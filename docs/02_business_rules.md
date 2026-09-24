# Business rules (testable)

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
- **BR-17 Batch blocking**: a load is rejected entirely if its delta (new or changed rows versus RAW) has a schema mismatch, a unit other than dollars per gallon, or more than `BATCH_MAX_BAD_PCT` bad rows.
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

Approved clarification D-01: an unchanged rerun is PASSED with zero inserted and updated rows. An empty or malformed source is blocked. The original brief is retained unchanged for audit.
