# Outcome Evals: oe-2025-07-15-avg-hrly-earn-30d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-07-15-avg-hrly-earn-30d-range
Today is 2025-07-15.

Will the 12-month change in U.S. average hourly earnings of all private employees (BLS, seasonally adjusted; computed from the level) for August 2025 (the latest monthly reading dated on or before 2025-08-14) be at least 3.70% and below 4.10%?

Resolves on the latest reading dated on or before 2025-08-14 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `avg-hrly-earn`. If no such reading is published within 85 days after the deadline, the question is void.
Series: U.S. Average Hourly Earnings, All Private Employees (U.S. Bureau of Labor Statistics), unit: $ per hour.

Readings published by 2025-07-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2023-07-01  33.85  ->  4.669
2023-08-01  33.89  ->  4.470
2023-09-01  34.01  ->  4.421
2023-10-01  34.08  ->  4.220
2023-11-01  34.17  ->  4.113
2023-12-01  34.29  ->  4.098
2024-01-01  34.47  ->  4.391
2024-02-01  34.52  ->  4.133
2024-03-01  34.65  ->  4.148
2024-04-01  34.76  ->  3.978
2024-05-01  34.89  ->  4.149
2024-06-01  35.01  ->  3.918
2024-07-01  35.08  ->  3.634
2024-08-01  35.22  ->  3.924
2024-09-01  35.34  ->  3.911
2024-10-01  35.46  ->  4.049
2024-11-01  35.6  ->  4.185
2024-12-01  35.69  ->  4.083
2025-01-01  35.84  ->  3.974
2025-02-01  35.94  ->  4.114
2025-03-01  36.11  ->  4.214
2025-04-01  36.12  ->  3.913
2025-05-01  36.28  ->  3.984
2025-06-01  36.36  ->  3.856

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
