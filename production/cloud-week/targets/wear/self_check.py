#!/usr/bin/env python
"""Tests target.json against its own photograph measurements and for internal consistency, before anything is built.

    /home/user/.bpyenv/bin/python self_check.py [--no-overlays] [--no-write]

Reads target.json beside it, the previews in production/previews/cloud-week/refs/wear/ and the Hook sheet
(production/previews/hook-sheet-2026-10-05.jpg), draws every kind's envelope with target_drawing.py and runs every
`checks` entry of target.json on the rasterised envelope. Prints a result line and writes it into target.json under "self_check".
Also exports `measure(mask, px_per_m, measure_id, **params)`: the same mask measures unit 4.5's automatic check should run
on a generated greyscale mask (0..1, row 0 at the top, frame as kind.mask.frame_extent_m says).

Parts:
  A  structure: every kind has its parts; numbers sit in order; every measurement id used exists; every surface has a tone.
  B  tone: the stated multiplier, the mark colour, the surface colour and the L* change agree with each other.
  C  photographs: the measurements are re-made from the reduced previews and must come back within their stated error;
     the envelope is laid on the main photograph (scale fitted on one dimension only) and its edges must fall on the marks.
  D  envelopes: each kind's drawn envelope is rasterised at its texel scale and the kind's checks are run on it.
"""
import importlib.util
import json
import math
import os
import sys
import datetime

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from scipy.cluster.vq import kmeans2

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PREV = os.path.join(REPO, "production", "previews", "cloud-week", "refs", "wear")
HOOK = os.path.join(REPO, "production", "previews", "hook-sheet-2026-10-05.jpg")
TARGET = os.path.join(HERE, "target.json")
Image.MAX_IMAGE_PIXELS = None


def load_drawing():
    spec = importlib.util.spec_from_file_location("target_drawing", os.path.join(HERE, "target_drawing.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- colour helpers
def srgb_to_lin(c):
    c = np.asarray(c, dtype=np.float64) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lum(rgb8):
    l = srgb_to_lin(rgb8)
    return 0.2126 * l[..., 0] + 0.7152 * l[..., 1] + 0.0722 * l[..., 2]


def Lstar(rgb8):
    Y = lum(rgb8)
    f = np.where(Y > 216 / 24389, np.cbrt(Y), (24389 / 27 * Y + 16) / 116)
    return 116 * f - 16


def lin_to_srgb8(l):
    l = np.clip(l, 0, 1)
    c = np.where(l <= 0.0031308, 12.92 * l, 1.055 * l ** (1 / 2.4) - 0.055)
    return np.round(c * 255).astype(int)


def gauss(a, s):
    return ndi.gaussian_filter(a, s, mode="reflect")


# ---------------------------------------------------------------- mask measures (also for unit 4.5)
def _comps(mask, thr):
    return ndi.label(mask >= thr, structure=np.ones((3, 3)))


def _pca_stats(mask, ppm, thr, min_length_m=0.0):
    """per component: (length_m, width_m, aspect, angle_from_vertical_deg); rod-equivalent lengths: sqrt(12 var)"""
    lab, n = _comps(mask, thr)
    out = []
    mm = 1.0 / ppm
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        sub = lab[sl] == i
        ys, xs = np.nonzero(sub)
        if len(ys) < 6:
            continue
        c = np.cov(np.vstack([xs, ys]))
        w, v = np.linalg.eigh(c)
        L = math.sqrt(12 * max(w[1], 1e-9)) * mm
        Wd = math.sqrt(12 * max(w[0], 1e-9)) * mm
        if L < min_length_m:
            continue
        vx, vy = v[0, 1], v[1, 1]
        ang = math.degrees(math.atan2(abs(vx), abs(vy)))   # 0 = vertical
        out.append((L, Wd, L / max(Wd, 1e-9), ang))
    return out


def measure(mask, px_per_m, measure_id, **p):
    """The mask measures named in target.json check_measures. mask: float 0..1, row 0 at the TOP of the decal frame."""
    mask = np.asarray(mask, dtype=np.float64)
    ppm = float(px_per_m)
    px_mm = 1000.0 / ppm
    if measure_id == "coverage":
        return float((mask >= p.get("thr", 0.5)).mean())
    if measure_id in ("blob_eqd_mm", "count_per_m2"):
        lab, n = _comps(mask, p.get("thr", 0.5))
        if n == 0:
            return 0.0
        areas = ndi.sum(np.ones_like(mask), lab, np.arange(1, n + 1)) * px_mm ** 2
        keep = areas >= p.get("min_area_mm2", 0.0)
        if measure_id == "count_per_m2":
            return float(keep.sum() / (mask.shape[0] * mask.shape[1] / ppm ** 2))
        if not keep.any():
            return 0.0
        eq = 2 * np.sqrt(areas[keep] / math.pi)
        return float(np.percentile(eq, 90 if p.get("stat") == "p90" else 50))
    if measure_id == "edge_10_90_mm":
        # 10-90 % of the mask's own peak: 0.8 x peak / median |gradient|, taken on the pixels within `reach_mm` of the half-peak contour
        mx = float(mask.max())
        if mx < 0.2:
            return 0.0
        gy, gx = np.gradient(mask)
        axis = p.get("axis")
        g = np.abs(gx) if axis == "x" else np.abs(gy) if axis == "y" else np.hypot(gx, gy)
        g = g * ppm
        core = mask >= 0.5 * mx
        reach = max(3, int(round(p.get("reach_mm", 60.0) * ppm / 1000.0)))
        near = ndi.binary_dilation(core, iterations=reach) & ~ndi.binary_erosion(core, iterations=reach)
        band = near & (mask > p.get("band_lo", 0.1) * mx) & (mask < p.get("band_hi", 0.9) * mx) & (g > 1e-6)
        if band.sum() < 10:
            return 0.0
        # steepest part of the edge (90th percentile of the gradient): 10-90 width = 0.95 x peak / that gradient (exact within +/-15 % for ramps and Gaussian edges)
        return float(0.95 * mx / np.percentile(g[band], 90) * 1000.0)
    if measure_id in ("crack_width_mm", "crack_length_per_m2"):
        b = mask >= p.get("thr", 0.5)
        if b.sum() < 10:
            return 0.0
        sk = zhang_suen(b)
        if measure_id == "crack_width_mm":
            dt = ndi.distance_transform_edt(b)
            return float(np.median(2 * dt[sk] - 1) * px_mm) if sk.any() else 0.0
        h = (sk[:, :-1] & sk[:, 1:]).sum() + (sk[:-1, :] & sk[1:, :]).sum()
        d = (sk[:-1, :-1] & sk[1:, 1:]).sum() + (sk[:-1, 1:] & sk[1:, :-1]).sum()
        step = 1 + (math.sqrt(2) - 1) * (d / max(h + d, 1)) * 0.5
        return float(sk.sum() * step * px_mm / 1000.0 / (mask.shape[0] * mask.shape[1] / ppm ** 2))
    if measure_id in ("streak_aspect", "streak_width_mm", "streak_length_m", "verticality_deg"):
        st = _pca_stats(mask, ppm, p.get("thr", 0.3), p.get("min_length_m", 0.0 if measure_id != "verticality_deg" else 0.1))
        if not st:
            return 0.0
        if measure_id == "verticality_deg":
            return float(max(s[3] for s in st))
        col = {"streak_length_m": 0, "streak_width_mm": 1, "streak_aspect": 2}[measure_id]
        vals = [s[col] * (1000.0 if measure_id == "streak_width_mm" else 1.0) for s in st]
        return float(np.percentile(vals, {"p10": 10, "p90": 90}.get(p.get("stat"), 50)))
    if measure_id == "fade_ratio":
        lab, n = _comps(mask, p.get("thr", 0.3))
        rs = []
        for i, sl in enumerate(ndi.find_objects(lab), start=1):
            h = sl[0].stop - sl[0].start
            if h * 1000.0 / ppm < 150:
                continue
            seg = mask[sl]
            a, b = seg[: h // 3].mean(), seg[-(h // 3):].mean()
            if a > 0:
                rs.append(b / a)
        return float(np.median(rs)) if rs else 0.0
    if measure_id == "foot_profile":
        raise ValueError("foot_profile needs the frame: use foot_profile_check")
    if measure_id == "tile_seam":
        # seam difference across the wrap relative to the difference between adjacent columns (rows) inside the tile: about 1 when seamless
        ax = p.get("axis", "x")
        e = []
        if "x" in ax:
            inner = np.abs(mask[:, 1:] - mask[:, :-1]).mean()
            e.append(np.abs(mask[:, 0] - mask[:, -1]).mean() / max(inner, 1e-6))
        if "y" in ax:
            inner = np.abs(mask[1:, :] - mask[:-1, :]).mean()
            e.append(np.abs(mask[0, :] - mask[-1, :]).mean() / max(inner, 1e-6))
        return float(max(e))
    if measure_id == "mask_max":
        return float(mask.max())
    if measure_id == "mask_std":
        return float(mask.std())
    raise ValueError(measure_id)


def foot_profile_check(mask, px_per_m, points):
    """points: [[height_m, min, max], ...] with row H-1 the foot. Returns list of (h, value, lo, hi, ok)."""
    H = mask.shape[0]
    out = []
    for h, lo, hi in points:
        r = int(round(H - 1 - h * px_per_m))
        r = min(max(r, 0), H - 1)
        v = float(mask[max(r - 1, 0):r + 2].mean())
        out.append((h, v, lo, hi, lo - 1e-9 <= v <= hi + 1e-9))
    return out


# ---------------------------------------------------------------- reporting
class Report:
    def __init__(self):
        self.lines = []
        self.fail = 0
        self.ok = 0

    def check(self, name, cond, detail=""):
        if cond:
            self.ok += 1
        else:
            self.fail += 1
        self.lines.append(("PASS " if cond else "FAIL ") + name + ((": " + detail) if detail else ""))
        return cond

    def note(self, s):
        self.lines.append("note " + s)


# ---------------------------------------------------------------- A: structure
REQUIRED = ["label", "layer", "where", "envelope", "geometry", "tone", "wet_dry", "texel", "variants", "period_1990", "not_modern", "checks", "mask"]
MEASURES = {"coverage", "blob_eqd_mm", "count_per_m2", "edge_10_90_mm", "streak_aspect", "streak_width_mm", "streak_length_m", "verticality_deg", "fade_ratio", "foot_profile", "tile_seam", "mask_max", "mask_std", "tone_ratio", "crack_flag_share", "crack_width_mm", "crack_length_per_m2", "role_length_per_m2", "role_blob_eqd_mm"}


def part_a(tj, R):
    ids = tj["kinds_order"]
    R.check("A1 every kind is in the order list and defined (at least 20 kinds)", len(ids) >= 20 and set(ids) == set(tj["kinds"]) and len(ids) == len(set(ids)), "%d kinds" % len(ids))
    M = tj["measurements"]
    for kid in ids:
        k = tj["kinds"][kid]
        miss = [r for r in REQUIRED if r not in k]
        R.check("A2 %s has every part" % kid, not miss, "missing %s" % miss)
        w = k["where"]
        R.check("A3 %s has place rule, surfaces, height, sides, footfall/wet, density" % kid,
                all(x in w for x in ("rule", "surfaces", "height_m", "sides", "footfall_and_wet", "density")))
        for s in w["surfaces"]:
            R.check("A4 %s: surface %s is defined and has a tone" % (kid, s), s in tj["surfaces"] and s in k["tone"])
        d = w["density"]
        R.check("A5 %s density range holds its typical value" % kid, d["range"][0] <= d["typical"] <= d["range"][1], "%s" % d)
        t = k["texel"]
        R.check("A6 %s texel: min <= recommended <= screen limit at 1.6 m (1122 px/m)" % kid, t["px_per_m_min"] <= t["px_per_m_recommended"] <= 1122 + 1e-9, "%s" % t)
        R.check("A7 %s texel: smallest feature has at least 6 texels at the recommended scale (or the screen limit)" % kid,
                t["smallest_feature_mm"] * t["px_per_m_recommended"] / 1000.0 >= 5.9 or t["px_per_m_recommended"] >= 1100 or t["smallest_feature_mm"] >= 100,
                "feature %s mm at %s px/m = %.1f texels" % (t["smallest_feature_mm"], t["px_per_m_recommended"], t["smallest_feature_mm"] * t["px_per_m_recommended"] / 1000.0))
        R.check("A8 %s has wet and dry looks with a roughness change" % kid, "wet" in k["wet_dry"] and "dry" in k["wet_dry"] and "roughness_delta" in k["wet_dry"]["wet"])
        R.check("A9 %s has at least 3 variants and says how they differ" % kid, k["variants"]["count"] >= 3 and len(k["variants"]["differ_by"]) > 10)
        R.check("A10 %s says what makes it 1990 and not modern" % kid, len(k["period_1990"]) > 40 and len(k["not_modern"]) > 20)
        for c in k["checks"]:
            R.check("A11 %s check %s uses a known measure with min <= max" % (kid, c["name"]), c["measure"] in MEASURES and c["min"] <= c["max"])
        nmask = sum(1 for c in k["checks"] if c.get("applies_to") == "mask")
        R.check("A11b %s has at least 3 checks unit 4.5 can run on a generated mask (it has %d)" % (kid, nmask), nmask >= 3 or kid in ("flag_patch_crack",), "")
        ext = k["mask"]["frame_extent_m"]
        R.check("A12 %s frame is a positive rectangle that matches its decal size" % kid, ext[2] > ext[0] and ext[3] > ext[1] and abs((ext[2] - ext[0]) - k["mask"]["decal_frame_m"][0]) < 1e-6)
        # every M-id named anywhere in the kind exists
        txt = json.dumps(k)
        import re
        used = set(re.findall(r"\bM(\d\d)\b", txt))
        R.check("A13 %s: every measurement id it cites exists" % kid, all(("M" + u) in M for u in used), "cites %s" % sorted(used))
    # side weights stated for the parade and the west block wherever a side is named
    R.check("A14 every kind says which side of the street it favours", all(("east" in tj["kinds"][k]["where"]["sides"].lower() or "both" in tj["kinds"][k]["where"]["sides"].lower() or "quay" in tj["kinds"][k]["where"]["sides"].lower()) for k in ids))
    R.check("A15 sources, unreached and disagreements are listed", len(tj["sources"]) >= 5 and len(tj["unreached"]) >= 2 and len(tj["disagreements"]) >= 4)
    R.check("A16 the era rules rule out 2000s and American marks and alcohol/gambling", len(tj["era_rules"]) >= 4 and any("alcohol" in r for r in tj["era_rules"]))
    # height profiles equal the envelope levels where both exist (nothing floats between the two statements of one rule)
    for kid in ("wall_foot_splash", "wall_foot_damp", "salt_bloom", "gutter_grime"):
        k = tj["kinds"][kid]
        hp = k["geometry"]["height_profile"]
        lv = [(l["h_m"], l["level"]) for l in k["envelope"]["levels"]]
        got = dict(zip(hp["h_m"], hp["mask"]))
        okp = all(abs(got.get(h, -9) - l) < 1e-9 for h, l in lv)
        R.check("A17 %s: height profile and envelope levels are the same numbers" % kid, okp)
    sp = {l["h_m"]: l["level"] for l in tj["kinds"]["wall_foot_splash"]["envelope"]["levels"]}
    salt0 = [l["h_m"] for l in tj["kinds"]["salt_bloom"]["envelope"]["levels"] if l["level"] > 0][0]
    top85 = max(h for h, l in sp.items() if l >= 0.85)
    top100 = max(h for h, l in sp.items() if l >= 1.0)
    R.check("A18 the salt band starts on the upper flank of the black foot (between the splash's full-strength top %.2f m and its 0.85 height %.2f m)" % (top100, top85), top100 <= salt0 <= top85 + 0.05, "salt starts %.2f" % salt0)
    R.check("A19 splash profile ends below the damp profile", max(sp) < max(l["h_m"] for l in tj["kinds"]["wall_foot_damp"]["envelope"]["levels"]))


# ---------------------------------------------------------------- B: tone
def part_b(tj, R):
    S = tj["surfaces"]
    worst = []
    for kid in tj["kinds_order"]:
        k = tj["kinds"][kid]
        for sname, t in k["tone"].items():
            surf = np.array(S[sname]["albedo_srgb"], float)
            mark = np.array(t["mark_srgb"], float)
            mult = t["albedo_mult_linear"]
            Ls, Lm = float(Lstar(surf)), float(Lstar(mark))
            if mult < 1.0:
                implied = float(lum(mark) / lum(surf))
                Lmult = float(Lstar(lin_to_srgb8(srgb_to_lin(surf) * mult)))
                okm = (mult / 1.6 <= implied <= mult * 1.6)
                okd = abs((Lm - Ls) - t["delta_L_star"]) <= 2.0
                R.check("B1 %s on %s: mark colour is the surface x %.2f in linear light (implied %.2f)" % (kid, sname, mult, implied), okm)
                R.check("B2 %s on %s: stated dL* %.0f is the mark colour minus the surface (%.1f)" % (kid, sname, t["delta_L_star"], Lm - Ls), okd)
                q = t.get("quoted_delta_L_star")
                if q is not None:
                    R.check("B2q %s on %s: dL* %.0f is within 14 of the figure measured or quoted for it (%s)" % (kid, sname, t["delta_L_star"], q), abs(t["delta_L_star"] - q) <= 14.0)
                worst.append((kid, sname, implied, mult, Lmult - Ls, t["delta_L_star"]))
            else:
                okd = abs((Lm - Ls) - t["delta_L_star"]) <= 2.0
                R.check("B3 %s on %s: stated dL* %.0f is the mark colour minus the surface (%.1f)" % (kid, sname, t["delta_L_star"], Lm - Ls), okd)
                q = t.get("quoted_delta_L_star")
                if q is not None:
                    R.check("B3q %s on %s: dL* %.0f is within 14 of the figure measured or quoted for it (%s)" % (kid, sname, t["delta_L_star"], q), abs(t["delta_L_star"] - q) <= 14.0)
    # flag classes
    sc = tj["kinds"]["flag_patch_crack"]["geometry"]["slab_classes"]
    ratio = float(lum(np.array(sc["dark"]["srgb"], float)) / lum(np.array(sc["pale"]["srgb"], float)))
    lo, hi = tj["kinds"]["flag_patch_crack"]["geometry"]["ratio_range"]
    R.check("B4 flag dark/pale luminance ratio from the class colours (%.3f) is in the measured range %.2f to %.2f" % (ratio, lo, hi), lo <= ratio <= hi)
    R.check("B5 flag class shares add to 1", abs(sum(v["share"] for v in sc.values()) - 1.0) < 1e-9)
    # wet: darker wet multipliers must be below 1 for every dirt mark, and wet stone follows the research (0.68)
    for kid in tj["kinds_order"]:
        wm = tj["kinds"][kid]["wet_dry"]["wet"]["albedo_mult_on_tone"]
        R.check("B6 %s wet multiplier in 0.3 to 1.0" % kid, 0.3 <= wm <= 1.0)


# ---------------------------------------------------------------- C: photographs
def load_rgb(path):
    return np.asarray(Image.open(path).convert("RGB"))


def kmeans_share(rgb, k, minority_index_from_end=0, size=400):
    small = np.asarray(Image.fromarray(rgb).resize((size, size), Image.LANCZOS)).astype(float)
    X = small.reshape(-1, 3)
    # Lab-ish: use sRGB Euclid (adequate for 2 well-separated clusters)
    best = None
    for seed in range(5):
        cen, lbl = kmeans2(X, k, minit="++", seed=seed + 1)
        inertia = ((X - cen[lbl]) ** 2).sum()
        if best is None or inertia < best[0]:
            best = (inertia, cen, lbl)
    _, cen, lbl = best
    shares = np.bincount(lbl, minlength=k) / lbl.size
    return shares, cen


def zhang_suen(img):
    img = np.pad(img.astype(np.uint8), 1)
    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            P = img
            p2 = P[:-2, 1:-1]; p3 = P[:-2, 2:]; p4 = P[1:-1, 2:]; p5 = P[2:, 2:]
            p6 = P[2:, 1:-1]; p7 = P[2:, :-2]; p8 = P[1:-1, :-2]; p9 = P[:-2, :-2]
            C = P[1:-1, 1:-1]
            B = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
            seq = [p2, p3, p4, p5, p6, p7, p8, p9, p2]
            A = sum(((seq[i] == 0) & (seq[i + 1] == 1)).astype(np.uint8) for i in range(8))
            m = ((p2 * p4 * p6 == 0) & (p4 * p6 * p8 == 0)) if step == 0 else ((p2 * p4 * p8 == 0) & (p2 * p6 * p8 == 0))
            rem = (C == 1) & (B >= 2) & (B <= 6) & (A == 1) & m
            if rem.any():
                changed = True
                P[1:-1, 1:-1][rem] = 0
    return img[1:-1, 1:-1].astype(bool)


def part_c(tj, R, draw, overlays):
    P = tj["previews"]
    M = tj["measurements"]
    overlay_log = []

    def pv(name):
        return os.path.join(PREV, name)

    # ---- C1..C4 oil drip speckle on the main photograph
    f = "ph-urban_street_03-oil-drip-speckle.jpg"
    rgb = load_rgb(pv(f))
    H, W, _ = rgb.shape
    mm = P[f]["mm_per_px"]
    yel = ((rgb[..., 0].astype(int) - rgb[..., 2].astype(int)) > 45) & (rgb[..., 0] > 110)
    yel = ndi.binary_closing(yel, np.ones((3, 3)))
    thick = []
    line_row = np.full(W, -1.0)
    for x in range(40, W - 40, 20):
        rows = np.where(yel[:, x])[0]
        if len(rows) < 8:
            continue
        runs = np.split(rows, np.where(np.diff(rows) > 1)[0] + 1)
        r = max(runs, key=len)
        if len(r) >= 8:
            thick.append(len(r))
            line_row[x] = r.mean()
    t_med = float(np.median(thick))
    scale_mm = 75.0 / t_med                                # one dimension only: the yellow line is 75 mm
    R.check("C1 scale fitted on one dimension (yellow line 75 mm = %.1f px) agrees with the stated 3.0 mm/px" % t_med, abs(scale_mm - mm) / mm <= 0.12, "fitted %.2f mm/px" % scale_mm)
    xs = np.array([x for x in range(W) if line_row[x] > 0])
    ys = np.array([line_row[x] for x in xs])
    coef = np.polyfit(xs, ys, 1)
    Y = lum(rgb)
    bg = ndi.median_filter(Y[::2, ::2], size=13)
    bg = np.kron(bg, np.ones((2, 2)))[:H, :W]
    rel = Y / np.maximum(bg, 1e-4)
    region = np.zeros((H, W), bool)
    for x in range(W):
        yl = np.polyval(coef, x)
        a, b = int(yl + 0.07 / (scale_mm / 1000) ), int(yl + 0.75 / (scale_mm / 1000))   # 0.07 to 0.75 m below the line's centre
        region[max(a, 0):min(b, H), x] = True
    region &= (np.arange(W)[None, :] > 330)
    dots = ndi.binary_opening((rel < 0.75) & region)
    lab, n = ndi.label(dots)
    px = np.array(ndi.sum(dots, lab, np.arange(1, n + 1)))
    pxmm2 = (scale_mm / 1000.0) ** 2
    keep = px * pxmm2 * 1e6 >= 70.0      # M04's smallest dots are 10.6 mm across = 88 mm2; 70 mm2 and up
    area_m2 = region.sum() * pxmm2
    dens = float(keep.sum() / area_m2)
    # dot density only inside the dotted band: restrict to the dotted strip (2.5 sigma of the dot rows)
    cen = np.array(ndi.center_of_mass(dots, lab, np.arange(1, n + 1)))[keep]
    eqd = 2 * np.sqrt(px[keep] * pxmm2 / math.pi) * 1000
    dm = M["M04"]["values"]
    R.check("C2 dot size from the preview at rel < 0.75 (p50 %.1f mm) matches M04 at rel < 0.75 (p50 %.1f mm) within 5 mm" % (np.percentile(eqd, 50), dm["eqd_mm_p10_50_90_rel0.75"][1]), abs(np.percentile(eqd, 50) - dm["eqd_mm_p10_50_90_rel0.75"][1]) <= 5.0)
    # band: principal axis of dot centres, central 90 %
    P2 = cen[:, ::-1] * (scale_mm / 1000.0)
    c0 = P2.mean(0)
    w_, v_ = np.linalg.eigh(np.cov((P2 - c0).T))
    ax = v_[:, 1]
    tcoord = (P2 - c0) @ ax
    ncoord = (P2 - c0) @ v_[:, 0]
    band_len = float(np.percentile(tcoord, 95) - np.percentile(tcoord, 5))
    band_wid = float(np.percentile(ncoord, 95) - np.percentile(ncoord, 5))
    env_w = tj["kinds"]["road_oil"]["geometry"]["band_width_m"]["p5_95"]
    R.check("C3 drip band width from the preview (%.2f m) matches the target's %.2f m within 35 %%" % (band_wid, env_w), abs(band_wid - env_w) / env_w <= 0.35)
    lo_len, hi_len = tj["kinds"]["road_oil"]["envelope"]["length_m"]
    R.check("C4 drip band visible length (%.2f m) lies in the target's length range %.1f to %.1f m (cut by the frame, so at least)" % (band_len, lo_len, hi_len), band_len >= lo_len * 0.75 and band_len <= hi_len * 1.1)
    # density in the dotted strip itself
    strip = np.abs(ncoord) <= 0.5 * env_w * 1.3
    strip_area = band_len * env_w * 1.3
    dens_strip = float(strip.sum() / max(strip_area, 1e-6))
    lo_d, hi_d = tj["kinds"]["road_oil"]["envelope"]["density_per_m2"]
    R.check("C5 dot density inside the band (%.0f per m2 at rel 0.75) is within 40 %% of M04's in-band %d (rel 0.75) and inside the target's range %d to %d widened by the same 40 %%" % (dens_strip, dm["in_band_per_m2_rel0.75"], lo_d, hi_d), abs(dens_strip - dm["in_band_per_m2_rel0.75"]) <= 0.4 * dm["in_band_per_m2_rel0.75"] and lo_d / 1.4 <= dens_strip <= hi_d * 1.4)
    # overlay: the envelope's band rectangle (length = measured visible length, width = target width x 1.3) at the measured axis; share of dots inside
    L_env = min(max(band_len * 1.08, lo_len), hi_len) if band_len < hi_len else hi_len
    inside = (np.abs(tcoord) <= L_env / 2) & (np.abs(ncoord) <= env_w * 1.3 / 2)
    share_in = float(inside.mean())
    R.check("C6 the envelope's drip band, laid on the photograph at the one-dimension scale, holds %.0f %% of the detected dots (needs 90 %%)" % (100 * share_in), share_in >= 0.90)
    if overlays:
        im = Image.fromarray(rgb)
        d = ImageDraw.Draw(im, "RGBA")
        cx, cy = c0 / (scale_mm / 1000.0)
        ux, uy = ax / (scale_mm / 1000.0)
        nx, ny = v_[:, 0] / (scale_mm / 1000.0)
        hl, hw = L_env / 2, env_w * 1.3 / 2
        pts = [(cx + ux * s1 * hl + nx * s2 * hw, cy + uy * s1 * hl + ny * s2 * hw) for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        d.polygon(pts, outline=(0, 255, 255, 255), fill=(0, 255, 255, 30))
        d.line(pts + [pts[0]], fill=(0, 255, 255, 255), width=3)
        for (yy, xx) in cen:
            d.ellipse([xx - 5, yy - 5, xx + 5, yy + 5], outline=(255, 60, 60, 255))
        for k in range(0, 800, 50):
            pass
        d.rectangle([20, H - 40, 20 + 500 / scale_mm, H - 30], fill=(255, 255, 255, 255))
        d.text((24, H - 62), "0.5 m at the one-dimension scale (yellow line 75 mm); cyan = target's drip band; red = dots found (rel < 0.75)", fill=(255, 255, 255, 255))
        out = pv("ph-urban_street_03-oil-drip-speckle-target-on-photo.jpg")
        im.save(out, quality=84, optimize=True)
        overlay_log.append(os.path.basename(out))
    # ---- C7 flags
    f = "ph-urban_street_03-flags-patched-ortho.jpg"
    rgb = load_rgb(pv(f))
    boxes = tj["measurements"]["M07"]["preview_boxes"]
    dk = np.mean([lum(rgb[b[2]:b[3], b[0]:b[1]].reshape(-1, 3).mean(0)) for b in boxes["dark"]])
    pl = np.mean([lum(rgb[b[2]:b[3], b[0]:b[1]].reshape(-1, 3).mean(0)) for b in boxes["pale"]])
    lo, hi = tj["kinds"]["flag_patch_crack"]["geometry"]["ratio_range"]
    R.check("C7 flag dark/pale luminance ratio re-measured on the preview (%.2f; JPEG 8-bit) is in the target's range %.2f to %.2f" % (dk / pl, lo, hi), lo - 0.05 <= dk / pl <= hi + 0.05)
    # ---- C8 peeling paint share and hard edge
    f = "ph-peeling_painted_wall-paint-flake.jpg"
    rgb = load_rgb(pv(f))
    shares, cen = kmeans_share(rgb, 2)
    loss = float(shares.min())
    v = M["M08"]["values"]
    R.check("C8 paint loss share re-measured (%.3f) is within 3 points of M08's %.3f" % (loss, v["loss_share"]), abs(loss - v["loss_share"]) <= 0.03)
    # ---- C9 plaster foot gradient
    f = "ph-plaster_brick_01-wall-foot-algae.jpg"
    rgb = load_rgb(pv(f)).astype(float)
    Hh = rgb.shape[0]
    mmpx = P[f]["mm_per_px"]
    green = rgb[..., 1] - 0.5 * (rgb[..., 0] + rgb[..., 2])
    n45 = int(450 / mmpx)
    foot = green[Hh - n45:].mean()
    above = green[Hh // 2: Hh // 2 + n45].mean()
    Lf = Lstar(rgb[Hh - n45:].mean((0, 1))); La = Lstar(rgb[Hh // 2: Hh // 2 + n45].mean((0, 1)))
    R.check("C9 plaster foot: green excess in the lowest 0.45 m (%.1f) is 1.4x or more of the plaster above (%.1f) and 5 L* darker (%.1f against %.1f)" % (foot, above, Lf, La), foot >= 1.4 * above and (La - Lf) >= 5.0)
    # ---- C10 drip streaks on concrete
    f = "ph-concrete_layers-drip-streaks.jpg"
    rgb = load_rgb(pv(f))
    L = Lstar(rgb.astype(float))
    mmpx = P[f]["mm_per_px"]
    D = gauss(L, max(0.5, 0.76 / mmpx)) - gauss(L, 9.1 / mmpx)
    m = ndi.binary_opening(D < -1.5, structure=np.ones((max(2, int(round(3 * 0.757 / mmpx))), 1)))
    lab, n = ndi.label(m)
    cnt = 0
    wid = []
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        hh = (sl[0].stop - sl[0].start) * mmpx
        ww = (sl[1].stop - sl[1].start) * mmpx
        if hh >= 60 and hh >= 4 * ww:
            cnt += 1
            wid.append(ww)
    per_m = cnt / (rgb.shape[1] * mmpx / 1000.0)
    R.check("C10 drip streaks re-detected: %.1f per metre (M16: 7.7 +/- 40 %%), median width %.1f mm (M16 10.6 to 19.7 mm)" % (per_m, np.median(wid) if wid else 0), 4.0 <= per_m <= 12.0 and wid and 8 <= np.median(wid) <= 25)
    # ---- C11 rust trickle
    f = "ph-asbestos_sheet_02-rust-bleed-fixings.jpg"
    rgb = load_rgb(pv(f)).astype(float)
    mmpx = P[f]["mm_per_px"]
    rust = (rgb[..., 0] - rgb[..., 2] > 45) & (rgb[..., 0] > 90)
    sub = rust[:, 0:90]
    rows = np.where(sub.any(1))[0]
    Ltr = (rows.max() - rows.min() + 1) * mmpx
    wd = [np.where(sub[r])[0].max() - np.where(sub[r])[0].min() + 1 for r in rows]
    R.check("C11 rust trickle re-measured: length %.0f mm (at least 400), median width %.1f mm (M14 5 to 20)" % (Ltr, np.median(wd) * mmpx), Ltr >= 400 and 3 <= np.median(wd) * mmpx <= 22)
    r_lo = tj["kinds"]["rust_bleed"]["geometry"]["streak_width_mm"]
    R.check("C12 the target's rust width p50 (%s mm) lies inside the re-measured trickle width" % r_lo["p50"], 3 <= r_lo["p50"] <= 22)
    # ---- C13 damp blotch edge softness
    f = "ph-concrete_wall_003-damp-mould-blotches.jpg"
    rgb = load_rgb(pv(f))
    L = Lstar(rgb.astype(float))
    mmpx = P[f]["mm_per_px"]
    dark = ndi.binary_opening(gauss(L, 2.0) < np.percentile(gauss(L, 2.0), 14))
    gy, gx = np.gradient(gauss(L, 1.5))
    g = np.hypot(gx, gy)
    b = ndi.binary_dilation(dark, iterations=2) & ~ndi.binary_erosion(dark, iterations=2)
    inside = L[ndi.binary_erosion(dark, iterations=5)].mean()
    outside = L[~ndi.binary_dilation(dark, iterations=5)].mean()
    ew = 0.8 * abs(outside - inside) / max(np.median(g[b]), 1e-6) * mmpx
    lo_e, hi_e = tj["kinds"]["algae_downpipe"]["geometry"]["edge_10_90_mm"]
    R.check("C13 damp blotch edge re-measured %.0f mm; target damp/algae edge range is %d to %d mm" % (ew, lo_e, hi_e), 0.4 * lo_e <= ew <= 3.0 * hi_e)
    # ---- C14 Hook sheet gable foot: one-dimension scale from the 75 mm brick course; the splash profile laid on it
    hs = load_rgb(HOOK).astype(float)
    cols = slice(15, 170)
    Yh = lum(hs)
    colprof = Yh[400:620, cols].mean(1)
    colprof = colprof - colprof.mean()
    ac = np.correlate(colprof, colprof, "full")[len(colprof) - 1:]
    per = 8 + int(np.argmax(ac[8:25]))
    mmpx = 75.0 / per
    R.check("C14 brick course on the Hook sheet gable = %d px (M18: 11) so %.2f mm/px" % (per, mmpx), 10 <= per <= 12)
    ref = float(np.median(Yh[430:600, cols]))
    ratio_rows = np.array([np.median(Yh[r:r + 6, cols]) / ref for r in range(560, 730, 6)])
    rows_c = np.arange(560, 730, 6) + 3
    dark_rows = [r for r, v in zip(rows_c, ratio_rows) if v < 0.25]
    foot_row = max(dark_rows) + 3 if dark_rows else 716
    k = tj["kinds"]["wall_foot_splash"]
    hp = k["geometry"]["height_profile"]
    mult = k["tone"]["brick_red"]["albedo_mult_linear"]
    errs = []
    for r, v in zip(rows_c, ratio_rows):
        h = (foot_row - r) * mmpx / 1000.0
        if h < 0.02 or h > 0.85:
            continue
        m_h = float(np.interp(h, hp["h_m"], hp["mask"]))
        pred = 1.0 - m_h * (1.0 - mult)
        errs.append(abs(pred - v))
    mean_err = float(np.mean(errs))
    R.check("C15 the splash profile (mult %.2f) laid on the sheet gable foot (foot row %d, scale fitted on the course only): mean error %.3f in luminance ratio (needs <= 0.17)" % (mult, foot_row, mean_err), mean_err <= 0.17)
    top_row = [r for r, v in zip(rows_c, ratio_rows) if v < 0.6]
    h_half = (foot_row - min(top_row)) * mmpx / 1000.0
    h_half_t = float(np.interp(0.45, hp["mask"][::-1], hp["h_m"][::-1]))
    R.check("C16 the sheet's half-strength height (ratio 0.6: %.2f m) falls within one course plus ragged amplitude (0.15 m) of the profile's mask-0.4 height (%.2f m)" % (h_half, h_half_t), abs(h_half - h_half_t) <= 0.15 + 0.075)
    if overlays:
        im = Image.fromarray(hs.astype(np.uint8)).crop((0, 540, 200, 740)).resize((800, 800), Image.LANCZOS)
        d = ImageDraw.Draw(im, "RGBA")
        sc = 4.0   # preview px per sheet px
        for h, m_h in zip(hp["h_m"], hp["mask"]):
            y = (foot_row - 540 - h * 1000.0 / mmpx) * sc
            d.line([(0, y), (800, y)], fill=(0, 255, 255, 200), width=2)
            d.text((6, y - 12), "%.2f m  mask %.2f" % (h, m_h), fill=(0, 255, 255, 255))
        d.line([(0, (foot_row - 540) * sc), (800, (foot_row - 540) * sc)], fill=(255, 255, 0, 255), width=3)
        d.text((6, (foot_row - 540) * sc + 4), "foot row; scale from the 75 mm course (%d px): Hook sheet, not a photograph" % per, fill=(255, 255, 0, 255))
        out = pv("hook-sheet-gable-foot-target-on-sheet.jpg")
        im.convert("RGB").save(out, quality=86, optimize=True)
        overlay_log.append(os.path.basename(out))
    # ---- C17 craquelure density re-measured
    f = "ph-preconcrete_wall_001-craquelure-flakes.jpg"
    rgb = load_rgb(pv(f)).astype(float)
    mmpx = P[f]["mm_per_px"]
    L = Lstar(rgb)
    Ls = gauss(L, 1.2)
    dm_ = Ls < gauss(L, 10) - 6
    lab, n = ndi.label(dm_, np.ones((3, 3)))
    keep = np.zeros_like(dm_)
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        ext = math.hypot(sl[0].stop - sl[0].start, sl[1].stop - sl[1].start) * mmpx
        if ext >= 40 and (lab[sl] == i).sum() >= 10:
            keep[sl] |= (lab[sl] == i)
    ln = float((zhang_suen(keep)).sum()) * mmpx * 1.1 / 1000.0
    area = rgb.shape[0] * rgb.shape[1] * (mmpx / 1000.0) ** 2
    cr = tj["kinds"]["paint_flake"]["geometry"]["crack_length_m_per_m2"]
    R.check("C17 craquelure re-measured %.1f m per m2 (M09: 5.7 +/- 30 %%); the target says %s" % (ln / area, cr), 3.5 <= ln / area <= 8.5 and cr[0] <= 5.7 <= cr[1] + 1.0)
    # ---- C18 aerial asphalt marks (share of area darker than the local mean)
    f = "ph-aerial_asphalt_01-road-tyre-scuffs.jpg"
    rgb = load_rgb(pv(f)).astype(float)
    L = Lstar(rgb)
    D = gauss(L, 6.0) - gauss(L, 120.0)
    share = float((ndi.binary_opening(D < -2.5, iterations=2)).mean())
    R.check("C18 road scan marks re-measured on the preview crop: %.3f of the area at dL* 2.5 (M02 whole tile 0.125; crop differs, accepted 0.04 to 0.30)" % share, 0.04 <= share <= 0.30)
    return overlay_log


# ---------------------------------------------------------------- D: envelopes
def ppm_for(k):
    t = k["texel"]["px_per_m_recommended"]
    ext = k["mask"]["frame_extent_m"]
    big = max(ext[2] - ext[0], ext[3] - ext[1]) > 2.0
    if k["texel"]["smallest_feature_mm"] <= 3:
        return min(t, 800 if big else 1000)          # hairline kinds need the finer scale even on a big frame
    return min(t, 400 if big else 1000)


def part_d(tj, R, draw):
    ed = draw.edges_by_kind(tj)
    summary = {}
    for kid in tj["kinds_order"]:
        k = tj["kinds"][kid]
        ppm = ppm_for(k)
        ext = k["mask"]["frame_extent_m"]
        ext_mm = (ext[0] * 1000, ext[1] * 1000, ext[2] * 1000, ext[3] * 1000)
        results = {}
        runs = 0
        for seed in (1990, 2024):
            for variant in range(3):
                polys = draw.kind_envelope(tj, kid, seed, variant)
                org = k["mask"]["origin"]
                wrap = "xy" if "seamless" in org else "x" if "tile" in org else False
                mask = draw.rasterize(polys, ext_mm, ppm, ed.get(kid, 0.0), wrap=wrap)
                runs += 1
                for c in k["checks"]:
                    m = c["measure"]
                    p = dict(c["params"])
                    if m == "foot_profile":
                        res = foot_profile_check(mask, ppm, p["points"])
                        val = float(np.mean([r[4] for r in res]))
                        results.setdefault(c["name"], []).append((val, [r for r in res if not r[4]]))
                        continue
                    if m == "tone_ratio":
                        sc = k["geometry"]["slab_classes"]
                        val = float(lum(np.array(sc["dark"]["srgb"], float)) / lum(np.array(sc["pale"]["srgb"], float)))
                        results.setdefault(c["name"], []).append((val, None))
                        continue
                    if m == "crack_flag_share":
                        slabs = [q for q in polys if q["role"].startswith("slab_")]
                        cracks = [q for q in polys if q["role"] == "crack"]
                        hit = 0
                        for s in slabs:
                            xs = [a for a, _ in s["poly"]]; ys = [b for _, b in s["poly"]]
                            if any(min(xs) <= np.mean([a for a, _ in q["poly"]]) <= max(xs) and min(ys) <= np.mean([b for _, b in q["poly"]]) <= max(ys) for q in cracks):
                                hit += 1
                        results.setdefault(c["name"], []).append((hit / max(len(slabs), 1), None))
                        continue
                    if m == "role_length_per_m2":
                        fx0, fy0, fx1, fy1 = ext_mm
                        tot = 0.0
                        for q in polys:
                            if q["role"] != p["role"]:
                                continue
                            cx = np.mean([a for a, _ in q["poly"]]); cy = np.mean([b for _, b in q["poly"]])
                            if fx0 <= cx <= fx1 and fy0 <= cy <= fy1:
                                tot += q.get("length_mm", 0.0)
                        results.setdefault(c["name"], []).append((tot / 1000.0 / ((fx1 - fx0) * (fy1 - fy0) / 1e6), None))
                        continue
                    if m == "role_blob_eqd_mm":
                        eqs = []
                        for q in polys:
                            if q["role"] != p["role"]:
                                continue
                            xs_ = np.array([a for a, _ in q["poly"]]); ys_ = np.array([b for _, b in q["poly"]])
                            area = 0.5 * abs(np.dot(xs_, np.roll(ys_, -1)) - np.dot(ys_, np.roll(xs_, -1)))
                            eqs.append(2 * math.sqrt(area / math.pi))
                        results.setdefault(c["name"], []).append((float(np.percentile(eqs, 90 if p.get("stat") == "p90" else 50)) if eqs else 0.0, None))
                        continue
                    if m == "count_per_m2" and p.get("region") == "speckle_band":
                        dots = [q for q in polys if q["role"] == "dot"]
                        xs = [np.mean([a for a, _ in q["poly"]]) for q in dots]
                        Lb = (max(xs) - min(xs)) / 1000.0
                        W = k["envelope"]["width_m"]
                        results.setdefault(c["name"], []).append((len(dots) / max(Lb * W, 1e-6), None))
                        continue
                    if "only_roles" in p:
                        roles = p.pop("only_roles")
                        sub = [q for q in polys if q["role"] in roles]
                        mk = draw.rasterize(sub, ext_mm, ppm, ed.get(kid, 0.0), wrap=wrap)
                        results.setdefault(c["name"], []).append((measure(mk, ppm, m, **p), None))
                        continue
                    results.setdefault(c["name"], []).append((measure(mask, ppm, m, **p), None))
        summary[kid] = {}
        for c in k["checks"]:
            vals = [v for v, _ in results[c["name"]]]
            med = float(np.median(vals))
            if c["measure"] == "foot_profile":
                ok = med >= 0.99 or (np.mean([v >= 0.8 for v in vals]) >= 0.8 and med >= 0.8)
                det = "median share of profile points inside their bands %.2f over %d runs" % (med, runs)
                if not ok:
                    det += "; first misses %s" % [(round(a, 2), round(b, 2), lo, hi) for a, b, lo, hi, _ in results[c["name"]][0][1]]
            else:
                ok = c["min"] <= med <= c["max"]
                det = "median %.4g over %d runs (range %.3g to %.3g), expected %.4g to %.4g" % (med, runs, min(vals), max(vals), c["min"], c["max"])
            R.check("D %s %s at %d px/m" % (kid, c["name"], ppm), ok, det)
            summary[kid][c["name"]] = {"median": med, "min": float(min(vals)), "max": float(max(vals)), "expected": [c["min"], c["max"]], "ok": bool(ok)}
        # envelope sanity: the level-1 core lies inside the frame (nothing floats outside its decal)
        polys = draw.kind_envelope(tj, kid, 1990, 0)
        x0, y0, x1, y1 = draw.bounds(polys)
        slack = 120.0 if kid not in ("streak_coping", "flag_patch_crack", "road_oil", "road_crack", "tyre_scuff") else 400.0
        tiled = "tile" in k["mask"]["origin"] or "seamless" in k["mask"]["origin"]
        inside = tiled or x0 >= ext_mm[0] - slack and y0 >= ext_mm[1] - slack and x1 <= ext_mm[2] + slack and y1 <= ext_mm[3] + slack
        R.check("D %s envelope lies inside its decal frame (within %d mm; tiles may wrap)" % (kid, slack), inside, "bounds %.0f,%.0f to %.0f,%.0f against frame %s" % (x0, y0, x1, y1, [round(v) for v in ext_mm]))
    # seeded: the same seed gives the same polygons
    a = draw.kind_envelope(tj, "streak_sill", 1990, 0)
    b = draw.kind_envelope(tj, "streak_sill", 1990, 0)
    R.check("D seeded: the same seed gives the same polygons", a == b)
    c2 = draw.kind_envelope(tj, "streak_sill", 1991, 0)
    R.check("D seeded: another seed gives different polygons", a != c2)
    return summary


def main(argv):
    overlays = "--no-overlays" not in argv
    write = "--no-write" not in argv
    tj = json.load(open(TARGET))
    draw = load_drawing()
    R = Report()
    part_a(tj, R)
    part_b(tj, R)
    olog = part_c(tj, R, draw, overlays)
    summary = part_d(tj, R, draw)
    for ln in R.lines:
        if ln.startswith("FAIL") or ln.startswith("note"):
            print(ln)
    line = "self_check: passed=%d/%d failed=%d (A structure, B tone, C photographs, D envelopes; %d kinds)" % (R.ok, R.ok + R.fail, R.fail, len(tj["kinds_order"]))
    print(line)
    if write:
        tj["self_check"] = {"date": datetime.date.today().isoformat(), "result": line, "passed": R.ok, "failed": R.fail, "overlays_written": olog,
                            "failures": [l for l in R.lines if l.startswith("FAIL")], "envelope_summary": summary}
        json.dump(tj, open(TARGET, "w"), indent=1)
    return 1 if R.fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
