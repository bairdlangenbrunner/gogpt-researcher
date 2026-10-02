"""
Build / refresh the per-country coverage tracker for the CREA emissions
scoping (see README.md and search_plan.md in this directory).

One row per fossil-gas PLANT (gem_location_id) in the fresh scoped export
(scripts/gem_export_gogpt_scoped.csv + its .colmap.json). The left-hand
columns are regenerated from the export on every run; the right-hand SEARCH
columns are hand-maintained and carried over from the existing CSV by
gem_location_id, so re-running after a fresh pull never loses research state.
Plants that drop out of the export keep their row, flagged in `track`.

    python emissions/build_coverage.py --countries Vietnam Brazil

Writes emissions/coverage/<country>.csv and prints a status summary.
Read-only against GEM: nothing here stages anything or feeds the GOGPT batch
workflows.
"""
import argparse
import csv
import json
from collections import Counter, OrderedDict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCOPED_CSV = REPO / "scripts" / "gem_export_gogpt_scoped.csv"
COLMAP = REPO / "scripts" / "gem_export_gogpt.colmap.json"
OUT_DIR = Path(__file__).resolve().parent / "coverage"

PIPELINE = ["construction", "pre-construction", "announced"]
# most informative status first: a plant is filed under its first match
LEAD_ORDER = PIPELINE + ["operating", "mothballed", "shelved", "shelved - inferred 2 y",
                         "cancelled", "cancelled - inferred 4 y", "retired"]

GEM_FIELDS = ["track", "lead_status", "gem_location_id", "plant_name", "plant_name_local",
              "other_names", "state_province", "units", "mw_pipeline", "mw_operating",
              "technology", "equipment", "fuel", "owner", "start_years", "lat", "lon"]
# Hand-maintained. Vocabulary is defined in search_plan.md.
SEARCH_FIELDS = ["licensor", "licence_stage", "search_status", "doc_type", "doc_ref",
                 "doc_design_matches", "evidence", "basis", "pollutants", "rungs_tried",
                 "last_checked", "notes"]


def mw(v):
    try:
        return float(v.replace(",", ""))
    except ValueError:
        return 0.0


def uniq(values):
    return "; ".join(OrderedDict.fromkeys(v.strip() for v in values if v.strip()))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--countries", nargs="+", required=True)
    args = ap.parse_args()

    col = {k: v for k, v in json.loads(COLMAP.read_text()).items() if isinstance(v, int) and not k.startswith("_")}
    with open(SCOPED_CSV, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))[1:]
    OUT_DIR.mkdir(exist_ok=True)

    for country in args.countries:
        plants = OrderedDict()
        for r in rows:
            if r[col["country"]] == country and "fossil gas" in r[col["fuel"]].lower():
                plants.setdefault(r[col["gem_location_id"]], []).append(r)

        out_path = OUT_DIR / f"{country.lower().replace(' ', '_')}.csv"
        kept = {}
        if out_path.exists():
            with open(out_path, encoding="utf-8", newline="") as f:
                kept = {r["gem_location_id"]: r for r in csv.DictReader(f)}

        out = []
        for pid, units in plants.items():
            statuses = [u[col["status"]] for u in units]
            lead = min(statuses, key=lambda s: LEAD_ORDER.index(s) if s in LEAD_ORDER else 99)
            track = "pipeline" if lead in PIPELINE else "operating" if lead == "operating" else "inactive"
            first = units[0]
            rec = {
                "track": track,
                "lead_status": lead,
                "gem_location_id": pid,
                "plant_name": first[col["plant_name"]],
                "plant_name_local": first[col["plant_name_local"]],
                "other_names": first[col["other_names"]],
                "state_province": first[col["state_province"]],
                "units": "; ".join(f"{s} x{n}" for s, n in Counter(statuses).items()),
                "mw_pipeline": round(sum(mw(u[col["capacity_mw"]]) for u in units if u[col["status"]] in PIPELINE)),
                "mw_operating": round(sum(mw(u[col["capacity_mw"]]) for u in units if u[col["status"]] == "operating")),
                "technology": uniq(u[col["technology"]] or "unknown" for u in units),
                "equipment": uniq(u[col["equipment"]] for u in units),
                "fuel": uniq(u[col["fuel"]] for u in units),
                "owner": uniq(u[col["owner"]] for u in units),
                "start_years": uniq(u[col["start_year"]] for u in units),
                "lat": first[col["latitude"]],
                "lon": first[col["longitude"]],
            }
            prev = kept.pop(pid, {})
            rec.update({k: prev.get(k, "") for k in SEARCH_FIELDS})
            out.append(rec)
        for pid, prev in kept.items():  # no longer a gas plant in the export: keep the research
            prev["track"] = "gone from export"
            out.append({k: prev.get(k, "") for k in GEM_FIELDS + SEARCH_FIELDS})

        order = {"pipeline": 0, "operating": 1, "inactive": 2, "gone from export": 3}
        out.sort(key=lambda r: (order[r["track"]],
                                LEAD_ORDER.index(r["lead_status"]) if r["lead_status"] in LEAD_ORDER else 99,
                                r["state_province"], r["plant_name"]))
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=GEM_FIELDS + SEARCH_FIELDS)
            w.writeheader()
            w.writerows(out)

        print(f"\n### {country} — {len(out)} gas plants -> {out_path.relative_to(REPO)}")
        for track in order:
            sub = [r for r in out if r["track"] == track]
            if sub:
                done = Counter(r["search_status"] or "not started" for r in sub)
                print(f"  {track:17s}{len(sub):4d}   " + ", ".join(f"{k}: {v}" for k, v in done.most_common()))


if __name__ == "__main__":
    main()
