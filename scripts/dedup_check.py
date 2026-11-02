#!/usr/bin/env python3
"""
Duplicate check for every new plant a batch stages (Discovery SOP §5).

Before a plant is added, someone has to show GEM does not already hold it,
under any fuel and any name. This script runs the four checks for each record
in <batch>/staging/staged_newplants.json and writes the results, so the check
never depends on an agent remembering it (Illinois, 2026-10-30: four PJM
queue adds were staged after a name search of the gas plants only).

    python dedup_check.py --batch ../batches/us-il [--csv gem_export_gogpt.csv] [--no-wiki]

Checks, per new plant
  name     every plant in the UNFILTERED export (gas, coal, bioenergy) in the
           same country whose Plant name, Other Name(s) or local-script name
           shares the candidate's distinctive words (generic words like
           power, station, county, LLC are dropped). All of one side's words
           must appear in the other, so "Will County Facility" meets "Will
           County Generating Station" but not "Willow Creek". A plant in
           another state or province must share every word.
  nearby   with a point on the record: every export plant within NEARBY_KM.
           Without one: every export plant in the same county (Local area)
           and state or province, any fuel.
  wiki     a gem.wiki full-text search for the name in quotes, without
           its "power station" suffix. Used only
           to DETECT a record GEM already has, never as a citation; the
           results stay in this file and never enter a staged record. A
           page counts as a match only when its title names a plant (station,
           plant, power, energy and the like) and is not a solar, wind,
           hydro, nuclear or battery project, a mine, a pipeline or a
           terminal; every title is still listed. A
           search that does not load is status "error" and the gate fails
           until it is rerun.
  staged   every other new plant, new unit, update or watch record in the
           batch that shares the candidate's distinctive words, and every
           other new plant in the same county.

Writes <batch>/dedup.json (machine) and <batch>/dedup.md (for a person).
Each entry carries a fingerprint of the name, county, state and point; a
record changed after the check is stale and the gate asks for a rerun.

Answering: a plant with any hit needs an entry under "dedup" in
<batch>/coverage.json, keyed by record_id:
    {"decision": "not_a_duplicate", "evidence": "<why each hit is a different plant>"}
"duplicate" means the finding belongs to the existing plant: move it to an
update record (Update SOP) and drop the new plant. state_gate.py gate `dedup`
enforces all of this.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import json
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from geo import distance_m, parse_coord  # noqa: E402
from paths import gem_export_csv  # noqa: E402

NEARBY_KM = 10
DEDUP_FILE = "dedup.json"
DECISIONS = ("not_a_duplicate", "duplicate")
WIKI_SEARCH = "https://www.gem.wiki/w/index.php?search={q}&fulltext=1&ns0=1&limit=20"
WIKI_HIT_RE = re.compile(r'class="mw-search-result-heading"><a href="[^"]+" title="([^"]+)"')

GENERIC = {
    "power", "station", "plant", "project", "facility", "energy", "energies", "center",
    "centre", "generating", "generation", "electric", "electricity", "llc", "inc", "corp",
    "company", "co", "ltd", "lp", "the", "of", "and", "gas", "natural", "fired", "combined",
    "cycle", "ccgt", "peaker", "peaking", "unit", "units", "county", "parish", "city", "hub",
    "site", "phase", "expansion", "new", "cogeneration", "cogen", "chp", "data", "campus",
    "holdings", "development", "partners", "solar", "wind", "storage", "battery", "mw",
    "sp", "z", "o", "sa", "ag", "gmbh", "elektrownia", "elektrocieplownia", "kraftwerk",
}
# gem.wiki pages for these can never be the same plant as a combustion project.
NOT_COMBUSTION = {"solar", "wind", "hydro", "hydroelectric", "nuclear", "battery", "pipeline",
                  "mine", "terminal", "farm"}
# A gem.wiki title is a plant page only when it carries one of these words.
PLANT_WORDS = {"station", "plant", "power", "generating", "generation", "energy", "facility",
               "cogeneration", "chp", "kraftwerk", "elektrownia", "elektrociepłownia"}
# Lanes whose records describe a plant that exists or is being added. Entity and
# question records about the same new plant are its companions, not duplicates.
STAGED_LANES = ("newplants", "newunits", "updates", "monitor")
NAME_COLS = ("Plant name", "Other Name(s)", "Plant Name in Local Language / Script")
COUNTY_COL = "Local area (taluk, county)"
STATE_COL = "State/Province"


def ws(s) -> str:
    return " ".join(str(s or "").split())


def words(name: str) -> set[str]:
    toks = re.findall(r"[^\W\d_]+|\d+", ws(name).lower())
    return {t for t in toks if t not in GENERIC and (len(t) > 2 or t.isdigit())}


def names_match(a: set[str], b: set[str]) -> bool:
    return bool(a) and bool(b) and (a <= b or b <= a)


def core_name(name: str) -> str:
    """The name without GEM's suffix, for a phrase search: "Will County Facility"."""
    return re.sub(r"\s+(power station|power plant|generating station|energy center|plant)$", "",
                  ws(name), flags=re.I)


def norm_county(s: str) -> str:
    s = ws(s).lower()
    return re.sub(r"\s+(county|parish|borough)$", "", s)


def plant_fields(rec: dict) -> dict:
    """The record's place fields, with any unit-level point folded in."""
    f = dict(rec.get("fields") or {})
    for u in rec.get("units") or []:
        for k in ("Latitude", "Longitude"):
            if not ws(f.get(k)) and ws((u.get("fields") or {}).get(k)):
                f[k] = u["fields"][k]
    return f


def fingerprint(rec: dict) -> str:
    f = plant_fields(rec)
    parts = [ws(rec.get("plant_name")), ws(rec.get("country")), ws(f.get(STATE_COL)),
             norm_county(f.get(COUNTY_COL)), ws(f.get("Latitude")), ws(f.get("Longitude"))]
    return hashlib.sha1("|".join(parts).lower().encode()).hexdigest()[:12]


def load_plants(csv_path: Path) -> list[dict]:
    """One entry per GEM location in the export, any fuel."""
    plants: dict[str, dict] = {}
    with open(csv_path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            lid = ws(row.get("GEM location ID"))
            if not lid:
                continue
            p = plants.setdefault(lid, {
                "gem_location_id": lid, "plant_name": ws(row.get("Plant name")),
                "country": ws(row.get("Country/Area")), "state": ws(row.get(STATE_COL)),
                "county": norm_county(row.get(COUNTY_COL)),
                "lat": ws(row.get("Latitude")), "lon": ws(row.get("Longitude")),
                "names": set(), "fuels": set(), "statuses": set()})
            for c in NAME_COLS:
                for n in re.split(r"[;,]\s*", ws(row.get(c))):
                    if n:
                        p["names"].add(n)
            if ws(row.get("Fuel")):
                p["fuels"].add(ws(row.get("Fuel")).split(":")[0])
            if ws(row.get("Status")):
                p["statuses"].add(ws(row.get("Status")))
    return list(plants.values())


def brief(p: dict, **extra) -> dict:
    out = {"gem_location_id": p["gem_location_id"], "plant_name": p["plant_name"],
           "fuels": sorted(p["fuels"]), "statuses": sorted(p["statuses"]),
           "county": p["county"], "state": p["state"]}
    out.update(extra)
    return out


def wiki_search(query: str) -> dict:
    from fetch import fetch_text
    url = WIKI_SEARCH.format(q=urllib.parse.quote(query))
    try:
        status, body = fetch_text(url, timeout=45)
    except Exception as e:  # noqa: BLE001 - any failure means rerun
        return {"status": "error", "query": query, "note": str(e)[:200], "titles": []}
    if status != "200" or "mw-search" not in body:
        return {"status": "error", "query": query, "note": f"HTTP {status}", "titles": []}
    titles = [t.replace("&#039;", "'").replace("&amp;", "&") for t in WIKI_HIT_RE.findall(body)]
    return {"status": "ok", "query": query, "titles": titles}


def check_record(rec: dict, plants: list[dict], others: list[tuple[str, str, dict]],
                 wiki: bool = True) -> dict:
    f = plant_fields(rec)
    cand = words(rec.get("plant_name"))
    country = ws(rec.get("country")).lower()
    state, county = ws(f.get(STATE_COL)).lower(), norm_county(f.get(COUNTY_COL))
    lat, lon = parse_coord(f.get("Latitude")), parse_coord(f.get("Longitude"))

    name_hits, nearby = [], []
    for p in plants:
        if country and p["country"].lower() != country:
            continue
        elsewhere = bool(state) and p["state"].lower() != state
        if any(cand == words(n) if elsewhere else names_match(cand, words(n)) for n in p["names"]):
            name_hits.append(brief(p))
        if lat is not None and lon is not None:
            d = distance_m(lat, lon, p["lat"], p["lon"])
            if d is not None and d <= NEARBY_KM * 1000:
                nearby.append(brief(p, km=round(d / 1000, 1)))
        elif county and p["county"] == county and p["state"].lower() == state:
            nearby.append(brief(p))
    nearby.sort(key=lambda x: x.get("km", 0))

    staged = []
    for lane, rid, o in others:
        if rid == rec.get("record_id") or lane not in STAGED_LANES:
            continue
        of = plant_fields(o)
        same_name = names_match(cand, words(o.get("plant_name")))
        same_county = lane == "newplants" and bool(county) and \
            norm_county(of.get(COUNTY_COL)) == county and ws(of.get(STATE_COL)).lower() == state
        if same_name or same_county:
            staged.append({"lane": lane, "record_id": rid, "plant_name": ws(o.get("plant_name")),
                           "why": "same name" if same_name else "same county"})

    out = {"plant_name": ws(rec.get("plant_name")), "fingerprint": fingerprint(rec),
           "words": sorted(cand), "point": [lat, lon] if lat is not None else None,
           "county": county, "state": state,
           "name": name_hits, "nearby": nearby, "staged": staged}
    if wiki:
        w = wiki_search(f'"{core_name(rec.get("plant_name"))}"')
        w["matches"] = [t for t in w["titles"] if names_match(cand, words(t))
                        and PLANT_WORDS & set(re.findall(r"[a-z]+", t.lower()))
                        and not NOT_COMBUSTION & set(re.findall(r"[a-z]+", t.lower()))]
        out["wiki"] = w
    else:
        out["wiki"] = {"status": "skipped", "titles": [], "matches": []}
    out["hits"] = len(name_hits) + len(nearby) + len(staged) + len(out["wiki"]["matches"])
    return out


def load_lane_records(staging: Path) -> list[tuple[str, str, dict]]:
    recs = []
    for p in sorted(staging.glob("staged_*.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        lane = p.stem.removeprefix("staged_")
        for i, r in enumerate(data.get("records") or []):
            recs.append((lane, r.get("record_id") or f"{lane}[{i}]", r))
    return recs


def run(batch: Path, csv_path: Path, wiki: bool = True) -> dict:
    staging = batch / "staging"
    allrecs = load_lane_records(staging) if staging.is_dir() else []
    new = [(rid, r) for lane, rid, r in allrecs if lane == "newplants"]
    plants = load_plants(csv_path) if new else []
    res = {"generated": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "export": str(csv_path), "nearby_km": NEARBY_KM, "records": {}}
    for rid, r in new:
        res["records"][rid] = check_record(r, plants, allrecs, wiki=wiki)
    return res


def plain(e: dict) -> list[str]:
    lines = [f"## {e['plant_name']}", ""]
    where = (f"within {NEARBY_KM} kilometers of its point" if e["point"]
             else f"in {e['county'].title() or 'an unknown'} county")
    if not e["hits"]:
        lines.append("No GEM plant of any fuel shares its name or sits " + where +
                     ". No other record in this batch overlaps it. gem.wiki shows no page with its name.")
        return lines + [""]
    for h in e["name"]:
        lines.append(f"- Same name: {h['plant_name']} ({', '.join(h['fuels']) or 'no fuel'}, "
                     f"{', '.join(h['statuses'])}), GEM location {h['gem_location_id']}.")
    for h in e["nearby"]:
        dist = f", {h['km']} km away" if "km" in h else ", same county"
        lines.append(f"- Nearby: {h['plant_name']} ({', '.join(h['fuels']) or 'no fuel'}, "
                     f"{', '.join(h['statuses'])}{dist}), GEM location {h['gem_location_id']}.")
    for s in e["staged"]:
        lines.append(f"- In this batch, {s['why']}: {s['plant_name']} ({s['record_id']}).")
    for t in e["wiki"]["matches"]:
        lines.append(f"- gem.wiki page with the same name: {t}. Check it, never cite it.")
    if e["wiki"]["status"] != "ok":
        lines.append("- The gem.wiki search did not run. Run this check again.")
    return lines + [""]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--csv", default=str(gem_export_csv()),
                    help="the UNFILTERED all-combustion export (default scripts/gem_export_gogpt.csv)")
    ap.add_argument("--no-wiki", action="store_true", help="skip the gem.wiki search (tests)")
    args = ap.parse_args()
    batch = Path(args.batch).resolve()
    res = run(batch, Path(args.csv), wiki=not args.no_wiki)
    (batch / DEDUP_FILE).write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n",
                                    encoding="utf-8")
    md = [f"# Duplicate check, {batch.name}", "",
          f"Run {res['generated'][:16].replace('T', ' ')} against every combustion plant in the export, any fuel. "
          "A plant with any line below needs an answer in coverage.json under dedup.", ""]
    for e in res["records"].values():
        md += plain(e)
    (batch / "dedup.md").write_text("\n".join(md), encoding="utf-8")
    hit = sum(1 for e in res["records"].values() if e["hits"])
    print(f"dedup_check: {len(res['records'])} new plants checked, {hit} with something to answer; "
          f"wrote {batch / DEDUP_FILE} and dedup.md")


if __name__ == "__main__":
    main()
