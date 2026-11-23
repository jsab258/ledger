#!/usr/bin/env python3
"""WANTED STARS BY FIXED SLOTS AND A STAR TEMPLATE (n23-2, try 3, 23 Nov 2026).

    python tools/star_slots.py SHEET.png [--cols 8] [--cw PX]    # one line per cell: row, column, lit, grey, empty slots, per-slot marks (L g d .)
    python tools/star_slots.py --selftest

WHY. tools/star_count.py (blob counting, two calibration tries) counts lit stars right but takes grey scenery for unlit
stars and white timer digits for lit ones. The researched method (production/research/lane/measurements/
HUD-ICON-READING-NOTES-2026-11-23.md): HUD readers compare a FIXED region against a reference image with a mask
(AutoSplit's compare.py) or match a masked template and keep only peaks over a threshold (the Honor of Kings reader).
So this third method stops searching the cell for star-like blobs and looks only where a star can be.

HOW. (1) Calibrate per sheet from star_count's lit blobs, which are trusted: the star row's height, the pitch between
neighbouring stars and the rightmost slot's distance from the cell's right edge (medians). (2) The template is the mean
grey-level patch of the lit stars found. (3) Each cell has up to SLOTS slots leftward from the rightmost; each slot's
patch (best of a +-2 px vertical, +-1 px sideways shift) is scored by normalised correlation with the template, so digits and scenery, which
are not star-shaped, fail (a grey star over bright sky correlates negatively and counts too); a star-shaped slot is lit when its core is bright, grey when middling; a slot darker than the sky round it in a
star's shape (negative correlation) is an empty slot of the HUD's six (seen at 9:05 and 13:10 on 6wy7gx, zoomed).
Red stars (seen by police) count as lit, marked R. (4) Lit stars sit rightmost and unlit ones to their left; a lone match beyond a gap is dropped.
"""
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, __file__.rsplit("tools", 1)[0] + "tools")
import star_count as sc  # noqa: E402

SLOTS = 6
NCC_MIN = 0.55
LIT_MIN = 155      # core mean grey level of a lit star (lit read 188-223 on 6wy7gx, grey 109-117: the midpoint)
GREY_MIN = 85      # ... of an unlit (grey) star; dark-scene noise reads 12-50
RED_MIN = 60       # red minus the larger of green and blue in a red star's core
GREY_SPREAD = 40   # grey stars over coloured sky blend a little colour in (31-33 at 9:05 on 6wy7gx)


def lit_blobs(cell, grey=False):
    """(y, x) centres of lit, star-shaped parts (star_count's trusted lit test), with x measured in the cell; with
    grey=True the unlit band instead (to calibrate a sheet that shows no lit star)."""
    from scipy import ndimage
    c = cell.astype(int)
    hi, lo = c.max(2), c.min(2)
    if grey:
        mask = ((hi - lo) <= sc.SAT) & (hi >= sc.GREY[0]) & (hi <= sc.GREY[1])
    else:
        mask = ((hi - lo) <= sc.SAT) & (lo >= sc.LIT)
    lab, _ = ndimage.label(mask)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        size = int((lab[sl] == i).sum())
        if sc.AREA[0] <= size <= sc.AREA[1] and 0.6 <= w / max(h, 1) <= 1.7 and 0.35 <= size / float(w * h) <= 0.9:
            out.append(((sl[0].start + sl[0].stop - 1) / 2.0, (sl[1].start + sl[1].stop - 1) / 2.0))
    return out


def cells(rgb, cols, cw=None):
    w = cw or rgb.shape[1] // cols
    for ri, (top, bottom) in enumerate(sc.label_rows(rgb)):
        star_h = max(1, int((bottom - top) * 0.65))
        for ci in range(cols):
            yield ri, ci, rgb[top:top + star_h, ci * w:(ci + 1) * w]


def calibrate(rgb, cols, cw=None, grey=False):
    ys, pitches, rights, found = [], [], [], []
    for ri, ci, cell in cells(rgb, cols, cw):
        b = sorted(lit_blobs(cell, grey), key=lambda p: p[1])
        if len(b) < 2:
            continue
        xs = [p[1] for p in b]
        d = np.diff(xs)
        # a HUD row is evenly spaced on one line; scenery and page text are not
        if d.min() < 4 or d.max() - d.min() > 2 or max(p[0] for p in b) - min(p[0] for p in b) > 1.5:
            continue
        pitches += list(d)
        rights.append(cell.shape[1] - 1 - xs[-1])
        ys += [cell.shape[0] - 1 - p[0] for p in b]   # measured up from the star area's bottom (rows differ in height)
        found.append((cell, b))
    if len(found) < 2:            # one cell is no calibration: page text can mimic it
        return None if grey else calibrate(rgb, cols, cw, True)
    pitch, right, y = float(np.median(pitches)), float(np.median(rights)), float(np.median(ys))
    half = max(2, int(round(pitch * 0.45)))
    patches = []
    for cell, b in found:
        g = cell.astype(float).mean(2)
        for (py, px) in b:
            iy, ix = int(round(py)), int(round(px))
            p = g[iy - half:iy + half + 1, ix - half:ix + half + 1]
            if p.shape == (2 * half + 1, 2 * half + 1):
                patches.append(p)
    tpl = np.mean(patches, 0)
    # the star's core (top 40% of the template's range): edges blend into the sky behind and would pull brightness and
    # colour spread towards the scenery's
    core = tpl > tpl.min() + 0.6 * (tpl.max() - tpl.min())
    return {"pitch": pitch, "right": right, "y": y, "half": half, "tpl": tpl, "mask": core}


def ncc(a, b):
    a, b = a - a.mean(), b - b.mean()
    den = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / den) if den > 0 else 0.0


def read_cell(cell, cal):
    g = cell.astype(float).mean(2)
    c = cell.astype(int)
    spread = c.max(2) - c.min(2)
    red = c[..., 0] - np.maximum(c[..., 1], c[..., 2])
    h = cal["half"]
    marks = []
    for k in range(SLOTS):
        cx = cell.shape[1] - 1 - cal["right"] - k * cal["pitch"]
        best = (0.0, 0.0, 999.0, 0.0)
        for dy in (-2, -1, 0, 1, 2):        # rows' label bands sit up to 1.5 px apart
            for dx in (-1, 0, 1):
                iy, ix = int(round(cell.shape[0] - 1 - cal["y"])) + dy, int(round(cx)) + dx
                if iy - h < 0 or ix - h < 0:
                    continue
                p = g[iy - h:iy + h + 1, ix - h:ix + h + 1]
                if p.shape != cal["tpl"].shape:
                    continue
                s = ncc(p, cal["tpl"])
                if abs(s) > abs(best[0]):
                    sp = spread[iy - h:iy + h + 1, ix - h:ix + h + 1][cal["mask"]]
                    rd = red[iy - h:iy + h + 1, ix - h:ix + h + 1][cal["mask"]]
                    best = (s, float(p[cal["mask"]].mean()), float(np.median(sp)), float(np.median(rd)))
        s, bright, sat, redness = best
        if s >= NCC_MIN and redness >= RED_MIN:
            marks.append("R")          # a red star: lit while the police see the player
        elif s >= NCC_MIN and sat <= GREY_SPREAD and bright >= LIT_MIN:
            marks.append("L")
        elif s >= NCC_MIN and sat <= GREY_SPREAD and bright >= GREY_MIN:
            marks.append("g")
        elif s <= -NCC_MIN and sat <= GREY_SPREAD:
            # darker than what surrounds it, star-shaped: an empty slot of the HUD's row, seen over bright sky
            marks.append("d")
        else:
            marks.append(".")
    # rightmost first: keep the unbroken run from the right; a match beyond a gap is scenery
    run = []
    for m in marks:
        if m == ".":
            break
        run.append(m)
    # order along the row is lit, then grey, then empty slots; a brighter mark left of a dimmer one takes the dimmer class
    rank, out, floor = {"L": 0, "R": 0, "g": 1, "d": 2}, [], 0
    for m in run:
        floor = max(floor, rank[m])
        out.append(m if floor == 0 else "Lgd"[floor])
    return out.count("L") + out.count("R"), out.count("g"), out.count("d"), "".join(marks)


def read_sheet(path, cols=8, cw=None):
    rgb = np.asarray(Image.open(path).convert("RGB"))
    cal = calibrate(rgb, cols, cw)
    if cal is None:
        return None, []
    return cal, [(ri, ci) + read_cell(cell, cal) for ri, ci, cell in cells(rgb, cols, cw)]


def selftest():
    import os
    import tempfile
    img = np.zeros((43, 800, 3), np.uint8)

    def star(x, v):
        img[8:13, x + 2] = v
        img[10, x:x + 5] = v
        img[9:12, x + 1:x + 4] = v
    for x in (65, 80, 92):                 # cell 0: three lit, rightmost slot near the edge
        pass
    for x in (68, 80, 92):
        star(x, 245)
    for x in (168, 180, 192):              # cell 1: lit at the two rightmost, grey at the third
        star(x, 245 if x > 170 else 140)
    img[9:12, 280:292] = 245               # cell 2: a white bar (a digit's stroke) where slots are: not a star
    img[36:40, 0:30] = (230, 220, 40)
    path = os.path.join(tempfile.gettempdir(), "selftest-star-slots.png")
    Image.fromarray(img).save(path)
    cal, r = read_sheet(path)
    ok = bad = 0
    for name, cond in (("calibrated", cal is not None),
                       ("three lit read", bool(r) and r[0][2:4] == (3, 0)),
                       ("two lit and one grey read", bool(r) and r[1][2:4] == (2, 1)),
                       ("a white bar is not a star", bool(r) and r[2][2:4] == (0, 0))):
        if cond:
            ok += 1
        else:
            bad += 1
            print("star_slots selftest FAIL " + name, r[:3] if r else r)
    print("star_slots selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cols = 8
    if "--cols" in sys.argv:
        cols = int(sys.argv[sys.argv.index("--cols") + 1])
        args.remove(str(cols))
    cw = None
    if "--cw" in sys.argv:
        cw = int(sys.argv[sys.argv.index("--cw") + 1])
        args.remove(str(cw))
    cal, rows = read_sheet(args[0], cols, cw)
    if cal is None:
        print("no evenly spaced star row in two or more cells to calibrate from")
        sys.exit(2)
    print("calibration: pitch %.1f px, right %.1f px, star row %.1f px above the area's bottom, patch %d px" % (cal["pitch"], cal["right"], cal["y"], 2 * cal["half"] + 1))
    for ri, ci, lit, grey, dim, marks in rows:
        print("row %d col %d lit %d grey %d empty %d slots %s" % (ri, ci, lit, grey, dim, marks))
