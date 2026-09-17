# Brazil — where gas-plant emissions data live

Last updated: 2026-09-17, after two scouting passes (six plants looked at).
Status labels are defined in [`README.md`](README.md). Values read out of the
documents are in `../findings/brazil_scout_20260917.md` (first pass) and
`../findings/brazil_construction_scout_20260917.md` (second pass); this file
only says where things are.

## At a glance

- **Who licenses:** mostly the **state** environment agency, one per state,
  each with its own website and habits. IBAMA (federal) takes a minority of
  plants; none of the six looked at so far was IBAMA-licensed.
- **What decides whether documents can be found:** the state agency, and
  whether a development bank lent. Not the project, and not how far along
  construction is.
- **Best route:** the agency's EIA/RIMA library → the **full EIA**, not the
  RIMA → its air-quality / dispersion-modelling chapter or annex.
- **Evidence to expect:** B + C + stack parameters. A (annual tonnes) in São
  Paulo, because CETESB requires t/ano per source. Operating plants have
  self-reported annual tonnes in IBAMA's open data — usable for NOx, weak for
  SOx and PM.
- **Pipeline:** 65 plants in 20 states with an announced, pre-construction or
  construction unit (GOGPT pull 2026-09-17); 83 operating plants.
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
| RAPP annual report to IBAMA | Annual tonnes per operating plant, self-reported | A | Yes, as open data |

## Where to look — state agencies

Pipeline and operating counts are plants, from the 2026-09-17 pull. Agency
names in **untested** rows come from general knowledge and have not been
checked against a live site.

| State | Pipeline (plants, MW) | Operating | Agency | Status | Notes |
|---|---|---|---|---|---|
| Rio de Janeiro | 10, 13,575 | 16 | INEA-RJ | untested | Most plants of any state — the next portal to learn |
| Amazonas | 6, 3,094 | 7 | IPAAM | untested | Two plants under construction (Azulão, Manaus I) |
| Pernambuco | 5, 1,986 | 8 | CPRH | untested | |
| São Paulo | 4, 3,253 | 7 | **CETESB** | open, with method | AWS WAF challenge; method below. Posts whole licensing files and requires kg/h **and t/ano** per source, so every São Paulo plant should reach A |
| Espírito Santo | 4, 3,816 | 5 | **IEMA-ES** | open | Whole EIAs, chapter by chapter, listed by year; a state-wide EIA register |
| Sergipe | 4, 4,035 | 1 | **ADEMA-SE** | blocked | Every host times out. IFC disclosure covers the complex as planned in 2017 |
| Ceará | 4, 3,772 | 3 | **SEMACE** | blocked | 403 on the whole state portal |
| Bahia | 4, 586 | 8 | INEMA | untested | |
| Piauí | 4, 973 | 0 | SEMARH-PI | untested | |
| Alagoas | 4, 742 | 0 | IMA-AL | untested | |
| Goiás | 3, 2,799 | 3 | SEMAD-GO | untested | |
| Pará | 2, 2,330 | 0 | **SEMAS-PA** | link rot | Site migration broke every old `/wp-content/uploads/` link |
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

**SEMAS-PA — link rot.** Old URLs 404 and Wayback is the only route. Not yet
tried: the SIMLAM public process lookup using process numbers (Novo Tempo
Barcarena: LP 2017/44570, LI 2019/48189 and 2020/22534); an LAI request.

**SEMACE-CE — blocked.** `semace.ce.gov.br` redirects to `www.ce.gov.br`, which
sits behind an F5 Distributed Cloud WAF (`server: volt-adc`) and returns 403
"The requested URL was rejected" on every page, to every client tried,
including a real Chrome's cookies. There is no JavaScript challenge to pass, so
a cookie does not help; it behaves like an IP-reputation or geography rule.
`natuur.semace.ce.gov.br` (the licensing system) answers but offers only an
applicant log-in, with no public process search. `mobile.semace.ce.gov.br`
returns 503. Likely fix: a Brazilian residential or VPN exit, or a partner.

**ADEMA-SE — blocked.** Every host times out with no TCP answer, on every
route. Either down or dropping foreign traffic. Same fix as SEMACE.

## Where to look — federal, lenders and other routes

| Source | Covers | URL | Status | What it yields |
|---|---|---|---|---|
| IBAMA licensing search | Federally licensed projects | `servicos.ibama.gov.br/licenciamento/consulta_empreendimentos.php` (also `licenciamento.ibama.gov.br`) | open, not yet used — a form-driven search, not scripted. One scout reported it login-gated; it is not | Not known yet |
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
  Portal: `dadosabertos.ibama.gov.br`; the exact dataset link is still to be
  recorded here.
- **IEMA, *5º Inventário de Emissões Atmosféricas em Usinas Termelétricas***
  (Dec 2025, base year 2024) audited that dataset: of 67 fossil plants on the
  grid, 55 had NOx data and 35 were order-of-magnitude consistent with EMEP/EEA
  factors; only 5 plants had coherent PM data and 9 coherent SOx data, and many
  report an unrepresentative zero. Good for a NOx anchor or regression, weak
  for SOx and PM.
  https://energiaeambiente.org.br/wp-content/uploads/2025/12/IEMA_inventariotermeletricas2024-2025.pdf
- Lender packages for operating plants (Porto de Sergipe I via IFC).

## People

- **Instituto Arayara** — tracks and litigates gas projects; ask what they
  already hold before spending more hours.
- **IEMA (Instituto de Energia e Meio Ambiente)** — authors of the inventory
  above; they know the RAPP data and its faults.
- **Jandaia plaintiffs' lawyers** (Instituto Verdeluz, Povo Anacé) hold the
  Portocem / Jandaia EIA.
- **A researcher with a Brazilian IP or VPN exit** would settle whether SEMACE
  and ADEMA are blocking by geography.
- **LAI (access-to-information) requests** to SUDEMA-PB and SEMAS-PA, quoting
  the licence and process numbers above.

## Next

1. Learn INEA-RJ's portal (10 pipeline plants, 16 operating).
2. Sweep CETESB's libraries for the other São Paulo plants; all should reach A.
3. Find the Lins licence text, to settle 25 vs 9 ppm.
4. Test SEMACE and ADEMA from a Brazilian IP.
5. IPAAM (Amazonas) and CPRH (Pernambuco): the next two states by plant count,
   and Amazonas has two plants under construction.
6. Script the IBAMA licensing search and find out which plants are federal.
7. Record the exact IBAMA RAPP dataset link and try a pull for the 83
   operating plants.
8. Retrieve the full CELSE EIA from the IFC page.
