"""A finished, skinned pair of boots reshaped at the toe and the welt, its points moved and nothing else: the same
faces, UVs and weights, so its maps and its skinning still hold.

    blender -b --factory-startup -P tools/meshgen/blender/reshape_footwear.py -- PAIR_SKINNED.fbx BODY.blend BODY_OBJECT
        OUT_DIR --name tom_boots [--allowance 0.021] [--shorten-max 0.008] [--shorten-min 0.006] [--spring 0.003]
        [--nose 0.003] [--square 0.18] [--forepart-drop 0.003] [--welt 0.004] [--pinch 0.0006]
        [--check-blend PAIR.blend --check-object NAME]

WHY, 30 October 2026 (Ron's and Tom's boots, one mesh carried point for point, judged in the game by two fresh
reviewers once their maps were on): a dark notch at each toe tip, where the upper dips up to 1.4 mm below the welt's
top; and at a player's distance a clog or slipper, from a soft, low, rounded toe a touch long (28.5 mm beyond the
toes) and a thick smooth welt. The research's numbers (production/research/clothing-pipeline/FOOTWEAR-2026-09-30.md,
SHOE-TOE-AND-LACING-2026-09-30.md): 15 to 20 mm beyond the toes (a man's last 20 mm), 8 to 12 mm of toe spring for
the boot, a toe box 25 to 35 mm tall at the tip, the welt 3 to 5 mm beyond the upper, the forepart's visible sole
thinner than the heel (Ron 28 and 15 mm: "the upper comes down over the difference"), and "a crisp turn where the
upper meets the sole reads as a low toe from a distance".

Each boot in its own frame (along the foot from the heel, across it, up), measured against the wearer's own toes:
1. THE TOE SHORTENED in front of the toes only (from 4 mm behind their tips): the boot's points there drawn back by
   up to --shorten (so the toe stands --allowance beyond the toes, held between the min and max), the most at the
   tip, a quadratic ease, so the nose is pressed blunter; and widened about its middle by up to --square at the tip
   (a squarer-round derby toe in plan), the welt with it.
2. THE NOSE RAISED by up to --nose on its upper part (its foot stays on the welt) and THE TOE SPRUNG by --spring more
   at the tip, the whole toe lifted from the toes forward (so the insole under the toes barely moves).
3. THE FOREPART'S SOLE THINNER: the welt's top lowered by --forepart-drop in front of the heel's breast (over 15 mm),
   the upper's foot and its insole coming down with it, so the heel stands that much thicker (a heel step).
4. THE WELT: its edge drawn in where it stands more than --welt beyond the upper (by at most 2 mm, top and bottom
   together), and a crisp turn: the upper's leather pinched in by --pinch just above the welt.
5. THE UPPER MEETS THE WELT ALL ROUND: every point of the upper inside the welt's outline and below its top lifted
   onto it, or up to 0.8 mm above it set down on it, the lining with it; and the upper's foot (its faces lying on the
   welt, facing down) hard-edged from its walls, so the walls' normals face out (the notch: the toe's lowest row and
   tip had taken the bottom into their smooth normals, 30 to 60 degrees down, drawn as a dark triangle).
Every move of an outer point is given to its lining partner too, so the leather keeps its thickness exactly. The
normals are recomputed from the new points, hard only along the original's own hard edges; checked on the original
first. --check-blend writes a copy of the pair's pose-check scene with the new points (for
footwear_pose_check.py), the body's mask taken off.

OUT_DIR gets NAME_skinned_v2.fbx and reshape.json (the toe's numbers before and after, the notch, the welt, folds,
and the export compared point for point: weights, UVs, faces, bones).
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

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, BODY, BODY_OBJ, OUT = argv[:4]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
NAME = opt("--name", "boots", str)
ALLOW = opt("--allowance", 0.021)
SH_MAX, SH_MIN = opt("--shorten-max", 0.008), opt("--shorten-min", 0.006)
SPRING = opt("--spring", 0.003)
NOSE = opt("--nose", 0.003)
SQUARE = opt("--square", 0.08)                     # (0.18 at first: a square box toe, more than "squarer-round")
FDROP = opt("--forepart-drop", 0.003)
WELT = opt("--welt", 0.004)
PINCH = opt("--pinch", 0.0006)
CHECK_BLEND = opt("--check-blend", "", str)
CHECK_OBJ = opt("--check-object", "", str)
os.makedirs(OUT, exist_ok=True)
LOG = {"src": SRC, "params": dict(allowance=ALLOW, spring=SPRING, nose=NOSE, square=SQUARE, forepartDrop=FDROP,
                                  welt=WELT, pinch=PINCH)}
Z = np.array([0.0, 0.0, 1.0])


def say(*a):
    print("RESHAPE", *a, flush=True)


def smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ---- the wearer's feet (positions only) ------------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(BODY, link=False) as (src_, dst_):
    dst_.objects = [n for n in src_.objects if n in (BODY_OBJ, "root")]
for o in dst_.objects:
    bpy.context.scene.collection.objects.link(o)
bpy.context.view_layer.update()
bo = next(o for o in dst_.objects if o.type == "MESH")
BCO = np.array([bo.matrix_world @ v.co for v in bo.data.vertices])
bpy.ops.wm.read_factory_settings(use_empty=True)

# ---- the pair -----------------------------------------------------------------------------------------------------
bpy.ops.import_scene.fbx(filepath=SRC)
pair = next(o for o in bpy.data.objects if o.type == "MESH")
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
me = pair.data
MW = np.array(pair.matrix_world)
assert np.allclose(MW, np.eye(4), atol=1e-6), "the pair's object transform is not identity"
CO0 = np.array([v.co[:] for v in me.vertices])
SLOT = {m.name.split(".")[0]: i for i, m in enumerate(me.materials)}
FMAT = np.array([p.material_index for p in me.polygons])
bm = bmesh.new()
bm.from_mesh(me)
bm.faces.ensure_lookup_table()
bm.verts.ensure_lookup_table()
comp = np.full(len(me.polygons), -1)
comps = []
for f in bm.faces:
    if comp[f.index] >= 0:
        continue
    st, cur = [f], []
    comp[f.index] = len(comps)
    while st:
        g = st.pop()
        cur.append(g.index)
        for v in g.verts:
            for h in v.link_faces:
                if comp[h.index] < 0:
                    comp[h.index] = len(comps)
                    st.append(h)
    comps.append(np.array(cur))
cverts = [np.array(sorted({v.index for i in c for v in bm.faces[int(i)].verts})) for c in comps]
cmat = [int(np.bincount(FMAT[c]).argmax()) for c in comps]
gname = {g.index: g.name for g in pair.vertex_groups}
vside = np.zeros(len(me.vertices))
for v in me.vertices:
    for g in v.groups:
        vside[v.index] += g.weight * (1 if gname[g.group].endswith("_l") else -1 if gname[g.group].endswith("_r") else 0)
cside = [0 if vside[cv].sum() > 0 else 1 for cv in cverts]


def frame(side, co):
    up = [i for i in range(len(comps)) if cmat[i] == SLOT["M_Upper"] and cside[i] == side][0]
    so = [i for i in range(len(comps)) if cmat[i] == SLOT["M_Sole"] and cside[i] == side][0]
    uv_ = cverts[up]
    nh = len(uv_) // 2
    outer, inner = uv_[:nh], uv_[nh:]
    # the shell's two halves by vertex order (the solidified upper; a carried pair keeps them within a millimetre or so)
    assert np.abs(np.linalg.norm(co[outer] - co[inner], axis=1) - 0.0025).max() < 0.004
    sp = co[cverts[so]]
    c2 = sp[:, :2].mean(axis=0)
    _u, _s, vt = np.linalg.svd(sp[:, :2] - c2)
    D = np.array([vt[0, 0], vt[0, 1], 0.0])
    if D[1] > 0:
        D = -D
    E = np.cross(Z, D) * (1 if side == 0 else -1)
    s0 = float((co[outer] @ D).min())
    return dict(up=up, so=so, outer=outer, inner=inner, D=D, E=E, s0=s0)


def sole_rings(b, co):
    """The sole's top and bottom edge rings (vertex indices in order) and its top cap's faces."""
    sf = comps[b["so"]]
    zmid = 0.5 * (co[cverts[b["so"]], 2].max() + co[cverts[b["so"]], 2].min())
    rings = {}
    for top in (True, False):
        adj = {}
        for fi in sf:
            f = bm.faces[int(fi)]
            if abs(f.normal.z) > 0.6:
                continue
            for e in f.edges:
                a_, c_ = e.verts[0].index, e.verts[1].index
                if (co[a_, 2] > zmid) == top and (co[c_, 2] > zmid) == top:
                    adj.setdefault(a_, set()).add(c_)
                    adj.setdefault(c_, set()).add(a_)
        st = next(iter(adj))
        ring, prev = [st], None
        while True:
            nx = [w for w in adj[ring[-1]] if w != prev and w not in ring]
            if not nx:
                break
            prev = ring[-1]
            ring.append(nx[0])
        rings[top] = np.array(ring)
    cap = [int(fi) for fi in sf if bm.faces[int(fi)].normal.z > 0.6]
    return rings[True], rings[False], cap


BOOT = {s_: frame(s_, CO0) for s_ in (0, 1)}
for side, b in BOOT.items():
    b["rtop"], b["rbot"], b["cap"] = sole_rings(b, CO0)
    rt, rb = CO0[b["rtop"]], CO0[b["rbot"]]
    # each top-ring point's column partner on the bottom ring (nearest in plan)
    b["col"] = b["rbot"][np.argmin(((rt[:, None, :2] - rb[None, :, :2]) ** 2).sum(2), axis=1)]
    # this foot's points (the body's skin on this side, below the boot's top), for the toes
    sg = 1 if side == 0 else -1
    foot = BCO[(BCO[:, 0] * sg > 0.02) & (BCO[:, 2] < 0.16)]
    b["foot"] = foot
    b["comp_v"] = np.concatenate([cverts[i] for i in range(len(comps)) if cside[i] == side])
    b["eyelace_v"] = np.concatenate([cverts[i] for i in range(len(comps)) if cside[i] == side and cmat[i] in
                                     (SLOT["M_Eyelet"], SLOT["M_Lace"])])
    if arm is not None:
        sn = "l" if side == 0 else "r"
        bn = arm.data.bones.get("ball_" + sn)
        b["s_ball"] = float(np.array(arm.matrix_world @ bn.head_local) @ b["D"] - b["s0"])
        fa = np.array(arm.matrix_world @ bn.head_local) - np.array(arm.matrix_world @ arm.data.bones["foot_" + sn].head_local)
        fa[2] = 0.0
        b["ax"] = fa / np.linalg.norm(fa)
    floor_ = float(BCO[:, 2].min())
    b["foot6"] = BCO[(BCO[:, 0] * sg > 0.02) & (BCO[:, 2] < floor_ + 0.06)]


def s_of(p, b):
    return p @ b["D"] - b["s0"]


def e_of(p, b):
    return p @ b["E"]


def cap_bvh(b, co):
    bm_ = bmesh.new()
    vm = {}
    for fi in b["cap"]:
        vs = []
        for v in me.polygons[fi].vertices:
            if v not in vm:
                vm[v] = bm_.verts.new(co[v])
            vs.append(vm[v])
        bm_.faces.new(vs)
    bm_.normal_update()
    return BVHTree.FromBMesh(bm_)


def cap_z(bvh, pts):
    """The welt's top under each point (None where the point lies outside the welt's outline)."""
    out = np.full(len(pts), np.nan)
    for i, p in enumerate(pts):
        hit = bvh.ray_cast(Vector((p[0], p[1], 0.2)), Vector((0, 0, -1)), 1.0)
        if hit[0] is not None:
            out[i] = hit[0].z
    return out


def ring_dist_plan(pts, ring):
    """Plan distance from each point to the closed ring polyline."""
    R = np.vstack([ring, ring[:1]])[:, :2]
    A, B_ = R[:-1], R[1:]
    AB = B_ - A
    L2 = np.maximum((AB * AB).sum(1), 1e-18)
    out = np.empty(len(pts))
    for a in range(0, len(pts), 4096):
        x = pts[a:a + 4096, :2]
        t = np.clip(((x[:, None, :] - A[None]) * AB[None]).sum(2) / L2[None], 0, 1)
        q = A[None] + t[..., None] * AB[None]
        out[a:a + 4096] = np.sqrt(((x[:, None, :] - q) ** 2).sum(2)).min(1)
    return out


def measure(co, tag):
    """The toe's and the welt's numbers, each boot (millimetres)."""
    res = {}
    for side, b in BOOT.items():
        po = co[b["outer"]]
        s = s_of(po, b)
        L = float(s.max())
        toes = float(s_of(b["foot"], b).max())
        floor_tip = float(co[b["rbot"], 2].min())
        rb = co[b["rbot"]]
        tip_bot = float(rb[np.argmax(s_of(rb, b)), 2]) if len(rb) else 0.0
        # the upper's own floor (the insole) and its top along the last 60 mm
        prof = {}
        for mm in (0, 5, 10, 20, int(round(0.10 * L * 1000)), 40, 60):
            x = L - mm / 1000.0
            sel = np.abs(s - x) < 0.004
            if sel.any():
                prof[mm] = [round(float((po[sel, 2].max() - zfl(x if tag == "before" else x, b)) * 1000), 1),
                            round(float(np.ptp(e_of(po[sel], b)) * 1000), 1)]
        ball = np.abs(s - b["s_ball"]) < 0.006
        ballw = float(np.ptp(e_of(po[ball], b)) * 1000)
        # the welt: how far its edge stands beyond the upper's foot (points 0-5 mm above its top)
        bvh = cap_bvh(b, co)
        cz = cap_z(bvh, po)
        inside = ~np.isnan(cz)
        dz = po[:, 2] - np.where(inside, cz, 0)
        base = inside & (dz > -0.004) & (dz < 0.005)
        rt_ = co[b["rtop"]]
        dist = np.sqrt(((rt_[:, None, :2] - po[base][None, :, :2]) ** 2).sum(2)).min(1) if base.any() else np.zeros(0)
        below = inside & (dz < -0.0002)
        # visible faces of the upper turned away from the outside near the toe (a fold): the face's normal against its
        # points' outward direction from the toe's middle
        whole = co[b["comp_v"]]
        res["left" if side == 0 else "right"] = {
            "toesBeyondMm (the upper's tip, along the sole)": round((L - toes) * 1000, 1),
            "toeBeyondFootMm (carry_footwear's: the whole boot, welt included, along the foot)": round(
                float((whole @ b["ax"]).max() - (b["foot6"] @ b["ax"]).max()) * 1000, 1),
            "soleBottomAtTipAboveGroundMm (spring)": round((tip_bot - floor_tip) * 1000, 1),
            "topAboveBareFloorMm_widthMm_atMmFromTip": prof,
            "ballWidthMm": round(ballw, 1),
            "soleEdgeMm_heel_forepart": [round(float(np.median((co[b["rtop"], 2] - co[b["col"], 2])[s_of(co[b["rtop"]], b) < 0.05]) * 1000), 1),
                                         round(float(np.median((co[b["rtop"], 2] - co[b["col"], 2])[
                                             (s_of(co[b["rtop"]], b) > b["s_ball"] - 0.02) & (s_of(co[b["rtop"]], b) < b["s_ball"] + 0.03)]) * 1000), 1)],
            "weltBeyondUpperMm_5_50_95 (each welt edge point to the upper's foot)": np.percentile(dist * 1000, [5, 50, 95]).round(2).tolist() if len(dist) else None,
            "upperPointsBelowWeltTop": int(below.sum()),
            "deepestBelowMm": round(float(-dz[below].min() * 1000), 2) if below.any() else 0.0,
            "belowWeltTopAtToe(last 40 mm)": int((below & (s > L - 0.04)).sum()),
        }
    LOG[tag] = res
    say(tag, json.dumps(res))
    return res


def folds(co):
    """Outer-shell faces above the welt whose winding faces against their own points' smooth normals (a fold: the game
    culls it from outside and shows the lining through it); [folded, all]."""
    cn = np.zeros(len(me.loops) * 3)
    me.corner_normals.foreach_get("vector", cn)
    cn = cn.reshape(-1, 3)
    out = {}
    for side, b in BOOT.items():
        oset = set(b["outer"].tolist())
        n_bad, n_all = 0, 0
        for p in me.polygons:
            if not all(v in oset for v in p.vertices):
                continue
            pts = co[list(p.vertices)]
            c = pts.mean(axis=0)
            nn = np.zeros(3)
            for k in range(len(pts)):
                nn += np.cross(pts[k], pts[(k + 1) % len(pts)])
            if np.linalg.norm(nn) < 1e-14:
                continue
            nn /= np.linalg.norm(nn)
            sm = cn[p.loop_start:p.loop_start + p.loop_total].sum(axis=0)
            n_all += 1
            if nn @ sm < 0 and (c[2] - zfl(s_of(c, b), b)) > 0.002:
                n_bad += 1
        out["left" if side == 0 else "right"] = [n_bad, n_all]
    return out


for side, b in BOOT.items():
    po = CO0[b["outer"]]
    s = s_of(po, b)
    b["L"] = float(s.max())
    bins = np.arange(-0.005, b["L"] + 0.01, 0.005)
    zf, ec, sb = [], [], []
    for x0 in bins:
        sel = np.abs(s - x0) < 0.006
        if sel.sum() >= 4:
            zf.append(po[sel, 2].min())
            ec.append(0.5 * (e_of(po[sel], b).max() + e_of(po[sel], b).min()))
            sb.append(x0)
    b["sb"], b["zf"], b["ec"] = np.array(sb), np.array(zf), np.array(ec)
    b["toes"] = float(s_of(b["foot"], b).max())
    # the heel's front: the bottom's waist lifting off the ground going forward
    rb = CO0[b["rbot"]]
    sr = s_of(rb, b)
    lift = [sr[i] for i in np.argsort(sr) if sr[i] < 0.5 * b["L"] and rb[i, 2] > rb[:, 2].min() + 0.0008]
    b["s_hf"] = float(min(lift)) - 0.004 if lift else 0.25 * b["L"]


def zfl(s, b):
    return np.interp(s, b["sb"], b["zf"])


def e_mid(s, b, co=None):
    return np.interp(s, b["sb"], b["ec"])


# ---- normals: the original's against a recompute (upper smooth, the rest smooth to 50 degrees) ----------------------
N_ORIG = np.zeros(len(me.loops) * 3)
me.corner_normals.foreach_get("vector", N_ORIG)
N_ORIG = N_ORIG.reshape(-1, 3)


# the original's own hard edges: where its two faces' normals part at either shared point (by more than 1 degree)
SHARP = set()
_bmn = bmesh.new()
_bmn.from_mesh(me)
_bmn.faces.ensure_lookup_table()
for e in _bmn.edges:
    lf = e.link_faces
    if len(lf) != 2:
        continue
    for v in e.verts:
        la = next(l_ for l_ in lf[0].loops if l_.vert == v)
        lb = next(l_ for l_ in lf[1].loops if l_.vert == v)
        if N_ORIG[la.index] @ N_ORIG[lb.index] < math.cos(math.radians(1.0)):
            SHARP.add(tuple(sorted((e.verts[0].index, e.verts[1].index))))
            break
_bmn.free()


def recompute_normals(mesh_obj, extra_sharp=()):
    """Smooth normals from the points, hard only along the original's own hard edges (as it was shaded) and any
    extra_sharp edges given."""
    m = mesh_obj.data
    bm_ = bmesh.new()
    bm_.from_mesh(m)
    xs = set(extra_sharp)
    for e in bm_.edges:
        key = tuple(sorted((e.verts[0].index, e.verts[1].index)))
        e.smooth = key not in SHARP and key not in xs
    for f in bm_.faces:
        f.smooth = True
    bm_.to_mesh(m)
    bm_.free()
    if m.has_custom_normals:
        bpy.context.view_layer.objects.active = mesh_obj
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
    m.update()


bpy.context.view_layer.objects.active = pair
probe = pair.copy()
probe.data = me.copy()
bpy.context.scene.collection.objects.link(probe)
recompute_normals(probe)
N_RE = np.zeros(len(probe.data.loops) * 3)
probe.data.corner_normals.foreach_get("vector", N_RE)
N_RE = N_RE.reshape(-1, 3)
ang = np.degrees(np.arccos(np.clip((N_ORIG * N_RE).sum(1), -1, 1)))
LOG["normalRecomputeOnOriginalDeg50_99_max"] = np.percentile(ang, [50, 99, 100]).round(3).tolist()
LMAT = np.zeros(len(me.loops), dtype=np.int64)
for p_ in me.polygons:
    LMAT[p_.loop_start:p_.loop_start + p_.loop_total] = p_.material_index
LOG["normalRecomputeBySlotDeg50_99_max"] = {k: np.percentile(ang[LMAT == i], [50, 99, 100]).round(3).tolist() for k, i in SLOT.items()}
say("by slot", LOG["normalRecomputeBySlotDeg50_99_max"])
say("normals recomputed on the original against its own: deg 50/99/max", LOG["normalRecomputeOnOriginalDeg50_99_max"])
bpy.data.objects.remove(probe, do_unlink=True)

measure(CO0, "before")
LOG["foldsBefore"] = folds(CO0)
say("folds before", LOG["foldsBefore"])

# ---- the moves, each boot -------------------------------------------------------------------------------------------
CO = CO0.copy()
DISP = np.zeros_like(CO0)
for side, b in BOOT.items():
    D, E = b["D"], b["E"]
    allow0 = float((CO0[b["comp_v"]] @ b["ax"]).max() - (b["foot6"] @ b["ax"]).max())
    A = float(np.clip(allow0 - ALLOW, SH_MIN, SH_MAX))
    b["shorten"] = A
    vs = b["comp_v"]
    p = CO0[vs]
    s = s_of(p, b)
    e = e_of(p, b)
    sc0 = b["toes"] - 0.004
    span = b["L"] - sc0
    u = np.clip((s - sc0) / span, 0, 1)
    # 1. shortened ahead of the toes (quadratic: the nose pressed most) and widened about the toe's middle
    ds = -A * u * u
    ecm = e_mid(s, b)
    de = (e - ecm) * SQUARE * smooth(0.25, 1.0, u)
    # 2. the nose raised on its upper part; the toe sprung from the toes forward
    h = p[:, 2] - zfl(s, b)
    dz = NOSE * smooth(0.35, 1.0, u) * smooth(0.004, 0.016, h)
    sp_u = np.clip((s - (b["toes"] - 0.005)) / (b["L"] - b["toes"] + 0.005), 0, 1)
    dz = dz + SPRING * sp_u * sp_u
    # 3. the forepart's welt top lowered, the upper's foot and insole with it (not the sole's bottom)
    is_bot_ring = np.isin(vs, b["rbot"])
    is_sole = np.isin(vs, cverts[b["so"]])
    fd = FDROP * smooth(b["s_hf"], b["s_hf"] + 0.015, s)
    drop = np.where(is_sole, np.where(is_bot_ring, 0.0, fd), fd * (1 - smooth(0.0, 0.010, h)))
    drop[np.isin(vs, b["eyelace_v"])] = 0.0
    dz = dz - drop
    d3 = D[None, :] * ds[:, None] + E[None, :] * de[:, None] + Z[None, :] * dz[:, None]
    DISP[vs] = d3
    b["moves"] = dict(shortenMm=round(A * 1000, 2), toesBeyondBeforeMm=round(allow0 * 1000, 1))
CO = CO0 + DISP
# the lining moves with its leather (each inner point by its outer partner's move)
for side, b in BOOT.items():
    CO[b["inner"]] = CO0[b["inner"]] + DISP[b["outer"]]

# 4. the welt drawn in where it stands wide, top and bottom together; the upper pinched just above it
for side, b in BOOT.items():
    po = CO[b["outer"]]
    rt = CO[b["rtop"]]
    bvh = cap_bvh(b, CO)
    cz = cap_z(bvh, po)
    ok = ~np.isnan(cz) & (po[:, 2] - np.nan_to_num(cz) < 0.006) & (po[:, 2] - np.nan_to_num(cz) > -0.004)
    base = po[ok]
    # (the first try moved each edge point towards its nearest upper point by its own amount: the welt's edge came out
    # wavy at the toe; now the amounts smoothed round the ring and each point moved along the ring's own inward normal)
    w = np.sqrt(((rt[:, None, :2] - base[None, :, :2]) ** 2).sum(2)).min(1) if len(base) else np.zeros(len(rt))
    m = np.clip(w - WELT, 0.0, 0.002)
    for _ in range(3):
        m = (np.roll(m, -3) + np.roll(m, -2) + np.roll(m, -1) + m + np.roll(m, 1) + np.roll(m, 2) + np.roll(m, 3)) / 7.0
    tang = np.roll(rt[:, :2], -1, axis=0) - np.roll(rt[:, :2], 1, axis=0)
    nrm2 = np.column_stack([tang[:, 1], -tang[:, 0]])
    nrm2 /= np.maximum(np.linalg.norm(nrm2, axis=1), 1e-12)[:, None]
    cen = rt[:, :2].mean(axis=0)
    if np.mean(((rt[:, :2] - cen) * nrm2).sum(1)) > 0:
        nrm2 = -nrm2                                  # inward
    CO[b["rtop"], :2] += nrm2 * m[:, None]
    CO[b["col"], :2] += nrm2 * m[:, None]
    b["moves"]["weltPointsDrawnIn"] = int((m > 1e-5).sum())
    b["moves"]["weltDrawnInMaxMm"] = round(float(m.max() * 1000), 2)
    # the pinch: the leather 0-6 mm above the welt drawn in (towards the foot's middle line), its lining with it
    po = CO[b["outer"]]
    cz = cap_z(cap_bvh(b, CO), po)
    hh = po[:, 2] - np.nan_to_num(cz, nan=-1.0)
    w_ = np.where(np.isnan(cz), 0.0, np.exp(-((hh - 0.0025) / 0.0018) ** 2) * (hh > -0.0005))
    s = s_of(po, b)
    axis = D[None, :] * (s + b["s0"])[:, None] + E[None, :] * e_mid(s, b)[:, None]
    inward = axis - po
    inward[:, 2] = 0.0
    inward /= np.maximum(np.linalg.norm(inward, axis=1), 0.01)[:, None]
    # round the toe the inward direction runs back along the foot
    tw = smooth(b["L"] - 0.035 - b["shorten"], b["L"] - b["shorten"], s)
    inward = inward * (1 - tw)[:, None] - D[None, :] * tw[:, None]
    inward /= np.maximum(np.linalg.norm(inward, axis=1), 1e-6)[:, None]
    mv = inward * (PINCH * w_)[:, None]
    CO[b["outer"]] += mv
    CO[b["inner"]] += mv

# 5. the upper meets the welt all round: any point of it inside the welt's outline and below the welt's top lifted
#    onto it, its lining by the same
for side, b in BOOT.items():
    po = CO[b["outer"]]
    cz = cap_z(cap_bvh(b, CO), po)
    gap = po[:, 2] - np.nan_to_num(cz)
    # below the welt's top: lifted onto it; just above it (a slit at the foot of the leather): set down on it, fully up
    # to 0.8 mm, then less and less to none at 3 mm, so the leather's lowest rows close down onto the welt evenly
    # (the first try set down only to 0.8 mm and left a slit at the toe's front, where the welt's top had moved)
    wdown = 1.0 - smooth(0.0008, 0.003, gap)
    lift = np.where(np.isnan(cz), 0.0, np.where(gap < 0, -gap, -gap * wdown))
    CO[b["outer"], 2] += lift
    CO[b["inner"], 2] += lift
    b["moves"]["pointsLiftedOntoWelt"] = int((lift > 1e-6).sum())
    b["moves"]["pointsSetDownOntoWelt"] = int((lift < -1e-6).sum())
    b["moves"]["mostLiftedMm"] = round(float(lift.max() * 1000), 2)
LOG["moves"] = {("left" if s_ == 0 else "right"): b["moves"] for s_, b in BOOT.items()}
say("moves", LOG["moves"])

for v, c in zip(me.vertices, CO):
    v.co = Vector(c)
me.update()
# THE UPPER'S FOOT HARD-EDGED FROM ITS WALLS (the notch, read from the normals: the toe's lowest row and its tip took the
# down-facing bottom into their smooth normals, 30 to 60 degrees down, and the game drew a dark triangle there; and a
# hard turn where the upper meets the welt is the crisp edge asked for): the outer shell's faces lying on the welt and
# facing down split from the walls
BOT_EDGES = []
LOG["normalSplit"] = {}
for side, b in BOOT.items():
    oset = set(b["outer"].tolist())
    bvh = cap_bvh(b, CO)
    botf = set()
    for p_ in me.polygons:
        if not all(v in oset for v in p_.vertices):
            continue
        c = np.array(p_.center)
        cz = cap_z(bvh, c[None])[0]
        if p_.normal.z < -0.6 and not np.isnan(cz) and c[2] - cz < 0.0025:
            botf.add(p_.index)
    bm_ = bmesh.new()
    bm_.from_mesh(me)
    bm_.faces.ensure_lookup_table()
    n_e = 0
    for e in bm_.edges:
        lf = e.link_faces
        if len(lf) == 2 and ((lf[0].index in botf) != (lf[1].index in botf)) and all(v.index in oset for v in e.verts):
            BOT_EDGES.append(tuple(sorted((e.verts[0].index, e.verts[1].index))))
            n_e += 1
    bm_.free()
    LOG["normalSplit"]["left" if side == 0 else "right"] = {"bottomFaces": len(botf), "hardEdges": n_e}
recompute_normals(pair, BOT_EDGES)
cn_ = np.zeros(len(me.loops) * 3)
me.corner_normals.foreach_get("vector", cn_)
cn_ = cn_.reshape(-1, 3)
LV_ = np.zeros(len(me.loops), dtype=np.int64)
me.loops.foreach_get("vertex_index", LV_)
for side, b in BOOT.items():
    po = CO[b["outer"]]
    s = s_of(po, b)
    L = float(s.max())
    sel = b["outer"][(s > L - 0.02)]
    low = sel[CO[sel, 2] < CO[sel, 2].min() + 0.004]
    nz = []
    for v in low:
        lsel = np.where(LV_ == v)[0]
        # each loop of the point on a wall face (not the foot's) counts
        nz += [cn_[l_] for l_ in lsel if cn_[l_][2] > -0.6]
    nz = np.array(nz)
    LOG["normalSplit"]["left" if side == 0 else "right"]["toeFrontLowestRowWallNormalZ_mean_min"] = [
        round(float(nz[:, 2].mean()), 2), round(float(nz[:, 2].min()), 2)] if len(nz) else None
say("normal split", LOG["normalSplit"])
measure(CO, "after")
LOG["foldsAfter"] = folds(CO)
say("folds after", LOG["foldsAfter"])
mvlen = np.linalg.norm(CO - CO0, axis=1)
LOG["pointMovesMm_max_99"] = [round(float(mvlen.max() * 1000), 2), round(float(np.percentile(mvlen, 99) * 1000), 2)]
LOG["pointsMoved"] = int((mvlen > 1e-6).sum())
thick = {("left" if s_ == 0 else "right"): round(float(np.abs(np.linalg.norm(CO[b["outer"]] - CO[b["inner"]], axis=1)
                                                                - np.linalg.norm(CO0[b["outer"]] - CO0[b["inner"]], axis=1)).max() * 1000), 4)
         for s_, b in BOOT.items()}
LOG["leatherThicknessChangeMaxMm"] = thick

# ---- the export, as the pair was written, then read back against the original ---------------------------------------
path = os.path.join(OUT, NAME + "_skinned_v2.fbx")
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
    return dict(co=np.array([m_.matrix_world @ v.co for v in m_.data.vertices]), W=W, uv=uv, lv=lv,
                uvn=len(m_.data.uv_layers), faces=len(m_.data.polygons), mats=[x.name.split(".")[0] for x in m_.data.materials],
                bones={bn.name: np.array(a_.matrix_world @ bn.head_local) for bn in a_.data.bones})


o_, n_ = read(SRC), read(path)
keys = set(o_["W"]) | set(n_["W"])
LOG["export"] = {
    "written": path, "points": len(n_["co"]), "faces": [o_["faces"], n_["faces"]], "materials": n_["mats"],
    "uvLayers": n_["uvn"], "loopsSame": bool(np.array_equal(o_["lv"], n_["lv"])),
    "maxUvChange": float(np.abs(o_["uv"] - n_["uv"]).max()),
    "weightsCompared": len(keys),
    "maxWeightChange": float(max(abs(o_["W"].get(k, 0.0) - n_["W"].get(k, 0.0)) for k in keys)),
    "maxBoneMoveMm": round(float(max(np.abs(o_["bones"][k] - n_["bones"][k]).max() for k in o_["bones"]) * 1000), 6),
    "pointsWrittenAsMovedMaxErrMm": round(float(np.abs(n_["co"] - CO).max() * 1000), 6),
}
say("export", json.dumps(LOG["export"]))

# ---- the pose-check scene: the pair's own (skeleton, body, pair) with the new points; the body unmasked -------------
def write_check(points, tag):
    bpy.ops.wm.open_mainfile(filepath=CHECK_BLEND)
    ob = bpy.data.objects[CHECK_OBJ]
    ok = len(ob.data.vertices) == len(CO0) and np.abs(np.array([v.co[:] for v in ob.data.vertices]) - CO0).max() < 2e-5
    LOG.setdefault("checkBlend", {"from": CHECK_BLEND, "samePointsAsTheFbx": bool(ok)})
    if not ok:
        return
    for v, c in zip(ob.data.vertices, points):
        v.co = Vector(c)
    ob.data.update()
    rig = next(o for o in bpy.data.objects if o.type == "ARMATURE")
    if ob.parent is None:
        ob.parent = rig
        ob.matrix_parent_inverse = rig.matrix_world.inverted()
    if not any(m_.type == "ARMATURE" for m_ in ob.modifiers):
        ob.modifiers.new("Armature", "ARMATURE").object = rig
    for o in bpy.data.objects:
        if o.type == "MESH" and o is not ob:
            for m_ in list(o.modifiers):
                if m_.type == "MASK":
                    o.modifiers.remove(m_)
    cb = os.path.join(OUT, "%s_%s_posecheck.blend" % (NAME, tag))
    bpy.ops.wm.save_as_mainfile(filepath=cb)
    LOG["checkBlend"][tag] = cb


if CHECK_BLEND:
    write_check(CO0, "v1")
    write_check(CO, "v2")
json.dump(LOG, open(os.path.join(OUT, "reshape.json"), "w"), indent=1, default=str)
say("done")
