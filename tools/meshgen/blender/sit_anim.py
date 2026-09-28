"""A sit-down on a MetaHuman's own skeleton, for testing clothes: standing, then seated over a second, then held.

    blender -b -P tools/meshgen/blender/sit_anim.py -- BODY.fbx OUT.fbx [--thigh 80] [--knee 85] [--lean 12] [--arm 40] [--elbow 55]

WHY, 28 September (Jafar's list, item 5: the jacket "tested walking,
sitting and with arms raised"). Epic's MetaHuman animations have a walk and a
range-of-motion loop but no sitting, and the free packs (Fab, Mixamo) need
Jafar signed in. So a plain sit is made here: the thighs raised forward, the
knees bent back, the back leaning a little forward, the pelvis lowered so the
feet stay on the floor. Which way a bone turns
depends on how its axes lie, so for each joint the script tries each local
axis both ways and keeps the one that moves the next joint where a sitting
body's goes (the knee forward and up; the ankle back under the knee). Frames:
1 standing, 30 seated, held to 90 at 30 frames a second. Writes OUT.fbx (the
skeleton and its animation only) and prints what it chose.
"""
import math
import sys

import bpy
from mathutils import Quaternion, Vector

argv = sys.argv[sys.argv.index("--") + 1:]
BODY, OUT = argv[0], argv[1]


def opt(name, default):
    return float(argv[argv.index(name) + 1]) if name in argv else default


THIGH, KNEE, LEAN = opt("--thigh", 80.0), opt("--knee", 85.0), opt("--lean", 12.0)
ARM, ELBOW = opt("--arm", 40.0), opt("--elbow", 55.0)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY)
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
# THE SKELETON KEEPS ITS SIZE: it comes in under an empty that scales it to
# metres (the file is in centimetres); removing the empty with the rest left
# it a hundred times too big, and Unreal put the whole sit a hundred times too
# big, out of every frame (28 September).
_mw = arm.matrix_world.copy()
arm.parent = None
arm.matrix_world = _mw
for o in list(bpy.context.scene.objects):
    if o is not arm:
        bpy.data.objects.remove(o, do_unlink=True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
scene = bpy.context.scene
scene.render.fps = 30
scene.frame_start, scene.frame_end = 1, 90
pb = arm.pose.bones


def world_head(name):
    bpy.context.view_layer.update()
    return arm.matrix_world @ pb[name].head


FRONT = Vector((0.0, -1.0, 0.0))     # the body faces -Y once imported (the jacket's buttons sit at -Y)
AXES = {"X": Vector((1, 0, 0)), "Y": Vector((0, 1, 0)), "Z": Vector((0, 0, 1))}


def best_turn(bone, child, degrees, score):
    """The local axis and sign that, turning `bone` by `degrees`, give `child`'s head the best score."""
    b = pb[bone]
    b.rotation_mode = "QUATERNION"
    rest = b.rotation_quaternion.copy()
    before = world_head(child)
    best = None
    for name, axis in AXES.items():
        for sign in (1, -1):
            b.rotation_quaternion = Quaternion(axis, math.radians(degrees * sign)) @ rest
            after = world_head(child)
            sc = score(before, after)
            if best is None or sc > best[0]:
                best = (sc, name, sign, Quaternion(axis, math.radians(degrees * sign)) @ rest)
    b.rotation_quaternion = rest
    return best


chosen = {}
for side in ("l", "r"):
    thigh, calf, foot = "thigh_" + side, "calf_" + side, "foot_" + side
    # the knee forward and up
    sc, ax, sg, q = best_turn(thigh, calf, THIGH, lambda a, b: (b - a).dot(FRONT) + (b - a).z)
    pb[thigh].rotation_quaternion = q
    chosen[thigh] = (ax, sg, round(sc, 3))
    # then the ankle back under the knee: down, and not forward
    sc, ax, sg, q = best_turn(calf, foot, KNEE, lambda a, b: -(b - a).dot(FRONT) - (b - a).z)
    pb[calf].rotation_quaternion = q
    chosen[calf] = (ax, sg, round(sc, 3))
# THE ARMS DOWN, the forearms forward onto the lap: without them the arms
# stayed out in the skeleton's modelling pose, as if he were balancing (28
# September). The elbow down; then the hand forward.
for side in ("l", "r"):
    up, low, hand = "upperarm_" + side, "lowerarm_" + side, "hand_" + side
    sc, ax, sg, q = best_turn(up, low, ARM, lambda a, b: -(b - a).z)
    pb[up].rotation_quaternion = q
    chosen[up] = (ax, sg, round(sc, 3))
    sc, ax, sg, q = best_turn(low, hand, ELBOW, lambda a, b: (b - a).dot(FRONT))
    pb[low].rotation_quaternion = q
    chosen[low] = (ax, sg, round(sc, 3))
# the back leans a little forward: the neck forward
sc, ax, sg, q = best_turn("spine_01", "neck_01", LEAN, lambda a, b: (b - a).dot(FRONT))
pb["spine_01"].rotation_quaternion = q
chosen["spine_01"] = (ax, sg, round(sc, 3))
seated = {n: pb[n].rotation_quaternion.copy() for n in chosen}
# DOWN ONTO THE SEAT: the legs alone leave him sitting in the air, feet off the
# ground; the pelvis is lowered by as much as the ankles rose, so the feet stay
# on the floor and the seat comes down to a chair's height.
stand_ankle = None
for n in chosen:
    pb[n].rotation_quaternion = Quaternion((1, 0, 0, 0))
stand_ankle = world_head("foot_l")
for n, q in seated.items():
    pb[n].rotation_quaternion = q
drop = world_head("foot_l").z - stand_ankle.z
m = pb["pelvis"].matrix.copy()
m.translation.z -= drop / arm.matrix_world.to_scale().z
pb["pelvis"].matrix = m
bpy.context.view_layer.update()
seated_pelvis = pb["pelvis"].location.copy()

# keys: standing at 1, seated at 30 and 90
for n in chosen:
    pb[n].rotation_mode = "QUATERNION"
for n, q in seated.items():
    pb[n].rotation_quaternion = Quaternion((1, 0, 0, 0))
    pb[n].keyframe_insert("rotation_quaternion", frame=1)
pb["pelvis"].location = (0.0, 0.0, 0.0)
pb["pelvis"].keyframe_insert("location", frame=1)
bpy.context.view_layer.update()
for n, q in seated.items():
    pb[n].rotation_quaternion = q
    pb[n].keyframe_insert("rotation_quaternion", frame=30)
    pb[n].keyframe_insert("rotation_quaternion", frame=90)
pb["pelvis"].location = seated_pelvis
for f in (30, 90):
    pb["pelvis"].keyframe_insert("location", frame=f)
scene.frame_set(90)
knee_l, ankle_l, hip_l = world_head("calf_l"), world_head("foot_l"), world_head("thigh_l")
bpy.ops.object.mode_set(mode="OBJECT")
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
bpy.ops.export_scene.fbx(filepath=OUT, use_selection=True, object_types={"ARMATURE"}, add_leaf_bones=False,
                         bake_anim=True, bake_anim_use_all_actions=False, bake_anim_use_nla_strips=False,
                         bake_anim_force_startend_keying=True)
print("SIT", {"chosen": chosen, "pelvisDropM": round(drop, 3), "hip": [round(v, 3) for v in hip_l], "knee": [round(v, 3) for v in knee_l],
              "ankle": [round(v, 3) for v in ankle_l], "out": OUT})
