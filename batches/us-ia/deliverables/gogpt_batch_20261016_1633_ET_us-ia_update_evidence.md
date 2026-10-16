# Evidence — gogpt batch 20261016_1633_ET (us-ia, update)

Each section below is one group of the GOGPT QC/Country checklist. The records in it are the evidence for ticking that group's boxes; the row numbers are the checklist tab's own.

## Utility resource plans (checklist row 37)

The IRP step read 2 utility rows of the US IRPs tab for this state. The records below come from a plan; the actions workbook's irp_box sheet says which units need the IRP box ticked, and its irp_notes_draft sheet has a draft line per utility for the tab's Notes column.

- Interstate Power and Light Company: 2025 RES. Tracked plants matched: 9
- MidAmerican Energy Company: 2024 RES. Tracked plants matched: 13

Records from a plan:
- G100001092276 / MidAmerican 2024 IRP power station 7 / 1 IRP: change to an existing unit, from the MidAmerican Energy Company plan
- G100001017907 / Burlington Generating Station / Unit 1, timepoint 2: question about existing data, from the Interstate Power and Light Company plan
- G100001092270 / Interstate Power and Light 2024 IRP power station 1 / 1 IRP: question about existing data, from the Interstate Power and Light Company plan
- Interstate Power and Light 2024 IRP power station 1: question about existing data, from the Interstate Power and Light Company plan
- MidAmerican 2024 IRP power station 1: question about existing data, from the MidAmerican Energy Company plan
- Orient Energy Center power station: question about existing data, from the MidAmerican Energy Company plan

## Checklist group 1. Validation report

Edits and questions that fix an error from the GEM validation report.

### G100001054408 / Ames Municipal Power Plant / Unit 7, timepoint 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: Not found. I looked at the Sargent and Lundy project page, the City of Ames electric department page and the EIA-860M table for August 2026. None of them mention carbon capture for Unit 7. Nothing suggests the unit has carbon capture, so the value no stays, but no document states it.
- notes: No document found that states whether Unit 7 has carbon capture.

### G100001017907 / Burlington Generating Station / Unit 1, timepoint 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: Not found. I looked for a document that says whether Burlington Unit 1 has carbon capture. The Environmental Protection Agency letter from March 2022, the Alliant coal ash pages, the EIA-860M table for August 2026 and the Alliant Iowa clean energy page say nothing about carbon capture. The unit burns natural gas in a steam boiler. GEM's current value of no looks right, but I have no source for it.
- notes: A no needs a document that states it. None found.

### G100001054413 / Earl F. Wisdom Generating Station / Unit 1, timepoint 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: Not found. I looked at the Corn Belt Power Cooperative generation page, its 2019 annual report and the EIA-860M table for August 2026. None mention carbon capture. Nothing suggests Unit 1 has it.
- notes: No document states the carbon capture value.

### G100001017855 / Riverside (IA) power station / Unit 5, timepoint 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: Not found. No document I read mentions carbon capture at Riverside Unit 5. The 2015 MidAmerican Energy filing describes it as burning natural gas only. The current value of no is consistent with that, but I have no document that states it.
  - links: https://www.sec.gov/Archives/edgar/data/0000928576/000092857615000020/eei2015.htm (ok=None, contains_value=None)
- notes: I looked at the 2015 MidAmerican Energy filing, a WVIK report and the EIA-860M table for August 2026. None mentions carbon capture.

## Checklist group 2. Blanks and unknowns

Empty or unknown cells that the research filled, and the ones it could not.

### G100001071243 / Bobcat Energy Center / 1
*change to an existing unit; checklist rows 26 (City and state or province filled)*
**Action:** Set City of unit 1 (G100001071243) to Marshalltown. The box is empty now. Add the link below to the Location Data Source box. Keep the links already there.
- `City`: `` -> `Marshalltown`
  - Location Data Source: https://www.alliantenergy.com/news/news-center/2026/081126-bobcat-construction-started (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Alliant Energy press release from August 11, 2026 places the plant in Marshalltown, next to the existing Marshalltown Generating Station.

### G100000403754 / Exira power station / U1
*change to an existing unit; checklist rows 19 (Missing or unknown owner searched)*
**Action:** Set Operator(s) of all 3 units of Exira power station to Missouri River Energy Services [100%]. The box is empty now. Add the link below to the Operators Data Source box on each unit. Keep the links already there.
- `Operator(s)`: `` -> `Missouri River Energy Services [100%]`
  - Operators Data Source: https://www.publicpower.org/periodical/article/missouri-river-energy-services-details-plans-significant-maintenance-work-power-plant (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: An American Public Power Association article from August 2026 says Exira Station is owned by the Western Minnesota Municipal Power Agency and operated by Missouri River Energy Services. The article also describes a fall 2026 maintenance outage, so the plant is running.

### G100001054496 / Orient Energy Center power station / 1
*change to an existing unit; checklist rows 26 (City and state or province filled)*
**Action:** Set City of unit 1 (G100001054496) to Orient. The box is empty now. Add the link below to the Location Data Source box. Keep the links already there.
- `City`: `` -> `Orient`
  - Location Data Source: https://www.kmaland.com/news/midamerican-energy-announces-energy-production-projects-to-meet-growing-demand/article_cc7120aa-f2d1-11ef-a941-b3dede76d9d9.html (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A KMAland article says the plant would be built south of the town of Orient in Adair County. The site is rural, so City is the nearest town.

### G100001055236 / Orient Energy Center power station / 2
*change to an existing unit; checklist rows 26 (City and state or province filled)*
**Action:** Set City of unit 2 (G100001055236) to Orient. The box is empty now. Add the link below to the Location Data Source box. Keep the links already there.
- `City`: `` -> `Orient`
  - Location Data Source: https://www.kmaland.com/news/midamerican-energy-announces-energy-production-projects-to-meet-growing-demand/article_cc7120aa-f2d1-11ef-a941-b3dede76d9d9.html (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A KMAland article says the plant would be built south of the town of Orient in Adair County. The site is rural, so City is the nearest town.

### G100000403018 / Prairie Creek Generating Station / Unit 4- timepoint 2
*change to an existing unit; checklist rows 25 (Location data for every entry)*
**Action:** Leave Latitude of unit Unit 4- timepoint 2 (G100000403018) as 41.9436670. It is still correct. Add the link below to the Location Data Source box. Keep the links already there.
- `Latitude`: `41.9436670` -> `41.9436670`
  - Location Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The EIA-860M table for August 2026 puts the plant at 41.944039, -91.63917. GEM's value is about 40 meters away, which is the same spot. The value is left as it is and only the source is added.

### G100000403018 / Prairie Creek Generating Station / Unit 4- timepoint 2
*change to an existing unit; checklist rows 25 (Location data for every entry)*
**Action:** Leave Longitude of unit Unit 4- timepoint 2 (G100000403018) as -91.6386920. It is still correct. Add the link below to the Location Data Source box. Keep the links already there.
- `Longitude`: `-91.6386920` -> `-91.6386920`
  - Location Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The EIA-860M table for August 2026 puts the plant at -91.63917. GEM's value is about 40 meters away, which is the same spot.

### G100000403018 / Prairie Creek Generating Station / Unit 4- timepoint 2
*change to an existing unit; checklist rows 25 (Location data for every entry), 42 (Exact location for approximate operating units (optional))*
**Action:** Leave Location accuracy of unit Unit 4- timepoint 2 (G100000403018) as exact. It is still correct. Add the link below to the Location Data Source box. Keep the links already there.
- `Location accuracy`: `exact` -> `exact`
  - Location Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The EIA coordinates fall on the plant site, within about 40 meters of GEM's point.

### G100001017855 / Riverside (IA) power station / Unit 5, timepoint 2
*change to an existing unit; checklist rows 26 (City and state or province filled)*
**Action:** Leave City of unit Unit 5, timepoint 2 (G100001017855) as Davenport. It is still correct. Add the link below to the Location Data Source box. Keep the links already there.
- `City`: `Davenport` -> `Davenport`
  - Location Data Source: https://www.wvik.org/post/utility-closes-its-last-qc-coal-plant (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A WVIK public radio report on the closing of the last Quad Cities coal plant describes the MidAmerican Energy Riverside plant in Davenport.

### G100000414185 / Summit Lake power station / IC
*change to an existing unit; checklist rows 26 (City and state or province filled)*
**Action:** Set City of unit IC (G100000414185) to Creston. The box is empty now. Add the link below to the Location Data Source box. Keep the links already there.
- `City`: `` -> `Creston`
  - Location Data Source: https://www.businessrecord.com/?p=11068 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Business Record article on the Central Iowa Power Cooperative plan to rebuild its Creston generating station describes the Summit Lake plant in Creston, Iowa, with new natural gas reciprocating engines. So the city is Creston.

### G100001071243 / Bobcat Energy Center / 1
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: The EIA-860M table for August 2026 has plant code 1077, Sutherland, in Marshall County, 0.3 km from GEM's coordinates. Its generator 1 (37.5 MW) and generator 3 (81.6 MW) are retired natural gas steam turbines from 1955 and 1961, both retired in 2017. Bobcat is a new 720 MW combustion turbine plant built next to the Marshalltown Generating Station, which is EIA plant 1068 and plant 58236. So Sutherland is the nearby retired plant and not this project. I would not link Bobcat to plant 1077 or to its generators. Please check whether a retired Sutherland record exists in GEM.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: I found no document that says Bobcat is on the former Sutherland site. Alliant says only that it is next to Marshalltown Generating Station.

### G100001017907 / Burlington Generating Station / Unit 1, timepoint 2
*question about existing data*
- about: source
- recommendation: The Gazette link in GEM's Status and Start year sources, thegazette.com/energy/why-power-plants-are-using-natural-gas-instead-of-coal, now returns not found. The same article is live at thegazette.com/environment-nature/why-power-plants-are-using-natural-gas-instead-of-coal. It says Burlington should resume operations after a coal to gas transition.
  - links: https://www.thegazette.com/environment-nature/why-power-plants-are-using-natural-gas-instead-of-coal/ (ok=None, contains_value=None)
- notes: Do not drop the old link. The newer address works.

### G100001071242 / Cedar River Generating Station / 1
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- recommendation: Coordinates are copied from Prairie Creek, which is the right site. A Corridor Business article says the plant goes on the vacant coal pile area of the Prairie Creek site at 3300 C Street Southwest, Cedar Rapids. I found no document with exact coordinates, so the approximate flag stays.
  - links: https://corridorbusiness.com/alliant-plans-for-natural-gas-fired-power-plant-at-prairie-creek-moving-forward/ (ok=None, contains_value=None)
- notes: No change to the coordinates.

### G100000403754 / Exira power station / U1
*question about existing data*
- about: Capacity (MW)
- recommendation: The EIA table gives 60.5 MW per unit and GEM shows 61.0 MW. The operator's website calls the plant a nominal 140 MW with units of about 47 MW each. No change is proposed, since the difference is small, but the reviewer may want to check which basis GEM uses.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: Capacity figures differ across sources.

### G100001071244 / Hickory Grove Generating Station / 1
*question about existing data*
- about: source
- recommendation: A Scott County meeting minutes file from July 14, 2026 is said in search results to name docket GCU-2026-0001 for this plant. The link returns not found, so I could not confirm the docket number. Please check the commission's filing system for the docket.
- notes: Not verified.

### Lime Creek power station
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: Check whether the single 90.2 MW unit should be two units of 45.1 MW each.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: GEM has one unit at Lime Creek, 90.2 MW, fuel oil, 1991. The EIA-860M table for August 2026 lists plant 7155, Lime Creek, owned by Interstate Power and Light in Cerro Gordo County, as two operating petroleum liquids combustion turbines. Generators 1 and 2 are each 45.1 MW and both date from 1991. The total matches GEM. Only the unit split differs.

### G100001092275 / MidAmerican 2024 IRP power station 6 / 1 IRP
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: The August 2026 EIA-860M table has plant code 1048, Milton L Kapp, in Clinton County, about 2.9 km from GEM's coordinates. Generator 2 is 218.5 MW and generator 1 is 18.8 MW, both retired gas steam units. This placeholder is a future 466 MW turbine set for 2043, not a Kapp unit, so the codes should not be added here. The coordinates may simply sit on the old Kapp site. The reviewer should decide whether to keep them.
- notes: The 2024 study names no site for this turbine. The Kapp retired units are a different kind of unit and capacity. I took the Kapp figures from the brief and did not re-read the EIA file.

### G100001092276 / MidAmerican 2024 IRP power station 7 / 1 IRP
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- recommendation: Leave City blank. The study does not say where this 2044 addition would be built, so no source places it.
  - links: https://www.midamericanenergy.com/media/pdf/mec_resource_evaluation_study_11-1.pdf (ok=None, contains_value=None)
- notes: The plan only lists capacity by year. No site is named.

### G100001054416 / Pleasant Hill power station / 1
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: Units 1 and 2 have no EIA generator number. The EIA table lists generators 1 and 2 as two identical 41.4 MW gas combustion turbines from 1990. Unit 1 matches generator 1 and unit 2 matches generator 2. Please add those as the unit identifiers by hand.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: EIA lists generator 3 at 97.0 MW from 1994, which matches GEM unit 3 that already carries the identifier EIA 3.

### G100001054415 / Pleasant Hill power station / 2
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: This unit matches EIA generator 2, a 41.4 MW gas combustion turbine from 1990. Generator 1 is the identical twin and belongs to unit 1.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: Both 1990 turbines have the same size and start year, so the pairing of unit to generator number cannot be proven from EIA alone.

### G100001017855 / Riverside (IA) power station / Unit 5, timepoint 2
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: Latitude
- recommendation: Not found. I did not find a document that states the plant coordinates, so the location source is still empty. The city is supported by the WVIK report.
  - links: https://www.wvik.org/post/utility-closes-its-last-qc-coal-plant (ok=None, contains_value=None)
- notes: The EIA-860M table does not carry coordinates for retired units.

## Checklist group 3. Status and timeline

Status changes, start and retirement years, planned retirements, Latest Activity.

### G100001071243 / Bobcat Energy Center / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 50 (Other last-minute status changes checked)*
**Action:** Set Status of unit 1 (G100001071243) to construction. It now says pre-construction. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `pre-construction` -> `construction`
  - Status Data Source: https://www.alliantenergy.com/news/news-center/2026/081126-bobcat-construction-started (ok=True, contains_value=True)
  - Status Data Source: https://www.timesrepublican.com/news/todays-news/2026/08/alliants-bobcat-energy-center-receives-air-permit/ (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: An Alliant Energy press release from August 11, 2026 says the Iowa Department of Natural Resources issued the air permit in early August and that construction is underway. The Times-Republican article from August 12, 2026 repeats the release, so this counts as one source. The unit is pre-construction in GEM today. The turbine maker and model are not in any public document I found. The air permit application at the Iowa Department of Natural Resources would likely list them. Latest Activity is left alone because the project is moving.

### G100001071243 / Bobcat Energy Center / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Add the entry below at the top of the Status Detail box of unit 1 (G100001071243), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Alliant Energy announced on August 11, 2026 that the Iowa Department of Natural Resources had issued the air permit the week before and that construction was underway. Major construction and equipment installation are expected to run for about three years.

https://www.alliantenergy.com/news/news-center/2026/081126-bobcat-construction-started
- `Status Detail`: `AM 05/2026: Construction planning and contractor mobilization discussions continued ahead of anticipated groundbreaking. https://www.constructionowners.com/news/bobcat-energy-center-set-to-begin-construction` -> `Alliant Energy announced on August 11, 2026 that the Iowa Department of Natural Resources had issued the air permit the week before and that construction was underway. Major construction and equipment installation are expected to run for about three years.

https://www.alliantenergy.com/news/news-center/2026/081126-bobcat-construction-started

AM 05/2026: Construction planning and contractor mobilization discussions continued ahead of anticipated groundbreaking. https://www.constructionowners.com/news/bobcat-energy-center-set-to-begin-construction`
  - Status Detail: https://www.alliantenergy.com/news/news-center/2026/081126-bobcat-construction-started (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Alliant Energy press release from August 11, 2026 gives these facts.

### G100001071243 / Bobcat Energy Center / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Start year of unit 1 (G100001071243) as 2029. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2029` -> `2029`
  - Start Year Data Source: https://www.alliantenergy.com/news/news-center/2026/081126-bobcat-construction-started (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Alliant Energy press release from August 11, 2026 says the company expects commercial operation in 2029.

### G100001071243 / Bobcat Energy Center / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Capacity (MW) of unit 1 (G100001071243) as 720.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `720.0` -> `720.0`
  - Capacity Data Source: https://www.alliantenergy.com/news/news-center/2026/081126-bobcat-construction-started (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Alliant Energy press release from August 11, 2026 says the plant will have about 720 megawatts of capacity.

### G100001071243 / Bobcat Energy Center / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Owner(s) of unit 1 (G100001071243) as Interstate Power and Light Co [100%]. It is still correct. Add the link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Interstate Power and Light Co [100%]` -> `Interstate Power and Light Co [100%]`
  - Owners Data Source: https://www.sec.gov/Archives/edgar/data/352541/000035254125000081/lnt-20250930.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Alliant Energy quarterly report to the Securities and Exchange Commission for September 2025 says Interstate Power and Light Company applied to the Iowa Utilities Commission to construct, own and operate the 720 MW Bobcat Energy Center.

### G100001017907 / Burlington Generating Station / Unit 1, timepoint 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of all 2 units of Burlington Generating Station as Interstate Power and Light Co [100%]. It is still correct. Add the 2 links below to the Owners Data Source box on each unit. Keep the links already there.
- `Owner(s)`: `Interstate Power and Light Co [100%]` -> `Interstate Power and Light Co [100%]`
  - Owners Data Source: https://www.epa.gov/system/files/documents/2023-10/burlington-petition-november-2021-final-response-march-2022_0.pdf (ok=True, contains_value=True)
  - Owners Data Source: https://www.sec.gov/Archives/edgar/data/352541/000035254125000081/lnt-20250930.htm (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The 2022 Environmental Protection Agency letter says Interstate Power and Light owns and operates the Burlington Generating Station. Alliant's September 2025 quarterly report says Interstate Power and Light applied to the Iowa Utilities Commission to construct, own and operate the 94 MW engines at Burlington.

### G100001094030 / Burlington Generating Station / Unit 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit Unit 2 (G100001094030) to Wärtsilä 18V50. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `Wärtsilä 18V50`
  - Turbine/Engine Equipment Data Source: https://alberici.com/projects/burlington-generating-station/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The contractor Alberici describes the 94 MW Burlington Generating Station as five Wärtsilä 18V50 reciprocating engines with selective catalytic reduction emissions controls. Regulators approved this unit on February 16, 2026, which is within the last year, so Latest Activity is left alone. No construction start or in-service date was found beyond the 2029 target already in GEM.

### G100001071242 / Cedar River Generating Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 50 (Other last-minute status changes checked)*
**Action:** Set Status of unit 1 (G100001071242) to construction. It now says pre-construction. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `pre-construction` -> `construction`
  - Status Data Source: https://alberici.com/projects/cedar-river-generating-station/ (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The contractor Alberici says on its project page that it is the general contractor and is constructing the 94 MW Cedar River Generating Station. KCRG reported in February 2026 that construction was expected to begin in early 2026. This is one source, and it gives no start date. No document gives exact coordinates for the new engines. They are on the former coal pile area of the Prairie Creek site at 3300 C Street Southwest in Cedar Rapids. Latest Activity is left alone because the project is moving.

### G100001071242 / Cedar River Generating Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Set Status Detail of unit 1 (G100001071242) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

The contractor Alberici describes itself as building the plant, with five Wärtsilä 18V50 engines. KCRG reported in February 2026 that construction would begin in early 2026. Alliant still expects the plant to run by June 2027.

https://alberici.com/projects/cedar-river-generating-station/
https://www.kcrg.com/2026/02/09/alliant-energy-plans-new-natural-gas-generating-station-cedar-rapids-coal-era-ends
- `Status Detail`: `` -> `The contractor Alberici describes itself as building the plant, with five Wärtsilä 18V50 engines. KCRG reported in February 2026 that construction would begin in early 2026. Alliant still expects the plant to run by June 2027.

https://alberici.com/projects/cedar-river-generating-station/
https://www.kcrg.com/2026/02/09/alliant-energy-plans-new-natural-gas-generating-station-cedar-rapids-coal-era-ends`
  - Status Detail: https://alberici.com/projects/cedar-river-generating-station/ (ok=True, contains_value=True)
  - Status Detail: https://www.kcrg.com/2026/02/09/alliant-energy-plans-new-natural-gas-generating-station-cedar-rapids-coal-era-ends (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Both pages name the plant and give these facts.

### G100001071242 / Cedar River Generating Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit 1 (G100001071242) to Wärtsilä 18V50. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `Wärtsilä 18V50`
  - Turbine/Engine Equipment Data Source: https://alberici.com/projects/cedar-river-generating-station/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Alberici says the plant has five Wärtsilä 18V50 reciprocating engines with selective catalytic reduction emissions controls.

### G100001071242 / Cedar River Generating Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 19 (Missing or unknown owner searched)*
**Action:** Set Owner(s) of unit 1 (G100001071242) to Interstate Power and Light Co [100%]. It now says Alliant Energy Corp [100%]. Add the link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Alliant Energy Corp [100%]` -> `Interstate Power and Light Co [100%]`
  - Owners Data Source: https://www.sec.gov/Archives/edgar/data/352541/000035254125000081/lnt-20250930.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Alliant's quarterly report to the Securities and Exchange Commission for September 2025 says the Iowa Utilities Commission in June 2025 authorized Interstate Power and Light Company to construct, own and operate the 94 MW Cedar River Generating Station at the Prairie Creek site. So the immediate owner is the Iowa utility and not Alliant Energy Corp, its parent.

### G100001096185 / Emery Station power plant / RH
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Set Status Detail of unit RH (G100001096185) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

In July 2026 Interstate Power and Light filed its certificate application with the Iowa Utilities Commission for the 1,200 MW Riverhawk Energy Center near Emery Station. A decision is expected in the second quarter of 2027, and Alliant expects service in 2031.

https://www.sec.gov/Archives/edgar/data/352541/000035254126000043/lnt-20260630.htm
https://www.alliantenergy.com/our-energy/natural-gas/riverhawk
- `Status Detail`: `` -> `In July 2026 Interstate Power and Light filed its certificate application with the Iowa Utilities Commission for the 1,200 MW Riverhawk Energy Center near Emery Station. A decision is expected in the second quarter of 2027, and Alliant expects service in 2031.

https://www.sec.gov/Archives/edgar/data/352541/000035254126000043/lnt-20260630.htm
https://www.alliantenergy.com/our-energy/natural-gas/riverhawk`
  - Status Detail: https://www.sec.gov/Archives/edgar/data/352541/000035254126000043/lnt-20260630.htm (ok=True, contains_value=True)
  - Status Detail: https://www.alliantenergy.com/our-energy/natural-gas/riverhawk (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Alliant's quarterly report for June 2026 gives the filing and decision timing. The Alliant project page gives the 2031 target. The project is moving through approval, so Latest Activity is left alone. Status stays announced until the commission decides. No turbine model found.

### G100001071244 / Hickory Grove Generating Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Add the entry below at the top of the Status Detail box of unit 1 (G100001071244), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

The Scott County Board of Supervisors rejected the zoning change on February 12, 2026. The Central Iowa Power Cooperative then asked the Iowa Utilities Commission for a certificate instead. The commission held its public information meeting in Davenport on April 6, 2026. The cooperative still targets late 2029.

https://www.wvik.org/wvik-top-stories/2026-02-12/controversial-new-power-plant-rejected-for-rural-scott-county
https://www.wqad.com/article/news/community/controversial-natural-gas-power-plant-proposal-resurfaces-amid-public-pushback/526-4ab92ec6-a62e-46d9-b672-402e2089d3cb
https://www.ourquadcities.com/news/local-news/cipco-begins-alternative-route-to-bring-natural-gas-power-plant-to-scott-county/amp/
https://www.wvik.org/wvik-top-stories/2026-04-07/scott-county-residents-pack-iowa-utilities-commission-meeting-on-cipco-plant
https://www.cipco.net/hickory-grove-generating-station
- `Status Detail`: `AM 05/2026: In February, the Central Iowa Power Cooperative (CIPCO) proposal was rejected by the Scott County Board of Supervisors, but the utility company is now pursuing approval through the Iowa Utilities Commission. https://www.wqad.com/article/news/community/controversial-natural-gas-power-plant-proposal-resurfaces-amid-public-pushback/526-4ab92ec6-a62e-46d9-b672-402e2089d3cb` -> `The Scott County Board of Supervisors rejected the zoning change on February 12, 2026. The Central Iowa Power Cooperative then asked the Iowa Utilities Commission for a certificate instead. The commission held its public information meeting in Davenport on April 6, 2026. The cooperative still targets late 2029.

https://www.wvik.org/wvik-top-stories/2026-02-12/controversial-new-power-plant-rejected-for-rural-scott-county
https://www.wqad.com/article/news/community/controversial-natural-gas-power-plant-proposal-resurfaces-amid-public-pushback/526-4ab92ec6-a62e-46d9-b672-402e2089d3cb
https://www.ourquadcities.com/news/local-news/cipco-begins-alternative-route-to-bring-natural-gas-power-plant-to-scott-county/amp/
https://www.wvik.org/wvik-top-stories/2026-04-07/scott-county-residents-pack-iowa-utilities-commission-meeting-on-cipco-plant
https://www.cipco.net/hickory-grove-generating-station

AM 05/2026: In February, the Central Iowa Power Cooperative (CIPCO) proposal was rejected by the Scott County Board of Supervisors, but the utility company is now pursuing approval through the Iowa Utilities Commission. https://www.wqad.com/article/news/community/controversial-natural-gas-power-plant-proposal-resurfaces-amid-public-pushback/526-4ab92ec6-a62e-46d9-b672-402e2089d3cb`
  - Status Detail: https://www.wvik.org/wvik-top-stories/2026-02-12/controversial-new-power-plant-rejected-for-rural-scott-county (ok=True, contains_value=True)
  - Status Detail: https://www.wqad.com/article/news/community/controversial-natural-gas-power-plant-proposal-resurfaces-amid-public-pushback/526-4ab92ec6-a62e-46d9-b672-402e2089d3cb (ok=True, contains_value=True)
  - Status Detail: https://www.ourquadcities.com/news/local-news/cipco-begins-alternative-route-to-bring-natural-gas-power-plant-to-scott-county/amp/ (ok=True, contains_value=True)
  - Status Detail: https://www.wvik.org/wvik-top-stories/2026-04-07/scott-county-residents-pack-iowa-utilities-commission-meeting-on-cipco-plant (ok=True, contains_value=True)
  - Status Detail: https://www.cipco.net/hickory-grove-generating-station (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: Several news reports and the cooperative's page give these facts. The commission has not ruled. The county board rejected it, not the state. The cooperative did not drop the project or move the site, so the status stays announced. The Iowa Utilities Commission case has not been decided. Latest Activity is left alone because the project is moving.

### G100001071244 / Hickory Grove Generating Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 18 (Unknown start year rechecked)*
**Action:** Set Start year of unit 1 (G100001071244) to 2029. The box is empty now. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `` -> `2029`
  - Start Year Data Source: https://www.cipco.net/hickory-grove-generating-station (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The cooperative's project page says the generating station will be online in late 2029.

### G100001092276 / MidAmerican 2024 IRP power station 7 / 1 IRP
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Set Latest Activity of unit 1 IRP (G100001092276) to Year: 2024, Month: 11, Day: 1. The box is empty now. Add the link below to the Latest Activity Data Source box. Keep the links already there.
- `Latest Activity`: `` -> `Year: 2024, Month: 11, Day: 1`
  - Latest Activity Data Source: https://www.midamericanenergy.com/media/pdf/mec_resource_evaluation_study_11-1.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The newest report found for this placeholder is the Resource Evaluation Study filed November 1, 2024. That is more than a year old. No later document names a 2044 addition. The plan's preferred portfolio supports the 699 MW and 2044 values. The plant has no site yet, so City, turbine model and operator cannot be filled.

### G100001094049 / Morgan Valley Energy Center / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Start year of unit 1 (G100001094049) as 2030. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2030` -> `2030`
  - Start Year Data Source: https://corridorbusiness.com/?p=132984 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Alliant's project page says the plant is expected to be operational in 2030 pending regulatory approval. A Corridor Business Journal article about the commission application says service would start in the second quarter of 2030. Status stays pre-construction. Alliant has asked the Iowa Utilities Commission for a decision by December 2026 and filed a rezoning request with Linn County in July 2026. The project is moving, so Latest Activity is left alone.

### G100001094049 / Morgan Valley Energy Center / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Capacity (MW) of unit 1 (G100001094049) as 240.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `240.0` -> `240.0`
  - Capacity Data Source: https://corridorbusiness.com/?p=132984 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Corridor Business Journal article on the commission application says three simple-cycle turbines rated at 240 MW each. This matches GEM.

### G100001096149 / Morgan Valley Energy Center / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Start year of unit 2 (G100001096149) as 2030. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2030` -> `2030`
  - Start Year Data Source: https://corridorbusiness.com/?p=132984 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Alliant's project page says the plant is expected to be operational in 2030 pending regulatory approval. A Corridor Business Journal article about the commission application says service would start in the second quarter of 2030. Status stays pre-construction. Alliant has asked the Iowa Utilities Commission for a decision by December 2026 and filed a rezoning request with Linn County in July 2026. The project is moving, so Latest Activity is left alone.

### G100001096149 / Morgan Valley Energy Center / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Capacity (MW) of unit 2 (G100001096149) as 240.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `240.0` -> `240.0`
  - Capacity Data Source: https://corridorbusiness.com/?p=132984 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Corridor Business Journal article on the commission application says three simple-cycle turbines rated at 240 MW each. This matches GEM.

### G100001096149 / Morgan Valley Energy Center / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit 2 (G100001096149) to Siemens Energy: SGT6-5000F. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `Siemens Energy: SGT6-5000F`
  - Turbine/Engine Equipment Data Source: https://www.siemens-energy.com/global/en/home/stories/gas-turbine-iowa-power-demand.html (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Siemens Energy story from June 2026 says its SGT6-5000F turbines will power the proposed Morgan Valley Energy Center. All three units are the same 240 MW simple-cycle turbine. Units 1 and 3 already show this model and unit 2 is blank, so only unit 2 needs it.

### G100001096150 / Morgan Valley Energy Center / 3
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Start year of unit 3 (G100001096150) as 2030. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2030` -> `2030`
  - Start Year Data Source: https://corridorbusiness.com/?p=132984 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Alliant's project page says the plant is expected to be operational in 2030 pending regulatory approval. A Corridor Business Journal article about the commission application says service would start in the second quarter of 2030. Status stays pre-construction. Alliant has asked the Iowa Utilities Commission for a decision by December 2026 and filed a rezoning request with Linn County in July 2026. The project is moving, so Latest Activity is left alone.

### G100001096150 / Morgan Valley Energy Center / 3
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Capacity (MW) of unit 3 (G100001096150) as 240.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `240.0` -> `240.0`
  - Capacity Data Source: https://corridorbusiness.com/?p=132984 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Corridor Business Journal article on the commission application says three simple-cycle turbines rated at 240 MW each. This matches GEM.

### G100001054496 / Orient Energy Center power station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 50 (Other last-minute status changes checked)*
**Action:** Set Status of unit 1 (G100001054496) to construction. It now says pre-construction. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `pre-construction` -> `construction`
  - Status Data Source: https://adaircounty.iowa.gov/files/meetings/2026-03-18_minutes_1828.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Adair County supervisors minutes of March 18, 2026 say a MidAmerican representative reported that construction of the Orient Energy Center will begin soon, with crews onsite the next week and paving in April. That points to construction starting in spring 2026. Only one source says so, and I found no later report confirming it. Construction appears to have started in spring 2026 per county minutes. No turbine model was found. The project is moving, so Latest Activity is left alone.

### G100001054496 / Orient Energy Center power station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Add the entry below at the top of the Status Detail box of unit 1 (G100001054496), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

March 2026. MidAmerican told Adair County supervisors that site construction would begin the following week, with paving in April.

https://adaircounty.iowa.gov/files/meetings/2026-03-18_minutes_1828.pdf
- `Status Detail`: `DON Jul'26: Construction likely to be ongoing but could not find source - see March 18 stating will begin soon - by next update (Q4 2026 I ould look hard for evidence constrution has begung - moved this from announved to pre-construction` -> `March 2026. MidAmerican told Adair County supervisors that site construction would begin the following week, with paving in April.

https://adaircounty.iowa.gov/files/meetings/2026-03-18_minutes_1828.pdf

DON Jul'26: Construction likely to be ongoing but could not find source - see March 18 stating will begin soon - by next update (Q4 2026 I ould look hard for evidence constrution has begung - moved this from announved to pre-construction`
  - Status Detail: https://adaircounty.iowa.gov/files/meetings/2026-03-18_minutes_1828.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Adair County supervisors minutes of March 18, 2026 say crews would be onsite the next week and paving would start in early to mid April 2026. Text to add: March 2026. MidAmerican told Adair County supervisors that site construction would begin the next week.

### G100001054496 / Orient Energy Center power station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Start year of unit 1 (G100001054496) as 2028. It is still correct. Add the 2 links below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2028` -> `2028`
  - Start Year Data Source: https://www.midamericanenergy.com/newsroom/2025-generation-projects (ok=True, contains_value=True)
  - Start Year Data Source: https://www.kmaland.com/news/midamerican-energy-announces-energy-production-projects-to-meet-growing-demand/article_cc7120aa-f2d1-11ef-a941-b3dede76d9d9.html (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: MidAmerican's release says the plant would generate power beginning in 2028. This matches GEM.

### G100001055236 / Orient Energy Center power station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 50 (Other last-minute status changes checked)*
**Action:** Set Status of unit 2 (G100001055236) to construction. It now says pre-construction. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `pre-construction` -> `construction`
  - Status Data Source: https://adaircounty.iowa.gov/files/meetings/2026-03-18_minutes_1828.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Adair County supervisors minutes of March 18, 2026 say a MidAmerican representative reported that construction of the Orient Energy Center will begin soon, with crews onsite the next week and paving in April. That points to construction starting in spring 2026. Only one source says so, and I found no later report confirming it. Construction appears to have started in spring 2026 per county minutes. No turbine model was found. The project is moving, so Latest Activity is left alone.

### G100001055236 / Orient Energy Center power station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Set Status Detail of unit 2 (G100001055236) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

March 2026. MidAmerican told Adair County supervisors that site construction would begin the following week, with paving in April.

https://adaircounty.iowa.gov/files/meetings/2026-03-18_minutes_1828.pdf
- `Status Detail`: `` -> `March 2026. MidAmerican told Adair County supervisors that site construction would begin the following week, with paving in April.

https://adaircounty.iowa.gov/files/meetings/2026-03-18_minutes_1828.pdf`
  - Status Detail: https://adaircounty.iowa.gov/files/meetings/2026-03-18_minutes_1828.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Adair County supervisors minutes of March 18, 2026 say crews would be onsite the next week and paving would start in early to mid April 2026. Text to add: March 2026. MidAmerican told Adair County supervisors that site construction would begin the next week.

### G100001055236 / Orient Energy Center power station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Start year of unit 2 (G100001055236) as 2028. It is still correct. Add the 2 links below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2028` -> `2028`
  - Start Year Data Source: https://www.midamericanenergy.com/newsroom/2025-generation-projects (ok=True, contains_value=True)
  - Start Year Data Source: https://www.kmaland.com/news/midamerican-energy-announces-energy-production-projects-to-meet-growing-demand/article_cc7120aa-f2d1-11ef-a941-b3dede76d9d9.html (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: MidAmerican's release says the plant would generate power beginning in 2028. This matches GEM.

### G100001072768 / Alliant Fairfax power station / Unit 1
*question about existing data; checklist rows 20 (No start year on cancelled or shelved projects), 24 (Presumed cancelled or shelved units have a Latest Activity date and source), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 50 (Other last-minute status changes checked)*
- about: Status
- recommendation: Keep cancelled. The Fairfax site was dropped, and Morgan Valley is a different site about 2.5 miles away with a different size.
  - links: https://corridorbusiness.com/alliant-energy-proposes-new-site-near-fairfax-for-natural-gas-power-plant/ (ok=None, contains_value=None)
- notes: The Energy Information Project's Oil and Gas Watch lists Morgan Valley under the same facility record that GEM uses for Fairfax, which is why it shows proposed. The Corridor Business Journal article of March 5, 2026 says the Fairfax proposal was dropped and Morgan Valley is a new proposal at another site. The same reporting gives Morgan Valley as three combustion turbines of about 720 MW, against two 425 MW units at Fairfax. The month or year of the drop is not stated in that article. The existing source dated October 2025 says deprioritized, and that page now returns a 404 error.

### G100001054408 / Ames Municipal Power Plant / Unit 7, timepoint 2
*watch item at an existing plant*
- what to watch: The city plans to retire Units 7 and 8 when the new Ames Energy Center opens, but no retirement year has been published.
- check again by: 2027-04
  - links: https://amesinfocus.podbean.com/e/ames-in-focus-powering-forward-with-curtis-spence (ok=None, contains_value=None)
- notes: A city podcast from November 2025 describes the planned retirement. Local news says the replacement engines arrive in October 2029.

### G100001071243 / Bobcat Energy Center / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
- about: Capacity (MW)
- recommendation: A KCRG story from August 11, 2026 calls the plant 650 MW. That figure is the existing Marshalltown station. Alliant's own releases say 720 MW. Keep 720.
- notes: The KCRG figure looks like an error.

### G100001071244 / Hickory Grove Generating Station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 50 (Other last-minute status changes checked)*
- about: Status
- recommendation: Keep announced. The Scott County Board of Supervisors voted against the zoning change on February 12, 2026. The Central Iowa Power Cooperative did not appeal or move the site. It went to the Iowa Utilities Commission for a certificate for the same plan and held the commission's public information meeting on April 6, 2026. No reporter has called the project cancelled or shelved.
  - links: https://www.wvik.org/wvik-top-stories/2026-02-12/controversial-new-power-plant-rejected-for-rural-scott-county (ok=None, contains_value=None)
  - links: https://www.ourquadcities.com/news/local-news/cipco-begins-alternative-route-to-bring-natural-gas-power-plant-to-scott-county/amp/ (ok=None, contains_value=None)
- notes: A rejection by the county is not a cancellation.

### G100001092270 / Interstate Power and Light 2024 IRP power station 1 / 1 IRP
*watch item at an existing plant; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- what to watch: The combined cycle unit may be the future conversion of Morgan Valley, but no filing says so yet.
- check again by: 2027-03
- notes: The commission decision on Morgan Valley is expected in the first quarter of 2027.

### Marshalltown power station
*watch item at an existing plant*
- what to watch: Alliant is building the 720 MW Bobcat Energy Center next to this site, so the old turbines could be affected later.
- check again by: 2027-06
  - links: https://www.alliantenergy.com/news/news-center/2025/12/121625-bobcat-energy-center-approved (ok=None, contains_value=None)
- notes: The Iowa Utilities Commission approved Bobcat in December 2025. Alliant says service is planned for 2029. No retirement of the 1978 turbines has been announced.

### G100001074296 / MidAmerican 2024 IRP power station 1 / 1 IRP
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
- about: Capacity (MW)
- recommendation: The study rounds each turbine to 233 MW. GEM shows 232.5 MW, which may come from a different filing. Keep 232.5 MW unless the reviewer prefers the study's figure.
  - links: https://www.midamericanenergy.com/media/pdf/mec_resource_evaluation_study_11-1.pdf (ok=None, contains_value=None)
- notes: The preferred portfolio table in the 2024 study says 233 MW for the 2031 turbine. I did not find a source that says 232.5 MW.

### G100001074296 / MidAmerican 2024 IRP power station 1 / 1 IRP
*watch item at an existing plant; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- what to watch: The turbine is an unsited planning placeholder with no filing yet.
- check again by: 2027-06
- notes: Watch Iowa Utilities Commission generating certificate filings for a named project of this size.

### G100001092271 / MidAmerican 2024 IRP power station 2 / 1 IRP
*watch item at an existing plant; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- what to watch: The turbine is an unsited planning placeholder with no filing yet.
- check again by: 2027-06
- notes: Watch Iowa Utilities Commission generating certificate filings for a named project of this size.

### G100001092272 / MidAmerican 2024 IRP power station 3 / 1 IRP
*watch item at an existing plant; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- what to watch: The turbine is an unsited planning placeholder with no filing yet.
- check again by: 2027-06
- notes: Watch Iowa Utilities Commission generating certificate filings for a named project of this size.

### G100001092273 / MidAmerican 2024 IRP power station 4 / 1 IRP
*watch item at an existing plant; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- what to watch: The turbine is an unsited planning placeholder with no filing yet.
- check again by: 2027-06
- notes: Watch Iowa Utilities Commission generating certificate filings for a named project of this size.

### G100001092274 / MidAmerican 2024 IRP power station 5 / 1 IRP
*watch item at an existing plant; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- what to watch: The turbine is an unsited planning placeholder with no filing yet.
- check again by: 2027-06
- notes: Watch Iowa Utilities Commission generating certificate filings for a named project of this size.

### G100001092275 / MidAmerican 2024 IRP power station 6 / 1 IRP
*watch item at an existing plant; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- what to watch: The turbine is an unsited planning placeholder with no filing yet.
- check again by: 2027-06
- notes: Watch Iowa Utilities Commission generating certificate filings for a named project of this size.

### G100001094049 / Morgan Valley Energy Center / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 50 (Other last-minute status changes checked)*
- about: Status
- recommendation: Keep pre-construction. A commission decision on the certificate is requested by December 2026 and the Linn County rezoning is pending, so construction approval is not yet given.
  - links: https://corridorbusiness.com/?p=132984 (ok=None, contains_value=None)
- notes: Corridor Business Journal reports opposition from Fairfax and Benton County residents who petitioned to intervene.

### G100001094049 / Morgan Valley Energy Center / 1
*watch item at an existing plant; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- what to watch: The Iowa Utilities Commission decision and the Linn County rezoning vote are both pending.
- check again by: 2027-02
  - links: https://corridorbusiness.com/?p=132984 (ok=None, contains_value=None)
- notes: Alliant's request is a decision by December 2026. Its June 2026 report expected the first quarter of 2027.

### G100001054496 / Orient Energy Center power station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
- about: Capacity (MW)
- recommendation: The MidAmerican fact sheet says the project has three turbines, 700 MW and a unit 3 in service in spring 2029. The company's news release, a business news article and local press say two turbines and 465 MW. GEM has two units of 232.5 MW. Keep two units unless a commission filing shows a third.
  - links: https://www.midamericanenergy.com/media/pdf/orient_energy_center_fact_sheet.pdf (ok=None, contains_value=None)
  - links: https://www.midamericanenergy.com/newsroom/2025-generation-projects (ok=None, contains_value=None)
- notes: The fact sheet appears to carry text from an earlier larger design. Local press also cited up to 520 MW.

### G100001054496 / Orient Energy Center power station / 1
*watch item at an existing plant; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- what to watch: A commission certificate decision was not found, and a September 2026 meeting report on foundation work could not be opened.
- check again by: 2026-12
- notes: Check Iowa Utilities Commission filings for the certificate and for turbine delivery.

### G100000403018 / Prairie Creek Generating Station / Unit 4- timepoint 2
*watch item at an existing plant*
- what to watch: Alliant plans a new 94 MW gas engine plant, Cedar River Generating Station, on this site, and units 1 and 3 ended coal use at the end of 2025.
- check again by: 2027-06
  - links: https://corridorbusiness.com/alliant-plans-for-natural-gas-fired-power-plant-at-prairie-creek-moving-forward/ (ok=None, contains_value=None)
- notes: Units 1 and 3 are separate rows in GEM and still show as operating in the EIA table.

## Checklist group 4. Conversions

Coal-to-gas and other conversions: unit naming, fuel and technology, replacement links.

### G100001054408 / Ames Municipal Power Plant / Unit 7, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Set Start year of unit Unit 7, timepoint 2 (G100001054408) to 2016. It now says 1968. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `1968` -> `2016`
  - Start Year Data Source: https://www.sargentlundy.com/projects/steam-electric-plant-coal-to-gas-boiler-conversion/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Sargent and Lundy project page says the City of Ames converted its Unit 7 and Unit 8 boilers from coal to natural gas. The project started in May 2014 and was completed in July 2016. So the unit first ran on gas in 2016, not 1968. The 1968 year is when the coal unit began operating.

### G100001054408 / Ames Municipal Power Plant / Unit 7, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 7, timepoint 2 (G100001054408) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.sargentlundy.com/projects/steam-electric-plant-coal-to-gas-boiler-conversion/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Sargent and Lundy project page says the City of Ames converted its Unit 7 and Unit 8 boilers from coal to natural gas. The project started in May 2014 and was completed in July 2016. This matches the value GEM already shows.

### G100001017969 / Ames Municipal Power Plant / Unit 8, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 8, timepoint 2 (G100001017969) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.sargentlundy.com/projects/steam-electric-plant-coal-to-gas-boiler-conversion/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Sargent and Lundy project page says the City of Ames converted its Unit 7 and Unit 8 boilers from coal to natural gas. The project started in May 2014 and was completed in July 2016. This matches the value GEM already shows.

### G100001017907 / Burlington Generating Station / Unit 1, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 1, timepoint 2 (G100001017907) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.epa.gov/system/files/documents/2023-10/burlington-petition-november-2021-final-response-march-2022_0.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A United States Environmental Protection Agency letter from March 2022 says Burlington Unit 1 has historically been a coal boiler of 212 MW and is being converted to burn only natural gas from January 1, 2022.

### G100001054413 / Earl F. Wisdom Generating Station / Unit 1, timepoint 2
*change to an existing unit; checklist rows 12 (Conversions carry "timepoint" in the unit name), 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Set Conversion/replacement? of unit Unit 1, timepoint 2 (G100001054413) to conversion. The box is empty now. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `` -> `conversion`
  - Conversion/replacement Data Source: https://www.cbpower.coop/filesimages/474346_cbp_2019_annual_report_lowres_final(2).pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Corn Belt Power Cooperative 2019 annual report says the coal pile was no longer needed because Wisdom Unit 1 was converted from coal to natural gas. So this unit is a conversion. The report gives no year for the conversion.

### G100000403018 / Prairie Creek Generating Station / Unit 4- timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 4- timepoint 2 (G100000403018) as conversion. It is still correct. Add the 2 links below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.thegazette.com/business/alliant-shifting-largest-cedar-rapids-coal-unit-to-burn-natural-gas/ (ok=True, contains_value=True)
  - Conversion/replacement Data Source: https://www.power-eng.com/coal/alliant-finishes-up-coal-to-gas-conversion/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: A Gazette article from November 2017 says crews were converting Prairie Creek unit 4 from coal to natural gas, with the work to finish that week. An Associated Press story from November 2, 2017 says the same. So this is a conversion and the unit began burning gas in 2017.

### G100001017855 / Riverside (IA) power station / Unit 5, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 5, timepoint 2 (G100001017855) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.sec.gov/Archives/edgar/data/0000928576/000092857615000020/eei2015.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The same filing says Riverside Unit 5 of 124 MW ceased burning coal in 2015 and operates solely on natural gas. That is a conversion.

### G100001054408 / Ames Municipal Power Plant / Unit 7, timepoint 2
*question about existing data; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
- about: Fuel
- recommendation: The City of Ames page says Unit 7 burns refuse derived fuel from municipal solid waste along with natural gas. GEM lists only natural gas. Consider adding a bioenergy fuel for waste. The page also says the city has started to phase this fuel out.
  - links: https://www.cityofames.org/My-Government/Departments/Electric-Department (ok=None, contains_value=None)
- notes: A fuel question only. Not changed here.

### G100001094030 / Burlington Generating Station / Unit 2
*question about existing data; checklist rows 12 (Conversions carry "timepoint" in the unit name), 13 (Coal-to-gas conversions have gas fuel and technology)*
- about: conversion-link
- recommendation: GEM does not have the plant's four combustion turbines, GT1 to GT4 at 19.7 MW each. The EIA-860M table for August 2026 lists them as operating with a planned retirement in 2030. They are listed as new units for this plant. Once they exist, link them to Unit 2 as the units it replaces.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://www.alliantenergy.com/news/news-center/2026/02/021626-regulators-ok-updates-at-burlington (ok=None, contains_value=None)
- notes: Alliant says the engines replace combustion turbines that are more than 30 years old.

### G100001054413 / Earl F. Wisdom Generating Station / Unit 1, timepoint 2
*question about existing data; checklist rows 12 (Conversions carry "timepoint" in the unit name), 13 (Coal-to-gas conversions have gas fuel and technology)*
- about: conversion-link
- recommendation: The earlier coal unit is Unit 1, timepoint 1 at Wisdom (GEM unit G100000102545, coal, 1960, retired). Its conversion link fields are blank. The conversion year was not found in a citable document, so the start year was left as it is.
  - links: https://www.cbpower.coop/filesimages/474346_cbp_2019_annual_report_lowres_final(2).pdf (ok=None, contains_value=None)
- notes: The 2019 annual report confirms the conversion but gives no year.

### Streeter Station
*question about existing data; checklist rows 12 (Conversions carry "timepoint" in the unit name), 13 (Coal-to-gas conversions have gas fuel and technology)*
- about: conversion-link
- recommendation: Ask the reviewer to check whether Streeter Station was converted from coal to gas. If it was, add gas timepoint 2 units (16.5 MW and 35 MW) with Cedar Falls Utilities as owner.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: GEM has Streeter Station only in the coal tracker, as unit 7 (35 MW, 1973), retired. The EIA-860M table for August 2026 lists Streeter Station, plant 1131, owned by Cedar Falls Utilities in Black Hawk County. Both of its units are listed as natural gas steam turbines and as operating. Unit 6 is 16.5 MW from 1963. Unit 7 is 35 MW from 1973. That is 51.5 MW of gas capacity in total, which is over the 50 MW threshold. The EIA table does not say when the plants switched from coal to gas, and I did not search for the conversion date. The owner name already exists in GEM as Cedar Falls Utilities.

## Checklist group 6. Owners and entities

Owner, operator and parent changes, and new owners or operators to create.

### G100000414312 / Ames GT power station / GT2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit GT2 (G100000414312) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists plant 6463, generator GT2, as operating, 57.4 MW nameplate, operating year 2005, with no planned retirement date. No retirement, mothballing or owner change was found. A web search found no announcement about these turbines.

### G100001054408 / Ames Municipal Power Plant / Unit 7, timepoint 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 7, timepoint 2 (G100001054408) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.cityofames.org/My-Government/Departments/Electric-Department (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists Plant 1122, generator 7, as operating with 37.5 MW. The City of Ames electric department page says Unit 7 is in service. Still operating. Gas start year should be 2016 per the conversion project. No retirement year published yet.

### G100001017969 / Ames Municipal Power Plant / Unit 8, timepoint 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 8, timepoint 2 (G100001017969) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.cityofames.org/My-Government/Departments/Electric-Department (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists Plant 1122, generator 8, as operating with 71.3 MW. The City of Ames electric department page says Unit 8 burns only natural gas and is in service. Still operating. The 1982 year in the EIA table is the original coal unit, so the 2016 start year stays.

### G100000402232 / Earl F. Wisdom Generating Station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000402232) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists Plant 1217, generator 2, as operating with 81.6 MW. It shows no planned retirement. The only planned change is an uprate of 0 MW in December 2027. Still operating. No retirement or sale found.

### G100001054413 / Earl F. Wisdom Generating Station / Unit 1, timepoint 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 1, timepoint 2 (G100001054413) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists Plant 1217, generator 1, as operating with 37.5 MW and an operating year of 1960. It shows no planned retirement. Still operating. The conversion is confirmed but the year and the earlier unit's ID were not found.

### G100001054413 / Earl F. Wisdom Generating Station / Unit 1, timepoint 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of unit Unit 1, timepoint 2 (G100001054413) as Corn Belt Power Cooperative [100%]. It is still correct. Add the link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Corn Belt Power Cooperative [100%]` -> `Corn Belt Power Cooperative [100%]`
  - Owners Data Source: https://www.cbpower.coop/power-supply/corn-belt-power-generation (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Corn Belt Power Cooperative generation page lists Wisdom Unit 1, 38 MW, under generating sources owned by Corn Belt Power. This matches GEM's value.

### G100000403156 / Electrifarm power station / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100000403156) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists Plant 6063, generator 1, as operating with 71.2 MW. It shows no planned retirement. A news search found no retirement or sale announcement. Still operating. No retirement, mothballing or sale found.

### G100000403157 / Electrifarm power station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000403157) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists Plant 6063, generator 2, as operating with 89.0 MW. It shows no planned retirement. A news search found no retirement or sale announcement. Still operating. No retirement, mothballing or sale found.

### G100000403158 / Electrifarm power station / 3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 3 (G100000403158) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists Plant 6063, generator 3, as operating with 103.9 MW. It shows no planned retirement. A news search found no retirement or sale announcement. Still operating. No retirement, mothballing or sale found.

### G100000403754 / Exira power station / U1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit U1 (G100000403754) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA monthly generator table for August 2026 lists plant 56013, generator U1, as operating with no planned retirement. The owner is the Western Minnesota Municipal Power Agency. Still operating. No retirement, mothballing or owner change was found.

### G100000403755 / Exira power station / U2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit U2 (G100000403755) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA monthly generator table for August 2026 lists plant 56013, generator U2, as operating with no planned retirement. The owner is the Western Minnesota Municipal Power Agency. Still operating. No retirement, mothballing or owner change was found.

### G100000403756 / Exira power station / U3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit U3 (G100000403756) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA monthly generator table for August 2026 lists plant 56013, generator U3, as operating with no planned retirement. The owner is the Western Minnesota Municipal Power Agency. Still operating. No retirement, mothballing or owner change was found.

### G100000402188 / Greater Des Moines power station / CC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC1 (G100000402188) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA monthly generator table for August 2026 lists plant 7985 units GT1, GT2 and ST1 as operating with no planned retirement. Owner is MidAmerican Energy Co. Still operating. No retirement, mothballing or owner change was found.

### G100001054470 / Lime Creek power station / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100001054470) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA monthly generator table for August 2026 lists plant 7155 generators 1 and 2 as operating, 45.1 MW each, with no planned retirement. Owner is Interstate Power and Light Co. Still operating. No retirement, mothballing or owner change was found.

### G100000402061 / Marshalltown generating station / MGS1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit MGS1 (G100000402061) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA monthly generator table for August 2026 lists plant 58236 units CTG1, CTG2 and STG1 as operating with no planned retirement. Owner is Interstate Power and Light Co. Still operating. No retirement, mothballing or owner change was found.

### G100000403015 / Marshalltown power station / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100000403015) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.sec.gov/Archives/edgar/data/352541/000035254126000007/lnt-20251231.htm (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for August 2026 lists this unit as operating. Alliant Energy's annual report for 2025, filed in 2026, lists the Marshalltown combustion turbines, units 1 to 3, in service in 1978 among Interstate Power and Light's gas plants. I found no retirement, mothballing or sale notice. Still operating. No retirement, planned retirement, mothballing or owner change was found.

### G100000403016 / Marshalltown power station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000403016) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.sec.gov/Archives/edgar/data/352541/000035254126000007/lnt-20251231.htm (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for August 2026 lists this unit as operating. Alliant Energy's annual report for 2025, filed in 2026, lists the Marshalltown combustion turbines, units 1 to 3, in service in 1978 among Interstate Power and Light's gas plants. I found no retirement, mothballing or sale notice. Still operating. No retirement, planned retirement, mothballing or owner change was found.

### G100000403017 / Marshalltown power station / 3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 3 (G100000403017) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.sec.gov/Archives/edgar/data/352541/000035254126000007/lnt-20251231.htm (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for August 2026 lists this unit as operating. Alliant Energy's annual report for 2025, filed in 2026, lists the Marshalltown combustion turbines, units 1 to 3, in service in 1978 among Interstate Power and Light's gas plants. I found no retirement, mothballing or sale notice. Still operating. No retirement, planned retirement, mothballing or owner change was found.

### G100001054416 / Pleasant Hill power station / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100001054416) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.sec.gov/Archives/edgar/data/1081316/000108131626000003/bhe-20251231.htm (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for August 2026 lists this generator as operating. MidAmerican Energy's table of generating plants in the Berkshire Hathaway Energy annual report for 2025 lists Pleasant Hill, 1990 to 1994, as a gas or oil plant in service. I found no retirement, mothballing or sale notice. Still operating. No retirement, planned retirement, mothballing or owner change was found.

### G100001054415 / Pleasant Hill power station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100001054415) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.sec.gov/Archives/edgar/data/1081316/000108131626000003/bhe-20251231.htm (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for August 2026 lists this generator as operating. MidAmerican Energy's table of generating plants in the Berkshire Hathaway Energy annual report for 2025 lists Pleasant Hill, 1990 to 1994, as a gas or oil plant in service. I found no retirement, mothballing or sale notice. Still operating. No retirement, planned retirement, mothballing or owner change was found.

### G100000403159 / Pleasant Hill power station / 3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 3 (G100000403159) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.sec.gov/Archives/edgar/data/1081316/000108131626000003/bhe-20251231.htm (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for August 2026 lists this generator as operating. MidAmerican Energy's table of generating plants in the Berkshire Hathaway Energy annual report for 2025 lists Pleasant Hill, 1990 to 1994, as a gas or oil plant in service. I found no retirement, mothballing or sale notice. Still operating. No retirement, planned retirement, mothballing or owner change was found.

### G100000403018 / Prairie Creek Generating Station / Unit 4- timepoint 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 4- timepoint 2 (G100000403018) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.sec.gov/Archives/edgar/data/352541/000035254126000007/lnt-20251231.htm (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for August 2026 lists unit 4 as operating on natural gas. Alliant Energy's annual report for 2025 lists Prairie Creek unit 4 among Interstate Power and Light's gas plants. It says units 3 and 4 face a federal rule, but no retirement of unit 4 is announced. Still operating on natural gas. The 1967 date in the EIA table is the original coal start, not the conversion.

### G100000403018 / Prairie Creek Generating Station / Unit 4- timepoint 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of unit Unit 4- timepoint 2 (G100000403018) as Interstate Power and Light Co [100%]. It is still correct. Add the 2 links below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Interstate Power and Light Co [100%]` -> `Interstate Power and Light Co [100%]`
  - Owners Data Source: https://www.sec.gov/Archives/edgar/data/352541/000035254126000007/lnt-20251231.htm (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Alliant Energy's annual report for 2025 lists Prairie Creek Generating Station unit 4 in a table of Interstate Power and Light's own generating plants. The EIA table names the same company as the plant's utility. The brief's Alliant Energy Corp is the parent, so it is not the owner.

### G100001017855 / Riverside (IA) power station / Unit 5, timepoint 2
*change to an existing unit*
**Action:** Leave Owner(s) of unit Unit 5, timepoint 2 (G100001017855) as MidAmerican Energy Co [100%]. It is still correct. Add the link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `MidAmerican Energy Co [100%]` -> `MidAmerican Energy Co [100%]`
  - Owners Data Source: https://www.sec.gov/Archives/edgar/data/0000928576/000092857615000020/eei2015.htm (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: A MidAmerican Energy presentation filed with the Securities and Exchange Commission in 2015 lists Riverside Unit 5 among MidAmerican Energy's own coal-fueled generation. So it supports MidAmerican Energy as owner. It does not give a percentage share. I found no document that states the coordinates, so they have no source yet. I found nothing that mentions carbon capture at this unit.

### G100000414185 / Summit Lake power station / IC
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit IC (G100000414185) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists generators R1, R2 and R3 at Summit Lake, plant 1206, as operating natural gas engines of 18.8 MW each, in service since April 2021. The sheet shows no retirement, mothballing or planned retirement for them, and the owner is still Central Iowa Power Cooperative. Still operating. No retirement or sale found. The city was filled from a news article on the cooperative's rebuild.

### G100000403161 / Sycamore (IA) power station / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100000403161) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists Sycamore (Iowa), plant 8029, generator 1 as operating, 78.8 MW nameplate, owned by MidAmerican Energy Co, in service 1974. The sheet shows no retirement, planned retirement or owner change. Still operating. No retirement, mothballing or sale found.

### G100000403162 / Sycamore (IA) power station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000403162) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists Sycamore (Iowa), plant 8029, generator 2 as operating, 78.8 MW nameplate, owned by MidAmerican Energy Co, in service 1974. The sheet shows no retirement, planned retirement or owner change. Still operating. No retirement, mothballing or sale found.

### Alliant Fairfax power station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Interstate Power and Light Co (owner); lookup: Bare lookup of Interstate Power and Light found nothing locally and asked for a database check; not reported as an owner because no source names the owner of the Fairfax project.

### G100001054408 / Ames Municipal Power Plant / Unit 7, timepoint 2
*question about existing data; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
- about: Planned retire
- recommendation: The City of Ames plans to retire Units 7 and 8 when the new Ames Energy Center opens. A city podcast episode from November 2025 describes this. Local news says the new plant, built from reciprocating engines, will open in 2029. I found no firm retirement year from the city, so I did not report one.
  - links: https://amesinfocus.podbean.com/e/ames-in-focus-powering-forward-with-curtis-spence (ok=None, contains_value=None)
- notes: Retirement is planned but no firm year was found. Both units are still operating.

### Bobcat Energy Center
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Interstate Power and Light Co (owner); lookup: Entity 'Interstate Power and Light Co' appears on 28 units (united states). Reuse existing entity ID; do NOT create a new one.

### Burlington Generating Station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Interstate Power and Light Co (owner); lookup: Entity 'Interstate Power and Light Co' appears on 28 units (united states). Reuse existing entity ID; do NOT create a new one.

### Cedar River Generating Station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Interstate Power and Light Co (owner); lookup: Entity 'Interstate Power and Light Co' appears on 28 units (united states). Reuse existing entity ID; do NOT create a new one.

### G100000402232 / Earl F. Wisdom Generating Station / 2
*question about existing data; checklist rows 19 (Missing or unknown owner searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
- about: Owner(s)
- recommendation: The Corn Belt Power Cooperative generation page lists Wisdom Unit 2, 40 MW, as owned by Corn Belt Power. GEM shows Basin Electric Power Cooperative at 50 percent and Corn Belt at 50 percent. The cooperative's own page does not mention Basin. Not changed.
  - links: https://www.cbpower.coop/power-supply/corn-belt-power-generation (ok=None, contains_value=None)
- notes: Ownership of Unit 2 may need a second look.

### Exira power station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Missouri River Energy Services (operator); lookup: Entity exists in the tracker, canonical name missouri river energy services, on 3 units in the United States. Reuse the existing entity.

## Checklist group 7. IDs, IRPs and data centers

United States only: EIA and other IDs, utility resource plans, gas-fired data centers.

### G100001017969 / Ames Municipal Power Plant / Unit 8, timepoint 2
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Leave Start year of unit Unit 8, timepoint 2 (G100001017969) as 2016. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2016` -> `2016`
  - Start Year Data Source: https://www.sargentlundy.com/projects/steam-electric-plant-coal-to-gas-boiler-conversion/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Sargent and Lundy project page says the City of Ames converted its Unit 7 and Unit 8 boilers from coal to natural gas. The project started in May 2014 and was completed in July 2016. The EIA table gives 1982 because that is the year the original coal unit began operating. GEM tracks the converted unit, so 2016 is right and should stay.

### G100001017907 / Burlington Generating Station / Unit 1, timepoint 2
*change to an existing unit; checklist rows 37 (IRP box ticked on every IRP project (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 1, timepoint 2 (G100001017907) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists plant 1104, generator 1, as operating, 212.0 MW, natural gas steam turbine, with no planned retirement date. I found no retirement, mothballing or sale announcement. This confirms the current status. I could not find any document that states whether the unit has carbon capture. I found no sign of it. The start year is unresolved. See the questions.

### G100000402192 / Emery Station power plant / G821
*change to an existing unit; checklist rows 37 (IRP box ticked on every IRP project (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit G821 (G100000402192) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists plant 8031, Emery Station, generators 11, 12 and ST1 as operating, 173.4 MW, 173.4 MW and 256.0 MW, natural gas combined cycle, started in May 2004, with no planned retirement. I found no retirement, mothballing or sale notice. Still operating with no change found.

### G100000403018 / Prairie Creek Generating Station / Unit 4- timepoint 2
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Leave Start year of unit Unit 4- timepoint 2 (G100000403018) as 2017. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2017` -> `2017`
  - Start Year Data Source: https://www.power-eng.com/coal/alliant-finishes-up-coal-to-gas-conversion/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: GEM's 2017 is the year the unit began burning gas. A Gazette article from November 2017 says crews were converting Prairie Creek unit 4 from coal to natural gas, with the work to finish that week. An Associated Press story from November 2, 2017 says the same. So this is a conversion and the unit began burning gas in 2017. The EIA table shows 1967 because that is when the original coal unit started. Under GEM's conversion rule 2017 is correct, so no change is needed.

### G100001017907 / Burlington Generating Station / Unit 1, timepoint 2
*question about existing data; checklist rows 37 (IRP box ticked on every IRP project (US only)), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
- about: Start year
- recommendation: GEM's start year is 2021. The EIA-860M table for August 2026 gives 1968, which is when the original coal unit started. For a conversion, GEM wants the year the unit began burning gas. The Environmental Protection Agency letter from March 2022 says the conversion would be done by January 1, 2022. A 2022 news report in GEM's sources said it was nearly done in May 2022, and EIA still showed coal in October 2022. So 2021 looks too early and 2022 or later looks likelier. I could not find a document that gives the exact date. Please keep 2021 only if you have a source for it.
  - links: https://www.epa.gov/system/files/documents/2023-10/burlington-petition-november-2021-final-response-march-2022_0.pdf (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: 1968 is the right year for the original boiler, not for the gas conversion.

### G100001017907 / Burlington Generating Station / Unit 1, timepoint 2
*question about existing data; checklist rows 37 (IRP box ticked on every IRP project (US only))*
- about: other
- recommendation: The Interstate Power and Light resource evaluation study comments from Synapse (April 2025) mention that the earlier Clean Energy Blueprint concluded Burlington would convert to natural gas. They give no new capacity, date or retirement for the plant. So there is no plan value to report.
  - links: https://www.synapse-energy.com/sites/default/files/IPL%20RES%20EI%20Final%20Comments%20on%20RES%204.7.25-%20Public%2024-008.pdf (ok=None, contains_value=None)
- notes: Background only.

### Interstate Power and Light 2024 IRP power station 1
*question about existing data; checklist rows 37 (IRP box ticked on every IRP project (US only)), 51 (Newly announced projects checked)*
- about: existence
- recommendation: Keep the placeholder for now and ask the reviewer whether the 430 MW combined cycle unit is still planned. If not, the placeholder could be cancelled.
  - links: https://www.synapse-energy.com/sites/default/files/IPL%20RES%20EI%20Final%20Comments%20on%20RES%204.7.25-%20Public%2024-008.pdf (ok=True, contains_value=True)
  - links: https://www.sec.gov/Archives/edgar/data/0000352541/000035254126000043/lnt-20260630.htm (ok=True, contains_value=True)
- notes: This placeholder holds the 430 MW combined cycle unit for 2029 that Interstate Power and Light modeled in its Resource Evaluation Study. I could not read the study itself, because it is filed with the Iowa Utilities Commission in docket RPU-2021-0003 and I did not reach that filing system. Comments filed by Synapse Energy Economics on April 7, 2025 describe the study, which is dated February 13, 2025. They say the main flat load portfolio adds over 1,500 MW of new gas, made up of a 430 MW combined cycle unit and the rest peaking units. They also say the company expected combined cycle units to be available no earlier than 2029. Alliant Energy's quarterly report for June 30, 2026 lists only simple-cycle gas projects: about 720 MW in Linn County (Morgan Valley) and about 1,200 MW near Emery Station (Riverhawk). It does not mention a combined cycle unit at all. Bobcat (720 MW) is already tracked as its own plant. I found no source that says the 430 MW combined cycle unit was dropped or replaced, and none that says it is still planned. So the placeholder cannot be confirmed or removed on the evidence found. A reviewer should check the docket or ask Alliant.

### G100001092270 / Interstate Power and Light 2024 IRP power station 1 / 1 IRP
*question about existing data; checklist rows 37 (IRP box ticked on every IRP project (US only)), 51 (Newly announced projects checked)*
- about: existence
- recommendation: I could not tie the 430 MW combined cycle placeholder to Morgan Valley or Fairfax. Morgan Valley is three simple-cycle turbines of about 240 MW each, 720 MW in total, filed in April 2026. Its application says the site could later be converted to combined cycle, but only if approved in a future filing. Keep the placeholder separate for now. The reviewer should decide whether it still belongs once a combined cycle plan is filed.
  - links: https://www.synapse-energy.com/sites/default/files/IPL%20RES%20EI%20Final%20Comments%20on%20RES%204.7.25-%20Public%2024-008.pdf (ok=None, contains_value=None)
  - links: https://cbs2iowa.com/resources/pdf/2fdc7cdb-e6ce-44c5-a3fe-c2d56823edb0-23fc9a8c72f84f73a302ef34d5f5f7f3MorganValleyEnergyCenterCT_Application1.pdf (ok=None, contains_value=None)
- notes: The intervenors' study comments from April 2025 say the model adds a 430 MW combined cycle, and the Morgan Valley application cites the study filed on February 13, 2025. The application does not drop or rename the combined cycle unit. It only mentions a possible future conversion.

### MidAmerican 2024 IRP power station 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
- about: Capacity (MW)
- recommendation: No change needed. All seven MidAmerican placeholders match the plan. Optionally set this one to 233 MW to match the plan's rounded size.
  - links: https://www.midamericanenergy.com/media/pdf/mec_resource_evaluation_study_11-1.pdf (ok=True, contains_value=True)
- notes: MidAmerican's Resource Evaluation Study of November 1, 2024 has a Preferred Portfolio table of gas combustion turbine additions. It lists 233 MW in 2028, 233 MW in 2029, 233 MW in 2031, 233 MW in 2033, 233 MW in 2035, 699 MW in 2041, 466 MW in 2042, 466 MW in 2043 and 699 MW in 2044, for a total of 3,495 MW. The 2028 and 2029 entries are the Orient Energy Center. The other seven are the placeholders: 233 MW in 2031 (this plant, which GEM holds at 232.5 MW), 233 MW in 2033, 233 MW in 2035, 699 MW in 2041, 466 MW in 2042, 466 MW in 2043 and 699 MW in 2044. Every year and size matches GEM, except that this plant is 232.5 MW in GEM and 233 MW in the plan. The plan models turbines in 233 MW blocks, and Orient's two turbines are each 232.5 MW, so the 0.5 MW gap is rounding. I read the table in the downloaded plan text.

### Orient Energy Center power station
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
- about: Start year
- recommendation: Leave both units at 2028. The plan's 2029 entry for the second turbine is older than the company's own later statements.
  - links: https://www.midamericanenergy.com/media/pdf/mec_resource_evaluation_study_11-1.pdf (ok=True, contains_value=True)
  - links: https://www.midamericanenergy.com/newsroom/2025-generation-projects (ok=True, contains_value=True)
  - links: https://www.misoenergy.org/api/giqueue/getprojects (ok=True, contains_value=True)
- notes: The tab note says MidAmerican plans two 233 MW peaking plants in 2028 and 2029, and GEM has both Orient units in 2028. MidAmerican's Resource Evaluation Study of November 1, 2024 does list one 233 MW turbine in 2028 and another in 2029. Its Action Plan table says the same, with a feasible timeline of 233 MW in each of those two years. A later MidAmerican news release says the Orient Energy Center, two gas-fired combustion turbines at one site in Adair County, will generate 465 MW beginning in 2028. The company gives no 2029 date for the second turbine in that release. A queue entry at the Midcontinent Independent System Operator for 263 MW at the Orient Energy Center substation, with service in November 2028, was withdrawn on December 23, 2025. A second entry for 263 MW at the Orient to Northboro line, with service in September 2027, is still active. I did not find which entry covers which turbine. I suggest keeping 2028 for both units unless the plant's own research finds a 2029 date.

### Sailfish Council Bluffs data center campus
*watch item, new to the tracker; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
- what to watch: The developer says on-site gas will supply part of the power, but no gas generating capacity, permit or equipment has been named.
- check again by: 2027-01
  - links: https://datacenterdynamics.com/en/news/sailfish-plans-multi-gigawatt-data-center-park-outside-dfw-texas (ok=True, contains_value=True)
  - links: https://www.blackridgeresearch.com/news-releases/edged-us-tops-out-two-data-center-buildings-at-council-bluffs-campus-targeting-200-mw-of-capacity (ok=True, contains_value=True)
- notes: A Data Center Dynamics article on Sailfish Digital Ventures from 2025 says the company plans, in Council Bluffs, Iowa, a ten-building, 1 GW campus powered in part by on-site natural gas generation on a 306-acre site. The article is mainly about a Texas campus. A Council Bluffs paragraph sits in the same story, and the Sailfish chief executive says the company has partnered with a natural gas generation developer. I found no source that gives the gas capacity at Council Bluffs, the gas generation partner, a street address, an air permit, a generating certificate or a start of construction. The article says Sailfish had not yet delivered a data center, so the campus may not be funded. The 1 GW figure is the campus size, not the generating capacity. If it is added later, the captive fields would be captive industry use power and captive industry type data center. I searched for Council Bluffs gas generation for other developers too. The only other new Council Bluffs campus I found, Edged's two-building site, is reported at about 200 MW of load with no gas generation.

## Checklist group 8. New to the tracker

New plants and units ready to add, candidates to watch, and the possible-updates rows.

### Ames GT power station / GT1
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `GT1`
- `Capacity (MW)`: `` -> `21.3`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1972`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator GT1 at Ames GT, EIA plant 6463, as an operating combustion turbine of 21.3 MW that started in 1972. GEM does not have this unit. The table gives the fuel as distillate fuel oil, the same as unit GT2. The owner is City of Ames (Iowa), the same as the other units at this plant; please copy it from them. Its Other IDs (unit) entry is EIA: GT1.

### Burlington Generating Station / GT1
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `GT1`
- `Capacity (MW)`: `` -> `19.7`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1994`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator GT1 at Burlington, EIA plant 1104, as an operating combustion turbine of 19.7 MW that started in 1994. GEM does not have this unit. The table gives a planned retirement year of 2030. The new gas engines (Unit 2) are meant to replace these turbines, so Unit 2 can be linked to them as a replacement. The owner is Interstate Power and Light Co, the same as the other units at this plant; please copy it from them. Its Other IDs (unit) entry is EIA: GT1.

### Burlington Generating Station / GT2
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `GT2`
- `Capacity (MW)`: `` -> `19.7`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1995`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator GT2 at Burlington, EIA plant 1104, as an operating combustion turbine of 19.7 MW that started in 1995. GEM does not have this unit. The table gives a planned retirement year of 2030. The new gas engines (Unit 2) are meant to replace these turbines, so Unit 2 can be linked to them as a replacement. The owner is Interstate Power and Light Co, the same as the other units at this plant; please copy it from them. Its Other IDs (unit) entry is EIA: GT2.

### Burlington Generating Station / GT3
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `GT3`
- `Capacity (MW)`: `` -> `19.7`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1996`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator GT3 at Burlington, EIA plant 1104, as an operating combustion turbine of 19.7 MW that started in 1996. GEM does not have this unit. The table gives a planned retirement year of 2030. The new gas engines (Unit 2) are meant to replace these turbines, so Unit 2 can be linked to them as a replacement. The owner is Interstate Power and Light Co, the same as the other units at this plant; please copy it from them. Its Other IDs (unit) entry is EIA: GT3.

### Burlington Generating Station / GT4
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `GT4`
- `Capacity (MW)`: `` -> `19.7`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1994`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator GT4 at Burlington, EIA plant 1104, as an operating combustion turbine of 19.7 MW that started in 1994. GEM does not have this unit. The table gives a planned retirement year of 2030. The new gas engines (Unit 2) are meant to replace these turbines, so Unit 2 can be linked to them as a replacement. The owner is Interstate Power and Light Co, the same as the other units at this plant; please copy it from them. Its Other IDs (unit) entry is EIA: GT4.

### Summit Lake power station / GT1
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `GT1`
- `Capacity (MW)`: `` -> `27.0`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1973`
- `Turbine/Engine Technology`: `` -> `gas turbine`
- `Owner(s)`: `` -> `Central Iowa Power Cooperative [100%]`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://swiarec.coop/sites/default/files/documents/cipco_legis_brochure_2022.pdf (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator GT1 at Summit Lake, EIA plant 1206, as an operating natural gas combustion turbine of 27.0 MW that started in 1973. GEM has only the three-engine unit at this plant. The owner is the same cooperative that owns the engines, as its 2022 brochure shows. Its Other IDs (unit) entry is EIA: GT1.

### Summit Lake power station / GT2
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `GT2`
- `Capacity (MW)`: `` -> `35.3`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1975`
- `Turbine/Engine Technology`: `` -> `gas turbine`
- `Owner(s)`: `` -> `Central Iowa Power Cooperative [100%]`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://swiarec.coop/sites/default/files/documents/cipco_legis_brochure_2022.pdf (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator GT2 at Summit Lake, EIA plant 1206, as an operating natural gas combustion turbine of 35.3 MW that started in 1975. GEM has only the three-engine unit at this plant. The owner is the same cooperative that owns the engines, as its 2022 brochure shows. Its Other IDs (unit) entry is EIA: GT2.

### G100001074208 / Alliant Fairfax power station / Unit 2
*question about existing data*
- about: identity
- recommendation: Treat Fairfax and Morgan Valley as separate entries. Fairfax is the dropped first proposal. Morgan Valley is the replacement, so a reviewer may want to link them in the notes.
  - links: https://corridorbusiness.com/alliant-energy-proposes-new-site-near-fairfax-for-natural-gas-power-plant/ (ok=None, contains_value=None)
- notes: Both are Alliant projects near Fairfax in Linn County. The sites differ and the sizes differ. I did not find a document that calls Morgan Valley the same project as Fairfax. The Sierra Club list showing Unit 2 as planned most likely reflects Morgan Valley.

### Coralville gas turbines
*watch item, new to the tracker; checklist rows 51 (Newly announced projects checked)*
- what to watch: Each unit is under 50 MW, and whether units that add up past 50 MW at one site count is not decided for Iowa.
- check again by: 2027-01
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026 lists Coralville gas turbines, EIA plant code 1079, in Johnson County, owned by MidAmerican Energy Co. Units: generators 1, 2, 3 and 4, each 18.0 MW, natural gas fired combustion turbines (prime mover GT, energy source NG), all operating since 1970; sheet Operating. Should these units be added? Each is under 50 MW, but together they are 72 MW.

### MISO queue J2945 Sub T 3 Hills 3
*watch item, new to the tracker; checklist rows 51 (Newly announced projects checked)*
- what to watch: A queue entry shows no owner, no site and no dated plan from the developer, so it is not yet a plant to add.
- check again by: 2027-01
  - links: https://www.misoenergy.org/api/giqueue/getprojects (ok=True, contains_value=True)
- notes: The public generator interconnection queue of the Midcontinent Independent System Operator, read in October 2026, lists project J2945 at the Sub T 3 Hills 3 345 kV point in Washington County, Iowa. It is a gas project of 350.0 MW, type gas steam turbine, with a planned service date of April 1, 2027. The application status is active, in the 2022 study cycle. The transmission owner is not named. The queue does not name the developer. Because the type is a steam turbine, this may be a combined cycle steam part or a data entry error. The in-service date is soon, but I found no news about it.

### MISO queue J2946 Salem Hickory Creek line
*watch item, new to the tracker; checklist rows 51 (Newly announced projects checked)*
- what to watch: A queue entry shows no owner, no site and no dated plan from the developer, so it is not yet a plant to add.
- check again by: 2027-01
  - links: https://www.misoenergy.org/api/giqueue/getprojects (ok=True, contains_value=True)
- notes: The public generator interconnection queue of the Midcontinent Independent System Operator, read in October 2026, lists project J2946 at the Salem to Hickory Creek 345 kV line in Dubuque County, Iowa. It is a gas project of 160.0 MW, type gas internal combustion engines, listed as diesel type piston engines, with a planned service date of April 1, 2027. The application status is active, in the 2022 study cycle. The transmission owner is ITC Midwest. The queue does not name the developer. Two more 160 MW gas engine entries (J3153 in Clinton County and J3154 in Franklin County) have the same size, date and study cycle. They look like one family of projects.

### MISO queue J3153 Beaver Channel
*watch item, new to the tracker; checklist rows 51 (Newly announced projects checked)*
- what to watch: A queue entry shows no owner, no site and no dated plan from the developer, so it is not yet a plant to add.
- check again by: 2027-01
  - links: https://www.misoenergy.org/api/giqueue/getprojects (ok=True, contains_value=True)
- notes: The public generator interconnection queue of the Midcontinent Independent System Operator, read in October 2026, lists project J3153 at the Beaver Channel 161 kV substation in Clinton County, Iowa. It is a gas project of 160.0 MW, type gas internal combustion engines, listed as diesel type piston engines, with a planned service date of April 1, 2027. The application status is active, in the 2022 study cycle. The transmission owner is ITC Midwest. The queue does not name the developer. It matches J2946 and J3154 in size and date.

### MISO queue J3154 Blackhawk Quinn line
*watch item, new to the tracker; checklist rows 51 (Newly announced projects checked)*
- what to watch: A queue entry shows no owner, no site and no dated plan from the developer, so it is not yet a plant to add.
- check again by: 2027-01
  - links: https://www.misoenergy.org/api/giqueue/getprojects (ok=True, contains_value=True)
- notes: The public generator interconnection queue of the Midcontinent Independent System Operator, read in October 2026, lists project J3154 at the Blackhawk to Quinn 345 kV line, shared with queue project J2892 in Franklin County, Iowa. It is a gas project of 160.0 MW, type gas internal combustion engines, listed as diesel type piston engines, with a planned service date of April 1, 2027. The application status is active, in the 2022 study cycle. The transmission owner is ITC Midwest. The queue does not name the developer. It matches J2946 and J3153 in size and date.

### MISO queue J4113 Killdeer
*watch item, new to the tracker; checklist rows 51 (Newly announced projects checked)*
- what to watch: A queue entry shows no owner, no site and no dated plan from the developer, so it is not yet a plant to add.
- check again by: 2027-01
  - links: https://www.misoenergy.org/api/giqueue/getprojects (ok=True, contains_value=True)
- notes: The public generator interconnection queue of the Midcontinent Independent System Operator, read in October 2026, lists project J4113 at the Killdeer substation in Cerro Gordo County, Iowa. It is a gas project of 787.4 MW, type simple-cycle combustion turbine, with a planned service date of June 30, 2028. The application status is active, in the 2025 study cycle, entered October 6, 2025. The transmission owner is ITC Midwest. The queue does not name the developer. Cleanview lists it as Killdeer, 787 MW. It is in the same county as Emery Station, where Alliant has proposed the Riverhawk Energy Center of about 1,200 MW in July 2026. The size and date differ, so I cannot say it is Riverhawk. Cleanview is a secondary site and I did not use it as a citation.

### MISO queue J4114 Haskins
*watch item, new to the tracker; checklist rows 51 (Newly announced projects checked)*
- what to watch: A queue entry shows no owner, no site and no dated plan from the developer, so it is not yet a plant to add.
- check again by: 2027-01
  - links: https://www.misoenergy.org/api/giqueue/getprojects (ok=True, contains_value=True)
- notes: The public generator interconnection queue of the Midcontinent Independent System Operator, read in October 2026, lists project J4114 at the Sub T Haskins point in Washington County, Iowa. It is a gas project of 525.0 MW, type simple-cycle combustion turbine, with a planned service date of July 31, 2030. The application status is active, in the 2025 study cycle, entered October 6, 2025. The transmission owner is MidAmerican Energy Co. The queue does not name the developer. I found no news or filing about a gas plant at this site. It could be one of MidAmerican's unsited plan placeholders, but the 525 MW size does not match any of them.

### MISO queue J4145 Emery
*watch item, new to the tracker; checklist rows 51 (Newly announced projects checked)*
- what to watch: A queue entry shows no owner, no site and no dated plan from the developer, so it is not yet a plant to add.
- check again by: 2027-01
  - links: https://www.misoenergy.org/api/giqueue/getprojects (ok=True, contains_value=True)
- notes: The public generator interconnection queue of the Midcontinent Independent System Operator, read in October 2026, lists project J4145 at the Emery point in Cerro Gordo County, Iowa. It is a gas project of 98.0 MW, type combined cycle, with a planned service date of June 30, 2028. The application status is active, in the 2026 study cycle. The transmission owner is ITC Midwest. The queue does not name the developer. It is at the same point as Emery Station. It may be an uprate or an addition to the existing plant, so a reviewer should check whether it needs a unit at Emery Station instead.

### G100001074296 / MidAmerican 2024 IRP power station 1 / 1 IRP
*question about existing data; checklist rows 51 (Newly announced projects checked)*
- about: existence
- recommendation: The two turbines the study dates to 2028 and 2029 appear to be the Orient Energy Center in Adair County, which GEM should hold as its own plant. This placeholder is the 2031 turbine and is a different unit.
- notes: A 2025 news report and MidAmerican's fact sheet describe Orient as about 465 MW in two turbines for 2028. I did not find a named site for the 2031 turbine.

### Muscatine Generating Station
*question about existing data*
- about: capacity-threshold
- recommendation: Watch only. A 35 MW gas turbine is below the 50 MW threshold. Ask the reviewer whether a unit this size should be added next to the coal units.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The plant is in GEM's coal tracker only. The EIA-860M table for August 2026 lists a planned natural gas combustion turbine, generator 10, at Muscatine Plant #1 (plant 1167, owned by the Board of Water Electric and Communications in Muscatine County). It is 35 MW, planned for 2027, with regulatory approvals received and construction not started. A 2024 public notice on the owner's website for generating certificate case GCU-2024-0003 described a combined heat and power facility of up to 45 MW, but that page now returns an error, so I could not confirm that it is the same project. I did not find a start of construction.

### G100001054496 / Orient Energy Center power station / 1
*question about existing data; checklist rows 51 (Newly announced projects checked)*
- about: existence
- recommendation: The IRP study lists 233 MW peaking plants in 2028 and 2029. The first two turbines here already add up to about 465 MW. No separate placeholder looks needed for them.
  - links: https://www.midamericanenergy.com/media/pdf/mec_resource_evaluation_study_11-1.pdf (ok=None, contains_value=None)
- notes: The study table shows 233 MW in each of 2028 and 2029. These match the two Orient turbines.

### River Hills gas turbines
*watch item, new to the tracker; checklist rows 51 (Newly announced projects checked)*
- what to watch: Each unit is under 50 MW, and whether units that add up past 50 MW at one site count is not decided for Iowa.
- check again by: 2027-01
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026 lists River Hills gas turbines, EIA plant code 1084, in Polk County, owned by MidAmerican Energy Co. Units: generators 1 to 8, each 16.0 MW, natural gas fired combustion turbines (prime mover GT, energy source NG), operating since 1966 (units 1 to 4), 1967 (units 5 and 6) and 1968 (units 7 and 8); sheet Operating. Should these units be added? Each is under 50 MW, but together they are 128 MW.

### Roquette America power plant
*watch item, new to the tracker; checklist rows 51 (Newly announced projects checked)*
- what to watch: Each unit is under 50 MW, and whether units that add up past 50 MW at one site count is not decided for Iowa.
- check again by: 2027-01
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026 lists Roquette America power plant, EIA plant code 57953, in Lee County, owned by Roquette America. Units: generator GT, 40.0 MW, natural gas fired combined cycle gas turbine (prime mover CT, energy source NG), operating since 2004; generator HRSG, 10.0 MW, the steam unit of the same combined cycle (prime mover CA, energy source NG), operating year 2004, status out of service and not expected to return to service in the next calendar year; generator ST, 34.4 MW, petroleum coke steam turbine (prime mover ST, energy source PC), operating since 2007; sheet Operating. The plant is in Keokuk. Should these units be added? Each is under 50 MW, but together they are 84.4 MW, or 50 MW for the gas combined cycle alone.

### G100000414185 / Summit Lake power station / IC
*question about existing data; checklist rows 51 (Newly announced projects checked)*
- about: existence
- recommendation: The two older gas turbines are listed as new units for this plant. Please confirm they are not already tracked under another plant name.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: The EIA-860M table for August 2026 lists two operating natural gas combustion turbines at Summit Lake, GT1 of 27.0 MW from 1973 and GT2 of 35.3 MW from 1975. The brief shows only the three-engine unit. A 2022 cooperative brochure gives a site total of 110 MW, which fits the engines plus the turbines. I did not find them as units in the brief, so they may be missing or may sit under another plant.

## Checklist group Other

### G100001071243 / Bobcat Energy Center / 1
*question about existing data*
- about: other
- recommendation: The Interstate Power and Light resource evaluation study comments from Synapse (April 2025) do not name Bobcat, so there is no plan value to report. The IRP box can stay unticked on this evidence.
- notes: I searched the document text for Bobcat and Marshalltown and found no match.

### G100001096185 / Emery Station power plant / RH
*question about existing data*
- about: other
- recommendation: The Interstate Power and Light resource evaluation study comments from Synapse (April 2025) do not name Emery Station or Riverhawk, so there is no plan value to report.
- notes: I searched the document text for Emery and Riverhawk and found no match.

### G100001054470 / Lime Creek power station / 1
*question about existing data*
- about: other
- recommendation: The City field is blank. Web listings place the plant near Mason City at 24510 Orchid Avenue in Cerro Gordo County, but I did not find a document that states the city, so no value is proposed.
- notes: City not filled.

### G100001094049 / Morgan Valley Energy Center / 1
*question about existing data*
- about: other
- recommendation: The Interstate Power and Light plan comments file on the checklist does not name Morgan Valley or Fairfax. It lists unsited additions, including a combined cycle unit in 2029 that GEM holds as IRP power station 1. A reviewer should decide whether Morgan Valley's 720 MW replaces that placeholder.
- notes: The plan file is a consultant's comments on the study, not the study itself. No finding here comes from the plan, so the IRP box was not flagged.

### G100000403018 / Prairie Creek Generating Station / Unit 4- timepoint 2
*question about existing data*
- about: other
- recommendation: The unit name should be 'Unit 4, timepoint 2', with a comma and a space before the word timepoint.
- notes: The current name 'Unit 4- timepoint 2' uses a dash. Another unit name rule in this tracker uses 'name, timepoint N'.

### G100000403018 / Prairie Creek Generating Station / Unit 4- timepoint 2
*question about existing data*
- about: other
- recommendation: No change. GEM shows 149.0 MW and EIA shows 148.8 MW, which rounds the same.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: Alliant's 2025 annual report shows 126 MW, but that is a summer figure, not nameplate.

## Checklist group 9. Close-out

Not record-level: the sheet and doc updates, research status, and the two database checks. These boxes are ticked by hand after the edits are applied: validation_report.py --closeout must print CLOSE-OUT CLEAN (row 54) and no_tracker.py lists the units with no tracker (row 56).
