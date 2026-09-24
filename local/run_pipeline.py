"""SYNTHETIC pipeline; business metrics are SQL, Python orchestrates only."""
from pathlib import Path
import sys,json,hashlib,time
import duckdb
from generate_sample_data import generate, VARIABLE
from render_snowflake import render,OBJECTS
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/sample'; DB=ROOT/'local/SYNTHETIC_fuel.duckdb'

def export(c,sql,path):
 path=ROOT/path;path.parent.mkdir(parents=True,exist_ok=True)
 c.sql(sql).df().to_csv(path,index=False)
 return c.sql(sql).df()

def setup(c):
 for s in ['listing','config','raw','model']:c.execute(f'CREATE SCHEMA IF NOT EXISTS {s}')
 c.execute('''CREATE OR REPLACE TABLE config.parameters AS SELECT 1.25::DOUBLE base_price,6.0::DOUBLE mpg,0::INTEGER index_lag_weeks,0.02::DOUBLE step_up_per_mile,0.03::DOUBLE regime_threshold,500::INTEGER load_miles,10::INTEGER freshness_max_days,1.0::DOUBLE min_price,8.0::DOUBLE max_price,0.05::DOUBLE batch_max_bad_pct,DATE '2026-09-23' as_of_date''')
 c.execute("""CREATE OR REPLACE TABLE config.contract_scenarios AS SELECT * FROM (VALUES ('S1','WEEKLY',false,true),('S2','WEEKLY',true,false),('S3','MONTHLY',false,false),('S4','MONTHLY',true,false),('S5','QUARTERLY',false,false),('S6','QUARTERLY',true,false)) t(scenario_id,reset_frequency,seasonal_clause,is_control)""")
 c.execute('CREATE TABLE IF NOT EXISTS raw.diesel_weekly(geo_id VARCHAR,week_date DATE,price DECIMAL(12,3),loaded_at TIMESTAMP,load_id INTEGER,PRIMARY KEY(geo_id,week_date))')
 c.execute('CREATE TABLE IF NOT EXISTS raw.source_seen(geo_id VARCHAR,week_date DATE,fingerprint VARCHAR PRIMARY KEY)')
 c.execute('CREATE TABLE IF NOT EXISTS raw.quarantine(load_id INTEGER,geo_id VARCHAR,week_date DATE,price DOUBLE,reason VARCHAR)')
 c.execute('CREATE TABLE IF NOT EXISTS raw.normalizations(load_id INTEGER,geo_id VARCHAR,source_date DATE,week_date DATE)')
 c.execute('CREATE TABLE IF NOT EXISTS raw.load_log(load_id INTEGER,status VARCHAR,inserted INTEGER,updated INTEGER,quarantined INTEGER,normalized INTEGER,raw_rows INTEGER,days_old INTEGER,freshness VARCHAR,reason VARCHAR,loaded_at TIMESTAMP)')

def log(c,lid,status,ins=0,upd=0,bad=0,norm=0,reason=''):
 c.execute('''INSERT INTO raw.load_log SELECT ?,?,?,?,?,?,COUNT(*),DATEDIFF('day',MAX(week_date),MAX(as_of_date)),CASE WHEN DATEDIFF('day',MAX(week_date),MAX(as_of_date))>MAX(freshness_max_days) THEN 'STALE' ELSE 'FRESH' END,?,CURRENT_TIMESTAMP FROM raw.diesel_weekly CROSS JOIN config.parameters''',[lid,status,ins,upd,bad,norm,reason])

def land(c,df):
 lid=c.sql('SELECT COALESCE(MAX(load_id),0)+1 FROM raw.load_log').fetchone()[0]
 required=['geo_id','variable','variable_name','date','value','unit']
 if sorted(df.columns)!=sorted(required):log(c,lid,'BLOCKED',reason='SCHEMA_MISMATCH');return
 c.register('incoming_frame',df)
 if c.sql('SELECT COUNT(*) FROM incoming_frame WHERE (date IS NOT NULL AND TRY_CAST(date AS DATE) IS NULL) OR (value IS NOT NULL AND TRY_CAST(value AS DOUBLE) IS NULL)').fetchone()[0]:log(c,lid,'BLOCKED',reason='SCHEMA_CAST_MISMATCH');return
 c.execute("CREATE OR REPLACE TEMP TABLE incoming AS SELECT CAST(geo_id AS VARCHAR) geo_id, CAST(date AS DATE) source_date, CAST(date_trunc('week',CAST(date AS DATE)) AS DATE) week_date, CAST(value AS DOUBLE) price, unit FROM incoming_frame WHERE variable=?",[VARIABLE])
 if c.sql('SELECT COUNT(*) FROM incoming').fetchone()[0]==0:log(c,lid,'BLOCKED',reason='EMPTY_SOURCE');return
 if c.sql("SELECT COUNT(*) FROM incoming WHERE unit IS DISTINCT FROM 'USD per gallon'").fetchone()[0]:log(c,lid,'BLOCKED',reason='UNIT_MISMATCH');return
 if c.sql('SELECT COUNT(*) FROM incoming WHERE geo_id IS NULL OR source_date IS NULL').fetchone()[0]:log(c,lid,'BLOCKED',reason='NULL_KEY');return
 c.execute("CREATE OR REPLACE TEMP TABLE fingerprinted AS SELECT DISTINCT *,md5(geo_id||'|'||CAST(source_date AS VARCHAR)||'|'||COALESCE(CAST(price AS VARCHAR),'NULL')||'|'||unit) fingerprint FROM incoming")
 c.execute('CREATE OR REPLACE TEMP TABLE changed_keys AS SELECT DISTINCT geo_id,week_date FROM fingerprinted WHERE fingerprint NOT IN (SELECT fingerprint FROM raw.source_seen) UNION SELECT DISTINCT s.geo_id,s.week_date FROM raw.source_seen s JOIN fingerprinted f USING(geo_id,week_date) WHERE s.fingerprint NOT IN (SELECT fingerprint FROM fingerprinted)')
 c.execute('CREATE OR REPLACE TEMP TABLE delta AS SELECT f.* FROM fingerprinted f JOIN changed_keys USING(geo_id,week_date)')
 n=c.sql('SELECT COUNT(*) FROM delta').fetchone()[0]
 if not n:log(c,lid,'PASSED',reason='NO_CHANGE');return
 c.execute('''CREATE OR REPLACE TEMP TABLE classified AS WITH conflicts AS (SELECT geo_id,week_date,COUNT(DISTINCT COALESCE(CAST(price AS VARCHAR),'NULL')) variants FROM incoming GROUP BY ALL)
 SELECT d.*,CASE WHEN variants>1 THEN 'CONFLICTING_DUPLICATE' WHEN price IS NULL THEN 'NULL_VALUE' WHEN NOT isfinite(price) OR price<p.min_price OR price>p.max_price THEN 'OUT_OF_RANGE' END reason
 FROM delta d JOIN conflicts USING(geo_id,week_date) CROSS JOIN config.parameters p''')
 bad=c.sql('SELECT COUNT(*) FROM classified WHERE reason IS NOT NULL').fetchone()[0]
 if c.sql('SELECT ?*1.0/?>batch_max_bad_pct FROM config.parameters',params=[bad,n]).fetchone()[0]:
  log(c,lid,'BLOCKED',bad=bad,reason='BAD_ROW_THRESHOLD');return
 c.execute('CREATE OR REPLACE TEMP TABLE accepted AS SELECT DISTINCT geo_id,week_date,CAST(price AS DECIMAL(12,3)) price FROM classified WHERE reason IS NULL')
 ins=c.sql('SELECT COUNT(*) FROM accepted a LEFT JOIN raw.diesel_weekly r USING(geo_id,week_date) WHERE r.geo_id IS NULL').fetchone()[0]
 upd=c.sql('SELECT COUNT(*) FROM accepted a JOIN raw.diesel_weekly r USING(geo_id,week_date) WHERE a.price IS DISTINCT FROM r.price').fetchone()[0]
 norm=c.sql('SELECT COUNT(*) FROM delta WHERE source_date<>week_date').fetchone()[0]
 c.execute('BEGIN')
 try:
  c.execute('INSERT INTO raw.quarantine SELECT ?,geo_id,week_date,price,reason FROM classified WHERE reason IS NOT NULL',[lid])
  c.execute('INSERT INTO raw.normalizations SELECT ?,geo_id,source_date,week_date FROM delta WHERE source_date<>week_date',[lid])
  c.execute('''INSERT INTO raw.diesel_weekly SELECT geo_id,week_date,price,CURRENT_TIMESTAMP,? FROM accepted
  ON CONFLICT(geo_id,week_date) DO UPDATE SET price=excluded.price,loaded_at=excluded.loaded_at,load_id=excluded.load_id WHERE raw.diesel_weekly.price IS DISTINCT FROM excluded.price''',[lid])
  c.execute('DELETE FROM raw.source_seen WHERE (geo_id,week_date) IN (SELECT geo_id,week_date FROM changed_keys)')
  c.execute('INSERT INTO raw.source_seen SELECT geo_id,week_date,fingerprint FROM delta ON CONFLICT DO NOTHING')
  log(c,lid,'PASSED_WITH_QUARANTINE' if bad else 'PASSED',ins,upd,bad,norm,'INVALID_CORRECTIONS_KEEP_LAST_ACCEPTED' if bad else '')
  c.execute('COMMIT')
 except Exception:c.execute('ROLLBACK');raise

def model(c):
 for file,name in OBJECTS:c.execute(f'CREATE OR REPLACE TABLE model.{name} AS '+(ROOT/'sql/selects'/file).read_text())
 for view,source in [('v_parameters','config.parameters'),('v_load_log','raw.load_log'),('v_quarantine','raw.quarantine')]:c.execute(f'CREATE OR REPLACE VIEW model.{view} AS SELECT * FROM {source}')
 c.execute("""CREATE OR REPLACE VIEW model.v_missing_weeks AS SELECT g.geo_id,CAST(w.week_date AS DATE) week_date FROM (SELECT DISTINCT geo_id FROM raw.diesel_weekly) g CROSS JOIN generate_series((SELECT MIN(week_date) FROM raw.diesel_weekly),(SELECT as_of_date FROM config.parameters),INTERVAL '7 days') w(week_date) LEFT JOIN raw.diesel_weekly r ON r.geo_id=g.geo_id AND r.week_date=w.week_date WHERE r.geo_id IS NULL""")
 c.execute("""CREATE OR REPLACE VIEW model.v_period_exclusions AS WITH all_weeks AS (SELECT geo_id,week_date,true missing FROM model.v_missing_weeks UNION ALL SELECT geo_id,week_date,false FROM raw.diesel_weekly), periods AS (SELECT geo_id,'MONTHLY' reset_frequency,DATE_TRUNC('month',week_date) period,missing FROM all_weeks UNION ALL SELECT geo_id,'QUARTERLY',DATE_TRUNC('quarter',week_date),missing FROM all_weeks) SELECT geo_id,reset_frequency,period,COUNT(*) expected_weeks FROM periods GROUP BY ALL HAVING BOOL_AND(missing)""")

def profile(c):
 for name in ['eia_timeseries','eia_attributes','geography_index']:
  c.execute(f"CREATE OR REPLACE TABLE listing.{name} AS SELECT * FROM read_csv_auto('{DATA / ('SYNTHETIC_'+name+'.csv')}')")
 export(c,"SELECT variable,unit,count(*) row_count,min(date) first_date,max(date) latest_date FROM listing.eia_timeseries GROUP BY ALL",'outputs/phase_1/SYNTHETIC_variables.csv')
 export(c,"SELECT dayname(date) weekday,count(*) row_count FROM listing.eia_timeseries WHERE variable='"+VARIABLE+"' GROUP BY ALL",'outputs/phase_1/SYNTHETIC_weekdays.csv')
 export(c,"SELECT DISTINCT geo_id FROM listing.eia_timeseries EXCEPT SELECT geo_id FROM listing.geography_index",'outputs/phase_1/SYNTHETIC_unindexed_regions.csv')
 export(c,"SELECT geo_id,DATE_TRUNC('week',date) week_date,count(*) row_count FROM listing.eia_timeseries WHERE variable='"+VARIABLE+"' GROUP BY ALL HAVING count(*)>1",'outputs/phase_1/SYNTHETIC_duplicates.csv')
 c.execute("CREATE OR REPLACE TEMP TABLE expected AS SELECT geo_id,CAST(week_date AS DATE) week_date FROM (SELECT DISTINCT geo_id FROM listing.eia_timeseries WHERE variable='"+VARIABLE+"') g CROSS JOIN generate_series(DATE '2002-01-07',DATE '2026-09-07',INTERVAL '7 days') t(week_date)")
 export(c,"SELECT * FROM expected EXCEPT SELECT geo_id,CAST(DATE_TRUNC('week',date) AS DATE) FROM listing.eia_timeseries WHERE variable='"+VARIABLE+"'",'outputs/phase_1/SYNTHETIC_missing_source_weeks.csv')
 export(c,"""WITH w AS (SELECT geo_id,date,LAG(date) OVER(PARTITION BY geo_id ORDER BY date) prior_date FROM listing.eia_timeseries WHERE variable='DIESEL_RETAIL_ONHWY_WEEKLY') SELECT *,DATEDIFF('day',prior_date,date) gap_days FROM w WHERE DATEDIFF('day',prior_date,date)<>7""",'outputs/phase_1/SYNTHETIC_gaps.csv')

def validate(c):
 checks={
 'INV-01':"SELECT * FROM model.dt_margin_spread WHERE is_control AND spread<>0",
 'INV-02':"SELECT 'row_count' failure WHERE (SELECT COUNT(*) FROM model.dt_margin_spread)<>(SELECT COUNT(*)*6 FROM raw.diesel_weekly)",
 'INV-03':"SELECT * FROM raw.load_log WHERE load_id=3 AND (inserted<>0 OR updated<>0)",
 'INV-04':"SELECT * FROM model.dt_margin_spread WHERE NOT seasonal_clause AND ((index_price>reset_price AND spread>0) OR (index_price<reset_price AND spread<0))",
 'INV-05':"SELECT s.geo_id,s.scenario_id FROM model.dt_scenario_summary s JOIN (SELECT geo_id,scenario_id,SUM(spread) total FROM model.dt_margin_spread WHERE complete_period GROUP BY ALL) r USING(geo_id,scenario_id) WHERE ABS(s.sum_spread-r.total)>1e-10",
 'FSC_NONNEGATIVE':"SELECT * FROM model.dt_margin_spread WHERE carrier_fsc<0",
 'RESET_CONSTANT':"SELECT geo_id,scenario_id,reset_period FROM model.dt_margin_spread WHERE NOT seasonal_clause GROUP BY ALL HAVING MIN(shipper_fsc)<>MAX(shipper_fsc)",
 'LOAD_COUNTS':"SELECT * FROM raw.load_log WHERE (load_id=1 AND raw_rows<>14163) OR (load_id IN (2,3,4) AND raw_rows<>14174)",
 'BLOCKED_UNCHANGED':"SELECT * FROM raw.load_log WHERE load_id=4 AND (status<>'BLOCKED' OR inserted<>0 OR updated<>0)"}
 result=[]
 for k,q in checks.items():
  n=c.sql(q).shape[0];result.append({'check':k,'expected_failures':0,'actual_failures':n,'status':'PASS' if n==0 else 'FAIL'})
  if n:export(c,q,f'outputs/phase_4/SYNTHETIC_FAILURE_{k}.csv');raise AssertionError(k)
 import pandas as pd
 pd.DataFrame(result).to_csv(ROOT/'outputs/phase_4/SYNTHETIC_validation.csv',index=False)
 (ROOT/'sql/05_validation.sql').write_text('-- UNVERIFIED: confirm in Snowflake. Zero rows means PASS. Run INV-01 first.\n'+ '\n\n'.join('-- '+k+'\n'+__import__('sqlglot').transpile(q,read='duckdb',write='snowflake')[0]+';' for k,q in checks.items() if k not in ['LOAD_COUNTS','BLOCKED_UNCHANGED','INV-03']))
 return result

def main():
 start=time.monotonic();command=sys.argv[1] if len(sys.argv)>1 else 'all'
 if command=='teardown':
  DB.unlink(missing_ok=True);print('Local database removed (idempotent).');return
 if command=='all':
  generate();DB.unlink(missing_ok=True)
 c=duckdb.connect(str(DB));c.execute("SET threads=1");setup(c)
 for i in range(7):(ROOT/f'outputs/phase_{i}').mkdir(parents=True,exist_ok=True)
 if command in ['all','land']:
  profile(c)
  source=c.sql('SELECT * FROM listing.eia_timeseries').df()
  land(c,source)
  export(c,'SELECT * FROM expected EXCEPT SELECT geo_id,week_date FROM raw.diesel_weekly','outputs/phase_2/SYNTHETIC_initial_missing_clean_weeks.csv')
  import pandas as pd
  weekly=pd.read_csv(DATA/'SYNTHETIC_batch_2026-09-14.csv');source=pd.concat([source,weekly],ignore_index=True)
  land(c,source);before=c.sql('SELECT * FROM raw.diesel_weekly ORDER BY geo_id,week_date').fetchall()
  land(c,source);assert before==c.sql('SELECT * FROM raw.diesel_weekly ORDER BY geo_id,week_date').fetchall()
  source=pd.concat([source,pd.read_csv(DATA/'SYNTHETIC_batch_2026-09-21_corrupt.csv')],ignore_index=True)
  land(c,source);assert before==c.sql('SELECT * FROM raw.diesel_weekly ORDER BY geo_id,week_date').fetchall()
  for table in ['load_log','quarantine','normalizations']:export(c,f'SELECT * FROM raw.{table}',f'outputs/phase_2/SYNTHETIC_{table}.csv')
 model(c);render();validate(c)
 export(c,"SELECT geo_id,week_date,scenario_id,index_price,reset_price,carrier_fsc,shipper_fsc,spread FROM model.dt_margin_spread WHERE geo_id='US' AND scenario_id IN ('S1','S3','S5') AND week_date BETWEEN DATE '2021-12-06' AND DATE '2022-01-24' ORDER BY week_date,scenario_id",'outputs/phase_3/SYNTHETIC_clock_excerpt.csv')
 export(c,"SELECT DISTINCT geo_id,reset_frequency,reset_period,reset_week FROM model.dt_surcharge_clocks WHERE reset_frequency<>'WEEKLY' AND reset_week>DATE_TRUNC('week',reset_period)+CASE WHEN DATE_TRUNC('week',reset_period)<reset_period THEN INTERVAL '7 days' ELSE INTERVAL '0 days' END",'outputs/phase_3/SYNTHETIC_reset_substitutions.csv')
 from analyze import analyze
 analyze(c);validate(c)
 print(c.sql('SELECT load_id,status,inserted,updated,quarantined,raw_rows,freshness FROM raw.load_log').df().to_string(index=False))
 print('All invariants passed; elapsed seconds',round(time.monotonic()-start,2))
 c.close()
if __name__=='__main__':main()
