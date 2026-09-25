# Phase 3: Build the two clocks [SYNTHETIC DRY RUN]

Business question: What is paid and collected each week?

What was built: see docs/phase_file_map.md and the evidence files below.

How it ran: `python local/run_pipeline.py all`, followed by verify_outputs.py, test_pipeline.py and test_app.py. Full pipeline runs took about 40–43 seconds here, excluding dependency installation.

Sample results:

| geo_id | week_date | scenario_id | index_price | reset_price | carrier_fsc | shipper_fsc | spread |
| --- | --- | --- | --- | --- | --- | --- | --- |
| US | 2021-12-06 | S1 | 2.661000 | 2.661000 | 0.235167 | 0.235167 | 0.000000 |
| US | 2021-12-06 | S3 | 2.661000 | 2.661000 | 0.235167 | 0.235167 | 0.000000 |
| US | 2021-12-06 | S5 | 2.661000 | 2.587000 | 0.235167 | 0.222833 | -0.012333 |
| US | 2021-12-13 | S1 | 2.727000 | 2.727000 | 0.246167 | 0.246167 | 0.000000 |
| US | 2021-12-13 | S3 | 2.727000 | 2.661000 | 0.246167 | 0.235167 | -0.011000 |
| US | 2021-12-13 | S5 | 2.727000 | 2.587000 | 0.246167 | 0.222833 | -0.023333 |
| US | 2021-12-20 | S1 | 2.801000 | 2.801000 | 0.258500 | 0.258500 | 0.000000 |
| US | 2021-12-20 | S3 | 2.801000 | 2.661000 | 0.258500 | 0.235167 | -0.023333 |
| US | 2021-12-20 | S5 | 2.801000 | 2.587000 | 0.258500 | 0.222833 | -0.035667 |
| US | 2021-12-27 | S1 | 2.871000 | 2.871000 | 0.270167 | 0.270167 | 0.000000 |
| US | 2021-12-27 | S3 | 2.871000 | 2.661000 | 0.270167 | 0.235167 | -0.035000 |
| US | 2021-12-27 | S5 | 2.871000 | 2.587000 | 0.270167 | 0.222833 | -0.047333 |
| US | 2022-01-03 | S1 | 2.940000 | 2.940000 | 0.281667 | 0.281667 | 0.000000 |
| US | 2022-01-03 | S3 | 2.940000 | 2.940000 | 0.281667 | 0.281667 | 0.000000 |
| US | 2022-01-03 | S5 | 2.940000 | 2.940000 | 0.281667 | 0.281667 | 0.000000 |
| US | 2022-01-10 | S1 | 3.010000 | 3.010000 | 0.293333 | 0.293333 | 0.000000 |
| US | 2022-01-10 | S3 | 3.010000 | 2.940000 | 0.293333 | 0.281667 | -0.011667 |
| US | 2022-01-10 | S5 | 3.010000 | 2.940000 | 0.293333 | 0.281667 | -0.011667 |

Validation: 85,044 scenario rows. The planted PADD4 March 2011 monthly reset moves to March 28; other reset periods have no substitutions.

Surprises and fixes: Date joins enforce exact calendar lags and four-week comparisons; missing observations are not filled.

Learnings:

- Technical: FIRST_VALUE holds reset prices.
- Data: A missing reset moves to the next available week.
- Analytical: Shared lags preserve the control.
- Business: Different schedules create exposure.

Explain-back:

1. What does this phase establish? 85,044 scenario rows. The planted PADD4 March 2011 monthly reset moves to March 28; other reset periods have no substitutions.
2. What does it not establish? Actual company margins or untested Snowflake behavior.
3. Why does it matter? Different schedules create exposure.

Exit criteria: local synthetic evidence is complete with documented scope gaps in docs/acceptance_status.md. Deployment and real-source criteria remain unverified. Publication is confirmed by GitHub PR links, not simulated pushes.

Evidence files:

- `outputs/phase_3/SYNTHETIC_clock_excerpt.csv`
- `outputs/phase_3/SYNTHETIC_missing_week_log.csv`
- `outputs/phase_3/SYNTHETIC_period_exclusion_log.csv`
- `outputs/phase_3/SYNTHETIC_reset_substitutions.csv`
