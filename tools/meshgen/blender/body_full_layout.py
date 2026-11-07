"""A built MetaHuman's body given back the full point layout, so carry_garment.py and carry_footwear.py can use it.

    blender -b --factory-startup -P tools/meshgen/blender/body_full_layout.py -- TEMPLATE_Body.fbx BUILT_BodyMesh.fbx OUT_Body.fbx [--sigma 0.03]

WHY, 7 November 2026. The carry tools need two bodies with the same points. An Optimized build's body has fewer (faces
under the default garment's hidden face map are cut: Darren's MH_SamS6 25,328 of 32,334), and the older export of the
same character may be another body altogether (MH_SamC5's pelvis 64 mm from S6's, though the notes called them the same;
Darren's clothes carried onto C5 showed skin in the game). So: match each built point to the template's by the shared
UVs, take the built position where a point exists, and fill the cut points with a Gaussian of their neighbours' moves.
Bones go to the built skeleton's rest places; weights and faces stay the template's. Lower levels of detail follow their
nearest LOD0 point. Writes OUT_Body.fbx and OUT_Body.json (matched, filled, the moves).
"""
import json
import os
import sys

import bpy
import numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree

argv = sys.argv[sys.argv.index("--") + 1:]
TEMPLATE, BUILT, OUT = argv[:3]
SIGMA = float(argv[argv.index("--sigma") + 1]) if "--sigma" in argv else 0.03


def load(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    return [o for o in bpy.data.objects if o not in before]


def world_co(o):
    n = len(o.data.vertices)
    co = np.zeros(n * 3)
    o.data.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    m = np.array(o.matrix_world)
    return co @ m[:3, :3].T + m[:3, 3]


def uv_per_point(o):
    """One UV per point (the first loop's) and every loop's, in the DiffuseUV layer or the first."""
    me = o.data
    layer = me.uv_layers.get("DiffuseUV") or me.uv_layers[0]
    loops = np.zeros(len(me.loops), dtype=int)
    me.loops.foreach_get("vertex_index", loops)
    uv = np.zeros(len(me.loops) * 2)
    layer.data.foreach_get("uv", uv)
    return loops, uv.reshape(-1, 2)


tpl = load(TEMPLATE)
tpl_arm = next(o for o in tpl if o.type == "ARMATURE")
tpl_meshes = sorted((o for o in tpl if o.type == "MESH"), key=lambda o: -len(o.data.vertices))
built = load(BUILT)
bu_arm = next(o for o in built if o.type == "ARMATURE")
bu = max((o for o in built if o.type == "MESH"), key=lambda o: len(o.data.vertices))
t0 = tpl_meshes[0]

tco, bco = world_co(t0), world_co(bu)
tl, tuv = uv_per_point(t0)
bl, buv = uv_per_point(bu)

# Match by UV, a loop at a time: a point on a UV seam has several UVs, any one of which identifies it.
kd = KDTree(len(tuv))
for i, u in enumerate(tuv):
    kd.insert((u[0], u[1], 0.0), i)
kd.balance()
match = {}
worst_uv = 0.0
for li, u in enumerate(buv):
    bp = int(bl[li])
    if bp in match:
        continue
    _, idx, dist = kd.find((u[0], u[1], 0.0))
    worst_uv = max(worst_uv, dist)
    if dist < 2e-4:
        match[bp] = int(tl[idx])
pairs = np.array(sorted(match.items()))
moves = np.full((len(tco), 3), np.nan)
moves[pairs[:, 1]] = bco[pairs[:, 0]] - tco[pairs[:, 1]]
known = ~np.isnan(moves[:, 0])
ki = np.where(known)[0]
fi = np.where(~known)[0]

# Fill the cut points: a Gaussian of the known moves nearby, wide enough to bridge a whole cut trunk.
kdk = KDTree(len(ki))
for j, i in enumerate(ki):
    kdk.insert(Vector(tco[i]), j)
kdk.balance()
for i in fi:
    hits = kdk.find_n(Vector(tco[i]), 48)
    nearest = hits[0][2]
    s = max(SIGMA, nearest)
    w = np.array([np.exp(-0.5 * (h[2] / s) ** 2) for h in hits])
    moves[i] = (w[:, None] * moves[ki[[h[1] for h in hits]]]).sum(0) / w.sum()
newco = tco + moves

# Lower levels follow their nearest LOD0 point.
kd0 = KDTree(len(tco))
for i, c in enumerate(tco):
    kd0.insert(Vector(c), i)
kd0.balance()
for o in tpl_meshes[1:]:
    c = world_co(o)
    m = np.array([moves[kd0.find(Vector(p))[1]] for p in c])
    inv = np.linalg.inv(np.array(o.matrix_world))
    d = c + m
    d = d @ inv[:3, :3].T + inv[:3, 3]
    o.data.vertices.foreach_set("co", d.ravel())
    o.data.update()
inv = np.linalg.inv(np.array(t0.matrix_world))
d = newco @ inv[:3, :3].T + inv[:3, 3]
t0.data.vertices.foreach_set("co", d.ravel())
t0.data.update()

# The skeleton's rest places from the built body.
want = {b.name: (bu_arm.matrix_world @ b.head_local, bu_arm.matrix_world @ b.tail_local) for b in bu_arm.data.bones}
bpy.ops.object.select_all(action="DESELECT")
bpy.context.view_layer.objects.active = tpl_arm
tpl_arm.select_set(True)
bpy.ops.object.mode_set(mode="EDIT")
minv = tpl_arm.matrix_world.inverted()
moved = 0
for eb in tpl_arm.data.edit_bones:
    if eb.name in want:
        eb.use_connect = False
for eb in tpl_arm.data.edit_bones:
    if eb.name in want:
        eb.head = minv @ want[eb.name][0]
        eb.tail = minv @ want[eb.name][1]
        moved += 1
bpy.ops.object.mode_set(mode="OBJECT")

for o in built:
    bpy.data.objects.remove(o, do_unlink=True)
base = os.path.basename(OUT)[:-4]
for o in tpl_meshes:
    suffix = o.name[o.name.rfind("_LOD"):] if "_LOD" in o.name else ""
    o.name = base + suffix
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.fbx(filepath=OUT, use_selection=True, add_leaf_bones=False, bake_anim=False, mesh_smooth_type="FACE",
                         armature_nodetype="NULL", apply_unit_scale=True, global_scale=1.0)
d = np.linalg.norm(moves, axis=1)
rec = {"template": TEMPLATE, "built": BUILT, "points": len(tco), "builtPoints": len(bco), "matched": int(known.sum()),
       "unmatchedBuilt": len(bco) - len(match), "filled": len(fi), "worstUv": worst_uv, "bonesMoved": moved,
       "moveMm": {"mean": float(d.mean() * 1000), "p95": float(np.percentile(d, 95) * 1000), "max": float(d.max() * 1000)},
       "top": float(newco[:, 2].max()), "sigma": SIGMA}
json.dump(rec, open(OUT[:-4] + ".json", "w"), indent=1)
print("BODY_FULL_LAYOUT " + json.dumps(rec))
