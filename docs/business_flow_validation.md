# How the business flow has been validated

Status: public-source review completed September 24, 2026 (America/New_York). No brokerage interviews, actual contracts, invoices or shipment records have been examined. All project results remain SYNTHETIC.

## What is supported, and what is assumed?

| Statement | Evidence | Status and limit |
|---|---|---|
| A broker arranges transportation between shipper and carrier | FMCSA's definitions of operating roles [1] | Supported general role; not a process study of any company |
| EIA prices can be inputs to fuel-pricing formulas | EIA fuel-surcharge FAQ [2] | Supported; EIA does not set the surcharge or endorse our formula |
| Fuel terms are privately negotiated and can differ | EIA FAQ [2] | Supported; does not validate our chosen numbers |
| Weekly and monthly adjustments occur in U.S. trucking contracts | C.H. Robinson's automotive market commentary [3] | Industry example, not a representative survey or evidence of a paired broker contract |
| Contract pricing differs from negotiated all-in spot pricing | C.H. Robinson's March discussion [4] | Supported distinction; an all-in price combines fuel with the transport price |
| A broker pays weekly adjustments while billing monthly or quarterly adjustments | No paired contracts inspected | Model assumption; prevalence unknown; quarterly reset is a stress scenario |
| A seasonal step-up is commercially acceptable | No supporting agreement or interview | Illustrative clause; extra modeled collection is not proven savings or acceptance |
| Our spread measures company profit | No company ledger or operating-cost data | Unsupported; the measure isolates one surcharge component |

The lag discussed in source [4] concerns a carrier's pump cost versus reimbursement based on earlier prices. That supports the relevance of timing, but it is not direct evidence of our broker's two-contract mismatch. Likewise, a monthly invoice does not imply a monthly surcharge reset: an invoice can contain charges calculated using several weekly rates.

## What did our earlier checks actually validate?

The local tests verified implementation behavior on generated inputs: known bad records, repeat loads, zero spread for identical terms, planted effects and reconciled totals. Earlier source checks covered diesel definitions and Snowflake features. They did not establish our assumed customer/carrier contract pairing or validate a company's operating process.

This source review exposed wording that was too certain in the original vision and business context. In particular, universal weekly-versus-monthly/quarterly language, implied completed real-data analysis and a claim that one control proves correctness were not justified. The current reader-facing documents qualify those claims. The original build brief and previous audit remain historical records; their wording should not override this evidence assessment.

## What would business validation require next?

1. Ask a brokerage pricing or operations practitioner to walk through one shipment from customer quote to final carrier and customer invoices. Record who confirmed the process, when, and any exceptions.
2. Obtain permission to inspect a small anonymized set of matched customer terms, carrier terms and completed shipments. Include ordinary weeks, a reset boundary and a correction or dispute where available. A small set tests applicability; it cannot estimate industry prevalence.
3. Extract each side's index, formula or surcharge table, baseline, fuel-efficiency assumption, mileage basis, rounding, floors/caps, lag, reset frequency and effective shipment date. Record whether fuel is separately identified or included in an all-in price.
4. Calculate expected charges for those shipments and reconcile them to both invoices. Agree acceptance criteria with the business owner before examining differences; explain each difference rather than tuning assumptions to force a match.
5. Review total transport charges and additional fees. A change to the fuel component can be offset elsewhere in negotiated pricing. Keep surcharge exposure separate from overall profitability and payment timing.
6. Have the business owner confirm the scope: which customers, carriers and contracts the model represents, where it does not apply, and which decisions it can support.

Real EIA observations would validate a historical-price scenario. Matched contracts and invoices are needed to validate actual commercial outcomes. Live technical deployment is a separate requirement.

## Sources and their limits

[1] [FMCSA: definitions of motor carrier, broker and freight forwarder](https://www.fmcsa.dot.gov/faq/what-are-definitions-motor-carrier-broker-and-freight-forwarder-authorities). Used for roles, not a legal opinion on a specific company's obligations.

[2] [EIA: How do I calculate diesel fuel surcharges?](https://www.eia.gov/tools/faqs/faq.php?id=2&t=5). Used for the distinction between published fuel prices and privately negotiated charges.

[3] [C.H. Robinson: May 2026 automotive market update](https://www.chrobinson.com/en-us/resources/insights-and-advisories/north-america-freight-insights/may-2026-freight-market-update/industry-insights/automotive/), section on U.S. versus Mexico fuel surcharges. Used only as an example of adjustment frequencies, not to generalize globally.

[4] [C.H. Robinson: March 19, 2026 market discussion](https://www.chrobinson.com/en-us/resources/insights-and-advisories/north-america-freight-insights/rr-03-19-2026/), fuel discussion. Used for contract/spot distinctions and the need to examine combined transport pricing. It is commercial practitioner commentary, not an independent estimate of mismatch prevalence.
