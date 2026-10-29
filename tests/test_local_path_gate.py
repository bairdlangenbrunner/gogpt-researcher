"""A note that points to a file on the researcher's computer is no source for the
reviewer (Baird 2026-10-27): state_gate's notes gate flags a repo path, a home path
or a saved spreadsheet named in any person-facing text."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from state_gate import gate_notes, local_paths  # noqa: E402


def test_local_paths_are_found_and_web_addresses_are_not():
    assert local_paths("saved as work/pjm/pjm_cycle_queue_2026-10-21.xlsx. That export") == ["work/pjm/pjm_cycle_queue_2026-10-21.xlsx"]
    assert local_paths("the file /Users/someone/queue.csv") == ["/Users/someone/queue.csv"]
    assert local_paths("I read pjm_cycle_queue.xlsx") == ["pjm_cycle_queue.xlsx"]
    assert local_paths("PJM's list at https://www.pjm.com/pub/planning/downloads/xml/PlanningQueues.xml names it") == []
    assert local_paths("the export at https://example.org/queue.xlsx") == []
    assert local_paths("work in progress at the site") == []


def test_the_notes_gate_flags_a_monitor_reason_and_a_proposed_source():
    rec = {"record_id": "us-il:plant:monitor-8", "monitor_reason": "I read this in work/pjm/pjm_cycle_queue_2026-10-21.xlsx.",
           "proposed_add": {"source_if_accepted": "pjm_cycle_queue_2026-10-21.xlsx"}}
    out = [reason for _, reason in gate_notes({"monitor": [rec]})]
    assert any(r.startswith("monitor_reason names a file on this computer") for r in out)
    assert any(r.startswith("proposed_add.source_if_accepted names a file") for r in out)


def test_a_note_with_steps_passes():
    rec = {"record_id": "us-il:plant:monitor-8",
           "monitor_reason": "On PJM's cycle request status page at https://www.pjm.com/planning/m/cycle-service-request-status, click XLS under full export and find row C01-2036."}
    assert [r for _, r in gate_notes({"monitor": [rec]}) if "this computer" in r] == []
