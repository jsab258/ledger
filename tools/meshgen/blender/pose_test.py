"""A garment tested on its wearer in the poses the game asks of it: arms down, arms raised, walking and sitting.

    blender -b -P tools/meshgen/blender/pose_test.py -- JACKET.blend OUT_DIR [--poses down,up,walk,sit] [--frames 45]

WHY, 29 September (the clothing session; Jafar's rule: every garment "tested
walking, sitting and with arms raised" before it goes to the builder). The
garment, as sew_donkey.py leaves it in the body's rest pose, takes the body's
skin weights (each point those of the nearest place on the body) and is
worn as cloth over the skin: an Armature modifier carries it with the
skeleton, and a cloth simulation on top lets it hang and swing, held to the
skinned shape most at the shoulders and least at the hem (as the builder's
maximum distance does in Unreal). The skeleton goes from the rest pose to
each test pose over 30 frames and holds; the stills are taken at the end.

Poses, each made by turning bones about world axes at their joints (the
MetaHuman skeleton's local axes differ bone to bone):
  down  the arms hanging, 80 degrees below the horizontal
  up    the arms raised 35 degrees above the horizontal
  walk  mid-stride: the left thigh 25 degrees forward, the right 15 back
        with its knee bent 30, the arms down and swinging 20 degrees
  sit   the thighs 85 degrees forward, the knees 85 back, the back leaning
        10 forward, the arms down with the forearms forward onto the lap

OUT_DIR gets pose-NAME-front.png, -side.png, -three-quarter.png and
pose-test.json (for each pose: points inside the body at the end, the
largest stretch of the garment's edges against its rest).
"""
import json
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, OUT = argv[0], argv[1]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


POSES = opt("--poses", "down,up,walk,sit", str).split(",")
FRAMES = opt("--frames", 45, int)
GARMENT = opt("--garment", "Jacket", str)
os.makedirs(OUT, exist_ok=True)


def say(*a):
    print("POSE", *a, flush=True)


def turn(arm, bone, axis, deg, child=None, want=None):
    """Turn a pose bone about a world axis through its own joint. If `want` is given (a world direction), the
    sign is chosen so that `child`'s joint moves that way."""
    pb = arm.pose.bones[bone]
    bpy.context.view_layer.update()
    M = arm.matrix_world
    head = pb.head.copy()
    before = pb.matrix.copy()

    def apply(sign):
        R = Matrix.Rotation(math.radians(deg * sign), 4, axis)
        Ra = (M.inverted() @ R @ M).to_3x3().to_4x4()
        pb.matrix = Matrix.Translation(head) @ Ra @ Matrix.Translation(-head) @ before
        bpy.context.view_layer.update()

    if want is None or child is None:
        apply(1)
        return
    c0 = M @ arm.pose.bones[child].head
    apply(1)
    moved = (M @ arm.pose.bones[child].head) - c0
    if moved.dot(want) < 0:
        apply(-1)


def make_pose(arm, name):
    X, Z = Vector((1, 0, 0)), Vector((0, 0, 1))
    fwd, up = Vector((0, -1, 0)), Vector((0, 0, 1))
    if name in ("down", "walk", "sit"):
        tailor.pose_arms(arm, 80.0)
    if name == "up":
        tailor.pose_arms(arm, -35.0)
    if name == "walk":
        turn(arm, "thigh_l", X, 25, "calf_l", fwd)
        turn(arm, "thigh_r", X, 15, "calf_r", -fwd)
        turn(arm, "calf_r", X, 30, "foot_r", -fwd + up * 0.3)
        turn(arm, "upperarm_l", X, 20, "lowerarm_l", -fwd)       # arms swing against the legs
        turn(arm, "upperarm_r", X, 20, "lowerarm_r", fwd)
    if name == "sit":
        turn(arm, "spine_01", X, 10, "spine_03", fwd)
        for s in ("l", "r"):
            turn(arm, "thigh_" + s, X, 85, "calf_" + s, fwd + up)
            turn(arm, "calf_" + s, X, 85, "foot_" + s, -fwd - up)
            turn(arm, "lowerarm_" + s, X, 50, "hand_" + s, fwd)


bpy.ops.wm.open_mainfile(filepath=BLEND)
garment = bpy.data.objects[GARMENT]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = next(o for o in bpy.data.objects if o.type == "MESH" and o is not garment and not o.hide_render
            and any(m.type == "ARMATURE" for m in o.modifiers))
for o in list(bpy.data.objects):
    if o.type == "MESH" and o not in (garment, body):
        bpy.data.objects.remove(o, do_unlink=True)
if arm.animation_data:
    arm.animation_data_clear()
for pb in arm.pose.bones:
    pb.rotation_mode = "QUATERNION"
    pb.rotation_quaternion = (1, 0, 0, 0)
    pb.location = (0, 0, 0)
    pb.scale = (1, 1, 1)
bpy.context.view_layer.update()
garment.modifiers.clear()
for mdf in list(body.modifiers):
    if mdf.type == "COLLISION":
        body.modifiers.remove(mdf)

# ---- the garment takes the body's skin weights ----------------------------------------

dt = garment.modifiers.new("Weights", "DATA_TRANSFER")
dt.object = body
dt.use_vert_data = True
dt.data_types_verts = {"VGROUP_WEIGHTS"}
dt.vert_mapping = "POLYINTERP_NEAREST"
dt.layers_vgroup_select_src = "ALL"
dt.layers_vgroup_select_dst = "NAME"
bpy.context.view_layer.objects.active = garment
bpy.ops.object.datalayout_transfer(modifier="Weights")
bpy.ops.object.modifier_apply(modifier="Weights")
mw = garment.matrix_world.copy()
garment.parent = arm
garment.matrix_world = mw
am = garment.modifiers.new("Armature", "ARMATURE")
am.object = arm

# HELD MOST AT THE SHOULDERS, LEAST AT THE HEM (the builder's maximum
# distance in Unreal: about 1 cm on the chest, back and shoulders, several
# towards the hem): a goal weight from 1 above the chest to 0.25 at the hem,
# the sleeves 0.7 down to 0.4 at the cuff
co = np.array([garment.matrix_world @ v.co for v in garment.data.vertices])
top, bottom = float(co[:, 2].max()), float(co[:, 2].min())
chest = top - 0.3
uv = garment.data.uv_layers.get("pattern")
vu = {}
if uv:
    for lp in garment.data.loops:
        vu[lp.vertex_index] = tuple(uv.data[lp.index].uv)
hold = garment.vertex_groups.new(name="hold")
for i, p in enumerate(co):
    u, v = vu.get(i, (0.0, 0.0))
    if abs(u) > 1.5:                                # a sleeve (its flat pattern at u beyond 1.5; v down it)
        w = 0.7 - 0.3 * max(0.0, min(1.0, -v / 0.53))
    else:
        t = max(0.0, min(1.0, (chest - p[2]) / max(0.05, chest - bottom)))
        w = 1.0 - 0.75 * t
    hold.add([i], w, "REPLACE")
cl = tailor.cloth(garment, frames=FRAMES, self_collision=True)
cl.settings.vertex_group_mass = "hold"
cl.settings.pin_stiffness = 1.0
tailor.collider(body, friction=20.0)
grey = tailor.material("M_Body", (0.5, 0.5, 0.5))
body.data.materials.clear()
body.data.materials.append(grey)

scn = bpy.context.scene
scn.frame_start, scn.frame_end = 1, FRAMES
rest = {pb.name: pb.rotation_quaternion.copy() for pb in arm.pose.bones}
rest_loc = {pb.name: pb.location.copy() for pb in arm.pose.bones}
edges = np.array([e.vertices[:] for e in garment.data.edges])
L0 = np.linalg.norm(co[edges[:, 0]] - co[edges[:, 1]], axis=1)
report = {}
for name in POSES:
    for pb in arm.pose.bones:
        pb.rotation_quaternion = rest[pb.name]
        pb.location = rest_loc[pb.name]
    if arm.animation_data:
        arm.animation_data_clear()
    bpy.context.view_layer.update()
    for pb in arm.pose.bones:
        pb.keyframe_insert("rotation_quaternion", frame=1)
    make_pose(arm, name)
    for pb in arm.pose.bones:
        pb.keyframe_insert("rotation_quaternion", frame=30)
    cl.point_cache.frame_start, cl.point_cache.frame_end = 1, FRAMES
    bpy.ops.ptcache.free_bake_all()
    for f in range(1, FRAMES + 1):
        scn.frame_set(f)
    c = tailor.coords(garment)
    bev = tailor.evaluated_copy(body, "BodyNow")
    bvh = tailor.bvh_of(bev)
    bpy.data.objects.remove(bev, do_unlink=True)
    inside = tailor.inside_count(bvh, c, range(len(c)), tol=0.003)
    L1 = np.linalg.norm(c[edges[:, 0]] - c[edges[:, 1]], axis=1)
    r = L1 / np.maximum(L0, 1e-6)
    report[name] = {"insideOver3mm": inside, "stretch95": round(float(np.percentile(r, 95)), 3),
                    "stretchMax": round(float(r.max()), 2)}
    say(name, report[name])
    cen = Vector((0.0, float(c[:, 1].mean()), float((c[:, 2].min() + c[:, 2].max()) / 2)))
    tailor.pictures(os.path.join(OUT, "pose-" + name), cen, views=(("front", (0, -3.6, 0.2)), ("side", (3.6, 0, 0.2)),
                                                                     ("three-quarter", (2.4, -2.6, 0.5))))
json.dump(report, open(os.path.join(OUT, "pose-test.json"), "w"), indent=1)
say("done")
