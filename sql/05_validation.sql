-- UNVERIFIED: confirm in Snowflake. Zero rows means PASS. Run INV-01 first.
-- INV-01
SELECT * FROM model.dt_margin_spread WHERE is_control AND spread <> 0;

-- INV-02
SELECT 'row_count' AS failure WHERE (SELECT COUNT(*) FROM model.dt_margin_spread) <> (SELECT COUNT(*) * 6 FROM raw.diesel_weekly);

-- INV-04
SELECT * FROM model.dt_margin_spread WHERE NOT seasonal_clause AND ((index_price > reset_price AND spread > 0) OR (index_price < reset_price AND spread < 0));

-- INV-05
SELECT s.geo_id, s.scenario_id FROM model.dt_scenario_summary AS s JOIN (SELECT geo_id, scenario_id, SUM(spread) AS total FROM model.dt_margin_spread WHERE complete_period GROUP BY ALL) AS r USING (geo_id, scenario_id) WHERE ABS(s.sum_spread - r.total) > 1e-10;

-- FSC_NONNEGATIVE
SELECT * FROM model.dt_margin_spread WHERE carrier_fsc < 0;

-- RESET_CONSTANT
SELECT geo_id, scenario_id, reset_period FROM model.dt_margin_spread WHERE NOT seasonal_clause GROUP BY ALL HAVING MIN(shipper_fsc) <> MAX(shipper_fsc);