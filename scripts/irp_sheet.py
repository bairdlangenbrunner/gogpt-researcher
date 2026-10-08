#!/usr/bin/env python3
"""
Read the "US IRPs" tab of the Update sheet for one or more US states and turn
it into the IRP research step (QC/Country checklist rows 34 and 37).

Usage (from scripts/):
    python irp_sheet.py --state Georgia [--state Indiana ...]
    python irp_sheet.py --state Georgia --from-json work/irp_tab.json   # offline / tests
    python irp_sheet.py --state Georgia --csv gem_export_gogpt_scoped.csv --out-dir ../work

Reads
    the "US IRPs" tab (spreadsheet in SPREADSHEET below) through gsheets.py:
    the read-only work profile, never a public export URL. --from-json takes
    the tab's values (a list of rows, header first) saved earlier, so tests
    and offline runs do not touch the sheet. --save-json writes the values
    read from the sheet to a file for the next offline run (it holds a
    colleague's working notes: keep it under work/, never commit it).
    The tab's shape: a row with only a State name, then one row per utility
    under it with Utility, IRP year, File (one or more links and sometimes a
    page hint), Notes (a running log, newest first, each entry starting
    "Q2 2026 ...") and a sparse Updated IRP column. The state row can carry a
    regulator link in a later column (Indiana does).
    the GOGPT-scoped export, for the state's plants: owners, operators and
    parents are matched to the utilities, and the IRP column (the database's
    IRP checkbox, exported as yes / no) says which units already carry the box.

Writes  work/irp_us-<state-slug>.json and .md per state
    where        the scope (same shape as validation_report.py / match_ids.py)
    skipped      true when the tab has no rows for the state; the brief then
                 says the step was skipped, and nothing else is produced
    utilities    one per sheet row: utility, irp_year, is_draft, links,
                 file_note (the non-link text in File), notes (dated entries,
                 newest first), latest_note, updated_irp, mw_mentions, and the
                 GEM plants matched to it (by owner / operator / parent, and by
                 an "IRP" placeholder plant name that carries the utility's
                 name or acronym)
    irp_units    every unit in the state whose IRP box is already ticked
    tasks        one whole-plant task per matched plant the plan can plausibly
                 move (an IRP placeholder plant, a unit with the IRP box
                 ticked, or a unit that is not simply operating or retired),
                 in the shape build_state_brief.py --irp reads (kind fix,
                 checks [37]); a utility's operating fleet is compared in the
                 statewide review instead
    brief        the "Integrated resource plans" block for the statewide
                 research agent, plain language (also the .md file)

The step never writes to the sheet. The Notes entry for the tab is drafted by
build_review_package.py (sheet irp_notes_draft) and pasted by a person.
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
from paths import gogpt_scoped_csv, work_dir  # noqa: E402

SPREADSHEET = "1xTcMPmwDfB1z3EcP6v3lg3y7Hcmo1wL_U8EJFQc9EtY"   # the Update V2 sheet
TAB = "US IRPs"
GID = 560668239
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET}/edit?gid={GID}#gid={GID}"

# Sheet spellings that differ from the state names GEM uses.
STATE_FIXES = {"noth carolina": "north carolina", "conneticut": "connecticut"}

# Short forms the sheet uses for utilities, expanded to the names GEM's owner
# columns carry. Matching is on word prefixes (see match_owner), so one entry
# per company is enough; subsidiaries with the same first words match too.
ALIASES = {
    "tva": ["tennessee valley authority"],
    "lg&e": ["louisville gas & electric"],
    "lge": ["louisville gas & electric"],
    "ku": ["kentucky utilities"],
    "kpco": ["kentucky power"],
    "ekpc": ["east kentucky power cooperative"],
    "kymea": ["kentucky municipal power agency"],
    "brec": ["big rivers electric"],
    "nipsco": ["northern indiana public service"],
    "aep": ["american electric power"],
    "i&m": ["indiana michigan power"],
    "impa": ["indiana municipal power agency"],
    "wvpa": ["wabash valley power association"],
    "vectren": ["vectren utility holdings", "southern indiana gas"],
    "vectren south": ["vectren utility holdings", "southern indiana gas"],
    "centerpoint energy indiana south": ["centerpoint energy", "southern indiana gas",
                                         "vectren utility holdings"],
    "georgia power": ["georgia power"],
    "southern company": ["southern co", "southern power"],
    "duke energy": ["duke energy"],
    "psnc": ["public service company of north carolina"],
    "dominion": ["dominion energy", "virginia electric"],
}
SUFFIXES = {"co", "corp", "inc", "llc", "lp", "ltd", "plc", "company", "corporation",
            "incorporated", "limited", "the"}
URL_RE = re.compile(r"https?://[^\s,;]+")
QUARTER_RE = re.compile(r"(?<![A-Za-z0-9])(Q[1-4]\s*20\d\d)\s*:?\s*")
MW_RE = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(?:/\s*\d[\d,]*\s*)?MW\b([^.;\n]{0,80})", re.I)
NEXT_IRP_RE = re.compile(
    r"(next IRP[^.]{0,80}?(?:no later than|by|for|in|on|due)\s+([A-Z][a-z]+ \d{1,2}, \d{4}|[A-Z][a-z]+ \d{4}|\d{4}))",
    re.I)

H_PLANT, H_LOC, H_UNIT, H_UNAME = "Plant name", "GEM location ID", "GEM unit ID", "Unit name"
OWNER_COLS = (("Owner(s)", "owner"), ("Operator(s)", "operator"), ("Parent(s)", "parent"))


def ws(v):
    return re.sub(r"\s+", " ", str(v or "")).strip()


def norm_name(s):
    """Lowercase, punctuation to spaces, corporate suffix words dropped."""
    s = ws(s).lower().replace("&", " & ")
    s = re.sub(r"[^a-z0-9&]+", " ", s)
    toks = [t for t in s.split() if t not in SUFFIXES]
    return " ".join(toks)


def utility_variants(utility):
    """Every name the sheet's Utility cell may mean: the main name, each
    parenthetical, each slash-separated part, and their alias expansions.
    Returns (long names for owner matching, short tokens for plant-name
    matching)."""
    cell = ws(utility)
    parts = []
    main = re.sub(r"\([^)]*\)", " ", cell)
    parts += [p for p in re.split(r"\s*/\s*", main) if ws(p)]
    for par in re.findall(r"\(([^)]*)\)", cell):
        par = re.sub(r"^\s*(formerly|now|part of)\s+", "", par, flags=re.I)
        parts += [p for p in re.split(r"\s*/\s*", par) if ws(p)]
    longs, shorts = [], []
    for p in parts:
        key = norm_name(p)
        if not key:
            continue
        if key in ALIASES:
            longs += ALIASES[key]
        elif len(key) <= 6 and " " not in key:
            # an acronym the alias table does not know: plant names only
            pass
        else:
            longs.append(key)
        shorts.append(key)
    longs = list(dict.fromkeys(norm_name(x) for x in longs))
    shorts = list(dict.fromkeys(shorts))
    return longs, shorts


def match_owner(owner, longs):
    """True when an export owner string names one of the utility's long names:
    the owner starts with the name (Georgia Power Co, Duke Energy Indiana LLC),
    or the name starts with the owner when the owner has at least two words
    (CenterPoint Energy Inc for CenterPoint Energy Indiana South)."""
    o = norm_name(owner)
    if not o:
        return False
    for name in longs:
        if o == name or o.startswith(name + " "):
            return True
        if len(o.split()) >= 2 and (name == o or name.startswith(o + " ")):
            return True
    return False


def owners_of(row):
    out = []
    for col, role in OWNER_COLS:
        for part in str(row.get(col) or "").split(";"):
            name = re.sub(r"\s*\[.*?\]\s*", " ", part)
            name = re.sub(r"\s*\(\d+(\.\d+)?\s*%\)", " ", name)
            name = ws(name)
            if name:
                out.append((name, role))
    return out


def plant_name_matches(plant_name, shorts, longs):
    """An IRP placeholder plant ("NIPSCO 2024 IRP power station 1") names its
    utility by acronym or name; match whole words only."""
    n = " " + norm_name(plant_name) + " "
    if " irp " not in n:
        return False
    for key in shorts + longs:
        if key and f" {key} " in n:
            return True
    return False


def split_links(cell):
    links = [u.rstrip(").,;") for u in URL_RE.findall(cell or "")]
    rest = URL_RE.sub(" ", cell or "")
    rest = ws(re.sub(r"^[\s,;]+|[\s,;]+$", "", rest))
    return list(dict.fromkeys(links)), rest


def split_notes(cell):
    """The Notes log as dated entries, newest first as the sheet writes them.
    Text before the first quarter marker (an undated note) gets quarter ""."""
    cell = str(cell or "").strip()
    if not cell:
        return []
    out = []
    marks = list(QUARTER_RE.finditer(cell))
    if not marks:
        return [{"quarter": "", "text": ws(cell)}]
    head = ws(cell[:marks[0].start()])
    if head:
        out.append({"quarter": "", "text": head})
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(cell)
        text = ws(cell[m.end():end])
        if text:
            out.append({"quarter": re.sub(r"\s+", " ", m.group(1)).upper(), "text": text})
    return out


def is_draft(irp_year, notes_text):
    return bool(re.search(r"\bdraft\b", f"{irp_year} {notes_text}", re.I))


def mw_mentions(text):
    out = []
    for m in MW_RE.finditer(text or ""):
        tail = ws(m.group(2))
        out.append(ws(f"{m.group(1)} MW {tail}")[:120])
    return out[:12]


def next_irp_due(text):
    m = NEXT_IRP_RE.search(text or "")
    return ws(m.group(2)) if m else ""


def parse_tab(values):
    """The tab's rows as {state name (GEM spelling): {"links": [...], "rows": [utility dicts]}}."""
    if not values:
        sys.exit("ERROR: the US IRPs tab came back empty")
    header = [ws(h) for h in values[0]]
    need = ["State", "Utility", "IRP year", "File", "Notes"]
    missing = [h for h in need if h not in header]
    if missing:
        sys.exit(f"ERROR: US IRPs tab header changed; missing {missing}; header is {header}")
    col = {h: header.index(h) for h in header}
    cell = lambda r, h: (r[col[h]] if h in col and col[h] < len(r) else "")  # noqa: E731
    states, current = {}, None
    for i, r in enumerate(values[1:], start=2):
        state = ws(cell(r, "State"))
        utility = ws(cell(r, "Utility"))
        if state and not utility:
            key = STATE_FIXES.get(state.lower(), state.lower())
            current = states.setdefault(key, {"name": key.title(), "sheet_name": state,
                                              "links": [], "rows": []})
            # a regulator link in any later column of the state row
            for v in r[1:]:
                links, _ = split_links(v)
                current["links"] += links
            continue
        if not utility:
            continue
        if state:
            key = STATE_FIXES.get(state.lower(), state.lower())
            current = states.setdefault(key, {"name": key.title(), "sheet_name": state,
                                              "links": [], "rows": []})
        if current is None:
            continue
        links, file_note = split_links(cell(r, "File"))
        notes = split_notes(cell(r, "Notes"))
        irp_year = ws(cell(r, "IRP year"))
        notes_text = " ".join(n["text"] for n in notes)
        current["rows"].append({
            "sheet_row": i, "utility": utility, "irp_year": irp_year,
            "is_draft": is_draft(irp_year, cell(r, "Notes")),
            "links": links, "file_note": file_note,
            "notes": notes, "latest_note": notes[0] if notes else None,
            "updated_irp": ws(cell(r, "Updated IRP")),
            "mw_mentions": mw_mentions(notes_text),
            "next_irp_due": next_irp_due(notes_text),
        })
    return states


def load_export(csv_path, state):
    plants = {}
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        hdr = reader.fieldnames or []
        for h in (H_PLANT, H_LOC, H_UNIT, "State/Province", "Country/Area"):
            if h not in hdr:
                sys.exit(f"ERROR: column {h!r} missing from {csv_path}")
        has_irp = "IRP" in hdr
        for r in reader:
            if ws(r.get("Country/Area")).lower() != "united states":
                continue
            if ws(r.get("State/Province")).lower() != state.lower():
                continue
            plants.setdefault(ws(r.get(H_LOC)), []).append(r)
    return plants, has_irp


def unit_brief(r):
    return {"unit_id": ws(r.get(H_UNIT)), "unit_name": ws(r.get(H_UNAME)),
            "status": ws(r.get("Status")), "capacity_mw": ws(r.get("Capacity (MW)")),
            "start_year": ws(r.get("Start year")), "irp_box": ws(r.get("IRP")).lower() == "yes"}


def match_plants(plants, row):
    longs, shorts = utility_variants(row["utility"])
    out = []
    for pid, rows in plants.items():
        first = rows[0]
        roles = set()
        for name, role in owners_of(first):
            if match_owner(name, longs):
                roles.add(role)
        by_name = plant_name_matches(first.get(H_PLANT), shorts, longs)
        if not roles and not by_name:
            continue
        units = [unit_brief(r) for r in rows]
        out.append({"plant_id": pid, "plant_name": ws(first.get(H_PLANT)),
                    "matched_by": sorted(roles) + (["plant name"] if by_name else []),
                    "owners": ws(first.get("Owner(s)")), "units": units,
                    "irp_box_units": sum(u["irp_box"] for u in units),
                    "statuses": sorted({u["status"] for u in units if u["status"]})})
    out.sort(key=lambda p: p["plant_name"].lower())
    return out


SETTLED = {"operating", "retired", "cancelled", "cancelled - inferred 4 y"}


def task_worthy(p):
    """A plant gets its own IRP task when the plan can plausibly move a value on
    it: an IRP placeholder plant, a unit with the IRP box ticked, or a unit that
    is not simply operating or retired. A utility's operating fleet is covered by
    the statewide IRP review instead (the brief lists it there)."""
    if "plant name" in p["matched_by"] or p["irp_box_units"]:
        return True
    return any((u["status"] or "").lower() not in SETTLED for u in p["units"])


def plant_task(row, p):
    """One whole-plant task for the per-plant brief, plain language."""
    listed = f' (listed on the US IRPs tab as "{row["irp_year"]}")' if row["irp_year"] else ""
    link = row["links"][0] if row["links"] else SHEET_URL
    latest = row["latest_note"]
    note = ""
    if latest:
        when = f" ({latest['quarter']})" if latest["quarter"] else ""
        note = f" The newest note on the US IRPs tab{when} says: {latest['text'][:400]}"
        if len(latest["text"]) > 400:
            note += " ..."
    ticked = p["irp_box_units"]
    n = len(p["units"])
    box = (f"The IRP box is already ticked on {ticked} of {n} units."
           if ticked else f"The IRP box is not ticked on any of the {n} units.")
    text = (f"This plant belongs to {row['utility']}, whose integrated resource plan{listed} is at "
            f"{link}. Read the plan's preferred or recommended portfolio and check whether it names "
            f"this plant: a new unit, a conversion, a retirement date, a capacity or start year that "
            f"differs from GEM. Report any such value with the plan page it appears on as the "
            f"source, and mark every finding that comes from the plan with irp true. {box}{note}")
    return {"plant_id": p["plant_id"], "plant_name": p["plant_name"], "unit_id": None,
            "unit_name": None, "source": "irp", "section": "IRP", "kind": "fix",
            "utility": row["utility"], "irp_year": row["irp_year"], "task": text,
            "fields": ["Status", "Capacity (MW)", "Start year", "Planned retire",
                       "Retired year", "Status Detail"],
            "checks": [37], "confidence": "medium" if p["matched_by"] == ["parent"] else "high"}


def render_brief(state, data):
    L = [f"## Integrated resource plans for {state} (checklist rows 34 and 37)", ""]
    if data["skipped"]:
        L += [f"The US IRPs tab of the Update sheet has no rows for {state}, so the IRP step is "
              "skipped. If you find a utility integrated resource plan for this state while "
              "researching, say so in a question so the tab can gain a row.", ""]
        return "\n".join(L)
    L += ["Utilities in this state file integrated resource plans (IRPs) that name the gas "
          "units they intend to build, convert or retire. GEM records a planned unit from a "
          "plan's preferred portfolio as a project with the utility as owner, and ticks the "
          "unit's IRP box. A draft plan counts (Baird, October 2026).", "",
          "What to do for each utility below:", "",
          "1. Open the plan links. Download a PDF with curl and read it with pdftotext. "
          "Find the preferred, recommended or base portfolio and its table of additions, "
          "conversions, co-firing and retirements, with capacity and year.",
          "2. Compare with the GEM plants listed under the utility, and with the whole state "
          "list in the briefs. A unit GEM already has: report only a value the plan changes "
          "(status, capacity, start year, planned retirement), with the plan page as the source.",
          "3. A named gas unit the plan commits to that GEM lacks: write a new plant record "
          "(or a new unit at an existing plant) with the plan as the source, status announced "
          "unless the plan says construction has begun, the high end of any capacity range, "
          "and the utility as owner. Set irp true on the record.",
          "4. Capacity the plan commits to without a site: GEM's convention is a placeholder "
          "plant named \"<utility short name> <plan year> IRP power station <n>\" (see the "
          "existing names below). Write it as a new plant record with irp true. Capacity the "
          "plan only studies as an option, outside the preferred portfolio, goes on the watch "
          "list as new to the tracker, with the plan as the source.",
          "5. Say what the plan does not contain. A utility whose plan adds no gas gets one "
          "sentence in your summary so the tab's Notes can record it.",
          "6. Never stage the IRP column itself. The irp true flag on a finding tells the "
          "build which plants need the box ticked in the web form.", ""]
    if data["state_links"]:
        L += ["Regulator pages for the state: " + ", ".join(data["state_links"]), ""]
    for u in data["utilities"]:
        tag = f"{u['irp_year']}" if u["irp_year"] else "year not given"
        if u["is_draft"]:
            tag += ", draft"
        L += [f"### {u['utility']} ({tag})", ""]
        if u["links"]:
            L += ["Plan files: " + ", ".join(u["links"])]
        else:
            L += ["Plan files: none on the tab. Search the utility's site and the regulator's docket."]
        if u["file_note"]:
            L.append(f"Where to look in the file: {u['file_note']}")
        if u["updated_irp"]:
            L.append(f"Updated IRP column: {u['updated_irp']}")
        if u["next_irp_due"]:
            L.append(f"Next plan due: {u['next_irp_due']}")
        L.append("")
        if u["notes"]:
            L += ["Notes already on the tab, newest first:", ""]
            for n in u["notes"][:4]:
                q = f"{n['quarter']}: " if n["quarter"] else ""
                L.append(f"- {q}{n['text']}")
            if len(u["notes"]) > 4:
                L.append(f"- ({len(u['notes']) - 4} older entries not shown)")
            L.append("")
        if u["plants"]:
            L += ["GEM plants in the state tied to this utility:", ""]
            for p in u["plants"]:
                how = ", ".join(p["matched_by"])
                box = f"IRP box ticked on {p['irp_box_units']} of {len(p['units'])} units"
                st = ", ".join(p["statuses"]) or "no status"
                own = ("; its own brief carries an IRP task" if p.get("own_task")
                       else "; no task of its own, compare it here")
                L.append(f"- {p['plant_name']} ({p['plant_id']}): {len(p['units'])} unit(s), "
                         f"{st}; matched by {how}; {box}{own}")
            L.append("")
        else:
            L += ["GEM has no plant in the state tied to this utility by owner, operator, parent "
                  "or an IRP placeholder name. Anything the plan commits to is new.", ""]
    others = [u for u in data["irp_units"] if not u.get("matched_utility")]
    if others:
        L += ["Units with the IRP box ticked that no utility row above matched:", ""]
        for u in others:
            L.append(f"- {u['plant_name']} ({u['plant_id']}), unit {u['unit_name'] or u['unit_id']}, "
                     f"{u['status'] or 'no status'}, owners: {u['owners'] or 'blank'}")
        L.append("")
    L += ["Output: findings on tracked plants go in that plant's shard as usual. New plants, new "
          "units and watch items from the plans go in shards/_state.json under newplants, "
          "newunits and monitor, each with \"irp\": true. Then write one plain sentence per "
          "utility in meta.irp_summary of _state.json: what the plan adds, what was staged, "
          "and the next plan's due date if the plan or the tab gives one.", ""]
    return "\n".join(L)


def build_state(state, tab_states, csv_path, read_date):
    key = state.lower()
    slug = re.sub(r"\s+", "-", key)
    where = {"kind": "state", "name": state, "slug": slug, "country": "United States",
             "postal": ""}
    try:
        from build_state_brief import POSTAL
        where["postal"] = (POSTAL.get(key) or "").lower()
    except Exception:
        pass
    entry = tab_states.get(key)
    plants, has_irp = load_export(csv_path, state)
    data = {"where": where, "read": read_date, "source": {"spreadsheet_id": SPREADSHEET,
            "tab": TAB, "gid": GID, "url": SHEET_URL}, "export_has_irp_column": has_irp,
            "skipped": entry is None or not entry["rows"], "state_links": [],
            "utilities": [], "irp_units": [], "tasks": []}
    irp_units = []
    for pid, rows in plants.items():
        for r in rows:
            if ws(r.get("IRP")).lower() == "yes":
                u = unit_brief(r)
                u.update({"plant_id": pid, "plant_name": ws(r.get(H_PLANT)),
                          "owners": ws(r.get("Owner(s)")), "matched_utility": ""})
                irp_units.append(u)
    data["irp_units"] = irp_units
    if not data["skipped"]:
        data["state_links"] = list(dict.fromkeys(entry["links"]))
        for row in entry["rows"]:
            u = dict(row)
            u["plants"] = match_plants(plants, row)
            matched = {p["plant_id"] for p in u["plants"]}
            for iu in irp_units:
                if iu["plant_id"] in matched and not iu["matched_utility"]:
                    iu["matched_utility"] = row["utility"]
            for p in u["plants"]:
                p["own_task"] = task_worthy(p)
                if p["own_task"]:
                    data["tasks"].append(plant_task(row, p))
            data["utilities"].append(u)
    data["brief"] = render_brief(state, data)
    return data


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--state", action="append", required=True, help="a US state (repeatable)")
    ap.add_argument("--csv", default=str(gogpt_scoped_csv()), help="the GOGPT-scoped export")
    ap.add_argument("--from-json", default=None,
                    help="the tab's values saved earlier (list of rows); skips the sheet read")
    ap.add_argument("--save-json", default=None,
                    help="save the values read from the sheet here (under work/, never committed)")
    ap.add_argument("--out-dir", default=None, help="default: <repo>/work")
    a = ap.parse_args(argv)
    csv_path = Path(a.csv)
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found; run scope_filter.py first")
    if a.from_json:
        values = json.loads(Path(a.from_json).read_text(encoding="utf-8"))
        if isinstance(values, dict):
            values = values.get("values") or values.get("rows") or []
        read_date = datetime.date.fromtimestamp(Path(a.from_json).stat().st_mtime).isoformat()
    else:
        from gsheets import read_tab
        values = read_tab(SPREADSHEET, TAB)
        read_date = datetime.date.today().isoformat()
        if a.save_json:
            Path(a.save_json).write_text(json.dumps(values, ensure_ascii=False, indent=1),
                                         encoding="utf-8")
    tab_states = parse_tab(values)
    out_dir = Path(a.out_dir) if a.out_dir else work_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    for state in a.state:
        state = ws(state)
        data = build_state(state, tab_states, csv_path, read_date)
        slug = data["where"]["slug"]
        jp = out_dir / f"irp_us-{slug}.json"
        mp = out_dir / f"irp_us-{slug}.md"
        jp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        mp.write_text(data["brief"] + "\n", encoding="utf-8")
        if data["skipped"]:
            print(f"{state}: step skipped, no rows for {state} on the US IRPs tab "
                  f"({len(data['irp_units'])} unit(s) in the export already carry the IRP box). "
                  f"Wrote {jp}")
            continue
        n_pl = sum(len(u["plants"]) for u in data["utilities"])
        print(f"{state}: {len(data['utilities'])} utility row(s), {n_pl} GEM plant(s) matched, "
              f"{len(data['tasks'])} plant task(s), {len(data['irp_units'])} unit(s) with the IRP "
              f"box ticked. Wrote {jp} and {mp}")
        for u in data["utilities"]:
            names = ", ".join(p["plant_name"] for p in u["plants"]) or "no GEM plant matched"
            print(f"  {u['utility']} ({u['irp_year'] or 'year not given'}"
                  f"{', draft' if u['is_draft'] else ''}): {names}")


if __name__ == "__main__":
    main()
