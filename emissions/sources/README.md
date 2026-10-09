# Sources: what was downloaded and accessed

A record of every file downloaded and every web resource accessed for the
emissions workstream, so any number in `findings/` or `coverage/` can be traced
back to the file it came from.

| Path | What | In git |
|---|---|---|
| `downloads.csv` | One row per file saved: date, publisher, title, URL, route, HTTP status, bytes, sha256, where the copy is in `raw/` | yes |
| `access_log.csv` | Every web request by session: fetches, searches, URLs in shell commands, Google Workspace reads (counted by kind only; no file IDs, thread IDs, or queries, which would name colleagues and internal files). Built by `build_access_log.py` from the session transcripts | yes |
| `sessions.txt` | The Claude Code sessions that worked on this workstream | yes |
| `get.py` | Download helper: fetches into `raw/`, hashes, appends to `downloads.csv`. Refuses banned sources and overwrites | yes |
| `build_access_log.py` | Rebuilds `access_log.csv` | yes |
| `raw/<country>/<publisher>/` | The downloaded files themselves: EIAs, datasets, saved pages | **no** (large third-party files) |

## Rules

- **Every download goes through `get.py`.** It writes the `downloads.csv` row
  at the time of download. Files fetched some other way (SharePoint REST, form
  POSTs, Drive) are saved in the scratchpad, then registered with
  `get.py --register`.
- **At the end of each session**, add its id to `sessions.txt` and rerun
  `build_access_log.py`.
- **Findings cite the URL, not the local copy.** `local_path` is for
  re-reading. The sha256 shows which version was read.
- **Private material is never kept in `raw/`.** This covers internal Drive
  docs, Gmail threads and anything confidential. It is recorded as an
  access only (`--no-keep`, `kind=private`), by id, with no content, subject
  line or figures. The repo is public.
- **Derived files are not registered:** pdftotext extracts, OCR pages,
  our own scripts and reports. Recreate them from the copy in `raw/`.
- **Session scratchpads are temporary.** Anything worth keeping goes into
  `raw/` through `get.py`.

## Backfill (2026-09-18)

- `downloads.csv` rows before 2026-09-18 were reconstructed from the session
  transcripts, since those files were saved to scratchpads before this
  register existed.
- `confidence` says how sure the URL is:
  - `high`: the URL is literally in the command that downloaded the file.
  - `medium`: rebuilt from shell variables or from the findings files.
  - `low`: a guess.
- Rows fetched through `get.py` leave `confidence` blank.
