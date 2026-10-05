"""
Harvest German environmental impact assessment files before a research sweep.

The national register (uvp-verbund.de) and the state front ends share one
server that answers "429 Too Many Requests" to most requests whatever the
pace. Research subagents hitting it in parallel get almost nothing. This
script does the slow part once, in one patient queue, ahead of the sweep:

  1. For each plant, search the register by town and plant name.
  2. Keep procedures whose title looks like a gas or power plant project.
     The register's search only lists procedures still in its index. A closed
     procedure stays online at its direct link but no longer turns up in
     search, so pass those in with --seed (find them with a web search for
     the plant name plus "uvp-verbund.de").
  3. Fetch each procedure page: project description, step dates, document list.
  4. Download the key documents (notices, decisions, the impact report).
  5. Write one plain-text index per plant under work/permits/<scope>/.

Every page and PDF that loads lands in fetch.py's disk cache
(work/fetch_cache/), so a later `python scripts/fetch.py <url>` or
`url_verifier.py` call on the same URL is answered from disk at once.
Nothing here stages a record: the index files are reading material for the
researcher or the subagent, and the usual verification still applies.

Usage (from scripts/):
    python harvest_permits.py --scope germany                  # in-development plants
    python harvest_permits.py --scope germany --plants L100000101913,L100000101983
    python harvest_permits.py --scope germany --all-plants
    python harvest_permits.py --scope germany --seed L100000101913=8aa50135-8a84-4107-8510-4ef885430b90
    python harvest_permits.py --scope germany --search-only    # list matches, fetch nothing else

Reruns are cheap: cached pages are not fetched again, and a plant whose index
exists is skipped unless --redo is given. Progress goes to stderr and to
work/permits/<scope>/harvest_log.jsonl.
"""
import argparse
import html
import json
import math
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote, unquote

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch import fetch_page  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
PORTAL = "https://www.uvp-verbund.de"
IN_DEVELOPMENT = {"announced", "pre-construction", "construction"}

# A procedure title must look like a power or heat plant project to be kept.
TITLE_KEEP = re.compile(
    r"kraftwerk|gud|gasturbine|gasmotor|motorenheiz|bhkw|heizwerk|kwk|"
    r"kraft-w[äa]rme|dampfturbine|energiezentrale|energiepark|feuerungsanlage|"
    r"h2-ready|wasserstoff.*kraftwerk|stromerzeugung", re.I)
TITLE_DROP = re.compile(
    r"windkraft|windenergie|wasserkraft|photovoltaik|solar|biogas|deponie|"
    r"klärschlamm|müll|abfall|kernkraft|pumpspeicher|freileitung|kv-leitung", re.I)
# Documents worth downloading in full, most useful first.
DOC_PRIORITY = [
    re.compile(r"bescheid|genehmigung|entscheidung|zulassung", re.I),
    re.compile(r"bekanntmachung|bek\b|bek[. _]", re.I),
    re.compile(r"kurzbeschreibung|allgemeinverst|erl[äa]uterung|zusammenfassung", re.I),
    re.compile(r"uvp-?bericht|uvp-b|umweltvertr", re.I),
    re.compile(r"antrag|vorhaben|anlagenbeschreibung", re.I),
]
DOC_SKIP = re.compile(r"lageplan|karte|kartier|schall|l[äa]rm|fledermaus|brutv|amphib|"
                      r"baugrund|altlast|benthos|fisch|\.zip$|\.(jpg|png|tif)$", re.I)
NAME_NOISE = re.compile(
    r"\b(power station|power plant|chp plant|chp|cogeneration plant|gas engine|"
    r"combined cycle|heat and power|plant|station)\b", re.I)


def log(msg):
    print(f"[harvest] {msg}", file=sys.stderr, flush=True)


def get(url, attempts, timeout=120):
    """One URL through the patient fetcher. Returns the Page (status may be non-200)."""
    page = fetch_page(url, timeout=timeout, rate_limit_attempts=attempts)
    return page


def strip_tags(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def search_terms(plant):
    """Search words for one plant: the town, then the distinctive name words."""
    terms = []
    for raw in (plant.get("city"), plant.get("local_name"), plant.get("name")):
        if not isinstance(raw, str) or not raw.strip():
            continue
        t = NAME_NOISE.sub(" ", raw)
        t = re.sub(r"\(.*?\)", " ", t)
        t = re.sub(r"\s+", " ", t).strip(" -,")
        if len(t) >= 4 and t.lower() not in [x.lower() for x in terms]:
            terms.append(t)
    return terms[:2]


def km(lat1, lon1, lat2, lon2):
    p = math.pi / 180
    a = (math.sin((lat2 - lat1) * p / 2) ** 2
         + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2)
    return 12742 * math.asin(math.sqrt(a))


def search(term, attempts):
    """Procedures matching one search word: [{uuid, title, lat, lon}], from the
    map marker feed (small JSON pages; an empty page ends the list)."""
    hits, page_no = [], 1
    while page_no <= 5:
        url = f"{PORTAL}/rest/getSearchMarkers?q={quote(term)}&page={page_no}"
        page = get(url, attempts)
        if page.status != "200":
            log(f"search {term!r} page {page_no}: HTTP {page.status}")
            return hits, False
        try:
            rows = json.loads(page.text)
            if isinstance(rows, str):
                rows = json.loads(rows)
        except ValueError:
            log(f"search {term!r}: reply is not JSON")
            return hits, False
        if not rows:
            break
        short_page = len(rows) < 5      # a nearly empty page is the last one
        for r in rows:
            if isinstance(r, dict) and r.get("uuid"):
                hits.append({"uuid": r["uuid"], "title": r.get("title") or "",
                             "lat": r.get("lat"), "lon": r.get("lon"),
                             "procedure": r.get("procedure") or ""})
        if short_page:
            break
        page_no += 1
    return hits, True


def pick(hits, plant, radius_km):
    """Keep power plant procedures; when the hit has coordinates, also require
    it to sit near the plant."""
    out, seen = [], set()
    for h in hits:
        if h["uuid"] in seen:
            continue
        seen.add(h["uuid"])
        title = h["title"]
        if not TITLE_KEEP.search(title) or TITLE_DROP.search(title):
            continue
        try:
            d = km(float(plant["lat"]), float(plant["lon"]), float(h["lat"]), float(h["lon"]))
        except (TypeError, ValueError):
            d = None
        if d is not None and d > radius_km:
            continue
        out.append({**h, "km": None if d is None else round(d, 1)})
    return out


def parse_procedure(text):
    """Title, description, step dates and documents from a procedure page."""
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    title = strip_tags(m.group(1)).split("|")[0].strip() if m else ""
    plain = strip_tags(text)
    desc = ""
    m = re.search(r"Vorhabenbeschreibung\s+(.*?)\s+(?:UVP-Kategorie|Raumbezug|Adressen|Verfahrensschritte)",
                  plain, re.S)
    if m:
        desc = m.group(1).strip()
    steps = []
    i = plain.find("Verfahrensschritte")
    tail = plain[i:] if i >= 0 else ""
    for m in re.finditer(r"(Zeitraum der [A-Za-zÄÖÜäöüß]+|Datum der [A-Za-zÄÖÜäöüß]+)\s+"
                         r"(\d{2}\.\d{2}\.\d{4})(?:\s*-\s*(\d{2}\.\d{2}\.\d{4}))?", tail):
        steps.append(" ".join(x for x in (m.group(1) + ":", m.group(2),
                                          ("to " + m.group(3)) if m.group(3) else "") if x))
    docs, seen = [], set()
    for m in re.finditer(r'href="([^"]*documents-ige-ng[^"]*)"[^>]*>(.*?)</a>', text, re.S):
        url = html.unescape(m.group(1))
        if url.startswith("/"):
            url = PORTAL + url
        if url in seen:
            continue
        seen.add(url)
        docs.append({"url": url, "file": unquote(url.rsplit("/", 1)[-1]),
                     "label": strip_tags(m.group(2))})
    return {"title": title, "description": desc, "steps": steps, "documents": docs}


def choose_documents(docs, limit):
    ranked = []
    for d in docs:
        name = d["file"] + " " + d["label"]
        if DOC_SKIP.search(name):
            continue
        for rank, pat in enumerate(DOC_PRIORITY):
            if pat.search(name):
                ranked.append((rank, len(ranked), d))
                break
    return [d for _, _, d in sorted(ranked, key=lambda x: x[:2])[:limit]]


def capacity_lines(text, limit=8):
    """Lines of a document that state electrical or thermal output."""
    out = []
    for line in text.splitlines():
        s = re.sub(r"\s+", " ", line).strip()
        if re.search(r"\d\s*(MW|MWel|MWth|MW el|Megawatt)\b", s) and 20 < len(s) < 400 and s not in out:
            out.append(s)
            if len(out) >= limit:
                break
    return out


def write_index(path, plant, procedures, searched, complete):
    L = [f"# Permit register files for {plant['name']} ({plant['id']})", "",
         "Source: the German environmental impact assessment register, uvp-verbund.de. "
         "Each page and document marked as saved is in the local fetch cache, so "
         "`python scripts/fetch.py <url> --text` and `url_verifier.py` read it at once "
         "without contacting the server.", "",
         f"Harvested: {time.strftime('%Y-%m-%d %H:%M %Z')}",
         f"Search words used: {', '.join(searched) or 'none (seeded procedures only)'}", ""]
    if not complete:
        L += ["One or more searches did not finish. A missing procedure here does not "
              "mean the register has none.", ""]
    if not procedures:
        L += ["No power plant procedure was found for this plant in the register.", ""]
    for p in procedures:
        L += [f"## {p['title'] or p.get('search_title') or p['uuid']}", "",
              f"Procedure page: {p['url']}"]
        if p.get("status") != "200":
            L += [f"The procedure page could not be read (HTTP {p.get('status')}). Try again later.", ""]
            continue
        if p.get("km") is not None:
            L.append(f"Distance from the GEM coordinates: {p['km']} km")
        L.append("")
        if p["description"]:
            L += ["Project description (German, as published):", "", "> " + p["description"], ""]
        if p["steps"]:
            L += ["Procedure dates:", ""] + [f"- {s}" for s in p["steps"]] + [""]
        if p["documents"]:
            L += [f"Documents ({len(p['documents'])}):", ""]
            for d in p["documents"]:
                tag = {"saved": "saved", "failed": "not saved, the download failed",
                       None: "not downloaded"}[d.get("state")]
                L.append(f"- {d['file']} ({tag}): {d['url']}")
                for c in d.get("capacity_lines", []):
                    L.append(f"    - states: {c}")
            L.append("")
    path.write_text("\n".join(L), encoding="utf-8")


def load_plants(args):
    scope_dir = REPO / "batches" / args.scope
    sweep = json.loads((scope_dir / "staging" / "sweep_args.json").read_text())
    csv = pd.read_csv(sweep["csv"], low_memory=False)
    ids = [p["plant_id"] for p in sweep["plants"]]
    names = {p["plant_id"]: p["plant_name"] for p in sweep["plants"]}
    wanted = set(args.plants.split(",")) if args.plants else None
    seeds = {}
    for s in args.seed or []:
        pid, uuid = s.split("=", 1)
        seeds.setdefault(pid, []).append(uuid)
    plants = []
    for pid in ids:
        rows = csv[csv["GEM location ID"] == pid]
        if rows.empty:
            continue
        in_dev = bool(set(rows["Status"].astype(str)) & IN_DEVELOPMENT)
        if wanted is not None:
            if pid not in wanted and pid not in seeds:
                continue
        elif not (args.all_plants or in_dev or pid in seeds):
            continue
        r = rows.iloc[0]
        plants.append({"id": pid, "name": names.get(pid) or r["Plant name"],
                       "local_name": r.get("Plant Name in Local Language / Script"),
                       "city": r.get("City"), "lat": r.get("Latitude"), "lon": r.get("Longitude"),
                       "seeds": seeds.get(pid, [])})
    return plants


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", required=True, help="batch folder name, e.g. germany")
    ap.add_argument("--plants", help="comma-separated GEM location IDs (default: in-development plants)")
    ap.add_argument("--all-plants", action="store_true", help="every plant in the sweep, not only in-development ones")
    ap.add_argument("--seed", action="append", metavar="PLANT=UUID",
                    help="a procedure already known for a plant (repeatable)")
    ap.add_argument("--seeds-only", action="store_true", help="skip searching; fetch seeded procedures only")
    ap.add_argument("--search-only", action="store_true", help="list matching procedures and stop")
    ap.add_argument("--docs-per-procedure", type=int, default=4)
    ap.add_argument("--radius-km", type=float, default=15.0)
    ap.add_argument("--attempts", type=int, default=40, help="patient retries per URL on HTTP 429")
    ap.add_argument("--redo", action="store_true", help="rebuild indexes that already exist")
    args = ap.parse_args()

    out_dir = REPO / "work" / "permits" / args.scope
    out_dir.mkdir(parents=True, exist_ok=True)
    logf = (out_dir / "harvest_log.jsonl").open("a", encoding="utf-8")
    plants = load_plants(args)
    log(f"{len(plants)} plants to harvest into {out_dir}")

    for n, plant in enumerate(plants, 1):
        index = out_dir / f"{plant['id']}.md"
        if index.exists() and not args.redo and not args.search_only:
            log(f"({n}/{len(plants)}) {plant['name']}: index exists, skipped")
            continue
        log(f"({n}/{len(plants)}) {plant['name']}")
        found = [{"uuid": u, "title": "", "km": None} for u in plant["seeds"]]
        searched, complete = [], True
        if not args.seeds_only:
            for term in search_terms(plant):
                hits, ok = search(term, args.attempts)
                searched.append(term)
                complete = complete and ok
                kept = pick(hits, plant, args.radius_km)
                log(f"    search {term!r}: {len(hits)} procedures, {len(kept)} kept")
                for k in kept:
                    if k["uuid"] not in [f["uuid"] for f in found]:
                        found.append(k)
        if args.search_only:
            for f in found:
                print(f"{plant['id']}\t{plant['name']}\t{f['uuid']}\t{f.get('km')}\t{f['title']}")
            continue
        procedures = []
        for f in found:
            url = f"{PORTAL}/trefferanzeige?docuuid={f['uuid']}"
            page = get(url, args.attempts)
            proc = {"uuid": f["uuid"], "url": url, "status": page.status, "km": f.get("km"),
                    "search_title": f.get("title"), "title": "", "description": "",
                    "steps": [], "documents": []}
            if page.status == "200":
                proc.update(parse_procedure(page.text))
                for d in choose_documents(proc["documents"], args.docs_per_procedure):
                    doc = get(d["url"], args.attempts, timeout=300)
                    ok = doc.status == "200" and bool(doc.text.strip())
                    d["state"] = "saved" if ok else "failed"
                    if ok:
                        d["capacity_lines"] = capacity_lines(doc.text)
                    log(f"    document {d['file']}: {'saved' if ok else 'HTTP ' + doc.status}")
            log(f"    procedure {f['uuid']}: HTTP {page.status}, {len(proc['documents'])} documents")
            procedures.append(proc)
        write_index(index, plant, procedures, searched, complete)
        logf.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "plant": plant["id"],
                               "name": plant["name"], "searched": searched, "complete": complete,
                               "procedures": [{"uuid": p["uuid"], "status": p["status"],
                                               "title": p["title"],
                                               "saved": sum(1 for d in p["documents"] if d.get("state") == "saved")}
                                              for p in procedures]}, ensure_ascii=False) + "\n")
        logf.flush()
    log("done")


if __name__ == "__main__":
    main()
