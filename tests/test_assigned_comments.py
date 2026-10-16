"""assigned_comments.py: the memo lists open threads first, names people by
name only, and maps a unit element to its G... ID."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from assigned_comments import ELEMENT_UNIT, memo  # noqa: E402

SCOPE = {"kind": "state", "name": "Iowa", "slug": "iowa", "country": "United States"}


def thread(open_, **kw):
    t = {"thread_id": 1, "open": open_, "plant_id": "L1", "plant_name": "Test Plant",
         "unit_id": "G2", "box": "status_id", "assignee": "A Person",
         "created": "2026-02-17", "modified": None,
         "comments": [{"created": "2026-02-17", "by": "B Person", "text": "see\nlink"}]}
    t.update(kw)
    return t


def test_unit_element_maps_to_unit_id():
    m = ELEMENT_UNIT.match("units-100001071244-status_id")
    assert m.group(1) == "100001071244" and m.group(2) == "status_id"
    assert ELEMENT_UNIT.match("name") is None


def test_memo_lists_open_first_and_flattens_text():
    text = memo(SCOPE, [thread(False, thread_id=2, plant_name="Closed Plant"),
                        thread(True)], "2026-10-16T16:00-04:00")
    assert "- Open threads: 1" in text and "- Completed threads: 1" in text
    assert text.index("Test Plant") < text.index("Closed Plant")
    assert "B Person: see link" in text
    assert "@" not in text


def test_memo_with_no_threads():
    text = memo(SCOPE, [], "2026-10-16T16:00-04:00")
    assert text.count("None.") == 2
