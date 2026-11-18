# Outcome Evals: oe-2024-04-15-fred_core_cpi-30d-threshold

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-04-15-fred_core_cpi-30d-threshold
Today is 2024-04-15.

Will the 12-month change in U.S. core CPI (CPI-U less food and energy, seasonally adjusted; computed from the index) for May 2024 (the latest monthly reading dated on or before 2024-05-15) be below 3.70%?

Resolves on the latest reading dated on or before 2024-05-15 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `fred_core_cpi`. If no such reading is published within 90 days after the deadline, the question is void.
Series: Core CPI (U.S. Bureau of Labor Statistics), unit: index.

Readings published by 2024-04-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2022-04-01  290.514  ->  6.159
2022-05-01  292.063  ->  6.025
2022-06-01  294.05  ->  5.906
2022-07-01  295.088  ->  5.900
2022-08-01  296.535  ->  6.286
2022-09-01  298.226  ->  6.624
2022-10-01  299.399  ->  6.295
2022-11-01  300.325  ->  5.970
2022-12-01  301.394  ->  5.686
2023-01-01  302.642  ->  5.540
2023-02-01  304.123  ->  5.498
2023-03-01  305.147  ->  5.567
2023-04-01  306.534  ->  5.514
2023-05-01  307.652  ->  5.338
2023-06-01  308.322  ->  4.854
2023-07-01  308.96  ->  4.701
2023-08-01  309.58  ->  4.399
2023-09-01  310.539  ->  4.129
2023-10-01  311.457  ->  4.027
2023-11-01  312.392  ->  4.018
2023-12-01  313.195  ->  3.915
2024-01-01  314.319  ->  3.858
2024-02-01  315.564  ->  3.762
2024-03-01  316.792  ->  3.816

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
