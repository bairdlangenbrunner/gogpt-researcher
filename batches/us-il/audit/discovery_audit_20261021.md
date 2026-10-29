# Illinois discovery audit, 2026-10-21

Question asked: the Illinois research pass of 2026-10-09 found no new power plants and only a few suggested new units. Was every source for new gas and oil plants in the Illinois pipeline checked? This memo answers that question. It is an audit, not a batch. Nothing here has been staged, and the live database was not touched.

## Short answer

No, the original pass did not check every source, and it said so in its own log. It read the EIA-860M planned, operating and canceled sheets, the PJM deactivation page and the current Illinois EPA air permit notices, and it searched the news. It did not download the PJM queue, did not search the MISO queue, did not open the Illinois Commerce Commission e-Docket, and did not read the Illinois EPA permit archive. It also never followed up six EIA plants that the ID matching step listed as absent from GEM. The pass ran before the 2026-10-19 rule that every portal and document a person could reach must be worked.

Those gaps have now been closed, with one exception noted below. The new checks found no gas or oil plant of 50 MW or more that is built, under construction or permitted in Illinois and missing from GEM. They did find four large gas interconnection requests filed with PJM in April 2026 that are not in GEM or on the watch list, a set of corrections to the two pipeline plants GEM already holds, and three existing plants in the EIA list that GEM does not hold. Details follow.

## What the original pass covered and skipped

The statewide search in the 2026-10-09 batch (batches/us-il/shards/_state.json) verified 19 of 20 URLs and staged no new plants, 12 new units (the Fisk and Waukegan oil peakers from EIA-860M) and 4 watch items. Its log says the MISO queue was not searched in detail and the PJM queue file was not downloaded. The Illinois country note repeats this: "Not searched: the MISO interconnection queue, the Illinois Commerce Commission e-Docket and the PJM queue file." Illinois has no air permit harvester, unlike Iowa and Kansas. The ID matching file (work/ids_us-illinois.json) listed six EIA plants with no GEM match (UIUC Cogen 54044, Ingredion 54556, UIUC Abbott 54780, Tilton 7760, Alsey 7818, Moline 899) and no one looked at them.

## Sources worked in this audit

1. PJM cycle queue, the live 2026 list. The static PJM transition file is stale (Cycle TC1 only, 310 rows, last updated 2024), so the audit pulled the full export from the PJM cycle service request status page (https://www.pjm.com/planning/m/cycle-service-request-status). The export holds 1,792 requests across Cycle TC1, TC2 and C01, filed 11 January 2021 to 28 April 2026. Illinois has 239 rows, 117 of them in Cycle C01. The file is saved at work/pjm/pjm_cycle_queue_2026-10-21.xlsx.
2. PJM serial queue, the fresh PlanningQueues.xml (9,263 rows) at https://www.pjm.com/pjmfiles/media/planning/queues-data/PlanningQueues.xml, saved at work/pjm/pjm_serial_queue_2026-10-21.xml. The older copy under pub/planning/downloads/xml has stale statuses and should not be used.
3. MISO queue through the MISO API and the ERAS spreadsheet (90 rows, sheet dated 24 October 2026), plus interconnection.fyi as a lead finder only. Report: batches/us-il/audit/queue_followup_20261021.md.
4. Illinois EPA air permit notices, current and archive, through the notice web service the Bureau of Air page calls (https://webapps.illinois.gov/EPA/WebSiteApi/api/PublicNotices/). 22 current and 2,163 archived notices were read, and 146 construction, PSD, nonattainment new source review and Title V construction records for power, data center and utility industry codes were examined. The RBLC permit database was queried through its new API. Report: batches/us-il/audit/permit_sweep_20261021.md.
5. EIA-860M for August 2026, planned, operating and canceled sheets, re-read for Illinois.
6. News, owner filings and local coverage, about 55 searches, with Vistra, Constellation and Springfield CWLP documents read. Report: batches/us-il/audit/news_sweep_20261021.md.

## Illinois gas pipeline as of 2026-10-21

### Plants GEM already holds

| Plant | GEM record | What the audit found |
|---|---|---|
| Broadwing Energy Center, Decatur | L100000407695, 400 MW, pre-construction | Illinois EPA issued the final construction permit and PSD approval on 14 October 2026 (https://webapps.illinois.gov/EPA/WebSiteApi/api/PublicNotices/GetAirPermitDocument/10625). The permit describes one combustion turbine with a duct burner, 452 MW gross at ISO conditions, serving the ADM east Decatur complex with the rest sold into MISO. No final investment decision has been reported. MISO queue entry J1839 (325 MW, Decatur ADM North 138 kV) is very likely this plant. Capacity and permit date should be updated. |
| Lincoln Land Energy Center, Pawnee | L100000402416, 2 x 638 MW, pre-construction | The construction permit was first issued 29 July 2022 and extended twice. The second extension, issued 21 July 2025, requires construction to start by 21 January 2027 (https://webapps.illinois.gov/EPA/WebSiteApi/api/PublicNotices/GetAirPermitDocument/9857, a scanned document read by OCR). The 2021 project summary calls the plant about 1,100 MW nominal. EmberClear is again the developer after Kindle Energy. The Eagle Rock data center that was to be the offtaker was abandoned on 12 August 2026 (Illinois Times). MISO entry J955 (1,040 MW, Austin 345 kV, Sangamon) is very likely this plant; its MISO label "Under Construction" is a queue step, not evidence of building. |
| Nelson energy center, Lee County | L100000402024 | The watch item for a "391 MW Nelson queue lead" is wrong in substance. PJM request AH1-718 (Invenergy Nelson Expansion LLC, 391 MW facility output) is an 11 MW energy and 38 MW capacity uprate, and C01-1171 (Invenergy Nelson LLC, 675 MW facility output) is a 66 MW energy and 6 MW capacity uprate. Neither is a new unit. The old AB1-089 request (575 MW, Byron to Wayne) was withdrawn on 9 June 2025 and should be dropped as a lead. |
| Zion energy center, Lake County | operating, 597 MW | A revised permit issued 28 July 2026 allows distillate oil in the three turbines during grid emergencies (https://webapps.illinois.gov/EPA/WebSiteApi/api/PublicNotices/GetAirPermitDocument/10511). A fuel note only. |

### Gas requests in the 2026 PJM cycle queue that GEM does not hold

| Request | Developer | County and point of interconnection | MW | Filed, requested in service | Status |
|---|---|---|---|---|---|
| C01-1569 | Will County Facility, LLC | Will, Braidwood 345 kV switchyard | 346 | 25 April 2026, 31 December 2029 | Active, Phase 1 |
| C01-1570 | Ogle County Hub, LLC | Ogle, Byron 345 kV switchyard | 347 | 25 April 2026, 31 December 2029 | Active, Phase 1 |
| C01-1571 | Prairie Pulse Project, LLC | LaSalle, LaSalle 345 kV switchyard | 346 | 25 April 2026, 31 December 2029 | Active, Phase 1 |
| C01-2036 | Marquis Solar LLC | Putnam, Crescent Ridge to Corbin 138 kV | 1,150, natural gas | 27 April 2026, 30 June 2031 | Active, Phase 1 |

The three 346 MW requests look like one program: same size, same filing day, same in-service date, each at a Constellation nuclear plant switchyard. Web searches for the three LLC names found nothing. C01-2036 is labeled natural gas in PJM's own file despite the developer name; the Marquis industrial complex at Hennepin is a plausible site, but no announcement, permit or site plan was found. The Illinois EDC site listing shows only 70 to 82 MW of existing electric service there (https://www.illinoisedc.org/vetted-site/marquis-industrial-complex/). All four belong on the watch list with a recheck date, not in GEM as plant records, until a permit, a site or a named owner appears. The next cheap step is the Illinois Secretary of State business search for the three LLCs, which was not done.

### Other queue entries checked and ruled out

PJM requests AH1-567 (University Park, 5 MW), AH1-563 (Aurora, 150 MW gas and storage hybrid) and AH1-564 (Rockford II, 150 MW hybrid) were all withdrawn on 30 September 2026. AH1-700 (664 MW, Lee County) was withdrawn 14 April 2025. AE1-070 (Elwood uprate) was withdrawn 22 January 2025. AD2-194 (Jackson Generation) is the original 2018 request for a plant that has been operating since 2022. AC1-142A (Joliet 7 and 8) is deactivated and AD1-039 (Three Rivers) is in service. The MISO ERAS list has no Illinois gas or oil project; the Illinois ERAS entries are all solar. MISO entry J2656 (180 MW, Macon County, Latham 138 kV, filed September 2022) has a blank fuel and could not be identified. About 21 Ameren-area MISO requests from the 2026 cycle have blank fuel (largest J4343 at 500 MW, then J4260, J4344, J4254 and J4301 at 240 to 300 MW); MISO left fuel blank for 193 of 283 requests in that cycle, so most are probably solar or storage, but they remain unclassified.

### Permit record

No construction permit for a new gas or oil generator of 20 MW or more appears in the Illinois EPA notice archive for 2021 to 2026 other than Broadwing, Lincoln Land and the Zion revision. The RBLC database lists Lincoln Land (29 July 2022) as the only Illinois turbine permit since 2020. Data center permits for Compass (Hoffman Estates), Aligned (Elk Grove Village and Northlake) and CyrusOne (Aurora) cover diesel emergency generators only. The Cronus Chemicals ammonia plant at Tuscola has an 8 MW waste-heat steam turbine.

### News and owners

No new Illinois gas or oil plant of 50 MW or more turned up in the news that is not in GEM or on the watch list. Vistra names no Illinois gas repowering for Baldwin, Kincaid or Newton. Constellation plans to run Zion past 2030. Springfield CWLP's February 2026 letter shows no new gas unit. Two thin items remain: the MicroLink Stickney data center is described as having a "behind-the-meter gas bridge" with no size (source page returns 404), and an undated Springfield report of a gas-only generator ordinance could not be recovered from any archive.

## Existing plants in the EIA list that GEM does not hold

These are not pipeline plants, but the audit surfaced them and they need a decision.

| EIA plant | County | Capacity | Note |
|---|---|---|---|
| Tilton Energy Center, 7760 | Vermilion | 188 MW, four 47 MW gas turbines, 1999 | Each unit is under the 50 MW line, but GEM already holds 65 US gas and oil units between 45 and 49.9 MW, so this is a threshold call for Baird. |
| Alsey, 7818 | Scott | 173 MW, units of 30, 30, 20, 20, 25 and 48 MW, newest 2016 | Same threshold call. |
| MPH Elwood, 69979 | Will | 384 MW, out of service per EIA | Very likely the retired Elwood units GT1 to GT4 under a new EIA ID. An ID check, not a new plant. |
| Moline, 899 | Rock Island | 72 MW, four 18 MW units | Under threshold. |
| UIUC Abbott 54780 (80 MW), UIC cogen 54044 (60 MW), Ingredion 54556 (55 MW), ExxonMobil Joliet 50627 (43 MW) | various | captive and campus plants | Unit sizes are under 50 MW. Listed so the leads file is closed out. |

## Coverage gaps that remain

1. Illinois EPA permits issued without a public notice (minor construction permits) are not in the notice archive. Closing this needs a records request or the Document Explorer, which cannot list by permit type.
2. The scanned Broadwing and Lincoln Land permits were read by OCR on the first pages only, and about 20 data center and industrial notices were judged by title and industry code without opening them.
3. The Illinois Commerce Commission e-Docket was not opened. Gas plants in Illinois do not need a certificate from the commission, so the relevance is low.
4. PJM Cycle 1 study reports are not yet posted, so the four C01 requests have no site or developer detail beyond the queue row.
5. The MISO blank-fuel 2026 requests above are unclassified.
6. The Illinois Secretary of State search for the three 346 MW LLCs has not been run.

## Recommended follow-ups, for Baird to approve

1. Stage an addendum to the Illinois batch: Broadwing capacity 452 MW gross and the 14 October 2026 final permit; Lincoln Land permit extensions, the 21 January 2027 construction deadline, the EmberClear return and the lost offtaker; the Nelson watch item corrected to an uprate; the Zion oil backup note; four new watch items for C01-1569, C01-1570, C01-1571 and C01-2036 with a recheck date after PJM posts the Cycle 1 Phase 1 reports.
2. Decide on Tilton and Alsey (add or leave out) and on the MPH Elwood ID check.
3. Update the Illinois country note: replace the "Not searched" line with what was searched in this audit and the gaps above.
4. Write an Illinois permit harvester from the notice web service, in the same shape as the Iowa and Kansas scripts, so the next Illinois pass reads the archive by script.
5. Add the PJM cycle queue export and the fresh PlanningQueues.xml to the Update SOP's statewide search step for every PJM state, since the static transition file is two years stale.

Appendices: the three agent reports are in this folder (permit_sweep_20261021.md, news_sweep_20261021.md, queue_followup_20261021.md). The queue report's note that C01-2036 is a mislabel is superseded: the fresh PJM export confirms natural gas.
