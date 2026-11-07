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

THE HEAD, 7 November 2026 (Darren's slits at the breastbone, diagnosed the same day; his yes for a third try). A
MetaHuman's head mesh runs down the chest and is not in the body file. --head FACE_DNA.uasset reads it from the
wearer's face DNA (dna_mesh.py) and, on the front only, moves the cloth forward until it stands --head-clear in front
of the head wherever the head is below --head-below; the amount is a soft spread (--head-spread metres) so no step
shows. Both surfaces are drawn into a 1 mm front-on grid, since the head's lower edge can poke between cloth points.
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
RIM_CAP = opt("--rim-cap", 0.0)
RIM_FADE = opt("--rim-fade", 0.03)
HEAD = opt("--head", "", str)
HEAD_CLEAR = opt("--head-clear", 0.007)
HEAD_BELOW = opt("--head-below", 1.56)
HEAD_SPREAD = opt("--head-spread", 0.02)
if HEAD:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    import dna_mesh  # noqa: E402
    _face = dna_mesh.meshes(HEAD)[0]
    HEAD_P, HEAD_T = dna_mesh.to_blender(_face["P"]), _face["tri"]

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


def triangles(mesh):
    mesh.calc_loop_triangles()
    return [tuple(t.vertices) for t in mesh.loop_triangles]


def front_grid(co, tri, xs, zs):
    """The frontmost y (front is -Y) of a surface in each grid cell, nan where it has none."""
    H = np.full((len(zs), len(xs)), np.nan)
    dx, dz = xs[1] - xs[0], zs[1] - zs[0]
    a, b, c = co[tri[:, 0]], co[tri[:, 1]], co[tri[:, 2]]
    lo, hi = np.minimum(np.minimum(a, b), c), np.maximum(np.maximum(a, b), c)
    keep = (hi[:, 0] >= xs[0]) & (lo[:, 0] <= xs[-1]) & (hi[:, 2] >= zs[0]) & (lo[:, 2] <= zs[-1])
    for A, B, C in zip(a[keep], b[keep], c[keep]):
        i0 = max(int(np.floor((min(A[0], B[0], C[0]) - xs[0]) / dx)), 0)
        i1 = min(int(np.ceil((max(A[0], B[0], C[0]) - xs[0]) / dx)), len(xs) - 1)
        j0 = max(int(np.floor((min(A[2], B[2], C[2]) - zs[0]) / dz)), 0)
        j1 = min(int(np.ceil((max(A[2], B[2], C[2]) - zs[0]) / dz)), len(zs) - 1)
        d = (B[0] - A[0]) * (C[2] - A[2]) - (C[0] - A[0]) * (B[2] - A[2])
        if abs(d) < 1e-14:
            continue
        X, Z = np.meshgrid(xs[i0:i1 + 1], zs[j0:j1 + 1])
        u = ((X - A[0]) * (C[2] - A[2]) - (C[0] - A[0]) * (Z - A[2])) / d
        v = ((B[0] - A[0]) * (Z - A[2]) - (X - A[0]) * (B[2] - A[2])) / d
        m = (u >= 0) & (v >= 0) & (1 - u - v >= 0)
        Y = A[1] + u * (B[1] - A[1]) + v * (C[1] - A[1])
        sub = H[j0:j1 + 1, i0:i1 + 1]
        sub[m] = np.fmin(sub[m], Y[m])
    return H


def clear_head(co, tri):
    """The front of the cloth moved forward of the head's lower edge, softly; the moved points and the clearance reported."""
    start = co.copy()
    xs, zs = np.arange(-0.2, 0.2001, 0.001), np.arange(HEAD_BELOW - 0.12, HEAD_BELOW + 0.04, 0.001)
    H = front_grid(HEAD_P, HEAD_T, xs, zs)
    low = np.broadcast_to(zs[:, None] < HEAD_BELOW, H.shape)
    gap0 = H - front_grid(co, tri, xs, zs)
    idx = np.where((co[:, 1] < -0.02) & (co[:, 2] > HEAD_BELOW - 0.18) & (co[:, 2] < HEAD_BELOW + 0.06))[0]
    with np.errstate(invalid="ignore"):
        for _ in range(6):
            short = (front_grid(co, tri, xs, zs) - H) + HEAD_CLEAR
            m = (short > 0) & low
            if not m.any():
                break
            a, b = np.where(m)
            cells, amount = np.c_[xs[b], zs[a]], short[a, b]
            dist = np.linalg.norm(co[idx][:, [0, 2]][:, None, :] - cells[None, :, :], axis=2)
            co[idx, 1] -= (amount[None, :] * np.exp(-0.5 * (dist / HEAD_SPREAD) ** 2)).max(axis=1)
    gap = H - front_grid(co, tri, xs, zs)
    moved = np.linalg.norm(co - start, axis=1)
    return co, {"points": len(HEAD_P), "beforeMinMm": round(float(np.nanmin(gap0[low])) * 1000, 1),
                "afterMinMm": round(float(np.nanmin(gap[low])) * 1000, 1), "movedOver0_5mm": int((moved > 0.0005).sum()),
                "mostMovedMm": round(float(moved.max()) * 1000, 1)}


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
    if HEAD:
        Q, log["head"] = clear_head(Q, np.array([t for t in triangles(me)]))
    if RIM_CAP:
        # the neck ring's high corners at the sides read as two points in the film (Ron, build 76db411): its height eased
        # toward the cap, softly, so the ring keeps its order and no step shows
        base = RIM_CAP - RIM_FADE
        ease = (Q[:, 2] > base) & (np.abs(Q[:, 0]) < 0.16)
        rim_before = float(Q[ease, 2].max())
        Q[ease, 2] = base + RIM_FADE * (1 - np.exp(-(Q[ease, 2] - base) / RIM_FADE))
        log["rim"] = {"points": int(ease.sum()), "topBefore": round(rim_before, 4), "topAfter": round(float(Q[ease, 2].max()), 4)}
    push = Q - P
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
