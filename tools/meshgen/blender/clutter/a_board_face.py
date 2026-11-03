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
    os.makedirs(os.path.dirname(out), exist_ok=True)
    face.save(out, optimize=True)
    return out, (top_row, foot_row), face.size


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
