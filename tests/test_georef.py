import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import georef  # noqa: E402

LAT0, LON0 = 39.0, -95.0
K = 111320 * math.cos(math.radians(LAT0))


def pix_to_ll(px, py):
    # synthetic affine: rotated, scaled, y flipped, a little shear
    X = 2.0 * px + 0.3 * py
    Y = -1.9 * py + 0.2 * px
    return LAT0 + Y / 110540, LON0 + X / K


def test_affine_three_points():
    pts = [(f"f{i}", p, pix_to_ll(*p)) for i, p in enumerate([(100, 100), (900, 150), (400, 800)])]
    site = (500, 400)
    lat, lon, fit, res = georef.solve(pts, site)
    elat, elon = pix_to_ll(*site)
    assert abs(lat - elat) < 1e-5 and abs(lon - elon) < 1e-5 and fit < 1


def test_affine_four_points_least_squares():
    pts = [(f"f{i}", p, pix_to_ll(*p)) for i, p in enumerate([(0, 0), (1000, 0), (0, 800), (1000, 800)])]
    lat, lon, fit, res = georef.solve(pts, (250, 600))
    elat, elon = pix_to_ll(250, 600)
    assert abs(lat - elat) < 1e-5 and abs(lon - elon) < 1e-5 and fit < 1


def test_similarity_two_points():
    s, ang = 3.0, math.radians(25)

    def ll(px, py):
        u, v = px, -py
        X = s * (math.cos(ang) * u - math.sin(ang) * v)
        Y = s * (math.sin(ang) * u + math.cos(ang) * v)
        return LAT0 + Y / 110540, LON0 + X / K
    pts = [("a", (100, 100), ll(100, 100)), ("b", (700, 500), ll(700, 500))]
    lat, lon, fit, res = georef.solve(pts, (400, 300))
    elat, elon = ll(400, 300)
    assert abs(lat - elat) < 1e-5 and abs(lon - elon) < 1e-5
    dist = georef.geo.distance_m(*pts[0][2], *pts[1][2])
    assert abs(fit - dist / 2 * 0.02) < 1e-6


def test_degenerate():
    try:
        georef.solve([("a", (1, 1), (39, -95)), ("b", (1, 1), (39.1, -95))], (5, 5))
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_draw_jpeg_under_300kb(tmp_path):
    rnd = random.Random(1)
    img = Image.new("RGB", (2000, 1500), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for _ in range(3000):
        x, y = rnd.randrange(2000), rnd.randrange(1500)
        d.line([(x, y), (x + rnd.randrange(60), y + rnd.randrange(60))],
               fill=(rnd.randrange(256), rnd.randrange(256), rnd.randrange(256)), width=2)
    src = tmp_path / "in.png"
    img.save(src)
    pts = [("a", (100, 100), (39.0, -95.0)), ("b", (900, 150), (39.0, -94.9)), ("c", (400, 800), (38.9, -95.0))]
    out = georef.draw_and_save(src, pts, (500, 400), 38.95, -94.95, tmp_path / "out" / "x.jpg")
    assert out.exists() and out.stat().st_size <= 300 * 1024
    with Image.open(out) as im:
        assert im.format == "JPEG" and max(im.size) <= 1600
