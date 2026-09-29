"""Boots, trainers or flat shoes modelled over the wearer's own feet, with their skin weights, for a MetaHuman.

    blender -b -P tools/meshgen/blender/model_footwear.py -- BODY.fbx OUT_DIR --kind boot|trainer|shoe [--name ron_boots]

WHY, 30 September (the clothing session, CLOTHES.md items 5 and 6: Ron's
"scuffed black leather boots", Darren's "scuffed white trainers", Sheila's
"flat brown lace-up shoes"; the research, production/research/clothing-
pipeline/FOOTWEAR-2026-09-30.md). Shoes are modelled solids, not cloth. The
recipe, for the left foot, then mirrored:
  - the body's own foot and ankle skin copied up to above the topline, set out
    by the ease and the leather (7 mm), each slice across the foot pushed out to
    its own hull (the toes become one toe box), smoothed;
  - the toe carried forward by the toe allowance (15 to 20 mm) and rounded, the
    bottom flattened onto the sole plane (the bare sole's floor), the toe given
    its spring;
  - the topline cut by a plane (level for the boot, 15 cm; rising forward for a
    low shoe, from 6 to 7 cm at the heel to the instep), the collar rolled;
  - a flat sole under the footprint, a welt beyond it, its waist lifted off the
    ground behind the ball so a heel reads; the foot stays flat (a heel lift
    needs a changed foot pose); the builder raises the character by the sole
    (MetaHumans stand barefoot on the floor since 5.6);
  - eyelets and laces on the instep (the boot's up its front);
  - weights written here: the heel, quarters and sole on foot, the toe box on
    ball across a 35 mm blend on a slanted ball line, the boot's shaft blending
    into the calf; no toe bones.
OUT_DIR gets NAME_render_static.fbx, NAME.blend (the pair, weighted, "FootwearRender") and pictures.
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
BODY, OUT = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


KIND = opt("--kind", "shoe", str)
NAME = opt("--name", "footwear_" + KIND, str)
P = {  # the kinds' numbers (the research)
    "boot": dict(top_back=0.155, top_front=0.148, rise=0.0, sole=0.028, fore=0.015, cup=0.0, welt=0.005, allow=0.016, spring=0.010, toe_h=0.036, toe_m=2.0,
                 upper=(0.012, 0.012, 0.013), sole_rgb=(0.02, 0.02, 0.02), lace_rgb=(0.01, 0.01, 0.01), eyelets=6),
    "trainer": dict(top_back=0.072, top_front=0.100, rise=0.30, sole=0.025, fore=0.018, cup=0.012, welt=0.002, allow=0.012, spring=0.012, toe_h=0.032, toe_m=1.9,
                    upper=(0.80, 0.79, 0.76), sole_rgb=(0.86, 0.85, 0.82), lace_rgb=(0.88, 0.88, 0.86), eyelets=6),
    "shoe": dict(top_back=0.062, top_front=0.092, rise=0.30, sole=0.020, fore=0.008, cup=0.0, welt=0.003, allow=0.014, spring=0.006, toe_h=0.030, toe_m=1.8,
                 upper=(0.075, 0.035, 0.016), sole_rgb=(0.03, 0.017, 0.01), lace_rgb=(0.045, 0.022, 0.01), eyelets=4),
}[KIND]
EASE = opt("--ease", 0.0045) + 0.0025
log = {"body": BODY, "kind": KIND}


def say(*a):
    print("FOOTWEAR", *a, flush=True)


arm, body = tailor.load_body(BODY, lod=opt("--lod", 1, int))
BVH = tailor.bvh_of(body)
co = np.array([body.matrix_world @ v.co for v in body.data.vertices])
J = lambda n: Vector(tuple(tailor.joint(arm, n)))
FLOOR = float(co[:, 2].min())

# ---- the left foot's frame: along the foot (heel to toe, level), across it, up --------------------------------
sole_pts = co[(co[:, 0] > 0.04) & (co[:, 2] < FLOOR + 0.03)]
c2 = sole_pts[:, :2].mean(axis=0)
u_, s_, vt = np.linalg.svd(sole_pts[:, :2] - c2)
d2 = vt[0]
if d2[1] > 0:
    d2 = -d2                                         # towards the toes (-y is forward)
D = Vector((float(d2[0]), float(d2[1]), 0.0)).normalized()
E = Vector((0, 0, 1)).cross(D).normalized()          # across the foot
proj = (sole_pts[:, :2] - c2) @ d2
HEEL = Vector((float(c2[0]), float(c2[1]), FLOOR)) + D * float(proj.min())
L_FOOT = float(proj.max() - proj.min())
S_BALL = float((J("ball_l") - HEEL).dot(D))
log["foot"] = {"lengthMm": round(L_FOOT * 1000), "ballMm": round(S_BALL * 1000)}
say("foot", log["foot"])


def s_of(p):
    return (p - HEEL).dot(D)


def e_of(p):
    return (p - HEEL).dot(E)


def top_at(s):
    """The topline's height above the floor at distance s along the foot."""
    return P["top_back"] + (P["top_front"] - P["top_back"]) * max(0.0, min(1.0, s / 0.12)) + (P["rise"] * max(0.0, s - 0.12) if P["rise"] else 0.0)


# ---- the upper: LOFTED RINGS along the foot (the skin copied and set out showed every toe and tore at the heel,
# 30 September): each ring the foot's own section across it (its hull, set out by the ease and leather), flat
# along the floor, clipped at the topline; in front of the ball a toe box of superellipse sections running to a
# rounded tip the toe allowance beyond the toes; the back and the tip closed; the ankle opening where the rings
# are clipped ----------------------------------------------------------------------------------------------
M_R = int(opt("--around", 32))
foot_pts_all = co[(co[:, 0] > 0.035)]
fp_s = np.array([s_of(Vector(p)) for p in foot_pts_all])
S_TOE0 = float(fp_s[foot_pts_all[:, 2] < FLOOR + 0.03].max())
ec_foot = float(np.median([e_of(Vector(p)) for p in sole_pts]))


def section_hull(s):
    loops = tailor.section_loops(body, HEEL + D * s, D)
    pts = np.concatenate(loops) if loops else np.zeros((0, 3))
    if not len(pts):
        return None
    e2 = np.array([e_of(Vector(p)) for p in pts])
    z2 = pts[:, 2]
    sel = (np.abs(e2 - ec_foot) < 0.085) & (z2 < FLOOR + top_at(s) + 0.06)
    if sel.sum() < 4:
        return None
    return np.array(tailor._hull2(np.column_stack([e2[sel], z2[sel]])))


def ring_from_hull(hull, s, ec, zc):
    """M_R points round the hull by angle about (ec, zc), set out by EASE, clamped onto the floor, clipped at the
    topline; and which of them were clipped."""
    out, clipped = [], []
    for k in range(M_R):
        a = -math.pi / 2 + 2 * math.pi * k / M_R          # from straight down, round the outer side first
        dvec = np.array([math.cos(a), math.sin(a)])
        best = None
        for i in range(len(hull)):
            q0, q1 = hull[i], hull[(i + 1) % len(hull)]
            ed = q1 - q0
            den = dvec[0] * (-ed[1]) + dvec[1] * ed[0]
            if abs(den) < 1e-12:
                continue
            w = q0 - np.array([ec, zc])
            t = (w[0] * (-ed[1]) + w[1] * ed[0]) / den
            u = (dvec[0] * w[1] - dvec[1] * w[0]) / den
            if t > 0 and -1e-9 <= u <= 1 + 1e-9 and (best is None or t > best):
                best = t
        r = (best if best is not None else 0.02) + EASE
        e, z = ec + dvec[0] * r, zc + dvec[1] * r
        z = max(z, FLOOR)
        topz = FLOOR + top_at(s)
        clipped.append(z > topz)
        z = min(z, topz)
        out.append((e, z))
    return out, clipped


rings, clips, s_list = [], [], []
S_START = 0.004
s_samples = list(np.arange(S_START, S_BALL, opt("--ring-step", 0.010))) + [S_BALL]
last = None
for s in s_samples:
    h = section_hull(s)
    if h is None:
        continue
    ec = float(np.mean(h[:, 0]))
    zc = FLOOR + 0.35 * float(h[:, 1].max() - FLOOR) if h[:, 1].max() - FLOOR < 0.08 else FLOOR + 0.03
    r, c = ring_from_hull(h, s, ec, zc)
    rings.append(r)
    clips.append(c)
    s_list.append(s)
# the toe box: superellipse sections from the ball's ring out to the tip
ball_ring = np.array(rings[-1])
ec_b = float((ball_ring[:, 0].max() + ball_ring[:, 0].min()) / 2)
wb = float((ball_ring[:, 0].max() - ball_ring[:, 0].min()) / 2)
hb = float(ball_ring[:, 1].max() - FLOOR)
S_TIP = S_TOE0 + P["allow"] + EASE
NS_ = 3.0
for u in np.linspace(0.0, 0.985, 12)[1:]:
    s = S_BALL + (S_TIP - S_BALL) * u
    w = wb * max(0.0, 1.0 - u ** P["toe_m"]) ** (1 / P["toe_m"]) * (1.0 - 0.10 * u)
    h = hb + (P["toe_h"] - hb) * u ** 1.3
    r = []
    for k in range(M_R):
        a = -math.pi / 2 + 2 * math.pi * k / M_R
        ca, sa = math.cos(a), math.sin(a)
        # the superellipse section: flat bottom at the floor, rounded top h, half-width w
        qn = abs(ca) ** (2 / NS_) * (1 if ca >= 0 else -1)
        e = ec_b + w * qn
        z = FLOOR + (h * sa ** (2 / NS_) if sa > 0 else 0.0)
        # blended from the ball's own ring over the first third (the change of shape had left a step)
        bl = min(1.0, u / 0.35)
        bl = bl * bl * (3 - 2 * bl)
        e = ball_ring[k, 0] * (1 - bl) + e * bl
        z = ball_ring[k, 1] * (1 - bl) + z * bl
        r.append((e, z))
    rings.append(r)
    clips.append([False] * M_R)
    s_list.append(s)
# the mesh: rings joined, the back capped, the tip capped, the clipped lid removed (the ankle opening)
bm = bmesh.new()
V = []
for s, r in zip(s_list, rings):
    row = []
    for e, z in r:
        p = HEEL + D * s + E * e
        row.append(bm.verts.new((p.x, p.y, z)))
    V.append(row)
for i in range(len(V) - 1):
    for k in range(M_R):
        k2 = (k + 1) % M_R
        if clips[i][k] and clips[i][k2] and clips[i + 1][k] and clips[i + 1][k2]:
            continue                                   # the opening
        bm.faces.new((V[i][k], V[i][k2], V[i + 1][k2], V[i + 1][k]))
# the back: a rounded heel cap, pushed back by the ease
r0 = V[0]
cback = sum((v.co for v in r0), Vector()) / M_R - D * (EASE + 0.004)
cv = bm.verts.new(cback)
for k in range(M_R):
    k2 = (k + 1) % M_R
    bm.faces.new((r0[k2], r0[k], cv))                # closed: the heel counter's back, up to the topline
rl = V[-1]
ctip = sum((v.co for v in rl), Vector()) / M_R + D * 0.004
tv = bm.verts.new(ctip)
for k in range(M_R):
    k2 = (k + 1) % M_R
    bm.faces.new((rl[k], rl[k2], tv))
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
# smoothed a little (the edges held), kept off the foot, the bottom on the floor
for _ in range(opt("--smooth", 6, int)):
    new = {}
    for v in bm.verts:
        if v.is_boundary or v.co.z <= FLOOR + 1e-4:
            continue
        nb = [e.other_vert(v).co for e in v.link_edges]
        new[v] = v.co * 0.5 + sum(nb, Vector()) / len(nb) * 0.5
    for v, c in new.items():
        v.co = c
for v in bm.verts:
    hit, nn, _f, _d = BVH.find_nearest(v.co)
    if hit is not None and (v.co - hit).dot(nn) < EASE * 0.6:
        v.co = hit + nn * EASE * 0.6
    if v.co.z < FLOOR:
        v.co.z = FLOOR
log["loft"] = {"rings": len(V), "tipMm": round((S_TIP) * 1000)}
# the collar: its edge put on the topline (the clipped rings left it zigzagging up and down), smoothed, then rolled
loop = [v for v in bm.verts if v.is_boundary]
for v in loop:
    v.co.z = FLOOR + top_at(s_of(v.co))
for _ in range(24):
    new = {}
    for v in loop:
        nb = [e.other_vert(v) for e in v.link_edges if e.is_boundary]
        if len(nb) == 2:
            new[v] = v.co * 0.5 + (nb[0].co + nb[1].co) * 0.25
    for v, c in new.items():
        v.co = c
bm.normal_update()
cedges = [e for e in bm.edges if e.is_boundary]
res = bmesh.ops.extrude_edge_only(bm, edges=cedges)
for v in [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]:
    # TURNED IN, a padded collar (rolled out, it read as a torn lip lifting off)
    hit, nn, _f, _d = BVH.find_nearest(v.co)
    inward = (hit - v.co).normalized() if hit is not None and (v.co - hit).length > 1e-6 else Vector((0, 0, -1))
    v.co = v.co + inward * 0.003 - Vector((0, 0, 0.007))
# toe spring: the front lifted, the most at the tip
s_tip = max(s_of(v.co) for v in bm.verts)
for v in bm.verts:
    s = s_of(v.co)
    if s > S_BALL:
        u = (s - S_BALL) / max(1e-6, s_tip - S_BALL)
        v.co.z += P["spring"] * u * u

S_HEEL_FRONT = 0.27 * L_FOOT
DROP = P["sole"] - P["fore"] - P["cup"]
for v in bm.verts:
    s = s_of(v.co)
    if v.co.z < FLOOR + 0.002 + (P["spring"] if s > S_BALL else 0.0) and s > S_HEEL_FRONT:
        f = min(1.0, (s - S_HEEL_FRONT) / 0.012)
        v.co.z -= DROP * f
upper_me = bpy.data.meshes.new("Upper")
bm.to_mesh(upper_me)
bm.free()
upper = bpy.data.objects.new("Upper", upper_me)
bpy.context.collection.objects.link(upper)
UPPER_BVH = tailor.bvh_of(upper)

# ---- the sole: ALONG THE FOOT'S OWN OUTLINE (the footprint's hull stood out at the arch as a ledge), the welt
# beyond it; a heel block the full stack under the heel, the forepart's visible edge thinner (the upper comes down
# over the difference); for a trainer a cupsole whose wall wraps up round the upper; the waist lifted off the ground
outl_r, outl_l = [], []
for sv, r in zip(s_list, rings):
    ra = np.array(r)
    low = ra[ra[:, 1] < FLOOR + 0.004]
    if len(low) < 2:
        continue
    outl_r.append((sv, float(low[:, 0].max())))
    outl_l.append((sv, float(low[:, 0].min())))
back_s = s_list[0] - EASE - 0.004
tip_s = S_TIP + 0.004
mid_e0 = (outl_r[0][1] + outl_l[0][1]) / 2
outline = [(back_s, mid_e0)] + outl_r + [(tip_s, ec_b)] + outl_l[::-1]
outline = np.array(outline, dtype=float)
for _ in range(6):                                  # smoothed round (the corners at the back and tip rounded)
    outline = 0.5 * outline + 0.25 * (np.roll(outline, 1, axis=0) + np.roll(outline, -1, axis=0))
cen = outline.mean(axis=0)
ring = []
dd_ = np.linalg.norm(np.diff(np.vstack([outline, outline[:1]]), axis=0), axis=1)
cum = np.concatenate([[0.0], np.cumsum(dd_)])
for t in np.linspace(0.0, cum[-1], 81)[:-1]:
    k = int(np.clip(np.searchsorted(cum, t) - 1, 0, len(outline) - 1))
    a, b = outline[k], outline[(k + 1) % len(outline)]
    f = (t - cum[k]) / max(1e-9, dd_[k])
    q = a + (b - a) * f
    ring.append(q)
ring = np.array(ring)
nrm2 = np.roll(ring, -1, axis=0) - np.roll(ring, 1, axis=0)
nrm2 = np.column_stack([nrm2[:, 1], -nrm2[:, 0]])
nrm2 /= np.maximum(np.linalg.norm(nrm2, axis=1), 1e-9)[:, None]
if np.mean(np.sum((ring - cen) * nrm2, axis=1)) < 0:
    nrm2 = -nrm2
ring = ring + nrm2 * (P["welt"] + 0.001)
T = P["sole"]
s_tip = max(s_of(Vector(v.co)) for v in upper_me.vertices)
sm = bmesh.new()
top_r, bot_r = [], []
for s, e in ring:
    base = HEEL + D * float(s) + E * float(e)
    lift = P["spring"] * max(0.0, (s - S_BALL) / max(1e-6, s_tip - S_BALL)) ** 2 if s > S_BALL else 0.0
    waist = 0.0
    if KIND != "trainer" and S_HEEL_FRONT + 0.004 < s < S_BALL - 0.015:
        waist = 0.004 * math.sin(math.pi * (s - S_HEEL_FRONT - 0.004) / (S_BALL - 0.019 - S_HEEL_FRONT)) ** 0.4
    ztop = FLOOR + P["cup"] + (0.0 if s < S_HEEL_FRONT else -DROP * min(1.0, (s - S_HEEL_FRONT) / 0.012))
    top_r.append(sm.verts.new((base.x, base.y, ztop + lift)))
    bot_r.append(sm.verts.new((base.x, base.y, FLOOR - T + P["cup"] + lift + waist)))
n = len(ring)
for i_ in range(n):
    j_ = (i_ + 1) % n
    sm.faces.new((top_r[i_], top_r[j_], bot_r[j_], bot_r[i_]))
sm.faces.new(top_r[::-1])
sm.faces.new(bot_r)
bmesh.ops.triangulate(sm, faces=sm.faces[:])
bmesh.ops.recalc_face_normals(sm, faces=sm.faces[:])
sole_me = bpy.data.meshes.new("Sole")
sm.to_mesh(sole_me)
sm.free()
sole = bpy.data.objects.new("Sole", sole_me)
bpy.context.collection.objects.link(sole)
bev = sole.modifiers.new("Bevel", "BEVEL")                    # the sole's edges rounded, not a slab's
bev.width, bev.segments, bev.limit_method = 0.0025, 2, "ANGLE"
log["sole"] = {"mm": T * 1000, "weltMm": P["welt"] * 1000}

# ---- the tongue, eyelets and laces, CENTRED ON THE TOP OF THE INSTEP (the first tries put them on the
# outer side: they were centred on the heel's line, not the foot's top); the laces crossing; a bow on a shoe ----
lace_m = tailor.material("M_Lace", P["lace_rgb"], 0.6)
metal = tailor.material("M_Eyelet", (0.03, 0.03, 0.03) if KIND != "trainer" else (0.7, 0.7, 0.7), 0.35)
extras = []
n_e = P["eyelets"]


def top_e(s):
    """Across the foot, where its top is highest at s (the lace line)."""
    best = (ec_b, -1.0)
    for e in np.linspace(ec_b - 0.05, ec_b + 0.05, 41):
        org = HEEL + D * s + E * float(e) + Vector((0, 0, 0.4))
        hit = UPPER_BVH.ray_cast(org, Vector((0, 0, -1)), 0.6)[0] or BVH.ray_cast(org, Vector((0, 0, -1)), 0.6)[0]
        if hit is not None and hit.z > best[1]:
            best = (float(e), hit.z)
    return best[0]


def on_top(s, e, from_front_z=None):
    """The upper's surface (or, in the opening, the foot's plus the ease) at s, e: from above, or for a boot's
    shaft from in front at height z."""
    if from_front_z is None:
        org = HEEL + D * s + E * e + Vector((0, 0, 0.4))
        dr = Vector((0, 0, -1))
    else:
        org = HEEL + D * (s + 0.3) + E * e + Vector((0, 0, from_front_z))
        dr = -D
    hit, nn, _i, _d = UPPER_BVH.ray_cast(org, dr, 0.8)
    if hit is None:
        hit, nn, _i, _d = BVH.ray_cast(org, dr, 0.8)
        if hit is None:
            return None
        hit = hit + nn * EASE
    return hit, nn


if KIND == "boot":
    lace_rows = [(0.07 + 0.05 * t, P["top_back"] - 0.014 - 0.09 * t) for t in np.linspace(0.0, 1.0, n_e)]
else:
    s0 = 0.108 if KIND == "trainer" else 0.112
    lace_rows = [(s0 + (0.058 if KIND == "trainer" else 0.036) * t, None) for t in np.linspace(0.0, 1.0, n_e)]
HALF = 0.012 if KIND != "boot" else 0.015
lace_pts = []
for s, z in lace_rows:
    ec_l = top_e(s)
    row = [on_top(s, ec_l + side * HALF, z) for side in (-1.0, 1.0)]
    lace_pts.append(row)
# the tongue: a strip 44 mm wide under the laces, from the vamp up through the opening to 12 mm above it
tongue_rows = []
s_a = lace_rows[-1][0] + 0.012
s_b = lace_rows[0][0] - 0.022
for t in np.linspace(0.0, 1.0, 10):
    s = s_a + (s_b - s_a) * t
    zf = None if KIND != "boot" else (lace_rows[-1][1] + (lace_rows[0][1] + 0.012 - lace_rows[-1][1]) * t)
    ec_l = top_e(s) if KIND != "boot" else top_e(lace_rows[-1][0])
    row = []
    for e in np.linspace(-0.022, 0.022, 7):
        q = on_top(s, ec_l + e, zf)
        row.append(None if q is None else q[0] + q[1] * 0.0012)
    if all(r_ is not None for r_ in row):
        tongue_rows.append(row)
if len(tongue_rows) > 2:
    # its top edge lifted 12 mm above the collar, as a tongue stands
    top_row = [p_ + Vector((0, 0, 0.012)) - D * 0.004 for p_ in tongue_rows[-1]]
    tongue_rows.append(top_row)
    tv_, tf_ = [], []
    w_ = len(tongue_rows[0])
    for r_ in tongue_rows:
        tv_.extend(tuple(p_) for p_ in r_)
    for i_ in range(len(tongue_rows) - 1):
        for j_ in range(w_ - 1):
            tf_.append((i_ * w_ + j_, i_ * w_ + j_ + 1, (i_ + 1) * w_ + j_ + 1, (i_ + 1) * w_ + j_))
    tm = bpy.data.meshes.new("Tongue")
    tm.from_pydata(tv_, [], tf_)
    to = bpy.data.objects.new("Tongue", tm)
    bpy.context.collection.objects.link(to)
    tm.materials.append(tailor.material("M_Upper", P["upper"], 0.5))
    sl = to.modifiers.new("Solidify", "SOLIDIFY")
    sl.thickness, sl.offset = 0.002, -1.0
    extras.append(to)


def bar(a, b, w=0.004, t=0.0022):
    mid = (a + b) / 2
    L_ = (b - a).length
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=mid)
    o = bpy.context.active_object
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = Vector((1, 0, 0)).rotation_difference((b - a).normalized())
    o.scale = (L_, w, t)
    o.data.materials.append(lace_m)
    extras.append(o)


pts_ok = [r_ for r_ in lace_pts if r_[0] is not None and r_[1] is not None]
for row in pts_ok:
    for hit, nn in row:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.0028, minor_radius=0.0009, location=hit + nn * 0.0012)
        o = bpy.context.active_object
        o.rotation_mode = "QUATERNION"
        o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(nn)
        o.data.materials.append(metal)
        extras.append(o)
for k in range(len(pts_ok) - 1):
    a0, a1 = pts_ok[k], pts_ok[k + 1]
    lift = 0.0035
    bar(a0[0][0] + a0[0][1] * lift, a1[1][0] + a1[1][1] * lift)     # crossing
    bar(a0[1][0] + a0[1][1] * lift, a1[0][0] + a1[0][1] * lift)
if pts_ok and KIND != "boot":
    # a bow at the top pair: two loops and two ends
    (hl, nl), (hr, nr) = pts_ok[0]
    c_ = (hl + hr) / 2 + nl * 0.005
    for sg in (-1.0, 1.0):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.008, minor_radius=0.0016, location=c_ + E * (sg * 0.009))
        o = bpy.context.active_object
        o.rotation_mode = "QUATERNION"
        o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference((nl + D * 0.3).normalized())
        o.scale = (1.0, 0.55, 1.0)
        o.data.materials.append(lace_m)
        extras.append(o)
        bar(c_, c_ + E * (sg * 0.006) + D * 0.022 - Vector((0, 0, 0.012)), w=0.004, t=0.002)
elif pts_ok:
    (hl, nl), (hr, nr) = pts_ok[0]
    bar(hl + nl * 0.004, hr + nr * 0.004)
log["eyelets"] = sum(2 for r_ in pts_ok)

# ---- a toe cap and a heel counter: overlays cut from the upper by planes (clean edges), 1.2 mm proud -----------
for part, keep_fn, planes in (
        ("ToeCap", lambda c: s_of(c) > S_BALL + 0.35 * (S_TIP - S_BALL), [(HEEL + D * (S_BALL + 0.35 * (S_TIP - S_BALL)), -D)]),
        ("HeelCounter", lambda c: s_of(c) < 0.075 and c.z < FLOOR + top_at(s_of(c)) - 0.014,
         [(HEEL + D * 0.075, D), (HEEL + Vector((0, 0, P["top_back"] - 0.014)), Vector((0, 0, 1)))])):
    ob = bmesh.new()
    ob.from_mesh(upper_me)
    for pc, pn in planes:
        bmesh.ops.bisect_plane(ob, geom=ob.verts[:] + ob.edges[:] + ob.faces[:], plane_co=pc, plane_no=pn, clear_outer=True)
    bmesh.ops.delete(ob, geom=[f for f in ob.faces if not keep_fn(f.calc_center_median())], context="FACES")
    bmesh.ops.delete(ob, geom=[v for v in ob.verts if not v.link_faces], context="VERTS")
    ob.normal_update()
    for v in ob.verts:
        hit, nn, _f, _d = BVH.find_nearest(v.co)
        out = (v.co - hit).normalized() if hit is not None and (v.co - hit).length > 1e-6 else Vector((0, 0, 1))
        v.co = v.co + out * 0.0012
    om = bpy.data.meshes.new(part)
    ob.to_mesh(om)
    ob.free()
    if len(om.polygons) > 4:
        oo = bpy.data.objects.new(part, om)
        bpy.context.collection.objects.link(oo)
        om.materials.append(tailor.material("M_Upper", P["upper"], 0.5))
        sl = oo.modifiers.new("Solidify", "SOLIDIFY")
        sl.thickness, sl.offset = 0.0012, 1.0
        extras.append(oo)

# ---- materials, thickness, the pair, weights ----------------------------------------------------------------
upm = tailor.material("M_Upper", P["upper"], 0.45 if KIND != "trainer" else 0.55)
som = tailor.material("M_Sole", P["sole_rgb"], 0.8)
upper_me.materials.append(upm)
sole_me.materials.append(som)
rb = bmesh.new()
rb.from_mesh(upper_me)
bmesh.ops.recalc_face_normals(rb, faces=rb.faces[:])
rb.normal_update()
vote = 0.0
for f in list(rb.faces)[::5]:
    c = f.calc_center_median()
    hit, _n, _i, _d = BVH.find_nearest(c)
    if hit is not None:
        vote += f.normal.dot(c - hit)
if vote < 0:
    bmesh.ops.reverse_faces(rb, faces=rb.faces[:])
rb.to_mesh(upper_me)
rb.free()
sol = upper.modifiers.new("Solidify", "SOLIDIFY")
sol.thickness, sol.offset, sol.use_rim = 0.0025, -1.0, True
for o in [upper, sole] + extras:
    for p_ in o.data.polygons:
        p_.use_smooth = o is upper
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    for mdf in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=mdf.name)
    for m in list(o.modifiers):
        o.modifiers.remove(m)
bpy.ops.object.select_all(action="DESELECT")
for o in [upper, sole] + extras:
    o.select_set(True)
bpy.context.view_layer.objects.active = upper
bpy.ops.object.join()
left = bpy.context.active_object
left.name = "FootwearLeft"


def weigh(obj, side):
    """foot behind the ball line, ball in front across a 35 mm blend on a slanted line (the inner side 15 mm further
    forward); the boot's shaft into the calf above the ankle."""
    g_foot = obj.vertex_groups.new(name="foot_" + side)
    g_ball = obj.vertex_groups.new(name="ball_" + side)
    g_calf = obj.vertex_groups.new(name="calf_" + side) if KIND == "boot" else None
    sg = 1.0 if side == "l" else -1.0
    for v in obj.data.vertices:
        p = obj.matrix_world @ v.co
        pl = Vector((p.x * sg, p.y, p.z))                 # in the left foot's frame
        s, e = s_of(pl), e_of(pl)
        inner = -e                                         # E points away from the body's middle on the left foot
        line = S_BALL + 0.015 * max(-1.0, min(1.0, inner / 0.04))
        wb = max(0.0, min(1.0, (s - line + 0.0175) / 0.035))
        wc = 0.0
        if g_calf is not None:
            wc = max(0.0, min(1.0, (p.z - FLOOR - 0.10) / 0.05))
        wf = max(0.0, 1.0 - wb - wc)
        wb = wb * (1.0 - wc)
        for g, w in ((g_foot, wf), (g_ball, wb), (g_calf, wc)):
            if g is not None and w > 1e-4:
                g.add([v.index], w, "REPLACE")


# the right one: mirrored across the body's middle
right = left.copy()
right.data = left.data.copy()
bpy.context.collection.objects.link(right)
right.name = "FootwearRight"
for v in right.data.vertices:
    v.co.x = -v.co.x
rb = bmesh.new()
rb.from_mesh(right.data)
bmesh.ops.reverse_faces(rb, faces=rb.faces[:])
rb.to_mesh(right.data)
rb.free()
weigh(left, "l")
weigh(right, "r")
bpy.ops.object.select_all(action="DESELECT")
left.select_set(True)
right.select_set(True)
bpy.context.view_layer.objects.active = left
bpy.ops.object.join()
pair = bpy.context.active_object
pair.name = "FootwearRender"
pair.data.name = "FootwearRender"
log["render"] = {"verts": len(pair.data.vertices), "tris": sum(len(p_.vertices) - 2 for p_ in pair.data.polygons)}
say("render", log["render"])
bpy.ops.object.select_all(action="DESELECT")
pair.select_set(True)
bpy.context.view_layer.objects.active = pair
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, "%s_render_static.fbx" % NAME), use_selection=True,
                         object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
grey = tailor.material("M_Body", (0.18, 0.18, 0.19))          # darker than any shoe, so white trainers read
body.data.materials.clear()
body.data.materials.append(grey)
# the feet inside hidden in the pictures, as the game hides them under shoes
hid = body.vertex_groups.new(name="in_shoe")
hide_ids = []
for v in body.data.vertices:
    p = body.matrix_world @ v.co
    pl = Vector((abs(p.x), p.y, p.z))
    if p.z < FLOOR + top_at(max(0.0, s_of(pl))) - 0.02 and abs(e_of(pl) - ec_foot) < 0.08 and -0.01 < s_of(pl) < S_TIP:
        hide_ids.append(v.index)
hid.add(hide_ids, 1.0, "REPLACE")
mk = body.modifiers.new("InShoe", "MASK")
mk.vertex_group = "in_shoe"
mk.invert_vertex_group = True
MID = Vector((0.0, float(HEEL.y) - 0.10, FLOOR + 0.06))
tailor.pictures(os.path.join(OUT, "feet"), MID, views=(("front", (0, -0.9, 0.12)), ("side", (0.9, 0.0, 0.05)), ("back", (0, 0.9, 0.12)),
                                                     ("three-quarter", (0.65, -0.65, 0.25))), res=(700, 500))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "footwear.json"), "w"), indent=1)
say("done", json.dumps(log))
