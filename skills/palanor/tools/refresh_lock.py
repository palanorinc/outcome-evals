#!/usr/bin/env python3
"""Refresh tools/tools.lock.json from the live server's tools/list, then run build.py.

    python skills/palanor/tools/refresh_lock.py
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skilllib import LOCK, SERVER, fetch_live_tools  # noqa: E402


def main() -> int:
    tools = fetch_live_tools()
    lock = {
        "server": SERVER,
        "captured": dt.date.today().isoformat(),
        "tools": [{"name": t["name"], "description": t["description"], "inputSchema": t.get("inputSchema")} for t in tools.values()],
    }
    LOCK.write_text(json.dumps(lock, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {LOCK.name}: {len(tools)} tools")
    return subprocess.call([sys.executable, str(Path(__file__).resolve().parent / "build.py")])


if __name__ == "__main__":
    sys.exit(main())
