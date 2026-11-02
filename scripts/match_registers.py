"""Match a European country's GEM plants to the European registers: the European Environment Agency
large combustion plant table and, with a token, the ENTSO-E list of installed capacity per production
unit. The European counterpart of match_ids.py (which does EIA, EIP and Sierra Club for US states).

    python match_registers.py --country Poland
    python match_registers.py --country Poland --refresh        # download the registers again

Writes work/ids_<tag>.json and .md in the match_ids.py contract (`where`, `sources`, `tasks`,
`ids_to_add`, `leads`, `problems`), so build_state_brief.py --ids briefs it unchanged.

- European Environment Agency, industrial reporting version 16 (bulk CSV zip, cached in work/eea/):
  table F5_2 gives each large combustion plant part (50 MW thermal input or more) its thermal
  input in MW and its yearly fuel use in terajoules. A part that burned natural gas in the newest
  year is matched to a GEM plant by distance (3 km) or by name. An unmatched part named as a power
  or combined heat and power plant, burning mostly gas, is a lead. Heat-only boilers and gas
  compressor stations are listed apart and are not leads (no generation, or a mechanical drive).
  Thermal input is never an electrical capacity; it only sizes the lead.
- ENTSO-E (needs ENTSOE_API_TOKEN, kept outside the repo): installed capacity per production unit,
  gas and oil units. A unit whose EIC code is in GEM's Other IDs is compared on capacity (a
  difference of more than 10 percent is a task); a unit in no GEM row is a lead. Without the token
  this part is skipped and the .md says so.

Nothing here is cited. The registers point the agents at a plant; they cite the operator's,
regulator's or permit's own document.
"""
from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import math
import os
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import gogpt_scoped_csv, scope_tag, work_dir  # noqa: E402

EEA_ZIP_URL = "https://sdi.eea.europa.eu/datashare/public.php/webdav/User%20friendly%20.csv%20files.zip"
EEA_SHARE = "AnfiqFkZYBSq36B"
EEA_PAGE = "https://sdi.eea.europa.eu/datashare/s/AnfiqFkZYBSq36B"
ENTSOE_API = "https://web-api.tp.entsoe.eu/api"
ENTSOE_AREAS = {"poland": "10YPL-AREA-----S", "romania": "10YRO-TEL------P", "germany": "10Y1001A1001A83F",
                "united kingdom": "10YGB----------A", "ireland": "10YIE-1001A00010", "italy": "10YIT-GRTN-----B"}
ENTSOE_FUELS = {"B04": "fossil gas", "B05": "fossil hard coal", "B06": "fossil oil", "B03": "coal-derived gas"}
FUELS = ["Biomass", "Coal", "Lignite", "LiquidFuels", "NaturalGas", "OtherGases", "OtherSolidFuels", "Peat"]
POWER = re.compile(r"elektrociep|elektrown|\bec\b|\bchp\b|kogenera|power|kraftwerk|heizkraft|centrala|ccgt|ocgt|"
                   r"blok|turbin|silnik|engine|gazowo", re.I)
NOT_POWER = re.compile(r"tlocznia|gaz-system|compressor|verdicht|kotlownia|cieplownia(?!.*elektro)|heizwerk|rafineri|"
                       r"\bpiec\b|furnace|cracker|reformer", re.I)
MATCH_KM = 3.0


def fold(s) -> str:
    s = str(s or "").replace("ł", "l").replace("Ł", "L")
    s = unicodedata.normalize("NFKD", s)
    return re.sub(r"\s+", " ", "".join(c for c in s if not unicodedata.combining(c))).lower().strip()


def km(a, b, c, d):
    if None in (a, b, c, d) or any(isinstance(x, float) and math.isnan(x) for x in (a, b, c, d)):
        return None
    p = math.pi / 180
    h = math.sin((c - a) * p / 2) ** 2 + math.cos(a * p) * math.cos(c * p) * math.sin((d - b) * p / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))


# ------------------------------------------------------------------ GEM side ---

def load_plants(country, csv_path=None):
    d = pd.read_csv(csv_path or gogpt_scoped_csv(), low_memory=False, encoding="utf-8-sig")
    d = d[d["Country/Area"].str.lower() == country.lower()]
    plants = []
    for pid, rows in d.groupby("GEM location ID", sort=False):
        r = rows.iloc[0]
        eic = {}
        for _, u in rows.iterrows():
            for cell in (u.get("Other IDs (unit)"), u.get("Other IDs (location)")):
                for code in re.findall(r"ENTSO-E:\s*([0-9A-Z-]{16})", str(cell or "")):
                    eic[code] = u["GEM unit ID"] if cell is u.get("Other IDs (unit)") else None
        caps = pd.to_numeric(rows["Capacity (MW)"], errors="coerce")
        plants.append({"id": pid, "name": r["Plant name"], "city": r["City"] if isinstance(r["City"], str) else "",
                       "lat": pd.to_numeric(r["Latitude"], errors="coerce"),
                       "lon": pd.to_numeric(r["Longitude"], errors="coerce"),
                       "cap": float(caps.sum()) if caps.notna().any() else None,
                       "units": {u["GEM unit ID"]: {"name": u["Unit name"], "cap": pd.to_numeric(u["Capacity (MW)"], errors="coerce"),
                                                     "status": u["Status"]} for _, u in rows.iterrows()},
                       "eic": eic})
    return plants


def name_words(p):
    base = re.sub(r"\b(power station|power plant|chp|ccgt)\b", " ", fold(p["name"]))
    return {w for w in re.split(r"[^a-z0-9]+", base + " " + fold(p["city"])) if len(w) >= 5}


def nearest(plants, lat, lon, text):
    best = None
    for p in plants:
        d = km(lat, lon, p["lat"], p["lon"])
        if d is not None and d <= MATCH_KM and (best is None or d < best[1]):
            best = (p, d)
    if best:
        return best[0], f"{best[1]:.1f} km from the GEM point"
    t = fold(text)
    for p in plants:
        if any(re.search(rf"\b{re.escape(w)}\b", t) for w in name_words(p)):
            return p, "name or town matches, check the site"
    return None, None


# ------------------------------------------------------------------ EEA ---

def eea_zip(refresh):
    z = work_dir() / "eea" / "eea_v16.zip"
    if refresh or not z.exists():
        import requests
        z.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(EEA_ZIP_URL, auth=(EEA_SHARE, ""), timeout=600)
        r.raise_for_status()
        z.write_bytes(r.content)
    return z


def eea_parts(country, zpath):
    """One row per large combustion plant part of the country in its newest reporting year:
    {lcp_id, name, city, lat, lon, year, thermal_mw, fuels_tj{}, gas_share}."""
    with zipfile.ZipFile(zpath) as z:
        name = next(n for n in z.namelist() if n.startswith("F5_2_LCP"))
        d = pd.read_csv(io.BytesIO(z.read(name)), encoding="utf-8-sig", low_memory=False)
    d = d[d["countryName"].str.lower() == country.lower()]
    return parts_from_rows(d)


def parts_from_rows(d):
    out = []
    if d.empty:
        return out
    year = int(d["reportingYear"].max())
    d = d[d["reportingYear"] == year]
    for lcp, g in d.groupby("LCPInspireId", sort=False):
        r = g.iloc[0]
        val = {(t, u): float(v) for t, u, v in zip(g["featureType"], g["unit"], pd.to_numeric(g["featureValue"], errors="coerce").fillna(0))}
        fuels = {f: val.get((f, "TJ"), 0.0) for f in FUELS}
        total = sum(fuels.values())
        out.append({"lcp_id": lcp, "name": str(r["installationPartName"]), "city": str(r["City_Of_Facility"] or ""),
                    "lat": r["Latitude"], "lon": r["Longitude"], "year": year,
                    "thermal_mw": val.get(("LCPCharacteristics", "MW")),
                    "fuels_tj": {k: round(v, 1) for k, v in fuels.items() if v},
                    "gas_share": round(fuels["NaturalGas"] / total, 2) if total else 0.0})
    return out


def classify_part(part):
    """power (a power or combined heat and power plant), heat_only, mechanical (compressor
    stations and process furnaces) or unclear."""
    t = fold(part["name"])
    if NOT_POWER.search(t) and not re.search(r"elektrociep|elektrown", t):
        return "mechanical" if re.search(r"tlocznia|gaz-system|compressor|verdicht|rafineri|piec|furnace|cracker|reformer", t) else "heat_only"
    return "power" if POWER.search(t) else "unclear"


# ------------------------------------------------------------------ ENTSO-E ---

def entsoe_units(country, token, year):
    import requests
    area = ENTSOE_AREAS[country.lower()]
    out = []
    for psr in ("B04", "B06"):
        r = requests.get(ENTSOE_API, timeout=120, params={
            "securityToken": token, "documentType": "A71", "processType": "A33", "in_Domain": area,
            "psrType": psr, "periodStart": f"{year}01010000", "periodEnd": f"{year}01020000"})
        if r.status_code != 200:
            raise RuntimeError(f"ENTSO-E {psr}: HTTP {r.status_code} {r.text[:200]}")
        out += parse_entsoe(r.text, ENTSOE_FUELS[psr])
    return out


def parse_entsoe(xml, fuel):
    """Units from an installed-capacity-per-unit document: [{eic, name, mw, fuel}]. The unit code and
    name sit on the series or in its PowerSystemResources block; not yet checked against a live
    response (no token on 2026-10-29)."""
    out = []
    for ts in re.findall(r"<TimeSeries>(.*?)</TimeSeries>", xml, re.S):
        psr = re.search(r"<PowerSystemResources>(.*?)</PowerSystemResources>", ts, re.S)
        psr = psr[1] if psr else ""
        eic = re.search(r"<registeredResource\.mRID[^>]*>([^<]+)<", ts) or re.search(r"<mRID[^>]*>([^<]+)<", psr)
        name = re.search(r"<registeredResource\.name>([^<]+)<", ts) or re.search(r"<name>([^<]+)<", psr)
        mw = re.search(r"<nominalP[^>]*>([\d.]+)<", ts) or re.search(r"<quantity>([\d.]+)<", ts)
        if eic:
            out.append({"eic": eic[1].strip(), "name": (name[1] if name else "").strip(),
                        "mw": float(mw[1]) if mw else None, "fuel": fuel})
    return out


# ------------------------------------------------------------------ build ---

def build(country, plants, parts, units, today):
    tag = scope_tag(country=country)
    tasks, leads, problems, matches, set_aside = [], [], [], [], []
    for part in parts:
        if not part["fuels_tj"].get("NaturalGas"):
            continue
        kind = classify_part(part)
        p, how = nearest(plants, part["lat"], part["lon"], f"{part['name']} {part['city']}")
        line = {"lcp_id": part["lcp_id"], "name": part["name"], "city": part["city"], "year": part["year"],
                "thermal_mw": part["thermal_mw"], "gas_share": part["gas_share"], "kind": kind,
                "fuels_tj": part["fuels_tj"]}
        if p:
            matches.append(dict(line, plant_id=p["id"], plant=p["name"], how=how))
        elif kind in ("power", "unclear") and part["gas_share"] >= 0.3:
            leads.append({"source": "eea", "name": part["name"], "ids": part["lcp_id"], "county": part["city"],
                          "owner": "", "capacity_mw": None, "thermal_input_mw": part["thermal_mw"],
                          "status": f"reported to the EEA for {part['year']}", "kind": kind,
                          "basis": (f"the EEA large combustion plant table for {part['year']}: "
                                    f"{part['gas_share']:.0%} of fuel was natural gas, {part['thermal_mw'] or '?'} MW "
                                    "thermal input, no GEM plant within 3 km or by name"), "staged_in": []})
        else:
            set_aside.append(line)
    by_eic = {code: (p, uid) for p in plants for code, uid in p["eic"].items()}
    for u in units:
        hit = by_eic.get(u["eic"])
        if not hit:
            leads.append({"source": "entsoe", "name": u["name"], "ids": f"ENTSO-E: {u['eic']}", "county": "",
                          "owner": "", "capacity_mw": u["mw"], "status": "in the ENTSO-E installed capacity list",
                          "basis": f"the ENTSO-E unit list ({u['fuel']}): EIC code in no GEM row", "staged_in": []})
            continue
        p, uid = hit
        gem = p["units"].get(uid, {}).get("cap") if uid else p["cap"]
        if u["mw"] and gem and not math.isnan(gem) and abs(u["mw"] - gem) / gem > 0.10:
            unit = p["units"].get(uid, {}) if uid else {}
            tasks.append({"plant_id": p["id"], "plant_name": p["name"], "unit_id": uid, "unit_name": unit.get("name"),
                          "source": "entsoe", "section": "Capacity", "kind": "fix", "fields": ["Capacity (MW)"],
                          "confidence": "medium",
                          "task": (f"The ENTSO-E installed capacity list gives {u['name']} (code {u['eic']}) "
                                   f"{u['mw']:g} MW, while GEM has {gem:g} MW. Find the nameplate in an operator "
                                   "or regulator document and report it. ENTSO-E may list net or available "
                                   "capacity, so it is not cited for nameplate.")})
    return {"where": {"kind": "country", "name": country, "slug": tag}, "read": today,
            "sources": [], "plants_checked": len(plants), "tasks": tasks, "ids_to_add": [],
            "sheet_fills": {}, "leads": leads, "problems": problems,
            "eea_matches": matches, "eea_set_aside": set_aside}


def write(data, out_json, entsoe_note):
    out_json.write_text(json.dumps(data, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    c = data["where"]["name"]
    L = [f"# {c}: European register match ({data['read']})", "",
         "Nothing here is cited. Thermal input is never an electrical capacity.", "", "## Sources", ""]
    L += [f"- {s}" for s in data["sources"]] + [f"- {entsoe_note}", ""]
    L += ["## Possible plants GEM lacks", ""]
    L += [f"- {d['name']} ({d['county'] or 'town not shown'}; {d['ids']}): {d['basis']}." for d in data["leads"]] or ["None."]
    L += ["", "## Capacity disagreements", ""]
    L += [f"- {t['plant_name']} ({t['plant_id']}): {t['task']}" for t in data["tasks"]] or ["None, or ENTSO-E not read."]
    L += ["", "## Gas-burning combustion plants matched to GEM plants", ""]
    L += [f"- {m['plant']} ({m['plant_id']}): {m['name']}, {m['thermal_mw'] or '?'} MW thermal input, "
          f"{m['gas_share']:.0%} gas, {m['how']}." for m in sorted(data["eea_matches"], key=lambda x: x["plant"])] or ["None."]
    L += ["", "## Gas-burning combustion plants set aside (heat only, compressor stations, process plant, or under 30 percent gas)", ""]
    L += [f"- {m['name']} ({m['city']}): {m['kind'].replace('_', ' ')}, {m['thermal_mw'] or '?'} MW thermal input, "
          f"{m['gas_share']:.0%} gas." for m in data["eea_set_aside"]] or ["None."]
    out_json.with_suffix(".md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--country", required=True)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--csv")
    ap.add_argument("--out", help="output json (default work/ids_<tag>.json)")
    a = ap.parse_args()
    today = dt.date.today().isoformat()
    plants = load_plants(a.country, a.csv)
    if not plants:
        sys.exit(f"ERROR: no GEM plants for {a.country!r} in the scoped export")
    parts = eea_parts(a.country, eea_zip(a.refresh))
    token = os.environ.get("ENTSOE_API_TOKEN")
    units, note = [], "ENTSO-E unit list: not read, ENTSOE_API_TOKEN is not set."
    if token and a.country.lower() in ENTSOE_AREAS:
        units = entsoe_units(a.country, token, dt.date.today().year)
        note = f"ENTSO-E installed capacity per production unit for {dt.date.today().year}: {len(units)} gas and oil units ({ENTSOE_API})."
    data = build(a.country, plants, parts, units, today)
    yr = parts[0]["year"] if parts else "no year"
    data["sources"] = [f"EEA industrial reporting version 16, large combustion plant table, {yr}: "
                       f"{len(parts)} parts in {a.country} ({EEA_PAGE})"]
    out = Path(a.out) if a.out else work_dir() / f"ids_{data['where']['slug']}.json"
    write(data, out, note)
    print(f"{len(data['eea_matches'])} gas plant parts matched, {len(data['leads'])} leads, "
          f"{len(data['tasks'])} capacity tasks -> {out.with_suffix('.md')}")


if __name__ == "__main__":
    main()
