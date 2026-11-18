"""Export calls as a Harbor dataset (https://github.com/laude-institute/harbor).

Each question becomes one task directory::

    <task>/task.toml
    <task>/instruction.md          the question, the rule and the context readings
    <task>/environment/Dockerfile  python:3.12-slim with the context in /app
    <task>/environment/context.csv readings dated on or before the cutoff only
    <task>/solution/solve.sh       a fixed-answer baseline (probability 0.5, or the no-change value)
    <task>/tests/test.sh           runs grade.py (standard library only)
    <task>/tests/grade.py          scores /app/answer.json against the resolution
    <task>/tests/resolution.json   the resolution (never in the agent's environment)

The verifier runs in a separate container (``environment_mode = "separate"``);
Harbor copies ``/app/answer.json`` across as an artifact.

The agent writes ``/app/answer.json`` (``{"probability": 0.62}`` or
``{"value": 4.3}``). The reward written to ``/logs/verifier/reward.txt`` is
``1 − Brier`` for a yes/no question and ``1 / (1 + |error| / scale)`` for a
number question, both in [0, 1]; ``rewards.json`` carries the details.

Only resolved questions are exported: a reward is never computed for a
question that has not resolved. Building a task needs no Harbor install; running
it does (``harbor run -p <dir> -a oracle``).
"""

from __future__ import annotations

import json
import shutil
from collections.abc import Iterable
from datetime import date
from pathlib import Path

from .._meta import DIST, NAME
from .._version import __version__
from ..calls import Call
from ..prompts import prompt
from ..series import Series

ORG = "palanor"
CONTEXT_YEARS = 5  # context.csv holds the last five years of readings before the cutoff
AUTHOR = ("Palanor", "opensource@palanor.com")

GRADE_PY = r'''#!/usr/bin/env python3
"""Grade one question: read /app/answer.json, compare with tests/resolution.json, write the reward."""
import json
import math
import sys
from pathlib import Path

answer_path, resolution_path, out_dir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
out_dir.mkdir(parents=True, exist_ok=True)
res = json.loads(resolution_path.read_text())
details = {"kind": res["kind"], "status": res["status"]}
if res["status"] != "resolved":
    # never reached for exported tasks; kept so a hand-built task cannot score an unresolved question
    details["error"] = "question not resolved; no reward"
    (out_dir / "rewards.json").write_text(json.dumps(details))
    sys.exit(1)
try:
    ans = json.loads(answer_path.read_text())
except Exception as e:  # missing or malformed answer
    ans = None
    details["answer_error"] = str(e)[:200]
reward = 0.0
if res["kind"] == "binary":
    o = 1.0 if res["outcome"] else 0.0
    p = ans.get("probability") if isinstance(ans, dict) else None
    if isinstance(p, (int, float)) and not isinstance(p, bool) and 0.0 <= p <= 1.0:
        b = (p - o) ** 2
        q = min(max(p if o else 1.0 - p, 1e-4), 1.0 - 1e-4)
        reward = 1.0 - b
        details.update(probability=p, outcome=bool(o), brier=b, log_score=math.log(q))
    else:
        details.update(outcome=bool(o), brier=1.0, answer_error=details.get("answer_error", "no probability in [0, 1]"))
else:
    v = ans.get("value") if isinstance(ans, dict) else None
    if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v):
        err = abs(float(v) - res["value"])
        reward = 1.0 / (1.0 + err / res["scale"])
        details.update(value=v, actual=res["value"], abs_error=err, scale=res["scale"])
    else:
        details.update(actual=res["value"], answer_error=details.get("answer_error", "no numeric value"))
details["reward"] = reward
(out_dir / "reward.txt").write_text(f"{reward:.6f}\n")
(out_dir / "rewards.json").write_text(json.dumps({"reward": reward}))
(out_dir / "details.json").write_text(json.dumps(details, indent=2))
print(json.dumps(details))
'''

TEST_SH = """#!/bin/bash
set -u
mkdir -p /logs/verifier
python3 /tests/grade.py /app/answer.json /tests/resolution.json /logs/verifier
"""

DOCKERFILE = """FROM python:3.12-slim

WORKDIR /app
COPY context.csv question.json /app/
"""


def _toml_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def task_name(call: Call) -> str:
    return f"{ORG}/{call.id}"


def task_toml(call: Call) -> str:
    desc = call.question if len(call.question) < 300 else call.question[:297] + "..."
    hist = call.split == "resolved_history"
    lines = [
        'schema_version = "1.4"',
        "# the answer is copied from the agent's container into the separate verifier at the same path",
        'artifacts = ["/app/answer.json"]',
        "",
        "[task]",
        f"name = {_toml_str(task_name(call))}",
        f'version = "{__version__}"',
        f"description = {_toml_str(desc)}",
        f'keywords = ["forecasting", "{DIST}", {_toml_str(call.series_id)}, "{call.kind}"]',
        "",
        "[[task.authors]]",
        f'name = "{AUTHOR[0]}"',
        f'email = "{AUTHOR[1]}"',
        "",
        "[metadata]",
        f"eval = {_toml_str(NAME)}",
        f"split = {_toml_str(call.split or 'private')}",
        f"series_id = {_toml_str(call.series_id)}",
        f'kind = "{call.kind}"',
        f'made_on = "{call.made_on.isoformat()}"',
        f'deadline = "{call.deadline.isoformat()}"',
        f"source = {_toml_str(call.source)}",
        f"license = {_toml_str(call.license)}",
    ]
    if hist:
        lines.append('caveat = "Resolved history: not a test of forecasting for any model trained after the outcome."')
    lines += [
        "",
        "[verifier]",
        "timeout_sec = 120.0",
        '# the grader runs in its own container: the agent never sees tests/ or the resolution',
        'environment_mode = "separate"',
        "",
        "[agent]",
        "timeout_sec = 900.0",
        "",
        "[environment]",
        "build_timeout_sec = 600.0",
        "cpus = 1",
        "memory_mb = 1024",
        "",
    ]
    return "\n".join(lines)


def instruction(call: Call, series: Series | None) -> str:
    body = prompt(call.question_only(), series)
    if call.kind == "binary":
        how = 'Write your answer to `/app/answer.json` as JSON: `{"probability": <number from 0 to 1>}`, the probability that the answer is yes.'
    else:
        how = 'Write your answer to `/app/answer.json` as JSON: `{"value": <number>}`, your estimate in the question\'s terms.'
    caveat = ""
    if call.split == "resolved_history":
        caveat = (
            "\n\n> This question comes from the resolved-history set. Its outcome is already published, so it is "
            "not a test of forecasting for any model trained after that date. It checks the plumbing.\n"
        )
    return (
        f"# {NAME}: {call.id}\n\n"
        "The readings below are also in `/app/context.csv` (`id,timestamp,target`), and the question record "
        "(without its answer) is in `/app/question.json`.\n"
        f"{caveat}\n```text\n{body}\n```\n\n{how}\n"
    )


def solve_sh(call: Call, probability: float = 0.5) -> str:
    if call.kind == "binary":
        ans = json.dumps({"probability": probability})
    else:
        ans = json.dumps({"value": call.anchor.value if call.anchor else 0.0})
    return f"#!/bin/bash\n# Fixed-answer baseline: the same answer for every question; no model.\necho '{ans}' > /app/answer.json\n"


def resolution_json(call: Call) -> str:
    r = call.resolution
    assert r is not None and r.resolved
    d = {"id": call.id, "kind": call.kind, "status": r.status, "value": r.value, "outcome": r.outcome, "scale": call.scale or 1.0, "resolution": r.to_dict()}
    return json.dumps(d, indent=2)


def export_task(call: Call, series: Series | None, out: Path, probability: float = 0.5) -> Path:
    if call.resolution is None or not call.resolution.resolved:
        raise ValueError(f"{call.id}: not resolved; Harbor tasks are built only for resolved questions")
    d = out / call.id
    if d.exists():
        shutil.rmtree(d)
    (d / "environment").mkdir(parents=True)
    (d / "solution").mkdir()
    (d / "tests").mkdir()
    (d / "task.toml").write_text(task_toml(call), encoding="utf-8")
    (d / "instruction.md").write_text(instruction(call, series), encoding="utf-8")
    (d / "environment" / "Dockerfile").write_text(DOCKERFILE, encoding="utf-8")
    ctx = "id,timestamp,target\n"
    if series is not None and call.cutoff:
        start = date(call.cutoff.year - CONTEXT_YEARS, call.cutoff.month, min(call.cutoff.day, 28))
        hist = series.upto(call.cutoff)
        ctx = Series.from_pairs(series.info, [(t, v) for t, v in hist.pairs() if t >= start]).to_csv()
    (d / "environment" / "context.csv").write_text(ctx, encoding="utf-8")
    (d / "environment" / "question.json").write_text(json.dumps(call.question_only().to_dict(), indent=2), encoding="utf-8")
    for name, text in (("solution/solve.sh", solve_sh(call, probability)), ("tests/test.sh", TEST_SH), ("tests/grade.py", GRADE_PY)):
        p = d / name
        p.write_text(text, encoding="utf-8")
        p.chmod(0o755)
    (d / "tests" / "resolution.json").write_text(resolution_json(call), encoding="utf-8")
    return d


def dataset_toml(name: str, description: str, tasks: list[str]) -> str:
    lines = [
        "[dataset]",
        f"name = {_toml_str(f'{ORG}/{name}')}",
        f'version = "{__version__}"',
        f"description = {_toml_str(description)}",
        f'keywords = ["forecasting", "{DIST}", "calibration", "brier"]',
        "",
        "[[dataset.authors]]",
        f'name = "{AUTHOR[0]}"',
        f'email = "{AUTHOR[1]}"',
        "",
        "# Task digests are filled by `harbor sync` before publishing.",
        "",
    ]
    return "\n".join(lines)


def export_dataset(
    calls: Iterable[Call], series: dict[str, Series], out: str | Path, name: str = "outcome-evals", description: str = "", probability: float = 0.5
) -> list[Path]:
    """Write a Harbor dataset directory. Unresolved calls are skipped (never scored)."""
    o = Path(out)
    o.mkdir(parents=True, exist_ok=True)
    made = []
    for c in calls:
        if c.resolution is None or not c.resolution.resolved:
            continue
        made.append(export_task(c, series.get(c.series_id), o, probability))
    desc = description or f"{NAME}: dated questions about public series, scored against what was published."
    (o / "dataset.toml").write_text(dataset_toml(name, desc, [p.name for p in made]), encoding="utf-8")
    return made
