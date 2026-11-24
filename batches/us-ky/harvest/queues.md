# Kentucky interconnection queues, gas and oil (2026-11-07)

A queue entry is a lead, not proof that a plant exists or will be built. The queue file or page below is the citation.

## Sources

- MISO generator interconnection queue (includes ERAS rows): open JSON https://www.misoenergy.org/api/giqueue/getprojects, plain GET; 4080 projects, 63 in Kentucky, 1 state-hidden leads of the state's own owners, 0 ERAS rows, 120 state-hidden entries of owners shared with other states not kept, 64 entries with neither state nor owner shown (https://www.misoenergy.org/planning/resource-utilization/GI_Queue/gi-interactive-queue/)
- PJM serial queue (A01 through AJ1): open XML https://www.pjm.com/pjmfiles/media/planning/queues-data/PlanningQueues.xml, plain GET; 13 Kentucky gas, oil or thermal-unknown entries (https://www.pjm.com/planning/service-requests/serial-service-request-status)
- PJM cycle queue (Transition Cycle 1 and 2, Cycle 1): open XML posted to https://www.pjm.com/m/ProjectTransition/GenerateXMLTransitionProjectsAll with an empty grid filter; 6 Kentucky gas, oil or thermal-unknown entries (https://www.pjm.com/planning/m/cycle-service-request-status)
- TVA queue, read from the Berkeley Lab Queued Up file: open workbook https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx, tab "03. Complete Queue Data", plain GET; 38201 requests in the file, 66 Kentucky requests in the TVA queue; newest queue date in the file 2025-12-24, so requests filed after that are missing (https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx)
- LGEE queue, read from the Berkeley Lab Queued Up file: open workbook https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx, tab "03. Complete Queue Data", plain GET; 38201 requests in the file, 125 Kentucky requests in the LGE-KU queue; newest queue date in the file 2025-12-24, so requests filed after that are missing (https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx)

## Completeness

- MISO generator interconnection queue (includes ERAS rows): 4080 rows read, 64 for the state, 1 gas or oil, 2 fuel not shown
- PJM serial queue (A01 through AJ1): 9263 rows read, 228 for the state, 13 gas or oil, 0 fuel not shown
- PJM cycle queue (Transition Cycle 1 and 2, Cycle 1): 1792 rows read, 78 for the state, 6 gas or oil, 0 fuel not shown
- TVA queue, read from the Berkeley Lab Queued Up file: 38201 rows read, 66 for the state, 7 gas or oil, 26 fuel not shown
- LGEE queue, read from the Berkeley Lab Queued Up file: 38201 rows read, 125 for the state, 33 gas or oil, 3 fuel not shown

Requests to answer in coverage.json under `queues`: 21.

- MISO R5102
- MISO S1073
- PJM AH1-721 - moved to TC2
- PJM AH1-721
- PJM C01-1131
- PJM C01-1227
- PJM C01-1228
- PJM C01-1325
- TVA 417
- TVA 55
- TVA 628
- TVA 657
- LGEE LGE-CS2025-002
- LGEE LGE-GIS-2009-001
- LGEE LGE-GIS-2009-004
- LGEE LGE-GIS-2010-001
- LGEE LGE-GIS-2013-001
- LGEE LGE-GIS-2022-003
- LGEE LGE-GIS-2023-002
- LGEE LGE-GIS-2024-002
- LGEE LGE-GIS-2024-006

## Matched to GEM plants

### Big Sandy Peaker Plant (L100000402085), Kenova, Wayne County

No queue entry matched.

### Big Sandy Plant (L100000103930), Louisa, Lawrence County

- PJM R62; Natural Gas; 20 MW; Lawrence County; In Service; queued 2007-01-08; in service 2016-05-31; point of interconnection: Big Sandy 138kV; AEP (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM W1-035; Natural Gas; 750 MW; Lawrence County; Withdrawn; queued 2010-02-26; in service 2012-06-01; point of interconnection: Baker 345kV; AEP (same county, gas or oil, check it is this plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM AC1-038; Natural Gas; 13 MW; Lawrence County; In Service; queued 2016-08-30; in service 2016-05-30; point of interconnection: Big Sandy 1 138kV; AEP (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM AC2-172; Natural Gas; 12 MW; Lawrence County; In Service; queued 2017-03-30; in service 2016-05-30; point of interconnection: Big Sandy 1 138kV; AEP (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM C01-1131; Natural Gas; 458 MW; Lawrence County; Active; queued 2026-04-10; in service 2030-09-30; point of interconnection: Baker 345 kV; AEP (same county, gas or oil, check it is this plant). Citation: https://www.pjm.com/planning/m/cycle-service-request-status
- PJM C01-1325; Natural Gas; 1046 MW; Lawrence County; Active; queued 2026-04-24; in service 2031-09-30; point of interconnection: Baker 345 kV; AEP (same county, gas or oil, check it is this plant). Citation: https://www.pjm.com/planning/m/cycle-service-request-status

### Bluegrass generating station (L100000401892), LaGrange, Oldham County

- LGEE LGE-GIS-2011-001; Gas; 450 MW; Oldham County; withdrawn; queued 2011-01-21; in service 2015-01-01; point of interconnection: Buckner Substation on the 345 kV (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx

### Cane Run Station (L100000103932), Louisville, Jefferson County

- LGEE LGE-CS2025-002; Gas; 680 MW; Jefferson County; active; queued 2025-11-20; in service 2031-04-01; point of interconnection: Mill Creek Substation, 345 kV (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2010-001; Gas; 690 MW; Jefferson County; active; queued 2010-04-07; in service 2015-03-01; point of interconnection: Cane Run Switching Station 138 kV (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2010-002; Gas; 704 MW; Jefferson County; withdrawn; queued 2010-11-08; in service 2016-06-01; point of interconnection: New substation that will tap and tie into the Mill Creek ‚Äì Middletown 345 kV and the Mill Creek ‚Äì Blue Lick 345 kV line; requested feasibility restudy for Alternative POI - Mill Creek to Hardin 345 kV line (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2011-002; Gas+Oil; 30 MW; Jefferson County; withdrawn; queued 2011-02-22; in service 2015-03-01; point of interconnection: Cane Run Switching Station 138 kV uprate (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2013-001; Gas+Oil; 691 MW; Jefferson County; active; queued 2013-08-23; in service 2015-03-01; point of interconnection: Cane Run Switching Station 138 kV uprate (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2021-005; Gas; 635 MW; Jefferson County; withdrawn; queued 2021-01-21; in service 2025-12-31; point of interconnection: Mill Creek 345 kV Station (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2022-003; Gas; 660 MW; Jefferson County; active; queued 2022-06-21; in service 2027-04-01; point of interconnection: Mill Creek Substation 345 kV bus (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2024-006; Gas+Oil; 94 MW; Jefferson County; active; queued 2024-05-03; in service 2026-05-04; point of interconnection: Cane Run CT Substation 138kV (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx

### Cooper power station (L100000103935), Burnside, Pulaski County

- PJM AH1-721 - moved to TC2; Natural Gas; 758.951 MW; N/A County; Active; queued 2025-04-02; in service 2030-12-31; point of interconnection: Laurel-Cooper 161 kV; EKPC (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM AH1-721; Natural Gas; 758.951 MW; Not Specified County; Active; queued 2025-04-02; in service 2030-12-31; point of interconnection: Laurel-Cooper 161 kV; EKPC (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/m/cycle-service-request-status
- PJM AH1-749; Natural Gas; 216 MW; Withdrawn; in service 2028-12-12; EKPC (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/m/cycle-service-request-status
- PJM C01-1227; Natural Gas; 758 MW; Mason County; Active; queued 2026-04-27; in service 2031-12-31; point of interconnection: Spurlock - Meldahl Dam 345 kV; EKPC (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/m/cycle-service-request-status
- PJM C01-1228; Natural Gas; 212.42 MW; Casey County; Active; queued 2026-04-27; in service 2028-12-12; point of interconnection: Casey County - Liberty Jct 161 kV; EKPC (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/m/cycle-service-request-status

### E.W. Brown Generating Station (L100000103937), Burgin, Mercer County

- LGEE LGE-GIS-2011-004; Gas+Oil; 880 MW; Mercer County; withdrawn; queued 2011-05-16; in service 2018-01-01; point of interconnection: Brown Substation on 345 kV side (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2021-006; Gas; 635 MW; Mercer County; withdrawn; queued 2021-01-21; in service 2025-12-31; point of interconnection: South 138 kV bus of the Brown North Substation (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2022-004; Gas; 660 MW; Mercer County; withdrawn; queued 2022-06-21; in service 2027-04-01; point of interconnection: Brown North Substation 345 kV bus (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2022-011; Gas; 660 MW; Mercer County; withdrawn; queued 2022-10-28; in service 2028-03-01; point of interconnection: Brown North Substation 138 kV bus (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2023-002; Gas; 660 MW; Mercer County; active; queued 2023-04-14; in service 2030-04-01; point of interconnection: Brown North Substation 345 kV bus. (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx

### East Bend Generating Station (L100000103938), Rabbit Hash, Boone County

No queue entry matched.

### Elmer Smith Station (L100000103939), Owensboro, Daviess County

No queue entry matched.

### Green Station (L100000103943), Sebree, Henderson County

- LGEE LGE-GIS-2007-003; Gas; 640 MW; Henderson County; withdrawn; queued 2007-03-02; in service 2011-03-31; point of interconnection: Green River substation on the 161 kV side (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2007-004; Gas+Coal; 642 MW; Henderson County; withdrawn; queued 2007-04-24; in service 2011-03-31; point of interconnection: Daviess 345 kV substation bus (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx

### J K Smith power station (L100000401893), Winchester, Clark County

- PJM Y1-039A_EKPC1; Natural Gas; 170 MW; Clark County; Withdrawn; queued 2012-03-23; in service 2016-06-01; point of interconnection: JK Smith 138 KV; EKPC (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM Z2-084; Natural Gas; 207.8 MW; Nelson County; Withdrawn; queued 2014-04-29; in service 2016-12-01; point of interconnection: JK Smith 345kV; EKPC (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM AB2-054; Natural Gas; 504 MW; Clark County; Withdrawn; queued 2016-03-17; in service 2023-03-01; point of interconnection: JK Smith 345kV; EKPC (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM AD1-134; Natural Gas; 72.9 MW; Unknown County; Withdrawn; queued 2017-09-29; in service 2020-07-01; point of interconnection: JK Smith 138 kV; EKPC (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status

### KYMEA Energy Center I (L100001026095), Madisonville,  County

No queue entry matched.

### Liberty Station Power Plant (L100001025720), Liberty, Casey County

- PJM C01-1228; Natural Gas; 212.42 MW; Casey County; Active; queued 2026-04-27; in service 2028-12-12; point of interconnection: Casey County - Liberty Jct 161 kV; EKPC (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/m/cycle-service-request-status

### Marshall energy facility (L100000402323), Calvert City, Marshall County

No queue entry matched.

### Mill Creek Station (L100000103945), Louisville, Jefferson County

- LGEE LGE-CS2025-002; Gas; 680 MW; Jefferson County; active; queued 2025-11-20; in service 2031-04-01; point of interconnection: Mill Creek Substation, 345 kV (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2010-001; Gas; 690 MW; Jefferson County; active; queued 2010-04-07; in service 2015-03-01; point of interconnection: Cane Run Switching Station 138 kV (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2010-002; Gas; 704 MW; Jefferson County; withdrawn; queued 2010-11-08; in service 2016-06-01; point of interconnection: New substation that will tap and tie into the Mill Creek ‚Äì Middletown 345 kV and the Mill Creek ‚Äì Blue Lick 345 kV line; requested feasibility restudy for Alternative POI - Mill Creek to Hardin 345 kV line (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2011-002; Gas+Oil; 30 MW; Jefferson County; withdrawn; queued 2011-02-22; in service 2015-03-01; point of interconnection: Cane Run Switching Station 138 kV uprate (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2013-001; Gas+Oil; 691 MW; Jefferson County; active; queued 2013-08-23; in service 2015-03-01; point of interconnection: Cane Run Switching Station 138 kV uprate (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2021-005; Gas; 635 MW; Jefferson County; withdrawn; queued 2021-01-21; in service 2025-12-31; point of interconnection: Mill Creek 345 kV Station (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2022-003; Gas; 660 MW; Jefferson County; active; queued 2022-06-21; in service 2027-04-01; point of interconnection: Mill Creek Substation 345 kV bus (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2024-006; Gas+Oil; 94 MW; Jefferson County; active; queued 2024-05-03; in service 2026-05-04; point of interconnection: Cane Run CT Substation 138kV (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx

### PPS power plant No 1 (L100000402189), Paducah, Mccracken County

- TVA 222; Gas; 122 MW; Mccracken County; withdrawn; queued 2009-07-16 (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- TVA 226; Gas; 122 MW; Mccracken County; withdrawn; queued 2010-12-01 (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx

### Paddys Run power station (L100000401571), Louisville, Jefferson County

- LGEE LGE-CS2025-002; Gas; 680 MW; Jefferson County; active; queued 2025-11-20; in service 2031-04-01; point of interconnection: Mill Creek Substation, 345 kV (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2010-001; Gas; 690 MW; Jefferson County; active; queued 2010-04-07; in service 2015-03-01; point of interconnection: Cane Run Switching Station 138 kV (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2010-002; Gas; 704 MW; Jefferson County; withdrawn; queued 2010-11-08; in service 2016-06-01; point of interconnection: New substation that will tap and tie into the Mill Creek ‚Äì Middletown 345 kV and the Mill Creek ‚Äì Blue Lick 345 kV line; requested feasibility restudy for Alternative POI - Mill Creek to Hardin 345 kV line (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2011-002; Gas+Oil; 30 MW; Jefferson County; withdrawn; queued 2011-02-22; in service 2015-03-01; point of interconnection: Cane Run Switching Station 138 kV uprate (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2013-001; Gas+Oil; 691 MW; Jefferson County; active; queued 2013-08-23; in service 2015-03-01; point of interconnection: Cane Run Switching Station 138 kV uprate (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2021-005; Gas; 635 MW; Jefferson County; withdrawn; queued 2021-01-21; in service 2025-12-31; point of interconnection: Mill Creek 345 kV Station (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2022-003; Gas; 660 MW; Jefferson County; active; queued 2022-06-21; in service 2027-04-01; point of interconnection: Mill Creek Substation 345 kV bus (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2024-006; Gas+Oil; 94 MW; Jefferson County; active; queued 2024-05-03; in service 2026-05-04; point of interconnection: Cane Run CT Substation 138kV (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx

### Paradise Fossil Plant (L100000103946), Drakesboro, Muhlenberg County

- TVA 243; Gas; 1184 MW; Muhlenberg County; operational; queued 2013-11-21 (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- TVA 417; Gas; 780 MW; Muhlenberg County; active; queued 2020-02-10; in service 2022-10-01; point of interconnection: Paradise 500-kV Station (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- TVA 657; Gas; 60 MW; Muhlenberg County; active; queued 2024-10-01; in service 2030-02-01; point of interconnection: Paradise CC Plant (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2007-001; Gas; 750 MW; Muhlenberg County; withdrawn; queued 2007-02-28; in service 2015-01-12; point of interconnection: Green River substation on the 161 kV side (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2007-002; Gas; 610 MW; Muhlenberg County; withdrawn; queued 2007-02-28; in service 2016-01-12; point of interconnection: Green River substation on the 161 kV side (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2009-002; Gas; 690 MW; Muhlenberg County; withdrawn; in service 2017-04-01; point of interconnection: Green River substation on the 161 kV side (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2009-003; Gas+Oil; 560 MW; Muhlenberg County; withdrawn; queued 2009-11-16; in service 2017-04-01; point of interconnection: Green River substation on the 161 kV side (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2010-003; Gas+Oil; 690 MW; Muhlenberg County; withdrawn; queued 2010-11-30; in service 2018-01-01; point of interconnection: Green River substation on the 161 kV side (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2013-002; Gas+Oil; 898 MW; Muhlenberg County; withdrawn; queued 2013-10-16; in service 2018-03-01; point of interconnection: Green River substation on the 161 kV side (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx

### Riverside Generating (KY) power station (L100000402250), Catlettsburg, Lawrence County

- PJM W1-035; Natural Gas; 750 MW; Lawrence County; Withdrawn; queued 2010-02-26; in service 2012-06-01; point of interconnection: Baker 345kV; AEP (same county, gas or oil, check it is this plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM W3-162; Natural Gas; 20 MW; Lawrence County; In Service; queued 2010-10-29; in service 2011-09-09; point of interconnection: Baker 345kV; AEP (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM X2-006; Natural Gas; Lawrence County; Withdrawn; queued 2011-05-06; in service 2021-06-01; point of interconnection: Baker 345kV; AEP (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM Y2-045; Natural Gas; 6 MW; Lawrence County; In Service; queued 2012-08-02; in service 2016-01-08; point of interconnection: Baker 345kV; AEP (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM C01-1131; Natural Gas; 458 MW; Lawrence County; Active; queued 2026-04-10; in service 2030-09-30; point of interconnection: Baker 345 kV; AEP (same county, gas or oil, check it is this plant). Citation: https://www.pjm.com/planning/m/cycle-service-request-status
- PJM C01-1325; Natural Gas; 1046 MW; Lawrence County; Active; queued 2026-04-24; in service 2031-09-30; point of interconnection: Baker 345 kV; AEP (same county, gas or oil, check it is this plant). Citation: https://www.pjm.com/planning/m/cycle-service-request-status

### Robert Reid Power Plant (L100000103947), Sebree,  County

- MISO J3089; Gas; 696 MW; Webster County; Withdrawn; queued 2022-09-15; in service 2029-04-30; point of interconnection: Reid EHV; BIG RIVERS ELECTRIC CORPORATION BREC (point of interconnection or name matches the plant). Citation: https://www.misoenergy.org/planning/resource-utilization/GI_Queue/gi-interactive-queue/
- MISO S1073; (not shown); 75 MW; Webster County; Active; queued 2025-02-19; in service 2026-08-31; point of interconnection: Hopkins to Reid EVH 161kV; BIG RIVERS ELECTRIC CORPORATION BREC (point of interconnection or name matches the plant). Citation: https://www.misoenergy.org/planning/resource-utilization/GI_Queue/gi-interactive-queue/

### Spurlock power station (L100000103950), Maysville, Mason County

- PJM AB1-169; Natural Gas; 1100 MW; Mason County; Withdrawn; queued 2015-10-30; in service 2023-06-30; point of interconnection: Stuart 345kV; Dayton (same county, gas or oil, check it is this plant). Citation: https://www.pjm.com/planning/service-requests/serial-service-request-status
- PJM C01-1227; Natural Gas; 758 MW; Mason County; Active; queued 2026-04-27; in service 2031-12-31; point of interconnection: Spurlock - Meldahl Dam 345 kV; EKPC (point of interconnection or name matches the plant). Citation: https://www.pjm.com/planning/m/cycle-service-request-status

### Trimble County power station (L100000103951), Bedford, Trimble County

- LGEE LGE-CS2025-005; Gas; 17 MW; Trimble County; active; queued 2025-12-18; in service 2026-10-01; point of interconnection: Trimble County Switching Station, 345 kV (Unit #5) (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-CS2025-006; Gas; 17 MW; Trimble County; active; queued 2025-12-18; in service 2026-10-01; point of interconnection: Trimble County Switching Station, 345 kV (Unit #6) (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-CS2025-007; Gas; 17 MW; Trimble County; active; queued 2025-12-18; in service 2026-10-01; point of interconnection: Trimble County Switching Station, 345 kV (Unit #7) (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-CS2025-008; Gas; 17 MW; Trimble County; active; queued 2025-12-18; in service 2026-10-01; point of interconnection: Trimble County Switching Station, 345 kV (Unit #8) (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-CS2025-009; Gas; 17 MW; Trimble County; active; queued 2025-12-18; in service 2026-10-01; point of interconnection: Trimble County Switching Station, 345 kV (Unit #9) (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-CS2025-010; Gas; 17 MW; Trimble County; active; queued 2025-12-18; in service 2026-10-01; point of interconnection: Trimble County Switching Station, 345 kV (Unit #10) (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-CS2025-011; Gas; 19 MW; Trimble County; active; queued 2025-12-18; in service 2029-05-13; point of interconnection: Trimble County Switching Station, 345 kV (Unit #7) (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-CS2025-012; Gas; 19 MW; Trimble County; active; queued 2025-12-18; in service 2030-05-05; point of interconnection: Trimble County Switching Station, 345 kV (Unit #6) (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2009-004; Gas; 785 MW; Trimble County; active; queued 2009-12-29; in service 2010-10-01; point of interconnection: Trimble County 345 kV (same county, gas or oil, check it is this plant). Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx

## Gas and oil entries that match no GEM plant (possible new plants or uprates)

- LGEE LGE-GIS-2009-001; Gas; 123 MW; Mccraken County; operational; queued 2009-02-23; in service 2010-05-01; point of interconnection: Grahamville ‚Äì South Paducah 161 kV line. Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- LGEE LGE-GIS-2024-002; Gas; 75 MW; Hopkins County; active; queued 2024-02-14; in service 2027-04-01; point of interconnection: 2MADSNV LP W to 2 EARLINGTN N 69 kV line. Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- TVA 628; Gas; 1600 MW; Todd County; active; queued 2024-06-12; in service 2030-06-01; point of interconnection: PARADISE - MONTGOMERY 500 KV. Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx
- TVA 629; Gas; 1224 MW; Todd County; withdrawn; queued 2024-06-12. Citation: https://emp.lbl.gov/sites/default/files/2026-05/LBNL_Ix_Queue_Data_File_thru2025.xlsx

## Entries with fuel not shown (state's own transmission owner with the state blanked, a PJM entry with no fuel, or an SPP thermal entry with no fuel)

MISO blanks state, fuel, county and point of interconnection on its newest entries. Sizes of 100 MW or more are worth a look when the sweep reaches the plant's utility.

- TVA 152; Other; 1500 MW; Muhlenberg County; withdrawn; queued 2001-03-13
- TVA 137; Other; 950 MW; Mccracken County; withdrawn; queued 2000-11-22
- TVA 106; Other; 800 MW; Logan County; withdrawn; queued 2000-06-06
- TVA 145; Other; 750 MW; Muhlenberg County; withdrawn; queued 2001-02-12
- TVA 146; Other; 750 MW; Muhlenberg County; withdrawn; queued 2001-02-12
- TVA 174; Other; 683 MW; Monroe County; withdrawn; queued 2001-08-20
- TVA 124; Other; 640 MW; Mccracken County; withdrawn; queued 2000-11-02
- TVA 132; Other; 640 MW; Metcalfe County; withdrawn; queued 2000-11-20
- TVA 133; Other; 640 MW; Marshall County; withdrawn; queued 2000-11-20
- TVA 55; Other; 640 MW; Marshall County; operational; queued 1999-08-11
- TVA 56; Other; 640 MW; Muhlenberg County; withdrawn; queued 1999-08-11
- TVA 57; Other; 640 MW; Metcalfe County; withdrawn; queued 1999-08-11
- TVA 39; Other; 600 MW; Marshall County; withdrawn; queued 1999-02-22
- TVA 42; Other; 600 MW; Marshall County; withdrawn; queued 1999-03-11
- TVA 16; Other; 500 MW; Marshall County; withdrawn; queued 1998-07-01
- TVA 8; Other; 350 MW; Warren County; withdrawn; queued 1998-05-19
- TVA 125; Other; 340 MW; Mccracken County; withdrawn; queued 2000-11-02
- TVA 119; Other; 320 MW; Warren County; withdrawn; queued 2000-09-11
- TVA 120; Other; 320 MW; Warren County; withdrawn; queued 2000-09-11
- TVA 60; Other; 316 MW; Warren County; withdrawn; queued 1999-09-13
- TVA 69; Other; 316 MW; Warren County; withdrawn; queued 1999-11-04
- TVA 58; Other; 300 MW; Marshall County; withdrawn; queued 1999-08-20
- TVA 77; Other; 95 MW; Livingston County; withdrawn; queued 1999-12-21
- MISO S1073; (not shown); 75 MW; Webster County; Active; queued 2025-02-19; in service 2026-08-31; point of interconnection: Hopkins to Reid EVH 161kV; BIG RIVERS ELECTRIC CORPORATION BREC
