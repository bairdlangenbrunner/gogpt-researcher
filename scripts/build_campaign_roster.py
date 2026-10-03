"""Build / refresh a campaign roster: per-scope status counts for a quarterly
GOGPT cycle, with manual tracking columns preserved across refreshes.

One roster row per SCOPE: `United States - <State/Province>` for each US state
(blank state -> `United States - (no state)`), the country name for every
other country. This mirrors the assignments tab's keys. A `country` column is
kept too, and `indev_mw` sums Capacity (MW) over in-development statuses
(the tab sorts US states by it).

Counts come from the GOGPT-SCOPED export (run scope_filter.py first). Manual
columns (assignee_role, assignment_status, packet_file, applied, notes) are
PRESERVED when the roster already exists (keyed on `scope`; an old roster with
only `country` is read with country as the scope) — a refresh only updates the
counts. The manual columns mirror the quarter's "Researcher Country
Assignments" tab (see docs/reference/sop_pointers.md); assignee_role is who
holds the assignment (names allowed, ruling 2026-09-15).

Usage (from scripts/):
    python build_campaign_roster.py --campaign q3-2026
    python build_campaign_roster.py --campaign q3-2026 --csv path/to/scoped.csv

Output: campaigns/<campaign>/roster.csv, sorted by in-dev total (desc).
"""
import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import gogpt_scoped_csv, repo_root
from pull_gem_db import derive_column_map
from schema_constants import STATUSES, STATUSES_IN_DEVELOPMENT

COUNTED = ["announced", "pre-construction", "construction", "shelved",
           "mothballed", "operating", "retired", "cancelled"]
MANUAL_COLS = ["assignee_role", "assignment_status", "packet_file", "applied",
               "notes"]


def parse_mw(cell):
    try:
        return float((cell or "").replace(",", "").strip() or 0)
    except ValueError:
        return 0.0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--campaign", required=True, help="slug, e.g. q3-2026")
    p.add_argument("--csv", default=str(gogpt_scoped_csv()),
                   help="GOGPT-scoped export (run scope_filter.py first)")
    args = p.parse_args()

    if not Path(args.csv).exists():
        sys.exit(f"ERROR: {args.csv} not found — run scope_filter.py first")

    col_map = derive_column_map(args.csv)
    for c in ("country", "state_province", "status", "capacity_mw"):
        if col_map.get(c) is None:
            sys.exit(f"ERROR: column {c!r} not in {args.csv} — schema drift?")

    counts = {}
    countries = {}
    indev_mw = {}
    unknown_statuses = set()
    with open(args.csv, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            country = row[col_map["country"]].strip()
            status = row[col_map["status"]].strip().lower()
            if not country:
                continue
            if country.lower() == "united states":
                state = row[col_map["state_province"]].strip() or "(no state)"
                scope = f"United States - {state}"
            else:
                scope = country
            rec = counts.setdefault(scope, {s: 0 for s in COUNTED})
            countries[scope] = country
            if status in STATUSES_IN_DEVELOPMENT:
                indev_mw[scope] = indev_mw.get(scope, 0.0) + parse_mw(
                    row[col_map["capacity_mw"]])
            if status in rec:
                rec[status] += 1
            elif status and status not in STATUSES:
                unknown_statuses.add(status)

    out_dir = repo_root() / "campaigns" / args.campaign
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "roster.csv"

    manual = {}
    if out_path.exists():
        with open(out_path, encoding="utf-8", newline="") as f:
            for prior in csv.DictReader(f):
                key = prior.get("scope") or prior.get("country")
                manual[key] = {c: prior.get(c, "") for c in MANUAL_COLS}

    header = ["scope", "country", "indev_total", "indev_mw"] + COUNTED + ["total_rows"] + MANUAL_COLS
    rows = []
    for scope, rec in counts.items():
        indev = sum(rec[s] for s in STATUSES_IN_DEVELOPMENT)
        row = {"scope": scope, "country": countries[scope],
               "indev_total": indev,
               "indev_mw": round(indev_mw.get(scope, 0.0), 1),
               "total_rows": sum(rec.values()), **rec,
               **manual.get(scope, {c: "" for c in MANUAL_COLS})}
        rows.append(row)
    rows.sort(key=lambda r: (-r["indev_total"], -r["total_rows"], r["scope"]))

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)

    print(f"wrote {out_path}: {len(rows)} scopes "
          f"({'manual columns preserved' if manual else 'fresh roster'})")
    if unknown_statuses:
        print(f"  WARNING: statuses outside the vocabulary in the export: "
              f"{sorted(unknown_statuses)}", file=sys.stderr)


if __name__ == "__main__":
    main()
