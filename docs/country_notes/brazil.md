# Brazil

Comprehensive official database (ANEEL SIGA) covering existing, proposed, and
under-construction plants, plus a useful secondary channel via public energy
auction records — but SIGA's coordinates need spot-checking, not blind trust.

## Regulators & official sources

- **ANEEL (Agência Nacional de Energia Elétrica) — SIGA (Sistema de
  Informações de Geração da ANEEL)** — excellent, comprehensive power-plant
  database, downloadable. Several access points have been used:
  - [Power BI view](https://app.powerbi.com/view?r=eyJrIjoiNjc4OGYyYjQtYWM2ZC00YjllLWJlYmEtYzdkNTQ1MTc1NjM2IiwidCI6IjQwZDZmOWI4LWVjYTctNDZhMi05MmQ0LWVhNGU5YzAxNzBlMSIsImMiOjR9)
  - [dados.gov.br dataset page](https://dados.gov.br/dataset/siga-sistema-de-informacoes-de-geracao-da-aneel)
  - [UFSC mirror](https://energiasolarfotovoltaica.ufsc.br/siga-aneel/)
  - [ANEEL SIGEL download page](https://sigel.aneel.gov.br/Down/)
  - Filtering approach used previously: query by "usina" (plant) type =
    "Usina termelétrica," then export the attribute table to CSV (via the
    three-dot "View in Attribute Table" → Options → "Export all to CSV" in
    the map-based tools). This surfaced 3,500+ thermal power plants in one
    prior pull.
  - **Status field**: the most common SIGA status value is **"DRO"**, which
    appears to correspond to a permit to participate in the power market
    (a registration/dispatch-authorization step) rather than an operating
    determination — see
    [ANEEL's own explainer](https://www.gov.br/pt-br/servicos/obter-despacho-de-registro-de-recebimento-de-outorga-de-centrais-geradoras-fotovoltaicas-termeletricas-ou-eolicas)
    and an [example DRO record](https://www.aneel.gov.br/outorgas/geracao/-/asset_publisher/mJhnKIi7qcJG/content/ute-central-geradora-termeletrica-ren-390-2009-/655808?inheritRedirect=false).
    A team note guessed plants must obtain this permit at some stage in the
    planning process, before construction begins — worth confirming with
    ANEEL documentation rather than treating as settled.
- **CCEE (Câmara de Comercialização de Energia Elétrica)** — publishes energy
  auction registrant and winner lists at
  [ccee.org.br/mercado/leilao-mercado](https://www.ccee.org.br/mercado/leilao-mercado),
  which is a good way to see the full set of gas plants competing in a given
  auction. Sample registrant lists and winner-summary PDFs were cited in the
  source doc from 2021 auctions — search CCEE's site for current-cycle
  auction documents rather than relying on those specific 2021 links.

## Key operators & utilities

- No single dominant thermal generator equivalent to Eskom (South Africa) or
  EVN (Vietnam) — Brazil's gas fleet is spread across many IPPs that surface
  through the ANEEL/CCEE auction process rather than through one or two
  utility websites. Identify relevant sponsors plant-by-plant via SIGA and
  auction records rather than expecting a single company page to cover the
  fleet.

## Preferred sources (beyond the global roster)

- ANEEL SIGA and CCEE auction records (above) are the primary preferred
  sources for this country — both official and comprehensive.

## Research tips

- When pulling SIGA data, keep the "DRO" status distinction in mind: a plant
  with DRO status is not necessarily operating or even under construction —
  confirm what stage of development it actually reflects before mapping it
  to a GEM status.
- CCEE auction winner/registrant PDFs are a good way to catch new gas
  proposals that haven't yet surfaced in SIGA, since auction participation
  often precedes full ANEEL registration.

## Gotchas

- **SIGA coordinate accuracy**: SIGA states coordinates for plants and
  sometimes flags them as approximate — but even where coordinates are
  presented as exact, spot-checking roughly a dozen previously found **no
  power plant at the stated location more than half the time**. Always
  verify SIGA coordinates against satellite imagery or another source before
  trusting them; don't take "exact" at face value.

## Open items

- Confirm the current interpretation of SIGA's "DRO" status against ANEEL
  documentation (rather than the team's working guess that it precedes
  construction).
- Re-run a coordinate spot-check on any current SIGA extract before relying
  on its location data — the ~50%+ miss rate found previously may or may not
  still hold.

## Update notes

- *2026-07-27* — seeded from GEM's team-wide "Gas/oil power plant data
  sources - by country" doc. SIGA access links and CCEE auction document
  links are 2021-vintage; as of 2026, re-verify.
