#!/usr/bin/env python3
"""
Find data center backup generator fleets in a scope's permit harvest, add up their
nameplate, match them to GEM plants and write a table the briefs and the gate read.

Why this exists (notes/data_center_backup_plan.md): GEM adds a data center's backup
engine fleet as a plant when the summed generator nameplate reaches the threshold
(50 MW, 20 MW in the EU and the United Kingdom). The sweep agents kept dismissing
these fleets as "backup only" without adding them up. This script does the adding.

    python data_center_fleets.py --state Mississippi
    python data_center_fleets.py --state Michigan
    python data_center_fleets.py --country Germany
    python data_center_fleets.py --state Iowa --leads my_leads.csv

Reads (nothing else, and the network only through fetch.py):
    batches/<tag>/harvest/facilities.json   the permit harvest's facility list with the
                                            permit documents it saved (Mississippi and
                                            Michigan). When that file is missing, the
                                            harvest's markdown lists under work/permits/<tag>/
                                            (_unmatched.md, _applications.md, _county.md)
                                            are read instead, which gives names and links only.
    the permit documents themselves         through fetch.py (disk cache, then the whole
                                            access ladder); PDFs and Word files come back
                                            as text. A document that will not load is tried
                                            once more through a Wayback copy before it is
                                            listed as not loaded.
    gem_export_gogpt_scoped.csv             the scope's rows with Captive industry type
                                            "data center", or "data center" in the plant name.
    --leads FILE                            optional CSV or JSON of extra sites the caller
                                            supplies: name, operator, address, city, urls
                                            (separate several with a space or semicolon), notes.

A site is a candidate when its industry code is a data center code (SIC 7374, NAICS 518210),
or its name says data center, data services, digital, cloud, colocation or hyperscale, or its
name carries a known data center operator (Amazon Data Services, Microsoft, Google, Meta,
Compass, QTS, Aligned, CyrusOne and the rest of OPERATOR_WORDS). Every GEM data center plant
in the scope also gets a row, so an already tracked fleet is checked against the newest permit.

How a fleet is added up. Each permit document is read four ways, best first, and the best
reading wins (one document, never a sum across documents, because a later permit version
repeats the earlier one):
    1. application equipment inventory forms (Michigan): one line per emission unit with a
       design capacity in kW, or a stack label such as "3 MW - Main Generator".
    2. numbered generator lines (Mississippi): "(for 2,750 kW Genset)", one per engine,
       grouped under the building or group heading that precedes them.
    3. emission unit rows (Michigan permits to install): "One 2,750 (kW) diesel-fueled
       emergency engine".
    4. running prose: "forty-eight (48) 3,000 kW diesel-fired emergency generators",
       "12 x 2.5 MW natural gas-fired engine generator sets", "EU-001 through EU-032 ...
       2,500 kWe each".
Only the generator's electrical rating counts (kW, kWe, MW). Horsepower, brake horsepower and
mechanical kilowatts (kWm) are never converted; when that is all a document gives, the
engines are counted, the sum stays empty and the site is `unknown_capacity`.

Writes work/permits/<tag>/_data_centers.json and _data_centers.md (never anywhere else):
    scope, tag, generated, threshold_mw, sites[]. Each site: site_id, name, operator, address,
    city, permit_numbers, permit_urls, issue_date, fuel (diesel | natural gas | dual |
    unknown), engine_count, capacity_per_engine_mw (the most common engine size),
    summed_nameplate_mw, phases [{label, engines, mw, status_hint}], gem_plant_id,
    gem_plant_name, verdict, source_notes.
    verdict:
        at_threshold      the sum is at or above the threshold
        unknown_capacity  generators are listed but no usable electrical nameplate, or the
                          documents could not be read in full; the manual adds with the
                          capacity blank
        below_threshold   the sum is under the threshold
        in_gem            a GEM data center plant already covers the site (the sum is still
                          recorded; the site gets a check task)
        no_generators     the documents were read and name no generator
    One extra top-level list, unread_sites, holds candidates that only a code or a name
    flagged and that have no permit document anywhere (for example an air reporting schedule
    alone). They are listed in the markdown for a person and are not gate items.

Nothing is staged, nothing is written outside work/, and the live database is never touched.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

# ------------------------------------------------------------------ constants

EU_COUNTRIES = {
    "austria", "belgium", "bulgaria", "croatia", "cyprus", "czechia", "czech republic",
    "denmark", "estonia", "finland", "france", "germany", "greece", "hungary", "ireland",
    "italy", "latvia", "lithuania", "luxembourg", "malta", "netherlands", "poland",
    "portugal", "romania", "slovakia", "slovenia", "spain", "sweden", "united kingdom",
}

POSTAL = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "district of columbia": "DC",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID", "illinois": "IL",
    "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA",
    "maine": "ME", "maryland": "MD", "massachusetts": "MA", "michigan": "MI",
    "minnesota": "MN", "mississippi": "MS", "missouri": "MO", "montana": "MT",
    "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
    "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND",
    "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA",
    "rhode island": "RI", "south carolina": "SC", "south dakota": "SD", "tennessee": "TN",
    "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA",
    "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
}

# Operator brands that mark a site as a data center when they are in the facility name.
OPERATOR_WORDS = [
    "Amazon Data Services", "Amazon Web Services", "AWS", "Amazon", "Microsoft", "Google",
    "Meta Platforms", "Meta", "Oracle", "Apple", "QTS", "Compass Datacenters", "Compass",
    "Aligned", "CyrusOne", "Digital Realty", "Equinix", "Vantage", "Stack Infrastructure",
    "EdgeConneX", "DataBank", "Switch", "Iron Mountain", "Sabey", "Flexential", "Prime Data",
    "Tract", "Hut 8", "CoreWeave", "Crusoe", "Lancium", "Applied Digital", "PowerHouse",
    "Metrobloks", "Project Mitten", "xAI", "OpenAI", "Stargate",
]
# Short words that are common in other names: they only count next to a data center word.
RISKY_OPERATOR_WORDS = {"apple", "meta", "oracle", "switch", "stack", "tract", "aligned", "vantage",
                        "compass", "prime data", "amazon", "aws", "google", "microsoft"}
DC_NAME_RX = re.compile(
    r"data ?cent(?:er|re)s?|datacent(?:er|re)s?|data services|data campus|\bdigital\b|\bcloud\b|"
    r"colocation|co-location|hyperscale|\bproject [A-Z][a-z]+\b.*\bdata\b|server farm|compute campus",
    re.I)
DC_CODE_RX = re.compile(r"\b7374\b|\b518210\b|Data Processing, Web Hosting", re.I)
OPERATOR_RX = re.compile(r"\b(" + "|".join(re.escape(w) for w in OPERATOR_WORDS) + r")\b", re.I)

# Brand to the words a GEM name or operator may use for the same company.
BRAND_ALIASES = {
    "amazon": ("amazon", "aws", "amazon web services", "amazon data services"),
    "google": ("google", "alphabet"),
    "microsoft": ("microsoft",),
    "meta": ("meta", "facebook"),
    "compass": ("compass",),
    "qts": ("qts",),
    "aligned": ("aligned",),
    "cyrusone": ("cyrusone", "cyrus one"),
}

SKIP_DOC_RX = re.compile(
    r"approval letter|modeling report|figure|stack test|test (report|plan)|compliance evaluation|"
    r"spec(ification)? data|cover letter|\.xlsx?$|\.zip$|\.jpe?g$|\.png$|spanish|arabic|"
    r"\bwater\b|npdes|solid waste|pretreatment", re.I)

NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90,
}

GEN_NOUN = r"(?:generators?|gen[- ]?sets?|gensets?|generator sets?|engine[- ]generators?|engines?)"
# An electrical rating. "kWm" (mechanical) and "g/kW-hr" never match.
RATING = (r"(?P<kw>\d[\d,]*(?:\.\d+)?)\s*-?\s*(?P<u>kWe|kW|MWe|MW|kilowatts?|megawatts?)"
          r"(?:\s*\((?:kW|kWe|MW)\))?(?![\w/-])")
RATING_RX = re.compile(RATING, re.I)
MECH_RX = re.compile(r"mechanical|shaft|brake|\bbhp\b|\bhp\b|horsepower|kWm\b", re.I)

# ------------------------------------------------------------------ small helpers


def num(s):
    try:
        return float(str(s).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def words_to_int(s):
    """'forty-eight' -> 48, 'twelve' -> 12; None when it is not a number word."""
    total, seen = 0, False
    for part in re.split(r"[-\s]+", (s or "").strip().lower()):
        if part in NUMBER_WORDS:
            total += NUMBER_WORDS[part]
            seen = True
        elif part == "hundred" and seen:
            total = (total or 1) * 100
        elif part == "and":
            continue
        else:
            return None
    return total if seen else None


def mw_of(kw, unit):
    unit = unit.lower()
    v = num(kw)
    if v is None:
        return None
    return v if unit.startswith("m") else v / 1000.0


def collapse(text):
    return re.sub(r"\s+", " ", text or "").strip()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def fuel_of(text):
    t = (text or "").lower()
    diesel = bool(re.search(r"diesel|fuel oil|hydrotreated vegetable|\bhvo\b|distillate", t))
    gas = bool(re.search(r"natural[- ]gas|gas[- ]fired|gas-fueled|\bgas engine|methane", t))
    if diesel and gas:
        return "dual"
    if diesel:
        return "diesel"
    if gas:
        return "natural gas"
    return "unknown"


def status_hint_for(doc_name):
    n = (doc_name or "").lower()
    if re.search(r"draft|public notice|application|proposed", n):
        return "announced"
    if re.search(r"title v|operating|\brop\b|state permit to operate", n):
        return "operating"
    if re.search(r"construction|permit to install|\bpti\b|permit", n):
        return "construction"
    return ""


# ------------------------------------------------------------------ parsing the generators

def _unit(count, kw_each, mw_each, fuel, label, basis):
    return {"count": count, "kw_each": kw_each, "mw_each": mw_each, "fuel": fuel,
            "label": collapse(label)[:110], "basis": basis}


def _count_before(text, pos):
    """The count written just before pos: '(48)', 'forty-eight (48)', 'Twelve (12)', 'Four'."""
    m = re.search(r"([A-Za-z-]+)?\s*\((\d{1,4})\)\s*$", text[max(0, pos - 40):pos])
    if m:
        return int(m.group(2))
    m = re.search(r"\b([A-Za-z]+(?:-[A-Za-z]+)?)\s*$", text[max(0, pos - 25):pos])
    if m:
        return words_to_int(m.group(1))
    return None


def parse_generator_lines(text):
    """Generator lines in running prose -> [{count, kw_each, mw_each, fuel, label}].

    mw_each is None when the line gives only horsepower or mechanical kilowatts (the count
    is still returned). The same wording repeated in one document is counted once."""
    t = collapse(text)
    found, spans = [], []

    def free(s, e):
        return all(e <= a or s >= b for a, b in spans)

    def add(s, e, count, kw, unit, label, basis):
        if not free(s, e) or not count or count < 1:
            return
        spans.append((s, e))
        mw = mw_of(kw, unit) if kw is not None else None
        found.append(_unit(count, num(kw) * (1 if unit.lower().startswith("k") else 1000)
                           if kw is not None else None, mw, fuel_of(label), label, basis))

    # 1. "forty-eight (48) 3,000 kW diesel-fired emergency generators"
    p1 = re.compile(r"\((?P<n>\d{1,4})\)\s+(?P<mid>[^.;:()]{0,80}?)" + RATING + r"(?P<tail>[^.;:()]{0,80}?)\b" + GEN_NOUN, re.I)
    for m in p1.finditer(t):
        if MECH_RX.search(m.group("mid")):
            continue
        add(m.start(), m.end(), int(m.group("n")), m.group("kw"), m.group("u"), m.group(0), "count then rating")

    # 2. "twenty-six (26) Critical Emergency Generators, each with a maximum rated power capacity of 2,750 kW"
    p2 = re.compile(r"\((?P<n>\d{1,4})\)\s+(?P<mid>[^.;:()]{0,80}?)\b" + GEN_NOUN +
                    r"[^.;]{0,140}?\b(?:each|per (?:engine|generator|unit))\b[^.;]{0,60}?" + RATING, re.I)
    for m in p2.finditer(t):
        add(m.start(), m.end(), int(m.group("n")), m.group("kw"), m.group("u"), m.group(0), "count, then each at rating")

    # 3. "12 x 2.5 MW natural gas-fired engine generator sets"
    p3 = re.compile(r"\b(?P<n>\d{1,4})\s*(?:x|×)\s*" + RATING + r"(?P<tail>[^.;:()]{0,60}?)\b" + GEN_NOUN, re.I)
    for m in p3.finditer(t):
        add(m.start(), m.end(), int(m.group("n")), m.group("kw"), m.group("u"), m.group(0), "count x rating")

    # 4. "Emergency Generators EU-001 through EU-032: Caterpillar 3516C, 2,500 kWe each"
    p4 = re.compile(r"(?P<lab>[A-Za-z ]{0,40}\b" + GEN_NOUN + r"[A-Za-z ]{0,20}?)\s*\(?(?P<a>[A-Z]{1,6}-?\d+)\s+(?:through|thru|to)\s+"
                    r"(?P<b>[A-Z]{1,6}-?\d+)\)?\s*[:,-]?\s*(?P<mid>[^.;]{0,90}?)" + RATING + r"\s*(?:each|per)", re.I)
    for m in p4.finditer(t):
        a = re.search(r"(\d+)$", m.group("a"))
        b = re.search(r"(\d+)$", m.group("b"))
        if a and b and int(b.group(1)) >= int(a.group(1)):
            add(m.start(), m.end(), int(b.group(1)) - int(a.group(1)) + 1, m.group("kw"), m.group("u"), m.group(0), "range, each at rating")

    # 4b. a total only: "emergency back-up generators with a total power capacity of approximately 250 Megawatts"
    p4b = re.compile(r"(?P<lab>[^.;]{0,80}?\b" + GEN_NOUN + r")\s+with a total (?:[a-z ]{0,20})?capacity of (?:approximately |about |up to )?"
                     r"(?P<kw>\d[\d,]*(?:\.\d+)?)\s*(?P<u>MWe|MW|megawatts?|kWe|kW|kilowatts?)\b", re.I)
    for m in p4b.finditer(t):
        if free(m.start(), m.end()):
            spans.append((m.start(), m.end()))
            mw = mw_of(m.group("kw"), m.group("u"))
            found.append({"count": 1, "kw_each": mw * 1000, "mw_each": mw, "fuel": fuel_of(t[max(0, m.start() - 100):m.end() + 200]),
                          "label": collapse(m.group(0))[:110], "basis": "stated total", "total_only": True})

    # 5. horsepower or mechanical kilowatts only: count the engines, no capacity
    p5 = re.compile(r"(?:\((?P<n>\d{1,4})\)|\b(?P<w>[A-Za-z]+(?:-[A-Za-z]+)?)\b)\s+(?P<mid>[^.;()]{0,25}?)"
                    r"(?P<hp>\d[\d,]*)\s*(?:hp\b|bhp\b|horsepower|brake horsepower|mechanical kilowatts?|kWm\b)"
                    r"(?P<tail>[^.;]{0,160}?)\b" + GEN_NOUN, re.I)
    for m in p5.finditer(t):
        n = int(m.group("n")) if m.group("n") else words_to_int(m.group("w") or "") or 1
        add(m.start(), m.end(), n, None, "kW", m.group(0), "horsepower or mechanical only")

    # 6. engines counted with a heat input rating only ("Fifteen diesel-powered emergency generators, each with a
    #    maximum heat input rating of 18.76 MMBtu/hr"): no electrical rating, so no capacity
    p6 = re.compile(r"\b(?P<w>[A-Za-z]+(?:-[A-Za-z]+)?)\s*(?:\((?P<n>\d{1,4})\))?\s+(?P<mid>[^.;()]{0,50}?)\b" + GEN_NOUN +
                    r"[^.;]{0,60}?\beach\b[^.;]{0,60}?(?:heat input|MMBtu)", re.I)
    for m in p6.finditer(t):
        n = int(m.group("n")) if m.group("n") else words_to_int(m.group("w"))
        add(m.start(), m.end(), n, None, "kW", m.group(0), "heat input only")

    # a repeated identical line is one fleet, not two
    out, seen = [], set()
    for u in found:
        key = (u["count"], u["kw_each"], u["label"][:40].lower())
        if key not in seen:
            seen.add(key)
            out.append(u)
    return out


# Mississippi style: "(for 2,750 kW Genset)" once per engine, under a building heading.
GENSET_RX = re.compile(
    r"\bfor\b(?:(?!\bwith\b)[^.;()]){0,40}?(?P<kw>\d[\d,]*(?:\.\d+)?)\s*-?\s*(?P<u>kWe|kW|MWe|MW|Kilowatts?)\b"
    r"(?:\s*\((?:kW)\))?\s*Genset(?!s)", re.I)
HEADER_RX = re.compile(r"\b(?P<id>[A-Z]{1,3})-000\b")


def parse_genset_specs(text):
    """One generator per '(for N kW Genset)' mention, grouped under the heading before it.

    Returns {units: [{count, kw_each, mw_each, fuel, label, group}], groups: OrderedDict}."""
    t = collapse(text)
    headers = [(m.start(), m.end()) for m in HEADER_RX.finditer(t)]
    units = []
    for m in GENSET_RX.finditer(t):
        kw = num(m.group("kw"))
        if not kw:
            continue
        kw = kw * (1000 if m.group("u").lower().startswith("m") else 1)
        label = "Facility"
        hs = [h for h in headers if h[0] < m.start()]
        if hs:
            h = hs[-1]
            after = t[h[1]:h[1] + 200]
            b = re.search(r"\b(?:Building|Bldg\.?|Phase|Block|Hall)\s*\d+", after, re.I)
            if b:
                label = re.sub(r"^Bldg\.?", "Building", b.group(0), flags=re.I)
                label = collapse(label).title().replace("Bldg", "Building")
            else:
                lab = re.sub(r"\b[A-Z]{1,3}-\d{3}\b.*", "", after).strip(" ,.-") or after[:40]
                label = collapse(re.sub(r"^[A-Z0-9 -]{2,14}\s{1}(?=[A-Z][a-z])", "", after[:70])).strip(" ,.-")
                label = label or lab
        window = t[max(0, m.start() - 260):m.end() + 80]
        units.append({"count": 1, "kw_each": kw, "mw_each": kw / 1000.0, "fuel": fuel_of(window),
                      "label": label, "group": label, "basis": "numbered generator lines"})
    groups = OrderedDict()
    for u in units:
        g = groups.setdefault(u["group"], {"engines": 0, "mw": 0.0, "fuels": set()})
        g["engines"] += 1
        g["mw"] += u["mw_each"]
        g["fuels"].add(u["fuel"])
    return {"units": units, "groups": groups}


FORM_EU_RX = re.compile(
    r"EU\d{3,5}\s*(?:\((?P<eu>[^)]*)\))?\s+(?P<proc>E\d{3}\s*-\s*[^:]{0,160}?)\s*(?:NYB|PRE|OP|SHUT|IA)?\s*"
    r"Regulatory Status:.{0,60}?Design Capacity:\s*(?P<cap>[\d,]+(?:\.\d+)?)\s*(?P<cu>[A-Za-z0-9/]+)", re.I)


def parse_inventory_form(text):
    """Michigan application equipment inventory form: one line per emission unit.

    The generator size comes from the unit's own label ('3 MW - Main Generator',
    '1000 kW Generator') when it has one, otherwise from a design capacity given in kW."""
    t = collapse(text)
    units = []
    for m in FORM_EU_RX.finditer(t):
        proc = m.group("proc")
        if not re.search(r"generator|genset|engine", proc, re.I):
            continue
        cu = m.group("cu").lower()
        label_part = re.sub(r"^E\d{3}\s*-\s*(?:Engine[- ][A-Za-z ]*?(?:Generator|Engine)(?: Engine)?(?: #\d+)?)", "", proc, flags=re.I)
        cap_kw = num(m.group("cap")) if cu in ("kw", "kwe") else (num(m.group("cap")) * 1000 if cu == "mw" else None)
        lab = RATING_RX.search(label_part)
        label_kw = None
        if lab and not MECH_RX.search(label_part[max(0, lab.start() - 12):lab.start()]):
            label_kw = num(lab.group("kw")) * (1000 if lab.group("u").lower().startswith("m") else 1)
        kw = label_kw if label_kw else cap_kw
        note = ""
        if label_kw and cap_kw and abs(label_kw - cap_kw) > 1:
            note = f"label says {label_kw:g} kW, design capacity says {cap_kw:g} kW"
        units.append({"count": 1, "kw_each": kw, "mw_each": kw / 1000.0 if kw else None,
                      "fuel": fuel_of(proc + " " + label_part), "label": (m.group("eu") or "") + " " + proc[:60],
                      "basis": "inventory form", "note": note,
                      "heat_input_only": bool(not kw and cu not in ("kw", "kwe", "mw"))})
    return units


EU_ROW_RX = re.compile(r"(?:^|\s)(?P<id>EU[A-Z0-9]{0,8}-?\d+)\s+(?P<desc>(?:A|An|One|Two|Three|Four|Five|Six|\d+)\b.{0,330}?)\s+(?:TBD|\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2}|NA)\s+(?:FG[A-Z0-9-]+|NA)")


def parse_eu_rows(text):
    """Michigan permit to install emission unit rows ('EU2750-1  One 2,750 (kW) diesel-fueled
    emergency engine ...'). A row with horsepower or mechanical kilowatts only has no capacity."""
    t = collapse(text)
    units, seen = [], set()
    for m in EU_ROW_RX.finditer(t):
        eid, desc = m.group("id"), m.group("desc")
        if eid in seen or not re.search(r"generator|genset|engine", desc, re.I):
            continue
        if re.search(r"fire ?pump|cooling tower", desc, re.I):
            continue
        seen.add(eid)
        r = RATING_RX.search(desc)
        mech = MECH_RX.search(desc[: r.start()] if r else desc)
        if r and not (mech and re.search(r"mechanical|bhp|hp\b", desc[max(0, r.start() - 20):r.start()], re.I)):
            kw = num(r.group("kw")) * (1000 if r.group("u").lower().startswith("m") else 1)
            units.append({"count": 1, "kw_each": kw, "mw_each": kw / 1000.0, "fuel": fuel_of(desc),
                          "label": eid, "basis": "emission unit rows"})
        else:
            units.append({"count": 1, "kw_each": None, "mw_each": None, "fuel": fuel_of(desc),
                          "label": eid, "basis": "emission unit rows (horsepower or mechanical only)"})
    return units


def sum_fleet(units):
    """Electrical MW of the units that give one; None when none does."""
    known = [u for u in units if u.get("mw_each")]
    if not known:
        return None
    return round(sum(u["count"] * u["mw_each"] for u in known), 3)


def classify(summed, threshold, has_generators, incomplete=False, has_documents=True):
    """Verdict for a fleet. `incomplete` means some generators have no usable rating;
    `has_documents` False means no document is on record for the site yet, so the
    researcher must find one (verdict no_documents)."""
    if not has_documents:
        return "no_documents"
    if not has_generators:
        return "no_generators"
    if summed is None:
        return "unknown_capacity"
    if summed >= threshold:
        return "at_threshold"
    return "unknown_capacity" if incomplete else "below_threshold"


METHOD_RANK = {"inventory form": 4, "numbered generator lines": 3, "emission unit rows": 2, "prose": 1}


def extract_fleet(text):
    """Best reading of one document: {method, units, phases, notes} or None.

    The first method that yields a usable electrical rating wins; if none does but a
    method found engines, that reading comes back with no capacity."""
    readings = []
    forms = parse_inventory_form(text)
    if forms:
        readings.append(("inventory form", forms, []))
    gs = parse_genset_specs(text)
    if gs["units"]:
        phases = []
        if len(gs["groups"]) >= 2:
            for label, g in gs["groups"].items():
                phases.append({"label": label, "engines": g["engines"], "mw": round(g["mw"], 3), "status_hint": ""})
        readings.append(("numbered generator lines", gs["units"], phases))
    rows = parse_eu_rows(text)
    if rows:
        readings.append(("emission unit rows", rows, []))
    prose = parse_generator_lines(text)
    if prose:
        readings.append(("prose", prose, []))
    if not readings:
        return None
    usable = [r for r in readings if sum_fleet(r[1]) is not None]
    pool = usable or readings
    best = max(pool, key=lambda r: (METHOD_RANK[r[0]], sum_fleet(r[1]) or 0, sum(u["count"] for u in r[1])))
    method, units, phases = best
    notes = []
    if any(u.get("mw_each") is None for u in units):
        notes.append("some generators give only horsepower, mechanical kilowatts or heat input, which is not the electrical rating")
    for u in units:
        if u.get("note"):
            notes.append(u["note"])
            break
    return {"method": method, "units": units, "phases": phases, "notes": notes}


# ------------------------------------------------------------------ GEM matching

def _brand(text):
    t = (text or "").lower()
    for brand, aliases in BRAND_ALIASES.items():
        if any(re.search(r"\b" + re.escape(a) + r"\b", t) for a in aliases):
            return brand
    return ""


def _norm_city(c):
    return re.sub(r"\b(city|township|twp|charter)\b", "", (c or "").lower()).strip()


def load_gem_data_centers(scope, csv_path=None):
    """Scope rows with Captive industry type data center (or 'data center' in the plant
    name), grouped by GEM location ID."""
    from paths import gogpt_scoped_csv
    path = csv_path or gogpt_scoped_csv()
    plants = OrderedDict()
    if not Path(path).exists():
        return plants
    want_state = scope["name"].lower() if scope["kind"] == "state" else None
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if (r.get("Country/Area") or "").strip().lower() != scope["country"].lower():
                continue
            if want_state and (r.get("State/Province") or "").strip().lower() != want_state:
                continue
            ctype = (r.get("Captive industry type") or "").lower()
            if "data center" not in ctype and "data center" not in (r.get("Plant name") or "").lower() \
                    and "data centre" not in (r.get("Plant name") or "").lower():
                continue
            pid = (r.get("GEM location ID") or "").strip()
            p = plants.setdefault(pid, {"id": pid, "name": (r.get("Plant name") or "").strip(), "rows": [],
                                        "city": (r.get("City") or "").strip(),
                                        "county": (r.get("Local area (taluk, county)") or "").strip(),
                                        "operator": (r.get("Operator(s)") or r.get("Owner(s)") or "").strip()})
            p["rows"].append(r)
    return plants


def match_gem(site, plants):
    """The GEM data center plant that covers the site, or None.

    A match needs the same city plus either the same operator brand, a shared distinctive
    word in the plant name, or a street address found in the plant's notes."""
    plants = plants.values() if isinstance(plants, dict) else plants
    s_city = _norm_city(site.get("city"))
    s_brand = _brand(site.get("operator", "") + " " + site.get("name", ""))
    s_words = {w for w in re.findall(r"[a-z]{4,}", (site.get("name", "") + " " + site.get("operator", "")).lower())
               if w not in GENERIC_WORDS}
    best, best_score = None, 0
    for p in plants:
        score = 0
        p_city = _norm_city(p.get("city"))
        city_ok = bool(s_city) and s_city == p_city
        p_brand = _brand(p["name"] + " " + p.get("operator", ""))
        p_words = {w for w in re.findall(r"[a-z]{4,}", p["name"].lower()) if w not in GENERIC_WORDS}
        if city_ok:
            score += 2
            if s_brand and s_brand == p_brand:
                score += 3
            elif s_words & p_words:
                score += 2
        street = re.match(r"\s*(\d+\s+[A-Za-z0-9 .]+?)(?:,|$)", site.get("address") or "")
        if street:
            blob = " ".join((r.get("Notes") or "") + " " + (r.get("Status Detail") or "") for r in p["rows"]).lower()
            if street.group(1).lower() in blob:
                score += 3
        if score >= 4 and score > best_score:
            best, best_score = p, score
    return best


GENERIC_WORDS = {"data", "center", "centre", "power", "station", "services", "campus", "facility", "plant",
                 "project", "inc", "llc", "company", "township", "mega", "site", "building", "datacenters",
                 "datacenter", "technology", "development", "digital", "cloud"}


# ------------------------------------------------------------------ scope

def make_scope(state=None, country=None):
    if state:
        postal = POSTAL.get(state.strip().lower())
        if not postal:
            sys.exit(f"ERROR: unknown state {state!r}")
        return {"kind": "state", "name": state.strip(), "country": "United States",
                "tag": "us-" + postal.lower()}
    c = country.strip()
    return {"kind": "country", "name": c, "country": c, "tag": slug(c)}


def threshold_for(scope):
    return 20.0 if scope["country"].lower() in EU_COUNTRIES else 50.0


# ------------------------------------------------------------------ candidate sites

def strong_operator(name):
    m = OPERATOR_RX.search(name or "")
    if not m:
        return ""
    return m.group(1)


def looks_like_data_center(name, codes=""):
    if DC_CODE_RX.search(codes or ""):
        return True
    if DC_NAME_RX.search(name or ""):
        return True
    op = strong_operator(name)
    if op and op.lower() not in RISKY_OPERATOR_WORDS:
        return True
    if op and re.search(r"data|center|campus|JAN\d|\bDC\b|\bproject\b|services", name or "", re.I):
        return True
    return False


def operator_of(name):
    base = re.split(r",\s*", name or "", 1)[0].strip()
    m = OPERATOR_RX.search(name or "")
    if m and m.group(1).lower() in ("amazon", "aws"):
        return "Amazon Data Services" if "data services" in name.lower() else base
    return base


def clean_site_name(name):
    return collapse(re.sub(r"\s*\(OOB\)", "", name or ""))


def city_from_address(addr):
    """'1001 Industrial Park Drive Clinton, MS 39056' -> 'Clinton'; '' when it cannot tell."""
    m = re.search(r"(?:,|\b(?:Drive|Dr|Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Highway|Hwy|Lane|Ln|Way|Parkway|Pkwy|Court|Ct)\.?)\s+"
                  r"([A-Z][A-Za-z .'-]+?),?\s+[A-Z]{2}\s+\d{5}", addr or "")
    return m.group(1).strip() if m else ""


def facilities_from_harvest(scope):
    """Candidate sites from the harvester's facilities.json (batches/<tag>/harvest/)."""
    p = REPO_ROOT / "batches" / scope["tag"] / "harvest" / "facilities.json"
    if not p.exists():
        return None
    data = json.loads(p.read_text())
    facs = list(data.get("unmatched", [])) + list(data.get("matched", []))
    sic_names = names_with_data_center_codes(scope["tag"])
    out = []
    for f in facs:
        name = f.get("name", "")
        codes = " ".join(f.get("codes", []) or []) if isinstance(f.get("codes"), list) else str(f.get("codes", ""))
        if name.lower() in sic_names:
            codes += " 7374"
        if not looks_like_data_center(name, codes):
            continue
        permits = []
        for pm in f.get("permits", []) or []:
            n = pm.get("number") or pm.get("permit")
            if n and n not in permits and not str(n).startswith("RPT"):
                permits.append(n)
        for ap in f.get("active_permits", []) or []:
            if ap.get("number") and ap["number"] not in permits and ap.get("type", "").lower().startswith("air"):
                permits.append(ap["number"])
        apps = [a for a in (f.get("applications") or []) if a and a[0] == "Air"]
        for a in apps:
            if len(a) > 2 and a[2] not in permits:
                permits.append(a[2])
        docs = [{"name": d.get("name", ""), "url": d["url"], "date": d.get("date", "")} for d in f.get("docs", []) or []
                if d.get("url")]
        addr = f.get("full_address") or f.get("address", "")
        city = f.get("city", "") or city_from_address(addr)
        out.append({
            "name": clean_site_name(name), "operator": operator_of(clean_site_name(name)),
            "address": addr, "city": city,
            "id": str(f.get("srn") or f.get("ai") or ""), "permits": permits, "docs": docs,
            "applications": apps, "source": "harvest", "coded": bool(DC_CODE_RX.search(codes)),
        })
    return out


def names_with_data_center_codes(tag):
    """Facility names the harvest's markdown lists with SIC 7374 or NAICS 518210."""
    names = set()
    for fn in ("_unmatched.md",):
        p = REPO_ROOT / "work" / "permits" / tag / fn
        if not p.exists():
            continue
        for block in re.split(r"\n(?=- )", p.read_text(encoding="utf-8", errors="replace")):
            if DC_CODE_RX.search(block):
                m = re.match(r"- (.+?)(?: \(| \(enSearch|:|$)", block)
                if m:
                    names.add(m.group(1).strip().lower())
    return names


def facilities_from_markdown(scope):
    """Fallback when there is no facilities.json: names and links from the harvest's markdown lists."""
    base = REPO_ROOT / "work" / "permits" / scope["tag"]
    out = []
    for fn in ("_unmatched.md", "_applications.md", "_county.md"):
        p = base / fn
        if not p.exists():
            continue
        for block in re.split(r"\n(?=- )", p.read_text(encoding="utf-8", errors="replace")):
            if not block.startswith("- "):
                continue
            m = re.match(r"- (.+?)\s*\(([^)]*)\)", block)
            name = m.group(1).strip() if m else block[2:60]
            if not looks_like_data_center(name, block[:400]) and not DC_CODE_RX.search(block):
                continue
            city = ""
            if m:
                city = m.group(2).split(",")[0].strip()
            urls = [u.rstrip(".,);") for u in re.findall(r"https?://[^\s)>\]]+", block)]
            out.append({"name": clean_site_name(name), "operator": operator_of(clean_site_name(name)),
                        "address": "", "city": city, "id": "", "permits": re.findall(r"\b\d{2}-[A-Z]-\d{3}(?:-[A-Z]\d)?\b", block),
                        "docs": [{"name": "harvest link", "url": u, "date": ""} for u in dict.fromkeys(urls)],
                        "applications": [], "source": fn, "coded": bool(DC_CODE_RX.search(block))})
    return out


def facilities_from_leads(path):
    rows = []
    p = Path(path)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text())
        rows = data if isinstance(data, list) else data.get("sites", [])
    else:
        with open(p, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        low = {k.lower().strip(): v for k, v in r.items()}
        urls = low.get("urls") or low.get("url") or low.get("permit_urls") or ""
        if isinstance(urls, list):
            ul = urls
        else:
            ul = [u for u in re.split(r"[\s;]+", str(urls)) if u.startswith("http")]
        name = clean_site_name(low.get("name", ""))
        if not name:
            continue
        out.append({"name": name, "operator": low.get("operator") or operator_of(name),
                    "address": low.get("address", ""), "city": low.get("city", ""), "id": "",
                    "permits": [x for x in re.split(r"[\s;,]+", str(low.get("permit_numbers", ""))) if x],
                    "docs": [{"name": "lead link", "url": u, "date": ""} for u in ul],
                    "applications": [], "source": "lead", "coded": True,
                    "lead_notes": low.get("notes", "")})
    return out


# ------------------------------------------------------------------ reading documents

def wayback_copy(url):
    """Newest saved copy of an address, or ''. Goes through fetch.py, like every fetch here."""
    from urllib.parse import quote
    from fetch import fetch_page
    try:
        p = fetch_page("https://archive.org/wayback/available?url=" + quote(url, safe=""), timeout=60)
        j = json.loads(p.text)
        snap = (j.get("archived_snapshots") or {}).get("closest") or {}
        return snap.get("url", "") if snap.get("available") else ""
    except Exception:
        return ""


def strip_office_xml(text):
    """fetch.py hands back a Word file's raw XML when it cannot unpack it; keep only the words."""
    if "<w:document" not in text and "<w:t" not in text:
        return text
    i = text.find("<w:document")
    body = text[i:] if i >= 0 else text
    body = re.sub(r"</w:p>", "\n", body)
    return re.sub(r"<[^>]+>", "", body)


def read_document(url, cache):
    """(loaded, text, route note). The whole ladder through fetch.py, then a Wayback copy."""
    if url in cache:
        return cache[url]
    from fetch import fetch_page
    note = ""
    try:
        page = fetch_page(url, timeout=180)
        ok = page.status == "200" and len(page.text.strip()) > 200
        route = ",".join(page.notes) or "plain curl"
        status = page.status
        text = strip_office_xml(page.text) if ok else ""
    except Exception as e:  # a missing curl is the only raise; keep going and say so
        ok, text, route, status = False, "", "error", str(e)[:60]
    if not ok:
        snap = wayback_copy(url)
        if snap:
            try:
                p2 = fetch_page(snap, timeout=180)
                if p2.status == "200" and len(p2.text.strip()) > 200:
                    ok, text, route = True, strip_office_xml(p2.text), "Wayback copy " + snap
            except Exception:
                pass
        if not ok:
            note = f"not loaded (HTTP {status}, Wayback copy {'found but empty' if snap else 'not found'})"
    cache[url] = (ok, text, route if ok else note)
    return cache[url]


# ------------------------------------------------------------------ one site

def doc_issue_date(d):
    m = re.search(r"issued (\d{4}-\d{2}-\d{2})", d.get("name", ""))
    return m.group(1) if m else (d.get("date") or "")


def analyze_site(site, gem_plants, threshold, max_docs, cache, offline=False):
    """Build the contract record for one candidate site."""
    docs = [d for d in site["docs"] if not SKIP_DOC_RX.search(d.get("name", ""))][:max_docs]
    readings, urls, notes = [], [], []
    for d in docs:
        if offline:
            ok, text, route = False, "", "not fetched (offline run)"
        else:
            ok, text, route = read_document(d["url"], cache)
        urls.append(d["url"] if ok else f"{d['url']} (not loaded: {route})")
        if not ok:
            notes.append(f"Could not read {d['name'] or d['url']}: {route}.")
            continue
        fleet = extract_fleet(text)
        label = d["name"] or "a permit document"
        if fleet is None:
            notes.append(f"Read {label}. It names no generator or engine.")
            continue
        total = sum_fleet(fleet["units"])
        engines = sum(u["count"] for u in fleet["units"] if not u.get("total_only"))
        readings.append({"doc": d, "fleet": fleet, "mw": total, "engines": engines, "route": route})
        how = {"inventory form": "the equipment lines of the application form",
               "numbered generator lines": "the numbered generator lines",
               "emission unit rows": "the emission unit table",
               "prose": "the text"}[fleet["method"]]
        if any(u.get("total_only") for u in fleet["units"]):
            notes.append(f"Read {label} (route: {route}). It states a total generator capacity of about {total:,.0f} MW "
                         f"and does not list the engines, so the engine count is not known.")
        elif total is None:
            notes.append(f"Read {label}. It lists {engines} generator or engine units (from {how}) but gives horsepower, "
                         f"mechanical kilowatts or heat input, not an electrical rating, so no sum is possible.")
        else:
            notes.append(f"Read {label} (route: {route}). From {how} it lists {engines} generators adding up to {total:,.1f} MW electrical.")
        for n in fleet["notes"]:
            notes.append(n[0].upper() + n[1:] + ".")

    best = None
    if readings:
        usable = [r for r in readings if r["mw"] is not None] or readings
        best = max(usable, key=lambda r: (METHOD_RANK[r["fleet"]["method"]], r["mw"] or 0))
        # equal rank: keep the first (the harvest lists the newest first)
        top_rank = max(METHOD_RANK[r["fleet"]["method"]] for r in usable)
        same = [r for r in usable if METHOD_RANK[r["fleet"]["method"]] == top_rank]
        best = same[0] if same[0]["mw"] == best["mw"] else best

    rec = {
        "site_id": "", "name": site["name"], "operator": site["operator"], "address": site["address"],
        "city": site["city"], "permit_numbers": site["permits"], "permit_urls": urls,
        "issue_date": "", "fuel": "unknown", "engine_count": None, "capacity_per_engine_mw": None,
        "summed_nameplate_mw": None, "phases": [], "gem_plant_id": None, "gem_plant_name": None,
        "verdict": "", "source_notes": "",
    }
    incomplete = False
    if best:
        fleet = best["fleet"]
        units = fleet["units"]
        rec["issue_date"] = doc_issue_date(best["doc"])
        rec["summed_nameplate_mw"] = best["mw"]
        rec["engine_count"] = best["engines"] or None
        fuels = {u["fuel"] for u in units if u["fuel"] != "unknown"}
        rec["fuel"] = "dual" if len(fuels) > 1 else (next(iter(fuels)) if fuels else "unknown")
        sizes = Counter()
        for u in units:
            if u.get("mw_each") and not u.get("total_only"):
                sizes[round(u["mw_each"], 4)] += u["count"]
        if sizes:
            rec["capacity_per_engine_mw"] = sizes.most_common(1)[0][0]
        hint = status_hint_for(best["doc"].get("name", ""))
        rec["phases"] = [dict(p, status_hint=hint) for p in fleet["phases"]]
        incomplete = any(u.get("mw_each") is None for u in units)
        notes.insert(0, f"The sum comes from {best['doc']['name'] or 'the permit document'}"
                        f"{' (dated ' + rec['issue_date'] + ')' if rec['issue_date'] and rec['issue_date'] not in best['doc']['name'] else ''}.")
        if rec["capacity_per_engine_mw"] and len(sizes) > 1:
            notes.append("Engines differ in size; capacity per engine is the most common size.")
    has_generators = bool(best)
    verdict = classify(rec["summed_nameplate_mw"], threshold, has_generators, incomplete)
    if not docs:
        notes.append("No permit document is on record for this site yet. Search the state's permit "
                     "portal, the county and the operator's filings for one before deciding.")
        if site.get("applications"):
            a = site["applications"][-1]
            notes.append(f"The state lists an air application, permit {a[2]}, with status \"{a[4]}\" (dated {a[3]}). "
                         "Its draft or final permit text has not been found, so the generators are not counted yet.")
        verdict = classify(None, threshold, False, has_documents=False)
    elif all(u.endswith(")") and "(not loaded" in u for u in urls) and not best:
        notes.append("None of the documents on record loaded, so the generators are not counted yet. "
                     "Run each through fetch.py and the Wayback lookup before deciding.")
        verdict = "unknown_capacity"
    elif not best and readings == [] and any("names no generator" in n for n in notes):
        verdict = "no_generators"
    if site.get("lead_notes"):
        notes.append("Lead note: " + site["lead_notes"])

    m = match_gem(site, gem_plants)
    if m:
        rec["gem_plant_id"], rec["gem_plant_name"] = m["id"], m["name"]
        rec["verdict"] = "in_gem"
        gem_mw = sum(num(r.get("Capacity (MW)")) or 0 for r in m["rows"])
        notes.append(f"GEM already has this campus as {m['name']} ({m['id']}), {gem_mw:,.1f} MW over {len(m['rows'])} unit rows. "
                     f"Check the fleet size, the phases, the Backup Power box and the engine counts against the permit.")
        if verdict != "in_gem":
            notes.append(f"Without the GEM match the verdict would be {verdict.replace('_', ' ')}.")
    else:
        rec["verdict"] = verdict
    if rec["summed_nameplate_mw"] is not None:
        rec["summed_nameplate_mw"] = round(rec["summed_nameplate_mw"], 2)
    if rec["capacity_per_engine_mw"] is not None:
        rec["capacity_per_engine_mw"] = round(rec["capacity_per_engine_mw"], 4)
    rec["source_notes"] = " ".join(notes)
    return rec


def gem_only_site(p):
    mw = sum(num(r.get("Capacity (MW)")) or 0 for r in p["rows"])
    first = p["rows"][0]
    engines = sum(int(num(r.get("Number Of Engines")) or 0) for r in p["rows"])
    return {
        "site_id": "", "name": p["name"], "operator": p.get("operator", ""),
        "address": "", "city": p["city"], "permit_numbers": [], "permit_urls": [], "issue_date": "",
        "fuel": fuel_of(" ".join((r.get("Fuel") or "") for r in p["rows"])),
        "engine_count": engines or None, "capacity_per_engine_mw": None,
        "summed_nameplate_mw": round(mw, 2) if mw else None, "phases": [],
        "gem_plant_id": p["id"], "gem_plant_name": p["name"], "verdict": "in_gem",
        "source_notes": f"This is a GEM data center plant in the scope ({len(p['rows'])} unit rows, {mw:,.1f} MW in GEM). "
                        f"No permit in the harvest matched it, so the check against the newest permit is still to do. "
                        f"Backup Power in GEM: {', '.join(sorted({(r.get('Backup Power') or 'blank').strip() or 'blank' for r in p['rows']}))}.",
    }


def assign_site_ids(sites):
    seen = Counter()
    for s in sites:
        brand = _brand(s["operator"] + " " + s["name"]) or slug(s["operator"])[:24]
        base = slug(f"{brand}-{s['city']}") if s["city"] else slug(brand + "-" + s["name"])[:40]
        seen[base] += 1
        s["site_id"] = base if seen[base] == 1 else f"{base}-{seen[base]}"
    # a collision keeps the first plain and numbers the rest, in the list's stable order


# ------------------------------------------------------------------ output

def verdict_words(v):
    return v.replace("_", " ")


def write_outputs(scope, threshold, sites, unread, out_dir):
    out_dir = Path(out_dir)
    work = (REPO_ROOT / "work").resolve()
    if work not in out_dir.resolve().parents and out_dir.resolve() != work:
        sys.exit(f"ERROR: refusing to write outside work/: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = {"scope": scope["name"], "tag": scope["tag"], "generated": dt.date.today().isoformat(),
           "threshold_mw": threshold, "sites": sites, "unread_sites": unread}
    (out_dir / "_data_centers.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    L = [f"# Data center backup fleets: {scope['name']}", "",
         f"Written {doc['generated']}. A fleet counts when the generator nameplate adds up to {threshold:g} MW or more. "
         "Only the electrical rating of each generator is added. Horsepower and mechanical kilowatts are not converted.", ""]
    L += ["| Site | Operator | City | Permits | Engines | MW | Fuel | Verdict | GEM plant |",
          "|---|---|---|---|---|---|---|---|---|"]
    for s in sites:
        L.append("| " + " | ".join([
            s["name"], s["operator"], s["city"] or "", ", ".join(s["permit_numbers"]) or "none found",
            str(s["engine_count"]) if s["engine_count"] is not None else "unknown",
            f"{s['summed_nameplate_mw']:,.1f}" if s["summed_nameplate_mw"] is not None else "unknown",
            s["fuel"], verdict_words(s["verdict"]),
            f"{s['gem_plant_name']} ({s['gem_plant_id']})" if s["gem_plant_id"] else "not in GEM"]) + " |")
    L += ["", "## What each permit says", ""]
    for s in sites:
        L.append(f"### {s['name']} (`{s['site_id']}`)")
        L.append("")
        if s["address"]:
            L.append(f"Address: {s['address']}.")
            L.append("")
        L.append(s["source_notes"])
        L.append("")
        if s["phases"]:
            L.append("Groups in the permit:")
            for p in s["phases"]:
                L.append(f"- {p['label']}: {p['engines']} engines, {p['mw']:,.2f} MW")
            L.append("")
        if s["permit_urls"]:
            L.append("Documents:")
            for u in s["permit_urls"]:
                L.append(f"- {u}")
            L.append("")
    if unread:
        L += ["## Flagged by a code or a name, with no permit document", "",
              "These are not counted. Nothing here lists generators, so there is nothing to add up.", ""]
        for u in unread:
            L.append(f"- {u['name']} ({u['city'] or 'city not given'}): {u['why']}")
        L.append("")
    (out_dir / "_data_centers.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return out_dir / "_data_centers.json", out_dir / "_data_centers.md"


# ------------------------------------------------------------------ main

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--state")
    g.add_argument("--country")
    ap.add_argument("--leads", help="CSV or JSON of extra sites: name, operator, address, city, urls, notes")
    ap.add_argument("--max-docs", type=int, default=12, help="permit documents read per site")
    ap.add_argument("--offline", action="store_true", help="read no documents (lead list and export parts only)")
    ap.add_argument("--csv", help="scoped export CSV (default: the repo's scoped export)")
    ap.add_argument("--out-dir", help="output folder under work/ (default work/permits/<tag>)")
    args = ap.parse_args(argv)

    scope = make_scope(args.state, args.country)
    threshold = threshold_for(scope)
    out_dir = args.out_dir or (REPO_ROOT / "work" / "permits" / scope["tag"])

    cands = facilities_from_harvest(scope)
    if cands is None:
        cands = facilities_from_markdown(scope)
        print(f"no facilities.json for {scope['tag']}: read the harvest markdown lists ({len(cands)} candidates)", file=sys.stderr)
    if args.leads:
        for lead in facilities_from_leads(args.leads):
            same = [c for c in cands if slug(c["name"]) == slug(lead["name"]) or
                    (lead["city"] and slug(c["city"]) == slug(lead["city"]) and _brand(c["name"]) and _brand(c["name"]) == _brand(lead["name"]))]
            if same:  # a lead for a site the harvest already lists adds its documents to that site
                c = same[0]
                c["docs"] += [d for d in lead["docs"] if d["url"] not in {x["url"] for x in c["docs"]}]
                c["city"] = c["city"] or lead["city"]
                c["address"] = c["address"] or lead["address"]
                c["lead_notes"] = lead.get("lead_notes", "")
            else:
                cands.append(lead)
    gem = load_gem_data_centers(scope, args.csv)

    cache, sites, unread = {}, [], []
    for c in cands:
        has_doc = bool(c["docs"]) or bool(c.get("applications"))
        strong = bool(strong_operator(c["name"])) and (strong_operator(c["name"]).lower() not in RISKY_OPERATOR_WORDS
                                                        or bool(DC_NAME_RX.search(c["name"]) or c["source"] == "lead"))
        if not has_doc and not strong and not match_gem(c, gem) and c["source"] != "lead":
            unread.append({"name": c["name"], "city": c["city"], "why": "flagged by its industry code or name; the harvest holds no permit document for it"})
            continue
        print(f"reading {c['name']} ({len(c['docs'])} documents)", file=sys.stderr)
        sites.append(analyze_site(c, gem, threshold, args.max_docs, cache, offline=args.offline))

    matched_ids = {s["gem_plant_id"] for s in sites if s["gem_plant_id"]}
    for pid, p in gem.items():
        if pid not in matched_ids:
            sites.append(gem_only_site(p))

    sites.sort(key=lambda s: (s["city"] or "", s["name"]))
    assign_site_ids(sites)
    jp, mp = write_outputs(scope, threshold, sites, unread, out_dir)

    counts = Counter(s["verdict"] for s in sites)
    print(f"{scope['name']}: {len(sites)} sites, threshold {threshold:g} MW: " +
          ", ".join(f"{v} {n}" for v, n in sorted(counts.items())))
    print(f"wrote {jp}\nwrote {mp}")


if __name__ == "__main__":
    main()
