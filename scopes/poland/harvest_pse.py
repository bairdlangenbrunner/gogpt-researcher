"""Poland's grid and capacity market harvester: the PSE connection list and the capacity auction
results, matched to the GEM plants of Poland.

    python scopes/poland/harvest_pse.py --scope poland
    python scopes/poland/harvest_pse.py --scope poland --offline   # reparse the saved copies

Two sources, both read anonymously:

- PSE connection list (article 7 section 8l of the Energy Law): one XLSX of every project asking
  to connect to the PSE grid, sheet "Wykaz wspólny". The file name never changes, so each run
  saves a dated copy under scopes/poland/work/pse/. Gas type codes are BG (gas block), BGP
  (combined cycle), SG (gas engines) and JS (combustion unit); MIX and rows naming gas are kept too.
- Capacity market main auctions: one page per delivery year (aukcja-glowna-na-rok-dostaw-YYYY)
  links the results PDFs. The final file is "Ostateczne wyniki" from 2024 on and the URE
  president's "Informacja" before that. Rows give a unit code (JRM/601), new, upgraded or
  existing, the obligation in MW, contract years and the supplier. No fuel column, so a row is
  gas only when a name says so; a new unit on a contract of 15 years or more with no
  fuel shown is kept as a lead. Obligation MW are de-rated, never nameplate: they go into the
  status text, never into `mw`.

Writes batches/poland/harvest/queues.json in the contract build_state_brief.py --harvest reads
(entries with source, queue_id, fuel, facility_type, mw, status, queue_date, in_service, poi,
url, matched) and queues.md. Settings and hand-checked name patterns are in
scopes/poland/harvest_pse.json. Nothing here is cited; the agents read the source and cite it.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urljoin

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from harvest_lib import CSV, REPO  # noqa: E402
from paths import scope_work  # noqa: E402

HERE = Path(__file__).resolve().parent
SETTINGS = json.loads((HERE / "harvest_pse.json").read_text(encoding="utf-8"))
PSE = "https://www.pse.pl"
CONN_URL = PSE + "/documents/20182/51490/Informacje_publikowane_zgodnie_z_Art_7_ust_8l_ustawy_PE.xlsx"
AUCTION_INDEX = [PSE + "/aukcje-mocy", PSE + "/aukcje-mocy-archiwum"]
AUCTION_PAGE = PSE + "/aukcja-glowna-na-rok-dostaw-{year}"
YEARS = range(2021, 2031)

GAS_CODES = {"BG", "BGP", "SG", "JS"}
GAS_WORDS = re.compile(r"\bgaz|\bccgt\b|\bocgt\b|\bbgp\b|\bbg\b|gazowo|silnik|\bsg\b|kogenerac|\bchp\b", re.I)
NOT_GAS = re.compile(r"magazyn|\bbess\b|storage|\bpv\b|fotowolt|wiatr|\bfw\b|farma|\bdsr\b|odb\b|"
                     r"redukc|elektrolizer|wodn|biogaz|biomas|\boze\b|solar|energy storage", re.I)
STATUS_PL = {"WNIOSEK": "application", "WARUNKI": "connection conditions issued",
             "UMOWA": "connection agreement signed", "ODMOWA": "refused"}


def fold(s) -> str:
    """Lowercase with Polish letters folded to plain ones (ł has no decomposition)."""
    s = str(s or "").replace("ł", "l").replace("Ł", "L")
    s = unicodedata.normalize("NFKD", s)
    return re.sub(r"\s+", " ", "".join(c for c in s if not unicodedata.combining(c))).lower().strip()


def iso(v):
    if isinstance(v, (dt.date, dt.datetime)):
        return v.strftime("%Y-%m-%d")
    m = re.fullmatch(r"(\d{2})\.(\d{2})\.(\d{4})", str(v or "").strip())
    return f"{m[3]}-{m[2]}-{m[1]}" if m else None


def installed(v):
    """Installed MW from the other-installed column, where a block pair reads '2x915'."""
    m = re.fullmatch(r"\s*(\d+)\s*[x×]\s*(\d+(?:[.,]\d+)?)\s*", str(v or ""))
    return int(m[1]) * float(m[2].replace(",", ".")) if m else num(v)


def num(v):
    """A number from a cell: 47.681, '279,99972E', '-' -> 47.681, 279.99972, None."""
    if isinstance(v, (int, float)):
        return float(v)
    m = re.search(r"\d[\d ]*(?:[.,]\d+)?", str(v or ""))
    return float(m[0].replace(" ", "").replace(",", ".")) if m else None


# ------------------------------------------------------- connection list ---

def conn_entries(rows, url=CONN_URL):
    """Gas rows of the connection list. `rows` are the sheet's value tuples from the header row on."""
    out = []
    for r in rows:
        r = list(r) + [None] * 27
        oid, name, applicant, station, kind = r[0], r[1], r[3], r[4], str(r[7] or "").strip().upper()
        if not name or kind == "" or str(name).startswith("Nazwa"):
            continue
        text = f"{name} {applicant}"
        gas = kind in GAS_CODES or (kind == "MIX" and GAS_WORDS.search(text)) or (
            kind not in {"PV", "FW", "MEE", "ODB", "OSD", "JW"} and GAS_WORDS.search(text) and not NOT_GAS.search(text))
        if not gas:
            continue
        stage = str(r[16] or "")
        status = next((v for k, v in STATUS_PL.items() if stage.upper().startswith(k)), stage)
        dates = {"conditions": iso(r[19]), "agreement": iso(r[23]), "supply_start": iso(r[24]),
                 "expired": iso(r[22]) or iso(r[26]), "refused": iso(r[20])}
        out.append({
            "source": "pse-8l", "queue_id": str(oid) if oid and oid != "-" else f"pse-8l:{fold(name)}",
            "project_name": clean(name), "owner": clean(applicant), "fuel": "gas",
            "facility_type": {"BG": "gas block", "BGP": "combined cycle", "SG": "gas engines",
                              "JS": "combustion unit", "MIX": "mixed"}.get(kind, kind),
            "mw": num(r[8]) or installed(r[15]), "status": f"{status} ({stage})" if stage else status,
            "queue_date": iso(r[17]), "in_service": dates["supply_start"], "poi": clean(station),
            "county": None, "dates": {k: v for k, v in dates.items() if v}, "url": url,
            "gas_oil": True, "fuel_unknown": False})
    return out


def read_conn(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["Wykaz wspólny"] if "Wykaz wspólny" in wb.sheetnames else wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    head = next(i for i, r in enumerate(rows) if r and str(r[0] or "").startswith("ID Obiektu"))
    stand = re.search(r"Stan na (\d{2}\.\d{2}\.\d{4})", str(rows[0][0] or ""))
    return rows[head + 1:], iso(stand[1]) if stand else None


def clean(s):
    return re.sub(r"\s+", " ", str(s or "")).strip() or None


# ------------------------------------------------------ capacity auctions ---

ROW = re.compile(r"^\s*\d+\.\s+(JRM/\d+)\b(.*)$")
OBL = re.compile(r"(?<![\d,])(\d{1,3}(?: \d{3})*,\d{3})\s+(\d{1,2})(?:\s+(.*))?$")
TYPE = re.compile(r"\b(nowa|modernizowana|istniej[aą]ca)\b", re.I)
TYPES = {"nowa": "new unit", "modernizowana": "upgraded unit", "istniejaca": "existing unit"}
FOREIGN = re.compile(r"\b(CZ|SK|DE|LT|SE)\d{6,}")


def auction_rows(text, year, url):
    """One dict per JRM row of a results PDF's text (pdftotext -layout). Layouts differ by year:
    the type sits on the row or on the line above it, and from 2028 a unit name follows the code."""
    lines = text.splitlines()
    out = []
    prev_row = -1
    for i, line in enumerate(lines):
        m = ROW.match(line)
        if not m:
            continue
        code, rest = m[1], m[2]
        o = OBL.search(rest)
        if not o:
            prev_row = i
            continue
        obligation = float(o[1].replace(" ", "").replace(",", "."))
        years = int(o[2])
        tail = (o[3] or "").strip()
        nip = re.search(r"(\S+)\s*$", tail)
        supplier = clean(tail[: nip.start()] if nip and re.search(r"\d{6,}", nip[1]) else tail)
        head = rest[: o.start()]
        t = TYPE.search(head)
        if not t:   # the type wraps onto the line above (2028 and 2029) or below (2021)
            for j in [i - 1, i + 1, i - 2]:
                if 0 <= j < len(lines) and j != prev_row and not ROW.match(lines[j]):
                    t = TYPE.search(lines[j])
                    if t:
                        break
        kind = TYPES.get(fold(t[1])) if t else None
        name = clean(TYPE.split(head)[0] if t and t.start() > 0 and TYPE.search(head) else head)
        if name and re.fullmatch(r"(jednostka rynku mocy|mocy)?\s*wytw[oó]rcza", name, re.I):
            name = None
        out.append({"code": code, "year": year, "name": name, "kind": kind, "obligation": obligation,
                    "years": years, "supplier": supplier, "foreign": bool(FOREIGN.search(line)), "url": url})
        prev_row = i
    return out


def auction_entries(rows):
    """Queue entries for new or upgraded units on contracts of 5 years or more that a name shows to be
    gas, plus new units on 15 to 17 year contracts with no fuel shown (kept as leads). Existing units
    on one-year contracts are the operating fleet and are left out."""
    out = []
    for r in rows:
        if r["foreign"]:
            continue
        if r["kind"] == "existing unit" or r["years"] < 5:
            continue
        text = f"{r['name'] or ''} {r['supplier'] or ''}"
        gas = bool(GAS_WORDS.search(text))
        if NOT_GAS.search(text) and not gas:
            continue
        if not gas and (r["obligation"] < 10 or r["kind"] == "upgraded unit" or r["years"] < 15):
            continue   # five-year upgrades with no fuel shown are the coal fleet's retrofits
        out.append({
            "source": f"pse-auction-{r['year']}", "queue_id": f"{r['code']} ({r['year']})",
            "project_name": r["name"] or r["supplier"], "owner": r["supplier"],
            "fuel": "gas" if gas else None, "facility_type": r["kind"] or "unit type not shown",
            "mw": None, "obligation_mw": r["obligation"], "contract_years": r["years"],
            "status": (f"capacity contract for delivery year {r['year']}, {r['years']} years, "
                       f"obligation {r['obligation']:g} MW (de-rated, not nameplate)"),
            "queue_date": None, "in_service": str(r["year"]), "poi": None, "county": None,
            "url": r["url"], "gas_oil": gas, "fuel_unknown": not gas})
    return out


def auction_links(html, page_url):
    """Final-results PDF links on one delivery-year page (preliminary files are skipped when a final
    one is there)."""
    hrefs = [urljoin(page_url, h) for h in re.findall(r'href="([^"]*/documents/20182/\d+/[^"]+)"', html)]
    hrefs = [h for h in dict.fromkeys(hrefs) if not re.search(r"instrukcj|regulamin", h, re.I)]
    final = [h for h in hrefs if re.search(r"ostateczn|informacj|/wyniki", fold(h.replace("+", " ")))]
    return final or hrefs


# ----------------------------------------------------------------- match ---

def load_plants(csv_path=None):
    import pandas as pd
    d = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    d = d[d["Country/Area"] == SETTINGS["name"]]
    plants = []
    for pid, rows in d.groupby("GEM location ID", sort=False):
        r = rows.iloc[0]
        city = r.get("City") if isinstance(r.get("City"), str) else ""
        plants.append({"id": pid, "name": r["Plant name"], "city": city,
                       "known": SETTINGS["known"].get(pid, [])})
    return plants


def town_words(p):
    words = {fold(p["city"])} | {fold(re.sub(r"\s*power station$", "", p["name"], flags=re.I))}
    return {w for w in words if len(w) >= 4 and w not in {"warszawa", "warsaw"}}


def match_entry(plant, e):
    text = fold(f"{e.get('project_name')} {e.get('owner')} {e.get('poi')}")
    if any(re.search(p, text) for p in plant["known"]):
        return "name, applicant or station matches the plant"
    if any(re.search(rf"\b{re.escape(w)}\b", text) for w in town_words(plant)):
        return "same town, check it is this plant"
    return None


def match_all(plants, entries):
    by_plant = {p["id"]: [] for p in plants}
    matched = set()
    for i, e in enumerate(entries):
        e["matched"] = []
        hits = [(p, match_entry(p, e)) for p in plants]
        hits = [(p, how) for p, how in hits if how]
        if any(not how.startswith("same town") for _, how in hits):
            hits = [(p, how) for p, how in hits if not how.startswith("same town")]
        for p, how in hits:
            e["matched"].append({"plant_id": p["id"], "plant": p["name"], "how": how})
            by_plant[p["id"]].append(i)
            matched.add(i)
    return by_plant, matched


# ---------------------------------------------------------------- output ---

def entry_line(e):
    bits = [f"{e['source']} {e['queue_id']}", e.get("project_name"), e.get("fuel") or "fuel not shown",
            e.get("facility_type"), f"{e['mw']:g} MW installed" if e.get("mw") else "", e.get("status"),
            f"applied {e['queue_date']}" if e.get("queue_date") else "",
            f"connection station {e['poi']}" if e.get("poi") else "", e.get("owner")]
    return "; ".join(b for b in bits if b)


def write_outputs(out_dir, plants, entries, by_plant, matched, sources, today):
    out_dir.mkdir(parents=True, exist_ok=True)
    unmatched = [e for i, e in enumerate(entries) if e["gas_oil"] and i not in matched]
    unknown = [e for i, e in enumerate(entries) if e["fuel_unknown"] and i not in matched]
    data = {"generated": today, "sources": sources, "entries": entries,
            "by_plant": {pid: [entries[i]["queue_id"] for i in ix] for pid, ix in by_plant.items() if ix},
            "unmatched_gas_oil": [e["queue_id"] for e in unmatched],
            "hidden_fuel_leads": [e["queue_id"] for e in unknown]}
    (out_dir / "queues.json").write_text(json.dumps(data, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    L = [f"# Poland grid connection list and capacity auctions ({today})", "",
         "A connection request or a capacity contract is a lead, not proof that a plant exists or will be built. "
         "Capacity auction megawatts are de-rated obligations, never nameplate capacity.", "", "## Sources", ""]
    L += [f"- {s['name']}: {s['how']} ({s['url']})" for s in sources]
    L += ["", "## Matched to GEM plants", ""]
    for p in plants:
        ix = by_plant.get(p["id"], [])
        if ix:
            L.append(f"### {p['name']} ({p['id']}), {p['city'] or 'town not shown'}")
            L.append("")
            for i in ix:
                how = next(m["how"] for m in entries[i]["matched"] if m["plant_id"] == p["id"])
                L.append(f"- {entry_line(entries[i])} ({how}). Source: {entries[i]['url']}")
            L.append("")
    L += ["## Gas entries that match no GEM plant (possible new plants)", ""]
    L += [f"- {entry_line(e)}. Source: {e['url']}" for e in unmatched] or ["None."]
    L += ["", "## New or upgraded capacity units with no fuel shown and no GEM match", "",
          "Check each supplier's unit before ruling it out; many are batteries or demand response.", ""]
    L += [f"- {entry_line(e)}" for e in sorted(unknown, key=lambda x: -x["obligation_mw"])] or ["None."]
    (out_dir / "queues.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return data


# ------------------------------------------------------------------- run ---

def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True).stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", default="poland")
    ap.add_argument("--out", help="output folder (default batches/<scope>/harvest)")
    ap.add_argument("--offline", action="store_true", help="reparse the saved copies, no network")
    ap.add_argument("--csv", help="scoped export (default the repo's)")
    a = ap.parse_args()
    today = dt.date.today().isoformat()
    work = scope_work(a.scope) / "pse"
    (work / "auctions").mkdir(parents=True, exist_ok=True)

    if not a.offline:
        import requests
        s = requests.Session()
        s.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"
        r = s.get(CONN_URL, timeout=120)
        r.raise_for_status()
        (work / f"connection_list_{today.replace('-', '')}.xlsx").write_bytes(r.content)
        for year in YEARS:
            page = AUCTION_PAGE.format(year=year)
            h = s.get(page, timeout=60)
            if h.status_code != 200:
                print(f"auction page {year}: HTTP {h.status_code}")
                continue
            for k, link in enumerate(auction_links(h.text, page)):
                f = work / "auctions" / f"{year}_{k}.pdf"
                if not f.exists():
                    f.write_bytes(s.get(link, timeout=120).content)
                (work / "auctions" / f"{year}_{k}.url").write_text(link)

    conn = sorted(work.glob("connection_list_*.xlsx"))
    if not conn:
        sys.exit(f"ERROR: no saved connection list in {work}; run without --offline")
    rows, stand = read_conn(conn[-1])
    entries = conn_entries(rows)
    sources = [{"name": f"PSE connection list, state of {stand or 'date not shown'}",
                "how": f"saved copy {conn[-1].name}, gas type codes and gas names kept", "url": CONN_URL}]
    seen = set()
    for f in sorted((work / "auctions").glob("*.pdf")):
        year = int(f.name[:4])
        url = (f.with_suffix(".url").read_text().strip() if f.with_suffix(".url").exists() else AUCTION_PAGE.format(year=year))
        for e in auction_entries(auction_rows(pdf_text(f), year, url)):
            if e["queue_id"] not in seen:
                seen.add(e["queue_id"])
                entries.append(e)
        sources.append({"name": f"PSE capacity market main auction for {year}", "how": f"results PDF {f.name}", "url": url})
    plants = load_plants(a.csv)
    by_plant, matched = match_all(plants, entries)
    out = Path(a.out) if a.out else REPO / "batches" / a.scope / "harvest"
    data = write_outputs(out, plants, entries, by_plant, matched, sources, today)
    print(f"{len(entries)} entries ({sum(e['source'] == 'pse-8l' for e in entries)} connection list), "
          f"{len(matched)} matched, {len(data['unmatched_gas_oil'])} gas unmatched, "
          f"{len(data['hidden_fuel_leads'])} fuel-unknown leads -> {out / 'queues.md'}")


if __name__ == "__main__":
    main()
