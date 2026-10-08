#!/usr/bin/env python
"""Draws Quay Street's wear target from target.json alone.

    /home/user/.bpyenv/bin/python target_drawing.py OUT_DIR [--target path/to/target.json] [--seed 1990]

Writes into OUT_DIR (pictures never go into git outside production/previews/):
  wear_envelopes.json     every scene and every kind's shape envelope as filled polygons in MILLIMETRES
                          (x to the right; y UP on walls, y FORWARD on the ground; each polygon has a kind, a level 0..1
                          (the mask value at full effect) and a role)
  scene_*.png             reference sheets at real scale: a 2 m wall bay, a 1 m2 pavement, a 3 x 2 m road, paint, render, flags, foot profiles
  kind_*.png              one sheet per kind: its envelope, its blurred mask (the edge softness the target states) and a scale bar
Seeded: the same target.json and seed give the same polygons.
"""
import json
import math
import os
import sys
import zlib

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ small helpers
def rng_for(seed, tag):
    return np.random.default_rng(zlib.crc32(("%s/%s" % (seed, tag)).encode()) & 0xFFFFFFFF)


def uni(rng, lohi):
    lo, hi = lohi
    return float(rng.uniform(lo, hi))


def uni_int(rng, lohi):
    lo, hi = lohi
    return int(rng.integers(int(lo), int(hi) + 1))


def lognormal3(rng, p10, p50, p90, n=1):
    """samples with the given 10th, 50th and 90th percentiles (a log-normal through them)"""
    sg = math.log(max(p90, 1e-9) / max(p10, 1e-9)) / (2 * 1.2816)
    return np.exp(math.log(max(p50, 1e-9)) + sg * rng.standard_normal(n))


def smooth_noise_1d(rng, n, wl_pts, periodic=False):
    """value noise, n samples, wavelength wl_pts samples; zero mean, about +/-1. periodic=True: sample n-1 is followed by sample 0 (seamless tile)."""
    if periodic:
        k = max(3, int(round(n / max(wl_pts, 1.0))))
        g = rng.uniform(-1, 1, k)
        x = np.arange(n) / float(n) * k
        i = np.floor(x).astype(int) % k
        f = x - np.floor(x)
        f = f * f * (3 - 2 * f)
        return g[i] * (1 - f) + g[(i + 1) % k] * f
    k = max(3, int(n / max(wl_pts, 1.0)) + 3)
    g = rng.uniform(-1, 1, k)
    x = np.linspace(0, k - 3, n)
    i = np.floor(x).astype(int)
    f = x - i
    f = f * f * (3 - 2 * f)
    return g[i] * (1 - f) + g[i + 1] * f


def poly(kind, level, pts_mm, role, length_mm=None):
    d = {"kind": kind, "level": round(float(level), 3), "role": role, "poly": [[round(float(x), 1), round(float(y), 1)] for x, y in pts_mm]}
    if length_mm is not None:
        d["length_mm"] = round(float(length_mm), 1)
    return d


def path_length(path):
    p = np.asarray(path, float)
    return float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())


def circle(cx, cy, r, n=14):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def blob(rng, cx, cy, eqd, aspect, angle, n=22, rough=0.22):
    """irregular closed blob with the given equivalent diameter (area-true), aspect and angle (radians)"""
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    noise = np.zeros(n)
    for k, amp in ((2, 0.5), (3, 0.35), (5, 0.2)):
        noise += amp * np.cos(k * th + rng.uniform(0, 2 * math.pi))
    r = 1.0 + rough * noise / 1.05
    a = math.sqrt(aspect)
    xs = r * np.cos(th) * a
    ys = r * np.sin(th) / a
    area = 0.5 * abs(np.dot(xs, np.roll(ys, -1)) - np.dot(ys, np.roll(xs, -1)))
    s = (eqd / 2.0) / math.sqrt(area / math.pi)
    xs, ys = xs * s, ys * s
    c, sn = math.cos(angle), math.sin(angle)
    return [(cx + c * x - sn * y, cy + sn * x + c * y) for x, y in zip(xs, ys)]


def ribbon(path, widths):
    """polygon around a polyline with per-point width (same units)"""
    path = np.asarray(path, float)
    d = np.gradient(path, axis=0)
    ln = np.linalg.norm(d, axis=1)[:, None]
    ln[ln == 0] = 1
    nrm = np.stack([-d[:, 1], d[:, 0]], 1) / ln
    left = path + nrm * (np.asarray(widths)[:, None] / 2)
    right = path - nrm * (np.asarray(widths)[:, None] / 2)
    return [tuple(p) for p in np.vstack([left, right[::-1]])]


# ------------------------------------------------------------------ primitives (millimetres)
def streak(rng, kind, x0, y0, w0, length, wander, taper, fade_exp, core, head_frac, tilt_deg=0.0, slices=14, role="streak", floor=0.04):
    """A run falling from (x0,y0) downward: width w0 tapering by `taper`, centre line wandering, mask = core up to head_frac of the length
    then exp(-(s)^fade_exp) so it is darkest at the head. Returns slice polygons."""
    n = slices * 3
    t = np.linspace(0, 1, n)
    wn = smooth_noise_1d(rng, n, n / 3.0)
    cx = x0 + wander * wn + math.tan(math.radians(tilt_deg)) * (-length * t)
    cy = y0 - length * t
    w = w0 * (1 - taper * t ** 1.2) * (1 + 0.15 * smooth_noise_1d(rng, n, n / 5.0))
    w = np.maximum(w, 0.25 * w0)
    k = (-math.log(floor)) ** (1.0 / fade_exp)
    out = []
    edges = np.linspace(0, n - 1, slices + 1).astype(int)
    for a, b in zip(edges[:-1], edges[1:]):
        tm = 0.5 * (t[a] + t[b])
        s = max(0.0, (tm - head_frac) / max(1e-6, 1 - head_frac)) * k
        lv = core * (1.0 if tm <= head_frac else math.exp(-(s ** fade_exp)))
        seg = np.stack([cx[a:b + 1], cy[a:b + 1]], 1)
        out.append(poly(kind, lv, ribbon(seg, w[a:b + 1]), role, path_length(seg)))
    return out


def foot_band_polys(rng, kind, E, length_mm, seed_tag):
    """Horizontal band rising from y=0: piecewise-linear level profile, ragged top stepped by brick courses, upward fingers, brick patches (salt)."""
    lv = [(0.0, E["levels"][0]["level"] if E["levels"][0]["h_m"] > 0.0 else 0.0)] + [(l["h_m"] * 1000.0, l["level"]) for l in E["levels"]]
    # the profile starts at the first stated level at h=0 unless the first stated height is a delayed start (salt bloom: level 0 at its own first height)
    if E["levels"][0]["level"] == 0.0:
        lv = [(l["h_m"] * 1000.0, l["level"]) for l in E["levels"]]
    top = E.get("top_edge", {})
    step = top.get("step_m", 0.0) * 1000.0
    amp = uni(rng, top.get("amplitude_m", [0.0, 0.0])) * 1000.0
    wl = uni(rng, top.get("wavelength_m", [0.3, 0.6])) * 1000.0
    nx = int(length_mm / 40.0) + 1
    xs = np.linspace(0, length_mm, nx)
    nz = np.append(smooth_noise_1d(rng, nx - 1, wl / (length_mm / (nx - 1)), periodic=True), 0.0)
    nz[-1] = nz[0]
    nz = amp * (nz / max(1e-6, np.abs(nz).max()))
    if step > 0:
        nz = np.round(nz / step) * step
    htop = lv[-1][0]
    out = []
    sub = 3
    prof = []
    for (h0, l0), (h1, l1) in zip(lv[:-1], lv[1:]):
        for j in range(sub):
            ha = h0 + (h1 - h0) * j / sub
            hb = h0 + (h1 - h0) * (j + 1) / sub
            la = l0 + (l1 - l0) * (j + 0.5) / sub
            prof.append((ha, hb, la))
    patches = E.get("brick_patches")
    for ha, hb, la in prof:
        if la <= 0.005:
            continue
        sa = 1.0 if ha == 0 else ha / htop
        sb = hb / htop
        lower = [(x, ha + sa * n) for x, n in zip(xs, nz)]
        upper = [(x, hb + sb * n) for x, n in zip(xs, nz)]
        lower = [(x, max(0.0, y)) for x, y in lower]
        upper = [(x, max(0.0, y)) for x, y in upper]
        if patches:
            bw, bh = patches["brick_m"][0] * 1000.0, patches["brick_m"][1] * 1000.0
            course = int(max(ha, 0) // bh)
            while course * bh < hb:
                y0, y1 = max(ha, course * bh), min(hb, (course + 1) * bh)
                if y1 - y0 > 6:
                    off = (course % 2) * bw / 2
                    xx = -off
                    while xx < length_mm:
                        if rng.uniform() < patches["fill_fraction"]:
                            a, b = max(xx, 0), min(xx + bw - 10, length_mm)
                            idx = min(nx - 1, max(0, int(a / length_mm * (nx - 1))))
                            ytop_ok = y1 <= hb + sb * nz[idx]
                            if b > a and ytop_ok:
                                out.append(poly(kind, la * uni(rng, [0.8, 1.0]), [(a, y0), (b, y0), (b, y1), (a, y1)], "brick_patch"))
                        xx += bw
                course += 1
        else:
            out.append(poly(kind, la, lower + upper[::-1], "band"))
    fg = E.get("fingers")
    if fg:
        nf = int(fg["n_per_m"] * length_mm / 1000.0)
        for _ in range(nf):
            x = rng.uniform(0, length_mm)
            idx = min(nx - 1, int(x / length_mm * (nx - 1)))
            yb = htop * 0.5 + nz[idx]
            L = uni(rng, [v * 1000.0 for v in fg["length_m"]])
            w = uni(rng, [v * 1000.0 for v in fg["width_m"]])
            out.append(poly(kind, 0.4, [(x - w / 2, yb), (x + w / 2, yb), (x + w * 0.2, yb + L), (x - w * 0.2, yb + L)], "finger"))
    return out


def streak_set_polys(rng, kind, E, tags):
    """streak_sill, streak_coping and rust_bleed: y=0 at the source, runs fall to negative y."""
    out = []
    wander = lambda: uni(rng, [v * 1000.0 for v in E.get("wander_m", [0.005, 0.02])])
    common = dict(taper=E.get("taper", 0.5), fade_exp=E.get("fade_exponent", 1.2), core=E.get("core_level", 0.9), head_frac=E.get("head_fraction_full", 0.15))
    if "sill_width_m" in E:
        S = uni(rng, [v * 1000.0 for v in E["sill_width_m"]])
        es = E["end_streaks"]
        out.append(poly(kind, 0.0, [(-S / 2, 0), (S / 2, 0), (S / 2, -1), (-S / 2, -1)], "sill_edge"))  # level-0 marker of the source line
        ws = E["wash"]
        wh = uni(rng, [v * 1000.0 for v in ws["height_m"]])
        ov = ws["overhang_m"] * 1000.0
        out.append(poly(kind, ws["level"], [(-S / 2 - ov, 0), (S / 2 + ov, 0), (S / 2 + ov * 0.6, -wh), (-S / 2 - ov * 0.6, -wh)], "wash"))
        for side in (-1, 1):
            w = uni(rng, es["width_frac_of_sill"]) * S
            L = uni(rng, [v * 1000.0 for v in es["length_m"]])
            xe = side * (S / 2 - w * 0.55)
            out += streak(rng, kind, xe, 0, w, L, wander(), **common, role="end_streak")
        rv = E["rivulets"]
        n = uni_int(rng, rv["n"])
        for _ in range(n):
            xr = rng.uniform(-S / 2 + 20, S / 2 - 20)
            w = uni(rng, [v * 1000.0 for v in rv["width_m"]])
            L = uni(rng, [v * 1000.0 for v in rv["length_m"]])
            out += streak(rng, kind, xr, -wh * 0.2, w, L, wander() * 0.5, **common, role="rivulet", slices=8)
            if rng.uniform() < 0.25:
                ang = rng.choice([-1, 1]) * uni(rng, [12, 25])
                out += streak(rng, kind, xr, -wh * 0.2 - L * 0.5, w * 0.7, L * 0.5, wander() * 0.3, **common, role="fork", tilt_deg=ang, slices=5)
        return out
    if "span_m" in E:
        span = uni(rng, [v * 1000.0 for v in E["span_m"]])
        fg = E["fingers"]
        ws = E["wash"]
        wh = uni(rng, [v * 1000.0 for v in ws["height_m"]])
        out.append(poly(kind, ws["level"], [(-span / 2, 0), (span / 2, 0), (span / 2, -wh), (-span / 2, -wh * 0.8)], "wash"))
        n = max(2, int(fg["n_per_m"][0] * span / 1000.0 + rng.uniform(0, (fg["n_per_m"][1] - fg["n_per_m"][0]) * span / 1000.0)))
        xs = np.sort(rng.uniform(-span / 2 + 30, span / 2 - 30, n))
        for x in xs:
            w = uni(rng, [v * 1000.0 for v in fg["width_m"]])
            L = uni(rng, [v * 1000.0 for v in fg["length_m"]])
            out += streak(rng, kind, x, 0, w, L, wander(), **common, role="finger", slices=14)
        return out
    if "fixing" in E:
        fx = E["fixing"]
        d = uni(rng, fx["dot_mm"])
        h = uni(rng, [v * 1000.0 for v in fx["halo_m"]])
        out.append(poly(kind, fx.get("halo_level", 0.22), circle(0, 0, h / 2), "halo"))
        out.append(poly(kind, 1.0, circle(0, 0, d / 2, 10), "fixing"))
        tr = E["trickle"]
        n = uni_int(rng, tr["n"])
        last = None
        for i in range(n):
            w = uni(rng, [v * 1000.0 for v in tr["width_m"]])
            L = uni(rng, [v * 1000.0 for v in tr["length_m"]])
            xo = (i - (n - 1) / 2) * 12.0
            out += streak(rng, kind, xo, -d / 2, w, L, wander(), **common, role="trickle")
            last = (xo, -d / 2 - L)
        dr = E.get("drops")
        if dr and last:
            for _ in range(uni_int(rng, dr["n"])):
                eq = uni(rng, dr["eqd_mm"])
                out.append(poly(kind, 0.9, blob(rng, last[0] + rng.uniform(-8, 8), last[1] - rng.uniform(10, 60), eq, 1.8, math.pi / 2), "drop"))
        return out
    raise ValueError("unknown streak_set variant for " + kind)


def blob_field_polys(rng, kind, E, tj, variant=0):
    out = []
    W, H = [v * 1000.0 for v in E["region_m"]]
    anchor = E.get("anchor", "centre")
    bl = E.get("blobs")
    if bl:
        n = uni_int(rng, bl["n"])
        p10, p50, p90 = [v * 1000.0 for v in bl["eqd_m"]]
        for eq in lognormal3(rng, p10, p50, p90, n):
            if anchor == "bottom_centre":
                cx, cy = rng.uniform(-W * 0.3, W * 0.3), rng.uniform(eq * 0.4, H * 0.6)
            elif anchor == "top_centre":
                cx, cy = rng.uniform(-W * 0.3, W * 0.3), -rng.uniform(eq * 0.4, H * 0.3)
            else:
                cx, cy = rng.uniform(-W * 0.3, W * 0.3), rng.uniform(-H * 0.3, H * 0.3)
            asp = uni(rng, bl["aspect"])
            ang = math.pi / 2 if bl.get("orient") == "vertical" else rng.uniform(0, math.pi)
            ang += rng.normal(0, 0.12)
            out.append(poly(kind, uni(rng, [0.75, 1.0]), blob(rng, cx, cy, float(eq), asp, ang), "blob"))
    jm = E.get("joint_moss")
    if jm:
        bw, bh = 215.0, 75.0
        for c in range(int(H / bh)):
            y = c * bh
            if rng.uniform() < jm["share"] * 4.0:
                x0 = rng.uniform(-W / 2, W / 4)
                x1 = x0 + rng.uniform(150, W / 2)
                out.append(poly(kind, 0.75, [(x0, y), (x1, y), (x1, y + 9), (x0, y + 9)], "joint_moss"))
    rn = E.get("run")
    if rn and rng.uniform() < 0.6:
        n = uni_int(rng, rn["n"])
        for _ in range(n):
            w = uni(rng, [v * 1000.0 for v in rn["width_m"]])
            L = uni(rng, [v * 1000.0 for v in rn["length_m"]])
            y0 = 0 if anchor != "bottom_centre" else min(H, L)
            out += streak(rng, kind, rng.uniform(-W * 0.25, W * 0.25), y0 if anchor == "bottom_centre" else -20, w, L, 0.02 * L, 0.4, 1.0, 0.7, 0.1, role="run", slices=8)
    ha = E.get("halo")
    if ha and variant % 3 == 0:
        wdt = uni(rng, [v * 1000.0 for v in ha["width_m"]])
        r_in = 200.0
        outer = circle(0, 0, r_in + wdt, 28)
        inner = circle(0, 0, r_in, 28)
        ring = outer + [outer[0]] + [inner[0]] + inner[::-1] + [inner[0]]
        out.append(poly(kind, ha["level"], ring, "halo"))
    jt = E.get("joints")
    if jt and variant % 3 == 2:
        for gx in (-300, 300):
            w = uni(rng, jt["width_mm"])
            out.append(poly(kind, jt["level"], [(gx - w / 2, -W / 2), (gx + w / 2, -W / 2), (gx + w / 2, W / 2), (gx - w / 2, W / 2)], "joint"))
    return out


def speckle_band_polys(rng, kind, E):
    out = []
    L = uni(rng, [v * 1000.0 for v in E["length_m"]])
    Wd = E["width_m"] * 1000.0
    dens = uni(rng, E["density_per_m2"])
    n = int(dens * (L / 1000.0) * (Wd / 1000.0))
    p10, p50, p90 = E["dot_eqd_mm"]
    eq = lognormal3(rng, p10, p50, p90, n)
    xs = rng.uniform(0, L, n)
    ys = np.clip(rng.normal(0, Wd / 4.0, n), -Wd * 0.65, Wd * 0.65)
    for x, y, e in zip(xs, ys, eq):
        out.append(poly(kind, 0.85, blob(rng, x, y, float(e), uni(rng, [1.0, 1.4]), rng.uniform(0, math.pi), n=9, rough=0.2), "dot"))
    bl = E.get("blots")
    if bl:
        p10, p50, p90 = [v * 1000.0 for v in bl["eqd_m"]]
        for e in lognormal3(rng, p10, p50, p90, uni_int(rng, bl["n"])):
            out.append(poly(kind, 0.7, blob(rng, rng.uniform(-200, L + 200), rng.uniform(-Wd * 1.2, Wd * 1.2) - 400, float(e), uni(rng, [1.0, 2.2]), rng.uniform(0, math.pi), rough=0.3), "blot"))
    ts = E.get("tyre_scuff")
    if ts:
        Ls = uni(rng, [v * 1000.0 for v in ts["length_m"]])
        R = Ls / 1.2
        th = np.linspace(-0.6, 0.6, 30)
        path = np.stack([R * np.sin(th) + L / 2, -1300.0 + R * (1 - np.cos(th)) * 0.3], 1)
        # a soft profile of 90 mm FWHM: five nested ribbons, widest faintest (Photo M02 cross-profile)
        for i in range(10):
            out.append(poly(kind, 0.07 * (i + 1), ribbon(path, np.full(30, ts["width_mm"] * (1.9 - 1.6 * i / 9.0))), "tyre_scuff"))
    return out


def crack_polys(rng, kind, x0, y0, ang, length, width, step, branch_prob, depth=0, turn=0.28):
    n = max(3, int(length / step))
    a = ang
    p = [(x0, y0)]
    for _ in range(n):
        a += rng.normal(0, turn)
        p.append((p[-1][0] + step * math.cos(a), p[-1][1] + step * math.sin(a)))
    w = np.linspace(width, width * 0.5, len(p))
    out = [poly(kind, 1.0, ribbon(p, w), "crack", path_length(p))]
    if depth < 1:
        for i in range(2, len(p) - 2):
            if rng.uniform() < branch_prob / max(n, 1) * 3:
                b = a + rng.choice([-1, 1]) * math.radians(uni(rng, [12, 25]))
                out += crack_polys(rng, kind, p[i][0], p[i][1], b, length * 0.4, width * 0.7, step, branch_prob, depth + 1)
    return out


def voronoi_cracks(rng, kind, W, H, cell_mm, width_mm, keep, periodic, role, ellipse=None, origin=(0.0, 0.0)):
    """Drying-crack network: the edges of a Voronoi diagram of jittered seeds (cells about cell_mm across, 120 degree junctions),
    each kept with probability `keep`, drawn as 3-point ribbons. periodic=True makes the W x H tile seamless; ellipse=(cx, cy, rx, ry) keeps only edges inside it."""
    from scipy.spatial import Voronoi
    nx, ny = max(2, int(round(W / cell_mm))), max(2, int(round(H / cell_mm)))
    cw, ch = W / nx, H / ny
    pts = []
    for i in range(nx):
        for j in range(ny):
            pts.append(((i + 0.5 + rng.uniform(-0.4, 0.4)) * cw, (j + 0.5 + rng.uniform(-0.4, 0.4)) * ch))
    base = np.array(pts)
    reps = [base + np.array([dx * W, dy * H]) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
    allp = np.vstack(reps)
    vor = Voronoi(allp)
    out = []
    for (a, b) in vor.ridge_vertices:
        if a < 0 or b < 0:
            continue
        p, q = vor.vertices[a], vor.vertices[b]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        if not (-5 <= mx <= W + 5 and -5 <= my <= H + 5):
            continue
        if rng.uniform() > keep:
            continue
        if ellipse is not None:
            ex, ey, rx, ry = ellipse
            if ((mx - ex) / rx) ** 2 + ((my - ey) / ry) ** 2 > 1.0:
                continue
        m = [(p[0], p[1]), (mx + rng.normal(0, cw * 0.03), my + rng.normal(0, ch * 0.03)), (q[0], q[1])]
        wd = uni(rng, width_mm) if isinstance(width_mm, (list, tuple)) else float(width_mm)
        m = [(x + origin[0], y + origin[1]) for x, y in m]
        shifts = [(dx * W, dy * H) for dx in (-1, 0, 1) for dy in (-1, 0, 1)] if periodic else [(0.0, 0.0)]
        for sx, sy in shifts:
            mm_ = [(x + sx, y + sy) for x, y in m]
            if periodic and (max(x for x, _ in mm_) < -10 or min(x for x, _ in mm_) > W + 10 or max(y for _, y in mm_) < -10 or min(y for _, y in mm_) > H + 10):
                continue
            out.append(poly(kind, 1.0 if role == "map_crack" else 0.8, ribbon(mm_, np.full(3, wd)), role, path_length(m)))
    return out


def map_cracks(rng, kind, cx, cy, size_mm, cell_mm, width_mm):
    # a mapped patch: Voronoi cracks of an ellipse of the stated size (drying cracks), about half the edges kept
    return voronoi_cracks(rng, kind, size_mm * 1.2, size_mm * 1.2, cell_mm, width_mm, 0.55, False, "map_crack",
                          ellipse=(size_mm * 0.6, size_mm * 0.6, size_mm * 0.5, size_mm * 0.42), origin=(cx - size_mm * 0.6, cy - size_mm * 0.6))


def scuff_polys(rng, kind, E):
    """one tyre scuff: an arc of the stated length, a soft profile of ~90 mm FWHM from ten nested ribbons (Photo M02)"""
    Ls = uni(rng, [v * 1000.0 for v in E["length_m"]])
    th_max = rng.uniform(0.35, 0.6)
    R = Ls / (2 * th_max)
    th = np.linspace(-th_max, th_max, 40)
    sag = R * (1 - math.cos(th_max))
    path = np.stack([R * np.sin(th), R * (1 - np.cos(th)) - sag / 2], 1)
    out = []
    for i in range(10):
        out.append(poly(kind, 0.07 * (i + 1), ribbon(path, np.full(40, E["width_mm"] * (1.9 - 1.6 * i / 9.0))), "tyre_scuff"))
    return out


def crack_lines_polys(rng, kind, E):
    """a cracked road section: one sealed main crack and a few hairlines"""
    W, H = [v * 1000.0 for v in E["region_m"]]
    out = []
    m = E["main"]
    L = uni(rng, [v * 1000.0 for v in m["length_m"]])
    wd = uni(rng, m["width_mm"])
    out += crack_polys(rng, kind, rng.uniform(-W * 0.12, W * 0.12), -L / 2, math.radians(rng.uniform(84, 96)), L, wd, 60.0, 0.1, turn=0.07)
    hl = E["hairlines"]
    for _ in range(uni_int(rng, hl["n"])):
        out += crack_polys(rng, kind, rng.uniform(-W * 0.4, W * 0.4), rng.uniform(-H * 0.4, H * 0.4), rng.uniform(0, math.pi),
                           uni(rng, [v * 1000.0 for v in hl["length_m"]]), uni(rng, hl["width_mm"]), hl["step_m"] * 1000.0, hl["branch_prob"])
    return out


def crack_set_polys(rng, kind, E):
    out = []
    W, H = [v * 1000.0 for v in E["region_m"]]
    cc = E["corner_cracks"]
    for side in (-1, 1):
        for _ in range(uni_int(rng, cc["n_per_opening"])):
            ang = math.radians(90 - side * uni(rng, cc["angle_deg"]))
            L = uni(rng, [v * 1000.0 for v in cc["length_m"]])
            out += crack_polys(rng, kind, side * 20.0, 20.0, ang, L, uni(rng, cc["width_mm"]), cc["step_m"] * 1000.0, cc["branch_prob"])
    mc = E["map_cracking"]
    size = uni(rng, [v * 1000.0 for v in mc["patch_m"]])
    out += map_cracks(rng, kind, W * 0.15, H * 0.1, size, uni(rng, [v * 1000.0 for v in mc["cell_m"]]), 4.0)
    return out


def rect_patch_polys(rng, kind, E):
    out = []
    w = uni(rng, [v * 1000.0 for v in E["patch_m"][0]])
    h = uni(rng, [v * 1000.0 for v in E["patch_m"][1]])
    rag = uni(rng, E["ragged_mm"])

    def ragged_rect(w, h, rag, n_per=8):
        pts = []
        for (ax, ay, bx, by) in ((-w / 2, -h / 2, w / 2, -h / 2), (w / 2, -h / 2, w / 2, h / 2), (w / 2, h / 2, -w / 2, h / 2), (-w / 2, h / 2, -w / 2, -h / 2)):
            for k in range(n_per):
                t = k / n_per
                x, y = ax + (bx - ax) * t, ay + (by - ay) * t
                if 0 < k:
                    x += rng.normal(0, rag * 0.4)
                    y += rng.normal(0, rag * 0.4)
                pts.append((x, y))
        return pts
    seam = E.get("seam_mm")
    if seam:
        sm = uni(rng, seam)
        outer = ragged_rect(w + 2 * sm, h + 2 * sm, rag)
        inner = ragged_rect(w, h, rag)
        ring = outer + [outer[0]] + [inner[0]] + inner[::-1] + [inner[0]]
        out.append(poly(kind, 1.0, ring, "seam"))
        out.append(poly(kind, E.get("infill_level", 0.35), inner, "infill"))
        ck = E.get("cracks")
        if ck:
            for _ in range(uni_int(rng, ck["n"])):
                out += crack_polys(rng, kind, rng.uniform(-w * 0.6, w * 0.6), rng.uniform(-h * 0.6, h * 0.6), rng.uniform(0, math.pi), uni(rng, [v * 1000.0 for v in ck["length_m"]]), uni(rng, ck["width_mm"]), 30.0, 0.3)
            mw = uni(rng, ck["main_crack_width_mm"])
            out += crack_polys(rng, kind, -w * 0.9, -h * 0.9, math.radians(80), ck.get("main_crack_length_m", 1.8) * 1000.0, mw, 60.0, 0.1, turn=0.07)
        return out
    out.append(poly(kind, 1.0, ragged_rect(w, h, rag), "patch"))
    dt = E.get("drip_tail")
    if dt and dt["length_m"][1] > 0:
        L = uni(rng, [v * 1000.0 for v in dt["length_m"]])
        ww = uni(rng, [v * 1000.0 for v in dt["width_m"]])
        out.append(poly(kind, 0.8, [(-ww / 2, -h / 2), (ww / 2, -h / 2), (ww * 0.15, -h / 2 - L), (-ww * 0.15, -h / 2 - L)], "drip_tail"))
    lb = E.get("loss_blobs")
    if lb:
        p10, p50, p90 = [v * 1000.0 for v in lb["eqd_m"]]
        n = int(uni(rng, lb["n_per_m2"]) * (w / 1000.0) * (h / 1000.0) * 1.0) + 1
        for e in lognormal3(rng, p10, p50, p90, n):
            e = min(float(e), 0.4 * min(w, h))
            out.append(poly(kind, 0.9, blob(rng, rng.uniform(-w / 2.4, w / 2.4), rng.uniform(-h / 2.4, h / 2.4), e, uni(rng, [1.0, 2.0]), rng.uniform(0, math.pi)), "loss"))
    ly = E.get("layers")
    if ly:
        for _ in range(uni_int(rng, ly["n"])):
            f = uni(rng, ly["intact_fraction"])
            ww, hh = w * math.sqrt(f), h * math.sqrt(f)
            ox, oy = rng.uniform(-(w - ww) / 2, (w - ww) / 2), rng.uniform(-(h - hh) / 2, (h - hh) / 2)
            out.append(poly(kind, uni(rng, [0.5, 0.95]), [(ox - ww / 2, oy - hh / 2), (ox + ww / 2, oy - hh / 2), (ox + ww / 2, oy + hh / 2), (ox - ww / 2, oy + hh / 2)], "layer"))
    return out


def flake_field_polys(rng, kind, E):
    out = []
    W, H = [v * 1000.0 for v in E["area_m"]]
    fl = E["flakes"]
    n = int(uni(rng, fl["density_per_m2"]) * W * H / 1e6)
    p10, p50, p90 = fl["eqd_mm"]
    for e in lognormal3(rng, p10, p50, p90, n):
        asp = float(np.clip(np.exp(rng.normal(math.log(fl["aspect_p50"]), 0.35)), 1.0, 8.0))
        cx0, cy0, an = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0, math.pi)
        bp = blob(rng, cx0, cy0, float(e), asp, an, n=14, rough=0.3)
        for dx in (-W, 0.0, W):
            for dy in (-H, 0.0, H):
                if (dx or dy) and not (-e <= cx0 + dx <= W + e and -e <= cy0 + dy <= H + e):
                    continue
                out.append(poly(kind, 1.0, [(x + dx, y + dy) for x, y in bp], "flake"))
    bs = fl.get("big_sheets")
    if bs:
        for _ in range(max(0, int(round(uni(rng, bs["n_per_m2"]) * W * H / 1e6)))):
            cx0, cy0 = rng.uniform(0, W), rng.uniform(0, H)
            eq0 = uni(rng, bs["eqd_mm"])
            bp = blob(rng, cx0, cy0, eq0, uni(rng, [1.0, 1.8]), rng.uniform(0, math.pi), n=20, rough=0.35)
            for dx in (-W, 0.0, W):
                for dy in (-H, 0.0, H):
                    if (dx or dy) and not (-eq0 <= cx0 + dx <= W + eq0 and -eq0 <= cy0 + dy <= H + eq0):
                        continue
                    out.append(poly(kind, 1.0, [(x + dx, y + dy) for x, y in bp], "sheet"))
    cq = E.get("craquelure")
    if cq:
        want = uni(rng, [v * 1000.0 for v in cq["cell_m"]])
        w_mm = (cq["width_mm"][0], cq["width_mm"][1])
        for q in voronoi_cracks(rng, kind, W, H, want, w_mm, cq.get("keep", 0.5), True, "craquelure"):
            out.append(q)
    return out


def points_polys(rng, kind, E, area_mm=(1000.0, 1000.0), density=None):
    out = []
    W, H = area_mm
    if "band" in E and density is None:
        pass
    dens = density if density is not None else float(np.sqrt(E["per_m2"][0] * E["per_m2"][1]))
    n = int(round(dens * W * H / 1e6))
    if E["shape"] == "disc":
        p10, p50, p90 = E["eqd_mm"]
        pts = []
        while len(pts) < n:
            if pts and rng.uniform() < E.get("cluster", {}).get("prob", 0.0):
                bx, by = pts[rng.integers(len(pts))]
                r = E["cluster"]["radius_m"] * 1000.0
                pts.append((bx + rng.uniform(-r, r), by + rng.uniform(-r, r)))
            else:
                pts.append((rng.uniform(0, W), rng.uniform(0, H)))
        eq = lognormal3(rng, p10, p50, p90, n)
        ring = E.get("ring")
        for (x, y), e in zip(pts, eq):
            asp = uni(rng, E["aspect"])
            ang = rng.uniform(0, math.pi)
            if ring:
                out.append(poly(kind, ring["level"], blob(rng, x, y, float(e) + 2 * ring["width_mm"], asp, ang, n=12, rough=0.18), "rim"))
            out.append(poly(kind, 1.0, blob(rng, x, y, float(e), asp, ang, n=12, rough=0.18), "disc"))
    else:
        (w10, w50, w90), (l10, l50, l90) = E["size_mm"]
        ws = lognormal3(rng, w10, w50, w90, n)
        ls = lognormal3(rng, l10, l50, l90, n)
        for w, l in zip(ws, ls):
            x, y, a = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0, math.pi)
            c, s = math.cos(a), math.sin(a)
            p = [(-l / 2, -w / 2), (l / 2, -w / 2), (l / 2, w / 2), (-l / 2, w / 2)]
            out.append(poly(kind, 1.0, [(x + c * px - s * py, y + s * px + c * py) for px, py in p], "end"))
    return out


def slab_grid_polys(rng, kind, E):
    out = []
    W, H = [v * 1000.0 for v in E["region_m"]]
    sw, sh = [v * 1000.0 for v in E["slab_m"]]
    cls = E["tone_shares"]
    names = list(cls)
    probs = np.array([cls[k] for k in names], float)
    probs /= probs.sum()
    lvl = {"dark": 0.0, "mid": 0.5, "pale": 1.0}
    nx, ny = int(math.ceil(W / sw)), int(math.ceil(H / sh))
    prev = names[0]
    for j in range(ny):
        off = 0.0 if j % 2 == 0 else sw / 2
        for i in range(-1, nx + 1):
            x0 = i * sw + off
            if i > -1 and rng.uniform() < 0.55:
                c = prev
            else:
                c = names[int(rng.choice(len(names), p=probs))]
            prev = c
            x1, y0, y1 = x0 + sw, j * sh, (j + 1) * sh
            if x1 < 0 or x0 > W:
                continue
            xa, xb = max(0, x0), min(W, x1)
            out.append(poly(kind, lvl[c], [(xa, y0), (xb, y0), (xb, y1), (xa, y1)], "slab_" + c))
            out.append(poly(kind, 0.0, [(xa, y0), (xb, y0), (xb, y0 + 6), (xa, y0 + 6)], "joint"))
            if rng.uniform() < E["crack_fraction"]:
                a = rng.uniform(0.3, 1.2) * rng.choice([-1, 1])
                out += crack_polys(rng, kind, (xa + xb) / 2 - 0.3 * sw, (y0 + y1) / 2 - 0.3 * sh, a, 0.9 * sw, 3.0, 25.0, 0.15)
    return out


def mottle_polys(rng, kind, E, size_mm=(2000.0, 2000.0)):
    wl = uni(rng, [v * 1000.0 for v in E["wavelength_m"]])
    cell = wl / 3.0
    nx, ny = max(2, int(round(size_mm[0] / cell))), max(2, int(round(size_mm[1] / cell)))
    g = rng.uniform(0, 1, (ny, nx))
    g = ndi.zoom(g, 3, order=3, mode="grid-wrap", grid_mode=True)
    g = ndi.gaussian_filter(g, 2.0, mode="wrap")
    lo, hi = E["level_range"]
    g = (g - g.min()) / (g.max() - g.min())
    g = lo + (hi - lo) * g
    subx, suby = size_mm[0] / g.shape[1], size_mm[1] / g.shape[0]
    out = []
    for j in range(g.shape[0]):
        for i in range(g.shape[1]):
            out.append(poly(kind, g[j, i], [(i * subx, j * suby), ((i + 1) * subx, j * suby), ((i + 1) * subx, (j + 1) * suby), (i * subx, (j + 1) * suby)], "mottle"))
    return out


# ------------------------------------------------------------------ one kind's envelope
def decal_frame_mm(tj, kid):
    return [v * 1000.0 for v in tj["kinds"][kid]["mask"]["decal_frame_m"]]


def kind_envelope(tj, kid, seed=1990, variant=0, density_override=None):
    """Polygons (mm) for one kind; origin and orientation as the decal frame says (see kind['mask']['origin'])."""
    k = tj["kinds"][kid]
    E = k["envelope"]
    rng = rng_for(seed, "%s/%d" % (kid, variant))
    p = E["primitive"]
    if p == "streak_set":
        return streak_set_polys(rng, kid, E, kid)
    if p == "foot_band":
        Wf = decal_frame_mm(tj, kid)[0]
        return foot_band_polys(rng, kid, E, Wf, kid)
    if p == "blob_field":
        return blob_field_polys(rng, kid, E, tj, variant)
    if p == "speckle_band":
        return speckle_band_polys(rng, kid, E)
    if p == "crack_set":
        return crack_set_polys(rng, kid, E)
    if p == "scuff_arc":
        return scuff_polys(rng, kid, E)
    if p == "crack_lines":
        return crack_lines_polys(rng, kid, E)
    if p == "rect_patch":
        return rect_patch_polys(rng, kid, E)
    if p == "flake_field":
        return flake_field_polys(rng, kid, E)
    if p == "points":
        W, H = decal_frame_mm(tj, kid)
        if density_override is None:
            tiers = k["where"]["density"].get("tiers")
            dens = k["where"]["density"]["typical"]
            if kid == "cig_end":
                dens = 4.0
        else:
            dens = density_override
        return points_polys(rng, kid, E, (W, H), dens)
    if p == "slab_grid":
        return slab_grid_polys(rng, kid, E)
    if p == "mottle":
        return mottle_polys(rng, kid, E, tuple(decal_frame_mm(tj, kid)))
    raise ValueError(p)


# ------------------------------------------------------------------ rasterising and drawing
def bounds(polys):
    xs = [x for p in polys for x, _ in p["poly"]]
    ys = [y for p in polys for _, y in p["poly"]]
    return min(xs), min(ys), max(xs), max(ys)


def rasterize(polys, extent_mm, px_per_m, edge_10_90_mm=0.0, wrap=False):
    """Mask (float 0..1) over extent_mm = (x0, y0, x1, y1), y up; polygons drawn from the lowest level up (so the highest wins); then a Gaussian blur giving the stated 10-90 % edge."""
    x0, y0, x1, y1 = extent_mm
    s = px_per_m / 1000.0
    w, h = int(round((x1 - x0) * s)), int(round((y1 - y0) * s))
    img = Image.new("F", (max(w, 1), max(h, 1)), 0.0)
    d = ImageDraw.Draw(img)
    for p in sorted(polys, key=lambda q: q["level"]):
        pts = [((x - x0) * s, (y1 - y) * s) for x, y in p["poly"]]
        if len(pts) >= 3:
            d.polygon(pts, fill=float(p["level"]))
    a = np.asarray(img, dtype=np.float32)
    if edge_10_90_mm and edge_10_90_mm * s > 0.9:
        mode = ("wrap", "wrap") if wrap in (True, "xy") else ("reflect", "wrap") if wrap == "x" else ("reflect", "reflect")
        a = ndi.gaussian_filter(a, edge_10_90_mm * s / 2.563, mode=mode)
    return np.clip(a, 0, 1)


PALETTE = {"streak_sill": (30, 60, 200), "streak_coping": (20, 100, 220), "wall_foot_splash": (10, 10, 10), "wall_foot_damp": (80, 60, 30), "salt_bloom": (240, 240, 230), "rust_bleed": (220, 100, 20),
           "algae_downpipe": (30, 140, 40), "paint_flake": (200, 30, 120), "paint_fade": (180, 150, 200), "render_crack": (60, 0, 0), "render_patch": (240, 200, 120), "poster_remnant": (255, 255, 255),
           "bird_dropping": (250, 250, 250), "gum": (40, 40, 40), "cig_end": (255, 240, 200), "pavement_stain": (130, 60, 20), "flag_patch_crack": (230, 230, 240), "road_oil": (20, 20, 20),
           "road_patch": (70, 70, 70), "road_blot": (10, 10, 10), "tyre_scuff": (50, 50, 90), "road_crack": (90, 20, 20), "gutter_grime": (30, 30, 30)}


def transform(polys, dx, dy, sx=1.0):
    return [dict(p, poly=[[round(x * sx + dx, 1), round(y * sx + dy, 1)] for x, y in p["poly"]]) for p in polys]


def draw_scene(name, W, H, items, out_dir, px_per_m=500, bg=(150, 146, 140), ground=False, edge_by_kind=None):
    """items: list of polys already in scene mm (y up). Colours each kind by PALETTE with alpha = level; a 0.1 m grid and a 0.5 m scale bar."""
    s = px_per_m / 1000.0
    w, h = int(W * s), int(H * s)
    base = np.zeros((h, w, 3), np.float32) + np.array(bg, np.float32)
    kinds = sorted({p["kind"] for p in items})
    for kid in kinds:
        ps = [p for p in items if p["kind"] == kid]
        a = rasterize(ps, (0, 0, W, H), px_per_m, (edge_by_kind or {}).get(kid, 0.0))
        col = np.array(PALETTE.get(kid, (0, 0, 0)), np.float32)
        base = base * (1 - a[..., None] * 0.85) + col * a[..., None] * 0.85
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for gx in range(0, int(W) + 1, 500):
        d.line([(gx * s, 0), (gx * s, h)], fill=(255, 255, 0), width=1)
    for gy in range(0, int(H) + 1, 500):
        d.line([(0, h - gy * s), (w, h - gy * s)], fill=(255, 255, 0), width=1)
    d.rectangle([8, h - 22, 8 + 0.5 * px_per_m, h - 12], fill=(255, 255, 255))
    d.text((12, h - 34), "0.5 m (grid 0.5 m)  %s" % name, fill=(255, 255, 255))
    im.save(os.path.join(out_dir, "scene_%s.png" % name))
    return im


def scene_wall_bay(tj, seed):
    """A 2.0 m wide, 3.6 m high plain bay: window sill at 2.2 m with its streaks, a coping at the top, a downpipe at the right with its shoe, an iron bracket with rust, a patch, the foot bands."""
    polys = []
    W, H = 2000.0, 3600.0
    polys += transform(kind_envelope(tj, "wall_foot_damp", seed, 1), 0, 0)
    polys += transform(kind_envelope(tj, "wall_foot_splash", seed, 1), 0, 0)
    polys += transform(kind_envelope(tj, "salt_bloom", seed, 1), 0, 0)
    polys += transform(kind_envelope(tj, "streak_sill", seed, 2), 900, 2200)
    polys += transform(kind_envelope(tj, "streak_coping", seed, 1), 1000, 3600)
    polys += transform(kind_envelope(tj, "algae_downpipe", seed, 1), 1800, 0)
    polys += transform(kind_envelope(tj, "rust_bleed", seed, 1), 300, 2900)
    polys += transform(kind_envelope(tj, "render_patch", seed, 1), 350, 1500)
    polys += transform(kind_envelope(tj, "bird_dropping", seed, 1), 1450, 2210)
    return W, H, polys


def scene_pavement(tj, seed):
    """1 m x 1 m of footway at a shop-door apron: gum, ends, a stain, two flag joints, a hairline crack."""
    W = H = 1000.0
    polys = []
    polys += transform(kind_envelope(tj, "pavement_stain", seed, 1), 500, 500)
    polys += transform(kind_envelope(tj, "gum", seed, 1, density_override=4.0), 0, 0)
    polys += transform(kind_envelope(tj, "cig_end", seed, 1, density_override=4.0), 0, 0)
    rng = rng_for(seed, "pavement/crack")
    polys += crack_polys(rng, "flag_patch_crack", 100, 80, math.radians(40), 700, 3.0, 25.0, 0.2)
    return W, H, polys


def scene_road(tj, seed):
    """3.0 m x 2.0 m of carriageway beside the kerb (kerb at y=0): channel grime, litter band, a drip band, a blot, a reinstatement, a crack and a scuff."""
    W, H = 3000.0, 2000.0
    polys = []
    polys += transform(kind_envelope(tj, "gutter_grime", seed, 1), 0, 0)  # foot_band's y is distance from the kerb foot
    polys += transform(kind_envelope(tj, "road_oil", seed, 1), 300, 1400)
    polys += transform(kind_envelope(tj, "road_blot", seed, 1), 1500, 1000)
    polys += transform(kind_envelope(tj, "tyre_scuff", seed, 1), 1500, 600)
    polys += transform(kind_envelope(tj, "road_patch", seed, 1), 2300, 1250)
    polys += transform(kind_envelope(tj, "road_crack", seed, 1), 700, 800)
    rng = rng_for(seed, "road/litter")
    k = tj["kinds"]["cig_end"]["envelope"]
    nb = int(rng.uniform(*k["band"]["per_m"]) * 3.0)
    (w10, w50, w90), (l10, l50, l90) = k["size_mm"]
    for _ in range(nb):
        x, y, a = rng.uniform(0, 3000), rng.uniform(40, 260), rng.uniform(0, math.pi)
        w, l = float(lognormal3(rng, w10, w50, w90)[0]), float(lognormal3(rng, l10, l50, l90)[0])
        c, s = math.cos(a), math.sin(a)
        polys.append(poly("cig_end", 1.0, [(x + c * px - s * py, y + s * px + c * py) for px, py in [(-l / 2, -w / 2), (l / 2, -w / 2), (l / 2, w / 2), (-l / 2, w / 2)]], "end"))
    return W, H, polys


def scene_paint(tj, seed):
    return 1000.0, 1000.0, kind_envelope(tj, "paint_flake", seed, 1)


def scene_render(tj, seed):
    polys = transform(kind_envelope(tj, "render_crack", seed, 1), 0, 0)
    return 1200.0, 1200.0, transform(polys, 600, 100)


def scene_flags(tj, seed):
    return 3000.0, 2400.0, kind_envelope(tj, "flag_patch_crack", seed, 1)


def scene_foot_profiles(tj, seed):
    W = 2000.0
    polys = []
    for i, kid in enumerate(("wall_foot_damp", "wall_foot_splash", "salt_bloom")):
        polys += transform(kind_envelope(tj, kid, seed, 3), 0, 0)
    return W, 1800.0, polys


def edges_by_kind(tj):
    out = {}
    for kid, k in tj["kinds"].items():
        if "edge_for_envelope_mm" in k["geometry"]:
            out[kid] = float(k["geometry"]["edge_for_envelope_mm"])
            continue
        e = k["geometry"].get("edge_10_90_mm")
        if isinstance(e, dict):
            vals = [v for x in e.values() for v in (x if isinstance(x, list) else [x])]
            out[kid] = float(np.mean([min(vals), max(vals)])) if vals else 0.0
        elif isinstance(e, list):
            out[kid] = float(np.sqrt(e[0] * e[1]))
        else:
            out[kid] = 0.0
    return out


def main(argv):
    if len(argv) < 2 or argv[1].startswith("-"):
        print(__doc__)
        return 2
    out_dir = argv[1]
    target = os.path.join(HERE, "target.json")
    seed = 1990
    if "--target" in argv:
        target = argv[argv.index("--target") + 1]
    if "--seed" in argv:
        seed = int(argv[argv.index("--seed") + 1])
    os.makedirs(out_dir, exist_ok=True)
    tj = json.load(open(target))
    ed = edges_by_kind(tj)
    result = {"seed": seed, "units": "millimetres; y up on walls, y forward on the ground", "scenes": {}, "kinds": {}}
    scenes = {"wall_bay_2m": scene_wall_bay, "pavement_1m2": scene_pavement, "road_3x2m": scene_road, "paint_1m2": scene_paint, "render_cracks": scene_render, "flags_3x2p4m": scene_flags, "foot_profiles_2m": scene_foot_profiles}
    for name, fn in scenes.items():
        W, H, polys = fn(tj, seed)
        result["scenes"][name] = {"width_mm": W, "height_mm": H, "polygons": polys}
        draw_scene(name, W, H, polys, out_dir, px_per_m=500 if max(W, H) <= 2500 else 380, edge_by_kind=ed)
    for kid in tj["kinds_order"]:
        k = tj["kinds"][kid]
        n_var = min(3, k["variants"]["count"])
        sheets = []
        for v in range(n_var):
            polys = kind_envelope(tj, kid, seed, v)
            result["kinds"].setdefault(kid, []).append({"variant": v, "polygons": polys})
            if not polys:
                continue
            x0, y0, x1, y1 = bounds(polys)
            pad = 60.0
            ext = (x0 - pad, y0 - pad, x1 + pad, y1 + pad)
            ppm = 800 if max(x1 - x0, y1 - y0) < 1500 else 400
            raw = rasterize(polys, ext, ppm, 0.0)
            soft = rasterize(polys, ext, ppm, ed.get(kid, 0.0))
            both = np.hstack([raw, np.full((raw.shape[0], 6), 0.5, np.float32), soft])
            sheets.append(Image.fromarray((255 - both * 255).astype(np.uint8)))
        if sheets:
            Wt = sum(s.size[0] for s in sheets) + 10 * (len(sheets) - 1)
            Ht = max(s.size[1] for s in sheets)
            sheet = Image.new("L", (Wt, Ht + 14), 200)
            xo = 0
            for s in sheets:
                sheet.paste(s, (xo, 14))
                xo += s.size[0] + 10
            ImageDraw.Draw(sheet).text((4, 1), "%s: left envelope, right softened to %.0f mm (10-90 %%); drawn %d px/m" % (kid, ed.get(kid, 0.0), ppm), fill=0)
            if max(sheet.size) > 1800:
                kf = 1800.0 / max(sheet.size)
                sheet = sheet.resize((int(sheet.size[0] * kf), int(sheet.size[1] * kf)), Image.LANCZOS)
            sheet.save(os.path.join(out_dir, "kind_%s.png" % kid))
    with open(os.path.join(out_dir, "wear_envelopes.json"), "w") as f:
        json.dump(result, f)
    print("target_drawing: %d scenes, %d kinds, %d polygons -> %s" % (len(result["scenes"]), len(result["kinds"]), sum(len(s["polygons"]) for s in result["scenes"].values()) + sum(len(v["polygons"]) for vs in result["kinds"].values() for v in vs), out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
