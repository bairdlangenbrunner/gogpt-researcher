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
- **Every source a note names comes with its URL**, written out in full right after the name ("the EIA-860M table for August 2026 is at https://..."). The review page turns it into a link, and the researcher needs it to check the claim or paste it into a source box (Baird 2026-10-22). A source with no live link, such as a saved copy, says so and names the link that is cited instead.
- **Never point to a file on your own computer.** The reader does not have it. No `work/...` or `batches/...` paths, no home folders, no saved file names like `pjm_cycle_queue_2026-10-21.xlsx`. Cite a web address that shows the claim. When a list only comes as a download, find the web page for the one entry if the site has one (PJM has a page per queue request at `https://www.pjm.com/m/ProjectTransition/SISReportDetails?queueNumber=<queue number>`). **Never hand the reader a task.** Download the file and read the row yourself, then say what it shows and when you read it. Cite a public page that states the values: the official per-entry page, or a queue tracker page such as `https://www.interconnection.fyi/project/pjm-<queue number>` (a lead site, so the values stay yellow). Never write steps for the reader to download a file and find a row (Baird 2026-10-29). `state_gate.py` flags a local path in any note (Baird 2026-10-27).
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
- **Every note makes sense read alone.** Write whole sentences that say what the note is about. Never squeeze a note into a fragment that only works next to the text beside it. "A no needs a document that states it. None found." became "The database flags this unit because its carbon capture answer has no source. I found no document that says whether the unit has carbon capture, so there is no source to add." (Baird, 2026-10-16.)
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

## Questions

A question record has four parts. The question is one sentence that ends with a question mark, stays under about 120 characters, and is specific to the record. The finding is one to three sentences on what the sources say. The recommendation is one or two sentences the reviewer can act on: leave as is, change X to Y, merge with Z, ask the PM, or cancel. Never write "the reviewer should decide". The note holds everything else, including what could not be reached and why. (Baird, 2026-10-27.) Name the filer of comments or testimony (the Environmental Law and Policy Center, the Iowa Environmental Council and Sierra Club), never "intervenors" or "the intervenor comments" on their own. When the database already carries a note from the reviewer on the unit, the question answers that note first: say whether the sources agree with it and why. (Baird, 2026-10-29.)

question: Is the 430 MW combined cycle unit from the 2024 study still planned?

finding: The study, dated February 13, 2025, adds a 430 MW combined cycle unit in 2029. No later filing names it. Alliant's quarterly report for June 30, 2026 lists only simple-cycle projects, Morgan Valley at 720 MW and Riverhawk at about 1,200 MW. Morgan Valley's April 2026 application says the site could later be converted to combined cycle, and nothing more.

recommendation: Leave the unit as announced. Check again when Alliant files a combined cycle plan.

note: everything else, including what could not be reached and why.

## Where the machine words still live

Field names in `fields`, `refs`, `tier`, `independent` and the rest of the
staged JSON stay exactly as the contract defines them. The scripts need them.
This rule is about the free text a person reads, not the keys a script reads.
