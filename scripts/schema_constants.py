"""
Shared GOGPT column-name sets and controlled vocabulary — canonical source for
the read-only column lists and enum values used by pull_gem_db.py,
scope_filter.py, worklist.py, qc_checks.py, and build_review_package.py.

Column names are the exact gem_export_gogpt.csv header strings (the 91-column
layout in gem-db-ops/gem_all_fields.py GOGPT_COLUMNS); enum values follow the
GOGPT Editing Manual (March 2026) — see docs/reference/controlled_vocab.md and
docs/reference/lifecycle_rules.md. Enum casing in the live export can drift;
compare case-insensitively and update here if verification against a fresh
pull shows different display strings.
"""

# GEM-computed / DB-assigned columns. The build script must never write these
# (a blank here is not actionable research-wise — the backend assigns or
# recomputes them; IDs are auto-generated on record creation).
COMPUTED_COLUMNS = {
    "GEM location ID", "GEM unit ID",
    "Wiki URL",
    "Last Updated", "Researcher", "Research status",
    "Operator GEM Entity ID", "Owner(s) GEM Entity ID", "Parent GEM Entity ID",
    "Parent(s)",  # derived from the owner entity graph
    "Linked Projects",
    "Owner Share Imputed", "Parent Share Imputed",  # Y/blank flags set by the pull
    "Subregion", "Region",  # derived from Country/Area
}

# "Do not research" per the Editing Manual (hydrogen lane is explicitly
# deprioritized) — never write or flag as missing.
OUT_OF_SCOPE_COLUMNS = {
    "Hydrogen capable?", "Hydrogen Notes", "Hydrogen Data Source",
    "H2 ready turbine (%)?", "MOU for H2 supply?", "Contract for H2 supply?",
    "Financing for supply of H2?",
    "Co-located with electrolyzer/H2 production facility?",
    "What % of H2 blending currently?", "H2 Criteria Data Source",
}

READ_ONLY_COLUMNS = COMPUTED_COLUMNS | OUT_OF_SCOPE_COLUMNS

# --- Status vocabulary (lifecycle_rules.md) --------------------------------
# In-development statuses are the research priority; inferred variants are
# staged by the researcher after the worklist.py date-arithmetic flags them.
# The live DB stores the inferred variants with a plain hyphen
# ("shelved - inferred 2 y"); the Editing Manual prints an en-dash. Accept both.
STATUSES_IN_DEVELOPMENT = {"announced", "pre-construction", "construction"}
STATUSES_OPERATING = {"operating"}
STATUSES_PAUSED = {"shelved", "shelved - inferred 2 y",
                   "shelved – inferred 2 y", "mothballed"}
STATUSES_ENDED = {"cancelled", "cancelled - inferred 4 y",
                  "cancelled – inferred 4 y", "retired"}
STATUSES = (STATUSES_IN_DEVELOPMENT | STATUSES_OPERATING
            | STATUSES_PAUSED | STATUSES_ENDED)

# Start year must be blank (or Planned-flagged projection) for these:
STATUSES_NO_START_YEAR = {"shelved", "shelved - inferred 2 y",
                          "shelved – inferred 2 y",
                          "cancelled", "cancelled - inferred 4 y",
                          "cancelled – inferred 4 y"}

# --- Technology vocabulary --------------------------------------------------
# Turbine/Engine Technology display values (abbreviation -> meaning).
TECHNOLOGIES = {
    "CC": "combined cycle",
    "GT": "gas turbine (frame-type, simple cycle)",
    "AGT": "aeroderivative gas turbine",
    "ST": "steam turbine",
    "IC": "internal combustion (reciprocating engines)",
    "ICCC": "internal combustion in combined cycle",
    "ISCC": "integrated solar combined cycle",
    "AFC": "Allam-Fetvedt Cycle",
}

# The live export stores the LONG form for the common technologies and the
# abbreviation only for the rare ones (observed 2026-07-27: "combined cycle",
# "gas turbine", "steam turbine", "internal combustion", "unknown", plus
# ICCC/ISCC/AFC). Accept both forms everywhere.
TECHNOLOGY_LONG_FORMS = {
    "combined cycle", "gas turbine", "aeroderivative gas turbine",
    "steam turbine", "internal combustion",
    "internal combustion combined cycle", "integrated solar combined cycle",
    "allam-fetvedt cycle", "unknown",
}

# --- Fuel vocabulary ---------------------------------------------------------
FUELS_FOSSIL_GAS = {
    "natural gas", "LNG", "coalbed methane", "gaseous propane",
    "waste heat from natural gas",
}
FUELS_FOSSIL_LIQUIDS = {
    "crude oil", "diesel", "fuel oil", "gasoline", "heavy fuel oil",
    "jet fuel", "kerosene", "light fuel oil", "LPG", "naphtha",
    "petroleum coke", "waste/other oil",
}
FUELS_BYPRODUCT = {"blast furnace gas", "coke oven gas"}
FUELS_HYDROGEN = {"hydrogen"}
GOGPT_FUELS = (FUELS_FOSSIL_GAS | FUELS_FOSSIL_LIQUIDS
               | FUELS_BYPRODUCT | FUELS_HYDROGEN)

# The live export writes fuel cells as comma-separated "category: detail"
# tokens ("fossil gas: natural gas, fossil liquids: fuel oil"). Category
# membership decides scope; the detail sets above cover bare-detail values
# (as the Editing Manual writes them, e.g. in staged records).
GOGPT_FUEL_CATEGORIES = {"fossil gas", "fossil liquids", "industrial by-product"}
NON_GOGPT_FUEL_CATEGORIES = {"coal", "bioenergy", "biomass", "waste",
                             "nuclear", "geothermal", "solar", "wind", "hydro"}

# Fuel tokens that indicate a NON-GOGPT combustion unit (coal/GCPT,
# bioenergy/GBPT) — used only by scope_filter.py's offline fallback.
NON_GOGPT_FUEL_HINTS = {
    "coal", "bituminous", "subbituminous", "sub-bituminous", "lignite",
    "anthracite", "coal refuse", "waste coal",
    "biomass", "biogas", "bagasse", "wood", "agricultural", "municipal solid waste",
}

# --- Capacity inclusion thresholds (MW) -------------------------------------
CAPACITY_THRESHOLD_MW = 50        # global floor (nameplate, per unit / per set)
CAPACITY_THRESHOLD_EU_UK_MW = 20  # EU + UK use a lower per-unit bar

EU_UK_COUNTRIES = {
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia",
    "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany",
    "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania",
    "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania",
    "Slovakia", "Slovenia", "Spain", "Sweden", "United Kingdom",
}

# --- Inferred-status thresholds (years since last evidence of activity) -----
SHELVED_INFERRED_YEARS = 2    # announced/pre-con/construction -> shelved (inferred)
CANCELLED_INFERRED_YEARS = 4  # same disappearance test -> cancelled (inferred)

# --- Research fields a state-agent subagent reports on -----------------------
# Exact CSV headers; imported by build_state_brief.py (brief header) and the
# sweep/assemble tooling. Plant-level fields apply to every unit of the plant.
RESEARCH_FIELDS = [
    "Status", "Capacity (MW)", "Fuel", "Turbine/Engine Technology",
    "Equipment Manufacturer/Model", "Number Of Engines", "Capacity Per Engine",
    "Start year", "Retired year", "Planned retire", "Cancellation year",
    "Latest Activity", "Status Detail", "CHP", "Owner(s)", "Operator(s)",
    "Latitude", "Longitude", "Location accuracy", "Captive industry use",
    "Captive industry type", "Captive non-industry use",
    "Conversion/replacement?",
]

# --- Free-text boxes that are only ever added to ------------------------------
# Status Detail and Notes are running logs in the GEM web form, newest entry at
# the top. A staged value for either is the new text placed ABOVE the text
# already there, which stays word for word; never a rewrite, never a deletion
# (Baird 2026-10-07). build_review_package.additive_value composes the cell,
# assemble_state.py uses it, and state_gate.py (gate `additive`) plus
# build_review_package.validate reject anything else.
ADDITIVE_TEXT_COLUMNS = ("Status Detail", "Notes")

# --- Boxes that carry their own source link -----------------------------------
# A Status Detail entry carries its source link in the text itself ("... target
# operation June 2029: https://..."), the way GEM researchers already write it.
# Its link never goes to Status Data Source, which feeds the unit's milestone
# and scheduled-event timeline (Baird 2026-10-08). ref_col_for maps such a
# column to itself, so a staged record keys the link under the column's own
# name and the build never merges it into a Data Source cell.
INLINE_SOURCE_COLUMNS = ("Status Detail",)
