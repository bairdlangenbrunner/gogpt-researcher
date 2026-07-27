# Batches

One directory per research scope (a country or region slug, lowercase
hyphenated — `nigeria`, `us-gulf`), each with:

```
batches/<scope>/
  staging/        staged_<lane>.json files — the audit trail (committed);
                  lanes per docs/reference/staged_json_schema.md
  deliverables/   the actions/evidence pair built by build_review_package.py
                  (xlsx files are gitignored; evidence .md is committed)
  archive/        superseded staging/deliverables kept for history
  INDEX.md        one line per batch run: date, mode, what shipped, status
```

`batches/run_records/` holds cross-scope run logs (pull dates, row counts,
colmap drift notices) — one small `.md` per run.

Conventions:
- fresh pull + `scope_filter.py` + `pull_gem_db.py --map-only` at the START of
  every batch — never research against a stale CSV.
- `qc_checks.py --staged` must pass with zero errors before building
  deliverables; `recalc.py` runs on every built xlsx.
- deliverables are never overwritten — every rebuild gets a fresh timestamp.
- nothing here is ever auto-applied: the human applies edits by hand in the
  GEM project DB web UI and records the date in the campaign roster.
