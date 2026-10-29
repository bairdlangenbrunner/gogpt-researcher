# Evidence — gogpt batch 20261023_1440_ET (us-ms, update)

Each section below is one group of the GOGPT QC/Country checklist. The records in it are the evidence for ticking that group's boxes; the row numbers are the checklist tab's own.

## Utility resource plans (checklist row 37)

The IRP step read 3 utility rows of the US IRPs tab for this state. The records below come from a plan; the actions workbook's irp_box sheet says which units need the IRP box ticked, and its irp_notes_draft sheet has a draft line per utility for the tab's Notes column.

- Mississippi Power Company: 2024 IRP. Tracked plants matched: 4
- Entergy Mississippi: 2024 IRP. Tracked plants matched: 8
- Mississippi PSC: plan

## Checklist group 1. Validation report

Edits and questions that fix an error from the GEM validation report.

### G100001017948 / Jack Watson Generating Plant / Unit 4, timepoint 2
*change to an existing unit; checklist rows 7 (Validation report errors fixed), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of all 2 units of Jack Watson Generating Plant as Mississippi Power Co [100%]. It is still correct. Add the 2 links below to the Owners Data Source box on each unit. Keep the links already there.
- `Owner(s)`: `Mississippi Power Co [100%]` -> `Mississippi Power Co [100%]`
  - Owners Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1583174 (ok=True, contains_value=True)
  - Owners Data Source: https://www.sec.gov/Archives/edgar/data/92122/000009212226000006/so-20251231.htm (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The Mississippi air permit renewal issued July 2022 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1583174) names Mississippi Power Company as the owner and operator of Plant Jack Watson. Southern Company's 2025 annual report (https://www.sec.gov/Archives/edgar/data/92122/000009212226000006/so-20251231.htm) lists the Watson steam units, 750 MW, under Mississippi Power. The EIA-860M table for September 2026 also names Mississippi Power Co as the entity for plant 2049. This agrees with GEM.

### G100001017948 / Jack Watson Generating Plant / Unit 4, timepoint 2
*change to an existing unit; checklist rows 7 (Validation report errors fixed), 25 (Location data for every entry), 42 (Exact location for approximate operating units (optional))*
**Action:** Leave the point of all 2 units of Jack Watson Generating Plant as it is. Add the 2 links below to the Location Data Source box on each unit. Keep the links already there.
- `Latitude`: `30.4392330` -> `30.4392330`
- `Longitude`: `-89.0261060` -> `-89.0261060`
- `Location accuracy`: `exact` -> `exact`
- location now: 30.4392330, -89.0261060 (exact) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=30.43923,-89.02611&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=30.43923,-89.02611)
- location proposed: 30.4392330, -89.0261060 (exact) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=30.43923,-89.02611&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=30.43923,-89.02611)
  - Location Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1583174 (ok=True, contains_value=False)
  - Location Data Source: https://www.google.com/maps/search/?api=1&query=30.43923,-89.02611 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The air permit at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1583174 gives the plant address as 10406 Lorraine Road, Gulfport, Mississippi 39503. The Census geocoder puts that address at 30.44115, -89.03097, about half a kilometer from GEM's point. A satellite picture of GEM's point at 30.43923, -89.02611 (imagery date unknown) shows the plant itself, with the boiler house, stacks, switchyard and cooling canal under the crosshair. So GEM's point is on the plant and stays as it is.

### G100000409451 / Morrow Generating Plant / MOR1
*change to an existing unit; checklist rows 7 (Validation report errors fixed), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of unit MOR1 (G100000409451) as Cooperative Energy [100%]. It is still correct. Add the 2 links below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Cooperative Energy [100%]` -> `Cooperative Energy [100%]`
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://cooperativeenergy.com/cooperative-energys-plant-morrow-enters-new-era/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 lists Cooperative Energy as the entity for plant 6061, and a Cooperative Energy announcement (https://cooperativeenergy.com/cooperative-energys-plant-morrow-enters-new-era/) calls Plant Morrow its plant. The documents agree with the value GEM holds.

### G100000409451 / Morrow Generating Plant / MOR1
*change to an existing unit; checklist rows 7 (Validation report errors fixed), 25 (Location data for every entry), 42 (Exact location for approximate operating units (optional))*
**Action:** Leave the point of unit MOR1 (G100000409451) as it is. Add the 3 links below to the Location Data Source box. Keep the links already there.
- `Latitude`: `31.2177560` -> `31.2177560`
- `Longitude`: `-89.3939720` -> `-89.3939720`
- `Location accuracy`: `exact` -> `exact`
- location now: 31.2177560, -89.3939720 (exact) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=31.21776,-89.39397&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=31.21776,-89.39397)
- location proposed: 31.2177560, -89.3939720 (exact) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=31.21776,-89.39397&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=31.21776,-89.39397)
  - Location Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Location Data Source: https://www.google.com/maps/search/?api=1&query=31.21776,-89.39397 (ok=True, contains_value=True)
  - Location Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1407519 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table lists the plant at 31.2186. GEM's point is about 94 meters from it. The point sits on the power block in a satellite picture. The Mississippi Department of Environmental Quality air permit from February 2020 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1407519) covers the Morrow plant and its combustion turbines, and the department's facility page gives the address 304 Old Okahola School Road, Purvis. Same document set and note as the latitude. The satellite picture at the point shows the stacks, turbine hall, cooling equipment and switchyard of the power block. The date of the imagery is unknown.

### G100001070976 / Colossus 2 power station / 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: The pre-construction step is best dated to August 2025, when MZX Tech LLC applied to the Mississippi Department of Environmental Quality for an air construction permit on August 22, 2025. The permit was issued on March 10 to 11, 2026. The application date comes from the department's enSearch facility history for MZX Tech LLC, facility 12592.
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1834338 (ok=None, contains_value=None)
  - links: https://www.mississippifreepress.org/mississippi-permit-board-grants-xais-request-for-41-southaven-gas-turbines-to-power-memphis-data-center/ (ok=None, contains_value=None)
- notes: The permit itself is at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1834338 and shows permit 0680-00119. The Permit Board approved it on March 10, 2026, per https://www.mississippifreepress.org/mississippi-permit-board-grants-xais-request-for-41-southaven-gas-turbines-to-power-memphis-data-center/.

### G100001030673 / Delta Blues Advanced Power Station / 1
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: The construction step is best dated to November 2024. Entergy Mississippi held a groundbreaking on November 7, 2024, which POWER Magazine reported on November 8, 2024. The Mississippi air construction permit was issued later, on April 16, 2025.
  - links: https://www.powermag.com/entergy-mississippi-breaks-ground-on-754-mw-gas-fired-power-station/ (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1779807 (ok=None, contains_value=None)
- notes: Sources are https://www.powermag.com/entergy-mississippi-breaks-ground-on-754-mw-gas-fired-power-station/ and the air permit at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1779807.

### G100001017948 / Jack Watson Generating Plant / Unit 4, timepoint 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: I found no document that states whether a carbon capture system is attached to this unit. The Mississippi air permit renewal of July 2022 lists the plant's boilers and turbines and mentions no carbon capture equipment. The value in GEM is no, and nothing found contradicts it.
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1583174 (ok=None, contains_value=None)
- notes: Looked at the air permit at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1583174 and Southern Company's 2025 annual report. Neither mentions carbon capture at Plant Watson.

### G100001017947 / Jack Watson Generating Plant / Unit 5, timepoint 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: I found no document that states whether a carbon capture system is attached to this unit. The Mississippi air permit renewal of July 2022 lists the plant's boilers and turbines and mentions no carbon capture equipment. The value in GEM is no, and nothing found contradicts it.
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1583174 (ok=None, contains_value=None)
- notes: Looked at the air permit at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1583174 and Southern Company's 2025 annual report. Neither mentions carbon capture at Plant Watson.

### G100001028154 / New Caledonia power station / 1
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: The construction step has no date in the database. The Commercial Dispatch article from October 23, 2025 (https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/) says the groundbreaking ceremony was October 22, 2025, and that construction was already well under way. The air construction permit was issued May 12, 2025 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643). I would date the construction step to October 2025, and earlier work may have started before the ceremony.
  - links: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=None, contains_value=None)
- notes: Dated from the groundbreaking article.

### G100001028155 / New Caledonia power station / 2
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: The construction step has no date in the database. The Commercial Dispatch article from October 23, 2025 (https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/) says the groundbreaking ceremony was October 22, 2025, and that construction was already well under way. The air construction permit was issued May 12, 2025 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643). I would date the construction step to October 2025, and earlier work may have started before the ceremony.
  - links: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=None, contains_value=None)
- notes: Dated from the groundbreaking article.

### G100001028156 / New Caledonia power station / 3
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: The construction step has no date in the database. The Commercial Dispatch article from October 23, 2025 (https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/) says the groundbreaking ceremony was October 22, 2025, and that construction was already well under way. The air construction permit was issued May 12, 2025 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643). I would date the construction step to October 2025, and earlier work may have started before the ceremony.
  - links: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=None, contains_value=None)
- notes: Dated from the groundbreaking article.

### G100001028157 / New Caledonia power station / 4
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: The construction step has no date in the database. The Commercial Dispatch article from October 23, 2025 (https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/) says the groundbreaking ceremony was October 22, 2025, and that construction was already well under way. The air construction permit was issued May 12, 2025 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643). I would date the construction step to October 2025, and earlier work may have started before the ceremony.
  - links: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=None, contains_value=None)
- notes: Dated from the groundbreaking article.

### G100001028158 / New Caledonia power station / 5
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: The construction step has no date in the database. The Commercial Dispatch article from October 23, 2025 (https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/) says the groundbreaking ceremony was October 22, 2025, and that construction was already well under way. The air construction permit was issued May 12, 2025 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643). I would date the construction step to October 2025, and earlier work may have started before the ceremony.
  - links: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=None, contains_value=None)
- notes: Dated from the groundbreaking article.

### G100001028159 / New Caledonia power station / 6
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: The construction step has no date in the database. The Commercial Dispatch article from October 23, 2025 (https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/) says the groundbreaking ceremony was October 22, 2025, and that construction was already well under way. The air construction permit was issued May 12, 2025 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643). I would date the construction step to October 2025, and earlier work may have started before the ceremony.
  - links: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=None, contains_value=None)
- notes: Dated from the groundbreaking article.

### G100001074418 / Traceview Advanced power station / Unit 1
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: The announced step is dated April 2025. Entergy's news release of April 11, 2025 says the company selected a site on West County Line Road in Ridgeland and held a town hall about the plans (https://www.entergy.com/news/entergy-mississippi-selects-new-power-generation-site-prioritizes-community-needs). The Ridgeland city council approved the plans on April 24, 2025 according to a WLBT article already cited by GEM.
  - links: https://www.entergy.com/news/entergy-mississippi-selects-new-power-generation-site-prioritizes-community-needs (ok=None, contains_value=None)
- notes: I read the Entergy release. I did not re-open the WLBT article, so the second date rests on the title of the existing source.

### G100001091020 / Vicksburg Advanced power station / 1A
*question about existing data; checklist rows 7 (Validation report errors fixed)*
- about: validation
- recommendation: The construction step is dated October 2025. Entergy held the groundbreaking on October 21, 2025 (https://www.wlbt.com/2025/10/22/leaders-attend-new-vicksburg-advanced-power-station-groundbreaking-ceremony), and the Magnolia Tribune reported it on October 23, 2025 (https://magnoliatribune.com/2025/10/23/entergy-mississippi-breaks-ground-on-1-2-billion-vicksburg-advanced-power-station/).
  - links: https://www.wlbt.com/2025/10/22/leaders-attend-new-vicksburg-advanced-power-station-groundbreaking-ceremony (ok=None, contains_value=None)
  - links: https://magnoliatribune.com/2025/10/23/entergy-mississippi-breaks-ground-on-1-2-billion-vicksburg-advanced-power-station/ (ok=None, contains_value=None)
- notes: The WLBT article says the ceremony was held Tuesday.

## Checklist group 2. Blanks and unknowns

Empty or unknown cells that the research filled, and the ones it could not.

### G100000401786 / Batesville generation facility / CC1
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit CC1 (G100000401786) as 297.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `297.0` -> `297.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026, https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55063, generators CTG1 and STG1, status operating, 184.5 MW plus 112.5 MW, operating August 2000, with no planned retirement date. The two parts add to 297.0 MW, which matches GEM.

### G100000401787 / Batesville generation facility / CC2
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit CC2 (G100000401787) as 297.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `297.0` -> `297.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026, https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55063, generators CTG2 and STG2, status operating, 184.5 MW plus 112.5 MW, operating August 2000, with no planned retirement date. The two parts add to 297.0 MW, which matches GEM.

### G100000401788 / Batesville generation facility / CC3
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit CC3 (G100000401788) as 297.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `297.0` -> `297.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026, https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55063, generators CTG3 and STG3, status operating, 184.5 MW plus 112.5 MW, operating August 2000, with no planned retirement date. The two parts add to 297.0 MW, which matches GEM.

### G100000401837 / Caledonia power station / CCC1
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit CCC1 (G100000401837) as 267.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `267.0` -> `267.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The same EIA table gives CTG1 at 161.0 MW and STG1 at 106.0 MW, which adds to 267 MW, the value GEM already shows.

### G100000401838 / Caledonia power station / CCC2
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit CCC2 (G100000401838) as 267.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `267.0` -> `267.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The same EIA table gives CTG2 at 161.0 MW and STG2 at 106.0 MW, which adds to 267 MW, the value GEM already shows.

### G100000401839 / Caledonia power station / CCC3
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit CCC3 (G100000401839) as 267.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `267.0` -> `267.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The same EIA table gives CTG3 at 161.0 MW and STG3 at 106.0 MW, which adds to 267 MW, the value GEM already shows.

### G100000403187 / Chevron Oil power station / 5
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 5 (G100000403187) as 101.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `101.0` -> `101.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The same EIA table gives a nameplate of 101.3 MW. GEM shows 101.0, so this is only a rounding difference. Change it only if you want the table's figure.

### G100000401972 / Choctaw County power station / CC1
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit CC1 (G100000401972) as 899.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `899.0` -> `899.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The same EIA table gives three turbines of 179.0 MW and one steam turbine of 362.0 MW. Together that is 899 MW, the value GEM already shows.

### G100000401924 / Magnolia power plant / MCC1
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit MCC1 (G100000401924) as 335.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `335.0` -> `335.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists CTG1 at 178.5 MW and STG1 at 156.0 MW. Together that is 334.5 MW, which rounds to the 335 MW GEM already shows. Plant 55451, unit code MCC1, status operating.

### G100000401925 / Magnolia power plant / MCC2
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit MCC2 (G100000401925) as 335.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `335.0` -> `335.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists CTG2 at 178.5 MW and STG2 at 156.0 MW. Together that is 334.5 MW, which rounds to the 335 MW GEM already shows. Plant 55451, unit code MCC2, status operating.

### G100000401926 / Magnolia power plant / MCC3
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit MCC3 (G100000401926) as 335.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `335.0` -> `335.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists CTG3 at 178.5 MW and STG3 at 156.0 MW. Together that is 334.5 MW, which rounds to the 335 MW GEM already shows. Plant 55451, unit code MCC3, status operating.

### G100000401969 / Quantum Choctaw Power station / CC1
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit CC1 (G100000401969) as 851.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `851.0` -> `851.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists this unit as operating. The nameplate is 850.5 MW. The table lists plant 55694 with two gas turbines of 270.0 MW each and one steam turbine of 310.5 MW. Together that is 850.5 MW, a little under the 851.0 MW GEM shows. Start year 2006 is unchanged.

### G100000402041 / Ratcliffe power plant / 1
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 1 (G100000402041) as 840.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `840.0` -> `840.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists this unit as operating. The nameplate is 840.0 MW. The table lists plant 57037 with two gas turbines of 235.5 MW each and one steam turbine of 369.0 MW. Together that is 840.0 MW, which matches GEM. Start year 2014 is unchanged.

### G100000402661 / Silver Creek power station / 1
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 1 (G100000402661) as 84.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `84.0` -> `84.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists this unit as operating. The nameplate is 83.5 MW. The table lists plant 7988, generator 1, nameplate 83.5 MW, operating year 2003. GEM shows 84.0 MW.

### G100000402662 / Silver Creek power station / 2
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 2 (G100000402662) as 84.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `84.0` -> `84.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists this unit as operating. The nameplate is 83.5 MW. The table lists plant 7988, generator 2, nameplate 83.5 MW, operating year 2004. GEM shows 84.0 MW.

### G100000402663 / Silver Creek power station / 3
*change to an existing unit*
**Action:** Leave Capacity (MW) of unit 3 (G100000402663) as 84.0. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `84.0` -> `84.0`
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists this unit as operating. The nameplate is 83.5 MW. The table lists plant 7988, generator 3, nameplate 83.5 MW, operating year 2005. GEM shows 84.0 MW.

### G100001074418 / Traceview Advanced power station / Unit 1
*change to an existing unit; checklist rows 25 (Location data for every entry)*
**Action:** Set Latitude of unit Unit 1 (G100001074418) to 32.40700, Longitude to -90.21500 and Location accuracy to approximate. They now say 32.4100000, -90.1450000 and approximate, about 6.6 km away. Add the 3 links below to the Location Data Source box. Keep the links already there.
- `Latitude`: `32.4100000` -> `32.40700`
- `Longitude`: `-90.1450000` -> `-90.21500`
- `Location accuracy`: `approximate` -> `approximate`
- location now: 32.4100000, -90.1450000 (approximate) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=32.41000,-90.14500&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=32.41000,-90.14500)
- location proposed: 32.40700, -90.21500 (approximate) [satellite](https://www.google.com/maps/@?api=1&map_action=map&center=32.40700,-90.21500&zoom=17&basemap=satellite) [pin](https://www.google.com/maps/search/?api=1&query=32.40700,-90.21500)
- moved: 6.6 km
- method: placed from a site reference in a document
  - Location Data Source: https://www.entergymississippi.com/generation/traceview (ok=True, contains_value=True)
  - Location Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274 (ok=True, contains_value=True)
  - Location Data Source: https://www.google.com/maps/search/?api=1&query=32.40700,-90.21500 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Entergy Mississippi's Traceview project page at https://www.entergymississippi.com/generation/traceview says the plant will sit north of West County Line Road in Ridgeland, between Livingston Road and the Natchez Trace Parkway, next to an existing high-voltage transmission corridor, on a 585 acre property. The final air permit from the Mississippi Department of Environmental Quality, issued October 14, 2026, gives the address as 1972 W County Line Road at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274. Entergy's July 2026 informational filing to the Mississippi Public Service Commission in docket 2026-UA-55 says the same 585 acre site lies next to the Amazon Web Services facility in Madison County. In satellite imagery of unknown date, the only large cleared ground between those roads is a set of graded pads on both sides of the transmission lines, about 800 meters north of West County Line Road. The Amazon Web Services data center buildings are visible about 2 kilometers to the east, past Livingston Road. I placed the point at 32.40700, -90.21500, at the middle of the graded pads where the transmission lines cross them. No stacks, turbine hall or switchyard are built yet, so the point stays approximate. GEM's current point at 32.41000, -90.14500 is about 6.6 kilometers east of the site, in a different part of Madison County. This goes with the latitude. The point is the middle of the graded site north of West County Line Road described in the latitude note. The satellite picture shows cleared and graded ground and a construction yard on the described property, but no plant buildings yet. The date of the imagery is unknown. I cannot tell which pad will hold the turbine and which the switchyard, so the point is approximate. Status moved from announced to pre-construction on the strength of the October 2026 air permit. I did not find the turbine make and model in the permit, the hearing notice or Entergy pages. Capacity is raised as a question because sources differ. Latest Activity is left alone because the project is moving. The move from GEM's point is about 6.6 kilometers, so the site was checked again against Entergy's description, the permit address and the EIA point, and all three agree. Entergy's own description of the site matches the graded ground in the picture, and the street address and the EIA-860M point for plant 70187 both fall on or next to the same property. The EIA point at 32.40565, -90.22114 is about 600 meters west of my point, on the western cleared area of the same property. The address geocodes to the road edge about 800 meters to the south. All three agree on the site, so no further look is needed.

### G100001053819 / Colossus 2 power station / 1
*question about existing data*
- about: Capacity (MW)
- recommendation: GEM shows 495 MW for 27 temporary turbines. The state order of July 30, 2026 covers 69 temporary turbines, and 46 were reported in May 2026. The megawatts for the extra turbines are not stated in any source I found. The count and capacity of unit 1 should be rechecked, though the whole group is being retired by July 2027.
  - links: https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/ (ok=None, contains_value=None)
- notes: See https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/ and https://mississippitoday.org/2026/05/11/xai-46-gas-turbines-no-air-permits/.

### G100001053819 / Colossus 2 power station / 1
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: The September 2026 EIA-860M table lists plant 55373, Enterprise Energy Facility, with generators CT3, CT4, CT5 and CT6, each 86.5 MW natural gas combustion turbines, operating since 2002 and retired in 2006. Its coordinates of 34.97667 and -90.03944 are about 0.6 km from GEM's point, and it appears to be the former Duke Energy plant that xAI bought, so it is the same site. The table lists the county as Clark, but the coordinates are in DeSoto County. These are the old retired turbines, not the xAI turbines, so none of the four generators matches unit 1 or unit 2. I did not report the codes as values. The old plant retired in 2006, before GEM's 2020 floor for retired units, so no record is needed.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: Source is the EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx. The former Duke Energy purchase is reported at https://www.datacenterdynamics.com/en/news/elon-musks-xai-buys-former-gas-power-plant-site-in-southaven-mississippi/.

### G100001028154 / New Caledonia power station / 1
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: The EIA-860M table for September 2026 lists six generators at plant 69147, G1 to G6, all 84 MW gas combustion turbines planned for December 2028. The table does not say which one is this unit. With six identical units, I suggest unit 1 maps to G1, but nothing sourced confirms the order.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: No document links generator ids to unit numbers.

### G100001028155 / New Caledonia power station / 2
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: The EIA-860M table for September 2026 lists six generators at plant 69147, G1 to G6, all 84 MW gas combustion turbines planned for December 2028. The table does not say which one is this unit. With six identical units, I suggest unit 2 maps to G2, but nothing sourced confirms the order.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: No document links generator ids to unit numbers.

### G100001028156 / New Caledonia power station / 3
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: The EIA-860M table for September 2026 lists six generators at plant 69147, G1 to G6, all 84 MW gas combustion turbines planned for December 2028. The table does not say which one is this unit. With six identical units, I suggest unit 3 maps to G3, but nothing sourced confirms the order.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: No document links generator ids to unit numbers.

### G100001028157 / New Caledonia power station / 4
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: The EIA-860M table for September 2026 lists six generators at plant 69147, G1 to G6, all 84 MW gas combustion turbines planned for December 2028. The table does not say which one is this unit. With six identical units, I suggest unit 4 maps to G4, but nothing sourced confirms the order.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: No document links generator ids to unit numbers.

### G100001028158 / New Caledonia power station / 5
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: The EIA-860M table for September 2026 lists six generators at plant 69147, G1 to G6, all 84 MW gas combustion turbines planned for December 2028. The table does not say which one is this unit. With six identical units, I suggest unit 5 maps to G5, but nothing sourced confirms the order.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: No document links generator ids to unit numbers.

### G100001028159 / New Caledonia power station / 6
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: The EIA-860M table for September 2026 lists six generators at plant 69147, G1 to G6, all 84 MW gas combustion turbines planned for December 2028. The table does not say which one is this unit. With six identical units, I suggest unit 6 maps to G6, but nothing sourced confirms the order.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: No document links generator ids to unit numbers.

### Traceview Advanced power station
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: No change. The MISO fast-track request E0047, the Lakeover combined cycle plant, is this plant.
  - links: https://cdn.misoenergy.org/ERAS%20Interconnection%20Requests718482.xlsx (ok=True, contains_value=True)
  - links: https://www.entergymississippi.com/generation/traceview (ok=True, contains_value=True)
  - links: https://www.mdeq.ms.gov/wp-content/uploads/2026/06/Notice-of-Public-Hearing.pdf (ok=True, contains_value=True)
- notes: MISO's Expedited Resource Addition Study list at https://cdn.misoenergy.org/ERAS%20Interconnection%20Requests718482.xlsx shows request E0047: Entergy Mississippi, Hinds County, a new Green Acres 230 kV substation, gas combined cycle, 820 MW maximum and 763.2 MW requested, in service 8/4/2028, study cycle 2, with the interconnection agreement executed or filed. Its summary reads: "The Lakeover CCCT (J3825) is one of two generators proposed to serve" new load of 1,000 to 1,300 MW, including large data centers. Entergy Mississippi's Traceview page at https://www.entergymississippi.com/generation/traceview describes a 754 MW combined cycle plant at Ridgeland, on the Hinds and Madison county line. The state air hearing notice at https://www.mdeq.ms.gov/wp-content/uploads/2026/06/Notice-of-Public-Hearing.pdf covers permit 1720-00100 for Traceview. The owner, site, size and 2028 date match, so Lakeover was the working name for Traceview. No new plant is needed.

### G100001074418 / Traceview Advanced power station / Unit 1
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: Confirm that EIA plant 70187 is this plant and record its codes by hand. The EIA-860M table for September 2026 lists plant 70187, Traceview Advanced Power Station, in Madison County with generator CT1 (477.7 MW) and generator ST1 (341.7 MW), both natural gas combined cycle, planned for August 2028.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: The name, county, owner and permit all match this plant. GEM holds one combined cycle block as one unit, so the two EIA generators belong to Unit 1. Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx

### Vicksburg Advanced power station
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: No change. The MISO fast-track request E0031, the Vicksburg combined cycle plant, is this plant. The reviewer may compare the queue's August 2027 in-service date with the start year GEM holds.
  - links: https://cdn.misoenergy.org/ERAS%20Interconnection%20Requests718482.xlsx (ok=True, contains_value=True)
- notes: MISO's Expedited Resource Addition Study list at https://cdn.misoenergy.org/ERAS%20Interconnection%20Requests718482.xlsx shows request E0031, the Vicksburg CCCT (J3583): Entergy Mississippi, Warren County, at the Baxter Wilson 115 kV substation, gas combined cycle, 820 MW maximum and 768.1 MW requested, in service 8/21/2027. That matches this plant by owner, county, fuel and size, so no new plant is needed.

### G100001091020 / Vicksburg Advanced power station / 1A
*question about existing data; checklist rows 25 (Location data for every entry)*
- about: location
- recommendation: GEM's point is 32.2831, -90.9306, the old Baxter Wilson coordinates. The EIA table puts the new plant at 32.28526, -90.92568, about 500 meters east. The permit address is 770 Kemp Bottom Road.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1845094 (ok=None, contains_value=None)
- notes: Not changed. This brief had no location task.

### Victor J Daniel Jr power station
*question about existing data; checklist rows 11 (Every unit has a unit name)*
- about: identity
- recommendation: Decide whether to hold one gas conversion record for Daniel, named Unit 2 for now, and fix the unit number once Mississippi Power says which coal unit it will convert.
  - links: https://www.psc.ms.gov/sites/default/files/2026-07/7-7-26-Agenda.pdf (ok=None, contains_value=None)
- notes: The Sierra Club planned unit 2 of 548 MW matches this conversion project. It is not a new plant. The original petition in docket 2026-UA-5 names Unit 2. The June 2026 supplemental petition leaves the choice between Unit 1 and Unit 2 open. The commission agenda for 7 July 2026 (https://www.psc.ms.gov/sites/default/files/2026-07/7-7-26-Agenda.pdf) shows a proposed order was up for action, but I did not find the final order.

## Checklist group 3. Status and timeline

Status changes, start and retirement years, planned retirements, Latest Activity.

### G100000401786 / Batesville generation facility / CC1
*change to an existing unit*
**Action:** Leave Start year of unit CC1 (G100000401786) as 2000. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2000` -> `2000`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026, https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55063, generators CTG1 and STG1, status operating, 184.5 MW plus 112.5 MW, operating August 2000, with no planned retirement date. So the start year 2000 is confirmed.

### G100000401787 / Batesville generation facility / CC2
*change to an existing unit*
**Action:** Leave Start year of unit CC2 (G100000401787) as 2000. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2000` -> `2000`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026, https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55063, generators CTG2 and STG2, status operating, 184.5 MW plus 112.5 MW, operating August 2000, with no planned retirement date. So the start year 2000 is confirmed.

### G100000401788 / Batesville generation facility / CC3
*change to an existing unit*
**Action:** Leave Start year of unit CC3 (G100000401788) as 2000. It is still correct. Add the link below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2000` -> `2000`
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026, https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55063, generators CTG3 and STG3, status operating, 184.5 MW plus 112.5 MW, operating August 2000, with no planned retirement date. So the start year 2000 is confirmed.

### G100000402851 / Baxter Wilson power station / 1
*change to an existing unit; checklist rows 21 (Planned retirements searched)*
**Action:** Leave Retired year of unit 1 (G100000402851) as 2023. It is still correct. Add the link below to the Retired Year Data Source box. Keep the links already there.
- `Retired year`: `2023` -> `2023`
  - Retired Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists Baxter Wilson plant 2050, generator 1, as retired. It shows nameplate 544.6 MW, operating March 1967 and retirement March 2023. So the retired year 2023 in GEM is confirmed. Retirement in March 2023 confirmed by the EIA table.

### G100001070976 / Colossus 2 power station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Capacity (MW) of unit 2 (G100001070976) as 1240.5. It is still correct. Add the link below to the Capacity Data Source box. Keep the links already there.
- `Capacity (MW)`: `1240.5` -> `1240.5`
  - Capacity Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1834338 (ok=True, contains_value=False)
- confidence: medium (independent: False)
- notes: The air permit issued March 11, 2026 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1834338) lists 41 turbines: 17 Solar Titan PGM-130 sets of about 16.5 MW, 16 Solar Titan 350 sets of 35 MW and 8 ProEnergy 6000PE sets of 50 MW. That adds to 280.5 plus 560 plus 400, which is 1,240.5 MW. The permit does not print the total, so I added it myself. GEM's capacity is right. The 41 turbines form one permitted plant at one site. I found no document that says whether they share one grid connection, because the plant is built to power the data center directly. I found no operating date for the permanent plant. Latest Activity is left alone because there was news in July 2026.

### G100001070976 / Colossus 2 power station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 15 (Turbine make and model searched for in-development units)*
**Action:** Set Equipment Manufacturer/Model of unit 2 (G100001070976) to Solar Turbines: Titan PGM-130; Solar Turbines: Titan-350; ProEnergy: 6000PE. It now says Solar Turbines: Titan-350. Add the link below to the Turbine/Engine Equipment Data Source box. Keep the links already there.
- `Equipment Manufacturer/Model`: `Solar Turbines: Titan-350` -> `Solar Turbines: Titan PGM-130; Solar Turbines: Titan-350; ProEnergy: 6000PE`
  - Turbine/Engine Equipment Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1834338 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The air permit (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1834338) names three models, not only the Titan 350. Only 16 of the 41 turbines are Titan 350 sets. GEM's current value covers 560 of the 1,240.5 MW.

### G100001070976 / Colossus 2 power station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 19 (Missing or unknown owner searched)*
**Action:** Set Owner(s) of unit 2 (G100001070976) to MZX Tech LLC [100%]. It now says MZT Tech LLC [100%]. Add the 2 links below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `MZT Tech LLC [100%]` -> `MZX Tech LLC [100%]`
  - Owners Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1834338 (ok=True, contains_value=True)
  - Owners Data Source: https://www.sec.gov/Archives/edgar/data/0001697500/000162828026054349/sei-20260630.htm (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The air permit and the Solaris Energy Infrastructure report for June 2026 (https://www.sec.gov/Archives/edgar/data/0001697500/000162828026054349/sei-20260630.htm) both name MZX Tech LLC. GEM's spelling MZT Tech LLC looks like a typing error. This is a spelling fix, not a change of owner. A separate question about the leased equipment is raised in the questions list.

### G100001070976 / Colossus 2 power station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Add the entry below at the top of the Status Detail box of unit 2 (G100001070976), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On March 10, 2026 the Mississippi Permit Board approved air construction permit 0680-00119 for MZX Tech LLC, covering 41 permanent turbines of 1,240.5 megawatts in total. In July 2026 xAI said it is constructing a 1.2 gigawatt plant under that permit, and news reports say supply problems have delayed the 41 turbines.

https://www.mississippifreepress.org/mississippi-permit-board-grants-xais-request-for-41-southaven-gas-turbines-to-power-memphis-data-center/
https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/
- `Status Detail`: `JM: permit page https://opcgis.deq.state.ms.us/ensearchonline/publichearingdetails.aspx?id=107
17 x 16.5MW Solar Titan Model PGM-130
16 x 35MW Solar Titan Model 350
8 x 50MW ProEnergy Model 6000PE

NF 10/30/25: There is an option to deploy 1.5 GW of turbines. To deploy faster than peers, xAI relies on rental turbine companies. This source mentions that there are ~240MW on the Memphis Colossus 1 site, while the remaining 900MW will be owned by a Joint Venture owned at 50.1% by Solaris and 49.9% by xAI. https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter It is unclear if 240 MW will be built in addition to currently operating 198 MW at the Colossus 1. If yes, 1.1 GW will need to be split between the two plants.` -> `On March 10, 2026 the Mississippi Permit Board approved air construction permit 0680-00119 for MZX Tech LLC, covering 41 permanent turbines of 1,240.5 megawatts in total. In July 2026 xAI said it is constructing a 1.2 gigawatt plant under that permit, and news reports say supply problems have delayed the 41 turbines.

https://www.mississippifreepress.org/mississippi-permit-board-grants-xais-request-for-41-southaven-gas-turbines-to-power-memphis-data-center/
https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/

JM: permit page https://opcgis.deq.state.ms.us/ensearchonline/publichearingdetails.aspx?id=107
17 x 16.5MW Solar Titan Model PGM-130
16 x 35MW Solar Titan Model 350
8 x 50MW ProEnergy Model 6000PE

NF 10/30/25: There is an option to deploy 1.5 GW of turbines. To deploy faster than peers, xAI relies on rental turbine companies. This source mentions that there are ~240MW on the Memphis Colossus 1 site, while the remaining 900MW will be owned by a Joint Venture owned at 50.1% by Solaris and 49.9% by xAI. https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter It is unclear if 240 MW will be built in addition to currently operating 198 MW at the Colossus 1. If yes, 1.1 GW will need to be split between the two plants.`
  - Status Detail: https://www.mississippifreepress.org/mississippi-permit-board-grants-xais-request-for-41-southaven-gas-turbines-to-power-memphis-data-center/ (ok=True, contains_value=True)
  - Status Detail: https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: New dated entry for the Status Detail box, from a Mississippi Free Press article about the March 10, 2026 board vote (https://www.mississippifreepress.org/mississippi-permit-board-grants-xais-request-for-41-southaven-gas-turbines-to-power-memphis-data-center/) and the Mississippi Today article of July 31, 2026 (https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/).

### G100001030673 / Delta Blues Advanced Power Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked)*
**Action:** Leave Status of unit 1 (G100001030673) as construction. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `construction` -> `construction`
  - Status Data Source: https://www.entergy.com/blog/delta-blues-reaches-important-milestone-in-construction (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: An Entergy blog post of May 19, 2026 (https://www.entergy.com/blog/delta-blues-reaches-important-milestone-in-construction) says the heat recovery steam generator modules are being erected. POWER Magazine reported a groundbreaking on November 7, 2024 (https://www.powermag.com/entergy-mississippi-breaks-ground-on-754-mw-gas-fired-power-station/). So the unit is under construction. The EIA table for September 2026 still says regulatory approvals pending, which looks out of date. This is the same status GEM already shows. The unit is moving, so Latest Activity is left alone. I found no new owner, operator or turbine information beyond what GEM has. The air permit lists 773 MW and the EIA table lists 477 plus 341.7 MW, but Entergy's 754 MW stays as the headline figure.

### G100001030673 / Delta Blues Advanced Power Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 49 (Construction to operating checked)*
**Action:** Leave Start year of unit 1 (G100001030673) as 2028. It is still correct. Add the 2 links below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2028` -> `2028`
  - Start Year Data Source: https://www.entergymississippi.com/generation/deltablues (ok=True, contains_value=True)
  - Start Year Data Source: https://www.powermag.com/entergy-mississippi-breaks-ground-on-754-mw-gas-fired-power-station/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: Entergy Mississippi's project page (https://www.entergymississippi.com/generation/deltablues) says construction is expected to finish by 2028. The EIA table for September 2026 gives a planned operating date of May 2028. GEM's 2028 is right.

### G100001030673 / Delta Blues Advanced Power Station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked)*
**Action:** Add the entry below at the top of the Status Detail box of unit 1 (G100001030673), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Entergy said on May 19, 2026 that the heat recovery steam generator modules were being erected and the project was on track. Construction began with a groundbreaking on November 7, 2024. The EIA table for September 2026 still lists regulatory approvals pending, which appears out of date.

https://www.entergy.com/blog/delta-blues-reaches-important-milestone-in-construction
https://www.powermag.com/entergy-mississippi-breaks-ground-on-754-mw-gas-fired-power-station/
- `Status Detail`: `EIA 2024 lists power plant as L - regulatory approvals pending. Not under construction, but other sources state construction has begun (as of May 2025).` -> `Entergy said on May 19, 2026 that the heat recovery steam generator modules were being erected and the project was on track. Construction began with a groundbreaking on November 7, 2024. The EIA table for September 2026 still lists regulatory approvals pending, which appears out of date.

https://www.entergy.com/blog/delta-blues-reaches-important-milestone-in-construction
https://www.powermag.com/entergy-mississippi-breaks-ground-on-754-mw-gas-fired-power-station/

EIA 2024 lists power plant as L - regulatory approvals pending. Not under construction, but other sources state construction has begun (as of May 2025).`
  - Status Detail: https://www.entergy.com/blog/delta-blues-reaches-important-milestone-in-construction (ok=True, contains_value=False)
  - Status Detail: https://www.powermag.com/entergy-mississippi-breaks-ground-on-754-mw-gas-fired-power-station/ (ok=True, contains_value=False)
- confidence: high (independent: True)
- notes: New dated entry for the Status Detail box, from the Entergy blog post (https://www.entergy.com/blog/delta-blues-reaches-important-milestone-in-construction) and the POWER Magazine article (https://www.powermag.com/entergy-mississippi-breaks-ground-on-754-mw-gas-fired-power-station/).

### G100000402852 / Gerald Andrus power station / 1
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit 1 (G100000402852) to 2028. It now says 2035. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `2035` -> `2028`
  - Planned Retire Data Source: https://www.accessnewswire.com/newsroom/en/utilities/entergy-mississippi-breaks-ground-on-delta-blues-advanced-power-station-940135 (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: An Entergy Mississippi press release from November 7, 2024, at https://www.accessnewswire.com/newsroom/en/utilities/entergy-mississippi-breaks-ground-on-delta-blues-advanced-power-station-940135 says the Gerald Andrus Steam Electric Station will be retired when the new Delta Blues Advanced Power Station comes online in 2028. GEM shows 2035, and the EIA-860M table for September 2026 also still lists June 2035. The two dates conflict. The release is the owner's own statement and is newer than the EIA entry, but it is one source. I did not find the 2024 integrated resource plan itself or a Public Service Commission order stating the date.

### G100000402658 / Moselle power station / 3
*change to an existing unit; checklist rows 21 (Planned retirements searched), 23 (Planned retirement year not in the past), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 3 (G100000402658) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1801089 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx), released October 23, 2026, lists Cooperative Energy plant 2070, Moselle, with Generator 3 as status Operating, nameplate 59.0 MW, operating year 1970. It shows no planned retirement. The row was read in the downloaded file; the verifier only proves the file loads. The Mississippi Department of Environmental Quality Title V air permit modification issued August 14, 2025 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1801089) still lists the Unit No. 3 Boiler, 668 million Btu per hour, natural gas fired. Checked only whether the unit is still operating. No retirement, mothballing or ownership change was found in the EIA table or the permit. The planned retirement of 2025 no longer appears in the EIA table, so it was dropped by EIA without a retirement.

### G100001028154 / New Caledonia power station / 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked)*
**Action:** Add the entry below at the top of the Status Detail box of unit 1 (G100001028154), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643
- `Status Detail`: `Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.` -> `October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643

Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.`
  - Status Detail: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=True, contains_value=True)
  - Status Detail: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: A Commercial Dispatch article from October 23, 2025 and the Mississippi Department of Environmental Quality air construction permit 1680-00090 from May 12, 2025 both name the plant. They add the groundbreaking, active construction and the May 2028 completion goal to the existing log. Status stays construction. The groundbreaking was October 22, 2025 and work was well under way. Start year 2028 is confirmed by the same article. Latest Activity is left alone because the newest report is from October 2025, under a year old. Capacity differs by source: EIA lists 84 MW nameplate, the air permit lists 90 MW per turbine, GEM shows 83.3 MW.

### G100001028155 / New Caledonia power station / 2
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Add the entry below at the top of the Status Detail box of unit 2 (G100001028155), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643
- `Status Detail`: `Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.` -> `October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643

Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.`
  - Status Detail: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=True, contains_value=True)
  - Status Detail: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: A Commercial Dispatch article from October 23, 2025 and the Mississippi Department of Environmental Quality air construction permit 1680-00090 from May 12, 2025 both name the plant. They add the groundbreaking, active construction and the May 2028 completion goal to the existing log. Status stays construction. The groundbreaking was October 22, 2025 and work was well under way. Start year 2028 is confirmed by the same article. Latest Activity is left alone because the newest report is from October 2025, under a year old. Capacity differs by source: EIA lists 84 MW nameplate, the air permit lists 90 MW per turbine, GEM shows 83.3 MW.

### G100001028156 / New Caledonia power station / 3
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Add the entry below at the top of the Status Detail box of unit 3 (G100001028156), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643
- `Status Detail`: `Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.` -> `October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643

Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.`
  - Status Detail: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=True, contains_value=True)
  - Status Detail: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: A Commercial Dispatch article from October 23, 2025 and the Mississippi Department of Environmental Quality air construction permit 1680-00090 from May 12, 2025 both name the plant. They add the groundbreaking, active construction and the May 2028 completion goal to the existing log. Status stays construction. The groundbreaking was October 22, 2025 and work was well under way. Start year 2028 is confirmed by the same article. Latest Activity is left alone because the newest report is from October 2025, under a year old. Capacity differs by source: EIA lists 84 MW nameplate, the air permit lists 90 MW per turbine, GEM shows 83.3 MW.

### G100001028157 / New Caledonia power station / 4
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Add the entry below at the top of the Status Detail box of unit 4 (G100001028157), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643
- `Status Detail`: `Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.` -> `October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643

Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.`
  - Status Detail: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=True, contains_value=True)
  - Status Detail: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: A Commercial Dispatch article from October 23, 2025 and the Mississippi Department of Environmental Quality air construction permit 1680-00090 from May 12, 2025 both name the plant. They add the groundbreaking, active construction and the May 2028 completion goal to the existing log. Status stays construction. The groundbreaking was October 22, 2025 and work was well under way. Start year 2028 is confirmed by the same article. Latest Activity is left alone because the newest report is from October 2025, under a year old. Capacity differs by source: EIA lists 84 MW nameplate, the air permit lists 90 MW per turbine, GEM shows 83.3 MW.

### G100001028158 / New Caledonia power station / 5
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Add the entry below at the top of the Status Detail box of unit 5 (G100001028158), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643
- `Status Detail`: `Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.` -> `October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643

Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.`
  - Status Detail: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=True, contains_value=True)
  - Status Detail: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: A Commercial Dispatch article from October 23, 2025 and the Mississippi Department of Environmental Quality air construction permit 1680-00090 from May 12, 2025 both name the plant. They add the groundbreaking, active construction and the May 2028 completion goal to the existing log. Status stays construction. The groundbreaking was October 22, 2025 and work was well under way. Start year 2028 is confirmed by the same article. Latest Activity is left alone because the newest report is from October 2025, under a year old. Capacity differs by source: EIA lists 84 MW nameplate, the air permit lists 90 MW per turbine, GEM shows 83.3 MW.

### G100001028159 / New Caledonia power station / 6
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
**Action:** Add the entry below at the top of the Status Detail box of unit 6 (G100001028159), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643
- `Status Detail`: `Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.` -> `October 2025: A Commercial Dispatch article from October 23, 2025 reports that TVA held a groundbreaking for the New Caledonia plant on October 22, 2025, and that bulldozers and construction work were already under way. TVA says all six turbines should be finished in May 2028. The Mississippi Department of Environmental Quality issued the air construction permit on May 12, 2025.

https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643

Gregor, Nov 2024: This new plant would be built on the site of an earlier six-unit gas plant that TVA dismantled in 2007, directly adjacent to TVA's existing Lowndes County electrical substation, and about 3.5 miles west of TVA's Caledonia combined cycle power station. An environmental impact statement for the plant was published in July 2024 and public comments were still being submitted as of Sep 2024.`
  - Status Detail: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=True, contains_value=True)
  - Status Detail: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: A Commercial Dispatch article from October 23, 2025 and the Mississippi Department of Environmental Quality air construction permit 1680-00090 from May 12, 2025 both name the plant. They add the groundbreaking, active construction and the May 2028 completion goal to the existing log. Status stays construction. The groundbreaking was October 22, 2025 and work was well under way. Start year 2028 is confirmed by the same article. Latest Activity is left alone because the newest report is from October 2025, under a year old. Capacity differs by source: EIA lists 84 MW nameplate, the air permit lists 90 MW per turbine, GEM shows 83.3 MW.

### G100000401864 / TVA Southaven Combined Cycle power station / SCC3
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry)*
**Action:** Leave Owner(s) of unit SCC3 (G100000401864) as it is. Add the 1 link below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `Tennessee Valley Authority [90%]; Southaven Power LLC [10%]` -> `Tennessee Valley Authority [90%]; Southaven Power LLC [10%]`
  - Owners Data Source: https://web.archive.org/web/20220119113115/https://www.power-technology.com/uncategorised/newstva-receives-financing-for-southaven-combined-cycle-plant-in-mississippi/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The value is unchanged. The source box already holds a link to a page that is gone from its old address (https://www.power-technology.com/uncategorised/newstva-receives-financing-for-southaven-combined-cycle-plant-in-mississippi/). The Internet Archive kept a saved copy of that page, which was read and states the value. The saved copy is added to the box next to the old link.

### G100001074418 / Traceview Advanced power station / Unit 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 50 (Other last-minute status changes checked)*
**Action:** Set Status of unit Unit 1 (G100001074418) to pre-construction. It now says announced. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `announced` -> `pre-construction`
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274 (ok=True, contains_value=True)
  - Status Data Source: https://www.mdeq.ms.gov/wp-content/uploads/2026/10/Agenda-for-the-October-13-2026-PBM.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Mississippi Department of Environmental Quality issued an air construction permit for the Traceview Advanced Power Station on October 14, 2026, permit number 1720-00100 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274). The Permit Board agenda of October 13, 2026 lists the same permit (https://www.mdeq.ms.gov/wp-content/uploads/2026/10/Agenda-for-the-October-13-2026-PBM.pdf). A permit issued and land work under way fit pre-construction. The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists the plant as under construction, less than 50 percent complete. I did not find a source that says physical construction has begun, so I used one step below that. Only the state permit and the EIA table support a change, so this is a single-step call. Status moved from announced to pre-construction on the strength of the October 2026 air permit. I did not find the turbine make and model in the permit, the hearing notice or Entergy pages. Capacity is raised as a question because sources differ. Latest Activity is left alone because the project is moving.

### G100001074418 / Traceview Advanced power station / Unit 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Leave Start year of unit Unit 1 (G100001074418) as 2029. It is still correct. Add the 2 links below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2029` -> `2029`
  - Start Year Data Source: https://www.entergymississippi.com/generation/traceview (ok=True, contains_value=True)
  - Start Year Data Source: https://www.powermag.com/entergy-mississippi-adding-third-gas-fired-power-plant-to-superpower-strategy/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Entergy's Traceview project page (https://www.entergymississippi.com/generation/traceview) gives an expected in-service date in 2029, and a Power Magazine article from October 2025 (https://www.powermag.com/entergy-mississippi-adding-third-gas-fired-power-plant-to-superpower-strategy/) says the same. Entergy's own filing at the Mississippi Public Service Commission, docket 2026-UA-55 from July 2026, gives August 2029. The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) says 2028, so that source disagrees.

### G100001074418 / Traceview Advanced power station / Unit 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 17 (Unknown technology rechecked)*
**Action:** Leave Turbine/Engine Technology of unit Unit 1 (G100001074418) as combined cycle. It is still correct. Add the 2 links below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `combined cycle` -> `combined cycle`
  - Turbine/Engine Technology Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274 (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.mdeq.ms.gov/wp-content/uploads/2026/06/Notice-of-Public-Hearing.pdf (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The air construction permit (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274) describes a combustion turbine with duct burner, a heat recovery steam generator and a steam turbine. The public hearing notice from July 2026 (https://www.mdeq.ms.gov/wp-content/uploads/2026/06/Notice-of-Public-Hearing.pdf) calls it a 1x1 combined cycle plant.

### G100001074418 / Traceview Advanced power station / Unit 1
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
**Action:** Set Status Detail of unit Unit 1 (G100001074418) to the entry below. The box is empty now. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

The Mississippi Department of Environmental Quality issued the air construction permit on October 14, 2026, permit number 1720-00100. Entergy's filing in July 2026 at the Mississippi Public Service Commission, docket 2026-UA-55, gives August 2029 as the planned in-service date.

https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274
- `Status Detail`: `` -> `The Mississippi Department of Environmental Quality issued the air construction permit on October 14, 2026, permit number 1720-00100. Entergy's filing in July 2026 at the Mississippi Public Service Commission, docket 2026-UA-55, gives August 2029 as the planned in-service date.

https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274`
  - Status Detail: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The permit is in the state's enSearch record (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274). The docket entry comes from the harvest on the brief and is cited by number because the commission portal needs a session.

### G100001091020 / Vicksburg Advanced power station / 1A
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked)*
**Action:** Leave Status of unit 1A (G100001091020) as construction. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `construction` -> `construction`
  - Status Data Source: https://www.wlbt.com/2025/10/22/leaders-attend-new-vicksburg-advanced-power-station-groundbreaking-ceremony (ok=True, contains_value=True)
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: A WLBT article from October 22, 2025 (https://www.wlbt.com/2025/10/22/leaders-attend-new-vicksburg-advanced-power-station-groundbreaking-ceremony) reports the groundbreaking at the Baxter Wilson site. The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 69223 as under construction, less than 50 percent complete. Status stays construction. Status and start year re-verified. Latest Activity is left alone because the project is moving. I did not find a turbine model in the permit or Entergy pages, and GEM's existing model comes from a source already cited.

### G100001091020 / Vicksburg Advanced power station / 1A
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 49 (Construction to operating checked)*
**Action:** Leave Start year of unit 1A (G100001091020) as 2028. It is still correct. Add the 2 links below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2028` -> `2028`
  - Start Year Data Source: https://www.entergymississippi.com/generation/vicksburg (ok=True, contains_value=True)
  - Start Year Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: Entergy's Vicksburg project page (https://www.entergymississippi.com/generation/vicksburg) says construction is expected to be complete by August 2028. The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) plans August 2028. Entergy's filing in docket 2025-AD-123 says the same.

### G100001091020 / Vicksburg Advanced power station / 1A
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked)*
**Action:** Add the entry below at the top of the Status Detail box of unit 1A (G100001091020), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

Entergy Mississippi held a groundbreaking on October 21, 2025. The Mississippi Department of Environmental Quality issued the air construction permit 2780-00027 on November 3, 2025.

https://www.wlbt.com/2025/10/22/leaders-attend-new-vicksburg-advanced-power-station-groundbreaking-ceremony
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1845094
- `Status Detail`: `NF 1/12/26: Air permit was approved in Sept 2025. Entergy will consider hydrogen combustion when planning for operation of the facility to meet the NSPS TTTTa CO2 emission limit that becomes effective on January 1, 2032.` -> `Entergy Mississippi held a groundbreaking on October 21, 2025. The Mississippi Department of Environmental Quality issued the air construction permit 2780-00027 on November 3, 2025.

https://www.wlbt.com/2025/10/22/leaders-attend-new-vicksburg-advanced-power-station-groundbreaking-ceremony
https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1845094

NF 1/12/26: Air permit was approved in Sept 2025. Entergy will consider hydrogen combustion when planning for operation of the facility to meet the NSPS TTTTa CO2 emission limit that becomes effective on January 1, 2032.`
  - Status Detail: https://www.wlbt.com/2025/10/22/leaders-attend-new-vicksburg-advanced-power-station-groundbreaking-ceremony (ok=True, contains_value=True)
  - Status Detail: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1845094 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The WLBT article is dated October 22, 2025 and says the groundbreaking was held Tuesday, which was October 21 (https://www.wlbt.com/2025/10/22/leaders-attend-new-vicksburg-advanced-power-station-groundbreaking-ceremony). The permit's issue date is in the state's permit record (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1845094). The existing text says the permit was approved in September 2025, and the state record shows November 3, 2025.

### G100001091020 / Vicksburg Advanced power station / 1A
*change to an existing unit; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 17 (Unknown technology rechecked), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked)*
**Action:** Leave Turbine/Engine Technology of unit 1A (G100001091020) as combined cycle. It is still correct. Add the link below to the Turbine/Engine Technology Data Source box. Keep the links already there.
- `Turbine/Engine Technology`: `combined cycle` -> `combined cycle`
  - Turbine/Engine Technology Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1845094 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The air construction permit (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1845094) lists a gas turbine with duct burner, a heat recovery steam generator and a steam turbine generator as unit VAPS-1A.

### G100001055022 / Baxter Wilson power station / 2
*question about existing data; checklist rows 21 (Planned retirements searched)*
- about: Retired year
- recommendation: Amalia, please look at unit 2. GEM shows a retired year of 2018, which is before the 2020 floor for retired units. The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) agrees on the date: plant 2050, generator 2, retired, 783.0 MW, operating October 1971, retirement June 2018. So the sources back 2018, and the problem is only the tracker rule. A SuperTalk Mississippi article (https://www.supertalk.fm/entergy-demolishes-retired-vicksburg-power-plant-to-make-way-for-new-station/) calls the whole station retired and says it was demolished to make way for the new Vicksburg plant, but it gives no unit dates. I did not stage a change. Please decide whether to keep the unit as a link for the replacement or handle it another way.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://www.supertalk.fm/entergy-demolishes-retired-vicksburg-power-plant-to-make-way-for-new-station/ (ok=None, contains_value=None)
- notes: No change is proposed, as the brief asked.

### G100001070976 / Colossus 2 power station / 2
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 50 (Other last-minute status changes checked)*
- about: Status
- recommendation: A July 2026 Mississippi Today article quotes xAI saying it is constructing a 1.2 gigawatt power plant under its air permit, which could mean unit 2 has moved from pre-construction to construction. I found no dated report of site work, turbine delivery or installation, and the same article says supply problems are delaying the 41 turbines. I did not find a second independent publisher. Please decide after one more check for site work.
  - links: https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/ (ok=None, contains_value=None)
  - links: https://www.actionnews5.com/2026/07/31/xai-announces-fourth-data-center-turbines-be-removed-southaven-site/ (ok=None, contains_value=None)
- notes: Sources are the Mississippi Today article of July 31, 2026 (https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/) and the Action News 5 report of the same day (https://www.actionnews5.com/2026/07/31/xai-announces-fourth-data-center-turbines-be-removed-southaven-site/).

### G100001030673 / Delta Blues Advanced Power Station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 49 (Construction to operating checked)*
- about: Capacity (MW)
- recommendation: Different sources give different sizes. Entergy says 754 MW. The air permit lists a 773 MW heat input rating for the block. The EIA table for September 2026 lists generator 1A at 477 MW and generator 1C at 341.7 MW, which adds to 818.7 MW. I kept GEM's 754 MW because it is the company's own figure.
  - links: https://www.entergymississippi.com/generation/deltablues (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1779807 (ok=None, contains_value=None)
- notes: Sources are https://www.entergymississippi.com/generation/deltablues, the permit at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1779807 and the EIA table at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx.

### G100000402852 / Gerald Andrus power station / 1
*question about existing data; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
- about: Planned retire
- recommendation: Check Entergy Mississippi's 2024 integrated resource plan and the Delta Blues approval docket for the retirement date. If they confirm 2028, change the planned retirement year from 2035 to 2028.
  - links: https://www.accessnewswire.com/newsroom/en/utilities/entergy-mississippi-breaks-ground-on-delta-blues-advanced-power-station-940135 (ok=None, contains_value=None)
- notes: The Entergy press release at https://www.accessnewswire.com/newsroom/en/utilities/entergy-mississippi-breaks-ground-on-delta-blues-advanced-power-station-940135 says retirement comes when Delta Blues starts in 2028. The EIA table still says June 2035. The Public Service Commission docket 2024-UA-144 named in the brief gives a Delta Blues in-service date of May 2028, which supports the earlier date, but I could not read the filing itself because the portal needs a session.

### G100000402658 / Moselle power station / 3
*question about existing data; checklist rows 21 (Planned retirements searched), 23 (Planned retirement year not in the past), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
- about: Planned retire
- recommendation: Clear the planned retirement year of 2025 on unit 3. The EIA-860M table for September 2026 lists unit 3 as operating with no planned retirement, and a Mississippi air permit change from August 2025 still lists the unit 3 boiler. I found no Cooperative Energy or state document naming a new retirement date.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1801089 (ok=None, contains_value=None)
- notes: EIA table: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx. Air permit: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1801089. I did not find a Cooperative Energy announcement either way.

### G100001028154 / New Caledonia power station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
- about: Capacity (MW)
- recommendation: GEM shows 83.3 MW per unit. The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 69147 generators G1 to G6 at 84.0 MW nameplate each and 81.0 MW summer. The Mississippi air construction permit 1680-00090 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643) lists each GE 7E turbine at 90 MW. TVA says the plant adds about 500 MW. I suggest 84 MW per unit from EIA, but a reviewer should choose.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1783643 (ok=None, contains_value=None)
  - links: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=None, contains_value=None)
- notes: Three sources disagree slightly, so I did not change the value.

### G100001028154 / New Caledonia power station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked), 50 (Other last-minute status changes checked)*
- about: Status
- recommendation: The Environmental Integrity Project spreadsheet lists this plant as proposed. Its Oil and Gas Watch page for the plant now shows a 404 Not Found page in a real browser, and the Wayback Machine has no saved copy, so the label cannot be checked on the page. Construction is supported by the October 2025 groundbreaking article (https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/), so GEM's status of construction looks right.
  - links: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=None, contains_value=None)
- notes: EIP status looks out of date.

### G100001028154 / New Caledonia power station / 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 49 (Construction to operating checked)*
- about: Start year
- recommendation: EIA lists planned operation in December 2028. TVA says completion in May 2028 (https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/). GEM start year 2028 fits both.
  - links: https://cdispatch.com/news/800-million-tva-energy-plant-breaks-ground-outside-caledonia/ (ok=None, contains_value=None)
  - links: https://cdispatch.com/news/tva-energy-plant-to-be-up-and-running-in-caledonia-by-2028/ (ok=None, contains_value=None)
- notes: No change needed.

### G100000401969 / Quantum Choctaw Power station / CC1
*watch item at an existing plant*
- what to watch: TVA and TC Energy announced a carbon capture feasibility study at Ackerman in September 2023, but I found no later document showing a funded project, a decision or a cancellation.
- check again by: 2027-03
  - links: https://www.power-eng.com/gas/turbines/tva-to-study-carbon-capture-at-two-natural-gas-fired-plants/ (ok=None, contains_value=None)
- notes: A Power Engineering article from September 2023 (https://www.power-eng.com/gas/turbines/tva-to-study-carbon-capture-at-two-natural-gas-fired-plants/) says the two partners would invest 1.25 million dollars in a study of about one year. Searches of news and the TVA announcement trail found no results or follow-up. So the carbon capture box stays blank.

### G100001074418 / Traceview Advanced power station / Unit 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only))*
- about: Capacity (MW)
- recommendation: Decide which capacity to record. GEM has 760 MW. The EIA-860M table lists 819.4 MW nameplate (477.7 plus 341.7). Entergy's project page says 754 MW (https://www.entergymississippi.com/generation/traceview). The air permit lists 772,200 kW rated power (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274) and the hearing notice says about 750 MW net (https://www.mdeq.ms.gov/wp-content/uploads/2026/06/Notice-of-Public-Hearing.pdf).
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://www.entergymississippi.com/generation/traceview (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1877274 (ok=None, contains_value=None)
  - links: https://www.mdeq.ms.gov/wp-content/uploads/2026/06/Notice-of-Public-Hearing.pdf (ok=None, contains_value=None)
- notes: The figures probably measure different things. EIA gives nameplate, which is the GEM measure. I did not change the value because no source states a nameplate that matches the others.

### G100001074418 / Traceview Advanced power station / Unit 1
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 50 (Other last-minute status changes checked)*
- about: Status
- recommendation: Consider whether construction has started. The EIA table says under construction, but Entergy said site work would start in summer 2025 and construction in 2026 and I found no report that it began.
  - links: https://www.entergymississippi.com/generation/traceview (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: Entergy project page: https://www.entergymississippi.com/generation/traceview

### G100001091020 / Vicksburg Advanced power station / 1A
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked)*
- about: Capacity (MW)
- recommendation: Decide which capacity to record. GEM has 750 MW. The EIA-860M table for September 2026 lists 819.4 MW nameplate (generator GT1 477.7 plus ST1 341.7). Entergy says 754 MW (https://www.entergymississippi.com/generation/vicksburg), and the air permit lists 773,000 kW rated power (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1845094). The Sierra Club note about a capacity change most likely reflects the EIA figure.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://www.entergymississippi.com/generation/vicksburg (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1845094 (ok=None, contains_value=None)
- notes: The figures probably measure different things. EIA gives nameplate, which is the GEM measure. I did not change the value.

### G100001091020 / Vicksburg Advanced power station / 1A
*question about existing data; checklist rows 10 (Every unit in development updated, with a Last Updated entry), 37 (IRP box ticked on every IRP project (US only)), 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 49 (Construction to operating checked), 50 (Other last-minute status changes checked)*
- about: Status
- recommendation: The Energy Industry Partners Oil and Gas Watch page calls the plant proposed. That is out of date. The groundbreaking in October 2025 and the EIA-860M table both say construction.
  - links: https://www.wlbt.com/2025/10/22/leaders-attend-new-vicksburg-advanced-power-station-groundbreaking-ceremony (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: I did not open the Oil and Gas Watch page, so this answer rests on the groundbreaking report (https://www.wlbt.com/2025/10/22/leaders-attend-new-vicksburg-advanced-power-station-groundbreaking-ceremony) and the EIA table.

## Checklist group 4. Conversions

Coal-to-gas and other conversions: unit naming, fuel and technology, replacement links.

### G100001017948 / Jack Watson Generating Plant / Unit 4, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 4, timepoint 2 (G100001017948) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.mpbonline.org/blogs/news/mississippi-powers-conversion-of-plant-nearly-complete/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: An Associated Press article carried by Mississippi Public Broadcasting in 2015 (https://www.mpbonline.org/blogs/news/mississippi-powers-conversion-of-plant-nearly-complete/) says Mississippi Power would convert Plant Watson units 4 and 5 from coal to natural gas, with the work finished by April 16, 2015.

### G100001017947 / Jack Watson Generating Plant / Unit 5, timepoint 2
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit Unit 5, timepoint 2 (G100001017947) as conversion. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `conversion` -> `conversion`
  - Conversion/replacement Data Source: https://www.mpbonline.org/blogs/news/mississippi-powers-conversion-of-plant-nearly-complete/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: An Associated Press article carried by Mississippi Public Broadcasting in 2015 (https://www.mpbonline.org/blogs/news/mississippi-powers-conversion-of-plant-nearly-complete/) says Mississippi Power would convert Plant Watson units 4 and 5 from coal to natural gas, with the work finished by April 16, 2015.

### G100000409451 / Morrow Generating Plant / MOR1
*change to an existing unit; checklist rows 13 (Coal-to-gas conversions have gas fuel and technology)*
**Action:** Leave Conversion/replacement? of unit MOR1 (G100000409451) as replacement. It is still correct. Add the link below to the Conversion/replacement Data Source box. Keep the links already there.
- `Conversion/replacement?`: `replacement` -> `replacement`
  - Conversion/replacement Data Source: https://www.powermag.com/morrow-reinvented-hl-class-gas-turbine-powers-a-coal-plants-rebirth/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A POWER magazine article (https://www.powermag.com/morrow-reinvented-hl-class-gas-turbine-powers-a-coal-plants-rebirth/) says the cooperative board decided in June 2018 to retire the original two coal units and replace them with an advanced-class natural gas unit. That supports replacement as a new source for the Burns and McDonnell link that no longer shows the value. The Burns and McDonnell page now sits at https://www.burnsmcd.com/news/milestone-in-550-mw-heat-recovery-repower-project and describes the coal to gas conversion.

### G100001091020 / Vicksburg Advanced power station / 1A
*question about existing data; checklist rows 12 (Conversions carry "timepoint" in the unit name), 13 (Coal-to-gas conversions have gas fuel and technology)*
- about: conversion-link
- recommendation: The field for the unit being replaced holds this unit's own ID, G100001091020. It should point at the retired Baxter Wilson unit, probably unit 2 (retired 2018) or unit 1 (retired 2023, EIA plant 2050).
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: EIA retired list, plant 2050 Baxter Wilson: generator 1 retired March 2023 and generator 2 retired June 2018. Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx

## Checklist group 6. Owners and entities

Owner, operator and parent changes, and new owners or operators to create.

### G100000401848 / Attala power station / PB01
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit PB01 (G100000401848) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55220, Attala, generators A01, A02 and A03 (unit code PB01) as operating since March 2001, owned by Entergy Mississippi LLC, with no planned retirement. Nameplate is 176.6, 176.6 and 198.1 MW, which is 551.3 MW. Still operating, with no retirement, planned retirement, mothballing or owner change in the EIA table. A web search found no 2026 news of a retirement or sale.

### G100000401786 / Batesville generation facility / CC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC1 (G100000401786) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1757213 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (released October 23, 2026, https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55063, generators CTG1 and STG1, status operating, 184.5 MW plus 112.5 MW, operating August 2000, with no planned retirement date. A Mississippi Department of Environmental Quality Title V air permit renewed on December 27, 2024 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1757213) still lists three 185,000 kW natural gas turbines with heat recovery boilers. No retirement, mothballing or sale was found. The unit is still operating. I did not look at other fields, as the task was only the operating check.

### G100000401786 / Batesville generation facility / CC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of all 3 units of Batesville generation facility as Cooperative Energy [100%]. It is still correct. Add the link below to the Owners Data Source box on each unit. Keep the links already there.
- `Owner(s)`: `Cooperative Energy [100%]` -> `Cooperative Energy [100%]`
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) names Cooperative Energy as the entity for plant 55063. The air permit (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1757213) also names Cooperative Energy. No sale was found.

### G100000401787 / Batesville generation facility / CC2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC2 (G100000401787) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1757213 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (released October 23, 2026, https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55063, generators CTG2 and STG2, status operating, 184.5 MW plus 112.5 MW, operating August 2000, with no planned retirement date. A Mississippi Department of Environmental Quality Title V air permit renewed on December 27, 2024 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1757213) still lists three 185,000 kW natural gas turbines with heat recovery boilers. No retirement, mothballing or sale was found. The unit is still operating. I did not look at other fields, as the task was only the operating check.

### G100000401788 / Batesville generation facility / CC3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC3 (G100000401788) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1757213 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (released October 23, 2026, https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55063, generators CTG3 and STG3, status operating, 184.5 MW plus 112.5 MW, operating August 2000, with no planned retirement date. A Mississippi Department of Environmental Quality Title V air permit renewed on December 27, 2024 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1757213) still lists three 185,000 kW natural gas turbines with heat recovery boilers. No retirement, mothballing or sale was found. The unit is still operating. I did not look at other fields, as the task was only the operating check.

### G100000401837 / Caledonia power station / CCC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CCC1 (G100000401837) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026) lists Caledonia, plant 55197, unit code CCC1, as operating with CTG1 at 161.0 MW and STG1 at 106.0 MW, started in June 2003. No planned retirement date is listed. The table has no Caledonia entry among its retired or canceled sheets. Still operating in the EIA table for September 2026. I found no retirement, mothballing or planned retirement notice for this unit.

### G100000401838 / Caledonia power station / CCC2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CCC2 (G100000401838) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026) lists Caledonia, plant 55197, unit code CCC2, as operating with CTG2 at 161.0 MW and STG2 at 106.0 MW, started in June 2003. No planned retirement date is listed. The table has no Caledonia entry among its retired or canceled sheets. Still operating in the EIA table for September 2026. I found no retirement, mothballing or planned retirement notice for this unit.

### G100000401839 / Caledonia power station / CCC3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CCC3 (G100000401839) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (released October 23, 2026) lists Caledonia, plant 55197, unit code CCC3, as operating with CTG3 at 161.0 MW and STG3 at 106.0 MW, started in June 2003. No planned retirement date is listed. The table has no Caledonia entry among its retired or canceled sheets. Still operating in the EIA table for September 2026. I found no retirement, mothballing or planned retirement notice for this unit.

### G100000403187 / Chevron Oil power station / 5
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 5 (G100000403187) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists Chevron Oil, plant 2047, generator 5, as operating. It is a gas turbine of 101.3 MW that started in May 1994. No retirement date is listed. Still operating in the EIA table for September 2026. I found no retirement or mothballing notice.

### G100000401972 / Choctaw County power station / CC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC1 (G100000401972) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 lists Choctaw County, plant 55706, as operating. Three combustion turbines of 179.0 MW each and one steam turbine of 362.0 MW started in July 2003. No planned retirement date is listed. Still operating in the EIA table for September 2026. The Mississippi Department of Environmental Quality renewed the Title V air permit in February 2025. I found no retirement or mothballing notice. The Public Service Commission docket 2022-UA-153 in the brief concerns new Entergy Mississippi resources, not a change to this unit.

### G100001053819 / Colossus 2 power station / 1
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit 1 (G100001053819) to 2027. The box is empty now. Add the 2 links below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `` -> `2027`
  - Planned Retire Data Source: https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/ (ok=True, contains_value=True)
  - Planned Retire Data Source: https://www.actionnews5.com/2026/07/31/xai-announces-fourth-data-center-turbines-be-removed-southaven-site/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Mississippi Today article from July 31, 2026 (https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/) reports a state order dated July 30, 2026 that sets a schedule to retire all the temporary turbines at the Southaven site. Most must stop by April 2027, and the newest ones must stop by July 14, 2027. An Action News 5 report of the same day (https://www.actionnews5.com/2026/07/31/xai-announces-fourth-data-center-turbines-be-removed-southaven-site/) says all of them will be removed and replaced by a permanent plant. I did not read the state order itself.

### G100001053819 / Colossus 2 power station / 1
*change to an existing unit; checklist rows 19 (Missing or unknown owner searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Owner(s) of unit 1 (G100001053819) to MZX Tech LLC [100%]. It now says MZT Tech LLC [100%]. Add the 2 links below to the Owners Data Source box. Keep the links already there.
- `Owner(s)`: `MZT Tech LLC [100%]` -> `MZX Tech LLC [100%]`
  - Owners Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1834338 (ok=True, contains_value=True)
  - Owners Data Source: https://www.sec.gov/Archives/edgar/data/0001697500/000162828026054349/sei-20260630.htm (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The Mississippi air permit issued March 11, 2026 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1834338) names MZX Tech LLC as the permit holder. The Solaris Energy Infrastructure quarterly report for June 2026 (https://www.sec.gov/Archives/edgar/data/0001697500/000162828026054349/sei-20260630.htm) also spells it MZX Tech LLC. GEM's spelling MZT Tech LLC looks like a typing error. This is a spelling fix for the same company, not a change of owner.

### G100000402624 / Crossroads energy center / CT01
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CT01 (G100000402624) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1666455 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026, released October 23, 2026, at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists Crossroads Energy Center unit CT01 (plant 55395) as operating, with 76.6 MW nameplate, operating since July 2002. It shows no planned retirement. A Mississippi Department of Environmental Quality Title V air permit renewal issued August 24, 2023, at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1666455 still lists four 77 MW natural gas combustion turbines at the plant. The status is unchanged, so this is a re-check and not a status change. Still operating. No retirement, planned retirement, mothballing or owner change was found. The owner in the EIA table is still Clarksdale Public Utilities. No news search turned up any announcement.

### G100000402625 / Crossroads energy center / CT02
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CT02 (G100000402625) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1666455 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026, released October 23, 2026, at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists Crossroads Energy Center unit CT02 (plant 55395) as operating, with 76.6 MW nameplate, operating since July 2002. It shows no planned retirement. A Mississippi Department of Environmental Quality Title V air permit renewal issued August 24, 2023, at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1666455 still lists four 77 MW natural gas combustion turbines at the plant. The status is unchanged, so this is a re-check and not a status change. Still operating. No retirement, planned retirement, mothballing or owner change was found. The owner in the EIA table is still Clarksdale Public Utilities. No news search turned up any announcement.

### G100000402626 / Crossroads energy center / CT03
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CT03 (G100000402626) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1666455 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026, released October 23, 2026, at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists Crossroads Energy Center unit CT03 (plant 55395) as operating, with 76.6 MW nameplate, operating since July 2002. It shows no planned retirement. A Mississippi Department of Environmental Quality Title V air permit renewal issued August 24, 2023, at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1666455 still lists four 77 MW natural gas combustion turbines at the plant. The status is unchanged, so this is a re-check and not a status change. Still operating. No retirement, planned retirement, mothballing or owner change was found. The owner in the EIA table is still Clarksdale Public Utilities. No news search turned up any announcement.

### G100000402627 / Crossroads energy center / CT04
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CT04 (G100000402627) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1666455 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026, released October 23, 2026, at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists Crossroads Energy Center unit CT04 (plant 55395) as operating, with 76.6 MW nameplate, operating since July 2002. It shows no planned retirement. A Mississippi Department of Environmental Quality Title V air permit renewal issued August 24, 2023, at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1666455 still lists four 77 MW natural gas combustion turbines at the plant. The status is unchanged, so this is a re-check and not a status change. Still operating. No retirement, planned retirement, mothballing or owner change was found. The owner in the EIA table is still Clarksdale Public Utilities. No news search turned up any announcement.

### G100000402852 / Gerald Andrus power station / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100000402852) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1641654 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists Gerald Andrus generator 1 (plant 8054) as operating, 781.4 MW nameplate, operating since January 1975. A Mississippi Department of Environmental Quality Title V renewal issued April 26, 2023, at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1641654 lists the 7,275 million Btu per hour steam boiler. The status is unchanged. Still operating. The planned retirement looks like 2028, not 2035, because Entergy says the unit closes when the replacement plant starts. No retirement or owner change has happened yet.

### G100000401847 / Hinds energy facility / PB01
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit PB01 (G100000401847) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists Hinds Energy Facility, plant 55218, generators H01, H02 and H03 as operating, each with an operating year of 2001. It shows no planned retirement date. The Mississippi air permit renewal application of September 2026 also shows the plant is still active. I found no news of a retirement, mothballing or sale. The plant is still operating. The EIA table lists the three generators that make up this block (176.6, 176.6 and 198.1 MW, about 551 MW in all, matching GEM). No retirement, planned retirement, mothballing or owner change was found. The owner in the EIA table is Entergy Mississippi LLC, the same as GEM.

### G100001017948 / Jack Watson Generating Plant / Unit 4, timepoint 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 4, timepoint 2 (G100001017948) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists Jack Watson, plant 2049, generator 4 as operating. The unit now burns natural gas. Unit 4 is operating on natural gas. Southern Company's 2025 annual report shows a planned retirement by the end of 2028, which may be extended. The EIA start year of 1968 is the original coal unit, so GEM's 2015 start year for the gas unit stands. No document was found that states whether a carbon capture system is attached.

### G100001017948 / Jack Watson Generating Plant / Unit 4, timepoint 2
*change to an existing unit; checklist rows 21 (Planned retirements searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Set Planned retire of unit Unit 4, timepoint 2 (G100001017948) to 2028. The box is empty now. Add the link below to the Planned Retire Data Source box. Keep the links already there.
- `Planned retire`: `` -> `2028`
  - Planned Retire Data Source: https://www.sec.gov/Archives/edgar/data/92122/000009212226000006/so-20251231.htm (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Southern Company's annual report for 2025 (https://www.sec.gov/Archives/edgar/data/92122/000009212226000006/so-20251231.htm) says Mississippi Power's 2024 resource plan schedules Plant Watson Unit 4, 268 MW, to retire by the end of 2028. The same report says Mississippi Power told the state regulator in January 2025 that it may extend the retirement dates of some steam units beyond 2028 to serve new large loads. The date may therefore move.

### G100001017947 / Jack Watson Generating Plant / Unit 5, timepoint 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit Unit 5, timepoint 2 (G100001017947) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists Jack Watson, plant 2049, generator 5 as operating. The unit now burns natural gas. Unit 5 is operating on natural gas. No retirement date is scheduled. The EIA start year of 1973 is the original coal unit, so GEM's 2015 start year for the gas unit stands. No document was found that states whether a carbon capture system is attached.

### G100000403629 / Kemper County power station / GT1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit GT1 (G100000403629) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1808614 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 7960, generator GT1, status operating, nameplate 93.0 MW, operating July 2002, with no planned retirement date. The Mississippi Department of Environmental Quality renewed the plant's Title V air permit for four natural gas and diesel fired gas turbines in September 2025 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1808614). I found no retirement, mothballing or ownership change. Still operating. No retirement, planned retirement date, mothballing or owner change was found.

### G100000403630 / Kemper County power station / GT2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit GT2 (G100000403630) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1808614 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 7960, generator GT2, status operating, nameplate 93.0 MW, operating July 2002, with no planned retirement date. The Mississippi Department of Environmental Quality renewed the plant's Title V air permit for four natural gas and diesel fired gas turbines in September 2025 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1808614). I found no retirement, mothballing or ownership change. Still operating. No retirement, planned retirement date, mothballing or owner change was found.

### G100000403631 / Kemper County power station / GT3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit GT3 (G100000403631) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1808614 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 7960, generator GT3, status operating, nameplate 93.0 MW, operating July 2002, with no planned retirement date. The Mississippi Department of Environmental Quality renewed the plant's Title V air permit for four natural gas and diesel fired gas turbines in September 2025 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1808614). I found no retirement, mothballing or ownership change. Still operating. No retirement, planned retirement date, mothballing or owner change was found.

### G100000403632 / Kemper County power station / GT4
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit GT4 (G100000403632) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1808614 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 7960, generator GT4, status operating, nameplate 93.0 MW, operating July 2002, with no planned retirement date. The Mississippi Department of Environmental Quality renewed the plant's Title V air permit for four natural gas and diesel fired gas turbines in September 2025 (https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1808614). I found no retirement, mothballing or ownership change. Still operating. No retirement, planned retirement date, mothballing or owner change was found.

### G100000401924 / Magnolia power plant / MCC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit MCC1 (G100000401924) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.tva.com/energy/our-power-system/natural-gas/magnolia-combined-cycle-plant (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists generators CTG1 and STG1 as operating. The TVA plant page (https://www.tva.com/energy/our-power-system/natural-gas/magnolia-combined-cycle-plant) describes the plant as in service. I found no retirement, mothballing or planned retirement notice. Nothing has changed for this unit. The EIA table shows it operating with no planned retirement date, and I found no news of a retirement or sale.

### G100000401924 / Magnolia power plant / MCC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Owner(s) of all 3 units of Magnolia power plant as Tennessee Valley Authority [100%]. It is still correct. Add the 2 links below to the Owners Data Source box on each unit. Keep the links already there.
- `Owner(s)`: `Tennessee Valley Authority [100%]` -> `Tennessee Valley Authority [100%]`
  - Owners Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Owners Data Source: https://www.power-eng.com/gas/turbines/natural-gas-fired-power-plant-buy-completed-by-tva/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 lists Tennessee Valley Authority as the entity for plant 55451. A Power Engineering article (https://www.power-eng.com/gas/turbines/natural-gas-fired-power-plant-buy-completed-by-tva/) reports TVA completed the purchase of the plant from Kelson in 2011. No sale since then was found.

### G100000401925 / Magnolia power plant / MCC2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit MCC2 (G100000401925) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.tva.com/energy/our-power-system/natural-gas/magnolia-combined-cycle-plant (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists generators CTG2 and STG2 as operating. The TVA plant page (https://www.tva.com/energy/our-power-system/natural-gas/magnolia-combined-cycle-plant) describes the plant as in service. I found no retirement, mothballing or planned retirement notice. Nothing has changed for this unit. The EIA table shows it operating with no planned retirement date, and I found no news of a retirement or sale.

### G100000401926 / Magnolia power plant / MCC3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit MCC3 (G100000401926) as operating. It is still correct. Add the 2 links below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Status Data Source: https://www.tva.com/energy/our-power-system/natural-gas/magnolia-combined-cycle-plant (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists generators CTG3 and STG3 as operating. The TVA plant page (https://www.tva.com/energy/our-power-system/natural-gas/magnolia-combined-cycle-plant) describes the plant as in service. I found no retirement, mothballing or planned retirement notice. Nothing has changed for this unit. The EIA table shows it operating with no planned retirement date, and I found no news of a retirement or sale.

### G100000402659 / Moselle power station / 4
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4 (G100000402659) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx), released October 23, 2026, lists Cooperative Energy plant 2070, Moselle, with Generator 4 as status Operating, nameplate 83.0 MW, operating year 1997. It shows no planned retirement. The row was read in the downloaded file; the verifier only proves the file loads. Checked only whether the unit is still operating. No retirement, mothballing or ownership change was found in the EIA table or the permit.

### G100000402660 / Moselle power station / 5
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 5 (G100000402660) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx), released October 23, 2026, lists Cooperative Energy plant 2070, Moselle, with Generator 5 as status Operating, nameplate 83.5 MW, operating year 2006. It shows no planned retirement. The row was read in the downloaded file; the verifier only proves the file loads. Checked only whether the unit is still operating. No retirement, mothballing or ownership change was found in the EIA table or the permit.

### G100000401636 / Moselle power station / CC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC1 (G100000401636) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx), released October 23, 2026, lists Cooperative Energy plant 2070, Moselle, with Generator GTG1 and steam generator 1 as status Operating, nameplate 83.5 MW, operating year 2012. It shows no planned retirement. The row was read in the downloaded file; the verifier only proves the file loads. Checked only whether the unit is still operating. No retirement, mothballing or ownership change was found in the EIA table or the permit.

### G100000401637 / Moselle power station / CC2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC2 (G100000401637) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=False)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx), released October 23, 2026, lists Cooperative Energy plant 2070, Moselle, with Generator GTG2 and steam generator 2 as status Operating, nameplate 83.5 MW, operating year 2012. It shows no planned retirement. The row was read in the downloaded file; the verifier only proves the file loads. Checked only whether the unit is still operating. No retirement, mothballing or ownership change was found in the EIA table or the permit.

### G100000401969 / Quantum Choctaw Power station / CC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit CC1 (G100000401969) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists this unit as operating. The table lists plant 55694 with two gas turbines of 270.0 MW each and one steam turbine of 310.5 MW. Together that is 850.5 MW, a little under the 851.0 MW GEM shows. Start year 2006 is unchanged. No planned retirement date is listed. I found no retirement, mothballing or sale in the sources I checked. The unit is still operating. The only change is a 0.5 MW difference in total capacity.

### G100000402041 / Ratcliffe power plant / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100000402041) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists this unit as operating. The table lists plant 57037 with two gas turbines of 235.5 MW each and one steam turbine of 369.0 MW. Together that is 840.0 MW, which matches GEM. Start year 2014 is unchanged. No planned retirement date is listed. I found no retirement, mothballing or sale in the sources I checked. The unit is still operating and every checked value matches GEM. The Public Service Commission dockets from 2023 and 2024 are routine equipment notices, not retirement filings.

### G100000402661 / Silver Creek power station / 1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100000402661) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists this unit as operating. The table lists plant 7988, generator 1, nameplate 83.5 MW, operating year 2003. GEM shows 84.0 MW. No planned retirement date is listed. I found no retirement, mothballing or sale in the sources I checked. The unit is still operating. The nameplate is 83.5 MW, half a megawatt under GEM.

### G100000402662 / Silver Creek power station / 2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 2 (G100000402662) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists this unit as operating. The table lists plant 7988, generator 2, nameplate 83.5 MW, operating year 2004. GEM shows 84.0 MW. No planned retirement date is listed. I found no retirement, mothballing or sale in the sources I checked. The unit is still operating. The nameplate is 83.5 MW, half a megawatt under GEM.

### G100000402663 / Silver Creek power station / 3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 3 (G100000402663) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists this unit as operating. The table lists plant 7988, generator 3, nameplate 83.5 MW, operating year 2005. GEM shows 84.0 MW. No planned retirement date is listed. I found no retirement, mothballing or sale in the sources I checked. The unit is still operating. The nameplate is 83.5 MW, half a megawatt under GEM.

### G100000401862 / TVA Southaven Combined Cycle power station / SCC1
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit SCC1 (G100000401862) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55269, generators CTG1 and STG1, as operating, with an operating year of 2003. The table shows no planned retirement. I found no retirement, mothballing or ownership change announcement for this unit. Still operating according to the September 2026 EIA table. Nothing else was researched, as the brief asked.

### G100000401863 / TVA Southaven Combined Cycle power station / SCC2
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit SCC2 (G100000401863) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55269, generators CTG2 and STG2, as operating, with an operating year of 2003. The table shows no planned retirement. I found no retirement, mothballing or ownership change announcement for this unit. Still operating according to the September 2026 EIA table. Nothing else was researched, as the brief asked.

### G100000401864 / TVA Southaven Combined Cycle power station / SCC3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit SCC3 (G100000401864) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 55269, generators CTG3 and STG3, as operating, with an operating year of 2003. The table shows no planned retirement. I found no retirement, mothballing or ownership change announcement for this unit. Still operating according to the September 2026 EIA table. Nothing else was researched, as the brief asked.

### G100000402099 / Victor J Daniel Jr power station / 3
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 3 (G100000402099) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 6073, generators 3, 3CT and 3ST, as operating, with an operating year of 2001 and no planned retirement. I found no retirement, mothballing or ownership change announcement for this unit. Still operating according to the September 2026 EIA table. Nothing else was researched, as the brief asked.

### G100000402100 / Victor J Daniel Jr power station / 4
*change to an existing unit; checklist rows 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 4 (G100000402100) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists plant 6073, generators 4, 4CT and 4ST, as operating, with an operating year of 2001 and no planned retirement. I found no retirement, mothballing or ownership change announcement for this unit. Still operating according to the September 2026 EIA table. Nothing else was researched, as the brief asked.

### Caledonia power station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Tennessee Valley Authority (operator); lookup: The lookup says the entity already exists on 192 units in the United States. Reuse the existing entity.

### Caledonia power station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: GE Energy Financial Services Inc (owner); lookup: The lookup says the entity already exists on 7 units in Chile and the United States. Reuse the existing entity.

### G100000401837 / Caledonia power station / CCC1
*question about existing data; checklist rows 19 (Missing or unknown owner searched), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
- about: Owner(s)
- recommendation: TVA does not own this plant. It leases it. GEM's owner, GE Energy Financial Services Inc, may still be the lessor, but I found no dated document that names the lessor today. Please keep the current owner unless the lessor is confirmed, and consider recording TVA as the operator.
  - links: https://tva.com/energy/our-power-system/natural-gas/caledonia-combined-cycle-plant (ok=None, contains_value=None)
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: A Tennessee Valley Authority page on the Caledonia Combined Cycle Plant at https://tva.com/energy/our-power-system/natural-gas/caledonia-combined-cycle-plant says the plant was built by Cogentrix from 2002 to 2003, began commercial operation on May 30, 2003, and that TVA leased the facility starting in December 2007. The Mississippi Department of Environmental Quality air permit lists the facility name as TVA Caledonia Combined Cycle Plant. The EIA-860M table for September 2026 lists the Tennessee Valley Authority as the entity for the plant, which reflects the lessee. I did not find a sale to TVA, and I did not find a document that names the lessor after 2007.

### Colossus 2 power station
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: MZX Tech LLC (owner); lookup: Bare lookup and Postgres lookup found no entity named MZX Tech LLC. An entity named MZT Tech LLC exists on 2 US units, which is the same company spelled differently, so the existing record should be corrected rather than a new one made.

### G100001070976 / Colossus 2 power station / 2
*question about existing data; checklist rows 19 (Missing or unknown owner searched)*
- about: attribution
- recommendation: The Solaris Energy Infrastructure quarterly report for June 2026 says Solaris holds 50.1 percent of Stateline Power LLC and MZX Tech LLC holds the other 49.9 percent. Stateline was formed in April 2025 to provide off-grid power under a long-term equipment lease to MZX Tech LLC, and it borrowed money to buy the equipment. So the leased generating equipment may be owned by Stateline, not by MZX Tech LLC. The filing does not say which turbines, how many megawatts, or whether they sit at Southaven or in Memphis. I did not change the owner. The May 2026 row on the possible-updates sheet about a change of ownership is answered this way: I found no closed sale of the plant, only this lease structure.
  - links: https://www.sec.gov/Archives/edgar/data/0001697500/000162828026054349/sei-20260630.htm (ok=None, contains_value=None)
- notes: Source is https://www.sec.gov/Archives/edgar/data/0001697500/000162828026054349/sei-20260630.htm. I could not open the ESG Dive story named on the sheet, and a search did not find it. The NAACP lawsuit of April 2026 covers the temporary turbines, per https://www.actionnews5.com/2026/04/14/naacp-sues-xai-alleging-unlawful-operation-gas-turbines-southaven/.

### Jack Watson Generating Plant
*new owner or operator to create; checklist rows 19 (Missing or unknown owner searched)*
- entity: Mississippi Power Co (owner); lookup: Name unchanged from GEM, no new entity needed.

## Checklist group 7. IDs, IRPs and data centers

United States only: EIA and other IDs, utility resource plans, gas-fired data centers.

### G100000403187 / Chevron Oil power station / 5
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Set Captive industry use of unit 5 (G100000403187) to both. The box is empty now. Add the link below to the Captive Data Source box. Keep the links already there.
- `Captive industry use`: `` -> `both`
  - Captive Data Source: https://www.sec.gov/Archives/edgar/data/92122/000009212225000018/so-20241231.htm (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Southern Company annual report for 2024 at https://www.sec.gov/Archives/edgar/data/92122/000009212225000018/so-20241231.htm says Mississippi Power provides retail service to the Chevron refinery in Pascagoula through at least 2038. It says Mississippi Power owns co-generation assets at the refinery, and that the contract refers to steam output at that facility. It does not name the 101 MW turbine alone, so the match to this unit is implied.

### G100000403187 / Chevron Oil power station / 5
*change to an existing unit; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only))*
**Action:** Set Captive industry type of unit 5 (G100000403187) to petroleum refining. The box is empty now. Add the link below to the Captive Data Source box. Keep the links already there.
- `Captive industry type`: `` -> `petroleum refining`
  - Captive Data Source: https://www.sec.gov/Archives/edgar/data/92122/000009212225000018/so-20241231.htm (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The Southern Company annual report for 2024 at https://www.sec.gov/Archives/edgar/data/92122/000009212225000018/so-20241231.htm says Mississippi Power provides retail service to the Chevron refinery in Pascagoula through at least 2038. It says Mississippi Power owns co-generation assets at the refinery, and that the contract refers to steam output at that facility. It does not name the 101 MW turbine alone, so the match to this unit is implied.

### G100001053819 / Colossus 2 power station / 1
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit 1 (G100001053819) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: A Mississippi Today article from July 31, 2026 says xAI has run trailer-mounted gas turbines at the Southaven site since August 2025 and still runs them, under a schedule to retire them by July 2027. The unit is still operating. This is the same status GEM already shows. Unit 1 is still running. The state order of July 30, 2026 covers 69 temporary turbines, but GEM's 495 MW counts about 27, so the capacity may be out of date. I did not find a source that gives the megawatts for all 69. The Environmental Integrity Project's Oil and Gas Watch page for the xAI Southaven Power Plant (https://oilandgaswatch.org/facility/rec_d5nrijecevv1v46o78d0, read in a real browser) lists one project, the initial construction, as proposed, a simple cycle gas plant of 1,240 MW for the data center, expected in 2026. That describes the permanent plant, which is unit 2 in GEM, not the temporary turbines of unit 1.

### G100001053819 / Colossus 2 power station / 1
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Add the entry below at the top of the Status Detail box of unit 1 (G100001053819), above the text already there. Keep the existing text below it, word for word. The source links are part of the entry, one per line. Do not add them to the Status Data Source box.

On July 30, 2026 the Mississippi Department of Environmental Quality set a schedule to retire all 69 temporary turbines at the Southaven site. Most must stop by April 2027 and the last by July 14, 2027. xAI says a permanent power plant is replacing them.

https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/
- `Status Detail`: `JM: temporary turbines include (operating, 18 units, 354 MW total):
7 x 13MW - Solar Turbines SMT130 
6x 25MW - GE Vernova TM2500
4 x 22MW - GE Vernova TM2500
1 x 25MW - M35

PLUS additional units (19-27, not operating until outfitted with pollution control equipment, 141 MW total):
2 x 25MW GE TM2500
7 x 13MW Solar Turbines SMT130

TOTAL = 495 MW temporary turbines

NF 10/30/25: A former Duke's Energy gas plant was purchased in New Haven, MS.
NF 7/11/25: Capacity will be up to 2 GW. The plant will be shipped from overseas because of U.S. delays.` -> `On July 30, 2026 the Mississippi Department of Environmental Quality set a schedule to retire all 69 temporary turbines at the Southaven site. Most must stop by April 2027 and the last by July 14, 2027. xAI says a permanent power plant is replacing them.

https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/

JM: temporary turbines include (operating, 18 units, 354 MW total):
7 x 13MW - Solar Turbines SMT130 
6x 25MW - GE Vernova TM2500
4 x 22MW - GE Vernova TM2500
1 x 25MW - M35

PLUS additional units (19-27, not operating until outfitted with pollution control equipment, 141 MW total):
2 x 25MW GE TM2500
7 x 13MW Solar Turbines SMT130

TOTAL = 495 MW temporary turbines

NF 10/30/25: A former Duke's Energy gas plant was purchased in New Haven, MS.
NF 7/11/25: Capacity will be up to 2 GW. The plant will be shipped from overseas because of U.S. delays.`
  - Status Detail: https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/ (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: New dated entry for the Status Detail box, from the Mississippi Today article of July 31, 2026 (https://mississippitoday.org/2026/07/31/southaven-xai-turbines-deadline/).

### G100001017948 / Jack Watson Generating Plant / Unit 4, timepoint 2
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Leave Start year of unit Unit 4, timepoint 2 (G100001017948) as 2015. It is still correct. Add the 2 links below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2015` -> `2015`
  - Start Year Data Source: https://www.mpbonline.org/blogs/news/mississippi-powers-conversion-of-plant-nearly-complete/ (ok=True, contains_value=True)
  - Start Year Data Source: https://web.archive.org/web/20211202115238/https://www.transmissionhub.com/articles/2015/02/mississippi-powers-watson-coal-to-gas-conversion-almost-completed.html (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The same 2015 article says the conversion to natural gas should be complete by April 16, 2015. So the start year of the gas unit is 2015. The EIA-860M table for September 2026 gives 1968 for unit 4 and 1973 for unit 5. Those are the years the original coal units began operating, so GEM's 2015 for the converted gas unit is right. A saved copy of the Transmission Hub article of February 27, 2015, which is already a source in GEM, says the same: Plant Watson would burn natural gas only by April 16, 2015. The live address now opens the TD World home page, so the saved copy is cited.

### G100001017947 / Jack Watson Generating Plant / Unit 5, timepoint 2
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
**Action:** Leave Start year of unit Unit 5, timepoint 2 (G100001017947) as 2015. It is still correct. Add the 2 links below to the Start Year Data Source box. Keep the links already there.
- `Start year`: `2015` -> `2015`
  - Start Year Data Source: https://www.mpbonline.org/blogs/news/mississippi-powers-conversion-of-plant-nearly-complete/ (ok=True, contains_value=True)
  - Start Year Data Source: https://web.archive.org/web/20211202115238/https://www.transmissionhub.com/articles/2015/02/mississippi-powers-watson-coal-to-gas-conversion-almost-completed.html (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: The same 2015 article says the conversion to natural gas should be complete by April 16, 2015. So the start year of the gas unit is 2015. The EIA-860M table for September 2026 gives 1968 for unit 4 and 1973 for unit 5. Those are the years the original coal units began operating, so GEM's 2015 for the converted gas unit is right. A saved copy of the Transmission Hub article of February 27, 2015, which is already a source in GEM, says the same: Plant Watson would burn natural gas only by April 16, 2015. The live address now opens the TD World home page, so the saved copy is cited.

### G100000409451 / Morrow Generating Plant / MOR1
*change to an existing unit; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only)), 43 (Ownership changes for operating units reviewed (optional)), 50 (Other last-minute status changes checked)*
**Action:** Leave Status of unit MOR1 (G100000409451) as operating. It is still correct. Add the link below to the Status Data Source box. Keep the links already there.
- `Status`: `operating` -> `operating`
  - Status Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists generators MOR1 and MOR2 at plant 6061 as operating since March 2023. No retirement, mothballing or sale was found. The unit is still operating. EIA lists it as two generators of 156.0 MW and 402.0 MW, which total 558 MW as GEM shows. See the question about the Sierra Club 156 MW flag.

### G100000409451 / Morrow Generating Plant / MOR1
*question about existing data; checklist rows 38 (GEM IDs matched to EIA-860M, EIP and Sierra Club (US only))*
- about: Capacity (MW)
- recommendation: No change. The Sierra Club 156 MW flag appears to come from the first generator row alone.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
  - links: https://www.power-eng.com/gas/572-mw-morrow-plant-completes-coal-to-natural-gas-conversion-in-mississippi/ (ok=None, contains_value=None)
- notes: The EIA-860M table for September 2026 (https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx) lists Morrow as two generators: MOR1 at 156.0 MW and MOR2 at 402.0 MW, 558 MW together, which is the capacity GEM holds for the combined cycle block. Cooperative Energy and trade press (https://www.power-eng.com/gas/572-mw-morrow-plant-completes-coal-to-natural-gas-conversion-in-mississippi/) quote 572 MW as the plant rating, which is a different basis. I found no public source of an actual capacity change.

## Checklist group 8. New to the tracker

New plants and units ready to add, candidates to watch, and the possible-updates rows.

### Enterprise Clarke County power station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create the plant in Clarke County, Mississippi, then add the unit below. Leave owner, technology and coordinates blank until a filing names them.
- `State/Province`: `` -> `Mississippi`
- `Local area (taluk, county)`: `` -> `Clarke`
- unit 1 `Capacity (MW)`: `785`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2032`
  - Location Data Source: https://www.interconnection.fyi/project/southern-company-26-ic-1425 (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: The Southern Company generator interconnection queue, read through its Power BI report at https://www.southerncompany.info/power-bi/transmission-policy-services/index.html, lists request 26-IC-1425 in Clarke County, Mississippi. It is a combined cycle gas project of 785 MW (991 MVA) connecting at the Enterprise substation 230 kV bus. The request was received on 3/26/2026, its status is Active, it is in the cluster study, and the requested in-service date is 5/1/2032. The queue note reads: "Affiliate request. Scoping Meeting scheduled for May 14, 2026." That means a Southern Company affiliate filed it, most likely Mississippi Power, but no filing says which one. The Power BI report needs a script to load, so the verifier cannot read it. The same row is copied at https://www.interconnection.fyi/project/southern-company-26-ic-1425, which passed the verifier and is cited here. Because that copy is a lead site, every value stays at medium confidence until a Mississippi Power or Public Service Commission filing names the project. Mississippi Power's 2024 resource plan at https://www.synapse-energy.com/mississippi-power-company-2024-integrated-resource-plan names no new gas plant. The plant is named after its substation and county because the request has no other name. Not found: the owner, the plant name, the turbine model, the exact site and the coordinates.

### Sykes Clarke County power station
*new plant; checklist rows 51 (Newly announced projects checked)*
**Action:** Create the plant in Clarke County, Mississippi, then add the two units below. Leave owner, technology and coordinates blank until a filing names them.
- `State/Province`: `` -> `Mississippi`
- `Local area (taluk, county)`: `` -> `Clarke`
- unit 1 `Capacity (MW)`: `199.4`
- unit 1 `Fuel`: `fossil gas: natural gas`
- unit 1 `Status`: `announced`
- unit 1 `Start year`: `2029`
- unit 2 `Capacity (MW)`: `199.4`
- unit 2 `Fuel`: `fossil gas: natural gas`
- unit 2 `Status`: `announced`
- unit 2 `Start year`: `2029`
  - Location Data Source: https://www.interconnection.fyi/project/southern-company-26-ic-1489 (ok=True, contains_value=True)
- confidence: medium (independent: )
- notes: The Southern Company generator interconnection queue, read through its Power BI report at https://www.southerncompany.info/power-bi/transmission-policy-services/index.html, lists two requests in Clarke County, Mississippi, both received on 4/3/2026: 26-IC-1489 and 26-IC-1490. Each is a gas combustion turbine of 199.4 MW (369.1 MVA) connecting on the Laurel East to Sykes substation 230 kV line, with a requested in-service date of 5/1/2029. Both are Active and in the cluster study. The queue gives no owner or plant name. The Power BI report needs a script to load, so the verifier cannot read it. The same rows are copied at https://www.interconnection.fyi/project/southern-company-26-ic-1489 and https://www.interconnection.fyi/project/southern-company-26-ic-1490, which passed the verifier and are cited here. Because those copies are a lead site, every value stays at medium confidence until a utility or Public Service Commission filing names the project. The two requests share a line and dates, so they are treated as one plant with two units. The plant is named after the substation and county. Not found: the owner, the plant name, the turbine model, the exact site and the coordinates. Moselle power station in Jones County is the nearest GEM gas plant. It is a different plant.

### Victor J Daniel Jr power station / 2 (gas conversion)
*new unit at an existing plant; checklist rows 51 (Newly announced projects checked)*
- `Unit name`: `` -> `2 (gas conversion)`
- `Capacity (MW)`: `` -> `548.3`
- `Fuel`: `` -> `fossil gas: natural gas`
- `Status`: `` -> `pre-construction`
- `Turbine/Engine Technology`: `` -> `steam turbine`
- `Conversion/replacement?`: `` -> `conversion`
  - Status Data Source: https://www.psc.ms.gov/sites/default/files/2026-02/3-2026-CONSENT-DOCKET.pdf (ok=True, contains_value=True)
  - Status Data Source: https://www.psc.ms.gov/sites/default/files/2026-07/7-7-26-Agenda.pdf (ok=True, contains_value=True)
  - Capacity Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Fuel Data Source: https://www.psc.ms.gov/sites/default/files/2026-02/3-2026-CONSENT-DOCKET.pdf (ok=True, contains_value=True)
  - Unit name Data Source: https://www.psc.ms.gov/sites/default/files/2026-02/3-2026-CONSENT-DOCKET.pdf (ok=True, contains_value=True)
  - Turbine/Engine Technology Data Source: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=True, contains_value=True)
  - Conversion/replacement Data Source: https://www.psc.ms.gov/sites/default/files/2026-02/3-2026-CONSENT-DOCKET.pdf (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: Mississippi Power asked the Mississippi Public Service Commission in docket 2026-UA-5, filed 12 February 2026, for a certificate to convert coal Unit 2 at Plant Daniel to natural gas. The February 2026 consent docket (https://www.psc.ms.gov/sites/default/files/2026-02/3-2026-CONSENT-DOCKET.pdf) and the commission agenda for 7 July 2026 (https://www.psc.ms.gov/sites/default/files/2026-07/7-7-26-Agenda.pdf) both list this petition. The agenda shows a proposed order was up for action, but I did not find the final order. A supplemental petition filed in June 2026 says the company now wants to convert one of the two coal units, Unit 1 or Unit 2, and will name the unit later. The company's testimony says the conversion work would finish in May 2029 and gas operation would begin in June 2029. I left the start year blank because the filings sit in the commission portal, which needs a session, and I could not verify a link for them. The capacity of 548.3 MW is the EIA nameplate for coal Unit 2 in the September 2026 EIA-860M table. The company's testimony gives 502 MW. The owner is not stated in these filings, so I left it blank. Units 1 and 2 are listed in the EIA table with a planned retirement in December 2027, which the petition suggests may change. The EIA-860M table for September 2026, Operating sheet, has this row: plant 6073, Victor J Daniel Jr, generator 2, nameplate 548.3 MW, technology Conventional Steam Coal, prime mover ST, energy source SUB, status (OP) Operating, planned retirement year 2027. The prime mover ST is the steam turbine the gas unit would keep.

### G100000403187 / Chevron Oil power station / 5
*question about existing data*
- about: scope
- recommendation: The EIA table lists five turbines at this plant, units 1 to 5, for 170.5 MW. GEM holds only unit 5. Units 1 to 4 are each 16.6 to 18.0 MW and started in 1967 and 1971, so they are under the 50 MW threshold individually, but please decide whether they belong with unit 5 as one plant.
  - links: https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx (ok=None, contains_value=None)
- notes: The EIA-860M table for September 2026 at https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx lists generators 1 to 4 at plant 2047 as operating gas turbines.

### Entergy Mississippi unnamed MISO requests 2030 and 2031
*watch item, new to the tracker; checklist rows 39 (Gas-powered data centers searched, captive data entered (US only)), 51 (Newly announced projects checked)*
- what to watch: Four large MISO requests on Entergy Mississippi's system have no fuel or plant named in the public queue. Entergy's chief executive has said two new plants will be needed in the early 2030s.
- check again by: 2027-04
  - links: https://mississippitoday.org/2025/09/17/entergy-mississippi-ceo-fisackerly-answers-questions-on-data-centers-and-electricity-rates/ (ok=True, contains_value=True)
- notes: The MISO generator interconnection queue, read through MISO's public queue data at https://www.misoenergy.org/planning/resource-utilization/GI_Queue/gi-interactive-queue/, lists requests J4286 and J4295 of 770 MW each with in-service dates of 5/31/2030, and J4245 of 770 MW with an in-service date of 7/31/2031, in Mississippi on Entergy's system. J4176 of 1,750 MW is withdrawn. The queue hides the fuel for these requests and no filing I found names them. In a September 2025 interview at https://mississippitoday.org/2025/09/17/entergy-mississippi-ceo-fisackerly-answers-questions-on-data-centers-and-electricity-rates/ Entergy Mississippi's chief executive said the company would need two new power plants in the early 2030s to serve data center growth. A 770 MW size matches a single combined cycle block, but that is a guess, so nothing is added. Not found: the fuel, the owner, the site and any filing for these requests.

### New Caledonia power station
*question about existing data*
- about: identity
- recommendation: No change. TVA interconnection request 569 is this plant. The reviewer may want to compare the 2028 start year with the queue's September 2026 in-service date.
  - links: https://www.oasis.oati.com/woa/docs/TVA/TVAdocs/OASIS_CurrentQueue_20260914.pdf (ok=True, contains_value=True)
  - links: https://tva.com/environment/environmental-stewardship/environmental-reviews/nepa-detail/new-caledonia-gas-plant (ok=True, contains_value=True)
- notes: The TVA generator interconnection queue posted on September 14, 2026 at https://www.oasis.oati.com/woa/docs/TVA/TVAdocs/OASIS_CurrentQueue_20260914.pdf lists request 569: gas, 515 MW, at the Lowndes 161 kV substation in Lowndes County, Mississippi, received 6/20/2023, in the facilities study, with an in-service date of 9/1/2026. TVA's environmental review page at https://tva.com/environment/environmental-stewardship/environmental-reviews/nepa-detail/new-caledonia-gas-plant describes the New Caledonia gas plant at the former gas plant site in Lowndes County, about 500 MW from six dual-fuel frame combustion turbines. GEM holds six units of 83.3 MW, which add to about 500 MW. The queue entry and the plant match by site, fuel and size, so no new plant is needed. The TVA archive queue lists request 575, also 515 MW at Lowndes, as withdrawn. It looks like a duplicate request. Caledonia power station (L100000401627) is the 2003 combined cycle plant on a neighboring site and is a different plant.

### Sylvarena generating plant
*watch item, new to the tracker; checklist rows 51 (Newly announced projects checked)*
- what to watch: Three 47 MW gas combustion turbines owned by Cooperative Energy in Smith County. Each turbine is under 50 MW. If they are aeroderivative turbines they count as one set of 141 MW and the plant is an add.
- check again by: 2027-04
  - links: https://www.eia.gov/electricity/data/eia860m/ (ok=None, contains_value=None)
  - links: https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1875726 (ok=True, contains_value=True)
- notes: EIA's monthly generator file at https://www.eia.gov/electricity/data/eia860m/ lists Sylvarena, EIA plant 7989, as three 47 MW natural gas combustion turbines from 2003, 141 MW in all, owned by Cooperative Energy. The state air permit renewal issued October 7, 2026 at https://opcgis.deq.state.ms.us/ensearchonline/get_doc.aspx?dt=finalp&id=1875726 covers three simple cycle combustion turbines of 417.7 million Btu per hour each, with water injection to control nitrogen oxides. It says new combustors were to be installed in 2026, a like-for-like replacement with no capacity change stated. The site is 3012 Smith County Road 97, Raleigh, at latitude 31.982076 and longitude -89.412714. No source I found names the turbine model. Water injection on a 47 MW gas turbine is typical of an aeroderivative model such as the LM6000. If a source confirms that, the three turbines are one set of 141 MW and the plant should be added at operating. Not found: the turbine maker or model.

## Checklist group Other

### G100001030673 / Delta Blues Advanced Power Station / 1
*question about existing data*
- about: other
- recommendation: The Entergy Mississippi 2024 integrated resource plan link on the sheet points to a public workshop notice, not the plan. The notice does not mention Delta Blues, so no finding comes from the plan and none is marked as coming from it. The PSC docket 2024-UA-144 filing of December 12, 2024 gives a planned in service date of May 2028, which agrees with GEM's 2028. I could not open the docket through the portal.
- notes: Notice checked: https://www.psc.ms.gov/sites/default/files/2023-07/EML-2024-IRP-Notice-Initial-Public-Workshop.pdf.

## Checklist group 9. Close-out

Not record-level: the sheet and doc updates, research status, and the two database checks. These boxes are ticked by hand after the edits are applied: validation_report.py --closeout must print CLOSE-OUT CLEAN (row 54) and no_tracker.py lists the units with no tracker (row 56).
