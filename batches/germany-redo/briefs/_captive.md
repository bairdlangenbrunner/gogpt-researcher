## Captive power at LNG terminals in Germany (checklist rows 6 and 44)

The LNG team keeps a sheet of LNG terminals whose on-site gas-fired generation reaches the GOGPT threshold (20 MW here). Read on 2026-11-03: https://docs.google.com/spreadsheets/d/19YvVT918PYHq_DkdvKWtoXYJ2Xl7l7R3. The rows below are the ones in Germany, joined to the LNG tracker by Terminal ID. The sheet is a lead list, not the whole answer. Check its Qualifying rows first, but any captive LNG plant you verify at the threshold is an add, whether or not the sheet lists it (Baird, October 2026).

Rules:

1. Capacity is generating capacity only. Gas turbines that drive the refrigerant compressors (mechanical drive, shaft MW) are not power plant capacity. A row the sheet qualifies on mechanical drive alone needs its own generator sets found before anything is added; if there are none at the threshold, write a watch item saying so (drive_or_storage).
2. Captive fields: captive industry use power (or both when heat is also supplied), captive industry type LNG liquefaction. Unit naming follows GEM's existing LNG plants ("<Terminal name> power station"), one unit per generator set or per combined-cycle block.
3. Never cite gem.wiki; the sheet's own gem.wiki references are listed as not citable. Every other link must pass the verifier and state the value.
4. Terminals under "GEM lacks" are new plant candidates: research them and write a full new-plant record (shards/_state.json, newplants) with "captive_lng": true and "checks": [6, 44] as soon as one verified source names generator sets at the threshold at the terminal (the manual's ladder sets the status; a missing start year or turbine model never holds the add back). A watch item (monitor) with the same two keys, new to the tracker, with the reason, a recheck date and a watch_case, only when the generation is unnamed, under the threshold, or mechanical drive is unresolved.
5. Terminals under "Excluded" stay out unless you verify generator sets at the threshold; then it is an add like any other.
6. Captive fields are filled for every captive plant, including one that also sends power or heat out. Captive non-industry use records what is exported: power, heat, both or none.

### Qualifying terminals GEM lacks (new plant candidates)

### Brunsbuttel LNG Terminal (T100000130460)

LNG tracker: operating; proposed; owner German LNG Terminal [100%]; parent Kreditanstalt für Wiederaufbau [50.0%]; Nederlandse Gasunie NV [40.0%]; RWE AG [10.0%]; operator KN Energies; at Brunsbüttel (53.887255, 9.171014).
Sheet: 4x Wartsila 50DF engines (3x8L50DF + 1x6L50DF). Per unit: ~9.7 MW / ~7.3 MW. Total: ~36.4 MW total (estimated). Basis: Aggregate >=20 MW (genset rule).
Sources on the sheet: https://energy-terminal.de/fileadmin/user_upload/Test/Meldungen/2024-02-09_Para8a-Bescheid.pdf, https://www.wartsila.com/energy/engine-power-plant-solutions/engine-power-plant-products/wartsila-50df-dual-fuel-engine

### Mukran LNG Terminal (Deutsche Ostsee) (T100000131141)

LNG tracker: operating; mothballed; owner Deutsche ReGas [100%]; parent Deutsche ReGas [100.0%]; at Rügen (54.478384, 13.598351).
Sheet: Dual-fuel engines aboard 2 FSRUs (Neptune + Energos Power). Per unit: not broken out individually. Total: 39.9 MW total. Basis: Aggregate >=20 MW (genset rule).
Sources on the sheet: https://www.stalu-mv.de/vp/Service/Presse_Bekanntmachungen/?id=200530&processor=processor.sa.pressemitteilung, https://www.stalu-mv.de/vp/Service/Bekanntmachungen-nach-BImSchG/Bereich-Immissionsschutz/?processor=processor.sa.bimschbekannt&bekann_id=1719, https://www.energie-und-management.de/nachrichten/recht/detail/deutsche-regas-darf-mukran-dauerhaft-ohne-landstrom-betreiben-356711, https://www.duh.de/presse/pressemitteilungen/pressemitteilung/lng-terminal-in-mukran-deutsche-umwelthilfe-legt-widerspruch-gegen-aenderungsgenehmigung-ein/, https://www.offshore-energy.biz/german-player-picks-up-permanent-permit-for-lng-terminal-with-fsru-duo/, https://www.wartsila.com/energy/engine-power-plant-solutions/engine-power-plant-products/wartsila-50df-dual-fuel-engine, https://www.enerdata.net/publications/daily-energy-news/deutsche-regas-terminates-contract-fsru-energos-power-germany.html

### Wilhelmshaven LNG Terminal (Wilhelmshaven 1) (T100000130458)

LNG tracker: operating; proposed; owner Uniper SE [100%]; parent Uniper SE [100.0%]; operator KN Energies; at Wilhelmshaven (53.6416299, 8.1113678).
Sheet: 4x Wartsila W8L50DF gensets. Per unit: 7.8 MW each. Total: 31.2 MW t+H9otal. Basis: Aggregate >=20 MW (genset rule).
Sources on the sheet: https://www.wilhelmshaven-lng.de/index.php/en/fsru, https://www.asap.nl/hoegh-esperanza-fsru-flawless-lng-sampler-inspection/

Output: findings on tracked plants go in that plant's shard as usual. New plants and watch items from this block go in shards/_state.json under newplants and monitor, each with "captive_lng": true and "checks": [6, 44].
