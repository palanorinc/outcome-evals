"""Inspect AI task and scorer (``pip install "outcome-evals[inspect]"``, Python 3.11+).

    inspect eval outcome_evals/outcome_evals --model <provider/model>
    inspect eval outcome_evals/outcome_evals -T split=live --model <provider/model>
    inspect eval outcome_evals/outcome_evals -T calls=my_calls.jsonl --model <provider/model>

    # a fixed-answer baseline that calls no model at all:
    inspect eval outcome_evals/outcome_evals -T fixed_probability=0.5 --model mockllm/model

The scorer resolves each question against the series (shipped files, or
Palanor's API when ``PALANOR_API_KEY`` is set and ``api=true``). A question
that is not resolved yet gets a score whose values are all ``None``: the
forecast is kept in the log (``answer`` and ``metadata``) so it can be scored
once the question resolves (``outcome-evals score-log``), and the metrics skip it.
"""

from __future__ import annotations

from typing import Any

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.model import ModelOutput
from inspect_ai.scorer import Metric, SampleScore, Score, Scorer, Target, metric, scorer
from inspect_ai.solver import Generate, Solver, TaskState, generate, solver, system_message

from .._meta import NAME
from ..calls import Call, load_calls
from ..data import LocalData, PalanorAPI, series_for
from ..prompts import parse_answer, prompt
from ..resolve import record, resolve
from ..score import UnresolvedCallError, score_call
from ..series import Series

SYSTEM = (
    "You are forecasting a dated question about a published statistic. Use only what you are shown "
    "and what you know as of the stated date. Reason briefly, then give the final line exactly as asked."
)


def _load(split: str, calls: str | None) -> list[Call]:
    if calls:
        return load_calls(calls)
    return LocalData().questions(split)


def _series(cs: list[Call], api: bool) -> dict[str, Series]:
    return series_for(cs, api=PalanorAPI() if api else None)


def samples(cs: list[Call], series: dict[str, Series], n_context: int = 24) -> list[Sample]:
    out = []
    for c in cs:
        q = c.question_only()
        target = ""
        if c.resolution is not None and c.resolution.resolved:
            target = ("yes" if c.resolution.outcome else "no") if c.kind == "binary" else str(c.resolution.value)
        out.append(
            Sample(
                id=c.id,
                input=prompt(q, series.get(c.series_id), n_context),
                target=target,
                metadata={"call": c.to_dict(), "kind": c.kind, "series_id": c.series_id, "split": c.split or ""},
            )
        )
    return out


def _mean_of(key: str) -> Metric:
    def m(scores: list[SampleScore]) -> float:
        xs = []
        for s in scores:
            v = s.score.value
            if isinstance(v, dict) and isinstance(v.get(key), (int, float)) and not isinstance(v.get(key), bool):
                xs.append(float(v[key]))
        return sum(xs) / len(xs) if xs else float("nan")

    return m


@metric
def brier() -> Metric:
    """Mean Brier score over resolved yes/no questions (lower is better)."""
    return _mean_of("brier")


@metric
def log_score() -> Metric:
    """Mean log score over resolved yes/no questions (higher is better; 0 is perfect)."""
    return _mean_of("log_score")


@metric
def hit_rate() -> Metric:
    """Share of resolved yes/no questions where the forecast leaned the right way."""
    return _mean_of("hit")


@metric
def no_change_brier() -> Metric:
    """The no-change baseline's Brier score on the same resolved questions."""
    return _mean_of("no_change_brier")


@metric
def base_rate_brier() -> Metric:
    """The base-rate baseline's Brier score on the same resolved questions."""
    return _mean_of("base_rate_brier")


@metric
def scaled_abs_error() -> Metric:
    """Mean absolute error over resolved number questions, divided by each question's scale."""
    return _mean_of("scaled_abs_error")


@metric
def resolved() -> Metric:
    """How many questions were resolved and scored (the rest are pending or void)."""

    def m(scores: list[SampleScore]) -> float:
        return float(sum(1 for s in scores if isinstance(s.score.value, dict) and s.score.value.get("resolved") == 1))

    return m


EMPTY: dict[str, float | None] = {
    "resolved": 0, "brier": None, "log_score": None, "hit": None,
    "no_change_brier": None, "base_rate_brier": None, "scaled_abs_error": None,
}


@scorer(metrics=[brier(), log_score(), hit_rate(), no_change_brier(), base_rate_brier(), scaled_abs_error(), resolved()])
def outcome_scorer(api: bool = False) -> Scorer:
    """Resolve the question against its series and score the parsed forecast. Never scores an unresolved question."""
    cache: dict[str, Series] = {}

    async def score(state: TaskState, target: Target) -> Score:
        call = Call.from_dict(state.metadata["call"])
        completion = state.output.completion if state.output else ""
        fc = parse_answer(completion, call.kind)
        if call.series_id not in cache:
            cache.update(_series([call], api))
        res = record(call.resolution, resolve(call, cache[call.series_id]))
        meta: dict[str, Any] = {"status": res.status, "reason": res.reason, "resolution": res.to_dict()}
        answer = None if fc is None else str(fc.probability if call.kind == "binary" else fc.value)
        if fc is not None:
            meta["forecast"] = fc.to_dict()
        if not res.resolved:
            return Score(value=dict(EMPTY), answer=answer, explanation=f"not scored: {res.status} ({res.reason})", metadata=meta)
        if fc is None:
            # a resolved question with no readable answer: the worst score, so a model can't skip hard questions
            if call.kind == "binary":
                p = 0.0 if res.outcome else 1.0
                return Score(
                    value={**EMPTY, "resolved": 1, "brier": 1.0, "log_score": -9.21034, "hit": 0.0,
                           **_baselines(call, res)},
                    answer=None, explanation="no PROBABILITY line; scored as the opposite of what happened",
                    metadata={**meta, "forecast": {"probability": p}, "unparsed": True},
                )
            return Score(value=dict(EMPTY), answer=None, explanation="no VALUE line; number question left unscored", metadata={**meta, "unparsed": True})
        try:
            cs = score_call(call, fc, res)
        except UnresolvedCallError as e:  # defensive: score_call re-checks
            return Score(value=dict(EMPTY), answer=answer, explanation=str(e), metadata=meta)
        if call.kind == "binary":
            value = {**EMPTY, "resolved": 1, "brier": cs.brier, "log_score": cs.log_score, "hit": cs.hit, **_baselines(call, res)}
            expl = f"outcome {'yes' if cs.outcome else 'no'} (value {cs.value:g}); forecast {cs.probability}; Brier {cs.brier:.4f}"
        else:
            sc = call.scale or 1.0
            assert cs.abs_error is not None
            value = {**EMPTY, "resolved": 1, "scaled_abs_error": cs.abs_error / sc}
            expl = f"value {cs.value:g}; forecast {cs.forecast_value:g}; abs error {cs.abs_error:g}"
        return Score(value=value, answer=answer, explanation=expl, metadata=meta)

    return score


def _baselines(call: Call, res: Any) -> dict[str, float | None]:
    cs = score_call(call, None, res)
    return {
        "no_change_brier": cs.no_change.get("brier") if cs.no_change else None,
        "base_rate_brier": cs.base_rate.get("brier") if cs.base_rate else None,
    }


@solver
def fixed_answer(probability: float = 0.5, value: float | None = None) -> Solver:
    """A baseline that answers every question the same way and calls no model.

    Yes/no questions get ``probability``; number questions get ``value``, or
    the anchor (the no-change answer) when ``value`` is not given.
    """

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        call = Call.from_dict(state.metadata["call"])
        if call.kind == "binary":
            text = f"PROBABILITY: {probability}"
        else:
            v = value if value is not None else (call.anchor.value if call.anchor else 0.0)
            text = f"VALUE: {v}"
        state.output = ModelOutput.from_content(model="fixed-answer", content=text)
        state.completed = True
        return state

    return solve


@task
def outcome_evals(
    split: str = "resolved_history",
    calls: str | None = None,
    limit_context: int = 24,
    api: bool = False,
    fixed_probability: float | None = None,
    kinds: str = "binary,number",
) -> Task:
    """Dated questions about public series, resolved against what was published.

    Args:
        split: ``resolved_history`` (plumbing check; not a forecasting test for any
            model trained after the outcomes), ``live`` (open questions), or ``all``.
        calls: a ``.jsonl`` or ``.json`` file of your own calls instead of the public set.
        limit_context: how many recent readings to show.
        api: read series from Palanor's API (needs ``PALANOR_API_KEY``) instead of shipped files.
        fixed_probability: answer every question with this probability and call no model (a baseline).
        kinds: which question kinds to include (``binary``, ``number``).
    """
    wanted = {k.strip() for k in kinds.split(",") if k.strip()}
    cs = [c for c in _load(split, calls) if c.kind in wanted]
    series = _series(cs, api)
    solver_: list[Solver] = [fixed_answer(fixed_probability)] if fixed_probability is not None else [system_message(SYSTEM), generate()]
    return Task(
        name="outcome_evals",
        dataset=MemoryDataset(samples(cs, series, limit_context), name=f"{NAME} ({calls or split})"),
        solver=solver_,
        scorer=outcome_scorer(api=api),
        metadata={"split": split, "calls_file": calls or "", "eval": NAME},
    )
