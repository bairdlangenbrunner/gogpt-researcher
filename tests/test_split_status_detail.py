"""A Status Detail edit that dates status steps splits into a minor text record and a
major status-timeline record (Baird 2026-11-06, Cooper Unit 3)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT)]

from assemble_state import split_status_detail  # noqa: E402

SRC = "https://example.gov/permit.pdf"


def rec(**kw):
    base = {"record_id": "L1:G1:status-detail", "gem_unit_id": "G1", "gem_plant_id": "L1",
            "verdict": "change", "fields": {"Status Detail": "new\n\nold"}, "current": {"Status Detail": "old"},
            "refs": {}, "verifications": [{"url": SRC, "ok": True}], "tier": "high", "independent": True,
            "checks": [7, 10], "researcher_notes": "text note", "action": "add at the top",
            "milestones": [{"status": "pre-construction", "year": 2025, "period": "January",
                            "sources": [SRC], "note": "Application received January 27, 2025."}]}
    base.update(kw)
    return base


def test_split_moves_milestones_and_check_7():
    detail, timeline = split_status_detail(rec())
    assert detail["record_id"] == "L1:G1:status-detail"
    assert "milestones" not in detail and detail["checks"] == [10]
    assert detail["fields"] == {"Status Detail": "new\n\nold"}
    assert timeline["record_id"] == "L1:G1:status-timeline"
    assert timeline["fields"] == {} and timeline["milestones"][0]["year"] == 2025
    assert 7 in timeline["checks"]
    assert SRC in timeline["researcher_notes"]
    assert timeline["independent"] is False      # one publisher


def test_other_records_unchanged():
    r = rec(fields={"Status": "construction"})
    assert split_status_detail(r) == [r]
    r = rec(milestones=[])
    assert split_status_detail(r) == [r]
