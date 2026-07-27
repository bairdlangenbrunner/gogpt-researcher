"""
Build a per-country prioritized worklist from the GOGPT-scoped export.

Encodes the Editing Manual's priority ladder for a quarterly country pass:
  1  in-development units (announced / pre-construction / construction)
  2  shelved units due for review
  3  units with a planned retirement this year
  4  other mothballed units
  5  operating spot-checks
  9  ended (retired / cancelled) — excluded unless --all

Plus the inferred-status sweep (date arithmetic only — the researcher must
search for recent evidence before staging anything):
  - priority-1 unit, newest evidence year >= SHELVED_INFERRED_YEARS old
      -> "shelved-inferred candidate"
  - priority-1 unit, newest evidence year >= CANCELLED_INFERRED_YEARS old
      -> "cancelled-inferred candidate"
  - shelved unit, newest evidence year >= CANCELLED_INFERRED_YEARS old
      -> "cancelled-inferred candidate"

"Newest evidence year" = the max 4-digit year found in the Latest Activity
and Last Updated cells. That is a proxy (Last Updated moves on ANY edit, so
this UNDER-flags rather than over-flags); the sweep finds candidates, it does
not decide statuses.

Usage (from scripts/):
    python worklist.py --country Nigeria              # -> work/worklist_nigeria.csv
    python worklist.py --country Brazil --country Peru
    python worklist.py                                # all countries, one file
    python worklist.py --all                          # include retired/cancelled
    python worklist.py --year 2027                    # override "this year"
"""
import argparse
import csv
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import gogpt_scoped_csv, work_dir
from pull_gem_db import derive_column_map
from schema_constants import (
    CANCELLED_INFERRED_YEARS,
    SHELVED_INFERRED_YEARS,
    STATUSES_IN_DEVELOPMENT,
)

YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")

NEEDED = ["country", "plant_name", "unit_name", "gem_unit_id", "status",
          "capacity_mw", "latest_activity", "last_updated", "planned_retire"]

OUT_HEADER = ["priority", "flag", "country", "plant_name", "unit_name",
              "gem_unit_id", "status", "capacity_mw", "latest_activity",
              "last_updated", "planned_retire"]


def newest_year(*cells):
    years = [int(m.group(0)) for c in cells for m in YEAR_RE.finditer(c or "")]
    return max(years) if years else None


def priority_for(status, planned_retire, this_year):
    s = (status or "").strip().lower()
    if s in STATUSES_IN_DEVELOPMENT:
        return 1
    if s.startswith("shelved"):          # incl. "shelved - inferred 2 y"
        return 2
    if str(this_year) in (planned_retire or "") \
            and not (s == "retired" or s.startswith("cancelled")):
        return 3
    if s == "mothballed":
        return 4
    if s == "operating":
        return 5
    return 9  # retired / cancelled / unrecognized


def inferred_flag(priority, status, evidence_year, this_year):
    if evidence_year is None:
        return "no evidence year parseable"
    age = this_year - evidence_year
    s = (status or "").strip().lower()
    if priority == 1:
        if age >= CANCELLED_INFERRED_YEARS:
            return f"cancelled-inferred candidate ({age}y since evidence)"
        if age >= SHELVED_INFERRED_YEARS:
            return f"shelved-inferred candidate ({age}y since evidence)"
    elif s.startswith("shelved") and age >= CANCELLED_INFERRED_YEARS:
        return f"cancelled-inferred candidate ({age}y since evidence)"
    return ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default=str(gogpt_scoped_csv()),
                   help="GOGPT-scoped export (run scope_filter.py first)")
    p.add_argument("--country", action="append", default=None,
                   help="repeatable; omit for all countries")
    p.add_argument("--all", action="store_true",
                   help="include priority-9 (retired/cancelled) rows")
    p.add_argument("--year", type=int, default=datetime.date.today().year)
    p.add_argument("--out", default=None)
    args = p.parse_args()

    if not Path(args.csv).exists():
        sys.exit(f"ERROR: {args.csv} not found — run scope_filter.py first\n"
                 "  (worklists must come from the SCOPED view, not the raw export)")

    col_map = derive_column_map(args.csv)
    missing = [c for c in NEEDED if col_map.get(c) is None]
    if missing:
        sys.exit(f"ERROR: columns not found in {args.csv}: {missing} — schema drift?")
    idx = {c: col_map[c] for c in NEEDED}

    countries = {c.strip().lower() for c in args.country} if args.country else None

    rows_out = []
    counts = {}
    with open(args.csv, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            country = row[idx["country"]].strip()
            if countries and country.lower() not in countries:
                continue
            status = row[idx["status"]]
            prio = priority_for(status, row[idx["planned_retire"]], args.year)
            if prio == 9 and not args.all:
                continue
            ev_year = newest_year(row[idx["latest_activity"]],
                                  row[idx["last_updated"]])
            flag = inferred_flag(prio, status, ev_year, args.year)
            rows_out.append([prio, flag, country,
                             row[idx["plant_name"]], row[idx["unit_name"]],
                             row[idx["gem_unit_id"]], status,
                             row[idx["capacity_mw"]],
                             row[idx["latest_activity"]],
                             row[idx["last_updated"]],
                             row[idx["planned_retire"]]])
            counts[prio] = counts.get(prio, 0) + 1

    rows_out.sort(key=lambda r: (r[0], r[2], r[3], r[4]))

    if args.out:
        out_path = Path(args.out)
    else:
        tag = ("_".join(sorted(countries)).replace(" ", "-")
               if countries else "all")
        out_path = work_dir() / f"worklist_{tag}.csv"
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(OUT_HEADER)
        w.writerows(rows_out)

    scope = ", ".join(sorted(countries)) if countries else "all countries"
    print(f"worklist for {scope}: {len(rows_out)} rows -> {out_path}")
    for prio in sorted(counts):
        print(f"  priority {prio}: {counts[prio]}")
    flagged = sum(1 for r in rows_out if "candidate" in r[1])
    if flagged:
        print(f"  inferred-status candidates to confirm/refute: {flagged}")


if __name__ == "__main__":
    main()
