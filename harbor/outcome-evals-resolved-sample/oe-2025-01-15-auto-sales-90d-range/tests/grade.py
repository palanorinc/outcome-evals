#!/usr/bin/env python3
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
