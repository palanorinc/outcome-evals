import json
from datetime import date
from importlib import resources

import pytest

from outcome_evals import Call, CallFormatError, Forecast, validate_dict
from outcome_evals.calls import dump_calls, load_calls

GOOD = {
    "id": "acme-001",
    "question": "Will U.S. initial claims for the week ending on or before 2027-01-15 be above 230,000?",
    "kind": "binary",
    "made_on": "2026-12-01",
    "deadline": "2027-01-15",
    "series_id": "fred_jobless",
    "rule": {"comparator": ">", "threshold": 230000, "period": "W"},
    "source": "U.S. Department of Labor",
    "license": "Public domain (U.S. Government work)",
    "forecast": {"probability": 0.35, "forecaster": "planning team"},
}


def schema():
    return json.loads((resources.files("outcome_evals") / "schema" / "call.schema.json").read_text())


def test_round_trip():
    c = Call.from_dict(GOOD)
    assert Call.from_dict(c.to_dict()) == c
    assert c.horizon_days == 45
    assert c.forecast == Forecast(probability=0.35, forecaster="planning team")


@pytest.mark.parametrize(
    "patch, msg",
    [
        ({"kind": "maybe"}, "kind"),
        ({"deadline": "2026-11-01"}, "before made_on"),
        ({"cutoff": "2026-12-02"}, "look-ahead"),
        ({"rule": {"comparator": ">"}}, "threshold"),
        ({"rule": {"comparator": "between", "low": 2, "high": 1}}, "low must be below high"),
        ({"forecast": {"probability": 1.2}}, "between 0 and 1"),
        ({"forecast": {"value": 3}}, "needs a probability"),
        ({"surprise": 1}, "unknown field"),
        ({"made_on": "12/01/2026"}, "ISO date"),
        ({"rule": {"comparator": ">", "threshold": 1, "transform": {"kind": "pct_change"}}}, "lag is required"),
        ({"rule": {"comparator": ">", "threshold": 1, "transform": {"kind": "pct_change", "lag": "12X"}}}, "lag"),
    ],
)
def test_rejects(patch, msg):
    d = {**GOOD, **patch}
    errs = validate_dict(d)
    assert errs and msg in errs[0]


def test_number_kind_takes_no_comparator():
    d = {**GOOD, "kind": "number", "forecast": {"value": 225000}}
    assert validate_dict(d)
    d["rule"] = {"period": "W"}
    assert not validate_dict(d)


def test_json_schema_agrees():
    jsonschema = pytest.importorskip("jsonschema")
    sch = schema()
    jsonschema.Draft202012Validator.check_schema(sch)
    v = jsonschema.Draft202012Validator(sch)
    assert not list(v.iter_errors(GOOD))
    assert list(v.iter_errors({**GOOD, "kind": "maybe"}))
    assert list(v.iter_errors({**GOOD, "rule": {"comparator": "between", "low": 1}}))
    assert list(v.iter_errors({**GOOD, "forecast": {"value": 3}}))


def test_every_shipped_record_matches_the_schema():
    jsonschema = pytest.importorskip("jsonschema")
    from outcome_evals import LocalData

    v = jsonschema.Draft202012Validator(schema())
    d = LocalData()
    calls = d.questions("all")
    assert calls
    for c in calls:
        errs = list(v.iter_errors(c.to_dict()))
        assert not errs, (c.id, errs[0].message)


def test_jsonl_and_json_files(tmp_path):
    c = Call.from_dict(GOOD)
    p = tmp_path / "calls.jsonl"
    dump_calls([c, Call.from_dict({**GOOD, "id": "acme-002"})], p)
    assert [x.id for x in load_calls(p)] == ["acme-001", "acme-002"]
    j = tmp_path / "calls.json"
    j.write_text(json.dumps({"calls": [GOOD]}))
    assert load_calls(j)[0].made_on == date(2026, 12, 1)
    with pytest.raises(CallFormatError, match="duplicate"):
        load_calls(p, p)
