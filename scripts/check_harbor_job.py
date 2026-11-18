"""Check a Harbor job directory: every trial has a reward in [0, 1]; yes/no tasks score 0.75 with the 0.5 baseline."""

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("job_dir")
    ap.add_argument("--expect", type=int, required=True)
    a = ap.parse_args()
    root = Path(a.job_dir)
    rewards = {}
    for f in root.rglob("reward.txt"):
        trial = next((p.name for p in f.parents if p.parent == root), f.parent.name)
        rewards[trial] = float(f.read_text().strip())
    for f in root.rglob("details.json"):
        d = json.loads(f.read_text())
        trial = next((p.name for p in f.parents if p.parent == root), f.parent.name)
        if d.get("kind") == "binary" and abs(rewards.get(trial, -1) - 0.75) > 1e-9:
            print(f"{trial}: binary reward {rewards.get(trial)} != 0.75", file=sys.stderr)
            return 1
    bad = {k: v for k, v in rewards.items() if not 0.0 <= v <= 1.0}
    print(f"{len(rewards)} rewards, mean {sum(rewards.values()) / max(len(rewards), 1):.4f}")
    if bad or len(rewards) != a.expect:
        print(f"expected {a.expect} rewards in [0, 1]; bad: {bad}", file=sys.stderr)
        for p in sorted(root.rglob("*"))[:60]:
            print(" ", p, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
