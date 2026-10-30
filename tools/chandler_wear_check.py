#!/usr/bin/env python3
"""THE CHANDLER'S WEAR MEASURED IN THE GAME'S OWN BUFFERS (his order D11, the look; production/research/street-wear/
MAFIA-WEAR-2026-10-28.md, "One shop front: the chandler": S1, S3 and the calibration's C6).

    python tools/chandler_wear_check.py streaks WITH_DIR WITHOUT_DIR     # S3: the brick's streaks on and off, marks off in both
    python tools/chandler_wear_check.py c6 DIR [--without NOMARKS_DIR] [--chart CAL_DIR]   # C6: the brick and each mark's base colour
    python tools/chandler_wear_check.py --selftest

Each DIR is a tools/office_look.py --editor --buffers run (basecolor.png, roughness.png and look-lines.txt, whose
camera line places the wall on screen: tools/stain_check.py project). S1's sheen and colour check is tools/stain_check.py
--camera ... --on east_chandler_bay0, as the office's marks were measured.

S3, the check: the streaks shift the brick's brightness 5 to 15% across a bay in the base-colour view, and every other
house is unchanged. Measured on the bay's upper wall (its brick between the cornice and the eaves, the windows and their
sills and lintels left out) as the ratio of linear luminance with the streaks to without, per pixel: its spread from the
darkest twentieth to the lightest (1 - p5/p95), and across the bay, the spread of the wall's column means (1 - min/max,
columns of 10 px); everywhere else on screen, the share of pixels changed by more than 1%.

C6, the check: albedo 0.03 to 0.88; brick's median 0.09 to 0.36 (linear luminance of the base colour). The bay's brick
median on the same upper wall; each mark of the wear file's chandler bay at its rectangle's middle 60% (the stain check's
footprint), its darkest and lightest fiftieth. With --chart, the calibrator's six neutrals in that run's base-colour view
against X-Rite's (the buffer read as linear base colour; tools/chart_read.py's places).
"""
import json
import os
import re
import sys

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import stain_check  # noqa: E402

CHANDLER = "east_chandler_bay0"
#: the bay's upper wall, street metres: x 40 to 46, from just above the cloud front's cornice to under the eaves, at the
#: frontage (vignette-pieces.json: the bay's face 5.125, its fascia board at 6.1 to 6.3)
WALL = {"x": (40.05, 45.95), "y": (3.75, 6.05), "z": 5.125}
#: what on it is not brick: the two upper windows with their sills and lintels (x 41.5 and 44.5, 0.95 wide, 4.29 to 6.05)
NOT_BRICK = [((41.5 - 0.53, 41.5 + 0.53), (4.27, 6.10)), ((44.5 - 0.53, 44.5 + 0.53), (4.27, 6.10))]
#: the chandler's house, for "everywhere else": its front x 39.6 to 46.1 up past its chimney, and its north wall (the
#: return on the alley, x 46.34, which carries the streaks too: street-wear.json "streak_also"), seen edge on
BAY_ALL = {"x": (39.55, 46.15), "y": (-0.2, 9.5), "z": 5.125}
NORTH_WALL = {"x": 46.34, "y": (-0.2, 6.6), "z": (5.0, 13.3)}
SHIFT_BAND, BRICK_BAND, ALBEDO_BAND = (0.05, 0.15), (0.09, 0.36), (0.03, 0.88)
XRITE_LINEAR = (0.88, 0.59, 0.36, 0.19, 0.09, 0.03)   # the method's neutrals (white, 8, 6.5, 5, 3.5, black), linear
LUM = np.array([0.2126, 0.7152, 0.0722])


def camera(d):
    """The shot's camera from its look-lines.txt: (x, y, z cm, pitch, yaw, horizontal fov)."""
    for line in open(os.path.join(d, "look-lines.txt"), encoding="utf-8", errors="replace"):
        m = re.search(r"shot 1 camera \(([-\d.]+), ([-\d.]+), ([-\d.]+)\) pitch ([-\d.]+) yaw ([-\d.]+) fov ([-\d.]+)", line)
        if m:
            return tuple(float(v) for v in m.groups())
    raise SystemExit("no camera line in %s/look-lines.txt" % d)


def luminance(path):
    return stain_check.srgb_to_linear(stain_check.load(path)) @ LUM


def polygon_mask(cam, corners_m, shape):
    """Pixels inside a rectangle given by four street-metre corners (x, y, z), projected through the camera."""
    from PIL import Image, ImageDraw
    h, w = shape
    pts = [stain_check.project(cam, (x * 100.0, z * 100.0, y * 100.0), w, h) for x, y, z in corners_m]
    img = Image.new("L", (w, h), 0)
    if all(p is not None for p in pts):
        ImageDraw.Draw(img).polygon(pts, fill=1)
    return np.asarray(img, dtype=bool)


def front_rect(xs, ys, z):
    return [(xs[0], ys[0], z), (xs[1], ys[0], z), (xs[1], ys[1], z), (xs[0], ys[1], z)]


def wall_mask(cam, shape):
    m = polygon_mask(cam, front_rect(WALL["x"], WALL["y"], WALL["z"]), shape)
    for xs, ys in NOT_BRICK:
        m &= ~polygon_mask(cam, front_rect(xs, ys, WALL["z"]), shape)
    return m


def column_ratios(lw, lo, m, width=10):
    """The ratio of the two pictures' sums over each `width`-px column of a mask (columns of at least 1,000 px): a
    run's sub-pixel and texture-detail noise averages out over the column, the streaks' tens of centimetres do not."""
    ys, xs = np.nonzero(m & (lo > 0.004))
    a = np.bincount(xs // width, weights=lw[ys, xs])
    b = np.bincount(xs // width, weights=lo[ys, xs])
    n = np.bincount(xs // width)
    k = n >= 1000
    return a[k] / b[k]


def streaks(lw, lo, wall, others, control=None):
    """S3's numbers from two luminance pictures (with and without the streaks), the wall's mask, everywhere else's, and
    a control wall nothing changes between the runs (the neighbour's), whose spread is the runs' own noise."""
    ok = wall & (lo > 0.004)
    r = lw[ok] / lo[ok]
    p5, p50, p95 = (float(np.percentile(r, q)) for q in (5, 50, 95))
    cols = column_ratios(lw, lo, wall)
    col_shift = float(1.0 - cols.min() / cols.max()) if len(cols) else 0.0
    col_shift90 = float(1.0 - np.percentile(cols, 5) / np.percentile(cols, 95)) if len(cols) else 0.0
    o = others & (lo > 0.004)
    changed = float((np.abs(lw[o] / lo[o] - 1.0) > 0.01).mean()) if o.any() else 0.0
    out = {"wall_pixels": int(ok.sum()), "ratio_p5_p50_p95": [round(p5, 4), round(p50, 4), round(p95, 4)],
           "mean_darkening": round(float(1.0 - lw[ok].sum() / lo[ok].sum()), 4), "pixel_shift": round(1.0 - p5 / p95, 4),
           "column_shift": round(col_shift, 4), "column_shift_p5_p95": round(col_shift90, 4), "columns": int(len(cols)),
           "elsewhere_pixels": int(o.sum()), "elsewhere_changed_over_1pc": round(changed, 5)}
    if control is not None:
        cc = column_ratios(lw, lo, control)
        out["control_column_shift"] = round(float(1.0 - cc.min() / cc.max()), 4) if len(cc) else None
        out["control_column_shift_p5_p95"] = round(float(1.0 - np.percentile(cc, 5) / np.percentile(cc, 95)), 4) if len(cc) else None
        out["control_mean_ratio"] = round(float(cc.mean()), 4) if len(cc) else None
    out["ok"] = bool(SHIFT_BAND[0] <= out["column_shift"] <= SHIFT_BAND[1] and out["elsewhere_changed_over_1pc"] < 0.001)
    return out


#: the neighbour's upper wall (the grocer's, east_parade bay 5), nothing on it changed by S3: the runs' noise floor
CONTROL = {"x": (34.6, 39.4), "y": (3.9, 6.0), "z": 5.125}


def run_streaks(with_dir, without_dir):
    cam = camera(with_dir)
    lw = luminance(os.path.join(with_dir, "basecolor.png"))
    lo = luminance(os.path.join(without_dir, "basecolor.png"))
    wall = wall_mask(cam, lw.shape)
    bay = polygon_mask(cam, front_rect(BAY_ALL["x"], BAY_ALL["y"], BAY_ALL["z"]), lw.shape)
    nx, (ny0, ny1), (nz0, nz1) = NORTH_WALL["x"], NORTH_WALL["y"], NORTH_WALL["z"]
    bay |= polygon_mask(cam, [(nx, ny0, nz0), (nx, ny0, nz1), (nx, ny1, nz1), (nx, ny1, nz0)], lw.shape)
    control = polygon_mask(cam, front_rect(CONTROL["x"], CONTROL["y"], CONTROL["z"]), lw.shape)
    res = streaks(lw, lo, wall, ~bay, control)
    res["camera"] = list(cam)
    print("brickStreaks wall=%d px, mean darkening %.1f%%; across the bay (10 px columns) %.1f%% (p5 to p95 %.1f%%; band 5 to 15%%) "
          "over %d columns; the neighbour's wall, unchanged, %.1f%% (p5 to p95 %.1f%%, mean ratio %.3f); elsewhere %.3f%% of %d px "
          "changed over 1%% %s" % (
              res["wall_pixels"], 100 * res["mean_darkening"], 100 * res["column_shift"], 100 * res["column_shift_p5_p95"],
              res["columns"], 100 * (res.get("control_column_shift") or 0), 100 * (res.get("control_column_shift_p5_p95") or 0),
              res.get("control_mean_ratio") or 0, 100 * res["elsewhere_changed_over_1pc"], res["elsewhere_pixels"],
              "PASS" if res["ok"] else "FAIL"))
    json.dump(res, open(os.path.join(with_dir, "brick-streaks.json"), "w", encoding="utf-8"), indent=1)
    return 0 if res["ok"] else 1


def run_c6(d, chart_dir=None, wear_file=None, without_dir=None, chart_row=None):
    cam = camera(d)
    lum = luminance(os.path.join(d, "basecolor.png"))
    # --without (the same view without the bay's marks): a mark is read only where it changes the base colour, so the
    # shop front inside its rectangle, which takes no marks, is not counted as the mark
    lo_lum = luminance(os.path.join(without_dir, "basecolor.png")) if without_dir else None
    wall = wall_mask(cam, lum.shape)
    rows = {"brick_median": round(float(np.median(lum[wall])), 4) if wall.any() else None, "brick_pixels": int(wall.sum())}
    rows["brick_ok"] = bool(rows["brick_median"] is not None and BRICK_BAND[0] <= rows["brick_median"] <= BRICK_BAND[1])
    print("c6 brick median %.4f over %d px (band %.2f to %.2f) %s" % (rows["brick_median"] or 0, rows["brick_pixels"], BRICK_BAND[0],
                                                                     BRICK_BAND[1], "PASS" if rows["brick_ok"] else "FAIL"))
    wear_file = wear_file or os.path.join(REPO, "production", "specs", "street-wear.json")
    marks = [m for m in json.load(open(wear_file, encoding="utf-8"))["decals"] if m["on"] == CHANDLER]
    rows["marks"] = []
    from PIL import Image, ImageDraw
    h, w = lum.shape
    for k, m in enumerate(marks):
        pts = [stain_check.project(cam, p, w, h) for p in stain_check.footprint(m)]
        row = {"mark": k, "kind": m["kind"]}
        if any(p is None for p in pts):
            rows["marks"].append(dict(row, seen=False))
            continue
        img = Image.new("L", (w, h), 0)
        ImageDraw.Draw(img).polygon(pts, fill=1)
        inside = np.asarray(img, dtype=bool) & (lum > 0.0)
        if lo_lum is not None:
            inside &= np.abs(lum - lo_lum) > 0.02 * np.maximum(lo_lum, 1e-3)
        if inside.sum() < 40:
            rows["marks"].append(dict(row, seen=False, pixels=int(inside.sum())))
            continue
        lo, hi = float(np.percentile(lum[inside], 2)), float(np.percentile(lum[inside], 98))
        row.update(seen=True, pixels=int(inside.sum()), p2=round(lo, 4), p98=round(hi, 4),
                   ok=bool(ALBEDO_BAND[0] <= lo and hi <= ALBEDO_BAND[1]))
        rows["marks"].append(row)
        print("c6 mark %d %-9s %6d px: base colour %.4f to %.4f (band %.2f to %.2f) %s" % (
            k, m["kind"], row["pixels"], lo, hi, ALBEDO_BAND[0], ALBEDO_BAND[1], "PASS" if row["ok"] else "FAIL"))
    if chart_dir:
        import chart_read
        # --chart-row: the neutrals' row as a fraction of the height (30 October: 0.562 with the camera tilted 12 degrees up
        # at the chandler, where tools/chart_read.py's 0.648 was measured at Tom's start); its columns are the same
        vals = chart_read.read(stain_check.load(os.path.join(chart_dir, "basecolor.png")) * 255.0, row=chart_row or chart_read.ROW)
        lin = [round(float(stain_check.srgb_to_linear(np.array(v) / 255.0) @ LUM), 4) for v in vals]
        rows["chart_neutrals_linear"] = lin
        rows["chart_xrite_linear"] = list(XRITE_LINEAR)
        print("c6 chart neutrals in the base-colour view, linear: %s against X-Rite's %s" % (lin, list(XRITE_LINEAR)))
    seen = [r for r in rows["marks"] if r.get("seen")]
    rows["ok"] = bool(rows["brick_ok"] and all(r["ok"] for r in seen))
    json.dump(rows, open(os.path.join(d, "c6.json"), "w", encoding="utf-8"), indent=1)
    print("c6 brick=%s marks seen=%d passed=%d" % ("PASS" if rows["brick_ok"] else "FAIL", len(seen), sum(r["ok"] for r in seen)))
    return 0 if rows["ok"] else 1


def selftest():
    ok = []
    h, w = 300, 200
    lo = np.full((h, w), 0.10)
    lw = lo.copy()
    wall = np.zeros((h, w), dtype=bool)
    wall[20:280, 50:150] = True
    lw[20:280, 50:150] *= np.where((np.arange(100) // 10) % 2 == 0, 1.0, 0.9)[None, :]   # 10% darker every other 10 px column
    r = streaks(lw, lo, wall, ~wall)
    ok.append(abs(r["column_shift"] - 0.10) < 0.005 and r["ok"])
    lw2 = lo.copy()
    lw2[0:20, 0:20] = 0.2                                                                # a change outside the bay
    lw2[20:280, 50:150] = lw[20:280, 50:150]
    ok.append(not streaks(lw2, lo, wall, ~wall)["ok"])
    ok.append(not streaks(lo.copy(), lo, wall, ~wall)["ok"])                          # no streaks at all fails 5%
    cam = (4300.0, -400.0, 300.0, 0.0, 90.0, 86.0)
    m = wall_mask(cam, (1080, 1920))
    ok.append(m.sum() > 1000 and not m[540, 960 - 300:960 + 300].all())                # the wall seen, its windows cut out
    print("chandler_wear_check selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or "--selftest" in a:
        sys.exit(selftest())
    if a[0] == "streaks":
        sys.exit(run_streaks(a[1], a[2]))
    if a[0] == "c6":
        sys.exit(run_c6(a[1], a[a.index("--chart") + 1] if "--chart" in a else None,
                        a[a.index("--wear") + 1] if "--wear" in a else None,
                        a[a.index("--without") + 1] if "--without" in a else None,
                        float(a[a.index("--chart-row") + 1]) if "--chart-row" in a else None))
    print(__doc__)
    sys.exit(2)
