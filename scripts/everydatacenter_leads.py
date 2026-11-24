#!/usr/bin/env python3
"""
Lead list from the US AI Data Center Atlas (everydatacenter.com): every campus
the atlas says is not grid-only, checked against the GEM export.

The atlas's terms forbid scraping without written permission. Baird has that
permission (2026-11-09) for this use: a lead list for GOGPT discovery. The
downloaded pages and every output stay in the gitignored
work/everydatacenter/ folder and are never committed or shared, because the
permission is to use the data, not to republish it. The atlas is never a
citation either: each lead is researched from the primary records its page
links to (permits, filings, company statements), like any other lead site.

    python everydatacenter_leads.py [--csv gem_export_gogpt.csv] [--include-unknown]
                                    [--refresh] [--delay 4] [--limit N]

Steps
  1. Read the campus list embedded in the atlas homepage and keep the
     campuses whose power type is one of: grid plus an on-site gas bridge,
     on-site gas as primary supply, grid plus on-site prime generation,
     behind the meter other. --include-unknown adds "Unknown".
  2. Fetch each campus page, a few seconds apart, and keep it for a week in
     work/everydatacenter/pages/ (--refresh fetches again).
  3. Read the address, county, power figures, technology, operator, stage and
     the atlas's evidence lines about on-site power with their source links.
  4. Check each campus against the UNFILTERED export (any fuel), same state:
       name    the campus name and a GEM plant name share distinctive words
               (dedup_check.words / names_match, state names and place words
               dropped). One shared word counts only when the GEM plant is a
               data center plant or not yet operating; otherwise it is listed
               as "one shared name word, an older plant"
       owner   a distinctive word of the atlas operator appears in the plant's
               Owner(s) or Operator(s), and the plant is in the same county
               or city, or is not yet operating
       place   same county or city, and the plant's name or notes say data
               center
     Verdict: "likely in GEM" (a name hit, or an owner hit in the same place),
     "check by hand" (any other hit), "not found". GEM plants not yet
     operating in the same county or city are listed as nearby context only.

Writes work/everydatacenter/leads.json, leads.csv and leads.md (not found
first). Nothing is staged: a lead becomes a newplants record only after the
Discovery SOP's research and dedup_check.py.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bs4 import BeautifulSoup  # noqa: E402
from dedup_check import NAME_COLS, COUNTY_COL, STATE_COL, names_match, norm_county, words, ws  # noqa: E402
from paths import US_POSTAL, gem_export_csv, work_dir  # noqa: E402

BASE = "https://everydatacenter.com/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Global Energy Monitor research"
CACHE_DAYS = 7

# Field positions in the homepage's MAPD campus rows (from the page's own map script).
ST, NM, SL, MW, PW, TC, OPR = 2, 3, 4, 11, 13, 14, 19
POWER = {0: "Grid only", 1: "Grid + on-site gas bridge", 2: "On-site gas as primary supply",
         3: "Grid + on-site prime generation", 4: "Behind the meter, other", 5: "Unknown"}
TECH = {0: "Gas turbines", 1: "Reciprocating engines", 2: "Fuel cells", 3: "Mixed",
        4: "Other (steam or coal plant)", 5: "Not stated", -1: "Not stated"}
KEEP = (1, 2, 3, 4)
NOT_BUILT = {"announced", "pre-construction", "construction", "shelved", "shelved - inferred 2 y"}
OWNER_GENERIC = {"data", "center", "centers", "campus", "llc", "inc", "corp", "group", "holdings",
                 "energy", "power", "partners", "development", "digital", "technologies",
                 "technology", "infrastructure", "capital", "company", "the", "and", "ventures"}
POSTAL_NAME = {v: k.title() for k, v in US_POSTAL.items()}
# State names and common place words say where a campus is, not which plant it is.
PLACE_WORDS = {w for k in US_POSTAL for w in k.split()} | {
    "north", "south", "east", "west", "southeast", "northeast", "southwest", "northwest",
    "upper", "lower", "lake", "river", "valley", "ranch", "park", "creek", "site", "township",
    "expansion", "project", "technology", "industrial", "compute", "hyperscale"}

OUT = work_dir() / "everydatacenter"
PAGES = OUT / "pages"


def log(msg: str) -> None:
    print(f"[edc] {msg}", file=sys.stderr, flush=True)


def get(url: str, cache: Path | None, refresh: bool, delay: float) -> str:
    if cache and cache.exists() and not refresh and \
            time.time() - cache.stat().st_mtime < CACHE_DAYS * 86400:
        return cache.read_text(encoding="utf-8")
    time.sleep(delay)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read().decode("utf-8", "replace")
    if cache:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(body, encoding="utf-8")
    return body


def campus_list(home: str) -> list[list]:
    i = home.find("var MAPD=")
    if i < 0:
        sys.exit("The atlas homepage no longer carries the MAPD campus list; the page layout changed.")
    data, _ = json.JSONDecoder().raw_decode(home[i + len("var MAPD="):])
    return data["c"]


def text(el) -> str:
    return ws(el.get_text(" ")) if el else ""


def parse_page(page: str) -> dict:
    soup = BeautifulSoup(page, "html.parser")
    desc = (soup.find("meta", attrs={"name": "description"}) or {}).get("content", "")
    m = re.search(r"for this AI data center in (.+?)\.?$", html.unescape(desc))
    address = ws(m.group(1)) if m else ""
    cm = re.search(r"([A-Z][\w.'\- ]+? (?:County|Parish|Borough))", address)
    county = norm_county(cm.group(1)) if cm else ""
    pre = address.split(cm.group(1))[0] if cm else ""
    city = ws(pre.rstrip(", ").split(",")[-1]) if pre.strip(", ") else ""
    pow_el = soup.select_one(".c3-pow")
    stage = re.search(r"Step (\d) of 8: ([^.\n]+)", soup.get_text("\n"))
    lines = []
    for li in soup.select("li[data-t]"):
        divs = li.find_all("div", recursive=False)
        claim = text(divs[0]) if divs else ""
        if not re.match(r"On-site|Behind|Bridge|Prime|Generation|Turbine|Engine|Fuel cell|Air permit|Power|Grid|Utility|Interconnection|Electric|Load|Substation|Gas",
                        claim, re.I):
            continue
        quote = text(li.select_one(".q"))
        links = [a.get("href") for a in li.select("a.src") if a.get("href", "").startswith("http")]
        lines.append({"claim": claim, "quote": quote, "kind": li.get("data-t", ""), "links": links})
    return {
        "address": address, "county": county, "city": city,
        "power_figures": text(pow_el.select_one(".x-s")) if pow_el else "",
        "power_note": text(pow_el.select_one(".v4-tip")) if pow_el else "",
        "stage": f"{stage.group(1)} of 8, {html.unescape(ws(stage.group(2)))}" if stage else "",
        "evidence": lines,
    }


def load_gem(csv_path: Path) -> list[dict]:
    plants: dict[str, dict] = {}
    with open(csv_path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if ws(row.get("Country/Area")) != "United States":
                continue
            lid = ws(row.get("GEM location ID"))
            if not lid:
                continue
            p = plants.setdefault(lid, {
                "gem_location_id": lid, "plant_name": ws(row.get("Plant name")),
                "state": ws(row.get(STATE_COL)), "county": norm_county(row.get(COUNTY_COL)),
                "city": ws(row.get("City")).lower(), "names": set(), "owners": "",
                "statuses": set(), "fuels": set(), "mw": 0.0, "dc": False})
            for c in NAME_COLS:
                for n in re.split(r"[;,]\s*", ws(row.get(c))):
                    if n:
                        p["names"].add(n)
            p["owners"] += " " + ws(row.get("Owner(s)")) + " " + ws(row.get("Operator(s)"))
            p["statuses"].add(ws(row.get("Status")))
            if ws(row.get("Fuel")):
                p["fuels"].add(ws(row.get("Fuel")).split(":")[0])
            try:
                p["mw"] += float(row.get("Capacity (MW)") or 0)
            except ValueError:
                pass
            blob = f"{row.get('Plant name')} {row.get('Other Name(s)')} {row.get('Notes')}".lower()
            p["dc"] = p["dc"] or "data center" in blob or "data centre" in blob
    for p in plants.values():
        p["owner_words"] = {w for w in re.findall(r"[a-z0-9]+", p["owners"].lower())
                            if len(w) > 2 and w not in OWNER_GENERIC}
    return list(plants.values())


def short(p: dict, why: str) -> dict:
    return {"gem_location_id": p["gem_location_id"], "plant_name": p["plant_name"],
            "status": ", ".join(sorted(s for s in p["statuses"] if s)),
            "fuel": ", ".join(sorted(p["fuels"])), "mw": round(p["mw"], 1),
            "county": p["county"], "why": why}


def match(c: dict, gem: list[dict]) -> tuple[str, list[dict]]:
    state = POSTAL_NAME.get(c["state"], c["state"]).lower()
    cand = words(c["name"]) - PLACE_WORDS
    opw = {w for w in re.findall(r"[a-z0-9]+", c["operator"].lower())
           if len(w) > 2 and w not in OWNER_GENERIC}
    hits, nearby, strong = [], [], False
    for p in gem:
        if p["state"].lower() != state:
            continue
        same_place = bool(c["county"] and p["county"] == c["county"]) or \
            bool(c["city"] and p["city"] == c["city"].lower())
        not_built = bool(p["statuses"] & NOT_BUILT)
        shared = max((len(cand & words(n)) for n in p["names"]
                      if cand and names_match(cand, words(n))), default=0)
        if shared >= 2 or (shared and (p["dc"] or not_built)):
            hits.append(short(p, "name"))
            strong = True
        elif shared:
            hits.append(short(p, "one shared name word, an older plant"))
        elif opw and opw & p["owner_words"] and (same_place or not_built):
            hits.append(short(p, "owner, same place" if same_place else "owner, not yet operating"))
            strong = strong or same_place
        elif same_place and p["dc"]:
            hits.append(short(p, "same county or city, a data center plant"))
        elif same_place and not_built:
            nearby.append(short(p, "same county or city, not yet operating"))
    if not hits:
        return "not found", hits, nearby
    return ("likely in GEM" if strong else "check by hand"), hits, nearby


def write_md(rows: list[dict], path: Path, csv_path: Path) -> None:
    order = {"not found": 0, "check by hand": 1, "likely in GEM": 2}
    rows = sorted(rows, key=lambda r: (order[r["verdict"]], r["state"], -(r["planned_it_mw"] or 0)))
    out = [f"# Atlas campuses with on-site power, checked against GEM",
           "",
           f"Built {datetime.date.today()} from everydatacenter.com and the GEM export {csv_path.name} "
           f"(pulled {datetime.date.fromtimestamp(csv_path.stat().st_mtime)}). "
           "Private working file: never commit or share it. The atlas is a lead list, never a citation.",
           ""]
    for v in ("not found", "check by hand", "likely in GEM"):
        part = [r for r in rows if r["verdict"] == v]
        out += [f"## {v.capitalize()} ({len(part)})", ""]
        for r in part:
            out.append(f"### {r['name']} ({r['state']})")
            out.append(f"- Atlas page: {r['url']}")
            out.append(f"- Where: {r['address'] or 'not given'}")
            out.append(f"- Power: {r['power']}. {r['power_figures']}. Technology: {r['technology']}.")
            out.append(f"- Operator: {r['operator'] or 'not named'}. Stage: {r['stage'] or 'not given'}. "
                       f"Planned computing load: {r['planned_it_mw'] or 'not given'} MW.")
            for h in r["gem_hits"]:
                out.append(f"- GEM: {h['plant_name']} ({h['gem_location_id']}), {h['status']}, "
                           f"{h['fuel']}, {h['mw']} MW. Matched on {h['why']}.")
            if r["gem_nearby"]:
                out.append("- GEM plants not yet operating in the same county or city: " + "; ".join(
                    f"{h['plant_name']} ({h['status']}, {h['mw']} MW)" for h in r["gem_nearby"][:8]))
            for e in r["evidence"][:6]:
                out.append(f"- Atlas says: {e['claim']}" + (f" Sources: {' '.join(e['links'])}" if e["links"] else ""))
            out.append("")
    path.write_text("\n".join(out), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--csv", type=Path, default=gem_export_csv(), help="unfiltered GEM export")
    ap.add_argument("--include-unknown", action="store_true", help="also keep power type Unknown")
    ap.add_argument("--refresh", action="store_true", help="fetch pages again even if cached")
    ap.add_argument("--delay", type=float, default=4.0, help="seconds between page fetches")
    ap.add_argument("--limit", type=int, default=0, help="stop after N campuses (testing)")
    a = ap.parse_args()

    keep = KEEP + ((5,) if a.include_unknown else ())
    home = get(BASE, PAGES / "_home.html", a.refresh, 0)
    rows = [c for c in campus_list(home) if c[PW] in keep]
    if a.limit:
        rows = rows[: a.limit]
    log(f"{len(rows)} campuses with power types {', '.join(POWER[k] for k in keep)}")
    gem = load_gem(a.csv)
    log(f"{len(gem)} US plants in {a.csv.name}")

    out = []
    for k, c in enumerate(rows, 1):
        url = f"{BASE}{c[SL]}.html"
        try:
            info = parse_page(get(url, PAGES / f"{c[SL]}.html", a.refresh, a.delay))
        except Exception as e:  # noqa: BLE001 - one bad page should not stop the run
            log(f"  {url}: {e}")
            info = {"address": "", "county": "", "city": "", "power_figures": "", "power_note": "",
                    "stage": "", "evidence": [], "error": str(e)[:200]}
        r = {"name": c[NM], "state": c[ST], "url": url, "operator": c[OPR] or "",
             "power": POWER.get(c[PW], str(c[PW])), "technology": TECH.get(c[TC], str(c[TC])),
             "planned_it_mw": c[MW] or None, **info}
        r["verdict"], r["gem_hits"], r["gem_nearby"] = match(r, gem)
        out.append(r)
        if k % 10 == 0:
            log(f"  {k}/{len(rows)}")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "leads.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    with open(OUT / "leads.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["verdict", "name", "state", "county", "city", "power", "power_figures", "technology",
                    "operator", "stage", "planned_it_mw", "gem_matches", "gem_nearby", "url"])
        for r in out:
            w.writerow([r["verdict"], r["name"], r["state"], r["county"], r["city"], r["power"],
                        r["power_figures"], r["technology"], r["operator"], r["stage"], r["planned_it_mw"],
                        "; ".join(f"{h['plant_name']} ({h['why']})" for h in r["gem_hits"]),
                        "; ".join(h["plant_name"] for h in r["gem_nearby"]), r["url"]])
    write_md(out, OUT / "leads.md", a.csv)
    counts = {v: sum(r["verdict"] == v for r in out) for v in ("not found", "check by hand", "likely in GEM")}
    log(f"done: {counts}. Files in {OUT}")


if __name__ == "__main__":
    main()
