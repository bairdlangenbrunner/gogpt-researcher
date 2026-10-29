"""
Build a per-country prioritized worklist from the GOGPT-scoped export.

Encodes the Editing Manual's priority ladder for a quarterly country pass
(September 2026 manual, Baird 2026-10-27):
  1  in-development units (announced / pre-construction / construction)
  2  shelved units, including shelved-inferred
  3  units with a planned retirement in the current year
  4  units with a planned retirement in any other year
  5  everything else that is not ended: operating, mothballed, and the rest
  9  ended (retired / cancelled) - excluded unless --all

Plus the inferred-status sweep (date arithmetic only; the researcher must
search for recent evidence before staging anything). Only in-development
units get it (the manual lists announced, pre-construction and construction):
  - newest evidence date at least SHELVED_INFERRED_YEARS old
      -> "shelved-inferred candidate"
  - newest evidence date at least CANCELLED_INFERRED_YEARS old
      -> "cancelled-inferred candidate"
Shelved units no longer get the cancelled-inferred flag.

"Newest evidence date" = the latest of the Latest Activity date (the full
date when the export gives one, "Year: 2024, Month: 6, Day: 17", else the
year, counted as the end of that year so the sweep under-flags) and the year
in the Last Updated cell. That is a proxy (Last Updated moves on ANY edit,
so this UNDER-flags rather than over-flags); the sweep finds candidates, it
does not decide statuses.

Usage (from scripts/):
    python worklist.py --country Nigeria              # -> work/worklist_nigeria.csv
    python worklist.py --country Brazil --country Peru
    python worklist.py --state Maryland               # -> work/worklist_us-maryland.csv
    python worklist.py --state Texas --state Oklahoma # US states (implies --country "United States")
    python worklist.py                                # all countries, one file
    python worklist.py --all                          # include retired/cancelled
    python worklist.py --year 2027                    # override "this year"

Stops if the export is over a day old (fresh pull every batch);
--allow-stale-export downgrades that to a warning.
"""
import argparse
import csv
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import gogpt_scoped_csv, require_fresh_export, work_dir
from pull_gem_db import derive_column_map
from schema_constants import (
    CANCELLED_INFERRED_YEARS,
    SHELVED_INFERRED_YEARS,
    STATUSES_IN_DEVELOPMENT,
)

YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
LA_DATE_RE = re.compile(r"Year:\s*(\d{4})(?:,\s*Month:\s*(\d{1,2}))?(?:,\s*Day:\s*(\d{1,2}))?")

NEEDED = ["country", "state_province", "plant_name", "unit_name", "gem_unit_id", "status",
          "capacity_mw", "latest_activity", "last_updated", "planned_retire"]

OUT_HEADER = ["priority", "flag", "country", "state", "plant_name", "unit_name",
              "gem_unit_id", "status", "capacity_mw", "latest_activity",
              "last_updated", "planned_retire"]


def _add_years(d, n):
    try:
        return d.replace(year=d.year + n)
    except ValueError:                    # Feb 29
        return d.replace(year=d.year + n, day=28)


def evidence_date(latest_activity, last_updated):
    """The newest date of activity the export shows: the Latest Activity date
    (full, or year and month, else the end of its year) and the end of the
    newest year in Last Updated (and in Latest Activity when it has no
    parseable date). None when nothing parses."""
    dates = []
    m = LA_DATE_RE.search(latest_activity or "")
    if m:
        y, mo, d = int(m.group(1)), m.group(2), m.group(3)
        try:
            if mo and d:
                dates.append(datetime.date(y, int(mo), int(d)))
            elif mo:
                nxt = datetime.date(y + (int(mo) == 12), int(mo) % 12 + 1, 1)
                dates.append(nxt - datetime.timedelta(days=1))
            else:
                dates.append(datetime.date(y, 12, 31))
        except ValueError:
            dates.append(datetime.date(y, 12, 31))
    cells = (last_updated,) if m else (latest_activity, last_updated)
    years = [int(x.group(0)) for c in cells for x in YEAR_RE.finditer(c or "")]
    if years:
        dates.append(datetime.date(max(years), 12, 31))
    return max(dates) if dates else None


def priority_for(status, planned_retire, this_year):
    s = (status or "").strip().lower()
    if s in STATUSES_IN_DEVELOPMENT:
        return 1
    if s.startswith("shelved"):          # incl. "shelved - inferred 2 y"
        return 2
    if s == "retired" or s.startswith("cancelled"):
        return 9  # ended
    pr = planned_retire or ""
    if str(this_year) in pr:
        return 3
    if YEAR_RE.search(pr):
        return 4
    if s == "operating" or s == "mothballed":
        return 5
    return 9 if not s else 5  # unrecognized non-blank statuses stay visible


def inferred_flag(status, evidence, as_of):
    """Flag an in-development unit whose newest evidence is old enough that the
    manual's inferred statuses would apply (date arithmetic, not a finding)."""
    s = (status or "").strip().lower()
    if s not in STATUSES_IN_DEVELOPMENT:
        return ""
    if evidence is None:
        return "no evidence date parseable"
    age = round((as_of - evidence).days / 365.25, 1)
    if as_of >= _add_years(evidence, CANCELLED_INFERRED_YEARS):
        return f"cancelled-inferred candidate ({age:g}y since evidence)"
    if as_of >= _add_years(evidence, SHELVED_INFERRED_YEARS):
        return f"shelved-inferred candidate ({age:g}y since evidence)"
    return ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default=str(gogpt_scoped_csv()),
                   help="GOGPT-scoped export (run scope_filter.py first)")
    p.add_argument("--country", action="append", default=None,
                   help="repeatable; omit for all countries")
    p.add_argument("--state", action="append", default=None,
                   help="repeatable; State/Province (full name, e.g. Texas); "
                        "implies --country 'United States' unless --country given")
    p.add_argument("--all", action="store_true",
                   help="include priority-9 (retired/cancelled) rows")
    p.add_argument("--year", type=int, default=datetime.date.today().year)
    p.add_argument("--out", default=None)
    p.add_argument("--allow-stale-export", action="store_true",
                   help="warn instead of stopping when the export is over a day old")
    args = p.parse_args()

    if not Path(args.csv).exists():
        sys.exit(f"ERROR: {args.csv} not found — run scope_filter.py first\n"
                 "  (worklists must come from the SCOPED view, not the raw export)")
    require_fresh_export(args.csv, args.allow_stale_export)

    col_map = derive_column_map(args.csv)
    missing = [c for c in NEEDED if col_map.get(c) is None]
    if missing:
        sys.exit(f"ERROR: columns not found in {args.csv}: {missing} — schema drift?")
    idx = {c: col_map[c] for c in NEEDED}

    today = datetime.date.today()
    as_of = _add_years(today, args.year - today.year)
    countries = {c.strip().lower() for c in args.country} if args.country else None
    states = {x.strip().lower() for x in args.state} if args.state else None
    if states and not countries:
        countries = {"united states"}

    rows_out = []
    counts = {}
    with open(args.csv, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            country = row[idx["country"]].strip()
            if countries and country.lower() not in countries:
                continue
            state = row[idx["state_province"]].strip()
            if states and state.lower() not in states:
                continue
            status = row[idx["status"]]
            prio = priority_for(status, row[idx["planned_retire"]], args.year)
            if prio == 9 and not args.all:
                continue
            ev = evidence_date(row[idx["latest_activity"]], row[idx["last_updated"]])
            flag = inferred_flag(status, ev, as_of)
            rows_out.append([prio, flag, country, state,
                             row[idx["plant_name"]], row[idx["unit_name"]],
                             row[idx["gem_unit_id"]], status,
                             row[idx["capacity_mw"]],
                             row[idx["latest_activity"]],
                             row[idx["last_updated"]],
                             row[idx["planned_retire"]]])
            counts[prio] = counts.get(prio, 0) + 1

    rows_out.sort(key=lambda r: (r[0], r[2], r[3], r[4], r[5]))

    if args.out:
        out_path = Path(args.out)
    else:
        if states:
            tag = "us-" + "_".join(sorted(x.replace(" ", "-") for x in states))
        else:
            tag = ("_".join(sorted(countries)).replace(" ", "-")
                   if countries else "all")
        out_path = work_dir() / f"worklist_{tag}.csv"
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(OUT_HEADER)
        w.writerows(rows_out)

    scope = ", ".join(sorted(countries)) if countries else "all countries"
    if states:
        scope += " / " + ", ".join(sorted(states))
    print(f"worklist for {scope}: {len(rows_out)} rows -> {out_path}")
    for prio in sorted(counts):
        print(f"  priority {prio}: {counts[prio]}")
    flagged = sum(1 for r in rows_out if "candidate" in r[1])
    if flagged:
        print(f"  inferred-status candidates to confirm/refute: {flagged}")


if __name__ == "__main__":
    main()
