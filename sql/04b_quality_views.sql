-- UNVERIFIED: confirm in Snowflake. Calendar spine differs from DuckDB generate_series.
USE ROLE FUEL_ANALYST; USE DATABASE FUEL_TIMING;
CREATE OR REPLACE VIEW MODEL.V_MISSING_WEEKS AS
WITH spine AS (SELECT DATEADD('week',ROW_NUMBER() OVER(ORDER BY SEQ4())-1,(SELECT MIN(week_date) FROM RAW.DIESEL_WEEKLY))::DATE week_date FROM TABLE(GENERATOR(ROWCOUNT=>10000))),
expected AS (SELECT g.geo_id,s.week_date FROM (SELECT DISTINCT geo_id FROM RAW.DIESEL_WEEKLY) g CROSS JOIN spine s CROSS JOIN CONFIG.PARAMETERS p WHERE s.week_date<=p.as_of_date)
SELECT e.* FROM expected e LEFT JOIN RAW.DIESEL_WEEKLY r USING(geo_id,week_date) WHERE r.geo_id IS NULL;
CREATE OR REPLACE VIEW MODEL.V_PERIOD_EXCLUSIONS AS
WITH all_weeks AS (SELECT geo_id,week_date,TRUE missing FROM MODEL.V_MISSING_WEEKS UNION ALL SELECT geo_id,week_date,FALSE FROM RAW.DIESEL_WEEKLY),
periods AS (SELECT geo_id,'MONTHLY' reset_frequency,DATE_TRUNC('month',week_date) period,missing FROM all_weeks UNION ALL SELECT geo_id,'QUARTERLY',DATE_TRUNC('quarter',week_date),missing FROM all_weeks)
SELECT geo_id,reset_frequency,period,COUNT(*) expected_weeks FROM periods GROUP BY geo_id,reset_frequency,period HAVING BOOLAND_AGG(missing);
