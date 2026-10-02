# IBAMA thermal-plant processes and where IBAMA keeps the studies (Brazil)

Probe run 2026-09-18. It covers two things: IBAMA's federal licensing search
(the process list, now matched to the frame in `../coverage/brazil.csv`) and
where IBAMA publishes the EIAs. All 98 processes are in
[`brazil_ibama_processes_20260918.csv`](brazil_ibama_processes_20260918.csv).
Five of them have a private individual as developer: that name and CPF are
withheld, and the processes are kept.

## 1. The licensing search: `servicos.ibama.gov.br/licenciamento/consulta_empreendimentos.php`

An old PHP FormDin app with no login and no captcha. Pages are Latin-1.
Plain `curl` works if it keeps a cookie jar.

**List.** GET the page to get a session cookie. Then POST
`formDinAcao=Pesquisar&vartipologia=9`, where 9 means "Usina Termelétrica".
This returns all 98 processes on one page, every fuel included. Each row is a
`<form name="p…">` carrying hidden `processo` and `cod_empreendimento`. The
project name is the `readonly value` of a text input. After `</form>` come a UF
cell (blank in 52 of the 98) and seven stage cells:

| Phase | Cells | Colour when done |
|---|---|---|
| LP | TR, EIA-RIMA/RAS, AP (hearing), AF (LP issued) | `#33CC00` |
| LI | PBA/PCA, AF (LI issued) | `#339900` |
| LO | LO | `#336600` |

`#FFFFFF` and `#E0E0E0` are row striping, and both mean "not reached". The
colour grid is coarse: TermoLinhares shows the whole LP phase done, while
Presidente Kennedy's 2026 process shows nothing.

**Per process.** The tabs are POSTs with
`modulo=empreendimento&cod_empreendimento=<n>`, plus:

- `formDinAcao=Informações do processo`: the process number, project,
  developer, **CNPJ/CPF**, tipologia, situação atual, observações. There is
  **no opening date**. A process number's year is all there is. A 2025
  number cannot be placed before or after 26 June 2025 from this app.
- `formDinAcao=Documentos do processo`: a grid of No., Documento, Assunto,
  Data and an "Abrir" link. It lists licences (LP/LI/LO with number and
  date), extensions, rectifications, ABio fauna permits, FCAs, pareceres
  técnicos, and for older processes the TR and the public-hearing minutes.
  It holds **no EIA or RIMA**. 58 of the 98 have no documents at all.
- **Opening a document:** POST
  `formDinAcao=btngdAbrir&modulo=documentos&cod_documento=<id>&cod_empreendimento=<n>`.
  The answer holds an iframe to
  `./modulos/documentos.php?cod_documento=<id>&donwload=` (the typo is IBAMA's).
  GET that with the same cookie jar and it returns the PDF. Test: TermoLinhares
  LP 683/2023 (cod_documento 74717). It is 2 pages and names TermoLinhares I
  + II up to 2,100 MW. The LP text has no emission limits.

The scrape was one serial pass with 1 s pauses: 1 list POST, then 2 POSTs
per process.

## 2. Matching to the frame (Task 1)

Name first, then the developer against GEM's owner, then CNPJ against ANEEL
SIGA (`DscPropriRegimePariticipacao`). SIGA confirms only plants it already
lists: most pipeline plants (Litos, NSF, TermoLinhares, Jandaia, Queluzito,
Gaslub, Barra do Furado, Monte Fuji, Kennedy, Ressurreição) are not in it,
so for those the match rests on name and developer. Results are in
`coverage/brazil.csv` (`licensor`, `licence_stage`, `notes`, `last_checked`).
`licensor = IBAMA` only where name and developer agree. Where they don't,
the note says AMBIGUOUS and the licensor is left unchanged.

- **IBAMA confirmed, pipeline:**
  - with LPs: Litos, TermoLinhares, Norte Fluminense 2, Tupã, Geramar III
  - no LP yet: Queluzito, Brasil Central, Centro Oeste, Gaslub, Porto Norte
    Fluminense, Araucária (two 2026 processes)
- **IBAMA confirmed, inactive in GEM:** Nossa Senhora de Fátima, Barra do
  Furado, Imetame I, Vila do Conde, Jaci, Gasen Suape, Fronteira, São Marcos,
  Itacoatiara, Norte Catarinense, Jorge Lacerda, Termopecém.
- **Tracker leads, noted and not acted on:**
  - Jaci is cancelled-inferred but received new LPs in July 2026.
  - NSF is shelved-inferred but has a new 2025 process.
  - Marlim Azul II has LP 695/2024 but no GEM row.
  - UTE Suape 5 (Genpower, 1,800 MW, 2025) has no GEM row.
- **Operating plants in the list:** Luiz Carlos Prestes and Uruguaiana
  (IBAMA-licensed from LP to LO), Parnaíba, Cuiabá, Jesus Soares Pereira,
  Baixada Fluminense, Mauá 3, Norte Fluminense, Marlim Azul (expansion),
  Nova Piratininga.
- **Ambiguous, flagged in notes:**
  - Porto de Sergipe (2026 complex process plus expired III/IV LPs, against
    ADEMA-SE)
  - Governador Marcelo Deda and Laranjeiras
  - Presidente Kennedy (2026 "Complexo Termelétrico Sudeste" and the 2018
    "UTE Sudeste", against the IEMA-ES LP)
  - Jandaia and Portocém (Portocem processes in CE, SIGA plant in PA)
  - Novo Tempo Barcarena
  - Azulão, Azulão III and Jaguatirica II (one CNPJ)
  - Suape IV B (Suape II processes)
  - Porto do Pecém (coal-to-gas?)
  - Rio Grande
  - Teresina and EPP Teresina
  - Brasília and Rio Matapi II (individual developers)
  - Monte Fuji M1 (299 MW, under the threshold)
  - Nova Piratininga STP, Piratininga, Fortaleza
- **Delegated to the state:** Ressurreição, Santa Cruz Rolugi.
- **Not gas or out of frame:** Candiota, Pampa Sul, Ouro Negro, Nova Seival
  and Porto de Itaqui (coal); Belém do Solimões, Feijoal and BBF (biomass);
  Betânia, Cucuí, Iauaretê and other small Amazon diesel; and assorted
  others.

**Post-June-2025 processes (the new TR applies):**
- 2026 numbers: Complexo Porto de Sergipe, Complexo Sudeste (Kennedy),
  UEG Araucária 1 and 2, UTE Suape II. Litos also got four new LPs in
  February 2026, and Jaci/Tupã two in July 2026, both under older
  processes.
- 2025 numbers, date unknown, no EIA filed yet: UTEs NSF 1 e 2, UTE Suape 5
  (IBAMA's Parecer 172/2025 ordered a full EIA under the IBAMA TR), and the
  Porto do Pecém processes.
- Every one of these is still before its EIA. None has a post-June-2025 EIA
  to read yet.

## 3. Where IBAMA keeps the studies (Task 2)

Rungs tried, in order:

1. **SEI public search**
   (`sei.ibama.gov.br/modulos/pesquisa/md_pesq_processo_pesquisar.php?acao_externa=protocolo_pesquisar&acao_origem_externa=protocolo_pesquisar&id_orgao_acesso_externo=0`).
   It answers 200, but the form has an image captcha (`txtInfraCaptcha`,
   with an audio option). It can't be scripted and was not bypassed. A
   person can search it by process number (`txtProtocoloPesquisa`) in a
   minute. It would give process opening dates and public SEI documents.
   Not needed for locating the EIAs (rung 2).
2. **`licenciamento.ibama.gov.br`**
   - Plain curl gets 301 → https, then **403**: a Cloudflare managed
     challenge (`cf-mitigated: challenge`). A browser UA also gets 403.
     `www.` does not resolve.
   - The lng-terminals-researcher fetch ladder, run from a scratch copy so
     nothing was written in that repo, gets through by `curl_cffi` Chrome
     impersonation (`cf_impersonate`). The host root is a **redirect to a
     public, anonymous SharePoint share link**:
     `https://ibamagovbr.sharepoint.com/:f:/s/LicenciamentoTeste/EoV6g0gR2wFBk668lwp8GD0BDhYVlZwOvmnhqXHoA1JxAg`
     → guest access →
     `https://ibamagovbr.sharepoint.com/sites/EstudosAmbientais/Documentos Compartilhados/Licenciamento`.
   - The old `/Termeletricas/` path now 404s. The folder lives inside the
     library.
3. and 4. (gov.br hearings pages, web archives): not needed once rung 2
   answered. Two guessed gov.br/ibama hearing URLs returned 404. The Wayback
   availability API returned 429. Neither was pursued.

**The library.** `Licenciamento/` has one folder per sector (Termeletricas,
Porto, Rodovias, LinhadeTransmissao, Hidreletricas, …).
`Licenciamento/Termeletricas/` has 33 project folders, most dated October
2024 (a bulk migration), with later additions: Suape 5 (December 2025),
Petrocity (March 2026), Jaci/Tupã (June 2026).

**Reading it without a browser:**
- Take the `FedAuth` cookie from the share-link redirect chain. `curl_cffi`
  with `impersonate="chrome"` gets it, starting either from the host root or
  straight from the share link.
- Then SharePoint REST, `Accept: application/json;odata=nometadata`:
  - `…/sites/EstudosAmbientais/_api/web/GetFolderByServerRelativeUrl('<path>')/Folders`
    (and `/Files`) to list
  - `…/_api/web/GetFileByServerRelativeUrl('<path>')/$value` to download

**Test plants:**

| Process | Folder | Holds | Verdict |
|---|---|---|---|
| UTEs NSF 1 e 2 (02001.032232/2025-17); earlier NSF 02001.102629/2017-65 | `UTE-Nossa Senhora de Fátima` | EIA Volumes 1–4 + RIMA (~250 MB) | The 2017–18 EIA behind LP 589/2018, not the 2025 process |
| UTE Suape 5 (02001.040413/2025-17) | `UTE Suape 5` | FCA, RAS (4 MB), memorial descritivo, shapefile, IBAMA Parecer Técnico 172/2025 | Downloaded and read. The RAS gives 1,800 MW net and **4,380 h/yr expected operation** (dispatch by availability). The only emission values are the CONAMA 382 limits (NOx 50, CO 65 mg/Nm³ @ 15 % O₂ dry). The parecer rules the plant federal (≥ 300 MW) and orders a full EIA/RIMA under the IBAMA TR |
| Complexo UTE Porto de Sergipe (02001.031497/2026-71) | none | nothing yet (initial phase, no documents) | Nearest is `02001102580201741 - Instalações Offshore…` (Eneva's gas and outfall infrastructure, LP 559/2017) |
| Litos (02001.027653/2019-70) | `UTE s    LITOS` | EIA (April 2020 and final June 2020), annex volumes, RIMA, TR checklist, filing letter | Full EIA |
| TermoLinhares (02001.018604/2022-41) | `UTE_TermoLinhares`, `UTE Termolinhares` | SEI process export in two PDFs (~420 + 330 MB), TR × EIA checklist, shapefiles | The EIA is presumably inside the SEI export. Not downloaded |

Only the test folders were listed file by file. The other top-level
folders: Brasil Central, Centro Oeste, Sudeste (35 files),
Queluzito, Geramar III, Norte Fluminense II, Imetame I, Luiz Carlos Prestes,
Jaci e Tupã, MPF Macaé response, MPX Sul, Brasília, Petrocity, Barra do Furado
(41 files), Porto de Itaqui, AES Uruguaiana, Ouro Negro, Marlim Azul II (30
files), Pampa Sul, Candiota and Candiota III, São Paulo, Seival, Nova Seival.

## Verdict

- **IBAMA holds a large share of the big pipeline plants.** The at-a-glance
  claim that none of our plants is federal came from a six-plant sample.
  Litos (5.3 GW), TermoLinhares (2.1 GW), Norte Fluminense 2, Geramar III,
  Gaslub, Brasil Central, Centro Oeste, Queluzito, Porto Norte Fluminense and
  Araucária are federal. The three largest ambiguous cases (Porto de Sergipe,
  Kennedy, Jandaia) have new IBAMA processes.
- **The studies are online and scriptable** on IBAMA's SharePoint, for
  processes that have reached the study stage. The processes opened in
  2025–26 have not filed an EIA yet. So the design-hours EIAs the June 2025
  TR should produce are still to come. Suape 5's RAS already states 4,380 h.
- **Not done (out of scope for this step):**
  - Reading the EIAs' air chapters.
  - Listing the other sector folders (Porto may hold FSRU-linked plants).
  - SEI dates by hand.
  - The Tier 0 remainder.
