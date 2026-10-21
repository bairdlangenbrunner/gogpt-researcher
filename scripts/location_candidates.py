"""
Select the plants whose location is weak, for the location step (docs/reference/location.md).

    python location_candidates.py --state Kansas
    python location_candidates.py --country "Germany"
    python location_candidates.py --state Kansas --csv path/to/export.csv --allow-stale-export
    python location_candidates.py --country "Germany" --no-eia      # skip the EIA files (non-US or offline)

Reads the fresh scoped export (gogpt_scoped_csv(), refused when older than a day unless
--allow-stale-export). A plant is a candidate when the first row of the plant has Location
accuracy "approximate" (any case) or a blank Latitude or Longitude. A plant marked exact is
never selected, even when a dataset point disagrees with it. Scope matching: a state takes
United States rows whose State/Province equals the state; a country takes rows whose
Country/Area equals the country (both case-insensitive).

For each candidate it gathers the current point and its map links, the hosts in Location Data
Source, the place fields already filled, the EIA plant codes in Other IDs (location), and every
dataset point available with its distance from GEM's point: EIA-860M generator rows (one point
per distinct coordinate per plant code, from eia860m.py) and the EIA-860 annual Plant table
(address, county, coordinates, from eia860.py), both only for the United States and only with
EIA codes. Permit-portal hits join the list only when work/permits/<tag>/harvest_log.jsonl
records coordinates; harvest_permits.py currently records none in that log (it uses the portal
coordinates only to filter its search hits), so no permit points are read today and the code
skips them without complaint. Nearest is the dataset point with the smallest distance; far is
true when it is more than 2000 m away.

Writes work/location_<tag>.json (tag is us-<postal> for a state, the country slug otherwise)
and work/location_<tag>.md. The json has the shape build_state_brief.load_validation reads
(producer "location_candidates.py"): where, read, csv, sources, plants_checked, candidates,
tasks, problems. Each task is one plant, tagged checklist row 25, plus row 42 when the plant is
operating, and carries a "location" dict with the gathered facts. The brief builder adds the
map links from that dict.

Library use (no network, no freshness check):
    from location_candidates import select_candidates
    result = select_candidates(rows, scope, provider=None)   # provider(plant) -> [point dicts]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

import geo
from paths import gogpt_scoped_csv, require_fresh_export, work_dir
from build_state_brief import (H_COUNTY, H_LOC, H_MAJOR, H_PLANT, H_UNAME, H_UNIT, make_scope,
                               status_group)
from match_ids import tag_values

FAR_M = 2000
H_STATE = "State/Province"
H_COUNTRY = "Country/Area"
H_ACC = "Location accuracy"
H_LAT, H_LON = "Latitude", "Longitude"
H_LOCSRC = "Location Data Source"
H_OTHER = "Other IDs (location)"


def ws(v):
    return v.strip() if isinstance(v, str) else ("" if v is None else str(v).strip())


def tag_of(scope):
    return f"us-{scope['postal']}" if scope["kind"] == "state" else scope["slug"]


def in_scope(row, scope):
    if scope["kind"] == "state":
        return (ws(row.get(H_COUNTRY)).lower() == "united states"
                and ws(row.get(H_STATE)).lower() == scope["name"].lower())
    return ws(row.get(H_COUNTRY)).lower() == scope["name"].lower()


def hosts_of(cell):
    out = []
    for part in re.split(r"[,;]", ws(cell)):
        part = part.strip()
        if not part:
            continue
        host = urlparse(part if "://" in part else "//" + part).hostname
        if host and host not in out:
            out.append(host)
    return out


def words_distance(m):
    if m is None:
        return None
    return f"{m / 1000:.1f} km" if m >= 1000 else f"{int(round(m))} m"


def group_plants(rows, scope):
    plants = {}
    for r in rows:
        if not in_scope(r, scope):
            continue
        pid = ws(r.get(H_LOC))
        if not pid:
            continue
        plants.setdefault(pid, []).append(r)
    return plants


def is_candidate(first):
    lat, lon = geo.parse_coord(first.get(H_LAT)), geo.parse_coord(first.get(H_LON))
    return ws(first.get(H_ACC)).lower() == "approximate" or lat is None or lon is None


def _point(source, lat, lon, cur, address=None, county=None):
    lat, lon = geo.parse_coord(lat), geo.parse_coord(lon)
    if lat is None or lon is None:
        return None
    d = geo.distance_m(cur[0], cur[1], lat, lon) if cur[0] is not None and cur[1] is not None else None
    p = {"source": source, "lat": lat, "lon": lon,
         "distance_m": None if d is None else round(d), "links": geo.links_for(lat, lon)}
    if address is not None:
        p["address"] = address
        p["county"] = county or ""
    return p


def build_task_text(loc):
    cur = loc["current"]
    blank = cur["lat"] is None or cur["lon"] is None
    acc = cur["accuracy"] or "blank"
    if blank:
        parts = [f"GEM has no coordinate for this plant and the location accuracy is {acc}."]
    else:
        parts = [f"Location accuracy is {acc}. GEM's point is {geo.fmt5(cur['lat'])}, "
                 f"{geo.fmt5(cur['lon'])}."]
    parts.append("Find the plant's address or a sentence that places the site in a primary "
                 "document, turn it into a point, and check it in satellite imagery.")
    pts = loc["dataset_points"]
    if pts:
        for p in pts:
            where = f"{geo.fmt5(p['lat'])}, {geo.fmt5(p['lon'])}"
            dist = words_distance(p["distance_m"])
            tail = f", {dist} from GEM's point" if dist else ""
            if p.get("address") or p.get("county"):
                addr = p.get("address") or ""
                county = f", county {p['county']}" if p.get("county") else ""
                parts.append(f"The {p['source']} gives {addr}{county}, at {where}{tail}.")
            else:
                parts.append(f"The {p['source']} places it at {where}{tail}.")
    else:
        parts.append("No EIA or permit point is available.")
    parts.append("Stage new coordinates only when the point moves more than 500 m, fills a "
                 "blank, or becomes exact.")
    if loc["operating"]:
        parts.append("This plant is operating, so the satellite picture should show its "
                     "footprint. An exact location is wanted, checklist row 42.")
    return " ".join(parts)


def select_candidates(rows, scope, provider=None):
    """Pure selection. rows: dicts with the export headers. provider(plant) -> list of dataset
    point dicts {source, lat, lon, address?, county?}; distances and links are added here.
    Returns {"plants_checked", "candidates", "tasks", "problems"}."""
    plants = group_plants(rows, scope)
    tasks, problems = [], []
    for pid, prows in plants.items():
        first = prows[0]
        if not is_candidate(first):
            continue
        lat, lon = geo.parse_coord(first.get(H_LAT)), geo.parse_coord(first.get(H_LON))
        groups = sorted({status_group(r.get("Status")) for r in prows})
        codes = tag_values(first.get(H_OTHER), "EIA")
        plant = {"plant_id": pid, "plant_name": ws(first.get(H_PLANT)), "eia_codes": codes,
                 "lat": lat, "lon": lon}
        pts = []
        if provider:
            try:
                for raw in provider(plant) or []:
                    p = _point(raw["source"], raw.get("lat"), raw.get("lon"), (lat, lon),
                               raw.get("address"), raw.get("county"))
                    if p:
                        pts.append(p)
            except Exception as e:      # one bad lookup must not drop the plant
                problems.append(f"{pid}: dataset lookup failed: {e}")
        measured = [p for p in pts if p["distance_m"] is not None]
        nearest = min(measured, key=lambda p: p["distance_m"]) if measured else None
        loc = {"current": {"lat": lat, "lon": lon, "accuracy": ws(first.get(H_ACC)),
                           "links": geo.links_for(lat, lon),
                           "decimals": {"lat": geo.decimals(first.get(H_LAT)),
                                        "lon": geo.decimals(first.get(H_LON))}},
               "place": {"city": ws(first.get("City")), "county": ws(first.get(H_COUNTY)),
                         "major_area": ws(first.get(H_MAJOR)), "state": ws(first.get(H_STATE))},
               "location_hosts": hosts_of(first.get(H_LOCSRC)),
               "eia_codes": codes, "dataset_points": pts,
               "nearest": nearest,
               "far": bool(nearest and nearest["distance_m"] > FAR_M),
               "operating": "operating" in groups, "groups": groups,
               "unit_ids": [ws(r.get(H_UNIT)) for r in prows if ws(r.get(H_UNIT))]}
        tasks.append({"plant_id": pid, "plant_name": plant["plant_name"], "unit_id": None,
                      "unit_name": None, "source": "location_candidates", "section": "location",
                      "kind": "fix", "task": build_task_text(loc),
                      "fields": [H_LAT, H_LON, H_ACC],
                      "checks": [25, 42] if loc["operating"] else [25],
                      "confidence": "high", "location": loc})
    return {"plants_checked": len(plants), "candidates": len(tasks), "tasks": tasks,
            "problems": problems}


# ------------------------------------------------------------ dataset providers
def eia_provider(eia860m_path=None, eia860_zip=None, gens=None, idx860=None, year860=None):
    """A provider for select_candidates built from the EIA files. Pass loaded data (gens: the
    eia860m.load_generators frame, idx860: eia860.plant_index) or paths to load here."""
    m_name = Path(eia860m_path).name if eia860m_path else ""
    if gens is None and eia860m_path:
        import eia860m
        gens = eia860m.load_generators(eia860m_path)
    if idx860 is None and eia860_zip:
        import eia860
        idx860 = eia860.plant_index(eia860.load_plants(eia860_zip))
    by_code = defaultdict(list)
    if gens is not None and len(gens):
        seen = set()
        for r in gens.to_dict("records"):
            code = ws(r.get("Plant ID"))
            la, lo = geo.parse_coord(r.get("Latitude")), geo.parse_coord(r.get("Longitude"))
            if la is None or lo is None or (code, la, lo) in seen:
                continue
            seen.add((code, la, lo))
            by_code[code].append((la, lo))
    idx860 = idx860 or {}

    def provider(plant):
        out = []
        for code in plant["eia_codes"]:
            for la, lo in by_code.get(code, []):
                out.append({"source": f"EIA-860M {m_name}".strip(), "lat": la, "lon": lo})
            e = idx860.get(code)
            if e and e.get("lat") is not None and e.get("lon") is not None:
                addr = ", ".join(x for x in (e["address"], e["city"],
                                             " ".join(x for x in (e["state"], e["zip"]) if x)) if x)
                out.append({"source": f"EIA-860 {year860 or ''} Plant table".replace("  ", " "),
                            "lat": e["lat"], "lon": e["lon"], "address": addr,
                            "county": e["county"]})
        return out
    return provider


def permit_provider(tag):
    """Points from work/permits/<tag>/harvest_log.jsonl procedures that record lat and lon.
    Returns None when the folder is absent or holds no coordinates."""
    log = work_dir() / "permits" / tag / "harvest_log.jsonl"
    if not log.exists():
        return None
    latest = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        latest[d.get("plant")] = d
    pts = {pid: [{"source": f"permit {p.get('procedure') or p.get('uuid')}", "lat": p["lat"],
                  "lon": p["lon"]} for p in d.get("procedures", [])
                 if p.get("lat") is not None and p.get("lon") is not None]
           for pid, d in latest.items()}
    if not any(pts.values()):
        return None
    return lambda plant: pts.get(plant["plant_id"], [])


def combine(*providers):
    provs = [p for p in providers if p]
    if not provs:
        return None
    return lambda plant: [pt for p in provs for pt in p(plant)]


# ------------------------------------------------------------------ output
def memo(out):
    sc = out["where"]
    L = [f"# Location candidates for {sc['name']}", "",
         f"Read {out['read']}. Plants checked: {out['plants_checked']}. Plants with a weak or "
         f"missing location: {out['candidates']}.", ""]
    n_blank = sum(1 for t in out["tasks"] if t["location"]["current"]["lat"] is None
                  or t["location"]["current"]["lon"] is None)
    n_op = sum(1 for t in out["tasks"] if t["location"]["operating"])
    n_far = sum(1 for t in out["tasks"] if t["location"]["far"])
    L += [f"With no coordinate: {n_blank}. Operating: {n_op}. With a dataset point more than "
          f"2 km from GEM's point: {n_far}.", ""]
    src = out["sources"]
    L += [f"Sources: EIA-860M file {src['eia860m'] or 'not used'}, EIA-860 file "
          f"{src['eia860'] or 'not used'}.", ""]
    for t in out["tasks"]:
        loc = t["location"]
        near = loc["nearest"]
        bits = [f"{t['plant_name']} ({t['plant_id']})",
                f"accuracy {loc['current']['accuracy'] or 'blank'}",
                ", ".join(loc["groups"])]
        if near:
            bits.append(f"nearest dataset point {words_distance(near['distance_m'])} away "
                        f"({near['source']})")
            addr = next((p["address"] for p in loc["dataset_points"] if p.get("address")), "")
            if addr:
                bits.append(f"address {addr}")
        else:
            bits.append("no dataset point")
        L.append("- " + "; ".join(bits))
    L.append("")
    if out["problems"]:
        L += ["## Problems", ""] + [f"- {x}" for x in out["problems"]] + [""]
    return "\n".join(L)


def now_et():
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("America/New_York")).replace(microsecond=0).isoformat()
    except Exception:
        return dt.datetime.now().astimezone().replace(microsecond=0).isoformat()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--state", help="a US state, e.g. Kansas")
    g.add_argument("--country", help="a country, e.g. Germany")
    ap.add_argument("--csv", help="export to read (default: the scoped export)")
    ap.add_argument("--allow-stale-export", action="store_true")
    ap.add_argument("--no-eia", action="store_true", help="skip the EIA files")
    a = ap.parse_args()
    scope = make_scope(state=a.state, country=a.country)
    csv_path = Path(a.csv) if a.csv else gogpt_scoped_csv()
    require_fresh_export(csv_path, allow_stale=a.allow_stale_export)
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    sources = {"eia860m": None, "eia860": None}
    provs = []
    if scope["kind"] == "state" and not a.no_eia:
        import eia860m
        import eia860
        p_m, _ = eia860m.ensure_latest()
        z, meta = eia860.ensure_latest()
        sources = {"eia860m": Path(p_m).name, "eia860": Path(z).name}
        provs.append(eia_provider(eia860m_path=p_m, eia860_zip=z, year860=meta.get("year")))
    tag = tag_of(scope)
    provs.append(permit_provider(tag))
    res = select_candidates(rows, scope, combine(*provs))
    out = {"where": scope, "read": now_et(), "csv": str(csv_path), "sources": sources, **res}
    wd = work_dir()
    (wd / f"location_{tag}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False),
                                             encoding="utf-8")
    (wd / f"location_{tag}.md").write_text(memo(out), encoding="utf-8")
    print(f"{res['plants_checked']} plants checked, {res['candidates']} candidates; "
          f"wrote {wd / ('location_' + tag + '.json')} and .md")


if __name__ == "__main__":
    main()
