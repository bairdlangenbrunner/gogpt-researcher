"""
Draw a reproducible random sample of in-development GOGPT plants for the
CREA emissions scoping (see README.md in this directory).

Reads the fresh scoped export produced by the normal pull chain
(scripts/gem_export_gogpt_scoped.csv + its .colmap.json) and samples at the
PLANT level (gem_location_id) among plants with at least one unit whose status
is in --statuses. The shuffle is seeded per country, so re-running with the
same seed on the same export gives the same draw order, and adding a country
never reshuffles another.

    python emissions/draw_sample.py --countries Vietnam Brazil
    python emissions/draw_sample.py --countries Germany --n 3 --alternates 2

Output is a markdown table on stdout. Read-only: nothing here stages anything
or feeds the GOGPT batch workflows.
"""
import argparse
import csv
import json
import random
from collections import OrderedDict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCOPED_CSV = REPO / "scripts" / "gem_export_gogpt_scoped.csv"
COLMAP = REPO / "scripts" / "gem_export_gogpt.colmap.json"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--countries", nargs="+", required=True)
    ap.add_argument("--statuses", nargs="+", default=["announced", "pre-construction"])
    ap.add_argument("--n", type=int, default=3, help="plants to sample per country")
    ap.add_argument("--alternates", type=int, default=2, help="extra plants drawn after the sample")
    ap.add_argument("--seed", default="20260917")
    args = ap.parse_args()

    col = {k: v for k, v in json.loads(COLMAP.read_text()).items() if isinstance(v, int) and not k.startswith("_")}
    with open(SCOPED_CSV, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))[1:]

    for country in args.countries:
        plants = OrderedDict()
        for r in rows:
            if r[col["country"]] == country and r[col["status"]] in args.statuses:
                plants.setdefault(r[col["gem_location_id"]], []).append(r)
        order = sorted(plants)
        random.Random(f"{args.seed}-{country}").shuffle(order)

        print(f"\n### {country} — {len(plants)} plants with {'/'.join(args.statuses)} units (seed {args.seed})\n")
        print("| draw | plant | GEM location ID | state/province | units (MW, status, technology) | owner |")
        print("|---|---|---|---|---|---|")
        for i, pid in enumerate(order[: args.n + args.alternates], 1):
            units = plants[pid]
            first = units[0]
            unit_txt = "; ".join(
                f"{u[col['unit_name']]}: {u[col['capacity_mw']]} MW, {u[col['status']]}, {u[col['technology']] or 'unknown'}"
                for u in units
            )
            label = str(i) if i <= args.n else f"alt {i - args.n}"
            print(
                f"| {label} | {first[col['plant_name']]} | {pid} | {first[col['state_province']]} "
                f"| {unit_txt} | {first[col['owner']]} |"
            )


if __name__ == "__main__":
    main()
