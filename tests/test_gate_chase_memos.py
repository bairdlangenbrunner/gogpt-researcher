"""The chase gate on audit memos (2026-10-30): a memo that hands a record set to
"a person" or says a register was not read is a search the batch still owes."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import state_gate as g  # noqa: E402

MEMO = """# Permit sweep

Construction permits are not on the notice feed. A person could request these from the agency.
The Document Explorer was not used as a source.
Grid Status was not checked.
The original pass did not check the docket; this memo closes that gap.
Emergency-only generator sets are out of scope for this sweep.
The register was searched by name for every plant on 2026-10-30; none found for Nelson.
See https://example.org/records?available-on-request=1 for the list.
The Illinois EPA record system has no public copy of the 2019 file.
"""


def test_memo_giveup_hits_flag_the_give_ups_and_leave_the_rest(tmp_path):
    memo = tmp_path / "permit_sweep.md"
    memo.write_text(MEMO, encoding="utf-8")
    hits = g.memo_giveup_hits(memo)
    assert hits == [(3, "a person could request"), (4, "not used as a source"), (5, "was not checked"),
                    (10, "has no public copy")]


def test_memo_giveup_hits_on_a_missing_file_is_empty(tmp_path):
    assert g.memo_giveup_hits(tmp_path / "nope.md") == []


def test_gate_chase_memos_names_the_memo_line(tmp_path):
    batch = tmp_path / "us-xx"
    (batch / "audit").mkdir(parents=True)
    (batch / "audit" / "a.md").write_text("A person could request these.\n", encoding="utf-8")
    (batch / "audit" / "b.md").write_text("Every record was read; none found.\n", encoding="utf-8")
    out = g.gate_chase_memos(batch)
    assert [o[0] for o in out] == ["audit/a.md:1"]
    assert "a person could request" in out[0][1] and "harvest_permits.py" in out[0][1]


def test_gate_chase_memos_without_an_audit_folder_passes(tmp_path):
    assert g.gate_chase_memos(tmp_path) == []
