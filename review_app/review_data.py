"""
Build the review app's dataset from one or more staging dirs.

    python review_app/review_data.py --scope us-md --scope us-ny [--out work/review_data.json]
    python review_app/review_data.py --dirs batches/us-md/staging ... [--export-csv PATH]

Reads ONLY staged_{updates,qa,monitor,entity,newunits,newplants}.json in each staging dir
(never the shards, briefs, comparison.json or the blind copies). Writes one JSON file:

    {"built", "scope": {"country", "states", "quarter"}, "dirs": [label, ...], "columns": [...],
     "plants": [{"pid", "name", "country", "state", "dir", "units": [{"gem_unit_id", "unit_name", "irp_box"}],
                 "lines": [...], "items": [...]}]}

One card per GEM plant ID (a statewide pseudo-card for records whose plant ID is the state
slug). A LINE is a staged edit the reviewer accepts, holds, rejects or suggests on: one
per updates/newunits/newplants record. An ITEM is a note that never writes a cell: a qa
concern, a monitor note, an entity lookup. Keys are `<dir label>::<record_id>`, the dir label
is repo-relative (`batches/us-md/staging`), and record_id is the stable id written by
scripts/assemble_state.py, so decisions survive a rebuild.

Every line and item carries `group` (a QC/Country checklist group id, review_app/checklist.py
GROUPS, or "other"), `group_label` and `checks` (the checklist rows it ticks), and the dataset
carries `groups` (the groups for this scope with counts and rows) and `us`. Watch items
(monitor lane) carry `monitor_kind`: `existing_plant` items sit on their plant's card,
`new_to_tracker` items get a candidate card keyed by the plant name with any parenthetical
stripped, so the same candidate staged in two folders shares one card (the later item is
marked `duplicate_of` the first).

Line kinds: fill (blank cell gets a value), change (a value is replaced), reverified (the
current value was checked and stands; only the Data Source link is new), delete (a value is
cleared), plant (a plant-level change applied to every unit row), new_row (a new unit or
plant). Severity: `minor` for reverified lines, `major` for everything else (a cell value
changes). `default` is "accept" for high-confidence lines (one fully validated source, or two
independent ones on a status change) and "hold" otherwise; the page shows it but nothing is
decided until a person clicks.

The current Data Source cell of each line comes from the scoped export (the batch's csv from
meta.scope.csv, else --export-csv, else scripts/gem_export_gogpt_scoped.csv); when the csv is
missing the lines carry current_ref = null and the page says so.
"""
import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT / "scripts", HERE, ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import paths  # noqa: E402
from build_review_package import URL_RE, ref_col_for  # noqa: E402
from review_app.checklist import MONITOR_KINDS, summarize, tag  # noqa: E402

ET = ZoneInfo("America/New_York")
LINE_LANES = ("updates", "newunits", "newplants")
ITEM_LANES = {"qa": "concern", "monitor": "monitor", "entity": "entity"}
# scope-wide items carry the batch tag as their plant id: us-md for a state,
# a country slug such as germany or czech-republic for a country batch
_STATE_PID = re.compile(r"^(us-[a-z]{2}|[a-z][a-z-]*)$")


def closeout_links(pointers=None):
    """The GEM sheets and docs the close-out panel points at, read from the link hub
    docs/reference/sop_pointers.md so the URLs live in one place. Each entry is
    {label, url}; a document the hub does not list is left out (the panel then names
    it without a link). Tab rows ("↳ name | ... | `gid=N`") become tab links on the
    Update sheet."""
    path = Path(pointers) if pointers else ROOT / "docs" / "reference" / "sop_pointers.md"
    if not path.exists():
        return {}
    url_re = re.compile(r"https?://[^\s|`)]+")
    gid_re = re.compile(r"`gid=(\d+)`")
    sheet, tabs, docs = "", {}, {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        name = cells[0]
        if "Update V2" in name and not sheet:
            m = url_re.search(cells[2])
            sheet = m.group(0) if m else ""
        elif name.startswith("↳"):
            m = gid_re.search(cells[2])
            if m:
                tabs[name.lstrip("↳ ").strip()] = m.group(1)
        else:
            m = url_re.search(cells[2])
            if m:
                docs[name] = m.group(0)

    def tab(key, label, *needles):
        for t, gid in tabs.items():
            if all(n.lower() in t.lower() for n in needles) and sheet:
                out[key] = {"label": label, "url": f"{sheet}/edit?gid={gid}#gid={gid}"}
                return

    def doc(key, label, *needles):
        for t, url in docs.items():
            if all(n.lower() in t.lower() for n in needles):
                out[key] = {"label": label, "url": url}
                return

    out = {}
    if sheet:
        out["update_sheet"] = {"label": "Q4 2026 GOGPT Update V2 sheet", "url": sheet}
    tab("assignments", "Researcher Country Assignments tab", "Researcher Country Assignments")
    tab("checklist", "QC/Country checklist tab", "QC/Country checklist")
    tab("us_research", "United States research tab", "United States research")
    tab("us_irps", "US IRPs tab", "US IRPs")
    tab("country_tips", "Country tips trends tab", "Country tips")
    doc("possible_updates", "GEM trackers possible updates sheet", "possible updates")
    doc("data_sources", "Gas and oil power plant data sources by country doc", "data sources", "by country")
    doc("europe_doc", "Europe Workflow Map doc", "Europe Workflow")
    doc("us_guide", "GOGPT United States Data/Research Guide", "Data/Research Guide")
    return out


def rel(path):
    """Repo-relative label for a staging dir (absolute when outside the repo)."""
    path = Path(path).resolve()
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def split_urls(cell):
    return [u.strip() for u in re.split(r",\s*(?=https?://)|\s*\n\s*", str(cell or "")) if u.strip()]


def host_of(url):
    try:
        h = urlsplit(url).netloc.lower()
    except ValueError:
        return ""
    return h[4:] if h.startswith("www.") else h


def load_lane(d, lane):
    p = Path(d) / f"staged_{lane}.json"
    if not p.exists():
        return {}, []
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {}, data
    return data.get("meta", {}), data.get("records", [])


def load_export(csv_path, unit_ids):
    """(header, {unit id: row dict}) for the unit ids named; ([], {}) when the csv is missing."""
    if not csv_path or not Path(csv_path).exists():
        return [], {}
    rows = {}
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        i_uid = header.index("GEM unit ID")
        for row in reader:
            if len(row) > i_uid and row[i_uid] in unit_ids:
                rows[row[i_uid]] = dict(zip(header, row))
    return header, rows


def line_kind(r):
    if r.get("delete"):
        return "delete"
    if r.get("applies_to_all_units"):
        return "plant"
    if r.get("reverified") or r.get("verdict") == "match":
        return "reverified"
    return "change" if r.get("verdict") == "change" else "fill"


def tier_of(r):
    t = str(r.get("tier") or "").lower()
    return t if t in ("high", "medium", "low") else ""


def verification_map(r):
    out = {}
    for v in r.get("verifications") or []:
        if v.get("url"):
            out[v["url"]] = {"ok": bool(v.get("ok")), "contains_value": bool(v.get("contains_value")),
                             "name_found": bool(v.get("name_found")), "note": v.get("note") or ""}
    return out


def candidate_key(name):
    """Slug for a plant GEM does not track yet, from its name with any parenthetical dropped:
    "Gowanus and Narrows repowering (AlphaGen)" and "... (Alpha Generation)" are one candidate."""
    base = re.sub(r"\s*\([^)]*\)", "", str(name or "")).lower()
    return re.sub(r"[^a-z0-9]+", "-", base).strip("-")


def tagged(obj, r, lane, unit_row=None, us=True):
    """Set group / group_label / checks on a line or item from the staged record."""
    t = tag(r, lane, unit_row=unit_row, us=us)
    obj["group"] = t["group"]
    obj["group_label"] = t["group_label"]
    obj["checks"] = t["checks"]
    return obj


def update_line(r, label, export_rows, us=True):
    kind = line_kind(r)
    fields = dict(r.get("fields") or {})
    cols = list(fields)
    column = cols[0] if cols else ""
    ref_col = ref_col_for(column) if column else ""
    refs = r.get("refs") or {}
    proposed_refs = []
    for rc, urls in refs.items():
        for u in (urls if isinstance(urls, list) else split_urls(urls)):
            if u not in proposed_refs:
                proposed_refs.append(u)
    uid = r.get("gem_unit_id") or ""
    row = export_rows.get(uid) or {}
    if ref_col and ref_col == column:
        # Status Detail carries its links in its own text
        current_ref = URL_RE.findall(row.get(column) or "") if row else None
    else:
        current_ref = split_urls(row.get(ref_col)) if row and ref_col in row else None
    current = dict(r.get("current") or {})
    for c in cols:
        if c not in current and row:
            current[c] = row.get(c, "")
    reverified = bool(r.get("reverified") or r.get("verdict") == "match")
    line = {
        "key": f"{label}::{r['record_id']}", "dir": label, "record_id": r["record_id"],
        "kind": kind, "reverified": reverified, "severity": "minor" if reverified else "major",
        "column": column, "columns": cols, "ref_col": ref_col,
        "gem_unit_id": uid, "unit_name": r.get("unit_name") or "",
        "current": current, "current_ref": current_ref,
        "proposed_values": fields, "proposed_refs": proposed_refs,
        "verifications": verification_map(r),
        "tier": tier_of(r), "independent": bool(r.get("independent")),
        "source_language": r.get("source_language") or "",
        "notes": r.get("researcher_notes") or "", "action": r.get("action") or "",
        "sibling_unit_ids": list(r.get("sibling_unit_ids") or []),
        "sibling_current": r.get("sibling_current") or {},
        "publishers": len({host_of(u) for u in proposed_refs if host_of(u)}),
        "default": "accept" if tier_of(r) == "high" else "hold",
        "decision": None, "reviewed": False,
        "irp": bool(r.get("irp")),
    }
    # a plant-level record may have no unit row of its own: any sibling's row tells the status
    unit_row = row or next((export_rows[s] for s in r.get("sibling_unit_ids") or [] if s in export_rows), {})
    return tagged(line, r, "updates", unit_row, us)


def _refs_by_col(refs):
    return {k: (v if isinstance(v, list) else split_urls(v)) for k, v in (refs or {}).items()}


def new_row_line(r, label, lane, us=True):
    """One line per new-row record. A newplants record carries its unit rows nested under
    `units` (plant-level fields on the record, per-unit fields on each unit); the whole plant is
    one decision, keyed on the record's id, so the units ride along on the line as `units` and
    their links count toward the line's publishers and verification marks."""
    fields = dict(r.get("fields") or {})
    refs = r.get("refs") or {}
    proposed_refs = []
    verifications = verification_map(r)
    units = []
    for u in r.get("units") or []:
        units.append({"unit_name": u.get("unit_name") or "", "fields": dict(u.get("fields") or {}),
                      "refs_by_col": _refs_by_col(u.get("refs")),
                      "notes": u.get("researcher_notes") or "", "action": u.get("action") or ""})
        verifications.update(verification_map(u))
    for rc, urls in list(refs.items()) + [kv for u in units for kv in u["refs_by_col"].items()]:
        for u in (urls if isinstance(urls, list) else split_urls(urls)):
            if u not in proposed_refs:
                proposed_refs.append(u)
    return tagged({
        "key": f"{label}::{r['record_id']}", "dir": label, "record_id": r["record_id"],
        "kind": "new_row", "reverified": False, "severity": "major", "lane": lane,
        "column": "", "columns": list(fields), "ref_col": "",
        "gem_unit_id": r.get("gem_unit_id") or "", "unit_name": r.get("unit_name") or "",
        "plant_name": r.get("plant_name") or "",
        "current": {}, "current_ref": None,
        "proposed_values": fields, "proposed_refs": proposed_refs,
        "refs_by_col": _refs_by_col(refs), "units": units,
        "verifications": verifications,
        "tier": tier_of(r), "independent": bool(r.get("independent")),
        "source_language": r.get("source_language") or "",
        "notes": r.get("researcher_notes") or "", "action": r.get("action") or "",
        "sibling_unit_ids": [], "sibling_current": {},
        "publishers": len({host_of(u) for u in proposed_refs if host_of(u)}),
        "default": "hold", "decision": None, "reviewed": False,
        "irp": bool(r.get("irp")),
    }, r, lane, None, us)


def monitor_kind(r):
    """new_to_tracker | existing_plant, from the record's own field or its GEM plant id."""
    k = r.get("monitor_kind")
    if k in MONITOR_KINDS:
        return k
    return "existing_plant" if str(r.get("gem_plant_id") or "").strip() else "new_to_tracker"


def item(r, label, kind, unit_row=None, us=True):
    refs = r.get("refs") or {}
    links = []
    for v in refs.values():
        for u in (v if isinstance(v, list) else split_urls(v)):
            if u not in links:
                links.append(u)
    it = {
        "key": f"{label}::{r['record_id']}", "dir": label, "record_id": r["record_id"], "kind": kind,
        "gem_unit_id": r.get("gem_unit_id") or "", "unit_name": r.get("unit_name") or "",
        "links": links, "verifications": verification_map(r),
        "notes": r.get("researcher_notes") or "",
        "call": None, "call_note": None, "reviewed": False,
        "irp": bool(r.get("irp")),
    }
    if kind == "concern":
        it["concern_type"] = r.get("concern_type") or ""
        it["concern_type_raw"] = r.get("concern_type_raw") or ""
        it["recommendation"] = r.get("recommendation") or ""
    elif kind == "monitor":
        # older records kept the one-line reason under `item`; the page reads `reason`
        it["monitor_kind"] = monitor_kind(r)
        it["plant_name"] = r.get("plant_name") or ""
        it["reason"] = r.get("monitor_reason") or r.get("item") or ""
        it["recheck_by"] = r.get("recheck_by") or ""
        fields = r.get("fields") or {}
        it["capacity_mw"] = str(fields.get("Capacity (MW)") or r.get("capacity_mw") or "")
        it["status"] = str(fields.get("Status") or r.get("status") or "")
        it["tier"] = tier_of(r)
    elif kind == "entity":
        it["entity_name"] = r.get("entity_name") or ""
        it["role"] = r.get("role") or ""
        it["lookup_result"] = r.get("lookup_result") or ""
        it["entity_country"] = r.get("entity_country") or ""
    return tagged(it, r, {"concern": "qa", "monitor": "monitor", "entity": "entity"}[kind], unit_row, us)


def build(dirs, export_csv=None):
    plants = {}
    labels, states, quarters, country = [], [], [], ""
    columns = []
    candidates = {}      # candidate slug -> the first watch item staged for it (for duplicate marks)
    # the scope's country decides whether the US-only checklist group exists
    metas = [m for d in dirs for lane in LINE_LANES + tuple(ITEM_LANES) for m in [load_lane(d, lane)[0]] if m]
    first_country = next((m.get("scope", {}).get("country") for m in metas if m.get("scope", {}).get("country")), "")
    us = (first_country or "United States") == "United States"
    for d in dirs:
        d = Path(d)
        if not d.is_dir():
            raise SystemExit(f"not a staging dir: {d}")
        label = rel(d)
        labels.append(label)
        lanes = {lane: load_lane(d, lane) for lane in LINE_LANES + tuple(ITEM_LANES)}
        meta = next((m for m, _ in lanes.values() if m), {})
        scope = meta.get("scope") or {}
        state = scope.get("state") or scope.get("country") or d.parent.name
        if state not in states:
            states.append(state)
        if scope.get("quarter") and scope["quarter"] not in quarters:
            quarters.append(scope["quarter"])
        country = country or scope.get("country") or ""
        csv_path = export_csv or scope.get("csv") or paths.gogpt_scoped_csv()
        uids = {r.get("gem_unit_id") for _, recs in lanes.values() for r in recs if r.get("gem_unit_id")}
        header, rows = load_export(csv_path, uids)
        if header and not columns:
            columns = header
        if uids and not rows:
            # a discovery folder holds only plants GEM does not track yet, so
            # it has no unit ids to look up and no warning to give
            print(f"review_data: export csv not read ({csv_path}); current Data Source cells unknown",
                  file=sys.stderr)

        def card(r):
            pid = r.get("gem_plant_id") or ""
            key = (label, pid)
            if not pid:
                # a plant GEM does not track yet (a discovery candidate, a new plant row): one card
                # per candidate name across every folder, with a stable "new:" id so links and
                # decisions hold and the same candidate staged twice lands on one card
                pid = "new:" + (candidate_key(r.get("plant_name")) or r["record_id"])
                key = ("*", pid)
            p = plants.get(key)
            if p is None:
                p = plants[key] = {
                    "pid": pid, "name": r.get("plant_name") or pid, "country": r.get("country") or country,
                    "state": state, "dir": label, "statewide": bool(_STATE_PID.match(pid)),
                    "units": [], "lines": [], "items": []}
            uid = r.get("gem_unit_id")
            if uid and uid not in {u["gem_unit_id"] for u in p["units"]}:
                # irp_box: the database's IRP checkbox as the export shows it (yes / no / "")
                box = str((rows.get(uid) or {}).get("IRP") or "").strip().lower()
                p["units"].append({"gem_unit_id": uid, "unit_name": r.get("unit_name") or "", "irp_box": box})
            return p

        def unit_row_for(r):
            row = rows.get(r.get("gem_unit_id") or "")
            if row:
                return row
            for s in r.get("sibling_unit_ids") or []:
                if s in rows:
                    return rows[s]
            if r.get("gem_plant_id"):
                return next((x for x in rows.values() if x.get("GEM location ID") == r["gem_plant_id"]), {})
            return {}

        for lane in LINE_LANES:
            for r in lanes[lane][1]:
                if not r.get("record_id"):
                    raise SystemExit(f"{d}/staged_{lane}.json: a record has no record_id (rebuild with assemble_state.py)")
                p = card(r)
                p["lines"].append(update_line(r, label, rows, us) if lane == "updates" else new_row_line(r, label, lane, us))
        for lane, kind in ITEM_LANES.items():
            for r in lanes[lane][1]:
                if not r.get("record_id"):
                    raise SystemExit(f"{d}/staged_{lane}.json: a record has no record_id (rebuild with assemble_state.py)")
                it = item(r, label, kind, unit_row_for(r), us)
                p = card(r)
                if kind == "monitor" and it["monitor_kind"] == "new_to_tracker":
                    first = candidates.get(p["pid"])
                    if first is None:
                        candidates[p["pid"]] = it
                    else:
                        it["duplicate_of"] = first["key"]
                p["items"].append(it)

    out = []
    for p in plants.values():
        for u in p["units"]:
            u["n"] = sum(1 for l in p["lines"] if l["gem_unit_id"] == u["gem_unit_id"])
        p["units"].sort(key=lambda u: (u["unit_name"], u["gem_unit_id"]))
        out.append(p)
    out.sort(key=lambda p: (p["state"], p["statewide"], p["name"].lower(), p["pid"]))
    tags = [o for p in out for o in p["lines"] + p["items"]]
    return {"built": datetime.now(ET).isoformat(timespec="seconds"),
            "scope": {"country": country or "United States", "states": states, "quarter": ", ".join(quarters)},
            "us": us, "groups": summarize(tags, us), "links": closeout_links(),
            "dirs": labels, "columns": columns, "plants": out}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", action="append", default=[], help="batch scope, e.g. us-md (repeatable)")
    ap.add_argument("--dirs", nargs="*", default=[], help="explicit staging dirs")
    ap.add_argument("--export-csv", default=None, help="scoped export csv for current Data Source cells")
    ap.add_argument("--out", default=None, help="dataset path (default work/review_data.json)")
    args = ap.parse_args(argv)
    dirs = [ROOT / "batches" / s / "staging" for s in args.scope] + [Path(d) for d in args.dirs]
    if not dirs:
        raise SystemExit("name at least one --scope or --dirs")
    data = build(dirs, args.export_csv)
    out = Path(args.out) if args.out else paths.work_dir() / "review_data.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    nl = sum(len(p["lines"]) for p in data["plants"])
    ni = sum(len(p["items"]) for p in data["plants"])
    print(f"review_data: {out} ({len(data['plants'])} plants, {nl} lines, {ni} items, "
          f"{len(data['dirs'])} staging dirs)", file=sys.stderr)
    return data


if __name__ == "__main__":
    main()
