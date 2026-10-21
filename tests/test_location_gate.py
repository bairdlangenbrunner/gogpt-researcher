"""The location gate (docs/reference/location.md): state_gate.gate_location
checks a staged point for completeness, validity, method, state box, exact
evidence, move explanations, map control points and sibling coverage, and
lets older per-field coordinate records through when they cover all three
columns between them."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from state_gate import gate_location  # noqa: E402

WHERE = {"kind": "state", "name": "Kansas", "slug": "kansas",
         "country": "United States", "postal": "ks"}
INDEX = {"mode": "update", "where": WHERE,
         "plants": [{"plant_id": "L1", "unit_ids": ["G1", "G2"]},
                    {"plant_id": "L2", "unit_ids": ["G3"]}]}


def record(**over):
    r = {"record_id": "L1:plant:location", "gem_plant_id": "L1", "gem_unit_id": "G1",
         "fields": {"Latitude": "38.12345", "Longitude": "-97.54321",
                    "Location accuracy": "approximate"},
         "verdict": "fill", "applies_to_all_units": True, "sibling_unit_ids": ["G2"],
         "sibling_current": {"G2": {"Latitude": "", "Longitude": "", "Location accuracy": ""}},
         "location_method": "address", "location_moved_m": None,
         "researcher_notes": "The plant's address from the county permit geocodes to this point."}
    r.update(over)
    return r


def lanes(*recs):
    return {"updates": list(recs)}


def test_clean_record_passes(tmp_path):
    assert gate_location(lanes(record()), INDEX, tmp_path) == []


def test_partial_fields_with_method_fail(tmp_path):
    r = record(fields={"Latitude": "38.1", "Longitude": "-97.5"})
    out = gate_location(lanes(r), INDEX, tmp_path)
    assert out and "together" in out[0][1]


def test_invalid_point_and_bad_accuracy(tmp_path):
    r = record(fields={"Latitude": "0", "Longitude": "0", "Location accuracy": "exact"})
    out = gate_location(lanes(r), INDEX, tmp_path)
    assert any("not a valid point" in m for _, m in out)
    r = record(fields={"Latitude": "38.1", "Longitude": "-97.5", "Location accuracy": "rough"})
    out = gate_location(lanes(r), INDEX, tmp_path)
    assert any("exact or approximate" in m for _, m in out)


def test_exact_needs_decimals_and_a_seen_note(tmp_path):
    r = record(fields={"Latitude": "38.12", "Longitude": "-97.54", "Location accuracy": "exact"},
               location_method="imagery", researcher_notes="Moved onto the site.")
    out = gate_location(lanes(r), INDEX, tmp_path)
    msgs = [m for _, m in out]
    assert any("three decimals" in m for m in msgs)
    assert any("satellite imagery" in m for m in msgs)
    r = record(fields={"Latitude": "38.12345", "Longitude": "-97.54321", "Location accuracy": "exact"},
               location_method="imagery",
               researcher_notes="The turbine hall and stack are visible in satellite imagery at this point.")
    assert gate_location(lanes(r), INDEX, tmp_path) == []


def test_method_and_state_box(tmp_path):
    out = gate_location(lanes(record(location_method="guess")), INDEX, tmp_path)
    assert any("location_method" in m for _, m in out)
    r = record(fields={"Latitude": "44.9", "Longitude": "-93.2", "Location accuracy": "approximate"})
    out = gate_location(lanes(r), INDEX, tmp_path)
    assert any("outside Kansas" in m for _, m in out)
    country = dict(INDEX, where={"kind": "country", "name": "Germany", "slug": "germany"})
    assert gate_location(lanes(r), country, tmp_path) == []


def test_big_move_needs_a_note(tmp_path):
    out = gate_location(lanes(record(location_moved_m=4200, researcher_notes="Moved.")),
                        INDEX, tmp_path)
    assert any("4.2 km" in m for _, m in out)
    assert gate_location(lanes(record(location_moved_m=4200)), INDEX, tmp_path) == []


def test_map_method_needs_points_fit_and_render(tmp_path):
    r = record(location_method="map", location_control_points=[{"feature": "a"}],
               location_fit_m=300, location_image="staging/maps/L1.jpg")
    out = gate_location(lanes(r), INDEX, tmp_path)
    msgs = [m for _, m in out]
    assert any("two control points" in m for m in msgs)
    assert any("fit error" in m for m in msgs)
    assert any("render" in m for m in msgs)
    (tmp_path / "staging" / "maps").mkdir(parents=True)
    (tmp_path / "staging" / "maps" / "L1.jpg").write_bytes(b"x")
    r = record(location_method="map", location_fit_m=40, location_image="staging/maps/L1.jpg",
               location_control_points=[{"feature": "a"}, {"feature": "b"}, {"feature": "c"}])
    assert gate_location(lanes(r), INDEX, tmp_path) == []


def test_sibling_coverage_and_shape(tmp_path):
    out = gate_location(lanes(record(sibling_unit_ids=[], sibling_current={})), INDEX, tmp_path)
    assert any("units not covered: G2" in m for _, m in out)
    out = gate_location(lanes(record(applies_to_all_units=False)), INDEX, tmp_path)
    assert any("every unit" in m for _, m in out)
    out = gate_location(lanes(record(sibling_current={"G2": ""})), INDEX, tmp_path)
    assert any("three columns" in m for _, m in out)


def test_legacy_per_field_records(tmp_path):
    def legacy(col, val, n):
        return {"record_id": f"L2:G3:{n}", "gem_plant_id": "L2", "gem_unit_id": "G3",
                "fields": {col: val}, "verdict": "fill"}
    full = lanes(legacy("Latitude", "38.1", "lat"), legacy("Longitude", "-97.5", "lon"),
                 legacy("Location accuracy", "approximate", "acc"))
    assert gate_location(full, INDEX, tmp_path) == []
    partial = lanes(legacy("Latitude", "38.1", "lat"), legacy("Longitude", "-97.5", "lon"))
    out = gate_location(partial, INDEX, tmp_path)
    assert out and "Location accuracy" in out[0][1]


def test_match_and_reverified_skipped(tmp_path):
    r = record(verdict="match", fields={"Latitude": "38.1"})
    assert gate_location(lanes(r), INDEX, tmp_path) == []
