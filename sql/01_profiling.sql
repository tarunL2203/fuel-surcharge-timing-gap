-- UNVERIFIED: confirm in Snowflake. Prerequisites: 00_setup then 03_seeds.
USE ROLE FUEL_ANALYST; USE DATABASE FUEL_TIMING; USE WAREHOUSE FUEL_WH;
ALTER SESSION SET WEEK_START=1;
-- First inspect the installed listing in the UI and build a read-only adapter.
-- Put its fully qualified identifier only in CONFIG.SOURCE_CONFIG.source_object.
SET SOURCE_OBJECT=(SELECT source_object FROM CONFIG.SOURCE_CONFIG);
-- P01: existence/schema. If configured object is absent or columns differ, STOP.
SELECT * FROM IDENTIFIER($SOURCE_OBJECT) LIMIT 10;
-- P02/P03: choose RETAIL ON-HIGHWAY DIESEL, never gasoline/spot/crude.
SELECT variable,variable_name,unit,COUNT(*) row_count,MIN(date) first_date,MAX(date) latest_date
FROM IDENTIFIER($SOURCE_OBJECT) GROUP BY ALL ORDER BY variable;
SET TARGET_VARIABLE=(SELECT diesel_variable FROM CONFIG.SOURCE_CONFIG);
-- P04: region scope must inspect actual raw geography values, not only index metadata.
SELECT geo_id,COUNT(*) row_count FROM IDENTIFIER($SOURCE_OBJECT)
WHERE variable=$TARGET_VARIABLE GROUP BY geo_id;
-- Look for separate region variable names as well; no regions means national-only scope.
SELECT DISTINCT variable,variable_name FROM IDENTIFIER($SOURCE_OBJECT)
WHERE variable_name ILIKE '%diesel%';
-- P05 freshness: provisional 10-day threshold; replace after actual lag is measured.
SELECT MAX(date) latest_date,DATEDIFF('day',MAX(date),DATE '2026-09-23') days_old
FROM IDENTIFIER($SOURCE_OBJECT) WHERE variable=$TARGET_VARIABLE;
-- P06 weekly frequency, holiday shifts, gaps and duplicates.
SELECT DAYNAME(date) weekday,COUNT(*) row_count FROM IDENTIFIER($SOURCE_OBJECT)
WHERE variable=$TARGET_VARIABLE GROUP BY ALL;
WITH d AS (SELECT geo_id,date,LAG(date) OVER(PARTITION BY geo_id ORDER BY date) prior_date
 FROM IDENTIFIER($SOURCE_OBJECT) WHERE variable=$TARGET_VARIABLE)
SELECT *,DATEDIFF('day',prior_date,date) gap_days FROM d WHERE DATEDIFF('day',prior_date,date)<>7;
SELECT geo_id,DATE_TRUNC('week',date) week_date,COUNT(*) row_count,COUNT(DISTINCT value) distinct_values
FROM IDENTIFIER($SOURCE_OBJECT) WHERE variable=$TARGET_VARIABLE GROUP BY ALL HAVING COUNT(*)>1;
SELECT * FROM IDENTIFIER($SOURCE_OBJECT) WHERE variable=$TARGET_VARIABLE
AND (value IS NULL OR value<1 OR value>8 OR unit<>'USD per gallon');
-- STOP if no retail diesel or no weekly series. Investigate units before proceeding.
-- Record all six answers in docs/real_source_gate.md. Never set the gate automatically.
-- No permission, warehouse availability, or listing cost is certified by these queries.
