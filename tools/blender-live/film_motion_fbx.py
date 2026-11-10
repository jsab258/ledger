"""Film a solved body motion (FBX, skeleton only) on a plain capsule body, front and side, beside its source clip.

    blender.exe -b --factory-startup --python tools/blender-live/film_motion_fbx.py -- FBX SOURCE_MP4 OUT_DIR

Why (n09-8, advisor 89, 10 Nov 2026): the experiment's verdict needs the solve seen beside the clip it came from.
A commandlet cannot export the preview mesh, so the body is drawn here: one capsule per main bone, weighted to it,
a grid floor at the lowest foot height (foot slide reads against the grid), fixed cameras framing the whole motion.
Writes OUT_DIR/front/f-00001.png..., OUT_DIR/side/..., OUT_DIR/source/... and OUT_DIR/film-info.json.
Compose with tools/compose_motion_film.py.
"""
import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
FBX, SRC, OUT = argv[0], argv[1], argv[2]
os.makedirs(OUT, exist_ok=True)

RAD = [("pelvis", .11), ("spine_0", .10), ("spine", .10), ("neck", .05), ("head", .095), ("clavicle", .045),
       ("upperarm", .045), ("lowerarm", .037), ("hand", .03), ("thumb", .009), ("index", .008), ("middle", .008),
       ("ring", .008), ("pinky", .007), ("thigh", .07), ("calf", .05), ("foot", .04), ("ball", .03)]

for o in list(bpy.data.objects):  # the factory scene's cube, light and camera (the cube stood in front of the body on 10 Nov)
    bpy.data.objects.remove(o)
bpy.ops.import_scene.fbx(filepath=FBX, automatic_bone_orientation=False)
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
act = arm.animation_data.action if arm.animation_data else None
f0, f1 = (int(act.frame_range[0]), int(act.frame_range[1])) if act else (1, 1)
scn = bpy.context.scene
scn.frame_start, scn.frame_end = f0, f1

# THE BODY: capsules in armature space (rest pose), one vertex group per bone, an Armature modifier.
bm = bmesh.new()
groups = []
import re
MAIN = re.compile(r"^(pelvis|spine_0\d|neck_0\d|head|clavicle_[lr]|upperarm_[lr]|lowerarm_[lr]|hand_[lr]|thigh_[lr]|calf_[lr]"
                  r"|foot_[lr]|ball_[lr]|(thumb|index|middle|ring|pinky)_0[1-3]_[lr])$")
scale = arm.matrix_world.to_scale()[0]
up = (arm.matrix_world.inverted().to_3x3() @ Vector((0, 0, 1))).normalized()
for b in arm.data.bones:
    n = b.name.lower()
    if not MAIN.match(n):
        continue
    rr = next(v for k, v in RAD if n.startswith(k)) / scale  # radii in metres; armature space is centimetres
    head = b.head_local
    # A segment runs from the bone's head to its main child's head: the importer's tails point nowhere useful
    # (the first film on 10 Nov fell apart at the knees on them).
    kids = [c for c in b.children if MAIN.match(c.name.lower())]
    if n == "head":
        geom = bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=rr)
        for v in geom["verts"]:
            v.co += head + up * rr
        k = len(geom["verts"])
        # A nose, so a film shows which way the head turns (the motion 2 reviewer could not tell, 10 Nov).
        # Forward is taken from the rest feet (foot head to ball head), flattened against up.
        fwd = Vector((0, 0, 0))
        for s in ("l", "r"):
            fb, bb = arm.data.bones.get(f"foot_{s}"), arm.data.bones.get(f"ball_{s}")
            if fb and bb:
                fwd += bb.head_local - fb.head_local
        fwd -= up * fwd.dot(up)
        if fwd.length > 1e-6:
            fwd.normalize()
            nl = rr * 0.9
            nose = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=rr * 0.28, radius2=0.0, depth=nl)
            nrot = Vector((0, 0, 1)).rotation_difference(fwd).to_matrix().to_4x4()
            for v in nose["verts"]:
                v.co = nrot @ v.co + head + up * rr + fwd * (rr * 0.85 + nl * 0.5)
            k += len(nose["verts"])
        groups.append((b.name, k))
        continue
    if kids:
        tail = kids[0].head_local
        if n == "pelvis":
            tail = head + up * (0.08 / scale)
    else:
        d = (head - b.parent.head_local).normalized() if b.parent else up
        tail = head + d * rr * 2.5
    length = (tail - head).length
    if length < 1e-4:
        continue
    geom = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=rr, radius2=rr * 0.85, depth=length)
    rot = Vector((0, 0, 1)).rotation_difference((tail - head).normalized()).to_matrix().to_4x4()
    for v in geom["verts"]:
        v.co = rot @ v.co + head + (tail - head) * 0.5
    groups.append((b.name, len(geom["verts"])))
bm.verts.ensure_lookup_table()
me = bpy.data.meshes.new("CapsuleBody")
bm.to_mesh(me)
body = bpy.data.objects.new("CapsuleBody", me)
scn.collection.objects.link(body)
body.parent = arm
body.matrix_parent_inverse.identity()
# Vertex ownership: each primitive's vertices are appended in order, so groups are consecutive ranges.
vcount = len(me.vertices)
pos = 0
for name, k in groups:
    vg = body.vertex_groups.new(name=name)
    vg.add(list(range(pos, pos + k)), 1.0, "REPLACE")
    pos += k
assert pos == vcount, (pos, vcount)
mod = body.modifiers.new("Arm", "ARMATURE")
mod.object = arm
mat = bpy.data.materials.new("Body")
mat.diffuse_color = (0.75, 0.68, 0.58, 1)
me.materials.append(mat)

# BOUNDS OVER THE WHOLE MOTION, and the facing from the rest feet.
def world_pts():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    m = ev.to_mesh()
    pts = [body.matrix_world @ v.co for v in m.vertices]
    ev.to_mesh_clear()
    return pts

lo = Vector((1e9, 1e9, 1e9)); hi = Vector((-1e9, -1e9, -1e9))
for f in range(f0, f1 + 1, max(1, (f1 - f0) // 12)):
    scn.frame_set(f)
    for pb in arm.pose.bones:  # pose bones' world places: the mesh's evaluated copy misled the bounds on 10 Nov
        for p in (arm.matrix_world @ pb.head, arm.matrix_world @ pb.tail):
            lo = Vector(map(min, lo, p)); hi = Vector(map(max, hi, p))
centre = (lo + hi) / 2
height = hi.z - lo.z

def bone_world(name):
    b = arm.data.bones.get(name)
    return arm.matrix_world @ b.head_local if b else None

fl, bl = bone_world("foot_l"), bone_world("ball_l")
fwd = (bl - fl) if (fl and bl) else Vector((0, -1, 0))
fwd.z = 0
fwd = fwd.normalized()
side = fwd.cross(Vector((0, 0, 1))).normalized()

# FLOOR: a grid of 25 cm squares at the lowest point.
bpy.ops.mesh.primitive_grid_add(x_subdivisions=24, y_subdivisions=24, size=6, location=(centre.x, centre.y, lo.z))
grid = bpy.context.active_object
wm = grid.modifiers.new("W", "WIREFRAME"); wm.thickness = 0.01
gm = bpy.data.materials.new("Grid"); gm.diffuse_color = (0.15, 0.15, 0.15, 1); grid.data.materials.append(gm)
scn.world = scn.world or bpy.data.worlds.new("W"); scn.world.color = (0.42, 0.44, 0.45)

scn.render.engine = "BLENDER_WORKBENCH"
scn.display.shading.light = "STUDIO"
scn.display.shading.color_type = "MATERIAL"
scn.display.shading.show_shadows = True
scn.display.shading.show_cavity = True
scn.render.resolution_x, scn.render.resolution_y = 640, 720
scn.render.fps = 24
scn.render.image_settings.file_format = "PNG"

def camera(name, direction):
    cd = bpy.data.cameras.new(name); cd.lens = 50
    cam = bpy.data.objects.new(name, cd); scn.collection.objects.link(cam)
    dist = max(height, (hi - lo).length) * 1.9
    target = Vector((centre.x, centre.y, lo.z + height * 0.5))
    cam.location = target + direction * dist + Vector((0, 0, height * 0.08))
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    return cam

views = {"front": camera("Front", fwd), "side": camera("Side", side)}
for v, cam in views.items():
    if os.path.exists(os.path.join(OUT, v, "f-%05d.png" % (f1 - f0 + 1))):
        continue  # already filmed (a rerun redoes only what is missing)
    scn.camera = cam
    os.makedirs(os.path.join(OUT, v), exist_ok=True)
    for i, f in enumerate(range(f0, f1 + 1)):
        scn.frame_set(f)
        scn.render.filepath = os.path.join(OUT, v, "f-%05d.png" % (i + 1))
        bpy.ops.render.render(write_still=True)

# THE SOURCE CLIP's frames, through the sequencer of a separate scene.
src = bpy.data.scenes.new("Source")
src.sequence_editor_create()
clip = bpy.data.movieclips.load(SRC)
cw, ch = clip.size
nsrc = clip.frame_duration
src.render.resolution_x, src.render.resolution_y = cw, ch
src.render.resolution_percentage = 100
src.render.image_settings.file_format = "PNG"
strips = src.sequence_editor.strips if hasattr(src.sequence_editor, "strips") else src.sequence_editor.sequences
strips.new_movie("src", SRC, channel=1, frame_start=1)
src.frame_start, src.frame_end = 1, nsrc
src.render.filepath = os.path.join(OUT, "source", "f-")
os.makedirs(os.path.join(OUT, "source"), exist_ok=True)
bpy.ops.render.render(animation=True, scene=src.name)

info = {"fbx": FBX, "source": SRC, "anim_frames": f1 - f0 + 1, "anim_range": [f0, f1], "source_frames": nsrc,
        "source_size": [cw, ch], "bones_drawn": len(groups), "height_m_scene": height,
        "forward": list(fwd), "armature_scale": list(arm.matrix_world.to_scale())}
json.dump(info, open(os.path.join(OUT, "film-info.json"), "w"), indent=1)
print("FILMMOTION " + json.dumps(info))
