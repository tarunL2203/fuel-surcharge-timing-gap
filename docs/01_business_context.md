# Business context

**SYNTHETIC DRY RUN.** This is a simplified U.S. truckload brokerage scenario, not a description of every broker or third-party logistics provider. See the [business-flow validation record](business_flow_validation.md) for sources and remaining evidence gaps.

### 3.1 Where this analysis fits in a shipment

The following is an illustrative process map to confirm with an actual operator. Its steps need not occur in a strict sequence, and payment dates follow the agreements rather than the moment the truck moves.

| Stage | Business activity | What this project represents |
|---|---|---|
| Quote and agree terms | Establish the customer price and carrier price, including how fuel is treated | Assumed terms only; negotiation and carrier selection are not modeled |
| Assign and move the load | Carrier transports the shipment; broker coordinates the arrangement | No dispatch, tracking or delivery workflow is implemented |
| Calculate charges | Apply the agreed rate and effective-date rules to a shipment | Hypothetical weekly surcharge calculations; no actual shipments or invoices |
| Check invoices and settle | Reconcile supporting records and amounts, then pay/collect under agreed terms | Outside scope; modeled charges are not evidence of cash payment or receipt |
| Review or renew terms | Consider cost, service and commercial acceptance | Scenario evidence for discussion, not an automatic rate recommendation |

### 3.2 What the two clocks mean here

- **Carrier clock:** the model updates the surcharge payable to the carrier weekly. This is a scenario setting, not an industry-wide rule.
- **Shipper clock:** the model updates the surcharge billable to the shipper weekly, monthly or quarterly, then holds it until the next reset. Quarterly terms have not been confirmed against an actual agreement.
- **Surcharge spread:** shipper surcharge minus carrier surcharge, in dollars per mile. Positive means a cushion in this component; negative means a squeeze. It excludes the underlying transport price, other charges and overhead.

A reset changes the price used in a calculation. It is different from the date an invoice is issued or paid. Spot freight may instead have a single negotiated price including fuel; do not invent a separate fuel component where none is available.

### 3.3 What the comparison tests

Under otherwise identical formulas, indexes and lags, changing reset frequency isolates a timing effect. Identical weekly terms must yield zero spread, but passing that control does not prove the whole model correct. Different schedules can also produce zero spread when relevant prices are unchanged.

The seasonal clause adds an illustrative increment. Its modeled effect does not establish that a customer would accept it or that the total negotiated price would improve. Public-source checks support the general mechanism; contracts and invoice reconciliation are still needed for commercial validation.

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

- As a **broker pricing analyst**, I want to change reset frequency and the seasonal clause and see the margin impact, so that I can identify terms that need further commercial review.
- As a **contracting manager**, I want the squeeze expressed in dollars per 1,000 loads, so that I can weigh it against the cost of renegotiating.
- As a **data reviewer**, I want every load validated and every assumption registered, so that I can trust the numbers.
- As a **reader exploring the analysis**, I want to see the method tested on known answers, so that I can understand what the checks establish.
- **Edge stories**: a week is missing; a contract's reset week is missing; the source goes stale; a corrupted batch arrives.
