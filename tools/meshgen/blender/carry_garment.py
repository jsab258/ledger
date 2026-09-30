"""A game-mesh garment carried from the body it was made on to another MetaHuman body of the same mesh.

    blender -b -P tools/meshgen/blender/carry_garment.py -- GAME.blend FROM_BODY.fbx TO_BODY.fbx OUT_DIR --garment ron_donkey --name darren_donkey

WHY, 30 September (Jafar, after an outside audit: one garment "proven on two approved bodies, Ron's and Darren's",
before any wardrobe). The MetaHuman bodies share one mesh, point for point (Ron's MH_RoccoP2 and Darren's MH_SamC5,
32,334 points each), so the change from one body to the other is known at every point of the skin. Each point of
the garment moves by the body's own change round it: the changes of the skin points near it, weighted by a
Gaussian of their distance (--sigma metres), so neighbouring points of the garment move together and loose parts
do not tear (carried by the nearest skin triangle alone, the jacket's loose sides came out in wings and ragged
seams on Darren; production/research/clothing-pipeline/RETOPOLOGY-AND-SKINNING-2026-09-30.md, section 5). Then any
point that ends nearer the new body than --clear is pushed out to it, the pushes smoothed over the garment so no
dent shows. Its UVs, textures, materials and "panel" pieces are kept; its SimMaxDistance colour is laid again from
the new body's hips (the same height above them as on the first body). Skin it afterwards with skin_garment.py on
TO_BODY.fbx.
OUT_DIR gets NAME.blend (the garment and the new body), NAME_static.fbx and carry.json.
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
GAME, FROM, TO, OUT = argv[:4]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


GARMENT = opt("--garment", "garment", str)
NAME = opt("--name", "carried", str)
SIG = opt("--sigma", 0.06)
CLEAR = opt("--clear", 0.005)
log = {"game": GAME, "from": FROM, "to": TO, "sigma": SIG, "clear": CLEAR}


def say(*a):
    print("CARRY", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=GAME)
g = bpy.data.objects[GARMENT]
sim_below = None
for o in list(bpy.data.objects):
    if o is not g:
        bpy.data.objects.remove(o, do_unlink=True)


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
me = g.data
P = np.array([tuple(g.matrix_world @ v.co) for v in me.vertices])
# the garment's pieces: the main surface is carried by the body; the pieces on it (the collar, the buttons) by the
# main surface's own move, so they stay where they sat on it (carried by the body, the collar followed the neck's
# skin and stood up in a funnel on Darren)
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
# the Gaussian's width follows the point's distance from the first body: a point close to the skin (the neckline,
# the shoulders) follows the skin just under it; a loose one (the skirt) the body round it (one width everywhere,
# 6 cm, left the neckline and collar up to 6 cm inside Darren's neck)
sb = bmesh.new()
sb.from_mesh(src.data)
sb.transform(src.matrix_world)
sbvh = BVHTree.FromBMesh(sb)
sb.free()
MIN_SIG = opt("--sigma-near", 0.012)
for i, p in enumerate(P):
    if not on_main[i]:
        continue
    dist = sbvh.find_nearest(Vector(p))[3] or 0.0
    sg = min(SIG, max(MIN_SIG, 1.2 * dist + 0.008))
    near = kd.find_range(Vector(p), 3.0 * sg)
    if len(near) < 8:
        near = kd.find_n(Vector(p), 32)
    idx = np.array([n[1] for n in near])
    d = np.array([n[2] for n in near])
    w = np.exp(-(d / sg) ** 2 / 2.0) + 1e-12
    w /= w.sum()
    Q[i] = p + (w[:, None] * dR[idx]).sum(0)
mkd = KDTree(int(on_main.sum()))
main_ids = np.where(on_main)[0]
for k, i in enumerate(main_ids):
    mkd.insert(Vector(P[i]), k)
mkd.balance()
dM = Q[main_ids] - P[main_ids]
PS = opt("--piece-sigma", 0.03)
for i in np.where(~on_main)[0]:
    near = mkd.find_n(Vector(P[i]), 48)
    idx = np.array([n[1] for n in near])
    d = np.array([n[2] for n in near])
    w = np.exp(-(d / PS) ** 2 / 2.0) + 1e-12
    w /= w.sum()
    Q[i] = P[i] + (w[:, None] * dM[idx]).sum(0)
log["meanMoveMm"] = round(float(np.linalg.norm(Q - P, axis=1).mean()) * 1000, 1)
# pushed out of the new body, the pushes smoothed (never less than a point needs)
bm = bmesh.new()
bm.from_mesh(dst.data)
bm.transform(dst.matrix_world)
bm.normal_update()
bvh = BVHTree.FromBMesh(bm)
# a point is pushed out only as far as it stood off the first body: the neckline and the collar's inner band run
# inside Ron's neck on the drape itself (hidden by his neck), and pushed clear on Darren they stood up in a funnel
sb2 = bmesh.new()
sb2.from_mesh(src.data)
sb2.transform(src.matrix_world)
sb2.normal_update()
sbvh2 = BVHTree.FromBMesh(sb2)
need = np.zeros_like(Q)
for i in range(len(Q)):
    h, n, _f, _d = bvh.find_nearest(Vector(Q[i]))
    if h is None:
        continue
    o = (Vector(Q[i]) - h).dot(n)
    h0, n0, _f0, _d0 = sbvh2.find_nearest(Vector(P[i]))
    was = (Vector(P[i]) - h0).dot(n0) if h0 is not None else CLEAR
    target = min(CLEAR, was)
    if o < target:
        need[i] = np.array(tuple(n)) * (target - o)
pushed = int((np.linalg.norm(need, axis=1) > 0).sum())
nm = np.linalg.norm(need, axis=1)
for lo_, hi_ in ((0.0, 0.8), (0.8, 1.0), (1.0, 1.2), (1.2, 1.4), (1.4, 1.55), (1.55, 1.7), (1.7, 2.0)):
    sel = (Q[:, 2] >= lo_) & (Q[:, 2] < hi_)
    say("DIAG z %.2f-%.2f main pushed>1cm %d max %.0fmm | pieces pushed>1cm %d max %.0fmm" % (
        lo_, hi_, int(((nm > 0.01) & sel & on_main).sum()), (nm[sel & on_main].max() * 1000) if (sel & on_main).any() else 0,
        int(((nm > 0.01) & sel & ~on_main).sum()), (nm[sel & ~on_main].max() * 1000) if (sel & ~on_main).any() else 0))
edges = np.array([e.vertices[:] for e in me.edges])
deg = np.bincount(edges.ravel(), minlength=len(Q)).astype(float)
push = need.copy()
for _ in range(opt("--push-smooth", 8, int)):
    acc = np.zeros_like(push)
    np.add.at(acc, edges[:, 0], push[edges[:, 1]])
    np.add.at(acc, edges[:, 1], push[edges[:, 0]])
    avg = acc / np.maximum(deg, 1)[:, None]
    bigger = np.linalg.norm(avg, axis=1) > np.linalg.norm(need, axis=1)
    push = np.where(bigger[:, None], avg, need)
Q = Q + push
log["pushedOut"] = pushed
log["mostPushMm"] = round(float(np.linalg.norm(push, axis=1).max()) * 1000, 1)
inv = g.matrix_world.inverted()
for i, v in enumerate(me.vertices):
    v.co = inv @ Vector(Q[i])
me.update()
# the loose part's colour laid again from the new hips
ca = me.color_attributes.get("SimMaxDistance")
if ca is not None:
    Pn = np.array([tuple(g.matrix_world @ v.co) for v in me.vertices])
    old = np.array([c.color[0] for c in ca.data])
    # where the colour began on the first body: the highest point that had any, carried by the hips' change
    start_from = P[old > 1e-4, 2].max() if (old > 1e-4).any() else None
    if start_from is not None:
        start_to = start_from + (hip(dst_arm).z - hip(src_arm).z)
        hem_z = Pn[:, 2].min()
        for i in range(len(Pn)):
            t = 0.0
            if Pn[i, 2] < start_to:
                t = (start_to - Pn[i, 2]) / max(1e-6, start_to - hem_z)
                t = t * t * (3 - 2 * t)
            ca.data[i].color = (t, t, t, 1.0)
        log["simBelow"] = round(float(start_to), 3)
bpy.data.objects.remove(src, do_unlink=True)
bpy.data.objects.remove(src_arm, do_unlink=True)
g.name = NAME
g.data.name = NAME
bpy.ops.object.select_all(action="DESELECT")
g.select_set(True)
bpy.context.view_layer.objects.active = g
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_static.fbx"), use_selection=True, object_types={"MESH"},
                         mesh_smooth_type="OFF", use_tspace=True, add_leaf_bones=False, colors_type="LINEAR")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "carry.json"), "w"), indent=1)
say("done", json.dumps(log))
