SELECT geo_id, scenario_id, reset_frequency, seasonal_clause, COUNT(*) AS weeks,
 SUM(spread) AS sum_spread, AVG(spread) AS mean_spread,
 AVG(dollars_per_1000_loads) AS mean_dollars_per_1000_loads,
 AVG(CASE WHEN spread<0 THEN 1.0 ELSE 0.0 END) AS squeeze_share,
 QUANTILE_CONT(spread,0.10) AS p10, QUANTILE_CONT(spread,0.50) AS p50,
 QUANTILE_CONT(spread,0.90) AS p90,
 MIN(week_date) AS start_date, MAX(week_date) AS end_date
FROM model.dt_margin_spread WHERE complete_period
GROUP BY geo_id,scenario_id,reset_frequency,seasonal_clause
