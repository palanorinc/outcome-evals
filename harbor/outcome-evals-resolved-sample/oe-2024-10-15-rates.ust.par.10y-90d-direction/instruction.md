# Outcome Evals: oe-2024-10-15-rates.ust.par.10y-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-10-15-rates.ust.par.10y-90d-direction
Today is 2024-10-15.

Will the 10-year U.S. Treasury par yield (Treasury daily par yield curve) for 2025-01-13 (or the last business day before it with a published reading) be above 4.08%, its value for 2024-10-11?

Resolves on the latest reading dated on or before 2025-01-13 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.10y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 10-Year (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2024-10-15 (latest 24, oldest first):
date  reading
2024-09-10  3.65
2024-09-11  3.65
2024-09-12  3.68
2024-09-13  3.66
2024-09-16  3.63
2024-09-17  3.65
2024-09-18  3.7
2024-09-19  3.73
2024-09-20  3.73
2024-09-23  3.75
2024-09-24  3.74
2024-09-25  3.79
2024-09-26  3.79
2024-09-27  3.75
2024-09-30  3.81
2024-10-01  3.74
2024-10-02  3.79
2024-10-03  3.85
2024-10-04  3.98
2024-10-07  4.03
2024-10-08  4.04
2024-10-09  4.06
2024-10-10  4.09
2024-10-11  4.08

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
