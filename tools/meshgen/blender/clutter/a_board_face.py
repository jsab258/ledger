"""The A-board's painted face as the street's own sign picture: one leaf's outer face, cut from the paint layout.

    python -I tools/meshgen/blender/clutter/a_board_face.py [--paint DIR] [--out PATH]

WHY, 3 November (the corner plan's step 10; production/cloud-week/targets/street-dressing/a-board): the street's
recipe (tools/art-recipes/terrace-front.py) takes a clutter model's geometry and flat colours only, and letters a
face only through a sign picture laid once across that part's own face (its lettered faces, sign_ materials). So the
board's two leaves (the model's f_main and r_main) wear this picture, and the rest of the board its flat paint.

WHAT IT CUTS. a_board_paint.py lays both faces out on one canvas 600 mm wide from canvas_z_bottom_mm up, at
px_per_mm, the leaf's length measured from the feet (a_board_paint.json). The leaf panel in the model runs from the
top of the feet's arch to the ridge (LEAF_FROM_MM to LEAF_TO_MM along the leaf), so that band is cut, full width,
and scaled to SIZE: the recipe stretches the picture over the part's own extent, so the cut is the panel's own.
The picture lives in the game inputs on F: under its repository path (new pictures stay out of git), where the
recipe and the game's staging both look.
"""
import json
import os
import sys

from PIL import Image

PAINT = r"F:\LedgerTools\tmp\clutter\a-board"
OUT = os.path.join(os.environ.get("LEDGER_GAME_INPUTS", r"F:\LedgerTools\game-inputs"),
                   "production", "assets", "vignette", "decals2d", "a_board_fish.png")
LEAF_FROM_MM = 57.0     # the panel's foot: the top of the feet's arch (the model's f_main, 0.057 m up)
LEAF_TO_MM = 990.0      # the ridge, along the leaf (the target's leaf length)
SIZE = (1024, 2048)     # a power of two each way, 1.7 px/mm across and 2.2 along: the lines are 36 mm high


def cut(paint_dir=PAINT, out=OUT):
    lay = json.load(open(os.path.join(paint_dir, "a_board_paint.json"), encoding="utf-8"))
    im = Image.open(os.path.join(paint_dir, "a_board_paint.png")).convert("RGB")
    w, h = im.size
    bottom, height = lay["canvas_z_bottom_mm"], lay["canvas_mm"][1]
    # rows count from the top; the canvas's v runs up from its bottom
    top_row = round((1.0 - (LEAF_TO_MM - bottom) / height) * h)
    foot_row = round((1.0 - (LEAF_FROM_MM - bottom) / height) * h)
    face = im.crop((0, max(0, top_row), w, min(h, foot_row))).resize(SIZE, Image.LANCZOS)
    face = weather(face)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    face.save(out, optimize=True)
    return out, (top_row, foot_row), face.size


#: THE WEAR AT STREET DISTANCE, 3 November (the board's first gate, F:/LedgerTools/gate/new/look/2026-11-03-a-board-b/
#: review.json: in the game the face was an even white panel, 187 of 255 with almost no variation, "a new printed or
#: plastic sign, not old painted plywood"; the target's wear, drawn at 3 px a millimetre, did not carry to 6 m). So the
#: target's own wear (TARGET.md, its wear section: the lower 150 mm streaked grey with splash, the top edge and right
#: arris rust-brown where the glue line weeps, emulsion chalking) is laid again at a scale that reads from the pavement.
GROUND_GAIN = 0.88          # chalked emulsion a few years out: the paint's ground about 12% under fresh
MOTTLE = 0.07               # broad patches of chalking and dirt, plus or minus
SPLASH_FROM_FOOT = 0.17     # the splash band's height, of the picture (150 mm of the 933 shown, and its fade)
SPLASH_GREY = (118, 116, 108)
RUST = (122, 78, 46)
SEED = 19901103


def _smooth_noise(rng, h, w, cells):
    """Sum of bilinearly enlarged random grids, 0..1."""
    from PIL import Image as I
    import numpy as np
    out = np.zeros((h, w))
    for c in cells:
        g = rng.random((c * 2, c))
        out += np.asarray(I.fromarray((g * 255).astype("uint8")).resize((w, h), I.BILINEAR)).astype(float) / 255.0
    return out / len(cells)


def weather(face):
    import numpy as np
    rng = np.random.default_rng(SEED)
    a = np.asarray(face).astype(float)
    h, w, _ = a.shape
    yy = np.linspace(0.0, 1.0, h)[:, None]          # 0 at the ridge, 1 at the foot
    xx = np.linspace(0.0, 1.0, w)[None, :]
    a *= GROUND_GAIN * (1.0 + MOTTLE * (2.0 * _smooth_noise(rng, h, w, (3, 6, 12)) - 1.0))[:, :, None]
    # THE SPLASH, NOT A COMB (3 November, the re-check, F:/LedgerTools/gate/new/look/2026-11-03-a-board-d/review.json:
    # the first draw stretched one row of random values down the face, an even comb of stripes to a level line, read
    # close to as curtain folds): a ragged line at uneven heights (broad noise along the width), under it a soft
    # gradient and splatter, specks thickening toward the foot, each a blot of its own size
    line = SPLASH_FROM_FOOT * (0.55 + 0.9 * _smooth_noise(rng, 1, w, (3, 7))[0])[None, :]
    rise = np.clip((yy - (1.0 - line)) / np.maximum(line, 1e-3), 0.0, 1.0)
    # IN CLUSTERS, FROM 150 MM DOWN (its second re-check, 2026-11-03-a-board-e/review.json: the spots stood too evenly,
    # one flat field starting at one height about 260 mm up, "a speckle brush or rain on glass"): splash from a wheel
    # or a shoe lands in sprays, so each blot belongs to a spray round a centre, the sprays thickest at the foot and the
    # corners, none higher than the target's 150 mm; each spray its own darkness
    speck = np.zeros((h, w))
    top_mm = 150.0 / 933.0
    sprays = []
    for _ in range(70):
        sx = rng.random() ** 0.7 if rng.random() < 0.5 else 1.0 - rng.random() ** 0.7      # toward the corners
        sy = 1.0 - top_mm * rng.random() ** 1.8                                              # toward the foot
        sprays.append((sx, sy, 0.02 + 0.06 * rng.random(), 0.35 + 0.55 * rng.random()))
    for _ in range(2600):
        sx, sy, spread, dark = sprays[int(rng.integers(len(sprays)))]
        y = sy + rng.normal(0.0, spread * 0.6)
        if y < 1.0 - top_mm * (0.75 + 0.5 * rng.random()) or y > 1.0:
            continue        # above its spray's reach, dropped, not piled at one line
        cy, cx = int(y * (h - 1)), int(min(1.0, max(0.0, sx + rng.normal(0.0, spread))) * (w - 1))
        r_ = 1.0 + rng.random() ** 3 * 7.0
        ry, rx = r_ * (0.7 + 0.6 * rng.random()), r_ * (0.7 + 0.6 * rng.random())   # a blot, round to oval
        y0, y1, x0, x1 = max(0, int(cy - ry)), min(h, int(cy + ry) + 1), max(0, int(cx - rx)), min(w, int(cx + rx) + 1)
        gy, gx = np.mgrid[y0:y1, x0:x1]
        d = ((gy - cy) / ry) ** 2 + ((gx - cx) / rx) ** 2
        speck[y0:y1, x0:x1] = np.maximum(speck[y0:y1, x0:x1], dark * (0.6 + 0.4 * rng.random()) * np.clip(1.2 - d, 0.0, 1.0))
    from PIL import ImageFilter
    speck = np.asarray(Image.fromarray((speck * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.8))).astype(float) / 255.0
    k = np.clip(0.45 * rise ** 1.6 + 0.5 * speck, 0.0, 0.75)[:, :, None]
    a = a * (1.0 - k) + np.array(SPLASH_GREY)[None, None, :] * k
    # RUST WEEPING FROM THE GLUE LINE: a broken band along the top edge, a few runs down from it of their own length,
    # width and spacing (not a row of drips), and the right arris's line, uneven along its length
    r = np.zeros((h, w))
    # deep and strong enough to carry to 3 m (the same re-check: at 0.018 deep and 0.25 to 0.6 strong the band shrank to
    # 2 or 3 px in the game and read as a thin dark rim; the first draw's band, about 8 px, did read as weep)
    r += np.clip(1.0 - yy / 0.035, 0.0, 1.0) ** 0.8 * (0.45 + 0.4 * _smooth_noise(rng, 1, w, (5, 11))[0])[None, :]
    for _ in range(int(rng.integers(4, 7))):
        x0, wid = rng.random(), 0.008 + 0.02 * rng.random()
        length, strength = 0.06 + 0.18 * rng.random() ** 1.3, 0.4 + 0.35 * rng.random()
        across = np.clip(1.0 - np.abs(xx - x0) / wid, 0.0, 1.0) ** 0.7
        r = np.maximum(r, strength * across * np.clip(1.0 - yy / length, 0.0, 1.0) ** 1.2)
    right = np.clip(1.0 - (1.0 - xx) / 0.035, 0.0, 1.0) * (0.4 + 0.6 * _smooth_noise(rng, h, 1, (6, 14))[:, :1])
    r = np.maximum(r, 0.7 * right ** 1.1)
    a = a * (1.0 - r[:, :, None]) + np.array(RUST)[None, None, :] * r[:, :, None]
    # grime toward the edges, where hands and weather reach first
    edge = np.minimum(np.minimum(xx, 1.0 - xx), np.minimum(yy, 1.0 - yy) * 0.5)
    a *= (1.0 - 0.18 * np.clip(1.0 - edge / 0.04, 0.0, 1.0))[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype("uint8"))


def selftest():
    import tempfile
    d = tempfile.mkdtemp()
    json.dump({"canvas_z_bottom_mm": -210.0, "canvas_mm": [600.0, 1200.0]}, open(os.path.join(d, "a_board_paint.json"), "w"))
    Image.new("RGB", (60, 120), (212, 213, 206)).save(os.path.join(d, "a_board_paint.png"))
    out, rows, size = cut(d, os.path.join(d, "face.png"))
    # the ridge (990 mm) is the canvas's top, 1200 - 210; the arch's top (57 mm) 267 mm up of 1200, row 93 of 120
    ok = rows == (0, 93) and size == SIZE
    print("a_board_face selftest: %s rows=%s size=%s" % ("passed" if ok else "FAILED", rows, size))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    a = sys.argv[1:]
    out, rows, size = cut(a[a.index("--paint") + 1] if "--paint" in a else PAINT, a[a.index("--out") + 1] if "--out" in a else OUT)
    print("a_board_face out=%s rows=%s size=%s" % (out, rows, size))
