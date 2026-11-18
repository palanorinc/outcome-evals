# Outcome Evals: oe-2024-01-15-rates.ust.par.10y-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-01-15-rates.ust.par.10y-90d-direction
Today is 2024-01-15.

Will the 10-year U.S. Treasury par yield (Treasury daily par yield curve) for 2024-04-14 (or the last business day before it with a published reading) be above 3.96%, its value for 2024-01-12?

Resolves on the latest reading dated on or before 2024-04-14 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.10y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 10-Year (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2024-01-15 (latest 24, oldest first):
date  reading
2023-12-08  4.23
2023-12-11  4.23
2023-12-12  4.2
2023-12-13  4.04
2023-12-14  3.92
2023-12-15  3.91
2023-12-18  3.95
2023-12-19  3.93
2023-12-20  3.86
2023-12-21  3.89
2023-12-22  3.9
2023-12-26  3.89
2023-12-27  3.79
2023-12-28  3.84
2023-12-29  3.88
2024-01-02  3.95
2024-01-03  3.91
2024-01-04  3.99
2024-01-05  4.05
2024-01-08  4.01
2024-01-09  4.02
2024-01-10  4.04
2024-01-11  3.98
2024-01-12  3.96

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
