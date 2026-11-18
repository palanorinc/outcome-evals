# Outcome Evals: oe-2025-04-15-fred_jolts-90d-range

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2025-04-15-fred_jolts-90d-range
Today is 2025-04-15.

Will U.S. job openings (BLS JOLTS, seasonally adjusted, thousands) for July 2025 (the latest monthly reading dated on or before 2025-07-14) be at least 6,800 thousand and below 7,700 thousand?

Resolves on the latest reading dated on or before 2025-07-14 (and no more than 31 days before it), using the reading itself, as published in series `fred_jolts`. If no such reading is published within 115 days after the deadline, the question is void.
Series: JOLTS Job Openings (U.S. Bureau of Labor Statistics), unit: count.

Readings published by 2025-04-15 (latest 24, oldest first):
date  reading
2023-03-01  9655
2023-04-01  9966
2023-05-01  9368
2023-06-01  9180
2023-07-01  8657
2023-08-01  9254
2023-09-01  9259
2023-10-01  8580
2023-11-01  8602
2023-12-01  8520
2024-01-01  8378
2024-02-01  8440
2024-03-01  8206
2024-04-01  7529
2024-05-01  7782
2024-06-01  7416
2024-07-01  7426
2024-08-01  7520
2024-09-01  6943
2024-10-01  7379
2024-11-01  7566
2024-12-01  7295
2025-01-01  7431
2025-02-01  7242

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
