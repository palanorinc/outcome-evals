"""Shared helpers for the Palanor skill tools: reading the source, the tool catalog, and the call syntax.

Standard library only, so the build and the checks run on a bare Python 3.10+.
"""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent  # skills/palanor
SOURCE = ROOT / "source"
DIST = ROOT / "dist"
LOCK = ROOT / "tools" / "tools.lock.json"
SERVER = "https://mcp.palanor.com"

# A call written in the skill: palanor_get_signal(slug="rates.spread_2y10y", history=true)
CALL_RE = re.compile(r"\b(palanor_[a-z0-9_]+)\(([^()]*)\)")
# Any tool name mentioned anywhere
NAME_RE = re.compile(r"\bpalanor_[a-z0-9_]+\b")
# key= inside a call's argument list (keys are bare identifiers)
ARG_RE = re.compile(r"(?:^|,)\s*([a-z_][a-z0-9_]*)\s*=")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_source() -> dict[str, Any]:
    src: dict[str, Any] = read_json(SOURCE / "skill.json")
    return src


def load_flows() -> list[dict[str, Any]]:
    flows: list[dict[str, Any]] = read_json(SOURCE / "flows.json")["flows"]
    return flows


def load_lock() -> dict[str, dict[str, Any]]:
    return {t["name"]: t for t in read_json(LOCK)["tools"]}


def fetch_live_tools(timeout: float = 30.0, attempts: int = 3) -> dict[str, dict[str, Any]]:
    """tools/list from the live server. Discovery is open: no key needed."""
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}).encode()
    last: Exception | None = None
    for _ in range(attempts):
        try:
            req = urllib.request.Request(
                SERVER,
                data=body,
                headers={"content-type": "application/json", "accept": "application/json, text/event-stream", "user-agent": "palanor-skill-check"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.load(r)
            return {t["name"]: t for t in data["result"]["tools"]}
        except Exception as e:  # network blips: retry, then fail loudly
            last = e
    raise RuntimeError(f"could not read tools/list from {SERVER}: {last}")


def schema_props(tool: dict[str, Any]) -> dict[str, Any]:
    props: dict[str, Any] = (tool.get("inputSchema") or {}).get("properties") or {}
    return props


def schema_required(tool: dict[str, Any]) -> list[str]:
    req: list[str] = (tool.get("inputSchema") or {}).get("required") or []
    return req


def split_top_level(arg_text: str) -> list[str]:
    """Split "a=1, b=[x, y], c={\"k\": 1}" on commas outside brackets and quotes."""
    out, depth, cur, quote = [], 0, [], ""
    for ch in arg_text:
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in "\"'":
            quote = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        elif ch == "," and depth == 0:
            out.append("".join(cur))
            cur = []
            continue
        cur.append(ch)
    if "".join(cur).strip():
        out.append("".join(cur))
    return out


def parse_call_args(arg_text: str) -> dict[str, str]:
    """Return {key: raw value text} for one written call. Raises ValueError on a malformed argument."""
    args: dict[str, str] = {}
    for part in split_top_level(arg_text):
        if "=" not in part:
            raise ValueError(f"argument without a name: {part.strip()!r}")
        k, v = part.split("=", 1)
        k = k.strip()
        if not re.fullmatch(r"[a-z_][a-z0-9_]*", k):
            raise ValueError(f"bad argument name {k!r}")
        args[k] = v.strip()
    return args
