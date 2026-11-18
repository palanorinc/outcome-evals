# Outcome Evals: oe-2025-01-15-rates.ust.par.3m-30d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-01-15-rates.ust.par.3m-30d-range
Today is 2025-01-15.

Will the 3-month U.S. Treasury par yield (Treasury daily par yield curve) for 2025-02-14 (or the last business day before it with a published reading) be at least 4.35% and below 4.45%?

Resolves on the latest reading dated on or before 2025-02-14 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.3m`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 3-Month (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2025-01-15 (latest 24, oldest first):
date  reading
2024-12-10  4.41
2024-12-11  4.38
2024-12-12  4.35
2024-12-13  4.34
2024-12-16  4.37
2024-12-17  4.38
2024-12-18  4.36
2024-12-19  4.35
2024-12-20  4.34
2024-12-23  4.36
2024-12-24  4.4
2024-12-26  4.35
2024-12-27  4.31
2024-12-30  4.37
2024-12-31  4.37
2025-01-02  4.36
2025-01-03  4.34
2025-01-06  4.35
2025-01-07  4.35
2025-01-08  4.35
2025-01-09  4.35
2025-01-10  4.36
2025-01-13  4.37
2025-01-14  4.36

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
