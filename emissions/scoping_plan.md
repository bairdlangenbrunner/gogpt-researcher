# Scoping plan — Vietnam and Brazil (drafted 2026-09-17)

Working plan; edit freely. Context and boundaries in `README.md`; what to
capture in `methods_and_fields.md`.

## The question this pass answers

Julie's open question 4 in the regional-prioritization doc — *"are the data
points we need likely to be found in EIAs or air permits in the countries we
choose to target?"* — for the two countries CREA is most worried about. The
output is not a dataset. It is, per country: which document types exist, where
they live, which evidence type (A–D) they support, minutes per plant, and one
or two real example sources to show Jamie and Daniel so they can say which
calculation method fits. They said explicitly they expect one or two methods to
be possible per country, not all.

Things the docs say that the meeting notes don't, or say differently:

- CREA's data-density ask is **25% of plants per country**. On the fresh pull
  that is ~5 of Vietnam's 20 announced/pre-construction plants and ~16 of
  Brazil's 62. The scoping sample (3 + 3) is a feasibility probe, not that.
- The ranking sheet has **Brazil = "Top priority"** and **Vietnam = "have to
  cover for completeness; scope out potential for impact"**. GEM's own
  suggestion in the prioritization doc was to *avoid* Vietnam (with the US and
  China) and offer Ireland, Australia, South Korea, Canada, Germany, UK, maybe
  Japan. So Vietnam is the "hard one" by everyone's account; a fast, honest
  "EIAs are not retrievable, here is the fallback" is a legitimate result.
- The concept note's tiering already gives the fallback: project-specific
  limits and controls where permits/EIAs exist → national emission standards →
  default (CEDS) factors. A licence that states only a NOx limit is a usable
  find, and so is the national standard itself.
- CREA's wish list is wider than the three pollutants: coordinates, turbine
  technology, controls, permit NOx limit, generation, utilisation, start-up
  cycles, lifetime, and stack height / diameter / flue temperature / velocity.
  The stack parameters come from the same table of the same document as the
  emission rates (the dispersion-modelling inputs), so capture them together.
- The Brazilian partner is **Instituto Arayara** (the notes' "Ariaro").
- The methods doc has six evidence types (A–F), not four; E (local intensity
  from a comparable plant) and F (interval data) matter for operating plants.

## Where it stands after two passes (2026-09-17)

First pass: 3 + 3 announced / pre-construction plants. Second pass: 3 + 3
**construction-stage** plants, plus work on the sites that had blocked scripted
access.

| | Brazil | Vietnam |
|---|---|---|
| First sample (announced / pre-construction) with numbers | 2 of 3 | 1 of 3 (Hai Lang, once the portal was reached) |
| Construction sample with numbers | 1 of 3, and that one is a 2017 lender study of an earlier plan (Porto de Sergipe) | 1 of 3 (Thái Bình) |
| Extra plants found along the way | — | 4 more ĐTMs (Hải Phòng, Quảng Trạch II and III, Cà Ná) + 2 operating plants with **measured** stack tests (Nhơn Trạch 2, Ô Môn I) |
| Best evidence found | **A + B + C + stack** (Lins full EIA); B + C + stack (Kennedy; Sergipe complex) | B + C + stack + operating hours, NOx and CO only (six ĐTMs) |
| Annual mass (A) | Lins: t/ano per stack for NOx, SOx, MP10, CO, COV | none stated; hours given, so one multiplication away |
| What decides availability | which **state agency** licenses the plant, then whether a DFI lent | whether the ĐTM went to consultation **since 2022** (then it is on the ministry portal) |
| Fallback limit confirmed | CONAMA 382/2006: NOx 50 mg/Nm³, 15 % O2, dry | QCVN 19:2024: NOx 50–150, SO2 50–90, PM 15–20 mg/Nm³ at 15 % O2, by capacity and zone |
| Recommended approach | document-hunt state by state, full EIA file not RIMA; 25 % looks reachable | portal first; 25 % looks reachable for NOx / CO; PM and SO2 need CREA's own factors |

Findings that cut across both countries and belong in front of Jamie and
Daniel:

- **EIA "predicted" NOx is usually the legal limit or the OEM guarantee ×
  design flow**, not a plant-specific prediction: 50 mg/Nm³ in Brazil (Kennedy,
  Sergipe, Lins), 47,02 / 51 mg/Nm³ (= 25 ppmv) in most Vietnamese ĐTMs, 68,02
  at Cà Ná (just under the new limit of 70). Record the provenance with the
  number.
- **The regulator may force a lower number.** At Lins, CETESB asked for 9 ppm
  (18 mg/Nm³, needs SCR) instead of 25 ppm; the developer contested it; which
  was licensed is not yet known. It is a factor of 2,8 on NOx.
- **Gas-plant PM and SO2 are asserted, not estimated.** Most ĐTMs say "zero".
  Measured total dust at Nhơn Trạch 2 runs 19–31 mg/Nm³.
- **The document may describe a different machine.** Kennedy (2013 project),
  Lins (2018, 3 × 7HA.02), Jandaia (licence inherited from a 4-turbine
  open-cycle design), O Môn IV (2007 inputs); Vietnamese consultation drafts
  also change before approval.
- **Construction status did not make documents easier to find.**

Walls (detail and methods in `findings/brazil_construction_scout_20260917.md`
and `findings/vietnam_construction_scout_20260917.md`): CETESB (AWS WAF),
ADB (Cloudflare) and the Vietnamese portal (flaky TLS) are **solved**; SEMAS-PA
is link rot, not a wall; **SEMACE-CE and ADEMA-SE refuse or drop our traffic at
network level** and need a Brazilian IP or a partner; the Internet Archive was
down all session, so every Wayback route is untested.

Detail: the four `findings/*_scout_20260917.md` files. The two first-pass files
carry *corrected* marks where the second pass overturned them.

## The sample

Fresh pull 2026-09-17 (34,946 rows → 15,435 GOGPT-scoped). Plant-level simple
random draw among plants with ≥1 announced or pre-construction unit, seed
`20260917`, via `draw_sample.py`. First three per country are the sample; the
next two are alternates, used only if a sampled plant turns out to be
unresearchable for a reason unrelated to document availability.

Second pass: same script and seed with `--statuses construction` — Vietnam:
Thái Bình LNG, Hiệp Phước phase 1, Ô Môn IV; Brazil: Novo Tempo Barcarena,
Jandaia II / III, Porto de Sergipe II / III / V.

| Country | Draw | Plant | MW | Status | Owner | Why it is an informative draw |
|---|---|---|---|---|---|---|
| Vietnam | 1 | Son My II | 3 × 750 LNG CCGT | pre-construction | AES | US sponsor → possible DFC / US EXIM disclosure |
| Vietnam | 2 | Long Son | 2 × 750 LNG CCGT | announced | EVNGENCO3 | Domestic sponsor, early stage → tests the "no EIA yet" case |
| Vietnam | 3 | Hai Lang ph. 1 | 1,500 LNG CCGT | pre-construction | T&T, KOGAS, KOSPO, Hanwha | Korean sponsors → K-EXIM / K-SURE disclosure; SFOC (already a CREA partner) watches Korean overseas gas |
| Vietnam | alt | Ca Mau 3; Ke Ga | 1,500; 3,600 | announced | PVN; ECV/B.Grimm/Siemens | |
| Brazil | 1 | Presidente Kennedy | 2 × 441.6 LNG CCGT | pre-construction | Eneva | LRCAP 2026 winner; port-linked; state (IEMA-ES) or IBAMA licensing |
| Brazil | 2 | Lins | 732.7 CCGT, GE 7HA.02 | pre-construction | New Fortress Energy | LRCAP 2026 winner; CETESB RIMA 249/2018 already linked in GEM's notes |
| Brazil | 3 | Termo João Pessoa | 55.9, technology unknown | pre-construction | EPASA (CPFL) | LRCAP 2026 winner; small, probably engines at an existing oil-engine site → tests the non-CCGT case Dan raised |
| Brazil | alt | Araucária II; Laranjeiras | 369; 618 | pre-con; announced | Âmbar; Eneva | |

The draw happens to cover the useful contrasts (foreign- vs domestic-financed,
announced vs pre-construction, CCGT vs probable engines). Brazil's pipeline is
46 of 84 units "technology unknown" and 9 internal-combustion, so Dan's point
about engines is live there; Vietnam's is essentially all LNG CCGT.

## How to look — common ladder

Per plant, time-boxed to ~60–90 minutes, stopping at the first rung that yields
a document with numbers, and logging every rung tried:

1. **Name the project the way the regulator does.** Local-language name,
   earlier developer / SPV names, licensing process number. Most misses are
   naming misses.
2. **Regulator's licensing portal** — the EIA, its public summary, the
   dispersion-modelling annex, the licence and its conditions.
3. **Lender disclosure** — DFIs and export-credit agencies publish ESIAs for
   Category A projects (IFC, ADB, DFC, JBIC/JICA, K-EXIM, K-SURE, SACE, SERV,
   Euler Hermes). Often the only route where the regulator publishes nothing.
4. **Public-hearing / consultation trail** — hearing notices, official
   gazettes, environment-council minutes; they frequently link the summary.
5. **Company and contractor sources** — investor presentations, securities
   filings, EPC / OEM press (turbine model and controls, which set NOx).
6. **Wayback** for anything that was posted for a consultation window and
   removed.
7. **People** — local NGOs and partners who already hold the PDFs.

Inside the document, go straight to the air-quality impact chapter and the
dispersion-model input table: that one table usually holds emission rate per
stack (g/s), stack height, diameter, exit temperature, exit velocity or flow,
and the operating scenario. Grep terms are in the country sections.

If nothing plant-specific exists, record that, and record the fallback inputs
instead: technology, turbine model, controls, the applicable national limit.

## Brazil

**Why it should be tractable.** Thermal plants above 10 MW need an EIA/RIMA
(CONAMA 01/1986); licensing runs LP → LI → LO; EIAs and RIMAs are public
documents with public hearings. Registering for an energy auction requires a
valid environmental licence, so every **LRCAP 2026 winner should already hold
at least an LP — meaning an environmental study exists somewhere**. All three
sampled plants are LRCAP winners. The scout confirmed the rule but with two
catches: the study may be for an older design, and a conversion at an existing
site (Termo João Pessoa) may have been licensed without a published EIA. The
difficulty is fragmentation: licensing sits with IBAMA or with one of ~20 state
agencies, each with its own portal — all three sampled plants turned out to be
state-licensed, and the three agencies behaved completely differently
(IEMA-ES: whole EIA online; CETESB-SP: whole licensing file online behind an
AWS WAF challenge, passable with a browser-earned cookie; SUDEMA-PB: council
decisions only). The construction pass added SEMAS-PA (old links dead), and
SEMACE-CE and ADEMA-SE (unreachable from a US address).

Next steps, in order: (1) full capture of Lins and Presidente Kennedy into
per-plant findings files — Lins is now the example to show CREA; (2) find the
Lins licence text, to settle 25 vs 9 ppm NOx; (3) sweep CETESB's library for
the other São Paulo plants — CETESB requires t/ano per source, so they should
all be method A; (4) test SEMACE and ADEMA from a Brazilian IP (one
researcher with a VPN settles whether it is geography); (5) learn INEA-RJ's
portal, since Rio has the most plants; (6) check whether Eneva's and NFE's
current designs match the licensed ones; (7) ask Arayara / IEMA what they
already hold before spending more hours.

- In the document: the numbers are in the full EIA's prognosis / air-quality
  chapter ("Prognóstico", "Qualidade do ar", "Estudo de dispersão
  atmosférica"), in the emission-inventory and source-parameter tables. The
  RIMA is a public summary and at best gives concentrations.
- Portals: IBAMA (`licenciamento.ibama.gov.br`, `servicos.ibama.gov.br/licenciamento`);
  CETESB-SP (`cetesb.sp.gov.br/eiarima`, and the older library at
  `www2.cetesb.sp.gov.br/licenciamentoambiental/eia-rima/`); IEMA-ES; SUDEMA-PB; IAT-PR; ADEMA-SE;
  INEA-RJ (Rio has 10 of the 62 plants — the state most worth learning).
- Search terms: `EIA RIMA "UTE <nome>"`, `estudo de dispersão atmosférica`,
  `emissões atmosféricas`, `chaminé`, `g/s`, `mg/Nm³`, `licença prévia`.
- National limit (fallback tier): CONAMA Resolution 382/2006 Annex V — gas
  turbines for power generation on natural gas, **NOx 50 mg/Nm³ as NO2, dry
  basis, 15% O2**; 135 mg/Nm³ on liquid fuel. (Confirmed from the resolution
  text via search; applicability thresholds and the CONAMA 436/2011 rules for
  older sources still to be read.)
- **Operating plants, evidence type A:** IBAMA's open-data portal publishes
  annual NOx, SOx, PM and CO tonnes per thermal plant from the operators'
  RAPP reports. IEMA (Instituto de Energia e Meio Ambiente)'s *5º Inventário
  de Emissões Atmosféricas em Usinas Termelétricas* (Dec 2025, base year 2024)
  audited it: of 67 fossil plants on the grid, 55 had NOx data, 35 were
  order-of-magnitude consistent with EMEP/EEA factors; only 5 (PM) and 9 (SOx)
  plants had coherent data, and many report an unrepresentative zero. So:
  usable for a NOx anchor / regression on operating gas plants, weak for SOx
  and PM, self-reported. IEMA is a second Brazilian group worth talking to,
  alongside Arayara.
  https://energiaeambiente.org.br/wp-content/uploads/2025/12/IEMA_inventariotermeletricas2024-2025.pdf

Scout results: see `findings/brazil_scout_20260917.md` and
`findings/brazil_construction_scout_20260917.md`.
Where the documents live, kept current: `countries/brazil.md`.

## Vietnam

**Easier than expected.** EIAs (ĐTM) for large thermal plants are appraised by
the environment ministry (MONRE until March 2025, now the Ministry of
Agriculture and Environment). The 2020 environment law requires consultation
postings, and the ministry's portal `thamvan.mae.gov.vn` keeps the **full
report PDFs online after the window closes** — every LNG plant consulted since
2022 that was looked for was there. What remains hard: plants approved before
2022 (lender ESIAs only), and announced plants with no ĐTM yet.

- Routes: **the consultation portal first** (JSON endpoints, HTTPS only, one
  request at a time, retries — see the construction-pass file);
  provincial people's-committee portals; lender / ECA disclosure; sponsors'
  home-country disclosure (Korea, Japan, US); SFOC for Korean-backed projects.
- Search terms: `báo cáo đánh giá tác động môi trường` / `ĐTM` + `nhà máy điện
  khí LNG <tên>`, `tham vấn`, `quyết định phê duyệt`, `ống khói`, `khí thải`,
  `bụi`, `mg/Nm3`.
- National limit (fallback tier): QCVN 22:2009/BTNMT (thermal power; gas NOx
  250, SO2 300, dust 50 mg/Nm³ × Kp × Kv; in force to 30 June 2025) and its
  successor **QCVN 19:2024/BTNMT** (gas turbines at 15 % O2: NOx 50–150, SO2
  50–90, PM 15–20 mg/Nm³ depending on capacity band and receiving zone A/B/C).
  Table and links in the scout file; dry/wet basis still to confirm.
- **Anchor-plant strategy** (what Daniel did in Malaysia with Tanjung
  Kidurong) is now needed only for PM and SO2, and for plants with no ĐTM.
  Anchors in hand: six LNG-CCGT ĐTMs for NOx / CO; Quảng Trạch II for PM and
  SO2 figures; **measured** stack tests at Nhơn Trạch 2 (gas CCGT) and Ô Môn I.
  O Môn IV's ADB EIA (2007 inputs) is superseded. Still to find: the lender
  ESIA for Nhơn Trạch 3&4.

Next steps, in order: (1) list every gas / LNG entry on the portal against
GEM's Vietnamese pipeline to get a true coverage figure; (2) read the Cà Mau
1&2 GPMT report (operating, measured data); (3) Nhơn Trạch 3&4 ESIA via
lenders / ECAs / PV Power; (4) stop there — announced plants have no ĐTM to
find.

Scout results: see `findings/vietnam_scout_20260917.md` and
`findings/vietnam_construction_scout_20260917.md`.
Where the documents live, kept current: `countries/vietnam.md`.

## What goes back to CREA

A short memo (not in this repo's deliverable format) with, per country:

1. Hit rate on the sample: documents found / values found, by evidence type.
2. One or two example sources with the actual table, so Jamie and Daniel can
   pick the method.
3. Minutes per plant, and an estimate for reaching 25% coverage.
4. The fallback: national limit with its reference conditions, and any
   operating-plant data usable as an anchor.
5. Who locally could shortcut it (Arayara, IEMA in Brazil; SFOC and lenders
   for Vietnam).

## Open questions for Dan / Jamie / Daniel

- Is a **permitted limit** (mg/Nm³ at 15% O2, no flow) worth recording on its
  own, or only together with flue-gas flow? It decides whether licences without
  EIAs count as hits.
- Announced plants mostly won't have an EIA (confirmed: Long Son, Son My II).
  Sample only pre-construction and construction plants for document-hunting,
  and treat announced ones as method-D by design?
- When an EIA's NOx rate is simply the legal limit or OEM guarantee × flow
  (Kennedy, Sergipe, most ĐTMs), does CREA want it as B/C evidence, or filed
  as "limit only"?
- ĐTMs assert zero PM and SO2 on gas while measured dust at Nhơn Trạch 2 is
  19–31 mg/Nm³. Which does CREA use — and is total dust usable for PM2.5?
- Where regulator and developer disagree on the limit (Lins, 9 vs 25 ppm),
  which goes in until the licence is found?
- Construction-status plants were tried (second pass) and were no easier than
  pre-construction ones. Keep the frame as announced / pre-construction /
  construction together?
- Can a partner in Brazil (Arayara, IEMA) test SEMACE-CE and ADEMA-SE access
  from a Brazilian connection?
- For the "easy" comparison country (Germany or Canada were floated), run the
  same 3-plant probe so the effort estimates are comparable?
- Unfunded-work ceiling: how many hours is this scoping allowed to take before
  the grant decision?
