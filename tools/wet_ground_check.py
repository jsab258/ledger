#!/usr/bin/env python3
"""THE WET GROUND'S CHECKS FOR ITS STEPS 3 AND 4 (production/research/street-wear/WET-GROUND-METHOD-2026-10-29.md, its
review's last line: "the checks of steps 3 and 4 have no project tool yet; each is written before its step is tried").

    python tools/wet_ground_check.py road HOOK_DAY.png REVERSE_DAY.png     # step 3, water as a coverage
    python tools/wet_ground_check.py decals MARKS_AT_GAIN.json MARKS_AT_DOUBLE.json   # step 4, decals relative
    python tools/wet_ground_check.py --selftest

STEP 3 (the method's own list, each target's source beside it):
  * the Hook sheet's three road regions (his order of 8 October, 2c: hook near lane 152, reverse near centre 164 and
    middle 183, sRGB means, each within 12 levels), read with the lab's boxes (production/lab/road/measure_road.py,
    their one home; imported, not copied);
  * the hook's middle road at least as blue as it is red, as the sheet's (185/188/193; the game's round 3b 118/105/98
    was the "milky" warm sheet);
  * the near lane's spread, linear p90 over p10, at least the sheet's own near road, 1.71 (measured 29 October on
    production/reference/hook-sheet.png, box 1100-1300 x 980-1060 of its 2048x1088): the stone's relief kept under the
    water;
  * the middle road's dash against its road, linear p99.5 over p50, between the sheet's 1.8 and 6 (6 the method's
    inference): a dash that glares, as the morning's 16.8 did, or vanishes.
  Frames of any size are read at 2560x1440, the size the boxes were placed on.

STEP 4: each ground decal's base-colour ratio to its surround moves by under 0.05 when the ground's own base colour is
doubled. Each input is stain_check.py --camera's stain-marks.json for one gain (marks with and without, the same
camera); a mark's ratio is 1 - darkens, so its move is the change in darkens. A mark seen in only one of the two is
listed, not judged.
"""
import importlib.util
import json
import os
import sys

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZE = (2560, 1440)
NEAR_LANE = (461, 1152, 819, 1325)          # the lab's hook near lane (measure_road.py's first target)
MIDDLE_ROAD = (700, 900, 1000, 1040)        # the hook's middle road, colour (29 October, wetmeasure)
DASH_BOX = (720, 940, 900, 1060)            # a stretch of middle road holding dashes (29 October, sheetmeasure)
SPREAD_MIN = 1.71
DASH_RANGE = (1.8, 6.0)
DECAL_MOVE_MAX = 0.05


def road_targets():
    """The 2c targets from their one home, the lab's measure_road.py."""
    path = os.path.join(REPO, "production", "lab", "road", "measure_road.py")
    spec = importlib.util.spec_from_file_location("measure_road", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TARGETS


def linear(v):
    v = np.asarray(v, dtype=float) / 255.0
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def load(path):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    return im.resize(SIZE) if im.size != SIZE else im


def crop(im, box):
    return np.asarray(im.crop(box), dtype=float).reshape(-1, 3)


def luma(px):
    """sRGB luma as PIL's 'L' reads it (ITU-R 601-2), so the 2c means agree with measure_road.py."""
    return px @ np.array([0.299, 0.587, 0.114])


def road(hook, reverse, targets):
    rows = []
    frames = {"hook": hook, "reverse": reverse}
    for view, name, box, want in targets:
        got = float(luma(crop(frames[view], box)).mean())
        rows.append(("2c %s %s" % (view, name), got, "sheet %d, within 12" % want, abs(got - want) <= 12))
    r, g, b = crop(hook, MIDDLE_ROAD).mean(axis=0)
    rows.append(("hook middle road blue - red", float(b - r), "at least 0 (sheet 185/188/193)", b >= r))
    near = np.sort(luma(crop(hook, NEAR_LANE)))
    n = len(near)
    spread = float(linear(near[9 * n // 10]) / max(float(linear(near[n // 10])), 1e-4))
    rows.append(("near lane linear p90/p10", spread, "at least %.2f (sheet's near road)" % SPREAD_MIN, spread >= SPREAD_MIN))
    dash = np.sort(luma(crop(hook, DASH_BOX)))
    m = len(dash)
    ratio = float(linear(dash[int(m * 0.995)]) / max(float(linear(dash[m // 2])), 1e-4))
    rows.append(("middle dash to road, linear", ratio, "%.1f to %.0f (sheet 1.8)" % DASH_RANGE, DASH_RANGE[0] <= ratio <= DASH_RANGE[1]))
    return rows


def decals(a, b):
    """Rows of (mark, darkens at gain, at double, move, ok); marks seen in one run only come back with ok None."""
    seen_a = {r["mark"]: r for r in a if r.get("seen")}
    seen_b = {r["mark"]: r for r in b if r.get("seen")}
    rows = []
    for k in sorted(set(seen_a) | set(seen_b)):
        if k not in seen_a or k not in seen_b:
            rows.append((k, seen_a.get(k, {}).get("darkens"), seen_b.get(k, {}).get("darkens"), None, None))
            continue
        move = abs(seen_a[k]["darkens"] - seen_b[k]["darkens"])
        rows.append((k, seen_a[k]["darkens"], seen_b[k]["darkens"], round(move, 3), move < DECAL_MOVE_MAX))
    return rows


def run_road(hook_path, reverse_path):
    rows = road(load(hook_path), load(reverse_path), road_targets())
    for name, got, want, ok in rows:
        print("wetGround %-30s %7.2f  %-34s %s" % (name, got, want, "ok" if ok else "OUT"))
    bad = sum(not r[3] for r in rows)
    print("wetGroundRoad checks=%d passed=%d failed=%d" % (len(rows), len(rows) - bad, bad))
    return 0 if bad == 0 else 1


def run_decals(a_path, b_path):
    rows = decals(json.load(open(a_path, encoding="utf-8")), json.load(open(b_path, encoding="utf-8")))
    for k, da, db, move, ok in rows:
        if ok is None:
            print("wetGround decal %2d seen in one run only (%s, %s): listed, not judged" % (k, da, db))
        else:
            print("wetGround decal %2d darkens %.3f then %.3f, moves %.3f (under %.2f) %s" % (k, da, db, move, DECAL_MOVE_MAX, "ok" if ok else "OUT"))
    judged = [r for r in rows if r[4] is not None]
    bad = sum(not r[4] for r in judged)
    print("wetGroundDecals marks=%d judged=%d passed=%d failed=%d" % (len(rows), len(judged), len(judged) - bad, bad))
    return 0 if judged and bad == 0 else 1


def selftest():
    from PIL import Image
    ok = []
    # a frame the sheet's own colours would pass: near lane 152 with relief, reverse regions 164 and 183, a faint dash
    hook = np.zeros((SIZE[1], SIZE[0], 3), dtype=np.uint8)
    hook[:, :] = (150, 152, 158)
    x0, y0, x1, y1 = NEAR_LANE
    hook[y0:y1, x0:x1] = (152, 152, 152)
    hook[y0:y1:2, x0:x1] = (130, 130, 130)
    hook[y0 + 1:y1:2, x0:x1] = (172, 172, 172)
    dx0, dy0, dx1, dy1 = DASH_BOX
    hook[dy0:dy0 + 3, dx0:dx1] = (205, 205, 205)                    # under half a percent of the box, the dash
    rev = np.zeros_like(hook)
    rev[:, :] = (164, 164, 164)
    rev[900:1100, 600:1000] = (183, 183, 183)
    rev[1150:1440, 450:1150] = (164, 164, 164)
    targets = (("hook", "near lane", NEAR_LANE, 152), ("reverse", "near centre", (450, 1150, 1150, 1440), 164),
               ("reverse", "middle", (600, 900, 1000, 1100), 183))
    rows = road(Image.fromarray(hook), Image.fromarray(rev), targets)
    ok.append(all(r[3] for r in rows))
    # the milky warm sheet of round 3b fails on colour and on relief
    warm = hook.copy()
    warm[:, :] = (118, 105, 98)
    rows = road(Image.fromarray(warm), Image.fromarray(rev), targets)
    ok.append(not rows[0][3] and not rows[3][3] and not rows[4][3])
    # the lab's own targets load from their home
    ok.append(len(road_targets()) == 3 and road_targets()[0][3] == 152)
    # decals: a black-at-opacity mark holds its ratio, a fixed-colour one does not; a mark seen once is not judged
    a = [{"mark": 0, "seen": True, "darkens": 0.30}, {"mark": 1, "seen": True, "darkens": 0.10}, {"mark": 2, "seen": True, "darkens": 0.2}]
    b = [{"mark": 0, "seen": True, "darkens": 0.31}, {"mark": 1, "seen": True, "darkens": 0.55}, {"mark": 2, "seen": False}]
    d = decals(a, b)
    ok.append(d[0][4] is True and d[1][4] is False and d[2][4] is None)
    print("wet_ground_check selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if a and a[0] == "road":
        sys.exit(run_road(a[1], a[2]))
    if a and a[0] == "decals":
        sys.exit(run_decals(a[1], a[2]))
    print(__doc__)
    sys.exit(2)
