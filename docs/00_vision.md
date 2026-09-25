# The broker's two clocks

**SYNTHETIC DRY RUN. Real contract behavior and Snowflake execution remain unverified.**

A freight broker arranges transport between a shipper with goods to move and a carrier that moves them. This project asks what happens to the fuel-surcharge component when the broker's customer charges and carrier charges follow different update schedules.

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

The intended deployment explores managed data processing, repeatable checks and an app alongside the data. The current demonstration runs locally. Marketplace availability, access, refresh behavior, costs and Snowflake execution must be verified before describing those as delivered capabilities.

## What if only national diesel prices are available?

The timing example can use a national index. Regional comparisons depend on actual source coverage and contract relevance. The sample's regions do not establish that a future listing contains the same coverage.
