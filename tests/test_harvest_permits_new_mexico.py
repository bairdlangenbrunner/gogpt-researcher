"""Parsers and matching for the New Mexico permit harvester, on small saved pages. No network."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-nm", "harvest_permits")
FX = Path(__file__).parent / "fixtures" / "harvest_nm"


def rd(n):
    return (FX / n).read_text(encoding="utf-8")


def test_locations_and_sweep_filter():
    facs = h.parse_locations(json.loads(rd("apmap_locations.json")))
    assert facs["ai-604"]["ai"] == 604 and facs["ai-604"]["county"] == "Lea"
    assert h.is_power(facs["ai-9001"])
    assert not h.is_power(facs["ai-9002"])


def test_popup():
    p = h.parse_popup(rd("popup_604.html"))
    assert p["nsr"] == "PSD0622" and p["tv"] == "P080" and p["airs"] == "350250054"
    assert p["organization"].startswith("Southwestern Public Service")
    f = h.new_fac("ai-604", "X", "NMED APMAP")
    h.apply_popup(f, p)
    assert [x["number"] for x in f["permits"]] == ["PSD0622", "P080"]


def test_collection():
    title, docs = h.parse_collection(rd("collection_604.html"))
    assert "(AI 604)" in title and len(docs) == 2
    assert docs[0]["number"] == "P080R2M1" and docs[0]["type"] == "Permit"
    assert docs[1]["date"] == "2002-08-19"


def test_notices():
    n = h.parse_notices(rd("notices.html"))
    assert len(n) == 2 and n[0]["air"] and not n[1]["air"]
    assert n[0]["posted"] == "2026-10-01" and n[0]["comment"] == ["2026-10-01", "2026-11-15"]
    assert "P263R1" in n[0]["numbers"]
    assert len(h.notice_facilities(n)) == 1


def test_albuquerque():
    p = h.parse_abq_pending(rd("abq_pending.html"))
    assert p[0]["application"] == "0456-M6" and p[0]["name"] == "Albuquerque Products Terminal"
    a = h.parse_aqn_report(rd("aqn_report.txt"))
    assert a[0]["record"] == "2026-AQN123" and a[0]["issued"] == "2026-10-30" and "EMERGENCY GENERATOR" in a[0]["text"]


def test_echo_skips_portable():
    f = h.echo_facilities(json.loads(rd("echo_qid.json"))["Results"]["Facilities"])
    assert len(f) == 1


def test_match_known_and_distance():
    facs = list(h.parse_locations(json.loads(rd("apmap_locations.json"))).values())
    cun = {"id": "L100000402297", "name": "Cunningham power station", "county": "Lea", "lat": 32.7131, "lon": -103.3533,
           "name_words": h.words("Cunningham power station")}
    assert [f["ai"] for f, _ in h.match(cun, facs)] == [604]
    other = {"id": "LX", "name": "Zed", "county": "", "lat": 34.5, "lon": -106.8, "name_words": set()}
    assert [f["ai"] for f, _ in h.match(other, facs)] == [9001]


def test_offline_main(tmp_path, monkeypatch):
    p = h.load_plants(csv_path=None)
    assert len(p) == 24
    net = h.Net(offline=True)
    assert h.cloud_collection(net, "k", 604).endswith("/collection/4827")
    assert h.wildcard_names(net, "Cunningham")[1] == "CUNNINGHAM STATION POWER PLANT"
