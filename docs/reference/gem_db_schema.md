# GEM Project Database: GOGPT Schema Reference

Distilled from `gem-db-ops/docs/gem_schema.dbml` (live-Postgres-derived DBML, 72
tables) and the export/join logic in `gem-db-ops/gem_all_fields.py`
(`export_gogpt_all_fields`, `GOGPT_COLUMNS`), cross-checked against the
86-column header held canonically in `gem-db-ops/gem_colmap.py`
(`GOGPT_EXPECTED_COLUMNS`, aliased as `EXPECTED_COLUMNS` by
`scripts/pull_gem_db.py`).

This covers what a GOGPT researcher needs to read the CSV export and stage
edits applied by hand in the live DB UI (gem-project-db.herokuapp.com). It
does not re-derive the manual's field-by-field editing rules — see
`docs/reference/datasource_conventions.md` for datasource/entity/location
mechanics and `docs/sops/update.md` for editing procedure.

## Terminology

- **Project**: the DB's tracker-agnostic term, stored in the `plant` table.
  GOGPT's web UI calls this a **"location."** The LNG tracker's web UI calls
  the same underlying table a **"Terminal."** Same table, different display
  label and ID prefix per tracker (see "Display IDs" below).
- **Unit**: sub-part of a project, stored in `powerplant_unit`. Wind/solar
  trackers call the equivalent thing a "phase"; GOGPT keeps "unit."
- **Entity**: any company/government/agency that can be an owner or operator,
  stored in `company`. DB-wide term from the Beneficial Ownership Data
  Standard — shared across every GEM tracker, not GOGPT-specific.

## Row structure and scope

- **One row per unit.** The export is generated from `powerplant_unit`
  joined up to `plant`; a multi-unit plant produces one row per unit with
  project-level fields duplicated across all its unit-rows.
- **The export is NOT scoped to GOGPT.** `export_gogpt_all_fields` selects
  every `powerplant_unit` row belonging to a `plant` with
  `projectType = 1` (combustion) — it does **not** filter on
  `powerplant_unit."trackerSearch" = 'GOGPT'`. The website's
  `?tracker=GOGPT` export parameter is cosmetic in the same way; both mirror
  the live site's actual (mis-scoped) export behavior on purpose, so this
  repo's pull matches what a researcher would get by hand.
- Practically: the raw pull contains oil/gas (GOGPT), coal (GCPT), and
  bioenergy (GBPT) units interleaved. `scripts/scope_filter.py` derives the
  GOGPT-only working view, authoritatively via
  `SELECT id FROM powerplant_unit WHERE "trackerSearch" = 'GOGPT'`
  against the read-only Postgres (`GEM_READONLY_DB_URL`), keeping rows whose
  `GEM unit ID` = `"G" + id` is in that set. An offline fuel-token heuristic
  fallback exists (`--offline`) but is approximate — never ship a batch from
  it without re-running DB mode first.
- The **unfiltered** export is kept on disk deliberately: co-located
  coal+gas plants and coal→gas fuel-conversion timepoint chains need the
  GCPT-side rows visible for cross-checks (see `docs/sops/update.md` §9.3).
- 91 columns as of the Oct 2026 export layout (`GOGPT_COLUMNS` in
  `gem_all_fields.py`). Column order and presence can drift between
  releases — `pull_gem_db.py` re-derives the column-index map from the
  header row every pull rather than hard-coding offsets.

## Underlying tables

| Table | Holds |
|---|---|
| `plant` | Project/"location" row. `projectType` (1 = combustion, covers GOGPT+GCPT+GBPT), name, `wikiUrl`, project-level location/captive fields, `plantLevelOwners`/`plantLevelOperators` flags. |
| `powerplant_unit` | Unit/"G" row. `plant_id` FK, `capacity`, `status_id`, `technology` (jsonb), fuel/technology/equipment datasource jsonb blobs, `trackerSearch` (the GOGPT/GCPT/GBPT scope marker), lifecycle year fields, `ownerPrimary_id`/`operatorPrimary_id`. |
| `company` | Entity row (owner/operator/parent). Name, country, `entityType_id`, `gemParents`/`gemParentsIds` (curated ultimate-parent chain — ownership-tracker team maintained). |
| `plant_owner` / `operator` | Owner/operator link rows; each can point at a `plant_id` (project-level) or `powerplant_unit_id` (unit-level), never both. |
| `unit_fuel` | Fuel category/detail rows per unit, with `primary` flag and `timepoint` — the fuel-conversion mechanism (see `datasource_conventions.md` "Fuel conversions"). |
| `status_timeline` | Ordered status history per unit — **not exposed in the flat export**; current `Status`/`Status Detail` only. |
| `plant_external_id` / `unit_external_id` | External-ID rows (`externalId`, `idSystem_id` → `external_id_system`). WEPP is one `idSystem`; everything else lands in the export's "Other IDs" columns. |
| `data_source` | The single central datasource table shared by every GEM tracker (url, shortName, etc.) — see `datasource_conventions.md`. |

## Display IDs

The website renders integer primary keys with a per-tracker prefix
(`gem_all_fields.py` `ID_PREFIX_*` constants):

| Prefix | Table.id | Meaning in GOGPT export |
|---|---|---|
| `L` | `plant.id` | **GEM location ID** — GOGPT's name for the project ID |
| `G` | `powerplant_unit.id` | **GEM unit ID** |
| `E` | `company.id` | **GEM Entity ID** (Owner/Operator/Parent) |
| `T` | `plant.id` | Not used by GOGPT — this is the *same* `plant` table's ID as rendered by the **LNG** tracker ("Terminal"). Seeing a `T`-prefixed ID in GOGPT context (e.g. a co-located project note) still means `plant.id`. |

IDs are DB-assigned; never invent or edit them. `GEM location ID` and
`GEM unit ID` are the join keys for `(Plant name, Unit name)` re-derivation
batch to batch — export row order is not stable.

## Column groups (91 columns)

Canonical list: `GOGPT_COLUMNS` in `gem_all_fields.py`; the canonical-name →
exact-header-string map is `GOGPT_EXPECTED_COLUMNS` in
`gem-db-ops/gem_colmap.py` (this repo's `pull_gem_db.py` only aliases it as
`EXPECTED_COLUMNS`). Grouped here by function rather than reproduced
column-by-column:

- **Record metadata**: `Last Updated`, `Researcher`, `Research status`,
  `Wiki URL` — all DB-computed, see "Read-only columns" below.
- **Identity**: `Country/Area`, `Plant name`, `Plant Name in Local
  Language / Script`, `Other Name(s)`, `Unit name`.
- **Fuel/technology/equipment**: `Fuel` + `Fuel Data Source`, `Number Of
  Engines`, `Capacity Per Engine`, `Capacity (MW)` + `Capacity Data Source`,
  `Turbine/Engine Technology` + ref, `Equipment Manufacturer/Model` + ref,
  `CHP` + ref.
- **Status/lifecycle**: `Status`, `Status Detail`, `Status Data Source`,
  `Disrupted by conflict` + ref (named `Disrupted due to conflict` before Oct 2026), `Latest Activity` + ref, `Cancellation
  year` + ref, `Start year` + ref, `Retired year` + ref, `Planned retire` +
  ref.
- **Conversion/replacement** (fuel-conversion timepoint chain — see
  `datasource_conventions.md`): `Conversion/replacement?`, `Conversion
  from/replacement of (fuel)`, `Conversion from/replacement of (GEM unit
  ID)`, `Conversion/replacement Data Source`, `Conversion to (fuel)`,
  `Conversion to (GEM unit ID)`.
- **Hydrogen lane** (`Hydrogen capable?` through `H2 Criteria Data Source`,
  9 columns): out of scope per the Editing Manual — see "Do-not-research
  columns" below.
- **CCS**: `CCS attachment?` + ref — in scope.
- **Ownership**: `Operator(s)` + ref + `Operator GEM Entity ID`, `Owner(s)`
  + `Owner(s) GEM Entity ID` + ref, `Parent(s)` + `Parent GEM Entity ID`.
- **Location**: `Latitude`, `Longitude`, `Location accuracy`, `Location
  Data Source`, `City`, `Local area (taluk, county)`, `Major area
  (prefecture, district)`, `State/Province`, `Subregion`, `Region`.
- **Other IDs**: `Other IDs (location)`, `Other IDs (unit)` (non-WEPP
  external IDs, `<system>: <id>` joined), `WEPP location ID`, `WEPP unit
  ID` (see "WEPP ID columns" below).
- **Captive power**: `Captive industry use`, `Captive industry type`,
  `Captive non-industry use`, `Captive Data Source`.
- **Misc**: `Notes`, `Employment Notes` + ref, `GEM location ID`, `GEM
  unit ID`, `Linked Projects`.

## Read-only columns (never write these)

Two distinct reasons a column is off-limits — both enforced in
`scripts/schema_constants.py`:

**DB-computed** (`COMPUTED_COLUMNS`) — the backend assigns or derives these;
writing to them is a no-op at best:
```
GEM location ID, GEM unit ID, Wiki URL,
Last Updated, Researcher, Research status,
Operator GEM Entity ID, Owner(s) GEM Entity ID, Parent GEM Entity ID,
Parent(s),          # derived from the owner entity graph (company.gemParents)
Linked Projects,
Owner Share Imputed, Parent Share Imputed,   # Y/blank flags set by the pull
Subregion, Region    # derived from Country/Area
```

**Out of scope** (`OUT_OF_SCOPE_COLUMNS`) — the Editing Manual explicitly
deprioritizes the hydrogen lane; these are researchable in principle but the
family does not research or flag them as missing:
```
Hydrogen capable?, Hydrogen Notes, Hydrogen Data Source,
H2 ready turbine (%)?, MOU for H2 supply?, Contract for H2 supply?,
Financing for supply of H2?, Co-located with electrolyzer/H2 production facility?,
What % of H2 blending currently?, H2 Criteria Data Source
```

`READ_ONLY_COLUMNS` in `schema_constants.py` is the union of both sets.
Everything else in the 91 columns is researcher-editable.

## Entity links (Owner/Operator/Parent)

- `Owner(s)` / `Operator(s)` display strings resolve from `plant_owner` /
  `operator` rows joined to `company.name` (+ legal-entity-type suffix for
  owners). Each link row is plant-level or unit-level per
  `plant.plantLevelOwners` / `plantLevelOperators` — see
  `datasource_conventions.md` for the switch-direction data-loss warning.
- `Owner(s) GEM Entity ID` / `Operator GEM Entity ID` are the parallel
  `E<company.id>` strings, share-annotated the same way as the name column
  (e.g. `E100001234 [40%]`).
- `Parent(s)` / `Parent GEM Entity ID` do **not** come from `company_owner`
  (which would pull in public minority shareholders like index funds).
  They read the curated `company.gemParents` / `gemParentsIds` fields on
  each direct owner — maintained by the ownership-tracker team, never
  edited by a GOGPT researcher. When an owner has no curated parent above
  it, the Parent column falls back to showing the owner itself.
- Before staging any new Owner/Operator/Parent, entity lookup is mandatory
  (`entity_lookup.py`, family rule) — duplicate entities are real cleanup
  debt across the whole DB. See `docs/sops/update.md` §8.

## Datasource `[ref]` / "Data Source" columns

- Every `<Field> Data Source` column resolves a list of `data_source.id`
  values (stored as jsonb on the parent row, e.g.
  `powerplant_unit."capacityDatasource"`) into a comma-joined string of
  `data_source.url` values, in stored order, duplicates preserved.
- `data_source` is one table shared by every GEM tracker — creating a
  datasource on a GOGPT edit makes it reusable anywhere in the DB, and vice
  versa. See `datasource_conventions.md` for short-name conventions and the
  effectively-append-only deletion behavior.
- **URLs live only in these columns** — never embed a URL in a value, name,
  or notes field (family rule, `docs/sops/update.md` §7.2).

## WEPP ID columns

- `external_id_system.name = "WEPP (S&P Global Platts)"` is the one
  external-ID system the export breaks out into dedicated columns:
  `WEPP location ID` (from `plant_external_id`) and `WEPP unit ID` (from
  `unit_external_id`).
- Every other `idSystem` row folds into `Other IDs (location)` / `Other
  IDs (unit)` as `<system name>: <id>` pairs, comma-joined.
- WEPP IDs are S&P Global Platts' own turbine/unit-level identifiers —
  useful for reconciling GOGPT units against WEPP rows (WEPP is turbine-
  granular; GOGPT/GGPT combines turbines into one row for a combined-cycle
  set). See `docs/reference/source_roster.md` for the WEPP `UTYPE`
  reconciliation guidance.

## Schema drift

`pull_gem_db.py` re-derives the column-index map from the CSV header on
every pull (`derive_column_map`) rather than trusting fixed offsets, and
flags: (a) an expected-column entry missing from the header — likely
renamed, check the live DB unit-edit page; (b) an unrecognized header
column — new field, decide in-scope vs. backend-only. Add newly-appearing
columns to `GOGPT_EXPECTED_COLUMNS` in `gem-db-ops/gem_colmap.py` (NOT here —
that map is shared with the pull engine), update `COMPUTED_COLUMNS`/
`OUT_OF_SCOPE_COLUMNS` (`schema_constants.py`) in the same pass, and note the
change here.
