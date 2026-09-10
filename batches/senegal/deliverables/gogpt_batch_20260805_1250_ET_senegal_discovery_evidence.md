# Evidence — gogpt batch 20260805_1250_ET (senegal, discovery)

## lane: qa

### G100000407255 / Cap des Biches power station / 1
**Action:** QA review — no edit this batch.
- confidence: low (independent: False)
- notes: Discovery-sweep byproduct, not researched to citation depth this batch (URLs not verified — treat as leads). The plant's own Status Detail already notes 'expected to reach a capacity of 366 megawatts', consistent with 366 = ultimate design figure. ALSO: sources routinely conflate this plant with Senelec's separate 250 MW EPCF tender at the same site (staged in newplants) — when applying, keep the two records' citations strictly apart.

### Kyrene Cement power station / 1
**Action:** QA review — no edit this batch (location fix routes to an update batch after satellite verification).
- confidence: medium (independent: False)
- notes: Caught while mirroring field conventions from the export during the discovery batch: the City field says Kirène but the coordinates and province point to Kaffrine region — internally inconsistent, so at least one is wrong, and all external descriptions place the cement plant ~50 km from Dakar (MAN 2021 release: 'located 50 km from the capital, Dakar'), which matches Thiès, not Kaffrine.

### G100000407256 / Malicounda power station / 1
**Action:** QA review — no edit this batch.
- confidence: low (independent: False)
- notes: Discovery-sweep byproduct; mp-nrg.com not run through the verifier this batch — lead only.

## lane: entity

### Gandon power station
**Action:** Before creating, re-run the lookup against the live entity system; then create entity 'Ndar Energies SA' (Senegal, owner) with the parent chain above.
- confidence: high (independent: True)
- notes: SPV owning the Gandon 255 MW CCGT. Parent chain for the entity record: Aksa-NDAR Holding SA 85% (itself 60% Aksa Enerji Uretim AŞ — EXISTING entity E100000002411 — per Aksa's KAP subsidiary table, Bildirim/1514788, 2025-11-10); National Electricity Company of Senegal (existing E100000000894) reported as 15% direct holder per Senegalese press (dakaractu 2025-10-28: Aksa 51% / ICONS-CSE-ELTON consortium 34% / Senelec 15% — reconciles with the KAP structure arithmetically). Whether to create the intermediate Aksa-NDAR Holding SA entity or attach Aksa Enerji directly is the ownership-team's call; SPV-as-owner is acceptable per the ownership rules.

### Sandiara power station
**Action:** Before creating, re-run the lookup against the live entity system; only create if the Sandiara plant record is accepted.
- confidence: medium (independent: True)
- notes: Spanish engineering group (Grupo TSK, Gijón), 50% developer stake in the Sandiara 360 MW CCGT per the GlobalData profile. Cross-country entity (Spain) — flag for the entity team per the cross-country warning convention.

### Sandiara power station
**Action:** Before creating, re-run the lookup against the live entity system; only create if the Sandiara plant record is accepted.
- confidence: low (independent: False)
- notes: TSK's local partner in the Sandiara project (africaoilgasreport 2023-07-18). No corporate website or registry entry found in the 2026 follow-up hunt — legal form and jurisdiction unconfirmed, share percentage unstated. Weakest entity of the batch; create only if the Sandiara plant record is accepted, and consider recording ownership as 'TSK [50%]; LFR Energy' with LFR's share blank per the ownership rules.

## lane: monitor

### Boto Gold Mine power plant (Managem)
**Action:** Monitor — recheck by 2027-08 for capacity expansion only.
- confidence: high (independent: False)
- notes: Well-evidenced (two Wärtsilä primary releases, 2024-09-27 and 2025-09-19) but permanently under threshold unless the mine expands generation ≥50 MW. Recheck is a low-priority existence check for expansion only.

### FONSIS 500 MW gas IPP (site unknown)
**Action:** Monitor — recheck by 2026-12 (tender outcome, site selection).
- confidence: medium (independent: False)
- notes: agenceecofin also covered the FONSIS-led 500 MW tender (2026-02-16) but that page 403s to automated fetches — single verified source for now. Distinct from the Senelec Cap des Biches EPCF tender (see newplants) and from the Sandiara project. At 500 MW this is a major newplants candidate as soon as a site and awardee exist.

### Grande Côte Opérations Diogo power plant (Eramet)
**Action:** Monitor — recheck by 2027-08 for capacity expansion only.
- confidence: high (independent: True)
- notes: Wärtsilä reference page + Eramet's own news page (hybridization with solar) — solid evidence, permanently under threshold. Eramet URL verified with accented token 'Grande Côte' (unaccented 'Grande Cote' fails).

### ICS Mboro power plant (Industries Chimiques du Sénégal / Indorama)
**Action:** Monitor — low priority; drop candidate unless threshold policy changes.
- confidence: medium (independent: True)
- notes: Permanently under threshold regardless of fuel; recorded so future Senegal batches don't re-research it from scratch. Pre-dates the 2020 retrospective window for status tracking anyway.

### Kirène Cement second power plant (Les Ciments du Sahel)
**Action:** Monitor — recheck by 2026-11 (try africa-energy DB via subscription, Senelec annual report IPP/autoproducteur tables, and fresh French-press sweep).
- confidence: medium (independent: False)
- notes: Rolls forward (enriched) from the update batch's monitor lane. MAN's own PDF is now verified live (man-es.com press-release PDF; the HTML page is dead). africa-energy.com has a database record 'ciments-du-sahel-kirene-hfo-lfo' whose Status/capacity/commissioning fields are paywalled — worth checking if GEM has subscription access; visible fuel field says 'HFO, Other fuel oils'. Cement-line context: the expansion line the plant serves was commissioned Feb 2023 (Global Cement), so the power plant plausibly operates by now — but that is inference, not evidence. 54 MW clears the threshold, so this promotes to newplants the moment one independent status source appears.

## lane: newplants

### Cap des Biches EPCF power station
**Action:** Create plant 'Cap des Biches EPCF power station' (Rufisque) owned by National Electricity Company of Senegal (existing entity E100000000894) with the unit below.
- `Plant name`: `` -> `Cap des Biches EPCF power station`
- `Other Name(s)`: `` -> `Centrale électrique EPCF 250 MW Cap des Biches`
- `Owner(s)`: `` -> `National Electricity Company of Senegal [100%]`
- `City`: `` -> `Rufisque`
- `State/Province`: `` -> `Dakar`
  - Owners Data Source: https://dgmarket.fr/Notice/93810338 (ok=True, contains_value=True)
  - Owners Data Source: https://fr.allafrica.com/stories/202607190110.html (ok=True, contains_value=True)
  - Location Data Source: https://dgmarket.fr/Notice/93810338 (ok=True, contains_value=True)
  - Location Data Source: https://fr.allafrica.com/stories/202607190110.html (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: Senelec's own EPCF (engineering-procurement-construction-financing) tender AOI N°16/2025 for a THIRD plant at the Cap des Biches site — distinct from both the 86 MW ContourGlobal engine plant and the 366 MW West Africa Energy CC (fr.allafrica/Le Soleil 2026-07-19 treats it as an additional 250 MW plant Senelec is building; high conflation risk in sources given similar capacity figures — see qa lane). Tender published 2025-05-14, 54 firms bought documents, 5 bids. Plant name 'Cap des Biches EPCF' follows the sources' own label; reviewer may prefer a different disambiguator. globaltenders.com is a mirror of the dgmarket notice (counted as one origin).

### Gandon power station
**Action:** Create plant 'Gandon power station' (Saint-Louis region) with owner Ndar Energies SA [100%] and the unit below; create the Ndar Energies SA entity first (see entity lane).
- `Plant name`: `` -> `Gandon power station`
- `Other Name(s)`: `` -> `Ndar Energies power station; Centrale électrique Ndar Energies`
- `Owner(s)`: `` -> `Ndar Energies SA [100%]`
- `City`: `` -> `Gandon`
- `State/Province`: `` -> `Saint-Louis`
  - Owners Data Source: https://www.kap.org.tr/en/Bildirim/1233784 (ok=True, contains_value=True)
  - Owners Data Source: https://www.power-technology.com/data-insights/power-plant-profile-ndar-energies-gas-power-plant-senegal/ (ok=True, contains_value=True)
  - Location Data Source: https://www.kap.org.tr/en/Bildirim/1233784 (ok=True, contains_value=True)
  - Location Data Source: https://johncockerill.com/en/press-and-news/news/making-senegal-cooler-and-more-autonomous-with-the-supply-of-a-new-air-cooled-condenser/ (ok=True, contains_value=True)
- confidence: high (independent: True)
- notes: 255 MW CCGT under construction in Gandon commune, Saint-Louis region — the physical terminus of RGS's Segment Nord pipeline from the GTA gas hub (offshore 45 km to Léona landing + 40 km onshore, per rgs.sn). Owner is the SPV Ndar Energies SA. Parent chain per Aksa Enerji's KAP filings: Aksa-NDAR Holding SA holds 85% of Ndar Energies SA, and Aksa Enerji Uretim AŞ holds 60% of the holding (KAP subsidiary table 2025-11-10, Bildirim/1514788); Senegalese press reports the economic split as Aksa 51% / consortium ICONS-CSE-ELTON 34% / Senelec 15% (dakaractu 2025-10-28, ndarinfo) — the two accounts reconcile arithmetically (60%×85%=51%, 40%×85%=34%, Senelec 15% direct) but no single document states all figures together. A Fasken deal page describes the 85% sale (closed Dec 2023) but is 403 with no Wayback snapshot — not citable as verified. Siting per the SERV-linked ESIA (Feb 2026): ~10 ha site ~1.5 km from Ndiakhère village; no public lat/long found — ESIA PDF URL not captured, coordinates left blank. power-technology profile verified via Wayback snapshot 20241214133945 (live URL 403s).

### Karpowership (Senegal) Gökhan Bey power station
**Action:** Create plant 'Karpowership (Senegal) Gökhan Bey power station' (Dakar) owned by Karpowership (existing entity E100000003399) with the unit below.
- `Plant name`: `` -> `Karpowership (Senegal) Gökhan Bey power station`
- `Other Name(s)`: `` -> `KPS 10; Karadeniz Powership Gökhan Bey`
- `Owner(s)`: `` -> `Karpowership [100%]`
- `City`: `` -> `Dakar`
- `State/Province`: `` -> `Dakar`
  - Owners Data Source: https://karpowership.com/senegal (ok=True, contains_value=True)
  - Owners Data Source: https://www.offshore-energy.biz/four-years-in-the-making-africas-first-lng-to-power-project-up-and-running-off-senegal/ (ok=True, contains_value=True)
  - Location Data Source: https://karpowership.com/senegal (ok=True, contains_value=True)
  - Location Data Source: https://www.offshore-energy.biz/four-years-in-the-making-africas-first-lng-to-power-project-up-and-running-off-senegal/ (ok=True, contains_value=True)
- confidence: medium (independent: True)
- notes: PROMOTED from the update batch's monitor lane. Karpowership's own Senegal page (primary): 'In December 2021, an additional contract of 100 MW was signed' and total 'installed capacity of 335 MW' — vs the 235 MW Ayşegül Sultan already in GEM, confirming a second vessel at Dakar. Vessel identity is the medium-confidence piece: offshore-energy calls the second unit 'KPS 10', AIS places Karadeniz Powership Gökhan Bey (IMO 9214563, nameplate ~125 MW) at Dakar, and an africa-energy database title pairs 'Aysegul Sultan and Gokhan Bey' — consistent but partly indirect. If the reviewer prefers not to commit to the vessel name, create as 'Karpowership (Senegal) second powership' instead. Plant-per-vessel naming mirrors the existing Ayşegül Sultan record. Gas supply from the Karmol FSRU since 2025 covers the whole Dakar operation. Coordinates left blank (AIS positions not a durable citation); anchorage adjacent to the existing L100000407151.

### Sandiara power station
**Action:** Create plant 'Sandiara power station' (Sandiara, Thiès) with owners TSK Electronica y Electricidad SA [50%] + LFR Energy (both new entities — see entity lane) and the unit below.
- `Plant name`: `` -> `Sandiara power station`
- `Other Name(s)`: `` -> `Centrale électrique de Sandiara; Sandiara SEZ gas-to-power project`
- `Owner(s)`: `` -> `TSK Electronica y Electricidad SA [50%]; LFR Energy`
- `City`: `` -> `Sandiara`
- `State/Province`: `` -> `Thiès`
  - Owners Data Source: https://africaoilgasreport.com/2023/07/power-deficit/tsk-to-start-construction-of-360mw-gas-fired-plant-in-senegal-from-2024/ (ok=True, contains_value=True)
  - Owners Data Source: https://www.power-technology.com/marketdata/power-plant-profile-sandiara-power-plant-senegal/ (ok=True, contains_value=True)
  - Location Data Source: https://africaoilgasreport.com/2023/07/power-deficit/tsk-to-start-construction-of-360mw-gas-fired-plant-in-senegal-from-2024/ (ok=True, contains_value=True)
  - Location Data Source: https://www.power-technology.com/marketdata/power-plant-profile-sandiara-power-plant-senegal/ (ok=True, contains_value=True)
- confidence: medium (independent: True)
- notes: 360 MW CCGT announced Jul 2023 for the Sandiara Special Economic Zone (TSK of Spain 50% + LFR Energy; Siemens SGT-800 turbines; 25-year Senelec PPA reported at announcement). Evidence trail goes cold after late 2024: GlobalData profile says 'permitting stage'; TSK's own live project portfolio does NOT list Sandiara; APIX SEZ-tenant coverage (Aug 2024) does not mention the plant; no financial close, groundbreaking, cancellation, or updated timeline found through Aug 2026. Both citations verified via Wayback snapshots (live URLs 403; snapshots 20250721052125 and 20240715185730) — live URLs kept as citations. If no new evidence by late 2026 the shelved-inference clock (2y from last evidence) starts to bite — flag for the next Senegal batch.

---

## Batch narrative (discovery, Senegal)

### Method

- Fresh pull + `scope_filter.py` at batch start (34.5k-row full export kept for cross-tracker dedup); colmap re-derived from the header.
- Four discovery rings swept: (1) national utility / IPP pipeline (Senelec tenders, ministry announcements, FONSIS), (2) gas-to-power buildout around the GTA/Yakaar-Teranga gas supply chain (RGS pipeline offtakers), (3) captive/industrial power (mining, cement, chemicals), (4) OEM + developer press (Wärtsilä, MAN, GE, Aksa, TSK, Karpowership).
- Dedup against BOTH the scoped GOGPT export and the full combustion export: none of the staged candidates matches an existing GEM plant/unit. The Cap des Biches EPCF tender was explicitly disambiguated from the two existing Cap des Biches records (86 MW ContourGlobal, 366 MW West Africa Energy) — see qa lane for the conflation warning.
- Every citation passed `url_verifier.py` (value-level token checks, not HTTP-200); full audit trail in `batches/senegal/staging-discovery/url_verifier_log.jsonl`.

### New plants — unit-level evidence

**Gandon power station, unit 1 — 255 MW, construction, fossil gas: natural gas, combined cycle, start year 2026 (tier: high)**
- Capacity 255 MW: Aksa Enerji KAP material-event disclosure 2024-01-08 (kap.org.tr/en/Bildirim/1233784, "installed capacity of 255 MW in the City of Saint Louis"); Aksa press release Jul 2026 (aksaenerji.com.tr, €57M financing, "255 MW… currently under construction"); John Cockerill air-cooled-condenser news; Enerdata daily-energy-news. Conflicting figures rejected: ESIA 250 MW (rounding), dakaractu 160→220 MW phased (contradicted by Le Soleil's own next-day 255 MW piece).
- Status construction: Aksa press release (under construction) + Le Soleil 2026-07-18 (turbines received at Port of Dakar, first tests Oct 2026).
- Fuel natural gas: KAP disclosure + Enerdata (both explicitly gas/CCGT). Plant is the terminus of RGS Segment Nord from the GTA hub.
- Technology combined cycle + start year 2026: KAP disclosure + power-technology profile (Wayback-verified, snapshot 20241214133945; live URL 403s — live URL kept as the citation).

**Cap des Biches EPCF power station, unit 1 — 250 MW, announced, fossil gas: natural gas, combined cycle, NO start year (tier: high)**
- The tender text itself (dgmarket.fr/Notice/93810338, primary) specifies "centrale électrique EPCF de 250 MW en cycle combiné CCGT fonctionnant au gaz"; fr.allafrica (Le Soleil) 2026-07-19 corroborates capacity/owner/site. globaltenders.com carries the same notice (mirror — counted as ONE origin with dgmarket, used only as a convenience link for fuel/technology wording).
- Status announced: provisional award to Sinohydro (287,876,216,633 FCFA, 30-month build, notice 2026-03-26) is contested — CMS (Morocco) obtained a bid re-evaluation (inamaenergy 2026-06-20, verified); no final award or construction start as of Aug 2026. No start year staged pre-award.

**Sandiara power station, unit 1 — 360 MW, pre-construction, fossil gas: natural gas, combined cycle, NO start year (tier: medium)**
- africaoilgasreport 2023-07-18 + GlobalData/power-technology profile; BOTH live URLs 403 to automated fetches — verified via Wayback snapshots 20250721052125 and 20240715185730 (all tokens present); live URLs kept as citations.
- Trail cold after the GlobalData "permitting stage" snapshot (Jul 2024): TSK's own portfolio omits the project; no financial close/groundbreaking/cancellation found through Aug 2026. Staged pre-construction with an explicit stalled warning; the 2-year shelved-inference clock starts biting late 2026.

**Karpowership (Senegal) Gökhan Bey power station, unit 1 — 100 MW, operating, fossil gas: LNG, NO technology, NO start year (tier: medium)**
- Promoted from the update batch's monitor lane. Capacity 100 MW (contracted) is single-primary: karpowership.com/senegal ("an additional contract of 100 MW was signed"; site total 335 MW vs the 235 MW Ayşegül Sultan already in GEM). The offshore-energy four-year article corroborates the 335 MW total and the "KPS 10" identity but does NOT state 100 MW — capacity is therefore yellow/single-primary by design.
- Fuel staged as LNG only (both sources explicit); the sibling record's fuel-oil backup component and ICCC technology are NOT stated by any verified source — left blank per the blank-over-weak rule, with mirror-the-sibling guidance in the notes.
- Vessel identity (Gökhan Bey / KPS 10) is consistent across offshore-energy, AIS position, and an africa-energy database title, but partly indirect — fallback name "Karpowership (Senegal) second powership" offered in the notes.

### Verification & tooling notes

- 3 citations rest on manual Wayback verification (live 403, verifier's built-in fallback missed the snapshots): power-technology Ndar profile, africaoilgasreport Sandiara, power-technology Sandiara. Manual JSONL entries record snapshot IDs. **Tooling follow-up:** url_verifier.py's Wayback fallback misses snapshots its CDX query should find.
- Rejected/unciteable along the way: fasken.com Ndar deal page (403, zero Wayback snapshots), lequotidien Karpowership interview (403, no snapshot), africabusinessplus CdB award piece (404), agenceecofin FONSIS piece (403). None are cited.
- eramet.com verified only with the accented token "Grande Côte" (unaccented fails) — noted for future verifier runs.

### Coverage gaps

- **gem.wiki name-check (Discovery SOP §5.3) could not run** — gem.wiki 403s from this host entirely. Dedup rests on the export (authoritative) only.
- Remote entity lookup skipped (GEM_PROJECT_DB_BASE_URL unset): all three entity-lane records must be re-checked against the live entity system before creation.
- africa-energy.com database fields (Kirène second plant status; Gökhan Bey record) are paywalled — worth one subscription lookup if GEM has access.

### Escalation flag — candidate density

4 newplants candidates in one country sits just under the ~5 "systematic gap" escalation line. This is explainable rather than alarming: Senegal's GTA-driven gas-to-power buildout (RGS pipeline, Senelec EPCF program, FONSIS IPP tender) is generating a genuine wave of new projects, and 2 of the 4 (Gandon, CdB EPCF) are that wave. The FONSIS 500 MW IPP (monitor lane) will likely add a 5th within months — flagging now so the next batch expects it.
