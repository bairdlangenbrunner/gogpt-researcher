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
  Public Service Commission document system. Both load with the fetch
  script now: the notice bulletin needs browser impersonation, which the
  script does on its own. Commission documents open by their ViewDoc
  address and case pages by MatterCaseNo, but a case's filing list loads
  only in a real browser, so find filings by web search. NYISO file
  addresses, including the Gold Book, are in the source roster.

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
  Gold Book from 2021 or later would make it green. The 2026 Gold Book
  lists Astoria units 2, 3 and 5 but not unit 4. That is a gap, not a
  statement, so it does not count. The 2021 and 2022 Gold Books are not at
  the address pattern that works for 2025 and 2026; find them by web search.
- Astoria NRG: Latest Activity reads January 24, 2024 and cites an NRG legal
  page that now shows unrelated gas rate notices. The newest events found
  are from 2022 and 2023, so the date was left in place. The unit is
  cancelled, so Latest Activity no longer matters for it.
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
  The discovery pass below adds the existing barge plants and carries the
  repowering as its own watch item, recheck 2027-04.

## Discovery pass of 2026-10-02

What was searched: the 2026 NYISO Gold Book (the existing-generator table,
the proposed-generator tables, the capacity-ineligible list, the
deactivation notices and the New York Power Authority 2030 list), the NYISO
interconnection queue, the NYISO first-quarter 2026 reliability report and
its June 30, 2026 planning status report, the EIA-860M table for August
2026 against the GEM export by EIA plant code, Public Service Commission
filings, Department of Environmental Conservation permit review reports,
the New York Power Authority's May 2025 transition plan for its small gas
plants, company pages and releases, and the trade press. Not searched: the
Department of Environmental Conservation permit database plant by plant,
and the Long Island Power Authority board materials beyond the Far Rockaway
contract.

Added (deliverable `gogpt_batch_20261002_2153_ET_us-ny_discovery`), all
operating plants that EIA and NYISO list but GEM lacks:

- Gowanus Gas Turbines generating station, Brooklyn (EIA plant 2494): four
  barges of eight 20 MW simple-cycle turbines each, 640 MW nameplate, in
  service 1971. Barges 1 and 4 burned oil only and retired in November
  2022. Barges 2 and 3 burn gas or distillate; their retirement notice for
  July 14, 2026 was withdrawn on April 16, 2026 because NYISO needs them
  through May 1, 2029. Owner entered as Alpha Generation LLC with operator
  Alpha Generation, following GEM's Astoria and Arthur Kill records for the
  same company; the legal owner is Astoria Generating Company, L.P.
- Narrows Gas Turbines generating station, Brooklyn (EIA plant 2499): two
  barges of eight 22 MW turbines each, 352 MW nameplate, in service 1972,
  same owner, notice and withdrawal as Gowanus.
- Vernon Boulevard power station, Long Island City (EIA plant 7909): two
  47 MW LM6000 turbines of 2001, New York Power Authority, entered as one
  unit of two engines the way GEM records Hell Gate. State law ends gas
  generation at the Authority's small plants by December 31, 2030.
- Pouch Terminal power station, Staten Island (EIA plant 8053): one 47 MW
  LM6000 turbine of 2001, New York Power Authority. Under the 50 MW bar on
  its own; added because GEM already records the identical sister plants
  Brentwood and North 1st at 47 MW. Scope call for the reviewer.

Each barge is entered as one unit with a turbine count and a per-turbine
capacity. No source names the barge turbine model, so the technology is
plain gas turbine; each turbine alone is under 50 MW, so the plants are in
scope only as engine sets. Two more Authority plants, Gowanus 5 and 6 (94
MW, next to the barges) and Kent (47 MW, Brooklyn), are also missing from
GEM and were not staged for lack of time; add them in the next pass.

Watch item (recheck by April 2027): AlphaGen's March 16, 2026 proposal to
replace the six Gowanus and Narrows barges with three new 273 MW dual-fuel
barges, 819 MW in all, offered in answer to Con Edison's request for
information. No permit, siting case, queue entry or schedule. The earlier
549 MW Gowanus repowering queue entry was withdrawn in January 2023 and the
2019 Siemens barge plan (case 18-F-0758) was withdrawn.

Looked at and set aside: RED-Rochester at Eastman Business Park (owner SDCL
Energy Efficiency Income Trust, operator Ironclad; the largest gas unit is a
38 MW recycled Frame 6B turbine of 2025, every unit under 50 MW, a captive
industrial plant for a human call); Far Rockaway GT1 and GT2, which are
GEM's Bayswater and Jamaica Bay records; Glenwood, Shoreham, Wading River
and West Babylon, all in GEM; withdrawn and cancelled queue entries; and the
diesel backup fleets at data center sites, which are standby generators.
No new gas or oil project of 50 MW or more was found in development in New
York.

For the next update batch: Danskammer units 1 to 4 filed to deactivate on
August 1, 2026, were held to at least January 15, 2027 by NYISO, and the
owner filed for Chapter 11 on June 10, 2026; Pinelawn Power 1 gave notice
for November 1, 2025 with no reliability hold; the Far Rockaway, Bayswater
and Jamaica Bay deactivation notices were withdrawn as of May 1, 2026 under
a ten-year Long Island Power Authority contract, and Jamaica Bay's parent
should read Hull Street Energy, not NextEra; Astoria GT 01 retired May 1,
2025; the Authority's 2030 phase-out belongs on the Brentwood, Harlem River
Yard, Hell Gate, Joseph J. Seymour and North 1st rows, and Harlem River
Yard has engine count and per-engine capacity swapped; Shoreham and
Glenwood lose water injection in May 2027; Ravenswood was sold to NRG on
January 30, 2026; Caithness II should move from announced to shelved;
Bethlehem (plus 40 MW) and Arthur Kill (plus 12.2 MW) have capacity-rights
uprate requests in the queue.

## Gotchas

- Latest Activity is a date field. Every filled value in the export reads
  `Year: 2024, Month: 6, Day: 17`. Put what happened in the note, and
  never move the date backward. It is only for stalled projects: units in
  development, shelved, or with an inferred status, and only when the
  newest report is more than a year old. Caithness II is the one New York
  unit that qualified in October 2026.
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
