# New York, United States

Scope: 123 unit rows across 74 plants in the pull of 2026-10-02. 115 units are
operating. The rest: one announced, Caithness II at 750 MW; one shelved by
inference, Bowline Point unit 3 at 750 MW; two mothballed, Astoria unit 4 and
West Babylon unit 4; three cancelled with no cancellation year, the Astoria
NRG repowering, the Danskammer combined cycle and NISA; one retired, Nassau
Energy in 2022. No planned retirements are recorded. Amalia Llano's state;
marked in progress on the assignments tab on 2026-09-30. First run of the
state agent in narrowed update mode on 2026-10-02 (`notes/us_state_agent_plan.md`):
20 of 74 plants had a task, 54 were left alone by design. Packet:
`batches/us-ny/deliverables/gogpt_batch_20261002_1631_ET_us-ny_update_*`,
26 edits, 29 questions, 2 watch items.

## State context

- Grid operator: NYISO. Its annual Load and Capacity Data report, called the
  Gold Book, lists every generator with nameplate capacity, in-service year
  and fuel, and its interconnection queue lists proposed plants. The NYISO
  Reliability Needs Assessment and Short-Term Assessment of Reliability name
  the units it keeps running for reliability, which is how some New York
  City peakers slated for retirement stayed online in 2025.
- Climate law: the Climate Leadership and Community Protection Act of 2019
  calls for 70 percent renewable electricity by 2030 and a zero-emission grid
  by 2040. The Department of Environmental Conservation cited it in October
  2021 when it denied Title V air permits for the Danskammer and Astoria
  NRG gas repowering projects. Both owners appealed. Danskammer lost in
  court in June 2022 and withdrew its application on June 17, 2024. NRG
  applied to withdraw on September 15, 2022 as part of selling the land to
  Beacon Wind, a sale that closed in January 2023.
- Peaker rule: Department of Environmental Conservation Part 227-3 set
  nitrogen oxide limits for simple-cycle turbines that phased in during 2023
  and 2025. It drove the retirement or mothballing of older peakers in New
  York City and on Long Island. A unit that went dark under this rule may be
  retired, mothballed, or kept under a reliability agreement; check which.
- Regulators and sources: the Public Service Commission's Document and
  Matter Management system (documents.dps.ny.gov) for case filings;
  Department of Environmental Conservation permit notices and Title V
  permits (dec.ny.gov); NYISO Gold Book and queue (nyiso.com); Long Island
  Power Authority and PSEG Long Island for Long Island plants; New York
  Power Authority for its own plants; EIA-860 annual and EIA-860M monthly
  tables for everything else. The 2026-10-02 statewide agent could not
  reach the Department of Environmental Conservation notice bulletin or the
  Public Service Commission document system from this machine; the NYISO
  queue workbook and EIA-860M covered the new-plant search.

## Backlog rows from the possible-updates sheet, worked 2026-10-02

- Row 110: Constellation's purchase of Calpine, closed January 7, 2026.
  No owner change staged. The EIA-860M table for August 2026 still lists
  Calpine Eastern Corp for Bethpage and the EIA-860 table for 2024 lists
  Calpine Corp for the Kennedy airport plant; no document renames or merges
  either plant-holding entity. Questions raised on both plants. Row can be
  marked done unless Amalia wants the parent recorded differently.
- Row 166: Digi Power X data center at the Fortistar North Tonawanda plant.
  The city extended its data center moratorium in June 2026, so the AI
  conversion is on hold. The reported 60 MW is a grid load request in the
  NYISO queue, not a new generator. Watch item, recheck by 2027-06-30.
- Row 1858: Lotus Infrastructure Partners bought the Caithness Long Island
  Energy Center; the sale closed January 7, 2026 and Lotus plans to rename
  the plant Brookhaven Energy Center. No source names the company that now
  holds the plant, so Owner(s) stays Caithness Long Island LLC with a
  question. Start year 2009 was filled from EIA-860M and a Caithness release.

## Still open after the 2026-10-02 batch

- Danskammer: the five unit rows carry coordinates with no Location Data
  Source. The EIA-860M point is about 200 meters from GEM's. Decide which to
  keep. Other Name(s) says Roseton Generating Station; Roseton is the
  neighboring plant with its own record, so the alias looks wrong.
- Astoria unit 4: EIA-860M lists it retired in February 2021. GEM says
  mothballed. Only one publisher found, so the change is yellow; a NYISO
  Gold Book from 2021 or later would make it green.
- Astoria NRG: Latest Activity reads January 24, 2024 and cites an NRG legal
  page that now shows unrelated gas rate notices. The newest events found
  are from 2022 and 2023, so the date was left in place.
- AES Greenidge "Unit 4, timepoint 2": add EIA generator ID 4 to Other IDs
  (unit). A March 2022 state letter says the gas conversion was in 2017;
  GEM has 2016. Single source, so yellow.
- Caithness II: no EIA plant code, which is expected for an unbuilt
  project. The newest activity is the April 2025 Department of Energy
  request for information that names the site for a 750 MW plant; a 2018
  article has Caithness asking the town for a smaller 600 MW plant.
- Bowline Point unit 3: newest dated report is a November 2012 open house.
  Proposed cancelled-inferred. A search result showed the interconnection
  queue entry as withdrawn but the page could not be opened.
- City naming: Riverbay filled as New York, the postal city in EIA and
  GridInfo, though the plant is in the Bronx like Harlem River Yard and
  Hell Gate; Brentwood filled as Islip from the state permit address,
  though the neighboring Edgewood plant says Brentwood. Amalia's call.
- NYISO queue, August 31, 2026 workbook: capacity-rights-only uprate
  requests for Bethlehem Energy Center, Arthur Kill unit 2 and West Babylon
  unit 4, no megawatt figures. The West Babylon one may mean the mothballed
  unit returns to service.
- Not in GEM: Alpha Generation proposed on March 16, 2026 to replace the
  Gowanus and Narrows barge peakers in Brooklyn with three new gas units.
  Watch item, recheck 2027-01.

## Gotchas

- Latest Activity is a date field. Every filled value in the export reads
  `Year: 2024, Month: 6, Day: 17`. Stage the date of the newest report and
  put what happened in the note, and never move the date backward.
- GEM's Owner column holds the plant-holding company; the parent is a
  separate computed column. Utility names in EIA tables are not owner
  changes. The Constellation and Lotus purchases were parent-level changes
  until a filing names the new plant holder.
- Many New York City plants are peakers of a few units each, split between
  the current owners that bought them from Con Edison in 1999. Several share
  names with their neighbors (Astoria, Astoria NRG, Astoria Energy); check
  the EIA plant code before attaching a document. EIA plant 8906 also lists
  a 15 MW generator 1, under the tracker threshold.
- Greenidge is a former coal plant converted to gas in 2017 that mainly
  powers cryptocurrency mining on site; its Title V renewal was denied in
  2022 and has been in litigation since. Greenidge and Fortistar North
  Tonawanda both have data center load requests in the NYISO queue; those
  are grid load, not new generators.
