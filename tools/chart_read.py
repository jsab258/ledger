#!/usr/bin/env python3
"""THE COLOUR CHART'S NEUTRALS READ FROM A PICTURE (his order D11, the look method's step 0 and check C2).

    python tools/chart_read.py PICTURE.png [--row 0.648] [--cols 0.398,0.4375,0.479,0.521,0.5605,0.601] [--half 0.010]
    python tools/chart_read.py --selftest

WHY. The calibrator (Unreal's own ColorCalibrator chart, cooked into the packaged game: -OfficeLookCalibrate, CrimeProbe.cpp)
stands 1.6 m before the player's camera at Tom's start; on 28 October its neutrals were read by eye and the reading's
place was kept nowhere. This reads the bottom row's six neutrals (white, 8, 6.5, 5, 3.5, black) at fixed places in
the frame (fractions of its width and height, measured on 28 October's 2560 x 1440 picture, so any size works),
the middle of each patch, and sets them beside X-Rite's published sRGB values and the method's band for neutral 5.

The method's checks (production/research/street-wear/MAFIA-WEAR-2026-10-28.md, calibration): C2, neutral 5 between 110
and 135 of 255; C3, the greys neutral (channels within a few levels of each other).
"""
import sys

import numpy as np

COLS = (0.398, 0.4375, 0.479, 0.521, 0.5605, 0.601)
ROW = 0.648
HALF = 0.010
NAMES = ("white", "neutral 8", "neutral 6.5", "neutral 5", "neutral 3.5", "black")
XRITE = (243, 200, 160, 122, 85, 52)        # X-Rite ColorChecker Classic, published sRGB (MAFIA-WEAR-2026-10-28.md)
BAND5 = (110, 135)


def read(im, cols=COLS, row=ROW, half=HALF):
    h, w = im.shape[:2]
    out = []
    for c in cols:
        x0, x1 = int((c - half) * w), int((c + half) * w)
        y0, y1 = int((row - half * w / h) * h), int((row + half * w / h) * h)
        patch = im[y0:y1, x0:x1].reshape(-1, 3)
        out.append([int(round(float(v))) for v in np.median(patch, axis=0)])
    return out


def judge(vals):
    n5 = float(np.mean(vals[3]))
    spread = max(max(v) - min(v) for v in vals[1:5])
    return {"neutral5": round(n5, 1), "c2": BAND5[0] <= n5 <= BAND5[1], "greySpread": spread, "c3": spread <= 6,
            "stopsFromXrite5": round(float(np.log2(((n5 / 255.0 + 0.055) / 1.055) ** 2.4 / ((122 / 255.0 + 0.055) / 1.055) ** 2.4)), 2)}


def main(a):
    from PIL import Image
    opt = lambda n, d: a[a.index(n) + 1] if n in a else d  # noqa: E731
    cols = tuple(float(x) for x in opt("--cols", ",".join(str(c) for c in COLS)).split(","))
    im = np.asarray(Image.open(a[0]).convert("RGB"), dtype=float)
    vals = read(im, cols, float(opt("--row", ROW)), float(opt("--half", HALF)))
    for n, v, x in zip(NAMES, vals, XRITE):
        print("chart %-12s %3d %3d %3d   (X-Rite %d)" % (n, v[0], v[1], v[2], x))
    j = judge(vals)
    print("chart neutral5=%.1f band=%d-%d C2=%s greySpread=%d C3=%s stopsFromXrite=%+.2f" % (
        j["neutral5"], BAND5[0], BAND5[1], "PASS" if j["c2"] else "FAIL", j["greySpread"], "PASS" if j["c3"] else "FAIL", j["stopsFromXrite5"]))
    return 0


def selftest():
    im = np.zeros((1440, 2560, 3))
    for c, x in zip(COLS, XRITE):
        im[int((ROW - 0.02) * 1440):int((ROW + 0.02) * 1440), int((c - 0.015) * 2560):int((c + 0.015) * 2560)] = x
    vals = read(im)
    j = judge(vals)
    ok = [vals[3] == [122, 122, 122], j["c2"] and j["c3"], abs(j["stopsFromXrite5"]) < 0.01]
    print("chart_read selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(selftest() if "--selftest" in a else main(a))
