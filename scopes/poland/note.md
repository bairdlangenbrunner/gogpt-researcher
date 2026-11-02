# Poland

Scope: 60 unit rows across 45 plants in the pull of 2026-10-29 at 14:51 Eastern. 30 units are operating, 13 pre-construction, 11 under construction, 4 announced, 1 shelved and 1 cancelled by inference. Assigned to Dan O'Beirne for the Q4 2026 cycle (Poland week 2026-11-09 to 11-13, high priority, 28 units in development, 11,587 MW). GEM tracks units of 20 MW or more in Poland (EU threshold). Last Updated is mostly May 2023 and October 2025, so most rows have not been touched in a year or more.

## Country context

- The grid operator is PSE (Polskie Sieci Elektroenergetyczne). It runs the transmission grid and the capacity market (rynek mocy). Distribution companies are Energa, Enea, PGE Dystrybucja, Tauron and Stoen. Large units connect to PSE; gas engines at city heat plants usually connect to a distribution company.
- The energy regulator is URE (Urząd Regulacji Energetyki). It grants generation licenses (koncesje) and publishes the final capacity auction results.
- Environmental decisions (decyzja o środowiskowych uwarunkowaniach) are issued by the city or town head for most plants, by a regional environment office (RDOŚ) for some, and by the national office (GDOŚ) for a few. Integrated permits (pozwolenie zintegrowane) for plants of 50 MW thermal input or more are issued by the regional marshal's office and posted on its public information site (BIP).
- The big state groups own nearly every project: PGE (and PGE Energia Ciepła for heat plants), Orlen (with Energa and Orlen Termika), Enea, Tauron. Private owners include Veolia, Fortum, CEZ, Synthos, KGHM and Polenergia. Grupa Azoty and Orlen run captive plants at chemical and refinery sites.
- New gas plants come from two drivers: coal-to-gas replacement at heat plants (gas engine sets of 20 to 140 MW) and large combined cycle units of 500 to 900 MW on capacity contracts. A new unit on a 15 or 17 year capacity contract is almost always a new build.
- Coal is still most of the fleet. The unfiltered export has 232 coal rows in Poland and 25 rows linked to a conversion. Gas units built next to a coal plant (Rybnik, Kozienice, Dolna Odra, Ostrołęka, Połaniec, Łagisza) are the common case.

## Sources that work (probed 2026-10-29)

- **PSE connection list**: https://www.pse.pl/documents/20182/51490/Informacje_publikowane_zgodnie_z_Art_7_ust_8l_ustawy_PE.xlsx. A spreadsheet of every project asking to connect to the PSE grid, published under article 7 section 8l of the Energy Law (in force 30 April 2026). The edition of 26 October 2026 covers 30 September 2026 and has 890 rows. Gas type codes are `BG` (gas block), `BGP` (combined cycle), `SG` (gas engines) and `JS` (combustion unit). The file name never changes, so save a dated copy every run. Plain download, no login.
- **Capacity auction results**: https://www.pse.pl/aukcje-mocy and the archive page link one page per delivery year (`https://www.pse.pl/aukcja-glowna-na-rok-dostaw-YYYY`, 2021 to 2030). Each links text PDFs; the final results are URE's "Informacja ... ostateczne wyniki". Rows give a unit code (`JRM/601`), new, upgraded or existing, MW, contract years and the supplier. There is no fuel column; unit names appear only from the 2028 auction. Scrape the links from each page because file names are not regular.
- **Integrated permits**: each marshal's office BIP. Kujawsko-Pomorskie lists them at https://bip.kujawsko-pomorskie.pl/4416/srodowisko-pozwolenia-zintegrowane-dla-instalacji-przemyslowych.html; the CCGT Grudziądz permit of 30 June 2026 (563.34 MW electric) is a plain PDF there.
- **gov.pl search**: `https://www.gov.pl/api/data/search?query=<words>&offset=0&limit=20` returns JSON for every gov.pl page, including the RDOŚ and GDOŚ decision notices. Search by a short plant or town name and keep results under `/web/rdos-`, `/web/gdos` and `/web/rozwoj-technologia`. Attachments under `https://www.gov.pl/attachment/<id>` are PDF or Word files.
- **Ekoportal list of environmental documents**: `https://wykaz.ekoportal.pl/apiv1/cards/<page>` with filters for district, municipality, document type and year. Metadata only, no document links, newest card seen July 2025. Use it to find a decision's case number and office, then get the document from that office.
- **EU industrial emissions data (European Environment Agency)**: the large combustion plant tables (version 16, 25 September 2026) give each plant's capacity in MW thermal and its gas use in each year to 2024, with coordinates. A good list of existing gas plants to check GEM against. Planned plants are not in it.
- **PSE open data**: `https://api.raporty.pse.pl/api/gen-jw` gives output per unit every 15 minutes, no token. No fuel and no nameplate, but a unit producing power is evidence it is operating.
- **ENTSO-E installed capacity per production unit** (European grid operators' transparency platform): units of 100 MW and up with type and MW. The API needs a token; Baird is registering one (store it as `ENTSOE_API_TOKEN`, never in the repo).

## Sources still to crack

- **URE register site** https://rejestry.ure.gov.pl/ returned errors and resets on 2026-10-29 on every fetch route and in the Wayback lookup. Retry with a slower pace and a full browser load; it holds the generation license list. Not blocked until the whole ladder fails on a second day.
- **KOBiZE** (national emissions trading office) has no installation list file a script can find yet. The EU emissions trading registry data is the fallback.
- **City public information sites** hold most environmental decisions and have no common layout. Read each plant's city site by hand in the sweep.
- **Instrat power plant database** (Polish think tank, openly licensed, updated February 2025) has no download link on the page. Worth asking Instrat for the file.

## Recent events 2024 to 2026

- Large combined cycle units on capacity contracts: Grudziądz (CCGT Grudziądz, Energa, 563 MW, permit June 2026, second block planned), Ostrołęka C (CCGT Ostrołęka, 696 MW contract), Gdańsk (Energa, about 560 MW, construction), Rybnik (PGE, about 883 MW, construction), Kozienice (Enea Elkogaz, two blocks of 668 MW gross, contract signed, 2029), Adamów (PAK CCGT, 600 MW class, gas pipelines in a ministry decision of 24 March 2026), Dolna Odra (two units of 683 MW, 2024) and Gryfino II, Siekierki (Orlen Termika, over 550 MW, letter of intent), Pelplin and Makowisko (EG Vivos 2 and 3, 386.8 MW each, capacity contracts in the 2030 auction).
- Gas engine sets replacing coal at heat plants: Bydgoszcz II (about 50 MW, running since September 2025), Czechnica-2 at Siechnice (179 MW, May 2025), Kraków stage 1 (about 100 MW, construction from December 2025), Kalisz (about 20 MW, commissioning 2025), Elbląg (three 10 MW engines), Pomorzany (about 24 MW), Gorzów (63.7 MW), Gdynia (45.4 MW contract).
- The 2030 capacity auction (11 December 2025, final results 2 January 2026) gave 15 year contracts to two PGE units of 548.9 MW, Łagisza (Tauron, 538 MW) and EG Vivos 2 and 3.

## Watch items to raise with the reviewer

- The PSE connection list names about ten large gas projects GEM lacks (Turów, Pątnów, Opole Dobrzeń, Kraków Wanda, Lublin Abramowice, Łaziska, Połaniec peaker). A connection request alone may not meet the manual's add bar for Europe. Ask Dan how GEM treats them before any add is staged.
- Ostrów Wielkopolski: GEM has a 600 MW plant and the PSE list has a gas row there, but no other source was found on 2026-10-29. Confirm the developer and site.
- Rybnik: Dan's open comment asks whether it is nearing completion.
- Pomorzany: Dan set pre-construction where the other source said announced.

## Still open

- 45 validation fixes (38 are status history steps with no date), four open comment threads, 12 plants with approximate or missing locations.
- Nowa Sarzyna sold to Axpo and PGE's contracts for new gas plants (possible-updates sheet).

## Gotchas

- Polish plant names carry diacritics (Ł, ą, ę, ó, ś, ź, ż, ń). Match names with and without them.
- Capacity auction MW are obligation (de-rated) MW, not nameplate. Never stage them as capacity; use them only to find a project and its year.
- PSE connection list MW are connection capacity. Cite them for capacity only when no nameplate figure exists, and say so in the note.
- Polish numbers use a comma for decimals and a space for thousands (`518,370 MW` is 518.37 MW).
- `kobize.pl` has a bad security certificate; `fetch.py` handles it.
