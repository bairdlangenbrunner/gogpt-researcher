# GOGPT review app

A small local page for deciding, one by one, on the edits a research batch proposes for the
Global Oil and Gas Plant Tracker. It reads the staged records in `batches/<scope>/staging/`,
shows each proposed cell edit next to the current value and its source links, and records one
call per edit: accept, hold, reject or suggest. Concerns, watch-list items and entity checks
take a call and a note too.

Nothing here writes the GEM database. There is no code path for it. Accepted edits go into
the actions workbook that is applied by hand in the GEM web form.

## Run it

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
- `--no-open`, `--no-build`, `--port`, `--data`.

Only one person at a time should run the server against a staging folder.

## What a decision does

Each call is appended to `review_log.jsonl` in the batch's staging folder (one JSON record
per line; an undo is another record). `review_decisions.json` next to it is a derived copy
with the latest record per edit. Both are committed with the batch, so the calls are part of
the audit trail and survive a rebuild: every staged record carries a stable `record_id`
(`assemble_state.py` writes it) and the log is keyed on it.

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

Back here:

```
python review_app/import_log.py ~/Downloads/review_log_us-md+us-ny_AL_20261003_0915_ET.jsonl --dry-run
python review_app/import_log.py ~/Downloads/review_log_us-md+us-ny_AL_20261003_0915_ET.jsonl
```

The same file can be published as a claude.ai artifact (Claude Code's Artifact tool, with the
`db`, `downloads` and `user` capabilities). Opened there, the page saves every call to the
artifact's own database as it is made (one document per reviewer under `logs/`, the whole log
in `records`), so nothing has to be sent back: read the document with the ArtifactData tool,
save it as a `.json` file and run `import_log.py` on it (it takes that document as well as a
`.jsonl`). The "download decisions" button then gives a `.json` backup of the same records.
A reviewer can only write to the database when they are invited by email as an editor and the
artifact is not also shared by link; otherwise the page says so in a banner, keeps the calls in
their browser, and they send the download instead.

The import appends the records to each batch's `review_log.jsonl` and regenerates
`review_decisions.json`, exactly as the server would have; then build with `--decisions` as
above. Importing the same file twice appends nothing. A record whose batch was rebuilt since
the page was made (its `record_id` is gone) stops the import before anything is written:
build a fresh page and ask for a fresh review. Two reviewers can each get a file; their calls
land in order of import and the latest per record wins, as with the server.

## On the page

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

## Files

- `review_data.py`: builds the dataset (one card per plant, one line per staged cell edit, one
  item per concern, watch-list entry or entity check).
- `store.py`: validates and appends decisions; the log is the truth, the derived file is a
  convenience copy.
- `server.py`: the loopback HTTP server (standard library only).
- `web/`: the page (`index.html`, `app.js`, `style.css`). No build step. `web/static_store.js`
  is the browser-side store the single-file page uses instead of the server.
- `build_static.py`: writes the single-file page for a colleague; `import_log.py` appends the
  file they send back to the batch logs.
- Tests: `python -m pytest tests/test_review_app.py`.
