# South Africa

Small in plant count but high-stakes for data quality: the country's main
gas/liquid-fuel stations are dual-fuel, and multiple otherwise-reliable
datasets have miscategorized them as simply "gas-fired" when they are
running mostly (or entirely) on diesel.

## Regulators & official sources

- **Department of Energy / Department of Mineral Resources and Energy** —
  publishes an annual South Africa Energy Sector Report
  ([2019 edition](http://www.energy.gov.za/files/media/explained/2019-South-African-Energy-Sector-Report.pdf)),
  and the [Integrated Resource Plan (IRP) 2019](http://www.energy.gov.za/files/irp_frame.html),
  which lists power plants:
  - Table 8: Municipal and Private Generators (name, capacity, planned
    decommissioning year)
  - Table 9: Eskom Generators — cites Eskom's 2018 Integrated Report; use the
    current Eskom Integrated Report instead (2019 report was released Mar 31,
    2019; check for the latest edition rather than assuming that's current).
- **Eskom** — the dominant utility, generating roughly 90% of the country's
  electricity per the 2019 Energy Sector Report.
  - [Power station GPS coordinates](http://www.eskom.co.za/Whatweredoing/ElectricityGeneration/PowerStations/Pages/Power_Station_GPS_Coordinates.aspx)
  - [Map of Eskom power stations (PDF)](http://www.eskom.co.za/Whatweredoing/ElectricityGeneration/PowerStations/Pages/Map_Of_Eskom_Power_Stations.aspx) —
    shows Acacia (171 MW), Port Rex (171 MW), Ankerlig (1,338 MW), and
    Gourikwa (746 MW).
  - [Facts and Figures page](http://www.eskom.co.za/AboutElectricity/FactsFigures/Pages/Facts_Figures.aspx) —
    detailed descriptions of Acacia, Port Rex, Ankerlig, Gourikwa.
  - [Eskom Integrated Reports (main page)](http://www.eskom.co.za/OurCompany/Investors/IntegratedReports/Pages/Annual_Statements.aspx) —
    check for the current year's edition rather than the 2018/2019 vintage
    cited in the IRP 2019.

## Key operators & utilities

- **Eskom** — effectively the only utility that matters for gas/liquid-fuel
  generation; under "Gas/liquid fuel turbine stations" it lists exactly 4
  power stations: **Acacia, Ankerlig, Gourikwa, Port Rex**. This is a short,
  closed list — there isn't a long tail of smaller gas IPPs to chase down.

## Preferred sources (beyond the global roster)

- [Power Africa (AfDB)](https://powerafrica.opendataforafrica.org/) — key
  source for identifying gas plants under construction/proposed; Google
  Maps-based location data.
- [African Energy](https://www.africa-energy.com/database) — potentially more
  current status info than Power Africa, includes primary fuel and location.
- "South Africa Gas Master Plan" (2019, EPCM Holdings) — came up as an
  example of gas-industry-hype framing around South African gas plans in a
  May 2021 civil-society coalition meeting (organized in part by 350.org);
  dated, but may still hold useful detail.

## Research tips

- Given the fleet is small (4 gas/liquid stations under Eskom), prioritize
  getting these 4 exactly right over breadth — check both Eskom's own
  materials and independent/government commentary on their actual fuel mix
  each time you touch this country.
- The Eskom IRP table citing the 2018 Integrated Report is itself a flag that
  the source may be stale by the time you're reading it; always look for the
  current Eskom Integrated Report rather than trusting the year cited in a
  secondary document.

## Gotchas

- **Diesel-vs-gas miscategorization**: multiple sources (including Power
  Africa, which lists the 746 MW Gourikwa station as simply "gas-fired") have
  missed that Eskom's gas/liquid stations have in recent years been run
  predominantly on **diesel**, not gas, due to natural gas unavailability. A
  2019 government minister's remarks stated: "South Africa continues to run
  diesel plants at Ankerlig (Saldanha Bay), Gourikwa (Mossel Bay), Avon
  (outside Durban) and Dedisa (Coega IDZ), simply because of the
  unavailability of natural gas, which is cheaper than diesel."
  ([source](http://www.energy.gov.za/files/media/speeches/2019/Remarks-by-Minister-at-the-IRP2019-workshop-NCOP-28112019.pdf))
- If diesel is genuinely the primary fuel for Ankerlig, Gourikwa, Avon, and
  Dedisa, these plants may need to be excluded from (or flagged within) GOGPT
  depending on the tracker's fuel-classification rules — check current
  methodology before including/excluding on this basis, since the underlying
  fuel mix may itself have shifted since 2019.
- Treat any single source's "gas-fired" label for these four plants with
  suspicion; corroborate fuel mix year-by-year rather than assuming it's
  static.

## Open items

- Re-verify current (not 2019) fuel mix at Acacia, Ankerlig, Gourikwa, and
  Port Rex/Avon/Dedisa — diesel dependency may have changed as gas
  availability has evolved.
- Confirm which Eskom Integrated Report is current and pull plant data from
  that rather than the 2018 edition cited in IRP 2019.

## Update notes

- *2026-07-27* — seeded from GEM's team-wide "Gas/oil power plant data
  sources - by country" doc. Diesel-vs-gas fuel mix at Eskom's four
  gas/liquid stations was last confirmed as of 2019 sources; re-verify.
