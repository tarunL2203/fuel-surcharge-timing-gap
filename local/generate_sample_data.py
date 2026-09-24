"""Generate the SYNTHETIC listing. Never represents EIA observations."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/sample'
REGIONS={'US':(0,.03),'PADD1':(.03,.06),'PADD1A':(.05,.06),'PADD1B':(.04,.06),'PADD1C':(.01,.04),'PADD2':(0,.03),'PADD3':(-.04,.02),'PADD4':(.02,.03),'PADD5':(.10,.02),'PADD5XCA':(.06,.02),'CA':(.15,.02)}
VARIABLE='DIESEL_RETAIL_ONHWY_WEEKLY'
def generate():
 DATA.mkdir(parents=True,exist_ok=True)
 rng=np.random.default_rng(42)
 dates=pd.date_range('2002-01-07','2026-09-21',freq='W-MON')
 level=np.full(len(dates),2.6)
 windows=[]
 for start in ['2005-04-04','2013-08-05','2021-12-06']:
  i=dates.get_loc(pd.Timestamp(start))
  level[i:i+26]=2.6*np.exp(np.linspace(0,np.log(1.8),26))
  level[i+26:i+52]=2.6*np.exp(np.linspace(np.log(1.8),0,26))
  for j,truth in [(i,'RISING'),(i+26,'FALLING')]:
   windows.append({'start':str(dates[j].date()),'end':str(dates[j+25].date()),'truth':truth})
 level*=1+rng.normal(0,.0008,len(dates))
 phase=2*np.pi*(dates.dayofyear.to_numpy()-15)/365.2425
 records=[]
 for geo,(offset,amplitude) in REGIONS.items():
  price=np.round(level*(1+offset)*(1+amplitude*np.cos(phase)),3)
  records.extend([dict(geo_id=geo,variable=VARIABLE,variable_name='Weekly retail on-highway diesel price (SYNTHETIC)',date=str(d.date()),value=float(v),unit='USD per gallon') for d,v in zip(dates,price)])
 clean=pd.DataFrame(records)
 history=clean[clean.date<='2026-09-07'].copy()
 history=history[~((history.geo_id=='PADD4')&history.date.isin(['2011-03-07','2011-03-14','2011-03-21']))]
 dup=history[(history.geo_id=='US')&history.date.isin(['2019-06-03','2019-06-10'])]
 history=pd.concat([history,dup],ignore_index=True)
 history.loc[(history.geo_id=='PADD3')&(history.date=='2016-02-08'),'value']*=100
 history.loc[(history.geo_id=='PADD2')&(history.date=='2014-11-10'),'value']=np.nan
 shifts=['2015-05-25','2016-05-30','2020-05-25','2023-05-29']
 for d in shifts:history.loc[history.date==d,'date']=str((pd.Timestamp(d)+pd.Timedelta(days=1)).date())
 attrs=[dict(variable=VARIABLE,variable_name='Weekly retail on-highway diesel price (SYNTHETIC)',unit='USD per gallon',frequency='Weekly',description='SYNTHETIC target')]
 for name,factor,unit in [('GASOLINE_RETAIL_REGULAR_WEEKLY',.85,'USD per gallon'),('DIESEL_ULSD_SPOT_WEEKLY',.70,'USD per gallon'),('CRUDE_OIL_SPOT_WEEKLY',22,'USD per barrel')]:
  decoy=clean[(clean.geo_id=='US')&(clean.date<='2026-09-07')].tail(260).copy()
  decoy['variable']=name;decoy['variable_name']=name+' (SYNTHETIC)';decoy['value']*=factor;decoy['unit']=unit
  history=pd.concat([history,decoy],ignore_index=True)
  attrs.append(dict(variable=name,variable_name=name+' (SYNTHETIC)',unit=unit,frequency='Weekly',description='SYNTHETIC decoy'))
 history.sort_values(['variable','geo_id','date']).to_csv(DATA/'SYNTHETIC_eia_timeseries.csv',index=False)
 pd.DataFrame(attrs).to_csv(DATA/'SYNTHETIC_eia_attributes.csv',index=False)
 pd.DataFrame([dict(geo_id='US',geo_name='United States (SYNTHETIC)',level='National')]).to_csv(DATA/'SYNTHETIC_geography_index.csv',index=False)
 for d,name,mult in [('2026-09-14','SYNTHETIC_batch_2026-09-14.csv',1),('2026-09-21','SYNTHETIC_batch_2026-09-21_corrupt.csv',100)]:
  batch=clean[clean.date==d].copy();batch['value']*=mult;batch.to_csv(DATA/name,index=False)
 truth={'label':'SYNTHETIC','seed':42,'as_of_date':'2026-09-23','regions':REGIONS,'regimes':windows,'plateaus':[{'start':'2003-01-06','end':'2003-12-29'},{'start':'2010-01-04','end':'2010-12-27'},{'start':'2018-01-01','end':'2018-12-31'}],'errors':{'T1':['PADD4','2011-03-07','2011-03-14','2011-03-21'],'T2':['US','2019-06-03','2019-06-10'],'T3':['PADD3','2016-02-08',100],'T4':['PADD2','2014-11-10'],'T5':shifts,'T6':[x['variable'] for x in attrs[1:]],'T7':'Only US indexed; 10 additional raw geographies','T8':'2026-09-07 latest initial date; 16 days old'}}
 (DATA/'SYNTHETIC_planted_truth.json').write_text(json.dumps(truth,indent=2)+'\n')
 (DATA/'README.md').write_text('# SYNTHETIC data\n\nGenerated with seed 42 by `python local/generate_sample_data.py`. These are fictional index prices, not EIA data. Truth locations and planted effects are in SYNTHETIC_planted_truth.json. Full history has 14,947 rows including decoys. Never use these numbers to price a real contract.\n')
 print('Generated SYNTHETIC listing:',len(history),'rows')
if __name__=='__main__':generate()
