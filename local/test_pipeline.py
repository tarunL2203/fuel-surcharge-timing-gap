"""Targeted edge cases plus dialect round-trip parity. Run after the dry run."""
import unittest
from pathlib import Path
import duckdb,pandas as pd,sqlglot
from run_pipeline import setup,land,model,DB,ROOT
from generate_sample_data import VARIABLE
from render_snowflake import OBJECTS

def frame(values):
 return pd.DataFrame([dict(geo_id='US',variable=VARIABLE,variable_name='SYNTHETIC edge case',date=d,value=v,unit='USD per gallon') for d,v in values])

class LandingTests(unittest.TestCase):
 def setUp(self):self.c=duckdb.connect();setup(self.c)
 def tearDown(self):self.c.close()
 def test_malformed_cast_blocks_without_mutation(self):
  land(self.c,frame([('not-a-date','bad-price')]))
  self.assertEqual(self.c.sql('SELECT status FROM raw.load_log').fetchone()[0],'BLOCKED')
 def test_whole_missing_month_is_logged(self):
  land(self.c,frame([('2026-01-05',2.5),('2026-03-02',3)]));model(self.c)
  self.assertEqual(self.c.sql("SELECT COUNT(*) FROM model.v_period_exclusions WHERE reset_frequency='MONTHLY' AND period=DATE '2026-02-01'").fetchone()[0],1)
 def test_valid_correction_and_reversion(self):
  land(self.c,frame([('2026-01-05',2.5)]));land(self.c,frame([('2026-01-05',3.0)]));land(self.c,frame([('2026-01-05',2.5)]))
  self.assertEqual(float(self.c.sql('SELECT price FROM raw.diesel_weekly').fetchone()[0]),2.5)
  self.assertEqual(self.c.sql('SELECT updated FROM raw.load_log ORDER BY load_id').fetchall(),[(0,),(1,),(1,)])
 def test_conflicting_duplicates_both_quarantined(self):
  self.c.execute('UPDATE config.parameters SET batch_max_bad_pct=1')
  land(self.c,frame([('2026-01-05',2.5),('2026-01-05',3.0)]))
  self.assertEqual(self.c.sql('SELECT COUNT(*) FROM raw.quarantine').fetchone()[0],2)
  self.assertEqual(self.c.sql('SELECT COUNT(*) FROM raw.diesel_weekly').fetchone()[0],0)
 def test_invalid_correction_preserves_history(self):
  land(self.c,frame([('2026-01-05',2.5)]));before=self.c.sql('SELECT * FROM raw.diesel_weekly').fetchall()
  land(self.c,frame([('2026-01-05',250)]))
  self.assertEqual(before,self.c.sql('SELECT * FROM raw.diesel_weekly').fetchall())
 def test_empty_schema_and_units_block(self):
  land(self.c,pd.DataFrame({'wrong':[]}))
  df=frame([('2026-01-05',2.5)]);df['unit']='USD per barrel';land(self.c,df)
  land(self.c,frame([]).reindex(columns=['geo_id','variable','variable_name','date','value','unit']))
  self.assertEqual(self.c.sql("SELECT COUNT(*) FROM raw.load_log WHERE status='BLOCKED'").fetchone()[0],3)
 def test_index_lag_uses_calendar_week(self):
  land(self.c,frame([('2026-01-05',2.5),('2026-01-19',3),('2026-01-26',3.1)]))
  self.c.execute('UPDATE config.parameters SET index_lag_weeks=1');model(self.c)
  self.assertEqual(self.c.sql('SELECT COUNT(*) FROM model.dt_margin_spread').fetchone()[0],6)
  self.assertEqual(self.c.sql('SELECT COUNT(*) FROM model.dt_margin_spread WHERE is_control AND spread<>0').fetchone()[0],0)
 def test_floor_and_missing_reset(self):
  land(self.c,frame([('2026-01-12',1.1),('2026-01-19',1.4)]));model(self.c)
  self.assertEqual(self.c.sql("SELECT MIN(shipper_fsc) FROM model.dt_margin_spread WHERE scenario_id='S5'").fetchone()[0],0)
  self.assertEqual(str(self.c.sql("SELECT MIN(reset_week) FROM model.dt_margin_spread WHERE scenario_id='S5'").fetchone()[0]),'2026-01-12')
 def test_four_week_regime_does_not_bridge_gap(self):
  land(self.c,frame([('2026-01-05',2.5),('2026-01-19',2.6),('2026-01-26',2.7),('2026-02-02',2.8),('2026-02-09',3.0)]));model(self.c)
  self.assertEqual(self.c.sql("SELECT regime FROM model.dt_diesel_weekly WHERE week_date=DATE '2026-02-09'").fetchone()[0],'UNCLASSIFIED')

class ModelParityTests(unittest.TestCase):
 def test_snowflake_roundtrip_same_results(self):
  c=duckdb.connect(str(DB),read_only=True)
  try:
   for file,name in OBJECTS:
    sql=(ROOT/'sql/selects'/file).read_text()
    sf=sqlglot.transpile(sql,read='duckdb',write='snowflake')[0]
    back=sqlglot.transpile(sf,read='snowflake',write='duckdb')[0]
    diff=c.sql(f'(SELECT * FROM ({sql}) EXCEPT ALL SELECT * FROM ({back})) UNION ALL (SELECT * FROM ({back}) EXCEPT ALL SELECT * FROM ({sql}))').fetchall()
    self.assertEqual(diff,[],name)
  finally:c.close()

if __name__=='__main__':unittest.main(verbosity=2)
