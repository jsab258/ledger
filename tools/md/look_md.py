"""Quick pictures of what Marvelous Designer holds: its OBJ export (avatar and garment) drawn from the front, side,
back and three-quarter, flat-shaded (Workbench, seconds a picture), the garment charcoal, the body pale.

    blender -b -P tools/md/look_md.py -- SCENE.obj OUT_PREFIX [--size 900] [--garment-only]

WHY, 2 October (the jacket proof in Marvelous): the bridge script cannot see Marvelous's 3D window, so each
arrangement and drape is exported and looked at here before the next step. These are working looks for me, never
the gate's pictures (those come from the game's camera and light, the builder's in-game test).
"""
import math
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, PREFIX = argv[0], argv[1]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


SIZE = opt("--size", 900, int)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=SRC, up_axis="Y", forward_axis="NEGATIVE_Z", use_split_objects=True, use_split_groups=True)
objs = [o for o in bpy.data.objects if o.type == "MESH"]
# the avatar's parts by their names in Marvelous's export (the garment's pieces are named after the pattern's)
AV = ("shoe", "hair", "body", "eye", "tooth", "lash", "avatar", "skin", "head")
avatar = [o for o in objs if any(w in o.name.lower() for w in AV)]
# --pieces: each garment piece its own colour (to see which piece is where), named in OUT_PREFIX-pieces.txt
PALETTE = [(0.85, 0.2, 0.2), (0.2, 0.6, 0.9), (0.95, 0.75, 0.1), (0.3, 0.75, 0.3), (0.7, 0.3, 0.8), (0.95, 0.5, 0.1),
           (0.1, 0.3, 0.7), (0.6, 0.6, 0.6), (0.9, 0.4, 0.6), (0.4, 0.9, 0.8), (0.5, 0.35, 0.2), (0.1, 0.1, 0.1),
           (1.0, 1.0, 1.0), (0.55, 0.55, 0.1), (0.0, 0.5, 0.4), (0.6, 0.1, 0.35), (0.3, 0.3, 0.55), (0.95, 0.85, 0.6)]
legend = []
for n, o in enumerate(sorted(objs, key=lambda o: o.name)):
    m = bpy.data.materials.new(o.name)
    is_av = o in avatar
    if is_av:
        m.diffuse_color = (0.80, 0.72, 0.66, 1)
    elif "--pieces" in argv:
        c = PALETTE[len(legend) % len(PALETTE)]
        m.diffuse_color = (*c, 1)
        legend.append("%s %s" % (o.name, c))
    else:
        m.diffuse_color = (0.16, 0.16, 0.17, 1)
    o.data.materials.clear()
    o.data.materials.append(m)
    if is_av and "--garment-only" in argv:
        o.hide_render = True
lo = Vector((min(min((o.matrix_world @ Vector(c)).x for c in o.bound_box) for o in objs),
             min(min((o.matrix_world @ Vector(c)).y for c in o.bound_box) for o in objs),
             min(min((o.matrix_world @ Vector(c)).z for c in o.bound_box) for o in objs)))
hi = Vector((max(max((o.matrix_world @ Vector(c)).x for c in o.bound_box) for o in objs),
             max(max((o.matrix_world @ Vector(c)).y for c in o.bound_box) for o in objs),
             max(max((o.matrix_world @ Vector(c)).z for c in o.bound_box) for o in objs)))
centre = (lo + hi) / 2
height = hi.z - lo.z
print("BOUNDS", [round(c, 3) for c in lo], [round(c, 3) for c in hi], "objects", [o.name for o in objs], flush=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.color_type = "MATERIAL"
sc.display.shading.show_cavity = True
sc.display.shading.show_specular_highlight = False   # the studio light's sheen made wool read as satin
sc.render.resolution_x = SIZE
sc.render.resolution_y = int(SIZE * 1.25)
sc.world = bpy.data.worlds.new("w")
sc.world.color = (0.9, 0.9, 0.9)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.type = "ORTHO"
cam.data.ortho_scale = height * 1.08
cam.data.clip_start, cam.data.clip_end = height * 0.01, height * 10   # Marvelous writes millimetres
# the garment's own height when only the garment is drawn
garment = [o for o in objs if o not in avatar]
glo = min(min((o.matrix_world @ Vector(c)).z for c in o.bound_box) for o in garment) if garment else lo.z
ghi = max(max((o.matrix_world @ Vector(c)).z for c in o.bound_box) for o in garment) if garment else hi.z
views = [("front", 0, centre, height * 1.08), ("three-quarter", 35, centre, height * 1.08), ("side", 90, centre, height * 1.08),
         ("back", 180, centre, height * 1.08)]
# close views of the garment's upper half: the lapels, collar, shoulders and chest, where a jacket is judged
up = Vector((centre.x, centre.y, ghi - (ghi - glo) * 0.3))
views += [("close-front", 0, up, (ghi - glo) * 0.75), ("close-three-quarter", 35, up, (ghi - glo) * 0.75),
          ("close-side", 90, up, (ghi - glo) * 0.75), ("close-back", 180, up, (ghi - glo) * 0.75)]
for name, ang, at, scale in views:
    a = math.radians(ang)
    # the avatar faces -Y in Blender after the OBJ import (Marvelous's +Z forward)
    d = Vector((math.sin(a), -math.cos(a), 0))
    cam.data.ortho_scale = scale
    cam.location = at + d * (height * 3)
    cam.rotation_euler = (d * -1).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = "%s-%s.png" % (PREFIX, name)
    bpy.ops.render.render(write_still=True)
# from above, the collar and lapels round the neck
cam.data.ortho_scale = (ghi - glo) * 0.6
cam.location = Vector((centre.x, centre.y, ghi + height))
cam.rotation_euler = (0, 0, 0)
sc.render.filepath = "%s-top.png" % PREFIX
for o in avatar:
    o.hide_render = True
bpy.ops.render.render(write_still=True)
if legend:
    open(PREFIX + "-pieces.txt", "w").write("\n".join(legend))
print("LOOKED", PREFIX, flush=True)
