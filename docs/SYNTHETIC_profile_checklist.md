# SYNTHETIC profiling checklist


| Item | Answer |
|---|---|
| 1. Availability/schema | Local CSV listing has the expected six columns and 14,947 rows; real Marketplace not accessed. |
| 2. Target variable | DIESEL_RETAIL_ONHWY_WEEKLY; three decoys excluded. |
| 3. Units/range | USD per gallon target; one 100x outlier and one null quarantined. Defaults remain illustrative. |
| 4. Geography | Eleven actual values, only US in geography metadata. Regional synthetic scope retained. |
| 5. Freshness | Initial September 7 tail is 16 days old; September 14 update is 9 days old as of September 23. |
| 6. Cadence/quality | Weekly Mondays after 44 holiday normalizations; three absent source weeks; two extra duplicate rows. |

STOP evaluation: synthetic source contains retail diesel and weekly cadence, so no source STOP rule triggers. This does not pass the real-source gate.
