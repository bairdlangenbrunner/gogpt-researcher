# GOGPT review app

A page for deciding, one by one, on the edits a research batch proposes for the Global Oil and Gas Plant Tracker. It reads the staged records in `batches/<scope>/staging/`, shows each proposed cell edit next to the current value and its source links, and records one call per edit: accept, hold, reject or suggest. Once an edit has an accept, hold or reject, a note box appears beside the buttons for an optional why that goes into the log with the call (a suggestion takes its note in its own form). Concerns, watch-list items and entity checks take a call and a note too.

Nothing here writes the GEM database. There is no code path for it. Accepted edits go into the actions workbook that is applied by hand in the GEM web form.

**The reviewers work from the claude.ai artifact pages** (the table under "Sharing as a claude.ai artifact"); the loopback server below is for Baird's own pass over a batch. Both record decisions the same way: the store spreadsheet first, the staging dir's log second (next section). This is the same model as `../pipelines-researcher/review_app/`, so the two review apps behave alike.

## Run it locally

From the repo root:

```
python review_app/server.py --scope us-md --scope us-ny
```

That rebuilds the dataset from the staging folders (`work/review_data.json`, not tracked),
starts a loopback-only server on port 8767 and opens the page. Options:

- `--scope <name>` (repeatable): a batch under `batches/`. `--dirs <path> ...` names staging
  folders directly.
- `--reviewer "Name"`: who is deciding. Default: the git user name. Calls are recorded by
  initials.
- `--export-csv <path>`: the scoped export the current Data Source cells are read from.
  Default: the batch's own, then the standard pull location.
- `--reviewer-email <addr>`: the address written on the store rows. Default: the account behind `gws-gem-write` (`ledger.whoami`).
- `--no-store`: skip the store spreadsheet and write only the staging dir's log. For development and tests only; the server warns on every start, and nothing written this way reaches the store.
- `--no-open`, `--no-build`, `--port`, `--data`.

Only one person at a time should run the server against a staging folder.

## What a decision does

**One ledger.** Every decision, whichever door it comes through, is appended first to the `log` tab of the store spreadsheet ("gogpt reviewer decision store", https://docs.google.com/spreadsheets/d/157PtaKfUK3k-pxE1J1IPAJ7ng-GCcCj_vAKMCrV1frg/edit, in the shared-drive folder "Reviewer apps"; its id is `review_app/google.json: store_sheet_id`) and second to `review_log.jsonl` in the batch's staging folder. `review_app/ledger.py` writes the row (21 columns: time, reviewer address, record kind, plant, record id, column, decision or call, note, flag, batch, snapshot, the key, a uuid `id`, scope, and the whole record as JSON) with `gws-gem-write`, reads the id cells back to confirm, and only then writes the sidecar. If the store cannot be written the decision is refused (the server answers 502 "decision store unreachable, nothing saved"; `import_log.py` exits) and nothing is written anywhere. There is no offline mode.

The doors: the loopback server (origin `local`), the artifact pages through `import_log.py` (origin `artifact`), and a Claude chat (origin `chat`). The store is the single source of truth; the sidecars are its committed mirror. `python review_app/pull.py` copies store rows the sidecars do not yet have (by `id`) into the right staging dir, so a clone that is behind catches up without touching the store; `python review_app/ledger.py status` says whether a store is configured, which address writes it, and how many rows it holds. A sidecar written before the ledger existed holds records with no `id`; `python review_app/ledger.py backfill batches/<scope>/staging --reviewer XX=EMAIL` appends them to the store (origin `chat`, each under its reviewer's address, keeping its own time) and rewrites the sidecar with the stamped records, the one case where a sidecar is rewritten rather than appended to (`--dry-run` lists them first). Appending to the `log` tab is a standing authorization (Baird 2026-10-08, recorded in CLAUDE.md); no other Google write is.

In the sidecars the reviewer is their initials (`store.initials`: baird.langenbrunner@... becomes BL); the store keeps the address. `review_log.jsonl` is one JSON record per line (an undo is another record); `review_decisions.json` next to it is a derived copy with the latest record per edit. Both are committed with the batch, so the calls are part of the audit trail and survive a rebuild: every staged record carries a stable `record_id` (`assemble_state.py` writes it) and the log is keyed on it.

To build the deliverable from the calls:

```
cd scripts
python build_review_package.py --staging-dir ../batches/us-md/staging --scope us-md --mode update --decisions
```

With `--decisions`, only accepted edits go into the actions workbook. Held, rejected,
suggested and undecided edits are listed at the top of the evidence file with the reviewer's
note. Items keep their call in the evidence file. Without the flag the build ignores the log
and says so.

## Sharing with a colleague (one html file)

A reviewer who does not run the repo gets the same page as a single file. From the repo root:

```
python review_app/build_static.py --scope us-md --scope us-ny --reviewer "Amalia Llano" --export-csv scripts/gem_export_gogpt_scoped.csv
```

That writes `work/gogpt_review_us-md+us-ny_<stamp>_ET.html` (a few MB; the dataset, the calls
already in the logs, and the page are all inside it; `work/` is not tracked). Send the file.
The reviewer opens it from disk in any browser, works the queue the same way, and their calls
stay in that browser (localStorage, so the page can be closed and reopened). When done they
press "download decisions" and send back the `review_log_..._ET.jsonl` it saves.

A rebuilt page (after the batch changes) picks up the calls the same browser made on an earlier
build of the same folders, for every record the rebuild still has. Calls on records that were
dropped are left behind.

Back here (`--reviewer` is the address written on their store rows; the page only knows initials):

```
python review_app/import_log.py ~/Downloads/review_log_us-md+us-ny_AL_20261003_0915_ET.jsonl --reviewer amalia.llano@globalenergymonitor.org --dry-run
python review_app/import_log.py ~/Downloads/review_log_us-md+us-ny_AL_20261003_0915_ET.jsonl --reviewer amalia.llano@globalenergymonitor.org
```

## Sharing as a claude.ai artifact (the current way; decisions save themselves)

The same file is published as a claude.ai artifact with Claude Code's Artifact tool, capabilities
`{db: {}, user: {scopes: ["profile"]}, downloads: true}`. Opened there, the page saves every call
to the artifact's own database as it is made (collection `logs`, one document per viewer named by
their viewer id, the whole log in `records`), so nothing has to be sent back. The "download
decisions" button is then only a backup (a `.json` of the same records).

Rules that came out of the first round (2026-10-05):

- **Publish from the work profile (`~/.claude-gem`), never the personal one.** The database and
  the download button only work for members of the publishing account's organization. The first
  page (2026-10-02) went out from the personal profile; Amalia Llano's accepts could not save
  ("the page could not save to the artifact (invalid_argument)") and her download was refused,
  so her two calls were copied into the log from a screenshot.
- **Share by email, as an editor**, from the page's Share menu. A viewer who can only view, or
  who opens a link share, is told in the banner that the page cannot save for them; their calls
  stay in their browser until they download them.
- Filters survive a reload (2026-10-08). The route (filters plus the open plant) is kept in this browser's localStorage per scope (`review-route:<scope>`) and restored on load when the URL carries no route, because a published artifact's frame does not keep the hash. A link with a route in it still wins. Takes effect on the next build and publish.
- The page is a snapshot. Calls already in the batch logs are laid over it at build time; a
  rebuild gets a fresh stamp and a publish of the new file to the same URL keeps the link.
- A "push to log" button (shown once the page is synced; its info box links to the store spreadsheet) saves the viewer's calls and writes a request document to the `requests` collection (`requests/<viewer>~push`). It never writes the spreadsheet itself: a Claude Code session on the work profile then runs the sync-back recipe below, which appends the viewer's calls to the store `log` tab and the batch `review_log.jsonl`. The tab counts show "n shown" when a filter hides some of them.
- Every call the page records carries a uuid `id` (`static_store.js`), the same `id` the store row and the sidecar record keep, so a page rebuilt from the logs recognizes its own calls and an import never appends one twice. Calls made on pages built before 2026-10-08 have no `id`; `import_log.py` derives one from the record's contents, the same every time, so those files import and re-import safely too.
- The GEM database is never touched. The artifact holds only the proposed edits and the calls.

A scope that also ran a discovery pass keeps those records in `batches/<scope>/staging-discovery/`
(docs/workflows.md). `--scope` reads only `staging/`, so name every folder with `--dirs` to put the
update edits and the discovery candidates on one page:

```
python review_app/build_static.py --dirs batches/us-md/staging batches/us-ny/staging batches/us-md/staging-discovery batches/us-ny/staging-discovery --reviewer "Amalia Llano" --export-csv scripts/gem_export_gogpt_scoped.csv --out work/gogpt_review_us-md+us-ny_<stamp>_ET.html
```

A new plant is one call for the plant and every unit row nested under it (the build script keys
the decision on the plant record), so the page shows the unit rows under the plant fields on one
line. The import then writes the calls to the `review_log.jsonl` of whichever folder the record
came from.

Live pages (the index is `artifacts.json`; one interface in `web/`, one page per reviewer, titled
`GOGPT reviewer - <first name>`):

| page | reviewer | url | folders |
|---|---|---|---|
| GOGPT reviewer - Amalia | Amalia Llano | https://claude.ai/artifact/7bnX9RMity3Yw5mdaojNaL | us-md and us-ny, update and discovery |
| GOGPT reviewer - Dan | Dan O'Beirne | https://claude.ai/artifact/3YnJ2C36PwrTJ8qYgUxbuW | germany and germany-permits |

**Keeping every page identical in interface.** The interface lives only in `web/` and
`build_static.py`; a page differs from the others only in its data, reviewer and title. After ANY
change there: `python review_app/build_all.py`, then publish each printed file to its url (work
profile, capabilities carried forward). Never edit a published page by hand; an edit made there
is lost at the next publish. To add a page (Nagwa, Warda), add an entry to `artifacts.json`
(name, title, reviewer, dirs, and the url once published) and run `build_all.py --only <name>`.

Bringing the calls back into the repo, from a Claude Code session on the work profile:

1. ArtifactData, action `list`, collection `logs`, with `out_dir` set to a scratch folder: one
   `.json` file per reviewer lands in `<out_dir>/logs/`.
2. `python review_app/import_log.py <out_dir>/logs/*.json --reviewer EMAIL --dry-run`, then without `--dry-run` (one `--reviewer` per person, `XX=EMAIL` when a file holds several; the page has no addresses). It reads that document shape as well as a `.jsonl`, and goes through the ledger like every other decision path: store `log` tab first, then each batch's `review_log.jsonl`.
3. `python scripts/build_review_package.py ... --decisions`.

Then rebuild the page and publish it to the same URL so the reviewer sees the calls as recorded.

The import appends the records to each batch's `review_log.jsonl` and regenerates `review_decisions.json`, exactly as the server would have; then build with `--decisions` as above. Importing the same file twice appends nothing (the `id` is already in the log). A record whose batch was rebuilt since the page was made (its `record_id` is gone) stops the import before anything is written: build a fresh page and ask for a fresh review. A page record older than a decision already in the log on the same edit is reported as superseded and skipped. Two reviewers can each have a page; their calls land in time order and the latest per record wins, as with the server.

## On the page

- Top: pick a country first (United States, Germany). The state box appears only after a country with
  more than one state is picked. Country batches such as Germany have no states.
- Left: the plants with something to decide. The badge counts open changes.
- Card: the plant's changes, grouped by unit. "Now" is the cell today, "proposed" is what the
  researcher wants. A proposed Data Source link is added next to the links already in the cell;
  the manual's merge rule, so nothing is ever replaced.
- Major changes move a value (fill a blank, change or clear a value, a plant-wide field, a new
  row). Minor changes leave the value as it is and only add a source link because the value
  was checked again and stands. Minor changes have their own tab and an accept-all button.
- Color is the confidence rating from the batch: green is one fully checked source (a status
  change needs two independent publishers), yellow is one source or a partial match, red is
  weak. Green defaults to accept, the rest to hold.
- Keys: `j` / `k` next and previous change, `J` / `K` next and previous plant, `a` / `h` / `r`
  accept, hold, reject, `s` suggest, `u` undo, `o` open the first source link, `i` items,
  `/` search, `?` help. The "how to" button explains the page in plain language.
- Checklist view (left pane): the nine QC/Country checklist groups, each a filter; every change
  and item carries a "checklist N" chip. Group 9 opens the close-out panel: a draft close-out
  note to copy, the sheets and docs to update with links, and on a United States page the IRP
  boxes to tick (row 37). "Ask the PM" is a checkbox beside any call, with its own filter.
- Watch items take one of four calls: incorporate into database, hold, send to possible updates,
  remove from watchlist. Remove needs a note.
- IRP chip (United States only): the finding comes from a utility integrated resource plan. The
  chip says whether the unit's IRP box in the database is already ticked; "IRP: tick the box"
  means it is not.

## Files

- `review_data.py`: builds the dataset (one card per plant, one line per staged cell edit, one
  item per concern, watch-list entry or entity check).
- **The app itself lives in the sibling repo `../gem-review-app`** (shared with pipelines-researcher since 2026-10-08; `GEM_REVIEW_APP` in the environment overrides the location). Its `review_core/` holds the page (`web/index.html`, `app.js`, `style.css`), the browser-side stores (`web/static_store.js` for the single-file and artifact page, `web/gas.js`), the generic decision log, the loopback server and the single-file builder; `trackers/gogpt/` holds the GOGPT config (kinds, calls, note rules, the ask-the-PM flag) and the page extension (`web/ext.js`, `web/ext.css`: checklist tabs, watch items, IRP chips). Any interface change is made there, never here, and reaches every tracker's pages. The files below are what is GOGPT's own.
- `store.py`: the shared store bound to the GOGPT config; validates decisions and writes the staging dir sidecars (`review_log.jsonl`, the derived `review_decisions.json`), through a ledger sink when one is given.
- `ledger.py`: the store spreadsheet door (row shape, verified append, the `Ledger` sink every decision path uses, `status`); `pull.py`: the `gws` wrapper, `google.json` config, and the store-to-sidecar mirror; `google.json`: the shared-drive folder and store sheet ids.
- `server.py`: the shared loopback HTTP server (standard library only) bound to the GOGPT store; it serves the shared page under `/`, the core files under `/core/` and the GOGPT extension under `/tracker/`.
- `build_static.py`: writes the single-file page for a colleague through the shared builder (the dataset rides in one gzip block with a packed key index; the store link goes into the page as `ledger_url`); `import_log.py` brings their calls into the store and the batch logs.
- `checklist.py`: the nine checklist groups, the row mapping and the tagging function shared by
  the page, the assembler and the workbook build.
- `build_all.py` and `artifacts.json`: the index of published pages and the one command that
  rebuilds every one of them after an interface change.
- Tests: `python -m pytest tests/test_review_app.py tests/test_review_ledger.py tests/test_review_pull.py tests/test_checklist.py tests/test_irp_sheet.py` (a fake `gws` stands in for the sheet; nothing in the tests touches Google).
