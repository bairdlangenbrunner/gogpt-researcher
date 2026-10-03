#!/usr/bin/env python3
"""
Assemble a US state batch: turn the per-plant research shards into the staged
lane files (and, in blind mode, the calibration comparison and memo).

Contract: notes/us_state_agent_plan.md (directory layout, modes, shard
contract, staged record additions, calibration memo) and
docs/reference/staged_json_schema.md (the lane files). Free text this script
writes (the `action` line, appended notes, the memo) follows
docs/reference/notes_style.md.

    python assemble_state.py --batch ../batches/us-md \
        [--csv gem_export_gogpt_scoped.csv] [--stamp YYYYMMDD_HHMM_ET] \
        [--quarter q4-2026]

Inputs
  briefs/_index.json         plants, unit IDs, mode (blind | update), csv path
  shards/<L...>.json         one per plant, written by the research subagent
  shards/_state.json         optional: statewide qa/monitor items (new plants,
                             gas-fired data centers) from the state-level search
  the fresh export           --csv, else the `csv` named in _index.json, else
                             scripts/gem_export_gogpt_scoped.csv
  briefs/_hidden/<L...>.json blind mode only: the withheld GEM values

Outputs (staging/ is overwritten on every run; it is the pending-state store,
and `record_id` is stable so review decisions survive a rebuild)
  staging/staged_updates.json   staging/staged_qa.json
  staging/staged_monitor.json   staging/staged_newunits.json
  staging/staged_entity.json    (all five always written, empty if nothing)
  staging/comparison.json            blind mode only
  calibration_<stamp>_ET.md          blind mode only, in the batch dir; never
                                     overwritten (rerun for a fresh stamp)

How each finding is judged
  Every finding (unit-level `units[].findings`, and plant-level
  `plant_findings`, which apply to every unit of the plant) is compared with
  the export's current cell for that unit:
    numbers   Capacity (MW) / Capacity Per Engine equal within 0.5 MW or 1%;
              Number Of Engines and the year columns compared as integers;
              Latitude / Longitude equal within 0.005 degrees
    Status    case-insensitive; "shelved - inferred 2 y" with a hyphen, en
              dash or em dash all equal (staged values use the hyphen form the
              live DB stores)
    owners    Owner(s) / Operator(s): whitespace, case, commas and periods
              ignored; "[100%]", "[100.0%]" and "(100%)" equal; a lone name
              with no share counts as 100%; order of the ";" list ignored
    fuel      "fossil gas: natural gas" equals "natural gas" (category prefix
              dropped, token set compared)
    tech      "CC" equals "combined cycle" (and the other abbreviations)
    other     whitespace-normalized, case-insensitive text
  Verdicts: match | fill (GEM blank, research has a value) | change |
  research_blank (research found nothing, GEM has a value; only from
  `not_found`) | both_blank. Blind mode adds not_reported (GEM has a value
  and the shard neither reported the field nor listed it in `not_found`);
  that verdict lives only in the comparison and memo.

What becomes a staged record (one record per unit and field; `cluster` = the
unit ID so the build can group a unit's edits)
  fill, change     updates record: fields / current / refs (keyed by the Data
                   Source column via build_review_package.ref_col_for) /
                   verifications / tier / independent / source_language "en" /
                   researcher_notes (the finding's note, plus the unit's notes
                   on the unit's first record) / action / record_id
                   `<plant_id>:<unit_id>:<field slug>`.
                   With no URL at all: kept with empty refs only when the value
                   is an inferred status; otherwise it goes to the qa lane
                   (concern_type "other", the value in `proposed_value`).
  match + new URL  updates record with `reverified: true`, fields = the
                   export's current string (so the workbook colors it blue),
                   refs = only the URLs not already in the Data Source cell.
  match, no new URL  no record, counted.
  Status change at tier high with fewer than two distinct hosts among the
  verified URLs is lowered to medium here, with a plain sentence appended to
  the note (a status change needs two independent publishers for green).

Plant-level findings become ONE record: `applies_to_all_units: true`,
`sibling_unit_ids`, `sibling_current` {unit_id: current cell} (so the gate can
check every unit), anchored on the first unit whose verdict is fill/change
(else the first unit), record_id `<plant_id>:plant:<field slug>`.

The shard's qa / monitor / newunits / entities sections pass through to their
lane files with identity and a record_id added. A shard's list-shaped `refs`
on qa / monitor items is stored as {"links": [...]}, since those items have no
value column to key on.

Nothing here verifies URLs or judges sources: run state_gate.py next; it
must print GATE CLEAN before build_review_package.py.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_review_package import _split_urls, ref_col_for  # noqa: E402
from paths import gogpt_scoped_csv  # noqa: E402
from schema_constants import RESEARCH_FIELDS  # noqa: E402

ET = ZoneInfo("America/New_York")
COUNTRY = "United States"
LANE_FILES = ["updates", "qa", "monitor", "newunits", "entity"]

CAPACITY_FIELDS = {"Capacity (MW)", "Capacity Per Engine"}
INT_FIELDS = {"Number Of Engines", "Start year", "Retired year",
              "Planned retire", "Cancellation year"}
COORD_FIELDS = {"Latitude", "Longitude"}
COORD_TOL = 0.005
ENTITY_FIELDS = {"Owner(s)", "Operator(s)"}
TECH_ABBR = {"CC": "combined cycle", "GT": "gas turbine",
             "AGT": "aeroderivative gas turbine", "ST": "steam turbine",
             "IC": "internal combustion",
             "ICCC": "internal combustion combined cycle",
             "ISCC": "integrated solar combined cycle",
             "AFC": "allam-fetvedt cycle"}
VERDICTS = ["match", "fill", "change", "research_blank", "both_blank",
            "not_reported"]
VERDICT_MEANING = {
    "match": "GEM and the research agree",
    "fill": "GEM is blank and the research found a value",
    "change": "GEM and the research disagree",
    "research_blank": "GEM has a value and the research found nothing",
    "both_blank": "both are blank",
    "not_reported": "GEM has a value and the research did not mention the field",
}
DOWNGRADE_NOTE = ("Only one publisher reports this status change. It needs a "
                  "second, independent source before it counts as fully "
                  "confirmed.")
SHARE_RE = re.compile(r"[\[(]\s*(\d+(?:\.\d+)?)\s*%\s*[\])]")


# ---------------------------------------------------------------- helpers ---

def now_et() -> datetime.datetime:
    return datetime.datetime.now(ET)


def ws(v) -> str:
    """Whitespace-normalized string ('' for None)."""
    return re.sub(r"\s+", " ", "" if v is None else str(v)).strip()


def is_blank(v) -> bool:
    return ws(v) == ""


def to_float(v):
    try:
        return float(ws(v).replace(",", ""))
    except ValueError:
        return None


def norm_status(v) -> str:
    """Lowercase; inferred variants written with the hyphen the DB stores."""
    s = ws(v).lower()
    return re.sub(r"\s*[-–—]\s*inferred", " - inferred", s)


def norm_entities(v):
    parts = []
    for p in (x for x in ws(v).split(";") if x.strip()):
        m = SHARE_RE.search(p)
        share = float(m.group(1)) if m else None
        name = ws(re.sub(r"[.,]", "", SHARE_RE.sub("", p)).lower())
        parts.append([name, share])
    if len(parts) == 1 and parts[0][1] is None:
        parts[0][1] = 100.0
    return tuple(sorted((n, None if s is None else round(s, 1))
                        for n, s in parts))


def norm_fuel(v):
    return {t.split(":", 1)[-1].strip().lower()
            for t in ws(v).split(",") if t.strip()}


def norm_tech(v) -> str:
    s = ws(v)
    return TECH_ABBR.get(s.upper(), s.lower())


def values_equal(field: str, gem, research) -> bool:
    if is_blank(gem) and is_blank(research):
        return True
    if is_blank(gem) or is_blank(research):
        return False
    if field == "Status":
        return norm_status(gem) == norm_status(research)
    if field in CAPACITY_FIELDS | INT_FIELDS | COORD_FIELDS:
        a, b = to_float(gem), to_float(research)
        if a is not None and b is not None:
            if field in CAPACITY_FIELDS:
                return abs(a - b) <= max(0.5, 0.01 * abs(a))
            if field in INT_FIELDS:
                return int(a) == int(b)
            return abs(a - b) <= COORD_TOL
    if field in ENTITY_FIELDS:
        return norm_entities(gem) == norm_entities(research)
    if field == "Fuel":
        return norm_fuel(gem) == norm_fuel(research)
    if field == "Turbine/Engine Technology":
        return norm_tech(gem) == norm_tech(research)
    return ws(gem).lower() == ws(research).lower()


def verdict_for(field: str, gem, research) -> str:
    rb, gb = is_blank(research), is_blank(gem)
    if rb and gb:
        return "both_blank"
    if rb:
        return "research_blank"
    if gb:
        return "fill"
    return "match" if values_equal(field, gem, research) else "change"


def host_of(url: str) -> str:
    """Publisher host, www. dropped, Wayback captures unwrapped."""
    p = urlparse(str(url).strip())
    h = (p.hostname or "").lower()
    if h == "web.archive.org":
        m = re.match(r"/web/[^/]+/(.+)", p.path)
        if m:
            inner = m.group(1)
            return host_of(inner if "://" in inner else "http://" + inner)
    return h[4:] if h.startswith("www.") else h


def verified_urls(urls, verifications) -> list[str]:
    ok = {v.get("url") for v in (verifications or []) if v.get("ok")}
    return [u for u in urls if u in ok]


def field_slug(field: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(field).lower()).strip("-")


def load_index(batch: Path) -> dict:
    p = batch / "briefs" / "_index.json"
    if not p.exists():
        sys.exit(f"ERROR: {p} not found. Run build_state_brief.py first.")
    return json.loads(p.read_text(encoding="utf-8"))


def resolve_csv(arg, index: dict) -> Path:
    if arg:
        return Path(arg)
    if index.get("csv") and Path(index["csv"]).exists():
        return Path(index["csv"])
    return gogpt_scoped_csv()


def load_export(csv_path: Path, unit_ids=None):
    """-> (header, {unit_id: {header: cell}}). Header re-derived every run."""
    if not Path(csv_path).exists():
        sys.exit(f"ERROR: export CSV not found: {csv_path}")
    rows = {}
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        i_uid = header.index("GEM unit ID")
        for row in reader:
            if len(row) <= i_uid:
                continue
            if unit_ids is None or row[i_uid] in unit_ids:
                rows[row[i_uid]] = dict(zip(header, row))
    return header, rows


def load_shard(batch: Path, pid: str):
    """-> (shard dict or None, problem string or '')."""
    p = batch / "shards" / f"{pid}.json"
    if not p.exists():
        return None, "no shard file"
    try:
        return json.loads(p.read_text(encoding="utf-8")), ""
    except (json.JSONDecodeError, OSError) as e:
        return None, f"shard does not parse ({e})"


# ------------------------------------------------------------ plain words ---

def unit_label(unit_name: str, uid: str) -> str:
    return f"unit {unit_name} ({uid})" if unit_name else f"unit {uid}"


def link_phrase(n: int) -> str:
    return "the link below" if n == 1 else f"the {n} links below"


def build_action(kind, field, value, current, target, ref_col, n_urls,
                 each_unit=False):
    if kind == "reverified":
        s = f"Leave {field} of {target} as {value}. It is still correct."
    elif kind == "fill":
        s = f"Set {field} of {target} to {value}. The box is empty now."
    else:
        s = f"Set {field} of {target} to {value}. It now says {current}."
    if n_urls:
        s += (f" Add {link_phrase(n_urls)} to the {ref_col} box"
              f"{' on each unit' if each_unit else ''}. "
              "Keep the links already there.")
    else:
        s += (" There is no link to add. The note explains how this status "
              "was worked out.")
    return s


def join_notes(*parts) -> str:
    return " ".join(ws(p) for p in parts if ws(p))


# --------------------------------------------------------------- assemble ---

class Assembler:
    def __init__(self, batch: Path, csv_path: Path, quarter: str):
        self.batch = batch
        self.index = load_index(batch)
        self.mode = self.index.get("mode", "update")
        self.state = self.index.get("state", "")
        self.postal = self.index.get("postal", "")
        self.quarter = quarter
        self.csv_path = csv_path
        self.warnings: list[str] = []
        self.lanes = {lane: [] for lane in LANE_FILES}
        self.verdicts = Counter()
        self.match_no_new_url = 0
        self.downgraded = 0
        self.comparison: dict = {}
        self.unit_notes_used: set[str] = set()
        self.shards: dict = {}
        self.hidden: dict = {}

    # -- loading
    def load(self):
        unit_ids = {u for p in self.index["plants"] for u in p["unit_ids"]}
        for p in self.index["plants"]:
            shard, problem = load_shard(self.batch, p["plant_id"])
            if shard is None:
                self.warnings.append(f"{p['plant_id']}: {problem}; skipped")
                continue
            if not (shard.get("meta") or {}).get("done"):
                self.warnings.append(f"{p['plant_id']}: shard not marked done; "
                                     "assembled anyway")
            self.shards[p["plant_id"]] = shard
            unit_ids |= {u.get("gem_unit_id") for u in shard.get("units") or []}
        self.header, self.export = load_export(self.csv_path, unit_ids)
        if self.mode == "blind":
            for pid in self.shards:
                hp = self.batch / "briefs" / "_hidden" / f"{pid}.json"
                if not hp.exists():
                    self.warnings.append(f"{pid}: blind mode but no _hidden "
                                         "file; comparing against the export")
                    continue
                self.hidden[pid] = json.loads(hp.read_text(encoding="utf-8"))
                self._check_hidden(pid)

    def _check_hidden(self, pid):
        """The withheld values should equal the export; warn where not."""
        for uid, vals in (self.hidden[pid].get("units") or {}).items():
            row = self.export.get(uid)
            if row is None:
                self.warnings.append(f"{pid}/{uid}: in _hidden but not in export")
                continue
            for h, v in vals.items():
                if h in row and ws(row[h]) != ws(v):
                    self.warnings.append(
                        f"{pid}/{uid}: export {h!r} is {row[h]!r} but the "
                        f"brief withheld {v!r}; export changed since briefs")

    def gem_value(self, pid, uid, field):
        """GEM value for the comparison: _hidden in blind mode, else export."""
        h = ((self.hidden.get(pid) or {}).get("units") or {}).get(uid)
        if h is not None and field in h:
            return h[field]
        return (self.export.get(uid) or {}).get(field, "")

    # -- comparison bookkeeping
    def compare(self, pid, plant_name, uid, field, research, verdict_gem,
                fd, scope):
        unit = (self.comparison.setdefault(pid, {"plant_name": plant_name,
                                                 "units": {}})["units"]
                .setdefault(uid, {"unit_name": (self.export.get(uid) or {})
                                  .get("Unit name", ""), "fields": {}}))
        gem = self.gem_value(pid, uid, field)
        verdict = verdict_gem if verdict_gem == "not_reported" else \
            verdict_for(field, gem, research)
        unit["fields"][field] = {
            "gem": gem, "research": research, "verdict": verdict,
            "tier": (fd or {}).get("tier", ""), "refs": list((fd or {}).get("refs") or []),
            "scope": scope, "note": (fd or {}).get("note", "")}
        self.verdicts[verdict] += 1

    # -- one finding against one unit
    def evaluate(self, field, fd, row):
        value = ws(fd.get("value"))
        if field == "Status" and value:
            value = norm_status(value)
        gem = row.get(field, "")
        refs = [u for u in (fd.get("refs") or []) if ws(u)]
        ds_col = ref_col_for(field)
        existing = set(_split_urls(row.get(ds_col, "")))
        return {"value": value, "gem": gem,
                "verdict": verdict_for(field, gem, value), "refs": refs,
                "ds_col": ds_col,
                "new_urls": [u for u in refs if u not in existing]}

    def tier_for(self, field, verdict, fd, refs):
        tier = str(fd.get("tier") or "medium").lower()
        note = ""
        if field == "Status" and verdict == "change" and tier == "high":
            hosts = {host_of(u) for u in verified_urls(refs, fd.get("verifications"))}
            if len(hosts - {""}) < 2:
                tier, note = "medium", DOWNGRADE_NOTE
                self.downgraded += 1
        return tier, note

    def base_record(self, pid, plant_name, uid):
        row = self.export.get(uid) or {}
        return {"gem_unit_id": uid, "gem_plant_id": pid,
                "plant_name": plant_name or row.get("Plant name", ""),
                "unit_name": row.get("Unit name", ""),
                "country": row.get("Country/Area", COUNTRY)}

    def unit_notes_once(self, uid, notes):
        if uid in self.unit_notes_used or is_blank(notes):
            return ""
        self.unit_notes_used.add(uid)
        return notes

    def stage(self, pid, plant_name, field, fd, anchor_uid, ev, unit_notes,
              siblings=None):
        """Turn one evaluated finding into an updates or qa record (or none)."""
        verdict = ev["verdict"]
        plant_level = siblings is not None
        rid = f"{pid}:{'plant' if plant_level else anchor_uid}:{field_slug(field)}"
        row = self.export.get(anchor_uid) or {}
        current = row.get(field, "")
        if plant_level:
            n = len(siblings) + 1
            target = (f"all {n} units of {plant_name}" if n > 1
                      else unit_label(row.get("Unit name", ""), anchor_uid))
        else:
            target = unit_label(row.get("Unit name", ""), anchor_uid)

        if verdict == "match":
            if not ev["new_urls"]:
                self.match_no_new_url += 1
                return
            rec = self.base_record(pid, plant_name, anchor_uid)
            rec.update({
                "record_id": rid, "cluster": anchor_uid, "verdict": "match",
                "reverified": True,
                "fields": {field: current}, "current": {field: current},
                "refs": {ev["ds_col"]: ev["new_urls"]},
                "verifications": fd.get("verifications") or [],
                "tier": str(fd.get("tier") or "medium").lower(),
                "independent": bool(fd.get("independent")),
                "source_language": "en",
                "researcher_notes": join_notes(fd.get("note"), unit_notes),
                "action": build_action("reverified", field, current, current,
                                       target, ev["ds_col"],
                                       len(ev["new_urls"]), plant_level and n > 1)})
        elif verdict in ("fill", "change"):
            value, refs = ev["value"], ev["refs"]
            if not refs and "inferred" not in value.lower():
                rec = self.base_record(pid, plant_name, anchor_uid)
                rec.update({
                    "record_id": rid, "concern_type": "other",
                    "recommendation": ("Find a source that states this value "
                                       "before changing the record."),
                    "fields": {}, "refs": {}, "proposed_value": {field: value},
                    "current": {field: current},
                    "researcher_notes": join_notes(
                        f"The research suggests {field} should be {value}, "
                        "but it gave no source for that, so no edit is "
                        "proposed.", fd.get("note"))})
                self.lanes["qa"].append(rec)
                return
            tier, extra = self.tier_for(field, verdict, fd, refs)
            rec = self.base_record(pid, plant_name, anchor_uid)
            rec.update({
                "record_id": rid, "cluster": anchor_uid, "verdict": verdict,
                "fields": {field: value}, "current": {field: current},
                "refs": {ev["ds_col"]: refs} if refs else {},
                "verifications": fd.get("verifications") or [],
                "tier": tier, "independent": bool(fd.get("independent")),
                "source_language": "en",
                "researcher_notes": join_notes(fd.get("note"), extra, unit_notes),
                "action": build_action(verdict, field, value, current, target,
                                       ev["ds_col"], len(refs),
                                       plant_level and n > 1)})
        else:
            return
        if plant_level:
            rec["applies_to_all_units"] = True
            rec["sibling_unit_ids"] = list(siblings)
            rec["sibling_current"] = {u: (self.export.get(u) or {}).get(field, "")
                                      for u in siblings}
        self.lanes["updates"].append(rec)

    # -- per plant
    def plant(self, p):
        pid, plant_name = p["plant_id"], p.get("plant_name", "")
        shard = self.shards.get(pid)
        if shard is None:
            return
        shard_units = {u.get("gem_unit_id"): u for u in shard.get("units") or []}
        order = list(p["unit_ids"]) + [u for u in shard_units
                                       if u not in p["unit_ids"]]
        order = [u for u in order if u]
        missing = [u for u in order if u not in self.export]
        for u in missing:
            self.warnings.append(f"{pid}/{u}: unit not in the export; skipped")
        order = [u for u in order if u in self.export]
        plant_findings = shard.get("plant_findings") or {}

        for uid in order:
            su = shard_units.get(uid)
            if su is None:
                self.warnings.append(f"{pid}/{uid}: unit not reported in shard")
                continue
            row = self.export[uid]
            findings = su.get("findings") or {}
            reported = set()
            for field, fd in findings.items():
                fd = fd or {}
                ev = self.evaluate(field, fd, row)
                if is_blank(ev["value"]):
                    continue        # an empty finding is treated as not found
                reported.add(field)
                self.compare(pid, plant_name, uid, field, ev["value"], None,
                             fd, "unit")
                notes = ""
                if ev["verdict"] != "match" or ev["new_urls"]:
                    notes = self.unit_notes_once(uid, su.get("notes"))
                self.stage(pid, plant_name, field, fd, uid, ev, notes)
            for field in su.get("not_found") or []:
                if field in reported:
                    continue
                reported.add(field)
                self.compare(pid, plant_name, uid, field, "", None, None, "unit")
            if self.mode == "blind":
                for field in RESEARCH_FIELDS:
                    if field in reported or field in plant_findings:
                        continue
                    if not is_blank(self.gem_value(pid, uid, field)):
                        self.compare(pid, plant_name, uid, field, "",
                                     "not_reported", None, "unit")

        for field, fd in plant_findings.items():
            fd = fd or {}
            evs = {uid: self.evaluate(field, fd, self.export[uid]) for uid in order}
            if not evs:
                continue
            value = next(iter(evs.values()))["value"]
            for uid in order:
                self.compare(pid, plant_name, uid, field, value, None, fd, "plant")
            if is_blank(value):
                continue
            non_match = [u for u in order if evs[u]["verdict"] in ("fill", "change")]
            anchor = non_match[0] if non_match else order[0]
            ev = dict(evs[anchor])
            if non_match:
                ev["verdict"] = ("change" if any(evs[u]["verdict"] == "change"
                                                 for u in non_match) else "fill")
            else:
                new = []
                for u in order:
                    new += [x for x in evs[u]["new_urls"] if x not in new]
                ev["new_urls"] = new
            siblings = [u for u in order if u != anchor]
            self.stage(pid, plant_name, field, fd, anchor, ev, "", siblings)

        for section, lane in (("qa", "qa"), ("monitor", "monitor"),
                              ("newunits", "newunits"), ("entities", "entity")):
            for i, item in enumerate(shard.get(section) or []):
                # A new-unit lead without proposed values and verified refs
                # is a candidate, not an edit: it goes to monitor.
                if lane == "newunits" and not (
                        isinstance(item.get("fields"), dict) and item["fields"]
                        and isinstance(item.get("refs"), dict)
                        and item.get("verifications")):
                    item = dict(item)
                    item["note"] = ("New unit lead, not yet confirmed: "
                                    + (item.get("note") or "")).strip()
                    lane = "monitor"
                self.lanes[lane].append(self.passthrough(pid, plant_name, lane,
                                                         item, i))

    def statewide(self):
        """shards/_state.json: qa and monitor items from the state-level search
        for newly announced plants and gas-fired data centers. Items may name
        an existing plant with gem_plant_id; otherwise gem_plant_id is blank and
        the record_id starts with us-<postal>:plant."""
        sp = self.batch / "shards" / "_state.json"
        if not sp.exists():
            return
        try:
            st = json.loads(sp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            self.warnings.append(f"_state.json does not parse: {e}; skipped")
            return
        tag = f"us-{self.postal}" if self.postal else "statewide"
        for section, lane in (("qa", "qa"), ("monitor", "monitor")):
            for i, item in enumerate(st.get(section) or []):
                rec = self.passthrough(tag, item.get("plant_name") or f"{self.state} statewide",
                                       lane, dict(item), i)
                rec["gem_plant_id"] = item.get("gem_plant_id") or ""
                self.lanes[lane].append(rec)

    def passthrough(self, pid, plant_name, lane, item, i):
        rec = dict(item)
        uid = rec.get("gem_unit_id", "") or ""
        row = self.export.get(uid) or {}
        rec.setdefault("gem_plant_id", pid)
        rec.setdefault("plant_name", plant_name)
        rec.setdefault("country", COUNTRY)
        if uid and row:
            rec.setdefault("unit_name", row.get("Unit name", ""))
        if lane in ("qa", "monitor"):
            if isinstance(rec.get("refs"), list):
                rec["refs"] = {"links": rec["refs"]} if rec["refs"] else {}
            rec.setdefault("fields", {})
            rec.setdefault("researcher_notes", rec.pop("note", ""))
        if lane == "qa":
            slug = f"qa-{field_slug(rec.get('concern_type', 'other'))}-{i + 1}"
            rec["record_id"] = f"{pid}:{uid or 'plant'}:{slug}"
        elif lane == "monitor":
            rec["record_id"] = f"{pid}:{uid or 'plant'}:monitor-{i + 1}"
        elif lane == "newunits":
            rec["record_id"] = (f"{pid}:new:"
                                f"{field_slug(rec.get('unit_name', '')) or i + 1}")
        else:
            rec.setdefault("entity_country", COUNTRY)
            rec["record_id"] = (f"{pid}:entity:"
                                f"{field_slug(rec.get('entity_name', '')) or i + 1}")
        return rec

    def run(self):
        self.load()
        for p in self.index["plants"]:
            self.plant(p)
        self.statewide()
        for lane, recs in self.lanes.items():   # record_id unique per lane
            seen = Counter()
            for r in recs:
                seen[r["record_id"]] += 1
                if seen[r["record_id"]] > 1:
                    r["record_id"] += f"-{seen[r['record_id']]}"

    # -- writing
    def scope(self):
        return {"country": COUNTRY, "state": self.state, "postal": self.postal,
                "quarter": self.quarter, "csv": str(self.csv_path)}

    def write_staging(self, generated):
        staging = self.batch / "staging"
        staging.mkdir(parents=True, exist_ok=True)
        for lane in LANE_FILES:
            recs = self.lanes[lane]
            counts = {"records": len(recs)}
            if lane == "updates":
                counts.update({
                    "fill": sum(r.get("verdict") == "fill" for r in recs),
                    "change": sum(r.get("verdict") == "change" for r in recs),
                    "reverified": sum(bool(r.get("reverified")) for r in recs),
                    "match_no_new_url": self.match_no_new_url,
                    "status_downgraded": self.downgraded})
            env = {"meta": {"lane": lane, "scope": self.scope(),
                            "generated": generated, "mode": self.mode,
                            "counts": counts},
                   "records": recs}
            (staging / f"staged_{lane}.json").write_text(
                json.dumps(env, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8")

    def write_comparison(self, generated):
        out = {"meta": {"scope": self.scope(), "generated": generated,
                        "mode": self.mode,
                        "counts": {v: self.verdicts.get(v, 0) for v in VERDICTS}},
               "plants": self.comparison}
        (self.batch / "staging" / "comparison.json").write_text(
            json.dumps(out, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")

    def write_memo(self, path: Path, stamp: str):
        def cell(v):
            s = ws(v)
            return s.replace("|", "\\|") if s else "(blank)"

        L = [f"# Calibration memo: {self.state}, blind run", "",
             f"Stamp {stamp}. Built by assemble_state.py from "
             f"{len(self.shards)} plant reports out of "
             f"{len(self.index['plants'])} plants in the brief index.", "",
             "This memo compares what the research found for each plant with "
             "what the GEM database already says. The research was done "
             "blind. The researcher saw only each plant's name, location and "
             "IDs, not the GEM values. Each table row is one field of one "
             "unit.", "",
             "Rows where the two sides agree are already marked match. Every "
             "other row has a question mark in the Verdict column. Score it by "
             "reading the source, then write one of these: match, GEM wrong, "
             "research wrong, both defensible, unresolvable. A row scored GEM "
             "wrong is a real error in the database. It should go into the "
             "update deliverable from this same run. Fields that are blank on "
             "both sides are counted in the totals but not listed.", "",
             "## Totals", "", "| Verdict | What it means | Count |",
             "|---|---|---|"]
        for v in VERDICTS:
            L.append(f"| {v} | {VERDICT_MEANING[v]} | {self.verdicts.get(v, 0)} |")
        L.append(f"| total | | {sum(self.verdicts.values())} |")

        resolved = defaultdict(Counter)
        for pid, plant in self.comparison.items():
            L += ["", f"## {plant['plant_name']} ({pid})", "",
                  "| Unit | Field | GEM value | Research value | "
                  "Source that resolved it | Verdict |",
                  "|---|---|---|---|---|---|"]
            for uid, unit in plant["units"].items():
                label = f"{unit['unit_name']} ({uid})"
                for field, c in unit["fields"].items():
                    if c["verdict"] == "both_blank":
                        continue
                    src = host_of(c["refs"][0]) if c["refs"] else ""
                    if src and c["verdict"] not in ("research_blank",
                                                    "not_reported"):
                        resolved[field][src] += 1
                    mark = "match" if c["verdict"] == "match" else "?"
                    L.append(f"| {cell(label)} | {cell(field)} | "
                             f"{cell(c['gem'])} | {cell(c['research'])} | "
                             f"{src or '(none)'} | {mark} |")

        L += ["", "## What resolved what", "",
              "How many unit fields each website settled, by field. A "
              "plant-wide finding counts once for each unit.", ""]
        if resolved:
            L += ["| Field | Website | Unit fields |", "|---|---|---|"]
            for field in sorted(resolved):
                for h, n in resolved[field].most_common():
                    L.append(f"| {field} | {h} | {n} |")
        else:
            L.append("No finding carried a link.")

        L += ["", "## Run facts per plant", "",
              "The plant reports record only when they finished, not when "
              "they started, so time per plant is not shown.", "",
              "| Plant | Model | Finished | Links tried | Links that checked out |",
              "|---|---|---|---|---|"]
        for pid, shard in self.shards.items():
            m = shard.get("meta") or {}
            L.append(f"| {cell(m.get('plant_name') or pid)} | {cell(m.get('model'))} | "
                     f"{cell(m.get('generated'))} | {cell(m.get('urls_attempted'))} | "
                     f"{cell(m.get('urls_verified'))} |")

        L += ["", "## Not found", ""]
        any_nf = False
        for pid, shard in self.shards.items():
            for su in shard.get("units") or []:
                nf = su.get("not_found") or []
                if not nf:
                    continue
                any_nf = True
                uid = su.get("gem_unit_id", "")
                name = (self.export.get(uid) or {}).get("Unit name", "") \
                    or su.get("unit_name", "")
                L.append(f"- **{shard.get('meta', {}).get('plant_name', pid)}, "
                         f"unit {name} ({uid})**: {', '.join(nf)}.")
                if not is_blank(su.get("notes")):
                    L.append(f"  {ws(su['notes'])}")
        if not any_nf:
            L.append("Every unit reported a value for every field it covered.")

        L += ["", "## GEM errors to carry into the update deliverable", "",
              "Fill this in after scoring. List each row scored GEM wrong, "
              "with the unit ID, the field and the source.", ""]
        path.write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batch", required=True, help="batches/us-<st> directory")
    ap.add_argument("--csv", default=None,
                    help="fresh scoped export (default: _index.json csv, "
                         "else scripts/gem_export_gogpt_scoped.csv)")
    ap.add_argument("--stamp", default=None,
                    help="memo stamp YYYYMMDD_HHMM_ET (default: now, New York)")
    ap.add_argument("--quarter", default="q4-2026")
    args = ap.parse_args()

    batch = Path(args.batch).resolve()
    if not batch.is_dir():
        sys.exit(f"ERROR: batch dir not found: {batch}")
    index = load_index(batch)
    csv_path = resolve_csv(args.csv, index)
    a = Assembler(batch, csv_path, args.quarter)

    stamp = args.stamp or now_et().strftime("%Y%m%d_%H%M_ET")
    if not stamp.endswith("_ET"):
        stamp += "_ET"
    memo = batch / f"calibration_{stamp}.md"
    if a.mode == "blind" and memo.exists():
        sys.exit(f"ERROR: {memo.name} already exists. The memo is never "
                 "overwritten; rerun in a minute or pass a new --stamp.")

    a.run()
    generated = now_et().isoformat(timespec="seconds")
    a.write_staging(generated)
    if a.mode == "blind":
        a.write_comparison(generated)
        a.write_memo(memo, stamp)

    for w in a.warnings:
        print(f"  WARNING: {w}")
    print(f"assembled {len(a.shards)} of {len(a.index['plants'])} plants "
          f"({a.mode} mode, {a.state})")
    print("  verdicts (unit x field): " + ", ".join(
        f"{v}={a.verdicts.get(v, 0)}" for v in VERDICTS))
    print(f"  match with no new link (no record): {a.match_no_new_url}")
    print(f"  status changes lowered from high to medium: {a.downgraded}")
    print("  records: " + ", ".join(f"{lane}={len(r)}"
                                    for lane, r in a.lanes.items()))
    print(f"  wrote {batch / 'staging'}/staged_<lane>.json")
    if a.mode == "blind":
        print(f"  wrote {batch / 'staging' / 'comparison.json'}")
        print(f"  wrote {memo}")
    print(f"next: python state_gate.py --batch {args.batch}")


if __name__ == "__main__":
    main()
