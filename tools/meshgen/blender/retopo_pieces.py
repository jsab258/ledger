"""A Marvelous Designer drape of any number of pieces made into an even game mesh: a grid laid on each flat pattern
piece, every seam sampled alike from both its pieces, lifted onto the drape and welded.

    blender -b --factory-startup -P tools/meshgen/blender/retopo_pieces.py -- SEWN.blend PLAN.json IMPORT.json OUT_DIR
        [--name zip_jacket] [--spacing 0.0115] [--elbow 1.6] [--taubin 12] [--weld 0.0005]

WHY, 27 October 2026 (Tom's zip jacket, the bake chain's steps 2 to 4: production/art/clothing/tom-outfit/
BAKE-PLAN-2026-10-27.md). tools/meshgen/blender/retopo_garment.py (30 September) does this for a five-piece jacket
found by where its islands lie and with its counts written out by hand (a shoulder, a side, an armhole...). The zip
jacket has thirteen pieces (fronts, back, sleeves, rib bands and cuffs, a stand collar, two zip tapes), so here the
pieces come from the importer's "piece" attribute (tools/meshgen/blender/import_md_drape.py), each piece's four patch
corners from the plan (zip_jacket.py's "patch" and "corners"), and the counts from a small solver: every seam run
one count, the same on both its pieces (they share its welded vertices), each piece's opposite sides equal in sum,
each count as near its length over --spacing as those rules allow. The grid on each piece, the lift and the weld are
retopo_garment.py's own (Tutte's map of the piece onto a rectangle, so no grid point falls outside it; the lift
through the pattern's triangles; points in the drape's holes averaged from their neighbours; Taubin's smoothing).

The drape here is a single sheet (Marvelous's cloth has no thickness), so all of it is the outer skin.

OUT_DIR gets NAME_low.blend (the game mesh "Low" beside the drape, the body and the armature; its "pattern" layer and
its "piece" attribute kept), retopo.json (the counts, each piece's grid, the checks) and three pictures.
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector
from mathutils.geometry import barycentric_transform, intersect_point_tri_2d
from mathutils.kdtree import KDTree

argv = sys.argv[sys.argv.index("--") + 1:]
SEWN, PLAN, IMPORT, OUT = argv[0], argv[1], argv[2], argv[3]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
NAME = opt("--name", "zip_jacket", str)
H = opt("--spacing", 0.0115)
ELBOW = opt("--elbow", 1.6)
os.makedirs(OUT, exist_ok=True)
plan = json.load(open(PLAN, encoding="utf-8"))
imp = json.load(open(IMPORT, encoding="utf-8"))
NAMES = [p["key"] for p in plan["pieces"]]
log = {"sewn": SEWN, "plan": PLAN, "spacing": H, "checks": {}}


def say(*a):
    print("RETOPO", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=SEWN)
drape = bpy.data.objects["Jacket"]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
J = lambda n: arm.matrix_world @ arm.pose.bones[n].head  # noqa: E731

sb = bmesh.new()
sb.from_mesh(drape.data)
sb.transform(drape.matrix_world)
sb.normal_update()
sb.faces.ensure_lookup_table()
sb.verts.ensure_lookup_table()
suv = sb.loops.layers.uv["pattern"]
play = sb.faces.layers.int["piece"]
panel_of_face = {f.index: NAMES[f[play]] for f in sb.faces}

# ---- the lift: each piece's triangles in the pattern, (a, b, c) there and (p, q, r) on the drape ----------------
tris = {n: [] for n in NAMES}
for f in sb.faces:
    n = panel_of_face[f.index]
    ls = f.loops
    for j in range(1, len(ls) - 1):
        a, b, c = ls[0], ls[j], ls[j + 1]
        if abs((b[suv].uv - a[suv].uv).cross(c[suv].uv - a[suv].uv)) < 1e-12:
            continue
        tris[n].append(((a[suv].uv.to_3d(), b[suv].uv.to_3d(), c[suv].uv.to_3d()), (a.vert.co.copy(), b.vert.co.copy(), c.vert.co.copy())))
tri_kd = {}
for n, ts in tris.items():
    kd = KDTree(len(ts))
    for j, (u3, _p) in enumerate(ts):
        kd.insert((u3[0] + u3[1] + u3[2]) / 3, j)
    kd.balance()
    tri_kd[n] = kd


def lift(panel, uv2):
    """The drape's point at this place in the piece's pattern (the nearest when it falls in a hole)."""
    q = Vector((uv2[0], uv2[1], 0.0))
    best, best_d = None, 1e9
    for _co, j, _d in tri_kd[panel].find_n(q, 32):
        (a, b, c), (p, r, s) = tris[panel][j]
        if intersect_point_tri_2d(q, a, b, c):
            x = barycentric_transform(q, a, b, c, p, r, s)
            if not any(math.isnan(t) for t in x):
                return x, True
        d = (q - (a + b + c) / 3).length
        if d < best_d:
            best_d, best = d, j
    (a, b, c), (p, r, s) = tris[panel][best]
    cands_ = []
    for x, y in ((a, b), (b, c), (c, a)):
        xy = y - x
        t = max(0.0, min(1.0, (q - x).dot(xy) / max(1e-12, xy.length_squared)))
        cands_.append(x + xy * t)
    qq = min(cands_, key=lambda z: (z - q).length)
    return barycentric_transform(qq, a, b, c, p, r, s), False


# ---- each piece's edge cut into runs: one seam (to another piece, or to itself) or one opening each --------------
def panel_runs(pname):
    corners = []
    for f in sb.faces:
        if panel_of_face[f.index] != pname:
            continue
        for lp in f.loops:
            ua, ub = lp[suv].uv, lp.link_loop_next[suv].uv
            matched, other = False, None
            for l2 in lp.edge.link_loops:
                if l2 is lp:
                    continue
                wa, wb = (l2[suv].uv, l2.link_loop_next[suv].uv) if l2.vert is lp.vert else (l2.link_loop_next[suv].uv, l2[suv].uv)
                if panel_of_face[l2.face.index] == pname and (ua - wa).length < 1e-5 and (ub - wb).length < 1e-5:
                    matched = True
                else:
                    other = panel_of_face[l2.face.index]
                    other = "self" if other == pname else other
            if not matched:
                corners.append((lp.vert, ua.copy(), lp.link_loop_next.vert, ub.copy(), other or "open"))
    key = lambda v, u: (v.index, round(u.x, 6), round(u.y, 6))  # noqa: E731
    nxt = {key(a, ua): (b, ub, kind, a, ua) for a, ua, b, ub, kind in corners}
    start = next(iter(nxt))
    cur, seq = start, []
    for _ in range(len(nxt)):
        b, ub, kind, a, ua = nxt[cur]
        seq.append((a, ua, b, ub, kind))
        cur = key(b, ub)
        if cur == start:
            break
    if len(seq) != len(nxt):
        raise SystemExit("RETOPO %s's edge is not one loop (%d of %d edges walked)" % (pname, len(seq), len(nxt)))
    runs = []
    for a, ua, b, ub, kind in seq:
        if runs and runs[-1]["kind"] == kind:
            runs[-1]["pts"].append((b, ub))
        else:
            runs.append({"kind": kind, "pts": [(a, ua), (b, ub)]})
    if len(runs) > 1 and runs[0]["kind"] == runs[-1]["kind"]:
        runs[0]["pts"] = runs[-1]["pts"][:-1] + runs[0]["pts"]
        runs.pop()
    for r in runs:
        r["len"] = sum((p[0].co - q[0].co).length for p, q in zip(r["pts"], r["pts"][1:]))
    return runs


# a plan corner's place in the pattern layer: millimetres in the plan, metres and the piece's layout offset here
def corner_uv(pname, cname):
    for n, x, y in plan["corners"][pname]:
        if n == cname:
            return Vector((x / 1000.0 + imp["pieces"][pname]["layoutOffsetM"], y / 1000.0))
    raise KeyError((pname, cname))


sides = {}
worst_end = 0.0
for pname in NAMES:
    runs = panel_runs(pname)
    # every run's ends are plan corners (checked); the patch corners cut the loop into its four sides
    allc = [corner_uv(pname, n) for n, _x, _y in plan["corners"][pname]]
    for r in runs:
        for _v, u in (r["pts"][0], r["pts"][-1]):
            worst_end = max(worst_end, min((u - c).length for c in allc))
    pc = plan["patch"][pname]
    want = {n: corner_uv(pname, n) for n in pc["bottom"] + pc["top"]}
    starts = [r["pts"][0][1] for r in runs]
    at = {n: min(range(len(runs)), key=lambda i: (starts[i] - u).length) for n, u in want.items()}
    for n, i in at.items():
        if (starts[i] - want[n]).length > 0.002:
            raise SystemExit("RETOPO %s: no run starts at its patch corner %s (nearest %.1f mm)" % (pname, n, 1000 * (starts[i] - want[n]).length))
    b0, b1 = at[pc["bottom"][0]], at[pc["bottom"][1]]
    m = len(runs)
    # the bottom side runs, in loop order, from the bottom corner whose next patch corner is the other bottom corner
    order = sorted(at.values())
    first = b0 if order[(order.index(b0) + 1) % 4] == b1 else b1
    rot = runs[first:] + runs[:first]
    cut = sorted((i - first) % m for i in at.values())
    sides[pname] = {"runs": rot, "bottom": rot[cut[0]:cut[1]], "s1": rot[cut[1]:cut[2]], "top": rot[cut[2]:cut[3]], "s3": rot[cut[3]:]}
    say("piece", pname, [(k, [(r["kind"], round(r["len"], 3)) for r in sides[pname][k]]) for k in ("bottom", "s1", "top", "s3")])
log["checks"]["runEndWorstMm"] = round(1000 * worst_end, 3)


# ---- the counts: one per run, shared across a seam, opposite sides equal ----------------------------------------
def var_of(pname, r):
    if r["kind"] == "open":
        return ("open", pname, id(r))
    return ("seam", frozenset(v.index for v, _u in r["pts"]))


target, appears = {}, {}
cons = []
for pname, sd in sides.items():
    for a, b in (("bottom", "top"), ("s1", "s3")):
        A = [var_of(pname, r) for r in sd[a]]
        B = [var_of(pname, r) for r in sd[b]]
        cons.append((pname, a, A, B))
        for v, r in zip(A + B, sd[a] + sd[b]):
            target[v] = r["len"] / H
            appears[v] = appears.get(v, 0) + 1
seam_vars = [v for v in target if v[0] == "seam"]
# MIRRORED RUNS ROUNDED ALIKE: the left and right halves' runs are separate seams of nearly the same length; rounded
# apart, the two zip tapes (sewn to each other) could never both balance. Each run's target is averaged with its
# mirror's (its midpoint mirrored across x = 0, the nearest run of the same kind within 3 cm and 10% in length).
mid = {}
for pname, sd in sides.items():
    for r in sd["runs"]:
        mid[var_of(pname, r)] = sum((v.co for v, _u in r["pts"]), Vector()) / len(r["pts"])
mirrored = 0
for v, c in mid.items():
    mc = Vector((-c.x, c.y, c.z))
    w = min((x for x in mid if x[0] == v[0]), key=lambda x: (mid[x] - mc).length)
    if w != v and (mid[w] - mc).length < 0.03 and abs(target[w] - target[v]) < 0.1 * max(target[v], 1):
        target[v] = target[w] = (target[v] + target[w]) / 2
        mirrored += 1
log["checks"]["mirroredRuns"] = mirrored
n_ = {v: max(1, int(round(t))) for v, t in target.items()}
adjusted = {v: 0 for v in target}
for v in target:
    if v[0] == "open" and target[v] * H < 0.02:
        n_[v] = 2                       # a tape's 12 mm end: two columns
for _round in range(200):
    bad = 0
    for pname, a, A, B in cons:
        d = sum(n_[v] for v in A) - sum(n_[v] for v in B)
        if d == 0:
            continue
        bad += 1
        # the most freely changed run: fewest constraints, then the longest (least distorted by one step)
        cand = sorted(set(A + B), key=lambda v: (appears[v], adjusted[v], -target[v]))
        for v in cand:
            want_ = n_[v] - d if v in A else n_[v] + d
            if want_ >= 1 and not (v[0] == "open" and target[v] * H < 0.02):
                n_[v] = want_
                adjusted[v] += 1
                break
    if bad == 0:
        break
viol = [(p, a) for p, a, A, B in cons if sum(n_[v] for v in A) != sum(n_[v] for v in B)]
log["checks"]["countRounds"] = _round + 1
log["checks"]["sidesUnequal"] = viol
if viol:
    raise SystemExit("RETOPO counts unsolved: %s" % viol)
paired = sum(1 for v in seam_vars if appears[v] >= 2)
log["checks"]["seamsShared"] = paired
log["checks"]["seamRuns"] = len(seam_vars)
log["checks"]["worstStretch"] = round(max(abs(n_[v] - target[v]) / max(target[v], 1) for v in target), 3)
tri_pred = sum(2 * sum(n_[var_of(p, r)] for r in sd["bottom"]) * sum(n_[var_of(p, r)] for r in sd["s1"]) for p, sd in sides.items())
log["checks"]["trianglesPredicted"] = tri_pred
say("counts solved in", _round + 1, "rounds; seam runs", len(seam_vars), "shared", paired, "triangles", tri_pred)

lower, upper, handj = J("lowerarm_l"), J("upperarm_l"), J("hand_l")
ELBOW_AT = (lower - upper).length / ((lower - upper).length + (handj - lower).length)


def warp(f):
    """Rows closer round the elbow (a sleeve's underarm, measured from the armpit)."""
    if ELBOW <= 1.0:
        return f
    xs = np.linspace(0, 1, 401)
    dens = 1.0 + (ELBOW - 1.0) * np.exp(-((xs - ELBOW_AT) / 0.09) ** 2)
    cum = np.concatenate([[0], np.cumsum((dens[1:] + dens[:-1]) / 2)])
    cum /= cum[-1]
    return float(np.interp(f, cum, xs))


def fracs(pname, side, r):
    n = n_[var_of(pname, r)]
    if pname.startswith("sleeve") and r["kind"] == "self":
        # s3 starts at the armpit (the top's end); s1 ends there
        from_start = side == "s3"
        fr = [warp(k / n) for k in range(n + 1)]
        return n, fr if from_start else [1 - warp(1 - k / n) for k in range(n + 1)]
    return n, [k / n for k in range(n + 1)]


def sample(pname, side, r):
    n, fr = fracs(pname, side, r)
    pts = r["pts"]
    seglen = [(p[0].co - q[0].co).length for p, q in zip(pts, pts[1:])]
    cum = np.concatenate([[0], np.cumsum(seglen)])
    total = cum[-1]
    seam = var_of(pname, r)
    flip = pts[0][0].index > pts[-1][0].index
    out = []
    for k, f in enumerate(fr):
        s = f * total
        j = min(len(seglen) - 1, int(np.searchsorted(cum, s, side="right") - 1))
        t = 0.0 if seglen[j] < 1e-12 else (s - cum[j]) / seglen[j]
        u = pts[j][1].lerp(pts[j + 1][1], t)
        key = ("v", pts[0 if k == 0 else -1][0].index) if k in (0, n) else ("s", seam, n - k if flip else k)
        out.append((Vector((u.x, u.y)), key))
    return out


def run_phi(r):
    pts = r["pts"]
    seglen = [(p[0].co - q[0].co).length for p, q in zip(pts, pts[1:])]
    cum = np.concatenate([[0], np.cumsum(seglen)])
    return cum / max(cum[-1], 1e-12)


# ---- the grid on each piece, through its map onto a rectangle (retopo_garment.py's) ---------------------------
grids, keys = {}, {}
off_map = 0
for pname, sd in sides.items():
    def chain(side):
        pts = []
        for r in sd[side]:
            sp = sample(pname, side, r)
            pts += sp if not pts else sp[1:]
        return pts
    Bk, Rk, Tk, Lk = chain("bottom"), chain("s1"), chain("top")[::-1], chain("s3")[::-1]
    B, R, T, Lf = ([p for p, _k in X] for X in (Bk, Rk, Tk, Lk))
    if len(B) != len(T) or len(R) != len(Lf):
        raise SystemExit("RETOPO the piece %s's opposite sides differ: %d/%d, %d/%d" % (pname, len(B), len(T), len(R), len(Lf)))
    nc, nr = len(B) - 1, len(R) - 1
    ukey = lambda v, u: (v.index, round(u.x, 6), round(u.y, 6))  # noqa: E731
    idx, uvs, ptris = {}, [], []
    for f in sb.faces:
        if panel_of_face[f.index] != pname:
            continue
        ids = []
        for lp in f.loops:
            kk = ukey(lp.vert, lp[suv].uv)
            if kk not in idx:
                idx[kk] = len(uvs)
                uvs.append((lp[suv].uv.x, lp[suv].uv.y))
            ids.append(idx[kk])
        for jj in range(1, len(ids) - 1):
            ptris.append((ids[0], ids[jj], ids[jj + 1]))
    uvs = np.array(uvs)
    npnt = len(uvs)
    rect = np.full((npnt, 2), np.nan)

    def place(side, fn):
        off = 0
        for r in sd[side]:
            n_r, fr_r = fracs(pname, side, r)
            fi = np.interp(run_phi(r), fr_r, np.arange(n_r + 1))
            for (v, u), f_ in zip(r["pts"], fi):
                kk = ukey(v, u)
                if kk in idx:
                    rect[idx[kk]] = fn(off + f_)
            off += n_r

    place("bottom", lambda f_: (f_, 0.0))
    place("s1", lambda f_: (nc, f_))
    place("top", lambda f_: (nc - f_, nr))
    place("s3", lambda f_: (0.0, nr - f_))
    fixed_b = ~np.isnan(rect[:, 0])
    ed = set()
    for t3 in ptris:
        for x_, y_ in ((t3[0], t3[1]), (t3[1], t3[2]), (t3[2], t3[0])):
            ed.add((min(x_, y_), max(x_, y_)))
    ed = np.array(sorted(ed))
    deg = np.bincount(ed.ravel(), minlength=npnt).astype(float)
    free = np.where(~fixed_b)[0]
    X = np.where(fixed_b[:, None], rect, 0.0)
    X[free] = np.nanmean(rect[fixed_b], axis=0)

    def lap(Y):
        out = deg[:, None] * Y
        np.subtract.at(out, ed[:, 0], Y[ed[:, 1]])
        np.subtract.at(out, ed[:, 1], Y[ed[:, 0]])
        return out

    Xb = np.where(fixed_b[:, None], X, 0.0)
    rhs = -lap(Xb)[free]
    Y = X[free].copy()

    def Aop(Yf):
        Z = np.zeros_like(X)
        Z[free] = Yf
        return lap(Z)[free]

    rr = rhs - Aop(Y)
    pp = rr.copy()
    rs_old = (rr * rr).sum(axis=0)
    for _it in range(4000):
        Ap = Aop(pp)
        alpha = rs_old / np.maximum((pp * Ap).sum(axis=0), 1e-30)
        Y += pp * alpha
        rr -= Ap * alpha
        rs_new = (rr * rr).sum(axis=0)
        if rs_new.max() < 1e-18:
            break
        pp = rr + pp * (rs_new / np.maximum(rs_old, 1e-30))
        rs_old = rs_new
    X[free] = Y
    rkd = KDTree(len(ptris))
    for ti, (a_, b_, c_) in enumerate(ptris):
        cc = (X[a_] + X[b_] + X[c_]) / 3
        rkd.insert((cc[0], cc[1], 0.0), ti)
    rkd.balance()
    G = [[None] * (nr + 1) for _ in range(nc + 1)]
    for i in range(nc + 1):
        G[i][0], G[i][nr] = B[i], T[i]
    for j in range(nr + 1):
        G[0][j], G[nc][j] = Lf[j], R[j]
    outside = 0
    for i in range(1, nc):
        for j in range(1, nr):
            q = Vector((i, j, 0.0))
            got, best = None, None
            for _c, ti, _d in rkd.find_n(q, 24):
                a_, b_, c_ = ptris[ti]
                A2, B2, C2 = (Vector((X[k_][0], X[k_][1], 0.0)) for k_ in (a_, b_, c_))
                if intersect_point_tri_2d(q, A2, B2, C2):
                    got = ti
                    break
                if best is None:
                    best = ti
            ti = got if got is not None else best
            outside += got is None
            a_, b_, c_ = ptris[ti]
            A2, B2, C2 = (Vector((X[k_][0], X[k_][1], 0.0)) for k_ in (a_, b_, c_))
            Ua, Ub, Uc = (Vector((uvs[k_][0], uvs[k_][1], 0.0)) for k_ in (a_, b_, c_))
            w3 = barycentric_transform(q, A2, B2, C2, Ua, Ub, Uc)
            G[i][j] = Vector((w3[0], w3[1]))
    K = {}
    for i in range(nc + 1):
        K[(i, 0)], K[(i, nr)] = Bk[i][1], Tk[i][1]
    for j in range(nr + 1):
        K[(0, j)], K[(nc, j)] = Lk[j][1], Rk[j][1]
    grids[pname], keys[pname] = G, K
    off_map += outside
    say("grid", pname, "%dx%d" % (nc, nr), "points off the map", outside)
log["grids"] = {p: [len(G) - 1, len(G[0]) - 1] for p, G in grids.items()}
log["checks"]["gridPointsOffMap"] = off_map

# ---- the lift, the pieces joined at their shared points, the smoothing -----------------------------------------
lb = bmesh.new()
puv = lb.loops.layers.uv.new("pattern")
pan_layer = lb.faces.layers.int.new("piece")
missed, shared, holes, npts, edge_miss = 0, {}, set(), 0, 0
edge_vs = set()
VG = {}
for pname, G in grids.items():
    nc, nr = len(G) - 1, len(G[0]) - 1
    V = [[None] * (nr + 1) for _ in range(nc + 1)]
    for i in range(nc + 1):
        for j in range(nr + 1):
            key = keys[pname].get((i, j))
            if key is not None and key in shared:
                V[i][j] = shared[key]
                edge_vs.add(V[i][j])
                continue
            p3, ok = lift(pname, G[i][j])
            npts += 1
            # A POINT ON THE PIECE'S OWN EDGE (a seam or an opening) that the triangle test misses by a hair is taken
            # where the clamp puts it, on the edge; only a point inside the piece that misses is a hole, averaged
            # from its neighbours (the first runs counted both: 1.06% "missed")
            edge_pt = i in (0, nc) or j in (0, nr)
            missed += not ok and not edge_pt
            edge_miss += not ok and edge_pt
            V[i][j] = lb.verts.new(p3)
            if edge_pt:
                edge_vs.add(V[i][j])
            if not ok and not edge_pt:
                holes.add(V[i][j])
            if key is not None:
                shared[key] = V[i][j]
    VG[pname] = V
    for i in range(nc):
        for j in range(nr):
            f = lb.faces.new((V[i][j], V[i + 1][j], V[i + 1][j + 1], V[i][j + 1]))
            f[pan_layer] = NAMES.index(pname)
            for lp, (a, b) in zip(f.loops, ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1))):
                lp[puv].uv = G[a][b]
for _ in range(opt("--hole-rounds", 60, int)):
    for v in holes:
        nb_ = [e.other_vert(v).co for e in v.link_edges]
        if nb_:
            v.co = sum(nb_, Vector()) / len(nb_)
log["checks"]["liftMissedShare"] = round(missed / max(npts, 1), 4)
log["checks"]["edgePointsClamped"] = edge_miss
n_before = len(lb.verts)
# THE WELD ON THE PIECES' EDGES ONLY (28 October 2026, drape 19: its right cuff is crumpled cloth, and two points inside
# that one piece were lifted within 0.5 mm of each other; welding them made a non-manifold edge. Seam partners are
# already shared by key, so only the pieces' own edges can need it; drape 6 welded 0 either way)
bmesh.ops.remove_doubles(lb, verts=[v for v in lb.verts if v in edge_vs], dist=opt("--weld", 0.0005))
log["checks"]["weldedAtSeams"] = n_before - len(lb.verts)
# THE ZIP'S TAPES HELD in the smoothing, like the openings (the first run: the 24 mm zip came out 27 mm wide)
held = {v for f in lb.faces if NAMES[f[pan_layer]].startswith("tape") for v in f.verts}
for _ in range(opt("--taubin", 12, int)):
    for lam in (0.5, -0.53):
        new_co = {}
        for v in lb.verts:
            if v.is_boundary or not v.link_edges or v in held:
                continue
            avg = sum((e.other_vert(v).co for e in v.link_edges), Vector()) / len(v.link_edges)
            new_co[v] = v.co + (avg - v.co) * lam
        for v, c in new_co.items():
            v.co = c
# ONE WINDING, FACING OUT (27 October: each piece's grid is wound as its pattern runs, so pieces disagreed and the
# zip's tapes faced in): made consistent across the sheet, then turned to face away from the garment's axis
bmesh.ops.recalc_face_normals(lb, faces=lb.faces[:])
lb.normal_update()
ax_ = sum((v.co for v in lb.verts), Vector()) / len(lb.verts)
votes_ = sum(1 if f.normal.dot(Vector((f.calc_center_median().x - ax_.x, f.calc_center_median().y - ax_.y, 0))) >= 0 else -1 for f in lb.faces)
if votes_ < 0:
    bmesh.ops.reverse_faces(lb, faces=lb.faces[:])
    lb.normal_update()
log["checks"]["facesOutwardShare"] = round(sum(1 for f in lb.faces if f.normal.dot(Vector((f.calc_center_median().x - ax_.x, f.calc_center_median().y - ax_.y, 0))) >= 0) / len(lb.faces), 3)
log["checks"]["triangles"] = 2 * len(lb.faces)
log["checks"]["nonManifoldEdges"] = sum(1 for e in lb.edges if len(e.link_faces) > 2)
bnd = {e for e in lb.edges if len(e.link_faces) == 1}
seen, loops = set(), 0
for e in bnd:
    if e in seen:
        continue
    loops += 1
    st = [e]
    while st:
        a = st.pop()
        if a in seen:
            continue
        seen.add(a)
        for v in a.verts:
            st += [x for x in v.link_edges if x in bnd and x not in seen]
log["checks"]["openings"] = loops
# THE ZIP'S WIDTH at ten heights (the plan's risk: smoothing narrowing the tapes): along each tape row, from the right
# tape's outer edge through the shared inner line to the left tape's outer edge (each tape's grid is 2 columns wide;
# its column 0 or 2 is the outer edge, whichever is not shared with the other tape)
if "tapeR" in VG and "tapeL" in VG:
    VR, VL = VG["tapeR"], VG["tapeL"]
    inner = {v for col in VR for v in col} & {v for col in VL for v in col}
    oR = VR[0] if VR[0][len(VR[0]) // 2] not in inner else VR[-1]
    oL = VL[0] if VL[0][len(VL[0]) // 2] not in inner else VL[-1]
    nrow = min(len(oR), len(oL))
    # the left tape's rows may run the other way: pair rows by height
    widths = []
    for k in range(1, 11):
        a = oR[int(k * (nrow - 1) / 11)]
        b = min(oL, key=lambda v: abs(v.co.z - a.co.z))
        widths.append(round(1000 * (a.co - b.co).length, 1))
    log["checks"]["zipWidthMm"] = widths

me = bpy.data.meshes.new("Low")
lb.to_mesh(me)
lb.free()
low = bpy.data.objects.new("Low", me)
bpy.context.scene.collection.objects.link(low)
mats = {}
for p in plan["pieces"]:
    mats.setdefault(p["fabric"], None)
for name_ in ("Shell", "Rib", "Tape"):
    me.materials.append(bpy.data.materials.get(name_) or bpy.data.materials.new(name_))
fab_mat = {"shell": 0, "rib": 1, "tape": 2}
attr = me.attributes["piece"]
for poly, a_ in zip(me.polygons, attr.data):
    poly.material_index = fab_mat[plan["pieces"][a_.value]["fabric"]]
drape.hide_render = True
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_low.blend"))

# THREE PICTURES of the game mesh on the body (Workbench, its wire over its shading), front, back and side
scn = bpy.context.scene
scn.render.engine = "BLENDER_WORKBENCH"
scn.display.shading.light = "STUDIO"
scn.display.shading.show_object_outline = False
scn.render.resolution_x, scn.render.resolution_y = 900, 1100
wire = low.modifiers.new("wire", "WIREFRAME")
wire.thickness = 0.0008
wire.use_replace = False
cam_d = bpy.data.cameras.new("cam")
cam_d.type = "ORTHO"
cam_d.ortho_scale = 0.95
cam = bpy.data.objects.new("cam", cam_d)
scn.collection.objects.link(cam)
scn.camera = cam
cz = sum((low.matrix_world @ Vector(c)).z for c in low.bound_box) / 8
for nm, loc, rot in (("front", (0, -3, cz), (math.pi / 2, 0, 0)), ("back", (0, 3, cz), (math.pi / 2, 0, math.pi)),
                     ("side", (3, 0, cz), (math.pi / 2, 0, math.pi / 2))):
    cam.location, cam.rotation_euler = loc, rot
    scn.render.filepath = os.path.join(OUT, "%s_low_%s.png" % (NAME, nm))
    bpy.ops.render.render(write_still=True)

log["ok"] = (not log["checks"]["sidesUnequal"] and log["checks"]["nonManifoldEdges"] == 0
             and 18000 <= log["checks"]["triangles"] <= 22000 and log["checks"]["liftMissedShare"] < 0.005)
json.dump(log, open(os.path.join(OUT, "retopo.json"), "w", encoding="utf-8"), indent=1)
print("RETOPO done", json.dumps(log["checks"]))
