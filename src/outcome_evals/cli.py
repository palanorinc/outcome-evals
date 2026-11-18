"""Command line: ``outcome-evals <command>``.

Using it:
  validate FILE...            check call files against the format
  score CALLS                 resolve and score your calls (shipped series, or --api)
  questions                   list the public questions (--split live|resolved_history)
  prompt ID                   print the prompt for one public question
  stats                       counts for the shipped data
  export-harbor OUT           write resolved questions as a Harbor dataset

Maintaining the public set (what the monthly job runs):
  refresh                     re-read every public series from Palanor's API
  resolve-live                record resolutions for live questions that are due
  publish-live                write a new live batch made today
  build-history               (re)generate the resolved-history set
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Sequence
from datetime import date, timedelta

from ._meta import NAME
from ._version import __version__
from .baselines import with_baselines
from .calls import CallFormatError, dump_calls, iter_calls, load_calls
from .data import LocalData, PalanorAPI, series_for
from .prompts import prompt
from .resolve import record, resolve, resolve_all
from .score import summarize
from .series import Series

HISTORY_START = "2005-01-01"


def _today(s: str | None) -> date:
    return date.fromisoformat(s) if s else date.today()


def cmd_validate(a: argparse.Namespace) -> int:
    bad = 0
    for f in a.files:
        n = 0
        try:
            for _ in iter_calls(f):
                n += 1
            print(f"{f}: {n} calls, valid")
        except CallFormatError as e:
            bad += 1
            print(f"{f}: {e}", file=sys.stderr)
    return 1 if bad else 0


def cmd_score(a: argparse.Namespace) -> int:
    calls = load_calls(*a.calls)
    api = PalanorAPI() if a.api else None
    local = LocalData(a.data) if a.data else None
    series = series_for(calls, local=local, api=api)
    if a.fill_baselines:
        calls = [with_baselines(c, series[c.series_id]) if c.anchor is None else c for c in calls]
    as_of = date.fromisoformat(a.as_of) if a.as_of else None
    calls = resolve_all(calls, series, as_of)
    if a.write_resolved:
        dump_calls(calls, a.write_resolved)
    s = summarize(calls)
    if a.json:
        print(json.dumps(s.to_dict(include_scores=a.per_call), indent=2, default=str))
    else:
        print(f"{NAME} {__version__}")
        print(s.text())
        if a.per_call:
            for c in calls:
                r = c.resolution
                st = r.status if r else "?"
                val = "" if not r or r.value is None else f" value={r.value:g}"
                oc = "" if not r or r.outcome is None else f" outcome={'yes' if r.outcome else 'no'}"
                fc = ""
                if c.forecast:
                    fc = f" forecast={c.forecast.probability if c.kind == 'binary' else c.forecast.value}"
                print(f"  {c.id}: {st}{val}{oc}{fc}" + (f" ({r.reason})" if r and r.reason else ""))
    return 0


def cmd_questions(a: argparse.Namespace) -> int:
    qs = LocalData(a.data).questions(a.split)
    for c in qs[: a.limit or None]:
        r = c.resolution
        tail = ""
        if r is not None:
            tail = f"  [{r.status}" + (f": {'yes' if r.outcome else 'no'}" if r.outcome is not None else (f": {r.value:g}" if r.value is not None else "")) + "]"
        print(f"{c.id}\n  {c.question}{tail}")
    return 0


def cmd_prompt(a: argparse.Namespace) -> int:
    d = LocalData(a.data)
    for c in d.questions("all"):
        if c.id == a.id:
            print(prompt(c.question_only(), d.all_series().get(c.series_id)))
            return 0
    print(f"no question {a.id}", file=sys.stderr)
    return 1


def stats(d: LocalData) -> dict[str, object]:
    hist = d.questions("resolved_history")
    live = d.questions("live")
    series = d.all_series()
    man = d.manifest()
    st = Counter((c.resolution.status if c.resolution else "pending") for c in live)
    return {
        "series": len(series),
        "sources": sorted({s.info.source for s in series.values() if s.info.source}),
        "readings": sum(len(s) for s in series.values()),
        "series_as_of": man.get("as_of"),
        "resolved_history": {"questions": len(hist), "by_kind": dict(Counter(c.kind for c in hist)),
                             "resolved": sum(1 for c in hist if c.resolution and c.resolution.resolved)},
        "live": {"questions": len(live), "batches": [p.stem for p in d.live_files()], "status": dict(st),
                 "by_kind": dict(Counter(c.kind for c in live))},
    }


def cmd_stats(a: argparse.Namespace) -> int:
    print(json.dumps(stats(LocalData(a.data)), indent=2))
    return 0


def cmd_export_harbor(a: argparse.Namespace) -> int:
    from .adapters.harbor import export_dataset

    d = LocalData(a.data)
    calls = load_calls(*a.calls) if a.calls else d.questions(a.split)
    if a.kinds:
        calls = [c for c in calls if c.kind in a.kinds.split(",")]
    if a.every and a.every > 1:
        calls = calls[:: a.every]
    if a.limit:
        calls = calls[: a.limit]
    series = series_for(calls, local=d)
    made = export_dataset(calls, series, a.out, name=a.name)
    print(f"wrote {len(made)} Harbor tasks to {a.out} ({len(calls) - len(made)} unresolved skipped)")
    return 0


# ---- maintaining the public set ------------------------------------------------


def _write_series(d: LocalData, series: dict[str, Series], as_of: date) -> None:
    from . import public_set

    d.series_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for spec in public_set.SPECS:
        s = series.get(spec.id)
        if s is None:
            continue
        info = public_set.info_for(spec, s.info)
        (d.series_dir / f"{spec.id}.csv").write_text(s.to_csv(), encoding="utf-8")
        e = info.to_dict()
        e["first"] = s.timestamps[0].isoformat() if len(s) else None
        e["last"] = s.timestamps[-1].isoformat() if len(s) else None
        e["n"] = len(s)
        entries.append(e)
    doc = {
        "as_of": as_of.isoformat(),
        "note": "Readings as served by Palanor's public API (latest vintage) on as_of. Each series keeps its source's licence; see DATA-LICENSES.md.",
        "series": entries,
    }
    (d.series_dir / "series.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_refresh(a: argparse.Namespace) -> int:
    from . import public_set

    d = LocalData(a.data)
    api = PalanorAPI()
    have = d.all_series() if d.series_dir.exists() else {}
    out: dict[str, Series] = {}
    skipped = []
    for spec in public_set.SPECS:
        prev = have.get(spec.id)
        start = HISTORY_START
        if prev is not None and len(prev) and not a.full:
            # re-read the last two years so revisions land; keep older readings as stored
            start = (date.today() - timedelta(days=730)).isoformat()
        fresh = api.series(spec.id, start=start, info=prev.info if prev else None)
        if fresh.info.extra.get("license_class") not in (None, "public_domain"):
            print(f"{spec.id}: licence class {fresh.info.extra.get('license_class')} is not public_domain", file=sys.stderr)
            skipped.append(spec.id)
            continue
        out[spec.id] = prev.merged(fresh) if (prev is not None and not a.full) else fresh
        print(f"{spec.id}: {len(out[spec.id])} readings, last {out[spec.id].timestamps[-1]}")
    if skipped:
        print(f"stopped: {len(skipped)} series no longer public_domain ({', '.join(skipped)}); nothing written", file=sys.stderr)
        return 1
    _write_series(d, out, date.today())
    print(f"{api.requests} API requests")
    return 0


def cmd_resolve_live(a: argparse.Namespace) -> int:
    d = LocalData(a.data)
    series = d.all_series()
    as_of = _today(a.as_of)
    stored = d.resolutions()
    calls = load_calls(*d.live_files()) if d.live_files() else []
    changed = 0
    rows = []
    for c in calls:
        prev = stored.get(c.id)
        s = series.get(c.series_id)
        if s is None:
            if prev:
                rows.append((c.id, prev))
            continue
        new = record(prev, resolve(c, s, as_of))
        if new.status == "pending":
            continue  # pending questions are not written down
        if prev is None or new.to_dict() != prev.to_dict():
            changed += 1
        rows.append((c.id, new))
    p = d.root / "resolutions.jsonl"
    p.write_text("".join(json.dumps({"id": i, "resolution": r.to_dict()}, separators=(",", ":")) + "\n" for i, r in sorted(rows)), encoding="utf-8")
    print(f"{len(rows)} live questions resolved or void ({changed} new or changed); {len(calls) - len(rows)} pending")
    return 0


def cmd_publish_live(a: argparse.Namespace) -> int:
    from .public_set import generate

    d = LocalData(a.data)
    made_on = _today(a.made_on)
    path = d.root / "questions" / "live" / f"{made_on.isoformat()}.jsonl"
    if path.exists() and not a.force:
        print(f"{path} exists; a batch is published once (pass --force to rewrite it)")
        return 0
    series = d.all_series()
    calls = generate(series, made_on, "live", live_cutoff=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    dump_calls(calls, path)
    print(f"wrote {len(calls)} live questions to {path}")
    return 0


def cmd_build_history(a: argparse.Namespace) -> int:
    from .public_set import generate

    d = LocalData(a.data)
    series = d.all_series()
    as_of = _today(a.as_of)
    start, end = date.fromisoformat(a.start), date.fromisoformat(a.end)
    dates = []
    t = start
    while t <= end:
        dates.append(t)
        m = t.month - 1 + a.every_months
        t = date(t.year + m // 12, m % 12 + 1, t.day)
    out = []
    for made_on in dates:
        qs = generate(series, made_on, "resolved_history")
        for c in resolve_all(qs, series, as_of):
            if c.resolution is not None and c.resolution.resolved:
                out.append(c)
    p = d.root / "questions" / "resolved_history.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    dump_calls(out, p)
    print(f"wrote {len(out)} resolved questions made on {len(dates)} dates to {p}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="outcome-evals", description=f"{NAME}: score dated calls against what happened.")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    ap.add_argument("--data", help="data directory (default: the files shipped with the package)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("validate", help="check call files")
    p.add_argument("files", nargs="+")
    p.set_defaults(fn=cmd_validate)

    p = sub.add_parser("score", help="resolve and score calls")
    p.add_argument("calls", nargs="+")
    p.add_argument("--api", action="store_true", help="read series from Palanor's API (PALANOR_API_KEY)")
    p.add_argument("--as-of", help="resolve as of this date (default: the series copy's date)")
    p.add_argument("--fill-baselines", action="store_true", help="compute anchor, base rate and scale for calls that lack them")
    p.add_argument("--write-resolved", help="also write the calls with their resolutions to this .jsonl")
    p.add_argument("--per-call", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_score)

    p = sub.add_parser("questions", help="list public questions")
    p.add_argument("--split", default="live", choices=["live", "resolved_history", "all"])
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(fn=cmd_questions)

    p = sub.add_parser("prompt", help="print one question's prompt")
    p.add_argument("id")
    p.set_defaults(fn=cmd_prompt)

    p = sub.add_parser("stats", help="counts for the shipped data")
    p.set_defaults(fn=cmd_stats)

    p = sub.add_parser("export-harbor", help="write resolved questions as a Harbor dataset")
    p.add_argument("out")
    p.add_argument("--calls", nargs="*", help="your own call files instead of the public set")
    p.add_argument("--split", default="resolved_history", choices=["resolved_history", "live", "all"])
    p.add_argument("--kinds", help="e.g. binary or binary,number")
    p.add_argument("--every", type=int, default=1, help="take every Nth question")
    p.add_argument("--limit", type=int)
    p.add_argument("--name", default="outcome-evals")
    p.set_defaults(fn=cmd_export_harbor)

    p = sub.add_parser("refresh", help="re-read the public series from Palanor's API")
    p.add_argument("--full", action="store_true", help=f"re-read everything since {HISTORY_START}")
    p.set_defaults(fn=cmd_refresh)

    p = sub.add_parser("resolve-live", help="record resolutions for due live questions")
    p.add_argument("--as-of")
    p.set_defaults(fn=cmd_resolve_live)

    p = sub.add_parser("publish-live", help="write a live batch made today")
    p.add_argument("--made-on")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_publish_live)

    p = sub.add_parser("build-history", help="(re)generate the resolved-history set")
    p.add_argument("--start", default="2024-01-15")
    p.add_argument("--end", default="2026-07-15")
    p.add_argument("--every-months", type=int, default=3)
    p.add_argument("--as-of")
    p.set_defaults(fn=cmd_build_history)

    a = ap.parse_args(argv)
    return int(a.fn(a) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
