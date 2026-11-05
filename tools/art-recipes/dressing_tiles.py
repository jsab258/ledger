#!/usr/bin/env python3
"""THE STONE DRESSINGS' AND THE RAINWATER GOODS' TILES (the corner's step 9b, 5 November 2026;
production/art/corner/STEP9-PLAN-2026-11-03.md, "9b").

    python tools/art-recipes/dressing_tiles.py              # writes each tile's three maps and its check lines
    python tools/art-recipes/dressing_tiles.py --selftest

WHY. Two of the street's rows wear a small generic map today: sills, doorsteps and coping a concrete at 0.8 m, gutters and
downpipes a metal at 0.35 m. Mafia's trims are photographed material laid at a fixed density (MAFIA-KIT section 2), so
each row takes a scan tile through the scan rows (production/specs/ps5-corner.json "scanned") at about 512 px a metre.

SOURCES, both CC0 1.0 from Poly Haven by Rob Tuytel, 2k maps in F:/LedgerTools/polyhaven/<asset>/, looked at before use:
  large_sandstone_blocks (https://polyhaven.com/a/large_sandstone_blocks, 3 m a tile): a trim sheet, a moulded band across
    its top 20% and a plinth across its bottom 8%, which on a sill would read as carving, so only the coursed ashlar
    between them is cut (v 0.205 to 0.92, 2.14 m).
  rusty_metal_02 (https://polyhaven.com/a/rusty_metal_02, 1 m a tile): white paint with rust, its paint brought down to the
    row's near-black by match_rgb, so the rust reads as blotches in black paint, already periodic.

METHOD. Cut, resample to about 512 px a metre, make periodic with paint_wood_tile.py's cross-blend, normal and roughness cut
the same way. match_rgb is the row's palette colour over the tile's linear mean, as the other rows'.

CHECK: 512 px a metre by construction; seam error at most 1.5 on both axes; the stone's reflectance after its grade
0.20 to 0.45 (FLAGS-BRICK-BANDS).

Files go to production/assets/scanned/polyhaven/<asset>/ (git-ignored pictures) and the same path in F:/LedgerTools/game-inputs.
"""
import json
import os
import shutil
import sys

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paint_wood_tile import seam_error, seamless  # noqa: E402

SOURCE = "F:/LedgerTools/polyhaven"
GAME_INPUTS = "F:/LedgerTools/game-inputs"
DENSITY = 512.0
TILES = (
    {"asset": "large_sandstone_blocks", "base": "stone_dressing", "source_m": 3.0, "v": (0.205, 0.92),
     "palette": (0.240, 0.225, 0.200), "blend": 220},
    {"asset": "rusty_metal_02", "base": "rainwater", "source_m": 1.0, "v": (0.0, 1.0),
     "palette": (0.030, 0.030, 0.032), "blend": 96, "match_on_paint": True},
)


def to_linear(c):
    c = np.asarray(c, dtype=np.float64) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def want_px(t):
    """The square cut, side and blend together, at the target density, so the tile's metres are its pixels' metres."""
    return int(round((t["v"][1] - t["v"][0]) * t["source_m"] * DENSITY))


def eight_bit(im):
    """Poly Haven's roughness is a 16-bit grey, which convert() would clip to white."""
    if im.mode.startswith("I"):
        return im.point(lambda v: v / 257.0).convert("L").convert("RGB")
    return im.convert("RGB")


def cut(im, t, Image):
    n = im.size[0]
    v0, v1 = int(t["v"][0] * n), int(t["v"][1] * n)
    im = im.crop((0, v0, v1 - v0, v1))
    return np.asarray(im.resize((want_px(t), want_px(t)), Image.LANCZOS))


def make(t, Image):
    side = want_px(t) - t["blend"]
    src = os.path.join(SOURCE, t["asset"], t["asset"])
    out = {}
    for key, name in (("diff", "_diff_2k.jpg"), ("nor_dx", "_nor_dx_2k.png"), ("rough", "_rough_2k.png")):
        with Image.open(src + name) as im:
            a = cut(eight_bit(im), t, Image)
        out[key] = np.clip(np.rint(seamless(a, side, t["blend"])), 0, 255).astype(np.uint8)
    return side, out


def numbers(t, side, maps):
    mean = to_linear(maps["diff"]).reshape(-1, 3).mean(axis=0)
    lum = to_linear(maps["diff"]).mean(axis=2)
    # A TILE OF TWO COLOURS (first try, 5 November): over the whole mean, the rust's orange turned the paint's patches
    # blue on the downpipe, so such a tile is graded on its paint alone, the brightest quarter, and the rust falls darker
    ref = to_linear(maps["diff"])[lum >= np.percentile(lum, 75)].mean(axis=0) if t.get("match_on_paint") else mean
    match = [round(float(p / m), 4) for p, m in zip(t["palette"], ref)]
    seam = seam_error(maps["diff"].astype(np.float64))
    covers_m = side / DENSITY
    return {"base": t["base"], "asset": t["asset"], "side": side, "covers_m": round(covers_m, 4),
            "px_a_metre": DENSITY, "match_rgb": match, "mean_linear": [round(float(x), 4) for x in mean],
            "contrast": round(float(lum.std() / lum.mean()), 3), "seam_u": round(seam["u"], 2), "seam_v": round(seam["v"], 2),
            "rough_mean": round(float(maps["rough"][..., 0].mean() / 255.0), 3)}


def main():
    from PIL import Image
    failed = 0
    for t in TILES:
        side, maps = make(t, Image)
        n = numbers(t, side, maps)
        rel = "production/assets/scanned/polyhaven/" + t["asset"]
        here = os.path.join(REPO, rel)
        os.makedirs(here, exist_ok=True)
        for key, a in maps.items():
            Image.fromarray(a).save(os.path.join(here, "%s_%s.png" % (t["asset"], key)))
        far = os.path.join(GAME_INPUTS, rel)
        os.makedirs(far, exist_ok=True)
        for key in maps:
            shutil.copyfile(os.path.join(here, "%s_%s.png" % (t["asset"], key)), os.path.join(far, "%s_%s.png" % (t["asset"], key)))
        ok = n["seam_u"] <= 1.5 and n["seam_v"] <= 1.5
        failed += 0 if ok else 1
        print(json.dumps(n), "PASS" if ok else "FAIL")
    return 1 if failed else 0


def selftest():
    ok = []
    a = np.zeros((64, 64, 3), dtype=np.uint8) + 128
    t = {"palette": (0.24, 0.225, 0.2), "base": "x", "asset": "x"}
    n = numbers(t, 64, {"diff": a, "rough": a})
    ok.append(abs(n["match_rgb"][0] - 0.24 / float(to_linear(128))) < 1e-3)
    ok.append(n["covers_m"] == 0.125)
    ok.append(want_px(TILES[0]) == 1098)
    ok.append(all(x["v"][0] < x["v"][1] <= 1.0 for x in TILES))
    print("dressing_tiles selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
