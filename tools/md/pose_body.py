"""A body raised from MetaHuman's reference pose (arms about 53 degrees below horizontal) to an A-pose Marvelous
Designer recognises, for draping; and the record of the turn, so the draped garment can be taken back.

    blender -b -P tools/md/pose_body.py -- BODY.fbx OUT.fbx --arms-below 40
    blender -b -P tools/md/pose_body.py -- BODY.fbx OUT.fbx --keep-arms --straight-elbows   # the arms as they are, elbows straight
    blender -b -P tools/md/pose_body.py -- BODY.fbx OUT.fbx --keep-arms --straight-elbows --thighs-apart 4   # and each thigh 4 degrees out
    blender -b -P tools/md/pose_body.py -- BODY.fbx OUT.fbx --keep-arms --straight-elbows --with-mesh BOOTS.fbx --raise 20   # shod, soles on the floor

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
# THE SHOES WORN FOR THE DRAPE, --with-mesh PATH[,PATH] (30 October 2026, Tom's jeans over his boots, drape n5: drape n2
# was draped over his bare feet, so with the boots on 29 to 30 of each hem's 32 points sat inside them). Each file's
# meshes (FBX or OBJ, in the body's own frame, e.g. F:/LedgerTools/garments/tom/boots/tom_boots_skinned.fbx) are joined
# into the body before any turn, so Marvelous takes one avatar mesh; a mesh skinned to the same skeleton keeps its
# weights (by bone name) and follows any turn; its own armature is dropped. Off by default.
with_mesh = []
if "--with-mesh" in argv:
    for path in argv[argv.index("--with-mesh") + 1].split(","):
        before = set(bpy.data.objects)
        if path.lower().endswith(".obj"):
            bpy.ops.wm.obj_import(filepath=path)
        else:
            bpy.ops.import_scene.fbx(filepath=path)
        new = [o for o in bpy.data.objects if o not in before]
        extra = [o for o in new if o.type == "MESH"]
        for o in extra:
            mw = o.matrix_world.copy()
            o.parent = None
            o.matrix_world = mw
            for m in list(o.modifiers):
                o.modifiers.remove(m)
        for o in new:
            if o.type != "MESH":
                bpy.data.objects.remove(o, do_unlink=True)
        added = sum(len(o.data.vertices) for o in extra)
        bpy.ops.object.select_all(action="DESELECT")
        for o in extra:
            o.select_set(True)
        body.select_set(True)
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.join()
        with_mesh.append({"path": path, "meshes": len(extra), "points": added})
turns = {}
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
for s in ("lr" if "--keep-arms" not in argv else ""):
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
# THE ELBOWS STRAIGHTENED, --straight-elbows (28 October 2026, the sleeve's end, fourth round: in the reference pose
# the elbow bends 36.6 degrees and the forearm points forward, while Marvelous wraps a sleeve round one straight volume
# per arm; that volume misses the forearm by 47 to 107 mm (tools/md-bridge/sleeve_wrap.py), so the sleeve's narrow end
# closed beside the arm and the hand came through it; Marvelous's manual drapes in a T- or A-pose and changes pose
# after). Each forearm is turned about its elbow until it runs on along the upper arm; the turn is recorded so the
# draped garment can be bent back with the arm.
if "--straight-elbows" in argv:
    for s in "lr":
        pb = arm.pose.bones["lowerarm_" + s]
        sh = arm.matrix_world @ arm.pose.bones["upperarm_" + s].head
        e = arm.matrix_world @ pb.head
        h = arm.matrix_world @ arm.pose.bones["hand_" + s].head
        up, fore = (e - sh).normalized(), (h - e).normalized()
        axis = fore.cross(up).normalized()
        ang = fore.angle(up)
        R = Matrix.Rotation(ang, 4, axis)
        pb.matrix = arm.matrix_world.inverted() @ Matrix.Translation(e) @ R @ Matrix.Translation(-e) @ arm.matrix_world @ pb.matrix
        bpy.context.view_layer.update()
        h2 = arm.matrix_world @ arm.pose.bones["hand_" + s].head
        turns.setdefault(s, {})["elbow"] = {"turnDeg": round(math.degrees(ang), 2), "axis": [round(c, 6) for c in axis],
                                            "elbow": [round(c, 5) for c in e],
                                            "bendAfterDeg": round(math.degrees((h2 - e).normalized().angle(up)), 3)}
# THE THIGHS DRAWN APART, --thighs-apart DEG (30 October 2026, Tom's jeans, drape n2: his inner thighs come within
# 0 to 5 mm of each other from 0.83 m to his crotch at 0.906, so the jeans' crotch, which hangs there, could not lie
# between them at Marvelous's 3 mm skin offset a side, and 8 of its points went more than 3 mm into the body). Each
# thigh is turned out about its hip joint, square to the thigh and the body's side, by DEG; the calves and feet follow,
# the skin follows the weights; the turn is recorded so the drape can be bent back with the legs (unpose_garment.py).
if "--thighs-apart" in argv:
    APART = opt("--thighs-apart", 0.0)
    for s, out_x in (("l", 1.0), ("r", -1.0)):
        pb = arm.pose.bones["thigh_" + s]
        hip = arm.matrix_world @ pb.head
        knee = arm.matrix_world @ arm.pose.bones["calf_" + s].head
        d = (knee - hip).normalized()
        axis = d.cross(Vector((out_x, 0.0, 0.0))).normalized()
        R = Matrix.Rotation(math.radians(APART), 4, axis)
        pb.matrix = arm.matrix_world.inverted() @ Matrix.Translation(hip) @ R @ Matrix.Translation(-hip) @ arm.matrix_world @ pb.matrix
        bpy.context.view_layer.update()
        k2 = arm.matrix_world @ arm.pose.bones["calf_" + s].head
        turns.setdefault(s, {})["thigh"] = {"turnDeg": round(APART, 3), "axis": [round(c, 6) for c in axis],
                                            "hip": [round(c, 5) for c in hip],
                                            "kneeOutMm": round(1000 * (k2.x - knee.x) * out_x, 1)}
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
# THE WHOLE RAISED, --raise MM (30 October 2026, drape n5: the boots' soles stand 20 mm under his bare floor, and
# Marvelous's floor is at the bare floor's height; the game raises him by the same 20 mm): the skin and every bone moved
# up by MM, after the turns (which stay recorded in his own frame); unpose_garment.py reads raiseMm and takes the drape
# back down. Off by default.
RAISE = opt("--raise", 0.0)
if RAISE:
    T = Matrix.Translation((0.0, 0.0, RAISE / 1000.0))
    body.data.transform(body.matrix_world.inverted() @ T @ body.matrix_world, shape_keys=True)
    arm.data.transform(arm.matrix_world.inverted() @ T @ arm.matrix_world)
    bpy.context.view_layer.update()
bpy.ops.object.select_all(action="DESELECT")
body.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.fbx(filepath=OUT, use_selection=True, object_types={"ARMATURE", "MESH"}, add_leaf_bones=False,
                         global_scale=1.0, apply_unit_scale=True, bake_anim=False, mesh_smooth_type="FACE")
record = {"source": SRC, "armsBelow": BELOW, "turns": turns}
if with_mesh:
    record["withMesh"] = with_mesh
if RAISE:
    record["raiseMm"] = RAISE
json.dump(record, open(OUT[:-4] + ".json", "w"), indent=1)
print("POSED", json.dumps(turns), flush=True)
