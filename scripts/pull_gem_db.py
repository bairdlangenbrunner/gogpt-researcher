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
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from schema_constants import COMPUTED_COLUMNS, OUT_OF_SCOPE_COLUMNS


DEFAULT_OUT = "./gem_export_gogpt.csv"

# Columns we depend on — keyed by canonical short name, value is the expected
# header text (exact, from gem-db-ops/gem_all_fields.py GOGPT_COLUMNS). The
# actual column index is derived from the header row at runtime.
EXPECTED_COLUMNS = {
    "last_updated": "Last Updated",
    "researcher": "Researcher",
    "research_status": "Research status",
    "wiki_url": "Wiki URL",
    "country": "Country/Area",
    "plant_name": "Plant name",
    "plant_name_local": "Plant Name in Local Language / Script",
    "other_names": "Other Name(s)",
    "unit_name": "Unit name",
    "fuel": "Fuel",
    "fuel_ref": "Fuel Data Source",
    "num_engines": "Number Of Engines",
    "capacity_per_engine": "Capacity Per Engine",
    "capacity_mw": "Capacity (MW)",
    "capacity_ref": "Capacity Data Source",
    "status": "Status",
    "status_detail": "Status Detail",
    "status_ref": "Status Data Source",
    "conflict_disrupted": "Disrupted due to conflict",
    "conflict_disrupted_ref": "Disrupted due to conflict Data Source",
    "latest_activity": "Latest Activity",
    "latest_activity_ref": "Latest Activity Data Source",
    "cancellation_year": "Cancellation year",
    "cancellation_year_ref": "Cancellation year Data Source",
    "technology": "Turbine/Engine Technology",
    "technology_ref": "Turbine/Engine Technology Data Source",
    "equipment": "Equipment Manufacturer/Model",
    "equipment_ref": "Turbine/Engine Equipment Data Source",
    "chp": "CHP",
    "chp_ref": "CHP Data Source",
    "hydrogen_capable": "Hydrogen capable?",
    "hydrogen_notes": "Hydrogen Notes",
    "hydrogen_ref": "Hydrogen Data Source",
    "h2_ready_pct": "H2 ready turbine (%)?",
    "h2_mou": "MOU for H2 supply?",
    "h2_contract": "Contract for H2 supply?",
    "h2_financing": "Financing for supply of H2?",
    "h2_colocated": "Co-located with electrolyzer/H2 production facility?",
    "h2_blending_pct": "What % of H2 blending currently?",
    "h2_criteria_ref": "H2 Criteria Data Source",
    "ccs": "CCS attachment?",
    "ccs_ref": "CCS Data Source",
    "conversion": "Conversion/replacement?",
    "conversion_from_fuel": "Conversion from/replacement of (fuel)",
    "conversion_from_unit": "Conversion from/replacement of (GEM unit ID)",
    "conversion_ref": "Conversion/replacement Data Source",
    "conversion_to_fuel": "Conversion to (fuel)",
    "conversion_to_unit": "Conversion to (GEM unit ID)",
    "start_year": "Start year",
    "start_year_ref": "Start Year Data Source",
    "retired_year": "Retired year",
    "retired_year_ref": "Retired Year Data Source",
    "planned_retire": "Planned retire",
    "planned_retire_ref": "Planned Retire Data Source",
    "operator": "Operator(s)",
    "operator_ref": "Operators Data Source",
    "operator_entity_id": "Operator GEM Entity ID",
    "owner": "Owner(s)",
    "owner_entity_id": "Owner(s) GEM Entity ID",
    "owner_ref": "Owners Data Source",
    "parent": "Parent(s)",
    "parent_entity_id": "Parent GEM Entity ID",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "location_accuracy": "Location accuracy",
    "location_ref": "Location Data Source",
    "city": "City",
    "local_area": "Local area (taluk, county)",
    "major_area": "Major area (prefecture, district)",
    "state_province": "State/Province",
    "subregion": "Subregion",
    "region": "Region",
    "other_ids_location": "Other IDs (location)",
    "other_ids_unit": "Other IDs (unit)",
    "notes": "Notes",
    "captive_industry_use": "Captive industry use",
    "captive_industry_type": "Captive industry type",
    "captive_non_industry_use": "Captive non-industry use",
    "captive_ref": "Captive Data Source",
    "gem_location_id": "GEM location ID",
    "gem_unit_id": "GEM unit ID",
    "wepp_location_id": "WEPP location ID",
    "wepp_unit_id": "WEPP unit ID",
    "employment_notes": "Employment Notes",
    "employment_notes_ref": "Employment Notes Data Source",
    "linked_projects": "Linked Projects",
}

# Read-only columns (build_review_package.py must NEVER write these). Derived
# from the canonical header-string sets in schema_constants.py, translated into
# this script's short/canonical column-name keys via EXPECTED_COLUMNS.
READ_ONLY_COMPUTED = {k for k, v in EXPECTED_COLUMNS.items() if v in COMPUTED_COLUMNS}

READ_ONLY_OUT_OF_SCOPE = {k for k, v in EXPECTED_COLUMNS.items() if v in OUT_OF_SCOPE_COLUMNS}


def derive_column_map(csv_path):
    """Read header row, return {canonical_name: 0-indexed-column} dict.
    Unknown columns get None; missing expected columns also get None
    (so the caller can detect schema drift).
    """
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            sys.exit(f"ERROR: empty CSV at {csv_path}")

    # Strip a BOM on the first column if present
    if header and header[0].startswith("﻿"):
        header[0] = header[0][1:]

    col_map = {"_header_columns": header, "_total_columns": len(header)}

    for canonical, needle in EXPECTED_COLUMNS.items():
        idx = None
        for i, h in enumerate(header):
            if h.strip() == needle:
                idx = i
                break
        col_map[canonical] = idx

    canonical_headers = set(EXPECTED_COLUMNS.values())
    unknown = [h for h in header if h.strip() not in canonical_headers]
    col_map["_unknown_columns"] = unknown

    return col_map


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
            "    python pull_gem_db.py --map-only\n"
        )

    col_map = derive_column_map(args.out)

    print(f"\nColumn-index map ({col_map['_total_columns']} total columns):")
    missing = []
    for k, v in col_map.items():
        if k.startswith("_"):
            continue
        status = "OK" if v is not None else "MISSING"
        if v is None:
            missing.append(k)
            print(f"  {k:35} = {'--':<5} [{status}]")
        else:
            print(f"  {k:35} = {v:<5}")

    if missing:
        print(f"\n  WARNING: {len(missing)} expected columns not found:")
        for k in missing:
            print(f"    {k}  (expected header text: {EXPECTED_COLUMNS[k]!r})")
        print(f"\n  Schema may have changed — check the live DB and update EXPECTED_COLUMNS.")

    if col_map["_unknown_columns"]:
        print(f"\n  NOTE: {len(col_map['_unknown_columns'])} unknown columns in header:")
        for h in col_map["_unknown_columns"]:
            print(f"    {h!r}")

    # Save the map next to the CSV
    map_path = Path(args.out).with_suffix(".colmap.json")
    serializable = {k: v for k, v in col_map.items() if k != "_header_columns"}
    serializable["_header_columns_count"] = col_map["_total_columns"]
    map_path.write_text(json.dumps(serializable, indent=2))
    print(f"\n  Column map saved to {map_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
