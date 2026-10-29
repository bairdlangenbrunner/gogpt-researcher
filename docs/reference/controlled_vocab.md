# Controlled Vocabulary — Fuels, Technology, Capacity, Ownership

Distilled from the GOGPT Editing Manual (September 2026); updated 2026-10-27.

Covers the fuel category/detail dropdowns, the technology abbreviations, capacity
inclusion and rounding rules, ownership-percentage rules, captive-plant fields, the
CCS/CHP "yes"/"not found" convention, and the hydrogen fields that are explicitly
out of scope. `scripts/schema_constants.py` is the machine-readable copy of these
vocabularies — see "Casing: manual vs. export vs. schema_constants.py" below for how the
two are kept in sync. See `lifecycle_rules.md` for the `Status` vocabulary and
`unit_conventions.md` for how these fields split across plant vs. unit level.

## Fuel categories and details

Choose **Fuel Category** first — it filters which **Fuel Detail** options are available.
If fuel-detail data isn't available, select "unknown".

### Fossil gas

- **Natural gas** — the main fuel GOGPT tracks.
- **LNG** — liquefied natural gas. In practice LNG is regasified and piped to plants as
  gas, but GOGPT tries to distinguish plants specifically supplied as "LNG" power plants.
- **Coalbed methane** — natural gas extracted from coal seams.
- **Gaseous propane** — propane in gas form, used as fuel or feedstock.
- **Waste heat from natural gas** — heat recovered from combustion/processing, used for
  energy. Technology should be `steam turbine` for this fuel; typically only seen when a
  simple-cycle plant is upgraded to combined cycle — once the CC is operating, all units
  combine into a single CC unit (see `unit_conventions.md`).
- Associated gas (a byproduct of oil extraction) is classified as **natural gas**.

### Fossil liquids

Crude oil, diesel, fuel oil (FO), gasoline, heavy fuel oil (HFO), jet fuel, kerosene,
light fuel oil (LFO), liquefied petroleum gas, naphtha, petroleum coke, waste/other oil.

### Industrial by-product

Blast furnace gas (BFG), coke oven gas (COG).

### Other

Hydrogen (all types) — see "Hydrogen: do not research" below; the fuel-category dropdown
value exists, but the associated Hydrogen research fields are out of scope.

### Single- vs. dual-fuel units and the Primary checkbox

- For a dual-fuel unit, one fuel must be natural gas or oil.
- Check **Primary** only when a unit has **more than one fuel** — and only for one of
  them. Whichever fuel is listed first, or the source emphasizes, is primary.
- If the two fuels route to the **same tracker** (e.g. gas + oil, both GOGPT), it's fine
  to leave Primary unchecked if the primary fuel isn't clear.
- If the two fuels route to **different trackers** (e.g. coal vs. gas), Primary must be
  set — it's what assigns the unit to the correct tracker in an ambiguous case.
- If a source mentions a future fuel-supply shift (e.g. "will be 100% LNG once terminal X
  opens in 2025"), stage that as a **conversion** (see `unit_conventions.md`) and note the
  detail in Status Details rather than changing Primary preemptively.

## Technology vocabulary

| Code | Meaning |
|---|---|
| `CC` | Combined Cycle — GT exhaust captured by HRSG to raise steam for a steam turbine. |
| `GT` | Gas turbine — standard (frame-type), simple/open cycle, no exhaust recapture. Sometimes called "turbogenerator". |
| `AGT` | Aeroderivative Gas Turbine — derived from aircraft jet-engine technology, adapted for stationary/industrial use; lightweight, compact, fast start/ramp, well suited to peaking/backup/flexible support; typically fossil gas or liquid fuel, smaller than a standard GT. |
| `ST` | Steam turbine — steam drives the blades. |
| `IC` | Internal combustion (reciprocating engines) — piston movement runs a crankshaft to the generator; individually small (often <20 MW) but frequently deployed in large sets. Add if the set's total capacity is ≥50 MW. |
| `ICCC` | Internal Combustion engine in Combined Cycle — an IC engine set contributing to the steam turbine of a combined-cycle gas plant. |
| `ISCC` | Integrated Solar Combined Cycle — the solar component is thermal (not PV); collected heat produces steam. |
| `AFC` | Allam-Fetvedt Cycle — recycles exhaust heat, eliminates air emissions including CO2, produces pipeline-quality CO2 as a byproduct that can be sequestered. |

If unit technology is unavailable, select "unknown".

## Capacity rules

- **Inclusion threshold: ≥50 MW nameplate/installed capacity**, per unit or per IC/AGT
  set. **EU and UK exception: ≥20 MW per unit.**
- Capacity fields hold **nameplate or installed electrical capacity in MW (MWe), never MWt (thermal)**. The manual's "generating capacity" is the lower operational figure and is not what GEM records; see the captive-plant note in `unit_conventions.md` on shaft/mechanical capacity.
  Watch specifically for thermal-capacity figures ("MWt") being entered into the
  electrical Capacity (MW) field by mistake.
- **Ranges**: if a source gives a capacity range, record the **high end** of the range —
  don't enter the range itself. This commonly arises for undecided proposed capacities, or
  net-vs-gross comparisons.
- **Rounding is optional** (manual, Precision of Capacity Data): record the figure the source gives, at most one decimal. Rounding to the whole MW (294.7 MW to 295 MW) is allowed, never required.
- **No breakdown available**: if you can't find a unit-by-unit breakdown but know the
  total plant capacity, stage one unit with the total (to be split later). If you know the
  number of units but not each one's capacity, you can assume an even average (e.g. a
  2000 MW plant with 4 CC units → 500 MW average per unit).
- **IC engine sets / AGT sets**: capacity is not entered directly. Enter Number of Engines/Turbines and Capacity of Engine/Turbine (MW); total Capacity (MW) is calculated and isn't directly editable.
- **Standard (non-aeroderivative) GT units**: enter total capacity directly in Capacity
  (MW), since only one turbine is entered per unit.
- If capacity can't be found at all, leave the field blank — "not found" is not a valid
  Capacity value (numeric only). If it later turns out to be below the 50/20 MW threshold,
  the unit can be removed then.

## Ownership rules

- Record ownership stakes of **5% or higher only**. Owners each below 5% are summed and
  recorded collectively as **"small shareholder(s)"**.
- An individual (natural person) owning ≥5% is entered as **"natural person(s)"** — never
  by name. Multiple qualifying individuals can be grouped into one "natural person(s)"
  entry.
- **Multiple owners with reported shares**: list the **four largest** explicitly, then use
  a final **"other"** entry for the remaining aggregate percentage.
- **SPVs** (special-purpose vehicles set up solely to own the one project) are acceptable
  as the recorded owner — no need to trace up to a "real" parent company.
- Aim for the **immediate/lowest-level owner**, but it's fine to use whatever owner is
  named in a readily available document (government dataset, company annual report) —
  don't spend research time chasing a lower-tier subsidiary once a company is already
  documented as owner.
- **Never enter a national government directly as owner.** If the national government is
  listed as the owner, find the specific government entity (ministry, state-owned company,
  etc.) that actually owns the plant instead — this preserves the distinction between,
  say, the entity that owns power plants vs. the one that owns pipelines vs. the one that
  owns oil fields, rather than collapsing everything to "the government."
- **Percentage**: enter 100% explicitly for a single confirmed owner (don't leave blank to imply full ownership). If ownership shares aren't reported, list owner names with percentages blank.
- **Unknown owner**: record the owner as **"unknown"** when ownership is unknown. For a very new or vague proposal where you cannot find the owner, leave the owner field blank (manual, Owner section).
- **Equal-share cases** (e.g. 10 companies each owning 10%): list the largest or best-known company or companies by name and group the rest as "other". This should be rare; ask the PM if unsure how to split a given case.
- **Pending acquisition or merger**: note it in the Notes field, add it to the "GEM Trackers - possible updates" sheet, and revisit the plant in the next cycle. Do not change the owner until the transaction closes.
- The company that buys the power (a PPA counterparty) is not the owner.
- **Operator** ≠ owner. Only record an operator when a source states one explicitly and it
  differs from the lowest-level owner; don't search for it specifically.

## Name, language and project fields

- **Name (Other)**: record any variation of the plant's name in English, so the plant is not duplicated under a very different name.
- **Language** and **Local Name**: add the plant's name in the local language, or in another language if the plant is known by a different name elsewhere (for example Ukrainian or Russian names).
- **Project Links**: the names of related projects, such as the LNG terminal an LNG power station serves or the data center a plant will supply (manual, Project Links section).
- **Fuel Percentage**: fill it only when a unit burns more than one fuel; leave it blank when the data is not available.
- **Research status**: choose "added" for a new unit or phase, "in progress" for a unit you started and did not finish, and "updated" or "no changes" when done (see `lifecycle_rules.md`).
- **Disrupted due to conflict** is the label of the checkbox between Status and Status Detail (see `lifecycle_rules.md`).

## Captive fields

| Field | Values / notes |
|---|---|
| Captive Industry Type | Industry served by the plant, or "unknown" if no data. Filled for every captive plant, including one that exports power. |
| Captive Data Source | Reference link(s) supporting the captive classification. |
| Captive Industry Use | `heat`, `power`, or `both` — if data is available. |
| Captive Non-Industry Use | `heat`, `power`, `both`, or `none` — covers cases like grid electricity sales or heat supplied to nearby homes/facilities. |
| Emergency/Backup (Backup Power in the export) | Unit-level only; appears only when Captive + Industry Type = "Data Centre" is set at the unit level. Check it when the unit is an emergency or backup generator for the data center. Backup units at data centers are captive units and are tracked (50 MW summed, 20 MW in the EU and UK). Do NOT check it if the unit provides primary or routine power. |

Captive plants may sell a large share of their power outside; Captive Non-Industry Use records that, so the captive fields are filled for an exporting plant too.



## CCS and CHP: the "yes" / "not found" convention

Both CCS (carbon capture and storage) and CHP (combined heat & power / cogeneration) are
optional unit-level fields that follow the **same convention**:

- Sources almost always state it **when present**, rarely state it when absent — so most
  entries land on **"yes"** or **"not found"**.
- Select **"no" only** when a comprehensive dataset (e.g. a government source)
  **explicitly** specifies the plant does not have CCS / is not CHP. Don't infer "no" from
  silence.
- CCS can apply to any combustion plant but is uncommon (expensive technology). CHP is
  widespread in Europe, South Korea, and Russia — check local/country-specific
  terminology for CHP or cogeneration before concluding a plant lacks it.
- CHP note: watch that **thermal capacity (MWt) is never entered into the electrical
  Capacity (MW) field** — see "Capacity rules" above.

## Hydrogen: do not research

The Hydrogen field group is explicitly **out of scope** — do not research or populate it.
This matches `OUT_OF_SCOPE_COLUMNS` in `scripts/schema_constants.py` (`Hydrogen capable?`,
`Hydrogen Notes`, `Hydrogen Data Source`, `H2 ready turbine (%)?`, `MOU for H2 supply?`,
`Contract for H2 supply?`, `Financing for supply of H2?`, `Co-located with
electrolyzer/H2 production facility?`, `What % of H2 blending currently?`, `H2 Criteria
Data Source`). Hydrogen still exists as a **Fuel Category/Detail** value (see "Fuel
categories and details" above) — that part of the fuel taxonomy is in scope; it's only
the dedicated Hydrogen field group that's deprioritized.

## Casing: manual vs. export vs. schema_constants.py

`scripts/schema_constants.py` is the machine-readable copy of the vocabularies on this
page — the enum sets it exposes (`STATUSES`, `TECHNOLOGIES`, `GOGPT_FUELS`,
`FUELS_FOSSIL_GAS`, `FUELS_FOSSIL_LIQUIDS`, `FUELS_BYPRODUCT`, etc.) are what
`pull_gem_db.py`, `scope_filter.py`, `worklist.py`, and `qc_checks.py` actually validate
against, not this document.

Casing is not always consistent between sources: this manual's own tables use Title Case
(e.g. "Announced", "Shelved - inferred 2 y"), while `schema_constants.py` stores the
`Status` vocabulary lowercase (`announced`, `shelved - inferred 2 y`) to match the live
database export. **When the manual and a fresh export disagree on casing or spelling, the
export wins** — compare case-insensitively, and update `schema_constants.py` (not this
doc's prose) to match whatever the current export actually displays. Don't assume Title
Case or ALL CAPS for any dropdown field without checking a live row first.

Three stored-form facts confirmed against the live export (2026-07-27):

- **Inferred statuses use a plain hyphen**: `shelved - inferred 2 y` /
  `cancelled - inferred 4 y` (the manual's PDF rendering shows an en-dash;
  `schema_constants.py` accepts both).
- **Technology is stored long-form** for the common types (`combined cycle`,
  `gas turbine`, `steam turbine`, `internal combustion`, `unknown`) and abbreviated only
  for the rare ones (`ICCC`, `ISCC`, `AFC`) — see `TECHNOLOGY_LONG_FORMS`. This doc's
  abbreviation table is the manual's shorthand, not the stored value.
- **Fuel cells are comma-separated `category: detail` tokens**
  (`fossil gas: natural gas, fossil liquids: fuel oil`). Scope is decided by category
  (`GOGPT_FUEL_CATEGORIES`); a mixed cell with a coal/bioenergy token alongside a GOGPT
  fuel is legitimate co-firing, not a scope leak.

## Cross-references

- `lifecycle_rules.md` — the `Status` vocabulary and inferred-status thresholds that
  `schema_constants.py` encodes as `STATUSES_NO_START_YEAR`, `SHELVED_INFERRED_YEARS`,
  `CANCELLED_INFERRED_YEARS`.
- `unit_conventions.md` — how Technology, Fuel, and Capacity fields split across
  plant-level vs. unit-level entry, and the CC/IC/AGT "one unit" grouping rules that
  capacity entry depends on.
- `datasource_conventions.md` — datasource requirements for any of the fields above when
  a value changes (a status, fuel, technology, capacity, or owner change always needs an
  attached datasource).
