---
title: Outcome Evals
emoji: 📈
colorFrom: gray
colorTo: blue
sdk: docker
app_port: 8000
tags: [openenv]
---

# Outcome Evals for OpenEnv

One dated question per episode about a public U.S. federal series. `reset()` returns the question and the readings published by its date; `step()` takes a probability (yes/no questions) or a value (number questions) and ends the episode.

**Reward = the score at resolution:** `1 − Brier` for yes/no, `1 / (1 + |error| / scale)` for a number, both in [0, 1]. A question that has not resolved yet returns `reward = None`; it is never scored early.

`OUTCOME_EVALS_SPLIT=resolved_history` (default) serves past questions with known outcomes. **They are not a test of forecasting for any model trained after the outcome**; use them for plumbing and training-loop checks. `OUTCOME_EVALS_SPLIT=live` serves the open questions.

```bash
pip install "outcome-evals[openenv]"
uvicorn outcome_evals.adapters.openenv_server:app --port 8000
```

Over stateless HTTP, send the question id with the action: `POST /step {"action": {"probability": 0.6, "question_id": "..."}}`. WebSocket sessions (`/ws`) keep it for you.

Code, data licences and the call format: https://github.com/palanorinc/outcome-evals (MIT; data files keep their sources' terms).
