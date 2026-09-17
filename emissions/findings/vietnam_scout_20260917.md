# Vietnam scout — 2026-09-17

First pass on the three sampled plants plus a hunt for a country-level anchor.
Shallow by design. *Checked* = I found the value in the downloaded document;
*scout* = reported by the search agent, not independently re-read.

> **Corrected later the same day** — see `vietnam_construction_scout_20260917.md`.
> The ministry's consultation portal is reachable after all (HTTPS, serial
> requests, retries), and it keeps full ĐTM reports online. Hai Lang's report
> was there. Lines below that this overturns are marked *corrected*.

## Summary

| Plant | EIA (ĐTM) status | Document retrieved | Evidence type |
|---|---|---|---|
| Son My II | Not yet prepared/approved, as far as can be told | none | nothing — method D |
| Long Son | None; still at feasibility / partner stage | none | nothing — method D |
| Hai Lang ph. 1 | **Approved by MONRE, 19 Dec 2024** | *corrected:* full ĐTM found on the consultation portal | **B + C + stack + hours** — values in the construction-pass file |
| *Anchor:* O Môn IV (not in sample; ADB-financed CCGT) | ADB-disclosed EIA | yes | **B and C**, with stack parameters |

Hit rate on the sample: 1 of 3 (*corrected* from 0 of 3). One usable anchor
plant found outside it, since superseded by better ones from the portal.

## Sampled plants

**Son My II (L100000405452, AES, 3 × 750 MW).** *(scout)* Feasibility study
awaiting MOIT approval; PECC3 contracted to prepare the ĐTM. A claim that an
"EIA was approved in 2022" circulates, but could not be verified and probably
refers to the Son My industrial park, not the power plant. Nothing on DFC's
project list despite the US sponsor. Tried: ministry consultation portal
(connection reset), news, PECC3, DFC, AES.

**Long Son (L100000405440, EVNGENCO3, 2 × 750 MW).** *(scout)* No ĐTM. Still
at the partner / feasibility stage — the scout found a T&T–TotalEnergies MOU
reported for Sept 2026, which does not match GEM's EVNGENCO3 ownership and
needs checking before anyone relies on it. This is the "announced ⇒ no EIA
exists yet" case, as expected.

**Hai Lang phase 1 (L100000405976, T&T / KOGAS / KOSPO / Hanwha, 1.500 MW).**
MONRE approved the ĐTM on 19 Dec 2024, per Tuổi Trẻ:
https://tuoitre.vn/phe-duyet-dtm-nha-may-dien-khi-lng-hai-lang-se-nhan-chim-1-1-trieu-m3-vat-chat-20241219161142262.htm
*(scout; article not re-read by me)*. *Corrected:* the report is on the
consultation portal — see the construction-pass file. The routes below were
not needed: Quảng Trị provincial portal and the economic-zone authority; the
consultation-portal archive; Korean sponsors' disclosure (KOSPO, KOGAS are
state-owned and publish overseas-project ESG material); K-EXIM / K-SURE;
SFOC. Status context:
https://theinvestor.vn/central-vietnam-based-hai-lang-lng-power-project-behind-schedule-authority-d15425.html.

Alternates (Ca Mau 3, Ke Ga) were barely touched.

## Anchor plant: O Môn IV (ADB project 43400-013)

ADB EIA, retrieved 2026-09-17:
https://www.adb.org/sites/default/files/linked-documents/43400-013-vie-eiaab.pdf
(ADB's project pages are Cloudflare-blocked to scripts; the
`/sites/default/files/linked-documents/` PDFs download directly.)

Table 44 (para 369) — dispersion-model inputs, O Mon II–V on natural gas
*(checked)*:

| Parameter | Value |
|---|---|
| Stack height | 40 m |
| Stack diameter | 6.6 m |
| Exit temperature | 95.3 °C |
| Exit velocity | 19.3 m/s |
| NOx | 50 mg/Nm³ → 24.4 g/s |
| SO2 | 1.2 mg/Nm³ → 0.6 g/s |
| CO | 84.79 mg/Nm³ → 41.4 g/s |
| PM10 | 10.32 mg/Nm³ → 5.0 g/s |

Caveats, all of which CREA should see before using it:

- Source data are from PECC3's **2007** feasibility study; the scenario is "all
  units emitting at peak levels all the time". Predicted, worst case, no annual
  totals → methods B and C only.
- Not clear from the table whether g/s is per stack or per 750 MW unit.
- The O Mon I natural-gas column is internally inconsistent (PM10 0.2 g/s at
  the same 10.32 mg/Nm³), and the document derives the applicable QCVN limit
  two different ways (175/210/42 vs 212.5/255/42.5 mg/Nm³). Treat the table as
  indicative.
- NOx is again exactly 50 mg/Nm³ — a design/limit-style round number, the same
  pattern as Presidente Kennedy in Brazil.
- Domestic pipeline gas, not LNG, and a design specified in 2007; the LNG
  pipeline will use newer, larger turbines (my inference, not from the document).

Also retrieved: Nhơn Trạch 3&4 lenders' environmental monitoring report
(SMBC, Mar 2025) —
http://pvpower.vn/pow-media/to-pr/608429100-SMBC-CM04_Nhon-Trach-3amp4-CCPP_Mar2025_submission-1.pdf
— construction-phase **ambient** monitoring only, no stack emissions. Its
existence shows a lender ESIA for Nhơn Trạch 3&4 exists; that ESIA (Vietnam's
first LNG CCGT) would be a much better anchor than O Môn IV and is
the single most valuable Vietnamese document to chase.

## National standards (fallback tier)

**QCVN 22:2009/BTNMT** — thermal power; in force until 30 June 2025
*(text retrieved; values from scout)*. Gas-fired: dust 50, NOx 250, SO2 300
mg/Nm³ base values; limit = C × Kp × Kv, Kp 1 / 0.85 / 0.7 by plant capacity
(≤300 / 300–1200 / >1200 MW), Kv 0.6–1.4 by location; gas turbines referenced
to 15 % O2. English copy:
https://www.env.go.jp/air/tech/ine/asia/vietnam/files/law/QCVN%2022-2009.pdf

**QCVN 19:2024/BTNMT** — industrial emissions, replaces the above
*(row values checked on disk; which column is which pollutant taken from the
scout; dry/wet basis not confirmed)*. Category 2.4, gas engines / turbines,
15 % O2, by receiving zone A / B / C, mg/Nm³:

| Capacity | SO2 | NOx | PM |
|---|---|---|---|
| > 1200 MW | 50 / 60 / 70 | 50 / 70 / 90 | 15 / 15 / 20 |
| 300–1200 MW | 50 / 70 / 80 | 50 / 90 / 110 | 15 / 15 / 20 |
| ≤ 300 MW | 50 / 80 / 90 | 70 / 120 / 150 | 15 / 15 / 20 |

https://mae.gov.vn/noidung/Lists/VBQPPL/Attachments/519/QCVN%20Khi%20thai%20cong%20nghiep_Signed.pdf

Using the limit needs each plant's zone (A/B/C), which depends on the
provincial zoning — one more lookup per plant, or assume the laxest.

## Dead ends and what was tried

- `thamvan.monre.gov.vn` / `thamvan.mae.gov.vn` (the ministry's ĐTM
  consultation portal — a JS app that does post full PDFs during the
  consultation window): connection resets from here on every route tried in
  the first pass. *Corrected:* it was a flaky TLS handshake, not a block —
  HTTPS only, one request at a time, up to 8 retries, `curl -C -` for the big
  PDFs. Reports stay up long after the window closes.
- ADB project pages: Cloudflare; worked around via direct PDF paths.
- DFC project list: no Son My entry.

## What generalises

- For **announced** plants there is usually no EIA to find yet.
  Document-hunting only makes sense for pre-construction and construction
  plants with an approved ĐTM.
- *Corrected:* ĐTMs that went to consultation since 2022 **are** kept online,
  on the consultation portal; six full ĐTMs and two permit reports were
  retrieved in the second pass. Lenders / ECAs matter only for earlier approvals (Hiệp Phước, Ô Môn
  IV, Nhơn Trạch 3&4).
- *Corrected:* plant-by-plant coverage of ~25 % looks achievable in Vietnam
  for NOx and CO. The anchor + QCVN 19:2024 approach is still what PM and SO2
  will need, because the ĐTMs mostly assert those are zero.
- Effort: the first three-plant probe cost ~2–3 h and produced no plant
  documents; with the portal, ~10–15 minutes per plant.

## Tracker leads (route to a normal GOGPT Update batch — not handled here)

- Long Son: ownership / partners may have moved (T&T–TotalEnergies MOU report)
  — verify.
- Hai Lang: ĐTM approval 19 Dec 2024 is a status-evidence point.
- Son My II: FS pending MOIT approval; PECC3 engaged for ĐTM.
