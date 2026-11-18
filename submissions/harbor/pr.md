# Two ways to list the dataset

## A. Harbor Hub (preferred by the current docs)

    pip install "harbor==0.25.0"
    harbor auth login                       # a Harbor Hub account for Palanor
    harbor publish harbor/outcome-evals-resolved-sample --public

## B. Pull request to harbor-framework/harbor

Add the object in `registry-entry.json` to the end of the array in `registry.json`.

**Title:** Add outcome-evals-resolved-sample: dated questions about U.S. federal statistics

**Body:**

Adds `outcome-evals-resolved-sample` (52 tasks) from https://github.com/palanorinc/outcome-evals (MIT; data are U.S. Government works in the public domain).

Each task is one dated yes/no or number question about a U.S. federal series (BLS, BEA, Census, DOL, Treasury, EIA). The agent sees the question and the readings published by its date (`/app/context.csv`) and writes `/app/answer.json`. The grader runs in a separate container (`environment_mode = "separate"`, answer passed as an artifact) and writes `1 − Brier` for yes/no or `1 / (1 + |error| / scale)` for numbers.

These are resolved questions, so they are not a test of forecasting for a model trained after the outcomes; they exercise the format and grading. Open questions are published monthly in the repository and can be exported with `outcome-evals export-harbor` once they resolve.

Checked: `harbor lint` is clean on every task, and `harbor run -p harbor/outcome-evals-resolved-sample -a oracle -e docker` gives 52 rewards with the fixed-answer oracle (mean 0.6875), in the repository's CI.
