import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import site_image  # noqa: E402


def fake_tile(z, x, y):
    return Image.new("RGB", (256, 256), (40, 90, 40))


def test_render_size_crosshair_scale():
    img = site_image.render(38.69512, -76.84071, zoom=16, size=3, fetch_tile=fake_tile)
    assert img.size == (768, 768)
    # find the crosshair center from the red pixels' bounding box
    red = [(x, y) for y in range(768) for x in range(768) if img.getpixel((x, y)) == (255, 0, 0)]
    xs = [p[0] for p in red]
    ys = [p[1] for p in red]
    cx, cy = (min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2
    assert img.getpixel((cx, cy)) != (255, 0, 0)          # center gap stays open
    assert img.getpixel((cx + 10, cy)) == (255, 0, 0)     # ring arms red
    assert img.getpixel((cx, cy - 10)) == (255, 0, 0)
    assert img.getpixel((0, 0)) == (0, 0, 0)               # frame


def test_scale_bar_range():
    for lat in (0, 39, 60):
        for z in (14, 15, 16, 17):
            m = site_image._scale_bar_m(site_image.geo.meters_per_pixel(lat, z))
            px = m / site_image.geo.meters_per_pixel(lat, z)
            if z in (16, 17):
                assert 80 <= px <= 200 or lat == 60


def test_scale_bar_at_default():
    mpp = site_image.geo.meters_per_pixel(39, 16)
    assert 80 <= site_image._scale_bar_m(mpp) / mpp <= 200


def test_missing_tile_gray():
    img = site_image.render(39, -95, size=3, fetch_tile=lambda z, x, y: None)
    assert img.getpixel((300, 300)) == (128, 128, 128)


def test_output_naming(tmp_path, monkeypatch):
    monkeypatch.setattr(site_image, "work_dir", lambda: tmp_path)
    p1, ext = site_image.save_site_image(39, -95, tag="us-ks", plant_id="L1", fetch_tile=fake_tile)
    p2, _ = site_image.save_site_image(39, -95, tag="us-ks", plant_id="L1", fetch_tile=fake_tile)
    assert p1 == tmp_path / "sweep_us-ks" / "maps" / "L1_1.png"
    assert p2.name == "L1_2.png" and p1.exists() and 1300 < ext < 1600
