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
# A ZIP JACKET (--zip; 30 September, Darren's shell-suit jacket): the V as the
# open zip, closed below it with a zip line; the band only up the V and round
# the neck, as a collar (--band-in wide); no buttons; the panel in the V a
# white T-shirt with no collar; --panels paints the raglan shoulders and upper
# sleeves a second colour
ZIP = "--zip" in argv
log = {"body": BODY}


def say(*a):
    print("CARDIGAN", *a, flush=True)


arm, body = tailor.load_body(BODY, lod=opt("--lod", 1, int))
BVH = tailor.bvh_of(body)
dom = tailor.dominant_bones(body)
co = np.array([body.matrix_world @ v.co for v in body.data.vertices])
J = lambda n: np.array(tailor.joint(arm, n))
NECK_Z = float(J("neck_01")[2]) - opt("--neck-drop", 0.035)       # the back neckline, at the base of the neck
SHORT = "--short-sleeve" in argv
wrist = ({s: (J("upperarm_" + s), J("lowerarm_" + s)) for s in ("l", "r")} if SHORT
         else {s: (J("lowerarm_" + s), J("hand_" + s)) for s in ("l", "r")})


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
    if SHORT and (b.startswith("lowerarm") or b.startswith("hand")):
        return False
    if b.startswith("lowerarm") or (SHORT and b.startswith("upperarm")):
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


TUBE_Z = opt("--tube-from", 0.0)
cut((0, 0, max(HEM_Z, TUBE_Z)), (0, 0, 1), "inner")                    # the hem, level
if TUBE_Z > HEM_Z:
    # A COAT'S SKIRT (a donkey jacket to below the crotch, 30 September: modelled from the skin, its lower part
    # wrapped each leg like shorts): the shell cut level above the crotch, then its edge carried straight down in
    # rows to the hem, each point out to the hull of the body's whole slice there (both legs) plus the ease, and
    # never further in than the row above: a straight tube
    def slice_hull_r(z_, cen_, dirs):
        loops_ = tailor.section_loops(body, Vector((0, 0, z_)), Vector((0, 0, 1)))
        pts_ = np.concatenate(loops_)[:, :2] if loops_ else np.zeros((0, 2))
        pts_ = pts_[np.abs(pts_[:, 0]) < 0.35]
        if len(pts_) < 3:
            return [0.0] * len(dirs)
        h_ = np.array(tailor._hull2(pts_))
        out = []
        for d_ in dirs:
            best = 0.0
            for i_ in range(len(h_)):
                q0, q1 = h_[i_], h_[(i_ + 1) % len(h_)]
                ed = q1 - q0
                den = d_[0] * (-ed[1]) + d_[1] * ed[0]
                if abs(den) < 1e-12:
                    continue
                w_ = q0 - cen_
                t_ = (w_[0] * (-ed[1]) + w_[1] * ed[0]) / den
                u_ = (d_[0] * w_[1] - d_[1] * w_[0]) / den
                if t_ > 0 and -1e-9 <= u_ <= 1 + 1e-9:
                    best = max(best, t_)
            out.append(best)
        return out

    bm.verts.ensure_lookup_table()
    edge_e = [e for e in bm.edges if e.is_boundary and all(v.co.z < TUBE_Z + 0.004 for v in e.verts)]
    loop_v = list({v for e in edge_e for v in e.verts})
    cen_t = np.array([float(np.mean([v.co.x for v in loop_v])), float(np.mean([v.co.y for v in loop_v]))])
    dirs_t = {v: (np.array([v.co.x, v.co.y]) - cen_t) for v in loop_v}
    rad_t = {v: float(np.linalg.norm(d_)) for v, d_ in dirs_t.items()}
    dirs_t = {v: d_ / max(1e-9, np.linalg.norm(d_)) for v, d_ in dirs_t.items()}
    # the join's loop evened round (cut through the shell's uneven faces it zigzagged, and every row below and
    # the seam across the jacket kept the zigzag): radii smoothed in order of angle, the loop's points moved to them
    _ord = sorted(loop_v, key=lambda v: math.atan2(dirs_t[v][1], dirs_t[v][0]))
    _rr = np.array([rad_t[v] for v in _ord])
    for _ in range(opt("--tube-loop-smooth", 12, int)):
        _rr = 0.5 * _rr + 0.25 * (np.roll(_rr, 1) + np.roll(_rr, -1))
    for v, r_ in zip(_ord, _rr):
        rad_t[v] = float(r_)
        v.co = Vector((cen_t[0] + dirs_t[v][0] * r_, cen_t[1] + dirs_t[v][1] * r_, v.co.z))
    n_rows = max(2, int(round((TUBE_Z - HEM_Z) / 0.02)))
    cur_e = edge_e
    cur_map = {v: v for v in loop_v}
    for r_ in range(1, n_rows + 1):
        z_r = TUBE_Z - (TUBE_Z - HEM_Z) * r_ / n_rows
        res = bmesh.ops.extrude_edge_only(bm, edges=cur_e)
        new_v = [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]
        new_e = [g for g in res["geom"] if isinstance(g, bmesh.types.BMEdge) and all(v in new_v for v in g.verts)]
        # each new point pairs with the old edge point it came from (nearest in plan)
        olds = list(cur_map.keys())
        old_xy = np.array([[cur_map[o].co.x, cur_map[o].co.y] for o in olds])
        hull_r = None
        next_map = {}
        for nv in new_v:
            k_ = int(np.argmin(np.sum((old_xy - np.array([nv.co.x, nv.co.y])) ** 2, axis=1)))
            next_map[olds[k_]] = nv
        dl = [dirs_t[o] for o in olds]
        hr = slice_hull_r(z_r, cen_t, dl)
        for i_, o in enumerate(olds):
            nv = next_map.get(o)
            if nv is None:
                continue
            r_new = max(rad_t[o], hr[i_] + EASE)
            rad_t[o] = r_new
            nv.co = Vector((cen_t[0] + dirs_t[o][0] * r_new, cen_t[1] + dirs_t[o][1] * r_new, z_r))
        cur_map = {o: next_map[o] for o in olds if o in next_map}
        cur_e = new_e
    # its loop closed where the shell's edge had a gap (at the back it opened as a slit up the tube): the two
    # open ends' columns joined by faces all the way down
    tv_ = [v for v in bm.verts if v.co.z < TUBE_Z + 0.003 and v.is_boundary]
    bmesh.ops.remove_doubles(bm, verts=tv_, dist=opt("--tube-weld", 0.018))
    open_e = [e for e in bm.edges if e.is_boundary and all(v.co.z < TUBE_Z - 0.001 for v in e.verts)
              and abs(e.verts[0].co.z - e.verts[1].co.z) > 0.005]
    if open_e:
        try:
            bmesh.ops.bridge_loops(bm, edges=open_e)
        except Exception:
            pass
    # the join above the tube eased up the jacket over 12 cm (the tube's straight fall met the moulded shell at a
    # step, and whatever was laid across it, the pockets, broke there)
    cen3 = Vector((cen_t[0], cen_t[1], 0.0))
    for _ in range(opt("--tube-ease", 10, int)):
        new_ = {}
        for v in bm.verts:
            if TUBE_Z - 0.06 < v.co.z < TUBE_Z + 0.12 and not v.is_boundary:
                nb_ = [e.other_vert(v).co for e in v.link_edges]
                c_ = sum(nb_, Vector()) / len(nb_)
                w_ = 0.5 * (1.0 - abs(v.co.z - TUBE_Z) / (0.12 if v.co.z > TUBE_Z else 0.06))
                new_[v] = v.co.lerp(c_, w_)
        for v, c_ in new_.items():
            v.co = c_
    log["tube"] = {"fromZ": TUBE_Z, "rows": n_rows, "bridged": len(open_e)}
for s_ in ("l", "r"):
    a_, h_ = wrist[s_]
    ax = (h_ - a_)
    if SHORT:
        # the sleeve alone: points within 9 cm of the upper arm's axis and past a quarter of its length
        axn = ax / np.linalg.norm(ax)
        sel_v = set()
        for v in bm.verts:
            rel = np.array(v.co) - np.array(a_)
            t_ = float(np.dot(rel, axn))
            if (v.co.x > 0) == (s_ == "l") and t_ > 0.25 * np.linalg.norm(ax) and np.linalg.norm(rel - axn * t_) < 0.12:
                sel_v.add(v)
        geom_ = list(sel_v) + list({e for v in sel_v for e in v.link_edges if all(u in sel_v for u in e.verts)}) + \
            list({f for v in sel_v for f in v.link_faces if all(u in sel_v for u in f.verts)})
        cut(tuple(a_ + ax * opt("--cuff-t", 0.90)), tuple(axn), "outer", geom=geom_)
        continue
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


if CREW or ZIP:
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
if not CREW and not ZIP:
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

# ---- TRIMS GROWN FROM THE GARMENT'S OWN EDGES (--extrude-trims; SHELLSUIT-EDGES-2026-09-30.md, after the
# jacket's second review: every trim laid on a cut edge tore at its ends or came away from the body) -----------
#
# The shell's open edges are cleaned (short edges collapsed, slivers dissolved)
# and snapped to clean lines: the hem level, each cuff square to its arm, each
# side of the V straight, the neckline smoothed round the neck. Then each trim
# is extruded from its edge, sharing its points: the waistband down from the hem
# and drawn in, turned inside; each cuff along the arm and drawn in to the
# wrist; the collar up from the neckline, leaning in, its front ends standing
# straight up from the top of the V (the zip's top tucks into it); the zip's
# tapes a few millimetres out from each side of the V. One mesh; the render
# step's Solidify closes every edge with a rim.
EXTRUDE = "--extrude-trims" in argv
if EXTRUDE:
    Zn_x = NECK_Z - 0.25 * 0.07
    mid_y_shell = float(np.mean(np.array([v.co[:] for v in knit_me.vertices])[:, 1]))
    bm = bmesh.new()
    bm.from_mesh(knit_me)
    for _ in range(4):
        short = [e for e in bm.edges if e.is_boundary and e.calc_length() < opt("--min-edge", 0.005)]
        if not short:
            break
        bmesh.ops.collapse(bm, edges=short)
    bmesh.ops.dissolve_degenerate(bm, dist=0.0008, edges=bm.edges[:])
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bm.verts.ensure_lookup_table()

    def border_loops():
        seen, loops_ = set(), []
        for v0 in bm.verts:
            if v0 in seen or not v0.is_boundary:
                continue
            line = [v0]
            seen.add(v0)
            cur, prev = v0, None
            while True:
                nxt = [e.other_vert(cur) for e in cur.link_edges if e.is_boundary and e.other_vert(cur) is not prev]
                nxt = [n for n in nxt if n not in seen]
                if not nxt:
                    break
                prev, cur = cur, nxt[0]
                seen.add(cur)
                line.append(cur)
            if len(line) > 6:
                loops_.append(line)
        return loops_

    loops = border_loops()
    roles = {}
    for lp in loops:
        cz = sum(v.co.z for v in lp) / len(lp)
        cx = sum(v.co.x for v in lp) / len(lp)
        if cz < HEM_Z + 0.03:
            roles["hem"] = lp
        elif cx > 0.25:
            roles["cuff_l"] = lp
        elif cx < -0.25:
            roles["cuff_r"] = lp
        else:
            roles["opening"] = lp
    log["borders"] = {k: len(v) for k, v in roles.items()}

    def smooth_loop(lp, rounds, fixed=()):
        n = len(lp)
        for _ in range(rounds):
            new = []
            for i in range(n):
                if lp[i] in fixed:
                    new.append(lp[i].co.copy())
                    continue
                a, b = lp[(i - 1) % n], lp[(i + 1) % n]
                new.append(lp[i].co * 0.5 + (a.co + b.co) * 0.25)
            for v, c in zip(lp, new):
                v.co = c

    # the hem level, then smooth round
    if "hem" in roles:
        for v in roles["hem"]:
            v.co.z = HEM_Z
        smooth_loop(roles["hem"], 6)
        for v in roles["hem"]:
            v.co.z = HEM_Z
    # the cuffs square to the arm
    for sd in ("l", "r"):
        lp = roles.get("cuff_" + sd)
        if not lp:
            continue
        a_, h_ = (Vector(tuple(wrist[sd][0])), Vector(tuple(wrist[sd][1])))
        ax_ = (h_ - a_).normalized()
        c_ = a_ + (h_ - a_) * opt("--cuff-t", 0.90)
        for v in lp:
            v.co = v.co - ax_ * (v.co - c_).dot(ax_)
        smooth_loop(lp, 6)
    # the opening: each side of the V straight, the neckline smooth round the neck; the V's point fixed
    op = roles.get("opening")
    if op:
        vpt = min(op, key=lambda v: v.co.z)
        i0 = op.index(vpt)
        op = op[i0:] + op[:i0]                   # from the V's point: one side up, the neckline, the other side down
        for v in op:
            if v is vpt:
                continue
            p = v.co
            on_v = p.y < NECK_AX.y and p.z < Zn_x - 0.003
            if on_v:
                sg = 1.0 if p.x >= 0 else -1.0
                t_ = max(0.0, min(1.0, (p.z - V_Z) / max(1e-6, Zn_x - V_Z)))
                v.co.x = sg * (0.004 + (NECK_SIDE - 0.004) * t_)
        smooth_loop(op, 4, fixed=(vpt,))
        # the neckline part: radius and height smoothed by angle round the neck
        neck_pts = [v for v in op if not (v.co.y < NECK_AX.y and v.co.z < Zn_x - 0.003)]
        if len(neck_pts) > 6:
            smooth_loop(neck_pts, 12, fixed=(neck_pts[0], neck_pts[-1]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.normal_update()

    TRIM = bm.faces.layers.int.get("trim") or bm.faces.layers.int.new("trim")

    def extrude_loop(edges, move, rows=1, tag=0):
        """Extrude border edges `rows` times; move(vert_new, orig_co, row_index) places each new point; the new faces
        are tagged `tag` in the face layer "trim" (1 collar, 2 zip tape, 3 waistband, 4 cuff). Returns the new rows'
        points."""
        out_rows = []
        cur_edges = edges
        for r in range(rows):
            res = bmesh.ops.extrude_edge_only(bm, edges=cur_edges)
            for f_ in res["geom"]:
                if isinstance(f_, bmesh.types.BMFace):
                    f_[TRIM] = tag
            new_verts = [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]
            new_edges = [e for e in res["geom"] if isinstance(e, bmesh.types.BMEdge)
                         and all(v in set(new_verts) for v in e.verts)]
            for v in new_verts:
                move(v, v.co.copy(), r)
            out_rows.append(new_verts)
            cur_edges = new_edges
        return out_rows

    def loop_edges(lp):
        s = set(lp)
        return [e for e in bm.edges if e.is_boundary and e.verts[0] in s and e.verts[1] in s]

    # the waistband: 2 rows down WELT, drawn in, ribbed; then turned 1.5 cm inside
    cxy = Vector((0.0, mid_y_shell, 0.0))
    if "hem" in roles:
        WI = opt("--welt-in", 0.02)
        n_rib = int(2 * math.pi * 0.17 / 0.007)

        def mv_band(v, c, r):
            d = Vector((c.x - cxy.x, c.y - cxy.y, 0.0))
            L_ = d.length
            if r < 2:
                f = (r + 1) / 2
                a = math.atan2(c.y - cxy.y, c.x)
                rib = 0.0016 * math.cos(a * n_rib) if r == 1 else 0.0
                v.co = Vector((c.x, c.y, HEM_Z - WELT * f)) - (d / max(L_, 1e-6)) * (WI * (0.7 if r == 0 else 0.3) - rib)
            else:
                v.co = Vector((c.x, c.y, c.z + 0.015)) - (d / max(L_, 1e-6)) * 0.004
        if not CREW:                                      # (a T-shirt's hem: the ring band below, not a jacket's grown band)
            extrude_loop(loop_edges(roles["hem"]), mv_band, rows=3, tag=3)
    # the sleeves drawn in over their last 10 cm to meet the cuffs (before the cuffs grow from them)
    for sd in ("l", "r"):
        a_, h_ = (Vector(tuple(wrist[sd][0])), Vector(tuple(wrist[sd][1])))
        ax_ = (h_ - a_).normalized()
        t1 = opt("--cuff-t", 0.90) * (h_ - a_).length
        WR0 = opt("--wrist-r", 0.026) + 0.011
        for v in bm.verts:
            p = v.co
            if (p.x > 0) != (sd == "l") or abs(p.x) < 0.2:
                continue
            rel = p - a_
            t = rel.dot(ax_)
            radial = rel - ax_ * t
            if t1 - 0.10 < t <= t1 + 0.002 and radial.length < 0.08:
                f = min(1.0, (t - (t1 - 0.10)) / 0.10) ** 1.5
                v.co = a_ + ax_ * t + radial.normalized() * (radial.length + (WR0 - radial.length) * f)
    # the cuffs: 2 rows along the arm 5 cm, drawn in to the wrist, ribbed; turned inside
    for sd in ("l", "r"):
        lp = roles.get("cuff_" + sd)
        if not lp:
            continue
        a_, h_ = (Vector(tuple(wrist[sd][0])), Vector(tuple(wrist[sd][1])))
        ax_ = (h_ - a_).normalized()
        WR = opt("--wrist-r", 0.026) + 0.008

        def mv_cuff(v, c, r, a_=a_, ax_=ax_, WR=WR):
            rel = c - a_
            t = rel.dot(ax_)
            radial = rel - ax_ * t
            u_ = radial.normalized() if radial.length > 1e-6 else Vector((0, 0, 1))
            if r < 2:
                f = (r + 1) / 2
                w_ = ax_.cross(u_)
                ang = math.atan2(radial.dot(w_), radial.dot(ax_.orthogonal().normalized()))
                rr = radial.length + (WR - radial.length) * min(1.0, f * 1.4)
                rib = 0.0012 * math.cos(ang * 18) if r == 1 else 0.0
                v.co = a_ + ax_ * (t + 0.025) + u_ * (rr + rib)
            else:
                v.co = a_ + ax_ * (t - 0.015) + u_ * (radial.length - 0.003)
        extrude_loop(loop_edges(lp), mv_cuff, rows=3, tag=4)
    # the collar: up from the neckline, leaning in; the zip tapes out from each side of the V (a pullover's neck
    # has its own band: grown here too, a T-shirt's neck stood up as a turtleneck)
    if op and not CREW:
        neck_set = set(v for v in op if not (v.co.y < NECK_AX.y and v.co.z < Zn_x - 0.003))
        v_set = set(op) - neck_set
        # the corners (where V meets neckline) belong to both
        corners = [v for v in neck_set if any(e.other_vert(v) in v_set for e in v.link_edges if e.is_boundary)]
        CH = opt("--collar-h", 0.045)

        def mv_collar(v, c, r):
            d = Vector((c.x - NECK_AX.x, c.y - NECK_AX.y, 0.0))
            rad = d.length
            hn = BVH.ray_cast(Vector((NECK_AX.x, NECK_AX.y, c.z + CH * (r + 1) / 3)), d.normalized(), 0.25)[0]
            r_neck = ((hn - Vector((NECK_AX.x, NECK_AX.y, hn.z))).length + 0.007) if hn is not None else rad - 0.01
            f = (r + 1) / 3
            r_new = rad + (min(rad, r_neck) - rad) * min(1.0, f * 1.2)
            v.co = Vector((NECK_AX.x, NECK_AX.y, c.z + CH / 3)) + d.normalized() * r_new
        ne = [e for e in bm.edges if e.is_boundary and e.verts[0] in neck_set and e.verts[1] in neck_set]
        extrude_loop(ne, mv_collar, rows=3, tag=1)
        TAPE = opt("--tape", 0.006)

        def mv_tape(v, c, r):
            sg = 1.0 if c.x >= 0 else -1.0
            v.co = c + Vector((-sg * TAPE, -0.001, 0.0))
        ve = [e for e in bm.edges if e.is_boundary and (e.verts[0] in v_set or e.verts[1] in v_set)
              and e.verts[0] in set(op) and e.verts[1] in set(op) and not (e.verts[0] in neck_set and e.verts[1] in neck_set)]
        extrude_loop(ve, mv_tape, rows=1, tag=2)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(knit_me)
    bm.free()
    knit_me.update()
    log["extruded"] = True

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
    if p.z < HEM_Z + WELT and not EXTRUDE:
        f = 1.0 - (p.z - HEM_Z) / WELT
        a = math.atan2(p.y - mid_y, p.x)
        n_rib = int(2 * math.pi * girth_r / 0.007)
        d = -opt("--welt-in", 0.008) * min(1.0, f * 1.6) + 0.0018 * opt("--rib", 1.0) * math.cos(a * n_rib) * min(1.0, f * 4)
    elif (HEM_Z if EXTRUDE else -9.0) < p.z < (HEM_Z if EXTRUDE else HEM_Z + WELT) + opt("--blouse-h", 0.0) and abs(p.x) < opt("--torso-half", 0.165) + 0.02:
        # A BLOUSON (Darren's first review: 'a straight tube, the band as wide as
        # the body'): the body just above the band puffs out, most 4 cm above it
        u_ = (p.z - HEM_Z - (0.0 if EXTRUDE else WELT)) / opt("--blouse-h", 0.12)
        d = opt("--blouse", 0.0) * math.sin(math.pi * min(1.0, u_ * 1.6)) ** 0.7 * (1.0 - u_) ** 0.5
    for s_ in ("l", "r"):
        a_, h_ = wrist[s_]
        if (p.x > 0) == (s_ == "l") and abs(p.x) > 0.25 and not EXTRUDE:
            L_ = float(np.linalg.norm(h_ - a_))
            t = float(np.dot(np.array(p) - a_, h_ - a_) / (L_ * L_))
            c0 = opt("--cuff-t", 0.90) - 0.06 / L_
            if t > c0:
                ax = (h_ - a_) / L_
                rel = np.array(p) - a_
                radial = rel - ax * np.dot(rel, ax)
                ang = math.atan2(radial[2], radial[1])
                f = min(1.0, (t - c0) * L_ / 0.02)
                # (--cuff-in 0 --rib 0: a T-shirt's plain sleeve hem, not a knitted cuff)
                d = -opt("--cuff-in", 0.006) * f + 0.0015 * opt("--rib", 1.0) * math.cos(ang * 18) * f
    if d:
        hit, n_, _f, _d = BVH.find_nearest(p)
        out = (p - hit).normalized() if hit is not None and (p - hit).length > 1e-6 else Vector((0, 0, 0))
        dist = (p - hit).length if hit is not None else 0.0
        d = max(d, -(dist - 0.004))                                   # never onto her skin
        v.co = p + out * d
knit_me.update()
if opt("--armpit-clear", 0.0):
    _ab = bmesh.new()
    _ab.from_mesh(knit_me)
    _ab.verts.ensure_lookup_table()
    AR_ = opt("--armpit-r", 0.12)
    centres = []
    for sd in ("l", "r"):
        sh_ = Vector(tuple(tailor.joint(arm, "upperarm_" + sd)))
        centres.append(Vector((sh_.x * 1.0, NECK_AX.y, opt("--armpit-z", sh_.z - 0.07))))
    wts = {}
    for v in _ab.verts:
        d_ = min((v.co - c_).length for c_ in centres)
        if d_ < AR_ and not v.is_boundary:
            wts[v] = (1.0 - d_ / AR_) ** 0.8
    for _ in range(opt("--armpit-rounds", 40, int)):
        new_ = {}
        for v, w_ in wts.items():
            nb_ = [e.other_vert(v).co for e in v.link_edges]
            new_[v] = v.co.lerp(sum(nb_, Vector()) / len(nb_), 0.5 * w_)
        for v, c_ in new_.items():
            v.co = c_
        for v in wts:
            hit, nn, _f, _d = BVH.find_nearest(v.co)
            if hit is not None and (v.co - hit).dot(nn) < opt("--armpit-clear", 0.0):
                v.co = hit + nn * opt("--armpit-clear", 0.0)
    _ab.to_mesh(knit_me)
    _ab.free()
    knit_me.update()
    log["armpitCleared"] = len(wts)
if opt("--bridge", 0.0):
    # STIFF CLOTH SPANS THE BODY'S HOLLOWS (a melton jacket, 30 September: the shell moulded his pectorals): each
    # level of the torso (the sleeves left out) out to its own hull, at most --bridge, the moves eased over the cloth
    kx = np.array([v.co[:] for v in knit_me.vertices])
    disp = np.zeros_like(kx)
    TH_ = opt("--torso-half", 0.165) + 0.03
    for z_ in np.arange(HEM_Z, NECK_Z - 0.05, 0.008):
        sel = np.where((np.abs(kx[:, 2] - z_) < 0.004) & (np.abs(kx[:, 0]) < TH_))[0]
        if len(sel) < 8:
            continue
        hull_ = tailor._hull2(kx[sel, :2])
        if len(hull_) < 3:
            continue
        for i_ in sel:
            q_, d_ = tailor._to_hull(kx[i_, :2], hull_)
            if 1e-4 < d_ <= opt("--bridge", 0.0):
                disp[i_, :2] = q_ - kx[i_, :2]
    edges_k = np.array([e.vertices[:] for e in knit_me.edges])
    deg_k = np.bincount(edges_k.ravel(), minlength=len(kx)).astype(float)
    mag0 = np.linalg.norm(disp, axis=1)
    for _ in range(16):
        acc = np.zeros_like(disp)
        np.add.at(acc, edges_k[:, 0], disp[edges_k[:, 1]])
        np.add.at(acc, edges_k[:, 1], disp[edges_k[:, 0]])
        avg = acc / np.maximum(deg_k, 1)[:, None]
        grow = np.linalg.norm(avg, axis=1) > np.linalg.norm(disp, axis=1)
        disp = np.where(grow[:, None] | (mag0[:, None] < 1e-6), 0.5 * (disp + avg), disp)
    for i_, v in enumerate(knit_me.vertices):
        v.co = Vector(tuple(kx[i_] + disp[i_]))
    knit_me.update()
    log["bridged"] = {"moved": int((np.linalg.norm(disp, axis=1) > 0.001).sum()), "mostMm": round(float(np.linalg.norm(disp, axis=1).max()) * 1000, 1)}
if opt("--tuck", 0.0):
    # TUCKED IN (a blouse under her skirt: the band and the blouse's foot met and patched through each other): the
    # lowest 5 cm drawn in towards her, up to --tuck, never nearer her than 2 mm
    for v in knit_me.vertices:
        p = Vector(v.co)
        TH = opt("--tuck-h", 0.05)                          # (a blouse: only the part inside the band, so it puffs above)
        if p.z < HEM_Z + TH:
            f = 1.0 - (p.z - HEM_Z) / TH
            f = f * f * (3 - 2 * f)
            hit, n_, _f, _d = BVH.find_nearest(p)
            if hit is not None:
                dist = (p - hit).dot(n_)
                v.co = p - n_ * max(0.0, min(opt("--tuck", 0.0) * f, dist - opt("--tuck-clear", 0.002)))
    knit_me.update()
if opt("--hem-smooth", 0, int):
    # the hem's edge eased along itself, level (a T-shirt's plain hem showed its every wobble as a wavy edge)
    hb = bmesh.new()
    hb.from_mesh(knit_me)
    edge_v = [v for v in hb.verts if v.is_boundary and v.co.z < HEM_Z + 0.006]
    z_edge = float(np.median([v.co.z for v in edge_v])) if edge_v else HEM_Z     # its own level (a grown band's is lower)
    _hc = sum((v.co for v in edge_v), Vector()) / max(1, len(edge_v))
    _r0 = {v: math.hypot(v.co.x - _hc.x, v.co.y - _hc.y) for v in edge_v}
    for _ in range(opt("--hem-smooth", 0, int)):
        new = {}
        for v in edge_v:
            nb = [e.other_vert(v) for e in v.link_edges if e.is_boundary]
            if len(nb) == 2:
                c_ = v.co * 0.5 + (nb[0].co + nb[1].co) * 0.25
                new[v] = Vector((c_.x, c_.y, z_edge))
        for v, c_ in new.items():
            v.co = c_
    if "--hem-keep-r" in argv:
        # each point back out to its own distance from the hem's middle (smoothing drew the loop in: a coat's
        # hem rolled under like an anorak's)
        _rs = sorted(_r0.values())
        for v in edge_v:
            dxy = Vector((v.co.x - _hc.x, v.co.y - _hc.y, 0.0))
            if dxy.length > 1e-6:
                r_t = _r0[v]
                p_ = Vector((_hc.x, _hc.y, 0.0)) + dxy.normalized() * r_t
                v.co = Vector((p_.x, p_.y, v.co.z))
    hb.to_mesh(knit_me)
    hb.free()
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
        inn.append(p + sd * opt("--band-in", 0.020) + lift)
        outn.append(p - sd * opt("--band-out", 0.009) + lift)
    return strip(name, [outn, [a.lerp(b, 0.5) for a, b in zip(outn, inn)], inn], knitm, 0.003), inn, outn


def flat_collar(extras_, W, gap_m):
    """A flat round collar: from the top of the neckline's band, rolled over 6 mm, then lying on the blouse 2.5 mm
    off it, walked outward over its surface in 5 mm steps (so it follows shoulder and chest alike), W wide; open at
    the throat by gap_m either side of the middle, each end rounded as a circle of radius W."""
    _bk = bmesh.new()
    _bk.from_mesh(knit_me)
    _ep = [v.co.copy() for v in _bk.verts if v.is_boundary and v.co.z > NECK_Z - 0.08
           and math.hypot(v.co.x - NECK_AX.x, v.co.y - NECK_AX.y) < opt("--edge-r", NECK_R + 0.03)]
    _bk.free()
    _ang = np.array([math.atan2(q.x - NECK_AX.x, -(q.y - NECK_AX.y)) for q in _ep])
    _rad = np.array([math.hypot(q.x - NECK_AX.x, q.y - NECK_AX.y) for q in _ep])
    _zz = np.array([q.z for q in _ep])
    o_ = np.argsort(_ang)
    _ang, _rad, _zz = _ang[o_], _rad[o_], _zz[o_]
    ext_a = np.concatenate([_ang - 2 * math.pi, _ang, _ang + 2 * math.pi])
    r0 = float(np.median(_rad))
    gap = gap_m / max(0.03, r0)
    grid_a = np.linspace(gap, 2 * math.pi - gap, 90)
    r_edge = np.interp(np.where(grid_a > math.pi, grid_a - 2 * math.pi, grid_a), ext_a, np.tile(_rad, 3))
    z_edge = np.interp(np.where(grid_a > math.pi, grid_a - 2 * math.pi, grid_a), ext_a, np.tile(_zz, 3))
    for _ in range(24):
        r_edge = 0.5 * r_edge + 0.25 * (np.roll(r_edge, 1) + np.roll(r_edge, -1))
        z_edge = 0.5 * z_edge + 0.25 * (np.roll(z_edge, 1) + np.roll(z_edge, -1))
    NB = opt("--neckband", 0.012)
    arc = (grid_a - gap) * r0                                 # metres along the neckline from the left end
    arc_len = float(arc[-1])
    rows = [[] for _ in range(10)]
    for k, a_ in enumerate(grid_a):
        d_ = Vector((math.sin(a_), -math.cos(a_), 0.0))
        u = min(arc[k], arc_len - arc[k])                     # distance from the nearer end
        if opt("--collar-point", 0.0):
            # POINTED ENDS: the fall grows towards each end to --collar-point times its width at the very front
            w_here = W * (1.0 + (opt("--collar-point", 0.0) - 1.0) * max(0.0, 1.0 - u / (2.5 * W)) ** 2)
        else:
            w_here = W * math.sqrt(max(0.0, 1.0 - (1.0 - min(1.0, u / W)) ** 2)) if u < W else W
        w_here = max(w_here, 0.004)
        top = Vector((NECK_AX.x, NECK_AX.y, z_edge[k] + NB * 0.7)) + d_ * (r_edge[k] + 0.004)
        # the roll over the band, then the blouse's own surface outward from the neckline, found by rays straight
        # down (walked over the surface from the edge, the collar kept snapping back to it and crumpled into a frill)
        pts = [top, top + d_ * 0.005 + Vector((0, 0, 0.001))]
        L_ = 0.0
        for s_ in np.arange(0.006, 0.20, 0.002):
            org = Vector((NECK_AX.x, NECK_AX.y, z_edge[k] + 0.12)) + d_ * (r_edge[k] + s_)
            hit, nn, _i, _d = KNIT_BVH.ray_cast(org, Vector((0, 0, -1)), 0.5)
            if hit is None or hit.z > z_edge[k] + 0.03:
                continue
            q = hit + nn * 0.0025
            L_ += (q - pts[-1]).length
            pts.append(q)
            if L_ >= w_here:
                break
        # resampled to 10 points along its length
        L_ = [0.0]
        for i_ in range(1, len(pts)):
            L_.append(L_[-1] + (pts[i_] - pts[i_ - 1]).length)
        for r_i in range(10):
            t = L_[-1] * r_i / 9
            j = max(0, min(len(pts) - 2, int(np.searchsorted(L_, t)) - 1))
            f = (t - L_[j]) / max(1e-9, L_[j + 1] - L_[j])
            rows[r_i].append(pts[j].lerp(pts[j + 1], min(1.0, max(0.0, f))))
    # each row eased along the collar, its ends held (point by point the outer edge came out wavy), and laid back
    # on the blouse 2.5 mm off it
    for r_i in range(2, 10):
        row = rows[r_i]
        for _ in range(8):
            row = [row[0]] + [row[i_ - 1] * 0.25 + row[i_] * 0.5 + row[i_ + 1] * 0.25 for i_ in range(1, len(row) - 1)] + [row[-1]]
        for i_, q in enumerate(row):
            hit, nn, _f, _d = KNIT_BVH.find_nearest(q)
            if hit is not None:
                row[i_] = hit + nn * (0.0025 + 0.0004 * r_i / 9)
        rows[r_i] = row
    colm = strip("FlatCollar", rows, knitm, 0.0018)
    extras_.append(colm)
    log["flatCollar"] = {"widthMm": W * 1000, "gapMm": gap_m * 1000 * 2}


def turn_collar(extras_, STAND, FALL, POINT, gap_m):
    """A work jacket's turn-down collar (FREE-BASES-AND-COLLARS-2026-09-30.md: a separate piece drafted as a stand
    and a fall, laid over the neckline, not grown from the body; grown, it read as a crew neck with a cape): the stand
    rises STAND from the neckline, leaning in to 5 mm off the neck; at its top (the roll line) the fall folds back
    down over it and out over the shoulders, FALL wide; within 5 cm of each front end the fall lengthens to POINT, so
    each end comes to a point lying down the chest at the front of the neck; open at the throat by gap_m."""
    _bk = bmesh.new()
    _bk.from_mesh(knit_me)
    _ep = [v.co.copy() for v in _bk.verts if v.is_boundary and v.co.z > NECK_Z - 0.08
           and math.hypot(v.co.x - NECK_AX.x, v.co.y - NECK_AX.y) < opt("--edge-r", NECK_R + 0.03)]
    _bk.free()
    _ang = np.array([math.atan2(q.x - NECK_AX.x, -(q.y - NECK_AX.y)) for q in _ep])
    _rad = np.array([math.hypot(q.x - NECK_AX.x, q.y - NECK_AX.y) for q in _ep])
    _zz = np.array([q.z for q in _ep])
    o_ = np.argsort(_ang)
    _ang, _rad, _zz = _ang[o_], _rad[o_], _zz[o_]
    ext_a = np.concatenate([_ang - 2 * math.pi, _ang, _ang + 2 * math.pi])
    r0 = float(np.median(_rad))
    gap = gap_m / max(0.03, r0)
    grid_a = np.linspace(gap, 2 * math.pi - gap, 96)
    ga = np.where(grid_a > math.pi, grid_a - 2 * math.pi, grid_a)
    r_edge = np.interp(ga, ext_a, np.tile(_rad, 3))
    z_edge = np.interp(ga, ext_a, np.tile(_zz, 3))
    for _ in range(24):
        r_edge[1:-1] = 0.5 * r_edge[1:-1] + 0.25 * (r_edge[:-2] + r_edge[2:])
        z_edge[1:-1] = 0.5 * z_edge[1:-1] + 0.25 * (z_edge[:-2] + z_edge[2:])
    arc = (grid_a - gap) * r0
    arc_len = float(arc[-1])
    N_ST, N_FA = 4, 9
    rows = [[] for _ in range(N_ST + N_FA)]
    for k, a_ in enumerate(grid_a):
        d_ = Vector((math.sin(a_), -math.cos(a_), 0.0))
        u = min(arc[k], arc_len - arc[k])
        f_pt = max(0.0, 1.0 - u / 0.05)
        fall_here = FALL + (POINT - FALL) * f_pt ** 1.5
        foot = Vector((NECK_AX.x, NECK_AX.y, z_edge[k] - 0.004)) + d_ * (r_edge[k] + 0.003)
        top_z = z_edge[k] + STAND
        hn = BVH.ray_cast(Vector((NECK_AX.x, NECK_AX.y, top_z)), d_, 0.25)[0]
        r_top = ((hn - Vector((NECK_AX.x, NECK_AX.y, top_z))).length + 0.005) if hn is not None else r_edge[k] - 0.01
        r_top = min(r_top, r_edge[k] + 0.002)
        top = Vector((NECK_AX.x, NECK_AX.y, top_z)) + d_ * r_top
        for i_ in range(N_ST):
            t = i_ / (N_ST - 1)
            rows[i_].append(foot.lerp(top, t))
        # the fall: over the roll line, down outside the stand, then out over the jacket (rays from above), or at
        # the points down the chest (rays from in front)
        fold = top + d_ * 0.006 + Vector((0, 0, 0.003))
        over = Vector((NECK_AX.x, NECK_AX.y, z_edge[k] - 0.002)) + d_ * (r_edge[k] + 0.016)
        pts = [fold, over]
        L_ = (over - fold).length
        front_ = f_pt > 0.0 and math.cos(a_) > 0.5
        steps = np.arange(0.004, 0.25, 0.003)
        for s_ in steps:
            if front_:
                # down the chest, spreading a little outward (the points' lower edges part in a V)
                x_ = (over.x + math.copysign(s_ * 0.35, math.sin(a_) if abs(math.sin(a_)) > 1e-6 else 1.0))
                q = on_knit_from_front(x_, over.z - s_)
                q = None if q is None else q + Vector((0, -0.0035, 0))
            else:
                org = Vector((NECK_AX.x, NECK_AX.y, z_edge[k] + 0.15)) + d_ * (r_edge[k] + 0.016 + s_)
                hit, nn, _i, _d = KNIT_BVH.ray_cast(org, Vector((0, 0, -1)), 0.5)
                q = None if (hit is None or hit.z > z_edge[k]) else hit + nn * 0.0035
            if q is None:
                continue
            L_ += (q - pts[-1]).length
            pts.append(q)
            if L_ >= fall_here:
                break
        Lc = [0.0]
        for i_ in range(1, len(pts)):
            Lc.append(Lc[-1] + (pts[i_] - pts[i_ - 1]).length)
        for r_i in range(N_FA):
            t = Lc[-1] * r_i / (N_FA - 1)
            j = max(0, min(len(pts) - 2, int(np.searchsorted(Lc, t)) - 1))
            f = (t - Lc[j]) / max(1e-9, Lc[j + 1] - Lc[j])
            rows[N_ST + r_i].append(pts[j].lerp(pts[j + 1], min(1.0, max(0.0, f))))
    for r_i in range(N_ST + 2, N_ST + N_FA):                  # the fall's rows eased along the collar, ends held
        row = rows[r_i]
        for _ in range(6):
            row = [row[0]] + [row[i_ - 1] * 0.25 + row[i_] * 0.5 + row[i_ + 1] * 0.25 for i_ in range(1, len(row) - 1)] + [row[-1]]
        rows[r_i] = row
    colm = strip("TurnCollar", rows, knitm, 0.0025)
    extras_.append(colm)
    log["turnCollar"] = {"standMm": STAND * 1000, "fallMm": FALL * 1000, "pointMm": POINT * 1000}


def placket(extras_):
    """A buttoned front: a band down the middle from the neckline to the hem, 1.2 mm proud, its buttons."""
    top_z = NECK_Z + 0.06                                   # up to the neckline (the ray stops where the blouse ends)
    zs = np.linspace(HEM_Z + 0.01, top_z, 90)                # (24 steps stopped it up to 2 cm short of the collar)
    rows_p = []
    PW = opt("--placket-w", 0.025) / 2
    for off in (-PW, 0.0, PW):
        row = []
        for z_ in zs:
            q = on_knit_from_front(off, float(z_))
            row.append(q + Vector((0, -0.0012, 0)) if q is not None else None)
        rows_p.append(row)
    keep = [k for k in range(len(zs)) if all(r_[k] is not None for r_ in rows_p)]
    if len(keep) < 4:
        return
    rows_p = [[r_[k] for k in keep] for r_ in rows_p]
    extras_.append(strip("Placket", rows_p, knitm, 0.0012))
    zb = [z_ for z_ in np.linspace(opt("--button-low", HEM_Z + 0.06), rows_p[1][-1].z - opt("--button-top-gap", 0.05),
                                   opt("--buttons", 5, int))]      # (the top one half sank under the collar)
    for z_ in zb:
        q = on_knit_from_front(0.0, float(z_))
        if q is None:
            continue
        BR_ = opt("--button-r", 0.0055)
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=BR_, depth=0.0022 + BR_ * 0.25, location=q + Vector((0, -0.0038 - BR_ * 0.1, 0)),   # on the placket's face
                                            rotation=(math.pi / 2, 0, 0))
        b_ = bpy.context.active_object
        b_.data.materials.append(tailor.material("M_Button", tuple(float(c) for c in opt("--button-rgb", "0.82,0.78,0.68", str).split(",")), 0.3))
        extras_.append(b_)
    log["placket"] = {"buttons": len(zb)}


def neck_ring(extras_, NB, gap=0.0, edge_z_min=None, ribbed=True, name="Neckband"):
    """A band from the knit's own neck edge (its points round the neck by angle, smoothed), rising NB and leaning
    in to 5 mm off the neck, arched over the cut edge; closed, or open at the front by `gap` radians either side."""
    if edge_z_min is None:
        edge_z_min = NECK_Z - 0.08
    # the crew neck's band: a ribbed ring from the knit's neck edge up to hug the neck, 28 mm, rising

    # ANCHORED TO THE KNIT'S OWN NECK EDGE (placed by the neck's radius, the band
    # sat low on the wide base of a thick neck and flared out under the knit):
    # the edge's points round the neck, by angle, smoothed; the band stands up
    # from them, leaning a little in, over the edge
    _bk = bmesh.new()
    _bk.from_mesh(knit_me)
    _ep = [v.co.copy() for v in _bk.verts if v.is_boundary and v.co.z > edge_z_min
           and math.hypot(v.co.x - NECK_AX.x, v.co.y - NECK_AX.y) < opt("--edge-r", NECK_R + 0.03)]
    _bk.free()
    _ang = np.array([math.atan2(q.x - NECK_AX.x, -(q.y - NECK_AX.y)) for q in _ep])
    _rad = np.array([math.hypot(q.x - NECK_AX.x, q.y - NECK_AX.y) for q in _ep])
    _zz = np.array([q.z for q in _ep])
    order_ = np.argsort(_ang)
    _ang, _rad, _zz = _ang[order_], _rad[order_], _zz[order_]
    grid_a = np.linspace(-math.pi, math.pi, 97)[:-1]                     # a closed ring: no seam at the back
    if gap > 0:
        grid_a = np.linspace(gap, 2 * math.pi - gap, 80)                  # open at the front (a collar over an open zip)
        grid_a = np.where(grid_a > math.pi, grid_a - 2 * math.pi, grid_a)
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
        for k in range(len(grid_a) + (1 if gap <= 0 else 0)):
            a_ = grid_a[k % len(grid_a)]
            k = k % len(grid_a)
            d_ = Vector((math.sin(a_), -math.cos(a_), 0.0))
            # from the knit's edge (its foot a little under it) in a straight line to 5 mm off the neck, NB up
            foot_r, foot_z = r_edge[k] + opt("--foot-out", 0.012), z_edge[k] - opt("--foot-down", 0.010)   # well over the cut edge
            top_z = foot_z + NB * opt("--band-rise", 0.7)
            hn = BVH.ray_cast(Vector((NECK_AX.x, NECK_AX.y, top_z)), d_, 0.25)[0]
            top_r = ((hn - Vector((NECK_AX.x, NECK_AX.y, top_z))).length + 0.005) if hn is not None else foot_r - 0.01
            top_r = min(top_r, foot_r)
            top_r = max(top_r, foot_r - opt("--max-lean", 1.0))          # a stand collar stands (it had lain flat)
            t_ = r_i / 6
            r_ = foot_r + (top_r - foot_r) * t_
            # arched, so it clears the knit's cut edge it passes over (straight, the edge showed through it as
            # a sawtooth) and stands up round the neck rather than lying flat
            z_ = foot_z + (top_z - foot_z) * t_ + opt("--band-arch", 0.007) * math.sin(math.pi * min(1.0, t_ * 1.3))
            rib = (0.0011 * math.cos(a_ * 48) * (0.4 + 0.6 * t_)) if ribbed else 0.0
            row.append(Vector((NECK_AX.x, NECK_AX.y, z_)) + d_ * (r_ + rib))
        rows_n.append(row)
    nb_obj = strip(name, rows_n, knitm, 0.003)
    _nb = bmesh.new()
    _nb.from_mesh(nb_obj.data)
    bmesh.ops.remove_doubles(_nb, verts=_nb.verts[:], dist=1e-5)       # the ring's ends one seam-free piece
    _nb.to_mesh(nb_obj.data)
    _nb.free()
    extras_.append(nb_obj)
    _all = [q for r_ in rows_n for q in r_]
    log[name] = {"mm": NB * 1000, "zRange": [round(min(q.z for q in _all), 3), round(max(q.z for q in _all), 3)],
                       "rFoot": round(float(np.mean([(q - Vector((NECK_AX.x, NECK_AX.y, q.z))).length for q in rows_n[0]])), 3),
                       "rTop": round(float(np.mean([(q - Vector((NECK_AX.x, NECK_AX.y, q.z))).length for q in rows_n[-1]])), 3)}


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
        seg_f = [] if ZIP else [(q, (sgn, 0, 0), "front") for q in front]
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
    if len(path) > 8 and not ZIP:
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

    left = [] if ZIP else band_left_pts
    if ZIP:
        # the zip: a 7 mm metal line from the hem to the V's point, on the knit
        zp = [on_knit_from_front(0.0, z_) for z_ in np.linspace(HEM_Z + 0.002, V_Z, 40)]
        zp = [q for q in zp if q is not None]
        if len(zp) > 3:
            zipm = tailor.material("M_Zip", tuple(float(c) for c in opt("--zip-rgb", "0.10,0.10,0.11", str).split(",")), 0.3)
            rows_z = []
            for dx in (-0.0035, 0.0, 0.0035):
                rows_z.append([q + Vector((dx, -0.0015, 0.0)) for q in zp])
            extras.append(strip("Zip", rows_z, zipm, 0.0015))
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=zp[-1] + Vector((0, -0.004, -0.012)))
            pull = bpy.context.active_object
            pull.scale = (0.010, 0.004, 0.024)
            pull.data.materials.append(zipm)
            extras.append(pull)
        log["zip"] = len(zp)
        # two slanted pocket openings, low on the front (the concept)
        for sgn in (1.0, -1.0):
            pp = [on_knit_from_front(sgn * (opt("--pocket-x", 0.085) + 0.035 * t_), HEM_Z + WELT + 0.02 + opt("--pocket-h", 0.13) * t_)
                  for t_ in np.linspace(0.0, 1.0, 14)]
            pp = [q for q in pp if q is not None]
            if len(pp) > 3:
                pocm = tailor.material("M_PocketEdge", tuple(0.6 * float(c) for c in knit_col), 0.5)
                rows_p = [[q + Vector((dx, -0.0012, 0.0)) for q in pp] for dx in (-0.003, 0.003)]
                extras.append(strip("Pocket", rows_p, pocm, 0.0012))
        # a narrow facing up each side of the open V (the zip's tape), so its edges are finished, not raw
        for sgn in (() if EXTRUDE else (1.0, -1.0)):
            vp = [on_knit_from_front(sgn * (0.004 + (NECK_SIDE - 0.004) * t_ + 0.006), V_Z + (Zn - V_Z) * t_)
                  for t_ in np.linspace(0.0, opt("--facing-top", 0.86), 24)]            # stopping under the collar
            vp = [q for q in vp if q is not None]
            if len(vp) > 3:
                sd_ = (sgn * (Zn - V_Z), 0.0, -NECK_SIDE)
                _bi, _bo = opt("--band-in", 0.020), opt("--band-out", 0.009)
                o_, _i, _o = band_along(vp, [sd_] * len(vp), name="Facing")
                extras.append(o_)
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
    if ZIP:
        blousem = tailor.material("M_TShirtWhite", (0.88, 0.88, 0.86), 0.7)
    if len(blouse_rows) > 2:
        extras.append(strip("BlouseFront", blouse_rows, blousem, 0.0012))
    if len(blouse_rows) > 2 and not ZIP:
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
    if not ZIP:
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
    log["blouse"] = {"panelRows": len(blouse_rows), "collarMm": 0 if ZIP else COLLAR * 1000}
else:
    extras = []
    if "--flat-collar" in argv:
        # A BLOUSE (Sheila's "cream blouse with a small round collar", 30 September): a narrow band at the neckline,
        # a flat round collar folded over it and lying on her shoulders and chest, its ends rounded at the throat,
        # and a buttoned placket down the front
        if opt("--turn-collar", 0.0):
            turn_collar(extras, opt("--stand", 0.025), opt("--turn-collar", 0.0), opt("--collar-point-len", 0.10),
                        opt("--collar-gap-m", 0.012))
        else:
            neck_ring(extras, opt("--neckband", 0.012), ribbed=False, name="CollarStand")
            flat_collar(extras, opt("--collar-w", 0.062), opt("--collar-gap-m", 0.012))
        placket(extras)
    else:
        neck_ring(extras, opt("--neckband", 0.028))
if ZIP and not EXTRUDE:
    # THE SHELL SUIT'S STAND COLLAR: the same band, taller and plain, round the back and sides, open over the zip
    _gap = math.asin(min(0.95, (NECK_SIDE + opt("--collar-gap", 0.006)) / max(1e-6, NECK_R + 0.03)))
    neck_ring(extras, opt("--collar-h", 0.045), gap=_gap, edge_z_min=Zn - 0.004, ribbed=False, name="Collar")

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
            rib = 0.0011 * opt("--rib", 1.0) * math.cos(2 * math.pi * k / max(1, around) * (2 * math.pi * radius_guess / rib_every))
            row.append(hit + d_ * (depth_out + rib))
        grid.append(row)
    # a miss filled from its nearest hits round the row (dropped, it left a gap at the side seam that read as a tear)
    if opt("--fill-misses", 0, int):
        for r in range(rows):
            row = grid[r]
            hits = [k for k in range(around + 1) if row[k] is not None]
            if hits and len(hits) < around + 1:
                for k in range(around + 1):
                    if row[k] is None:
                        kb = max([h for h in hits if h < k], default=None)
                        ka = min([h for h in hits if h > k], default=None)
                        if kb is not None and ka is not None:
                            t_ = (k - kb) / (ka - kb)
                            row[k] = row[kb] * (1 - t_) + row[ka] * t_
    # drop columns that missed anywhere, or fall in the skipped (the front opening) span
    keep_cols = [k for k in range(around + 1) if all(grid[r][k] is not None for r in range(rows))
                 and (skip is None or not skip(grid[0][k]))]
    if len(keep_cols) < 4:
        return None
    rows_pts = [[grid[r][k] for k in keep_cols] for r in range(rows)]
    return strip(name, rows_pts, knitm, 0.002)


mid_c = Vector((0.0, mid_y, 0.0))
WD = opt("--welt-drop", 0.006)          # the welt's lowest row below the knit (0 for a T-shirt: below, it met the body, frilled)
welt = ring_band("Welt", lambda r: Vector((0.0, mid_y, HEM_Z + 0.002 + (WELT - 0.002) * r / 5 - (WD if r == 0 else 0.0))), lambda r: Vector((0, 0, 1)),
                 6, 256, 0.0025, 0.007, 0.20,
                 skip=lambda q: q is None or (not CREW and q.y < FRONT_Y and abs(q.x) < 0.012))   # (a pullover's welt goes all round)
if welt and (not EXTRUDE or CREW) and not opt("--tuck", 0.0) and "--no-welt" not in argv:      # (tucked in, a hem band showed as a ledge)
    extras.append(welt)
# SNUG CUFFS (the second review: 'the sleeve ends flare open with a thin,
# ragged rim'): each a ribbed tube 5 cm long round the wrist, 8 mm clear of it,
# the sleeve's last 10 cm drawn in to meet it and ending 5 mm over it
WRIST_R = opt("--wrist-r", 0.026) + 0.008
for s_ in (() if EXTRUDE else ("l", "r")):
    a_, h_ = (Vector(tuple(wrist[s_][0])), Vector(tuple(wrist[s_][1])))
    ax_ = (h_ - a_).normalized()
    L_ = (h_ - a_).length
    t1 = opt("--cuff-t", 0.90) * L_
    # the sleeve drawn in
    for v in knit_me.vertices:
        p = Vector(v.co)
        if (p.x > 0) != (s_ == "l") or abs(p.x) < (0.12 if SHORT else 0.2):
            continue
        rel = p - a_
        t = rel.dot(ax_)
        radial = rel - ax_ * t
        CD = opt("--cuff-draw", 0.10)
        if t1 - CD < t <= t1 + 0.01 and radial.length < (0.09 if SHORT else 0.07):   # the sleeve only (not her hip)
            f = min(1.0, (t - (t1 - CD)) / CD)
            r_now = radial.length
            r_to = r_now + (WRIST_R + 0.003 - r_now) * f
            if radial.length > 1e-6:
                v.co = a_ + ax_ * t + radial.normalized() * r_to
    u_ = ax_.orthogonal().normalized()
    w_ = ax_.cross(u_).normalized()
    rows_k = []
    CL = opt("--cuff-len", 0.05)                          # (a T-shirt's sleeve hem: 2 cm, plain)
    for r_i in range(6):
        c_ = a_ + ax_ * (t1 - CL + 0.005 + CL * r_i / 5)
        row = []
        for k in range(49):
            ang = 2 * math.pi * k / 48
            rib = 0.0012 * opt("--rib", 1.0) * math.cos(ang * 16)
            row.append(c_ + (u_ * math.cos(ang) + w_ * math.sin(ang)) * (WRIST_R + rib))
        rows_k.append(row)
    extras.append(strip("Cuff", rows_k, knitm, 0.003))
knit_me.update()
log["ribbed"] = {"welt": bool(welt)}

# ---- a second colour over the shoulders and upper sleeves (--panels r,g,b: a shell suit's raglan panels) --------
PANELS = opt("--panels", "", str)
if PANELS:
    # CLEAN PANEL LINES (assigned face by face the edge came out sawtoothed):
    # the knit is first cut along each raglan line (a plane from the side of the
    # neck down to the armpit) and across each arm below the elbow, then each
    # face takes the panel colour above its raglan line and above that cut
    panm = tailor.material("M_Panel", tuple(float(c) for c in PANELS.split(",")), 0.5)
    knit_me.materials.append(panm)
    NS = NECK_SIDE + 0.01
    T_P = opt("--panel-t", 1.15)
    planes = {}
    bmp = bmesh.new()
    bmp.from_mesh(knit_me)
    for sd, sg in (("l", 1.0), ("r", -1.0)):
        sh = Vector(tuple(tailor.joint(arm, "upperarm_" + sd)))
        el = Vector(tuple(tailor.joint(arm, "lowerarm_" + sd)))
        P0 = Vector((sg * NS, 0.0, NECK_Z - 0.02))
        P1 = Vector((sg * (abs(sh.x) + 0.03), 0.0, opt("--armpit-z", 1.40)))
        d_ = P1 - P0
        n_ = Vector((d_.z, 0.0, -d_.x)).normalized()
        if n_.dot(Vector((sg * 0.15, 0.0, NECK_Z + 0.05)) - P0) < 0:
            n_ = -n_
        Q = sh + (el - sh) * T_P
        m_ = (el - sh).normalized()
        planes[sd] = (P0, n_, Q, m_)
        for co_, no_ in ((P0, n_), (Q, m_)):
            bmesh.ops.bisect_plane(bmp, geom=bmp.verts[:] + bmp.edges[:] + bmp.faces[:], plane_co=co_, plane_no=no_)
    # slivers the cuts left collapsed (the first review: dark specks along the panel line)
    bmesh.ops.dissolve_degenerate(bmp, dist=0.0008, edges=bmp.edges[:])
    TRIM_P = bmp.faces.layers.int.get("trim")
    for f in bmp.faces:
        c = f.calc_center_median()
        if TRIM_P is not None and f[TRIM_P] in (1, 2, 3, 4):
            continue                                 # the collar, tapes, waistband and cuffs keep the body colour
        sd = "l" if c.x > 0 else "r"
        P0, n_, Q, m_ = planes[sd]
        # the teal ends at the raglan line itself; only the collar (inside the neckline) stays purple (an extra
        # clearance from the neck's side left the line jagged where it met the collar)
        if (c - P0).dot(n_) > 0 and (c - Q).dot(m_) < 0:
            f.material_index = 1
    bmp.to_mesh(knit_me)
    bmp.free()
    knit_me.update()
    log["panels"] = PANELS

YOKE = opt("--yoke", "", str)
if YOKE:
    # A DONKEY JACKET'S YOKE (production/reference/donkey-jacket-1990.md): one piece over both shoulders, front and
    # back, cut along clean plane lines: at the front a level line --yoke-front below the base of the neck, at the
    # back a level line at the armpits; over the top of the sleeves down to where the shoulder rounds off
    yk = tailor.material("M_Yoke", tuple(float(c) for c in YOKE.split(",")), 0.35)
    knit_me.materials.append(yk)
    yi = len(knit_me.materials) - 1
    z_front = NECK_Z - opt("--yoke-front", 0.10)
    z_back = opt("--yoke-back-z", NECK_Z - 0.26)
    bmy = bmesh.new()
    bmy.from_mesh(knit_me)
    for zc_ in (z_front, z_back):
        bmesh.ops.bisect_plane(bmy, geom=bmy.verts[:] + bmy.edges[:] + bmy.faces[:], plane_co=(0, 0, zc_), plane_no=(0, 0, 1))
    sx_ = {}
    for sd, sg in (("l", 1.0), ("r", -1.0)):
        sh = Vector(tuple(tailor.joint(arm, "upperarm_" + sd)))
        sx_[sd] = (sh, sg)
        # the armhole: an upright plane over the shoulder joint (square to the arm, it slanted across the back and
        # left the back yoke a V)
        bmesh.ops.bisect_plane(bmy, geom=bmy.verts[:] + bmy.edges[:] + bmy.faces[:],
                               plane_co=Vector((sg * (abs(sh.x) + opt("--yoke-side", 0.0)), 0, 0)), plane_no=Vector((1, 0, 0)))
    bmesh.ops.dissolve_degenerate(bmy, dist=0.0008, edges=bmy.edges[:])
    TRIM_Y = bmy.faces.layers.int.get("trim")
    n_y = 0
    for f in bmy.faces:
        c = f.calc_center_median()
        if TRIM_Y is not None and f[TRIM_Y] in (1, 2, 3, 4):
            continue
        sh, sg = sx_["l" if c.x > 0 else "r"]
        if abs(c.x) > abs(sh.x) + opt("--yoke-side", 0.0):
            continue                                  # the sleeve stays wool: the yoke ends at the armhole
        front = c.y < NECK_AX.y
        if (front and c.z > z_front) or ((not front) and c.z > z_back):
            f.material_index = yi
            n_y += 1
    bmy.to_mesh(knit_me)
    bmy.free()
    knit_me.update()
    log["yoke"] = {"faces": n_y, "frontZ": round(z_front, 3), "backZ": round(z_back, 3)}

if "--pockets-inset" in argv:
    PW_, PH_ = opt("--pocket-w", 0.19), opt("--pocket-h", 0.20)
    z0_, z1_ = HEM_Z + opt("--pocket-low", 0.08), HEM_Z + opt("--pocket-low", 0.08) + PH_
    bpk = bmesh.new()
    bpk.from_mesh(knit_me)
    yc0 = float(np.median([v.co.y for v in bpk.verts]))
    for sg in (1.0, -1.0):
        cx = sg * opt("--pocket-x", 0.115)
        for pc_, pn_ in (((cx - PW_ / 2, 0, 0), (1, 0, 0)), ((cx + PW_ / 2, 0, 0), (1, 0, 0)),
                         ((0, 0, z0_), (0, 0, 1)), ((0, 0, z1_), (0, 0, 1))):
            # cut only round the pocket (cut right round the jacket, each plane left a ragged line across it)
            fz = [f for f in bpk.faces if f.calc_center_median().y < yc0 and abs(f.calc_center_median().x - cx) < PW_ / 2 + 0.02
                  and z0_ - 0.02 < f.calc_center_median().z < z1_ + 0.02]
            gv = list({v for f in fz for v in f.verts})
            ge = list({e for f in fz for e in f.edges})
            bmesh.ops.bisect_plane(bpk, geom=gv + ge + fz, plane_co=pc_, plane_no=pn_)
    bpk.normal_update()
    yc_ = float(np.median([v.co.y for v in bpk.verts]))
    inside = set()
    for f in bpk.faces:
        c = f.calc_center_median()
        if c.y < yc_ and z0_ < c.z < z1_ and any(abs(c.x - sg * opt("--pocket-x", 0.115)) < PW_ / 2 for sg in (1.0, -1.0)):
            inside |= set(f.verts)
    rim = {v for v in inside if any(e.other_vert(v) not in inside for e in v.link_edges)}
    for v in inside:
        v.co = v.co + v.normal * (0.0004 if v in rim else opt("--pocket-raise", 0.003))
    # the pocket's outline a hard edge (a smooth step of a millimetre or two did not show at all)
    in_f = set()
    for f in bpk.faces:
        c = f.calc_center_median()
        if all(v in inside for v in f.verts):
            in_f.add(f)
    n_sharp = 0
    for e in bpk.edges:
        lf = e.link_faces
        if len(lf) == 2 and ((lf[0] in in_f) != (lf[1] in in_f)):
            e.smooth = False
            n_sharp += 1
        if len(lf) == 2 and lf[0] in in_f and lf[1] in in_f and all(v in rim for v in e.verts):
            e.smooth = False
    bpk.to_mesh(knit_me)
    bpk.free()
    knit_me.update()
    log["pocketsInset"] = {"points": len(inside), "sharpEdges": n_sharp}

if EXTRUDE and ZIP:
    # the zip's tapes (the rows grown out from each side of the V) in the zip's colour
    zipm2 = tailor.material("M_ZipTape", tuple(float(c) for c in opt("--zip-rgb", "0.10,0.10,0.11", str).split(",")), 0.3)
    knit_me.materials.append(zipm2)
    zi = len(knit_me.materials) - 1
    Zn_y = NECK_Z - 0.25 * 0.07
    _tr = knit_me.attributes.get("trim")
    if _tr is not None:
        for f in knit_me.polygons:
            if _tr.data[f.index].value == 2:
                f.material_index = zi

if "--patch-pockets" in argv:
    # TWO FLAPLESS PATCH POCKETS low on the front (a donkey jacket's: about 19 cm wide and 20 tall, their feet 8 cm
    # over the hem), one layer 1 mm proud, their rims eased into the jacket
    PW_, PH_ = opt("--pocket-w", 0.19), opt("--pocket-h", 0.20)
    for sg in (1.0, -1.0):
        cx = sg * opt("--pocket-x", 0.115)
        rows_pp = []
        for j in range(11):
            z_ = HEM_Z + opt("--pocket-low", 0.08) + PH_ * j / 10
            row = []
            for i in range(11):
                x_ = cx - PW_ / 2 + PW_ * i / 10
                q = on_knit_from_front(x_, float(z_))
                if q is None:
                    row.append(None)
                    continue
                rim = min(1.0, min(i, 10 - i) / 1.2, (10 - j) / 1.2 if j > 0 else 1.0)
                hit, nn, _f, _d = KNIT_BVH.find_nearest(q)
                row.append(q + (nn if hit is not None else Vector((0, -1, 0))) * (0.0008 + 0.0012 * rim))
            rows_pp.append(row)
        nm_ = sum(1 for rr in rows_pp for r_ in rr if r_ is None)
        log.setdefault("pocketMisses", []).append(nm_)
        for rr in rows_pp:                             # a miss filled from its row's neighbours
            for i_ in range(len(rr)):
                if rr[i_] is None:
                    nb_ = [rr[j_] for j_ in (i_ - 1, i_ + 1) if 0 <= j_ < len(rr) and rr[j_] is not None]
                    rr[i_] = sum(nb_, Vector()) / len(nb_) if nb_ else None
        nm_ = sum(1 for rr in rows_pp for r_ in rr if r_ is None)
        if nm_ == 0:
            extras.append(strip("PatchPocket", rows_pp, knitm, 0.0012))
    log["patchPockets"] = {"wMm": PW_ * 1000, "hMm": PH_ * 1000}

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
