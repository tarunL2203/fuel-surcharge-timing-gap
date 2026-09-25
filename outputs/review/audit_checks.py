"""Read-only independent audit. Run with the project's pinned environment.
Usage: python audit_checks.py ORIGINAL_CHECKOUT RERUN_CHECKOUT
Writes JSON to stdout; never changes either checkout.
"""
import sys,json,hashlib,re
from pathlib import Path
import pandas as pd
import duckdb,sqlglot
original,root=map(Path,sys.argv[1:3]);out={}; checks=[]
def check(name,actual,expected):
    ok=bool(actual==expected);checks.append(dict(check=name,actual=actual,expected=expected,passed=ok))
s=pd.read_csv(root/'data/sample/SYNTHETIC_eia_timeseries.csv'); d=s[s.variable=='DIESEL_RETAIL_ONHWY_WEEKLY'].copy();d['week']=pd.to_datetime(d.date)-pd.to_timedelta(pd.to_datetime(d.date).dt.weekday,unit='d')
regions=['US','PADD1','PADD1A','PADD1B','PADD1C','PADD2','PADD3','PADD4','PADD5','PADD5XCA','CA']
weeks=pd.date_range('2002-01-07','2026-09-07',freq='7D');pairs=set(zip(d.geo_id,d.week)); missing=sorted((g,str(w.date())) for g in regions for w in weeks if (g,w) not in pairs)
check('listing rows',len(s),14947);check('weeks',len(weeks),1288);check('regions',sorted(d.geo_id.unique()),sorted(regions));check('diesel distinct pairs',len(pairs),14165)
check('T1',missing,[('PADD4',x) for x in ['2011-03-07','2011-03-14','2011-03-21']]);check('T2',sorted(d[d.duplicated()].date.tolist()),['2019-06-03','2019-06-10'])
check('T3',list(map(tuple,d[d.value>8][['geo_id','date']].values)),[('PADD3','2016-02-08')]);check('T4',list(map(tuple,d[d.value.isna()][['geo_id','date']].values)),[('PADD2','2014-11-10')]); shifted=d[pd.to_datetime(d.date).dt.weekday!=0];check('T5',len(shifted),44);check('T5 locations',sorted(set(str(x.date()) for x in shifted.week)),['2015-05-25','2016-05-30','2020-05-25','2023-05-29']);check('T6 rows',len(s)-len(d),780);check('T7',pd.read_csv(root/'data/sample/SYNTHETIC_geography_index.csv').geo_id.tolist(),['US']);check('T8',(pd.Timestamp('2026-09-23')-d.week.max()).days,16);check('synthetic names',bool(d.variable_name.str.endswith('(SYNTHETIC)').all()),True)
out['decoys']=s[s.variable!= 'DIESEL_RETAIL_ONHWY_WEEKLY'].groupby(['variable','unit','geo_id']).size().to_dict().__str__()
c=duckdb.connect(str(root/'local/SYNTHETIC_fuel.duckdb'),read_only=True)
logs=c.sql('select load_id,status,inserted,updated,quarantined,normalized,raw_rows,days_old,freshness from raw.load_log order by load_id').fetchall();out['load_events']=logs
check('load states',[(r[1],r[6],r[7],r[8]) for r in logs],[('PASSED_WITH_QUARANTINE',14163,16,'STALE'),('PASSED',14174,9,'FRESH'),('PASSED',14174,9,'FRESH'),('BLOCKED',14174,9,'FRESH')]);check('rerun delta',list(logs[2][2:4]),[0,0]);check('blocked invalid',logs[3][4],11)
check('quarantine',c.sql('select reason,count(*) from raw.quarantine group by reason order by reason').fetchall(),[('NULL_VALUE',1),('OUT_OF_RANGE',1)])
check('normalizations',c.sql('select count(*) from raw.normalizations').fetchone()[0],44)
r=c.sql('select * from raw.diesel_weekly').df(); m=c.sql('select * from model.dt_margin_spread').df();check('scenario rows',len(m),85044)
check('INV-01',int((m.loc[m.is_control,'spread']!=0).sum()),0);check('INV-02',len(m),len(r)*6);check('INV-03',list(logs[2][2:4]),[0,0]); n=m[~m.seasonal_clause];bad=((n.index_price>n.reset_price)&(n.spread>0))|((n.index_price<n.reset_price)&(n.spread<0));check('INV-04 / E4',int(bad.sum()),0)
summary=c.sql('select * from model.dt_scenario_summary').df().set_index(['geo_id','scenario_id']);summed=m[m.complete_period].groupby(['geo_id','scenario_id']).spread.sum();out['INV05_max_error']=float((summary.sum_spread-summed).abs().max());check('INV-05',out['INV05_max_error']<1e-10,True)
truth=json.loads((root/'data/sample/SYNTHETIC_planted_truth.json').read_text());dw=c.sql('select * from model.dt_diesel_weekly').df();e1=dw[dw.month_number==1].groupby('geo_id').seasonal_ratio.mean()-1;out['E1_max_error']=max(abs(e1[g]-v[1]) for g,v in truth['regions'].items());check('E1',bool(out['E1_max_error']<=.01),True)
conf=[]
for t in truth['regimes']:
    z=dw[(dw.geo_id=='US')&(dw.week_date>=t['start'])&(dw.week_date<=t['end'])];conf.extend((t['truth'],p) for p in z.regime)
cm=pd.crosstab(pd.Series([x[0] for x in conf],name='truth'),pd.Series([x[1] for x in conf],name='predicted'));out['E2_confusion']=cm.to_dict();out['E2_shares']={k:float(cm.loc[k,k]/cm.loc[k].sum()) for k in cm.index};check('E2',min(out['E2_shares'].values())>=.7,True)
piv=r.pivot(index='week_date',columns='geo_id',values='price').dropna();piv=piv[piv.index.year<2026];offset=piv.div(piv.US,axis=0).mean()-1;out['E3_max_error']=max(abs(offset[g]-v[0]) for g,v in truth['regions'].items());check('E3',bool(out['E3_max_error']<=.01),True)
check('reset substitution',pd.read_csv(root/'outputs/phase_3/SYNTHETIC_reset_substitutions.csv').to_dict('records'),[{'geo_id':'PADD4','reset_frequency':'MONTHLY','reset_period':'2011-03-01','reset_week':'2011-03-28'}])
check('initial missing clean',len(pd.read_csv(root/'outputs/phase_2/SYNTHETIC_initial_missing_clean_weeks.csv')),5)
common=m[(m.geo_id=='US')&(m.week_date<'2026-07-01')];out['memo_recomputed']=common.groupby('scenario_id').agg(mean_dollars=('dollars_per_1000_loads','mean'),squeeze_share=('spread',lambda a:(a<0).mean())).to_dict('index')
compare=[]
for folder in ['data/sample','outputs','sql']:
 for p in sorted((original/folder).rglob('*')):
  if not p.is_file() or 'review' in p.parts:continue
  target=root/p.relative_to(original)
  if not target.exists():continue
  if p.read_bytes()!=target.read_bytes():
   result={'path':str(p.relative_to(original)),'hash_match':False}
   if p.suffix=='.csv':
    a,b=pd.read_csv(p),pd.read_csv(target)
    if 'loaded_at' in a.columns:a=a.drop(columns='loaded_at');b=b.drop(columns='loaded_at');result['excluded_metadata']='loaded_at'
    try:pd.testing.assert_frame_equal(a,b,check_exact=False,rtol=1e-12,atol=1e-12);result['values_match']=True
    except AssertionError:result['values_match']=False
   compare.append(result)
out['changed_output_hashes']=compare
parse=[]
for p in sorted((root/'sql').glob('*.sql')):
 try:
  ast=sqlglot.parse(p.read_text(),read='snowflake');parse.append({'file':p.name,'parsed':True,'unsupported_command_nodes':sum(type(x).__name__=='Command' for x in ast)})
 except Exception as e:parse.append({'file':p.name,'parsed':False,'error':str(e)[:500]})
out['snowflake_parse']=parse
broken=[]
for p in original.rglob('*.md'):
 if any(x in p.parts for x in ['.git','.venv','review']):continue
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  if not (p.parent/target.split('#')[0]).exists():broken.append({'file':str(p.relative_to(original)),'target':target})
out['broken_relative_links']=broken;out['checks']=checks;out['failed_checks']=[x for x in checks if not x['passed']]
print(json.dumps(out,indent=2,default=str))
