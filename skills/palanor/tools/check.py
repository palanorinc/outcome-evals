#!/usr/bin/env python3
"""Checks for the Palanor skill. Exit 1 on any failure.

    python skills/palanor/tools/check.py            # drift + names/arguments against the live server
    python skills/palanor/tools/check.py --offline  # same, against tools/tools.lock.json (no network)

1. Drift: dist/ is exactly what build.py generates from source/.
2. Tool names and arguments: every tool the skill names or calls, in every variant and in flows.json, exists in
   the server's tools/list (which is listMcpTools() in Palanor's code); every argument a call passes is in that
   tool's input schema; required arguments are present; literal enum values are allowed.
3. Lock: the tools the skill teaches have the same arguments live as in tools.lock.json (else refresh the lock and
   rebuild, so references/tools.md stays true).
4. Spec limits (agentskills.io): name, description, compatibility lengths; SKILL.md body under 500 lines.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skilllib import (  # noqa: E402
    CALL_RE,
    DIST,
    NAME_RE,
    fetch_live_tools,
    load_flows,
    load_lock,
    load_source,
    parse_call_args,
    schema_props,
    schema_required,
)

# Prefixes harnesses put in front of MCP tool names; the skill may mention them in setup notes.
HARNESS_PREFIXES = ("mcp__palanor__", "palanor__", "palanor.")
# palanor_* words that are not tools (licence classes, index slug prefix)
NOT_TOOLS = {"palanor_derived", "palanor_refined", "palanor_licensed_closes"}
# A tool name the skill presents as a tool: in backticks, or followed by "(".
MENTION_RE = re.compile(r"`((?:mcp__palanor__|palanor__)?palanor_[a-z0-9_]+)(?:\(|`)")
NAME_OK = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def strip_prefix(name: str) -> str:
    for p in HARNESS_PREFIXES:
        if name.startswith(p) and name[len(p):].startswith("palanor_"):
            return name[len(p):]
    return name


def check_value(tool: str, arg: str, raw: str, spec: dict[str, Any], where: str, errors: list[str]) -> None:
    try:
        val = json.loads(raw)
    except json.JSONDecodeError:
        if raw in ("true", "false"):
            return
        if raw.startswith('"<') or raw.startswith("<"):
            return  # a placeholder such as "<job id>"
        errors.append(f"{where}: {tool}({arg}=...) value is not JSON: {raw}")
        return
    check_json_value(tool, arg, val, spec, where, errors)


def check_json_value(tool: str, arg: str, val: Any, spec: dict[str, Any], where: str, errors: list[str]) -> None:
    if isinstance(val, str) and val.startswith("<") and val.endswith(">"):
        return
    if isinstance(val, str) and val.startswith("$"):
        return  # a reference to an earlier step
    if "enum" in spec and val not in spec["enum"]:
        errors.append(f"{where}: {tool}({arg}={val!r}) not one of {spec['enum']}")
    typ = spec.get("type")
    types: dict[str, type | tuple[type, ...]] = {"string": str, "number": (int, float), "integer": int, "boolean": bool, "array": list, "object": dict}
    py = types.get(typ or "")
    if py and not isinstance(val, py):
        errors.append(f"{where}: {tool}({arg}=...) should be {typ}, got {type(val).__name__}")
    if typ == "array" and isinstance(val, list) and isinstance(spec.get("items"), dict):
        items = spec["items"]
        for item in val:
            if items.get("type") == "object" and isinstance(item, dict):
                sub = items.get("properties") or {}
                for k, v in item.items():
                    if k not in sub:
                        errors.append(f"{where}: {tool}({arg}=[{{{k}: ...}}]) {k!r} is not an item field (has {sorted(sub)})")
                    else:
                        check_json_value(tool, f"{arg}[].{k}", v, sub[k], where, errors)
                for k in items.get("required") or []:
                    if k not in item:
                        errors.append(f"{where}: {tool}({arg}=[...]) item is missing required {k!r}")


def check_call(tool: str, args: dict[str, Any], raw_args: bool, tools: dict[str, dict[str, Any]], where: str, errors: list[str]) -> None:
    if tool not in tools:
        errors.append(f"{where}: {tool} is not a tool on the server")
        return
    props, req = schema_props(tools[tool]), schema_required(tools[tool])
    for arg, val in args.items():
        if arg not in props:
            errors.append(f"{where}: {tool} has no argument {arg!r} (has {sorted(props)})")
            continue
        if raw_args:
            check_value(tool, arg, val, props[arg], where, errors)
        else:
            check_json_value(tool, arg, val, props[arg], where, errors)
    for r in req:
        if r not in args:
            errors.append(f"{where}: {tool} call is missing required argument {r!r}")


def scan_markdown(path: Path, tools: dict[str, dict[str, Any]], errors: list[str]) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    where = str(path.relative_to(DIST.parent))
    n_calls = n_names = 0
    # tools.md headings name tools; descriptions there come from the server itself
    if path.name == "tools.md":
        for m in re.finditer(r"^## (palanor_[a-z0-9_]+)$", text, re.M):
            n_names += 1
            if m.group(1) not in tools:
                errors.append(f"{where}: heading {m.group(1)} is not a tool on the server")
        for m in re.finditer(r"^- `(palanor_[a-z0-9_]+)`", text, re.M):
            n_names += 1
            if m.group(1) not in tools:
                errors.append(f"{where}: {m.group(1)} is not a tool on the server")
        return n_calls, n_names
    for m in CALL_RE.finditer(text):
        name = strip_prefix(m.group(1))
        if name in NOT_TOOLS:
            continue
        n_calls += 1
        try:
            args = parse_call_args(m.group(2))
        except ValueError as e:
            errors.append(f"{where}: {m.group(0)}: {e}")
            continue
        check_call(name, args, True, tools, where, errors)
    if path.suffix == ".yaml":  # recipes name tools in plain prose
        for m in NAME_RE.finditer(text):
            name = strip_prefix(m.group(0))
            if name in NOT_TOOLS or name.endswith("_") or name == "palanor_api_key":
                continue
            n_names += 1
            if name not in tools:
                errors.append(f"{where}: {m.group(0)} is not a tool on the server")
    for m in MENTION_RE.finditer(text):
        name = strip_prefix(m.group(1))
        if name in NOT_TOOLS or name.endswith("_"):
            continue
        n_names += 1
        if name not in tools:
            errors.append(f"{where}: `{m.group(1)}` is not a tool on the server")
    return n_calls, n_names


def check_spec(src: dict[str, Any], errors: list[str]) -> None:
    name = src["name"]
    if not (1 <= len(name) <= 64 and NAME_OK.match(name)):
        errors.append(f"skill name {name!r} breaks the spec (a-z, 0-9, single hyphens, 1-64 chars)")
    if not (1 <= len(src["description"]) <= 1024):
        errors.append(f"description is {len(src['description'])} chars (1-1024)")
    if not (1 <= len(src["compatibility"]) <= 500):
        errors.append(f"compatibility is {len(src['compatibility'])} chars (1-500)")
    for skill_md in DIST.glob("*/" + name + "/SKILL.md"):
        lines = skill_md.read_text(encoding="utf-8").count("\n")
        if lines >= 500:
            errors.append(f"{skill_md.relative_to(DIST.parent)} has {lines} lines (keep under 500)")
        if skill_md.parent.name != name:
            errors.append(f"{skill_md} folder must be named {name}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="check against tools.lock.json instead of the live server")
    a = ap.parse_args()
    errors: list[str] = []

    # 1. drift
    build = Path(__file__).resolve().parent / "build.py"
    r = subprocess.run([sys.executable, str(build), "--check"], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        errors.append("drift check failed (see above)")

    # 2. names and arguments
    lock = load_lock()
    tools = lock if a.offline else fetch_live_tools()
    print(f"tool catalog: {len(tools)} tools ({'tools.lock.json' if a.offline else 'live tools/list'})")
    src = load_source()
    n_calls = n_names = 0
    for md in sorted([*DIST.rglob("*.md"), *DIST.rglob("*.yaml")]):
        c, n = scan_markdown(md, tools, errors)
        n_calls += c
        n_names += n
    for f in load_flows():
        for i, s in enumerate(f["steps"]):
            n_calls += 1
            check_call(s["call"], s["args"], False, tools, f"flows.json {f['id']} step {i + 1}", errors)
    for t in src["tools_taught"]:
        if t not in tools:
            errors.append(f"skill.json tools_taught: {t} is not a tool on the server")
    print(f"names/arguments: {n_calls} calls and {n_names} tool mentions checked across {len(list(DIST.rglob('*.md')))} files and flows.json")

    # 3. lock vs live (taught tools must match exactly; other tools only warn)
    if not a.offline:
        for t in src["tools_taught"]:
            if t in tools and t in lock and tools[t].get("inputSchema") != lock[t].get("inputSchema"):
                errors.append(f"{t}: arguments changed on the server; run tools/refresh_lock.py then build.py")
        added = sorted(set(tools) - set(lock))
        removed = sorted(set(lock) - set(tools))
        if added or removed:
            print(f"warning: server tools changed since the lock (added {added or 'none'}, removed {removed or 'none'}); "
                  "refresh the lock so references/tools.md lists them")
        for t in removed:
            errors.append(f"{t} is listed in references/tools.md but no longer on the server; refresh the lock")

    # 4. spec limits
    check_spec(src, errors)

    if errors:
        print("\nFAILED:")
        print("\n".join(f"  - {e}" for e in errors))
        return 1
    print("all skill checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
