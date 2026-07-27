# Confidence tiers

The rubric behind the green/yellow/red/blue cell colors in the deliverables
(`workbook_conventions.md`) and the `tier`/`independent` fields in staged
records (`staged_json_schema.md`).

## The rubric

For every material data point (status, capacity, technology, fuel, start year,
ownership, location), **try to find 2+ independent sources that agree** before
treating it as settled. Record the tier and the corroborating sources in the
record's `researcher_notes`.

| Tier | Color | Meaning |
|---|---|---|
| **High** | green | 2+ **independent** sources agree, or one primary/regulatory source (regulator registry, official filing, grid operator data) |
| **Medium** | yellow | a single solid source (operator filing, regulator, top-tier trade press), no contradictions |
| **Low** | red | a single weak/secondary source, or sources partially conflict |
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

**Single-source-that-confirms is fillable, not blank.** The 2+ target governs
when a value is *settled* (green); it does not mean a lone source is discarded.
If exactly one source can be found but its page verifiably contains the precise
data point (the plant/unit is named and the value or status is stated), fill
the cell at medium/yellow and keep hunting for the promoting second source.
"Prefer blank + a note" applies to a single weak source that does NOT actually
confirm the value.

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
