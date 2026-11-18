# Outcome Evals: oe-2024-10-15-retail-sales-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-10-15-retail-sales-90d-range
Today is 2024-10-15.

Will the one-month change in U.S. advance retail and food services sales (Census, seasonally adjusted; computed from the level) for January 2025 (the latest monthly reading dated on or before 2025-01-13) be at least -1.30% and below 0.30%?

Resolves on the latest reading dated on or before 2025-01-13 (and no more than 31 days before it), using the percent change from the reading 1 month earlier, as published in series `retail-sales`. If no such reading is published within 92 days after the deadline, the question is void.
Series: Retail sales · advance (U.S. Census Bureau), unit: index.

Readings published by 2024-10-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2022-09-01  661072  ->  -0.291
2022-10-01  666924  ->  0.885
2022-11-01  656410  ->  -1.576
2022-12-01  648305  ->  -1.235
2023-01-01  674646  ->  4.063
2023-02-01  664692  ->  -1.475
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

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
