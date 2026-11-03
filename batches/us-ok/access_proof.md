# Access proof: us-ok

Checked 2026-11-03T15:03:58. 25 of 26 sources proven; 1 behind a person's action.

| id | ok | route | status | kind | bytes | reason or person |
|---|---|---|---|---|---|---|
| aeci | yes | curl | 200 | html | 73444 |  |
| captive-lng-sheet | yes | gws-gem | 200 |  | 0 |  |
| data-centers | yes | cf_clearance | 200 | html | 100645 |  |
| eia-860 | yes | curl | 200 | html | 67537 |  |
| eia-860m | yes | curl | 200 | html | 93611 |  |
| eip-oil-gas-watch | yes | curl | 200 | html | 1946 |  |
| evergy-irp | yes | cf_impersonate, pdf_via_ladder | 200 | html | 5908 |  |
| grda | yes | curl | 200 | html | 129241 |  |
| local-planning-records | yes | cf_impersonate | 200 | html | 159482 |  |
| occ-ecf | yes | curl | 200 | html | 27296 |  |
| occ-pud-dockets | yes | curl | 200 | pdf | 195938 |  |
| occ-pud-reports | yes | curl | 200 | pdf | 1161279 |  |
| occ-weblink | NO | curl | 200 | html | 1910 | PERSON: If the real-Chrome route cannot run a search here, Baird opens the WebLink search in Chrome for one 2025 cause number and downloads one order PDF so the DocView address form is known; a case the run still cannot open is cited from the daily docket PDF and the utility's own copy of the filing. |
| odeq-air-pages | yes | curl | 200 | html | 386565 |  |
| odeq-onbase | yes | direct_post | 200 | json | 1152 |  |
| odeq-ppr | yes | insecure_tls | 200 | table | 551528 |  |
| oge-irp | yes | cf_impersonate, pdf_via_ladder | 200 | pdf | 92169 |  |
| ompa | yes | curl | 200 | html | 166000 |  |
| possible-updates-sheet | yes | gws-gem | 200 |  | 0 |  |
| pso-irp | yes | curl | 200 | pdf | 1809558 |  |
| sec-edgar | yes | sec_declared_ua | 200 | json | 36907 |  |
| spp-eras | yes | curl | 200 | html | 75551 |  |
| spp-gi-active | yes | curl | 200 | csv | 242345 |  |
| state-news | yes | cf_impersonate | 200 | html | 246658 |  |
| tenaska-kiamichi | yes | curl | 200 | html | 93349 |  |
| wfec | yes | curl | 200 | html | 442645 |  |

Samples are under the scope's work folder (`access/`), never committed. A NO with no PERSON line blocks the batch: fix the route (fetch.py --render, a harvester, the real document's address) and run the check again.
