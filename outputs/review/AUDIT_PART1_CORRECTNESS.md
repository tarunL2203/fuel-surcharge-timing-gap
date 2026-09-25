# SYNTHETIC audit, Part 1: correctness

Verdict: **PASS WITH FIXES**. No demonstrated wrong core answer or failed invariant. This is a review by the same assistant that built the project, using newly written checks and a fresh environment. It is not independent third-party assurance.

Baseline: phase-6 commit `69a7c9b69451ded75aa4bf442b208370eaf83f29`, reviewed 2026-09-24. See [independent evidence](INDEPENDENT_CHECKS.json), [rerun log](RERUN_LOG.txt), [reproduction instructions](REPRODUCE.md) and [history scan](HISTORY_CHECKS.json).

## Phase status

| Phase | Status | Report exists | Template coverage | Merge commit |
|---|---|---|---|---|
| 0 | PARTIAL | outputs/phase_0/REPORT.md | Missing validation table | None, PR #2 open |
| 1 | PARTIAL | outputs/phase_1/REPORT.md | Missing validation table | None, PR #3 open |
| 2 | PARTIAL | outputs/phase_2/REPORT.md | Missing validation table | None, PR #4 open |
| 3 | PARTIAL | outputs/phase_3/REPORT.md | Missing validation table | None, PR #5 open |
| 4 | PARTIAL | outputs/phase_4/REPORT.md | Missing validation table | None, PR #6 open |
| 5 | PARTIAL | outputs/phase_5/REPORT.md | Missing validation table | None, PR #7 open |
| 6 | PARTIAL | outputs/phase_6/REPORT.md | Missing validation table | None, PR #8 open |

All seven have business question, built/run descriptions, sample results or evidence, surprises, four learning categories, three questions with answers, and exit criteria. The built section is a generic pointer, rather than a file-by-file account. Local implementation is present for every phase; PARTIAL refers to closure and reporting, not absent implementation.

## Known answers recomputed

All 30 checks in INDEPENDENT_CHECKS.json pass. Source contains 14,947 rows; diesel spans 1,288 normalized Mondays and 11 expected regions, with 14,165 distinct present pairs. The 14,168 possible pairs have exactly the three specified PADD4 removals. T2 duplicates, T3 out-of-range row, T4 null and all four T5 shifted weeks match the canonical locations. T5 has 44 rows. Three US-only decoys each have 260 rows and the prescribed units. The index contains only US. The initial tail is 16 days old. Diesel names carry `(SYNTHETIC)`.

Truth JSON records T1-T8 and regional offsets/amplitudes, regime windows and plateaus. Effect properties are recorded without explicit E1-E4 headings; E4 is the model sign-control contract. Generator code applies the T3 multiplier of 100; the observed location is the sole initial value above the upper price bound. The supplied original brief and committed BUILD_BRIEF are byte-identical. The approved no-change PASS clarification in DECISIONS D-01 agrees with this audit's canonical answers.

| Event | Accepted rows | Inserted / updated | Status | Freshness |
|---|---:|---|---|---|
| 1 | 14,163 | 14,163 / 0 | PASSED_WITH_QUARANTINE | 16 days, STALE |
| 2 | 14,174 | 11 / 0 | PASSED | 9 days, FRESH |
| 3 | 14,174 | 0 / 0 | PASSED | 9 days, FRESH |
| 4 | 14,174 | 0 / 0 | BLOCKED, 11 invalid of 11 new | 9 days, FRESH |

Initial quarantine has one NULL_VALUE and one OUT_OF_RANGE. There are 44 normalization records, five initial clean missing pairs and one monthly substitution, PADD4 March 2011 to March 28, shared by S3/S4. The final missing-week view also flags the rejected September 21 tail; those are not additional initial-data traps.

All 85,044 scenario rows are present. INV-01 is first in local/run_pipeline.py:84 and in the emitted validation CSV. Independent control, join-count, rerun-delta, sign and reconciliation checks pass. Maximum reconciliation rounding difference is 1.94e-13, below the existing 1e-10 threshold. E4 has zero sign violations, or 100% compliance.

| Effect | Recomputed result | Required | Outcome |
|---|---|---|---|
| E1 | Maximum error 0.29374 percentage points | At most 1.0 point | PASS |
| E2 rising | 73 / 78 = 93.59% | At least 70% | PASS |
| E2 falling | 70 / 78 = 89.74% | At least 70% | PASS |
| E3 | Maximum error 0.05497 percentage points | At most 1.0 point | PASS |
| E4 | 100% sign compliance | 100% | PASS |

E2 confusion matrix, columns FALLING / PLATEAU / RISING: falling truth = 70 / 4 / 4; rising truth = 0 / 5 / 73. These agree with the committed recovery tables.

## Reproducibility and report numbers

Pinned dependencies installed. All noninteractive README commands passed, including ten targeted tests and app tests. The pipeline took 8.92 seconds on this environment. Earlier reported 40-43 seconds are historical timings, not a performance requirement. Total installation/walkthrough elapsed time and a literal authenticated clone are CANNOT VERIFY; see REPRODUCE.md for the verified-snapshot substitution.

All generated sample, analytical CSV, SQL and PNG hashes matched the baseline except the two differences below. Every phase report's sample-result table was reproduced unchanged; phase 6 differs only in its evidence list. There are no numeric result mismatches. App checks pass, but interactive usability and live Snowflake behavior are not certified.

- **F-01, MAJOR, SAFE:** All phase REPORT.md files use a prose `Validation:` paragraph, not the required expected/actual/pass table (for example phase_0/REPORT.md:20). Add tables from existing evidence without changing results, thresholds or tests. The generator would overwrite hand-edited reports on rerun, so retain a durable documentation process.
- **F-02, MAJOR, OWNER DECISION:** sql/05_validation.sql has INV-01, 02, 04 and 05 but omits INV-03. local/run_pipeline.py:98 explicitly filters it out when generating Snowflake SQL. The local idempotency test passes; this is a missing deployment validation step, not a failed local invariant. Add an explicit Snowflake rerun validation procedure under a separately authorized implementation task. This review's rules prohibit changing tests or SQL in either stage.
- **F-03, MINOR, SAFE:** Rerunning local/write_reports.py adds `SYNTHETIC_verification_log.txt` to phase_6/REPORT.md's evidence list. The committed report is stale relative to the committed files. The exact diff is a single added link, not a changed result.
- **F-04, NIT, NO CHANGE NEEDED:** The load-log CSV hash changes because loaded_at is actual run time. All other columns match. README explicitly discloses this variability. Record the difference rather than claiming every output hash is identical.

## Test integrity and Snowflake static review

GitHub tree comparison found only README changed after its initial introduction. Thus the committed brief, defaults, checks, thresholds and expected values have one version each. No unexplained committed tolerance changes were found. This does not reconstruct uncommitted development attempts. Native git log was unavailable; complete reachable commit/tree/blob evidence was used instead.

Required role, warehouse, monitor, database, four schemas, landing tables/procedure/task and four dynamic tables exist. Seeds include the four business configuration tables plus run configuration. Setup has XSMALL, 60-second auto-suspend and WEEK_START=1. The task uses FUEL_WH and is explicitly suspended. Three intermediate tables use DOWNSTREAM and the final summary uses a one-day target. Source adapter names are confined to CONFIG.SOURCE_CONFIG. No external network integration or external function is introduced. Deployment files carry UNVERIFIED markers. Teardown suspends the task before dropping the database, warehouse, monitor and role.

All nine top-level SQL files parsed with sqlglot's Snowflake dialect. Setup, landing and teardown contain respectively 5, 2 and 4 generic Command nodes: these are unsupported parser constructs, not successful semantic validation. PARSER_LOG.txt records warnings. Shared SELECT regeneration was byte-identical and the Snowflake round-trip model test passed. local/dialect_notes.md documents engine differences. Procedure execution, privileges, task session settings, transactions, rerun safety in Snowflake and teardown after database deletion remain CANNOT VERIFY without running there. No Snowflake code was executed.

## Honesty, sources and numeric lineage

The README disclosure is present verbatim. Charts and result filenames carry SYNTHETIC. Memo and simulated narration explicitly deny real-company inference. The method post contains no outcome numbers. The schedule is TODO(source), ILLUSTRATIVE. No invented source was found. On 2026-09-24 all four primary URLs in docs/sources.md opened successfully: Snowflake dynamic-table syntax, target lag, resource monitors and EIA survey definitions. Their documented scope supports the cited claims; none validates prices, company margins, contract acceptance or listing access.

At least ten numerical claims trace to rerun evidence:

| Prose location / claim | Recomputed evidence |
|---|---|
| README: 14,947 listing rows | Source CSV length; variables CSV sum |
| README: 14,163 initially accepted | load_log event 1 |
| README: 14,174 after update | load_log event 2 |
| README: 85,044 scenario rows | model.dt_margin_spread count |
| README: 8/8 traps | trap_detection.csv, eight passing rows |
| README: INV-01 through INV-05 | validation.csv, first five rows plus independent checks |
| README: 10 targeted tests | RERUN_LOG.txt, ten named successes |
| README: four app pages | local/test_app.py and successful rerun |
| Memo: weekly control zero | same_window_contracts.csv S1; independently zero |
| Memo: 44.2% quarterly squeeze | S5; recomputed 0.4420970266 |
| Memo: 20.7% with clause | S6; recomputed 0.2065727700 |
| Memo: $67.55 per 1,000 loads | S5; recomputed $67.55346896 |
| Narration: 44.2%, 20.7%, zero | Same S5/S6/S1 rows |

Method post has no outcome numbers to trace. Test/page counts properly trace to execution evidence rather than an unrelated result table.
