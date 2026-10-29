# Illinois air permit sweep for new or proposed gas and oil power plants

Run date: 2026-10-21. Downloaded files and raw harvests are in /private/tmp/claude-501/-Users-baird-Dropbox--git-ALL--github-repos-gem-gogpt-researcher/9a2b433e-bde4-4755-9675-4269f026b73a/scratchpad/permits/ (archive.json, current.json, docs/, rblc/).

## Bottom line

The permit record shows no new or proposed gas or oil power plant in Illinois beyond the two GEM already has. Every power-related construction permit found maps to Lincoln Land Energy Center or Broadwing Energy Center, or to the existing Zion Energy Center. Three of the findings change what GEM has recorded.

1. Broadwing Energy Center: the final construction permit and PSD approval was issued 14 October 2026. Size is one combustion turbine with duct burner, 452 MW gross at ISO conditions (design net about 418 MW at 102 F and 467 MW at 18 F). GEM has 400 MW and "pre-construction". Status should move to permitted, still pre-construction.
2. Lincoln Land Energy Center: the permit was initially issued 29 July 2022 and extended twice. The second extension (issued 21 July 2025) moves the deadline to start construction to 21 January 2027. The permit describes two combined-cycle turbines. The 2021 project summary calls the plant 1,100 MW nominal (design net about 1,055 MW at 92 F and 1,118 MW at 20 F). GEM has 1,276 MW.
3. Zion Energy Center (GEM: operating, 597 MW): a 2026 permit revision allows burning distillate oil in the three simple-cycle turbines during grid emergencies, within the existing 500-hour yearly oil limit. Final revised permit issued 28 July 2026. This is a possible fuel-field note (gas with oil backup), not a new plant.

## (a) Candidate table

Scope tested: 50 MW or more gas or oil generation, including captive power. Emergency-only generator sets are out of scope.

| Facility | City, county | Applicant or owner | Equipment and MW | Permit type and number | Permit date and status | Exact URL that states it | In il_gem_plants.txt? |
|---|---|---|---|---|---|---|---|
| Broadwing Energy Center (ID 115015BWL) | Decatur, Macon | Broadwing Energy LLC (permittee address Houston, Texas) | One gas combustion turbine plus HRSG and duct burner, cogeneration with carbon capture and storage. 452 MW gross at ISO, up to 1.8 million lb/h steam. Serves ADM east Decatur complex, rest sold to MISO. Responsiveness summary mentions a Google power purchase agreement | Construction permit and PSD approval, application 25040003 | Received 4 Apr 2025. Draft and hearing 21 May 2026, comments closed 22 Jun 2026. Final permit issued 14 Oct 2026 | Project summary https://webapps.illinois.gov/EPA/WebSiteApi/api/PublicNotices/GetAirPermitDocument/10283 ; final permit https://webapps.illinois.gov/EPA/WebSiteApi/api/PublicNotices/GetAirPermitDocument/10625 ; responsiveness summary .../GetAirPermitDocument/10626 | Yes, Broadwing Energy Center, 400 MW, pre-construction. Capacity and status need update |
| Lincoln Land Energy Center (ID 167085ABB) | Pawnee, Sangamon | Lincoln Land Energy Center, LLC (Princeton, NJ) | Two combined-cycle combustion turbines, about 1,100 MW nominal | Construction permit and PSD approval, application 18040008 | Initially issued 29 Jul 2022. First extension 22 Jan 2024. Second extension 21 Jul 2025, construction must start by 21 Jan 2027. Not yet built | Second extension https://webapps.illinois.gov/EPA/WebSiteApi/api/PublicNotices/GetAirPermitDocument/9857 (scanned image, read by OCR) ; first extension .../9294 ; 2021 project summary .../7738 | Yes, Lincoln Land energy center, 1,276 MW. Permit year is 2022 (GEM note says 2018 permit, 2022 draft), extensions are new facts |
| Zion Energy Center (ID 097200ABB) | Zion, Lake | Zion Energy, LLC | Three simple-cycle turbines, up to 480 MW nominal peaker. Revision adds distillate oil use in grid emergencies | Construction permit and PSD revision, 99110042 | Draft 27 Apr to 27 May 2026. Final revised permit 28 Jul 2026 | Project summary https://webapps.illinois.gov/EPA/WebSiteApi/api/PublicNotices/GetAirPermitDocument/10339 ; final .../10511 | Yes, Zion energy center, 597 MW operating (GEM figure differs from the 480 MW nominal in the permit text, probably nameplate versus nominal) |

No other candidate at or above 50 MW was found in the Illinois EPA construction permit record, RBLC, or the Title V and FESOP notice lists for 2022 to 2026.

### 20 to 50 MW candidates (low priority)

None found as new projects in the permit record. Nothing in the 2021 to 2026 notice list is a new 20 to 50 MW gas or oil generator.

### Looked at and ruled out (power-adjacent permits)

| Facility | Permit | Why out of scope |
|---|---|---|
| Compass Datacenters ORD I, Hoffman Estates (23110012, draft 4 Jun 2024) | Construction | 205 diesel emergency generators (200 at 2,000 kWe, 5 at 1,250 kWe). Emergency backup only. .../GetAirPermitDocument/9420 |
| Aligned Data Centers EGV, Elk Grove Village (24050021, final Aug 2025) | Construction | 112 diesel emergency generator sets at 3,000 kWe, emergency only. .../9820 |
| Aligned Energy, Northlake (21050040, 2021) | Construction | 49 diesel emergency generators at 3,000 kW plus 2 at 500 kW, emergency only. .../7659 |
| CyrusOne, Aurora (17060002, final 21 Jul 2026) | Title V, new major source | 91 diesel emergency generators. .../10254 |
| Other data centers with FESOP notices (Equinix CH-5, Stream, T5 Chicago II, SDC CHI II Busse, Ensono, Elk Grove CHI10-12) | FESOP | Titles and SIC codes 7374 and 7376 only. I did not open each one. Their documents are fetchable the same way if a reviewer wants them checked, but the data center permits I did open were all emergency generators |
| Cronus Chemicals, Tuscola (19110020, final 21 Dec 2023) | Construction PSD | Ammonia plant. Has a steam turbine generator of about 8 MW fed by waste heat, not a fired generator. .../9257 |
| ADM Decatur east and west soybean plants (21060028 final May 2024, 06120051 Aug 2022) | Construction PSD | Soybean process changes, no power generation |
| Exxon Mobil Channahon, Marquis Carbon Capture Hennepin, CITGO Lemont, Nucor Kankakee, Granite City Works, East Dubuque Nitrogen, Aux Sable Morris, Incobrasa, ethanol plants | Construction | Process or boiler permits. Titles only, not opened. RBLC shows boilers, heaters or flares for those that have RBLC entries |

## Existing plants that are not in GEM's Illinois list (secondary, from a different source)

These are not new projects. They came out of the cross-check against the EIA-860M file already in the repo (work/eia/august_generator2026.xlsx, gas and oil fuel codes, plants whose EIA plant ID is not in il_gem_plants.txt, 15 MW and up). The Illinois EPA operating-permit lists confirm that several of them hold Title V permits. I did not verify their GEM scope status. Listing them here in case the research pass also wants existing-plant gaps.

| EIA plant | County | Nameplate MW | Note |
|---|---|---|---|
| MPH Elwood (69979) | Will | 384 | Title V renewal notice 2025-11-27 (MPH Elwood LLC). EIA status out of service |
| Tilton (7760) | Vermilion | 188 | Tilton Energy Center Title V renewal Aug 2025 |
| Alsey (7818) | Scott | 173 | Prairie Power Inc Title V |
| University of Illinois Abbott Power Plant (54780) | Champaign | 80 | Captive combined heat and power |
| Moline (899) | Rock Island | 72 | Moline Combustion Turbines Title V renewal Mar 2026 |
| University of Illinois Chicago cogeneration (54044) | Cook | 60 | Captive |
| Ingredion, Bedford Park (54556) | Cook | 55 | Captive, food processing |
| ExxonMobil Joliet Refinery (50627) | Will | 43 | Captive, below threshold |
| Waterloo (971), Princeton (957), Winnetka (972), Geneva (56462), Geneseo (944), Factory (8016), Pearl Station (6238), Sullivan (969), Peru, Marshall, Breese and others | various | 15 to 38 each | Municipal turbines and engines, 20 to 50 MW low priority group |

Note the il_gem_plants.txt file does list Zion and several others only by EIA ID, and the first EIA-ID match I ran treated float IDs wrongly, so I reran with integer IDs. The table above comes from the corrected run.

## (b) Sources worked

1. Illinois EPA Bureau of Air public notices, current and archive.
   - The page https://epa.illinois.gov/public-notices/boa-notices.html builds its table in the browser. The script (/content/dam/soi/en/web/epa/javascript-files/boa-notices.js) calls https://webapps.illinois.gov/EPA/WebSiteApi/api/PublicNotices/. The archive page script is epa-air-permit-search.js.
   - Endpoints: GetCurrentAirPublicNotices/ (GET) and GetArchivedAirPublicNotices/ (POST), both DataTables server-side, which need all eight column parameters or they return an error. Also GetPermitTypes, GetPermitDocumentsList/?facilityId=&permitId=, and GetAirPermitDocument/{PublicNoticeId} (PDF).
   - Read: 22 current notices and 2,163 archive records (the archive includes the current ones). Date range of records with dates: 2004 to 2026, with the bulk 2014 to 2026. 877 records have no public notice end date. I filtered by permit type (Construction, PSD, NANSR, Title V Construction, State Construction: 146 records) and by SIC 4911, 4931, 4939, 4961, 7374, 7376 (power and data centers).
   - Downloaded and read in full (text extraction, OCR where scanned): Broadwing (10 documents), Zion (9), Lincoln Land (36, read the final permit extensions by OCR and the 2021 project summary by text), ADM (2024 and 2022 project summaries), Compass, Aligned EGV, Aligned Northlake, Cronus, CyrusOne (7). The Broadwing final permit PDF and the Lincoln Land extension PDFs are scanned images with no text layer, so I read their first pages by OCR with tesseract. The rest of those permits, such as unit-by-unit limits, I did not read.
   - Coverage limit: only permits that go to public notice appear here (PSD, major sources, Title V, and some others). Smaller construction permits that need no public notice, for example a synthetic-minor engine plant under 100 tons per year of NOx, are not in this list.
2. Illinois EPA Document Explorer, https://webapps.illinois.gov/EPA/DocumentExplorer/. Loaded fine. It searches by facility name, address, city, zip, county or interest ID only (Attributes and Geography tabs). It cannot search by permit type, equipment or date, so it cannot list new projects. A test search by name returned an empty response to my plain-GET probe, which I did not pursue because the form posts through a script and no listing function exists. Not used as a source.
3. RBLC. The old cfpub.epa.gov/rblc URLs now return 404. The current tool is https://cdxoarapps.epa.gov/oar-rblc/ (linked from https://www.epa.gov/catc/rblc), an Angular app. I read its JavaScript and found the JSON API at /oar-rblc/api/. Reference calls: reference/permitting-authorities, reference/states. Search: POST rblc/search and rblc/keyword-search with fields keywords, legacyProcessCode, processName, unitType, pollutantId, controlMethod, state, facilityName, startDate and endDate (MM/DD/YYYY), tabIndex. A state-only query (state "IL", 01/01/2015 to 12/31/2026) returned 309 limit rows, not truncated, covering 17 Illinois facility permits dated 2015 to 2025. Twenty keyword searches (turbine, combined cycle, simple cycle, engine, generator, peaking, natural gas, combustion and others) returned 16 distinct permits. The only Illinois turbine entries from 2020 on are Lincoln Land (29 Jul 2022, combined-cycle turbines). Earlier ones are Invenergy Nelson Expansion 2016 (two simple-cycle turbines), CPV Three Rivers 2018, Hoosier Energy landfill gas turbines 2017, Jackson Energy Center 2018. RBLC has no Broadwing entry because that permit was issued only on 14 Oct 2026. The filter by process code 15.110 and similar did not run because I used the state-only search, which returns every process type, so I filtered locally.
4. US EPA Region 5 PSD and Title V pages. https://www.epa.gov/caa-permitting/caa-permits-issued-epa-region-5 returned 404. Illinois took over PSD permitting under its own rules (35 IAC Part 204, effective 12 Oct 2021), so Region 5 no longer issues Illinois PSD permits, which is consistent with the Illinois EPA notices carrying them. No other Region 5 page tried. Not read.
5. Illinois Pollution Control Board and county notices: not worked because nothing above pointed to them.
6. One general web search for Illinois gas plants and data center permits turned up Lincoln Land, an old Taylorville Energy Center reconsideration (GEM already lists Taylorville as cancelled coal) and the CyrusOne notice. No new project.
7. Illinois EPA permit annual summary PDFs (CAAPP, FESOP, lifetime sources): statistics only, not project lists. Not read.

## What I could not read or do

- A list of pending air permit applications (applications received but not yet noticed). I found no public page for it at the Illinois EPA. I tried the Bureau of Air notices page, the IEPA Permit Portal page, the Air Permits page, the Permit Annual Summary page and Document Explorer. None lists applications.
- Construction permits with no public notice. See coverage limit above. A person could request these from the Illinois EPA Bureau of Air records unit.
- The unit-level contents of the final Broadwing permit (scanned). Capacity comes from the project summary and responsiveness summary text.
- The FESOP data center notices listed above, not opened one by one.
- Illinois EPA permit documents before 2021 and the 877 archive records with no notice date were scanned only by facility name, SIC and type, not opened.
