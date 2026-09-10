# Global Oil and Gas Plant Tracker (GOGPT) — Research Pipeline

Tooling for Global Energy Monitor's [Global Oil and Gas Plant Tracker](https://globalenergymonitor.org/projects/global-oil-gas-plant-tracker),
an open-source dataset covering oil- and gas-fired power plants worldwide.
GEM publishes two releases a year (H1 in January, H2 in July); this repo holds
the scripts, templates, and reference data used to research a country each
cycle and compile the public deliverable.

## What this pipeline does

Each research cycle, a researcher works one country (or one US state) at a time
through a fixed sequence of sessions, recording findings in a per-country
**context card**. The scripts here slice the full database down to what a single
session needs, run cross-cutting quality checks, keep the context card in sync,
and finally compile the reviewed database into the multi-tab spreadsheet GEM
publishes.

```
data dump (GOGPTall*.xlsx)
        │
        ▼
 gogpt_csv_query.py ──► targeted slices, counts, missing-field & duplicate scans
        │                        │
        │                        ├─ gogpt_checks.py         (ownership / in-progress / duplicate / possible-updates)
        │                        └─ gogpt_verify_fields.py  (re-check card claims vs live data)
        ▼
 context card (.md)  ◄──► gogpt_card_update.py   (writes findings into sections, versions the card)
        │
        ▼
 gogpt_compile.py ──► "Global Oil and Gas Plant Tracker (GOGPT) compiled <date>.xlsx"
```

An interactive, self-contained researcher UI is bundled at
[`docs/GOGPT_Researcher_Launchpad_Q2_2026.html`](docs/GOGPT_Researcher_Launchpad_Q2_2026.html) —
open it in a browser to step through the sessions with copy-ready commands.

## Repository layout

```
gogpt-tracker/
├── README.md                     ← you are here
├── CLAUDE.md                     ← guidance for Claude Code
├── requirements.txt
├── scripts/
│   ├── gogpt_paths.py            ← central, env-overridable path resolution
│   ├── gogpt_csv_query.py        ← main entry point: slice + scan the database
│   ├── gogpt_checks.py           ← ownership / in-progress / duplicate / possible-updates
│   ├── gogpt_verify_fields.py    ← re-verify card field claims vs live data
│   ├── gogpt_card_update.py      ← write findings into the context card, version it
│   └── gogpt_compile.py          ← build the published multi-tab deliverable
├── templates/
│   └── COUNTRY_CONTEXT_CARD_TEMPLATE.md
├── assets/
│   └── H2_units_to_exclude.xlsx  ← units excluded at compile time (H2 conversions)
├── data/                         ← database dumps + possible-updates (see data/README.md)
│   ├── GOGPTall20260618T164506sheet.xlsx
│   ├── GEM_trackers__possible_updates__gas_oil_plants1.csv
│   └── gasDB_unitsHistory1.csv
├── docs/
│   └── GOGPT_Researcher_Launchpad_Q2_2026.html
├── output/                       ← compiled files + updated cards land here
└── uploads/                      ← drop freshly-exported dumps / cards here
```

## Setup

Requires Python 3.9+.

```bash
pip install -r requirements.txt
# or, on a managed system:
pip install -r requirements.txt --break-system-packages
```

No install step for the scripts themselves — run them from `scripts/`.

## Quick start

```bash
cd scripts

# 1. Unit counts for a country (auto-detects the newest dump in data/)
python3 gogpt_csv_query.py --country "Japan" --counts-only

# 2. The in-development units you'll research this session
python3 gogpt_csv_query.py --country "Japan" --status in-development

# 3. Cross-cutting scans
python3 gogpt_csv_query.py --country "Japan" --status operating --ownership-scan
python3 gogpt_csv_query.py --country "Japan" --duplicate-scan
python3 gogpt_csv_query.py --country "Japan" --possible-updates

# 4. Write a finding into the context card (section 6b = in-development)
python3 gogpt_card_update.py --country "Japan" --section 6b --session 3 \
        --content "🔄 UPDATE — ..."

# 5. Compile the reviewed database into the published spreadsheet
#    (compile takes a raw CSV export of the database)
python3 gogpt_compile.py --input ../data/<raw_export>.csv
```

US-state work passes `--state` alongside `--country "United States"`:

```bash
python3 gogpt_csv_query.py --country "United States" --state "Arizona" --counts-only
```

## Paths & portability

All directory locations resolve through `scripts/gogpt_paths.py`, in this order:

1. an environment variable, if set;
2. the repo-relative default (`data/`, `assets/`, `output/`, …);
3. a legacy `/mnt/...` fallback (so the scripts also run unchanged in the
   original hosted environment).

| Variable            | Purpose                                          | Default        |
|---------------------|--------------------------------------------------|----------------|
| `GOGPT_DATA_DIR`    | database dumps + possible-updates CSV            | `./data`       |
| `GOGPT_ASSETS_DIR`  | bundled reference lists (H2 exclusions)          | `./assets`     |
| `GOGPT_OUTPUT_DIR`  | compiled files + updated cards                   | `./output`     |
| `GOGPT_WORK_DIR`    | persistent working copy of the context card      | `./.gogpt_work`|
| `GOGPT_UPLOADS_DIR` | freshly-uploaded dumps / cards                    | `./uploads`    |

Example — point at data living elsewhere:

```bash
GOGPT_DATA_DIR=~/gem/dumps python3 scripts/gogpt_csv_query.py --country "Japan" --counts-only
```

## The research cycle

Sessions mirror the status groups in the tracker and the rows in the context
card's session log:

| Session | Focus                                   | Card section |
|---------|-----------------------------------------|--------------|
| 0–1     | Setup, unit counts, country context     | 1–4          |
| 2       | New proposals                           | 6a           |
| 2b/2c   | US-state research / EIP-SC matching     | 6a           |
| 3       | In-development units (+ turbine table)  | 6b           |
| 4       | Shelved & cancelled units               | 6c           |
| 5       | Operating units                         | 6d           |
| 6       | Retired & mothballed units              | 6e           |
| 7       | Export QC report                        | 5            |
| 8       | Wrap-up                                 | 7            |

`gogpt_card_update.py` marks each session done in the log and writes findings
between the `<!-- SECTION:X:START/END -->` markers in the template.

## Methodology (summary)

The GOGPT tracks all oil- and gas-fired power plants generating electricity in
any setting — peaking, base load, captive industrial, and co-generation. It
includes units of **50 MW or more** (**20 MW or more in the EU and UK**). For
combined-cycle units the threshold applies to the whole set, not each component;
for internal-combustion or multi-engine sets it applies to the total. Gas
boilers producing only district or industrial heat are excluded.

Status vocabulary: *announced, pre-construction, construction, shelved,
cancelled, operating, mothballed, retired.* Full definitions live in
[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

The compile step applies the capacity thresholds, drops units retired before
2020, removes bundled H2-conversion units, and splits announced "IRP" units into
their own tab.

## License / attribution

Data and methodology © Global Energy Monitor, published under GEM's open-data
terms. See the project page for citation guidance:
<https://globalenergymonitor.org/projects/global-oil-gas-plant-tracker>.
