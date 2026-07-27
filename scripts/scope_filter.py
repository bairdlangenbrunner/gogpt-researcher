"""
Derive the GOGPT-scoped view from the all-combustion export.

THE SCOPE GOTCHA (why this script exists): the gem-db-ops GOGPT export
deliberately mirrors the website and contains EVERY combustion unit — oil +
gas (GOGPT) alongside coal (GCPT) and bioenergy (GBPT). ~34.5k rows, of which
only the trackerSearch='GOGPT' subset is this repo's research scope. Every
batch must work from the scoped view this script writes; the UNFILTERED CSV
is kept on disk on purpose — conversion/replacement checks need the GCPT/GBPT
side visible (timepoint links, "R"-suffix replacement units, shared plants).

Primary mode (authoritative): query the read-only Postgres for
    SELECT id FROM powerplant_unit WHERE "trackerSearch" = 'GOGPT'
via the sibling gem-db-ops engine (GEM_READONLY_DB_URL env var), and keep the
CSV rows whose "GEM unit ID" == "G" + id.

Offline fallback (--offline, or automatic when the env var is unset):
fuel-token heuristic — drop rows whose Fuel matches a coal/bioenergy hint and
contains no GOGPT fuel. APPROXIMATE: mixed-fuel and oddly-labelled units can
be misclassified. Never ship a batch from an offline-scoped view without
re-running the DB mode first.

Usage (from scripts/):
    python scope_filter.py                    # gem_export_gogpt.csv -> gem_export_gogpt_scoped.csv
    python scope_filter.py --offline          # force the fuel heuristic
    python scope_filter.py --csv X --out Y    # custom paths
"""
import argparse
import csv
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import db_ops_repo, gem_export_csv, gogpt_scoped_csv
from pull_gem_db import derive_column_map
from schema_constants import GOGPT_FUELS, NON_GOGPT_FUEL_HINTS

ENV_VAR = "GEM_READONLY_DB_URL"


def gogpt_unit_ids_from_db():
    """Authoritative scope: display unit IDs ('G'+id) with trackerSearch='GOGPT'."""
    sys.path.insert(0, str(db_ops_repo()))
    from gem_query import get_database_url, build_engine, DEFAULT_STATEMENT_TIMEOUT_MS
    from sqlalchemy import text

    engine = build_engine(get_database_url(), DEFAULT_STATEMENT_TIMEOUT_MS)
    with engine.connect() as conn:
        rows = conn.execute(
            text('SELECT id FROM powerplant_unit WHERE "trackerSearch" = :t'),
            {"t": "GOGPT"},
        )
        return {f"G{r[0]}" for r in rows}


def fuel_is_gogpt(fuel_cell):
    """Offline heuristic. Keep unless the fuel is recognizably coal/bioenergy
    with no GOGPT fuel alongside. Unknown/blank fuels are KEPT (flagged for
    review) rather than silently dropped."""
    fuel = (fuel_cell or "").strip().lower()
    if not fuel:
        return True
    has_gogpt = any(f.lower() in fuel for f in GOGPT_FUELS)
    has_non = any(hint in fuel for hint in NON_GOGPT_FUEL_HINTS)
    return has_gogpt or not has_non


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default=str(gem_export_csv()),
                   help="unfiltered all-combustion export (kept, never modified)")
    p.add_argument("--out", default=str(gogpt_scoped_csv()))
    p.add_argument("--offline", action="store_true",
                   help="force the fuel-token heuristic (no DB query)")
    args = p.parse_args()

    if not Path(args.csv).exists():
        sys.exit(f"ERROR: {args.csv} not found — pull first:\n"
                 f"    python ../../gem-db-ops/gogpt/pull.py --output {args.csv}")

    col_map = derive_column_map(args.csv)
    for needed in ("gem_unit_id", "fuel"):
        if col_map.get(needed) is None:
            sys.exit(f"ERROR: column {needed!r} not found in {args.csv} header — "
                     "schema drift? Run pull_gem_db.py --map-only and check.")
    id_idx, fuel_idx = col_map["gem_unit_id"], col_map["fuel"]

    use_db = not args.offline and os.environ.get(ENV_VAR)
    if use_db:
        gogpt_ids = gogpt_unit_ids_from_db()
        print(f"DB scope: {len(gogpt_ids):,} trackerSearch='GOGPT' unit IDs",
              file=sys.stderr)
    else:
        gogpt_ids = None
        print(f"WARNING: offline mode ({ENV_VAR} unset or --offline) — using the\n"
              "  APPROXIMATE fuel heuristic. Re-run in DB mode before any batch ships.",
              file=sys.stderr)

    kept = dropped = 0
    unmatched_ids = 0
    with open(args.csv, encoding="utf-8", newline="") as fin, \
         open(args.out, "w", encoding="utf-8", newline="") as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        writer.writerow(next(reader))  # header
        for row in reader:
            if gogpt_ids is not None:
                keep = row[id_idx].strip() in gogpt_ids
                if not keep and not row[id_idx].strip():
                    unmatched_ids += 1
            else:
                keep = fuel_is_gogpt(row[fuel_idx])
            if keep:
                writer.writerow(row)
                kept += 1
            else:
                dropped += 1

    mode = "db" if gogpt_ids is not None else "offline-heuristic"
    print(f"scoped view: kept {kept:,} rows, dropped {dropped:,} "
          f"(mode={mode}) -> {args.out}")
    if unmatched_ids:
        print(f"  NOTE: {unmatched_ids} rows had a blank GEM unit ID", file=sys.stderr)
    print(f"  unfiltered export retained at {args.csv} "
          "(needed for conversion/replacement cross-checks)")


if __name__ == "__main__":
    main()
