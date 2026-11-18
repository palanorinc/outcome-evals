"""HTTP/WebSocket server for the OpenEnv environment.

    uvicorn outcome_evals.adapters.openenv_server:app --port 8000
    python -m outcome_evals.adapters.openenv_server --port 8000

``OUTCOME_EVALS_SPLIT`` picks the question set (``resolved_history`` by default, or ``live``).
"""

from __future__ import annotations

import os

from openenv.core.env_server.http_server import create_app

from .openenv_env import OutcomeAction, OutcomeEnvironment, OutcomeObservation, OutcomeState


def _factory() -> OutcomeEnvironment:
    return OutcomeEnvironment(split=os.environ.get("OUTCOME_EVALS_SPLIT", "resolved_history"))


app = create_app(
    _factory,
    OutcomeAction,
    OutcomeObservation,
    env_name="outcome_evals",
    max_concurrent_envs=8,
    state_cls=OutcomeState,
)


def main() -> None:
    import argparse

    import uvicorn

    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8000)
    a = ap.parse_args()
    uvicorn.run(app, host=a.host, port=a.port)


if __name__ == "__main__":
    main()
