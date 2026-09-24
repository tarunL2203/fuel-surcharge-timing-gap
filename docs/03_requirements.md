# Requirements

### 5.1 Must have (P0)

- **FR-01 Profile the source** and complete the six-item exit checklist.
  *Accepted when* all six answers are recorded and every STOP rule has been evaluated.
- **FR-02 Land a validated weekly copy**: idempotent MERGE, row quarantine, batch blocking, and a load log with load timestamps.
  *Accepted when* the four load events in Section 7.3 produce the expected counts.
- **FR-03 Compute both clocks** for every week, region, and scenario.
  *Accepted when* INV-01, INV-02, and INV-04 pass.
- **FR-04 Compute spread and summaries**: by scenario, by regime and season, and by region; worst 4-week stretches; share of squeeze weeks; P10, P50, P90.
  *Accepted when* INV-05 passes and every summary number traces to weekly rows.
- **FR-05 Streamlit in Snowflake app**: filters (region, reset frequency, clause, date range), spread-over-time chart, regime and season table, worst stretches, dollars per 1,000 loads, freshness banner, data quality page, assumptions page.
  *Accepted when* every chart title states the insight and the date range, and the banner follows BR-16.
- **FR-06 Business outputs**: a one-page memo (decision first), a LinkedIn method post (the method, no results), and the vision doc.
  *Accepted when* every number in them traces to a results table.
- **FR-07 Teardown script.**
  *Accepted when* it runs twice in a row without errors and leaves no project objects.

### 5.2 Nice to have (P1)

- **FR-08 Narration with `AI_COMPLETE`**, using only numbers from a results table and showing those numbers next to the text.
- **FR-09 DAT Trendlines overlay**, only if its schema check passes.
- **FR-10 Sensitivity page** in the app for A-01, A-02, A-05, A-07, and A-08.

### 5.3 Design for, do not build (P2)

- Owner-operator lens on the same clean diesel table.
- Index-basis mismatch (national versus regional index) as a third contract lever.

### 5.4 Non-functional requirements

- **NFR-01 Cost**: XS warehouse, `AUTO_SUSPEND = 60`, a resource monitor with notify and suspend triggers, and the weekly task running on the same warehouse so the monitor covers it. A resource monitor does not cap AI usage, so if Cortex Code is used, set its credit limits separately.
- **NFR-02 Reproducibility**: numbered run order, fixed seed, fixed AS_OF_DATE, pinned Python dependencies.
- **NFR-03 Idempotency**: every script is safe to rerun.
- **NFR-04 Single source of truth**: real listing object names appear in exactly one place (`CONFIG.SOURCE_CONFIG`).
- **NFR-05 Least privilege**: one functional role owns all project objects; the listing is granted through `IMPORTED PRIVILEGES`.
- **NFR-06 Transparency**: assumptions register, sources file, synthetic labels.
- **NFR-07 Explainability**: all numeric logic lives in SQL rules, never in an LLM.

### 5.5 Success metrics

- **Dry run**: 8 of 8 planted errors caught; INV-01 to INV-05 pass; planted effects recovered within tolerance; a stranger can reproduce every output from the README.
- **Real run**: Phase 1 gate passed; the weekly task runs four consecutive weeks with no manual fixes; one reviewer outside the project can state the memo's decision in one sentence.

### 5.6 Open questions

- **Blocking (owner, before real Phase 2)**: the six Phase 1 checklist answers.
- **Non-blocking (owner)**: enable AI features on the trial, or skip FR-08?
- **Non-blocking (research)**: which public, formula-style surcharge schedule to cite for A-01 and A-02.
- **Non-blocking (data)**: DAT Trendlines schema and fields.
