# Access proof: us-nm

Checked 2026-11-19T09:07:41. 33 of 34 sources proven; 1 behind a person's action.

| id | ok | route | status | kind | bytes | reason or person |
|---|---|---|---|---|---|---|
| abq-air-quality | yes | curl | 200 | html | 129746 |  |
| business-registry | yes | disk_cache | 200 | html | 51029 |  |
| captive-lng-sheet | yes | gws-gem | 200 |  | 0 |  |
| data-centers | yes | disk_cache | 200 | html | 247141 |  |
| eia-860 | yes | curl | 200 | html | 67578 |  |
| eia-860m | yes | curl | 200 | html | 94695 |  |
| eip-oil-gas-watch | yes | disk_cache | 200 | html | 21612 |  |
| epa-campd | yes | curl | 200 | json | 16871 |  |
| epa-echo | yes | curl | 200 | json | 158334 |  |
| epa-r9-ntec | yes | curl | 200 | json | 16776 |  |
| epa-rblc | yes | curl | 200 | html | 62335 |  |
| epe-news | yes | curl | 200 | html | 105058 |  |
| epe-queue | yes | curl | 200 | pdf | 203067 |  |
| farmington-electric | yes | curl | 200 | html | 192024 |  |
| industrial-cogeneration | yes | curl | 200 | html | 1292377 |  |
| lbnl-queued-up | yes | cf_impersonate | 200 | html | 50388 |  |
| local-planning-records | yes | curl | 200 | json | 814820 |  |
| nmed-apmap | yes | curl | 200 | json | 69 |  |
| nmed-coda-pending | NO | curl | 200 | html | 69832 | PERSON: The Coda pages load rows only in a browser, and the Coda API needs a sign-in token (401 without one, probed 2026-11-17). Baird opens each of the three tables, exports it as CSV and saves it under scopes/us-nm/work/permits/coda/, or sets a personal CODA_API_TOKEN outside the repo. |
| nmed-comment-portal | yes | curl | 200 | html | 107412 |  |
| nmed-public-notices | yes | curl | 200 | html | 1292023 |  |
| ntec | yes | curl | 200 | html | 9752 |  |
| pnm-irp | yes | curl | 200 | html | 179782 |  |
| pnm-news | yes | curl | 200 | html | 362913 |  |
| pnm-queue | yes | insecure_tls, pdf_via_ladder | 200 | pdf | 160771 |  |
| possible-updates-sheet | yes | gws-gem | 200 |  | 0 |  |
| prc-e360-cases | yes | direct_post | 200 | json | 659 |  |
| public-notices | yes | disk_cache | 200 | html | 118792 |  |
| sec-edgar | yes | sec_declared_ua | 200 | json | 61181 |  |
| spp-queue | yes | curl | 200 | csv | 241827 |  |
| state-news | yes | curl | 200 | html | 156385 |  |
| tristate | yes | curl | 200 | html | 129225 |  |
| tristate-queue | yes | insecure_tls, pdf_via_ladder | 200 | pdf | 32612 |  |
| xcel-sps | yes | curl | 200 | html | 59533 |  |

Samples are under the scope's work folder (`access/`), never committed. A NO with no PERSON line blocks the batch: fix the route (fetch.py --render, a harvester, the real document's address) and run the check again.
