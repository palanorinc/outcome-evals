# Outcome Evals: oe-2026-04-15-avg-hrly-earn-30d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-04-15-avg-hrly-earn-30d-direction
Today is 2026-04-15.

Will the 12-month change in U.S. average hourly earnings of all private employees (BLS, seasonally adjusted; computed from the level) for May 2026 (the latest monthly reading dated on or before 2026-05-15) be above 3.43%, its value for March 2026?

Resolves on the latest reading dated on or before 2026-05-15 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `avg-hrly-earn`. If no such reading is published within 85 days after the deadline, the question is void.
Series: U.S. Average Hourly Earnings, All Private Employees (U.S. Bureau of Labor Statistics), unit: $ per hour.

Readings published by 2026-04-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
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
2025-07-01  36.47  ->  3.962
2025-08-01  36.62  ->  3.975
2025-09-01  36.7  ->  3.848
2025-10-01  36.85  ->  3.920
2025-11-01  37  ->  3.933
2025-12-01  37.02  ->  3.727
2026-01-01  37.15  ->  3.655
2026-02-01  37.27  ->  3.701
2026-03-01  37.35  ->  3.434

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
