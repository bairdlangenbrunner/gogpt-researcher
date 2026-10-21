# The location step: addresses, site maps and coordinates

Planned and built 2026-10-20 (Baird). The first scope to run it is Kansas (`location_candidates.py --state Kansas` finds 6 candidates among 30 plants). This page is the contract the scripts follow, in the same way `staged_json_schema.md` is the contract for staged records. It runs on every scope batch by default, like the validation report and the captive LNG steps: `build_state_brief.py --location ../work/location_<tag>.json` is part of the standard step 2 in `docs/workflows.md` §2.

## What it is for

GEM stores one location per plant: `Latitude`, `Longitude`, `Location accuracy` (`exact` or `approximate`), `Location Data Source`, and the place fields (`City`, county, district, `State/Province`). The manual wants `exact` to mean the point sits on the plant, with at least three decimals. The export carries almost every coordinate at six decimals whatever the accuracy, so the decimal count says nothing; only the accuracy value does.

The step looks at plants whose location is weak and tries to pin them down, in the cheapest order that works:

1. an address, a parcel, or a stated site reference in a document, turned into a point;
2. a satellite look at the point to confirm it;
3. only then, an official map in a document, georeferenced to a point.

It also makes every coordinate a person reads clickable, so a reviewer can open the spot in Google Maps and judge it in seconds.

Scale as of the October 2026 export: 1,607 of 6,819 plants are approximate and one has no coordinate. In the United States 261 are approximate, of which 178 are announced, 58 pre-construction and 10 under construction; only 3 are operating. So in the US this is a "where will it be built" question. Worldwide, 453 operating plants are approximate, and those are usually settled by the satellite look alone.

## Which plants get the step

Only plants whose `Location accuracy` is `approximate` or whose `Latitude` or `Longitude` is blank (Baird 2026-10-20). A plant marked `exact` is never reopened by this step, even when a dataset point disagrees with it; `match_ids.py` already reports the distance between GEM's point and the EIA-860M point, and that line stays a question on the brief, not a location task. New plants from a discovery batch or the scope-wide search always go through the ladder, since a new row needs coordinates (Discovery SOP §6).

`location_candidates.py --state <State>` (or `--country "<Country>"`) selects them from the fresh scoped export and writes `work/location_<tag>.json` and `.md`: per plant, the current coordinate and accuracy, the hosts in `Location Data Source`, the place fields already filled, the status group, and every dataset point available with its distance from GEM's point. For a US state the dataset points come from the EIA-860M file already kept under `work/eia/` and from the EIA-860 annual Plant table, which carries a street address, county and coordinates; `eia860.py` keeps the newest annual file next to the monthly one. Permit-portal hits with coordinates (`harvest_permits.py`) join the same list.

`build_state_brief.py --location ../work/location_<tag>.json` puts one location task on each candidate plant's brief, with the current point as a map link, the dataset points and their distances, and the address when a dataset gives one. Tagged checklist row 25, and row 42 when the plant is operating.

## The ladder the agent follows

Written for the research agent and for the person who reads its note afterwards.

1. **Address or site reference first.** Look for a street address, a parcel number, or a sentence that places the plant ("on the site of the retired Riverside coal plant", "next to the Elm Creek substation", "in the Great Plains industrial park south of town") in a primary document: the air permit application, the utility's filing or integrated resource plan, a county planning agenda, the developer's project page, the EIA-860 Plant table. For a US state the EIA address is often enough on its own. Quote the sentence and name the document.
2. **Turn it into a point.** `geocode.py "<address or place>" --near <lat>,<lon>` resolves the text through the US Census geocoder for US addresses (free, no key) and Nominatim for everything else (free, no key, one request a second, results cached under `work/geocode/`). It prints the candidates with a match quality, and a Google Maps link for each. A site reference resolves by looking up the named neighbor the same way. The agent picks the candidate that fits the document and says why.
3. **Look at it.** `site_image.py <lat> <lon> [--zoom 16]` fetches a satellite mosaic around the point (Esri World Imagery tiles, no key) into `work/sweep_<tag>/maps/<plant_id>_<n>.png`, with a crosshair at the point and a scale bar. The agent looks at the picture. An operating or under-construction plant should show its footprint: stacks or exhaust stacks, the turbine hall, cooling towers or an air-cooled condenser, the switchyard, the gas yard. A proposal should show the stated parcel, cleared ground, or at least the named neighbor. The note says in words what was seen ("a gas plant footprint with two stacks and a switchyard, about 400 m east of the GEM point") and that the imagery date is unknown, since tiles can lag new construction by a year or more.
4. **Only if 1 and 2 fail: an official map.** Find a site plan or location figure in a document: the air permit's site map, an environmental review figure, an interconnection or transmission drawing, a zoning exhibit. `georef.py render <pdf> --page N` renders the page to an image under `work/sweep_<tag>/maps/`. The agent names two or three features it can see labeled on the map: a road intersection, a named substation or plant, a river crossing, or, best of all, a coordinate grid tick when the map has one. It resolves each feature's coordinate (the grid tick directly; the others through `geocode.py`) and gives `georef.py solve` the pixel positions and the coordinates. The script fits the transform, converts the marked site to a lat lon, reports the fit error in meters, and writes the page image with the control points and the site drawn on it to `batches/<scope>/staging/maps/<plant_id>.jpg`. The note lists the control points so a reviewer can redo it.
5. **If nothing works**, say so in words, leave the coordinate alone, and raise a question (`qa`, `concern_type` `location`) that names what was searched.

A found point only becomes an edit when it tells GEM something new: a blank filled, an approximate point moved more than 500 m (the assembler's 0.005 degree match tolerance), or an approximate plant promoted to exact. A better-but-nearby point on an approximate plant that stays approximate is not worth an edit; the agent reports it in the note and moves on.

## Accuracy and confidence rules

- **Exact** needs the point confirmed in imagery (step 3) with the plant's footprint visible, or a parcel or address placed in imagery for a proposal whose parcel the document names. At least three decimals, and the staged value is written with five.
- **Approximate** is everything else: a bare geocode, a georeferenced map without an imagery check, a proposal known only to a town or county. A proposal known only to a town stays as it is and is not staged unless GEM's point is blank or more than 2 km from the right town.
- **Confidence tier.** One fully validated document plus a map pin is `high` (green): the document names the plant and places it, and the pin link opens on the point. A georeferenced map alone is `medium` (yellow), because the point rests on the agent's reading of the figure. A geocode the agent could not check in imagery is `medium`. A location change is not a status change, so one source is enough for green (`confidence_tiers.md`).
- **Data Source.** A Google Maps pin link alone is an acceptable `Location Data Source` (Baird 2026-10-20); it is already the most common location source in GEM, about 2,100 plants. When a document gave the address or the map, cite the document too. Merge, never replace, like every other Data Source cell.
- **Place fields.** When the ladder settles the point it usually settles `City` and the county as well; fill those when blank, from the same document, tagged row 26 for City and State/Province and row 25 otherwise. Never change a filled place field from a geocoder's reverse lookup alone.

## Links and pictures a person sees

Every coordinate shown to a person is a link (Baird 2026-10-20):

- Satellite view at the point, for checking a plant: `https://www.google.com/maps/@?api=1&map_action=map&center=<lat>,<lon>&zoom=17&basemap=satellite`
- A dropped pin, for the Data Source cell and for sharing: `https://www.google.com/maps/search/?api=1&query=<lat>,<lon>`

Coordinates are written with five decimals in links and staged values. The actions workbook makes the `Latitude` and `Longitude` cells hyperlinks (current and proposed), the evidence markdown writes both links on the location line, the brief shows the current point as a link, and the review card shows current and proposed as links with the distance moved and the method.

Pictures (Baird left this to the agent; decided 2026-10-20, yes):

- **The review card** shows a satellite patch for the current point and one for the proposed point, side by side, with a crosshair. The patches are a two-by-two grid of Esri World Imagery tiles at zoom 16 assembled in the page from the coordinate, so no image files are stored; the page carries the Esri attribution line. The interface change belongs in `../gem-review-app`, never in a shim here (`review_app/README.md`).
- **A georeferenced plant** also shows the saved map render with its control points, from `batches/<scope>/staging/maps/<plant_id>.jpg` (a small JPEG, under 300 KB, committed with the batch because it is the evidence for the point). The evidence markdown links it.
- The agent's own mosaics under `work/` are scratch and are not committed; the note describes what was seen in words.

## What is staged

An `updates` record with `applies_to_all_units: true` and `fields` holding `Latitude`, `Longitude` and `Location accuracy` (and `City` or the county when filled from the same document), `refs` under `Location Data Source` (the document, if any, and the pin link), and these optional fields, all written by the agent in the shard and passed through by `assemble_state.py` (`staged_json_schema.md`):

| field | type | meaning |
|---|---|---|
| `location_method` | str | `address`, `site_reference`, `dataset`, `map`, or `imagery` (an operating plant placed by the satellite look alone) |
| `location_moved_m` | int | distance from GEM's current point in meters, blank when GEM had none |
| `location_control_points` | list | `map` only: each control point as `{"feature": "...", "px": [x, y], "lat": .., "lon": ..}` plus `fit_m`, the fit error in meters |
| `location_image` | str | `map` only: the batch-relative path of the saved render |
| `location_needs_review` | bool | the first agent asked for a second look (`build_sweep_args.py --location-review`); the review card shows a "needs a second look" chip |

The shard carries them in a top-level `location` object (`method`, `moved_m`, `control_points`, `fit_m`, `image`, `needs_review`, `review_note`); `assemble_state.py` recomputes `location_moved_m` from the export, adds the pin link to the refs when the agent left it out, and records a verification for the pin link by construction (it opens on the staged point; `url_verifier.py` cannot read a map page). A second-look shard written to `shards/<plant_id>.review.json` replaces the first shard's location and its location questions; nothing else in the first shard changes.

The `researcher_notes` text says, in plain words, which rung of the ladder worked, what the document says about the site, what the satellite picture showed, and how far the point moved. The `action` tells the human to enter the coordinates, set the accuracy, and add the links to the Location Data Source box, keeping the links already there.

## The gate

`state_gate.py` gains a hard gate `location`:

- an `exact` value has at least three decimals and a note that says the point was seen in imagery or placed on a named parcel;
- a staged point in a US state sits inside that state's bounding box (`geo.US_STATE_BBOX`, an offline check, since the gate has no network); for a country scope the check is the reviewer's, on the review card's satellite panel;
- `location_method` names a rung of the ladder (`address`, `site_reference`, `dataset`, `map`, `imagery`);
- a move of more than 2 km from an existing point needs the note to say why GEM's point was wrong;
- a `map` method record carries `location_control_points` with a `fit_m` under 150, and its `location_image` file exists;
- `Latitude` and `Longitude` are staged together, with `Location accuracy`, and on every unit row of the plant (`applies_to_all_units`, `sibling_unit_ids` covering the index's units, `sibling_current` holding the three columns per sibling). Older per-column coordinate records from before the step only need to cover the three columns between them.

`tests/test_location_gate.py` and `tests/test_location_assemble.py` exercise the gate and the assembler on synthetic batches.

Everything else is the usual: `verified`, `orphans`, `headers`, `cell prose`, and `notes`.

## Who does what (model use)

The user-level rule applies: the cheapest model that is genuinely good enough, chosen at dispatch time, never pinned (Baird 2026-10-20 for this step in particular).

- **No model at all** for selection, geocoding, tile fetching, link building, the gate and the workbook. Those are scripts.
- **The per-plant sweep agent, Sonnet or Haiku**, runs rungs 1 to 3 from a clear brief: find the address or site sentence, geocode it, fetch the picture, and describe what it sees. For an operating plant with an obvious footprint this is routine. When the picture is ambiguous, when two candidate sites fit the document, or when only a map is available, the agent does not guess: it writes `location_needs_review: true` in the shard with the document link, the page number of the map, and what it found so far, and leaves the coordinate alone.
- **A second pass, Opus or Fable, only for the plants handed back.** `build_sweep_args.py --location-review` collects the handed-back plants into a short sweep whose agents do the georeferencing (rung 4) and the ambiguous site calls, with the first agent's notes in the brief. This pass is expected to be a handful of plants per scope. Judging a site plan against a satellite picture and choosing control points is the judgment-heavy part; nothing else in the step is.
- **The main loop** keeps the scope calls: whether a move over 2 km is right, whether a proposal's parcel is really known, and the review in the app.

## What the step never does

- Never reopens an `exact` plant.
- Never stages a coordinate from a geocoder alone on a plant that already has one; a geocode without an imagery check or a document is a note, not an edit.
- Never fills `Latitude` or `Longitude` with a town center for a plant whose site is unknown; a town is a `City` fill plus `approximate`, and only when the box is blank.
- Never cites gem.wiki, globalenergymonitor.org, Wikipedia's coordinates, or any map site that republishes GEM; those are for finding leads only. OpenStreetMap is a lead too, except as a geocoder result the agent then checked in imagery.
- Never changes a per-unit location; GEM locations are plant-level.
