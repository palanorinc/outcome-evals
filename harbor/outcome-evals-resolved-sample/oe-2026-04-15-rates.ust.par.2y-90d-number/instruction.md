# Outcome Evals: oe-2026-04-15-rates.ust.par.2y-90d-number

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-04-15-rates.ust.par.2y-90d-number
Today is 2026-04-15.

What will the 2-year U.S. Treasury par yield (Treasury daily par yield curve) be for 2026-07-14 (or the last business day before it with a published reading)?

Resolves on the latest reading dated on or before 2026-07-14 (and no more than 5 days before it), using the reading itself, as published in series `rates.ust.par.2y`. If no such reading is published within 46 days after the deadline, the question is void.
Series: U.S. Treasury Par Yield, 2-Year (Daily) (U.S. Department of the Treasury, Bureau of the Fiscal Service), unit: pct.

Readings published by 2026-04-15 (latest 24, oldest first):
date  reading
2026-03-12  3.76
2026-03-13  3.73
2026-03-16  3.68
2026-03-17  3.68
2026-03-18  3.76
2026-03-19  3.79
2026-03-20  3.88
2026-03-23  3.83
2026-03-24  3.9
2026-03-25  3.84
2026-03-26  3.96
2026-03-27  3.88
2026-03-30  3.82
2026-03-31  3.79
2026-04-01  3.81
2026-04-02  3.79
2026-04-03  3.84
2026-04-06  3.84
2026-04-07  3.81
2026-04-08  3.79
2026-04-09  3.78
2026-04-10  3.81
2026-04-13  3.78
2026-04-14  3.76

Give your best estimate of the value in the question's terms. End your reply with one line: VALUE: <number>
```

Write your answer to `/app/answer.json` as JSON: `{"value": <number>}`, your estimate in the question's terms.
