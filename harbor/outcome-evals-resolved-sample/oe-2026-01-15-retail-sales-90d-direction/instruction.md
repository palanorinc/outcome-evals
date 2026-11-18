# Outcome Evals: oe-2026-01-15-retail-sales-90d-direction

The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record (without its answer) is in `/app/question.json`.


> This question comes from the resolved-history set. Its outcome is already published, so it is not a test of forecasting for any model trained after that date. It checks the plumbing.

```text
Outcome Evals question oe-2026-01-15-retail-sales-90d-direction
Today is 2026-01-15.

Will the one-month change in U.S. advance retail and food services sales (Census, seasonally adjusted; computed from the level) for April 2026 (the latest monthly reading dated on or before 2026-04-15) be above 0.72%, its value for November 2025?

Resolves on the latest reading dated on or before 2026-04-15 (and no more than 31 days before it), using the percent change from the reading 1 month earlier, as published in series `retail-sales`. If no such reading is published within 92 days after the deadline, the question is void.
Series: Retail sales · advance (U.S. Census Bureau), unit: index.

Readings published by 2026-01-15 (latest 24, oldest first):
date  reading  ->  value in the question's terms
2023-12-01  666963  ->  0.082
2024-01-01  660602  ->  -0.954
2024-02-01  664621  ->  0.608
2024-03-01  664328  ->  -0.044
2024-04-01  664858  ->  0.080
2024-05-01  667659  ->  0.421
2024-06-01  666040  ->  -0.242
2024-07-01  673662  ->  1.144
2024-08-01  670668  ->  -0.444
2024-09-01  676005  ->  0.796
2024-10-01  681808  ->  0.858
2024-11-01  685709  ->  0.572
2024-12-01  691794  ->  0.887
2025-01-01  687058  ->  -0.685
2025-02-01  683772  ->  -0.478
2025-03-01  694750  ->  1.606
2025-04-01  695464  ->  0.103
2025-05-01  685488  ->  -1.434
2025-06-01  691883  ->  0.933
2025-07-01  698280  ->  0.925
2025-08-01  700407  ->  0.305
2025-09-01  700614  ->  0.030
2025-10-01  700427  ->  -0.027
2025-11-01  705453  ->  0.718

Give your probability that the answer is yes. End your reply with one line: PROBABILITY: <a number from 0 to 1>
```

Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.
