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


def test_inline_value_lists_links_under_the_text_once():
    # the text, a blank line, then one link per line (Baird 2026-10-09)
    URL2 = "https://psc.maryland.gov/order2.pdf"
    block = f"Permit not yet filed.\n\n{URL}\n{URL2}"
    assert inline_value("Permit not yet filed.", [URL, URL2]) == block
    # the older "text: link" form, and a link the agent already wrote in
    assert inline_value(f"Permit not yet filed: {URL}: {URL2}", [URL, URL2]) == block
    assert inline_value(f"Permit not yet filed: {URL}", [URL2]) == block
    assert inline_value(block, [URL, URL2]) == block


def test_additive_value_leaves_a_blank_line_under_the_links():
    from build_review_package import additive_value
    new = inline_value("Permit filed.", [URL])
    assert additive_value(new, "NF 6/7/24: old note") == f"{new}\n\nNF 6/7/24: old note"


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
