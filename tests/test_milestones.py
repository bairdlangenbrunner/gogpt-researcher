"""Milestone timeline entries on staged statuses (Baird 2026-11-02)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT / "scripts", ROOT / "review_app", ROOT):
    sys.path.insert(0, str(p))

from state_gate import gate_milestones  # noqa: E402
from review_data import milestone_rows  # noqa: E402

URL = "https://example.org/permit.pdf"


def unit(**extra):
    u = {"unit_name": "Backup generators", "fields": {"Status": "construction"},
         "refs": {"Status Data Source": [URL]},
         "verifications": [{"url": URL, "ok": True, "contains_value": True}]}
    u.update(extra)
    return u


def lanes_with(u):
    return {"newplants": [{"record_id": "p", "fields": {}, "units": [u]}]}


def test_missing_milestone_flagged():
    out = gate_milestones(lanes_with(unit()))
    assert len(out) == 1 and "no milestone entry" in out[0][1]


def test_dated_milestone_passes():
    m = [{"status": "construction", "year": 2025, "period": "May", "sources": [URL]}]
    assert gate_milestones(lanes_with(unit(milestones=m))) == []


def test_bad_period_and_blank_period():
    bad = [{"status": "construction", "year": 2025, "period": "Spring", "sources": [URL]}]
    assert any("full month name" in r for _, r in gate_milestones(lanes_with(unit(milestones=bad))))
    blank = [{"status": "construction", "year": 2025, "period": "", "sources": [URL]}]
    assert any("period_note" in r for _, r in gate_milestones(lanes_with(unit(milestones=blank))))
    noted = [{"status": "construction", "year": 2025, "period": "", "sources": [URL],
              "period_note": "the permit and the news reports give only the year"}]
    assert gate_milestones(lanes_with(unit(milestones=noted))) == []


def test_card_rows():
    f, r = milestone_rows({"milestones": [{"status": "construction", "year": 2025,
                                           "period": "May", "sources": [URL]}]})
    assert f == {"Milestone: construction": "May 2025"}
    assert r == {"Milestone: construction Data Source": [URL]}
