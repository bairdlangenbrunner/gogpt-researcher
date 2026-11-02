# United States — North Dakota

Scope: 36 unit rows across 14 plants in the pull of 2026-10-29 at 14:46 Eastern (four operating plants, one cancelled, the rest announced, pre-construction or under construction). Assigned to Amalia Llano for the Q4 2026 cycle, and she was editing the state on 2026-10-28 and 2026-10-29 (Base Electron, Polaris Forge 1 and 2, both Applied Digital plants and Nakota carry her recent edits). Three utility rows on the US IRPs tab (Montana-Dakota Utilities, Otter Tail Power, Minnkota Power Cooperative). No captive LNG sheet rows. The roster row still shows the 24 rows of the campaign start. Drafted 2026-10-29 before any sweep; the plan is `scopes/us-nd/plan.md`.

## State context

- Two grid operators. The Southwest Power Pool covers most of the state (Basin Electric Power Cooperative, Montana-Dakota Utilities, Western Area Power Administration). The Midcontinent Independent System Operator covers the eastern edge (Otter Tail Power, Minnkota Power Cooperative, Great River Energy, Northern States Power around Fargo and Grand Forks). Both queues must be read for every batch.
- The regulator is the North Dakota Public Service Commission. Generating plants of 50 MW or more need a certificate of site compatibility under Chapter 49-22; a developer first files a letter of intent, and a jurisdictional determination case decides whether a plant is exempt (Applied Digital's backup generation, case PU-26-155, decided 2026-04-24). Case numbers are a prefix, a two-digit year and a sequence (PU-25-086 is Bison). The case search at https://apps.psc.nd.gov/cases/pscasesearch answers a plain form post with no token; each case page lists its docket entries, and the documents sit in a folder index at https://www.psc.nd.gov/webdocs/case/YY-NNNN/ as PDFs. Descriptions carry entity names, so "data center" finds nothing; search by company. `scopes/us-nd/harvest_psc.py` reads all of this ahead of a sweep.
- Air permits come from the Department of Environmental Quality, Division of Air Quality. Public comment notices are per facility at https://deq.nd.gov/AQ/PublicCom.aspx, each pointing at a PDF under deq.nd.gov/AQ/Notices/<Facility>/. The directory itself refuses listing, but the Wayback Machine's CDX index lists 288 past notice PDFs under about 45 facility folders (older ones under ndhealth.gov). Known folders: BasinElectricBison (the November 2025 notice of intent letter) and AppliedDigital (the May 2026 letter and notice). The CERIS-ND portal at https://ceris.deq.nd.gov/ext/nsite/ is a single-page app; its public notices list answers anonymously but carried only solid waste notices in October 2026, and site search needs a session. `scopes/us-nd/harvest_permits.py` reads the Air Quality pages and the Wayback copies.
- Utilities and developers: Basin Electric (Bison, Pioneer, Lonesome Creek, River Run with NextEra), Great River Energy (Spiritwood), Minnkota (Harmony Township plant), Montana-Dakota Utilities (Heskett), Otter Tail Power, Northern States Power (Xcel), Rainbow Energy Center (Coal Creek), Applied Digital, Nakota Energy, Base Electron with Babcock and Wilcox.
- Data center load drives most new gas generation: Applied Digital's Polaris Forge campuses at Ellendale (Dickey County) and Harwood (Cass County), Nakota's Williston campus, Base Electron's campus at Center (Oliver County), and the Geronimo Power proposal in Harmony Township. Bakken flare gas feeds smaller captive generation and bitcoin mining sites.
- The coal fleet (Coal Creek, Antelope Valley, Milton R. Young, Coyote, Leland Olds) is where conversions and co-located gas units would appear; check the unfiltered export's coal rows each cycle.

## Recent events 2024 to 2026

- Bison Generation Station (Basin Electric, Wheelock Township, Williams County): two 745 MW combined cycle units, under construction, 2029 and 2030. Air notice of intent November 2025; commission case PU-25-086 (77 documents); Southwest Power Pool requests GEN-2024-081 and 082 (760 MW nameplate each); EIA plant 69071 lists CT1 and CA1 for 2029 and CT2 and CA2 for 2030, 1,518 MW in total. GEM's Bison has no EIA plant ID yet.
- River Run Energy Center (NextEra and Basin Electric, Stanton, Mercer County): 1,450 MW combined cycle for 2030, memorandum of understanding December 2025, early siting in April 2026. Southwest Power Pool ERAS-2025-011 and 012 list two 750 MW units with the agreement pending and a 2029-09-27 date at Leland Olds.
- Minnkota Power Cooperative announced a 400 MW gas turbine plant in Harmony Township north of Mapleton, Cass County, about one billion dollars, 2031 to 2032, dependent on the Bakken East pipeline (North Dakota Monitor, 2026-10-06). Amalia added it on 2026-10-29 as Minnkota Power Cass power station (L100001089086, one 400 MW unit, announced, 2031); the sweep re-verifies it.
- Northern States Power has an active MISO request J3163 for 481 MW with a simple cycle combustion turbine in Cass County, in service 2028-03-30. Not in GEM as of 2026-10-29.
- Applied Digital: ELN Generation Plant at Ellendale (four engine fleets, 180 to 288 MW each) and FAR Generation Plant at Harwood (two of 288 MW), both pre-construction, from Department of Environmental Quality notices; Polaris Forge 1 (400 MW steam, 2028) and Polaris Forge 2 (280 MW steam, 2028) under construction. Commission cases PU-26-155, PU-24-359, PU-24-330, PU-26-173; Minnkota's Agassiz line case PU-26-022 serves the Harwood campus at 280 MW.
- Base Electron (Center, Oliver County): four 300 MW Babcock and Wilcox boilers with Siemens steam turbines for a data center campus, about 2.4 billion dollars, pre-construction. Montana-Dakota Utilities cases PU-26-219 and PU-26-236 for the APLD BIS-01 site.
- Nakota Data Center Campus Power Plant (Williston): three units of 338 MW of 16.9 MW engines; unit 1 pre-construction for 2027, units 2 and 3 announced.
- Cerilon gas-to-liquids plant (Williams County): commission approval 2024-09-27 in case PU-23-325; each of two phases has a 100 MW steam turbine (65 to 81 MW net) sold to Basin Electric. Scope call open.
- Rainbow Energy was reported in September 2025 to plan 2,100 MW of gas generation near Coal Creek Station; no later document found as of 2026-10-29. MISO S1036 (Great River Energy, McLean County, 400 MW, done 2025) is a surplus interconnection near the same site.
- Heskett Station unit 4 (88 MW gas turbine) started 2024 at Mandan; Pioneer phase IV (two 250 MW turbines and a 112.8 MW engine set) started 2025 at Williston. Xcel Fargo's 400 MW turbine was cancelled in 2022.

## Watch items to raise with the reviewer

- Cerilon's steam turbines on gas-to-liquids process heat: in scope or not.
- River Run at 1,450 MW in GEM against 1,500 MW in the queue.
- Sierra Club "Applied Digital Natural Gas Plant" units 1 to 4 of 300 MW: Polaris Forge or Base Electron.

## Still open

- Everything in the plan's "Known leads" list until the batch runs.
- The Minnkota plan on the US IRPs tab is the 2022 resource plan; the Cass plant is newer than it.
- Five validation fixes: Heskett owner source, Heskett unit 4 replacement link, Spiritwood owner source, Spiritwood location source, Spiritwood carbon capture source.
- Eight plants with approximate or blank coordinates.
- Polaris Forge 1 county typed "Dikey County"; Spiritwood county blank.

## Gotchas

- Amalia's live edits: compare against the fresh export at run time and stage against her values only when a verified source disagrees.
- The EIP sheet's "Brickhouse Power Plant" row points at a plant outside North Dakota; report it as a sheet error, do not match it.
- `worklist.py` writes `work/worklist_us-north-dakota.csv` while every other script uses the `us-nd` tag.
- Queue megawatts are nameplate in the Southwest Power Pool CSV (summer MW is a separate column); GEM takes nameplate.
- Backup engine fleets at the Applied Digital campuses are already GEM plants (ELN and FAR); new permits change their unit counts and megawatts, they do not create new plants.
