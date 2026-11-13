"""Body films of retargeted clips on a MetaHuman body, in Blender with no window, for a fresh reviewer.

    blender -b --factory-startup --python tools/tool-tests/hmc_body_film.py -- jobs.json

jobs.json: {"out": dir, "jobs": [{"name", "mesh_fbx", "anim_fbx", "video": bool}]}. Per job: the body mesh exported
from Unreal (its skeleton's reference pose is the clip's rest), the clip exported from Unreal on that same skeleton;
the mesh is moved onto the clip's armature (same bone names, same rest), and six moments are rendered from the side
and the front (Workbench, one grey, a floor line) as <name>_side_<k>.png / <name>_front_<k>.png, plus <name>.mp4 when
asked. Facing is read from the body (ball ahead of ankle), not assumed. Also per frame: pelvis height and the right
hand's distance to the head, written to <name>_track.json. Written for the HumanMotionCraft test, 13 Nov 2026.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
cfg = json.load(open(args[0], encoding="utf-8"))
OUT = cfg["out"]
os.makedirs(OUT, exist_ok=True)


def arm_with_action():
    return [o for o in bpy.context.scene.objects if o.type == "ARMATURE" and o.animation_data and o.animation_data.action]


for job in cfg["jobs"]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    bpy.ops.import_scene.fbx(filepath=job["anim_fbx"], automatic_bone_orientation=False)
    anims = arm_with_action()
    if not anims:
        print("hmc_body_film: no animated armature in", job["anim_fbx"])
        continue
    arm = anims[0]
    act = arm.animation_data.action
    f0, f1 = int(act.frame_range[0]), int(act.frame_range[1])
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.fbx(filepath=job["mesh_fbx"], automatic_bone_orientation=False)
    new_names = [o.name for o in bpy.context.scene.objects if o not in before]
    for nm in [n for n in new_names if "_LOD" in n and "_LOD0" not in n]:  # the body FBX stacks LOD0 to LOD3
        bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
    new = [bpy.data.objects[n] for n in new_names if n in bpy.data.objects]
    meshes = [o for o in new if o.type == "MESH"]
    grey = bpy.data.materials.new("body_grey")
    grey.diffuse_color = (0.62, 0.6, 0.58, 1)
    for m in meshes:
        m.data.materials.clear()
        m.data.materials.append(grey)
    for m in meshes:
        for mod in m.modifiers:
            if mod.type == "ARMATURE":
                mod.object = arm
        mw = m.matrix_world.copy()
        m.parent = None
        m.matrix_world = mw
    for o in new:
        if o.type == "ARMATURE":
            bpy.data.objects.remove(o, do_unlink=True)
    sc.frame_start, sc.frame_end = f0, f1
    sc.render.fps = 30

    P = lambda n: arm.matrix_world @ arm.pose.bones[n].head
    sc.frame_set(f0)
    fwd = P("ball_l") - P("foot_l")
    fwd.z = 0
    fwd = fwd.normalized() if fwd.length > 1e-6 else Vector((0, -1, 0))
    side = fwd.cross(Vector((0, 0, 1))).normalized()
    track, lo, hi = [], Vector((1e9, 1e9, 1e9)), Vector((-1e9, -1e9, -1e9))
    for fr in range(f0, f1 + 1):
        sc.frame_set(fr)
        pel, hd, hr = P("pelvis"), P("head"), P("hand_r")
        row = {"frame": fr, "pelvis_z_cm": round(pel.z * 100, 2), "hand_r_to_head_cm": round((hr - hd).length * 100, 2)}
        for s in "lr":
            th, ca, fo = P("thigh_" + s), P("calf_" + s), P("foot_" + s)
            row["knee_" + s] = round(math.degrees((ca - th).normalized().angle((fo - ca).normalized())), 1)
            row["ball_z_" + s] = round(P("ball_" + s).z * 100, 2)
        track.append(row)
        for n in ("head", "foot_l", "foot_r", "hand_l", "hand_r", "pelvis"):
            p = P(n)
            lo = Vector(map(min, lo, p))
            hi = Vector(map(max, hi, p))
    json.dump(track, open(os.path.join(OUT, job["name"] + "_track.json"), "w"), indent=0)
    centre = (lo + hi) / 2
    height = max(hi.z - min(lo.z, 0), 1.0)

    # Floor: a thin dark plane at z 0 so contact can be judged.
    bpy.ops.mesh.primitive_plane_add(size=6, location=(centre.x, centre.y, 0))
    fl = bpy.context.object
    mat = bpy.data.materials.new("floor")
    mat.diffuse_color = (0.18, 0.18, 0.2, 1)
    fl.data.materials.append(mat)
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light = "STUDIO"
    sc.display.shading.color_type = "MATERIAL"
    sc.display.shading.show_shadows = True
    sc.render.resolution_x, sc.render.resolution_y = 600, 800
    sc.render.film_transparent = False
    sc.world = bpy.data.worlds.new("w")
    sc.world.color = (0.55, 0.57, 0.6)
    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = 50
    cam = bpy.data.objects.new("cam", cam_data)
    sc.collection.objects.link(cam)
    sc.camera = cam
    dist = height * 2.6
    aim = Vector((centre.x, centre.y, height * 0.5))

    def place(direction):
        cam.location = aim + direction * dist + Vector((0, 0, height * 0.08))
        cam.rotation_euler = (aim - cam.location).to_track_quat("-Z", "Y").to_euler()

    moments = [f0 + round(k * (f1 - f0) / 5) for k in range(6)]
    for view, direction in (("side", side), ("front", fwd)):
        place(direction)
        for k, fr in enumerate(moments):
            sc.frame_set(fr)
            sc.render.image_settings.file_format = "PNG"
            sc.render.filepath = os.path.join(OUT, "%s_%s_%d.png" % (job["name"], view, k))
            bpy.ops.render.render(write_still=True)
    if job.get("video"):
        try:  # Blender 5.x: video is a media type first, then FFMPEG (13 Nov: "FFMPEG" alone is refused)
            place((side + fwd).normalized())
            sc.render.image_settings.media_type = "VIDEO"
            sc.render.image_settings.file_format = "FFMPEG"
            sc.render.ffmpeg.format = "MPEG4"
            sc.render.ffmpeg.codec = "H264"
            sc.render.ffmpeg.constant_rate_factor = "MEDIUM"
            sc.render.resolution_x, sc.render.resolution_y = 540, 720
            sc.render.filepath = os.path.join(OUT, job["name"] + ".mp4")
            bpy.ops.render.render(animation=True)
        except Exception as e:
            print("hmc_body_film: video refused for", job["name"], str(e)[:160])
    print("hmc_body_film: done", job["name"], "frames", f0, f1, "moments", moments)
