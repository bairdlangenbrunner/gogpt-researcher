"""
Match a US state's GEM plants and units to EIA-860M, EIP (Oil & Gas Watch) and
the Sierra Club gas plant list, and turn what differs into research tasks.
This is the checklist's "GEM IDs matched to EIA-860M, EIP and Sierra Club"
item (QC/Country checklist row 38) plus the guide's 860M comparison step.

    python match_ids.py --state "New York"                 # batch start
    python match_ids.py --state Maryland --refresh         # re-read the two sheets now
    python match_ids.py --state Texas --eia-check          # look at eia.gov for a newer 860M file now

Reads:
    the scoped export (Other IDs (location) carries "EIA: <plant code>" and
    "EIP: <facility id>", Other IDs (unit) carries "EIA: <generator id>",
    comma-joined for a combined-cycle block) and the unfiltered export (so a
    coal plant that already holds an EIA code is not reported as new);
    EIA-860M, the newest local file under work/eia/ (eia860m.py keeps it
    current: eia.gov is checked at most once a week, the file changes monthly);
    the "EIP_GEM IDs matched" sheet, newest "<date> data filtered" tab
    (facility__id is the EIP id GEM records; the two "GEM ... (for EIP blanks)"
    columns are GEM's own matches; a "GEM Notes" cell starting "skipped" means
    the row was looked at and left alone);
    the Sierra Club "MATCHED IDs" tab (reference only, never cited, never
    shared outside GEM; ORIS Code is the EIA plant code, Unit Code the EIA
    generator id, GEM Location ID / GEM Unit ID are GEM's matches, "excluded"
    means out of GOGPT scope).
    Both sheets are read through gsheets.py (work profile, read-only) and
    cached under work/ids/ for 7 days.

Writes work/ids_<tag>.json and work/ids_<tag>.md (tag us-<state-slug>):
    tasks         research tasks for build_state_brief.py --ids: a status,
                  capacity or year that one of the three sources gives
                  differently from GEM, and a plant or unit match that needs
                  a person's confirmation
    ids_to_add    high-confidence IDs to type into the web UI's Other IDs
                  fields (the GEM database holds IDs without a Data Source,
                  and the staging contract has no Other IDs lane)
    sheet_fills   GEM IDs for the blank rows of the Sierra Club and EIP
                  sheets, for Baird to paste (writes to work sheets are his)
    leads         plants the sources list that are not in GEM at all
    problems      an EIA code GEM holds that the 860M file does not, a
                  duplicated EIP tag, and the like

Nothing is staged by this script; every ID and every change still goes
through the normal research and verification path. A Sierra Club value is
never a citation: the task says what their data shows and asks for a public
source.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import difflib
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

from build_state_brief import H_LOC, H_PLANT, H_UNAME, H_UNIT, make_scope
from eia860m import ensure_latest, load_generators
from gsheets import as_dicts, list_tabs, read_tab
from paths import REPO_ROOT, gem_export_csv, gogpt_scoped_csv, work_dir

EIP_SHEET = "14L3HqKEiP3GhHaWaotuf_pQiXvUT_xQtusokohch4Gg"
SC_SHEET = "11K84v5CPX38qb80ri8EFvPl2k2t7TR2MtWlZFXChAfc"
SC_TAB = "MATCHED IDs"
CACHE_DAYS = 7

GAS = {"NG", "PG", "OG", "BFG", "SGC", "SGP", "LNG"}
OIL = {"DFO", "RFO", "KER", "JF", "WO", "PC"}
FOSSIL = GAS | OIL

# EIA status codes to GEM status groups (lifecycle_rules.md vocabulary). The
# first entry is the reading; the whole set is what GEM may say without it
# counting as a difference (standby can be operating or mothballed, out of
# service can be mothballed or retired, EIA's canceled-or-postponed sheet
# covers both cancelled and shelved).
EIA_GROUP = {"OP": ["operating"], "SB": ["operating", "mothballed"], "OA": ["operating"],
             "OS": ["mothballed", "retired"],
             "P": ["announced"], "L": ["pre-construction"], "T": ["pre-construction"],
             "U": ["construction"], "V": ["construction"], "TS": ["construction"],
             "RE": ["retired"], "CN": ["cancelled"]}
EIP_GROUP = {"proposed": "in development", "under construction": "construction",
             "operating": "operating", "partially operating": "construction",
             "on hold": "shelved", "canceled": "cancelled", "cancelled": "cancelled"}
SC_GROUP = {"planned": "in development", "under construction": "construction",
            "operating": "operating", "terminated": "cancelled", "postponed": "shelved",
            "retired": "retired"}
# Differences inside "in development" (announced vs pre-construction) are not
# worth a task; everything else is.
IN_DEV = {"announced", "pre-construction", "in development"}

STOP = {"power", "station", "plant", "generating", "generation", "energy", "center",
        "centre", "facility", "project", "llc", "inc", "co", "company", "corp",
        "corporation", "the", "of", "and", "electric", "electricity", "gas", "natural",
        "turbine", "peaker", "peaking", "combined", "cycle", "unit", "units", "new",
        "lp", "l.p", "ltd", "partners", "holdings", "county", "city"}
MWNAME = re.compile(r"\b\d+(\.\d+)?\s*mw\b")


# ----------------------------------------------------------------- helpers
def ws(v):
    return (v or "").strip() if isinstance(v, str) else ("" if v is None or
                                                          (isinstance(v, float) and math.isnan(v))
                                                          else str(v).strip())


def num(v):
    s = ws(v).replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def year_of(v):
    s = ws(v)
    m = re.match(r"(\d{4})", s)
    return int(m.group(1)) if m else None


def norm_name(s):
    s = ws(s).lower()
    s = MWNAME.sub(" ", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    toks = [t for t in s.split() if t not in STOP]
    return toks


def name_sim(a, b):
    ta, tb = norm_name(a), norm_name(b)
    if not ta or not tb:
        return 0.0
    jac = len(set(ta) & set(tb)) / len(set(ta) | set(tb))
    seq = difflib.SequenceMatcher(None, " ".join(ta), " ".join(tb)).ratio()
    return max(jac, seq)


def km(lat1, lon1, lat2, lon2):
    if None in (lat1, lon1, lat2, lon2):
        return None
    p = math.pi / 180
    a = (0.5 - math.cos((lat2 - lat1) * p) / 2
         + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2)
    return 12742 * math.asin(math.sqrt(max(0.0, a)))


def parse_tags(cell):
    """'EIA: 6137, EIP: rec_x' -> [('EIA','6137'), ('EIP','rec_x')]."""
    out = []
    for part in re.split(r"[;,]\s*", ws(cell)):
        m = re.match(r"\s*([A-Za-z][A-Za-z0-9 _.\-/&]*?)\s*:\s*(.+?)\s*$", part)
        if m:
            out.append((m.group(1).strip().upper(), m.group(2).strip()))
        elif part.strip():
            out.append(("", part.strip()))
    return out


def tag_values(cell, system):
    return [v for s, v in parse_tags(cell) if s == system]


def gen_eq(a, b):
    a, b = ws(a), ws(b)
    return a == b or (a.lstrip("0") == b.lstrip("0") and a.lstrip("0") != "")


def eia_code(status):
    m = re.match(r"\(([A-Z]+)\)", ws(status))
    return m.group(1) if m else ""


def close(a, b, rel=0.10, abs_mw=5.0):
    if a is None or b is None:
        return True
    return abs(a - b) <= max(abs_mw, rel * max(abs(a), abs(b)))


def gem_group(status):
    s = ws(status).lower()
    for k in ("announced", "pre-construction", "construction", "operating", "mothballed",
              "retired", "shelved", "cancelled"):
        if s.startswith(k):
            return k
    return s


def groups_differ(gem, other):
    """other is one group or a list of acceptable groups."""
    others = [other] if isinstance(other, str) else list(other)
    if not gem or not others:
        return False
    for o in others:
        if gem == o or (gem in IN_DEV and o in IN_DEV):
            return False
    return True


def cap1(s):
    return s[:1].upper() + s[1:]


def fossil_row(r):
    fuel = ws(r.get("Energy Source Code"))
    if fuel:
        return fuel in FOSSIL
    t = ws(r.get("Technology")).lower()
    return "natural gas" in t or "petroleum" in t or "gas" in t


# ------------------------------------------------------------------ inputs
def load_gem(scope):
    """{plant_id: {"name", "rows": [...], "eia": [codes], "eip": [ids], "lat", "lon",
    "cap", "county", "city"}} for the state, plus the EIA codes every US row
    of the unfiltered export holds (any tracker)."""
    plants = {}
    with open(gogpt_scoped_csv(), encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if ws(r["Country/Area"]).lower() != "united states":
                continue
            if ws(r["State/Province"]).lower() != scope["name"].lower():
                continue
            pid = ws(r[H_LOC])
            p = plants.setdefault(pid, {"id": pid, "name": ws(r[H_PLANT]), "rows": []})
            p["rows"].append(r)
    for p in plants.values():
        first = p["rows"][0]
        p["eia"] = tag_values(first.get("Other IDs (location)"), "EIA")
        p["eip"] = tag_values(first.get("Other IDs (location)"), "EIP")
        p["lat"], p["lon"] = num(first.get("Latitude")), num(first.get("Longitude"))
        p["county"], p["city"] = ws(first.get("County")), ws(first.get("City"))
        caps = [num(r.get("Capacity (MW)")) for r in p["rows"]]
        p["cap"] = sum(c for c in caps if c) if any(caps) else None
        p["groups"] = {gem_group(r.get("Status")) for r in p["rows"]}
        p["other_ids"] = ws(first.get("Other IDs (location)"))
    all_eia = set()
    with open(gem_export_csv(), encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if ws(r.get("Country/Area")).lower() == "united states":
                all_eia.update(tag_values(r.get("Other IDs (location)"), "EIA"))
    return plants, all_eia


def cache_path(name):
    d = work_dir() / "ids"
    d.mkdir(parents=True, exist_ok=True)
    return d / name


def cached(name, refresh, loader):
    p = cache_path(name)
    if p.exists() and not refresh:
        d = json.loads(p.read_text(encoding="utf-8"))
        try:
            age = (dt.date.today() - dt.date.fromisoformat(d["read"])).days
        except (KeyError, ValueError):
            age = CACHE_DAYS
        if age < CACHE_DAYS:
            return d
    d = loader()
    d["read"] = dt.date.today().isoformat()
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return d


def newest_eip_tab():
    best = None
    for t in list_tabs(EIP_SHEET):
        m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{2,4})\s+data filtered", t["title"])
        if not m:
            continue
        mo, da, yr = (int(m.group(i)) for i in (1, 2, 3))
        yr = yr + 2000 if yr < 100 else yr
        key = (yr, mo, da)
        if best is None or key > best[0]:
            best = (key, t["title"])
    if not best:
        sys.exit("ERROR: no '<date> data filtered' tab on the EIP sheet")
    return best[1], dt.date(*best[0]).isoformat()


def load_eip(refresh):
    def loader():
        tab, date = newest_eip_tab()
        rows = as_dicts(read_tab(EIP_SHEET, tab))
        return {"tab": tab, "date": date, "rows": rows}
    return cached("eip.json", refresh, loader)


def load_sc(refresh):
    def loader():
        rows = as_dicts(read_tab(SC_SHEET, SC_TAB))
        hdr = [h for h in rows[0]] if rows else []
        status_col = next((h for h in hdr if h.lower().endswith("status") and "'" in h), "")
        return {"tab": SC_TAB, "status_col": status_col, "rows": rows}
    return cached("sierra_club.json", refresh, loader)


# ---------------------------------------------------------------- matching
class Match:
    def __init__(self, scope, plants, all_eia, gens, meta, eip, sc):
        self.scope, self.plants, self.all_eia = scope, plants, all_eia
        self.gens, self.eia_meta, self.eip, self.sc = gens, meta, eip, sc
        self.postal = scope["postal"].upper()
        self.eia_label = (f"the EIA-860M file for "
                          f"{self._month_label(meta.get('file', ''))}")
        self.tasks, self.ids_to_add, self.leads, self.problems = [], [], [], []
        self.sheet_fills = {"sierra_club": [], "eip": []}
        self._seen = set()
        self.eia_by_plant = {}
        self._index_eia()

    @staticmethod
    def _month_label(fname):
        m = re.match(r"([a-z]+)_generator(\d{4})", fname)
        return f"{m.group(1).capitalize()} {m.group(2)}" if m else "the newest month"

    # ---- EIA index: fossil generators of this state by plant
    def _index_eia(self):
        g = self.gens
        st = g[g["Plant State"] == self.postal]
        st = st[st.apply(fossil_row, axis=1)] if len(st) else st
        for pid, grp in st.groupby("Plant ID"):
            self.eia_by_plant[pid] = self.eia_plant(pid, grp)

    @staticmethod
    def eia_plant(pid, grp):
        gens = []
        for _, r in grp.iterrows():
            gens.append({"gen": ws(r["Generator ID"]), "unit_code": ws(r.get("Unit Code")),
                         "mw": num(r.get("Nameplate Capacity (MW)")),
                         "tech": ws(r.get("Technology")), "pm": ws(r.get("Prime Mover Code")),
                         "fuel": ws(r.get("Energy Source Code")),
                         "status": ws(r.get("Status")), "sheet": r["sheet"],
                         "op_year": year_of(r.get("Operating Year")),
                         "plan_year": year_of(r.get("Planned Operation Year")),
                         "ret_year": year_of(r.get("Retirement Year")),
                         "plan_ret": year_of(r.get("Planned Retirement Year")),
                         "lat": num(r.get("Latitude")), "lon": num(r.get("Longitude"))})
        first = grp.iloc[0]
        lat = next((x["lat"] for x in gens if x["lat"] is not None), None)
        lon = next((x["lon"] for x in gens if x["lon"] is not None), None)
        live = [x for x in gens if x["sheet"] in ("Operating", "Planned")]
        return {"id": pid, "name": ws(first["Plant Name"]), "county": ws(first.get("County")),
                "state": ws(first.get("Plant State")),
                "entity": ws(first.get("Entity Name")), "lat": lat, "lon": lon, "gens": gens,
                "mw": sum(x["mw"] for x in live if x["mw"]) or None,
                "mw_all": sum(x["mw"] for x in gens if x["mw"]) or None}

    def gen_groups(self, x):
        """Acceptable GEM groups for an EIA generator, the reading first."""
        if x["sheet"] == "Retired":
            return ["retired"]
        if x["sheet"] == "Canceled or Postponed":
            return ["cancelled", "shelved"]
        return EIA_GROUP.get(eia_code(x["status"]), [])

    def gen_group(self, x):
        g = self.gen_groups(x)
        return g[0] if g else ""

    def gen_desc(self, x):
        bits = [f"generator {x['gen']}"]
        if x["mw"]:
            bits.append(f"{x['mw']:g} MW")
        if x["tech"]:
            bits.append(x["tech"].lower())
        if x["sheet"] == "Retired":
            bits.append(f"retired {x['ret_year'] or ''}".strip())
        elif x["sheet"] == "Canceled or Postponed":
            bits.append("canceled or postponed")
        elif x["status"]:
            bits.append(x["status"].split(" ", 1)[1].lower() if " " in x["status"]
                        else x["status"])
        if x["op_year"]:
            bits.append(f"operating since {x['op_year']}")
        elif x["plan_year"]:
            bits.append(f"planned for {x['plan_year']}")
        return ", ".join(bits)

    def add_task(self, plant, unit, source, section, text, fields, confidence="high"):
        key = (plant["id"], unit[H_UNIT] if unit is not None else None, source, section)
        if key in self._seen:
            return
        self._seen.add(key)
        self.tasks.append({"plant_id": plant["id"], "plant_name": plant["name"],
                           "unit_id": unit[H_UNIT] if unit is not None else None,
                           "unit_name": ws(unit.get(H_UNAME)) if unit is not None else None,
                           "source": source, "section": section, "kind": "fix",
                           "task": text, "fields": fields, "confidence": confidence})

    def add_id(self, plant, unit, column, value, basis, confidence="high"):
        self.ids_to_add.append({"plant_id": plant["id"], "plant_name": plant["name"],
                                "unit_id": unit[H_UNIT] if unit is not None else None,
                                "unit_name": ws(unit.get(H_UNAME)) if unit is not None else None,
                                "column": column, "add": value,
                                "current": ws((unit if unit is not None else plant["rows"][0])
                                              .get(column)),
                                "basis": basis, "confidence": confidence})

    # ---- plant-level match of a GEM plant to an EIA plant
    def score_eia_plant(self, p, e):
        d = km(p["lat"], p["lon"], e["lat"], e["lon"])
        s = name_sim(p["name"], e["name"])
        score = 0.0
        if d is not None:
            score += 0.6 if d < 1.0 else 0.4 if d < 3.0 else 0.15 if d < 10.0 else -0.3
        if s >= 0.8:
            score += 0.5
        elif s >= 0.5:
            score += 0.3
        elif s >= 0.3:
            score += 0.1
        if p["cap"] and e["mw_all"] and close(p["cap"], e["mw_all"]):
            score += 0.2
        return score, d, s

    def best_eia_plant(self, p, exclude=()):
        cands = []
        for e in self.eia_by_plant.values():
            if e["id"] in exclude:
                continue
            score, d, s = self.score_eia_plant(p, e)
            if score >= 0.3:
                cands.append((score, d, s, e))
        cands.sort(key=lambda c: -c[0])
        return cands

    # ---- EIA
    def resolve_code(self, p, code):
        """The EIA plant GEM's code points at, or None after writing a problem."""
        e = self.eia_by_plant.get(code)
        if e is not None:
            return e
        anyst = self.gens[self.gens["Plant ID"] == code]
        if not len(anyst):
            self.problems.append(
                f"{p['name']} ({p['id']}) holds EIA plant code {code}, which is not in "
                f"{self.eia_label} at all. It may be a code typed wrong, or a plant that "
                "left the inventory.")
            return None
        # The code exists but no generator passed the gas or oil filter (blank
        # fuel, coal only, or another state): compare anyway and say so.
        e = self.eia_plant(code, anyst)
        fuels = sorted({x["fuel"] or "blank" for x in e["gens"]})
        if e["state"] != self.postal:
            self.problems.append(
                f"{p['name']} ({p['id']}) holds EIA plant code {code}, but {self.eia_label} "
                f"lists that code as \"{e['name']}\" in {e['state']}, not {self.postal}. "
                "Check the code.")
            return None
        self.problems.append(
            f"{p['name']} ({p['id']}) holds EIA plant code {code}; {self.eia_label} lists it "
            f"as \"{e['name']}\" with fuel {', '.join(fuels)} only, so it was compared "
            "without the gas and oil filter.")
        return e

    def sibling_code(self, p, es, claimed):
        """An unclaimed EIA plant nearby that holds the generator ids GEM's units
        carry but GEM's own code does not. EIA splits a plant into two codes when
        part of it changes hands or retires (Chalk Point Steam / Chalk Point Power)."""
        want = {gid for r in p["rows"] for gid in tag_values(r.get("Other IDs (unit)"), "EIA")}
        have = {x["gen"] for e in es for x in e["gens"]}
        missing = {g for g in want if not any(gen_eq(g, h) for h in have)}
        if not missing:
            return None
        best = None
        for e in self.eia_by_plant.values():
            if e["id"] in claimed:
                continue
            hits = {g for g in missing if any(gen_eq(g, x["gen"]) for x in e["gens"])}
            if not hits:
                continue
            d = km(p["lat"], p["lon"], e["lat"], e["lon"])
            s = name_sim(p["name"], e["name"])
            # A generator id like "1" is at every other plant, so the plant
            # must also be next door or share the name.
            if not ((d is not None and d <= 5.0) or s >= 0.5):
                continue
            key = (len(hits), s)
            if best is None or key > best[0]:
                best = (key, e, hits, d)
        if best is None:
            return None
        (n, s), e, hits, d = best
        if n < max(1, len(missing) // 2) and s < 0.5:
            return None
        return e, hits, d

    def run_eia(self):
        # EIA plant codes some GEM plant already holds, so a plant without a
        # code is never matched to its neighbor's code.
        claimed = {c for p in self.plants.values() for c in p["eia"]}
        for p in self.plants.values():
            if p["eia"]:
                es = [e for e in (self.resolve_code(p, c) for c in p["eia"]) if e is not None]
                sib = self.sibling_code(p, es, claimed)
                if sib:
                    e, hits, d = sib
                    claimed.add(e["id"])
                    where = f"{d:.1f} km from GEM's coordinates" if d is not None else ""
                    self.add_id(p, None, "Other IDs (location)", f"EIA: {e['id']}",
                                f"{self.eia_label} lists the generators GEM calls "
                                f"{', '.join(sorted(hits))} under plant {e['id']} "
                                f"\"{e['name']}\" ({e['county']} County{', ' + where if where else ''}), "
                                f"not under {', '.join(p['eia'])}. Keep the existing code and add "
                                "this one.")
                    es.append(e)
                if es:
                    self.compare_units(p, es)
                continue
            cands = self.best_eia_plant(p, exclude=claimed)
            cands = [c for c in cands if c[3]["mw_all"] and c[3]["mw_all"] >= 10]
            if not cands or cands[0][0] < 0.5:
                continue
            score, d, s, e = cands[0]
            where = (f"{d:.1f} km from GEM's coordinates" if d is not None
                     else "with no coordinates to compare")
            desc = "; ".join(self.gen_desc(x) for x in e["gens"][:6])
            if score >= 0.9 and (len(cands) == 1 or cands[1][0] < score - 0.3):
                claimed.add(e["id"])
                self.add_id(p, None, "Other IDs (location)", f"EIA: {e['id']}",
                            f"{self.eia_label} lists plant {e['id']} \"{e['name']}\" "
                            f"({e['county']} County), {where}, gas and oil generators: "
                            f"{desc}.")
                self.compare_units(p, [e])
            else:
                self.add_task(p, None, "eia", "IDs",
                              f"This plant has no EIA plant code. {cap1(self.eia_label)} "
                              f"has plant {e['id']} \"{e['name']}\" in {e['county']} County, "
                              f"{where}, with {desc}. If that is this plant, say so in a "
                              "question that gives the plant code and the generator IDs "
                              "for each unit. Do not report the codes as values.",
                              [], "medium")
        # EIA plants not in GEM anywhere
        for e in self.eia_by_plant.values():
            if e["id"] in claimed or e["id"] in self.all_eia:
                continue
            if not e["mw"] or e["mw"] < 50:
                continue
            live = [x for x in e["gens"] if x["sheet"] in ("Operating", "Planned")]
            groups = sorted({self.gen_group(x) for x in live} - {""})
            self.leads.append({"source": "eia", "name": e["name"], "ids": f"EIA: {e['id']}",
                               "county": e["county"], "owner": e["entity"],
                               "capacity_mw": round(e["mw"], 1), "status": ", ".join(groups),
                               "basis": f"{self.eia_label}: " + "; ".join(self.gen_desc(x)
                                                                           for x in live[:8])})

    def compare_units(self, p, es):
        """Units of GEM plant p against the generators of its EIA plants es."""
        rows = p["rows"]
        gens = [dict(x, plant=e["id"]) for e in es for x in e["gens"]]
        codes = ", ".join(e["id"] for e in es)
        taken = set()
        unmatched = []
        for r in rows:
            ids = tag_values(r.get("Other IDs (unit)"), "EIA")
            mine = []
            for gid in ids:
                hit = next((x for x in gens if gen_eq(x["gen"], gid)), None)
                if hit is None:
                    self.problems.append(
                        f"{p['name']} unit {ws(r.get(H_UNAME))} ({r[H_UNIT]}) holds EIA "
                        f"generator id {gid}, but {self.eia_label} has no gas or oil "
                        f"generator {gid} at plant {codes}.")
                    continue
                mine.append(hit)
                taken.add((hit["plant"], hit["gen"]))
            if mine:
                self.compare_unit(p, r, mine)
            else:
                unmatched.append(r)
        # Generator ids for units that have none, by capacity (and year / status).
        free = [x for x in gens if (x["plant"], x["gen"]) not in taken]
        groups = defaultdict(list)
        for x in free:
            groups[(x["plant"], x["unit_code"] or f"gen:{x['gen']}")].append(x)
        cand_groups = list(groups.values())
        for r in unmatched:
            cap = num(r.get("Capacity (MW)"))
            sy = year_of(r.get("Start year"))
            gg = gem_group(r.get("Status"))
            # A conversion unit ("timepoint 2") keeps EIA's original generator
            # and year, so the year says nothing about the match.
            conv = "timepoint" in ws(r.get(H_UNAME)).lower()
            fits = []
            for grp in cand_groups:
                mw = sum(x["mw"] for x in grp if x["mw"]) or None
                if cap and mw and not close(cap, mw):
                    continue
                score = 1.0
                yrs = {x["op_year"] or x["plan_year"] for x in grp} - {None}
                if sy and yrs and not conv:
                    score += 0.5 if sy in yrs else -0.5
                if gg and grp and not any(groups_differ(gg, self.gen_groups(x)) for x in grp):
                    score += 0.3
                fits.append((score, grp))
            if not fits:
                continue
            fits.sort(key=lambda f: -f[0])
            best = fits[0][1]
            unique = len(fits) == 1 or fits[1][0] < fits[0][0]
            value = ", ".join(f"EIA: {x['gen']}" for x in best)
            desc = "; ".join(self.gen_desc(x) for x in best)
            if unique and fits[0][0] >= 1.3:
                cand_groups.remove(best)
                self.add_id(p, r, "Other IDs (unit)", value,
                            f"{self.eia_label}, plant {best[0]['plant']}: {desc}; GEM capacity "
                            f"{ws(r.get('Capacity (MW)')) or 'blank'} MW, start year "
                            f"{ws(r.get('Start year')) or 'blank'}.")
                self.compare_unit(p, r, best)
            else:
                others = "; ".join(" + ".join(x["gen"] for x in grp) for _, grp in fits[1:4])
                self.add_task(p, r, "eia", "IDs",
                              f"This unit has no EIA generator id. {cap1(self.eia_label)} "
                              f"lists at plant {best[0]['plant']}: {desc}"
                              + (f" (other possible matches: {others})" if others else "")
                              + ". Say in a question which generator id or ids belong to "
                              "this unit; do not report them as values.",
                              [], "medium")

    def compare_unit(self, p, r, mine):
        gg = gem_group(r.get("Status"))
        src = f"{self.eia_label} (plant {mine[0]['plant']})"
        # Status
        diff = [x for x in mine if groups_differ(gg, self.gen_groups(x))]
        if diff and len(diff) == len(mine):
            x = diff[0]
            self.add_task(p, r, "eia", "Status",
                          f"{cap1(src)} shows {self.gen_desc(x)}, which reads as "
                          f"{self.gen_group(x)}, while GEM says {ws(r.get('Status'))}. "
                          "Check which is right and report the status with a public source. "
                          "A status change needs two independent publishers for high confidence.",
                          ["Status", "Status Detail"] + self.year_fields(self.gen_group(x)))
            return
        # Capacity
        cap = num(r.get("Capacity (MW)"))
        mw = sum(x["mw"] for x in mine if x["mw"]) or None
        if cap and mw and not close(cap, mw):
            self.add_task(p, r, "eia", "Capacity",
                          f"{cap1(src)} gives {mw:g} MW nameplate for "
                          f"{' + '.join(x['gen'] for x in mine)}, while GEM says {cap:g} MW. "
                          "Check the nameplate electric capacity and report it with a source.",
                          ["Capacity (MW)"])
        # Years
        sy = year_of(r.get("Start year"))
        oy = {x["op_year"] for x in mine} - {None}
        if gg == "operating" and oy and sy and sy not in oy and abs(sy - max(oy)) > 1:
            self.add_task(p, r, "eia", "Start year",
                          f"{cap1(src)} gives operating year "
                          f"{', '.join(str(y) for y in sorted(oy))}, while GEM's start year is "
                          f"{sy}. Check which is right.", ["Start year"])
        if gg == "operating" and oy and not sy:
            self.add_task(p, r, "eia", "Start year",
                          f"Start year is blank. {cap1(src)} gives operating year "
                          f"{', '.join(str(y) for y in sorted(oy))}. Confirm and report it.",
                          ["Start year"])
        ry = year_of(r.get("Retired year"))
        ery = {x["ret_year"] for x in mine} - {None}
        if gg == "retired" and ery and ry and ry not in ery:
            self.add_task(p, r, "eia", "Retired year",
                          f"{cap1(src)} gives retirement year "
                          f"{', '.join(str(y) for y in sorted(ery))}, while GEM says {ry}. "
                          "Check which is right.", ["Retired year"])
        if gg == "retired" and ery and not ry:
            self.add_task(p, r, "eia", "Retired year",
                          f"Retired year is blank. {cap1(src)} gives "
                          f"{', '.join(str(y) for y in sorted(ery))}. Confirm and report it.",
                          ["Retired year"])
        pr = year_of(r.get("Planned retire"))
        epr = {x["plan_ret"] for x in mine} - {None}
        if gg == "operating" and epr and pr not in epr:
            self.add_task(p, r, "eia", "Planned retire",
                          f"{cap1(src)} gives a planned retirement year of "
                          f"{', '.join(str(y) for y in sorted(epr))}"
                          + (f", while GEM says {pr}" if pr else ", and GEM has none")
                          + ". Check the plan and report it with a source.",
                          ["Planned retire"])
        py = {x["plan_year"] for x in mine} - {None}
        if gg in IN_DEV and py and sy and sy not in py:
            self.add_task(p, r, "eia", "Start year",
                          f"{cap1(src)} gives a planned operation year of "
                          f"{', '.join(str(y) for y in sorted(py))}, while GEM's start year is "
                          f"{sy}. Check which is current.", ["Start year"])

    @staticmethod
    def year_fields(group):
        return {"operating": ["Start year"], "retired": ["Retired year"],
                "cancelled": ["Cancellation year"], "cancelled or postponed":
                ["Cancellation year", "Latest Activity"], "mothballed": [],
                "construction": ["Start year"]}.get(group, [])

    # ---- EIP
    def run_eip(self):
        rows = [r for r in self.eip["rows"] if ws(r.get("facility__state")).upper() == self.postal]
        label = f"the EIP Oil & Gas Watch data of {self.eip['date']}"
        for r in rows:
            note = ws(r.get("GEM Notes")).lower()
            fid = ws(r.get("facility__id"))
            name = ws(r.get("facility__facility_name"))
            gem_loc = (ws(r.get("facility__gaspower_gemlocationid"))
                       or ws(r.get("GEM Location ID (for EIP blanks)")))
            gem_unit = (ws(r.get("project__gaspower_gemunitid"))
                        or ws(r.get("GEM Unit ID (for EIP blanks)")))
            status = ws(r.get("project__operatingstatus"))
            cap = num(r.get("project__gaspower_generatingcapacity_mw"))
            link = ws(r.get("OGWLink")) or (f"https://oilandgaswatch.org/facility/{fid}" if fid else "")
            p = self.plants.get(gem_loc) if gem_loc.startswith("L") else None
            if p is None and gem_loc.startswith("L"):
                self.problems.append(f"EIP row \"{name}\" points at {gem_loc}, which is not a "
                                     f"{self.scope['name']} plant in the scoped export.")
            if p is None and not note.startswith("skipped"):
                # match by name / city / county
                best = None
                for q in self.plants.values():
                    s = name_sim(name, q["name"])
                    if ws(r.get("facility__city")) and q["city"] and \
                            ws(r.get("facility__city")).lower() == q["city"].lower():
                        s += 0.2
                    if cap and q["cap"] and close(cap, q["cap"]):
                        s += 0.15
                    if best is None or s > best[0]:
                        best = (s, q)
                if best and best[0] >= 0.75:
                    p = best[1]
                    conf = "high" if best[0] >= 0.95 else "medium"
                    unit_hint = p["rows"][0][H_UNIT] if len(p["rows"]) == 1 else ""
                    self.sheet_fills["eip"].append({
                        "facility_id": fid, "facility_name": name, "eip_status": status,
                        "capacity_mw": cap, "gem_location_id": p["id"], "gem_plant_name": p["name"],
                        "gem_unit_id": unit_hint, "confidence": conf,
                        "basis": f"name match {best[0]:.2f}" + (", one unit in GEM" if unit_hint
                                                              else f", {len(p['rows'])} units in GEM")})
                    if conf != "high":
                        what = f"\"{name}\" ({status.lower() or 'status unknown'}"
                        what += f", {cap:g} MW)" if cap else ")"
                        self.add_task(p, None, "eip", "IDs",
                                      f"{cap1(label)} has a facility {what} that may be this "
                                      f"plant: {link}. Say in a question whether it is, and if "
                                      f"so give the EIP facility id {fid}; do not report it as "
                                      "a value.", [], "medium")
                        continue
                elif not gem_loc:
                    self.leads.append({"source": "eip", "name": name, "ids": f"EIP: {fid}",
                                       "county": ws(r.get("facility__countyorparish")),
                                       "owner": "", "capacity_mw": cap,
                                       "status": status, "basis": f"{label}: {link}"
                                       + (f"; GEM note: {ws(r.get('GEM Notes'))}" if note else "")})
                    continue
            if p is None:
                continue
            # the EIP id in Other IDs (location)
            if fid and fid not in p["eip"]:
                old = [x for x in p["eip"] if x.startswith("rec_")]
                self.add_id(p, None, "Other IDs (location)", f"EIP: {fid}",
                            f"{label}: facility \"{name}\" ({link}) is matched to this plant "
                            + (f"by the EIP sheet. GEM holds an older EIP record id "
                               f"{old[0]}; keep it and add the current facility id."
                               if old else "by the EIP sheet."))
            if len(p["eip"]) != len(set(p["eip"])):
                self.problems.append(f"{p['name']} ({p['id']}): Other IDs (location) repeats "
                                     f"the same EIP id ({p['other_ids']}).")
            # status
            eg = EIP_GROUP.get(status.lower(), "")
            unit = next((u for u in p["rows"] if u[H_UNIT] == gem_unit), None)
            targets = [unit] if unit is not None else p["rows"]
            for u in targets:
                gg = gem_group(u.get("Status"))
                if eg and groups_differ(gg, eg):
                    self.add_task(p, u, "eip", "Status",
                                  f"{cap1(label)} lists \"{name}\" as "
                                  f"{status.lower()} ({link}), while GEM says {ws(u.get('Status'))}. "
                                  "Check which is right and report the status with a public "
                                  "source; EIP's own source documents are a good start.",
                                  ["Status", "Status Detail"] + self.year_fields(eg))
                    break
            ey = year_of(r.get("project__currentexpectedoperatingyear"))
            if unit is not None and ey and gem_group(unit.get("Status")) in IN_DEV:
                sy = year_of(unit.get("Start year"))
                if sy and sy != ey:
                    self.add_task(p, unit, "eip", "Start year",
                                  f"{cap1(label)} expects operation in {ey} ({link}), "
                                  f"while GEM's start year is {sy}. Check which is current.",
                                  ["Start year"])

    # ---- Sierra Club
    def run_sc(self):
        rows = [r for r in self.sc["rows"] if ws(r.get("State")).upper() == self.postal]
        scol = self.sc.get("status_col") or next((h for h in (rows[0] if rows else {})
                                                  if h.lower().endswith("status")), "")
        label = f"the Sierra Club list ({scol.replace(' Status', '')}, reference only, never cited)"
        by_eia = {}
        for p in self.plants.values():
            for c in p["eia"]:
                by_eia.setdefault(c, []).append(p)
        for r in rows:
            loc, unit = ws(r.get("GEM Location ID")), ws(r.get("GEM Unit ID"))
            if loc.lower() == "excluded":
                continue
            oris, ucode = ws(r.get("ORIS Code")), ws(r.get("Unit Code"))
            oris = re.sub(r"\.0$", "", oris)
            name = ws(r.get("Power Plant"))
            cap = num(r.get("Unit Nameplate Capacity (MW)"))
            status = ws(r.get(scol)) if scol else ""
            check = ws(r.get("Check against Jan 26 SC data")) or next(
                (ws(v) for k, v in r.items() if k.lower().startswith("check against")), "")
            p = self.plants.get(loc) if loc.startswith("L") else None
            u = None
            if p is not None and unit.startswith("G"):
                u = next((x for x in p["rows"] if x[H_UNIT] == unit), None)
            if p is None:
                cands = by_eia.get(oris, []) if oris else []
                basis = ""
                if len(cands) == 1:
                    p = cands[0]
                    basis = f"ORIS code {oris} equals the plant's EIA code"
                elif not cands:
                    best = max(((name_sim(name, q["name"]), q) for q in self.plants.values()),
                               key=lambda t: t[0], default=None)
                    if best and best[0] >= 0.85:
                        p = best[1]
                        basis = f"name match {best[0]:.2f}"
                if p is None:
                    live = status.lower() in ("planned", "under construction", "operating")
                    if not loc and (live or check.upper().startswith("ADDED")):
                        self.leads.append({"source": "sierra_club", "name": name,
                                           "ids": f"ORIS {oris}, unit {ucode}" if oris and oris != "0"
                                           else "", "county": "", "owner": ws(r.get("Owner")),
                                           "capacity_mw": cap, "status": status,
                                           "basis": f"{label}: "
                                           + ("newly added row" if check.upper().startswith("ADDED")
                                              else "no GEM match")})
                    continue
            # unit, when the sheet does not name one
            sg = SC_GROUP.get(status.lower(), "")
            if u is None:
                if ucode:
                    u = next((x for x in p["rows"] if any(gen_eq(g, ucode) for g in
                                                          tag_values(x.get("Other IDs (unit)"), "EIA"))),
                             None)
                # Only-unit and same-capacity guesses hold only when the status
                # agrees too; otherwise the row is probably a different project
                # at the same site (a terminated repowering, say).
                guess = None
                if u is None and len(p["rows"]) == 1:
                    guess = p["rows"][0]
                if u is None and guess is None and cap:
                    fits = [x for x in p["rows"] if close(cap, num(x.get("Capacity (MW)")) or -1)]
                    if len(fits) == 1:
                        guess = fits[0]
                if guess is not None and not (sg and groups_differ(gem_group(guess.get("Status")), sg)):
                    u = guess
            if not loc.startswith("L"):
                self.sheet_fills["sierra_club"].append({
                    "plant_key_unit_code": ws(r.get("Plant Key_Unit Code")),
                    "power_plant": name, "unit_code": ucode, "oris": oris,
                    "gem_location_id": p["id"], "gem_plant_name": p["name"],
                    "gem_unit_id": u[H_UNIT] if u is not None else "",
                    "gem_unit_name": ws(u.get(H_UNAME)) if u is not None else "",
                    "basis": basis + ("" if u is not None else
                                      f"; unit not resolved among {len(p['rows'])} GEM units")})
            if p is None:
                continue
            # status and the sheet's own check flags
            flagged = check.upper().startswith("CHECK")
            if u is not None:
                gg = gem_group(u.get("Status"))
                if sg and groups_differ(gg, sg):
                    self.add_task(p, u, "sierra_club", "Status",
                                  f"{cap1(label)} shows this unit as {status.lower()}, "
                                  f"while GEM says {ws(u.get('Status'))}. Find a public source "
                                  "that settles the status; never cite the Sierra Club data.",
                                  ["Status", "Status Detail"] + self.year_fields(sg))
                    continue
            elif sg and all(groups_differ(gem_group(x.get("Status")), sg) for x in p["rows"]):
                # A row matched to the plant but to none of its units, with a
                # status no unit has: usually a separate proposal at the site.
                units = "; ".join(f"{ws(x.get(H_UNAME))} ({gem_group(x.get('Status'))})"
                                  for x in p["rows"][:6])
                self.add_task(p, None, "sierra_club", "Unit " + ucode,
                              f"{cap1(label)} has a row \"{name}\" unit {ucode or '?'} "
                              f"({status.lower()}"
                              + (f", {cap:g} MW" if cap else "") + ") matched to this plant, "
                              f"but no GEM unit here has that status (GEM units: {units}). It "
                              "may be a project GEM holds under another plant or not at all. "
                              "Say in a question what it is and whether GEM should hold it; "
                              "never cite the Sierra Club data.", [], "medium")
                continue
            if flagged:
                what = check.replace("CHECK", "").strip(" -").strip() or "a change"
                self.add_task(p, u, "sierra_club", "Check",
                              f"{cap1(label)} flags {what} for "
                              + ("this unit" if u is not None else f"unit {ucode or '?'}")
                              + f", with status {status.lower() or 'not given'}"
                              + (f" and {cap:g} MW" if cap else "")
                              + ". Look for a public source that shows what changed and "
                              "report it; never cite the Sierra Club data.",
                              ["Status", "Capacity (MW)", "Turbine/Engine Technology",
                               "Owner(s)"], "medium")

    def run(self):
        self.run_eia()
        self.run_eip()
        self.run_sc()
        self.mark_staged_leads()

    def mark_staged_leads(self):
        """A lead whose id already appears in a batch's staging files (a discovery
        pass that has not been applied yet) is marked, not dropped."""
        staged = {}
        # both the update staging dir and the discovery one; the code may be written
        # as "EIA: 2494", "EIA plant 2494" or inside a record id like "eia2494"
        for f in (REPO_ROOT / "batches").glob("*/staging*/**/*.json"):
            try:
                text = f.read_text(encoding="utf-8")
            except OSError:
                continue
            for d in self.leads:
                key = d["ids"].split(",")[0].strip()
                src, _, val = key.partition(":")
                val = val.strip()
                if not val:
                    continue
                pat = re.compile(rf"\b{re.escape(src)}\W{{0,12}}{re.escape(val)}\b", re.I)
                if pat.search(text):
                    staged.setdefault(id(d), set()).add(f.relative_to(REPO_ROOT).parts[1])
        for d in self.leads:
            b = staged.get(id(d))
            d["staged_in"] = sorted(b) if b else []
            if b:
                d["basis"] = f"already staged in batch {', '.join(sorted(b))}; " + d["basis"]


# ------------------------------------------------------------------ output
def memo(scope, out):
    L = [f"# ID matching for {scope['name']}", "",
         f"Read {out['read']}. Sources: {out['sources']['eia860m']['file']} "
         f"(EIA-860M, released {out['sources']['eia860m'].get('release_date') or 'date unknown'}), "
         f"the EIP tab \"{out['sources']['eip']['tab']}\", and the Sierra Club tab "
         f"\"{out['sources']['sierra_club']['tab']}\" (reference only; never cite or share it).",
         "", f"GEM plants checked: {out['plants_checked']}. Research tasks: {len(out['tasks'])}. "
         f"IDs to add by hand: {len(out['ids_to_add'])}. Sheet rows to fill: "
         f"{len(out['sheet_fills']['sierra_club'])} Sierra Club, {len(out['sheet_fills']['eip'])} EIP. "
         f"Possible new plants: {len(out['leads'])}. Problems: {len(out['problems'])}.", ""]
    ids = out["ids_to_add"]
    L += ["## IDs to add in the web UI", ""]
    if ids:
        L += ["These matches are confident. Type the value into the Other IDs field, keeping "
              "what is already there.", "",
              "| Plant | Unit | Field | Add | Already there | Why |", "|---|---|---|---|---|---|"]
        for i in ids:
            L.append(f"| {i['plant_name']} ({i['plant_id']}) | "
                     f"{(i['unit_name'] or '') + (' (' + i['unit_id'] + ')' if i['unit_id'] else '')} | "
                     f"{i['column']} | {i['add']} | {i['current'] or 'blank'} | {i['basis']} |")
    else:
        L.append("None.")
    L.append("")
    L += ["## Research tasks", ""]
    if out["tasks"]:
        L.append("These go into the briefs through `build_state_brief.py --ids`.")
        L.append("")
        byp = defaultdict(list)
        for t in out["tasks"]:
            byp[(t["plant_name"], t["plant_id"])].append(t)
        for (pn, pid), ts in sorted(byp.items()):
            L.append(f"### {pn} ({pid})")
            L.append("")
            for t in ts:
                who = (f"{t['unit_name']} ({t['unit_id']})" if t["unit_id"] else "whole plant")
                L.append(f"- {who}: {t['task']}")
            L.append("")
    else:
        L += ["None.", ""]
    for key, title, cols in (
            ("sierra_club", "Sierra Club sheet: GEM IDs for blank rows",
             ["plant_key_unit_code", "power_plant", "unit_code", "oris", "gem_location_id",
              "gem_unit_id", "gem_plant_name", "basis"]),
            ("eip", "EIP sheet: GEM IDs for blank rows",
             ["facility_id", "facility_name", "eip_status", "capacity_mw", "gem_location_id",
              "gem_unit_id", "gem_plant_name", "confidence", "basis"])):
        L += [f"## {title}", ""]
        rows = out["sheet_fills"][key]
        if rows:
            L += ["For Baird to paste into the sheet (the repo never writes to work sheets). "
                  "A blank unit id means the plant matched but the unit did not; pick it by hand.",
                  "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
            for r in rows:
                L.append("| " + " | ".join(ws(r.get(c)) if r.get(c) is not None else ""
                                           for c in cols) + " |")
        else:
            L.append("None.")
        L.append("")
    L += ["## Possible new plants", ""]
    if out["leads"]:
        L += ["Listed by a source but matched to no GEM plant. Each is a discovery lead, "
              "not a finding: check the 50 MW threshold and the usual evidence bar before "
              "staging anything.", "",
              "| Source | Name | IDs | County | Owner | MW | Status | Basis |", "|---|---|---|---|---|---|---|---|"]
        for d in out["leads"]:
            L.append(f"| {d['source']} | {d['name']} | {d['ids']} | {d['county']} | {d['owner']} | "
                     f"{d['capacity_mw'] if d['capacity_mw'] is not None else ''} | {d['status']} | "
                     f"{d['basis']} |")
    else:
        L.append("None.")
    L.append("")
    L += ["## Problems", ""]
    L += [f"- {x}" for x in out["problems"]] or ["None."]
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--state", required=True, help="a US state, e.g. Maryland")
    ap.add_argument("--refresh", action="store_true", help="re-read the EIP and Sierra Club sheets")
    ap.add_argument("--eia-check", action="store_true", help="check eia.gov for a newer file now")
    ap.add_argument("--out-dir", default=None)
    a = ap.parse_args()
    scope = make_scope(state=a.state)
    tag = f"us-{scope['slug']}"
    out_dir = Path(a.out_dir) if a.out_dir else work_dir()

    plants, all_eia = load_gem(scope)
    if not plants:
        sys.exit(f"ERROR: no {scope['name']} rows in the scoped export")
    path, meta = ensure_latest(force=a.eia_check)
    gens = load_generators(path)
    eip = load_eip(a.refresh)
    sc = load_sc(a.refresh)

    m = Match(scope, plants, all_eia, gens, {**meta, "file": path.name}, eip, sc)
    m.run()
    out = {"where": scope, "read": dt.date.today().isoformat(),
           "sources": {"eia860m": {"file": path.name, "release_date": meta.get("release_date", ""),
                                   "url": meta.get("url", "")},
                       "eip": {"tab": eip["tab"], "date": eip["date"], "read": eip["read"]},
                       "sierra_club": {"tab": sc["tab"], "read": sc["read"]}},
           "plants_checked": len(plants), "tasks": m.tasks, "ids_to_add": m.ids_to_add,
           "sheet_fills": m.sheet_fills, "leads": m.leads, "problems": m.problems}
    jp = out_dir / f"ids_{tag}.json"
    mp = out_dir / f"ids_{tag}.md"
    jp.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    mp.write_text(memo(scope, out), encoding="utf-8")
    print(f"state: {scope['name']}  plants: {len(plants)}  EIA file: {path.name}  "
          f"EIP tab: {eip['tab']}")
    print(f"tasks: {len(m.tasks)}  ids to add: {len(m.ids_to_add)}  sheet fills: "
          f"{len(m.sheet_fills['sierra_club'])} SC / {len(m.sheet_fills['eip'])} EIP  "
          f"leads: {len(m.leads)}  problems: {len(m.problems)}")
    print(f"wrote {jp}\nwrote {mp}")


if __name__ == "__main__":
    main()
