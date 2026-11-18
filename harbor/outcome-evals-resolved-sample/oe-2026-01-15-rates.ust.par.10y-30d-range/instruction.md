# Outcome Evals: oe-2026-01-15-rates.ust.par.10y-30d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-01-15-rates.ust.par.10y-30d-range
Today is 2026-01-15.

Will the 10-year U.S. Treasury par yield (Treasury daily par yield curve) for 2026-02-14 (or the last business day before it with a published reading) be at least 4.05% and below 4.30%?

Resolves on the latest reading dated on or before 2026-02-14 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.10y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 10-Year (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2026-01-15 (latest 24, oldest first):
date  reading
2025-12-10  4.13
2025-12-11  4.14
2025-12-12  4.19
2025-12-15  4.18
2025-12-16  4.15
2025-12-17  4.16
2025-12-18  4.12
2025-12-19  4.16
2025-12-22  4.17
2025-12-23  4.18
2025-12-24  4.15
2025-12-26  4.14
2025-12-29  4.12
2025-12-30  4.14
2025-12-31  4.18
2026-01-02  4.19
2026-01-05  4.17
2026-01-06  4.18
2026-01-07  4.15
2026-01-08  4.19
2026-01-09  4.18
2026-01-12  4.19
2026-01-13  4.18
2026-01-14  4.15

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
