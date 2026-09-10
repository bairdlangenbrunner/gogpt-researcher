"""
gogpt_checks.py  —  Cross-cutting checks module for the GOGPT research pipeline
=================================================================================
Provides four functions called by gogpt_csv_query.py:

    load_possible_updates(pu_file, country, state=None, plant_names=None) -> str (markdown)
    count_card_flags(card_text)              -> (dict, str markdown)
    ownership_scan(df_scope, label)          -> str (markdown)
    in_progress_scan(df_scope, label)        -> str (markdown)
    duplicate_scan(df_country, label)        -> str (markdown)

load_possible_updates auto-detects its input: a structured CSV export
(filtered by country/state + Status!=done) OR the flattened multi-tab Drive
sheet read via Google Drive:read_file_content (matched by a high-recall token
scan over geographic tokens AND in-scope plant names, so geographically
unlabeled ownership rows are still surfaced). See that function's docstring.

All scan functions receive a pandas DataFrame slice already filtered to the
target country/state (and optionally status) by gogpt_csv_query.py, plus a
human-readable label string such as "Germany" or "Texas, United States".
They return a markdown string ready to print / write to file.

This module never writes to disk and has no side-effects; the caller handles
all I/O.
"""

from __future__ import annotations

import re
import sys
from typing import Optional

try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas is required. Run: pip install pandas --break-system-packages")
    sys.exit(1)

# ── Column name constants (must match gogpt_csv_query.py) ──────────────────
COL_UNIT_ID     = "GEM unit ID"
COL_LOC_ID      = "GEM location ID"
COL_PLANT       = "Plant name"
COL_UNIT        = "Unit name"
COL_STATUS      = "Status"
COL_CAPACITY    = "Capacity (MW)"
COL_START_YEAR  = "Start year"
COL_OWNER       = "Owner(s)"
COL_PARENT      = "Parent(s)"
COL_OPERATOR    = "Operator(s)"
COL_FUEL        = "Fuel"
COL_CHP         = "CHP"
COL_RET_YEAR    = "Planned retire"
COL_CONFLICT    = "Disrupted due to conflict"
COL_COORDS_LAT  = "Latitude"
COL_COORDS_LON  = "Longitude"
COL_LOC_ACC     = "Location accuracy"
COL_TURBINE     = "Turbine/Engine Technology"
COL_TURBINE_MFR = "Equipment Manufacturer/Model"
COL_REGION      = "Region"
COL_STATE       = "State/Province"
COL_COUNTRY     = "Country/Area"
COL_STATUS_DT   = "Status Detail"

# Status values considered "in-development"
IN_DEV_STATUSES = {"announced", "pre-construction", "construction"}

# US state name → USPS code (for matching "US-OH" / ", OH |" tokens in the
# flattened Drive possible-updates sheet against a "Ohio" / "United States"
# query).
_US_STATE_CODE = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN",
    "mississippi": "MS", "missouri": "MO", "montana": "MT", "nebraska": "NE",
    "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
    "new mexico": "NM", "new york": "NY", "north carolina": "NC",
    "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR",
    "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA",
    "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
    "district of columbia": "DC",
}


def _country_match_tokens(country: str, state: Optional[str] = None) -> list[str]:
    """
    Build the lowercase token list a possible-updates row must contain (in any
    of its cells) to be considered a match for this country/state.

    Handles the flattened Drive sheet's mixed conventions:
      - full country / state name ("ohio", "united states")
      - "US-XX" style codes ("us-oh")
      - state-code-in-context (", oh |", "| oh |", " oh,")
    For a US-state query, the state is the discriminating token (NOT
    "united states", which would match every US row).
    """
    toks: list[str] = []
    c = (country or "").strip().lower()
    s = (state or "").strip().lower()

    # US state query: country may arrive as "United States" + state, OR the
    # state name itself may be passed as `country` (legacy call style).
    state_name = None
    if s and s in _US_STATE_CODE:
        state_name = s
    elif c in _US_STATE_CODE:
        state_name = c

    if state_name:
        code = _US_STATE_CODE[state_name]
        toks.append(state_name)                 # "ohio"
        toks.append(f"us-{code.lower()}")        # "us-oh"
        toks.append(f", {code.lower()} ")        # ", oh "  (in a cell)
        toks.append(f"| {code.lower()} |")       # "| oh |" (own cell)
        toks.append(f" {code.lower()},")         # " oh,"
        return toks

    # Non-US (or whole-US) query: match the country name as written.
    if c:
        toks.append(c)
    return toks

# ── Helpers ────────────────────────────────────────────────────────────────

def _col(df: pd.DataFrame, name: str) -> Optional[str]:
    """Case-insensitive column lookup; returns actual column name or None."""
    low = name.lower()
    for c in df.columns:
        if c.lower() == low:
            return c
    return None


def _get(row: pd.Series, name: str) -> str:
    """Return the string value for a column, or '' if missing/NaN."""
    try:
        v = row[name]
        return "" if pd.isna(v) else str(v).strip()
    except (KeyError, TypeError):
        return ""


def _to_float(val: str) -> Optional[float]:
    try:
        return float(val.replace(",", "")) if val else None
    except (ValueError, AttributeError):
        return None


def _unit_label(row: pd.Series) -> str:
    uid   = _get(row, COL_UNIT_ID)
    plant = _get(row, COL_PLANT)
    unit  = _get(row, COL_UNIT)
    parts = [x for x in [uid, plant, unit] if x]
    return " — ".join(parts) if parts else "(unknown unit)"


# ══════════════════════════════════════════════════════════════════════════════
# 1. load_possible_updates
# ══════════════════════════════════════════════════════════════════════════════

def load_possible_updates(pu_file: str, country: str,
                          state: Optional[str] = None,
                          plant_names: Optional[list[str]] = None) -> str:
    """
    Return a markdown digest of the GEM possible-updates rows that bear on the
    given country (and, for the US, an optional state).

    Two input formats are supported and auto-detected:

      1. **Structured CSV** — the standalone `GEM_trackers__possible_updates…csv`
         export with a clean header row including a `country` column. Filtered
         by exact country match, `Status != done`.

      2. **Flattened Drive sheet** — the live "GEM trackers - possible updates"
         Google Sheet, read via `Google Drive:read_file_content`, which arrives
         as a single multi-tab markdown/plain-text blob (`.md`/`.txt`). The tabs
         have *different* schemas (coal/gas/oil/ownership/data-center), and the
         operating-relevant ownership rows often carry **no country column at
         all** — the country is implied by the plant. A header-based filter
         would silently drop exactly those rows. So for this format we fall back
         to a **whole-row token scan**: any pipe-table row whose text contains a
         country/state token (see `_country_match_tokens`) is surfaced for the
         researcher to verify by hand. This is intentionally high-recall; the
         caller confirms each hit against the unit list.

    Parameters
    ----------
    pu_file : str
        Path to the CSV export *or* to the file the Drive read was written to.
    country : str
        Country/Area name (e.g. "United States", "Japan"). For a US state, may
        be "United States" with `state` set, or the state name itself.
    state : str, optional
        US state/province name (e.g. "Ohio") for US-state cycles.

    Returns
    -------
    str
        Markdown digest, or a message if nothing matched.
    """
    try:
        with open(pu_file, "r", encoding="utf-8-sig", errors="replace") as fh:
            raw = fh.read()
    except Exception as e:
        return f"ERROR: Could not read possible-updates file: {e}"

    if _looks_like_flattened_sheet(pu_file, raw):
        return _possible_updates_from_flattened(raw, country, state, plant_names)
    return _possible_updates_from_csv(pu_file, country, state)


def _looks_like_flattened_sheet(pu_file: str, raw: str) -> bool:
    """
    Heuristic: is this the flattened Drive sheet rather than the structured CSV?

    True when the file is markdown/text (.md/.txt) OR its body is dominated by
    pipe-delimited table rows (the Drive read renders every tab as `| … |`
    markdown tables) rather than comma-separated columns with a single header.
    """
    low = pu_file.lower()
    if low.endswith((".md", ".txt", ".json")):
        return True
    if low.endswith(".csv"):
        # A real CSV won't be full of '|' table rows.
        pipe_rows = sum(1 for ln in raw.splitlines() if ln.lstrip().startswith("|"))
        return pipe_rows > 5
    # Unknown extension: sniff the content.
    pipe_rows = sum(1 for ln in raw.splitlines() if ln.lstrip().startswith("|"))
    return pipe_rows > 5


def _possible_updates_from_csv(pu_file: str, country: str,
                               state: Optional[str]) -> str:
    """Structured-CSV path (original behaviour, with optional state matching)."""
    try:
        df = pd.read_csv(pu_file, dtype=str, encoding="utf-8-sig")
    except Exception as e:
        return f"ERROR: Could not read possible-updates file: {e}"

    df.columns = [c.strip() for c in df.columns]
    country_col = next((c for c in df.columns if c.lower() == "country"), None)
    status_col  = next((c for c in df.columns if c.lower() == "status"), None)

    if country_col is None:
        # No country column even in CSV form — degrade to a token scan over the
        # CSV's own text rather than erroring out (some exports are headerless).
        return _possible_updates_from_flattened(
            df.to_csv(index=False, sep="|"), country, state)

    label = state.strip() if state else country.strip()
    tokens = _country_match_tokens(country, state)
    col_series = df[country_col].fillna("").str.strip().str.lower()

    if state and state.strip().lower() in _US_STATE_CODE:
        # US state: match any token within the country cell.
        mask = col_series.apply(lambda v: any(t in v for t in tokens))
    else:
        mask = col_series == country.strip().lower()

    if status_col:
        mask &= df[status_col].fillna("").str.strip().str.lower() != "done"

    rows = df[mask]
    if rows.empty:
        return f"POSSIBLE UPDATES — {label}\n\nNo unresolved rows found."

    lines = [f"## POSSIBLE UPDATES — {label} (CSV source)\n",
             f"Unresolved rows: {len(rows)}\n"]
    for _, r in rows.iterrows():
        status   = (_get(r, "Status") or (_get(r, status_col) if status_col else ""))
        plant    = _get(r, "plant name")   or _get(r, "Plant name")
        capacity = _get(r, "capacity")     or _get(r, "Capacity (MW)")
        proj_st  = _get(r, "project status")
        notes    = _get(r, "update notes") or _get(r, "notes")
        url      = _get(r, "URL for more info")
        date     = _get(r, "date added")
        by       = _get(r, "added by")
        lines.append("---")
        if status:  lines.append(f"**Status:** {status}")
        if plant:   lines.append(f"**Plant:** {plant}")
        if capacity:lines.append(f"**Capacity:** {capacity} MW")
        if proj_st: lines.append(f"**Project status:** {proj_st}")
        if notes:   lines.append(f"**Notes:** {notes}")
        if url:     lines.append(f"**URL:** {url}")
        if date or by:
            lines.append(f"**Added:** {date}" + (f" by {by}" if by else ""))
        lines.append("")
    return "\n".join(lines)


def _possible_updates_from_flattened(raw: str, country: str,
                                     state: Optional[str],
                                     plant_names: Optional[list[str]] = None) -> str:
    """
    Token-scan path for the flattened multi-tab Drive sheet.

    Matches a row if EITHER:
      - its text contains a country/state token (geographic match), OR
      - its text contains one of the in-scope plant names (name match) — this
        is what catches geographically-unlabeled ownership rows like the
        gas-plants block, where the plant is named but no country cell exists.

    Rows whose first cell reads "done"/"resolved" are KEPT but tagged, not
    dropped: "done" in this sheet means a researcher actioned it, which is not
    the same as "confirmed in the current DB," so the caller should still see
    it. High-recall by design; the caller verifies each hit.
    """
    geo_tokens = _country_match_tokens(country, state)
    label = state.strip() if state else country.strip()

    # Some plant-name tokens are also common place/word names and cause false
    # positives when used for name-matching across other regions (e.g. an Ohio
    # "Madison" / "Richland" / "Waterford" / "Guernsey" matching a county, an
    # NPP, or the island elsewhere). Such rows are still caught by the
    # geographic scan when they are genuinely about this country/state, so we
    # exclude these tokens from *name* matching only.
    _GENERIC_NAME_STOP = {
        "madison", "richland", "waterford", "guernsey", "fremont", "dresden",
        "washington", "oregon clean", "troy energy", "cadiz", "bluegrass",
        "middletown", "edgeconnex data center", "dicks creek", "darby power",
    }
    # Build a clean, deduped, lowercased plant-name token set (skip very short
    # names that would over-match, e.g. a 2-char unit code).
    name_tokens: list[str] = []
    if plant_names:
        seen_n = set()
        for nm in plant_names:
            n = (nm or "").strip().lower()
            # Trim common suffixes so "Rolling Hills Generating power station"
            # still matches "Rolling Hills Generating LLC".
            for suf in (" power station", " power plant", " energy center",
                        " generating station", " energy facility"):
                if n.endswith(suf):
                    n = n[: -len(suf)]
                    break
            if len(n) >= 6 and n not in seen_n and n not in _GENERIC_NAME_STOP:
                seen_n.add(n)
                name_tokens.append(n)
    # Pre-compile word-boundary patterns for name tokens. Substring matching
    # over-fires on short/common names ("madison" → "madison.com",
    # "guernsey" → the island), so require the token to appear as a whole
    # word/phrase. Geographic tokens stay substring (they're already specific:
    # "us-oh", "| oh |", "ohio").
    name_patterns = [re.compile(r"\b" + re.escape(t) + r"\b") for t in name_tokens]

    if not geo_tokens and not name_tokens:
        return ("ERROR: no country/state token and no plant names to match "
                f"(country={country!r}, state={state!r}).")

    geo_rows: list[tuple[list[str], bool]] = []
    name_rows: list[tuple[list[str], bool]] = []
    seen: set[str] = set()

    for ln in raw.splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        low = s.lower()
        geo_hit  = any(t in low for t in geo_tokens)
        name_hit = any(p.search(low) for p in name_patterns)
        if not (geo_hit or name_hit):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        joined = " ".join(cells).lower()
        if set(joined) <= set("-| :") or joined.startswith("update status date added"):
            continue
        if sum(1 for c in cells if c) < 3:
            continue
        key = "|".join(cells)
        if key in seen:
            continue
        seen.add(key)
        resolved = bool(cells) and cells[0].strip().lower() in ("done", "resolved")
        # Prefer the geographic bucket; only put a row in the name bucket if it
        # did NOT also match geographically (avoids double-listing).
        if geo_hit:
            geo_rows.append((cells, resolved))
        else:
            name_rows.append((cells, resolved))

    if not geo_rows and not name_rows:
        return (f"POSSIBLE UPDATES — {label} (live Drive sheet)\n\n"
                "No matching rows found for this country/state or in-scope plant names.")

    def _emit(rows):
        out = []
        for cells, resolved in rows:
            out.append("---")
            tag = "  _(marked done/resolved in sheet — verify vs DB)_" if resolved else ""
            out.append(("  |  ".join(c for c in cells if c)) + tag)
            out.append("")
        return out

    lines = [f"## POSSIBLE UPDATES — {label} (live Drive sheet)\n",
             "Source: flattened 'GEM trackers - possible updates' sheet "
             "(multi-tab; matched by token scan, verify each by hand).\n",
             f"Geographic-match rows: {len(geo_rows)}  ·  "
             f"plant-name-match rows: {len(name_rows)}\n",
             f"Geo tokens: {', '.join(geo_tokens) or '(none)'}\n"]
    if geo_rows:
        lines.append("\n### Matched by country/state\n")
        lines += _emit(geo_rows)
    if name_rows:
        lines.append("\n### Matched by in-scope plant name "
                     "(geographically unlabeled — e.g. ownership rows)\n")
        lines += _emit(name_rows)
    lines.append("> High-recall across all tabs (coal/gas/oil/ownership/"
                 "data-center). Confirm each row is (a) in scope for this "
                 "session and (b) not already resolved in the DB before "
                 "recording a finding. 'done' tags mean a researcher actioned "
                 "the row, not that the current DB reflects it.")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# 2. count_card_flags
# ══════════════════════════════════════════════════════════════════════════════

# Map of emoji/token → flag key
_FLAG_PATTERNS = [
    ("new_proposals",       [r"🆕\s*NEW PROPOSAL"]),
    ("monitor",             [r"📋\s*MONITOR"]),
    ("updates",             [r"🔄\s*UPDATE"]),
    ("checks",              [r"⚠️\s*CHECK"]),
    ("turbine",             [r"⚙️\s*TURBINE"]),
    ("status_changes",      [r"❌\s*STATUS CHANGE"]),
    ("in_progress",         [r"⏳\s*IN PROGRESS"]),
    ("no_changes",          [r"✅\s*No changes?"]),
    ("duplicate_candidates",[r"⚠️\s*CHECK\s*[—\-]+\s*possible duplicate",
                             r"⚠️\s*duplicate candidate"]),
]

def count_card_flags(card_text: str) -> tuple[dict, str]:
    """
    Count each flag type found in the context card markdown.

    Parameters
    ----------
    card_text : str
        Full text of the context card .md file.

    Returns
    -------
    (counts_dict, markdown_table_str)
        counts_dict  : { flag_key: int, ... }
        markdown_table_str : human-readable table string
    """
    counts: dict[str, int] = {}

    for key, patterns in _FLAG_PATTERNS:
        total = 0
        for pattern in patterns:
            total += len(re.findall(pattern, card_text, re.IGNORECASE))
        counts[key] = total

    # Duplicate candidates are already counted inside 'checks' via their ⚠️;
    # de-duplicate the duplicate count so the CHECK total is net of duplicates.
    # We report both.
    dup_count = counts.get("duplicate_candidates", 0)
    net_checks = max(0, counts.get("checks", 0) - dup_count)

    flag_rows = [
        ("🆕 New proposals",       counts.get("new_proposals", 0)),
        ("📋 Monitor (undisclosed capacity)", counts.get("monitor", 0)),
        ("🔄 Updates",             counts.get("updates", 0)),
        ("⚠️ Checks (total)",      counts.get("checks", 0)),
        ("  ↳ of which ⚠️ Duplicate candidates", dup_count),
        ("⚙️ Turbine findings",    counts.get("turbine", 0)),
        ("❌ Status changes",      counts.get("status_changes", 0)),
        ("⏳ In-progress",         counts.get("in_progress", 0)),
        ("✅ No changes (excluded from export)", counts.get("no_changes", 0)),
    ]

    header = f"{'Flag type':<45} {'Count':>6}"
    sep    = "-" * 53
    rows   = [f"{name:<45} {str(count):>6}" for name, count in flag_rows]
    md     = "\n".join([header, sep] + rows)

    note = (
        "\nNote: ⏳ In-progress items are NOT included in the 🔄 Updates total.\n"
        "      ⚠️ Duplicate candidates are sub-counted within ⚠️ Checks.\n"
        "      Counts are raw occurrences — de-duplicate by hand before reporting.\n"
        "      📋 Monitor entries are not counted in 🆕 New proposals.\n"
    )

    return counts, md + note


# ══════════════════════════════════════════════════════════════════════════════
# 3. ownership_scan
# ══════════════════════════════════════════════════════════════════════════════

def ownership_scan(df: pd.DataFrame, label: str) -> str:
    """
    Surface the current immediate owner (Owner(s)) for each unit in the slice,
    and flag units where the owner field is blank so Claude can search for it.

    The scan outputs a structured table: unit ID, plant, unit name, status,
    current Owner(s), and a research prompt for each unit.

    This is purely a surface-and-search prompt — it does not attempt to fetch
    live ownership data. Claude runs web searches after receiving this output.

    Parameters
    ----------
    df    : DataFrame slice (already filtered to country/state + status)
    label : human-readable scope label

    Returns
    -------
    str  markdown output
    """
    uid_col    = _col(df, COL_UNIT_ID)
    plant_col  = _col(df, COL_PLANT)
    unit_col   = _col(df, COL_UNIT)
    status_col = _col(df, COL_STATUS)
    owner_col  = _col(df, COL_OWNER)
    parent_col = _col(df, COL_PARENT)

    if df.empty:
        return f"## OWNERSHIP SCAN — {label}\n\nNo units found in scope."

    lines = [f"## OWNERSHIP SCAN — {label}",
             f"Units in scope: {len(df)}\n",
             "For each unit below, search: \"[plant name] owner / acquired / sold / stake / developer [current year]\"",
             "Apply the rule: CLOSED change → 🔄 UPDATE to Owner(s); UPCOMING change → ⏳ IN PROGRESS in Section 6g.\n",
             f"{'GEM unit ID':<20} {'Plant name':<35} {'Status':<18} {'Current Owner(s)':<35} {'Parent(s)'}",
             "-" * 130]

    for _, row in df.iterrows():
        uid    = _get(row, uid_col)    if uid_col    else ""
        plant  = _get(row, plant_col)  if plant_col  else ""
        unit   = _get(row, unit_col)   if unit_col   else ""
        status = _get(row, status_col) if status_col else ""
        owner  = _get(row, owner_col)  if owner_col  else ""
        parent = _get(row, parent_col) if parent_col else ""

        owner_display  = owner  if owner  else "(BLANK — search required)"
        parent_display = parent if parent else ""

        plant_unit = f"{plant} / {unit}" if unit else plant
        lines.append(
            f"{uid:<20} {plant_unit[:35]:<35} {status[:18]:<18} {owner_display[:35]:<35} {parent_display}"
        )

    lines.append(
        "\nReminder: Owner(s) = immediate owner only — NOT the parent company. "
        "A parent-level-only change is NOT an Owner(s) update."
    )
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# 4. in_progress_scan
# ══════════════════════════════════════════════════════════════════════════════

# Status groups that commonly have time-sensitive changes in an update window
_IN_PROGRESS_STATUS_TRIGGERS = {
    # construction units due online this year → commissioning pending
    "construction":     "Due online this year? Confirm commissioning or flag delay.",
    # pre-construction with groundbreaking expected
    "pre-construction": "Groundbreaking expected this year? Confirm or flag delay.",
    # announced units that may have progressed
    "announced":        "Any status change since last research? Check for permits or groundbreaking.",
    # operating units with a retirement year in the current/next year
    "operating":        "Planned retirement this year or next? Confirm or flag delay.",
    # mothballed — restart may be imminent
    "mothballed":       "Restart announced or under negotiation? Confirm or flag.",
    # shelved — may be approaching cancellation threshold or revival
    "shelved":          "Revival in progress? Or approaching 4-year cancellation threshold?",
    "shelved - inferred 2y": "Approaching 4-year cancellation threshold?",
}

def in_progress_scan(df: pd.DataFrame, label: str) -> str:
    """
    Identify units likely to have a status/ownership change within the current
    update window (H1 of the year) that has not yet occurred.

    Heuristics used:
    - Construction units (may commission this year)
    - Pre-construction units (groundbreaking expected)
    - Operating units with Planned retire = current year or year+1
    - Mothballed units (restart possible)
    - Shelved units near the 4-year cancellation threshold
    - Announced units with no recent activity signal

    This scan surfaces candidates for Claude to confirm via web search.
    Units whose change has already occurred should be flagged 🔄 instead.

    Returns
    -------
    str  markdown output
    """
    import datetime
    current_year = datetime.datetime.now().year

    uid_col    = _col(df, COL_UNIT_ID)
    plant_col  = _col(df, COL_PLANT)
    unit_col   = _col(df, COL_UNIT)
    status_col = _col(df, COL_STATUS)
    ret_col    = _col(df, COL_RET_YEAR)
    start_col  = _col(df, COL_START_YEAR)

    if df.empty:
        return f"## IN-PROGRESS SCAN — {label}\n\nNo units found in scope."

    candidates = []

    for _, row in df.iterrows():
        status = _get(row, status_col).lower() if status_col else ""
        uid    = _get(row, uid_col)   if uid_col    else ""
        plant  = _get(row, plant_col) if plant_col  else ""
        unit   = _get(row, unit_col)  if unit_col   else ""
        ret    = _get(row, ret_col)   if ret_col    else ""
        start  = _get(row, start_col) if start_col  else ""

        reason = None

        # Construction: start year = this year or already past (may have commissioned)
        if status == "construction":
            yr = _to_float(start)
            if yr and yr <= current_year:
                reason = f"Start year {int(yr)} — may have commissioned. Confirm or flag delay."
            else:
                reason = _IN_PROGRESS_STATUS_TRIGGERS.get(status, "")

        # Pre-construction: start year this year or next
        elif status == "pre-construction":
            yr = _to_float(start)
            if yr and yr <= current_year + 1:
                reason = f"Start year {int(yr)} — groundbreaking may be imminent. Confirm or flag delay."
            else:
                reason = _IN_PROGRESS_STATUS_TRIGGERS.get(status, "")

        # Operating: planned retirement this year or next
        elif status == "operating":
            yr = _to_float(ret)
            if yr and yr <= current_year + 1:
                reason = f"Planned retire {int(yr)} — confirm retirement or flag delay."

        # Mothballed, shelved
        elif status in _IN_PROGRESS_STATUS_TRIGGERS:
            reason = _IN_PROGRESS_STATUS_TRIGGERS[status]

        # Announced with a start year that has passed
        elif status == "announced":
            yr = _to_float(start)
            if yr and yr < current_year:
                reason = f"Start year {int(yr)} has passed — status update likely needed."
            else:
                reason = _IN_PROGRESS_STATUS_TRIGGERS.get(status, "")

        if reason:
            plant_unit = f"{plant} / {unit}" if unit else plant
            candidates.append((uid, plant_unit, _get(row, status_col) if status_col else status, reason))

    if not candidates:
        return (
            f"## IN-PROGRESS SCAN — {label}\n\n"
            "No in-progress candidates identified by heuristic scan.\n"
            "Manually verify construction units and any units with planned retirement "
            "in the current year."
        )

    lines = [f"## IN-PROGRESS SCAN — {label}",
             f"Candidates: {len(candidates)}\n",
             "For each: verify via web search. If the change has ALREADY OCCURRED → 🔄 UPDATE.",
             "If not yet closed → ⏳ IN PROGRESS block in Section 6g (re-check before publish).\n",
             f"{'GEM unit ID':<20} {'Plant / Unit':<40} {'Status':<22} Reason",
             "-" * 130]

    for uid, plant_unit, status, reason in candidates:
        lines.append(f"{uid:<20} {plant_unit[:40]:<40} {status[:22]:<22} {reason}")

    lines.append(
        "\nReminder: ⏳ IN PROGRESS means the current DB value is CORRECT NOW — "
        "a change is expected this window but has not yet occurred.\n"
        "Convert to 🔄 UPDATE only once the change has actually happened."
    )
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# 5. duplicate_scan
# ══════════════════════════════════════════════════════════════════════════════

def duplicate_scan(df: pd.DataFrame, label: str) -> str:
    """
    Flag candidate duplicate plant entries within the country/state.

    A candidate pair is flagged when two or more of the following signals match
    between two different GEM location IDs:

        STRONG (each alone can flag a pair):
        - Coordinates within ~1 km (lat/lon difference < 0.01°)

        COMBINED (two required):
        - Capacity within 20 MW  (or both blank)
        - Owner(s) overlap (at least one common token ≥ 4 chars)
        - Plant name fuzzy match (≥ 50% token overlap after lowercasing)

    The scan also looks for the announce-then-refine pattern:
        - One entry has "approximate" location accuracy and the other "exact"
        - One entry has a generic/numbered name pattern
          (e.g. "power station 4", "CCGT unit A", "IRP plant")

    All candidate pairs are returned for Claude to confirm by hand — the scan
    NEVER auto-flags; it just surfaces pairs worth reviewing.

    Parameters
    ----------
    df    : FULL country/state DataFrame (all statuses)
    label : human-readable scope label

    Returns
    -------
    str  markdown output
    """
    if df.empty:
        return f"## DUPLICATE SCAN — {label}\n\nNo units found in scope."

    # Collapse to location level (one row per GEM location ID)
    loc_col    = _col(df, COL_LOC_ID)
    plant_col  = _col(df, COL_PLANT)
    cap_col    = _col(df, COL_CAPACITY)
    owner_col  = _col(df, COL_OWNER)
    lat_col    = _col(df, COL_COORDS_LAT)
    lon_col    = _col(df, COL_COORDS_LON)
    acc_col    = _col(df, COL_LOC_ACC)
    status_col = _col(df, COL_STATUS)

    # Build a per-location summary (aggregate unit statuses)
    def first_nonempty(series):
        vals = [v for v in series if str(v).strip() and str(v).lower() != "nan"]
        return vals[0] if vals else ""

    if loc_col:
        locs = (
            df.groupby(loc_col, sort=False)
            .agg(
                plant    = (plant_col  if plant_col  else loc_col, first_nonempty),
                capacity = (cap_col    if cap_col    else loc_col, first_nonempty),
                owner    = (owner_col  if owner_col  else loc_col, first_nonempty),
                lat      = (lat_col    if lat_col    else loc_col, first_nonempty),
                lon      = (lon_col    if lon_col    else loc_col, first_nonempty),
                acc      = (acc_col    if acc_col    else loc_col, first_nonempty),
                statuses = (status_col if status_col else loc_col,
                            lambda x: " | ".join(sorted(set(str(v) for v in x if str(v).strip())))),
            )
            .reset_index()
        )
        id_col_name = loc_col
    else:
        # Fallback: treat each row as its own location
        uid_col = _col(df, COL_UNIT_ID)
        locs = df.copy()
        locs["plant"]    = df[plant_col]  if plant_col  else ""
        locs["capacity"] = df[cap_col]    if cap_col    else ""
        locs["owner"]    = df[owner_col]  if owner_col  else ""
        locs["lat"]      = df[lat_col]    if lat_col    else ""
        locs["lon"]      = df[lon_col]    if lon_col    else ""
        locs["acc"]      = df[acc_col]    if acc_col    else ""
        locs["statuses"] = df[status_col] if status_col else ""
        id_col_name = uid_col or "index"

    records = locs.to_dict("records")

    def _tokens(s: str) -> set:
        return {t.lower() for t in re.split(r"[\s\-_/]+", s) if len(t) >= 4}

    def _token_overlap(a: str, b: str) -> float:
        ta, tb = _tokens(a), _tokens(b)
        if not ta or not tb:
            return 0.0
        return len(ta & tb) / max(len(ta), len(tb))

    _GENERIC_PATTERN = re.compile(
        r"(power station|plant|unit|ccgt|gt|peaker|peaking|irp|unnamed)\s*\d*[a-z]?\s*$",
        re.IGNORECASE,
    )

    def _signals(a: dict, b: dict) -> list[str]:
        sigs = []

        # Coordinate proximity
        try:
            la, lo_a = float(a["lat"]), float(a["lon"])
            lb, lo_b = float(b["lat"]), float(b["lon"])
            if abs(la - lb) < 0.01 and abs(lo_a - lo_b) < 0.01:
                sigs.append(f"coords ~{abs(la-lb)*111:.1f} km apart")
        except (ValueError, TypeError):
            pass

        # Capacity within 20 MW
        ca, cb = _to_float(str(a["capacity"])), _to_float(str(b["capacity"]))
        if ca and cb and abs(ca - cb) <= 20:
            sigs.append(f"capacity {ca} vs {cb} MW (within 20 MW)")
        elif not ca and not cb:
            sigs.append("capacity both blank")

        # Owner overlap
        ov = _token_overlap(str(a["owner"]), str(b["owner"]))
        if ov >= 0.5:
            sigs.append(f"owner overlap {ov:.0%}")

        # Plant name fuzzy match
        nv = _token_overlap(str(a["plant"]), str(b["plant"]))
        if nv >= 0.5:
            sigs.append(f"name overlap {nv:.0%}")

        # Announce-then-refine: one approx + one exact location
        acc_a = str(a.get("acc", "")).lower()
        acc_b = str(b.get("acc", "")).lower()
        if ("approx" in acc_a and "exact" in acc_b) or ("exact" in acc_a and "approx" in acc_b):
            sigs.append("⟵ announce-then-refine? (one approx + one exact location)")

        # Generic name pattern
        if _GENERIC_PATTERN.search(str(a["plant"])) or _GENERIC_PATTERN.search(str(b["plant"])):
            sigs.append("⟵ announce-then-refine? (generic/numbered plant name)")

        return sigs

    candidates = []
    seen = set()

    for i, a in enumerate(records):
        for j, b in enumerate(records):
            if j <= i:
                continue
            pair_key = (str(a.get(id_col_name, i)), str(b.get(id_col_name, j)))
            if pair_key in seen:
                continue

            sigs = _signals(a, b)

            # Flag if: coordinate signal present (strong), OR ≥ 2 other signals
            coord_sig = any("coord" in s for s in sigs)
            strong    = coord_sig or len(sigs) >= 2

            if strong:
                seen.add(pair_key)
                seen.add((pair_key[1], pair_key[0]))
                candidates.append((a, b, sigs))

    if not candidates:
        return (
            f"## DUPLICATE SCAN — {label}\n\n"
            f"No duplicate candidates identified among {len(records)} location(s) in scope.\n"
            "Note: the scan requires coordinate data or two co-occurring signals "
            "(capacity, owner, name). If coordinates are missing, some duplicates may not surface."
        )

    lines = [f"## DUPLICATE SCAN — {label}",
             f"Candidate pairs: {len(candidates)}\n",
             "Confirm EACH pair by hand before writing a ⚠️ CHECK — possible duplicate block.",
             "The scan never auto-flags. Dismissed candidates need no flag.\n"]

    for idx, (a, b, sigs) in enumerate(candidates, 1):
        id_a = str(a.get(id_col_name, "?"))
        id_b = str(b.get(id_col_name, "?"))
        pl_a = str(a.get("plant", ""))
        pl_b = str(b.get("plant", ""))
        st_a = str(a.get("statuses", ""))
        st_b = str(b.get("statuses", ""))
        ca   = str(a.get("capacity", ""))
        cb   = str(b.get("capacity", ""))
        ow_a = str(a.get("owner", ""))
        ow_b = str(b.get("owner", ""))

        lines += [
            f"--- Pair {idx} ---",
            f"  Plant A: {id_a} — {pl_a}  [{st_a}]  cap={ca} MW  owner={ow_a}",
            f"  Plant B: {id_b} — {pl_b}  [{st_b}]  cap={cb} MW  owner={ow_b}",
            f"  Signals: {'; '.join(sigs)}",
            f"  → Confirm same plant? Which location ID to keep?",
            "",
        ]

    lines.append(
        "Output format for confirmed duplicates (Section 6g):\n"
        "⚠️ CHECK — possible duplicate\n"
        "Plant A: [location ID] — [Plant Name] — [status]\n"
        "Plant B: [location ID] — [Plant Name] — [status]\n"
        "Matched on: [signals]\n"
        "Assessment: [same plant? announce-then-refine?]\n"
        "Recommended action: [merge B into A, keep location ID … / no action — distinct]\n"
        "Source: [URL]"
    )
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# Self-test (run with: python3 gogpt_checks.py --test)
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if "--test" not in sys.argv:
        print("Usage: python3 gogpt_checks.py --test")
        sys.exit(0)

    print("=== Running gogpt_checks.py self-test ===\n")

    # count_card_flags
    sample_card = (
        "🆕 NEW PROPOSAL\nPlant: Acme Gas\n\n"
        "📋 MONITOR — CAPACITY UNDISCLOSED\nPlant: TBD Plant\n\n"
        "🔄 UPDATE\nUnit: 123 — Plant A\n\n"
        "🔄 UPDATE\nUnit: 456 — Plant B\n\n"
        "⚠️ CHECK\nUnit: 789 — Plant C\n\n"
        "⚠️ CHECK — possible duplicate\nPlant A vs Plant D\n\n"
        "⚙️ TURBINE\nUnit: 111 — Plant E\n\n"
        "⏳ IN PROGRESS\nUnit: 222 — Plant F\n\n"
        "✅ No changes\n"
    )
    counts, md = count_card_flags(sample_card)
    print("count_card_flags:")
    print(md)
    assert counts["new_proposals"]  == 1, f"Expected 1, got {counts['new_proposals']}"
    assert counts["monitor"]        == 1, f"Expected 1, got {counts['monitor']}"
    assert counts["updates"]        == 2, f"Expected 2, got {counts['updates']}"
    assert counts["checks"]         >= 2, f"Expected >=2, got {counts['checks']}"
    assert counts["turbine"]        == 1
    assert counts["in_progress"]    == 1
    assert counts["no_changes"]     == 1
    print("count_card_flags: PASSED\n")

    # ownership_scan, in_progress_scan, duplicate_scan with minimal DataFrame
    import datetime
    cy = datetime.datetime.now().year

    data = {
        "GEM unit ID":    ["U001",    "U002",    "U003",    "U004"],
        "GEM location ID":["L001",    "L002",    "L003",    "L004"],
        "Plant name":     ["Alpha",   "Beta",    "Alpha",   "Gamma"],
        "Unit name":      ["Unit 1",  "Unit 1",  "Unit 2",  "Unit 1"],
        "Status":         ["Construction", "Operating", "Construction", "Announced"],
        "Capacity (MW)":  ["100",     "200",     "105",     ""],
        "Owner(s)":       ["Acme",    "Beta Co", "Acme",    ""],
        "Parent(s)":      ["Acme Parent", "", "", ""],
        "Planned retire": ["",        str(cy),   "",        ""],
        "Start year":     [str(cy),   "",        str(cy),   str(cy-1)],
        "Latitude":       ["10.001",  "20.0",    "10.002",  "30.0"],
        "Longitude":      ["50.001",  "60.0",    "50.002",  "70.0"],
        "Location accuracy": ["approximate", "exact", "exact", "exact"],
    }
    df_test = pd.DataFrame(data)

    print("ownership_scan:")
    print(ownership_scan(df_test, "Test Country"))
    print()

    print("in_progress_scan:")
    print(in_progress_scan(df_test, "Test Country"))
    print()

    print("duplicate_scan:")
    print(duplicate_scan(df_test, "Test Country"))
    print()

    print("=== All tests PASSED ===")
