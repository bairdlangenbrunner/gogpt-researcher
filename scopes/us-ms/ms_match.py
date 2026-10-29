"""Shared plant list and matching for the Mississippi pre-sweep harvesters.

`harvest_psc.py` (Public Service Commission dockets) and
`scopes/us-ms/pull_queues_mississippi.py` (interconnection queues) both match what they
find to the Mississippi plants in the scoped GEM export. This module holds the
parts they share: the plant list, the hand-checked name patterns, and the
plain helpers. Nothing here touches the network.
"""

import json
import re
from pathlib import Path

import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from harvest_lib import CSV, REPO, clean_ws, norm_county  # noqa: E402,F401

OUT = REPO / "batches" / "us-ms" / "harvest"

# Hand-checked patterns (2026-10-23): GEM plant id -> regexes that, when they
# hit a docket title, a document or a queue point of interconnection, mean the
# item names this plant (or its substation). Plants missing here fall back to
# the name words and are marked for checking. Kept in queues.json next to this
# file, the one list pull_queues.py also reads for Mississippi.
KNOWN = json.loads((Path(__file__).resolve().parent / "queues.json").read_text(encoding="utf-8"))["known"]

NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|station|energy center|energy|"
    r"plant|power|gt|ms|mississippi|the|municipal|of|and|city|llc|inc|company|co|irp|facility|"
    r"generation|advanced|county|cc|ct)\b", re.I)


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


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


