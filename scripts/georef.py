"""
Georeference an official map: render a PDF page, then turn marked pixels into a point.

    python georef.py render <pdf> --page N [--dpi 150] [--out path] [--tag us-ks --plant-id L...]
    python georef.py solve --image <png> --site X,Y --point "<feature>" X,Y LAT,LON
                           --point ... [--out batches/<scope>/staging/maps/<plant_id>.jpg] [--json]

render: pdftoppm draws one page (falls back to pypdf image extraction, and says
so, only when pdftoppm is missing). Default output
work/sweep_<tag>/maps/<plant_id>_p<N>.png. Prints the path and the pixel size so
pixel coordinates can be read off the picture.

solve: two or more control points, each a feature label, its pixel x,y in the
image and its lat,lon. Two points fit a similarity (scale, rotation, shift);
three or more fit an affine transform by least squares, all in a local flat
plane centered on the control points. Prints the site lat lon (five decimals),
the fit error in meters (root mean square of the control-point residuals), the
satellite and pin links, and the written image. With two points the fit error
cannot be measured, so the number reported is a floor (half the distance between
the points times 0.02) and the output says to add a third. With exactly three the
affine fit is exact by construction, so its residual is zero and says little.
The saved JPEG shows the control points as blue circles with labels and the site
as a red crosshair with its lat lon; it is downscaled to at most 1600 px on the
long side and kept under 300 KB. The staged copy under batches/<scope>/staging/maps/
is committed with the batch as the evidence for the point.

Library use:
    from georef import solve
    lat, lon, fit_m, residuals = solve([(feature, (px, py), (lat, lon)), ...], (px, py))
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

import geo
from paths import REPO_ROOT, work_dir

PDFTOPPM_FALLBACK = "/Users/baird/miniconda3/bin/pdftoppm"
MAX_SIDE = 1600
MAX_BYTES = 300 * 1024


# ------------------------------------------------------------------ math
def _solve_linear(A, b):
    """Gaussian elimination with partial pivoting for a small square system."""
    n = len(A)
    M = [list(map(float, row)) + [float(b[i])] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-12:
            raise ValueError("control points are degenerate (collinear or identical)")
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n + 1):
                M[r][k] -= f * M[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (M[r][n] - sum(M[r][k] * x[k] for k in range(r + 1, n))) / M[r][r]
    return x


def _lstsq(rows, rhs):
    """Least squares through the normal equations."""
    n = len(rows[0])
    AtA = [[sum(r[i] * r[j] for r in rows) for j in range(n)] for i in range(n)]
    Atb = [sum(r[i] * y for r, y in zip(rows, rhs)) for i in range(n)]
    return _solve_linear(AtA, Atb)


def _plane(points):
    lat0 = sum(p[2][0] for p in points) / len(points)
    lon0 = sum(p[2][1] for p in points) / len(points)
    k = 111320.0 * math.cos(math.radians(lat0))

    def fwd(lat, lon):
        return (lon - lon0) * k, (lat - lat0) * 110540.0

    def inv(x, y):
        return lat0 + y / 110540.0, lon0 + x / k
    return fwd, inv


def solve(points, site_px):
    """points: [(feature, (px, py), (lat, lon)), ...]; returns (lat, lon, fit_m, residuals)."""
    if len(points) < 2:
        raise ValueError("need at least two control points")
    fwd, inv = _plane(points)
    pix = [(float(p[1][0]), float(p[1][1])) for p in points]
    xy = [fwd(float(p[2][0]), float(p[2][1])) for p in points]
    sx, sy = float(site_px[0]), float(site_px[1])
    if len(points) == 2:
        # similarity: X = a*u - b*v + tx, Y = b*u + a*v + ty, with v = -py (pixel y points down)
        rows, rhs = [], []
        for (px, py), (X, Y) in zip(pix, xy):
            u, v = px, -py
            rows.append([u, -v, 1, 0])
            rhs.append(X)
            rows.append([v, u, 0, 1])
            rhs.append(Y)
        a, b, tx, ty = _lstsq(rows, rhs)

        def apply(px, py):
            u, v = px, -py
            return a * u - b * v + tx, b * u + a * v + ty
    else:
        rows = [[px, py, 1.0] for px, py in pix]
        cx = _lstsq(rows, [p[0] for p in xy])
        cy = _lstsq(rows, [p[1] for p in xy])

        def apply(px, py):
            return (cx[0] * px + cx[1] * py + cx[2], cy[0] * px + cy[1] * py + cy[2])
    resid = []
    for (px, py), (X, Y) in zip(pix, xy):
        ax, ay = apply(px, py)
        resid.append(math.hypot(ax - X, ay - Y))
    if len(points) == 2:
        d = geo.distance_m(points[0][2][0], points[0][2][1], points[1][2][0], points[1][2][1]) or 0.0
        fit = d / 2 * 0.02
    else:
        fit = math.sqrt(sum(r * r for r in resid) / len(resid))
    lat, lon = inv(*apply(sx, sy))
    return lat, lon, fit, resid


# ------------------------------------------------------------------ drawing
def draw_and_save(image_path, points, site_px, lat, lon, out):
    img = Image.open(image_path).convert("RGB")
    scale = min(1.0, MAX_SIDE / max(img.size))
    if scale < 1.0:
        img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    blue = (0, 80, 255)
    for feature, (px, py), _ll in points:
        x, y = px * scale, py * scale
        d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=blue, width=3)
        tw = d.textlength(feature)
        d.rectangle([x + 11, y - 8, x + 15 + tw, y + 6], fill=(255, 255, 255))
        d.text((x + 13, y - 7), feature, fill=blue)
    x, y = site_px[0] * scale, site_px[1] * scale
    red = (255, 0, 0)
    for sx_, sy_ in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        d.line([(x + sx_ * 4, y + sy_ * 4), (x + sx_ * 28, y + sy_ * 28)], fill=red, width=3)
    label = f"{geo.fmt5(lat)}, {geo.fmt5(lon)}"
    tw = d.textlength(label)
    d.rectangle([x + 8, y + 8, x + 12 + tw, y + 22], fill=(255, 255, 255))
    d.text((x + 10, y + 10), label, fill=red)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    quality = 80
    while True:
        img.save(out, "JPEG", quality=quality, optimize=True)
        if out.stat().st_size <= MAX_BYTES or quality <= 20:
            break
        quality -= 10
    while out.stat().st_size > MAX_BYTES and max(img.size) > 400:
        img = img.resize((round(img.width * 0.85), round(img.height * 0.85)), Image.LANCZOS)
        img.save(out, "JPEG", quality=quality, optimize=True)
    return out


# ------------------------------------------------------------------ render
def _pdftoppm():
    return shutil.which("pdftoppm") or (PDFTOPPM_FALLBACK if Path(PDFTOPPM_FALLBACK).exists() else None)


def render_page(pdf, page, dpi, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    exe = _pdftoppm()
    if exe:
        prefix = out.with_suffix("")
        subprocess.run([exe, "-r", str(dpi), "-f", str(page), "-l", str(page), "-png",
                        "-singlefile", str(pdf), str(prefix)], check=True)
        return out, "pdftoppm"
    print("pdftoppm is missing; falling back to pypdf image extraction "
          "(only works for scanned pages that hold one embedded image)", file=sys.stderr)
    from pypdf import PdfReader
    reader = PdfReader(str(pdf))
    images = list(reader.pages[page - 1].images)
    if not images:
        raise SystemExit("no embedded image on that page; install poppler (pdftoppm)")
    Image.open(__import__("io").BytesIO(images[0].data)).convert("RGB").save(out)
    return out, "pypdf"


def _xy(s):
    a, b = s.split(",")
    return float(a), float(b)


def _rel(p):
    p = Path(p).resolve()
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render", help="render one PDF page to a PNG")
    r.add_argument("pdf")
    r.add_argument("--page", type=int, required=True)
    r.add_argument("--dpi", type=int, default=150)
    r.add_argument("--out")
    r.add_argument("--tag")
    r.add_argument("--plant-id")
    s = sub.add_parser("solve", help="turn a marked pixel into lat lon")
    s.add_argument("--image", required=True)
    s.add_argument("--site", required=True, type=_xy, metavar="X,Y")
    s.add_argument("--point", nargs=3, action="append", metavar=("FEATURE", "X,Y", "LAT,LON"),
                   required=True)
    s.add_argument("--out")
    s.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "render":
        if a.out:
            out = Path(a.out)
        elif a.tag and a.plant_id:
            out = work_dir() / f"sweep_{a.tag}" / "maps" / f"{a.plant_id}_p{a.page}.png"
        else:
            ap.error("--out is required unless both --tag and --plant-id are given")
        path, how = render_page(a.pdf, a.page, a.dpi, out)
        with Image.open(path) as im:
            print(f"{path} {im.width}x{im.height} px (rendered with {how})")
        return 0

    points = [(f, _xy(px), _xy(ll)) for f, px, ll in a.point]
    if len(points) < 2:
        ap.error("give at least two --point")
    lat, lon, fit, resid = solve(points, a.site)
    out = Path(a.out) if a.out else work_dir() / "georef_last.jpg"
    draw_and_save(a.image, points, a.site, lat, lon, out)
    links = geo.links_for(lat, lon)
    if a.json:
        print(json.dumps({
            "lat": round(lat, 5), "lon": round(lon, 5), "fit_m": round(fit, 1),
            "control_points": [{"feature": f, "px": [px[0], px[1]], "lat": ll[0], "lon": ll[1],
                                "residual_m": round(rs, 1)}
                               for (f, px, ll), rs in zip(points, resid)],
            "image": _rel(out)}, indent=2))
        return 0
    print(f"site {geo.fmt5(lat)}, {geo.fmt5(lon)}")
    if len(points) == 2:
        print(f"fit error about {fit:.0f} m (2 control points: fit error cannot be measured, add a third)")
    else:
        extra = " (three points fit exactly, so this says little; a fourth would test it)" if len(points) == 3 else ""
        print(f"fit error {fit:.1f} m{extra}")
    print(f"satellite {links.get('satellite', '')}")
    print(f"pin       {links.get('pin', '')}")
    print(f"image     {_rel(out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
