"""
Sort staged records into the QC/Country checklist's groups and rows.

The "QC/Country checklist" tab of the Q4 2026 GOGPT Update V2 sheet is what a
researcher ticks off at the end of a country or state. Its rows 6 to 56 are
grouped here into nine review groups so the review page and the actions
workbook can show every edit, question and watch item under the checkbox it
helps tick (notes/review_app_checklist_plan.md, "The nine groups").

    from review_app.checklist import tag, GROUPS, ROWS, group_of_row
    t = tag(record, "updates", unit_row=export_row, us=True)
    t == {"group": 2, "checks": [9, 18], "group_label": "Blanks and unknowns"}

`tag()` never reads the staged-JSON contract's required fields differently from
review_data.py; `group` and `checks` are derived values, not part of the
contract. Precedence, first hit wins for the group, and `checks` keeps every
row that matches (plan, "How the tag is computed"):

1. provenance: a record's `checks` list, copied by assemble_state.py from the
   brief task that asked for the field;
2. the staged column and its current value (TABLE below);
3. the lane: newplants and newunits are group 8, entity is 6, monitor splits
   by `monitor_kind`, qa falls through to the field its concern_type names;
4. fallback: group 2 if the record fills a blank, else the visible "other"
   bucket. The caller counts "other" and prints it so TABLE gets extended.

Row labels are copied from the tab verbatim (2026-10-07) as `question`, with a
short `label` for the page. Rows 41 to 46 are optional and never counted open.
"""
from __future__ import annotations

import datetime
import re

OTHER = "other"

GROUPS = [
    {"id": 1, "key": "validation", "label": "Validation report", "rows": [7, 54],
     "blurb": "Edits and questions that fix an error from the GEM validation report."},
    {"id": 2, "key": "blanks", "label": "Blanks and unknowns",
     "rows": [8, 9, 11, 16, 17, 18, 19, 22, 25, 26],
     "blurb": "Empty or unknown cells that the research filled, and the ones it could not."},
    {"id": 3, "key": "status", "label": "Status and timeline",
     "rows": [10, 20, 21, 23, 24, 49, 50],
     "blurb": "Status changes, start and retirement years, planned retirements, Latest Activity."},
    {"id": 4, "key": "conversions", "label": "Conversions", "rows": [12, 13, 14],
     "blurb": "Coal-to-gas and other conversions: unit naming, fuel and technology, replacement links."},
    {"id": 5, "key": "equipment", "label": "Turbine make and model", "rows": [15],
     "blurb": "Equipment manufacturer and model, especially on units in development."},
    {"id": 6, "key": "owners", "label": "Owners and entities", "rows": [19, 43],
     "blurb": "Owner, operator and parent changes, and new owners or operators to create."},
    {"id": 7, "key": "us", "label": "IDs, IRPs and data centers", "rows": [34, 37, 38, 39],
     "us_only": True,
     "blurb": "United States only: EIA and other IDs, utility resource plans, gas-fired data centers."},
    {"id": 8, "key": "new", "label": "New to the tracker", "rows": [6, 31, 44, 51, 55],
     "blurb": "New plants and units ready to add, candidates to watch, and the possible-updates rows."},
    {"id": 9, "key": "closeout", "label": "Close-out",
     "rows": [29, 30, 32, 33, 34, 35, 36, 52, 53, 56], "panel": True,
     "blurb": "Not record-level: the sheet and doc updates, research status, and the two database checks."},
]

GROUP_BY_ID = {g["id"]: g for g in GROUPS}
OTHER_GROUP = {"id": OTHER, "key": OTHER, "label": "Other", "rows": [],
               "blurb": "Edits the checklist table does not place yet. Shown, never hidden."}

OPTIONAL_ROWS = frozenset(range(41, 47))
US_ONLY_ROWS = frozenset({34, 35, 36, 37, 38, 39})

# Row number -> (short label, the tab's wording). Header rows 5, 28, 41, 48 and
# blank rows 27, 40, 47 are not rows a researcher ticks.
ROWS = {
    6: ("Captive LNG sheet checked",
        "[*New*] Have you checked the captive LNG Sheet for new plants in your country?"),
    7: ("Validation report errors fixed",
        "Have you checked and fixed all errors from the validation report for your country?"),
    8: ("No blanks for fuel, status, technology, country, coordinates, accuracy, owner",
        "Check that there are no blank entries for: fuel, status, technology, country, coordinate, "
        "coordinate accuracy, owner"),
    9: ("Operating units with unknown start year rechecked",
        "Have you reresearched operating units with unknown start year?"),
    10: ("Every unit in development updated, with a Last Updated entry",
         'Have you updated and added a "Last Updated" entry for every unit in development for your country?'),
    11: ("Every unit has a unit name", "Does every unit have a unit name?"),
    12: ("Conversions carry \"timepoint\" in the unit name",
         'For any projects that are conversions, is "timepoint XYZ" included in the unit name?'),
    13: ("Coal-to-gas conversions have gas fuel and technology",
         "Do all coal to gas conversion units have a gas technology fuel and technology? "
         '(ie: no "subcritical" or "IGCC" etc)'),
    14: ("Waste-heat units have steam turbine technology",
         'Do all units with "waste heat from natural gas" have techology as "steam turbine"?'),
    15: ("Turbine make and model searched for in-development units",
         "Have you searched for turbine make/model for in development units? "
         '(including projects with "unknown").'),
    16: ("Zero-capacity units rechecked",
         "For any units with zero capacity, have you searched for an update?"),
    17: ("Unknown technology rechecked",
         "For any units with an unknown technology, have you searched for any update?"),
    18: ("Unknown start year rechecked",
         "For any projects with an unknown start year, have you searched for any update?"),
    19: ("Missing or unknown owner searched",
         "For any projects without an owner or unknown/not found owner, have you searched for the owner?"),
    20: ("No start year on cancelled or shelved projects",
         "No cancelled or shelved projects should have a start year."),
    21: ("Planned retirements searched", "Have you searched for planned retirements?"),
    22: ("Retired units have a retired year",
         'For any projects that are "retired", is there a date in the "Retired Year" column?'),
    23: ("Planned retirement year not in the past",
         "Planned retirement year should not be in the past. If no source confirms that a plant has "
         "been retired during the second annual research update, which concludes in December, update "
         "the retirement year to the following year."),
    24: ("Presumed cancelled or shelved units have a Latest Activity date and source",
         'For any projects that are presumed "cancelled" or "shelved", have you added the date and the '
         '"Latest Activity Datasource" to the "Latest Activity" field?'),
    25: ("Location data for every entry",
         "Is there location data (either exact or approximate) for every entry?"),
    26: ("City and state or province filled",
         "Is there additional location information (city and state/province) filled out for all entries?"),
    29: ("Country tips or United States research row updated",
         'Have you REVIEWED and UPDATED your country row in the "GOGPT country tips / trends" or '
         '"United States research" tab?'),
    30: ("Columns M and N on the assignments tab updated",
         'Have you UPDATED the columns M,N in the "Researcher Country Assignments" tab in this sheet?'),
    31: ("Possible-updates sheet reviewed",
         'Have you REVIEWED and UPDATED the "GEM trackers - possible updates" sheet for additional '
         "projects in your country?"),
    32: ("Data sources by country sheet updated",
         'Have you REVIEWED and UPDATED the "Gas power plant data sources - by country" sheet for '
         "additional projects/resources in your country?"),
    33: ("Europe workflow doc updated (Europe only)",
         "[EUROPE ONLY] Have you REVIEWED and UPDATED the Europe workflow doc?"),
    34: ("US IRPs tab updated for the state (US only)",
         '[USA ONLY] Have you REVIEWED and UPDATED the "US IRPs" tab for your state?'),
    35: ("United States research tab updated for the state (US only)",
         '[USA ONLY] Have you REVIEWED and UPDATED the "United States research" tab for your state?'),
    36: ("US Data/Research Guide updated for the state (US only)",
         '[USA ONLY] Have you REVIEWED and UPDATED the "GOGPT United States Data/Research Guide" for '
         "your state?"),
    37: ("IRP box ticked on every IRP project (US only)",
         '[USA ONLY] Have you checked the "IRP" box for all IRP projects in your state?'),
    38: ("GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)",
         "[USA ONLY] Have you matched GEM IDs to: EIA (use latest EIA 860M file), EIP, and Sierra Club?"),
    39: ("Gas-powered data centers searched, captive data entered (US only)",
         "[USA ONLY] Have you specifically searched for gas-powered data centers and included the "
         "captive data?"),
    42: ("Exact location for approximate operating units (optional)",
         'For any operating project with a location accuracy of "approximate", have you searched for '
         "an exact location?"),
    43: ("Ownership changes for operating units reviewed (optional)",
         "Have you reviewed any ownership changes for operating units?"),
    44: ("LNG terminals with captive plants checked (optional)",
         "Have you checked if LNG terminals in your country of research have or will have captive "
         "power plants? If yes, have you added them to the database?"),
    45: ("GOGPT country files folder reviewed (optional)",
         'Have you REVIEWED and UPDATED the "GOGPT country files" folder for additional projects in '
         "your country?"),
    46: ("GEM data sources sheet reviewed (optional)",
         'Have you REVIEWED and UPDATED the "GEM data sources" sheet for additional projects in your '
         "country?"),
    49: ("Construction to operating checked",
         "Have you checked for units that may have started operating (construction --> operating) for "
         "your countries?"),
    50: ("Other last-minute status changes checked",
         "Have you checked for any other last minute status changes (operating --> retired, "
         "announced/pre-construction --> construction)?"),
    51: ("Newly announced projects checked",
         "Have you checked for any newly announced projects for your countries?"),
    52: ("AI used to search for changes",
         "Have you used claude (or chatGPT or any other AI) to search for any changes or additions to "
         "your countries?"),
    53: ("All in-progress units moved to updated or no changes",
         'Have you reviewed all "in progress" units for your country and changed "Research status" to '
         '"updated" or "no changes"?'),
    54: ("Validation report errors fixed (end of update)",
         "Have you checked and fixed any errors from the validation report for your countries?"),
    55: ("Possible-updates rows marked done or Q2 2027",
         'Have you reviewed all entries in GEM possible updates and designated them as "done" or to be '
         'reviewed in "Q2 2027"?'),
    56: ("\"No tracker found\" units reviewed",
         'Have you reviewed the units under "no tracker found" to make sure any newly added units did '
         "not get assigned a tracker?"),
}


def row_label(n):
    return ROWS.get(n, ("", ""))[0]


def row_question(n):
    return ROWS.get(n, ("", ""))[1]


# A row that sits in two groups (19, 34) resolves to the first group listed;
# tag() overrides 19 to group 6 when the owner cell is not blank.
_ROW_GROUP = {}
for _g in GROUPS:
    for _r in _g["rows"]:
        _ROW_GROUP.setdefault(_r, _g["id"])


def group_of_row(n):
    return _ROW_GROUP.get(n)


def group_label(gid):
    return (GROUP_BY_ID.get(gid) or OTHER_GROUP)["label"]


def groups_for(us=True):
    """The groups a page or workbook shows for this scope: group 7 is dropped
    outside the United States. The "other" bucket is appended by the caller
    only when something landed in it."""
    return [g for g in GROUPS if us or not g.get("us_only")]


# ------------------------------------------------------------- vocabulary ---

IN_DEVELOPMENT = frozenset({"announced", "pre-construction", "construction"})
OWNER_COLUMNS = ("Owner(s)", "Operator(s)", "Parent(s)", "Owner Share Imputed",
                 "Parent Share Imputed", "Owner(s) GEM Entity ID",
                 "Operator GEM Entity ID", "Parent GEM Entity ID")
CAPACITY_COLUMNS = ("Capacity (MW)", "Number Of Engines", "Capacity Per Engine")
COORD_COLUMNS = ("Latitude", "Longitude", "Location accuracy")
PLACE_COLUMNS = ("City", "State/Province", "Local area (taluk, county)",
                 "Major area (prefecture, district)", "Subregion", "Region")
CONVERSION_COLUMNS = ("Conversion/replacement?", "Conversion from/replacement of (fuel)",
                      "Conversion from/replacement of (GEM unit ID)",
                      "Conversion to (fuel)", "Conversion to (GEM unit ID)")
CAPTIVE_COLUMNS = ("Captive industry use", "Captive industry type",
                   "Captive non-industry use", "Backup Power")
ID_COLUMNS = ("Other IDs (location)", "Other IDs (unit)", "WEPP location ID", "WEPP unit ID")
NAME_COLUMNS = ("Plant name", "Other Name(s)", "Plant Name in Local Language / Script")

# concern_type values that are not a column (docs/reference/staged_json_schema.md
# after the 2026-10-07 normalization) -> (group, rows)
CONCERN_KINDS = {
    "duplicate": (8, []),
    "existence": (8, [51]),
    "scope": (8, []),
    "capacity-threshold": (8, []),
    "identity": (2, [11]),
    "attribution": (6, [19]),
    "conversion-link": (4, [12, 13]),
    "location": (2, [25]),
    "source": (2, []),
    "validation": (1, [7]),
    "other": (None, []),
}

# Watch-list items (monitor lane) take these calls on the review page instead
# of accept / hold / reject / suggest. `remove` makes assemble_state.py drop
# the candidate if a later sweep proposes it again.
WATCH_CALLS = ("add_to_database", "hold", "possible_updates", "remove")
MONITOR_KINDS = ("new_to_tracker", "existing_plant")


def name_key(name):
    """Plant name reduced to lowercase letters and digits, for matching a
    watch-list candidate across sweeps."""
    return re.sub(r"[^a-z0-9]+", "", _ws(name).lower())


# The columns a concern may name. Anything else a shard writes is mapped by
# normalize_concern_type() below, and state_gate.py flags what still misses.
CONCERN_COLUMNS = (
    "Fuel", "Status", "Status Detail", "Start year", "Retired year", "Planned retire",
    "Cancellation year", "Latest Activity", "Capacity (MW)", "Number Of Engines",
    "Capacity Per Engine", "Turbine/Engine Technology", "Equipment Manufacturer/Model",
    "CHP", "CCS attachment?", "Unit name", "Plant name", "Other Name(s)",
) + OWNER_COLUMNS[:3] + COORD_COLUMNS + PLACE_COLUMNS[:2] + CONVERSION_COLUMNS[:1] \
    + CAPTIVE_COLUMNS[:3] + ID_COLUMNS[:2] + ("IRP", "Notes")
CONCERN_VOCAB = frozenset(CONCERN_COLUMNS) | frozenset(CONCERN_KINDS)

_CONCERN_WORDS = [
    # (regex on the lowercased, space-normalized shard value, canonical type)
    (r"^(capacity|uprate|register mismatch|mw)\b|capacity", "Capacity (MW)"),
    (r"^owner|ownership|^parent|^operator|attribution", "Owner(s)"),
    (r"status detail", "Status Detail"),
    (r"^status|status (conflict|mapping|change)|^permit|permit\b", "Status"),
    (r"start.?year", "Start year"),
    (r"retired year|retirement year", "Retired year"),
    (r"planned retire", "Planned retire"),
    (r"cancellation", "Cancellation year"),
    (r"latest.?activity|^stale", "Latest Activity"),
    (r"^technolog|^tech\b", "Turbine/Engine Technology"),
    (r"equipment|make.?model|manufacturer|turbine model", "Equipment Manufacturer/Model"),
    (r"^fuel", "Fuel"),
    (r"data.?cent|colocation|co-location", "Captive non-industry use"),
    (r"^captive", "Captive industry use"),
    (r"^(ids?|other.?ids?|identifier|eia (id|code))\b", "Other IDs (location)"),
    (r"^(unit.?name|naming|alias|name)\b", "identity"),
    (r"^(location|coordinates?|site)\b", "location"),
    (r"^(source|dead link|link|citation|reference)", "source"),
    (r"missing.?unit|unit.?missing|new.?unit|new.?plant|existence", "existence"),
    (r"duplicate", "duplicate"),
    (r"scope|unit (structure|definition|match)|misgrouped|cc block|grouping", "scope"),
    (r"threshold", "capacity-threshold"),
    (r"conversion|replacement", "conversion-link"),
    (r"identity|register", "identity"),
    (r"validation", "validation"),
]


def normalize_concern_type(raw, rec=None):
    """Map a shard's free-text concern_type to the vocabulary: a staged column
    name, or one of CONCERN_KINDS. A generic word (value, conflict, wrong
    value) takes the column of the record's single proposed_value, if any.
    Unknown text becomes "other"; the caller keeps the raw text beside it."""
    rec = rec or {}
    s = re.sub(r"[\s_]+", " ", _ws(raw)).strip().lower()
    if not s:
        return "other"
    for col in CONCERN_COLUMNS:
        if s == col.lower():
            return col
    proposed = rec.get("proposed_value") or {}
    if len(proposed) == 1 and next(iter(proposed)) in CONCERN_COLUMNS:
        if re.search(r"value|conflict|unverified|unsupported|wrong|stale|mismatch", s) \
                or s == "other":
            return next(iter(proposed))
    if s in CONCERN_KINDS:
        return s
    for pat, canon in _CONCERN_WORDS:
        if re.search(pat, s):
            return canon
    return "other"

_UNKNOWN = ("", "unknown", "not found", "n/a", "--", "none")
_DC = re.compile(r"data[ -]?cent(er|re)|hyperscale|colocation|co-location", re.I)
_EXPANSION = re.compile(r"new unit|additional unit|expansion|expand|second phase|phase 2|phase ii"
                        r"|repower|uprate|add(ing|s)? \d|new (cc|ct|block|turbine|engine)", re.I)


def _ws(v):
    return str(v or "").strip()


def _blank(v):
    return _ws(v).lower() in _UNKNOWN


def _zero(v):
    try:
        return float(_ws(v)) == 0
    except ValueError:
        return False


def _year(v):
    m = re.match(r"\s*(\d{4})", _ws(v))
    return int(m.group(1)) if m else None


def _status_group(status):
    s = _ws(status).lower()
    if s in IN_DEVELOPMENT:
        return "in development"
    for k in ("shelved", "cancelled", "mothballed", "retired", "operating"):
        if s.startswith(k):
            return k
    return "unknown"


def _kind(rec):
    if rec.get("delete"):
        return "delete"
    if rec.get("reverified") or rec.get("verdict") == "match":
        return "reverified"
    cur = rec.get("current") or {}
    if cur and all(_blank(x) for x in cur.values()):
        return "fill"          # "unknown" or "not found" counts as a blank being filled
    v = rec.get("verdict")
    return v if v in ("fill", "change") else "change"


# ------------------------------------------------------------- the table ---

def column_rows(col, kind, current, value, unit_row, us=True, today=None):
    """(group, rows) for one staged column. `kind` is fill / change /
    reverified / delete, `current` the GEM value, `value` the staged one,
    `unit_row` the export row of the unit (for its status and conversion
    flags) or {}."""
    unit_row = unit_row or {}
    today = today or datetime.date.today()
    status_now = _ws(unit_row.get("Status") or (current if col == "Status" else ""))
    sg = _status_group(status_now)
    indev = sg == "in development"
    conversion = not _blank(unit_row.get("Conversion/replacement?")) or col in CONVERSION_COLUMNS
    extra = [10] if indev and col in ("Status", "Status Detail", "Start year", "Latest Activity",
                                       "Equipment Manufacturer/Model", "Capacity (MW)",
                                       "Turbine/Engine Technology", "Owner(s)") else []

    if col == "Fuel":
        if kind == "fill":
            return 2, [8]
        if kind == "change" and (conversion or "waste heat" in _ws(value).lower()):
            return 4, [13, 14] if "waste heat" in _ws(value).lower() else [13]
        return 2, []
    if col == "Status":
        if kind == "fill":
            return 2, [8]
        if kind == "change":
            old, new = _ws(current).lower(), _ws(value).lower()
            rows = []
            if old == "construction" and new == "operating":
                rows.append(49)
            else:
                rows.append(50)
            if _status_group(old) == "in development":
                rows.append(10)
            if new.startswith(("shelved", "cancelled")):
                rows += [20]
                if "inferred" in new:
                    rows.append(24)
            return 3, sorted(set(rows))
        return 3, extra
    if col == "Status Detail":
        return 3, extra
    if col == "Start year":
        if kind == "delete":
            return 3, [20]
        if kind == "fill":
            return 2, [9, 18] if sg == "operating" else [18]
        return 3, extra
    if col == "Retired year":
        if kind == "fill":
            return (2, [22]) if sg == "retired" else (3, [21, 22])
        return 3, [21]
    if col == "Planned retire":
        rows = [21]
        y = _year(current)
        if y is not None and y < today.year:
            rows.append(23)
        return 3, rows
    if col == "Cancellation year":
        return 3, []
    if col == "Latest Activity":
        return 3, [24] + extra if "inferred" in status_now.lower() or sg == "shelved" else extra
    if col == "Disrupted by conflict":
        return 3, []
    if col == "Turbine/Engine Technology":
        if kind == "change" and conversion:
            return 4, [14] if "steam" in _ws(value).lower() else [13]
        if kind == "fill" or _blank(current):
            return 2, [8, 17] + extra
        return 2, [17] + extra
    if col == "Equipment Manufacturer/Model":
        return 5, [15] if indev else []
    if col in OWNER_COLUMNS:
        if kind == "fill" and col in ("Owner(s)", "Operator(s)", "Parent(s)"):
            return 2, [8, 19] if col == "Owner(s)" else [19]
        rows = [19] if kind != "reverified" else []
        if kind == "change" and sg == "operating":
            rows.append(43)
        return 6, rows
    if col in CAPACITY_COLUMNS:
        rows = [16] if (kind == "fill" or _zero(current)) else []
        return 2, rows + extra if col == "Capacity (MW)" else rows
    if col == "Unit name":
        if "timepoint" in _ws(value).lower():
            return 4, [12]
        return 2, [11] if kind == "fill" else []
    if col in COORD_COLUMNS:
        if kind == "fill":
            return 2, [8, 25]
        if col == "Location accuracy" and _ws(value).lower() == "exact":
            return 2, [25, 42]
        return 2, [25]
    if col in PLACE_COLUMNS:
        return 2, [26] if col in ("City", "State/Province") else [25]
    if col in CONVERSION_COLUMNS:
        return 4, [13]
    if col == "IRP":
        return (7, [37]) if us else (OTHER, [])
    if col in ID_COLUMNS:
        return (7, [38]) if us else (OTHER, [])
    if col in CAPTIVE_COLUMNS:
        if us:
            return 7, [39]
        return (2, []) if kind == "fill" else (OTHER, [])
    if col in ("CHP", "CCS attachment?"):
        return (2, []) if kind == "fill" else (OTHER, [])
    if col in NAME_COLUMNS or col == "Notes":
        return (2, []) if kind == "fill" else (OTHER, [])
    return None, []


# -------------------------------------------------------------------- tag ---

def tag(rec, lane, unit_row=None, us=True, today=None):
    """Group and checklist rows for one staged record.

    rec: a record from any of the six lanes. lane: its lane name.
    unit_row: the export row for rec's gem_unit_id (or any unit of the plant
    for a plant-level record), used for the unit's status and conversion flag.
    us: whether the scope is a US state (group 7 exists)."""
    unit_row = unit_row or {}
    checks = set()
    group = None

    # 1. provenance from the brief task
    prov = [int(c) for c in (rec.get("checks") or []) if str(c).isdigit()]
    if 7 in prov or 54 in prov or rec.get("validation"):
        group = 1
        checks.update(c for c in prov if c in ROWS)
        checks.add(7)
    elif prov:
        kind = _kind(rec)
        first = prov[0]
        group = group_of_row(first)
        if first == 19 and kind != "fill":
            group = 6
        checks.update(c for c in prov if c in ROWS)

    # IRP-sourced records live in group 7 whatever their column
    if rec.get("irp") and us:
        group = group or 7
        checks.add(37)

    # 2. column and current value
    if lane in ("updates",):
        kind = _kind(rec)
        cur = rec.get("current") or {}
        for col, value in (rec.get("fields") or {}).items():
            g, rows = column_rows(col, kind, cur.get(col, ""), value, unit_row, us, today)
            checks.update(rows)
            if group is None:
                group = g
        if group is None:
            group = 2 if kind == "fill" else OTHER

    # 3. lane
    elif lane in ("newplants", "newunits"):
        name = _ws(rec.get("plant_name")).lower()
        rows = [51]
        if "lng terminal" in name or rec.get("captive_lng"):
            rows = [6, 44]
        if _DC.search(" ".join(_ws(x) for x in (rec.get("researcher_notes"), rec.get("action"),
                                                  name, _ws((rec.get("fields") or {}).get(
                                                      "Captive non-industry use"))))):
            if us:
                checks.add(39)
        checks.update(rows)
        group = group or 8
    elif lane == "entity":
        checks.add(19)
        group = group or 6
    elif lane == "monitor":
        text = " ".join(_ws(rec.get(k)) for k in ("monitor_reason", "item", "researcher_notes",
                                                 "plant_name", "unit_name"))
        if rec.get("monitor_kind") == "existing_plant" or (
                rec.get("monitor_kind") is None and _ws(rec.get("gem_plant_id"))):
            if us and _DC.search(text):
                group, rows = 7, [39]
            elif _EXPANSION.search(text):
                group, rows = 8, [51]
            else:
                group, rows = 3, ([10] if _status_group(unit_row.get("Status")) == "in development"
                                  else [])
            checks.update(rows)
        else:
            group = group or 8
            checks.add(51)
            if "lng terminal" in text.lower():
                checks.update([6, 44])
            if us and _DC.search(text):
                checks.add(39)
    elif lane == "qa":
        ct = _ws(rec.get("concern_type")) or "other"
        if ct not in CONCERN_VOCAB:
            ct = normalize_concern_type(ct, rec)
        if ct in CONCERN_KINDS:
            g, rows = CONCERN_KINDS[ct]
            checks.update(rows)
            group = group or g
        else:
            # a column name: a question is tagged like a change on that column
            cur = (rec.get("current") or {}).get(ct, unit_row.get(ct, ""))
            prop = (rec.get("proposed_value") or {}).get(ct, "")
            kind = "fill" if _blank(cur) else "change"
            g, rows = column_rows(ct, kind, cur, prop, unit_row, us, today)
            checks.update(rows)
            group = group or g
        if group is None:
            group = OTHER
    else:
        group = group or OTHER

    if group is None:
        group = OTHER
    if not us and group == 7:
        group = OTHER
    checks = sorted(c for c in checks if c in ROWS and (us or c not in US_ONLY_ROWS))
    return {"group": group, "checks": checks, "group_label": group_label(group)}


def summarize(tags, us=True):
    """Counts per group and per row from a list of tag() results, in the
    page's order. `other` is appended only when non-empty."""
    out = []
    for g in groups_for(us) + [OTHER_GROUP]:
        n = sum(1 for t in tags if t["group"] == g["id"])
        if g["id"] == OTHER and n == 0:
            continue
        rows = [{"row": r, "label": row_label(r), "optional": r in OPTIONAL_ROWS,
                 "count": sum(1 for t in tags if r in t["checks"])} for r in g["rows"]]
        out.append({"id": g["id"], "key": g["key"], "label": g["label"], "blurb": g["blurb"],
                    "count": n, "rows": rows, "panel": bool(g.get("panel"))})
    return out
