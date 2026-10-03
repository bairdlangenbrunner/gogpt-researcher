# Evidence — gogpt batch 20261002_2153_ET (us-ny, discovery)

## lane: monitor

### Gowanus and Narrows repowering (AlphaGen)
  - links: https://www.prnewswire.com/news-releases/alphagen-proposes-repowering-and-battery-projects-to-secure-nycs-long-term-grid-reliability-302714755.html (ok=True, contains_value=True)
  - links: https://www.nyiso.com/documents/20142/16004172/2026-Q1-STAR-Report-Final.pdf/a5fd3388-ea22-ff21-7f95-490356af30f5 (ok=True, contains_value=True)
  - links: https://www.eenews.net/articles/plans-to-repower-2-peaker-plants-floated-in-new-york-city/ (ok=True, contains_value=True)
  - links: https://www.rtoinsider.com/128325-alphagen-proposes-repowering-to-meet-nyc-reliability-need/ (ok=True, contains_value=True)
- confidence: medium (independent: True)
- notes: AlphaGen, the ArcLight affiliate that manages the Gowanus and Narrows barge plants in Brooklyn, proposed on March 16, 2026 to replace the six existing barges with three new fast-start barges of 273 MW each, 819 MW in all, burning natural gas or ultra-low sulfur diesel and described as hydrogen-ready, plus a 150 MW battery at Gowanus and a 126 MW battery at its Astoria site. The proposal answered Con Edison's request for information on meeting a New York City reliability need. NYISO's first-quarter 2026 reliability report mentions the proposed Gowanus repowering with hydrogen-capable turbines at 819 MW nameplate, and E&E News and RTO Insider covered the proposal in March 2026. There is no air permit application, no state siting application, no interconnection queue entry (an earlier 549 MW Gowanus repowering entry was withdrawn in January 2023, and a 2019 siting case for eight new units was withdrawn), no turbine order and no schedule. The state Public Service Commission's December 2025 order steers Con Edison toward non-emitting solutions, so the gas build is uncertain. The existing barges are staged as new plants in this batch; the earlier watch item in the New York update batch is replaced by this one. Recheck after Con Edison selects solutions or a permit application appears.

## lane: newplants

### Gowanus Gas Turbines generating station
**Action:** Create a new plant named Gowanus Gas Turbines generating station in New York, United States. Set Owner(s) to Alpha Generation LLC at 100 percent and Operator(s) to Alpha Generation, both existing entities, and set the parents the same way as the Astoria generating station record. Set the location to latitude 40.6635, longitude -74.0051, accuracy approximate, city Brooklyn, and add EIA: 2494 to Other IDs (location). Then add the four barge units listed below. Add the links to the matching Data Source boxes.
- `Owner(s)`: `` -> `Alpha Generation LLC [100%]`
- `Operator(s)`: `` -> `Alpha Generation`
- `Latitude`: `` -> `40.6635`
- `Longitude`: `` -> `-74.0051`
- `Location accuracy`: `` -> `approximate`
- `City`: `` -> `Brooklyn`
  - Owners Data Source: https://documents.dps.ny.gov/public/Common/ViewDoc.aspx?DocRefId=%7B50EEA8CD-58A9-40FC-87B5-3DC6E1CE3D4E%7D (ok=True, contains_value=True)
  - Owners Data Source: https://www.prnewswire.com/news-releases/arclight-creates-alphagen-to-manage-one-of-the-largest-power-infrastructure-portfolios-in-the-united-states-302031341.html (ok=True, contains_value=True)
  - Owners Data Source: https://www.prnewswire.com/news-releases/alphagen-withdraws-retirement-notices-for-gowanus--narrows-generating-stations-following-nyiso-reliability-determinations-302743905.html (ok=True, contains_value=True)
  - Operators Data Source: https://documents.dps.ny.gov/public/Common/ViewDoc.aspx?DocRefId=%7BCAC45C80-A88F-425D-9511-1C6525605C3D%7D (ok=True, contains_value=True)
  - Operators Data Source: https://alphagen.com/portfolio/gowanus/ (ok=True, contains_value=True)
  - Location Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Location Data Source: https://documents.dps.ny.gov/public/Common/ViewDoc.aspx?DocRefId=%7B50EEA8CD-58A9-40FC-87B5-3DC6E1CE3D4E%7D (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: Gowanus is a floating peaking plant in Gowanus Bay, Sunset Park, Brooklyn (EIA plant 2494, entrance at 420 2nd Avenue). It has four barges that each carry eight 20 MW simple-cycle turbines, 640 MW nameplate in all, in service since 1971. Barges 1 and 4 burned oil only and were retired in November 2022. Barges 2 and 3 burn gas or distillate oil and still run; the owner's July 2025 notice to retire them in July 2026 was withdrawn on April 16, 2026 after NYISO found the units are needed through May 1, 2029. The plant is not in GEM. Its neighbor, the 94 MW New York Power Authority plant called Gowanus 5 and 6 in the Gold Book, is a separate plant and is not in GEM either (see the Vernon Boulevard and Pouch records for the same fleet). The legal owner is Astoria Generating Company, L.P., a wholly owned subsidiary of Eastern Generation, LLC, which the ArcLight affiliate Alpha Generation (AlphaGen) has managed since January 2024. GEM's existing Astoria and Arthur Kill records for the same company carry Alpha Generation LLC as owner and Alpha Generation as operator, so these records follow that convention. Parents follow the Astoria generating station record: ArcLight Capital Partners LLC 50 percent, ACH GP LLC 25 percent, ACHP II LP 12.5 percent, ACHP LP 12.5 percent. Capacity is entered as engine sets (eight turbines of 20 MW per barge), which is how GEM already records the New York Power Authority's two-turbine Hell Gate plant. Each turbine on its own is under the 50 MW threshold, so the plant is in scope only if the barge counts as one unit; the turbine model (reported elsewhere as the Pratt and Whitney FT4, an aircraft-derived design) is not named in any source I could verify. Coordinates are the EIA plant point; NYISO's generator list puts the barges about 250 meters away, so the location is marked approximate. AlphaGen's March 2026 proposal to replace the six Gowanus and Narrows barges with three new 273 MW barges is a separate watch item in this batch.

### Narrows Gas Turbines generating station
**Action:** Create a new plant named Narrows Gas Turbines generating station in New York, United States. Set Owner(s) to Alpha Generation LLC at 100 percent and Operator(s) to Alpha Generation, both existing entities, and set the parents the same way as the Astoria generating station record. Set the location to latitude 40.648611, longitude -74.02083, accuracy approximate, city Brooklyn, and add EIA: 2499 to Other IDs (location). Then add the two barge units listed below. Add the links to the matching Data Source boxes.
- `Owner(s)`: `` -> `Alpha Generation LLC [100%]`
- `Operator(s)`: `` -> `Alpha Generation`
- `Latitude`: `` -> `40.648611`
- `Longitude`: `` -> `-74.02083`
- `Location accuracy`: `` -> `approximate`
- `City`: `` -> `Brooklyn`
  - Owners Data Source: https://documents.dps.ny.gov/public/Common/ViewDoc.aspx?DocRefId=%7B50EEA8CD-58A9-40FC-87B5-3DC6E1CE3D4E%7D (ok=True, contains_value=True)
  - Owners Data Source: https://extapps.dec.ny.gov/data/dar/afs/permits/prr_261020008600011_r3_1.pdf (ok=True, contains_value=True)
  - Owners Data Source: https://www.prnewswire.com/news-releases/arclight-creates-alphagen-to-manage-one-of-the-largest-power-infrastructure-portfolios-in-the-united-states-302031341.html (ok=True, contains_value=True)
  - Owners Data Source: https://www.prnewswire.com/news-releases/alphagen-withdraws-retirement-notices-for-gowanus--narrows-generating-stations-following-nyiso-reliability-determinations-302743905.html (ok=True, contains_value=True)
  - Operators Data Source: https://extapps.dec.ny.gov/data/dar/afs/permits/prr_261020008600011_r3_1.pdf (ok=True, contains_value=True)
  - Operators Data Source: https://www.alphagen.com/compliance/plant/narrows/ (ok=True, contains_value=True)
  - Location Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Location Data Source: https://extapps.dec.ny.gov/data/dar/afs/permits/prr_261020008600011_r3_1.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: Narrows is a floating peaking plant in Bay Ridge Channel, Sunset Park, Brooklyn (EIA plant 2499, entrance at 54th Street off 1st Avenue). Two barges each carry eight 22 MW simple-cycle turbines, 352 MW nameplate in all, in service since 1972 and burning gas or distillate oil. The company's own page gives 322 MW, which looks like a summer rating. The owner's July 2025 notice to retire the plant in July 2026 was withdrawn on April 16, 2026 after NYISO found the units are needed through May 1, 2029. The plant is not in GEM. Owner, operator and parents follow the Gowanus record: the legal owner is Astoria Generating Company, L.P. (the holder of state air permit 2-6102-00086/00011), a subsidiary of Eastern Generation, LLC, managed by Alpha Generation; GEM's existing records for the same company use Alpha Generation LLC. Parents follow the Astoria generating station record: ArcLight Capital Partners LLC 50 percent, ACH GP LLC 25 percent, ACHP II LP 12.5 percent, ACHP LP 12.5 percent. Capacity is entered as engine sets of eight turbines, as for Gowanus, and the same scope caution applies: each turbine on its own is under 50 MW. Coordinates are the EIA plant point; NYISO's generator list gives a point about 3 kilometers inland that cannot be right, so the location is marked approximate. AlphaGen's March 2026 proposal to replace the Gowanus and Narrows barges is a separate watch item in this batch.

### Pouch Terminal power station
**Action:** Create a new plant named Pouch Terminal power station in New York, United States, if the reviewer agrees a 47 MW single-turbine plant belongs in the tracker (GEM already has Brentwood and North 1st at 47 MW). Set Owner(s) to New York Power Authority at 100 percent and Operator(s) to New York Power Authority (existing entity), with no parent. Set the location to latitude 40.6182, longitude -74.06849, accuracy exact, city Staten Island, and add EIA: 8053 to Other IDs (location). Then add unit 1 as listed below. Add the links to the matching Data Source boxes.
- `Owner(s)`: `` -> `New York Power Authority [100%]`
- `Operator(s)`: `` -> `New York Power Authority`
- `Latitude`: `` -> `40.6182`
- `Longitude`: `` -> `-74.06849`
- `Location accuracy`: `` -> `exact`
- `City`: `` -> `Staten Island`
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://19january2017snapshot.epa.gov/sites/production/files/2015-08/documents/nypapouch_decision2005.pdf (ok=True, contains_value=True)
  - Owners Data Source: https://edge.sitecorecloud.io/newyorkpowe1810-nypa32f6-prodnewd354-e629/media/Feature/nypa-sites/small-natural-gas-media/SNGPP-Transition-Plan.pdf (ok=True, contains_value=True)
  - Operators Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Operators Data Source: https://19january2017snapshot.epa.gov/sites/production/files/2015-08/documents/nypapouch_decision2005.pdf (ok=True, contains_value=True)
  - Location Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Location Data Source: https://19january2017snapshot.epa.gov/sites/production/files/2015-08/documents/nypapouch_decision2005.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: Pouch Terminal is one of the New York Power Authority's eleven small gas plants of 2001 (EIA plant 8053, at 143 Edgewater Street, Rosebank, Staten Island). It has one 47 MW LM6000 turbine, which is below GEM's 50 MW threshold; see the unit note for why it is staged anyway. The Power Authority owns and operates it; no parent applies. The 2023 state budget law requires the Authority to stop gas generation at these plants by the end of 2030. The May 2025 transition plan names Pouch as one of five sites where a battery is planned after the turbine is removed, under a non-binding term sheet signed in April 2025. The 2026 Gold Book, Table IV-6, lists Pouch with a December 31, 2030 date and no deactivation notice. The current state air permit was not found; the 2005 federal order on the original permit is the location source. Coordinates are the EIA plant point.

### Vernon Boulevard power station
**Action:** Create a new plant named Vernon Boulevard power station in New York, United States. Set Owner(s) to New York Power Authority at 100 percent and Operator(s) to New York Power Authority (existing entity), with no parent. Set the location to latitude 40.7537, longitude -73.9508, accuracy exact, city Long Island City, and add EIA: 7909 to Other IDs (location). Then add unit 1 as listed below. Add the links to the matching Data Source boxes.
- `Owner(s)`: `` -> `New York Power Authority [100%]`
- `Operator(s)`: `` -> `New York Power Authority`
- `Latitude`: `` -> `40.7537`
- `Longitude`: `` -> `-73.9508`
- `Location accuracy`: `` -> `exact`
- `City`: `` -> `Long Island City`
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://extapps.dec.ny.gov/data/dar/afs/permits/prr_263040137700003.pdf (ok=True, contains_value=True)
  - Owners Data Source: https://edge.sitecorecloud.io/newyorkpowe1810-nypa32f6-prodnewd354-e629/media/Feature/nypa-sites/small-natural-gas-media/SNGPP-Transition-Plan.pdf (ok=True, contains_value=True)
  - Operators Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Operators Data Source: https://extapps.dec.ny.gov/data/dar/afs/permits/prr_263040137700003.pdf (ok=True, contains_value=True)
  - Location Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Location Data Source: https://extapps.dec.ny.gov/data/dar/afs/permits/prr_263040137700003.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: Vernon Boulevard is one of the eleven small gas plants the New York Power Authority built in 2001 (EIA plant 7909, at 42-30 Vernon Boulevard, Long Island City, Queens). It has two 47 MW LM6000 turbines. GEM already holds the sister plants Brentwood, Harlem River Yard, Hell Gate, Joseph J. Seymour and North 1st, but not this one, nor Pouch (staged in this batch), nor the Gowanus 5 and 6 and Kent plants in Brooklyn. The Power Authority owns and operates it; no parent applies. The 2023 state budget law requires the Authority to stop gas generation at these plants by the end of 2030, and its May 2025 transition plan says a plan for the Vernon site is still to come because a 2001 settlement with a neighboring studio complicates the site's future. The 2026 Gold Book, Table IV-6, lists Vernon Blvd 2 and 3 with a December 31, 2030 date and notes that no deactivation notice has been filed. Coordinates are the EIA plant point.
