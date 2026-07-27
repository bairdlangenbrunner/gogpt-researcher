# Unit Conventions — Unit Definition, Naming, and Conversions

Distilled from the GOGPT Editing Manual (March 2026); fetched 2026-07-27.

Covers what counts as one GOGPT "unit," the naming conventions for numbering, blocks,
phases, replacements, and IRP units, which fields live at plant level vs. unit level,
co-located coal/gas plants, conversion vs. replacement (and how conversions link across
records), and captive-plant capacity scope. See `lifecycle_rules.md` for how status and
year fields interact with these unit records, and `controlled_vocab.md` for the
technology and fuel vocabularies referenced below.

## What counts as one unit

A unit is a technology (or group of technologies) that operates as a single system:

- **A combined-cycle block is one unit**, even though it's a combination of gas
  turbine(s), steam turbine, and heat-recovery (HRSG) technology working together as one
  system. Multiple CC blocks at a plant ("blocks") each get their own unit entry — but if
  a source describes gas + steam turbines running in combined cycle without explaining the
  block arrangement, stage it as **one CC unit with the whole capacity**; split it later
  if a per-block capacity breakdown turns up.
- **A gas turbine is its own unit** if it is not part of a combined-cycle system.
  **A steam turbine is its own unit** on the same condition.
- **Internal combustion (IC) engine sets and aeroderivative gas turbine (AGT) sets are
  entered as one unit for the whole set**, not one unit per engine/turbine: use "Number of
  Engines/Turbines" for the count and "Capacity of Engine/Turbine (MW)" for the per-unit
  figure. Total "Capacity (MW)" is auto-calculated from those two and is not directly
  editable.
- Standard (open-frame, non-aeroderivative) gas turbines are the opposite case: enter only
  **one turbine per unit**, with its total capacity in the "Capacity (MW)" field directly.
- One "power station" can contain more than one "power plant" (e.g. "Ballylumford A/B/C,"
  or Roman-numeral-differentiated plants, sometimes called "blocks") — don't assume
  power station and power plant are always synonymous.

## Unit naming conventions

- **Default: plain numbers** (1, 2, 3…) for the unit name.
- If a source (company report, etc.) gives its own designated numbers, use theirs even if
  the order looks unusual (e.g. starts at 4). Convert Roman numerals to Arabic numbers. If
  the source uses a different unique identifier format, use that format instead.
- Proposed plant / minimal info, unit count unknown: enter unit name **"1"**. Rename once
  better information becomes available.
- **Blocks**: preface the unit number with the block number and a dash — `1-1`, `1-2`,
  `1-3`, then `2-1`, `2-2`… (restart numbering at 1 for each block). Don't include the word
  "Block" in the name.
- **Phases**: if a plant is built in distinct phases (e.g. two IC-engine sets with
  different start years), name units `Phase 1`, `Phase 2`, etc.
- **"R" replacement suffix**: when a new turbine/unit replaces an old one (old one is not
  kept), append `R` to the unit name — e.g. old unit `5` retires, new unit is named `5R`.
  See "Conversion vs. replacement" below.
- **"IRP" suffix**: a unit that appears in Integrated Resource Plan data but doesn't yet
  meet the detail threshold for the public data release gets `IRP` appended to the unit
  name (e.g. `1 IRP`, `2 IRP`), status `announced`, and the IRP checkbox checked. Once a
  unit crosses the detail threshold for `announced`-or-beyond, the IRP checkbox stays
  checked but the **name drops the "IRP" suffix** — see "IRP" fields note below.
- **Avoid "CC"/"ST" in the unit name** by default — that's what the Technology field is
  for. **Exception**: at bigger stations mixing older simple-cycle steam/gas turbines with
  newer combined-cycle units, prefacing with the technology type to disambiguate is fine —
  `ST1`, `GT1`, `CC1`. For a combined-cycle unit assembled from parts each named
  separately in a source (GT, HRSG, ST), collapse it to one unit named `1` or `CC1`.
- **Combined-cycle unit built up from prior GT/ST units**: when the CC becomes
  operational, replace the separate `GT1`/`ST1` unit entries with one new `CC1` unit and
  give it its own new start year (do not keep `GT1`/`ST1` as separate live units once the
  CC unit is combined).
- All unit names within one plant must stay unambiguous — see "Co-located coal and gas
  units" below for the naming overlap rule when a plant tracks in two trackers.

## Plant-level vs. unit-level fields

- **Location is plant-level by default.** Even though units within one "complex" or
  development can be in physically different spots, the whole power station is treated as
  one location — GOGPT does not differentiate unit-level locations within a plant.
- **Owner** and **Operator** can each be set at plant level or unit/phase level; in most
  cases the same owner/operator applies to the whole plant, so plant-level is the default
  and unit-level is the exception (e.g. a plant where different units have different
  owners).
- **Captive** fields (industry type, industry use, non-industry use) are entered at plant
  level, except the **Emergency/Backup** checkbox, which is unit-level only and requires
  the captive-data-center data to also be entered at the unit level even if it's already
  present at the plant level (this is what reveals the checkbox).

## Co-located coal and gas units

Some power plants have both coal-fired and gas-fired units. These plants are tracked in
**both** GCPT (coal) and GOGPT (gas/oil) trackers, but each individual unit appears in
only one tracker, based on its fuel. All units at such a plant share the **same Project
ID and the same wiki URL** across trackers.

- Keep new gas-unit naming consistent with existing coal-unit naming when no official
  names are available — e.g. a coal plant with operating "Unit 1" gets a new gas unit
  named "Unit 2".
- **Gas unit names must not overlap coal unit names.** If a coal plant already has "Unit
  1" and the official name of a newly-added gas unit is also "1", rename the gas unit
  (e.g. "GT1" or otherwise disambiguated) rather than duplicating "1".
- Validation errors on the coal-fired side of a co-located plant (missing datasource for
  location/owner, etc.) are optional to fix — not a priority, per
  `datasource_conventions.md`.

## Conversion vs. replacement

GOGPT tracks fuel **conversion** — modifying an existing unit to run on a different
primary fuel than originally designed — as distinct from **replacement** (a new
turbine/unit installed and the old one retired, "R" suffix, see above). Conversion types
tracked:

- Full conversion from coal to gas (most common).
- Full conversion between two GOGPT-tracked fuels (e.g. gas to oil, gas to hydrogen).
- Partial conversion from coal to gas where gas becomes the primary fuel (the unit already
  burns both; this is staged as a conversion because the unit transfers from GCPT to
  GOGPT).

If a unit already burns multiple fuels and only the *primary* fuel designation is
changing, no conversion record is needed — just move the "Primary" checkbox under
Technical Details to the new fuel. Only stage an actual conversion when one fuel fully
replaces another.

**Coal-to-gas conversion vs. coal-to-gas replacement** — don't conflate the two:

- **Conversion**: the boiler of a coal-fired steam plant is converted to burn gas, possibly
  along with repowering into combined cycle (adding gas turbine(s) + HRSG to the existing
  steam turbine). For the converting coal unit, set "Type (replacement/change)" to **"use
  of ST in CC set"** and add the Unit ID of the new combined-cycle unit.
- **Replacement**: the coal-fired plant is retired outright and replaced by a new,
  separate gas-fired plant. This is a normal replacement ("R" suffix / Replacement
  workflow), not a conversion timepoint.

### Timepoint linking mechanism

Since conversions are staged as linked records (see `datasource_conventions.md`'s "Fuel
conversions (timepoint mechanics)" section for the full procedure), the GOGPT-specific
steps are:

1. Rename the existing (pre-conversion) unit to append `, timepoint 1` to its name. Make
   no other changes to that unit in GCPT or any other tracker besides GOGPT.
2. Clone that unit ("Clone this Unit") — creates a new unit record/ID, auto-named `Clone
   of <name>, timepoint 1`.
3. Rename the clone to `<name>, timepoint 2`.
4. On the timepoint-2 unit, use the **"converted from"** dropdown to select the timepoint-1
   unit — this is what links the two records as a conversion pair (surfaced via the
   linked-timepoints table and the **GEM unit ID** columns).
5. For an already-completed conversion (e.g. already converted from coal to gas), confirm
   the old unit is marked `retired` in the other tracker (e.g. GCPT) and add the new unit
   to GOGPT as `operating`. The gas unit's start year should not precede the coal unit's
   retired year — in most cases they're the same year.

## Captive plants

Captive plants are in GOGPT's scope. A captive plant sits within an industrial facility
and primarily supplies power (and, for CHP captive plants, heat) to that facility; it may
also export a portion of power/heat externally (grid sales, nearby industrial heat
supply) — see Captive Industry Use / Captive Non-Industry Use in `controlled_vocab.md`.

**Only GENERATING capacity (electrical, MWe) is in scope for the Capacity (MW) field —
never shaft or mechanical-drive capacity.** GOGPT tracks power *generation*: a captive gas
turbine or engine that drives a compressor or other mechanical load directly (shaft power,
no generator) is out of scope for the Capacity field even if co-located with generating
units on the same industrial site. This follows the same generating-vs-nameplate-vs-
installed distinction the manual draws for capacity generally (see `controlled_vocab.md`)
— GOGPT's capacity fields are always the electricity-generating figure, not a thermal or
mechanical one.

## Cross-references

- `lifecycle_rules.md` — status/year handling for replaced units, and how a converted
  unit's `retired`/`operating` statuses line up across the old and new records.
- `controlled_vocab.md` — Technology vocabulary (CC/GT/AGT/ST/IC/ICCC/ISCC/AFC), capacity
  thresholds and rounding, captive-field dropdown values.
- `datasource_conventions.md` — the full fuel-conversion timepoint procedure (naming,
  cloning, "converted from" dropdown) and general plant-level vs. unit-level field
  behavior in the DB UI.
