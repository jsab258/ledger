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
V_Z = opt("--v", 1.25)                    # the V's point at the centre front (the concept: at the first button, mid-chest)
WELT = opt("--welt", 0.05)
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
        if p[2] > NECK_Z + 0.03:
            return False
    elif not b.startswith(("spine_", "clavicle", "upperarm", "lowerarm", "pelvis")):
        return False
    if p[2] < HEM_Z - 0.03 or p[2] > NECK_Z + 0.04:
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

# ---- CLEAN EDGES, cut by planes after the shaping (the first try's edges followed her skin's faces: a ragged
# hem, a jagged V): a level hem, square cuffs, the back of the neckline, the V, the opening down the front ----------

FRONT_Y = float(np.median(np.array([v.co[:] for v in knit_me.vertices])[:, 1]))
NECK_SIDE = opt("--neck-side", 0.072)
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
cut((0, 0, NECK_Z + 0.03), (0, 0, 1), "outer")                           # nothing above the neck's base
bmesh.ops.delete(bm, geom=[f for f in bm.faces
                           if f.calc_center_median().z > NECK_Z - 0.035
                           and math.hypot(f.calc_center_median().x - NECK_AX.x, f.calc_center_median().y - NECK_AX.y) < NECK_R],
                 context="FACES")
log["neck"] = {"axisY": round(NECK_AX.y, 3), "r": NECK_R}
# the V, on the front only, each side's plane through its line
Zn = NECK_Z - 0.25 * 0.07
for sgn in (1.0, -1.0):
    # the V's planes only below the neck (running on above it they ate the front of her shoulders)
    front = [f for f in bm.faces if f.calc_center_median().y < FRONT_Y and f.calc_center_median().x * sgn >= 0
             and f.calc_center_median().z < Zn + 0.004]
    geom = list({v for f in front for v in f.verts}) + list({e for f in front for e in f.edges}) + front
    n_ = Vector((sgn * (Zn - V_Z), 0.0, -NECK_SIDE))
    nf0 = len(bm.faces)
    cut((0.0, 0.0, V_Z), tuple(n_.normalized()), "inner", geom)
    log.setdefault("vFacesRemoved", []).append(nf0 - len(bm.faces))
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
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
_bk = bmesh.new()
_bk.from_mesh(knit_me)
_bpts = [v.co.copy() for v in _bk.verts if v.is_boundary and v.co.z > NECK_Z - 0.06 and v.co.y > FRONT_Y - 0.03]
_bk.free()
BACK_PART = []
if len(_bpts) > 3:
    _bpts.sort(key=lambda q: -math.atan2(q.x, q.y - FRONT_Y))        # from her left round to her right
    BACK_PART = [(q, (0.0, 0.0, -1.0), "back") for q in _bpts]
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
    zs = np.linspace(V_Z - 0.025, HEM_Z + WELT + 0.02, 7)
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

# ---- the blouse: its round collar over the neckband, and its front inside the V ------------------------------

# THE COLLAR LAID ON BY PROJECTION (the first review: 'a flat, jagged white
# strip ... notched flaps at the back, a split'): the neck's base as a ring
# just above the knit's neckline, evenly spaced and smoothed; each point's
# outer edge straight out and down from it by the collar's width, then put on
# the knit (on the band, 4 mm above) or, in the V, on her; the outer line
# smoothed; the ends rounded at the throat, where the two halves meet
# the collar's neckline a circle just inside the knit's own, on her (a section
# through the body at the neck's base took in her shoulders: a band out to
# the shoulder points, like a sailor's collar)
ring = []
for a_ in np.linspace(-math.pi, math.pi, 141)[:-1]:
    x_ = NECK_AX.x + (NECK_R - opt("--collar-in", 0.006)) * math.sin(a_)
    y_ = NECK_AX.y - (NECK_R - opt("--collar-in", 0.006)) * math.cos(a_)     # a_ = 0 at the throat
    hit, _n, _i, _d = BVH.ray_cast(Vector((x_, y_, NECK_Z + 0.045)), Vector((0, 0, -1)), 0.2)
    z_ = hit.z if hit is not None else NECK_Z
    ring.append((x_, y_, z_))
ring = np.array(ring)
cm_ = np.array([NECK_AX.x, NECK_AX.y, float(ring[:, 2].mean())])
for _ in range(6):
    ring[1:-1] = 0.5 * ring[1:-1] + 0.25 * (ring[:-2] + ring[2:])
COLLAR = opt("--collar", 0.045)
inner, outer = [], []
for p in ring:
    p = Vector(p)
    away = Vector((p.x - cm_[0], p.y - cm_[1], 0.0)).normalized()
    q = p + away * 0.004
    front_d = abs(math.atan2(p.x - cm_[0], -(p.y - cm_[1])))            # 0 at the throat
    d_cf = front_d * 0.055                                                # about the arc from the front, m
    w = COLLAR if d_cf > 0.035 else COLLAR * math.sqrt(max(0.0, 1.0 - ((0.035 - d_cf) / 0.035) ** 2))
    r_ = q + (away * 0.75 + Vector((0, 0, -0.66))).normalized() * max(w, 0.002)
    hk, nk, _fk, dk = KNIT_BVH.find_nearest(r_)
    hb, nb, _fb, db = BVH.find_nearest(r_)
    if hk is not None and dk < 0.04 and hb is not None and (hk - hb).length > 1e-6:
        r_ = hk + (hk - hb).normalized() * 0.0065                        # over the knit and its band
    elif hb is not None:
        r_ = hb + (r_ - hb).normalized() * 0.006 if (r_ - hb).length > 1e-6 else hb + nb * 0.006
    inner.append(q)
    outer.append(r_)
_o = np.array([tuple(p) for p in outer])
for _ in range(12):
    _o[1:-1] = 0.5 * _o[1:-1] + 0.25 * (_o[:-2] + _o[2:])
outer = [Vector(p) for p in _o]
# every row on top of the knit (with only the outer edge laid on it, the rest
# of the collar lay under the knit and showed as a thin line)


def on_top(p):
    """Dropped straight down onto whatever lies beneath, the knit or her, and lifted clear of it (found by
    the nearest point, the rows looped at the back)."""
    top = p + Vector((0, 0, 0.06))
    hk = KNIT_BVH.ray_cast(top, Vector((0, 0, -1)), 0.12)[0]
    hb = BVH.ray_cast(top, Vector((0, 0, -1)), 0.12)[0]
    zs = [h.z + (0.0065 if h is hk else 0.005) for h in (hk, hb) if h is not None]
    return Vector((p.x, p.y, max(zs))) if zs else p


raw_outer = []
for q, p in zip(inner, ring):
    away = Vector((q.x - cm_[0], q.y - cm_[1], 0.0)).normalized()
    front_d = abs(math.atan2(q.x - cm_[0], -(q.y - cm_[1])))
    d_cf = front_d * 0.055
    w = COLLAR if d_cf > 0.035 else COLLAR * math.sqrt(max(0.0, 1.0 - ((0.035 - d_cf) / 0.035) ** 2))
    raw_outer.append(q + away * max(w, 0.002))
rows_c = [[on_top(a.lerp(b, f_)) for a, b in zip(inner, raw_outer)] for f_ in (0.0, 0.33, 0.66, 1.0)]
for r_ in rows_c[1:]:
    _o = np.array([tuple(p) for p in r_])
    for _ in range(6):
        _o[1:-1] = 0.5 * _o[1:-1] + 0.25 * (_o[:-2] + _o[2:])
    r_[:] = [Vector(p) for p in _o]
# ONLY THE COLLAR'S FRONT, TWO ROUNDED POINTS AT THE THROAT (the whole collar
# round the neck failed five ways here: a line, a sailor's band, strips up the
# neck, loops at the back; under a buttoned cardigan a round collar shows
# mostly as its two points either side of the throat, as in her concept):
# each a rounded lobe 5 cm across and 4 cm down from the neck's base, laid
# from the front on whatever lies beneath it, 5 mm proud
throat = Vector(tuple(ring[int(np.argmin(np.abs(np.arctan2(ring[:, 0] - cm_[0], -(ring[:, 1] - cm_[1])))))]))
LOBE_W, LOBE_H, ROUND = opt("--lobe-w", 0.05), opt("--lobe-h", 0.04), opt("--lobe-round", 0.03)
for sgn in (1.0, -1.0):
    rows_l = []
    for vj in np.linspace(0.0, 1.0, 9):
        row = []
        for ui in np.linspace(0.0, 1.0, 11):
            u_, v_ = ui * LOBE_W, vj * LOBE_H
            # the outer lower corner rounded: pull points outside the rounded corner back onto it
            cu, cv = LOBE_W - ROUND, LOBE_H - ROUND
            if u_ > cu and v_ > cv:
                du, dv = u_ - cu, v_ - cv
                r_ = math.hypot(du, dv)
                if r_ > ROUND:
                    u_, v_ = cu + du * ROUND / r_, cv + dv * ROUND / r_
            x_ = throat.x + sgn * (0.002 + u_)
            z_ = throat.z + 0.004 + u_ * 0.35 - v_                        # rising a little towards the shoulder
            start = Vector((x_, -0.5, z_))
            hk = KNIT_BVH.ray_cast(start, Vector((0, 1, 0)), 1.0)[0]
            hb = BVH.ray_cast(start, Vector((0, 1, 0)), 1.0)[0]
            hits = [(h.y - (0.0065 if h is hk else 0.004), h) for h in (hk, hb) if h is not None]
            y_ = min(hits)[0] if hits else throat.y - 0.01
            row.append(Vector((x_, y_, z_)))
        rows_l.append(row)
    extras.append(strip("CollarPoint", rows_l, blousem, 0.0015))
log["collar"] = "the two front points"
# the blouse front in the V: her chest there, set out a little, cream
bmf = bmesh.new()
bmf.from_mesh(body.data)
bmf.transform(body.matrix_world)


def inside(c):
    return (c.y < FRONT_Y and V_Z - 0.035 < c.z < NECK_Z
            and abs(c.x) < NECK_SIDE * (c.z - V_Z) / max(1e-6, NECK_Z - V_Z) + 0.03)


bmesh.ops.delete(bmf, geom=[f for f in bmf.faces if not inside(f.calc_center_median())], context="FACES")
bmesh.ops.delete(bmf, geom=[v for v in bmf.verts if not v.link_faces], context="VERTS")
bmf.normal_update()
for v in bmf.verts:
    v.co = v.co + v.normal * 0.005
bf_me = bpy.data.meshes.new("BlouseFront")
bmf.to_mesh(bf_me)
bmf.free()
bf = bpy.data.objects.new("BlouseFront", bf_me)
bpy.context.collection.objects.link(bf)
bf_me.materials.append(blousem)
for p in bf_me.polygons:
    p.use_smooth = True
extras.append(bf)

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
for s_ in ("l", "r"):
    a_, h_ = (Vector(tuple(wrist[s_][0])), Vector(tuple(wrist[s_][1])))
    ax_ = (h_ - a_).normalized()
    L_ = (h_ - a_).length
    t1 = opt("--cuff-t", 0.90) * L_
    cuff = ring_band("Cuff", lambda r, a_=a_, ax_=ax_, t1=t1: a_ + ax_ * (t1 - 0.055 + 0.057 * r / 5), lambda r, ax_=ax_: ax_,
                     6, 64, 0.0022, 0.006, 0.045)
    if cuff:
        extras.append(cuff)
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
