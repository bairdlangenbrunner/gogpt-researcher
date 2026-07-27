# GOGPT QC SOP

Last revised: 2026-07-27 (rev 1 — initial GOGPT adaptation from lng-terminals-researcher qc.md rev 1)

Operational rules for the quality-control gate: the mechanical checks that must pass before a batch's deliverables are built, plus the country close-out process once the human has applied a batch. Where Triage looks forward ("what should this batch research?"), QC looks backward — it confirms the staged edits are internally consistent, the citations hold up, and the country's checklist and validation report are clean before the country is marked done.

The GOGPT Editing Manual is authoritative for the close-out checklist items and the validation-report expectations. This SOP is operational — it describes how to execute the QC pass, citing the manual rather than restating it.

## §1 When to run this SOP

Trigger conditions:
- **Before every `build_review_package.py` run** — the batch QC gate (§3–§5) is mandatory, not optional, for every batch regardless of size
- **At the end of a country's research cycle**, before the roster row moves to `done` — the close-out pass (§6)
- After the human reports having applied a batch, to confirm the country's validation report is clean
- The user phrases: "run qc", "check before building", "close out `<country>`"

Unlike Triage, QC doesn't gate the start of a batch — it gates the **end** of one, twice: once mechanically before the deliverable is built, and once procedurally at country close-out.

## §2 What it produces

Two distinct outputs depending on which trigger fired:

1. **Batch QC gate** (§3–§5): no separate file — a pass/fail confirmation that the staging dir is clean, reported inline before `build_review_package.py` runs. A failure blocks the build until fixed.
2. **Country close-out** (§6): the completed GC/Country Checklist, a clean GOGPT Validation Report for the country, and the roster row's close-out fields (notes, next-cycle time estimate) filled in.

QC never writes to the live GEM database and never stages edits of its own — a QC failure routes back to the researcher to fix within the batch already in progress, not to a separate follow-up batch (contrast with the family's QC-detects/Update-fixes split for periodic audits — GOGPT's QC is an in-batch gate, tighter-scoped than that).

## §3 Mechanical validation — `qc_checks.py`

Run against the batch's staging dir before every build:

```bash
python qc_checks.py
```

Checks, per the manual:
- **Capacity thresholds** — ≥50 MW nameplate (generating MWe only), with the EU/UK <20 MW per-unit exception
- **Status–year consistency** — Start Year blank on `shelved`/`cancelled` (and their inferred variants); no Retired Year on `mothballed`; Planned checkbox set while a start/retire year is projected, cleared once actual
- **Controlled vocabulary** — Technology (CC, GT, AGT, ST, IC, ICCC, ISCC, AFC) and Fuel category/detail values inside the manual's enums; hydrogen fields untouched (do-not-research)
- **Ownership shares** — stakes ≥5% only (smaller aggregate as "small shareholder(s)"), shares sum sensibly, four-largest-plus-other structure, sole owner explicit 100%, no national government listed directly as an owner

Fix every failure before building. A deliberate exception (e.g. a genuinely ambiguous ownership share) gets a `qa` record explaining it — `qc_checks.py` failing silently or being skipped is never acceptable.

## §4 URL re-verification

Every URL in the staging dir passes `url_verifier.py` (update.md §7.1) — including URLs that were already verified earlier in the same batch, since sources can go dead between staging and build. Re-verify pre-existing URLs on any row the batch touched, not only newly-added ones. Bot-blocked URLs (401/403/429, interstitials) fall back to the newest Wayback snapshot for the content check per update.md §7.1 — a pass keeps the live URL citable; only a hard 404/410/DNS failure, or a live page missing the cited value, is a genuine failure.

## §5 Reference-merge audit

Before building, spot-check that every reference-field edit in the batch followed merge semantics (update.md §7.3):

- New value = surviving existing URLs (original order) + new URLs — never a wholesale replacement of a working citation with the agent's own find
- Any dropped URL is declared in the staged record's `dropped_urls_dead` key, and was proven dead (not merely re-verified as inconvenient)
- No orphan citations — every reference has a paired data value (Rule F)
- URLs appear only in reference/datasource columns, never embedded in name/value/notes fields

A reference-merge violation is a build blocker, same as a `qc_checks.py` failure.

## §6 Country close-out

Once the human has applied the batch (or at the natural end of the country's research cycle), confirm every item before the roster row moves to `done`:

- Every worklist unit (from the Triage SOP, `docs/sops/triage.md`) has a Record of Full Updates entry — `updated`, `no changes`, or `in progress` if genuinely unfinished
- Assigned Comments in the database are reviewed and resolved
- The "GEM trackers – possible updates" backlog items for the country are cleared — researched and annotated with initials/date/notes (`docs/sops/triage.md` §6)
- Country Tips are updated with anything learned this cycle; durable findings mirrored into `docs/country_notes/<country>.md`
- The **GC/Country Checklist** is completed
- The **GOGPT Validation Report** is run for the country (Projects tab → country search → "GOGPT Validation Report" tab) and errors resolved. **Exception**: validation errors on project-level fields for co-located coal/gas plants (e.g. missing datasource for shared location or owner) or unit-level fields for coal-to-gas-conversion units (e.g. missing datasource for CCS) are **optional / low priority** — the manual explicitly deprioritizes these
- A time estimate for the next cycle is logged in the roster's notes (`campaigns/<quarter>/roster.csv`)
- The roster row moves to `done`; the PM reviews and may flag fields needing revisit — process flags as a small follow-up batch

## §7 Workflow (linear)

**Batch gate** (runs inside every batch, right before build):
1. `python qc_checks.py` on the staging dir (§3) — fix every failure
2. `python url_verifier.py` re-run on all staged + touched pre-existing URLs (§4)
3. Manual reference-merge spot-check on any reference-field edits this batch made (§5)
4. `python build_review_package.py` → deliverables
5. `python recalc.py` → confirm zero formula errors

**Country close-out** (runs once, at the end of the country's cycle):
1. Confirm every worklist unit has a Record of Full Updates entry
2. Review and resolve Assigned Comments
3. Confirm the possible-updates backlog is cleared for the country
4. Update Country Tips / `docs/country_notes/<country>.md`
5. Complete the GC/Country Checklist
6. Run the GOGPT Validation Report for the country; resolve errors (co-located/coal-conversion exceptions per §6)
7. Log the next-cycle time estimate in the roster
8. Move the roster row to `done`; hand off for PM review

## §8 Hard rules

- **`qc_checks.py` passes before every build** — no exceptions, no silent skips (§3).
- **Every URL re-verified before build**, including previously-verified ones (§4).
- **Reference edits merge, never replace; no orphan citations; URLs only in reference columns** (§5).
- **Co-located coal/gas and coal-conversion validation-error exceptions are the ONLY validation errors allowed to ship unresolved** — everything else blocks close-out (§6).
- **QC never writes to the live database and never stages edits** — failures route back into the batch already in progress.
- **The roster row only moves to `done` after every §6 item is confirmed.**

## §9 Escalation thresholds / pause-and-ask

Stop and consult the user when:

- `qc_checks.py` fails on a large fraction of the staging dir (suggests a systematic staging error, not isolated mistakes — worth finding the root cause before re-running the fix loop row by row)
- URL re-verification shows a country's citation base substantially decayed since the batch started (many pre-existing URLs on touched rows now dead) — may warrant broadening the batch rather than patching individual cells
- The GOGPT Validation Report shows errors outside the co-located/coal-conversion exception that don't resolve with a straightforward fix — may indicate a schema or methodology misunderstanding
- A reference-merge audit finds a dropped URL that wasn't actually dead — treat as a process error, not a one-off fix, and check the rest of the batch for the same mistake

---

## Quick-reference card

| Check | Tool | Blocks build? |
|---|---|---|
| Capacity / status-year / vocab / ownership | `qc_checks.py` | Yes |
| URL liveness (staged + touched pre-existing) | `url_verifier.py` | Yes |
| Reference-merge semantics, no orphan citations | Manual spot-check | Yes |

| Close-out item | Where |
|---|---|
| Record of Full Updates | Per-unit, in the actions workbook / DB |
| Possible-updates backlog | Filtered sheet, initials/date/notes |
| GC/Country Checklist | GEM roster spreadsheet |
| GOGPT Validation Report | DB Projects tab, per country |
| Next-cycle time estimate | `campaigns/<quarter>/roster.csv` |
