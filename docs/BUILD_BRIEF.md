# The Broker's Two Clocks: End-to-End Build Brief

**Project**: Fuel surcharge timing gap for freight brokers and 3PLs
**Version**: 1.0 (September 2026)
**Owner**: Sai Tarun Reddy
**Status**: Design complete. Phase 1 on real data pending.

---

## How to use this brief (read first)

- **Paste the whole file into an LLM** as the first message, then add: `Execute this brief end to end in autonomous mode. Stop only at STOP conditions. Save a phase report after every phase.`
- **Best environment**: an agent that can create files, run Python, and use git on your machine (for example, Claude Code). A chat-only LLM can do everything except push to GitHub; it hands back a zip and the exact git commands.
- **Checkpoint mode**: say `checkpoint mode` instead of `autonomous mode` if you want the LLM to pause for your review after each phase.
- **A person can follow it too**: every phase lists its business question, what to build, what to run, the expected results, and exit criteria.
- **Nothing here connects to Snowflake.** The dry run executes on a local database using synthetic data. The Snowflake SQL is written for you to run later in your trial account.

---

## 0. Role and mission (for the executor)

You are a senior analytics engineer who also thinks like a pricing analyst. Build the complete sample project below, from business rules to a published repository, using a synthetic dataset of about 15,000 rows. For every phase:

1. Write the Snowflake SQL that will run in production (the **deployment track**).
2. Execute the same logic locally on the synthetic data (the **local twin**) to produce real sample outputs.
3. Save a phase report with sample results, validation results, and learnings.

Your work will be judged on three things:

- **Technical rigor**: idempotent, validated, reproducible, cost-safe.
- **Analytical rigor**: controls, known-answer tests, sensitivity analysis, honest limits.
- **Business acumen**: every number translated into a pricing decision.

---

## 1. Vision (mentor version)

*Use this section verbatim as `docs/00_vision.md`.*

**The pitch**

Freight brokers sit between shippers and carriers. They pay carriers a fuel surcharge that resets every week with the government's diesel price index, but they bill shippers under contract terms that reset monthly, quarterly, or not at all. When diesel moves, the two clocks drift apart and the difference lands on the broker's margin, even though the broker never buys a gallon of fuel. This project measures that gap on real EIA diesel data inside Snowflake: how large it gets under different contract terms, when it is worst (rising prices, the winter heating season), and whether a contract clause closes it. The deliverable is a Streamlit app where a pricing team can change contract terms and see the margin impact, plus a one-page memo that leads with the decision.

**Why it is credible**

- **Real, free data**: EIA weekly retail diesel prices from the Snowflake Marketplace, with data limits stated upfront.
- **A built-in correctness proof**: when both clocks reset weekly, the model must show zero spread in every week. Any spread in the other scenarios comes from the mechanism, not a bug.
- **Method tested before the real run**: a synthetic dry run plants eight known data errors (the checks must catch all of them) and known effects (the analysis must recover them).
- **Every assumption is labeled, registered, and stress-tested.**

**What it does not claim**

- No real company's margins or surcharge collections (that data is private).
- No forecasting.
- Synthetic results show the method works. Only the real run produces findings.

**Why Snowflake, when the data is small**

The real diesel slice is expected to be under about 20,000 rows, so the case is not volume. The case is that the data arrives live through the Marketplace with no pipeline to maintain, every weekly load is validated before it touches the model, the rebuild is declarative, and the app sits next to the data, so a pricing analyst can test contract terms without exporting anything.

**Questions a mentor will ask**

- *Is the surcharge schedule real?* The formula structure is public and cited. The parameter values are labeled assumptions with sensitivity ranges.
- *What if the listing has no regional data?* The core mechanism runs on the national index. Regional analysis is a scope option decided in Phase 1.
- *How do you know the model is right?* The zero-spread control, known-answer tests on synthetic data, and reconciliation checks on every run.
- *What would an owner-operator version change?* Same data, different exposure: an owner-operator buys the fuel, so the question becomes whether the surcharge received covers the fuel burned. That is the planned second lens.

---

## 2. Ground rules (non-negotiable)

1. **Label synthetic work.** The sample data and every result derived from it carry `SYNTHETIC` in the file name, table name, chart title, or first line. Never present sample numbers as findings about real prices or real companies.
2. **No invented facts or sources.** If a claim needs a source you cannot verify, write `TODO(source)`. Never fabricate citations, statistics, company names, or quotes.
3. **Snowflake SQL is the deployment target.** Write valid Snowflake SQL for every object. Mark anything you could not execute with `-- UNVERIFIED: confirm in Snowflake`.
4. **One logic, two tracks.** The local twin runs the same SELECT logic as the Snowflake objects. Record every dialect difference in `local/dialect_notes.md`.
5. **Parameters, not magic numbers.** Every tunable value lives in a parameter or seed table and in `docs/assumptions_register.md` (ID, value, rationale, sensitivity range, status).
6. **Failed checks are findings.** Never edit data or expected values to make a check pass. Report the failure, the cause, and the fix.
7. **Deterministic runs.** Use random seed `42` and `AS_OF_DATE = 2026-09-23` everywhere, so every run produces identical numbers.
8. **Trial-safe.** Snowflake trial accounts have no external network access. Cortex AI features are optional and require AI features to be enabled on the trial (by adding a credit card). Nothing in the core build depends on them.
9. **Numbers come from SQL.** No LLM ever calculates a metric. An LLM may only narrate numbers that already exist in a results table.
10. **Stop conditions.** Halt and report if (a) a Phase 1 STOP rule triggers on real data, (b) an invariant fails and you cannot explain why, or (c) two business rules conflict.
11. **Writing style.** Plain language for business readers, decision implications first, every acronym defined on first use, no em dashes.
12. **Honest learnings.** Learnings logs record what actually happened in this run, including real errors and fixes. Never invent a lesson.

---

## 3. Business context

### 3.1 How a broker/3PL operates day to day

| Phase | What happens | Fuel surcharge role | In scope? |
|---|---|---|---|
| Quoting | Broker prices a load for a shipper | Surcharge folded into an all-in rate or listed separately | No: negotiation data not available |
| Contracting | Terms agreed for committed freight | **Both clocks are set here**: index, reset frequency, lag | Yes |
| Execution | Load moves; broker pays the carrier | Carrier clock applies, usually weekly | Yes |
| Settlement | Broker invoices the shipper | Shipper clock applies; **margin is realized** | Yes |
| Renewal | Terms revisited | Chance to fix a mismatch | No: behavioral data not available |

### 3.2 The two clocks

- **Carrier clock (fast)**: what the broker pays carriers. Resets every week from the EIA weekly retail on-highway diesel price.
- **Shipper clock (slow)**: what the broker bills shippers. Resets on the contract's schedule (weekly, monthly, or quarterly), then holds.
- **Margin spread**: shipper fuel surcharge (FSC) minus carrier FSC, in dollars per mile. Positive is a cushion; negative is a squeeze.

### 3.3 Naive assumption vs. what we test

- **Naive**: fuel surcharges pass straight through, so brokers are fuel-neutral.
- **Tested**: pass-through only holds when both clocks tick together. The project measures how far margin drifts when they do not, in which price regimes, which seasons, and which regions.

### 3.4 Goals (measurable)

- **G1**: Quantify the weekly margin spread for each contract scenario, with the control scenario proven at exactly zero.
- **G2**: Identify which price regime and season combinations produce the largest squeeze, reported in dollars per 1,000 loads.
- **G3**: Measure how much a seasonal step-up clause reduces heating-season squeeze, with sensitivity bounds.
- **G4**: Deliver an app a non-technical pricing analyst can use without help, plus a one-page memo.
- **G5 (dry run only)**: Catch 100% of planted data errors and recover the planted effects within stated tolerances.

### 3.5 Non-goals (with rationale)

- **Real company financials or surcharge collections**: private data, not on the Marketplace.
- **Lane-level freight rates**: paid data. Free DAT Trendlines is optional, pending a schema check.
- **Quoting and renewal behavior**: behavioral, not in any available dataset.
- **Carrier fuel economics and broker overhead**: not the broker's surcharge exposure.
- **Hedging and futures**: no relevant free data.
- **Other modes (rail, ocean, air)**: different surcharge mechanics.
- **Consumer or retail demand**: not needed for the surcharge mechanism.
- **Forecasting**: the project is diagnostic; forecasts would imply precision the model does not have.
- **Owner-operator lens**: planned as a second project on the same clean diesel table.

### 3.6 Users and stories

- As a **broker pricing analyst**, I want to change reset frequency and the seasonal clause and see the margin impact, so that I can recommend contract terms.
- As a **contracting manager**, I want the squeeze expressed in dollars per 1,000 loads, so that I can weigh it against the cost of renegotiating.
- As a **data reviewer**, I want every load validated and every assumption registered, so that I can trust the numbers.
- As a **mentor or hiring manager**, I want to see the method tested on known answers, so that I can judge the rigor.
- **Edge stories**: a week is missing; a contract's reset week is missing; the source goes stale; a corrupted batch arrives.

---

## 4. Business rules (testable)

### 4.1 Definitions

- `week_date`: the Monday the index price is reported for.
- `region`: one of 11 geographies (US plus 10 regions), or US only if Phase 1 finds national data only.
- `price`: EIA weekly retail on-highway diesel price, dollars per gallon.
- `FSC(price)`: fuel surcharge in dollars per mile, from the surcharge schedule.

### 4.2 Rules

- **BR-01 Schedule**: `FSC(price) = GREATEST(0, (price - BASE_PRICE) / MPG)`. Both clocks use the same schedule, so timing and the seasonal clause are the only differences between them.
- **BR-02 Index lag**: both clocks read `price(week_date - INDEX_LAG_WEEKS)`. The lag is a shared publication convention, never a difference between the clocks.
- **BR-03 Carrier clock**: resets every week.
- **BR-04 Shipper clock**: resets on the first available week of each reset period (the week, the calendar month, or the calendar quarter) and holds that FSC until the next reset.
- **BR-05 Seasonal step-up clause**: when ON, add `STEP_UP_PER_MILE` to the shipper FSC in heating-season weeks.
- **BR-06 Spread**: `SPREAD = FSC_shipper - FSC_carrier` (dollars per mile). Positive = cushion, negative = squeeze.
- **BR-07 Business translation**: `dollars per 1,000 loads = SPREAD x LOAD_MILES x 1,000`.
- **BR-08 Price regime**: from the trailing 4-week percent change in price: `RISING` if at least +REGIME_THRESHOLD, `FALLING` if at most -REGIME_THRESHOLD, otherwise `PLATEAU`. The first four weeks of each region are `UNCLASSIFIED`.
- **BR-09 Season**: `HEATING` for October to March, `NON_HEATING` for April to September. Anchor: EIA's heating oil price survey runs October through March.
- **BR-10 Seasonal index**: price divided by its centered 52-week moving average, averaged by calendar month. Descriptive only. Weeks without a full 52-week window are excluded.
- **BR-11 Region is a dimension, never a lever**: both clocks always read the same region's price.
- **BR-12 Missing weeks**: flagged, excluded, and counted. Never forward-filled or interpolated. No carrier price means no spread row for that week.
- **BR-13 Missing reset week**: the shipper clock resets on the next available week in the same period, and the substitution is logged. If a whole period is missing, its weeks are excluded and logged.
- **BR-14 Date normalization**: dates that are not Mondays move to the Monday of the same week, and each move is logged. In Snowflake, set `WEEK_START = 1` (Monday) so week truncation is explicit.
- **BR-15 Row quarantine**: null or out-of-range prices go to a quarantine table with a reason code. Exact duplicates keep one row; conflicting duplicates are both quarantined.
- **BR-16 Freshness**: if `AS_OF_DATE - latest week_date > FRESHNESS_MAX_DAYS`, the data is flagged stale. It stays usable for history, and the app shows a banner.
- **BR-17 Batch blocking**: a load is rejected entirely if its delta (new or changed rows versus RAW) has zero rows, a schema mismatch, a unit other than dollars per gallon, or more than `BATCH_MAX_BAD_PCT` bad rows.
- **BR-18 Partial periods**: the current, unfinished month or quarter is excluded from period-level comparisons and labeled in charts.

### 4.3 Invariants (tested every run)

- **INV-01 Zero-spread control** (the PERFECT_WORLD check): WEEKLY resets with the clause OFF must produce a spread of exactly 0 in every row.
- **INV-02 Row count**: spread rows = valid carrier weeks x scenarios.
- **INV-03 Idempotency**: rerunning a load inserts 0 rows and changes 0 values.
- **INV-04 Sign test**: with the clause OFF, within a reset period, if price has risen since the reset week then spread is at most 0; if it has fallen, spread is at least 0. This follows from the rules, so it must hold on any data.
- **INV-05 Reconciliation**: summary totals equal the sum of the weekly rows they summarize. Never average pre-computed averages.

### 4.4 Default parameters

All values are **ILLUSTRATIVE** until replaced by a cited schedule or by Phase 1 profiling.

| ID | Parameter | Default | Sensitivity range | Rationale |
|---|---|---|---|---|
| A-01 | BASE_PRICE | 1.25 $/gal | 1.00 to 1.50 | Placeholder; replace with the cited schedule's value |
| A-02 | MPG | 6.0 | 5.5 to 7.0 | Fleet fuel economy assumed inside the schedule |
| A-03 | INDEX_LAG_WEEKS | 0 | 0 to 1 | Price published for week w applies to week w |
| A-04 | RESET_FREQUENCIES | WEEKLY, MONTHLY, QUARTERLY | fixed | Scenario design |
| A-05 | STEP_UP_PER_MILE | 0.02 $/mile | 0.01 to 0.04 | Clause size; tested, not recommended |
| A-06 | HEATING_MONTHS | Oct to Mar | fixed | EIA heating oil survey window |
| A-07 | REGIME_THRESHOLD | 3% over 4 weeks | 2% to 5% | Separates trend from weekly noise |
| A-08 | LOAD_MILES | 500 | 250 to 1,000 | Business translation only |
| A-09 | FRESHNESS_MAX_DAYS | 10 | set from Phase 1 item 5 | Weekly data plus listing lag |
| A-10 | PRICE_RANGE | 1.00 to 8.00 $/gal | set from Phase 1 Step 8 | Catches unit errors |
| A-11 | BATCH_MAX_BAD_PCT | 5% | 1% to 10% | Separates row issues from a broken batch |

### 4.5 Contract scenarios (seed table `CONFIG.CONTRACT_SCENARIOS`)

| ID | Shipper reset | Seasonal clause | Role |
|---|---|---|---|
| S1 | WEEKLY | OFF | Control (INV-01) |
| S2 | WEEKLY | ON | Clause effect alone |
| S3 | MONTHLY | OFF | Medium clock |
| S4 | MONTHLY | ON | Medium clock with clause |
| S5 | QUARTERLY | OFF | Slowest clock tested |
| S6 | QUARTERLY | ON | Slowest clock with clause |

---

## 5. Requirements

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

---

## 6. Data

### 6.1 Real source (Snowflake track)

- **Listing**: Snowflake Public Data (Free), on the Snowflake Marketplace.
- **Expected shape** (confirm in Phase 1): a `*_timeseries` table (date, geo_id, variable, variable_name, value), a matching `*_attributes` table (unit, frequency), and a shared `geography_index` (geo_id, geo_name, level).
- **Placeholders until Phase 1**: `<<LISTING_DB>>`, `<<EIA_TIMESERIES>>`, `<<EIA_ATTRIBUTES>>`, `<<DIESEL_VARIABLE_NAME>>`.
- **Expected volume**: EIA publishes weekly retail diesel for the US and about ten regions, and the national series (EIA series ID `EMD_EPD2D_PTE_NUS_DPG`) runs weekly from March 1994. The diesel slice should therefore be under about 20,000 rows, and the six-scenario grid about six times that.
- **Never commit extracts of the real listing to GitHub.** Commit code, not data, unless the listing's terms explicitly allow redistribution.

### 6.2 Sample dataset (SYNTHETIC)

Generated by `local/generate_sample_data.py` into `data/sample/`:

- `SYNTHETIC_eia_timeseries.csv`: geo_id, variable, variable_name, date, value, unit
- `SYNTHETIC_eia_attributes.csv`: variable, variable_name, unit, frequency, description
- `SYNTHETIC_geography_index.csv`: geo_id, geo_name, level
- `SYNTHETIC_batch_2026-09-14.csv`: one valid new week (11 rows)
- `SYNTHETIC_batch_2026-09-21_corrupt.csv`: one corrupted new week (11 rows, every value x 100)
- `SYNTHETIC_planted_truth.json`: every planted error and effect, with exact locations and sizes
- `README.md`: what is synthetic, why, and how it was generated

**Diesel series**

- variable `DIESEL_RETAIL_ONHWY_WEEKLY`, variable_name `Weekly retail on-highway diesel price (SYNTHETIC)`, unit `USD per gallon`, frequency `Weekly`.
- 11 geographies, mirroring the regional set EIA publishes: `US`, `PADD1` East Coast, `PADD1A` New England, `PADD1B` Central Atlantic, `PADD1C` Lower Atlantic, `PADD2` Midwest, `PADD3` Gulf Coast, `PADD4` Rocky Mountain, `PADD5` West Coast, `PADD5XCA` West Coast less California, `CA` California.
- Mondays from 2002-01-07 through 2026-09-07: **1,288 weeks x 11 geographies = 14,168 expected rows**.
- Prices rounded to 3 decimals.

**Price generator**

- **National path**: piecewise regimes plus small weekly noise, bounded to roughly 1.30 to 6.00 dollars per gallon. Include at least 3 run-ups (+40% or more within 26 weeks), 3 declines (-30% or more within 26 weeks), and 3 plateaus (26 or more weeks with 4-week moves under 2%). Log every regime window in the truth file.
- **Seasonality**: multiplicative, peaking in mid-January. Amplitude by region: PADD1, PADD1A, PADD1B 6%; PADD1C 4%; US, PADD2, PADD4 3%; PADD3, PADD5, PADD5XCA, CA 2%.
- **Regional level offsets** versus US (multiplicative, stable over time): CA +15%, PADD5 +10%, PADD5XCA +6%, PADD1A +5%, PADD1B +4%, PADD1 +3%, PADD4 +2%, PADD1C +1%, PADD2 0%, PADD3 -4%. These are synthetic. They echo EIA's description of higher West Coast and California prices, but they are not EIA's actual figures.

**Decoy variables** (US only, last 260 weeks, 780 rows)

- `GASOLINE_RETAIL_REGULAR_WEEKLY`: Weekly retail regular gasoline price (SYNTHETIC), USD per gallon
- `DIESEL_ULSD_SPOT_WEEKLY`: Weekly wholesale spot ultra-low sulfur diesel price (SYNTHETIC), USD per gallon
- `CRUDE_OIL_SPOT_WEEKLY`: Weekly crude oil spot price (SYNTHETIC), USD per barrel

### 6.3 Planted data errors (the checks must catch all eight)

| ID | Trap | Exact plant | Caught by | Expected handling |
|---|---|---|---|---|
| T1 | Missing weeks | PADD4: 2011-03-07, 2011-03-14, 2011-03-21 removed | Checklist item 6; completeness check | 3 flagged; one 28-day gap; BR-13 substitution for the March 2011 monthly reset |
| T2 | Duplicates | US: 2019-06-03 and 2019-06-10 duplicated exactly | Uniqueness check | 2 extra rows; one copy of each kept |
| T3 | Unit error | PADD3: 2016-02-08 value x 100 | Checklist item 3; range check | 1 row quarantined (`OUT_OF_RANGE`) |
| T4 | Null price | PADD2: 2014-11-10 | Null check | 1 row quarantined (`NULL_VALUE`) |
| T5 | Holiday date shift | All 11 geographies, Memorial Day weeks 2015-05-25, 2016-05-30, 2020-05-25, 2023-05-29, dated Tuesday | Checklist item 6; weekday check | 44 rows normalized to Monday and logged; paired 8-day and 6-day gaps in profiling |
| T6 | Decoy variables | 3 non-target variables | Checklist items 2 and 3 | Retail diesel chosen; wholesale and crude rejected |
| T7 | Unindexed regions | Only `US` appears in `geography_index` | Checklist item 4 (second Step 5 query) | 10 regions found through raw geo_id values |
| T8 | Stale tail | Series ends 2026-09-07; AS_OF_DATE is 2026-09-23 | Checklist item 5; freshness check | 16 days old, flagged STALE |

### 6.4 Planted effects (the analysis must recover them)

| ID | Effect | Recovery test | Tolerance |
|---|---|---|---|
| E1 | Seasonal amplitude by region | January seasonal index minus 1, compared with planted amplitude | Within 1.0 percentage point |
| E2 | Regime windows | Share of planted run-up weeks labeled RISING; share of planted decline weeks labeled FALLING | At least 70% each; report the confusion matrix |
| E3 | Regional level offsets | Mean price ratio, region versus US, over full years | Within 1.0 percentage point |
| E4 | Mechanical sign (logical, not planted) | INV-04 | 100% |

If a recovery misses its tolerance, report it and explain why (ground rule 6). On synthetic data, a result that confirms a planted effect is expected; label it as planted, never as a finding.

### 6.5 Seed and parameter tables

- `CONFIG.SURCHARGE_SCHEDULE`: schedule_id, base_price, mpg, source_note, status (`ILLUSTRATIVE` or `CITED`)
- `CONFIG.CONTRACT_SCENARIOS`: scenario_id, reset_frequency, seasonal_clause, is_control
- `CONFIG.MODEL_PARAMETERS`: param_name, param_value, unit, assumption_id
- `CONFIG.SOURCE_CONFIG`: the only place real listing names live (NFR-04)

Find and cite a publicly documented, formula-style fuel surcharge schedule in `docs/sources.md`. If you cannot verify one, keep `status = ILLUSTRATIVE` and add `TODO(source)`.

### 6.6 Sanity-check numbers for the dry run

| Check | Expected |
|---|---|
| Rows in `SYNTHETIC_eia_timeseries.csv` | **14,947** (14,168 - 3 missing + 2 duplicates + 780 decoys) |
| Diesel week and region pairs expected | 14,168 |
| Distinct diesel pairs present | 14,165 |
| Rows quarantined | 2 (1 null, 1 out of range) |
| Dates normalized to Monday | 44 |
| Valid prices after the first load | 14,163 |
| Missing pairs in the clean table | 5 (3 removed, 2 quarantined) |
| BR-13 reset substitutions | 1 (PADD4, March 2011, MONTHLY frequency; affects S3 and S4) |
| Days since latest week at first load | 16 (STALE) |

---

## 7. Architecture

### 7.1 Snowflake track (deployment)

- **Setup**: role `FUEL_ANALYST`; warehouse `FUEL_WH` (XSMALL, `AUTO_SUSPEND = 60`, `AUTO_RESUME = TRUE`, `INITIALLY_SUSPENDED = TRUE`); resource monitor `FUEL_RM`; database `FUEL_TIMING` with schemas `CONFIG`, `RAW`, `MODEL`, `APP`.
- **Landing**: a stored procedure `RAW.LOAD_DIESEL_WEEKLY()` in Snowflake Scripting reads `CONFIG.SOURCE_CONFIG`, computes the delta, validates it (BR-14 to BR-17), quarantines bad rows, MERGEs into `RAW.DIESEL_WEEKLY` with `loaded_at` and `load_id`, and writes `RAW.LOAD_LOG`. A task `RAW.TASK_LOAD_DIESEL_WEEKLY` runs it weekly on `FUEL_WH`, on a CRON schedule set after Phase 1 item 5. Tasks are created suspended; resume only after one successful manual `CALL`.
- **Why a copy instead of reading the share in place**: consumers cannot enable change tracking on shared objects, and a dynamic table reading a share reports success even when the provider's data is stale. The landed copy fixes both and carries its own load timestamps.
- **Model**: Dynamic Tables `MODEL.DT_DIESEL_WEEKLY` (clean prices, 4-week change, regime, month, season, seasonal ratio), then `MODEL.DT_SURCHARGE_CLOCKS` (both clocks per scenario), then `MODEL.DT_MARGIN_SPREAD`, then `MODEL.DT_SCENARIO_SUMMARY`. Intermediates use `TARGET_LAG = DOWNSTREAM`; the final table uses a daily target lag.
- **Validation**: `sql/05_validation.sql`. Every assertion returns zero rows when it passes and names the failing rows when it does not.
- **App**: Streamlit in Snowflake in schema `APP`, reading `MODEL` tables only.
- **Teardown**: `sql/99_teardown.sql` suspends the task first, then drops objects in dependency order.

### 7.2 Local twin (no Snowflake connection)

Engine: DuckDB (preferred) or Python `sqlite3` (fallback). A translator such as sqlglot may help convert Snowflake SQL, but every translation is checked by hand and logged in `local/dialect_notes.md`.

| Snowflake piece | Local twin |
|---|---|
| Marketplace listing | Sample CSVs loaded into a `listing` schema |
| Stored procedure and task | `python local/run_pipeline.py land` (same checks, same MERGE semantics) |
| Dynamic Tables | `CREATE TABLE AS` with the identical SELECT |
| Validation assertions | Same SQL; results written to the phase report |
| Streamlit in Snowflake | Same app code with a local data-access switch; static PNG charts if no browser is available |
| `AI_COMPLETE` narration | Executor writes the paragraph from the results JSON only, labeled `SIMULATED NARRATION` |
| Role, warehouse, resource monitor, task schedule | Written, not simulated; marked UNVERIFIED |

### 7.3 Load events the twin must simulate

| Event | Action | RAW rows after | Expected log status |
|---|---|---|---|
| 1 | Initial load of full history | 14,163 | PASSED_WITH_QUARANTINE: 2 quarantined, 44 normalized, 3 missing weeks, STALE |
| 2 | Provider adds week 2026-09-14 (11 valid rows) | 14,174 | PASSED; 9 days old, FRESH |
| 3 | Same load rerun with no source change | 14,174 | PASSED; 0 inserted, 0 updated (INV-03) |
| 4 | Provider adds week 2026-09-21 with every value x 100 | 14,174 | BLOCKED: 11 of 11 rows out of range |

Final scenario rows: **14,174 x 6 = 85,044**.

---

## 8. Phase plan

Every phase ends with a phase report (`outputs/phase_N/REPORT.md`, template in Section 11), a learnings entry in `docs/LEARNINGS.md`, and one git commit.

### Phase 0: Frame the business and set guardrails

- **Business question**: Why is a broker exposed to diesel prices if it buys no fuel, and where in its operating cycle is that exposure created?
- **Build**: `docs/00_vision.md` (Section 1), `docs/01_business_context.md` (Section 3), `docs/02_business_rules.md` (Section 4), `docs/03_requirements.md` (Section 5, plus a traceability table mapping every BR and FR to a named test), `docs/assumptions_register.md`, `docs/sources.md`, `docs/architecture.md` (a Mermaid flowchart of Section 7), `sql/00_setup.sql`.
- **Sample result**: a hand-worked 6-week example (SYNTHETIC numbers) showing both clocks and the spread under S5, computed with BR-01 to BR-06.
- **Exit**: every rule and requirement has an ID and a named test.
- **Explain-back**: Why is the broker exposed? Why is region a dimension and not a lever?
- **Commit**: `phase-0: business framing, rules, requirements, guardrails`

### Phase 1: Profile the listing

- **Business question**: Can this data support two surcharge clocks?
- **Build**: `local/generate_sample_data.py`, everything in `data/sample/`, and `sql/01_profiling.sql`, based on the existing Steps 0 to 9 and the six-item exit checklist, with four updates:
  - Use `FUEL_WH` instead of `COMPUTE_WH`.
  - Add a weekday check (`DAYNAME(date)` counts).
  - Add a search for regions stored as separate variable names.
  - Update the comments: in the broker framing, Step 3 (retail diesel exists) and Step 7 (weekly frequency) are make-or-break. Step 5 (geography) decides scope only.
- **Run**: generate the sample, then run every profiling step against the local listing.
- **Sample results**: the six checklist answers for the SYNTHETIC listing, plus which planted traps each step surfaced.
- **Exit**: all six answers recorded; STOP rules evaluated (none should trigger on the sample).
- **Explain-back**: Which answers could stop the project? Why did the first Step 5 query show only one geography?
- **Commit**: `phase-1: synthetic listing, profiling queries, exit checklist`

### Phase 2: Land a validated copy

- **Business question**: Is this week's data safe to use for pricing decisions?
- **Build**: `sql/02_landing.sql`: `RAW.DIESEL_WEEKLY`, `RAW.QUARANTINE`, `RAW.LOAD_LOG`, the stored procedure, and the task (created suspended).
- **Run**: load events 1 to 4 (Section 7.3).
- **Sample results**: `LOAD_LOG` after all four events, the quarantine table, and freshness status before and after event 2.
- **Exit**: counts match Section 7.3 exactly; INV-03 passes.
- **Explain-back**: Why copy the share instead of reading it in place? What is the difference between quarantining a row and blocking a batch?
- **Commit**: `phase-2: validated idempotent landing, quarantine, load log`

### Phase 3: Build the two clocks

- **Business question**: Each week, what does the broker pay the carrier and bill the shipper?
- **Build**: `sql/03_seeds.sql`, and part 1 of `sql/04_dynamic_tables.sql` (`DT_DIESEL_WEEKLY`, `DT_SURCHARGE_CLOCKS`).
- **Key pattern**: the shipper reset price is `FIRST_VALUE(price) OVER (PARTITION BY geo_id, scenario_id, reset_period ORDER BY week_date)`, where `reset_period` is the week itself, `DATE_TRUNC('MONTH', week_date)`, or `DATE_TRUNC('QUARTER', week_date)`. Because it only sees rows that exist, it applies BR-13 automatically. Log a substitution whenever the reset week is not the period's first calendar Monday.
- **Sample results**: an 8-week excerpt for one region under S1, S3, and S5, and the PADD4 March 2011 substitution.
- **Exit**: scenario rows = valid weeks x 6; carrier FSC is never negative; with the clause OFF, shipper FSC is constant within each reset period.
- **Explain-back**: What makes the shipper clock slow in SQL? Why does `FIRST_VALUE` handle a missing reset week on its own?
- **Commit**: `phase-3: seeds and two-clock dynamic tables`

### Phase 4: Measure the spread

- **Business questions** (restate in the report):
  - How big is the spread under weekly, monthly, and quarterly shipper resets?
  - Which price regimes squeeze margin, and which cushion it?
  - Is the squeeze predictably worse in the heating season?
  - Does a seasonal step-up clause close the gap, and by how much?
  - Is it worse in some regions (if regions exist)?
- **Build**: part 2 of `sql/04_dynamic_tables.sql` (`DT_MARGIN_SPREAD`, `DT_SCENARIO_SUMMARY`), and `sql/05_validation.sql`.
- **Run order**: INV-01 first. If it fails, stop and debug before reading any other result.
- **Analyses**:
  - Spread by scenario; by regime and season; by region over a common window.
  - Worst 4-week stretches; share of squeeze weeks; P10, P50, P90.
  - Clause effect: S5 versus S6, and S3 versus S4.
  - Dollars per 1,000 loads.
  - Sensitivity runs for A-01, A-02, A-05, A-07, and A-08.
  - Planted-effect recovery (E1 to E4).
- **Sample results** (every title says SYNTHETIC): summary tables as CSV, and PNG charts for spread over time (S1, S3, S5, US), a regime and season heatmap, the clause effect, the regional comparison, and planted versus recovered effects.
- **Exit**: INV-01 to INV-05 pass; recovery results reported against tolerances.
- **Key learning to state**: separate mechanism from magnitude. The mechanism (slow resets squeeze margin in rising markets and cushion it in falling ones) follows from the rules and holds on any data. The magnitude (how much, when, and where) depends on the data, so on synthetic data it only echoes what was planted.
- **Explain-back**: Why must S1 show zero? Which results would change on real data, and which cannot?
- **Commit**: `phase-4: margin spread, validation suite, planted-effect recovery`

### Phase 5: Serve and translate

- **Business question**: What should a broker's pricing team change in its shipper contracts?
- **Build**:
  - `app/streamlit_app.py`, with pages for Overview, Scenario explorer, Data quality, and Assumptions. Data access uses `get_active_session()` in Snowflake and DuckDB locally.
  - Optional `sql/06_narration.sql`, calling `AI_COMPLETE` with the summary passed as JSON and an instruction to use only those numbers.
  - `docs/business_memo.md`: decision first, then evidence, then limits, with a SYNTHETIC banner for the dry run.
  - `docs/linkedin_method_post.md`: the method only, no results.
- **Sample results**: app screenshots if the environment can render them, otherwise PNGs of each view plus a written walkthrough; one `SIMULATED NARRATION` paragraph.
- **Exit**: every number in the memo, post, and narration traces to a results table row (include a traceability table in the report). Rate the memo against Section 9 as Ready to share, Share with caveats, or Needs revision.
- **Explain-back**: Why does the LLM narrate but never calculate? What decision does the memo ask for?
- **Commit**: `phase-5: app, narration, memo, method post`

### Phase 6: Package and publish

- **Build**: `README.md` (problem, approach, architecture diagram, Snowflake run order, local twin instructions, SYNTHETIC results preview, data quality traps table, limitations, disclosure line), `docs/LEARNINGS.md` (all phases), `sql/99_teardown.sql`, `.gitignore`, `LICENSE` (MIT), and a pinned `local/requirements.txt`.
- **Disclosure line for the README**: "The sample build in this repository was generated with AI assistance on synthetic data to test the method end to end. The problem framing, business rules, and validation design are the author's. Findings will come from the real run in Snowflake."
- **Publish**: see Section 10.
- **Exit**: Definition of done (Section 12).
- **Commit**: `phase-6: readme, learnings, teardown, packaging`, then tag `v0.1-synthetic-dry-run`.

---

## 9. Rigor checklist (apply in Phases 4 and 5)

**Analytical**

- **Control first**: INV-01 passes before any other result is read.
- **Known-answer tests**: on synthetic data, recover planted effects and report the error.
- **Sensitivity**: rerun key results across every ILLUSTRATIVE assumption's range, and report which conclusions change.
- **No look-ahead**: any parameter calibrated from data uses only data from before the evaluation window.
- **Distributions over averages**: report shares, worst stretches, and percentiles, not just means.
- **Aggregate from weekly rows**: never average pre-computed averages.
- **Complete periods only** in period comparisons (BR-18).
- **Rolling windows count rows, not weeks**: exclude a 4-week window if its first and last weeks are more than 21 days apart.
- **Common windows**: regional comparisons use the same weeks for every region.
- **Mechanism versus magnitude** is stated explicitly next to results.
- **Descriptive, not predictive.**
- **Red flag**: on real data, a result that perfectly confirms the hypothesis gets investigated before it is reported.

**Technical**

- Every script reruns safely, and every object has a teardown path.
- Row counts are checked after every join.
- Every check returns zero rows on pass and names the failing rows on fail.

**Presentation**

- Chart titles state the insight and the date range; bar charts start at zero; comparison panels share scales.
- Every limitation sits next to the result it limits.

---

## 10. Repository and GitHub

**Repository name**: `fuel-surcharge-timing-gap`

```
fuel-surcharge-timing-gap/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── 00_vision.md
│   ├── 01_business_context.md
│   ├── 02_business_rules.md
│   ├── 03_requirements.md
│   ├── assumptions_register.md
│   ├── sources.md
│   ├── architecture.md
│   ├── business_memo.md
│   ├── linkedin_method_post.md
│   ├── LEARNINGS.md
│   └── BUILD_BRIEF.md              (this file)
├── sql/
│   ├── 00_setup.sql
│   ├── 01_profiling.sql
│   ├── 02_landing.sql
│   ├── 03_seeds.sql
│   ├── 04_dynamic_tables.sql
│   ├── 05_validation.sql
│   ├── 06_narration.sql            (optional)
│   └── 99_teardown.sql
├── app/
│   └── streamlit_app.py
├── local/
│   ├── generate_sample_data.py
│   ├── run_pipeline.py
│   ├── requirements.txt
│   └── dialect_notes.md
├── data/
│   └── sample/                     (every file prefixed SYNTHETIC_, plus README.md)
└── outputs/
    └── phase_0/ to phase_6/        (REPORT.md, CSVs, PNGs)
```

- **Commits**: one per phase, in order, using the messages in Section 8, so the history reads as the build story.
- **`.gitignore`**: `*.duckdb`, `*.db`, `__pycache__/`, `.venv/`, `.env`, `.streamlit/secrets.toml`, `*.zip`.
- **Never commit**: credentials, Snowflake account identifiers, tokens, or extracts of real listing data.

**Publishing**

- **With git and GitHub access** (for example, the GitHub CLI `gh` authenticated on the user's machine): create the repository (ask whether it should be public or private if the user has not said), commit each phase, push `main`, and push the tag.
- **Without access**: produce `fuel-surcharge-timing-gap.zip` containing the full repository, including its `.git` history. Tell the user to create an empty GitHub repository with the same name (no README), then run:

```bash
cd fuel-surcharge-timing-gap
git remote add origin https://github.com/<your-username>/fuel-surcharge-timing-gap.git
git push -u origin main --tags
```

---

## 11. Templates

**Phase report** (`outputs/phase_N/REPORT.md`)

```markdown
# Phase N: <name>   [SYNTHETIC DRY RUN]

Business question:
What was built: (files, one line each)
How it ran: (commands, run time)
Sample results: (tables of 20 rows or fewer, links to charts)
Validation: (check | expected | actual | pass or fail)
Surprises and fixes: (what broke, why, what changed)
Learnings:
  - Technical: (Snowflake or SQL concept)
  - Data: (trap found or handled)
  - Analytical: (method insight)
  - Business: (what it means for a pricing team)
Explain-back questions: (3, each with a model answer)
Exit criteria: (met or not met)
```

**Learnings log entry** (`docs/LEARNINGS.md`)

```markdown
## Phase N: <name>
Expected:
What happened:
What I changed:
Concept I can now explain:
```

---

## 12. Definition of done

- [ ] Every file in Section 10 exists and follows the ground rules.
- [ ] The sample data matches the Section 6.6 counts exactly.
- [ ] All 8 planted errors were caught and handled as specified.
- [ ] INV-01 to INV-05 pass; E1 to E3 are reported against tolerances.
- [ ] Every chart, table, and document built on the sample says SYNTHETIC.
- [ ] Every number in the memo, post, and narration traces to a results table.
- [ ] The teardown script runs twice without errors (Snowflake version marked UNVERIFIED until run).
- [ ] A stranger can rerun the local twin from the README in under 15 minutes.
- [ ] Seven phase reports and a complete `docs/LEARNINGS.md` exist.
- [ ] The repository is pushed, or a zip plus push commands has been delivered.

---

## 13. After the dry run: the real build in Snowflake

1. Run `sql/00_setup.sql` (as ACCOUNTADMIN for the resource monitor, then switch to `FUEL_ANALYST`).
2. Get the Snowflake Public Data (Free) listing and grant it to the role.
3. Run `sql/01_profiling.sql`, record the six answers, and apply the STOP rules honestly.
4. Put the real names in `CONFIG.SOURCE_CONFIG`. Set A-09 and A-10 from the profiling results. Drop the regional analysis if the listing is national only.
5. Run `sql/02_landing.sql`, `CALL` the procedure once by hand, then resume the task.
6. Run `sql/03_seeds.sql`, `sql/04_dynamic_tables.sql`, and `sql/05_validation.sql`.
7. Deploy the app and record a demo. Viewers need a Snowflake login, and the trial ends after 30 days or when free credits run out, whichever comes first.
8. Write the real memo. Expect real results to differ from the dry run; that difference is the point.
9. Keep the dry run in `outputs/` as the method-validation record. Never mix synthetic and real results in one chart.
10. Optional: enable AI features and use Cortex Code as a tutor while rebuilding. Ask it to explain each query before you run it.

---

## 14. Sources to carry into `docs/sources.md`

- EIA, factors affecting diesel prices (heating oil competition, West Coast pricing): https://www.eia.gov/energyexplained/diesel-fuel/factors-affecting-diesel-prices.php
- EIA, heating oil and propane survey window (October through March): https://www.eia.gov/todayinenergy/detail.php?id=47396
- Snowflake, trial account limitations: https://docs.snowflake.com/en/user-guide/admin-trial-account
- Snowflake, dynamic tables and shared data: https://docs.snowflake.com/en/user-guide/dynamic-tables/sharing
- Surcharge schedule: `TODO(source)` until a public, formula-style schedule is verified.
