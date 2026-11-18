# Outcome Evals: oe-2024-04-15-avg-hrly-earn-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-04-15-avg-hrly-earn-90d-direction
Today is 2024-04-15.

Will the 12-month change in U.S. average hourly earnings of all private employees (BLS, seasonally adjusted; computed from the level) for July 2024 (the latest monthly reading dated on or before 2024-07-14) be above 4.15%, its value for March 2024?

Resolves on the latest reading dated on or before 2024-07-14 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `avg-hrly-earn`. If no such reading is published within 85 days after the deadline, the question is void.
Series: U.S. Average Hourly Earnings, All Private Employees (U.S. Bureau of Labor Statistics), unit: $ per hour.

Readings published by 2024-04-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2022-04-01  31.96  ->  5.758
2022-05-01  32.1  ->  5.557
2022-06-01  32.19  ->  5.403
2022-07-01  32.34  ->  5.479
2022-08-01  32.44  ->  5.393
2022-09-01  32.57  ->  5.132
2022-10-01  32.7  ->  5.010
2022-11-01  32.82  ->  5.091
2022-12-01  32.94  ->  4.938
2023-01-01  33.02  ->  4.494
2023-02-01  33.15  ->  4.772
2023-03-01  33.27  ->  4.623
2023-04-01  33.43  ->  4.599
2023-05-01  33.5  ->  4.361
2023-06-01  33.69  ->  4.660
2023-07-01  33.85  ->  4.669
2023-08-01  33.89  ->  4.470
2023-09-01  34.01  ->  4.421
2023-10-01  34.08  ->  4.220
2023-11-01  34.17  ->  4.113
2023-12-01  34.29  ->  4.098
2024-01-01  34.47  ->  4.391
2024-02-01  34.52  ->  4.133
2024-03-01  34.65  ->  4.148

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
