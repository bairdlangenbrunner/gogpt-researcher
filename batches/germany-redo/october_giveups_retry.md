# Access audit

Failed checks in the batch logs: 111
- rate_limited: 10
- bot_wall: 9
- gone: 16
- dead_host: 5
- server_error: 5
- value_missing: 47
- other: 19
- passing now with the current ladder: 23
- still failing, by class: rate_limited 4, bot_wall 2, gone 22, dead_host 9, server_error 5, value_missing 45, other 1

| Host | Failed | Classes then | Now | Learned route |
|---|---|---|---|---|
| www.uvp-verbund.de | 14 | rate_limited 10, other 3, gone 1 | 10 pass, rate_limited 4 | rate_limit_wait |
| www.energate-messenger.de | 6 | bot_wall 4, other 2 | 6 pass | cf_clearance |
| www.enbw.com | 3 | value_missing 2, other 1 | value_missing 2, gone 1 | browser_render |
| www.infraserv.com | 3 | value_missing 1, server_error 2 | value_missing 1, server_error 2 | browser_render |
| www.iqony.energy | 3 | value_missing 3 | value_missing 3 | browser_render |
| www.pq-energy.com | 3 | other 1, dead_host 2 | dead_host 3 |  |
| de.wikipedia.org | 2 | value_missing 2 | value_missing 2 | browser_render |
| www.berlin.de | 2 | other 1, value_missing 1 | gone 1, value_missing 1 | browser_render |
| www.bs-energy.de | 2 | gone 1, value_missing 1 | gone 1, value_missing 1 | browser_render |
| www.chemieindustrie-online.de | 2 | bot_wall 2 | 2 pass | cf_impersonate |
| www.kraftwerk-saarbruecken.com | 2 | other 2 | dead_host 2 |  |
| www.mainova.de | 2 | value_missing 2 | value_missing 2 | browser_render |
| www.man-es.com | 2 | value_missing 2 | value_missing 2 | browser_render |
| www.stadt-und-werk.de | 2 | value_missing 2 | value_missing 2 | browser_render |
| www.statkraft.de | 2 | value_missing 2 | value_missing 2 | browser_render |
| 100jahre.auew.de | 1 | dead_host 1 | dead_host 1 |  |
| auew.de | 1 | gone 1 | gone 1 |  |
| bund-region-hannover.de | 1 | value_missing 1 | value_missing 1 | cf_impersonate |
| eisenhuettenstadt.arcelormittal.com | 1 | bot_wall 1 | bot_wall 1 |  |
| energie-und-management.de | 1 | value_missing 1 | other 1 |  |
| evh.de | 1 | other 1 | gone 1 |  |
| fuelcellsworks.com | 1 | value_missing 1 | value_missing 1 | browser_render |
| gwf-gas.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| ldc.sachsen.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| pq-energy.com | 1 | dead_host 1 | dead_host 1 |  |
| pressearchiv.steag.com | 1 | dead_host 1 | dead_host 1 |  |
| unserwerk.swd-ag.de | 1 | gone 1 | gone 1 |  |
| waerme.hamburg | 1 | server_error 1 | server_error 1 |  |
| web2.cylex.de | 1 | bot_wall 1 | 1 pass | browser_render |
| www.allgaeukraft.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.bayern-innovativ.de | 1 | gone 1 | gone 1 |  |
| www.bew.berlin | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.bundesnetzagentur.de | 1 | other 1 | gone 1 |  |
| www.cdu-herdecke.de | 1 | gone 1 | gone 1 |  |
| www.chemcoast.de | 1 | value_missing 1 | 1 pass | browser_render |
| www.chemiepark-marl.de | 1 | gone 1 | gone 1 |  |
| www.dillinger.de | 1 | gone 1 | gone 1 |  |
| www.energie-und-management.de | 1 | value_missing 1 | dead_host 1 |  |
| www.energie.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.energiejobs.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.energy-saxony.net | 1 | gone 1 | gone 1 |  |
| www.entwicklungsstadt.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.eza-allgaeu.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.fernwaerme-ulm.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.foerde.news | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.hamburger-energiewerke.de | 1 | server_error 1 | server_error 1 |  |
| www.ihk.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.industriepark-hoechst.com | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.ingenieur.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.jaeger-ingenieure.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.kmw-ag.de | 1 | other 1 | gone 1 |  |
| www.leag.de | 1 | other 1 | gone 1 |  |
| www.oeko.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.pv-magazine.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.qcintel.com | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.regierung-schwaben.bayern.de | 1 | gone 1 | 1 pass |  |
| www.regierung.schwaben.bayern.de | 1 | gone 1 | 1 pass |  |
| www.saarbruecker-stadtwerke.de | 1 | gone 1 | gone 1 |  |
| www.saarland.ihk.de | 1 | server_error 1 | server_error 1 |  |
| www.solar-professionell.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.stadtwerke-duisburg.de | 1 | other 1 | gone 1 |  |
| www.stadtwerke-ffo.de | 1 | gone 1 | gone 1 |  |
| www.stadtwerke-flensburg.de | 1 | gone 1 | value_missing 1 | browser_render |
| www.statkraft.com | 1 | other 1 | gone 1 |  |
| www.suedkurier.de | 1 | gone 1 | gone 1 |  |
| www.swb.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.sweco-gmbh.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.swm.de | 1 | gone 1 | gone 1 |  |
| www.trianel-hamm.de | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.umweltbundesamt.de | 1 | other 1 | gone 1 |  |
| www.uniper.energy | 1 | bot_wall 1 | bot_wall 1 | cf_impersonate |
| www.volkswagen-group.com | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.volkswagen-newsroom.com | 1 | other 1 | gone 1 |  |
| www.waz-online.de | 1 | other 1 | 1 pass | browser_render |
| www.wirtschaft-regional.net | 1 | value_missing 1 | value_missing 1 | browser_render |
| www.zfk.de | 1 | value_missing 1 | value_missing 1 | browser_render |

## Each failure now

- gone: http://www.cdu-herdecke.de/utool/news/0/archiv/155.htm  
  HTTP 404
- dead_host: http://www.pq-energy.com/de/projekte.html  
  HTTP 000; the live page is gone, but the archived copy https://web.archive.org/web/20210124000926/http://pq-energy.com/de/projekte.html still shows the value. Cite that archived address (verify it directly) or a live copy of the document
- dead_host: http://www.pq-energy.com/en/projects.html  
  HTTP 000
- dead_host: https://100jahre.auew.de/  
  HTTP 000; the live page is gone, but the archived copy https://web.archive.org/web/20260517021245/https://100jahre.auew.de/ still shows the value. Cite that archived address (verify it directly) or a live copy of the document
- gone: https://auew.de/presse/auew-installiert-grossspeicher-im-stromnetz/  
  HTTP 404
- value_missing: https://bund-region-hannover.de/service/meldungen/detail/news/neubau-eines-mega-gaskraftwerks-in-mehrum-droht-warum-fragt-niemand-nach-dem-sinn/  
  missing expected content: ['1200', 'Hohenhameln']
- value_missing: https://de.wikipedia.org/wiki/Heizkraftwerk_Cottbus  
  missing expected content: ['14.34']
- value_missing: https://de.wikipedia.org/wiki/Stadtwerke_Pforzheim  
  missing expected content: ['eigenes Heizkraftwerk']
- bot_wall: https://eisenhuettenstadt.arcelormittal.com/News-Information/Pressemeldungen/2019/broker.jsp  
  HTTP 403
- other: https://energie-und-management.de/nachrichten/alle/detail/allgaeuer-koppeln-energiespeicher-mit-gasturbine-131316  
  HTTP 301
- gone: https://evh.de/gro%C3%9Fkunden/unternehmen/Heizkraftwerke/energiepark/trotha  
  HTTP 404
- value_missing: https://fuelcellsworks.com/2026/09/09/h2/kawasaki-and-rwe-complete-30mw-hydrogen-gas-turbine-installation-in-germany  
  missing expected content: ['L30A', 'Emsland']
- value_missing: https://gwf-gas.de/maerkte-und-unternehmen/gasturbine-fuer-neue-gud-anlage-der-stadtwerke-flensburg-ist-da/  
  missing expected content: ['SGT']
- value_missing: https://ldc.sachsen.de/bekanntmachung/?ID=22592&art_param=634  
  missing expected content: ['EVC 3', '14.04.2025']
- dead_host: https://pq-energy.com/en/projects.html  
  HTTP 000; the live page is gone, but the archived copy https://web.archive.org/web/20210123230940/http://pq-energy.com/en/projects.html still shows the value. Cite that archived address (verify it directly) or a live copy of the document
- dead_host: https://pressearchiv.steag.com/3292+M58ae6efec2d.html  
  HTTP 000; no Wayback snapshot to verify against
- gone: https://unserwerk.swd-ag.de/fileadmin/user_upload/pdfs/Geschaeftsbericht-2024_Stadtwerke-Duesseldorf.pdf  
  HTTP 404
- server_error: https://waerme.hamburg/fernwaermesystem/energiepark-hafen  
  HTTP 500
- PASS: https://web2.cylex.de/firma-home/heizkraftwerk-pforzheim---swp-stadtwerke-pforzheim-gmbh-_-co--kg-15642936.html  
  OK
- value_missing: https://www.allgaeukraft.de/download/akw_basismaterial.pdf  
  missing expected content: ['Veits']
- gone: https://www.bayern-innovativ.de/en/page/stadtwerke-muenchen-reconsiders-rapid-phase-out-of-coal-use  
  HTTP 404
- value_missing: https://www.berlin.de/lagetsi/aktuelles/bekanntmachungen/artikel.1587918.php  
  missing expected content: ['Spreebord']
- gone: https://www.berlin.de/sen/uvk/klimaschutz/klimaschutz-in-der-umsetzung/waermewende-im-land-berlin/kohleausstieg-berlin/  
  HTTP 404
- value_missing: https://www.bew.berlin/fernwaermesystem/erzeugungsanlagen/  
  missing expected content: ['Spreebord']
- gone: https://www.bs-energy.de/geschaeftskunden/unternehmen-1/erzeugung-der-zukunft/gasturbine-flexibel-mit-brennstoff-erdgas  
  HTTP 404
- value_missing: https://www.bs-energy.de/unternehmen/versorgung/erzeugungsanlagen/  
  missing expected content: ['Hamburger Stra']
- gone: https://www.bundesnetzagentur.de/SharedDocs/Downloads/EN/Areas/ElectricityGas/Gas_grid/ConsultationScenario2020.pdf?__blob=publicationFile&v=2  
  HTTP 404
- PASS: https://www.chemcoast.de/unternehmen/dow-deutschland-anlagengesellschaft-mbh  
  value found once the page ran its scripts in Chrome
- PASS: https://www.chemieindustrie-online.de/branchennews/gas-statt-kohle-currenta-investiert-rund-50-millionen-euro-in-nachhaltige-kraftwerks-sanierung  
  OK
- PASS: https://www.chemieindustrie-online.de/branchennews/infraserv-hoechst-investiert-dreistelligen-millionenbetrag-in-neue-gasturbinen-anlage  
  OK
- gone: https://www.chemiepark-marl.de/de/evonik-nimmt-neues-gaskraftwerk-in-marl-in-betrieb-178347.html  
  HTTP 404
- gone: https://www.dillinger.de/d/en/news/press-releases/turning-of-the-first-sod-for-blast-furnace-gas-power-plant-in-dillingen-68177.shtml  
  HTTP 404
- gone: https://www.enbw.com/media/konzern/docs/energieerzeugung/broschuere-rheinhafen-dampfkraftwerk-karlsruhe.pdf  
  HTTP 404
- value_missing: https://www.enbw.com/media/konzern/docs/energieerzeugung/rdk9-epl-praesentation-foeb-fachveranstaltung-buergerinformation.pdf  
  missing expected content: ['2030']
- value_missing: https://www.enbw.com/presse/letzte-kohle-verlaesst-walheim-abtransport-juni-2025.html  
  missing expected content: ['Gasturbine']
- PASS: https://www.energate-messenger.de/news/131050/statkraft-legt-zweites-kraftwerk-still  
  OK
- PASS: https://www.energate-messenger.de/news/137928/dow-nimmt-gaskraftwerk-in-betrieb  
  OK
- PASS: https://www.energate-messenger.de/news/148004/pq-energy-plant-drei-gaskraftwerke-in-deutschland  
  OK
- PASS: https://www.energate-messenger.de/news/184324/dessau-stellt-fernwaermesystem-auf-erdgas-um  
  OK
- PASS: https://www.energate-messenger.de/news/192466/auew-kombiniert-batterie-mit-gasturbine  
  OK
- PASS: https://www.energate-messenger.de/news/77693/stadtwerke-bielefeld-nehmen-gud-kraftwerk-in-betrieb  
  OK
- dead_host: https://www.energie-und-management.de/nachrichten/energieerzeugung/detail/uniper-will-kraftwerk-mit-gas-statt-kohle-betreiben-240202  
  HTTP 000; Wayback snapshot 20251011170833 and 1 older snapshot(s) missing expected content: ['Dampfturbin']
- value_missing: https://www.energie.de/euroheatpower/news-detailansicht/nsctrl/detail/News/stadtwerke-flensburg-nehmen-auf-dem-weg-zur-klimaneutralitaet-kessel-13-in-betrieb  
  missing expected content: ['Siemens-Gasturbine']
- value_missing: https://www.energiejobs.de/news/ticker/brennstoffwechsel-im-kraftwerk-muenchen-nord-stadtwerke-muenchen-stellen-heizkraftwerk-jetzt-von-kohle-auf-gas-um-artikel6530  
  missing expected content: ['2035']
- gone: https://www.energy-saxony.net/aktuelles/eins-nimmt-motorenheizkraftwerke-in-betrieb.html  
  HTTP 404
- value_missing: https://www.entwicklungsstadt.de/heizkraftwerk-charlottenburg-genehmigung-fuer-neue-gasturbinen-ab-2028/  
  missing expected content: ['Spreebord']
- value_missing: https://www.eza-allgaeu.de/bau-energieberatung/fachleute-finden/detail/partner-37/  
  missing expected content: ['1988']
- value_missing: https://www.fernwaerme-ulm.de/energie/erzeugungsanlagen/hkw-magirusstrasse/  
  missing expected content: ['BHKW']
- value_missing: https://www.foerde.news/news/herzstueck-der-neuen-gas-und-dampfturbinenanlage-der-stadtwerke-flensburg-ist-da.html  
  missing expected content: ['SGT']
- server_error: https://www.hamburger-energiewerke.de/ueber-uns/presse/mehrarbeiten-bei-gas-und-dampfturbinen-anlage-dradenau-notwendig  
  HTTP 500
- value_missing: https://www.ihk.de/hamburg/produktmarken/beratung-service/innovation/umweltberatung/stoerfallbetriebe-hamburg/betriebe-a-z/vattenfall-waerme-hamburg-3698744  
  missing expected content: ['Billbrook']
- value_missing: https://www.industriepark-hoechst.com/en/stp/site/site-services/energy/products-and-solutions-for-utilities/heat/  
  missing expected content: ['gas turbine']
- value_missing: https://www.infraserv.com/de/unternehmen/nachhaltigkeit/gasturbinen/  
  missing expected content: ['Infraserv GmbH & Co. Höchst KG']
- server_error: https://www.infraserv.com/de_1/aktuelles/pressemeldungen/pressemeldung.html?lang=de&nach_id=19221  
  HTTP 500; no Wayback snapshot to verify against
- server_error: https://www.infraserv.com/en_1/aktuelles/pressemeldungen/pressemeldung.html?lang=en&nach_id=5210  
  HTTP 500; no Wayback snapshot to verify against
- value_missing: https://www.ingenieur.de/technik/fachbereiche/energie/allgaeuer-hybridkraftwerk-mit-der-lizenz-zu-regeln/  
  missing expected content: ['Waltenhofen']
- value_missing: https://www.iqony.energy/en/reuther-west  
  missing expected content: ['Reuter']
- value_missing: https://www.iqony.energy/h2-ready-gaskraftwerke  
  missing expected content: ['Bexbach']
- value_missing: https://www.iqony.energy/newsroom/zweiter-oeffentlichkeitsdialog-neue-gasleitung-zum-kraftwerk  
  missing expected content: ['2027']
- value_missing: https://www.jaeger-ingenieure.de/news/motorenheizkraftwerke-eins-energie-chemnitz.html  
  missing expected content: ['Furth']
- gone: https://www.kmw-ag.de/zkw-in-planung/  
  HTTP 404
- dead_host: https://www.kraftwerk-saarbruecken.com/  
  HTTP 000
- dead_host: https://www.kraftwerk-saarbruecken.com/heizkraftwerk-heute/das-kraftwerk-saarbruecken/  
  HTTP 000
- gone: https://www.leag.de/de/gigawattfactory/innovationskraftwerk/  
  HTTP 404
- value_missing: https://www.mainova.de/de/ihre-mainova/presse/pressemitteilungen/2023/bau-des-gemeinschaftskraftwerks-hanau-fuer-kuenftige-fernwaermeversorgung-der-stadt-startet-124516  
  missing expected content: ['Gasmotoren']
- value_missing: https://www.mainova.de/de/ihre-mainova/ueber-uns/waerme-stromversorgung/kohleersatzprojekt-hkw-west  
  missing expected content: ['Herbst']
- value_missing: https://www.man-es.com/de/unternehmen/pressemitteilungen/press-details/2019/08/21/man-energy-solutions-baut-zwei-heizkraftwerke-in-chemnitz  
  missing expected content: ['Furth', 'Nord I']
- value_missing: https://www.man-es.com/de/unternehmen/pressemitteilungen/press-details/2022/03/17/neues-heizkraftwerk-in-frankfurt-(oder)-spart-50.000-tonnen-co2-j%C3%A4hrlich  
  missing expected content: ['Stadtwerke Frankfurt', 'Gasmotor']
- value_missing: https://www.oeko.de/fileadmin/oekodoc/Hintergrundinformationen_HKW-Muenchen-Nord_Update.pdf  
  missing expected content: ['Siemens']
- dead_host: https://www.pq-energy.com/en/projects.html  
  HTTP 000; the live page is gone, but the archived copy https://web.archive.org/web/20210123230940/http://pq-energy.com/en/projects.html still shows the value. Cite that archived address (verify it directly) or a live copy of the document
- value_missing: https://www.pv-magazine.de/2019/06/17/zulassung-fuer-regelenergiemarkt-fuer-hybridkraftwerk-aus-grossspeicher-und-gasturbine/  
  missing expected content: ['Waltenhofen']
- value_missing: https://www.qcintel.com/hydrogen/article/bavaria-backs-new-800-mw-gas-plant-at-zolling-highlights-hydrogen-push-64366.html  
  missing expected content: ['2031']
- PASS: https://www.regierung-schwaben.bayern.de/aufgaben/info_sachgebiete/55-1gasmotor/index.html  
  OK
- PASS: https://www.regierung.schwaben.bayern.de/aufgaben/info_sachgebiete/55-1gasmotor/index.html  
  OK
- gone: https://www.saarbruecker-stadtwerke.de/energie/die_energieerzeugung_der_sw  
  HTTP 404
- server_error: https://www.saarland.ihk.de/p/1._Spatenstich_f%C3%BCr_den_Bau_des_neuen_Gichtgaskraftwerks_in_Dillingen-23-4126.html  
  HTTP 400; no Wayback snapshot to verify against
- value_missing: https://www.solar-professionell.de/2019/06/27/deutschlands-erstes-hybridkraftwerk-mit-genehmigung-zum-regelbetrieb/  
  missing expected content: ['Waltenhofen']
- value_missing: https://www.stadt-und-werk.de/k21-meldungen/erneuerung-des-kraftwerkparks/  
  missing expected content: ['SGT']
- value_missing: https://www.stadt-und-werk.de/k21-meldungen/kessel-12-rollt-an/  
  missing expected content: ['Kessel 7']
- gone: https://www.stadtwerke-duisburg.de/unternehmen/daten-fakten/  
  HTTP 404
- gone: https://www.stadtwerke-ffo.de/2022/  
  HTTP 404; no Wayback snapshot to verify against
- value_missing: https://www.stadtwerke-flensburg.de/foerdepost/presse/inbetriebnahme-k13  
  missing expected content: ['Siemens', 'SGT']
- gone: https://www.statkraft.com/about-statkraft/where-we-operate/germany/emden-gas-fired-power-plant/  
  HTTP 404
- value_missing: https://www.statkraft.de/ueber-statkraft/standorte/Knapsack-Gaskraftwerk/  
  missing expected content: ['120 MW']
- value_missing: https://www.statkraft.de/ueber-statkraft/standorte/Landesbergen-Gaskraftwerk/  
  missing expected content: ['Kapazitätsreserve']
- gone: https://www.suedkurier.de/region/nachbarschaft/freiburg/Warum-das-Heizkraftwerk-der-Uniklinik-Freiburg-aufruestet  
  HTTP 404
- value_missing: https://www.swb.de/ueber-swb/unternehmen/nachhaltigkeit/bhkw-hastedt  
  missing expected content: ['SWB Erzeugung']
- value_missing: https://www.sweco-gmbh.de/showroom/gas-oel-reservekraftwerk-gundelfingen/  
  missing expected content: ['Gundelfingen', '2020']
- gone: https://www.swm.de/presse/pressemitteilungen/2024/04-2024/swm-hkw-nord  
  soft-error page (title: '404 – Seite nicht gefunden')
- value_missing: https://www.trianel-hamm.de/pressemeldungen/trianel-gaskraftwerk-hamm-soll-um-einen-dritten-wasserstofffaehigen-kraftwerksblock-ergaenzt-werden  
  missing expected content: ['500 Megawatt']
- gone: https://www.umweltbundesamt.de/sites/default/files/medien/384/bilder/dateien/4_tab_genehmigte-in_genehmigung-kraftwerksprojekte_2019-04-04.pdf  
  HTTP 404
- bot_wall: https://www.uniper.energy/system/files/2026-03/2026_03_11_FY_2025_Uniper_List_of_Assets_Edition_2025.pdf  
  HTTP 403
- rate_limited: https://www.uvp-verbund.de/documents-ige-ng/igc_by/33fa0692-a59a-4846-ade5-47101d836eda/2023-09-26%20Genehmigungsbescheid_Zolling.pdf  
  HTTP 429
- PASS: https://www.uvp-verbund.de/documents-ige-ng/igc_ni/8aa50135-8a84-4107-8510-4ef885430b90/Bek.%20lang.pdf  
  OK (via disk_cache)
- PASS: https://www.uvp-verbund.de/documents-ige-ng/igc_sn/1d802955-e253-435f-8bf8-ecde4471591f/2022_11-08_Bekanntmachung%20Auslegung%20E%C3%96T%20GV%20EVC%202.pdf  
  OK
- rate_limited: https://www.uvp-verbund.de/documents-ige-ng/igc_sn/64322a9b-6fd6-48ad-874c-5127ccbe0ad2/GuD%20Lippendorf%20Bekanntmachung%20Entscheidung%20Amtsblatt.pdf  
  HTTP 429
- PASS: https://www.uvp-verbund.de/documents-ige-ng/igc_sn/a56b4d10-6aa9-41ec-85b9-a7283d8661f9/Bekanntmachung%20Bescheid_1.TG%20EVC%203.docx.pdf  
  OK
- rate_limited: https://www.uvp-verbund.de/documents-ige-ng/igc_st/f530c838-ed0a-4df4-8f86-b24ab6b0c123/ZESA_1TG_13_b_UVP_Bericht_Saale_Energie_Schkopau_Rev01_250702.pdf  
  HTTP 429
- PASS: https://www.uvp-verbund.de/trefferanzeige?docuuid=43E46C3F-F2A3-493A-9520-6DD9474EE0F1&plugid=%2Fingrid-group%3Aige-iplug-hb  
  OK
- PASS: https://www.uvp-verbund.de/trefferanzeige?docuuid=517d7250-56d8-4989-b364-4c1f64c8e319  
  OK
- PASS: https://www.uvp-verbund.de/trefferanzeige?docuuid=59b969fd-2031-40ce-8d88-cbc3846e7a08  
  OK
- rate_limited: https://www.uvp-verbund.de/trefferanzeige?docuuid=64322a9b-6fd6-48ad-874c-5127ccbe0ad2  
  HTTP 429
- PASS: https://www.uvp-verbund.de/trefferanzeige?docuuid=8aa50135-8a84-4107-8510-4ef885430b90&rstart=380&currentSelectorPage=1  
  OK (via rate_limit_wait)
- PASS: https://www.uvp-verbund.de/trefferanzeige?docuuid=8aa50135-8a84-4107-8510-4ef885430b90&rstart=380&currentSelectorPage=1&f=  
  OK
- PASS: https://www.uvp-verbund.de/trefferanzeige?docuuid=B9CFC7FE-09DF-4F29-B6BF-8087F73D4291&plugid=/ingrid-group:ige-iplug-hh  
  OK
- PASS: https://www.uvp-verbund.de/trefferanzeige?docuuid=E6D6C369-C231-4076-88ED-268BF5B86F4D  
  OK
- value_missing: https://www.volkswagen-group.com/en/press-releases/volkswagen-group-realigns-energy-supplies-company-power-stations-to-change-over-from-coal-to-gas-16552  
  missing expected content: ['Wolfsburg site']
- gone: https://www.volkswagen-newsroom.com/en/press-releases/volkswagen-group-realigns-energy-supplies-company-power-stations-to-change-over-from-coal-to-gas-2108  
  HTTP 404
- PASS: https://www.waz-online.de/lokales/wolfsburg/vw-kraftwerk-wolfsburgs-wahrzeichen-laeuft-jetzt-mit-erdgas-PNMXZKRB7DD6FVZPIIMNCRXV6E.html  
  OK
- value_missing: https://www.wirtschaft-regional.net/stadtwerke-bielefeld-und-mitsubishi-hitec-paper-setzen-erfolgreiche-zusammenarbeit-fort/  
  missing expected content: ['Niedernholz']
- value_missing: https://www.zfk.de/energie/waerme/hamburger-energiewerke-gas-und-dampfturbinen-wurden-angeliefert  
  missing expected content: ['180 Megawatt']
