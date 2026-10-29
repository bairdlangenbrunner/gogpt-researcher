#!/usr/bin/env python3
"""
Gate a US state batch before the deliverable is built. Read-only: it reports,
it never edits a shard or a staged file.

Contract: the Gate table in notes/us_state_agent_plan.md. Run after
assemble_state.py; it must print GATE CLEAN (exit 0) before
build_review_package.py.

    python state_gate.py --batch ../batches/us-md [--csv ...] \
        [--entity-check] [--entity-csv gem_export_gogpt.csv] [--no-qc] [--json]

Hard gates (any failure exits 1)
  coverage    every plant in briefs/_index.json has shards/<L...>.json that
              parses, has meta.done true, and reports every unit ID the index
              lists for it (a unit missing from the shard is silent loss)
  banned      no gem.wiki, globalenergymonitor.org or abarrelfull anywhere in
              any record's refs or verifications, any lane, case-insensitive.
              GEM-derived republishers cannot be detected mechanically; the
              reviewer still owns that check.
  verified    updates / newunits / newplants: every URL in refs has a
              verification with ok true. contains_value false is accepted only
              when researcher_notes is non-empty (the researcher explained the
              inference). Spreadsheet citations (URL ending .xlsx / .xls / .zip,
              or host eia.gov: EIA-860M, 860 and 923 files the verifier cannot
              text-match) are accepted when ok is true and researcher_notes is
              non-empty (the note quotes the matching row); they are listed on
              an informational line "spreadsheet citations confirmed by hand".
  orphans     every fields column has >=1 URL under its Data Source column
              (build_review_package.ref_col_for), and every refs key pairs with
              a fields column. Exempt: a delete record only. An inferred status
              needs its Status Data Source like any value: the Latest Activity
              source, with the milestone year equal to the Latest Activity date
              plus 2 (shelved) or 4 (cancelled) years (manual M621, M637; the
              year itself is not checked mechanically, see the TODO in
              gate_orphans). Status Detail is its own source column: its
              links sit under "Status Detail" and each must appear in the
              text of the value (Baird 2026-10-08).
  fresh       every current[header] (and sibling_current[unit]) equals the
              export's cell for that unit, whitespace-normalized; a mismatch
              means the export changed after the shards were built
  headers     every fields key is an export header and not a read-only column
              (schema_constants.READ_ONLY_COLUMNS)
  cell-prose  a value holds a value: no "http", at most 120 characters, no
              sentence break (a lowercase word, a period, a space, a capital).
              Exempt columns: Status Detail, Latest Activity, Notes, Captive*,
              Equipment Manufacturer/Model.
  latest-activity
              a Latest Activity edit is only for a unit that is in development,
              shelved, or carries an inferred status (the export's Status, or
              the Status in the same batch), and its date is at least a year
              before today. A newer date means the project is moving and the
              field is not needed (docs/reference/lifecycle_rules.md).
  additive    Status Detail and Notes are running logs, newest entry first
              (Baird 2026-10-07): a staged value must end with the text the
              box already holds (whitespace-normalized), on this unit and on
              every sibling unit of a plant-wide edit, and a delete record may
              never name either column. assemble_state.py composes the value
              with build_review_package.additive_value.
  location    the location step (docs/reference/location.md): a record that
              stages Latitude, Longitude or Location accuracy with a
              location_method stages all three together, applies to every
              unit of the plant, holds a valid point, names a method from the
              list (schema_constants.LOCATION_METHODS: address, site_reference,
              dataset, map, imagery, published), sits inside its US state's
              bounding box (geo.US_STATE_BBOX; a country scope has no offline
              box, so the review card's satellite panel is the check), writes
              an exact point with at least three decimals, and for a map
              method carries at least two control points, a fit error under
              150 m and an existing render file. An exact point rests on one
              of the manual's five routes (coordinates or a map published by a
              government body, owner or operator; coordinates in a permit or
              similar document; a map on the owner's or operator's site;
              Wikimapia or OpenStreetMap; Google Maps naming the project) or
              on the satellite look or a named parcel: method `published` or
              `imagery`, or `dataset` or `site_reference` with a
              `location_route` that names the publisher; an address or map
              method needs a note that says it was seen in imagery or placed
              on a named parcel. Place fields (City, Local area, Major area,
              Subnational) on an exact plant are allowed. Older per-field
              coordinate records (one column each, no method) only need to
              cover all three columns between them for the plant.
  validation  every item of the database's validation report has an answer
              (checklist row 7; the user's standing rule, 2026-10-16): each
              brief task carrying check 7, and each fix or person item in the
              current work/validation_<tag>.json, needs a record in any lane
              for that unit (or a sibling) carrying check 7, or for a
              whole-plant item a record on that plant. A finding that nothing
              was found is a qa record with concern_type validation. An item
              is optional under the manual (M198, M220) when the plant also
              has coal units in the unfiltered export, or the unit is a coal
              conversion; a record on that plant or unit whose text says
              "optional under the manual" answers it. The
              validation file must exist and be under a day old (rerun
              validation_report.py; --allow-stale-validation downgrades the age
              check), so an item that appeared after the briefs were built is
              still caught. Update mode only.
  access      every source_log entry an agent gave up on (outcome blocked or
              dead) was retried by `access_audit.py <batch> --retry`, which
              writes <batch>/access_retry.json, and still fails; one that
              loads now must be read and used. No source_log note, whatever
              its outcome, may give a search form, a script, a session or
              paging as the reason a page was not read: those never stop a
              person (Baird 2026-10-19, after the Iowa air permit pages were
              skipped as "a search form that needs a script").
  statewide-coverage
              every statewide source in docs/coverage/<scope>.json (a state
              batch must have that list) has an entry in
              <batch>/coverage.json: status "searched" with `how` (script
              name or pages read) and `found` (what turned up, or that nothing
              did), or status "blocked" with an `access` note that records the
              fetch.py and Wayback tries. "not searched", "skipped", an empty
              entry, a missing id, or a form, script or paging given as the
              reason all fail. (Named statewide-coverage because the first
              gate above already uses the name coverage.)
  data-centers
              every site in work/permits/<tag>/_data_centers.json (written by
              data_center_fleets.py) with verdict at_threshold,
              unknown_capacity or in_gem has an entry under `data_centers` in
              <batch>/coverage.json, keyed by site_id, with a valid decision:
              add (names a record_id that exists in the newplants or newunits
              lane), already_in_gem or update (names a plant_id or a
              record_id), below_threshold or no_generators (never for an
              at_threshold or unknown_capacity site). A missing file is a
              warning, not a failure (backup engine fleets are plants at the
              summed nameplate threshold, Baird 2026-10-27).
  chase       no staged record, in any lane, may say a thing was noticed in
              passing, not researched, not checked, outside this pass or left
              for later (researcher_notes, action, note, recommendation,
              monitor_reason, question, review_note, and the `how` and `found`
              text of coverage.json). "backup only", "emergency generators
              only" and the like are flagged unless a summed MW figure sits in
              the same note. If it is worth writing down it is worth
              chasing: research it, then stage it, or say plainly what was
              searched and not found.
  ids_followup
              every EIA plant that match_ids.py lists as missing from GEM
              (50 MW or more; the "leads" in work/ids_us-<st>.json, copied into
              briefs/_index.json as ids_followup by build_state_brief.py --ids)
              needs an answer: a staged record that names its EIA plant ID or
              plant name, or an `ids_followup` entry in coverage.json with
              decision add, below_threshold, out_of_scope or already_in_gem
              and evidence text. Update mode, US states only.
  build       build_review_package.validate() on the lane files: the errors
              that would stop the build anyway (qa records with fields, etc.)
  qc_checks   qc_checks.py --staged on each lane file present must exit 0
              (skipped with --no-qc)

Advisory gates (reported, never fail the run)
  lead-only     a cited link in updates, newunits or newplants on a lead site
                (build_review_package.LEAD_ONLY: cleanview.co,
                interconnection.fyi, gridstatus.io, GridInfo, Wikipedia, the
                Global Energy Observatory, the WRI power plant database). The
                value stays yellow; cite the primary document when one exists
                (Baird 2026-10-23, softened from a hard gate; gem.wiki and
                globalenergymonitor.org stay banned under `banned`).
  false-high    tier high on a Status change (current Status non-blank and
                different) with fewer than two distinct hosts among verified
                Status links
  independence  independent true with fewer than two verified links
  entities      with --entity-check: every proposed Owner(s) / Operator(s)
                name not already in the unit's current cell (share brackets
                stripped) is looked up with entity_lookup.lookup_local over the
                unfiltered export; not-found names are listed. Skipped cleanly
                without the flag or when the lookup cannot run.
  notes         researcher_notes or action containing repo jargon (lane,
                shard, tier, staged, ref, orphan, url_verifier, blue, green,
                yellow and the like) or an em dash, en dash or arrow;
                rewrite per docs/reference/notes_style.md; a location record's
                researcher_notes that names a source must also give its URL;
                any person-facing text (or proposed_add.source_if_accepted)
                that names a file on the researcher's computer (work/,
                batches/, /Users/, a saved .xlsx or .csv) instead of a web
                address or steps anyone can follow
  concern-types a qa record whose concern_type is outside the vocabulary
                (a staged column name or one of review_app/checklist.py
                CONCERN_KINDS); assemble_state.py maps shard text onto it, so
                an offender here is text the mapping did not recognize
  monitor-fields
                a monitor record with no monitor_reason, no recheck_by, a
                recheck_by not of the form YYYY-MM, or a monitor_kind outside
                new_to_tracker / existing_plant
  watch-case    a watch item for a project GEM lacks (monitor_kind
                new_to_tracker, or a lead) names no watch_case from
                schema_constants.WATCH_CASES, or its own values contradict
                the case: under_threshold with a capacity_mw at the scope's
                threshold, unverified with a passing verification
                that states the value. A watch item that says backup,
                emergency or standby generators at a data center with no
                summed MW figure is flagged too: that fleet is an add or a
                below-threshold record, never a watch item (Baird
                2026-10-27). A project that fits no case is an add (Baird
                2026-10-23).
  location-notes
                an exact point whose record names no `location_route`, and a
                move of more than 500 m on a Location record (a flag for the
                reviewer, never a block; Baird 2026-10-27).

Output: one line per gate, `GATE <name> HARD|ADVISORY PASS|FAIL (n)`, then
up to 25 offenders (record_id and reason). Last line: `GATE CLEAN` or
`GATE FAILED: <names>`. --json prints the same result as JSON (exit code
unchanged).
"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from review_app.checklist import CONCERN_VOCAB, MONITOR_KINDS  # noqa: E402
from assemble_state import (  # noqa: E402
    host_of, is_blank, load_export, load_index, norm_entities, norm_status,
    resolve_csv, ws)
from schema_constants import LOCATION_METHODS, STATUSES_IN_DEVELOPMENT  # noqa: E402
from build_review_package import (  # noqa: E402
    URL_RE, additive_errors, is_lead_only, load_lanes, ref_col_for, validate)
from schema_constants import (  # noqa: E402
    ADDITIVE_TEXT_COLUMNS, CAPACITY_THRESHOLD_EU_UK_MW, CAPACITY_THRESHOLD_MW,
    EU_UK_COUNTRIES, READ_ONLY_COLUMNS, WATCH_CASES)
from paths import EXPORT_MAX_AGE_HOURS, gem_export_csv, work_dir  # noqa: E402
from geo import decimals, in_state_box, valid_point  # noqa: E402
from access_audit import EXCUSE, OUTCOMES, RETRY_FILE, gave_up_outcome, unknown_outcome  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
BANNED = ("gem.wiki", "globalenergymonitor.org", "abarrelfull")
VALUE_LANES = ("updates", "newunits", "newplants")
PROSE_OK = {"Status Detail", "Latest Activity", "Notes",
            "Equipment Manufacturer/Model"}
SENTENCE_RE = re.compile(r"(?<![A-Za-z])([a-z]{2,})[.!?]\s+[A-Z]")
ABBREVS = {"inc", "corp", "ltd", "co", "jr", "sr", "st", "mt", "no", "bros"}
JARGON_RE = re.compile(r"\b(lane|shard|tier|staged|stage|ref|refs|orphan|"
                       r"qa record|url_verifier|colmap|merge-never-replace|"
                       r"blue|green|yellow)\b", re.I)
DASH_RE = re.compile(r" — | – |->|→")
SPREADSHEET_EXT = (".xlsx", ".xls", ".zip")
CAP = 25

# Person-facing text a researcher writes on a record.
PROSE_KEYS = ("researcher_notes", "action", "note", "recommendation", "monitor_reason",
              "question", "finding", "review_note")
# A recommendation that hands the decision back instead of giving one (docs/reference/notes_style.md, Questions).
DECIDE_RE = re.compile(r"\b(?:reviewer|PM|someone|team) (?:should|must|will have to|needs? to|can) (?:decide|judge|check|confirm|look|verify)\b"
                       r"|\b(?:should|needs? to|must) be (?:checked|confirmed|verified|decided|reviewed)\b"
                       r"|\b(?:up to|left to|for) the (?:reviewer|PM)\b", re.I)
QUESTION_GENERATED = "2026-10-28"   # batches assembled from this date on must carry question and finding
# A note that says the thing was seen and left alone. Each pattern is a reason a
# reviewer cannot use: the agent should have researched it before writing it down.
CHASE_RE = re.compile("|".join([
    r"\bin passing\b", r"\bpassing (?:observation|note|remark|mention)s?\b",
    r"\b(?:did not|didn't|have not|haven't|was not|were not|wasn't|not been|never been)"
    r"\s+(?:been\s+)?(?:researched|research|checked|check|chased|investigated|investigate|"
    r"followed up|follow up|looked into|look into|pursued|pursue)\b",
    r"\bI (?:did not|didn't|have not|haven't) (?:confirm|verify)\b",
    r"\bnot (?:yet )?(?:researched|checked|chased|investigated|followed up)\b",
    r"\b(?:outside|beyond) (?:of )?(?:the |this |my )?(?:scope|tasks?|brief|pass|check|request)\b",
    r"\bout of scope\b",
    r"\bnot (?:a |part of (?:the |this )?)(?:task|check|brief|pass|request|assignment)\b",
    r"\bwas not (?:a )?task for\b",
    r"\bnot asked (?:for|about)\b",
    r"\b(?:for|until) (?:a )?later\b", r"\blater pass\b", r"\bsecond look\b",
    r"\bworth (?:a )?(?:closer|further|second) (?:look|check|research)\b",
    r"\b(?:needs?|requires?|deserves?) (?:a )?(?:further|more|closer) (?:research|checking|work|review|look)\b",
    r"\bshould be (?:checked|researched|looked at|followed up|investigated)\b",
    r"^\s*(?:left unchanged|no change|unchanged|noted|see above)\.?\s*$",
]), re.I)
DECISIONS = ("add", "below_threshold", "out_of_scope", "already_in_gem")


def rid_of(rec, lane, i):
    return rec.get("record_id") or f"{lane}[{i}]:{rec.get('gem_unit_id', '')}"


def iter_records(lanes, names=None):
    """Yield (lane, record_id, record) including newplants' unit sub-records."""
    for lane, recs in lanes.items():
        if names and lane not in names:
            continue
        for i, rec in enumerate(recs):
            rid = rid_of(rec, lane, i)
            yield lane, rid, rec
            for j, u in enumerate(rec.get("units") or []):
                yield lane, f"{rid}/unit[{j}]", u


def ref_urls(rec):
    refs = rec.get("refs") or {}
    if isinstance(refs, list):
        return [u for u in refs if ws(u)]
    return [u for us in refs.values() for u in (us or []) if ws(u)]


def is_spreadsheet(url):
    path = url.split("?", 1)[0].split("#", 1)[0].lower()
    return path.endswith(SPREADSHEET_EXT) or host_of(url).endswith("eia.gov")


def ok_urls(rec):
    return {v.get("url") for v in rec.get("verifications") or [] if v.get("ok")}


# ------------------------------------------------------------------ gates ---

def gate_coverage(batch, index):
    out = []
    for p in index["plants"]:
        pid = p["plant_id"]
        sp = batch / "shards" / f"{pid}.json"
        if not sp.exists():
            out.append((pid, "no shard file"))
            continue
        try:
            shard = json.loads(sp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            out.append((pid, f"shard does not parse: {e}"))
            continue
        if (shard.get("meta") or {}).get("done") is not True:
            out.append((pid, "shard not marked done"))
        reported = {u.get("gem_unit_id") for u in shard.get("units") or []}
        for uid in p["unit_ids"]:
            if uid not in reported:
                out.append((pid, f"unit {uid} not reported in the shard"))
    return out


def saved_copy_cited(shard, url):
    """True when the shard cites a Wayback snapshot of this address as verified."""
    path = url.split("://", 1)[-1]
    return any(isinstance(x, dict) and x.get("outcome") == "verified"
               and "web.archive.org/web/" in (x.get("url") or "") and path in x["url"]
               for x in shard.get("source_log") or [])


def gate_access(batch):
    """Pages the research agents gave up on: each must be retried with the
    current fetch ladder and still fail, and none may have been given up on
    because of a form, a script or paging."""
    out, info = [], []
    try:
        retried = json.loads((batch / RETRY_FILE).read_text(encoding="utf-8"))
    except (ValueError, OSError):
        retried = {}
    gave_up = still = 0
    for sp in sorted((batch / "shards").glob("*.json")):
        try:
            shard = json.loads(sp.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        for e in shard.get("source_log") or []:
            if not isinstance(e, dict) or not e.get("url"):
                continue
            url, note = e["url"], e.get("note") or ""
            where = f"{sp.stem}: {url[:90]}"
            if e.get("outcome") != "verified" and EXCUSE.search(note):
                out.append((where, "the note gives a form, a script or paging as the reason. "
                                   "Read the page source, find the address the form calls or "
                                   "the per-record links, or use fetch.py's real-Chrome load"))
                continue
            if unknown_outcome(e.get("outcome")):
                out.append((where, f"unknown outcome '{e.get('outcome')}': use one of "
                                   + ", ".join(OUTCOMES)))
                continue
            kind = gave_up_outcome(e.get("outcome"))
            if not kind:
                continue
            gave_up += 1
            r = retried.get(url)
            if r is None:
                out.append((where, f"{kind} but never retried: run "
                                   f"access_audit.py {batch} --retry"))
            elif r.get("ok"):
                out.append((where, f"{kind} in the shard but loads now; read it and use it"))
            else:
                still += 1
                arch = r.get("archive") or {}
                if kind == "dead" and not arch.get("checked"):
                    out.append((where, "dead but no Wayback lookup is recorded: run "
                                       f"access_audit.py {batch} --retry"))
                elif kind == "dead" and arch.get("snapshots") and not saved_copy_cited(shard, url):
                    out.append((where, f"dead, but saved copies exist ({len(arch['snapshots'])}); "
                                       f"the newest is {arch['snapshots'][-1]}. Read them. If one shows the value, "
                                       "add it to source_log as verified with its web.archive.org "
                                       "address, and say in this entry's note what you tried"))
    info.append(f"pages given up on: {gave_up}; retried and still failing: {still}")
    return out, info


def gate_banned(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes):
        strings = list(ref_urls(rec))
        for v in rec.get("verifications") or []:
            strings += [str(x) for x in v.values() if isinstance(x, str)]
        hits = sorted({s for s in strings for b in BANNED if b in s.lower()})
        for h in hits:
            out.append((rid, f"banned source: {h[:120]}"))
    return out


def gate_verified(lanes):
    out, by_hand = [], []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        notes = ws(rec.get("researcher_notes"))
        vers = rec.get("verifications") or []
        for u in ref_urls(rec):
            ok = [v for v in vers if v.get("url") == u and v.get("ok")]
            if not ok:
                out.append((rid, f"no passing verification for {u}"))
                continue
            if is_spreadsheet(u):
                if notes:
                    by_hand.append((rid, u))
                else:
                    out.append((rid, f"spreadsheet link with no note quoting "
                                     f"the matching row: {u}"))
                continue
            if all(v.get("contains_value") is False for v in ok) and not notes:
                out.append((rid, f"page does not state the value and no note "
                                 f"explains the inference: {u}"))
    return out, by_hand


def gate_orphans(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        fields = rec.get("fields") or {}
        refs = rec.get("refs") or {}
        if isinstance(refs, list):
            out.append((rid, "refs is a list, not keyed by Data Source column"))
            continue
        for col, val in fields.items():
            # an inferred status is a milestone entry like any value: it needs the
            # Latest Activity source in Status Data Source (Baird 2026-10-27).
            # TODO: also check the milestone year equals the Latest Activity date
            # plus 2 (shelved) or 4 (cancelled) years (manual M637); the staged
            # record has no field for that year yet, so only the source is required.
            if rec.get("delete"):
                continue
            rc = ref_col_for(col)
            if not [u for u in refs.get(rc) or [] if ws(u)]:
                out.append((rid, f"{col} has a value but no link under {rc}"))
            elif rc == col:
                for u in refs.get(rc) or []:
                    if ws(u) and ws(u) not in str(val):
                        out.append((rid, f"{col} link is not written into the "
                                         f"text: {u}"))
        paired = {ref_col_for(c) for c in fields}
        for rc, urls in refs.items():
            if rc not in paired and urls:
                out.append((rid, f"links under {rc} have no paired value"))
    return out


def gate_fresh(lanes, export):
    out = []
    for lane, rid, rec in iter_records(lanes, ("updates",)):
        uid = rec.get("gem_unit_id")
        cur = rec.get("current") or {}
        checks = [(uid, cur)]
        for sib, val in (rec.get("sibling_current") or {}).items():
            # a location record keeps a dict of its three columns per sibling
            checks += [(sib, dict(val) if isinstance(val, dict) else {h: val for h in cur})]
        for u, values in checks:
            row = export.get(u)
            if row is None:
                out.append((rid, f"unit {u} not in the export"))
                continue
            for h, v in values.items():
                if ws(v) != ws(row.get(h, "")):
                    out.append((rid, f"{u} {h}: record has {ws(v)!r}, export "
                                     f"has {ws(row.get(h, ''))!r}"))
    return out


def gate_headers(lanes, header):
    out, hset = [], set(header)
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        for col in rec.get("fields") or {}:
            if col not in hset:
                out.append((rid, f"{col!r} is not an export header"))
            elif col in READ_ONLY_COLUMNS:
                out.append((rid, f"{col!r} is a read-only column"))
    return out


def prose_reason(col, val):
    if col in PROSE_OK or col.startswith("Captive"):
        return ""
    s = ws(val)
    if "http" in s.lower():
        return "contains a link"
    if len(s) > 120:
        return f"{len(s)} characters long"
    for m in SENTENCE_RE.finditer(s):
        if m.group(1).lower() not in ABBREVS:
            return "reads as a sentence"
    return ""


def gate_cell_prose(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        for col, val in (rec.get("fields") or {}).items():
            why = prose_reason(col, val)
            if why:
                out.append((rid, f"{col} value {why}: {ws(val)[:80]!r}"))
    return out

DATE_RE = re.compile(r"^Year: \d{4}(, Month: \d{1,2}(, Day: \d{1,2})?)?$")
YEAR_COLS = ("Start year", "Retired year", "Cancellation year", "Planned retire")


def gate_dates(lanes):
    """Latest Activity is a date field in GEM (every value in the export reads
    'Year: 2024, Month: 6, Day: 17', month and day optional); the year columns
    hold a four-digit year. Free text in either is a value the web UI cannot take."""
    out = []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        for col, val in (rec.get("fields") or {}).items():
            v = ws(val)
            if not v:
                continue
            if col == "Latest Activity" and not DATE_RE.match(v):
                out.append((rid, f"Latest Activity is a date field; write Year: YYYY, Month: M, Day: D, not {v[:60]!r}"))
            elif col in YEAR_COLS and not re.fullmatch(r"\d{4}", v):
                out.append((rid, f"{col} must be a four-digit year, not {v[:40]!r}"))
    return out


def la_status_ok(status):
    s = ws(status).lower()
    return s in STATUSES_IN_DEVELOPMENT or s.startswith("shelved") or "inferred" in s


def gate_latest_activity(lanes, export, today=None):
    """Latest Activity tracks stalled projects only: units in development,
    shelved, or with an inferred status, and only once the newest report is
    more than a year old (docs/reference/lifecycle_rules.md)."""
    today = today or datetime.date.today()
    cutoff = today - datetime.timedelta(days=365)
    proposed = {}
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        st = (rec.get("fields") or {}).get("Status")
        if st and rec.get("gem_unit_id"):
            proposed.setdefault(rec["gem_unit_id"], []).append(st)
    out = []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        fields = rec.get("fields") or {}
        v = ws(fields.get("Latest Activity"))
        m = DATE_RE.match(v) and re.findall(r"\d+", v)
        if not m:
            continue
        uid = rec.get("gem_unit_id")
        statuses = [fields.get("Status"), (export.get(uid) or {}).get("Status")]
        statuses += proposed.get(uid, [])
        statuses = [s for s in statuses if ws(s)]
        if not any(la_status_ok(s) for s in statuses):
            out.append((rid, "Latest Activity is only for units in development, shelved or "
                             f"with an inferred status; this unit is {ws(statuses[0]) if statuses else 'of unknown status'}"))
            continue
        nums = [int(x) for x in m] + [1, 1]
        try:
            day = datetime.date(nums[0], nums[1], nums[2])
        except ValueError:
            continue
        if day > cutoff:
            out.append((rid, f"Latest Activity {v!r} is less than a year old; the project "
                             "is still moving, so leave the field alone"))
    return out


def gate_additive(lanes):
    """Status Detail and Notes are running logs, newest entry first: a staged
    value is the new text placed above the text already in the box, which
    stays word for word on this unit and on every sibling unit of a plant-wide
    edit. Neither box is ever rewritten or cleared (Baird 2026-10-07)."""
    out = []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        if not any(c in (rec.get("fields") or {}) for c in ADDITIVE_TEXT_COLUMNS):
            continue
        for e in additive_errors(rec, rec, rid):
            out.append((rid, e.split(": ", 1)[1]))
    return out


LOCATION_FIELDS = ("Latitude", "Longitude", "Location accuracy")
SEEN_WORDS = ("imagery", "satellite", "aerial", "parcel", "footprint")
LOCATION_MOVE_EXPLAIN_M = 2000
LOCATION_MOVE_REVIEW_M = 500
LOCATION_FIT_MAX_M = 150


def gate_location(lanes, index, batch):
    """The location step's own checks (docs/reference/location.md)."""
    out = []
    where = index.get("where") or {}
    state = where.get("name", "") if where.get("kind", "state") == "state" else ""
    state = state or index.get("state", "")
    units_of = {p.get("plant_id"): set(p.get("unit_ids") or [])
                for p in index.get("plants") or []}
    legacy = {}
    for lane, rid, rec in iter_records(lanes, ("updates",)):
        fields = rec.get("fields") or {}
        have = [f for f in LOCATION_FIELDS if f in fields]
        if not have or rec.get("verdict") == "match" or rec.get("reverified"):
            continue
        pid = rec.get("gem_plant_id")
        if len(have) < 3 and not rec.get("location_method"):
            legacy.setdefault(pid, set()).update(have)
            continue
        if len(have) < 3:
            out.append((rid, "Latitude, Longitude and Location accuracy are staged "
                             f"together; this record has only {', '.join(have)}"))
            continue
        lat, lon = fields["Latitude"], fields["Longitude"]
        acc = ws(fields["Location accuracy"]).lower()
        note = ws(rec.get("researcher_notes"))
        if not valid_point(lat, lon):
            out.append((rid, f"{lat!r}, {lon!r} is not a valid point"))
            continue
        if acc not in ("exact", "approximate"):
            out.append((rid, f"Location accuracy must be exact or approximate, not {acc!r}"))
        method = rec.get("location_method")
        if acc == "exact":
            if min(decimals(lat), decimals(lon)) < 3:
                out.append((rid, "an exact point needs at least three decimals"))
            route = ws(rec.get("location_route"))
            if method in ("published", "imagery"):
                pass
            elif method in ("dataset", "site_reference"):
                if not route:
                    out.append((rid, f"an exact point from a {method} needs a location_route "
                                     "that names who published the point"))
            elif not any(w in note.lower() for w in SEEN_WORDS):
                out.append((rid, "an exact point needs one of the manual's five routes "
                                 "(location_method published), or a note that says it was "
                                 "seen in satellite imagery or placed on a named parcel"))
        if method not in LOCATION_METHODS:
            out.append((rid, f"location_method {method!r} is not one of "
                             f"{', '.join(LOCATION_METHODS)}"))
        if state and in_state_box(lat, lon, state) is False:
            out.append((rid, f"point {lat}, {lon} lies outside {state}"))
        if method == "map":
            cps = rec.get("location_control_points") or []
            fit = rec.get("location_fit_m")
            img = rec.get("location_image") or ""
            if len(cps) < 2:
                out.append((rid, "a map method needs at least two control points"))
            if not isinstance(fit, (int, float)) or fit >= LOCATION_FIT_MAX_M:
                out.append((rid, f"a map method needs a fit error under {LOCATION_FIT_MAX_M} m, "
                                 f"got {fit!r}"))
            if not img or not (Path(batch) / img).exists():
                out.append((rid, f"the map render {img!r} is missing"))
        if not rec.get("applies_to_all_units"):
            out.append((rid, "a location edit applies to every unit of the plant"))
        covered = {rec.get("gem_unit_id")} | set(rec.get("sibling_unit_ids") or [])
        want = units_of.get(pid) or set()
        if want - covered:
            out.append((rid, "units not covered: " + ", ".join(sorted(want - covered))))
        for u, v in (rec.get("sibling_current") or {}).items():
            if not isinstance(v, dict):
                out.append((rid, f"sibling_current[{u}] must hold the three columns"))
                break
    for pid, have in legacy.items():
        if len(have) < 3:
            missing = [f for f in LOCATION_FIELDS if f not in have]
            out.append((f"{pid}:plant", f"{', '.join(sorted(have))} staged without "
                                        f"{', '.join(missing)}; the three go together"))
    return out


def gate_location_notes(lanes):
    """Advisory location checks: an exact point that names no route, and a move
    of more than 500 m (a flag for the reviewer, never a block; Baird
    2026-10-27)."""
    out = []
    for lane, rid, rec in iter_records(lanes, ("updates",)):
        fields = rec.get("fields") or {}
        if not all(f in fields for f in LOCATION_FIELDS) or rec.get("verdict") == "match" \
                or rec.get("reverified"):
            continue
        if ws(fields.get("Location accuracy")).lower() == "exact" and not ws(rec.get("location_route")):
            out.append((rid, "exact point with no location_route; say which of the manual's "
                             "routes (or the satellite look) placed it"))
        moved = rec.get("location_moved_m")
        if isinstance(moved, (int, float)) and moved > LOCATION_MOVE_REVIEW_M:
            out.append((rid, f"the point moves {moved:.0f} m from GEM's; the reviewer should "
                             "look at both on the map"))
        if isinstance(moved, (int, float)) and moved > LOCATION_MOVE_EXPLAIN_M \
                and len(ws(rec.get("researcher_notes"))) < 40:
            out.append((rid, f"a move of {moved / 1000:.1f} km has no note saying why GEM's "
                             "point was wrong"))
    return out


def gate_build(lanes):
    return [("build", e) for e in validate(lanes)
            if " drops or rewrites the text already in the box" not in e
            and " is never cleared; new text is added above " not in e]


def gate_false_high(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes, ("updates",)):
        fields, cur = rec.get("fields") or {}, rec.get("current") or {}
        if str(rec.get("tier", "")).lower() != "high" or "Status" not in fields:
            continue
        if is_blank(cur.get("Status")) or \
                norm_status(cur["Status"]) == norm_status(fields["Status"]):
            continue
        refs = (rec.get("refs") or {}).get(ref_col_for("Status")) or []
        good = ok_urls(rec)
        hosts = {host_of(u) for u in refs if u in good} - {""}
        if len(hosts) < 2:
            out.append((rid, f"high status change on {len(hosts)} host(s): "
                             f"{sorted(hosts)}"))
    return out


def gate_independence(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes):
        if not rec.get("independent"):
            continue
        good = ok_urls(rec)
        n = len({u for u in ref_urls(rec) if u in good})
        if n < 2:
            out.append((rid, f"independent is true with {n} verified link(s)"))
    return out


def split_names(v):
    return [ws(re.sub(r"[\[(]\s*\d+(?:\.\d+)?\s*%\s*[\])]", "", p))
            for p in ws(v).split(";") if ws(p)]


def gate_entities(lanes, entity_csv):
    """-> (offenders, skip_reason or '')."""
    try:
        from entity_lookup import lookup_local
    except Exception as e:  # pragma: no cover
        return [], f"entity_lookup could not be imported ({e})"
    out, seen = [], set()
    for lane, rid, rec in iter_records(lanes, ("updates",)):
        if rec.get("reverified"):
            continue
        for col in ("Owner(s)", "Operator(s)"):
            val = (rec.get("fields") or {}).get(col)
            if is_blank(val):
                continue
            current = {n for n, _ in norm_entities((rec.get("current") or {})
                                                   .get(col, ""))}
            for name in split_names(val):
                if norm_entities(name)[0][0] in current or name in seen:
                    continue
                seen.add(name)
                try:
                    res = lookup_local(name, csv_path=str(entity_csv))
                except Exception as e:
                    return [], f"lookup failed ({type(e).__name__}: {e})"
                if res.get("result") != "found":
                    out.append((rid, f"{col} name not found in the export: "
                                     f"{name!r}"))
    return out, ""


# a file on the researcher's own computer: a repo or home path, or a saved spreadsheet or data file
# by name. The reviewer cannot open it (Baird 2026-10-27, a PJM queue export cited as work/pjm/...)
LOCAL_PATH_RE = re.compile(r"(?<![\w/.])(?:(?:work|batches|data|upstream|scripts|tmp)/\S+|/Users/\S+|~/\S+|/tmp/\S+)"
                           r"|\b[\w-]+\.(?:xlsx|xls|csv|json|zip|parquet)\b", re.I)


def local_paths(text):
    """The local file names in a piece of person-facing text, web addresses left out."""
    return sorted({m.group(0).rstrip(".,;:)") for m in LOCAL_PATH_RE.finditer(URL_RE.sub("", str(text or "")))})


NAMES_SOURCE_RE = re.compile(r"\b(table|petition|filing|article|permit|press release|report|"
                             r"notice|application|plan|statement|document)\b", re.I)


def gate_notes(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes):
        for key in ("researcher_notes", "action", "question", "finding", "recommendation", "monitor_reason"):
            # an action can quote a Status Detail entry with its link in it
            text = URL_RE.sub("", str(rec.get(key) or ""))
            # a capitalized word followed by another one is a name
            # ("Green Rocks data center", "Blue Ridge"), not repo jargon
            words = sorted({m.group(0).lower() for m in JARGON_RE.finditer(text)
                            if not (m.group(0)[0].isupper()
                                    and re.match(r" [A-Z]", text[m.end():m.end() + 2]))})
            dashes = sorted(set(DASH_RE.findall(text)))
            if words:
                out.append((rid, f"{key} uses repo words: {', '.join(words)}"))
            if dashes:
                out.append((rid, f"{key} uses dashes or arrows: "
                                 f"{' '.join(repr(d) for d in dashes)}"))
        # a location note that names a document must give its link (Baird 2026-10-22)
        notes = str(rec.get("researcher_notes") or "")
        if (rid.endswith((":location", ":location-source")) and NAMES_SOURCE_RE.search(notes)
                and not URL_RE.search(notes)):
            out.append((rid, "researcher_notes names a source but gives no link; "
                             "write each source's URL right after its name"))
        # a file on the researcher's computer is no source for anyone else
        texts = [(k, rec.get(k)) for k in PROSE_KEYS]
        if isinstance(rec.get("proposed_add"), dict):
            texts.append(("proposed_add.source_if_accepted", rec["proposed_add"].get("source_if_accepted")))
        for key, text in texts:
            hits = local_paths(text)
            if hits:
                out.append((rid, f"{key} names a file on this computer: {', '.join(hits)}; "
                                 "give the web address, or the steps that get anyone the same file"))
    return out


NOTE_BLOCK_RE = re.compile(r"^### Unit [^\n]*\((G\d+)\)\n+(?:- [^\n]*\n)*?- Notes \(verbatim\):\n\n```\n([\s\S]*?)\n```", re.M)


def brief_notes(brief_path):
    """{unit id: the database note the plant brief printed} from the Notes and history section."""
    try:
        text = Path(brief_path).read_text(encoding="utf-8")
    except OSError:
        return {}
    tail = text.split("## Notes and history", 1)
    if len(tail) < 2:
        return {}
    body = tail[1].split("\n## ", 1)[0]
    out = {}
    for m in NOTE_BLOCK_RE.finditer(body):
        note = m.group(2).strip()
        out[m.group(1)] = "" if note == "(blank)" else note
    return out


def gate_note_drift(batch, index, export):
    """A database note that changed after the plant brief was built, so the agent never read it
    (Iowa, 2026-10-29: a reviewer tied a placeholder to two named plants in the Notes column
    after the brief printed it blank, and the question on the card answered something else)."""
    out = []
    when = str(index.get("generated") or "")[:10]
    for p in index.get("plants") or []:
        path = p.get("brief_path") or ""
        bp = Path(path) if Path(path).is_absolute() else batch.parent.parent / path
        if not bp.exists():
            bp = batch / "briefs" / f"{p.get('plant_id')}.md"
        for uid, old in brief_notes(bp).items():
            row = export.get(uid)
            if row is None:
                continue
            new = ws(row.get("Notes", ""))
            if ws(old) == new:
                continue
            short = lambda t: (t[:90] + "…") if len(t) > 90 else (t or "(blank)")
            out.append((f"{p.get('plant_id')}:{uid}",
                        f"database note changed since the brief of {when or 'the batch'}: "
                        f"brief printed {short(ws(old))!r}, export has {short(new)!r}; "
                        "the agent never read the new note, so check the questions on this plant against it"))
    return out


def load_lanes_meta(staging_dir):
    """The meta block of each staged lane file (generated date, backfill stamps)."""
    out = {}
    for lane in ("updates", "qa", "monitor", "newunits", "newplants", "entity"):
        p = staging_dir / f"staged_{lane}.json"
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if isinstance(data, dict):
                out[lane] = data.get("meta") or {}
    return out


ABBR_RE = re.compile(r"(?:\b[A-Z]|\b(?:Mr|Mrs|Ms|Dr|St|No|Nos|Inc|Co|Corp|Ltd|LLC|vs|approx|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)|U\.S|U\.K)\.$")


def sentences_of(text):
    """The sentences of a short prose field, split on a period, question or exclamation mark followed
    by a capital. A period after an initial or a common abbreviation (Earl F. Wisdom, No. 3, Inc.)
    does not end a sentence."""
    text = ws(text)
    if not text:
        return []
    out = []
    for piece in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"(])", text):
        if out and ABBR_RE.search(out[-1]):
            out[-1] += " " + piece
        elif piece:
            out.append(piece)
    return out


def question_strict(lanes_meta, flag=False):
    """Missing question or finding fails a batch assembled from QUESTION_GENERATED on, or one whose
    staged_qa meta says the fields were backfilled, or any batch under --strict-questions."""
    if flag:
        return True
    meta = (lanes_meta or {}).get("qa") or {}
    if meta.get("question_fields"):
        return True
    return str(meta.get("generated") or "")[:10] >= QUESTION_GENERATED


def gate_questions(lanes, strict=False):
    """Every qa record reads at a glance (Baird 2026-10-27): a question that ends with a question
    mark, a finding, and a recommendation of at most two sentences that gives an instruction
    rather than handing the call back. Missing question or finding is reported only when strict."""
    out = []
    for lane, rid, rec in iter_records(lanes, {"qa"}):
        q, f, r = ws(rec.get("question")), ws(rec.get("finding")), ws(rec.get("recommendation"))
        if not q:
            if strict:
                out.append((rid, "no question; write one sentence ending in a question mark"))
        else:
            if not q.endswith("?"):
                out.append((rid, "question does not end with a question mark"))
            if len(q) > 160:
                out.append((rid, f"question is {len(q)} characters; keep it under about 120"))
            if len(sentences_of(q)) > 1:
                out.append((rid, "question is more than one sentence"))
        if not f:
            if strict:
                out.append((rid, "no finding; say in one to three sentences what the sources say"))
        elif len(sentences_of(f)) > 3:
            out.append((rid, f"finding runs to {len(sentences_of(f))} sentences; keep it to three"))
        if not r:
            out.append((rid, "no recommendation; say what to do"))
            continue
        n = len(sentences_of(r))
        if n > 2:
            out.append((rid, f"recommendation runs to {n} sentences; keep it to two"))
        m = DECIDE_RE.search(r) or CHASE_RE.search(r)
        if m:
            out.append((rid, f"recommendation hands the call back ('{m.group(0)}'); give an instruction: leave as is, change, merge, cancel, or ask the PM a specific question"))
    return out


def gate_concern_types(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes, ("qa",)):
        ct = ws(rec.get("concern_type"))
        if ct not in CONCERN_VOCAB:
            out.append((rid, f"concern_type {ct!r} is outside the vocabulary"
                             + (f" (shard wrote {rec['concern_type_raw']!r})"
                                if rec.get("concern_type_raw") else "")))
    return out


def gate_monitor_fields(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes, ("monitor",)):
        if not ws(rec.get("monitor_reason")):
            out.append((rid, "monitor_reason is empty"))
        rb = ws(rec.get("recheck_by"))
        if not rb:
            out.append((rid, "recheck_by is empty"))
        elif not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", rb):
            out.append((rid, f"recheck_by {rb!r} is not YYYY-MM"))
        if rec.get("monitor_kind") not in MONITOR_KINDS:
            out.append((rid, f"monitor_kind {rec.get('monitor_kind')!r} is not one of "
                             f"{' / '.join(MONITOR_KINDS)}"))
    return out


def scope_threshold_mw(index):
    """The add threshold for the batch's country: 20 MW in the EU and UK, 50
    elsewhere (schema_constants)."""
    w = index.get("where") or {}
    country = w.get("country") or index.get("country") or ""
    return (CAPACITY_THRESHOLD_EU_UK_MW if country in EU_UK_COUNTRIES
            else CAPACITY_THRESHOLD_MW)


DATA_CENTER_RE = re.compile(r"\bdata\s*cent(?:er|re)s?\b", re.I)
BACKUP_GEN_RE = re.compile(r"\b(?:backup|back-up|emergency|standby)\b[^.;]{0,40}?"
                           r"\b(?:generators?|gensets?|engines?|diesel)\b", re.I)
MW_FIGURE_RE = re.compile(r"\d[\d,]*(?:\.\d+)?\s*(?:MWe?|megawatts?)\b", re.I)


def backup_fleet_without_sum(text):
    """True when the text puts backup, emergency or standby generators at a data
    center and gives no MW figure."""
    t = URL_RE.sub("", str(text or ""))
    return bool(DATA_CENTER_RE.search(t) and BACKUP_GEN_RE.search(t) and not MW_FIGURE_RE.search(t))


def gate_watch_case(lanes, index):
    """A watch item for a project GEM lacks names the one reason it is not an
    add (schema_constants.WATCH_CASES, Baird 2026-10-23), and its own values
    do not contradict the reason: an under_threshold case whose capacity_mw
    reaches the threshold, or an unverified case with a passing verification,
    is an add that was held back."""
    out = []
    thr = scope_threshold_mw(index)
    cases = " / ".join(WATCH_CASES)
    for lane, rid, rec in iter_records(lanes, ("monitor",)):
        if rec.get("monitor_kind") != "new_to_tracker" and not rec.get("lead_for"):
            continue
        text = " ".join(str(rec.get(k) or "") for k in PROSE_KEYS + ("item", "watch_case"))
        if backup_fleet_without_sum(text):
            out.append((rid, "backup, emergency or standby generators at a data center are "
                             "a plant at their summed nameplate (an add, or a below-threshold "
                             "record with the sum), never a watch item"))
            continue
        case = rec.get("watch_case")
        if case not in WATCH_CASES:
            out.append((rid, "names no watch_case; a project GEM lacks is added unless one "
                             f"of these applies: {cases}"))
            continue
        cap = rec.get("capacity_mw")
        try:
            cap = float(cap) if cap not in (None, "") else None
        except (TypeError, ValueError):
            cap = None
        if case == "under_threshold" and cap is not None and cap >= thr:
            out.append((rid, f"watch_case under_threshold but capacity_mw {cap:g} reaches the "
                             f"{thr} MW threshold; stage it as a new plant or unit"))
        # a link that only confirms the project exists (a queue page with no size or fuel) leaves
        # it unverified; one that states the value is enough to stage it
        if case == "unverified" and any(v.get("ok") and v.get("contains_value", True)
                                        for v in rec.get("verifications") or [] if isinstance(v, dict)):
            out.append((rid, "watch_case unverified but a source passed the verifier; stage "
                             "it as a new plant or unit, or name the real case"))
    return out


def validation_file(index):
    w = index.get("where") or {}
    slug = w.get("slug") or (index.get("state") or "").lower().replace(" ", "-")
    tag = f"us-{slug}" if (w.get("kind") or "state") == "state" else slug
    return work_dir() / f"validation_{tag}.json"


OPTIONAL_RE = re.compile(r"optional under the manual", re.I)


def coal_plant_ids(csv_path=None):
    """GEM location IDs of plants with at least one coal unit in the unfiltered
    export (scripts/gem_export_gogpt.csv). Empty set when the file is missing."""
    p = Path(csv_path) if csv_path else gem_export_csv()
    if not p.exists():
        return set()
    out = set()
    with open(p, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, [])
        try:
            i_pid, i_fuel = header.index("GEM location ID"), header.index("Fuel")
        except ValueError:
            return set()
        for row in reader:
            if len(row) > max(i_pid, i_fuel) and "coal" in row[i_fuel].lower():
                out.add(row[i_pid])
    return out


def is_coal_conversion(row):
    """A unit whose Conversion/replacement? names a coal conversion: a conversion
    from coal, or a value that says coal itself."""
    conv = ws((row or {}).get("Conversion/replacement?")).lower()
    frm = ws((row or {}).get("Conversion from/replacement of (fuel)")).lower()
    return "coal" in conv or ("conversion" in conv and "coal" in frm)


def narrow_focus(index):
    """The index's `focus` when build_state_brief.py built a narrow batch (one step of the
    checklist, such as `data_centers`), else None."""
    return (index.get("focus") or None) if isinstance(index, dict) else None


def gate_validation(index, lanes, vpath=None, allow_stale=False, now=None, applied=None,
                    export=None, unfiltered_csv=None):
    """Every validation report item (brief tasks with check 7, plus the fix and
    person items in the current validation file) needs a record carrying check 7
    on that unit, a sibling, or for a whole-plant item the plant. An answer the
    human already typed into the database (a record moved to applied_in_db.json)
    still counts. An item is optional under the manual (M198: a project-level
    error on a plant that also has coal units; M220: a unit-level error on a
    coal-to-gas conversion) and a record on that plant or unit whose text says
    "optional under the manual" answers it. `export` is {unit id: row} for the
    scope; `unfiltered_csv` is the all-combustion export. Returns (offenders, info)."""
    out, info = [], []
    lanes = dict(lanes or {})
    if applied:
        lanes["applied"] = list(applied)
    if (index.get("mode") or "update") != "update":
        return out, ["skipped: not an update batch"]
    if narrow_focus(index):
        return out, [f"skipped: narrow batch ({narrow_focus(index)}); the statewide batch answers the report"]
    wanted = {}                                   # (pid, uid or None) -> text
    for p in index["plants"]:
        pid = p["plant_id"]
        for uid, tasks in (p.get("tasks") or {}).items():
            for t in tasks:
                if 7 in (t.get("checks") or []):
                    wanted.setdefault((pid, uid), t.get("text", "")[:90])
        for t in p.get("plant_tasks") or []:
            if 7 in (t.get("checks") or []):
                wanted.setdefault((pid, None), t.get("text", "")[:90])
    vpath = Path(vpath) if vpath else validation_file(index)
    if not vpath.exists():
        out.append((vpath.name, "no validation report file; run validation_report.py "
                    "for this scope (checklist row 7)"))
    else:
        data = json.loads(vpath.read_text(encoding="utf-8"))
        info.append(f"validation report {vpath.name} read {data.get('read', '?')}")
        try:
            read = datetime.datetime.fromisoformat(data.get("read", ""))
            age = ((now or datetime.datetime.now(read.tzinfo)) - read).total_seconds() / 3600
        except (TypeError, ValueError):
            age = None
        if age is None or age > EXPORT_MAX_AGE_HOURS:
            msg = (f"{vpath.name} is {'of unknown age' if age is None else f'{age / 24:.1f} days old'}; "
                   "rerun validation_report.py so items added since are answered")
            if allow_stale:
                info.append("warning: " + msg)
            else:
                out.append((vpath.name, msg))
        for e in data.get("errors", []):
            if e.get("kind") in ("fix", "person"):
                wanted.setdefault((e["plant_id"], e.get("unit_id")),
                                  f"{e.get('kind')}: {e.get('item', '')} {e.get('message', '')}"[:90])
    answered_units, answered_plants = set(), set()
    opt_units, opt_plants = set(), set()
    for _, _, rec in iter_records(lanes):
        text = " ".join(str(rec.get(k) or "") for k in PROSE_KEYS)
        if OPTIONAL_RE.search(text):
            opt_plants.add(rec.get("gem_plant_id"))
            opt_units.add(rec.get("gem_unit_id"))
            opt_units |= set(rec.get("sibling_unit_ids") or [])
        if 7 not in (rec.get("checks") or []):
            continue
        answered_plants.add(rec.get("gem_plant_id"))
        answered_units.add(rec.get("gem_unit_id"))
        answered_units |= set(rec.get("sibling_unit_ids") or [])
    coal = coal_plant_ids(unfiltered_csv) if wanted else set()
    optional = 0
    for (pid, uid), text in sorted(wanted.items(), key=lambda kv: (kv[0][0], kv[0][1] or "")):
        if (uid and uid not in answered_units) or (not uid and pid not in answered_plants):
            is_opt = pid in coal or (uid and is_coal_conversion((export or {}).get(uid)))
            if is_opt:
                optional += 1
                if (uid and uid in opt_units) or pid in opt_plants:
                    continue
                out.append((f"{pid}:{uid or 'plant'}",
                            f"optional under the manual (coal on the plant or a coal conversion), "
                            f"but not answered: write a note saying \"optional under the manual\", "
                            f"or fix it: {text}"))
                continue
            out.append((f"{pid}:{uid or 'plant'}", f"no record with check 7 answers: {text}"))
    info.append(f"validation items to answer: {len(wanted)} ({optional} unanswered but optional under the manual)")
    return out, info


def gate_lead_only(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        for u in sorted(set(ref_urls(rec))):
            d = is_lead_only(u)
            if d:
                out.append((rid, f"{d} is a lead site, so this value stays yellow: cite the "
                                 f"primary document it points to (a queue file, a permit, a "
                                 f"filing, a press release) if one exists: {u[:100]}"))
    return out


BACKUP_ONLY_RE = re.compile(r"\b(?:backup only|backup generators only|emergency generators only|"
                            r"emergency diesel|standby generators)\b", re.I)


def chase_hits(text):
    """The phrases in one note that say it was left unresearched. "backup only"
    and its kin count only when the note gives no summed MW figure."""
    t = URL_RE.sub("", str(text or ""))
    hits = {m.group(0).strip().lower() for m in CHASE_RE.finditer(t) if m.group(0).strip()}
    if not MW_FIGURE_RE.search(t):
        hits |= {m.group(0).strip().lower() for m in BACKUP_ONLY_RE.finditer(t)}
    return sorted(hits)


def gate_chase(lanes, coverage=None):
    out = []
    for lane, rid, rec in iter_records(lanes):
        for key in PROSE_KEYS:
            hits = chase_hits(rec.get(key))
            if hits:
                out.append((rid, f"{key} says it was not chased ({'; '.join(repr(h) for h in hits)}). "
                                 "Research it now and stage what you find, or say what you "
                                 "searched and did not find"))
    for sid, e in (coverage or {}).items():
        for key in ("how", "found", "note"):
            hits = chase_hits(e.get(key))
            if hits:
                out.append((f"coverage.json:{sid}", f"{key} says it was not chased "
                                                    f"({'; '.join(repr(h) for h in hits)})"))
    return out


# ------------------------------------------------ statewide source coverage ---

def load_coverage_file(batch):
    """<batch>/coverage.json as {source id: entry}. Accepts {"sources": {...}} or a
    list of entries with an `id`. Returns (entries, ids_followup, error)."""
    p = Path(batch) / "coverage.json"
    if not p.exists():
        return None, {}, f"{p.name} is missing: the statewide agent writes it (one entry per source id)"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        return None, {}, f"{p.name} does not parse: {e}"
    if isinstance(data, list):
        data = {"sources": data}
    src = data.get("sources") if isinstance(data, dict) else None
    if isinstance(src, list):
        src = {e.get("id"): e for e in src if isinstance(e, dict)}
    if not isinstance(src, dict):
        return None, {}, f'{p.name} needs a "sources" object keyed by source id'
    fol = data.get("ids_followup") or {}
    if isinstance(fol, list):
        fol = {str(e.get("eia_id")): e for e in fol if isinstance(e, dict)}
    return {k: v for k, v in src.items() if isinstance(v, dict)}, fol, ""


def coverage_list_path(batch, coverage_dir=None):
    return Path(coverage_dir or SCRIPTS.parent / "docs" / "coverage") / f"{Path(batch).name}.json"


def gate_source_coverage(batch, index, coverage_dir=None):
    """Statewide sources that must be searched (docs/coverage/<scope>.json) against
    what the statewide agent recorded in <batch>/coverage.json. Returns (offenders, info)."""
    if (index.get("where") or {}).get("kind", "state") != "state":
        return [], ["skipped: not a US state batch"]
    if narrow_focus(index):
        return [], [f"skipped: narrow batch ({narrow_focus(index)}); the statewide batch searches the source list"]
    lp = coverage_list_path(batch, coverage_dir)
    if not lp.exists():
        return [(lp.name, f"no statewide source list for this scope: write docs/coverage/{lp.name} "
                          "(id, name, url, what for each source) before the batch runs")], []
    try:
        wanted = json.loads(lp.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        return [(lp.name, f"the source list does not parse: {e}")], []
    entries, _, err = load_coverage_file(batch)
    if entries is None:
        return [("coverage.json", err)], [f"sources to search: {len(wanted)}"]
    out = []
    for w in wanted:
        sid = w.get("id")
        e = entries.get(sid)
        if e is None:
            out.append((sid, f"not recorded in coverage.json: {w.get('name')} ({w.get('url')})"))
            continue
        status = re.sub(r"[\s-]+", "_", ws(e.get("status")).lower())
        how, found, access = ws(e.get("how")), ws(e.get("found")), ws(e.get("access"))
        if status == "searched":
            if not how:
                out.append((sid, "searched but `how` is empty: name the script or the pages read"))
            if not found:
                out.append((sid, "searched but `found` is empty: say what turned up, or that nothing did"))
        elif status == "blocked":
            if not (re.search(r"fetch\.py|access_audit", access, re.I)
                    and re.search(r"wayback|web\.archive|archive", access, re.I)):
                out.append((sid, "blocked without an access record: `access` must say what fetch.py "
                                 "returned and what the Wayback lookup found"))
            elif EXCUSE.search(access):
                out.append((sid, "the access note gives a form, a script or paging as the reason; "
                                 "none of those stops a person"))
        else:
            out.append((sid, f"status {e.get('status')!r}: every listed source must be searched "
                             f"({w.get('name')})"))
    listed = {w.get("id") for w in wanted}
    info = [f"sources to search: {len(wanted)}",
            f"extra ids in coverage.json: {sorted(set(entries) - listed) or 'none'}"]
    return out, info


# ------------------------------------------------ data center backup fleets ---

DC_NEEDS_ANSWER = ("at_threshold", "unknown_capacity", "no_documents", "in_gem")
DC_DECISIONS = ("add", "already_in_gem", "update", "below_threshold", "no_generators",
                "not_data_center", "nothing_found")
# a site the harvester could not size may be closed with a number, a reason, or a search record;
# a fleet it summed at the threshold may not
DC_CLOSE_WITH_NUMBER = ("below_threshold",)
DC_CLOSE_WITH_NOTE = ("no_generators", "not_data_center", "nothing_found")


def load_data_centers_coverage(batch):
    """The `data_centers` object of <batch>/coverage.json as {site_id: entry}."""
    p = Path(batch) / "coverage.json"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}
    dc = data.get("data_centers") if isinstance(data, dict) else None
    if isinstance(dc, list):
        dc = {e.get("site_id"): e for e in dc if isinstance(e, dict)}
    return {k: v for k, v in (dc or {}).items() if isinstance(v, dict)}


def gate_data_centers(index, lanes, batch, permits_dir=None, applied=None):
    """Every data center site that data_center_fleets.py found at the threshold, with
    unknown capacity, with no document on record, or already in GEM is answered in
    coverage.json under `data_centers` (work/permits/<tag>/_data_centers.json; the tag
    is the batch folder name). An at-threshold fleet is an add or already in GEM. A
    site the harvester could not size may also be closed below_threshold with the
    summed nameplate the researcher found, or no_generators / not_data_center /
    nothing_found with a note saying what was read or searched. Returns (offenders,
    info). A missing file is a warning, not a failure."""
    tag = Path(batch).name
    p = Path(permits_dir or work_dir() / "permits" / tag) / "_data_centers.json"
    if not p.exists():
        return [], [f"warning: {p.name} not found for {tag}; run data_center_fleets.py so "
                    "backup engine fleets at data centers are checked"]
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        return [(p.name, f"does not parse: {e}")], []
    sites = data.get("sites") or []
    answers = load_data_centers_coverage(batch)
    lanes = dict(lanes or {})
    if applied:
        lanes["applied"] = list(applied)
    rids = {rec.get("record_id") for lane in ("newplants", "newunits", "applied")
            for rec in lanes.get(lane, []) if rec.get("record_id")}
    all_rids = {rec.get("record_id") for _, _, rec in iter_records(lanes) if rec.get("record_id")}
    out, need = [], 0
    for s in sites:
        verdict, sid = s.get("verdict"), s.get("site_id")
        if verdict not in DC_NEEDS_ANSWER:
            continue
        need += 1
        label = f"{s.get('name') or sid} ({verdict}, {s.get('summed_nameplate_mw')} MW)"
        a = answers.get(sid)
        if not a:
            out.append((f"data_centers:{sid}", f"{label} has no entry under data_centers in "
                                               "coverage.json: add the plant, or record why not"))
            continue
        dec = ws(a.get("decision")).lower()
        if dec not in DC_DECISIONS:
            out.append((f"data_centers:{sid}", f"decision {a.get('decision')!r} is not one of "
                                               f"{', '.join(DC_DECISIONS)}"))
        elif dec in DC_CLOSE_WITH_NUMBER + DC_CLOSE_WITH_NOTE and verdict == "at_threshold":
            out.append((f"data_centers:{sid}", f"{label} cannot be {dec}: a fleet summed at the "
                                               "threshold is an add, or already in GEM"))
        elif dec in DC_CLOSE_WITH_NUMBER and not isinstance(a.get("summed_nameplate_mw"), (int, float)):
            out.append((f"data_centers:{sid}", f"{dec} must give `summed_nameplate_mw` as a number, "
                                               "the electrical nameplate the researcher added up"))
        elif dec in DC_CLOSE_WITH_NOTE and len(ws(a.get("note"))) < 40:
            out.append((f"data_centers:{sid}", f"{dec} needs a `note` saying what was read or searched "
                                               "and what it showed"))
        elif dec == "add" and ws(a.get("record_id")) not in rids:
            out.append((f"data_centers:{sid}", "add must name the record_id of a newplants or "
                                               f"newunits record in the batch, not {a.get('record_id')!r}"))
        elif dec in ("already_in_gem", "update") and not (
                ws(a.get("plant_id")) or ws(a.get("record_id"))):
            out.append((f"data_centers:{sid}", f"{dec} must name a plant_id or a record_id"))
        elif dec == "update" and ws(a.get("record_id")) and not ws(a.get("plant_id")) \
                and ws(a.get("record_id")) not in all_rids:
            out.append((f"data_centers:{sid}", f"update names record_id {a.get('record_id')!r}, "
                                               "which is not in the batch"))
    return out, [f"data center sites needing an answer: {need} of {len(sites)}"]


# ------------------------------------------------ EIA plants missing from GEM ---

def ids_leads(index, batch, ids_file=None):
    """EIA plants of 50 MW or more that match_ids.py found in no GEM plant: from the
    index (build_state_brief.py --ids copies them), else from the ids file."""
    leads = index.get("ids_followup")
    if leads is None:
        p = Path(ids_file) if ids_file else None
        if p is None:
            w = index.get("where") or {}
            slug = w.get("slug") or (index.get("state") or "").lower().replace(" ", "-")
            p = work_dir() / f"ids_us-{slug}.json"
        if not p.exists():
            return None
        data = json.loads(p.read_text(encoding="utf-8"))
        leads = []
        for d in data.get("leads") or []:
            if d.get("source") != "eia":
                continue
            m = re.search(r"\d+", d.get("ids", ""))
            leads.append({"eia_id": m.group(0) if m else "", "name": d.get("name"),
                          "capacity_mw": d.get("capacity_mw"), "status": d.get("status")})
    return leads


def gate_ids_followup(index, lanes, batch, ids_file=None, applied=None):
    out, info = [], []
    if (index.get("mode") or "update") != "update" or (index.get("where") or {}).get("kind", "state") != "state":
        return out, ["skipped: not a US state update batch"]
    if narrow_focus(index):
        return out, [f"skipped: narrow batch ({narrow_focus(index)}); the statewide batch answers the EIA leads"]
    leads = ids_leads(index, batch, ids_file)
    if leads is None:
        return [("ids", "no match_ids.py file for this scope: run match_ids.py --state <State> "
                        "and rebuild the briefs with --ids")], []
    lanes = dict(lanes or {})
    if applied:
        lanes["applied"] = list(applied)
    texts = [json.dumps(rec, ensure_ascii=False).lower() for _, _, rec in iter_records(lanes)]
    _, fol, _ = load_coverage_file(batch)
    for d in leads:
        eid, name = str(d.get("eia_id") or ""), ws(d.get("name")).lower()
        idre = re.compile(rf"\b(?:eia\W{{0,12}}|plant\W{{0,3}}|eia_?){re.escape(eid)}\b", re.I) if eid else None
        if any((idre and idre.search(t)) or (name and f'"{name}"' in t) for t in texts):
            continue
        a = fol.get(eid) or {}
        dec = ws(a.get("decision")).lower()
        label = f"EIA plant {eid} {d.get('name')} ({d.get('capacity_mw')} MW, {d.get('status')})"
        if dec not in DECISIONS:
            out.append((f"EIA:{eid}", f"{label} is missing from GEM and has no staged record and no "
                                      f"answer: stage it as a new plant, or record a decision in "
                                      f"coverage.json ids_followup ({', '.join(DECISIONS)}) with evidence"))
        elif not ws(a.get("evidence")):
            out.append((f"EIA:{eid}", f"{label}: decision {dec} has no evidence text"))
        elif dec == "already_in_gem" and not ws(a.get("gem_plant_id")):
            out.append((f"EIA:{eid}", f"{label}: already_in_gem needs the gem_plant_id it sits under"))
    info.append(f"EIA plants missing from GEM: {len(leads)}")
    return out, info


def gate_qc(staging):
    out, ran = [], []
    for p in sorted(staging.glob("staged_*.json")):
        r = subprocess.run([sys.executable, str(SCRIPTS / "qc_checks.py"),
                            "--staged", str(p)], cwd=SCRIPTS,
                           capture_output=True, text=True)
        ran.append((p.name, r.returncode))
        if r.returncode != 0:
            lines = [ln for ln in (r.stdout + r.stderr).splitlines()
                     if "ERROR" in ln or "Error" in ln or "Traceback" in ln]
            out.append((p.name, f"qc_checks exit {r.returncode}"))
            out += [(p.name, ln.strip()[:160]) for ln in lines[:5]]
    return out, ran


# ------------------------------------------------------------------- main ---

def run(args):
    batch = Path(args.batch).resolve()
    index = load_index(batch)
    staging = batch / "staging"
    lanes = load_lanes(staging) if staging.is_dir() else {}
    lanes_meta = load_lanes_meta(staging) if staging.is_dir() else {}
    csv_path = resolve_csv(args.csv, index)
    ids = {u for p in index["plants"] for u in p["unit_ids"]}
    for _, _, rec in iter_records(lanes):
        ids.add(rec.get("gem_unit_id"))
        ids |= set(rec.get("sibling_unit_ids") or [])
    header, export = load_export(csv_path, ids)

    gates = []

    def add(name, hard, offenders, status=None, info=None):
        gates.append({"name": name, "hard": hard,
                      "status": status or ("FAIL" if offenders else "PASS"),
                      "count": len(offenders),
                      "offenders": [{"id": a, "reason": b} for a, b in offenders],
                      "info": info or []})

    add("coverage", True, gate_coverage(batch, index))
    add("banned", True, gate_banned(lanes))
    ver, by_hand = gate_verified(lanes)
    add("verified", True, ver,
        info=[f"spreadsheet citations confirmed by hand ({len(by_hand)})"])
    add("orphans", True, gate_orphans(lanes))
    add("fresh", True, gate_fresh(lanes, export))
    add("headers", True, gate_headers(lanes, header))
    add("cell-prose", True, gate_cell_prose(lanes))
    add("dates", True, gate_dates(lanes))
    add("latest-activity", True, gate_latest_activity(lanes, export))
    add("additive", True, gate_additive(lanes))
    add("location", True, gate_location(lanes, index, batch))
    acc, acc_info = gate_access(batch)
    add("access", True, acc, info=acc_info)
    applied_path = staging / "applied_in_db.json"
    applied = (json.loads(applied_path.read_text(encoding="utf-8")).get("records") or []
               if applied_path.exists() else [])
    val, val_info = gate_validation(index, lanes, args.validation, args.allow_stale_validation,
                                    applied=applied, export=export)
    add("validation", True, val, info=val_info)
    idf, idf_info = gate_ids_followup(index, lanes, batch, applied=applied)
    add("ids_followup", True, idf, info=idf_info)
    dc, dc_info = gate_data_centers(index, lanes, batch, applied=applied)
    add("data-centers", True, dc, info=dc_info)
    add("lead-only", False, gate_lead_only(lanes))
    cov_entries, _, _ = load_coverage_file(batch)
    add("chase", True, gate_chase(lanes, cov_entries))
    sc, sc_info = gate_source_coverage(batch, index)
    add("statewide-coverage", True, sc, info=sc_info)
    add("build", True, gate_build(lanes))
    add("false-high", False, gate_false_high(lanes))
    add("independence", False, gate_independence(lanes))
    if args.entity_check:
        ent, skip = gate_entities(lanes, args.entity_csv)
        if skip:
            add("entities", False, [], status="SKIPPED", info=[f"skipped: {skip}"])
        else:
            add("entities", False, ent)
    else:
        add("entities", False, [], status="SKIPPED",
            info=["skipped: pass --entity-check to run the lookup"])
    add("notes", False, gate_notes(lanes))
    strict_q = question_strict(lanes_meta, args.strict_questions)
    add("questions", strict_q, gate_questions(lanes, strict_q),
        info=[] if strict_q else ["advisory: a batch assembled before the question fields; --strict-questions makes it hard"])
    add("concern-types", False, gate_concern_types(lanes))
    add("monitor-fields", False, gate_monitor_fields(lanes))
    add("watch-case", False, gate_watch_case(lanes, index))
    add("location-notes", False, gate_location_notes(lanes))
    add("note-drift", False, gate_note_drift(batch, index, export))
    qc_ran = []
    if args.no_qc:
        add("qc_checks", True, [], status="SKIPPED", info=["skipped: --no-qc"])
    else:
        qc, qc_ran = gate_qc(staging)
        add("qc_checks", True, qc,
            status="FAIL" if any(rc for _, rc in qc_ran) else "PASS",
            info=[f"{name} exit {rc}" for name, rc in qc_ran])
        gates[-1]["count"] = sum(1 for _, rc in qc_ran if rc)

    failed = [g["name"] for g in gates if g["hard"] and g["status"] == "FAIL"]
    return {"batch": str(batch), "csv": str(csv_path),
            "lanes": {k: len(v) for k, v in lanes.items()},
            "spreadsheet_by_hand": [{"id": a, "url": b} for a, b in by_hand],
            "gates": gates, "failed": failed,
            "verdict": "CLEAN" if not failed else "FAILED"}


def report(res):
    print(f"state gate: {res['batch']}")
    print("  lane files: " + (", ".join(f"{k}={v}" for k, v in res["lanes"].items())
                              or "(none)"))
    for g in res["gates"]:
        kind = "HARD" if g["hard"] else "ADVISORY"
        print(f"GATE {g['name']} {kind} {g['status']} ({g['count']})")
        for line in g["info"]:
            print(f"    {line}")
        offs = g["offenders"]
        for o in offs[:CAP]:
            print(f"    {o['id']}: {o['reason']}")
        if len(offs) > CAP:
            print(f"    … and {len(offs) - CAP} more")
    print("GATE CLEAN" if not res["failed"]
          else f"GATE FAILED: {', '.join(res['failed'])}")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--csv", default=None,
                    help="fresh scoped export (default: _index.json csv, "
                         "else scripts/gem_export_gogpt_scoped.csv)")
    ap.add_argument("--entity-check", action="store_true")
    ap.add_argument("--entity-csv", default=str(SCRIPTS / "gem_export_gogpt.csv"),
                    help="export the entity lookup scans (default: the "
                         "unfiltered all-combustion export; entities are "
                         "shared across trackers)")
    ap.add_argument("--validation", default=None,
                    help="validation_report.py JSON (default: work/validation_<tag>.json "
                         "for the batch scope)")
    ap.add_argument("--allow-stale-validation", action="store_true",
                    help="warn instead of failing when the validation file is over a day old")
    ap.add_argument("--strict-questions", action="store_true",
                    help="fail on a qa record without question and finding, whatever the batch's date")
    ap.add_argument("--no-qc", action="store_true",
                    help="skip qc_checks.py --staged on the lane files")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    res = run(args)
    if args.json:
        print(json.dumps(res, indent=1, ensure_ascii=False))
    else:
        report(res)
    sys.exit(0 if not res["failed"] else 1)


if __name__ == "__main__":
    main()
