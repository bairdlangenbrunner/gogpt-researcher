# Staged-JSON contract

The machine-readable interface between research output and the human apply step
(hand edits in the GEM project DB web UI — nothing here is ever auto-applied).
**Treat this document as the contract**: `qc_checks.py --staged` and
`build_review_package.py` both consume these files; if a field changes,
version-note it here.

Files live in the per-scope staging dir (`batches/<scope>/staging/`, committed
as the audit trail), one per lane:

| file | lane | holds |
|---|---|---|
| `staged_updates.json` | `updates` | edits to existing plants/units |
| `staged_qa.json` | `qa` | read-and-flag concerns — never an edit |
| `staged_entity.json` | `entity` | new entities to create (after `entity_lookup.py` found no match) |
| `staged_monitor.json` | `monitor` | watch-list candidates that cannot be added yet (one of the seven `watch_case` values below) and things to watch at existing plants |
| `staged_newplants.json` | `newplants` | candidate new plants (with their units); `assemble_state.py` writes it only when the scope-wide search staged one, the other five lanes are always written |
| `staged_newunits.json` | `newunits` | new units at an existing plant |

`assemble_state.py` also writes `irp_summary.json` next to them for a US state that ran the IRP step (`irp_sheet.py`, Update SOP §3 step 8): the plan file read, the read date, a skipped flag, and one plain sentence per utility from the scope-wide agent's `meta.irp_summary`, used by `build_review_package.py --irp` for the Notes draft. Not a lane; `qc_checks.py` ignores it.

Two more files may sit next to them once a batch has been through the review app
(`review_app/`): `review_log.jsonl` (append-only, one JSON record per reviewer call or undo,
keyed on `<staging dir>::<record_id>`) and `review_decisions.json` (derived, latest record per
key). They are committed with the batch. `build_review_package.py --decisions` reads the log;
`qc_checks.py` ignores both.

There is deliberately **no wiki lane** — GOGPT wiki pages are auto-generated
from the DB; only the free-text "Background" section is hand-editable, and
Background-worthy narrative goes in a record's `researcher_notes` for the human
to place (see `wiki_pages.md`).

## Envelope (every file)

```json
{
  "meta": {
    "lane": "updates",
    "scope": {"country": "Nigeria", "quarter": "q3-2026",
              "csv": "gem_export_gogpt_scoped.csv"},
    "generated": "2026-07-27T14:00:00-04:00",
    "counts": {"records": 12}
  },
  "records": [ { ... } ]
}
```

## Common record core

| field | type | meaning |
|---|---|---|
| `gem_unit_id` | str | `G####` display ID (empty only in `newplants`/`newunits`/`entity`) |
| `gem_plant_id` | str | `T####` display ID (required in `newunits`; empty in `newplants`) |
| `plant_name`, `unit_name`, `country` | str | identity, from the scoped export |
| `fields` | {header: value} | proposed values, keyed by EXACT CSV header strings (e.g. `"Status"`, `"Capacity (MW)"`) — `qc_checks.py --staged` validates headers and vocab |
| `current` | {header: value} | the same columns' values before this batch (diff context for the reviewer) |
| `refs` | {header: [url]} | verified URLs per **Data Source column** (e.g. `"Status Data Source"`); every column in `fields` MUST have its paired Data Source entry, and vice versa — no orphan values, no orphan refs. Status Detail is its own source column: its links are keyed `"Status Detail"` and written into the text of the value (Baird 2026-10-08) |
| `verifications` | [{url, ok, contains_value}] | `url_verifier.py` results — no URL enters `refs` without a passing entry |
| `tier` | str | `high` \| `medium` \| `low` (see `confidence_tiers.md`) |
| `independent` | bool | ≥2 genuinely independent sources reached (preferred, not required; required for green on a status change) |
| `source_language` | str | e.g. `"en"`, `"pt"` |
| `researcher_notes` | str | rationale, conflicts, Background-worthy narrative — **plain language for a human reader**, per `notes_style.md` (no repo jargon, sources named by what they are) |
| `action` | str | one instruction a person follows in the web form, in plain words ("Set the status of unit GT5 to retired and the retired year to 2024. Add the two links below to the status and retired-year source boxes. Keep the links already there.") |
| `record_id` | str | optional, added 2026-10-02: `<plant_id>:<unit_id>:<field slug>`, stable across rebuilds so a review-app decision survives a rebuild; written by `assemble_state.py` |
| `reverified` | bool | optional, added 2026-10-02: the value is unchanged and a new source confirms it (blue in the workbook); the new URL still merges into the Data Source cell |
| `additive` | bool | optional, added 2026-10-07: the `fields` value for `Status Detail` or `Notes` is the new text placed above the existing text (see below); written by `assemble_state.py` |
| `irp` | bool | optional, added 2026-10-07, US only: the value comes from a utility integrated resource plan (the shard's finding carried `irp: true`, or one of its refs is a plan link the IRP step listed). The export's `IRP` column is never staged; this flag plus the export's box state tell the review page and the `irp_box` sheet which units need the IRP box ticked in the web form (checklist row 37). Written by `assemble_state.py` |
| `captive_lng` | bool | optional, added 2026-10-08, `monitor` / `newplants` / `newunits`: the record comes from the captive LNG sheet step (`captive_lng.py`, `briefs/_captive.md`); the scope-wide agent sets it with `checks: [6, 44]` and `assemble_state.py` passes it through. The review page files the record under checklist rows 6 and 44 |
| `location_method` | str | optional (since 2026-10-20), on a record that stages `Latitude`, `Longitude` and `Location accuracy`: `published` (one of the manual's five routes to exact, no imagery needed), `address`, `site_reference`, `dataset`, `map` or `imagery`, the rung of the location ladder that placed the point (`location.md`). Comes with `location_route` (str, one sentence naming who published the point; required for an exact point from `dataset` or `site_reference`, advisory for `published`), `location_moved_m` (int, meters from GEM's current point, blank when GEM had none), and for `map` only `location_control_points` (list of `{"feature", "px", "lat", "lon"}` plus `fit_m`) and `location_image` (the batch-relative path of the saved map render under `staging/maps/`). Also `location_fit_m` (the fit error) and `location_needs_review` (bool). The agent writes them in the shard's top-level `location` object; `assemble_state.py` folds the three fields into ONE plant-level record (`<plant_id>:plant:location`, `applies_to_all_units`, `sibling_current` holding a dict of the three columns per sibling) and passes the meta through; `state_gate.py` gate `location` reads them |

Ref semantics are **merge, never replace**: `refs` URLs are ADDED to the
existing Data Source cell contents; existing datasources are never deleted
(`datasource_conventions.md`). URLs appear ONLY in Data Source columns, never
inside value cells.

**Status Detail and Notes are additive, newest on top** (Baird 2026-10-07). Both boxes are running logs in the web form. A staged `fields` value for either is the full box contents to paste: the new text on its own line, then the existing text word for word (`build_review_package.additive_value`). Never a rewrite, never a shortening, never a deletion. `state_gate.py` gate `additive` and `build_review_package.validate` fail any value that does not end with the current text, on the unit and on every sibling of a plant-wide edit.

## Lane-specific fields

**`updates`** — the core lane. One record per (unit, edit-cluster). Extra:
`delete: true` marks a staged deletion (the existing value could not be
supported by any source; apply = clear the cell, note why). Project-level
fields (ownership, location, plant names) must be staged onto **every unit row
of the plant** — stage one record per unit or set `applies_to_all_units: true`
with the sibling `gem_unit_id`s listed in `sibling_unit_ids`.

**`qa`** — never an edit. Extra: `concern_type`, `question`, `finding`, `recommendation` (short human
next step), `proposed_value` (`{column: value}` when the question is about a
specific value). `fields` stays empty. `concern_type` is either the exact
header of the column the question is about (`Status`, `Capacity (MW)`,
`Owner(s)`, ...) or one of: `existence` (a unit or plant may be missing or may
not exist) | `duplicate` | `scope` (unit grouping, combined-cycle block, what
counts as one unit) | `capacity-threshold` | `identity` (which unit the source
means, unit naming) | `attribution` (who the owner really is) |
`conversion-link` | `location` | `source` (a dead or wrong link) |
`validation` (an error from the validation report) | `notes_cleanup` (an outdated or no longer applicable line in the Notes box: the researcher flags it for a human to remove, and never shortens Notes) | `other`. Shards may write
free text; `assemble_state.py` maps it onto this list and keeps the original
in `concern_type_raw`. `state_gate.py` (advisory `concern-types`) lists what
did not map. The review page files each question under the checklist box the
type implies (`review_app/checklist.py`).

A `qa` record carries four person-facing parts. `question` is one sentence that ends with "?", stays under about 120 characters, and is specific to the record. `finding` is one to three sentences on what the sources say. `recommendation` is one or two sentences, an instruction the reviewer can act on: leave as is, change X to Y, merge with Z, ask the PM, or cancel; never "the reviewer should decide". `researcher_notes` holds everything else (in a shard the key is `note` and the assembler renames it). A merged record may also carry `merged_from` (the id of a dropped record), and a backfilled one `recommendation_raw`.

**`entity`** — extra: `entity_name`, `role` (`owner`/`operator`/`parent`),
`entity_country`, `lookup_result` (the `entity_lookup.py` outcome that
justified staging a NEW entity — including any cross-country warning). Created
entities get an `E####` ID assigned by the DB.

**`monitor`** — the watch list. Extra: `monitor_reason` (required; in one
sentence why this is not an add or an edit yet, or what to watch at an
existing plant), `recheck_by` (required, YYYY-MM), `monitor_kind`
(`new_to_tracker`: a plant or project GEM does not have, `gem_plant_id` blank |
`existing_plant`: a possible change or expansion at a plant GEM already
tracks, `gem_plant_id` set), and for a `new_to_tracker` record or a lead
`watch_case` (added 2026-10-23, one of `schema_constants.WATCH_CASES`):
`no_generation` | `under_threshold` | `drive_or_storage` | `duplicate_check` |
`not_committed` | `other_scope` | `unverified`. **A
project that fits none of them is an add, not a watch item** (the add
threshold under `newplants` below). Optional `capacity_mw`, `status`.
`assemble_state.py` fills `monitor_reason` from an older `item` key or the
note, sets `monitor_kind` from `gem_plant_id` when the shard did not, sets
`watch_case` `unverified` on a lead it demotes itself, and drops a candidate a
reviewer removed from the watch list. `state_gate.py` gate `watch-case`
(advisory) flags a new-to-tracker watch item with no case, an
`under_threshold` case whose own `capacity_mw` reaches the threshold, and an
`unverified` case with a passing verification. Monitor records
roll forward between quarters until promoted, sent to the possible-updates
backlog, or removed; the review page's calls for them are in
`review_app/README.md`. Optional `lead_for` (`newplants` | `newunits`): the
record is a lead, a new plant or new unit the agent found but could not
stage as a row; `assemble_state.py` sets it when it turns a thin new-row
record into a monitor record, and the review page shows leads with the
proposed additions, where they take the extra call "research further". A
record called "incorporate into database" or "research further" is not
edited in place: `build_state_brief.py --promote <staging dir>` reads the
call from `review_log.jsonl` and makes it a research task in the next batch,
whose research produces the real `updates`, `newplants` or `newunits` record.

**`checks`** (any lane, optional) — row numbers of the QC/Country checklist
tab that this record serves, copied from the brief task that produced it.
Derived bookkeeping, not research content: `review_app/checklist.py` uses it
first and falls back to the column and the value when it is absent.

**`newplants`** — plant-level `fields` plus a `units` list, each unit a mini
record with its own `fields`/`refs` (unit name per `unit_conventions.md`,
capacity ≥ threshold or an explicit scope justification in
`researcher_notes`).

**The add threshold (Baird 2026-10-23, from the manual's own bar).** A project GEM lacks is added when ONE verified public source names a gas or oil generating project, places it in the scope, and gives a capacity at the threshold (50 MW, or 20 MW in the EU and UK; engine and aeroderivative sets summed), a unit count with a plant total, or no capacity at all. The manual says to add a plant whose capacity cannot be found with the cell blank and to remove it later if it proves small, so a missing figure never holds an add back; neither does a missing start year, owner, turbine model or exact coordinate. Those stay blank, with a note in `researcher_notes` saying what was not found. The manual's status ladder decides the status, never the add: a long-range planning document, a grid-operator interconnection queue entry or a press announcement is `announced`; a permit application, land, financing, a prior-approval docket or a signed interconnection agreement is `pre-construction`. A project found already cancelled, shelved or retired since 2020 is an add with that status. A queue entry whose sponsor is a shell company is still an add at `announced` under its queue name (the live database already records 18 US units from ERCOT, MISO, SPP and PJM documents alone). Only the seven `watch_case` values keep a project on the watch list; a find in another state or country is a `monitor` record with `watch_case` `other_scope`, and the evidence file lists those as handoffs. A status change at an existing plant still needs two independent publishers for green (one is yellow); an add from one source is green on every other value.

**`newunits`** — like a `newplants` unit record but anchored to
`gem_plant_id`; used for expansions/uprates at existing plants. A queue entry
or filing for new capacity at a plant GEM has is a `newunits` record once the
source names the plant, not a watch item; it is a `qa` question
(`concern_type` `duplicate`) only when it may describe a unit GEM already has.

Both come from the scope-wide agent's `shards/_state.json` (`newplants` and `newunits` sections) as well as from a discovery batch. A gas project in a utility integrated resource plan is an add on the plan alone, draft plans included (Baird 2026-10-07); capacity a plan only studies as an option, outside its preferred portfolio, is a `monitor` record with `watch_case` `not_committed`. A captive plant at an LNG terminal is an add when a source verifies generating capacity at the threshold (50 MW, or 20 MW in the EU and UK), never compressor-drive turbines; the captive LNG sheet's Qualifying rows are the ones to check first (Baird 2026-10-27). A gas-fired data center plant is an add like any other project, with its status from the manual's ladder; there is no data center hold. Backup engine fleets at data centers are adds at the summed nameplate threshold (see "Data center backup fleets" below).

**Fields on `newplants` and `newunits` unit rows.** `Backup Power` (yes at unit level for a backup fleet), `Number Of Engines` and `Capacity Per Engine` are stageable on a unit row. `Number Of Engines` and `Capacity Per Engine` are for internal combustion sets and aeroderivative gas turbine sets; a frame gas turbine is one turbine per unit with its capacity in `Capacity (MW)`. Captive fields go with them for a backup fleet (Captive industry type data center, Captive industry use power).

**Projected years are scheduled events.** A projected year in `Start year` or `Planned retire` is the Event Year of a scheduled event (the Source Year is the year the source reported it). The `action` tells the human to add a new scheduled event entry, never to change an existing one. There is no Planned checkbox.

**Inferred statuses.** A record that stages `shelved - inferred 2 y` or `cancelled - inferred 4 y` carries a Latest Activity datasource in its refs and the computed milestone year (the Latest Activity date plus two or four years). An inferred status is no longer exempt from the orphan rule.

**Data center backup fleets.** The harvester writes `scopes/<tag>/work/permits/_data_centers.json`, one object: `scope` (the state or country name), `tag` (`us-mi`), `generated` (ISO date), `threshold_mw` (50, or 20 for EU and UK scopes), and `sites`, a list. Each site has `site_id` (a slug the harvester keeps stable across runs, built from operator and place), `name`, `operator`, `address`, `city`, `permit_numbers` (list), `permit_urls` (list, every URL verified or marked with the fetch route that failed), `issue_date`, `fuel` (`diesel`, `natural gas`, `dual`, `unknown`), `engine_count` (integer or null), `capacity_per_engine_mw` (number or null), `summed_nameplate_mw` (number or null, electrical), `phases` (list of `{label, engines, mw, status_hint}`, empty when the permit does not split the fleet), `gem_plant_id` and `gem_plant_name` (null unless a GEM data center plant matches by name or address), `verdict` and `source_notes` (plain language, what the permit says and where the numbers come from). `verdict` is one of `at_threshold` (sum at or above the threshold), `unknown_capacity` (generators listed, or documents on record that did not load, and no usable nameplate; the manual adds with capacity blank once generators are confirmed), `no_documents` (a named site with no permit or filing on record yet; the researcher searches for one), `below_threshold`, `in_gem` (a GEM plant already covers the fleet; the site still gets a check task comparing the fleet, phases and Backup Power box with the permit), `no_generators` (the permit covers no generators). The researcher answers every `at_threshold`, `unknown_capacity`, `no_documents` and `in_gem` site in `coverage.json` under `data_centers`: `decision` `add` (with the `record_id`), `already_in_gem` (with `plant_id`), `update` (with the `record_id`), `below_threshold` (with `summed_nameplate_mw`, the number added up), or `no_generators`, `not_data_center`, `nothing_found` (each with a `note` of at least a sentence saying what was read or searched). An `at_threshold` site may only be `add`, `already_in_gem` or `update`. A narrow catch-up batch built with `build_state_brief.py --data-centers-only` records `focus: data_centers` in `briefs/_index.json`; the `validation`, `ids_followup` and `statewide-coverage` gates step aside for it and the statewide batch answers those.

`batches/<tag>/coverage.json` gains a `data_centers` object keyed by `site_id`: `decision` is `add` (with `record_id` of the newplants record), `already_in_gem` (with `plant_id`), `update` (with `record_id` of the updates record, when the permit disagrees with the GEM rows), `below_threshold` (with `summed_nameplate_mw`) or `no_generators`, plus `note`. The gate `data-centers` requires an answer for every site whose verdict is `at_threshold`, `unknown_capacity` or `in_gem`; `add` is the only valid decision for `at_threshold` and `unknown_capacity` sites unless the note names the GEM plant that already holds the fleet.

## QC gates (mechanical, enforced before deliverables)

- `qc_checks.py --staged <file>` passes with zero ERRORs (vocab, thresholds,
  status-year consistency, ownership shares, unknown headers).
- Every `refs` URL has a passing `verifications` entry (`ok` and
  `contains_value` — but see `confidence_tiers.md` on status-by-inference).
- Blocklist: no gem.wiki / globalenergymonitor.org / GEM-derived republishers /
  abarrelfull anywhere in `refs`.
- A record with zero verified refs cannot stay in `updates`/`newplants`/
  `newunits` — downgrade to `monitor` (candidates) or `qa` (concerns), or drop.
