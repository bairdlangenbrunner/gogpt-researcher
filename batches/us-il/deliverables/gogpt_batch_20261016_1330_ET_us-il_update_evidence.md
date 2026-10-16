# Evidence — gogpt batch 20261016_1330_ET (us-il, update)

Each section below is one group of the GOGPT QC/Country checklist. The records in it are the evidence for ticking that group's boxes; the row numbers are the checklist tab's own.

## Utility resource plans (checklist row 37)

The US IRPs tab has no row for this state, so no plan was read. The IRP box stays as it is on every unit.


## Checklist group 1. Validation report

Edits and questions that fix an error from the GEM validation report.

### G100000409402 / CPV Three Rivers energy center / GEN1
*change to an existing unit; checklist rows 7 (Validation report errors fixed)*
**Action:** Set Employment Notes of all 2 units of CPV Three Rivers energy center to Operational workforce size: 25 full-time employees. It now says Unit GEN1: Construction workforce size: 300; Operational workforce size: 100; Unit GEN2: Construction workforce size: 300; Operational workforce size: 100. Add the link below to the Employment Notes Data Source box on each unit. Keep the links already there.
- `Employment Notes`: `Unit GEN1: Construction workforce size: 300; Operational workforce size: 100; Unit GEN2: Construction workforce size: 300; Operational workforce size: 100` -> `Operational workforce size: 25 full-time employees`
  - Employment Notes Data Source: https://cpv.com/wp-content/uploads/2025/06/CPV-Three-Rivers-Energy-Center-Project-Fact-Sheet-June2025-1.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A CPV project fact sheet from June 2025 says the plant has 25 full-time employees. GEM currently shows an operational workforce of 100 and a construction workforce of 300 for each unit. The fact sheet gives a different operating figure, 25 rather than 100. News coverage of the October 2023 dedication also mentions full-time staff, and a web search summary reported up to 900 workers at the construction peak, but I did not verify that figure on a page.

### G100001100702 / Aurora power station / --
*question about existing data; checklist rows 7 (Validation report errors fixed), 51 (Newly announced projects checked), 56 ("No tracker found" units reviewed)*
- about: existence
- recommendation: In the web form, delete the unit named "--" at Aurora power station, or fill it in if it is a real unit. It has no fuel, no capacity and no status history, and the name "--" is not allowed on a plant with more than one unit.
- notes: The database's validation report lists four problems on this unit: fuel, capacity and the status history are required but blank, and the name is "--". It also shows up on the list of units with no tracker, because it has no fuel. The ten real Aurora units are all present. This looks like an empty unit added by mistake. Nothing to research: this is a fix by hand.

### G100000410074 / Broadwing Energy Center / 1
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: Date the pre-construction step as October 2023, when Broadwing Energy announced signed agreements to build the plant.
  - links: https://decarbonfuse.com/posts/warwick-carbon-solutions-announces-construction-of-first-of-its-kind-lower-emission-power-facility-in-decatur (ok=True, contains_value=True)
  - links: https://wsgr.com/en/insights/firm-advises-warwick-carbon-solutions-on-its-first-of-its-kind-industrial-decarbonization-project.html (ok=True, contains_value=True)
- notes: The database's validation report says the pre-construction step has no date. A Broadwing Energy press release from October 2023 says formal agreements were signed to build the Decatur plant. A law firm announcement says those agreements covered real estate, interconnection and regulatory work. The month is firm. The exact day did not match on the page. The date the Illinois Environmental Protection Agency received the air permit application was not found. The February 2022 interconnection request in the old notes has no source, and no grid queue entry was found. An April 2021 trade story on an earlier, smaller design only announced intent, so it is not used.

### G100000402197 / Grand Tower energy center / CC01
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: Date the mothballed step in the status history of units CC01 and CC02 as 2021. A SIL News story from January 5, 2021 already reports that operations had ceased, so January 2021 is the earliest month a document supports.
  - links: https://silnews.com/stories/569938995-grand-tower-energy-center-shuts-down-operations (ok=True, contains_value=True)
  - links: https://dailyegyptian.com/123274/uncategorized/grand-tower-power-plant-under-redevelopment-many-expect-it-to-become-a-data-center/ (ok=True, contains_value=True)
- notes: The database's validation report says the mothballed step has no date. A SIL News story from January 5, 2021 says operations at the gas plant had ceased for an extended outage. A Daily Egyptian article from February 2026 says the plant ceased operations in February 2021. The two sources differ by a month, so the year is firm and the month is not. This is a date for the status history in the web form, not a cell in the export.

### G100001017993 / Joliet 29 Generating Station / Unit 7, timepoint 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: CCS attachment?
- recommendation: Leave the value as no. No document states it. Please decide whether the EIA-860M file already cited for the unit's other fields can stand as the source, as it does for the combined heat and power value.
- notes: The database's validation report says the carbon capture value has no data source. No document states that these units have no carbon capture. The EIA-860 annual generator files for 2021 to 2024 have a carbon capture column, but the cell is blank for these generators, not N, so it is not a statement either way. The value no is believable because the units were coal boilers converted to gas and are now retired.

### G100001017847 / Joliet 9 Generating Station / Unit 6, timepoint 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: CCS attachment?
- recommendation: Leave the value as no. No document states it. Please decide whether the EIA-860M file already cited for the unit's other fields can stand as the source, as it does for the combined heat and power value.
- notes: The database's validation report says the carbon capture value has no data source. No document states that these units have no carbon capture. The EIA-860 annual generator files for 2021 to 2024 have a carbon capture column, but the cell is blank for these generators, not N, so it is not a statement either way. The value no is believable because the units were coal boilers converted to gas and are now retired.

### G100000403820 / Lincoln Land energy center / GEN1
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: Date the pre-construction step of units GEN1 and GEN2 as April 2018, when the Illinois Environmental Protection Agency received the air permit application. If you prefer the date the permit was issued, use July 2022.
  - links: https://s3.documentcloud.org/documents/21169241/2021-10-1-draft-air-permit-for-lincoln-land-gas-plant.pdf (ok=True, contains_value=True)
  - links: https://www.powermag.com/illinois-epa-issues-permit-for-new-1-1-gw-gas-fired-facility/ (ok=True, contains_value=True)
- notes: The database's validation report says the pre-construction step has no date. The Illinois Environmental Protection Agency draft construction permit from October 2021 says the application was received on April 6, 2018. Seeking a permit is what pre-construction means, so the project was at that step by April 2018. A POWER magazine article says the permit was issued on July 29, 2022. No earlier interconnection or zoning filing was found.

### G100000403513 / Marion Plant / 5
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: Remove the undated mothballed step from the status history of units 5 and 6 instead of dating it. The plant's gas turbines generated power every year from 2020 to 2025.
  - links: https://www.eia.gov/electricity/data/eia923/archive/xls/f923_2025.zip (ok=True, contains_value=True)
  - links: https://sipower.org/power-supply/ (ok=True, contains_value=False)
  - links: https://siec.org/power-supplier (ok=True, contains_value=False)
- notes: The database's validation report says the mothballed step has no date. No document says units 5 or 6 were idled or mothballed. The EIA-923 annual generation files for plant 976 show the gas turbines produced power every year: about 4,300 MWh in 2020, 43,700 in 2021, 103,400 in 2022, 71,900 in 2023, 113,600 in 2024 and 93,100 in 2025. Those files report both turbines together, so they cannot show each unit on its own. The Southern Illinois Power Cooperative website and a member cooperative's website still list two 70 megawatt combustion turbines at Marion as part of the supply. A unit that ran every year was never inactive for a full year, so the step looks like a mistake.

### G100000403514 / Marion Plant / 6
*question about existing data; checklist rows 7 (Validation report errors fixed), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 50 (Other last-minute status changes checked)*
- about: Status
- recommendation: Ask the owner or check a second public source before accepting operating. Also ask when the mothballed step happened.
- notes: A mothballed status needs a dated source. None was found for units 5 and 6. The 2020 retirement of coal unit 4 is documented, but that is a different unit. A search found no 2021 or later article on mothballing the gas units.

### G100000409601 / Tate & Lyle Decatur cogeneration power station / GEN1
*question about existing data; checklist rows 7 (Validation report errors fixed), 13 (Coal-to-gas conversions have gas fuel and technology)*
- about: Conversion/replacement?
- recommendation: The database's validation report says this unit's replacement link points at a unit that does not exist. GEM has no coal unit for this Decatur corn mill, so there is no unit to link. The Archer Daniels Midland Decatur coal units in GEM belong to a different plant. Either clear the link or mark this as a conversion of the same unit.
  - links: https://www.tateandlyle.com/news/tate-lyle-delivers-its-commitment-eliminate-use-coal-all-its-operations (ok=True, contains_value=True)
- notes: A Tate and Lyle press release from November 2021 says the final coal system at the Decatur plant was decommissioned in October 2021 and that coal systems were replaced with natural gas combined heat and power. The only generator at this EIA plant is the 1989 steam turbine, so the coal boilers may have been replaced while the turbine stayed.

## Checklist group 2. Blanks and unknowns

Empty or unknown cells that the research filled, and the ones it could not.

### G100000403513 / Marion Plant / 5
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 5 (G100000403513) as 75.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `75.0` -> `75.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists generator 5 at 75.0 MW nameplate.

### G100000403514 / Marion Plant / 6
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 6 (G100000403514) as 75.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `75.0` -> `75.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists generator 6 at 75.0 MW nameplate.

### G100000402256 / Elwood Energy power station / GT1
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: Note which units carry which EIA plant code.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: EIA plant code 69979, MPH Elwood, carries GT1 to GT4 on the retired sheet and GT8 and GT9 on the operating sheet. Plant code 55199 stays with GT5 to GT7. The ID columns were left alone.

### G100000402197 / Grand Tower energy center / CC01
*question about existing data*
- about: Capacity (MW)
- recommendation: EIA lists a 223.2 MW gas turbine and an 80.9 MW steam unit for generator set 1 and 3, and 223.2 plus 113.6 MW for set 2 and 4. GEM shows 304 and 337 MW. This matches within rounding.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: No change needed.

### G100001017993 / Joliet 29 Generating Station / Unit 7, timepoint 2
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- recommendation: Leave the coordinates as they are. The EIA coordinates are about 30 meters away.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: The EIA table for August 2026 gives 41.494636 and -88.12383 for Joliet 29. GEM shows 41.494919 and -88.124342. The two points are very close, but no document I found states GEM's exact numbers, so the location source stays empty. A researcher may choose to cite the EIA table for the location.

### G100001017993 / Joliet 29 Generating Station / Unit 7, timepoint 2
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: Match GEM Unit 7 to EIA generator 7, and GEM Unit 8 to EIA generator 8, at plant 384.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: The EIA table for August 2026 lists generator 7 (660 MW, natural gas steam turbine, operating April 1965, retired September 2023) and generator 8 (660 MW, same type, operating March 1966, retired September 2023). The names and capacities line up one to one. GEM shows start year 2018 for both because they restarted on gas then. Generator 8 is the match for Unit 8 and not another candidate for Unit 7.

### G100001017847 / Joliet 9 Generating Station / Unit 6, timepoint 2
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- recommendation: Keep GEM's coordinates unless a reviewer prefers the EIA point.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: The EIA-860M table for August 2026 puts the plant at 41.4931, -88.1153. GEM has 41.4949190, -88.1243420, about 0.8 km away. I did not find a document that states GEM's exact point, so Location Data Source stays empty.

### G100000403513 / Marion Plant / 5
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- recommendation: The EIA table gives slightly different coordinates from GEM. Keep GEM's values unless a reviewer prefers the EIA point.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: The August 2026 EIA-860M table places plant 976 at 37.619747, -88.95311. GEM has 37.6196810, -88.9529190. The two are about 15 meters apart, so the location is the same.

## Checklist group 3. Status and timeline

Status changes, start and retirement years, planned retirements, Latest Activity.

### G100000402477 / Aurora power station / CTG10
*change to an existing unit*
**Action:** Set Status Detail of unit CTG10 (G100000402477) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Aurora's own letter of June 30, 2026 gave a retirement date of January 1, 2030. A second letter from Aurora dated July 2, 2026 says PJM asked for continued operation until May 31, 2031, that Aurora agreed, and that the retirement notice is withdrawn. Both letters are on PJM's generator deactivation page. Because the notice was withdrawn, no planned retirement year is reported. Nothing else was checked for this unit. No planned retirement year is reported because Aurora withdrew its retirement notice on July 2, 2026.

### G100000402478 / Aurora power station / CTG2
*change to an existing unit*
**Action:** Set Status Detail of unit CTG2 (G100000402478) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Aurora's own letter of June 30, 2026 gave a retirement date of January 1, 2030. A second letter from Aurora dated July 2, 2026 says PJM asked for continued operation until May 31, 2031, that Aurora agreed, and that the retirement notice is withdrawn. Both letters are on PJM's generator deactivation page. Because the notice was withdrawn, no planned retirement year is reported. Nothing else was checked for this unit. No planned retirement year is reported because Aurora withdrew its retirement notice on July 2, 2026.

### G100000402479 / Aurora power station / CTG3
*change to an existing unit*
**Action:** Set Status Detail of unit CTG3 (G100000402479) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Aurora's own letter of June 30, 2026 gave a retirement date of January 1, 2030. A second letter from Aurora dated July 2, 2026 says PJM asked for continued operation until May 31, 2031, that Aurora agreed, and that the retirement notice is withdrawn. Both letters are on PJM's generator deactivation page. Because the notice was withdrawn, no planned retirement year is reported. Nothing else was checked for this unit. No planned retirement year is reported because Aurora withdrew its retirement notice on July 2, 2026.

### G100000402480 / Aurora power station / CTG4
*change to an existing unit*
**Action:** Set Status Detail of unit CTG4 (G100000402480) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Aurora's own letter of June 30, 2026 gave a retirement date of January 1, 2030. A second letter from Aurora dated July 2, 2026 says PJM asked for continued operation until May 31, 2031, that Aurora agreed, and that the retirement notice is withdrawn. Both letters are on PJM's generator deactivation page. Because the notice was withdrawn, no planned retirement year is reported. Nothing else was checked for this unit. No planned retirement year is reported because Aurora withdrew its retirement notice on July 2, 2026.

### G100000402481 / Aurora power station / CTG5
*change to an existing unit*
**Action:** Set Status Detail of unit CTG5 (G100000402481) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Aurora's own letter of June 30, 2026 gave a retirement date of January 1, 2030. A second letter from Aurora dated July 2, 2026 says PJM asked for continued operation until May 31, 2031, that Aurora agreed, and that the retirement notice is withdrawn. Both letters are on PJM's generator deactivation page. Because the notice was withdrawn, no planned retirement year is reported. Nothing else was checked for this unit. No planned retirement year is reported because Aurora withdrew its retirement notice on July 2, 2026.

### G100000402482 / Aurora power station / CTG6
*change to an existing unit*
**Action:** Set Status Detail of unit CTG6 (G100000402482) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Aurora's own letter of June 30, 2026 gave a retirement date of January 1, 2030. A second letter from Aurora dated July 2, 2026 says PJM asked for continued operation until May 31, 2031, that Aurora agreed, and that the retirement notice is withdrawn. Both letters are on PJM's generator deactivation page. Because the notice was withdrawn, no planned retirement year is reported. Nothing else was checked for this unit. No planned retirement year is reported because Aurora withdrew its retirement notice on July 2, 2026.

### G100000402483 / Aurora power station / CTG7
*change to an existing unit*
**Action:** Set Status Detail of unit CTG7 (G100000402483) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Aurora's own letter of June 30, 2026 gave a retirement date of January 1, 2030. A second letter from Aurora dated July 2, 2026 says PJM asked for continued operation until May 31, 2031, that Aurora agreed, and that the retirement notice is withdrawn. Both letters are on PJM's generator deactivation page. Because the notice was withdrawn, no planned retirement year is reported. Nothing else was checked for this unit. No planned retirement year is reported because Aurora withdrew its retirement notice on July 2, 2026.

### G100000402484 / Aurora power station / CTG8
*change to an existing unit*
**Action:** Set Status Detail of unit CTG8 (G100000402484) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Aurora's own letter of June 30, 2026 gave a retirement date of January 1, 2030. A second letter from Aurora dated July 2, 2026 says PJM asked for continued operation until May 31, 2031, that Aurora agreed, and that the retirement notice is withdrawn. Both letters are on PJM's generator deactivation page. Because the notice was withdrawn, no planned retirement year is reported. Nothing else was checked for this unit. No planned retirement year is reported because Aurora withdrew its retirement notice on July 2, 2026.

### G100000402485 / Aurora power station / CTG9
*change to an existing unit*
**Action:** Set Status Detail of unit CTG9 (G100000402485) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On June 30, 2026 Aurora Generation told PJM it would retire all ten units on January 1, 2030 because of the Illinois Climate and Equitable Jobs Act. On July 2, 2026 PJM asked for the units to keep running until May 31, 2031, Aurora agreed, and Aurora withdrew its retirement notice.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Aurora's own letter of June 30, 2026 gave a retirement date of January 1, 2030. A second letter from Aurora dated July 2, 2026 says PJM asked for continued operation until May 31, 2031, that Aurora agreed, and that the retirement notice is withdrawn. Both letters are on PJM's generator deactivation page. Because the notice was withdrawn, no planned retirement year is reported. Nothing else was checked for this unit. No planned retirement year is reported because Aurora withdrew its retirement notice on July 2, 2026.

### G100000410074 / Broadwing Energy Center / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Add the entry below at the top of the Status Detail box of unit 1 (G100000410074), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

A Power magazine article from October 23, 2025 reports that Google signed a power purchase agreement for the plant. Kiewit Power Constructors leads engineering, procurement and construction. The owner expects a financing decision in the second quarter of 2026 and commercial operation in 2030.

https://www.powermag.com/google-backs-first-u-s-gas-fired-power-plant-with-integrated-ccs-for-data-centers/
- `Status Detail`: `AM 4/13/26: Illinois EPA proposed a draft air construction permit / PSD approval for the project. https://oilandgaswatch.org/alert/dd7b8d37-3702-4a25-868e-be0f06045a1f
NF 1/13/25: COD - by the end of 2029. CCS component will be operational by early 2030. Currently in the permitting stage. It is being developed on an existing Archer Daniels Midland (ADM) site in Decatur, adjacent to ADM’s longtime CO₂ sequestration operation. Project financing expected to reach final investment decision in Q2 2026
NF 5/21/25: Construction to begin in 2026.
NF 6/3/24: Construction agreement signed between ADM and Warwick in Oct 2023. NF: Pre-FEED stage (Front-End Engineering Design) for the CCS project. 
Jenny: filed interconnection app in Feb 2022` -> `A Power magazine article from October 23, 2025 reports that Google signed a power purchase agreement for the plant. Kiewit Power Constructors leads engineering, procurement and construction. The owner expects a financing decision in the second quarter of 2026 and commercial operation in 2030.

https://www.powermag.com/google-backs-first-u-s-gas-fired-power-plant-with-integrated-ccs-for-data-centers/

AM 4/13/26: Illinois EPA proposed a draft air construction permit / PSD approval for the project. https://oilandgaswatch.org/alert/dd7b8d37-3702-4a25-868e-be0f06045a1f
NF 1/13/25: COD - by the end of 2029. CCS component will be operational by early 2030. Currently in the permitting stage. It is being developed on an existing Archer Daniels Midland (ADM) site in Decatur, adjacent to ADM’s longtime CO₂ sequestration operation. Project financing expected to reach final investment decision in Q2 2026
NF 5/21/25: Construction to begin in 2026.
NF 6/3/24: Construction agreement signed between ADM and Warwick in Oct 2023. NF: Pre-FEED stage (Front-End Engineering Design) for the CCS project. 
Jenny: filed interconnection app in Feb 2022`
  - Status Detail: https://www.powermag.com/google-backs-first-u-s-gas-fired-power-plant-with-integrated-ccs-for-data-centers/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The article names the plant, the Mitsubishi turbine, Kiewit and the financing and operating targets. I did not find a report that the financing decision has closed or that construction has started. Status stays pre-construction. I found no report after the October 2025 article that financing closed or construction began. Latest Activity is left alone because the newest report is under a year old.

### G100000403820 / Lincoln Land energy center / GEN1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Capacity (MW) of unit GEN1 (G100000403820) as 638.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `638.0` -> `638.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists plant 62022, generator GEN1, planned, natural gas fired combined cycle, nameplate 638.4 MW, planned operation June 2030. Status stays pre-construction. No construction start, financing close or cancellation was found. The turbine maker and model are still not found. Latest Activity is left alone because the newest report is from summer 2026.

### G100000403820 / Lincoln Land energy center / GEN1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Start year of unit GEN1 (G100000403820) as 2030. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2030` -> `2030`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 gives planned operation in June 2030 for generator GEN1.

### G100000403820 / Lincoln Land energy center / GEN1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Add the entry below at the top of the Status Detail box of unit GEN1 (G100000403820), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

An Illinois Times article carried by the Springfield Business Journal in summer 2026 says construction has not begun. Development control moved back from Kindle Energy to the original developer EmberClear. The Illinois Environmental Protection Agency construction permit was extended twice and now expires on January 1, 2027.

https://www.springfieldbusinessjournal.com/news/data-center-development-linked-to-power-plant-construction/
- `Status Detail`: `NF 6/7/24: Construction to begin in Q4 2024. Commissioning in Dec 2027 (EIA) or Jan 2028 (Kindle Energy). No data on the turbine model yet. NF: According to EIA 4/23, the station is planned for installation, but regulatory approvals not initiated. 7/2022 The Illinois Environmental Protection Agency issued a construction permit for the station. It would be able to incorporate 30% hydrogen and up to 100% within the lifespan of this project.` -> `An Illinois Times article carried by the Springfield Business Journal in summer 2026 says construction has not begun. Development control moved back from Kindle Energy to the original developer EmberClear. The Illinois Environmental Protection Agency construction permit was extended twice and now expires on January 1, 2027.

https://www.springfieldbusinessjournal.com/news/data-center-development-linked-to-power-plant-construction/

NF 6/7/24: Construction to begin in Q4 2024. Commissioning in Dec 2027 (EIA) or Jan 2028 (Kindle Energy). No data on the turbine model yet. NF: According to EIA 4/23, the station is planned for installation, but regulatory approvals not initiated. 7/2022 The Illinois Environmental Protection Agency issued a construction permit for the station. It would be able to incorporate 30% hydrogen and up to 100% within the lifespan of this project.`
  - Status Detail: https://www.springfieldbusinessjournal.com/news/data-center-development-linked-to-power-plant-construction/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The article names Lincoln Land Energy Center and the permit expiry date of January 1, 2027.

### G100000403821 / Lincoln Land energy center / GEN2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Capacity (MW) of unit GEN2 (G100000403821) as 638.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `638.0` -> `638.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 lists plant 62022, generator GEN2, planned, natural gas fired combined cycle, nameplate 638.4 MW, planned operation June 2030. Status stays pre-construction. No construction start, financing close or cancellation was found. The turbine maker and model are still not found. Latest Activity is left alone because the newest report is from summer 2026.

### G100000403821 / Lincoln Land energy center / GEN2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Start year of unit GEN2 (G100000403821) as 2030. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2030` -> `2030`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for August 2026 gives planned operation in June 2030 for generator GEN2.

### G100000403821 / Lincoln Land energy center / GEN2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Add the entry below at the top of the Status Detail box of unit GEN2 (G100000403821), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

An Illinois Times article carried by the Springfield Business Journal in summer 2026 says construction has not begun. Development control moved back from Kindle Energy to the original developer EmberClear. The Illinois Environmental Protection Agency construction permit was extended twice and now expires on January 1, 2027.

https://www.springfieldbusinessjournal.com/news/data-center-development-linked-to-power-plant-construction/
- `Status Detail`: `EIA August 2024: start year 2028 for GEN2, same status as 2023. NF 6/7/24: Construction to begin in Q4 2024. Commissioning in Dec 2027 (EIA) or Jan 2028 (Kindle Energy). No data on the turbine model yet. NF: According to EIA 4/23, the station is planned for installation, but regulatory approvals not initiated. 7/2022 The Illinois Environmental Protection Agency issued a construction permit for the station. It would be able to incorporate 30% hydrogen and up to 100% within the lifespan of this project.` -> `An Illinois Times article carried by the Springfield Business Journal in summer 2026 says construction has not begun. Development control moved back from Kindle Energy to the original developer EmberClear. The Illinois Environmental Protection Agency construction permit was extended twice and now expires on January 1, 2027.

https://www.springfieldbusinessjournal.com/news/data-center-development-linked-to-power-plant-construction/

EIA August 2024: start year 2028 for GEN2, same status as 2023. NF 6/7/24: Construction to begin in Q4 2024. Commissioning in Dec 2027 (EIA) or Jan 2028 (Kindle Energy). No data on the turbine model yet. NF: According to EIA 4/23, the station is planned for installation, but regulatory approvals not initiated. 7/2022 The Illinois Environmental Protection Agency issued a construction permit for the station. It would be able to incorporate 30% hydrogen and up to 100% within the lifespan of this project.`
  - Status Detail: https://www.springfieldbusinessjournal.com/news/data-center-development-linked-to-power-plant-construction/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The article names Lincoln Land Energy Center and the permit expiry date of January 1, 2027.

### G100000403457 / NRG Rockford I power station / 1
*change to an existing unit*
**Action:** Set Status Detail of unit 1 (G100000403457) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

July 2026: PJM asked NRG to keep Rockford running until May 31, 2031 instead of closing by December 31, 2029 under the Illinois Climate and Equitable Jobs Act. NRG agreed on July 2, 2026 and withdrew its deactivation notice.

https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/generation-resources/ceja-reliability-extension-agreements/nrg-energy-inc-illinois.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf
- `Status Detail`: `` -> `July 2026: PJM asked NRG to keep Rockford running until May 31, 2031 instead of closing by December 31, 2029 under the Illinois Climate and Equitable Jobs Act. NRG agreed on July 2, 2026 and withdrew its deactivation notice.

https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/generation-resources/ceja-reliability-extension-agreements/nrg-energy-inc-illinois.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/generation-resources/ceja-reliability-extension-agreements/nrg-energy-inc-illinois.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: PJM's letter of July 2, 2026 asks for continued operation of the Rockford units until May 31, 2031. The Rockford Generation letter of the same date says it agreed to the plan and withdraws its earlier deactivation notice. No Planned retire year is recorded because the notice was withdrawn. The August 2026 EIA-860M table lists this unit as operating with the same capacity and start year as GEM, so no change is needed. The operator is not named in that table.

### G100000403458 / NRG Rockford I power station / 2
*change to an existing unit*
**Action:** Set Status Detail of unit 2 (G100000403458) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

July 2026: PJM asked NRG to keep Rockford running until May 31, 2031 instead of closing by December 31, 2029 under the Illinois Climate and Equitable Jobs Act. NRG agreed on July 2, 2026 and withdrew its deactivation notice.

https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/generation-resources/ceja-reliability-extension-agreements/nrg-energy-inc-illinois.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf
- `Status Detail`: `` -> `July 2026: PJM asked NRG to keep Rockford running until May 31, 2031 instead of closing by December 31, 2029 under the Illinois Climate and Equitable Jobs Act. NRG agreed on July 2, 2026 and withdrew its deactivation notice.

https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/generation-resources/ceja-reliability-extension-agreements/nrg-energy-inc-illinois.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/generation-resources/ceja-reliability-extension-agreements/nrg-energy-inc-illinois.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: PJM's letter of July 2, 2026 asks for continued operation of the Rockford units until May 31, 2031. The Rockford Generation letter of the same date says it agreed to the plan and withdraws its earlier deactivation notice. No Planned retire year is recorded because the notice was withdrawn. The August 2026 EIA-860M table lists this unit as operating with the same capacity and start year as GEM, so no change is needed. The operator is not named in that table.

### G100000403459 / NRG Rockford II energy center / GT3
*change to an existing unit*
**Action:** Set Status Detail of unit GT3 (G100000403459) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

July 2026: PJM asked NRG to keep Rockford running until May 31, 2031 instead of closing by December 31, 2029 under the Illinois Climate and Equitable Jobs Act. NRG agreed on July 2, 2026 and withdrew its deactivation notice.

https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/generation-resources/ceja-reliability-extension-agreements/nrg-energy-inc-illinois.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf
- `Status Detail`: `` -> `July 2026: PJM asked NRG to keep Rockford running until May 31, 2031 instead of closing by December 31, 2029 under the Illinois Climate and Equitable Jobs Act. NRG agreed on July 2, 2026 and withdrew its deactivation notice.

https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/generation-resources/ceja-reliability-extension-agreements/nrg-energy-inc-illinois.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/generation-resources/ceja-reliability-extension-agreements/nrg-energy-inc-illinois.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: PJM's letter of July 2, 2026 asks for continued operation of the Rockford units until May 31, 2031. The Rockford Generation letter of the same date says it agreed to the plan and withdraws its earlier deactivation notice. No Planned retire year is recorded because the notice was withdrawn. The August 2026 EIA-860M table lists this unit as operating with the same capacity and start year as GEM, so no change is needed. The operator is not named in that table.

### G100000403701 / University Park South power station / UPG1
*change to an existing unit*
**Action:** Set Status Detail of unit UPG1 (G100000403701) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The owner, University Park Energy, filed a retirement notice with PJM on June 30, 2026 asking for January 1, 2030. PJM's July 2, 2026 reply asked for operation through May 31, 2031. The owner's withdrawal letter of July 2, 2026 says it agreed to that plan and withdrew the notice. Both letters are on PJM's deactivation notices page. Because the notice was withdrawn, no planned retirement year is reported. The owner withdrew its retirement notice on July 2, 2026, so no planned retirement year is reported. Nothing else was checked, as the brief asked.

### G100000403702 / University Park South power station / UPG2
*change to an existing unit*
**Action:** Set Status Detail of unit UPG2 (G100000403702) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The owner, University Park Energy, filed a retirement notice with PJM on June 30, 2026 asking for January 1, 2030. PJM's July 2, 2026 reply asked for operation through May 31, 2031. The owner's withdrawal letter of July 2, 2026 says it agreed to that plan and withdrew the notice. Both letters are on PJM's deactivation notices page. Because the notice was withdrawn, no planned retirement year is reported. The owner withdrew its retirement notice on July 2, 2026, so no planned retirement year is reported. Nothing else was checked, as the brief asked.

### G100000403703 / University Park South power station / UPG3
*change to an existing unit*
**Action:** Set Status Detail of unit UPG3 (G100000403703) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The owner, University Park Energy, filed a retirement notice with PJM on June 30, 2026 asking for January 1, 2030. PJM's July 2, 2026 reply asked for operation through May 31, 2031. The owner's withdrawal letter of July 2, 2026 says it agreed to that plan and withdrew the notice. Both letters are on PJM's deactivation notices page. Because the notice was withdrawn, no planned retirement year is reported. The owner withdrew its retirement notice on July 2, 2026, so no planned retirement year is reported. Nothing else was checked, as the brief asked.

### G100000403704 / University Park South power station / UPG4
*change to an existing unit*
**Action:** Set Status Detail of unit UPG4 (G100000403704) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The owner, University Park Energy, filed a retirement notice with PJM on June 30, 2026 asking for January 1, 2030. PJM's July 2, 2026 reply asked for operation through May 31, 2031. The owner's withdrawal letter of July 2, 2026 says it agreed to that plan and withdrew the notice. Both letters are on PJM's deactivation notices page. Because the notice was withdrawn, no planned retirement year is reported. The owner withdrew its retirement notice on July 2, 2026, so no planned retirement year is reported. Nothing else was checked, as the brief asked.

### G100000403705 / University Park South power station / UPG5
*change to an existing unit*
**Action:** Set Status Detail of unit UPG5 (G100000403705) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The owner, University Park Energy, filed a retirement notice with PJM on June 30, 2026 asking for January 1, 2030. PJM's July 2, 2026 reply asked for operation through May 31, 2031. The owner's withdrawal letter of July 2, 2026 says it agreed to that plan and withdrew the notice. Both letters are on PJM's deactivation notices page. Because the notice was withdrawn, no planned retirement year is reported. The owner withdrew its retirement notice on July 2, 2026, so no planned retirement year is reported. Nothing else was checked, as the brief asked.

### G100000403706 / University Park South power station / UPG6
*change to an existing unit*
**Action:** Set Status Detail of unit UPG6 (G100000403706) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf
- `Status Detail`: `` -> `On July 2, 2026 PJM asked the owner to keep the plant running through May 31, 2031 under the Illinois Climate and Equitable Jobs Act, and the owner agreed the same day and withdrew its June 30, 2026 retirement notice for January 1, 2030.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf
https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=True, contains_value=True)
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The owner, University Park Energy, filed a retirement notice with PJM on June 30, 2026 asking for January 1, 2030. PJM's July 2, 2026 reply asked for operation through May 31, 2031. The owner's withdrawal letter of July 2, 2026 says it agreed to that plan and withdrew the notice. Both letters are on PJM's deactivation notices page. Because the notice was withdrawn, no planned retirement year is reported. The owner withdrew its retirement notice on July 2, 2026, so no planned retirement year is reported. Nothing else was checked, as the brief asked.

### G100000402476 / Aurora power station / CTG1
*question about existing data; checklist rows 21 (Planned retirements searched)*
- about: Planned retire
- recommendation: Leave Planned retire blank for all ten units for now. Recheck when PJM and Aurora settle the terms of continued operation.
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=None, contains_value=None)
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=None, contains_value=None)
- notes: Aurora's letter of July 2, 2026 says it agreed to PJM's request to run the units until May 31, 2031 and withdrew its retirement notice. The June 30 cover letter said the agreement depends on PJM committing to keep the units running through the 2029 to 2030 and 2030 to 2031 delivery years with appropriate pay. So the extension was accepted, with conditions. The Illinois law deadline of January 1, 2030 is not a retirement date by itself.

### G100000402476 / Aurora power station / CTG1
*watch item at an existing plant*
- what to watch: The retirement notice was withdrawn, but the units may still close by May 31, 2031 or after the state resource plan in 2028.
- check again by: 2027-06
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=None, contains_value=None)
- notes: Watch PJM's deactivation page for a new notice from Aurora Generation.

### G100000410074 / Broadwing Energy Center / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- about: Start year
- recommendation: Please check whether the start year should move from 2029 to 2030.
  - links: https://www.powermag.com/google-backs-first-u-s-gas-fired-power-plant-with-integrated-ccs-for-data-centers/ (ok=None, contains_value=None)
- notes: The Power magazine article from October 23, 2025 says commercial operation is targeted for 2030. Earlier company statements said steam and power by the end of 2029 and carbon capture by early 2030. GEM shows 2029.

### G100000402260 / Elwood Energy power station / GT5
*question about existing data; checklist rows 21 (Planned retirements searched), 23 (Planned retirement year not in the past)*
- about: Planned retire
- recommendation: Clear the planned retirement year of 2025 for units 5, 6 and 7.
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-withdraw-letter.pdf (ok=None, contains_value=None)
- notes: Dairyland withdrew the retirement notice on May 6, 2026, and the EIA-860M table for August 2026 still lists these units as operating.

### G100000402263 / Elwood Energy power station / GT8
*question about existing data; checklist rows 50 (Other last-minute status changes checked)*
- about: Status
- recommendation: Check units 8 and 9 against federal data.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-revision-8-9.pdf (ok=None, contains_value=None)
- notes: GEM shows GT8 and GT9 as retired. PJM's May 2025 letter said they would retire on June 1, 2025 if the Hull Street sale closed. The EIA-860M table for August 2026 still lists both under plant 69979 as operating, 192 MW each. They may not have retired.

### G100001017847 / Joliet 9 Generating Station / Unit 6, timepoint 2
*question about existing data*
- about: Start year
- recommendation: Check that 2018 is the intended start year.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: The EIA-860M table gives an operating year of 1959 for this generator. GEM's 2018 is the year of the gas conversion, which fits the conversion naming. No change proposed.

### G100000403820 / Lincoln Land energy center / GEN1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 50 (Other last-minute status changes checked)*
- about: Status
- recommendation: EIA lists both generators as planned with regulatory approvals not initiated, while GEM has pre-construction because the state permit exists. I left the status alone.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: The state permit is from July 2022 per the existing text and was extended twice.

### G100000403820 / Lincoln Land energy center / GEN1
*watch item at an existing plant; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- what to watch: The construction permit expires on January 1, 2027 and the developer has changed, so a cancellation or a new extension is possible.
- check again by: 2027-01
  - links: https://www.springfieldbusinessjournal.com/news/data-center-development-linked-to-power-plant-construction/ (ok=None, contains_value=None)
- notes: Check the Illinois Environmental Protection Agency permit record after January 2027.

### G100000403513 / Marion Plant / 5
*question about existing data; checklist rows 21 (Planned retirements searched)*
- about: Planned retire
- recommendation: No deactivation notice found.
- notes: I did not find a PJM deactivation notice, and Marion is in the grid operator MISO, not PJM. No planned retirement is proposed. The 2021 Illinois law deadline is not a retirement date.

### G100000403457 / NRG Rockford I power station / 1
*question about existing data; checklist rows 21 (Planned retirements searched)*
- about: Planned retire
- recommendation: Do not record a planned retirement year for now.
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf (ok=None, contains_value=None)
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-revised-notice.pdf (ok=None, contains_value=None)
- notes: NRG's earlier notice set deactivation for December 31, 2029 (revised notice of March 2, 2026). On July 2, 2026 NRG agreed to PJM's request to keep the plant running until May 31, 2031 and withdrew the notice. So NRG's own letters no longer give a retirement date. The 2029 deadline comes from state law, not from an owner plan.

### G100000403457 / NRG Rockford I power station / 1
*watch item at an existing plant*
- what to watch: The state law deadline of December 31, 2029 is paused by the reliability agreement through May 31, 2031, so the planned retirement may return.
- check again by: 2027-06
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf (ok=None, contains_value=None)
- notes: Check the PJM deactivation page for a new notice before the 2030 to 2031 capacity auction.

### G100000403459 / NRG Rockford II energy center / GT3
*question about existing data; checklist rows 21 (Planned retirements searched)*
- about: Planned retire
- recommendation: Do not record a planned retirement year for now.
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf (ok=None, contains_value=None)
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-revised-notice.pdf (ok=None, contains_value=None)
- notes: NRG's earlier notice set deactivation for December 31, 2029 (revised notice of March 2, 2026). On July 2, 2026 NRG agreed to PJM's request to keep the plant running until May 31, 2031 and withdrew the notice. So NRG's own letters no longer give a retirement date. The 2029 deadline comes from state law, not from an owner plan.

### G100000403459 / NRG Rockford II energy center / GT3
*watch item at an existing plant*
- what to watch: The state law deadline of December 31, 2029 is paused by the reliability agreement through May 31, 2031, so the planned retirement may return.
- check again by: 2027-06
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/rockford-withdrawal.pdf (ok=None, contains_value=None)
- notes: Check the PJM deactivation page for a new notice before the 2030 to 2031 capacity auction.

### G100000403113 / University Park North power station / 1
*question about existing data; checklist rows 21 (Planned retirements searched)*
- about: Planned retire
- recommendation: Do not record a planned retirement year for any of the twelve units. Consider adding a note on the plant's status that the owner agreed to keep the units running to May 2031 if PJM needs them.
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=None, contains_value=None)
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=None, contains_value=None)
- notes: On June 30, 2026 the owner, LSP University Park LLC, sent PJM a deactivation notice for University Park North units 1 to 12 with a retirement date of January 1, 2030. On July 2, 2026 PJM asked for continued operation until May 31, 2031 under the Illinois Climate and Equitable Jobs Act. The same day the owner agreed to that plan and withdrew its deactivation notice in a letter posted on PJM's deactivation page. So the owner has accepted the extension and no deactivation notice stands. A statutory deadline is not a retirement date, so Planned retire stays blank.

### G100000403701 / University Park South power station / UPG1
*question about existing data; checklist rows 21 (Planned retirements searched)*
- about: Planned retire
- recommendation: Do not enter a planned retirement year yet. The owner accepted PJM's request to keep the units running through May 31, 2031 and withdrew its notice. Check PJM's page again in 2027 and 2028.
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=None, contains_value=None)
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-deactivation-letter.pdf (ok=None, contains_value=None)
- notes: The owner's June 30, 2026 notice named January 1, 2030, but the withdrawal letter of July 2, 2026 cancels it. The May 31, 2031 date is a PJM request for continued operation, not a retirement date set by the owner. PJM's letter to NRG is not on the page under that name. The owner's letters say the owner agreed. The brief's question about whether NRG accepted is answered yes in the withdrawal letter.

### G100000403701 / University Park South power station / UPG1
*watch item at an existing plant*
- what to watch: The owner agreed to run the plant to May 31, 2031 but may file a new retirement notice later.
- check again by: 2027-06
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/il-assets-withdrawal-letters.pdf (ok=None, contains_value=None)
- notes: Watch PJM's deactivation notices page for a new letter for University Park South.

### G100000403786 / Zion energy center / CTG1
*question about existing data; checklist rows 21 (Planned retirements searched)*
- about: Planned retire
- recommendation: Do not enter a planned retirement year for units 1, 2 and 3 at this time.
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/zion-ct1-ct2-ct3-deactivation-notice.pdf (ok=None, contains_value=None)
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/zion-ct1-ct2-ct3-withdrawal.pdf (ok=None, contains_value=None)
- notes: Constellation sent PJM a deactivation notice on June 22, 2026 for Zion units 1, 2 and 3, effective December 31, 2029, to meet the Illinois Climate and Equitable Jobs Act. PJM replied that the plant is needed and asked for operation through May 2031. On July 2, 2026 Constellation wrote that it intends to withdraw the notice and take part in the capacity auctions for those years. The letter says a formal withdrawal will follow, and I did not find it. So the 2029 date is no longer the owner's plan. Please recheck the PJM page for the formal withdrawal.

### G100000403786 / Zion energy center / CTG1
*watch item at an existing plant*
- what to watch: The owner said it intends to withdraw its 2029 retirement notice but the formal withdrawal is not yet seen.
- check again by: 2026-12
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/zion-ct1-ct2-ct3-withdrawal.pdf (ok=None, contains_value=None)
- notes: Check the PJM deactivation notices page for a formal withdrawal letter for Zion units 1 to 3.

## Checklist group 4. Conversions

Coal-to-gas and other conversions: unit naming, fuel and technology, replacement links.

### G100001017993 / Joliet 29 Generating Station / Unit 7, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 7, timepoint 2 (G100001017993) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.power-eng.com/coal/illinois-epa-oks-air-permit-for-joliet-coal-to-gas-conversion/ (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: A Power Engineering article from October 2015 says the Illinois EPA issued a permit for NRG to convert Units 6 to 8 at the Joliet plant from coal to natural gas, and that Units 7 and 8 are part of Joliet 29. It describes the plan, not the finished conversion. The EIA table for August 2026 shows both units burning natural gas.

### G100001017949 / Joliet 29 Generating Station / Unit 8, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 8, timepoint 2 (G100001017949) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.power-eng.com/coal/illinois-epa-oks-air-permit-for-joliet-coal-to-gas-conversion/ (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: A Power Engineering article from October 2015 says the Illinois EPA issued a permit for NRG to convert Units 6 to 8 at the Joliet plant from coal to natural gas, and that Units 7 and 8 are part of Joliet 29. It describes the plan, not the finished conversion. The EIA table for August 2026 shows both units burning natural gas.

### G100001017847 / Joliet 9 Generating Station / Unit 6, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 6, timepoint 2 (G100001017847) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.power-eng.com/coal/illinois-epa-oks-air-permit-for-joliet-coal-to-gas-conversion/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Power Engineering article from October 2015 says the Illinois EPA issued a final air construction permit for NRG Energy to convert the three coal-fired units 6 to 8 at the Joliet plant to burn natural gas. So unit 6 is a conversion.

### G100000409601 / Tate & Lyle Decatur cogeneration power station / GEN1
*question about existing data; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
- about: Fuel
- recommendation: Consider removing coal from the fuel list.
  - links: https://www.tateandlyle.com/news/tate-lyle-delivers-its-commitment-eliminate-use-coal-all-its-operations (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: The EIA table lists only natural gas for this generator, and the 2021 press release says the last coal system at Decatur was decommissioned. The EIA table is the source here, so I left Fuel unchanged.

## Checklist group 6. Owners and entities

Owner, operator and parent changes, and new owners or operators to create.

### G100001017993 / Joliet 29 Generating Station / Unit 7, timepoint 2
*change to an existing unit*
**Action:** Leave Owner(s) of unit Unit 7, timepoint 2 (G100001017993) as Midwest Generation EME LLC [100%]. It is still correct. Add the link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Midwest Generation EME LLC [100%]` -> `Midwest Generation EME LLC [100%]`
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The EIA table for August 2026 lists plant 384, Joliet 29, generator 7, under the owner name Midwest Generations EME LLC. That is a spelling variant of GEM's owner name. The table does not give a share. I could not find a document that states the coordinates or says whether carbon capture is attached. See the questions for details.

### G100001017949 / Joliet 29 Generating Station / Unit 8, timepoint 2
*change to an existing unit*
**Action:** Leave Owner(s) of unit Unit 8, timepoint 2 (G100001017949) as Midwest Generation EME LLC [100%]. It is still correct. Add the link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Midwest Generation EME LLC [100%]` -> `Midwest Generation EME LLC [100%]`
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The EIA table for August 2026 lists plant 384, Joliet 29, generator 8, under the owner name Midwest Generations EME LLC. That is a spelling variant of GEM's owner name. The table does not give a share. I could not find a document that states the coordinates or says whether carbon capture is attached. See the questions for details.

### G100001017847 / Joliet 9 Generating Station / Unit 6, timepoint 2
*change to an existing unit*
**Action:** Leave Owner(s) of unit Unit 6, timepoint 2 (G100001017847) as Midwest Generation EME LLC [100%]. It is still correct. Add the link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Midwest Generation EME LLC [100%]` -> `Midwest Generation EME LLC [100%]`
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The EIA-860M table for August 2026 lists the owner of Joliet 9, generator 6, as Midwest Generations EME LLC. The spelling has an extra s, but it is clearly the same company. The table names one owner and gives no share, so the 100 percent is implied. I read the name in the downloaded file. The EIA-860M table for August 2026 lists generator 6 as retired in June 2023, 360.4 MW, natural gas steam turbine, operating since June 1959. That matches GEM's status, capacity and retired year. I found no document that states a carbon capture value for this unit.

### G100000403513 / Marion Plant / 5
*change to an existing unit*
**Action:** Leave Owner(s) of all 2 units of Marion Plant as Southern Illinois Power Cooperative Inc [100%]. It is still correct. Add the link below to the Owners Data Source box on each unit. Keep the links already there.
- `Owner(s)`: `Southern Illinois Power Cooperative Inc [100%]` -> `Southern Illinois Power Cooperative Inc [100%]`
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The EIA-860M table for August 2026 names Southern Illinois Power Coop as the entity for plant 976. This matches GEM's owner. The table does not give a share, so the share is not independently shown.

### Elwood Energy power station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Dairyland Power Cooperative (owner); lookup: Found. The name appears on 10 units in the United States. Reuse the existing entity.

### Elwood Energy power station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Hull Street Energy (owner); lookup: Not found in local data. A bare lookup gave nothing. The entity system was not checked.

### Elwood Energy power station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: MPH Elwood (owner); lookup: Not found in local data. A bare lookup gave nothing. The entity system was not checked.

### G100000402256 / Elwood Energy power station / GT1
*question about existing data; checklist rows 19 (Missing or unknown owner searched)*
- about: Owner(s)
- recommendation: Decide the owner of units 1 to 4 and 8 and 9.
  - links: https://www.utilitydive.com/news/pjm-market-monitor-hull-street-rockland-data-centers/818520/ (ok=None, contains_value=None)
- notes: EIA lists the owner of plant 69979 as MPH Elwood, LLC. Utility Dive says Hull Street Energy owns the Elwood plant. I could not find a dated closing document from two publishers, so I did not report a change. The name MPH Elwood is not in the entity data, and Hull Street Energy is not either, so a new owner entry would be needed.

### G100000402197 / Grand Tower energy center / CC01
*question about existing data; checklist rows 19 (Missing or unknown owner searched)*
- about: attribution
- recommendation: Perdomo Worldwide now owns the site according to the Daily Egyptian. Please check the sale record.
  - links: https://dailyegyptian.com/123274/uncategorized/grand-tower-power-plant-under-redevelopment-many-expect-it-to-become-a-data-center/ (ok=None, contains_value=None)
- notes: Mainline Generation LLC is still the owner in the EIA table.

### Joliet 29 Generating Station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Midwest Generation EME LLC (owner); lookup: Entity midwest generation eme llc appears on 18 units in the United States. Reuse the existing entity.

### Joliet 9 Generating Station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Midwest Generation EME LLC (owner); lookup: Not run. The owner is unchanged from GEM's current value.

### Lee energy facility
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Hull Street Energy (owner); lookup: Local lookup found nothing. The query against the entity system found that Hull Street Energy exists with 2 matches. Reuse the existing entity.

### G100000402277 / Lee energy facility / CT1
*question about existing data; checklist rows 19 (Missing or unknown owner searched), 43 (Ownership changes for operating units reviewed (optional))*
- about: Owner(s)
- recommendation: The sale appears to have closed, so the owner likely needs to change from Rockland Capital to Hull Street Energy. Please confirm the exact company that holds the plant before changing it.
  - links: https://www.powermag.com/hull-street-acquires-two-pjm-based-power-stations-from-rockland-capital/ (ok=None, contains_value=None)
  - links: https://www.energymonitor.ai/news/hull-street-energy-acquires-plants-pjm/ (ok=None, contains_value=None)
- notes: A POWER magazine article says Hull Street Energy announced on August 26, 2026 that it had completed the purchase of the Lee County Generating Station from Rockland Capital. An Energy Monitor article from August 27, 2026 says the same. Both appear to rest on one Hull Street press release, so I count them as one source. Neither names the specific company that holds the plant, only Hull Street Energy and its managed funds. The PJM deactivation notices page was checked and has no notice for this plant. The one Lee entry there is Lee DeKalb, a different plant.

### G100000403820 / Lincoln Land energy center / GEN1
*question about existing data; checklist rows 19 (Missing or unknown owner searched)*
- about: attribution
- recommendation: Please check who holds the project. The article says Kindle Energy is the owner and developer, but development control has moved back to EmberClear.
  - links: https://www.springfieldbusinessjournal.com/news/data-center-development-linked-to-power-plant-construction/ (ok=None, contains_value=None)
- notes: GEM shows Lincoln Land Energy Center LLC as the owner. I did not find a closed sale document. The owner does not change.

### Marion Plant
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Southern Illinois Power Cooperative (owner); lookup: Existing owner already in GEM; no new entity needed.

### Zion energy center
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Zion Energy LLC (owner); lookup: Entity zion energy llc appears on 3 units in the United States. Reuse the existing entity.

### Zion energy center
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Constellation Energy Generation LLC (parent); lookup: Local lookup found nothing for Constellation Energy or Constellation Energy Generation. Not checked against the entity system with the database option.

### G100000403786 / Zion energy center / CTG1
*question about existing data; checklist rows 19 (Missing or unknown owner searched), 43 (Ownership changes for operating units reviewed (optional))*
- about: Owner(s)
- recommendation: Keep Zion Energy LLC as owner at 100 percent. Consider adding Constellation Energy Generation LLC as the parent.
  - links: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/zion-ct1-ct2-ct3-deactivation-notice.pdf (ok=None, contains_value=None)
- notes: Constellation's June 2026 letter to PJM says Constellation Energy Generation, LLC is the upstream owner of Zion Energy LLC, which owns and operates the plant. The EIA table for August 2026 still lists Zion Energy LLC as the owner. So the owning entity did not change. Only the parent changed after the Calpine purchase closed on January 7, 2026. The parent is a computed field, so I did not report it as a value. The entity lookup found no entity named Constellation Energy or Constellation Energy Generation in the local export, so the parent entity may need to be checked in the entity system.

## Checklist group 7. IDs, IRPs and data centers

United States only: EIA and other IDs, utility resource plans, gas-fired data centers.

### G100000402256 / Elwood Energy power station / GT1
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Set Status Detail of unit GT1 (G100000402256) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Elwood Energy told PJM in May 2024 that it would retire all nine units by June 1, 2025, and in March 2025 asked to extend that to June 1, 2026. Hull Street Energy agreed to buy units 1 to 4, 8 and 9 in 2025. The EIA-860M table for August 2026 lists this unit as retired in June 2026.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf
- `Status Detail`: `` -> `Elwood Energy told PJM in May 2024 that it would retire all nine units by June 1, 2025, and in March 2025 asked to extend that to June 1, 2026. Hull Street Energy agreed to buy units 1 to 4, 8 and 9 in 2025. The EIA-860M table for August 2026 lists this unit as retired in June 2026.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The PJM extension letter from March 2025 asks for a new deactivation date of June 1, 2026 for all nine units. The retirement month comes from the EIA table, which is cited under the status.

### G100000402257 / Elwood Energy power station / GT2
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Set Status Detail of unit GT2 (G100000402257) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Elwood Energy told PJM in May 2024 that it would retire all nine units by June 1, 2025, and in March 2025 asked to extend that to June 1, 2026. Hull Street Energy agreed to buy units 1 to 4, 8 and 9 in 2025. The EIA-860M table for August 2026 lists this unit as retired in June 2026.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf
- `Status Detail`: `` -> `Elwood Energy told PJM in May 2024 that it would retire all nine units by June 1, 2025, and in March 2025 asked to extend that to June 1, 2026. Hull Street Energy agreed to buy units 1 to 4, 8 and 9 in 2025. The EIA-860M table for August 2026 lists this unit as retired in June 2026.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The PJM extension letter from March 2025 asks for a new deactivation date of June 1, 2026 for all nine units. The retirement month comes from the EIA table, which is cited under the status.

### G100000402258 / Elwood Energy power station / GT3
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Set Status Detail of unit GT3 (G100000402258) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Elwood Energy told PJM in May 2024 that it would retire all nine units by June 1, 2025, and in March 2025 asked to extend that to June 1, 2026. Hull Street Energy agreed to buy units 1 to 4, 8 and 9 in 2025. The EIA-860M table for August 2026 lists this unit as retired in May 2026.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf
- `Status Detail`: `` -> `Elwood Energy told PJM in May 2024 that it would retire all nine units by June 1, 2025, and in March 2025 asked to extend that to June 1, 2026. Hull Street Energy agreed to buy units 1 to 4, 8 and 9 in 2025. The EIA-860M table for August 2026 lists this unit as retired in May 2026.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The PJM extension letter from March 2025 asks for a new deactivation date of June 1, 2026 for all nine units. The retirement month comes from the EIA table, which is cited under the status.

### G100000402259 / Elwood Energy power station / GT4
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Set Status Detail of unit GT4 (G100000402259) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Elwood Energy told PJM in May 2024 that it would retire all nine units by June 1, 2025, and in March 2025 asked to extend that to June 1, 2026. Hull Street Energy agreed to buy units 1 to 4, 8 and 9 in 2025. The EIA-860M table for August 2026 lists this unit as retired in May 2026.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf
- `Status Detail`: `` -> `Elwood Energy told PJM in May 2024 that it would retire all nine units by June 1, 2025, and in March 2025 asked to extend that to June 1, 2026. Hull Street Energy agreed to buy units 1 to 4, 8 and 9 in 2025. The EIA-860M table for August 2026 lists this unit as retired in May 2026.

https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf`
  - Status Detail: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/elwood-deactivation-extension.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The PJM extension letter from March 2025 asks for a new deactivation date of June 1, 2026 for all nine units. The retirement month comes from the EIA table, which is cited under the status.

### G100000402197 / Grand Tower energy center / CC01
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 50 (Other last-minute status changes checked)*
**Action:** Set Status of unit CC01 (G100000402197) to retired. It now says mothballed. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `mothballed` -> `retired`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://dailyegyptian.com/123274/uncategorized/grand-tower-power-plant-under-redevelopment-many-expect-it-to-become-a-data-center/ (ok=True, contains_value=True)
- confidence: medium (independent: True)
- notes: The EIA-860M table for August 2026 lists plant 862, generators 1 and 3, as retired in April 2024. The Daily Egyptian says the plant ceased operations in February 2021, was sold to Perdomo Worldwide and is being demolished. A SIL News article also reports the shutdown. The two sources agree the plant is gone, but only EIA gives the 2024 date. Status looks retired, not mothballed. The plant stopped in February 2021 after mechanical failures and is now being demolished. EIA says retired April 2024.

### G100000402197 / Grand Tower energy center / CC01
*change to an existing unit; checklist rows 21 (Planned retirements searched), 22 (Retired units have a retired year), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Set Retired year of unit CC01 (G100000402197) to 2024. The box is empty now. Add the link below to the Retired Year Data Source box. Keep the links already there.
- `Retired year`: `` -> `2024`
  - Retired Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Only the EIA-860M table for August 2026 gives the year. It lists retirement in April 2024 for generators 1 and 3.

### G100000402197 / Grand Tower energy center / CC01
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Set Status Detail of unit CC01 (G100000402197) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

The Daily Egyptian reports that the plant ceased operations in February 2021 and that Perdomo Worldwide bought the site from Rockland Capital and is demolishing structures for redevelopment. The EIA-860M table for August 2026 lists the generators as retired in April 2024.

https://dailyegyptian.com/123274/uncategorized/grand-tower-power-plant-under-redevelopment-many-expect-it-to-become-a-data-center/
- `Status Detail`: `` -> `The Daily Egyptian reports that the plant ceased operations in February 2021 and that Perdomo Worldwide bought the site from Rockland Capital and is demolishing structures for redevelopment. The EIA-860M table for August 2026 lists the generators as retired in April 2024.

https://dailyegyptian.com/123274/uncategorized/grand-tower-power-plant-under-redevelopment-many-expect-it-to-become-a-data-center/`
  - Status Detail: https://dailyegyptian.com/123274/uncategorized/grand-tower-power-plant-under-redevelopment-many-expect-it-to-become-a-data-center/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The article names the plant and says operations ceased in February 2021 and demolition is under way.

### G100000402198 / Grand Tower energy center / CC02
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 50 (Other last-minute status changes checked)*
**Action:** Set Status of unit CC02 (G100000402198) to retired. It now says mothballed. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `mothballed` -> `retired`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://dailyegyptian.com/123274/uncategorized/grand-tower-power-plant-under-redevelopment-many-expect-it-to-become-a-data-center/ (ok=True, contains_value=True)
- confidence: medium (independent: True)
- notes: The EIA-860M table for August 2026 lists plant 862, generators 2 and 4, as retired in April 2024. The Daily Egyptian says the plant ceased operations in February 2021, was sold to Perdomo Worldwide and is being demolished. A SIL News article also reports the shutdown. The two sources agree the plant is gone, but only EIA gives the 2024 date. Status looks retired, not mothballed. The plant stopped in February 2021 after mechanical failures and is now being demolished. EIA says retired April 2024.

### G100000402198 / Grand Tower energy center / CC02
*change to an existing unit; checklist rows 21 (Planned retirements searched), 22 (Retired units have a retired year), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Set Retired year of unit CC02 (G100000402198) to 2024. The box is empty now. Add the link below to the Retired Year Data Source box. Keep the links already there.
- `Retired year`: `` -> `2024`
  - Retired Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Only the EIA-860M table for August 2026 gives the year. It lists retirement in April 2024 for generators 2 and 4.

### G100000402198 / Grand Tower energy center / CC02
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Set Status Detail of unit CC02 (G100000402198) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

The Daily Egyptian reports that the plant ceased operations in February 2021 and that Perdomo Worldwide bought the site from Rockland Capital and is demolishing structures for redevelopment. The EIA-860M table for August 2026 lists the generators as retired in April 2024.

https://dailyegyptian.com/123274/uncategorized/grand-tower-power-plant-under-redevelopment-many-expect-it-to-become-a-data-center/
- `Status Detail`: `` -> `The Daily Egyptian reports that the plant ceased operations in February 2021 and that Perdomo Worldwide bought the site from Rockland Capital and is demolishing structures for redevelopment. The EIA-860M table for August 2026 lists the generators as retired in April 2024.

https://dailyegyptian.com/123274/uncategorized/grand-tower-power-plant-under-redevelopment-many-expect-it-to-become-a-data-center/`
  - Status Detail: https://dailyegyptian.com/123274/uncategorized/grand-tower-power-plant-under-redevelopment-many-expect-it-to-become-a-data-center/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The article names the plant and says operations ceased in February 2021 and demolition is under way.

### G100000403513 / Marion Plant / 5
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 50 (Other last-minute status changes checked)*
**Action:** Set Status of unit 5 (G100000403513) to operating. It now says mothballed. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `mothballed` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The EIA-860M table for August 2026 lists generator 5 at the Marion plant, plant code 976, as operating, 75.0 MW, natural gas fired combustion turbine, operating since May 2003. The EIA-923 annual file for 2024 also shows gas turbines at Marion generating about 113,000 megawatt-hours on natural gas, so at least one gas unit ran that year. That file could not be run through the checker, so it is not cited. Both are from the same publisher, the Energy Information Administration, so this is a single-source status change. I found no owner statement about a mothball or a restart. The August 2026 EIA table says this unit is operating, which conflicts with GEM's mothballed status. I found no owner or news document that dates the mothballing, so the missing date is not found.

### G100000403514 / Marion Plant / 6
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 50 (Other last-minute status changes checked)*
**Action:** Set Status of unit 6 (G100000403514) to operating. It now says mothballed. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `mothballed` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The EIA-860M table for August 2026 lists generator 6 at the Marion plant, plant code 976, as operating, 75.0 MW, natural gas fired combustion turbine, operating since May 2003. The EIA-923 annual file for 2024 also shows gas turbines at Marion generating about 113,000 megawatt-hours on natural gas, so at least one gas unit ran that year. That file could not be run through the checker, so it is not cited. Both are from the same publisher, the Energy Information Administration, so this is a single-source status change. I found no owner statement about a mothball or a restart. The August 2026 EIA table says this unit is operating, which conflicts with GEM's mothballed status. I found no owner or news document that dates the mothballing, so the missing date is not found.

### G100000402197 / Grand Tower energy center / CC01
*question about existing data; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 50 (Other last-minute status changes checked)*
- about: Status
- recommendation: Please review the change from mothballed to retired. EIA gives April 2024. A second article shows demolition but gives no retirement year.
  - links: https://dailyegyptian.com/123274/uncategorized/grand-tower-power-plant-under-redevelopment-many-expect-it-to-become-a-data-center/ (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: Owner changed to Perdomo Worldwide per the Daily Egyptian. The sale date and closing were not found, so the owner is not changed.

### Hut 8 Illinois Project 4 data center
*watch item, new to the tracker; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
- what to watch: The source gives a data center size of 50 MW and names no gas generation.
- check again by: 2027-03
  - links: https://www.datacenterdynamics.com/en/news/hut-8-announces-four-data-center-projects-totaling-15gw-across-us/ (ok=True, contains_value=True)
- notes: Hut 8 announced four data center sites in Louisiana, Texas and Illinois. A Data Center Dynamics article says the Illinois site, called Project 4, totals 50 MW. The source does not say where in Illinois, and does not say the site will make its own power from gas. The possible-updates sheet row mentions 1.5 GW across Texas and Illinois, but the Illinois share is only 50 MW. Still unknown: town, power source, any gas turbines or engines and their capacity. It stays on the list only to see whether on-site gas is announced. If added later, the captive fields are captive industry use power and captive industry type data center.

### Joliet Technology Center data center campus
*watch item, new to the tracker; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
- what to watch: The campus is approved at 1.8 GW of data center capacity, but no gas power plant is named.
- check again by: 2027-03
  - links: https://www.datacenterdynamics.com/en/news/approval-given-to-20bn-data-center-near-chicago-illinois/ (ok=True, contains_value=True)
- notes: The Joliet city council approved the PowerHouse Data Centers and Hillwood campus in March 2026. A Data Center Dynamics article says it will offer up to 1.8 GW at full buildout, built in four phases, each with its own six-acre substation. The article describes grid substations and names no on-site gas turbines or engines. Still unknown: whether any on-site gas generation will be built, and its capacity. Only a gas plant tied to this campus would be added. If added later, the captive fields are captive industry use power and captive industry type data center.

### Monarch Rock Air data center campus (Rockford)
*watch item, new to the tracker; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
- what to watch: A gas generation plan for this data center is not confirmed by any source I could read, and no capacity, equipment or permit is public.
- check again by: 2027-03
  - links: https://www.rockrivercurrent.com/2026/06/monarch-has-entered-tax-incentive-deal-with-state-for-rockford-data-center-records-request-shows/ (ok=True, contains_value=True)
- notes: Monarch Rock Air, a company tied to Monarch Energy, plans a data center campus on Friday Road in Rockford, Illinois. A Rock River Current article from June 2026, based on state incentive records, says the campus has associated power generation and is a 1,400 megawatt phased data center. That is the size of the data center, not of any power plant. The task list mentions 250 MW of gas engines planned for 2027 from Monarch's own website. I could not confirm that: the Monarch page is built with scripts and showed no text about Illinois or engines, and other articles describe ComEd grid supply. Still unknown: fuel, number of engines, generating capacity and air permit. Check for an Illinois air permit application. If added later, the captive fields are captive industry use power and captive industry type data center.

### Nelson energy center
*watch item at an existing plant; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
- what to watch: Only a queue listing on a data aggregator shows a possible 391 MW gas addition. No owner, permit or construction step is found.
- check again by: 2027-03
  - links: https://www.infrasure.ai/project/pjm-ah1-718-moved-to-tc2-nelson-345-kv (ok=True, contains_value=True)
- notes: A listing on the Infrasure project site shows an active PJM queue request, entered in April 2025, for 391 MW of gas generation at the Nelson 345 kV point in Lee County, Illinois. The Nelson energy center near Rock Falls is already in GEM as operating. I do not know if this is a new unit, an uprate or a different site at the same connection point. I could not find an owner statement or an air permit. This is not a data center item. Check the PJM queue and the Illinois air permit list again.

### G100000409601 / Tate & Lyle Decatur cogeneration power station / GEN1
*question about existing data; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
- about: Start year
- recommendation: Decide whether 2021 is kept as the year the unit began running on gas, or changed to 1989 to match the EIA table.
  - links: https://www.tateandlyle.com/news/tate-lyle-delivers-its-commitment-eliminate-use-coal-all-its-operations (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: The August 2026 EIA-860M table gives operating year 1989 for generator GEN1. The Tate and Lyle press release from November 2021 gives October 2021 as the end of coal at the plant. GEM's 2021 matches the fuel change, not the turbine's first operation.

## Checklist group 8. New to the tracker

New plants and units ready to add, candidates to watch, and the possible-updates rows.

### Fisk Generating Station / CT31-1
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT31-1`
- `Capacity (MW)`: `` -> `32.5`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 311 at the Fisk Street plant (plant code 886) in Cook County, Illinois. It is a 32.5 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT31, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 49.1 MW for Fisk CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 65 MW.

### Fisk Generating Station / CT31-2
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT31-2`
- `Capacity (MW)`: `` -> `32.5`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 312 at the Fisk Street plant (plant code 886) in Cook County, Illinois. It is a 32.5 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT31, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 49.1 MW for Fisk CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 65 MW.

### Fisk Generating Station / CT32-1
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT32-1`
- `Capacity (MW)`: `` -> `32.5`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 321 at the Fisk Street plant (plant code 886) in Cook County, Illinois. It is a 32.5 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT32, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 49.1 MW for Fisk CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 65 MW.

### Fisk Generating Station / CT32-2
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT32-2`
- `Capacity (MW)`: `` -> `32.5`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 322 at the Fisk Street plant (plant code 886) in Cook County, Illinois. It is a 32.5 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT32, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 49.1 MW for Fisk CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 65 MW.

### Fisk Generating Station / CT33-1
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT33-1`
- `Capacity (MW)`: `` -> `32.5`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 331 at the Fisk Street plant (plant code 886) in Cook County, Illinois. It is a 32.5 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT33, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 49.1 MW for Fisk CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 65 MW.

### Fisk Generating Station / CT33-2
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT33-2`
- `Capacity (MW)`: `` -> `32.5`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 332 at the Fisk Street plant (plant code 886) in Cook County, Illinois. It is a 32.5 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT33, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 49.1 MW for Fisk CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 65 MW.

### Fisk Generating Station / CT34-1
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT34-1`
- `Capacity (MW)`: `` -> `32.5`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `mothballed`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 341 at the Fisk Street plant (plant code 886) in Cook County, Illinois. It is a 32.5 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT34, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. EIA lists this generator as out of service and not expected to return next year, which is why the status is mothballed. PJM's capacity figure for CT34 is 22.9 MW, close to the other half only, so this half looks idle. A reviewer should confirm before setting mothballed. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 49.1 MW for Fisk CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 65 MW.

### Fisk Generating Station / CT34-2
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT34-2`
- `Capacity (MW)`: `` -> `32.5`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 342 at the Fisk Street plant (plant code 886) in Cook County, Illinois. It is a 32.5 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT34, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 49.1 MW for Fisk CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 65 MW.

### Waukegan Generating Station / CT31-1
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT31-1`
- `Capacity (MW)`: `` -> `28`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 311 at the Waukegan plant (plant code 883) in Lake County, Illinois. It is a 28 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT31, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. EIA lists the Waukegan units as standby, available for service but not normally used. They are kept as operating. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 52.5 MW for Waukegan CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 56 MW.

### Waukegan Generating Station / CT31-2
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT31-2`
- `Capacity (MW)`: `` -> `28`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 312 at the Waukegan plant (plant code 883) in Lake County, Illinois. It is a 28 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT31, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. EIA lists the Waukegan units as standby, available for service but not normally used. They are kept as operating. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 52.5 MW for Waukegan CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 56 MW.

### Waukegan Generating Station / CT32-1
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT32-1`
- `Capacity (MW)`: `` -> `28`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 321 at the Waukegan plant (plant code 883) in Lake County, Illinois. It is a 28 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT32, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. EIA lists the Waukegan units as standby, available for service but not normally used. They are kept as operating. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 52.5 MW for Waukegan CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 56 MW.

### Waukegan Generating Station / CT32-2
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `CT32-2`
- `Capacity (MW)`: `` -> `28`
- `Fuel`: `` -> `fossil liquids: fuel oil`
- `Status`: `` -> `operating`
- `Start year`: `` -> `1968`
- `Owner(s)`: `` -> `Midwest Generation EME LLC [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.pjm.com/-/media/DotCom/planning/gen-retire/deactivation-notices/mwg-withdrawal-letter.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Unit name Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIA-860M table for August 2026, Operating sheet, lists generator 322 at the Waukegan plant (plant code 883) in Lake County, Illinois. It is a 28 MW nameplate gas turbine burning distillate fuel oil, in service since 1968, owned by Midwest Generation. PJM's letters call the unit it belongs to CT32, which is made of two generators. GEM has only the retired coal units at this site, so this oil peaker is missing. EIA lists the Waukegan units as standby, available for service but not normally used. They are kept as operating. Midwest Generation told PJM on February 3, 2025 that it withdrew its earlier retirement notice, and again on July 2, 2026 that it agreed to PJM's request to keep the units running until May 31, 2031. No planned retirement year is proposed, because that date is a reliability extension and not a retirement notice. The owner's figures to PJM, such as 52.5 MW for Waukegan CT31, cover both generators of the unit together and look like net capacity, so they are lower than the EIA nameplate total of 56 MW.

### G100001017949 / Joliet 29 Generating Station / Unit 8, timepoint 2
*question about existing data*
- about: identity
- recommendation: Add EIA generator id 8 for Unit 8 and 7 for Unit 7 in Other IDs.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: See the question on Unit 7. The two units map to generators 7 and 8.

### G100001017847 / Joliet 9 Generating Station / Unit 6, timepoint 2
*question about existing data; checklist rows 51 (Newly announced projects checked)*
- about: existence
- recommendation: Check whether the old Joliet 9 gas combustion turbines are in GEM.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx (ok=None, contains_value=None)
- notes: EIA also lists eight small gas combustion turbines of 18.4 MW each at this plant, generators 311 to 314 and 321 to 324, retired in December 2004. That is before the 2020 cutoff, so no new unit is proposed.

### G100000401832 / Nelson energy center / BLK1
*watch item at an existing plant; checklist rows 51 (Newly announced projects checked)*
- what to watch: A 38 MW uprate for 2028 is reported on an existing plant, which is not a new or replacement unit, so it is not an edit.
- check again by: 2027-03
- notes: I could not find the 2026 PJM addendum that the possible-updates sheet describes. The PJM queue file lists Nelson projects only as in service: a 600 MW project in service since May 2015, two 157 MW projects in service since May 2023, and a 24.4 MW project in service since May 2023. A web search also found nothing on a 38 MW uprate. Capacity is left unchanged.

## Checklist group 9. Close-out

Not record-level: the sheet and doc updates, research status, and the two database checks. These boxes are ticked by hand after the edits are applied: validation_report.py --closeout must print CLOSE-OUT CLEAN (row 54) and no_tracker.py lists the units with no tracker (row 56).
