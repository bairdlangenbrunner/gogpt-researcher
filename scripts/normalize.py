"""
Canonical name normalization for countries and entities (owners/operators/
parents). Used by entity_lookup.py so matching is consistent across batches.

Without this, "TotalEnergies" vs "Total Energies" vs "Total" would be treated
as three different entities, and local-scan lookups would over- or
under-match.

The mappings are conservative — only canonicalize where there's no ambiguity.
When a new entity/country appears in a batch and isn't in the map, add it here
rather than papering over it.

Returns canonical short tags (e.g. 'totalenergies', 'qatarenergy', 'karpowership').
If the input doesn't match any known variant, returns the input lowercased
and stripped — so unknown entities still cluster against themselves.

PORTING NOTE: this is a trimmed port of the LNG Terminals tracker's
normalize.py, which also carried LNG-specific capacity-unit conversion
(mtpa/bcm/bcf — GOGPT capacity is plain MW, so that's dropped entirely) and
LNG-terminal-name matching helpers (stripping "LNG Terminal"/"FSRU"/"FLNG"
suffixes, roman-numeral canonicalization, trailing-region stripping, and
CJK-to-pinyin transliteration for terminal names) that entity_lookup.py never
used and that don't map cleanly onto GOGPT plant/unit names. Only the generic,
tracker-agnostic pieces are kept: diacritic folding, country normalization,
entity normalization (including the owner-percentage list parser and the
owner-equivalence helpers used for name matching). The entity map below was
inherited from the LNG tracker and still covers the many integrated majors and
NOCs that also own gas/oil power plants, but it also carries some
LNG-shipping/FSRU-operator entries that are dead weight for GOGPT and will
need supplementing with GOGPT-specific owners (IPPs, utilities, EPC firms) as
they're encountered.
"""
import re
import unicodedata


# --- Diacritic folding (Latin-script matching only) ---
#
# Some source datasets write plant/country names WITHOUT diacritics ("Sao
# Paulo", "Turkiye"), while GEM stores them WITH ("São Paulo", "Türkiye"). A
# matcher comparing normalized token forms needs accent-variant names to fold
# to the same ASCII spelling or the same entity lands in two buckets.
#
# NFKD decomposes most accented Latin letters into base + combining mark, which we
# then drop. A handful of letters carry the diacritic in the codepoint itself and
# do NOT decompose under NFKD (ø, đ, ł, ı, ß, ...) — those need an explicit map.
_DIACRITIC_FALLBACKS = {
    "ø": "o", "Ø": "O",
    "đ": "d", "Đ": "D",
    "ð": "d", "Ð": "D",
    "ł": "l", "Ł": "L",
    "ı": "i", "İ": "I",
    "ß": "ss",
    "æ": "ae", "Æ": "AE",
    "œ": "oe", "Œ": "OE",
    "þ": "th", "Þ": "TH",
}


def _strip_diacritics(s):
    """Fold Latin diacritics to their ASCII base letters.

    NFKD-decompose, drop combining marks (Unicode category 'Mn'), and apply an
    explicit fallback map for letters NFKD leaves intact (ø→o, đ→d, ł→l, ı→i,
    ß→ss, ...). CJK and other non-Latin codepoints are untouched: NFKD does not
    introduce combining marks for them and they aren't in the fallback map, so
    they pass through unchanged.
    """
    if s is None:
        return ""
    s = str(s)
    # Explicit fallbacks first (these don't decompose under NFKD).
    if any(c in _DIACRITIC_FALLBACKS for c in s):
        s = "".join(_DIACRITIC_FALLBACKS.get(c, c) for c in s)
    decomposed = unicodedata.normalize("NFKD", s)
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


# --- Country normalization ---

# Canonical country names (left side) and their variants
_COUNTRY_MAP = {
    "united states": "united states",
    "usa": "united states",
    "us": "united states",
    "u.s.": "united states",
    "u.s": "united states",
    "u.s.a.": "united states",
    "u.s.a": "united states",
    "america": "united states",
    "united kingdom": "united kingdom",
    "uk": "united kingdom",
    "great britain": "united kingdom",
    "russia": "russia",
    "russian federation": "russia",
    "south korea": "south korea",
    "korea, south": "south korea",
    "republic of korea": "south korea",
    "korea": "south korea",
    "north korea": "north korea",
    "democratic people's republic of korea": "north korea",
    "dprk": "north korea",
    "china": "china",
    "people's republic of china": "china",
    "prc": "china",
    "taiwan": "taiwan",
    "republic of china": "taiwan",
    "japan": "japan",
    "uae": "united arab emirates",
    "u.a.e.": "united arab emirates",
    "united arab emirates": "united arab emirates",
    "ivory coast": "côte d'ivoire",
    "cote d'ivoire": "côte d'ivoire",
    "côte d'ivoire": "côte d'ivoire",
    "burma": "myanmar",
    "myanmar": "myanmar",
    "cape verde": "cape verde",
    "cabo verde": "cape verde",
    "swaziland": "eswatini",
    "eswatini": "eswatini",
    "trinidad": "trinidad and tobago",
    "trinidad and tobago": "trinidad and tobago",
    "congo": "republic of the congo",
    "republic of the congo": "republic of the congo",
    "congo-brazzaville": "republic of the congo",
    "dr congo": "democratic republic of the congo",
    "drc": "democratic republic of the congo",
    "democratic republic of the congo": "democratic republic of the congo",
    "dominican": "dominican republic",
    "dominican republic": "dominican republic",
    "papua new guinea": "papua new guinea",
    "png": "papua new guinea",
    "north macedonia": "north macedonia",
    "macedonia": "north macedonia",
    "czech republic": "czech republic",
    "czechia": "czech republic",
    "turkey": "türkiye",
    "türkiye": "türkiye",
    "turkiye": "türkiye",
    "viet nam": "vietnam",
    "vietnam": "vietnam",
    # Region/area names that GEM uses
    "puerto rico": "puerto rico",
    "hong kong": "hong kong",
    "macao": "macao",
    "macau": "macao",
}


# --- Entity normalization ---
_ENTITY_MAP = {
    # Integrated majors
    "totalenergies": "totalenergies",
    "total": "totalenergies",
    "total energies": "totalenergies",
    "total sa": "totalenergies",
    "shell": "shell",
    "royal dutch shell": "shell",
    "shell plc": "shell",
    "bp": "bp",
    "british petroleum": "bp",
    "bp plc": "bp",
    "exxonmobil": "exxonmobil",
    "exxon mobil": "exxonmobil",
    "exxon": "exxonmobil",
    "chevron": "chevron",
    "chevron corp": "chevron",
    "conocophillips": "conocophillips",
    "conoco phillips": "conocophillips",
    "eni": "eni",
    "eni spa": "eni",
    "equinor": "equinor",
    "statoil": "equinor",
    "repsol": "repsol",
    "repsol sa": "repsol",
    "galp": "galp",
    "galp energia": "galp",

    # State-linked / NOCs
    "qatarenergy": "qatarenergy",
    "qatar energy": "qatarenergy",
    "qatar petroleum": "qatarenergy",
    "qp": "qatarenergy",
    "adnoc": "adnoc",
    "abu dhabi national oil company": "adnoc",
    "adnoc gas": "adnoc",
    "saudi aramco": "aramco",
    "aramco": "aramco",
    "petronas": "petronas",
    "petroliam nasional berhad": "petronas",
    "pertamina": "pertamina",
    "pt pertamina": "pertamina",
    "pertamina hulu": "pertamina",
    "cnpc": "cnpc",
    "china national petroleum corp": "cnpc",
    "petrochina": "cnpc",
    "sinopec": "sinopec",
    "cnooc": "cnooc",
    "china national offshore oil corp": "cnooc",
    "kogas": "kogas",
    "korea gas corporation": "kogas",
    "jera": "jera",
    "jera co": "jera",
    "inpex": "inpex",
    "inpex corp": "inpex",
    "gazprom": "gazprom",
    "gazprom export": "gazprom",
    "novatek": "novatek",
    "ngc": "ngc-trinidad",
    "national gas company of trinidad": "ngc-trinidad",
    "nlng": "nlng",
    "nigeria lng": "nlng",
    "sonangol": "sonangol",
    "sonangol ep": "sonangol",
    "sonatrach": "sonatrach",
    "egas": "egas",
    "egyptian natural gas holding": "egas",
    "egpc": "egpc",
    "egyptian general petroleum corp": "egpc",
    "pdvsa": "pdvsa",
    "petroleos de venezuela": "pdvsa",
    "ypf": "ypf",
    "enarsa": "enarsa",
    "ieasa": "enarsa",
    "petrobras": "petrobras",
    "petroleo brasileiro": "petrobras",
    "ecopetrol": "ecopetrol",
    "bapco": "bapco",
    "bapco energies": "bapco",
    "nnpc": "nnpc",
    "nigerian national petroleum corporation": "nnpc",
    "gnpc": "gnpc",
    "socar": "socar",
    "tpao": "tpao",
    "botas": "botas",

    # Floating power operators (Karpowership Powerships are gas/HFO-fired
    # floating generation, directly relevant to GOGPT — kept, unlike the
    # LNG-shipping-specific entries this map otherwise dropped)
    "karpowership": "karpowership",
    "karadeniz holding": "karpowership",

    # European utilities
    "engie": "engie",
    "gdf suez": "engie",
    "naturgy": "naturgy",
    "naturgy energy group": "naturgy",
    "gas natural fenosa": "naturgy",
    "snam": "snam",
    "snam spa": "snam",
    "fluxys": "fluxys",
    "fluxys belgium": "fluxys",
    "enagas": "enagas",
    "enagás": "enagas",
    "enagas sa": "enagas",
    "rwe": "rwe",
    "rwe ag": "rwe",
    "uniper": "uniper",
    "uniper se": "uniper",
    "national grid": "national-grid",

    # Asian state utilities / IPPs
    "tepco": "tepco",
    "tokyo electric power": "tepco",
    "chubu electric power": "chubu",
    "kansai electric": "kansai-electric",
    "kansai electric power": "kansai-electric",
    "osaka gas": "osaka-gas",
    "daigas": "osaka-gas",
    "tokyo gas": "tokyo-gas",
    "cpc corporation taiwan": "cpc-taiwan",
    "cpc": "cpc-taiwan",
    "pgn": "pgn-indonesia",
    "perusahaan gas negara": "pgn-indonesia",
    "ptt": "ptt",
    "gail": "gail-india",
    "petronet lng": "petronet",
    "petronet": "petronet",

    # North American sponsors
    "fortisbc": "fortisbc",
    "fortisbc energy": "fortisbc",
    "fortisbc energy inc": "fortisbc",

    # African
    "kosmos energy": "kosmos",
    "kosmos": "kosmos",
    "marathon": "marathon",
    "marathon oil": "marathon",
    "smhpm": "smhpm",
    "société mauritanienne des hydrocarbures": "smhpm",
    "petrosen": "petrosen",
    "enh": "enh",
    "empresa nacional de hidrocarbonetos": "enh",
}


def _normalize_input(s):
    """Lowercase, fold diacritics, strip, collapse whitespace, remove parens."""
    if s is None:
        return ""
    # Fold diacritics so accent-variant inputs ("Türkiye"/"Turkiye",
    # "Enagás"/"Enagas") collapse to one form before map lookup / clustering.
    s = _strip_diacritics(str(s)).lower().strip()
    # Remove parenthetical content
    s = re.sub(r"\([^)]*\)", "", s).strip()
    # Strip trailing periods
    s = s.rstrip(".")
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s)
    return s


# _normalize_input folds diacritics, so a map key carrying one (e.g. "türkiye",
# "côte d'ivoire", "enagás") would never be hit by a lookup. Pre-fold the keys so
# both the accented and unaccented spellings resolve. Canonical VALUES keep their
# preferred display form (with diacritics) — they're only compared for equality,
# and both accent-variants now route to the same value.
_COUNTRY_MAP_FOLDED = {_strip_diacritics(k): v for k, v in _COUNTRY_MAP.items()}
_ENTITY_MAP_FOLDED = {_strip_diacritics(k): v for k, v in _ENTITY_MAP.items()}


def normalize_country(s):
    """Return canonical country name. Unknown inputs returned lowercased/stripped."""
    norm = _normalize_input(s)
    if not norm:
        return ""
    if norm in _COUNTRY_MAP_FOLDED:
        return _COUNTRY_MAP_FOLDED[norm]
    return norm


def normalize_entity(s):
    """Return canonical entity tag. Unknown inputs returned lowercased/stripped."""
    norm = _normalize_input(s)
    if not norm:
        return ""
    # Exact match first (keys pre-folded so accent variants both resolve).
    if norm in _ENTITY_MAP_FOLDED:
        return _ENTITY_MAP_FOLDED[norm]
    # Substring match (longer keys first to avoid false positives)
    for key in sorted(_ENTITY_MAP_FOLDED.keys(), key=len, reverse=True):
        if norm.startswith(key + " ") or norm == key or " " + key + " " in " " + norm + " ":
            return _ENTITY_MAP_FOLDED[key]
    return norm


def parse_entity_list(s):
    """Parse a comma- or semicolon-separated entity list with optional percentages.
    Returns list of {entity, pct} dicts; pct is None if not present.

    Examples:
        "ENI 50%, EGAS 40%, EGPC 10%" -> [{eni,50},{egas,40},{egpc,10}]
        "Cheniere"                     -> [{cheniere,None}]
        "Shell, Total, BP"             -> [{shell,None},{totalenergies,None},{bp,None}]
    """
    if not s:
        return []
    s = str(s).strip()
    # A SPACED slash joins co-owners ("New Fortress Energy / Celba"). A TIGHT
    # slash is part of one name ("SIGER/ERGIS Group", "Torp Technology A/S")
    # and never splits.
    parts = re.split(r"[,;]|\s+/\s+", s)
    out = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Try to extract a trailing percentage in (...) OR [...] brackets, or bare.
        # GEM owner cells use square brackets ("Exxon Mobil Corp [24.15%]");
        # other sources use round parens or none ("ExxonMobil 30%") — accept
        # all so the entity name is recovered cleanly either way.
        m = re.search(r"(.+?)\s*[\(\[]?(\d+(?:\.\d+)?)\s*%[\)\]]?\s*$", part)
        if m:
            entity = m.group(1).strip().rstrip("([").strip()
            pct = float(m.group(2))
        else:
            entity = part
            pct = None
        canonical = normalize_entity(entity)
        out.append({"entity": canonical, "raw": entity, "pct": pct})
    return out


# ---------------------------------------------------------------------------
# Owner equivalence (name-matching helper for entity_lookup.py and any future
# dedup logic — one definition so callers agree on what "the same owner" means)
# ---------------------------------------------------------------------------

# Legal-form suffix tokens dropped before comparing owner names by core tokens —
# "Gasum" == "Gasum Oy", "Toho Gas" == "Toho Gas Co Ltd". "consortium" is here
# too: it's a legal/structural descriptor, not an identifying token.
_OWNER_LEGAL_SUFFIX = {
    "co", "ltd", "corp", "inc", "sa", "ab", "llc", "group", "bhd", "oy", "pvt",
    "sas", "plc", "gmbh", "as", "spa", "nv", "kk", "ag", "holding", "holdings",
    "company", "limited", "corporation", "lp", "slu", "pte", "the", "of",
    "consortium", "ase", "asa", "oao", "pao", "ojsc", "jsc", "srl", "bv"}

# Short-form / acronym aliases matched bidirectionally on core tokens.
_OWNER_ALIAS_PAIRS = [
    ({"petronas"}, {"petroliam", "nasional"}),
    ({"kogas"}, {"korea", "gas"}),
    ({"sinopec"}, {"china", "petrochemical"}),
    ({"cnpc"}, {"china", "national", "petroleum"}),
    ({"cnooc"}, {"china", "national", "offshore", "oil"}),
    ({"adnoc"}, {"abu", "dhabi", "national", "oil"}),
]


def owner_core(name):
    """Core identifying tokens of an owner string: lowercased, diacritics folded,
    legal-form suffixes and stray punctuation removed. ('Gasum Oy' -> {'gasum'},
    'Chugoku Electric Power' -> {'chugoku', 'electric', 'power'})."""
    name = _strip_diacritics(str(name)).lower()
    name = re.sub(r"[()%\[\].,/]", " ", name)
    return {t for t in re.findall(r"[a-z]{2,}", name) if t not in _OWNER_LEGAL_SUFFIX}


def same_owner_entity(a, b):
    """True when two owner strings name the SAME entity in a different form, so a
    diff shouldn't flag them as a real ownership change. The test, after stripping
    legal-form suffixes:

      * one side's core tokens are a SUBSET of the other's — covers an added
        qualifier or legal suffix ("Gasum" ⊂ "Gasum Oy"; "Chugoku Electric" ⊂
        "Chugoku Electric Power"); or
      * a known acronym alias matches (KOGAS = Korea Gas, Petronas = Petroliam
        Nasional).

    Subset (not "any shared token") is deliberate: names that merely share a
    GENERIC word but each carry their own distinctive token stay DIFFERENT
    ("Korea Gas" vs "Korea Electric", "Tokyo Gas" vs "Tokyo Electric") — i.e. we
    only call owners the same when one name is essentially the other plus
    descriptive padding, never when they are substantially different."""
    ca, cb = owner_core(a), owner_core(b)
    if not ca or not cb:
        return False
    if ca <= cb or cb <= ca:
        return True
    for s1, s2 in _OWNER_ALIAS_PAIRS:
        if (ca & s1 and cb & s2) or (ca & s2 and cb & s1):
            return True
    return False


def main():
    """CLI smoke test."""
    samples_country = ["USA", "United States", "U.S.", "Türkiye", "Turkey", "PRC", "Korea, South"]
    samples_entity = [
        "TotalEnergies", "Total", "Total SA",
        "ExxonMobil", "Exxon Mobil",
        "Karpowership", "Karadeniz Holding",
        "QatarEnergy", "Qatar Petroleum",
    ]
    samples_ownership = [
        "ENI 50%, EGAS 40%, EGPC 10%",
        "TotalEnergies",
        "Shell, Total, BP",
    ]
    print("Country:")
    for s in samples_country:
        print(f"  {s!r:30} -> {normalize_country(s)!r}")
    print("\nEntity:")
    for s in samples_entity:
        print(f"  {s!r:30} -> {normalize_entity(s)!r}")
    print("\nOwnership parsing:")
    for s in samples_ownership:
        print(f"  {s!r:40} -> {parse_entity_list(s)}")


if __name__ == "__main__":
    main()
