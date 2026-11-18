# Outcome Evals: oe-2025-01-15-fred_pcepilfe-30d-threshold

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-01-15-fred_pcepilfe-30d-threshold
Today is 2025-01-15.

Will the 12-month change in the U.S. core PCE price index, excluding food and energy (BEA, seasonally adjusted; computed from the index) for February 2025 (the latest monthly reading dated on or before 2025-02-14) be below 2.70%?

Resolves on the latest reading dated on or before 2025-02-14 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `fred_pcepilfe`. If no such reading is published within 107 days after the deadline, the question is void.
Series: U.S. Core PCE Price Index (U.S. Bureau of Economic Analysis), unit: index (2017=100).

Readings published by 2025-01-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2022-12-01  116.923  ->  5.071
2023-01-01  117.415  ->  5.002
2023-02-01  117.825  ->  4.862
2023-03-01  118.295  ->  4.865
2023-04-01  118.671  ->  4.853
2023-05-01  119.061  ->  4.834
2023-06-01  119.35  ->  4.443
2023-07-01  119.515  ->  4.236
2023-08-01  119.662  ->  3.830
2023-09-01  120.053  ->  3.738
2023-10-01  120.321  ->  3.559
2023-11-01  120.525  ->  3.437
2023-12-01  120.694  ->  3.225
2024-01-01  121.201  ->  3.224
2024-02-01  121.57  ->  3.178
2024-03-01  122.016  ->  3.146
2024-04-01  122.252  ->  3.018
2024-05-01  122.406  ->  2.809
2024-06-01  122.667  ->  2.779
2024-07-01  122.872  ->  2.809
2024-08-01  123.135  ->  2.902
2024-09-01  123.462  ->  2.840
2024-10-01  123.816  ->  2.905
2024-11-01  123.989  ->  2.874

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
