"""An OpenEnv environment whose reward is the score at resolution (``pip install "outcome-evals[openenv]"``).

One question per episode:

- ``reset()`` deals a question (by ``seed``, ``question_id`` or in order) and
  returns its prompt;
- ``step(OutcomeAction(probability=0.7))`` (or ``value=`` for a number
  question; add ``question_id=`` over stateless HTTP) ends the episode with the reward:
  ``1 − Brier`` for yes/no, ``1 / (1 + |error| / scale)`` for a number, both
  in [0, 1].

A question that has not resolved yet returns ``reward=None`` and
``metadata["status"] = "pending"``: there is no score until the outcome is
published. Serve it with ``python -m outcome_evals.adapters.openenv_server``
or ``uvicorn outcome_evals.adapters.openenv_server:app``.
"""

from __future__ import annotations

import random
import uuid
from typing import Any

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import Action, EnvironmentMetadata, Observation, State
from pydantic import Field

from .._meta import NAME, REPO_URL
from .._version import __version__
from ..calls import Call, Forecast
from ..data import LocalData
from ..prompts import prompt
from ..resolve import record, resolve
from ..score import score_call
from ..series import Series


class OutcomeAction(Action):
    """A forecast: ``probability`` for a yes/no question, ``value`` for a number question."""

    probability: float | None = Field(default=None, ge=0.0, le=1.0, description="Probability that the answer is yes")
    value: float | None = Field(default=None, description="Estimate for a number question, in the question's terms")
    question_id: str | None = Field(
        default=None, description="Which question this answers. Needed over stateless HTTP /step; optional over WebSocket sessions."
    )


class OutcomeObservation(Observation):
    question_id: str = Field(default="", description="The question's id")
    kind: str = Field(default="", description="binary or number")
    prompt: str = Field(default="", description="The question, its rule and the readings published by the question date")
    split: str = Field(default="", description="resolved_history, live or private")


class OutcomeState(State):
    question_id: str = Field(default="")
    split: str = Field(default="")


def reward_for(call: Call, forecast: Forecast) -> tuple[float | None, dict[str, Any]]:
    """The reward for a forecast on a call with a resolution; ``None`` when not resolved."""
    r = call.resolution
    if r is None or not r.resolved:
        return None, {"status": r.status if r else "pending", "reason": r.reason if r else ""}
    cs = score_call(call, forecast, r)
    if call.kind == "binary":
        assert cs.brier is not None
        return 1.0 - cs.brier, {"status": "resolved", "outcome": cs.outcome, "brier": cs.brier, "log_score": cs.log_score}
    assert cs.abs_error is not None
    scale = call.scale or 1.0
    return 1.0 / (1.0 + cs.abs_error / scale), {"status": "resolved", "actual": cs.value, "abs_error": cs.abs_error, "scale": scale}


class OutcomeEnvironment(Environment[OutcomeAction, OutcomeObservation, OutcomeState]):
    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self, calls: list[Call] | None = None, series: dict[str, Series] | None = None, split: str = "resolved_history") -> None:
        super().__init__()
        data = LocalData()
        self.calls = calls if calls is not None else data.questions(split)
        self.series = series if series is not None else data.all_series()
        self._by_id = {c.id: c for c in self.calls}
        self._next = 0
        self._call: Call | None = None
        self._state = OutcomeState(episode_id=None, step_count=0)

    def reset(self, seed: int | None = None, episode_id: str | None = None, **kwargs: Any) -> OutcomeObservation:
        if not self.calls:
            raise ValueError("no questions loaded")
        qid = kwargs.get("question_id")
        if qid:
            call = self._by_id[qid]
        elif seed is not None:
            call = random.Random(seed).choice(self.calls)
        else:
            call = self.calls[self._next % len(self.calls)]
            self._next += 1
        self._call = call
        self._state = OutcomeState(episode_id=episode_id or str(uuid.uuid4()), step_count=0, question_id=call.id, split=call.split or "")
        return OutcomeObservation(
            question_id=call.id, kind=call.kind, split=call.split or "",
            prompt=prompt(call.question_only(), self.series.get(call.series_id)), done=False, reward=None,
        )

    def step(self, action: OutcomeAction, timeout_s: float | None = None, **kwargs: Any) -> OutcomeObservation:
        if action.question_id:
            if action.question_id not in self._by_id:
                return OutcomeObservation(question_id=action.question_id, done=True, reward=None, metadata={"error": "unknown question_id"})
            self._call = self._by_id[action.question_id]
        if self._call is None:
            return OutcomeObservation(done=True, reward=None, metadata={"error": "call reset() first, or pass question_id"})
        call = self._call
        self._state.step_count += 1
        s = self.series.get(call.series_id)
        if s is not None:
            call = call.with_resolution(record(call.resolution, resolve(call, s)))
        if call.kind == "binary":
            if action.probability is None:
                return OutcomeObservation(question_id=call.id, kind=call.kind, done=True, reward=0.0, metadata={"error": "probability is required"})
            fc = Forecast(probability=action.probability)
        else:
            if action.value is None:
                return OutcomeObservation(question_id=call.id, kind=call.kind, done=True, reward=0.0, metadata={"error": "value is required"})
            fc = Forecast(value=action.value)
        reward, meta = reward_for(call, fc)
        return OutcomeObservation(question_id=call.id, kind=call.kind, split=call.split or "", done=True, reward=reward, metadata=meta)

    @property
    def state(self) -> OutcomeState:
        return self._state

    def get_metadata(self) -> EnvironmentMetadata:
        return EnvironmentMetadata(
            name="outcome_evals",
            description=f"{NAME}: dated questions about public series; the reward is the score at resolution.",
            version=__version__,
            author="Palanor, Inc.",
            documentation_url=REPO_URL,
        )
