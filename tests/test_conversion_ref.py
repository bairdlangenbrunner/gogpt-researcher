"""The conversion detail columns share the Conversion/replacement Data Source box
(Oklahoma, Grand River unit 3, 2026-11-06: the validation report asks which unit a
replacement came from, and the gate called the answer an orphan)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_review_package as brp  # noqa: E402


def test_conversion_detail_columns_pair_with_conversion_box():
    for col in brp.CONVERSION_DETAIL_COLUMNS:
        assert brp.ref_col_for(col) == "Conversion/replacement Data Source"
    backed = brp.value_cols_for("Conversion/replacement Data Source")
    assert backed[0] == "Conversion/replacement?"
    assert set(brp.CONVERSION_DETAIL_COLUMNS) <= set(backed)
