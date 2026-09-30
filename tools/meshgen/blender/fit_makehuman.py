"""A ready-made MakeHuman garment (CC0) fitted onto a MetaHuman body, as the shape of a game garment.

    blender -b -P tools/meshgen/blender/fit_makehuman.py -- GARMENT.obj BODY_FullBody.fbx OUT_DIR [--name tom_suit]

WHY, 30 September (Jafar's list, item 2: free ready-made tailored clothes from MakeHuman's CC0 libraries, altered
and re-coloured to read as 1990 British working clothes, bound as game clothes are; the research:
production/research/clothing-pipeline/PIPELINE-2026-09-30.md and TAILORED-ROUTES-2026-09-30.md). A MakeHuman garment
is modelled on MakeHuman's own base body (decimetres, y up); nothing ties it to a MetaHuman, so it is carried over:
  1. imported, metres, z up, facing -y;
  2. its heights mapped piece by piece onto the body's: its collar's top to the base of his neck, its crotch to
     his, its hems to his ankles (the two bodies' proportions differ);
  3. its sleeves turned about the shoulder to lie along his arms (the two rest poses hold the arms differently);
  4. fitted by a smooth displacement: each round, every point is pushed out of the body to at least --min-ease and
     drawn in where it stands more than --max-ease off, and those moves are smoothed over the garment many times
     before they are applied, so the whole shape follows his body while the garment's own detail (lapels,
     pockets, creases) rides along unchanged.
OUT_DIR gets NAME.blend (the garment, "GarmentRender", beside the body), NAME_render_static.fbx and pictures.
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
OBJ, BODY, OUT = argv[0], argv[1], argv[2]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "garment", str)
log = {"garment": OBJ, "body": BODY}


def say(*a):
    print("FIT", *a, flush=True)


arm, body = tailor.load_body(BODY, lod=1)
BVH = tailor.bvh_of(body)
bco = np.array([tuple(body.matrix_world @ v.co) for v in body.data.vertices])
J = lambda n: arm.matrix_world @ arm.pose.bones[n].head

# ---- 1. import -------------------------------------------------------------------------------------------------
before = set(bpy.data.objects)
bpy.ops.wm.obj_import(filepath=OBJ, forward_axis="Y", up_axis="Z")
g = next(o for o in bpy.data.objects if o not in before and o.type == "MESH")
g.name = "GarmentRender"
g.data.name = "GarmentRender"
# MakeHuman: y up, the figure facing +z, decimetres. Blender here: z up, facing -y, metres.
M = Matrix(((0.1, 0, 0, 0), (0, 0, -0.1, 0), (0, 0.1, 0, 0), (0, 0, 0, 1)))
raw = np.array([tuple(v.co) for v in g.data.vertices])
# the importer's own axes are undone first: take the file's numbers as they are
for i, v in enumerate(g.data.vertices):
    v.co = Vector(tuple(raw[i]))
g.matrix_world = Matrix.Identity(4)
co = np.array([tuple(v.co) for v in g.data.vertices])
# decide the file's up and front from the shape itself: up is the long axis; the front is where the jacket opens
ext = co.max(axis=0) - co.min(axis=0)
up_ax = int(np.argmax(ext))
say("file extents", ext.round(2).tolist(), "up axis", up_ax)
if up_ax == 1:
    co = np.column_stack([co[:, 0] * 0.1, -co[:, 2] * 0.1, co[:, 1] * 0.1])
elif up_ax == 2:
    co = co * 0.1
else:
    raise SystemExit("unexpected axes")

# ---- 2. heights, piece by piece ----------------------------------------------------------------------------------
def crotch_of(pts, top_z):
    """The lowest height at which something lies in the middle between the legs."""
    yc = float(np.median(pts[:, 1]))
    mid = pts[(np.abs(pts[:, 0]) < 0.015) & (np.abs(pts[:, 1] - yc) < 0.045)]
    mid = mid[mid[:, 2] < top_z - 0.3]
    return float(mid[:, 2].min()) if len(mid) else None


g_top, g_bot = float(co[:, 2].max()), float(co[:, 2].min())
g_crotch = crotch_of(co, g_top)
floor = float(bco[:, 2].min())
b_neck = float(J("neck_01").z) + opt("--collar-up", 0.02)
b_crotch = crotch_of(bco, float(bco[:, 2].max()))
b_ankle = floor + opt("--hem-up", 0.035)
say("garment top/crotch/bottom", round(g_top, 3), g_crotch and round(g_crotch, 3), round(g_bot, 3),
    "body neck/crotch/ankle", round(b_neck, 3), b_crotch and round(b_crotch, 3), round(b_ankle, 3))
if g_crotch is not None and b_crotch is not None and g_bot < g_crotch - 0.2:
    src = [g_bot, g_crotch, g_top]
    dst = [b_ankle, b_crotch - 0.01, b_neck]
else:                                             # a garment with no legs: the top only, the scale from the torso
    src = [g_bot, g_top]
    dst = [b_neck - (g_top - g_bot) * (b_neck - b_crotch) / max(1e-6, (g_top - (g_crotch or g_bot))), b_neck]
co[:, 2] = np.interp(co[:, 2], src, dst)
# across: the garment's width at the chest to the body's chest plus its ease, and centred on him
z_chest = float(J("spine_04").z)
def half_widths(pts, z_, band=0.02, xmax=0.22):
    s_ = pts[(np.abs(pts[:, 2] - z_) < band) & (np.abs(pts[:, 0]) < xmax)]
    return (float(np.percentile(np.abs(s_[:, 0] - np.median(s_[:, 0])), 95)),
            float(np.percentile(s_[:, 1], 95) - np.percentile(s_[:, 1], 5)) / 2, float(np.median(s_[:, 0])), float(np.median(s_[:, 1])))
bw, bd, bx, by = half_widths(bco, z_chest)
gw, gd, gx, gy = half_widths(co, z_chest, xmax=0.25)
sx_ = (bw + opt("--ease", 0.03)) / max(1e-6, gw)
sy_ = (bd + opt("--ease", 0.03)) / max(1e-6, gd)
co[:, 0] = bx + (co[:, 0] - gx) * sx_
co[:, 1] = by + (co[:, 1] - gy) * sy_
log["scale"] = {"heights": [src, dst], "x": round(sx_, 3), "y": round(sy_, 3)}

# ---- 3. the sleeves turned onto his arms ------------------------------------------------------------------------
for sd, sg in (("l", 1.0), ("r", -1.0)):
    sh = J("upperarm_" + sd)
    hand = J("hand_" + sd)
    side = co[:, 0] * sg > abs(sh.x) - 0.02
    arm_pts = co[side & (co[:, 2] < sh.z + 0.05)]
    if len(arm_pts) < 20:
        continue
    far = arm_pts[np.argsort(-(arm_pts[:, 0] * sg))[:max(10, len(arm_pts) // 40)]]
    g_wrist = far.mean(axis=0)
    a_g = math.atan2(sh.z - g_wrist[2], abs(g_wrist[0] - sh.x))
    a_b = math.atan2(sh.z - hand.z, abs(hand.x - sh.x))
    turn = a_b - a_g                                   # more downward if positive
    for i in np.where(side)[0]:
        p = co[i]
        d_ = p[0] * sg - (abs(sh.x) - 0.02)
        w_ = min(1.0, max(0.0, d_ / 0.08))
        if w_ <= 0:
            continue
        rx, rz = (p[0] - sh.x) * sg, p[2] - sh.z
        c_, s_ = math.cos(-turn * w_), math.sin(-turn * w_)
        nx, nz = rx * c_ - rz * s_, rx * s_ + rz * c_
        co[i, 0] = sh.x + nx * sg
        co[i, 2] = sh.z + nz
    log.setdefault("sleeveTurnDeg", {})[sd] = round(math.degrees(turn), 1)
for i, v in enumerate(g.data.vertices):
    v.co = Vector(tuple(co[i]))
g.data.update()

# ---- 4. the smooth fit ------------------------------------------------------------------------------------------
edges = np.array([e.vertices[:] for e in g.data.edges])
deg = np.bincount(edges.ravel(), minlength=len(co)).astype(float)
MIN_E, MAX_E = opt("--min-ease", 0.012), opt("--max-ease", 0.05)
for rnd in range(opt("--rounds", 6, int)):
    disp = np.zeros_like(co)
    for i, p in enumerate(co):
        hit, nn, _f, dist = BVH.find_nearest(Vector(tuple(p)))
        if hit is None:
            continue
        d_ = Vector(tuple(p)) - hit
        off = d_.dot(nn)
        if off < MIN_E:
            disp[i] = np.array(tuple(nn)) * (MIN_E - off)
        elif off > MAX_E and dist < 0.25:
            disp[i] = -np.array(tuple(nn)) * (off - MAX_E) * 0.5
    for _ in range(opt("--smooth", 30, int)):
        acc = np.zeros_like(disp)
        np.add.at(acc, edges[:, 0], disp[edges[:, 1]])
        np.add.at(acc, edges[:, 1], disp[edges[:, 0]])
        disp = 0.5 * disp + 0.5 * acc / np.maximum(deg, 1)[:, None]
    co = co + disp
    say("round", rnd, "moved most mm", round(float(np.linalg.norm(disp, axis=1).max()) * 1000, 1))
# a last push: nothing inside him
for i, p in enumerate(co):
    hit, nn, _f, _d = BVH.find_nearest(Vector(tuple(p)))
    if hit is not None and (Vector(tuple(p)) - hit).dot(nn) < 0.004:
        co[i] = np.array(tuple(hit + nn * 0.004))
for i, v in enumerate(g.data.vertices):
    v.co = Vector(tuple(co[i]))
g.data.update()

# ---- 5. colour, pictures, files ---------------------------------------------------------------------------------
RGB = opt("--rgb", "", str)
if RGB:
    g.data.materials.clear()
    g.data.materials.append(tailor.material("M_Suit", tuple(float(c) for c in RGB.split(",")), 0.8))
for p_ in g.data.polygons:
    p_.use_smooth = True
if opt("--subsurf", 0, int):
    sm = g.modifiers.new("Sub", "SUBSURF")
    sm.levels = opt("--subsurf", 0, int)
    bpy.ops.object.select_all(action="DESELECT")
    g.select_set(True)
    bpy.context.view_layer.objects.active = g
    bpy.ops.object.modifier_apply(modifier="Sub")
body.data.materials.clear()
body.data.materials.append(tailor.material("M_Body", (0.55, 0.55, 0.56)))
log["render"] = {"verts": len(g.data.vertices), "tris": sum(len(p_.vertices) - 2 for p_ in g.data.polygons)}
tailor.pictures(os.path.join(OUT, "fit"), Vector((0, 0, 1.0)), views=(("front", (0, -3.4, 0.1)), ("side", (3.4, 0, 0.1)),
                                                                       ("back", (0, 3.4, 0.1)), ("three-quarter", (2.3, -2.4, 0.4))))
tailor.pictures(os.path.join(OUT, "fit-close"), Vector((0, 0, 1.3)), views=(("front", (0, -1.3, 0.1)), ("three-quarter", (0.9, -0.9, 0.2)),
                                                                             ("back", (0, 1.3, 0.1))), res=(700, 700))
bpy.ops.object.select_all(action="DESELECT")
g.select_set(True)
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_render_static.fbx"), use_selection=True,
                         object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "fit.json"), "w"), indent=1)
say("done", json.dumps(log))
