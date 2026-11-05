# Evidence — gogpt batch 20261105_1422_ET (us-ok, update)

Each section below is one group of the GOGPT QC/Country checklist. The records in it are the evidence for ticking that group's boxes; the row numbers are the checklist tab's own.

## Utility resource plans (checklist row 37)

The IRP step read 1 utility row of the US IRPs tab for this state. The records below come from a plan; the actions workbook's irp_box sheet says which units need the IRP box ticked, and its irp_notes_draft sheet has a draft line per utility for the tab's Notes column.

- OG&E: 2024 IRP, 2025 Draft IRP Update (a draft). Tracked plants matched: 8

Records from a plan:
- G100000403305 / Horseshoe Lake power station / 10: change to an existing unit, from the OG&E plan
- G100001092969 / Horseshoe Lake power station / 13: change to an existing unit, from the OG&E plan
- G100001092970 / Horseshoe Lake power station / 14: change to an existing unit, from the OG&E plan
- G100000403307 / Horseshoe Lake power station / 8: change to an existing unit, from the OG&E plan
- G100000403308 / Horseshoe Lake power station / 9: change to an existing unit, from the OG&E plan
- Northeastern power station / Unit 5 and Unit 6: question about existing data
- Comanche (OK) power station / CC1: question about existing data
- Southwestern power station: question about existing data
- Tulsa power station: question about existing data
- Riverside (OK) power station: question about existing data
- Northeastern power station: question about existing data
- Public Service Company of Oklahoma 2026 all-source request for proposals: watch item, new to the tracker
- OG&E 2026 requests for proposals: watch item, new to the tracker

## Checklist group 1. Validation report

Edits and questions that fix an error from the GEM validation report.

### G100001017849 / Muskogee Generating Station / Unit 4, timepoint 2
*change to an existing unit; checklist rows 7 (Validation report errors fixed), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of all 2 units of Muskogee Generating Station as Oklahoma Gas and Electric Co [100%]. It is still correct. Add the link below to the Owners Data Source box on each unit. Keep the links already there.
- `Owner(s)`: `Oklahoma Gas and Electric Co [100%]` -> `Oklahoma Gas and Electric Co [100%]`
  - Owners Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Oklahoma Department of Environmental Quality permit memo from November 2021 at https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf names Oklahoma Gas & Electric Company as the permit holder for the Muskogee Generating Station. It states no ownership share, so 100 percent is implied.

### G100001017849 / Muskogee Generating Station / Unit 4, timepoint 2
*change to an existing unit; checklist rows 7 (Validation report errors fixed), 25 (Location data for every entry), 42 (Exact location for approximate operating units (optional))*
**Action:** Leave the point of all 2 units of Muskogee Generating Station as it is. Add the 2 links below to the Location Data Source box on each unit. Keep the links already there.
- `Latitude`: `35.7619220` -> `35.7619220`
- `Longitude`: `-95.2878780` -> `-95.2878780`
- `Location accuracy`: `exact` -> `exact`
- location now: 35.7619220, -95.2878780 (exact) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=35.76192,-95.28788&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=35.76192,-95.28788)
- location proposed: 35.7619220, -95.2878780 (exact) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=35.76192,-95.28788&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=35.76192,-95.28788)
  - Location Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf (ok=True, contains_value=True)
  - Location Data Source: https://www.google.com/maps/search/?api=1&query=35.76192,-95.28788 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The same permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf gives the site as latitude 35.76054 north and longitude 95.28731 west. That is about 160 meters from GEM's point, so GEM's value stands. The permit memo gives longitude 95.28731 west, about 160 meters from GEM's point. GEM's value stands. Coordinates are published in a permit document, which makes the point exact.

### G100000401629 / Grand River Energy Center / 3
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- question: Which older unit did unit 3 replace?
- finding: A Black and Veatch project page (https://www.bv.com/projects/power-plant-replacement-project-brings-price-certainties-cleaner-air) names the project Grand River Energy Center Units 2 and 3, which suggests the combined cycle replaced older unit 2. The EIA-860M table for September 2026 still lists a coal unit 2 as operating at 594 MW.
- recommendation: Find the GEM unit ID of the coal unit 2 at this plant and, if it exists, put it in the replacement link for unit 3. If no unit 2 record exists, ask the project manager whether to add one.
  - links: https://www.bv.com/projects/power-plant-replacement-project-brings-price-certainties-cleaner-air (ok=None, contains_value=None)
- notes: I could not read the GEM unit ID for unit 2 from the brief. I did not find a document that says plainly which unit unit 3 replaced.

### G100000403306 / Horseshoe Lake power station / 6
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- question: Where do units 6 and ST7 stand in GEM, and what is their source?
- finding: Both are retired in GEM with 2024 retirement years. The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists unit 6 retired January 2024 and ST7 retired December 2024.
- recommendation: Leave both as retired, and use the EIA-860M table as the source of the retirement year.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: The September 2024 notes in the status detail say to be retired and were not changed.

### G100001017849 / Muskogee Generating Station / Unit 4, timepoint 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- question: Does a document state that Muskogee units 4 and 5 have no carbon capture?
- finding: No document I read mentions carbon capture at units 4 or 5. The permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf lists activated carbon handling for Unit 6 mercury control, which is not carbon capture.
- recommendation: Leave CCS attachment as no. No source was found, so the validation item stays open for a person to dismiss.
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf (ok=None, contains_value=None)
- notes: Looked at the permit memos from 2018 and 2021 and the harvested permit file for this plant. Not found.

### G100001017849 / Muskogee Generating Station / Unit 4, timepoint 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- question: What document supports Owner and Location for Muskogee Generating Station?
- finding: The permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf names Oklahoma Gas & Electric Company as the permit holder and gives coordinates 35.76054, -95.28731. GEM's point is about 160 meters away.
- recommendation: Use the permit memo as the Owner and Location source. Keep GEM's values.
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf (ok=None, contains_value=None)
- notes: The Southwest Power Pool open queue list read on 5 November 2026 (https://opsportal.spp.org/Studies/GenerateActiveCSV) shows GEN-2025-SR9 at 400 MW, owned by OG&E, with no fuel shown, at the Muskogee 345 kV substation, with commercial operation in December 2029. It is added in this batch as a new unit at this plant. GEN-2024-293 is 248 MW of gas at the same substation name, with commercial operation in May 2033. No document ties it to this plant, so it is added as its own project.

### G100001055294 / Northeastern Station / Unit 3, timepoint 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- question: Is the SPP queue entry ERAS-2025-023 a separate project from Units 5 and 6?
- finding: The 513 MW queue entry is one turbine with commercial operation in December 2029, a year after the two 229 MW turbines of Units 5 and 6. The queue list names no developer, and no document I found ties it to either project.
- recommendation: Add no new unit now. Check the Southwest Power Pool list again in the next monthly update and the Oklahoma Corporation Commission docket for a third Northeastern turbine.
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AWtoGCCMAPa3ZmzV9bv2lNVdjzgKUd4GV4oRCuMNP0goK6NykmHJHyG5WSO1mUZe7mM1J5HwOpKpJWodbQLKNmw%3D/?ViewerMode=PDF&ForceDownload=true (ok=None, contains_value=None)
  - links: https://www.sec.gov/Archives/edgar/data/4904/000000490426000059/aep-20260630.htm (ok=None, contains_value=None)
- notes: An Oklahoma Department of Environmental Quality permit file for Northeastern also describes a separate 453 MW turbine (https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AS0IjaCrV1T%C3%81SEUDdXmwkZpG2VRBClzAKR911pep%C3%81uAtGhYCcgV7UJnH1xPqDg4ZbOaSJTShXSL302lcWYvl9ds%3D/?ViewerMode=PDF&ForceDownload=true). The entry may be that turbine or a later one. I could not tell which from a document.

## Checklist group 2. Blanks and unknowns

Empty or unknown cells that the research filled, and the ones it could not.

### G100000401815 / Green Country Energy power station / G841
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit G841 (G100000401815) as 301.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `301.0` -> `301.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 gives CTG1 at 179.3 MW and STG1 at 122.0 MW, which sum to 301.3 MW. GEM shows 301.0 MW. The difference is rounding, so no change is proposed.

### G100000401816 / Green Country Energy power station / G842
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit G842 (G100000401816) as 301.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `301.0` -> `301.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 gives CTG2 at 179.3 MW and STG2 at 122.0 MW, which sum to 301.3 MW. GEM shows 301.0 MW. The difference is rounding, so no change is proposed.

### G100000401817 / Green Country Energy power station / G843
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit G843 (G100000401817) as 301.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `301.0` -> `301.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 gives CTG3 at 179.3 MW and STG3 at 122.0 MW, which sum to 301.3 MW. GEM shows 301.0 MW. The difference is rounding, so no change is proposed.

### G100000401944 / Kiamichi energy facility / STG1
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit STG1 (G100000401944) as 685.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `685.0` -> `685.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 gives two turbines of 183.9 MW and a steam turbine of 317.2 MW, which sum to 685.0 MW. This matches GEM.

### G100000401945 / Kiamichi energy facility / STG2
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit STG2 (G100000401945) as 685.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `685.0` -> `685.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 gives two turbines of 183.9 MW and a steam turbine of 317.2 MW, which sum to 685.0 MW. This matches GEM.

### G100001091053 / Muskogee Data Center power station / 1
*change to an existing unit*
**Action:** Leave Fuel of unit 1 (G100001091053) as fossil liquids: diesel. It is still correct. Add the link below to the Fuel Data Source box. Keep the links already there.
- `Fuel`: `fossil liquids: diesel` -> `fossil liquids: diesel`
  - Fuel Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ae6Ctfv7oSCmhMZ%C3%89kDp%C3%89JKeyyrF%C3%897NeqHWN6Fd0wYTdl604KTTG6bsIhnFC9Sgq7vhd656jR%C3%895uQBkEpWYOBnMg%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft permit says all engines burn diesel.

### G100001093027 / ONE Nuclear power station 1 / 1
*change to an existing unit*
**Action:** Leave Fuel of unit 1 (G100001093027) as fossil gas: natural gas. It is still correct. Add the link below to the Fuel Data Source box. Keep the links already there.
- `Fuel`: `fossil gas: natural gas` -> `fossil gas: natural gas`
  - Fuel Data Source: https://www.sec.gov/Archives/edgar/data/1846416/000149315225019001/ex99-1.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The ONE Nuclear press release filed with the Securities and Exchange Commission in October 2025 (https://www.sec.gov/Archives/edgar/data/1846416/000149315225019001/ex99-1.htm) describes gas generation at its first two sites, one in Oklahoma. The company's plan is gas first, with nuclear later. So the fuel is gas, not nuclear. I found no address, county, permit or queue entry for this site. The filing only says Oklahoma. The 2028 date is a company goal, and GEM already shows 2028.

### G100001028184 / Ripley Energy Center power station / RP1
*change to an existing unit*
**Action:** Leave Fuel of unit RP1 (G100001028184) as fossil gas: natural gas, fossil liquids: diesel. It is still correct. Add the link below to the Fuel Data Source box. Keep the links already there.
- `Fuel`: `fossil gas: natural gas, fossil liquids: diesel` -> `fossil gas: natural gas, fossil liquids: diesel`
  - Fuel Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8877.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: This is a replacement source for the Associated Electric Cooperative page that no longer opens. The permit memorandum (https://applications.deq.ok.gov/permitspublic/storedpermits/8877.pdf) says the turbine burns pipeline natural gas, with distillate fuel oil as backup in emergencies. The value is left as it stands.

### G100000402873 / Spring Creek energy center / CT01
*change to an existing unit*
**Action:** Set Capacity (MW) of unit CT01 (G100000402873) to 86.5. It now says 85.0. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `85.0` -> `86.5`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) gives a nameplate capacity of 86.5 MW for generator CT01. GEM shows a different figure.

### G100000402874 / Spring Creek energy center / CT02
*change to an existing unit*
**Action:** Set Capacity (MW) of unit CT02 (G100000402874) to 86.5. It now says 85.0. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `85.0` -> `86.5`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) gives a nameplate capacity of 86.5 MW for generator CT02. GEM shows a different figure.

### G100000402875 / Spring Creek energy center / CT03
*change to an existing unit*
**Action:** Set Capacity (MW) of unit CT03 (G100000402875) to 86.5. It now says 85.0. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `85.0` -> `86.5`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) gives a nameplate capacity of 86.5 MW for generator CT03. GEM shows a different figure.

### G100000402876 / Spring Creek energy center / CT04
*change to an existing unit*
**Action:** Set Capacity (MW) of unit CT04 (G100000402876) to 86.5. It now says 85.0. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `85.0` -> `86.5`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) gives a nameplate capacity of 86.5 MW for generator CT04. GEM shows a different figure.

### G100000414190 / Stillwater Energy Center / IC
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit IC (G100000414190) as 56.4. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `56.4` -> `56.4`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) gives 3 engines of 18.8 MW, a total of 56.4 MW, which matches GEM.

### G100001072817 / Tinker Air Force Base power station / 1-2
*change to an existing unit*
**Action:** Leave Capacity Per Engine of unit 1-2 (G100001072817) as 48.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `48.0` -> `48.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists Tinker plant 63628, generators 1 and 2, as operating, 48.1 MW each, natural gas combustion turbines, operating since March 2026.

### G100000403433 / Tulsa power station / 2
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 2 (G100000403433) as 170.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `170.0` -> `170.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Nameplate is 170.0 MW in the EIA table.

### G100000403434 / Tulsa power station / 4
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 4 (G100000403434) as 170.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `170.0` -> `170.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Nameplate is 170.0 MW in the EIA table.

### G100001101631 / Bristow Energy Center / 1
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Is GEM's point for Bristow close to the site Associated describes?
- finding: The Associated page at https://www.aeci.org/bristow-energy-center-1 puts the plant about 2 miles southeast of Bristow. GEM's point at 35.81000, -96.36600 is consistent with that. No address, parcel or coordinates were found.
- recommendation: Leave the point and the approximate accuracy as they are.
  - links: https://www.aeci.org/bristow-energy-center-1 (ok=None, contains_value=None)
- notes: No imagery check was done because no document gave a more exact place. An air permit application would give coordinates.

### G100001101676 / Citadel Facility Data Center power station / 1
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Which point is the Citadel data center site, GEM's or the permit's?
- finding: The Oklahoma Department of Environmental Quality permit memo at https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf gives latitude 36.27133 and longitude -95.90837. The same memo says the site is at North Yale Avenue and East 86th Street North in Sperry, which geocodes to 36.27857, -95.91994, about 100 meters from GEM's point of 36.27924, -95.91897. The permit point is about 1.3 kilometers from GEM's point.
- recommendation: Leave the point and the approximate accuracy as they are. Ask the permit engineer or check a county parcel map for the Yale and 86th Street site before making it exact.
  - links: https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf (ok=None, contains_value=None)
- notes: Satellite images show ground with no data center built at either place, and the imagery date is unknown. The permit directions start from Owasso and fit the permit point better than the street address. Pin links: https://www.google.com/maps/search/?api=1&query=36.27133,-95.90837 and https://www.google.com/maps/search/?api=1&query=36.27924,-95.91897

### Comanche (OK) power station
*question about existing data*
- about: Capacity (MW)
- question: Should Comanche units CC2 and CC3 be 775.2 MW each instead of 686.4 MW?
- finding: The SPP queue lists two combined cycle requests in Lawton, ERAS-2025-024 and ERAS-2025-026, at 775.2 MW nameplate each (744 MW capacity each), with commercial operation on November 30, 2029. GEM carries CC2 and CC3 at 686.4 MW each.
- recommendation: Check the Public Service Company of Oklahoma preapproval order for the unit rating, and if the order says 686.4 MW keep GEM as is and add both SPP numbers to Other IDs.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- notes: The utility helper found the plan figure; the queue figure is the interconnection customer's nameplate and may include duct firing or a different site rating. Both queue rows have fully executed agreements.

### G100001101686 / Comanche (OK) power station / CC2
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- question: Which EIA generator ids belong to Comanche CC2 and CC3?
- finding: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists generators 2G1 at 408.8 MW and 2S1 at 277.6 MW with unit code CC2. It lists generators 3G1 at 408.8 MW and 3S1 at 277.6 MW with unit code CC3. Each pair is a gas turbine plus a steam turbine, so each pair is one combined cycle block.
- recommendation: Treat 2G1 and 2S1 as CC2, and 3G1 and 3S1 as CC3. Type these ids into Other IDs for the unit by hand in the web form.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: EIA's own unit code column names the blocks, so there is no doubt about the pairing. The generators are planned for September 2029 and EIA says regulatory approvals are not initiated, which is out of date because the air permit application was filed in April 2026.

### G100001091022 / Cross Timbers Power Plant / 1
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Should the Cross Timbers point move about 500 meters?
- finding: GEM's point is 34.95195, -96.73905 and is marked exact. The permit memorandum at https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf gives 34.95595, -96.73635 for the facility.
- recommendation: Leave the point as it is. The two points are about 500 meters apart and GEM's is already exact.
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf (ok=None, contains_value=None)
- notes: I did not open a satellite image. The difference is small compared with the size of the site.

### Grand River Energy Center
*question about existing data*
- about: Capacity (MW)
- question: Is unit 4 at Grand River 426 MW as in GEM, or 594 MW as in the federal file?
- finding: GEM gives unit 4 as 426 MW, operating from 2026. The federal file for September 2026 gives 594 MW for generator 4. The Grand River Dam Authority describes the unit as a 426 MW J-class combustion turbine dedicated on September 9.
- recommendation: Keep 426 MW and the operating status. The federal figure of 594 MW is the old coal unit 2 size and looks like a carry-over.
  - links: https://www.publicpower.org/periodical/article/grand-river-dam-authority-formally-dedicates-unit-4-grand-river-energy-center (ok=True, contains_value=True)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- notes: The federal file lists generator 4 as operating since September 2026, so its status agrees with GEM and disagrees with EIP, which lists the plant as under construction. The 2025 annual survey still shows unit 4 as proposed. EIP's page loads only through a script, so the page could not be read as text.

### Horseshoe Lake power station
*question about existing data*
- about: Capacity (MW)
- question: Should Horseshoe Lake units 13 and 14 be 248 MW each instead of 224 MW?
- finding: SPP request ERAS-2025-010 is a 496 MW combustion turbine request at Horseshoe Lake 138 kilovolt with a fully executed agreement and commercial operation on January 1, 2029. GEM has units 13 and 14 at 224 MW each, 448 MW, pre-construction, due 2029. Request GEN-2024-GR1 is also 492 MW for units 11 and 12, which GEM carries at 448 MW.
- recommendation: Look at the OG&E turbine order or an air permit for the rated output, and if it supports 248 MW per unit change units 11 to 14 to match.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- notes: Both pairs are 44 to 48 MW above GEM, so the queue may be reporting a different rating basis than the one GEM used.

### G100001092969 / Horseshoe Lake power station / 13
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- question: Which EIA generator ids belong to units 13 and 14?
- finding: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists generators 13 and 14, each 224 MW, planned February 2029. The earnings call at https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ gives 440 MW for both, which is 220 MW each.
- recommendation: Treat EIA generator 13 as unit 13 and generator 14 as unit 14. Both are 224 MW in EIA and in GEM, so no capacity change.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ (ok=None, contains_value=None)
- notes: OG&E's own figure of 440 MW total is a rounded plant total.

### G100001101619 / Hugo power station / Site A
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Should the City for Hugo be Fort Towson, not Fort Townsend?
- finding: The Rural Utilities Service environmental assessment (https://www.rd.usda.gov/media/file/download/rus-ea-hugo-new-generation.pdf) places the site west of Fort Towson, Oklahoma. The database spells it Fort Townsend.
- recommendation: Change City to Fort Towson for both units. The pin link is https://www.google.com/maps/search/?api=1&query=34.01875,-95.32186.
  - links: https://www.rd.usda.gov/media/file/download/rus-ea-hugo-new-generation.pdf (ok=None, contains_value=None)
- notes: Both units are shown as exact in the database, so the coordinates were not reopened.

### Mooreland power station
*question about existing data*
- about: Capacity (MW)
- question: Should Mooreland unit 1 be added at 45 MW?
- finding: GEM lists units 2 and 3 at 125 and 135 MW. The federal file also lists unit 1 at 45 MW, natural gas steam turbine, from 1964.
- recommendation: Do not add unit 1. It is below the 50 MW unit threshold.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- notes: The plant total in the federal file is 305 MW against GEM's 260 MW. The gap is unit 1.

### Mustang (OK) power station
*question about existing data*
- about: Capacity (MW)
- question: Is Mustang unit 6-12 one block of 462 MW as in GEM, or seven turbines of 66 MW each as in the federal file?
- finding: GEM lists one unit named 6-12 at 462 MW. The federal file lists seven natural gas combustion turbines, GT1 to GT7, each 66 MW, all started in 2017. Seven times 66 is 462 MW.
- recommendation: Keep the total at 462 MW. Consider splitting the unit into seven turbines of 66 MW each.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- notes: The totals agree. Only the way the units are counted differs.

### Northeastern power station
*question about existing data*
- about: Capacity (MW)
- question: Should Northeastern units 5 and 6 be 513 MW in total instead of 450 MW, and start in 2029 instead of 2028?
- finding: SPP request ERAS-2025-023 is a 513 MW combustion turbine request at Northeastern 345 kilovolt with a fully executed agreement and commercial operation on December 15, 2029. GEM has units 5 and 6 at 225 MW each, 450 MW, due 2028.
- recommendation: Keep the two units at 225 MW each, which matches the utility's 450 MW plan figure, add SPP ERAS-2025-023 to Other IDs, and move the start year to 2029 once the start-year question on this plant is settled.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- notes: The 63 MW gap may be the queue nameplate against the plan's net rating. The AEP quarterly report text did not give a unit size. The start year question for 2029 is also raised by the utility plan review.

### G100001093027 / ONE Nuclear power station 1 / 1
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Where is the ONE Nuclear Oklahoma gas site?
- finding: The filing at https://www.sec.gov/Archives/edgar/data/1846416/000149315225019001/ex99-1.htm names Oklahoma only. No ODEQ permit, commission cause or queue entry matched, and the point GEM shows could not be checked.
- recommendation: Leave the point and the blank city as they are. Search again when ONE Nuclear files an air permit or names a county.
  - links: https://www.sec.gov/Archives/edgar/data/1846416/000149315225019001/ex99-1.htm (ok=None, contains_value=None)
- notes: The location ladder found no address, so no imagery was checked.

### G100001101690 / Port of Inola Power Station / 1A
*question about existing data*
- about: source
- question: Is the PSO 2026 resource plan line for Port of Inola still to be found?
- finding: The commission cause search (the daily docket PDFs) and the queue file matched nothing for this plant. The permit application is the only document found for the 2030 start.
- recommendation: Ask the reviewer to check PSO's 2026 resource plan refresh by hand for the Port of Inola line and the Oklahoma Corporation Commission cause number.
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUk7Pfms86Dwy6B9RtySPXY8zCMWK8b6prK%C3%81TES%C3%81ksWrcWp06P8ZaPQ3atfhjmXORD%C3%89mJf1dwQNey9skV%C3%89JMF5I%3D/?ViewerMode=PDF&ForceDownload=true (ok=None, contains_value=None)
- notes: A web search found no news article naming a combined cycle plant at the Port of Inola.

### G100000401931 / Redbud power plant / G112
*question about existing data*
- about: Capacity (MW)
- question: Should each Redbud unit's capacity move from 358 MW to 372.5 MW after the upgrade?
- finding: The permit memorandum (https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf) says each combined cycle unit goes from 317 MW to 372.5 MW. The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) still shows 198.9 MW plus 159.5 MW, or 358.4 MW, per unit.
- recommendation: Leave 358 MW for now. Change all four units to 372.5 MW when EIA or the owner confirms the upgrade is finished.
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: The memorandum describes planned work, so it does not prove the upgrade is done.

### River Valley power station
*question about existing data; checklist rows 16 (Zero-capacity units rechecked)*
- about: Capacity (MW)
- question: Is the 496 MW Southwest Power Pool request GEN-2024-286 the first phase of the five turbine project at River Valley?
- finding: The request is for 496 MW of gas at a 161 kV substation in Le Flore County owned by OG&E. The state permit application is for about 1,124 MW of simple-cycle turbines or 1,280 MW of combined cycle.
- recommendation: Record the permit capacity on the new unit and add a note naming the request as a possible first phase.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Af6FiOuAWfwTfP7%C3%89lBObAZu2%C3%81jK627i0ruRb1YVA9ucGjOJwUUHCsEMbR%C3%81V4w%C3%819YC3Cw0VwM4maTrcJLCxoanak%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- notes: The request lists commercial operation in May 2031. No document ties the two numbers together.

### G100000403319 / Seminole (OK) power station / 1
*question about existing data; checklist rows 26 (City and state or province filled)*
- about: City
- question: Should the city for Seminole (OK) power station read Konawa instead of Konowa?
- finding: The 2026 OG&E integrated resource plan at https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 places the plant in Konawa, Oklahoma. The tracker shows Konowa.
- recommendation: Change City to Konawa on every unit of this plant.
  - links: https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 (ok=None, contains_value=None)
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/8353.pdf (ok=None, contains_value=None)
- notes: An Oklahoma Department of Environmental Quality permit memo for the Seminole Generating Station at https://applications.deq.ok.gov/permitspublic/storedpermits/8353.pdf also gives the facility location as Konawa, Seminole County. Two sources agree on this spelling. I found no document that uses Konowa.

### G100000402873 / Spring Creek energy center / CT01
*question about existing data*
- about: source
- question: Were the Oklahoma resource plans and queue entry GEN-2024-255 checked for Spring Creek?
- finding: I did not open the Evergy resource plan or the Southwest Power Pool entry GEN-2024-255. The brief calls that entry a lead that is not this plant.
- recommendation: Leave the plant as it is. Check the Evergy plan for a retirement year if a person wants it done.
- notes: The 12 fetch budget went to the monthly EIA table only, which covers status and capacity for all four units.

### Tinker Air Force Base power station
*question about existing data*
- about: Capacity (MW)
- question: Should the Tinker units be changed to match the federal file of 48.1 MW each for units 1 and 2 and 41 MW each for 5A and 5B?
- finding: GEM lists units 1 and 2 together at 96 MW, operating 2026, and units 5A and 5B together at 64 MW, retired. The federal file for September 2026 lists plant 63628, Tinker, with units 1 and 2 at 48.1 MW each and units 5A and 5B at 41 MW each, out of service.
- recommendation: Change units 1 and 2 to 96.2 MW in total, and units 5A and 5B to 82 MW in total, after checking the commissioning release. Keep 5A and 5B at retired only if a document says they are retired.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - links: https://www.okenergytoday.com/2026/02/oge-and-tinker-air-force-base-celebrate-new-power-generation (ok=True, contains_value=True)
- notes: A February 2026 story on the OG&E and Tinker Air Force Base celebration confirms the new turbines are running. The federal file still counts 5A and 5B as out of service and not expected to return, which is not the same as retired. The plant point in the federal file is the same as GEM's point.

### G100001072817 / Tinker Air Force Base power station / 1-2
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- question: Is EIA plant 63628 Tinker the same site as this plant?
- finding: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 63628 Tinker in Oklahoma County at the same coordinates as GEM. Generators 1 and 2 (48.1 MW each, operating since March 2026) match unit 1-2. Generators 5A and 5B (41 MW each, out of service, since 1971) match unit 5A-5B.
- recommendation: Type EIA 63628 into Other IDs (location). Type EIA 1 and EIA 2 into Other IDs (unit) for unit 1-2, and EIA 5A and EIA 5B for unit 5A-5B.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: The codes are not added as values.

## Checklist group 3. Status and timeline

Status changes, start and retirement years, planned retirements, Latest Activity.

### G100001055235 / Anadarko power station / Roulet 12
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Leave Status of unit Roulet 12 (G100001055235) as construction. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `construction` -> `construction`
  - Status Data Source: https://www.power-eng.com/gas-turbines/new-ge-vernova-aeroderivative-units-to-expand-capacity-at-oklahoma-gas-plant/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Power Engineering article (https://www.power-eng.com/gas-turbines/new-ge-vernova-aeroderivative-units-to-expand-capacity-at-oklahoma-gas-plant/) says work was expected to start in late 2024 and finish in late 2026. An Oklahoma Energy Today article from October 2024 (https://www.okenergytoday.com/2024/10/groundbreaking-for-expansion-of-western-farmers-electric-generating-plant-in-anadarko/) reports the groundbreaking. I found no newer report of completion, so status stays construction. Still under construction with completion expected in late 2026. The EIA September 2026 table does not list this unit under Oklahoma planned units. I found no stated Backup Power value, and no dated start of operation, so start year is left as it is.

### G100001055235 / Anadarko power station / Roulet 12
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Leave Capacity (MW) of unit Roulet 12 (G100001055235) as 50.2. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `50.2` -> `50.2`
  - Capacity Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8827.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Oklahoma air permit memorandum from October 2024 (https://applications.deq.ok.gov/permitspublic/storedpermits/8827.pdf) gives gross generation of 50,182 kW per turbine, which is 50.2 MW.

### G100001055235 / Anadarko power station / Roulet 12
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units), 49 (Construction to operating checked)*
**Action:** Leave Equipment Manufacturer/Model of unit Roulet 12 (G100001055235) as GE Vernova: LM6000PC-Sprint. It is still correct. Add the 2 links below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `GE Vernova: LM6000PC-Sprint` -> `GE Vernova: LM6000PC-Sprint`
  - Turbine/Engine Equipment Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8827.pdf (ok=True, contains_value=True)
  - Turbine/Engine Equipment Data Source: https://www.power-eng.com/gas-turbines/new-ge-vernova-aeroderivative-units-to-expand-capacity-at-oklahoma-gas-plant/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The same permit memorandum names two LM6000PC-SPRINT turbines for units 12 and 13. The Power Engineering article names GE Vernova as supplier.

### G100001055237 / Anadarko power station / Roulet 13
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Leave Status of unit Roulet 13 (G100001055237) as construction. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `construction` -> `construction`
  - Status Data Source: https://www.power-eng.com/gas-turbines/new-ge-vernova-aeroderivative-units-to-expand-capacity-at-oklahoma-gas-plant/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Power Engineering article (https://www.power-eng.com/gas-turbines/new-ge-vernova-aeroderivative-units-to-expand-capacity-at-oklahoma-gas-plant/) says work was expected to start in late 2024 and finish in late 2026. An Oklahoma Energy Today article from October 2024 (https://www.okenergytoday.com/2024/10/groundbreaking-for-expansion-of-western-farmers-electric-generating-plant-in-anadarko/) reports the groundbreaking. I found no newer report of completion, so status stays construction. Still under construction with completion expected in late 2026. The EIA September 2026 table does not list this unit under Oklahoma planned units. I found no stated Backup Power value, and no dated start of operation, so start year is left as it is.

### G100001055237 / Anadarko power station / Roulet 13
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Leave Capacity (MW) of unit Roulet 13 (G100001055237) as 50.2. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `50.2` -> `50.2`
  - Capacity Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8827.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Oklahoma air permit memorandum from October 2024 (https://applications.deq.ok.gov/permitspublic/storedpermits/8827.pdf) gives gross generation of 50,182 kW per turbine, which is 50.2 MW.

### G100001055237 / Anadarko power station / Roulet 13
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units), 49 (Construction to operating checked)*
**Action:** Leave Equipment Manufacturer/Model of unit Roulet 13 (G100001055237) as GE Vernova: LM6000PC-Sprint. It is still correct. Add the 2 links below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `GE Vernova: LM6000PC-Sprint` -> `GE Vernova: LM6000PC-Sprint`
  - Turbine/Engine Equipment Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8827.pdf (ok=True, contains_value=True)
  - Turbine/Engine Equipment Data Source: https://www.power-eng.com/gas-turbines/new-ge-vernova-aeroderivative-units-to-expand-capacity-at-oklahoma-gas-plant/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The same permit memorandum names two LM6000PC-SPRINT turbines for units 12 and 13. The Power Engineering article names GE Vernova as supplier.

### G100001101631 / Bristow Energy Center / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Set Status Detail of unit 1 (G100001101631) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Associated Electric Cooperative says the site is going through regulatory approvals and permitting. It expects construction to start in 2027 and take about two years.

https://www.aeci.org/bristow-energy-center-1
- `Status Detail`: `` -> `Associated Electric Cooperative says the site is going through regulatory approvals and permitting. It expects construction to start in 2027 and take about two years.

https://www.aeci.org/bristow-energy-center-1`
  - Status Detail: https://www.aeci.org/bristow-energy-center-1 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Associated Electric Cooperative project page at https://www.aeci.org/bristow-energy-center-1 says construction is scheduled to begin in 2027. The status stays pre-construction. Construction has not started, so status stays pre-construction. The page meta description says under construction but its text says construction begins in 2027. Latest Activity is left alone because the project is moving. I found no operator and no air permit application in the harvest.

### G100001101676 / Citadel Facility Data Center power station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Set Status Detail of unit 1 (G100001101676) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

The Oklahoma Department of Environmental Quality issued minor source construction permit 2026-0286-C to Citadel Asset Ventures LLC on August 6, 2026. It covers 118 diesel generator engines plus one fire pump engine at the Citadel Facility data center in Sperry. No comments came in during the 30 day public notice.

https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf
- `Status Detail`: `` -> `The Oklahoma Department of Environmental Quality issued minor source construction permit 2026-0286-C to Citadel Asset Ventures LLC on August 6, 2026. It covers 118 diesel generator engines plus one fire pump engine at the Citadel Facility data center in Sperry. No comments came in during the 30 day public notice.

https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf`
  - Status Detail: https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Oklahoma Department of Environmental Quality permit memo and permit dated August 6, 2026 at https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf state the issue date, the engine groups and the public notice result. The permit confirms 36 Cummins DQLF engines. The 99 MW total uses 2.75 MW electrical per engine from the Cummins DQLF product page https://www.cummins.com/en-na/generators/products/dqlf. The permit gives 3,997 horsepower, which is mechanical output and not the electrical rating. No start year is given in the permit. Latest Activity is left alone because the permit is under a year old.

### G100001101678 / Citadel Facility Data Center power station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Add the entry below at the top of the Status Detail box of unit 2 (G100001101678), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

The Oklahoma Department of Environmental Quality issued minor source construction permit 2026-0286-C to Citadel Asset Ventures LLC on August 6, 2026. It covers 118 diesel generator engines plus one fire pump engine at the Citadel Facility data center in Sperry. No comments came in during the 30 day public notice.

https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf
- `Status Detail`: `ALQ42026: equipment TBD between Caterpillar 3516E / MTU 20V4000G74S; both engine models have similar capacities (2.75 and 2.8 MW)` -> `The Oklahoma Department of Environmental Quality issued minor source construction permit 2026-0286-C to Citadel Asset Ventures LLC on August 6, 2026. It covers 118 diesel generator engines plus one fire pump engine at the Citadel Facility data center in Sperry. No comments came in during the 30 day public notice.

https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf

ALQ42026: equipment TBD between Caterpillar 3516E / MTU 20V4000G74S; both engine models have similar capacities (2.75 and 2.8 MW)`
  - Status Detail: https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Oklahoma Department of Environmental Quality permit memo and permit dated August 6, 2026 at https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf state the issue date, the engine groups and the public notice result. The permit engine table at https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf shows Caterpillar 3516E and MTU 20V4000 as options for engines 37 to 108 and does not say how many of each. So the model is left blank. Capacity per engine of 2.75 MW matches the Caterpillar page https://www.cat.com/en_US/products/new/power-systems/electric-power/diesel-generator-sets/117341.html and the MTU nomenclature sheet. No start year is given.

### G100000402193 / Comanche (OK) power station / CC1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of all 3 units of Comanche (OK) power station as Public Service Company of Oklahoma [100%]. It is still correct. Add the link below to the Owners Data Source box on each unit. Keep the links already there.
- `Owner(s)`: `Public Service Company of Oklahoma [100%]` -> `Public Service Company of Oklahoma [100%]`
  - Owners Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The air permit application at https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true was filed on behalf of Public Service Company of Oklahoma, which proposes to build the two new blocks at its Comanche Power Station. The EIA-860M table for September 2026 also lists Public Service Co of Oklahoma as the entity for plant 8059.

### G100001101686 / Comanche (OK) power station / CC2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Status of unit CC2 (G100001101686) as pre-construction. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `pre-construction` -> `pre-construction`
  - Status Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Status Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUaLH0lqtPpM7wIdg%C3%890yv415JmIPaJZoK9Ya%C3%89BR7tBogWWFqxsgDeUkF%C3%81wO80qH%C3%8979HjhK2Ry9yhHML12tWVu1g%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A permit application filed for Public Service Company of Oklahoma on April 22, 2026 at https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true asks the Oklahoma Department of Environmental Quality for a construction permit for two new combined cycle turbines at Comanche. The department's letter of June 10, 2026 at https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUaLH0lqtPpM7wIdg%C3%890yv415JmIPaJZoK9Ya%C3%89BR7tBogWWFqxsgDeUkF%C3%81wO80qH%C3%8979HjhK2Ry9yhHML12tWVu1g%3D/?ViewerMode=PDF&ForceDownload=true says the application is administratively complete and ready for public review. The status stays pre-construction. Latest Activity is left alone because the project is moving: the air permit application was filed in April 2026 and found complete in June 2026. The air permit is still in technical review. The 2026 resource plan refresh does not mention the two new blocks.

### G100001101686 / Comanche (OK) power station / CC2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Capacity (MW) of unit CC2 (G100001101686) as 686.4. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `686.4` -> `686.4`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists plant 8059 with unit code CC2: generator 2G1 at 408.8 MW and generator 2S1 at 277.6 MW. Together that is 686.4 MW, the same as GEM. The air permit application gives 633 MW per block and the Southwest Power Pool queue gives 775.2 MW, so a question is raised.

### G100001101686 / Comanche (OK) power station / CC2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Start year of unit CC2 (G100001101686) as 2029. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2029` -> `2029`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx shows planned operation in September 2029 for generators 2G1 and 2S1. This is a projected year, so the reviewer adds a new scheduled event for 2029 with Source Year 2026 and never changes an existing event.

### G100001101686 / Comanche (OK) power station / CC2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit CC2 (G100001101686) to Mitsubishi M501JAC. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `Mitsubishi M501JAC`
  - Turbine/Engine Equipment Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The air permit application at https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true says the company proposes two new Mitsubishi Model M501JAC combustion turbine generators, one for each combined cycle block.

### G100001101686 / Comanche (OK) power station / CC2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Set Status Detail of unit CC2 (G100001101686) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Public Service Company of Oklahoma applied on April 22, 2026 for a major source air construction permit for two new Mitsubishi M501JAC combined cycle blocks at Comanche. The Oklahoma Department of Environmental Quality found the application complete on June 10, 2026.

https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true
https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUaLH0lqtPpM7wIdg%C3%890yv415JmIPaJZoK9Ya%C3%89BR7tBogWWFqxsgDeUkF%C3%81wO80qH%C3%8979HjhK2Ry9yhHML12tWVu1g%3D/?ViewerMode=PDF&ForceDownload=true
- `Status Detail`: `` -> `Public Service Company of Oklahoma applied on April 22, 2026 for a major source air construction permit for two new Mitsubishi M501JAC combined cycle blocks at Comanche. The Oklahoma Department of Environmental Quality found the application complete on June 10, 2026.

https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true
https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUaLH0lqtPpM7wIdg%C3%890yv415JmIPaJZoK9Ya%C3%89BR7tBogWWFqxsgDeUkF%C3%81wO80qH%C3%8979HjhK2Ry9yhHML12tWVu1g%3D/?ViewerMode=PDF&ForceDownload=true`
  - Status Detail: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Status Detail: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUaLH0lqtPpM7wIdg%C3%890yv415JmIPaJZoK9Ya%C3%89BR7tBogWWFqxsgDeUkF%C3%81wO80qH%C3%8979HjhK2Ry9yhHML12tWVu1g%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The two documents are the permit application and the department's completeness letter. Both name the Comanche Power Station.

### G100001101687 / Comanche (OK) power station / CC3
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Status of unit CC3 (G100001101687) as pre-construction. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `pre-construction` -> `pre-construction`
  - Status Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Status Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUaLH0lqtPpM7wIdg%C3%890yv415JmIPaJZoK9Ya%C3%89BR7tBogWWFqxsgDeUkF%C3%81wO80qH%C3%8979HjhK2Ry9yhHML12tWVu1g%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A permit application filed for Public Service Company of Oklahoma on April 22, 2026 at https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true asks the Oklahoma Department of Environmental Quality for a construction permit for two new combined cycle turbines at Comanche. The department's letter of June 10, 2026 at https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUaLH0lqtPpM7wIdg%C3%890yv415JmIPaJZoK9Ya%C3%89BR7tBogWWFqxsgDeUkF%C3%81wO80qH%C3%8979HjhK2Ry9yhHML12tWVu1g%3D/?ViewerMode=PDF&ForceDownload=true says the application is administratively complete and ready for public review. The status stays pre-construction. Latest Activity is left alone because the project is moving: the air permit application was filed in April 2026 and found complete in June 2026. The air permit is still in technical review. The 2026 resource plan refresh does not mention the two new blocks.

### G100001101687 / Comanche (OK) power station / CC3
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Capacity (MW) of unit CC3 (G100001101687) as 686.4. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `686.4` -> `686.4`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists plant 8059 with unit code CC3: generator 3G1 at 408.8 MW and generator 3S1 at 277.6 MW. Together that is 686.4 MW, the same as GEM. The air permit application gives 633 MW per block and the Southwest Power Pool queue gives 775.2 MW, so a question is raised.

### G100001101687 / Comanche (OK) power station / CC3
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Start year of unit CC3 (G100001101687) as 2029. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2029` -> `2029`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx shows planned operation in September 2029 for generators 3G1 and 3S1. This is a projected year, so the reviewer adds a new scheduled event for 2029 with Source Year 2026 and never changes an existing event.

### G100001101687 / Comanche (OK) power station / CC3
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit CC3 (G100001101687) to Mitsubishi M501JAC. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `Mitsubishi M501JAC`
  - Turbine/Engine Equipment Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The air permit application at https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true says the company proposes two new Mitsubishi Model M501JAC combustion turbine generators, one for each combined cycle block.

### G100001101687 / Comanche (OK) power station / CC3
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Set Status Detail of unit CC3 (G100001101687) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Public Service Company of Oklahoma applied on April 22, 2026 for a major source air construction permit for two new Mitsubishi M501JAC combined cycle blocks at Comanche. The Oklahoma Department of Environmental Quality found the application complete on June 10, 2026.

https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true
https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUaLH0lqtPpM7wIdg%C3%890yv415JmIPaJZoK9Ya%C3%89BR7tBogWWFqxsgDeUkF%C3%81wO80qH%C3%8979HjhK2Ry9yhHML12tWVu1g%3D/?ViewerMode=PDF&ForceDownload=true
- `Status Detail`: `` -> `Public Service Company of Oklahoma applied on April 22, 2026 for a major source air construction permit for two new Mitsubishi M501JAC combined cycle blocks at Comanche. The Oklahoma Department of Environmental Quality found the application complete on June 10, 2026.

https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true
https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUaLH0lqtPpM7wIdg%C3%890yv415JmIPaJZoK9Ya%C3%89BR7tBogWWFqxsgDeUkF%C3%81wO80qH%C3%8979HjhK2Ry9yhHML12tWVu1g%3D/?ViewerMode=PDF&ForceDownload=true`
  - Status Detail: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Status Detail: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUaLH0lqtPpM7wIdg%C3%890yv415JmIPaJZoK9Ya%C3%89BR7tBogWWFqxsgDeUkF%C3%81wO80qH%C3%8979HjhK2Ry9yhHML12tWVu1g%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The two documents are the permit application and the department's completeness letter. Both name the Comanche Power Station.

### G100001091022 / Cross Timbers Power Plant / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Status of unit 1 (G100001091022) as pre-construction. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `pre-construction` -> `pre-construction`
  - Status Data Source: https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Permits_Issued_During_Past_Year.csv (ok=True, contains_value=True)
  - Status Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Oklahoma Department of Environmental Quality list of permits issued in the past year at https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Permits_Issued_During_Past_Year.csv shows construction permit 2025-0397-C for Cross Timbers Power Plant issued on December 22, 2025. The permit memorandum from October 31, 2025 at https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf describes two simple cycle gas turbines still to be built. The status stays pre-construction. The company has not chosen between a GE Vernova 7F.05 and a Siemens SGT6-5000F turbine, so no model can be reported. No start year is given in the permit memorandum. Latest Activity is left alone because the permit was issued in December 2025, less than a year ago.

### G100001091022 / Cross Timbers Power Plant / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Capacity (MW) of unit 1 (G100001091022) as 255.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `255.0` -> `255.0`
  - Capacity Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The permit memorandum at https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf lists 255 MW for each Siemens SGT6-5000F option and 240 MW for each GE Vernova 7F.05 option. GEM's 255 MW matches the Siemens option only, because the company has not chosen yet.

### G100001091022 / Cross Timbers Power Plant / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 17 (Unknown technology rechecked)*
**Action:** Leave Turbine/Engine Technology of unit 1 (G100001091022) as gas turbine. It is still correct. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `gas turbine` -> `gas turbine`
  - Turbine/Engine Technology Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The permit memorandum at https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf says the company is proposing two simple cycle natural gas fired combustion turbines.

### G100001091022 / Cross Timbers Power Plant / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Add the entry below at the top of the Status Detail box of unit 1 (G100001091022), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Construction permit 2025-0397-C was issued by the Oklahoma Department of Environmental Quality on December 22, 2025.

https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Permits_Issued_During_Past_Year.csv
- `Status Detail`: `NF 1/12/26: Draft air permit issued in Nov 2025. Cross Timbers is currently deciding between one of two potential turbines: the GE Vernova 7F.05 units or Siemens SGT6-5000F units, with a nominal gross output of 480 MW or 510 MW respectively. CCS to be added after Dec 2031 (p.4-4 of the Permit Application).` -> `Construction permit 2025-0397-C was issued by the Oklahoma Department of Environmental Quality on December 22, 2025.

https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Permits_Issued_During_Past_Year.csv

NF 1/12/26: Draft air permit issued in Nov 2025. Cross Timbers is currently deciding between one of two potential turbines: the GE Vernova 7F.05 units or Siemens SGT6-5000F units, with a nominal gross output of 480 MW or 510 MW respectively. CCS to be added after Dec 2031 (p.4-4 of the Permit Application).`
  - Status Detail: https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Permits_Issued_During_Past_Year.csv (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The department's list of permits issued in the past year names Cross Timbers Power Plant and this permit number.

### G100001091022 / Cross Timbers Power Plant / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Owner(s) of all 2 units of Cross Timbers Power Plant as Cross Timbers Power LLC [100%]. It is still correct. Add the link below to the Owners Data Source box on each unit. Keep the links already there.
- `Owner(s)`: `Cross Timbers Power LLC [100%]` -> `Cross Timbers Power LLC [100%]`
  - Owners Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The permit memorandum at https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf names Cross Timbers Power LLC as the company that applied. It does not state ownership shares, so the 100 percent is GEM's existing value.

### G100001091024 / Cross Timbers Power Plant / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Status of unit 2 (G100001091024) as pre-construction. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `pre-construction` -> `pre-construction`
  - Status Data Source: https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Permits_Issued_During_Past_Year.csv (ok=True, contains_value=True)
  - Status Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Oklahoma Department of Environmental Quality list of permits issued in the past year at https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Permits_Issued_During_Past_Year.csv shows construction permit 2025-0397-C for Cross Timbers Power Plant issued on December 22, 2025. The permit memorandum from October 31, 2025 at https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf describes two simple cycle gas turbines still to be built. The status stays pre-construction. The company has not chosen between a GE Vernova 7F.05 and a Siemens SGT6-5000F turbine, so no model can be reported. No start year is given in the permit memorandum. Latest Activity is left alone because the permit was issued in December 2025, less than a year ago.

### G100001091024 / Cross Timbers Power Plant / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Capacity (MW) of unit 2 (G100001091024) as 255.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `255.0` -> `255.0`
  - Capacity Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The permit memorandum at https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf lists 255 MW for each Siemens SGT6-5000F option and 240 MW for each GE Vernova 7F.05 option. GEM's 255 MW matches the Siemens option only, because the company has not chosen yet.

### G100001091024 / Cross Timbers Power Plant / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 17 (Unknown technology rechecked)*
**Action:** Leave Turbine/Engine Technology of unit 2 (G100001091024) as gas turbine. It is still correct. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `gas turbine` -> `gas turbine`
  - Turbine/Engine Technology Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The permit memorandum at https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf says the company is proposing two simple cycle natural gas fired combustion turbines.

### G100001091024 / Cross Timbers Power Plant / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Add the entry below at the top of the Status Detail box of unit 2 (G100001091024), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Construction permit 2025-0397-C was issued by the Oklahoma Department of Environmental Quality on December 22, 2025.

https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Permits_Issued_During_Past_Year.csv
- `Status Detail`: `NF 1/12/26: Draft air permit issued in Nov 2025. Cross Timbers is currently deciding between one of two potential turbines: the GE Vernova 7F.05 units or Siemens SGT6-5000F units, with a nominal gross output of 480 MW or 510 MW respectively. CCS to be added after Dec 2031 (p.4-4 of the Permit Application).` -> `Construction permit 2025-0397-C was issued by the Oklahoma Department of Environmental Quality on December 22, 2025.

https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Permits_Issued_During_Past_Year.csv

NF 1/12/26: Draft air permit issued in Nov 2025. Cross Timbers is currently deciding between one of two potential turbines: the GE Vernova 7F.05 units or Siemens SGT6-5000F units, with a nominal gross output of 480 MW or 510 MW respectively. CCS to be added after Dec 2031 (p.4-4 of the Permit Application).`
  - Status Detail: https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Permits_Issued_During_Past_Year.csv (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The department's list of permits issued in the past year names Cross Timbers Power Plant and this permit number.

### G100000403305 / Horseshoe Lake power station / 10
*change to an existing unit; checklist rows 21 (Planned retirements searched), 37 (IRP box ticked on every IRP project (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Planned retire of unit 10 (G100000403305) as 2035. It is still correct. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `2035` -> `2035`
  - Planned Retire Data Source: https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 OG&E integrated resource plan, page 16, says OG&E plans to retire Horseshoe Lake units 9 and 10 in 2035. The plan is at https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8. The EIA-860M table for September 2026 lists unit 10 as operating at 60.5 MW, so no status change. The question about the EIP record is in the questions list.

### G100001092969 / Horseshoe Lake power station / 13
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 50 (Other last-minute status changes checked)*
**Action:** Set Status of unit 13 (G100001092969) to construction. It now says pre-construction. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `pre-construction` -> `construction`
- milestone `construction`: October 2026 (https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/)
  - Status Data Source: https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: On the October 28, 2026 earnings call, OGE Energy said Horseshoe Lake units 13 and 14 remain under construction and are expected to add another 440 MW. The call summary is at https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/. The EIA-860M table for September 2026 still lists them as regulatory approvals received and not under construction, so this is a single-source status change. A construction start date was not found. The project is moving, so Latest Activity is left alone. Start year 2029 in GEM was not contradicted.

### G100001092969 / Horseshoe Lake power station / 13
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Set Equipment Manufacturer/Model of unit 13 (G100001092969) to GE Vernova: 7FA.05. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE Vernova: 7FA.05`
  - Turbine/Engine Equipment Data Source: https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 OG&E integrated resource plan, page 17, says units 13 and 14 are virtually identical to units 11 and 12, which use GE 7FA.05 turbines. The plan is at https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8. It does not name the turbine for units 13 and 14 directly.

### G100001092970 / Horseshoe Lake power station / 14
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 50 (Other last-minute status changes checked)*
**Action:** Set Status of unit 14 (G100001092970) to construction. It now says pre-construction. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `pre-construction` -> `construction`
- milestone `construction`: October 2026 (https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/)
  - Status Data Source: https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: On the October 28, 2026 earnings call, OGE Energy said Horseshoe Lake units 13 and 14 remain under construction and are expected to add another 440 MW. The call summary is at https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/. The EIA-860M table for September 2026 still lists them as regulatory approvals received and not under construction, so this is a single-source status change. A construction start date was not found. The project is moving, so Latest Activity is left alone. Start year 2029 in GEM was not contradicted.

### G100001092970 / Horseshoe Lake power station / 14
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Set Equipment Manufacturer/Model of unit 14 (G100001092970) to GE Vernova: 7FA.05. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE Vernova: 7FA.05`
  - Turbine/Engine Equipment Data Source: https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 OG&E integrated resource plan, page 17, says units 13 and 14 are virtually identical to units 11 and 12, which use GE 7FA.05 turbines. The plan is at https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8. It does not name the turbine for units 13 and 14 directly.

### G100001101622 / Horseshoe Lake power station / 15
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Capacity (MW) of unit 15 (G100001101622) as 755. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `755` -> `755`
  - Capacity Data Source: https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: On the October 28, 2026 earnings call, OGE Energy said it filed for pre-approval of a 755 MW combined cycle plant, Horseshoe Lake unit 15. The call summary is at https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/. Status pre-construction fits: the commission pre-approval case was filed in 2026. No newer dated report was needed for Latest Activity.

### G100001101622 / Horseshoe Lake power station / 15
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Start year of unit 15 (G100001101622) as 2031. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2031` -> `2031`
  - Start Year Data Source: https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The same call summary at https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ says unit 15 is expected to enter service in 2031. The human adds this as a new scheduled event.

### G100000403307 / Horseshoe Lake power station / 8
*change to an existing unit; checklist rows 21 (Planned retirements searched), 37 (IRP box ticked on every IRP project (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Planned retire of unit 8 (G100000403307) as 2027. It is still correct. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `2027` -> `2027`
  - Planned Retire Data Source: https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 OG&E integrated resource plan, page 16, says OG&E plans to retire Horseshoe Lake unit 8 in 2027. The plan is at https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8. The EIA-860M table for September 2026 lists unit 8 as operating at 443 MW. The 2027 retirement plan still holds in the 2026 plan.

### G100000403308 / Horseshoe Lake power station / 9
*change to an existing unit; checklist rows 21 (Planned retirements searched), 37 (IRP box ticked on every IRP project (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Planned retire of unit 9 (G100000403308) as 2035. It is still correct. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `2035` -> `2035`
  - Planned Retire Data Source: https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 OG&E integrated resource plan, page 16, says OG&E plans to retire Horseshoe Lake units 9 and 10 in 2035. The plan is at https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8. The EIA-860M table for September 2026 lists unit 9 as operating. The 2035 retirement plan still holds.

### G100001101619 / Hugo power station / Site A
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Leave Equipment Manufacturer/Model of unit Site A (G100001101619) as Siemens Energy: SGT-600. It is still correct. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `Siemens Energy: SGT-600` -> `Siemens Energy: SGT-600`
  - Turbine/Engine Equipment Data Source: https://constructionreviewonline.com/1b-hugo-plant-expansion-western-farmers-electric-breaks-ground-on-nine-gas-turbines-in-oklahoma/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The October 2026 article says three Siemens Energy SGT-600 turbines will be installed, and the Rural Utilities Service environmental assessment names the same turbines. This matches the model already in the database.

### G100001101619 / Hugo power station / Site A
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Start year of unit Site A (G100001101619) as 2029. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2029` -> `2029`
  - Start Year Data Source: https://constructionreviewonline.com/1b-hugo-plant-expansion-western-farmers-electric-breaks-ground-on-nine-gas-turbines-in-oklahoma/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The same article says construction should finish by mid-2029 and that a cooperative annual report lists 2029 as the commercial operation date. The human adds this as a scheduled event with Event Year 2029 and Source Year 2026 only if one is not already there.

### G100001101620 / Hugo power station / Site B
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Leave Equipment Manufacturer/Model of unit Site B (G100001101620) as Siemens Energy: SGT-800. It is still correct. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `Siemens Energy: SGT-800` -> `Siemens Energy: SGT-800`
  - Turbine/Engine Equipment Data Source: https://constructionreviewonline.com/1b-hugo-plant-expansion-western-farmers-electric-breaks-ground-on-nine-gas-turbines-in-oklahoma/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The October 2026 article says six Siemens Energy SGT-800 turbines will be installed. This matches the model already in the database.

### G100001101620 / Hugo power station / Site B
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Start year of unit Site B (G100001101620) as 2029. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2029` -> `2029`
  - Start Year Data Source: https://constructionreviewonline.com/1b-hugo-plant-expansion-western-farmers-electric-breaks-ground-on-nine-gas-turbines-in-oklahoma/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The same article says construction should finish by mid-2029 and that a cooperative annual report lists 2029 as the commercial operation date. The human adds this as a scheduled event with Event Year 2029 and Source Year 2026 only if one is not already there.

### G100001091053 / Muskogee Data Center power station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only)), 49 (Construction to operating checked)*
**Action:** Set Capacity (MW) of unit 1 (G100001091053) to 324.0. It now says 283.1. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `283.1` -> `324.0`
  - Capacity Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ae6Ctfv7oSCmhMZ%C3%89kDp%C3%89JKeyyrF%C3%897NeqHWN6Fd0wYTdl604KTTG6bsIhnFC9Sgq7vhd656jR%C3%895uQBkEpWYOBnMg%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft permit gives the MTU generators as 3,250 kilowatts each, so 83 engines make 269.75 MW. The 21 Cummins engines are rated 3,391 horsepower, about 2.53 MW each or 53.1 MW. The one Caterpillar engine is about 1.11 MW. The sum is about 324 MW. This is my own sum of the permit's ratings, and the permit states no total.

### G100001091053 / Muskogee Data Center power station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units), 49 (Construction to operating checked)*
**Action:** Set Equipment Manufacturer/Model of unit 1 (G100001091053) to MTU: 20V4000 DS3250, Caterpillar Energy Solutions: D1000 GC, Cummins: C3000D6EB. It now says MTU: 20V400G94S DS3000, Caterpillar Energy Solutions: D1000 GC, Cummins: C3000D6EB. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `MTU: 20V400G94S DS3000, Caterpillar Energy Solutions: D1000 GC, Cummins: C3000D6EB` -> `MTU: 20V4000 DS3250, Caterpillar Energy Solutions: D1000 GC, Cummins: C3000D6EB`
  - Turbine/Engine Equipment Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ae6Ctfv7oSCmhMZ%C3%89kDp%C3%89JKeyyrF%C3%897NeqHWN6Fd0wYTdl604KTTG6bsIhnFC9Sgq7vhd656jR%C3%895uQBkEpWYOBnMg%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft permit changes the MTU model from 20V4000 DS3000 to 20V4000 DS3250 and adds four more of them. The Cummins and Caterpillar models are as in the database.

### G100001091053 / Muskogee Data Center power station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only)), 49 (Construction to operating checked)*
**Action:** Add the entry below at the top of the Status Detail box of unit 1 (G100001091053), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Draft permit memorandum MIC001302 dated September 21, 2026 (public comment October 15 to November 14, 2026) lists 105 diesel emergency engines: 83 MTU 3,250 kW, 21 Cummins C3000D6EB and 1 Caterpillar D1000GC. It adds four MTU engines to building MSK1-B and renames the facility Core Scientific MSK1-A and MSK1-B.

https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ae6Ctfv7oSCmhMZ%C3%89kDp%C3%89JKeyyrF%C3%897NeqHWN6Fd0wYTdl604KTTG6bsIhnFC9Sgq7vhd656jR%C3%895uQBkEpWYOBnMg%3D/?ViewerMode=PDF&ForceDownload=true
- `Status Detail`: `ALQ42026: will probably begin operations soon: "Core Scientific also said in May that a leased 70 MW building at Muskogee was undergoing final testing and commissioning. Designed for Nvidia’s GB300 platform, that building had been scheduled for customer delivery during the second quarter of 2026, although Friday’s acquisition announcement did not provide an updated commissioning status."

NF 1/14/26: 102 backup diesel engines (29x3.49MW MTU engines, 71x 2.53MW Cummins engines, 2x1.11MW CATD1000GC engines). Draft Permit Application for the engines No. 2025-0466-C was filed in Oct 2025 for public comment.  Monitor here https://oklahoma.gov/deq/permits/air-permits/pp-ip/active-air-permit-listing.html The data center is already under construction.` -> `Draft permit memorandum MIC001302 dated September 21, 2026 (public comment October 15 to November 14, 2026) lists 105 diesel emergency engines: 83 MTU 3,250 kW, 21 Cummins C3000D6EB and 1 Caterpillar D1000GC. It adds four MTU engines to building MSK1-B and renames the facility Core Scientific MSK1-A and MSK1-B.

https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ae6Ctfv7oSCmhMZ%C3%89kDp%C3%89JKeyyrF%C3%897NeqHWN6Fd0wYTdl604KTTG6bsIhnFC9Sgq7vhd656jR%C3%895uQBkEpWYOBnMg%3D/?ViewerMode=PDF&ForceDownload=true

ALQ42026: will probably begin operations soon: "Core Scientific also said in May that a leased 70 MW building at Muskogee was undergoing final testing and commissioning. Designed for Nvidia’s GB300 platform, that building had been scheduled for customer delivery during the second quarter of 2026, although Friday’s acquisition announcement did not provide an updated commissioning status."

NF 1/14/26: 102 backup diesel engines (29x3.49MW MTU engines, 71x 2.53MW Cummins engines, 2x1.11MW CATD1000GC engines). Draft Permit Application for the engines No. 2025-0466-C was filed in Oct 2025 for public comment.  Monitor here https://oklahoma.gov/deq/permits/air-permits/pp-ip/active-air-permit-listing.html The data center is already under construction.`
  - Status Detail: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ae6Ctfv7oSCmhMZ%C3%89kDp%C3%89JKeyyrF%C3%897NeqHWN6Fd0wYTdl604KTTG6bsIhnFC9Sgq7vhd656jR%C3%895uQBkEpWYOBnMg%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: This is new text for the top of the box. The draft permit is the source.

### G100001055294 / Northeastern Station / Unit 3, timepoint 2
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Planned retire of unit Unit 3, timepoint 2 (G100001055294) as 2041. It is still correct. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `2041` -> `2041`
  - Planned Retire Data Source: https://www.sec.gov/Archives/edgar/data/4904/000000490426000059/aep-20260630.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The same AEP report says the April 2025 agreement with the Oklahoma Department of Environmental Quality allows Unit 3 to run on natural gas through May 31, 2041. That agreement still needs approval by the federal Environmental Protection Agency. So the planned retirement of 2041 still holds.

### G100001101665 / Northeastern Station / Unit 5
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit Unit 5 (G100001101665) to GE Vernova. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE Vernova`
  - Turbine/Engine Equipment Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AWtoGCCMAPa3ZmzV9bv2lNVdjzgKUd4GV4oRCuMNP0goK6NykmHJHyG5WSO1mUZe7mM1J5HwOpKpJWodbQLKNmw%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Oklahoma Department of Environmental Quality draft permit memo from September 2026 (see link) says PSO proposes two 229 MW GE natural gas simple cycle combustion turbines. The memo names the maker but no model, so the model was not found. Approved May 2026 and projected online by the end of 2028. The project is moving, so Latest Activity is left alone. The turbine model is not in the permit memo.

### G100001101666 / Northeastern Station / Unit 6
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit Unit 6 (G100001101666) to GE Vernova. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE Vernova`
  - Turbine/Engine Equipment Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AWtoGCCMAPa3ZmzV9bv2lNVdjzgKUd4GV4oRCuMNP0goK6NykmHJHyG5WSO1mUZe7mM1J5HwOpKpJWodbQLKNmw%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Oklahoma Department of Environmental Quality draft permit memo from September 2026 (see link) says PSO proposes two 229 MW GE natural gas simple cycle combustion turbines. The memo names the maker but no model, so the model was not found. Same as Unit 5.

### G100001093027 / ONE Nuclear power station 1 / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Leave Equipment Manufacturer/Model of unit 1 (G100001093027) as Rolls-Royce. It is still correct. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `Rolls-Royce` -> `Rolls-Royce`
  - Turbine/Engine Equipment Data Source: https://www.sec.gov/Archives/edgar/data/1846416/000149315225019001/ex99-1.htm (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The same filing says ONE Nuclear has a non-binding relationship with Rolls-Royce Solutions America for gas generators. This implies but does not prove the engines at this site.

### G100001101690 / Port of Inola Power Station / 1A
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 17 (Unknown technology rechecked)*
**Action:** Leave Turbine/Engine Technology of unit 1A (G100001101690) as combined cycle. It is still correct. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `combined cycle` -> `combined cycle`
  - Turbine/Engine Technology Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUk7Pfms86Dwy6B9RtySPXY8zCMWK8b6prK%C3%81TES%C3%81ksWrcWp06P8ZaPQ3atfhjmXORD%C3%89mJf1dwQNey9skV%C3%89JMF5I%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Public Service Company of Oklahoma permit application saved in the Oklahoma Department of Environmental Quality document store (https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUk7Pfms86Dwy6B9RtySPXY8zCMWK8b6prK%C3%81TES%C3%81ksWrcWp06P8ZaPQ3atfhjmXORD%C3%89mJf1dwQNey9skV%C3%89JMF5I%3D/?ViewerMode=PDF&ForceDownload=true) describes two new combined cycle combustion turbine units with a total nominal output of 1,282 MW, which is 641 MW each. The permit application is under administrative review. The project is moving, so Latest Activity is left alone. The only emergency equipment named is one 2,500 kilowatt emergency diesel generator, which is not a data center backup fleet. No start date was found beyond what GEM already shows.

### G100001101690 / Port of Inola Power Station / 1A
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Leave Equipment Manufacturer/Model of unit 1A (G100001101690) as GE Vernova: 7HA.03. It is still correct. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `GE Vernova: 7HA.03` -> `GE Vernova: 7HA.03`
  - Turbine/Engine Equipment Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUk7Pfms86Dwy6B9RtySPXY8zCMWK8b6prK%C3%81TES%C3%81ksWrcWp06P8ZaPQ3atfhjmXORD%C3%89mJf1dwQNey9skV%C3%89JMF5I%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The permit application (https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUk7Pfms86Dwy6B9RtySPXY8zCMWK8b6prK%C3%81TES%C3%81ksWrcWp06P8ZaPQ3atfhjmXORD%C3%89mJf1dwQNey9skV%C3%89JMF5I%3D/?ViewerMode=PDF&ForceDownload=true) says the station will have two GE Model 7HA.03 combustion turbine generators with heat recovery steam generators.

### G100001101691 / Port of Inola Power Station / 1B
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 17 (Unknown technology rechecked)*
**Action:** Leave Turbine/Engine Technology of unit 1B (G100001101691) as combined cycle. It is still correct. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `combined cycle` -> `combined cycle`
  - Turbine/Engine Technology Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUk7Pfms86Dwy6B9RtySPXY8zCMWK8b6prK%C3%81TES%C3%81ksWrcWp06P8ZaPQ3atfhjmXORD%C3%89mJf1dwQNey9skV%C3%89JMF5I%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Public Service Company of Oklahoma permit application saved in the Oklahoma Department of Environmental Quality document store (https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUk7Pfms86Dwy6B9RtySPXY8zCMWK8b6prK%C3%81TES%C3%81ksWrcWp06P8ZaPQ3atfhjmXORD%C3%89mJf1dwQNey9skV%C3%89JMF5I%3D/?ViewerMode=PDF&ForceDownload=true) describes two new combined cycle combustion turbine units with a total nominal output of 1,282 MW, which is 641 MW each. The permit application is under administrative review. The project is moving, so Latest Activity is left alone. The only emergency equipment named is one 2,500 kilowatt emergency diesel generator, which is not a data center backup fleet. No start date was found beyond what GEM already shows.

### G100001101691 / Port of Inola Power Station / 1B
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit 1B (G100001101691) to GE Vernova: 7HA.03. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE Vernova: 7HA.03`
  - Turbine/Engine Equipment Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUk7Pfms86Dwy6B9RtySPXY8zCMWK8b6prK%C3%81TES%C3%81ksWrcWp06P8ZaPQ3atfhjmXORD%C3%89mJf1dwQNey9skV%C3%89JMF5I%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The permit application (https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AUk7Pfms86Dwy6B9RtySPXY8zCMWK8b6prK%C3%81TES%C3%81ksWrcWp06P8ZaPQ3atfhjmXORD%C3%89mJf1dwQNey9skV%C3%89JMF5I%3D/?ViewerMode=PDF&ForceDownload=true) says both new turbines are GE Model 7HA.03, so unit 1B should carry the same model as unit 1A.

### G100001028184 / Ripley Energy Center power station / RP1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Set Capacity (MW) of unit RP1 (G100001028184) to 419.0. It now says 445.0. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `445.0` -> `419.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Capacity Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8877.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists Ripley Energy Center, plant 67262, generator RP1, nameplate 419.0 MW, net winter 444.5 MW, planned operation April 2027, under construction more than 50 percent complete. The Oklahoma Department of Environmental Quality permit memorandum (https://applications.deq.ok.gov/permitspublic/storedpermits/8877.pdf) describes one combustion turbine with a nominal gross output of 420 MW. GEM's 445 MW matches the winter capability, not the nameplate. The unit is moving toward its April 2027 start, so Latest Activity is left alone. No document says anything about Backup Power, and this is a utility peaking plant, not a data center, so the value no is not contradicted.

### G100001028184 / Ripley Energy Center power station / RP1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Leave Status of unit RP1 (G100001028184) as construction. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `construction` -> `construction`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists generator RP1 as under construction, more than 50 percent complete. This is the same status GEM shows and is a replacement for the dead Associated Electric Cooperative link.

### G100001028184 / Ripley Energy Center power station / RP1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Leave Start year of unit RP1 (G100001028184) as 2027. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2027` -> `2027`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 gives a planned operation date of April 2027. The human adds this as a new scheduled event only if GEM lacks one.

### G100001028184 / Ripley Energy Center power station / RP1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units), 49 (Construction to operating checked)*
**Action:** Set Equipment Manufacturer/Model of unit RP1 (G100001028184) to Siemens Energy: SGT6-9000HL. It now says Siemens Energy: SGT6‑9000HL. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `Siemens Energy: SGT6‑9000HL` -> `Siemens Energy: SGT6-9000HL`
  - Turbine/Engine Equipment Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8877.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The permit memorandum (https://applications.deq.ok.gov/permitspublic/storedpermits/8877.pdf) names a single Siemens SGT6-9000HL simple cycle combustion turbine.

### G100001028184 / Ripley Energy Center power station / RP1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Capacity (MW) of unit RP1 (G100001028184) as it is. Add the 1 link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `445.0` -> `445.0`
  - Capacity Data Source: https://web.archive.org/web/20241208072036/https://aeci.org/resources/natural-gas/ripley/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The value is unchanged. The source box already holds a link to a page that is gone from its old address (https://www.aeci.org/resources/natural-gas/ripley/). The Internet Archive kept a saved copy of that page, which was read and states the value. The saved copy is added to the box next to the old link.

### G100001028184 / Ripley Energy Center power station / RP1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Status of unit RP1 (G100001028184) as it is. Add the 1 link below to the Status Data Source box. Keep the links already there.
- `Status`: `construction` -> `construction`
  - Status Data Source: https://web.archive.org/web/20241208072036/https://aeci.org/resources/natural-gas/ripley/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The value is unchanged. The source box already holds a link to a page that is gone from its old address (https://www.aeci.org/resources/natural-gas/ripley/). The Internet Archive kept a saved copy of that page, which was read and states the value. The saved copy is added to the box next to the old link.

### G100000403319 / Seminole (OK) power station / 1
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Planned retire of unit 1 (G100000403319) as 2031. It is still correct. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `2031` -> `2031`
  - Planned Retire Data Source: https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 integrated resource plan from OG&E (the Oklahoma Gas and Electric Company) says it plans to retire Seminole 1 in early 2031. This matches the 2031 already in the tracker. The human adds no new scheduled event, since the date is unchanged. The plan is at https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8.

### G100000403320 / Seminole (OK) power station / 2
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Planned retire of unit 2 (G100000403320) as 2033. It is still correct. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `2033` -> `2033`
  - Planned Retire Data Source: https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 integrated resource plan from OG&E (the Oklahoma Gas and Electric Company) says it plans to retire Seminole 2 in early 2033. This matches the 2033 already in the tracker. The human adds no new scheduled event, since the date is unchanged. The plan is at https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8.

### G100000403321 / Seminole (OK) power station / 3
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Planned retire of unit 3 (G100000403321) as 2035. It is still correct. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `2035` -> `2035`
  - Planned Retire Data Source: https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 integrated resource plan from OG&E (the Oklahoma Gas and Electric Company) says it plans to retire Seminole 3 in early 2035. This matches the 2035 already in the tracker. The human adds no new scheduled event, since the date is unchanged. The plan is at https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8.

### G100001072817 / Tinker Air Force Base power station / 1-2
*change to an existing unit*
**Action:** Leave Start year of unit 1-2 (G100001072817) as 2026. It is still correct. Add the 2 links below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2026` -> `2026`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Start Year Data Source: https://www.oge.com/documents/d/portal/oge-2026-irp-final (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Both the EIA table and OG&E's 2026 integrated resource plan give March 2026.

### G100001072817 / Tinker Air Force Base power station / 1-2
*change to an existing unit*
**Action:** Set Status Detail of unit 1-2 (G100001072817) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

First fire of the two new LM6000 turbines was on November 26, 2025. OG&E reports the units were placed in service in March 2026.

https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AeNgrdQLsFw5W8dEEwRTc%C3%81pApsum6Hqboy8ro%C3%81CyJ8OFtu0HRxDmnOy6W2%C3%81nwK2s%C3%81raDCV3qK%C3%8912Ie4gZNs%C3%89Vd0%3D/?ViewerMode=PDF&ForceDownload=true
https://www.oge.com/documents/d/portal/oge-2026-irp-final
- `Status Detail`: `` -> `First fire of the two new LM6000 turbines was on November 26, 2025. OG&E reports the units were placed in service in March 2026.

https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AeNgrdQLsFw5W8dEEwRTc%C3%81pApsum6Hqboy8ro%C3%81CyJ8OFtu0HRxDmnOy6W2%C3%81nwK2s%C3%81raDCV3qK%C3%8912Ie4gZNs%C3%89Vd0%3D/?ViewerMode=PDF&ForceDownload=true
https://www.oge.com/documents/d/portal/oge-2026-irp-final`
  - Status Detail: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AeNgrdQLsFw5W8dEEwRTc%C3%81pApsum6Hqboy8ro%C3%81CyJ8OFtu0HRxDmnOy6W2%C3%81nwK2s%C3%81raDCV3qK%C3%8912Ie4gZNs%C3%89Vd0%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Status Detail: https://www.oge.com/documents/d/portal/oge-2026-irp-final (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Oklahoma Department of Environmental Quality application says first fire occurred on November 26, 2025. The 2026 plan gives March 2026 for service.

### G100001092967 / Tinker Air Force Base power station / 5A-5B
*change to an existing unit*
**Action:** Leave Status of unit 5A-5B (G100001092967) as retired. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `retired` -> `retired`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: OG&E's 2026 integrated resource plan says units 5A and 5B retired in early 2026. The EIA-860M table for September 2026 still lists them as out of service and not expected to return. This matches GEM's retired status. The units retired in early 2026 per OG&E. No month was found.

### G100000403435 / Weleetka power station / 4
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Planned retire of unit 4 (G100000403435) as 2030. It is still correct. Add the 2 links below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `2030` -> `2030`
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
  - Planned Retire Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 integrated resource plan refresh from PSO (Public Service Company of Oklahoma) lists Weleetka units 4 and 5 for retirement in 2030, and the EIA-860M table for September 2026 gives planned retirement year 2030. This matches the tracker. No new scheduled event is needed. The plan is at https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf.

### G100000403436 / Weleetka power station / 5
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Planned retire of unit 5 (G100000403436) as 2030. It is still correct. Add the 2 links below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `2030` -> `2030`
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
  - Planned Retire Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 integrated resource plan refresh from PSO (Public Service Company of Oklahoma) lists Weleetka units 4 and 5 for retirement in 2030, and the EIA-860M table for September 2026 gives planned retirement year 2030. This matches the tracker. No new scheduled event is needed. The plan is at https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf.

### Anadarko power station
*question about existing data; checklist rows 50 (Other last-minute status changes checked)*
- about: Status
- question: Does EIP's under construction status for Anadarko describe the new Roulet units rather than the retired unit 3?
- finding: GEM lists unit 3 as retired and units 12 and 13 as the Roulet units under construction for 2026. The federal file shows Anadarko plant units 1, 2 and 3 retired in 2024. Units 1 and 2 are 17.3 MW each and are below the threshold.
- recommendation: Keep unit 3 as retired and the Roulet units as under construction. Treat EIP's status as describing the Roulet units.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- notes: The EIP page loads only through a script and could not be read as text. The match between EIP's under construction status and the Roulet units is an inference.

### G100001101631 / Bristow Energy Center / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 19 (Missing or unknown owner searched)*
- about: Owner(s)
- question: Is the blank owner in the task right, since the database shows Associated Electric?
- finding: The database already shows Associated Electric Cooperative Inc at 100 percent. The Associated page at https://www.aeci.org/bristow-energy-center-1 says the cooperative is building the plant, and the Siemens story at https://www.siemens-energy.com/global/en/home/stories/gas-turbine-peaker-oklahoma-us.html calls it Associated's plant.
- recommendation: Leave the owner as it is. Leave the operator blank until a document names one.
  - links: https://www.aeci.org/bristow-energy-center-1 (ok=None, contains_value=None)
  - links: https://www.siemens-energy.com/global/en/home/stories/gas-turbine-peaker-oklahoma-us.html (ok=None, contains_value=None)
- notes: No project company was found.

### Comanche (OK) power station
*question about existing data; checklist rows 50 (Other last-minute status changes checked)*
- about: Status
- question: Do federal generators 2G1, 2S1, 3G1 and 3S1 belong to GEM units CC2 and CC3?
- finding: GEM lists CC2 and CC3 at 686.4 MW each, pre-construction, 2029. The federal file lists 2G1 at 408.8 MW and 2S1 at 277.6 MW, then 3G1 and 3S1 with the same sizes, planned for 2029 with approvals not started.
- recommendation: Treat 2G1 and 2S1 as CC2, and 3G1 and 3S1 as CC3, since the sums of 686.4 MW agree. Consider setting the status to announced if no permit was filed.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- notes: The federal file says regulatory approvals have not started. GEM says pre-construction. No permit filing was found in this pass.

### G100001101686 / Comanche (OK) power station / CC2
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- about: Capacity (MW)
- question: What capacity should each new Comanche block carry?
- finding: GEM and the EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx show 686.4 MW per block. The Southwest Power Pool queue at https://opsportal.spp.org/Studies/GIActive shows 775.2 MW for each of the two queue entries ERAS-2025-024 and ERAS-2025-026. The air permit application at https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true says each block will produce 633 MW.
- recommendation: Leave 686.4 MW, which is EIA's nameplate figure. Ask the project manager whether the larger queue figure should be used because it may include duct burner output.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true (ok=None, contains_value=None)
  - links: https://opsportal.spp.org/Studies/GIActive (ok=None, contains_value=None)
- notes: The queue figure may be the interconnection request and not the nameplate. The permit figure is a total output at one set of site conditions. I did not find a document that gives the nameplate in plain terms.

### G100001101687 / Comanche (OK) power station / CC3
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- about: Capacity (MW)
- question: What capacity should each new Comanche block carry?
- finding: GEM and the EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx show 686.4 MW per block. The Southwest Power Pool queue at https://opsportal.spp.org/Studies/GIActive shows 775.2 MW for each of the two queue entries ERAS-2025-024 and ERAS-2025-026. The air permit application at https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true says each block will produce 633 MW.
- recommendation: Leave 686.4 MW, which is EIA's nameplate figure. Ask the project manager whether the larger queue figure should be used because it may include duct burner output.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ATdpa%C3%81tiBf6AUlxodMaTf4RyyKtRvO65cbkkb3aVZbN4JAjNn88hU2pksW3d3Ngw9ZE27%C3%81UOLoThr916JdkRs9c%3D/?ViewerMode=PDF&ForceDownload=true (ok=None, contains_value=None)
  - links: https://opsportal.spp.org/Studies/GIActive (ok=None, contains_value=None)
- notes: The queue figure may be the interconnection request and not the nameplate. The permit figure is a total output at one set of site conditions. I did not find a document that gives the nameplate in plain terms.

### Horseshoe Lake power station
*question about existing data*
- about: Start year
- question: Should Horseshoe Lake unit 15 start in 2030 instead of 2031?
- finding: SPP request ERAS-2025-004 is a 756.2 MW combined cycle request at Horseshoe Lake 138 kilovolt with a fully executed agreement and commercial operation on October 3, 2030. GEM has unit 15 at 755 MW, pre-construction, due 2031.
- recommendation: Keep 2031 only if the OG&E plan or order says so, otherwise change the start year to 2030 and add SPP ERAS-2025-004 to Other IDs.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- notes: The size matches within rounding. Only the year differs.

### Horseshoe Lake power station
*question about existing data; checklist rows 50 (Other last-minute status changes checked)*
- about: Status
- question: Are Horseshoe Lake units 10, 11 and 12 operating, as in GEM, or proposed or under construction, as other sources say?
- finding: The federal file shows unit 10 as operating since 2001 at 60.5 MW, so EIP's proposed status for unit 10 is likely about the new units. Units 11 and 12 are listed as construction complete but not yet in commercial operation, planned for 2026. Units 13 and 14 at 224 MW each are approved but not under construction, planned for 2029.
- recommendation: Keep unit 10 as operating and change units 11 and 12 to construction until a document shows commercial operation. Units 13 and 14 match GEM.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - links: https://www.okenergytoday.com/2025/11/oge-acts-promptly-on-energy-projects-approval (ok=True, contains_value=True)
- notes: A November 2025 story says the state commission approved 448 MW at Horseshoe Lake for OG&E. A status change needs two independent publishers for high confidence, and only the federal file gives the current state. Federal generator ids 13 and 14 belong to GEM units 13 and 14.

### G100001092969 / Horseshoe Lake power station / 13
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
- about: Start year
- question: How do SPP queue dates ERAS-2025-010 and GEN-2024-GR1 fit units 13 and 14?
- finding: The Southwest Power Pool queue at https://opsportal.spp.org/Studies/GIActive lists ERAS-2025-010, a 496 MW combustion turbine at the Horseshoe Lake substation with an in-service date of April 2028, and GEN-2024-GR1, 492 MW. OG&E and EIA say units 13 and 14 start in 2029.
- recommendation: Leave the start year at 2029. The queue entries are about 496 MW, close to two 224 MW units plus margin.
- notes: I did not open the 2025 commission docket orders to check for an earlier date, because the call summary and EIA both say 2029 or later.

### G100001101622 / Horseshoe Lake power station / 15
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
- about: Start year
- question: Is unit 15 a 2031 start, or is queue entry ERAS-2025-004 for 2029 the same project?
- finding: The October 28, 2026 call at https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ says unit 15 is 755 MW and enters service in 2031. The Southwest Power Pool queue at https://opsportal.spp.org/Studies/GIActive lists ERAS-2025-004, a 756.2 MW combined cycle at the same substation dated April 2029.
- recommendation: Keep 2031 from the owner's statement and treat the queue entry as the same project with an earlier placeholder date.
  - links: https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ (ok=None, contains_value=None)
- notes: The queue is a lead only.

### G100001101620 / Hugo power station / Site B
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- about: Capacity (MW)
- question: Should Site B be 372 MW as in the Southwest Power Pool queue, not 342 MW?
- finding: The Southwest Power Pool queue entry GEN-2024-323 (https://opsportal.spp.org/Studies/GIActive) lists 372 MW for the Hugo project at the ITC Hugo 7 345 kV substation. The database has 342 MW from six SGT-800 turbines. A Construction Review article (https://constructionreviewonline.com/1b-hugo-plant-expansion-western-farmers-electric-breaks-ground-on-nine-gas-turbines-in-oklahoma/) says the nine turbines add about 400 MW, and a cooperative annual report says 404 MW.
- recommendation: Leave 342 MW as it is, since queue sizes often include extra margin. The total of 415.5 MW for both sites is close to the 404 MW to 415 MW reported.
  - links: https://constructionreviewonline.com/1b-hugo-plant-expansion-western-farmers-electric-breaks-ground-on-nine-gas-turbines-in-oklahoma/ (ok=None, contains_value=None)
- notes: I read the Southwest Power Pool open queue list on 5 November 2026 (https://opsportal.spp.org/Studies/GenerateActiveCSV). Entry GEN-2024-323 shows a nameplate of 372 MW and a capacity of 356.8 MW, with commercial operation in May 2029. Site A is 73.5 MW in the database and entry GEN-2026-SR34 shows 75 MW, owned by the cooperative, at the Hugo 138 kV substation, with commercial operation in April 2029.

### G100001091053 / Muskogee Data Center power station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only)), 49 (Construction to operating checked)*
- about: Capacity (MW)
- question: Should capacity be 324 MW, summed from the newest draft permit?
- finding: The database shows 283.1 MW from the earlier fleet of 102 engines. The September 2026 draft permit (https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ae6Ctfv7oSCmhMZ%C3%89kDp%C3%89JKeyyrF%C3%897NeqHWN6Fd0wYTdl604KTTG6bsIhnFC9Sgq7vhd656jR%C3%895uQBkEpWYOBnMg%3D/?ViewerMode=PDF&ForceDownload=true) lists 105 engines, with the MTU units now at 3,250 kW each. My sum of the permit ratings is about 324 MW.
- recommendation: Change Capacity to 324.0 once the permit is final, or now if you accept a sum of the draft's ratings. The earlier figure used 3.49 MW per MTU engine, which is the engine rating, not the generator rating.
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ae6Ctfv7oSCmhMZ%C3%89kDp%C3%89JKeyyrF%C3%897NeqHWN6Fd0wYTdl604KTTG6bsIhnFC9Sgq7vhd656jR%C3%895uQBkEpWYOBnMg%3D/?ViewerMode=PDF&ForceDownload=true (ok=None, contains_value=None)
- notes: I read the Southwest Power Pool open queue list on 5 November 2026 (https://opsportal.spp.org/Studies/GenerateActiveCSV). Entry GEN-2025-SR9 is 400 MW with no fuel shown, owned by OG&E, at the Muskogee 345 kV substation, with commercial operation in December 2029. Entry GEN-2024-293 is 248 MW of gas at the same substation name, with commercial operation in May 2033. Both are grid interconnection requests with no site address, and neither names this data center. They are added as separate projects, not as this plant's backup fleet. The permit has not been issued yet, so numbers could still change.

### Muskogee Generating Station
*question about existing data; checklist rows 50 (Other last-minute status changes checked)*
- about: Status
- question: Should Muskogee units 4 and 5 keep the start year 2019, or change to the federal file's 1977 and 1978?
- finding: GEM uses two rows for each unit and gives the gas conversion year of 2019 for the second row. The federal file gives 1977 and 1978 for natural gas steam turbines of 572 MW.
- recommendation: Keep 2019 for the converted rows. The federal file shows the original start years, which GEM already holds in the first row of each unit.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- notes: No change is needed. This follows GEM's convention for coal-to-gas conversions.

### Mustang (OK) power station
*watch item at an existing plant*
- what to watch: A 100 MW special study at the Mustang substation names no fuel or generator yet.
- check again by: 2027-03
- notes: SPP GEN-2025-SR23, interconnection agreement executed, on schedule.

### Northeastern Station
*question about existing data; checklist rows 50 (Other last-minute status changes checked)*
- about: Status
- question: Is Northeastern unit 3 operating on gas as in GEM, or still coal as in the federal file?
- finding: GEM lists unit 3 as converted to gas and operating from 2026. The federal file for September 2026 still lists generator 3 as conventional steam coal at 473 MW. Public Service Company of Oklahoma told the state in October 2025 that it would stop burning coal on December 31, 2025 and run unit 3 on gas from 2026.
- recommendation: Keep unit 3 as operating on gas if a document confirms the conversion is done. Otherwise note the planned conversion date.
  - links: https://docs.aep.com/docs/requiredpostings/elg/NEPSB-AnnualProgressReportforthePermanentCessationofCoalCombustionby12-31-2028-10102025.pdf (ok=True, contains_value=True)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- notes: The utility's annual report to the state environmental agency says coal burning would end at the end of 2025. It also says a required filing with the Southwest Power Pool was still pending. EIP lists this unit as proposed, which fits the new units 5 and 6 at 225 MW that GEM has as pre-construction for 2028.

### G100001101665 / Northeastern Station / Unit 5
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
- about: Capacity (MW)
- question: Should Units 5 and 6 be 229 MW each instead of 225 MW?
- finding: The Oklahoma Department of Environmental Quality draft permit memo from September 2026 (https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AWtoGCCMAPa3ZmzV9bv2lNVdjzgKUd4GV4oRCuMNP0goK6NykmHJHyG5WSO1mUZe7mM1J5HwOpKpJWodbQLKNmw%3D/?ViewerMode=PDF&ForceDownload=true) lists two 229 MW GE turbines. The permit application from late 2025 said 222 MW each. The AEP report says 450 MW in total.
- recommendation: Leave 225 MW on both units, since 450 MW in total matches the AEP report. Change to 229 only if you prefer the permit figure.
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AWtoGCCMAPa3ZmzV9bv2lNVdjzgKUd4GV4oRCuMNP0goK6NykmHJHyG5WSO1mUZe7mM1J5HwOpKpJWodbQLKNmw%3D/?ViewerMode=PDF&ForceDownload=true (ok=None, contains_value=None)
  - links: https://www.sec.gov/Archives/edgar/data/4904/000000490426000059/aep-20260630.htm (ok=None, contains_value=None)
- notes: The Southwest Power Pool entry ERAS-2025-023 at https://opsportal.spp.org/Studies/GIActive is a single combustion turbine of 513 MW nameplate and 510 MW capacity at the Northeastern 345 kV substation, with commercial operation in December 2029 in the open list at https://opsportal.spp.org/Studies/GenerateActiveCSV, read on 5 November 2026. It does not match two 229 MW turbines due by the end of 2028. The same Oklahoma Department of Environmental Quality permit file also describes a separate large turbine of nominal 453 MW at Northeastern (https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AS0IjaCrV1T%C3%81SEUDdXmwkZpG2VRBClzAKR911pep%C3%81uAtGhYCcgV7UJnH1xPqDg4ZbOaSJTShXSL302lcWYvl9ds%3D/?ViewerMode=PDF&ForceDownload=true). The permit and the AEP report describe two turbines for Units 5 and 6.

### G100001101715 / Project Thunderbird Data Center power station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only)), 50 (Other last-minute status changes checked)*
- about: Status
- question: Does pre-construction fit Project Thunderbird before any air permit exists?
- finding: No air permit application, commission filing or queue entry was found. The only documents are news reports of a rezoning request that was delayed in September 2026 (https://okcfox.com/news/local/project-thunderbird-data-center-proposal-promises-600-jobs-and-self-generated-power).
- recommendation: Change status to announced unless a permit application or land purchase is found. Ask the reviewer to check the Garfield County and Enid records.
  - links: https://okcfox.com/news/local/project-thunderbird-data-center-proposal-promises-600-jobs-and-self-generated-power (ok=None, contains_value=None)
- notes: The ODEQ permit harvest matched nothing. An air permit may have been requested under a different name.

### G100001028184 / Ripley Energy Center power station / RP1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
- about: Capacity (MW)
- question: Should Ripley RP1 capacity change from 445 MW to 419 MW?
- finding: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) gives 419.0 MW nameplate and 444.5 MW net winter. The state permit memorandum (https://applications.deq.ok.gov/permitspublic/storedpermits/8877.pdf) gives a nominal gross output of 420 MW.
- recommendation: Change capacity to 419 MW, the nameplate figure, because the manual wants nameplate and not winter capability.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/8877.pdf (ok=None, contains_value=None)
- notes: The old Associated Electric Cooperative page could not be read, so I could not see why 445 was used. It likely came from the winter figure. A second check of the plan found: GEM gives 445 MW, under construction for 2027. The federal file for September 2026 gives 419 MW, under construction, more than half complete. Look for the cooperative's own figure before changing GEM. Keep 445 MW until a document names the nameplate.

### G100001092967 / Tinker Air Force Base power station / 5A-5B
*question about existing data; checklist rows 50 (Other last-minute status changes checked)*
- about: Status
- question: Should units 5A and 5B stay retired although EIA lists them out of service?
- finding: OG&E's 2026 plan (https://www.oge.com/documents/d/portal/oge-2026-irp-final) says they retired in early 2026. The EIA table for September 2026 still shows out of service, not retired, and gives no retirement date.
- recommendation: Leave as retired in 2026. Check the EIA table again after its next release on November 24, 2026.
  - links: https://www.oge.com/documents/d/portal/oge-2026-irp-final (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: EIA often lags a retirement by several months.

### Tulsa power station
*watch item at an existing plant*
- what to watch: Southwest Power Pool request GEN-2025-SR21 (100 MW, fuel not shown) connects at the Tulsa Power Station 138 kV substation.
- check again by: 2027-03
- notes: No document names a generating unit or fuel.

## Checklist group 4. Conversions

Coal-to-gas and other conversions: unit naming, fuel and technology, replacement links.

### G100001017849 / Muskogee Generating Station / Unit 4, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 4, timepoint 2 (G100001017849) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/4454.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Oklahoma Department of Environmental Quality permit memo from June 2018 at https://applications.deq.ok.gov/permitspublic/storedpermits/4454.pdf says permit 2005-271-C, issued February 27, 2017, converts Units 4 and 5 from coal to natural gas.

### G100001017850 / Muskogee Generating Station / Unit 5, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 5, timepoint 2 (G100001017850) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/4454.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Oklahoma Department of Environmental Quality permit memo from June 2018 at https://applications.deq.ok.gov/permitspublic/storedpermits/4454.pdf says permit 2005-271-C, issued February 27, 2017, converts Units 4 and 5 from coal to natural gas.

### G100001055294 / Northeastern Station / Unit 3, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 3, timepoint 2 (G100001055294) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.sec.gov/Archives/edgar/data/4904/000000490426000059/aep-20260630.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The AEP report says PSO retired 325 million dollars of coal-related assets at Unit 3 in the first quarter of 2026 and began running it on gas. That describes a coal to gas conversion.

## Checklist group 5. Turbine make and model

Equipment manufacturer and model, especially on units in development.

### G100000401931 / Redbud power plant / G112
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit G112 (G100000401931) to GE 7FA. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE 7FA`
  - Turbine/Engine Equipment Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: An Oklahoma Department of Environmental Quality permit memorandum, read in May 2025, lists four General Electric Model 7FA combustion turbines at the Redbud plant (https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf). The EIA-860M table for September 2026 lists generators CT01 and ST01 as operating, so the unit is still operating. No retirement, mothballing or owner change was found. I found no document that states a Backup Power value for this unit.

### G100000401932 / Redbud power plant / G113
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit G113 (G100000401932) to GE 7FA. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE 7FA`
  - Turbine/Engine Equipment Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: An Oklahoma Department of Environmental Quality permit memorandum, read in May 2025, lists four General Electric Model 7FA combustion turbines at the Redbud plant (https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf). The EIA-860M table for September 2026 lists generators CT02 and ST02 as operating, so the unit is still operating. No retirement, mothballing or owner change was found. I found no document that states a Backup Power value for this unit.

### G100000401933 / Redbud power plant / G114
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit G114 (G100000401933) to GE 7FA. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE 7FA`
  - Turbine/Engine Equipment Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: An Oklahoma Department of Environmental Quality permit memorandum, read in May 2025, lists four General Electric Model 7FA combustion turbines at the Redbud plant (https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf). The EIA-860M table for September 2026 lists generators CT03 and ST03 as operating, so the unit is still operating. No retirement, mothballing or owner change was found. I found no document that states a Backup Power value for this unit.

### G100000401934 / Redbud power plant / G115
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit G115 (G100000401934) to GE 7FA. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE 7FA`
  - Turbine/Engine Equipment Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: An Oklahoma Department of Environmental Quality permit memorandum, read in May 2025, lists four General Electric Model 7FA combustion turbines at the Redbud plant (https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf). The EIA-860M table for September 2026 lists generators CT04 and ST04 as operating, so the unit is still operating. No retirement, mothballing or owner change was found. I found no document that states a Backup Power value for this unit.

### G100001072817 / Tinker Air Force Base power station / 1-2
*change to an existing unit*
**Action:** Leave Equipment Manufacturer/Model of unit 1-2 (G100001072817) as GE Vernova: LM6000. It is still correct. Add the 2 links below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `GE Vernova: LM6000` -> `GE Vernova: LM6000`
  - Turbine/Engine Equipment Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AeNgrdQLsFw5W8dEEwRTc%C3%81pApsum6Hqboy8ro%C3%81CyJ8OFtu0HRxDmnOy6W2%C3%81nwK2s%C3%81raDCV3qK%C3%8912Ie4gZNs%C3%89Vd0%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Turbine/Engine Equipment Data Source: https://www.oge.com/documents/d/portal/oge-2026-irp-final (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: An application to the Oklahoma Department of Environmental Quality names two new GE LM6000 PC Sprint gas-fired simple-cycle turbines. OG&E's 2026 plan says two identical GE LM6000 turbines. This matches GEM.

## Checklist group 6. Owners and entities

Owner, operator and parent changes, and new owners or operators to create.

### G100000403749 / Anadarko power station / 4
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4 (G100000403749) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 3006, generator 4, as operating, 105.1 MW, natural gas combined cycle, in service 1977, with no planned retirement date. I found no retirement, mothballing or owner change in the August 2026 air permit documents either. Unit 4 is still operating per EIA with no planned retirement. I found no document that states a Backup Power value.

### G100000403750 / Anadarko power station / 5
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 5 (G100000403750) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 3006, generator 5, as operating, 105.1 MW, natural gas combined cycle, in service 1977, with no planned retirement date. I found no retirement, mothballing or owner change in the August 2026 air permit documents either. Unit 5 is still operating per EIA with no planned retirement. I found no document that states a Backup Power value.

### G100000403751 / Anadarko power station / 6
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 6 (G100000403751) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 3006, generator 6, as operating, 105.1 MW, natural gas combined cycle, in service 1977, with no planned retirement date. I found no retirement, mothballing or owner change in the August 2026 air permit documents either. Unit 6 is still operating per EIA with no planned retirement. I found no document that states a Backup Power value.

### G100000403322 / Charles D. Lamb energy center / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100000403322) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026) lists this unit as operating with no planned retirement year. Plant 58325, generator 1, status OP, nameplate 122.0 MW, natural gas combustion turbine, operating April 2015, no planned retirement year. The file shows no retirement, mothballing or change of status. The unit is still operating and no retirement is planned in the EIA table. I found no document that states a backup power value for this unit, so the current value was left alone.

### G100000402169 / Chouteau power station / CC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC1 (G100000402169) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026) lists this unit as operating with no planned retirement year. Plant 7757, generators 1, 2 and 3, status OP, nameplate 176.0, 176.0 and 182.8 MW, combined cycle, operating January 2000, no planned retirement year. The file shows no retirement, mothballing or change of status. The unit is still operating and no retirement is planned in the EIA table. I found no document that states a backup power value for this unit, so the current value was left alone.

### G100000402170 / Chouteau power station / CC2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC2 (G100000402170) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026) lists this unit as operating with no planned retirement year. Plant 7757, generators 4, 5 and 6, status OP, nameplate 176.0, 176.0 and 182.8 MW, combined cycle, operating June 2011, no planned retirement year. The file shows no retirement, mothballing or change of status. The unit is still operating and no retirement is planned in the EIA table. I found no document that states a backup power value for this unit, so the current value was left alone.

### G100000402193 / Comanche (OK) power station / CC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC1 (G100000402193) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists plant 8059, generators 1G1 and 1G2 at 85.0 MW each and 1S at 120.0 MW, all operating, with no retirement date. I found no mothballing or change of owner. The unit is still operating in the EIA table for September 2026. I found no retirement notice, mothballing or sale. The 2035 planned retirement comes from the company's 2026 resource plan refresh.

### G100000402193 / Comanche (OK) power station / CC1
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit CC1 (G100000402193) to 2035. The box is empty now. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `` -> `2035`
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Public Service Company of Oklahoma's 2026 integrated resource plan refresh at https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf lists Comanche 1G1, 1G2 and 1S with a retirement date of 2035 in its table of current resources on page 18. Page 11 says the retirement happens by summer planning year 2036. The reviewer adds a new scheduled retirement event for 2035 with Source Year 2026.

### G100000401716 / Frontier power station / CC01
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC01 (G100000401716) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026) lists this unit as operating with no planned retirement year. Plant 50558, generators GT01 and ST01, status OP, nameplate 87.2 and 44.2 MW, combined cycle, operating September 1989, no planned retirement year. The file shows no retirement, mothballing or change of status. The unit is still operating and no retirement is planned in the EIA table. I found no document that states a backup power value for this unit, so the current value was left alone.

### G100000401815 / Green Country Energy power station / G841
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit G841 (G100000401815) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (plant 55146) lists generators CTG1 and STG1 as operating, natural gas fired combined cycle. It shows no retirement date and no planned retirement. This matches the current value. Still operating per the September 2026 EIA table. No retirement, mothballing or planned retirement found. I found no document that states a Backup Power value for this unit. The EIA table has no such field.

### G100000401816 / Green Country Energy power station / G842
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit G842 (G100000401816) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (plant 55146) lists generators CTG2 and STG2 as operating, natural gas fired combined cycle. It shows no retirement date and no planned retirement. This matches the current value. Still operating per the September 2026 EIA table. No retirement, mothballing or planned retirement found. I found no document that states a Backup Power value for this unit. The EIA table has no such field.

### G100000401817 / Green Country Energy power station / G843
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit G843 (G100000401817) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (plant 55146) lists generators CTG3 and STG3 as operating, natural gas fired combined cycle. It shows no retirement date and no planned retirement. This matches the current value. Still operating per the September 2026 EIA table. No retirement, mothballing or planned retirement found. I found no document that states a Backup Power value for this unit. The EIA table has no such field.

### G100000401944 / Kiamichi energy facility / STG1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit STG1 (G100000401944) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (plant 55501) lists CTG1 and CTG2 and STG1 as operating, natural gas fired combined cycle. It shows no retirement. Still operating per the September 2026 EIA table. No retirement, mothballing or sale found. I found no document that states a Backup Power value.

### G100000401945 / Kiamichi energy facility / STG2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit STG2 (G100000401945) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (plant 55501) lists CTG3 and CTG4 and STG2 as operating, natural gas fired combined cycle. It shows no retirement. Still operating per the September 2026 EIA table. No retirement, mothballing or sale found. I found no document that states a Backup Power value.

### G100000401929 / McClain energy facility / G011
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit G011 (G100000401929) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists plant 55457, generators CT1, CT2 and ST1, as operating, all with an operating date of June 2001. No retirement, planned retirement or mothballing is shown. The Oklahoma Department of Environmental Quality permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8740.pdf also describes the two combustion turbines and the steam turbine as the plant's combined cycle, with a Title V operating permit renewal requested. The unit is still operating. No retirement, mothballing or owner change was found in the EIA table or the permit memo. The queue entries named in the brief are new projects and are not this unit.

### G100000403752 / Mooreland power station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000403752) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists plant 3008, generator 2, as operating since July 1968. No retirement or planned retirement is shown. The Oklahoma Department of Environmental Quality permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8994.pdf says the three boilers burn natural gas and run as peaking units. The unit is still operating. No retirement, mothballing or owner change was found.

### G100000403753 / Mooreland power station / 3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 3 (G100000403753) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists plant 3008, generator 3, as operating since July 1975. No retirement or planned retirement is shown. The Oklahoma Department of Environmental Quality permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8994.pdf says the three boilers burn natural gas and run as peaking units. The unit is still operating. No retirement, mothballing or owner change was found.

### G100001017849 / Muskogee Generating Station / Unit 4, timepoint 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 4, timepoint 2 (G100001017849) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists plant 2952, generator 4, as operating natural gas steam. No retirement or planned retirement is shown. An Oklahoma Department of Environmental Quality permit memo from November 2021 at https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf says the station burns natural gas and sub-bituminous coal. The unit is still operating. EIA gives 1977 as the operating year of the original coal unit. GEM uses the conversion year 2019, which was not confirmed in a document I could read.

### G100001017850 / Muskogee Generating Station / Unit 5, timepoint 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 5, timepoint 2 (G100001017850) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists plant 2952, generator 5, as operating natural gas steam. No retirement or planned retirement is shown. An Oklahoma Department of Environmental Quality permit memo from November 2021 at https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf says the station burns natural gas and sub-bituminous coal. The unit is still operating. EIA gives 1978 as the operating year of the original coal unit. GEM uses the conversion year 2019, which was not confirmed in a document I could read.

### G100000403312 / Mustang (OK) power station / 6-12
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 6-12 (G100000403312) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
  - Status Data Source: https://oklahoma.gov/content/dam/ok/en/occ/documents/pu/pud-reports-page/2025-oge-irp.pdf (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (plant 2953, generators GT1 to GT7) lists all seven turbines as operating. The 2025 resource plan at https://oklahoma.gov/content/dam/ok/en/occ/documents/pu/pud-reports-page/2025-oge-irp.pdf lists Mustang 6 to 12 as existing. No retirement, mothballing or ownership change was found. The row stands for seven 66 MW turbines. EIA shows operating dates between September and December 2017 while GEM has 2018, which matches the resource plan year, so I left the start year alone.

### G100000403423 / Northeastern Station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000403423) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists generator 2 as a natural gas steam turbine of 473.0 MW at Northeastern, plant 2963, in its Operating sheet. No retirement, planned retirement or mothballing is shown. I read the matching row in the file myself. Still operating in the September 2026 EIA table. No retirement or owner change found. No document states backup power.

### G100000401657 / Northeastern Station / NE1S
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit NE1S (G100000401657) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists generators 1, 1A and 1B as a natural gas combined cycle at Northeastern, plant 2963, in its Operating sheet. No retirement, planned retirement or mothballing is shown. I read the matching row in the file myself. Still operating in the September 2026 EIA table. No retirement or owner change found. No document states backup power.

### G100000401851 / Oneta energy center / BLK1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit BLK1 (G100000401851) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (plant 55225, CTG1, CTG2 and STG1) lists this block as operating. It lists a planned uprate of 17 MW per turbine in 2027 or 2028, but no retirement. The Oklahoma Department of Environmental Quality permit memo from August 2021 at https://applications.deq.ok.gov/permitspublic/storedpermits/8041.pdf describes four gas turbines. The PSO 2026 resource plan at https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf lists Oneta as contracted capacity of 260 MW through 2031, which is a contract end and not a plant retirement. No retirement, mothballing or sale was found. A web search showed an older sale to Argo Infrastructure Partners but no 2026 transaction, and GEM already shows Oneta Power LLC as owner.

### G100000401852 / Oneta energy center / BLK2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit BLK2 (G100000401852) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (plant 55225, CTG3, CTG4 and STG2) lists this block as operating. It lists a planned uprate of 17 MW per turbine in 2027 or 2028, but no retirement. The Oklahoma Department of Environmental Quality permit memo from August 2021 at https://applications.deq.ok.gov/permitspublic/storedpermits/8041.pdf describes four gas turbines. The PSO 2026 resource plan at https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf lists Oneta as contracted capacity of 260 MW through 2031, which is a contract end and not a plant retirement. No retirement, mothballing or sale was found. A web search showed an older sale to Argo Infrastructure Partners but no 2026 transaction, and GEM already shows Oneta Power LLC as owner.

### G100000403323 / Ponca City power station / 4
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4 (G100000403323) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (plant 7546) lists generator 4, 60.5 MW, combustion turbine, 2003 as operating with no planned retirement. The permit memo from April 2019 at https://applications.deq.ok.gov/permitspublic/storedpermits/4608.pdf shows no retirement plan. No sale or mothballing was found in a web search. No retirement, mothballing or owner change was found.

### G100000402159 / Ponca City power station / CC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC1 (G100000402159) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (plant 7546) lists generators 1 and 3, 19.8 MW steam and 54.0 MW turbine, combined cycle, 1995 as operating with no planned retirement. The permit memo from April 2019 at https://applications.deq.ok.gov/permitspublic/storedpermits/4608.pdf shows no retirement plan. No sale or mothballing was found in a web search. No retirement, mothballing or owner change was found. The permit memo says unit 3 can also burn fuel oil, which GEM does not list.

### G100000403424 / Riverside (OK) power station / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100000403424) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists plant 4940, generator 1, status operating, nameplate 473.0 MW, operating year 1974, and no planned retirement date. This re-verifies the current status. No retirement, mothballing or owner change was found. Still operating in the September 2026 EIA table. I found no document that states a Backup Power value. The EIA table and the resource plan do not address it, so the current value of no stays without a source.

### G100000403424 / Riverside (OK) power station / 1
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit 1 (G100000403424) to 2041. The box is empty now. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `` -> `2041`
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Public Service Company of Oklahoma 2026 resource plan refresh at https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf lists Riverside 1 as existing capacity with a retirement year of 2041. The human adds a new scheduled retirement event for 2041. The EIA table shows no planned retirement.

### G100000403425 / Riverside (OK) power station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000403425) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists plant 4940, generator 2, status operating, nameplate 473.0 MW, operating year 1976, and no planned retirement date. This re-verifies the current status. No retirement, mothballing or owner change was found. Still operating in the September 2026 EIA table. I found no document that states a Backup Power value. The EIA table and the resource plan do not address it, so the current value of no stays without a source.

### G100000403425 / Riverside (OK) power station / 2
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit 2 (G100000403425) to 2041. The box is empty now. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `` -> `2041`
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Public Service Company of Oklahoma 2026 resource plan refresh at https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf lists Riverside 2 as existing capacity with a retirement year of 2041. The human adds a new scheduled retirement event for 2041. The EIA table shows no planned retirement.

### G100000403426 / Riverside (OK) power station / 3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 3 (G100000403426) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists plant 4940, generator 3, status operating, nameplate 86.5 MW, operating year 2008, and no planned retirement date. This re-verifies the current status. No retirement, mothballing or owner change was found. Still operating in the September 2026 EIA table. I found no document that states a Backup Power value. The EIA table and the resource plan do not address it, so the current value of no stays without a source.

### G100000403426 / Riverside (OK) power station / 3
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit 3 (G100000403426) to 2056. The box is empty now. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `` -> `2056`
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Public Service Company of Oklahoma 2026 resource plan refresh at https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf lists Riverside 3 as existing capacity with a retirement year of 2056. The human adds a new scheduled retirement event for 2056. The EIA table shows no planned retirement.

### G100000403427 / Riverside (OK) power station / 4
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4 (G100000403427) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists plant 4940, generator 4, status operating, nameplate 86.5 MW, operating year 2008, and no planned retirement date. This re-verifies the current status. No retirement, mothballing or owner change was found. Still operating in the September 2026 EIA table. I found no document that states a Backup Power value. The EIA table and the resource plan do not address it, so the current value of no stays without a source.

### G100000403427 / Riverside (OK) power station / 4
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit 4 (G100000403427) to 2056. The box is empty now. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `` -> `2056`
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Public Service Company of Oklahoma 2026 resource plan refresh at https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf lists Riverside 4 as existing capacity with a retirement year of 2056. The human adds a new scheduled retirement event for 2056. The EIA table shows no planned retirement.

### G100000403319 / Seminole (OK) power station / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100000403319) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists this unit as operating. Row: Plant 2956, generator 1, status operating, nameplate 567.0 MW, operating year 1971. This confirms the status; it does not change it. The EIA table for September 2026 and the 2026 OG&E plan both show unit 1 operating with retirement planned for early 2031. I found no document that states a Backup Power value for this unit. It is a large steam unit that serves the grid, and no source says otherwise.

### G100000403320 / Seminole (OK) power station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000403320) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists this unit as operating. Row: Plant 2956, generator 2, status operating, nameplate 567.0 MW, operating year 1973. This confirms the status; it does not change it. The EIA table for September 2026 and the 2026 OG&E plan both show unit 2 operating with retirement planned for early 2033. I found no document that states a Backup Power value for this unit. It is a large steam unit that serves the grid, and no source says otherwise.

### G100000403321 / Seminole (OK) power station / 3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 3 (G100000403321) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists this unit as operating. Row: Plant 2956, generator 3, status operating, nameplate 567.0 MW, operating year 1975. This confirms the status; it does not change it. The EIA table for September 2026 and the 2026 OG&E plan both show unit 3 operating with retirement planned for early 2035. I found no document that states a Backup Power value for this unit. It is a large steam unit that serves the grid, and no source says otherwise.

### G100000403428 / Southwestern power station / 1
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit 1 (G100000403428) to 2030. The box is empty now. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `` -> `2030`
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 Public Service Company of Oklahoma resource plan refresh at https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf lists Southwestern 1 (gas, in service 1952) with a retirement year of 2030. The human adds a new scheduled retirement event for 2030 and does not change an existing one. The EIA-860M table for September 2026 (released October 23, 2026) at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists Southwestern generator 1 as operating, 84.0 MW nameplate, natural gas, in service 1952. No planned retirement is listed there. I found no document that states whether this unit is backup power, so Backup Power stays as it is.

### G100000403429 / Southwestern power station / 2
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit 2 (G100000403429) to 2030. The box is empty now. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `` -> `2030`
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 Public Service Company of Oklahoma resource plan refresh at https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf lists Southwestern 2 (gas, in service 1954) with a retirement year of 2030. The human adds a new scheduled retirement event for 2030 and does not change an existing one. The EIA-860M table for September 2026 (released October 23, 2026) at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists Southwestern generator 2 as operating, 84.0 MW nameplate, natural gas, in service 1954. No planned retirement is listed there. I found no document that states whether this unit is backup power, so Backup Power stays as it is.

### G100000402873 / Spring Creek energy center / CT01
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CT01 (G100000402873) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55651 generator CT01 as operating with no retirement date. So I found no retirement, mothballing or planned retirement. Still operating in the EIA table. No change of owner, retirement or mothballing found in the EIA file. I did not search news because the brief asked only for a last check.

### G100000402874 / Spring Creek energy center / CT02
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CT02 (G100000402874) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55651 generator CT02 as operating with no retirement date. So I found no retirement, mothballing or planned retirement. Still operating in the EIA table. No change of owner, retirement or mothballing found in the EIA file. I did not search news because the brief asked only for a last check.

### G100000402875 / Spring Creek energy center / CT03
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CT03 (G100000402875) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55651 generator CT03 as operating with no retirement date. So I found no retirement, mothballing or planned retirement. Still operating in the EIA table. No change of owner, retirement or mothballing found in the EIA file. I did not search news because the brief asked only for a last check.

### G100000402876 / Spring Creek energy center / CT04
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CT04 (G100000402876) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55651 generator CT04 as operating with no retirement date. So I found no retirement, mothballing or planned retirement. Still operating in the EIA table. No change of owner, retirement or mothballing found in the EIA file. I did not search news because the brief asked only for a last check.

### G100000414190 / Stillwater Energy Center / IC
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit IC (G100000414190) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 59647 generator IC as operating with no retirement date. So I found no retirement, mothballing or planned retirement. Still operating in the EIA table. No change of owner, retirement or mothballing found in the EIA file. I did not search news because the brief asked only for a last check.

### G100000403433 / Tulsa power station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000403433) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists Tulsa plant 2965, generator 2, as operating at 170.0 MW, operating since November 1956. No retirement notice found. Still operating per EIA. No sale, mothballing or retirement notice found. I found no document stating a Backup Power value for this steam unit, so Backup Power was not changed.

### G100000403433 / Tulsa power station / 2
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit 2 (G100000403433) to 2034. The box is empty now. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `` -> `2034`
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: Public Service Company of Oklahoma's 2026 integrated resource plan refresh (https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf) lists Tulsa 2 retiring in 2034. A second table in the same report gives 2033 for unit 2, so the report disagrees with itself. The human adds a new scheduled retirement event.

### G100000403434 / Tulsa power station / 4
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4 (G100000403434) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists Tulsa plant 2965, generator 4, as operating at 170.0 MW, operating since April 1958. No retirement notice found. Still operating per EIA. No sale, mothballing or retirement notice found. I found no document stating a Backup Power value for this steam unit, so Backup Power was not changed.

### G100000403434 / Tulsa power station / 4
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit 4 (G100000403434) to 2034. The box is empty now. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `` -> `2034`
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2026 integrated resource plan refresh (https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf) lists Tulsa 4 retiring in 2034 in two tables. The human adds a new scheduled retirement event.

### G100000403435 / Weleetka power station / 4
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4 (G100000403435) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists this unit as operating. Row: Plant 2966, generator 4, status operating, nameplate 53.0 MW, operating year 1975, planned retirement 2030. This confirms the status; it does not change it. The EIA table for September 2026 shows unit 4 operating with retirement planned for 2030, and the PSO plan agrees. I found no document that states a Backup Power value. The unit is a grid gas turbine and no source says it is backup power.

### G100000403436 / Weleetka power station / 5
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 5 (G100000403436) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists this unit as operating. Row: Plant 2966, generator 5, status operating, nameplate 53.0 MW, operating year 1976, planned retirement 2030. This confirms the status; it does not change it. The EIA table for September 2026 shows unit 5 operating with retirement planned for 2030, and the PSO plan agrees. I found no document that states a Backup Power value. The unit is a grid gas turbine and no source says it is backup power.

### Comanche (OK) power station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Public Service Company of Oklahoma (owner); lookup: Entity exists, appears on 28 units in the United States. Reuse the existing entity.

### Cross Timbers Power Plant
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Cross Timbers Power LLC (owner); lookup: Entity exists, appears on 2 units in the United States. Reuse the existing entity.

### Green Country Energy power station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Public Service Company of Oklahoma (owner); lookup: Already the owner in GEM; no new entity named.

### Kiamichi energy facility
*question about existing data; checklist rows 19 (Missing or unknown owner searched), 43 (Ownership changes for operating units reviewed (optional))*
- about: Owner(s)
- question: Should Kiamichi be owned by Kiowa Power Partners alone, or by the partnerships in the federal ownership table?
- finding: GEM lists Kiowa Power Partners LLC at 100 percent. The federal annual survey for 2025 lists Tenaska Oklahoma I LP at about 99 percent, with small shares for Tenaska Oklahoma Inc, TC Oklahoma GP and Tyr Oklahoma GP.
- recommendation: Keep Kiowa Power Partners at 100 percent. The listed partnerships hold under five percent each apart from the main partnership, which is the Tenaska affiliate of the same owner group.
  - links: https://www.eia.gov/electricity/data/eia860/ (ok=True, contains_value=True)
- notes: GEM's parents, ITOCHU and Tenaska Energy, are consistent with the federal table. The entity lookup found no separate Tenaska Oklahoma entity.

### Kiamichi energy facility
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Kiowa Power Partners LLC (owner); lookup: Already the owner in GEM; no new entity named.

### G100000403433 / Tulsa power station / 2
*question about existing data; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
- about: Planned retire
- question: Does Tulsa 2 retire in 2033 or 2034?
- finding: The PSO 2026 integrated resource plan refresh (https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf) shows 2034 in one table and 2033 in another for Tulsa 2.
- recommendation: Use 2034, which matches the other table and Tulsa 4. Add a scheduled retirement event for 2034.
  - links: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=None, contains_value=None)
- notes: Both tables are in the same report.

## Checklist group 7. IDs, IRPs and data centers

United States only: EIA and other IDs, utility resource plans, data center power (gas or diesel, routine or backup; a backup engine fleet counts and is added at the summed nameplate threshold).

### G100000403748 / Anadarko power station / 3
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Leave Status of unit 3 (G100000403748) as retired. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `retired` -> `retired`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 3006, generator 3, on its Retired sheet with a retirement date of December 2024 and 50.0 MW nameplate. I read the row myself. So GEM's retired status is right. The Energy Institute Project row that calls Anadarko under construction describes the new Roulet 12 and 13 turbines, not unit 3. Unit 3 is retired per EIA. The Energy Institute row saying under construction matches the new Roulet units. I found no document that states a Backup Power value.

### G100001101631 / Bristow Energy Center / 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 1 (G100001101631) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.aeci.org/bristow-energy-center-1 (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Associated Electric Cooperative page at https://www.aeci.org/bristow-energy-center-1 describes a natural gas peaking unit serving member demand, not a backup unit. It does not use the words backup power, so this is implied.

### G100001101676 / Citadel Facility Data Center power station / 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Number Of Engines of unit 1 (G100001101676) as 36. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `36` -> `36`
  - Capacity Data Source: https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The permit at https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf lists 36 diesel generators of 3,997 horsepower each, numbered 1 to 36, all Cummins DQLF.

### G100000402193 / Comanche (OK) power station / CC1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit CC1 (G100000402193) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8810.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Oklahoma Department of Environmental Quality permit memorandum from September 2024 at https://applications.deq.ok.gov/permitspublic/storedpermits/8810.pdf describes Comanche as an electric utility plant that burns natural gas to generate electricity for the grid. It does not use the words backup power, so this is implied.

### G100001091022 / Cross Timbers Power Plant / 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 1 (G100001091022) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The permit memorandum at https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf describes the two turbines as the plant's generation, with a separate small diesel emergency generator. It does not use the words backup power, so this is implied. The turbines are not a backup fleet for a data center.

### G100001091024 / Cross Timbers Power Plant / 2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 2 (G100001091024) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The permit memorandum at https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf describes the two turbines as the plant's generation, with a separate small diesel emergency generator. It does not use the words backup power, so this is implied. The turbines are not a backup fleet for a data center.

### G100000414263 / Grand River Energy Center / 4
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4 (G100000414263) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (plant 165, generator 4) lists the unit as operating since September 2026. An American Public Power Association article from September 9, 2026 describes the formal dedication of Unit 4. The status of operating stays. The Energy Impact Partners page and the Sierra Club list that show under construction are out of date. Unit 4 is operating. The owner says 426 MW and EIA says 594 MW nameplate. No retirement, mothballing or owner change was found. The Oklahoma Department of Environmental Quality permit memo lists a 2.5 MW diesel emergency generator for the Unit 4 project, but it does not say the unit is a backup power unit.

### G100000414263 / Grand River Energy Center / 4
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Leave Capacity (MW) of unit 4 (G100000414263) as 426.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `426.0` -> `426.0`
  - Capacity Data Source: https://www.publicpower.org/periodical/article/grand-river-dam-authority-formally-dedicates-unit-4-grand-river-energy-center (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The American Public Power Association article from September 9, 2026 says Unit 4 has a 426 megawatt Mitsubishi Power combustion turbine in simple cycle. The EIA-860M table for September 2026 gives 594 MW nameplate for generator 4. Both are in the question about capacity. GEM's 426 MW matches the owner's stated rating.

### G100001048466 / Horseshoe Lake power station / 11
*change to an existing unit; checklist rows 37 (IRP box ticked on every IRP project (US only)), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 11 (G100001048466) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: On the October 28, 2026 earnings call, OGE Energy said Horseshoe Lake units 11 and 12 were completed ahead of schedule and added about 448 MW. The call summary is at https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/. A September 2026 OG&E news release at https://www.oge.com/web/portal/-/208-og-e-completes-horseshoe-lake-unit-11-ahead-of-schedule-and-under-budget said unit 11 passed its performance tests and would enter commercial service in October, and unit 12 would follow in October. No document found states the exact commercial operation date for unit 11. The EIA-860M table for September 2026 still shows it as construction complete, not yet in commercial operation. So GEM's operating status is kept, with a question for the reviewer. Status operating is kept. No retirement, mothballing or owner change was found. The exact in-service month was not found in a document.

### G100001048467 / Horseshoe Lake power station / 12
*change to an existing unit; checklist rows 37 (IRP box ticked on every IRP project (US only)), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 12 (G100001048467) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: On the October 28, 2026 earnings call, OGE Energy said Horseshoe Lake units 11 and 12 were completed ahead of schedule and added about 448 MW. The call summary is at https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/. A September 2026 OG&E news release at https://www.oge.com/web/portal/-/208-og-e-completes-horseshoe-lake-unit-11-ahead-of-schedule-and-under-budget said unit 11 passed its performance tests and would enter commercial service in October, and unit 12 would follow in October. No document found states the exact commercial operation date for unit 12. The EIA-860M table for September 2026 still shows it as construction complete, not yet in commercial operation. So GEM's operating status is kept, with a question for the reviewer. Status operating is kept. No retirement, mothballing or owner change was found. The exact in-service month was not found in a document.

### G100000403306 / Horseshoe Lake power station / 6
*change to an existing unit; checklist rows 21 (Planned retirements searched), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Retired year of unit 6 (G100000403306) as 2024. It is still correct. Add the link below to the Retired Year Data Source box. Keep the links already there.
- `Retired year`: `2024` -> `2024`
  - Retired Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026, Retired sheet, plant 2951, lists unit 6, a 163 MW steam unit as retired in January 2024. This matches GEM and is the source for the 2024 retirement. The file is at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx. Unit 6 is retired in GEM and in the EIA-860M Retired sheet (January 2024).

### G100000403309 / Horseshoe Lake power station / ST7
*change to an existing unit; checklist rows 21 (Planned retirements searched), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Retired year of unit ST7 (G100000403309) as 2024. It is still correct. Add the link below to the Retired Year Data Source box. Keep the links already there.
- `Retired year`: `2024` -> `2024`
  - Retired Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026, Retired sheet, plant 2951, lists unit ST7, a 220 MW steam unit as retired in December 2024. This matches GEM and is the source for the 2024 retirement. The file is at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx. Unit ST7 is retired in GEM and in the EIA-860M Retired sheet (December 2024).

### G100000401929 / McClain energy facility / G011
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit G011 (G100000401929) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8740.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Oklahoma Department of Environmental Quality permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8740.pdf describes a combined cycle power plant that serves the grid. Its only backup equipment is small emergency engines for the plant itself. It does not call any generating unit a backup unit. So the value no is implied, not stated outright.

### G100000403752 / Mooreland power station / 2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 2 (G100000403752) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8994.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8994.pdf says the plant sells wholesale power over Western Farmers Electric Cooperative's system. It calls the boilers peaking units. It does not describe any unit as backup power. So the value no is implied, not stated outright.

### G100000403753 / Mooreland power station / 3
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 3 (G100000403753) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8994.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8994.pdf says the plant sells wholesale power over Western Farmers Electric Cooperative's system. It calls the boilers peaking units. It does not describe any unit as backup power. So the value no is implied, not stated outright.

### G100001091053 / Muskogee Data Center power station / 1
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Set Number Of Engines of unit 1 (G100001091053) to 105. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `` -> `105`
  - Capacity Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ae6Ctfv7oSCmhMZ%C3%89kDp%C3%89JKeyyrF%C3%897NeqHWN6Fd0wYTdl604KTTG6bsIhnFC9Sgq7vhd656jR%C3%895uQBkEpWYOBnMg%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft permit memorandum lists 83 MTU engines, 21 Cummins engines and 1 Caterpillar D1000GC engine, 105 diesel emergency engines in all. Status stays construction. A Core Scientific press release says a leased 70 MW building was in final testing and commissioning, so the project is moving and Latest Activity is left alone. Capacity Per Engine is blank because the fleet mixes three engine sizes.

### G100001091053 / Muskogee Data Center power station / 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 1 (G100001091053) as yes. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `yes` -> `yes`
  - Backup Power Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ae6Ctfv7oSCmhMZ%C3%89kDp%C3%89JKeyyrF%C3%897NeqHWN6Fd0wYTdl604KTTG6bsIhnFC9Sgq7vhd656jR%C3%895uQBkEpWYOBnMg%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft permit says the 105 diesel generators provide backup power to the facility in an emergency.

### G100001017849 / Muskogee Generating Station / Unit 4, timepoint 2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit Unit 4, timepoint 2 (G100001017849) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf describes the unit as a main boiler. The only emergency equipment is diesel generators and a fire pump for the plant. So the value no is implied.

### G100001017850 / Muskogee Generating Station / Unit 5, timepoint 2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit Unit 5, timepoint 2 (G100001017850) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8130.pdf describes the unit as a main boiler. The only emergency equipment is diesel generators and a fire pump for the plant. So the value no is implied.

### G100000403312 / Mustang (OK) power station / 6-12
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Leave Capacity (MW) of unit 6-12 (G100000403312) as 462.0. It is still correct. Add the 3 links below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `462.0` -> `462.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Capacity Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/4458.pdf (ok=True, contains_value=True)
  - Capacity Data Source: https://oklahoma.gov/content/dam/ok/en/occ/documents/pu/pud-reports-page/2025-oge-irp.pdf (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists seven generators, GT1 to GT7, each with a nameplate of 66.0 MW. Together that is 462 MW, so GEM's one row for units 6 to 12 matches the whole plant. The 2018 permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/4458.pdf gives 66 MW per Siemens Trent turbine. The OG&E 2025 resource plan at https://oklahoma.gov/content/dam/ok/en/occ/documents/pu/pud-reports-page/2025-oge-irp.pdf lists summer capability of 55 to 58 MW each for Mustang 6 to 12, in service 2018. Suggested line for the resource plan notes: OG&E 2025 resource plan lists Mustang 6 to 12 as existing gas turbines, 2018, 55 to 58 MW summer each, no retirement.

### G100000403312 / Mustang (OK) power station / 6-12
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 6-12 (G100000403312) as no. It is still correct. Add the 2 links below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/4458.pdf (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 lists all seven turbines at Mustang under the sector Electric Utility, not as backup units, and the Oklahoma Department of Environmental Quality permit memo from June 2018 at https://applications.deq.ok.gov/permitspublic/storedpermits/4458.pdf calls the site an electric generating station that sells power. Only the small diesel generator and fire pump are emergency equipment. So the existing value of no stands.

### G100001055294 / Northeastern Station / Unit 3, timepoint 2
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 3, timepoint 2 (G100001055294) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.sec.gov/Archives/edgar/data/4904/000000490426000059/aep-20260630.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The AEP quarterly report for June 2026 (https://www.sec.gov/Archives/edgar/data/4904/000000490426000059/aep-20260630.htm) says Public Service Company of Oklahoma began operating Northeastern Unit 3 on natural gas in January 2026. The September 2026 EIA-860M table still lists generator 3 with coal as its energy source, which is out of date. This settles the question raised by the Oil and Gas Watch listing of proposed. I could not read that Oil and Gas Watch page because it is drawn by script and the fetch showed no plant name. Operating on gas since January 2026 and planned to run through May 2041. No document states backup power.

### G100000401851 / Oneta energy center / BLK1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit BLK1 (G100000401851) as no. It is still correct. Add the 2 links below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8041.pdf (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 lists Oneta Power LLC as an independent power producer, not as backup or emergency generation, and the 2021 permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8041.pdf describes base-load combined cycle turbines with duct burners. So the value of no stands.

### G100000401852 / Oneta energy center / BLK2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit BLK2 (G100000401852) as no. It is still correct. Add the 2 links below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/8041.pdf (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 lists Oneta Power LLC as an independent power producer, not as backup or emergency generation, and the 2021 permit memo at https://applications.deq.ok.gov/permitspublic/storedpermits/8041.pdf describes base-load combined cycle turbines with duct burners. So the value of no stands.

### G100000403323 / Ponca City power station / 4
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 4 (G100000403323) as no. It is still correct. Add the 2 links below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/4608.pdf (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 lists the plant as an electric utility plant, and the Oklahoma Department of Environmental Quality memo from April 2019 at https://applications.deq.ok.gov/permitspublic/storedpermits/4608.pdf describes it as an electricity generation plant with diesel emergency generators as separate equipment. So the value of no stands.

### G100000402159 / Ponca City power station / CC1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit CC1 (G100000402159) as no. It is still correct. Add the 2 links below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
  - Backup Power Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/4608.pdf (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 lists the plant as an electric utility plant, and the Oklahoma Department of Environmental Quality memo from April 2019 at https://applications.deq.ok.gov/permitspublic/storedpermits/4608.pdf describes it as an electricity generation plant with diesel emergency generators as separate equipment. So the value of no stands.

### G100000402873 / Spring Creek energy center / CT01
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit CT01 (G100000402873) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists the plant in the electric utility sector, which sells power to the grid. It does not say anything about backup power directly, so this is implied only.

### G100000402874 / Spring Creek energy center / CT02
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit CT02 (G100000402874) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists the plant in the electric utility sector, which sells power to the grid. It does not say anything about backup power directly, so this is implied only.

### G100000402875 / Spring Creek energy center / CT03
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit CT03 (G100000402875) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists the plant in the electric utility sector, which sells power to the grid. It does not say anything about backup power directly, so this is implied only.

### G100000402876 / Spring Creek energy center / CT04
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit CT04 (G100000402876) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists the plant in the electric utility sector, which sells power to the grid. It does not say anything about backup power directly, so this is implied only.

### G100000414190 / Stillwater Energy Center / IC
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit IC (G100000414190) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists the plant in the electric utility sector, which sells power to the grid. It does not say anything about backup power directly, so this is implied only.

### G100001072817 / Tinker Air Force Base power station / 1-2
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1-2 (G100001072817) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.oge.com/documents/d/portal/oge-2026-irp-final (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 lists generators 1 and 2 as operating. OG&E's 2026 integrated resource plan says Tinker units 1 and 2 were placed in service in March 2026. This matches the current value. The unit is operating and no retirement, mothballing or owner change was found. The Sierra Club change flag most likely reflects the March 2026 start of service, which the EIA table and OG&E plan confirm.

### G100001072817 / Tinker Air Force Base power station / 1-2
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Leave Capacity (MW) of unit 1-2 (G100001072817) as 96.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `96.0` -> `96.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Two generators of 48.1 MW each in the EIA-860M table for September 2026 add up to 96.2 MW. GEM shows 96.0 MW. The air permit application lists a higher 51.1 MW rating per turbine at standard test conditions, which is not nameplate.

### G100001072817 / Tinker Air Force Base power station / 1-2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 1-2 (G100001072817) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.oge.com/documents/d/portal/oge-2026-irp-final (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: OG&E's 2026 integrated resource plan says the Tinker units can be dispatched by the Southwest Power Pool to serve all customers and supply the grid at peak times. They also give islanding resilience to the base. So they are grid units, not a backup fleet. The plan does not use the words backup power, so this is implied.

### G100001092967 / Tinker Air Force Base power station / 5A-5B
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 5A-5B (G100001092967) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.oge.com/documents/d/portal/oge-2026-irp-final (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: OG&E's 2026 plan lists these units among its grid resources before their retirement. It does not call them backup. This is implied.

### Myall Pryor Data Center power station
*new plant; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
**Action:** Create Myall Pryor Data Center power station in Pryor, Mayes County, Oklahoma, owned by Myall, LLC, then add the one unit below with capacity blank. Create the owner as a new entity.
- `State/Province`: `` -> `Oklahoma`
- `Local area (taluk, county)`: `` -> `Mayes`
- `City`: `` -> `Pryor`
- `Other Name(s)`: `` -> `PRY Data Storage Facility`
- `Latitude`: `` -> `36.2425`
- `Longitude`: `` -> `-95.3302`
- `Location accuracy`: `` -> `approximate`
- `Owner(s)`: `` -> `Myall, LLC [100%]`
- unit 1 `Fuel`: `fossil liquids: diesel`
- unit 1 `Status`: `operating`
- unit 1 `Turbine/Engine Technology`: `internal combustion`
- unit 1 `Captive industry use`: `power`
- unit 1 `Captive industry type`: `data center`
- unit 1 `Captive non-industry use`: `none`
- unit 1 `Backup Power`: `yes`
- location now: none in GEM
- location proposed: 36.2425, -95.3302 (approximate) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=36.24250,-95.33020&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=36.24250,-95.33020)
  - Location Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9149.pdf (ok=True, contains_value=True)
  - Owners Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/9149.pdf (ok=True, contains_value=True)
  - Owners Data Source: https://www.datacenterknowledge.com/hyperscalers/google-planning-oklahoma-data-center (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this plant. The Oklahoma Department of Environmental Quality permit evaluation of November 5, 2025 covers Myall, LLC and its PRY Data Storage Facility in Pryor, Mayes County, at 36.2425 north and 95.3302 west. The facility has emergency generator engines, some fitted with selective catalytic reduction, plus fire pump engines. Myall asked the department to keep all engine details confidential, so the engine count and size are not public. The nitrogen oxide limit in the permit is 249 tons a year, which is a large fleet but gives no megawatt figure. Myall LLC is the company that bought the land for Google's Pryor campus in the MidAmerica Industrial Park, so this is very likely a Google building. The permit itself does not name Google. The record is added with capacity blank, as the rules say for an unknown size. Diesel is the fuel named for the generators in the permit, and the permit also says the facility burns natural gas in other equipment. Unit 1 is the emergency generator engine group.

### OKC2 Scale Datacenter power station
*new plant; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
**Action:** Create OKC2 Scale Datacenter power station in Oklahoma City, Oklahoma County, owned by 6000 N Shartel Ave, LLC, then add the two engine units below. Create the owner as a new entity.
- `State/Province`: `` -> `Oklahoma`
- `Local area (taluk, county)`: `` -> `Oklahoma`
- `City`: `` -> `Oklahoma City`
- `Other Name(s)`: `` -> `OKC2`
- `Latitude`: `` -> `35.53351`
- `Longitude`: `` -> `-97.52242`
- `Location accuracy`: `` -> `approximate`
- `Owner(s)`: `` -> `6000 N Shartel Ave, LLC [100%]`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Status`: `pre-construction`
- unit 1 `Start year`: `2027`
- unit 1 `Turbine/Engine Technology`: `internal combustion`
- unit 1 `Number Of Engines`: `16`
- unit 1 `Capacity Per Engine`: `9`
- unit 1 `Capacity (MW)`: `144`
- unit 1 `Captive industry use`: `power`
- unit 1 `Captive industry type`: `data center`
- unit 1 `Captive non-industry use`: `none`
- unit 1 `Backup Power`: `no`
- unit 2 `Fuel`: `fossil gas: natural gas`
- unit 2 `Status`: `pre-construction`
- unit 2 `Start year`: `2027`
- unit 2 `Turbine/Engine Technology`: `internal combustion`
- unit 2 `Number Of Engines`: `3`
- unit 2 `Capacity Per Engine`: `5.94`
- unit 2 `Capacity (MW)`: `17.82`
- unit 2 `Captive industry use`: `power`
- unit 2 `Captive industry type`: `data center`
- unit 2 `Captive non-industry use`: `none`
- unit 2 `Backup Power`: `no`
- location now: none in GEM
- location proposed: 35.53351, -97.52242 (approximate) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=35.53351,-97.52242&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=35.53351,-97.52242)
  - Location Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ASCsZfZJOr8EbvF%C3%81Ggb4d5pgBB8P%C3%893SavzfBq06GG90H9bIu884yqy5xtHsV9LFXKJVMOhq8Jt7BeOnZ7nXm4%C3%89E%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Owners Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/ASCsZfZJOr8EbvF%C3%81Ggb4d5pgBB8P%C3%893SavzfBq06GG90H9bIu884yqy5xtHsV9LFXKJVMOhq8Jt7BeOnZ7nXm4%C3%89E%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: )
- notes: GEM does not list this plant. The Oklahoma Department of Environmental Quality has an application from 6000 N Shartel Ave, LLC, dated September 2026, for the OKC2 data center in Oklahoma City. It asks to add 8 natural gas engines to 11 already permitted under permit 2026-0216-C, which the department issued on August 26, 2026. That makes 19 engines in all: sixteen Wartsila 20V34SG of 9,000 kilowatts and three Wartsila 18V34SG of 5,940 kilowatts, for 161.82 megawatts of electrical capacity. The engines are the continuous power source for the site and run apart from the grid, so they are not backup units. Six of the eight new engines run and two stand by. Construction and start-up are planned for the first quarter of 2027. None of the first 11 engines can be operating yet, because the application says start-up has not happened. The application gives the site point at 35.53351 north and 97.52242 west. That point is approximate until it is checked on a map. The applicant name is the permit holder, and no match exists in the entity list. Unit 1 is the group of Wartsila 20V34SG engines and unit 2 is the group of Wartsila 18V34SG engines.

### G100001072819 / Chickasha industrial park power station / 1
*question about existing data; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 39 (Gas-powered data centers searched, captive data entered (US only)), 50 (Other last-minute status changes checked)*
- about: Status
- question: Is a second source needed for the Chickasha cancellation?
- finding: The Chickasha Economic Development Authority release page (https://chickashaedc.com/2025/06/governor-stitt-chickasha-leaders-celebrate-largest-private-investment-in-city-history-with-announcement-of-new-industrial-park) carries the note that the project was cancelled as of early 2026 due to site limitations. No second publisher was found. The Energy Infrastructure Platform still lists it as proposed.
- recommendation: Keep cancelled, as a single-source status change. Ask the Chickasha authority or search the Express-Star for a second report.
  - links: https://chickashaedc.com/2025/06/governor-stitt-chickasha-leaders-celebrate-largest-private-investment-in-city-history-with-announcement-of-new-industrial-park (ok=None, contains_value=None)
- notes: The industrial park hub page (https://chickashaedc.com/chickasha-airport-industrial-park) does not mention the cancellation text.

### Citadel Facility Data Center power station
*question about existing data; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
- about: Captive non-industry use
- question: Should GEM add the 10 smaller backup engines in the Citadel Facility permit to its 297 megawatt record?
- finding: The department's comment document for permit 2026-0286-C lists 36 engines of 3,997 horsepower and 72 of 4,043 horsepower, which are the 108 engines GEM counts at 297 megawatts. It also lists 6 engines of 2,584 horsepower and 4 of 1,340 horsepower for backup, and one fire pump, that GEM does not carry.
- recommendation: Add the 10 smaller engines as one more backup unit when the permit is final, with their electrical rating taken from the application, and leave the fire pump out.
  - links: https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf (ok=True, contains_value=True)
- notes: The horsepower figures are engine shaft ratings, so the electrical rating has to come from the generator data sheets in the application. The comment period was still open on November 5, 2026.

### G100001101676 / Citadel Facility Data Center power station / 1
*question about existing data; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
- about: Number Of Engines
- question: Should the 10 smaller backup engines at Citadel be added as a unit?
- finding: The permit at https://oklahoma.gov/content/dam/ok/en/deq/documents/air-quality/Citadel%20Facility-2026-0286-C.pdf lists 6 engines of 2,584 horsepower and 4 engines of 1,340 horsepower besides the 108 engines in the two units, plus one fire pump. At about 1.75 MW for the first six, the groups sum to about 10.5 MW and about 5 MW.
- recommendation: Leave them out. They sum well under the 50 MW bar.
- notes: This matches the existing database note from November 4, 2026.

### Comanche (OK) power station / CC1
*question about existing data; checklist rows 21 (Planned retirements searched), 37 (IRP box ticked on every IRP project (US only))*
- about: Planned retire
- question: Should Comanche unit 1 get a planned retirement year of 2035?
- finding: The 2026 refresh report from the Public Service Company of Oklahoma lists the Comanche gas steam and combined cycle block 1 with a retirement or contract expiration date of 2035. GEM has no planned retirement year for it.
- recommendation: Add 2035 as the planned retirement year for unit CC1 only if you accept planning assumption dates, and cite the refresh report.
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- notes: The report says retirement dates are assumptions for planning only. The plan text also says the utility plans to retire Comanche 1 by summer 2036. I used the table date of 2035.

### G100000414263 / Grand River Energy Center / 4
*question about existing data; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
- about: Capacity (MW)
- question: Should unit 4 capacity stay at 426 MW or change to 594 MW?
- finding: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) gives 594.0 MW nameplate for generator 4, and the Southwest Power Pool queue entry GEN-2024-GR5 (https://opsportal.spp.org/Studies/GIActive) lists 594 MW as a gas and storage hybrid. The owner's dedication article (https://www.publicpower.org/periodical/article/grand-river-dam-authority-formally-dedicates-unit-4-grand-river-energy-center) says 426 MW. A 2024 permit memo (https://applications.deq.ok.gov/permitspublic/storedpermits/8824.pdf) lists a 453 MW turbine.
- recommendation: Leave 426 MW for now. If the generator nameplate is 594 MW, change it to 594.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://opsportal.spp.org/Studies/GIActive (ok=None, contains_value=None)
  - links: https://www.publicpower.org/periodical/article/grand-river-dam-authority-formally-dedicates-unit-4-grand-river-energy-center (ok=None, contains_value=None)
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/8824.pdf (ok=None, contains_value=None)
- notes: The three numbers describe different ratings. Queue entry GEN-2024-GR5 is a replacement request, with a cessation date of 16 September 2026 and a summer rating of 554 MW against a winter rating of 594 MW in the open list at https://opsportal.spp.org/Studies/GenerateActiveCSV, read on 5 November 2026. That points to ratings that change with the season, not to extra storage capacity. A rating of 594 MW is a winter figure.

### G100000403305 / Horseshoe Lake power station / 10
*question about existing data; checklist rows 37 (IRP box ticked on every IRP project (US only)), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
- about: Status
- question: Is the Energy and Policy Institute proposed record for Horseshoe Lake wrong for unit 10?
- finding: The Energy and Policy Institute Oil and Gas Watch record at https://oilandgaswatch.org/facility/rec_d4f1u5oq7easr8ra1f60 lists the plant as proposed. The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists unit 10 as operating, 60.5 MW, started 2001.
- recommendation: Leave unit 10 as operating. The proposed label most likely reflects the new units 13 to 15.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: The record page is drawn by script and its text could not be read by the page checker.

### G100001048466 / Horseshoe Lake power station / 11
*question about existing data; checklist rows 37 (IRP box ticked on every IRP project (US only)), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
- about: Status
- question: Should units 11 and 12 stay operating when EIA still shows testing?
- finding: OG&E said in September 2026 that unit 11 passed its tests and would enter service in October. The October 28, 2026 earnings call at https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ describes both units as added capacity. The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx still shows both as construction complete, not yet in commercial operation, planned October 2026.
- recommendation: Leave both units as operating. Check the OG&E ribbon cutting release in November 2026 for the exact date.
  - links: https://www.marketbeat.com/instant-alerts/transcript-oge-energy-q3-earnings-call-highlights-2026-10-28/ (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: I did not find a document that gives the commercial operation date. Sierra Club data also shows construction, but it is not cited.

### Muskogee Data Center power station
*question about existing data; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
- about: Captive non-industry use
- question: Should GEM raise the Muskogee Data Center power station from 283.1 megawatts to about 314 megawatts?
- finding: Core Scientific's July 2026 permit application asks for 105 diesel generators: 50 of 2.75 or 3 megawatts and one of 1 megawatt at MSK1-A, and 54 of 3.25 megawatts at MSK1-B. That sums to 314.0 megawatts with the 2.75 megawatt model, or 326.5 megawatts with the 3 megawatt model. GEM lists 283.1 megawatts, built from the earlier permit of 102 engines.
- recommendation: Update the plant to the 105 engines in the July 2026 application once the department issues the modified permit, and use 314.0 megawatts until the engine model is chosen.
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AXCzq%C3%89UzFvv6lAbMvp98F3wyixVRq%C3%89EeQdXeDl4C1Lwqd6ORCTsNS8N0kvwYkUSiOXX7FUOqIAMk7Z505l52EkM%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- notes: The application also renames the buildings MSK1 and MSK2 as MSK1-A and MSK1-B. It changes the 50 engines at the second building to 3.25 megawatt models, adds four more, and drops the house generator there. The old total of 102 engines had 100 main generators and 2 house generators.

### G100001017849 / Muskogee Generating Station / Unit 4, timepoint 2
*question about existing data; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
- about: Start year
- question: Should units 4 and 5 timepoint 2 keep start year 2019 against EIA's 1977 and 1978?
- finding: The EIA-860M table for September 2026 gives operating years 1977 for unit 4 and 1978 for unit 5. Those are the original coal units. GEM records the conversion year, 2019, for the converted units.
- recommendation: Leave 2019 as it is, since GEM's convention is the conversion year. Add the conversion permit memo as the source if a reviewer wants one.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/4454.pdf (ok=None, contains_value=None)
- notes: EIA table: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx. Conversion permit memo: https://applications.deq.ok.gov/permitspublic/storedpermits/4454.pdf. I could not confirm the 2019 restart date in a document.

### G100001055294 / Northeastern Station / Unit 3, timepoint 2
*question about existing data; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
- about: Status
- question: Should the Oil and Gas Watch and Sierra Club entries for Unit 3 be updated to operating?
- finding: The AEP report for June 2026 (https://www.sec.gov/Archives/edgar/data/4904/000000490426000059/aep-20260630.htm) says Unit 3 has run on natural gas since January 2026.
- recommendation: Keep Unit 3 as operating in GEM. Tell the owners of the Oil and Gas Watch and Sierra Club lists that their proposed and planned labels look out of date.
  - links: https://www.sec.gov/Archives/edgar/data/4904/000000490426000059/aep-20260630.htm (ok=None, contains_value=None)
- notes: I could not read the Oil and Gas Watch page, so I did not see its own source documents.

### Northeastern power station
*question about existing data; checklist rows 21 (Planned retirements searched), 37 (IRP box ticked on every IRP project (US only))*
- about: Planned retire
- question: Should Northeastern unit 2 and the NE1S unit get a planned retirement year of 2036?
- finding: The 2026 refresh report from the Public Service Company of Oklahoma lists Northeastern unit 2 and the 1A, 1B and 1S combined cycle block retiring in 2036. GEM has no planned retirement year for them.
- recommendation: Add 2036 for unit 2 and NE1S.
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- notes: Retirement dates in the report are planning assumptions. Unit 3 already shows 2041 in GEM, which matches the report. The report lists unit 3 as 420 MW after the gas conversion while GEM shows 473 MW.

### Northeastern power station / Unit 5 and Unit 6
*question about existing data; checklist rows 37 (IRP box ticked on every IRP project (US only))*
- about: Start year
- question: Should Northeastern Units 5 and 6 show a 2029 start year instead of 2028?
- finding: The Public Service Company of Oklahoma 2026 refresh report lists the two new F class gas turbines at Northeastern, 450 MW in total, with a commercial operation date of 2029. GEM shows 2028 for both units.
- recommendation: Change the start year of both units to 2029 and keep 225 MW each, which matches the plan total of 450 MW.
  - Start Year Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- notes: The plan was filed in 2026 and the state commission approved the project on May 11, 2026. The plan's capacity table gives 2029 and a 2059 contract end. Another helper holds the permit side of the same plant.

### OG&E 2026 requests for proposals
*watch item, new to the tracker; checklist rows 37 (IRP box ticked on every IRP project (US only)), 51 (Newly announced projects checked)*
- what to watch: The OG&E 2026 plan says its 2026 requests for proposals are open to cover current capacity needs.
- check again by: 2027-03
  - links: https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 (ok=True, contains_value=True)
- notes: The OG&E 2026 plan says its 2026 requests for proposals are open to cover current capacity needs. The plan names no new gas site beyond Horseshoe Lake units 11 to 15 and the Tinker project, which GEM already lists. Recheck when OG&E files a pre-approval case for any new unit.

### Public Service Company of Oklahoma 2026 all-source request for proposals
*watch item, new to the tracker; checklist rows 37 (IRP box ticked on every IRP project (US only)), 51 (Newly announced projects checked)*
- what to watch: The Public Service Company of Oklahoma issued an all-source request for proposals on January 2, 2026 for about 4,000 MW of accredited capacity, and received bids on March 16, 2026.
- check again by: 2027-03
  - links: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- notes: The Public Service Company of Oklahoma issued an all-source request for proposals on January 2, 2026 for about 4,000 MW of accredited capacity, and received bids on March 16, 2026. No gas site or unit is named, and the utility has not picked winners. Recheck after the shortlist is filed with the state commission.

### Riverside (OK) power station
*question about existing data; checklist rows 21 (Planned retirements searched), 37 (IRP box ticked on every IRP project (US only))*
- about: Planned retire
- question: Should Riverside units 1 and 2 get a planned retirement year of 2041?
- finding: The 2026 refresh report from the Public Service Company of Oklahoma lists Riverside units 1 and 2 retiring in 2041 and units 3 and 4 in 2056. GEM has no planned retirement years for the plant.
- recommendation: Add 2041 for units 1 and 2 and leave units 3 and 4 blank.
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- notes: The report says retirement dates are planning assumptions. GEM also shows 473 MW for units 1 and 2 while the report lists 431 and 448 MW, so check the capacity at the same time.

### Southwestern power station
*question about existing data; checklist rows 21 (Planned retirements searched), 37 (IRP box ticked on every IRP project (US only))*
- about: Planned retire
- question: Should Southwestern units 1 and 2 get a planned retirement year of 2030?
- finding: The 2026 refresh report from the Public Service Company of Oklahoma lists units 1 and 2 retiring in 2030, and unit 3 in 2037. Units 4 and 5 are listed to 2056. GEM has no planned retirement years for the plant.
- recommendation: Add 2030 for units 1 and 2 and 2037 for unit 3, and leave units 4 and 5 blank because 2056 is a contract life assumption.
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- notes: The report says its retirement dates are planning assumptions, not filed retirement notices.

### G100001072817 / Tinker Air Force Base power station / 1-2
*question about existing data; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
- about: Capacity (MW)
- question: Is 96 MW or 102 MW the right capacity for the two new turbines?
- finding: EIA nameplate is 48.1 MW per generator. The air permit application (https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AeNgrdQLsFw5W8dEEwRTc%C3%81pApsum6Hqboy8ro%C3%81CyJ8OFtu0HRxDmnOy6W2%C3%81nwK2s%C3%81raDCV3qK%C3%8912Ie4gZNs%C3%89Vd0%3D/?ViewerMode=PDF&ForceDownload=true) raises the maximum power rating to 51.1 MW per turbine at standard test conditions.
- recommendation: Use the EIA nameplate, so 96.2 MW in total, unless a document gives a different nameplate.
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/AeNgrdQLsFw5W8dEEwRTc%C3%81pApsum6Hqboy8ro%C3%81CyJ8OFtu0HRxDmnOy6W2%C3%81nwK2s%C3%81raDCV3qK%C3%8912Ie4gZNs%C3%89Vd0%3D/?ViewerMode=PDF&ForceDownload=true (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: The permit figure is a site-condition rating, not a nameplate.

### Tulsa power station
*question about existing data; checklist rows 21 (Planned retirements searched), 37 (IRP box ticked on every IRP project (US only))*
- about: Planned retire
- question: Should Tulsa units 2 and 4 get a planned retirement year of 2034?
- finding: The 2026 refresh report from the Public Service Company of Oklahoma lists Tulsa units 2 and 4 retiring in 2034. GEM has no planned retirement year for either unit.
- recommendation: Add 2034 as the planned retirement year for units 2 and 4.
  - Planned Retire Data Source: https://www.psoklahoma.com/lib/docs/community/projects/PSO_2026_IRP_Refresh_Final_Report.pdf (ok=True, contains_value=True)
- notes: The report says retirement dates are planning assumptions, not filed retirement notices.

## Checklist group 8. New to the tracker

New plants and units ready to add, candidates to watch, and the possible-updates rows.

### Georgia-Pacific Muskogee Mill power plant
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create Georgia-Pacific Muskogee Mill power plant in Muskogee County, Oklahoma, owned by Georgia-Pacific LLC, then add the three units below. Put EIA plant 10362 in Other IDs. Check the linked question card about GEM's Fort James plant first.
- `State/Province`: `` -> `Oklahoma`
- `Local area (taluk, county)`: `` -> `Muskogee`
- `City`: `` -> `Muskogee`
- `Latitude`: `` -> `35.7322`
- `Longitude`: `` -> `-95.2939`
- `Location accuracy`: `` -> `approximate`
- `Owner(s)`: `` -> `Georgia-Pacific LLC [100%]`
- `Captive industry use`: `` -> `power`
- `Captive industry type`: `` -> `pulp & paper`
- `Captive non-industry use`: `` -> `none`
- unit GEN1 `Fuel`: `fossil gas: natural gas`
- unit GEN1 `Capacity (MW)`: `25`
- unit GEN1 `Status`: `operating`
- unit GEN1 `Start year`: `1979`
- unit GEN1 `Turbine/Engine Technology`: `steam turbine`
- unit GEN2 `Fuel`: `fossil gas: natural gas`
- unit GEN2 `Capacity (MW)`: `44.5`
- unit GEN2 `Status`: `operating`
- unit GEN2 `Start year`: `1980`
- unit GEN2 `Turbine/Engine Technology`: `steam turbine`
- unit GEN3 `Fuel`: `fossil gas: natural gas`
- unit GEN3 `Capacity (MW)`: `44.5`
- unit GEN3 `Status`: `operating`
- unit GEN3 `Start year`: `1982`
- unit GEN3 `Turbine/Engine Technology`: `steam turbine`
- location now: none in GEM
- location proposed: 35.7322, -95.2939 (approximate) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=35.73220,-95.29390&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=35.73220,-95.29390)
  - Location Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Location Data Source: https://www.google.com/maps?q=35.7322,-95.2939 (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Captive Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Captive Data Source: https://applications.deq.ok.gov/permitspublic/storedpermits/3131.pdf (ok=True, contains_value=True)
- confidence: high (independent: )
- notes: GEM does not list a plant by this name. The monthly federal generator file for September 2026 lists Georgia-Pacific Muskogee, plant 10362, with three natural gas steam turbines: GEN1 at 25 MW from 1979, GEN2 at 44.5 MW from 1980 and GEN3 at 44.5 MW from 1982. All three are operating. That is 114 MW in total. The plant is at the Georgia-Pacific Muskogee mill, 4901 Chandler Road, Muskogee. A 2016 notice from the Oklahoma Department of Environmental Quality describes the mill's power boilers, which make steam for turbines that generate electricity. No document shows the units retired. GEM already lists a Fort James Muskogee Mill power plant with two coal units of 45.5 MW that are marked retired in 2020, and its note says conversion to gas. These may be the same turbines. A separate question card asks about that link. The owner is Georgia-Pacific LLC, which already exists as an entity. The status is operating because the federal file says so. The point comes from the federal file, so the location is approximate.

### Peoples Electric Cooperative Centrahoma power station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create the plant in Coal County, Oklahoma, owned by Peoples Electric Cooperative. Add the three engine groups below. The owner was not found in the entity list, so ask whether a new entity is needed.
- `State/Province`: `` -> `Oklahoma`
- `Local area (taluk, county)`: `` -> `Coal`
- `City`: `` -> `Centrahoma`
- `Latitude`: `` -> `34.5939`
- `Longitude`: `` -> `-96.2905`
- `Location accuracy`: `` -> `approximate`
- `Owner(s)`: `` -> `Peoples Electric Cooperative [100%]`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Capacity (MW)`: `24.69`
- unit 1 `Status`: `operating`
- unit 1 `Start year`: `2019`
- unit 1 `Turbine/Engine Technology`: `internal combustion`
- unit 1 `Number Of Engines`: `10`
- unit 1 `Capacity Per Engine`: `2.469`
- unit 2 `Fuel`: `fossil gas: natural gas`
- unit 2 `Capacity (MW)`: `24.69`
- unit 2 `Status`: `operating`
- unit 2 `Start year`: `2019`
- unit 2 `Turbine/Engine Technology`: `internal combustion`
- unit 2 `Number Of Engines`: `10`
- unit 2 `Capacity Per Engine`: `2.469`
- unit 3 `Fuel`: `fossil gas: natural gas`
- unit 3 `Capacity (MW)`: `12.35`
- unit 3 `Status`: `operating`
- unit 3 `Start year`: `2019`
- unit 3 `Turbine/Engine Technology`: `internal combustion`
- unit 3 `Number Of Engines`: `5`
- unit 3 `Capacity Per Engine`: `2.469`
- location now: none in GEM
- location proposed: 34.5939, -96.2905 (approximate) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=34.59390,-96.29050&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=34.59390,-96.29050)
  - Owners Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Aevth4xmYyMYEUksZxJwUqGnaRaWfTbuqstqjNNkWYX43sTZcmwOpZkwiQnIvBom5aPYVRnVFqOmoareNhLZSGg%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Owners Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Adi%C3%81Uj4HU48j7TJinfPrZ7F99J8r2OmzRMCr78Mar5%C3%81iTb6ZjN92Z8hh1DZPsPqO7bKF3FxOM26IVudy91ABEfs%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Location Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Aevth4xmYyMYEUksZxJwUqGnaRaWfTbuqstqjNNkWYX43sTZcmwOpZkwiQnIvBom5aPYVRnVFqOmoareNhLZSGg%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: )
- notes: GEM does not list this plant. Peoples Electric Cooperative runs three engine sites about one kilometer apart near Centrahoma. State permit files name ten G3520H engines at the Targa site, ten at the Centrahoma site and five at Little Dixie. Each engine is 2.469 MW, so the three sites together are 61.7 MW. The Southwest Power Pool list shows one commercial operation entry of 61.725 MW for Centrahoma, which matches the three sites exactly. Each site alone is under 50 MW, so the sites are grouped as one plant. Little Dixie has asked to add two newer engines, planned for spring 2027, and that application is still in review. The federal monthly generator file for September 2026 lists three plants owned by Peoples Electric Cooperative in Coal County. Centrahoma East has ten engines, Centrahoma West has ten and Little Dixie has five. Each engine is 2.5 MW and all are operating since July 2019. Unit 1 is Centrahoma East, unit 2 is Centrahoma West and unit 3 is Little Dixie. The state permit file calls the two ten-engine sites Targa and Centrahoma. The entity lookup found no entity for any spelling of Peoples Electric Cooperative, so a new entity is needed. Two smaller Peoples sites exist at 5 MW in Pittsburg County and 7.5 MW in Hughes County. Each is under 50 MW alone and is not added.

### SPP GEN-2024-013 McClain County gas turbine power station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2024-013 McClain County gas turbine power station in Oklahoma with owner left blank, then add the one unit below. Put SPP GEN-2024-013 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- `Local area (taluk, county)`: `` -> `McClain`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Capacity (MW)`: `496`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2030`
- unit 1 `Turbine/Engine Technology`: `gas turbine`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. The SPP active queue lists GEN-2024-013 as a gas request of 496 MW nameplate, in the DISIS-2024-001 study cluster, connecting at the Norman Hills 345 kilovolt substation (OG&E). Row: McClain, OGE, CT, nameplate 496 MW, DISIS study phase, commercial operation January 1, 2030. The queue row is the only source. It is a study phase request with no interconnection agreement, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. No Oklahoma Corporation Commission cause, utility plan or news item was found that names this request. The queue row does not say combined cycle or simple cycle, so the technology is left unknown. The site is only the substation, so no coordinates are listed. I checked it against GEM's Oklahoma units by size, county and substation and found no match.

### SPP GEN-2024-128 Anadarko gas power station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2024-128 Anadarko gas power station in Oklahoma with owner left blank, then add the one unit below. Put SPP GEN-2024-128 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- `City`: `` -> `Anadarko`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Capacity (MW)`: `726.9`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2030`
- unit 1 `Turbine/Engine Technology`: `unknown`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. The SPP active queue lists GEN-2024-128 as a gas request of 726.9 MW nameplate, in the DISIS-2024-001 study cluster, connecting at the Gracemont to Lawton 345 kilovolt line (OG&E). Row: Anadarko, OGE, Gas, nameplate 726.9 MW, capacity 690 MW, DISIS study phase, commercial operation December 31, 2030. The queue row is the only source. It is a study phase request with no interconnection agreement, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. No Oklahoma Corporation Commission cause, utility plan or news item was found that names this request. The queue row does not say combined cycle or simple cycle, so the technology is left unknown. The site is only the substation, so no coordinates are listed. I checked it against GEM's Oklahoma units by size, county and substation and found no match.

### SPP GEN-2024-293 Muskogee 345 kilovolt gas power station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2024-293 Muskogee 345 kilovolt gas power station in Oklahoma with owner left blank, then add the one unit below. Put SPP GEN-2024-293 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Capacity (MW)`: `248`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2033`
- unit 1 `Turbine/Engine Technology`: `unknown`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. The SPP active queue lists GEN-2024-293 as a gas request of 248 MW nameplate, in the DISIS-2024-001 study cluster, connecting at the Muskogee 345 kilovolt substation (OG&E). Row: Oklahoma, OGE, Gas, nameplate 248 MW, DISIS study phase, commercial operation May 1, 2033. The queue row is the only source. It is a study phase request with no interconnection agreement, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. No Oklahoma Corporation Commission cause, utility plan or news item was found that names this request. The queue row does not say combined cycle or simple cycle, so the technology is left unknown. The site is only the substation, so no coordinates are listed. I checked it against GEM's Oklahoma units by size, county and substation and found no match.

### SPP GEN-2024-299 AES 5 345 kilovolt gas power station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2024-299 AES 5 345 kilovolt gas power station in Oklahoma with owner left blank, then add the one unit below. Put SPP GEN-2024-299 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Capacity (MW)`: `744`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2032`
- unit 1 `Turbine/Engine Technology`: `unknown`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. The SPP active queue lists GEN-2024-299 as a gas request of 744 MW nameplate, in the DISIS-2024-001 study cluster, connecting at the AES 5 345 kilovolt substation (OG&E). Row: Oklahoma, OGE, Gas, nameplate 744 MW, DISIS study phase, commercial operation May 1, 2032. The queue row is the only source. It is a study phase request with no interconnection agreement, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. No Oklahoma Corporation Commission cause, utility plan or news item was found that names this request. The queue row does not say combined cycle or simple cycle, so the technology is left unknown. The site is only the substation, so no coordinates are listed. I checked it against GEM's Oklahoma units by size, county and substation and found no match.

### SPP GEN-2024-321 Seminole gas power station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2024-321 Seminole gas power station in Oklahoma with owner left blank, then add the one unit below. Put SPP GEN-2024-321 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- `Local area (taluk, county)`: `` -> `Seminole`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Capacity (MW)`: `507`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2030`
- unit 1 `Turbine/Engine Technology`: `unknown`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. The SPP active queue lists GEN-2024-321 as a gas request of 507 MW nameplate, in the DISIS-2024-001 study cluster, connecting at the Seminole 345 kilovolt substation (OG&E). Row: Seminole, OGE, Gas, nameplate 507 MW, capacity 493 MW, DISIS study phase, commercial operation April 30, 2030. The queue row is the only source. It is a study phase request with no interconnection agreement, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. No Oklahoma Corporation Commission cause, utility plan or news item was found that names this request. The queue row does not say combined cycle or simple cycle, so the technology is left unknown. The site is only the substation, so no coordinates are listed. I checked it against GEM's Oklahoma units by size, county and substation and found no match.

### SPP GEN-2024-334 Kay County gas power station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2024-334 Kay County gas power station in Oklahoma with owner left blank, then add the one unit below. Put SPP GEN-2024-334 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- `Local area (taluk, county)`: `` -> `Kay`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Capacity (MW)`: `103`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2029`
- unit 1 `Turbine/Engine Technology`: `unknown`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. The SPP active queue lists GEN-2024-334 as a gas request of 103 MW nameplate, in the DISIS-2024-001 study cluster, connecting at the Ranch Road 345 kilovolt substation (OG&E). Row: Kay, OGE, Gas, nameplate 103 MW, DISIS study phase, commercial operation June 1, 2029. The queue row is the only source. It is a study phase request with no interconnection agreement, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. No Oklahoma Corporation Commission cause, utility plan or news item was found that names this request. The queue row does not say combined cycle or simple cycle, so the technology is left unknown. The site is only the substation, so no coordinates are listed. I checked it against GEM's Oklahoma units by size, county and substation and found no match.

### SPP GEN-2024-340 Creek County gas power station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2024-340 Creek County gas power station in Oklahoma with owner left blank, then add the one unit below. Put SPP GEN-2024-340 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- `Local area (taluk, county)`: `` -> `Creek`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Capacity (MW)`: `1440`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2032`
- unit 1 `Turbine/Engine Technology`: `unknown`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. The SPP active queue lists GEN-2024-340 as a gas request of 1440 MW nameplate, in the DISIS-2024-001 study cluster, connecting at the Riverside to Redbud 345 kilovolt line (AEP). Row: Creek, AEP, Gas, nameplate 1440 MW, capacity 1400 MW, DISIS study phase, commercial operation January 1, 2032. The queue row is the only source. It is a study phase request with no interconnection agreement, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. No Oklahoma Corporation Commission cause, utility plan or news item was found that names this request. The queue row does not say combined cycle or simple cycle, so the technology is left unknown. The site is only the substation, so no coordinates are listed. I checked it against GEM's Oklahoma units by size, county and substation and found no match.

### SPP GEN-2024-341 Pittsburg County gas power station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2024-341 Pittsburg County gas power station in Oklahoma with owner left blank, then add the one unit below. Put SPP GEN-2024-341 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- `Local area (taluk, county)`: `` -> `Pittsburg`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Capacity (MW)`: `1077.8`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2031`
- unit 1 `Turbine/Engine Technology`: `unknown`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. The SPP active queue lists GEN-2024-341 as a gas request of 1077.8 MW nameplate, in the DISIS-2024-001 study cluster, connecting at the Pittsburgh 345 kilovolt substation (AEP). Row: Pittsburgh, AEP, Gas, nameplate 1077.8 MW, capacity 1045 MW, DISIS study phase, commercial operation November 10, 2031. The queue row is the only source. It is a study phase request with no interconnection agreement, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. No Oklahoma Corporation Commission cause, utility plan or news item was found that names this request. The queue row does not say combined cycle or simple cycle, so the technology is left unknown. The site is only the substation, so no coordinates are listed. I checked it against GEM's Oklahoma units by size, county and substation and found no match.

### SPP GEN-2025-SR19 Maid diesel engine power station
*new plant; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2025-SR19 Maid diesel engine power station near Chouteau, Oklahoma, with owner left blank, then add the one engine unit below. Put SPP GEN-2025-SR19 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- `City`: `` -> `Chouteau`
- unit 1 `Fuel`: `fossil liquids: diesel`
- unit 1 `Capacity (MW)`: `100.76`
- unit 1 `Status`: `pre-construction`
- unit 1 `Start year`: `2029`
- unit 1 `Turbine/Engine Technology`: `internal combustion`
- unit 1 `Number Of Engines`: `31`
- unit 1 `Capacity Per Engine`: `3.25`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. SPP's surplus interconnection study for GEN-2025-SR19 describes a new set of 31 Cummins C3250 D6e diesel engines at the Maid 161 kilovolt substation, using spare capacity at the point where GEN-2019-002, a 101.5 MW battery already connects. The engines total 100.76 MW in the study table and the injection is capped at 100 MW. The queue row reads: Chouteau, Grand River Dam Authority area, 100 MW, IA FULLY EXECUTED/ON SCHEDULE, commercial operation November 30, 2029. The interconnection agreement is fully executed, which puts the status at pre-construction. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. Each engine is 4.063 megavolt-amperes, which is 3.25 MW at the usual power factor, so the engine count and the table total agree. The exact site is not given, only the substation, so no coordinates are listed. Whether these are backup engines for a data center or a stand-alone peaking plant is not stated in the study.

### SPP GEN-2025-SR21 Tulsa Power Station diesel engine power station
*new plant; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2025-SR21 Tulsa Power Station diesel engine power station near Tulsa, Oklahoma, with owner left blank, then add the one engine unit below. Put SPP GEN-2025-SR21 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- `City`: `` -> `Tulsa`
- unit 1 `Fuel`: `fossil liquids: diesel`
- unit 1 `Capacity (MW)`: `100.76`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2028`
- unit 1 `Turbine/Engine Technology`: `internal combustion`
- unit 1 `Number Of Engines`: `31`
- unit 1 `Capacity Per Engine`: `3.25`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. SPP's surplus interconnection study for GEN-2025-SR21 describes a new set of 31 Cummins C3250 D6e diesel engines at the Tulsa Power Station 138 kilovolt substation, using spare capacity at the point where GEN-2018-027, a 100 MW battery already connects. The engines total 100.76 MW in the study table and the injection is capped at 100 MW. The queue row reads: Tulsa, AEP area, 100 MW, IA PENDING, commercial operation May 31, 2028. The interconnection agreement is pending, which puts the status at announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. Each engine is 4.063 megavolt-amperes, which is 3.25 MW at the usual power factor, so the engine count and the table total agree. The exact site is not given, only the substation, so no coordinates are listed. Whether these are backup engines for a data center or a stand-alone peaking plant is not stated in the study.

### SPP GEN-2025-SR22 Horseshoe Lake diesel engine power station
*new plant; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2025-SR22 Horseshoe Lake diesel engine power station near Harrah, Oklahoma, with owner left blank, then add the one engine unit below. Put SPP GEN-2025-SR22 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- `City`: `` -> `Harrah`
- unit 1 `Fuel`: `fossil liquids: diesel`
- unit 1 `Capacity (MW)`: `100.76`
- unit 1 `Status`: `pre-construction`
- unit 1 `Start year`: `2030`
- unit 1 `Turbine/Engine Technology`: `internal combustion`
- unit 1 `Number Of Engines`: `31`
- unit 1 `Capacity Per Engine`: `3.25`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. SPP's surplus interconnection study for GEN-2025-SR22 describes a new set of 31 Cummins C3250 D6e diesel engines at the Horseshoe Lake 138 kilovolt substation, using spare capacity at the point where GEN-2018-029, a 100.7 MW battery already connects. The engines total 100.76 MW in the study table and the injection is capped at 100 MW. The queue row reads: Harrah, OG&E area, 100 MW, IA FULLY EXECUTED/ON SCHEDULE, commercial operation November 30, 2030. The interconnection agreement is fully executed, which puts the status at pre-construction. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. Each engine is 4.063 megavolt-amperes, which is 3.25 MW at the usual power factor, so the engine count and the table total agree. The exact site is not given, only the substation, so no coordinates are listed. Whether these are backup engines for a data center or a stand-alone peaking plant is not stated in the study.

### SPP GEN-2025-SR23 Mustang diesel engine power station
*new plant; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2025-SR23 Mustang diesel engine power station near Oklahoma City, Oklahoma, with owner left blank, then add the one engine unit below. Put SPP GEN-2025-SR23 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- `City`: `` -> `Oklahoma City`
- unit 1 `Fuel`: `fossil liquids: diesel`
- unit 1 `Capacity (MW)`: `100.76`
- unit 1 `Status`: `pre-construction`
- unit 1 `Start year`: `2029`
- unit 1 `Turbine/Engine Technology`: `internal combustion`
- unit 1 `Number Of Engines`: `31`
- unit 1 `Capacity Per Engine`: `3.25`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. SPP's surplus interconnection study for GEN-2025-SR23 describes a new set of 31 Cummins C3250 D6e diesel engines at the Mustang 138 kilovolt substation, using spare capacity at the point where GEN-2018-026, a 115.2 MW battery already connects. The engines total 100.76 MW in the study table and the injection is capped at 100 MW. The queue row reads: Oklahoma City, OG&E area, 100 MW, IA FULLY EXECUTED/ON SCHEDULE, commercial operation November 30, 2029. The interconnection agreement is fully executed, which puts the status at pre-construction. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. Each engine is 4.063 megavolt-amperes, which is 3.25 MW at the usual power factor, so the engine count and the table total agree. The exact site is not given, only the substation, so no coordinates are listed. Whether these are backup engines for a data center or a stand-alone peaking plant is not stated in the study.

### SPP GEN-2025-SR25 Tulsa North diesel engine power station
*new plant; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
**Action:** Create SPP GEN-2025-SR25 Tulsa North diesel engine power station near Sperry, Oklahoma, with owner left blank, then add the one engine unit below. Put SPP GEN-2025-SR25 in Other IDs.
- `State/Province`: `` -> `Oklahoma`
- `City`: `` -> `Sperry`
- unit 1 `Fuel`: `fossil liquids: diesel`
- unit 1 `Capacity (MW)`: `201.53`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2028`
- unit 1 `Turbine/Engine Technology`: `internal combustion`
- unit 1 `Number Of Engines`: `62`
- unit 1 `Capacity Per Engine`: `3.25`
  - Location Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list this project. SPP's surplus interconnection study for GEN-2025-SR25 describes a new set of 62 Cummins C3250 D6e diesel engines at the Tulsa North 138 kilovolt substation, using spare capacity at the point where GEN-2018-028, a 200 MW battery already connects. The engines total 201.53 MW in the study table and the injection is capped at 200 MW. The queue row reads: Sperry, AEP area, 200 MW, IA PENDING, commercial operation May 31, 2028. The interconnection agreement is pending, which puts the status at announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. Each engine is 4.063 megavolt-amperes, which is 3.25 MW at the usual power factor, so the engine count and the table total agree. The exact site is not given, only the substation, so no coordinates are listed. Whether these are backup engines for a data center or a stand-alone peaking plant is not stated in the study.

### Charles D. Lamb energy center / 2
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Add Unit 2 to the Charles D. Lamb energy center with the values listed, status pre-construction.
- `Unit name`: `` -> `2`
- `Capacity (MW)`: `` -> `90`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `pre-construction`
- `Start year`: `` -> `2028`
- `Owner(s)`: `` -> `Oklahoma Municipal Power Authority [100%]`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ac%C3%89PChnKuUSvuWZVQIFTvlUUq5X%C3%81Hzd9Glajj%C3%89H9yC3L05C3YHBOqpbheH2tQFiUXhjxRQlq2n6qKEna9J83FQI%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Fuel Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ac%C3%89PChnKuUSvuWZVQIFTvlUUq5X%C3%81Hzd9Glajj%C3%89H9yC3L05C3YHBOqpbheH2tQFiUXhjxRQlq2n6qKEna9J83FQI%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Status Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Aa4uMQdC7sAIwdopO3DGmSJ1fN6dFuZ2DF2LgcWnu1nPjwUZQst2jzAUeBwyDm8c3sU6S71OwLno%C3%81pg5HeNZltE%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Status Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ac%C3%89PChnKuUSvuWZVQIFTvlUUq5X%C3%81Hzd9Glajj%C3%89H9yC3L05C3YHBOqpbheH2tQFiUXhjxRQlq2n6qKEna9J83FQI%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Start Year Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ac%C3%89PChnKuUSvuWZVQIFTvlUUq5X%C3%81Hzd9Glajj%C3%89H9yC3L05C3YHBOqpbheH2tQFiUXhjxRQlq2n6qKEna9J83FQI%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Owners Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ac%C3%89PChnKuUSvuWZVQIFTvlUUq5X%C3%81Hzd9Glajj%C3%89H9yC3L05C3YHBOqpbheH2tQFiUXhjxRQlq2n6qKEna9J83FQI%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ac%C3%89PChnKuUSvuWZVQIFTvlUUq5X%C3%81Hzd9Glajj%C3%89H9yC3L05C3YHBOqpbheH2tQFiUXhjxRQlq2n6qKEna9J83FQI%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Ac%C3%89PChnKuUSvuWZVQIFTvlUUq5X%C3%81Hzd9Glajj%C3%89H9yC3L05C3YHBOqpbheH2tQFiUXhjxRQlq2n6qKEna9J83FQI%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Aa4uMQdC7sAIwdopO3DGmSJ1fN6dFuZ2DF2LgcWnu1nPjwUZQst2jzAUeBwyDm8c3sU6S71OwLno%C3%81pg5HeNZltE%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: high (independent: )
- notes: The Oklahoma Municipal Power Authority applied to the state environmental agency in May 2026 for a construction permit for one new 90 megawatt General Electric 7E.03 simple cycle natural gas turbine at its Lamb plant in Ponca City. The state agency's completeness letter is dated June 8, 2026, and a notice of filing for New Unit 2 ran in the Ponca City News on June 11, 2026. The application gives 2028 as the construction date, so 2028 is used as the start year. A Southwest Power Pool request matched to this plant shows 103 to 124 megawatts, which is likely a winter or study rating. The permit application figure is the manufacturer nameplate figure used here. The permit is still in technical review, so the status stays pre-construction until a permit is issued and work starts.

### McClain energy facility / 2
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Add a unit to McClain energy facility: 6 INDAR and Ingeteam synchronous gas-fired units of 21.7534 MW each, 130.5 MW in all, announced, start year 2029, owner left blank.
- `Unit name`: `` -> `2`
- `Capacity (MW)`: `` -> `130.52`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `announced`
- `Start year`: `` -> `2029`
- `Turbine/Engine Technology`: `` -> `internal combustion`
- `Number Of Engines`: `` -> `6`
- `Capacity Per Engine`: `` -> `21.7534`
  - Capacity Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR15.pdf (ok=True, contains_value=True)
  - Fuel Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR15.pdf (ok=True, contains_value=True)
  - Status Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
  - Status Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR15.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR15.pdf (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM has the plant but not this unit. SPP's surplus interconnection study for GEN-2025-SR15 describes 6 INDAR and Ingeteam synchronous gas-fired units of 21.7534 MW each, 130.5 MW in all, connecting at the McClain 138 kilovolt substation, shared with McClain units 1, 2 and 3 (648.6 MW). The queue row reads: Newcastle, OG&E area, 125 MW, IA PENDING, commercial operation December 1, 2029. The injection is capped at 125 MW, but the equipment adds up to more, and the listed capacity is the equipment total. The interconnection agreement is still pending, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. OG&E owns the existing units at this point, but a surplus request can come from a different company, so no owner is assumed. The study says synchronous gas-fired units without naming the engine maker's model, so the engine type is read from the unit size and count.

### Muskogee Generating Station / 7
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Add a unit to Muskogee Generating Station: 20 INDAR and Ingeteam synchronous gas-fired units of 21.0812 MW each, 421.6 MW in all, announced, start year 2029, owner left blank.
- `Unit name`: `` -> `7`
- `Capacity (MW)`: `` -> `421.62`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `announced`
- `Start year`: `` -> `2029`
- `Turbine/Engine Technology`: `` -> `internal combustion`
- `Number Of Engines`: `` -> `20`
- `Capacity Per Engine`: `` -> `21.0812`
  - Capacity Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR9_06112026.pdf (ok=True, contains_value=True)
  - Fuel Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR9_06112026.pdf (ok=True, contains_value=True)
  - Status Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
  - Status Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR9_06112026.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR9_06112026.pdf (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM has the plant but not this unit. SPP's surplus interconnection study for GEN-2025-SR9 describes 20 INDAR and Ingeteam synchronous gas-fired units of 21.0812 MW each, 421.6 MW in all, connecting at the Muskogee 345 kilovolt substation, shared with Muskogee units 4, 5 and 6 (1,908 MW). The queue row reads: Fort Gibson, OG&E area, 400 MW, IA PENDING, commercial operation December 1, 2029. The injection is capped at 400 MW, but the equipment adds up to more, and the listed capacity is the equipment total. The interconnection agreement is still pending, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. OG&E owns the existing units at this point, but a surplus request can come from a different company, so no owner is assumed. The study says synchronous gas-fired units without naming the engine maker's model, so the engine type is read from the unit size and count.

### River Valley power station / 3
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Add one new gas unit group of five simple-cycle turbines at the existing River Valley plant, pre-construction.
- `Unit name`: `` -> `3`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Capacity (MW)`: `` -> `1124`
- `Status`: `` -> `pre-construction`
- `Turbine/Engine Technology`: `` -> `gas turbine`
- `Number Of Engines`: `` -> `5`
- `Capacity Per Engine`: `` -> `224.8`
- `Owner(s)`: `` -> `Oklahoma Gas and Electric Co [100%]`
  - Capacity Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Af6FiOuAWfwTfP7%C3%89lBObAZu2%C3%81jK627i0ruRb1YVA9ucGjOJwUUHCsEMbR%C3%81V4w%C3%819YC3Cw0VwM4maTrcJLCxoanak%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Fuel Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Af6FiOuAWfwTfP7%C3%89lBObAZu2%C3%81jK627i0ruRb1YVA9ucGjOJwUUHCsEMbR%C3%81V4w%C3%819YC3Cw0VwM4maTrcJLCxoanak%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Status Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Af6FiOuAWfwTfP7%C3%89lBObAZu2%C3%81jK627i0ruRb1YVA9ucGjOJwUUHCsEMbR%C3%81V4w%C3%819YC3Cw0VwM4maTrcJLCxoanak%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Af6FiOuAWfwTfP7%C3%89lBObAZu2%C3%81jK627i0ruRb1YVA9ucGjOJwUUHCsEMbR%C3%81V4w%C3%819YC3Cw0VwM4maTrcJLCxoanak%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - Owners Data Source: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Af6FiOuAWfwTfP7%C3%89lBObAZu2%C3%81jK627i0ruRb1YVA9ucGjOJwUUHCsEMbR%C3%81V4w%C3%819YC3Cw0VwM4maTrcJLCxoanak%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM lists only the two coal units here. OG&E applied to ODEQ for a construction permit, number 2025-0187, to install five GE 7F.05 gas turbines of about 224.8 MW each, about 1,124 MW in total, while retiring the coal units. A second option in the same application is two combined-cycle blocks of about 1,280 MW. The Southwest Power Pool request GEN-2024-286 for 496 MW at the nearby 161 kV substation is a smaller figure than the permit, so the permit capacity is used and the mismatch is flagged in a question. The new unit is named 3 because GEM already lists units 1 and 2. The five turbines are one unit group of five engines. The owner is Oklahoma Gas and Electric, the applicant on the permit, and it already owns units 1 and 2.

### Seminole (OK) power station / 4
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Add a unit to Seminole (OK) power station: one GE gas-fired combustion turbine of 249 MW, announced, start year 2030, owner left blank.
- `Unit name`: `` -> `4`
- `Capacity (MW)`: `` -> `249`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `announced`
- `Start year`: `` -> `2030`
- `Turbine/Engine Technology`: `` -> `gas turbine`
  - Capacity Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR10_06-19-2026.pdf (ok=True, contains_value=True)
  - Fuel Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR10_06-19-2026.pdf (ok=True, contains_value=True)
  - Status Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
  - Status Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR10_06-19-2026.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR10_06-19-2026.pdf (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM has the plant but not this unit. SPP's surplus interconnection study for GEN-2025-SR10 describes one GE gas-fired combustion turbine of 249 MW, connecting at the Seminole 345 kilovolt substation, shared with Seminole units 2 and 3. The queue row reads: Konawa, OG&E area, 238 MW, IA PENDING, commercial operation April 30, 2030. The injection is capped at 238 MW, but the equipment adds up to more, and the listed capacity is the equipment total. The interconnection agreement is still pending, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. OG&E owns the existing units at this point, but a surplus request can come from a different company, so no owner is assumed. The study says synchronous gas-fired units without naming the engine maker's model, so the engine type is read from the unit size and count.

### Seminole (OK) power station / 5
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Add a unit to Seminole (OK) power station: 6 INDAR and Ingeteam synchronous gas-fired units of 21.7534 MW each, 130.5 MW in all, announced, start year 2029, owner left blank.
- `Unit name`: `` -> `5`
- `Capacity (MW)`: `` -> `130.52`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `announced`
- `Start year`: `` -> `2029`
- `Turbine/Engine Technology`: `` -> `internal combustion`
- `Number Of Engines`: `` -> `6`
- `Capacity Per Engine`: `` -> `21.7534`
  - Capacity Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR13_07-16-2026.pdf (ok=True, contains_value=True)
  - Fuel Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR13_07-16-2026.pdf (ok=True, contains_value=True)
  - Status Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
  - Status Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR13_07-16-2026.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://opsportal.spp.org/documents/studies/files/2025_Generation_Studies/FINAL_SPP_Report_GEN-2025-SR13_07-16-2026.pdf (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM has the plant but not this unit. SPP's surplus interconnection study for GEN-2025-SR13 describes 6 INDAR and Ingeteam synchronous gas-fired units of 21.7534 MW each, 130.5 MW in all, connecting at the Seminole 138 kilovolt substation, shared with Seminole unit 1. The queue row reads: Konawa, OG&E area, 125 MW, IA PENDING, commercial operation December 1, 2029. The injection is capped at 125 MW, but the equipment adds up to more, and the listed capacity is the equipment total. The interconnection agreement is still pending, so the status is announced. SPP does not publish the name of the company behind a queue request, and no regulator filing or news item naming it was found, so the owner is left blank for the reviewer. OG&E owns the existing units at this point, but a surplus request can come from a different company, so no owner is assumed. The study says synchronous gas-fired units without naming the engine maker's model, so the engine type is read from the unit size and count.

### G100001055235 / Anadarko power station / Roulet 12
*question about existing data; checklist rows 51 (Newly announced projects checked)*
- about: existence
- question: Should Roulet 12 and 13 have a federal EIA record yet?
- finding: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists no planned Oklahoma units at Anadarko plant 3006. The Oklahoma permit memorandum and trade press do describe the two turbines.
- recommendation: Leave both units as construction and recheck the next EIA monthly table due November 24, 2026.
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/8827.pdf (ok=None, contains_value=None)
- notes: I read the Southwest Power Pool open queue list on 5 November 2026 (https://opsportal.spp.org/Studies/GenerateActiveCSV). Entry GEN-2023-GR1 is a replacement request of 97.488 MW of gas at the Anadarko 69 kV plant connection, owned by the cooperative, with commercial operation shown as December 2025 and a cessation date of November 2025. Its size fits the two new 50.2 MW turbines, so it is not a third project. Its dates are earlier than the late 2026 completion reported in the press, and I found no report that the turbines are running. Entries GEN-2007-052 at 150 MW and GEN-2005-022 at 177 MW are older plants already in commercial operation and match existing units.

### G100001091022 / Cross Timbers Power Plant / 1
*question about existing data*
- about: duplicate
- question: Is SPP queue entry GEN-2024-321 the Cross Timbers plant?
- finding: The Southwest Power Pool queue at https://opsportal.spp.org/Studies/GIActive lists GEN-2024-321 as a 507 MW gas project in Seminole County, connecting at the Seminole 345 kV substation, with an OG&E owner label and a 2029 in service date. The Cross Timbers permit memorandum at https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf describes two turbines of up to 255 MW each at Section 36, Township 6N, Range 5E near Konawa. Two times 255 MW is 510 MW, close to 507 MW.
- recommendation: Do not add a new unit for GEN-2024-321 now. Leave the queue entry linked to the Seminole station, and ask the project manager to check the queue study documents to see whether OG&E is buying Cross Timbers output.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=None, contains_value=None)
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/9156.pdf (ok=None, contains_value=None)
- notes: Nothing I found ties Cross Timbers Power LLC to the queue entry. The queue names OG&E and a substation at the Seminole plant. A web search found no news about Cross Timbers Power. The point of interconnection is the main reason I think it is a different project.

### Fort James Muskogee Mill Power Plant
*question about existing data*
- about: duplicate
- question: Are the Georgia-Pacific gas steam turbines in the federal file the same units as GEM's Fort James Muskogee Mill coal units 2 and 3?
- finding: GEM lists Fort James units 2 and 3 at 45.5 MW each, coal, started 1979 and 1982, retired in 2020, with a note about conversion to gas. The federal file for September 2026 lists three operating natural gas steam turbines at the same mill of 25, 44.5 and 44.5 MW from 1979, 1980 and 1982.
- recommendation: Check the mill's air permit to see whether the turbines are the same. If they are, update the Fort James units to operating on gas and drop the new plant, and if not, keep the new plant and add a Notes line on both.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/3131.pdf (ok=True, contains_value=True)
- notes: The 2016 notice from the state environmental agency says the mill runs power boilers that feed steam turbines, and that one boiler would be replaced by a gas boiler. It does not give turbine sizes. The start years of 1979 and 1982 match GEM's two units closely, which points to the same machines. The federal plant code for Fort James in GEM is 362, and the new code is 10362.

### Grand River Energy Center
*question about existing data*
- about: duplicate
- question: Is Southwest Power Pool request GEN-2025-SR19 at the Maid 161 kV substation part of the Grand River Energy Center?
- finding: The request is for 100 MW, owned by the Grand River Dam Authority, with no fuel shown, near Chouteau, with commercial operation in November 2029 in the open list at https://opsportal.spp.org/Studies/GenerateActiveCSV, read on 5 November 2026. The Grand River Energy Center connects at its own 345 kV substation, which is a different connection point.
- recommendation: Keep GEN-2025-SR19 as its own new project and add no unit at the Grand River Energy Center.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=None, contains_value=None)
- notes: The queue list gives no site address or project name for this request. I found no air permit or board document that places it at the Grand River Energy Center.

### Hugo power station
*question about existing data*
- about: duplicate
- question: Is SPP request GEN-2024-323 at the ITC Hugo 7 substation the same project as GEM's Hugo Site B?
- finding: GEM lists Hugo Site B as 342 MW, pre-construction, due in 2029, owned by Western Farmers Electric Cooperative. The SPP queue has a 372 MW gas request in Choctaw County at the ITC Hugo 7 345 kilovolt substation with commercial operation on May 1, 2029. The county, year and size are close, but the queue does not name a company.
- recommendation: Treat GEN-2024-323 as Hugo Site B unless the cooperative says otherwise, add SPP GEN-2024-323 to Other IDs on Site B, and ask the cooperative whether the 372 MW nameplate is right.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- notes: Hugo Site A at 73.5 MW matches request GEN-2026-SR34, a 75 MW thermal surplus request at the WFEC Hugo 138 kilovolt point with commercial operation on April 1, 2029. Site B being 342 MW against 372 MW in the queue is a 30 MW gap that may be a rating difference.

### G100000401929 / McClain energy facility / G011
*question about existing data; checklist rows 51 (Newly announced projects checked)*
- about: existence
- question: Do the two Southwest Power Pool queue entries at McClain describe new units?
- finding: The Southwest Power Pool active queue lists GEN-2025-SR15 (125 MW, McClain Substation) and GEN-2024-013 (a 496 MW combustion turbine, Norman Hills 345 kV substation). The Norman Hills entry has an in-service date of April 2029. I did not find a permit or utility filing that ties either entry to the McClain site.
- recommendation: Leave GEM as it is. Ask the project manager whether to add GEN-2024-013 as an announced unit once a document names the McClain site.
- notes: The queue page is https://opsportal.spp.org/Studies/GIActive. It is drawn by script and I did not read the entries myself; the brief reported them from an earlier download. Not verified further because the brief task for this plant was only to recheck operation and Backup Power.

### G100000403752 / Mooreland power station / 2
*question about existing data*
- about: scope
- question: Should Mooreland unit 1 (45 MW) be listed in GEM?
- finding: The EIA-860M table for September 2026 lists three operating gas steam units at plant 3008: unit 1 at 45 MW (1964), unit 2 at 125 MW and unit 3 at 135 MW. GEM lists only units 2 and 3 here.
- recommendation: Check whether unit 1 is in GEM under another record. If not, it is below the 50 MW threshold, so leave it out.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: Source is the EIA-860M table at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx.

### G100000403312 / Mustang (OK) power station / 6-12
*question about existing data; checklist rows 51 (Newly announced projects checked)*
- about: existence
- question: Do the two Southwest Power Pool entries at Mustang describe new units?
- finding: The Southwest Power Pool queue lists GEN-2025-SR23, 100 MW with no fuel shown, at the Mustang 138 kV substation with an executed agreement, and GEN-2016-047, a 24 MW combustion turbine in service in December 2017 at Mustang 69 kV. The EIA table lists no unit of 24 MW at Mustang. Neither entry names a fuel or turbine for a new unit.
- recommendation: Leave GEM as is. Ask OG&E or look again at the next queue update to see whether SR23 is a gas unit, then add it as a new unit if so.
- notes: The queue page is https://opsportal.spp.org/Studies/GIActive . I could not load a per-project page. The Oklahoma Corporation Commission daily dockets showed no Mustang case.

### Peoples Electric Cooperative Centrahoma power station
*question about existing data*
- about: duplicate
- question: Should the Targa, Centrahoma and Little Dixie engine sites be one plant when each is under 50 MW alone?
- finding: The three sites are about one kilometer apart, share one owner and sum to 61.7 MW, matching one Southwest Power Pool entry of 61.725 MW. The federal monthly file lists them as three small plants.
- recommendation: Keep them as one plant with three units, and split them only if the manual treats separate permits as separate plants.
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Aevth4xmYyMYEUksZxJwUqGnaRaWfTbuqstqjNNkWYX43sTZcmwOpZkwiQnIvBom5aPYVRnVFqOmoareNhLZSGg%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - links: https://okdeqonbaseexternal.databankcloud.com/pav/api/Document/Adi%C3%81Uj4HU48j7TJinfPrZ7F99J8r2OmzRMCr78Mar5%C3%81iTb6ZjN92Z8hh1DZPsPqO7bKF3FxOM26IVudy91ABEfs%3D/?ViewerMode=PDF&ForceDownload=true (ok=True, contains_value=True)
  - links: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- notes: The owner name was not found in the entity list.

### Redbud power plant
*question about existing data*
- about: duplicate
- question: Is Southwest Power Pool entry ERAS-2025-003 at Redbud a new unit or the turbine upgrade?
- finding: The Southwest Power Pool entry ERAS-2025-003 lists a 186 MW combined cycle addition at the Redbud 345 kV substation, with commercial operation in January 2027. A state air permit memorandum (https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf) says the four existing combustion turbines are being upgraded, which raises the plant from about 1,268 MW to 1,490 MW. The 2026 OG&E resource plan (https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8) lists no new unit at Redbud.
- recommendation: Do not add a new unit. Treat the entry as the capacity increase of the four existing units, and consider raising each unit from 358 MW to about 372.5 MW once the upgrade is confirmed complete.
  - links: https://applications.deq.ok.gov/permitspublic/storedpermits/9021.pdf (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://ogeenergy.gcs-web.com/static-files/80b39a4f-b2b2-45cc-b848-efc9ba018dd8 (ok=None, contains_value=None)
  - links: https://opsportal.spp.org/Studies/GIActive (ok=True, contains_value=True)
- notes: I read the OG&E 2026 resource plan. Its list of planned additions names only Horseshoe Lake and Tinker, and its footnote says OG&E owns 51 percent of Redbud, which matches the shares in the database. I read the queue entry in the Southwest Power Pool open list on 5 November 2026 (https://opsportal.spp.org/Studies/GenerateActiveCSV). It names OG&E as the owner and gives no turbine count. The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) shows no planned generator at this plant. I did not find the other owners' shares in a document beyond the database values, so those stay as they are. A second check of the plan found: The SPP queue lists a 186 MW combined cycle request at the Redbud 345 kilovolt substation near Luther with a fully executed agreement, an in-service date of October 24, 2025 and commercial operation on January 18, 2027. GEM has four Redbud units of 358 MW, all operating. Ask OG&E whether this is a combined cycle uprate, and if it is add a note to the Redbud record without a new unit, otherwise add a 186 MW unit with start year 2027.

### G100000403319 / Seminole (OK) power station / 1
*question about existing data; checklist rows 51 (Newly announced projects checked)*
- about: existence
- question: Is the 507 MW gas queue entry GEN-2024-321 a new unit at Seminole?
- finding: The Southwest Power Pool queue page at https://opsportal.spp.org/Studies/GIActive lists GEN-2024-321 as a 507 MW gas project, queued March 2025, with a planned in-service date of March 2029 and a connection at the Seminole 345 kV substation. Two smaller entries, GEN-2025-SR10 at 238 MW and GEN-2025-SR13 at 125 MW, connect at the Seminole 345 kV and 138 kV substations with no fuel shown.
- recommendation: Ask the project manager whether these are expansions at the OG&E plant or separate projects near the substation. If at the plant, add a new announced unit for GEN-2024-321.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=None, contains_value=None)
- notes: A connection point at a substation does not prove the project sits at the plant site. The queue page gives no developer name or site address that I could read, and the 2026 OG&E plan names no new unit at Seminole. I did not find an air permit for a new unit at Seminole in the harvested permit file.

### G100000414190 / Stillwater Energy Center / IC
*question about existing data*
- about: duplicate
- question: Is Southwest Power Pool entry ASGI-2014-014 Ferguson the same as this plant?
- finding: The queue entry shows 56.4 MW, Payne County, a fully executed agreement and commercial operation. The EIA-860M table for September 2026 lists Stillwater Energy Center with three engines of 18.8 MW each, which sum to 56.4 MW, in service since July 2016.
- recommendation: Treat the queue entry as this plant and add no new unit. Leave the unit as it is.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: The queue page is https://opsportal.spp.org/Studies/GIActive. It names the entry but does not name the plant, so the match rests on matching capacity and county.

### G100000403433 / Tulsa power station / 2
*question about existing data; checklist rows 51 (Newly announced projects checked)*
- about: existence
- question: Should the 8.2 MW diesel unit IC1 at Tulsa be added?
- finding: The EIA table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists generator IC1, 8.2 MW petroleum liquids, internal combustion, operating since 1967.
- recommendation: Leave it out. It is below the 50 MW threshold.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: Retired unit 3 (95 MW, retired 2012) is also in EIA and before 2020.

## Checklist group Other

### G100001101631 / Bristow Energy Center / 1
*question about existing data*
- about: other
- question: Is SPP queue row GEN-2024-340 a different project from Bristow?
- finding: The Southwest Power Pool queue at https://opsportal.spp.org/Studies/GIActive lists GEN-2024-340 as 1,440 MW in Creek County for American Electric Power at the Riverside to Redbud line. That does not match a 420 MW Associated plant.
- recommendation: Treat it as another project. No queue row for Bristow was found.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=None, contains_value=None)
- notes: Associated may have a queue row under another county or name. The Oklahoma Department of Environmental Quality harvest found no air permit application for Bristow either. The permit records before 2016 are not online.

### G100000401815 / Green Country Energy power station / G841
*question about existing data*
- about: other
- question: Is there a document that states Backup Power for the Green Country units?
- finding: The EIA table and the news article do not state a Backup Power value. The plant sells to the grid.
- recommendation: Leave Backup Power as no and add the EIA table for September 2026 as its source if a source is required.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: I did not search the Oklahoma Department of Environmental Quality air permit files for Green Country beyond the harvested index, which holds a water discharge permit renewal and a 2003 major source permit, neither of which states backup use.

### G100001048466 / Horseshoe Lake power station / 11
*question about existing data*
- about: other
- question: Is there a document that states Backup Power for the Horseshoe Lake units?
- finding: I found no document that says whether any Horseshoe Lake unit is a backup power unit. All sources describe the units as grid supply for OG&E customers.
- recommendation: Leave Backup Power as no on all ten units and leave the source box empty.
- notes: Searched the 2026 OG&E plan, the September 2026 news release and EIA-860M. None uses the term.

### G100000401944 / Kiamichi energy facility / STG1
*question about existing data*
- about: other
- question: Is there a document that states Backup Power for the Kiamichi units?
- finding: The EIA table and the Tenaska fact sheet do not state a Backup Power value. The plant sells power into the grid.
- recommendation: Leave Backup Power as no.
  - links: http://www.tenaska.com/wp-content/uploads/2020/03/Kiamichi.pdf (ok=None, contains_value=None)
- notes: A Title V air permit renewal, number 2026-0277-ARR4, is under review at the Oklahoma Department of Environmental Quality. I did not open its documents for this check.

## Checklist group 9. Close-out

Not record-level: the sheet and doc updates, research status, and the two database checks. These boxes are ticked by hand after the edits are applied: validation_report.py --closeout must print CLOSE-OUT CLEAN (row 54) and no_tracker.py lists the units with no tracker (row 56).
