# Outcome Evals

Score dated calls against what happened.

An organization makes calls all the time: "claims will stay under 230,000 through June", "housing starts hold above 1.3 million", "the 10-year ends the quarter below 4.5%". Outcome Evals gives those calls a common format, resolves each one mechanically against the published series, and scores them (Brier, log score, calibration, hit rate) beside two baselines: no change, and the historical base rate. The same questions load into [Inspect AI](https://inspect.aisi.org.uk/), [Harbor](https://github.com/laude-institute/harbor) and [OpenEnv](https://github.com/meta-pytorch/OpenEnv), so a model can be evaluated, or trained, on them.

- **A call format**: JSON Schema plus typed dataclasses (`outcome_evals/schema/call.schema.json`).
- **A resolver**: a pure function from a call and a dated series to *resolved*, *not yet* or *void*, with the reading and date it used. The rules for late readings, revisions and series that end are written down and tested.
- **Scoring** that never scores a call that hasn't resolved.
- **A public question set** from U.S. federal series (public domain), in two parts kept apart: **live** questions and **resolved history**.
- **Adapters** for Inspect AI, Harbor and OpenEnv, plus a data client that reads the shipped files with no key or Palanor's public API with one.

MIT licence for the code. Each data file keeps its source's terms: see [DATA-LICENSES.md](DATA-LICENSES.md).

## Install

```bash
pip install outcome-evals                 # core: no dependencies, Python 3.10+
pip install "outcome-evals[inspect]"      # + Inspect AI task (Python 3.11+)
pip install "outcome-evals[openenv]"      # + OpenEnv environment
```

Until the package is on PyPI, install from this repository: `pip install "outcome-evals @ git+https://github.com/palanorinc/outcome-evals"`.

## Score your own calls

Write calls as JSON Lines, one per line:

```json
{"id": "acme-001", "question": "Will U.S. initial jobless claims for the latest week on or before 2025-06-30 be above 230,000?",
 "kind": "binary", "made_on": "2025-03-10", "deadline": "2025-06-30", "series_id": "fred_jobless",
 "rule": {"comparator": ">", "threshold": 230000, "period": "W"},
 "source": "U.S. Department of Labor", "license": "Public domain (U.S. Government work)",
 "forecast": {"probability": 0.35, "forecaster": "planning team"}}
```

Then:

```bash
outcome-evals score my_calls.jsonl --fill-baselines --per-call
```

or in Python:

```python
from outcome_evals import LocalData, load_calls, resolve_all, summarize, with_baselines

calls = load_calls("my_calls.jsonl")
series = LocalData().all_series()                              # shipped series, no key
calls = [with_baselines(c, series[c.series_id]) for c in calls]  # anchor, base rate, scale
print(summarize(resolve_all(calls, series)).text())
```

A complete example with a fictional company, including a call resolved against the company's own private series, is in [`examples/bring_your_own_calls`](examples/bring_your_own_calls):

```bash
python examples/bring_your_own_calls/run.py
```

Your own series work the same way: any CSV with `timestamp` and `target` columns (`Series.from_csv`). To resolve against series that aren't shipped here, use Palanor's API with a key (a free key is at <https://palanor.com/developers/keys>):

```python
from outcome_evals import PalanorAPI
series = PalanorAPI().many({c.series_id for c in calls})   # reads PALANOR_API_KEY
```

## The call format

| Field | Meaning |
|---|---|
| `id` | Unique id. |
| `question` | The question in words. |
| `kind` | `binary` (yes/no on a threshold or a range) or `number`. |
| `made_on` | The date the call was made. |
| `deadline` | The date the rule reads the series at. |
| `series_id` | The resolving series: a public id (a Palanor signal slug such as `fred_unemployment`) or the id of your own series. |
| `rule` | How the reading is chosen and judged (below). |
| `source`, `license` | Who publishes the series, and its licence. |
| `forecast` | Optional: `probability` (binary), or `value` and optionally `quantile_levels` + `quantiles` (number), and `forecaster`. |
| `cutoff` | Optional: the last series timestamp the forecaster could see. |
| `anchor`, `base_rate`, `base_change`, `scale` | Optional baselines; `with_baselines` fills them from readings up to the cutoff. |
| `split` | `live`, `resolved_history` or `private`. |
| `resolution` | Written by the resolver. |

**The rule.** `comparator` (`>`, `>=`, `<`, `<=`) with `threshold`, or `between` with `low` (inclusive) and `high` (exclusive). `pick` is `last_on_or_before` (default: the latest reading dated on or before the deadline) or `first_on_or_after`. `period` is the series' cadence (`D`, `B` business days, `W`, `M`, `Q`, `A`). `max_gap_days` limits how far from the deadline the reading may be dated, and `grace_days` sets how long to wait after the deadline for a late publication. `transform` compares the reading itself (`level`) or its `change`, `pct_change` or `annualized_pct_change` against the reading `lag` earlier (`"1M"`, `"12M"`, `"1Q"`, `"7D"`).

## How a call resolves

1. Before the deadline, a call is always **pending**.
2. `last_on_or_before` takes the latest reading in `[deadline − max_gap_days, deadline]`. It is final once a later reading exists, or once the next reading by the series' cadence would be dated after the deadline: the December figure settles an 18 December deadline as soon as it is published.
3. **No reading on the deadline:** the call stays pending until `grace_days` after the deadline, then it is **void**. It is void at once if a later reading already exists, because the gap is then permanent. (The U.S. October 2025 CPI figure was never published; calls that need it are void.)
4. **A series that ends** before the window is void.
5. **Transforms** need the earlier reading within `tolerance_days` of (reading date − lag), or the call is void.
6. **Revisions:** the first resolution stands. Re-resolving against revised data doesn't change a recorded outcome; the new value is added to `resolution.revisions`.

## Scoring

- **Brier score** (lower is better), **log score** (natural log of the probability given to what happened; probabilities are clipped to [0.0001, 0.9999]), **calibration** in ten bins, and **hit rate** (did the forecast lean the right way; exactly 0.5 counts half).
- **No-change baseline**: the rule applied to the latest reading the forecaster could see (a probability of 1 or 0).
- **Base-rate baseline**: replay the call's own rule from every earlier reading in the past ten years (same distance, same reading choice) and count how often it held.
- **Number calls**: absolute error, RMSE, error divided by `scale` (the median absolute move over the same distance) so different units can be averaged, skill against no change, and quantile loss when quantiles are given.
- A pending or void call is counted and never scored: `score_call` raises `UnresolvedCallError`.

## The public question set

Generated by code (`outcome_evals.public_set`) from 27 U.S. federal series published by BLS, BEA, the Census Bureau, the Department of Labor, the Treasury and EIA. Each question is one of four kinds: *direction* (above the latest reading?), *threshold* (above or below a round number near the upper or lower quartile of past moves?), *range* (inside the band of typical moves?) and *number*. Every question's baselines come only from readings dated on or before its cutoff.

- **Live** (`src/outcome_evals/data/questions/live/<date>.jsonl`): open questions with deadlines 30 and 90 days after the day they were made, about periods that hadn't happened yet. **This is the part that measures forecasting.** A new batch is published on the 1st of each month, and due questions are resolved in `resolutions.jsonl`.
- **Resolved history** (`questions/resolved_history.jsonl`): the same kinds of question made on past dates (quarterly since January 2024), with their outcomes. **This part is not a test of forecasting for any model trained after the outcome**, because such a model has already read what happened. Use it to test the plumbing (formats, resolver, scorers, adapters) and as a template for an organization's private calls. Its context readings are today's revised values, not first releases.

```bash
outcome-evals stats
outcome-evals questions --split live --limit 5
outcome-evals prompt oe-2026-11-18-fred_unemployment-30d-direction
```

The no look-ahead rule: a resolved-history question's cutoff is the last reading dated at least the series' publication lag before `made_on` (for example 45 days for CPI). A live question's cutoff is the last reading actually published on `made_on`.

## Adapters

**Inspect AI**

```bash
inspect eval outcome_evals/outcome_evals --model <provider/model>                     # resolved history
inspect eval outcome_evals/outcome_evals -T split=live --model <provider/model>       # live
inspect eval outcome_evals/outcome_evals -T calls=my_calls.jsonl --model <provider/model>
inspect eval outcome_evals/outcome_evals -T fixed_probability=0.5 --model mockllm/model   # baseline, no model call
```

Metrics: `brier`, `log_score`, `hit_rate`, `no_change_brier`, `base_rate_brier`, `scaled_abs_error`, `resolved`. A live question that hasn't resolved gets a score whose values are all empty: the forecast is kept in the log for later, and the metrics skip it.

**Harbor**

```bash
outcome-evals export-harbor my-dataset                       # resolved questions → Harbor tasks
harbor run -p harbor/outcome-evals-resolved-sample -a oracle   # the oracle runs the fixed-answer baseline
```

Each task asks the agent to write `/app/answer.json`. The grader runs in a separate container. The reward is `1 − Brier` for yes/no and `1 / (1 + |error| / scale)` for numbers. Only resolved questions are exported. A 51-task sample is committed in `harbor/`.

**OpenEnv**

```bash
uvicorn outcome_evals.adapters.openenv_server:app --port 8000
```

One question per episode; `step()` takes `probability` or `value` and returns the reward at resolution (the same reward as Harbor), or `None` while the question is open. The OpenEnv package (manifest, client, Dockerfile) is in `openenv-env/`.

Tested with inspect-ai 0.3.291, harbor 0.25.0 and openenv 0.13.0.

## Relation to fev

[fev](https://github.com/autogluon/fev) evaluates time-series forecasting models on fixed tasks. Outcome Evals scores dated, decision-shaped calls (often yes/no) against a published outcome. Where the two share an idea, they share the name: series files use fev's `id`, `timestamp` and `target` columns, `cutoff` is the last timestamp a forecaster may see, and quantile forecasts use `quantile_levels`. A shipped series CSV converts to a fev dataset with `fev.utils.convert_long_df_to_hf_dataset(df, id_column="id", timestamp_column="timestamp")`; a series with a gap (CPI has no October 2025 reading) needs the gap filled before fev's frequency check.

## Development

```bash
pip install -e ".[dev,inspect,openenv]"
pytest -q
python scripts/check_against_agencies.py      # 20 resolved questions against the agencies' own figures
```

The monthly job (`.github/workflows/monthly.yml`) runs `outcome-evals refresh`, `resolve-live` and `publish-live`, runs the checks and commits the result.

## Licence

Code: MIT, © 2026 Palanor, Inc. Data: each source's own terms ([DATA-LICENSES.md](DATA-LICENSES.md)); all shipped series are U.S. Government works in the public domain. Credit the publishing agency when you use them. Nothing here implies endorsement by any agency.
