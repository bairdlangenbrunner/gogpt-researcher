# IBAMA RAPP emissions reports matched to 10 operating gas plants (Brazil pilot)

Run 2026-09-18. This pilot joins IBAMA's annual air-emission reports (RAPP) to
10 of the operating plants in `../coverage/brazil.csv`, to test the join
before running it on all 50. The data is in
[`brazil_rapp_pilot_20260918.csv`](brazil_rapp_pilot_20260918.csv), one row per
plant, year, pollutant and CNPJ. [`brazil_rapp_pilot_20260918.py`](brazil_rapp_pilot_20260918.py)
rebuilds it from the RAPP file.

Sources (full list in `../sources/downloads.csv`):
- RAPP: https://dadosabertos.ibama.gov.br/dados/RAPP/emissoesPoluentesAtmosfericos/relatorio.csv
- ANEEL SIGA: owner CNPJ for each plant.
- Branch addresses: the Receita Federal CNPJ registry, read through
  `https://brasilapi.com.br/api/cnpj/v1/<cnpj>`.

## Result

| Plant | MW | Reporting CNPJ | Match | Years with NOx | NOx range (t) | Method | Usable? |
|---|---|---|---|---|---|---|---|
| GNA I | 1,338 | 23.449.511/0001-90 (UTE GNA I) | clean | 2021–24 | 301–1,637 | measured | **yes** |
| Norte Fluminense | 827 | 03.258.983/0002-30 (Macaé branch) | clean | 2013–25 | 5–1,841 (2013: 6,503) | estimated | **yes**, 2013 suspect |
| Termomacaé | 922 | 02.290.787/0001-07 (Termomacaé Ltda) | clean | 2013–24 | 108–8,392 | calculated | **yes** |
| Governador Leonel Brizola (Termorio) | 989 | 33.000.167/0092-49 (Petrobras, Campos Elíseos, Duque de Caxias) | probable | 2013–25 | 1,083–9,039 | calculated | **yes**, if the branch is confirmed |
| Porto de Sergipe | 1,593 | 23.758.522/0001-52 (CELSE, Barra dos Coqueiros) | clean | 2019–22 | 166–3,008 | calc./estimated | **yes**, but 2023 is a zero and 2024–25 are missing |
| Parnaíba complex | 1,906 | five CNPJs (below) | complex-sum | 2015–24 | 175–2,225 | est. to 2019; measured NOx/CO 2020–24 | **yes**, as a complex total |
| Mauá 3 | 591 | 17.957.780/0007-50 (Amazonas GT) to 2020; 00.350.763/0012-15 (J&F) 2025 | clean | 2018–20, 2025 | 8–136 | est. / measured | **no**: too low for a baseload plant |
| Termopernambuco | 533 | 03.795.050/0001-09 and /0002-81 | reported-zero | — | 0.00 every year, 2013–24 | estimated | **no** |
| Uruguaiana | 640 | 01.600.202/0001-37 (Âmbar Sul); J&F /0025-30 in 2025 | reported-zero | 2013 (53 t) | 0.00 from 2015 | measured | **no** |
| Karkey 013 | 259 | Karpowership 43.854.903/xxxx | none | — | — | — | **no**: no RAPP filing under any activity |

Five plants have a usable NOx series, and two more have partial ones (Porto de
Sergipe and Parnaíba). Three are unusable: two file zeros and one does not
file. No match was shared with another plant: every CNPJ used here covers a
single plant or complex.

## How each match was made

- **Exact CNPJ from SIGA:** GNA I, and Parnaíba II and Parnaíba GC.
- **Same CNPJ root, branch in the plant's town:**
  - Norte Fluminense: SIGA gives HQ `/0001-59`; the report comes from Macaé branch `/0002-30`.
  - Termopernambuco: both branches are in Ipojuca; `/0002-81` is at the Suape port complex.
  - Termorio: the only Petrobras thermal-generation branch in Duque de Caxias. The
    REDUC refinery next door reports under a different branch, `/0088-62`, as a
    refinery. The registry gives the branch no plant name, so this match is
    **probable**, not confirmed.
- **Operator rather than SIGA owner, found by name and town:**
  - Porto de Sergipe: SIGA lists Eneva S.A.; the plant reports as CELSE.
  - Termomacaé: SIGA lists Petrobras; the plant reports as its own company, Termomacaé Ltda.
  - Uruguaiana: SIGA lists J&F S.A.; the plant reports as Âmbar Sul.
- **Registry branch name:** Mauá 3.
  - `17.957.780/0007-50` is registered as "Usina Termelétrica de Mauá 3" (closed).
  - `00.350.763/0012-15` is "UTE Mauá 3" (J&F, opened 2024-09-05).
  - The other Amazonas GT and J&F branches in Manaus are Aparecida, Mauá (the old
    plant), Jaraqui, Tambaqui, Pirarucu, Tucunaré and Cristiano Rocha. None is
    counted here.
- **Parnaíba complex:** one row per CNPJ, summed by year:
  - Parnaíba I 11.744.699/0001-10 (2013–19)
  - Parnaíba II 14.578.002/0001-77 (2014–24)
  - Parnaíba III 10.536.701/0001-01 (2013–18)
  - Parnaíba IV 15.842.091/0001-80 (2013–18)
  - Parnaíba Geração e Comercialização 15.743.303/0001-71 (2020–24)

  The earlier CNPJs stop once PGC starts, so the years do not overlap.
- **Not used:**
  - Eneva's Rio de Janeiro HQ (`04.423.567/0001-21`) filed a thermal report for
    2024 of 24 t NOx. That is far too small for Porto de Sergipe, so it is not
    attributed.
  - "Âmbar Uruguaiana Energia" reports from Candiota, which is a different plant.

## Checks

- **GNA I test values reproduced:** NOx 1,294.49 / 301.25 / 1,249.85 /
  1,637.34 t for 2021–24, all measured.
- **Size check.** Column `t_per_gwh_full_cf` in the CSV divides each year's
  tonnes by what the plant would generate running flat out all year
  (MW × 8,760 h). That is the lowest the plant's true intensity can be. Real
  capacity factors are well below 100%, so the true intensity is higher.
  - **No figure goes above 2 t NOx per GWh**, so none is impossible for gas.
  - Termorio (2013–15) and Termomacaé (2014–15) are **about 1 t/GWh even at
    full load**, so the real figure is higher still. For Termomacaé, open-cycle
    LM6000 turbines without dry low-NOx burners, that is plausible. For
    Termorio, a combined-cycle plant, it is high and needs checking against
    generation. Both are Petrobras "calculated" figures with a fixed CO:NOx
    ratio (0.268), which points to an emission factor applied to fuel burned,
    not a measurement.
  - **Norte Fluminense 2013** (6,503 t) is 3.5× the next year's figure. That is
    suspect until generation data shows whether 2013 dispatch was that much higher.
  - **GNA I CO 2023** (4,037 t, against 14–320 t in other years) is an outlier.
  - **Mauá 3** reports 8–136 t NOx. That is 0.01–0.03 t/GWh even at full load,
    and Manaus runs this plant as baseload. These are not credible.
- **Zeros and placeholders.** `value_class` in the CSV marks both:
  - `reported-zero`: the operator filed 0.00.
  - `placeholder`: every pollutant that CNPJ filed that year is 0.01–0.05 t,
    e.g. Parnaíba 2013–14. These are start-up entries, not measurements.

  Neither counts as data. A lone 0.01 t SOx next to real NOx is kept as a
  value: gas plants emit almost no SO2.
- **Pollutant coverage:** NOx is the most complete; CO is close behind; PM and
  SOx are filed only by Parnaíba, Termorio and Termomacaé, plus one
  Uruguaiana PM figure (2013). This matches IEMA's
  verdict: NOx mostly usable, SOx and PM mostly not.

## What this means for the full join

- Taking the CNPJ straight from SIGA fully resolves **one plant in ten**
  (GNA I). It finds part of Parnaíba and Termopernambuco's zeros. SIGA gives the owner or holding company; RAPP is filed by the
  operating company or the plant's own branch. Every other match needed a
  search by name and town, or a lookup in the CNPJ registry.
- The CNPJ registry (via BrasilAPI) names the plant for recently opened
  branches, e.g. J&F's Manaus plants. It is the quickest way to settle which
  branch is which. Petrobras branches carry no plant name.
- To separate real low-output years from bad filings, the ONS generation data
  is the next dependency. It would also turn Termorio and Termomacaé into real
  intensities.
