# Senegal

Small, active fleet: 11 GOGPT units at 10 plants (~1.2 GW), mostly HFO/diesel
IC engines transitioning to domestic gas ("gas-to-power"); high churn in
ownership and fuel status makes it a good periodic-refresh country.

## Country context

- Grid operator / TSO: Senelec (Société nationale d'électricité du Sénégal) —
  also the offtaker for every IPP and, increasingly, an owner (bought out West
  African Energy in 2026).
- LNG / fuel-supply context: national "gas-to-power" strategy on domestic gas
  (GTA and Yakaar-Teranga fields). Conversions of the HFO fleet keep slipping —
  ministerial timeline was end-2028–Q1 2029 as of May 2026. Bel-Air runs on
  LNG since May 2025; Cap des Biches CC burns gas-oil pending its LNG
  regasification link.
- Conflict zone: no.
- Large country — split research by region: no.

## Regulators & official sources

- CRSE (Commission de Régulation du Secteur de l'Énergie) — tariff decisions
  and IPP contract references — https://www.crse.sn
- Senelec — annual reports carry per-IPP purchase volumes (GWh), the best
  operating-status evidence for small IPPs; report PDF URLs rot quickly, so
  re-locate the current URL each batch — https://www.senelec.sn
- APS (Agence de Presse Sénégalaise) — carries Senelec statements verbatim —
  https://aps.sn

## Key operators & utilities

- Senelec (state utility) — owner of Bel-Air C6, 15% of Malicounda, and since
  2026-04-25 sole shareholder of West African Energy (Cap des Biches CC).
- MP Energy (formerly Melec PowerGen Inc; site mp-nrg.com) — 55% of Malicounda,
  parent of Kounoune Power SA. DFI documents use the old "Melec Powergen" name.
- Azura Power Holdings (shareholders Actis, Africa50, Amaya Capital) — owns
  Tobene Power SA since Oct 2019.
- Karpowership — floating power at Dakar (Ayşegül Sultan, 235 MW + second
  vessel ~100 MW contracted, likely Gökhan Bey/KPS 10 — staged as a newplants
  candidate in the 2026-08 discovery batch).
- ContourGlobal (parent KKR & Co since 2022) — 86 MW Cap des Biches "engine"
  plant; its HFO→LNG conversion slipped from mid-2023 to FID-2025/target-2026.
- Endeavour Mining — captive plant at Sabodala-Massawa gold mine.
- Les Ciments du Sahel — captive plant(s) at Kirène cement works.

## Preferred sources (beyond the global roster)

- lesoleil.sn, lequotidien.sn, pressafrik.com — Senegalese dailies; good for
  commissioning/fuel-switch events; French-language.
- financialafrik.com, agenceecofin.com — pan-African business press, good on
  ownership transactions.
- ewsdata.rightsindevelopment.org — mirrors DFI (MIGA/IFC/AfDB) project
  documentation that the DFI sites themselves often 403 to automated fetches.

## Research tips

- French search terms that worked: "centrale" + plant name, "basculement au
  gaz" (fuel switchover), "actionnaire unique" (sole shareholder), "mise en
  service" (commissioning).
- Senelec statements syndicate widely (APS, PressAfrik, Seneweb carry the same
  text) — treat them as ONE origin when counting independence.
- Le Soleil has run Karpowership-sponsored content — check for "tribune" or
  sponsor framing before treating it as independent.

## Gotchas

- Two distinct "Cap des Biches" plants in Rufisque: the 86 MW ContourGlobal
  ICCC ("engine") plant and the 366 MW West African Energy CC — different
  owners, ~same location; don't merge or cross-cite them. Bel-Air C6 is a third
  separate plant ~15 km away in Dakar.
- Dual-fuel fields may reflect gas-READY design, not actual gas operation
  (Tobène recorded as gas+fuel oil while conversions were still pending).
- kounounepower.com is dead (HTTP 526 as of 2026-08) yet is the sole citation
  on all five of Kounoune's Data Source cells.
- news-pravda.com surfaced carrying Senegal energy stories — unreliable
  aggregator, do not cite.

## Open items

- Karpowership: no public contract end date after the recorded 2025 planned
  retirement passed. (Second vessel: promoted to newplants in the 2026-08
  discovery batch — no longer a monitor item.)
- Kirène: MAN release describes a later ~54 MW 6×9L51/60 plant for Ciments du
  Sahel not in GEM (monitor lane, recheck 2026-11; 54 MW clears the threshold —
  promotes to newplants on ONE independent status source; africa-energy.com DB
  record exists but status field is paywalled).
- Sandiara 360 MW (staged pre-construction 2026-08): last evidence Jul 2024
  "permitting" — the 2-year shelved-inference clock starts biting late 2026.
- FONSIS 500 MW gas IPP tender (Feb 2026): no site/awardee yet (monitor,
  recheck 2026-12) — a major newplants candidate the moment those exist.
- Kyrene Cement coords/State-Province point to Kaffrine, ~250 km from the
  Kirène/Thiès location the City field and all sources describe (qa-flagged
  2026-08) — fix after satellite verification.
- Sabodala-Massawa unit 1 start year (likely 2009) — needs the Endeavour/
  Teranga NI 43-101 technical report to date the plant commissioning.
- Sendou gas-conversion timepoint — announced only; recheck after FID/EPC.
- Cap des Biches (engine) conversion — watch IFC record "CdB Gas Convers."
  (IFC-50638) and the ~EUR 105M refinancing (reported closing May 2025) for the
  actual gas-conversion date; Fuel field currently overstates gas (qa-flagged).

## Update notes

- *2026-08-05 (batch gogpt_batch_20260805_0953_ET_senegal_update)* — first full
  Update pass: 6 updates-lane records (Kounoune owner fill, Sabodala unit-1
  technology, Karpowership planned-retire deletion, 3 datasource
  enrichments), 9 qa flags (3 entity-parent corrections incl. Senelec/WAE and
  Azura/Tobène), 2 monitor items. Parent(s) is a computed column — parent
  findings route to qa as entity-record changes, not unit edits.
- *2026-08-05 (batch gogpt_batch_20260805_1451_ET_senegal_discovery)* — first
  discovery pass: 4 newplants staged (Gandon/Ndar Energies 255 MW construction,
  Cap des Biches EPCF 250 MW announced-tender, Sandiara 360 MW stalled
  pre-construction, Karpowership Gökhan Bey ~100 MW operating), 3 entity
  candidates, 5 monitor items, 3 qa flags. Candidate density (~4-5) reflects
  the real GTA gas-to-power buildout, not a tracking failure. Useful sources:
  KAP (kap.org.tr) material-event disclosures beat local press on Aksa project
  facts; dgmarket.fr carries Senelec tender notices verbatim; power-technology
  and africaoilgasreport 403 live but Wayback snapshots verify.
