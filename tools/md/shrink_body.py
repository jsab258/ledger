"""Thinned copies of a body for Marvelous Designer: every point of the skin drawn towards its nearest bone by a
factor, the skeleton and the joints' places unchanged, so the body keeps its height, pose and the line of its arms.

    blender -b -P tools/md/shrink_body.py -- BODY.fbx OUT_PREFIX 0.8 0.85 0.9 0.95

OUT_PREFIX-k0.80.fbx and so on (centimetres, mesh and skeleton, as tools/md/pad_body.py writes them).

WHY, 2 October (the jacket proof). Our MetaHuman bodies get no arrangement points by script, so the jacket's pieces
are placed on Marvelous's stock man and the stock man is then replaced by our body before draping
(tools/md/jobs/swap_body.py). Ron is a much bigger man: his chest and arms came through the placed pieces, and the
distance a piece sits off the body cannot be set (SetArrangementPosition moves nothing; research
MD-LAPEL-FOLD-TURNED-2026-10-02.md). So the drape starts on a thinned Ron that fits inside the placed pieces, and is
carried to his full size by swapping in fuller copies a few millimetres at a time, the cloth settling at each, as
Marvelous itself morphs a garment from one avatar to the next. Drawing each point towards its own bone (not scaling
the whole body) keeps the arms where the sleeves were placed round them.
"""
import sys

import bpy
from mathutils import Vector
from mathutils.geometry import intersect_point_line

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, PREFIX = argv[0], argv[1]
KS = [float(k) for k in argv[2:]]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = sorted([o for o in bpy.data.objects if o.type == "MESH"], key=lambda o: -len(o.data.vertices))[0]
J = lambda n: arm.matrix_world @ arm.pose.bones[n].head  # noqa: E731
CHAINS = [["pelvis", "spine_01", "spine_02", "spine_03", "spine_04", "spine_05", "neck_01", "neck_02", "head"]]
for s in "lr":
    CHAINS += [["clavicle_" + s, "upperarm_" + s, "lowerarm_" + s, "hand_" + s, "middle_metacarpal_" + s, "middle_01_" + s],
               ["pelvis", "thigh_" + s, "calf_" + s, "foot_" + s, "ball_" + s]]
segs = []
for ch in CHAINS:
    pts = [J(n) for n in ch if n in arm.pose.bones]
    segs += list(zip(pts, pts[1:]))
head = J("head")
segs.append((head, head + Vector((0, 0, 0.12))))
mw = body.matrix_world
inv = mw.inverted()
rest = [mw @ v.co for v in body.data.vertices]
target = []
for w in rest:
    best = None
    for a, b in segs:
        q, t = intersect_point_line(w, a, b)
        t = max(0.0, min(1.0, t))
        q = a + (b - a) * t
        d = (w - q).length
        if best is None or d < best[0]:
            best = (d, q)
    target.append(best[1])
for o in [o for o in bpy.data.objects if o.type == "MESH" and o is not body]:
    bpy.data.objects.remove(o, do_unlink=True)
for k in KS:
    for v, w, q in zip(body.data.vertices, rest, target):
        v.co = inv @ (q + (w - q) * k)
    body.data.update()
    out = "%s-k%.2f.fbx" % (PREFIX, k)
    bpy.ops.object.select_all(action="DESELECT")
    body.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.export_scene.fbx(filepath=out, use_selection=True, object_types={"ARMATURE", "MESH"}, add_leaf_bones=False,
                             global_scale=1.0, apply_unit_scale=True, bake_anim=False, mesh_smooth_type="FACE")
    print("THINNED", k, out, flush=True)
