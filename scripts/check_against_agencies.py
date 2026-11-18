"""Check resolved questions against each agency's own published figures.

For each chosen question, fetch the reading(s) the resolver used straight from
the publishing agency (BLS API, Treasury's par yield CSV, DOL's weekly claims
report, EIA's weekly gasoline table), recompute the question's value and
outcome from those figures, and compare with the stored resolution.

    python scripts/check_against_agencies.py [--n 20] [--seed 18]

Standard library only. Prints a table and exits 1 on any mismatch.
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import random
import re
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime

from outcome_evals import Call, LocalData
from outcome_evals.resolve import apply_transform
from outcome_evals.series import Series, SeriesInfo

UA = {"User-Agent": "Mozilla/5.0 (compatible; outcome-evals agency check)"}

BLS = {
    "fred_cpi": "CUSR0000SA0",
    "fred_core_cpi": "CUSR0000SA0L1E",
    "fred_unemployment": "LNS14000000",
    "fred_u6_underemployment": "LNS13327709",
    "fred_lfpr": "LNS11300000",
    "fred_nfp": "CES0000000001",
    "avg-hrly-earn": "CES0500000003",
    "fred_jolts": "JTS000000000000000JOL",
}
TREASURY = {"rates.ust.par.10y": "10 Yr", "rates.ust.par.2y": "2 Yr", "rates.ust.par.3m": "3 Mo"}
SPREADS = {"rates.spread_2y10y": ("10 Yr", "2 Yr"), "rates.spread_3m10y": ("10 Yr", "3 Mo")}
PLAN = [*BLS, *TREASURY, *SPREADS, "fred_jobless", "fred_jobless", "continued-claims", "continued-claims",
        "fred_gas_price_regular", "fred_gas_price_regular", "fred_gas_price_regular"]


def get(url: str, data: bytes | None = None, headers: dict[str, str] | None = None) -> str:
    req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=60) as r:  # noqa: S310
        return r.read().decode("utf-8", "replace")


def bls(series_ids: list[str], start: int, end: int) -> dict[str, dict[date, float]]:
    body = json.dumps({"seriesid": series_ids, "startyear": str(start), "endyear": str(end)}).encode()
    d = json.loads(get("https://api.bls.gov/publicAPI/v1/timeseries/data/", body, {"Content-Type": "application/json"}))
    if d.get("status") != "REQUEST_SUCCEEDED":
        raise RuntimeError(f"BLS: {d.get('status')} {d.get('message')}")
    out: dict[str, dict[date, float]] = {}
    for s in d["Results"]["series"]:
        m = {}
        for row in s["data"]:
            if row["period"].startswith("M") and row["period"] != "M13" and row["value"] not in ("-", ""):
                m[date(int(row["year"]), int(row["period"][1:]), 1)] = float(row["value"])
        out[s["seriesID"]] = m
    return out


def treasury(years: set[int]) -> dict[date, dict[str, float]]:
    out: dict[date, dict[str, float]] = {}
    for y in sorted(years):
        url = (f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{y}/all"
               f"?type=daily_treasury_yield_curve&field_tdr_date_value={y}&page&_format=csv")
        for row in csv.DictReader(io.StringIO(get(url))):
            out[datetime.strptime(row["Date"], "%m/%d/%Y").date()] = {k: float(v) for k, v in row.items() if k != "Date" and v}
    return out


def dol(start: int, end: int) -> dict[date, tuple[float, float]]:
    """Week-ending date → (initial claims SA, continued claims SA) from report r539cy."""
    page = get("https://oui.doleta.gov/unemploy/wkclaims/report.asp", urllib.parse.urlencode(
        {"level": "US", "strtdate": start, "enddate": end, "filetype": "html", "final_yr": end}).encode())
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", page)))
    out = {}
    for m in re.finditer(r"(\d{2}/\d{2}/\d{4}) ([\d,]+) ([\d.]+) ([\d,]+) ([\d,]+) ([\d,]+) ([\d.]+) ([\d,]+) ", text):
        d = datetime.strptime(m.group(1), "%m/%d/%Y").date()
        out[d] = (float(m.group(4).replace(",", "")), float(m.group(8).replace(",", "")))
    return out


def eia() -> dict[date, float]:
    """Week (Monday) → U.S. regular gasoline retail price, from EIA's weekly history table."""
    page = get("https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=EMM_EPMR_PTE_NUS_DPG&f=W").replace("&nbsp;", " ")
    out: dict[date, float] = {}
    for row in re.findall(r"<tr>(.*?)</tr>", page, re.S):
        m = re.search(r"(\d{4})-([A-Za-z]{3})", row)
        if not m:
            continue
        year = int(m.group(1))
        cells = re.findall(r"<td class='B5'>\s*(\d{2}/\d{2})\s*</td>\s*<td class='B3'>\s*([\d.]+)\s*</td>", row)
        for md, v in cells:
            mm, dd = md.split("/")
            out[date(year, int(mm), int(dd))] = float(v)
    return out


def pick(calls: list[Call], n: int, seed: int) -> list[Call]:
    rnd = random.Random(seed)
    by: dict[str, list[Call]] = defaultdict(list)
    for c in calls:
        if c.kind == "binary":
            by[c.series_id].append(c)
    chosen: list[Call] = []
    for sid in PLAN[:n]:
        pool = [c for c in by[sid] if c not in chosen]
        chosen.append(rnd.choice(pool))
    return chosen


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=18)
    a = ap.parse_args()
    data = LocalData()
    chosen = pick(data.questions("resolved_history"), a.n, a.seed)
    years = {c.resolution.reading_timestamp.year for c in chosen if c.resolution and c.resolution.reading_timestamp}
    lo, hi = min(years) - 1, max(years)
    b = bls(list(BLS.values()), lo, hi)
    t = treasury({y for y in range(lo, hi + 1)})
    w = dol(lo, hi)
    g = eia()
    bad = 0
    print(f"{'question':<52} {'reading':<11} {'stored':>12} {'agency':>12} {'value':>10} {'agency value':>13} outcome  ok")
    for c in chosen:
        r = c.resolution
        assert r is not None and r.reading_timestamp is not None
        ts = r.reading_timestamp
        sid = c.series_id
        if sid in BLS:
            src = b[BLS[sid]]
        elif sid in TREASURY:
            src = {d: v[TREASURY[sid]] for d, v in t.items() if TREASURY[sid] in v}
        elif sid in SPREADS:
            x, y = SPREADS[sid]
            src = {d: round(v[x] - v[y], 2) for d, v in t.items() if x in v and y in v}
        elif sid == "fred_jobless":
            src = {d: v[0] for d, v in w.items()}
        elif sid == "continued-claims":
            src = {d: v[1] for d, v in w.items()}
        else:
            src = g
        agency_reading = src.get(ts)
        # recompute the value in the question's terms from agency figures only
        agency_series = Series.from_pairs(SeriesInfo(id=sid), sorted(src.items()))
        tv = apply_transform(agency_series, ts, agency_reading, c.rule.transform) if agency_reading is not None else None
        agency_value = None if tv is None else round(tv[0], 9)
        agency_outcome = None if agency_value is None else c.rule.holds(agency_value)
        ok = (
            agency_reading is not None
            and abs(agency_reading - (r.reading_value or 0)) < 1e-6
            and agency_value is not None
            and abs(agency_value - (r.value or 0)) < 1e-6
            and agency_outcome == r.outcome
        )
        bad += not ok
        print(f"{c.id:<52} {ts.isoformat():<11} {r.reading_value:>12g} {agency_reading if agency_reading is not None else 'missing':>12} "
              f"{r.value:>10.4g} {agency_value if agency_value is not None else 'n/a':>13.6} {'yes' if r.outcome else 'no':<8} {'✓' if ok else '✗'}")
    print(f"\n{len(chosen) - bad} of {len(chosen)} match the agency's published figures")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
