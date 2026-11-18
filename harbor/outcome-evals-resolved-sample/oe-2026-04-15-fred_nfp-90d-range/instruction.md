# Outcome Evals: oe-2026-04-15-fred_nfp-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-04-15-fred_nfp-90d-range
Today is 2026-04-15.

Will the one-month change in U.S. nonfarm payrolls (BLS, seasonally adjusted, thousands of jobs) for July 2026 (the latest monthly reading dated on or before 2026-07-14) be at least 100 thousand and below 300 thousand?

Resolves on the latest reading dated on or before 2026-07-14 (and no more than 31 days before it), using the reading minus the reading 1 month earlier, as published in series `fred_nfp`. If no such reading is published within 85 days after the deadline, the question is void.
Series: Nonfarm Payrolls (U.S. Bureau of Labor Statistics), unit: thousands of persons.

Readings published by 2026-04-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2024-04-01  157530  ->  64.000
2024-05-01  157608  ->  78.000
2024-06-01  157695  ->  87.000
2024-07-01  157748  ->  53.000
2024-08-01  157757  ->  9.000
2024-09-01  157912  ->  155.000
2024-10-01  157945  ->  33.000
2024-11-01  158079  ->  134.000
2024-12-01  158316  ->  237.000
2025-01-01  158268  ->  -48.000
2025-02-01  158310  ->  42.000
2025-03-01  158377  ->  67.000
2025-04-01  158485  ->  108.000
2025-05-01  158498  ->  13.000
2025-06-01  158478  ->  -20.000
2025-07-01  158542  ->  64.000
2025-08-01  158472  ->  -70.000
2025-09-01  158548  ->  76.000
2025-10-01  158408  ->  -140.000
2025-11-01  158449  ->  41.000
2025-12-01  158432  ->  -17.000
2026-01-01  158592  ->  160.000
2026-02-01  158436  ->  -156.000
2026-03-01  158650  ->  214.000

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
