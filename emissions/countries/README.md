# Where the emissions data live — country index

One file per country: **where** NOx / SOx / PM data for gas plants can be
found, how to get at it, and what kind of evidence each source yields. This is
the living reference; it gets edited as we learn more.

It is not where values are recorded. Dated research passes and the numbers
read out of documents stay in `../findings/`; the country files point there.
Evidence types A–F are CREA's ladder, defined in `../methods_and_fields.md`
(A annual mass, B mass rate, C concentration + flow, D emission factor). The
same file defines **basis** — whether a number is measured, reported for a
real year, predicted on stated operating hours, a bare full-load rate, or a
potential figure at 8,760 h. Only the first three count as actual or
well-reasoned.

## Countries

Pipeline = plants with at least one announced, pre-construction or construction
unit, from the GOGPT pull of the date shown.

| Country | File | Pipeline | Where the documents live | Best evidence so far | Main access problem | Updated |
|---|---|---|---|---|---|---|
| Brazil | [`brazil.md`](brazil.md) | 65 plants in 20 states (pull 2026-09-18) | The licensing agency's site — a state agency, or IBAMA for some plants ≥ 300 MW; lender disclosure where a DFI lent; IBAMA RAPP open data (per CNPJ) joined through ANEEL SIGA for operating plants | Pipeline: B + C + stack, full-load rates with no operating hours (`rate-only`); the one annual figure, Lins, is 8,760 h potential. Operating: self-reported actual annual NOx tonnes | Rio de Janeiro and Ceará unreachable from a US address; the licensor of each plant unconfirmed; CEMS and licence texts not public | 2026-09-18 |
| Vietnam | [`vietnam.md`](vietnam.md) | 24 plants in 20 provinces (pull 2026-09-18) | One national site: the environment ministry's consultation portal, for anything posted since July 2023; provincial portals possibly for ĐTMs appraised since July 2025; World Bank documents for the Phú Mỹ plants | B + C + stack + stated operating hours (`design-hours`) in five of six ĐTMs, NOx and CO only (Quảng Trạch III and the 2007 Ô Môn IV EIA are rate-only); measured stack tests for three operating plants (Nhơn Trạch 2 quarterly, giving ≈300–340 t NOx in 2024; Bà Rịa one campaign; Ô Môn I on oil) | Nothing online for ĐTMs posted before July 2023; PM and SO2 are asserted zero; no public PRTR; CEMS data exist (Cà Mau 1&2) but are not published | 2026-09-18 |

## Source status labels

Used in every country file so the tables read the same way.

| Label | Meaning |
|---|---|
| **open** | Plain browser or `curl` works |
| **open, with method** | Works, but needs a specific technique — the file says which |
| **blocked** | Tried properly and not got through; the file says what was tried and what would likely work |
| **link rot** | The site answers but the documents have moved or gone; web archives are the route |
| **untested** | Known or believed to exist, not yet visited. Agency names in untested rows are pointers, not confirmed facts |
| **does not exist** | Looked for as a source class and found absent (say how hard the look was) |
| **exists, not public** | Collected by a regulator or company but not published; an access-to-information request is the route |

A blocked or untested source says nothing about whether the documents exist.

## Sources that cut across countries

| Source | What it holds | Access |
|---|---|---|
| IFC disclosure (`disclosures.ifc.org`) | Full ESIA packages for financed projects, including dispersion-modelling annexes | open; files come from `disclosuresservice.ifc.org/api/File/downloadfile?id=…` |
| IDB Invest (`idbinvest.org`) | Review summaries and action plans; the full studies less often | open |
| ADB (`adb.org`) | EIAs for financed projects | open, with method — project pages have a Cloudflare bot check, but PDFs under `/sites/default/files/linked-documents/` download directly |
| Export-credit agencies (JBIC, NEXI, K-EXIM, K-SURE, US DFC / EXIM) | ESIAs for Category A projects, usually for a limited window | untested in depth. DFC had no entry for Son My II. NEXI's page is easy to misread (see `vietnam.md`) |
| Internet Archive (Wayback) | Documents removed after a consultation window or lost in a site migration | Its lookup APIs were rate-limited, then offline, for the whole of 2026-09-17. Direct `web.archive.org/web/<timestamp>/<url>` links sometimes work when the APIs do not |

Lender documents describe the project at financial close. They are better for
anchoring operating plants than for today's pipeline.

## Adding a country

1. Pull fresh and draw a sample: `python emissions/draw_sample.py --countries <Country>`.
2. Copy [`_template.md`](_template.md) to `<country>.md` and fill it in as the
   first pass goes. Leave sections empty rather than guess.
3. Write the pass itself up in `../findings/<country>_scout_<YYYYMMDD>.md`.
4. Add a row to the table above.

Rules that carry over from `../README.md`: never cite gem.wiki,
globalenergymonitor.org or abarrelfull; a failed fetch is not evidence about
the document; copy no private contact details out of source documents.
