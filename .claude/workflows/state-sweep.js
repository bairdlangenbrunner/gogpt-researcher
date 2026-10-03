export const meta = {
  name: 'state-sweep',
  description: 'US state sweep for the GOGPT tracker: one research subagent per plant (or plant group) reads its brief, researches the plant in blind or update mode, verifies every URL, and writes one JSON shard per plant. Read-and-write-shards only; nothing touches the live GEM database.',
  whenToUse: 'After build_state_brief.py and build_sweep_args.py have produced briefs and sweep_args.json for one US state batch (batches/us-<st>/).',
  phases: [
    { title: 'Research', detail: 'one subagent per plant (or per plant group), each writing shards/<plant_id>.json' },
  ],
}

// state-sweep.js: the fan-out step of the US state research agent.
// Contract: notes/us_state_agent_plan.md (Modes, Shard contract, the rules list).
// Free text in shards follows docs/reference/notes_style.md.
//
// Args (from `python scripts/build_sweep_args.py --batch batches/us-md --model sonnet`,
// which also writes batches/us-<st>/staging/sweep_args.json):
//   { repo, batch, state, postal, mode: "blind"|"update", model, csv,
//     plants: [{plant_id, plant_name, brief_path (absolute), unit_ids:[...], shard_path (absolute)}],
//     groups: [[plant_id,...], ...],     // every plant_id exactly once
//     extra_brief?: string }             // inlined into every prompt (file CONTENTS, not a path)
//
// Invoke: run build_sweep_args.py, then the Workflow tool with
//   scriptPath: .claude/workflows/state-sweep.js
//   args: <that JSON, passed as an object, not a string>
// Afterwards: assemble_state.py, state_gate.py (must print GATE CLEAN), qc_checks.py --staged.
//
// Model: chosen by the orchestrator at dispatch time (standing rule: the cheapest model
// genuinely good enough for this run) and passed as args.model. 'sonnet' is only the
// fallback when no choice is passed, never a pin.

// tolerate a JSON-encoded string (some invocation paths stringify `args`)
const A = (typeof args === 'string') ? JSON.parse(args) : (args || {})
if (!Array.isArray(A.plants) || !A.plants.length) {
  throw new Error('state-sweep needs args.plants. Run scripts/build_sweep_args.py and pass its JSON as `args`.')
}
if (A.mode !== 'blind' && A.mode !== 'update') {
  throw new Error(`state-sweep needs args.mode = "blind" or "update" (got ${JSON.stringify(A.mode)})`)
}
for (const p of A.plants) {
  if (!p.plant_id || !p.brief_path || !p.shard_path || !Array.isArray(p.unit_ids) || !p.unit_ids.length) {
    throw new Error(`plant entry incomplete (needs plant_id, brief_path, shard_path, unit_ids): ${JSON.stringify(p)}`)
  }
}
const MODEL = A.model || 'sonnet'
const REPO = A.repo
const BATCH = A.batch
const STATE = A.state || ''
const POSTAL = (A.postal || '').toUpperCase()
const MODE = A.mode
const PLANTS = Object.fromEntries(A.plants.map(p => [p.plant_id, p]))
const IDS = A.plants.map(p => p.plant_id)
const GROUPS = Array.isArray(A.groups) && A.groups.length ? A.groups : IDS.map(id => [id])
{
  const seen = GROUPS.flat()
  const missing = IDS.filter(id => !seen.includes(id))
  const dup = seen.filter((id, i) => seen.indexOf(id) !== i)
  const unknown = seen.filter(id => !PLANTS[id])
  if (missing.length || dup.length || unknown.length || seen.length !== IDS.length) {
    throw new Error(`args.groups must cover every plant_id exactly once (missing: ${missing.join(',')}; duplicated: ${dup.join(',')}; unknown: ${unknown.join(',')})`)
  }
}

// Scope-specific guidance, INLINED. Do not switch this to a path the agent is told to read:
// in the pipelines researcher (Russia R2, 2026-09-15) 8 of 8 agents skipped a brief they were
// told to read and went straight to Step 0. Agents reliably run the Step 0 commands they are
// given and reliably read text already in their prompt; they do not reliably fetch a document
// they were told to read. The per-plant briefs are therefore `cat` commands in Step 0.
const EXTRA = A.extra_brief
  ? `\n\n## Scope-specific guidance from the orchestrator\n${A.extra_brief}`
  : ''

// Exact CSV headers (schema_constants.RESEARCH_FIELDS); the brief's "Fields to report on" list wins if it differs.
const RESEARCH_FIELDS = [
  'Status', 'Capacity (MW)', 'Fuel', 'Turbine/Engine Technology',
  'Equipment Manufacturer/Model', 'Number Of Engines', 'Capacity Per Engine',
  'Start year', 'Retired year', 'Planned retire', 'Cancellation year',
  'Latest Activity', 'Status Detail', 'CHP', 'Owner(s)', 'Operator(s)',
  'Latitude', 'Longitude', 'Location accuracy', 'Captive industry use',
  'Captive industry type', 'Captive non-industry use',
  'Conversion/replacement?',
]
const PLANT_LEVEL = ['Owner(s)', 'Operator(s)', 'Latitude', 'Longitude', 'Location accuracy',
  'Captive industry use', 'Captive industry type', 'Captive non-industry use']

const BUDGET = MODE === 'blind' ? 25 : 12

const modeText = MODE === 'blind'
  ? `## Mode: blind (calibration run)
GEM's values are withheld; research every field in RESEARCH_FIELDS from scratch; do not look at
gem.wiki or globalenergymonitor.org at all, they would leak the answer and are banned as citations
anyway. Also do not open the export CSV, anything under \`${BATCH}/briefs/_hidden/\`, or another
plant's brief, and do not run entity_lookup.py: all of those reveal withheld GEM values. Record
owner and operator names in \`entities\` with lookup_result "not run, blind mode"; the main loop
checks them later. Report a finding for every field you can source. A field you could not source
goes in \`not_found\`.`
  : `## Mode: update (normal batch)
The brief shows current values and existing sources, and its "What to check" section lists the
tasks for each unit. Do those tasks and nothing else. Report only the fields in the brief's
"Fields to report on" list: a blank you can fill, a value that should change, or a value you
re-verified with a source not already cited. Units marked "Nothing to check" are not researched;
list them in \`units\` with empty findings. Harvest the existing source URLs first (they are
candidates, still run them through the verifier). A dead existing link is never dropped by you; say
in \`source_log\` that it is dead. Before naming a new owner or operator, run
\`python scripts/entity_lookup.py "<name>"\` (bare, no --country) and copy what it says into
\`entities[].lookup_result\`. In \`not_found\` list the fields a task asked for that you could not
fill. A value you notice in passing that looks wrong goes in \`qa\`, not in \`findings\`.`

const statusRule = MODE === 'blind'
  ? `blind mode has no current value to change, so a status gets \`high\` on one fully validated ref`
  : `a status change, meaning your status differs from the brief's current status, is \`high\` only\n  with two independent publishers, else \`medium\``

const contractFor = (group) => {
  const plants = group.map(id => PLANTS[id])
  const multi = plants.length > 1
  const catLines = plants.map(p => `  cat "${p.brief_path}"`).join('\n')
  const plantList = plants.map(p =>
    `- ${p.plant_id} ${p.plant_name || ''}: units ${p.unit_ids.join(', ')}; write the shard to \`${p.shard_path}\``).join('\n')
  const logLines = plants.map(p => `  ${p.plant_id}: ${BATCH}/shards/${p.plant_id}.urls.jsonl`).join('\n')
  const workDir = `${REPO}/work/sweep_${(A.postal || 'us').toLowerCase()}`
  const pid = multi ? '<plant_id>' : plants[0].plant_id

  return `You are a careful researcher for Global Energy Monitor (GEM), a nonprofit that tracks
fossil fuel infrastructure worldwide. You are updating its Global Oil and Gas Plant Tracker (GOGPT),
a unit-by-unit database of oil and gas fired power plants; your job is one ${multi ? 'group of plants' : 'plant'}
in ${STATE}, United States. You write a JSON file; you never edit the GEM database.

${modeText}

## Your ${multi ? 'plants' : 'plant'}
${plantList}
${multi ? `These plants share documents, so research shared documents once, but each plant gets its own
shard file, its own verifier log and its own unit entries. A page that states a value for one plant
is not a source for another plant unless it states that plant's value too.\n` : ''}
RESEARCH_FIELDS (exact CSV headers; the brief's "Fields to report on" list wins if it differs):
${RESEARCH_FIELDS.join(' | ')}
Plant-level fields (report once in \`plant_findings\`; they apply to every unit):
${PLANT_LEVEL.join(' | ')}
Every other field is unit-level and goes under that unit in \`units[].findings\`.

## Step 0, before any research
Run these from the repo root, in this order:
  cd ${REPO}
${catLines}
  python scripts/url_verifier.py
The last command has no --help flag; with no arguments it prints its usage line and exits 2.
That is expected. Each plant's verifier log (append-only JSONL, one line per check):
${logLines}
Environment variables do not survive between your shell calls, so pass the log on every call:
  python scripts/url_verifier.py --log ${BATCH}/shards/${pid}.urls.jsonl "<url>" "<value>" ["<more>"]
Save any downloaded file (curl -o, PDFs, pdftotext output, Excel files) under \`${workDir}/${pid}/\`,
never anywhere else in the repo.

Then write a first version of each shard right away, with every unit present, empty findings and
\`meta.done: false\`, and rewrite it as findings come in. If you run out of room, the file on disk is
what survives.

## Research ladder for a US gas plant
Work down this list. Prefer the document that names the plant AND states the value.
1. EIA-860M, the monthly generator inventory, by plant and generator. The plant's EIA plant code is
   often in "Other IDs (location)" (for example "EIA: 54832") and generator IDs in "Other IDs (unit)".
   The files are Excel downloads listed at https://www.eia.gov/electricity/data/eia860m/ . Download
   the newest monthly file with curl, read it with python (pandas or openpyxl), and filter on the
   plant code. It gives status, nameplate MW, technology, operating month and year, planned and
   actual retirement dates.
2. EIA-860 annual (https://www.eia.gov/electricity/data/eia860/): ownership shares (schedule 4),
   technology, prime mover, CHP flags, coordinates (schedule 2).
3. EIA-923 (https://www.eia.gov/electricity/data/eia923/): monthly generation and fuel use by plant.
   Recent generation proves operating. EPA CAMPD (https://campd.epa.gov/) has unit-level emissions
   and operating hours, which also prove a unit is running.
4. The state public utility commission docket search (certificates, siting orders, retirement filings).
5. The state environmental agency's air permits (permits list units, turbine models and MW ratings).
6. The regional grid operator's interconnection queue and deactivation lists: PJM for Maryland,
   ERCOT for Texas, otherwise MISO, SPP, CAISO, NYISO or ISO-NE as the state requires.
   PJM's queue web pages are drawn by JavaScript and show nothing to a fetch, so use its files.
   The whole queue is one file of about 9,200 projects, withdrawn ones included. Download it once:
     curl -sL -o ${workDir}/${pid}/PlanningQueues.xml https://www.pjm.com/pub/planning/downloads/xml/PlanningQueues.xml
   Read it with python (xml.etree). Match on Name, CommercialName, State and County. Each project
   has Fuel, MWCapacity, Status, ProjectedInServiceDate, ActualInServiceDate and WithdrawalDate.
   Verify the file URL with url_verifier.py --timeout 120 and the plant name as the expected
   string. Quote the matching record in \`note\`, as for EIA Excel files. For retirements, the
   notices page https://www.pjm.com/planning/service-requests/gen-deactivations/generator-deactivation-notices
   links each plant's deactivation letter and PJM's reply as PDFs. Cite the PDF, not the list page.
7. The owner's own website, press releases and SEC 10-K filings.
8. FERC filings (eLibrary).
9. Local news.
Search with your WebSearch and WebFetch tools (load them with ToolSearch if they are deferred) and with curl.

Excel files cannot be checked by the verifier's text match. For an EIA Excel file, cite the URL of
the specific file you read (not the index page), run the verifier on it with no expected strings to
prove it loads, read the value from the downloaded file, set \`contains_value\` and \`name_found\` to
true only if you saw them in the file, and put the matching row in \`note\`, for example "Plant
54832, generator 1, status OP, nameplate 289.0 MW, operating year 1996".

Every other URL you cite must be run through url_verifier.py with the value as the expected string
(a distinctive form of it: "289", "1996", the turbine model). Its last line reads
"Result: PASS (...)" or "Result: FAIL (...)", and the same result lands in the JSONL log. Copy it
into \`verifications\`: \`ok\` is true when the page loaded and is not an error, paywall or banned page;
\`contains_value\` is true on a PASS with the value as the expected string; \`name_found\` is true when
a second run with a distinctive piece of the plant name passes, or you read the name on the page
yourself (then say so in \`note\`). A status is often stated in other words ("began commercial
operation", "retired in May"). If the verifier misses a status word, read the page and explain the
inference in \`note\`.

Fetch failures are tooling failures, not facts about the page. WebFetch is blocked by many sites
that the repo's own fetcher reads fine, so never stop at a WebFetch failure. When any fetch is
blocked (401, 403, 429, "Access Denied", "Just a moment", "Undeclared Automated Tool"), empty,
truncated or garbled, work this ladder in order and stop at the first rung that gives you the page:
  1. python scripts/fetch.py "<url>" --head 3000
     This runs curl with a browser user agent, then browser-fingerprint impersonation, then a real
     Chrome window for JavaScript challenges. It handles sec.gov itself with the declared identity
     SEC requires. Its "notes:" line says which route worked. Use --text for the whole body. PDFs
     and zip bundles come back as extracted text, with OCR for scanned PDFs.
  2. Run url_verifier.py on the URL. It uses the same fetcher and falls back to the newest Wayback
     Machine snapshot when the live page still refuses. A Wayback pass keeps the LIVE URL citable.
  3. Try other forms of the same page: www. or bare host, http or https, the canonical URL from a
     search result, a print view, or the publisher's own copy of a wire story.
  4. Find the same document at another address. Company press releases are usually also on PR
     Newswire, Business Wire or GlobeNewswire. Investor pages often have a second host, for example
     investor.conedison.com and conedison.gcs-web.com.
SEC filings: never fetch sec.gov with curl or WebFetch directly. SEC refuses any client that does
not declare a contact, so always go through fetch.py or url_verifier.py. To find a filing, use
EDGAR full-text search, for example
  python scripts/fetch.py 'https://efts.sec.gov/LATEST/search-index?q=%22North%20Tonawanda%22&forms=10-K' --text
then cite the filing document URL under https://www.sec.gov/Archives/edgar/data/.
Only after the whole ladder fails may you record a URL as blocked in \`source_log\`, and the note
must say what you tried. Never conclude a page lacks the value from a blocked or truncated fetch.
Cite the live URL, never a web.archive.org address.

## Rules
- Values are cell content only, in exact controlled vocabulary. Status is lowercase: announced,
  pre-construction, construction, operating, mothballed, shelved, retired, cancelled. A
  shelved-inferred or cancelled-inferred status (stored as "shelved - inferred 2 y" or
  "cancelled - inferred 4 y") carries NO URL and documents the search in \`note\`: where you looked,
  the newest evidence you found and its date. It applies only to an announced, pre-construction or
  construction unit with no activity in documents for 2 years (shelved) or 4 years (cancelled).
- Never a URL or a sentence in a value.
- Every URL in \`refs\` needs a passing verification. \`refs\` may be empty only for an inferred status.
- Hydrogen and computed columns are never reported.
- A combined-cycle block is one unit, never split into turbines.
- Capacity is electric generating MW (nameplate), not thermal, not mechanical. Give it as the
  source states it, to one decimal at most (289.0, 53.1); for a range give the high end.
- No start year for shelved or cancelled units. No retired year for mothballed units.
- Mothballed, retired and cancelled are only tracked from 2020 onward.
- Owners as \`Name [share%]\`, separated by semicolons, five percent or more, top four plus "other",
  never a national government. A single confirmed owner is \`Name [100%]\`.
- \`Latitude\` and \`Longitude\` in decimal degrees, with \`Location accuracy\` exact or approximate.
- Fuel as \`category: detail\` tokens, for example "fossil gas: natural gas, fossil liquids: fuel oil".
  Technology long form: combined cycle, gas turbine, aeroderivative gas turbine, steam turbine,
  internal combustion, or ICCC, ISCC, AFC, unknown. CHP is yes, no or not found, and "no" only when a
  dataset explicitly says so.
- Never cite gem.wiki, globalenergymonitor.org, abarrelfull, or anything that footnotes GEM.
  Wikipedia, GridInfo, plant-map sites and the Sierra Club ID sheet are for finding leads only;
  cite the document they point to.
- Mirrors of one document count as one source. A press release and its wire reprints are one source.
- Tier \`high\` = one fully validated ref: it names the plant, states the value, and passes the
  verifier. BUT ${statusRule}.
- \`medium\` = a single-source status change, or a ref that names the plant but only implies the value.
- \`low\` = partial validation: the page does not name the plant, or the value is not on it, or
  sources conflict. Prefer leaving the field out and raising a \`qa\` item.
- \`independent\` = true only with 2 or more genuinely separate origins among the refs.
- Take a second source when it is cheap, but never spend searches chasing one, except for a status
  change in update mode, where one extra search for a second publisher is worth it.
- Location: never change \`Latitude\`, \`Longitude\` or \`Location accuracy\` when the brief shows a value.
  Only fill blanks. A better coordinate you found is a \`qa\` note.
- Owners: GEM's \`Owner(s)\` is the company that holds the plant; the corporate parent is a separate,
  computed field you never report. The utility or operator name in an EIA table is not the owner.
  If it differs from GEM's owner, raise a \`qa\` question. Change an owner only on a dated, closed
  transaction (sale completed, not announced) from two independent publishers, and name the buying
  entity that holds the plant, not its parent.
- Fuel: never remove a fuel that the EIA-860 energy source columns (1 to 6) list for the unit. The
  EIA-923 monthly fuel table shows what was burned recently, not what the unit can burn.
- Conversion units (a unit name with "timepoint 2" or a \`Conversion/replacement?\` value): the
  start year is the year the converted unit began operating on the new fuel, and
  \`Conversion/replacement?\` takes only the values conversion or replacement.
- \`Number Of Engines\` and \`Capacity Per Engine\` are for reciprocating engines (internal
  combustion) only. Never fill them for turbines.
- Captive fields (\`Captive industry use\`, \`Captive industry type\`, \`Captive non-industry use\`)
  stay blank for a plant that sells to the grid. Never write "no" in them. Fill them only for a
  plant that mainly serves one industrial site or a data center, with a source.
- \`Latest Activity\` is a date field in GEM. Its value is the date of the newest dated report of
  activity you found, written exactly as \`Year: 2024, Month: 6, Day: 17\` (leave off day, or month
  and day, when the source does not give them). What happened goes in the finding's note, never
  in the value. Never move the date backward: if GEM already shows a later date, raise a \`qa\` note.
  Year fields (\`Start year\`, \`Retired year\`, \`Cancellation year\`, \`Planned retire\`) hold a
  four-digit year only.
- Possible duplicates, units that look split or merged wrongly, and values you think are wrong but
  cannot source go in \`qa\`. Units at the plant missing from the brief go in \`newunits\`, with refs.

## How to write notes
Every \`note\`, \`notes\` and \`recommendation\` is read by a GEM researcher who has never seen this
repository. Write the way a careful colleague explains something across a desk.
- Plain words, short sentences, one idea per sentence.
- Say what the source says, then what it means.
- Name sources by what they are: "a Constellation press release from March 2026", "the EIA-860M
  table for July 2026", "a Baltimore Sun article".
- No repo jargon: never write tier, lane, shard, ref, staged, qa, verifier, orphan.
- No abbreviations without expansion on first use: commercial operation date, combustion turbine,
  power purchase agreement, integrated resource plan.
- No em-dashes, no arrows, no slashes between alternatives, no parentheses. Start a new sentence.
- Dates and numbers in full: "February 2026", "289 MW".
- Say what was not found, and why.
Examples:
  "The Maryland Public Service Commission order from March 2026 says the plant began commercial
  operation in February 2026. So the start year is 2026."
  "I could not find a start year for unit 2. The EIA table lists the plant but not this unit, and
  the owner's website only gives the total capacity."

## Budget
Up to about ${BUDGET} fetches per plant${MODE === 'blind' ? ' (blind mode researches every field)' : ' (update mode does only the tasks in the brief)'}. The EIA files cover many
fields at once, so start there. When the budget is spent, stop and write the shard with what you
have. A shard with honest \`not_found\` lists is useful; returning nothing is not.${EXTRA}

## Output
Write each shard to its \`shard_path\` as one JSON object with EXACTLY this shape (write it with
python json.dump or your Write tool, then check it parses with
\`python -c "import json,sys; json.load(open(sys.argv[1]))" <shard_path>\`):
{
  "meta": {
    "plant_id": "L100000402511", "plant_name": "Brandywine power facility",
    "state": "${STATE}", "mode": "${MODE}", "model": "${MODEL}",
    "generated": "2026-10-02T15:10:00-04:00", "done": true,
    "urls_attempted": 14, "urls_verified": 9
  },
  "units": [
    {
      "gem_unit_id": "G100000401771", "unit_name": "F701",
      "findings": {
        "Status": {
          "value": "operating",
          "refs": ["https://..."],
          "verifications": [{"url": "https://...", "ok": true,
                             "contains_value": true, "name_found": true}],
          "tier": "high", "independent": false,
          "note": "The EIA-860M table for July 2026 lists this unit as operating."
        },
        "Capacity (MW)": { "...": "same shape" }
      },
      "not_found": ["Start year"],
      "notes": "One or two plain sentences about this unit, including what was not found and why."
    }
  ],
  "plant_findings": { "Owner(s)": { "...": "same shape; applies to every unit" } },
  "qa": [ {"gem_unit_id": "G...", "concern_type": "duplicate",
           "recommendation": "...", "note": "...", "refs": []} ],
  "monitor": [], "newunits": [],
  "entities": [ {"entity_name": "...", "role": "owner", "lookup_result": "..."} ],
  "source_log": [ {"url": "https://...", "used_for": ["Status", "Capacity (MW)"],
                   "outcome": "verified", "note": "..."} ]
}
- \`meta.done\`: true only in the final write. \`meta.model\`: "${MODEL}". \`meta.mode\`: "${MODE}".
- \`meta.generated\`: ISO time with offset, from
  \`TZ=America/New_York python3 -c "import datetime; print(datetime.datetime.now().astimezone().isoformat(timespec='seconds'))"\`.
- \`meta.urls_attempted\` = URLs you ran through the verifier; \`meta.urls_verified\` = those that passed.
- \`units\` has one entry per unit ID listed above, every unit, even if nothing was found, with
  \`not_found\` listing the fields. A plant-level field you could not find goes in every unit's
  \`not_found\`.
- Field keys in \`findings\` and \`plant_findings\` are exact CSV headers from RESEARCH_FIELDS.
- \`source_log\` lists every URL you tried, including failures, with outcome verified, failed,
  blocked, dead or not relevant.

Then return ${multi ? 'one summary object per plant in `plants`' : 'a short JSON summary'}: plant_id,
units_reported, fields_found, fields_not_found, urls_verified, shard_written (true only if the file
is on disk, parses, and has meta.done true), problems (one plain sentence, or "none"). The shard
file is the deliverable, not your message.`
}

const SUMMARY_PROPS = {
  plant_id: { type: 'string' },
  units_reported: { type: 'integer' },
  fields_found: { type: 'integer' },
  fields_not_found: { type: 'integer' },
  urls_verified: { type: 'integer' },
  shard_written: { type: 'boolean' },
  problems: { type: 'string' },
}
const SUMMARY_SCHEMA = {
  type: 'object',
  properties: SUMMARY_PROPS,
  required: Object.keys(SUMMARY_PROPS),
}
// a multi-plant group returns one summary per plant
const GROUP_SCHEMA = {
  type: 'object',
  properties: { plants: { type: 'array', items: SUMMARY_SCHEMA } },
  required: ['plants'],
}

phase('Research')
log(`State sweep: ${STATE} (${POSTAL}), ${MODE} mode, ${IDS.length} plants in ${GROUPS.length} agent(s), model ${MODEL}.`)
const results = await parallel(GROUPS.map(group => () =>
  agent(contractFor(group), {
    label: `research:${POSTAL}:${group.join('+')}`,
    phase: 'Research',
    agentType: 'general-purpose',
    model: MODEL,
    schema: group.length > 1 ? GROUP_SCHEMA : SUMMARY_SCHEMA,
  })
))

const summaries = []
results.forEach((r, i) => {
  if (!r) {
    GROUPS[i].forEach(id => summaries.push({ plant_id: id, shard_written: false, problems: 'agent returned nothing (skipped or failed)' }))
    return
  }
  if (GROUPS[i].length === 1) summaries.push({ ...(Array.isArray(r.plants) ? r.plants[0] : r), plant_id: GROUPS[i][0] })
  else summaries.push(...(r.plants || []))
})
// counted by plant ID, so a mislabeled or missing per-plant summary shows up as not written
const missing = IDS.filter(id => !summaries.some(s => s && s.plant_id === id && s.shard_written))
const written = IDS.length - missing.length
log(`Research done: ${written}/${IDS.length} shards reported written in ${BATCH}/shards/.${missing.length ? ' Not written: ' + missing.join(', ') + '.' : ''} Next: assemble_state.py, then state_gate.py.`)
return { state: STATE, mode: MODE, plants: IDS.length, shards_written: written, summaries }
