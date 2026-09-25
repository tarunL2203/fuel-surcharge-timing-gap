-- UNVERIFIED: confirm in Snowflake. Run after setup, before landing.
USE ROLE FUEL_ANALYST;
USE DATABASE FUEL_TIMING;
CREATE TABLE IF NOT EXISTS CONFIG.SURCHARGE_SCHEDULE(schedule_id VARCHAR,base_price FLOAT,mpg FLOAT,source_note VARCHAR,status VARCHAR);
INSERT INTO CONFIG.SURCHARGE_SCHEDULE SELECT 'DEFAULT',1.25,6.0,'TODO(source): illustrative formula parameters','ILLUSTRATIVE' WHERE NOT EXISTS(SELECT 1 FROM CONFIG.SURCHARGE_SCHEDULE);
CREATE TABLE IF NOT EXISTS CONFIG.CONTRACT_SCENARIOS(scenario_id VARCHAR,reset_frequency VARCHAR,seasonal_clause BOOLEAN,is_control BOOLEAN);
MERGE INTO CONFIG.CONTRACT_SCENARIOS t USING (SELECT column1 scenario_id,column2 reset_frequency,column3 seasonal_clause,column4 is_control FROM VALUES ('S1','WEEKLY',FALSE,TRUE),('S2','WEEKLY',TRUE,FALSE),('S3','MONTHLY',FALSE,FALSE),('S4','MONTHLY',TRUE,FALSE),('S5','QUARTERLY',FALSE,FALSE),('S6','QUARTERLY',TRUE,FALSE)) s
 ON t.scenario_id=s.scenario_id WHEN NOT MATCHED THEN INSERT VALUES(s.scenario_id,s.reset_frequency,s.seasonal_clause,s.is_control);
CREATE TABLE IF NOT EXISTS CONFIG.MODEL_PARAMETERS(param_name VARCHAR,param_value FLOAT,unit VARCHAR,assumption_id VARCHAR);
MERGE INTO CONFIG.MODEL_PARAMETERS t USING (SELECT column1 param_name,column2 param_value,column3 unit,column4 assumption_id FROM VALUES ('INDEX_LAG_WEEKS',0,'weeks','A-03'),('STEP_UP_PER_MILE',0.02,'USD/mile','A-05'),('REGIME_THRESHOLD',0.03,'fraction','A-07'),('LOAD_MILES',500,'miles','A-08'),('FRESHNESS_MAX_DAYS',10,'days','A-09'),('MIN_PRICE',1,'USD/gallon','A-10'),('MAX_PRICE',8,'USD/gallon','A-10'),('BATCH_MAX_BAD_PCT',0.05,'fraction','A-11')) s
 ON t.param_name=s.param_name WHEN NOT MATCHED THEN INSERT VALUES(s.param_name,s.param_value,s.unit,s.assumption_id);
CREATE TABLE IF NOT EXISTS CONFIG.RUN_CONFIG(as_of_date DATE);
INSERT INTO CONFIG.RUN_CONFIG SELECT DATE '2026-09-23' WHERE NOT EXISTS(SELECT 1 FROM CONFIG.RUN_CONFIG);
CREATE OR REPLACE VIEW CONFIG.PARAMETERS AS SELECT s.base_price,s.mpg,r.as_of_date,
 MAX(IFF(param_name='INDEX_LAG_WEEKS',param_value,NULL))::INTEGER index_lag_weeks,
 MAX(IFF(param_name='STEP_UP_PER_MILE',param_value,NULL)) step_up_per_mile,
 MAX(IFF(param_name='REGIME_THRESHOLD',param_value,NULL)) regime_threshold,
 MAX(IFF(param_name='LOAD_MILES',param_value,NULL))::INTEGER load_miles,
 MAX(IFF(param_name='FRESHNESS_MAX_DAYS',param_value,NULL))::INTEGER freshness_max_days,
 MAX(IFF(param_name='MIN_PRICE',param_value,NULL)) min_price,
 MAX(IFF(param_name='MAX_PRICE',param_value,NULL)) max_price,
 MAX(IFF(param_name='BATCH_MAX_BAD_PCT',param_value,NULL)) batch_max_bad_pct
 FROM CONFIG.SURCHARGE_SCHEDULE s CROSS JOIN CONFIG.RUN_CONFIG r CROSS JOIN CONFIG.MODEL_PARAMETERS p WHERE s.schedule_id='DEFAULT' GROUP BY s.base_price,s.mpg,r.as_of_date;
-- The sole storage location for real listing object names. Fill only after profiling.
CREATE TABLE IF NOT EXISTS CONFIG.SOURCE_CONFIG(source_object VARCHAR,diesel_variable VARCHAR,profile_gate_passed BOOLEAN,review_note VARCHAR);
INSERT INTO CONFIG.SOURCE_CONFIG SELECT NULL,NULL,FALSE,'Real source not profiled' WHERE NOT EXISTS(SELECT 1 FROM CONFIG.SOURCE_CONFIG);
-- source_object must identify a reviewed read-only adapter view exposing:
-- GEO_ID, VARIABLE, VARIABLE_NAME, DATE, VALUE, UNIT. Do not alter shared data.
