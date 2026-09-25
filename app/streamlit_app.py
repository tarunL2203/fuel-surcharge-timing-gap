"""SYNTHETIC local app and Snowflake deployment entry point."""
from pathlib import Path
import os
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]
MODE=os.getenv('FUEL_MODE','local')
st.set_page_config(page_title='The Broker’s Two Clocks',layout='wide')
st.title('The Broker’s Two Clocks')
st.warning('SYNTHETIC DRY RUN • Illustrative contract terms • Diagnostic, not predictive')

def query(sql,params=None):
 if MODE=='snowflake':
  from snowflake.snowpark.context import get_active_session
  df=get_active_session().sql(sql,params=params or []).to_pandas()
 else:
  import duckdb
  path=ROOT/'local/SYNTHETIC_fuel.duckdb'
  if not path.exists():st.info('Run python local/run_pipeline.py all first.');st.stop()
  with duckdb.connect(str(path),read_only=True) as c:df=c.execute(sql,params or []).df()
 df.columns=[x.lower() for x in df.columns];return df

params=query('SELECT * FROM MODEL.V_PARAMETERS')
asof=params.iloc[0].as_of_date
status=query("SELECT MAX(d.week_date) latest_date,DATEDIFF('day',MAX(d.week_date),MAX(p.as_of_date)) days_old FROM MODEL.DT_DIESEL_WEEKLY d CROSS JOIN MODEL.V_PARAMETERS p")
latest=pd.Timestamp(status.iloc[0].latest_date)
age=int(status.iloc[0].days_old)
if age>int(params.iloc[0].freshness_max_days):st.error(f'STALE: latest accepted week is {latest.date()}, {age} days before the configured as-of date.')
else:st.caption(f'Fresh as of {pd.Timestamp(asof).date()}. Latest accepted week: {latest.date()}. This is a fixed-date replay, not a live feed.')
page=st.sidebar.radio('Page',['Overview','Scenario explorer','Data quality','Assumptions'])
regions=query('SELECT DISTINCT geo_id FROM MODEL.DT_DIESEL_WEEKLY ORDER BY geo_id').geo_id.tolist()
region=st.sidebar.selectbox('Region',regions,index=regions.index('US'))
reset=st.sidebar.selectbox('Shipper reset',['WEEKLY','MONTHLY','QUARTERLY'],index=1)
clause=st.sidebar.checkbox('Seasonal clause',False)
bounds=query('SELECT MIN(week_date) first_date,MAX(week_date) last_date FROM MODEL.DT_DIESEL_WEEKLY')
dates=st.sidebar.date_input('Date range',value=(pd.Timestamp(bounds.iloc[0].first_date).date(),pd.Timestamp(bounds.iloc[0].last_date).date()))
if len(dates)!=2:st.info('Select both dates.');st.stop()
filters=[region,reset,clause,dates[0],dates[1]]
where='geo_id=? AND reset_frequency=? AND seasonal_clause=? AND week_date BETWEEN ? AND ?'
if page in ['Overview','Scenario explorer']:
 series=query('SELECT week_date,carrier_fsc,shipper_fsc,spread,dollars_per_1000_loads,complete_period FROM MODEL.DT_MARGIN_SPREAD WHERE '+where+' ORDER BY week_date',filters)
 if series.empty:st.info('No eligible weeks for this selection.');st.stop()
 stats=query('SELECT AVG(spread) mean_spread,AVG(dollars_per_1000_loads) mean_dollars,AVG(CASE WHEN spread<0 THEN 1.0 ELSE 0.0 END) squeeze_share FROM MODEL.DT_MARGIN_SPREAD WHERE '+where+' AND complete_period',filters).iloc[0]
 a,b,c=st.columns(3);a.metric('Mean spread ($/mile)',f'{stats.mean_spread:.4f}');b.metric('Mean $ per 1,000 loads',f'{stats.mean_dollars:,.0f}');c.metric('Squeeze-week share',f'{stats.squeeze_share:.1%}')
 st.caption('Summary metrics exclude the current unfinished reset period. Each observation assumes 1,000 loads of the configured distance; this is not actual company revenue. Regions overlap and must not be summed.')
 title=f'SYNTHETIC: {reset.lower()} reset timing exposure | {region} | {dates[0]} to {dates[1]}'
 st.subheader(title);st.line_chart(series.set_index('week_date')[['spread']]);st.caption('The weekly chart includes unfinished periods; the complete_period column identifies them in the table below.')
 st.dataframe(series,width='stretch')
 st.subheader('SYNTHETIC: regime and season averages for selected completed periods')
 st.dataframe(query('SELECT regime,season,COUNT(*) AS weeks,AVG(spread) mean_spread FROM MODEL.DT_MARGIN_SPREAD WHERE '+where+' AND complete_period GROUP BY regime,season ORDER BY regime,season',filters),width='stretch')
 st.subheader('SYNTHETIC: worst contiguous four-week stretches in the selected dates')
 st.dataframe(query('WITH w AS (SELECT week_date,COUNT(*) OVER win n,MIN(week_date) OVER win first_date,AVG(spread) OVER win mean_spread FROM MODEL.DT_MARGIN_SPREAD WHERE '+where+" WINDOW win AS (ORDER BY week_date ROWS BETWEEN 3 PRECEDING AND CURRENT ROW)) SELECT * FROM w WHERE n=4 AND DATEDIFF('day',first_date,week_date)=21 ORDER BY mean_spread,week_date LIMIT 5",filters),width='stretch')
 if page=='Scenario explorer':
  st.info('The controls compare the six predefined contracts. A seasonal clause changes price, so an improvement does not prove shipper acceptance. Review the stored sensitivity output before proposing a rate.')
  st.dataframe(query('SELECT * FROM MODEL.DT_SCENARIO_SUMMARY WHERE geo_id=? ORDER BY scenario_id',[region]),width='stretch')
  st.caption('The table above uses each scenario’s full completed-period history; it is not date-filtered. Weekly, monthly and quarterly endpoints differ.')
elif page=='Data quality':
 st.subheader('SYNTHETIC: accepted loads and blocked attempts');st.dataframe(query('SELECT * FROM MODEL.V_LOAD_LOG ORDER BY loaded_at,load_id'),width='stretch')
 st.subheader('SYNTHETIC: quarantined rows');st.dataframe(query('SELECT * FROM MODEL.V_QUARANTINE'),width='stretch')
 st.subheader('SYNTHETIC: missing weeks and excluded periods');st.dataframe(query('SELECT * FROM MODEL.V_MISSING_WEEKS ORDER BY geo_id,week_date'),width='stretch');st.dataframe(query('SELECT * FROM MODEL.V_PERIOD_EXCLUSIONS'),width='stretch')
 st.caption('Blocked batches do not change accepted prices. Historical rejected rows are tracked so an unchanged source rerun is a no-op.')
else:
 st.subheader('ILLUSTRATIVE assumptions');st.dataframe(params,width='stretch')
 st.markdown('Both clocks use the same regional index and fuel formula. Heating season means October–March. No real surcharge contract or company financial data was used. Centered seasonal averages are descriptive and include future observations. Real deployment remains gated on source profiling.')
