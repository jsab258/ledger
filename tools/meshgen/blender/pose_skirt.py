"""A skirt tested as the game wears it: its band and hip on the pelvis, the rest cloth over the legs, walking and sitting.

    blender -b -P tools/meshgen/blender/pose_skirt.py -- SKIRT.blend OUT_DIR [--poses walk,sit] [--hip 0.909]

WHY, 29 September (the clothing session; Jafar's rule that every garment is
tested walking and sitting; the research, SHEILA-CLOTHES-2026-09-29.md: "test
sitting before anything else"). The coarse simulation skirt (model_skirt.py's
SkirtSim) rides the pelvis by skin and is held there above the hip, where its
pleats are stitched; below, it is Blender cloth of a wool skirt's weight,
falling over the legs as they move, as Chaos will in the game. The pleated
render skirt follows it by a surface deform, as Unreal's proxy deformer
carries a render mesh on its simulation mesh. The skeleton goes from the rest
pose to each test pose over 30 frames and holds 20; the stills are taken at
the end. OUT_DIR gets pose-NAME-front.png, -side.png, -three-quarter.png and
pose-test.json (points of the cloth inside the body, stretch).
"""
import json
import os
import sys

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


POSES = opt("--poses", "walk,sit", str).split(",")
HIP = opt("--hip", 0.95)                  # held above this (the hip joint), fading over FADE below
FADE = opt("--fade", 0.04)
FRAMES, HOLD = opt("--frames", 70, int), opt("--hold-frames", 25, int)
log = {"blend": BLEND, "poses": {}}


def say(*a):
    print("POSE", *a, flush=True)


for name in POSES:
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sim = bpy.data.objects["SkirtSim"]
    render = bpy.data.objects["SkirtRender"]
    arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
    body = next(o for o in bpy.data.objects if o.type == "MESH" and any(m.type == "ARMATURE" for m in o.modifiers))
    for o in list(bpy.data.objects):
        if o.type == "MESH" and o not in (sim, render, body):
            bpy.data.objects.remove(o, do_unlink=True)
    if arm.animation_data:
        arm.animation_data_clear()
    for pb in arm.pose.bones:
        pb.rotation_mode = "QUATERNION"
        pb.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()
    # AS THE GAME HOLDS IT (Chaos's max distance, growing from nothing at the hip
    # to a few centimetres at the hem): the cloth skinned (the pelvis at the top,
    # each side blending towards its own thigh lower down, less at the back,
    # which hangs from the seat) and held softly to that skinned place, fully
    # above the hip, still a third at the hem. (Hanging free, the first tries
    # rode up into a bunch walking and fell through the thighs sitting.)
    sco = np.array([sim.matrix_world @ v.co for v in sim.data.vertices])
    z_hem = float(sco[:, 2].min())
    cy = float(sco[:, 1].mean())
    groups = {n: sim.vertex_groups.new(name=n) for n in ("pelvis", "thigh_l", "thigh_r")}
    hold = sim.vertex_groups.new(name="hold")
    SIT_W = name in opt("--sit-weights", "sit", str).split(",")
    FOLD = opt("--fold", 0.85)                  # the buttock fold's height
    SHARE = opt("--share", 0.045)               # the middle shared by both thighs over twice this
    for i, p in enumerate(sco):
        t = float(np.clip((HIP - p[2]) / max(1e-6, HIP - z_hem), 0.0, 1.0)) ** 0.8
        if SIT_W:
            # FOR SITTING (SEATED-SKIRT-2026-09-29.md): the band and hip on the
            # pelvis; below the buttock fold the whole ring on the thighs, the
            # back included (it is sat on), each half on its own thigh, the
            # middle front and back shared over 9 cm
            # the front goes over to the thighs from the hip down; the back and
            # sides only from the buttock fold, the seat staying on the pelvis
            # (the first seated try tipped the whole back out over the seat)
            back = float(np.clip((p[1] - cy) / 0.06, 0.0, 1.0))
            top = HIP + (FOLD - HIP) * back
            leg = float(np.clip((top - p[2]) / max(1e-6, opt("--leg-blend", 0.06)), 0.0, 1.0))
            own = 0.5 + 0.5 * float(np.clip(abs(p[0]) / SHARE, 0.0, 1.0))
            groups["pelvis"].add([i], 1.0 - leg, "REPLACE")
            if leg > 0:
                mine, other = ("thigh_l", "thigh_r") if p[0] > 0 else ("thigh_r", "thigh_l")
                groups[mine].add([i], leg * own, "REPLACE")
                if own < 1.0:
                    groups[other].add([i], leg * (1.0 - own), "REPLACE")
        else:
            back = float(np.clip((p[1] - cy) / 0.08, 0.0, 1.0))
            leg = t * (opt("--front-leg", 0.97) - opt("--back-less", 0.5) * back)
            groups["pelvis"].add([i], 1.0 - leg, "REPLACE")
            if leg > 0:
                groups["thigh_l" if p[0] > 0 else "thigh_r"].add([i], leg, "REPLACE")
        hold.add([i], 1.0 - opt("--hem-free", 0.65) * t, "REPLACE")
    am = sim.modifiers.new("Armature", "ARMATURE")
    am.object = arm
    SKINNED = name in opt("--skinned", "sit", str).split(",")
    # SITTING SETTLES IN THE POSE (29 September: as cloth moving with the
    # thighs, they rose through the skirt's front; skinned alone, the front
    # stood off the thighs like a lampshade): the skeleton is put in the pose
    # first, then the cloth, skinned there, falls onto the lap and hangs behind,
    # held only where its pleats are stitched, with the body still
    SETTLE = name in opt("--settle-in-pose", "", str).split(",")
    if SETTLE:
        tailor.make_pose(arm, name)
        bpy.context.view_layer.update()
        hold.add(list(range(len(sim.data.vertices))), 0.0, "REPLACE")
        for i, p in enumerate(sco):
            hold.add([i], 1.0 if p[2] >= HIP else max(0.0, 1.0 - (HIP - p[2]) / FADE), "REPLACE")
    tailor.collider(body, friction=opt("--friction", 20.0) if SETTLE else 5.0)
    body.collision.thickness_outer = 0.006
    cl = None if SKINNED else tailor.cloth(sim, quality=opt("--quality", 14, int), mass=None, tension=30.0, compression=30.0, shear=10.0,
                      bending=opt("--bending", 6.0), distance=0.006, frames=FRAMES + HOLD)
    # SITTING IS SKINNED ALONE (29 September: as cloth, hanging or held softly,
    # the thighs rose through the skirt's front and left it below them; games
    # skin a seated skirt, the front riding the thighs onto the lap)
    if cl is not None:
        cl.collision_settings.collision_quality = 8
        cl.settings.mass = tailor.mass_per_point(sim, opt("--density", 0.30))
        cl.settings.vertex_group_mass = "hold"
        cl.settings.pin_stiffness = opt("--pin", 1.5)
    # the render skirt rides the cloth
    sd = render.modifiers.new("Follow", "SURFACE_DEFORM")
    sd.target = sim
    bpy.context.view_layer.objects.active = render
    bpy.ops.object.surfacedeform_bind(modifier="Follow")
    # rest to the pose over FRAMES, then held
    scn = bpy.context.scene
    scn.frame_start, scn.frame_end = 1, FRAMES + HOLD
    scn.frame_set(1)
    for pb in arm.pose.bones:
        pb.keyframe_insert("rotation_quaternion", frame=1)
    if not SETTLE:
        tailor.make_pose(arm, name)
    for pb in arm.pose.bones:
        pb.keyframe_insert("rotation_quaternion", frame=FRAMES)
        pb.keyframe_insert("rotation_quaternion", frame=FRAMES + HOLD)
    for f in range(1, FRAMES + HOLD + 1):
        scn.frame_set(f)
    co = tailor.coords(sim)
    bev = tailor.evaluated_copy(body, "BodyPosed")
    bvh = tailor.bvh_of(bev)
    bpy.data.objects.remove(bev, do_unlink=True)
    deep = np.array([tailor.depth_inside(bvh, Vector(p)) for p in co])
    rco = tailor.coords(render)
    rdeep = np.array([tailor.depth_inside(bvh, Vector(p)) for p in rco[::3]])
    log["poses"].setdefault(name, {})["renderPointsInsideOver3mm"] = int((rdeep > 0.003).sum())
    log["poses"][name].update({"skinnedOnly": SKINNED, "settledInPose": SETTLE, "simPointsInsideOver5mm": int((deep > 0.005).sum()), "deepestMm": round(float(deep.max()) * 1000, 1),
                          "lowestZ": round(float(co[:, 2].min()), 3)})
    say(name, json.dumps(log["poses"][name]))
    grey = tailor.material("M_Body", (0.5, 0.5, 0.5))
    body.data.materials.clear()
    body.data.materials.append(grey)
    mid = Vector((0.0, float(co[:, 1].mean()), float(co[:, 2].mean()) + 0.05))
    tailor.pictures(os.path.join(OUT, "pose-%s" % name), mid,
                    views=(("front", (0, -2.6, 0.2)), ("side", (2.6, 0, 0.2)), ("three-quarter", (1.8, -1.9, 0.4))))
json.dump(log, open(os.path.join(OUT, "pose-test.json"), "w"), indent=1)
say("done")
