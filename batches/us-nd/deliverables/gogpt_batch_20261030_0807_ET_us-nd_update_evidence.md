# Evidence — gogpt batch 20261030_0807_ET (us-nd, update)

Each section below is one group of the GOGPT QC/Country checklist. The records in it are the evidence for ticking that group's boxes; the row numbers are the checklist tab's own.

## Utility resource plans (checklist row 37)

The IRP step read 3 utility rows of the US IRPs tab for this state. The records below come from a plan; the actions workbook's irp_box sheet says which units need the IRP box ticked, and its irp_notes_draft sheet has a draft line per utility for the tab's Notes column.

- Montana-Dakota Utilities (MDU): ND 2024 IRP Vol. IV. Tracked plants matched: 1
- Otter Tail Power (OTP): IRP approved by ND PSC (Dec 4, 2024)
- Minnkota Power Cooperative: 2022 INTEGRATED RESOURCE PLAN (2022 – 2036). Tracked plants matched: 3

Records from a plan:
- G100001101376 / Minnkota Power Cass power station / 1: change to an existing unit, from the Minnkota Power Cooperative plan
- G100001094121 / Polaris Forge 2 power station / 1: question about existing data, from the Minnkota Power Cooperative plan
- G100001094121 / Polaris Forge 2 power station / 1: question about existing data, from the Minnkota Power Cooperative plan
- Otter Tail Power 50 MW gas plant in the 2027 to 2041 plan: watch item, new to the tracker, from the Otter Tail Power (OTP) plan
- Coyote Station replacement turbines in Montana-Dakota's 2024 plan: watch item, new to the tracker, from the Montana-Dakota Utilities (MDU) plan

## Checklist group 1. Validation report

Edits and questions that fix an error from the GEM validation report.

### G100000403194 / Heskett Station / Unit 3
*change to an existing unit; checklist rows 7 (Validation report errors fixed), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of all 2 units of Heskett Station as Montana-Dakota Utilities Co [100%]. It is still correct. Add the link below to the Owners Data Source box on each unit. Keep the links already there.
- `Owner(s)`: `Montana-Dakota Utilities Co [100%]` -> `Montana-Dakota Utilities Co [100%]`
  - Owners Data Source: https://www.psc.nd.gov/webdocs/case/19-0307/001-010.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: Montana-Dakota's application in case PU-19-307 asks to own and operate Heskett 4 and calls Heskett Unit 3 its own unit. The commission order in case PU-25-280 from February 2026 also names Montana-Dakota Utilities Co. as the owner of the Heskett units 1 and 2 assets. Both units 3 and 4 are therefore owned by Montana-Dakota. The value matches GEM.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*change to an existing unit; checklist rows 7 (Validation report errors fixed)*
**Action:** Leave CCS attachment? of unit Unit 1, timepoint 2 (G100001017988) as no. It is still correct. Add the 2 links below to the CCS Data Source box. Keep the links already there.
- `CCS attachment?`: `no` -> `no`
  - CCS Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/68774514989013349 (ok=True, contains_value=True)
  - CCS Data Source: https://www.psc.nd.gov/webdocs/case/25-0263/001-010.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The air permit renewal application of October 2025 (https://ceris.deq.nd.gov/ext/ncore/downloadpdf/68774514989013349) proposes a yearly megawatt-hour limit so that Unit 1 is exempt from the carbon capture rules, which means no capture equipment is installed. The Otter Tail Power filing in commission case PU-25-263 (https://www.psc.nd.gov/webdocs/case/25-0263/001-010.pdf) describes a separate DSA Capture Company carbon capture facility next to the ethanol plant in the Spiritwood Energy Park. It is not attached to the power plant.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*change to an existing unit; checklist rows 7 (Validation report errors fixed), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of unit Unit 1, timepoint 2 (G100001017988) as Great River Energy Cooperative [100%]. It is still correct. Add the 2 links below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Great River Energy Cooperative [100%]` -> `Great River Energy Cooperative [100%]`
  - Owners Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/68774514989013349 (ok=True, contains_value=True)
  - Owners Data Source: https://www.psc.nd.gov/webdocs/case/26-0279/001-010.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The air permit renewal application of October 2025 (https://ceris.deq.nd.gov/ext/ncore/downloadpdf/68774514989013349) names Great River Energy as the permit holder for Spiritwood Station. The 2026 ten-year plan (https://www.psc.nd.gov/webdocs/case/26-0279/001-010.pdf) lists the station in Great River Energy's own portfolio. The EIA-860M table for September 2026 also lists Great River Energy as the entity. No document gives a share, but none names another owner. The value matches GEM.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*change to an existing unit; checklist rows 7 (Validation report errors fixed), 25 (Location data for every entry), 42 (Exact location for approximate operating units (optional))*
**Action:** Leave the point of unit Unit 1, timepoint 2 (G100001017988) as it is. Add the 2 links below to the Location Data Source box. Keep the links already there.
- `Latitude`: `46.9255110` -> `46.9255110`
- `Longitude`: `-98.5021730` -> `-98.5021730`
- `Location accuracy`: `exact` -> `exact`
- location now: 46.9255110, -98.5021730 (exact) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=46.92551,-98.50217&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=46.92551,-98.50217)
- location proposed: 46.9255110, -98.5021730 (exact) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=46.92551,-98.50217&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=46.92551,-98.50217)
  - Location Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/68774514989013349 (ok=True, contains_value=True)
  - Location Data Source: https://www.google.com/maps/search/?api=1&query=46.92551,-98.50217 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The air permit renewal application of October 2025 (https://ceris.deq.nd.gov/ext/ncore/downloadpdf/68774514989013349) gives the site as latitude 46.92589 and longitude -98.50071. That is about 120 meters from GEM's point, so GEM's point stays. The EIA-860M table for September 2026 has 46.92642, -98.49971, about 210 meters away. All three are the same site. See the latitude note. The permit application point is about 120 meters from GEM's longitude, so no change. Coordinates stated in a permit application make the point exact under the manual. GEM already shows exact.

### G100000403194 / Heskett Station / Unit 3
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- question: What document gives the Heskett owner that the validation report found unsourced?
- finding: Case PU-19-307 (https://www.psc.nd.gov/webdocs/case/19-0307/001-010.pdf) shows Montana-Dakota Utilities owns the Heskett site and Heskett Unit 3. It states no other owner.
- recommendation: Add the commission filing in case PU-19-307 as the Owners Data Source and leave the value as is.
  - links: https://www.psc.nd.gov/webdocs/case/19-0307/001-010.pdf (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: The September 2026 EIA-860M table lists Montana-Dakota Utilities Co. as the plant's entity.

### G100000403835 / Heskett Station / Unit 4
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- question: Which unit did Heskett unit 4 replace?
- finding: The Montana-Dakota application in case PU-19-307 (https://www.psc.nd.gov/webdocs/case/19-0307/001-010.pdf) says Heskett 4 serves customers after the retirement of the coal units Heskett 1 and Heskett 2. A February 2026 commission order in case PU-25-280 (https://www.psc.nd.gov/webdocs/case/25-0280/013-010.pdf) confirms those two units are retired.
- recommendation: Link Heskett unit 4 to GEM unit G100000103860 (Heskett Unit 1) and G100000103861 (Heskett Unit 2), replacing the link to ID 0. If only one link is allowed, use G100000103861.
  - links: https://www.psc.nd.gov/webdocs/case/19-0307/001-010.pdf (ok=None, contains_value=None)
  - links: https://www.psc.nd.gov/webdocs/case/25-0280/013-010.pdf (ok=None, contains_value=None)
- notes: The same application also names Lewis and Clark 1 in Montana as retired for the same need. That plant is not part of this one.

## Checklist group 2. Blanks and unknowns

Empty or unknown cells that the research filled, and the ones it could not.

### G100001101353 / Applied Digital ELN Generation Plant / ELN02
*change to an existing unit; checklist rows 25 (Location data for every entry), 42 (Exact location for approximate operating units (optional))*
**Action:** Set Latitude of all 4 units of Applied Digital ELN Generation Plant to 46.01438, Longitude to -98.57427 and Location accuracy to exact. They now say 46.0217800, -98.5736000 and approximate, about 824 m away. Add the 3 links below to the Location Data Source box on each unit. Keep the links already there.
- `Latitude`: `46.0217800` -> `46.01438`
- `Longitude`: `-98.5736000` -> `-98.57427`
- `Location accuracy`: `approximate` -> `exact`
- location now: 46.0217800, -98.5736000 (approximate) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=46.02178,-98.57360&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=46.02178,-98.57360)
- location proposed: 46.01438, -98.57427 (exact) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=46.01438,-98.57427&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=46.01438,-98.57427)
- moved: 824 m
- method: published
  - Location Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Location Data Source: https://www.openstreetmap.org/way/1422191450 (ok=True, contains_value=True)
  - Location Data Source: https://www.google.com/maps/search/?api=1&query=46.01438,-98.57427 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit from the North Dakota Department of Environmental Quality, https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf, gives the ELN Generation Plant address as 9663 87th Ave. SE, Ellendale. The department's site record for that address, Applied Digital Corporation ELN Building 1 GEN Plant, https://ceris.deq.nd.gov/ext/nsite/DEFAULT/map/results/detail/-8841860088109998100/detail, holds both air permits for the engines, ACP-18296 and ACP-18338. The department's site map service places that record at 46.014383, -98.574269. That page is drawn by a script, so I read the point from the map service the page calls. OpenStreetMap maps the campus as Applied Digital / Ellendale Data Center, https://www.openstreetmap.org/way/1422191450, and the department's point falls inside that outline. The new point is 46.01438, -98.57427, about 820 meters south of the database point. So the plant is exact, by coordinates a government body published, backed by the OpenStreetMap outline. Satellite imagery of unknown date shows the existing data halls just south of the point and a new building under construction just east of it. The draft permit lists 60 Caterpillar 3516E engines in building ELN02, matching the database. No start year or operating date is stated. The project is moving, so Latest Activity is left alone.

### G100000402504 / Lonesome Creek Station / 1
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 1 (G100000402504) as 61.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `61.0` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW nameplate for this unit. GEM shows 61.0 MW, which is the same figure rounded up, so no change is needed.

### G100000402504 / Lonesome Creek Station / 1
*change to an existing unit; checklist rows 17 (Unknown technology rechecked)*
**Action:** Set Turbine/Engine Technology of unit 1 (G100000402504) to aeroderivative gas turbine. It now says gas turbine. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `gas turbine` -> `aeroderivative gas turbine`
  - Turbine/Engine Technology Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The North Dakota air quality draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE LM6000 PF Sprint simple cycle gas turbines. The LM6000 is an aeroderivative turbine, but the permit does not use that word. GEM now says gas turbine.

### G100000402504 / Lonesome Creek Station / 1
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Number Of Engines of unit 1 (G100000402504) to 1. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `` -> `1`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf lists each unit as one LM6000 turbine, so each unit has one engine.

### G100000402504 / Lonesome Creek Station / 1
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Capacity Per Engine of unit 1 (G100000402504) to 61.0. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Each unit is one turbine, so the capacity per engine equals the unit capacity of 61.0 MW. The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW.

### G100000402505 / Lonesome Creek Station / 2
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 2 (G100000402505) as 61.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `61.0` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW nameplate for this unit. GEM shows 61.0 MW, which is the same figure rounded up, so no change is needed.

### G100000402505 / Lonesome Creek Station / 2
*change to an existing unit; checklist rows 17 (Unknown technology rechecked)*
**Action:** Set Turbine/Engine Technology of unit 2 (G100000402505) to aeroderivative gas turbine. It now says gas turbine. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `gas turbine` -> `aeroderivative gas turbine`
  - Turbine/Engine Technology Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The North Dakota air quality draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE LM6000 PF Sprint simple cycle gas turbines. The LM6000 is an aeroderivative turbine, but the permit does not use that word. GEM now says gas turbine.

### G100000402505 / Lonesome Creek Station / 2
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Number Of Engines of unit 2 (G100000402505) to 1. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `` -> `1`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf lists each unit as one LM6000 turbine, so each unit has one engine.

### G100000402505 / Lonesome Creek Station / 2
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Capacity Per Engine of unit 2 (G100000402505) to 61.0. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Each unit is one turbine, so the capacity per engine equals the unit capacity of 61.0 MW. The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW.

### G100000402506 / Lonesome Creek Station / 3
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 3 (G100000402506) as 61.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `61.0` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW nameplate for this unit. GEM shows 61.0 MW, which is the same figure rounded up, so no change is needed.

### G100000402506 / Lonesome Creek Station / 3
*change to an existing unit; checklist rows 17 (Unknown technology rechecked)*
**Action:** Set Turbine/Engine Technology of unit 3 (G100000402506) to aeroderivative gas turbine. It now says gas turbine. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `gas turbine` -> `aeroderivative gas turbine`
  - Turbine/Engine Technology Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The North Dakota air quality draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE LM6000 PF Sprint simple cycle gas turbines. The LM6000 is an aeroderivative turbine, but the permit does not use that word. GEM now says gas turbine.

### G100000402506 / Lonesome Creek Station / 3
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Number Of Engines of unit 3 (G100000402506) to 1. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `` -> `1`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf lists each unit as one LM6000 turbine, so each unit has one engine.

### G100000402506 / Lonesome Creek Station / 3
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Capacity Per Engine of unit 3 (G100000402506) to 61.0. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Each unit is one turbine, so the capacity per engine equals the unit capacity of 61.0 MW. The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW.

### G100000402507 / Lonesome Creek Station / 4
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 4 (G100000402507) as 61.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `61.0` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW nameplate for this unit. GEM shows 61.0 MW, which is the same figure rounded up, so no change is needed.

### G100000402507 / Lonesome Creek Station / 4
*change to an existing unit; checklist rows 17 (Unknown technology rechecked)*
**Action:** Set Turbine/Engine Technology of unit 4 (G100000402507) to aeroderivative gas turbine. It now says gas turbine. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `gas turbine` -> `aeroderivative gas turbine`
  - Turbine/Engine Technology Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The North Dakota air quality draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE LM6000 PF Sprint simple cycle gas turbines. The LM6000 is an aeroderivative turbine, but the permit does not use that word. GEM now says gas turbine.

### G100000402507 / Lonesome Creek Station / 4
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Number Of Engines of unit 4 (G100000402507) to 1. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `` -> `1`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf lists each unit as one LM6000 turbine, so each unit has one engine.

### G100000402507 / Lonesome Creek Station / 4
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Capacity Per Engine of unit 4 (G100000402507) to 61.0. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Each unit is one turbine, so the capacity per engine equals the unit capacity of 61.0 MW. The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW.

### G100000402508 / Lonesome Creek Station / 5
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 5 (G100000402508) as 61.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `61.0` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW nameplate for this unit. GEM shows 61.0 MW, which is the same figure rounded up, so no change is needed.

### G100000402508 / Lonesome Creek Station / 5
*change to an existing unit; checklist rows 17 (Unknown technology rechecked)*
**Action:** Set Turbine/Engine Technology of unit 5 (G100000402508) to aeroderivative gas turbine. It now says gas turbine. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `gas turbine` -> `aeroderivative gas turbine`
  - Turbine/Engine Technology Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The North Dakota air quality draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE LM6000 PF Sprint simple cycle gas turbines. The LM6000 is an aeroderivative turbine, but the permit does not use that word. GEM now says gas turbine.

### G100000402508 / Lonesome Creek Station / 5
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Number Of Engines of unit 5 (G100000402508) to 1. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `` -> `1`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf lists each unit as one LM6000 turbine, so each unit has one engine.

### G100000402508 / Lonesome Creek Station / 5
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Capacity Per Engine of unit 5 (G100000402508) to 61.0. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Each unit is one turbine, so the capacity per engine equals the unit capacity of 61.0 MW. The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW.

### G100000409510 / Lonesome Creek Station / 6
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 6 (G100000409510) as 61.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `61.0` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW nameplate for this unit. GEM shows 61.0 MW, which is the same figure rounded up, so no change is needed.

### G100000409510 / Lonesome Creek Station / 6
*change to an existing unit; checklist rows 17 (Unknown technology rechecked)*
**Action:** Set Turbine/Engine Technology of unit 6 (G100000409510) to aeroderivative gas turbine. It now says gas turbine. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `gas turbine` -> `aeroderivative gas turbine`
  - Turbine/Engine Technology Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The North Dakota air quality draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE LM6000 PF Sprint simple cycle gas turbines. The LM6000 is an aeroderivative turbine, but the permit does not use that word. GEM now says gas turbine.

### G100000409510 / Lonesome Creek Station / 6
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Number Of Engines of unit 6 (G100000409510) to 1. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `` -> `1`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf lists each unit as one LM6000 turbine, so each unit has one engine.

### G100000409510 / Lonesome Creek Station / 6
*change to an existing unit; checklist rows 16 (Zero-capacity units rechecked)*
**Action:** Set Capacity Per Engine of unit 6 (G100000409510) to 61.0. The box is empty now. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `` -> `61.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Each unit is one turbine, so the capacity per engine equals the unit capacity of 61.0 MW. The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx gives 60.5 MW.

### G100001096407 / Nakota Data Center Campus Power Plant / 1
*change to an existing unit; checklist rows 25 (Location data for every entry)*
**Action:** Set Latitude of all 3 units of Nakota Data Center Campus Power Plant to 48.10124, Longitude to -103.87389 and Location accuracy to approximate. They now say 48.3479511, -103.4875743 and approximate, about 39.6 km away. Add the 3 links below to the Location Data Source box on each unit. Keep the links already there.
- `Latitude`: `48.3479511` -> `48.10124`
- `Longitude`: `-103.4875743` -> `-103.87389`
- `Location accuracy`: `approximate` -> `approximate`
- location now: 48.3479511, -103.4875743 (approximate) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=48.34795,-103.48757&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=48.34795,-103.48757)
- location proposed: 48.10124, -103.87389 (approximate) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=48.10124,-103.87389&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=48.10124,-103.87389)
- moved: 39.6 km
- method: georeferenced from a map in a document
- map render: [staging/maps/L100001084854.jpg](staging/maps/L100001084854.jpg)
  - control point: northwest oil well pad at pixel 854.0,273.9 is 48.11044, -103.87185
  - control point: north oil well pad at pixel 901.3,274.6 is 48.11033, -103.86754
  - control point: east oil well pad at pixel 962.3,301.8 is 48.10735, -103.8618
  - control point: road corner at the northeast of section 1 at pixel 948.8,266.3 is 48.11124, -103.86312
- fit error: 1.9 m
- needs a second look: yes
  - Location Data Source: https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm (ok=True, contains_value=True)
  - Location Data Source: https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/image_062.jpg (ok=True, contains_value=False)
  - Location Data Source: https://www.google.com/maps/search/?api=1&query=48.10124,-103.87389 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The binding letter of intent filed by Nixxy with the Securities and Exchange Commission in 2026 carries the developer's project slides at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm. Its site rendering slide, drawn by JLG Architects as project JLG 250082, shows an aerial photo of the campus parcel at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/image_062.jpg. I matched that photo to Esri satellite imagery using three oil well pads and a road corner. The match is close, with a fit error of about 2 meters. The parcel is in section 1 of township 153 north, range 103 west, about 20 kilometers west-southwest of downtown Williston and about 4 kilometers north-northeast of Trenton. The same slides include a map of the gas pipelines at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/image_065.jpg that shades a parcel in the same section. The point is the middle of the campus parcel. The slides do not show where the power plant sits inside the campus, so the point stays approximate. The pin link for the new point is https://www.google.com/maps/search/?api=1&query=48.10124,-103.87389. The new point is the middle of the campus parcel shown in the developer's site rendering in the letter of intent at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm. The slides do not show where the turbines will stand inside the parcel. So the accuracy stays approximate. If the reviewer accepts the parcel match, the point could be marked exact. No Public Service Commission case or Department of Environmental Quality air permit was found for Tachyon9, Nixxy or Nakota. The news is from June and July 2026, so the project is active. The move is about 40 kilometers, far more than 2 kilometers. The slides also say in words that the campus is 5 miles west of Williston, but the parcel in their own aerial photo is about 12 miles west-southwest of downtown. The control points were read from a small photo in a slide, and the point is the middle of the parcel, not a known turbine location. The imagery date is unknown, and no construction is visible at the parcel.

### G100000413122 / Pioneer generating station / 4-2
*change to an existing unit*
**Action:** Leave Number Of Engines of unit 4-2 (G100000413122) as 6. It is still correct. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `6` -> `6`
  - Capacity Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/2211455608767769004 (ok=True, contains_value=True)
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The air permit to construct application for phase IV lists six gas engines. The EIA table lists six engine generators, 31 to 36.

### G100000413122 / Pioneer generating station / 4-2
*change to an existing unit*
**Action:** Leave Capacity Per Engine of unit 4-2 (G100000413122) as 18.8. It is still correct. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `18.8` -> `18.8`
  - Capacity Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/2211455608767769004 (ok=True, contains_value=True)
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The air permit to construct application gives 18.8 MW for each engine, and the EIA table lists 18.8 MW for each of generators 31 to 36.

### G100000413124 / Pioneer generating station / IC
*change to an existing unit*
**Action:** Leave Number Of Engines of unit IC (G100000413124) as 12. It is still correct. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `12` -> `12`
  - Capacity Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/8220580009086318601 (ok=True, contains_value=True)
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The air permit lists twelve engines, and the EIA table lists twelve engine generators, 11 to 22.

### G100000413124 / Pioneer generating station / IC
*change to an existing unit*
**Action:** Leave Capacity Per Engine of unit IC (G100000413124) as 9.3. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `9.3` -> `9.3`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA table lists 9.3 MW for each of generators 11 to 22.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit Unit 1, timepoint 2 (G100001017988) as 106.2. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `106.2` -> `106.2`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) shows plant 56786, generator 1, status OP, nameplate 106.2 MW, operating year 2014. This is a live replacement for the dead Great River Energy fact sheet. The utility's own ten-year plan lists 99 MW, which is a lower generating capability figure, so GEM keeps the nameplate.

### G100001101353 / Applied Digital ELN Generation Plant / ELN02
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Should the Ellendale engine plant move to the point the air quality division publishes for it?
- finding: The air quality division's site record for the permitted generator plant, at 9663 87th Ave. SE, sits at 46.01438, -98.57427. The database point, 46.02178, -98.57360, is about 76 meters from a separate stormwater construction record named Applied Digital ELN-03, which the department places at 46.0211, -98.573731.
- recommendation: Move the plant point to 46.01438, -98.57427 and mark it exact, since both engine air permits sit on that site record.
  - links: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=None, contains_value=None)
  - links: https://www.openstreetmap.org/way/1422191450 (ok=None, contains_value=None)
  - links: https://www.google.com/maps/search/?api=1&query=46.01438,-98.57427 (ok=None, contains_value=None)
- notes: The first look used the street address geocoded to 46.01096, -98.56866. That point sits on the road at the southeast corner of the campus, about 450 meters from the department's point. The ELN-03 record covers a construction stormwater permit, NDR113237, and no air permit, so the database point may mark the ELN03 engine building site rather than the generator plant record. The site record page is https://ceris.deq.nd.gov/ext/nsite/DEFAULT/map/results/detail/-8841860088109998100/detail. It is drawn by a script, so the coordinates were read from the department's map search service and could not be checked by text match on the page. Imagery of the database point shows farmland, but the imagery date is unknown and may be older than construction.

### G100001101351 / Applied Digital FAR Generation Plant / FAR01
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Can the Harwood plant point be made exact from the 6805 County Road 81 address?
- finding: The air quality analysis at https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf gives the site address as 6805 County Road 81, Harwood, ND 58042. The geocoder found no match for that address, and only placed Harwood town about 2.4 km from GEM's point.
- recommendation: Leave the point as approximate. Place 6805 County Road 81 using Cass County parcel records or a map and then mark it exact.
  - links: https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf (ok=None, contains_value=None)
- notes: I tried the geocoder with several spellings. A web search found a data center listing with the same address but no coordinates. A satellite image of GEM's point, Esri World Imagery at zoom 15, shows bare farm fields east of Interstate 29 near Harwood, with no buildings yet. The imagery is older than the construction, so it cannot place the plant. The Internet Archive was offline during this pass, so older Harwood notices could not be read there.

### G100001101351 / Applied Digital FAR Generation Plant / FAR01
*question about existing data*
- about: source
- question: Should the permit number on the June 2026 Harwood notice letter be treated as a typo?
- finding: The notice letter at https://deq.nd.gov/aq/Notices/AppliedDigital/20260611BaylisLtrandNOT.pdf names the FAR Generation Plant but its comment line gives permit ACP-18338 version 1.0, which is the Ellendale permit. The analysis at https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf says ACP-18345 version 1.0.
- recommendation: Use ACP-18345 for Harwood and treat the letter's number as a copy error.
  - links: https://deq.nd.gov/aq/Notices/AppliedDigital/20260611BaylisLtrandNOT.pdf (ok=None, contains_value=None)
  - links: https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf (ok=None, contains_value=None)
- notes: The commission case PU-26-155 covers the Ellendale site per the earlier pass and does not name Harwood.

### G100001101332 / Base Electron power station / 1
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- question: Is the Sierra Club's Applied Digital Natural Gas Plant units 1 to 4 this plant?
- finding: Only Base Electron has four 300 MW natural gas steam units in North Dakota. Polaris Forge 1 is 400 MW and Polaris Forge 2 is 280 MW in GEM, and the Applied Digital engine plants are 3 MW diesel engine sets.
- recommendation: Treat the Sierra Club row as Base Electron power station and add no new plant for it.
  - links: https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses (ok=None, contains_value=None)
  - links: https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm (ok=None, contains_value=None)
- notes: The Babcock and Wilcox release at https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses gives four 300 MW boilers with steam turbines for Applied Digital campuses, and the quarterly report at https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm ties the 1,200 MW plant to Polaris Forge 3. I could not open the Sierra Club list as a citable source, so this rests on the matching size and unit count.

### G100001101332 / Base Electron power station / 1
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Can the Base Electron point be improved beyond GEM's approximate point near Center?
- finding: Montana-Dakota Utilities filings PU-26-219 and PU-26-236 place the Applied Digital campus in Section 24, Township 142 North, Range 85 West, Oliver County, west of Center. GEM's point is 47.09400, -101.27980, about 2.9 km from the town of Center at 47.11639, -101.29959.
- recommendation: Leave the point as approximate. A person should convert the section and township to a point or find the county conditional use permit 1105 site map.
  - links: https://s25.q4cdn.com/697625600/files/doc_news/Montana-Dakota-Utilities-Announces-Electric-Service-Agreement-with-Applied-Digital-for-Proposed-AI-Factory-2026.pdf (ok=None, contains_value=None)
- notes: The filings are at https://www.psc.nd.gov/webdocs/case/26-0219/ and https://www.psc.nd.gov/webdocs/case/26-0236/. I did not convert the survey description into coordinates or look at satellite imagery, and the campus is not confirmed to be the power plant site. The Oliver County permit documents were behind a sign-in page.

### G100001101376 / Minnkota Power Cass power station / 1
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Should the Minnkota plant point move near the Bison Substation?
- finding: The article at https://northdakotamonitor.com/2026/10/06/minnkota-plans-gas-fired-power-plant-in-cass-county-adding-to-energy-development/ says the land is in Harmony Township north of Mapleton, near the Bison Substation at the end of an existing WBI Energy gas pipeline. A 2018 commission filing at https://www.psc.nd.gov/webdocs/case/18-0219/064-130.pdf places that substation in Section 11 of Township 140 North, Range 51 West. A map in that filing labels a point near 46.94188, -97.10511.
- recommendation: Keep GEM's point for now and ask the project manager whether to use the substation area, about 3 km from GEM's point, as an approximate location until Minnkota files a site.
  - links: https://northdakotamonitor.com/2026/10/06/minnkota-plans-gas-fired-power-plant-in-cass-county-adding-to-energy-development/ (ok=None, contains_value=None)
  - links: https://www.psc.nd.gov/webdocs/case/18-0219/064-130.pdf (ok=None, contains_value=None)
- notes: A satellite picture at that point shows farm fields and no substation, and the imagery date is unknown, so I could not confirm the point. No address, parcel number or permit map for the plant was found. A geocode of Harmony Township gave 46.92729, -97.11547.

### G100001096407 / Nakota Data Center Campus Power Plant / 1
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Should the Nakota plant point move about 40 kilometers to the campus parcel near Trenton shown in the developer's slides?
- finding: The letter of intent at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm says in words that the campus is 5 miles west of Williston. Its site rendering photo at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/image_062.jpg matches satellite imagery of section 1, township 153 north, range 103 west, near Trenton, about 12 miles west-southwest of downtown Williston. The database point is in farmland about 40 kilometers northeast of that parcel.
- recommendation: Move all three units to 48.10124, -103.87389 and keep the accuracy approximate until a permit or county filing names the parcel.
  - links: https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm (ok=None, contains_value=None)
  - links: https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/image_062.jpg (ok=None, contains_value=None)
  - links: https://www.google.com/maps/search/?api=1&query=48.10124,-103.87389 (ok=None, contains_value=None)
- notes: I matched the photo by three oil well pads and a road corner, with a fit error of about 2 meters. The pipeline map slide at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/image_065.jpg shades a parcel in the same section. The Williams County news site pages about a data center zoning change could not be opened because their host name does not resolve. No air permit or Public Service Commission case for this campus was found by the first look.

### G100000413123 / Pioneer generating station / 4-1
*question about existing data*
- about: Capacity (MW)
- question: Should the capacity of the phase IV turbines match the EIA figure of 245.7 MW?
- finding: The EIA table lists 245.7 MW for each of the two new turbines. GEM shows 250.0 MW. The EIA table lists 60.5 MW for each of units 1 to 3, while GEM shows 61.0 MW.
- recommendation: Leave as is, since the differences are small and the 250 MW figure came from the owner's plan. Look at the EIA figures only if a nameplate check is wanted.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: Capacity was not in this batch's report list, so no change is proposed.

### G100001094120 / Polaris Forge 1 power station / 1
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Is there a site address for a power plant at Ellendale, separate from the diesel backup site?
- finding: The Department of Environmental Quality notice at https://deq.nd.gov/AQ/Notices/ELN/DRAFTACP18296v10.pdf gives 9663 87th Avenue Southeast, Ellendale as the address of the diesel backup plant, which is its own entry in the database. Imagery of that address shows the diesel plant area and farmland and no steam plant. The database point is approximate.
- recommendation: Leave the point approximate. Do not move it to the diesel plant address.
  - links: https://deq.nd.gov/AQ/Notices/ELN/DRAFTACP18296v10.pdf (ok=None, contains_value=None)
- notes: The county is spelled Dikey County in the database and should read Dickey County. City and area fields are also blank.

### G100001090288 / River Run Energy Center / Unit 1
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Is GEM's River Run point near enough to the described site to leave unchanged?
- finding: The FAQ at https://www.nexteraenergyresources.com/river-run-energy-center/faq.html places the plant on about 150 acres next to the Leland Olds 345-kilovolt substation off Highway 200 in Mercer County. GEM's point at 47.26818, -101.31580 sits on a cleared field beside a 345 kilovolt substation and Highway 200 in satellite imagery of unknown date. The Leland Olds station itself is about 1.4 kilometers north.
- recommendation: Leave the point and the approximate accuracy as they are. Make it exact only when a permit or county filing gives the parcel.
  - links: https://www.nexteraenergyresources.com/river-run-energy-center/faq.html (ok=None, contains_value=None)
- notes: No address or parcel was found. The footprint is not built, so imagery cannot make it exact.

### G100000410559 / Xcel Fargo power plant / 1
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- question: Can the Xcel Fargo turbine site be placed any better than Fargo?
- finding: The Xcel Energy 2019 resource plan filing (https://www.psc.nd.gov/webdocs/case/19-0220/001-010.pdf) and the reply comments saved at the Wayback Machine name only Fargo. GEM's point of 46.88087, -96.82783 matches a point in the World Resources Institute power plant database, not a site document. I found no air permit, commission case or address for this project.
- recommendation: Leave the point as it is and keep the accuracy approximate. The project was cancelled before any site was named.
  - links: https://www.psc.nd.gov/webdocs/case/19-0220/001-010.pdf (ok=None, contains_value=None)
  - links: https://web.archive.org/web/20220118235603/https://www.xcelenergy.com/staticfiles/xe-responsive/Company/Rates%20&%20Regulations/Resource%20Plans/Upper%20Midwest%20Energy%20Plan%20-%20Reply%20Comments.pdf (ok=None, contains_value=None)
- notes: Searched: the harvested air permit index (nothing matched), North Dakota commission documents, the Xcel reply comments, and a web search. The Minnesota decision of February 2022 is described at https://elpc.org/news/solar-advocates-celebrate-decision-on-xcel-energy-resource-plan/ and names no site.

### G100000410559 / Xcel Fargo power plant / 1
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- question: Is MISO request J3163 in Cass County the cancelled Xcel Fargo turbine?
- finding: MISO request J3163 is an active Northern States Power hybrid of 481 MW in Cass County, queued July 2022, in service March 2028, with the connection at the Bison substation. The Fargo turbine was a 400 MW unit dropped in 2022 per https://elpc.org/news/solar-advocates-celebrate-decision-on-xcel-energy-resource-plan/. No document ties the two together.
- recommendation: Treat J3163 as a separate project and leave this unit cancelled. Add J3163 as its own plant in a discovery pass once a document gives its turbine type.
- notes: I could not verify the queue entry text: the MISO queue page at https://www.misoenergy.org/planning/resource-utilization/GI_Queue/gi-interactive-queue/ is drawn by script and does not show the request to the verifier. The entry was read from the pre-sweep harvest for this batch.

## Checklist group 3. Status and timeline

Status changes, start and retirement years, planned retirements, Latest Activity.

### G100001101353 / Applied Digital ELN Generation Plant / ELN02
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Leave Equipment Manufacturer/Model of unit ELN02 (G100001101353) as CAT: 3516E. It is still correct. Add the 2 links below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `CAT: 3516E` -> `CAT: 3516E`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf names this engine fleet as CAT: 3516E. The analysis at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf gives the same make and model.

### G100001101353 / Applied Digital ELN Generation Plant / ELN02
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 17 (Unknown technology rechecked)*
**Action:** Leave Turbine/Engine Technology of unit ELN02 (G100001101353) as internal combustion. It is still correct. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `internal combustion` -> `internal combustion`
  - Turbine/Engine Technology Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft air permit describes these units as emergency diesel generator engines. Those are reciprocating internal combustion engines. This fleet is 60 engines of about 3 MW each, about 180 MW in all, above the 50 MW threshold for backup fleets.

### G100001101353 / Applied Digital ELN Generation Plant / ELN02
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Owner(s) of unit ELN02 (G100001101353) as Applied Digital Corp [100%]. It is still correct. Add the link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Applied Digital Corp [100%]` -> `Applied Digital Corp [100%]`
  - Owners Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft air permit at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf names Applied Digital Corporation as the permittee, which the permit defines as the owner.

### G100001101356 / Applied Digital ELN Generation Plant / ELN03-CAT
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Leave Equipment Manufacturer/Model of unit ELN03-CAT (G100001101356) as CAT: 3516E. It is still correct. Add the 2 links below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `CAT: 3516E` -> `CAT: 3516E`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf names this engine fleet as CAT: 3516E. The analysis at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf gives the same make and model.

### G100001101356 / Applied Digital ELN Generation Plant / ELN03-CAT
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 17 (Unknown technology rechecked)*
**Action:** Leave Turbine/Engine Technology of unit ELN03-CAT (G100001101356) as internal combustion. It is still correct. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `internal combustion` -> `internal combustion`
  - Turbine/Engine Technology Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft air permit describes these units as emergency diesel generator engines. Those are reciprocating internal combustion engines. This fleet is 48 engines of about 3 MW each, about 144 MW in all, above the 50 MW threshold for backup fleets.

### G100001101356 / Applied Digital ELN Generation Plant / ELN03-CAT
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Owner(s) of unit ELN03-CAT (G100001101356) as Applied Digital Corp [100%]. It is still correct. Add the link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Applied Digital Corp [100%]` -> `Applied Digital Corp [100%]`
  - Owners Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft air permit at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf names Applied Digital Corporation as the permittee, which the permit defines as the owner.

### G100001101354 / Applied Digital ELN Generation Plant / ELN03-MTU
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Leave Equipment Manufacturer/Model of unit ELN03-MTU (G100001101354) as MTU: 20V4000 DS3250. It is still correct. Add the 2 links below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `MTU: 20V4000 DS3250` -> `MTU: 20V4000 DS3250`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf names this engine fleet as MTU: 20V4000 DS3250. The analysis at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf gives the same make and model.

### G100001101354 / Applied Digital ELN Generation Plant / ELN03-MTU
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 17 (Unknown technology rechecked)*
**Action:** Leave Turbine/Engine Technology of unit ELN03-MTU (G100001101354) as internal combustion. It is still correct. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `internal combustion` -> `internal combustion`
  - Turbine/Engine Technology Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft air permit describes these units as emergency diesel generator engines. Those are reciprocating internal combustion engines. This fleet is 48 engines, about 167.5 MW in all as the database already has it, above the 50 MW threshold for backup fleets.

### G100001101354 / Applied Digital ELN Generation Plant / ELN03-MTU
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Owner(s) of unit ELN03-MTU (G100001101354) as Applied Digital Corp [100%]. It is still correct. Add the link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Applied Digital Corp [100%]` -> `Applied Digital Corp [100%]`
  - Owners Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft air permit at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf names Applied Digital Corporation as the permittee, which the permit defines as the owner.

### G100001101357 / Applied Digital ELN Generation Plant / ELN04
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit ELN04 (G100001101357) to CAT: 3516E. The box is empty now. Add the 2 links below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `CAT: 3516E`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf names this engine fleet as CAT: 3516E. The analysis at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf gives the same make and model.

### G100001101357 / Applied Digital ELN Generation Plant / ELN04
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 17 (Unknown technology rechecked)*
**Action:** Leave Turbine/Engine Technology of unit ELN04 (G100001101357) as internal combustion. It is still correct. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `internal combustion` -> `internal combustion`
  - Turbine/Engine Technology Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft air permit describes these units as emergency diesel generator engines. Those are reciprocating internal combustion engines. This fleet is 96 engines of about 3 MW each, about 288 MW in all, above the 50 MW threshold for backup fleets.

### G100001101357 / Applied Digital ELN Generation Plant / ELN04
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Owner(s) of unit ELN04 (G100001101357) as Applied Digital Corp [100%]. It is still correct. Add the link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Applied Digital Corp [100%]` -> `Applied Digital Corp [100%]`
  - Owners Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft air permit at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf names Applied Digital Corporation as the permittee, which the permit defines as the owner.

### G100001101351 / Applied Digital FAR Generation Plant / FAR01
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Set Status Detail of unit FAR01 (G100001101351) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

A draft air permit to construct, number ACP-18345 version 1.0, for 192 diesel emergency generator engines at the FAR Generation Plant in Harwood was open for public comment from June 15 to July 15, 2026. Each of the two buildings holds 96 Caterpillar 3516E engines of 3,000 kilowatts.

https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf
https://deq.nd.gov/aq/Notices/AppliedDigital/20260611BaylisLtrandNOT.pdf
- `Status Detail`: `` -> `A draft air permit to construct, number ACP-18345 version 1.0, for 192 diesel emergency generator engines at the FAR Generation Plant in Harwood was open for public comment from June 15 to July 15, 2026. Each of the two buildings holds 96 Caterpillar 3516E engines of 3,000 kilowatts.

https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf
https://deq.nd.gov/aq/Notices/AppliedDigital/20260611BaylisLtrandNOT.pdf`
  - Status Detail: https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf (ok=True, contains_value=True)
  - Status Detail: https://deq.nd.gov/aq/Notices/AppliedDigital/20260611BaylisLtrandNOT.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The North Dakota Department of Environmental Quality air quality effects analysis from June 11, 2026 at https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf gives the comment dates, the engine count and the engine model. The state notice letter from June 2026 at https://deq.nd.gov/aq/Notices/AppliedDigital/20260611BaylisLtrandNOT.pdf says the department proposes to issue the permit for 192 emergency generators at the FAR Generation Plant. Both are from the same agency, so they count as one source. I found no final permit or later notice, so the status stays pre-construction. The draft permit gives building FAR01 96 Caterpillar 3516E engines of 3 MW each, which is 288 MW of diesel, the same as GEM shows. The 192 engines and 576 MW across both buildings also match GEM, and Backup Power yes fits. No start year or scheduled operating date was found. Latest Activity is left alone because the newest report is from June 2026, under a year old. No final permit was found.

### G100001101351 / Applied Digital FAR Generation Plant / FAR01
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Leave Equipment Manufacturer/Model of unit FAR01 (G100001101351) as CAT: 3516E. It is still correct. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `CAT: 3516E` -> `CAT: 3516E`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345%20v1_0.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The database already shows this model for FAR01 but gives no source for it. The draft air permit to construct ACP-18345 from the Department of Environmental Quality lists 96 Caterpillar 3516E generator engines of 3,000 kilowatts for building FAR01, and the department's air quality analysis says the same. Both are from one publisher.

### G100001101352 / Applied Digital FAR Generation Plant / FAR02
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Set Status Detail of unit FAR02 (G100001101352) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

A draft air permit to construct, number ACP-18345 version 1.0, for 192 diesel emergency generator engines at the FAR Generation Plant in Harwood was open for public comment from June 15 to July 15, 2026. Each of the two buildings holds 96 Caterpillar 3516E engines of 3,000 kilowatts.

https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf
https://deq.nd.gov/aq/Notices/AppliedDigital/20260611BaylisLtrandNOT.pdf
- `Status Detail`: `` -> `A draft air permit to construct, number ACP-18345 version 1.0, for 192 diesel emergency generator engines at the FAR Generation Plant in Harwood was open for public comment from June 15 to July 15, 2026. Each of the two buildings holds 96 Caterpillar 3516E engines of 3,000 kilowatts.

https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf
https://deq.nd.gov/aq/Notices/AppliedDigital/20260611BaylisLtrandNOT.pdf`
  - Status Detail: https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf (ok=True, contains_value=True)
  - Status Detail: https://deq.nd.gov/aq/Notices/AppliedDigital/20260611BaylisLtrandNOT.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The North Dakota Department of Environmental Quality air quality effects analysis from June 11, 2026 at https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf gives the comment dates, the engine count and the engine model. The state notice letter from June 2026 at https://deq.nd.gov/aq/Notices/AppliedDigital/20260611BaylisLtrandNOT.pdf says the department proposes to issue the permit for 192 emergency generators at the FAR Generation Plant. Both are from the same agency, so they count as one source. I found no final permit or later notice, so the status stays pre-construction. The draft permit gives building FAR02 96 Caterpillar 3516E engines of 3 MW each, which is 288 MW of diesel, the same as GEM shows. The 192 engines and 576 MW across both buildings also match GEM, and Backup Power yes fits. No start year or scheduled operating date was found. Latest Activity is left alone because the newest report is from June 2026, under a year old. No final permit was found.

### G100001101352 / Applied Digital FAR Generation Plant / FAR02
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit FAR02 (G100001101352) to CAT: 3516E. The box is empty now. Add the 2 links below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `CAT: 3516E`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345%20v1_0.pdf (ok=True, contains_value=True)
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/aq/Notices/AppliedDigital/DRAFTACP18345v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft air permit to construct ACP-18345 from the Department of Environmental Quality, and the department's air quality analysis, both list 96 Caterpillar 3516E generator engines of 3,000 kilowatts for building FAR02. Unit FAR01 already shows this model and FAR02 is blank.

### G100001101332 / Base Electron power station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Set Status Detail of unit 1 (G100001101332) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Applied Digital's quarterly report for the three months ended August 2026 says Applied Digital signed a power purchase agreement with Base Electron on October 4, 2026 for about 1,200 MW from a natural gas plant in Center, North Dakota. The agreement lets Base Electron end it if financial close has not happened by March 31, 2027. An Oliver County commission story from October 15, 2026 says the county rezoned the land to industrial and approved a conditional use permit for the plant, but held the building permit until state permits, road use and water and gas routing are settled.

https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm
https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled
- `Status Detail`: `` -> `Applied Digital's quarterly report for the three months ended August 2026 says Applied Digital signed a power purchase agreement with Base Electron on October 4, 2026 for about 1,200 MW from a natural gas plant in Center, North Dakota. The agreement lets Base Electron end it if financial close has not happened by March 31, 2027. An Oliver County commission story from October 15, 2026 says the county rezoned the land to industrial and approved a conditional use permit for the plant, but held the building permit until state permits, road use and water and gas routing are settled.

https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm
https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled`
  - Status Detail: https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm (ok=True, contains_value=True)
  - Status Detail: https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The Applied Digital quarterly report at https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm and the Citizen Portal story at https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled are two separate publishers. The unit stays in pre-construction because the building permit is not yet issued and financing has not closed. No start year is given for the plant. Applied Digital expects the data center to begin operating in August 2027, but no document gives a date for the power units. The project is moving, so Latest Activity is left alone.

### G100001101337 / Base Electron power station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Set Status Detail of unit 2 (G100001101337) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Applied Digital's quarterly report for the three months ended August 2026 says Applied Digital signed a power purchase agreement with Base Electron on October 4, 2026 for about 1,200 MW from a natural gas plant in Center, North Dakota. The agreement lets Base Electron end it if financial close has not happened by March 31, 2027. An Oliver County commission story from October 15, 2026 says the county rezoned the land to industrial and approved a conditional use permit for the plant, but held the building permit until state permits, road use and water and gas routing are settled.

https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm
https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled
- `Status Detail`: `` -> `Applied Digital's quarterly report for the three months ended August 2026 says Applied Digital signed a power purchase agreement with Base Electron on October 4, 2026 for about 1,200 MW from a natural gas plant in Center, North Dakota. The agreement lets Base Electron end it if financial close has not happened by March 31, 2027. An Oliver County commission story from October 15, 2026 says the county rezoned the land to industrial and approved a conditional use permit for the plant, but held the building permit until state permits, road use and water and gas routing are settled.

https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm
https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled`
  - Status Detail: https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm (ok=True, contains_value=True)
  - Status Detail: https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The Applied Digital quarterly report at https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm and the Citizen Portal story at https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled are two separate publishers. The unit stays in pre-construction because the building permit is not yet issued and financing has not closed. No start year is given for the plant. Applied Digital expects the data center to begin operating in August 2027, but no document gives a date for the power units. The project is moving, so Latest Activity is left alone.

### G100001101337 / Base Electron power station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit 2 (G100001101337) to Siemens Energy. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `Siemens Energy`
  - Turbine/Engine Equipment Data Source: https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Babcock and Wilcox press release from March 4, 2026 at https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses says Siemens Energy has been released to design and supply the steam turbine generator sets for the four 300 MW units. It names no separate model.

### G100001101338 / Base Electron power station / 3
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Set Status Detail of unit 3 (G100001101338) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Applied Digital's quarterly report for the three months ended August 2026 says Applied Digital signed a power purchase agreement with Base Electron on October 4, 2026 for about 1,200 MW from a natural gas plant in Center, North Dakota. The agreement lets Base Electron end it if financial close has not happened by March 31, 2027. An Oliver County commission story from October 15, 2026 says the county rezoned the land to industrial and approved a conditional use permit for the plant, but held the building permit until state permits, road use and water and gas routing are settled.

https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm
https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled
- `Status Detail`: `` -> `Applied Digital's quarterly report for the three months ended August 2026 says Applied Digital signed a power purchase agreement with Base Electron on October 4, 2026 for about 1,200 MW from a natural gas plant in Center, North Dakota. The agreement lets Base Electron end it if financial close has not happened by March 31, 2027. An Oliver County commission story from October 15, 2026 says the county rezoned the land to industrial and approved a conditional use permit for the plant, but held the building permit until state permits, road use and water and gas routing are settled.

https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm
https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled`
  - Status Detail: https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm (ok=True, contains_value=True)
  - Status Detail: https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The Applied Digital quarterly report at https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm and the Citizen Portal story at https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled are two separate publishers. The unit stays in pre-construction because the building permit is not yet issued and financing has not closed. No start year is given for the plant. Applied Digital expects the data center to begin operating in August 2027, but no document gives a date for the power units. The project is moving, so Latest Activity is left alone.

### G100001101339 / Base Electron power station / 4
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Set Status Detail of unit 4 (G100001101339) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Applied Digital's quarterly report for the three months ended August 2026 says Applied Digital signed a power purchase agreement with Base Electron on October 4, 2026 for about 1,200 MW from a natural gas plant in Center, North Dakota. The agreement lets Base Electron end it if financial close has not happened by March 31, 2027. An Oliver County commission story from October 15, 2026 says the county rezoned the land to industrial and approved a conditional use permit for the plant, but held the building permit until state permits, road use and water and gas routing are settled.

https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm
https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled
- `Status Detail`: `` -> `Applied Digital's quarterly report for the three months ended August 2026 says Applied Digital signed a power purchase agreement with Base Electron on October 4, 2026 for about 1,200 MW from a natural gas plant in Center, North Dakota. The agreement lets Base Electron end it if financial close has not happened by March 31, 2027. An Oliver County commission story from October 15, 2026 says the county rezoned the land to industrial and approved a conditional use permit for the plant, but held the building permit until state permits, road use and water and gas routing are settled.

https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm
https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled`
  - Status Detail: https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm (ok=True, contains_value=True)
  - Status Detail: https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The Applied Digital quarterly report at https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm and the Citizen Portal story at https://citizenportal.ai/articles/11129926/north-dakota/oliver-county/oliver-county-approves-zoning-and-cup-for-base-electron-power-plant-building-permit-tabled are two separate publishers. The unit stays in pre-construction because the building permit is not yet issued and financing has not closed. No start year is given for the plant. Applied Digital expects the data center to begin operating in August 2027, but no document gives a date for the power units. The project is moving, so Latest Activity is left alone.

### G100001101339 / Base Electron power station / 4
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit 4 (G100001101339) to Siemens Energy. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `Siemens Energy`
  - Turbine/Engine Equipment Data Source: https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Babcock and Wilcox press release from March 4, 2026 at https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses says Siemens Energy has been released to design and supply the steam turbine generator sets for the four 300 MW units. It names no separate model.

### G100001054598 / Bison Generation Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked)*
**Action:** Leave Status of unit 1 (G100001054598) as construction. It is still correct. Add the 3 links below to the Status Data Source box. Keep the links already there.
- `Status`: `construction` -> `construction`
  - Status Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/4882770595279333132 (ok=True, contains_value=True)
  - Status Data Source: https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility (ok=True, contains_value=True)
  - Status Data Source: https://www.minotdailynews.com/news/local-news/2026/05/basin-electric-breaks-ground-on-historic-generation-facility/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: Status stays construction. Basin Electric told the North Dakota Department of Environmental Quality in a letter dated January 21, 2026 that construction began on January 8, 2026. A Basin Electric news release from May 2026 and a Minot Daily News article from May 2026 report the groundbreaking. The EIA-860M table for September 2026 still shows regulatory approvals pending, which looks out of date because it predates these documents. Construction is confirmed under way. Nameplate is 759 MW by the EIA table and the Southwest Power Pool queue was not opened in this pass.

### G100001054598 / Bison Generation Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Set Capacity (MW) of unit 1 (G100001054598) to 759.0. It now says 745.0. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `745.0` -> `759.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists plant 69071 with a combustion turbine of 496.0 MW and a steam turbine of 263.0 MW for this block, so 759.0 MW nameplate. The air permit at https://ceris.deq.nd.gov/ext/ncore/downloadpdf/-6052959693102246591 and the Basin Electric release at https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility both say about 745 MW per unit, and the Southwest Power Pool queue shows 760 MW. The permit and release do not say whether 745 is nameplate.

### G100001054598 / Bison Generation Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units), 49 (Construction to operating checked)*
**Action:** Set Equipment Manufacturer/Model of unit 1 (G100001054598) to Mitsubishi Power M501JAC. It now says Mitsubishi Power. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `Mitsubishi Power` -> `Mitsubishi Power M501JAC`
  - Turbine/Engine Equipment Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/-6052959693102246591 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The final air permit to construct ACP-18273 version 1.0 from December 2025 lists a Mitsubishi 1x1 M501JAC natural gas combined cycle combustion turbine with a duct burner for each block.

### G100001054598 / Bison Generation Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Leave Start year of unit 1 (G100001054598) as 2029. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2029` -> `2029`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 gives a planned operation of February 2029 for this block. The human adds a new scheduled event with 2029 as Event Year and 2026 as Source Year.

### G100001054598 / Bison Generation Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked)*
**Action:** Set Status Detail of unit 1 (G100001054598) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Basin Electric reported to the state air regulator that construction began on January 8, 2026. The company held a groundbreaking in May 2026.

https://ceris.deq.nd.gov/ext/ncore/downloadpdf/4882770595279333132
https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility
- `Status Detail`: `` -> `Basin Electric reported to the state air regulator that construction began on January 8, 2026. The company held a groundbreaking in May 2026.

https://ceris.deq.nd.gov/ext/ncore/downloadpdf/4882770595279333132
https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility`
  - Status Detail: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/4882770595279333132 (ok=True, contains_value=True)
  - Status Detail: https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The letter dated January 21, 2026 gives the construction start date. The Basin Electric release from May 2026 reports the groundbreaking.

### G100001054598 / Bison Generation Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Leave Owner(s) of all 2 units of Bison Generation Station as Basin Electric Power Cooperative [100%]. It is still correct. Add the 2 links below to the Owners Data Source box on each unit. Keep the links already there.
- `Owner(s)`: `Basin Electric Power Cooperative [100%]` -> `Basin Electric Power Cooperative [100%]`
  - Owners Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/-6052959693102246591 (ok=True, contains_value=True)
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The air permit names Basin Electric Power Cooperative as the permit holder, and the EIA-860M table for September 2026 lists Basin Electric Power Coop as the owner.

### G100001054668 / Bison Generation Station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked)*
**Action:** Leave Status of unit 2 (G100001054668) as construction. It is still correct. Add the 3 links below to the Status Data Source box. Keep the links already there.
- `Status`: `construction` -> `construction`
  - Status Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/4882770595279333132 (ok=True, contains_value=True)
  - Status Data Source: https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility (ok=True, contains_value=True)
  - Status Data Source: https://www.minotdailynews.com/news/local-news/2026/05/basin-electric-breaks-ground-on-historic-generation-facility/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: Status stays construction. Basin Electric told the North Dakota Department of Environmental Quality in a letter dated January 21, 2026 that construction began on January 8, 2026. A Basin Electric news release from May 2026 and a Minot Daily News article from May 2026 report the groundbreaking. The EIA-860M table for September 2026 still shows regulatory approvals pending, which looks out of date because it predates these documents. Construction is confirmed under way. Nameplate is 759 MW by the EIA table and the Southwest Power Pool queue was not opened in this pass.

### G100001054668 / Bison Generation Station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Set Capacity (MW) of unit 2 (G100001054668) to 759.0. It now says 745.0. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `745.0` -> `759.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists plant 69071 with a combustion turbine of 496.0 MW and a steam turbine of 263.0 MW for this block, so 759.0 MW nameplate. The air permit at https://ceris.deq.nd.gov/ext/ncore/downloadpdf/-6052959693102246591 and the Basin Electric release at https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility both say about 745 MW per unit, and the Southwest Power Pool queue shows 760 MW. The permit and release do not say whether 745 is nameplate.

### G100001054668 / Bison Generation Station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units), 49 (Construction to operating checked)*
**Action:** Set Equipment Manufacturer/Model of unit 2 (G100001054668) to Mitsubishi Power M501JAC. It now says Mitsubishi Power. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `Mitsubishi Power` -> `Mitsubishi Power M501JAC`
  - Turbine/Engine Equipment Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/-6052959693102246591 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The final air permit to construct ACP-18273 version 1.0 from December 2025 lists a Mitsubishi 1x1 M501JAC natural gas combined cycle combustion turbine with a duct burner for each block.

### G100001054668 / Bison Generation Station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Leave Start year of unit 2 (G100001054668) as 2030. It is still correct. Add the 2 links below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2030` -> `2030`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Start Year Data Source: https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 gives a planned operation of March 2030 for this block. The Basin Electric release from May 2026 says the plant is expected to be fully operational in 2030. The human adds a new scheduled event with 2030 as Event Year and 2026 as Source Year.

### G100001054668 / Bison Generation Station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked)*
**Action:** Set Status Detail of unit 2 (G100001054668) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Basin Electric reported to the state air regulator that construction began on January 8, 2026. The company held a groundbreaking in May 2026.

https://ceris.deq.nd.gov/ext/ncore/downloadpdf/4882770595279333132
https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility
- `Status Detail`: `` -> `Basin Electric reported to the state air regulator that construction began on January 8, 2026. The company held a groundbreaking in May 2026.

https://ceris.deq.nd.gov/ext/ncore/downloadpdf/4882770595279333132
https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility`
  - Status Detail: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/4882770595279333132 (ok=True, contains_value=True)
  - Status Detail: https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The letter dated January 21, 2026 gives the construction start date. The Basin Electric release from May 2026 reports the groundbreaking.

### G100000403194 / Heskett Station / Unit 3
*change to an existing unit*
**Action:** Leave Start year of unit Unit 3 (G100000403194) as 2014. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2014` -> `2014`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Plant 2790, generator 3, operating month 8, operating year 2014 in the EIA-860M table for September 2026.

### G100000403835 / Heskett Station / Unit 4
*change to an existing unit*
**Action:** Leave Start year of unit Unit 4 (G100000403835) as 2024. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2024` -> `2024`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Plant 2790, generator 4, operating month 7, operating year 2024 in the EIA-860M table for September 2026.

### G100001101376 / Minnkota Power Cass power station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Status of unit 1 (G100001101376) as announced. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `announced` -> `announced`
  - Status Data Source: https://www.psc.nd.gov/webdocs/case/26-0254/001-020.pdf (ok=True, contains_value=True)
  - Status Data Source: https://cdn.prod.website-files.com/5ef212e2cdca1e094063db4e/6a32962a1710e21255119192_2025%20Integrated%20Resource%20Plan%20Public%20Website%20Final.pdf (ok=True, contains_value=True)
- confidence: medium (independent: True)
- notes: Minnkota's ten-year plan filed with the commission in July 2026 says it is evaluating a natural gas plant and would operate it in the early 2030s if it goes ahead. The 2025 integrated resource plan says the same. The North Dakota Monitor article of October 6, 2026 reports that Minnkota has bought land and plans one 400 MW turbine. None of these shows a permit application, so announced stands. The two Minnkota documents are one origin, and the news article is a second. The plant is a single planned 400 MW gas turbine. No source names the turbine maker or model, and no document states a backup power use. Latest Activity is left alone because the newest report is from October 2026.

### G100001101376 / Minnkota Power Cass power station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Start year of unit 1 (G100001101376) as 2031. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2031` -> `2031`
  - Start Year Data Source: https://www.psc.nd.gov/webdocs/case/26-0254/001-020.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The North Dakota Monitor article says the plant could start generating in 2031 or 2032. Minnkota's 2026 ten-year plan says early 2030s. The lower year, 2031, is kept. The human adds a new scheduled event with Event Year 2031 and Source Year 2026 only if none exists.

### G100001101359 / Nakota Data Center Campus Power Plant / 3
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit 3 (G100001101359) to Baker Hughes (Aero): NovaLT16. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `Baker Hughes (Aero): NovaLT16`
  - Turbine/Engine Equipment Data Source: https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The binding letter of intent filed with the Securities and Exchange Commission at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm says Baker Hughes committed NovaLT16 turbines of 16.9 megawatts each, in simple cycle. The model is spelled NovaLT16. The database spells it NovalT16 on units 1 and 2 and leaves unit 3 blank. No Public Service Commission case or Department of Environmental Quality air permit was found for Tachyon9, Nixxy or Nakota. The news is from June and July 2026, so the project is active.

### G100001090288 / River Run Energy Center / Unit 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Status of unit Unit 1 (G100001090288) as pre-construction. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `pre-construction` -> `pre-construction`
  - Status Data Source: https://www.nexteraenergyresources.com/river-run-energy-center/faq.html (ok=True, contains_value=True)
  - Status Data Source: https://www.grandforksherald.com/news/north-dakota/data-center-concerns-rise-in-2nd-western-north-dakota-county-as-nextera-basin-eye-project (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The project FAQ from NextEra Energy Resources says construction could start as early as 2027, after permits and a state Certificate of Site Compatibility. A Grand Forks Herald article from March 2026 says NextEra holds purchase options on about 530 acres of land. Land options fit pre-construction. This matches the current status, so it is not a change. No turbine make or model is public. Latest Activity is left alone because the newest report, the April 2026 open house, is under a year old. The coordinates were checked and not changed.

### G100001090288 / River Run Energy Center / Unit 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Capacity (MW) of unit Unit 1 (G100001090288) as 1450.0. It is still correct. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `1450.0` -> `1450.0`
  - Capacity Data Source: https://www.nexteraenergyresources.com/river-run-energy-center/faq.html (ok=True, contains_value=True)
  - Capacity Data Source: https://www.basinelectric.com/News-Center/news-briefs/Basin-Electric-and-NextEra-Energy-Resources-hold-an-open-house-for-proposed-River-Run-Energy-Center (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The project FAQ, a Basin Electric news brief from April 2026 and the NextEra Energy press release from December 2025 all give about 1,450 megawatts. The Southwest Power Pool queue lists two requests of 750 megawatts each, which is 1,500 megawatts. No company or state document uses 1,500 megawatts or says there are two blocks, so 1,450 stays.

### G100001090288 / River Run Energy Center / Unit 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 17 (Unknown technology rechecked)*
**Action:** Leave Turbine/Engine Technology of unit Unit 1 (G100001090288) as combined cycle. It is still correct. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `combined cycle` -> `combined cycle`
  - Turbine/Engine Technology Data Source: https://www.nexteraenergyresources.com/river-run-energy-center/faq.html (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The project FAQ calls the plant a proposed combined-cycle natural gas-fueled generation facility.

### G100001090288 / River Run Energy Center / Unit 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Start year of unit Unit 1 (G100001090288) as 2030. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2030` -> `2030`
  - Start Year Data Source: https://www.nexteraenergyresources.com/river-run-energy-center/faq.html (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The project FAQ says site preparation could start in 2027 and the plant could reach operation by 2030. The Southwest Power Pool queue entries show an in-service date of 27 September 2029. The company date is later, so 2030 stays. The human should add a scheduled event with Event Year 2030 and Source Year 2026 only if one is not already on the timeline.

### G100001090288 / River Run Energy Center / Unit 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Add the entry below at the top of the Status Detail box of unit Unit 1 (G100001090288), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

The Mercer County Commission voted 3 to 2 on 3 March 2026 for a one-year pause on data center development. The companies had not brought a project to the county as of that date.

https://www.grandforksherald.com/news/north-dakota/data-center-concerns-rise-in-2nd-western-north-dakota-county-as-nextera-basin-eye-project
- `Status Detail`: `AM 4/23/26: Early-stage siting and stakeholder engagement in April
NF 1/7/26: Jointly submitted application to the SPP ERAS2 process.` -> `The Mercer County Commission voted 3 to 2 on 3 March 2026 for a one-year pause on data center development. The companies had not brought a project to the county as of that date.

https://www.grandforksherald.com/news/north-dakota/data-center-concerns-rise-in-2nd-western-north-dakota-county-as-nextera-basin-eye-project

AM 4/23/26: Early-stage siting and stakeholder engagement in April
NF 1/7/26: Jointly submitted application to the SPP ERAS2 process.`
  - Status Detail: https://www.grandforksherald.com/news/north-dakota/data-center-concerns-rise-in-2nd-western-north-dakota-county-as-nextera-basin-eye-project (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Grand Forks Herald article from March 2026 reports the vote and that the companies had not formally brought the project to the county commission.

### G100001054598 / Bison Generation Station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
- about: Capacity (MW)
- question: Should unit capacity change from 745 MW to 759 MW?
- finding: The EIA table gives 759.0 MW nameplate per block, while the permit at https://ceris.deq.nd.gov/ext/ncore/downloadpdf/-6052959693102246591 and Basin Electric's release at https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility say about 745 MW per unit.
- recommendation: Keep 759 MW if you accept the EIA nameplate over the company's round figure. Otherwise leave 745 MW.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/-6052959693102246591 (ok=None, contains_value=None)
  - links: https://www.basinelectric.com/News-Center/news-releases/Basin-Electric-breaks-ground-on-historic-generation-facility (ok=None, contains_value=None)
- notes: The queue entries show 760 MW.

### G100001101376 / Minnkota Power Cass power station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
- about: Capacity (MW)
- question: Is the Minnkota plant 400 MW or 450 MW?
- finding: The North Dakota Monitor article at https://northdakotamonitor.com/2026/10/06/minnkota-plans-gas-fired-power-plant-in-cass-county-adding-to-energy-development/ quotes Minnkota's chief executive saying one turbine of 400 MW. The existing Status Detail says the Midcontinent queue may show 450 MW.
- recommendation: Leave capacity at 400 MW until Minnkota names a turbine or files a siting case.
  - links: https://northdakotamonitor.com/2026/10/06/minnkota-plans-gas-fired-power-plant-in-cass-county-adding-to-energy-development/ (ok=None, contains_value=None)
  - links: https://www.psc.nd.gov/webdocs/case/26-0254/001-020.pdf (ok=None, contains_value=None)
  - links: https://cdn.prod.website-files.com/5ef212e2cdca1e094063db4e/6a32962a1710e21255119192_2025%20Integrated%20Resource%20Plan%20Public%20Website%20Final.pdf (ok=None, contains_value=None)
- notes: Minnkota's ten-year plan at https://www.psc.nd.gov/webdocs/case/26-0254/001-020.pdf and its integrated resource plan at https://cdn.prod.website-files.com/5ef212e2cdca1e094063db4e/6a32962a1710e21255119192_2025%20Integrated%20Resource%20Plan%20Public%20Website%20Final.pdf give no size or site. I did not find the Midcontinent queue entry for this plant.

### G100001094120 / Polaris Forge 1 power station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 19 (Missing or unknown owner searched), 49 (Construction to operating checked)*
- about: Owner(s)
- question: Why is Minnkota Power Cooperative listed as a 50 percent owner of this unit?
- finding: The 2025 Minnkota integrated resource plan at https://cdn.prod.website-files.com/5ef212e2cdca1e094063db4e/6a32962a1710e21255119192_2025%20Integrated%20Resource%20Plan%20Public%20Website%20Final.pdf describes Minnkota as the power supplier to Applied Digital under a data center rate. It does not say Minnkota owns generation at the campus. The Babcock and Wilcox release at https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses names Base Electron as the buyer and does not name Minnkota.
- recommendation: Remove the 50 percent Babcock and Wilcox and 50 percent Minnkota ownership if the unit is kept. Find an owner document first.
  - links: https://cdn.prod.website-files.com/5ef212e2cdca1e094063db4e/6a32962a1710e21255119192_2025%20Integrated%20Resource%20Plan%20Public%20Website%20Final.pdf (ok=None, contains_value=None)
  - links: https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses (ok=None, contains_value=None)
- notes: This follows the open question on whether the unit exists at all.

### G100001094121 / Polaris Forge 2 power station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 19 (Missing or unknown owner searched), 37 (IRP box ticked on every IRP project (US only)), 49 (Construction to operating checked)*
- about: Owner(s)
- question: Why is Minnkota Power Cooperative listed as a 50 percent owner of this unit?
- finding: The Minnkota plan at https://cdn.prod.website-files.com/5ef212e2cdca1e094063db4e/6a32962a1710e21255119192_2025%20Integrated%20Resource%20Plan%20Public%20Website%20Final.pdf and the article at https://constructionreviewonline.com/applied-digital-to-break-ground-on-3b-280mw-polaris-forge-2-ai-campus-in-north-dakota/ show Minnkota supplying grid power to the campus. Neither says it owns generation there. The Babcock and Wilcox release at https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses names no site.
- recommendation: Remove the 50 percent Babcock and Wilcox and 50 percent Minnkota ownership if the unit is kept. Find an owner document first.
  - links: https://cdn.prod.website-files.com/5ef212e2cdca1e094063db4e/6a32962a1710e21255119192_2025%20Integrated%20Resource%20Plan%20Public%20Website%20Final.pdf (ok=None, contains_value=None)
  - links: https://constructionreviewonline.com/applied-digital-to-break-ground-on-3b-280mw-polaris-forge-2-ai-campus-in-north-dakota/ (ok=None, contains_value=None)
  - links: https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses (ok=None, contains_value=None)
- notes: Same concern as at Polaris Forge 1.

### G100001090288 / River Run Energy Center / Unit 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 19 (Missing or unknown owner searched)*
- about: Owner(s)
- question: What ownership shares should River Run carry when no document gives them?
- finding: GEM shows NextEra Energy Inc at 50 percent and Basin Electric Cooperative at 50 percent. The December 2025 release at https://www.investor.nexteraenergy.com/news-and-events/news-releases/2025/12-08-2025-123038666 says only that the two companies signed a memorandum of understanding to explore joint development, and gives no shares. The developer named there is the subsidiary NextEra Energy Resources.
- recommendation: Keep the entries for now and add a note that the split is not documented. Revisit when a siting or air permit filing names the owner.
  - links: https://www.investor.nexteraenergy.com/news-and-events/news-releases/2025/12-08-2025-123038666 (ok=None, contains_value=None)
  - links: https://www.nexteraenergyresources.com/river-run-energy-center/faq.html (ok=None, contains_value=None)
- notes: The FAQ at https://www.nexteraenergyresources.com/river-run-energy-center/faq.html also gives no ownership split.

## Checklist group 4. Conversions

Coal-to-gas and other conversions: unit naming, fuel and technology, replacement links.

### G100000403835 / Heskett Station / Unit 4
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 4 (G100000403835) as replacement. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `replacement` -> `replacement`
  - Conversion/replacement Data Source: https://www.psc.nd.gov/webdocs/case/19-0307/001-010.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Montana-Dakota's application to the North Dakota Public Service Commission in case PU-19-307 says Heskett 4 will be used after the retirement of the Heskett 1 and Heskett 2 coal units. So the unit replaced coal units 1 and 2.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Set Start year of unit Unit 1, timepoint 2 (G100001017988) to 2022. It now says 2014. Add the 2 links below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2014` -> `2022`
  - Start Year Data Source: https://www.psc.nd.gov/webdocs/case/22-0275/001-010.pdf (ok=True, contains_value=True)
  - Start Year Data Source: https://www.psc.nd.gov/webdocs/case/20-0333/001-010.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The 2020 ten-year plan (https://www.psc.nd.gov/webdocs/case/20-0333/001-010.pdf) says the gas conversion would be finished by the end of 2022. The July 2022 ten-year plan (https://www.psc.nd.gov/webdocs/case/22-0275/001-010.pdf) says the station has been retrofitted to allow 100 percent natural gas generation. Neither gives the month gas first ran, so 2022 is the latest year it could have started. GEM shows 2014, the year the unit began on coal. The human should add the new start year with these two links. The coal unit's retired year is 2022, so the gas start cannot be earlier.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 1, timepoint 2 (G100001017988) as conversion. It is still correct. Add the 2 links below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.psc.nd.gov/webdocs/case/20-0333/001-010.pdf (ok=True, contains_value=True)
  - Conversion/replacement Data Source: https://www.psc.nd.gov/webdocs/case/22-0275/001-010.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The 2020 ten-year plan (https://www.psc.nd.gov/webdocs/case/20-0333/001-010.pdf) says Great River Energy intends to convert Spiritwood Station from coal to natural gas. The 2022 plan (https://www.psc.nd.gov/webdocs/case/22-0275/001-010.pdf) says the retrofit is done.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*question about existing data; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
- about: Fuel
- question: Should Spiritwood Unit 1 keep coal in its fuel list?
- finding: GEM lists natural gas only. The air permit renewal application of October 2025 (https://ceris.deq.nd.gov/ext/ncore/downloadpdf/68774514989013349) lets the main boiler burn lignite, natural gas or propane, with coal limited to 10 percent of heat input in the gas scenario. The 2026 ten-year plan (https://www.psc.nd.gov/webdocs/case/26-0279/001-010.pdf) lists the fuel as natural gas and coal.
- recommendation: Leave the fuel as natural gas for now. Ask the project manager whether to add coal: lignite as a second fuel, since the permit still allows it.
  - links: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/68774514989013349 (ok=None, contains_value=None)
  - links: https://www.psc.nd.gov/webdocs/case/26-0279/001-010.pdf (ok=None, contains_value=None)
- notes: I found no document that says how much coal was burned in recent years. EIA-923 fuel data was not read in this pass.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*question about existing data; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
- about: Start year
- question: Is 2022 the right gas start year for Spiritwood Unit 1?
- finding: The July 2022 ten-year plan (https://www.psc.nd.gov/webdocs/case/22-0275/001-010.pdf) says the retrofit for 100 percent gas was done. The 2020 plan (https://www.psc.nd.gov/webdocs/case/20-0333/001-010.pdf) targeted the end of 2022, with gas as the main fuel from 2023.
- recommendation: Use 2022 as the start year for the converted unit. If the reviewer wants the first full year on gas, use 2023.
  - links: https://www.psc.nd.gov/webdocs/case/22-0275/001-010.pdf (ok=None, contains_value=None)
  - links: https://www.psc.nd.gov/webdocs/case/20-0333/001-010.pdf (ok=None, contains_value=None)
- notes: I found no document with the month gas was first burned.

## Checklist group 5. Turbine make and model

Equipment manufacturer and model, especially on units in development.

### G100000402504 / Lonesome Creek Station / 1
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit 1 (G100000402504) to GE LM6000 PF Sprint. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE LM6000 PF Sprint`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE Model LM6000 PF Sprint simple cycle natural gas turbines, each rated at 46.0 MW gross.

### G100000402505 / Lonesome Creek Station / 2
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit 2 (G100000402505) to GE LM6000 PF Sprint. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE LM6000 PF Sprint`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE Model LM6000 PF Sprint simple cycle natural gas turbines, each rated at 46.0 MW gross.

### G100000402506 / Lonesome Creek Station / 3
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit 3 (G100000402506) to GE LM6000 PF Sprint. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE LM6000 PF Sprint`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE Model LM6000 PF Sprint simple cycle natural gas turbines, each rated at 46.0 MW gross.

### G100000402507 / Lonesome Creek Station / 4
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit 4 (G100000402507) to GE LM6000 PF Sprint. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE LM6000 PF Sprint`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE Model LM6000 PF Sprint simple cycle natural gas turbines, each rated at 46.0 MW gross.

### G100000402508 / Lonesome Creek Station / 5
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit 5 (G100000402508) to GE LM6000 PF Sprint. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE LM6000 PF Sprint`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE Model LM6000 PF Sprint simple cycle natural gas turbines, each rated at 46.0 MW gross.

### G100000409510 / Lonesome Creek Station / 6
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit 6 (G100000409510) to GE LM6000 PF Sprint. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `GE LM6000 PF Sprint`
  - Turbine/Engine Equipment Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The draft Title V permit renewal from June 2026 at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf says the station has six GE Model LM6000 PF Sprint simple cycle natural gas turbines, each rated at 46.0 MW gross.

### G100000413123 / Pioneer generating station / 4-1
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit 4-1 (G100000413123) to Siemens Energy: SGT6-5000F. It now says Siemens Energy: STG6-5000F. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `Siemens Energy: STG6-5000F` -> `Siemens Energy: SGT6-5000F`
  - Turbine/Engine Equipment Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/2211455608767769004 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The December 2022 air permit to construct application for phase IV names the turbine make as Siemens and the model as SGT6-5000F, for two simple cycle combustion turbines. GEM shows the model as STG6-5000F, which looks like a typing slip. The correct model name is SGT6-5000F.

### G100000413122 / Pioneer generating station / 4-2
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit 4-2 (G100000413122) to Wärtsilä: 18V50SG. It now says Wärtsilä: W18V50SG. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `Wärtsilä: W18V50SG` -> `Wärtsilä: 18V50SG`
  - Turbine/Engine Equipment Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/2211455608767769004 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The December 2022 air permit to construct application for phase IV names the engine make as Wartsila and the model as 18V50SG, at 18.8 MW each.

### G100000413121 / Pioneer generating station / 4-3
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit 4-3 (G100000413121) to Siemens Energy: SGT6-5000F. It now says Siemens Energy: STG6-5000F. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `Siemens Energy: STG6-5000F` -> `Siemens Energy: SGT6-5000F`
  - Turbine/Engine Equipment Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/2211455608767769004 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The December 2022 air permit to construct application for phase IV names the turbine make as Siemens and the model as SGT6-5000F, for two simple cycle combustion turbines. GEM shows the model as STG6-5000F, which looks like a typing slip. The correct model name is SGT6-5000F.

### G100000413124 / Pioneer generating station / IC
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit IC (G100000413124) to Wärtsilä: 20V34SG. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `Wärtsilä: 20V34SG`
  - Turbine/Engine Equipment Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/8220580009086318601 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Title V air permit, number AOP-28359 version 2.0 issued March 2022, lists twelve Wartsila Model 20V34SG natural gas engines, each driving a generator. The permit text was read from a scanned copy.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*change to an existing unit*
**Action:** Set Equipment Manufacturer/Model of unit Unit 1, timepoint 2 (G100001017988) to Siemens SST-800. The box is empty now. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `` -> `Siemens SST-800`
  - Turbine/Engine Equipment Data Source: https://www.psc.nd.gov/webdocs/case/26-0279/001-010.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Great River Energy 2026 ten-year plan (https://www.psc.nd.gov/webdocs/case/26-0279/001-010.pdf) lists Spiritwood Station as heat and power, one unit, Siemens SST 800, fuel natural gas and coal, 99 MW. The boiler is a Babcock and Wilcox unit per the air permit renewal application of October 2025 (https://ceris.deq.nd.gov/ext/ncore/downloadpdf/68774514989013349). I report the turbine maker and model.

## Checklist group 6. Owners and entities

Owner, operator and parent changes, and new owners or operators to create.

### G100000403194 / Heskett Station / Unit 3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 3 (G100000403194) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Plant 2790, generator 3, status OP, nameplate 88.0 MW, operating 2014 in the EIA-860M table for September 2026 (released 23 October 2026). No retirement date is planned. The unit is still operating with no retirement planned. The Montana-Dakota Utilities owner value is carried in the plant findings.

### G100000403835 / Heskett Station / Unit 4
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 4 (G100000403835) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Plant 2790, generator 4, status OP, nameplate 88.4 MW, operating July 2024 in the EIA-860M table for September 2026. No retirement date is planned. EIA lists 88.4 MW against GEM's 88.0 MW. The difference is within rounding, so capacity stays as it is.

### G100000402504 / Lonesome Creek Station / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100000402504) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists this unit as operating. Matching row: Plant 57943, generator 01, status operating, nameplate 60.5 MW, no planned retirement, began operating November 2013. It shows no planned retirement, mothballing or owner change. The unit is operating in the EIA table for September 2026. No retirement, mothballing or owner change was found. Latest Activity is left alone because the unit is operating.

### G100000402504 / Lonesome Creek Station / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of all 6 units of Lonesome Creek Station as Basin Electric Power Cooperative [100%]. It is still correct. Add the link below to the Owners Data Source box on each unit. Keep the links already there.
- `Owner(s)`: `Basin Electric Power Cooperative [100%]` -> `Basin Electric Power Cooperative [100%]`
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists Basin Electric Power Coop as the owning entity for all six units. This matches GEM and is not a new source for the share.

### G100000402505 / Lonesome Creek Station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000402505) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists this unit as operating. Matching row: Plant 57943, generator 02, status operating, nameplate 60.5 MW, no planned retirement, began operating January 2015. It shows no planned retirement, mothballing or owner change. The unit is operating in the EIA table for September 2026. No retirement, mothballing or owner change was found. Latest Activity is left alone because the unit is operating.

### G100000402506 / Lonesome Creek Station / 3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 3 (G100000402506) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists this unit as operating. Matching row: Plant 57943, generator 03, status operating, nameplate 60.5 MW, no planned retirement, began operating January 2015. It shows no planned retirement, mothballing or owner change. The unit is operating in the EIA table for September 2026. No retirement, mothballing or owner change was found. Latest Activity is left alone because the unit is operating.

### G100000402507 / Lonesome Creek Station / 4
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4 (G100000402507) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists this unit as operating. Matching row: Plant 57943, generator 04, status operating, nameplate 60.5 MW, no planned retirement, began operating May 2017. It shows no planned retirement, mothballing or owner change. The unit is operating in the EIA table for September 2026. No retirement, mothballing or owner change was found. Latest Activity is left alone because the unit is operating.

### G100000402508 / Lonesome Creek Station / 5
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 5 (G100000402508) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists this unit as operating. Matching row: Plant 57943, generator 05, status operating, nameplate 60.5 MW, no planned retirement, began operating May 2017. It shows no planned retirement, mothballing or owner change. The unit is operating in the EIA table for September 2026. No retirement, mothballing or owner change was found. Latest Activity is left alone because the unit is operating.

### G100000409510 / Lonesome Creek Station / 6
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 6 (G100000409510) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists this unit as operating. Matching row: Plant 57943, generator 06, status operating, nameplate 60.5 MW, no planned retirement, began operating October 2021. It shows no planned retirement, mothballing or owner change. The unit is operating in the EIA table for September 2026. No retirement, mothballing or owner change was found. Latest Activity is left alone because the unit is operating.

### G100000402510 / Pioneer generating station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000402510) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026, released October 23, 2026, lists plant 57881, generator 02, nameplate 60.5 MW, operating since January 2014, status operating. The EIA table lists this unit as operating with no planned retirement. No retirement, mothballing or owner change was found.

### G100000402511 / Pioneer generating station / 3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 3 (G100000402511) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026, released October 23, 2026, lists plant 57881, generator 03, nameplate 60.5 MW, operating since February 2014, status operating. The EIA table lists this unit as operating with no planned retirement. A North Dakota air quality letter from March 2025 mentions a replacement turbine for unit 3. I did not read it in full, so no change is reported.

### G100000413123 / Pioneer generating station / 4-1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4-1 (G100000413123) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026, released October 23, 2026, lists plant 57881, generator 05 or 04, nameplate 245.7 MW, operating since 2025, status operating. The EIA table lists the two new turbines, generators 04 and 05, as operating, starting August 2025 and June 2025. So the start year of 2025 holds. No commission case or queue entry was needed to settle this.

### G100000413122 / Pioneer generating station / 4-2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4-2 (G100000413122) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026, released October 23, 2026, lists plant 57881, generators 31 to 36, six engines of 18.8 MW each, operating since April 2025, status operating. The six engines are operating in the EIA table, starting April 2025, so the start year of 2025 holds.

### G100000413121 / Pioneer generating station / 4-3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4-3 (G100000413121) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026, released October 23, 2026, lists plant 57881, generator 04 or 05, nameplate 245.7 MW, operating since 2025, status operating. The EIA table lists generators 04 and 05 as operating, starting August 2025 and June 2025. So the start year of 2025 holds. The table does not say which of the two is GEM unit 4-1 and which is 4-3.

### G100000413124 / Pioneer generating station / IC
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit IC (G100000413124) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026, released October 23, 2026, lists plant 57881, generators 11 to 22, twelve engines of 9.3 MW each, operating since January 2017, status operating. The twelve engines are operating in the EIA table, with no planned retirement.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 1, timepoint 2 (G100001017988) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 56786, Spiritwood Station, generator 1, as operating. Nameplate is 106.2 MW and there is no planned retirement date. The Great River Energy 2026 North Dakota ten-year plan (https://www.psc.nd.gov/webdocs/case/26-0279/001-010.pdf) still lists the station as a working heat and power plant. I found no retirement, mothballing or owner change. The unit is still operating per EIA. The start year probably should move from 2014 to 2022, the year the gas retrofit was finished. No retirement or planned retirement date was found.

### Bison Generation Station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Basin Electric Power Cooperative (owner); lookup: Already the owner in GEM; no new entity needed.

### Spiritwood Industrial Park
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Great River Energy Cooperative (owner); lookup: Entity appears on 15 units in the United States. Reuse the existing entity.

## Checklist group 7. IDs, IRPs and data centers

United States only: EIA and other IDs, utility resource plans, data center power (gas or diesel, routine or backup; a backup engine fleet counts and is added at the summed nameplate threshold).

### G100001101353 / Applied Digital ELN Generation Plant / ELN02
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Number Of Engines of unit ELN02 (G100001101353) as 60. It is still correct. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `60` -> `60`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit ACP-18338 at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf and its air quality effects analysis at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf list 60 diesel generator engines for ELN02. The draft permit lists 60 Caterpillar 3516E engines in building ELN02, matching the database. No start year or operating date is stated. The project is moving, so Latest Activity is left alone.

### G100001101353 / Applied Digital ELN Generation Plant / ELN02
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Capacity Per Engine of unit ELN02 (G100001101353) as 3.0. It is still correct. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `3.0` -> `3.0`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf says each Caterpillar 3516E engine produces 3,000 kilowatts, which is 3.0 megawatts.

### G100001101356 / Applied Digital ELN Generation Plant / ELN03-CAT
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Number Of Engines of unit ELN03-CAT (G100001101356) as 48. It is still correct. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `48` -> `48`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit ACP-18338 at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf and its air quality effects analysis at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf list 48 diesel generator engines for ELN03-CAT. The draft permit lists 48 Caterpillar 3516E engines in building ELN03, matching the database. No start year was found. The project is moving, so Latest Activity is left alone.

### G100001101356 / Applied Digital ELN Generation Plant / ELN03-CAT
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Capacity Per Engine of unit ELN03-CAT (G100001101356) as 3.0. It is still correct. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `3.0` -> `3.0`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf says each Caterpillar 3516E engine produces 3,000 kilowatts, which is 3.0 megawatts.

### G100001101354 / Applied Digital ELN Generation Plant / ELN03-MTU
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Number Of Engines of unit ELN03-MTU (G100001101354) as 48. It is still correct. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `48` -> `48`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit ACP-18338 at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf and its air quality effects analysis at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf list 48 diesel generator engines for ELN03-MTU. The draft permit lists 48 MTU 20V4000 DS3250 engines in building ELN03. The permit table says 3,490 kilowatts each but its analysis document says 3,250 kilowatts each, so capacity per engine is left to a reviewer question. No start year was found.

### G100001101357 / Applied Digital ELN Generation Plant / ELN04
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Number Of Engines of unit ELN04 (G100001101357) as 96. It is still correct. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Number Of Engines`: `96` -> `96`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit ACP-18338 at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf and its air quality effects analysis at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf list 96 diesel generator engines for ELN04. The draft permit lists 96 Caterpillar 3516E engines in building ELN04. The database has no engine make for this unit, so CAT: 3516E fills the blank. No start year was found.

### G100001101357 / Applied Digital ELN Generation Plant / ELN04
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Capacity Per Engine of unit ELN04 (G100001101357) as 3.0. It is still correct. Add the 2 links below to the Capacity Data Source box. Keep the links already there.
- `Capacity Per Engine`: `3.0` -> `3.0`
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=True, contains_value=True)
  - Capacity Data Source: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The draft air permit at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf says each Caterpillar 3516E engine produces 3,000 kilowatts, which is 3.0 megawatts.

### G100001101332 / Base Electron power station / 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 1 (G100001101332) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Applied Digital quarterly report at https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm describes the plant as dedicated generation for the Polaris Forge 3 campus under a 15 year power purchase agreement. It does not call any unit backup power, so the current value of no fits. The report never uses the words backup power for this plant.

### G100001101337 / Base Electron power station / 2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 2 (G100001101337) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Applied Digital quarterly report at https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm describes the plant as dedicated generation for the Polaris Forge 3 campus under a 15 year power purchase agreement. It does not call any unit backup power, so the current value of no fits. The report never uses the words backup power for this plant.

### G100001101338 / Base Electron power station / 3
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 3 (G100001101338) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Applied Digital quarterly report at https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm describes the plant as dedicated generation for the Polaris Forge 3 campus under a 15 year power purchase agreement. It does not call any unit backup power, so the current value of no fits. The report never uses the words backup power for this plant.

### G100001101339 / Base Electron power station / 4
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 4 (G100001101339) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Applied Digital quarterly report at https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000059/apld-20260831.htm describes the plant as dedicated generation for the Polaris Forge 3 campus under a 15 year power purchase agreement. It does not call any unit backup power, so the current value of no fits. The report never uses the words backup power for this plant.

### G100001054598 / Bison Generation Station / 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 1 (G100001054598) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/-40749731620493823 (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The air permit support document lists one standby diesel generator and one diesel fire pump engine for the whole plant. Both are small support engines, not power units. The document does not say the combined cycle blocks serve as backup power, so this unit stays no.

### G100001054668 / Bison Generation Station / 2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 2 (G100001054668) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/-40749731620493823 (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The air permit support document lists one standby diesel generator and one diesel fire pump engine for the whole plant. Both are small support engines, not power units. The document does not say the combined cycle blocks serve as backup power, so this unit stays no.

### G100000403194 / Heskett Station / Unit 3
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit Unit 3 (G100000403194) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 lists generator 3 as operating, not as standby or backup. The only standby generator at the plant is a 2 MW engine named EMER.

### G100000403835 / Heskett Station / Unit 4
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit Unit 4 (G100000403835) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The EIA-860M table for September 2026 lists generator 4 as operating, not as standby or backup.

### G100000402504 / Lonesome Creek Station / 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 1 (G100000402504) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf calls the station a natural gas-fired electric generating peaking plant. It sells to the grid and no document describes it as backup power. So the value stays no.

### G100000402505 / Lonesome Creek Station / 2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 2 (G100000402505) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf calls the station a natural gas-fired electric generating peaking plant. It sells to the grid and no document describes it as backup power. So the value stays no.

### G100000402506 / Lonesome Creek Station / 3
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 3 (G100000402506) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf calls the station a natural gas-fired electric generating peaking plant. It sells to the grid and no document describes it as backup power. So the value stays no.

### G100000402507 / Lonesome Creek Station / 4
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 4 (G100000402507) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf calls the station a natural gas-fired electric generating peaking plant. It sells to the grid and no document describes it as backup power. So the value stays no.

### G100000402508 / Lonesome Creek Station / 5
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 5 (G100000402508) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf calls the station a natural gas-fired electric generating peaking plant. It sells to the grid and no document describes it as backup power. So the value stays no.

### G100000409510 / Lonesome Creek Station / 6
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 6 (G100000409510) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The draft permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf calls the station a natural gas-fired electric generating peaking plant. It sells to the grid and no document describes it as backup power. So the value stays no.

### G100001096407 / Nakota Data Center Campus Power Plant / 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 1 (G100001096407) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://hiranandaniltd.com/updates/hiranandani-backed-nidar-infrastructure-signs-binding-mou-and-offtake-agreement-with-tachyon9-nixxy-to-anchor-nakota-ai-data-campus-in-north-dakota/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The announcement at https://hiranandaniltd.com/updates/hiranandani-backed-nidar-infrastructure-signs-binding-mou-and-offtake-agreement-with-tachyon9-nixxy-to-anchor-nakota-ai-data-campus-in-north-dakota/ describes dedicated behind-the-meter power generation fueled by natural gas for the data campus. That is the routine power supply for the campus, so Backup Power stays no. No Public Service Commission case or Department of Environmental Quality air permit was found for Tachyon9, Nixxy or Nakota. The news is from June and July 2026, so the project is active.

### G100001096410 / Nakota Data Center Campus Power Plant / 2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 2 (G100001096410) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://hiranandaniltd.com/updates/hiranandani-backed-nidar-infrastructure-signs-binding-mou-and-offtake-agreement-with-tachyon9-nixxy-to-anchor-nakota-ai-data-campus-in-north-dakota/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The announcement at https://hiranandaniltd.com/updates/hiranandani-backed-nidar-infrastructure-signs-binding-mou-and-offtake-agreement-with-tachyon9-nixxy-to-anchor-nakota-ai-data-campus-in-north-dakota/ describes dedicated behind-the-meter power generation fueled by natural gas for the data campus. That is the routine power supply for the campus, so Backup Power stays no. No Public Service Commission case or Department of Environmental Quality air permit was found for Tachyon9, Nixxy or Nakota. The news is from June and July 2026, so the project is active.

### G100001101359 / Nakota Data Center Campus Power Plant / 3
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 3 (G100001101359) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://hiranandaniltd.com/updates/hiranandani-backed-nidar-infrastructure-signs-binding-mou-and-offtake-agreement-with-tachyon9-nixxy-to-anchor-nakota-ai-data-campus-in-north-dakota/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The announcement at https://hiranandaniltd.com/updates/hiranandani-backed-nidar-infrastructure-signs-binding-mou-and-offtake-agreement-with-tachyon9-nixxy-to-anchor-nakota-ai-data-campus-in-north-dakota/ describes dedicated behind-the-meter power generation fueled by natural gas for the data campus. That is the routine power supply for the campus, so Backup Power stays no.

### G100000402509 / Pioneer generating station / 1
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100000402509) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026, released October 23, 2026, lists plant 57881, generator 01, nameplate 60.5 MW, operating since September 2013, status operating. The EIA table still lists this unit as operating, with no planned retirement. The Energy Information Administration table is the only place I checked for retirement news, and none was found. The Oil and Gas Watch entry that calls Pioneer unit 1 under construction appears to mean the new phase IV units, because the EIA table shows all seven generator sets operating.

### G100000402509 / Pioneer generating station / 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 1 (G100000402509) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/8220580009086318601 (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The Title V air permit for the plant, number AOP-28359 version 2.0 issued March 2022, lists three simple cycle combustion turbines described as peaking units that sell power to the grid. It does not describe them as emergency or backup power. So backup power stays no. The permit does not state this in those words, so this rests on the description.

### G100000402510 / Pioneer generating station / 2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 2 (G100000402510) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/8220580009086318601 (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The Title V air permit for the plant, number AOP-28359 version 2.0 issued March 2022, lists three simple cycle combustion turbines described as peaking units that sell power to the grid. It does not describe them as emergency or backup power. So backup power stays no. The permit does not state this in those words, so this rests on the description.

### G100000402511 / Pioneer generating station / 3
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 3 (G100000402511) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/8220580009086318601 (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The Title V air permit for the plant, number AOP-28359 version 2.0 issued March 2022, lists three simple cycle combustion turbines described as peaking units that sell power to the grid. It does not describe them as emergency or backup power. So backup power stays no. The permit does not state this in those words, so this rests on the description.

### G100000413123 / Pioneer generating station / 4-1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 4-1 (G100000413123) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/2211455608767769004 (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The December 2022 air permit to construct application for phase IV lists the new turbines for grid supply with 3,500 operating hours a year each. It does not describe any of them as emergency or backup power. So backup power stays no. The application does not say this in those words.

### G100000413122 / Pioneer generating station / 4-2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 4-2 (G100000413122) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/2211455608767769004 (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The air permit to construct application says the engines are allowed to run without any limit on use. It does not describe them as emergency or backup power. So backup power stays no.

### G100000413121 / Pioneer generating station / 4-3
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 4-3 (G100000413121) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/2211455608767769004 (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The December 2022 air permit to construct application for phase IV lists the new turbines for grid supply with 3,500 operating hours a year each. It does not describe any of them as emergency or backup power. So backup power stays no. The application does not say this in those words.

### G100000413124 / Pioneer generating station / IC
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit IC (G100000413124) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://ceris.deq.nd.gov/ext/ncore/downloadpdf/-4335381491789088075 (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: A North Dakota air quality department review from February 2025 calls each Wartsila engine a non-emergency spark ignition natural gas engine and says the twelve engines make up 111 MW of the plant. So these are not emergency engines and backup power stays no.

### G100001090288 / River Run Energy Center / Unit 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit Unit 1 (G100001090288) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.nexteraenergyresources.com/river-run-energy-center/faq.html (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The project FAQ describes the plant as generation to meet data center demand and mentions no backup engine fleet. So the plant supplies routine power, not backup power.

### G100001090288 / River Run Energy Center / Unit 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Captive industry use of unit Unit 1 (G100001090288) as power. It is still correct. Add the 2 links below to the Captive Data Source box. Keep the links already there.
- `Captive industry use`: `power` -> `power`
  - Captive Data Source: https://www.nexteraenergyresources.com/river-run-energy-center/faq.html (ok=True, contains_value=True)
  - Captive Data Source: https://dakotagas.com/News-Center/news-releases/Basin-Electric-Power-Cooperative-and-NextEra-Energy-Resources-announce-collaboration-to-bring-responsible-growth-jobs-and-economic-benefits-to-North-Dakota-through-development-of-the-River-Run-Energy-Center (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The FAQ and the December 2025 release say the plant is meant to meet demand from data centers, and that data centers would fund their own generation.

### G100001090288 / River Run Energy Center / Unit 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Captive industry type of unit Unit 1 (G100001090288) as data center. It is still correct. Add the 2 links below to the Captive Data Source box. Keep the links already there.
- `Captive industry type`: `data center` -> `data center`
  - Captive Data Source: https://www.nexteraenergyresources.com/river-run-energy-center/faq.html (ok=True, contains_value=True)
  - Captive Data Source: https://dakotagas.com/News-Center/news-releases/Basin-Electric-Power-Cooperative-and-NextEra-Energy-Resources-announce-collaboration-to-bring-responsible-growth-jobs-and-economic-benefits-to-North-Dakota-through-development-of-the-River-Run-Energy-Center (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The FAQ says NextEra is securing land options of up to about 1,500 acres for a data center campus beside the plant.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit Unit 1, timepoint 2 (G100001017988) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://www.psc.nd.gov/webdocs/case/20-0333/001-010.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The 2020 ten-year plan (https://www.psc.nd.gov/webdocs/case/20-0333/001-010.pdf) says Spiritwood Station will remain a full-time generating facility. That means it is not a backup unit. The document does not use the words backup power.

### G100000410559 / Xcel Fargo power plant / 1
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Leave Backup Power of unit 1 (G100000410559) as no. It is still correct. Add the link below to the Backup Power Data Source box. Keep the links already there.
- `Backup Power`: `no` -> `no`
  - Backup Power Data Source: https://web.archive.org/web/20220118235603/https://www.xcelenergy.com/staticfiles/xe-responsive/Company/Rates%20&%20Regulations/Resource%20Plans/Upper%20Midwest%20Energy%20Plan%20-%20Reply%20Comments.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: A saved copy of Xcel Energy's Upper Midwest Energy Plan reply comments (https://web.archive.org/web/20220118235603/https://www.xcelenergy.com/staticfiles/xe-responsive/Company/Rates%20&%20Regulations/Resource%20Plans/Upper%20Midwest%20Energy%20Plan%20-%20Reply%20Comments.pdf) describes a 400 MW combustion turbine in Fargo as a system reliability unit, not a data center backup unit. It does not use the words backup power. This is a saved copy because the live page is gone. The unit stays cancelled. No document names a turbine maker or model, because the project never reached a permit.

### G100001101354 / Applied Digital ELN Generation Plant / ELN03-MTU
*question about existing data; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
- about: Capacity Per Engine
- question: Is each MTU engine at ELN03 rated 3,490 kilowatts or 3,250 kilowatts?
- finding: The permit table at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf says the 48 MTU 20V4000 DS3250 engines produce 3,490 kilowatts each. The analysis at https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf says 3,250 kilowatts each. The database uses 3.49 megawatts per engine and 167.52 megawatts in total.
- recommendation: Keep 3.49 for now. Ask the North Dakota air quality office which figure the final permit uses, and change to 3.25 and 156.0 megawatts if it says 3,250.
  - links: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0.pdf (ok=None, contains_value=None)
  - links: https://deq.nd.gov/AQ/Notices/AppliedDigital/DRAFT_ACP18338v1_0AQEA.pdf (ok=None, contains_value=None)
  - links: https://www.psc.nd.gov/webdocs/case/26-0155/001-010.pdf (ok=None, contains_value=None)
- notes: The commission filing at https://www.psc.nd.gov/webdocs/case/26-0155/001-010.pdf says the site plans about 252 engines of 3 megawatts each, up to 756 megawatts. That rounds the MTU engines down and does not settle the question.

### Bison Generation Station
*question about existing data; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
- about: Other IDs (location)
- question: Should the EIP row named Brickhouse Power Plant be matched to Basin's Bison Generation Station?
- finding: The Environmental Integrity Project sheet has a North Dakota row named Brickhouse Power Plant, a proposed 1,400 MW combined cycle plant for 2030. It points at GEM ID L100001025913, which is not in the current GEM export.
- recommendation: Put L100001047848 and Bison's unit IDs in the GEM ID columns of that EIP sheet row, since it describes Basin's Bison plant.
- notes: Todd Brickhouse is Basin Electric's chief executive, and the row's research note cites a North Dakota Monitor story of May 15, 2024 about Basin's planned gas plant. The size, technology and year match Bison Generation Station, which GEM lists with two 745 MW combined cycle units. The old GEM ID seems to belong to a record that was merged or removed. This is a sheet fix only and needs no change in the database.

### Coyote Station replacement turbines in Montana-Dakota's 2024 plan
*watch item, new to the tracker; checklist rows 34 (US IRPs tab updated for the state (US only)), 37 (IRP box ticked on every IRP project (US only)), 51 (Newly announced projects checked)*
- what to watch: Montana-Dakota's 2024 North Dakota resource plan models gas turbines to replace Coyote Station only as a sensitivity case.
- check again by: 2027-01
  - links: https://www.montana-dakota.com/wp-content/uploads/PDFs/Rates-Tariffs/2024-ND-IRP-Volume-4-non-print.pdf (ok=True, contains_value=True)
  - links: https://puc.sd.gov/commission/commissionaction/10yearplan/mdu2026.pdf (ok=True, contains_value=True)
- notes: Volume IV of Montana-Dakota's 2024 North Dakota resource plan, filed July 12, 2024, tests a case where Coyote Station retires at the end of 2031. In that case it models two large gas turbines of about 429 MW and 393 MW in total, with Montana-Dakota taking a 25 percent share as it does at Coyote. No site, owner group or schedule is described. Montana-Dakota's ten year plan filed in South Dakota in July 2026 lists no new gas plant.

### G100001096407 / Nakota Data Center Campus Power Plant / 1
*question about existing data; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
- about: Number Of Engines
- question: Should each unit show 20 turbines of 16.9 megawatts, or 22 including spares?
- finding: The letter of intent at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm counts 22 NovaLT16 turbines per 300 megawatt phase, 20 operating and 2 spare, each 16.9 megawatts. The database uses 20 per unit, 338 megawatts, and 1,014 megawatts in all. The announced target is up to 1 gigawatt.
- recommendation: Keep 20 turbines and 338 megawatts per unit. The spares are not counted in capacity.
  - links: https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm (ok=None, contains_value=None)
- notes: The database technology is gas turbine, which matches the letter. The brief called the fleet engines, but these are turbines. No air permit exists yet to confirm the count.

### Otter Tail Power 50 MW gas plant in the 2027 to 2041 plan
*watch item, new to the tracker; checklist rows 34 (US IRPs tab updated for the state (US only)), 37 (IRP box ticked on every IRP project (US only)), 51 (Newly announced projects checked)*
- what to watch: Otter Tail's Minnesota resource plan proposes a 50 MW gas plant for 2031 or 2032 with no site named, so it may not be in North Dakota.
- check again by: 2027-07
  - links: https://www.otpco.com/about-us/energy-generation/resource-plan/ (ok=True, contains_value=True)
- notes: Otter Tail Power's resource plan page says it filed its 2027 to 2041 plan with the Minnesota Public Utilities Commission on May 15, 2026, in docket E017/RP-26-90. The plan proposes a 50 MW natural gas plant in service in 2031 or 2032. No site is named. The page says Otter Tail files its next North Dakota plan in 2027. The Minnesota batch should check the docket for the site and add it in whichever state it sits.

### G100000402509 / Pioneer generating station / 1
*question about existing data; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
- about: Status
- question: Is the Oil and Gas Watch under construction label for Pioneer unit 1 out of date?
- finding: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists all seven generator groups at the plant as operating, including the phase IV turbines and engines from 2025.
- recommendation: Leave the status as operating for every unit. Tell the Oil and Gas Watch team that their record looks out of date.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: I did not open the Oil and Gas Watch page, since it is a lead site and not a citable source.

### G100001094121 / Polaris Forge 2 power station / 1
*question about existing data; checklist rows 37 (IRP box ticked on every IRP project (US only)), 51 (Newly announced projects checked)*
- about: existence
- question: Does Polaris Forge 2 have its own 280 megawatt gas steam plant, or is 280 megawatts the data center load?
- finding: The 2025 Minnkota integrated resource plan at https://cdn.prod.website-files.com/5ef212e2cdca1e094063db4e/6a32962a1710e21255119192_2025%20Integrated%20Resource%20Plan%20Public%20Website%20Final.pdf calls Polaris Forge 2 a 280 megawatt AI data center campus near Harwood and says Minnkota serves it under a data center rate. It lists no generation at the campus. The Construction Review article at https://constructionreviewonline.com/applied-digital-to-break-ground-on-3b-280mw-polaris-forge-2-ai-campus-in-north-dakota/ also describes a 280 megawatt campus powered by Minnkota and Cass County Electric Cooperative.
- recommendation: Treat the 280 megawatts as data center load and do not keep this unit as a generating plant unless a document shows a power plant at Harwood.
  - links: https://cdn.prod.website-files.com/5ef212e2cdca1e094063db4e/6a32962a1710e21255119192_2025%20Integrated%20Resource%20Plan%20Public%20Website%20Final.pdf (ok=None, contains_value=None)
  - links: https://constructionreviewonline.com/applied-digital-to-break-ground-on-3b-280mw-polaris-forge-2-ai-campus-in-north-dakota/ (ok=None, contains_value=None)
- notes: The Minnkota plan says system upgrades and power supply resources for this load will be paid for by Applied Digital, so a future dedicated plant is possible but none is named. This is a plan source.

## Checklist group 8. New to the tracker

New plants and units ready to add, candidates to watch, and the possible-updates rows.

### Coal Creek gas plant
*new plant; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
**Action:** Create Coal Creek gas plant near Underwood, McLean County, North Dakota, owned by Rainbow Energy Center LLC with parent United Energy Corp, then add the one unit below. Leave the start year and technology blank.
- `State/Province`: `` -> `North Dakota`
- `Local area (taluk, county)`: `` -> `McLean`
- `City`: `` -> `Underwood`
- `Latitude`: `` -> `47.3785`
- `Longitude`: `` -> `-101.1570`
- `Location accuracy`: `` -> `approximate`
- `Owner(s)`: `` -> `Rainbow Energy Center LLC [100%]`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Capacity (MW)`: `2000`
- unit 1 `Status`: `announced`
- location now: none in GEM
- location proposed: 47.3785, -101.1570 (approximate) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=47.37850,-101.15700&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=47.37850,-101.15700)
  - Location Data Source: https://ndlegis.gov/sites/default/files/pdf/committees/69-2025/27.5070.02000presentation0910.pdf (ok=True, contains_value=True)
  - Location Data Source: https://www.google.com/maps?q=47.3785110,-101.1570330 (ok=True, contains_value=True)
  - Owners Data Source: https://ndlegis.gov/sites/default/files/pdf/committees/69-2025/27.5070.02000presentation0910.pdf (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: GEM does not list a gas plant at Coal Creek. Rainbow Energy Center owns the Coal Creek coal plant near Underwood in McLean County. Its presentation to a North Dakota legislative committee on September 10, 2025 lists 2+ GW of new natural gas generation at Coal Creek as a growth plan. The same slide set says Rainbow is in exclusive talks with a data center developer on a 2.1 GW power purchase agreement and has 800 acres zoned. A Minot Daily News story of April 15, 2026 says Rainbow is looking to add gas generation and expects 2.1 gigawatts to be available, fed by a new 136 mile, 36 inch pipeline due in 2029. A POWER magazine article from July 2025 says the same plan is under consideration. No buyer has signed, no air permit or commission case was found, and no turbine, unit count or start year is given. The capacity is the 2,000 MW floor the company states. The point is the Coal Creek plant, so the location is approximate. The status is announced on the company's own planning document.

### Xcel Bison Generating Station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create Xcel Bison Generating Station in Harmony Township, Cass County, North Dakota, owned by Northern States Power Co with parent Xcel Energy Inc, then add the one unit below. Put MISO J3163 in Other IDs.
- `State/Province`: `` -> `North Dakota`
- `Local area (taluk, county)`: `` -> `Cass`
- `City`: `` -> `Harmony Township`
- `Latitude`: `` -> `46.9508`
- `Longitude`: `` -> `-97.0759`
- `Location accuracy`: `` -> `approximate`
- `Owner(s)`: `` -> `Northern States Power Co [100%]`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Capacity (MW)`: `447`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2032`
- unit 1 `Turbine/Engine Technology`: `gas turbine`
- unit 1 `Latest Activity`: `Year: 2025, Month: 10, Day: 23`
- location now: none in GEM
- location proposed: 46.9508, -97.0759 (approximate) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=46.95080,-97.07590&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=46.95080,-97.07590)
  - Location Data Source: https://www.psc.nd.gov/webdocs/case/24-0342/011-010.pdf (ok=True, contains_value=True)
  - Location Data Source: https://www.google.com/maps?q=46.9507742,-97.0758717 (ok=True, contains_value=True)
  - Owners Data Source: https://www.psc.nd.gov/webdocs/case/24-0342/011-010.pdf (ok=True, contains_value=True)
- confidence: high (independent: )
- notes: GEM does not list this plant. In case PU-24-342 at the North Dakota Public Service Commission, Northern States Power, doing business as Xcel Energy, must build a gas plant of at least 200 MW in eastern North Dakota. Its supplemental filing of August 5, 2025 says it bid 447 MW of firm dispatchable capacity directly adjacent to the Xcel Energy Bison Substation in Harmony Township, Cass County, about 10 miles west of Fargo. The project chart in that filing shows service in the third quarter of 2032. Xcel says it has already spent about 1.6 million dollars on site design, surveys, land options and MISO study payments. The timeline in the filing has the revised plant proposed in 2027, an interconnection agreement and a certificate filing in 2029, construction in 2030 and service late in 2032. The commission order of October 23, 2025 moved the deadline to December 31, 2032. MISO queue entry J3163 is the same project: Northern States Power, Cass County, 481 MW simple cycle combustion turbine, connecting at Bison. The filing gives 447 MW, so that is the capacity used. The status is announced because no certificate application or interconnection agreement exists yet. The point is the Bison Substation, so the location is approximate. The name is chosen to keep it apart from Basin Electric's Bison Generation Station in Williams County. GEM's Xcel Fargo power plant record is a cancelled 400 MW project from an earlier plan. A separate question card covers it.

### G100001101332 / Base Electron power station / 1
*watch item at an existing plant; checklist rows 51 (Newly announced projects checked)*
- what to watch: Applied Digital is only evaluating an option for another 1.2 GW with Base Electron, so there is no committed second phase.
- check again by: 2027-03
  - links: https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses (ok=None, contains_value=None)
- notes: The Babcock and Wilcox release at https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses says Applied Digital is evaluating an option for another 1.2 GW. Recheck when financial close is due on March 31, 2027.

### G100001054598 / Bison Generation Station / 1
*question about existing data; checklist rows 51 (Newly announced projects checked)*
- about: existence
- question: Does Bison need extra units for the Sierra Club CA1 and CA2 rows?
- finding: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists each block as a 496 MW combustion turbine plus a 263 MW steam turbine, generators CA1 and CT1 for block one and CA2 and CT2 for block two. The CA rows are the steam turbine halves of the two blocks that GEM holds as units 1 and 2.
- recommendation: Add no new units. Leave units 1 and 2 as combined cycle blocks.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: I did not cite the Sierra Club list. The Southwest Power Pool queue entries GEN-2024-081 and GEN-2024-082 were not downloaded in this pass.

### Cerilon gas to liquids complex, Trenton
*question about existing data*
- about: scope
- question: Should GEM track the steam power units at Cerilon's planned gas to liquids plant near Trenton?
- finding: The commission approved two gas to liquids plants near Trenton in Williams County, each with a 100 MW steam turbine plant driven by process heat and boilers burning leftover fuel gas. Most of the power is used on site and less than 50 MW per phase goes to the grid.
- recommendation: Leave it out of GEM for now. Add each phase as a 100 MW waste heat from natural gas steam turbine unit only if the manual's lead confirms captive waste heat units at a gas to liquids plant are in scope.
  - links: https://www.psc.nd.gov/webdocs/case/23-0325/067-010.pdf (ok=True, contains_value=True)
  - links: https://www.psc.nd.gov/webdocs/case/23-0325/001-010.pdf (ok=True, contains_value=True)
- notes: The commission order in case PU-23-325, dated September 27, 2024, approves the site and describes two phases, each with an associated 100 MW steam powered electric facility. Excess process heat drives the steam turbines, and the plant also has fuel gas fired boilers. Output is 65 to 81 MW per phase, depending on catalyst age. All power is sold to Basin Electric and all power used is bought from Lower Yellowstone Rural Electric Cooperative. Phase 1 construction starts in 2026 with operation in 2029. Phase 2 operation is planned for 2033. The application gives the site as Sections 25 and 36, Township 153 North, Range 103 West, about 1.5 miles southwest of Trenton. The state air permit draft for this site, ACP-18233 from November 2024, now returns a not found page and the Wayback Machine was offline when tried on October 29, 2026. The fuel would count as waste heat from natural gas with a steam turbine. Each phase is over 50 MW gross, which is why it is raised here.

### Harmony Energy Park data center, Geronimo Power
*watch item, new to the tracker; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
- what to watch: Geronimo Power plans a data center in Harmony Township, Cass County, that may draw on new gas generation, but no gas plant is named yet.
- check again by: 2027-04
  - links: https://www.valleynewslive.com/2026/09/30/2nd-fargo-area-data-center-would-use-double-power-harwood-site/ (ok=True, contains_value=True)
  - links: https://www.valleynewslive.com/2026/10/14/cass-county-residents-learn-more-about-proposed-harmony-energy-park-data-center/ (ok=True, contains_value=True)
- notes: Valley News Live stories from September and October 2026 say Geronimo Power filed for a conditional use permit for the Harmony Energy Park data center near the Bison Substation north of Mapleton. A story of September 30, 2026 says power may come from new renewables, batteries and natural gas, and that the site would use about twice the power of the Harwood data center. The company has a 200 MW solar farm and a planned 200 MW battery in commission case PU-26-284. No gas turbine, engine, size or air permit was found. Cass County was voting on a building moratorium in October 2026.

### G100000409510 / Lonesome Creek Station / 6
*question about existing data*
- about: duplicate
- question: Is Southwest Power Pool request GEN-2020-014 the same as unit 6 at Lonesome Creek?
- finding: The queue entry from the brief is 45 MW of gas at Lonesome Creek, in commercial operation with an in-service date of 17 June 2021. The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists six units at plant 57943, with unit 6 operating since October 2021. The state permit at https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf also lists six turbines.
- recommendation: Treat the request as unit 6 and add no new unit. Leave the unit count at six.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://deq.nd.gov/AQ/Notices/LonesomeCreek/LonesomeCrkNoticeSOBDraftPTO.pdf (ok=None, contains_value=None)
- notes: I did not open the Southwest Power Pool queue page itself because its list is drawn by script and the brief already quotes the entry. No seventh unit appears in the EIA table or the permit.

### G100001094120 / Polaris Forge 1 power station / 1
*question about existing data; checklist rows 51 (Newly announced projects checked)*
- about: existence
- question: Does Polaris Forge 1 have its own 400 megawatt gas steam plant, or is 400 megawatts the data center load?
- finding: The Applied Digital release at https://ir.applieddigital.com/news-events/press-releases/detail/133/applied-digital-achieves-ready-for-service-for-phase-1-at calls Polaris Forge 1 a 400 megawatt critical IT load campus in Ellendale, with a first phase of 50 megawatts. The Babcock and Wilcox release at https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses covers four 300 megawatt gas boilers with Siemens Energy steam turbines for Base Electron, and does not name Ellendale or Minnkota. No document found ties a steam plant to Ellendale.
- recommendation: Treat the 400 megawatts as data center load and do not keep this unit as a generating plant unless a document shows a power plant at Ellendale. Ask the plant owner or the reviewer who found the original entry for the source.
  - links: https://ir.applieddigital.com/news-events/press-releases/detail/133/applied-digital-achieves-ready-for-service-for-phase-1-at (ok=None, contains_value=None)
  - links: https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-receives-full-notice-to-proceed-on-24-billion-power-generation-project-for-base-electron-to-supply-power-to-applied-digital-ai-factory-campuses (ok=None, contains_value=None)
- notes: The Base Electron project of four 300 megawatt units is a separate plant in the database near Center, North Dakota. The diesel backup fleet at Ellendale is also separate. I could not read the Power magazine article on this, so I did not cite it.

### Polaris Forge 3 data center, Applied Digital, Center
*watch item, new to the tracker; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
- what to watch: Applied Digital's third North Dakota campus near Center will take 430 MW of grid power, and no backup generator fleet has been permitted for it yet.
- check again by: 2027-04
  - links: https://s25.q4cdn.com/697625600/files/doc_news/Montana-Dakota-Utilities-Announces-Electric-Service-Agreement-with-Applied-Digital-for-Proposed-AI-Factory-2026.pdf (ok=True, contains_value=True)
  - links: https://www.psc.nd.gov/webdocs/case/26-0155/001-020.pdf (ok=True, contains_value=True)
- notes: A Montana-Dakota Utilities release from 2026 says it signed an electric service agreement with Applied Digital for the Polaris Forge 3 campus near Center in Oliver County, needing 430 MW at full build, with first operation in August 2027. In commission case PU-26-155, filed April 23, 2026, Applied Digital says similar diesel engine backup generation would be used at its other North Dakota sites. Its Ellendale site has 252 engines of 3 MW. No air permit or engine count for Center was found among the state air notices read on October 29, 2026. A backup fleet there would very likely pass 50 MW and be an add once permitted.

### Project Fighting Pike data center, Critical Data House, Williston
*watch item, new to the tracker; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
- what to watch: A planned data center campus near Williston has no gas plant or backup generator fleet named yet.
- check again by: 2027-04
  - links: https://www.kfyrtv.com/2025/03/26/williston-commissioners-approve-plans-data-center-north-town/ (ok=True, contains_value=True)
- notes: KFYR TV reported on March 26, 2025 that Williston city commissioners approved plans for the Fighting Pike data center on the north side of town. Trade reports give seven buildings of 65 MW each, up to 455 MW of load, built in three phases over about ten years. No air permit, gas turbine or engine fleet for this campus was found among the state air notices or commission cases read on October 29, 2026.

### G100001090288 / River Run Energy Center / Unit 1
*question about existing data*
- about: scope
- question: Should River Run stay one 1,450 MW unit when the queue shows two 750 MW requests?
- finding: The Southwest Power Pool queue (https://opsportal.spp.org/Studies/GIActive) lists requests ERAS-2025-011 and ERAS-2025-012 at 750 megawatts each, in service 27 September 2029, at the Leland Olds substation. Company documents, such as the FAQ at https://www.nexteraenergyresources.com/river-run-energy-center/faq.html, give one plant of about 1,450 megawatts and never mention two blocks.
- recommendation: Leave one unit at 1,450 MW. Ask the project manager to split it into two 725 MW units only if a later filing shows two combined cycle blocks.
  - links: https://opsportal.spp.org/Studies/GIActive (ok=None, contains_value=None)
  - links: https://www.nexteraenergyresources.com/river-run-energy-center/faq.html (ok=None, contains_value=None)
- notes: I searched the harvested commission cases, the air permit harvest and company pages. I found no letter of intent, siting application or air permit application for this plant yet.

### Xcel Fargo power plant
*question about existing data*
- about: duplicate
- question: Is the new Xcel Bison plant the same project as GEM's cancelled Xcel Fargo power plant?
- finding: GEM lists Xcel Fargo as a 400 MW gas plant near Fargo, cancelled in 2022, with an approximate point. Xcel's filings in case PU-24-342 now name a 447 MW plant at the Bison Substation west of Fargo for 2032, to meet the same settlement duty from 2016.
- recommendation: Keep Xcel Fargo as cancelled, add Xcel Bison Generating Station as a new plant, and add a line to the Notes of each plant that links the two.
  - links: https://www.psc.nd.gov/webdocs/case/24-0342/011-010.pdf (ok=True, contains_value=True)
  - links: https://www.psc.nd.gov/webdocs/case/24-0342/016-010.pdf (ok=True, contains_value=True)
- notes: Xcel Fargo was last reviewed on October 29, 2026 and marked as no changes. The 2016 settlement required a gas plant of at least 200 MW in eastern North Dakota by the end of 2025. Xcel did not build one. In 2024 Xcel asked to move the deadline, and the commission moved it to the end of 2032 on October 23, 2025. The new site is next to the Bison Substation in Harmony Township, Cass County. The old record has no site beyond Fargo. A new record is cleaner than reviving the cancelled one, because the site, size and timeline have all changed.

## Checklist group Other

### G100001096407 / Nakota Data Center Campus Power Plant / 1
*change to an existing unit*
**Action:** Set Location Data Source of unit 1 (G100001096407) to approximate. It now says https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas. Add the link below to the Location Data Source Data Source box. Keep the links already there.
- `Location Data Source`: `https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas` -> `approximate`
  - Location Data Source Data Source: https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The letter of intent at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm places the campus on 620 acres about 5 miles west of Williston in Williams County. It gives no street address or parcel. This is offered as a live source for the dead Morningstar link. The point stays approximate.

### G100001096407 / Nakota Data Center Campus Power Plant / 1
*change to an existing unit*
**Action:** Set Fuel Data Source of unit 1 (G100001096407) to fossil gas: natural gas. It now says https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm, https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas. Add the link below to the Fuel Data Source Data Source box. Keep the links already there.
- `Fuel Data Source`: `https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm, https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas` -> `fossil gas: natural gas`
  - Fuel Data Source Data Source: https://www.businesswire.com/news/home/20260609432974/en/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The press release at https://www.businesswire.com/news/home/20260609432974/en/ says the campus will run on natural gas from the Williston Basin. It is offered as a live source for the dead Morningstar link.

### G100001096407 / Nakota Data Center Campus Power Plant / 1
*change to an existing unit*
**Action:** Set Status Data Source of unit 1 (G100001096407) to pre-construction. It now says https://hiranandaniltd.com/updates/hiranandani-backed-nidar-infrastructure-signs-binding-mou-and-offtake-agreement-with-tachyon9-nixxy-to-anchor-nakota-ai-data-campus-in-north-dakota/, https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm, https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas. Add the link below to the Status Data Source Data Source box. Keep the links already there.
- `Status Data Source`: `https://hiranandaniltd.com/updates/hiranandani-backed-nidar-infrastructure-signs-binding-mou-and-offtake-agreement-with-tachyon9-nixxy-to-anchor-nakota-ai-data-campus-in-north-dakota/, https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm, https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas` -> `pre-construction`
  - Status Data Source Data Source: https://www.businesswire.com/news/home/20260609432974/en/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The press release at https://www.businesswire.com/news/home/20260609432974/en/ says the first 150 megawatts are expected to be operational by the second quarter of 2027 and the campus is up to 1 gigawatt over a 36 month buildout. No air permit or commission case was found, so the status stays as in the database. It is offered as a live source for the dead Morningstar link.

### G100001096407 / Nakota Data Center Campus Power Plant / 1
*change to an existing unit*
**Action:** Set Turbine/Engine Technology Data Source of unit 1 (G100001096407) to gas turbine. It now says https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm, https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas. Add the link below to the Turbine/Engine Technology Data Source Data Source box. Keep the links already there.
- `Turbine/Engine Technology Data Source`: `https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm, https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas` -> `gas turbine`
  - Turbine/Engine Technology Data Source Data Source: https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The letter of intent at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm describes NovaLT16 gas turbines in simple cycle. It is offered as a live source for the dead Morningstar link.

### G100001096410 / Nakota Data Center Campus Power Plant / 2
*change to an existing unit*
**Action:** Set Location Data Source of unit 2 (G100001096410) to approximate. It now says https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas. Add the link below to the Location Data Source Data Source box. Keep the links already there.
- `Location Data Source`: `https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas` -> `approximate`
  - Location Data Source Data Source: https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The letter of intent at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm places the campus on 620 acres about 5 miles west of Williston in Williams County. It gives no street address or parcel. This is offered as a live source for the dead Morningstar link. The point stays approximate.

### G100001096410 / Nakota Data Center Campus Power Plant / 2
*change to an existing unit*
**Action:** Set Status Data Source of unit 2 (G100001096410) to announced. It now says https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas. Add the link below to the Status Data Source Data Source box. Keep the links already there.
- `Status Data Source`: `https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas` -> `announced`
  - Status Data Source Data Source: https://www.businesswire.com/news/home/20260609432974/en/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The press release at https://www.businesswire.com/news/home/20260609432974/en/ describes the up to 1 gigawatt campus as built out in phases over 36 months. It is offered as a live source for the dead Morningstar link.

### G100001101359 / Nakota Data Center Campus Power Plant / 3
*change to an existing unit*
**Action:** Set Location Data Source of unit 3 (G100001101359) to approximate. It now says https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas. Add the link below to the Location Data Source Data Source box. Keep the links already there.
- `Location Data Source`: `https://www.morningstar.com/news/business-wire/20260618848981/tachyon9-secures-offtake-agreement-supporting-156-million-annual-revenue-platform-and-up-to-1-gw-of-grid-independent-ai-infrastructure-powered-by-abundant-north-dakota-natural-gas` -> `approximate`
  - Location Data Source Data Source: https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The letter of intent at https://www.sec.gov/Archives/edgar/data/1462223/000168316826004843/nixxy_ex1001.htm places the campus on 620 acres about 5 miles west of Williston in Williams County. It gives no street address or parcel. This is offered as a live source for the dead Morningstar link. The point stays approximate.

### G100001017988 / Spiritwood Industrial Park / Unit 1, timepoint 2
*change to an existing unit*
**Action:** Leave CHP of unit Unit 1, timepoint 2 (G100001017988) as yes. It is still correct. Add the 2 links below to the CHP Data Source box. Keep the links already there.
- `CHP`: `yes` -> `yes`
  - CHP Data Source: https://www.psc.nd.gov/webdocs/case/26-0279/001-010.pdf (ok=True, contains_value=True)
  - CHP Data Source: https://www.psc.nd.gov/webdocs/case/16-0490/001-010.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The Great River Energy 2026 ten-year plan (https://www.psc.nd.gov/webdocs/case/26-0279/001-010.pdf) lists Spiritwood Station as a heat and power plant. The 2016 ten-year plan (https://www.psc.nd.gov/webdocs/case/16-0490/001-010.pdf) calls it a combined heat and power plant that began commercial operation on November 1, 2014. Both are filings by the same company, so they are one origin.

### G100000403835 / Heskett Station / Unit 4
*question about existing data*
- about: other
- question: Should the possible Heskett combined cycle conversion be tracked?
- finding: Montana-Dakota's 2024 North Dakota resource plan, volume IV (https://www.montana-dakota.com/wp-content/uploads/PDFs/Rates-Tariffs/2024-ND-IRP-Vol-4_nonprint.pdf), lists a 329.7 MW expansion of Heskett 3 and 4 to combined cycle among the least-cost options in some scenarios. The base plan only completes Heskett 4 in 2024.
- recommendation: Do not add anything. Check the next resource plan for a committed combined cycle.
  - links: https://www.montana-dakota.com/wp-content/uploads/PDFs/Rates-Tariffs/2024-ND-IRP-Vol-4_nonprint.pdf (ok=None, contains_value=None)
- notes: I found no commission case for it. The queue entries J1193 and R1000 are the earlier requests for unit 4.

## Checklist group 9. Close-out

Not record-level: the sheet and doc updates, research status, and the two database checks. These boxes are ticked by hand after the edits are applied: validation_report.py --closeout must print CLOSE-OUT CLEAN (row 54) and no_tracker.py lists the units with no tracker (row 56).
