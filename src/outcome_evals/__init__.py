"""Outcome Evals: score dated calls against what happened.

    from outcome_evals import LocalData, load_calls, resolve_all, summarize

    calls = load_calls("my_calls.jsonl")
    series = LocalData().all_series()          # or PalanorAPI().many(...)
    print(summarize(resolve_all(calls, series)).text())

Docs: https://github.com/palanorinc/outcome-evals
"""

from ._meta import NAME
from ._version import __version__
from .baselines import with_baselines
from .calls import Anchor, Call, CallFormatError, Forecast, Resolution, Rule, Transform, dump_calls, load_calls, validate_dict
from .data import LocalData, PalanorAPI, PalanorAPIError, series_for
from .prompts import parse_answer, prompt
from .resolve import record, resolve, resolve_all
from .score import CallScore, Summary, UnresolvedCallError, brier, calibration, log_score, score_call, summarize
from .series import Series, SeriesInfo

__all__ = [
    "NAME", "__version__",
    "Call", "Rule", "Transform", "Forecast", "Anchor", "Resolution", "CallFormatError",
    "load_calls", "dump_calls", "validate_dict",
    "Series", "SeriesInfo", "LocalData", "PalanorAPI", "PalanorAPIError", "series_for",
    "resolve", "resolve_all", "record", "with_baselines",
    "score_call", "summarize", "Summary", "CallScore", "UnresolvedCallError", "brier", "log_score", "calibration",
    "prompt", "parse_answer",
]
