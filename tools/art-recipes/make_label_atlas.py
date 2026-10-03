"""The grocer's printed labels: one sheet of made-up 1990 packaging, a tile a product.

    python tools/art-recipes/make_label_atlas.py            # writes production/assets/shop-goods/labels.jpg and .json
    python tools/art-recipes/make_label_atlas.py --selftest

WHY, 3 October: three fresh reviews read the shops' shelves as toy bricks: every tin and packet
was a plain colour block. The close-range research (production/research/shop-window-interiors/
CLOSE-RANGE-2026-10-03.md, section 3) says how games make shelves read: simple tins and packets
carrying labels from one shared sheet, varied per item. Every maker and product here is made up
(no real brands: canon and the allowlist), set in the project's own OFL fonts (production/fonts).

The sheet is 8 by 4 tiles of 256 pixels. A tin's tile wraps round it; a packet's is its face.
tools/art-recipes/shop-room.py maps each item to a tile by name from the .json beside the sheet.
"""
import json
import os
import random
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "production", "assets", "shop-goods")
FONTS = os.path.join(REPO, "production", "fonts")
TILE, COLS, ROWS = 256, 8, 4

# (kind, maker, product, background, band, ink, picture): picture is a simple drawn mark
PRODUCTS = [
    ("tin", "KESTLE", "Garden Peas", (0.12, 0.35, 0.16), (0.92, 0.88, 0.70), (0.95, 0.95, 0.90), "peas"),
    ("tin", "WENLOW", "Baked Beans", (0.70, 0.30, 0.10), (0.20, 0.30, 0.55), (0.98, 0.95, 0.85), "beans"),
    ("tin", "ALDBURY", "Tomato Soup", (0.65, 0.08, 0.06), (0.95, 0.85, 0.30), (0.98, 0.95, 0.88), "tomato"),
    ("tin", "FERNSIDE", "Pilchards", (0.15, 0.25, 0.50), (0.90, 0.90, 0.85), (0.98, 0.95, 0.88), "fish"),
    ("tin", "SUNBURY", "Peach Slices", (0.92, 0.62, 0.20), (0.40, 0.15, 0.10), (0.25, 0.10, 0.05), "peach"),
    ("tin", "HOLME", "Rice Pudding", (0.88, 0.85, 0.72), (0.15, 0.30, 0.55), (0.15, 0.15, 0.30), "bowl"),
    ("tin", "KINGSMEAD", "Corned Beef", (0.55, 0.12, 0.10), (0.85, 0.75, 0.40), (0.98, 0.95, 0.85), "band"),
    ("tin", "BRANNOCK", "Custard", (0.95, 0.80, 0.20), (0.10, 0.20, 0.50), (0.10, 0.15, 0.40), "bowl"),
    ("tin", "KESTLE", "Carrots", (0.85, 0.40, 0.08), (0.15, 0.35, 0.15), (0.98, 0.95, 0.88), "carrot"),
    ("tin", "WENLOW", "Spaghetti", (0.75, 0.15, 0.10), (0.95, 0.90, 0.75), (0.98, 0.95, 0.88), "lines"),
    ("tin", "ALDBURY", "Mushroom Soup", (0.45, 0.35, 0.25), (0.92, 0.88, 0.75), (0.98, 0.95, 0.88), "bowl"),
    ("tin", "FERNSIDE", "Salmon", (0.85, 0.45, 0.40), (0.15, 0.20, 0.40), (0.98, 0.95, 0.90), "fish"),
    ("packet", "KINGSMEAD", "Tea", (0.10, 0.30, 0.20), (0.85, 0.70, 0.30), (0.95, 0.90, 0.75), "leaf"),
    ("packet", "HOLME", "Porridge Oats", (0.90, 0.85, 0.70), (0.55, 0.15, 0.10), (0.30, 0.10, 0.05), "bowl"),
    ("packet", "SUNBURY", "Corn Flakes", (0.95, 0.75, 0.15), (0.70, 0.10, 0.08), (0.65, 0.08, 0.05), "flakes"),
    ("packet", "BRANNOCK", "Plain Flour", (0.92, 0.92, 0.88), (0.15, 0.25, 0.55), (0.10, 0.15, 0.40), "wheat"),
    ("packet", "KESTLE", "Granulated Sugar", (0.20, 0.35, 0.65), (0.95, 0.95, 0.95), (0.98, 0.98, 0.98), "cubes"),
    ("packet", "WENLOW", "Gravy Granules", (0.35, 0.18, 0.10), (0.90, 0.75, 0.30), (0.95, 0.90, 0.75), "band"),
    ("packet", "ALDBURY", "Cocoa", (0.30, 0.15, 0.08), (0.85, 0.70, 0.35), (0.95, 0.88, 0.70), "cup"),
    ("packet", "FERNSIDE", "Rich Tea Biscuits", (0.80, 0.20, 0.12), (0.95, 0.90, 0.70), (0.98, 0.95, 0.88), "biscuit"),
    ("packet", "KINGSMEAD", "Digestives", (0.15, 0.25, 0.55), (0.90, 0.80, 0.50), (0.98, 0.95, 0.88), "biscuit"),
    ("packet", "HOLME", "Soap Flakes", (0.55, 0.75, 0.90), (0.15, 0.25, 0.55), (0.10, 0.15, 0.40), "flakes"),
    ("packet", "SUNBURY", "Custard Powder", (0.95, 0.85, 0.30), (0.65, 0.10, 0.08), (0.55, 0.08, 0.05), "bowl"),
    ("packet", "BRANNOCK", "Matches", (0.75, 0.10, 0.08), (0.95, 0.90, 0.75), (0.98, 0.95, 0.88), "band"),
    ("jar", "KESTLE", "Strawberry Jam", (0.70, 0.10, 0.15), (0.95, 0.90, 0.80), (0.98, 0.95, 0.90), "berry"),
    ("jar", "WENLOW", "Marmalade", (0.90, 0.55, 0.15), (0.95, 0.90, 0.80), (0.40, 0.15, 0.05), "orange"),
    ("jar", "ALDBURY", "Pickled Onions", (0.85, 0.80, 0.60), (0.20, 0.35, 0.20), (0.15, 0.25, 0.15), "onion"),
    ("jar", "HOLME", "Honey", (0.85, 0.60, 0.15), (0.35, 0.20, 0.08), (0.30, 0.15, 0.05), "band"),
    ("bottle", "FERNSIDE", "Washing-up Liquid", (0.20, 0.60, 0.30), (0.95, 0.95, 0.90), (0.98, 0.98, 0.95), "drops"),
    ("bottle", "KINGSMEAD", "Brown Sauce", (0.30, 0.15, 0.08), (0.85, 0.75, 0.40), (0.95, 0.90, 0.75), "band"),
    ("bottle", "SUNBURY", "Orange Squash", (0.95, 0.55, 0.10), (0.20, 0.30, 0.60), (0.98, 0.95, 0.88), "orange"),
    ("bottle", "BRANNOCK", "Vinegar", (0.55, 0.40, 0.20), (0.90, 0.88, 0.80), (0.20, 0.15, 0.10), "band"),
]


def rgb(c):
    return tuple(int(max(0.0, min(1.0, v)) * 255) for v in c)


def tile_rect(k):
    """(u0, v0, u1, v1) of tile k in the sheet's UVs (v up from the bottom)."""
    col, row = k % COLS, k // COLS
    return (col / COLS, 1.0 - (row + 1) / ROWS, (col + 1) / COLS, 1.0 - row / ROWS)


def draw_mark(d, kind, x, y, s, ink, band, rnd):
    from PIL import ImageDraw  # noqa: F401
    if kind in ("peas", "berry", "drops"):
        col = {"peas": (60, 150, 60), "berry": (190, 30, 40), "drops": (230, 240, 255)}[kind]
        for _ in range(9):
            r = s * rnd.uniform(0.07, 0.11)
            cx, cy = x + rnd.uniform(-s * 0.3, s * 0.3), y + rnd.uniform(-s * 0.2, s * 0.2)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col, outline=(20, 40, 20))
    elif kind == "beans":
        for _ in range(10):
            cx, cy = x + rnd.uniform(-s * 0.32, s * 0.32), y + rnd.uniform(-s * 0.2, s * 0.2)
            d.ellipse((cx - s * 0.08, cy - s * 0.05, cx + s * 0.08, cy + s * 0.05), fill=(225, 120, 50), outline=(120, 50, 20))
    elif kind in ("tomato", "orange", "peach", "onion"):
        col = {"tomato": (200, 35, 30), "orange": (240, 140, 30), "peach": (245, 170, 90), "onion": (235, 225, 190)}[kind]
        d.ellipse((x - s * 0.28, y - s * 0.25, x + s * 0.28, y + s * 0.25), fill=col, outline=(60, 30, 10), width=2)
        d.ellipse((x - s * 0.06, y - s * 0.28, x + s * 0.06, y - s * 0.18), fill=(50, 120, 40))
    elif kind == "fish":
        d.polygon([(x - s * 0.35, y), (x + s * 0.2, y - s * 0.15), (x + s * 0.2, y + s * 0.15)], fill=(170, 180, 190), outline=(40, 50, 60))
        d.polygon([(x + s * 0.2, y), (x + s * 0.38, y - s * 0.13), (x + s * 0.38, y + s * 0.13)], fill=(150, 160, 170))
    elif kind in ("bowl", "cup"):
        d.pieslice((x - s * 0.3, y - s * 0.3, x + s * 0.3, y + s * 0.25), 0, 180, fill=(250, 248, 240), outline=(60, 60, 60), width=2)
        d.ellipse((x - s * 0.3, y - s * 0.08, x + s * 0.3, y + s * 0.06), fill=(240, 220, 160))
    elif kind in ("flakes", "biscuit", "cubes", "wheat", "leaf", "carrot"):
        col = {"flakes": (235, 190, 80), "biscuit": (215, 170, 100), "cubes": (250, 250, 250), "wheat": (220, 190, 110),
               "leaf": (70, 140, 60), "carrot": (230, 110, 30)}[kind]
        for _ in range(7):
            cx, cy = x + rnd.uniform(-s * 0.3, s * 0.3), y + rnd.uniform(-s * 0.18, s * 0.18)
            r = s * rnd.uniform(0.07, 0.12)
            if kind in ("cubes",):
                d.rectangle((cx - r, cy - r, cx + r, cy + r), fill=col, outline=(120, 120, 140))
            else:
                d.ellipse((cx - r, cy - r * 0.7, cx + r, cy + r * 0.7), fill=col, outline=(110, 70, 30))
    elif kind == "lines":
        for i in range(8):
            yy = y - s * 0.2 + i * s * 0.055
            d.arc((x - s * 0.35, yy - s * 0.08, x + s * 0.35, yy + s * 0.08), 0, 180, fill=(240, 200, 100), width=3)
    else:   # "band": a plain printed band
        d.rectangle((x - s * 0.4, y - s * 0.06, x + s * 0.4, y + s * 0.06), fill=rgb(band))


def make():
    from PIL import Image, ImageDraw, ImageFont
    rnd = random.Random(12)
    os.makedirs(OUT, exist_ok=True)
    sheet = Image.new("RGB", (TILE * COLS, TILE * ROWS), (200, 200, 200))
    d = ImageDraw.Draw(sheet)
    head = ImageFont.truetype(os.path.join(FONTS, "marcellus-sc", "MarcellusSC-Regular.ttf"), 30)
    body = ImageFont.truetype(os.path.join(FONTS, "evening-paper", "LeagueGothic-Regular.ttf"), 46)
    small = ImageFont.truetype(os.path.join(FONTS, "evening-paper", "LibreFranklin-600.ttf"), 16)
    index = []
    for k, (kind, maker, product, bg, band, ink, mark) in enumerate(PRODUCTS[:COLS * ROWS]):
        col, row = k % COLS, k // COLS
        x0, y0 = col * TILE, row * TILE
        d.rectangle((x0, y0, x0 + TILE - 1, y0 + TILE - 1), fill=rgb(bg))
        d.rectangle((x0, y0 + 28, x0 + TILE - 1, y0 + 72), fill=rgb(band))
        d.text((x0 + TILE / 2, y0 + 50), maker, font=head, fill=rgb(bg), anchor="mm")
        draw_mark(d, mark, x0 + TILE / 2, y0 + 112, TILE * 0.5, ink, band, rnd)   # clear of a two-line name
        lines = product.split(" ") if len(product) > 12 else [product]
        if len(lines) > 2:
            lines = [" ".join(lines[:-1]), lines[-1]]
        # a two-line name set smaller, so it stays above the weight
        f = body if len(lines) == 1 else ImageFont.truetype(os.path.join(FONTS, "evening-paper", "LeagueGothic-Regular.ttf"), 36)
        for i, ln in enumerate(lines):
            d.text((x0 + TILE / 2, (y0 + 196) if len(lines) == 1 else (y0 + 178 + i * 32)), ln, font=f, fill=rgb(ink), anchor="mm")
        d.text((x0 + TILE / 2, y0 + TILE - 14), {"tin": "NET WT 15 OZ", "packet": "NET 1 LB", "jar": "1 LB JAR",
                                                 "bottle": "1 PINT"}[kind], font=small, fill=rgb(ink), anchor="mm")
        index.append({"tile": k, "kind": kind, "maker": maker, "product": product, "uv": [round(v, 6) for v in tile_rect(k)]})
    path = os.path.join(OUT, "labels.jpg")
    sheet.save(path, quality=90)
    json.dump({"what": "The grocer's printed labels (tools/art-recipes/make_label_atlas.py): every maker and product made up, "
                       "set in the project's OFL fonts; a tin's tile wraps round it, a packet's is its face.",
               "tiles": index, "cols": COLS, "rows": ROWS, "tile_px": TILE},
              open(os.path.join(OUT, "labels.json"), "w", encoding="utf-8"), indent=1)
    print("labels: %d tiles -> %s (%.0f KB)" % (len(index), path, os.path.getsize(path) / 1024))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("make_label_atlas selftest FAIL " + name)
    check("the sheet holds every product", len(PRODUCTS) <= COLS * ROWS)
    check("tile 0 is the top left", tile_rect(0) == (0.0, 0.75, 0.125, 1.0))
    check("every kind is one the room maps", all(p[0] in ("tin", "packet", "jar", "bottle") for p in PRODUCTS))
    # no real brands: the makers are our own words
    real = ("HEINZ", "BIRDS", "KELLOGG", "TYPHOO", "HOVIS", "MCVITIE", "HP ", "BRANSTON", "ROBINSON", "COLMAN", "OXO", "BISTO")
    check("no maker is a real brand", not any(r in p[1].upper() or r in p[2].upper() for p in PRODUCTS for r in real))
    print("make_label_atlas selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else (make() or 0))
