# How to write notes people can read

Rule set by Baird, 2026-10-02. It applies to everything the researcher agent
writes for a human: `researcher_notes` and `action` in staged records, the
evidence markdown, calibration memos, country notes, QC memos, and the text a
subagent puts in its shard.

## The rule

Write the way a careful colleague would explain it across a desk. Plain
words, short sentences, one idea per sentence. A GEM researcher who has never
seen this repo should be able to read a note once and know what was found,
where, and what to do.

## What that means in practice

- **Say what the source says, then what it means.** "The Maryland PSC order
  from March 2026 says the plant began commercial operation in February 2026.
  So the start year is 2026." Not: "Primary regulatory source confirms COD;
  stage start_year=2026."
- **Name sources by what they are**, not by role labels. "a Constellation
  press release", "the EIA-860M table for July 2026", "a Baltimore Sun
  article". Avoid "primary source", "OEM statement", "regulatory filing" as
  stand-ins for the actual document.
- **No repo jargon in the note itself.** Words like lane, shard, tier, staged,
  stage, ref, orphan, blue/green, qa record, url_verifier, colmap, merge-never-
  replace belong in scripts and docs, not in a note a researcher reads. If a
  process fact matters, say it in plain words: "The old link is dead, so I
  kept it and added the new one."
- **No abbreviations the reader might not know.** Spell out COD (commercial
  operation date), EPC (engineering, procurement and construction), PPA
  (power purchase agreement), IRP (integrated resource plan), CT (combustion
  turbine) the first time. State and agency names in full on first use.
- **Plain punctuation.** No em-dashes, no arrows, no slashes between
  alternatives, no parentheses holding a second thought. Start a new sentence
  instead.
- **Dates and numbers in full.** "February 2026", "289 MW", not "Feb-26" or
  "~289".
- **Say what was not found, in words.** "I could not find a start year for
  unit 2. The EIA table lists the plant but not this unit, and the owner's
  website only gives the total capacity." Not: "start_year unresolved; EIA
  n/a."
- **The action line is an instruction a person follows in the web form.**
  "Set the status of unit GT5 to retired and the retired year to 2024. Add
  the two links below to the status and retired-year source boxes. Keep the
  links already there."

## Before and after

Before (how notes used to read):

> Staged deletion: the recorded 2025 planned retirement has passed and the
> vessel was still supplying Dakar in June-July 2026 (Senelec
> maintenance/outage announcements carried by APS and PressAfrik — both trace
> to the same Senelec statement, so one independent origin). No source states
> a new contract end date (see qa).

After:

> The record says this power ship was due to retire in 2025, but it was still
> supplying Dakar in June and July 2026. Two news sites, APS and PressAfrik,
> reported Senelec maintenance notices that mention it. Both repeat the same
> Senelec statement, so this counts as one source. I suggest clearing the
> planned retirement year. I could not find a new contract end date, so I
> have flagged that separately for a human to look into.

## Where the machine words still live

Field names in `fields`, `refs`, `tier`, `independent` and the rest of the
staged JSON stay exactly as the contract defines them. The scripts need them.
This rule is about the free text a person reads, not the keys a script reads.
