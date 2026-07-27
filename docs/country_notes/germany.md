# Germany

Well-documented fleet via the federal regulator's Kraftwerksliste (power
plant list), which is comprehensive but uses its own status vocabulary that
needs mapping onto GEM status categories — get this mapping right, since it's
the single most important translation step for this country.

## Regulators & official sources

- **Bundesnetzagentur (BNA / Federal Network Agency)** —
  [Kraftwerksliste](https://www.bundesnetzagentur.de/DE/Sachgebiete/ElektrizitaetundGas/Unternehmen_Institutionen/Versorgungssicherheit/Erzeugungskapazitaeten/Kraftwerksliste/start.html) —
  lists all operating power plants plus planned extensions, dismantling, and
  closures (the distinction between "dismantling" and "closure" isn't fully
  clear from the source material — worth clarifying if it matters for a
  specific plant). Look for files under:
  - *Aktuelle Erzeugungsanlagen* (Current generation plants)
  - *Zu- und Rückbau von Kraftwerken* (Extension and dismantling of power
    plants)
  - Also releases *Genehmigung des Szenariorahmens* (Approval of the scenario
    framework), whose Anlage 1 / Annex 1 "Kraftwerksliste zum
    Szenariorahmen" appears to include both current Kraftwerksliste plants
    and proposed future plants.
  - The Gas NDP (Network Development Plan) Scenario Framework's Appendix 2
    ("List of gas power plants") draws on BDEW, BNetzA, Prognos AG, and TSO
    data to include some plants absent from the core Kraftwerksliste (e.g.
    Hagen-Kabel was cited as an example).
  - [Gas Network Development Plan map of pipelines and power plants (PDF)](https://www.bundesnetzagentur.de/SharedDocs/Downloads/EN/Areas/ElectricityGas/Gas_grid/Draft_NDP2020_2030.pdf?__blob=publicationFile&v=1) —
    figure 6 has plant-level capacities.

### BNA status → GEM status mapping

| BNA status | GEM status |
|---|---|
| in Betrieb | operating |
| vorläufig stillgelegt | operating |
| saisonale Konservierung | operating |
| Sicherheitsbereitschaft | [coal only] |
| gesetzlich an Stilllegung gehindert (Netzreserve) [legally prevented from decommissioning] | operating |
| Kohlestromvermarktungsverbot | [coal only] |
| Sonderfall (special cases) | operating |
| endgültig stillgelegt (permanently shut down) | Retired |

Re-verify this mapping periodically — it was compiled against BNA's category
set as of the early-2020s source doc; BNA could add or rename categories.

## Key operators & utilities

- **Uniper** — publishes "List of Assets" documents detailing its German
  power plant portfolio (editions seen: 2018, 2019, 2020 — check for a
  current edition rather than relying on these).

## Preferred sources (beyond the global roster)

- [Gasturbinen-Kenndaten Gasturbinen-Referenzen (ASUE, 2006)](https://asue.de/sites/default/files/asue/themen/gasturbinen/2006/broschueren/11_05_06_gasturbinenkenndaten_01.pdf) —
  table of captive industrial gas turbine units; useful for industrial/captive
  plants that may not surface in the Kraftwerksliste. Dated (2006) — treat as
  a lead to confirm current status, not a current-status source.

## Research tips

- Start with the current Kraftwerksliste "Aktuelle Erzeugungsanlagen" file
  for the operating fleet, then check "Zu- und Rückbau" for planned
  additions/retirements, then cross-reference against the Gas NDP Scenario
  Framework appendix for plants that fall outside the core Kraftwerksliste.
- Uniper's List of Assets documents are a good secondary check for
  Uniper-owned plants specifically, since Uniper's numbers may be more
  current than the last BNA snapshot for its own fleet.

## Gotchas

- The BNA→GEM status mapping table above is the load-bearing piece of this
  country's research — miscoding "vorläufig stillgelegt" (provisionally shut
  down) as anything other than "operating," for example, would misclassify a
  plant that BNA itself still counts as available.
- It's unclear from the source material what distinguishes BNA's
  "dismantling" from "closure" categories for a plant — don't assume they're
  synonymous without checking BNA's own definitions if it matters for a
  specific case.

## Open items

- Confirm the BNA status vocabulary hasn't changed since this mapping was
  compiled; re-check against a current Kraftwerksliste file.
- Find a Uniper List of Assets edition newer than 2020, if one exists.

## Update notes

- *2026-07-27* — seeded from GEM's team-wide "Gas/oil power plant data
  sources - by country" doc, including the BNA→GEM status mapping table.
  As of 2026, re-verify the mapping and Uniper asset-list currency.
