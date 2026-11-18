# Outcome Evals: oe-2024-07-15-fred_ppi-30d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-07-15-fred_ppi-30d-range
Today is 2024-07-15.

Will the 12-month change in the U.S. Producer Price Index for all commodities (not seasonally adjusted; computed from the index) for August 2024 (the latest monthly reading dated on or before 2024-08-14) be at least -1.25% and below 2.75%?

Resolves on the latest reading dated on or before 2024-08-14 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `fred_ppi`. If no such reading is published within 91 days after the deadline, the question is void.
Series: Producer Price Index (U.S. Bureau of Labor Statistics), unit: index.

Readings published by 2024-07-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2022-06-01  280.251  ->  22.434
2022-07-01  272.274  ->  17.435
2022-08-01  269.546  ->  15.479
2022-09-01  267.898  ->  13.671
2022-10-01  265.061  ->  10.229
2022-11-01  263.157  ->  8.167
2022-12-01  257.897  ->  6.861
2023-01-01  260.227  ->  5.589
2023-02-01  258.669  ->  2.378
2023-03-01  257.062  ->  -1.135
2023-04-01  256.908  ->  -3.167
2023-05-01  253.67  ->  -7.166
2023-06-01  253.86  ->  -9.417
2023-07-01  253.835  ->  -6.772
2023-08-01  257.68  ->  -4.402
2023-09-01  258.934  ->  -3.346
2023-10-01  255.192  ->  -3.723
2023-11-01  252.856  ->  -3.914
2023-12-01  249.866  ->  -3.114
2024-01-01  251.306  ->  -3.428
2024-02-01  254.926  ->  -1.447
2024-03-01  255.095  ->  -0.765
2024-04-01  256.978  ->  0.027
2024-05-01  255.313  ->  0.648

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
