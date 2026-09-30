"""A drape made to hang as stiff wool does: below the armpits straight down from the body's widest point, with an
even ease; the sleeves as tubes. Run on the drape before retopo_garment.py, so the game mesh and its bake agree.

    blender -b -P tools/meshgen/blender/hang_drape.py -- DRAPE.blend OUT_DIR --name ron_hung [--ease 0.03] [--sleeve-tube 0.6]

WHY, 30 September (the game-way donkey jacket's first blind review, production/art/clothing/donkey-jacket-game/
review-1.md): on Darren, carried from Ron, the jacket "hangs like a sack" below the chest yet "clings tightly enough
to show his pectorals"; on both men "the back bellies out from the waist like a bustle ... A donkey jacket hangs
straight down from the shoulder blades"; "heavy melton would hang as a tube" in the sleeves. The drape came from a
cloth simulation that let the wool follow the body's hollows and swell where its pattern had room; heavy melton
bridges hollows and falls plumb (production/reference/donkey-jacket-1990.md: "stiff and boxy ... not draping";
"straight from the shoulders").

THE TRUNK, from --chest-up above the armpit down (easing to nothing near the armhole seams): in each horizontal slice of the body (its trunk, the arms left out, the
two legs bridged below the crotch) the slice's outline is taken round its convex hull, and the jacket's place at
each angle round a fixed upright axis is that hull plus --ease; going down, the jacket never comes back in (it falls
plumb from the widest point above it). The drape keeps its own folds: each point moves by the difference between
that place and the drape's own smoothed radius there, so the folds ride on the new shape (they are baked into the
game mesh's normal map). The move eases in over 6 cm below the top.
THE SLEEVES: each ring round the arm made rounder (--sleeve-tube: 0 as draped, 1 a round tube as wide as the ring's
widest), plus 3 mm, easing in over 8 cm from the armhole, so the sleeve hangs as a tube and no longer shows the arm.
Every point of the render mesh moves (both faces of the wool and the pieces on it: pockets, the front strip,
buttons), so thickness and pieces are kept. OUT_DIR gets NAME.blend and hang.json.
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, OUT = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "hung", str)
RENDER = opt("--render", "JacketRender", str)
EASE = opt("--ease", 0.03)
TUBE = opt("--sleeve-tube", 0.6)
NB = 144
DZ = 0.01
log = {"blend": BLEND, "ease": EASE, "sleeveTube": TUBE}


def say(*a):
    print("HANG", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=BLEND)
g = bpy.data.objects[RENDER]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = next(o for o in bpy.data.objects if o.type == "MESH" and "Body" in o.name)
J = lambda n: arm.matrix_world @ arm.pose.bones[n].head  # noqa: E731

# ---- the body's trunk, its arms left out -----------------------------------------------------------------------
ARMY = ("upperarm", "lowerarm", "hand", "thumb", "index", "middle", "ring", "pinky")
arm_groups = {vg.index for vg in body.vertex_groups if vg.name.startswith(ARMY)}
BP = []
for v in body.data.vertices:
    a = sum(ge.weight for ge in v.groups if ge.group in arm_groups)
    if a < 0.3:
        BP.append(tuple(body.matrix_world @ v.co))
BP = np.array(BP)

# ---- the drape: its pieces, the wool's pattern pieces, its outer skin ------------------------------------------
bm = bmesh.new()
bm.from_mesh(g.data)
bm.transform(g.matrix_world)
bm.normal_update()
bm.faces.ensure_lookup_table()
bm.verts.ensure_lookup_table()
comp = [-1] * len(bm.faces)
for f0 in bm.faces:
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
mats = [m.name if m else "" for m in g.data.materials]
count = {}
for f in bm.faces:
    count[comp[f.index]] = count.get(comp[f.index], 0) + 1
main = max((k for k in count if "Wool" in mats[bm.faces[k].material_index]), key=lambda k: count[k])
uv = bm.loops.layers.uv["pattern"]
main_faces = [f for f in bm.faces if comp[f.index] == main]
isl = {}
k_ = 0
for f in main_faces:
    if f.index in isl:
        continue
    isl[f.index] = k_
    st = [f]
    while st:
        x = st.pop()
        for lp in x.loops:
            va, ua, ub = lp.vert, lp[uv].uv, lp.link_loop_next[uv].uv
            for l2 in lp.edge.link_loops:
                y = l2.face
                if y is x or y.index in isl or comp[y.index] != main:
                    continue
                wa, wb = (l2[uv].uv, l2.link_loop_next[uv].uv) if l2.vert is va else (l2.link_loop_next[uv].uv, l2[uv].uv)
                if (ua - wa).length < 1e-5 and (ub - wb).length < 1e-5:
                    isl[y.index] = k_
                    st.append(y)
    k_ += 1
mean_u = {}
for f in main_faces:
    mean_u.setdefault(isl[f.index], []).append(sum(lp[uv].uv.x for lp in f.loops) / len(f.loops))
sleeve_isl = {i for i, us in mean_u.items() if abs(sum(us) / len(us)) > 1.5}
is_sleeve = np.zeros(len(bm.verts), bool)
is_trunk_face_v = np.zeros(len(bm.verts), bool)
for f in main_faces:
    for v in f.verts:
        if isl[f.index] in sleeve_isl:
            is_sleeve[v.index] = True
        else:
            is_trunk_face_v[v.index] = True
armhole = is_sleeve & is_trunk_face_v
cands = [f for f in main_faces if abs(f.calc_center_median().x) < 0.04 and f.normal.y < -0.85]
seed = min(cands, key=lambda f: abs(f.calc_center_median().z - 1.2) + f.calc_center_median().y)
lim = math.cos(math.radians(50.0))
outer = {seed.index}
st = [seed]
while st:
    f = st.pop()
    for e in f.edges:
        for f2 in e.link_faces:
            if f2.index not in outer and f2.normal.dot(f.normal) > lim:
                outer.add(f2.index)
                st.append(f2)
outer_v = np.zeros(len(bm.verts), bool)
for i in outer:
    for v in bm.faces[i].verts:
        outer_v[v.index] = True
P = np.array([tuple(v.co) for v in bm.verts])


def smooth1(a, sigma, axis, circular=False):
    r = int(math.ceil(3 * sigma))
    kx = np.exp(-(np.arange(-r, r + 1) / sigma) ** 2 / 2)
    kx /= kx.sum()
    pad = "wrap" if circular else "edge"
    return np.apply_along_axis(lambda x: np.convolve(np.pad(x, r, mode=pad), kx, mode="valid"), axis, a)


def fill_empty(a):
    """Empty cells (nan) take their row's neighbours round the circle, then the rows above or below."""
    a = a.copy()
    for k in range(a.shape[0]):
        row = a[k]
        ok = ~np.isnan(row)
        if ok.any() and not ok.all():
            idx = np.arange(len(row))
            row[~ok] = np.interp(idx[~ok], idx[ok], row[ok], period=len(row))
    for b in range(a.shape[1]):
        col = a[:, b]
        ok = ~np.isnan(col)
        if ok.any() and not ok.all():
            idx = np.arange(len(col))
            col[~ok] = np.interp(idx[~ok], idx[ok], col[ok])
    return a


# ---- the trunk ---------------------------------------------------------------------------------------------------
armpit = P[armhole, 2].min() if armhole.any() else J("upperarm_l").z - 0.12
# THE CHEST TOO (the first review, on Darren: the chest "clings tightly enough to show his pectorals"): the hang
# starts --chest-up above the armpit, and near the armhole seam it eases to nothing (--armhole-ease metres), so the
# sleeves, which it does not move, stay joined smoothly
top = armpit + opt("--chest-up", 0.10)
hem = P[:, 2].min()
hipz = (J("thigh_l").z + J("thigh_r").z) / 2
band = BP[(BP[:, 2] > hipz) & (BP[:, 2] < armpit)]
AX = band[:, :2].mean(axis=0)
K = int(math.ceil((top - hem) / DZ)) + 2
zs = top - np.arange(K) * DZ
angles = np.arange(NB) * 2 * math.pi / NB
dirs = np.stack([np.cos(angles), np.sin(angles)], axis=1)


def hull2(pts):
    pts = sorted(set(map(tuple, np.round(pts, 5))))
    if len(pts) < 3:
        return np.array(pts)
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and np.cross(np.subtract(lower[-1], lower[-2]), np.subtract(p, lower[-2])) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and np.cross(np.subtract(upper[-1], upper[-2]), np.subtract(p, upper[-2])) <= 0:
            upper.pop()
        upper.append(p)
    return np.array(lower[:-1] + upper[:-1])


def ray_hull(poly, d):
    """Distance from the axis along d to the hull's edge (the farthest crossing)."""
    best = 0.0
    n = len(poly)
    for i in range(n):
        a, b = poly[i] - AX, poly[(i + 1) % n] - AX
        e = b - a
        den = d[0] * (-e[1]) - d[1] * (-e[0])
        if abs(den) < 1e-12:
            continue
        t = (a[0] * (-e[1]) - a[1] * (-e[0])) / den
        s = (d[0] * a[1] - d[1] * a[0]) / den
        if t > 0 and -1e-9 <= s <= 1 + 1e-9:
            best = max(best, t)
    return best


RT = np.full((K, NB), np.nan)
for k, z in enumerate(zs):
    sl = BP[np.abs(BP[:, 2] - z) < 0.015]
    if len(sl) < 6:
        continue
    poly = hull2(sl[:, :2])
    if len(poly) < 3:
        continue
    RT[k] = [ray_hull(poly, d) + EASE for d in dirs]
RT = fill_empty(RT)
R = np.maximum.accumulate(RT, axis=0)                      # plumb: never back in going down
# the drape's own radius there, smoothed (its folds are what is left over)
trunk_outer = outer_v & ~is_sleeve
rad = np.linalg.norm(P[:, :2] - AX, axis=1)
ang = np.mod(np.arctan2(P[:, 1] - AX[1], P[:, 0] - AX[0]), 2 * math.pi)
kk = np.round((top - P[:, 2]) / DZ).astype(int)
bb = np.round(ang / (2 * math.pi) * NB).astype(int) % NB
RO = np.full((K, NB), np.nan)
acc = np.zeros((K, NB))
cnt = np.zeros((K, NB))
sel = trunk_outer & (kk >= 0) & (kk < K)
np.add.at(acc, (kk[sel], bb[sel]), rad[sel])
np.add.at(cnt, (kk[sel], bb[sel]), 1)
RO[cnt > 0] = acc[cnt > 0] / cnt[cnt > 0]
RO = fill_empty(RO)
RO = smooth1(smooth1(RO, opt("--fold-keep", 3.0), 1, circular=True), opt("--fold-keep", 3.0), 0)
W = np.clip(np.arange(K) * DZ / 0.06, 0, 1)
W = W * W * (3 - 2 * W)
DR = (R - RO) * W[:, None]


def dr_at(z, a):
    fk = (top - z) / DZ
    fb = a / (2 * math.pi) * NB
    k0 = int(math.floor(fk))
    b0 = int(math.floor(fb))
    tk, tb = fk - k0, fb - b0
    k0c, k1c = min(max(k0, 0), K - 1), min(max(k0 + 1, 0), K - 1)
    b0c, b1c = b0 % NB, (b0 + 1) % NB
    return ((1 - tk) * ((1 - tb) * DR[k0c, b0c] + tb * DR[k0c, b1c]) + tk * ((1 - tb) * DR[k1c, b0c] + tb * DR[k1c, b1c]))


# every point of the render mesh below the top that is not a sleeve's
from mathutils.kdtree import KDTree  # noqa: E402
ah = np.where(armhole)[0]
akd = KDTree(len(ah))
for n_, i in enumerate(ah):
    akd.insert(Vector(P[i]), n_)
akd.balance()
AE = opt("--armhole-ease", 0.07)
moved = 0
most = 0.0
not_sleeve_v = ~is_sleeve
for i, v in enumerate(bm.verts):
    if not not_sleeve_v[i] or P[i, 2] >= top:
        continue
    d = dr_at(P[i, 2], ang[i])
    if len(ah):
        da = akd.find(Vector(P[i]))[2]
        wa = min(1.0, da / AE)
        d *= wa * wa * (3 - 2 * wa)
    v.co.x += d * math.cos(ang[i])
    v.co.y += d * math.sin(ang[i])
    moved += 1
    most = max(most, abs(d))
log["trunk"] = {"armpitZ": round(float(armpit), 3), "topZ": round(float(top), 3), "hemZ": round(float(hem), 3),
                "axis": [round(float(c), 3) for c in AX], "pointsMoved": moved, "mostMm": round(most * 1000, 1),
                "meanMm": round(float(np.nanmean(np.abs(DR[W > 0.99]))) * 1000, 1)}
say("trunk", json.dumps(log["trunk"]))

# ---- the sleeves ----------------------------------------------------------------------------------------------
if TUBE > 0:
    TB, FB = 0.01, 48
    for s in "lr":
        chain = [J("upperarm_" + s), J("lowerarm_" + s), J("hand_" + s)]
        L0 = (chain[1] - chain[0]).length
        sgn = 1 if s == "l" else -1
        ids = np.where(is_sleeve & (P[:, 0] * sgn > 0))[0]
        T = np.zeros(len(ids))
        PHI = np.zeros(len(ids))
        RHO = np.zeros(len(ids))
        RDIR = np.zeros((len(ids), 3))
        for n_, i in enumerate(ids):
            p = Vector(P[i])
            best = None
            for si, (a, b) in enumerate(((chain[0], chain[1]), (chain[1], chain[2]))):
                ab = b - a
                t = max(0.0, min(1.0, (p - a).dot(ab) / ab.length_squared))
                q = a + ab * t
                dd = (p - q).length
                if best is None or dd < best[0]:
                    best = (dd, si, t, q, ab.normalized())
            dd, si, t, q, u = best
            T[n_] = (t * L0) if si == 0 else (L0 + t * (chain[2] - chain[1]).length)
            e1 = Vector((0, 0, 1)) - u * u.z
            e1.normalize()
            e2 = u.cross(e1)
            r = p - q
            RHO[n_] = r.length
            PHI[n_] = math.atan2(r.dot(e2), r.dot(e1)) % (2 * math.pi)
            RDIR[n_] = tuple(r.normalized()) if r.length > 1e-9 else (0, 0, 0)
        t0 = T[armhole[ids]].mean() if armhole[ids].any() else T.min()
        KT = int(math.ceil((T.max() - T.min()) / TB)) + 2
        kt = np.round((T - T.min()) / TB).astype(int)
        bf = np.round(PHI / (2 * math.pi) * FB).astype(int) % FB
        so = outer_v[ids]
        acc = np.zeros((KT, FB))
        cnt = np.zeros((KT, FB))
        np.add.at(acc, (kt[so], bf[so]), RHO[so])
        np.add.at(cnt, (kt[so], bf[so]), 1)
        RS = np.full((KT, FB), np.nan)
        RS[cnt > 0] = acc[cnt > 0] / cnt[cnt > 0]
        RS = fill_empty(RS)
        RS = smooth1(smooth1(RS, 2.0, 1, circular=True), 2.0, 0)
        target = (1 - TUBE) * RS + TUBE * RS.max(axis=1, keepdims=True) + 0.003
        wt = np.clip((T.min() + np.arange(KT) * TB - t0) / 0.08, 0, 1)
        wt = wt * wt * (3 - 2 * wt)
        DRS = (target - RS) * wt[:, None]
        for n_, i in enumerate(ids):
            d = DRS[min(kt[n_], KT - 1), bf[n_]]
            # eased to nothing at the armhole seam as the trunk is (the second review: moved by different amounts
            # either side of it, the back of the armhole looked torn)
            if len(ah):
                wa = min(1.0, akd.find(Vector(P[i]))[2] / AE)
                d *= wa * wa * (3 - 2 * wa)
            bm.verts[i].co += Vector(RDIR[n_]) * d
        log["sleeve_" + s] = {"points": int(len(ids)), "mostMm": round(float(np.abs(DRS).max()) * 1000, 1)}
        say("sleeve", s, json.dumps(log["sleeve_" + s]))
bm.transform(g.matrix_world.inverted())
bm.to_mesh(g.data)
bm.free()
g.data.update()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "hang.json"), "w"), indent=1)
say("done", NAME)
