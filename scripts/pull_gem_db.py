"""
Derive the column-index map for a GOGPT all-fields export CSV from its header row.

This script never fetches anything. Pull the CSV first via the sibling
gem-db-ops repo's engine (from scripts/):

    python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv

then run `python pull_gem_db.py --map-only` to derive the .colmap.json.
Running without `--map-only` exits with a pointer to those commands — this
repo keeps no pull-engine copies (family rule since 2026-07-21).

SCOPE WARNING: the export contains EVERY combustion unit (oil + gas + coal/
GCPT + bioenergy/GBPT) — the website's ?tracker=GOGPT filter is cosmetic and
the engine deliberately mirrors that. Run `python scope_filter.py` after the
pull to derive the GOGPT-only view; keep the unfiltered CSV for coal-
conversion/replacement cross-checks.

Why re-derive the column map every batch:
  - The GOGPT all-fields export is 86 columns (Q2 2026) but the schema can
    drift between releases (columns added, renamed, reordered)
  - Hard-coding column offsets means batch breakage on any schema change
  - The derived map is saved next to the CSV so other scripts use the same one
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import db_ops_repo  # noqa: E402  — resolves the sibling gem-db-ops checkout
from schema_constants import COMPUTED_COLUMNS, OUT_OF_SCOPE_COLUMNS  # noqa: E402

sys.path.insert(0, str(db_ops_repo()))
import gem_colmap  # noqa: E402  — canonical expected columns + derive/report/save


DEFAULT_OUT = "./gem_export_gogpt.csv"

# Columns we depend on — keyed by canonical short name, value is the expected
# header text (exact, from gem-db-ops/gem_all_fields.py GOGPT_COLUMNS). The
# actual column index is derived from the header row at runtime.
#
# Maintained in gem-db-ops/gem_colmap.py (GOGPT_EXPECTED_COLUMNS) as of
# 2026-08-11 so this repo and the pull itself can never disagree about the
# schema. Add newly-appearing GEM columns THERE, not here.
EXPECTED_COLUMNS = gem_colmap.GOGPT_EXPECTED_COLUMNS

# Read-only columns (build_review_package.py must NEVER write these). Derived
# from the canonical header-string sets in schema_constants.py, translated into
# this script's short/canonical column-name keys via EXPECTED_COLUMNS.
READ_ONLY_COMPUTED = {k for k, v in EXPECTED_COLUMNS.items() if v in COMPUTED_COLUMNS}

READ_ONLY_OUT_OF_SCOPE = {k for k, v in EXPECTED_COLUMNS.items() if v in OUT_OF_SCOPE_COLUMNS}


def derive_column_map(csv_path):
    """Read header row, return {canonical_name: 0-indexed-column} dict.
    Missing expected columns get None (so the caller can detect schema drift).
    Thin wrapper over gem-db-ops' gem_colmap.derive_from_csv."""
    return gem_colmap.derive_from_csv(csv_path, EXPECTED_COLUMNS)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", "--out", dest="out", default=DEFAULT_OUT)
    p.add_argument("--map-only", action="store_true",
                   help="Derive the map from an existing CSV (the only mode)")
    args = p.parse_args()

    if not args.map_only:
        sys.exit(
            "ERROR: this script never fetches the export — pull via the sibling\n"
            "  gem-db-ops repo's engine, then derive the map (from scripts/):\n\n"
            "    python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv\n"
            "    python pull_gem_db.py --map-only\n\n"
            "  (gem-db-ops' pull writes an identical .colmap.json itself, so the\n"
            "  second step is only needed for a CSV pulled some other way.)\n"
        )

    gem_colmap.derive_report_save(args.out, EXPECTED_COLUMNS)


if __name__ == "__main__":
    main()
