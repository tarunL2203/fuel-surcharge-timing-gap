# Fuel Surcharge Policy and Exposure Analytics

The loaded source contains 16,275 weekly diesel observations across 10 geographies through June 22, 2026. It contains no contracts, shipment volumes or invoices. Historical analysis is possible; live-feed readiness is unresolved. Existing analytical outputs remain SYNTHETIC. See [dataset availability](dataset_availability.md).

## Why this is interesting

A price chart explains how diesel moved. A useful pricing analysis must also explain which observation applied, which commercial rule selected it, and how the result changes under another rule. I want to build that connection in a repeatable Snowflake pipeline, with visible assumptions and an explanation for every excluded or calculated row.

The engineering challenge is not data volume. It is source adaptation, safe repeated loading, corrections, changing policy versions, date boundaries, incomplete periods and reconciliation. The completed historical landing checkpoint is a foundation for this work, not proof that the new model already operates.

## Intended decision

Help a pricing or finance team compare surcharge policies before a review. Mid-market shippers are the initial proposed audience; broker users need separately identified customer and carrier terms. [Industry sources](research/fuel_policy_evidence.md) motivate the workflow. Actual product demand and savings remain unvalidated.

The initial model compares a weekly baseline, an additional index lag and a monthly adjustment schedule using illustrative per-mile rules. The result is a modeled surcharge difference, not profit or cash flow. Quarterly and seasonal rules stay optional stress tests in the historical sample.

## What we can demonstrate

Explainable historical simulations, deterministic calculations, named missing-input exclusions, comparisons on matching dates and validation against known answers. Price provenance and policy provenance will be displayed separately. Real prices do not make hypothetical contracts real.

A later invoice check needs shipment dates, agreed mileage, exact policy versions and billed charges. Synthetic invoices can test that mechanism but cannot establish real billing errors. A current published tariff applied to older prices remains a simulation.

Read the [current brief](BUILD_BRIEF.md), [Phase 3 specification](PHASE_3_MODEL_SPEC.md) and [Snowflake next steps](SNOWFLAKE_NEXT_STEPS.md). The old sample app and reports remain available as a separate, reproducible demonstration.
