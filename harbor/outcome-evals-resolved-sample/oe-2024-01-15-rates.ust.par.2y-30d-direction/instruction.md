# Outcome Evals: oe-2024-01-15-rates.ust.par.2y-30d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2024-01-15-rates.ust.par.2y-30d-direction
Today is 2024-01-15.

Will the 2-year U.S. Treasury par yield (Treasury daily par yield curve) for 2024-02-14 (or the last business day before it with a published reading) be above 4.14%, its value for 2024-01-12?

Resolves on the latest reading dated on or before 2024-02-14 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.2y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 2-Year (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2024-01-15 (latest 24, oldest first):
date  reading
2023-12-08  4.71
2023-12-11  4.71
2023-12-12  4.73
2023-12-13  4.46
2023-12-14  4.37
2023-12-15  4.44
2023-12-18  4.43
2023-12-19  4.41
2023-12-20  4.34
2023-12-21  4.33
2023-12-22  4.31
2023-12-26  4.26
2023-12-27  4.2
2023-12-28  4.26
2023-12-29  4.23
2024-01-02  4.33
2024-01-03  4.33
2024-01-04  4.38
2024-01-05  4.4
2024-01-08  4.36
2024-01-09  4.36
2024-01-10  4.37
2024-01-11  4.26
2024-01-12  4.14

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
