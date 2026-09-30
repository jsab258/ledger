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
    "trainer": dict(top_back=0.072, top_front=0.100, rise=0.30, sole=0.025, fore=0.018, cup=0.012, welt=0.002, allow=0.012, spring=0.010, toe_h=0.032, toe_m=1.9,
                    upper=(0.80, 0.79, 0.76), sole_rgb=(0.86, 0.85, 0.82), lace_rgb=(0.88, 0.88, 0.86), eyelets=7,
                    throat=0.67, slot=(0.010, 0.007), eyelet_off=0.008, tongue_up=0.020, nose=0.015),
    "shoe": dict(top_back=0.062, top_front=0.092, rise=0.30, sole=0.020, fore=0.008, cup=0.004, welt=0.003, allow=0.014, spring=0.008, toe_h=0.030, toe_m=1.8,
                 upper=(0.075, 0.035, 0.016), sole_rgb=(0.03, 0.017, 0.01), lace_rgb=(0.045, 0.022, 0.01), eyelets=4,
                 throat=0.59, slot=(0.003, 0.002), eyelet_off=0.0095, tongue_up=0.006, nose=0.013),
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


SLOPE = (P["top_front"] - P["top_back"]) / 0.12


def top_at(s):
    """The topline's height above the floor at distance s along the foot: one plane, rising forward for a low shoe
    (the opening cut by it is a clean, flat curve)."""
    return P["top_back"] + SLOPE * s


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


CO_S = (co[:, :2] - np.array([HEEL.x, HEEL.y])) @ np.array([D.x, D.y])
CO_E = (co[:, :2] - np.array([HEEL.x, HEEL.y])) @ np.array([E.x, E.y])


def section_hull(s):
    loops = tailor.section_loops(body, HEEL + D * s, D)
    pts = np.concatenate(loops) if loops else np.zeros((0, 3))
    if not len(pts):
        return None
    e2 = np.array([e_of(Vector(p)) for p in pts])
    z2 = pts[:, 2]
    if s < 0.06:
        # at the heel the section at s is only the heel's back, below the collar (a dip in it there): the leg's
        # points up to 3 cm ahead added, so the counter rises to the collar round the tendon
        ahead = (CO_S > s) & (CO_S < s + 0.03) & (co[:, 2] > FLOOR + 0.04)
        e2 = np.concatenate([e2, CO_E[ahead]])
        z2 = np.concatenate([z2, co[ahead, 2]])
    sel = (np.abs(e2 - ec_foot) < 0.085) & (z2 < FLOOR + top_at(s) + 0.012)
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
        clipped.append(False)                         # the opening is cut by the topline's plane afterwards
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
for _ in range(2):                                   # eased along the foot, the ball's ring held
    ra_ = np.array(rings)
    sm_ = ra_.copy()
    sm_[1:-1] = 0.25 * ra_[:-2] + 0.5 * ra_[1:-1] + 0.25 * ra_[2:]
    rings = [list(map(tuple, r_)) for r_ in sm_[:-1]] + [rings[-1]]
# the toe box: superellipse sections from the ball's ring out to the tip
ball_ring = np.array(rings[-1])
ec_b = float((ball_ring[:, 0].max() + ball_ring[:, 0].min()) / 2)
wb = float((ball_ring[:, 0].max() - ball_ring[:, 0].min()) / 2)
hb = float(ball_ring[:, 1].max() - FLOOR)
S_TIP = S_TOE0 + P["allow"] + EASE
NS_ = {"boot": 3.0, "trainer": 2.6, "shoe": 2.3}[KIND]
TIP_H = opt("--tip-h", 0.55)
if KIND == "boot":
    for u in np.linspace(0.0, 0.985, 12)[1:]:
        s = S_BALL + (S_TIP - S_BALL) * u
        w = wb * max(0.0, 1.0 - u ** P["toe_m"]) ** (1 / P["toe_m"]) * (1.0 - 0.10 * u)
        h = hb + (P["toe_h"] - hb) * u ** 1.3
        if KIND != "boot" and u > 0.5:
            h *= math.sqrt(max(0.0, 1.0 - ((u - 0.5) / 0.5) ** 2)) * 0.75 + 0.25
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
else:
    # THE TOE BOX DRAWN AS A LAST IS, to the research's numbers (production/research/clothing-pipeline/SHOE-TOE-AND-
    # LACING-2026-09-30.md; the third try, after two reviews called a dome over the toes "a clown shoe" and the toes'
    # own shapes stood up as pads and a nub). The feet are hidden inside the shoes, so the toe need not clear them.
    # Its top falls steadily from the ball: three quarters of the ball's height half way, 0.6 at four fifths, a nose
    # NOSE tall at the tip. Seen from above the inner edge runs straight to nine tenths of the length and then rounds;
    # the outer edge curves in from the ball; the tip lines up with the second toe. Each section a flat-bottomed
    # round; the last a seam, welded
    NT_ = opt("--toe-flat", 2.6)
    NOSE = P["nose"]
    hb_z = float(ball_ring[:, 1].max())
    Hb = hb_z - FLOOR
    e_med0, e_lat0 = float(ball_ring[:, 0].min()), float(ball_ring[:, 0].max())
    e_tip = e_med0 + 0.35 * (e_lat0 - e_med0)
    u_med = max(0.3, min(0.9, (0.9 * S_TIP - S_BALL) / (S_TIP - S_BALL)))
    us_ = [1.0 - (1.0 - t) ** 1.5 for t in np.linspace(0.0, 1.0, 17)[1:]]
    for i_, u in enumerate(us_):
        s = S_BALL + u * (S_TIP - S_BALL)
        if u <= u_med:
            e_m = e_med0
        else:
            v_ = (u - u_med) / (1.0 - u_med)
            e_m = e_tip - (e_tip - e_med0) * math.sqrt(max(0.0, 1.0 - v_ * v_))
        e_l = e_tip + (e_lat0 - e_tip) * max(0.0, 1.0 - u ** 1.45) ** (1 / 1.45)
        if u <= 0.8:
            f_ = 1.0 - 0.5 * u
        else:
            v_ = (u - 0.8) / 0.2
            f_ = NOSE / Hb + (0.6 - NOSE / Hb) * math.sqrt(max(0.0, 1.0 - v_ * v_))
        hz = FLOOR + Hb * f_
        c, w = 0.5 * (e_m + e_l), 0.5 * (e_l - e_m)
        b = min(1.0, (i_ + 1) / 2.0)                     # the first section a blend from the ball's own
        r_ = []
        for k in range(M_R):
            a = -math.pi / 2 + 2 * math.pi * k / M_R
            ca, sa = math.cos(a), math.sin(a)
            e_r = c + w * abs(ca) ** (2 / NT_) * (1 if ca >= 0 else -1)
            z_r = FLOOR + ((hz - FLOOR) * sa ** (2 / NT_) if sa > 0 else 0.0)
            r_.append((ball_ring[k, 0] * (1 - b) + e_r * b, ball_ring[k, 1] * (1 - b) + z_r * b))
        if u >= 1.0 - 1e-9:
            r_ = [(c, 0.5 * (r_[k][1] + r_[(M_R - k) % M_R][1])) for k in range(M_R)]
        rings.append(r_)
        clips.append([False] * M_R)
        s_list.append(float(s))
    # the rings eased along the foot across the ball, where the foot's own sections meet the drawn toe (a hump)
    ra_ = np.array(rings)
    for _ in range(2):
        sm_ = ra_.copy()
        sm_[1:-2] = 0.25 * ra_[:-3] + 0.5 * ra_[1:-2] + 0.25 * ra_[2:-1]
        ra_ = sm_
    rings = [list(map(tuple, r_)) for r_ in ra_]
# the heel: rings narrowing behind the first, upright, round in plan, EASE and 4 mm behind it (a fan from the first
# ring left a notch at the collar and spikes at the floor)
r0a = np.array(rings[0])
ec0 = float((r0a[:, 0].max() + r0a[:, 0].min()) / 2)
RB = EASE + 0.004
back_r, back_s = [], []
for t in (1.0, 0.9, 0.75, 0.55, 0.3):
    f = math.cos(t * math.pi / 2) if t < 1.0 else 0.0
    back_s.append(s_list[0] - RB * math.sin(t * math.pi / 2))
    if t < 1.0:
        back_r.append([(ec0 + (e - ec0) * f, z) for e, z in rings[0]])
    else:
        zz = [z for _e, z in rings[0]]
        back_r.append([(ec0, 0.5 * (zz[k] + zz[(M_R - k) % M_R])) for k in range(M_R)])
rings = back_r + rings
s_list = back_s + s_list
clips = [[False] * M_R for _ in back_r] + clips
# the mesh: rings joined, the back and the tip capped, the opening cut by the topline's plane
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
bmesh.ops.remove_doubles(bm, verts=V[0], dist=1e-5)     # the back seam: the two sides of the last ring welded
rl = V[-1]
if KIND == "boot":
    ctip = sum((v.co for v in rl), Vector()) / M_R + D * 0.002
    tv = bm.verts.new(ctip)
    for k in range(M_R):
        k2 = (k + 1) % M_R
        bm.faces.new((rl[k], rl[k2], tv))
else:
    bmesh.ops.remove_doubles(bm, verts=rl, dist=1e-5)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=HEEL + Vector((0, 0, P["top_back"])),
                       plane_no=(Vector((0, 0, 1)) - D * SLOPE).normalized(), clear_outer=True)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
# smoothed a little (the edges held), kept off the foot, the bottom on the floor
# (Taubin's two passes, one shrinking and one swelling, so the surface is evened without being drawn onto the foot:
# the plain passes drew it in, and kept off the foot it took the toes' bumps)
for round_, lam in [(r_ // 2, (0.5, -0.53)[r_ % 2]) for r_ in range(2 * opt("--smooth", 6, int))]:
    new = {}
    for v in bm.verts:
        if v.co.z <= FLOOR + 1e-4:
            fl = [e.other_vert(v).co for e in v.link_edges if e.other_vert(v).co.z <= FLOOR + 1e-4]
            if len(fl) >= 2:
                c_ = v.co + (sum(fl, Vector()) / len(fl) - v.co) * lam
                new[v] = Vector((c_.x, c_.y, FLOOR))
            continue
        if v.is_boundary:
            if lam < 0:
                continue                             # the swelling pass drove the opening's front into a spike
            nb = [e.other_vert(v).co for e in v.link_edges if e.is_boundary]
        else:
            nb = [e.other_vert(v).co for e in v.link_edges]
        if nb:
            new[v] = v.co + (sum(nb, Vector()) / len(nb) - v.co) * lam
    for v, c in new.items():
        v.co = c
    if lam > 0:
        continue
    for v in bm.verts:
        hit, nn, _f, _d = BVH.find_nearest(v.co)
        if hit is not None and (v.co - hit).dot(nn) < EASE * 0.6 and (
                KIND == "boot" or v.co.z > FLOOR + top_at(s_of(v.co)) - 0.035 or s_of(v.co) < S_BALL - 0.02):
            v.co = v.co.lerp(hit + nn * EASE * 0.6, 0.6 if round_ < 5 else 1.0)
        if v.co.z < FLOOR:
            v.co.z = FLOOR
log["loft"] = {"rings": len(V), "tipMm": round((S_TIP) * 1000)}
# the collar: its edge put on the topline (the clipped rings left it zigzagging up and down), smoothed, then rolled
bmesh.ops.remove_doubles(bm, verts=[v for v in bm.verts if v.is_boundary], dist=0.0008)
loop = [v for v in bm.verts if v.is_boundary]
for v in loop:
    v.co.z = FLOOR + top_at(s_of(v.co))
for _ in range(6):
    new = {}
    for v in loop:
        nb = [e.other_vert(v) for e in v.link_edges if e.is_boundary]
        if len(nb) == 2:
            new[v] = v.co * 0.5 + (nb[0].co + nb[1].co) * 0.25
    for v, c in new.items():
        v.co = c
bm.normal_update()
cedges = [e for e in bm.edges if e.is_boundary] if opt("--collar-roll", 0, int) else []
# (by default no turned-in strip: the plane's clean cut and the leather's own thickness make the edge; turned in,
# it met the leg, and kept off the leg, it stood out as a frill)
res = bmesh.ops.extrude_edge_only(bm, edges=cedges) if cedges else {"geom": []}
OPEN_C = sum((v.co for v in loop), Vector()) / max(1, len(loop))
for v in [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]:
    # TURNED IN, a padded collar (rolled out, it read as a torn lip lifting off)
    inward = OPEN_C - v.co
    inward.z = 0.0
    inward = inward.normalized() if inward.length > 1e-6 else Vector((0, 0, 0))
    v.co = v.co + inward * 0.0015 - Vector((0, 0, 0.007))
    hit, nn, _f, _d = BVH.find_nearest(v.co)
    if hit is not None and (v.co - hit).dot(nn) < 0.004:
        v.co = hit + nn * 0.004
# toe spring: the front lifted, the most at the tip
s_tip = max(s_of(v.co) for v in bm.verts)
for v in bm.verts:
    s = s_of(v.co)
    if s > S_BALL:
        u = (s - S_BALL) / max(1e-6, s_tip - S_BALL)
        v.co.z += P["spring"] * u * u

S_HEEL_FRONT = 0.27 * L_FOOT
DROP = max(0.0, P["sole"] - P["fore"])
S_TIP_U = max(s_of(v.co) for v in bm.verts)


def lift_at(s):
    return P["spring"] * max(0.0, (s - S_BALL) / max(1e-6, S_TIP_U - S_BALL)) ** 2 if s > S_BALL else 0.0


def drop_at(s):
    run = (S_BALL - 0.02 - S_HEEL_FRONT) if KIND == "trainer" else 0.012
    u = max(0.0, min(1.0, (s - S_HEEL_FRONT) / run))
    return DROP * u * u * (3 - 2 * u)


def floor_at(s):
    """The upper's own floor at s: the bare floor, lowered in front of the heel by the drop, lifted by the spring."""
    return FLOOR - drop_at(s) + lift_at(s)


for v in bm.verts:
    s = s_of(v.co)
    zr = v.co.z - (FLOOR + lift_at(s))
    if zr < 0.035:
        u_ = 1.0 - max(0.0, zr) / 0.035
        v.co.z -= drop_at(s) * u_ * u_ * (3 - 2 * u_)
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
uv_ = np.array([tuple(v.co) for v in upper_me.vertices])
us_ = np.array([s_of(Vector(q)) for q in uv_])
ue_ = np.array([e_of(Vector(q)) for q in uv_])
uzr = uv_[:, 2] - np.array([floor_at(q) for q in us_])
band = uzr < max(P["cup"], 0.004) + 0.010
for sv in np.arange(s_list[0], S_TIP_U - 0.006, 0.008):
    sel = band & (np.abs(us_ - sv) < 0.005)
    if sel.sum() < 2:
        continue
    outl_r.append((float(sv), float(ue_[sel].max())))
    outl_l.append((float(sv), float(ue_[sel].min())))
back_s = float(us_.min()) - 0.001
tip_s = S_TIP_U + 0.001
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
bpts = np.column_stack([us_[band], ue_[band]])
tng = np.column_stack([-nrm2[:, 1], nrm2[:, 0]])
need = np.zeros(len(ring))
for i_ in range(len(ring)):
    rel = bpts - ring[i_]
    near = np.abs(rel @ tng[i_]) < 0.006
    if near.any():
        need[i_] = max(0.0, float((rel[near] @ nrm2[i_]).max()))
need = np.max([np.roll(need, k) for k in range(-3, 4)], axis=0)
for _ in range(3):
    need = 0.25 * np.roll(need, 1) + 0.5 * need + 0.25 * np.roll(need, -1)
ring = ring + nrm2 * need[:, None]
RING_IN = ring.copy()
_seg_a, _seg_b = RING_IN, np.roll(RING_IN, -1, axis=0)
for v in upper_me.vertices:
    sv, ev = s_of(v.co), e_of(v.co)
    zr = v.co.z - floor_at(sv)
    if zr <= 0.0005 or zr > 0.012:
        continue                                     # the floor itself stays inside; above 12 mm is untouched
    q = np.array([sv, ev])
    ab = _seg_b - _seg_a
    t_ = np.clip(np.sum((q - _seg_a) * ab, axis=1) / np.maximum(np.sum(ab * ab, axis=1), 1e-12), 0.0, 1.0)
    cl = _seg_a + ab * t_[:, None]
    k_ = int(np.argmin(np.sum((cl - q) ** 2, axis=1)))
    w_ = (1.0 - zr / 0.012) ** 2 * 0.9
    tgt = cl[k_] - nrm2[k_] * 0.0008                 # a hair inside the line, under the sole's rim
    ns, ne = sv + (tgt[0] - sv) * w_, ev + (tgt[1] - ev) * w_
    p3 = HEEL + D * float(ns) + E * float(ne)
    v.co = Vector((p3.x, p3.y, v.co.z))
ring = ring + nrm2 * (P["welt"] + 0.001)
T = P["sole"]
s_tip = max(s_of(Vector(v.co)) for v in upper_me.vertices)
sm = bmesh.new()
top_r, bot_r = [], []
for s, e in ring:
    base = HEEL + D * float(s) + E * float(e)
    lift = lift_at(s)
    waist = 0.0
    if KIND != "trainer" and S_HEEL_FRONT + 0.004 < s < S_BALL - 0.015:
        waist = 0.004 * math.sin(math.pi * (s - S_HEEL_FRONT - 0.004) / (S_BALL - 0.019 - S_HEEL_FRONT)) ** 0.4
    ztop = FLOOR + P["cup"] - drop_at(s)
    top_r.append(sm.verts.new((base.x, base.y, ztop + lift)))
    bot_r.append(sm.verts.new((base.x, base.y, FLOOR - T + P["cup"] + lift * 0.6 + waist)))
n = len(ring)
for i_ in range(n):
    j_ = (i_ + 1) % n
    sm.faces.new((top_r[i_], top_r[j_], bot_r[j_], bot_r[i_]))
cen_se = ring.mean(axis=0)


def waist_at(s_):
    if KIND != "trainer" and S_HEEL_FRONT + 0.004 < s_ < S_BALL - 0.015:
        return 0.004 * math.sin(math.pi * (s_ - S_HEEL_FRONT - 0.004) / (S_BALL - 0.019 - S_HEEL_FRONT)) ** 0.4
    return 0.0


def cap(outer, top):
    """Inset rings towards the middle, each on the sole's own face (lifted at the toe as the edge is), then a fan."""
    rows = [outer]
    for f in (0.8, 0.55, 0.3):
        row = []
        for (s_, e_) in cen_se + (ring - cen_se) * f:
            b_ = HEEL + D * float(s_) + E * float(e_)
            z_ = (FLOOR + P["cup"] - drop_at(s_) + lift_at(s_)) if top else (FLOOR - T + P["cup"] + lift_at(s_) * 0.6 + waist_at(s_))
            row.append(sm.verts.new((b_.x, b_.y, z_)))
        rows.append(row)
    for a_, b_ in zip(rows[:-1], rows[1:]):
        for i_ in range(n):
            j_ = (i_ + 1) % n
            q = (a_[i_], a_[j_], b_[j_], b_[i_])
            sm.faces.new(q if not top else q[::-1])
    b0 = HEEL + D * float(cen_se[0]) + E * float(cen_se[1])
    z0 = (FLOOR + P["cup"] - drop_at(cen_se[0]) + lift_at(cen_se[0])) if top else (FLOOR - T + P["cup"] + lift_at(cen_se[0]) * 0.6)
    cv_ = sm.verts.new((b0.x, b0.y, z0))
    for i_ in range(n):
        j_ = (i_ + 1) % n
        t_ = (rows[-1][i_], rows[-1][j_], cv_)
        sm.faces.new(t_ if not top else t_[::-1])


cap(top_r, True)
cap(bot_r, False)
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
            if zf is None:
                # a low shoe's tongue lies on the foot, under the vamp and seen only in the opening (laid on the upper,
                # its edges stood up as fins where they crossed the collar)
                hit_, nn_ = BVH.ray_cast(HEEL + D * s + E * (ec_l + e) + Vector((0, 0, 0.4)), Vector((0, 0, -1)), 0.6)[:2]
                row.append(None if hit_ is None else hit_ + nn_ * (EASE * 0.6 - 0.001))
                continue
            q = on_top(s, ec_l + e, zf)
            row.append(None if q is None else q[0] + q[1] * 0.0012)
        if all(r_ is not None for r_ in row):
            if max(r_.z for r_ in row) > FLOOR + top_at(s) + 0.015:
                break
            tongue_rows.append(row)
    if len(tongue_rows) > 2:
        # its top edge lifted 12 mm above the collar, as a tongue stands
        top_row = [p_ + Vector((0, 0, 0.006)) - D * 0.003 for p_ in tongue_rows[-1]]
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


else:
    # AN OPEN THROAT (the third try: two reviews saw "a short flat cluster of crosses bunched under the ankle, the
    # rest of the instep bare", "no tongue or open throat", "eyelets as if printed on"). The lace opening is cut
    # through the leather from the collar's front down the instep to the throat, THROAT of the way from the heel to
    # the tip, wider at the top; the eyelets run down both edges; the tongue lies on the foot under it and stands
    # above the collar; the laces cross over the gap; on a trainer the edges are raised as an eyestay
    s_top = 0.08
    while s_top < S_BALL - 0.06:
        q = UPPER_BVH.ray_cast(HEEL + D * s_top + E * top_e(s_top) + Vector((0, 0, 0.4)), Vector((0, 0, -1)), 0.6)[0]
        if q is not None and q.z < FLOOR + top_at(s_top) - 0.004:
            break
        s_top += 0.003
    S_THROAT = P["throat"] * S_TIP
    HW_TOP, HW_THR = P["slot"]
    e_top, e_thr = top_e(s_top + 0.004), top_e(S_THROAT)

    def lace_e(s_):
        return e_top + (e_thr - e_top) * (s_ - s_top) / max(1e-6, S_THROAT - s_top)

    def slot_hw(s_):
        return HW_TOP + (HW_THR - HW_TOP) * max(0.0, min(1.0, (s_ - s_top) / max(1e-6, S_THROAT - s_top)))

    lace_rows = [(float(s_), None) for s_ in np.linspace(s_top + 0.005, S_THROAT - 0.007, n_e)]
    lace_pts = []
    for s_, _z in lace_rows:
        lace_pts.append([on_top(s_, lace_e(s_) + side * (slot_hw(s_) + P["eyelet_off"])) for side in (-1.0, 1.0)])
    # the tongue: on the foot 1.5 mm off the skin, from under the vamp in front of the throat up through the opening
    # to above the collar's front; as wide as the opening and 14 mm under each edge
    tongue_rows = []
    s_list_t = list(np.arange(S_THROAT + 0.010, s_top - 0.035, -0.006))
    for s_ in s_list_t:
        hwt = slot_hw(min(max(s_, s_top), S_THROAT)) + 0.014
        row = []
        for e in np.linspace(-hwt, hwt, 7):
            hit_, nn_ = BVH.ray_cast(HEEL + D * s_ + E * (lace_e(min(max(s_, s_top), S_THROAT)) + e) + Vector((0, 0, 0.4)),
                                     Vector((0, 0, -1)), 0.6)[:2]
            row.append(None if hit_ is None else hit_ + nn_ * 0.0010)
        if any(r_ is None for r_ in row):
            break
        if max(r_.z for r_ in row) > FLOOR + top_at(s_) + P["tongue_up"]:
            break
        tongue_rows.append(row)
    if len(tongue_rows) > 2:
        top_row = [p_ + Vector((0, 0, 0.004)) - D * 0.002 for p_ in tongue_rows[-1]]
        tongue_rows.append(top_row)
        tv_, tf_ = [], []
        w_ = len(tongue_rows[0])
        for r_ in tongue_rows:
            tv_.extend(tuple(p_) for p_ in r_)
        for i_ in range(len(tongue_rows) - 1):
            for j_ in range(w_ - 1):
                tf_.append((i_ * w_ + j_, (i_ + 1) * w_ + j_, (i_ + 1) * w_ + j_ + 1, i_ * w_ + j_ + 1))
        tm = bpy.data.meshes.new("Tongue")
        tm.from_pydata(tv_, [], tf_)
        to = bpy.data.objects.new("Tongue", tm)
        bpy.context.collection.objects.link(to)
        tm.materials.append(tailor.material("M_Upper", P["upper"], 0.5))
        sl = to.modifiers.new("Solidify", "SOLIDIFY")
        # 1.5 mm, under the leather's inner face (4 mm thick, its edges came through the upper beside the laces)
        sl.thickness, sl.offset = 0.0015, 1.0
        extras.append(to)
    # the opening cut through the upper between two upright planes along the lace line, back from the throat
    cb = bmesh.new()
    cb.from_mesh(upper_me)
    planes_ = []
    for side in (-1.0, 1.0):
        a_ = HEEL + D * (s_top - 0.03) + E * (lace_e(s_top) + side * HW_TOP)
        b_ = HEEL + D * S_THROAT + E * (lace_e(S_THROAT) + side * HW_THR)
        n_ = Vector((0, 0, 1)).cross(b_ - a_).normalized()
        planes_.append((a_, n_ if n_.dot(E) * side > 0 else -n_))    # each pointing away from the lace line
    for pc, pn in planes_ + [(HEEL + D * S_THROAT, D)]:
        bmesh.ops.bisect_plane(cb, geom=cb.verts[:] + cb.edges[:] + cb.faces[:], plane_co=pc, plane_no=pn)
    cut = []
    for f in cb.faces:
        c = f.calc_center_median()
        inside = all((c - pc).dot(pn) < 0 for pc, pn in planes_)
        if inside and s_top - 0.03 < s_of(c) < S_THROAT and c.z > FLOOR + 0.03:     # (unbounded, it opened the heel)
            cut.append(f)
    bmesh.ops.delete(cb, geom=cut, context="FACES")
    bmesh.ops.delete(cb, geom=[v for v in cb.verts if not v.link_faces], context="VERTS")
    if KIND == "trainer":
        # the eyestay: the leather within 14 mm of the opening raised 1.2 mm
        cb.normal_update()
        for v in cb.verts:
            s_ = s_of(v.co)
            if s_top - 0.01 < s_ < S_THROAT + 0.004 and v.co.z > FLOOR + 0.03:
                d_ = abs(e_of(v.co) - lace_e(min(max(s_, s_top), S_THROAT))) - slot_hw(s_)
                if -0.001 < d_ < 0.016:
                    v.co = v.co + v.normal * 0.0012 * math.sin(math.pi * min(1.0, (d_ + 0.001) / 0.017))
    cb.to_mesh(upper_me)
    cb.free()
    log["throat"] = {"fromHeelMm": round(S_THROAT * 1000), "topMm": round(s_top * 1000), "pairs": n_e}


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
        bpy.ops.mesh.primitive_torus_add(major_radius=0.0028, minor_radius=0.0009, major_segments=10, minor_segments=4,
                                         location=hit + nn * 0.0012)
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
        bpy.ops.mesh.primitive_torus_add(major_radius=0.008, minor_radius=0.0016, major_segments=14, minor_segments=5,
                                         location=c_ + E * (sg * 0.009))
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
# ---- a toe cap and a heel counter: panels of the upper itself, split along plane lines and a shade apart (as
# separate pieces 1 mm proud, their edges read as slits, slivers and cuts to the second reviewers) --------------
S_CAP = S_BALL + 0.35 * (S_TIP - S_BALL)
CN = (D + Vector((0, 0, 1.1))).normalized()
C0 = HEEL + D * 0.085 + Vector((0, 0, FLOOR - HEEL.z))
ZC = HEEL + Vector((0, 0, FLOOR - HEEL.z + P["top_back"] - 0.012))
pan_rgb = tuple(c * (0.95 if KIND == "trainer" else 0.90) for c in P["upper"])
upper_me.materials.append(tailor.material("M_Panel", pan_rgb, 0.45 if KIND != "trainer" else 0.55))
pb = bmesh.new()
pb.from_mesh(upper_me)
for pc, pn in ((HEEL + D * S_CAP, D), (C0, CN), (ZC, Vector((0, 0, 1)))):
    bmesh.ops.bisect_plane(pb, geom=pb.verts[:] + pb.edges[:] + pb.faces[:], plane_co=pc, plane_no=pn)
for f in pb.faces:
    c = f.calc_center_median()
    cap_ = s_of(c) > S_CAP
    counter = (c - C0).dot(CN) < 0 and c.z < ZC.z
    f.material_index = 1 if (cap_ or counter) else 0
pb.to_mesh(upper_me)
pb.free()
SMOOTH_ALL = set(extras)
if KIND == "trainer":
    pb = bmesh.new()
    pb.from_mesh(upper_me)
    pb.normal_update()
    for v in pb.verts:
        d_ = FLOOR + top_at(s_of(v.co)) - v.co.z
        if -0.001 < d_ < 0.016:
            v.co = v.co + v.normal * 0.0042 * math.sin(math.pi * min(1.0, (d_ + 0.003) / 0.019))
    pb.to_mesh(upper_me)
    pb.free()

sol = upper.modifiers.new("Solidify", "SOLIDIFY")
sol.thickness, sol.offset, sol.use_rim = 0.0025, -1.0, True
for o in [upper, sole] + extras:
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    for mdf in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=mdf.name)
    for m in list(o.modifiers):
        o.modifiers.remove(m)
    if o is upper:
        for p_ in o.data.polygons:
            p_.use_smooth = True
    else:
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(50))
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
    if p.z < FLOOR + top_at(max(0.0, s_of(pl))) - 0.03 and abs(e_of(pl) - ec_foot) < 0.08 and -0.01 < s_of(pl) < S_TIP:
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
