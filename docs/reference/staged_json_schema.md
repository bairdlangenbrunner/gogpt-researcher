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
| `staged_monitor.json` | `monitor` | watch-list candidates below the add threshold |
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
| `refs` | {header: [url]} | verified URLs per **Data Source column** (e.g. `"Status Data Source"`); every column in `fields` MUST have its paired Data Source entry, and vice versa — no orphan values, no orphan refs |
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

**`qa`** — never an edit. Extra: `concern_type`, `recommendation` (short human
next step), `proposed_value` (`{column: value}` when the question is about a
specific value). `fields` stays empty. `concern_type` is either the exact
header of the column the question is about (`Status`, `Capacity (MW)`,
`Owner(s)`, ...) or one of: `existence` (a unit or plant may be missing or may
not exist) | `duplicate` | `scope` (unit grouping, combined-cycle block, what
counts as one unit) | `capacity-threshold` | `identity` (which unit the source
means, unit naming) | `attribution` (who the owner really is) |
`conversion-link` | `location` | `source` (a dead or wrong link) |
`validation` (an error from the validation report) | `other`. Shards may write
free text; `assemble_state.py` maps it onto this list and keeps the original
in `concern_type_raw`. `state_gate.py` (advisory `concern-types`) lists what
did not map. The review page files each question under the checklist box the
type implies (`review_app/checklist.py`).

**`entity`** — extra: `entity_name`, `role` (`owner`/`operator`/`parent`),
`entity_country`, `lookup_result` (the `entity_lookup.py` outcome that
justified staging a NEW entity — including any cross-country warning). Created
entities get an `E####` ID assigned by the DB.

**`monitor`** — the watch list. Extra: `monitor_reason` (required; which
add-threshold leg failed: capacity unconfirmed, no concrete step, sponsor
unclear, or what to watch at an existing plant), `recheck_by` (required,
YYYY-MM), `monitor_kind` (`new_to_tracker`: a plant or project GEM does not
have, `gem_plant_id` blank | `existing_plant`: a possible change or expansion
at a plant GEM already tracks, `gem_plant_id` set). Optional `capacity_mw`,
`status`. `assemble_state.py` fills `monitor_reason` from an older `item` key
or the note, sets `monitor_kind` from `gem_plant_id` when the shard did not,
and drops a candidate a reviewer removed from the watch list. Monitor records
roll forward between quarters until promoted, sent to the possible-updates
backlog, or removed; the review page's four calls for them are in
`review_app/README.md`. A record called "incorporate into database" is not
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
`researcher_notes`). New-plant records must have cleared the add threshold:
named sponsor + specific site + a concrete development step, each corroborated.

**`newunits`** — like a `newplants` unit record but anchored to
`gem_plant_id`; used for expansions/uprates at existing plants.

Both come from the scope-wide agent's `shards/_state.json` (`newplants` and
`newunits` sections) as well as from a discovery batch. A gas project in a
utility integrated resource plan clears the add threshold on the plan alone,
draft plans included (Baird 2026-10-07); a thinner lead stays a `monitor`
record.

## QC gates (mechanical, enforced before deliverables)

- `qc_checks.py --staged <file>` passes with zero ERRORs (vocab, thresholds,
  status-year consistency, ownership shares, unknown headers).
- Every `refs` URL has a passing `verifications` entry (`ok` and
  `contains_value` — but see `confidence_tiers.md` on status-by-inference).
- Blocklist: no gem.wiki / globalenergymonitor.org / GEM-derived republishers /
  abarrelfull anywhere in `refs`.
- A record with zero verified refs cannot stay in `updates`/`newplants`/
  `newunits` — downgrade to `monitor` (candidates) or `qa` (concerns), or drop.
