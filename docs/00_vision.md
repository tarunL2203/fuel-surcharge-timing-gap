# The broker's two clocks

**Engineering focus: reliable ingestion and explainable timing calculations.**

The inspected real source contains 16,275 weekly price observations across 10 geographies and ends on June 22, 2026, as reviewed on September 27. It supports historical analysis; current-feed availability is unresolved. Contracts, invoices and shipment volumes are unavailable, so this project cannot establish actual brokerage margins. The published analytical results remain SYNTHETIC. [Dataset availability and evidence](dataset_availability.md) separates observed coverage from pending deployment and business validation.

A freight broker arranges transport between a shipper with goods to move and a carrier that moves them. This project asks what happens to the fuel-surcharge component when the broker's customer charges and carrier charges follow different update schedules.

## Why this problem interests me

I want to connect data analysis to a decision a small business owner can recognize: whether the terms used to charge a customer keep pace with the terms used to pay a supplier. Freight brokerage provides a concrete way to investigate that question through fuel surcharges.

What interests me is the combination of business reasoning and reliable execution. A chart can reveal a pattern, but an owner also needs to know which contract assumptions produced it, whether the input data is complete, and whether the calculation will still work when another week of data arrives. This project brings those questions together in a repeatable process.

The intended user is a small freight brokerage owner or pricing manager whose agreements identify a fuel component. It is a proposed decision-support use case, not evidence that every small brokerage has this problem or wants this product. The model does not yet establish usefulness for a business that buys and sells transport at a single price including fuel.

## Where the engineering complexity sits

The design combines a real-source adapter with a deterministic synthetic test environment. Artificial errors and known answers let us exercise failure paths before trusting the real feed. Shared SQL connects both tracks, while Snowflake execution is validated separately.

The creative part is turning a simple timing question into a system that can explain its own results: which source rows were accepted, which corrections changed history, which reset price applied, and which assumptions produced each summary. Dataset size alone does not require Snowflake; this project uses it to practice managed execution, access control, refresh behavior and an app close to the data. Those operational benefits remain to be verified in this deployment.

## The challenges I am addressing

| Practical question | What the sample addresses | What a business version still needs |
|---|---|---|
| What do the two agreements actually say? | Makes reset schedules, formulas and assumptions explicit | Matched customer and carrier agreements, including exceptions |
| Can I trust this week's input? | Detects missing, duplicate, invalid and stale observations | Validation of the live source and a named person to resolve exceptions |
| What happens when the schedules differ? | Compares hypothetical surcharge spreads under different resets | Actual effective dates, shipment miles and invoice reconciliation |
| Is a favorable average hiding difficult weeks? | Shows adverse weeks alongside average results | Customer and shipment weighting appropriate to the business |
| Will the next update duplicate or corrupt previous work? | Tests repeated loads and rejection of bad incoming data | Scheduled operation, monitoring and recovery procedures |
| What action does the evidence support? | Provides a scenario comparison and a memo with limitations | Owner review of total transport pricing, service and contract feasibility |

## How an owner could use a validated version

Before a contract review, an owner could compare the current surcharge terms with a proposed reset schedule, identify periods requiring closer attention, and take an evidence-backed question to the customer or carrier. The useful output would explain the difference, its assumptions and any data-quality warnings in ordinary language.

That workflow is the product direction. The current app explores configured synthetic scenarios; it does not import an owner's contracts, reconcile their invoices, send alerts or recommend a commercially optimal price. The first business pilot should test whether an owner can reproduce a known invoice outcome and use the explanation in a real contract discussion. Savings or reduced review time would need to be measured during that pilot.

## What the demonstration models

The sample holds the formula and other terms constant, then compares weekly, monthly and quarterly resets. These are modeled contract scenarios, not a claim that every broker uses these terms. The resulting spread is the surcharge billed to the shipper minus the surcharge payable to the carrier. It is not total profit or a measure of cash received.

Start with [how the business process relates to the model](01_business_context.md), [the evidence behind the assumptions](business_flow_validation.md), or [the synthetic decision memo](business_memo.md).

## What can this project tell us?

It demonstrates how a timing difference can change a modeled surcharge spread, checks the calculations against known answers and provides charts and an app for exploring the assumptions. Artificial prices, planted data problems and known effects let us test the method before introducing real data.

## How do we check the calculations?

When both sides use identical formulas, indexes, lags and weekly resets, the spread should be zero. This is one useful control, not proof that all code or business assumptions are correct. Other checks cover data quality, repeated loads, known effects and reconciliation between detail and summaries.

## Does this describe actual brokerage contracts?

Only at the level of a business hypothesis. We have checked public sources for the parties' roles and the existence of differing fuel-pricing arrangements. We have not inspected paired shipper/carrier contracts, reconciled invoices or interviewed a brokerage operator. Quarterly resets and the seasonal clause remain illustrative scenarios. The [validation record](business_flow_validation.md) distinguishes supported facts from assumptions.

## What would make the results useful for a real decision?

A real application needs actual contract terms, shipment dates and miles, invoice records, and a business reviewer who can confirm how charges are applied. Replacing artificial diesel prices with real prices alone would still produce a scenario analysis, not verified company margins.

## Why include Snowflake?

The intended deployment explores managed data processing, repeatable checks and an app alongside the data. The full synthetic demonstration runs locally. Real-source access and adapter profiling have now been exercised by the owner in Snowflake; landing, refresh behavior, scheduling, operating costs and app deployment still require execution evidence.

## What if only national diesel prices are available?

The timing example can use a national index. Regional comparisons depend on actual source coverage and contract relevance. The sample's regions do not establish that a future listing contains the same coverage.
