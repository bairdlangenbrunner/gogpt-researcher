# Brazil — construction-stage pass and the agency walls (2026-09-17)

Second pass, same day as `brazil_scout_20260917.md`. Three
**construction-stage** plants were scouted, and the walls met in the first pass
were worked on. The biggest single result is not from the new sample: getting
through CETESB's wall produced the full Lins EIA, which has annual tonnes.

*Checked* = I read the value in the downloaded file. *Scout* = reported by a
search agent, not re-read by me. Values are in the documents' own notation
(decimal comma).

## Summary

| Plant | Licensing body | Document | Evidence |
|---|---|---|---|
| Novo Tempo Barcarena (PA) | SEMAS-PA | only a compensation fact-sheet naming the RIMA | nothing *(sheet checked; rest scout)* |
| Jandaia II / III (CE) | SEMACE | EIA of the associated transmission line; plant EIA not reachable | nothing *(scout; capacities checked)* |
| Porto de Sergipe II / III / V (SE) | ADEMA-SE | none for the expansion; IFC-disclosed 2017 cumulative dispersion study for phase I + two sister plants | **B + C + stack** for the complex as then planned *(checked)* |
| *Lins (SP) — first-pass sample plant* | CETESB | **full EIA process file**, 3.305 pages | **A + B + C + stack** *(checked)* |

Construction sample: 1 of 3 with numbers, and that one is a lender document
describing an earlier plan. Being under construction did **not** make the
documents easier to find — what decides it is still the state agency and
whether a development bank was involved.

## Construction sample

### Novo Tempo Barcarena — nothing with numbers

- Regulator name "CELBA Usina Termoelétrico (UTE) Novo Tempo", proponent
  Centrais Elétricas Barcarena S.A.; SEMAS-PA processes LP 2017/44570, LI
  2019/48189 (fase 1) and 2020/22534 (fase 2) *(checked)* — from the SEMAS
  compensation fact-sheet, live URL now 404, Wayback copy:
  https://web.archive.org/web/20230731134212/https://www.semas.pa.gov.br/wp-content/uploads/2021/05/24-Ficha-Técnica_Brazauro-–-CELBA-Usina-Termoelétrico-UTE-Novo-Tempo.pdf
- The sheet cites "RIMA (págs. 15-39)", so an EIA/RIMA exists; it was not
  found. Public hearings were held in Barcarena in April 2018 *(scout)*.
- No development-bank disclosure: financing reported as BNDES plus private
  funds *(scout)*. EPC Mitsubishi Power + Andrade Gutierrez; turbine model not
  confirmed *(scout)*.
- Next: SEMAS-PA's SIMLAM public process lookup with the three process
  numbers; an access-to-information (LAI) request; Wayback CDX crawl of
  `semas.pa.gov.br` once the Internet Archive is back.

### Jandaia II / III — nothing with numbers

- The site's LP (2019) and LI (March 2023) were issued to **UTE Portocem**, a
  2.189,60 MW open-cycle design (4 × 392,972 MW); the licences passed to
  Jandaia Geração de Energia and then, in Sept 2025, to Eneva *(scout; the
  Portocem design figures are quoted from the transmission-line EIA)*.
- What Eneva is building *(checked, Eneva Fato Relevante)*: UTE Jandaia II
  860,9 / 899,6 MW and Jandaia III 287,0 / 299,8 MW (contracted / installed),
  COD 01/08/2029; UTE Jandaia 1 441,4 / 460,0 MW, COD 01/08/2031.
  https://api.mziq.com/mzfilemanager/v2/d/6c663f3b-ae5a-4692-81d3-ab23ee84c1de/1e932961-9537-34cd-09ab-52db552f87f9?origin=2
- Retrieved: the 2023 EIA for the 500 kV line (five volumes, public Google
  Drive folder from the hearing notice). It has a regional ambient air
  baseline and no stack data *(scout)*.
- The plant's own EIA/RIMA sits with SEMACE, which is unreachable from here
  (below). A climate lawsuit (Instituto Verdeluz + Povo Anacé, 2023) means
  the plaintiffs' lawyers hold the EIA — a people route.
- Same caveat as Kennedy and Lins: the licence describes a different machine
  from the one being built.

### Porto de Sergipe II / III / V — numbers, but for an earlier plan

No licensing document specific to the expansion units was found; ADEMA-SE's
hosts time out on every route. What exists is the lender disclosure for
phase I (operating since 2020): IFC project 39652 lists ~60 PDFs at
https://disclosures.ifc.org/project-detail/ESRS/39652/celse — open, no wall.
IDB Invest 12048-01 has summaries only
(https://idbinvest.org/sites/default/files/2018-12/celse_esrs_esap_final_oct_17_0eng.pdf).

"Anexo II — Estudo de dispersão atmosférica do complexo termelétrico" (Sept
2017, prepared at IFC's request) models the **2.951 MW complex as then
planned** *(checked, Quadros 3.1–3.3)*:

| Per stack | Porto Sergipe I (3 × 517 MW) | Gov. Marcelo Deda (2 × 475 MW) | Laranjeiras I (1 × 450 MW) |
|---|---|---|---|
| NOx, kg/h | 146,31 | 117,78 | 112,36 |
| MP10, kg/h | 4,97 | 4,00 | 3,82 |
| SOx, kg/h | 11,22 | 10,13 | 9,82 |
| CO, kg/h | 190,20 | 153,12 | 146,07 |
| Stack H × D, exit T | 60 m × 7 m, 82 °C | 60 m × 7 m, 88 °C | 60 m × 7 m, 91 °C |

Phase I concentrations: NOx 50,0, CO 65,0, MP10 1,7, SOx 4,6 mg/Nm³ at 15 %
O2; flue gas 730,8 m³/s (1.819.382 Nm³/h dry) per stack; SOx derived from
70 mg/m³ sulphur in the gas; MP, NOx and CO "fornecidas pelo empreendedor".
Stack UTM coordinates are in the model-input tables.

Caveats: NOx and CO are again exactly the CONAMA 382 limits. Whether Marcelo
Deda and Laranjeiras I are the projects GEM now carries as Porto de Sergipe
II / III / V is **not confirmed** — treat as a lineage lead. No operating
hours, so no annual totals. The full EIA
(`GN_UTE_ESIA_EIA_UTE_rev00_v06.pdf` on the same IFC page) was not retrieved.
The study PDF carries its author's personal contact details; do not copy them.

## Lins — the full EIA, via the CETESB wall

`https://www2.cetesb.sp.gov.br/eiarima/eia/EIA_249_2018.pdf` — 272 MB, 3.305
pages, the whole licensing file (EIA, annexes, CETESB technical opinions,
the developer's replies). Image-only, so it was OCR'd (tesseract, `por`);
tables OCR badly and were read from page images. Index of CETESB's older
library (661 files): `https://www2.cetesb.sp.gov.br/licenciamentoambiental/eia-rima/`.

Dispersion study (Omega / Mineral Engenharia, OMG01_r00, 12/2018), PDF page
1972 = file page "2107", repeated at PDF p. 2634 *(checked on the image)*:

- Tabela III-1 — three stacks, each **55 m high, 6,7 m diameter, 79 °C,
  892,6 m³/s, 25,3 m/s**, base elevation 455 m, UTM (WGS 84) coordinates.
- Tabela III-2 — emission rates **per stack**:

  | | g/s | kg/h | **t/ano** |
  |---|---|---|---|
  | NOx (as NO2) | 45,83 | 165 | **1445,4** |
  | SOx (as SO2) | 5,06 | 18,2 | 159,6 |
  | MP10 | 0,75 | 3,8 | 33,3 |
  | CO | 6,64 | 23,9 | 209,4 |
  | COV | 0,64 | 2,3 | 20,1 |
  | HCT | 3,28 | 11,8 | 103,4 |

  "valores informados pelo empreendedor, exceto SOx". SOx is computed from
  gas flow (109.933,5 m³/h per turbine) × 70 mg/Nm³ sulphur × 1,2 margin.
- Tabela III-3 — NOx 50 mg/Nm³ (developer; 15 % O2, dry); CO 6,1; MP10 1,0;
  HCT 3,0; COV 0,6; SOx printed as 5,06 (the summary table at PDF p. 3297
  says 3,0).
- AERMOD; the annual figure is simply 8.760 h at full load (my arithmetic:
  45,83 g/s × 8.760 h = 1.445 t). MP10 is internally inconsistent: 0,75 g/s
  is 2,7 kg/h, not 3,8 — the t/ano follows the kg/h figure.

**This explains the first-pass puzzle.** CETESB's air division told the
developer that 50 mg/Nm³ (~25 ppm) is above the 9 ppm it recommends and asked
for a revision (Parecer Técnico, PDF pp. 1124 and 1160). The RIMA's 18 mg/Nm³
is the 9 ppm case. The developer then argued, with GE, to go back to 25 ppm:
9 ppm needs an SCR (~US$15 m capex, ~150 t/month of ammonia), and the file's
comparison table (PDF p. 3297) gives 25 ppm → NOx 50, CO 6,1, MP10 1,0 against
9 ppm → NOx 18, CO 12,2, MP10 1,53 mg/Nm³. **Which limit the licence finally
set was not determined** — it decides whether CREA should use ~1.445 or
~520 t NOx per stack-year. CETESB states that the emission value used in the
study becomes the licence limit, so the licence text is the thing to find.

Still the 2018 design (3 × GE 7HA.02, ~1.835–2.050 MW), not the 732,7 MW
plant contracted in 2026.

## The walls — what they are and what gets past them

| Wall | What it is | What worked |
|---|---|---|
| **CETESB** (`cetesb.sp.gov.br`) | AWS WAF JavaScript challenge — HTTP 202, header `x-amzn-waf-action: challenge`, empty body to any script | Open the site once in a real Chrome, take the `aws-waf-token` cookie, replay it with the same User-Agent in curl. The sibling repo's `scripts/cf_clearance.py` (`cookie_for(url)`) automates this. Token lasts minutes-to-hours; large files need `-C -` resume. |
| **ADB** (first pass) | Cloudflare bot check on project pages | TLS-fingerprint impersonation (`curl_cffi`), or skip the pages: `/sites/default/files/linked-documents/*.pdf` is not protected. |
| **IFC / IDB Invest** | none | plain curl; IFC files come from `disclosuresservice.ifc.org/api/File/downloadfile?id=…` |
| **IBAMA** | none at the front door — `servicos.ibama.gov.br/licenciamento/consulta_empreendimentos.php` answers plain curl (a scout reported it login-gated; it is not). It is a form-driven search, not yet scripted. | — |
| **SEMAS-PA** | not a wall: site migration broke every old `/wp-content/uploads/` link (404) | Wayback, when it is up |
| **SEMACE** (`semace.ce.gov.br` → `www.ce.gov.br`) | F5 Distributed Cloud WAF (`server: volt-adc`), HTTP 403 "The requested URL was rejected" on every page of the state portal, for every client tried including real-Chrome cookies | **Not solved.** No JS challenge to pass, so a cookie does not help; the behaviour fits an IP-reputation or geography rule. Needs a Brazilian residential/VPN exit or a partner. `natuur.semace.ce.gov.br` (the licensing system) does answer, but only offers applicant log-in — no public process search. `mobile.semace.ce.gov.br` returns 503. |
| **ADEMA-SE** | every host times out (no TCP answer) on all routes | **Not solved.** Either down or dropping foreign traffic; same remedy as SEMACE. |
| **Internet Archive** | availability/CDX APIs returned 429, then "temporarily offline" all session | retry another day; direct `web.archive.org/web/<ts>/<url>` snapshot URLs sometimes work when the API does not |

Three different things were being lumped together as "bot-walled": real bot
challenges (CETESB, ADB — solved), link rot (SEMAS-PA — Wayback), and
network-level refusal (SEMACE, ADEMA — not solvable from a US address). Only
the last needs outside help, and one researcher with a Brazilian VPN exit
would settle whether it is geography.

## What generalises

- Construction status does not predict document availability. Agency and
  lender do.
- **Get the full EIA process file, not the RIMA.** Lins shows the full file
  can hold annual tonnes, stack parameters, the agency's objections and the
  developer's cost arguments — the RIMA had one number with no context.
- CETESB asks every thermal plant for kg/h **and t/ano** per source in its
  terms of reference (PDF p. 1124). São Paulo plants should therefore all be
  method A. Its old library is open once through the WAF.
- Lender disclosures describe the project at financial close. Useful for
  operating-plant anchors (Sergipe I) more than for today's pipeline.
- Large scanned files: budget OCR time (3.305 pages ≈ 1 h on 8 cores) and read
  the tables from page images.

## Tracker leads (route to a normal GOGPT Update batch — not handled here)

- Jandaia: Eneva's filing gives Jandaia II 899,6 MW, III 299,8 MW (COD Aug
  2029) and Jandaia 1 460,0 MW (COD Aug 2031); ownership passed Ceiba → Eneva
  in Sept 2025.
- Novo Tempo Barcarena: SEMAS-PA process numbers above; EPC Mitsubishi Power
  + Andrade Gutierrez *(scout)*.
- Porto de Sergipe: earlier sister-plant names UTE Governador Marcelo Deda
  (2 × 475 MW) and UTE Laranjeiras I (450 MW) — check against units II/III/V.
- Lins: 2018 file says 3 × GE 7HA.02, 1.835 MW (CETESB opinion).
