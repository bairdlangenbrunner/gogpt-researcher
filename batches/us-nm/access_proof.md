# Access proof: us-nm

Checked 2026-11-17T08:53:53. 32 of 34 sources proven; 2 behind a person's action.

| id | ok | route | status | kind | bytes | reason or person |
|---|---|---|---|---|---|---|
| abq-air-quality | yes | curl | 200 | html | 128942 |  |
| business-registry | NO | curl | 200 | html | 592 | PERSON: The search is a script page behind a Cloudflare Turnstile check (probed 2026-11-17), and no script gets past it. Baird looks up each company named in the batch's questions on https://enterprise.sos.nm.gov/search/business and pastes the registered name, formation date and principal office into the question. |
| captive-lng-sheet | yes | gws-gem | 200 |  | 0 |  |
| data-centers | yes | disk_cache | 200 | html | 247141 |  |
| eia-860 | yes | curl | 200 | html | 67578 |  |
| eia-860m | yes | curl | 200 | html | 93652 |  |
| eip-oil-gas-watch | yes | curl | 200 | html | 1946 |  |
| epa-campd | yes | curl | 200 | json | 56585 |  |
| epa-echo | yes | curl | 200 | json | 157942 |  |
| epa-r9-ntec | yes | curl | 200 | json | 16776 |  |
| epa-rblc | yes | curl | 200 | html | 62335 |  |
| epe-news | yes | curl | 200 | html | 104536 |  |
| epe-queue | yes | curl | 200 | pdf | 206317 |  |
| farmington-electric | yes | curl | 200 | html | 193586 |  |
| industrial-cogeneration | yes | curl | 200 | html | 1291853 |  |
| lbnl-queued-up | yes | cf_impersonate | 200 | html | 50388 |  |
| local-planning-records | yes | curl | 200 | json | 814820 |  |
| nmed-apmap | yes | curl | 200 | json | 69 |  |
| nmed-coda-pending | NO | curl | 200 | html | 69927 | PERSON: The Coda pages load rows only in a browser, and the Coda API needs a sign-in token (401 without one, probed 2026-11-17). Baird opens each of the three tables, exports it as CSV and saves it under scopes/us-nm/work/permits/coda/, or sets a personal CODA_API_TOKEN outside the repo. |
| nmed-comment-portal | yes | curl | 200 | html | 103422 |  |
| nmed-public-notices | yes | curl | 200 | html | 1291853 |  |
| ntec | yes | curl | 200 | html | 9752 |  |
| pnm-irp | yes | curl | 200 | html | 179689 |  |
| pnm-news | yes | curl | 200 | html | 363062 |  |
| pnm-queue | yes | insecure_tls | 200 | html | 443 |  |
| possible-updates-sheet | yes | gws-gem | 200 |  | 0 |  |
| prc-e360-cases | yes | direct_post | 200 | json | 659 |  |
| public-notices | yes | curl | 200 | html | 110267 |  |
| sec-edgar | yes | sec_declared_ua | 200 | json | 87036 |  |
| spp-queue | yes | curl | 200 | csv | 241797 |  |
| state-news | yes | curl | 200 | html | 156385 |  |
| tristate | yes | curl | 200 | html | 129225 |  |
| tristate-queue | yes | insecure_tls | 200 | html | 444 |  |
| xcel-sps | yes | curl | 200 | html | 59533 |  |

Samples are under the scope's work folder (`access/`), never committed. A NO with no PERSON line blocks the batch: fix the route (fetch.py --render, a harvester, the real document's address) and run the check again.
