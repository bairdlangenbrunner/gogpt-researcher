# Brazil scout — 2026-09-17

First pass on the three sampled plants, ~1 agent-session each plus spot checks.
Shallow by design: the aim was "does a document with numbers exist, and what
kind of numbers", not a full capture. Per-plant files (from `_template.md`) are
still to be written for the plants worth a full pass.

**Verification labels.** *Checked* = I opened the downloaded PDF text and found
the value at the cited place. *Scout* = reported by the search agent, not
independently re-read. Values are quoted in the document's own notation
(Brazilian decimal comma unless noted).

> **Corrected later the same day** — see `brazil_construction_scout_20260917.md`.
> CETESB's wall was passed and the full Lins EIA retrieved; Lins is now
> **A + B + C + stack**. Lines below that this overturns are marked
> *corrected*.

## Summary

| Plant | Licensing body | Document found | Evidence type | Verdict |
|---|---|---|---|---|
| Presidente Kennedy | IEMA-ES (state) | Full 2013 EIA, chapter by chapter, plus RIMA | **B and C**, with full stack parameters and stack coordinates | Best example to show CREA — with the caveat below |
| Lins | CETESB-SP (state), process 249/2018 | RIMA + licensing-form annexes; *corrected:* full EIA file since found | *corrected:* **A + B + C + stack** (first pass: C without flow, A for NOx only) | Best Brazilian example; older, larger design; 25 vs 9 ppm NOx limit unresolved |
| Termo João Pessoa | SUDEMA-PB (state) | Only the environment-council decision homologating the LPs | Nothing | Dead end online; records request or partner needed |

Hit rate: 2 of 3 with numbers, 2 of 3 with the full set CREA wants
(*corrected* from 1 of 3).

## Presidente Kennedy (L100000406528)

- **Documents.** IEMA-ES publishes EIAs by year; the 2013 list is at
  https://iema.es.gov.br/GrupodeArquivos/EIA-2013-2 and the chapter PDFs sit
  under `iema.es.gov.br/media/CQAI/EIA/2013/Usina termelétrica à gás -
  Presidente KennedyES/`. RIMA:
  https://iema.es.gov.br/Media/iema/Downloads/RIMAS/RIMAS_2013/2017.04.06%20-%20RIMA_GERA.pdf.
  State-wide EIA register (useful for every other Espírito Santo plant):
  https://iema.es.gov.br/Media/iema/EIA-RIMA/EIA/Relacao_EIA_IEMA_site_24.02.2026.pdf.
  Retrieved 2026-09-17: chapters 1, 2 and 7, RIMA, register.
- **Project as described** *(checked)*: proponent GERAES – Geradora de Energia
  do Espírito Santo S.A.; consultant Econservation; 2 combined-cycle sets of
  440 MW gross, 880 MW total, in two phases; gas turbine **MHI M501J**; gas
  consumption 78.000 m³/h per phase (1 atm, 20 °C).
- **Emissions, EIA ch. 7 §7.2.5** *(checked)*:

  | Table | Scope | MP | MP10 | SO2 | NOx | CO | COV |
  |---|---|---|---|---|---|---|---|
  | 7.2.5-2, full load, kg/h | plant | 15,1 | 15,1 | 7,3 | 176,0 | 228,8 | 4,8 |
  | 7.2.5-3, kg/h | per stack (2 stacks) | 7,5 | 7,5 | 3,6 | 88,0 | 114,4 | 2,4 |

  Table 7.2.5-6: NOx 50 and CO 65 mg/Nm³, "base seca e 15% de excesso de
  oxigênio"; actual flue-gas O2 13,3 %.
- **Stack** *(checked)*: 2 stacks; D 6,5 m; Q 625,9 Nm³/s; T 85 °C; H 45 m
  *(H from scout)*; coordinates -21,203480 / -41,013576 and -21,203013 /
  -41,012823.
- **The caveat that matters.** The EIA says outright that the NOx and CO
  concentrations — and therefore the kg/h rates — "representam o limite
  estabelecido pela legislação" (CONAMA 382/2006): the modellers took the legal
  limit × design flow as a worst case. So the NOx figure is a **permitted-limit
  number dressed as a predicted rate**, not an OEM guarantee. MP, SO2 and COV
  are not regulated for gas turbines, so those rates are design/factor-based.
  An M501J with dry low-NOx combustors would normally run well under 50 mg/Nm³.
- No annual tonnes and no operating-hours assumption found (grep of ch. 7 for
  horas / fator de capacidade / 8.760 turned up nothing relevant) → A is not
  available; B needs CREA's own hours.
- **Second caveat.** This is the 2013 GERA project. GEM now lists Eneva as
  owner, 2 × 441,6 MW, an LRCAP 2026 winner. Whether Eneva is building to this
  licence and this turbine has not been checked.

## Lins (L100000406518)

- **Documents.** CETESB process 249/2018. The live site is behind an AWS WAF
  challenge; Wayback has both files:
  https://web.archive.org/web/20240125114526/https://cetesb.sp.gov.br/eiarima/rima/RIMA_249_2018.pdf
  and
  https://web.archive.org/web/20240125114526/https://cetesb.sp.gov.br/eiarima/anexos/ANEXOS_249_2018.pdf.
  *Corrected:* the full EIA is at
  `https://www2.cetesb.sp.gov.br/eiarima/eia/EIA_249_2018.pdf` (272 MB, 3.305
  pages), reachable with a browser-earned WAF cookie — method and contents in
  the construction-pass file.
- **Project as described** *(scout)*: the original ~2.050 MW proposal, 3 × GE
  7HA.02 + 1 steam turbine. GEM's current record is 732,7 MW (New Fortress
  Energy, LRCAP 2026). The scout reports MME authorised the 732,7 MW
  configuration by Portaria SNTEP/MME 3.188 of 2026-09-15 — not verified.
- **Emissions** *(checked)*:

  | Source | NOx | MP | SOx | CO | Other | Basis |
  |---|---|---|---|---|---|---|
  | RIMA project-data table (p. 15) | 18 mg/Nm³ ("da turbina") | 1,93 | 5,29 | 13,4 | HCT 7,06 | not stated there |
  | RIMA air-quality table (p. 53) | 18 (as NO2), "informado pelo empreendedor" | MP10 1,53 | 3,0 (as SO2) | 12,2 | COV 1,29 | 15 % O2, dry; all but NOx "calculados a partir das taxas de emissão" |
  | ANEXOS licensing form | **Emissão de NOx 3,582 ton/ano** | 1.9 mg/Nm3 | – | – | – | form uses English number format (10,000 kWh/mês = RIMA's 10.000), so this is 3 582 t/yr |

  The two RIMA tables disagree on MP, SOx and CO; record both. The p. 53
  footnote proves a table of emission **rates** exists in the full EIA.
  *Corrected:* found — per stack NOx 45,83 g/s = 165 kg/h = 1445,4 t/ano at
  50 mg/Nm³; the RIMA's 18 mg/Nm³ is the 9 ppm case CETESB asked for.
- Fuel use 2883×10⁶ Nm³/ano *(checked)*. My own rough cross-check, not from the
  document: that much gas at 18 mg/Nm³ (15 % O2, dry) gives on the order of
  1 500–1 700 t NOx/yr, so the form's 3 582 t/yr rests on some other basis
  (higher concentration, start-ups, or a different hours assumption). Flag to
  CREA rather than resolve.
- No stack parameters in the RIMA or the annexes (*corrected:* they are in the
  full EIA's dispersion study — 3 stacks, 55 m × 6,7 m).
- 18 mg/Nm³ is a developer-declared OEM-type value (≈9 ppm class), a useful
  contrast with Kennedy's "assume the legal limit".

## Termo João Pessoa (L100001083458)

- **Found** *(checked that the names and LP numbers appear; the rest scout)*:
  SUDEMA-PB's council, COPAM, Deliberação 5.821 (16 Dec 2025), homologating
  preliminary licences incl. LP 3320/2025 for UTE Termoparaíba II and siblings
  Termonordeste II / III and Termoparaíba III, all Centrais Elétricas da
  Paraíba S.A. (EPASA):
  https://sudema.pb.gov.br/institucional/copam-1/deliberacoes/2025/deliberacao-5821-homologacao.pdf.
  LRCAP result list: https://ppi.gov.br/wp-content/uploads/2026/03/Resultado-geral-1.pdf.
- It looks like a gas conversion / expansion at EPASA's existing oil-engine
  site, licensed under different plant names from the one GEM carries. No EIA,
  RIMA, or simplified study found on SUDEMA's site; no emissions numbers.
- Who might hold it: SUDEMA (access-to-information request, LAI), EPASA/CPFL,
  Arayara.

## What generalises

- **Availability is decided by the state agency, not by the project.** IEMA-ES
  posts whole EIAs; CETESB posts RIMA + annexes and full EIAs behind an AWS
  WAF challenge (*corrected:* passable with a browser-earned cookie); SUDEMA
  posts decisions only. Learn the ~6 states that hold most
  of the pipeline (RJ first: 10 of 62 plants) rather than plant by plant.
- **The RIMA is not enough.** It is the public summary; emission rates and
  stack parameters live in the full EIA's air-quality / prognosis chapter and
  its dispersion-modelling annex.
- **Expect B and C, rarely A.** Brazilian EIAs model worst-case full load; they
  seldom annualise. (*Corrected:* CETESB requires t/ano per source, so São
  Paulo is the exception.)
- **"Predicted" may really be "permitted".** Check whether the modelled NOx
  equals 50 mg/Nm³; if so it is the CONAMA 382 limit.
- **Re-emerged projects.** Two of three sampled plants are licensed on a
  document written for a different developer, size or turbine (Kennedy 2013,
  Lins 2018). The LRCAP rule "licence ⇒ EIA exists" holds, but the EIA may
  describe a different machine. Conversions (João Pessoa) may have been
  licensed on a simplified study with no dispersion modelling at all.
- **Effort.** Finding the document: 30–90 min when the agency publishes;
  open-ended when it doesn't. Full capture of one EIA: 2–3 h. Call it 3–6 h per
  plant for a proper pass, so 25 % of Brazil (~16 plants) is roughly 2–3 weeks
  of one researcher, before records requests.

## Tracker leads (route to a normal GOGPT Update batch — not handled here)

- Presidente Kennedy has two 441,6 MW units named "1" and "I" — check for a
  duplicate or a naming slip.
- Presidente Kennedy: turbine technology per the 2013 EIA is MHI M501J,
  single-shaft CCGT — only a lead until Eneva's current design is confirmed.
- Termo João Pessoa: licensed as UTE Termoparaíba II / III and Termonordeste
  II / III (EPASA); GEM's plant name and 55,9 MW may map to only one of them.
- Lins: confirm 732,7 MW against the Sept 2026 MME ordinance.
