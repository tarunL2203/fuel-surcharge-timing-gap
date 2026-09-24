# Business context

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
