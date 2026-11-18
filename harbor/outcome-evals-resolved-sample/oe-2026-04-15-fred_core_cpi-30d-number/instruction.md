# Outcome Evals: oe-2026-04-15-fred_core_cpi-30d-number

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-04-15-fred_core_cpi-30d-number
Today is 2026-04-15.

What will the 12-month change in U.S. core CPI (CPI-U less food and energy, seasonally adjusted; computed from the index) be for May 2026 (the latest monthly reading dated on or before 2026-05-15)?

Resolves on the latest reading dated on or before 2026-05-15 (and no more than 31 days before it), using the percent change from the reading 12 months earlier, as published in series `fred_core_cpi`. If no such reading is published within 90 days after the deadline, the question is void.
Series: Core CPI (U.S. Bureau of Labor Statistics), unit: index.

Readings published by 2026-04-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2024-03-01  316.792  ->  3.816
2024-04-01  317.649  ->  3.626
2024-05-01  318.095  ->  3.394
2024-06-01  318.39  ->  3.265
2024-07-01  318.94  ->  3.230
2024-08-01  319.75  ->  3.285
2024-09-01  320.732  ->  3.282
2024-10-01  321.731  ->  3.299
2024-11-01  322.657  ->  3.286
2024-12-01  323.259  ->  3.213
2025-01-01  324.638  ->  3.283
2025-02-01  325.465  ->  3.138
2025-03-01  325.69  ->  2.809
2025-04-01  326.467  ->  2.776
2025-05-01  326.893  ->  2.766
2025-06-01  327.658  ->  2.911
2025-07-01  328.682  ->  3.054
2025-08-01  329.7  ->  3.112
2025-09-01  330.418  ->  3.020
2025-11-01  331.043  ->  2.599
2025-12-01  331.814  ->  2.646
2026-01-01  332.793  ->  2.512
2026-02-01  333.512  ->  2.472
2026-03-01  334.165  ->  2.602

Give your best estimate of the value in the question's terms. End your reply with one line: VALUE: <number>
```

Write your answer to `/app/answer.json` as JSON: `{"value": <number>}`, your estimate in the question's terms.
