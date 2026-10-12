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
    """Continuous fades: every streak drawn by the target's module takes one slice per 5 mm of its length (the review's finding 3)."""
    if getattr(draw, "_ledger_streak_fixed", False):
        return
    orig = draw.streak

    def streak(rng, kind, x0, y0, w0, length, *a, slices=14, **k):
        return orig(rng, kind, x0, y0, w0, length, *a, slices=max(int(slices), int(math.ceil(float(length) / 5.0))), **k)
    draw.streak = streak
    draw._ledger_streak_fixed = True


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
    if f is None:
        return draw.kind_envelope(tj, kid, seed, variant)
    E = tj["kinds"][kid]["envelope"]
    rng = draw.rng_for(seed, "%s/%d" % (kid, variant))
    return f(draw, rng, kid, E, variant)


# ------------------------------------------------------------------------------------------ algae_downpipe (finding 1)
def algae(d, rng, kind, E, variant):
    out = []
    W, H = [v * 1000.0 for v in E["region_m"]]
    bl = E["blobs"]
    wb = rng.uniform(300.0, 650.0)                       # the patch on the shoe: 0.3 m wide or more (the rule's 0.9 m is past the target's own size check, eqd 450 mm)
    hb = wb * rng.uniform(0.45, 0.8)
    cx = rng.uniform(-100.0, 100.0)
    pts = d.blob(rng, cx, hb * 0.35, math.sqrt(wb * hb), hb / wb, math.pi / 2, n=26, rough=0.18)
    lv0 = d.uni(rng, [0.85, 1.0])
    out.append(d.poly(kind, lv0, pts, "blob"))
    n = d.uni_int(rng, bl["n"]) - 1
    top = hb * 0.85
    for i in range(max(0, n)):                            # the others overlap it and narrow upward
        w = wb * rng.uniform(0.3, 0.5) * (0.8 ** i)
        h = w * rng.uniform(1.2, 2.0)
        cy = top + h * rng.uniform(0.0, 0.25)
        bx = cx + rng.uniform(-0.2, 0.2) * wb
        out.append(d.poly(kind, d.uni(rng, [0.75, 0.95]), d.blob(rng, bx, cy, math.sqrt(w * h), h / w, math.pi / 2 + rng.normal(0, 0.1), n=22, rough=0.2), "blob"))
        top = cy + h * 0.35
    if variant != 3:                                      # moss in the joints near the patch (variant 3 has none: "joint moss on/off")
        p10, p50, p90 = 5.5, 10.2, 31.5
        reach = 150.0
        ys = np.arange(0.0, min(1200.0, top + reach), 75.0)
        cand = []
        for c, y in enumerate(ys):
            off = 0.0 if c % 2 == 0 else 107.5
            for x in np.arange(-W / 2 - off, W / 2, 215.0):
                cand.append((x + off, y))                 # a perpend's foot
            for x in np.linspace(-W / 2, W / 2, 24):
                cand.append((x, y))                       # along the bed joint
        cand = np.array(cand)
        # within 0.15 m of the patch: distance to the patch ellipse (approximated by the first blob's box, grown) and to the upper blobs' column
        near = (np.abs(cand[:, 0] - cx) <= wb / 2 + reach) & (cand[:, 1] <= top + reach)
        cand = cand[near]
        k = int(min(len(cand), rng.integers(18, 45)))
        if k:
            pick = cand[rng.choice(len(cand), k, replace=False)]
            for (x, y), e in zip(pick, d.lognormal3(rng, p10, p50, p90, k)):
                e = float(np.clip(e, 4.0, 45.0))
                horiz = rng.random() < 0.7
                asp = rng.uniform(1.5, 3.0)
                out.append(d.poly(kind, 0.75, d.blob(rng, x + rng.normal(0, 15), y + rng.normal(0, 3), e, asp, 0.0 if horiz else math.pi / 2, n=12, rough=0.3), "joint_moss"))
    rn = E.get("run")
    if rn and variant in (0, 2):                          # a run from a leaking joint: narrow at the joint, widening as it falls
        L = d.uni(rng, [v * 1000.0 for v in rn["length_m"]])
        L = min(L, H - 50.0)
        y0 = min(H - 20.0, max(top + 150.0, L))
        w0 = rng.uniform(30.0, 50.0)
        w1 = rng.uniform(100.0, 300.0)
        out += d.streak(rng, kind, cx + rng.uniform(-0.15, 0.15) * wb, y0, w0, min(L, y0), 0.02 * L, 1.0 - w1 / w0, 1.0, 0.7, 0.15, role="run")
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
    elif t == 4:                                          # a loss cluster: 4 to 9 losses (33 / 67 / 294 mm), no patch
        p10, p50, p90 = [v * 1000.0 for v in E["loss_blobs"]["eqd_m"]]
        n = int(rng.integers(4, 10))
        cx, cy = rng.uniform(-60, 60), rng.uniform(-80, 40)
        for e in d.lognormal3(rng, p10, p50, p90, n):
            e = float(np.clip(e, 30.0, 260.0))
            out.append(d.poly(kind, rng.uniform(0.85, 1.0), d.blob(rng, cx + rng.normal(0, 110), cy + rng.normal(0, 90), e, d.uni(rng, [1.0, 2.0]), rng.uniform(0, math.pi)), "loss"))
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
    rim = rng.uniform(10.0, 40.0)                          # the paste ghost: a rim at 0.25, 10 to 40 mm wide
    outer = ragged(d, rng, site, 6.0, 8)
    inner = [(x * (1 - 2 * rim / w), y * (1 - 2 * rim / h)) for x, y in outer]
    out.append(d.poly(kind, 0.25, outer + [outer[0]] + [inner[0]] + inner[::-1] + [inner[0]], "paste_rim"))
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
        for p in cut_by_tears(d, rng, rect, int(rng.integers(1, 3))):
            out.append(d.poly(kind, rng.uniform(0.6, 1.0), p, "layer"))
    return out


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
        else:
            cx0, cy0, an = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0, math.pi)
        bp = d.blob(rng, cx0, cy0, float(e), asp, an, n=14, rough=0.3)
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
        for dx in (-W, 0.0, W):
            for dy in (-H, 0.0, H):
                if (dx or dy) and not (-eq0 <= cx0 + dx <= W + eq0 and -eq0 <= cy0 + dy <= H + eq0):
                    continue
                out.append(d.poly(kind, 1.0, [(x + dx, y + dy) for x, y in bp], "sheet"))
    return out


# ------------------------------------------------------------------------------------------ checks: the target's, less the one a departure replaces, and the review's new ones
REPLACED = {("poster_remnant", "coverage_of_decal"): (None, "replaced by poster_intact: the target's 0.25 to 0.75 of the frame assumed one whole sheet; its own variants are 20 to 70 per cent intact"),
            ("render_patch", "coverage_of_decal"): ((5,), "not on variant 5, the target's own single replacement brick (0.215 x 0.065 m is 2.5 per cent of the 0.7 x 0.8 m frame; the check asks 10)")}


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
    elif kid == "poster_remnant":
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
