-- SYNTHETIC locally; identical SELECT translated to Snowflake deployment syntax.
WITH w AS (
 SELECT r.*, p.regime_threshold, p.as_of_date,
   prior.price AS prior_4week_price,
   AVG(r.price) OVER (PARTITION BY r.geo_id ORDER BY r.week_date ROWS BETWEEN 25 PRECEDING AND 26 FOLLOWING) AS centered_avg,
   COUNT(*) OVER (PARTITION BY r.geo_id ORDER BY r.week_date ROWS BETWEEN 25 PRECEDING AND 26 FOLLOWING) AS window_count,
   MIN(r.week_date) OVER (PARTITION BY r.geo_id ORDER BY r.week_date ROWS BETWEEN 25 PRECEDING AND 26 FOLLOWING) AS window_start,
   MAX(r.week_date) OVER (PARTITION BY r.geo_id ORDER BY r.week_date ROWS BETWEEN 25 PRECEDING AND 26 FOLLOWING) AS window_end
 FROM raw.diesel_weekly r CROSS JOIN config.parameters p
 LEFT JOIN raw.diesel_weekly prior ON r.geo_id=prior.geo_id AND prior.week_date=r.week_date-INTERVAL '28 days'
)
SELECT *, price/NULLIF(prior_4week_price,0)-1 AS change_4week,
 CASE WHEN prior_4week_price IS NULL THEN 'UNCLASSIFIED'
 WHEN price/prior_4week_price-1 >= regime_threshold THEN 'RISING'
 WHEN price/prior_4week_price-1 <= -regime_threshold THEN 'FALLING' ELSE 'PLATEAU' END AS regime,
 EXTRACT(MONTH FROM week_date) AS month_number,
 CASE WHEN EXTRACT(MONTH FROM week_date) IN (10,11,12,1,2,3) THEN 'HEATING' ELSE 'NON_HEATING' END AS season,
 CASE WHEN window_count=52 AND DATEDIFF('day',window_start,window_end)=357 THEN price/centered_avg END AS seasonal_ratio
FROM w
