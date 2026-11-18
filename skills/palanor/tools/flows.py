#!/usr/bin/env python3
"""Run the skill's example flows against the live Palanor MCP server, calling the tools directly (no model).

    PALANOR_API_KEY=... python skills/palanor/tools/flows.py            # every flow
    PALANOR_API_KEY=... python skills/palanor/tools/flows.py --only index --json out.json

Each step's `expect` paths must be present in the result (and `expect_error` steps must be refused). Exit 1 if
any is not. The key is read from the environment and never printed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skilllib import SERVER, load_flows  # noqa: E402

MISSING = object()


def call_tool(key: str, name: str, args: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    """(parsed result, error text). A tool-level refusal comes back as an error text, not an exception."""
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": args}}).encode()
    req = urllib.request.Request(
        SERVER,
        data=body,
        headers={
            "content-type": "application/json",
            "accept": "application/json, text/event-stream",
            "authorization": f"Bearer {key}",
            "user-agent": "palanor-skill-flows",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            msg = json.load(r)
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read()[:300].decode(errors='replace')}"
    if "error" in msg:
        return None, f"JSON-RPC error: {msg['error'].get('message')}"
    res = msg.get("result") or {}
    text = "".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
    try:
        data = json.loads(text) if text else res.get("structuredContent")
    except json.JSONDecodeError:
        data = {"text": text}
    if res.get("isError"):
        return data, (data.get("error") if isinstance(data, dict) else None) or text or "tool error"
    if isinstance(data, dict) and set(data) == {"error"}:
        return data, str(data["error"])
    return data, None


def get_path(obj: Any, path: str) -> Any:
    cur = obj
    for part in path.split("."):
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return MISSING
        elif isinstance(cur, dict):
            if part not in cur:
                return MISSING
            cur = cur[part]
        else:
            return MISSING
    return cur


def resolve_args(args: dict[str, Any], results: list[Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in args.items():
        if isinstance(v, str) and v.startswith("$"):
            step, _, path = v[1:].partition(".")
            out[k] = get_path(results[int(step)], path)
        else:
            out[k] = v
    return out


def short(v: Any, n: int = 110) -> str:
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s if len(s) <= n else s[: n - 1] + "…"


def run_flow(key: str, flow: dict[str, Any], log: list[str]) -> tuple[bool, list[Any]]:
    ok = True
    results: list[Any] = []
    log.append(f"\n## {flow['id']}: {flow['question']}")
    for step in flow["steps"]:
        args = resolve_args(step["args"], results)
        log.append(f"  → {step['call']}({', '.join(f'{k}={short(v, 60)}' for k, v in args.items())})")
        t0 = time.time()
        data, err = call_tool(key, step["call"], args)
        if "poll" in step:
            p = step["poll"]
            while err is None and get_path(data, p["until"]) != p["equals"] and time.time() - t0 < p["max_s"]:
                if get_path(data, p["until"]) in ("failed", "error"):
                    break
                time.sleep(p["every_s"])
                data, err = call_tool(key, step["call"], args)
            log.append(f"    polled {time.time() - t0:.0f} s, {p['until']} = {get_path(data, p['until'])}")
        results.append(data)
        if step.get("expect_error"):
            if err:
                log.append(f"    refused as expected: {short(err, 140)}")
            else:
                ok = False
                log.append("    FAIL: expected a refusal, got a result")
            continue
        if err:
            ok = False
            log.append(f"    FAIL: {short(err, 200)}")
            continue
        for path in step.get("expect", []):
            v = get_path(data, path)
            if v is MISSING or v is None:
                ok = False
                log.append(f"    FAIL: {path} missing")
            else:
                log.append(f"    {path} = {short(v)}")
    return ok, results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="run one flow by id")
    ap.add_argument("--json", help="write every raw result to this file")
    a = ap.parse_args()
    key = os.environ.get("PALANOR_API_KEY", "").strip()
    if not key:
        print("PALANOR_API_KEY is not set (a free key: https://palanor.com/developers/keys)")
        return 2
    flows = [f for f in load_flows() if not a.only or f["id"] == a.only]
    log: list[str] = [f"Palanor skill flows against {SERVER} at {time.strftime('%Y-%m-%d %H:%M:%S %Z')}"]
    raw: dict[str, Any] = {}
    failed = []
    for f in flows:
        ok, results = run_flow(key, f, log)
        raw[f["id"]] = results
        if not ok:
            failed.append(f["id"])
    log.append(f"\n{len(flows) - len(failed)} of {len(flows)} flows passed" + (f"; failed: {', '.join(failed)}" if failed else ""))
    print("\n".join(log))
    if a.json:
        Path(a.json).write_text(json.dumps(raw, indent=1, ensure_ascii=False), encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
