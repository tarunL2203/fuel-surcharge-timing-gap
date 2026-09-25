WITH eligible AS (
 SELECT d.*, i.price AS index_price, p.base_price, p.mpg, p.step_up_per_mile, p.load_miles,
 p.index_lag_weeks, s.*,
 CASE s.reset_frequency WHEN 'WEEKLY' THEN d.week_date WHEN 'MONTHLY' THEN DATE_TRUNC('month',d.week_date) ELSE DATE_TRUNC('quarter',d.week_date) END AS reset_period
 FROM model.dt_diesel_weekly d CROSS JOIN config.parameters p CROSS JOIN config.contract_scenarios s
 JOIN raw.diesel_weekly i ON d.geo_id=i.geo_id AND i.week_date=d.week_date-p.index_lag_weeks*INTERVAL '7 days'
), reset AS (
 SELECT *, FIRST_VALUE(index_price) OVER (PARTITION BY geo_id,scenario_id,reset_period ORDER BY week_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS reset_price,
 MIN(week_date) OVER (PARTITION BY geo_id,scenario_id,reset_period) AS reset_week
 FROM eligible
)
SELECT *, GREATEST(0.0,(index_price-base_price)/mpg) AS carrier_fsc,
 GREATEST(0.0,(reset_price-base_price)/mpg) + CASE WHEN seasonal_clause AND season='HEATING' THEN step_up_per_mile ELSE 0 END AS shipper_fsc,
 CASE reset_frequency WHEN 'WEEKLY' THEN TRUE
 WHEN 'MONTHLY' THEN DATE_TRUNC('month',week_date)<DATE_TRUNC('month',as_of_date)
 ELSE DATE_TRUNC('quarter',week_date)<DATE_TRUNC('quarter',as_of_date) END AS complete_period
FROM reset
