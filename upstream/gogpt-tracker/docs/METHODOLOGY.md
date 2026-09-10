# GOGPT Methodology

Source: Global Energy Monitor, [Global Oil and Gas Plant Tracker](https://globalenergymonitor.org/projects/global-oil-gas-plant-tracker).

## Two-level system

GOGPT organizes information at two levels:

- **Database** — tracks individual oil and gas plant *units*: owner and parent
  company, status, plant type, and location.
- **Wiki pages** — one per power station on GEM.wiki, with footnoted detail such
  as project history and public opposition.

Both are updated twice a year, in January (H1) and July (H2).

## Scope

The tracker covers all oil- and gas-fired power plants that generate electricity
in any setting: peaking and base-load generation, captive industrial plants, and
co-generation.

**Capacity thresholds**

- 50 MW or more, worldwide.
- 20 MW or more in the European Union and the United Kingdom.
- Combined-cycle units: the threshold applies to the **entire combined-cycle
  set**, not the individual components.
- Internal-combustion or multi-engine units (multiple identically sized
  engines): the threshold applies to the **total capacity** of the set.

Gas boilers that only generate district or industrial heat are **not** included.

## Status definitions

| Status | Meaning |
|---|---|
| **Announced** | Publicly reported but not yet actively moving forward (no permits, land, materials, or financing sought). |
| **Pre-construction** | Actively moving forward — seeking government approvals, land rights, or financing. |
| **Construction** | Site preparation and equipment installation underway. |
| **Shelved** | Suspension announced, or no progress observed for ≥ 2 years. |
| **Cancelled** | Cancellation announced, or no progress observed for ≥ 4 years. |
| **Operating** | Formally commissioned; commercial operation has begun. |
| **Mothballed** | Disused but not dismantled. |
| **Retired** | Decommissioned. |

## Data sources

- Government data on individual plants, country/area energy and resource plans,
  and permit/application tracking sites.
- Reports by state-owned and private power companies.
- News and media reports.
- Local NGOs tracking oil/gas plants or permits.

## Validation

GEM researchers validate the dataset against proprietary and public data —
including S&P Global Platts World Electric Power Plants database and the World
Resources Institute's Global Power Plant Database — plus company and government
sources. Where possible, data is circulated for review to researchers familiar
with local conditions and languages. Reviewers and collaborators include the
Centre for Research on Energy and Clean Air, Beyond Fossil Fuels, Environmental
Integrity Project, and Sierra Club, among others.

## How this repo's compile step applies the methodology

`scripts/gogpt_compile.py` turns a raw database CSV export into the published
multi-tab spreadsheet:

1. **Drop pre-2020 retirements** — retired units with a retirement year before
   2020 are removed from the deliverable.
2. **Apply capacity thresholds** — 20 MW for the EU/UK country list, 50 MW
   elsewhere; sub-threshold units are split into their own tab. A narrow
   exception keeps sub-50 MW "waste heat from natural gas" units.
3. **Remove H2 conversions** — units listed in `assets/H2_units_to_exclude.xlsx`
   (identified by GEM Unit ID) are dropped.
4. **Split IRP units** — announced units whose plant name contains "IRP" are
   moved to a dedicated IRP tab, out of the main list.

Output tabs: **Gas & Oil Units**, **sub-threshold units**, **IRP**.
