-- Manual unchanged-source verification, recorded September 27, 2026.
-- Run AFTER a successful first manual load and source review.
-- The CALL runs the loader and writes a load-log entry.
-- Expected results below apply only when the source is unchanged.
-- Do not run simultaneous manual CALLs or resume the scheduled task.
USE ROLE FUEL_ANALYST;
USE WAREHOUSE FUEL_WH;
USE DATABASE FUEL_TIMING;

-- 1. Select and execute this statement alone.
CALL FUEL_TIMING.RAW.LOAD_DIESEL_WEEKLY();
-- Expected response: PASSED: no changes

-- 2. Select and execute this query separately; export its result.
SELECT STATUS, INSERTED, UPDATED, QUARANTINED, RAW_ROWS, FRESHNESS, REASON
FROM FUEL_TIMING.RAW.LOAD_LOG
ORDER BY LOADED_AT DESC
LIMIT 1;
-- September 27 checkpoint: PASSED,0,0,0,16275,STALE,NO_CHANGE
-- Latest-log selection assumes no concurrent loader execution.
-- If the source changed, investigate the delta instead of forcing this expectation.

-- 3. Select and execute this query separately; export even if empty.
SELECT GEO_ID, WEEK_DATE, COUNT(*) AS ROW_COUNT
FROM FUEL_TIMING.RAW.DIESEL_WEEKLY
GROUP BY GEO_ID, WEEK_DATE
HAVING COUNT(*) > 1;
-- Expected: zero rows. A header-only CSV records the empty exception result.
