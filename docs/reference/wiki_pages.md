# GOGPT Wiki Pages: Structure, Auto-Generation & Editing Rules

Distilled from the GOGPT Wiki Pages Manual (Google Doc, fetched 2026-07-27)

This covers how gem.wiki pages relate to the GEM database, what auto-populates vs.
what's hand-edited, and the style rules that apply to the one editable section. It's
context for understanding wiki pages a researcher (human or this agent) might encounter
— not a workflow this agent performs. **This agent never edits wiki pages and never
cites gem.wiki (or GEM-derived republishers) as a source** — see `docs/sops/update.md`.
Wiki content is a downstream copy of the DB, never an input to it.

## What a wiki page is

- Wiki pages **duplicate information already in the tracker/DB** — descriptive details
  and references — for public/human-readable consumption on gem.wiki.
- **Auto-generation**:
  - When work starts on a new country, pages are bulk-generated programmatically (Python).
  - Since then, adding a new plant to the tracker **auto-creates** its wiki page.
  - Adding new units to an *existing* plant (e.g. new gas units at an existing coal
    plant) does not create a new page — the existing page just needs its content updated
    to reflect the addition.
- **Human researchers are not required to update wiki pages.** Some choose to, because
  it makes it easier to track a plant/unit's status across research cycles — especially
  useful for coal-to-gas conversions. This is optional, not a standard task step.

## Page sections (baseline, gas/oil plants)

Standard sections every gas plant page includes, in order (`==` is the wikitext heading
markup):

1. Intro sentence (unheaded)
2. `==Location==`
3. `==Project Details==`
4. `==Ownership Tree==`
5. `==Articles and Resources==`

- The main *additional* section commonly added beyond this baseline is **Background**.
- Coal plant pages, or other more complex projects, may carry further sections (e.g.
  protests, expansions, financing) — acceptable when project complexity warrants it, but
  not part of the gas/oil baseline.
- All of these sections (Location, Project Details, Ownership Tree, Articles and
  Resources) are populated from the DB, not hand-authored. **Background is the only
  section researchers ever edit.**

## Editing the "Background" section

- This is the **only** part of a wiki page a human researcher edits directly.
- Purpose: capture the **date and basic details of the initial proposal** for a plant.
  This is what lets GEM later track progress (or lack of it) and justify moving a plant's
  status to "shelved" or "cancelled" — including when citing the plant in reports, media,
  or to partner organizations.
- **Edit boundary**: only add text between the "Ownership Tree" heading and the "Articles
  and Resources" heading (referred to in the manual as between "Comment 2" and
  "Comment 3" markers, visible in both "Editing" and "Edit Source" modes). Do not touch
  content outside that span — it's auto-generated/auto-maintained.
- **Joint coal-gas pages**: same rule — Background is the only section researchers edit.

## Renaming and duplicates

- **Renaming a plant**: the wiki URL and the page's displayed plant name update
  automatically from the DB — no manual page move/rename needed. The one manual step:
  if the old name is mentioned inside the Background section text, update it there,
  since that text isn't auto-rewritten.
- **Duplicate pages**: if duplicate plants are found in the tracker, fix the wiki side by
  redirecting the duplicate page to the correct one. In "Edit Source," add as the very
  first line: `#REDIRECT [[pagename]]`, where `pagename` is the title of the target page
  to redirect to.

## Link rot and archiving

- Links break over time (site redesigns, company renames without redirects, etc.).
- **Datasources attached in the DB are auto-archived** and used as the reference links
  that populate wiki pages — no manual archiving needed for those.
- **Reference links placed directly in the Background section are NOT auto-archived.**
  If a good source is found for Background text, manually archive it via the
  [Wayback Machine](https://web.archive.org/) at the time of writing. Some sites block
  bots/archiving — that's fine, it's a best-effort step, not a hard requirement.

## Wiki style guidelines (for Background-section text)

- Spell it **"Cancelled"**, not "Canceled" (matches the spelling used where most of the
  page audience is).
- Foreign-language articles: cite the article title in its original language.
- Translated quotes: prefer paraphrasing or indirect citation over a direct translated
  quote — a literal translation can misrepresent the speaker's meaning past a certain
  point.
- Units of measure: use the unit system of the country the plant is in (e.g. miles for a
  US plant, km for a Canadian plant), not a fixed house standard.

## Editing manuals referenced (external, not GEM-authored)

- MediaWiki "Quick guide to editing" and the "GEM Wiki Style Manual" are linked from the
  source manual as general wikitext/style references for researchers who choose to edit
  Background sections. Not reproduced here — consult gem.wiki's own help pages if needed.
