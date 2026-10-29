# Access audit

Failed checks in the batch logs: 164
- bot_wall: 1
- gone: 138
- dead_host: 6
- server_error: 2
- value_missing: 7
- other: 10
- passing now with the current ladder: 2
- still failing, by class: bot_wall 1, gone 143, dead_host 7, server_error 2, value_missing 6, other 3

| Host | Failed | Classes then | Now | Learned route |
|---|---|---|---|---|
| www.kdhe.ks.gov | 95 | gone 89, value_missing 1, other 5 | gone 94, value_missing 1 | cf_impersonate |
| www.kpp.energy | 23 | value_missing 1, gone 22 | value_missing 1, gone 22 |  |
| estar.kcc.ks.gov | 5 | other 1, dead_host 4 | dead_host 5 |  |
| www.bpu.com | 4 | gone 3, value_missing 1 | gone 3, value_missing 1 |  |
| www.crestonnews.com | 3 | gone 3 | gone 3 |  |
| www.eia.gov | 3 | value_missing 1, other 2 | 2 pass, value_missing 1 |  |
| www.kdheks.gov | 3 | gone 3 | gone 3 |  |
| idnraqrr.iowadnr.gov | 2 | server_error 2 | server_error 2 |  |
| newschannel20.com | 2 | gone 2 | gone 2 |  |
| www.kpp.agency | 2 | gone 1, other 1 | other 2 |  |
| www.thegazette.com | 2 | gone 2 | gone 2 |  |
| baxtel.com | 1 | gone 1 | gone 1 |  |
| bpu.com | 1 | gone 1 | gone 1 |  |
| cfpub.epa.gov | 1 | gone 1 | gone 1 |  |
| cityofames.org | 1 | gone 1 | gone 1 |  |
| crestonnews.com | 1 | gone 1 | gone 1 |  |
| ftp.pjm.com | 1 | dead_host 1 | dead_host 1 |  |
| investors.evergy.com | 1 | gone 1 | gone 1 | cf_impersonate |
| iuc.iowa.gov | 1 | bot_wall 1 | bot_wall 1 |  |
| kpp.agency | 1 | other 1 | other 1 |  |
| modernpowersystems.com | 1 | gone 1 | gone 1 |  |
| mpw.org | 1 | gone 1 | gone 1 |  |
| oilandgaswatch.org | 1 | value_missing 1 | gone 1 | browser_render |
| pcb.illinois.gov | 1 | dead_host 1 | dead_host 1 |  |
| shareus11.springcm.com | 1 | value_missing 1 | value_missing 1 |  |
| sos.ks.gov | 1 | gone 1 | gone 1 | cf_clearance |
| wcfcourier.com | 1 | gone 1 | gone 1 |  |
| webapps.illinois.gov | 1 | gone 1 | gone 1 |  |
| www.alliantenergy.com | 1 | gone 1 | gone 1 |  |
| www.sos.ks.gov | 1 | value_missing 1 | value_missing 1 | cf_clearance |
| www3.scottcountyiowa.gov | 1 | gone 1 | gone 1 |  |

## Each failure now

- gone: https://baxtel.com/data-center/microlink-chicago-il  
  HTTP 404
- gone: https://bpu.com/About/MediaNewsReleases/BPUIssuesRequestsforProposals.aspx  
  HTTP 404
- gone: https://cfpub.epa.gov/rblc/  
  HTTP 404
- gone: https://cityofames.org/home/showpublisheddocument/19258/635809338107530000  
  HTTP 404
- gone: https://crestonnews.com/2018/11/06/cipco-announces-85-million-infrastructure-investment-in-rural-southwest-iowa/akqjfpw  
  HTTP 404
- dead_host: https://estar.kcc.ks.gov/  
  HTTP 000
- dead_host: https://estar.kcc.ks.gov/estar/ViewFile.aspx  
  HTTP 000
- dead_host: https://estar.kcc.ks.gov/estar/ViewFile.aspx/S202109200727054038.pdf?Id=7918cb08-a60d-4dea-b4b0-eeafa61bc0d0  
  HTTP 000
- dead_host: https://estar.kcc.ks.gov/estar/portal/kcc/Page/Docket/Docket.aspx  
  HTTP 000
- dead_host: https://estar.kcc.ks.gov/estar/portal/kcc/page/docket-docs/PSC/DocketDetails.aspx?DocketId=  
  HTTP 000
- dead_host: https://ftp.pjm.com/planning/m/cycle-service-request-status  
  HTTP 000
- server_error: https://idnraqrr.iowadnr.gov/ConPermitSearch/DownloadFile?dataString=%7B%22permitNumber%22%3A%2213-A-008-S3%22,%22permitNumber2%22%3A%2213-A-008-S3%22,%22projectNumber%22%3A%2218-194%22,%22emissionPointID%22%3A%22EP-87%22,%22emissionPointDescription%22%3A%22NATURAL%20GAS%20BOILER%22,%22issueDate%22%3A%222018-07-03T00%3A00%3A00%22,%22fileName%22%3A%2213-A-008-S3.pdf%22,%22rescissionDate%22%3Anull,%22easyAirPermitID%22%3Anull,%22documentType%22%3Anull,%22facilityNumber%22%3A%2282-02-006%22,%22documentID%22%3A0%7D&type=PERMIT_FILLED_OBJECT  
  HTTP 500
- server_error: https://idnraqrr.iowadnr.gov/ConPermitSearch/DownloadFile?dataString=%7B%22permitNumber%22%3A%2213-A-009-S3%22,%22permitNumber2%22%3A%2213-A-009-S3%22,%22projectNumber%22%3A%2218-194%22,%22emissionPointID%22%3A%22EP-88%22,%22emissionPointDescription%22%3A%22NATURAL%20GAS%20BOILER%22,%22issueDate%22%3A%222018-07-03T00%3A00%3A00%22,%22fileName%22%3A%2213-A-009-S3.pdf%22,%22rescissionDate%22%3Anull,%22easyAirPermitID%22%3Anull,%22documentType%22%3Anull,%22facilityNumber%22%3A%2282-02-006%22,%22documentID%22%3A0%7D&type=PERMIT_FILLED_OBJECT  
  HTTP 500
- gone: https://investors.evergy.com/2026IRP  
  HTTP 404
- bot_wall: https://iuc.iowa.gov/press-release/2024-07-02/iowa-utilities-board-now-iowa-utilities-commission  
  HTTP 403
- other: https://kpp.agency/wp-content/uploads/March-2023-KPP-Lightning-Round-min.pdf  
  HTTP 301
- gone: https://modernpowersystems.com/features/featuregas-with-carbon-capture-at-decatur-11561497/  
  HTTP 404
- gone: https://mpw.org/wp-content/uploads/2024/07/GCU-2024-0003-Public-Notice-.pdf  
  HTTP 404
- gone: https://newschannel20.com/news/local/aldermen-move-forward-in-cwlp-agreement-with-emberclear  
  HTTP 404
- gone: https://newschannel20.com/news/local/potential-natural-gas-generator-draws-opposition-from-clean-energy-activists  
  HTTP 404
- gone: https://oilandgaswatch.org/facility/rec_d4f1u5oq7easr8ra1fc0  
  soft-error page (title: '404 Not Found | EIP Oil &amp; Gas Watch')
- dead_host: https://pcb.illinois.gov/documents/dsweb/Get/Document-114055/as 21-6 SIPC Hearing Exhibits and Exhibit List_6-13-25.pdf  
  HTTP 000
- value_missing: https://shareus11.springcm.com/Public/Document/35150/e56d0963-88e0-4e4b-999a-0587e0573f89/ba249c18-eec2-f011-b84a-48df377ee718  
  missing expected content: ['Jeffrey']
- gone: https://sos.ks.gov/publications/pubs_kansas_register.aspx  
  HTTP 404
- gone: https://wcfcourier.com/online_features/press_releases/article_bd8d0c58-6e81-55eb-b13a-04bcd39f0ac9.html  
  HTTP 404
- gone: https://webapps.illinois.gov/EPA/WebSiteApi/api/PublicNotices/GetAirPublicNotices  
  HTTP 404
- gone: https://www.alliantenergy.com/cleanenergy/ourenergyvision/poweringwhatsnext/cleanenergyblueprint/cebiowa  
  HTTP 404
- value_missing: https://www.bpu.com/  
  missing expected content: ['Nearman']
- gone: https://www.bpu.com/Portals/0/pdf/2024-BPU_IRP_Report-2024_11-4-2024.pdf  
  HTTP 404
- gone: https://www.bpu.com/about-us/power-generation  
  HTTP 404
- gone: https://www.bpu.com/forbusiness/electricservice.aspx  
  HTTP 404
- gone: https://www.crestonnews.com/adair-county-free-press/2025/06/24/midamerican-gives-details-on-orient-energy-center-project  
  HTTP 404
- gone: https://www.crestonnews.com/adair-county-free-press/2025/08/13/county-supervisors-receive-iub-application-for-orient-energy-center  
  HTTP 404
- gone: https://www.crestonnews.com/adair-county-free-press/2025/09/03/midamerican-energy-moves-forward-with-replacing-tornado-damaged-turbines  
  HTTP 404
- value_missing: https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602024.zip  
  missing expected content: ['37.072616']
- PASS: https://www.eia.gov/electricity/data/eia923/archive/xls/f923_2024.zip  
  OK
- PASS: https://www.eia.gov/electricity/data/eia923/xls/f923_2024.zip  
  OK
- value_missing: https://www.kdhe.ks.gov/413/Public-Notices  
  missing expected content: ['Viola Energy Center', 'Conway Springs']
- gone: https://www.kdhe.ks.gov/DocumentCenter/Index/52528  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/15397  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/15402  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/23333  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/23334  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/23525  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/23526  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/27360  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/27361  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/27362  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/27363  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/29487  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/29488  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/35955  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/35956  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/35957  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/36020  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/36021  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/36092  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/36093  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/41445  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/41446  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/41562  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/41563  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/42028  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/42029  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43284  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43285  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43286  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43287  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43288  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43289  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43290  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43291  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43384  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43387  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43573  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/43574  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/44017  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/44018  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/44019  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/44020  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/46501  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/46502  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/46802  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/46803  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/51008  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/51009  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/51074  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/51075  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/51076  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/51077  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/51097  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/51098  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52012  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52013  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52014  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52015  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52447  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52448  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52527  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52528  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52540  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52540/Evergy-Viola-Energy-Center-Permit-Summary-PDF?bidId=  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52541  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52541/Evergy-Viola-Energy-Center-PSD-Application-PDF?bidId=  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52601  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52602  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52603  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52604  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52872  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52873  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52874  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52882  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52883  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/52884  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/56628  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/56631  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/56632  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/56633  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/56763  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/56764  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/58545  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/58546  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/58546/Evergy-Inc-Crooked-Creek-Energy-Draft-Permit-PDF?bidId=  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/58613  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/58613/Evergy-Inc--Crooked-Creek-Energy-Summary-Sheet-PDF?bidId=  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/58616  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/58616/Evergy-Inc--Crooked-Creek-Energy-Application-PDF?bidId=  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/59376  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/59377  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/59394  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/60220  
  HTTP 404
- gone: https://www.kdhe.ks.gov/DocumentCenter/View/60221  
  HTTP 404
- gone: https://www.kdheks.gov/bar/  
  HTTP 404
- gone: https://www.kdheks.gov/bar/airpermit.html  
  HTTP 404
- gone: https://www.kdheks.gov/bar/publicnotice.html  
  HTTP 404
- other: https://www.kpp.agency/projects/  
  HTTP 301
- other: https://www.kpp.agency/wp-content/uploads/March-2023-KPP-Lightning-Round-min.pdf  
  HTTP 301
- gone: https://www.kpp.energy/wp-content/uploads/2023/03/March-2023-KPP-Lightning-Round-min.pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2023/04/March-2023-KPP-Lightning-Round-min.pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2024/09/August-24-Lightning-Round-compressed-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2024/12/October-24-Lightning-Round-compressed-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2025/01/December-24-Lightning-Round-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2025/01/January-25-Lightning-Round-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2025/04/March-25-Lightning-Round-compressed-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2025/05/April-25-Lightning-Round-1-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2025/06/June-25-Lightning-Round-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2025/07/July-25-Lightning-Round-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2025/08/KPP-Lightning-Round-August-2025-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2025/11/Sept-Oct-25-Lightning-Round-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2025/12/Dec-25-Lightning-Round-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2026/01/KPP-Lightning-Round-January-2026-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2026/02/KPP-Lightning-Round-February-2026-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2026/03/KPP-Lightning-Round-March-2026-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2026/04/April-26-Lightning-Round-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2026/05/May-26-Lightning-Round-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2026/06/June-26-Lightning-Round-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/2026/07/July-26-Lightning-Round-1-pdf  
  HTTP 404
- value_missing: https://www.kpp.energy/wp-content/uploads/2026/07/July-26-Lightning-Round-1.pdf  
  missing expected content: ['Walnut']
- gone: https://www.kpp.energy/wp-content/uploads/2026/08/KPP-Lightning-Round-August-2026-pdf  
  HTTP 404
- gone: https://www.kpp.energy/wp-content/uploads/March-2023-KPP-Lightning-Round-min.pdf  
  HTTP 404
- value_missing: https://www.sos.ks.gov/publications/Register/Volume-44/Issues/Issue-48/11-27-25-53674.html  
  missing expected content: ['Viola Energy Center']
- gone: https://www.thegazette.com/energy/alliant-says-it-is-deprioritizing-fairfax-location-for-proposed-natural-gas-power-plant/  
  HTTP 404
- gone: https://www.thegazette.com/energy/why-power-plants-are-using-natural-gas-instead-of-coal/  
  HTTP 404
- gone: https://www3.scottcountyiowa.gov/auditor/pub/board_minutes/2026/20260714_Unofficial_COW_Meeting_Minutes.pdf  
  HTTP 404
