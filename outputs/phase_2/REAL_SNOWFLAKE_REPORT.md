# Phase 2: real Snowflake historical loading checkpoint

Executed by the owner on September 27, 2026 (America/New_York). Reviewed from supplied CSV exports and chat confirmations. This is real-source loading evidence, separate from the [synthetic phase report](REPORT.md).

## Result and scope

The initial load was reported successful. The supplied unchanged-rerun log records PASSED, zero inserts, zero updates and 16,275 RAW rows. The supplied duplicate query export contains only its header, indicating zero returned duplicate groups. The historical loading and unchanged-rerun checkpoint passes on this evidence.

This is not full Phase 2 failure-path certification: new arrivals, corrections/reversions, rejected batches and transaction rollback still require separate Snowflake tests. The original synthetic four-event test remains separate. The evidence supports the recorded no-change run; it is not a before/after comparison of every stored value or independent live execution by the reviewer.

| Check | Expected | Observed | Evidence |
|---|---|---|---|
| First load into empty RAW | PASSED; 16,275 inserted; 0 updated/quarantined | Owner confirmed the expected result | Chat confirmation; first-load CSV not supplied |
| Unchanged rerun | PASSED; 0 inserted; 0 updated | PASSED; 0 inserted; 0 updated | [Rerun log](REAL_SNOWFLAKE_rerun_log.csv) |
| Retained RAW count | 16,275 | 16,275 | Rerun log |
| Quarantined on rerun | 0 | 0 | Rerun log |
| Rerun reason | NO_CHANGE | NO_CHANGE | Rerun log |
| Duplicate geography/week groups | 0 | Header-only result; 0 groups | [Duplicate check](REAL_SNOWFLAKE_duplicate_check.csv) |
| Freshness | STALE while data ends June 22 | STALE | Rerun log |

## Configuration and execution record

The owner ran sql/03_seeds.sql, then the configuration updates supplied in the guided run. The historical run used AS_OF_DATE 2026-09-27, MIN_PRICE 0.50, MAX_PRICE 8 and FRESHNESS_MAX_DAYS 10. The $0.50 lower bound is an illustrative project guardrail, not an EIA rule; the observed minimum of $0.916 was incorrectly excluded by the original $1 default. The canonical variable is DIESEL_RETAIL_ONHWY_WEEKLY, read through the Phase 1 adapter configured in CONFIG.SOURCE_CONFIG.

The owner reported 16,275 source rows and zero invalid prices under those bounds. The source was then enabled for manual historical loading. The source approval flag does not establish freshness or approve automatic scheduling.

Running sql/02_landing.sql twice created/replaced the procedure and suspended task; it did not itself run a load. The owner subsequently executed CALL FUEL_TIMING.RAW.LOAD_DIESEL_WEEKLY(), confirmed the first-load result, and executed the unchanged rerun. No task RESUME was instructed or reported; the task is expected to remain suspended, but a task-state export is not included.

[Reproduction SQL](../../sql/02b_verify_unchanged_rerun.sql) preserves the two evidence queries and the manual rerun command. It is an operator check, not an automatic assertion suite. First-load setup requires the reviewed adapter and configuration above; the repository's default seeds alone do not reproduce this real run. Exact adapter creation SQL is still a separate evidence gap.

## Provenance

The CSV contents are retained unchanged under descriptive filenames. They contain operational summary data and an empty exception result, not source-price extracts or account identifiers.

| Original attachment | Repository file | SHA-256 of supplied bytes |
|---|---|---|
| Phase2- Loading and val_2026-09-27-2302.csv | REAL_SNOWFLAKE_rerun_log.csv | 2a054113ecf2ad0df56def8d00335fbbf8fb74194255b9653744a37d85824882 |
| Phase2- Loading and val_2026-09-27-2303.csv | REAL_SNOWFLAKE_duplicate_check.csv | 3e0ab5b54168486a07b54e60aa4158f65970fb8ce3e8adca13c5e3fc4c355373 |

The digests identify the supplied exports; they do not authenticate Snowflake execution. These exports omit query IDs, load IDs and execution timestamps. Their association with the queries is based on the guided execution and owner submission. No missing identifiers or first-load results were fabricated.

## Remaining work

- Preserve first-load log details and query/run identifiers if stronger audit evidence is needed.
- Run controlled Snowflake correction, new-row and rejected-batch tests before full loader certification.
- Keep the existing F-02 issue open for its missing integrated Snowflake validation coverage; this report adds the manual unchanged-rerun evidence.
- Resolve source freshness and provider cadence before automatic operation.
- Proceed to model creation and validation in Phase 3; published analytical outputs remain synthetic.
