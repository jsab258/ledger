"""A carried garment pushed clear of the body and of the garment under it, measured first.

    blender -b -P tools/meshgen/blender/clear_layers.py -- GARMENT.blend NAME OUT_DIR --over UNDER.blend:UNDER_NAME
        [--body-clear 0.008] [--over-clear 0.005] [--neck-margin 0.03] [--rounds 24] [--measure]

WHY, 7 November 2026 (n02-9-dress-the-cast, the packaged film of build 3143bf6). carry_garment.py pushes a point out
of the new body only as far as it stood off the old one, which keeps a neckline from funnelling, and it knows nothing
of the garment beneath. On Darren and Ron the jeans' waist cut through the jumper's hem in a jagged line and skin
showed at Darren's breastbone. Below the neck (the neck ring lies inside the neck on purpose, hidden by it), each
point is moved out along the nearest surface's normal until it clears the body and the under garment; the moves are
spread over the neighbouring points so no dent or step shows. The under garment is left as it is.

GARMENT.blend is carry_garment.py's NAME.blend, which holds the wearer's body and skeleton. OUT_DIR gets NAME.blend,
NAME_static.fbx and clear.json, ready for skin_garment.py. --measure writes clear.json only.
"""
import json
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
IN, NAME, OUT = argv[:3]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


BODY_CLEAR = opt("--body-clear", 0.008)
OVER_CLEAR = opt("--over-clear", 0.005)
NECK_MARGIN = opt("--neck-margin", 0.03)
ROUNDS = opt("--rounds", 24, int)
MEASURE = "--measure" in argv
OVER = opt("--over", "", str)

bpy.ops.wm.open_mainfile(filepath=IN)
g = bpy.data.objects[NAME]
body = max((o for o in bpy.data.objects if o.type == "MESH" and o is not g), key=lambda o: len(o.data.vertices))
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")


def bvh(o):
    b = bmesh.new()
    b.from_mesh(o.data)
    b.transform(o.matrix_world)
    b.normal_update()
    t = BVHTree.FromBMesh(b)
    b.free()
    return t


BODY = bvh(body)
UNDER, under_top = None, None
if OVER:
    path, under_name = OVER.rsplit(":", 1)
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [under_name]
    u = dst.objects[0]
    bpy.context.scene.collection.objects.link(u)
    u.parent = None
    UNDER = bvh(u)
    under_top = max((u.matrix_world @ v.co).z for v in u.data.vertices)

neck_z = (arm.matrix_world @ arm.pose.bones["neck_01"].head).z - NECK_MARGIN
neck_z_front = (arm.matrix_world @ arm.pose.bones["neck_01"].head).z - opt("--front-neck-margin", NECK_MARGIN)
me = g.data
P = np.array([tuple(g.matrix_world @ v.co) for v in me.vertices])
log = {"in": IN, "name": NAME, "points": len(P), "bodyPoints": len(body.data.vertices), "body": body.name, "neckZ": round(float(neck_z), 3),
       "underTop": None if under_top is None else round(float(under_top), 3), "bodyClear": BODY_CLEAR, "overClear": OVER_CLEAR}


def signed(tree, p):
    h, n, _f, _d = tree.find_nearest(Vector(p))
    if h is None:
        return None, None
    return (Vector(p) - h).dot(n), np.array(tuple(n))


need = np.zeros_like(P)
off_body = np.full(len(P), np.nan)
off_under = np.full(len(P), np.nan)
for i, p in enumerate(P):
    # the front of the neck ring's neighbourhood is reached (--front-neck-margin), its back never: pushed there the back of
    # the ring moved 22 mm and would stand up in a funnel (7 November, Darren's first measure)
    if p[2] > (neck_z_front if p[1] < 0 else neck_z):
        continue
    o, n = signed(BODY, p)
    if o is not None:
        off_body[i] = o
        if o < BODY_CLEAR:
            need[i] = n * (BODY_CLEAR - o)
    if UNDER is not None and p[2] < under_top + 0.01:
        o, n = signed(UNDER, p + need[i])
        if o is not None:
            off_under[i] = o
            if o < OVER_CLEAR:
                need[i] = need[i] + n * (OVER_CLEAR - o)


def report(a):
    a = a[~np.isnan(a)]
    if not len(a):
        return None
    return {"n": len(a), "minMm": round(float(a.min()) * 1000, 1), "under0": int((a < 0).sum()), "under3mm": int((a < 0.003).sum()),
            "under8mm": int((a < 0.008).sum()), "medianMm": round(float(np.median(a)) * 1000, 1)}


log["offBody"] = report(off_body)
log["offUnder"] = report(off_under)
worst = np.argsort(np.nan_to_num(off_body, nan=9))[:8]
log["worstBody"] = [[round(float(c), 3) for c in P[i]] + [round(float(off_body[i]) * 1000, 1)] for i in worst]
log["pointsToMove"] = int((np.linalg.norm(need, axis=1) > 0).sum())

if not MEASURE:
    edges = np.array([e.vertices[:] for e in me.edges])
    deg = np.bincount(edges.ravel(), minlength=len(P)).astype(float)
    below = P[:, 2] <= np.where(P[:, 1] < 0, neck_z_front, neck_z)
    size = np.linalg.norm(need, axis=1)
    push = need.copy()
    for _ in range(ROUNDS):
        acc = np.zeros_like(push)
        np.add.at(acc, edges[:, 0], push[edges[:, 1]])
        np.add.at(acc, edges[:, 1], push[edges[:, 0]])
        avg = acc / np.maximum(deg, 1)[:, None]
        bigger = np.linalg.norm(avg, axis=1) > size
        push = np.where((bigger & below)[:, None], avg, need)
    Q = P + push
    inv = g.matrix_world.inverted()
    for i, v in enumerate(me.vertices):
        v.co = inv @ Vector(Q[i])
    me.update()
    log["mostPushMm"] = round(float(np.linalg.norm(push, axis=1).max()) * 1000, 1)
    edge_before = np.linalg.norm(P[edges[:, 0]] - P[edges[:, 1]], axis=1)
    edge_after = np.linalg.norm(Q[edges[:, 0]] - Q[edges[:, 1]], axis=1)
    ratio = edge_after / np.maximum(edge_before, 1e-6)
    log["edgeStretchMax"] = round(float(ratio.max()), 3)
    if UNDER is not None:
        bpy.data.objects.remove(u, do_unlink=True)
    bpy.ops.object.select_all(action="DESELECT")
    g.select_set(True)
    bpy.context.view_layer.objects.active = g
    bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_static.fbx"), use_selection=True, object_types={"MESH"},
                             mesh_smooth_type="OFF", use_tspace=True, add_leaf_bones=False, colors_type="LINEAR")
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))

json.dump(log, open(os.path.join(OUT, "clear.json"), "w"), indent=1)
print("CLEAR", json.dumps(log), flush=True)
