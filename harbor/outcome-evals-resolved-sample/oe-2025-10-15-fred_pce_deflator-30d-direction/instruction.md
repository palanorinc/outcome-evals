# Outcome Evals: oe-2025-10-15-fred_pce_deflator-30d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-10-15-fred_pce_deflator-30d-direction
Today is 2025-10-15.

Will the 12-month change in the U.S. PCE price index (BEA, seasonally adjusted; computed from the index) for November 2025 (the latest monthly reading dated on or before 2025-11-14) be above 2.69%, its value for August 2025?

Resolves on the latest reading dated on or before 2025-11-14 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `fred_pce_deflator`. If no such reading is published within 107 days after the deadline, the question is void.
Series: PCE Price Index (U.S. Bureau of Economic Analysis), unit: index.

Readings published by 2025-10-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2023-09-01  121.403  ->  3.492
2023-10-01  121.557  ->  3.100
2023-11-01  121.636  ->  2.889
2023-12-01  121.76  ->  2.862
2024-01-01  122.206  ->  2.748
2024-02-01  122.613  ->  2.807
2024-03-01  123.093  ->  2.952
2024-04-01  123.289  ->  2.839
2024-05-01  123.369  ->  2.697
2024-06-01  123.504  ->  2.570
2024-07-01  123.701  ->  2.596
2024-08-01  123.891  ->  2.437
2024-09-01  124.146  ->  2.259
2024-10-01  124.482  ->  2.406
2024-11-01  124.666  ->  2.491
2024-12-01  124.984  ->  2.648
2025-01-01  125.423  ->  2.632
2025-02-01  125.77  ->  2.575
2025-03-01  125.869  ->  2.255
2025-04-01  126.163  ->  2.331
2025-05-01  126.408  ->  2.463
2025-06-01  126.73  ->  2.612
2025-07-01  126.906  ->  2.591
2025-08-01  127.229  ->  2.694

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
