# Vietnam — where gas-plant emissions data live

Last updated: 2026-09-17, after two scouting passes. Status labels are defined
in [`README.md`](README.md). Values read out of the documents are in
`../findings/vietnam_construction_scout_20260917.md` (second pass — the one
that matters) and `../findings/vietnam_scout_20260917.md` (first pass, partly
overturned); this file only says where things are.

## At a glance

- **Who licenses:** one national body. EIAs (ĐTM) for large thermal plants are
  appraised by the environment ministry — MONRE until March 2025, now the
  Ministry of Agriculture and Environment (MAE). Provinces matter only for the
  receiving-zone lookup under QCVN 19:2024 and as a secondary place to search.
- **Best route:** the ministry's consultation portal, `thamvan.mae.gov.vn`.
  Search it before anything else.
- **What decides whether a document can be found:** the date. ĐTMs consulted
  since January 2022 are on the portal and stay there. Earlier approvals are
  not online at all; lender ESIAs are the only route. Announced plants have no
  ĐTM to find yet.
- **Evidence to expect:** B + C + stack parameters + operating hours (about
  6,000 h/yr), for **NOx and CO only**. Most ĐTMs assert PM and SO2 are zero on
  gas. Operating plants: measured periodic stack tests, in their
  environmental-permit (GPMT) reports.
- **Pipeline:** 24 plants in 20 provinces with an announced, pre-construction
  or construction unit (GOGPT pull 2026-09-17); 10 operating plants, six of
  them in Bà Rịa – Vũng Tàu.
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

| Source | Covers | URL | Status | What it yields |
|---|---|---|---|---|
| **Ministry consultation portal** | Ministry-appraised ĐTMs consulted since Jan 2022; GPMT reports | `https://thamvan.mae.gov.vn` | open, with method (below) | Full report PDFs |
| ADB | ADB-financed plants (Ô Môn IV) | `adb.org/sites/default/files/linked-documents/<file>.pdf` | open, with method — project pages are behind Cloudflare, direct PDF paths are not | EIA |
| Other lenders and ECAs (JBIC, NEXI, K-EXIM, K-SURE, SMBC, US DFC) | Pre-2022 approvals and internationally financed plants | — | untested in depth | Nothing found yet. DFC lists no Sơn Mỹ entry. JBIC's July 2024 Block B loans cover the upstream field and pipeline only |
| Sponsors' own sites | Lender monitoring reports, press releases | e.g. `pvpower.vn` | open | Turbine models; ambient monitoring only |
| Sponsors' home-country disclosure (KOSPO, KOGAS; AES) | Korean- and US-backed plants | — | untested | — |
| SFOC (Solutions for Our Climate) | Korean-financed projects | — | untested, people route | — |
| Provincial people's-committee portals, economic-zone authorities | Provincial copies and notices | — | untested — not needed so far | — |
| Vietnamese press | Approval dates and decision numbers | e.g. `tuoitre.vn`, `theinvestor.vn` | open | Status only |

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

- Anything approved before 2022 — Hiệp Phước (ĐTM approved Feb 2021).
- Plants that have not reached the ĐTM stage — Sơn Mỹ II, Long Sơn, Ô Môn
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
| Ô Môn I (operating, oil → gas conversion) | GPMT report, May 2026 | not recorded | **measured** stack tests 2023–25 | Oil-fired, so not a gas anchor |
| Ô Môn IV | ADB EIA, project 43400-013 — https://www.adb.org/sites/default/files/linked-documents/43400-013-vie-eiaab.pdf | not on portal | B + C + stack | 2007 inputs, worst case; superseded by the portal ĐTMs |
| Nhơn Trạch 3&4 | Lenders' monitoring report, SMBC, Mar 2025 (PV Power site) | not on portal | none (ambient only) | Shows a lender ESIA exists |

Listed on the portal, not yet downloaded: **Cà Mau 1&2 GPMT** (id 5894, posted
2025-09-18; operating, so measured data), Bà Rịa, and the Sơn Mỹ, Vũng Áng
and Thị Vải LNG terminals.

Looked for and not found anywhere: Hiệp Phước's ĐTM (Quyết định
188/QĐ-BTNMT, 1 Feb 2021); the Ô Môn IV lender ESIA (tender package
OM4-ESIA-TVA-16, still in procurement at last report); the Nhơn Trạch 3&4
lender ESIA. One false lead to avoid: the "ESIA" PDF on NEXI's disclosure page
near the Block B entry is for a Nigerian pipeline.

## Pipeline plants against the portal

Plant names and statuses as GEM carries them (pull 2026-09-17). Only nine of
the 24 have been checked, so this table is the to-do list.

| Plant (GEM name) | Province | GEM status | ĐTM on portal? |
|---|---|---|---|
| Thai Binh Combined Cycle | Thái Bình | construction | **yes** — 4985 |
| Haiphong LNG | Hải Phòng | construction | **yes** — 5824 |
| Ca Na | Ninh Thuận | construction | **yes** — 6315 |
| Hiep Phuoc | Hồ Chí Minh | announced / construction | no — approved before 2022 |
| O Mon Power Complex | Cần Thơ | announced / pre-construction / construction | no ĐTM for III / IV; Ô Môn I GPMT report only |
| Quynh Lap | Nghệ An | construction | not searched |
| Quang Trach Power Center | Quảng Bình | pre-construction | **yes** — II (4786, 4954) and III (6086) |
| Hai Lang | Quảng Trị | pre-construction | **yes** — 1440 |
| Son My II | Bình Thuận | pre-construction | no — ĐTM not yet prepared |
| Son My I | Bình Thuận | pre-construction | not searched (the Sơn Mỹ LNG terminal is listed) |
| Vung Ang | Hà Tĩnh | pre-construction | not searched (the Vũng Áng LNG terminal is listed) |
| LNG Nghi Son | Thanh Hóa | pre-construction | not searched |
| Cong Thanh | Thanh Hóa | pre-construction | not searched |
| Quang Ninh Combined Cycle | Quảng Ninh | pre-construction | not searched |
| Bac Lieu Project | Bạc Liêu | pre-construction | not searched |
| Long Son | Bà Rịa – Vũng Tàu | announced | no — feasibility stage |
| Ka Ga, Quang Tri Combined Cycle, Chan May, Dung Quat, Mien Trung, Nam Dinh, Long An, Ca Mau | various | announced | not searched; announced plants rarely have a ĐTM |

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
  first-pass findings file. Dry / wet basis not yet confirmed.
  https://mae.gov.vn/noidung/Lists/VBQPPL/Attachments/519/QCVN%20Khi%20thai%20cong%20nghiep_Signed.pdf
- **QCVN 22:2009/BTNMT** — thermal power, in force to 30 June 2025. Gas: NOx
  250, SO2 300, dust 50 mg/Nm³ × Kp (capacity) × Kv (location). English copy:
  https://www.env.go.jp/air/tech/ine/asia/vietnam/files/law/QCVN%2022-2009.pdf
- Using the 2024 limit needs each plant's zone, which depends on provincial
  zoning: one more lookup per plant, or assume the laxest. The ĐTM states which
  column applies (Thái Bình and Cà Ná: column B).

## Operating-plant data

GPMT reports on the portal (`/Home/DSGiayPhep`) carry periodic stack tests with
measured flow, and confirm whether CEMS is installed. Read so far: Nhơn Trạch 2
(gas CCGT) and Ô Môn I (oil). Posted and unread: Cà Mau 1&2. Not yet searched
for: the five Phú Mỹ plants (1, 2.1, 2.2, 3, 4), which with Bà Rịa are the six
operating plants in Bà Rịa – Vũng Tàu.

This is the reality check on the ĐTMs. At Nhơn Trạch 2, measured total dust
runs 19–31,5 mg/Nm³ on gas, against the "~0" most ĐTMs assert. Whether CEMS
data are published anywhere has not been checked.

## People

- **Consultants that write the ĐTMs:** Viện Năng lượng (Institute of Energy),
  PECC1, PECC2, PECC3. The same few firms recur, so their tables follow the
  same layout.
- **SFOC** for Korean-backed projects (Hải Lăng's sponsors include KOGAS and
  KOSPO).
- **PV Power and its lenders** for the Nhơn Trạch 3&4 ESIA.

## Next

1. Search the portal for every pipeline plant marked "not searched" above, to
   get a true coverage figure.
2. Read the Cà Mau 1&2 GPMT report; search the permit list for the Phú Mỹ
   plants.
3. Nhơn Trạch 3&4 lender ESIA, via lenders, ECAs or PV Power.
4. Confirm the dry / wet basis in QCVN 19:2024.
5. Stop there — announced plants have no ĐTM to find.
