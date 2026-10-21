"""
Turn address or place text into candidate points, and a point into a place.

    python geocode.py "<address or place text>" [--near lat,lon] [--country US] [--limit 5] [--json]
    python geocode.py --reverse lat,lon [--json]

US queries (--country US, or --near inside any US state box) go to the US Census
geocoder first (free, no key). When Census returns nothing, or the query is not
a US one, Nominatim answers (free, no key, an identifying User-Agent, at most
one request a second). Every answer is cached as JSON under
work/geocode/<sha1 of provider and query>.json, so a rerun costs nothing.

Output is a numbered candidate list: provider, matched text, match quality,
lat lon with five decimals, distance from --near in km when given, and the
satellite and pin links. With --near the list is ordered nearest first.
--reverse returns country code, state, county and city (the gate uses it to
check a point lands in the plant's state or country).

Library use:
    from geocode import geocode, reverse
    geocode(text, near=None, country=None, limit=5) -> list of dicts with keys
        provider, label, lat, lon, quality, type, distance_m
    reverse(lat, lon) -> dict with keys country_code, country, state, county, city, display_name
Tests monkeypatch the module-level _fetch_json(url) and cache_dir().
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request

import geo
from paths import work_dir

UA = ("Global Energy Monitor research (GOGPT location step; "
      "baird.langenbrunner@globalenergymonitor.org)")
CENSUS = ("https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?"
          "address={q}&benchmark=Public_AR_Current&format=json")
NOMINATIM = "https://nominatim.openstreetmap.org/search?q={q}&format=jsonv2&limit=5&addressdetails=1"
NOMINATIM_REVERSE = ("https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}"
                     "&format=jsonv2&zoom=10&addressdetails=1")
_last_call = [0.0]


def cache_dir():
    d = work_dir() / "geocode"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _fetch_json(url):
    """GET a URL and parse JSON; Nominatim calls wait so they stay under one a second."""
    if "nominatim" in url:
        wait = 1.05 - (time.time() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    finally:
        _last_call[0] = time.time()


def _cached(provider, key, url):
    path = cache_dir() / (hashlib.sha1(f"{provider}|{key}".encode()).hexdigest() + ".json")
    if path.exists():
        try:
            return json.loads(path.read_text())
        except ValueError:
            pass
    data = _fetch_json(url)
    path.write_text(json.dumps(data))
    return data


def _is_us(near, country):
    if country:
        return country.strip().upper() in ("US", "USA")
    if near:
        return bool(geo.us_state_of(near[0], near[1]))
    return False


def _census(text):
    data = _cached("census", text, CENSUS.format(q=urllib.parse.quote(text)))
    out = []
    for m in ((data or {}).get("result") or {}).get("addressMatches") or []:
        c = m.get("coordinates") or {}
        if "x" not in c or "y" not in c:
            continue
        tl = m.get("tigerLine") or {}
        side = tl.get("side")
        quality = "tiger line side " + side if side else "address match"
        out.append({"provider": "census", "label": m.get("matchedAddress", ""),
                    "lat": float(c["y"]), "lon": float(c["x"]), "quality": quality,
                    "type": "address"})
    return out


def _nominatim(text, country, limit):
    url = NOMINATIM.format(q=urllib.parse.quote(text))
    if country:
        url += "&countrycodes=" + urllib.parse.quote(country.lower())
    data = _cached("nominatim", f"{text}|{country or ''}", url)
    out = []
    for r in (data or [])[:max(limit, 1)]:
        try:
            lat, lon = float(r["lat"]), float(r["lon"])
        except (KeyError, TypeError, ValueError):
            continue
        imp = r.get("importance")
        quality = (f"importance {float(imp):.2f}" if imp is not None else "importance unknown")
        out.append({"provider": "nominatim", "label": r.get("display_name", ""),
                    "lat": lat, "lon": lon, "quality": quality,
                    "type": "/".join(x for x in (r.get("category") or r.get("class"),
                                                 r.get("type")) if x)})
    return out


def geocode(text, near=None, country=None, limit=5):
    """Candidates for the text, nearest to `near` first when given."""
    near = (geo.parse_coord(near[0]), geo.parse_coord(near[1])) if near else None
    if near and (near[0] is None or near[1] is None):
        near = None
    results = []
    if _is_us(near, country):
        results = _census(text)
    if not results:
        results = _nominatim(text, country, limit)
    for r in results:
        r["distance_m"] = geo.distance_m(near[0], near[1], r["lat"], r["lon"]) if near else None
    if near:
        results.sort(key=lambda r: r["distance_m"] if r["distance_m"] is not None else 1e18)
    return results[:limit]


def reverse(lat, lon):
    """Place for a point, via Nominatim reverse (cached)."""
    url = NOMINATIM_REVERSE.format(lat=geo.fmt5(lat), lon=geo.fmt5(lon))
    data = _cached("nominatim-reverse", f"{geo.fmt5(lat)},{geo.fmt5(lon)}", url) or {}
    a = data.get("address") or {}
    return {"country_code": (a.get("country_code") or "").upper(),
            "country": a.get("country", ""),
            "state": a.get("state") or a.get("region") or "",
            "county": a.get("county", ""),
            "city": a.get("city") or a.get("town") or a.get("village")
            or a.get("municipality") or a.get("hamlet") or "",
            "display_name": data.get("display_name", "")}


def _pair(s):
    a, b = s.split(",")
    return float(a), float(b)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("text", nargs="?", help="address or place text")
    ap.add_argument("--near", type=_pair, metavar="LAT,LON")
    ap.add_argument("--country", help="ISO country code, e.g. US")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--reverse", type=_pair, metavar="LAT,LON")
    a = ap.parse_args(argv)
    if a.reverse:
        r = reverse(*a.reverse)
        if a.json:
            print(json.dumps(r, indent=2))
        else:
            print(f"{r['country_code']} | {r['state']} | {r['county']} | {r['city']}")
            print(r["display_name"])
        return 0
    if not a.text:
        ap.error("give the text to geocode, or --reverse lat,lon")
    res = geocode(a.text, near=a.near, country=a.country, limit=a.limit)
    for r in res:
        r["links"] = geo.links_for(r["lat"], r["lon"])
    if a.json:
        print(json.dumps(res, indent=2))
        return 0
    if not res:
        print("no candidates found")
        return 1
    for i, r in enumerate(res, 1):
        dist = f" | {r['distance_m'] / 1000:.1f} km from near" if r["distance_m"] is not None else ""
        print(f"{i}. [{r['provider']}] {r['label']}")
        print(f"   {r['quality']} | {r['type']} | {geo.fmt5(r['lat'])} {geo.fmt5(r['lon'])}{dist}")
        print(f"   satellite {r['links'].get('satellite', '')}")
        print(f"   pin       {r['links'].get('pin', '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
