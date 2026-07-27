# GOGPT Triage SOP

Last revised: 2026-07-27 (rev 1 — initial GOGPT adaptation from lng-terminals-researcher triage.md rev 2)

Operational rules for turning a fresh, scoped pull into a **prioritized worklist** for a country: running `worklist.py`, working the priority ladder, confirming or refuting the inferred-status (2y/4y) candidates it flags, and folding the "GEM trackers – possible updates" backlog into the same pass. This SOP expands the Update SOP's §3 pull-and-worklist step into full operational detail — run it as the first step of any country batch, before research begins in earnest.

The GOGPT Editing Manual is authoritative for the priority ladder and the inferred-status rule. This SOP is operational — it describes how to execute triage, citing the manual rather than restating it.

## §1 When to run this SOP

Trigger conditions:
- The start of every country batch (Update, Discovery, or a mixed batch) — triage always runs before the research pass, right after the fresh pull
- A roster row (`campaigns/<quarter>/roster.csv`) moves to `in progress`
- The user asks "what's next for `<country>`" or "what's overdue"
- A QC memo (`docs/sops/qc.md`) recommends a re-triage because worklist counts look stale

Triage is a per-country/per-batch step, not a standalone quarterly-planning exercise — quarterly composition (which countries get assigned this cycle) is a roster/PM decision upstream of this SOP.

## §2 What it produces

A prioritized worklist for the country, plus a set of inferred-status candidates confirmed or refuted for staging. This isn't a separate deliverable file — it's the input that determines which units the country's Update batch actually researches, and its inferred-status confirmations get staged directly into the `updates` lane alongside the rest of the batch's work. `worklist.py`'s raw output is a working artifact in `work/` (re-derivable, not committed); the confirmed/refuted inferred-status calls and their evidence are what carries forward into staging.

## §3 The priority ladder

Per the manual, review units within a country in this order:

1. **In-development units** — `announced`, `pre-construction`, `construction`. This is the manual's stated update focus and always comes first.
2. **Shelved review** — `shelved` and `shelved – inferred 2 y` units due for a fresh look.
3. **Units with planned retirement in the current year.**
4. **Other units with planned or actual retirement** (mothballed, retiring in a future year, or past retirements needing a datasource check).
5. **Operating spot-checks** — a lower-priority tier, worked only after 1–4 are exhausted or when the batch is explicitly scoped as an exhaustive/refresh pass rather than a priority-driven one.

`worklist.py --country <name>` outputs the country's units in this order; work top to bottom unless the user has scoped the batch narrower (e.g. "just the in-development units").

## §4 Running the worklist

```bash
python worklist.py --country <name>
```

Run this against the **GOGPT-scoped CSV** (`scope_filter.py` output, per update.md §3) — never the unfiltered export, which still contains coal (GCPT) and bioenergy (GBPT) rows. The script does the date-arithmetic flagging for §5 automatically; it does not confirm anything itself — that's the researcher's job.

## §5 The inferred-status sweep (2y / 4y)

`worklist.py` flags two kinds of candidates by pure date arithmetic against each in-development unit's most recent evidence date:

- **Shelved – inferred**: an `announced`/`pre-construction`/`construction` unit with no evidence of activity for **≥2 years** → candidate for `shelved – inferred 2 y`.
- **Cancelled – inferred**: the same disappearance test at **≥4 years** → candidate for `cancelled – inferred 4 y`.

A flag is a **candidate**, not a decision. For each one:

1. Search specifically for recent evidence — company disclosures, permit renewals, news, regulator filings — dated more recently than the unit's current last-seen date.
2. **Evidence found** → the clock resets. Do not change status. Update the Latest Activity field / last-seen date and its datasource so the next cycle's date arithmetic starts from the new date.
3. **No evidence found** after a genuine search → confirm the inferred status. Stage it in the `updates` lane with the paired year-field blanking (Start Year blanks for both `shelved` and `cancelled`, per update.md §4.2) and record the last-seen source/date in the Latest Activity field so a future cycle can re-run the clock from a documented baseline.
4. **Never leave a flagged candidate un-staged with a hedge.** Per update.md §4.1: if the search genuinely turns up nothing, that itself is the confirmation — stage the inferred status rather than punting it to a `qa` note. A `qa` record is for genuine ambiguity (conflicting evidence), not for "didn't get to it."

## §6 Working the "possible updates" backlog during country research

The "GEM trackers – possible updates" backlog is a running list the whole research team feeds. **Filter it to the country at batch start and fold its items into the worklist** — research them alongside the regular pass, not as an afterthought:

1. Filter the backlog sheet to the country being worked
2. Merge its items into the priority-ordered worklist from §3–§4 (a backlog item usually corresponds to a specific unit already in the ladder; if it references a unit not otherwise selected this batch, add it explicitly)
3. As each backlog item is resolved, mark it with initials/date/notes in "Update Notes" — this is a close-out requirement (`docs/sops/qc.md`), not optional cleanup

Doing this during the pass rather than after avoids reviewing the same plant twice — a key time-saver the manual calls out explicitly.

## §7 Workflow (linear)

1. Confirm country scope with the user (roster assignment, QC recommendation, or direct request)
2. Fresh pull chain: `python ../../gem-db-ops/gogpt/pull.py` → `python pull_gem_db.py --map-only` → `python scope_filter.py`
3. `python worklist.py --country <name>` → priority-ordered worklist + inferred-status flags (§3–§5)
4. Filter the "possible updates" backlog to the country and fold it in (§6)
5. Work each inferred-status flag: search, confirm or refute, stage the result if confirmed (§5)
6. Hand the finished worklist + confirmed inferred-status stages to the Update SOP for the research pass proper

Triage doesn't build a deliverable workbook itself — `build_review_package.py` runs later, once the Update SOP's research pass has staged the rest of the batch's edits.

## §8 Hard rules

- **Always work from the GOGPT-scoped CSV**, never the unfiltered export (§4).
- **Priority ladder order is fixed** — in-development, then shelved review, then current-year retirements, then other retirements, then operating spot-checks (§3).
- **An inferred-status flag is a candidate, not a decision** — confirm or refute with an active search before staging anything (§5).
- **No evidence found is itself the confirmation** — don't leave a flagged candidate unstaged with a hedge (§5.4).
- **Fold the possible-updates backlog in during the pass**, not after (§6).
- **Fresh pull at the start of every triage run** — worklist accuracy depends on current data.

## §9 Pause-and-ask triggers

Stop and consult the user when:

- The inferred-status sweep flags an unusually large number of candidates for one country (suggests either a genuine backlog or a data-quality issue worth discussing before bulk-confirming)
- A search for recent evidence turns up conflicting signals (one source suggests activity, another suggests abandonment) — this is a `qa` case, not a clean confirm or refute
- The "possible updates" backlog for the country is large enough to meaningfully change the batch's scope or size estimate

---

## Quick-reference card

| Priority tier | Statuses | Order |
|---|---|---|
| 1 | announced, pre-construction, construction | Always first |
| 2 | shelved, shelved – inferred 2 y | Second |
| 3 | planned retirement this year | Third |
| 4 | other mothballed / retiring | Fourth |
| 5 | operating | Spot-check only, lowest priority |

| Inferred flag | Trigger | Confirm action |
|---|---|---|
| Shelved – inferred 2 y | ≥2 y no activity evidence | Stage `shelved – inferred 2 y`, blank Start Year, log last-seen source |
| Cancelled – inferred 4 y | ≥4 y no activity evidence | Stage `cancelled – inferred 4 y`, blank Start Year, log last-seen source |
| Either, evidence found | Recent evidence located | No status change — update Latest Activity date, reset the clock |
