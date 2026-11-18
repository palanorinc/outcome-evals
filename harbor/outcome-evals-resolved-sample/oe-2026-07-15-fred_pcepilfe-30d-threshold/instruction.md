# Outcome Evals: oe-2026-07-15-fred_pcepilfe-30d-threshold

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-07-15-fred_pcepilfe-30d-threshold
Today is 2026-07-15.

Will the 12-month change in the U.S. core PCE price index, excluding food and energy (BEA, seasonally adjusted; computed from the index) for August 2026 (the latest monthly reading dated on or before 2026-08-14) be above 3.30%?

Resolves on the latest reading dated on or before 2026-08-14 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `fred_pcepilfe`. If no such reading is published within 107 days after the deadline, the question is void.
Series: U.S. Core PCE Price Index (U.S. Bureau of Economic Analysis), unit: index (2017=100).

Readings published by 2026-07-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2024-06-01  122.667  ->  2.779
2024-07-01  122.872  ->  2.809
2024-08-01  123.135  ->  2.902
2024-09-01  123.462  ->  2.840
2024-10-01  123.816  ->  2.905
2024-11-01  123.989  ->  2.874
2024-12-01  124.198  ->  2.903
2025-01-01  124.609  ->  2.812
2025-02-01  125.002  ->  2.823
2025-03-01  125.144  ->  2.564
2025-04-01  125.524  ->  2.676
2025-05-01  125.818  ->  2.787
2025-06-01  126.133  ->  2.826
2025-07-01  126.363  ->  2.841
2025-08-01  126.646  ->  2.851
2025-09-01  126.94  ->  2.817
2025-10-01  127.165  ->  2.705
2025-11-01  127.363  ->  2.721
2025-12-01  127.765  ->  2.872
2026-01-01  128.27  ->  2.938
2026-02-01  128.701  ->  2.959
2026-03-01  129.03  ->  3.105
2026-04-01  129.395  ->  3.084
2026-05-01  129.796  ->  3.162

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
