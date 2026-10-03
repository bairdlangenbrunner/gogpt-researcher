# United States — Maryland

Scope: small assignment, 37 unit rows across 17 plants in the pull of
2026-10-02. Amalia Llano worked seven plants on 2026-09-28 to 09-30; the
other ten were last touched between 2021 and 2025. Used as the first blind
calibration of the state research agent (`notes/us_state_agent_plan.md`).

## State context

- Grid operator: PJM. Retirements of the Baltimore-area oil and coal units
  (Brandon Shores, Herbert Wagner) are held back by PJM reliability
  agreements through May 2029.
- The Next Generation Energy Act (2025) gave the Public Service Commission
  an expedited permit route for dispatchable generation. Constellation's two
  Perryman-area proposals (Project 1, 150 MW; Project 2, 564 MW) were
  approved for that route in December 2025 and must file by July 1, 2027.
  They are alternatives, so only one may be built.
- Regulators and sources: Maryland Public Service Commission orders
  (psc.maryland.gov), the Power Plant Research Program siting reports
  (dnr.maryland.gov/pprp), Department of the Environment air permits
  (mde.maryland.gov, including the Test and Documents folders), plus the
  EIA-860 annual and EIA-860M monthly tables.

## Open questions from the 2026-10-02 run

- Morgantown units 5 and 6: GEM says retired (set 2026-09-30), the EIA
  monthly tables for 2026 say operating after a June 2024 retirement. Retired
  year is blank on both.
- Chalk Point SGT1 appears twice: under Chalk Point Generating Station
  (EIA plant 65285 recorded) and under NRG Chalk Point CT power station
  (EIA plant 61890). Probably one generator.
- Essential Power Rock Springs: Old Dominion Electric Cooperative built two
  of the four units; GEM lists Essential Power as owner of all four.
- Chalk Point units 3 and 4 fuel (gas only in the 2024 EIA annual file,
  oil and gas elsewhere); NRG Chalk Point CT SGT1 may also burn gas.
- CPV St. Charles capacity: 775 MW nameplate in EIA against 725 MW in the
  owners' release. Mattawoman (cancelled): 859 MW in approvals, 1,008 MW in
  EIA.
- Watch: Vistra's purchase of Cogentrix (owner of Essential Power Rock
  Springs) was approved by FERC in August 2026 and had not closed.
- Essential Power Rock Springs generators 5 and 6 (195 MW each, flagged as
  a possible new unit lead in the update batch) are not a lead. They have
  sat in the EIA monthly "canceled or postponed" table since at least
  December 2016 and were never installed, so the cancellation is before
  2020 and outside GEM's tracking window. Nothing to add.

## Discovery pass of 2026-10-02

What was searched: the PJM queue (through the interconnection.fyi copy,
because PJM's own queue tool could not be read), Public Service Commission
orders on the expedited permit route, the EIA-860M table for August 2026
and its December files back to 2016, Department of the Environment permit
pages, company filings and the trade press. Not searched: the Public
Service Commission e-filing system case by case, and the Department of the
Environment open-data air permit dataset.

Added (deliverable `gogpt_batch_20261002_2128_ET_us-md_discovery`):

- Morgantown, Phase 1: TeraWulf's first 500 MW of gas generation at the
  site, status announced. The company's February 2026 investor presentation
  gives two phases of 500 MW gas, 250 MW battery and 500 MW data center load
  each. FERC approved the sale of the plant on July 29, 2026 (ownership only).
  No certificate application, no air permit, and the county planning
  commission recommended against the zoning change in June 2026.

Watch items (in the deliverable's watch list, recheck by April 2027 unless
noted):

- Morgantown, Phase 2: same presentation, no date or step.
- PJM queue entries of April 2026 with no plant name and no second source:
  Old Line Reserve Energy 510 MW (Charles County, on the Morgantown lines,
  possibly TeraWulf's vehicle), Parkway Generation 618 MW (Cheltenham),
  KMC Thermo 620 MW (Brandywine), FS CT Project 300 MW (Brandon Shores),
  Dickerson Power 200 MW (Dickerson), and Parkway's 53.5 MW entry at
  Cheltenham that sits on the 50 MW line.
- Perryman Gas LLC 555 MW (queue C01-1579, target December 2029) is almost
  certainly Constellation Project 2 under a project company name. Do not
  add it; tie the queue number to the GEM record once the certificate
  application names the company (recheck July 2027).
- Aberdeen Proving Ground: the Army picked Ameresco in September 2026 for
  gas generation first and a molten salt reactor later. No megawatts, site
  or schedule yet.

Looked at and set aside: White Oak FDA campus (54 MW of units under 10 MW
each), Philadelphia Road (four 20.7 MW units), Gould Street (retired 2019),
Notch Cliff, a withdrawn 108 MW oil entry by Lanyard Power (queued and
withdrawn within days in June 2025), and the diesel backup fleets at the
Frederick and Dickerson data centers (Aligned about 508 MW, Amazon about
258 MW, Rowan about 253 MW), which are standby generators, not plants.

For the next update batch: Herbert Wagner units 3 and 4 show a planned
retirement of June 2029 in the August 2026 EIA monthly table; Talen has
asked FERC to extend the Brandon Shores and Wagner reliability agreements
to May 2031 (docket ER26-2739); Wagner unit 1 and GT1 retired in June
2025; AlphaGen withdrew the Keys uprate (766 to 801 MW) from the expedited
route on December 22, 2025 and will seek a change to the existing
certificate instead.

## Gotchas

- Herbert Wagner "Unit 3, timepoint 2" is the coal unit after its 2023
  conversion to fuel oil. Start year 2023 is the conversion year by GEM
  convention.
- GEM's Owner column holds the project company (Dickerson Power LLC, Cove
  Point LNG LP, CPV Maryland LLC) with parents in Parent(s). EIA utility names
  are not owner changes.
- Cove Point's two steam turbines are captive to the LNG terminal and are not
  in EIA.
