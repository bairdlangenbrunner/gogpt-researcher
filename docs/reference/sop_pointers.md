# SOP index and GEM source-document pointers

Where procedure lives in this repo, and the canonical GEM team documents it
was distilled from. Drive links need GEM Workspace access (read via
`gws-gem` / Drive MCP; this repo never modifies Drive files).

## SOPs in this repo (`docs/sops/`)

| SOP | file | run when |
|---|---|---|
| Update | `update.md` | working a country's existing plants/units in a quarterly pass |
| Discovery | `discovery.md` | hunting plants/units missing from the tracker |
| Triage | `triage.md` | turning a fresh scoped pull into a prioritized worklist (incl. the 2y/4y inferred-status sweep) |
| QC | `qc.md` | batch gate before deliverables; country close-out |

Reference docs supporting them all live in `docs/reference/`; country-specific
source knowledge in `docs/country_notes/`.

## Canonical GEM documents (Google Drive)

Distillations in this repo record the fetch date; when a distilled rule and
the live doc disagree, the live doc wins — update the distillation.

| document | type | Drive ID |
|---|---|---|
| GOGPT Editing Manual (March 2026) | Doc | `1CCtz2ITRpYkAaupEO7K-FuB3KXMv18mg_W6NpJNV9h8` |
| Guide to GEM Documents | Doc | `1wUg57Nw6Dum28wuMcw4LYnLu0OP6dU19k6mECjQTZjc` |
| Gas/oil power plant data sources — by country | Doc | `1J4JHu_Sy5190nMGCUqw8B_0UQwVgopcNo8UJTXE-cRw` |
| GEM Project Database Manual | Doc | `1mXWow4Q_7qU3s5KPHw34RvnZ_SjEhYNAB5ygS2oaNTs` |
| GOGPT Wiki Pages Manual | docx | `1kj9VKwASLicxiJhuV8soe4WhlLoC_DXy` |
| GOGPT Q2 2026 Update (assignments + checklists) | Sheet | `1kZ2jettyoWW7GaSbZvQyJ_gvfa6AzHsIPtrVcBxjdAI` |
| GEM trackers — possible updates (backlog) | Sheet | `1GAXwGdI0UFeW9mFSxJhhR6MRBW7VDtlWBqsooVZyUzs` |
| GEM data sources on energy projects | Doc | `1pBY78P2lEZb9cXnTXuwLl6JXKHwM5ZldX8UtFnTH9LI` |
| Country files folder | Drive folder | `1M1kpE8dLJapU-I653A2r1ZuzxwWHrkX-` |
| GEM National Reports folder | Drive folder | `1dedvh40sWY7N2VE2g1LVWhBYdLZU0Xsh` |
| Local terminology sheet | Sheet | `1nPNQJrJLRkDlFhPfMZMu6cuMEmSee4g3NQSqXnFShCw` |
| Intro to Gas and Oil Power Plants | docx | `12uC6OKq0_gx7zcg2Jgk7Cq5y28iSF2wK` |
| Immediate Ownership Guide | Doc | `1Eqat408hLd1o7OKBdNZoT5QUwYQ24mlUIn_-ubEBxeg` |
| Q2 2026 Kickoff deck | Slides | `1ogHGPaDdJfXlg9P2ViVe-zyRUGSf9GKWh4fZs8DUst4` |
| GOGPT project folder | Drive folder | `1UebqU-Rw70CvO5Vv81fPqovs5k827TRl` |
| Research Resources folder | Drive folder | `1mLM0yBlrLbhFBiAoImTAWPMAjtZ23jgr` |

## Which distillation came from which doc

| repo file | source document(s) |
|---|---|
| `lifecycle_rules.md`, `unit_conventions.md`, `controlled_vocab.md` | GOGPT Editing Manual |
| `datasource_conventions.md` | GEM Project Database Manual (+ Editing Manual datasource sections) |
| `wiki_pages.md` | GOGPT Wiki Pages Manual |
| `source_roster.md`, `docs/country_notes/*` | Gas/oil power plant data sources — by country |
| `campaigns/<quarter>/roster.csv` | the quarter's Update sheet (Researcher Country Assignments tab) |
