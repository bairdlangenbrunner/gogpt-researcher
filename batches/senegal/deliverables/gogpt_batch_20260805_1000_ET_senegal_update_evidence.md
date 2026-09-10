# Evidence — gogpt batch 20260805_1000_ET (senegal, update)

## lane: updates

### G100000411356 / Bel-Air C6 power station / 1-6
**Action:** On G100000411356, no value edits; add the listed URLs to the Status/Capacity/Fuel/Owners Data Source cells (keep pumps-africa.com).
- `Status`: `operating` -> `operating`
- `Capacity (MW)`: `90.0` -> `90.0`
- `Fuel`: `fossil gas: LNG, fossil liquids: heavy fuel oil` -> `fossil gas: LNG, fossil liquids: heavy fuel oil`
- `Owner(s)`: `National Electricity Company of Senegal [100%]` -> `National Electricity Company of Senegal [100%]`
  - Status Data Source: https://lesoleil.sn/actualites/economie/fourniture-delectricite-senelec-annonce-le-basculement-au-gaz-de-ses-unites-de-bel-air/ (ok=True, contains_value=True)
  - Capacity Data Source: https://www.wartsila.com/media/news/12-04-2021-wartsila-gas-conversion-project-will-accelerate-senegal-s-move-to-cleaner-energy-production-2893841 (ok=True, contains_value=True)
  - Capacity Data Source: https://www.offshore-energy.biz/wartsila-scores-senegal-power-plant-lng-conversion/ (ok=True, contains_value=True)
  - Fuel Data Source: https://www.wartsila.com/media/news/12-04-2021-wartsila-gas-conversion-project-will-accelerate-senegal-s-move-to-cleaner-energy-production-2893841 (ok=True, contains_value=True)
  - Fuel Data Source: https://lesoleil.sn/actualites/economie/fourniture-delectricite-senelec-annonce-le-basculement-au-gaz-de-ses-unites-de-bel-air/ (ok=True, contains_value=True)
  - Fuel Data Source: https://energycapitalpower.com/senegal-begins-major-lng-conversion-of-bel-air-power-plant/ (ok=True, contains_value=True)
  - Owners Data Source: https://www.wartsila.com/media/news/12-04-2021-wartsila-gas-conversion-project-will-accelerate-senegal-s-move-to-cleaner-energy-production-2893841 (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: No value changes — re-verified (blue) with datasource enrichment: every Data Source cell currently cites only pumps-africa.com. Wärtsilä's 2021 release (primary OEM) confirms 90 MW, Senelec ownership and six 50DF dual-fuel engines; Le Soleil (May 2025) reports the switchover to gas operation (entails operating); energycapitalpower covers the LNG conversion. offshore-energy.biz derives from the Wärtsilä release (not independent of it) but the Wärtsilä primary alone carries the capacity.

### G100000408642 / Karpowership (Senegal) Aysegul Sultan power station / 1
**Action:** On G100000408642, clear Planned retire (currently 2025); add both URLs to Planned Retire Data Source as evidence of continued operation past the recorded date (keep existing URL).
- `Planned retire`: `2025` -> ``
  - Planned Retire Data Source: https://aps.sn/coupures-delectricite-senelec-evoque-lindisponibilite-de-certains-de-moyens-de-production/ (ok=True, contains_value=True)
  - Planned Retire Data Source: https://www.pressafrik.com/Maintenance-a-la-centrale-flottante-Karpowership-KPS-la-Senelec-annonce-des-coupures-dans-plusieurs-localites_a306375.html (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: Staged deletion: the recorded 2025 planned retirement has passed and the vessel was still supplying Dakar in June-July 2026 (Senelec maintenance/outage announcements carried by APS and PressAfrik — both trace to the same Senelec statement, so one independent origin). No source states a new contract end date (see qa). The existing Planned Retire Data Source (karpowership.com/en/project-senegal) no longer resolves.

### G100000413926 / Kounoune power station / 1
**Action:** On G100000413926, set Owner(s) to 'Kounoune Power SA [100%]'; add both URLs to Owners Data Source (keep kounounepower.com despite link-rot — datasources are never deleted; see qa).
- `Owner(s)`: `` -> `Kounoune Power SA [100%]`
  - Owners Data Source: https://mp-nrg.com/kounoune/ (ok=True, contains_value=True)
  - Owners Data Source: https://ewsdata.rightsindevelopment.org/projects/d5c2b9c9d4-kounoune-power-sa/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: Fills the blank Owner(s): the project company is Kounoune Power SA (mp-nrg.com lists Kounoune as a current asset; DFI project documentation confirms 'Kounoune Power SA'). Kounoune Power already exists in the GEM entity system (it is this unit's operator). Parent(s) is a computed column (entity graph) — the parent finding (MP Energy, ex Melec PowerGen) is flagged in qa for the entity record instead.

### G100000413545 / Kyrene Cement power station / 1
**Action:** On G100000413545, no value edits; add the powermag.com URL to Owners Data Source (keep grupotsk.com).
- `Owner(s)`: `Les Ciment du Sahel SA` -> `Les Ciment du Sahel SA`
  - Owners Data Source: https://www.powermag.com/press-releases/man-energy-solutions-installs-over-225-mw-of-generation-capacity-in-west-africa/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: No value change — re-verified (blue) with a second independent origin: MAN Energy Solutions' release (via POWER Magazine) names Ciments du Sahel as its Kirene customer, independent of the existing grupotsk.com (TSK, the EPC) citation. The same MAN release mentions a later ~54 MW 6x9L51/60 MAN plant at Kirene (2021) that is not in GEM — routed to the monitor lane, not staged.

### G100000407256 / Malicounda power station / 1
**Action:** On G100000407256, no value edits; add the two URLs to Owners Data Source (keep existing three — and see qa for the dedupe).
- `Owner(s)`: `MP Energy [55%]; Africa50 SA [30%]; National Electricity Company of Senegal [15%]` -> `MP Energy [55%]; Africa50 SA [30%]; National Electricity Company of Senegal [15%]`
  - Owners Data Source: https://mp-nrg.com/malicounda-power/ (ok=True, contains_value=True)
  - Owners Data Source: https://www.africa50.com/our-funds/projects/malicounda-power-plant/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: No value change — re-verified (blue): ownership split confirmed on mp-nrg.com (which names 'Melec Powergen', MP Energy's former name, as the 55% holder) and Africa50's project page (120 MW, 30% stake context). The Owners Data Source cell currently contains its three URLs TRIPLICATED (9 entries) — dedupe flagged in qa. The africa50.com URL here is the current path of the page already cited in Capacity Data Source under an older path.

### G100000413543 / Sadobala-Massawa Gold Mine power plant / 1
**Action:** On G100000413543, set Turbine/Engine Technology to 'internal combustion'; paste the URL into Turbine/Engine Technology Data Source.
- `Turbine/Engine Technology`: `unknown` -> `internal combustion`
  - Turbine/Engine Technology Data Source: https://www.wartsila.com/media/news/16-08-2022-wartsila-power-plant-upgrade-and-extension-will-enable-production-expansion-for-largest-gold-mine-in-senegal-3141522 (ok=True, contains_value=True)
- confidence: high (independent: False)
- notes: Wärtsilä's Aug 2022 EPC release for the 18 MW extension (unit 2) states the three new Wärtsilä 32 engines are '20 per cent more fuel efficient than the plant's existing engines' — a primary OEM statement that the existing 36 MW unit is reciprocating-engine (internal combustion). engineeringnews.co.za carries the same release (not independent). Start year deliberately NOT staged — see qa: no source explicitly dates the plant's commissioning.

## lane: qa

### G100000407254 / Cap des Biches (engine) power station / 1
**Action:** Review only — refresh Status Detail; fuel change waits for the conversion timepoint.
- confidence: medium (independent: True)
- notes: Verified URLs (live, value-on-page): https://www.contourglobal.com/assets/cap-des-biches/ ('HFO', '86 MW') ; https://www.contourglobal.com/portfolio-decarbonization/ ('Final Investment Decision', '2025') ; https://mg.co.za/thought-leader/opinion/2026-03-13-ifcs-new-gas-projects-will-destroy-africa/ ('Cap des Biches', 'heavy fuel oil' — independent of ContourGlobal). The two contourglobal.com pages are one origin; the Mail & Guardian piece is a second, so the still-on-HFO finding has two independent origins. Note the DB's citation path /asset/cap-des-biches has moved to /assets/cap-des-biches/. Same gas-ready-vs-actual pattern as Tobène. Do not conflate this 86 MW ContourGlobal plant with the 366 MW West African Energy CC at the same site (G100000407255).

### G100000407255 / Cap des Biches power station / 1
**Action:** Review only — route to the entity/ownership update path.
- confidence: high (independent: True)
- notes: Two independent verified sources (financialafrik.com 2026-04-25: Senelec 'becomes sole shareholder of West African Energy'; seneweb.com: 'brings the national company's stake to 100% of the capital of West African Energy'). Unit-row Owner(s) stays 'West Africa Energy SA [100%]' — no unit edit needed. Verified URLs: https://www.financialafrik.com/en/2026/04/25/senegal-senelec-becomes-sole-shareholder-of-west-african-energy-wae/ ; https://www.seneweb.com/en/news/Energie/energy-sovereignty-senelec-takes-full-control-of-west-african-energy_n_490677.html

### G100000408642 / Karpowership (Senegal) Aysegul Sultan power station / 1
**Action:** Review only — no edit.
- confidence: low (independent: False)
- notes: The 2025 planned retirement passed without event (deletion staged in updates); no public source states the current contract end date — a documented transparency gap for Karpowership's Senegal operations.

### G100000413926 / Kounoune power station / 1
**Action:** Review only — route to the entity/ownership update path.
- confidence: high (independent: True)
- notes: Two independent verified sources: mp-nrg.com/kounoune (MP Energy's own portfolio page) and ewsdata.rightsindevelopment.org ('All three assets are currently owned by Melec Powergen Inc', from DFI project documentation). Pairs with the updates-lane Owner(s) fill on this unit. Verified URLs: https://mp-nrg.com/kounoune/ ; https://ewsdata.rightsindevelopment.org/projects/d5c2b9c9d4-kounoune-power-sa/

### G100000413926 / Kounoune power station / 1
**Action:** Review only — no edit.
- confidence: low (independent: False)
- notes: Link-rot: the unit's single citation domain no longer resolves. Operating status was corroborated in research via Senelec's 2024 annual report (88.18 GWh purchased from IPP Kounoune) but the report PDF's URL 404s — it moved; locate the current URL before citing.

### G100000407256 / Malicounda power station / 1
**Action:** Review only — dedupe during the updates-lane edit.
- confidence: low (independent: False)
- notes: Triplication is presumably an earlier copy-paste artifact; deduping does not violate the never-delete-datasources rule because every distinct URL is retained.

### G100000413543 / Sadobala-Massawa Gold Mine power plant / 1
**Action:** Review only — no edit.
- confidence: low (independent: False)
- notes: Start year is blank and very likely 2009: the mine poured first gold in March 2009 and mining-technology.com (2020 Wayback snapshot; live page 403s) confirms 'Power comes from a 36MW, on-site heavy fuel oil (HFO) power station' at a remote off-grid site. But no accessible source explicitly dates the POWER PLANT's commissioning, and an earlier research pass's claim of '25 MW commissioned early 2009' could not be verified on any retrievable page — so nothing is staged.

### G100001017958 / Sendou power station / Unit 1, timepoint 2
**Action:** Review only — no edit.
- confidence: low (independent: False)
- notes: No edit supportable this batch: the conversion timeline rests on one ministerial interview syndicated across outlets (one origin), and one carrying outlet (news-pravda.com) is an unreliable aggregator. Cross-tracker note: any coal-unit status change belongs to GCPT, not this batch.

### G100000407257 / Tobène power station / 1
**Action:** Review only — route to the entity/ownership update path.
- confidence: high (independent: True)
- notes: Three independent verified sources: tobenepower.com (subsidiary of Azura Power Holdings), amayacap.com/investments (lists Tobene), africa50.com (Azura acquisition announcement). All entities already exist in the GEM entity system (seen on other trackers). Verified URLs: https://tobenepower.com/ ; https://www.amayacap.com/investments ; https://www.africa50.com/media/news/article/azura-power-invests-in-tobene-power-in-senegal-through-its-pan-african-baseload-generation-platform-312/ Canonical GEM entity names confirmed via entity_lookup.py: 'Azura Power Holdings Ltd' (1 unit, Mozambique), 'Actis LLP' (7 units), 'Africa50 SA' (2 units), 'Amaya Capital' (5 units) — reuse existing IDs, create nothing.

### G100000407257 / Tobène power station / 1
**Action:** Review only — no edit.
- confidence: low (independent: False)
- notes: The recorded fuel 'natural gas, fuel oil' may reflect the dual-fuel design rather than actual operation; Senegal's gas-to-power conversions were still pending as of mid-2026 (national timeline end-2028 to Q1 2029). Canonical GEM entity names confirmed via entity_lookup.py: 'Azura Power Holdings Ltd' (1 unit, Mozambique), 'Actis LLP' (7 units), 'Africa50 SA' (2 units), 'Amaya Capital' (5 units) — reuse existing IDs, create nothing.

## lane: monitor

### Karpowership Dakar — possible second vessel
**Action:** Monitor — recheck by 2026-12.
- confidence: low (independent: False)
- notes: GEM's unfiltered export has no second Senegal Karpowership unit (Goktay Bey is The Gambia). If confirmed, this is a newplants candidate (floating power plant).

### Kirene (Ciments du Sahel) — possible second MAN plant
**Action:** Monitor — recheck by 2026-11.
  - Status Data Source: https://www.powermag.com/press-releases/man-energy-solutions-installs-over-225-mw-of-generation-capacity-in-west-africa/ (ok=True, contains_value=True)
- confidence: medium (independent: False)
- notes: If corroborated (e.g. Ciments du Sahel/MAN project pages, Senegalese press), stage as newunits at the existing Kyrene Cement power station location or a newplants record if it is a separate site. Captive plant — generating MW only.
