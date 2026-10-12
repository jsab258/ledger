"""wear_departures.py: where the wear masks depart from the target's own envelope drawing, after the fresh review of 12 October (REVIEW-v1.md, FAIL) (unit 4.5, cloud week 42).

The target is not edited (Jafar's ruling of 11 October: no more polishing of targets). Each departure below answers a finding of the review, keeps the kind's rule of place and size,
and is drawn with the target's own primitives (`blob`, `ribbon`, `poly`, `streak`, `voronoi_cracks`, `lognormal3`); check_wear.py runs the target's mask checks on the result as before,
and adds the review's own new checks (algae_shoe, poster_intact, paint_flake_on_crack).

  every streak       (finding 3) the target's `streak()` fades in 5 to 14 flat slices, which shows as banding down a sill; it now takes one slice per 5 mm of length
  algae_downpipe     (finding 1) the first patch stands on the shoe (lower edge on y = 0, 0.3 to 0.9 m wide), the others overlap it and narrow upward; the moss is patches on the
                     joints near the patch (none above 1.2 m); the run from a leaking joint widens downward, 0.03 to 0.05 m at the top to 0.1 to 0.3 m
  render_patch       (finding 2) one of the target's six types per variant: a rectangle, an L, a cut chase, a square with a smear tail, a loss cluster, one replacement brick
  poster_remnant     (finding 4) a paste-ghost rim at 0.25, layers at 0.6 to 1.0 covering 20, 40 or 70 per cent of the site, cut by straight tears; one strips-only variant
  tyre_scuff         (finding 5) radius 2, 3 or 5 m or near-straight by variant; strength 0.45 + 0.55 x smooth noise along the arc; the ends fade over 0.25 m
  gutter_grime       (finding 6) no trapezoid "fingers" (the target's fingers.n_per_m 1.0 becomes 0)
  paint_flake        (finding 7) crazing in variants 0 to 2 only (3 to 5 are for timber); in 0 to 2, 60 per cent of the flakes centred on a crack, long axis along it; one big sheet only
                     in variants 1 and 4 (the stallriser tile takes 0, 2, 3 and 5)
"""
import copy
import math

import numpy as np

SHEET_VARIANTS = {"paint_flake": (1, 4)}
CRAZING_VARIANTS = {"paint_flake": (0, 1, 2)}
POSTER_INTACT = (0.2, 0.4, 0.7, 0.4)          # variants 0 to 3: the intact fraction of the site; variant 4 is strips only
_STATE = {}


def install(draw):
    """Continuous fades: every streak drawn by the target's module takes one slice per 5 mm of its length (the first review's finding 3); every Voronoi crack (the paint's crazing,
    the render's map cracks) wanders (the second review's finding 3)."""
    if getattr(draw, "_ledger_streak_fixed", False):
        return
    orig = draw.streak

    def streak(rng, kind, x0, y0, w0, length, *a, slices=14, **k):
        return orig(rng, kind, x0, y0, w0, length, *a, slices=max(int(slices), int(math.ceil(float(length) / 5.0))), **k)
    draw.streak = streak
    draw.voronoi_cracks = lambda *a, **k: voronoi_cracks_bent(draw, *a, **k)
    draw._ledger_streak_fixed = True


def voronoi_cracks_bent(d, rng, kind, W, H, cell_mm, width_mm, keep, periodic, role, ellipse=None, origin=(0.0, 0.0)):
    """The target's voronoi_cracks (same seeds, same keeping, same 120-degree junctions and periodic copies), each edge's centre line bent sideways every 5 mm by smooth noise of
    0.06 times the edge's length, wavelength 25 to 50 mm, nothing at its two ends (so the junctions stay joined): a drying crack wanders, a Voronoi edge is straight."""
    from scipy.spatial import Voronoi
    nx, ny = max(2, int(round(W / cell_mm))), max(2, int(round(H / cell_mm)))
    cw, ch = W / nx, H / ny
    pts = []
    for i in range(nx):
        for j in range(ny):
            pts.append(((i + 0.5 + rng.uniform(-0.4, 0.4)) * cw, (j + 0.5 + rng.uniform(-0.4, 0.4)) * ch))
    base = np.array(pts)
    vor = Voronoi(np.vstack([base + np.array([dx * W, dy * H]) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]))
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
        L = float(np.hypot(q[0] - p[0], q[1] - p[1]))
        n = max(3, int(math.ceil(L / 5.0)) + 1)
        tt = np.linspace(0, 1, n)
        wl = rng.uniform(25.0, 50.0)
        off = d.smooth_noise_1d(rng, n, max(2.0, wl / 5.0)) * 0.06 * L * np.sin(math.pi * tt)
        tx, ty = (q[0] - p[0]) / max(L, 1e-9), (q[1] - p[1]) / max(L, 1e-9)
        m = [(p[0] + (q[0] - p[0]) * s - ty * o + origin[0], p[1] + (q[1] - p[1]) * s + tx * o + origin[1]) for s, o in zip(tt, off)]
        wd = d.uni(rng, width_mm) if isinstance(width_mm, (list, tuple)) else float(width_mm)
        shifts = [(dx * W, dy * H) for dx in (-1, 0, 1) for dy in (-1, 0, 1)] if periodic else [(0.0, 0.0)]
        for sx, sy in shifts:
            mm_ = [(x + sx, y + sy) for x, y in m]
            if periodic and (max(x for x, _ in mm_) < -10 or min(x for x, _ in mm_) > W + 10 or max(y for _, y in mm_) < -10 or min(y for _, y in mm_) > H + 10):
                continue
            out.append(d.poly(kind, 1.0 if role == "map_crack" else 0.8, d.ribbon(mm_, np.full(len(mm_), wd)), role, d.path_length(m)))
    return out


def envelope(tj, draw, kid, seed, variant):
    """The polygons of one mask: the target's envelope, or this unit's departure for the kinds above."""
    install(draw)
    if kid == "gutter_grime":
        if "tj_nofingers" not in _STATE:
            t2 = copy.deepcopy(tj)
            t2["kinds"]["gutter_grime"]["envelope"]["fingers"]["n_per_m"] = 0.0
            _STATE["tj_nofingers"] = t2
        return draw.kind_envelope(_STATE["tj_nofingers"], kid, seed, variant)
    f = {"algae_downpipe": algae, "render_patch": render_patch, "poster_remnant": poster, "tyre_scuff": scuff, "paint_flake": flakes}.get(kid)
    if kid == "rust_bleed":
        return rust_halo(draw, draw.kind_envelope(tj, kid, seed, variant), kid)
    if f is None:
        return draw.kind_envelope(tj, kid, seed, variant)
    E = tj["kinds"][kid]["envelope"]
    rng = draw.rng_for(seed, "%s/%d" % (kid, variant))
    return f(draw, rng, kid, E, variant)


# ------------------------------------------------------------------------------------------ rust_bleed (the second review's finding 4)
def rust_halo(d, polys, kind):
    """The rust halo round a fixing: not one flat disc at 0.18 with a crisp edge, but 12 nested discs fading as (1 - r/R)^1.5 from the target's halo level, centred 0.3 R below the fixing."""
    out = []
    for p in polys:
        if p["role"] != "halo":
            out.append(p)
            continue
        P = np.asarray(p["poly"], float)
        cx, cy = P.mean(0)
        R = float(np.hypot(*(P - [cx, cy]).T).mean())
        for i in range(12):
            r = R * (1 - i / 12.0)
            lv = p["level"] * (1 - r / R + 1.0 / 24.0) ** 1.5
            out.append(d.poly(kind, lv, d.circle(cx, cy - 0.3 * R, r, 28), "halo"))
    return out


# ------------------------------------------------------------------------------------------ algae_downpipe (finding 1)
def algae(d, rng, kind, E, variant):
    """The patch on the shoe, rising 0.4 to 0.7 m and wider low down (the second review: in 3 of 5 variants it rose only 0.2 m); its moss in the joints near it, horizontal in the bed
    joints and upright in the perpends; in variants 0 and 2 a run from a leaking joint, 0.08 to 0.30 m wide at full strength, no fade, from 0.9 to 1.35 m up down to the patch."""
    out = []
    W, H = [v * 1000.0 for v in E["region_m"]]
    wb = rng.uniform(300.0, 500.0)
    wt = rng.uniform(60.0, 120.0)
    rise = rng.uniform(400.0, 700.0)
    cx = rng.uniform(-80.0, 80.0)
    m = 14
    ys = np.linspace(0.0, rise, m)
    half = (wb / 2) * (1 - (ys / rise) ** 0.8) + (wt / 2) * (ys / rise) ** 0.8
    rag_l = d.smooth_noise_1d(rng, m, 3.0) * 25.0
    rag_r = d.smooth_noise_1d(rng, m, 3.0) * 25.0
    lean = rng.uniform(-40.0, 40.0) * (ys / rise)
    left = [(cx + lean[k] - half[k] + rag_l[k], ys[k]) for k in range(m)]
    right = [(cx + lean[k] + half[k] + rag_r[k], ys[k]) for k in range(m - 1, -1, -1)]
    top = [(cx + lean[-1] + rng.uniform(-0.3, 0.3) * wt, rise + rng.uniform(10.0, 40.0))]
    pts = [(cx - wb / 2 - 30.0, -40.0)] + left + top + right + [(cx + wb / 2 + 30.0, -40.0)]
    out.append(d.poly(kind, d.uni(rng, [0.75, 0.9]), pts, "blob"))
    if variant != 3:                                      # moss in the joints near the patch (variant 3 has none: "joint moss on/off")
        p10, p50, p90 = 5.5, 10.2, 31.5
        reach = 150.0
        cand = []
        for c, y in enumerate(np.arange(0.0, min(1200.0, rise + reach), 75.0)):
            off = 0.0 if c % 2 == 0 else 107.5
            for x in np.arange(-W / 2 - off, W / 2, 215.0):
                cand.append((x + off, y + 37.5, 1))      # a perpend (upright)
            for x in np.linspace(-W / 2, W / 2, 24):
                cand.append((x, y, 0))                    # along the bed joint (horizontal)
        cand = np.array(cand)
        near = (np.abs(cand[:, 0] - cx) <= wb / 2 + reach) & (cand[:, 1] <= rise + reach)
        cand = cand[near]
        k = int(min(len(cand), rng.integers(18, 45)))
        if k:
            pick = cand[rng.choice(len(cand), k, replace=False)]
            for (x, y, up), e in zip(pick, d.lognormal3(rng, p10, p50, p90, k)):
                e = float(np.clip(e, 4.0, 45.0))
                out.append(d.poly(kind, 0.75, d.blob(rng, x + (rng.normal(0, 15) if not up else rng.normal(0, 2)), y + (rng.normal(0, 3) if not up else rng.normal(0, 15)), e,
                                                    rng.uniform(1.5, 3.0), math.pi / 2 if up else 0.0, n=12, rough=0.3), "joint_moss"))
    if variant in (0, 2):                                 # a run from a leaking joint: full strength, no fade, 0.08 to 0.30 m wide
        y0 = rng.uniform(900.0, 1350.0)
        w = rng.uniform(80.0, 300.0)
        xr = cx + lean[-1] + rng.uniform(-0.3, 0.3) * wt
        n = 24
        yy = np.linspace(y0, rise * 0.6, n)
        ww = w * np.clip(1 + 0.15 * d.smooth_noise_1d(rng, n, 6.0), 0.8, 1.2)
        wx = xr + 12.0 * d.smooth_noise_1d(rng, n, 8.0)
        pts = [(wx[k] - ww[k] / 2, yy[k]) for k in range(n)] + [(wx[k] + ww[k] / 2, yy[k]) for k in range(n - 1, -1, -1)]
        out.append(d.poly(kind, 0.85, pts, "run"))
    return out


# ------------------------------------------------------------------------------------------ render_patch (finding 2)
def ragged(d, rng, pts, rag, n_per=10):
    """A ragged outline along a closed polyline of straight sides (the target's ragged_rect, for any polygon): smooth noise across each side, the corners kept."""
    out = []
    P = list(pts)
    for i in range(len(P)):
        ax, ay = P[i]
        bx, by = P[(i + 1) % len(P)]
        L = math.hypot(bx - ax, by - ay)
        nx, ny = (-(by - ay) / max(L, 1e-6), (bx - ax) / max(L, 1e-6))
        k = max(3, int(n_per * L / 300.0) + 3)
        off = d.smooth_noise_1d(rng, k + 1, max(2.0, k / 3.0)) * rag * 0.35
        for j in range(k):
            t = j / k
            o = off[j] if j else 0.0
            out.append((ax + (bx - ax) * t + nx * o, ay + (by - ay) * t + ny * o))
    return out


def render_patch(d, rng, kind, E, variant):
    out = []
    rag = d.uni(rng, E["ragged_mm"])
    w = d.uni(rng, [v * 1000.0 for v in E["patch_m"][0]])
    h = d.uni(rng, [v * 1000.0 for v in E["patch_m"][1]])
    t = variant % 6
    if t == 0:                                            # a rectangle, no tail
        out.append(d.poly(kind, 1.0, ragged(d, rng, [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)], rag), "patch"))
    elif t == 1:                                          # an L: one corner cut, 40 to 60 per cent of each side
        from shapely.geometry import box
        cw, ch = w * rng.uniform(0.4, 0.6), h * rng.uniform(0.4, 0.6)
        sx, sy = (1 if rng.random() < 0.5 else -1), (1 if rng.random() < 0.5 else -1)
        cx, cy = sx * w / 2, sy * h / 2
        Lp = box(-w / 2, -h / 2, w / 2, h / 2).difference(box(min(cx, cx - sx * cw), min(cy, cy - sy * ch), max(cx, cx - sx * cw), max(cy, cy - sy * ch)))
        out.append(d.poly(kind, 1.0, ragged(d, rng, list(Lp.exterior.coords)[:-1], rag), "patch"))
    elif t == 2:                                          # a cut chase: 0.06 to 0.12 by 0.4 to 0.7 m (vertical or across)
        cw, cl = rng.uniform(60.0, 120.0), rng.uniform(400.0, 700.0)
        cl = min(cl, 760.0)
        if rng.random() < 0.6:
            pts = [(-cw / 2, -cl / 2 - 50), (cw / 2, -cl / 2 - 50), (cw / 2, cl / 2 - 50), (-cw / 2, cl / 2 - 50)]
        else:
            cl = min(cl, 660.0)
            pts = [(-cl / 2, -cw / 2), (cl / 2, -cw / 2), (cl / 2, cw / 2), (-cl / 2, cw / 2)]
        out.append(d.poly(kind, 1.0, ragged(d, rng, pts, min(rag, 15.0)), "patch"))
    elif t == 3:                                          # a square with a smear tail: level 0.4, 40 mm soft edge (the edge is the raster's), offset up to 0.3 w
        s = min(w, h)
        out.append(d.poly(kind, 1.0, ragged(d, rng, [(-s / 2, -s / 2), (s / 2, -s / 2), (s / 2, s / 2), (-s / 2, s / 2)], rag), "patch"))
        L = rng.uniform(80.0, 220.0)
        ox = rng.uniform(-0.3, 0.3) * s
        tw = rng.uniform(0.35, 0.6) * s
        out += d.streak(rng, kind, ox, -s / 2 + 10.0, tw, L, 8.0, 0.6, 1.0, 0.4, 0.2, role="smear")
    elif t == 4:                                          # a loss cluster: 4 to 9 losses (33 / 67 / 294 mm), no patch, spread and not touching, ragged (the second review)
        p10, p50, p90 = [v * 1000.0 for v in E["loss_blobs"]["eqd_m"]]
        n = int(rng.integers(4, 10))
        placed = []
        for e in sorted(d.lognormal3(rng, p10, p50, p90, n), reverse=True):
            e = float(np.clip(e, 30.0, 200.0))
            for _try in range(60):
                x, y = rng.uniform(-300 + e / 2, 300 - e / 2), rng.uniform(-400 + e / 2, 300 - e / 2)
                if all(math.hypot(x - a, y - b) > (e + f_) * 0.75 + 20.0 for a, b, f_ in placed):
                    break
            else:
                continue
            placed.append((x, y, e))
            out.append(d.poly(kind, rng.uniform(0.85, 1.0), d.blob(rng, x, y, e, d.uni(rng, [1.0, 2.0]), rng.uniform(0, math.pi), n=24, rough=0.38), "loss"))
    else:                                                 # one replacement brick, 0.215 by 0.065 m, a mortar-coloured ring round it
        bw, bh = 215.0, 65.0
        out.append(d.poly(kind, 1.0, ragged(d, rng, [(-bw / 2, -bh / 2), (bw / 2, -bh / 2), (bw / 2, bh / 2), (-bw / 2, bh / 2)], 2.0, 4), "brick"))
    return out


# ------------------------------------------------------------------------------------------ poster_remnant (finding 4)
def cut_by_tears(d, rng, pts, n):
    """Cut a polygon by 1 to 3 straight tears at 30 to 60 degrees (keeping the side that holds the polygon's first point's far side), each tear edge ragged."""
    from shapely.geometry import Polygon, LineString
    from shapely.ops import split
    P = Polygon(pts).buffer(0)
    for _ in range(n):
        if P.is_empty:
            break
        c = P.centroid
        bx0, by0, bx1, by1 = P.bounds
        ang = math.radians(rng.uniform(30, 60)) * (1 if rng.random() < 0.5 else -1) + (0 if rng.random() < 0.5 else math.pi / 2)
        dx, dy = math.cos(ang), math.sin(ang)
        off = rng.uniform(0.2, 0.4) * max(bx1 - bx0, by1 - by0) * (1 if rng.random() < 0.5 else -1)          # a tear takes a corner or an edge
        px, py = c.x - dy * off, c.y + dx * off
        R = 0.8 * math.hypot(bx1 - bx0, by1 - by0)
        k = max(24, int(2 * R / 6.0))                    # a point every 6 mm: a torn edge wanders 6 to 10 mm over 30 to 60 mm and is ragged by 2 mm
        ts = np.linspace(-R, R, k)
        jag = d.smooth_noise_1d(rng, k, max(3.0, 45.0 / 6.0)) * rng.uniform(6.0, 10.0) + rng.normal(0, 1.2, k)
        line = LineString([(px + dx * t - dy * j, py + dy * t + dx * j) for t, j in zip(ts, jag)])
        parts = list(split(P, line).geoms) if P.intersects(line) else [P]
        if len(parts) > 1:
            parts.sort(key=lambda g: -g.area)
            P = parts[0]                                  # the larger part stays on the wall
    if P.is_empty:
        return []
    geoms = list(P.geoms) if P.geom_type == "MultiPolygon" else [P]
    return [list(g.exterior.coords) for g in geoms if g.area > 100]


def poster(d, rng, kind, E, variant):
    out = []
    w = d.uni(rng, [v * 1000.0 for v in E["patch_m"][0]])
    h = d.uni(rng, [v * 1000.0 for v in E["patch_m"][1]])
    w, h = min(w, 1050.0), min(h, 850.0)
    site = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    out += paste_rim(d, rng, kind, w, h)
    if variant % 5 == 4:                                  # strips only: 2 to 5 vertical strips, 30 to 120 mm wide
        for _ in range(int(rng.integers(2, 6))):
            sw = rng.uniform(30.0, 120.0)
            x = rng.uniform(-w / 2 + sw / 2, w / 2 - sw / 2)
            y0, y1 = -h / 2 + rng.uniform(0, 0.3) * h, h / 2 - rng.uniform(0, 0.4) * h
            for p in cut_by_tears(d, rng, ragged(d, rng, [(x - sw / 2, y0), (x + sw / 2, y0), (x + sw / 2, y1), (x - sw / 2, y1)], 8.0, 30), 0):
                out.append(d.poly(kind, rng.uniform(0.7, 1.0), p, "strip"))
        return out
    f = POSTER_INTACT[variant % 5]
    n_l = int(rng.integers(2, 5))
    for i in range(n_l):                                  # layers: the oldest biggest; each cut by 1 to 3 tears
        fi = f * (1.0 if i == 0 else rng.uniform(0.3, 0.7))
        ww, hh = w * math.sqrt(fi) * rng.uniform(1.0, 1.3), h * math.sqrt(fi) * rng.uniform(1.0, 1.3)
        ww, hh = min(ww, w), min(hh, h)
        ox, oy = rng.uniform(-(w - ww) / 2, (w - ww) / 2), rng.uniform(-(h - hh) / 2, (h - hh) / 2)
        rect = ragged(d, rng, [(ox - ww / 2, oy - hh / 2), (ox + ww / 2, oy - hh / 2), (ox + ww / 2, oy + hh / 2), (ox - ww / 2, oy + hh / 2)], 14.0, 30)
        for _try in range(20):                          # a tear that leaves a corner under 70 degrees is redrawn
            parts = cut_by_tears(d, rng, rect, int(rng.integers(1, 3)))
            if all(min_corner_deg(p) >= 70.0 for p in parts):
                break
        lv = rng.uniform(0.6, 1.0)
        for p in parts:
            out.append(d.poly(kind, lv, p, "layer"))
    return out


def paste_rim(d, rng, kind, w, h):
    """The paste ghost (the second review): 2 to 4 broken runs along the site's edge, together 30 to 60 per cent of it, each 10 to 40 mm wide and varying along it, at 0.25."""
    per = 2 * (w + h)
    k = int(rng.integers(2, 5))
    total = per * rng.uniform(0.3, 0.6)
    lens = rng.dirichlet(np.ones(k)) * total
    starts = np.sort(rng.uniform(0, per, k))
    out = []

    def at(s):
        s %= per
        if s < w:
            return np.array([-w / 2 + s, -h / 2]), np.array([0.0, 1.0])
        s -= w
        if s < h:
            return np.array([w / 2, -h / 2 + s]), np.array([-1.0, 0.0])
        s -= h
        if s < w:
            return np.array([w / 2 - s, h / 2]), np.array([0.0, -1.0])
        s -= w
        return np.array([-w / 2, h / 2 - s]), np.array([1.0, 0.0])
    for s0, L in zip(starts, lens):
        n = max(4, int(L / 10.0))
        ss = s0 + np.linspace(0, L, n)
        wd = np.clip(rng.uniform(10, 40) * (1 + 0.35 * d.smooth_noise_1d(rng, n, 4.0)), 10.0, 40.0)
        P, N = zip(*[at(s) for s in ss])
        outer = [tuple(p) for p in P]
        inner = [tuple(p + nn * wv) for p, nn, wv in zip(P, N, wd)]
        out.append(d.poly(kind, 0.25, outer + inner[::-1], "paste_rim", L))
    return out


def min_corner_deg(pts, tol=10.0):
    """The sharpest corner of a polygon after simplifying it by `tol` mm (a tear must not leave a sliver: the second review)."""
    from shapely.geometry import Polygon
    g = Polygon(pts).buffer(0).simplify(tol)
    if g.is_empty or g.geom_type != "Polygon":
        return 180.0
    P = np.asarray(g.exterior.coords)[:-1]
    if len(P) < 3:
        return 180.0
    a = np.roll(P, 1, 0) - P
    b = np.roll(P, -1, 0) - P
    cosv = (a * b).sum(1) / np.maximum(np.hypot(*a.T) * np.hypot(*b.T), 1e-9)
    return float(np.degrees(np.arccos(np.clip(cosv, -1, 1))).min())


def poster_intact(variant):
    return None if variant % 5 == 4 else POSTER_INTACT[variant % 5]


# ------------------------------------------------------------------------------------------ tyre_scuff (finding 5)
def scuff(d, rng, kind, E, variant):
    Ls = d.uni(rng, [v * 1000.0 for v in E["length_m"]])
    R = {0: 2000.0, 1: 3000.0, 2: 5000.0}.get(variant % 4)
    n = 240
    if R is None:                                         # near-straight
        x = np.linspace(-Ls / 2, Ls / 2, n)
        path = np.stack([x, 12.0 * d.smooth_noise_1d(rng, n, n / 2.0)], 1)
    else:
        th_max = min(Ls / (2 * R), 1.2)
        th = np.linspace(-th_max, th_max, n)
        sag = R * (1 - math.cos(th_max))
        path = np.stack([R * np.sin(th), R * (1 - np.cos(th)) - sag / 2], 1)
    s = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(path, axis=0).T))])
    Lt = s[-1]
    wl = rng.uniform(300.0, 800.0)
    nz = d.smooth_noise_1d(rng, n, max(2.0, n * wl / Lt))
    nz = (nz - nz.min()) / max(1e-6, nz.max() - nz.min())
    st = 0.45 + 0.55 * nz
    fe = np.clip(np.minimum(s, Lt - s) / 250.0, 0, 1)
    st = st * fe * fe * (3 - 2 * fe)
    out = []
    seg = 2                                               # 10 to 12 mm a segment: the strength steps under 1 per cent, under the 70 mm edge
    for a in range(0, n - 1, seg):
        b = min(n - 1, a + seg)
        sm = float(st[a:b + 1].mean())
        if sm <= 0.01:
            continue
        p = path[a:b + 1]
        for i in range(10):
            out.append(d.poly(kind, 0.07 * (i + 1) * sm, d.ribbon(p, np.full(len(p), E["width_mm"] * (1.9 - 1.6 * i / 9.0))), "tyre_scuff"))
    return out


# ------------------------------------------------------------------------------------------ paint_flake (finding 7)
def flakes(d, rng, kind, E, variant):
    out = []
    W, H = [v * 1000.0 for v in E["area_m"]]
    fl = E["flakes"]
    crazing = variant in CRAZING_VARIANTS["paint_flake"]
    segs = []
    cq = E.get("craquelure")
    if crazing and cq:
        want = d.uni(rng, [v * 1000.0 for v in cq["cell_m"]])
        cr = d.voronoi_cracks(rng, kind, W, H, want, (cq["width_mm"][0], cq["width_mm"][1]), cq.get("keep", 0.5), True, "craquelure")
        out += cr
        for q in cr:                                      # each crack is a ribbon round a 3-point centre line
            P = np.asarray(q["poly"], float)
            m = len(P) // 2
            cl = (P[:m] + P[m:][::-1]) / 2.0
            mid = cl.mean(0)
            if 0 <= mid[0] <= W and 0 <= mid[1] <= H:
                segs.append(cl)
    dens = d.uni(rng, fl["density_per_m2"]) * (1.25 if variant in (2, 5) else 1.0)
    n = int(dens * W * H / 1e6)
    p10, p50, p90 = fl["eqd_mm"]
    if not crazing:                                       # timber, no crazing: the flakes 1.45 times the size, so that they alone bare the target's 3 to 15 per cent (its photograph's 6.3)
        p10, p50, p90 = p10 * 1.45, p50 * 1.45, p90 * 1.45
    for e in d.lognormal3(rng, p10, p50, p90, n):
        asp = float(np.clip(np.exp(rng.normal(math.log(fl["aspect_p50"]), 0.35)), 1.0, 8.0))
        if segs and rng.random() < 0.6:                   # centred on a crack, its long axis along it (+/- 10 degrees)
            sg = segs[int(rng.integers(len(segs)))]
            j = int(rng.integers(len(sg) - 1))
            t = rng.random()
            p0, p1 = sg[j], sg[j + 1]
            cx0, cy0 = p0 + (p1 - p0) * t
            an = math.atan2(p1[1] - p0[1], p1[0] - p0[0]) + math.radians(rng.uniform(-10, 10))
            cx0, cy0 = cx0 % W, cy0 % H
        elif not crazing:                                 # timber: along the grain (x in the tile), within 8 degrees
            cx0, cy0, an = rng.uniform(0, W), rng.uniform(0, H), math.radians(rng.uniform(-8, 8))
        else:
            cx0, cy0, an = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0, math.pi)
        bp = d.blob(rng, cx0, cy0, float(e), asp, an, n=int(rng.integers(6, 10)), rough=0.35)          # an angular chip: 6 to 9 straight sides (the second review)
        e = max(max(abs(x - cx0), abs(y - cy0)) for x, y in bp) + 2.0          # the flake's true reach, so that a copy over the tile's edge is never skipped (the seam)
        for dx in (-W, 0.0, W):
            for dy in (-H, 0.0, H):
                if (dx or dy) and not (-e <= cx0 + dx <= W + e and -e <= cy0 + dy <= H + e):
                    continue
                out.append(d.poly(kind, 1.0, [(x + dx, y + dy) for x, y in bp], "flake"))
    bs = fl.get("big_sheets")
    if bs and variant in SHEET_VARIANTS["paint_flake"]:
        cx0, cy0 = rng.uniform(0, W), rng.uniform(0, H)
        eq0 = d.uni(rng, bs["eqd_mm"])
        bp = d.blob(rng, cx0, cy0, eq0, d.uni(rng, [1.0, 1.8]), rng.uniform(0, math.pi), n=20, rough=0.35)
        eq0 = max(max(abs(x - cx0), abs(y - cy0)) for x, y in bp) + 2.0
        for dx in (-W, 0.0, W):
            for dy in (-H, 0.0, H):
                if (dx or dy) and not (-eq0 <= cx0 + dx <= W + eq0 and -eq0 <= cy0 + dy <= H + eq0):
                    continue
                out.append(d.poly(kind, 1.0, [(x + dx, y + dy) for x, y in bp], "sheet"))
    return out


# ------------------------------------------------------------------------------------------ checks: the target's, less the one a departure replaces, and the review's new ones
REPLACED = {("poster_remnant", "coverage_of_decal"): (None, "replaced by poster_intact: the target's 0.25 to 0.75 of the frame assumed one whole sheet; its own variants are 20 to 70 per cent intact"),
            ("render_patch", "coverage_of_decal"): ((5,), "not on variant 5, the target's own single replacement brick (0.215 x 0.065 m is 2.5 per cent of the 0.7 x 0.8 m frame; the check asks 10)"),
            ("algae_downpipe", "blob_eqd_mm_p50"): ((0, 2), "not on variants 0 and 2, which carry the rule's run from a leaking joint (0.1 to 0.3 m wide, 0.5 to 1.5 m long): joined to the patch on the shoe it is past the check's 450 mm; algae_rise and algae_run hold them")}


def kind_checks(k, kid, composition_measures, variant=None):
    """The target's mask checks of a kind, less those a departure replaces (for the given variant; variant None: the checks every variant takes)."""
    out = []
    for c in k["checks"]:
        if c.get("applies_to") != "mask" or c["measure"] in composition_measures:
            continue
        r = REPLACED.get((kid, c["name"]))
        if r is not None and (r[0] is None or (variant is not None and variant in r[0])):
            continue
        out.append(c)
    return out


def extra_checks(kid, variant, m, ppm, polys):
    """[(name, value, ok, detail)]: the review's new checks for the departures (algae on the shoe, the poster's intact share, flakes on the cracks)."""
    out = []
    if kid == "algae_downpipe":
        row = m[m.shape[0] - 1 - int(round(0.02 * ppm))]          # 0.02 m above the shoe (row 0 is the frame's top, 1.4 m)
        wide = float((row >= 0.5).sum()) / ppm
        out.append(("algae_shoe", wide, wide >= 0.3, "mask >= 0.5 over %.2f m at 0.02 m up (at least 0.3)" % wide))
        bl = [q for q in polys if q["role"] == "blob"]
        rise = max(y for q in bl for _x, y in q["poly"]) / 1000.0 if bl else 0.0
        out.append(("algae_rise", rise, 0.4 <= rise <= 1.2, "the patch rises %.2f m above the shoe (the rule: 0.4 to 1.2)" % rise))
        rn = [q for q in polys if q["role"] == "run"]
        if variant in (0, 2):
            ok, det, val = False, "no run", 0.0
            if rn:
                P = np.asarray(rn[0]["poly"], float)
                n = len(P) // 2
                wmin = float(np.min(P[n:][::-1, 0] - P[:n, 0]))
                ytop = float(P[:, 1].max())
                xc = float(P[:, 0].mean())
                col = int(round((xc / 1000.0 + 0.45) * ppm))
                r0 = int(round((1.4 - ytop / 1000.0) * ppm)) + 2
                r1 = int(round((1.4 - P[:, 1].min() / 1000.0) * ppm)) - 2
                frac = float((m[r0:r1, col] >= 0.5).mean()) if r1 > r0 else 0.0
                val = frac
                ok = wmin >= 80.0 and 900.0 <= ytop <= 1350.0 and frac >= 0.9
                det = "run %.2f m wide or more from %.2f m up, at 0.5 or more over %.0f per cent of its length (0.08 to 0.30 m, 0.9 to 1.35 m, 90 per cent)" % (wmin / 1000.0, ytop / 1000.0, 100 * frac)
            out.append(("algae_run", val, ok, det))
    elif kid == "poster_remnant":
        rim = [q for q in polys if q["role"] == "paste_rim"]
        ys_, xs_ = np.nonzero(m >= 0.2)
        if rim and len(ys_):
            per = 2.0 * ((xs_.max() - xs_.min() + 1) + (ys_.max() - ys_.min() + 1)) / ppm * 1000.0
            share = sum(q.get("length_mm", 0.0) for q in rim) / per
            out.append(("poster_rim", share, 0.25 <= share <= 0.65, "the paste ghost runs along %.0f per cent of the site's edge in %d pieces (30 to 60)" % (100 * share, len(rim))))
        f = poster_intact(variant)
        ys, xs = np.nonzero(m >= 0.2)
        if f is not None and len(ys):
            site = float((ys.max() - ys.min() + 1) * (xs.max() - xs.min() + 1))
            cov = float((m >= 0.5).sum()) / site
            out.append(("poster_intact", cov, abs(cov - f) <= 0.1, "%.2f of the site at 0.5 or more, the variant's intact fraction %.1f +/- 0.1" % (cov, f)))
        elif f is None:
            n = 0
            from scipy import ndimage as ndi
            lab, n = ndi.label(m >= 0.5)
            out.append(("poster_strips", n, 2 <= n <= 6, "%d strips (2 to 5, a tear may split one)" % n))
    elif kid == "render_patch" and variant == 4:
        from scipy import ndimage as ndi
        lab, n = ndi.label(m >= 0.5)
        out.append(("patch_pieces", n, 4 <= n <= 9, "%d separate losses (4 to 9)" % n))
    elif kid == "paint_flake" and variant in CRAZING_VARIANTS["paint_flake"]:
        from shapely.geometry import Polygon, Point
        from shapely.ops import unary_union
        cr = [Polygon(q["poly"]).buffer(0) for q in polys if q["role"] == "craquelure"]
        fl = [q for q in polys if q["role"] == "flake"]
        if cr and fl:
            near = unary_union(cr).buffer(4.0)
            on = sum(1 for q in fl if near.contains(Polygon(q["poly"]).buffer(0).centroid))
            share = on / float(len(fl))
            out.append(("flake_on_crack", share, share >= 0.5, "%.2f of the flakes centred within 4 mm of a crack (the review: 0.6)" % share))
    return out
