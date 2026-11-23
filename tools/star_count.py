#!/usr/bin/env python3
"""WANTED STARS COUNTED BY CODE, NOT READ BY A MODEL (n23-1 and n23-2, 23 Nov 2026).

    python tools/star_count.py SHEET.png [--cols 8]   # one line per cell: row, column, white stars, grey stars
    python tools/star_count.py --selftest

WHY. The cheap-reader trial of 23 Nov (production/research/lane/measurements/STATUS.md) found no model fit to read
wanted stars: Sonnet and Haiku agreed with Opus on 63-78% of 1,710 cells, and Opus itself read two lit stars where the
zoomed pixels show three. Advisor 303's method: code reads the HUD, models only label and spot-check.

HOW. A sheet is the measuring page's grid of top-right frame crops, each with its time label in yellow beneath
(starscan/starscanT). Rows are found from the yellow label bands; each cell's area above its label is searched for
star-sized blobs of near-white (lit) or mid-grey, unsaturated pixels (unlit or fading), counted by connected parts.
FIRST PASS (23 Nov, two calibration tries): lit counts match every eye-checked cell; grey counts still take grey
scenery, and white timer digits read as lit stars in some cells. Not yet trusted for grey or near a timer.
Time labels are not read here: a model or the page's own list gives them; the count is per cell, left to right.
The bands (LIT, GREY, AREA) were set on sheet 6wy7gx of m_2RP_EIHM8 against cells checked by eye (9:00 three lit;
9:05 three lit and three grey; 9:10 three lit); every new clip is spot-checked by eye on two sheets before use.
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

LIT = 215          # min channel value for a lit star pixel
GREY = (95, 185)   # max channel range for an unlit star pixel
SAT = 30           # max spread between channels (stars are unsaturated)
AREA = (6, 160)    # star blob size in pixels at the sheet's scale


def label_rows(rgb):
    """[(top, bottom)] of each row's picture area, from the yellow label bands under it."""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    yellow = (r > 180) & (g > 180) & (b < 90)
    ys = np.where(yellow.sum(1) > 3)[0]
    bands, start = [], None
    for i, y in enumerate(ys):
        if start is None:
            start = y
        if i == len(ys) - 1 or ys[i + 1] != y + 1:
            bands.append((start, y))
            start = None
    rows, top = [], 0
    for b0, b1 in bands:
        rows.append((top, b0))
        top = b1 + 1
    return rows


def blobs(mask):
    """Star-shaped parts: size within AREA, bounding box near square, partly filled (a star, not a block of sky)."""
    lab, n = ndimage.label(mask)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        size = int((lab[sl] == i).sum())
        if AREA[0] <= size <= AREA[1] and 0.6 <= w / max(h, 1) <= 1.7 and 0.35 <= size / float(w * h) <= 0.9:
            out.append(((sl[0].start + sl[0].stop) / 2.0, size))
    return out


def count_cell(cell):
    c = cell.astype(int)
    hi, lo = c.max(2), c.min(2)
    flat = (hi - lo) <= SAT
    lit = blobs(flat & (lo >= LIT))
    grey = blobs(flat & (hi >= GREY[0]) & (hi <= GREY[1]))
    if lit:
        # unlit stars sit on the lit ones' line; anything off it is scenery (cells with no lit star keep every
        # star-shaped grey part: the first pass's known weakness, see STATUS.md)
        y = sum(b[0] for b in lit) / len(lit)
        grey = [b for b in grey if abs(b[0] - y) <= 3]
    return [len(lit), len(grey)]


def count_sheet(path, cols=8):
    rgb = np.asarray(Image.open(path).convert("RGB"))
    w = rgb.shape[1] // cols
    res = []
    for ri, (top, bottom) in enumerate(label_rows(rgb)):
        band = rgb[top:bottom]
        star_h = max(1, int((bottom - top) * 0.65))   # stars sit in the upper part; the icons below them are red
        for ci in range(cols):
            cell = band[:star_h, ci * w:(ci + 1) * w]
            white, grey = count_cell(cell)
            res.append((ri, ci, white, grey))
    return res


def selftest():
    ok = bad = 0
    img = np.zeros((43, 800, 3), np.uint8)
    def star(x, v):                       # a plus shape: near square, partly filled, like a small star
        img[8:13, x + 2] = v
        img[10, x:x + 5] = v
        img[9:12, x + 1:x + 4] = v
    for x in (40, 55, 70):
        star(x, 245)                      # three lit stars in cell 0
    for x in (130, 145):
        star(x, 140)                      # two grey ones in cell 1, on the same line
    img[36:40, 0:30] = (230, 220, 40)    # the yellow label band
    path = "selftest-star.png"
    try:
        import os
        import tempfile
        path = os.path.join(tempfile.gettempdir(), path)
        Image.fromarray(img).save(path)
        r = count_sheet(path)
        for name, cond in (("three lit stars counted", r[0][2] == 3 and r[0][3] == 0),
                           ("two grey stars counted", r[1][2] == 0 and r[1][3] == 2),
                           ("an empty cell counts none", r[2][2:] == (0, 0))):
            if cond:
                ok += 1
            else:
                bad += 1
                print("star_count selftest FAIL " + name, r[:3])
    finally:
        pass
    print("star_count selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cols = int(sys.argv[sys.argv.index("--cols") + 1]) if "--cols" in sys.argv else 8
    if "--cols" in sys.argv:
        args.remove(str(cols))
    for ri, ci, white, grey in count_sheet(args[0], cols):
        print("row %d col %d white %d grey %d" % (ri, ci, white, grey))
