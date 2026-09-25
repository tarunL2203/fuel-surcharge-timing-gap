# Real-source gate: NOT RUN

| Gate | Evidence needed | Current status |
|---|---|---|
| 1 | Listing accessible, source objects and schema known | NOT RUN |
| 2 | Retail on-highway diesel variable identified | NOT RUN |
| 3 | Dollars per gallon confirmed; range investigated | NOT RUN |
| 4 | Actual geographies checked, including variables; choose US-only or regions | NOT RUN |
| 5 | Latest date, provider lag and task schedule justified | NOT RUN |
| 6 | Weekly cadence, duplicates, gaps and shifted dates reviewed | NOT RUN |

STOP if there is no retail diesel series or it is not weekly. Unexpected units or a broken schema block landing. Geography limits scope; it does not by itself stop the national model. Do not enable the load task until the six answers, adapter schema and first manual load are reviewed.

Original referenced profiling “Steps 0 to 9” were not attached. The numbered checks in sql/01_profiling.sql implement the six stated gates; they do not claim to reproduce an unseen earlier worksheet.
