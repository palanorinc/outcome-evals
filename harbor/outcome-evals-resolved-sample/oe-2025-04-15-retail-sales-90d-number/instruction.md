# Outcome Evals: oe-2025-04-15-retail-sales-90d-number

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-04-15-retail-sales-90d-number
Today is 2025-04-15.

What will the one-month change in U.S. advance retail and food services sales (Census, seasonally adjusted; computed from the level) be for July 2025 (the latest monthly reading dated on or before 2025-07-14)?

Resolves on the latest reading dated on or before 2025-07-14 (and no more than 31 days before it), using the percent change from the reading 1 month earlier, as published in series `retail-sales`. If no such reading is published within 92 days after the deadline, the question is void.
Series: Retail sales · advance (U.S. Census Bureau), unit: index.

Readings published by 2025-04-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2023-03-01  655146  ->  -1.436
2023-04-01  658962  ->  0.582
2023-05-01  662303  ->  0.507
2023-06-01  664476  ->  0.328
2023-07-01  663391  ->  -0.163
2023-08-01  667632  ->  0.639
2023-09-01  671096  ->  0.519
2023-10-01  667815  ->  -0.489
2023-11-01  666419  ->  -0.209
2023-12-01  666963  ->  0.082
2024-01-01  660602  ->  -0.954
2024-02-01  664621  ->  0.608
2024-03-01  664328  ->  -0.044
2024-04-01  664858  ->  0.080
2024-05-01  667659  ->  0.421
2024-06-01  666040  ->  -0.242
2024-07-01  673662  ->  1.144
2024-08-01  670668  ->  -0.444
2024-09-01  676005  ->  0.796
2024-10-01  681808  ->  0.858
2024-11-01  685709  ->  0.572
2024-12-01  691794  ->  0.887
2025-01-01  687058  ->  -0.685
2025-02-01  683772  ->  -0.478

Give your best estimate of the value in the question's terms. End your reply with one line: VALUE: <number>
```

Write your answer to `/app/answer.json` as JSON: `{"value": <number>}`, your estimate in the question's terms.
