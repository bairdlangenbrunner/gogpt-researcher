# Confidence tiers

The rubric behind the green/yellow/red/blue cell colors in the deliverables
(`workbook_conventions.md`) and the `tier`/`independent` fields in staged
records (`staged_json_schema.md`).

## The rubric

**One fully validated ref is sufficient; a second independent source is
preferred but never required** (Baird 2026-10-02, adopting the pipelines-researcher ruling of 2026-09-30). For every material
data point (status, capacity, technology, fuel, start year, ownership,
location), a single ref that passes every check below closes it at
high/green. Take a second independent source when it is cheap (document
already open, one quick search) and record it via the `independent` flag, but
never hold a unit open or spend another search for it. Record the tier and
any corroborating sources in the record's `researcher_notes`.

**Validation checklist** (all four must pass for a ref to count as fully
validated):

1. It clears `url_verifier.py`: the URL loads, is not gem.wiki /
   globalenergymonitor.org / a banned domain after redirects, and is not a
   search, index, or homepage.
2. It NAMES this plant/unit.
3. It STATES the value (within rounding; status-by-inference counts, see
   Nuances).
4. It is not a GEM-derived republisher.

**Exception: a STATUS CHANGE is green only on 2+ independent publishers; a
single-source status change is medium/yellow.** Inferred statuses are
unchanged (no URL by design).

| Tier | Color | Meaning |
|---|---|---|
| **High** | green | one ref that passes every validation check; or, for a status change, 2+ **independent** publishers agree |
| **Medium** | yellow | a single-source status change; or a ref that validates only partially (names the plant but the value is implied, or sources contested) |
| **Low** | red | a single ref that does NOT fully validate (weak, doesn't name the plant, value not on the page), or sources partially conflict |
| **Inferred** | (blank + note) | no verifiable source — e.g. a shelved/cancelled-inferred status from the 2y/4y disappearance test; never fabricate a URL for an inference |
| **Re-verified** | blue | value unchanged from the existing GEM value but checked again this batch |

**Independent** = genuinely separate origins (an operator press release AND a
regulator filing AND a trade-press article reporting independently). **NOT
independent:** the same wire story republished by several outlets; multiple
pages tracing to one original; mirrors/host-copies of one document; anything
citing GEM or gem.wiki (circular — banned outright, see `source_roster.md`).
When sources conflict, prefer the one higher in the source roster, note the
conflict, and lower the tier.

## Nuances that prevent common mistakes

**Partial validation is yellow; no confirmation is red/blank.** A fully
validated single ref is green (see the rubric). A single ref that only
PARTIALLY validates (the plant is named but the value is merely implied, or
the page is a weak secondary) is yellow; keep hunting if it is cheap. A ref
that confirms nothing (doesn't name the plant, value not on the page) is red:
prefer blank + a note and a `qa` record.

**Status is inferred from context — don't require the literal word.** A source
confirms a status when its prose *entails* it: a commissioning ceremony, a
generation/dispatch figure, or "supplies power to the grid since March"
confirms `operating` even if the word never appears; a groundbreaking or EPC
award confirms `construction`. Make that inference yourself — `url_verifier`'s
"value not found" on a status token is a screen artifact, not a verdict; the
researcher decides and says why in `researcher_notes`.

**Match names fuzzily; read the full page.** Plant names transliterate
inconsistently (and units get renumbered); don't reject a source over a
one-letter spelling delta. Never conclude "the page doesn't support the value"
from a truncated or blocked fetch (cookie wall, archive interstitial) — pull
the full text first. Asserting a negative from a partial fetch is a
standing-rule error.

**Harvest the existing Data Source cells first.** Before declaring a value
un-corroborable, mine the unit's existing Data Source columns in the export —
GOGPT datasources are never deleted, so the trail of prior citations is intact.
Prior citations are candidate sources, not auto-valid: they still go through
`url_verifier.py`, and a dead link gets logged (never removed — see
`datasource_conventions.md`).

**Inferred statuses carry no ref by design.** A `shelved – inferred` /
`cancelled – inferred` proposal rests on the documented ABSENCE of evidence
(the 2y/4y tests in `lifecycle_rules.md`). Its staged record documents the
search performed (where you looked, newest evidence found and its date) in
`researcher_notes` instead of `refs` — and a single fresh piece of activity
evidence refutes the inference entirely.
