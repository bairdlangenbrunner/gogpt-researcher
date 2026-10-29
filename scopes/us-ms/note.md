# United States, Mississippi

Scope: 53 unit rows across 24 plants in the pull of 2026-10-23. By status that is 1 announced, 1 pre-construction, 8 construction, 41 operating and 2 retired. Assigned to Amalia Llano for the Q4 2026 cycle. Three rows are on the US IRPs tab: Mississippi Power Company (2024 plan), Entergy Mississippi (2024 plan) and a Mississippi Public Service Commission row with no plan of its own. One captive LNG sheet row: the Gulf LNG terminal at Pascagoula, which the sheet excludes. The validation report has 16 research fixes on 7 plants and no by-hand fixes. No Assigned Comments threads and no units without a tracker. Batch plan: `scopes/us-ms/plan.md`.

## State context

- Four utilities and three grid operators. Entergy Mississippi and Cooperative Energy sit in the Midcontinent Independent System Operator, called MISO, in its southern region (local resource zone 10). Mississippi Power is a Southern Company utility in the Southern balancing area, with its own interconnection queue on the Southern Company transmission site. The Tennessee Valley Authority, called TVA, serves the north of the state and runs its own queue on its OASIS site. Clarksdale Public Utilities owns Crossroads.
- The utility regulator is the Mississippi Public Service Commission. Docket numbers look like 2022-UA-153. Portal document links need a session, so cite the docket number and the document name, or the monthly docket list PDF for a docket's title and filing date. `scopes/us-ms/harvest_psc.py` reads the portal ahead of a sweep; copies stay in `work/psc_ms/`. TVA projects need no state certificate; TVA's environmental reviews and records of decision are the approval documents.
- Air permits come from the Mississippi Department of Environmental Quality, called MDEQ, through its Permit Board. Permits and activity are in enSearch Online at opcgis.deq.state.ms.us. The Permit Board posts monthly agendas and minutes; the 2021 minutes are missing from the minutes index. `scopes/us-ms/harvest_permits.py` reads all three and writes `scopes/us-ms/work/permits/<plant>.md`, plus `_unmatched.md` for power-like facilities GEM lacks.
- Entergy Mississippi's new combined cycle plants are Delta Blues (Greenville), Vicksburg (at the Baxter Wilson site) and Traceview (Madison County, called Madison County Advanced Power Station in its air permit). Each is one Mitsubishi M501JAC block in GEM.
- TVA's New Caledonia plant (Lowndes County) is six GE 7E.03 heavy-duty frames, so six units is right. A groundbreaking was held on October 22, 2025.
- Colossus 2 (Southaven area) is xAI's data center power plant. GEM holds the operating temporary turbines as unit 1 (495 MW) and the planned Solar Titan 350 set as unit 2 (1,240.5 MW). The MDEQ facility is MZX Tech LLC (agency interest 12592); GEM's owner name is MZT Tech LLC, so check the spelling.
- Plant Ratcliffe is the gas combined cycle of Mississippi Power's Kemper County project. The coal gasifier was cancelled. The GEM plant named Kemper County power station is TVA's separate four-turbine peaking plant.
- Jack Watson units 4 and 5 burned coal until 2015 and burn gas now; GEM holds the gas phase as timepoint 2 units. Morrow's coal units retired in 2018 and the gas combined cycle MOR1 replaced them.

## Watch items to raise with the reviewer

- Baxter Wilson unit 2 has a retired year of 2018, before the 2020 floor for retired units. Amalia added it in July 2025, likely as the link for the Vicksburg replacement. Ask her before any change.
- Caledonia's owner in GEM is GE Energy Financial Services, while MDEQ names the facility TVA Caledonia Combined Cycle Plant.

## Gotchas

- 35 of 53 rows were last touched in October 2021. Operator is optional in the manual, so a blank operator source is not a gap.
- The ID matcher's possible new plants include L L Wilkins (Clarksdale, 55.2 MW only as a group of four small units) and Sylvarena (Cooperative Energy, three 47 MW turbines, 141 MW). Both need a threshold call.
- The TVA queue is two PDFs in the TVA OASIS document folder, `OASIS_CurrentQueue_<date>.pdf` and `OASIS_ArchiveQueue_<date>.pdf` under https://www.oasis.oati.com/woa/docs/TVA/TVAdocs/. The dated names change, so read them from the OASIS menu in real Chrome and download with `curl -k`. Save each table as a CSV under `work/tva_queue/` and pass each one to `scopes/us-ms/pull_queues_mississippi.py --tva-file`.
