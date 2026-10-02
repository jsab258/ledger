"""A body raised from MetaHuman's reference pose (arms about 53 degrees below horizontal) to an A-pose Marvelous
Designer recognises, for draping; and the record of the turn, so the draped garment can be taken back.

    blender -b -P tools/md/pose_body.py -- BODY.fbx OUT.fbx --arms-below 40

WHY, 1 October (the jacket proof): imported in MetaHuman's reference pose, Marvelous said "Arrangement Points were
not fitted to the avatar. The avatar must be in a T-pose or A-pose" and found no measurements, so it cannot place the
pieces round the body. So the upper arms are turned up about the axis square to the arm's own plane until they hang
--arms-below degrees below horizontal (the forearms and hands follow), the skin following the skeleton, and the
posed body is written as the avatar (FBX, centimetres, with its skeleton in the A-pose as rest). OUT.json beside it records the turn, so the
garment draped on it can be turned back (tools/md/unpose_garment.py) to the reference pose the game's bodies stand
in.
"""
import json
import math
import sys

import bpy
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT = argv[0], argv[1]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


BELOW = opt("--arms-below", 40.0)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = sorted([o for o in bpy.data.objects if o.type == "MESH"], key=lambda o: -len(o.data.vertices))[0]
for o in [o for o in bpy.data.objects if o.type == "MESH" and o is not body]:
    bpy.data.objects.remove(o, do_unlink=True)
turns = {}
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
for s in "lr":
    pb = arm.pose.bones["upperarm_" + s]
    a = arm.matrix_world @ pb.head
    b = arm.matrix_world @ arm.pose.bones["lowerarm_" + s].head
    d = (b - a).normalized()
    now = math.degrees(math.atan2(-d.z, math.hypot(d.x, d.y)))
    turn = now - BELOW
    # the axis: square to the arm and the vertical, so the arm swings up in its own plane
    axis = d.cross(Vector((0, 0, 1))).normalized()
    R = Matrix.Rotation(math.radians(turn), 4, axis)
    # world-space rotation about the shoulder joint, written into the bone's pose
    M = arm.matrix_world.inverted() @ Matrix.Translation(a) @ R @ Matrix.Translation(-a) @ arm.matrix_world @ pb.matrix
    pb.matrix = M
    bpy.context.view_layer.update()
    b2 = arm.matrix_world @ arm.pose.bones["lowerarm_" + s].head
    d2 = (b2 - a).normalized()
    turns[s] = {"from": round(now, 2), "to": round(math.degrees(math.atan2(-d2.z, math.hypot(d2.x, d2.y))), 2),
                "turnDeg": round(turn, 2), "axis": [round(c, 6) for c in axis], "shoulder": [round(c, 5) for c in a]}
bpy.ops.object.mode_set(mode="OBJECT")
# the posed skin made the body's rest shape, and the posed skeleton its rest pose, so the FBX carries the skeleton in
# the A-pose with the skin bound to it (Marvelous recognises a MetaHuman by its joint names, through its own
# MH_m_med_nrw_combined mapping; written without the skeleton, it found no arrangement points)
bpy.context.view_layer.objects.active = body
for m in list(body.modifiers):
    if m.type == "ARMATURE":
        bpy.ops.object.modifier_apply(modifier=m.name)
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
bpy.ops.pose.select_all(action="SELECT")
bpy.ops.pose.armature_apply(selected=False)
bpy.ops.object.mode_set(mode="OBJECT")
mod = body.modifiers.new("Armature", "ARMATURE")
mod.object = arm
bpy.ops.object.select_all(action="DESELECT")
body.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.fbx(filepath=OUT, use_selection=True, object_types={"ARMATURE", "MESH"}, add_leaf_bones=False,
                         global_scale=1.0, apply_unit_scale=True, bake_anim=False, mesh_smooth_type="FACE")
json.dump({"source": SRC, "armsBelow": BELOW, "turns": turns}, open(OUT[:-4] + ".json", "w"), indent=1)
print("POSED", json.dumps(turns), flush=True)
