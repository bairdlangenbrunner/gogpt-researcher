# GEM Project Database: Datasource, Ownership, Location & Fuel-Conversion Conventions

Distilled from: GEM Project Database Manual (Google Doc ID 1mXWow4Q_7qU3s5KPHw34RvnZ_SjEhYNAB5ygS2oaNTs), fetched 2026-07-27

This covers what a researcher staging edits for the GOGPT needs to know before those
edits are applied by hand in the live DB UI (gem-project-db.herokuapp.com). It skips
pure button/screenshot walkthroughs and focuses on rules, required values, and data
that must be prepared in advance.

## Terminology

- **Project**: the DB's tracker-agnostic term for a plant/power station/wind or solar
  project/etc. Combustion trackers (coal, gas/oil, bioenergy) still call the top-level
  thing a "plant" informally, but in the DB it is a "project."
- **Unit / phase**: the sub-parts of a project. Combustion trackers use "unit"; wind/solar
  use "phase." Different trackers are allowed to keep their own terminology.
- **Entity**: any company, government, or government agency that can be an owner —
  DB-wide terminology from the Beneficial Ownership Data Standard.

## Datasources

- Every data point that changes (a status, capacity, technology, owner, fuel, etc.)
  MUST have a datasource attached. Exception: fixing a typo or non-substantive correction
  doesn't require a new/updated datasource.
- **Datasources are stored in one central table shared by every GEM tracker** — not
  per-project or per-tracker. Adding one makes it available for reuse anywhere in the DB.
- Attaching a datasource to a field opens a search pop-up. You can search by URL or by
  short name against all datasources already in the DB before creating a new one.
- Two ways to create a new datasource from a URL:
  - **"Create New Datasource From Citoid"** — Citoid (same tool used by GEM's wiki and
    Wikipedia) auto-fetches and fills in reference details from the URL.
  - **"New Datasource"** — build one from scratch (also fine to just paste a bare URL;
    additional bibliographic detail is optional).
- **Browser language must be set to English.** Adding new datasources behaves incorrectly
  otherwise (and other interactions may too).

### Short names

- Creating a datasource from a URL auto-generates a short name from the URL's domain plus
  an internal ID, e.g. `eia-13464`.
- The short name is editable and searchable, and it **MUST be unique across the entire
  database** (all trackers) — the UI blocks reuse of an existing short name.
- Edit the auto-generated short name to something memorable whenever a source will be
  reused, especially when multiple documents/editions live at the same URL (e.g. an
  annual report or dataset republished yearly at one unchanging link). The documented
  example: EIA's Form 860 is published yearly at the same URL, so the auto short name
  `eia-13464` gets manually renamed to something like `EIA 2023` to identify the specific
  edition. Follow the same `<org/domain> <year>` (or `<org>-<year>-<doc-type>`, e.g. an
  annual-report abbreviation) style so a short name is unambiguous and reusable across
  projects.
- Reasoning for reusing rather than duplicating: linking straight to a specific file
  (e.g. a zip download) is less useful to wiki/DB readers than linking to the source's
  landing page, so multiple editions intentionally share one URL and are disambiguated
  by short name instead.

### Reusing datasources on a project

- Once a project has at least one datasource attached, the "add datasource" pop-up shows
  a **"Currently used Datasources"** list for that project — click **"Use"** to reattach
  one instead of re-searching.
- To attach a different one, paste a URL or type a short name above that list to check
  whether it already exists in the DB before creating a new entry.

### Datasources are effectively never deleted

- The manual describes delete-with-confirmation for units/phases, projects, entities, and
  individual owner rows — but **no delete function for datasources at all**. Given they are
  a single table shared across every GEM tracker, treat them as append-only: when a fact
  changes, attach/create a new datasource for the new fact rather than trying to remove or
  overwrite an old one. An outdated datasource staying attached to historical data is
  expected, not a bug to clean up.
- General DB-wide caution: there is no "undo" for saved changes (only unsaved text-field
  edits can be Cmd/Ctrl+Z'd before you click away). Anything deleted is retained in DB
  history but is hard to recover — deletion should not be routine.

## Owners, operators, and entities

- **Operator** = the company running day-to-day operations (almost always one company).
  Per-tracker guidance: for gas plants, only add the operator if it differs from the owner.
  Operator can be set at plant level or unit/phase level.
- **Owner** = the most direct owner you can find evidence for. Do not spend research time
  chasing the true lowest-level legal owner (e.g. a local subsidiary or SPV) if you already
  have a company documented as owner one level up — GEM's ownership-tracker workflow is
  responsible for tracing ownership *up* to parent companies, not down to the lowest tier.
  For combustion trackers (coal, gas/oil, bioenergy) it is fine to enter an SPV itself as
  the owner.
- **Percentage ownership**: enter it whenever known. If there is only one owner, enter
  `100%` explicitly (never leave blank to imply full ownership). If an owner's share is
  unknown, leave that owner's share field blank. If only a subset of owners is known,
  add an extra owner row using the entity **"unknown"** (entity ID `E100000132388`) for the
  unknown remainder, with no datasource.
- **Owner datasource requirement**: the citation must specifically show that company owns
  *this* project — not just a general company-info page. (This also rules out generic QCC
  company listings, which don't tie a company to a specific project.)

### Finding/creating entities

- Before creating a new entity, search the existing entity table using name variations —
  search requires exact spelling and word order (though spacing is ignored), and it
  excludes legal-entity-type suffixes (drop "Co Ltd," "Corp," "Inc," etc. from the search
  term). Abbreviations and local-language names are also searchable.
- New entity — only **Name** is required. Other fields:
  - **Legal entity type**: split out from the name when possible (e.g. name = "ExxonMobil",
    legal entity type = "Corp"); if the right value isn't in the dropdown, leave the type
    embedded in the name for now rather than guessing.
  - **Abbreviation**: shortened form/acronym, kept out of the Name field.
  - **Name Other**: additional alternate names — one per entry (green + to add another),
    never comma-separated in a single field.
  - **China companies**: enter only the official Chinese name (e.g. as found on QCC) in
    "Name" and leave everything else blank; an automated QCC-based process later fills in
    the English "Name" and moves the Chinese name to "Local Name."
  - **IMPORTANT**: if you're researching for an infrastructure tracker (e.g. GOGPT, not the
    ownership tracker), leave every other field blank — IDs, "interested parties"/parents,
    notes, etc. are the ownership-tracker team's job to fill in later.
- **Never edit the ownership tree or "Parents" line** for an entity — that is generated/
  maintained by the ownership-tracker team, not by tracker researchers.
- **Deleting an entity**: only possible if it is not currently attached to any owner
  field; an attached entity must be reconciled (reassigned/detached) first.

## Location

- Required: coordinates **or** other location details (city/state/etc.) — at least one is
  mandatory; both is fine.
- No auto-fill between the two (coordinates ↔ place-name details) inside the UI; that only
  happens via a separate offline data-team process on request.
- **Coordinate Format**: `WGS 84 decimal` (default), `WGS 84 degrees-minutes-seconds`, or
  `Other` (with a free-text field for the system name).
- **Coordinate Accuracy**: required whenever coordinates are entered — `exact` or
  `approximate`. If `exact`, latitude/longitude must have at least 3 decimal places.
- Place-detail hierarchy, smallest to largest: Street Address → City → Local Area (county)
  → Major Area (district) → Subnational (state/province) → Country.
- **Plant-level vs. unit-level**: Owner, Operator, and Location can each be stored at the
  project level or pushed down to unit/phase level. Switching plant-level → unit-level
  copies the existing plant-level data down into each unit/phase. **Switching back from
  unit-level → plant-level DELETES all unit-level data for that field** (there's a
  confirmation prompt, but there is no automated reconciliation of differing per-unit
  values) — never do this switch as a casual toggle.

## Technical details (combustion units — coal/gas/oil/bioenergy)

- **Fuels**: choose "fuel category" (coal, gas, bioenergy, ...) before "fuel details" —
  the fuel-detail options depend on the category chosen first. Multiple fuels per unit are
  allowed (green + to add rows). Attach a "Fuel Datasource" (multiple allowed).
  - **Primary fuel** checkbox: only check it when a unit has more than one fuel AND those
    fuels would route to *different* trackers (e.g. coal vs. gas) — marking primary is
    what assigns the unit to the correct tracker in an ambiguous case. If multiple fuels
    all belong to the same tracker (e.g. gas + oil, both GOGPT), leave primary unchecked
    unless it's actually known.
- **Equipment** (gas/oil only): Equipment Manufacturer (dropdown, or type a new one) and
  Model (free text, e.g. "9HA").
- **Technology**: choose fuel category(ies) first — technology options are filtered by
  fuel category, so entering technology first risks an inconsistent combination. Attach a
  datasource.
- **Capacity**: numeric only — "not found" is not an accepted value (rare cases where
  capacity truly isn't known should go in a comment on that field or the project Notes,
  not in the capacity field itself).
  - **Internal combustion** technology is a special case: enter the whole engine set as
    one "unit," with "Number of engines" and "Capacity of engine (MW)" as inputs; total
    "Capacity (MW)" is auto-calculated and not directly editable.
  - Combined-cycle sets: enter total capacity for the whole set (all turbines combined).

## Fuel conversions (timepoint mechanics)

Since May 2024, each stage of a unit's fuel conversion (e.g. coal → gas) is its own unit
record in the DB, linked together as "timepoints." This directly affects how a researcher
must stage a conversion edit.

- **Naming convention**: `<Unit name>, timepoint 1`, `<Unit name>, timepoint 2`, etc.
  (comma-separated from the original unit name).
- **Procedure to add a conversion to an existing unit**:
  1. Rename the existing unit to append `, timepoint 1`.
  2. On that unit, click **"Clone this Unit"** — this creates a new unit record with a new
     unit ID, all data copied from timepoint 1, auto-named `Clone of <Unit name>, timepoint 1`.
  3. Rename the clone to `<Unit name>, timepoint 2`.
  4. On the new (timepoint 2) unit, use the "converted from" dropdown to select the unit it
     was converted from (timepoint 1). Selecting this links both records as a fuel-conversion
     pair.
     - If the prior fuel/timepoint isn't known or isn't in the DB, select **"unknown"** in
       that dropdown instead — the new unit then behaves as a fully standalone unit (all
       fields editable, no inheritance), since there's no earlier timepoint to draw from.
  5. Once linked, only specific fields are editable directly on timepoint 2+: fuel/
     technology/capacity/equipment (technical details), status, latest-activity details,
     and start/retired/cancellation year. **Owner and location are inherited from timepoint 1**
     (when those are set at the unit level) and are not independently editable on later
     timepoints.
- **More than two timepoints**: every additional timepoint's "converted from" dropdown can
  only point back to **timepoint 1** (not to the immediately preceding timepoint) — this is
  a DB implementation limitation, not a data-order choice. The naming convention alone
  conveys chronological order to readers.
- A linked-timepoints table auto-renders at the bottom of each involved unit's page,
  showing every timepoint in the chain, with the currently-viewed one highlighted.
- To find all conversion-linked units: on the unit search page, check **"In Conversion"**.
