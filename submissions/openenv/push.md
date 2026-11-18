# OpenEnv

## A. Hugging Face Space (the OpenEnv hub)

    pip install "outcome-evals[openenv]"
    huggingface-cli login                 # a Palanor organization token
    openenv push openenv-env --repo-id <palanor-hf-org>/outcome-evals

`openenv-env/README.md` carries the Space front matter (`sdk: docker`, `tags: [openenv]`). The Dockerfile installs
the package from the public repository archive.

## B. Optional pull request to openenv/OpenEnv (needs the Meta CLA)

Add `envs/outcome_evals_env/` with the contents of `openenv-env/`.

**Title:** Add outcome_evals_env: dated forecasting questions, reward at resolution

**Body:**

A single-step environment from https://github.com/palanorinc/outcome-evals (MIT). `reset()` deals a dated yes/no or number question about a U.S. federal series with the readings published by its date; `step()` takes a probability or a value. The reward is the score at resolution: `1 − Brier` (yes/no) or `1 / (1 + |error| / scale)` (number), in [0, 1]. Open questions return `reward=None` until they resolve, so nothing is scored early.

`OUTCOME_EVALS_SPLIT=resolved_history` (default) serves past questions with known outcomes (labelled as not a forecasting test for models trained after the outcomes); `live` serves the open ones.

Checked: `openenv validate --url` passes all runtime checks (openapi, health, metadata, schema, mcp, mode consistency) and the static manifest check passes; HTTP and WebSocket sessions are exercised in the repository's CI.
