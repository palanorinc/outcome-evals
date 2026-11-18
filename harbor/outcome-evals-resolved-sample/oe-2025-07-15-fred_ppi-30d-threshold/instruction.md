# Outcome Evals: oe-2025-07-15-fred_ppi-30d-threshold

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-07-15-fred_ppi-30d-threshold
Today is 2025-07-15.

Will the 12-month change in the U.S. Producer Price Index for all commodities (not seasonally adjusted; computed from the index) for August 2025 (the latest monthly reading dated on or before 2025-08-14) be above 3.75%?

Resolves on the latest reading dated on or before 2025-08-14 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `fred_ppi`. If no such reading is published within 91 days after the deadline, the question is void.
Series: Producer Price Index (U.S. Bureau of Labor Statistics), unit: index.

Readings published by 2025-07-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
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
2024-06-01  255.914  ->  0.809
2024-07-01  257.321  ->  1.373
2024-08-01  255.463  ->  -0.860
2024-09-01  252.682  ->  -2.415
2024-10-01  253.081  ->  -0.827
2024-11-01  253.211  ->  0.140
2024-12-01  253.423  ->  1.424
2025-01-01  257.36  ->  2.409
2025-02-01  259.498  ->  1.793
2025-03-01  258.525  ->  1.345
2025-04-01  258.392  ->  0.550
2025-05-01  258.678  ->  1.318

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
