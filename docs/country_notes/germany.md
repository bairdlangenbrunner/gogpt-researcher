# Germany

The fleet is well documented. The federal regulator, the Bundesnetzagentur, publishes a
plant list built from the national unit register. Its status vocabulary has to be
mapped onto GEM statuses, and that mapping is the single most important step for
this country. GEM tracks units of 20 MW or more in Germany (EU threshold).

## Regulator and official sources

### Bundesnetzagentur Kraftwerksliste (power plant list)

- Landing page: https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/Versorgungssicherheit/Erzeugungskapazitaeten/Kraftwerksliste/start.html
- Excel: https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/Versorgungssicherheit/Erzeugungskapazitaeten/Kraftwerksliste/_DL/Kraftwerksliste.xlsx?__blob=publicationFile
- CSV: https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/Versorgungssicherheit/Erzeugungskapazitaeten/Kraftwerksliste/_DL/Kraftwerksliste_CSV.csv?__blob=publicationFile
- Data date of the edition checked on 2026-10-05: 26 June 2026 (page says Stand 10.07.2026). A new edition replaces the file at the same URL, so record the data date in the note when citing it.
- Built from the Marktstammdatenregister. Single rows exist for sites of 10 MW net or more; smaller units are summed by state and fuel (rows of type Kleinanlagen_aggregiert, ignore them).
- Sheet "Gesamtkraftwerksliste", header on row 8. Useful columns: EinheitMastrNummer, Anlagenbetreiber (operator), Anzeigename (plant or unit name), Bundesland, Jahr_Inbetriebnahme (start year), Jahr_Stilllegung (closure year), Kraftwerksstatus, Energietraeger (fuel; gas rows have the value Erdgas), Hauptbrennstoff, Waermeauskopplung_KWK (combined heat and power flag), Bruttoleistung_MW, Nettonennleistung_MW, Technologie_Stromerzeugung.
- Gas rows in the June 2026 edition: 937, of which 360 are 20 MW net or more. Technology values: Verbrennungsmotor (engine), GasturbinenmitAbhitzekessel (gas turbine with heat recovery), GasturbinenmitnachgeschalteterDampfturbine (combined cycle), GasturbinenohneAbhitzekessel (simple cycle), GegendruckmaschinemitEntnahme (steam turbine).
- The file has years only, no exact dates. Capacity: GEM records nameplate generating capacity, so Bruttoleistung_MW is the closer figure; note which column a value came from.
- Download the Excel once per batch into the batch work directory and read it with pandas; do not fetch it per unit.

### Status mapping, June 2026 vocabulary

The exact strings in the Kraftwerksstatus column (capitalization is inconsistent, match exactly):

| Bundesnetzagentur status | GEM status | Note |
|---|---|---|
| InBetrieb | operating | |
| vorläufig Stillgelegt | operating | provisional closure notified under section 13b of the energy law; the plant can still return. GEM's team mapping keeps it as operating. Confirm with a second source before any change. |
| Netzreserve aufgrund § 13b EnWG | operating | grid reserve; the regulator stops the closure |
| Kapazitätsreserve aufgrund von § 13e EnWG | operating | capacity reserve outside the market; by analogy with the grid reserve. Not in the older GEM team mapping; see open items. |
| besonderes netztechnisches Betriebsmittel | operating | grid stability plants built for the transmission operators (Biblis, Irsching 6, Marbach, Leipheim); run only on instruction. Not in the older mapping; see open items. |
| endgültig stillgelegt ohne § 13b EnWG oder KVBG | retired | retired year from Jahr_Stilllegung |
| endgültig stillgelegt nach § 13b EnWG | retired | same |
| endgültig stillgelegt nach KVBG | retired | coal exit law; coal only |
| Netzreserve aufgrund von KVBG | coal only | |
| zeitl. gestreckte Stilllegung aufgrund § 50 KVBG | coal only | |

The older strings in GEM's team document (saisonale Konservierung, Sicherheitsbereitschaft, Sonderfall, gesetzlich an Stilllegung gehindert) no longer appear in the file. The older document mapped all of them to operating except the coal-only ones, which is consistent with the table above.

### Bundesnetzagentur Zu- und Rückbau (additions and dismantling)

- Excel: https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/Versorgungssicherheit/Erzeugungskapazitaeten/Kraftwerksliste/_DL/ZuUndRueckbau.xlsx?__blob=publicationFile
- Same data date as the plant list. Sheet 1 gives expected additions by fuel and year (June 2026 edition: 1,890 MW of gas in 2026 and 13 MW in 2027, from units under construction or in trial operation reported under section 35 of the energy law). Sheet 2 lists expected additions and closures unit by unit for sites of 10 MW net or more, with the register number where one exists. This is the best official check for construction and planned retirement statuses.

### Marktstammdatenregister (MaStR, national unit register)

- Public search with filters, no login: https://www.marktstammdatenregister.de/MaStR/Einheit/Einheiten/ErweiterteOeffentlicheEinheitenuebersicht
- Fields: Betriebs-Status, Energieträger, Bruttoleistung der Einheit, Nettonennleistung der Einheit, Inbetriebnahmedatum der Einheit (exact commissioning date), Datum der geplanten Inbetriebnahme (planned commissioning date, present on planned units), Datum der endgültigen Stilllegung, Technologie der Stromerzeugung, Name des Anlagenbetreibers, MaStR-Nr. der Einheit.
- The register gives exact dates where the Bundesnetzagentur list gives years, and it lists planned units (status In Planung) that the plant list leaves out. A unit page URL is a citable source once the value is on the page.
- Full data dump, no login, XML zip refreshed daily: https://www.marktstammdatenregister.de/MaStR/Datendownload (format changed on 1 October 2025). Only worth it for a whole-country pass.

### Netzentwicklungsplan Strom (grid development plan)

- Approval of the Szenariorahmen 2025 for the 2037/2045 plan, 30 April 2025: https://www.netzentwicklungsplan.de/sites/default/files/2025-04/Genehmigung%20Szenariorahmen%202025_0.pdf
- Kraftwerksliste zum Szenariorahmen: https://www.netzentwicklungsplan.de/sites/default/files/2025-05/Kraftwerksliste_Szenariorahmen_0.xlsx
- Anlage 1 (plant sites by state and scenario, no names): weak for plant identity, only useful for totals.
- The Gas NDP scenario framework's appendix "List of gas power plants" draws on BDEW, Bundesnetzagentur, Prognos and transmission operator data and includes some plants absent from the plant list (Hagen-Kabel was the example in GEM's team document).

## The 2026 capacity tenders (StromVKG)

- The law is the Strom-Versorgungssicherheits- und Kapazitätengesetz (StromVKG), passed by the Bundestag on 9 July 2026 and the Bundesrat on 10 July 2026, signed 21 July 2026, state aid approved by the European Commission on 2 September 2026. Text: https://www.gesetze-im-internet.de/stromvkg/BJNR0D2AB0026.html. The 2024 draft was called Kraftwerkssicherheitsgesetz (KWSG); that name only helps for older articles. The policy umbrella is the Kraftwerksstrategie.
- The Bundesnetzagentur runs the auctions. Rounds written into the law: long-duration capacity (section 4) on 8 September 2026 and 29 December 2026, 4,500 MW of derated capacity each (gas plants are derated by 0.85, so about 5.3 GW of nameplate per round); technology-open generation capacity (section 5) on 18 May 2027, 2,000 MW; a capacity market (section 6) from 1 December 2027. Fifteen-year obligation, price cap 244,000 euros per MW per year, a hydrogen conversion concept is required from each bidder.
- First-round notice: https://www.bundesnetzagentur.de/1111198. Press release of 21 July 2026: https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/DE/2026/20260721_StromVKG.html. The September round was reported oversubscribed (iwr.de, 10 September 2026); awards are due by 3 November 2026 and no award list existed on 2026-10-05. Check the tenders page for results: https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/Ausschreibungen/start.html
- What an award means for GEM: a Zuschlag (award) is a strong signal of a real project but is not construction. A project with an award and no permit stays announced or pre-construction per the lifecycle rules. An award is recent activity, so it goes in the note and in Status Detail with the Bundesnetzagentur list as the source, not in Latest Activity, which is only for projects with no report in the last year. Bidders usually announce their own bids and awards in press releases, which are the per-plant sources.
- Keep tender projects separate from the other growth stories: municipal combined heat and power and district heating plants (Heizkraftwerk, often under 100 MW, utility press releases), industrial captive plants (chemical parks, paper mills, refineries), and data-center backup or peaking plants (Mainz KMW, Frankfurt). Each class has its own sources and its own capacity-threshold risk.

## Transmission operators and market data

- Transmission operators: 50Hertz, Amprion, TenneT, TransnetBW. Their grid reserve (Netzreserve) determinations and the joint Bundesnetzagentur reserve reports name plants held back from closure.
- ENTSO-E Transparency, installed capacity per production unit (Germany units of 100 MW or more): https://transparency.entsoe.eu/generation/r2/installedCapacityPerProductionUnit/show (script-driven page; bulk download may need a free account).

## Permit register (environmental impact assessments)

- The register of environmental impact assessments (UVP-Verbund) is the primary source for planned plants. Each permit procedure has one page with the applicant, the project description with capacity, the dated procedure steps, and the documents: public notice, permit decision, environmental report.
- Addresses: `https://www.uvp-verbund.de/trefferanzeige?docuuid=<ID>` for a procedure and `https://www.uvp-verbund.de/documents-ige-ng/igc_<state>/<ID>/<file>.pdf` for a document. The state front ends (`uvp.niedersachsen.de`, `www.uvp.sachsen.de` and the like) are the same server and the same pages. Bavaria, Hesse and North Rhine-Westphalia also publish on their own state portals.
- The server answers "429 Too Many Requests" to about six of every seven requests, however slowly they are sent. This is a throttle, not a block. `fetch.py` and `url_verifier.py` now wait and retry until the page comes (one to eight minutes per address), let only one request at a time go to the server, and keep every page and PDF in `work/fetch_cache/` for 30 days so a second read is instant.
- Because each read is slow, collect the files before the research starts: `python scripts/harvest_permits.py --scope germany` (runs for hours; start it in the background). It writes one summary per plant to `work/permits/germany/<plant id>.md` with the procedure title, dates, capacity lines and the links, and it warms the cache for the research agents.
- The register's own search only lists procedures that are still open. A closed procedure, such as the Mehrum gas plant preliminary decision, stays online at its direct address but the search does not find it. Find those addresses with a web search for the town and "uvp-verbund.de", then pass them in with `--seed <plant id>=<ID>`. Check each seed against the plant first: in October 2026 three seeds were look-alike projects elsewhere (an RWE engine plant at Hürth under Gundremmingen, Herne under Staudinger, Herdecke under Voerde). The summary now flags a seeded procedure that names neither the plant's town nor the plant.
- Some procedure pages show only "Keine Detailinformationen verfügbar" (no detail information), even after the throttle lets the request through. Lippendorf's combined cycle permit is one. These empty pages are never cached. Look for the same notice where it is re-posted, as below.
- Every permit notice is also published by the permit authority and often by the town. Their sites do not throttle. Search the web for the plant's town with "Bekanntmachung" and "BImSchG", or for a register document's exact file name. Hosts that carried copies in October 2026:
  - Saxony: lds.sachsen.de/bekanntmachung (Saxony state directorate, a rolling list that drops old notices), the Saxony gazette on recht-sachsen.de, and town sites such as neukieritzsch.de (the Lippendorf permit notice of 22 August 2024).
  - Saxony-Anhalt: lvwa.sachsen-anhalt.de notices by month, and presse.sachsen-anhalt.de (the Schkopau decision of 18 March 2026).
  - Hesse: rp-darmstadt.hessen.de (Staudinger, Hanau).
  - Baden-Württemberg: rp.baden-wuerttemberg.de and the town sites, such as heilbronn.de.
  - Bavaria: each district government's project pages, such as regierung-schwaben.bayern.de (Gundremmingen) and regierung.oberbayern.bayern.de (Ingolstadt).
  - North Rhine-Westphalia: the district governments, such as brd.nrw.de (Voerde). Their notices come down after the display period.
- Never report a permit page as blocked after one refused read. Never read these pages "by hand" as a substitute; the retry gets them.

## Site access

What each German source needed in October 2026. The general playbook is `docs/reference/site_access.md`.

- The permit register throttles almost everything. See the section above.
- energate-messenger.de sets a browser puzzle on the first visit. `fetch.py` opens it in Chrome once and then reads the teaser pages with the earned cookie. The full article text needs a free energate account. Once Baird signs in with `python scripts/cf_clearance.py --login https://www.energate-messenger.de/`, every later fetch reads the full text.
- waz.de and waz-online.de use the DataDome bot check. Chrome passes it once and plain fetches reuse the cookie.
- chemieindustrie-online.de refuses plain requests with "406 Not Acceptable" and accepts the Chrome network fingerprint.
- District government notices (bra.nrw.de and the like) are taken down after the display period and then answer 403 or 404. The same documents are usually in the permit register, and the register's documents are usually on a town or authority site. Each is a way in when the other fails.
- waerme.hamburg and hamburger-energiewerke.de block requests from outside Germany, even from a real browser. Use the archive, or a German connection through the `https_proxy` setting.
- Old company domains are gone: pressearchiv.steag.com (Steag is now Iqony), kraftwerk-saarbruecken.com and pq-energy.com. The archive has some of their pages. The Saarbrücken plant pages now live on energie-saarlorlux.com under "kraftwerke". For the Steag Leverkusen deal, the law firm CMS's announcement on cms.law states the 570 MW. For PQ Energy's Gundelfingen project, the Swabia regional government's planning report and the energate article both work.
- infraserv.com rebuilt its site. Old press release addresses with "nach_id" answer with a server error; the same releases are now under infraserv.com/de/medien/pressemeldungen/. The old saarland.ihk.de page on the 2007 groundbreaking of the Dillingen blast furnace gas plant has no live or archived copy; the date still needs a source.
- Dradenau in Hamburg: 180 MW is the electric maximum (290 MW thermal), per a ZfK article on the turbine delivery. Use that when the Hamburg sites are blocked.
- Live replacements found on 6 October 2026, each checked with `url_verifier.py`:
  - Infraserv gas turbines at Höchst: https://www.infraserv.com/de/medien/pressemeldungen/pressemeldung-nc_56326.html
  - Steag Leverkusen 570 MW: https://cms.law/de/deu/news-information/cms-begleitet-steag-erfolgreich-beim-kauf-eines-grosskraftwerkprojekts
  - Saarbrücken Römerbrücke: https://www.energie-saarlorlux.com/kraftwerke/standort-roemerbruecke/geschichte/
  - PQ Energy Gundelfingen: https://www.energate-messenger.de/news/148004/pq-energy-plant-drei-gaskraftwerke-in-deutschland
  - Kempten Veits gas turbine of 1988, replacing the gone 100jahre.auew.de: http://www.kreisbote.de/lokales/kempten/stadtgeschichte-kempten-seit-ueber-100-jahren-versorgt-das-auew-kempten-mit-strom-und-kann-auf-eine-bewegte-geschichte-blicken-teil-13815990.html
  - Dradenau 180 MW: https://www.zfk.de/energie/waerme/hamburger-energiewerke-gas-und-dampfturbinen-wurden-angeliefert
  - Dillingen: the ROGESA environment page states the 90 MW blast furnace gas plant but not the 2007 groundbreaking.

## Key operators

- Uniper publishes a yearly "List of Assets". Edition 2025 (status 31 December 2025): https://www.uniper.energy/system/files/2026-09/2026_11_03_FY_2025_Uniper_List_of_Assets_Edition_2025.pdf. Uniper moves this file when it reissues it, and the old address then answers "Access denied" instead of "not found". If the link fails, open https://www.uniper.energy/investors/reports-and-presentations through `fetch.py` and take the current "List of Assets" link from that page. The Uniper site needs the browser-fingerprint route, which `fetch.py` uses on its own.
- Others with useful per-plant pages: RWE (Biblis, Gersteinwerk, Weisweiler, Voerde), EnBW (RDK Karlsruhe, Altbach, Heilbronn, Stuttgart-Münster), LEAG (Jänschwalde, Schwarze Pumpe, Lippendorf), Steag/Iqony (Völklingen, Bexbach, Quierschied), Trianel (Hamm), municipal utilities (Mainova, MVV, Stadtwerke München, enercity, swb, SachsenEnergie).

## Trade press

- iwr.de: free, readable in full, good on the tenders.
- zfk.de and energie-und-management.de: mixed free and paid articles.
- montelnews.com/de and energate-messenger.de: subscription; headlines only. energate needs Chrome on the first visit and a free account for full text (see Site access).
- Local newspapers and the operator's own press releases are usually the per-plant sources.

## German search vocabulary

Kraftwerk, Gaskraftwerk, Heizkraftwerk (combined heat and power plant), GuD-Kraftwerk (combined cycle), Gasturbine, Gasmotor or Blockheizkraftwerk (engine plant), Erdgas, Inbetriebnahme (commissioning), Baubeginn (start of construction), Genehmigung (permit, often under the BImSchG emissions law), Stilllegung (closure), Netzreserve, Kapazitätsreserve, Systemrelevanz, Kraftwerksstrategie, StromVKG, Ausschreibung, Zuschlag, Wasserstofffähigkeit or wasserstofffähig (hydrogen ready), Fernwärme (district heating), Rechenzentrum (data center).

## Older sources

- Gasturbinen-Kenndaten (ASUE, 2006): https://asue.de/sites/default/files/asue/themen/gasturbinen/2006/broschueren/11_05_06_gasturbinenkenndaten_01.pdf. A table of industrial gas turbine units. Dated; a lead to confirm, never a current-status source.

## Research tips

- Start with the Kraftwerksliste for the operating fleet and the retired year, then the Zu- und Rückbau file for construction and planned closures, then the register for exact dates and planned units, then the owner's own pages.
- Match plants by Anlagenbetreiber plus Bundesland plus capacity, not by name alone. GEM plant names are English translations and often differ from Anzeigename.
- A unit in the grid reserve or capacity reserve is operating in GEM terms. Note the reserve in Status Detail.
- Combined heat and power plants report electric capacity (Nettonennleistung or Bruttoleistung) and thermal output separately; record electric only.

## Gotchas

- The status mapping table is load bearing. Coding vorläufig Stillgelegt, Netzreserve or Kapazitätsreserve as anything but operating would misclassify plants the regulator still counts as available.
- The Bundesnetzagentur list changes its status vocabulary between editions (three categories from the older GEM mapping are gone, three are new). Re-read the distinct values of the status column every batch.
- The plant list has no planned units. Planned and under-construction units come from the Zu- und Rückbau file, the register's In Planung rows, and the owners.

## Open items

- Confirm with the GOGPT leads that Kapazitätsreserve and besonderes netztechnisches Betriebsmittel map to operating (the table above does this by analogy with the grid reserve).
- Ask Dan O'Beirne whether the Beyond Fossil Fuels dataset and the GEM to BFF id mapping may be used as a source.
- After 3 November 2026: read the first StromVKG award list and compare against GEM's in-development units.
- Whether the register's public CSV export has a row limit without login.

## Update notes

- 2026-10-05, from the first Germany batch (`batches/germany/INDEX.md`): the countrywide check of the June 2026 power plant list against GEM found no gas plant of 20 MW or more missing. Mukran (Rügen) is the 39.9 MW of engines on the floating regasification ship Neptune, not a shore plant, so it is out of scope; the batch carries it as a question. The register's status column mapped cleanly with the table above. The permit register refused most reads in that batch; the fix is in "Permit register" above.
- 2026-10-05: full refresh before the Germany update batch (Baird, with a source check by a research agent). Replaced the status mapping with the June 2026 vocabulary, added the register, the Zu- und Rückbau file, the StromVKG tenders, transmission operators, trade press and the German search vocabulary.
- 2026-07-27: seeded from GEM's team-wide "Gas/oil power plant data sources - by country" document, including the older status mapping.
