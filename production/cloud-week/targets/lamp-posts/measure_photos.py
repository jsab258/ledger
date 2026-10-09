#!/usr/bin/env python
"""Re-makes every photograph measurement of the lamp-post target from the Poly Haven panoramas and writes photo_measurements.json.

    /home/user/.bpyenv/bin/python measure_photos.py PANO_DIR        (PANO_DIR holds tm_bethnal_green_entrance.jpg and tm_urban_street_01.jpg, 8192 x 4096)

Scales. Each panorama has no recorded camera height. This target uses the heights the bollards' target measured and its reviewer re-measured
(production/cloud-week/targets/bollards/TARGET.md section 3, calibrate.py there), each AT THE OBJECT'S OWN GROUND:
  bethnal_green_entrance (BGE): 1.02 +-0.07 m on the block paving the column stands on (the planter wall on that paving: 0.96 by the bollards' writer, 1.03 to 1.04 by
     the reviewer; this writer's own horizon fit 0.96); every BGE length below is therefore +-7 % in absolute size (the proportions are exact to the pixel)
  urban_street_01 (US01): the garden wall and gate pier on the footway: 1.16 +-0.07 m above the footway (1.23 above the planting bed 0.07 m lower, the bollards' value)
The column's horizontal distance d comes from the depression angle of its foot: d = camera height / tan(angle), plus its radius to the axis.
BGE: foot front at row 2524 of 4096 (-20.9 deg) -> 2.665 m; axis 2.665 + 0.062 = 2.73 m, bearing 138.5 deg (the column's own centre column u = 7249 of 8192).
US01: the column's foot is hidden by a car; its distance is read from the gate pier beside it (foot at -7.9 deg -> 8.4 m) and the lowest visible sleeve point
(-7.15 deg -> 9.2 m): 8.8 +-0.6 m, bearing -15.7 deg. Only RATIOS from US01 are used by the target (its column is a taller class, about 11 m).
"""
import json
import os
import sys

import numpy as np
from scipy.ndimage import gaussian_filter1d

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lamp_lib as L  # noqa: E402

PANO = sys.argv[1]
BGE = dict(pano="bethnal_green_entrance", yaw=138.5, d=2.73, cam=1.02, cam_err=0.07)
US01 = dict(pano="urban_street_01", yaw=-15.7, d=8.8, cam=1.16, cam_err=0.07, d_err=0.6)
out = {"written": "2026-10-09", "frames": {"BGE": BGE, "US01": US01}, "method": {}}


def edge_fit(img, fr, z, expect_left, expect_right, win=14, rows=8, mm=1):
    """left and right edges of a dark column at height z (mm): strongest negative / positive luminance gradient of the row-averaged profile in a window of +-win mm round the
    expected edges. Returns (xl, xr, width, gradient_left, gradient_right)."""
    e = L.elevation(img, fr["yaw"], fr["d"], fr["cam"], -300, 400, z - rows, z + rows, mm)
    prof = L.luminance(e).mean(0)
    g = np.gradient(gaussian_filter1d(prof, 1.2))
    xs = np.arange(-300, 400, mm) + mm / 2
    lw = (xs > expect_left - win) & (xs < expect_left + win)
    rw = (xs > expect_right - win) & (xs < expect_right + win)
    li = int(np.argmin(np.where(lw, g, 1e9)))
    ri = int(np.argmax(np.where(rw, g, -1e9)))
    return float(xs[li]), float(xs[ri]), float(xs[ri] - xs[li]), float(g[li]), float(g[ri])


def main():
    img = L.load(PANO, BGE["pano"])
    # ---- BGE sleeve: left/right edges at z 100 .. 800, expected -56 and +67 -------------------------------------------------------
    rows = []
    for z in range(100, 900, 100):
        xl, xr, w, gl, gr = edge_fit(img, BGE, z, -56, 67)
        rows.append({"z": z, "xl": xl, "xr": xr, "width": w, "grad_l": round(gl, 1), "grad_r": round(gr, 1)})
    out["bge_sleeve_width"] = {"rows": rows, "mean_width": round(float(np.mean([r["width"] for r in rows])), 1),
                               "centre_x": round(float(np.mean([(r["xl"] + r["xr"]) / 2 for r in rows])), 1)}
    # ---- BGE shaft: gradient fit where the contrast is strong (against brick at z 1700 to 1900, against the sky at 3800 to 4000) -----
    sh = []
    for z, el, er in [(1700, -25, 42), (1800, -32, 37), (1900, -33, 36), (3800, -21, 39), (3900, -21, 39), (4000, -21, 39)]:
        xl, xr, w, gl, gr = edge_fit(img, BGE, z, el, er, win=12)
        sh.append({"z": z, "xl": xl, "xr": xr, "width": w, "grad_l": round(gl, 1), "grad_r": round(gr, 1)})
    out["bge_shaft_width"] = {"rows": sh}
    # ---- BGE shoulder: width profile z 940 .. 1080 each 10 mm, window +-14 round the cone of the nominal profile -------------------
    prof = []
    for z in range(940, 1090, 10):
        if z < 978:
            hl, hr = -56, 67
        elif z < 1040:
            t = (z - 978) / 62.0
            hl, hr = -56 + t * 27, 67 - t * 27
        else:
            hl, hr = -25, 41
        xl, xr, w, gl, gr = edge_fit(img, BGE, z, hl, hr, win=10, rows=3)
        prof.append({"z": z, "xl": xl, "xr": xr, "width": w, "grad_l": round(gl, 1), "grad_r": round(gr, 1)})
    out["bge_shoulder_profile"] = {"rows": prof}
    # ---- BGE pod: the elevation of the pod's own silhouette against the pale sky (z 4000 to 4800), widest row ------------------------
    e = L.elevation(img, BGE["yaw"], BGE["d"], BGE["cam"], -400, 400, 3900, 4900, 1)
    lum = L.luminance(e)
    sky = float(np.percentile(lum[:100], 50))
    mask = lum < sky - 40
    widest = (0, 0, 0, 0)
    for r in range(mask.shape[0]):
        idx = np.where(mask[r, 100:700])[0]
        if len(idx) < 50:
            continue
        runs = np.split(idx, np.where(np.diff(idx) > 3)[0] + 1)
        big = max(runs, key=len)
        if len(big) > widest[0]:
            widest = (len(big), int(big[0] + 100 - 400), int(big[-1] + 100 - 400), 4900 - r)
    out["bge_pod"] = {"sky_luminance": round(sky, 1), "widest_run_mm": widest[0], "x_left": widest[1], "x_right": widest[2], "at_picture_z_mm": widest[3],
                      "note": "silhouette of the pod seen from below at about 51 degrees: the horizontal extreme is in the plane through the axis, so the width is the true diameter within the scale error; its height cannot be read from below"}
    # pod centre height from the angles of its top and bottom limb in the panorama (rows read on the 8192 x 4096 picture)
    out["bge_pod_angles"] = {"top_row": 824, "bottom_row": 944, "el_top_deg": round((0.5 - 824 / 4096) * 180, 2), "el_bottom_deg": round((0.5 - 944 / 4096) * 180, 2),
                             "centre_height_m": round(BGE["cam"] + BGE["d"] * float(np.tan(np.radians((0.5 - 884 / 4096) * 180))), 2),
                             "note": "the disc's own foreshortened width (about 0.33 m seen from 51 degrees) makes up most of the 5.4 degrees between the rows; so the thickness is not read"}
    # ---- BGE colours (median sRGB of the tone-mapped JPG; reflections make the p90 brighter) --------------------------------------------
    def samp(x0, x1, z0, z1):
        a = L.elevation(img, BGE["yaw"], BGE["d"], BGE["cam"], x0, x1, z0, z1, 2).reshape(-1, 3)
        return {"median": np.median(a, 0).round(0).tolist(), "p10": np.percentile(a, 10, 0).round(0).tolist(), "p90": np.percentile(a, 90, 0).round(0).tolist()}
    out["bge_colours"] = {"sleeve_paint_z500_900": samp(-35, 55, 500, 900), "sleeve_splash_z20_250": samp(-35, 55, 20, 250),
                          "sleeve_z250_480": samp(-35, 55, 250, 480), "shaft_z1300_1600": samp(-12, 30, 1300, 1600)}
    # ---- US01 -------------------------------------------------------------------------------------------------------------------------
    im1 = L.load(PANO, US01["pano"])
    e = L.elevation(im1, US01["yaw"], US01["d"], US01["cam"], -1800, 400, 8800, 11400, 2)
    lum = L.luminance(e)
    sky = float(np.median(lum[:50, -100:]))
    thr = sky - 45
    x0, z1, mm = -1800, 11400, 2

    def runs_of(row):
        idx = np.where(row < thr)[0]
        return [] if len(idx) == 0 else np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    shaft = []
    for z in range(8900, 9800, 100):
        rs = [a for a in runs_of(lum[int((z1 - z) / mm)]) if len(a) > 2]
        if rs:
            a = max(rs, key=len)
            shaft.append({"z": z, "x_left": x0 + int(a[0]) * mm, "x_right": x0 + int(a[-1]) * mm, "width": (len(a)) * mm})
    stem = []
    for z in (9800, 9900, 10000):
        rs = [a for a in runs_of(lum[int((z1 - z) / mm)]) if len(a) > 2]
        if rs:
            a = max(rs, key=len)
            stem.append({"z": z, "x_left": x0 + int(a[0]) * mm, "x_right": x0 + int(a[-1]) * mm, "width": len(a) * mm})
    # arm: vertical thickness at columns along the straight part, converted with the slope seen in the picture
    arm = []
    for x in range(-1100, -140, 80):
        c = int((x - x0) / mm)
        idx = np.where(lum[:, c] < thr)[0]
        if len(idx) == 0:
            continue
        for a in np.split(idx, np.where(np.diff(idx) > 1)[0] + 1):
            zc = z1 - (a[0] + a[-1]) / 2 * mm
            if 10000 <= zc <= 11300 and 30 <= len(a) * mm <= 140:
                arm.append({"x": x, "z_centre": round(zc, 1), "vertical_thickness": len(a) * mm})
    slope = np.polyfit([a["x"] for a in arm], [a["z_centre"] for a in arm], 1)[0]
    out["us01_top"] = {"sky_luminance": round(sky, 1), "shaft": shaft, "stem": stem, "arm": arm, "arm_slope_in_picture": round(float(slope), 3),
                       "shaft_mean_width": round(float(np.mean([s["width"] for s in shaft])), 1),
                       "stem_mean_width": round(float(np.mean([s["width"] for s in stem])), 1) if stem else None,
                       "arm_perpendicular_width": round(float(np.mean([a["vertical_thickness"] for a in arm]) * np.cos(np.arctan(abs(slope)))), 1),
                       "note": "the arm's slope in the picture (about 43 degrees) is NOT its rake: the arm points partly out of the plane; only widths are used (as ratios to the shaft)"}
    # sleeve and shoulder on US01 (z 0 .. 1000): widths by dark-run at 100 mm steps; the bonnet of a parked car crosses the lower left, so the left edge is read only above z 250
    e = L.elevation(im1, US01["yaw"], US01["d"], US01["cam"], -400, 400, 0, 1800, 3)
    lu = L.luminance(e)
    sl = []
    for z in range(300, 900, 100):
        row = lu[int((1800 - z) / 3)]
        sl.append({"z": z, "min": int(row.min())})
    out["us01_sleeve_note"] = {"sleeve_width_mm_at_8p8m": 232, "shaft_above_mm_at_8p8m": 113, "sleeve_top_z": 880, "reading": "by eye on the gridded elevation (g_us01_base): left edge -115, right edge +117 at z 300 to 800; shaft above -63 to +50; the ratio sleeve / shaft 2.05"}
    # lit glow colour of the lantern, seen from below (a rectilinear view 5 degrees wide aimed at the lantern)
    v = L.view(im1, -23.5, 49, 5, 800, 800)
    a = v.reshape(-1, 3)
    sat = a.max(1) - a.min(1)
    m = (a[:, 0] > 180) & (a[:, 2] < 140) & (sat > 90)
    lum_a = a @ np.array([0.2126, 0.7152, 0.0722])
    core = a[np.argsort(lum_a)[-200:]].mean(0)
    out["us01_lit_lantern"] = {"orange_pixels": int(m.sum()), "median": np.median(a[m], 0).round(0).tolist(), "p10": np.percentile(a[m], 10, 0).round(0).tolist(),
                               "p90": np.percentile(a[m], 90, 0).round(0).tolist(), "core_200_brightest": core.round(0).tolist(),
                               "note": "tone-mapped 2019 photograph, daylight white balance, overcast sky behind; the lamp type (sodium or not) is unknown; the clipped core is over-exposure"}
    json.dump(out, open(os.path.join(HERE, "photo_measurements.json"), "w"), indent=1)
    print("wrote photo_measurements.json")
    print("BGE sleeve width mean", out["bge_sleeve_width"]["mean_width"], "centre", out["bge_sleeve_width"]["centre_x"])
    print("BGE shaft", [(r["z"], r["width"]) for r in sh])
    print("BGE pod", out["bge_pod"])
    print("US01 shaft mean", out["us01_top"]["shaft_mean_width"], "stem", out["us01_top"]["stem_mean_width"], "arm perp", out["us01_top"]["arm_perpendicular_width"])
    print("US01 lit", out["us01_lit_lantern"])


if __name__ == "__main__":
    main()
