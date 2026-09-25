"""Static page evidence, explicitly not browser screenshots."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import duckdb
from run_pipeline import DB,ROOT
c=duckdb.connect(str(DB),read_only=True)
views={
 'overview':("SELECT scenario_id,ROUND(mean_spread,5) mean_spread,ROUND(squeeze_share,4) squeeze_share FROM model.dt_scenario_summary WHERE geo_id='US' ORDER BY scenario_id",'US contract summaries; scenario-specific completed periods'),
 'scenario_explorer':("SELECT week_date,scenario_id,ROUND(carrier_fsc,4) carrier_fsc,ROUND(shipper_fsc,4) shipper_fsc,ROUND(spread,4) spread FROM model.dt_margin_spread WHERE geo_id='US' AND scenario_id='S5' AND week_date BETWEEN DATE '2022-01-03' AND DATE '2022-02-21' ORDER BY week_date",'US quarterly contract, 2022-01-03 to 2022-02-21'),
 'data_quality':('SELECT load_id,status,inserted,quarantined,raw_rows,freshness FROM model.v_load_log ORDER BY load_id','Four replay events, as of 2026-09-23'),
 'assumptions':('SELECT base_price,mpg,step_up_per_mile,load_miles,index_lag_weeks,as_of_date FROM model.v_parameters','Illustrative values, fixed 2026-09-23 replay date')}
for name,(sql,title) in views.items():
 df=c.sql(sql).df();fig,ax=plt.subplots(figsize=(12,4));ax.axis('off');t=ax.table(cellText=df.astype(str).values,colLabels=df.columns,loc='center');t.auto_set_font_size(False);t.set_fontsize(8);t.scale(1,1.8)
 ax.set_title('SYNTHETIC static '+name.replace('_',' ')+' view\n'+title,fontsize=12)
 fig.tight_layout();fig.savefig(ROOT/f'outputs/phase_5/SYNTHETIC_{name}_view.png',dpi=130);plt.close(fig)
c.close()
