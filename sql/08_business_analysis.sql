-- UNVERIFIED: confirm in Snowflake. Business analysis queries from local/analyze.py.
USE ROLE FUEL_ANALYST; USE DATABASE FUEL_TIMING;

-- outputs/phase_4/SYNTHETIC_summary.csv
SELECT
  *
FROM model.dt_scenario_summary
ORDER BY
  geo_id,
  scenario_id;

-- outputs/phase_4/SYNTHETIC_regime_season.csv
SELECT
  geo_id,
  scenario_id,
  regime,
  season,
  COUNT(*) AS weeks,
  AVG(spread) AS mean_spread,
  AVG(dollars_per_1000_loads) AS mean_dollars_per_1000_loads
FROM model.dt_margin_spread
WHERE
  complete_period
GROUP BY ALL
ORDER BY
  ALL;

-- outputs/phase_4/SYNTHETIC_worst_stretches.csv
WITH r AS (
  SELECT
    geo_id,
    scenario_id,
    week_date,
    complete_period,
    COUNT(*) OVER (
      PARTITION BY geo_id, scenario_id
      ORDER BY week_date
      ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS n,
    MIN(week_date) OVER (
      PARTITION BY geo_id, scenario_id
      ORDER BY week_date
      ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS start_date,
    AVG(spread) OVER (
      PARTITION BY geo_id, scenario_id
      ORDER BY week_date
      ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS mean_spread,
    AVG(dollars_per_1000_loads) OVER (
      PARTITION BY geo_id, scenario_id
      ORDER BY week_date
      ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS mean_dollars_per_1000_loads
  FROM model.dt_margin_spread
), ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY geo_id, scenario_id ORDER BY mean_spread, week_date) AS rank
  FROM r
  WHERE
    n = 4 AND DATEDIFF(DAY, start_date, week_date) = 21
)
SELECT
  *
FROM ranked
WHERE
  rank <= 5
ORDER BY
  geo_id,
  scenario_id,
  rank;

-- outputs/phase_4/SYNTHETIC_clause_effect.csv
SELECT
  a.geo_id,
  a.scenario_id,
  b.scenario_id AS paired_scenario,
  a.season,
  COUNT(*) AS weeks,
  AVG(a.spread) AS without_clause,
  AVG(b.spread) AS with_clause,
  AVG(b.spread - a.spread) AS clause_uplift,
  AVG(GREATEST(0, -a.spread)) AS squeeze_without,
  AVG(GREATEST(0, -b.spread)) AS squeeze_with
FROM model.dt_margin_spread AS a
JOIN model.dt_margin_spread AS b
  ON a.geo_id = b.geo_id
  AND a.week_date = b.week_date
  AND (
    (
      a.scenario_id = 'S3' AND b.scenario_id = 'S4'
    )
    OR (
      a.scenario_id = 'S5' AND b.scenario_id = 'S6'
    )
  )
WHERE
  a.complete_period AND b.complete_period
GROUP BY ALL
ORDER BY
  ALL;

-- outputs/phase_4/SYNTHETIC_regions_common_window.csv
WITH common AS (
  SELECT
    week_date
  FROM raw.diesel_weekly
  GROUP BY
    week_date
  HAVING
    COUNT(DISTINCT geo_id) = 11
)
SELECT
  geo_id,
  scenario_id,
  COUNT(*) AS weeks,
  AVG(spread) AS mean_spread
FROM model.dt_margin_spread
JOIN common
  USING (week_date)
WHERE
  complete_period
GROUP BY ALL
ORDER BY
  ALL;

-- outputs/phase_5/SYNTHETIC_memo_evidence.csv
SELECT
  *
FROM model.dt_scenario_summary
WHERE
  geo_id = 'US'
ORDER BY
  scenario_id;
