# Where the emissions data live — country index

One file per country: **where** NOx / SOx / PM data for gas plants can be
found, how to get at it, and what kind of evidence each source yields. This is
the living reference; it gets edited as we learn more.

It is not where values are recorded. Dated research passes and the numbers
read out of documents stay in `../findings/`; the country files point there.
Evidence types A–F are CREA's ladder, defined in `../methods_and_fields.md`
(A annual mass, B mass rate, C concentration + flow, D emission factor).

## Countries

Pipeline = plants with at least one announced, pre-construction or construction
unit, from the GOGPT pull of the date shown.

| Country | File | Pipeline | Where the documents live | Best evidence so far | Main access problem | Updated |
|---|---|---|---|---|---|---|
| Brazil | [`brazil.md`](brazil.md) | 65 plants in 20 states (pull 2026-09-17) | The licensing **state agency's** site, one per state; lender disclosure where a DFI lent; IBAMA open data for operating plants | A + B + C + stack (Lins, São Paulo); B + C + stack elsewhere | Two state agencies unreachable from a US address (Ceará, Sergipe); 14 states' portals not yet visited | 2026-09-17 |
| Vietnam | [`vietnam.md`](vietnam.md) | 24 plants in 20 provinces (pull 2026-09-17) | One national site: the environment ministry's consultation portal, for anything consulted since 2022 | B + C + stack + operating hours, NOx and CO only (six ĐTMs); measured stack tests for two operating plants | Nothing online for ĐTMs approved before 2022; PM and SO2 are asserted zero | 2026-09-17 |

## Source status labels

Used in every country file so the tables read the same way.

| Label | Meaning |
|---|---|
| **open** | Plain browser or `curl` works |
| **open, with method** | Works, but needs a specific technique — the file says which |
| **blocked** | Tried properly and not got through; the file says what was tried and what would likely work |
| **link rot** | The site answers but the documents have moved or gone; web archives are the route |
| **untested** | Known or believed to exist, not yet visited. Agency names in untested rows are pointers, not confirmed facts |

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
