"""Write executable evidence for the eight planted traps and generation contract."""
import json
import duckdb,pandas as pd
from run_pipeline import ROOT,DB,export
c=duckdb.connect(str(DB),read_only=True);c.execute('SET threads=1')
traps=[('T1',3,"SELECT COUNT(*) FROM read_csv_auto('outputs/phase_1/SYNTHETIC_missing_source_weeks.csv')"),('T2',2,"SELECT SUM(row_count-1) FROM read_csv_auto('outputs/phase_1/SYNTHETIC_duplicates.csv')"),('T3',1,"SELECT COUNT(*) FROM raw.quarantine WHERE reason='OUT_OF_RANGE' AND load_id=1"),('T4',1,"SELECT COUNT(*) FROM raw.quarantine WHERE reason='NULL_VALUE' AND load_id=1"),('T5',44,"SELECT COUNT(*) FROM raw.normalizations WHERE load_id=1"),('T6',3,"SELECT COUNT(*) FROM listing.eia_attributes WHERE variable<>'DIESEL_RETAIL_ONHWY_WEEKLY'"),('T7',10,"SELECT COUNT(*) FROM (SELECT DISTINCT geo_id FROM listing.eia_timeseries EXCEPT SELECT geo_id FROM listing.geography_index)"),('T8',16,"SELECT days_old FROM raw.load_log WHERE load_id=1")]
rows=[]
for trap,expected,q in traps:
 actual=c.sql(q).fetchone()[0];rows.append(dict(trap=trap,expected=expected,actual=actual,passed=actual==expected))
 if actual!=expected:raise AssertionError((trap,actual,expected))
pd.DataFrame(rows).to_csv(ROOT/'outputs/phase_1/SYNTHETIC_trap_detection.csv',index=False)
assert c.sql('SELECT COUNT(*) FROM model.dt_margin_spread').fetchone()[0]==85044
assert c.sql('SELECT COUNT(*) FROM listing.eia_timeseries').fetchone()[0]==14947
# Verify the generator's declared regime windows and plateau contract on US prices.
truth=json.loads((ROOT/'data/sample/SYNTHETIC_planted_truth.json').read_text());windows=pd.DataFrame(truth['regimes']);c.register('truth_windows',windows)
export(c,"""SELECT w.truth,w.start,w.end,(MAX(CASE WHEN d.week_date=CAST(w.end AS DATE) THEN price END)/MAX(CASE WHEN d.week_date=CAST(w.start AS DATE) THEN price END))-1 window_change FROM truth_windows w JOIN model.dt_diesel_weekly d ON d.week_date BETWEEN CAST(w.start AS DATE) AND CAST(w.end AS DATE) WHERE geo_id='US' GROUP BY ALL ORDER BY w.start""",'outputs/phase_1/SYNTHETIC_generator_regimes.csv')
plateaus=pd.DataFrame(truth['plateaus']);c.register('plateau_windows',plateaus)
export(c,"""SELECT p.start,p.end,COUNT(*) AS weeks,MAX(ABS(change_4week)) max_abs_4week_change,COUNT(*)>=26 AND MAX(ABS(change_4week))<0.02 passed FROM plateau_windows p JOIN model.dt_diesel_weekly d ON d.week_date BETWEEN CAST(p.start AS DATE) AND CAST(p.end AS DATE) WHERE geo_id='US' GROUP BY ALL ORDER BY p.start""",'outputs/phase_1/SYNTHETIC_generator_plateaus.csv')
# Export same-window contract comparison to avoid different partial-period cutoffs.
export(c,"""SELECT scenario_id,MIN(week_date) first_date,MAX(week_date) last_date,COUNT(*) AS weeks,AVG(spread) mean_spread,AVG(dollars_per_1000_loads) mean_dollars_per_1000_loads,AVG(CASE WHEN spread<0 THEN 1.0 ELSE 0.0 END) squeeze_share FROM model.dt_margin_spread WHERE geo_id='US' AND week_date<DATE_TRUNC('quarter',as_of_date) GROUP BY scenario_id ORDER BY scenario_id""",'outputs/phase_4/SYNTHETIC_same_window_contracts.csv')
export(c,'SELECT * FROM model.v_missing_weeks ORDER BY geo_id,week_date','outputs/phase_3/SYNTHETIC_missing_week_log.csv')
export(c,'SELECT * FROM model.v_period_exclusions ORDER BY geo_id,reset_frequency,period','outputs/phase_3/SYNTHETIC_period_exclusion_log.csv')
export(c,'SELECT geo_id,month_number,COUNT(seasonal_ratio) valid_windows,AVG(seasonal_ratio) seasonal_index FROM model.dt_diesel_weekly GROUP BY geo_id,month_number ORDER BY geo_id,month_number','outputs/phase_4/SYNTHETIC_monthly_seasonal_index.csv')
print('8/8 traps verified; final spread rows 85044; generation window evidence exported.')
c.close()
