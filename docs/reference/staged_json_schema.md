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
| `staged_newplants.json` | `newplants` | candidate new plants (with their units) |
| `staged_newunits.json` | `newunits` | new units at an existing plant |

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
| `independent` | bool | ≥2 genuinely independent sources reached |
| `source_language` | str | e.g. `"en"`, `"pt"` |
| `researcher_notes` | str | rationale, conflicts, Background-worthy narrative |
| `action` | str | one-line web-UI instruction ("On G100234, set Status to shelved; paste refs into Status Data Source") |

Ref semantics are **merge, never replace**: `refs` URLs are ADDED to the
existing Data Source cell contents; existing datasources are never deleted
(`datasource_conventions.md`). URLs appear ONLY in Data Source columns, never
inside value cells.

## Lane-specific fields

**`updates`** — the core lane. One record per (unit, edit-cluster). Extra:
`delete: true` marks a staged deletion (the existing value could not be
supported by any source; apply = clear the cell, note why). Project-level
fields (ownership, location, plant names) must be staged onto **every unit row
of the plant** — stage one record per unit or set `applies_to_all_units: true`
with the sibling `gem_unit_id`s listed in `sibling_unit_ids`.

**`qa`** — never an edit. Extra: `concern_type`
(`existence` | `duplicate` | `scope` | `capacity-threshold` |
`conversion-link` | `attribution` | `other`), `recommendation` (short human
next step). `fields` stays empty.

**`entity`** — extra: `entity_name`, `role` (`owner`/`operator`/`parent`),
`entity_country`, `lookup_result` (the `entity_lookup.py` outcome that
justified staging a NEW entity — including any cross-country warning). Created
entities get an `E####` ID assigned by the DB.

**`monitor`** — extra: `monitor_reason` (which add-threshold leg failed:
capacity unconfirmed, no concrete step, sponsor unclear…), `recheck_by`
(YYYY-MM). Monitor records roll forward between quarters until promoted or
dropped.

**`newplants`** — plant-level `fields` plus a `units` list, each unit a mini
record with its own `fields`/`refs` (unit name per `unit_conventions.md`,
capacity ≥ threshold or an explicit scope justification in
`researcher_notes`). New-plant records must have cleared the add threshold:
named sponsor + specific site + a concrete development step, each corroborated.

**`newunits`** — like a `newplants` unit record but anchored to
`gem_plant_id`; used for expansions/uprates at existing plants.

## QC gates (mechanical, enforced before deliverables)

- `qc_checks.py --staged <file>` passes with zero ERRORs (vocab, thresholds,
  status-year consistency, ownership shares, unknown headers).
- Every `refs` URL has a passing `verifications` entry (`ok` and
  `contains_value` — but see `confidence_tiers.md` on status-by-inference).
- Blocklist: no gem.wiki / globalenergymonitor.org / GEM-derived republishers /
  abarrelfull anywhere in `refs`.
- A record with zero verified refs cannot stay in `updates`/`newplants`/
  `newunits` — downgrade to `monitor` (candidates) or `qa` (concerns), or drop.
