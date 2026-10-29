"""Shared plant list and matching for the Mississippi pre-sweep harvesters.

`harvest_psc_mississippi.py` (Public Service Commission dockets) and
`pull_queues_mississippi.py` (interconnection queues) both match what they
find to the Mississippi plants in the scoped GEM export. This module holds the
parts they share: the plant list, the hand-checked name patterns, and the
plain helpers. Nothing here touches the network.
"""

import re
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
CSV = REPO / "scripts" / "gem_export_gogpt_scoped.csv"
OUT = REPO / "batches" / "us-ms" / "harvest"

# Hand-checked patterns (2026-10-23): GEM plant id -> regexes that, when they
# hit a docket title, a document or a queue point of interconnection, mean the
# item names this plant (or its substation). Plants missing here fall back to
# the name words and are marked for checking.
KNOWN = {
    "L100000401921": [r"attala", r"sallis"],
    "L100000401833": [r"batesville"],
    "L100000401922": [r"baxter wilson", r"\bbaxter\b"],
    "L100000401627": [r"caledonia"],
    "L100000402094": [r"chevron", r"pascagoula"],
    "L100000401923": [r"choctaw county", r"french camp"],
    "L100001047324": [r"colossus", r"new haven"],
    "L100000401819": [r"crossroads", r"clarksdale"],
    "L100001025781": [r"delta blues"],
    "L100000401924": [r"andrus"],
    "L100000401925": [r"hinds", r"greenacres"],
    "L100000104009": [r"watson", r"gulfport"],
    "L100000402320": [r"kemper"],
    "L100000402322": [r"magnolia", r"ashland"],
    "L100000104011": [r"morrow", r"purvis"],
    "L100000401834": [r"moselle"],
    "L100001023568": [r"new caledonia"],
    "L100000402325": [r"quantum", r"ackerman"],
    "L100000402096": [r"ratcliffe"],
    "L100000401835": [r"silver creek"],
    "L100000401628": [r"southaven"],
    "L100001064651": [r"traceview", r"ridgeland"],
    "L100001080981": [r"vicksburg advanced", r"vicksburg"],
    "L100000402097": [r"daniel", r"escatawpa"],
}

NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|station|energy center|energy|"
    r"plant|power|gt|ms|mississippi|the|municipal|of|and|city|llc|inc|company|co|irp|facility|"
    r"generation|advanced|county|cc|ct)\b", re.I)


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def norm_county(s):
    """'Madison County' / 'madison' / 'Jackson County, MS' -> 'madison'."""
    s = re.sub(r",.*$", "", str(s or "")).strip().lower()
    return re.sub(r"\s+county$", "", s).strip()


def load_plants(csv_path=None, wanted=None):
    """One dict per Mississippi plant in the scoped export (unit rows grouped)."""
    csv = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    csv = csv[csv["State/Province"] == "Mississippi"]
    plants = []
    for pid, rows in csv.groupby("GEM location ID", sort=False):
        if wanted is not None and pid not in wanted:
            continue
        r = rows.iloc[0]
        if re.search(r"IRP power station", str(r["Plant name"])):
            continue
        city = r.get("City") if isinstance(r.get("City"), str) else ""
        county = r.get("Local area (taluk, county)")
        county = norm_county(county) if isinstance(county, str) else ""
        owner = r.get("Owner(s)") if isinstance(r.get("Owner(s)"), str) else ""
        plants.append({"id": pid, "name": r["Plant name"], "city": city, "county": county,
                       "owner": owner, "statuses": sorted(set(rows["Status"].astype(str))),
                       "name_words": words(r["Plant name"])})
    return plants


def known_hit(plant, text):
    pats = KNOWN.get(plant["id"])
    return bool(pats) and any(re.search(p, text, re.I) for p in pats)


def clean_ws(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()
