"""A close garment tested as the game wears it, skinned to the body: arms down, arms raised, walking, sitting.

    blender -b -P tools/meshgen/blender/pose_skinned.py -- FINISHED.blend OUT_DIR --render CardiganRender [--poses down,up,walk,sit]

(Written 29 September for Sheila's cardigan, from pose_trousers.py: a close
knit is skinned from the body with no cloth, the research says,
SHEILA-CLOTHES-2026-09-29.md. Its weights are the body's own, each point
those of the nearest place on her skin, smoothed; the small pieces sewn on it
(bands, buttons, the collar) take the weights of the knit's nearest point,
so nothing parts from it; the body the garment always covers is hidden in
the pictures, as the game hides it. What follows is pose_trousers.py's own
note, most of which applies.)

WHY, 29 September (the clothing session; Jafar's rule: every garment tested
walking, sitting and with arms raised before it goes to the builder; the
arms do not move trousers). Close garments are skinned in games, not
simulated (production/research/clothing-pipeline/TROUSERS-AND-CAP-2026-09-29.md),
so the test is the skinning: the finished render mesh takes the body's own
skin weights (each point those of the nearest place on the body, the arms'
and hands' taken off, smoothed over the cloth), rides the skeleton into each
pose (tailor.make_pose), and is measured there against the posed body
without its parted thighs (the true body): points of the trousers inside
it, and how far the skinning stretches the cloth's edges.

OUT_DIR gets pose-NAME-front.png, -side.png, -three-quarter.png and
pose-test.json.
"""
import json
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, OUT = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


POSES = opt("--poses", "down,up,walk,sit", str).split(",")
RENDER = opt("--render", "TrousersRender", str)


def say(*a):
    print("POSE", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=BLEND)
garment = bpy.data.objects[RENDER]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = next(o for o in bpy.data.objects if o.type == "MESH" and o is not garment
            and any(m.type == "ARMATURE" for m in o.modifiers))
for o in list(bpy.data.objects):
    if o.type == "MESH" and o not in (garment, body):
        bpy.data.objects.remove(o, do_unlink=True)
if body.data.shape_keys and body.data.shape_keys.key_blocks.get("apart"):
    body.data.shape_keys.key_blocks["apart"].value = 0.0         # the true body, thighs touching
body.hide_render = False
body.hide_set(False)
if arm.animation_data:
    arm.animation_data_clear()
for pb in arm.pose.bones:
    pb.rotation_mode = "QUATERNION"
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()

# ---- the body's own weights, the small pieces glued to the garment -------------------------------------

for g in list(garment.vertex_groups):
    garment.vertex_groups.remove(g)
dt = garment.modifiers.new("Weights", "DATA_TRANSFER")
dt.object = body
dt.use_vert_data = True
dt.data_types_verts = {"VGROUP_WEIGHTS"}
dt.vert_mapping = "POLYINTERP_NEAREST"
dt.layers_vgroup_select_src = "ALL"
dt.layers_vgroup_select_dst = "NAME"
bpy.ops.object.select_all(action="DESELECT")
garment.select_set(True)
bpy.context.view_layer.objects.active = garment
bpy.ops.object.datalayout_transfer(modifier="Weights")
bpy.ops.object.modifier_apply(modifier="Weights")
bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
bpy.ops.object.vertex_group_smooth(group_select_mode="ALL", factor=0.5, repeat=opt("--smooth", 6, int))
bpy.ops.object.vertex_group_normalize_all(group_select_mode="ALL", lock_active=False)
bpy.ops.object.mode_set(mode="OBJECT")
from mathutils.kdtree import KDTree
bm_ = bmesh.new()
bm_.from_mesh(garment.data)
comp = [-1] * len(bm_.verts)
sizes = []
bm_.verts.ensure_lookup_table()
for v0 in bm_.verts:
    if comp[v0.index] >= 0:
        continue
    cid, stack, n_ = len(sizes), [v0], 0
    comp[v0.index] = cid
    while stack:
        v = stack.pop()
        n_ += 1
        for e in v.link_edges:
            o = e.other_vert(v)
            if comp[o.index] < 0:
                comp[o.index] = cid
                stack.append(o)
    sizes.append(n_)
bm_.free()
main = int(np.argmax(sizes))
gco = np.array([garment.matrix_world @ v.co for v in garment.data.vertices])
cloth_ids = [i for i, c in enumerate(comp) if c == main]
kd = KDTree(len(cloth_ids))
for k, i in enumerate(cloth_ids):
    kd.insert(Vector(gco[i]), k)
kd.balance()
names = {g.index: g for g in garment.vertex_groups}
wmap = {i: [(g.group, g.weight) for g in garment.data.vertices[i].groups] for i in cloth_ids}
glued = 0
for i, c in enumerate(comp):
    if c == main:
        continue
    _p, k, _d = kd.find(Vector(gco[i]))
    for g in list(garment.data.vertices[i].groups):
        names[g.group].remove([i])
    for gi, w in wmap[cloth_ids[k]]:
        names[gi].add([i], w, "REPLACE")
    glued += 1
# the body the garment always covers, hidden in the pictures (not in the measure)
covered = body.vertex_groups.get("covered") or body.vertex_groups.new(name="covered")
bco = np.array([body.matrix_world @ v.co for v in body.data.vertices])
kd2 = KDTree(len(cloth_ids))
for k, i in enumerate(cloth_ids):
    kd2.insert(Vector(gco[i]), k)
kd2.balance()
# only well inside the garment's edges (the first cardigan review: white at
# the hips below the hem, at the neck, between cuff and hand, where the body
# was hidden past the cardigan's edge): a body point is hidden if the garment
# is within 3 cm of it and that garment point is 4 cm or more from an edge
_bmg = bmesh.new()
_bmg.from_mesh(garment.data)
_edge_pts = [garment.matrix_world @ v.co for v in _bmg.verts if v.is_boundary and comp[v.index] == main]
_bmg.free()
kd3 = KDTree(max(1, len(_edge_pts)))
for k, q in enumerate(_edge_pts):
    kd3.insert(q, k)
kd3.balance()
deep_cloth = [i for i in cloth_ids if not _edge_pts or kd3.find(Vector(gco[i]))[2] > opt("--edge-keep", 0.04)]
kd2 = KDTree(max(1, len(deep_cloth)))
for k, i in enumerate(deep_cloth):
    kd2.insert(Vector(gco[i]), k)
kd2.balance()
ids_cov = [i for i, q in enumerate(bco) if kd2.find(Vector(q))[2] < opt("--cover", 0.03)]
covered.add(ids_cov, 1.0, "REPLACE")
mask = body.modifiers.new("Covered", "MASK")
mask.vertex_group = "covered"
mask.invert_vertex_group = True
mask.show_viewport = False
log_rigid = glued
side_cut = 0
am = garment.modifiers.new("Armature", "ARMATURE")
am.object = arm

bm = bmesh.new()
bm.from_mesh(garment.data)
EDGES = np.array([[e.verts[0].index, e.verts[1].index] for e in bm.edges])
bm.free()
REST = tailor.coords(garment)
L0 = np.linalg.norm(REST[EDGES[:, 1]] - REST[EDGES[:, 0]], axis=1)
log = {"blend": BLEND, "poses": {}, "gluedToCloth": log_rigid, "bodyHidden": len(ids_cov)}
grey = tailor.material("M_Body", (0.5, 0.5, 0.5))
body.data.materials.clear()
body.data.materials.append(grey)

for name in POSES:
    for pb in arm.pose.bones:
        pb.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()
    tailor.make_pose(arm, name)
    bpy.context.view_layer.update()
    co = tailor.coords(garment)
    bev = tailor.evaluated_copy(body, "BodyPosed")
    bvh = tailor.bvh_of(bev)
    bpy.data.objects.remove(bev, do_unlink=True)
    deep = np.array([tailor.depth_inside(bvh, Vector(p)) for p in co])
    ln = np.linalg.norm(co[EDGES[:, 1]] - co[EDGES[:, 0]], axis=1)
    r = ln / np.maximum(L0, 1e-9)
    ok = L0 > 1e-6
    lo_z, hi_z = float(co[:, 2].min()), float(co[:, 2].max())
    worst = [[round(float(c), 3) for c in co[i]] for i in np.argsort(-deep)[:4] if deep[i] > 0.003]
    log["poses"][name] = {"insideOver3mm": int((deep > 0.003).sum()), "deepestMm": round(float(deep.max()) * 1000, 1),
                          "whereDeepest": worst,
                          "stretch95": round(float(np.percentile(r[ok], 95)), 3), "stretchMax": round(float(r[ok].max()), 2),
                          "squeeze5": round(float(np.percentile(r[ok], 5)), 3)}
    say(name, json.dumps(log["poses"][name]))
    mid = Vector((float(co[:, 0].mean()), float(co[:, 1].mean()), 0.5 * (lo_z + hi_z)))
    tailor.pictures(os.path.join(OUT, "pose-%s" % name), mid,
                    views=(("front", (0, -3.2, 0.2)), ("side", (3.2, 0, 0.2)), ("three-quarter", (2.2, -2.3, 0.4))))
json.dump(log, open(os.path.join(OUT, "pose-test.json"), "w"), indent=1)
say("done")
