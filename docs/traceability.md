# Traceability and test status

PASS below refers to the local synthetic run. UNVERIFIED means no Snowflake execution. A named check is not a claim that the production gate passed.

| Rule | Named check / evidence | Status |
|---|---|---|
| BR-01 | test_floor_and_missing_reset; six-week SQL example | PASS |
| BR-02 | test_index_lag_uses_calendar_week | PASS |
| BR-03 | INV-01 and clock excerpt | PASS |
| BR-04 | RESET_CONSTANT | PASS |
| BR-05 | SYNTHETIC_clause_effect.csv | SQL evidence |
| BR-06 | INV-01 and INV-04 | PASS |
| BR-07 | Shared 30_spread.sql; SQL memo evidence | SQL evidence |
| BR-08 | test_four_week_regime_does_not_bridge_gap; E2 confusion matrix | PASS |
| BR-09 | season CASE; EIA survey reference | Implemented |
| BR-10 | E1 recovery and complete 52-week calendar windows | PASS |
| BR-11 | Same geo_id join in both clocks; common-week region comparison | Implemented |
| BR-12 | T1, initial missing-clean-week CSV, calendar-lag tests | PASS |
| BR-13 | PADD4 monthly substitution; test_floor_and_missing_reset | PASS; test_whole_missing_month_is_logged verifies exclusions |
| BR-14 | T5, 44 normalization log rows | PASS |
| BR-15 | T2/T3/T4; conflicting duplicate test | PASS |
| BR-16 | T8 and event 2 load-log freshness | PASS |
| BR-17 | schema/unit/empty tests; BLOCKED_UNCHANGED; approved D-01 | PASS locally; procedure UNVERIFIED |
| BR-18 | complete_period and common-window comparison CSV | Implemented |

| Requirement | Named evidence or gate | Status |
|---|---|---|
| FR-01 | Six synthetic answers; docs/real_source_gate.md | Synthetic PASS; real NOT RUN |
| FR-02 | Four-event replay and landing tests | Local PASS; Snowflake UNVERIFIED |
| FR-03 | INV-01/02/04, RESET_CONSTANT | PASS |
| FR-04 | Summary, regime, regions, worst stretches, percentiles, INV-05 | PASS locally |
| FR-05 | test_app.py; four static page views and walkthrough | Local PASS; Snowflake NOT RUN |
| FR-06 | Vision, memo, method post, claim-lineage CSV | Complete; share with caveats |
| FR-07 | Two local teardown invocations; sql/99_teardown.sql | Local PASS; Snowflake NOT RUN |
| FR-08 | Simulated narration | Optional AI skipped |
| FR-09 | DAT overlay | Optional skipped |
| FR-10 | SYNTHETIC_sensitivity.csv | Analysis complete; optional interactive page deferred |
| NFR-01 | Warehouse/monitor DDL and resource monitor docs | UNVERIFIED |
| NFR-02 | Pinned requirements, fixed seed/date, repeatability check | Local PASS |
| NFR-03 | No-op landing and teardown tests | Local PASS; deployment UNVERIFIED |
| NFR-04 | CONFIG.SOURCE_CONFIG | Real names unconfigured |
| NFR-05 | FUEL_ANALYST model ownership | DDL only; infrastructure remains admin-owned |
| NFR-06 | Assumptions, sources, banners and filenames | Reviewed |
| NFR-07 | SQL model and analysis result lineage | Implemented |
