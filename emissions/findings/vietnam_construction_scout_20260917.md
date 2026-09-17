# Vietnam — construction-stage pass and the consultation portal (2026-09-17)

Second pass, same day as `vietnam_scout_20260917.md`. Two things changed the
picture: three **construction-stage** plants were scouted, and the ministry's
ĐTM consultation portal — written off as unreachable in the first pass — was
got into. The portal is the main result.

*Checked* = I read the value in the downloaded file. *Scout* = reported by a
search agent, not re-read by me. Values are in the documents' own notation
(decimal comma).

## Summary

| Plant | Why looked at | Document | Evidence |
|---|---|---|---|
| Thái Bình LNG (2 × 750 MW) | construction sample | full ĐTM, consultation draft, June 2025 | **B + C + stack + hours** *(checked)* |
| Hiệp Phước ph. 1 (3 × SGT5-4000F) | construction sample | none — ĐTM approved Feb 2021, before the portal existed | nothing *(scout)* |
| Ô Môn IV (2 × M701JAC) | construction sample | none newer than the 2007 ADB EIA; lender ESIA still being procured | nothing new *(scout)* |
| Hải Lăng ph. 1 | **first-pass sample plant** | full ĐTM on the portal | **B + C + stack + hours** *(checked)* |
| Hải Phòng LNG | found on portal | full ĐTM, Aug 2025 | **B + C + stack + hours** *(checked)* |
| Quảng Trạch II LNG | found on portal | full ĐTM, May 2025 edition | **B + C + stack + hours**, incl. PM and SO2 *(checked)* |
| Quảng Trạch III LNG | found on portal | full ĐTM, Dec 2025 | **B + C + stack** *(checked)* |
| Cà Ná LNG (2 × 750 MW) | found on portal | full ĐTM, consultation draft, June 2026 | **B + C + stack + hours**, NOx and CO only *(checked)* |
| Nhơn Trạch 3&4 | found on portal | environmental-permit (GPMT) report, Feb 2024 | stack parameters + turbine model only *(checked)* |
| Ô Môn I (operating, oil → gas conversion) | found by the Ô Môn IV scout | GPMT report, May 2026 | **measured** stack tests 2023–25 *(checked)* |
| Nhơn Trạch 2 (operating CCGT, 750 MW) | found on portal | GPMT report, Dec 2024 | **measured** quarterly stack tests 2022–24 + stack parameters *(checked)* |

Construction sample: 1 of 3 with numbers. But the portal turns the first-pass
"0 of 3, don't attempt 25 %" into something much better: every LNG plant whose
ĐTM went to consultation since 2022 appears to have its full report still
downloadable. Listed, not downloaded: Cà Mau 1&2 GPMT (2025), Bà Rịa, and the
Sơn Mỹ, Vũng Áng and Thị Vải LNG terminals.

## The portal: `thamvan.mae.gov.vn`

- **What it is.** The environment ministry's statutory consultation site. Since
  the 2020 environment law took effect (Jan 2022) every ministry-appraised ĐTM
  is posted here before appraisal, and environmental-permit (GPMT) reports for
  operating plants are posted too. Files stay up after the window closes.
- **Why the first pass failed.** `http://` and the old `thamvan.monre.gov.vn`
  host reset the connection; `https://thamvan.mae.gov.vn` works but the TLS
  handshake fails roughly every other attempt (curl exit 35). It is flakiness,
  not a block: retry serially, up to ~8 times, resume with `-C -`.
- **How to use it.**
  - search: `https://thamvan.mae.gov.vn/?searchString=<term>&page=N` (also
    `/Home/DSDTM?searchString=` for ĐTMs, `/Home/DSGiayPhep?searchString=` for
    permits). Search on `LNG`, `nhiệt điện`, `điện khí`, the plant name, the
    province.
  - detail pages are empty shells; the data come from
    `/XemChiTiet/XemChiTiet?id=<N>` (JSON: owner, consultant, dates, files).
  - files: `/Uploads/<ddmmyyyy>/<name>.pdf`, 2–250 MB, mostly with a usable
    text layer (`pdftotext -layout`).
- **Coverage limits.** Nothing approved before 2022 (Hiệp Phước), nothing for
  plants that have not reached the ĐTM stage (Sơn Mỹ II, Long Sơn, Ô Môn III/IV
  so far). Consultation drafts, not the approved final — see Quảng Trạch II
  below for how much that can matter.

Entries used (id → posted):
1440 Hải Lăng (2024-01-04) · 2462 Nhơn Trạch 3&4 GPMT (2024-02-18) ·
4786 / 4954 Quảng Trạch II (2025-03-17 / 2025-05-20) · 4985 Thái Bình
(2025-06-05) · 5824 Hải Phòng (2025-08-07) · 6086 Quảng Trạch III
(2025-12-14) · 6315 Cà Ná (2026-06-07) · 4530 Nhơn Trạch 2 GPMT (2024-12-08) ·
5894 Cà Mau 1&2 GPMT (2025-09-18).

## Construction sample

### Thái Bình LNG — full hit *(checked)*

ĐTM consultation draft, June 2025; owner Công ty CP Điện khí LNG Thái Bình;
consultant Viện Năng lượng. 1.500 MW (2 × 750 gross), 6.000 h/yr, 9,00 TWh.
https://thamvan.mae.gov.vn/Uploads/06062025/TL06.06.%20BC%20DTM%20DA%20NM%20NHIET%20DIEN%20LNG%20THAI%20BINH.pdf

| | Gas | Oil backup (≤3 days per event) |
|---|---|---|
| NOx as NO2, mg/Nm³ (dry, 15 % O2) — Bảng 3-10 | 12,23 | 12,23 |
| PM / SO2 / CO, mg/Nm³ | ~0 / ~0 / 7,10 | 20 / 250 / 7,33 |
| NOx / PM / SO2 / CO, g/s per unit — Bảng 3-12 | 13,3 / ~0 / ~0 / 7,74 | 13,3 / 21,8 / 69,60 / 7,66 |
| Exit velocity, temperature | 23,4 m/s, 361 K | 25,6 m/s, 414 K |

Stacks 60 m × 7,5 m internal diameter, UTM coordinates for both candidate
layouts (Bảng 3-11); flue gas 1.035,65 m³/s per stack. NOx is low because an
**SCR at ~80 % efficiency is required** (site is next to a nature reserve, so
QCVN 19:2024 column B applies). A failure case is modelled: SCR of one unit
out, 51,32 g/s. Turbine model not stated. My arithmetic, not the document's:
13,3 g/s × 6.000 h ≈ 288 t NOx/yr per unit.

### Hiệp Phước phase 1 — nothing *(scout)*

ĐTM approved by Quyết định 188/QĐ-BTNMT, 1 Feb 2021 — before the portal
regime, and neither the decision nor the report was found online. Domestic
financing, so no lender disclosure. Turbines 3 × Siemens SGT5-4000F per the
2019 Siemens press release (read). The scout's construction dates conflict
with each other and are not recorded here.

### Ô Môn IV — nothing new *(scout)*

No ĐTM on the portal. The international-standard ESIA for lenders (tender
package OM4-ESIA-TVA-16) was still in procurement at last report. Turbines
2 × Mitsubishi M701JAC (Mitsubishi Power release, Sept 2025); EPC Doosan
Enerbility + PECC2. JBIC's July 2024 Block B loans cover the upstream field
and pipeline only and link no ESIA. One false lead to avoid: the "ESIA" PDF on
NEXI's disclosure page near the Block B entry is for a Nigerian pipeline.

By-product — **Ô Môn I GPMT report (May 2026)**, same site, 2 × 330 MW
oil-fired units being converted to Block B gas *(checked)*:
https://thamvan.mae.gov.vn/Uploads/22052026/8X4.1.%20BC%20GPMT%20Nhi%E1%BB%87t%20%C4%91i%E1%BB%87n%20%C3%94%20M%C3%B4n%20I.pdf
Periodic stack tests (mg/Nm³, two stacks): 2023 — PM 5,04 / 7,28, SO2 217 /
214, NOx 235 / 239; 2024 round 1 — PM 7,76 / 13,47, SO2 34 / 157, NOx 251 /
271; round 2 — PM 72,2 / 75,3, SO2 242 / 123, NOx 128 / 157; 2025 (one stack)
— PM <12, SO2 110, NOx 70. CEMS on both stacks at 33 m. Oil-fired, so not an
anchor for gas — but it shows GPMT reports carry **measured** data, which is
what CREA wants for operating plants (Cà Mau 1&2, Nhơn Trạch 2 are posted).

## Found on the portal

### Hải Lăng phase 1 *(checked)* — first-pass sample plant

The first pass said the report "is not online". It is: portal id 1440, posted
2024-01-04, 124 MB, consultant Viện Năng lượng.
https://thamvan.mae.gov.vn/Uploads/05012024/FBDTM%20du%20an%20LNG%20Hai%20Lang%20Giai%20doan%201%20-%20Bao%20cao%20day%20du%20%28scan%29.pdf

- Bảng 3-12: NOx 51 mg/Nm³ (dry, 15 % O2) = the IFC guideline value; PM ~0,
  SO2 ~0.
- Bảng 3-13: two stacks, 60 m × 7,7 m, 21,16 m/s, 351 K, **NOx 53,31 g/s per
  stack**, UTM coordinates. No NOx abatement. CALPUFF.
- 6.000 h/yr; CO2 249.324 kg/h → 1.495.944 t/yr.
- The appraisal-comment table in the same file has a reviewer pointing out
  that 53,31 g/s and the stated flow imply 63,76, not 51, mg/Nm³ — the
  internal inconsistency is on the record.

### Hải Phòng LNG *(checked)*

Vingroup / Vinenergo; consultant PECC1; 4.800 MW in two phases; 6.000 h/yr.
https://thamvan.mae.gov.vn/Uploads/08082025/UJ08.8.%20BC%20DTM%20DA%20NM%20NHIET%20DIEN%20LNG%20HP.pdf
Bảng 3.30, identical for each of six stacks: 60 m × 8 m, 26,51 m/s, 87,74 °C,
1.332,3 m³/s, **NOx 47,02 mg/Nm³ | 62,4 g/s, CO 6,44 mg/Nm³ | 8,59 g/s**,
VN2000 coordinates. "No PM or SO2" asserted. No SCR. (The text says eight
stacks in one place and six in another.)

### Quảng Trạch II LNG *(checked)*

EVNPMB2; May 2025 edition; 1.725 MW; 6.000–6.500 h/yr.
https://thamvan.mae.gov.vn/Uploads/23052025/RA21.5..%20BC%20DTM%20NM%20NHIET%20DIEN%20LNG%20QUANG%20TRACH%20II.pdf
Bảng 3.31: 2 stacks, 60 m × 6 m, 87,76 °C, 1.025,90 m³/s per stack; NOx 47,
**SO2 4, PM 10 mg/Nm³** (dry, 15 % O2, 25 °C); both stacks together **NOx
86,97, SO2 6,78, PM 16,95 g/s**. The footnotes give provenance, which is rare
and useful: NOx is the OEM guarantee of 25 ppmv × 1,88; SO2 is a conservative
4,0 against the LNG supplier's ~0,025; PM is a conservative 10,0 against 3,46
computed from US EPA AP-42. The only Vietnamese document seen so far that
gives non-zero PM and SO2 for gas firing.

The approved version differs: Quảng Trạch III's ĐTM quotes the Quảng Trạch II
ĐTM as approved (Quyết định 4025/QĐ-BNNMT, 27 Sep 2025) at 8 m diameter,
1.104,9 m³/s and NOx 118,83 g/s. **Consultation drafts are not final.**

### Quảng Trạch III LNG *(checked)*

EVNPMB2; consultant PECC2; Dec 2025.
https://thamvan.mae.gov.vn/Uploads/30122025/IZ8O%5BLNG-QT3%5D%20BaoCao_DTM_LNG_QT3_Full-2025.12.pdf
Bảng 3.21: 2 stacks, 60 m × 8,3 m, 100 °C, 1.122,6 m³/s per stack, VN2000
coordinates; NOx 47,02 and CO 114,52 mg/Nm³; both stacks NOx 117,86 and CO
287,02 g/s. PM and SO2 explicitly not calculated. The same table carries
Quảng Trạch I (coal) and II for the cumulative assessment.

### Cà Ná LNG *(checked)*

ĐTM consultation draft, portal id 6315, posted June 2026; 253 MB, 727 pages —
it took five attempts with `curl -C -` resume to land. Trung Nam – Sideros
River consortium, 1.500 MW (2 units), Tmax 6.000 h/yr.
https://thamvan.mae.gov.vn/Uploads/08062026/L5Bao%20cao%20%C4%90TM%20nh%C3%A0%20m%C3%A1y%20nhi%E1%BB%87t%20%C4%91i%E1%BB%87n%20LNG%20C%C3%A0%20N%C3%A1%20tham%20v%E1%BA%A5n.pdf

- Bảng 3.27: NOx (as NO2) **68,02 mg/Nm³**, CO 20,72 mg/Nm³ (25 °C, dry;
  15 % O2 for NOx, 4 % for CO), against QCVN 19:2024 column B (70 / 100).
  GT PRO / GT Master output.
- Bảng 3.28–3.29: two stacks, 60 m × 7,7 m (the civil-works table says
  9,01 m), 89 °C, 999,00 m³/s each, VN2000 coordinates; **NO2 68,02 g/s, CO
  20,72 g/s per stack**.
- PM and SO2 asserted negligible, not quantified.
- Caveats: the g/s figures are numerically identical to the mg/Nm³ figures —
  concentration × ~1.000 m³/s actual flow, with no correction to normal
  conditions, so treat the mass rate as approximate. NOx here is set just
  under the new legal limit rather than at the 25 ppmv guarantee. The
  model's own 1-hour NO2 maximum (338 µg/m³) exceeds the 200 µg/m³ ambient
  standard.

### Nhơn Trạch 3&4 *(checked)* — permit report, not the lender ESIA

https://thamvan.mae.gov.vn/Uploads/27022024/VCHo%20so%20GPMT.pdf
GE 9HA.02; gas 26,764 kg/s per turbine; Bảng 3.12: stacks 60 m × 8,3 m,
3.792.884 m³/h on gas (80,8 °C, 1.000,9 kg/s), VN2000 coordinates. **No
concentrations or rates**, and the operator asks for *no* air-emission limits
to be written into the permit, on the grounds that there is no abatement
system. CEMS is installed. So: stack geometry yes, emissions no — the lender
ESIA is still the document to find.

### Nhơn Trạch 2 *(checked)* — operating gas CCGT, measured data

GPMT report, portal id 4530, posted Dec 2024.
https://thamvan.mae.gov.vn/Uploads/18122024/3DBao%20cao%20GPMT%20Nhon%20Trach%202.pdf

- Bảng 1.3: two main stacks 60 m × 6,8 m (plus two 35 m bypass stacks for
  simple-cycle running); main stacks together 1.373,7 m³/s, 97 °C, 37,83 m/s
  on gas; VN2000 coordinates. CEMS on the main stacks.
- Bảng 5.9: eleven quarterly stack tests per stack, Mar 2022 – Sept 2024,
  with measured flow (mostly 1,0–1,8 million m³/h per stack). Ranges, mg/Nm³:
  **total dust 19–31,5; SO2 always <2,62; NOx 5,6–74,1 (typically 25–55);
  CO 15–478.** Reference O2 / dry basis not stated in the table.
- Why it matters: measured dust is **not zero** on gas — it sits around
  20–30 mg/Nm³, above the 10 mg/Nm³ "conservative" figure in the Quảng Trạch
  II ĐTM and far from the "~0" most ĐTMs assert. (Total dust by a periodic
  manual method, not PM10 / PM2.5 — not interchangeable, per the QC rules.)

## What generalises

- **Portal first.** For any Vietnamese plant, search the portal before
  anything else. Lenders remain the route only for pre-2022 approvals.
- **Expect B + C + stack + hours, NOx and CO only.** Every ĐTM models full load
  with GTPro / Steam Pro output and states ~6.000 h/yr, so annual NOx is one
  multiplication away. Most assert PM and SO2 are zero on gas; only Quảng
  Trạch II puts numbers on them. CREA will need its own PM / SO2 factors.
- **NOx is the 25 ppmv guarantee, not a plant-specific prediction.** 47,02 (at
  25 °C) or 51 (at 0 °C) mg/Nm³ is the same OEM figure in different reference
  conditions — record the reference temperature. Thái Bình (SCR, 12,23) and
  Cà Ná (68,02, just under the QCVN 19:2024 limit of 70) are the exceptions. This is the Vietnamese counterpart of Brazil's "50 mg/Nm³ is
  the CONAMA limit".
- **Drafts move.** Stack diameter, flow and g/s changed between the Quảng
  Trạch II draft and the approved version. Record which version a value is
  from.
- **Operating plants:** GPMT reports hold measured periodic stack tests (with
  flow) and confirm CEMS — Nhơn Trạch 2 on gas, Ô Môn I on oil; Cà Mau 1&2 is
  posted and unread. These are the natural reality check on the ĐTMs' NOx
  guarantee and zero-PM assumption.
- Effort: once the portal was understood, ~10–15 minutes per plant to
  download, extract and find the table.

## Tracker leads (route to a normal GOGPT Update batch — not handled here)

- Turbine models: Nhơn Trạch 3&4 GE 9HA.02; Ô Môn IV Mitsubishi M701JAC; Hiệp
  Phước Siemens SGT5-4000F.
- ĐTM consultation dates (above) are status evidence for Thái Bình, Hải
  Phòng, Quảng Trạch II / III, Cà Ná; Quảng Trạch II ĐTM approved 27 Sep 2025.
- Hải Phòng LNG: 4.800 MW in two phases (1.600 + 3.200), Vingroup / Vinenergo.
- Ô Môn I: conversion from fuel oil to Block B gas under way.
