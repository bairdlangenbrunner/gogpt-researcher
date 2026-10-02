# Systematic search plan — Vietnam (census) and Brazil (subset)

Drafted 2026-09-18; Step 0 run the same day and its results folded in below.
Supersedes the sampling approach in `scoping_plan.md`,
which stays as the record of the two 3 + 3 probes of 2026-09-17. What those
probes established — where documents live and how to reach them — is in
`countries/`; this file is about covering the plant list methodically.

## What changes

The probes answered "can documents be found at all?" (yes, both countries).
The question now is **coverage**: for what share of plants can plant-specific
NOx / SOx / PM inputs be found, by which route, at what cost. That needs a
fixed frame, every plant walked through the same ladder, and every outcome
logged — including the misses, with the rungs tried.

- **The frame** is `coverage/<country>.csv`, one row per fossil-gas plant,
  built by `build_coverage.py` from the fresh scoped pull. GEM columns are
  regenerated on each run; the search columns are hand-kept and carried over by
  `gem_location_id`.
- **Work source-first, not plant-first.** Enumerate a source completely (a
  portal, an agency library, an open-data set), then join it to the frame. The
  probes lost most of their time rediscovering the same portal per plant.
- **A row is closed only with an outcome** from the vocabulary below. "Not
  found" needs `rungs_tried` filled in; a blocked fetch is `blocked`, never
  `not-found`.

## The frame (pull 2026-09-18, fossil-gas units only)

Plants are filed once, under their most advanced status
(construction > pre-construction > announced > operating > the rest).

| | Vietnam | Brazil |
|---|---|---|
| Gas plants (units, MW) | 45 (117; 129,095) | 163 (259; 114,895) |
| **Pipeline** plants | **24** — 6 construction, 9 pre-construction, 9 announced | **65** — 6 construction, 31 pre-construction, 28 announced |
| Pipeline units, MW | 50; 54,285 | 97; 46,402 |
| **Operating** plants | 7, plus operating units at 2 pipeline plants (Cà Mau, Ô Môn) | 50, plus operating units at 3 pipeline plants |
| Inactive (cancelled, shelved, mothballed) | 14 | 48 |
| CREA's 25 % of pipeline plants | 6 | 16–17 |
| Already closed with values (2026-09-17) | 6 pipeline + 1 operating | 3 pipeline |

Brazil's scoped export also holds 10 blast-furnace / coke-oven gas units and 35
oil units; they are outside the frame.

## Tracker vocabulary

| Column | Values |
|---|---|
| `track` | `pipeline`, `operating`, `inactive`, `gone from export` (set by the script) |
| `licensor` | The body that licenses the plant, once **confirmed** (Brazil: IBAMA or the state agency; Vietnam: the ministry). Blank = unresolved |
| `licence_stage` | Brazil: LP / LI / LO with number and date where known. Vietnam: ĐTM consulted / approved, GPMT |
| `search_status` | blank (not started) · `located` (document identified, unread) · `found-values` · `found-no-values` (document read, no usable emissions numbers) · `not-found` (ladder exhausted) · `no-document-expected` (too early a stage, confirmed) · `blocked` (source exists, access fails) |
| `doc_type`, `doc_ref` | What and where (portal id, URL, process number) |
| `doc_design_matches` | `yes` / `no` / `unchecked` — does the document describe the plant GEM now carries (capacity, technology, turbine)? |
| `evidence` | CREA ladder, `methods_and_fields.md`: A, B, C, stack, hours, measured, limit-only |
| `basis` | Whether the number describes what the plant emits: `measured` · `reported-actual` · `design-hours` · `rate-only` · `potential` (8,760 h at full load, or from the limit) · `limit-only`. Defined in `methods_and_fields.md`. The headline count is plants with one of the first three, plus `rate-only` plants that have a defensible utilisation |
| `pollutants` | Which of NOx, SO2/SOx, PM, CO carry a number (not an asserted zero) |
| `rungs_tried` | Every source tried, in order |
| `last_checked`, `notes` | Date; anything else |

Values read from documents still go in `findings/` (one file per plant, from
`_template.md`); the tracker only points at them.

## Step 0, every country — survey WHERE emissions information lives

Before any per-plant work, and before trusting the source map in
`countries/<country>.md`: a deliberate, country-level search for every place
plant-level NOx / SOx / PM information for gas plants could be published. The
2026-09-17 maps were a by-product of chasing six plants each; they are deep on
EIAs and permits and nearly silent on everything else. An environmental
assessment or air permit is the ideal, but it may not exist or be reachable, so
the survey walks **every source class below and records an answer for each —
including "does not exist" and "exists, not public"**.

| # | Source class | What to establish |
|---|---|---|
| 1 | **Environmental assessment** (EIA / ESIA and its dispersion annex) | Who appraises (national / state / by size threshold); is the full study posted, where, since when; is there a register of all studies |
| 2 | **Air / environmental permit or licence** and its conditions | Same; does the permit state limits, rates, or nothing |
| 3 | **Public-consultation and hearing records** | Portals, gazettes, council minutes that attach or link the study |
| 4 | **Regulator's emissions reporting** — PRTR, annual self-reports, national emissions inventory with point sources | Dataset, granularity (plant? stack?), pollutants, years, known quality problems |
| 5 | **Continuous monitoring (CEMS) and periodic stack tests** | Is CEMS mandatory for gas plants; are data or compliance reports public |
| 6 | **Lender and ECA disclosure** | Which DFIs / ECAs finance gas power here; their disclosure pages |
| 7 | **Carbon-market and climate-finance documents** (CDM / JCM PDDs, monitoring reports) | Gas plants registered; PDDs carry technology, efficiency, generation, sometimes stack data |
| 8 | **Power-sector regulator and system operator** | Plant register, licensed names / SPVs, technology, dispatch and generation (for utilisation — CREA's method needs it) |
| 9 | **Company disclosure** — sustainability reports, securities filings, OEM / EPC press | Plant-level NOx / SOx / PM tonnes or intensities; turbine model, DLN / SCR |
| 10 | **Secondary compilations** — NGO / academic inventories, theses, journal papers using stack data | Who has already assembled this, from what, and will they share |
| 11 | **Emission standards** (the fallback tier) | Current and previous limits, reference conditions, applicability by size / zone / vintage |
| 12 | **Access-to-information route and people** | The FOI mechanism, turnaround; local NGOs, consultants, litigants who hold documents |

Method: search in the local language with the regulator's own terms; start from
the law (what must be produced, by whom, and what must be published) rather
than from plant names; test each candidate source on **two known plants** — one
pipeline, one operating — before calling it useful; give every source a status
label from `countries/README.md`. Time-box: about half a day per country.

Output: the "Where to look" section of `countries/<country>.md` rewritten so
that every class above has a row, plus a ranked **route list** — which sources
to enumerate, in what order, for the pipeline track and for the operating
track. The per-country steps below are then run against that route list, not
against yesterday's assumptions. For Vietnam and Brazil the expected result is
confirmation plus additions (classes 4, 5, 7, 8, 9, 10 are largely unexamined
in both); for any new country this step is the whole first day.

**Done for Vietnam and Brazil on 2026-09-18.** The source tables, route lists
and (Brazil) agency order are in `countries/vietnam.md` and
`countries/brazil.md`; the steps below have been adjusted to them. What it
changed, in short: Vietnam — no public PRTR, CEMS or CDM source exists, World
Bank documents cover the Phú Mỹ plants, and ĐTM appraisal was partly
decentralised to provinces in July 2025. Brazil — thermal plants ≥ 300 MW are
nominally IBAMA's (34 of the 65), RAPP reports per CNPJ and joins through
ANEEL SIGA, IPAAM-AM and INEMA-BA have open full-EIA libraries, INEA-RJ is
blocked.

The gaps the step was set to close (kept for the record): **Vietnam** — whether CEMS data are
published (mandatory transmission to provincial DONREs is known; publication is
not), EVN / PV Power / GENCO annual and sustainability reports, CDM / JCM
registrations, provincial ĐTM postings for sub-threshold plants. **Brazil** —
the exact RAPP dataset, CETESB and INEA stack-inventory publications, ONS / CCEE
generation by plant, ANEEL SIGA for licensed names, CDM PDDs for the 2000s gas
fleet, Eneva / Petrobras sustainability reports, IEMA's and SEEG's underlying
point-source tables.

## Vietnam — census of all 45 plants

Runs after Step 0; the steps below assume the portal is still the lead route.

**Status 2026-09-18:** steps 1–4 done. The inventory is `portal_inventory.py`,
the join is in `coverage/vietnam.csv`, the pipeline results are in the
`countries/vietnam.md` table, and the operating pilot is in
`findings/vietnam_gpmt_pilot_20260918.md`. Open: Long An and Quảng Trị CC
(one check each). Steps 5–6 are deferred. Current next steps are at the end
of `countries/vietnam.md`.

One licensor and one portal make a census cheap. Steps, in order:

1. **Enumerate the portal, completely.** Page through `/Home/DSDTM` (ĐTMs)
   and `/Home/DSGiayPhep` (permits) on `thamvan.mae.gov.vn` with each of:
   `LNG`, `điện khí`, `nhiệt điện`, `tua bin khí`, `chu trình hỗn hợp`, `Phú
   Mỹ`, `Nhơn Trạch`, `Cà Mau`, `Ô Môn`, and each of the 20 pipeline provinces.
   Pull `/XemChiTiet/XemChiTiet?id=N` for every hit. Save the raw inventory
   (id, title, owner, consultant, dates, files, **appraising body**) to
   `coverage/vietnam_portal_inventory.csv`. The appraising body on entries
   posted since July 2025 settles whether Decree 136/2025 has moved gas-plant
   ĐTMs to the provinces.
   Serial requests, ~8 retries (method in `countries/vietnam.md`).
2. **Join inventory to frame** on name / province / owner. This alone settles
   `located` vs nothing for all 45 rows, and surfaces gas ĐTMs for plants GEM
   does not carry (log as tracker leads).
3. **Pipeline, 24 plants.** 6 closed. For the 15 unsearched and the 3
   `not-found`: read every located ĐTM (10–15 min each: chapter 3 tables).
   For construction / pre-construction plants with no portal hit (Hiệp Phước,
   Quỳnh Lập, Ô Môn III / IV, Sơn Mỹ I / II, and whichever others) run the
   rest of the ladder once each: lender / ECA disclosure by sponsor nationality
   (JBIC / NEXI for JERA's Nghi Sơn; K-EXIM / K-SURE for KEPCO's Vũng Áng and
   Hải Lăng; DFC / US EXIM for AES's Sơn Mỹ II; EDF / Proparco for Sơn Mỹ I;
   Thai lenders for Cà Ná; SACE / SERV for Nhơn Trạch 3&4), and the
   **provincial portal** — no longer optional, since a ĐTM begun after July
   2025 may have been consulted on provincially. Announced plants with no
   portal hit close as `no-document-expected` after one news check that no ĐTM
   has been commissioned — no deeper.
4. **Operating, 7 plants + Cà Mau 1&2, Ô Môn I.** GPMT reports first (the
   World Bank Phú Mỹ table, already in hand, gives 2002 design NOx / SO2 for
   the five Phú Mỹ plants where a GPMT report is missing; one read each of the
   PVN 2024 sustainability report and an NT2 annual report): Phú Mỹ
   1, 2.1, 2.2, 3, 4, Bà Rịa, Nhơn Trạch 1, Cà Mau 1&2 (id 5894, located).
   These give **measured** NOx / CO / SO2 / dust with flow — the anchors for
   the PM and SO2 that ĐTMs assert as zero.
5. **Inactive, 14 plants.** Inventory join only (step 2). A cancelled LNG
   plant's ĐTM is still a valid design anchor if it turns up; do not hunt for
   one.
6. **Per-plant zone under QCVN 19:2024** for every pipeline plant — the ĐTM
   states the column; otherwise the provincial zoning, or assume the laxest.
   This completes the fallback tier for plants with no document.

Output: a coverage figure over 24 (and 45), by evidence type and pollutant, and
minutes per plant. Estimate: step 1–2 half a day (the portal is slow), step 3
one to two days, step 4 half a day.

## Brazil — all 65 resolved, a subset hunted

Brazil cannot be a census at scoping cost: ~20 state agencies, each a new
portal. So split cheap-for-all from expensive-for-some.

**Tier 0 — all 65 pipeline plants, desk work, no document hunting.** Fill
`licensor` and `licence_stage`:
- Match against the auction results (LRCAP 2026, and earlier A-4 / A-5 / A-6 /
  PCS lists from CCEE / EPE): a winner must hold a licence, so a study exists.
- **First**, ANEEL SIGA (one CSV; URL in `countries/brazil.md`, class 8) for
  the licensed name, SPV and **CNPJ** of every plant (naming misses were the
  commonest failure in the probes: Termo João Pessoa = Termoparaíba II,
  Jandaia = Portocem). The CNPJ is also the Tier 2 join key.
- IBAMA's licensing search (`servicos.ibama.gov.br/licenciamento/
  consulta_empreendimentos.php`, typology 9 "Usina Termelétrica") for every
  plant name and SPV. Thermal plants ≥ 300 MW are nominally IBAMA's (Decreto
  8.437/2015) — 34 of the 65, 16 of the hunting set — but states license many
  of them in practice, so this has to be looked up, not inferred. Plain
  `curl` works (tested 2026-09-18): GET the page for a session cookie, then
  POST `formDinAcao=Pesquisar&vartipologia=9` — 98 processes, one page. The
  method is in `countries/brazil.md`.
- The LRCAP result PDF on `ppi.gov.br` was serving a block page on 2026-09-18;
  take the auction lists from CCEE / EPE / ANEEL instead.

**Tier 1 — document hunt, agency by agency.** The hunting set is the **37
construction / pre-construction plants** (announced plants wait for Tier 0 to
show a licence). Order agencies by plants-per-portal-learned and known access:

The order was re-ranked after Step 0 and now lives in `countries/brazil.md`
("Route lists and agency order") — one copy, kept there. As of 2026-09-18:
**IBAMA first, largest plants first, if Tier 0 shows it holds more than a
handful of ours** (the Brazilian partner's advice: federal files are more
centralised, and EIAs begun after June 2025 follow a standard terms of
reference with an average-operation case — the likeliest source of a reasoned
rather than a potential estimate); batch what IBAMA does not post into LAI
requests at once. If IBAMA holds only a few, it drops back behind the open
libraries. Then IPAAM-AM → INEMA-BA → CETESB-SP → IEMA-ES → SEMAS-PA → ADEMA-SE → IMA-AL → CPRH-PE → INEA-RJ (blocked; partner,
Brazilian exit or LAI) → SEMAD-GO; SEMACE-CE and SUDEMA-PB stay LAI / partner
routes; IMASUL-MS, IAT-PR, SEMA-AP only if time remains. File LAI requests for
the known walls at the start of Tier 1, since they take 20–30 days.

Per agency: find the EIA/RIMA library and the public process lookup, enumerate
every thermal-plant entry (not just ours), join to the frame, then read. **Stop
rule:** two hours on an agency without reaching a document library → mark its
plants `blocked` or `not-found` with rungs, record the wall in
`countries/brazil.md`, move on. Lender disclosure (IFC, IDB Invest, BNDES) is
run once across all 37 by owner, not per plant.

Reaching CREA's 25 % (16–17 plants) needs ~13 more than the 3 in hand. The
four open libraries at the top of the order hold 10 hunting-set plants not yet
closed, so the
target depends on IBAMA's share or on one of SEMAS-PA / ADEMA-SE / IMA-AL
yielding full studies.

**Tier 2 — operating plants, bulk.** IBAMA RAPP open data
(`relatorio.csv`, URL in `countries/brazil.md`, class 4): one download, join
to the 50 + 3 operating plants on the CNPJ from SIGA — RAPP reports per CNPJ,
not per plant, so companies with several plants under one CNPJ need flagging.
Add ONS generation by plant for utilisation, flag IEMA's coherence verdicts
(NOx usable, SOx / PM mostly not). No per-plant hunting.

**Not covered in this pass:** the 28 announced plants beyond Tier 0, the 48
inactive plants, and plant-by-plant `design_matches` checks beyond those with
`found-values`.

## Order of work

0. **Step 0 source survey, both countries** — rewrite each country file's
   source table and route list before anything else.
1. Vietnam steps 1–2 (portal inventory + join) — slow, serial, runs unattended.
2. Brazil Tier 0 and Tier 2 in parallel with it — both bulk and scriptable.
3. Vietnam steps 3–6.
4. Brazil Tier 1, agencies in the order above.
5. Roll up: coverage by country × track × evidence × **basis** × pollutant from the two
   CSVs; update `countries/*.md` with every new source and wall.

## How far down the Brazil agency list

Not fixed in advance — the plan's own rules set it (agreed 2026-09-18):

- The agency order is provisional. Re-ranked once after Step 0 (done);
  **re-rank it again after Tier 0**, by hunting-set plants per agency and by what Step 0 found each agency
  publishes; IBAMA's share is unknown until then.
- Work down the re-ranked list. The two-hour stop rule bounds the cost of any
  one agency.
- **Stop when `found-values` reaches CREA's 25 % of pipeline plants (16–17)**
  with every agency tried so far written up in `countries/brazil.md`, or when
  the list is exhausted. Agencies never reached are reported as "untested", not
  as misses.
- If 25 % is reached early, the remaining effort goes to `design_matches`
  checks on the plants in hand, not to more agencies.
