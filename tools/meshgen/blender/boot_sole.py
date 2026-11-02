"""A finished, skinned pair of boots given a thinner sole and a narrower welt ledge round the toe: only the sole's points
move (the sole is one piece per boot: a welt-top ring over a tread ring, joined by a wall, each ring closed by a cap),
and only their positions, so faces, UVs, material slots and weights stay those of the pair it was given, its baked maps
and its skinning still hold, and the upper, the insole, the eyelets and the laces do not move at all.

    blender -b --factory-startup -P tools/meshgen/blender/boot_sole.py -- PAIR_SKINNED.fbx FULL_BODY.fbx OUT_DIR
        [--name tom_boots] [--out-version v4] [--ball 0.012] [--ledge 0.0025] [--ledge-min 0.002]
        [--toe-from 0.02] [--toe-full 0.05] [--clear 0.004] [--measure-only] [--no-preview] [--debug-stretch]
    python tools/meshgen/blender/boot_sole.py --selftest        (the moves' arithmetic, without Blender)

    Tom's v4 (2 November): -- F:/LedgerTools/garments/tom/boots/maps/tom_boots_skinned_v3.fbx
        F:/LedgerTools/bodies/MH_TomL1/MH_TomL1_FullBody.fbx F:/LedgerTools/garments/tom/boots/maps
    (--measure-only prints the measures and writes nothing; --debug-stretch prints each moved triangle over 1.2.)

WHY, 2 November 2026 (Tom's boots, his order C9; his yes of 2 November 14:56 to a fourth try at the heavy look): after
v3 lowered and rounded the toe (boot_toe.py), two fresh reviewers still read the boots as clog-like, now because of the
sole: a slab 17 to 20 mm thick all round, and a welt ledge standing out round the toe
(F:/LedgerTools/gate/new/tom-outfit/2026-11-02-toe3/review-tom-boots.json, review-tom-whole.json).

TARGETS AND WHERE THEY COME FROM (production/research/clothing-pipeline/FOOTWEAR-2026-09-30.md; SHOE-TOE-AND-LACING-
2026-09-30.md and EPIC-BOOTS-ON-TOM-2026-11-02.md hold no sole or welt number, the latter lists Epic's sole depth as
not checked, and the pictures of Epic's boot look down at about 30 degrees, from which its sole's wall cannot be told
from its welt's top):
- the sole 12 mm at the ball (--ball): the brief's number; FOOTWEAR gives a Dr Martens sole of about 15 mm (D), a work
  boot's visible forepart 15 mm on a 28 mm heel stack (I) and a derby's 6 to 8 mm sole on a 20 to 25 mm heel (I), so 12
  lies between a derby's sole with its welt and a work boot's. The floor stays one flat plane (FOOTWEAR's recipe: the
  sole's bottom one plane, parallel to the bare sole), so every tread point rises by the same amount; the heel, whose
  welt top stands 3 mm above the forepart's, keeps 3 mm more than the ball (heels are thicker than foreparts in every
  number above), the waist keeps its lift off the floor and the toe its spring exactly. The rise is rounded so the
  floor drops a whole mm under the bare foot's floor (raise_mm is whole mm).
- the ledge 2.5 mm proud of the upper at the toe (--ledge): no documented number was found (the Mafia and Kingdom Come
  II study 06 gives shoes' triangles and textures, no sole or welt measure; FOOTWEAR's "extend the upper's outline 3-5 mm for the welt edge" is its helper's
  inference for a first scripted build); the brief's 2 to 3 mm, its middle. No point is brought nearer than
  --ledge-min (2 mm).
  Behind the toe the ledge is left as it is (fully trimmed from --toe-full ahead of the ball joint, untouched behind
  --toe-from, a smoothstep between).

THE MOVES, each boot in its own frame from the skeleton's rest pose (along the foot from the foot joint's head to the
ball joint's, flat; across it, outward; up), s the distance ahead of the ball joint:
1. THE TREAD RAISED: every point of the tread ring (the sole's lower ring and its cap) up by one amount d, the ball's
   median thickness less --ball, rounded as above. The welt top, which the upper and the insole stand on, stays.
2. THE LEDGE TRIMMED: for each point of the welt-top ring, the ledge is how far it stands outside the upper's outermost
   point in the vertical plane across the ring there, within the upper's lowest 10 mm over it (the join: at the toe
   the upper's wall leans back from its foot, so this is its foot). The record gives it seen from above too (the
   upper's outermost within 30 mm: at the ball the leather bulges out over a foot tucked in 11 mm). The trim, w(s)
   times what stands beyond --ledge, is smoothed along the ring over a point either side and held within its bounds
   (nothing nearer than --ledge-min, nothing behind --toe-from), then HELD: wherever a moved triangle would stretch
   over 1.24 (area or edges) or turn over, the trims of its corners are eased towards its least-moved corner's, round
   after round until none does. Each cap is one ring closed by thin triangles with no point inside, so a trim unlike
   its neighbours' bends them: beside the toe's inner front corner, whose ledge is already 1.6 to 1.9 mm and stays,
   the first run stretched six to 1.5, and smoothing the trim over up to 6 points still left one at 1.27 while
   trimming almost nothing. The trim moves the column (the welt-top point and the tread point under it) in along the
   ring's flat normal, so the wall stays upright. The welt-top point takes the old cap's height at its new place (the
   surface the upper stands on stays where it was); the tread point keeps its height, so the spring's profile behind
   the tip is kept.
Nothing else moves. Normals are recomputed as boot_toe.py did (smooth, hard only along the pair's own hard edges).

CHECKED, each before and after: the sole's thickness at the ball, the waist, the heel and the tip; the ledge at the toe
tip, the toe's sides, the ball's sides and the heel; the floor under the bare foot's floor (the full body's LOD0 lowest
point, as carry_footwear.py and the v2 record measured it) and the raise it needs; the toe's height above the floor
and its spring; the clearance of every moved point to the foot's skin (none brought under --clear that was not);
each face's 3D area against its UV area and its largest edge stretch (flagged over 1.25); faces turned over; the sole
one closed piece with every column of positive thickness; the upper's points under the welt's top; counts, UVs,
weights, bones and material slots read back from the written file against the pair given; the floor footprints
(sole_footprints.py's measure).

OUT_DIR gets NAME_skinned_V.fbx (written as v2 and v3 were: smoothing by face, no leaf bones, no animation),
boot-sole-record.json and boot-sole-preview.png (the left boot, side and three-quarter: the pair given, the new, and
the two outlines over each other, each standing on its own floor; Cycles on the CPU, a plain grey material).
"""
import json
import math
import os
import sys

import numpy as np

try:
    import bmesh
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    from mathutils.kdtree import KDTree
except ImportError:                                       # --selftest runs without Blender
    bpy = None


# ---- the arithmetic of the moves (no Blender; --selftest checks these) -------------------------------------------------
def smoothstep(a, b, x):
    t = np.clip((np.asarray(x, dtype=float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def plan_normals(P):
    """Outward flat normals of a closed ring of points (n, 3) given in order, either winding."""
    P = np.asarray(P, float)
    t = np.roll(P, -1, 0) - np.roll(P, 1, 0)
    t[:, 2] = 0.0
    t /= np.linalg.norm(t, axis=1)[:, None]
    n = np.stack([t[:, 1], -t[:, 0], np.zeros(len(t))], 1)
    x, y = P[:, 0], P[:, 1]
    area = 0.5 * float((x * np.roll(y, -1) - np.roll(x, -1) * y).sum())
    return (n if area > 0 else -n), t


def circ_fill(x):
    """Gaps (nan) in a closed ring's values filled by straight lines between the nearest known neighbours."""
    x = np.asarray(x, float).copy()
    ok = ~np.isnan(x)
    if ok.all() or not ok.any():
        return x
    i = np.arange(len(x))
    k = i[ok]
    return np.interp(i, np.concatenate([k - len(x), k, k + len(x)]), np.tile(x[ok], 3))


def circ_smooth(x, sigma):
    """A closed ring's values smoothed by a Gaussian over sigma points (0: unchanged)."""
    x = np.asarray(x, float)
    if sigma <= 0:
        return x.copy()
    r = int(math.ceil(3 * sigma))
    k = np.arange(-r, r + 1)
    w = np.exp(-0.5 * (k / sigma) ** 2)
    w /= w.sum()
    return sum(wj * np.roll(x, -kj) for kj, wj in zip(k, w))


def trim_profile(ledge, s, s_from, s_full, target, keep_min, sigma=1.0, rounds=6):
    """How far each welt-top ring point comes in: what stands beyond target, weighted by its place along the foot,
    then smoothed along the ring and held within its bounds, a few rounds (never bringing a point nearer the upper
    than keep_min, never outward, nothing behind s_from)."""
    led = circ_fill(ledge)
    w = smoothstep(s_from, s_full, s)
    hi = np.maximum(0.0, led - keep_min) * (np.asarray(s) > s_from)
    t = np.clip(w * np.maximum(0.0, led - target), 0.0, hi)
    for _ in range(rounds if sigma > 0 else 0):
        t = np.clip(circ_smooth(t, sigma), 0.0, hi)
    return t


def tread_rise(ball_thick, target, drop_now):
    """The rise of the tread: the ball's thickness less the target, rounded so the floor's drop under the bare floor
    (drop_now before) comes out in whole mm."""
    want = drop_now - (ball_thick - target)
    return drop_now - round(want * 1000.0) / 1000.0


def plane_extent(q, t, n, A, B, zlo=-0.001, zhi=0.010, nlo=-0.040, nhi=0.010):
    """The ledge at a ring point q: how far q stands outside the furthest (along n) crossing of the edges A-B with the
    vertical plane through q across the ring (normal t), within zlo..zhi above q and nlo..nhi along n. nan if none."""
    da, db = (A - q) @ t, (B - q) @ t
    m = da * db < 0
    if not m.any():
        return float("nan")
    tt = da[m] / (da[m] - db[m])
    X = A[m] + tt[:, None] * (B[m] - A[m])
    rn, rz = (X - q) @ n, X[:, 2] - q[2]
    k = (rn > nlo) & (rn < nhi) & (rz > zlo) & (rz < zhi)
    return float(-rn[k].max()) if k.any() else float("nan")


def selftest():
    ok = bad = 0

    def check(what, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("boot_sole selftest FAIL " + what)
    ang = np.linspace(0, 2 * np.pi, 40, endpoint=False)
    ring = np.stack([0.06 * np.cos(ang), 0.06 * np.sin(ang), np.zeros(40)], 1)
    for P in (ring, ring[::-1]):
        n, t = plan_normals(P)
        check("normals point out of a ring, either winding", np.allclose((n * P).sum(1) / 0.06, 1.0, atol=0.02))
        check("tangents are flat and across the normals", np.allclose((n * t).sum(1), 0.0) and np.allclose(t[:, 2], 0.0))
    check("a gap is filled between its neighbours, round the end too",
          np.allclose(circ_fill([1.0, np.nan, 3.0, 4.0]), [1, 2, 3, 4]) and np.allclose(circ_fill([np.nan, 2.0, 3.0, 4.0]), [3, 2, 3, 4]))
    check("smoothing keeps a constant and the total", np.allclose(circ_smooth(np.full(9, 2.0), 1.0), 2.0)
          and abs(circ_smooth(np.eye(1, 20, 5)[0], 1.0).sum() - 1.0) < 1e-9)
    s = np.array([-0.10, 0.0, 0.02, 0.035, 0.05, 0.08, 0.10])
    led = np.array([0.006, 0.004, 0.006, np.nan, 0.006, 0.0025, 0.0065])
    tr = trim_profile(led, s, 0.02, 0.05, 0.003, 0.002, sigma=0.0)
    check("nothing trimmed behind toe-from", tr[0] == 0.0 and tr[1] == 0.0 and tr[2] == 0.0)
    check("fully trimmed to the target ahead of toe-full", abs(tr[4] - 0.003) < 1e-9 and abs(tr[6] - 0.0035) < 1e-9)
    check("a ledge under the target is not pushed out or in", tr[5] == 0.0)
    check("a gap in the ledge is filled, then trimmed by its weight", 0.0 < tr[3] < 0.003)
    tr2 = trim_profile(led, s, 0.02, 0.05, 0.003, 0.002, sigma=1.5)
    check("smoothing never brings a point under keep-min", (np.nan_to_num(circ_fill(led)) - tr2 >= 0.002 - 1e-12).all()
          and (tr2 >= 0).all())
    check("smoothing reaches nothing behind toe-from", tr2[0] == 0.0 and tr2[1] == 0.0 and tr2[2] == 0.0)
    ss = np.linspace(-0.2, 0.1, 40)
    lw = 0.003 + 0.002 * (np.arange(40) % 2)                     # a ledge that zigzags point to point
    t1, t3 = (trim_profile(lw, ss, 0.02, 0.05, 0.0025, 0.002, sigma=sg) for sg in (1.0, 3.0))
    check("a wider smoothing leaves a smoother trim", np.abs(np.diff(t3, 2)).max() < np.abs(np.diff(t1, 2)).max())
    d = tread_rise(0.01697, 0.012, 0.0200)
    check("the rise brings the ball near the target and the drop to whole mm",
          abs(d - 0.005) < 1e-9 and abs(round((0.0200 - d) * 1000) - (0.0200 - d) * 1000) < 1e-6)
    # a ring 56 mm round an upright cylinder of the upper 50 mm round: a ledge of 6 mm everywhere
    h = np.linspace(0, 0.02, 5)
    cyl = np.array([[0.05 * math.cos(a), 0.05 * math.sin(a), z] for z in h for a in ang])
    A, B = [], []
    for zi in range(len(h)):
        for ai in range(40):
            i0 = zi * 40 + ai
            A.append(cyl[i0])
            B.append(cyl[zi * 40 + (ai + 1) % 40])
            if zi + 1 < len(h):
                A.append(cyl[i0])
                B.append(cyl[i0 + 40])
    A, B = np.array(A), np.array(B)
    rr = ring * (0.056 / 0.06)
    n, t = plan_normals(rr)
    le = [plane_extent(rr[k], t[k], n[k], A, B) for k in range(0, 40, 7)]
    check("the ledge round a cylinder reads its 6 mm", np.allclose(le, 0.006, atol=0.0003))
    check("no upper in the window reads nan", math.isnan(plane_extent(rr[0] + np.array([0, 0, 0.05]), t[0], n[0], A, B)))
    print("boot_sole selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__" and "--selftest" in sys.argv:
    sys.exit(selftest())
if bpy is None:
    sys.exit("boot_sole.py: run inside Blender (or with --selftest)")

# ---- the arguments ----------------------------------------------------------------------------------------------------
argv = sys.argv[sys.argv.index("--") + 1:]
PAIR, BODY, OUT = argv[:3]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
NAME = opt("--name", "tom_boots", str)
VER = opt("--out-version", "v4", str)
BALL = opt("--ball", 0.012)
LEDGE = opt("--ledge", 0.0025)
LEDGE_MIN = opt("--ledge-min", 0.002)
TOE_FROM, TOE_FULL = opt("--toe-from", 0.02), opt("--toe-full", 0.05)
CLEAR = opt("--clear", 0.004)
TOL = 0.00001
MEASURE_ONLY = "--measure-only" in argv
PREVIEW = "--no-preview" not in argv
os.makedirs(OUT, exist_ok=True)
Z = np.array([0.0, 0.0, 1.0])
REC = {"pair": PAIR, "body": BODY, "date": "2026-11-02",
       "params": dict(ballM=BALL, ledgeM=LEDGE, ledgeMinM=LEDGE_MIN, toeFromM=TOE_FROM, toeFullM=TOE_FULL, clearM=CLEAR)}


def say(*a):
    print("BOOTSOLE", *a, flush=True)


def mm(x):
    return round(float(x) * 1000, 2)


# ---- the full body: its feet and its floor (LOD0, rest pose) ----------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY)
body = next(o for o in bpy.data.objects if o.type == "MESH" and o.name.endswith("LOD0"))
BCO = np.array([body.matrix_world @ v.co for v in body.data.vertices])
BARE_FLOOR = float(BCO[:, 2].min())
BPOLY = [tuple(p.vertices) for p in body.data.polygons]
barm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
BBONES = {b.name: np.array(barm.matrix_world @ b.head_local) for b in barm.data.bones}
FOOT = {}
for side, sg in ((0, 1.0), (1, -1.0)):
    keep = (BCO[:, 0] * sg > 0.02) & (BCO[:, 2] < 0.16)
    polys = [p for p in BPOLY if all(keep[i] for i in p)]
    idx = np.unique(np.concatenate([np.array(p) for p in polys]))
    remap = -np.ones(len(BCO), dtype=np.int64)
    remap[idx] = np.arange(len(idx))
    FOOT[side] = dict(pts=BCO[idx], bvh=BVHTree.FromPolygons([Vector(p) for p in BCO[idx]],
                                                              [[int(remap[i]) for i in p] for p in polys]))
bpy.ops.wm.read_factory_settings(use_empty=True)
REC["bareFloorZmm (the full body's LOD0 lowest point)"] = mm(BARE_FLOOR)

# ---- the pair ------------------------------------------------------------------------------------------------------------
bpy.ops.import_scene.fbx(filepath=PAIR)
pair = next(o for o in bpy.data.objects if o.type == "MESH")
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
me = pair.data
assert np.allclose(np.array(pair.matrix_world), np.eye(4), atol=1e-6), "the pair's object transform is not identity"
CO0 = np.array([v.co[:] for v in me.vertices])
NV = len(CO0)
SLOT = {m.name.split(".")[0]: i for i, m in enumerate(me.materials)}
FMAT = np.array([p.material_index for p in me.polygons])
POLYS = [np.array(p.vertices) for p in me.polygons]
bm = bmesh.new()
bm.from_mesh(me)
bm.faces.ensure_lookup_table()
comp = np.full(len(me.polygons), -1)
comps = []
for f_ in bm.faces:
    if comp[f_.index] >= 0:
        continue
    st, cur = [f_], []
    comp[f_.index] = len(comps)
    while st:
        g = st.pop()
        cur.append(g.index)
        for v in g.verts:
            for h in v.link_faces:
                if comp[h.index] < 0:
                    comp[h.index] = len(comps)
                    st.append(h)
    comps.append(np.array(cur))
bm.free()
cverts = [np.unique(np.concatenate([POLYS[int(i)] for i in c])) for c in comps]
cmat = [int(np.bincount(FMAT[c]).argmax()) for c in comps]
cside = [0 if CO0[cv, 0].mean() > 0 else 1 for cv in cverts]
BONES = {b.name: np.array(arm.matrix_world @ b.head_local) for b in arm.data.bones}
REC["skeletonAgreesWithBodyMm"] = mm(max(np.abs(BONES[k] - BBONES[k]).max() for k in ("foot_l", "ball_l", "foot_r", "ball_r")))


def edges_of(faces):
    es = set()
    for fi in faces:
        pv = POLYS[int(fi)]
        for k in range(len(pv)):
            a_, b_ = int(pv[k]), int(pv[(k + 1) % len(pv)])
            es.add((min(a_, b_), max(a_, b_)))
    return np.array(sorted(es))


BOOT = {}
for side in (0, 1):
    sn = "l" if side == 0 else "r"
    up = [i for i in range(len(comps)) if cmat[i] == SLOT["M_Upper"] and cside[i] == side]
    so = [i for i in range(len(comps)) if cmat[i] == SLOT["M_Sole"] and cside[i] == side]
    assert len(up) == 1 and len(so) == 1, (up, so)
    uv_ = cverts[up[0]]
    nh = len(uv_) // 2
    outer, inner = uv_[:nh], uv_[nh:]
    F_, B_ = BONES["foot_" + sn], BONES["ball_" + sn]
    f = (B_ - F_) * np.array([1.0, 1.0, 0.0])
    f /= np.linalg.norm(f)
    a = np.array([-f[1], f[0], 0.0])
    if a @ (B_ * np.array([1.0, 1.0, 0.0])) < 0:
        a = -a
    sole = cverts[so[0]]
    # the sole: an outline extruded down, two rings and their caps; each point's column partner the other sole point
    # nearest it in plan
    p = CO0[sole]
    d2 = ((p[:, None, :2] - p[None, :, :2]) ** 2).sum(2)
    np.fill_diagonal(d2, np.inf)
    nn = d2.argmin(1)
    assert (nn[nn] == np.arange(len(sole))).all(), "the sole's points do not pair in columns"
    col = dict(zip(sole.tolist(), sole[nn].tolist()))
    is_top = p[:, 2] > p[nn, 2]
    top, bot = sole[is_top], sole[~is_top]
    topset = set(top.tolist())
    # the ring's order from the wall's faces (each joins two neighbouring welt-top points)
    adj = {int(v): set() for v in top}
    for fi in comps[so[0]]:
        tv = [int(v) for v in POLYS[int(fi)] if int(v) in topset]
        if len(tv) == 2:
            adj[tv[0]].add(tv[1])
            adj[tv[1]].add(tv[0])
    assert all(len(x) == 2 for x in adj.values()), "the welt-top ring is not one simple loop"
    order = [int(top[0])]
    prev = None
    while True:
        nx = [w for w in sorted(adj[order[-1]]) if w != prev]
        prev = order[-1]
        if nx[0] == order[0]:
            break
        order.append(nx[0])
    assert len(order) == len(top), "the welt-top ring does not walk round all its points"
    order = np.array(order)
    every = np.concatenate([cverts[i] for i in range(len(comps)) if cside[i] == side])
    BOOT[side] = dict(sn=sn, outer=outer, inner=inner, upper=uv_, sole=sole, top=top, bot=bot, col=col,
                      ring=order, ringbot=np.array([col[int(v)] for v in order]), every=every, ball=B_, f=f, a=a,
                      sole_faces=comps[so[0]], E_up=edges_of(comps[up[0]]), E_so=edges_of(comps[so[0]]),
                      faces=np.concatenate([comps[i] for i in range(len(comps)) if cside[i] == side]),
                      foot_tip_s=float(((FOOT[side]["pts"] - B_) @ f).max()))
    b = BOOT[side]
    b["E_out"] = b["E_up"][np.isin(b["E_up"][:, 0], outer) & np.isin(b["E_up"][:, 1], outer)]

for side, b in BOOT.items():          # which half lies nearer the foot (the lining): swap if the order says otherwise
    def near(ix):
        d = []
        for q in CO0[ix]:
            r = FOOT[side]["bvh"].find_nearest(Vector(q))
            d.append(r[3] if r[0] is not None else 1.0)
        return float(np.median(d))
    if near(b["outer"]) < near(b["inner"]):
        b["outer"], b["inner"] = b["inner"], b["outer"]
        b["E_out"] = b["E_up"][np.isin(b["E_up"][:, 0], b["outer"]) & np.isin(b["E_up"][:, 1], b["outer"])]


def s_of(q, b):
    return (np.asarray(q) - b["ball"]) @ b["f"]


def e_of(q, b):
    return (np.asarray(q) - b["ball"]) @ b["a"]


def section(co, E, b, s0):
    sa, sb = s_of(co[E[:, 0]], b), s_of(co[E[:, 1]], b)
    m = (sa - s0) * (sb - s0) < 0
    if not m.any():
        return np.zeros((0, 3))
    t = (s0 - sa[m]) / (sb[m] - sa[m])
    return co[E[m, 0]] + t[:, None] * (co[E[m, 1]] - co[E[m, 0]])


def ledges(co, b, zhi=0.010):
    """Each welt-top ring point's ledge (m) beyond the upper's outside within zhi over it, its outward normal and
    tangent."""
    P = co[b["ring"]]
    n, t = plan_normals(P)
    A, B = co[b["E_up"][:, 0]], co[b["E_up"][:, 1]]
    return np.array([plane_extent(P[k], t[k], n[k], A, B, zhi=zhi) for k in range(len(P))]), n, t


def groups(b, co):
    """The ring's points by place: the tip, the toe's sides, the ball's sides, the waist and the heel."""
    s = s_of(co[b["ring"]], b)
    stip = float(s_of(co[b["every"]], b).max())
    return {"tip (within 12 mm of the tip)": s > stip - 0.012,
            "toe sides (12 to 45 mm behind the tip)": (s <= stip - 0.012) & (s > stip - 0.045),
            "ball (within 15 mm of the ball joint)": np.abs(s) <= 0.015,
            "waist (40 to 110 mm behind the ball)": (s < -0.04) & (s > -0.11),
            "heel (over 150 mm behind the ball)": s < -0.15}


def stats(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if not len(x):
        return None
    return {"median": mm(np.median(x)), "min": mm(x.min()), "max": mm(x.max()), "n": int(len(x))}


def measure(co, tag):
    res = {}
    for side, b in BOOT.items():
        floor_ = float(co[b["sole"], 2].min())
        stip = float(s_of(co[b["every"]], b).max())
        th = co[b["ring"], 2] - co[b["ringbot"], 2]
        le, _, _ = ledges(co, b)
        la, _, _ = ledges(co, b, zhi=0.030)
        G = groups(b, CO0)                       # the same points before and after
        r = {"floorZmm": mm(floor_), "floorUnderBareFloorMm": mm(BARE_FLOOR - floor_),
             "soleThicknessMm (welt top over tread, at the ring)": {k: stats(th[m]) for k, m in G.items()},
             "ledgeMm (the welt beyond the upper's outside, at the join: its lowest 10 mm)": {
                 k: stats(le[m]) for k, m in G.items()},
             "ledgeSeenFromAboveMm (beyond the upper's outermost within 30 mm)": {
                 k: stats(la[m]) for k, m in G.items()},
             "ledgeUnreadPoints": int(np.isnan(le).sum()),
             "tipSmm": mm(stip), "beyondFootToesMm": mm(stip - b["foot_tip_s"])}
        prof = {}
        for d in (10, 30, 50):
            pu = section(co, b["E_out"], b, stip - d / 1000.0)
            prof[d] = mm(pu[:, 2].max() - floor_) if len(pu) else None
        r["toeTopAboveFloorMm (10, 30, 50 mm behind the tip)"] = prof
        sp = section(co, b["E_so"], b, stip - 0.001)
        r["toeSpringMm (underside 1 mm behind the tip, above the floor)"] = mm(sp[:, 2].min() - floor_) if len(sp) else None
        r["undersideAboveFloorMm (mm behind the tip)"] = {
            d: mm(section(co, b["E_so"], b, stip - d / 1000.0)[:, 2].min() - floor_)
            for d in (1, 10, 20, 40, 60, 80, 100) if len(section(co, b["E_so"], b, stip - d / 1000.0))}
        r["perRingPoint (s, thickness, ledge; mm)"] = [[mm(x), mm(y), (mm(z) if not np.isnan(z) else None)]
                                                       for x, y, z in zip(s_of(co[b["ring"]], b), th, le)]
        res["left" if side == 0 else "right"] = r
    REC.setdefault("measures", {})[tag] = res
    say(tag, json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "perRingPoint (s, thickness, ledge; mm)"}
                         for k, v in res.items()}))
    return res


def clearance(co, ix, side):
    out = np.empty(len(ix))
    for k, q in enumerate(co[ix]):
        r = FOOT[side]["bvh"].find_nearest(Vector(q))
        if r[0] is None:
            out[k] = 1.0
            continue
        out[k] = -r[3] if (Vector(q) - r[0]).dot(r[1]) < 0 else r[3]
    return out


def cap_bvh(b, co):
    bm_ = bmesh.new()
    vm = {}
    tops = set(b["top"].tolist())
    for fi in b["sole_faces"]:
        pv = me.polygons[int(fi)].vertices
        if not all(v in tops for v in pv):
            continue
        vs = []
        for v in pv:
            if v not in vm:
                vm[v] = bm_.verts.new(co[v])
            vs.append(vm[v])
        bm_.faces.new(vs)
    bm_.normal_update()
    t = BVHTree.FromBMesh(bm_)
    bm_.free()
    return t


def cap_z(bvh, pts):
    out = np.full(len(pts), np.nan)
    for i, q in enumerate(pts):
        hit = bvh.ray_cast(Vector((q[0], q[1], 0.3)), Vector((0, 0, -1)), 1.0)
        if hit[0] is not None:
            out[i] = hit[0].z
    return out


M0 = measure(CO0, "before")
if MEASURE_ONLY:
    sys.exit(0)

# ---- the moves -------------------------------------------------------------------------------------------------------------
ball_th = []
for b in BOOT.values():
    th = CO0[b["ring"], 2] - CO0[b["ringbot"], 2]
    ball_th.append(float(np.median(th[groups(b, CO0)["ball (within 15 mm of the ball joint)"]])))
floor0 = float(min(CO0[b["sole"], 2].min() for b in BOOT.values()))
D_RISE = tread_rise(float(np.mean(ball_th)), BALL, BARE_FLOOR - floor0)
REC["targets"] = {
    "soleAtBallMm": mm(BALL), "ledgeAtToeMm": mm(LEDGE), "ledgeNeverUnderMm": mm(LEDGE_MIN),
    "toeTrimFromToFullMmAheadOfBall": [mm(TOE_FROM), mm(TOE_FULL)],
    "sources": {
        "sole": "the brief's 12 mm; FOOTWEAR-2026-09-30.md: a Dr Martens sole about 15 mm (D, Dr. Martens 'Our soles'), "
                "a work boot's forepart 15 mm on a 28 mm heel stack (I), a derby's 6-8 mm sole on a 20-25 mm heel (I); "
                "the floor one flat plane (its recipe), so the heel keeps its 3 mm over the ball",
        "ledge": "none documented (FOOTWEAR-2026-09-30.md section C.5: the welt edge 3-5 mm beyond the upper's "
                 "outline, its helper's inference for a first scripted build); the brief's 2-3 mm, its middle",
        "epic": "none: EPIC-BOOTS-ON-TOM-2026-11-02.md lists Epic's sole depth as not checked; its pictures look down "
                "about 30 degrees, from which the sole's wall cannot be told from the welt's top",
        "derbyToe": "SHOE-TOE-AND-LACING-2026-09-30.md: no sole or welt number"}}
# the triangles and their UVs, for the stretch (each face's 3D area over its UV area, and its edges' stretch)
LV = np.zeros(len(me.loops), dtype=np.int64)
me.loops.foreach_get("vertex_index", LV)
UV = np.zeros(len(me.loops) * 2)
me.uv_layers[0].data.foreach_get("uv", UV)
UV = UV.reshape(-1, 2)
tri_l = []
for p in me.polygons:
    ls = list(range(p.loop_start, p.loop_start + p.loop_total))
    for k_ in range(1, len(ls) - 1):
        tri_l.append((ls[0], ls[k_], ls[k_ + 1], p.index))
tri_l = np.array(tri_l)
TV = LV[tri_l[:, :3]]
U_ = UV[tri_l[:, :3]]
AUV = 0.5 * np.abs((U_[:, 1, 0] - U_[:, 0, 0]) * (U_[:, 2, 1] - U_[:, 0, 1]) - (U_[:, 2, 0] - U_[:, 0, 0]) * (U_[:, 1, 1] - U_[:, 0, 1]))


def tri_area(co):
    return 0.5 * np.linalg.norm(np.cross(co[TV[:, 1]] - co[TV[:, 0]], co[TV[:, 2]] - co[TV[:, 0]]), axis=1)


A0 = tri_area(CO0)


def edge_stretch(i, co):
    def frame2(a, b, c):
        e1 = b - a
        n_ = np.cross(e1, c - a)
        x_ = e1 / np.linalg.norm(e1)
        y_ = np.cross(n_ / np.linalg.norm(n_), x_)
        return np.array([[e1 @ x_, (c - a) @ x_], [e1 @ y_, (c - a) @ y_]])
    J = frame2(*co[TV[i]]) @ np.linalg.inv(frame2(*CO0[TV[i]]))
    sv_ = np.linalg.svd(J, compute_uv=False)
    return sv_[0], sv_[1]


def stretch_of(co):
    """The moved triangles' area change (3D over UV, after against before) and edge stretch, and the worst of both."""
    mv = np.linalg.norm(co - CO0, axis=1) > 1e-7
    ok_ = mv[TV].any(1) & (AUV > 1e-12) & (A0 > 1e-12)
    ch = tri_area(co)[ok_] / A0[ok_]
    sv = np.array([edge_stretch(i, co) for i in np.where(ok_)[0]]) if ok_.any() else np.ones((0, 2))
    return ok_, ch, sv, float(max(ch.max() if len(ch) else 0.0, sv[:, 0].max() if len(sv) else 0.0))


VRK = {}                                                # a sole ring point: its boot and its place on the ring
for side_, b_ in BOOT.items():
    for k_, v_ in enumerate(b_["ring"]):
        VRK[int(v_)] = (side_, k_)
    for k_, v_ in enumerate(b_["ringbot"]):
        VRK[int(v_)] = (side_, k_)
LEDGE0, NRM0 = {}, {}
for side_, b_ in BOOT.items():
    LEDGE0[side_], NRM0[side_], _ = ledges(CO0, b_)
    b_["cap0"] = cap_bvh(b_, CO0)


def apply_trims(TR):
    """The tread up by D_RISE; each welt-top column in along the ring's flat normal by its trim."""
    co = CO0.copy()
    for side, b in BOOT.items():
        co[b["bot"], 2] += D_RISE                                    # 1. the tread up
        tr, n = TR[side], NRM0[side]                                # 2. the columns in
        newxy = CO0[b["ring"]] - tr[:, None] * n
        mv = tr > 1e-7
        zc = cap_z(b["cap0"], newxy[mv])
        for j, k in enumerate(np.where(mv)[0]):
            v, w = int(b["ring"][k]), int(b["ringbot"][k])
            co[v, :2] = newxy[k, :2]
            if not np.isnan(zc[j]):
                co[v, 2] = zc[j]                                     # the old cap's height at its new place
            co[w, :2] = CO0[w, :2] - tr[k] * n[k, :2]
    return co


def flagged(co, lim=1.24):
    """The moved triangles stretched over lim (area or edges) or turned over."""
    ok_, ch, sv, _ = stretch_of(co)
    ii = np.where(ok_)[0]
    n0 = np.cross(CO0[TV[ii, 1]] - CO0[TV[ii, 0]], CO0[TV[ii, 2]] - CO0[TV[ii, 0]])
    n1 = np.cross(co[TV[ii, 1]] - co[TV[ii, 0]], co[TV[ii, 2]] - co[TV[ii, 0]])
    turned_ = (n0 * n1).sum(1) <= 0
    return ii[(ch > lim) | (sv[:, 0] > lim) | turned_]


# the trims wanted, then HELD: wherever a moved triangle would stretch over 1.24 or turn over, the trims of its corners
# eased towards its least-moved corner's (each cap is one ring closed by thin triangles with no point inside, so a trim
# unlike its neighbours' bends them: next to the toe's inner front corner, where the ledge is already 1.6 to 1.9 mm and
# stays, the first run stretched six of them to 1.5)
TR = {}
for side, b in BOOT.items():
    TR[side] = trim_profile(LEDGE0[side], s_of(CO0[b["ring"]], b), TOE_FROM, TOE_FULL, LEDGE, LEDGE_MIN, sigma=1.0)
TR_WANTED = {k: v.copy() for k, v in TR.items()}
held_rounds = []
for rnd in range(80):
    CO = apply_trims(TR)
    bad = flagged(CO)
    held_rounds.append(int(len(bad)))
    if not len(bad):
        break
    for ti in bad:
        ks = [VRK[int(v)] for v in TV[ti] if int(v) in VRK]
        tmin = min(TR[sd][k] for sd, k in ks)
        for sd, k in ks:
            TR[sd][k] = tmin + 0.7 * (TR[sd][k] - tmin)
REC["moves"] = {"treadRiseMm (every tread point, both boots)": mm(D_RISE),
                "ballThicknessBeforeMm (median, left and right)": [mm(x) for x in ball_th],
                "heldRounds (triangles over 1.24 or turned, each round)": held_rounds}
for side, b in BOOT.items():
    nm = "left" if side == 0 else "right"
    tr, s = TR[side], s_of(CO0[b["ring"]], b)
    mvt = tr > 1e-7
    REC["moves"][nm] = {
        "ledgeTrimMm_max": mm(tr.max()), "ringPointsTrimmed": int(mvt.sum()), "ringPoints": int(len(tr)),
        "trimmedBetweenSmm": [mm(s[mvt].min()), mm(s[mvt].max())] if mvt.any() else None,
        "heldPoints (trim under 0.9 of the wanted)": int((tr < 0.9 * TR_WANTED[side] - 1e-6).sum()),
        "weltTopHeightChangeMm_min_max (the old cap's height at the new place)": [
            mm((CO[b["ring"], 2] - CO0[b["ring"], 2])[mvt].min()),
            mm((CO[b["ring"], 2] - CO0[b["ring"], 2])[mvt].max())] if mvt.any() else None,
        "trimMmPerRingPoint_wanted_used": [[mm(x), mm(y)] for x, y in zip(TR_WANTED[side], tr)]}
    say("moves", nm, json.dumps({k: x for k, x in REC["moves"][nm].items() if k != "trimMmPerRingPoint_wanted_used"}))
say("held rounds", held_rounds)
movedv = np.linalg.norm(CO - CO0, axis=1) > 1e-7
REC["moves"]["pointsMoved"] = int(movedv.sum())
REC["moves"]["pointsMovedOutsideTheSole"] = int(sum(int(movedv[np.setdiff1d(b["every"], b["sole"])].sum()) for b in BOOT.values()))
assert REC["moves"]["pointsMovedOutsideTheSole"] == 0

# ---- clearance to the foot ---------------------------------------------------------------------------------------------
for side, b in BOOT.items():
    nm = "left" if side == 0 else "right"
    ix = b["sole"]
    c0, c1 = clearance(CO0, ix, side), clearance(CO, ix, side)
    mv = movedv[ix]
    REC.setdefault("clearance", {})[nm] = {
        "soleMinMm_before_after": [mm(c0.min()), mm(c1.min())],
        "movedPointsMinMm_before_after": [mm(c0[mv].min()), mm(c1[mv].min())],
        "movedPointsUnder4mm_before_after": [int((mv & (c0 < CLEAR)).sum()), int((mv & (c1 < CLEAR)).sum())],
        "movedPointsNowUnder4mmThatWereNot": int((mv & (c1 < CLEAR) & (c0 >= CLEAR)).sum()),
        "movedPointsNearerThanBeforeAndUnder4mm": int((mv & (c1 < CLEAR) & (c1 < c0 - TOL)).sum()),
        "solePointsInsideTheFoot_before_after": [int((c0 < 0).sum()), int((c1 < 0).sum())]}
    say("clearance", nm, json.dumps(REC["clearance"][nm]))

M1 = measure(CO, "after")

# ---- the faces: turned over, stretched against their UVs --------------------------------------------------------------
okt, chg, svs, _ = stretch_of(CO)
if "--debug-stretch" in argv:
    ii = np.where(okt)[0]
    bad_ = np.where((chg > 1.2) | (svs[:, 0] > 1.2))[0]
    for j in bad_:
        tri = TV[ii[j]]
        e0 = CO0[tri]
        L = [np.linalg.norm(e0[x] - e0[(x + 1) % 3]) * 1000 for x in range(3)]
        rp = []
        for v in tri:
            for b in BOOT.values():
                for nmr, arr in (("top", b["ring"]), ("bot", b["ringbot"])):
                    w_ = np.where(arr == v)[0]
                    if len(w_):
                        rp.append("%s%d s%.0f" % (nmr, int(w_[0]), s_of(CO0[v], b) * 1000))
        say("debug tri", int(ii[j]), "area0 mm2 %.3f" % (A0[ii[j]] * 1e6), "edges mm", [round(x, 2) for x in L],
            "chg %.3f sv %.3f" % (chg[j], svs[j, 0]), rp,
            "moves mm", [round(float(np.linalg.norm(CO[v] - CO0[v])) * 1000, 3) for v in tri])
TPART = np.full(len(tri_l), "other", dtype=object)
for b in BOOT.values():
    TPART[np.isin(TV, b["top"]).all(1)] = "welt top (cap)"
    TPART[np.isin(TV, b["bot"]).all(1)] = "tread (cap)"
    TPART[np.isin(TV, b["sole"]).all(1) & ~np.isin(TV, b["top"]).all(1) & ~np.isin(TV, b["bot"]).all(1)] = "wall"
REC["stretch"] = {
    "trianglesTouchingMovedPoints": int(okt.sum()),
    "areaChange_max_min (3D over UV after, against before)": [round(float(chg.max()), 3), round(float(chg.min()), 3)],
    "areaChange_1_50_99pct": np.percentile(chg, [1, 50, 99]).round(3).tolist(),
    "over1.25": int((chg > 1.25).sum()), "under0.8": int((chg < 0.8).sum()),
    "edgeStretch_max_least (singular values)": [round(float(svs[:, 0].max()), 3), round(float(svs[:, 1].min()), 3)],
    "edgeStretchOver1.25": int((svs[:, 0] > 1.25).sum()),
    "flaggedOver1.25 (area or edge)": bool((chg > 1.25).any() or (svs[:, 0] > 1.25).any()),
    "byPart: area change max, min; edge stretch max, least; triangles": {}}
for nm_ in ("wall", "welt top (cap)", "tread (cap)"):
    m_ = TPART[okt] == nm_
    if m_.any():
        REC["stretch"]["byPart: area change max, min; edge stretch max, least; triangles"][nm_] = [
            round(float(chg[m_].max()), 3), round(float(chg[m_].min()), 3), round(float(svs[m_, 0].max()), 3),
            round(float(svs[m_, 1].min()), 3), int(m_.sum())]
say("stretch", json.dumps(REC["stretch"]))


def newell(co, p):
    pts = co[list(p.vertices)]
    n_ = np.zeros(3)
    for k_ in range(len(pts)):
        n_ += np.cross(pts[k_], pts[(k_ + 1) % len(pts)])
    return n_


turned, worst = 0, 0.0
for p in me.polygons:
    if not movedv[list(p.vertices)].any():
        continue
    n0_, n1_ = newell(CO0, p), newell(CO, p)
    if np.linalg.norm(n0_) < 1e-14 or np.linalg.norm(n1_) < 1e-14:
        turned += 1
        continue
    c_ = n0_ @ n1_ / np.linalg.norm(n0_) / np.linalg.norm(n1_)
    turned += int(c_ < 0)
    worst = max(worst, math.degrees(math.acos(max(-1.0, min(1.0, c_)))))
REC["faces"] = {"turnedOverOrCollapsed": turned, "mostTurnedDeg": round(worst, 1)}

# the sole: one closed piece, every column thick; the upper's points under the welt's top (the notch of 30 October)
REC["sole"] = {}
for side, b in BOOT.items():
    nm = "left" if side == 0 else "right"
    ec_ = {}
    for fi in b["sole_faces"]:
        pv = POLYS[int(fi)]
        for k_ in range(len(pv)):
            e_ = (min(pv[k_], pv[(k_ + 1) % len(pv)]), max(pv[k_], pv[(k_ + 1) % len(pv)]))
            ec_[e_] = ec_.get(e_, 0) + 1
    th0 = np.array([CO0[v, 2] - CO0[b["col"][int(v)], 2] for v in b["top"]])
    th1 = np.array([CO[v, 2] - CO[b["col"][int(v)], 2] for v in b["top"]])
    po0, po1 = CO0[b["upper"]], CO[b["upper"]]
    cz0, cz1 = cap_z(cap_bvh(b, CO0), po0), cap_z(cap_bvh(b, CO), po1)
    below0 = ~np.isnan(cz0) & (po0[:, 2] < cz0 - 0.0002)
    below1 = ~np.isnan(cz1) & (po1[:, 2] < cz1 - 0.0002)
    out0 = ~np.isnan(cz0) & (po0[:, 2] < cz0 - 0.0002) & np.isin(b["upper"], b["outer"])
    out1 = ~np.isnan(cz1) & (po1[:, 2] < cz1 - 0.0002) & np.isin(b["upper"], b["outer"])
    REC["sole"][nm] = {"openEdges": int(sum(1 for c in ec_.values() if c != 2)), "pieces": 1,
                       "columnThicknessMinMm_before_after": [mm(th0.min()), mm(th1.min())],
                       "upperPointsUnderTheWeltTop_before_after (both halves)": [int(below0.sum()), int(below1.sum())],
                       "outsidePointsUnderTheWeltTop_before_after": [int(out0.sum()), int(out1.sum())],
                       "deepestUnderMm_before_after": [mm(-(po0[below0, 2] - cz0[below0]).min()) if below0.any() else 0.0,
                                                       mm(-(po1[below1, 2] - cz1[below1]).min()) if below1.any() else 0.0]}
say("faces", json.dumps(REC["faces"]), "sole", json.dumps(REC["sole"]))

# ---- normals: smooth from the new points, hard only along the pair's own hard edges (read from its normals) ---------
N_ORIG = np.zeros(len(me.loops) * 3)
me.corner_normals.foreach_get("vector", N_ORIG)
N_ORIG = N_ORIG.reshape(-1, 3)
SHARP = set()
_bm = bmesh.new()
_bm.from_mesh(me)
for e_ in _bm.edges:
    lf = e_.link_faces
    if len(lf) != 2:
        continue
    for v in e_.verts:
        la = next(l_ for l_ in lf[0].loops if l_.vert == v)
        lb = next(l_ for l_ in lf[1].loops if l_.vert == v)
        if N_ORIG[la.index] @ N_ORIG[lb.index] < math.cos(math.radians(1.0)):
            SHARP.add(tuple(sorted((e_.verts[0].index, e_.verts[1].index))))
            break
_bm.free()


def recompute_normals(ob):
    m = ob.data
    bm_ = bmesh.new()
    bm_.from_mesh(m)
    for e_ in bm_.edges:
        e_.smooth = tuple(sorted((e_.verts[0].index, e_.verts[1].index))) not in SHARP
    for f_ in bm_.faces:
        f_.smooth = True
    bm_.to_mesh(m)
    bm_.free()
    if m.has_custom_normals:
        bpy.context.view_layer.objects.active = ob
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
    m.update()


bpy.context.view_layer.objects.active = pair
for v, c in zip(me.vertices, CO):
    v.co = Vector(c)
me.update()
recompute_normals(pair)
N_NEW = np.zeros(len(me.loops) * 3)
me.corner_normals.foreach_get("vector", N_NEW)
N_NEW = N_NEW.reshape(-1, 3)
still = ~movedv[LV]
ang1 = np.degrees(np.arccos(np.clip((N_ORIG * N_NEW).sum(1), -1, 1)))
REC["normals"] = {"unmovedCornersChangeDeg_max": round(float(ang1[still].max()), 3),
                  "unmovedCornersChangeDeg_99pct": round(float(np.percentile(ang1[still], 99)), 3),
                  "movedCornersChangeDeg_50_99_max": np.percentile(ang1[~still], [50, 99, 100]).round(2).tolist(),
                  "hardEdgesKept": len(SHARP)}
say("normals", json.dumps(REC["normals"]))

# ---- the export, as v2 and v3 were written, then read back against the pair given -------------------------------------
path = os.path.join(OUT, "%s_skinned_%s.fbx" % (NAME, VER))
for o in bpy.context.view_layer.objects:
    o.select_set(False)
arm.select_set(True)
pair.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.fbx(filepath=path, use_selection=True, object_types={"ARMATURE", "MESH"}, add_leaf_bones=False,
                         mesh_smooth_type="FACE", bake_anim=False, colors_type="LINEAR")


def read(p_):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=p_)
    m_ = next(o for o in bpy.data.objects if o.type == "MESH")
    a_ = next(o for o in bpy.data.objects if o.type == "ARMATURE")
    gn = {g.index: g.name for g in m_.vertex_groups}
    W = {}
    for v in m_.data.vertices:
        for g in v.groups:
            W[(v.index, gn[g.group])] = g.weight
    uv = np.zeros(len(m_.data.loops) * 2)
    m_.data.uv_layers[0].data.foreach_get("uv", uv)
    lv = np.zeros(len(m_.data.loops), dtype=np.int64)
    m_.data.loops.foreach_get("vertex_index", lv)
    fm = np.zeros(len(m_.data.polygons), dtype=np.int64)
    m_.data.polygons.foreach_get("material_index", fm)
    return dict(co=np.array([m_.matrix_world @ v.co for v in m_.data.vertices]), W=W, uv=uv, lv=lv, fm=fm,
                uvn=len(m_.data.uv_layers), faces=len(m_.data.polygons), mats=[x.name.split(".")[0] for x in m_.data.materials],
                groups=sorted(gn.values()), bones={bn.name: np.array(a_.matrix_world @ bn.head_local) for bn in a_.data.bones},
                bonetails={bn.name: np.array(a_.matrix_world @ bn.tail_local) for bn in a_.data.bones})


o_, n_ = read(PAIR), read(path)
keys = set(o_["W"]) | set(n_["W"])
REC["export"] = {
    "written": path, "points_given_written": [len(o_["co"]), len(n_["co"])], "faces_given_written": [o_["faces"], n_["faces"]],
    "materials_given_written": [o_["mats"], n_["mats"]], "materialPerFaceSame": bool(np.array_equal(o_["fm"], n_["fm"])),
    "uvLayers": [o_["uvn"], n_["uvn"]], "loopsSame": bool(np.array_equal(o_["lv"], n_["lv"])),
    "maxUvChange": float(np.abs(o_["uv"] - n_["uv"]).max()),
    "groupsSame": o_["groups"] == n_["groups"], "weightsCompared": len(keys),
    "maxWeightChange": float(max(abs(o_["W"].get(k, 0.0) - n_["W"].get(k, 0.0)) for k in keys)),
    "bones": [len(o_["bones"]), len(n_["bones"])], "boneNamesSame": sorted(o_["bones"]) == sorted(n_["bones"]),
    "maxBoneMoveMm (heads and tails)": round(float(max(max(np.abs(o_["bones"][k] - n_["bones"][k]).max(),
                                                           np.abs(o_["bonetails"][k] - n_["bonetails"][k]).max())
                                                       for k in o_["bones"])) * 1000, 6),
    "pointsGivenReadBackMaxErrMm": round(float(np.abs(o_["co"] - CO0).max() * 1000), 6),
    "pointsWrittenAsMovedMaxErrMm": round(float(np.abs(n_["co"] - CO).max() * 1000), 6),
    "pointsMoved": int(movedv.sum())}
say("export", json.dumps(REC["export"], default=str))


# ---- the floor, the raise, the footprints (sole_footprints.py's measure, the contact decals) -----------------------------
def footprints(P, rise=0.025, overlap=0.01):
    out = {}
    for sn in ("l", "r"):
        Fh, Bh = BONES["foot_" + sn], BONES["ball_" + sn]
        sidep = P[(P[:, 0] > 0) == (Bh[0] > 0)]
        low = sidep[sidep[:, 2] < sidep[:, 2].min() + rise]
        f = (Bh - Fh) * np.array([1.0, 1.0, 0.0])
        f /= np.linalg.norm(f)
        a = np.array([-f[1], f[0], 0.0])
        if a @ (Bh * np.array([1.0, 1.0, 0.0])) < 0:
            a = -a
        u, v = (low - Bh) @ f, (low - Bh) @ a
        out[sn] = {"floor_cm": round(float(sidep[:, 2].min()) * 100, 2),
                   "parts [heel half, ball half] each [along min, max, across min, max] cm": [
                       [round(float(u[sel].min()) * 100, 2), round(float(u[sel].max()) * 100, 2),
                        round(float(v[sel].min()) * 100, 2), round(float(v[sel].max()) * 100, 2)]
                       for sel in (u <= overlap, u >= -overlap)]}
    return out


fl0, fl1 = float(CO0[:, 2].min()), float(n_["co"][:, 2].min())
drop0, drop1 = BARE_FLOOR - fl0, BARE_FLOOR - fl1
REC["raise"] = {
    "bareFloorZmm": mm(BARE_FLOOR), "soleFloorZmm_given_new": [mm(fl0), mm(fl1)],
    "soleUnderBareFloorMm_given_new": [mm(drop0), mm(drop1)],
    "raiseMmNow (garments.json TomBoots)": 17,
    "raiseMmForV4_keepingTheSame3mmSink": int(round(drop1 * 1000)) - 3,
    "raiseMmForV4_standingExactlyOnTheGround": int(round(drop1 * 1000)),
    "why": "v2 and v3 stood 20 mm under the bare floor and Tom is raised 17 (30 October: the soles set 3 mm into the "
           "ground against the pale band under them); the same sink with v4 is its drop less 3"}
fp0, fp1 = footprints(o_["co"]), footprints(n_["co"])
REC["footprints"] = {"given": fp0, "new": fp1,
                     "largestChangeMm (along and across)": round(max(
                         abs(x - y) for sn in fp0 for h0, h1 in zip(
                             fp0[sn]["parts [heel half, ball half] each [along min, max, across min, max] cm"],
                             fp1[sn]["parts [heel half, ball half] each [along min, max, across min, max] cm"])
                         for x, y in zip(h0, h1)) * 10, 2)}
say("raise", json.dumps(REC["raise"]), "footprints", json.dumps(REC["footprints"]))
json.dump(REC, open(os.path.join(OUT, "boot-sole-record.json"), "w"), indent=1, default=str)


# ---- the preview: the left boot, side and three-quarter, the pair given, the new, and the two over each other -----------
def preview():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scn = bpy.context.scene
    b = BOOT[0]
    keep = np.zeros(NV, bool)
    keep[b["every"]] = True
    remap = -np.ones(NV, dtype=np.int64)
    remap[keep] = np.arange(keep.sum())
    faces = [[int(remap[v]) for v in POLYS[int(fi)]] for fi in b["faces"]]
    sharp = [(int(remap[x]), int(remap[y])) for x, y in SHARP if keep[x] and keep[y]]

    def mat(name, rgb, rough=0.55):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bs = m.node_tree.nodes["Principled BSDF"]
        bs.inputs["Base Color"].default_value = (*rgb, 1)
        bs.inputs["Roughness"].default_value = rough
        return m

    grey = mat("grey", (0.30, 0.30, 0.30))
    floor_given = float(CO0[b["sole"], 2].min())
    floor_new = float(CO[b["sole"], 2].min())

    def boot_obj(name, co, m, dz):
        md = bpy.data.meshes.new(name)
        md.from_pydata([tuple(c) for c in (co[keep] + np.array([0.0, 0.0, dz]))], [], faces)
        md.update()
        ob = bpy.data.objects.new(name, md)
        scn.collection.objects.link(ob)
        for p in md.polygons:
            p.use_smooth = True
        es = set(sharp) | set((y, x) for x, y in sharp)
        for e_ in md.edges:
            e_.use_edge_sharp = tuple(e_.vertices) in es
        md.materials.append(m)
        return ob

    # each stands on its own floor, as each would in the game with its own raise
    old, new = boot_obj("given", CO0, grey, 0.0), boot_obj("new", CO, grey, floor_given - floor_new)
    flm = mat("floor", (0.62, 0.62, 0.60), rough=0.8)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    fl = bpy.context.active_object
    fl.scale = (3.0, 3.0, 0.002)
    fl.location = (0, 0, floor_given - 0.001)
    fl.data.materials.append(flm)
    scn.render.engine = "CYCLES"
    scn.cycles.device = "CPU"
    scn.render.threads_mode, scn.render.threads = "FIXED", 4
    scn.cycles.use_denoising = True
    W_, H_ = 960, 560
    scn.render.resolution_x, scn.render.resolution_y = W_, H_
    scn.view_settings.view_transform = "AgX"
    w = bpy.data.worlds.new("sky")
    scn.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.82, 0.83, 0.85, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.8
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.0
    sun.data.angle = math.radians(8)
    scn.collection.objects.link(sun)
    cen = np.array([0.5 * (CO0[b["every"], 0].max() + CO0[b["every"], 0].min()),
                    0.5 * (CO0[b["every"], 1].max() + CO0[b["every"], 1].min()), floor_given + 0.075])
    f, a = b["f"], b["a"]
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    scn.collection.objects.link(cam)
    scn.camera = cam
    txt = bpy.data.curves.new("label", "FONT")
    tob = bpy.data.objects.new("label", txt)
    tm = bpy.data.materials.new("ink")
    tm.use_nodes = True
    nt = tm.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1)
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs[0])
    txt.materials.append(tm)
    scn.collection.objects.link(tob)
    tob.parent = cam
    views = [("side", "ORTHO", Vector(cen + a * 1.0), 0.38, cen)]
    tcen = b["ball"] * np.array([1.0, 1.0, 0.0]) + f * 0.03 + Z * (floor_given + 0.04)
    dd = f * math.cos(math.radians(50)) + a * math.sin(math.radians(50))
    el = math.radians(25)
    views.append(("three-quarter", "PERSP", Vector(tcen + dd * 0.85 * math.cos(el) + Z * 0.85 * math.sin(el)), 80.0, tcen))
    gv, nv = VER_GIVEN, VER

    def shot(fp_, samples, transparent, show, label):
        for ob in (old, new):
            ob.hide_render = ob not in show
        fl.hide_render = transparent
        tob.hide_render = label is None
        if label is not None:
            txt.body = label
        scn.render.film_transparent = transparent
        scn.cycles.samples = samples
        scn.cycles.use_denoising = samples > 8
        scn.render.filepath = fp_
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(fp_)
        px = np.array(im.pixels[:], dtype=np.float32).reshape(H_, W_, 4)
        bpy.data.images.remove(im)
        os.remove(fp_)
        return px

    def outline(alpha):
        m_ = alpha > 0.5
        er = m_.copy()
        for ax in (0, 1):
            for sh in (1, -1):
                er &= np.roll(m_, sh, axis=ax)
        e_ = m_ & ~er
        e_ = e_ | np.roll(e_, 1, 0) | np.roll(e_, 1, 1) | np.roll(e_, -1, 0)
        e_[:2], e_[-2:], e_[:, :2], e_[:, -2:] = False, False, False, False
        return e_

    panels = []
    for vn, kind, loc, lens, aim in views:
        cam.data.type = kind
        if kind == "ORTHO":
            cam.data.ortho_scale = lens
            span = lens
        else:
            cam.data.lens = lens
            span = 0.5 * 36.0 / lens
        cam.location = loc
        cam.rotation_euler = (Vector(aim) - loc).to_track_quat("-Z", "Y").to_euler()
        sun.rotation_euler = (-(Vector(dd) * 2 + Vector((0, 0, 2.5)))).to_track_quat("-Z", "Y").to_euler()
        txt.size = span * 0.042
        tob.location = (-span * 0.47, span * 0.5 * H_ / W_ - span * 0.07, -0.5)
        tmp = os.path.join(OUT, "_preview_tmp.png")
        given = shot(tmp, 48, False, (old,), "%s (given), %s" % (gv, vn))
        newp = shot(tmp, 48, False, (new,), "%s (new), %s" % (nv, vn))
        base = shot(tmp, 48, False, (new,), "outlines: %s red, %s blue, %s" % (gv, nv, vn))
        mg = shot(tmp, 1, True, (old,), None)[..., 3]
        mn = shot(tmp, 1, True, (new,), None)[..., 3]
        over = base.copy()
        over[..., :3] = 0.55 * over[..., :3] + 0.45
        eg, en = outline(mg), outline(mn)
        over[eg, :3] = (0.85, 0.05, 0.03)
        over[en, :3] = (0.05, 0.25, 0.95)
        panels.append([given, newp, over])
    big = np.ones((H_ * 2, W_ * 3, 4), dtype=np.float32)
    for r_, row in enumerate(panels):
        for c_, px in enumerate(row):
            big[(1 - r_) * H_:(2 - r_) * H_, c_ * W_:(c_ + 1) * W_] = px
    big[..., 3] = 1.0
    big[:, W_ - 1:W_ + 1, :3] = 1.0
    big[:, 2 * W_ - 1:2 * W_ + 1, :3] = 1.0
    big[H_ - 1:H_ + 1, :, :3] = 1.0
    out_im = bpy.data.images.new("preview", W_ * 3, H_ * 2, alpha=False)
    out_im.pixels[:] = big.ravel()
    out_im.filepath_raw = os.path.join(OUT, "boot-sole-preview.png")
    out_im.file_format = "PNG"
    out_im.save()
    return out_im.filepath_raw


VER_GIVEN = os.path.splitext(os.path.basename(PAIR))[0].rsplit("_", 1)[-1]
if PREVIEW:
    REC["preview"] = {"file": preview(), "layout": "rows: side (orthographic, from the outside), three-quarter (ahead "
                      "and outside, 25 degrees up, nearer the toe); columns: %s as given, %s, %s with both outlines (%s red, "
                      "%s blue); each boot standing on its own floor (the new one lowered by its tread's rise), as each "
                      "stands in the game with its own raise" % (VER_GIVEN, VER, VER, VER_GIVEN, VER),
                      "boot": "left", "renderer": "Cycles on the CPU, 48 samples, a plain grey material"}
json.dump(REC, open(os.path.join(OUT, "boot-sole-record.json"), "w"), indent=1, default=str)
say("done", os.path.join(OUT, "boot-sole-record.json"))
