import json
import subprocess
import sys
from pathlib import Path

from outcome_evals.cli import main

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "examples" / "bring_your_own_calls"


def test_example_runs_end_to_end():
    out = subprocess.run([sys.executable, str(EX / "run.py")], capture_output=True, text=True, check=True).stdout
    assert "Bramblewick Hardware Co. (fictional)" in out
    assert "pending: 1" in out
    assert "yes/no calls scored: 7" in out


def test_validate(capsys):
    assert main(["validate", str(EX / "bramblewick_calls.jsonl")]) == 0
    assert "10 calls, valid" in capsys.readouterr().out


def test_score_json(capsys, tmp_path):
    calls = tmp_path / "c.jsonl"
    calls.write_text("".join(line + "\n" for line in (EX / "bramblewick_calls.jsonl").read_text().splitlines() if "weekly_orders" not in line))
    assert main(["score", str(calls), "--fill-baselines", "--json"]) == 0
    d = json.loads(capsys.readouterr().out)
    assert d["n_calls"] == 8 and d["n_pending"] == 1 and d["binary"]["n"] == 6


def test_stats(capsys):
    assert main(["stats"]) == 0
    d = json.loads(capsys.readouterr().out)
    assert d["series"] == 27 and d["live"]["questions"] > 0 and d["resolved_history"]["questions"] > 0


def test_resolve_live_on_a_copy(tmp_path):
    import shutil

    from outcome_evals.data import packaged_data_dir

    dst = tmp_path / "data"
    shutil.copytree(packaged_data_dir(), dst)
    assert main(["--data", str(dst), "resolve-live", "--as-of", "2026-11-18"]) == 0
    # nothing is due on the day the batch was made
    assert (dst / "resolutions.jsonl").read_text() == ""
