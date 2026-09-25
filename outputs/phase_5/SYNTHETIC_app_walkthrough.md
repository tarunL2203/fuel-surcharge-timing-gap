# SYNTHETIC app walkthrough

Run `python -m streamlit run app/streamlit_app.py` after building the database.

1. Overview: select US/monthly/clause off. Inspect spread, regime/season and worst contiguous four-week windows. Metrics exclude the unfinished reset period; the detail retains it with a complete_period flag.
2. Scenario explorer: compare reset/clause settings. The full-history comparison table states its date scope. Use the common-window CSV for comparisons across schedules.
3. Data quality: inspect the four attempts and quarantine. The blocked week does not replace the accepted September 14 observations.
4. Assumptions: inspect illustrative values and limitations. The fixed replay date is not a live freshness claim.

Static supporting charts are in outputs/phase_4. They are analysis plots, not claimed browser screenshots. AppTest checks behavior; a visual production review in Snowflake is still required.
