"""A finished, skinned pair of boots given a lower, rounder toe with its tip sprung off the floor: only the points
ahead of the ball move (with a smooth falloff behind it), and only their positions, so faces, UVs, material slots
and weights stay those of the pair it was given, and its baked maps and its skinning still hold.

    blender -b --factory-startup -P tools/meshgen/blender/boot_toe.py -- PAIR_SKINNED.fbx FULL_BODY.fbx OUT_DIR
        [--name tom_boots] [--out-version v3] [--spring 0.014] [--h10 0.044] [--h30 0.0535] [--h50 0.0555]
        [--w20 0.68] [--fall 0.020] [--clear 0.004] [--narrow-from 0.45] [--hold-radius 0.025] [--welt-follow 0]
        [--measure-only] [--stop-after-moves] [--no-preview]

    Tom's v3 (2 November): -- F:/LedgerTools/garments/tom/boots/maps/tom_boots_skinned_v2.fbx
        F:/LedgerTools/bodies/MH_TomL1/MH_TomL1_FullBody.fbx F:/LedgerTools/garments/tom/boots/maps
    (--measure-only and --stop-after-moves print and write nothing.)

WHY, 2 November 2026 (Tom's boots, carried from Ron's passed pair; his order C9): fresh reviewers read the boots as
"heavy, almost clog-like" at the toe, and two tries on the toe failed on 30 October (reshape_footwear.py: shorter,
the nose raised, squarer, a crisper welt). The owner said yes to a third, taking the toe's shape from Epic's MetaHuman
boots. Epic's boot cannot be brought into Blender (its export crashes), so its shape was read from pictures of it worn
on Tom in the game at the played level, beside ours from the same camera (F:/LedgerTools/gate/new/tom-outfit/
2026-11-02-epicboots and 2026-11-02-jeans2s): Epic's toe is lower and rounder and its tip turns up off the floor;
ours keeps a box 36 mm tall over its welt nearly to the tip and ends in an upright front wall, which is the clog.
The method is a last's: the top line falls steadily from the instep to a low nose, the forepart's bottom tilts up
ahead of the ball (production/research/clothing-pipeline/SHOE-TOE-AND-LACING-2026-09-30.md).

Each boot in its own frame from the skeleton's rest pose: along the foot (flat, from the foot joint's head to the
ball joint's), across it (flat, outward) and up; s is the distance ahead of the ball joint. The floor is the sole's
lowest point (where the boot stands); the tip is the boot's foremost point.

MEASURED, before and after: the toe box's top above the floor 1, 3 and 5 cm behind the tip (and over the welt's top
there); the toe spring (the sole's underside 1 mm behind the tip, above the floor) and its profile; the toe's width
2 cm behind the tip against the boot's widest (welt included, and the upper alone); the length beyond the foot's toes
(the full body's LOD0 skin, that side).

THE MOVES, each a function of s that is nil from --fall behind the ball and smooth (no kink) where it starts:
1. THE SPRING: the sole's underside lifted ahead of the ball by (--spring less the spring it has) times u^2.5, u
   running from the ball to the tip. Its top (the welt, and the upper standing on it) stays (--welt-follow 0), so the
   forepart's sole thins towards the tip (17 to about 13 mm, a welted forepart is thinner than its heel) and the insole
   under the toes, which the bare foot stands on, does not rise into them.
2. THE BOX LOWERED: the upper squeezed down towards the welt's top in each section, the leather's vertical scale
   running from 1 at the welt to a factor k above its lowest 8 mm (never squeezed harder than k, so its foot stays on
   the welt and its turn there stays crisp); k set so the top meets --h10, --h30 and --h50 above the floor, monotone
   cubic between, back to 1 from --fall behind the ball. Then HELD where the lining would come nearer than --clear to
   the foot's skin than it was: each such point's share of its move halved down to what keeps it clear, eased back to
   the whole move over --hold-radius round it (a smoothstep by distance), a few rounds; so the box comes down in the
   middle and on the outside and bends round the big toe on the inside. (Holding it section by section, by each
   lining point's room straight down, was tried and kept the box within 6% of its height at 3 and 5 cm; a hold eased
   over 18 mm left faces stretched 1.39 next to held points; scaling the box straight by h squeezed a band at the
   welt to 0.23 of its area.)
3. THE TOE NARROWED towards its inside edge (a last's inside edge runs nearly straight, its outside curves in; and the
   big toe stands on the inside) by n = N v^2, v from --narrow-from of the way from the ball to the tip (ahead of where
   the little toes end; drawn in from the ball it pressed the lining onto the little toe's side), N set from --w20
   (the width 2 cm behind the tip over the widest); most at the tip, which rounds the toe in plan. The welt with the
   upper above it, so it keeps its margin.
Nothing moves along the foot, so the toe's length is unchanged and the floor footprints still hold. Each move of an
outside point is given to its lining partner, so the leather keeps its thickness exactly; the upper's foot is kept at
its own height over the welt's top where it stood within 3 mm of it (the notch fixed on 30 October stays fixed);
eyelets and laces take the moves of the upper under them. Normals are recomputed as reshape_footwear.py did (smooth,
hard only along the pair's own hard edges, found from its normals).

CHECKED: the measures; the clearance to the foot (each moved point's distance to the skin, before and after, none
inside); the stretch (each face's 3D area over its UV area after, against before: flagged above 1.25 or below 0.8;
and the largest edge stretch); faces turned over (none); the sole still one closed piece of positive thickness;
counts, UVs and weights identical to the pair given, read back from the written file; the footprints
(sole_footprints.py's measure) before and after.

OUT_DIR gets NAME_skinned_V.fbx (written as v2 was: smoothing by face, no leaf bones, no animation),
boot-toe-record.json and boot-toe-preview.png (one boot, the left: side and three-quarter, the pair given against
the new, and the two outlines over each other; Cycles on the CPU, a plain grey material).
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
from mathutils.kdtree import KDTree

argv = sys.argv[sys.argv.index("--") + 1:]
PAIR, BODY, OUT = argv[:3]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
NAME = opt("--name", "tom_boots", str)
VER = opt("--out-version", "v3", str)
SPRING = opt("--spring", 0.014)
H10, H30, H50 = opt("--h10", 0.044), opt("--h30", 0.0535), opt("--h50", 0.0555)
W20 = opt("--w20", 0.68)
FALL = opt("--fall", 0.020)
CLEAR = opt("--clear", 0.004)
NARROW_FROM = opt("--narrow-from", 0.45)
R_HOLD = opt("--hold-radius", 0.025)
WELT_FOLLOW = opt("--welt-follow", 0.0)
TOL = 0.00001                    # a point under the clearance may come no nearer than this
MEASURE_ONLY = "--measure-only" in argv
PREVIEW = "--no-preview" not in argv
os.makedirs(OUT, exist_ok=True)
Z = np.array([0.0, 0.0, 1.0])
REC = {"pair": PAIR, "body": BODY, "date": "2026-11-02",
       "params": dict(springM=SPRING, h10M=H10, h30M=H30, h50M=H50, w20=W20, fallM=FALL, clearM=CLEAR)}


def say(*a):
    print("BOOTTOE", *a, flush=True)


def mm(x):
    return round(float(x) * 1000, 2)


def smoothstep(a, b, x):
    t = np.clip((np.asarray(x, dtype=float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ---- the full body's feet (LOD0, rest pose) ---------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY)
body = next(o for o in bpy.data.objects if o.type == "MESH" and o.name.endswith("LOD0"))
BCO = np.array([body.matrix_world @ v.co for v in body.data.vertices])
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
    pts = BCO[idx]
    FOOT[side] = dict(pts=pts, bvh=BVHTree.FromPolygons([Vector(p) for p in pts], [[int(remap[i]) for i in p] for p in polys]))
bpy.ops.wm.read_factory_settings(use_empty=True)

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
cside = [0 if CO0[cv, 0].mean() > 0 else 1 for cv in cverts]          # 0: the left boot (+x), 1: the right
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
    # the upper is solidified leather: its two halves by vertex order, each point's partner 2.5 mm off (as
    # reshape_footwear.py found); which half is the lining is read from the foot (it lies nearer)
    gap = np.linalg.norm(CO0[outer] - CO0[inner], axis=1)
    assert np.abs(gap - 0.0025).max() < 0.004, "the upper's halves are not partners"
    F_, B_ = BONES["foot_" + sn], BONES["ball_" + sn]
    f = (B_ - F_) * np.array([1.0, 1.0, 0.0])
    f /= np.linalg.norm(f)
    a = np.array([-f[1], f[0], 0.0])
    if a @ (B_ * np.array([1.0, 1.0, 0.0])) < 0:
        a = -a
    every = np.concatenate([cverts[i] for i in range(len(comps)) if cside[i] == side])
    eyelace = np.concatenate([cverts[i] for i in range(len(comps)) if cside[i] == side and
                              cmat[i] in (SLOT["M_Eyelet"], SLOT["M_Lace"])])
    BOOT[side] = dict(sn=sn, outer=outer, inner=inner, sole=cverts[so[0]], every=every, eyelace=eyelace,
                      ball=B_, f=f, a=a, upper_faces=comps[up[0]], sole_faces=comps[so[0]],
                      E_up=edges_of(comps[up[0]]), E_so=edges_of(comps[so[0]]),
                      faces=np.concatenate([comps[i] for i in range(len(comps)) if cside[i] == side]))
    b = BOOT[side]
    b["E_out"] = b["E_up"][np.isin(b["E_up"][:, 0], outer) & np.isin(b["E_up"][:, 1], outer)]
    b["foot_tip_s"] = float(((FOOT[side]["pts"] - B_) @ f).max())

# which half lies nearer the foot (the lining) -- swap if the order says otherwise
for side, b in BOOT.items():
    def near(ix):
        d = []
        for p in CO0[ix]:
            q = FOOT[side]["bvh"].find_nearest(Vector(p))
            d.append(q[3] if q[0] is not None else 1.0)
        return float(np.median(d))
    if near(b["outer"]) < near(b["inner"]):
        b["outer"], b["inner"] = b["inner"], b["outer"]
        b["E_out"] = b["E_up"][np.isin(b["E_up"][:, 0], b["outer"]) & np.isin(b["E_up"][:, 1], b["outer"])]
        say("side", b["sn"], "halves swapped: the second half is the outside")


def s_of(p, b):
    return (np.asarray(p) - b["ball"]) @ b["f"]


def e_of(p, b):
    return (np.asarray(p) - b["ball"]) @ b["a"]


def section(co, E, b, s0):
    """Where the plane s = s0 cuts the given edges: the points, (n, 3)."""
    sa, sb = s_of(co[E[:, 0]], b), s_of(co[E[:, 1]], b)
    m = (sa - s0) * (sb - s0) < 0
    if not m.any():
        return np.zeros((0, 3))
    t = (s0 - sa[m]) / (sb[m] - sa[m])
    return co[E[m, 0]] + t[:, None] * (co[E[m, 1]] - co[E[m, 0]])


def welt_top(co, b, s0):
    p = section(co, b["E_so"], b, s0)
    if len(p) < 2:
        return np.nan
    zm = 0.5 * (p[:, 2].max() + p[:, 2].min())
    return float(p[p[:, 2] > zm, 2].mean())


def measure(co, tag):
    res = {}
    for side, b in BOOT.items():
        ev = b["every"]
        floor_ = float(co[b["sole"], 2].min())
        stip = float(s_of(co[ev], b).max())
        utip = float(s_of(co[b["outer"]], b).max())
        r = {"floorZmm": mm(floor_), "tipSmm (ahead of the ball joint)": mm(stip),
             "beyondFootToesMm (the boot's foremost point, welt included)": mm(stip - b["foot_tip_s"]),
             "upperBeyondFootToesMm": mm(utip - b["foot_tip_s"])}
        prof = {}
        for d in (10, 20, 30, 40, 50):
            s0 = stip - d / 1000.0
            pu = section(co, b["E_out"], b, s0)
            wt = welt_top(co, b, s0)
            ps = section(co, b["E_so"], b, s0)
            prof[d] = {"topAboveFloorMm": mm(pu[:, 2].max() - floor_) if len(pu) else None,
                       "topOverWeltMm": mm(pu[:, 2].max() - wt) if len(pu) and not np.isnan(wt) else None,
                       "weltTopAboveFloorMm": mm(wt - floor_) if not np.isnan(wt) else None,
                       "underSideAboveFloorMm": mm(ps[:, 2].min() - floor_) if len(ps) else None}
        r["byMmBehindTip"] = prof
        sp = section(co, b["E_so"], b, stip - 0.001)
        r["toeSpringMm (the sole's underside 1 mm behind the tip, above the floor)"] = mm(sp[:, 2].min() - floor_)
        r["undersideProfileMm (mm behind tip: height)"] = {
            d: mm(section(co, b["E_so"], b, stip - d / 1000.0)[:, 2].min() - floor_)
            for d in (1, 5, 10, 20, 30, 40, 50, 60, 80, 100) if len(section(co, b["E_so"], b, stip - d / 1000.0))}
        widths = []
        for s0 in np.arange(-0.12, stip, 0.001):
            p = np.vstack([section(co, b["E_so"], b, s0), section(co, b["E_out"], b, s0)])
            if len(p) >= 2:
                widths.append((float(np.ptp(e_of(p, b))), float(s0)))
        wmax, smax = max(widths)
        p20 = np.vstack([section(co, b["E_so"], b, stip - 0.02), section(co, b["E_out"], b, stip - 0.02)])
        u20 = section(co, b["E_out"], b, stip - 0.02)
        uw = [float(np.ptp(e_of(section(co, b["E_out"], b, s0), b))) for s0 in np.arange(-0.12, utip - 0.002, 0.001)
              if len(section(co, b["E_out"], b, s0)) >= 2]
        r["widthAt20Mm"] = mm(np.ptp(e_of(p20, b)))
        r["widestMm (welt included) and its s"] = [mm(wmax), mm(smax)]
        r["width20OverWidest"] = round(float(np.ptp(e_of(p20, b)) / wmax), 3)
        r["upperWidthAt20Mm"] = mm(np.ptp(e_of(u20, b)))
        r["upperWidth20OverUpperWidest"] = round(float(np.ptp(e_of(u20, b)) / max(uw)), 3)
        res["left" if side == 0 else "right"] = r
    REC.setdefault("measures", {})[tag] = res
    say(tag, json.dumps(res))
    return res


def clearance(co, ix, side):
    """Each point's distance to the foot's skin (negative inside it)."""
    out = np.empty(len(ix))
    for k, p in enumerate(co[ix]):
        q = FOOT[side]["bvh"].find_nearest(Vector(p))
        if q[0] is None:
            out[k] = 1.0
            continue
        d = q[3]
        out[k] = -d if (Vector(p) - q[0]).dot(q[1]) < 0 else d
    return out


M0 = measure(CO0, "before")
if MEASURE_ONLY:
    for side, b in BOOT.items():
        stip = float(s_of(CO0[b["every"]], b).max())
        tz = []
        for d in range(0, 125, 5):
            s0 = stip - d / 1000.0
            pu = section(CO0, b["E_out"], b, s0)
            ps = section(CO0, b["E_so"], b, s0)
            fp = FOOT[side]["pts"]
            fs = fp[np.abs(s_of(fp, b) - s0) < 0.0015]
            tz.append("d%3d s%6.1f top %6.1f  weltTop %6.1f  under %6.1f  w %5.1f | footTop %s footBot %s" % (
                d, s0 * 1000, pu[:, 2].max() * 1000 if len(pu) else np.nan, welt_top(CO0, b, s0) * 1000,
                ps[:, 2].min() * 1000 if len(ps) else np.nan,
                np.ptp(e_of(np.vstack([pu, ps]), b)) * 1000 if len(pu) + len(ps) > 1 else np.nan,
                "%5.1f" % (fs[:, 2].max() * 1000) if len(fs) else "  -  ", "%5.1f" % (fs[:, 2].min() * 1000) if len(fs) else "  -  "))
        say("profile", b["sn"], "\n" + "\n".join(tz))
        ix = np.concatenate([b["outer"], b["inner"], b["sole"]])
        sel = ix[s_of(CO0[ix], b) > -FALL]
        c = clearance(CO0, sel, side)
        for nm, part in (("inner", b["inner"]), ("outer", b["outer"]), ("sole", b["sole"])):
            m = np.isin(sel, part)
            say("clearance", b["sn"], nm, "min %.2f mm, under 4 mm: %d of %d, inside: %d" % (
                c[m].min() * 1000, (c[m] < 0.004).sum(), m.sum(), (c[m] < 0).sum()))
    sys.exit(0)

# ---- Epic's boot, read from the pictures (estimates, not measurements) ---------------------------------------------
# How: the same camera, the same foot in the same pose, Epic's boot (2026-11-02-epicboots) against ours
# (2026-11-02-jeans2s), tom-boots-dress.png at full size, the left boot (seen nearly side-on, right of frame). At 22, 67
# and 111 px behind each boot's foremost pixel (about 10, 30 and 50 mm along the boot: ours runs about 2.4 px a mm
# along its axis, from its lowest eyelet 137 mm behind its tip), the silhouette's height from the sole's lower edge to
# its top edge: Epic 94, 139, 184 px against ours 152, 204, 228 px, so 0.62, 0.68 and 0.81 of ours; times our measured
# height above the floor. The spring: the sole's lower edge rising from its lowest pixel to the front corner, against
# the silhouette's height 1 cm behind the tip: Epic 36/94 = 0.38, ours 32/152 = 0.21; Epic's height times its ratio,
# scaled by ours (measured 10.4 mm against 12 by the same reading). The width: not readable, no frame sees the boots from
# above (the front-on boot's outline mixes width with the toe's side wall); it looks about as wide as ours.
# Uncertain by a fifth or more: a camera looking down at about 30 degrees mixes height with width, both edges are soft.
EPIC = {"method": "estimates from pictures, see the comment above EPIC in boot_toe.py",
        "topAboveFloorMm": {"10": 36, "30": 42, "50": 51}, "ratioToOurs": {"10": 0.62, "30": 0.68, "50": 0.81},
        "toeSpringMm": "12 to 14", "width20OverWidest": "not readable from these frames (no view from above)",
        "uncertainty": "about a fifth either way"}
# A 1990 men's derby (no period or maker's source with toe numbers was read in full for this; the numbers are the
# 30 September research's, SHOE-TOE-AND-LACING-2026-09-30.md: a man's last 26.5 mm tall at 10% of its length from the
# toe (D, search summary), a nose 10 to 15 mm at the tip (I), 2 to 3 mm of leather (I), toe spring 10 to 12 mm on a
# derby (I), 19 mm on Springline's round-toe formal last (D, read 30 September); 0.7 of the ball's width at 10% of the
# length (I)), set on this boot's own welt and sole:
DERBY = {"topAboveFloorMm": {"10": 45, "30": 50, "50": 56.7}, "toeSpringMm": "10 to 15",
         "width20OverWidest": "about 0.65 to 0.7", "how": "the last's height over the insole plus 2.5 mm of leather "
         "over this boot's welt top, which stands 18 to 24 mm above its floor"}
REC["epicEstimate"] = EPIC
REC["derbyReference"] = DERBY


def pchip(xk, yk, x):
    """Monotone cubic interpolation (Fritsch and Carlson), flat outside the knots."""
    xk, yk = np.asarray(xk, float), np.asarray(yk, float)
    h = np.diff(xk)
    dlt = np.diff(yk) / h
    d = np.zeros_like(yk)
    for i in range(1, len(xk) - 1):
        if dlt[i - 1] * dlt[i] > 0:
            w1, w2 = 2 * h[i] + h[i - 1], h[i] + 2 * h[i - 1]
            d[i] = (w1 + w2) / (w1 / dlt[i - 1] + w2 / dlt[i])
    x = np.clip(np.asarray(x, float), xk[0], xk[-1])
    i = np.clip(np.searchsorted(xk, x) - 1, 0, len(xk) - 2)
    t = (x - xk[i]) / h[i]
    h00, h10, h01, h11 = 2 * t ** 3 - 3 * t ** 2 + 1, t ** 3 - 2 * t ** 2 + t, -2 * t ** 3 + 3 * t ** 2, t ** 3 - t ** 2
    return h00 * yk[i] + h10 * h[i] * d[i] + h01 * yk[i + 1] + h11 * h[i] * d[i + 1]


def gauss1d(y, sig):
    k = np.arange(-3 * sig, 3 * sig + 1)
    w = np.exp(-0.5 * (k / sig) ** 2)
    w /= w.sum()
    yp = np.concatenate([np.full(3 * sig, y[0]), y, np.full(3 * sig, y[-1])])
    return np.convolve(yp, w, mode="valid")


def faces_top_bottom(b):
    """The sole's top ring (the welt) and bottom ring (the tread), each point paired with its column partner: the
    other sole point nearest it in plan (the sole is an outline extruded down, two rings and their caps)."""
    so = b["sole"]
    p = CO0[so]
    d2 = ((p[:, None, :2] - p[None, :, :2]) ** 2).sum(2)
    np.fill_diagonal(d2, np.inf)
    nn = d2.argmin(1)
    assert (nn[nn] == np.arange(len(so))).all(), "the sole's points do not pair in columns"
    is_top = p[:, 2] > p[nn, 2]
    top, bot = so[is_top], so[~is_top]
    assert len(top) == len(bot), "the sole is not two rings"
    b["col"] = dict(zip(so.tolist(), so[nn].tolist()))
    return top, bot


def cap_bvh(b, co):
    bm_ = bmesh.new()
    vm = {}
    tops = set(b["top"].tolist())
    for fi in b["sole_faces"]:
        p = me.polygons[int(fi)]
        if not all(v in tops for v in p.vertices):
            continue
        vs = []
        for v in p.vertices:
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
    for i, p in enumerate(pts):
        hit = bvh.ray_cast(Vector((p[0], p[1], 0.3)), Vector((0, 0, -1)), 1.0)
        if hit[0] is not None:
            out[i] = hit[0].z
    return out


SGRID = np.arange(-0.15, 0.13, 0.001)
for side, b in BOOT.items():
    b["top"], b["bot"] = faces_top_bottom(b)
    b["stip"] = float(s_of(CO0[b["every"]], b).max())
    b["floor"] = float(CO0[b["sole"], 2].min())
    wt = np.array([welt_top(CO0, b, s0) for s0 in SGRID])
    ok = ~np.isnan(wt)
    wt = np.interp(SGRID, SGRID[ok], wt[ok])
    b["wt"] = gauss1d(wt, 3)                                          # the welt's top along the foot, smoothed over mm
    emin, wid = [], []
    for s0 in SGRID:
        p = np.vstack([section(CO0, b["E_so"], b, s0), section(CO0, b["E_out"], b, s0)])
        if len(p) >= 2:
            emin.append(e_of(p, b).min())
            wid.append(np.ptp(e_of(p, b)))
        else:
            emin.append(np.nan)
            wid.append(np.nan)
    emin, wid = np.array(emin), np.array(wid)
    ok = ~np.isnan(emin)
    piv = np.interp(SGRID, SGRID[ok], emin[ok])
    # the line the toe is drawn in towards: its inside edge (a last's inside edge runs nearly straight and rounds off at
    # the end, its outside curves in: the research's plan view; and the big toe stands on the inside)
    b["piv"] = gauss1d(piv, 3)
    b["eyelace_nn"] = None
    b["widest"] = float(np.nanmax(wid))
    p20 = np.vstack([section(CO0, b["E_so"], b, b["stip"] - 0.02), section(CO0, b["E_out"], b, b["stip"] - 0.02)])
    b["w20"] = float(np.ptp(e_of(p20, b)))


def fields(b):
    """The moves' profiles along s for one boot (each an array over SGRID)."""
    stip, s = b["stip"], SGRID
    nm = "left" if b is BOOT[0] else "right"
    spring_now = M0[nm]["toeSpringMm (the sole's underside 1 mm behind the tip, above the floor)"] / 1000.0
    dS = max(0.0, SPRING - spring_now)
    u = np.clip(s / stip, 0.0, 1.0)
    db = dS * u ** 2.5
    dt = db * smoothstep(b["foot_tip_s"] - 0.005, stip, s) * WELT_FOLLOW
    # the box: its factor at the three sections from the targets, PCHIP between, 1 from FALL behind the ball back
    kk = []
    for d, H in ((50, H50), (30, H30), (10, H10)):
        s0 = stip - d / 1000.0
        top = section(CO0, b["E_out"], b, s0)[:, 2].max()
        wt0 = float(np.interp(s0, SGRID, b["wt"]))
        dt0 = float(np.interp(s0, SGRID, dt))
        # the top comes down by (1 - k) W(h), W(h) = h - 4 mm above the 8 mm band at the welt (see moves)
        kk.append((s0, 1.0 - (wt0 + dt0 + (top - wt0) - (b["floor"] + H)) / ((top - wt0) - 0.004)))
    xs = [-FALL - 0.02, -FALL] + [x for x, _ in kk] + [stip + 0.01]
    ys = [1.0, 1.0] + [y for _, y in kk] + [kk[-1][1]]
    # (holding the box up section by section over the toes, by each lining point's room straight down, was tried on
    # 2 November and kept the whole box within 6% of its height at 3 and 5 cm: the big toe's flank sets every section;
    # the hold point by point below lowers the middle and the outside and bends round the big toe)
    k = pchip(xs, ys, s)
    # the narrowing: n = N v^2, v from NARROW_FROM of the way to the tip (ahead of the foot's widest, where the little
    # toes end), N from the width wanted 2 cm behind the tip
    s20 = stip - 0.02
    sn0 = NARROW_FROM * stip
    v = np.clip((s - sn0) / (stip - sn0), 0.0, 1.0)
    n20 = max(0.0, 1.0 - W20 * b["widest"] / b["w20"])
    N = n20 / ((s20 - sn0) / (stip - sn0)) ** 2
    n = N * v ** 2
    return dict(db=db, dt=dt, k=k, n=n, dS=dS, kAt=kk, N=N)


def moves(b, F, om):
    """The displacement of every point of this boot, from the profiles F; om, one share per outside point of the upper
    (and its lining partner), scales its box and narrowing moves where the foot holds them."""
    D_ = np.zeros((NV, 3))
    # the upper: its outside points moved, each lining point by its partner's move
    p = CO0[b["outer"]]
    s = s_of(p, b)
    e = e_of(p, b)
    h = p[:, 2] - np.interp(s, SGRID, b["wt"])
    k = np.interp(s, SGRID, F["k"])
    # the box squeezed down towards the welt: each height h over the welt's top comes down by (1 - k) W(h), where W
    # is the integral of a smoothstep over the lowest 8 mm, so the leather's vertical scale runs from 1 at the welt to k
    # above 8 mm and is never squeezed harder than k (its foot stays on the welt, its turn there crisp)
    t_ = np.clip(h / 0.008, 0.0, 1.0)
    W = np.where(h >= 0.008, h - 0.004, 0.008 * (t_ ** 3 - 0.5 * t_ ** 4))
    hz = np.where(h > 0, h - (1.0 - k) * W, h)
    dz = om * (hz - h) + np.interp(s, SGRID, F["dt"])
    de = -om * (e - np.interp(s, SGRID, b["piv"])) * np.interp(s, SGRID, F["n"])
    D_[b["outer"]] = b["a"][None, :] * de[:, None] + Z[None, :] * dz[:, None]
    D_[b["inner"]] = D_[b["outer"]]
    # the sole: the underside by db, the top (welt) by dt; both drawn in across with the upper's foot above them
    if "sole_nn" not in b:
        low = np.where(h < 0.005)[0]
        kd = KDTree(len(low))
        for i, j in enumerate(low):
            kd.insert((p[j, 0], p[j, 1], 0.0), i)
        kd.balance()
        b["sole_nn"] = np.array([low[kd.find((q[0], q[1], 0.0))[1]] for q in CO0[b["sole"]]])
    som = dict(zip(b["sole"].tolist(), om[b["sole_nn"]].tolist()))
    for ix, dzf in ((b["top"], F["dt"]), (b["bot"], F["db"])):
        p_ = CO0[ix]
        s_ = s_of(p_, b)
        e_ = e_of(p_, b)
        o_ = np.array([som[int(i)] for i in ix])
        de_ = -o_ * (e_ - np.interp(s_, SGRID, b["piv"])) * np.interp(s_, SGRID, F["n"])
        D_[ix] = b["a"][None, :] * de_[:, None] + Z[None, :] * np.interp(s_, SGRID, dzf)[:, None]
    # eyelets and laces: the mean move of the four nearest outside points (by inverse distance)
    if b["eyelace_nn"] is None:
        kd = KDTree(len(b["outer"]))
        for i, q in enumerate(CO0[b["outer"]]):
            kd.insert(q, i)
        kd.balance()
        nn = []
        for q in CO0[b["eyelace"]]:
            r = kd.find_n(q, 4)
            nn.append(([int(b["outer"][x[1]]) for x in r], [1.0 / max(x[2], 1e-4) for x in r]))
        b["eyelace_nn"] = nn
    for v, (ids, ws) in zip(b["eyelace"], b["eyelace_nn"]):
        D_[v] = (D_[ids] * np.array(ws)[:, None]).sum(0) / sum(ws)
    return D_


def keep_on_welt(b, co_new):
    """The upper's foot kept at its own height over the welt's top where it stood within 3 mm of it."""
    po0 = CO0[b["outer"]]
    if "gap0" not in b:
        b["gap0"] = po0[:, 2] - cap_z(cap_bvh(b, CO0), po0)
    gap0 = b["gap0"]
    cz1 = cap_z(cap_bvh(b, co_new), co_new[b["outer"]])
    w = np.where(np.isnan(gap0) | np.isnan(cz1) | (np.nan_to_num(gap0) < -0.0005), 0.0,
                 1.0 - smoothstep(0.0008, 0.003, np.nan_to_num(gap0)))
    adj = w * ((np.nan_to_num(cz1) + np.nan_to_num(gap0)) - co_new[b["outer"], 2])
    co_new[b["outer"], 2] += adj
    co_new[b["inner"], 2] += adj
    return float(np.abs(adj).max())


REC["targets"] = {"topAboveFloorMm": {"10": mm(H10), "30": mm(H30), "50": mm(H50)}, "toeSpringMm": mm(SPRING),
                  "width20OverWidest": W20, "clearanceMm": mm(CLEAR),
                  "why": "between Epic's (estimated from pictures) and a 1990 derby's set on this boot's own welt and "
                         "sole; 3 cm: the derby's 50 is under the big toe plus 4 mm and the leather, so 53.5; the spring: "
                         "14 mm in the reference pose, about 10 seen in the game, which sets Tom's soles about 3 mm into "
                         "the ground (raise 17 mm against a 21 mm sole)"}
CO = CO0.copy()
REC["moves"] = {}
for side, b in BOOT.items():
    nm = "left" if side == 0 else "right"
    moved = np.concatenate([b["outer"], b["inner"], b["sole"]])
    c0 = clearance(CO0, moved, side)
    no = len(b["outer"])
    pos = {int(v): i for i, v in enumerate(b["outer"])}
    pos.update({int(v): i for i, v in enumerate(b["inner"])})
    om = np.ones(no)
    anchors = {}
    kd_o = KDTree(no)
    for i_, q_ in enumerate(CO0[b["outer"]]):
        kd_o.insert(q_, i_)
    kd_o.balance()
    F = fields(b)
    rounds, sole_offenders = [], 0
    for rnd in range(25):
        cn = CO0 + moves(b, F, om)
        adj = keep_on_welt(b, cn)
        c1 = clearance(cn, moved, side)
        mv = np.linalg.norm(cn[moved] - CO0[moved], axis=1) > 1e-7
        bad = mv & (c1 < CLEAR) & (c1 < c0 - TOL)
        rounds.append(int(bad.sum()))
        if not bad.any():
            break
        # each offender's share of its move that may stay (by halving): its pair held to that share
        for vi in np.where(bad)[0]:
            v = int(moved[vi])
            if v not in pos:
                sole_offenders += 1
                continue
            lo, hi = 0.0, 1.0
            for _ in range(12):
                mid = 0.5 * (lo + hi)
                c = clearance((CO0[v] + mid * (cn[v] - CO0[v]))[None], np.array([0]), side)[0]
                if c >= min(CLEAR, c0[vi] - TOL):
                    lo = mid
                else:
                    hi = mid
            anchors[pos[v]] = min(anchors.get(pos[v], 1.0), om[pos[v]] * lo * 0.95)
        # every point's share: the least, over the held points within R_HOLD, of the held share eased back to whole by
        # distance (a smoothstep), so the leather bends round the toes over about 2 cm instead of denting
        om = np.ones(no)
        for j_, lam_ in anchors.items():
            for (_, i_, d_) in kd_o.find_range(CO0[b["outer"][j_]], R_HOLD):
                om[i_] = min(om[i_], lam_ + (1.0 - lam_) * float(smoothstep(0.0, R_HOLD, d_)))
    CO[b["every"]] = cn[b["every"]]
    b["F"], b["om"] = F, om
    sv = s_of(CO0[b["outer"]], b)
    REC["moves"][nm] = {
        "springAddedMm": mm(F["dS"]),
        "boxFactorAtMmBehindTip (50, 30, 10), from the targets, before the hold": [round(float(y), 3) for _, y in F["kAt"]],
        "narrowAtTipFraction": round(float(F["N"]), 3), "heldRounds (offenders each round)": rounds,
        "soleOffenders": sole_offenders,
        "heldPoints (share under 0.99) and least share": [int((om < 0.99).sum()), round(float(om.min()), 3)],
        "heldBetweenSmm": [mm(sv[om < 0.99].min()), mm(sv[om < 0.99].max())] if (om < 0.99).any() else None,
        "weltKeepAdjustMaxMm": mm(adj),
        "pointMoveMaxMm": mm(np.linalg.norm(CO[b["every"]] - CO0[b["every"]], axis=1).max())}
    say("moves", nm, json.dumps(REC["moves"][nm]))
    c1 = clearance(CO, moved, side)
    mvd = np.linalg.norm(CO[moved] - CO0[moved], axis=1) > 1e-7
    lin = np.isin(moved, b["inner"])
    sm = s_of(CO0[moved], b)
    hm = CO0[moved, 2] - np.interp(sm, SGRID, b["wt"])
    box = lin & (sm > 0) & (hm > 0.015)
    REC.setdefault("clearance", {})[nm] = {
        "liningMinMm_before_after": [mm(c0[lin].min()), mm(c1[lin].min())],
        "toeBoxLiningMinMm_before_after (lining 15 mm or more over the welt, ahead of the ball)": [
            mm(c0[box].min()), mm(c1[box].min())],
        "movedPointsUnder4mm_before_after": [int((mvd & (c0 < CLEAR)).sum()), int((mvd & (c1 < CLEAR)).sum())],
        "movedPointsNowUnder4mmThatWereNot": int((mvd & (c1 < CLEAR) & (c0 >= CLEAR)).sum()),
        "movedPointsNearerThanBeforeAndUnder4mm": int((mvd & (c1 < CLEAR) & (c1 < c0 - TOL)).sum()),
        "pointsInsideTheFoot_before_after": [int((c0 < 0).sum()), int((c1 < 0).sum())]}
    say("clearance", nm, json.dumps(REC["clearance"][nm]))

M1 = measure(CO, "after")
if "--stop-after-moves" in argv:
    sys.exit(0)

# ---- the faces: turned over, stretched against their UVs ------------------------------------------------------------
LV = np.zeros(len(me.loops), dtype=np.int64)
me.loops.foreach_get("vertex_index", LV)
UV = np.zeros(len(me.loops) * 2)
me.uv_layers[0].data.foreach_get("uv", UV)
UV = UV.reshape(-1, 2)
movedv = np.linalg.norm(CO - CO0, axis=1) > 1e-7
tri_l = []                                                       # (loop a, loop b, loop c, polygon) per fan triangle
for p in me.polygons:
    ls = list(range(p.loop_start, p.loop_start + p.loop_total))
    for k_ in range(1, len(ls) - 1):
        tri_l.append((ls[0], ls[k_], ls[k_ + 1], p.index))
tri_l = np.array(tri_l)
TV = LV[tri_l[:, :3]]
touch = movedv[TV].any(1)


def tri_area(co):
    return 0.5 * np.linalg.norm(np.cross(co[TV[:, 1]] - co[TV[:, 0]], co[TV[:, 2]] - co[TV[:, 0]]), axis=1)


A0, A1 = tri_area(CO0), tri_area(CO)
U_ = UV[tri_l[:, :3]]
AUV = 0.5 * np.abs((U_[:, 1, 0] - U_[:, 0, 0]) * (U_[:, 2, 1] - U_[:, 0, 1]) - (U_[:, 2, 0] - U_[:, 0, 0]) * (U_[:, 1, 1] - U_[:, 0, 1]))
okt = touch & (AUV > 1e-12) & (A0 > 1e-12)
rho0, rho1 = A0[okt] / AUV[okt], A1[okt] / AUV[okt]
chg = rho1 / rho0


def edge_stretch(i):
    """The largest and least stretch of one triangle's own plane, before to after (singular values)."""
    a0, b0, c0_ = CO0[TV[i]]
    a1, b1, c1_ = CO[TV[i]]

    def frame2(a, b, c):
        e1 = b - a
        n_ = np.cross(e1, c - a)
        x_ = e1 / np.linalg.norm(e1)
        y_ = np.cross(n_ / np.linalg.norm(n_), x_)
        return np.array([[e1 @ x_, (c - a) @ x_], [e1 @ y_, (c - a) @ y_]])
    J = frame2(a1, b1, c1_) @ np.linalg.inv(frame2(a0, b0, c0_))
    sv_ = np.linalg.svd(J, compute_uv=False)
    return sv_[0], sv_[1]


svs = np.array([edge_stretch(i) for i in np.where(okt)[0]])
med0 = np.median(rho0)
REC["stretch"] = {
    "trianglesTouchingMovedPoints": int(okt.sum()),
    "areaChange_max_min (3D over UV after, against before)": [round(float(chg.max()), 3), round(float(chg.min()), 3)],
    "areaChange_1_50_99pct": np.percentile(chg, [1, 50, 99]).round(3).tolist(),
    "over1.25": int((chg > 1.25).sum()), "under0.8 (1/1.25)": int((chg < 0.8).sum()),
    "edgeStretch_max_least (singular values)": [round(float(svs[:, 0].max()), 3), round(float(svs[:, 1].min()), 3)],
    "edgeStretchOver1.25_orUnder0.8": int(((svs[:, 0] > 1.25) | (svs[:, 1] < 0.8)).sum()),
    "density3DoverUV_against_its_median_max_before_after": [round(float(rho0.max() / med0), 3), round(float(rho1.max() / med0), 3)],
    "flaggedOver1.25 (area or edge)": bool((chg > 1.25).any() or (svs[:, 0] > 1.25).any()),
    "squashedUnder0.8 (area), where": "the nose's front and shoulder, squeezed down to about 0.45 of its height; the "
                                      "leather's grain there is finer, not stretched"}
TPART = np.full(len(tri_l), "other", dtype=object)
for b in BOOT.values():
    for nm_, ix_ in (("outside of the upper", b["outer"]), ("lining", b["inner"]), ("sole", b["sole"])):
        TPART[np.isin(TV, ix_).all(1)] = nm_
for nm_ in ("outside of the upper", "lining", "sole"):
    m_ = TPART[okt] == nm_
    if m_.any():
        REC["stretch"]["byPart: area change max, min; edge stretch max, least; under 0.8"] = REC["stretch"].get(
            "byPart: area change max, min; edge stretch max, least; under 0.8", {})
        REC["stretch"]["byPart: area change max, min; edge stretch max, least; under 0.8"][nm_] = [
            round(float(chg[m_].max()), 3), round(float(chg[m_].min()), 3), round(float(svs[m_, 0].max()), 3),
            round(float(svs[m_, 1].min()), 3), int((chg[m_] < 0.8).sum())]
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
        continue
    c_ = n0_ @ n1_ / np.linalg.norm(n0_) / np.linalg.norm(n1_)
    turned += int(c_ < 0)
    worst = max(worst, math.degrees(math.acos(max(-1.0, min(1.0, c_)))))
REC["faces"] = {"turnedOver": turned, "mostTurnedDeg": round(worst, 1)}

# the sole: one closed piece, thick everywhere; the upper's foot on the welt (the notch of 30 October)
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
    po0, po1 = CO0[b["outer"]], CO[b["outer"]]
    cz0, cz1 = cap_z(cap_bvh(b, CO0), po0), cap_z(cap_bvh(b, CO), po1)
    below0 = ~np.isnan(cz0) & (po0[:, 2] < cz0 - 0.0002)
    below1 = ~np.isnan(cz1) & (po1[:, 2] < cz1 - 0.0002)
    REC["sole"][nm] = {"openEdges": int(sum(1 for c in ec_.values() if c != 2)), "pieces": 1,
                       "thicknessMinMm_before_after": [mm(th0.min()), mm(th1.min())],
                       "thicknessAtTipMm_before_after": [mm(th0[np.argmax(s_of(CO0[b["top"]], b))]), mm(th1[np.argmax(s_of(CO0[b["top"]], b))])],
                       "upperPointsBelowWeltTop_before_after": [int(below0.sum()), int(below1.sum())],
                       "deepestBelowMm_after": mm(-(po1[below1, 2] - cz1[below1]).min()) if below1.any() else 0.0}
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
probe = pair.copy()
probe.data = me.copy()
bpy.context.scene.collection.objects.link(probe)
recompute_normals(probe)
N_RE = np.zeros(len(me.loops) * 3)
probe.data.corner_normals.foreach_get("vector", N_RE)
N_RE = N_RE.reshape(-1, 3)
bpy.data.objects.remove(probe, do_unlink=True)
ang0 = np.degrees(np.arccos(np.clip((N_ORIG * N_RE).sum(1), -1, 1)))
for v, c in zip(me.vertices, CO):
    v.co = Vector(c)
me.update()
recompute_normals(pair)
N_NEW = np.zeros(len(me.loops) * 3)
me.corner_normals.foreach_get("vector", N_NEW)
N_NEW = N_NEW.reshape(-1, 3)
still = ~movedv[LV]
ang1 = np.degrees(np.arccos(np.clip((N_ORIG * N_NEW).sum(1), -1, 1)))
# folds: outside faces of the upper whose winding faces against their own smooth normals
folds = {}
for side, b in BOOT.items():
    oset = set(b["outer"].tolist())
    nb = 0
    for p in me.polygons:
        if all(v in oset for v in p.vertices):
            nn_ = newell(CO, p)
            if nn_ @ N_NEW[p.loop_start:p.loop_start + p.loop_total].sum(0) < 0:
                nb += 1
    folds["left" if side == 0 else "right"] = nb
REC["normals"] = {"recomputedOnThePairGivenDeg_50_99_max": np.percentile(ang0, [50, 99, 100]).round(3).tolist(),
                  "unmovedCornersChangeDeg_max": round(float(ang1[still].max()), 3),
                  "movedCornersChangeDeg_50_99_max": np.percentile(ang1[~still], [50, 99, 100]).round(2).tolist(),
                  "hardEdgesKept": len(SHARP), "foldsAfter": folds}
say("normals", json.dumps(REC["normals"]))

# ---- the export, as v2 was written, then read back against the pair given ----------------------------------------------
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
                groups=sorted(gn.values()), bones={bn.name: np.array(a_.matrix_world @ bn.head_local) for bn in a_.data.bones})


o_, n_ = read(PAIR), read(path)
keys = set(o_["W"]) | set(n_["W"])
REC["export"] = {
    "written": path, "points_given_written": [len(o_["co"]), len(n_["co"])], "faces_given_written": [o_["faces"], n_["faces"]],
    "materials_given_written": [o_["mats"], n_["mats"]], "materialPerFaceSame": bool(np.array_equal(o_["fm"], n_["fm"])),
    "uvLayers": [o_["uvn"], n_["uvn"]], "loopsSame": bool(np.array_equal(o_["lv"], n_["lv"])),
    "maxUvChange": float(np.abs(o_["uv"] - n_["uv"]).max()),
    "groupsSame": o_["groups"] == n_["groups"], "weightsCompared": len(keys),
    "maxWeightChange": float(max(abs(o_["W"].get(k, 0.0) - n_["W"].get(k, 0.0)) for k in keys)),
    "bones": [len(o_["bones"]), len(n_["bones"])],
    "maxBoneMoveMm": round(float(max(np.abs(o_["bones"][k] - n_["bones"][k]).max() for k in o_["bones"])) * 1000, 6),
    "pointsGivenReadBackMaxErrMm": round(float(np.abs(o_["co"] - CO0).max() * 1000), 6),
    "pointsWrittenAsMovedMaxErrMm": round(float(np.abs(n_["co"] - CO).max() * 1000), 6),
    "pointsMoved": int(movedv.sum()), "pointsMovedFurtherBehindTheBallThanTheFall": int(sum(
        int((movedv[b["every"]] & (s_of(CO0[b["every"]], b) < -FALL - 1e-4)).sum()) for b in BOOT.values())),
    "theirLargestMoveMm": round(max([0.0] + [float(np.linalg.norm(CO[v] - CO0[v])) for b in BOOT.values()
                                          for v in b["every"] if movedv[v] and s_of(CO0[v], b) < -FALL - 1e-4]) * 1000, 3)}
say("export", json.dumps(REC["export"], default=str))


# ---- the floor footprints, as sole_footprints.py measures them (the contact decals) ------------------------------------
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
        out[sn] = [[round(float(u[sel].min()) * 100, 2), round(float(u[sel].max()) * 100, 2),
                    round(float(v[sel].min()) * 100, 2), round(float(v[sel].max()) * 100, 2)]
                   for sel in (u <= overlap, u >= -overlap)]
    return out


fp0, fp1 = footprints(o_["co"]), footprints(n_["co"])
REC["footprints"] = {"cm, per side [heel half, ball half] each [along min, max, across min, max]": {"given": fp0, "new": fp1},
                     "largestChangeMm": round(max(abs(x - y) for sn in fp0 for h0, h1 in zip(fp0[sn], fp1[sn])
                                                  for x, y in zip(h0, h1)) * 10, 2)}
say("footprints", json.dumps(REC["footprints"]))
json.dump(REC, open(os.path.join(OUT, "boot-toe-record.json"), "w"), indent=1, default=str)


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

    def mat(name, rgb, alpha=1.0, rough=0.55):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bs = m.node_tree.nodes["Principled BSDF"]
        bs.inputs["Base Color"].default_value = (*rgb, 1)
        bs.inputs["Roughness"].default_value = rough
        bs.inputs["Alpha"].default_value = alpha
        return m

    grey = mat("grey", (0.30, 0.30, 0.30))

    def boot_obj(name, co, m):
        md = bpy.data.meshes.new(name)
        md.from_pydata([tuple(c) for c in co[keep]], [], faces)
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

    old, new = boot_obj("given", CO0, grey), boot_obj("new", CO, grey)
    flm = mat("floor", (0.62, 0.62, 0.60), rough=0.8)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    fl = bpy.context.active_object
    fl.scale = (3.0, 3.0, 0.002)
    fl.location = (0, 0, b["floor"] - 0.001)
    fl.data.materials.append(flm)
    scn.render.engine = "CYCLES"
    scn.cycles.device = "CPU"
    scn.render.threads_mode, scn.render.threads = "FIXED", 4      # leaves the rest of the machine to anything running
    scn.cycles.samples = 48
    scn.cycles.use_denoising = True
    scn.render.resolution_x, scn.render.resolution_y = 960, 560
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
    B_TOE = lambda b_: b_["ball"] * np.array([1.0, 1.0, 0.0]) + b_["f"] * 0.03 + Z * (b_["floor"] + 0.04)  # noqa: E731
    cen = np.array([0.5 * (CO0[b["every"], 0].max() + CO0[b["every"], 0].min()),
                    0.5 * (CO0[b["every"], 1].max() + CO0[b["every"], 1].min()), b["floor"] + 0.075])
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
    views = []
    # side: orthographic, from the outside, level with the floor, the whole boot
    views.append(("side", "ORTHO", Vector(cen + a * 1.0), 0.38, cen))
    # three-quarter: from ahead and outside, 25 degrees up, nearer the toe
    tcen = np.array(B_TOE(b))
    dd = f * math.cos(math.radians(50)) + a * math.sin(math.radians(50))
    el = math.radians(25)
    views.append(("three-quarter", "PERSP", Vector(tcen + dd * 0.85 * math.cos(el) + Z * 0.85 * math.sin(el)), 80.0, tcen))
    W_, H_ = 960, 560

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
        e_[:2], e_[-2:], e_[:, :2], e_[:, -2:] = False, False, False, False     # no edge where the frame cuts the boot
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
        given = shot(tmp, 48, False, (old,), "v2 (given), %s" % vn)
        newp = shot(tmp, 48, False, (new,), "v3 (new), %s" % vn)
        base = shot(tmp, 48, False, (new,), "outlines: v2 red, v3 blue, %s" % vn)
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
            big[(1 - r_) * H_:(2 - r_) * H_, c_ * W_:(c_ + 1) * W_] = px      # Blender's rows run bottom up
    big[..., 3] = 1.0
    big[:, W_ - 1:W_ + 1, :3] = 1.0
    big[:, 2 * W_ - 1:2 * W_ + 1, :3] = 1.0
    big[H_ - 1:H_ + 1, :, :3] = 1.0
    out_im = bpy.data.images.new("preview", W_ * 3, H_ * 2, alpha=False)
    out_im.pixels[:] = big.ravel()
    out_im.filepath_raw = os.path.join(OUT, "boot-toe-preview.png")
    out_im.file_format = "PNG"
    out_im.save()
    return out_im.filepath_raw


if PREVIEW:
    REC["preview"] = {"file": preview(), "layout": "rows: side (orthographic, from the outside), three-quarter (ahead "
                      "and outside, 25 degrees up, nearer the toe); columns: v2 as given, v3, v3 with both outlines (v2 red, v3 blue)",
                      "boot": "left", "renderer": "Cycles on the CPU, 48 samples, a plain grey material"}
json.dump(REC, open(os.path.join(OUT, "boot-toe-record.json"), "w"), indent=1, default=str)
say("done", os.path.join(OUT, "boot-toe-record.json"))
