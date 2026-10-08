# United States

Largest single-country fleet in scope; EIA is the backbone data source, with
a long tail of supplementary trackers and news sources for keeping pace with
retirements/additions between EIA release cycles.

**Research is organised per state** — Q4 2026 assignments, priority levels and
days are per `United States - <State>` row on the assignments tab, and state
files live in `united_states/` (start with `united_states/texas.md`). This
file holds what is true of every state.

## US-specific rules (Q4 2026; from the US Data/Research Guide + kickoff doc)

- **IDs are the join keys — filling them is in scope.** Other IDs (location) =
  EIA plant ID (system name as already used in the export); Other IDs (unit) =
  EIA-860M Generator ID(s), comma-joined for a CC block; EIP (Oil & Gas Watch)
  record IDs also live in Other IDs (location). Match every GEM plant to
  EIA-860M, EIP and the Sierra Club sheet during the state pass:
  `scripts/match_ids.py --state <State>` does the join and writes
  `work/ids_us-<st>.md` (Update SOP §3 step 7, `docs/workflows.md` §7).
  - EIA-860M: `scripts/eia860m.py --check` keeps the newest monthly file in
    `work/eia/` (release dates are on the EIA-860M page; a new file comes
    out about monthly, so check at the start of a US batch). EIA sometimes
    splits one site into two plant codes when part of it changes hands or
    retires (Chalk Point 65285 coal and 1571 gas); a GEM plant can hold both.
  - EIP: the GEM-held "EIP_GEM IDs matched" sheet (link in
    `docs/reference/sop_pointers.md`), newest "EIP <date> data filtered" tab.
    EIP's `facility__id` goes in Other IDs (location) as `EIP: <id>`; the
    public page is `oilandgaswatch.org/facility/<id>`. The sheet's own GEM
    ID columns record the match, so a blank one is a row for Baird to fill.
  - Sierra Club: the "MATCHED IDs" tab of the GEM-IDs-matched sheet, joined by
    its GEM Location ID and GEM Unit ID columns, else by ORIS code (the EIA
    plant id). It carries terminated proposals at existing GEM sites with a
    location id but no unit; those come back as a whole-plant question.
- **Sierra Club GEM-IDs-matched sheet is reference only** — use it to find
  plants and cross-check IDs, never cite it, never share it outside GEM.
- **IRPs**: a unit that appears in a utility Integrated Resource Plan gets the
  IRP checkbox and, where the unit is only known from the IRP, the "IRP"
  suffix in its unit name; log the IRP on the US IRPs tab. The step is
  scripted: `irp_sheet.py --state <State>` reads the tab (one row per
  utility: plan year, plan links, a running Notes log) and the export's
  `IRP` column (the checkbox, yes or no), `build_state_brief.py --irp`
  briefs the matched plants and the scope-wide agent, and the build's
  `--irp` lists the boxes to tick and a draft Notes line per utility to
  paste by hand (Update SOP §3 step 8). A gas project in a draft plan is
  enough to add it (Baird 2026-10-07). Placeholder plants named
  "<Utility> IRP CC power station 3" and the like are how earlier cycles
  recorded unsited plan capacity; whether that continues is still open.
- **Data-center gas**: search every state for behind-the-meter gas serving
  data centres; mark captive with industry type Data Centre. Emergency/backup
  gensets are a unit-level checkbox, not a captive flag.
- **ISO/RTO context** decides where in-development units are visible (queues,
  CDR-type reports): ERCOT, SPP, MISO, PJM, NYISO, ISO-NE, CAISO, plus
  non-RTO Southeast and Northwest (balancing-authority queues instead).
- **EIA-860M** monthly is the status backbone (operating / planned /
  retired / cancelled, with planned and actual dates); **EIA-860 annual** for
  ownership shares and technology; **EPA CAMPD** for unit-level "actually
  running" evidence.

## Regulators & official sources

- **U.S. Energy Information Administration (EIA)** — the primary source for
  this country.
  - [Electric Power Monthly — planned generating unit retirements (Table 6.06)](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=table_6_06)
  - [Electric Power Monthly — planned generating unit additions (Table 6.05)](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=table_6_05)
  - EIA also maintains the Form EIA-860/861/923 generator-level data sets
    (not directly cited by URL in the source material, but these are the
    standard EIA generator-level tables underlying the Electric Power
    Monthly views above — check eia.gov/electricity/data for current links).
  - [EIA country analysis page for the US and other countries (global resource)](https://www.eia.gov/international/analysis/world) —
    general overview pages that may be useful for context.

## Key operators & utilities

- Not centralized in the source material — the U.S. market is deregulated in
  much of the country, so ownership is fragmented across many IPPs and
  utilities. Use EIA's generator-level ownership fields as the primary
  ownership source rather than expecting a small set of utility sites to
  cover the fleet.

## Preferred sources (beyond the global roster)

- [Interactive map of US power plants (Esri/ArcGIS)](https://experience.arcgis.com/experience/bb8c905b75f84d908ab83f579498d085/page/Page#data_s=id%3AdataSource_18-1961298a8e3-layer-21%3A2909)
- [Intertek plant search](https://ingrid.intertek.com/adv_search)
- [Northwest Power and Conservation Council map](https://www.nwcouncil.org/energy/energy-topics/power-supply/map-of-power-generation-in-the-northwest/) —
  regional (Pacific Northwest) generation map.
- [GridInfo](https://www.gridinfo.com/plants?s=)
- [CitizenPortal](https://citizenportal.ai/newhome1) — local-government
  meeting-minutes search; can surface early permitting/siting news for
  proposed plants.
- [Synapse Energy Economics search](https://www.synapse-energy.com/search?search_api_fulltext=indiana)
  and [Marcellus Drilling News](https://marcellusdrilling.com/) — useful for
  gas-sector news specifically, including plant proposals tied to gas supply.
- Hydrogen-adjacent project trackers (relevant where hydrogen-blending or
  hydrogen-capable gas plants are in scope):
  [Clean Energy Group US hydrogen projects](https://www.cleanegroup.org/ceg-projects/hydrogen/projects-in-the-us/),
  [Hydrogen Forward](https://www.hydrogenfwd.org/united-states-of-hydrogen/).

## Research tips

- Start with EIA's Electric Power Monthly retirement/addition tables for
  anything time-sensitive (recent status changes), and fall back to the
  underlying EIA-860/923 generator data for plant-level detail EPM
  summarizes.
- CitizenPortal and Marcellus Drilling News are worth checking specifically
  for early-stage proposals that may not have reached EIA's planned-additions
  table yet.

## Gotchas

- None specific to data miscategorization noted in the source material for
  this country — the main risk is simply the fleet's size and the number of
  supplementary trackers, which makes it easy to cite a secondary source
  (map tool, news aggregator) instead of tracing back to the underlying EIA
  generator record.

## Open items

- Confirm current EIA-860/923 access URLs (the source material referenced
  Electric Power Monthly views rather than the raw generator datasets
  directly).

## Update notes

- *2026-10-07* — the IRP step is wired in (`irp_sheet.py`, `--irp` on the
  brief builder and the build, the `irp` record flag). First live read for
  Georgia (1 utility row, 34 plants matched, 28 units already ticked),
  Indiana (8 rows, 42 plants, 34 ticked) and Kentucky (7 rows, 19 plants,
  15 ticked); files under `work/`, no batch run yet.

- *2026-10-06* — ID matching is now a script step (`match_ids.py`, EIA-860M
  file kept by `eia860m.py`); EIP and Sierra Club sheet links recorded in
  `sop_pointers.md`. The US IRPs tab of the Update sheet holds Natalia's
  per-utility IRP notes; Amalia pairs it with a web search for new IRPs per
  state.

- *2026-09-15* — added the per-state structure and the US-specific Q4 2026
  rules (ID matching, IRP, data-center captive, Sierra Club reference-only)
  from the GOGPT US Data/Research Guide, the Q4 kickoff doc and the Update
  sheet's United States research tab. First state file: `united_states/texas.md`.

- *2026-07-27* — seeded from GEM's team-wide "Gas/oil power plant data
  sources - by country" doc. Supplementary tool links (ArcGIS map, GridInfo,
  CitizenPortal, etc.) are undated in the source material; re-verify they're
  still live before relying on them.
