"""Client for the Outcome Evals environment.

    with OutcomeEnv(base_url="http://localhost:8000").sync() as env:
        r = env.reset(seed=1)
        print(r.observation.prompt)
        r = env.step(OutcomeAction(probability=0.6))
        print(r.reward)  # 1 - Brier once the question has resolved; None while it is open
"""

from typing import Any, Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult

from .models import OutcomeAction, OutcomeObservation, OutcomeState


class OutcomeEnv(EnvClient[OutcomeAction, OutcomeObservation, OutcomeState]):
    def _step_payload(self, action: OutcomeAction) -> Dict[str, Any]:
        return action.model_dump(exclude_none=True, exclude={"metadata"})

    def _parse_result(self, payload: Dict[str, Any]) -> StepResult[OutcomeObservation]:
        obs = dict(payload.get("observation", {}))
        obs.setdefault("done", payload.get("done", False))
        obs.setdefault("reward", payload.get("reward"))
        observation = OutcomeObservation(**obs)
        return StepResult(observation=observation, reward=payload.get("reward"), done=payload.get("done", False), metadata=payload.get("metadata"))

    def _parse_state(self, payload: Dict[str, Any]) -> OutcomeState:
        return OutcomeState(**payload)
