# United States — New Mexico

Scope tag `us-nm`. The scoped export pulled on 2026-11-17 holds 52 unit rows at 24 plants: 19 operating, 15 pre-construction, 9 announced, 7 cancelled (one of them inferred), 1 construction and 1 retired. The roster row counts 22 units in development, 6,216.4 MW. The batch goes onto Amalia Llano's review page. Amalia edited about 30 New Mexico rows on November 9 and 10, 2026, and tagged her notes "ALQ42026". Her values are the starting point. Change one only when a document says otherwise, and name the document.

## State context

- **Grids.** The east of the state is in the Southwest Power Pool. That area is Lea, Eddy, Chaves, Roosevelt and Curry counties, served by Xcel's Southwestern Public Service (SPS). The SPP active queue is an open CSV. The rest of the state has no market. PNM, El Paso Electric (EPE, which serves the Las Cruces area), Tri-State and its member cooperatives, Farmington Electric Utility System and Los Alamos County each run their own interconnection. EPE posts its active queue as a PDF. PNM and Tri-State requests are read from the Lawrence Berkeley National Laboratory queue file until their own lists are found.
- **Regulator.** The New Mexico Public Regulation Commission (PRC) regulates PNM, SPS and EPE. That covers resource plans every three years, certificates for new plants, abandonment approvals for retirements and data center tariffs. Its docket system is PRCe360 (`e360.prc.nm.gov`). It is open to guests, and documents download through a token request. The old e-docket addresses are dead.
- **Air permits.**
  - The New Mexico Environment Department Air Quality Bureau permits everything outside Bernalillo County. Its complete record is APMAP, a facility map with an open data service. Every facility has an AI number and a public document collection on `cloud.env.nm.gov`.
  - Draft permits at comment are on `env.nm.gov/public-notices/`. Pending work is in the bureau's Coda tables.
  - Bernalillo County (Reeves, Rio Bravo, Albuquerque data centers) is permitted by the City of Albuquerque Air Quality Program.
  - The Navajo Nation (NTEC) is permitted by EPA Region 9. Other tribal land is permitted by EPA Region 6.
- **Utilities and owners to read.**
  - PNM (TXNM Energy): Afton, Lordsburg, Luna share, Reeves, Rio Bravo, La Luz and the 2023 and 2026 resource plans.
  - SPS: Cunningham, Maddox, the 2,088 MW of gas approved May 7, 2026, and the 2026 plan filed October 23, 2026.
  - El Paso Electric: Rio Grande 6 to 9 and the 2026 New Mexico all-source request for proposals.
  - Tri-State: Pyramid, which GEM lacks.
  - NTEC: the San Juan basin gas plant.
  - Saddle Butte: Westside.
  - Lea Power Partners: Hobbs.
  - Freeport-McMoRan: Chino Mines.
  - Farmington: Bluffview.
  - Los Alamos County.
- **Resource plans.**
  - PNM: 2026 plan in case 25-00022-UT. It has a 172 MW gas placeholder.
  - SPS: 2026 plan in case 25-00076-UT. The 2023 plan's portfolio was approved in 2026.
  - EPE: 2025 plan in case 24-00260-UT.
  - Tri-State: plan filed in Colorado, proceeding 23A-0585E.
  - Farmington, Los Alamos County, Kit Carson Electric and the cooperatives.
  - Every plan is listed in `scopes/us-nm/irp_plans.json` and read in full each batch.
- **Data centers.**
  - Already in GEM: Project Jupiter (cancelled as gas; now a fuel cell plan), Lea County Data Center, Roswell Information Park and Site Layer 1.
  - Not in GEM: Zenith Volts in Chaves County, Google in Lea County, Meta Los Lunas (Greater Kudu LLC, diesel emergency engines) and the Santa Teresa sites.
  - Each is answered under `data_centers`.

## Recent events 2024 to 2026

- **2024:**
  - EPE asked to abandon Rio Grande 7 (case 23-00403-UT).
  - The Rio Grande 6 abandonment approved in case 20-00194-UT was due to take effect in October.
  - NTEC's EPA Region 9 docket opened (EPA-R09-OAR-2024-0028).
- **2025:**
  - Saddle Butte applied to NMED for Westside.
  - Site Layer 1 and Project Jupiter filed air applications.
  - Chaves County approved Zenith Volts in August.
  - EPE filed its 2025 plan.
- **2026:**
  - Project Jupiter withdrew its gas turbine permits in April and moved to fuel cells under NMED permit 10883. The December hearing was vacated on November 6.
  - NTEC's draft permit comment period closed May 18.
  - The PRC approved SPS's gas portfolio May 7.
  - Grant County passed a data center moratorium.
  - PNM filed its 2026 plan September 1, and SPS filed its 2026 plan October 23.

## Watch items to raise with the reviewer

- Rio Grande 6: EIA lists it retired in 2025, and GEM says operating.
- Cunningham 1: EIA gives the retirement year as 2024, and GEM gives 2023.
- NTEC gas plant: GEM has 18 units at 60.5 MW, which is 1,089 MW. The EPA draft permit says 742 MW. GEN13-18 is one row of 363 MW.
- Westside: GEM and EIA list 3 units. The NMED application lists 16 engines.
- Pyramid: an operating Tri-State plant of 186 MW (EIA 7975) that GEM lacks.
- Lordsburg: the owner is recorded as "PNM Resources Inc" rather than the operating company. EIA 7967 is missing from Other IDs.
- The PNM and SPS 2023 resource plan placeholders: the 2026 plans supersede them.

## Still open

See `scopes/us-nm/plan.md`, Stage A. Still to find: the PNM and Tri-State queue lists, the Secretary of State search, and the Valencia, Bernalillo, Las Cruces and Sandoval agenda routes.
