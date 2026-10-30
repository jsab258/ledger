"""A garment's rib bands built from its shell's own open ends, in place of the bands the cloth simulator draped:
each draped band's faces deleted and a new band lofted from the shell's ring it is sewn to.

    blender -b --factory-startup -P tools/meshgen/blender/build_rib_band.py -- DRAPE_UNPOSED.obj PLAN.json OUT.obj
        [--bands cuffL,cuffR,welt,neckband] [--clear 4.5] [--row 6] [--cuff-past 8] [--reach 160] [--welt-in 0.90]
        [--neck-in 0.92] [--weights-body F:/LedgerTools/bodies/MH_TomL1/MH_TomL1_Body.fbx]

WHY, 30 October 2026 (Tom's jumper, drape j3; the coordinator's ruling of the same day). The plan builds the welt, the
cuffs and the crew neckband to the body rather than draping them to fit (JUMPER-PLAN-2026-10-29.md). The jacket's
tool for that, tools/md/build_cuffs.py, keeps each draped cuff's faces and moves its points by the angles of its sewn
edge round the forearm, so it needs that edge to be a round ring: on the jumper's drapes Marvelous left a cuff as a
flat flap whose sewn edge went 191 degrees round the wrist, and the cuffs built from it came out 301 and 351 mm round
at the hand with points 22 mm inside the wrist (j2). The shell's own open ends (the sleeve's end, the hem, the
neckline) are round, so each band is made from them: its columns start at the shell ring's own points, its rows go
the band's height to a ring set by the body (the cuffs, the welt) or by the band's cut (the neckband).

HOW (Marvelous's millimetres, y up, the figure facing +z, the OBJ bent back to his reference pose):
- each piece's UVs are put back in pattern millimetres as tools/meshgen/blender/import_md_drape.py does (tile = the
  plan outline's box over the UV box); a ring is the shell's points on the edge the plan sews to the band, in order
  along that edge, and the band's column at a ring point takes the matching place along the band's sewn edge (the
  share of the edge's length, as Marvelous spreads a seam);
- THE CUFF (tools/md-bridge/cuff_measure.py's forearm axis and wrist, the narrowest cut): its lower edge --cuff-past mm
  past the wrist (the wrist's own girth, short of the hand's widening; the band's centre then within 30 mm of the
  wrist), its top the band's height up the forearm; the ring's turn round the forearm fitted to the drape's angles and
  each ring point set at its own share of the edge (a flap's ring made round), at the skin (the farthest skin in a 30
  degree wedge, as a tape bridges the tendons) plus --clear (the skin offset 3 mm and half the rib's thickness); the
  sleeve's last --reach mm of pattern rebuilt from its pattern up to the cuff's top and blended into the drape (KNOWN
  FAULT, 30 October, second try: the blend is made point by point in space, so where the drape's sleeve end is folded
  the blend crosses the arm: 2 centre-line crossings a sleeve 62 to 82 mm above the wrist, the body through it at 8
  and 17 points; to be blended along, round and out separately, over the reach's upper part only);
- THE WELT: each hem point's column straight down the band's height, drawn in round the trunk's own axis to --welt-in
  of the hem's radius at its lower edge (0.90: the plan's welt), never nearer the skin than --clear;
- THE NECKBAND: each neckline point's column up the neck's axis (fitted to the neck's own slab centres), drawn in to
  --neck-in of the neckline's radius at its top (0.92: the plan's band), its surface length the band's height;
- the band's pattern layer (its UVs) is its cut rectangle, x along the ring and y up the band, so the bake's rib
  ridges, drawn along the pattern's x, run across the band as wales do;
- weights (the record, not the skinning: skin_garment.py skins the game mesh later and is a script, not a module):
  each new point takes the body's skin weights at its nearest skin by Blender's data transfer (nearest face,
  interpolated), as tools/md/unpose_garment.py does; written per band to OUT_weights.json (the strongest bones, and
  the share of cuff points led by a hand or finger bone).
OUT.obj keeps every group (the body too, for the checks), the shell's faces and UVs as read (the sleeves' last reach
moved), the bands new; OUT_bands.json holds each band's rings and what was built.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(TOOLS, "md-bridge"))
import cuff_measure as cm  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
SRC, PLAN, DST = argv[:3]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
BANDS = opt("--bands", "cuffL,cuffR,welt,neckband", str).split(",")
CLEAR = opt("--clear", 4.5)
ROW = opt("--row", 6.0)
CUFF_PAST = opt("--cuff-past", 8.0)
REACH = opt("--reach", 160.0)
WELT_IN = opt("--welt-in", 0.90)
NECK_IN = opt("--neck-in", 0.92)
WEIGHTS_BODY = opt("--weights-body", "F:/LedgerTools/bodies/MH_TomL1/MH_TomL1_Body.fbx", str)

plan = json.load(open(PLAN, encoding="utf-8"))
P = {p["key"]: p for p in plan["pieces"]}
CORN = {k: {n: (x, y) for n, x, y in v} for k, v in plan["corners"].items()}

# ---- the OBJ, faces kept --------------------------------------------------------------------------------------
lines = open(SRC, encoding="utf-8", errors="replace").read().splitlines()
V, T, order, groups, mtl, cur = [], [], [], {}, {}, None
head = []
for line in lines:
    if line.startswith("v "):
        V.append([float(t) for t in line.split()[1:4]])
    elif line.startswith("vt "):
        T.append([float(t) for t in line.split()[1:3]])
    elif line.startswith("g "):
        cur = line[2:].strip()
        if cur not in groups:
            groups[cur] = []
            order.append(cur)
    elif line.startswith("usemtl ") and cur is not None:
        mtl[cur] = line
    elif line.startswith("f ") and cur is not None:
        f = []
        for t in line.split()[1:]:
            a = t.split("/")
            f.append((int(a[0]) - 1, int(a[1]) - 1 if len(a) > 1 and a[1] else -1))
        groups[cur].append(f)
    elif line.startswith("mtllib"):
        head.append(line)
V = np.array(V)
T = np.array(T)
body_key = next(k for k in groups if k.endswith("LOD0"))
body = V[sorted({i for f in groups[body_key] for i, _ in f})]


def tile_of(key):
    p = P[key]
    px = [x for x, _y, _t in p["points"]]
    py = [y for _x, y, _t in p["points"]]
    tis = sorted({t for f in groups[key] for _, t in f})
    us, vs = T[tis, 0], T[tis, 1]
    tile = ((max(px) - min(px)) / (us.max() - us.min()), (max(py) - min(py)) / (vs.max() - vs.min()))
    uc = ((us.max() + us.min()) / 2, (vs.max() + vs.min()) / 2)
    pc = ((max(px) + min(px)) / 2, (max(py) + min(py)) / 2)
    return tile, uc, pc


def pattern_of(key):
    tile, uc, pc = tile_of(key)
    out = {}
    for f in groups[key]:
        for i, t in f:
            out[i] = ((T[t, 0] - uc[0]) * tile[0] + pc[0], (T[t, 1] - uc[1]) * tile[1] + pc[1])
    return out


def edge_poly(key, k):
    pts = P[key]["points"]
    corners = [i for i, p in enumerate(pts) if p[2] == 0]
    i0, i1 = corners[k], corners[(k + 1) % len(corners)]
    idx = list(range(i0, i1 + 1)) if i1 > i0 else list(range(i0, len(pts))) + list(range(0, i1 + 1))
    return np.array([(pts[i][0], pts[i][1]) for i in idx])


def ring(shell, k, start_name):
    """The shell's points on its k-th plan edge, in order from the corner start_name: [(vertex, share along)]."""
    poly = edge_poly(shell, k)
    s0 = np.array(CORN[shell][start_name])
    if np.linalg.norm(poly[0] - s0) > np.linalg.norm(poly[-1] - s0):
        poly = poly[::-1]
    seg = np.linalg.norm(np.diff(poly, axis=0), axis=1)
    cum = np.r_[0.0, np.cumsum(seg)]
    pat = pattern_of(shell)
    ids = np.array(sorted(pat))
    q = np.array([pat[i] for i in ids])
    A, B = poly[:-1], poly[1:]
    d = B - A
    t = np.clip(((q[:, None, :] - A[None]) * d[None]).sum(2) / np.maximum((d * d).sum(1), 1e-12)[None], 0, 1)
    c = A[None] + t[..., None] * d[None]
    dist = np.sqrt(((q[:, None, :] - c) ** 2).sum(2))
    j = dist.argmin(1)
    on = dist.min(1) < 0.3
    share = (cum[j[on]] + t[on, j[on]] * seg[j[on]]) / cum[-1]
    o = np.argsort(share)
    return [(int(v), float(s)) for v, s in zip(ids[on][o], share[o])]


def seam_of(band, shell):
    for s in plan["seams"]:
        if s["a"][0] == band and s["b"][0] == shell:
            return s
    raise SystemExit("no seam %s to %s in the plan" % (band, shell))


def smoothstep(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def fit_angles(angles, shares):
    """The ring's angles as a0 + sgn * 2 pi * share (one turn), the sign and start fitted to the drape's own angles."""
    best = None
    for sgn in (1.0, -1.0):
        z = np.exp(1j * (np.array(angles) - sgn * 2 * math.pi * np.array(shares)))
        m = z.mean()
        if best is None or abs(m) > best[2]:
            best = (sgn, float(np.angle(m)), float(abs(m)))
    return best


moved = {}            # shell vertex: new place
new_bands = {}        # band piece: (points (n,3), uv pattern mm (n,2), triangles)
report = {"src": SRC, "plan": PLAN, "clear": CLEAR, "row": ROW, "bands": {}}


def grid(cols_xyz, cols_x, ys, yf):
    """A band's points, pattern and triangles from its columns: cols_xyz (ncol, nrow, 3), cols_x (ncol,)."""
    ncol, nrow = cols_xyz.shape[:2]
    pts = cols_xyz.reshape(-1, 3)
    uv = np.array([(cols_x[c], ys + (yf - ys) * r / (nrow - 1)) for c in range(ncol) for r in range(nrow)])
    tris = []
    for c in range(ncol - 1):
        for r in range(nrow - 1):
            a, b, cc, d = c * nrow + r, (c + 1) * nrow + r, (c + 1) * nrow + r + 1, c * nrow + r + 1
            tris += [(a, b, cc), (a, cc, d)]
    return pts, uv, tris


def outward(pts, tris, centre_of):
    """Triangles wound so their normals face away from the band's axis (centre_of(p): the axis point nearest p)."""
    votes = 0
    for a, b, c in tris[:: max(1, len(tris) // 200)]:
        n = np.cross(pts[b] - pts[a], pts[c] - pts[a])
        m = (pts[a] + pts[b] + pts[c]) / 3
        votes += 1 if n @ (m - centre_of(m)) > 0 else -1
    return tris if votes >= 0 else [(a, c, b) for a, b, c in tris]


# ---- THE CUFFS ------------------------------------------------------------------------------------------------
for cuff in [b for b in BANDS if b.startswith("cuff")]:
    s_ = cuff[-1]
    side = 1.0 if s_ == "L" else -1.0
    sleeve = "sleeve" + s_
    seam = seam_of(cuff, sleeve)
    a0, a1, b0, b1 = seam["names"]
    rg = ring(sleeve, seam["b"][1], b0)
    f = cm.forearm(body, side)
    H = abs(CORN[cuff][a0][1] - [y for n, (x, y) in CORN[cuff].items() if n not in (a0, a1)][0])
    s_low = CUFF_PAST
    s_top = s_low - H
    rel = lambda p: p - f["centre"]  # noqa: E731
    def polar(p):
        r_ = rel(p)
        return float(r_ @ f["axis"]), math.atan2(float(r_ @ f["w"]), float(r_ @ f["u"])), math.hypot(float(r_ @ f["u"]), float(r_ @ f["w"]))
    def place(s, a, r):
        return f["centre"] + f["axis"] * s + (f["u"] * math.cos(a) + f["w"] * math.sin(a)) * r
    def skin(s, a):
        x = cm.skin_radius(f["arm"], f, s, a)
        if math.isnan(x):
            for ds in (4, -4, 8, -8, 12, -12):
                x = cm.skin_radius(f["arm"], f, s + ds, a)
                if not math.isnan(x):
                    break
        return x
    # the ring's turn round the forearm fitted to the drape's own angles (its sign and start), each point then at
    # its own share of the edge, so a ring Marvelous folded into a flap comes out round
    angs = [polar(V[v])[1] for v, _ in rg]
    shares = [sh for _, sh in rg]
    sgn, a0_fit, conc = fit_angles(angs, shares)
    ang_at = lambda t: a0_fit + sgn * 2 * math.pi * t  # noqa: E731
    # THE SLEEVE'S LAST --reach mm OF PATTERN REBUILT FROM ITS PATTERN (second try, 30 October: the first drew the
    # drape's own sleeve end up the forearm, as build_cuffs.cut_sleeve does, and its folds came with it: 2 centre-line
    # crossings a sleeve, the body through it at 31 and 38 points, edges to 14.8 times their pattern). Each point of
    # that reach is placed from its pattern: its share across the sleeve's width there (from the plan's two underarm
    # edges) gives its angle as the ring's, its height above the wrist edge its place along the forearm, from the
    # cuff's top up to where the drape's sleeve is at the reach's end; at the skin plus the clearance at the cuff's top,
    # blended into the drape's own place over the reach (smoothly, so nothing steps where the drape takes over), and
    # never nearer the skin than the clearance.
    pat_s = pattern_of(sleeve)
    y_w = CORN[sleeve][b0][1]
    self_seam = next(x for x in plan["seams"] if x["a"][0] == sleeve and x["b"][0] == sleeve)
    pa_, pb_ = edge_poly(sleeve, self_seam["a"][1]), edge_poly(sleeve, self_seam["b"][1])
    c0 = np.array(CORN[sleeve][b0])
    near0 = lambda poly: min(np.linalg.norm(poly[0] - c0), np.linalg.norm(poly[-1] - c0))  # noqa: E731
    left, right = (pa_, pb_) if near0(pa_) < near0(pb_) else (pb_, pa_)
    def x_at(poly, y):
        o = np.argsort(poly[:, 1])
        return float(np.interp(y, poly[o, 1], poly[o, 0]))
    zone = [i for i, q in pat_s.items() if q[1] - y_w <= REACH + 1e-6]
    s_end = [polar(V[i])[0] for i, q in pat_s.items() if abs(q[1] - y_w - REACH) < 6.0]
    s_D = float(np.median(s_end))
    clamped = 0
    for i in zone:
        x, y = pat_s[i]
        d = max(0.0, y - y_w)
        xl, xr = x_at(left, y), x_at(right, y)
        t = min(1.0, max(0.0, (x - xl) / (xr - xl))) if abs(xr - xl) > 1e-6 else 0.0
        a = ang_at(t)
        sp = s_top + (s_D - s_top) * d / REACH
        p_param = place(sp, a, skin(sp, a) + CLEAR)
        w = smoothstep(d / REACH)
        p = p_param * (1 - w) + V[i] * w
        s_, a_, r_ = polar(p)
        fl = skin(s_, a_) + CLEAR
        if not math.isnan(fl) and r_ < fl:
            p = place(s_, a_, fl)
            clamped += 1
        moved[i] = p
    ring_new = {v: place(s_top, ang_at(sh), skin(s_top, ang_at(sh)) + CLEAR) for v, sh in rg}
    moved.update(ring_new)
    up = zone
    # the band: one column per ring point, rows down the forearm to the lower edge
    nrow = max(2, int(math.ceil(H / ROW)) + 1)
    xa, xb = CORN[cuff][a0][0], CORN[cuff][a1][0]
    ys = CORN[cuff][a0][1]
    yf = [y for n, (x, y) in CORN[cuff].items() if n not in (a0, a1)][0]
    cols, cx = [], []
    for v, sh in rg:
        a = ang_at(sh)
        col = [ring_new[v]]
        for r_i in range(1, nrow):
            s = s_top + (s_low - s_top) * r_i / (nrow - 1)
            col.append(place(s, a, skin(s, a) + CLEAR))
        cols.append(col)
        cx.append(xa + (xb - xa) * sh)
    pts, uv, tris = grid(np.array(cols), cx, ys, yf)
    tris = outward(pts, tris, lambda m: f["centre"] + f["axis"] * float((m - f["centre"]) @ f["axis"]))
    new_bands[cuff] = (pts, uv, tris)
    report["bands"][cuff] = {"ringPoints": len(rg), "rows": nrow, "wristGirthMm": round(f["girth"], 1),
                             "lowerEdgePastWristMm": s_low, "topPastWristMm": round(s_top, 1), "sleeveRebuilt": len(up), "sleeveReachTopMm": round(s_D, 1),
                             "sleeveClampedToSkin": clamped, "ringAngleFit": {"sign": sgn, "concentration": round(conc, 3)}}

# ---- THE WELT -------------------------------------------------------------------------------------------------
# (second try, 30 October: the first took the trunk's centre and skin from the body's vertices slab by slab, and the
# avatar's torso is sparse, about 50 points in 8 mm, so the centre jumped up to 50 mm between rows and the welt's lower
# edge came out twice its cut: now one upright axis through the hem's own centre, and the skin found by a ray from
# outside the trunk toward that axis, on the body's surface)
from mathutils import Vector  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402
bverts = sorted({i for f in groups[body_key] for i, _ in f})
bloc = {i: j for j, i in enumerate(bverts)}
body_bvh = BVHTree.FromPolygons([Vector(V[i]) for i in bverts], [[bloc[i] for i, _ in f] for f in groups[body_key]])


def trunk_radius(cx, cz, y, a, start=320.0):
    o = Vector((cx + start * math.cos(a), y, cz + start * math.sin(a)))
    hit = body_bvh.ray_cast(o, Vector((-math.cos(a), 0.0, -math.sin(a))), start)
    if hit[0] is None:
        return float("nan")
    return math.hypot(hit[0].x - cx, hit[0].z - cz)


if "welt" in BANDS:
    rings = {}
    for welt, shell in (("weltFront", "front"), ("weltBack", "back")):
        seam = seam_of(welt, shell)
        rings[welt] = (seam, ring(shell, seam["b"][1], seam["names"][2]))
    allp = V[[v for _, (_, rg) in rings.items() for v, _ in rg]]
    cx_, cz_ = float(allp[:, 0].mean()), float(allp[:, 2].mean())
    for welt, (seam, rg) in rings.items():
        a0, a1, b0, b1 = seam["names"]
        H = abs(CORN[welt][a0][1] - [y for n, (x, y) in CORN[welt].items() if n not in (a0, a1)][0])
        nrow = max(2, int(math.ceil(H / ROW)) + 1)
        xa, xb = CORN[welt][a0][0], CORN[welt][a1][0]
        ys = CORN[welt][a0][1]
        yf = [y for n, (x, y) in CORN[welt].items() if n not in (a0, a1)][0]
        cols, cx, clamp = [], [], 0
        for v, sh in rg:
            p0 = V[v]
            a = math.atan2(p0[2] - cz_, p0[0] - cx_)
            r0 = math.hypot(p0[0] - cx_, p0[2] - cz_)
            r1 = r0 * WELT_IN
            drop = math.sqrt(max(H * H - (r0 - r1) ** 2, 1.0))
            col = [p0.copy()]
            for r_i in range(1, nrow):
                h = r_i / (nrow - 1)
                y = p0[1] - drop * h
                r = r0 + (r1 - r0) * h
                fl = trunk_radius(cx_, cz_, y, a) + CLEAR
                if not math.isnan(fl) and r < fl:
                    r = fl
                    clamp += 1
                col.append(np.array([cx_ + r * math.cos(a), y, cz_ + r * math.sin(a)]))
            cols.append(col)
            cx.append(xa + (xb - xa) * sh)
        pts, uv, tris = grid(np.array(cols), cx, ys, yf)
        tris = outward(pts, tris, lambda m: np.array([cx_, m[1], cz_]))
        new_bands[welt] = (pts, uv, tris)
        report["bands"][welt] = {"ringPoints": len(rg), "rows": nrow, "pointsHeldOffSkin": clamp, "axis": [round(cx_, 1), round(cz_, 1)]}

# ---- THE NECKBAND -----------------------------------------------------------------------------------------------
if "neckband" in BANDS:
    # the neck's centre a little above the neckline (its slab between the throat and the nape, the chin left out:
    # above about 1,655 mm the slab takes the jaw), and the band drawn in toward the upright through it (over the
    # band's 28 mm the neck's forward lean moves its centre about 8 mm, left as it is)
    neck = body[(body[:, 1] > 1630) & (body[:, 1] < 1650) & (np.abs(body[:, 0]) < 85) & (body[:, 2] > -100) & (body[:, 2] < 65)]
    nc = np.array([(neck[:, 0].max() + neck[:, 0].min()) / 2, 1640.0, (neck[:, 2].max() + neck[:, 2].min()) / 2])
    nd = np.array([0.0, 1.0, 0.0])
    segs = [s for s in plan["seams"] if s["a"][0] == "neckband" and s["b"][0] != "neckband"]
    cols, cx = [], []
    for s in segs:
        a0, a1, b0, b1 = s["names"]
        rg = ring(s["b"][0], s["b"][1], b0)
        xa, xb = CORN["neckband"][a0][0], CORN["neckband"][a1][0]
        for v, sh in rg:
            x = xa + (xb - xa) * sh
            if cx and abs(x - cx[-1]) < 1e-6:
                continue                     # the shoulder's point shared by the front's and back's rings
            cols.append(v)
            cx.append(x)
    H = abs(CORN["neckband"]["nbTopStart"][1] - CORN["neckband"]["nbFrontL"][1])
    nrow = max(2, int(math.ceil(H / ROW)) + 1)
    ys, yf = CORN["neckband"]["nbFrontL"][1], CORN["neckband"]["nbTopStart"][1]
    grid_cols, inside_held = [], 0
    for v in cols:
        p0 = V[v]
        s0 = float((p0 - nc) @ nd)
        rho = (p0 - nc) - nd * s0
        r0 = float(np.linalg.norm(rho))
        e = rho / r0
        r1 = r0 * NECK_IN
        rise = math.sqrt(max(H * H - (r0 - r1) ** 2, 1.0))
        col = [p0.copy()]
        for r_i in range(1, nrow):
            h = r_i / (nrow - 1)
            col.append(nc + nd * (s0 + rise * h) + e * (r0 + (r1 - r0) * h))
        grid_cols.append(col)
    pts, uv, tris = grid(np.array(grid_cols), cx, ys, yf)
    tris = outward(pts, tris, lambda m: nc + nd * float((m - nc) @ nd))
    new_bands["neckband"] = (pts, uv, tris)
    report["bands"]["neckband"] = {"ringPoints": len(cols), "rows": nrow, "neckAxis": [round(float(x), 3) for x in nd]}

# ---- WRITTEN: the shell and body as read (the sleeves' reach moved), the bands new ------------------------------
rib_tile = next((tile_of(k)[0] for k in new_bands if groups.get(k)), (156.888, 156.888))
out = list(head)
vmap, tmap = {}, {}
nv = nt = 0
body_lines = []
for g in order:
    if g in new_bands:
        pts, uv, tris = new_bands[g]
        pc = ((min(x for n, (x, y) in CORN[g].items()) + max(x for n, (x, y) in CORN[g].items())) / 2,
              (min(y for n, (x, y) in CORN[g].items()) + max(y for n, (x, y) in CORN[g].items())) / 2)
        base_v, base_t = nv, nt
        for p in pts:
            out.append("v %.4f %.4f %.4f" % tuple(p))
            nv += 1
        for q in uv:
            out.append("vt %.6f %.6f" % ((q[0] - pc[0]) / rib_tile[0], (q[1] - pc[1]) / rib_tile[1]))
            nt += 1
        out.append("g " + g)
        if g in mtl:
            out.append(mtl[g])
        for a, b, c in tris:
            out.append("f %d/%d %d/%d %d/%d" % (base_v + a + 1, base_t + a + 1, base_v + b + 1, base_t + b + 1, base_v + c + 1, base_t + c + 1))
        continue
    fl = []
    for fc in groups[g]:
        idx = []
        for i, t in fc:
            if i not in vmap:
                p = moved.get(i, V[i])
                out.append("v %.4f %.4f %.4f" % tuple(p))
                nv += 1
                vmap[i] = nv
            if t >= 0 and t not in tmap:
                out.append("vt %.6f %.6f" % tuple(T[t]))
                nt += 1
                tmap[t] = nt
            idx.append("%d/%d" % (vmap[i], tmap[t]) if t >= 0 else "%d" % vmap[i])
        fl.append("f " + " ".join(idx))
    out.append("g " + g)
    if g in mtl:
        out.append(mtl[g])
    out += fl
open(DST, "w", encoding="utf-8").write("\n".join(out) + "\n")

# ---- THE WEIGHTS' RECORD ------------------------------------------------------------------------------------------
try:
    import bpy
    have_bpy = True
except ImportError:
    have_bpy = False
weights = {}
if have_bpy and os.path.isfile(WEIGHTS_BODY):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=WEIGHTS_BODY)
    wbody = max([o for o in bpy.data.objects if o.type == "MESH"], key=lambda o: len(o.data.vertices))
    for k, (pts, _uv, tris) in new_bands.items():
        me = bpy.data.meshes.new(k)
        me.from_pydata([(x / 1000.0, -z / 1000.0, y / 1000.0) for x, y, z in pts], [], tris)
        ob = bpy.data.objects.new(k, me)
        bpy.context.scene.collection.objects.link(ob)
        for gname in wbody.vertex_groups:
            ob.vertex_groups.new(name=gname.name)
        m = ob.modifiers.new("weights", "DATA_TRANSFER")
        m.object = wbody
        m.use_vert_data = True
        m.data_types_verts = {"VGROUP_WEIGHTS"}
        m.vert_mapping = "POLYINTERP_NEAREST"
        m.layers_vgroup_select_src = "ALL"
        m.layers_vgroup_select_dst = "NAME"
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.modifier_apply(modifier=m.name)
        names = [g.name for g in ob.vertex_groups]
        lead, tot = {}, {}
        handish = 0
        for v in ob.data.vertices:
            ws = sorted(((g.weight, names[g.group]) for g in v.groups if g.weight > 0), reverse=True)
            if not ws:
                continue
            lead[ws[0][1]] = lead.get(ws[0][1], 0) + 1
            for w, n in ws:
                tot[n] = tot.get(n, 0.0) + w
            if ws[0][1].startswith(("hand_", "thumb", "index", "middle", "ring", "pinky", "wrist")):
                handish += 1
        nvb = len(ob.data.vertices)
        weights[k] = {"points": nvb, "leadBone": dict(sorted(lead.items(), key=lambda x: -x[1])[:6]),
                      "weightShare": {n: round(w / nvb, 3) for n, w in sorted(tot.items(), key=lambda x: -x[1])[:6]},
                      "ledByHandOrFinger": handish}
    json.dump(weights, open(os.path.splitext(DST)[0] + "_weights.json", "w", encoding="utf-8"), indent=1)
report["weights"] = weights
json.dump(report, open(os.path.splitext(DST)[0] + "_bands.json", "w", encoding="utf-8"), indent=1)
print("BANDS", json.dumps(report))
