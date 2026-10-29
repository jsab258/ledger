"""A skinned garment's limb weights mended from the body where the binder strayed from it.

    blender -b SKINNED.blend -P tools/meshgen/blender/mend_limb_weights.py -- OUT_DIR NAME BODY_OBJECT [--limb lowerarm_r]
            [--from 0.45] [--to 1.12] [--radius 0.09] [--max-influences 8] [--all] [--end BONE] [--stray PREFIX]

WHY, 30 October 2026 (his order C9; Tom's jacket with built cuffs, withdrawn on 29 October after holes and a right
sleeve almost gone in the packaged game): the per-pose check (garment_pose_check.py) put 341 of its points through
the right forearm in a walking stride against none for drape 19's jacket, and the weights showed why: on the right
forearm, 60 to 80% of the way from the elbow, the jacket's points took lowerarm_twist_02_r (the bone a third of the
way down) where the body's own skin there, the left sleeve and drape 19's take lowerarm_twist_01_r. The skill's
rule is the body's weights (game-garment, step 9), so on the named limb each point whose strongest bone is not the
body's strongest at its nearest skin takes the body's weights there, interpolated over that skin triangle; every
other point keeps the binder's. SKINNED.blend is skin_garment.py's NAME_skinned.blend (garment, armature, body).
OUT_DIR gets NAME_skinned.fbx (the same export as skin_garment.py), NAME_skinned.blend and mend.json.
"""
import json
import os
import sys

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
OUT, NAME, BODY = argv[:3]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


LIMB = opt("--limb", "lowerarm_r", str)
T0, T1, RADIUS = opt("--from", 0.45), opt("--to", 1.12), opt("--radius", 0.09)
MAXI = opt("--max-influences", 8, int)
# --all: every point of the limb takes the body's weights, not only those whose strongest bone strays
ALL = "--all" in argv
# --end BONE: the limb runs from LIMB's head to this bone's (default the hand); --stray PREFIX: only points whose
# strongest bone starts with PREFIX and is not the body's (30 October: lower-arm weights reaching up the upper arm)
END = opt("--end", "", str)
STRAY = opt("--stray", "", str)
os.makedirs(OUT, exist_ok=True)

g = bpy.data.objects[NAME]
body = bpy.data.objects[BODY]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
side = LIMB.rsplit("_", 1)[1]
elbow = arm.matrix_world @ arm.data.bones[LIMB].head_local
hand = arm.matrix_world @ arm.data.bones[END or "hand_" + side].head_local
axis = hand - elbow
length = axis.length
axis.normalize()

# the body's skin as triangles, in the world, with each corner's weights by bone name
bm = body.data
bm.calc_loop_triangles()
bw = body.matrix_world
verts = [bw @ v.co for v in bm.vertices]
tris = [tuple(t.vertices) for t in bm.loop_triangles]
tree = BVHTree.FromPolygons(verts, tris)
bnames = {gr.index: gr.name for gr in body.vertex_groups}
bweights = [{bnames[e.group]: e.weight for e in v.groups if e.weight > 1e-4} for v in bm.vertices]

gnames = {gr.index: gr.name for gr in g.vertex_groups}
gw = g.matrix_world
changed, judged, was = 0, 0, {}
new_weights = {}
for v in g.data.vertices:
    p = gw @ v.co
    t = (p - elbow).dot(axis) / length
    r = ((p - elbow) - axis * (p - elbow).dot(axis)).length
    if not (T0 <= t <= T1 and r <= RADIUS) or not v.groups:
        continue
    judged += 1
    hit, _n, fi, _d = tree.find_nearest(p)
    if hit is None:
        continue
    a, b, c = (verts[i] for i in tris[fi])
    # barycentric weights of the nearest point in its triangle
    v0, v1, v2 = b - a, c - a, hit - a
    d00, d01, d11, d20, d21 = v0.dot(v0), v0.dot(v1), v1.dot(v1), v2.dot(v0), v2.dot(v1)
    den = d00 * d11 - d01 * d01
    if abs(den) < 1e-12:
        continue
    wb = (d11 * d20 - d01 * d21) / den
    wc = (d00 * d21 - d01 * d20) / den
    wa = 1.0 - wb - wc
    mix = {}
    for corner, share in zip(tris[fi], (wa, wb, wc)):
        for bone, w in bweights[corner].items():
            mix[bone] = mix.get(bone, 0.0) + max(0.0, share) * w
    if not mix:
        continue
    body_best = max(mix, key=mix.get)
    own_best = gnames[max(v.groups, key=lambda e: e.weight).group]
    if own_best == body_best and not ALL:
        continue
    if STRAY and not own_best.startswith(STRAY):
        continue
    top = sorted(mix.items(), key=lambda kv: -kv[1])[:MAXI]
    s = sum(w for _b, w in top)
    new_weights[v.index] = {bone: w / s for bone, w in top}
    was[own_best + " -> " + body_best] = was.get(own_best + " -> " + body_best, 0) + 1
    changed += 1

for i, ws in new_weights.items():
    for gr in g.vertex_groups:
        gr.remove([i])
    for bone, w in ws.items():
        gr = g.vertex_groups.get(bone) or g.vertex_groups.new(name=bone)
        gr.add([i], w, "REPLACE")

print("MEND limb=%s judged=%d changed=%d %s" % (LIMB, judged, changed, json.dumps(was)), flush=True)


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uv_order import maps_layout_first  # noqa: E402

reordered = maps_layout_first(g)
print("MEND uv layers %s%s" % ([u.name for u in g.data.uv_layers], " (reordered)" if reordered else ""), flush=True)
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
g.select_set(True)
bpy.context.view_layer.objects.active = arm
body.select_set(False)
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_skinned.fbx"), use_selection=True,
                         object_types={"ARMATURE", "MESH"}, add_leaf_bones=False, mesh_smooth_type="OFF", use_tspace=True,
                         colors_type="LINEAR", bake_anim=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_skinned.blend"))
json.dump({"limb": LIMB, "all": ALL, "uvReordered": reordered, "from": T0, "to": T1, "radius": RADIUS, "judged": judged, "changed": changed, "was": was},
          open(os.path.join(OUT, "mend.json"), "w"), indent=1)
