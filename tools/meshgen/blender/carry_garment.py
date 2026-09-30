"""A garment (or a drape) carried from the body it was made on to another MetaHuman body of the same mesh.

    blender -b -P tools/meshgen/blender/carry_garment.py -- IN.blend FROM_BODY.fbx TO_BODY.fbx OUT_DIR --garment ron_donkey --name darren_donkey
    blender -b -P tools/meshgen/blender/carry_garment.py -- DRAPE.blend FROM_BODY.fbx TO_BODY.fbx OUT_DIR --garment JacketRender,JacketSim --keep Jacket --name darren_drape

WHY, 30 September (Jafar, after an outside audit: one garment "proven on two approved bodies, Ron's and Darren's",
before any wardrobe). The MetaHuman bodies share one mesh, point for point (Ron's MH_RoccoP2 and Darren's MH_SamC5,
32,334 points each), so the change from one body to the other is known at every point of the skin. Each point of
the garment's main surface moves by the body's own change round it: the changes of the skin points near it,
weighted by a Gaussian whose width grows with the point's distance from the skin (--sigma-near to --sigma metres),
so a point close to the skin follows the skin under it and a loose one the body round it, and neighbouring points
move together (carried by the nearest skin triangle alone, the jacket's loose sides came out in wings and ragged
seams on Darren; production/research/clothing-pipeline/RETOPOLOGY-AND-SKINNING-2026-09-30.md, section 5). The
pieces on the main surface (a collar, buttons, a yoke, pockets) move with the main surface itself, so they stay
where they sat on it. A point is then pushed out of the new body, only as far as it stood off the first body (the
jacket's neckline and collar band lie inside Ron's neck on the drape itself, hidden by it; pushed clear on Darren
they stood up in a funnel), the pushes smoothed so no dent shows. UVs, materials and attributes are kept; a
SimMaxDistance colour is laid again from the new body's hips.

The first form carries a finished game mesh; the second a drape (the render mesh and its cloth mesh), so the game
mesh can be made again on the new body by retopo_garment.py with the same pattern (--keep leaves the sewn pattern
mesh as it is: its pattern and lengths give the same grid, the same UVs and the same textures' layout on both
bodies). Everything else in the file is replaced by the new body and its skeleton.
OUT_DIR gets NAME.blend, NAME_static.fbx (a single garment only) and carry.json.
"""
import json
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

argv = sys.argv[sys.argv.index("--") + 1:]
IN, FROM, TO, OUT = argv[:4]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


GARMENTS = opt("--garment", "garment", str).split(",")
KEEP = [k for k in opt("--keep", "", str).split(",") if k]
NAME = opt("--name", "carried", str)
SIG = opt("--sigma", 0.06)
MIN_SIG = opt("--sigma-near", 0.012)
CLEAR = opt("--clear", 0.005)
PS = opt("--piece-sigma", 0.03)
log = {"in": IN, "from": FROM, "to": TO, "garments": GARMENTS, "sigma": SIG, "clear": CLEAR}


def say(*a):
    print("CARRY", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=IN)
objs = [bpy.data.objects[n] for n in GARMENTS]
kept = [bpy.data.objects[n] for n in KEEP]
for o in list(bpy.data.objects):
    if o not in objs and o not in kept:
        bpy.data.objects.remove(o, do_unlink=True)
for o in objs + kept:
    mw = o.matrix_world.copy()
    o.parent = None
    o.matrix_world = mw


def load_body(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    arm = next(o for o in new if o.type == "ARMATURE")
    ms = sorted([o for o in new if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
    for o in ms[1:]:
        bpy.data.objects.remove(o, do_unlink=True)
    return ms[0], arm


src, src_arm = load_body(FROM)
dst, dst_arm = load_body(TO)
R = np.array([tuple(src.matrix_world @ v.co) for v in src.data.vertices])
D = np.array([tuple(dst.matrix_world @ v.co) for v in dst.data.vertices])
if R.shape != D.shape:
    raise SystemExit("CARRY the two bodies are not the same mesh (%d and %d points)" % (len(R), len(D)))
hip = lambda a: (a.matrix_world @ a.pose.bones["thigh_l"].head + a.matrix_world @ a.pose.bones["thigh_r"].head) / 2  # noqa: E731
log["hipFrom"], log["hipTo"] = [round(c, 3) for c in hip(src_arm)], [round(c, 3) for c in hip(dst_arm)]
dR = D - R
kd = KDTree(len(R))
for i, c in enumerate(R):
    kd.insert(Vector(c), i)
kd.balance()


def body_bvh(o):
    b = bmesh.new()
    b.from_mesh(o.data)
    b.transform(o.matrix_world)
    b.normal_update()
    t = BVHTree.FromBMesh(b)
    b.free()
    return t


SRC_BVH, DST_BVH = body_bvh(src), body_bvh(dst)


def carry(g):
    me = g.data
    P = np.array([tuple(g.matrix_world @ v.co) for v in me.vertices])
    gbm = bmesh.new()
    gbm.from_mesh(me)
    gbm.verts.ensure_lookup_table()
    comp = np.full(len(gbm.verts), -1)
    for v0 in gbm.verts:
        if comp[v0.index] >= 0:
            continue
        comp[v0.index] = v0.index
        st = [v0]
        while st:
            v = st.pop()
            for e in v.link_edges:
                w_ = e.other_vert(v)
                if comp[w_.index] < 0:
                    comp[w_.index] = v0.index
                    st.append(w_)
    gbm.free()
    main = np.bincount(comp).argmax()
    on_main = comp == main
    Q = P.copy()
    for i, p in enumerate(P):
        if not on_main[i]:
            continue
        dist = SRC_BVH.find_nearest(Vector(p))[3] or 0.0
        sg = min(SIG, max(MIN_SIG, 1.2 * dist + 0.008))
        near = kd.find_range(Vector(p), 3.0 * sg)
        if len(near) < 8:
            near = kd.find_n(Vector(p), 32)
        idx = np.array([n[1] for n in near])
        d = np.array([n[2] for n in near])
        w = np.exp(-(d / sg) ** 2 / 2.0) + 1e-12
        w /= w.sum()
        Q[i] = p + (w[:, None] * dR[idx]).sum(0)
    # pushed out of the new body only as far as the point stood off the first (the main surface; its pieces follow)
    need = np.zeros_like(Q)
    for i in np.where(on_main)[0]:
        h, n, _f, _d = DST_BVH.find_nearest(Vector(Q[i]))
        if h is None:
            continue
        o = (Vector(Q[i]) - h).dot(n)
        h0, n0, _f0, _d0 = SRC_BVH.find_nearest(Vector(P[i]))
        was = (Vector(P[i]) - h0).dot(n0) if h0 is not None else CLEAR
        target = min(CLEAR, was)
        if o < target:
            need[i] = np.array(tuple(n)) * (target - o)
    edges = np.array([e.vertices[:] for e in me.edges])
    deg = np.bincount(edges.ravel(), minlength=len(Q)).astype(float)
    push = need.copy()
    for _ in range(opt("--push-smooth", 8, int)):
        acc = np.zeros_like(push)
        np.add.at(acc, edges[:, 0], push[edges[:, 1]])
        np.add.at(acc, edges[:, 1], push[edges[:, 0]])
        avg = acc / np.maximum(deg, 1)[:, None]
        bigger = np.linalg.norm(avg, axis=1) > np.linalg.norm(need, axis=1)
        push = np.where((bigger & on_main)[:, None], avg, need)
    Q = Q + push
    # the pieces on the main surface move with it
    main_ids = np.where(on_main)[0]
    if (~on_main).any():
        mkd = KDTree(len(main_ids))
        for k, i in enumerate(main_ids):
            mkd.insert(Vector(P[i]), k)
        mkd.balance()
        dM = Q[main_ids] - P[main_ids]
        for i in np.where(~on_main)[0]:
            near = mkd.find_n(Vector(P[i]), 48)
            idx = np.array([n[1] for n in near])
            d = np.array([n[2] for n in near])
            w = np.exp(-(d / PS) ** 2 / 2.0) + 1e-12
            w /= w.sum()
            Q[i] = P[i] + (w[:, None] * dM[idx]).sum(0)
    inv = g.matrix_world.inverted()
    for i, v in enumerate(me.vertices):
        v.co = inv @ Vector(Q[i])
    me.update()
    # the loose part's colour laid again from the new hips
    ca = me.color_attributes.get("SimMaxDistance")
    out = {"points": len(P), "meanMoveMm": round(float(np.linalg.norm(Q - P, axis=1).mean()) * 1000, 1),
           "pushedOut": int((np.linalg.norm(need, axis=1) > 0).sum()), "mostPushMm": round(float(np.linalg.norm(push, axis=1).max()) * 1000, 1)}
    if ca is not None:
        old = np.array([c.color[0] for c in ca.data]) if ca.domain == "POINT" else None
        if old is not None and (old > 1e-4).any():
            start_to = P[old > 1e-4, 2].max() + (hip(dst_arm).z - hip(src_arm).z)
            hem_z = Q[:, 2].min()
            for i in range(len(Q)):
                t = 0.0
                if Q[i, 2] < start_to:
                    t = (start_to - Q[i, 2]) / max(1e-6, start_to - hem_z)
                    t = t * t * (3 - 2 * t)
                ca.data[i].color = (t, t, t, 1.0)
            out["simBelow"] = round(float(start_to), 3)
    return out


for g in objs:
    log[g.name] = carry(g)
    say(g.name, json.dumps(log[g.name]))
bpy.data.objects.remove(src, do_unlink=True)
bpy.data.objects.remove(src_arm, do_unlink=True)
if len(objs) == 1:
    g = objs[0]
    g.name = NAME
    g.data.name = NAME
    bpy.ops.object.select_all(action="DESELECT")
    g.select_set(True)
    bpy.context.view_layer.objects.active = g
    bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_static.fbx"), use_selection=True, object_types={"MESH"},
                             mesh_smooth_type="OFF", use_tspace=True, add_leaf_bones=False, colors_type="LINEAR")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "carry.json"), "w"), indent=1)
say("done", NAME)
