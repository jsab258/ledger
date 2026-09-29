"""A hand-knitted V-neck cardigan over a round-collared blouse, modelled close round the wearer's own body.

    blender -b -P tools/meshgen/blender/model_cardigan.py -- BODY.fbx OUT_DIR [--name sheila_cardigan]

WHY, 29 September (the clothing session, CLOTHES.md item 5; the research,
production/research/clothing-pipeline/SHEILA-CLOTHES-2026-09-29.md). Sheila's
casting sheet: "a beige hand-knitted cardigan buttoned over a cream blouse
with a small round collar"; her approved concept (production/casting/
sheila-dunn/full.jpg): a V-neck to the bust, seven buttons, set-in sleeves to
the wrist, ribbed welt at the hip and ribbed cuffs, loose enough to hang
straight. Knitwear is knitted to shape, a close stretchy layer, so the
research's route is to build it as an offset of her body rather than sew
panels (which also removes the sleeve cap that sank the jacket): the torso
and arms of her skin, set out by the knit's ease, smoothed until it spans
her hollows (between the breasts, the spine's groove, under the arm), kept
off her body; the front opened into a V and down the middle, a button band
up both fronts and round the neck, seven buttons; ribbing modelled at the
welt and cuffs (the knit stitch itself is a tiling normal map in the game).
The blouse is only what shows: its round collar, drafted by the shoulder-
overlap rule (4.5 cm wide), lying over the cardigan's neckband, and its
front inside the V. Skinned to her body in the game, no cloth simulation.
OUT_DIR gets NAME_render_static.fbx, NAME.blend, pictures and cardigan.json.
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


NAME = opt("--name", "sheila_cardigan", str)
HEM_Z = opt("--hem", 0.905)               # the welt's lower edge, at the top of the hip
EASE = opt("--ease", 0.028)               # the knit out from her body, m
V_Z = opt("--v", 1.30)                    # the V's point, level with her underarm (CARDIGAN-BUILD-2026-09-29.md)
WELT = opt("--welt", 0.05)
# A CREW-NECK JUMPER (--crew; 30 September, Ron's grey jumper, CLOTHES.md item
# 6): no V, no opening, no bands, buttons or blouse; a 28 mm ribbed neckband
# built as a clean ring round the neck (what failed on the cardigan was every
# edge cut from the skin; its body, welt and sleeves passed)
CREW = "--crew" in argv
log = {"body": BODY}


def say(*a):
    print("CARDIGAN", *a, flush=True)


arm, body = tailor.load_body(BODY, lod=opt("--lod", 1, int))
BVH = tailor.bvh_of(body)
dom = tailor.dominant_bones(body)
co = np.array([body.matrix_world @ v.co for v in body.data.vertices])
J = lambda n: np.array(tailor.joint(arm, n))
NECK_Z = float(J("neck_01")[2]) - opt("--neck-drop", 0.035)       # the back neckline, at the base of the neck
wrist = {s: (J("lowerarm_" + s), J("hand_" + s)) for s in ("l", "r")}


def keep(i):
    b, p = dom[i], co[i]
    # THE NECK AND THE HIPS TOO (the first review: a boat neck and shoulder
    # holes where the neck's skin was left out, a shirt-tail hem where the
    # hips' belong to the thighs): the thighs' skin above the hem, the neck's
    # below the neckline's cut, never the arms' hands or the head
    if b.startswith(("thigh",)):
        if p[2] < HEM_Z - 0.03 or abs(p[0]) > opt("--torso-half", 0.165) + 0.06:
            return False
    elif b.startswith(("neck",)):
        if p[2] > NECK_Z + opt("--keep-up", 0.04) - 0.01:
            return False
    elif not b.startswith(("spine_", "clavicle", "upperarm", "lowerarm", "pelvis")):
        return False
    if p[2] < HEM_Z - 0.03 or p[2] > NECK_Z + opt("--keep-up", 0.04):
        return False
    if b.startswith("lowerarm"):
        s = "l" if p[0] > 0 else "r"
        a, h = wrist[s]
        t = float(np.dot(p - a, h - a) / np.dot(h - a, h - a))
        if t > opt("--cuff-t", 0.90) + 0.06:
            return False
    return True


keep_v = np.array([keep(i) for i in range(len(co))])
bm = bmesh.new()
bm.from_mesh(body.data)
bm.transform(body.matrix_world)
bm.verts.ensure_lookup_table()
bmesh.ops.delete(bm, geom=[f for f in bm.faces if not all(keep_v[v.index] for v in f.verts)], context="FACES")
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
# the largest piece only (stray islands of skin at the edges)
bm.verts.ensure_lookup_table()
comp = {}
for v0 in bm.verts:
    if v0 in comp:
        continue
    cid = len(set(comp.values()))
    stack = [v0]
    comp[v0] = cid
    while stack:
        v = stack.pop()
        for e in v.link_edges:
            o = e.other_vert(v)
            if o not in comp:
                comp[o] = cid
                stack.append(o)
sizes = {}
for c in comp.values():
    sizes[c] = sizes.get(c, 0) + 1
main = max(sizes, key=sizes.get)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if comp[v] != main], context="VERTS")
# finer: two cuts, so the knit's surface is smooth when it spans the hollows
bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
bmesh.ops.triangulate(bm, faces=bm.faces[:])
bm.normal_update()
knit_me = bpy.data.meshes.new("Cardigan")
bm.to_mesh(knit_me)
bm.free()
knit = bpy.data.objects.new("Cardigan", knit_me)
bpy.context.collection.objects.link(knit)

# ---- out by the ease, smoothed until it spans the hollows, kept off the body ----------------------------------

x = np.array([v.co[:] for v in knit_me.vertices])
nrm = np.array([v.normal[:] for v in knit_me.vertices])
x = x + nrm * EASE
edges = np.array([e.vertices[:] for e in knit_me.edges])
deg = np.bincount(edges.ravel(), minlength=len(x)).astype(float)
bnd = np.zeros(len(x), dtype=bool)
_b = bmesh.new()
_b.from_mesh(knit_me)
for e in _b.edges:
    if e.is_boundary:
        bnd[e.verts[0].index] = bnd[e.verts[1].index] = True
_b.free()
for rnd in range(opt("--smooth-rounds", 6, int)):
    for _ in range(12):
        acc = np.zeros_like(x)
        np.add.at(acc, edges[:, 0], x[edges[:, 1]])
        np.add.at(acc, edges[:, 1], x[edges[:, 0]])
        avg = acc / np.maximum(deg, 1)[:, None]
        # the open edges held (smoothed with the rest, the top edge shrank down
        # off her shoulders into a boat neck, three tries)
        x[~bnd] = x[~bnd] * 0.5 + avg[~bnd] * 0.5
    for i in range(len(x)):
        p = Vector(x[i])
        hit, n_, _f, _d = BVH.find_nearest(p)
        if hit is not None and (p - hit).dot(n_) < EASE * 0.55:
            x[i] = hit + n_ * EASE * 0.55
for i, v in enumerate(knit_me.vertices):
    v.co = x[i]
knit_me.update()
# THE KNIT SPANS HER HOLLOWS (the first try clung like a leotard, the bust
# and every hollow modelled): each level of the torso out to its own hull,
# the arms left out of it
torso_only = [i for i in range(len(x)) if abs(x[i][0]) < opt("--torso-half", 0.165)]
_keep = knit_me.vertices
xyz = np.array([v.co[:] for v in _keep])
disp = np.zeros_like(xyz)
for z in np.arange(HEM_Z - 0.03, NECK_Z - 0.02, 0.008):
    sel = [i for i in torso_only if abs(xyz[i][2] - z) < 0.004]
    if len(sel) < 6:
        continue
    hull = tailor._hull2(xyz[sel, :2])
    if len(hull) < 3:
        continue
    for i in sel:
        q, d = tailor._to_hull(xyz[i, :2], hull)
        if 1e-4 < d < 0.05:
            disp[i, :2] = q - xyz[i, :2]
for _ in range(10):
    acc = np.zeros_like(disp)
    np.add.at(acc, edges[:, 0], disp[edges[:, 1]])
    np.add.at(acc, edges[:, 1], disp[edges[:, 0]])
    avg = acc / np.maximum(deg, 1)[:, None]
    disp = np.where((np.linalg.norm(avg, axis=1) > np.linalg.norm(disp, axis=1))[:, None], 0.5 * (disp + avg), disp)
for i, v in enumerate(_keep):
    v.co = Vector(xyz[i] + disp[i])
knit_me.update()

# HANGING STRAIGHT FROM THE BUST (the concept: a hand-knit hanging straight
# down from the bust to the welt, not pulled in at the waist): below the bust,
# round the front and sides, each point at least as far out as the knit is
# anywhere above it down from the bust
xyz = np.array([v.co[:] for v in knit_me.vertices])
t_ids = [i for i in range(len(xyz)) if abs(xyz[i][0]) < opt("--torso-half", 0.165)]
cy_t = float(np.mean(xyz[t_ids, 1]))
Z_BUST = opt("--hang-from", 1.30)          # below the bust and the shoulder blades
ang_ = np.arctan2(xyz[:, 1] - cy_t, xyz[:, 0])
rad_ = np.hypot(xyz[:, 0], xyz[:, 1] - cy_t)
bins = {}
for i in t_ids:
    if xyz[i][2] <= Z_BUST + 0.01:                                     # all round: the back from the shoulder blades
        bins.setdefault(int((ang_[i] + math.pi) // math.radians(4)), []).append(i)
hung = 0
for b_, ids in bins.items():
    ids = sorted(ids, key=lambda i: -xyz[i][2])
    run = 0.0
    for i in ids:
        run = max(run, rad_[i])
        if rad_[i] < run - 0.001:
            f_ = (run - 0.001) / rad_[i]
            xyz[i][0] *= f_
            xyz[i][1] = cy_t + (xyz[i][1] - cy_t) * f_
            hung += 1
for i, v in enumerate(knit_me.vertices):
    v.co = Vector(xyz[i])
knit_me.update()
log["hungStraight"] = {"points": hung, "bustZ": round(Z_BUST, 3)}
# and smoothed after the hang (where the hang begins it left a crinkled line across the chest), the edges held,
# kept off the body
_x = np.array([v.co[:] for v in knit_me.vertices])
for _r in range(opt("--post-smooth", 0, int)):
    acc = np.zeros_like(_x)
    np.add.at(acc, edges[:, 0], _x[edges[:, 1]])
    np.add.at(acc, edges[:, 1], _x[edges[:, 0]])
    avg = acc / np.maximum(deg, 1)[:, None]
    _x[~bnd] = _x[~bnd] * 0.5 + avg[~bnd] * 0.5
for i, v in enumerate(knit_me.vertices):
    p = Vector(_x[i])
    hit, n_, _f, _d = BVH.find_nearest(p)
    if hit is not None and (p - hit).dot(n_) < EASE * 0.55:
        p = hit + n_ * EASE * 0.55
    v.co = p
knit_me.update()

# ---- CLEAN EDGES, cut by planes after the shaping (the first try's edges followed her skin's faces: a ragged
# hem, a jagged V): a level hem, square cuffs, the back of the neckline, the V, the opening down the front ----------

FRONT_Y = float(np.median(np.array([v.co[:] for v in knit_me.vertices])[:, 1]))
NECK_SIDE = opt("--neck-side", 0.066)
NECK_NO = Vector((0.0, -0.25, 1.0)).normalized()                    # the throat lower than the back of the neck
bm = bmesh.new()
bm.from_mesh(knit_me)


def cut(plane_co, plane_no, clear, geom=None):
    g = geom if geom is not None else bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=g, plane_co=plane_co, plane_no=plane_no, clear_inner=(clear == "inner"),
                           clear_outer=(clear == "outer"))


cut((0, 0, HEM_Z), (0, 0, 1), "inner")                                 # the hem, level
for s_ in ("l", "r"):
    a_, h_ = wrist[s_]
    ax = (h_ - a_)
    cut(tuple(a_ + ax * opt("--cuff-t", 0.90)), tuple(ax / np.linalg.norm(ax)), "outer")   # the cuffs, square
# THE NECKLINE ROUND THE NECK, NOT ACROSS IT (a flat cut at the neck's base
# took the tops of her shoulders and left a boat neck, two tries): the knit
# is taken away within NECK_R of the neck's axis above the shoulders' slope
NECK_R = opt("--neck-r", 0.064)
_ns = tailor.section_loops(body, (0.0, 0.0, NECK_Z + 0.02), (0, 0, 1))
_ns = np.concatenate(_ns) if _ns else np.zeros((0, 3))
_ns = _ns[np.abs(_ns[:, 0]) < 0.09]
NECK_AX = Vector((0.0, float(_ns[:, 1].mean()) if len(_ns) else float(J("neck_01")[1]), 0.0))
cut((0, 0, NECK_Z + opt("--top-cut", 0.03)), (0, 0, 1), "outer")       # nothing above the neck's base
# a crew neck dips at the front towards the collarbones (Ron's first review:
# level all round it read as a mock turtleneck): --neck-dip lowers the cut at
# the front, fading to nothing at the sides
DIP = opt("--neck-dip", 0.0)


def _neck_cut(c):
    fr = max(0.0, (NECK_AX.y - c.y) / max(1e-6, NECK_R))
    return c.z > NECK_Z - 0.035 - DIP * fr * fr and math.hypot(c.x - NECK_AX.x, c.y - NECK_AX.y) < NECK_R + DIP * 0.3 * fr


if CREW:
    # THE CREW NECK STOPS AT THE NECK'S BASE (Ron's second try: cut round a
    # radius, the knit climbed the slope of his thick neck into a tube): all
    # the knit above the base, level at the back and sides, dipping at the
    # front; the band then lies on the slope and leans in to hug the neck
    Z_NB = opt("--neck-top", 1.665)

    def _neck_cut(c):  # noqa: F811
        a_ = math.atan2(c.x - NECK_AX.x, -(c.y - NECK_AX.y))
        fr = max(0.0, math.cos(a_))
        return c.z > Z_NB - DIP * fr * fr
bmesh.ops.delete(bm, geom=[f for f in bm.faces if _neck_cut(f.calc_center_median())], context="FACES")
log["neck"] = {"axisY": round(NECK_AX.y, 3), "r": NECK_R, "neckZ": round(NECK_Z, 3)}
# the V, on the front only, each side's plane through its line
Zn = NECK_Z - 0.25 * 0.07
for sgn in (() if CREW else (1.0, -1.0)):
    # the V's planes only below the neck (running on above it they ate the front of her shoulders)
    front = [f for f in bm.faces if f.calc_center_median().y < FRONT_Y and f.calc_center_median().x * sgn >= 0
             and f.calc_center_median().z < Zn + 0.004]
    geom = list({v for f in front for v in f.verts}) + list({e for f in front for e in f.edges}) + front
    n_ = Vector((sgn * (Zn - V_Z), 0.0, -NECK_SIDE))
    nf0 = len(bm.faces)
    cut((0.0, 0.0, V_Z), tuple(n_.normalized()), "inner", geom)
    log.setdefault("vFacesRemoved", []).append(nf0 - len(bm.faces))
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
seam = []
if not CREW:
    # the opening down the middle: cut at x = 0 on the front, then parted there
    front = [f for f in bm.faces if f.calc_center_median().y < FRONT_Y]
    geom = list({v for f in front for v in f.verts}) + list({e for f in front for e in f.edges}) + front
    res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0), plane_no=(1, 0, 0))
    seam = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge) and not e.is_boundary]
    if seam:
        bmesh.ops.split_edges(bm, edges=seam)
bm.to_mesh(knit_me)
bm.free()
knit_me.update()
log["cut"] = {"frontParted": len(seam)}

# ---- ribbing at the welt and the cuffs ---------------------------------------------------------------------------

# THE WELT AND CUFFS AS SHAPES (the first review: 'no ribbed welt and no
# ribbed cuffs as shapes'): the welt's 5 cm drawn in 8 mm towards the hip and
# ribbed 1.8 mm deep every 7 mm round; each cuff's last 6 cm drawn in 6 mm to
# the wrist and ribbed the same
mid_y = float(np.mean(np.array([v.co[:] for v in knit_me.vertices])[:, 1]))
girth_r = 0.17
for v in knit_me.vertices:
    p = Vector(v.co)
    d = 0.0
    if p.z < HEM_Z + WELT:
        f = 1.0 - (p.z - HEM_Z) / WELT
        a = math.atan2(p.y - mid_y, p.x)
        n_rib = int(2 * math.pi * girth_r / 0.007)
        d = -0.008 * min(1.0, f * 1.6) + 0.0018 * math.cos(a * n_rib) * min(1.0, f * 4)
    for s_ in ("l", "r"):
        a_, h_ = wrist[s_]
        if (p.x > 0) == (s_ == "l") and abs(p.x) > 0.25:
            L_ = float(np.linalg.norm(h_ - a_))
            t = float(np.dot(np.array(p) - a_, h_ - a_) / (L_ * L_))
            c0 = opt("--cuff-t", 0.90) - 0.06 / L_
            if t > c0:
                ax = (h_ - a_) / L_
                rel = np.array(p) - a_
                radial = rel - ax * np.dot(rel, ax)
                ang = math.atan2(radial[2], radial[1])
                f = min(1.0, (t - c0) * L_ / 0.02)
                d = -0.006 * f + 0.0015 * math.cos(ang * 18) * f
    if d:
        hit, n_, _f, _d = BVH.find_nearest(p)
        out = (p - hit).normalized() if hit is not None and (p - hit).length > 1e-6 else Vector((0, 0, 0))
        dist = (p - hit).length if hit is not None else 0.0
        d = max(d, -(dist - 0.004))                                   # never onto her skin
        v.co = p + out * d
knit_me.update()

# ---- the button band: up both fronts and round the back of the neck -------------------------------------------

knit_col = tuple(float(c) for c in opt("--rgb", "0.60,0.52,0.42", str).split(","))
knitm = tailor.material("M_KnitBeige", knit_col, 0.95)
blousem = tailor.material("M_BlouseCream", (0.86, 0.81, 0.69), 0.6)
buttonm = tailor.material("M_ButtonBrown", (0.30, 0.20, 0.12), 0.4)
knit_me.materials.append(knitm)
KNIT_BVH = tailor.bvh_of(knit)                                     # the knit's own surface, for the band's side and the collar
# THE BAND FROM ITS KNOWN LINES (the walks along the mesh's edge mixed the
# edges up, four tries): straight up each front at the middle, up each side
# of the V, round the back of the neck, each point laid on the knit


def strip(name, rows, mat, thickness):
    verts, faces = [], []
    w = len(rows[0])
    for r_ in rows:
        verts.extend(tuple(p) for p in r_)
    for i in range(len(rows) - 1):
        for j in range(w - 1):
            faces.append((i * w + j, i * w + j + 1, (i + 1) * w + j + 1, (i + 1) * w + j))
    m = bpy.data.meshes.new(name)
    m.from_pydata(verts, [], faces)
    m.validate()
    o = bpy.data.objects.new(name, m)
    bpy.context.collection.objects.link(o)
    m.materials.append(mat)
    for p in m.polygons:
        p.use_smooth = True
    s_ = o.modifiers.new("Solidify", "SOLIDIFY")
    s_.thickness, s_.offset = thickness, -1.0
    return o


def on_knit_from_front(x_, z_):
    """The knit's front surface at (x, z) (a ray from in front, the front half only: along the V's edge a ray
    passed through the opening and put the band on her back)."""
    hit, n_, _i, _d = KNIT_BVH.ray_cast(Vector((x_, -0.6, z_)), Vector((0, 1, 0)), 1.2)
    return hit if hit is not None and hit.y < FRONT_Y else None


def on_knit_near(p):
    hit, n_, _i, _d = KNIT_BVH.find_nearest(p)
    return hit


def band_along(pts, side_dirs, name="Band"):
    """A band 29 mm wide along points on the knit: 20 mm onto the fabric side, 9 mm beyond the edge, 2.5 mm
    proud of the knit."""
    pts = np.array([tuple(p) for p in pts])
    for _ in range(4):
        pts[1:-1] = 0.5 * pts[1:-1] + 0.25 * (pts[:-2] + pts[2:])
    inn, outn = [], []
    for p, sd in zip(pts, side_dirs):
        p = Vector(p)
        hb, nb, _f, _d = BVH.find_nearest(p)
        nrm_ = (p - hb).normalized() if hb is not None and (p - hb).length > 1e-6 else Vector((0, -1, 0))
        sd = Vector(sd)
        sd = (sd - nrm_ * sd.dot(nrm_)).normalized()
        lift = nrm_ * 0.0025
        inn.append(p + sd * 0.020 + lift)
        outn.append(p - sd * 0.009 + lift)
    return strip(name, [outn, [a.lerp(b, 0.5) for a, b in zip(outn, inn)], inn], knitm, 0.003), inn, outn


if not CREW:
    extras = []
    Zn = NECK_Z - 0.25 * 0.07
    # ONE BAND (the first review: planks up the V, no back-neck band, a step at
    # the V's foot): a single line from the left front's hem up to the V's point,
    # up the V's left side, round the back of the neck, down the right side and
    # the right front to its hem, each part's fabric side given, smoothed through
    # the joins
    path, sides, parts = [], [], []


    def add(pts, sd, part):
        for q in pts:
            if q is not None:
                path.append(q)
                sides.append(sd)
                parts.append(part)


    for sgn, order in ((1.0, 1), (-1.0, -1)):
        front = [on_knit_from_front(sgn * 0.004, z_) for z_ in np.linspace(HEM_Z + 0.004, V_Z, 26)]
        vside = [on_knit_from_front(sgn * (0.004 + (NECK_SIDE - 0.004) * t_ + 0.008), V_Z + (Zn - V_Z) * t_)
                 for t_ in np.linspace(0.0, 1.0, 22)[1:]]
        seg_f = [(q, (sgn, 0, 0), "front") for q in front]
        seg_v = [(q, (sgn * (Zn - V_Z), 0.0, -NECK_SIDE), "v") for q in vside]
        if sgn > 0:
            LEFT_PART = seg_f + seg_v
        else:
            RIGHT_PART = list(reversed(seg_f + seg_v))
    # the back of the neck: the knit's edge there (its boundary points above the shoulders, behind the front)
    # THE BACK OF THE BAND ALONG A SMOOTH CIRCLE ROUND HER NECK (the second
    # review: the knit's own ragged edge made 'a wavy, frayed double lip'): from
    # where the V's lines reach it, round the back, each point dropped onto the knit
    R_B = opt("--band-r", 0.068)
    a0 = math.asin(min(0.99, NECK_SIDE / R_B))
    BACK_PART = []
    for a_ in np.linspace(a0, 2 * math.pi - a0, 60):
        x_, y_ = NECK_AX.x + R_B * math.sin(a_), NECK_AX.y - R_B * math.cos(a_)
        hit = KNIT_BVH.ray_cast(Vector((x_, y_, NECK_Z + 0.08)), Vector((0, 0, -1)), 0.3)[0]
        if hit is not None:
            BACK_PART.append((hit, (math.sin(a_), -math.cos(a_), -1.0), "back"))
    for q, sd, part in LEFT_PART + BACK_PART + RIGHT_PART:
        if q is not None:
            path.append(q)
            sides.append(sd)
            parts.append(part)
    band_left_pts = []
    if len(path) > 8:
        # resampled evenly along the path, then made
        P_ = np.array([tuple(q) for q in path])
        d_ = np.linalg.norm(np.diff(P_, axis=0), axis=1)
        s_ = np.concatenate([[0.0], np.cumsum(d_)])
        t_ = np.arange(0.0, s_[-1], 0.006)
        Pr = np.column_stack([np.interp(t_, s_, P_[:, k]) for k in range(3)])
        Sr = np.array([sides[min(int(np.searchsorted(s_, tt)), len(sides) - 1)] for tt in t_], dtype=float)
        for _ in range(6):                                                  # the fabric side turns smoothly at the joins
            Sr[1:-1] = 0.5 * Sr[1:-1] + 0.25 * (Sr[:-2] + Sr[2:])
        Pr = [on_knit_near(Vector(q)) or Vector(q) for q in Pr]
        o_, inn, outn = band_along(Pr, [tuple(v) for v in Sr])
        extras.append(o_)
        band_left_pts = [(a, b) for a, b in zip(inn, outn) if (a.x + b.x) > 0 and a.z < V_Z - 0.01]
    log["band"] = {"left": len(band_left_pts)}

    # ---- seven buttons on the left front band, from just under the V to above the welt ----------------------------

    left = band_left_pts
    if left:
        zs = np.linspace(V_Z - 0.012, HEM_Z + 0.015 + 0.006, 7)       # the top one marks the V, the first 1.5 cm over the hem
        for z_ in zs:
            k = int(np.argmin([abs(0.5 * (a.z + b.z) - z_) for a, b in left]))
            a, b = left[k]
            c = a.lerp(b, 0.45)
            hit, n_, _f, _d = BVH.find_nearest(c)
            n_ = (c - hit).normalized() if hit is not None and (c - hit).length > 1e-6 else Vector((0, -1, 0))
            bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.0075, depth=0.003, location=c + n_ * 0.0025)
            btn = bpy.context.active_object
            btn.rotation_mode = "QUATERNION"
            btn.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(n_)
            btn.data.materials.append(buttonm)
            extras.append(btn)
        log["buttons"] = len(zs)

    # ---- the blouse: a flat panel across the V with its placket and buttons, then its round collar over all ----------
    #
    # (CARDIGAN-BUILD-2026-09-29.md, after two reviews: the blouse copied from
    # her chest clung to the cleavage and read as bare skin; the collar, five ways,
    # never lay flat.) The panel spans each level's chest hull, 5 mm out, a little
    # wider than the V; a 25 mm placket down the middle, 1.5 mm proud, two buttons.
    # The collar is drafted flat, 55 mm wide, its neckline a circle at the base of
    # her neck, its ends rounded and meeting at the throat, and laid from above
    # on whatever is beneath it (the band and knit at the back and shoulders, the
    # panel at the front), 3 mm clear.
    blouse_rows = []
    for z_ in np.arange(V_Z - 0.035, Zn + 0.012, 0.005):
        loops = tailor.section_loops(body, (0, 0, float(z_)), (0, 0, 1))
        pts2 = np.concatenate(loops)[:, :2] if loops else np.zeros((0, 2))
        pts2 = pts2[np.abs(pts2[:, 0]) < 0.16]
        if len(pts2) < 3:
            continue
        hull = np.array(tailor._hull2(pts2))
        wv = 0.004 + (NECK_SIDE - 0.004) * max(0.0, min(1.0, (z_ - V_Z) / max(1e-6, Zn - V_Z))) + 0.025
        row = []
        for x_ in np.linspace(-wv, wv, 25):
            # the hull's front at x_
            best = None
            for k in range(len(hull)):
                p0, p1 = hull[k], hull[(k + 1) % len(hull)]
                if (p0[0] - x_) * (p1[0] - x_) <= 0 and abs(p1[0] - p0[0]) > 1e-9:
                    yy = p0[1] + (p1[1] - p0[1]) * (x_ - p0[0]) / (p1[0] - p0[0])
                    best = yy if best is None else min(best, yy)
            if best is None:
                best = float(hull[:, 1].min())
            row.append(Vector((float(x_), best - 0.005, float(z_))))
        blouse_rows.append(row)
    if len(blouse_rows) > 2:
        extras.append(strip("BlouseFront", blouse_rows, blousem, 0.0012))
        # the placket: a 25 mm strip down the middle, 1.5 mm proud
        plk = []
        for row in blouse_rows:
            mid = len(row) // 2
            c_ = row[mid]
            plk.append([c_ + Vector((dx, -0.0015, 0.0)) for dx in (-0.0125, 0.0, 0.0125)])
        extras.append(strip("Placket", plk, blousem, 0.0012))
        for z_b in (Zn - 0.018, Zn - 0.018 - 0.085):
            k = int(np.argmin([abs(r[0].z - z_b) for r in blouse_rows]))
            c_ = blouse_rows[k][len(blouse_rows[k]) // 2] + Vector((0, -0.003, 0))
            bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=0.0052, depth=0.002, location=c_, rotation=(math.pi / 2, 0, 0))
            b_ = bpy.context.active_object
            b_.data.materials.append(tailor.material("M_BlouseButton", (0.92, 0.90, 0.84), 0.3))
            extras.append(b_)
    # the collar: laid on everything made so far, and on her
    _cb = bmesh.new()
    for o_ in [knit] + [e for e in extras if e.type == "MESH"]:
        _dg = bpy.context.evaluated_depsgraph_get()
        _m = bpy.data.meshes.new_from_object(o_.evaluated_get(_dg))
        _m.transform(o_.matrix_world)
        _cb.from_mesh(_m)
        bpy.data.meshes.remove(_m)
    UNDER = BVHTree.FromBMesh(_cb)
    _cb.free()


    def laid(x_, y_):
        """Dropped from just above the neck's base (from higher, the ray began inside her neck) onto the band,
        knit or blouse beneath, or her where there is none."""
        top = Vector((x_, y_, NECK_Z + 0.03))
        if tailor.depth_inside(BVH, top) > 0.0:
            return None
        hu = UNDER.ray_cast(top, Vector((0, 0, -1)), 0.3)[0]
        hb = BVH.ray_cast(top, Vector((0, 0, -1)), 0.3)[0]
        hits = [h for h in (hu, hb) if h is not None]
        return max(hits, key=lambda h: h.z) + Vector((0, 0, 0.003)) if hits else None


    COLLAR = opt("--collar", 0.055)
    R_IN = NECK_R - opt("--collar-in", 0.004)
    rows_c = []
    for f_ in np.linspace(0.0, 1.0, 7):
        row = []
        for a_ in np.linspace(math.radians(8), math.radians(352), 90):   # a_ = 0 at the throat: the two ends meet there
            # the ends rounded: within 35 mm of the throat the collar narrows on a quarter circle
            d_front = min(a_, 2 * math.pi - a_) * R_IN
            w_ = COLLAR if d_front > 0.035 else COLLAR * math.sqrt(max(0.0, 1.0 - ((0.035 - d_front) / 0.035) ** 2))
            r_ = R_IN + w_ * f_
            x_, y_ = NECK_AX.x + r_ * math.sin(a_), NECK_AX.y - r_ * math.cos(a_)
            q = laid(x_, y_)
            row.append(q)
        rows_c.append(row)
    # a point that found nothing takes its neighbour's height
    for row in rows_c:
        for k in range(len(row)):
            if row[k] is None:
                near_ = next((row[j] for j in sorted(range(len(row)), key=lambda j: abs(j - k)) if row[j] is not None), None)
                a_k = math.radians(8) + (math.radians(344)) * k / (len(row) - 1)
                row[k] = Vector((NECK_AX.x + R_IN * math.sin(a_k), NECK_AX.y - R_IN * math.cos(a_k), near_.z if near_ else NECK_Z))
    for r_ in rows_c:
        _o = np.array([tuple(p) for p in r_])
        for _ in range(4):
            _o[1:-1] = 0.5 * _o[1:-1] + 0.25 * (_o[:-2] + _o[2:])
        r_[:] = [Vector(p) for p in _o]
    extras.append(strip("Collar", rows_c, blousem, 0.002))
    log["blouse"] = {"panelRows": len(blouse_rows), "collarMm": COLLAR * 1000}
else:
    # the crew neck's band: a ribbed ring from the knit's neck edge up to hug the neck, 28 mm, rising
    extras = []
    NB = opt("--neckband", 0.028)
    # ANCHORED TO THE KNIT'S OWN NECK EDGE (placed by the neck's radius, the band
    # sat low on the wide base of a thick neck and flared out under the knit):
    # the edge's points round the neck, by angle, smoothed; the band stands up
    # from them, leaning a little in, over the edge
    _bk = bmesh.new()
    _bk.from_mesh(knit_me)
    _ep = [v.co.copy() for v in _bk.verts if v.is_boundary and v.co.z > NECK_Z - 0.08
           and math.hypot(v.co.x - NECK_AX.x, v.co.y - NECK_AX.y) < opt("--edge-r", NECK_R + 0.03)]
    _bk.free()
    _ang = np.array([math.atan2(q.x - NECK_AX.x, -(q.y - NECK_AX.y)) for q in _ep])
    _rad = np.array([math.hypot(q.x - NECK_AX.x, q.y - NECK_AX.y) for q in _ep])
    _zz = np.array([q.z for q in _ep])
    order_ = np.argsort(_ang)
    _ang, _rad, _zz = _ang[order_], _rad[order_], _zz[order_]
    grid_a = np.linspace(-math.pi, math.pi, 97)[:-1]                     # a closed ring: no seam at the back
    ext_a = np.concatenate([_ang - 2 * math.pi, _ang, _ang + 2 * math.pi])
    r_edge = np.interp(grid_a, ext_a, np.tile(_rad, 3))
    z_edge = np.interp(grid_a, ext_a, np.tile(_zz, 3))
    for _ in range(opt("--band-smooth", 24, int)):                     # round the ring (the rim had come out wavy)
        r_edge = 0.5 * r_edge + 0.25 * (np.roll(r_edge, 1) + np.roll(r_edge, -1))
        z_edge = 0.5 * z_edge + 0.25 * (np.roll(z_edge, 1) + np.roll(z_edge, -1))
    rows_n = []
    for r_i in range(7):
        h = NB * r_i / 6
        row = []
        for k in range(len(grid_a) + 1):
            a_ = grid_a[k % len(grid_a)]
            k = k % len(grid_a)
            d_ = Vector((math.sin(a_), -math.cos(a_), 0.0))
            # from the knit's edge (its foot a little under it) in a straight line to 5 mm off the neck, NB up
            foot_r, foot_z = r_edge[k] + opt("--foot-out", 0.012), z_edge[k] - opt("--foot-down", 0.010)   # well over the cut edge
            top_z = foot_z + NB * opt("--band-rise", 0.7)
            hn = BVH.ray_cast(Vector((NECK_AX.x, NECK_AX.y, top_z)), d_, 0.25)[0]
            top_r = ((hn - Vector((NECK_AX.x, NECK_AX.y, top_z))).length + 0.005) if hn is not None else foot_r - 0.01
            top_r = min(top_r, foot_r)
            t_ = r_i / 6
            r_ = foot_r + (top_r - foot_r) * t_
            # arched, so it clears the knit's cut edge it passes over (straight, the edge showed through it as
            # a sawtooth) and stands up round the neck rather than lying flat
            z_ = foot_z + (top_z - foot_z) * t_ + opt("--band-arch", 0.007) * math.sin(math.pi * min(1.0, t_ * 1.3))
            rib = 0.0011 * math.cos(a_ * 48) * (0.4 + 0.6 * t_)
            row.append(Vector((NECK_AX.x, NECK_AX.y, z_)) + d_ * (r_ + rib))
        rows_n.append(row)
    nb_obj = strip("Neckband", rows_n, knitm, 0.003)
    _nb = bmesh.new()
    _nb.from_mesh(nb_obj.data)
    bmesh.ops.remove_doubles(_nb, verts=_nb.verts[:], dist=1e-5)       # the ring's ends one seam-free piece
    _nb.to_mesh(nb_obj.data)
    _nb.free()
    extras.append(nb_obj)
    _all = [q for r_ in rows_n for q in r_]
    log["neckband"] = {"mm": NB * 1000, "zRange": [round(min(q.z for q in _all), 3), round(max(q.z for q in _all), 3)],
                       "rFoot": round(float(np.mean([(q - Vector((NECK_AX.x, NECK_AX.y, q.z))).length for q in rows_n[0]])), 3),
                       "rTop": round(float(np.mean([(q - Vector((NECK_AX.x, NECK_AX.y, q.z))).length for q in rows_n[-1]])), 3)}

# ---- THE WELT AND CUFFS AS FINE RIBBED RINGS OVER THE KNIT (the second try's
# ribs, cut into the knit's own points, were too coarse to show) -------------------------------------------------


def ring_band(name, centre_of, axis_of, rows, around, depth_out, rib_every, radius_guess, skip=None):
    """Rows of points round an axis, each put on the knit by a ray from outside towards the axis, set out
    `depth_out` and ribbed; returned as a strip object."""
    grid = []
    for r_i in range(rows):
        row = []
        c_, ax_ = centre_of(r_i), axis_of(r_i)
        u_ = ax_.orthogonal().normalized()
        w_ = ax_.cross(u_).normalized()
        for k in range(around + 1):
            a_ = 2 * math.pi * k / around
            d_ = (u_ * math.cos(a_) + w_ * math.sin(a_))
            hit, n_, _i, _dd = KNIT_BVH.ray_cast(c_ + d_ * (radius_guess + 0.15), -d_, radius_guess + 0.15)
            if hit is None:
                row.append(None)
                continue
            rib = 0.0011 * math.cos(2 * math.pi * k / max(1, around) * (2 * math.pi * radius_guess / rib_every))
            row.append(hit + d_ * (depth_out + rib))
        grid.append(row)
    # drop columns that missed anywhere, or fall in the skipped (the front opening) span
    keep_cols = [k for k in range(around + 1) if all(grid[r][k] is not None for r in range(rows))
                 and (skip is None or not skip(grid[0][k]))]
    if len(keep_cols) < 4:
        return None
    rows_pts = [[grid[r][k] for k in keep_cols] for r in range(rows)]
    return strip(name, rows_pts, knitm, 0.002)


mid_c = Vector((0.0, mid_y, 0.0))
welt = ring_band("Welt", lambda r: Vector((0.0, mid_y, HEM_Z + 0.002 + (WELT - 0.002) * r / 5)), lambda r: Vector((0, 0, 1)),
                 6, 256, 0.0025, 0.007, 0.20, skip=lambda q: q is None or (q.y < FRONT_Y and abs(q.x) < 0.012))
if welt:
    extras.append(welt)
# SNUG CUFFS (the second review: 'the sleeve ends flare open with a thin,
# ragged rim'): each a ribbed tube 5 cm long round the wrist, 8 mm clear of it,
# the sleeve's last 10 cm drawn in to meet it and ending 5 mm over it
WRIST_R = opt("--wrist-r", 0.026) + 0.008
for s_ in ("l", "r"):
    a_, h_ = (Vector(tuple(wrist[s_][0])), Vector(tuple(wrist[s_][1])))
    ax_ = (h_ - a_).normalized()
    L_ = (h_ - a_).length
    t1 = opt("--cuff-t", 0.90) * L_
    # the sleeve drawn in
    for v in knit_me.vertices:
        p = Vector(v.co)
        if (p.x > 0) != (s_ == "l") or abs(p.x) < 0.2:
            continue
        rel = p - a_
        t = rel.dot(ax_)
        radial = rel - ax_ * t
        if t1 - 0.10 < t <= t1 + 0.01 and radial.length < 0.07:            # the sleeve only (not her hip beside it)
            f = min(1.0, (t - (t1 - 0.10)) / 0.10)
            r_now = radial.length
            r_to = r_now + (WRIST_R + 0.003 - r_now) * f
            if radial.length > 1e-6:
                v.co = a_ + ax_ * t + radial.normalized() * r_to
    u_ = ax_.orthogonal().normalized()
    w_ = ax_.cross(u_).normalized()
    rows_k = []
    for r_i in range(6):
        c_ = a_ + ax_ * (t1 - 0.045 + 0.05 * r_i / 5)
        row = []
        for k in range(49):
            ang = 2 * math.pi * k / 48
            rib = 0.0012 * math.cos(ang * 16)
            row.append(c_ + (u_ * math.cos(ang) + w_ * math.sin(ang)) * (WRIST_R + rib))
        rows_k.append(row)
    extras.append(strip("Cuff", rows_k, knitm, 0.003))
knit_me.update()
log["ribbed"] = {"welt": bool(welt)}

# ---- the render mesh -------------------------------------------------------------------------------------------

rb = bmesh.new()
rb.from_mesh(knit_me)
bmesh.ops.recalc_face_normals(rb, faces=rb.faces[:])
rb.normal_update()
vote = 0.0
for f in list(rb.faces)[::9]:
    c = f.calc_center_median()
    hit, _n, _i, _d = BVH.find_nearest(c)
    if hit is not None:
        vote += f.normal.dot(c - hit)
if vote < 0:
    bmesh.ops.reverse_faces(rb, faces=rb.faces[:])
rb.to_mesh(knit_me)
rb.free()
for p in knit_me.polygons:
    p.use_smooth = True
s_ = knit.modifiers.new("Solidify", "SOLIDIFY")
s_.thickness, s_.offset = opt("--knit", 0.004), -1.0
for o in [knit] + extras:
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    for mdf in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=mdf.name)
bpy.ops.object.select_all(action="DESELECT")
for o in [knit] + extras:
    o.select_set(True)
bpy.context.view_layer.objects.active = knit
bpy.ops.object.join()
render = bpy.context.active_object
render.name = "CardiganRender"
log["render"] = {"verts": len(render.data.vertices), "tris": sum(len(p.vertices) - 2 for p in render.data.polygons)}
say("render", log["render"])
bpy.ops.object.select_all(action="DESELECT")
render.select_set(True)
bpy.context.view_layer.objects.active = render
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, "%s_render_static.fbx" % NAME), use_selection=True,
                         object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
# her skirt beside it for the pictures, if made
SKIRT = opt("--skirt", "", str)
if SKIRT and os.path.exists(SKIRT):
    bpy.ops.import_scene.fbx(filepath=SKIRT)
grey = tailor.material("M_Body", (0.5, 0.5, 0.5))
body.data.materials.clear()
body.data.materials.append(grey)
MID = Vector((0.0, FRONT_Y, 1.10))
tailor.pictures(os.path.join(OUT, "cardigan"), MID,
                views=(("front", (0, -3.0, 0.1)), ("side", (3.0, 0, 0.1)), ("back", (0, 3.0, 0.1)), ("three-quarter", (2.1, -2.2, 0.3))))
tailor.pictures(os.path.join(OUT, "cardigan-close"), Vector((0.0, FRONT_Y, 1.25)),
                views=(("front", (0, -1.3, 0.05)), ("three-quarter", (0.9, -1.0, 0.12)), ("back", (0, 1.3, 0.05))))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "cardigan.json"), "w"), indent=1)
say("done", json.dumps(log))
