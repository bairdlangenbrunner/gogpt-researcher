"""
Fetch a satellite mosaic around a point, with a crosshair and a scale bar.

    python site_image.py <lat> <lon> [--zoom 16] [--size 3] [--out path.png]
                         [--tag us-ks --plant-id L100000402511]

Tiles are Esri World Imagery (no key), cached under work/tiles/<z>/<x>/<y>.jpg
so a rerun is free. --size is tiles per side (odd, default 3: 768 px square,
about 1.8 km across at zoom 16 and 39 N). A missing tile becomes a gray square
and is reported on stderr. The image carries a red crosshair at the point with
a gap at the center, a scale bar, a text line (point, zoom, Esri World Imagery,
date unknown) and a 1 px black frame.

Default output with --tag and --plant-id: work/sweep_<tag>/maps/<plant_id>_<n>.png
(n is the next free integer). Otherwise --out is required. The last line printed
is the path and the ground extent in meters. The mosaics are scratch under work/
and are never committed.

Library use:
    from site_image import render, save_site_image
    img = render(lat, lon, zoom=16, size=3, fetch_tile=None)   # PIL.Image
"""
from __future__ import annotations

import argparse
import io
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

import geo
from paths import work_dir

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
TILE = 256
RED = (255, 0, 0)
missing_tiles = []


def tiles_dir():
    return work_dir() / "tiles"


def fetch_tile(z, x, y):
    """One Esri tile as a PIL image, from the cache or the network (one retry); None if missing."""
    path = tiles_dir() / str(z) / str(x) / f"{y}.jpg"
    if path.exists():
        try:
            return Image.open(path).convert("RGB")
        except OSError:
            path.unlink(missing_ok=True)
    for attempt in range(2):
        try:
            req = urllib.request.Request(geo.tile_url(x, y, z), headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            img = Image.open(io.BytesIO(data)).convert("RGB")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            return img
        except Exception:
            if attempt == 0:
                time.sleep(1)
    return None


def _scale_bar_m(mpp):
    for m in (100, 200, 500, 1000):
        if 80 <= m / mpp <= 200:
            return m
    # none fits: take the one nearest the middle of the range
    return min((100, 200, 500, 1000), key=lambda m: abs(m / mpp - 140))


def render(lat, lon, zoom=16, size=3, fetch_tile=None):
    """Mosaic of size x size tiles centered on the point, annotated."""
    fetch = fetch_tile or globals()["fetch_tile"]
    size = int(size)
    if size % 2 == 0:
        size += 1
    fx, fy = geo.tile_xy(lat, lon, zoom)
    half = size // 2
    cx, cy = int(fx), int(fy)
    img = Image.new("RGB", (size * TILE, size * TILE), (128, 128, 128))
    for dy in range(-half, half + 1):
        for dx in range(-half, half + 1):
            x, y = cx + dx, cy + dy
            tile = None
            try:
                tile = fetch(zoom, x, y)
            except Exception:
                tile = None
            if tile is None:
                missing_tiles.append((zoom, x, y))
                continue
            img.paste(tile.convert("RGB").resize((TILE, TILE)), ((dx + half) * TILE, (dy + half) * TILE))
    # pixel of the point inside the mosaic
    px = round((fx - (cx - half)) * TILE)
    py = round((fy - (cy - half)) * TILE)
    d = ImageDraw.Draw(img)
    gap, length = 4, 24
    for sx, sy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        a = (px + sx * gap, py + sy * gap)
        b = (px + sx * (gap + length), py + sy * (gap + length))
        d.line([a, b], fill=RED, width=2)
    W, H = img.size
    mpp = geo.meters_per_pixel(lat, zoom)
    bar_m = _scale_bar_m(mpp)
    bar_px = round(bar_m / mpp)
    x0, y0 = 14, H - 26
    d.rectangle([x0 - 4, y0 - 14, x0 + bar_px + 4, H - 6], fill=(0, 0, 0))
    d.line([(x0, y0), (x0 + bar_px, y0)], fill=(255, 255, 255), width=3)
    for xx in (x0, x0 + bar_px):
        d.line([(xx, y0 - 5), (xx, y0 + 5)], fill=(255, 255, 255), width=2)
    d.text((x0, y0 - 13), f"{bar_m} m", fill=(255, 255, 255))
    text = f"{geo.fmt5(lat)}, {geo.fmt5(lon)} · zoom {zoom} · Esri World Imagery, date unknown"
    tw = d.textlength(text)
    d.rectangle([W - tw - 14, H - 22, W - 4, H - 4], fill=(0, 0, 0))
    d.text((W - tw - 9, H - 19), text, fill=(255, 255, 255))
    d.rectangle([0, 0, W - 1, H - 1], outline=(0, 0, 0), width=1)
    img.info["ground_extent_m"] = W * mpp
    return img


def _next_path(tag, plant_id):
    d = work_dir() / f"sweep_{tag}" / "maps"
    d.mkdir(parents=True, exist_ok=True)
    n = 1
    while (d / f"{plant_id}_{n}.png").exists():
        n += 1
    return d / f"{plant_id}_{n}.png"


def save_site_image(lat, lon, zoom=16, size=3, out=None, tag=None, plant_id=None, fetch_tile=None):
    """Render and write; returns (path, ground_extent_m)."""
    if out:
        path = Path(out)
        path.parent.mkdir(parents=True, exist_ok=True)
    elif tag and plant_id:
        path = _next_path(tag, plant_id)
    else:
        raise ValueError("give out, or both tag and plant_id")
    img = render(lat, lon, zoom=zoom, size=size, fetch_tile=fetch_tile)
    img.save(path)
    return path, img.info["ground_extent_m"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("lat", type=float)
    ap.add_argument("lon", type=float)
    ap.add_argument("--zoom", type=int, default=16)
    ap.add_argument("--size", type=int, default=3, help="tiles per side, odd")
    ap.add_argument("--out")
    ap.add_argument("--tag")
    ap.add_argument("--plant-id")
    a = ap.parse_args(argv)
    if not geo.valid_point(a.lat, a.lon):
        ap.error("not a valid point")
    if not a.out and not (a.tag and a.plant_id):
        ap.error("--out is required unless both --tag and --plant-id are given")
    path, extent = save_site_image(a.lat, a.lon, a.zoom, a.size, a.out, a.tag, a.plant_id)
    if missing_tiles:
        print(f"{len(missing_tiles)} tile(s) missing, shown as gray: {missing_tiles}", file=sys.stderr)
    print(f"{path} ground extent about {extent:.0f} m across")
    return 0


if __name__ == "__main__":
    sys.exit(main())
