"""Each adapter loads and runs with a fixed-answer baseline. No model is called."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

try:
    import tomllib
except ImportError:  # Python 3.10
    import tomli as tomllib  # type: ignore[no-redef]

from outcome_evals import LocalData
from outcome_evals.adapters.harbor import export_dataset

ROOT = Path(__file__).resolve().parents[1]


# ---- Harbor -------------------------------------------------------------------


def test_harbor_export_and_grade(tmp_path):
    d = LocalData()
    calls = d.questions("resolved_history")[::200]
    made = export_dataset(calls, d.all_series(), tmp_path / "ds")
    assert len(made) == len(calls)
    for t in made:
        cfg = tomllib.loads((t / "task.toml").read_text())
        assert cfg["verifier"]["environment_mode"] == "separate"
        assert cfg["artifacts"] == ["/app/answer.json"]
        assert "resolution" not in (t / "environment" / "question.json").read_text()
        assert not (t / "environment" / "resolution.json").exists()
        # the agent's context holds nothing after the cutoff
        q = json.loads((t / "environment" / "question.json").read_text())
        rows = (t / "environment" / "context.csv").read_text().splitlines()[1:]
        assert rows and all(r.split(",")[1] <= q["cutoff"] for r in rows)
        # fixed-answer baseline → reward in [0, 1]
        ans = tmp_path / f"{t.name}.json"
        script = (t / "solution" / "solve.sh").read_text().replace("/app/answer.json", str(ans))
        subprocess.run(["bash", "-c", script], check=True)
        out = tmp_path / f"{t.name}-logs"
        subprocess.run([sys.executable, str(t / "tests" / "grade.py"), str(ans), str(t / "tests" / "resolution.json"), str(out)], check=True, capture_output=True)
        r = float((out / "reward.txt").read_text())
        assert 0.0 <= r <= 1.0
        if cfg["metadata"]["kind"] == "binary":
            assert r == pytest.approx(0.75)  # probability 0.5 → Brier 0.25


def test_harbor_grader_missing_answer_scores_zero(tmp_path):
    d = LocalData()
    c = next(q for q in d.questions("resolved_history") if q.kind == "binary")
    (t,) = export_dataset([c], d.all_series(), tmp_path / "ds")
    out = tmp_path / "logs"
    subprocess.run([sys.executable, str(t / "tests" / "grade.py"), str(tmp_path / "nope.json"), str(t / "tests" / "resolution.json"), str(out)], check=True, capture_output=True)
    assert float((out / "reward.txt").read_text()) == 0.0


def test_harbor_skips_unresolved(tmp_path):
    d = LocalData()
    live = d.questions("live")[:5]
    assert export_dataset(live, d.all_series(), tmp_path / "ds") == []


def test_committed_harbor_sample_matches_tasks():
    ds = ROOT / "harbor" / "outcome-evals-resolved-sample"
    cfg = tomllib.loads((ds / "dataset.toml").read_text())
    names = {t["name"].split("/", 1)[1] for t in cfg["tasks"]}
    dirs = {p.name for p in ds.glob("oe-*")}
    assert names == dirs and len(dirs) >= 50


# ---- OpenEnv -----------------------------------------------------------------


def test_openenv_reward_is_score_at_resolution():
    pytest.importorskip("openenv")
    from outcome_evals.adapters.openenv_env import OutcomeAction, OutcomeEnvironment

    env = OutcomeEnvironment()
    seen = 0
    for seed in range(20):
        o = env.reset(seed=seed)
        assert o.prompt and not o.done
        r = env.step(OutcomeAction(probability=0.5) if o.kind == "binary" else OutcomeAction(value=0.0))
        assert r.done and r.reward is not None and 0.0 <= r.reward <= 1.0
        if o.kind == "binary":
            assert r.reward == pytest.approx(0.75)
        seen += 1
    assert seen == 20
    live = OutcomeEnvironment(split="live")
    o = live.reset(seed=0)
    r = live.step(OutcomeAction(probability=0.5) if o.kind == "binary" else OutcomeAction(value=1.0))
    assert r.reward is None and r.metadata["status"] == "pending"


def test_openenv_http_and_ws():
    pytest.importorskip("openenv")
    from fastapi.testclient import TestClient

    from outcome_evals.adapters.openenv_server import app

    c = TestClient(app)
    assert c.get("/health").json()["status"] == "healthy"
    obs = c.post("/reset", json={"seed": 3}).json()["observation"]
    act = {"probability": 0.5} if obs["kind"] == "binary" else {"value": 0.0}
    res = c.post("/step", json={"action": {**act, "question_id": obs["question_id"]}}).json()
    assert res["done"] and 0.0 <= res["reward"] <= 1.0
    with c.websocket_connect("/ws") as ws:
        ws.send_json({"type": "reset", "data": {"seed": 4}})
        o = ws.receive_json()["data"]["observation"]
        ws.send_json({"type": "step", "data": {"probability": 0.5} if o["kind"] == "binary" else {"value": 0.0}})
        m = ws.receive_json()["data"]
        assert m["done"] and m["reward"] is not None


# ---- Inspect AI --------------------------------------------------------------


def test_inspect_fixed_answer_baseline(tmp_path):
    pytest.importorskip("inspect_ai")
    from inspect_ai import eval as inspect_eval

    from outcome_evals.adapters.inspect_task import outcome_evals

    (log,) = inspect_eval(outcome_evals(fixed_probability=0.5), model="mockllm/model", limit=60, log_dir=str(tmp_path), display="none")
    assert log.status == "success"
    m = {k: v.value for s in log.results.scores for k, v in s.metrics.items()}
    assert m["brier"] == pytest.approx(0.25)
    assert m["resolved"] == 60
    # no model was called
    assert not log.stats.model_usage or all(u.input_tokens == 0 for u in log.stats.model_usage.values())


def test_inspect_live_split_is_never_scored(tmp_path):
    pytest.importorskip("inspect_ai")
    from inspect_ai import eval as inspect_eval

    from outcome_evals.adapters.inspect_task import outcome_evals

    (log,) = inspect_eval(outcome_evals(split="live", fixed_probability=0.5), model="mockllm/model", limit=10, log_dir=str(tmp_path), display="none")
    m = {k: v.value for s in log.results.scores for k, v in s.metrics.items()}
    assert m["resolved"] == 0
    assert log.samples and all(s.scores["outcome_scorer"].value["brier"] is None for s in log.samples)


def test_inspect_own_calls_file(tmp_path):
    pytest.importorskip("inspect_ai")
    from inspect_ai import eval as inspect_eval

    from outcome_evals.adapters.inspect_task import outcome_evals

    calls = ROOT / "examples" / "bring_your_own_calls" / "bramblewick_calls.jsonl"
    public = tmp_path / "public.jsonl"
    public.write_text("".join(line + "\n" for line in calls.read_text().splitlines() if "bramblewick.weekly_orders" not in line))
    (log,) = inspect_eval(outcome_evals(calls=str(public), fixed_probability=0.5), model="mockllm/model", log_dir=str(tmp_path), display="none")
    assert log.status == "success" and len(log.samples) == 8
