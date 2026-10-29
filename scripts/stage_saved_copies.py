"""Stage saved (Wayback) copies of dead Data Source links as unchanged-value records.

Kansas batch, 2026-10-23: four Data Source links already in the database no longer
load (the Kansas Department of Health and Environment permit files, an old Kansas
Corporation Commission filing, an old Kansas Power Pool newsletter). Each saved copy
was checked with url_verifier.py against the value it supports. A record here keeps
the value and adds the saved copy to the Data Source box; the dead link stays
(datasources are never deleted). Safe to re-run: records are keyed on record_id.

    python stage_saved_copies.py --scope us-ks

Superseded (2026-10-23) by check_existing_links.py, which finds the dead Data Source links
for any scope before the sweep, reads their saved copies and stages the same records
without a hand-written list. This file stays as the record of the Kansas items.
"""
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from url_verifier import verify_url  # noqa: E402

W = "https://web.archive.org/web/"
VIOLA = W + "20251203003910/https://www.kdhe.ks.gov/DocumentCenter/View/52541/Evergy-Viola-Energy-Center-PSD-Application-PDF"
MCNEW = W + "20251128090354/https://www.kdhe.ks.gov/DocumentCenter/View/52884/Evergy-McNew-Energy-Application-PDF"
ESTAR = W + "20240702151342/https://estar.kcc.ks.gov/estar/ViewFile.aspx/S202109200727054038.pdf?Id=7918cb08-a60d-4dea-b4b0-eeafa61bc0d0"
KPP = W + "20230329141358/https://www.kpp.agency/wp-content/uploads/March-2023-KPP-Lightning-Round-min.pdf"

# (plant id, unit id, plant name, unit name, value column, current value, source column, saved copy, words it must hold, what the old link is)
ITEMS = [
    ("L100001043000", "G100001048433", "Viola Generating Station", "1", "Equipment Manufacturer/Model",
     "Mitsubishi Power: M501JAC", "Turbine/Engine Equipment Data Source", VIOLA, ["Viola", "M501JAC"],
     "the Kansas Department of Health and Environment permit application for Viola (document 52541)"),
    ("L100001023601", "G100001028229", "McNew Generating Station", "1", "Equipment Manufacturer/Model",
     "Mitsubishi Power: M501JAC", "Turbine/Engine Equipment Data Source", MCNEW, ["McNew", "M501JAC"],
     "the Kansas Department of Health and Environment permit application for McNew (document 52884)"),
    ("L100000103924", "G100001017857", "Lawrence Energy Center (Kansas)", "Unit 5, timepoint 2", "Fuel",
     "fossil gas: natural gas", "Fuel Data Source", ESTAR, ["Lawrence", "natural gas"],
     "an old Kansas Corporation Commission filing (the old filing site is gone)"),
    ("L100001023564", "G100001028107", "Walnut Energy Center power station", "1", "Start year",
     "2026", "Start Year Data Source", KPP, ["Walnut", "2026"],
     "the March 2023 Kansas Power Pool newsletter (the old web address now redirects to a broken one)"),
    ("L100001023564", "G100001028107", "Walnut Energy Center power station", "1", "Owner(s)",
     "Kansas Power Pool [100%]", "Owners Data Source", KPP, ["Walnut", "Kansas Power Pool"],
     "the March 2023 Kansas Power Pool newsletter (the old web address now redirects to a broken one)"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", required=True)
    a = ap.parse_args()
    path = REPO / "batches" / a.scope / "staging" / "staged_updates.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    have = {r["record_id"] for r in data["records"]}
    added = 0
    for pid, uid, pname, uname, col, cur, src, url, words, old in ITEMS:
        rid = f"{pid}:{uid}:{col.lower().replace('(', '').replace(')', '').replace('/', '-').replace(' ', '-')}-saved-copy"
        if rid in have:
            continue
        ok, why = verify_url(url, words)
        if not ok:
            print(f"skip {rid}: {why}")
            continue
        data["records"].append({
            "gem_unit_id": uid, "gem_plant_id": pid, "plant_name": pname, "unit_name": uname,
            "country": "United States", "record_id": rid, "cluster": uid, "verdict": "match",
            "reverified": True, "fields": {col: cur}, "current": {col: cur},
            "refs": {src: [url]},
            "verifications": [{"url": url, "ok": True, "contains_value": True, "name_found": True}],
            "tier": "high", "independent": False, "source_language": "en",
            "researcher_notes": (f"The value is unchanged. The source box already holds a link to {old}, and that link no "
                                 "longer opens. The Internet Archive kept a saved copy, which was read and states the value."),
            "action": f"Leave {col} of unit {uname} ({uid}) as it is. Add the 1 link below to the {src} box. Keep the links already there.",
            "checks": [10],
        })
        added += 1
    data["meta"]["counts"]["records"] = len(data["records"])
    data["meta"]["counts"]["reverified"] = data["meta"]["counts"].get("reverified", 0) + added
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"added {added} record(s) to {path}")


if __name__ == "__main__":
    main()
