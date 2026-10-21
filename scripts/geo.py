"""
Shared coordinate helpers for the location step (docs/reference/location.md).

No network, no model. Every script that shows, compares or stages a coordinate
uses these so links, rounding and distances agree everywhere: the brief, the
shard contract, the assembler, the gate, the workbook, the evidence file and
the review page.

    from geo import parse_coord, fmt5, decimals, distance_m, satellite_link, pin_link
    from geo import tile_xy, tile_url, us_state_of
"""
from __future__ import annotations

import math
import re

# Google Maps, no key: satellite view centered on the point, and a dropped pin
# (the pin link is an accepted Location Data Source on its own; Baird 2026-10-20).
SATELLITE = ("https://www.google.com/maps/@?api=1&map_action=map&center={lat},{lon}"
             "&zoom={zoom}&basemap=satellite")
PIN = "https://www.google.com/maps/search/?api=1&query={lat},{lon}"

# Esri World Imagery tiles (no key; attribution required on anything shown).
ESRI_TILE = ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/"
             "MapServer/tile/{z}/{y}/{x}")
ESRI_ATTRIBUTION = ("Imagery: Esri, Maxar, Earthstar Geographics, and the GIS User "
                    "Community")

COORD_RE = re.compile(r"^\s*([-+]?\d+(?:\.\d+)?)\s*$")


def parse_coord(value):
    """A cell or string as a float, or None when blank or not a number."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    m = COORD_RE.match(str(value))
    return float(m.group(1)) if m else None


def decimals(value) -> int:
    """How many decimals the written coordinate carries ("38.1" is 1, "38" is 0)."""
    s = str(value or "").strip()
    return len(s.split(".", 1)[1]) if "." in s else 0


def fmt5(x) -> str:
    """A coordinate written with five decimals, the way the step stages it."""
    return f"{float(x):.5f}"


def valid_point(lat, lon) -> bool:
    lat, lon = parse_coord(lat), parse_coord(lon)
    return (lat is not None and lon is not None
            and -90 <= lat <= 90 and -180 <= lon <= 180 and not (lat == 0 and lon == 0))


def distance_m(lat1, lon1, lat2, lon2):
    """Great-circle distance in meters, or None when a coordinate is missing."""
    pts = [parse_coord(v) for v in (lat1, lon1, lat2, lon2)]
    if any(v is None for v in pts):
        return None
    a1, o1, a2, o2 = pts
    p = math.pi / 180
    h = (0.5 - math.cos((a2 - a1) * p) / 2
         + math.cos(a1 * p) * math.cos(a2 * p) * (1 - math.cos((o2 - o1) * p)) / 2)
    return 12_742_000 * math.asin(math.sqrt(max(0.0, min(1.0, h))))


def satellite_link(lat, lon, zoom=17) -> str:
    return SATELLITE.format(lat=fmt5(lat), lon=fmt5(lon), zoom=int(zoom))


def pin_link(lat, lon) -> str:
    return PIN.format(lat=fmt5(lat), lon=fmt5(lon))


PIN_RE = re.compile(r"google\.com/maps/search/\?api=1&query=([-+]?\d+(?:\.\d+)?),([-+]?\d+(?:\.\d+)?)")


def pin_point(url):
    """The (lat, lon) a Google Maps pin link opens on, or None for any other URL."""
    m = PIN_RE.search(str(url or ""))
    return (float(m.group(1)), float(m.group(2))) if m else None


def links_for(lat, lon) -> dict:
    """{"satellite", "pin"} for a point, or {} when it is not a valid point."""
    if not valid_point(lat, lon):
        return {}
    return {"satellite": satellite_link(lat, lon), "pin": pin_link(lat, lon)}


# ---------------------------------------------------------------- web tiles
def tile_xy(lat, lon, zoom):
    """Fractional tile coordinates (x, y) of a point at a zoom level
    (Web Mercator, the scheme Esri and OpenStreetMap tiles use)."""
    lat, lon = float(lat), float(lon)
    n = 2 ** int(zoom)
    x = (lon + 180.0) / 360.0 * n
    lat_r = math.radians(max(-85.05112878, min(85.05112878, lat)))
    y = (1.0 - math.log(math.tan(lat_r) + 1.0 / math.cos(lat_r)) / math.pi) / 2.0 * n
    return x, y


def tile_latlon(x, y, zoom):
    """The north-west corner of tile (x, y) as (lat, lon); fractional x, y work too."""
    n = 2 ** int(zoom)
    lon = x / n * 360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lat, lon


def tile_url(x, y, zoom) -> str:
    return ESRI_TILE.format(z=int(zoom), x=int(x), y=int(y))


def meters_per_pixel(lat, zoom, tile_px=256) -> float:
    return 156_543.03392 * math.cos(math.radians(float(lat))) / (2 ** int(zoom)) * (256 / tile_px)


# ------------------------------------------------------------ US state boxes
# Generous bounding boxes (south, west, north, east) for the offline sanity
# check in state_gate.py: a staged point outside its state's box is wrong.
# A point inside the box is not proof it is in the state; geocode.py's reverse
# lookup settles the close calls.
US_STATE_BBOX = {
    "Alabama": (30.1, -88.5, 35.1, -84.8), "Alaska": (51.0, -180.0, 71.6, -129.9),
    "Arizona": (31.3, -114.9, 37.1, -109.0), "Arkansas": (33.0, -94.7, 36.6, -89.6),
    "California": (32.5, -124.5, 42.1, -114.1), "Colorado": (36.9, -109.1, 41.1, -102.0),
    "Connecticut": (40.9, -73.8, 42.1, -71.7), "Delaware": (38.4, -75.8, 39.9, -74.9),
    "District of Columbia": (38.78, -77.13, 39.0, -76.9),
    "Florida": (24.4, -87.7, 31.1, -79.9), "Georgia": (30.3, -85.7, 35.1, -80.7),
    "Hawaii": (18.8, -160.3, 22.3, -154.7), "Idaho": (41.9, -117.3, 49.1, -110.9),
    "Illinois": (36.9, -91.6, 42.6, -87.4), "Indiana": (37.7, -88.2, 41.8, -84.7),
    "Iowa": (40.3, -96.7, 43.6, -90.1), "Kansas": (36.9, -102.1, 40.1, -94.5),
    "Kentucky": (36.4, -89.6, 39.2, -81.9), "Louisiana": (28.8, -94.1, 33.1, -88.7),
    "Maine": (42.9, -71.1, 47.5, -66.9), "Maryland": (37.8, -79.5, 39.8, -74.9),
    "Massachusetts": (41.2, -73.6, 42.9, -69.8), "Michigan": (41.6, -90.5, 48.4, -82.1),
    "Minnesota": (43.4, -97.3, 49.4, -89.4), "Mississippi": (30.1, -91.7, 35.1, -88.0),
    "Missouri": (35.9, -95.8, 40.7, -89.0), "Montana": (44.3, -116.1, 49.1, -104.0),
    "Nebraska": (39.9, -104.1, 43.1, -95.2), "Nevada": (34.9, -120.1, 42.1, -113.9),
    "New Hampshire": (42.6, -72.6, 45.4, -70.5), "New Jersey": (38.8, -75.6, 41.4, -73.8),
    "New Mexico": (31.2, -109.1, 37.1, -102.9), "New York": (40.4, -79.8, 45.1, -71.7),
    "North Carolina": (33.7, -84.4, 36.7, -75.3), "North Dakota": (45.8, -104.1, 49.1, -96.5),
    "Ohio": (38.3, -84.9, 42.0, -80.4), "Oklahoma": (33.5, -103.1, 37.1, -94.3),
    "Oregon": (41.9, -124.7, 46.4, -116.4), "Pennsylvania": (39.6, -80.6, 42.4, -74.6),
    "Rhode Island": (41.0, -71.95, 42.1, -71.0), "South Carolina": (31.9, -83.4, 35.3, -78.4),
    "South Dakota": (42.4, -104.1, 46.0, -96.3), "Tennessee": (34.9, -90.4, 36.8, -81.5),
    "Texas": (25.7, -106.7, 36.6, -93.4), "Utah": (36.9, -114.1, 42.1, -108.9),
    "Vermont": (42.6, -73.5, 45.1, -71.4), "Virginia": (36.4, -83.8, 39.6, -75.1),
    "Washington": (45.4, -124.9, 49.1, -116.8), "West Virginia": (37.1, -82.7, 40.7, -77.6),
    "Wisconsin": (42.4, -92.9, 47.4, -86.7), "Wyoming": (40.9, -111.1, 45.1, -104.0),
}


def in_state_box(lat, lon, state: str, tolerance=0.05):
    """True, False, or None when the state is not in the table."""
    box = US_STATE_BBOX.get(str(state or "").strip())
    if box is None:
        return None
    lat, lon = parse_coord(lat), parse_coord(lon)
    if lat is None or lon is None:
        return False
    s, w, n, e = box
    if state == "Alaska" and lon > 0:
        lon -= 360          # the Aleutians cross the date line
    return (s - tolerance <= lat <= n + tolerance) and (w - tolerance <= lon <= e + tolerance)


def us_state_of(lat, lon):
    """The states whose boxes hold the point (often more than one near a border)."""
    return [s for s in US_STATE_BBOX if in_state_box(lat, lon, s, tolerance=0.0)]
