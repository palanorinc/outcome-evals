import pytest

from outcome_evals import LocalData, parse_answer, prompt


@pytest.mark.parametrize(
    "text, p",
    [
        ("blah\nPROBABILITY: 0.62", 0.62),
        ("probability = .3", 0.3),
        ("PROBABILITY: 0.2\nOn reflection.\nPROBABILITY: 0.4", 0.4),
        ("PROBABILITY: 70%", 0.7),
        ("PROBABILITY: 1", 1.0),
        ("PROBABILITY: 7", None),
        ("I think 60%", None),
    ],
)
def test_parse_probability(text, p):
    f = parse_answer(text, "binary")
    assert (f.probability if f else None) == p


@pytest.mark.parametrize("text, v", [("VALUE: 4.25", 4.25), ("value: 215,000", 215000.0), ("VALUE: $3.10", 3.1), ("VALUE: -0.4", -0.4), ("no", None)])
def test_parse_value(text, v):
    f = parse_answer(text, "number")
    assert (f.value if f else None) == v


def test_prompt_shows_only_readings_up_to_cutoff():
    d = LocalData()
    c = next(q for q in d.questions("resolved_history") if q.series_id == "fred_cpi")
    s = d.series("fred_cpi")
    text = prompt(c.question_only(), s)
    later = [t.isoformat() for t in s.timestamps if c.cutoff is not None and t > c.cutoff]
    assert later and not any(t in text for t in later)
    assert c.cutoff is not None and c.cutoff.isoformat() in text
    assert "PROBABILITY:" in text
    assert c.resolution is not None and f"{c.resolution.value}" not in text
