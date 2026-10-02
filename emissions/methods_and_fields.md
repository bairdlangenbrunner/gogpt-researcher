# What to capture, and which numbers are worth most

Distilled from CREA's methods doc (Daniel Nesan; link in `README.md`) and the
2026-09 meetings. The live doc wins on any conflict. GEM's job is to **find and
faithfully record** the evidence; CREA does the calculation and picks the
method. Usually only one or two evidence types exist per country — don't try to
fill all of them.

Pollutants: **NOx, SOx/SO2, PM**. PM fractions (TSP, PM10, PM2.5) are not
interchangeable — record the fraction as reported.

## Evidence ladder (best first)

| | Evidence found in the document | What CREA does with it | What we must also record |
|---|---|---|---|
| A | Annual mass total (t/yr, kg/yr) | Uses directly | Scope (plant / unit / stack), period, and whether it is measured, predicted (EIA scenario), permitted, or estimated. The operating-hours / load assumption behind it |
| B | Mass rate (g/s, kg/h) | Annualises with operating hours | Operating hours if stated — capacity factor is *not* automatically operating hours. Per stack or per plant |
| C | Stack concentration (mg/m³, ppm) **plus** flue-gas flow | Converts to g/s, then annualises | Is it normalised? Reference O2 %, dry/wet basis, temperature/pressure, actual vs standard volume. If flow is missing: exit velocity + internal stack diameter |
| D | Nothing plant-specific | Capacity × capacity factor × heat rate × emission factor (EMEP/EEA, CEDS, a local anchor EIA, or the national limit) | Technology (CCGT / open-cycle GT / engines — matters for efficiency and for NOx), turbine model, controls, fuel. CREA assumes CCGT for future plants unless told otherwise |
| E | Emissions + generation for a comparable plant | Derives a local intensity (kg/MWh) or a capacity regression, applies to similar plants | Only transfers between same fuel, technology, controls, era |
| F | Interval / CEMS time series | Sums | Timestamps, operating state, bypass-stack coverage (operating plants only) |

## Basis — actual or reasoned, versus potential

The ladder says what *form* a number takes. It does not say whether the number
describes what a plant emits. An annual total built on full load for 8,760
hours is a **potential** emission, not an estimate: it says what the plant
could emit if it never stopped, and gas plants never run like that. The scoping
has to show, plant by plant, which kind we can get. Record it for every find,
next to the ladder letter (`basis` in the coverage sheets).

| `basis` | Meaning | Counts as actual or well-reasoned? |
|---|---|---|
| `measured` | Stack tests, CEMS, or an annual total the operator reports as measured | yes |
| `reported-actual` | An annual total calculated or estimated from that year's real fuel use or generation (operator report, inventory) | yes |
| `design-hours` | Predicted, and the document itself states a realistic operating assumption — hours, capacity factor, dispatch case | yes |
| `rate-only` | A full-load rate or concentration with no operating assumption. Dispersion studies model the worst case, so this is the usual EIA result | only once paired with a defensible utilisation — real generation for an operating plant, a stated or comparable-plant figure for a proposed one. Say which |
| `potential` | An annual figure at 8,760 h and full load, or derived from the permit limit | no. Back out the rate, record it as `rate-only`, and never quote the tonnes as an emission |
| `limit-only` | A limit with no emission | no |

How to tell: divide the annual figure by the mass rate. 8,760 means potential;
anything else is the document's operating assumption, and it should be stated
somewhere in the text — find it and cite the page. An annual figure whose hours
cannot be recovered is `potential` until shown otherwise.

A permitted **limit** is not an emission, but it is still wanted: the concept
note's tiering is project-specific limits and controls in priority countries →
national emission standards elsewhere → default factors where standards are
absent or laxer than uncontrolled factors. So a licence that only states a NOx
limit is a usable find.

An **operating** plant's EIA or monitoring report is useful too: CREA
extrapolates to proposed plants from existing ones (Thailand: single-variable
regression of g/s on MW; Malaysia: one ESIA anchored the whole proposed fleet).
One well-documented anchor plant per country and technology is worth more than
several thin ones.

## Fields per plant

From CREA's answer in the regional-prioritization doc plus §4 of the methods
doc. Blank is fine; never guess.

- **Identity** — GEM location ID and unit IDs; local-language name; how the
  document's units / turbines / stacks map onto GEM's units.
- **Evidence** — document title, type (EIA / RIMA / ESIA / licence / dispersion
  study / monitoring report), issuing body, year, URL, retrieval date,
  page/table per value; status of the number (measured / predicted / permitted
  / estimated); operating basis (hours, load, fuel case).
- **Emissions** — per pollutant: original value and unit exactly as written;
  which of A/B/C it is; reference O2; dry/wet; averaging period; per-what
  (stack / turbine / unit / plant).
- **Stack** — number of stacks, height, internal diameter, exit temperature,
  exit velocity or volumetric flow; bypass stacks.
- **Technology** — CCGT / OCGT / RICE; turbine or engine make and model;
  NOx controls (DLN, SCR, water/steam injection); backup fuel and its sulfur.
- **Activity** — assumed capacity factor or operating hours, efficiency or heat
  rate (net/gross, LHV/HHV), expected lifetime, start-ups per year if given.
- **Coordinates** — the stack location if the document gives one.

## QC rules (CREA's, kept verbatim in spirit)

- Unknown ≠ zero; measured ≠ predicted; permitted limit ≠ actual emissions.
- Never overwrite or convert the reported value — record the original; any
  conversion goes in a separate, labelled field.
- Check O2, dry/wet, temperature, pressure, actual/standard volume before
  anyone combines a concentration with a flow.
- Don't apply utilisation or time adjustments twice (an EIA annual total already
  embeds its operating assumption).
- Keep the plant–unit–stack mapping intact.
- Country-derived factors don't compare across countries (CREA's Malaysia vs
  Hsieh-Ho example: 4.4× the capacity, 16× the NOx, purely from method). Always
  carry the method label with the number.
