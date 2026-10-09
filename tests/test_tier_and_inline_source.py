"""One validated source is green, and Status Detail carries its own link (Baird 2026-10-08)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from build_review_package import inline_value, ref_col_for, validated_tier  # noqa: E402

URL = "https://psc.maryland.gov/order.pdf"
GOOD = [{"url": URL, "ok": True, "name_found": True, "contains_value": True}]


def test_status_detail_is_its_own_source_column():
    assert ref_col_for("Status Detail") == "Status Detail"
    assert ref_col_for("Status") == "Status Data Source"


def test_inline_value_appends_links_once():
    assert inline_value("Permit not yet filed.", [URL]) == f"Permit not yet filed: {URL}"
    assert inline_value(f"Permit not yet filed: {URL}", [URL]) == f"Permit not yet filed: {URL}"


def test_one_validated_source_is_high():
    assert validated_tier("Status Detail", "fill", "medium", [URL], GOOD) == "high"
    assert validated_tier("Capacity (MW)", "change", "medium", [URL], GOOD) == "high"


def test_status_change_is_never_raised():
    assert validated_tier("Status", "change", "medium", [URL], GOOD) == "medium"


def test_low_partial_and_caveated_stay():
    assert validated_tier("Start year", "fill", "low", [URL], GOOD) == "low"
    partial = [dict(GOOD[0], contains_value=False)]
    assert validated_tier("Start year", "fill", "medium", [URL], partial) == "medium"
    assert validated_tier("Start year", "fill", "medium", [URL], GOOD,
                          "The two sources differ on the year.") == "medium"
