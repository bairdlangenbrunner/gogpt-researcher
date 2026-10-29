"""
Build the review app's dataset from one or more staging dirs.

    python review_app/review_data.py --scope us-md --scope us-ny [--out work/review_data.json]
    python review_app/review_data.py --dirs batches/us-md/staging ... [--export-csv PATH]

Reads ONLY staged_{updates,qa,monitor,entity,newunits,newplants}.json in each staging dir
(never the shards, briefs, comparison.json or the blind copies). Writes one JSON file:

    {"built", "scope": {"country", "states", "quarter"}, "dirs": [label, ...], "columns": [...],
     "plants": [{"pid", "name", "country", "state", "dir", "wiki", "no_changes",
                 "units": [{"gem_unit_id", "unit_name", "irp_box", "status", "capacity", "last_updated", "researcher", "research_status"}],
                 "lines": [...], "items": [...]}]}

Cards come in three kinds (`card_kind`), and what a record IS decides which card it lands on;
how strong its evidence is only changes a chip on the card:

- `plant`: the edits to a plant GEM tracks. One card per GEM plant ID (a statewide pseudo-card
  for records whose plant ID is the state slug): the updates lines, sourced validation
  answers, concerns and entity checks. `pid` is the GEM plant ID.
- `addition`: a proposed new plant or new units. A plant GEM does not track yet gets one card
  keyed by its name with any parenthetical stripped (`pid` "new:<slug>", so the same candidate
  staged in two folders shares one card and the later watch item is marked `duplicate_of` the
  first): its newplants line and any watch item that is `new_to_tracker`. A tracked plant
  gets a separate "new units at" card, `pid` "<GEM id>#add", holding its newunits lines (one
  decidable block per unit) and its leads: watch items assemble_state.py made from a new-row
  record too thin to stage (`lead_for` names the lane it was headed for, newunits or
  newplants; review_app/checklist.py reads the older note prefix too).
- `watch`: a genuine watch at a tracked plant (`existing_plant` watch items that are not
  leads), `pid` "<GEM id>#watch".

Every card carries `plant_pid` (the GEM plant ID, "" for a plant GEM does not track); the
plant card's `pid` is unchanged so older plant flags and routes still match. Cards sort plant
edits first, then additions, then the watch list, so the page shows three headed sections.

A LINE is a staged edit the reviewer accepts, holds, rejects or suggests on: one per
updates/newunits/newplants record. An ITEM is a note that never writes a cell: a qa concern,
a monitor note, an entity lookup. Keys are `<dir label>::<record_id>`, the dir label is
repo-relative (`batches/us-md/staging`), and record_id is the stable id written by
scripts/assemble_state.py, so decisions survive a rebuild.

Every line and item carries `group` (a QC/Country checklist group id, review_app/checklist.py
GROUPS, or "other"), `group_label` and `checks` (the checklist rows it ticks), and the dataset
carries `groups` (the groups for this scope with counts and rows) and `us`. Watch items
(monitor lane) carry `monitor_kind` (`existing_plant` | `new_to_tracker`) and `lead_for`.
A new-row line carries `ready`: at least one of its links was verified to state a value.

Line kinds: fill (blank cell gets a value), change (a value is replaced), reverified (the
current value was checked and stands; only the Data Source link is new), delete (a value is
cleared), plant (a plant-level change applied to every unit row), new_row (a new unit or
plant), checked (see below).

Every plant GEM tracks in the scope is on the page, not only the ones the batch touched: the
export rows of the scope's country and state are read whole, a plant card gets every unit of
its plant (with the unit's Status, Capacity, Last Updated, Researcher and Research status as
the export shows them), and a plant no record touches gets a card flagged `no_changes` with
one `checked` line (key `<dir>::checked:<plant id>`, severity `check`) that the researcher
marks checked once they have looked at the plant and set its Last Updated and Research status
in the database, or holds for later. The card lands in the first staging dir of that scope
(a discovery dir never gets one). The page's status filter opens on the plants in
development, so the researcher can say every one of them was looked at.

Validation report answers (check 7): a qa answer that proposes a value with a source
(validation_report.is_fix) is a LINE, not an item, with `validation_fix: true` and lane "qa",
so the reviewer accepts it like any edit (milestone dates have no export column; the workbook
lists accepted ones on its validation_fixes sheet). Every check-7 line and item carries
`validation_errors`: the database's error it answers, from the scope's current
work/validation_<tag>.json, else the batch's brief task marked as gone from the report. Severity: `minor` for a reverified
line, a Status Detail edit, or an edit whose value equals the current cell and only adds a
link to a cell that already has one; `major` for everything else (a cell value changes). `default` is "accept" for high-confidence lines (one fully validated source, or two
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
from review_app.checklist import GROUP_BY_ID, MONITOR_KINDS, lead_for, summarize, tag  # noqa: E402
import geo  # noqa: E402
import validation_report  # noqa: E402

ET = ZoneInfo("America/New_York")
KIND_ORDER = {"plant": 0, "addition": 1, "watch": 2}
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


def load_export(csv_path, unit_ids, country="", state=""):
    """(header, {unit id: row dict}) for the unit ids named plus, when a country is given, every
    row of that country (and state, when one is given); ([], {}) when the csv is missing."""
    if not csv_path or not Path(csv_path).exists():
        return [], {}
    rows = {}
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        i_uid = header.index("GEM unit ID")
        i_c = header.index("Country/Area") if country and "Country/Area" in header else -1
        i_s = header.index("State/Province") if state and "State/Province" in header else -1
        for row in reader:
            if len(row) <= i_uid:
                continue
            keep = row[i_uid] in unit_ids
            if not keep and i_c >= 0 and row[i_c] == country:
                keep = i_s < 0 or row[i_s] == state
            if keep:
                rows[row[i_uid]] = dict(zip(header, row))
    return header, rows


def unit_entry(uid, row, unit_name=""):
    """A plant card's unit, from its export row: the IRP box (yes / no / ""), the current Status
    (never a proposed value), Capacity, and the research bookkeeping columns."""
    row = row or {}
    return {"gem_unit_id": uid, "unit_name": unit_name or str(row.get("Unit name") or ""),
            "irp_box": str(row.get("IRP") or "").strip().lower(),
            "status": str(row.get("Status") or "").strip(), "capacity": str(row.get("Capacity (MW)") or "").strip(),
            "last_updated": str(row.get("Last Updated") or "").strip(), "researcher": str(row.get("Researcher") or "").strip(),
            "research_status": str(row.get("Research status") or "").strip()}


def _norm(v):
    return re.sub(r"\s+", " ", str(v if v is not None else "")).strip().lower()


def severity_of(kind, reverified, column, fields, current, current_ref):
    """minor: the value stands and only a link is added (reverified; or the proposed value equals
    the current cell, which already has a Data Source link), or the edit is to Status Detail.
    major: a cell value moves."""
    if reverified or column == "Status Detail":
        return "minor"
    if kind in ("fill", "change") and fields and current_ref:
        if all(_norm(fields.get(c)) == _norm(current.get(c)) and _norm(fields.get(c)) for c in fields):
            return "minor"
    return "major"


def checked_line(label, pid, units, us=True):
    """The one line of a plant no record touched: "no suggested changes", to mark checked."""
    dev = any(is_dev_status(u.get("status")) for u in units)
    line = {"key": f"{label}::checked:{pid}", "dir": label, "record_id": f"checked:{pid}",
            "kind": "checked", "reverified": False, "severity": "check",
            "column": "", "columns": [], "ref_col": "", "gem_unit_id": "", "unit_name": "",
            "current": {}, "current_ref": [], "proposed_values": {}, "proposed_refs": [], "verifications": {},
            "tier": "", "independent": False, "validation_errors": [], "source_language": "",
            "notes": "", "action": "", "sibling_unit_ids": [u["gem_unit_id"] for u in units], "sibling_current": {},
            "publishers": 0, "default": "hold", "decision": None, "reviewed": False, "irp": False}
    gid = 3 if dev else 9
    line["group"] = gid
    line["group_label"] = GROUP_BY_ID[gid]["label"]
    line["checks"] = [10, 53] if dev else [53]
    return line


DEV_STATUS = ("announced", "preconstruction", "construction", "shelved", "shelvedinferred")


def is_dev_status(s):
    """The page's in-development statuses, compared by letters only and without an inferred age."""
    base = re.sub(r"\s+\d+\s*y(ears?)?$", "", str(s or "").strip(), flags=re.I)
    return re.sub(r"[^a-z]", "", base.lower()) in DEV_STATUS


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


LOC_ZOOM = 16
TILE_UA = "Mozilla/5.0 (gogpt-researcher review page)"


def _tile_data_uri(z, x, y):
    """One Esri tile as a data URI, from the cache under work/tiles or the network; "" if missing.
    The review page embeds its satellite tiles because an artifact page may not load images from
    other hosts (Baird's browser showed broken images, 2026-10-21)."""
    import base64
    import time
    import urllib.request
    path = paths.work_dir() / "tiles" / str(z) / str(x) / f"{y}.jpg"
    if not path.exists():
        for attempt in range(2):
            try:
                req = urllib.request.Request(geo.tile_url(x, y, z), headers={"User-Agent": TILE_UA})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read()
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                break
            except Exception:
                if attempt == 0:
                    time.sleep(1)
    if not path.exists():
        return ""
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def point_tiles(lat, lon):
    """The 2 by 2 block of tiles the page draws around a point (same grid as ext.js locPane):
    {"x0", "y0", "z", "uris": [row-major, 4]}, or {} when a tile could not be fetched."""
    import math
    tx, ty = geo.tile_xy(lat, lon, LOC_ZOOM)
    x0, y0 = math.floor(tx - 0.5), math.floor(ty - 0.5)
    uris = [_tile_data_uri(LOC_ZOOM, x0 + dx, y0 + dy) for dy in (0, 1) for dx in (0, 1)]
    return {"z": LOC_ZOOM, "x0": x0, "y0": y0, "uris": uris} if all(uris) else {}


MAP_RENDER_CAPTION = "saved map render"


def map_render(image, label, root=None):
    """The location record's saved map render (`location_image`, relative to the batch folder above the staging dir `label`) as one image dict for the page, `{role, caption, asset, path, width, height}` (the `line.location.image` shape in ../gem-review-app/docs/plan.md), or "" when the record has none.
    The picture is copied to work/review_assets/<sha256>.jpg by review_core.assets.prepare, as the pipelines map pictures are, so the artifact page loads it from its own uploads (`url`, which build_static fills from review_app/assets.json) instead of a repo path it cannot reach (the broken "saved map render" picture, 2026-10-27). A file that is missing or unreadable keeps its path and caption with no asset, and the page says the picture was not uploaded."""
    if not image:
        return ""
    rel = (Path(label).parent / image).as_posix()
    out = {"role": "render", "caption": MAP_RENDER_CAPTION, "path": rel}
    from review_core import assets as core_assets
    root = Path(root or ROOT)
    got = core_assets.prepare(root / rel, root)
    if got:
        out.update({"asset": got["asset"], "width": got["width"], "height": got["height"]})
    return out


def location_block(r, label, current):
    """The `location` dict of a staged location record (fields hold Latitude): the current and
    proposed points with their Google Maps links, how the point was found, and the saved map
    render as an artifact asset (map_render)."""
    fields = r.get("fields") or {}

    def point(src):
        lat, lon = geo.parse_coord(src.get("Latitude")), geo.parse_coord(src.get("Longitude"))
        ok = geo.valid_point(lat, lon)
        links = geo.links_for(lat, lon) if ok else {}
        return {"lat": lat if ok else None, "lon": lon if ok else None,
                "accuracy": str(src.get("Location accuracy") or ""),
                "satellite": links.get("satellite"), "pin": links.get("pin"),
                "tiles": point_tiles(lat, lon) if ok else {}}

    return {"current": point(current), "proposed": point(fields),
            "moved_m": r.get("location_moved_m"), "method": r.get("location_method") or "",
            "needs_review": bool(r.get("location_needs_review")),
            "control_points": list(r.get("location_control_points") or []),
            "fit_m": r.get("location_fit_m"), "image": map_render(r.get("location_image"), label)}


def update_line(r, label, export_rows, us=True):
    kind = line_kind(r)
    fields = dict(r.get("fields") or r.get("proposed_value") or {})
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
        "kind": kind, "reverified": reverified, "severity": severity_of(kind, reverified, column, fields, current, current_ref),
        "column": column, "columns": cols, "ref_col": ref_col,
        "gem_unit_id": uid, "unit_name": r.get("unit_name") or "",
        "current": current, "current_ref": current_ref,
        "proposed_values": fields, "proposed_refs": proposed_refs,
        "verifications": verification_map(r),
        "tier": tier_of(r), "independent": bool(r.get("independent")),
        "validation_errors": list(r.get("_validation_errors") or []),
        "source_language": r.get("source_language") or "",
        "notes": r.get("researcher_notes") or "", "action": r.get("action") or "",
        "sibling_unit_ids": list(r.get("sibling_unit_ids") or []),
        "sibling_current": r.get("sibling_current") or {},
        "publishers": len({host_of(u) for u in proposed_refs if host_of(u)}),
        "default": "accept" if tier_of(r) == "high" else "hold",
        "decision": None, "reviewed": False,
        "irp": bool(r.get("irp")),
    }
    if "Latitude" in fields:
        line["location"] = location_block(r, label, current)
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
        # ready to add: at least one link was verified to state a value on the page
        "ready": any(v.get("contains_value") for v in verifications.values()),
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
        "validation_errors": list(r.get("_validation_errors") or []),
    }
    if kind == "concern":
        it["concern_type"] = r.get("concern_type") or ""
        it["concern_type_raw"] = r.get("concern_type_raw") or ""
        it["recommendation"] = r.get("recommendation") or ""
        it["question"] = r.get("question") or ""
        it["finding"] = r.get("finding") or ""
        it["recommendation_raw"] = r.get("recommendation_raw") or ""
        if r.get("merged_from"):
            it["merged_from"] = r["merged_from"]
        # a value the answer suggests without a source (a sourced one is a line instead)
        pv = r.get("proposed_value") or {}
        it["proposed_value"] = dict(pv) if isinstance(pv, dict) else {"value": str(pv)}
    elif kind == "monitor":
        # older records kept the one-line reason under `item`; the page reads `reason`
        it["monitor_kind"] = monitor_kind(r)
        it["lead_for"] = lead_for(r)
        it["plant_name"] = r.get("plant_name") or ""
        it["reason"] = r.get("monitor_reason") or r.get("item") or ""
        # recheck_by stays in the staged record for the next batch's briefs; the reviewer never sees it (Baird 2026-10-26)
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


def validation_fix_line(r, label, export_rows, us=True):
    """A qa answer to a validation error with a value and a source, as an edit line: the
    value is the record's proposed_value, the action its recommendation."""
    rec = dict(r)
    cur = dict(r.get("current") or {})
    row = export_rows.get(r.get("gem_unit_id") or "") or {}
    blank = all(not str(cur.get(c, row.get(c, "")) or "").strip() for c in r["proposed_value"])
    rec.update({"fields": dict(r["proposed_value"]), "verdict": "fill" if blank else "change",
                "action": r.get("recommendation") or r.get("action") or ""})
    line = update_line(rec, label, export_rows, us)
    line.update({"validation_fix": True, "lane": "qa"})
    return line


def build(dirs, export_csv=None):
    plants = {}
    scope_rows = {}      # (country, state) -> (dir label, state name, export rows) of the first staging dir of that scope
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
        verrs = validation_report.load_report(scope) if scope else []
        ix = d.parent / "briefs" / "_index.json"
        vtasks = validation_report.brief_tasks(json.loads(ix.read_text(encoding="utf-8")) if ix.exists() else {})
        uids = {r.get("gem_unit_id") for _, recs in lanes.values() for r in recs if r.get("gem_unit_id")}
        # the whole scope's rows, so every plant GEM tracks there gets a card
        scope_country = scope.get("country") or ""
        scope_state = scope.get("state") or ""
        header, rows = load_export(csv_path, uids, scope_country, "" if scope_state == scope_country else scope_state)
        if header and not columns:
            columns = header
        if rows and (scope_country, scope_state) not in scope_rows and "discovery" not in d.name:
            scope_rows[(scope_country, scope_state)] = (label, state, rows)
        if uids and not rows:
            # a discovery folder holds only plants GEM does not track yet, so
            # it has no unit ids to look up and no warning to give
            print(f"review_data: export csv not read ({csv_path}); current Data Source cells unknown",
                  file=sys.stderr)

        def card(r, kind="plant"):
            """The card a record lands on: its plant's `plant` card, the plant's `addition`
            card (new units and leads, pid "<id>#add"), its `watch` card ("<id>#watch"), or
            for a plant GEM does not track the one `addition` card keyed by its name."""
            plant_pid = r.get("gem_plant_id") or ""
            statewide = bool(_STATE_PID.match(plant_pid))
            if not plant_pid:
                # a plant GEM does not track yet (a discovery candidate, a new plant row): one card
                # per candidate name across every folder, with a stable "new:" id so links and
                # decisions hold and the same candidate staged twice lands on one card
                kind = "addition"
                pid = "new:" + (candidate_key(r.get("plant_name")) or r["record_id"])
                key = ("*", pid, kind)
            elif statewide or kind == "plant":
                # the statewide pseudo-card keeps everything; the plant card keeps its bare pid
                # so older plant-level flags and routes still match
                kind, pid = "plant", plant_pid
                key = (label, pid, kind)
            else:
                pid = f"{plant_pid}#{'add' if kind == 'addition' else 'watch'}"
                key = (label, pid, kind)
            p = plants.get(key)
            if p is None:
                p = plants[key] = {
                    "pid": pid, "plant_pid": plant_pid, "card_kind": kind,
                    "name": r.get("plant_name") or plant_pid or pid, "country": r.get("country") or country,
                    "state": state, "dir": label, "statewide": statewide,
                    "wiki": "", "units": [], "lines": [], "items": []}
            uid = r.get("gem_unit_id")
            if not p.get("wiki"):
                # the plant's GEM wiki page, from the export's Wiki URL cell on any of its unit rows
                p["wiki"] = str((rows.get(uid or "") or unit_row_for(r) or {}).get("Wiki URL") or "").strip()
            if uid and uid not in {u["gem_unit_id"] for u in p["units"]}:
                p["units"].append(unit_entry(uid, rows.get(uid), r.get("unit_name") or ""))
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
                if validation_report.is_answer(r):
                    r = {**r, "_validation_errors": validation_report.errors_for(r, verrs, vtasks)}
                if lane == "updates":
                    card(r)["lines"].append(update_line(r, label, rows, us))
                else:
                    card(r, "addition")["lines"].append(new_row_line(r, label, lane, us))
        for lane, kind in ITEM_LANES.items():
            for r in lanes[lane][1]:
                if not r.get("record_id"):
                    raise SystemExit(f"{d}/staged_{lane}.json: a record has no record_id (rebuild with assemble_state.py)")
                if lane == "qa" and validation_report.is_answer(r):
                    r = {**r, "_validation_errors": validation_report.errors_for(r, verrs, vtasks)}
                    if validation_report.is_fix(r):
                        card(r)["lines"].append(validation_fix_line(r, label, rows, us))
                        continue
                it = item(r, label, kind, unit_row_for(r), us)
                if kind != "monitor":
                    p = card(r)
                elif it["monitor_kind"] == "new_to_tracker" or it["lead_for"]:
                    # a candidate plant, or a new-unit lead at a tracked plant: a proposed addition
                    p = card(r, "addition")
                else:
                    p = card(r, "watch")
                if kind == "monitor" and it["monitor_kind"] == "new_to_tracker":
                    first = candidates.get(p["pid"])
                    if first is None:
                        candidates[p["pid"]] = it
                    else:
                        it["duplicate_of"] = first["key"]
                p["items"].append(it)

    # every plant in the scope: a plant card gets all of its units, and a plant no record touched gets a card with one "checked" line
    by_plant = {}
    for (label, state, rows) in scope_rows.values():
        for uid, row in rows.items():
            lid = str(row.get("GEM location ID") or "").strip()
            if lid:
                by_plant.setdefault(lid, []).append((uid, row))
        for lid, units in by_plant.items():
            have = next((p for (lb, pid, kind), p in plants.items() if kind == "plant" and pid == lid), None)
            if have is None:
                row0 = units[0][1]
                have = plants[(label, lid, "plant")] = {
                    "pid": lid, "plant_pid": lid, "card_kind": "plant", "no_changes": True,
                    "name": str(row0.get("Plant name") or "").strip() or lid, "country": str(row0.get("Country/Area") or "").strip() or country,
                    "state": str(row0.get("State/Province") or "").strip() or state, "dir": label, "statewide": False,
                    "wiki": str(row0.get("Wiki URL") or "").strip(), "units": [], "lines": [], "items": []}
            known = {u["gem_unit_id"] for u in have["units"]}
            for uid, row in units:
                if uid not in known:
                    have["units"].append(unit_entry(uid, row))
            if not have["lines"]:
                have["lines"].append(checked_line(have["dir"], lid, have["units"], us))
                have["no_changes"] = True
        by_plant = {}

    out = []
    for p in plants.values():
        for u in p["units"]:
            u["n"] = sum(1 for l in p["lines"] if l["gem_unit_id"] == u["gem_unit_id"])
        p["units"].sort(key=lambda u: (u["unit_name"], u["gem_unit_id"]))
        out.append(p)
    # plant edits first (plants with proposed changes before the ones with none), then proposed additions, then the watch list
    out.sort(key=lambda p: (KIND_ORDER[p["card_kind"]], p["state"], p["statewide"], bool(p.get("no_changes")), p["name"].lower(), p["pid"]))
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
