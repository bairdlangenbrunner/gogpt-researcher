# United States — Iowa

Scope: 47 unit rows across 30 plants in the pull of 2026-10-16 (10 announced, 8 pre-construction, 26 operating, 2 cancelled, 1 retired). Assigned to Amalia Llano for the Q4 2026 cycle. Two utility rows on the US IRPs tab (Interstate Power and Light and MidAmerican Energy). No captive LNG sheet rows for the state. First run as a state research pass in update mode on 2026-10-16, with every plant briefed. The assignments tab's counts (10 units in development, 3,533 MW, 2 cancelled or shelved, 0 operating without a start year) match the pull once the eight IRP placeholder plants (3,458.5 MW) are left out. The last edits before this cycle were Dan O'Beirne's in July 2026 (Fairfax, Morgan Valley, Orient, Riverhawk).

## State context

- Two grid operators. The Midcontinent Independent System Operator (MISO) covers most of the state. The Southwest Power Pool (SPP) also serves Iowa customers, mostly in the west (an Iowa Utilities Commission briefing deck says "Two RTOs in the Iowa footprint: MISO and SPP"). Which counties sit in SPP was not confirmed.
- The regulator is the Iowa Utilities Commission. It was the Iowa Utilities Board until July 1, 2024, so older documents use that name. Filings are on its electronic filing system at efs.iowa.gov. Docket numbers are a type, a year and a number. A generating certificate case is GCU (for example GCU-2026-0002, Morgan Valley); a ratemaking case is RPU.
- A new plant of 25 MW or more at one site needs a generating certificate from the commission (Iowa Code 476A.1). A certificate approval is a good pre-construction marker.
- The two big utilities do not file integrated resource plans. They file Resource Evaluation Studies instead. MidAmerican Energy filed one on November 1, 2024, under a settlement in docket RPU-2025-0001. The commission is writing guidelines for these studies in docket NOI-2025-0002; final guidelines and the filing cycle were not found. A 2025 bill to require integrated resource plans every five years appears not to have passed.
- Air construction permits come from the Iowa Department of Natural Resources Air Quality Bureau. Every facility has its own permit page at https://idnraqrr.iowadnr.gov/ConPermitSearch/ConstructionPermit?id=N, listing each permit with its number, project number, equipment and issue date, and a download link to the permit PDF. The Burlington Generating Station page is id 1499; it lists the five engine permits issued March 12, 2026. The full facility directory, with every id, plant name, city and plant number, comes from ConPermitSearch/ByConstructionPermitPlantNameView?searchString=a. Large projects also have a page at ConPermitSearch/PSDSearch?id=N with the application, engineering evaluation and final permit. Open public comment periods, about 30 days long, are at ConPermitSearch/PublicComment, each with a detail page at PublicComment?id=N. Applications still under review are listed at programs.iowadnr.gov/easyair/Public/Client/IA_EASY/Public/Pages/PublicApplicationList.aspx. Each application's submitted forms open as PDFs on the EasyAir report viewer by a plain request, and they are the best early source: equipment, manufacturer, model, nameplate MW and the date installation begins, months before a permit is issued. A pre-application can point at a draft application, which is worth reading too. Linn County (Cedar Rapids) and Polk County (Des Moines) run their own air permit programs, so plants there get county permits. A new plant can be filed under an older facility's id: Bobcat's turbines are under Marshalltown Generating Station, facility 1462. `harvest_permits_iowa.py` reads all of this ahead of a sweep; the hosts are in `docs/reference/site_access.md`.
- Interstate Power and Light is the Alliant Energy utility in Iowa. It owns the Alliant plants, so the immediate owner is Interstate Power and Light Co and Alliant Energy Corp is the parent. Alliant's quarterly reports to the Securities and Exchange Commission list project dates and docket timing.
- Many new gas plants are being proposed for data center load. A June 2026 Des Moines Register opinion piece said Alliant and MidAmerican had 3,845 MW of gas plants pending at the commission.

## Recent events 2024 to 2026

- Orient Energy Center (MidAmerican, Adair County, two combustion turbines, about 465 MW): listed in MidAmerican's February 2025 generation plan for 2028. The certificate application was reported in August 2025, with local news citing up to 520 MW. MidAmerican told the county supervisors in September 2026 that construction began in April 2026. The state issued air permits for units 1 and 2 on April 30, 2026, and for a third turbine (permit 26-A-246) on June 11, 2026. MidAmerican's fact sheet now says three turbines and up to 700 MW, with unit 3 in spring 2029.
- Bobcat Energy Center (Interstate Power and Light, Marshall County, 720 MW of combustion turbines next to Marshalltown Generating Station): certificate approved December 16, 2025. Alliant said on August 11, 2026 that the air permit had arrived and construction had started. Service is planned for 2029.
- Cedar River Generating Station (five gas engines, 94 MW, at the Prairie Creek site in Cedar Rapids): commission approval in June (the article implies 2025), a Linn County air permit hearing on January 28, 2026, service expected by June 2027. Prairie Creek stopped burning coal on December 31, 2025.
- Burlington Generating Station: five gas engines totaling 94 MW were approved February 16, 2026, to replace combustion turbines more than 30 years old. Service is planned for 2029.
- Fairfax and Morgan Valley (Linn County): Alliant said in October 2025 that it was deprioritizing the Fairfax site after objections from Eastern Iowa Airport leaders. It then proposed the Morgan Valley Energy Center, three 240 MW simple-cycle turbines about 2.5 miles northwest of Fairfax, filed April 29, 2026 in docket GCU-2026-0002. Rezoning was filed with Linn County on July 15, 2026. Alliant's June 2026 quarterly report expects the commission's decision in the first quarter of 2027.
- Riverhawk Energy Center (Interstate Power and Light, next to Emery Station, Cerro Gordo County): about 1,200 MW of simple-cycle gas filed in July 2026. A decision is expected in the second quarter of 2027, with service targeted for 2031.
- Hickory Grove Generating Station (Central Iowa Power Cooperative, 240 MW of simple-cycle gas near Maysville, Scott County): the county supervisors voted 4 to 0 against the zoning change on February 12, 2026. The cooperative still lists the project, targeted for late 2029. Reports that it took the project to the commission were not confirmed.
- Ames Municipal Energy Center (City of Ames): three Wärtsilä dual fuel engines of 18.13 MW each, about 54 MW, bought on July 28, 2026, for the coal yard of the Ames Municipal Power Plant. Delivery October 2029, running about 2030; the site has room for three more engines. Unit 7 then moves to standby, and the city hopes to run Unit 8 until 2040. An Ames Tribune story gives 108 MW for the new engines; the city and two other local outlets give 54 MW. No air permit application was on file in October 2026.
- Streeter Station (Cedar Falls Utilities): a September 2026 air permit application asks to drop coal from unit 6, which already burns gas.
- Hickory Grove applied for its air permit in January 2026 (one Siemens SGT6-5000F that can also burn fuel oil). Morgan Valley applied in July 2026 (three Siemens turbines of 240 MW, installation from June 2027). Riverhawk sent a pre-application in July 2026 for GE Vernova 7F.05 turbines.
- No Iowa gas plant retirement announcement was found for 2024 to 2026.

## Watch items to raise with the reviewer

- Three possible new plants sit at the 50 MW threshold. Coralville gas turbines (EIA plant 1079, four 18 MW units, 72 MW in total) and River Hills (EIA plant 1084, eight 16 MW units, 128 MW in total) are above 50 MW only as a group. Roquette America in Keokuk (EIA plant 57953) has a 40 MW gas turbine and a 10 MW heat recovery steam generator, exactly 50 MW as one combined cycle block. Whether to add them is a threshold call for the reviewer.
- A Council Bluffs data center campus of 1 GW on 306 acres, reported to run partly on on-site gas, is on the possible-updates sheet marked "monitor next update". No source confirming the gas plant was found.
- Cleanview's October 2026 list shows 15 planned Iowa gas projects (2,742 MW), many named after substations, such as Killdeer at 787 MW in Cerro Gordo County. Treat them as leads only.

## Still open after the 2026-10-16 run

- Threshold calls for the reviewer: Coralville (72 MW from four 18 MW turbines), River Hills (128 MW from eight 16 MW turbines), Roquette America (exactly 50 MW as a combined cycle block, 84.4 MW with the petroleum coke steam turbine), and Streeter Station, which GEM tracks as coal only while the EIA table shows 51.5 MW of operating gas steam turbines.
- New units under 50 MW were added at tracked plants from the EIA-860M August 2026 table (Summit Lake GT1 and GT2, Burlington GT1 to GT4, Ames GT1). Whether small units at tracked plants should be added is a reviewer call.
- Seven Midcontinent Independent System Operator queue entries are on the watch list (J4113 Killdeer 787.4 MW, J4114 Haskins 525 MW, J4145 Emery 98 MW, J2945 Hills 350 MW, and three 160 MW engine entries). Whether Killdeer is the same capacity as Riverhawk was not settled.
- Interstate Power and Light 2024 IRP power station 1 (a 430 MW combined cycle) could not be tied to any named project. "Alliant IA RES CC 2" at 1,720 MW was not found in any primary source.
- MidAmerican IRP power station 7 carries a staged Latest Activity date and IRP power stations 1 to 6 do not. That should be made consistent.
- Hickory Grove: the reported commission docket GCU-2026-0001 was not confirmed.
- Burlington unit 2 start year, 2021 or 2022, is open. A dead Gazette link has a live replacement at thegazette.com/environment-nature/why-power-plants-are-using-natural-gas-instead-of-coal.
- Wisdom unit 2 is Basin 50% and Corn Belt 50% in GEM, but Corn Belt's own page does not mention Basin.
- Lime Creek is one 90.2 MW unit in GEM and two 45.1 MW units in the EIA table. Exira is 61.0 MW in GEM and 60.5 MW in the EIA table.
- Orient: the fact sheet says 520 MW and the plan puts the second turbine in 2029. The recommendation is to keep both units at 2028 until a dated source says otherwise.
- Muscatine has a planned 35 MW gas turbine, below the threshold.
- Prairie Creek's unit name "Unit 4- timepoint 2" should read "Unit 4, timepoint 2".
- Not reached in the October 2026 batch: the Iowa Utilities Commission electronic filing system. The air permit pages were wrongly skipped in the first run as a "search form" and the March 2026 Burlington engine permits were missed. The follow-on of 2026-10-19 harvested every plant's state and county permits and applications and staged what they showed.

## Follow-on of 2026-10-19

- Ames Municipal Power Plant gets a new unit, Phase 1: three engines of 18.13 MW, pre-construction, 2030. Whether it should instead be a separate plant named Ames Municipal Energy Center is a reviewer call; the city uses that name for the whole site.
- Orient gets a new unit 3 of 232.5 MW, worked out from the fact sheet's 700 MW total. It may be the same capacity as MidAmerican 2024 IRP power station 1 (232.5 MW in 2031); a question asks the reviewer.
- Equipment from the air permit applications: Siemens SGT6-5000F at Bobcat unit 3 and Hickory Grove, GE Vernova 7F.05 at Riverhawk.
- Fuel oil as a second fuel at Hickory Grove and Orient is a question, not an edit.
- Polk County has three draft permits out for comment at Pleasant Hill (limit changes only, no new unit).

## Gotchas

- Coal-to-gas conversions are separate units named "<name>, timepoint 2", with the coal unit as timepoint 1. Several Iowa conversions carry the coal unit's start year or have blank conversion fields (Ames unit 7, Earl F. Wisdom unit 1), and Prairie Creek's name uses a dash ("Unit 4- timepoint 2").
- IRP placeholder plants (Interstate Power and Light 2024 IRP power station 1, MidAmerican 2024 IRP power stations 1 to 7) hold unsited capacity from the Resource Evaluation Studies. When a named project appears, check whether it is the same capacity before keeping both.
- Fairfax is cancelled and Morgan Valley is its replacement at a nearby site. Do not move Fairfax's units into Morgan Valley.
- Cedar River Generating Station sits inside the Prairie Creek site, and its coordinates are copied from Prairie Creek. Its owner should be Interstate Power and Light Co like the other Alliant plants.
- Burlington's new engines are unit 2 of the existing Burlington plant, not a new plant. Riverhawk is unit RH of Emery Station.
