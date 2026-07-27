# United States

Largest single-country fleet in scope; EIA is the backbone data source, with
a long tail of supplementary trackers and news sources for keeping pace with
retirements/additions between EIA release cycles.

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

- *2026-07-27* — seeded from GEM's team-wide "Gas/oil power plant data
  sources - by country" doc. Supplementary tool links (ArcGIS map, GridInfo,
  CitizenPortal, etc.) are undated in the source material; re-verify they're
  still live before relying on them.
