# Illinois interconnection queue follow-up

Scope: gas or oil plants of 50 MW or more in Illinois, chased from the parsed PJM XML and MISO API files to primary documents. Downloads are in `scratchpad/queue_followup/`. GEM match column refers to `scratchpad/il_gem_plants.txt`. "fyi" means interconnection.fyi, which is a lead only, never a citation.

## Task 1. PJM newer processes (RRI, Transition Cycles, Cycle 1)

| Queue ID | Site / POI | Developer | Fuel | MW | Status and date | URL that states it (opened and read) | GEM match |
|---|---|---|---|---|---|---|---|
| AH1-718 | Nelson 345 kV, Lee County, ComEd | Invenergy Nelson Expansion LLC | Natural gas | 391 MW total facility; 11 MW energy and 38 MW capacity uprate | Selected in the Reliability Resource Initiative, May 2025. Moved to Transition Cycle 2. Phase 1 report issued. Requested in service 2028. | https://www.pjm.com/pjmfiles/pub/planning/project-queues/TC2/PHASE_1/AH1-718/AH1-718_imp_PHASE_1.htm and https://www.pjm.com/-/media/DotCom/committees-groups/committees/pc/2025/20250506/20250506-rri-addendum---post-meeting.pdf | Yes, an uprate at the existing Nelson energy center (1008 MW, operating). Not a new plant. |
| AH1-567 | University Park 138 kV, Will County, ComEd | University Park Energy, LLC | Natural gas | 328 MW facility; 5 MW energy and 5 MW capacity | Transition Cycle 2 Phase 1 report, study year 2028 | https://www.pjm.com/pjmfiles/pub/planning/project-queues/TC2/PHASE_1/AH1-567/AH1-567_imp_PHASE_1.htm | Probably University Park South (354 MW) or North (732 MW). The 5 MW increment points to an add or uprate at the existing site. The report does not say "uprate", so this is not confirmed. |
| AE1-070 | Elwood 345 kV, ComEd | Elwood Energy, LLC | Natural gas | 1610 MW facility; 135 MW capacity | Transition Cycle 1 Phase 1 | https://www.pjm.com/pjmfiles/pub/planning/project-queues/TC1/PHASE_1/AE1-070/AE1-070_imp_PHASE_1.htm | Yes, Elwood Energy power station (1728 MW). The report says "an uprate to the existing Elwood Energy Units". |
| AH1-700 | Lee County, ComEd | Not named | Natural gas | 664 MW facility | Marked "withdrew before scoring" in the Reliability Resource Initiative list | https://www.pjm.com/-/media/DotCom/committees-groups/committees/pc/2025/20250506/20250506-rri-addendum---post-meeting.pdf | Unknown. Likely Lee energy facility (696 MW) or Nelson. Withdrawn. |
| AD2-194 | Will County, ComEd | Not shown | Natural gas | Not shown | Active on fyi, proposed completion 2027 | fyi only (https://www.interconnection.fyi). Not opened in a PJM document. | Labeled "Jackson Generation" on fyi. Likely an add or uprate at Jackson Generation (1288 MW). |
| C01-1171 | Lee County | Invenergy Nelson LLC (per fyi) | Gas (per fyi) | Not public | Cycle 1 (2026), queued 24 Apr 2026, proposed completion 28 Apr 2028 | fyi only | Probably another Nelson uprate. Not confirmed. |
| C01-1569 | Will County | Will County Facility, LLC (per fyi) | Gas (per fyi) | Not public | Cycle 1, queued 25 Apr 2026, proposed completion 31 Dec 2029 | fyi only | No match. Possible gap. |
| C01-1570 | Ogle County | Ogle County Hub, LLC (per fyi) | Gas (per fyi) | Not public | Cycle 1, queued 25 Apr 2026, proposed completion 31 Dec 2029 | fyi only | No match. Possible gap. |
| C01-1571 | LaSalle County | Prairie Pulse Project, LLC (per fyi) | Gas (per fyi) | Not public | Cycle 1, queued 25 Apr 2026, proposed completion 31 Dec 2029 | fyi only | No match. Possible gap. |

Other Illinois rows in Transition Cycle 1 and 2 Phase 1 and Phase 2 reports are solar, storage, wind or nuclear. The Reliability Resource Initiative selected no new-build Illinois gas. It did select nuclear uprates at Braidwood, Byron and LaSalle. C01-2036 (Putnam) is labeled gas on fyi but is Marquis Solar LLC, a mislabel. PJM's news release of 29 April 2026 says Cycle 1 drew 811 projects and 220 GW, including 157 gas projects and 105.8 GW of gas: https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/2026-releases/20260429-over-800-new-generation-projects-seek-to-connect-under-pjms-reformed-process.pdf

## Task 2. PJM AB1-089 "Byron to Wayne Thermal #1 Project"

| Queue ID | Site / POI | Developer | Fuel | MW | Status and date | URL that states it (opened and read) | GEM match |
|---|---|---|---|---|---|---|---|
| AB1-089 | Lee County. Point of interconnection is the ComEd 345 kV Byron to Wayne line, about 10 miles east of Byron Station. The interconnection agreement also modifies the Nelson Energy Center substation (TSS 942) and the customer address is 1311 Nelson Road, Rock Falls. | Invenergy Nelson LLC (impact study); Invenergy Thermal Development LLC (signed the interconnection agreement) | Natural gas, 1x1 combined cycle | 575 MW facility, 550 MW capacity | Queue XML status Suspended, submitted 30 Sep 2015. Interconnection agreement effective 19 Jan 2022, with commercial operation due 1 Jun 2026 and site permits due 17 Mar 2023. fyi says Withdrawn, which conflicts. The PJM XML is the primary source. | https://www.pjm.com/pub/planning/project-queues/impact_studies/ab1089_imp.pdf , .../isa/ab1_089_isa.pdf , .../facilities/ab1089_fac.pdf , .../feas_docs/ab1089_fea.pdf , .../csa/ab1_089_csa.pdf | Not in GEM as a separate unit. It is a possible third unit at the Nelson site. GEM Nelson (1008 MW, 4 units, operating) should be checked for it. The agreement is signed, so this is a candidate for a shelved or pre-construction record. |

Companion AB1-090 (Byron to Wayne #2, 575 MW) was withdrawn. No Illinois EPA permit or news for a new Nelson combined-cycle unit was found. That search was not finished.

## Task 3. MISO Electric Reliability Approval for Surplus (ERAS) cycles

| Queue ID | Site / POI | Developer | Fuel | MW | Status and date | URL | GEM match |
|---|---|---|---|---|---|---|---|
| E0003 | Sangamon County, Palomino 138 kV | Lincoln Capital Land LLC | Solar | 127.84 | Cycle 1 | https://cdn.misoenergy.org/ERAS%20Interconnection%20Requests718482.xlsx | Not gas |
| E0052 | Greene County | Pumpkin Patch Solar | Solar | not recorded | Cycle 4 | same file | Not gas |
| E0053, E0073 | Bureau County | Bluejacket Solar | Solar | not recorded | E0053 withdrawn | same file | Not gas |
| Alsey Solar | Scott County | not recorded | Solar | not recorded | Under review | same file | Not gas |

No Illinois gas or oil project is in the ERAS list (90 rows, sheet dated 24 Oct 2026). E0060 Missouri Electric Commission (86 MW gas) is in Missouri. The Cycle 5 release lists 15 projects, none in Illinois: https://www.misoenergy.org/meet-miso/media-center/2026---news-releases/miso-accelerates-new-generation-and-storage-projects-with-fifth-eras-cycle/ . The Cycle 2 release has no project list.

## Task 4. MISO entries

All rows come from `queues/miso_queue.json` (MISO API). fyi pages were opened for dates and counties. fyi hides developer, MW and fuel behind a paywall, and the project-name notes quoted below were copied from the earlier fyi and API read.

| Queue ID | Site / POI | Developer | Fuel | MW | Status and date | URL | GEM match |
|---|---|---|---|---|---|---|---|
| J955 | Sangamon County, Austin 345 kV bus | Not in API | Gas combined cycle | 1040 summer | Facility study done 2022-04-26, interconnection agreement 2022. Post-agreement status "Under Construction" (MISO field). Queued 2018-03-08, negotiated in service 2025-01-31. | https://www.interconnection.fyi/project/miso-j955 (lead) | Very likely Lincoln Land energy center, Pawnee (GEM 1276 MW, pre-construction). The MISO field says under construction. GEM status should be reviewed with dated evidence. |
| J1839 | Macon County, Decatur ADM North 138 kV | Not in API | Gas simple-cycle turbine | 325 summer | Interconnection agreement signed. Post-agreement status "Not Started". Negotiated in service 2026-11-01. | https://www.interconnection.fyi/project/miso-j1839 (lead) | Likely Broadwing Energy Center, Decatur (GEM 400 MW, pre-construction). Not confirmed. |
| J2656 | Macon County, Latham 138 kV | Not shown | Blank | 180 | Active in queue, Phase 2 of the 2022 study. Queued 2022-09-15. | https://www.interconnection.fyi/project/miso-j2656 | Unknown. Not identified. |
| R1025 | Williamson County, Marion Unit 4 main bus | Southern Illinois Power Cooperative | Battery storage | 180 | Queued 2022-10-14 | https://www.interconnection.fyi/project/miso-r1025 | Not gas. Replaces coal at Marion with a battery. |
| R1054 | Tazewell County, E.D. Edwards 69 kV | Not shown | Solar | 261 | Withdrawn 2025-12-31 | https://www.interconnection.fyi/project/miso-r1054 | Not gas. Edwards (retired coal). |
| R1055 | Peoria County, E.D. Edwards 138 kV | Not shown | Battery | 322 | Active in queue | https://www.interconnection.fyi/project/miso-r1055 | Not gas |
| R1056 | Tazewell County, E.D. Edwards 138 kV | Not shown | Solar | 184.71 | Withdrawn 2025-12-31 | https://www.interconnection.fyi/project/miso-r1056 | Not gas |
| S1040, S1041 | McLean and Ford counties, Gibson City South | Not shown | Solar (surplus of J734, J33) | 135 each | Active | https://www.interconnection.fyi/project/miso-s1040 | Not gas |
| S1048 | Logan County, Fogarty 138 kV | Not shown | Battery (surplus of J1102) | 40 | Active | https://www.interconnection.fyi/project/miso-s1048 | Not gas |
| S1052, S1057 | Cumberland and Coles counties, Neoga South | Not shown | Solar (Shelby, Glacier Moraine) | 150, 210 | Active | https://www.interconnection.fyi/project/miso-s1052 | Not gas. Not the Energy Shelby County plant. |

Blank-fuel requests in the 2026 study cycle and the no-cycle group (all Ameren, fuel blank in the API, MW is summer):

| Queue ID | County / POI | MW |
|---|---|---|
| J4232, J4238, J4247, J4254, J4257 | not given | 200, 125, 120, 250, 80 |
| J4260 | Wayne, Kays-Reifen 138 kV | 300 |
| J4262, J4267 | Tazewell (queued 2026-08-20, completion 2030-12-01) | 250, 200 |
| J4282, J4283, J4329, J4334, J4336, J4363 | not given | 242.8, 243.4, 250, 294, 250, 200 |
| J4301 | Peoria, Fargo to Sandburg 345 kV | 240 |
| J4344 | Macon, Oreana (in service 2028-09-06) | 300 |
| S1143, S1149, S1150 | not given | 135, 80, 80 |
| S1167 | Coles, Greenway 138 kV | 99 |
| S1168 | Marion, Finks 138 kV | 99 |
| J4321, J4343, J4279 (extra, not on the task list) | Redwood (two), not given | 250, 500, 9 |

Fuel for these is blank in the MISO data for most 2026-cycle requests (193 of 283), so it is a MISO publication gap and not specific to Illinois. No public document giving their fuel was found. The fyi pages show "-" for fuel. Treat the large ones (J4343 500 MW, J4260, J4344, J4254, J4301) as unclassified leads. Many are likely solar or battery.

## Task 5. Aggregators

- interconnection.fyi: opened and parsed. It is the source of all the PJM Cycle 1 leads and the J955, J1839 and AD2-194 gas labels. It shows 1,461 Illinois projects. It does not show developer, MW or fuel for most rows.
- Infrasure (https://www.infrasure.ai/project/pjm-ah1-718-moved-to-tc2-nelson-345-kv) and Cleanview were seen in search snippets only and not opened.
- Grid Status was not checked.

## What could not be determined, and what was tried

- PJM Cycle 1 (2026) project list with MW, site and fuel. PJM has not posted one. Tried the Cycle Service Request Status page, the Cycle 1 model FAQ PDF (no list), guessed Phase I report URLs (404), and ftp.pjm.com (fetch failed with both curl and `fetch.py`). Several guessed PJM paths return a "Page Not Found" template with HTTP 200, which is not a document. The Long-Term Firm Cycle 01 spreadsheet is mentioned on the status page but its link was not found. Open lead.
- C01-1569, C01-1570, C01-1571: web searches for Prairie Pulse, Ogle County Hub and Will County Facility found nothing. Developer, site and fuel are unconfirmed. Suggest asking for a GridTracker or PJM Cycle 1 data view.
- AB1-089: no permit or news found for a new Nelson unit. The Illinois EPA permit search was not finished here. A separate permit agent was running.
- AH1-700: no project name. AD2-194: no PJM document opened.
- J955 and J1839: no dated construction evidence found. Earlier web hits on the Lincoln Land permit (EmberClear, about 1.1 GW) are old.
- J2656 and the blank-fuel 2026 list: the MISO public map file `Generator.json` is empty, the MISO queue pages need a login, and MISO site scripts were only partly checked. The Cartovista map was not opened.
- MISO ERAS Cycle 2 press release gave no project list. The ERAS spreadsheet covers all cycles.
- fyi pages hide developer and MW. Descriptions for R and S rows came from MISO project names that fyi copies, not from a MISO primary file.
