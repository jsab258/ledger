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
HOLD_SLEEVE, HOLD_HEM = opt("--hold-sleeve", 0.95), opt("--hold-hem", 0.5)
GARMENT = opt("--garment", "JacketSim", str)      # the coarse simulation mesh, as Unreal simulates it
os.makedirs(OUT, exist_ok=True)


def say(*a):
    print("POSE", *a, flush=True)


turn, make_pose = tailor.turn, tailor.make_pose


bpy.ops.wm.open_mainfile(filepath=BLEND)
garment = bpy.data.objects[GARMENT]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = next(o for o in bpy.data.objects if o.type == "MESH" and o is not garment
            and any(m.type == "ARMATURE" for m in o.modifiers))
# THE FINISHED GARMENT RIDES THE CLOTH (finish_donkey.py's NAME.blend): its
# render mesh (collar, yoke, buttons, pockets and all) follows the simulated
# drape by a surface deform, as Unreal's proxy deformer carries a render mesh
# on its simulation mesh; the drape itself is simulated and not drawn
RENDER = opt("--render", "JacketRender", str)
follower = bpy.data.objects.get(RENDER)
keep = (garment, body, follower)
for o in list(bpy.data.objects):
    if o.type == "MESH" and o not in keep:
        bpy.data.objects.remove(o, do_unlink=True)
garment.hide_set(False)
body.hide_render = False
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
# THE WEIGHTS PUT RIGHT FOR A JACKET (tailor.torso_weights): the body pieces
# without the arms' weights except near the sleeves, all smoothed round the
# armpits as Unreal's transfer smooths them (copied point by point, the arm's
# and the torso's weights met in one row, and the cloth there was squeezed out
# in flaps, run 16; the side panels rose into a sail, the second review)
tailor.torso_weights(garment, smooth=opt("--smooth-weights", 8, int))
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
# LOOSER ROUND THE ARMPITS (the first blind review: the body came through at
# the inside of the upper arm in the walk; with the arms raised the chest
# beside them came through the front): within 12 cm of an armpit the cloth is
# held at 0.4 rising to full, so the body's collision can push it clear, as
# Unreal's backstop will
arm_pits = [tailor.joint(arm, "upperarm_" + s_) + Vector((0.0, 0.0, -0.10)) for s_ in ("l", "r")]
for i, p in enumerate(co):
    u, v = vu.get(i, (0.0, 0.0))
    if abs(u) > 1.5:                                # a sleeve (its flat pattern at u beyond 1.5; v down it)
        w = HOLD_SLEEVE - 0.15 * max(0.0, min(1.0, -v / 0.53))
    else:
        t = max(0.0, min(1.0, (chest - p[2]) / max(0.05, chest - bottom)))
        w = 1.0 - (1.0 - HOLD_HEM) * t
    near_pit = min((Vector(p) - q).length for q in arm_pits)
    if near_pit < 0.12:
        w = min(w, 0.4 + 0.6 * near_pit / 0.12)
    hold.add([i], w, "REPLACE")
# HELD AS UNREAL HOLDS IT (run 16's poses: on the coarse mesh, held weakly,
# the sleeves stayed where they were and the arms came out of them): Unreal's
# maximum distance keeps each point within a few centimetres of where the
# skin carries it, so here the goal is strong: the sleeves and the upper body
# nearly all the way, the hem half
cl = tailor.cloth(garment, frames=FRAMES, self_collision=True, mass=None, bending=opt("--bending", 10.0))
cl.settings.vertex_group_mass = "hold"
cl.settings.pin_stiffness = opt("--pin", 5.0)
if follower is not None:
    follower.hide_set(False)
    follower.hide_render = False
    follower.modifiers.clear()
    sd = follower.modifiers.new("OnTheCloth", "SURFACE_DEFORM")
    sd.target = garment
    sd.falloff = 4.0
    bpy.context.view_layer.objects.active = follower
    bpy.ops.object.select_all(action="DESELECT")
    follower.select_set(True)
    bpy.ops.object.surfacedeform_bind(modifier="OnTheCloth")
    garment.hide_render = True
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
    worst = np.argsort(r)[-4:][::-1]
    report[name] = {"insideOver3mm": inside, "stretch95": round(float(np.percentile(r, 95)), 3),
                    "stretchMax": round(float(r.max()), 2),
                    "worst": [(round(float(r[k]), 1), [round(float(x), 3) for x in co[edges[k, 0]]],
                               [round(float(x), 2) for x in vu.get(int(edges[k, 0]), (0, 0))]) for k in worst]}
    say(name, report[name])
    cen = Vector((0.0, float(c[:, 1].mean()), float((c[:, 2].min() + c[:, 2].max()) / 2)))
    tailor.pictures(os.path.join(OUT, "pose-" + name), cen, views=(("front", (0, -3.6, 0.2)), ("side", (3.6, 0, 0.2)),
                                                                     ("three-quarter", (2.4, -2.6, 0.5))))
json.dump(report, open(os.path.join(OUT, "pose-test.json"), "w"), indent=1)
say("done")
