# Source Roster (Oil & Gas Power Plants)

Distilled from GEM's team-wide crowdsourced Google Doc, **"Gas/oil power
plant data sources - by country"** (Doc ID
`1J4JHu_Sy5190nMGCUqw8B_0UQwVgopcNo8UJTXE-cRw`), GLOBAL/multi-country
sections, fetched 2026-07-27. That doc remains the living, team-wide list
across all countries GEM tracks; this file is the repo-local distillation
of its cross-country material. Country-specific sources belong in
`docs/country_notes/<country>.md` (see that directory's `README.md`) —
this file does not duplicate them.

Tiers are operational, mirroring the confidence-labeling rule in
`docs/sops/update.md` §6: any source that fully validates (names the unit,
states the value) can stand alone for green; a second independent
corroborator is preferred, and required only for green on a status change.

## Tier 1 — Primary (stand-alone for green confidence)

Sources that establish a fact on their own — government dataset, regulator
filing, or owner/operator IR direct.

### Regulator / government registries and statistics

Energy ministries, electricity regulators, and grid operators that publish
plant-level generation, capacity, or licensing data. Quality and structure
vary enormously by country and drift over time (much of the upstream doc's
sourcing dates to 2019–2022 — re-verify a flagged link before relying on
it). Representative examples surfaced in the source doc:

| Country/region | Source | Notes |
|---|---|---|
| Nigeria | NERC (`nerc.gov.ng`) | Plant-level generation stats, GPS coordinates, ownership, licensee list |
| Bahrain | Electricity and Water Authority (`ewa.bh`) | Annual statistical books, unit-level fuel/capacity/commission year |
| Philippines | DOE (`doe.gov.ph`) | Philippine Energy Plan |
| Singapore | EMA (`ema.gov.sg`) | Singapore Energy Statistics |
| Côte d'Ivoire | Ministry of Mines, Petroleum and Energy (`energie.gouv.ci`) | Annual activity reports |
| Algeria | Sonelgaz (`sonelgaz.dz`) | Development plan with plant-level detail |
| Russia | SO UPS scheme/programme reports | Progress reports on power-system development |
| United States (PJM: MD, PA, NJ, DE, VA, WV, OH, DC and parts of IL, IN, KY, MI, NC, TN) | PJM Interconnection (`pjm.com`) | See "PJM data files" below |
| United States (New York) | NYISO (`nyiso.com`) | See "NYISO data files" below |

**PJM data files** (checked 2026-10-02; not bot-walled, plain curl works,
but the queue web pages render from JavaScript, so go to the files):
- Full interconnection queue, about 9,200 projects back to the early 2000s, all
  statuses including withdrawn: `https://www.pjm.com/pub/planning/downloads/xml/PlanningQueues.xml`
  (22 MB; fields include Name, CommercialName, State, County, Fuel, MWCapacity,
  MWEnergy, Status, ProjectedInServiceDate, ActualInServiceDate, WithdrawalDate,
  TransmissionOwner). Verify with `url_verifier.py --timeout 120`; read the
  record from a downloaded copy and quote it in the note, as with EIA Excel files.
- Transition-cycle projects: `https://www.pjm.com/pub/planning/downloads/xml/transitionProjects.xml`.
- Deactivations: the notices page
  `https://www.pjm.com/planning/service-requests/gen-deactivations/generator-deactivation-notices`
  links each plant's deactivation letter and PJM's response as PDFs (cite the
  PDF); currently mothballed units:
  `https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-mothballed-units.xlsx`.
- Old addresses that now 404: `pub/planning/downloads/xls/PlanningQueues.xlsx`,
  `planning/services-requests/interconnection-queues`. The `services.pjm.com`
  queue export needs a key; don't use it.

**NYISO data files** (checked 2026-10-02; not bot-walled, but every document
list on nyiso.com is drawn by JavaScript and its folder-listing service needs
a browser session, so go to the files by address):
- Gold Book (Load & Capacity Data Report), yearly each spring:
  `https://www.nyiso.com/documents/20142/2226333/<YEAR>-Gold-Book-Public.pdf`
  (2025 and 2026 resolve). Table III-2 has every existing generator (owner,
  zone, in-service date, nameplate, summer and winter capability, fuel);
  IV-1a proposed additions; IV-3 and IV-4 deactivated units; IV-5 units with
  a deactivation notice; IV-6 peaker-rule status changes. Tables run to
  March 15 of the report year. The PDF text extracts cleanly, so the
  verifier can match plant name and value (`--timeout 90`).
- Interconnection queue workbook (monthly):
  `https://www.nyiso.com/documents/20142/1407078/NYISO-Interconnection-Queue.xlsx`.
  Cite like an EIA Excel file.
- Deactivation news after the Gold Book cutoff: the monthly "NYISO System &
  Resource Planning Status Report" posted on `nysrc.org` (for example
  `https://www.nysrc.org/wp-content/uploads/2026/07/7.1-6-30-2026-NYISO-Planning-Status-Attachment-7.1.pdf`).
  NYISO's own monthly Generator Status Updates folder (on the NY Power System
  Information & Outlook page) can only be listed in a real browser.
- Market generator list with PTID, zone and coordinates:
  `https://mis.nyiso.com/public/htm/generator/generator.htm`.

For a country not yet seeded in `docs/country_notes/`, search pattern:
`"<country>" ministry OR authority energy OR electricity statistics
generation capacity`, and add findings to a new `<country>.md` from
`docs/country_notes/_template.md`.

### Multi-country regulatory/statistical aggregators

- **US EIA international analysis** (`eia.gov/international/analysis/world`)
  — country-level overview pages; useful context, not usually plant-level
  detail on its own.
- **IEA country energy policy reviews** (`iea.org/reports/...`,
  `iea.blob.core.windows.net/...`) — periodic in-depth country reports
  (e.g. Netherlands 2020, Spain 2021, Tajikistan 2022) that often include
  plant tables. Treat as Tier 1 when the report itself names the plant and
  cites its own primary source; treat as Tier 2 (needs corroboration) when
  it's summarizing without attribution.
- **Ember's African Electricity Data Transparency project**
  (`ember-climate.org/project/africa-electricity-data`) — a guide to where
  national electricity data lives per African country; a finding tool, not
  itself a plant-level citation.

### Operator / owner direct

Company IR pages, annual reports, and project pages, when they name the
specific plant. Always preferred over any aggregator for capacity, status,
ownership, and technology once the operator/owner is known.

## Tier 1 (with caveats) — WEPP (S&P Global Platts)

**WEPP (World Electric Power Plants database)** is turbine/unit-level,
proprietary, and licensed to GEM — treat a WEPP value as Tier 1 for
existence/capacity leads but corroborate before citing (WEPP itself is not
a public URL you can cite in a `[ref]` column).

Reconciling WEPP against GOGPT/GGPT rows:

- WEPP records **each turbine separately**; GOGPT/GGPT combines a combined-
  cycle set's turbines into **one row**. Don't assume a 1:1 match between
  WEPP rows and GOGPT units — check every WEPP row at a plant before
  concluding capacity or count.
- In a combined-cycle set, WEPP lists the gas turbine's fuel as `GAS` and
  the downstream steam turbine's fuel as `WSTH` (waste heat). Seeing
  `WSTH` alone does **not** mean gas-fired combined-cycle — `WSTH` also
  appears standalone at refineries/cement plants as an industrial
  byproduct. Check all units at the plant before inferring combined-cycle.
- **UTYPE** (WEPP's technology field) conventions for combined-cycle
  components:
  - `GT/C`, `ST/C` — gas/steam turbine in combined cycle
  - `GT/CP`, `ST/CP` — combined cycle in CHP (cogen)
  - `GT/S`, `ST/S` — CHP steam sendout / heat recovery (cogen)
  - `GT/CS`, `ST/CS`, `GT/D`, `ST/D`, `CC/D` — desalination-linked CHP
  - `CC` — combined-cycle set on one row, turbines not broken out
    (typically an early-stage proposal without turbine detail yet)
  - `CCSS`, `CCSS/P` — single-shaft combined-cycle (GT and ST mechanically
    coupled, must be treated as one functional unit)
- The GEM DB's `unit_external_id` / `plant_external_id` tables carry WEPP
  IDs under `external_id_system.name = "WEPP (S&P Global Platts)"`,
  surfaced as the export's dedicated `WEPP location ID` / `WEPP unit ID`
  columns (see `docs/reference/gem_db_schema.md`).

## Tier 2 — Trade press and analytical aggregators

Good for finding leads and cluster-level coverage; need a primary source
alongside for green confidence.

- Trade/energy press generally (regional business press, industry
  newsletters) — treat per-article credibility case by case; prefer
  outlets that cite their own primary source.
- **IndustryAbout** (`industryabout.com`) — per-country fossil-fuel plant
  lists, often useful for lat/lon when a regulator source lacks
  coordinates.
- **Energybase.ru** (`energybase.ru`) — plant database strong on
  post-Soviet states; good secondary check alongside GEO-derived leads.
- **Power Africa / Open Data for Africa** (`powerafrica.opendataforafrica.org`)
  and **African Energy** (`africa-energy.com/database`) — Africa-focused
  plant status and fuel-type data, including proposed/under-construction
  projects; African Energy tends to be more current on status than Power
  Africa.

## Tier 3 — Aggregators (lead-generation only, never citable alone)

These identify candidate plants and rough parameters fast, but their
values must always be re-verified against a Tier 1/2 primary before
staging — never cite the aggregator itself as the `[ref]`.

- **Global Energy Observatory** (`globalenergyobservatory.org`) — legacy
  crowdsourced plant database; largely inactive/frozen. Historically used
  for start-year leads; corroborate independently, don't cite.
- **WRI Global Power Plant Database** (`datasets.wri.org/dataset/globalpowerplantdatabase`)
  — aggregated, GEM/GEO/other-sourced; useful for a location/coordinate
  lead, never a standalone citation (partly circular with GEM's own data
  in places).
- **Wikipedia "List of power stations in `<country>`" pages** (and
  non-English equivalents, e.g. Russian/Vietnamese/Spanish Wikipedia) —
  frequently well-referenced and a fast way to find candidate plants and
  the sources they in turn cite. **Never cite Wikipedia directly** — open
  its footnotes and cite the original source.
- Industry equipment-vendor reference lists (e.g. a turbine OEM's project
  reference list) — useful for confirming a plant existed and its
  equipment, not for current status.

## Forbidden / banned (family-wide, non-negotiable)

Verbatim from `docs/sops/update.md` §7.2 and `docs/sops/discovery.md`:

- **Never cite gem.wiki or globalenergymonitor.org**, and never cite a
  republisher whose data is GEM-derived — anti-circularity: GEM data must
  never source itself. gem.wiki may be used to check for an existing
  record during dedup, but never as a citation or `[ref]` value.
- **abarrelfull is banned outright** as a source, in any lane, even
  corroborated. Chase the primary source it footnotes instead.
- **One fully validated working URL is sufficient per staged value; a
  second independent source is preferred, never required** (Baird 2026-10-02, adopting the pipelines-researcher ruling of 2026-09-30).
  A status change needs 2+ independent publishers for green.
- **Mirrors/syndications of one document count as ONE source** — a press
  release plus wire re-publications of it is one source, not several.
- **URLs live only in `[ref]` / "Data Source" columns** — never embedded
  in a value, name, or notes field.
- Every candidate URL passes `python url_verifier.py <url> <expected
  strings>` before it's staged — HTTP 200 (or a passing Wayback fallback
  on bot-block), not a soft-error/paywall stub, and the body must contain
  the plant name and the cited value. See `docs/sops/update.md` §7.1.

## Working order

1. Check `docs/country_notes/<country>.md` first for known regulator URLs
   and prior gotchas for that country.
2. Government/regulator (Tier 1) → operator/owner IR (Tier 1) → trade
   press (Tier 2) for corroboration → WEPP for existence/capacity leads,
   reconciled per the UTYPE guidance above.
3. Use Tier 3 aggregators (GEO, WRI GPPD, Wikipedia) only to find
   candidates or leads; always resolve to a citable primary before
   staging.
4. Log any new durable source or dead link back into the relevant
   `docs/country_notes/<country>.md` at batch close, per that directory's
   `README.md`.
