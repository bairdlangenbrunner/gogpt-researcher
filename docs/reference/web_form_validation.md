# What the GEM web form checks when a plant is saved

Read from the database code (`GEM-project-db`, `projects/powerplant_views.py`, function `validate` and its helpers, commit a26b658, read 2026-11-07). The repo is read-only to us; this page is the working copy of the rules for GOGPT. If the code changes, the live form wins.

The form sorts what it finds into two kinds:

- **Errors stop the save.** Nothing is written until they are fixed.
- **Warnings are saved with the plant.** They are stored in `plant.validation` and become the Validation Report tab, which `validation_report.py` reads for every batch.

Every new plant and new unit the researcher proposes should clear both, so that Baird or the browser-apply session can type it in once and leave no report items behind. `state_gate.py` gate `add-basics` checks staged adds against this list (Baird 2026-11-07).

## Errors (the save fails)

- The plant name is blank, or another plant in the database (any tracker, not deleted) already has it. A staged add whose name is already in the export was either typed in already or is a duplicate.
- Two units of the plant have the same name.
- An update date that is not written YYYY-MM-DD.

## Required values (reported as "Required")

Plant:

- Country.
- Latitude and Longitude. They are checked at plant level unless the plant is set to unit-level location, which GOGPT never uses.
- Location accuracy, as soon as coordinates are entered. Latitude must be between -90 and 90, longitude between -180 and 180, and the two come as a pair.

Each unit:

- A status timeline with a current status. Every timeline row that has a status needs a date, only one row can be marked current, and the current row cannot sit before a later dated row. A withdrawn plan needs its withdrawn year.
- Capacity, and not zero.
- At least one fuel, with a fuel detail that belongs to its category.
- Technology, whenever a fuel is coal, fossil gas or fossil liquids. That is every GOGPT unit. "unknown" is a valid choice, staged only after a comprehensive search finds no source anywhere online that names the design (`controlled_vocab.md`, Baird 2026-11-07).

The manual still allows a blank capacity or an approximate point on an add. The form will report the blank, so the staged record says what was searched: put the field in `not_found` with a sentence, for example `"not_found": {"Capacity (MW)": "Searched the county board packets, the air permit system and the developer's site; no size is given."}`. A plain list (`"not_found": ["Capacity (MW)"]`) passes only when `researcher_notes` says what was searched for it.

## A value needs its Data Source

When one of these is filled, the matching Data Source box needs a link, or the form reports it:

| Value | Data Source box | No link needed when the value is |
|---|---|---|
| Owner(s) | Owners Data Source | |
| Operator(s) | Operators Data Source | |
| Fuel | Fuel Data Source | |
| Capacity (MW), Number Of Engines, Capacity Per Engine, capacity rating | Capacity Data Source | |
| Turbine/Engine Technology | Turbine/Engine Technology Data Source | unknown |
| Equipment Manufacturer/Model | its Data Source | |
| CHP, CCS attachment | their Data Sources | not found |
| Backup Power | Backup Power Data Source | no |
| Captive, Captive industry type and use | Captive Data Source | |
| Latest Activity | Latest Activity Data Source | |
| Disrupted by conflict | its Data Source | no |
| Employment notes, cost, financing, associated projects, pipelines, data center power purchase agreement, associated storage | their Data Sources | |
| Any location value (country, state, area, city, coordinates, accuracy) | Location Data Source | |

The last row means every plant needs a Location Data Source: the country alone triggers it.

The repo's own rule is stricter for one case: `qc_checks.py` and gate `orphans` want a link even for Technology "unknown". Use the queue entry or document that shows no turbine type is given.

## Other warnings

- Fuel shares over 100 percent, or owner shares over 101 percent.
- Names: a double space; any of `# < > [ ] { } % + ? |`; "phase" or "extension" in a plant name (put the phase in the unit name); a unit named `--` when the plant has more than one unit.
- A replacement or conversion link that points at a unit that does not exist.

For combustion plants the code skips the status-change checks and the per-row timeline Data Source checks (those run for LNG terminals only), and the cost-unit and interim facility checks are LNG-only too.

## Where it is enforced

- `state_gate.py` gate `add-basics`: Technology from the dropdown, a dated milestone, and everything on this page for each add not yet typed in. Adds whose name is already in the export, or whose record is in `applied_in_db.json`, are set aside with one line saying so.
- `state_gate.py` gate `validation`: every item in the live Validation Report for the scope is answered by an edit.
- The browser-apply session reads the form's warnings after each save (`docs/sops/database-browser-edits.md` §5).
