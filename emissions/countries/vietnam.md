# Vietnam — where gas-plant emissions data live

Last updated: 2026-09-18, after two scouting passes and the Step 0 source
survey. Status labels are defined
in [`README.md`](README.md). Values read out of the documents are in
`../findings/vietnam_construction_scout_20260917.md` (second pass — the one
that matters) and `../findings/vietnam_scout_20260917.md` (first pass, partly
overturned); this file only says where things are.

## At a glance

- **Who licenses:** one national body. EIAs (ĐTM) for large thermal plants are
  appraised by the environment ministry — MONRE until March 2025, now the
  Ministry of Agriculture and Environment (MAE). Since 1 July 2025 part of
  that authority sits with provincial chairmen (Decree 136/2025; see "Who
  appraises"), so provinces are now a real second place to search, as well as
  the receiving-zone lookup under QCVN 19:2024.
- **Best route:** the ministry's consultation portal, `thamvan.mae.gov.vn`.
  Search it before anything else.
- **What decides whether a document can be found:** the date. ĐTMs posted
  since July 2023 are on the portal and stay there (the lists start on 10–11
  July 2023). Earlier approvals are not online at all; lender ESIAs are the only route. Announced plants have no
  ĐTM to find yet.
- **Evidence to expect:** B + C + stack parameters + operating hours (about
  6,000 h/yr, stated in the ĐTM itself — so `design-hours`, a reasoned
  estimate rather than a potential one), for **NOx and CO only**. Most ĐTMs assert PM and SO2 are zero on
  gas. Operating plants: measured periodic stack tests, in their
  environmental-permit (GPMT) reports.
- **Pipeline:** 24 plants in 20 provinces with an announced, pre-construction
  or construction unit (GOGPT pull 2026-09-18); 9 gas plants with operating
  units, six of them in Bà Rịa – Vũng Tàu. Per-plant search state:
  `../coverage/vietnam.csv`.
- **Effort:** once the portal is understood, 10–15 minutes per plant to
  download, extract and find the table.

## Document types

| Document | What it holds | Evidence | Public? |
|---|---|---|---|
| **ĐTM** (báo cáo đánh giá tác động môi trường), consultation draft | Emission concentrations and rates per stack, stack geometry and coordinates, operating hours, dispersion modelling (CALPUFF, AERMOD) from GT PRO / Steam Pro output | B + C + stack + hours | On the portal, if consulted since 2022 |
| ĐTM as approved | Same, final numbers | same | Not posted. Seen only as quoted in a neighbouring plant's ĐTM |
| Approval decision (quyết định phê duyệt) | Date and number | none | Usually known only from news |
| **GPMT report** (environmental-permit application) | Stack geometry, CEMS, and for operating plants **measured** periodic stack tests with flow | measured concentrations + flow | On the portal |
| Lender / ECA ESIA | Full ESIA to IFC standards | B + C + stack | Only for internationally financed plants; ADB's is open |
| Lenders' monitoring reports | Construction-phase ambient monitoring | none for stacks | Sometimes on the sponsor's site |

## Where to look

Source survey of 2026-09-18 (Step 0 of `../search_plan.md`): one row or more
for each of the twelve source classes, including the ones that turned out
empty. Each candidate was tried on a pipeline plant (Nhơn Trạch 3&4) and an
operating one (Phú Mỹ 2.2 / 3). Two extra labels: **does not exist** and
**exists, not public**.

| # | Class | Source | Covers | URL | Status | What it yields |
|---|---|---|---|---|---|---|
| 1 | Environmental assessment | **Ministry consultation portal** | ĐTMs and GPMT reports posted since July 2023 (1,637 + 1,132 entries at 2026-09-18) | `https://thamvan.mae.gov.vn` | open, with method (below) | Full report PDFs: B + C + stack + hours |
| 1 | | **World Bank documents** — Phú Mỹ 2.2 EIA (2002) and the Phú Mỹ 2.2 appraisal document | The five Phú Mỹ plants, pre-portal | EIA: https://documents1.worldbank.org/curated/en/181301468133799789/pdf/multi0page.pdf · PAD: https://documents1.worldbank.org/curated/en/927821468780593323/pdf/multi0page.pdf | open | The PAD's annex table "iii. Emissions" gives NOx and SO2 mg/Nm³ for Phú Mỹ 1, 2.1, 2.2, 3 and 4, on gas and on oil (NOx on gas 51–52). **Design values of 2002, not measurements**; no PM, no flow |
| 1 | | ADB | Ô Môn IV | `adb.org/sites/default/files/linked-documents/<file>.pdf` | open, with method — project pages are behind Cloudflare, direct PDF paths are not | EIA (2007 inputs) |
| 1 | | Provincial portals (people's committee, Sở Nông nghiệp và Môi trường, economic-zone boards) | Sub-threshold plants; from 1 July 2025 possibly some large ones (see "Who appraises" below) | one per province | untested | No register of which provinces post full ĐTMs |
| 2 | Permit | Ministry portal, `/Home/DSGiayPhep` | GPMT application reports | same | open, with method | Operating plants: **measured** periodic stack tests with flow. The permit itself is not posted |
| 3 | Consultation records | The portal *is* the consultation register (Law on Environmental Protection 2020, art. 33) | — | same | open, with method | Nothing beyond class 1. No separate hearing minutes |
| 4 | Emissions reporting / PRTR | None public. Annual environmental-protection reports go to the regulator; Công văn 1074/BTNMT-KSONMT (2024) only tells provinces how to build inventories | — | — | **does not exist** as a public dataset | — |
| 5 | CEMS | Operators transmit to the province and on to the ministry's Envisoft system. The public layer (`cem.gov.vn`, VN Air) shows ambient air quality only | All plants above the CEMS threshold | https://cem.gov.vn/ | **exists, not public** | Nothing at plant or stack level |
| 5 | | Operator's own disclosure — Decree 08/2022, art. 102: CEMS results shown on the operator's website or a board at the gate; periodic results within 10 days | every operating plant, in law | operators' sites | untested — no gas-plant operator page found doing it | In principle, current stack readings; nothing archived |
| 5 | | Periodic stack tests, as reproduced in GPMT reports | operating plants | portal (class 2) | open, with method | The only measured data reachable |
| 6 | Lenders and ECAs | World Bank (class 1 above); MIGA project page for Phú Mỹ 3 | Phú Mỹ 2.2, 3 | https://www.miga.org/project/phu-my-3-bot-power-company-ltd | open | MIGA: a page, no documents |
| 6 | | **SERV** (Swiss export credit), Category A project list | Nhơn Trạch 3&4 | https://www.serv-ch.com/fileadmin/user_upload/files/Projektliste/A-Projekte/ESIA_Nhon_Trach_3_and_Nhon_Trach_4_Power_Plant.pdf | open | The Fichtner ESIA, 994 pp.: B + C + stack + hours. SACE and K-SURE, the other covers, post nothing |
| 6 | | JBIC, NEXI, K-EXIM, K-SURE, US DFC, US EXIM; Proparco partly | Nghi Sơn, Vũng Áng, Hải Lăng, Sơn Mỹ I / II, Cà Ná, Hiệp Phước, Ô Môn IV | — | checked 2026-09-18, nothing | No ESIA for any of them; most have not reached financial close. JBIC's July 2024 Block B loans cover the upstream field and pipeline only. Ô Môn IV's new lender ESIA is not posted |
| 7 | Carbon market | CDM and JCM registries | — | `cdm.unfccc.int`, https://www.jcm.go.jp/projects/registers | **does not exist** for gas plants, as far as searches show (the CDM search page is JavaScript-only and was not paged through) | Gas plants appear only as grid-baseline line items in other projects' PDDs: capacity and generation, no stack data |
| 8 | Power regulator / operator | NSMO (system operator, split from EVN in Aug 2024), the electricity regulator, EVN annual reports | whole fleet | — | untested below system totals — no per-plant generation table found | Utilisation still has to come from ĐTMs (design hours) or company reports |
| 9 | Company disclosure | EVNGENCO3 sustainability reports | Phú Mỹ 1, 2.1, 4, Bà Rịa | https://bctn.genco3.com/en/sustainable-development-report/ | open | Narrative only; nothing per plant for gas |
| 9 | | PVN 2024 sustainability report; PV Power (POW) and NT2 2024 annual reports | Nhơn Trạch 1, 2, Cà Mau 1&2 | PVN 2024: https://www.pvn.vn/DataStore/2025/files/09/20250811_BC%20PTBV%20PVN_2024_VN_Final.pdf · NT2: https://finance.vietstock.vn/nt2/tai-tai-lieu.htm | open, read 2026-09-18 | **No per-plant NOx, SO2 or PM** — compliance statements only. Utilisation inputs: POW annual report p. 88, 2024 gas use (million Sm³) Cà Mau 1 480.06, Cà Mau 2 729.50, Nhơn Trạch 1 58.59, Nhơn Trạch 2 530.70; NT2 generated 2,742 million kWh, emitted 1,177,038 t CO2e and 38.6 billion m³ of flue gas, and has a stack CEMS. The NT2 report is a scan (OCR needed) |
| 9 | | Sponsors' sites and press | pipeline plants | e.g. `pvpower.vn` | open | Turbine models; lenders' ambient-monitoring reports |
| 10 | Secondary compilations | **Roy, Lam, Ngo, Chan & Fu (2020)**, *Atmospheric Environment* — 2015 inventory of Vietnamese power units | All thermal plants of 2010 and 2015; names every operating gas plant | author-hosted copy: http://acs.engr.utk.edu/publications/2020_Roy.pdf | open | Per-plant NOx, SO2, PM **estimated from emission factors and fuel use**, not measured. A cross-check and a utilisation source (generation by plant, 2015), not an anchor |
| 10 | | GreenID and similar NGO surveys; REAS / EDGAR | coal; gridded totals | — | open | Nothing usable for gas plants |
| 11 | Emission standards | QCVN 19:2024/BTNMT, QCVN 22:2009/BTNMT | national | see "National limits" | open | Reference conditions now confirmed; dry / wet basis is not stated in the text |
| 12 | Access to information, people | Law on Access to Information 2016 (104/2016/QH13): simple requests answered in days, complex ones in 15 working days plus 10; Decree 08/2022 art. 101 covers environmental information on request | any document a ministry or province holds | — | untested; open to Vietnamese citizens, so a local partner has to file | The approved ĐTM and the permit text, in principle |
| 12 | | SFOC (Korean-financed projects); the ĐTM consultants | — | — | untested, people route | — |
| — | Press | Approval dates and decision numbers | — | e.g. `tuoitre.vn`, `theinvestor.vn` | open | Status only |

### Who appraises — changed on 1 July 2025

Until then every large thermal plant's ĐTM went to the ministry. Decree
136/2025/NĐ-CP (in force 1 July 2025) hands appraisal of ministry-level
projects to the **provincial chairman**, except — among others — projects
whose investment policy was decided by the National Assembly or the Prime
Minister. Several LNG plants had their investment policy approved by the
province, so their ĐTMs may now be appraised, and consulted on, provincially.
Against that: Hải Phòng (Aug 2025), Quảng Trạch III (Dec 2025) and Cà Ná (June
2026) all appeared on the ministry portal after the change. Not settled. The
portal enumeration should record the appraising body for every post-July-2025
entry, and a pipeline plant with no portal hit needs its provincial portal
checked before it is closed as `not-found`.

### Route lists

**Pipeline track**
1. Ministry portal — enumerate completely (ĐTM and permit lists).
2. Provincial portal of any construction / pre-construction plant with no
   portal hit (because of the 2025 decentralisation).
3. Lender and ECA disclosure by sponsor nationality, after a press search for
   who actually lent: SACE and SERV for Nhơn Trạch 3&4; JBIC / NEXI for Nghi
   Sơn; K-EXIM / K-SURE for Vũng Áng and Hải Lăng; DFC / US EXIM for Sơn Mỹ
   II; Proparco for Sơn Mỹ I.
4. QCVN 19:2024 by receiving zone — the fallback for everything left.

Classes 4, 5, 7 and 8 add nothing for pipeline plants.

**Operating track**
1. Portal GPMT reports — the only measured data (Phú Mỹ 1, 2.1, 2.2, 3, 4,
   Bà Rịa, Nhơn Trạch 1, Cà Mau 1&2).
2. World Bank Phú Mỹ documents — design NOx / SO2 for the five Phú Mỹ plants,
   in hand already; useful where a GPMT report is missing.
3. PVN / PV Power and NT2 reports — one read each, for generation and any
   pollutant figures.
4. Roy et al. 2020 — factor-based cross-check and 2015 generation.
5. An access-to-information request through a partner, for permit texts and
   CEMS summaries, only if 1–4 leave gaps that matter.

### Using the portal

- **HTTPS only.** `http://` and the old `thamvan.monre.gov.vn` host reset the
  connection.
- The TLS handshake fails roughly every other attempt (curl exit 35). It is
  flakiness, not a block: **one request at a time, up to about 8 retries**, and
  `curl -C -` to resume big files. The 253 MB Cà Ná report took five attempts.
- Search: `https://thamvan.mae.gov.vn/?searchString=<term>&page=N`. ĐTMs only:
  `/Home/DSDTM?searchString=`. Permits only: `/Home/DSGiayPhep?searchString=`.
- Search on `LNG`, `nhiệt điện`, `điện khí`, the plant name, the province.
- Detail pages are empty shells. The data come from
  `/XemChiTiet/XemChiTiet?id=<N>` — JSON with owner, consultant, dates and the
  file list.
- Files: `/Uploads/<ddmmyyyy>/<name>.pdf`, 2–250 MB, mostly with a usable text
  layer (`pdftotext -layout`).

### What the portal does not have

- Anything posted before July 2023. Both lists start on 10–11 July 2023
  (full inventory, 2026-09-18: `../coverage/vietnam_portal_all.csv`). Hiệp
  Phước (ĐTM approved Feb 2021) is one casualty.
- Any GPMT report for the five Phú Mỹ plants. The operating plants with a
  report are Nhơn Trạch 2 (4530), Nhơn Trạch 3&4 (2462), Cà Mau 1&2 (5894),
  Bà Rịa (5807) and Ô Môn I (6303). The Phú Mỹ permits were presumably
  handled outside this portal (province, or before July 2023).
- Plants that have not reached the ĐTM stage — Long Sơn, Ô Môn
  III / IV as of 2026-09-17.
- The approved final. Posted reports are consultation drafts, and they move:
  Quảng Trạch II's stack diameter, flow and NOx g/s all changed between the
  draft and the approved version. Record which version a value came from.

## Documents in hand

All on the portal unless noted. Full URLs are in the second-pass findings file.

| Plant | Document, date | Portal id | Evidence | Caveat |
|---|---|---|---|---|
| Hải Lăng ph. 1 | Full ĐTM, posted 2024-01-04 | 1440 | B + C + stack + hours | NOx 51 mg/Nm³ is the IFC guideline value; a reviewer notes the rate and the concentration do not agree |
| Thái Bình LNG | ĐTM draft, June 2025 | 4985 | B + C + stack + hours, gas and oil backup | SCR required, so NOx is far lower than elsewhere; SCR-failure case modelled |
| Hải Phòng LNG | ĐTM, Aug 2025 | 5824 | B + C + stack + hours | "No PM or SO2" asserted; six vs eight stacks inconsistent in the text |
| Quảng Trạch II LNG | ĐTM, March and May 2025 editions | 4786, 4954 | B + C + stack + hours, **incl. PM and SO2** | Only ĐTM with non-zero PM and SO2 on gas, with provenance footnotes. The approved version differs |
| Quảng Trạch III LNG | ĐTM, Dec 2025 | 6086 | B + C + stack | Quotes Quảng Trạch II as approved; PM and SO2 not calculated |
| Cà Ná LNG | ĐTM draft, June 2026 | 6315 | B + C + stack + hours | g/s equals mg/Nm³ numerically — mass rate approximate; NOx set just under the new limit |
| Nhơn Trạch 3&4 | GPMT report, Feb 2024 | 2462 | stack parameters + turbine model only | No concentrations or rates; the operator asks for no air limits in the permit |
| Nhơn Trạch 2 (operating CCGT) | GPMT report, Dec 2024 | 4530 | **measured** quarterly stack tests 2022–24, with flow | Total dust, not PM10 / PM2.5; reference O2 not stated |
| Bà Rịa (operating, 10 units, rarely dispatched) | GPMT report (scanned), July 2025 | 5807 | **measured** one campaign, GT3–8, June 2024, + GT7 Dec 2024 | Asks for no air permit; no further tests, no CEMS. `../findings/vietnam_gpmt_pilot_20260918.md` |
| Cà Mau 1&2 (operating CCGT) | GPMT report, Sep 2025, main + 5 annexes | 5894 | CEMS on 6 stacks, **values not published**; 2004 CM1 ĐTM design values (annex 1) | No periodic tests; asks for no air permit. Same findings file |
| Ô Môn I (operating, oil → gas conversion) | GPMT report, May 2026 | not recorded | **measured** stack tests 2023–25 | Oil-fired, so not a gas anchor |
| Ô Môn IV | ADB EIA, project 43400-013 — https://www.adb.org/sites/default/files/linked-documents/43400-013-vie-eiaab.pdf | not on portal | B + C + stack | 2007 inputs, worst case; superseded by the portal ĐTMs |
| Nhơn Trạch 3&4 | Lenders' monitoring report, SMBC, Mar 2025 (PV Power site) | not on portal | none (ambient only) | Shows a lender ESIA exists |
| Nhơn Trạch 3&4 | Fichtner ESIA, Vol. 1 approved 08.03.2024 (SERV) | not on portal | B + C + stack + hours, incl. SO2 and dust | Rates and concentrations agree; no SCR. `../findings/vietnam_nhon_trach_34_esia_20260918.md` |

Listed on the portal, not yet downloaded: the Sơn Mỹ, Vũng Áng and Thị Vải
LNG terminals.

Looked for and not found anywhere: Hiệp Phước's ĐTM (Quyết định
188/QĐ-BTNMT, 1 Feb 2021); the Ô Môn IV lender ESIA (tender package
OM4-ESIA-TVA-16, still in procurement at last report). One false lead to avoid: the "ESIA" PDF on NEXI's disclosure page
near the Block B entry is for a Nigerian pipeline.

## Pipeline plants against the portal

Full portal inventory (2026-09-18), then provincial portals and one news check
for every plant without a hit. Per-plant detail and URLs in
`../coverage/vietnam.csv`.

| Plant (GEM name) | Province | GEM status | Result |
|---|---|---|---|
| Thai Binh Combined Cycle | Thái Bình | construction | **ĐTM on portal**, 4985 |
| Haiphong LNG | Hải Phòng | construction | **ĐTM on portal**, 5824 |
| Ca Na | Ninh Thuận | construction | **ĐTM on portal**, 6315 |
| Quang Trach Power Center | Quảng Bình | pre-construction | **ĐTM on portal**, II (4786, 4954) and III (6086) |
| Hai Lang | Quảng Trị | pre-construction | **ĐTM on portal**, 1440 |
| O Mon Power Complex | Cần Thơ | announced / pre-construction / construction | 2011 ADB EIA for IV; no III / IV ĐTM anywhere |
| Hiep Phuoc | Hồ Chí Minh | announced / construction | ĐTM approved Feb 2021, before the portal; not online |
| Son My I, Son My II | Bình Thuận | pre-construction | ĐTMs **approved by MONRE in 2022**, before the portal; not online |
| Bac Lieu Project | Bạc Liêu | pre-construction | ĐTM approval reported for Sep 2021 (not verified); not online |
| Quang Ninh Combined Cycle | Quảng Ninh | pre-construction | ĐTM appraisal approved (press; date not given); not online |
| Quynh Lap | Nghệ An | construction | not found — portal, Nghệ An sites, press |
| Cong Thanh | Thanh Hóa | pre-construction | not found — only the superseded coal-phase ĐTM exists |
| Vung Ang | Hà Tĩnh | pre-construction | none expected — investment policy approved 9 June 2026. The PV GAS terminal's ĐTM is on the portal (6318) |
| LNG Nghi Son | Thanh Hóa | pre-construction | none expected — no investor yet |
| Long Son | Bà Rịa – Vũng Tàu | announced | none expected — feasibility stage |
| Ka Ga, Mien Trung, Dung Quat, Nam Dinh, Chan May | various | announced | none expected (Nam Định has only a 2018 coal-design ĐTM) |
| Long An | Long An | announced | press says a ĐTM was approved around May 2025 — not verified, still to check |
| Quang Tri Combined Cycle | Quảng Trị | announced | news check still to redo |
| Ca Mau | Cà Mau | announced (unit 3) | nothing for Cà Mau 3 |

So: 6 plants with a ĐTM in hand, 5 whose ĐTM exists but predates the portal
and is not online, 2 not found, 9 with nothing yet to find, 2 open. No
pipeline plant turned up a ĐTM consulted provincially under Decree 136/2025.

## Inside the document

- Chapter 3 (impact assessment), the air-emissions section. The tables wanted
  are "Bảng 3.x": emission concentrations, then the dispersion-model source
  parameters (stack height, diameter, velocity, temperature, flow, g/s,
  coordinates in VN2000 or UTM).
- Search terms: `báo cáo đánh giá tác động môi trường` / `ĐTM` + `nhà máy điện
  khí LNG <tên>`, `tham vấn`, `quyết định phê duyệt`; inside the PDF: `ống
  khói`, `khí thải`, `tải lượng`, `nồng độ`, `bụi`, `mg/Nm3`, `g/s`.
- **NOx is the OEM's 25 ppmv guarantee, not a plant-specific prediction.**
  47,02 mg/Nm³ (at 25 °C) and 51 (at 0 °C) are the same figure under different
  reference conditions, so record the reference temperature. Exceptions:
  Thái Bình (SCR, 12,23) and Cà Ná (68,02, just under the limit of 70).
- Operating hours are stated, about 6,000 h/yr, so annual NOx is one
  multiplication away. The document itself does not do it.
- Check the mass rate against concentration × flow. Hải Lăng and Cà Ná are both
  internally inconsistent.
- The appraisal-comment table at the back of a report can flag the errors for
  you (Hải Lăng).
- A neighbouring plant's ĐTM may quote another plant's **approved** values in
  its cumulative assessment (Quảng Trạch III quotes II).
- Decimal comma, thousands point.

## National limits (fallback tier)

- **QCVN 19:2024/BTNMT** — industrial emissions, in force from 1 July 2025.
  Category 2.4, gas engines and turbines, 15 % O2, by receiving zone A / B / C
  and capacity band: NOx 50–150, SO2 50–90, PM 15–20 mg/Nm³. Full table in the
  first-pass findings file. Nm³ is defined at 25 °C and 760 mmHg (§1.3.10).
  The text nowhere states a dry or wet basis.
  https://mae.gov.vn/noidung/Lists/VBQPPL/Attachments/519/QCVN%20Khi%20thai%20cong%20nghiep_Signed.pdf
- **QCVN 22:2009/BTNMT** — thermal power, in force to 30 June 2025. Gas: NOx
  250, SO2 300, dust 50 mg/Nm³ × Kp (capacity) × Kv (location). English copy:
  https://www.env.go.jp/air/tech/ine/asia/vietnam/files/law/QCVN%2022-2009.pdf
- Using the 2024 limit needs each plant's zone, which depends on provincial
  zoning: one more lookup per plant, or assume the laxest. The ĐTM states which
  column applies (Thái Bình and Cà Ná: column B).

## Operating-plant data

GPMT reports on the portal (`/Home/DSGiayPhep`) are the only place measured
stack data for operating gas plants turned up. Pilot of all three gas plants
with one, 2026-09-18: `../findings/vietnam_gpmt_pilot_20260918.md`.

- **Nhơn Trạch 2**: quarterly stack tests 2022–24 with flow. Combined with the
  NT2 annual report's CO2 and gas use, **≈300–340 t NOx in 2024 (0.11–0.12
  t/GWh)**. The annual report's own flue-gas volume fails a carbon-balance
  check (~70 % too high), so don't use it.
- **Bà Rịa**: one test campaign (June 2024) plus one retest; the plant runs at
  ~4 % capacity factor. Roughly 86 t NOx/yr on 2022–24 generation.
- **Cà Mau 1&2**: CEMS on every stack, but the report gives only data
  completeness, no concentrations, and there are no periodic tests. The data
  go to the Cà Mau department and the ministry: `exists, not public`, and an
  information-request target. Only 2004 design values are in the package.
- **Phú Mỹ 1, 2.1, 2.2, 3, 4**: no GPMT report or ĐTM on the portal (full
  inventory). World Bank design documents only.

Bà Rịa and Cà Mau both ask for permits with no air-emissions component and
propose no future stack tests, so the GPMT route will get thinner, not richer.
Measured dust at NT2 runs 19–31,5 mg/Nm³ on gas, against the "~0" most ĐTMs
assert. CEMS data are not published anywhere (source table, class 5).

## People

- **Consultants that write the ĐTMs:** Viện Năng lượng (Institute of Energy),
  PECC1, PECC2, PECC3. The same few firms recur, so their tables follow the
  same layout.
- **SFOC** for Korean-backed projects (Hải Lăng's sponsors include KOGAS and
  KOSPO).
- **PV Power and its lenders** for the Nhơn Trạch 3&4 ESIA.

## Tracker leads (route to a normal GOGPT Update batch — not handled here)

Press found during the 2026-09-18 lender sweep, not verified to the GOGPT
evidence bar:

- Nghi Sơn LNG: investor tenders cancelled; no investor as of May 2026.
- Vũng Áng III LNG: awarded to PV Power + Lilama + B.Grimm, 9 June 2026 (not
  KEPCO).
- Ô Môn III and IV: transferred to Petrovietnam in 2023.
- Cà Ná LNG: now Trung Nam – Sideros River (April 2026).
- Hiệp Phước LNG: now Hải Linh; groundbreaking 26 March 2026.
- Bà Rịa (L100000405433): GEM has "operating x1; cancelled - inferred 4 y x1"
  at 389 MW; the GPMT report (id 5807, p. 18) lists ten units in service, GT1–8
  and ST9–10, totalling 388.9 MW.

## Next

1. Long An: verify the press claim of a ĐTM approval around May 2025.
   Quảng Trị Combined Cycle: redo the news check.
2. Cà Mau CEMS data: an information request to the Cà Mau department or the
   ministry is the only route. Decide whether it is worth making.
3. Phú Mỹ plants: EVN / Genco 3 annual reports for fuel and generation, to
   pair with the World Bank design values (`rate-only` + real fuel).
4. QCVN 19:2024 receiving zones for each pipeline plant (deferred).
5. Inactive plants and the cross-country rollup (deferred).
