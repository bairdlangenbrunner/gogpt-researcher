# Campaign q3-2026

The quarterly cycle is the organizing unit of GOGPT work: each quarter gets a
`campaigns/<quarter>/` dir whose `roster.csv` mirrors that quarter's
"Researcher Country Assignments" tab (see `docs/reference/sop_pointers.md` for
the Update sheet) plus per-country status counts from the scoped export.

Generate / refresh the roster (counts update, manual columns survive):

    cd scripts
    python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv
    python scope_filter.py
    python build_campaign_roster.py --campaign q3-2026

Manual columns (fill by hand as the quarter progresses):

| column | meaning |
|---|---|
| `assignee_role` | role only, never a personal name (public repo) |
| `assignment_status` | `unassigned` / `in-progress` / `close-out` / `done` |
| `packet_file` | the country's deliverable pair basename in `batches/<scope>/deliverables/` |
| `applied` | date the human finished applying the packet in the web UI |
| `notes` | one-liners; anything longer goes in `docs/country_notes/` |

Country close-out requires the GC/Country checklist + validation report
(QC SOP) before `assignment_status` moves to `done`.
