# Brazil — where gas-plant emissions data live

Last updated: 2026-09-18, after two scouting passes (six plants looked at) and
the Step 0 source survey, then the IBAMA process match.
Status labels are defined in [`README.md`](README.md). Values read out of the
documents are in `../findings/brazil_scout_20260917.md` (first pass) and
`../findings/brazil_construction_scout_20260917.md` (second pass); this file
only says where things are.

## At a glance

- **Who licenses:** on paper, IBAMA for any thermal plant of **300 MW or
  more** (Decreto 8.437/2015, art. 3º, VII, b, under LC 140/2011 art. 7º, XIV,
  h), the state agency below that. In practice the state agency very often
  licenses large plants too: processes begun before April 2015 stay where they
  started (art. 4º), and IBAMA can delegate. None of the six plants in the
  scouting passes was IBAMA-licensed, but that was a small sample: IBAMA's
  thermal-plant list (98 processes, matched 2026-09-18) holds Litos,
  TermoLinhares, Norte Fluminense 2, Geramar III, Tupã, Gaslub, Brasil
  Central, Centro Oeste, Queluzito, Porto Norte Fluminense and Araucária, and
  has new 2025–26 processes touching Porto de Sergipe, Presidente Kennedy and
  Jandaia (`../findings/brazil_ibama_20260918.md`). 34 of the 65
  pipeline plants (16 of the 37 under construction or in pre-construction) are
  ≥ 300 MW, so the licensor is still confirmed plant by plant.
- **What decides whether documents can be found:** the state agency, and
  whether a development bank lent. Not the project, and not how far along
  construction is.
- **Best route:** the agency's EIA/RIMA library → the **full EIA**, not the
  RIMA → its air-quality / dispersion-modelling chapter or annex.
- **Evidence to expect:** B + C + stack parameters, as full-load rates with no
  operating assumption (`rate-only`). São Paulo adds annual tonnes because
  CETESB requires t/ano per source, but the Lins figure is full load × 8,760 h
  — a **potential** emission, not an estimate. No Brazilian EIA read so far
  states operating hours. The actual figures are on the operating side:
  self-reported annual tonnes in IBAMA's open data, flagged measured,
  calculated or estimated — usable for NOx, weak for SOx and PM.
- **Pipeline:** 65 plants in 20 states with an announced, pre-construction or
  construction unit (GOGPT pull 2026-09-18); 53 gas plants with operating
  units (the 83 counted on 2026-09-17, and the per-state "Operating" column
  below, also include oil and blast-furnace-gas plants). Per-plant search
  state: `../coverage/brazil.csv`.
- **A licence implies a study.** Registering for an energy auction needs a
  valid environmental licence, so every LRCAP 2026 winner holds at least an LP
  and a study exists somewhere. Two catches: the study may describe an older
  design, and a conversion at an existing site may have been licensed on a
  simplified study with no dispersion modelling.

## Document types

| Document | What it holds | Evidence | Public? |
|---|---|---|---|
| **EIA** (Estudo de Impacto Ambiental), full | Emission inventory, source-parameter tables, dispersion study (usually AERMOD) | B, C, stack; A in São Paulo | Public by law; whether it is *posted* depends on the agency |
| **RIMA** (the public summary) | At best a concentration or two, without flow or context | C without flow | Usually the easiest file to find, and not enough |
| Whole licensing file (CETESB posts these) | EIA plus annexes, the agency's technical opinions and the developer's replies | A + B + C + stack, plus the argument over which limit applies | São Paulo |
| Licensing form / annexes | Occasional annual figure | A, single number, basis unclear | São Paulo |
| Licences: LP → LI → LO | The emission limit actually imposed | permitted | Rarely posted; not yet found for any plant |
| State environment-council decisions (e.g. COPAM) | That a licence exists, its number, the licensed plant names | none | Yes |
| RAS / simplified study | May have no dispersion modelling at all | — | Suspected for conversions; none seen yet |
| Lender ESIA package (IFC, IDB Invest) | Full ESIA and dispersion annexes, as of financial close | B, C, stack | Yes |
| RAPP annual report to IBAMA | Annual tonnes per operating plant, self-reported for the actual year (`measured` or `reported-actual`, by the method flag) | A | Yes, as open data |

## Where to look — by source class

Source survey of 2026-09-18 (Step 0 of `../search_plan.md`): every one of the
twelve classes has a row, including the empty ones. Candidates were tried on
pipeline plants (Azulão, Manaus III) and operating ones (GNA I, Porto de
Sergipe I). Two extra labels: **does not exist** and **exists, not public**.

| # | Class | Source | URL | Status | What it yields |
|---|---|---|---|---|---|
| 1 | Environmental assessment | State agency EIA/RIMA libraries — one per state, table below. No national register of studies | below | varies by agency | Full EIA: B + C + stack; A in São Paulo |
| 1 | | PNLA, the national licensing portal | — | per the partner, a directory of state sites rather than a searchable database; not tested | Nothing of its own |
| 1 | | IBAMA, for federally licensed plants | `servicos.ibama.gov.br/licenciamento/consulta_empreendimentos.php` | open, with method — an old PHP form, no login or captcha. GET the page for a session cookie, then POST `formDinAcao=Pesquisar&vartipologia=9` (9 = "Usina Termelétrica"): 98 processes on one page, all fuels. Each row is a form carrying `processo` and `cod_empreendimento`; its stage cells (TR, studies, hearing, LP, LI, LO) are colour-coded. POST `modulo=empreendimento&cod_empreendimento=<n>` for the developer and status; add `formDinAcao=Documentos do processo` for the document list. Page encoding is Latin-1 | Process number, plant name, developer and CNPJ, state (often blank), licensing stage, no opening date. The documents tab lists **licences, authorisations and pareceres, not the EIA**, and is empty for 58 of 98; a listed document opens via `formDinAcao=btngdAbrir` → `modulos/documentos.php?cod_documento=<id>`. All 98 and the method: `../findings/brazil_ibama_20260918.md` |
| 1 | | **IBAMA study library (SharePoint)**, where IBAMA keeps the EIAs | `licenciamento.ibama.gov.br` (Cloudflare challenge; passes with `curl_cffi` Chrome impersonation) redirects to an anonymous share link into `https://ibamagovbr.sharepoint.com/sites/EstudosAmbientais/Documentos Compartilhados/Licenciamento/Termeletricas` | open, with method — take the `FedAuth` cookie from the share-link redirect, then SharePoint REST (`_api/web/GetFolderByServerRelativeUrl(…)/Folders`, `/Files`; `GetFileByServerRelativeUrl(…)/$value`) | 33 project folders: full EIA + RIMA for Litos and NSF (2017–20), a SEI dossier export for TermoLinhares, a RAS for Suape 5 (4,380 h/yr stated; only CONAMA limits). Processes still before their EIA (Porto de Sergipe 2026, NSF 1 e 2, Araucária) have nothing yet. SEI public search (`sei.ibama.gov.br`) is captcha-gated: manual only, for dates |
| 2 | Licence and conditions | State licence lists and council decisions: IPAAM "licenças concedidas" spreadsheets (https://www.ipaam.am.gov.br/licencas-ambientais-concedidas/), SUDEMA COPAM decisions, SEMAS-PA SIMLAM | — | open | That a licence exists, its number and holder. Licence texts with emission limits: not found for any plant |
| 3 | Consultation and hearing records | Hearing notices (agency sites, state gazettes); Querido Diário, a search API over municipal gazettes | https://queridodiario.ok.org.br | open; the API query syntax still to be worked out | Notices that sometimes link the proponent's document folder (Jandaia). Not yet run on a plant |
| 4 | Emissions reporting | **IBAMA RAPP — "Emissões de poluentes atmosféricos"** | https://dadosabertos.ibama.gov.br/dados/RAPP/emissoesPoluentesAtmosfericos/relatorio.csv (59 MB, `;`-separated) | open | Annual tonnes per **CNPJ** (not per plant or stack), 2013–2025, by pollutant (NOx, CO, MP, SOx), with the method (Medição / Cálculo / Estimativa) and activity category. 366 CNPJs under "Produção de energia termoelétrica", 212 of them with NOx for 2023 or 2024. Test: UTE GNA I, NOx 1,294 / 301 / 1,250 / 1,637 t for 2021–24, measured. No plant id — join on CNPJ from ANEEL SIGA. A company with several plants under one CNPJ reports one figure |
| 4 | | State stack-source inventories: CETESB's annual air-quality report (RQAR); INEA's fixed-source monitoring programme | `cetesb.sp.gov.br/ar/` | CETESB: open, with method (WAF; a fresh token for `/ar/` not yet tried). INEA: blocked | Whether RQAR lists emissions per company is unconfirmed |
| 5 | CEMS and stack tests | Required by licence conditions and, in Rio de Janeiro, by Conema 84/2018; results go to the agency | — | **exists, not public** | The RAPP "Medição" flag is the only public trace |
| 6 | Lenders and ECAs | IFC (Sergipe 39652; GNA I 40314), IDB Invest, KfW IPEX (GNA I, press only), BNDES | `disclosures.ifc.org` | open (IFC, IDB Invest); BNDES untested | Full ESIA with dispersion annexes where IFC lent |
| 7 | Carbon market | CDM registry | `cdm.unfccc.int` | **does not exist** — no gas-fired power PDD found for Brazil | — |
| 8 | Power regulator and operator | **ANEEL SIGA** | https://dadosabertos.aneel.gov.br/dataset/6d90b77c-c5f5-4d81-bdec-7bc619494bb9/resource/11ec447d-698d-4ab8-977f-b424d5deee6a/download/siga-empreendimentos-geracao.csv (8 MB, `;`-separated) | open | Licensed plant name, CEG code, state, municipality, phase (Operação / Construção / not started), fuel, kW, coordinates, and **owner with CNPJ** — the key to both the naming problem and the RAPP join |
| 8 | | ONS open data, "Geração por Usina"; CCEE open data | `dados.ons.org.br` | open | Hourly generation per plant → utilisation |
| 8 | | Auction results and EPE's lists of qualified projects | LRCAP 2026 result PDF on `ppi.gov.br` | **blocked** as of 2026-09-18 — the government WAF serves a block page with HTTP 200; not in Wayback. Try CCEE / EPE / ANEEL copies | Which plants must already hold a licence |
| 9 | Company disclosure | Eneva, Petrobras, GNA sustainability reports and CVM filings | investor-relations sites | open | Corporate totals and method text only; no per-plant NOx / SOx / MP found. Filings remain the check on what is actually being built |
| 10 | Secondary compilations | IEMA's thermoelectric inventory (PDF; see "Operating-plant data") and its plant map `usinas.energiaeambiente.org.br`; SEEG | — | open | The inventory's plant tables exist only in the PDF — ask IEMA for them. The map has no emissions fields. SEEG is greenhouse gases only |
| 11 | Emission standards | CONAMA 382/2006 (new sources), 436/2011 (sources licensed before 2 Jan 2007); air-quality standards CONAMA 491/2018 → 506/2024 | see "National limits" | open | Fallback tier |
| 12 | Access to information, people | LAI (Lei 12.527/2011): 20 days + 10, through Fala.BR for federal bodies and each state's e-SIC; Lei 10.650/2003 for environmental information | — | open, not yet used | The route for licence texts, CEMS reports and studies an agency does not post |

## Where to look — state agencies

Pipeline and operating counts are plants, from the 2026-09-17 pull. Agency
names in **untested** rows come from general knowledge and have not been
checked against a live site.

| State | Pipeline (plants, MW) | Operating | Agency | Status | Notes |
|---|---|---|---|---|---|
| Rio de Janeiro | 10, 13,575 | 16 | **INEA-RJ** | blocked | Every host refuses or times out from a US address. The library page (read via Wayback) says studies are consulted in person. Most plants of any state |
| Amazonas | 6, 3,094 | 7 | **IPAAM** | open | Library with a page per project: Azulão, Manaus I / II (RIMA), Manaus III (full EIA), Itacoatiara, Eneva Silves–Itapiranga, Sparta |
| Pernambuco | 5, 1,986 | 8 | **CPRH** | open, with method | Bad TLS certificate (`curl -k`); the library is a JavaScript page. Only a simplified study (RAS, Pernambuco III) found so far |
| São Paulo | 4, 3,253 | 7 | **CETESB** | open, with method | AWS WAF challenge; method below. Posts whole licensing files and requires kg/h **and t/ano** per source, so every São Paulo plant should reach A — but check the hours behind it: at Lins the t/ano is 8,760 h at full load (`potential`) |
| Espírito Santo | 4, 3,816 | 5 | **IEMA-ES** | open | Whole EIAs, chapter by chapter, listed by year; a state-wide EIA register |
| Sergipe | 4, 4,035 | 1 | **ADEMA-SE** | open, unexplored | Answering again on 2026-09-18 (`adema.se.gov.br`, with an "estudos ambientais" page); was timing out on 09-17. IFC disclosure covers the complex as planned in 2017 |
| Ceará | 4, 3,772 | 3 | **SEMACE** | blocked | 403 on the whole state portal |
| Bahia | 4, 586 | 8 | **INEMA** | open | Library with full EIAs in volumes (UTE Global VII, Sulbahia 1, Barra do Rocha I). The process-lookup host times out |
| Piauí | 4, 973 | 0 | SEMARH-PI | untested | |
| Alagoas | 4, 742 | 0 | **IMA-AL** | open | RIMAs only (UTE Pilar Nova); no full EIA found |
| Goiás | 3, 2,799 | 3 | SEMAD-GO | untested — no library found; the portal is a JavaScript application that needs a browser | |
| Pará | 2, 2,330 | 0 | **SEMAS-PA** | link rot for old files; process lookup open | Site migration broke every old `/wp-content/uploads/` link. SIMLAM public lookup answers — not yet queried |
| Paraíba | 2, 347 | 3 | **SUDEMA-PB** | open | Council (COPAM) decisions only — no studies posted |
| Maranhão | 2, 2,192 | 3 | SEMA-MA | untested | |
| Mato Grosso do Sul | 2, 330 | 2 | IMASUL | untested | |
| Paraná | 1, 369 | 2 | IAT-PR | untested | |
| Rio Grande do Sul | 1, 1,238 | 4 | FEPAM | untested | |
| Minas Gerais | 1, 630 | 4 | SEMAD-MG / FEAM | untested | |
| Santa Catarina | 1, 93 | 0 | IMA-SC | untested | |
| Amapá | 1, 242 | 0 | SEMA-AP | untested | |

States with operating plants only: Roraima 2, Rio Grande do Norte 2, Acre 1,
Mato Grosso 1, Rondônia 1.

Six states — Rio de Janeiro, Amazonas, Pernambuco, São Paulo, Espírito Santo
and Sergipe — hold 33 of the 65 pipeline plants. Learn agencies in that order
rather than going plant by plant.

Name collision: **IEMA-ES** is Espírito Santo's state agency. **IEMA**
(Instituto de Energia e Meio Ambiente) is the São Paulo NGO behind the
thermoelectric emissions inventory.

### Agency detail

**IPAAM-AM — open.**
- Library: https://www.ipaam.am.gov.br/eia-rima-site/ — one page per project,
  PDFs under `/wp-content/uploads/`.
- Full EIA confirmed: UTE Manaus III (38 MB),
  `http://www.ipaam.am.gov.br/wp-content/uploads/2024/03/EIA-MANAUS-III-site.pdf`,
  with an air-quality chapter; values not yet read.
- Licences granted, as spreadsheets:
  https://www.ipaam.am.gov.br/licencas-ambientais-concedidas/

**INEMA-BA — open.**
- Library: https://www.ba.gov.br/inema/estudos-ambientais/avaliacao-ambiental/eia-rima
- Full EIA confirmed: UTE Global VII, vol. I (50 MB),
  `https://www.ba.gov.br/inema/sites/site-inema/files/migracao_2024/arquivos/wp-content/files/EIA.pdf`.
  None of the four Bahia pipeline plants has been looked for yet.

**INEA-RJ — blocked.** `inea.rj.gov.br`, the licensing portal and the
air-quality system all refuse or time out, to curl and to the fetch tool
(2026-09-18, three separate attempts). Wayback shows the site's structure only. Behaves
like a geography rule; same likely fix as SEMACE.

**IEMA-ES — open.**
- EIAs by year: `https://iema.es.gov.br/GrupodeArquivos/EIA-<year>` (2013 list:
  https://iema.es.gov.br/GrupodeArquivos/EIA-2013-2). Chapter PDFs sit under
  `iema.es.gov.br/media/CQAI/EIA/<year>/<project folder>/`.
- State-wide EIA register, the way into every other Espírito Santo plant:
  https://iema.es.gov.br/Media/iema/EIA-RIMA/EIA/Relacao_EIA_IEMA_site_24.02.2026.pdf
- RIMAs: `iema.es.gov.br/Media/iema/Downloads/RIMAS/RIMAS_<year>/`.

**CETESB-SP — open, with method.**
- Files are named by process number and year:
  `/eiarima/eia/EIA_<n>_<yyyy>.pdf`, `/eiarima/rima/RIMA_<n>_<yyyy>.pdf`,
  `/eiarima/anexos/ANEXOS_<n>_<yyyy>.pdf`. Seen so far: the Lins EIA on
  `www2.cetesb.sp.gov.br`, its RIMA and ANEXOS on `cetesb.sp.gov.br` (Wayback
  copies). Try both hosts.
- Older library index (661 files):
  `https://www2.cetesb.sp.gov.br/licenciamentoambiental/eia-rima/`
- The wall is an AWS WAF JavaScript challenge: HTTP 202, header
  `x-amzn-waf-action: challenge`, empty body to any script. What works: open
  the site once in a real Chrome, take the `aws-waf-token` cookie, replay it in
  curl with the same User-Agent. `scripts/cf_clearance.py` (`cookie_for(url)`)
  in the sibling `lng-terminals-researcher` repo automates this. The token
  lasts minutes to hours; large files need `curl -C -` to resume.
- Files are whole licensing processes — Lins is 272 MB, 3,305 pages,
  image-only. Budget about an hour of OCR (tesseract, `por`) on 8 cores and
  read the tables from page images; tables OCR badly.
- Wayback holds some RIMA and ANEXOS files.

**SUDEMA-PB — open, but only decisions.** COPAM deliberations by year under
`sudema.pb.gov.br/institucional/copam-1/deliberacoes/<year>/`. They give
licence numbers and the *licensed* plant names, which can differ from the
tracker's (Termo João Pessoa is licensed as UTE Termoparaíba II and siblings).
The studies need an access-to-information (LAI) request or a partner.

**SEMAS-PA — link rot, lookup open.** Old URLs 404 and Wayback is the only
route to them. The SIMLAM public process lookup answers
(`https://monitoramento.semas.pa.gov.br/simlam/`); next is to query it with
the known process numbers (Novo Tempo Barcarena: LP 2017/44570, LI 2019/48189
and 2020/22534). Then an LAI request.

**SEMACE-CE — blocked.** `semace.ce.gov.br` redirects to `www.ce.gov.br`, which
sits behind an F5 Distributed Cloud WAF (`server: volt-adc`) and returns 403
"The requested URL was rejected" on every page, to every client tried,
including a real Chrome's cookies. There is no JavaScript challenge to pass, so
a cookie does not help; it behaves like an IP-reputation or geography rule.
`natuur.semace.ce.gov.br` (the licensing system) answers but offers only an
applicant log-in, with no public process search. `mobile.semace.ce.gov.br`
returns 503. Likely fix: a Brazilian residential or VPN exit, or a partner.

**ADEMA-SE — open, unexplored.** Timed out on every route on 2026-09-17;
answered normally on 09-18, so it was an outage or an intermittent rule.
`https://adema.se.gov.br/estudos-ambientais-2/` is the studies page; not yet
walked.

## Route lists and agency order

**Pipeline track**
1. **Tier 0 first, for all 65:** ANEEL SIGA for the licensed name, SPV and
   CNPJ; then the licensor — IBAMA's search, by `curl` (34 plants
   are ≥ 300 MW and could be federal), auction lists for who must hold a
   licence.
2. Agency libraries, in the order below.
3. IFC / IDB Invest / BNDES once across all owners.
4. Querido Diário and state gazettes for hearing notices, for plants whose
   agency posts nothing.
5. LAI requests, started early for the known walls since they take 20–30 days.
6. CONAMA 382 limit as the fallback.

**Agency order for the document hunt** (re-ranked 2026-09-18 by hunting-set
plants × what the agency is known to post; to be re-ranked again after Tier 0
shows IBAMA's share):

| Order | Agency | Hunting-set plants | Why here |
|---|---|---|---|
| 1 | IPAAM-AM | 5 | Open library; every one of the five has a page; one full EIA confirmed |
| 2 | INEMA-BA | 4 | Open library with full EIAs; our four not yet looked for |
| 3 | CETESB-SP | 1 done + 3 announced | Method known; the only route to evidence A |
| 4 | IEMA-ES | 2 (1 done) + 2 announced | Open; state register makes it a short sweep |
| 5, or first | IBAMA | 11 confirmed + several ambiguous (matched 2026-09-18) | Holds more than a handful, so **goes first, largest plants first** (partner's advice); studies are on IBAMA's SharePoint and scriptable. Its 2025–26 processes have no EIA yet; post-June-2025 EIAs will follow the standard terms of reference |
| 6 | SEMAS-PA | 2 | SIMLAM answers and process numbers are in hand |
| 7 | ADEMA-SE | 1 + 3 announced | Reachable again; library unexplored |
| 8 | IMA-AL | 4 | Open but RIMA-only so far; all engines — the non-CCGT case |
| 9 | CPRH-PE | 3 | Reachable with method; nothing for our plants yet |
| 10 | INEA-RJ | 5 + 5 announced | Most plants, but blocked and reportedly in-person only: partner / Brazilian exit / LAI rather than scripted attempts |
| 11 | SEMAD-GO | 3 | No library found |
| — | SEMACE-CE (1), SUDEMA-PB (2) | | Known walls, not re-tested: LAI or partner |
| — | IMASUL-MS (2), IAT-PR (1), SEMA-AP (1) | | Sites answer; unexplored; only if time remains |

**Operating track**
1. IBAMA RAPP CSV, joined to the frame on CNPJ taken from ANEEL SIGA.
2. IEMA's inventory for the coherence verdict per plant (ask IEMA for the
   tables).
3. ONS generation by plant, for utilisation and to turn RAPP tonnes into
   intensities.
4. IFC / IDB Invest packages for the DFI-financed plants (GNA I, Porto de
   Sergipe I).
5. Nothing else: CEMS and stack tests are not public, company reports have
   no per-plant figures, there are no CDM documents.

## Where to look — federal, lenders and other routes

| Source | Covers | URL | Status | What it yields |
|---|---|---|---|---|
| IBAMA licensing search and study library | Federally licensed projects | `servicos.ibama.gov.br/licenciamento/consulta_empreendimentos.php`; studies on IBAMA's SharePoint via `licenciamento.ibama.gov.br` | open, scripted — see the source table, class 1 | Process list and licences; full EIAs where the process has reached the study stage |
| IFC disclosure | DFI-financed plants | https://disclosures.ifc.org/project-detail/ESRS/39652/celse (CELSE / Porto de Sergipe I, ~60 PDFs) | open | Full ESIA and dispersion annexes: B + C + stack |
| IDB Invest | same | project 12048-01; https://idbinvest.org/sites/default/files/2018-12/celse_esrs_esap_final_oct_17_0eng.pdf | open | Summaries only |
| BNDES | domestically financed plants | — | untested | Novo Tempo Barcarena was reported as BNDES plus private funds; no disclosure found |
| Auction results (LRCAP 2026) | Which plants must already hold a licence | https://ppi.gov.br/wp-content/uploads/2026/03/Resultado-geral-1.pdf | open | No emissions; narrows the search |
| Company filings (Fatos Relevantes) | What is actually being built — capacities, COD, ownership | via the investor-relations site; Eneva's Jandaia filing is linked from the findings file | open | No emissions; needed to check the licence describes the same machine |
| Public-hearing notices | Links to the hearing's document folder | Varies; the Jandaia 500 kV line EIA was in a public Google Drive folder linked from the notice | open when found | Whatever the proponent uploaded |
| Litigation | Plaintiffs' lawyers hold the EIA | Jandaia: Instituto Verdeluz + Povo Anacé climate suit, 2023 | people route | — |
| Wayback | Files lost to site migrations, older CETESB files | see `README.md` | unreliable on 2026-09-17 | — |

## Documents in hand

Evidence codes as in the ladder. "Permitted as predicted" means the modelled
NOx is exactly the CONAMA limit.

| Plant (state) | Document, date | URL | Evidence | Caveat | Values in |
|---|---|---|---|---|---|
| Presidente Kennedy (ES) | Full EIA, 2013, chapters 1, 2, 7; RIMA | IEMA-ES 2013 list, above | B + C + stack + coordinates | NOx and CO are the legal limit × design flow. 2013 GERA project, MHI M501J; Eneva's current design not checked | first pass |
| Lins (SP) | Whole CETESB process 249/2018: EIA, annexes, opinions, replies | `https://www2.cetesb.sp.gov.br/eiarima/eia/EIA_249_2018.pdf` | **A + B + C + stack** | 2018 design (3 × GE 7HA.02), not the 732.7 MW plant contracted in 2026. Whether the licence set 25 or 9 ppm NOx is not determined | second pass |
| Lins (SP) | RIMA and ANEXOS | Wayback copies, URLs in the first-pass file | C without flow; one annual NOx figure | The two RIMA tables disagree with each other | first pass |
| Porto de Sergipe I + Gov. Marcelo Deda + Laranjeiras I (SE) | "Anexo II — Estudo de dispersão atmosférica do complexo termelétrico", Sept 2017, in the IFC package | IFC 39652, above | B + C + stack + coordinates | The complex as planned in 2017. NOx and CO at the CONAMA limit. No hours. GEM carries Governador Marcelo Deda and Laranjeiras as separate announced plants; whether they are still these designs is unchecked. The PDF carries its author's personal contact details — do not copy them | second pass |
| Termo João Pessoa (PB) | COPAM Deliberação 5.821, 16 Dec 2025 | https://sudema.pb.gov.br/institucional/copam-1/deliberacoes/2025/deliberacao-5821-homologacao.pdf | none | Proves LP 3320/2025 exists | first pass |
| Novo Tempo Barcarena (PA) | SEMAS compensation fact-sheet | Wayback copy, URL in the second-pass file | none | Cites "RIMA (págs. 15-39)", so a RIMA exists | second pass |
| Jandaia (CE) | 2023 EIA for the associated 500 kV line | public Drive folder from the hearing notice | none (ambient baseline only) | The plant's own EIA is with SEMACE | second pass |

Known to exist, not retrieved: the full CELSE EIA
(`GN_UTE_ESIA_EIA_UTE_rev00_v06.pdf`, on the IFC page); the Lins licence text;
the Novo Tempo Barcarena and Jandaia EIA/RIMAs; whatever study underlies the
Paraíba LPs.

## Inside the document

- Go to the full EIA's prognosis / air-quality chapter — "Prognóstico",
  "Qualidade do ar", "Emissões atmosféricas" — and the annex "Estudo de
  dispersão atmosférica". The tables wanted are the emission inventory and the
  source parameters (model inputs).
- Search terms: `EIA RIMA "UTE <nome>"`, `estudo de dispersão atmosférica`,
  `emissões atmosféricas`, `chaminé`, `taxa de emissão`, `g/s`, `kg/h`,
  `t/ano`, `mg/Nm³`, `licença prévia`. For hours: `horas`, `fator de
  capacidade`, `8.760`.
- **Check whether "predicted" is really "permitted".** If modelled NOx is
  50 mg/Nm³ and CO 65, the modellers used the CONAMA 382 limit × design flow
  (Kennedy, Sergipe). About 18 mg/Nm³ is the 9 ppm case CETESB recommends.
- Annual tonnes, where given, are 8,760 h at full load (Lins).
- **IBAMA's standard terms of reference for thermal-plant EIAs (26 June 2025)**
  — for new federal processes only. It requires emissions in g/s **and**
  t/ano, rates per MWh, stack height, temperature, flow, exit velocity and
  SIRGAS coordinates, the calculation memo and emission factors, and a
  dispersion study at full load (critical), **average operation (typical)**
  and start-up. The typical case is the one that gives a reasoned estimate
  rather than a potential one. The capacity-factor-versus-100 % pair is
  required explicitly only for greenhouse gases, so check what hours the
  pollutant t/ano rests on. For gas it lists NOx, CO, CO2, COV and O3 as the
  minimum; PM and SO2 are on the coal list — expect them only where a liquid
  backup fuel is licensed (a screening variable). PDF:
  https://www.gov.br/ibama/pt-br/assuntos/notas/2025/ibama-publica-novo-termo-de-referencia-para-estudo-de-impacto-ambiental-de-usinas-termeletricas/2025-06-26_tr_termeletricas_revisao_pos_consulta_final.pdf
  (the note page itself is login-gated to scripts; the PDF path is not).
  EIAs older than mid-2025 do not follow it.
- Where tonnes are missing, the turbine specification, exhaust flow and stack
  parameters give a rate (`rate-only`), and ANP's gas-specification sulphur
  ceiling gives an SO2 upper bound — a bound, to be labelled `potential`.
- SOx is typically computed from 70 mg/m³ sulphur in the gas, not measured or
  guaranteed. MP, SO2 and COV have no legal limit for gas turbines, so those
  rates are design or factor values.
- Brazilian number format: decimal comma, thousands point. CETESB's licensing
  form uses English format, so check which one a table is in.
- The licensed project is often not the one being built (Kennedy 2013, Lins
  2018, Jandaia licensed as UTE Portocem). Record the design the document
  describes. GEM also lists a Portocém plant in Pará — different site, not
  looked at.

## National limits (fallback tier)

CONAMA Resolution 382/2006, Annex V — gas turbines for power generation on
natural gas: **NOx 50 mg/Nm³ as NO2, dry basis, 15 % O2**; CO 65 mg/Nm³; NOx
135 mg/Nm³ on liquid fuel. No limit for PM or SOx on gas. Still to read: the
applicability thresholds, and CONAMA 436/2011 for older sources. CETESB
recommends 9 ppm (about 18 mg/Nm³) and argued for it in the Lins file; state
practice can be tighter than the federal limit.

## Operating-plant data

- **IBAMA open data — RAPP reports.** Annual NOx, SOx, PM and CO tonnes per
  thermal plant, as reported by operators. Evidence type A, self-reported.
  Dataset and fields: class 4 in the source-class table. It reports per CNPJ,
  so plants sharing a company need splitting by other means.
- **IEMA, *5º Inventário de Emissões Atmosféricas em Usinas Termelétricas***
  (Dec 2025, base year 2024) audited that dataset: of 67 fossil plants on the
  grid, 55 had NOx data and 35 were order-of-magnitude consistent with EMEP/EEA
  factors; only 5 plants had coherent PM data and 9 coherent SOx data, and many
  report an unrepresentative zero. Good for a NOx anchor or regression, weak
  for SOx and PM.
  https://energiaeambiente.org.br/wp-content/uploads/2025/12/IEMA_inventariotermeletricas2024-2025.pdf
- Lender packages for operating plants (Porto de Sergipe I via IFC).

## People

- **Instituto Arayara** — tracks and litigates gas projects. In contact
  through CREA (2026-09-18): they advise starting with a sample of the large
  IBAMA-licensed plants, and have offered to help define it and to file the
  LAI requests for whatever is not published. Their experience: refusals
  usually cite commercial confidentiality over technical annexes, are
  appealable and often reversed; federal requests go through Fala.BR.
- **IEMA (Instituto de Energia e Meio Ambiente)** — authors of the inventory
  above; they know the RAPP data and its faults.
- **Jandaia plaintiffs' lawyers** (Instituto Verdeluz, Povo Anacé) hold the
  Portocem / Jandaia EIA.
- **A researcher with a Brazilian IP or VPN exit** would settle whether SEMACE
  and ADEMA are blocking by geography.
- **LAI (access-to-information) requests** to SUDEMA-PB and SEMAS-PA, quoting
  the licence and process numbers above.

## Next

1. Work the agencies in the order under "Route lists and agency order";
   INEA-RJ needs a partner, a Brazilian exit or an LAI request.
2. Sweep CETESB's libraries for the other São Paulo plants; all should reach A.
3. Find the Lins licence text, to settle 25 vs 9 ppm.
4. Test SEMACE and ADEMA from a Brazilian IP.
5. IPAAM first (five plants, all with library pages), then INEMA-BA.
6. IBAMA's 98 processes are matched (2026-09-18; `coverage/brazil.csv` and
   `../findings/brazil_ibama_20260918.md`). Next: read the air chapters of the
   IBAMA-held EIAs, largest first (Litos, TermoLinhares, Norte Fluminense 2,
   Geramar III); resolve the flagged ambiguous matches; get opening dates for
   the 2025 processes from SEI by hand.
7. RAPP join: 10-plant pilot done (2026-09-18,
   `../findings/brazil_rapp_pilot_20260918.md`); 5 full NOx series, 2 partial,
   3 unusable. SIGA's owner CNPJ is rarely the filer; match by operator name,
   town and the CNPJ registry. Next: the other 40 operating plants, then ONS
   generation to check the tonnes.
8. Retrieve the full CELSE EIA from the IFC page.
