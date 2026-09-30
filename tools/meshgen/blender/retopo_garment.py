"""A finished garment made into a game mesh: an even grid laid on its flat pattern pieces, lifted onto the drape,
the drape's detail baked into textures.

    blender -b -P tools/meshgen/blender/retopo_garment.py -- GARMENT.blend OUT_DIR --name ron_donkey [options]

WHY, 30 September (Jafar, after an outside audit: "one properly skinned jacket: shape, retopology, skinning, joint
weights corrected, only loose parts simulated"; the eased sewn jacket's second blind review failed on its back yoke,
a separate shell lying millimetres over the wool, which a renderer shows as navy tearing through the black:
production/art/clothing/donkey-jacket-skinned/eased-review-2.md). Games do not hand over the dense drape: it is the
shape and the source of the bake, and the game mesh is a new, even surface laid over it. The way garment artists
lay it (production/research/clothing-pipeline/RETOPOLOGY-AND-SKINNING-2026-09-30.md): on the flat pattern pieces,
a grid of four-sided faces on each, the same number of points on both sides of every seam, lifted onto the drape
through the pattern (Blender's own remesher is not for anything that bends). So:

1. THE SHAPE: the render mesh (--render), a closed wool solid with pieces on it; its outer skin is taken by
   following the surface from the front of the chest and stopping where it turns sharply (--crease degrees; the
   rim at the openings turns about 90).
2. THE PATTERN: the sewn garment (--sewn), whose "pattern" UV layer is its flat pieces at true size (a back, two
   fronts, two sleeves), tells each piece's edges: which are sewn to which piece and which are open (the hem, the
   neck, the cuffs). Each piece is a four-sided patch (bottom: the hem or cuff; its sides; its top: the shoulders
   and neck, or the sleeve's head), filled with a grid (--spacing metres; the sleeve's rows closer at the elbow,
   --elbow), every seam sampled once so both pieces share its points.
3. THE LIFT: each grid point found on the eased drape's outer skin through the same pattern layer, the pieces
   joined at their shared points.
4. THE HEM LENGTHENED (--hem-drop metres; two reviewers found it 5 to 8 cm short of the references) by rows
   continuing the skirt's own fall, and every opening turned in (--thick, then --lip up inside) so it reads as
   cloth with a thickness.
5. THE PIECES KEPT AS GEOMETRY: the collar (a doubled solid) and the buttons, seated on the new surface
   (--even-buttons spaces them evenly). The yoke, the patch pockets and the front edge's strip are baked, not
   modelled, so no two surfaces can fight: the yoke is a region of the one surface's colour.
6. THE UVs: "pattern" is the flat pieces themselves (one island a piece, which the builder's binder reads);
   "UVMap" is the same pieces packed into one texture square.
7. THE LOOSE PART marked for cloth: a vertex colour "SimMaxDistance" (0 skinned, 1 free to --sim-max metres)
   rising from --sim-below to the hem, for Unreal's VertexColorToAttribute node.
8. THE BAKE (Cycles on the processor, --tex pixels square): the drape's colour and its detail as a normal map;
   the normal map also written for Unreal (its green channel flipped).

OUT_DIR gets NAME_static.fbx (the game mesh, unskinned, on the body it was made on), NAME_basecolor.png,
NAME_normal_dx.png (and _gl), NAME.blend and retopo.json.
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform, intersect_point_tri_2d
from mathutils.kdtree import KDTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, OUT = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "garment", str)
RENDER = opt("--render", "JacketRender", str)
SEWN = opt("--sewn", "Jacket", str)
CREASE = opt("--crease", 50.0)
H = opt("--spacing", 0.018)
H_ARM = opt("--armhole-spacing", 0.022)
ELBOW = opt("--elbow", 1.6)
HEM_DROP = opt("--hem-drop", 0.0)
LIP = opt("--lip", 0.012)
THICK = opt("--thick", 0.004)
TEX = opt("--tex", 2048, int)
SIM_BELOW, SIM_MAX = opt("--sim-below", 0.0), opt("--sim-max", 0.08)
log = {"blend": BLEND, "name": NAME, "spacing": H}


def say(*a):
    print("RETOPO", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=BLEND)
hi = bpy.data.objects[RENDER]
sewn = bpy.data.objects[SEWN]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = next(o for o in bpy.data.objects if o.type == "MESH" and "Body" in o.name)
bb = bmesh.new()
bb.from_mesh(body.data)
bb.transform(body.matrix_world)
bb.normal_update()
BODY_BVH = BVHTree.FromBMesh(bb)
J = lambda n: arm.matrix_world @ arm.pose.bones[n].head  # noqa: E731


def uv_islands(bm, uv, faces=None):
    """Each face's island: faces joined across an edge whose two sides carry the same pattern coordinates."""
    faces = list(bm.faces) if faces is None else faces
    member = {f.index for f in faces}
    isl = {}
    k = 0
    for f in faces:
        if f.index in isl:
            continue
        isl[f.index] = k
        st = [f]
        while st:
            x = st.pop()
            for lp in x.loops:
                va, ua, ub = lp.vert, lp[uv].uv, lp.link_loop_next[uv].uv
                for l2 in lp.edge.link_loops:
                    y = l2.face
                    if y is x or y.index in isl or y.index not in member:
                        continue
                    wa, wb = (l2[uv].uv, l2.link_loop_next[uv].uv) if l2.vert is va else (l2.link_loop_next[uv].uv, l2[uv].uv)
                    if (ua - wa).length < 1e-5 and (ub - wb).length < 1e-5:
                        isl[y.index] = k
                        st.append(y)
        k += 1
    return isl, k


def name_panels(bm, uv, isl, k):
    """A jacket's five pieces, by where they lie in the pattern: sleeve, front, back, front, sleeve."""
    mean_u = []
    for i in range(k):
        us = [lp[uv].uv.x for f in bm.faces if isl.get(f.index) == i for lp in f.loops]
        mean_u.append((sum(us) / len(us), len(us), i))
    big = sorted(mean_u, key=lambda r: -r[1])[:5]
    order = [r[2] for r in sorted(big)]
    return dict(zip(order, ["sleeve_r", "front_r", "back", "front_l", "sleeve_l"]))


# ---- 1. the drape: its pieces, and its outer skin ------------------------------------------------------------
hb = bmesh.new()
hb.from_mesh(hi.data)
hb.transform(hi.matrix_world)
hb.normal_update()
hb.faces.ensure_lookup_table()
hb.verts.ensure_lookup_table()
comp = [-1] * len(hb.faces)
for f0 in hb.faces:
    if comp[f0.index] >= 0:
        continue
    comp[f0.index] = f0.index
    st = [f0]
    while st:
        f = st.pop()
        for e in f.edges:
            for f2 in e.link_faces:
                if comp[f2.index] < 0:
                    comp[f2.index] = f0.index
                    st.append(f2)
pieces = {}
for f in hb.faces:
    pieces.setdefault(comp[f.index], []).append(f)
mat_names = [m.name if m else "" for m in hi.data.materials]


def piece_mat(fs):
    return mat_names[fs[0].material_index] if fs[0].material_index < len(mat_names) else ""


def centre(fs):
    return sum((f.calc_center_median() for f in fs), Vector()) / len(fs)


wool = [k for k in pieces if "Wool" in piece_mat(pieces[k])]
main = max(wool, key=lambda k: len(pieces[k]))
buttons = [k for k in pieces if "Button" in piece_mat(pieces[k])]
small_wool = [k for k in wool if k != main]
collar = max(small_wool, key=lambda k: centre(pieces[k]).z) if small_wool else None
log["pieces"] = {"main": len(pieces[main]), "collar": len(pieces[collar]) if collar is not None else 0,
                 "buttons": len(buttons), "bakedOnly": [len(pieces[k]) for k in pieces if k not in (main, collar) and k not in buttons]}
say("pieces", json.dumps(log["pieces"]))
cands = [f for f in pieces[main] if abs(f.calc_center_median().x) < 0.04 and f.normal.y < -0.85]
seed = min(cands, key=lambda f: abs(f.calc_center_median().z - 1.2) + f.calc_center_median().y)
lim = math.cos(math.radians(CREASE))
outer = {seed.index}
st = [seed]
while st:
    f = st.pop()
    for e in f.edges:
        for f2 in e.link_faces:
            if f2.index not in outer and f2.normal.dot(f.normal) > lim:
                outer.add(f2.index)
                st.append(f2)
skin_faces = [hb.faces[i] for i in sorted(outer)]
say("outer skin", len(skin_faces), "faces of", len(pieces[main]))
huv = hb.loops.layers.uv["pattern"]
hisl, hk = uv_islands(hb, huv, skin_faces)
hnames = name_panels(hb, huv, hisl, hk)
# each piece's triangles in the pattern, for the lift: (a, b, c) in the pattern, (p, q, r) on the drape
tris = {n: [] for n in hnames.values()}
for f in skin_faces:
    n = hnames.get(hisl[f.index])
    if n is None:
        continue
    ls = f.loops
    for j in range(1, len(ls) - 1):
        a, b, c = ls[0], ls[j], ls[j + 1]
        if abs((b[huv].uv - a[huv].uv).cross(c[huv].uv - a[huv].uv)) < 1e-10:
            continue                                     # flat in the pattern (a rim's faces): no place on it
        tris[n].append(((a[huv].uv.to_3d(), b[huv].uv.to_3d(), c[huv].uv.to_3d()), (a.vert.co.copy(), b.vert.co.copy(), c.vert.co.copy())))
tri_kd = {}
for n, ts in tris.items():
    kd = KDTree(len(ts))
    for j, (u3, _p) in enumerate(ts):
        kd.insert((u3[0] + u3[1] + u3[2]) / 3, j)
    kd.balance()
    tri_kd[n] = kd
log["liftTriangles"] = {n: len(ts) for n, ts in tris.items()}


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
        # the nearest triangle, with the point pulled onto it
        cen = (a + b + c) / 3
        d = (q - cen).length
        if d < best_d:
            best_d, best = d, j
    (a, b, c), (p, r, s) = tris[panel][best]
    # clamp: the closest point on the triangle's edges
    cands_ = []
    for x, y in ((a, b), (b, c), (c, a)):
        xy = y - x
        t = max(0.0, min(1.0, (q - x).dot(xy) / max(1e-12, xy.length_squared)))
        cands_.append(x + xy * t)
    qq = min(cands_, key=lambda z: (z - q).length)
    return barycentric_transform(qq, a, b, c, p, r, s), False


# ---- 2. the pattern: its pieces, their edges, the grid on each ----------------------------------------------
sb = bmesh.new()
sb.from_mesh(sewn.data)
sb.transform(sewn.matrix_world)
sb.faces.ensure_lookup_table()
suv = sb.loops.layers.uv["pattern"]
sisl, sk = uv_islands(sb, suv)
snames = name_panels(sb, suv, sisl, sk)
panel_of_face = {f.index: snames[sisl[f.index]] for f in sb.faces if sisl[f.index] in snames}


def panel_runs(pname):
    """The piece's edge, in order round it, cut into runs: each run one seam (to another piece, or to itself for a
    sleeve's underarm) or one opening; each run a list of (vertex, pattern point)."""
    corners = []
    for f in sb.faces:
        if panel_of_face.get(f.index) != pname:
            continue
        for lp in f.loops:
            ua, ub = lp[suv].uv, lp.link_loop_next[suv].uv
            matched, other = False, None
            for l2 in lp.edge.link_loops:
                if l2 is lp:
                    continue
                wa, wb = (l2[suv].uv, l2.link_loop_next[suv].uv) if l2.vert is lp.vert else (l2.link_loop_next[suv].uv, l2[suv].uv)
                if panel_of_face.get(l2.face.index) == pname and (ua - wa).length < 1e-5 and (ub - wb).length < 1e-5:
                    matched = True
                else:
                    other = panel_of_face.get(l2.face.index)
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
        r["v"] = sum(u.y for _v, u in r["pts"]) / len(r["pts"])
    return runs


panels = {n: panel_runs(n) for n in snames.values()}
# each run's part in the garment
for pname, runs in panels.items():
    opens = sorted([r for r in runs if r["kind"] == "open"], key=lambda r: r["v"])
    if pname.startswith("sleeve"):
        opens[0]["role"] = "cuff"
        for r in runs:
            if r["kind"] == "self":
                r["role"] = "under"
            elif r["kind"] == "back":
                r["role"] = "cap_back"
            elif r["kind"].startswith("front"):
                r["role"] = "cap_front"
    else:
        opens[0]["role"] = "hem"
        for r in opens[1:]:
            r["role"] = "neck"
        for r in runs:
            if r["kind"].startswith("sleeve"):
                r["role"] = "arm_" + ("b" if pname == "back" else "f")
            elif r["kind"].startswith("front") and pname.startswith("front"):
                r["role"] = "cf"
        seams = [r for r in runs if "role" not in r]
        for r in seams:
            r["role"] = "side" if r["len"] > 0.4 else "sh"
    say("piece", pname, [(r["role"], r["kind"], round(r["len"], 3)) for r in runs])
roles = {}
for runs in panels.values():
    for r in runs:
        roles.setdefault(r["role"], []).append(r["len"])
L = {k: sum(v) / len(v) for k, v in roles.items()}
# the counts: every seam the same on both its pieces, left and right alike, each piece's opposite sides equal
n_ = lambda length, h=H: max(2, int(round(length / h)))  # noqa: E731
C = {"sh": n_(L["sh"]), "side": n_(L["side"]), "arm_b": n_(L["arm_b"], H_ARM), "arm_f": n_(L["arm_f"], H_ARM),
     "under": n_(L["under"])}
C["cuff"] = C["arm_b"] + C["arm_f"]
C["cf"] = C["arm_f"] + C["side"]
necks = sorted(roles["neck"])
L_neck_f, L_neck_b = (necks[0], necks[-1]) if len(necks) >= 3 else (necks[0], necks[0])
hems = sorted(roles["hem"])
L_hem_f, L_hem_b = hems[0], hems[-1]
C["neck_b"] = max(4, n_((L_hem_b + 2 * L["sh"] + L_neck_b) / 2) - 2 * C["sh"])
C["hem_b"] = 2 * C["sh"] + C["neck_b"]
C["neck_f"] = max(3, n_((L_hem_f + L["sh"] + L_neck_f) / 2) - C["sh"])
C["hem_f"] = C["sh"] + C["neck_f"]
log["counts"] = C
say("counts", json.dumps(C))
lower = J("lowerarm_l")
upper = J("upperarm_l")
handj = J("hand_l")
ELBOW_AT = (lower - upper).length / ((lower - upper).length + (handj - lower).length)


def count_of(pname, r):
    ro = r["role"]
    if ro == "hem":
        return C["hem_b"] if pname == "back" else C["hem_f"]
    if ro == "neck":
        return C["neck_b"] if pname == "back" else C["neck_f"]
    return C[{"cap_back": "arm_b", "cap_front": "arm_f"}.get(ro, ro)]


def warp(f):
    """Rows closer round the elbow (a sleeve's underarm, measured from the armpit)."""
    if ELBOW <= 1.0:
        return f
    xs = np.linspace(0, 1, 401)
    dens = 1.0 + (ELBOW - 1.0) * np.exp(-((xs - ELBOW_AT) / 0.09) ** 2)
    cum = np.concatenate([[0], np.cumsum((dens[1:] + dens[:-1]) / 2)])
    cum /= cum[-1]
    return float(np.interp(f, cum, xs))


def sample(pname, r, runs):
    """The run's points: n+1 places along it by length on the garment, each as this piece's pattern point."""
    n = count_of(pname, r)
    pts = r["pts"]
    seglen = [(p[0].co - q[0].co).length for p, q in zip(pts, pts[1:])]
    cum = np.concatenate([[0], np.cumsum(seglen)])
    total = cum[-1]
    if r["role"] == "under":
        # measured from the armpit end: the end that meets the sleeve's head
        i = runs.index(r)
        prev_role = runs[i - 1]["role"]
        from_start = prev_role.startswith("cap")
        fr = [warp(k / n) for k in range(n + 1)]
        fr = fr if from_start else [1 - warp(1 - k / n) for k in range(n + 1)]
    else:
        fr = [k / n for k in range(n + 1)]
    seam = frozenset(v.index for v, _u in pts) if r["kind"] != "open" else (pname, id(r))
    flip = pts[0][0].index > pts[-1][0].index
    out = []
    for k, f in enumerate(fr):
        s = f * total
        j = min(len(seglen) - 1, int(np.searchsorted(cum, s, side="right") - 1))
        t = 0.0 if seglen[j] < 1e-12 else (s - cum[j]) / seglen[j]
        u = pts[j][1].lerp(pts[j + 1][1], t)
        if k == 0 or k == n:
            key = ("v", pts[0 if k == 0 else -1][0].index)
        else:
            key = ("s", seam, n - k if flip else k)
        out.append((Vector((u.x, u.y)), key))
    return out


TOP = {"sh", "neck", "cap_back", "cap_front"}
BOTTOM = {"hem", "cuff"}
grids, keys = {}, {}
for pname, runs in panels.items():
    ib = next(i for i, r in enumerate(runs) if r["role"] in BOTTOM)
    rot = runs[ib + 1:] + runs[:ib]
    bottom = runs[ib]
    it = [i for i, r in enumerate(rot) if r["role"] in TOP]
    s1, top, s3 = rot[:it[0]], rot[it[0]:it[-1] + 1], rot[it[-1] + 1:]

    def chain(rs):
        pts = []
        for r in rs:
            sp = sample(pname, r, runs)
            pts += sp if not pts else sp[1:]
        return pts

    Bk = sample(pname, bottom, runs)
    Rk = chain(s1)
    Tk = chain(top)[::-1]
    Lk = chain(s3)[::-1]
    B, R, T, Lf = ([p for p, _k in X] for X in (Bk, Rk, Tk, Lk))
    if len(B) != len(T) or len(R) != len(Lf):
        raise SystemExit("RETOPO the piece %s's opposite sides differ: %d/%d, %d/%d" % (pname, len(B), len(T), len(R), len(Lf)))
    nc, nr = len(B) - 1, len(R) - 1

    def arcpar(ps):
        d = [0.0] + [(b - a).length for a, b in zip(ps, ps[1:])]
        c = np.cumsum(d)
        return c / c[-1]

    sB, sT, tL, tR = arcpar(B), arcpar(T), arcpar(Lf), arcpar(R)
    c0, c1, c2, c3 = B[0], B[-1], T[-1], T[0]
    G = [[None] * (nr + 1) for _ in range(nc + 1)]
    for i in range(nc + 1):
        for j in range(nr + 1):
            t = float(tL[j] + tR[j]) / 2
            s = float(sB[i] + sT[i]) / 2
            G[i][j] = ((1 - t) * B[i] + t * T[i] + (1 - s) * Lf[j] + s * R[j]
                       - ((1 - s) * (1 - t) * c0 + s * (1 - t) * c1 + (1 - s) * t * c3 + s * t * c2))
    # folded faces (a concave edge can fold a Coons patch): the inside eased by Laplacian until none
    def folded():
        sgn = []
        for i in range(nc):
            for j in range(nr):
                a, b, c, d = G[i][j], G[i + 1][j], G[i + 1][j + 1], G[i][j + 1]
                sgn.append((b - a).cross(d - a) + (d - c).cross(b - c))
        pos = sum(1 for x in sgn if x > 0)
        return min(pos, len(sgn) - pos)

    nf = folded()
    rounds = 0
    while nf and rounds < 200:
        for _ in range(5):
            for i in range(1, nc):
                for j in range(1, nr):
                    G[i][j] = (G[i - 1][j] + G[i + 1][j] + G[i][j - 1] + G[i][j + 1]) / 4
        rounds += 5
        nf = folded()
    K = {}
    for i in range(nc + 1):
        K[(i, 0)], K[(i, nr)] = Bk[i][1], Tk[i][1]
    for j in range(nr + 1):
        K[(0, j)], K[(nc, j)] = Lk[j][1], Rk[j][1]
    grids[pname] = G
    keys[pname] = K
    say("grid", pname, "%dx%d" % (nc, nr), "folded", nf, "eased rounds", rounds)
log["grids"] = {p: [len(G) - 1, len(G[0]) - 1] for p, G in grids.items()}

# ---- 3. the lift, and the pieces joined ------------------------------------------------------------------------
lb = bmesh.new()
puv = lb.loops.layers.uv.new("pattern")
pan_layer = lb.faces.layers.int.new("panel")
extra_layer = lb.faces.layers.int.new("extra")          # 1: made here, nothing of the drape under it
PANELS = ["back", "front_l", "front_r", "sleeve_l", "sleeve_r"]
over_layer = lb.faces.layers.int.new("overlap")        # 1: the front's overlapping edge strip (painted above the opening)
missed = 0
shared = {}
VG = {}
for pname, G in grids.items():
    nc, nr = len(G) - 1, len(G[0]) - 1
    V = [[None] * (nr + 1) for _ in range(nc + 1)]
    for i in range(nc + 1):
        for j in range(nr + 1):
            key = keys[pname].get((i, j))
            if key is not None and key in shared:
                V[i][j] = shared[key]
                continue
            p3, ok = lift(pname, G[i][j])
            missed += not ok
            V[i][j] = lb.verts.new(p3)
            if key is not None:
                shared[key] = V[i][j]
    VG[pname] = V
    for i in range(nc):
        for j in range(nr):
            f = lb.faces.new((V[i][j], V[i + 1][j], V[i + 1][j + 1], V[i][j + 1]))
            f[pan_layer] = PANELS.index(pname)
            if pname == "front_r" and i == 0:
                f[over_layer] = 1
            for lp, (a, b) in zip(f.loops, ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1))):
                lp[puv].uv = G[a][b]
nan = sum(1 for v in lb.verts if any(math.isnan(t) for t in v.co))
if nan:
    raise SystemExit("RETOPO %d lifted points have no position" % nan)
say("lifted; points in the drape's holes (taken from the nearest place)", missed)
log["liftMissed"] = missed
n_before = len(lb.verts)
bmesh.ops.remove_doubles(lb, verts=lb.verts[:], dist=opt("--weld", 0.0005))
say("joined at the seams", n_before, "->", len(lb.verts), "points")


def boundary_loops(bm):
    adj = {}
    for e in bm.edges:
        if e.is_boundary:
            a, b = e.verts
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
    seen, loops = set(), []
    for v0 in adj:
        if v0 in seen:
            continue
        loop, cur = [v0], v0
        seen.add(v0)
        while True:
            nx = [w for w in adj[cur] if w not in seen]
            if not nx:
                break
            cur = nx[0]
            seen.add(cur)
            loop.append(cur)
        loops.append(loop)
    return loops


openings = boundary_loops(lb)
log["openings"] = sorted(len(L_) for L_ in openings)
say("openings", log["openings"], "non-manifold edges", sum(1 for e in lb.edges if len(e.link_faces) > 2))


def face_outward(bm):
    """Faces turned to point away from the body."""
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.normal_update()
    score = 0.0
    for f in bm.faces:
        if f.index % 7 == 0:
            c = f.calc_center_median()
            h = BODY_BVH.find_nearest(c)[0]
            if h is not None:
                score += f.normal.dot((c - h).normalized())
    if score < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
        bm.normal_update()


lb.faces.ensure_lookup_table()
face_outward(lb)


def copy_uv(new_faces, src_of, offset_of):
    """New faces made along an edge: each corner takes the pattern point its source corner has in the face across
    the old edge, moved by offset_of (a new point's source is the point it was made from)."""
    for f in new_faces:
        old_edge = None
        for e in f.edges:
            if all(v not in src_of for v in e.verts):
                old_edge = e
        across = None
        if old_edge is not None:
            across = next((g for g in old_edge.link_faces if g is not f), None)
        if across is None:
            continue
        f[pan_layer] = across[pan_layer]
        f[extra_layer] = 1
        uv_at = {lp.vert: lp[puv].uv.copy() for lp in across.loops}
        for lp in f.loops:
            v = lp.vert
            if v in uv_at:
                lp[puv].uv = uv_at[v]
            elif v in src_of and src_of[v] in uv_at:
                lp[puv].uv = uv_at[src_of[v]] + offset_of.get(v, Vector((0, 0)))


# the hem lengthened: rows continuing the skirt's fall, the pattern continued below the hem
hem_src = {}
if HEM_DROP > 0:
    hem = min(boundary_loops(lb), key=lambda L_: sum(v.co.z for v in L_) / len(L_))
    hem_set = set(hem)
    edges = [e for e in lb.edges if e.is_boundary and all(v in hem_set for v in e.verts)]
    rows = max(1, int(round(HEM_DROP / 0.025)))
    for _ in range(rows):
        rim = {v for e in edges for v in e.verts}
        fall = {}
        for v in rim:
            up = [e2.other_vert(v) for e2 in v.link_edges if not e2.is_boundary]
            d = (v.co - up[0].co) if up else Vector((0, 0, -1))
            d.z = min(d.z, -1e-4)
            fall[v] = (d.normalized() * 0.6 + Vector((0, 0, -0.4))).normalized()
        res = bmesh.ops.extrude_edge_only(lb, edges=edges)
        src_of, off = {}, {}
        for v in (g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)):
            s = next((e2.other_vert(v) for e2 in v.link_edges if e2.other_vert(v) in rim), None)
            if s is not None:
                v.co = s.co + fall[s] * (HEM_DROP / rows)
                src_of[v] = s
                off[v] = Vector((0, -HEM_DROP / rows))
        copy_uv([g for g in res["geom"] if isinstance(g, bmesh.types.BMFace)], src_of, off)
        hem_src.update(src_of)
        edges = [g for g in res["geom"] if isinstance(g, bmesh.types.BMEdge) and all(x in src_of for x in g.verts)]
    say("hem lengthened", HEM_DROP, "m in", rows, "rows")
    face_outward(lb)
# THE FRONT OPENS BELOW ITS LAST BUTTON (the first review: "No picture shows a front edge or opening below the last
# button. If the skirt is a closed tube, the cloth has to stretch round both thighs instead of parting"): a man's
# jacket laps left over right, its left front's edge about 2 cm to his right of the buttons; the mesh is cut along
# that line (the right front's first line of points from the centre) from --open-below (default: 2.5 cm under the
# lowest button) down through the hem, so the two fronts part over the thighs. Above it, the same line is painted
# as the overlapping front's edge (the "overlap" faces).
if "--no-open" not in argv and "front_r" in VG:
    btn_z = [centre(pieces[k]).z for k in buttons]
    open_z = opt("--open-below", (min(btn_z) - 0.025) if btn_z else 1.0)
    col = [VG["front_r"][1][j] for j in range(len(VG["front_r"][1]))]
    chain = [v for v in col if v.is_valid]
    chain.sort(key=lambda v: v.co.z)
    below = [v for v in chain if v.co.z < open_z]
    # down through the hem's new rows
    nxt = {s_: n_ for n_, s_ in hem_src.items()}
    cur = below[0] if below else None
    ext = []
    while cur is not None and cur in nxt:
        cur = nxt[cur]
        ext.append(cur)
    line = ext[::-1] + below
    if below:
        line.append(next(v for v in chain if v.co.z >= open_z))
    cut = []
    for a, b in zip(line, line[1:]):
        e = next((e for e in a.link_edges if e.other_vert(a) is b), None)
        if e is not None:
            cut.append(e)
    if cut:
        bmesh.ops.split_edges(lb, edges=cut)
    for f in lb.faces:
        if f[over_layer] and f.calc_center_median().z < open_z:
            f[over_layer] = 0
    log["frontOpening"] = {"belowZ": round(open_z, 3), "edgesCut": len(cut)}
    say("the front opened below", round(open_z, 3), "m:", len(cut), "edges")
# every opening turned in: by --thick towards the body, then --lip up inside
if LIP > 0:
    bnd = [e for e in lb.edges if e.is_boundary]
    rim = {v for e in bnd for v in e.verts}
    vn = {v: v.normal.copy() for v in rim}
    up_in = {}
    for v in rim:
        ins = [e2.other_vert(v) for e2 in v.link_edges if not e2.is_boundary]
        up_in[v] = (ins[0].co - v.co).normalized() if ins else Vector((0, 0, 1))
    res = bmesh.ops.extrude_edge_only(lb, edges=bnd)
    ring1 = {}
    for v in (g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)):
        s = next((e2.other_vert(v) for e2 in v.link_edges if e2.other_vert(v) in rim), None)
        if s is not None:
            v.co = s.co - vn[s] * THICK
            ring1[v] = s
    copy_uv([g for g in res["geom"] if isinstance(g, bmesh.types.BMFace)], ring1, {})
    bnd2 = [g for g in res["geom"] if isinstance(g, bmesh.types.BMEdge) and all(x in ring1 for x in g.verts)]
    res2 = bmesh.ops.extrude_edge_only(lb, edges=bnd2)
    ring2 = {}
    for v in (g for g in res2["geom"] if isinstance(g, bmesh.types.BMVert)):
        s = next((e2.other_vert(v) for e2 in v.link_edges if e2.other_vert(v) in ring1), None)
        if s is not None:
            v.co = s.co + up_in[ring1[s]] * LIP
            ring2[v] = s
    copy_uv([g for g in res2["geom"] if isinstance(g, bmesh.types.BMFace)], ring2, {})
    face_outward(lb)
lo_me = bpy.data.meshes.new(NAME)
lb.to_mesh(lo_me)
lb.free()
lo = bpy.data.objects.new(NAME, lo_me)
bpy.context.scene.collection.objects.link(lo)
for p in lo.data.polygons:
    p.use_smooth = True
log["faces"] = len(lo.data.polygons)
log["tris"] = sum(len(p.vertices) - 2 for p in lo.data.polygons)
say("game mesh", log["faces"], "faces", log["tris"], "triangles", sum(1 for p in lo.data.polygons if len(p.vertices) == 4), "quads")

# ---- 5. the pieces kept as geometry: the collar and the buttons --------------------------------------------
kept = ([collar] if collar is not None and "--no-collar" not in argv else []) + sorted(buttons, key=lambda k: -centre(pieces[k]).z)
pbm = bmesh.new()
vm = {}
kept_mat, kept_of = [], []
# the collar smoothed by one level of subdivision (--collar-subd; the drape's collar is coarse and showed its facets)
if collar in kept and opt("--collar-subd", 1, int) > 0:
    cb = bmesh.new()
    cvm = {}
    for f in pieces[collar]:
        vs = []
        for v in f.verts:
            if v.index not in cvm:
                cvm[v.index] = cb.verts.new(v.co)
            vs.append(cvm[v.index])
        try:
            cb.faces.new(vs)
        except ValueError:
            pass
    cme = bpy.data.meshes.new("_collar")
    cb.to_mesh(cme)
    cb.free()
    cob = bpy.data.objects.new("_collar", cme)
    bpy.context.scene.collection.objects.link(cob)
    sm = cob.modifiers.new("Subd", "SUBSURF")
    sm.levels = opt("--collar-subd", 1, int)
    ev = cob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    em_ = ev.to_mesh()
    base = len(pbm.verts)
    for v in em_.vertices:
        pbm.verts.new(v.co)
    pbm.verts.ensure_lookup_table()
    for p_ in em_.polygons:
        pbm.faces.new([pbm.verts[base + i] for i in p_.vertices])
        kept_mat.append(mat_names[pieces[collar][0].material_index])
        kept_of.append(collar)
    ev.to_mesh_clear()
    bpy.data.objects.remove(cob, do_unlink=True)
    kept_rest = [k for k in kept if k != collar]
else:
    kept_rest = kept
for k in kept_rest:
    for f in pieces[k]:
        vs = []
        for v in f.verts:
            if v.index not in vm:
                vm[v.index] = pbm.verts.new(v.co)
            vs.append(vm[v.index])
        try:
            pbm.faces.new(vs)
        except ValueError:
            continue
        kept_mat.append(mat_names[f.material_index])
        kept_of.append(k)
pbm.faces.index_update()
pbm.verts.index_update()
pbm.faces.ensure_lookup_table()
# the buttons: evenly spaced between the top and the bottom one (--even-buttons; a reviewer measured 12, 14 and
# 17 cm), and each seated on the new surface (on the drape they sat on the front strip, which is now baked)
LO_BVH = BVHTree.FromObject(lo, bpy.context.evaluated_depsgraph_get())
btn_groups = {}
for f in pbm.faces:
    if kept_of[f.index] in buttons:
        btn_groups.setdefault(kept_of[f.index], set()).update(f.verts)
btn_groups = list(btn_groups.values())


def vcentre(vs):
    return sum((v.co for v in vs), Vector()) / len(vs)


if btn_groups and "--even-buttons" in argv:
    zs = [vcentre(g).z for g in btn_groups]
    top_z, bot_z = max(zs), min(zs)
    for j, g in enumerate(sorted(btn_groups, key=lambda g: -vcentre(g).z)):
        dz = top_z + (bot_z - top_z) * j / max(1, len(btn_groups) - 1) - vcentre(g).z
        for v in g:
            v.co.z += dz
for g in btn_groups:
    c = vcentre(g)
    q, n, _i, _d = LO_BVH.find_nearest(c)
    if q is None:
        continue
    back = min((v.co - q).dot(n) for v in g)
    shift = n * (opt("--button-gap", 0.001) - back)
    for v in g:
        v.co += shift
pc_me = bpy.data.meshes.new(NAME + "_pieces")
pbm.to_mesh(pc_me)
pbm.free()
pc = bpy.data.objects.new(NAME + "_pieces", pc_me)
bpy.context.scene.collection.objects.link(pc)
log["buttonsEven"] = "--even-buttons" in argv

# ---- 6. materials and UVs -------------------------------------------------------------------------------------
lm = lo.data
wool_mat = bpy.data.materials.new("M_" + NAME)
lm.materials.append(wool_mat)
btn_src = next((m for m in hi.data.materials if m and "Button" in m.name), None)
lm.materials.append(btn_src or tailor.material("M_Button", (0.02, 0.02, 0.025), 0.5))
for m in lm.materials:
    pc.data.materials.append(m)
for p in pc.data.polygons:
    p.material_index = 1 if "Button" in kept_mat[p.index] else 0
    p.use_smooth = True
pa = pc.data.attributes.new("panel", "INT", "FACE")
for i in range(len(pc.data.polygons)):
    pa.data[i].value = len(PANELS)                       # a kept piece, not a pattern piece
bpy.ops.object.select_all(action="DESELECT")
pc.select_set(True)
lo.select_set(True)
bpy.context.view_layer.objects.active = lo
bpy.ops.object.join()
lm = lo.data
# "UVMap" (first, the texture's) starts as the flat pieces; the kept pieces are unwrapped into it; "pattern"
# keeps the flat pieces unpacked; then "UVMap" is packed into one square
lm.uv_layers["pattern"].name = "UVMap"
lm.uv_layers.active_index = 0
panel_attr = [d.value for d in lm.attributes["panel"].data]
bpy.context.scene.tool_settings.use_uv_select_sync = True
bpy.ops.object.mode_set(mode="EDIT")
em = bmesh.from_edit_mesh(lm)
em.faces.ensure_lookup_table()
for f in em.faces:
    f.select_set(panel_attr[f.index] == len(PANELS))
bmesh.update_edit_mesh(lm)
bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.004, scale_to_bounds=False)
bpy.ops.object.mode_set(mode="OBJECT")
pat = lm.uv_layers.new(name="pattern")
src = lm.uv_layers["UVMap"]
for i in range(len(src.data)):
    pat.data[i].uv = src.data[i].uv
lm.uv_layers.active_index = 0
lm.uv_layers["UVMap"].active_render = True
bpy.context.scene.tool_settings.use_uv_select_sync = True
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.select_all(action="SELECT")
bpy.ops.uv.pack_islands(rotate=True, margin=0.004)
bpy.ops.object.mode_set(mode="OBJECT")
counts = {}
for v in panel_attr:
    k = PANELS[v] if v < len(PANELS) else "kept"
    counts[k] = counts.get(k, 0) + 1
log["faceCounts"] = counts
say("faces by piece", json.dumps(counts))

# ---- 7. the loose part marked for cloth ---------------------------------------------------------------------
if SIM_BELOW > 0:
    hem_z = min(v.co.z for v in lm.vertices)
    ca = lm.color_attributes.new(name="SimMaxDistance", type="FLOAT_COLOR", domain="POINT")
    for i, v in enumerate(lm.vertices):
        t = 0.0
        if v.co.z < SIM_BELOW:
            t = (SIM_BELOW - v.co.z) / max(1e-6, SIM_BELOW - hem_z)
            t = t * t * (3 - 2 * t)
        ca.data[i].color = (t, t, t, 1.0)
    log["simMaxDistance"] = {"below": SIM_BELOW, "hemZ": round(hem_z, 3), "maxM": SIM_MAX}

# ---- 8. the bake --------------------------------------------------------------------------------------------
# The colour is the wool's, the yoke painted from its own pattern piece (its outline on the flat pattern, so its
# edge is clean: baked from the drape's yoke shell, its ragged sides at the armholes came through); the normal map
# is the drape's detail (the pockets, the front's strip, the folds, softened), with the yoke's edge raised on it.
scn = bpy.context.scene
scn.render.engine = "CYCLES"
scn.cycles.device = "CPU"
scn.cycles.samples = opt("--bake-samples", 4, int)
scn.render.bake.use_selected_to_active = True
scn.render.bake.use_cage = False
scn.render.bake.cage_extrusion = opt("--cage", 0.008)
scn.render.bake.max_ray_distance = opt("--ray", 0.0)
scn.render.bake.margin = 8
wool_mat.use_nodes = True
nt = wool_mat.node_tree
bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")


def new_image(label_, float_buffer=False, colour=True):
    im = bpy.data.images.new(NAME + label_, TEX, TEX, alpha=False, float_buffer=float_buffer)
    if not colour:
        im.colorspace_settings.name = "Non-Color"
    return im


def only_selected(*objs):
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)


def glow(mats, on):
    """Every material of the source made to glow white (to find where rays land), or put back."""
    out = []
    for m in mats:
        b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if m and m.use_nodes else None
        if b is None:
            continue
        if on:
            out.append((b, tuple(b.inputs["Emission Color"].default_value), b.inputs["Emission Strength"].default_value))
            b.inputs["Emission Color"].default_value = (1, 1, 1, 1)
            b.inputs["Emission Strength"].default_value = 1.0
    return out


def unglow(saved_):
    for b, col_, s_ in saved_:
        b.inputs["Emission Color"].default_value = col_
        b.inputs["Emission Strength"].default_value = s_


def blur(a, sigma):
    if sigma <= 0:
        return a
    r = int(math.ceil(3 * sigma))
    k = np.exp(-(np.arange(-r, r + 1) / sigma) ** 2 / 2)
    k /= k.sum()
    a = np.apply_along_axis(lambda x: np.convolve(np.pad(x, r, mode="edge"), k, mode="valid"), 0, a)
    return np.apply_along_axis(lambda x: np.convolve(np.pad(x, r, mode="edge"), k, mode="valid"), 1, a)


# the buttons are not baked: their material gets a small image of its own for the bake to write to
bt = lm.materials[1]
bt.use_nodes = True
dummy = bpy.data.images.new("_button_bake", 8, 8)
bn = bt.node_tree.nodes.new("ShaderNodeTexImage")
bn.image = dummy
bt.node_tree.nodes.active = bn
yoke_key = max((k for k in pieces if "Yoke" in piece_mat(pieces[k])), key=lambda k: len(pieces[k]), default=None)

# (a) the normal map's source: the drape without its yoke shell, its faces turned outward, the wool's small
# creases softened (--bake-smooth rounds)
src_bm = bmesh.new()
src_bm.from_mesh(hi.data)
src_bm.faces.ensure_lookup_table()
def piece_height(k):
    zz = [v.co.z for f in pieces[k] for v in f.verts]
    return max(zz) - min(zz)


strips = [k for k in small_wool if k != collar and piece_height(k) > 0.4]
pockets = [k for k in small_wool if k != collar and k not in strips]
drop = {yoke_key} | set(strips)
bmesh.ops.delete(src_bm, geom=[f for f in src_bm.faces if comp[f.index] in drop], context="FACES")
src_bm.faces.ensure_lookup_table()
src_comp = [comp[i] for i in range(len(comp)) if comp[i] not in drop]
POCKET_LIFT = opt("--pocket-lift", 0.003)
if POCKET_LIFT > 0:
    lift_vs = {v for f, c_ in zip(src_bm.faces, src_comp) if c_ in pockets for v in f.verts}
    for v in lift_vs:
        w_ = hi.matrix_world @ v.co
        h_, n_, _i, _d = BODY_BVH.find_nearest(w_)
        if h_ is not None:
            v.co += hi.matrix_world.inverted().to_3x3() @ ((w_ - h_).normalized() * POCKET_LIFT)
log["bakeLeftOut"] = {"frontStrips": len(strips), "pocketsLifted": len(pockets)}
bmesh.ops.recalc_face_normals(src_bm, faces=[f for f, c_ in zip(src_bm.faces, src_comp) if c_ == main])
src_bm.normal_update()
src_bm.transform(hi.matrix_world)
flip = []
for f, c_ in zip(src_bm.faces, src_comp):
    if c_ != main:
        cc = f.calc_center_median()
        h_ = BODY_BVH.find_nearest(cc)[0]
        if h_ is not None and f.normal.dot(cc - h_) < 0:
            flip.append(f)
bmesh.ops.reverse_faces(src_bm, faces=flip)
wool_vs = list({v for f, c_ in zip(src_bm.faces, src_comp) if c_ == main for v in f.verts})
for _ in range(opt("--bake-smooth", 8, int)):
    bmesh.ops.smooth_vert(src_bm, verts=wool_vs, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
src_me = bpy.data.meshes.new(RENDER + "_bake")
src_bm.to_mesh(src_me)
src_bm.free()
for m in hi.data.materials:
    src_me.materials.append(m)
hib = bpy.data.objects.new(RENDER + "_bake", src_me)
bpy.context.scene.collection.objects.link(hib)
img_n = new_image("_normal", colour=False)
img_m = new_image("_hit", float_buffer=True, colour=False)
node_n = nt.nodes.new("ShaderNodeTexImage")
node_n.image = img_n
node_m = nt.nodes.new("ShaderNodeTexImage")
node_m.image = img_m
only_selected(hib, lo)
bpy.context.view_layer.objects.active = lo
saved = glow(hib.data.materials, True)
nt.nodes.active = node_m
bpy.ops.object.bake(type="EMIT")
unglow(saved)
nt.nodes.active = node_n
bpy.ops.object.bake(type="NORMAL", normal_space="TANGENT")
hit = np.array(img_m.pixels[:]).reshape(TEX, TEX, 4)[:, :, 0] > 0.5

# (b) the yoke's place on the texture: its pattern piece laid flat, and the game mesh laid flat on its own pattern,
# the flat yoke baked onto the flat mesh
yb = bmesh.new()
if yoke_key is not None:
    for f in pieces[yoke_key]:
        vs = [yb.verts.new((lp[huv].uv.x, lp[huv].uv.y, 0.0)) for lp in f.loops]
        try:
            yb.faces.new(vs)
        except ValueError:
            pass
yme = bpy.data.meshes.new("_yoke_flat")
yb.to_mesh(yme)
yb.free()
yflat = bpy.data.objects.new("_yoke_flat", yme)
bpy.context.scene.collection.objects.link(yflat)
white = bpy.data.materials.new("_white")
white.use_nodes = True
wb = next(n for n in white.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
wb.inputs["Emission Color"].default_value = (1, 1, 1, 1)
wb.inputs["Emission Strength"].default_value = 1.0
yme.materials.append(white)
fb = bmesh.new()
pat_l = lm.uv_layers["pattern"].data
map_uv = fb.loops.layers.uv.new("UVMap")
pan_vals = [d.value for d in lm.attributes["panel"].data]
for p_ in lm.polygons:
    far = pan_vals[p_.index] >= len(PANELS)
    vs = [fb.verts.new((pat_l[li].uv.x, pat_l[li].uv.y, 5.0 if far else 0.0)) for li in p_.loop_indices]
    f = fb.faces.new(vs)
    for lp, li in zip(f.loops, p_.loop_indices):
        lp[map_uv].uv = lm.uv_layers["UVMap"].data[li].uv
    f.material_index = 0
fme = bpy.data.meshes.new("_lo_flat")
fb.to_mesh(fme)
fb.free()
lflat = bpy.data.objects.new("_lo_flat", fme)
bpy.context.scene.collection.objects.link(lflat)
flat_mat = bpy.data.materials.new("_flat")
flat_mat.use_nodes = True
img_y = new_image("_yoke", float_buffer=True, colour=False)
ny = flat_mat.node_tree.nodes.new("ShaderNodeTexImage")
ny.image = img_y
flat_mat.node_tree.nodes.active = ny
fme.materials.append(flat_mat)
only_selected(yflat, lflat)
bpy.context.view_layer.objects.active = lflat
scn.render.bake.cage_extrusion = 0.01
bpy.ops.object.bake(type="EMIT")
yoke = np.array(img_y.pixels[:]).reshape(TEX, TEX, 4)[:, :, 0]
for o in (yflat, lflat):
    bpy.data.objects.remove(o, do_unlink=True)
log["yokeShare"] = round(float((yoke > 0.5).mean()), 4)

# (c) the faces made here (the hem's new rows, the turned-in edges) take the plain wool, whatever the rays found
ex = lm.attributes.get("extra")
uvd = lm.uv_layers["UVMap"].data


def raster(polys):
    """The texels the given faces cover in UVMap (with a small pad), as a mask."""
    out = np.zeros((TEX, TEX), bool)
    for p_ in polys:
        uvs = [np.array(uvd[li].uv) * TEX for li in p_.loop_indices]
        for k_ in range(1, len(uvs) - 1):
            a_, b_, c_ = uvs[0], uvs[k_], uvs[k_ + 1]
            x0, y0 = np.floor(np.minimum(np.minimum(a_, b_), c_)).astype(int) - 2
            x1, y1 = np.ceil(np.maximum(np.maximum(a_, b_), c_)).astype(int) + 2
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(TEX - 1, x1), min(TEX - 1, y1)
            if x1 < x0 or y1 < y0:
                continue
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            m_ = np.array([[b_[0] - a_[0], c_[0] - a_[0]], [b_[1] - a_[1], c_[1] - a_[1]]])
            if abs(np.linalg.det(m_)) < 1e-9:
                continue
            inv = np.linalg.inv(m_)
            d0, d1 = xs - a_[0], ys - a_[1]
            l1 = inv[0, 0] * d0 + inv[0, 1] * d1
            l2 = inv[1, 0] * d0 + inv[1, 1] * d1
            pad = 2.5 / max(1.0, np.linalg.norm(b_ - a_), np.linalg.norm(c_ - a_))
            inside = (l1 >= -pad) & (l2 >= -pad) & (l1 + l2 <= 1 + pad)
            out[y0:y1 + 1, x0:x1 + 1] |= inside
    return out


plain = raster([p_ for p_ in lm.polygons if ex is not None and ex.data[p_.index].value])
hit &= ~plain
log["plainTexels"] = int(plain.sum())


def to_srgb(c):
    c = np.clip(np.asarray(c, float), 0, 1)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def base_colour(name, fallback):
    m = next((m for m in hi.data.materials if m and name in m.name), None)
    b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if m and m.use_nodes else None
    return to_srgb(tuple(b.inputs["Base Color"].default_value)[:3] if b else fallback)


wool_c = base_colour("Wool", (0.03, 0.04, 0.09))
yoke_c = base_colour("Yoke", (0.012, 0.012, 0.014))
ymask = np.clip(blur(yoke, opt("--yoke-aa", 0.7)), 0, 1)
col = np.ones((TEX, TEX, 4))
col[:, :, :3] = wool_c[None, None, :] * (1 - ymask[:, :, None]) + yoke_c[None, None, :] * ymask[:, :, None]
img_c = new_image("_basecolor")
img_c.pixels[:] = col.ravel()
POCKET_LINE = opt("--pocket-line", 0.35)
# the normal map: steep texels (the drape's crumpled armpits) laid flat, the texels with nothing under them flat,
# the yoke's edge raised (--ledge, the step's height in texture steps)
nrm = np.array(img_n.pixels[:]).reshape(TEX, TEX, 4)
v3 = nrm[:, :, :3] * 2 - 1
steep = v3[:, :, 2] < opt("--steep", 0.55)
v3[steep | ~hit] = (0.0, 0.0, 1.0)
h = blur(yoke, opt("--ledge-soft", 1.6))
gy, gx = np.gradient(h)
LEDGE = opt("--ledge", 1.2)
v3[:, :, 0] -= LEDGE * gx
v3[:, :, 1] -= LEDGE * gy
# THE POCKETS' OUTLINES (the first review: "faint painted outlines only ... at street distance they disappear, and
# on the V&A jacket they are a strong feature"): each texel's place on the game mesh (a position bake) tested against
# the drape's pocket pieces; where a pocket lies over it, a mask; its edge raised in the normal map (--pocket-ledge)
# and a thin shadow line drawn round it in the colour (--pocket-line, how much darker)
pocket_mask = np.zeros((TEX, TEX))
cover = hit | plain
if pockets:
    pbm_ = bmesh.new()
    for k in pockets:
        vmap = {}
        for f in pieces[k]:
            vs = []
            for v in f.verts:
                if v.index not in vmap:
                    vmap[v.index] = pbm_.verts.new(v.co)
                vs.append(vmap[v.index])
            try:
                pbm_.faces.new(vs)
            except ValueError:
                pass
    POCKET_BVH = BVHTree.FromBMesh(pbm_)
    zlo = min(v.co.z for v in pbm_.verts) - 0.02
    zhi = max(v.co.z for v in pbm_.verts) + 0.02
    pbm_.free()
    # each texel's place on the game mesh, from the faces of the two fronts (a bake of "POSITION" gave other values)
    pos = np.zeros((TEX, TEX, 3))
    front_ids = {PANELS.index("front_l"), PANELS.index("front_r")}
    panel_a = lm.attributes["panel"].data
    for p_ in lm.polygons:
        if panel_a[p_.index].value not in front_ids:
            continue
        uvs = [np.array(uvd[li].uv) * TEX for li in p_.loop_indices]
        cos = [np.array(lo.matrix_world @ lm.vertices[vi].co) for vi in p_.vertices]
        for k_ in range(1, len(uvs) - 1):
            a_, b_, c_ = uvs[0], uvs[k_], uvs[k_ + 1]
            A_, B_, C_ = cos[0], cos[k_], cos[k_ + 1]
            x0, y0 = np.floor(np.minimum(np.minimum(a_, b_), c_)).astype(int)
            x1, y1 = np.ceil(np.maximum(np.maximum(a_, b_), c_)).astype(int)
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(TEX - 1, x1), min(TEX - 1, y1)
            if x1 < x0 or y1 < y0:
                continue
            m_ = np.array([[b_[0] - a_[0], c_[0] - a_[0]], [b_[1] - a_[1], c_[1] - a_[1]]])
            if abs(np.linalg.det(m_)) < 1e-9:
                continue
            inv = np.linalg.inv(m_)
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            d0, d1 = xs - a_[0], ys - a_[1]
            l1 = inv[0, 0] * d0 + inv[0, 1] * d1
            l2 = inv[1, 0] * d0 + inv[1, 1] * d1
            inside = (l1 >= -0.02) & (l2 >= -0.02) & (l1 + l2 <= 1.02)
            P3 = A_[None, None, :] + l1[:, :, None] * (B_ - A_)[None, None, :] + l2[:, :, None] * (C_ - A_)[None, None, :]
            blk = pos[y0:y1 + 1, x0:x1 + 1]
            blk[inside] = P3[inside]
    cand = (pos[:, :, 2] > zlo) & (pos[:, :, 2] < zhi) & (pos[:, :, 1] < 0)
    ys_, xs_ = np.nonzero(cand)
    PT = opt("--pocket-reach", 0.009)
    for y_, x_ in zip(ys_, xs_):
        q_ = POCKET_BVH.find_nearest(Vector(pos[y_, x_]))
        if q_[0] is not None and q_[3] < PT:
            pocket_mask[y_, x_] = 1.0
    log["pocketTexels"] = int(pocket_mask.sum())
    pm = blur(pocket_mask, 1.0)
    py_, px_ = np.gradient(pm)
    PL = opt("--pocket-ledge", 1.4)
    v3[:, :, 0] -= PL * px_
    v3[:, :, 1] -= PL * py_
# the overlapping front's edge above the opening: the strip of the right front between the centre and the line is
# the left front lying over it; its outer side is raised (--edge-ledge); its mask spreads past its island's edges
# (as a bake's margin) so only the line itself makes a step
over = lm.attributes.get("overlap")
cover = hit | plain
if over is not None and any(d.value for d in over.data):
    strip = raster([p_ for p_ in lm.polygons if over.data[p_.index].value])
    sm = strip.astype(float)
    for _ in range(8):
        grown = np.maximum.reduce([sm, np.roll(sm, 1, 0), np.roll(sm, -1, 0), np.roll(sm, 1, 1), np.roll(sm, -1, 1)])
        sm = np.where(cover, sm, grown)
    he = blur(sm, 1.2)
    ey, ex_ = np.gradient(he)
    EL = opt("--edge-ledge", 1.6)
    v3[:, :, 0] -= EL * ex_ * cover
    v3[:, :, 1] -= EL * ey * cover
    log["frontEdgeTexels"] = int(strip.sum())
# melton's felted face: a fine, even grain on the wool (not the yoke), --felt its strength
FELT = opt("--felt", 0.05)
if FELT > 0:
    rng = np.random.default_rng(7)
    nz_ = rng.normal(size=(TEX, TEX, 2))
    nz_ = np.stack([blur(nz_[:, :, 0], 1.0), blur(nz_[:, :, 1], 1.0)], axis=2)
    nz_ /= nz_.std() + 1e-9
    wool_t = (cover & (yoke < 0.5)).astype(float)[:, :, None]
    v3[:, :, :2] += FELT * nz_ * wool_t
v3 /= np.linalg.norm(v3, axis=2, keepdims=True)
nrm[:, :, :3] = (v3 + 1) / 2
img_n.pixels[:] = nrm.ravel()
if pocket_mask.any() and POCKET_LINE > 0:
    edge = np.clip(blur(pocket_mask, 1.2) - blur(pocket_mask, 3.0), 0, None)
    edge = edge / (edge.max() + 1e-9)
    colp = np.array(img_c.pixels[:]).reshape(TEX, TEX, 4)
    colp[:, :, :3] *= (1 - POCKET_LINE * edge)[:, :, None]
    img_c.pixels[:] = colp.ravel()
# the yoke's shine: PVC or leather, not wool (--yoke-rough), in a roughness map
rough = np.ones((TEX, TEX, 4))
rv = opt("--wool-rough", 0.9) * (1 - ymask) + opt("--yoke-rough", 0.42) * ymask
rough[:, :, 0] = rough[:, :, 1] = rough[:, :, 2] = rv
img_r = new_image("_roughness", colour=False)
img_r.pixels[:] = rough.ravel()
log["bakeHitShare"] = round(float(hit.mean()), 3)
log["steepFlattened"] = int(steep.sum())


def save(im, fname):
    im.filepath_raw = os.path.join(OUT, fname)
    im.file_format = "PNG"
    im.save()


save(img_c, NAME + "_basecolor.png")
save(img_r, NAME + "_roughness.png")
save(img_n, NAME + "_normal_gl.png")
dx = nrm.copy()
dx[:, :, 1] = 1.0 - dx[:, :, 1]
img_dx = new_image("_normal_dx", colour=False)
img_dx.pixels[:] = dx.ravel()
save(img_dx, NAME + "_normal_dx.png")
# the game mesh's material as the pictures show it: the colour and the normal map
nt.nodes.remove(node_m)
node_c = nt.nodes.new("ShaderNodeTexImage")
node_c.image = img_c
nt.links.new(node_c.outputs["Color"], bsdf.inputs["Base Color"])
nmap = nt.nodes.new("ShaderNodeNormalMap")
nmap.uv_map = "UVMap"
nt.links.new(node_n.outputs["Color"], nmap.inputs["Color"])
nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
node_r = nt.nodes.new("ShaderNodeTexImage")
node_r.image = img_r
nt.links.new(node_r.outputs["Color"], bsdf.inputs["Roughness"])
bt.node_tree.nodes.remove(bn)
bpy.data.objects.remove(hib, do_unlink=True)
hi.hide_render = True
say("baked", TEX, "hit share", log["bakeHitShare"], "yoke share", log["yokeShare"], "steep flattened", log["steepFlattened"])

bm_t = bmesh.new()
bm_t.from_mesh(lm)
ng = [f for f in bm_t.faces if len(f.verts) > 4]
if ng:
    bmesh.ops.triangulate(bm_t, faces=ng)
    bm_t.to_mesh(lm)
log["ngonsCut"] = len(ng)
bm_t.free()
# ---- the export ----------------------------------------------------------------------------------------------
log["faces"] = len(lm.polygons)
log["tris"] = sum(len(p.vertices) - 2 for p in lm.polygons)
log["points"] = len(lm.vertices)
bpy.ops.object.select_all(action="DESELECT")
lo.select_set(True)
bpy.context.view_layer.objects.active = lo
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_static.fbx"), use_selection=True, object_types={"MESH"},
                         mesh_smooth_type="OFF", use_tspace=True, add_leaf_bones=False, colors_type="LINEAR")
img_c.pack()
img_n.pack()
img_r.pack()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "retopo.json"), "w"), indent=1)
say("done", json.dumps({k: log[k] for k in ("faces", "tris", "points")}))
