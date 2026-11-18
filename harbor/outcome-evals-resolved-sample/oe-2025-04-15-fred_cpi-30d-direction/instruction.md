# Outcome Evals: oe-2025-04-15-fred_cpi-30d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-04-15-fred_cpi-30d-direction
Today is 2025-04-15.

Will the 12-month change in the U.S. Consumer Price Index (CPI-U, all items, seasonally adjusted; computed from the index) for May 2025 (the latest monthly reading dated on or before 2025-05-15) be above 2.38%, its value for March 2025?

Resolves on the latest reading dated on or before 2025-05-15 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `fred_cpi`. If no such reading is published within 90 days after the deadline, the question is void.
Series: Consumer Price Index (U.S. Bureau of Labor Statistics), unit: index.

Readings published by 2025-04-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2023-04-01  302.845  ->  4.950
2023-05-01  303.334  ->  4.132
2023-06-01  304.014  ->  3.071
2023-07-01  304.609  ->  3.288
2023-08-01  306.082  ->  3.723
2023-09-01  307.276  ->  3.687
2023-10-01  307.696  ->  3.251
2023-11-01  308.148  ->  3.133
2023-12-01  308.741  ->  3.316
2024-01-01  309.698  ->  3.088
2024-02-01  310.967  ->  3.157
2024-03-01  312.345  ->  3.487
2024-04-01  313.023  ->  3.361
2024-05-01  313.175  ->  3.244
2024-06-01  313.044  ->  2.970
2024-07-01  313.569  ->  2.941
2024-08-01  314.062  ->  2.607
2024-09-01  314.732  ->  2.426
2024-10-01  315.631  ->  2.579
2024-11-01  316.528  ->  2.719
2024-12-01  317.604  ->  2.871
2025-01-01  318.961  ->  2.991
2025-02-01  319.679  ->  2.802
2025-03-01  319.785  ->  2.382

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
