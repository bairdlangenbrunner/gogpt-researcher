#!/usr/bin/env python3
"""
Read every utility resource plan of a scope in full, so no plan is skipped (QC/Country
checklist rows 34 and 37; Baird 2026-11-06, after Kentucky, where the statewide researcher read
only the docket summaries and missed the KYMEA Energy Center II option).

Usage (from scripts/):
    python irp_plans.py --state Kentucky
    python irp_plans.py --country Germany          # only when scopes/<tag>/irp_plans.json exists
    python irp_plans.py --state Kentucky --offline # reuse saved text, no fetching (tests, reruns)

Reads
    scopes/<tag>/irp_plans.json, the scope's plan list (committed, edited by the researcher):
      regulator     who receives the plans ("Kentucky Public Service Commission")
      plan_search   how the list was made complete: the regulator's plan cases, each
                    utility's own planning page, and what was searched (a sentence)
      utilities     one per planning utility:
                      utility, short, sheet (its Utility cell on the US IRPs tab, if any),
                      owners (owner, operator or parent names in the export it covers),
                      plan ("2026 IRP"), year, filed (YYYY-MM-DD), case, other_cases,
                      documents (every volume of the newest plan, read in full),
                      landing (pages where a newer plan would appear), next_due
      not_planners  {owner name in the export: why it files no plan of its own}
    the unfiltered export (gem_export_gogpt.csv), for plant names to match and the scope's owners
    work/irp_us-<state-slug>.json from irp_sheet.py, when present (the US IRPs tab)
    batches/<tag>/harvest/*.json docket harvests, for plan cases the list does not name

Writes
    scopes/<tag>/work/irp/<utility-slug>/<n>.txt   the text of every plan document (gitignored)
    batches/<tag>/harvest/irp_plans.json and .md
      utilities     per utility: the documents with reached, pages and characters; gas_hits
                    (page, line and the GEM plants the line names) for every line that names a
                    gas or oil technology and a megawatt figure; preferred_pages (where the plan
                    names its preferred or recommended portfolio); unmatched_names (named sites in
                    gas lines that match no GEM plant: candidates for an add or a watch item);
                    newer_hints (a later plan on a landing page or in a docket); overdue
      sheet_corrections  lines for the US IRPs tab Notes (build_review_package.py --irp puts
                    them in irp_notes_draft; the repo never writes the tab)
      sheet_unlisted, unlisted_cases, owners_unlisted   gaps in the plan list itself
      needs_answer  one key per utility, "plan <utility>", answered in batches/<tag>/coverage.json
                    under irp_plans (state_gate.py gate irp-plans)

The script surfaces lines; it never decides. The statewide researcher reads each plan's preferred
portfolio and every alternative portfolio that names a gas or oil plant, and answers each utility.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import REPO_ROOT, gem_export_csv, scope_dir, scope_tag, scope_work, work_dir  # noqa: E402

MAX_AGE_DAYS = 7
MIN_CHARS = 5000           # a plan volume with less text than this did not really load
MAX_HITS = 1500            # gas lines kept per utility

GAS_RX = re.compile(
    r"natural gas|gas[- ]fired|\bgas\b|combined[- ]cycle|\bNGCC\b|\bCCGT\b|\bCCs?\b|combustion turbine|"
    r"\bCTs?\b|simple[- ]cycle|\bSCCT\b|\bRICE\b|reciprocating|aeroderivative|\bpeak(?:er|ing)\b|"
    r"\boil\b|diesel|fuel oil|dual[- ]fuel|\bengines?\b", re.I)
MW_RX = re.compile(r"\d[\d,.]*\s*(?:MW|megawatt|GW)\b", re.I)
ADD_RX = re.compile(r"\badd(?:s|ed|ing|ition)?\b|\bnew\b|\bbuild\b|construct|replace|repower|conver(?:t|sion)|"
                    r"\bselect|\bpropos|\bplanned\b|\b20[3-5]\d\b|(?:\b\d{2,4}\b.*){3}", re.I)
PREFERRED_RX = re.compile(r"preferred (?:plan|portfolio|resource plan)|recommended (?:plan|portfolio)|"
                          r"selected (?:plan|portfolio)|strategic portfolio", re.I)
SITE_RX = re.compile(r"((?:[A-Z][A-Za-z.'&-]+ ){0,3}[A-Z][A-Za-z.'&-]+) "
                     r"(Energy Center|Generating Station|Generating Plant|Power Station|Power Plant|Station|Plant)"
                     r"(?: (?:I{1,3}|IV|\d))?")
GENERIC = {"power", "plant", "station", "generating", "energy", "center", "centre", "the", "unit", "units",
           "combined", "cycle", "gas", "natural", "facility", "project", "power station", "electric",
           "new", "existing", "peaking", "solar", "coal", "steam", "combustion", "turbine", "county"}
SITE_NOISE = {"mw", "gw", "mwh", "a", "an", "of", "and", "at", "in", "to", "new", "proposed", "planned",
              "add", "build", "existing", "retire", "retirement", "total", "table", "figure", "rice", "ct", "cc",
              "ccgt", "ngcc", "scct", "aero", "frame", "peaker", "greenfield", "brownfield", "self", "fossil", "fuel", "fired", "fuel-fired", "gas-fired"}
UTILITY_RX = re.compile(r"electric|power|energy|utilit|cooperative|co-op|municipal|authority|light|"
                        r"public service|g&e|gas and electric|plant board", re.I)
PLAN_CASE_RX = re.compile(r"integrated resource plan|resource planning report|\bIRP\b", re.I)


def ws(v):
    return re.sub(r"\s+", " ", str(v or "")).strip()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", ws(s).lower()).strip("-") or "utility"


def norm(s):
    from irp_sheet import norm_name
    return norm_name(s)


# ------------------------------------------------------------------ inputs ---

def load_settings(tag):
    p = scope_dir(tag) / "irp_plans.json"
    if not p.exists():
        return None, p
    return json.loads(p.read_text(encoding="utf-8")), p


def plant_keys(csv_path, country=None):
    """{name key: [(plant_id, plant name, state)]} for every plant of the scope's country in the
    unfiltered export (a utility's plan names plants in neighboring states), where the key is the
    plant name without generic words, at least five letters long."""
    keys = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if country and ws(r.get("Country/Area")) != country:
                continue
            name = ws(r.get("Plant name"))
            key = site_core(name)
            if len(key) < 5:
                continue
            ent = (ws(r.get("GEM location ID")), name, ws(r.get("State/Province")))
            lst = keys.setdefault(key, [])
            if ent not in lst:
                lst.append(ent)
    return keys


def scope_owners(csv_path, state=None, country=None):
    """Every owner, operator and parent name on the scope's rows that looks like a utility."""
    out = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if state and ws(r.get("State/Province")) != state:
                continue
            if country and ws(r.get("Country/Area")) != country:
                continue
            for col in ("Owner(s)", "Operator(s)", "Parent(s)"):
                for part in re.split(r";|\|", ws(r.get(col))):
                    name = re.sub(r"\s*\[[^\]]*\]\s*", " ", part)
                    name = ws(re.sub(r"\s*\(?\d+(\.\d+)?%\)?\s*$", "", name))
                    if name and UTILITY_RX.search(name):
                        out.setdefault(name, set()).add(ws(r.get("GEM location ID")))
    return {k: sorted(v) for k, v in out.items()}


def docket_plan_cases(batch):
    """Plan cases named in any docket harvest of the batch: [(docket, title)]."""
    found = []
    hdir = Path(batch) / "harvest"
    for p in sorted(hdir.glob("*.json")) if hdir.exists() else []:
        if p.name == "irp_plans.json":
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            continue
        items = data.get("dockets") if isinstance(data, dict) else None
        for d in items or []:
            if isinstance(d, dict) and PLAN_CASE_RX.search(ws(d.get("title"))):
                found.append((ws(d.get("docket")), ws(d.get("title"))))
    return found


# ------------------------------------------------------------------- reading ---

def read_document(url, out_txt, offline=False):
    """(reached, status, text). The text is saved; offline reuses the saved text."""
    if offline:
        if out_txt.exists():
            t = out_txt.read_text(encoding="utf-8", errors="replace")
            return len(t) >= MIN_CHARS, "saved", t
        return False, "not saved", ""
    if not url.startswith(("http://", "https://")):
        # a repo path to a copy a harvester already saved, for a plan that only downloads
        # through a session or token (New Mexico PRCe360, 2026-11-17)
        src = (REPO_ROOT / url).resolve()
        if not src.exists():
            return False, "local file missing", ""
        if src.suffix.lower() == ".pdf":
            import subprocess
            text = subprocess.run(["pdftotext", "-layout", str(src), "-"], capture_output=True,
                                  text=True, errors="replace").stdout
        else:
            text = src.read_text(encoding="utf-8", errors="replace")
        out_txt.parent.mkdir(parents=True, exist_ok=True)
        out_txt.write_text(text, encoding="utf-8")
        return len(text) >= MIN_CHARS, "local", text
    from fetch import fetch_page
    page = fetch_page(url, timeout=180)
    text = page.text or ""
    if not page.is_pdf and "<html" in text[:2000].lower():
        text = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", text)
        text = re.sub(r"(?s)<[^>]+>", " ", text)
    ok = page.status.startswith("2") and len(text) >= MIN_CHARS
    if not ok and out_txt.exists():
        # a failed fetch never wipes text read on an earlier run (Oklahoma, 2026-11-06:
        # ompa.com started refusing and the saved minutes were overwritten with nothing)
        saved = out_txt.read_text(encoding="utf-8", errors="replace")
        if len(saved) >= MIN_CHARS:
            return True, f"saved ({page.status} today)", saved
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    out_txt.write_text(text, encoding="utf-8")
    return ok, page.status, text


def site_core(text):
    """The tokens of a site name that are not generic words or units: "KYMEA Energy Center II" -> "kymea ii"."""
    toks = re.sub(r"[^a-z0-9 ]+", " ", text.lower()).split()
    return " ".join(t for t in toks if t not in GENERIC and t not in SITE_NOISE and not t.isdigit())


SITE_AFTER_RX = r"(?:plant|station|generating|energy center|ct|cts|cc|ccs?gt|ngcc|scct|rice|unit|units|combustion|combined|steam|peaker)\b"


def match_plants(low, keys, home=None):
    """GEM plants named in a lowercased line. A one-word name outside the home state (Carbon,
    Aurora, Bridge) counts only when a site word follows it, so ordinary words do not match."""
    plants = []
    for k, ents in keys.items():
        if f" {k} " not in low:
            continue
        loose = len(k.split()) == 1 and not re.search(rf" {re.escape(k)} {SITE_AFTER_RX}", low)
        plants += [{"plant_id": e[0], "plant_name": e[1], "state": e[2]} for e in ents
                   if not loose or (home and e[2] == home)]
    return plants


def scan_text(text, keys, doc_no, home=None):
    """Gas lines with a megawatt figure on the line or a line next to it, preferred-plan pages,
    and named sites in those lines that match no GEM plant name."""
    hits, preferred, unmatched, seen = [], [], {}, set()
    for pno, page in enumerate(text.split("\f"), 1):
        if PREFERRED_RX.search(page):
            preferred.append(f"{doc_no}:{pno}")
        lines = [ws(x) for x in page.splitlines()]
        for i, line in enumerate(lines):
            if len(line) < 12 or not GAS_RX.search(line):
                continue
            window = " ".join(lines[max(0, i - 1):i + 2])
            if not (MW_RX.search(window) or ADD_RX.search(line)):
                continue
            low = " " + re.sub(r"[^a-z0-9 ]+", " ", line.lower()) + " "
            plants = match_plants(low, keys, home)
            for m in SITE_RX.finditer(line):
                core = site_core(m.group(0))
                if len(core) < 4 or core in seen:
                    continue
                seen.add(core)
                if not any(set(core.split()) <= set(k.split()) for k in keys):
                    unmatched.setdefault(ws(m.group(0)), f"{doc_no}:{pno}")
            hits.append({"doc": doc_no, "page": pno, "line": line[:300], "plants": plants[:6]})
    return hits, preferred, unmatched


def newer_on_landing(text, year):
    """Plan years later than `year` (the plan's filing year) and no later than this year, near the
    words resource plan or IRP on a landing page. A later year is a due date, not a plan."""
    out = set()
    for m in re.finditer(r"(20\d\d)[^.\n]{0,60}(?:integrated resource plan|resource plan|\bIRP\b)|"
                         r"(?:integrated resource plan|\bIRP\b)[^.\n]{0,40}(20\d\d)", text, re.I):
        y = int(m.group(1) or m.group(2))
        if year and int(year) < y <= datetime.date.today().year:
            out.add(y)
    return sorted(out)


# ------------------------------------------------------------------- build ---

def match_sheet(sheet_row, utilities):
    cell = ws(sheet_row.get("utility"))
    for u in utilities:
        if ws(u.get("sheet")) and ws(u.get("sheet")) == cell:
            return u
    ncell = norm(cell)
    for u in utilities:
        names = [u.get("utility"), u.get("short")] + list(u.get("owners") or [])
        if any(norm(n) and (norm(n) in ncell or ncell in norm(n)) for n in names if n):
            return u
    return None


def best_utility(title, utilities):
    """The utility whose name, short name or owner name matches the case title with the longest
    whole-word match ("East Kentucky Power Cooperative" beats "Kentucky Power"). None when none matches."""
    t = " " + norm(title) + " "
    best, size = None, 0
    for u in utilities:
        for n in [u.get("utility"), u.get("short")] + list(u.get("owners") or []):
            k = norm(n or "")
            if k and f" {k} " in t and len(k) > size:
                best, size = u, len(k)
    return best


def year_of(s):
    m = re.findall(r"20\d\d", ws(s))
    return max(int(y) for y in m) if m else None


def build(tag, settings, batch, export_csv, state=None, country=None, sheet=None, offline=False,
          today=None):
    today = today or datetime.date.today()
    keys = plant_keys(export_csv, country or ("United States" if state else None))
    utilities = settings.get("utilities") or []
    cases = docket_plan_cases(batch)
    out_utils = []
    for u in utilities:
        name = ws(u.get("utility"))
        udir = scope_work(tag) / "irp" / slug(u.get("short") or name)
        docs, hits, preferred, unmatched = [], [], [], {}
        for i, url in enumerate(u.get("documents") or [], 1):
            ok, status, text = read_document(url, udir / f"{i}.txt", offline=offline)
            npages = text.count("\f") + 1 if text else 0
            docs.append({"n": i, "url": url, "reached": ok, "status": status, "pages": npages,
                         "chars": len(text), "saved": str((udir / f"{i}.txt").relative_to(REPO_ROOT))
                         if str(udir).startswith(str(REPO_ROOT)) else str(udir / f"{i}.txt")})
            if ok:
                h, p, um = scan_text(text, keys, i, home=state)
                hits += h
                preferred += p
                for k, v in um.items():
                    unmatched.setdefault(k, v)
        newer = []
        for url in u.get("landing") or []:
            if offline:
                continue
            from fetch import fetch_page
            page = fetch_page(url, timeout=60)
            filed_year = year_of(u.get("filed")) or u.get("year")
            for y in newer_on_landing(page.text or "", filed_year):
                newer.append(f"{url} mentions a {y} plan")
        known = {ws(u.get("case"))} | {ws(c) for c in u.get("other_cases") or []}
        names = [n for n in [name, u.get("short")] + list(u.get("owners") or []) if n]
        for dk, title in cases:
            if dk in known or best_utility(title, utilities) is not u:
                continue
            if True:
                y = year_of(title)
                if y and u.get("year") and y >= int(u["year"]):
                    newer.append(f"docket {dk}: {title}")
        due = ws(u.get("next_due"))
        overdue = False
        try:
            overdue = bool(due) and datetime.date.fromisoformat(due[:10] if len(due) >= 10
                                                               else due + "-01") < today
        except ValueError:
            pass
        out_utils.append({
            "utility": name, "short": u.get("short"), "plan": u.get("plan"), "year": u.get("year"),
            "filed": u.get("filed"), "case": u.get("case"), "next_due": due, "overdue": overdue,
            "documents": docs, "gas_hits": hits[:MAX_HITS], "gas_hits_total": len(hits),
            "preferred_pages": preferred[:60], "unmatched_names": unmatched,
            "newer_hints": newer, "key": f"plan {name}"})
    # gaps in the plan list itself
    listed = set()
    for u in utilities:
        listed |= {ws(u.get("case"))} | {ws(c) for c in u.get("other_cases") or []}
    listed |= {ws(c) for c in settings.get("other_cases") or []}
    unlisted_cases = [f"{dk}: {t}" for dk, t in cases if dk not in listed]
    covered = [norm(n) for u in utilities for n in [u.get("utility"), u.get("short")] + list(u.get("owners") or []) if n]
    covered += [norm(n) for n in (settings.get("not_planners") or {})]
    owners = scope_owners(export_csv, state=state, country=country)
    owners_unlisted = {o: pids for o, pids in owners.items()
                       if norm(o) and not any(c and (c in norm(o) or norm(o) in c) for c in covered)}
    sheet_unlisted, corrections = [], []
    for row in (sheet or {}).get("utilities") or []:
        u = match_sheet(row, utilities)
        if not u:
            sheet_unlisted.append(ws(row.get("utility")))
            continue
        sy, uy = year_of(row.get("irp_year")), u.get("year")
        bits = []
        if uy and (not sy or sy < int(uy)):
            doc = (u.get("documents") or [""])[0]
            bits.append(f"the tab shows {ws(row.get('irp_year')) or 'no plan year'}, but the newest plan is the "
                        f"{u.get('plan')}" + (f", filed {u.get('filed')}" if u.get("filed") else "")
                        + (f" in case {u.get('case')}" if u.get("case") else "") + (f" ({doc})" if doc else ""))
        if ws(u.get("next_due")) and ws(u.get("next_due")) != ws(row.get("next_irp_due")):
            bits.append(f"next plan due {u.get('next_due')}")
        if ws(u.get("sheet_note")):
            bits.append(ws(u.get("sheet_note")))
        if bits:
            corrections.append({"utility": ws(row.get("utility")), "line": "; ".join(bits) + "."})
    return {
        "generated": today.isoformat(), "scope": tag, "regulator": settings.get("regulator"),
        "plan_search": settings.get("plan_search"), "utilities": out_utils,
        "sheet_corrections": corrections, "sheet_unlisted": sheet_unlisted,
        "unlisted_cases": unlisted_cases, "owners_unlisted": owners_unlisted,
        "needs_answer": [u["key"] for u in out_utils],
    }


def render(data):
    L = [f"# Utility resource plans: {data['scope']}", "",
         "Read every plan below in full. For each one, find the preferred or recommended portfolio and "
         "every alternative portfolio that names a gas or oil plant. Match each gas or oil addition to a "
         "GEM unit, stage an update, add it, or put it on the watch list. A plan option that the "
         "board has not chosen is a watch item with watch case not_committed. Answer each utility in "
         "coverage.json under irp_plans with the key shown.", ""]
    for u in data["utilities"]:
        L.append(f"## {u['utility']}: {u['plan']}" + (f", case {u['case']}" if u.get("case") else ""))
        L.append(f"Answer key: `{u['key']}`.")
        for d in u["documents"]:
            state = (f"read, {d['pages']} pages" if d["reached"]
                     else f"NOT READ (status {d['status']}): read it by hand")
            L.append(f"- Document {d['n']}: {d['url']} ({state}; text saved at {d['saved']})")
        if u["newer_hints"]:
            L.append("- A newer plan may exist. Check: " + "; ".join(u["newer_hints"]))
        if u["overdue"]:
            L.append(f"- The next plan was due {u['next_due']}. Look for it before using this one.")
        if u["preferred_pages"]:
            L.append("- Pages that name the preferred or recommended plan (document:page): "
                     + ", ".join(u["preferred_pages"][:30]))
        if u["unmatched_names"]:
            L.append("- Named sites in gas lines that match no GEM plant (document:page): "
                     + "; ".join(f"{k} ({v})" for k, v in list(u["unmatched_names"].items())[:40]))
        L.append(f"- {u['gas_hits_total']} lines name gas or oil with a megawatt figure. The first ones:")
        for h in u["gas_hits"][:25]:
            pl = ", ".join(f"{p['plant_name']} {p['plant_id']}" for p in h["plants"][:3])
            L.append(f"  - {h['doc']}:{h['page']}: {h['line'][:200]}" + (f" [GEM: {pl}]" if pl else ""))
        L.append("")
    if data["unlisted_cases"]:
        L += ["## Plan cases not in the plan list", ""] + [f"- {c}" for c in data["unlisted_cases"]] + [""]
    if data["owners_unlisted"]:
        L += ["## Utility owners in the export with no plan listed", ""]
        L += [f"- {o} ({', '.join(p[:3])})" for o, p in data["owners_unlisted"].items()] + [""]
    if data["sheet_unlisted"]:
        L += ["## Utilities on the US IRPs tab missing from the plan list", ""]
        L += [f"- {s}" for s in data["sheet_unlisted"]] + [""]
    if data["sheet_corrections"]:
        L += ["## Corrections for the US IRPs tab", ""]
        L += [f"- {c['utility']}: {c['line']}" for c in data["sheet_corrections"]] + [""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--state")
    g.add_argument("--country")
    ap.add_argument("--csv", default=None, help="the unfiltered export (default gem_export_gogpt.csv)")
    ap.add_argument("--sheet", default=None, help="irp_sheet.py output (default work/irp_us-<slug>.json)")
    ap.add_argument("--batch", default=None, help="default batches/<tag>")
    ap.add_argument("--offline", action="store_true", help="reuse saved text; fetch nothing")
    a = ap.parse_args(argv)
    tag = scope_tag(state=a.state, country=a.country)
    settings, sp = load_settings(tag)
    if settings is None:
        sys.exit(f"ERROR: {sp} is missing. List every planning utility of the scope there first "
                 "(see this script's docstring).")
    batch = Path(a.batch) if a.batch else REPO_ROOT / "batches" / tag
    export_csv = Path(a.csv) if a.csv else gem_export_csv()
    sheet = None
    if a.state:
        shp = Path(a.sheet) if a.sheet else work_dir() / f"irp_us-{slug(a.state)}.json"
        if shp.exists():
            sheet = json.loads(shp.read_text(encoding="utf-8"))
    data = build(tag, settings, batch, export_csv, state=a.state, country=a.country, sheet=sheet,
                 offline=a.offline)
    out = batch / "harvest"
    out.mkdir(parents=True, exist_ok=True)
    (out / "irp_plans.json").write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    (out / "irp_plans.md").write_text(render(data) + "\n", encoding="utf-8")
    for u in data["utilities"]:
        nread = sum(d["reached"] for d in u["documents"])
        print(f"{u['utility']}: {nread} of {len(u['documents'])} documents read, {u['gas_hits_total']} gas lines, "
              f"{len(u['unmatched_names'])} named sites not in GEM"
              + (", NEWER PLAN HINT" if u["newer_hints"] else "") + (", OVERDUE" if u["overdue"] else ""))
    for k in ("unlisted_cases", "owners_unlisted", "sheet_unlisted"):
        if data[k]:
            print(f"{k}: {len(data[k])} (fix scopes/{tag}/irp_plans.json)")
    print(f"Wrote {out / 'irp_plans.json'} and .md")


if __name__ == "__main__":
    main()
