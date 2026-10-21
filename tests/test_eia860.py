import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import eia860  # noqa: E402

HTML = '''
<a href="/electricity/data/eia860/xls/eia8602023.zip">2023</a>
<a href="/electricity/data/eia860/xls/eia8602024ER.zip">2024 ER</a>
<a href="/electricity/data/eia860/xls/eia8602024.zip">2024</a>
<a href="/electricity/data/eia860/xls/eia8602025ER.zip">2025 ER</a>
<a href="/electricity/data/eia860/xls/eia8602025ER.zip">2025 ER again</a>
'''


def test_candidate_sorting():
    c = eia860.candidate_links(HTML)
    assert [(y, er) for y, er, _ in c] == [(2025, True), (2024, False), (2024, True), (2023, False)]
    assert c[0][2] == "https://www.eia.gov/electricity/data/eia860/xls/eia8602025ER.zip"


def test_final_beats_early_same_year():
    c = eia860.candidate_links('<a href="/x/xls/eia8602025ER.zip">a</a><a href="/x/xls/eia8602025.zip">b</a>')
    assert c[0][1] is False


def test_plant_index():
    df = pd.DataFrame([
        {"Plant Code": "12345", "Plant Name": "Brandywine", "Street Address": "12345 Brandywine Rd",
         "City": "Brandywine", "State": "MD", "Zip": "20613", "County": "Prince George's",
         "Latitude": 38.69512, "Longitude": -76.84071, "Utility Name": "Utility A"},
        {"Plant Code": "99", "Plant Name": "No coords", "Street Address": None, "City": "X",
         "State": "MD", "Zip": 20613.0, "County": "Y", "Latitude": float("nan"),
         "Longitude": None, "Utility Name": None},
    ])
    idx = eia860.plant_index(df)
    assert idx["12345"]["lat"] == 38.69512 and idx["12345"]["address"] == "12345 Brandywine Rd"
    assert idx["12345"]["utility"] == "Utility A"
    assert idx["99"]["lat"] is None and idx["99"]["lon"] is None
    assert idx["99"]["address"] == "" and idx["99"]["zip"] == "20613"
