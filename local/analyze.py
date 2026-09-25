from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run_pipeline import export,model,ROOT

def analyze(c):
 out=ROOT/'outputs/phase_4'
 summary=export(c,'SELECT * FROM model.dt_scenario_summary ORDER BY geo_id,scenario_id','outputs/phase_4/SYNTHETIC_summary.csv')
 regime=export(c,"SELECT geo_id,scenario_id,regime,season,COUNT(*) AS weeks,AVG(spread) mean_spread,AVG(dollars_per_1000_loads) mean_dollars_per_1000_loads FROM model.dt_margin_spread WHERE complete_period GROUP BY ALL ORDER BY ALL",'outputs/phase_4/SYNTHETIC_regime_season.csv')
 export(c,"""WITH r AS (SELECT geo_id,scenario_id,week_date,complete_period,COUNT(*) OVER w n,MIN(week_date) OVER w start_date,AVG(spread) OVER w mean_spread,AVG(dollars_per_1000_loads) OVER w mean_dollars_per_1000_loads FROM model.dt_margin_spread WINDOW w AS (PARTITION BY geo_id,scenario_id ORDER BY week_date ROWS BETWEEN 3 PRECEDING AND CURRENT ROW)),ranked AS (SELECT *,ROW_NUMBER() OVER (PARTITION BY geo_id,scenario_id ORDER BY mean_spread,week_date) rank FROM r WHERE n=4 AND DATEDIFF('day',start_date,week_date)=21) SELECT * FROM ranked WHERE rank<=5 ORDER BY geo_id,scenario_id,rank""",'outputs/phase_4/SYNTHETIC_worst_stretches.csv')
 clause=export(c,"""SELECT a.geo_id,a.scenario_id,b.scenario_id paired_scenario,a.season,COUNT(*) AS weeks,AVG(a.spread) without_clause,AVG(b.spread) with_clause,AVG(b.spread-a.spread) clause_uplift,AVG(GREATEST(0,-a.spread)) squeeze_without,AVG(GREATEST(0,-b.spread)) squeeze_with FROM model.dt_margin_spread a JOIN model.dt_margin_spread b ON a.geo_id=b.geo_id AND a.week_date=b.week_date AND ((a.scenario_id='S3' AND b.scenario_id='S4') OR (a.scenario_id='S5' AND b.scenario_id='S6')) WHERE a.complete_period AND b.complete_period GROUP BY ALL ORDER BY ALL""",'outputs/phase_4/SYNTHETIC_clause_effect.csv')
 export(c,"""WITH common AS (SELECT week_date FROM raw.diesel_weekly GROUP BY week_date HAVING COUNT(DISTINCT geo_id)=11) SELECT geo_id,scenario_id,COUNT(*) AS weeks,AVG(spread) mean_spread FROM model.dt_margin_spread JOIN common USING(week_date) WHERE complete_period GROUP BY ALL ORDER BY ALL""",'outputs/phase_4/SYNTHETIC_regions_common_window.csv')
 truth=json.loads((ROOT/'data/sample/SYNTHETIC_planted_truth.json').read_text())
 expected=pd.DataFrame([{'geo_id':g,'level_offset':v[0],'amplitude':v[1]} for g,v in truth['regions'].items()]);c.register('effect_truth',expected)
 seasonal=export(c,"""SELECT d.geo_id,AVG(seasonal_ratio)-1 recovered_amplitude,MAX(t.amplitude) planted_amplitude,ABS(AVG(seasonal_ratio)-1-MAX(t.amplitude)) AS recovery_error,ABS(AVG(seasonal_ratio)-1-MAX(t.amplitude))<=0.01 passed FROM model.dt_diesel_weekly d JOIN effect_truth t USING(geo_id) WHERE month_number=1 AND seasonal_ratio IS NOT NULL GROUP BY d.geo_id ORDER BY d.geo_id""",'outputs/phase_4/SYNTHETIC_E1_seasonality_recovery.csv')
 export(c,"""WITH common AS (SELECT week_date FROM raw.diesel_weekly GROUP BY week_date HAVING COUNT(DISTINCT geo_id)=11) SELECT r.geo_id,AVG(r.price/u.price)-1 recovered_offset,MAX(t.level_offset) planted_offset,ABS(AVG(r.price/u.price)-1-MAX(t.level_offset)) AS recovery_error,ABS(AVG(r.price/u.price)-1-MAX(t.level_offset))<=0.01 passed FROM raw.diesel_weekly r JOIN raw.diesel_weekly u ON r.week_date=u.week_date AND u.geo_id='US' JOIN common ON r.week_date=common.week_date JOIN effect_truth t ON r.geo_id=t.geo_id WHERE EXTRACT(YEAR FROM r.week_date)<2026 GROUP BY r.geo_id ORDER BY r.geo_id""",'outputs/phase_4/SYNTHETIC_E3_offset_recovery.csv')
 windows=pd.DataFrame(truth['regimes']);c.register('regime_truth',windows)
 export(c,"""SELECT t.truth,d.regime predicted,COUNT(*) AS weeks FROM model.dt_diesel_weekly d JOIN regime_truth t ON d.week_date BETWEEN CAST(t.start AS DATE) AND CAST(t.end AS DATE) WHERE geo_id='US' GROUP BY ALL ORDER BY ALL""",'outputs/phase_4/SYNTHETIC_E2_confusion_matrix.csv')
 export(c,"""SELECT t.truth,COUNT(*) AS weeks,AVG(CASE WHEN d.regime=t.truth THEN 1.0 ELSE 0.0 END) recovered_share,AVG(CASE WHEN d.regime=t.truth THEN 1.0 ELSE 0.0 END)>=0.70 passed FROM model.dt_diesel_weekly d JOIN regime_truth t ON d.week_date BETWEEN CAST(t.start AS DATE) AND CAST(t.end AS DATE) WHERE geo_id='US' GROUP BY ALL ORDER BY ALL""",'outputs/phase_4/SYNTHETIC_E2_recovery.csv')
 # One-factor-at-a-time scenarios: ranges set before examining outputs.
 frames=[]
 baseline_parameters=c.execute('SELECT * FROM config.parameters').fetchall()
 baseline_spread=c.execute('SELECT * FROM model.dt_margin_spread ORDER BY geo_id,scenario_id,week_date').fetchall()
 for param,values in {'base_price':[1,1.25,1.5],'mpg':[5.5,6,7],'step_up_per_mile':[.01,.02,.04],'regime_threshold':[.02,.03,.05],'load_miles':[250,500,1000],'index_lag_weeks':[0,1]}.items():
  for val in values:
   c.execute('BEGIN TRANSACTION')
   try:
    c.execute('UPDATE config.parameters SET '+param+'=?',[val]);model(c)
    f=c.execute("SELECT scenario_id,AVG(spread) mean_spread,AVG(dollars_per_1000_loads) mean_dollars_per_1000_loads,AVG(CASE WHEN spread<0 THEN 1.0 ELSE 0.0 END) squeeze_share,COUNT(*) AS weeks FROM model.dt_margin_spread WHERE geo_id='US' AND complete_period GROUP BY scenario_id ORDER BY scenario_id").fetchdf()
    f.insert(0,'value',val);f.insert(0,'parameter',param);frames.append(f)
   finally:c.execute('ROLLBACK')
   assert c.execute('SELECT * FROM config.parameters').fetchall()==baseline_parameters, 'Sensitivity parameter isolation failed'
 assert c.execute('SELECT * FROM model.dt_margin_spread ORDER BY geo_id,scenario_id,week_date').fetchall()==baseline_spread, 'Sensitivity model isolation failed'
 pd.concat(frames).to_csv(out/'SYNTHETIC_sensitivity.csv',index=False)
 # Plain chart outputs for environments without an app browser.
 def save(name,title):
  plt.title('SYNTHETIC: '+title,fontsize=10);plt.tight_layout();plt.savefig(out/name,dpi=130);plt.close()
 series=c.sql("SELECT week_date,scenario_id,spread FROM model.dt_margin_spread WHERE geo_id='US' AND scenario_id IN ('S1','S3','S5') ORDER BY week_date").df()
 fig,ax=plt.subplots(figsize=(11,4))
 for s,g in series.groupby('scenario_id'):ax.plot(g.week_date,g.spread,label=s,lw=.8)
 ax.axhline(0,color='black',lw=.6);ax.legend();ax.set_ylabel('Dollars per mile');save('SYNTHETIC_spread.png','slower resets create timing exposure | US | 2002-01-07 to 2026-09-14 | includes partial current periods')
 h=regime[(regime.geo_id=='US')&(regime.scenario_id=='S5')].pivot(index='regime',columns='season',values='mean_spread')
 fig,ax=plt.subplots(figsize=(7,4));im=ax.imshow(h.values,cmap='RdBu',vmin=-.2,vmax=.2);ax.set_xticks(range(len(h.columns)),h.columns);ax.set_yticks(range(len(h.index)),h.index);fig.colorbar(im,label='Dollars per mile');save('SYNTHETIC_regime_season.png','regime and season averages | S5 US | 2002-01-07 to 2026-06-29')
 x=clause[(clause.geo_id=='US')&(clause.season=='HEATING')];x.plot.bar(x='scenario_id',y=['squeeze_without','squeeze_with'],figsize=(7,4));plt.ylim(bottom=0);plt.ylabel('Mean negative spread magnitude ($/mile)');save('SYNTHETIC_clause.png','clause reduces modeled heating squeeze | US | completed periods through 2026-08')
 seasonal.plot.bar(x='geo_id',y=['planted_amplitude','recovered_amplitude'],figsize=(9,4));plt.ylim(bottom=0);plt.ylabel('January amplitude (fraction)');save('SYNTHETIC_recovery.png','planted vs recovered January effect | full windows | Jan 2003 to Jan 2026')
 regions=pd.read_csv(out/'SYNTHETIC_regions_common_window.csv');regions[regions.scenario_id=='S5'].plot.bar(x='geo_id',y='mean_spread',figsize=(9,4));plt.axhline(0,color='black',lw=.6);plt.ylabel('Mean spread ($/mile)');save('SYNTHETIC_regions.png','same-week regional exposure comparison | S5 | 2002-01-07 to 2026-06-29')
 # Known-answer six-week example, computed by SQL.
 export(c,"""WITH v AS (SELECT * FROM (VALUES (DATE '2026-01-05',2.45),(DATE '2026-01-12',2.75),(DATE '2026-01-19',3.05),(DATE '2026-01-26',2.15),(DATE '2026-02-02',1.25),(DATE '2026-02-09',1.10)) t(week_date,price)), f AS (SELECT *,GREATEST(0,(price-1.25)/6) carrier_fsc,GREATEST(0,(FIRST_VALUE(price) OVER(ORDER BY week_date)-1.25)/6) shipper_fsc FROM v) SELECT *,shipper_fsc-carrier_fsc spread FROM f ORDER BY week_date""",'outputs/phase_0/SYNTHETIC_six_week_example.csv')
 # SQL-derived memo rows used verbatim by report writer.
 export(c,"SELECT * FROM model.dt_scenario_summary WHERE geo_id='US' ORDER BY scenario_id",'outputs/phase_5/SYNTHETIC_memo_evidence.csv')
