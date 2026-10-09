#!/usr/bin/env python
"""Tests target.json against its own photograph measurements and for internal consistency, before anything is built.

    /home/user/.bpyenv/bin/python self_check.py [--no-overlays] [--no-write] [--verbose]

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
  E  composition and wrong masks: the order, floor and per-channel colour rule of target.json "compose" are applied to the drawn masks (foot, head, soot, channel, ground), and masks made
     deliberately wrong (uniform gradients, symmetric streak pairs, evenly spaced fingers, gridded dots, a plain stripe, white noise) must each be refused by the kind's own mask checks.
  F  placement: the placement checks of target.json are run on a conforming placed street and on deliberately wrong ones (an offset sill streak, a rotated streak, oil in the wrong place, gum on the road,
     one variant over 40 %, neighbouring tiles in phase).
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
    if measure_id == "mask_mean":
        return float(mask.mean())
    if measure_id == "top_edge_std_mm":
        m = _from_source(mask, p.get("source", "bottom"))
        ab = m >= p.get("thr", 0.5)
        has = ab.any(0)
        if has.mean() < 0.6:
            return 0.0
        far = m.shape[0] - 1 - np.argmax(ab[::-1], axis=0)
        return float(far[has].astype(float).std() * px_mm)
    if measure_id in ("column_mean_cv", "core_column_cv"):
        m = _from_source(mask, p.get("source", "bottom"))
        r0, r1 = int(round(p["from_m"] * ppm)), int(round(p["to_m"] * ppm))
        cm = m[r0:r1].mean(0)
        return float(cm.std() / cm.mean()) if cm.mean() > 1e-4 else 0.0
    if measure_id == "edge_on_course_share":
        m = _from_source(mask, p.get("source", "bottom"))
        ab = m >= p.get("thr", 0.5)
        has = ab.any(0)
        if has.mean() < 0.6:
            return 0.0
        far = m.shape[0] - 1 - np.argmax(ab[::-1], axis=0)
        c = p.get("course_m", 0.075) * 1000.0
        h = (far[has].astype(float) + 1.0) * px_mm
        return float((np.abs(((h + c / 2) % c) - c / 2) <= p.get("tol_mm", 10.0)).mean())
    if measure_id == "lower_wall_excess":
        m = _from_source(mask, "bottom")
        lo = m[int(round(p.get("low_from_m", 0.1) * ppm)):int(round(p.get("low_to_m", 0.6) * ppm))].mean()
        hi = m[int(round(p.get("high_from_m", 1.5) * ppm)):int(round(p.get("high_to_m", 3.5) * ppm))].mean()
        return float(lo - hi)
    if measure_id == "coverage_share_below_m":
        ab = mask >= p.get("thr", 0.5)
        if not ab.any():
            return 0.0
        n_below = int(round(p.get("below_m", 0.3) * ppm))
        return float(ab[mask.shape[0] - n_below:].sum() / ab.sum())
    if measure_id in ("brick_patch_share", "brick_cell_std", "brick_neighbour_same_share"):
        m = _from_source(mask, "bottom")
        bw, bh = p["brick_w_m"], p["brick_h_m"]
        Wm = m.shape[1] / ppm
        means, stds = [], []
        pairs_same = []
        j = 0
        while (j + 1) * bh <= p["to_m"] + 1e-9:
            if j * bh >= p["from_m"] - 1e-9:
                off = (j % 2) * bw / 2
                x0 = -off
                course_on = []
                while x0 + bw <= Wm + 1e-9:
                    if x0 >= -1e-9:
                        cell = m[int(round(j * bh * ppm)):int(round((j + 1) * bh * ppm)), int(round(x0 * ppm)):int(round((x0 + bw) * ppm))]
                        means.append(float(cell.mean()))
                        stds.append(float(cell.std()))
                        course_on.append(float(cell.mean()) > p.get("cell_mean_above", 0.4))
                    x0 += bw
                pairs_same += [a == b for a, b in zip(course_on[:-1], course_on[1:])]
            j += 1
        if not means:
            return 0.0
        if measure_id == "brick_neighbour_same_share":
            return float(np.mean(pairs_same)) if pairs_same else 0.0
        means, stds = np.array(means), np.array(stds)
        on = means > p.get("cell_mean_above", 0.4)
        if measure_id == "brick_patch_share":
            return float(on.mean())
        return float(stds[on].mean()) if on.any() else 0.0
    if measure_id in ("rivulet_spacing_cv", "rivulet_length_cv"):
        comps = _head_components(mask, ppm, p.get("thr", 0.25), p.get("head_m", 0.2))
        riv = [c for c in comps[1:-1] if c[1] >= p.get("min_length_m", 0.1)] if len(comps) >= 2 else []
        if len(riv) < 3:
            return 0.0
        if measure_id == "rivulet_length_cv":
            L = np.array([c[1] for c in riv])
            return float(L.std() / L.mean())
        gaps = np.diff([c[0] for c in riv])
        return float(gaps.std() / gaps.mean())
    if measure_id in ("end_streak_length_ratio", "end_streak_width_ratio", "rivulet_count", "finger_length_cv"):
        comps = _head_components(mask, ppm, p.get("thr", 0.25), p.get("head_m", 0.2))
        if measure_id == "finger_length_cv":
            L = np.array([c[1] for c in comps])
            return float(L.std() / L.mean()) if len(L) >= 3 else 0.0
        if len(comps) < 2:
            return 0.0
        if measure_id == "rivulet_count":
            return float(sum(1 for c in comps[1:-1] if c[1] >= p.get("min_length_m", 0.1)))
        a, b = comps[0], comps[-1]
        col = 1 if measure_id == "end_streak_length_ratio" else 2
        return float(max(a[col], b[col]) / max(min(a[col], b[col]), 1e-9))
    if measure_id == "finger_spacing_cv":
        r = int(round(p.get("head_row_m", 0.12) * ppm))
        row = mask[min(r, mask.shape[0] - 1)] >= p.get("thr", 0.25)
        lab, n = ndi.label(row)
        if n < 3:
            return 0.0
        cx = np.array(ndi.center_of_mass(row, lab, np.arange(1, n + 1))).ravel()
        gaps = np.diff(cx)
        return float(gaps.std() / gaps.mean())
    if measure_id in ("nn_ratio", "size_cv"):
        lab, n = _comps(mask, p.get("thr", 0.5))
        if n == 0:
            return 0.0
        idx = np.arange(1, n + 1)
        areas = ndi.sum(np.ones_like(mask), lab, idx) * px_mm ** 2
        keep = areas >= p.get("min_area_mm2", 0.0)
        if keep.sum() < 4:
            return 0.0
        if measure_id == "size_cv":
            eq = 2 * np.sqrt(areas[keep] / math.pi)
            return float(eq.std() / eq.mean())
        from scipy.spatial import cKDTree, ConvexHull
        cen = np.array(ndi.center_of_mass(mask >= p.get("thr", 0.5), lab, idx))[keep] / ppm      # metres (row, col)
        dd = cKDTree(cen).query(cen, k=2)[0][:, 1]
        A = mask.shape[0] * mask.shape[1] / ppm ** 2 if p.get("area", "frame") == "frame" else ConvexHull(cen).volume
        return float(dd.mean() / (0.5 / math.sqrt(len(cen) / max(A, 1e-9))))
    if measure_id == "dominant_wavelength_m":
        m = mask - mask.mean()
        F = np.abs(np.fft.fft2(m)) ** 2
        ky = np.fft.fftfreq(m.shape[0], d=1.0 / ppm)
        kx = np.fft.fftfreq(m.shape[1], d=1.0 / ppm)
        k = np.hypot(*np.meshgrid(kx, ky))
        fund = 1.0 / min(m.shape[0], m.shape[1]) * ppm
        kb = np.rint(k / fund).astype(int)
        P = np.bincount(kb.ravel(), weights=F.ravel())
        peak = 1 + int(np.argmax(P[1:]))
        return float(1.0 / (peak * fund))
    raise ValueError(measure_id)


def _from_source(mask, source):
    """orient a mask so that row 0 is the source edge (the pavement line for a foot band, the feature's lower edge for a head band)"""
    return mask if source == "top" else mask[::-1]


def _head_components(mask, ppm, thr, head_m):
    """components of mask >= thr whose top lies within head_m of the frame's top edge, left to right: (x centre px, rod length m, rod width m)"""
    lab, n = _comps(mask, thr)
    out = []
    mm = 1.0 / ppm
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        if sl[0].start > head_m * ppm:
            continue
        ys, xs = np.nonzero(lab[sl] == i)
        if len(ys) < 6:
            continue
        w, v = np.linalg.eigh(np.cov(np.vstack([xs, ys])))
        out.append((float(xs.mean() + sl[1].start), math.sqrt(12 * max(w[1], 1e-9)) * mm, math.sqrt(12 * max(w[0], 1e-9)) * mm))
    out.sort()
    return out


def foot_profile_check(mask, px_per_m, points, axis="rows_from_bottom"):
    """points: [[height_m, min, max], ...] with row H-1 the foot (axis rows_from_bottom) or row 0 the source edge (rows_from_top, a head band). Returns list of (h, value, lo, hi, ok)."""
    H = mask.shape[0]
    out = []
    for h, lo, hi in points:
        r = int(round(H - 1 - h * px_per_m)) if axis != "rows_from_top" else int(round(h * px_per_m))
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
# One sentence per measure, the exact definition the code below implements. target.json's "check_measures" is this dictionary (build step), and part A tests that the two are equal,
# so a builder implementing from target.json alone gets the same numbers as `measure()`.
MEASURE_DOCS = {
    "coverage": "share of decal pixels with mask >= thr (default 0.5)",
    "blob_eqd_mm": "equivalent diameter (mm) = 2 sqrt(area / pi) of the 8-connected components of mask >= thr (default 0.5) with area >= min_area_mm2; stat p50 (default) or p90 over the components",
    "count_per_m2": "number of 8-connected components of mask >= thr with area >= min_area_mm2, per m2 of the decal frame",
    "edge_10_90_mm": ("10 to 90 % edge width, relative to the mask's own peak: 0.95 x peak / the 90th percentile of |gradient| (per metre; one axis if axis is x or y), taken over pixels with band_lo x peak < mask < band_hi x peak "
                      "(defaults 0.1 and 0.9) that lie within reach_mm (default 60) of the contour at half the peak; 0 if the peak is below 0.2"),
    "streak_aspect": "median over the 8-connected components of mask >= thr (default 0.3) with rod length >= min_length_m of rod length / rod width; rod length = sqrt(12 x variance) along the major axis, width likewise along the minor axis",
    "streak_width_mm": "stat (p50 default, p10 or p90) over those components of the rod width in mm",
    "streak_length_m": "stat (p50 default, p10 or p90) over those components of the rod length in m",
    "verticality_deg": "largest deviation of a component's major axis from vertical (degrees) over the components of mask >= thr (default 0.3) with rod length >= min_length_m (default 0.1 m)",
    "fade_ratio": "per component of mask >= thr (default 0.3) taller than 150 mm: mean mask over its last third of rows / its first third; median over components",
    "foot_profile": ("mean mask per row of the whole decal width, at each point [height_m, min, max], mean of three rows: axis rows_from_bottom counts height up from the frame's bottom row (the pavement line), "
                     "rows_from_top counts down from its top row (the feature's lower edge); the check passes when at least 80 % of the points are inside their bounds"),
    "tile_seam": "mean |mask(first column) - mask(last column)| (rows for axis y; the larger of the two for xy) divided by the mean absolute difference of adjacent columns (rows) inside the tile: about 1 when seamless",
    "mask_max": "maximum mask value", "mask_std": "standard deviation of the mask", "mask_mean": "mean of the mask",
    "top_edge_std_mm": ("standard deviation along x, in mm, of the far edge of the band: for each column the row farthest from the source edge (source bottom: the pavement line, the frame's bottom row; source top: the feature's "
                        "lower edge, the top row) where mask >= thr; columns without such a row are left out; 0 if fewer than 60 % of the columns have one"),
    "column_mean_cv": "coefficient of variation (std / mean) across x of the column means of the mask over the rows from_m to to_m (m) measured from the source edge (source bottom or top)",
    "brick_patch_share": ("share of brick cells whose mean mask is above cell_mean_above (default 0.4): cells brick_w_m x brick_h_m in stretcher bond (courses brick_h_m high from the pavement line, each course offset by half a brick), "
                          "only courses lying wholly between from_m and to_m, only whole cells inside the frame"),
    "brick_cell_std": "mean over the cells counted as whitened in brick_patch_share (same cells, same parameters) of the standard deviation of the mask inside the cell",
    "end_streak_length_ratio": ("longer over shorter rod length of the leftmost and rightmost components of mask >= thr (default 0.25) whose top lies within head_m (default 0.2) of the frame's top edge (the sill's lower edge); 0 if there are fewer than two"),
    "end_streak_width_ratio": "wider over narrower rod width of the same two end components",
    "rivulet_count": "number of the components between those two end components, in x order, with rod length >= min_length_m (default 0.1)",
    "finger_spacing_cv": "std / mean of the gaps between the centres of the runs of mask >= thr (default 0.25) along the row head_row_m (default 0.12 m) below the frame's top edge; 0 if fewer than three runs",
    "finger_length_cv": "std / mean of the rod lengths of the components of mask >= thr whose top lies within head_m of the top edge; 0 if fewer than three",
    "nn_ratio": ("Clark-Evans ratio of the components of mask >= thr (area >= min_area_mm2; at least 4): mean nearest-neighbour distance of their centroids / (0.5 / sqrt(n / A)), A the frame area (area frame) or the "
                 "convex hull of the centroids (area hull); about 1 for random scatter, above 1.3 for a lattice, below 0.8 for clusters; 0 if fewer than four"),
    "size_cv": "std / mean of the equivalent diameters of the components of mask >= thr with area >= min_area_mm2 (at least 4)",
    "dominant_wavelength_m": ("wavelength 1 / (k x f) in m of the annulus with the largest summed power in the 2-D power spectrum of the mask minus its mean, annuli of width f = 1 / the shorter side of the frame (m), "
                              "k = 1, 2, 3, ... the annulus index (the zero-frequency annulus is left out)"),
    "core_column_cv": "coefficient of variation (std / mean) across x of the column means of the mask over the FULL-STRENGTH zone, the rows from_m to to_m (m) measured from the source edge (source bottom or top); a band in vertical stripes is refused",
    "edge_on_course_share": ("share of columns whose far edge of the band (as in top_edge_std_mm, at mask >= thr, measured from the source edge: the row farthest from it, taken as the outer boundary of that row) lies within tol_mm (default 10) of a multiple "
                             "of course_m (default 0.075 m, a brick course) from the source edge; 0 if fewer than 60 % of the columns have an edge"),
    "brick_neighbour_same_share": ("share of pairs of side-by-side brick cells in a course (cells as in brick_patch_share, same parameters) that are both on (cell mean above cell_mean_above) or both off; a checkerboard gives 0, a random fill of 0.55 about 0.5, "
                                   "a solid stripe 1"),
    "rivulet_spacing_cv": "std / mean of the gaps between the x centres of the rivulet components (the components between the two end components, rod length >= min_length_m, as for rivulet_count); 0 if there are fewer than three",
    "rivulet_length_cv": "std / mean of the rod lengths of the same rivulet components; 0 if there are fewer than three",
    "lower_wall_excess": "mean of the mask over the rows low_from_m to low_to_m (default 0.1 to 0.6 m) minus its mean over the rows high_from_m to high_to_m (default 1.5 to 3.5 m), heights from the bottom row (the pavement line)",
    "coverage_share_below_m": "share of the pixels with mask >= thr (default 0.5) that lie in the lowest below_m (default 0.3 m) of the frame (its bottom rows); 0 if there are none",
    "tone_ratio": "mean luminance of the dark-slab class over the pale-slab class in the generated flag colour map (check applies to the flag colour result, not the mask)",
    "crack_flag_share": "share of flags carrying a crack in the generated flag attributes",
    "crack_width_mm": "median of 2 x distance-transform - 1 along the Zhang-Suen skeleton of mask >= thr (mm)",
    "crack_length_per_m2": "skeleton length (m) of mask >= thr per m2 of the decal frame",
    "role_length_per_m2": "envelope polygons only (drawing check): path length of the polygons with the named role per m2 of the frame",
    "role_blob_eqd_mm": "envelope polygons only (drawing check): equivalent diameter of the polygons with the named role (stat p50 or p90)",
    "role_count": "envelope polygons only (drawing check): number of polygons with the named role",
    "role_share_below": "envelope polygons only (drawing check): share (by polygon area, of=area, or by count) of the polygons with the named role whose centroid lies below below_mm of the frame's bottom edge",
    "house_to_house_ratio": ("composition: for every house of target.json `houses` that the Hook sheet's frame shows, the mean linear luminance of its composed upper wall (rows from 1.3 m up, wall_soot at the house's state weight, albedo, no haze) over Mickey's front's "
                             "(east_parade_bay0); the value returned is the one furthest from 1 (so the darkest and the brightest are both tested)"),
    "composed_soot_chroma_ratio": "composition: CIE chroma (L*a*b*, D65) of the mean colour of the composed sooted wall (state sooted, rows from 1.3 m up, brick_red) over the clean brick's",
    "composed_eaves_front_ratio": ("composition: luminance over the wall's, mean over x, of a wall under its eaves gutter composed with wall_head_band at the stated strength (default 0.2) and depth_m (default 0.3: the profile compressed in depth so that its "
                                   "half-strength height, 0.675 m, falls at depth_m, factor depth_m / 0.675), at below_m (default 0.3 m) below the eaves"),
    "composed_foot_ratio": ("composition (compose block, self_check.compose_walls; every composition measure takes either the target's own drawn envelopes or, for unit 4.5, a `masks` dict of the builder's own masks): the luminance of a composed 2 m brick foot beside a downpipe (wall_soot, wall_foot_damp, wall_foot_splash, algae_downpipe in the stated order, "
                            "then the floor, at house wear 1.0, dry, in the state given) over the clean wall's, mean over x 0.6 to 1.4 m at height_m (default 0.1)"),
    "composed_salt_ratio": "composition: luminance over the clean wall's of the composed foot at the whitened bricks (salt mask > 0.4) between 0.30 and 0.52 m, after the replacing marks",
    "composed_wall_min_ratio": "composition: the lowest luminance over the clean wall's anywhere on the composed foot before the replacing marks (the floor is working when it is not below the wall floor)",
    "composed_soot_ratio": "composition: mean luminance of the sooted house's composed wall (soot state weight 1.0) over the cleaned house's (weight 0.0), rows from 1.3 m up",
    "composed_head_ratio": "composition: luminance over the wall's of the composed head band at depth 0.1 m below the feature, wall_soot in the given state first, mean over x",
    "channel_over_road": "composition: luminance of the channel_concrete albedo after the channel body's gutter_grime (mean over the channel rows 0.06 to 0.23 m) over the asphalt_dry albedo's",
    "fringe_over_road": "composition: luminance of the asphalt_dry albedo after the gutter_grime fringe (mean over rows 0.30 to 0.45 m) over the unmarked asphalt_dry albedo's",
    "composed_ground_min_ratio": "composition: the lowest luminance over the clean surface's of a kerb_granite texel under pavement_stain and gutter_grime together (at mask 1), after the ground floor",
}
MEASURES = set(MEASURE_DOCS)


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
    for kid in ("wall_foot_splash", "wall_foot_damp", "salt_bloom", "gutter_grime", "wall_head_band"):
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
    # ---- second pass (review of 8 October)
    cm = tj["compose"]
    stages = cm["walls"]["stage_1_L0_multiplicative"] + cm["walls"]["stage_2_L1_multiplicative"] + cm["walls"]["stage_3_replacing"] + cm["ground"]["stages"]
    R.check("A20 compose: every kind named in the order exists, none twice in the wall order, floors are numbers (walls 0.15, ground 0.28)",
            all(x in tj["kinds"] for x in stages) and len(cm["walls"]["stage_1_L0_multiplicative"] + cm["walls"]["stage_2_L1_multiplicative"] + cm["walls"]["stage_3_replacing"]) == len(set(cm["walls"]["stage_1_L0_multiplicative"] + cm["walls"]["stage_2_L1_multiplicative"] + cm["walls"]["stage_3_replacing"]))
            and cm["walls"]["floor"] == 0.15 and cm["ground"]["floor"] == 0.28, "stages %s" % stages)
    covered = set(stages) | set(cm.get("not_composed", []))
    R.check("A20b every kind is either in a compose stage or named as not composed (with a reason)", set(tj["kinds"]) <= covered, "missing %s" % sorted(set(tj["kinds"]) - covered))
    need = ["quay_end", "rank", "fishmonger_apron", "chandler_apron", "yard_entrance", "gully", "standing_places", "bus_stop", "empty_unit", "west_blind_gable"]
    R.check("A21 places: every anchor a rule uses has an x range or a count (%s)" % ", ".join(need), all(n in tj["places"] for n in need), "missing %s" % [n for n in need if n not in tj["places"]])
    pc_ids = [c["id"] for c in tj["placement_checks"]]
    R.check("A22 placement checks: the nine of the first review and P10, P11 of the second are present and each has a rule in this file", all(i in PLACEMENT_RULES for i in pc_ids) and len(pc_ids) >= 11, "ids %s" % pc_ids)
    R.check("A23 check_measures in target.json is word for word the MEASURE_DOCS of this file (what the code does)", tj["check_measures"] == MEASURE_DOCS,
            "differs in %s" % sorted(k for k in set(tj["check_measures"]) | set(MEASURE_DOCS) if tj["check_measures"].get(k) != MEASURE_DOCS.get(k)))
    undocumented = [(k, c["name"]) for k, kk in tj["kinds"].items() for c in kk["checks"] if c["measure"] not in MEASURE_DOCS]
    R.check("A24 every check's measure is documented", not undocumented, "%s" % undocumented)
    txt = json.dumps({k: v for k, v in tj.items() if k != "self_check"}).lower()
    import re
    pat = re.compile(r"\b(child|children|child's|children's|kid|kids|pushchairs?|prams?|buggy|buggies|toddlers?|hopscotch|playgrounds?|schoolboys?|schoolgirls?|nursery|sweet-wrappers?|sweetshops?|babies|baby)\b")
    bad = sorted(set(pat.findall(txt)))
    md = os.path.join(HERE, "TARGET.md")
    if os.path.exists(md):
        bad += [w + " (TARGET.md)" for w in sorted(set(pat.findall(open(md, encoding="utf-8").read().lower())))]
    R.check("A25 wording: no word that implies a minor anywhere (canon content rule), in target.json and TARGET.md", not bad, "found %s" % bad)
    M = tj["measurements"]
    R.check("A26 sources: M03 and M05 carry the tones cited to them, M15 states the Poly Haven tags, M21 to M29 exist, the seven files are listed as looked at and not used, flag_concrete cites M27",
            "core_L_star" in M["M03"]["values"] and "seam_ratio" in M["M05"]["values"] and "tags" in M["M15"]["values"] and all(("M%d" % i) in M for i in range(21, 30))
            and len(tj["looked_at_not_used"]) == 7 and "M27" in tj["surfaces"]["flag_concrete"]["src"] and "no soot on the brick" not in json.dumps(tj["sources"]))
    rows = tj["wet_dry_rule"]["rows"]
    R.check("A27 wet and dry once: for each sheet-derived row, dry multiplier x wet multiplier equals the sheet's own ratio (within 0.03)",
            all(abs(tj["kinds"][r["kind"]]["tone"][r["surface"]]["albedo_mult_linear"] * tj["kinds"][r["kind"]]["wet_dry"]["wet"]["albedo_mult_on_tone"] - r["sheet_ratio"]) <= 0.03 for r in rows),
            "%s" % [(r["kind"], tj["kinds"][r["kind"]]["tone"][r["surface"]]["albedo_mult_linear"], tj["kinds"][r["kind"]]["wet_dry"]["wet"]["albedo_mult_on_tone"], r["sheet_ratio"]) for r in rows])
    part_a_third(tj, R)


def part_a_third(tj, R):
    """The second review's four faults (Jafar's ruling of 9 October): each fix is present in target.json as the reviewer wrote it"""
    K_ = tj["kinds"]
    chk = lambda kid, name: next((c for c in K_[kid]["checks"] if c["name"] == name), None)
    # ---- R1 the houses
    hs = tj["houses"]
    ids = [h["id"] for h in hs["list"]]
    st = {h["id"]: h["state"] for h in hs["list"]}
    sw_path = os.path.join(REPO, "production", "specs", "street-wear.json")
    sw_ids = [h["bay"] for h in json.load(open(sw_path))["houses"]] if os.path.exists(sw_path) else ids
    sooted = [i for i in ids if st[i] == "sooted"]
    R.check("A28 houses (R1a): the 13 houses of street-wear.json each carry a state; no parade bay and no west_south bay is sooted; sooted houses are at the inland end (the chandler, west_north) and at most 30 %% of the 13 (%s)" % sooted,
            sorted(ids) == sorted(sw_ids) and len(ids) == 13 and all(not i.startswith(("east_parade", "west_south")) for i in sooted) and 1 <= len(sooted) <= 0.3 * 13 and set(sooted) <= {"east_chandler_bay0", "west_north_bay0", "west_north_bay1", "west_north_bay2"}
            and st[hs["reference_house"]] != "sooted" and hs["counts"] == {k: sum(1 for i in ids if st[i] == k) for k in ("sooted", "as_built", "cleaned")})
    alb = srgb_to_lin(np.array(tj["surfaces"]["brick_red"]["albedo_srgb"], float))
    Yw_ = np.array([0.2126, 0.7152, 0.0722])
    drift = max(abs(float((alb * np.array(h["look_hue_only"]) * Yw_).sum() / (alb * Yw_).sum()) - 1.0) for h in hs["list"])
    R.check("A29 houses (R1c): every house's look is divided by its own luminance on the brick (hue only; the largest change of the wall's luminance %.4f), HOUSE_SET_FACTOR is deleted from the table, the states are the sheet's" % drift,
            drift < 0.005 and any("HOUSE_SET_FACTOR" in r["this_target"] and "DELETE" in r["this_target"] for r in tj["compose"]["recipe_handover"]) and "D13" in [d["id"] for d in tj["disagreements"]])
    ws = K_["wall_soot"]
    mk = ws["tone"]["brick_red"]["mark_srgb"]
    R.check("A30 soot colour (R1b): the sooted mark on brick_red is a grey-brown lerp toward M21's neutral soot (%s), its chroma %.2f of the clean brick's, composed 0.4 to 0.6 (composed_soot_chroma_ratio, house_to_house_ratio, lower_wall_excess are checks of wall_soot); D9 withdraws 0.84" % (mk, ws["geometry"]["chroma_ratio_of_mark"]["brick_red"]),
            0.3 <= ws["geometry"]["chroma_ratio_of_mark"]["brick_red"] <= 0.5 and all(chk("wall_soot", n) for n in ("composed_soot_chroma_ratio", "house_to_house_ratio", "lower_wall_excess"))
            and "withdrawn" in next(d for d in tj["disagreements"] if d["id"] == "D9")["chose"])
    # ---- R2 the head band
    hb = K_["wall_head_band"]
    lv = [(l["h_m"], l["level"]) for l in hb["envelope"]["levels"]]
    h50 = next(h0 + (h1 - h0) * (l0 - 0.5) / (l0 - l1) for (h0, l0), (h1, l1) in zip(lv[:-1], lv[1:]) if l0 >= 0.5 > l1)
    fw = hb["envelope"]["feature_weights"]
    qg = [g["house"] for g in tj["places"]["quay_gables"]["gables"]]
    R.check("A31 head band (R2): full strength only under gable verges and barges (quay-facing 1.0, other 0.3 to 1.0), coping scale 0.3, eaves gutter strength 0 to 0.2 and depth 0.1 to 0.3 m (profile half-strength at %.3f m: a course line), the quay gables %s are houses of the street, composed_eaves_front_ratio 0.90 to 1.10" % (h50, qg),
            fw["gable_verge_quay_facing"] == 1.0 and fw["gable_verge_other"] == [0.3, 1.0] and fw["eaves_gutter_front"] == [0.0, 0.2] and hb["envelope"]["depth_scale"]["coping_or_string_course"] == 0.3
            and abs(h50 / 0.075 - round(h50 / 0.075)) < 0.02 and set(qg) <= set(ids) and (chk("wall_head_band", "composed_eaves_front_ratio")["min"], chk("wall_head_band", "composed_eaves_front_ratio")["max"]) == (0.90, 1.10))
    # ---- R3 the new mask checks, as the reviewer wrote them
    want = [("wall_foot_splash", "core_column_cv", 0.0, 0.05, {"from_m": 0.0, "to_m": 0.20}), ("wall_foot_damp", "core_column_cv", 0.0, 0.05, {"from_m": 0.0, "to_m": 0.25}),
            ("wall_head_band", "core_column_cv", 0.0, 0.05, {"from_m": 0.0, "to_m": 0.15, "source": "top"}), ("gutter_grime", "core_column_cv", 0.0, 0.05, {"from_m": 0.05, "to_m": 0.23}),
            ("wall_foot_splash", "edge_on_course_share", 0.6, 1.0, {"course_m": 0.075, "tol_mm": 10}), ("salt_bloom", "edge_on_course_share", 0.6, 1.0, {"course_m": 0.075, "tol_mm": 10}), ("wall_head_band", "edge_on_course_share", 0.6, 1.0, {"course_m": 0.075, "tol_mm": 10}),
            ("salt_bloom", "brick_neighbour_same_share", 0.3, 0.8, {}), ("streak_sill", "rivulet_spacing_cv", 0.25, 99.0, {}), ("streak_sill", "rivulet_length_cv", 0.25, 99.0, {}),
            ("wall_soot", "lower_wall_excess", 0.05, 0.15, {"low_from_m": 0.1, "low_to_m": 0.6, "high_from_m": 1.5, "high_to_m": 3.5}), ("iron_wear", "coverage_share_below_m", 0.25, 0.6, {"below_m": 0.3}),
            ("stone_top_lichen", "blob_eqd_mm", 10, 60, {"stat": "p50", "min_area_mm2": 50}), ("stone_top_lichen", "size_cv", 0.3, 99.0, {})]
    miss = []
    for kid, meas, lo, hi, prm in want:
        cs = [c for c in K_[kid]["checks"] if c["measure"] == meas]
        okc = any(c["min"] == lo and (c["max"] == hi or hi == 99.0 and c["max"] >= 1.0) and all(c["params"].get(a) == b for a, b in prm.items()) for c in cs)
        if not okc:
            miss.append((kid, meas))
    R.check("A32 the six wrong masks (R3): the 14 checks the reviewer listed are in the kinds with the reviewer's zones and bounds (missing %s)" % miss, not miss)
    # ---- R4
    lw = K_["line_wear"]
    ext = lw["mask"]["frame_extent_m"]
    R.check("A33 line mask (R4.1): the frame is the 100 mm band's own (y %.3f to %.3f, line_width_mm %s), the scene's bands are 100 mm" % (ext[1], ext[3], lw["envelope"]["line_width_mm"]), abs(ext[1] + 0.05) < 1e-9 and abs(ext[3] - 0.05) < 1e-9 and lw["envelope"]["line_width_mm"] == 100)
    vt = K_["footway_infill"].get("variant_tone", {})
    R.check("A34 infill tone (R4.2): a variant_tone block names variants 0 to 2 (bitmac 70/68/66) and 3 to 5 (in-situ concrete 150/143/136) and the tone table keeps both colours",
            vt.get("variants_0_2", {}).get("mark_srgb") == [70, 68, 66] and vt.get("variants_3_5", {}).get("mark_srgb") == [150, 143, 136] and K_["footway_infill"]["variants"]["count"] >= 6)
    iw = K_["iron_wear"]
    e_ = iw["mask"]["frame_extent_m"]
    R.check("A35 pipe mask (R4.3): unwrapped round the pipe, %.3f m wide = pi x 0.068 (%.3f), x = 0 the street-facing line, the seam at the back, the back takes the same mask" % (e_[2] - e_[0], math.pi * 0.068),
            abs((e_[2] - e_[0]) - math.pi * 0.068) < 0.002 and abs(iw["envelope"]["circumference_m"] - math.pi * 0.068) < 0.002 and "UNWRAPPED" in iw["where"]["rule"] and "seam" in iw["mask"]["origin"])
    R.check("A36 pillar box (R4.4): iron_wear has a pillar_box_red row (grey primer and rust through the red) and lists the surface; the surface exists", "pillar_box_red" in iw["tone"] and "pillar_box_red" in iw["where"]["surfaces"] and "pillar_box_red" in tj["surfaces"])
    fx = tj["second_review_fixes"]
    R.check("A37 second_review_fixes lists R1 to R4, each with what the review said, what was applied and which choice was taken", [f["id"] for f in fx] == ["R1", "R2", "R3", "R4"] and all(f.get("applied") and f.get("review_said") for f in fx))


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
                okm = (mult / 1.12 <= implied <= mult * 1.12)
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
    # tan filter rows, house-state multipliers, floors
    for kid in tj["kinds_order"]:
        k = tj["kinds"][kid]
        for sname, t in k["tone"].items():
            for al in t.get("also", []):
                R.check("B7 %s on %s: the extra mark '%s' has a share in (0, 1] and a tan colour (R above B by 30)" % (kid, sname, al["name"]), 0 < al["share"] <= 1 and al["mark_srgb"][0] - al["mark_srgb"][2] >= 30)
        hs = k.get("by_house_state")
        if hs:
            R.check("B8 %s: house-state multipliers are in (0, 1] and the sooted one is the lighter (nothing darkened twice)" % kid, all(0 < hs[x] <= 1 for x in ("as_built", "cleaned", "sooted")) and hs["sooted"] >= hs["as_built"])
    cmp_ = tj["compose"]
    exempt = set(cmp_["exempt_from_floor"])
    for kid in tj["kinds_order"]:
        for sname, t in tj["kinds"][kid]["tone"].items():
            m = t["albedo_mult_linear"]
            if m < 1.0:
                fl = cmp_["ground"]["floor"] if sname in cmp_["ground"]["surfaces"] else cmp_["walls"]["floor"]
                R.check("B9 %s on %s: a single mark's multiplier %.2f is not below the floor %.2f (%s)" % (kid, sname, m, fl, "exempt" if kid in exempt else "applies"), m >= fl - 1e-9 or kid in exempt)
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


def _course_px(Y, y0, y1, x0, x1):
    y0 = max(y0, 0)
    y1 = min(y1, Y.shape[0])
    if y1 - y0 < 70:
        return None
    pr = Y[y0:y1, x0:x1].mean(1)
    pr = pr - ndi.uniform_filter1d(pr, 25)
    ac = np.correlate(pr, pr, "full")[len(pr) - 1:]
    j = 5 + int(np.argmax(ac[5:min(40, len(pr) // 2)]))
    return j if ac[j] / ac[0] > 0.12 else None


def sill_columns(rgb):
    """M23: for each white sill or ledge edge with brick below it, the darkest 80 mm wide column 80 to 380 mm below the edge over the median column of the same edge
    (scale from the brick courses, 75 mm, under the edge). Returns [(x, y, min_ratio)]."""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    Y = rgb @ np.array([0.2126, 0.7152, 0.0722])
    white = ndi.binary_opening(ndi.binary_closing((Y > 170) & ((rgb.max(-1) - rgb.min(-1)) < 45), np.ones((5, 5))), np.ones((5, 5)))
    brick = ndi.binary_opening((r >= g - 1) & (r >= b + 6) & (Y > 45) & (Y < 175) & ((r - b) < 70), np.ones((3, 3)))
    lab, n = ndi.label(white)
    out = []
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        m = lab[sl] == i
        W = sl[1].stop - sl[1].start
        if m.sum() < 2500 or W < 60:
            continue
        ys0, xs0 = sl[0].start, sl[1].start
        yb = np.full(W, -1)
        for xx in range(W):
            col = np.where(m[:, xx])[0]
            if len(col):
                yb[xx] = col.max() + ys0
        cp = None
        for xx0 in range(0, W - 40, 40):
            seg = yb[xx0:xx0 + 40]
            if not (seg > 0).any():
                continue
            c = _course_px(Y, int(np.median(seg[seg > 0])) + 8, int(np.median(seg[seg > 0])) + 118, xs0 + xx0, xs0 + xx0 + 40)
            if c:
                cp = c if cp is None else int(round((cp + c) / 2))
        if cp is None:
            continue
        mmpx = 75.0 / cp
        top, bot, win = int(round(80 / mmpx)), int(round(380 / mmpx)), int(round(80 / mmpx))
        vals = []
        for xx in range(0, W - win, max(2, win // 4)):
            yy = yb[xx:xx + win]
            if (yy < 0).any() or np.ptp(yy) > 6:
                continue
            ybm = int(np.median(yy))
            seg = brick[ybm + top:ybm + bot, xs0 + xx:xs0 + xx + win]
            if seg.shape[0] < bot - top or seg.mean() < 0.85:
                continue
            vals.append(Y[ybm + top:ybm + bot, xs0 + xx:xs0 + xx + win][seg].mean())
        if len(vals) >= 6:
            vals = np.array(vals)
            out.append((xs0, int(np.median(yb[yb > 0])), float((vals / np.median(vals)).min())))
    return out


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
    t_unworn = float(np.percentile(thick, 90))              # the UNWORN line is the gauge: a worn line's median thickness is narrower than its 75 mm (the first pass used the median and so took 1.6 m for a camera that is at 1.40 m)
    scale_line = 75.0 / t_unworn
    scale_mm = mm                                           # the stated scale (M30: camera 1.40 m above the road); the line only has to agree with it
    R.check("C1 scale fitted on one dimension (the unworn yellow line, the 90th percentile of its thickness, %.1f px = 75 mm; the median %.1f px is a worn line's) agrees with the stated %.3f mm/px (camera 1.40 m, M30) within 6 %%" % (t_unworn, t_med, mm),
            abs(scale_line - mm) / mm <= 0.06, "fitted %.3f mm/px" % scale_line)
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
    keep = px >= 7.5                     # 7.5 px and up (70 mm2 at the first pass's 3.06 mm/px; M04's smallest dots are about 9 mm across at the corrected scale)
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
    sheet_mm = mmpx
    ref = float(np.median(Yh[430:600, cols]))
    ratio_rows = np.array([np.median(Yh[r:r + 6, cols]) / ref for r in range(560, 730, 6)])
    rows_c = np.arange(560, 730, 6) + 3
    dark_rows = [r for r, v in zip(rows_c, ratio_rows) if v < 0.25]
    foot_row = max(dark_rows) + 3 if dark_rows else 716
    k = tj["kinds"]["wall_foot_splash"]
    hp = k["geometry"]["height_profile"]
    mult = k["tone"]["brick_red"]["albedo_mult_linear"]
    wetm = k["wet_dry"]["wet"]["albedo_mult_on_tone"]       # the Hook sheet is a wet street: its ratios are wet values, dry multiplier x wet multiplier
    errs = []
    for r, v in zip(rows_c, ratio_rows):
        h = (foot_row - r) * mmpx / 1000.0
        if h < 0.02 or h > 0.85:
            continue
        m_h = float(np.interp(h, hp["h_m"], hp["mask"]))
        pred = 1.0 - m_h * (1.0 - mult * wetm)
        errs.append(abs(pred - v))
    mean_err = float(np.mean(errs))
    R.check("C15 the splash profile (dry mult %.2f x wet %.2f = %.3f at mask 1) laid on the sheet gable foot (foot row %d, scale fitted on the course only): mean error %.3f in luminance ratio (needs <= 0.15; the sheet's own brick-to-brick scatter in 6 px bands is about 0.1)" % (mult, wetm, mult * wetm, foot_row, mean_err), mean_err <= 0.15)
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

    # ---- C19 M21: the soot-blackened garden wall, sooted over cleaner panel
    f = "ph-urban_street_03-garden-wall-soot-streaks.jpg"
    rgb = load_rgb(pv(f)).astype(float)
    bx = M["M21"]["preview_boxes"]
    def _box(b):
        x0, x1, y0, y1 = b
        return rgb[y0:y1, x0:x1].reshape(-1, 3)
    ys_, yc_ = float(lum(_box(bx["sooted"])).mean()), float(lum(_box(bx["clean"])).mean())
    sat = lambda c: float((c.max() - c.min()) / c.max())
    sr = sat(np.median(_box(bx["sooted"]), 0)) / sat(np.median(_box(bx["clean"]), 0))
    soot_mult = tj["kinds"]["wall_soot"]["geometry"]["multiplier"]
    R.check("C19 garden wall re-measured on the preview: sooted over cleaner luminance %.3f (M21 0.377 to 0.40; the target's soot multiplier %.2f must lie in 0.37 to 0.48 and so must the measurement within 0.33 to 0.50)" % (ys_ / yc_, soot_mult), 0.33 <= ys_ / yc_ <= 0.50 and 0.37 <= soot_mult <= 0.48)
    ps_, pc_ = _box(bx["sooted"]), _box(bx["clean"])
    hsv_px = lambda p_: float(((p_.max(1) - p_.min(1)) / np.maximum(p_.max(1), 1e-9)).mean())
    r_hsv_px = hsv_px(ps_) / hsv_px(pc_)
    r_c_med = float(chroma_px(np.median(ps_, 0)[None, :])[0] / chroma_px(np.median(pc_, 0)[None, :])[0])
    r_c_px = float(chroma_px(ps_).mean() / chroma_px(pc_).mean())
    cs_ = next(c for c in tj["kinds"]["wall_soot"]["checks"] if c["name"] == "composed_soot_chroma_ratio")
    comp_c = composition(tj, draw, cs_, 1990)
    R.check("C19b the soot keeps little of the brick's colour (second review R1b): HSV saturation of the sooted panel over the cleaner, per pixel %.2f and of the medians %.2f; CIE chroma of the medians %.2f and per pixel %.2f (M21: 0.65, 0.73, 0.455, 0.43); "
            "the first pass's 0.84 (HSV of two medians) is not what the photograph shows on any per-pixel measure; the target's composed sooted wall keeps %.2f of the clean wall's chroma (accepted 0.4 to 0.6, and within 0.12 of the photograph's per-pixel chroma ratio)" % (r_hsv_px, sr, r_c_med, r_c_px, comp_c),
            0.55 <= r_hsv_px <= 0.78 and 0.38 <= r_c_med <= 0.60 and 0.33 <= r_c_px <= 0.55 and 0.4 <= comp_c <= 0.6 and abs(comp_c - r_c_px) <= 0.12)
    # ---- C20 M22: the head under the Hook sheet's gable verge, and the lower wall of the right-hand cottage
    Yl = lum(hs)
    colsel = slice(15, 170)
    head = float(np.median(Yl[40:170, colsel]) / np.median(Yl[250:600, colsel]))
    bm = M["M22"]["values"]
    hbm = tj["kinds"]["wall_head_band"]["by_house_state"]["as_built"]
    if overlays:
        hp_ = tj["kinds"]["wall_head_band"]["geometry"]["height_profile"]
        im = Image.fromarray(hs.astype(np.uint8)).crop((0, 0, 300, 300)).resize((900, 900), Image.LANCZOS)
        d = ImageDraw.Draw(im, "RGBA")
        row0 = 20.0                      # the verge's lower edge on the sheet (the first dark band is centred on row 30)
        for h, m_h in zip(hp_["h_m"], hp_["mask"]):
            y = (row0 + h * 1000.0 / sheet_mm) * 3.0
            d.line([(0, y), (900, y)], fill=(0, 255, 255, 200), width=2)
            d.text((6, y - 12), "%.2f m below the verge  mask %.2f" % (h, m_h), fill=(0, 255, 255, 255))
        d.line([(0, row0 * 3), (900, row0 * 3)], fill=(255, 255, 0, 255), width=3)
        d.text((6, row0 * 3 + 4), "verge's lower edge; scale from the 75 mm course (%.1f mm/px): Hook sheet, not a photograph" % sheet_mm, fill=(255, 255, 0, 255))
        out = pv("hook-sheet-gable-head-target-on-sheet.jpg")
        im.convert("RGB").save(out, quality=86, optimize=True)
        overlay_log.append(os.path.basename(out))
    R.check("C20 sheet gable head re-measured: luminance %.2f of the body over rows 40 to 170 (M22 0.61; accepted 0.50 to 0.72); the target's as-built head multiplier %.2f x the wet 0.90 = %.2f lies in the same range" % (head, hbm, hbm * 0.9), 0.50 <= head <= 0.72 and 0.50 <= hbm * 0.9 <= 0.72)
    cot = Yl[:, 1490:1590]
    body = float(np.median(cot[380:430]))
    lowr = float(np.mean([np.median(cot[r:r + 8]) for r in range(516, 580, 8)]))
    lw = tj["kinds"]["wall_soot"]["geometry"]["lower_wall_ratio"]["composed"]
    R.check("C21 sheet right-hand cottage lower wall re-measured: %.2f of the wall above (M22b 0.84 to 0.93, mean 0.90); the composed target value %.2f is within 0.06 of it" % (lowr / body, lw), 0.80 <= lowr / body <= 0.96 and abs(lw - lowr / body) <= 0.08)
    # ---- C21b M28: the sheet shows no dark head under an eaves gutter (Mickey's front) nor under the right-hand cottage's gable verge
    cm_ = Yl[:, 385:445]
    mbody = float(cm_[200:331].mean())
    first10 = float(cm_[160:170].mean() / mbody)
    rest_ = [float(cm_[r:r + 10].mean() / mbody) for r in range(170, 340, 10)]
    gv = Yl[322:478, 1560:1595]
    gb = [float(gv[r:r + 16].mean()) for r in range(16, 150, 16)]
    ce_ = next(c for c in tj["kinds"]["wall_head_band"]["checks"] if c["name"] == "composed_eaves_front_ratio")
    comp_e = composition(tj, draw, ce_, 1990)
    R.check("C21b Mickey's front under its eaves gutter, re-measured: %.2f of its body in the first 10 rows (the dentil course's shadow; review 0.63), then %.2f to %.2f (mean %.2f; review 1.00 to 1.10); the right-hand cottage's gable under its verge is flat: top three bands over the last three %.2f (0.85 to 1.25); "
            "the target's eaves-gutter head composes to %.2f at 0.3 m (accepted 0.90 to 1.10: inside the sheet's range)" % (first10, min(rest_), max(rest_), float(np.mean(rest_)), float(np.mean(gb[:3]) / np.mean(gb[-3:])), comp_e),
            0.5 <= first10 <= 0.8 and 0.90 <= float(np.mean(rest_)) <= 1.15 and 0.85 <= float(np.mean(gb[:3]) / np.mean(gb[-3:])) <= 1.25 and min(rest_) <= comp_e <= max(rest_) and 0.90 <= comp_e <= 1.10)
    # ---- C22 M23: no clear streak under the sills of a maintained 2019 brick street
    f = "ph-urban_street_03-facade-sills-no-streaks.jpg"
    rgb = load_rgb(pv(f)).astype(float)
    cols = sill_columns(rgb)
    mr = np.array([c[2] for c in cols])
    dens = tj["kinds"]["streak_sill"]["where"]["density"]
    R.check("C22 sill streaks re-measured on the preview: %d sill edges, darkest column over the median column %.2f to %.2f (median %.2f); none below 0.80 (M23: 0.87 to 0.99); the target's share of sills with a set (%.2f) is above the measured 3 to 15 %% (a 1990 street is dirtier)" % (len(cols), mr.min(), mr.max(), np.median(mr), dens["typical"]),
            len(cols) >= 3 and mr.min() >= 0.80 and 0.90 <= np.median(mr) <= 1.0 and dens["typical"] >= 0.15)
    # ---- C23 M25: the sheet's gable downpipe
    pipe = hs[100:720, 204:211]
    ochre = (pipe[..., 0] > 95) & (pipe[..., 0] - pipe[..., 2] > 35) & (pipe[..., 1] > 70) & (pipe[..., 0] > 1.3 * pipe[..., 2])
    rows_o = float(ochre.any(1).mean())
    ic = tj["kinds"]["iron_wear"]["where"]["density"]["range"]
    R.check("C23 sheet downpipe re-measured: paint loss on %.1f %% of its length (M25 4.8 to 7 %%); the target's 4 to 8 %% (%s) brackets it" % (100 * rows_o, ic), 0.03 <= rows_o <= 0.09 and ic[0] <= rows_o + 0.02 and ic[1] >= rows_o - 0.02)
    # ---- C24 M24: the channel is lighter than the road
    f = "ph-urban_street_03-kerb-flags-channel-view.jpg"
    rgb = load_rgb(pv(f)).astype(float)
    Yc = lum(rgb)
    chan = float(np.median(Yc[372:388, 250:550]))
    road = float(np.median(Yc[560:760, 100:800]))
    fringe = float(np.median(Yc[432:470, 250:750]))
    R.check("C24 channel re-measured: channel setts %.2f x the open road (M24 1.4, 1.35 to 1.7) and the strip beside it %.2f x (0.95, 0.91 to 0.97); the reviewer's 150/146/140 channel would be %.1f x the road, the target's %s is %.2f x"
            % (chan / road, fringe / road, float(lum(np.array([150, 146, 140.0])) / lum(np.array(tj["surfaces"]["asphalt_dry"]["albedo_srgb"], float))), tj["surfaces"]["channel_concrete"]["albedo_srgb"],
               float(lum(np.array(tj["surfaces"]["channel_concrete"]["albedo_srgb"], float)) * 0.85 / lum(np.array(tj["surfaces"]["asphalt_dry"]["albedo_srgb"], float)))),
            1.2 <= chan / road <= 1.8 and 0.88 <= fringe / road <= 1.0)
    # ---- C25 M26: how much of the yellow line is lost
    f = "ph-urban_street_03-oil-drip-speckle.jpg"
    rgb = load_rgb(pv(f))
    yel = ((rgb[..., 0].astype(int) - rgb[..., 2].astype(int)) > 45) & (rgb[..., 0] > 110)
    yel = ndi.binary_closing(yel, np.ones((3, 3)))
    xs_, ys_c = [], []
    for x in range(30, rgb.shape[1] - 10):
        r_ = np.where(yel[:, x])[0]
        if len(r_) >= 6:
            xs_.append(x); ys_c.append(r_.mean())
    co2 = np.polyfit(xs_, ys_c, 2)
    cov = []
    for x in range(30, rgb.shape[1] - 10):
        sl_ = np.polyval(np.polyder(co2), x)
        Lc = (75.0 / P[f]["mm_per_px"]) * math.sqrt(1 + sl_ * sl_)
        yc0 = np.polyval(co2, x)
        seg = yel[max(int(round(yc0 - Lc / 2)) - 3, 0):int(round(yc0 + Lc / 2)) + 3, x]
        cov.append(min(1.0, seg.sum() / Lc))
    loss = 1 - float(np.mean(cov))
    lr = tj["kinds"]["line_wear"]["where"]["density"]["range"]
    m26 = M["M26"]["values"]["loss_share"]
    R.check("C25 yellow line re-measured: %.0f %% of the nominal 75 mm strip (%.1f px at %.3f mm/px) lost (M26 %.0f +/- 8 %%, camera 1.40 m; 22 %% at the assumed 1.6 m); the target's %s brackets it" % (100 * loss, 75.0 / P[f]["mm_per_px"], P[f]["mm_per_px"], 100 * m26, lr), abs(loss - m26) <= 0.08 and lr[0] - 0.02 <= loss <= lr[1] + 0.05)
    # ---- C26 M03: the sealed crack on the full-resolution crop
    f = "ph-asphalt_02-road-sealed-crack.jpg"
    rgb = load_rgb(pv(f)).astype(float)
    Yl_ = lum(rgb)
    ysm = ndi.gaussian_filter(Yl_, 2.0)
    surf = float(np.median(Yl_))
    mm_ = P[f]["mm_per_px"]
    ws_, cores = [], []
    for r_ in range(0, rgb.shape[0], 2):
        row = ysm[r_, 60:420]
        j = int(np.argmin(row))
        if row[j] > 0.6 * surf:
            continue
        a_ = b_ = j
        while a_ > 0 and row[a_ - 1] < 0.7 * surf:
            a_ -= 1
        while b_ < len(row) - 1 and row[b_ + 1] < 0.7 * surf:
            b_ += 1
        ws_.append((b_ - a_ + 1) * mm_)
        cores.append(row[j])
    pw = np.percentile(ws_, [10, 50, 90])
    mw = tj["kinds"]["road_crack"]["geometry"]["main_crack_width_mm"]
    R.check("C26 sealed crack re-measured on the preview: widths below 0.7 of the surface p10 / p50 / p90 = %.0f / %.0f / %.0f mm (M03 15 / 35 / 59); the target's main width %s mm lies around it; core luminance %.2f of the surface (0.23)" % (pw[0], pw[1], pw[2], mw, float(np.median(cores) / surf)),
            10 <= pw[0] <= 22 and 28 <= pw[1] <= 45 and 45 <= pw[2] <= 75 and mw["p10"] <= pw[1] <= mw["p90"] and 0.15 <= np.median(cores) / surf <= 0.35)
    # ---- C27 M05: the reinstatement's seam
    f = "ph-urban_street_02-road-reinstatement-ortho.jpg"
    rgb = load_rgb(pv(f)).astype(float)
    Yr = lum(rgb)
    roadY = float(np.median(Yr[100:450, 500:1100]))
    box = ndi.gaussian_filter(Yr, 1.2)[560:830, 30:170]
    seam = float(np.percentile(box, 4) / roadY)
    infill = float(np.median(Yr[560:780, 170:330]) / roadY)
    ptone = tj["kinds"]["road_patch"]["tone"]["asphalt_dry"]["albedo_mult_linear"]
    R.check("C27 reinstatement re-measured: the seam's darkest 4 %% of pixels read %.2f of the road (M05 0.63 to 0.77), the infill %.2f (0.93); the target's seam multiplier %.2f and infill %.2f (%.2f x level %.2f)"
            % (seam, infill, ptone, 1 - (1 - ptone) * tj["kinds"]["road_patch"]["envelope"]["infill_level"], 1 - ptone, tj["kinds"]["road_patch"]["envelope"]["infill_level"]),
            0.55 <= seam <= 0.80 and 0.85 <= infill <= 1.0 and 0.63 <= ptone <= 0.77 and abs((1 - (1 - ptone) * tj["kinds"]["road_patch"]["envelope"]["infill_level"]) - 0.93) <= 0.03)
    # ---- C28 M06: share of tan filter tips among the kerb litter
    f = "ph-urban_street_02-kerb-litter-view.jpg"
    rgb = load_rgb(pv(f)).astype(float)
    Yk = rgb @ np.array([0.2126, 0.7152, 0.0722])
    bgk = ndi.median_filter(Yk, size=31)
    sat_ = rgb.max(-1) - rgb.min(-1)
    bright = ndi.binary_opening((Yk > 1.35 * bgk + 8) | ((Yk > 1.1 * bgk) & (sat_ > 45) & (rgb[..., 0] > rgb[..., 2] + 40)))
    lab_k, nk = ndi.label(bright)
    bits = []
    for i_, sl_ in enumerate(ndi.find_objects(lab_k), start=1):
        m_ = lab_k[sl_] == i_
        if m_.sum() < 6:
            continue
        cy, cx = ndi.center_of_mass(m_)
        cy += sl_[0].start; cx += sl_[1].start
        if 225 <= cy <= 320 and 150 < cx < 1100:
            c_ = rgb[sl_][m_].mean(0)
            if c_[1] > c_[0] + 30:       # the green toy-like thing is not litter of the street's kind
                continue
            bits.append(c_[0] - c_[2] > 45)
    tan_share = float(np.mean(bits))
    tan_t = tj["kinds"]["cig_end"]["tone"]["flag_concrete"]["also"][0]["share"]
    R.check("C28 kerb litter re-counted on the preview: %d of %d bits are clearly tan (%.2f; M06 0.31 to 0.46); the target's tan share is %.2f" % (sum(bits), len(bits), tan_share, tan_t), len(bits) >= 8 and 0.2 <= tan_share <= 0.5 and 0.3 <= tan_t <= 0.5)
    return overlay_log


# ---------------------------------------------------------------- D: envelopes
ENVELOPE_MEASURES = {"role_length_per_m2", "role_blob_eqd_mm", "role_count", "role_share_below"}
DATA_MEASURES = {"tone_ratio", "crack_flag_share"}
COMPOSITION_MEASURES = {"house_to_house_ratio", "composed_soot_chroma_ratio", "composed_eaves_front_ratio", "composed_foot_ratio", "composed_salt_ratio", "composed_wall_min_ratio", "composed_soot_ratio", "composed_head_ratio", "channel_over_road", "fringe_over_road", "composed_ground_min_ratio"}


def ppm_for(k):
    t = k["texel"]["px_per_m_recommended"]
    ext = k["mask"]["frame_extent_m"]
    big = max(ext[2] - ext[0], ext[3] - ext[1]) > 2.0
    if k["texel"]["smallest_feature_mm"] <= 3:
        return min(t, 800 if big else 1000)          # hairline kinds need the finer scale even on a big frame
    return min(t, 400 if big else 1000)


def _poly_area(q):
    xs_ = np.array([a for a, _ in q["poly"]])
    ys_ = np.array([b for _, b in q["poly"]])
    return 0.5 * abs(np.dot(xs_, np.roll(ys_, -1)) - np.dot(ys_, np.roll(xs_, -1)))


def run_mask_check(c, mask, ppm):
    """One check of a kind on a generated mask (what unit 4.5's automatic check does). Returns (value, ok)."""
    m, p = c["measure"], dict(c["params"])
    if m == "foot_profile":
        res = foot_profile_check(mask, ppm, p["points"], p.get("axis", "rows_from_bottom"))
        v = float(np.mean([r[4] for r in res]))
        return v, v >= 0.8
    v = measure(mask, ppm, m, **p)
    return v, c["min"] <= v <= c["max"]


def eval_check(c, k, mask, ppm, polys, ext_mm, draw, edge_mm=0.0):
    """value of one check on a kind's drawn envelope (polygons) and its rasterised mask"""
    m, p = c["measure"], dict(c["params"])
    fx0, fy0, fx1, fy1 = ext_mm
    if m == "foot_profile":
        res = foot_profile_check(mask, ppm, p["points"], p.get("axis", "rows_from_bottom"))
        return float(np.mean([r[4] for r in res])), [r for r in res if not r[4]]
    if m == "tone_ratio":
        sc = k["geometry"]["slab_classes"]
        return float(lum(np.array(sc["dark"]["srgb"], float)) / lum(np.array(sc["pale"]["srgb"], float))), None
    if m == "crack_flag_share":
        slabs = [q for q in polys if q["role"].startswith("slab_")]
        cracks = [q for q in polys if q["role"] == "crack"]
        hit = 0
        for sl_ in slabs:
            xs = [a for a, _ in sl_["poly"]]; ys = [b for _, b in sl_["poly"]]
            if any(min(xs) <= np.mean([a for a, _ in q["poly"]]) <= max(xs) and min(ys) <= np.mean([b for _, b in q["poly"]]) <= max(ys) for q in cracks):
                hit += 1
        return hit / max(len(slabs), 1), None
    if m == "role_length_per_m2":
        tot = 0.0
        for q in polys:
            if q["role"] != p["role"]:
                continue
            cx = np.mean([a for a, _ in q["poly"]]); cy = np.mean([b for _, b in q["poly"]])
            if fx0 <= cx <= fx1 and fy0 <= cy <= fy1:
                tot += q.get("length_mm", 0.0)
        return tot / 1000.0 / ((fx1 - fx0) * (fy1 - fy0) / 1e6), None
    if m == "role_blob_eqd_mm":
        eqs = [2 * math.sqrt(_poly_area(q) / math.pi) for q in polys if q["role"] == p["role"]]
        return (float(np.percentile(eqs, 90 if p.get("stat") == "p90" else 50)) if eqs else 0.0), None
    if m == "role_count":
        return float(sum(1 for q in polys if q["role"] == p["role"])), None
    if m == "role_share_below":
        sel = [q for q in polys if q["role"] == p["role"]]
        if not sel:
            return 0.0, None
        w = [(_poly_area(q) if p.get("of", "area") == "area" else 1.0) * (1.0 if np.mean([b for _, b in q["poly"]]) - fy0 < p["below_mm"] else 0.0) for q in sel]
        tot = sum(_poly_area(q) if p.get("of", "area") == "area" else 1.0 for q in sel)
        return float(sum(w) / tot), None
    if m == "count_per_m2" and p.get("region") == "speckle_band":
        dots = [q for q in polys if q["role"] == "dot"]
        xs = [np.mean([a for a, _ in q["poly"]]) for q in dots]
        Lb = (max(xs) - min(xs)) / 1000.0
        return len(dots) / max(Lb * k["envelope"]["width_m"], 1e-6), None
    if "only_roles" in p:
        roles = p.pop("only_roles")
        sub = [q for q in polys if q["role"] in roles]
        wrap = "xy" if "seamless" in k["mask"]["origin"] else "x" if "tile" in k["mask"]["origin"] else False
        mk = draw.rasterize(sub, ext_mm, ppm, edge_mm, wrap=wrap)
        return measure(mk, ppm, m, **p), None
    return measure(mask, ppm, m, **p), None


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
        org = k["mask"]["origin"]
        wrap = "xy" if "seamless" in org else "x" if "tile" in org else False
        for seed in (1990, 2024):
            for variant in range(3):
                polys = draw.kind_envelope(tj, kid, seed, variant)
                mask = draw.rasterize(polys, ext_mm, ppm, ed.get(kid, 0.0), wrap=wrap)
                runs += 1
                for c in k["checks"]:
                    if c["measure"] in COMPOSITION_MEASURES:
                        continue
                    results.setdefault(c["name"], []).append(eval_check(c, k, mask, ppm, polys, ext_mm, draw, ed.get(kid, 0.0)))
        summary[kid] = {}
        for c in k["checks"]:
            if c["measure"] in COMPOSITION_MEASURES:
                continue
            vals = [v for v, _ in results[c["name"]]]
            med = float(np.median(vals))
            if c["measure"] == "foot_profile":
                ok = med >= 0.8
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
        slack = 120.0 if kid not in ("streak_coping", "flag_patch_crack", "road_oil", "road_crack", "tyre_scuff", "streak_sill") else 400.0
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


# ---------------------------------------------------------------- E: composition and wrong masks
STATE_WEIGHT = {"sooted": 1.0, "as_built": 0.35, "cleaned": 0.0}


def _lin(rgb8):
    return srgb_to_lin(np.asarray(rgb8, float))


def _ylin(l):
    return 0.2126 * l[..., 0] + 0.7152 * l[..., 1] + 0.0722 * l[..., 2]


def _ratio(tj, kid, surface):
    """the per-channel ratio mark_lin / surface_lin the builder applies (the dirt tint travels in it)"""
    return _lin(tj["kinds"][kid]["tone"][surface]["mark_srgb"]) / _lin(tj["surfaces"][surface]["albedo_srgb"])


def _darken(alb, mask, ratio, strength=1.0):
    f = 1.0 - np.clip(mask * strength, 0, 1)[..., None] * (1.0 - ratio[None, None, :])
    return alb * f


def _floor_to(alb, clean, fl):
    sc = np.maximum(1.0, fl * _ylin(clean) / np.maximum(_ylin(alb), 1e-9))
    return alb * sc[..., None]


_M_XYZ = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
_W_XYZ = np.array([0.95047, 1.0, 1.08883])


def lab_chroma(lin):
    """CIE (L*a*b*, D65) chroma C* of a linear-light sRGB colour"""
    xyz = (_M_XYZ @ np.asarray(lin, float)) / _W_XYZ
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return float(np.hypot(500 * (f[0] - f[1]), 200 * (f[1] - f[2])))


def chroma_px(srgb8):
    """CIE chroma C* of every colour of an (n, 3) array of sRGB 0..255"""
    lin = srgb_to_lin(np.asarray(srgb8, float))
    xyz = (lin @ _M_XYZ.T) / _W_XYZ
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return np.hypot(500 * (f[:, 0] - f[:, 1]), 200 * (f[:, 1] - f[:, 2]))


def _fit_strip(m, Hp, Wp, ppm_in, ppm, from_top=False):
    """A builder's own mask fitted to the composition strip (Hp x Wp at ppm px/m): resampled to ppm, tiled across x, cropped to Hp rows counted from the pavement line (the bottom row) or,
    for from_top (the head band), from the feature (the top row); a shorter mask is padded with 0 beyond its frame"""
    m = np.asarray(m, float)
    if abs(ppm_in - ppm) > 1e-6:
        m = ndi.zoom(m, ppm / ppm_in, order=1)
    if m.shape[1] < Wp:
        m = np.tile(m, (1, int(math.ceil(Wp / m.shape[1]))))
    m = m[:, :Wp]
    if m.shape[0] < Hp:
        pad = Hp - m.shape[0]
        m = np.pad(m, ((0, pad), (0, 0)) if from_top else ((pad, 0), (0, 0)))
    return (m[:Hp] if from_top else m[m.shape[0] - Hp:]).copy()


def _paste_centred(m, Hp, Wp, ppm_in, ppm, cx_px):
    """the downpipe's algae mask (a 0.9 m wide frame, pavement line at its bottom) pasted with its centre at cx_px of the strip"""
    m = np.asarray(m, float)
    if abs(ppm_in - ppm) > 1e-6:
        m = ndi.zoom(m, ppm / ppm_in, order=1)
    out = np.zeros((Hp, Wp))
    h = min(m.shape[0], Hp)
    x0 = cx_px - m.shape[1] // 2
    for j in range(m.shape[1]):
        if 0 <= x0 + j < Wp:
            out[Hp - h:, x0 + j] = m[m.shape[0] - h:, j]
    return out


def _squeeze_depth(m, scale):
    """the head band's profile compressed in depth by `scale` (rows counted from the feature): row r takes the value of row r / scale"""
    Hp = m.shape[0]
    src = np.arange(Hp) / scale
    i0 = np.floor(src).astype(int)
    w = (src - i0)[:, None]
    a = np.where((i0 < Hp)[:, None], m[np.clip(i0, 0, Hp - 1)], 0.0)
    b = np.where((i0 + 1 < Hp)[:, None], m[np.clip(i0 + 1, 0, Hp - 1)], 0.0)
    return a * (1 - w) + b * w


def compose_walls(tj, draw, seed=1990, state="cleaned", ppm=100, head=False, masks=None, masks_ppm=None, head_strength=1.0, head_depth_scale=1.0):
    """A 2.0 m x 1.6 m strip of brick at the pavement line with a downpipe at x = 1.0: the kinds of target.json compose.walls applied in their order, dry, house wear 1.0.
    Returns dict(clean, pre, final, masks, ppm); arrays have row 0 at the top (height 1.6 m).
    masks: a dict kind id -> array of the BUILDER'S OWN mask for that kind (row 0 the top of the kind's frame, the bottom row the pavement line; the head band's top row the feature), at masks_ppm px/m (a number,
    or a dict by kind; default the strip's own ppm); a kind named there is not drawn from the target's envelope but taken from the array, so unit 4.5 can run every composition check on its own masks.
    head_strength and head_depth_scale: the head band's strength and its profile compressed in depth (a gable verge 1.0 and 1.0; an eaves gutter 0 to 0.2 and 0.15 to 0.44)."""
    ed = draw.edges_by_kind(tj)
    cm = tj["compose"]["walls"]
    W_mm, H_mm = 2000.0, 1600.0
    ext = (0.0, 0.0, W_mm, H_mm)
    ras = lambda kid, polys: draw.rasterize(polys, ext, ppm, ed.get(kid, 0.0), wrap="x")
    Hp, Wp = int(H_mm * ppm / 1000), int(W_mm * ppm / 1000)
    mp = lambda kid: masks_ppm.get(kid, ppm) if isinstance(masks_ppm, dict) else (ppm if masks_ppm is None else masks_ppm)
    given = masks or {}
    clean = np.broadcast_to(_lin(tj["surfaces"]["brick_red"]["albedo_srgb"]), (Hp, Wp, 3)).copy()
    out = {}
    if "wall_soot" in given:
        out["wall_soot"] = _fit_strip(given["wall_soot"], Hp, Wp, mp("wall_soot"), ppm)
    else:
        full = draw.rasterize(draw.kind_envelope(tj, "wall_soot", seed, 0), (0.0, 0.0, 4000.0, 4000.0), ppm, ed.get("wall_soot", 0.0), wrap="x")
        out["wall_soot"] = full[full.shape[0] - Hp:, :Wp]
    for kid in ("wall_foot_damp", "wall_foot_splash", "salt_bloom"):
        out[kid] = _fit_strip(given[kid], Hp, Wp, mp(kid), ppm) if kid in given else ras(kid, draw.kind_envelope(tj, kid, seed, 0))
    if "algae_downpipe" in given:
        out["algae_downpipe"] = _paste_centred(given["algae_downpipe"], Hp, Wp, mp("algae_downpipe"), ppm, Wp // 2)
    else:
        out["algae_downpipe"] = ras("algae_downpipe", draw.transform(draw.kind_envelope(tj, "algae_downpipe", seed, 0), 1000.0, 0.0))
    if head:
        if "wall_head_band" in given:
            hb = _fit_strip(given["wall_head_band"], Hp, Wp, mp("wall_head_band"), ppm, from_top=True)
        else:
            hb = ras("wall_head_band", draw.transform(draw.kind_envelope(tj, "wall_head_band", seed, 0), 0.0, H_mm))
        if head_depth_scale != 1.0:
            hb = _squeeze_depth(hb, head_depth_scale)
        out["wall_head_band"] = hb
    masks_out = out
    alb = clean.copy()
    for kid in cm["stage_1_L0_multiplicative"] + cm["stage_2_L1_multiplicative"]:
        if kid not in masks_out:
            continue
        st = STATE_WEIGHT[state] if kid == "wall_soot" else (head_strength if kid == "wall_head_band" else 1.0)
        ratio = _ratio(tj, kid, "brick_red")
        if kid == "wall_head_band":
            hs_ = tj["kinds"][kid]["by_house_state"]
            f = (1.0 - hs_[state]) / (1.0 - tj["kinds"][kid]["tone"]["brick_red"]["albedo_mult_linear"])
            ratio = 1.0 - f * (1.0 - ratio)
        alb = _darken(alb, masks_out[kid], ratio, st)
    pre = _floor_to(alb, clean, cm["floor"])
    final = pre.copy()
    mk = masks_out["salt_bloom"]
    sm = _lin(tj["kinds"]["salt_bloom"]["tone"]["brick_red"]["mark_srgb"])
    final = final * (1 - mk[..., None]) + sm[None, None, :] * mk[..., None]
    return {"clean": clean, "pre": pre, "unfloored": alb, "final": final, "masks": masks_out, "ppm": ppm}


def compose_head(tj, draw, seed, state, ppm=100):
    return compose_walls(tj, draw, seed, state, ppm, head=True)


def upper_wall_colour(tj, draw, seed, state, masks=None, masks_ppm=None, ppm=100):
    """mean linear colour of the composed upper wall (rows from 1.3 m up, albedo, no haze, no floor) in a house state, and the clean brick's"""
    a = compose_walls(tj, draw, seed, state, ppm, masks=masks, masks_ppm=masks_ppm)
    rows = slice(0, a["clean"].shape[0] - int(1.3 * ppm))
    return a["unfloored"][rows].reshape(-1, 3).mean(0), a["clean"][rows].reshape(-1, 3).mean(0)


def composition(tj, draw, c, seed=1990, masks=None, masks_ppm=None):
    """One composition check. masks / masks_ppm: the builder's own masks by kind id (see compose_walls) in place of the target's drawn envelopes; for channel_over_road and fringe_over_road the gutter_grime mask
    (its frame, 2.0 x 0.75 m, the kerb foot at the bottom row) at masks_ppm px/m (default 500)."""
    m, p = c["measure"], c["params"]
    ppm = 100
    kw = dict(masks=masks, masks_ppm=masks_ppm)
    if m in ("composed_foot_ratio", "composed_salt_ratio", "composed_wall_min_ratio"):
        r = compose_walls(tj, draw, seed, p.get("state", "cleaned"), ppm, **kw)
        Hp = r["clean"].shape[0]
        ratio = _ylin(r["pre"]) / _ylin(r["clean"])
        if m == "composed_foot_ratio":
            rr = int(round(Hp - 1 - p.get("height_m", 0.1) * ppm))
            return float(ratio[rr - 1:rr + 2, int(0.6 * ppm):int(1.4 * ppm)].mean())
        if m == "composed_wall_min_ratio":
            return float(ratio.min())
        sm = r["masks"]["salt_bloom"] > 0.4
        rows = np.zeros_like(sm)
        rows[Hp - 1 - int(0.52 * ppm):Hp - int(0.30 * ppm), :] = True
        sel = sm & rows
        fin = _ylin(r["final"]) / _ylin(r["clean"])
        return float(fin[sel].mean()) if sel.any() else 0.0
    if m == "composed_soot_ratio":
        a = compose_walls(tj, draw, seed, "sooted", ppm, **kw)
        b = compose_walls(tj, draw, seed, "cleaned", ppm, **kw)
        rows = slice(0, a["clean"].shape[0] - int(1.3 * ppm))
        return float(_ylin(a["unfloored"])[rows].mean() / _ylin(b["unfloored"])[rows].mean())
    if m == "composed_soot_chroma_ratio":
        col, clean = upper_wall_colour(tj, draw, seed, "sooted", masks, masks_ppm, ppm)
        return lab_chroma(col) / lab_chroma(clean)
    if m == "house_to_house_ratio":
        hs = tj["houses"]
        cols = {st: upper_wall_colour(tj, draw, seed, st, masks, masks_ppm, ppm)[0] for st in ("cleaned", "as_built", "sooted")}
        ys = {h["id"]: float(_ylin(cols[h["state"]] * np.asarray(h["look_hue_only"], float))) for h in hs["list"]}
        ref = ys[hs["reference_house"]]
        vals = [ys[h["id"]] / ref for h in hs["list"] if h["in_sheet_frame"]]
        return float(max(vals, key=lambda v: abs(math.log(v))))
    if m == "composed_head_ratio":
        r = compose_walls(tj, draw, seed, p.get("state", "cleaned"), ppm, head=True, **kw)
        row = int(round(0.1 * ppm))
        return float((_ylin(r["unfloored"]) / _ylin(r["clean"]))[row - 1:row + 2, :].mean())
    if m == "composed_eaves_front_ratio":
        # the head band alone: the strip also holds the foot kinds (damp reaches 1.6 m), which are not under test here, so their masks are zero
        mk = dict(masks or {})
        mpp = dict(masks_ppm) if isinstance(masks_ppm, dict) else {}
        for kid in ("wall_foot_damp", "wall_foot_splash", "algae_downpipe", "salt_bloom", "wall_soot"):
            if kid not in mk:
                mk[kid] = np.zeros((int(1.6 * ppm) + 1, int(2.0 * ppm) + 1))
                mpp[kid] = ppm
        for kid in mk:
            if kid not in mpp:
                mpp[kid] = masks_ppm if (masks_ppm is not None and not isinstance(masks_ppm, dict)) else ppm
        r = compose_walls(tj, draw, seed, "cleaned", ppm, head=True, masks=mk, masks_ppm=mpp, head_strength=p.get("strength", 0.2), head_depth_scale=p.get("depth_m", 0.3) / 0.675)
        row = int(round(p.get("below_m", 0.3) * ppm))
        return float((_ylin(r["unfloored"]) / _ylin(r["clean"]))[row - 1:row + 2, :].mean())
    if m in ("channel_over_road", "fringe_over_road"):
        ed = draw.edges_by_kind(tj)
        k = tj["kinds"]["gutter_grime"]
        ext_mm = tuple(v * 1000 for v in k["mask"]["frame_extent_m"])
        if masks and "gutter_grime" in masks:
            gp = masks_ppm.get("gutter_grime", 500) if isinstance(masks_ppm, dict) else (500 if masks_ppm is None else masks_ppm)
            mk = np.asarray(masks["gutter_grime"], float)
            if abs(gp - 500) > 1e-6:
                mk = ndi.zoom(mk, 500.0 / gp, order=1)
        else:
            mk = draw.rasterize(draw.kind_envelope(tj, "gutter_grime", seed, 0), ext_mm, 500, ed.get("gutter_grime", 0.0), wrap="x")
        Hh = mk.shape[0]
        asp = _lin(tj["surfaces"]["asphalt_dry"]["albedo_srgb"])
        if m == "channel_over_road":
            sel = mk[Hh - 1 - int(0.23 * 500):Hh - int(0.06 * 500), :]
            alb = _darken(np.broadcast_to(_lin(tj["surfaces"]["channel_concrete"]["albedo_srgb"]), sel.shape + (3,)).copy(), sel, _ratio(tj, "gutter_grime", "channel_concrete"))
            return float(_ylin(alb).mean() / _ylin(asp))
        sel = mk[Hh - 1 - int(0.45 * 500):Hh - int(0.30 * 500), :]
        alb = _darken(np.broadcast_to(asp, sel.shape + (3,)).copy(), sel, _ratio(tj, "gutter_grime", "asphalt_dry"))
        return float(_ylin(alb).mean() / _ylin(asp))
    if m == "composed_ground_min_ratio":
        fl = tj["compose"]["ground"]["floor"]
        prod = 1.0
        for kid in ("pavement_stain", "gutter_grime"):
            prod *= tj["kinds"][kid]["tone"]["kerb_granite"]["albedo_mult_linear"]
        return float(max(prod, fl))
    raise ValueError(m)


def part_e_composition(tj, R, draw):
    out = {}
    for kid in tj["kinds_order"]:
        for c in tj["kinds"][kid]["checks"]:
            if c["measure"] not in COMPOSITION_MEASURES:
                continue
            vals = [composition(tj, draw, c, sd) for sd in (1990, 2024, 7)]
            med = float(np.median(vals))
            R.check("E %s %s (%s): median %.3f over 3 seeds (%.3f to %.3f), expected %s to %s" % (kid, c["name"], c["measure"], med, min(vals), max(vals), c["min"], c["max"]), c["min"] <= med <= c["max"])
            out[kid + "/" + c["name"]] = {"median": med, "expected": [c["min"], c["max"]]}
    # without the floor the stacked foot would be darker than the sheet's darkest: the floor is doing work
    r = compose_walls(tj, draw, 1990, "sooted", 100)
    raw_min = float((_ylin(r["unfloored"]) / _ylin(r["clean"])).min())
    R.check("E the floor does work: the stacked sooted foot would reach %.3f of the clean wall without it (floor %.2f)" % (raw_min, tj["compose"]["walls"]["floor"]), raw_min < tj["compose"]["walls"]["floor"])
    # the salt band stays pale whichever the order of marks in the (wrong) order: salt first then darkening makes it dark
    r2 = compose_walls(tj, draw, 1990, "cleaned", 100)
    Hp = r2["clean"].shape[0]
    sm = r2["masks"]["salt_bloom"] > 0.4
    sm[: Hp - int(0.52 * 100)] = False
    sm[Hp - int(0.30 * 100):] = False
    wrong = _lin(tj["surfaces"]["brick_red"]["albedo_srgb"])[None, None, :] * np.ones((Hp, r2["clean"].shape[1], 1))
    wrong = wrong * (1 - r2["masks"]["salt_bloom"][..., None]) + _lin(tj["kinds"]["salt_bloom"]["tone"]["brick_red"]["mark_srgb"])[None, None, :] * r2["masks"]["salt_bloom"][..., None]
    for kid in ("wall_foot_damp", "wall_foot_splash"):
        wrong = _darken(wrong, r2["masks"][kid], _ratio(tj, kid, "brick_red"))
    wr = float((_ylin(wrong) / _ylin(r2["clean"]))[sm].mean())
    rt = float((_ylin(r2["final"]) / _ylin(r2["clean"]))[sm].mean())
    R.check("E the order matters: salt laid AFTER the darkening reads %.2f of the clean wall at the whitened bricks, laid BEFORE it only %.2f" % (rt, wr), rt > wr * 1.5)
    # R2: the first pass's head band (full strength and full depth under an eaves gutter) is refused by composed_eaves_front_ratio
    ce = next(c for c in tj["kinds"]["wall_head_band"]["checks"] if c["name"] == "composed_eaves_front_ratio")
    wrong_e = dict(ce, params=dict(ce["params"], strength=1.0, depth_m=0.675))
    ve = float(np.median([composition(tj, draw, wrong_e, sd) for sd in (1990, 2024, 7)]))
    R.check("E the first pass's head band under an eaves gutter (strength 1, full depth) composes to %.2f of the wall at 0.3 m, outside %s to %s" % (ve, ce["min"], ce["max"]), not (ce["min"] <= ve <= ce["max"]))
    # the composition checks take the builder's own masks (the second review's narrow note): the target's masks passed back in give the target's values, a wrong builder mask is refused
    same = []
    for kid in tj["kinds_order"]:
        for c in tj["kinds"][kid]["checks"]:
            if c["measure"] in ("composed_foot_ratio", "composed_salt_ratio", "composed_soot_ratio", "composed_soot_chroma_ratio", "composed_eaves_front_ratio", "composed_head_ratio", "house_to_house_ratio"):
                head_ = c["measure"] in ("composed_head_ratio", "composed_eaves_front_ratio")
                rr = compose_walls(tj, draw, 1990, "cleaned", 100, head=True)
                mk = {"wall_head_band": rr["masks"]["wall_head_band"]} if c["measure"] == "composed_eaves_front_ratio" else {k_: v for k_, v in rr["masks"].items() if k_ != "wall_head_band" or head_}
                a_ = composition(tj, draw, c, 1990)
                b_ = composition(tj, draw, c, 1990, masks=mk, masks_ppm=100)
                same.append((c["name"], a_, b_))
    bad = [(n_, round(a_, 4), round(b_, 4)) for n_, a_, b_ in same if abs(a_ - b_) > 0.02]
    R.check("E composition checks run on the builder's own masks (masks argument): %d checks, the target's masks fed back give the same value within 0.02 (off: %s)" % (len(same), bad), not bad and len(same) >= 7)
    flat = {"wall_foot_splash": np.ones((75, 200)), "wall_foot_damp": np.ones((160, 200)), "algae_downpipe": np.ones((140, 90))}
    cf = next(c for c in tj["kinds"]["wall_foot_splash"]["checks"] if c["name"] == "composed_foot_ratio")
    vf = composition(tj, draw, cf, 1990, masks=flat, masks_ppm=100)
    R.check("E a builder's foot masks at 1.0 everywhere compose to %.2f of the clean wall at 0.1 m, outside %s to %s: the composition check refuses a wrong mask of the builder's" % (vf, cf["min"], cf["max"]), not (cf["min"] <= vf <= cf["max"]))
    cs = next(c for c in tj["kinds"]["wall_soot"]["checks"] if c["name"] == "composed_soot_chroma_ratio")
    vs = composition(tj, draw, cs, 1990, masks={"wall_soot": np.full((400, 400), 0.9)}, masks_ppm=100)
    R.check("E the soot chroma ratio on a builder's uniform mask %.2f stays in %s to %s (the mask changes the brightness, the colour mark keeps the grey)" % (vs, cs["min"], cs["max"]), cs["min"] <= vs <= cs["max"])
    return out


def wrong_masks(tj, draw):
    """Masks made deliberately wrong, one or more per kind: each one is what a lazy generator would make."""
    out = []
    ed = draw.edges_by_kind(tj)

    def frame(kid):
        k = tj["kinds"][kid]
        ppm = ppm_for(k)
        ext = k["mask"]["frame_extent_m"]
        H, W = int(round((ext[3] - ext[1]) * ppm)), int(round((ext[2] - ext[0]) * ppm))
        return k, ppm, ext, H, W

    def gradient(kid, from_top=False):
        k, ppm, ext, H, W = frame(kid)
        lv = k["envelope"]["levels"]
        hs = [0.0] + [l["h_m"] for l in lv]
        ls = [lv[0]["level"] if lv[0]["h_m"] > 0 else 0.0] + [l["level"] for l in lv]
        h = (np.arange(H) / ppm) if from_top else ((H - 1 - np.arange(H)) / ppm)
        col = np.interp(h, hs, ls)
        return np.repeat(col[:, None], W, axis=1).astype(float), ppm

    for kid in ("wall_foot_splash", "wall_foot_damp", "gutter_grime"):
        m, ppm = gradient(kid)
        out.append((kid, "a perfectly straight, uniform gradient with no ragged top", m, ppm))
    m, ppm = gradient("wall_head_band", from_top=True)
    out.append(("wall_head_band", "a perfectly straight, uniform gradient from the feature", m, ppm))
    # two identical symmetric bars
    k, ppm, ext, H, W = frame("streak_sill")
    m = np.zeros((H, W))
    for xc in (-0.35, 0.35):
        x0 = int(round((xc - 0.04 - ext[0]) * ppm))
        L = int(round(0.4 * ppm))
        for r in range(L):
            m[r, x0:x0 + int(0.08 * ppm)] = 0.9 * (1 - r / L)
    out.append(("streak_sill", "two identical, symmetric bars and nothing else", m, ppm))
    # identical fingers, identical spacing
    k, ppm, ext, H, W = frame("streak_coping")
    m = np.zeros((H, W))
    for xc in np.arange(-2.8, 2.81, 0.4):
        x0 = int(round((xc - 0.05 - ext[0]) * ppm))
        m[: int(0.6 * ppm), x0:x0 + int(0.1 * ppm)] = 0.85
    out.append(("streak_coping", "identical fingers at an identical 0.4 m spacing", m, ppm))
    # gridded identical discs
    for kid, nside, dmm in (("gum", 3, 20), ("cig_end", 4, 10)):
        k, ppm, ext, H, W = frame(kid)
        yy, xx = np.mgrid[0:H, 0:W]
        m = np.zeros((H, W))
        for i in range(nside):
            for j in range(nside):
                cy, cx = (i + 0.5) * H / nside, (j + 0.5) * W / nside
                m[((yy - cy) ** 2 + (xx - cx) ** 2) <= (dmm / 2000.0 * ppm) ** 2] = 1.0
        out.append((kid, "a %d x %d grid of identical discs" % (nside, nside), m, ppm))
    # lattice of identical dots
    k, ppm, ext, H, W = frame("road_oil")
    yy, xx = np.mgrid[0:H, 0:W]
    m = np.zeros((H, W))
    step = 0.075
    for cy in np.arange(H / 2 - 0.15 * ppm, H / 2 + 0.15 * ppm + 1, step * ppm):
        for cx in np.arange(0.5 * ppm, W - 0.5 * ppm, step * ppm):
            m[((yy - cy) ** 2 + (xx - cx) ** 2) <= (0.0085 * ppm) ** 2] = 1.0
    out.append(("road_oil", "a lattice of identical dots", m, ppm))
    # one plain stripe of salt
    k, ppm, ext, H, W = frame("salt_bloom")
    m = np.zeros((H, W))
    r1 = H - 1 - int(0.35 * ppm)
    m[r1 - int(0.09 * ppm):r1, :] = 0.6
    out.append(("salt_bloom", "one uniform 0.09 m stripe", m, ppm))
    # white noise at texel scale
    k, ppm, ext, H, W = frame("paint_fade")
    out.append(("paint_fade", "white noise at texel scale", np.random.default_rng(3).uniform(0.2, 0.8, (H, W)), ppm))
    # a flat soot
    k, ppm, ext, H, W = frame("wall_soot")
    out.append(("wall_soot", "a perfectly uniform mask", np.full((H, W), 0.9), ppm))

    # ---- the second review's six wrong masks (R3), each of which passed every check of the second pass; the check that must refuse each one is named
    # 1. the straight profile multiplied by a smooth vertical cosine: a band in vertical stripes with no course steps
    def stripes(kid, from_top, period, amp, normalised):
        m, ppm_ = gradient(kid, from_top)
        x = np.arange(m.shape[1]) / ppm_
        mod = 1.0 + amp * np.cos(2 * np.pi * x / period)
        if normalised:
            mod = mod / (1.0 + amp)
        return np.clip(m * mod[None, :], 0.0, 1.0), ppm_
    for kid, from_top in (("wall_foot_splash", False), ("wall_foot_damp", False), ("wall_head_band", True), ("gutter_grime", False)):
        for period, amp, norm in ((0.25, 0.25, True), (0.40, 0.20, False), (0.50, 0.15, True)):
            m, ppm_ = stripes(kid, from_top, period, amp, norm)
            out.append((kid, "the straight profile times a vertical cosine (period %.2f m, +/-%d %%%s): a band in vertical stripes" % (period, int(amp * 100), ", clipped at 1" if not norm else ", scaled to peak 1"), m, ppm_, "core_column_cv"))
    # 2. a perfect checkerboard of salt bricks, every other brick in two courses, blurred 3 to 4 px
    k, ppm, ext, H, W = frame("salt_bloom")
    for sig in (3.0, 4.0):
        m = np.zeros((H, W))
        for course in (4, 5):                                       # the courses 0.30 to 0.45 m, the zone the check reads
            y0 = H - int(round((course + 1) * 0.075 * ppm)); y1 = H - int(round(course * 0.075 * ppm))
            off = (course % 2) * 0.1075
            for i in range(-1, int(W / ppm / 0.215) + 2):
                if (i + course) % 2 == 0:
                    x0 = int(round((off + i * 0.215) * ppm)); x1 = int(round((off + (i + 1) * 0.215) * ppm))
                    m[y0:y1, max(x0, 0):max(min(x1, W), 0)] = 0.6
        out.append(("salt_bloom", "a perfect checkerboard of whitened bricks in two courses, blurred %d px" % sig, ndi.gaussian_filter(m, sig), ppm, "brick_neighbour_same_share"))
    # 3. unequal end streaks plus four identical, evenly spaced, ruler-straight rivulets
    k, ppm, ext, H, W = frame("streak_sill")
    m = np.zeros((H, W))
    def bar(xc, wid, ln, lvl):
        x0 = int(round((xc - wid / 2 - ext[0]) * ppm)); x1 = max(int(round((xc + wid / 2 - ext[0]) * ppm)), x0 + 1); L = int(round(ln * ppm))
        for r in range(min(L, H)):
            m[r, x0:x1] = lvl * (1 - 0.8 * r / L)
    bar(-0.65, 0.045, 0.50, 0.9); bar(0.65, 0.030, 0.34, 0.8)
    for xc in (-0.30, -0.10, 0.10, 0.30):
        bar(xc, 0.014, 0.25, 0.7)
    out.append(("streak_sill", "unequal end streaks and four identical, evenly spaced, ruler-straight rivulets", ndi.gaussian_filter(m, 0.6), ppm, "rivulet_spacing_cv"))
    # 4. a correct 0.5 to 2 m mottle with no darker lower wall
    k, ppm, ext, H, W = frame("wall_soot")
    rg = np.random.default_rng(11)
    mot = ndi.gaussian_filter(rg.normal(size=(H, W)), 0.22 * ppm, mode="wrap")
    m = np.clip(0.90 + 0.07 * mot / mot.std(), 0.0, 1.0)
    out.append(("wall_soot", "a 0.5 to 2 m mottle (std 0.07 around 0.90) with no darker lower wall", m, ppm, "lower_wall_excess"))
    # 5. rust patches spread evenly up the pipe, none at the shoe (and a second one spread over the whole pipe)
    k, ppm, ext, H, W = frame("iron_wear")
    for lo, what in ((0.35, "none below 0.35 m"), (0.0, "spread evenly over the whole pipe")):
        rg = np.random.default_rng(5)
        yy, xx = np.mgrid[0:H, 0:W]
        m = np.zeros((H, W))
        cover = 0.0
        while cover < 0.06:
            e = float(np.clip(rg.lognormal(np.log(0.045), 0.45), 0.02, 0.11))
            cy = (H - 1) - rg.uniform(lo, 2.4) * ppm
            cx = rg.uniform(0, W)
            m[((yy - cy) ** 2 + (xx - cx) ** 2) <= (e / 2 * ppm) ** 2] = 1.0
            cover = float(m.mean())
        out.append(("iron_wear", "rust patches %s" % what, m, ppm, "coverage_share_below_m"))
    # 6. lichen as one flat block over half the top
    k, ppm, ext, H, W = frame("stone_top_lichen")
    m = np.zeros((H, W)); m[:, : W // 2] = 1.0
    out.append(("stone_top_lichen", "one flat block over half the top", ndi.gaussian_filter(m, 1.5), ppm, "blob_eqd_mm_p50"))
    return out


def part_e_wrong(tj, R, draw):
    log = {}
    for item in wrong_masks(tj, draw):
        kid, what, mask, ppm = item[:4]
        must = item[4] if len(item) > 4 else None
        fails = []
        for c in tj["kinds"][kid]["checks"]:
            if c.get("applies_to") != "mask":
                continue
            try:
                v, ok = run_mask_check(c, mask, ppm)
            except Exception as e:      # a mask the measure cannot read is refused too
                v, ok = float("nan"), False
            if not ok:
                fails.append("%s=%.3g" % (c["name"], v))
        names = [f.split("=")[0] for f in fails]
        R.check("E wrong mask refused: %s, %s: %d check(s) fail (%s)%s" % (kid, what, len(fails), ", ".join(fails[:4]), (", by the new check " + must) if must else ""),
                len(fails) >= 1 and (must is None or must in names))
        log.setdefault(kid, []).append({"what": what, "refused_by": fails})
    return log


# ---------------------------------------------------------------- F: placement
def _group(pl, kinds):
    return [q for q in pl if q["kind"] in kinds]


def rule_P1(pl, tj):
    sel = _group(pl, ("streak_sill", "streak_coping"))
    bad = [q for q in sel if abs(q["y_m"] - q["anchor_y_m"]) > 0.03 or abs(q["x_m"] - q["anchor_x_m"]) > q.get("anchor_half_width_m", 0.6) or abs(q.get("roll_deg", 0)) > 3.0]
    return not bad, "%d of %d streak decals off their sill or feature edge by more than 0.03 m or rolled by more than 3 degrees" % (len(bad), len(sel))


def rule_P2(pl, tj):
    sel = _group(pl, ("wall_foot_splash", "wall_foot_damp", "salt_bloom", "gutter_grime"))
    bad = [q for q in sel if abs(q["y_m"]) > 0.02]
    return not bad, "%d of %d L0 bands not at the pavement line (kerb foot) within 0.02 m" % (len(bad), len(sel))


def rule_P3(pl, tj):
    sel = _group(pl, ("road_oil",))
    bad = [q for q in sel if not (0.9 <= q["dist_from_kerb_m"] <= 1.6) or abs(q["axis_deg"]) > 10]
    return not bad, "%d of %d oil bands more than the allowed distance 0.9 to 1.6 m from the kerb or more than 10 degrees off its axis" % (len(bad), len(sel))


def rule_P4(pl, tj):
    sel = _group(pl, ("gum",))
    bad = [q for q in sel if q["on_carriageway"] or q["wall_dist_m"] < 0.4]
    return not bad, "%d of %d gum stamps on the carriageway or within 0.4 m of a wall" % (len(bad), len(sel))


def rule_P5(pl, tj):
    bad = []
    for kid in sorted({q["kind"] for q in pl}):
        sel = [q for q in pl if q["kind"] == kid and q.get("in_hook_frame")]
        if len(sel) >= 5:
            cnt = np.bincount([q["variant"] for q in sel])
            if cnt.max() / len(sel) > 0.40:
                bad.append((kid, round(float(cnt.max() / len(sel)), 2)))
    return not bad, "kinds with one variant over 40 %% of their decals in the hook frame: %s" % bad


def rule_P6(pl, tj):
    bad = 0
    for kid in sorted({q["kind"] for q in pl}):
        for wall in sorted({q.get("wall") for q in pl if q["kind"] == kid}):
            sel = sorted([q for q in pl if q["kind"] == kid and q.get("wall") == wall], key=lambda q: q["x_m"])
            for i in range(len(sel)):
                for j in range(i + 1, len(sel)):
                    if sel[j]["x_m"] - sel[i]["x_m"] >= 6.0:
                        break
                    if sel[i]["variant"] == sel[j]["variant"] and sel[i]["seed"] == sel[j]["seed"]:
                        bad += 1
    return bad == 0, "%d pairs with the same variant and seed within 6 m along one wall" % bad


def rule_P7(pl, tj):
    tiles = {"wall_foot_splash": 2.0, "wall_foot_damp": 2.0, "wall_soot": 4.0, "wall_head_band": 2.0}
    bad = 0
    for kid, T_ in tiles.items():
        sel = sorted([q for q in pl if q["kind"] == kid and q.get("house") is not None], key=lambda q: (q["side"], q["x_m"]))
        for a, b in zip(sel[:-1], sel[1:]):
            if a["side"] == b["side"] and abs(((a["tile_phase_m"] - b["tile_phase_m"]) + T_ / 2) % T_ - T_ / 2) < 0.1:
                bad += 1
    return bad == 0, "%d neighbouring houses whose tiled L0 kinds start in the same x phase (within 0.1 m)" % bad


def rule_P8(pl, tj):
    places = tj["places"]["standing_places"]["places"]
    sel = _group(pl, ("road_oil", "road_blot"))
    bad = [q for q in sel if not any(r["side"] == q["side"] and r["x_m"][0] <= q["x_m"] <= r["x_m"][1] for r in places)]
    return not bad, "%d of %d oil bands and blots outside the declared standing places" % (len(bad), len(sel))


def rule_P9(pl, tj):
    sel = [q for q in _group(pl, ("gum", "cig_end")) if q.get("tier") == "bus stop"]
    return not sel, "%d gum or end stamps at a bus stop (there is none: zero)" % len(sel)


def rule_P10(pl, tj):
    sel = _group(pl, ("wall_head_band",))
    bad = []
    for q in sel:
        f = q.get("feature")
        if f == "eaves_gutter":
            ok = q["strength"] <= 0.2 + 1e-9 and q["depth_m"] <= 0.3 + 1e-9
        elif f in ("gable_verge", "barge"):
            ok = abs(q["strength"] - 1.0) < 1e-9 if q.get("quay_facing") else 0.3 - 1e-9 <= q["strength"] <= 1.0 + 1e-9
        elif f in ("coping", "string_course"):
            ok = q["strength"] <= 1.0 + 1e-9 and abs(q.get("depth_scale", 0) - 0.3) < 1e-9
        else:
            ok = False
        if not ok:
            bad.append(q)
    gables = tj["places"]["quay_gables"]["gables"]
    missing = [g["house"] for g in gables if not any(q.get("feature") in ("gable_verge", "barge") and q.get("wall") == g["house"] and q.get("face") == "gable" and q.get("quay_facing") and abs(q["strength"] - 1.0) < 1e-9 for q in sel)]
    return not bad and not missing, "%d of %d head bands off their rule (eaves gutter: strength 0 to 0.2 and depth 0.1 to 0.3 m; gable verge or barge: 1.0 on a quay-facing gable, 0.3 to 1.0 elsewhere; coping: depth scale 0.3); quay gables without a full-strength verge band: %s" % (len(bad), len(sel), missing)


def rule_P11(pl, tj):
    st = {h["id"]: h["state"] for h in tj["houses"]["list"]}
    sel = _group(pl, ("wall_soot",))
    bad = [q["wall"] for q in sel if q.get("house_state") != st.get(q["wall"])]
    sooted = [q for q in sel if q.get("house_state") == "sooted"]
    near = [q["wall"] for q in sooted if q["wall"].startswith(("east_parade", "west_south"))]
    over = len(sooted) > 0.3 * max(len(sel), 1)
    return not bad and not near and not over, "%d of %d wall_soot decals whose house state is not the one in target.json `houses` (%s); sooted on a parade or west_south house: %s; sooted share %.2f (at most 0.30)" % (len(bad), len(sel), bad[:3], near, len(sooted) / max(len(sel), 1))


PLACEMENT_RULES = {"P1": rule_P1, "P2": rule_P2, "P3": rule_P3, "P4": rule_P4, "P5": rule_P5, "P6": rule_P6, "P7": rule_P7, "P8": rule_P8, "P9": rule_P9, "P10": rule_P10, "P11": rule_P11}


def check_placement(pl, tj):
    """Run the placement checks of target.json on a list of placed decals: dicts with kind, variant, seed, x_m (along the street), y_m (height of the decal's origin above the pavement, or
    distance from the kerb foot for gutter_grime), anchor_x_m, anchor_y_m, anchor_half_width_m, roll_deg, dist_from_kerb_m, axis_deg (to the kerb), on_carriageway, wall_dist_m, wall, side,
    house, tile_phase_m, in_hook_frame, tier. Returns [(id, ok, detail)]."""
    return [(c["id"], ) + PLACEMENT_RULES[c["id"]](pl, tj) for c in tj["placement_checks"]]


def sample_street(tj, seed=1):
    """A conforming placed street built from the rules (x 3 to 45): sills, copings, L0 bands per house, oil at the standing places, gum on the footway."""
    rng = np.random.default_rng(seed)
    pl = []
    houses = [("east_parade_bay%d" % i, "east", 3.0 + 6 * i) for i in range(6)] + [("east_chandler_bay0", "east", 40.0)] + [("west_south_bay%d" % i, "west", 3.0 + 6 * i) for i in range(3)] + [("west_north_bay%d" % i, "west", 24.0 + 6 * i) for i in range(3)]
    state_of = {h["id"]: h["state"] for h in tj["houses"]["list"]}
    quay = {g["house"] for g in tj["places"]["quay_gables"]["gables"]}
    n = 0
    for hi, (name, side, x0) in enumerate(houses):
        for kid, T_ in (("wall_foot_splash", 2.0), ("wall_foot_damp", 2.0), ("wall_soot", 4.0), ("wall_head_band", 2.0)):
            q = {"kind": kid, "variant": hi % 4, "seed": n, "x_m": x0, "y_m": 0.0 if kid != "wall_head_band" else 6.2, "wall": name, "side": side, "house": hi, "tile_phase_m": (hi * 0.37 + 0.11 * len(kid)) % T_, "in_hook_frame": True}
            if kid == "wall_soot":
                q["house_state"] = state_of[name]
            if kid == "wall_head_band":                                    # under the eaves gutter of the front: almost nothing
                q.update(feature="eaves_gutter", strength=round(float(rng.uniform(0.0, 0.2)), 3), depth_m=round(float(rng.uniform(0.1, 0.3)), 3))
            pl.append(q)
            n += 1
        if name in quay or name == "east_chandler_bay0":                   # a gable verge: full strength on the quay-facing gables, 0.3 to 1.0 on another
            qg = name in quay
            pl.append({"kind": "wall_head_band", "variant": (hi + 1) % 4, "seed": n, "x_m": x0, "y_m": 6.2, "wall": name, "face": "gable", "side": side, "house": hi, "tile_phase_m": (hi * 0.37 + 0.9) % 2.0, "in_hook_frame": qg,
                       "feature": "gable_verge", "quay_facing": qg, "strength": 1.0 if qg else round(float(rng.uniform(0.3, 1.0)), 3), "depth_m": 1.15})
            n += 1
        for sx in (x0 + 1.5, x0 + 4.5):
            if rng.uniform() < 0.5:
                v = int(rng.integers(0, 6))
                pl.append({"kind": "streak_sill", "variant": v, "seed": n, "x_m": sx, "y_m": 3.2, "anchor_x_m": sx + rng.uniform(-0.1, 0.1), "anchor_y_m": 3.2 + rng.uniform(-0.02, 0.02), "anchor_half_width_m": 0.6, "roll_deg": rng.uniform(-1, 1), "wall": name, "side": side, "in_hook_frame": hi < 3})
                n += 1
        pl.append({"kind": "streak_coping", "variant": int(rng.integers(0, 5)), "seed": n, "x_m": x0 + 3.0, "y_m": 6.4, "anchor_x_m": x0 + 3.0, "anchor_y_m": 6.4, "anchor_half_width_m": 3.0, "roll_deg": 0.0, "wall": name, "side": side, "in_hook_frame": hi < 3})
        n += 1
    for a, b in tj["places"]["standing_places"]["sample_oil_x_m"]:
        pl.append({"kind": "road_oil", "variant": n % 5, "seed": n, "x_m": a, "y_m": 0.0, "dist_from_kerb_m": rng.uniform(1.0, 1.5), "axis_deg": rng.uniform(-5, 5), "wall": "road", "side": "east", "in_hook_frame": True})
        n += 1
    for _ in range(14):
        pl.append({"kind": "gum", "variant": int(rng.integers(0, 8)), "seed": n, "x_m": rng.uniform(3, 45), "y_m": 0.0, "on_carriageway": False, "wall_dist_m": rng.uniform(0.5, 1.9), "wall": "east_footway", "side": "east", "in_hook_frame": True, "tier": "open footway"})
        n += 1
    return pl


def part_f(tj, R):
    base = sample_street(tj)
    res = check_placement(base, tj)
    for i, ok, det in res:
        R.check("F %s on the conforming placed street: %s" % (i, det), ok)
    # deliberately wrong placements, each of which must be refused by exactly its rule
    import copy as _copy
    def mutate(f):
        pl = _copy.deepcopy(base)
        f(pl)
        return pl
    def first(pl, kid):
        return next(q for q in pl if q["kind"] == kid)
    wrong = {
        "P1": ("a sill streak 0.10 m below its sill", lambda pl: first(pl, "streak_sill").update(y_m=first(pl, "streak_sill")["anchor_y_m"] - 0.10)),
        "P1b": ("a coping streak rolled 12 degrees", lambda pl: first(pl, "streak_coping").update(roll_deg=12.0)),
        "P2": ("a foot band hung 0.15 m above the pavement", lambda pl: first(pl, "wall_foot_splash").update(y_m=0.15)),
        "P3": ("an oil band 0.3 m from the kerb", lambda pl: first(pl, "road_oil").update(dist_from_kerb_m=0.3)),
        "P3b": ("an oil band at 40 degrees to the kerb", lambda pl: first(pl, "road_oil").update(axis_deg=40.0)),
        "P4": ("gum on the carriageway", lambda pl: first(pl, "gum").update(on_carriageway=True)),
        "P4b": ("gum 0.1 m from a wall", lambda pl: first(pl, "gum").update(wall_dist_m=0.1)),
        "P5": ("one gum variant on every stamp", lambda pl: [q.update(variant=2) for q in pl if q["kind"] == "gum"]),
        "P6": ("the same sill-streak variant and seed twice within 6 m", lambda pl: (lambda a, b: b.update(variant=a["variant"], seed=a["seed"], wall=a["wall"], x_m=a["x_m"] + 3.0, anchor_x_m=a["x_m"] + 3.0, anchor_y_m=b["y_m"]))(*[q for q in pl if q["kind"] == "streak_sill"][:2])),
        "P7": ("two neighbouring houses with the same tile phase", lambda pl: [q.update(tile_phase_m=0.5) for q in pl if q["kind"] == "wall_foot_splash"]),
        "P8": ("an oil band in the yard entrance (west, x 22.5), which is no standing place", lambda pl: first(pl, "road_oil").update(x_m=22.5, side="west")),
        "P9": ("gum at a bus stop", lambda pl: first(pl, "gum").update(tier="bus stop")),
        "P10": ("the first pass's head band: full strength and full depth under an eaves gutter", lambda pl: next(q for q in pl if q["kind"] == "wall_head_band" and q.get("feature") == "eaves_gutter").update(strength=1.0, depth_m=1.15)),
        "P10b": ("a quay-facing gable verge at weight 0.5", lambda pl: next(q for q in pl if q["kind"] == "wall_head_band" and q.get("quay_facing")).update(strength=0.5)),
        "P11": ("a parade bay sooted by the recipe's random brick set", lambda pl: [q.update(house_state="sooted") for q in pl if q["kind"] == "wall_soot" and q["wall"] == "east_parade_bay3"]),
        "P11b": ("a house whose state is not the one in `houses`", lambda pl: [q.update(house_state="cleaned") for q in pl if q["kind"] == "wall_soot" and q["wall"] == "west_south_bay1"]),
    }
    for key, (what, f) in wrong.items():
        rid = key[:-1] if key.endswith("b") else key
        r = {i: ok for i, ok, _ in check_placement(mutate(f), tj)}
        R.check("F wrong placement refused by %s: %s" % (rid, what), r[rid] is False and all(v for kk, v in r.items() if kk != rid))
    return {"conforming": [(i, ok) for i, ok, _ in res]}


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
    comp = part_e_composition(tj, R, draw)
    wlog = part_e_wrong(tj, R, draw)
    plog = part_f(tj, R)
    for ln in R.lines:
        if ln.startswith("FAIL") or ln.startswith("note") or ("--verbose" in argv and (" E " in ln[:8] or " F " in ln[:8] or ln[5:7] in ("E ", "F "))):
            print(ln[:600])
    line = "self_check: passed=%d/%d failed=%d (A structure, B tone, C photographs, D envelopes, E composition and wrong masks, F placement; %d kinds)" % (R.ok, R.ok + R.fail, R.fail, len(tj["kinds_order"]))
    print(line)
    if write:
        tj["self_check"] = {"date": datetime.date.today().isoformat(), "result": line, "passed": R.ok, "failed": R.fail, "overlays_written": olog,
                            "failures": [l for l in R.lines if l.startswith("FAIL")], "envelope_summary": summary, "composition": comp, "wrong_masks_refused": wlog, "placement": plog}
        json.dump(tj, open(TARGET, "w"), indent=1)
    return 1 if R.fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
