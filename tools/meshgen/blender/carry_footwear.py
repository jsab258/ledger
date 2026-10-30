"""A finished, skinned pair of shoes or boots carried from the MetaHuman it was made on to another of the same mesh,
by correspondence, its weights kept point for point (30 October 2026, Tom's boots from Ron's passed pair).

    blender -b --factory-startup -P tools/meshgen/blender/carry_footwear.py -- SRC_SKINNED.fbx FROM_BODY.fbx TO_BODY.fbx
        OUT_DIR [--name tom_boots] [--k 24] [--smooth 4] [--drop 0.020] [--colours COLOURS.json] [--ease 0.0045]

WHY: a pair that passed its review on one wearer is worth more than a new one made for the next; the MetaHuman full
bodies share one mesh, point for point (Ron's MH_RoccoP2 and Tom's MH_TomL1: 51,619 points and the same faces at
LOD0), so where each foot differs is known at every point of its skin. carry_garment.py moves a garment by the
body's own broad change round it (a Gaussian of the skin's moves); a shoe stands off the foot by its ease, toe
allowance and sole, and those are lengths that must stay what they were, so here each shoe point keeps its offset
from the skin in the skin's own frame:

1. ANCHORS: the skin of each foot and ankle (LOD0 points below --anchor-top metres, that side), on both bodies by the
   same index. Each anchor's frame is its normal (area-weighted, the seam-split copies of a point summed) and a
   tangent towards one fixed neighbour (the same index on both bodies), so the frame turns as that patch of skin
   turns from one foot to the other.
2. EACH SHOE POINT, from its --k nearest anchors on the first foot (inverse square distance weights, 2 mm softened):
   its offset from each anchor in that anchor's frame, rebuilt from the same anchor on the second foot; the
   weighted mean is its new place. The moves are then smoothed over the shoe's own edges (--smooth rounds, half
   each), which takes out any jitter and leaves its shape (the moves vary over centimetres, its detail over
   millimetres).
2b. --ease E (off unless given): the leather then set out to at least E off the second body's skin (below).
3. THE SOLE KEPT FLAT: the sole's floor (the points within 0.3 mm of its lowest) set exactly --drop metres under the
   second body's bare floor (MetaHumans stand barefoot on the floor since 5.6: the builder raises the wearer by the
   sole); the correction a plane plus each floor point's own remainder, eased out over 30 to 60 mm up the shoe.
4. THE WEIGHTS AS THEY WERE: every point keeps the source's groups and weights (footwear: never re-transferred from
   the body; FOOTWEAR-2026-09-30.md: copied from the bare foot the toe box would go to the toe bones), bound to the
   second body's own armature in its reference pose; the bone names are the MetaHuman skeleton's on both.
5. THE COLOURS: --colours, a JSON {slot: {"rgb": [r, g, b] linear, "rough": r, "metal": m}}, set as each material's
   base colour (the import carries it as the slot's colour), roughness and metallic.

Measured and written to carry.json: the moves; the jitter before and after the smoothing; the sole's floor before
and after; the ease (each covered skin point's gap to the shoe's inner face, behind the ball and above the sole,
5th, 50th and 95th percentiles) and the toe allowance on both bodies; where the ball's weight crosses one half
against each body's ball joint; the weights compared point for point.

OUT_DIR gets NAME_skinned.fbx (the pair on the second body's skeleton; pose_skinned.py --export's settings, as Ron's
ron_boots_skinned.fbx was written: smoothing by face, no leaf bones, no animation), NAME_static.fbx, NAME.blend
(the pair "NAME", the skeleton and the second body's LOD0 for the pose checks) and carry.json.
"""
import json
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, FROM, TO, OUT = argv[:4]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
NAME = opt("--name", "carried_footwear", str)
K = opt("--k", 24, int)
SMOOTH = opt("--smooth", 4, int)
DROP = opt("--drop", 0.020)
ANCHOR_TOP = opt("--anchor-top", 0.25)
COLOURS = json.load(open(opt("--colours", "", str))) if "--colours" in argv else {}
os.makedirs(OUT, exist_ok=True)
log = {"source": SRC, "from": FROM, "to": TO, "k": K, "smooth": SMOOTH, "dropM": DROP}


def say(*a):
    print("CARRYFOOT", *a, flush=True)


def mm(x):
    return round(float(x) * 1000, 2)


bpy.ops.wm.read_factory_settings(use_empty=True)

# ---- the source pair: its points in the world, its weights ------------------------------------------------------
bpy.ops.import_scene.fbx(filepath=SRC)
src_arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
shoe = max([o for o in bpy.data.objects if o.type == "MESH"], key=lambda o: len(o.data.vertices))
mw = shoe.matrix_world.copy()
shoe.parent = None
shoe.matrix_world = mw
shoe.data.transform(mw)
shoe.matrix_world = Matrix.Identity(4)
for m in list(shoe.modifiers):
    shoe.modifiers.remove(m)
for o in list(bpy.data.objects):
    if o is not shoe:
        bpy.data.objects.remove(o, do_unlink=True)
for a in list(bpy.data.armatures):
    bpy.data.armatures.remove(a)
S0 = np.array([tuple(v.co) for v in shoe.data.vertices])
GROUPS = [g.name for g in shoe.vertex_groups]
W0 = np.zeros((len(S0), len(GROUPS)))
for v in shoe.data.vertices:
    for g in v.groups:
        W0[v.index, g.group] = g.weight
log["source_pair"] = {"points": len(S0), "tris": sum(len(p.vertices) - 2 for p in shoe.data.polygons), "groups": GROUPS,
                      "materials": [m.name for m in shoe.data.materials]}
say("source", json.dumps(log["source_pair"]))


def load_body(path, keep):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    arm = next(o for o in new if o.type == "ARMATURE")
    ms = sorted([o for o in new if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
    body = ms[0]
    P = np.array([tuple(body.matrix_world @ v.co) for v in body.data.vertices])
    faces = [tuple(p.vertices) for p in body.data.polygons]
    joints = {b: np.array(arm.matrix_world @ arm.data.bones[b].head_local) for b in ("foot_l", "foot_r", "ball_l", "ball_r")}
    if keep:
        for o in ms[1:]:
            bpy.data.objects.remove(o, do_unlink=True)
        return P, faces, joints, arm, body
    for o in new:
        bpy.data.objects.remove(o, do_unlink=True)
    for a in list(bpy.data.armatures):
        if a.users == 0:
            bpy.data.armatures.remove(a)
    for me in list(bpy.data.meshes):
        if me.users == 0:
            bpy.data.meshes.remove(me)
    return P, faces, joints, None, None


PR, FR, JR, _, _ = load_body(FROM, False)
PT, FT, JT, arm, body = load_body(TO, True)
if len(PR) != len(PT) or FR != FT:
    raise SystemExit("CARRYFOOT the bodies do not share one mesh (%d and %d points, faces %s)" % (
        len(PR), len(PT), "equal" if FR == FT else "different"))
log["correspondence"] = {"points": len(PR), "faces": len(FR), "sameFaces": True}
say("one mesh", len(PR), "points", len(FR), "faces")

# ---- frames: normals (seam copies summed) and a tangent towards one fixed neighbour ----------------------------
key = {}
canon = np.empty(len(PR), int)
for i, p in enumerate(np.round(PR * 1e5).astype(np.int64)):
    canon[i] = key.setdefault(tuple(p), i)
spread = float(np.abs(PT - PT[canon]).max())
log["correspondence"]["seamCopies"] = int((canon != np.arange(len(PR))).sum())
log["correspondence"]["seamCopiesApartOnSecondMm"] = mm(spread)
tris = np.array([(f[0], f[a], f[a + 1]) for f in FR for a in range(1, len(f) - 1)])
nb = [[] for _ in range(len(PR))]
for f in FR:
    for a in range(len(f)):
        u, w = f[a], f[(a + 1) % len(f)]
        nb[u].append(w)
        nb[w].append(u)


def normals(P):
    fn = np.cross(P[tris[:, 1]] - P[tris[:, 0]], P[tris[:, 2]] - P[tris[:, 0]])
    N = np.zeros_like(P)
    for c in range(3):
        np.add.at(N, tris[:, c], fn)
    Nc = np.zeros_like(P)
    np.add.at(Nc, canon, N)
    N = Nc[canon]
    return N / np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]


NR, NT = normals(PR), normals(PT)
# the neighbour: on the first body, the one whose direction lies most in the skin's plane (the same index on both)
pick = np.zeros(len(PR), int)
for i in range(len(PR)):
    best, bl = i, -1.0
    for j in set(nb[i]):
        d = PR[j] - PR[i]
        t = d - d.dot(NR[i]) * NR[i]
        if np.linalg.norm(t) > bl:
            best, bl = j, np.linalg.norm(t)
    pick[i] = best


def frames(P, N):
    T = P[pick] - P
    T = T - np.sum(T * N, axis=1)[:, None] * N
    T /= np.maximum(np.linalg.norm(T, axis=1), 1e-12)[:, None]
    B = np.cross(N, T)
    return np.stack([T, B, N], axis=2)         # columns: tangent, bitangent, normal


FRm, FTm = frames(PR, NR), frames(PT, NT)
ROT = np.einsum("nij,nkj->nik", FTm, FRm)       # each anchor's turn from the first foot to the second

# ---- the carry, side by side --------------------------------------------------------------------------------------
side_of = np.where(S0[:, 0] > 0, 1, -1)
S1 = S0.copy()
log["anchors"] = {}
for sg, sname in ((1, "l"), (-1, "r")):
    A = np.where((PR[:, 0] * sg > 0.02) & (PR[:, 2] < ANCHOR_TOP) & (canon == np.arange(len(PR))))[0]
    kd = KDTree(len(A))
    for n, i in enumerate(A):
        kd.insert(Vector(tuple(PR[i])), n)
    kd.balance()
    ids = np.where(side_of == sg)[0]
    near = np.zeros((len(ids), K), int)
    dist = np.zeros((len(ids), K))
    for r, i in enumerate(ids):
        for c, (_co, n, d) in enumerate(kd.find_n(Vector(tuple(S0[i])), K)):
            near[r, c], dist[r, c] = A[n], d
    w = 1.0 / (dist ** 2 + 0.002 ** 2)
    w /= w.sum(axis=1, keepdims=True)
    off = S0[ids][:, None, :] - PR[near]                                  # (n, K, 3)
    cand = PT[near] + np.einsum("nkij,nkj->nki", ROT[near], off)
    S1[ids] = np.sum(w[:, :, None] * cand, axis=1)
    log["anchors"][sname] = {"skinPoints": int(len(A)), "nearestMm": [mm(np.percentile(dist[:, 0], q)) for q in (50, 95, 100)],
                             "spreadOfCandidatesMm95": mm(np.percentile(np.linalg.norm(cand - S1[ids][:, None, :], axis=2).max(axis=1), 95))}

bm = bmesh.new()
bm.from_mesh(shoe.data)
E = np.array([[e.verts[0].index, e.verts[1].index] for e in bm.edges])
bm.free()
deg = np.bincount(E.ravel(), minlength=len(S0)).astype(float)


def nb_mean(X):
    acc = np.zeros_like(X)
    np.add.at(acc, E[:, 0], X[E[:, 1]])
    np.add.at(acc, E[:, 1], X[E[:, 0]])
    return acc / np.maximum(deg, 1)[:, None]


D = S1 - S0
jit0 = np.linalg.norm(D - nb_mean(D), axis=1)
for _ in range(SMOOTH):
    D = 0.5 * D + 0.5 * nb_mean(D)
jit1 = np.linalg.norm(D - nb_mean(D), axis=1)
S1 = S0 + D
mv = np.linalg.norm(D, axis=1)
log["moves"] = {"meanMm": mm(mv.mean()), "maxMm": mm(mv.max()), "minMm": mm(mv.min()),
                "jitterMm95Before": mm(np.percentile(jit0, 95)), "jitterMmMaxBefore": mm(jit0.max()),
                "jitterMm95After": mm(np.percentile(jit1, 95)), "jitterMmMaxAfter": mm(jit1.max())}
say("moves", json.dumps(log["moves"]))

# ---- --ease E: the leather set out to at least E off the second body's skin --------------------------------------
# (30 October 2026, Tom's boots, second try: Ron's passed pair stands 3.5 mm off his foot at the quarters, 1.6 mm low
# down and in his leg at the collar, its top 2 cm inside the shin and calf by up to 16 mm at rest, and the carry kept
# that; FOOTWEAR-2026-09-30.md asks 4 to 5 mm.) Each covered skin point (below the shoe's top, not facing down) looks
# along its normal, from inside the leg out, for the upper's faces: the nearest one is the leather's inner face, and
# the point asks a push along its normal of E less that gap. Every shoe point takes the mean of its nearest skin
# points' pushes, smoothed over its edges, so the leather's layers, the laces and eyelets move together and its
# thickness stays; the sole only sideways (its floor stays flat). Four rounds, each measured afresh. The upper's bottom
# under the foot (within 4 mm of the bare floor, inside the sole) is not looked for: pushed off the sole of the foot
# the first run carried the toe box 16 mm forward and the heel 6 mm back; nor the toes (more than 10 mm ahead of the ball
# joint: the toe box's room is the allowance, and a crease's normal between the toes started its ray outside the foot,
# reading the toe box's side as 30 mm through); a shoe point takes the push in full within 15 mm of a looked skin point
# and none beyond 40 mm (without it the toe box's sides took the ball's push each round, 11.6 mm in four).
EASE = opt("--ease", 0.0)
UPPER = opt("--upper-slot", "M_Upper", str)
SOLE = opt("--sole-slot", "M_Sole", str)
if EASE > 0:
    mnames = [m.name for m in shoe.data.materials]
    vmat = np.zeros(len(S0), int)
    polys = [tuple(p.vertices) for p in shoe.data.polygons]
    for p in shoe.data.polygons:
        vmat[list(p.vertices)] = p.material_index
    is_sole = vmat == mnames.index(SOLE)
    up_tris = [(f[0], f[a], f[a + 1]) for f, p in zip(polys, shoe.data.polygons) if p.material_index == mnames.index(UPPER)
               for a in range(1, len(f) - 1)]
    body_bvh = BVHTree.FromPolygons([tuple(p) for p in PT], [tuple(t) for t in tris])
    floor2 = float(PT[:, 2].min())
    log["ease"] = {"targetMm": mm(EASE), "rounds": []}
    for rnd in range(4):
        bvh_up = BVHTree.FromPolygons([tuple(p) for p in S1], up_tris)
        PUSH = np.zeros_like(S1)
        rec = {}
        for sg, sname in ((1, "l"), (-1, "r")):
            top = float(S1[side_of == sg][:, 2].max())
            fa = JT["ball_" + sname] - JT["foot_" + sname]
            fa[2] = 0
            fa /= np.linalg.norm(fa)
            cand = np.where((PT[:, 0] * sg > 0.02) & (PT[:, 2] > floor2 + 0.008) & (PT[:, 2] < top + 0.005) &
                            (NT[:, 2] > -0.3) & (canon == np.arange(len(PT))) &
                            ((PT - JT["ball_" + sname]) @ fa < 0.010))[0]
            pv = np.zeros((len(cand), 3))
            gaps = []
            for r, i in enumerate(cand):
                p, n = Vector(tuple(PT[i])), Vector(tuple(NT[i]))
                back = body_bvh.ray_cast(p - n * 1e-5, -n, 0.03)
                depth = min(0.03, 0.9 * back[3]) if back[0] is not None else 0.003
                o = p - n * depth
                hb, nb_, _fb, _db = body_bvh.find_nearest(o)
                if hb is None or (o - hb).dot(nb_) > 0:
                    continue                    # the start is not inside the leg (a crease's normal): no reading
                tt, hits = 0.0, []
                for _ in range(12):
                    h_ = bvh_up.ray_cast(o + n * (tt + 1e-6), n, depth + 0.04 - tt)
                    if h_[0] is None:
                        break
                    tt = (h_[0] - o).length
                    if h_[0].z > floor2 + 0.004:       # the upper's bottom under the foot (in the sole) is not its ease
                        hits.append(tt - depth)
                if not hits or min(hits) > 0.03:
                    continue
                g = min(hits)
                gaps.append(g)
                if g < EASE:
                    pv[r] = np.array(NT[i]) * (EASE - g)
            kd = KDTree(len(cand))
            for r, i in enumerate(cand):
                kd.insert(Vector(tuple(PT[i])), r)
            kd.balance()
            ids = np.where(side_of == sg)[0]
            for i in ids:
                hits = kd.find_n(Vector(tuple(S1[i])), 12)
                ww = np.array([1.0 / (d * d + 0.003 ** 2) for _c, _r, d in hits])
                reach = min(1.0, max(0.0, (0.04 - hits[0][2]) / 0.025))   # full within 15 mm of a looked point, none past 40
                PUSH[i] = reach * (ww[:, None] * pv[[r for _c, r, _d in hits]]).sum(0) / ww.sum()
            g = np.array(gaps)
            rec[sname] = {"skinPointsLooked": int(len(g)), "gapP5P50Mm": [mm(np.percentile(g, 5)), mm(np.percentile(g, 50))],
                          "underTarget": int((g < EASE - 0.0005).sum()), "askedMaxMm": mm(np.linalg.norm(pv, axis=1).max())}
        for _ in range(4):
            PUSH = 0.5 * PUSH + 0.5 * nb_mean(PUSH)
        PUSH[is_sole, 2] = 0.0
        S1 = S1 + PUSH
        rec["movedMaxMm"] = mm(np.linalg.norm(PUSH, axis=1).max())
        rec["movedMeanMm"] = mm(np.linalg.norm(PUSH, axis=1).mean())
        log["ease"]["rounds"].append(rec)
        say("ease round", rnd + 1, json.dumps(rec))
    tot = np.linalg.norm(S1 - S0 - D, axis=1)
    log["ease"]["setOutTotalMm"] = {"max": mm(tot.max()), "p95": mm(np.percentile(tot, 95)), "mean": mm(tot.mean())}

# ---- the sole kept flat, its floor DROP under the bare floor ------------------------------------------------------
floor_from, floor_to = float(PR[:, 2].min()), float(PT[:, 2].min())
src_floor = float(S0[:, 2].min())
target = floor_to - DROP
bottom = S0[:, 2] < src_floor + 0.0003
log["sole"] = {"sourceFloorUnderBareMm": mm(floor_from - src_floor), "bareFloorFirst": round(floor_from, 5),
               "bareFloorSecond": round(floor_to, 5), "targetZ": round(target, 5), "floorPoints": int(bottom.sum())}
h = S0[:, 2] - src_floor
fade = np.clip(1.0 - (h - 0.03) / 0.03, 0.0, 1.0)
for sg, sname in ((1, "l"), (-1, "r")):
    bi = np.where(bottom & (side_of == sg))[0]
    e = target - S1[bi, 2]
    X = np.c_[np.ones(len(bi)), S1[bi, 0], S1[bi, 1]]
    coef, *_ = np.linalg.lstsq(X, e, rcond=None)
    res = e - X @ coef
    kd = KDTree(len(bi))
    for n, i in enumerate(bi):
        kd.insert(Vector((S1[i, 0], S1[i, 1], 0.0)), n)
    kd.balance()
    ids = np.where(side_of == sg)[0]
    dz = np.zeros(len(ids))
    for r, i in enumerate(ids):
        hits = kd.find_n(Vector((S1[i, 0], S1[i, 1], 0.0)), 6)
        ww = np.array([1.0 / (d * d + 1e-8) for _c, _n, d in hits])
        rr = np.array([res[n] for _c, n, _d in hits])
        dz[r] = (coef[0] + coef[1] * S1[i, 0] + coef[2] * S1[i, 1] + float((ww * rr).sum() / ww.sum())) * fade[i]
    before = S1[bi, 2].copy()
    S1[ids, 2] += dz
    S1[bi, 2] = target
    L = float(np.ptp(S1[bi, 1]))
    log["sole"][sname] = {"floorBeforeMm": [mm(before.min() - floor_to), mm(before.max() - floor_to)],
                          "tiltBeforeMmOverLength": mm(abs(coef[2]) * L), "correctionMaxMm": mm(np.abs(dz).max()),
                          "floorAfterSpreadMm": mm(np.ptp(S1[bi, 2])), "floorAfterUnderBareMm": mm(floor_to - S1[bi, 2].mean())}
say("sole", json.dumps(log["sole"]))

for v, p in zip(shoe.data.vertices, S1):
    v.co = Vector(tuple(p))
shoe.data.update()

# ---- measures on both bodies: the ease, the toe allowance, the ball line -------------------------------------------


def foot_axis(P, J, sg):
    d = J["ball_" + ("l" if sg > 0 else "r")] - J["foot_" + ("l" if sg > 0 else "r")]
    d[2] = 0
    return d / np.linalg.norm(d)


def measures(P, N, S, J):
    bmx = bmesh.new()
    bmx.from_mesh(shoe.data)
    for v, p in zip(bmx.verts, S):
        v.co = Vector(tuple(p))
    bvh = BVHTree.FromBMesh(bmx)
    bmx.free()
    out = {}
    floor = float(P[:, 2].min())
    top = float(S[:, 2].max())
    for sg, sname in ((1, "l"), (-1, "r")):
        ax = foot_axis(P, J, sg)
        ball = J["ball_" + sname]
        sel = np.where((P[:, 0] * sg > 0.02) & (P[:, 2] > floor + 0.008) & (P[:, 2] < top - 0.02) &
                       (canon == np.arange(len(P))))[0]
        behind = (P[sel] - ball) @ ax < 0
        gaps, gaps_front = [], []
        for i, b in zip(sel, behind):
            hit, nrm, _f, d = bvh.find_nearest(Vector(tuple(P[i])))
            if hit is None or d > 0.03:
                continue
            if (np.array(hit) - P[i]) @ N[i] <= 0:
                continue                      # the shoe's face found is not outward of the skin here
            (gaps if b else gaps_front).append(d)
        foot = P[(P[:, 0] * sg > 0.02) & (P[:, 2] < floor + 0.06)]
        sh = S[side_of == sg]
        tip_foot, tip_shoe = float((foot @ ax).max()), float((sh @ ax).max())
        heel_foot, heel_shoe = float((foot @ ax).min()), float((sh @ ax).min())
        g = np.array(gaps)
        out[sname] = {"easeBehindBallMm": [mm(np.percentile(g, q)) for q in (5, 50, 95)], "easePoints": int(len(g)),
                      "easeFrontOfBallMedianMm": mm(np.median(gaps_front)) if gaps_front else None,
                      "toeBeyondFootMm": mm(tip_shoe - tip_foot), "heelBehindFootMm": mm(heel_foot - heel_shoe),
                      "footLengthMm": mm(tip_foot - heel_foot), "shoeLengthMm": mm(tip_shoe - heel_shoe),
                      "shoeTopAboveBareFloorMm": mm(float(sh[:, 2].max()) - floor)}
        # where the ball's weight crosses one half, along the foot, against the ball joint
        gi = GROUPS.index("ball_" + sname)
        half = np.where((side_of == sg) & (np.abs(W0[:, gi] - 0.5) < 0.12))[0]
        if len(half):
            out[sname]["ballHalfLineFromJointMm"] = mm(float(np.median((S[half] - ball) @ ax)))
    return out


log["fit"] = {"first": measures(PR, NR, S0, JR), "second": measures(PT, NT, S1, JT)}
say("fit", json.dumps(log["fit"]))

# ---- the weights as they were, on the second body's skeleton -------------------------------------------------------
W1 = np.zeros_like(W0)
for v in shoe.data.vertices:
    for g in v.groups:
        W1[v.index, g.group] = g.weight
log["weights"] = {"samePointForPoint": bool(np.array_equal(W0, W1)), "groups": [g.name for g in shoe.vertex_groups],
                  "maxInfluences": int((W1 > 1e-6).sum(axis=1).max()),
                  "sumMin": round(float(W1.sum(axis=1).min()), 4), "sumMax": round(float(W1.sum(axis=1).max()), 4),
                  "bonesInSkeleton": all(n in arm.data.bones for n in GROUPS)}
if not log["weights"]["samePointForPoint"] or not log["weights"]["bonesInSkeleton"]:
    raise SystemExit("CARRYFOOT the weights changed or a bone is missing: %s" % json.dumps(log["weights"]))
for mat in shoe.data.materials:
    c = COLOURS.get(mat.name)
    if not c:
        continue
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    rgb = tuple(float(x) for x in c["rgb"])
    if bsdf is not None:
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = float(c.get("rough", bsdf.inputs["Roughness"].default_value))
        bsdf.inputs["Metallic"].default_value = float(c.get("metal", 0.0))
    mat.diffuse_color = (*rgb, 1.0)
    mat.roughness = float(c.get("rough", mat.roughness))
    mat.metallic = float(c.get("metal", 0.0))
log["materials"] = {}
for mat in shoe.data.materials:
    bsdf = mat.node_tree.nodes.get("Principled BSDF") if mat.use_nodes else None
    log["materials"][mat.name] = {"baseLinear": [round(x, 4) for x in (bsdf.inputs["Base Color"].default_value[:3] if bsdf else mat.diffuse_color[:3])],
                                  "rough": round(bsdf.inputs["Roughness"].default_value, 3) if bsdf else None,
                                  "metal": round(bsdf.inputs["Metallic"].default_value, 3) if bsdf else None}
shoe.name = NAME
shoe.data.name = NAME
bpy.ops.object.select_all(action="DESELECT")
shoe.select_set(True)
bpy.context.view_layer.objects.active = shoe
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_static.fbx"), use_selection=True, object_types={"MESH"},
                         mesh_smooth_type="FACE", add_leaf_bones=False)
shoe.parent = arm
shoe.matrix_parent_inverse = arm.matrix_world.inverted()
mod = shoe.modifiers.new("Armature", "ARMATURE")
mod.object = arm
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
shoe.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_skinned.fbx"), use_selection=True,
                         object_types={"ARMATURE", "MESH"}, add_leaf_bones=False, mesh_smooth_type="FACE",
                         bake_anim=False, colors_type="LINEAR")
log["files"] = [NAME + "_skinned.fbx", NAME + "_static.fbx", NAME + ".blend"]
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "carry.json"), "w"), indent=1)
say("done", json.dumps({k: log[k] for k in ("moves", "weights")}))
