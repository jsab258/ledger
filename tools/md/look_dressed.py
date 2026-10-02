"""A man dressed in the proof suit, textured, in a soft overcast light, for my own check against the bar before the
builder's in-game test: front, three-quarter, side, back and a close three-quarter of the chest and lapels.

    blender -b -P tools/md/look_dressed.py -- BODY.fbx JACKET.blend JACKET_NAME SHIRT.fbx TEX_DIR OUT_PREFIX
        [--size 1200] [--samples 48]

BODY.fbx the man's body (the FullBody, head on); JACKET.blend tools/md/finish_md_jacket.py's file; SHIRT.fbx
tools/md/shirt_and_tie.py's; TEX_DIR tools/md/cloth_textures.py's.

WHY, 2 October: the gate's first check is mine, against the Hook sheet and the KCD2 frames; the grey looks
(tools/md/look_md.py) show the cut but not the cloth. These are Cycles on the processor, an overcast sky and no
sun, as the Hook sheet's street is lit. Never the gate's final pictures: those come from the game's own camera and
light (CLAUDE.md), the builder's in-game test.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
BODY, JACKET, JNAME, SHIRT, TEX, PREFIX = argv[:6]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


SIZE, SAMPLES = opt("--size", 1200, int), opt("--samples", 48, int)
bpy.ops.wm.open_mainfile(filepath=JACKET)
for o in [o for o in bpy.data.objects if o.name != JNAME]:
    bpy.data.objects.remove(o, do_unlink=True)
jacket = bpy.data.objects[JNAME]
before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=BODY)
bpy.ops.import_scene.fbx(filepath=SHIRT)
new = [o for o in bpy.data.objects if o not in before]
meshes = [o for o in new if o.type == "MESH"]
shirt = next(o for o in meshes if any(m and m.name.startswith("M_shirt") for m in o.data.materials))
bodies = [o for o in meshes if o is not shirt]
body = max(bodies, key=lambda o: len(o.data.vertices))
for o in bodies:
    if o is not body and "LOD0" not in o.name:
        o.hide_render = True
for o in bodies:
    if o.name.endswith(("LOD1", "LOD2", "LOD3", "LOD4", "LOD5", "LOD6", "LOD7")):
        o.hide_render = True
# the shirt's armature modifier off (the reference pose is its rest)
for m in shirt.modifiers:
    m.show_render = False


def material(name, tex, tile=1.0, rough=0.8, flat=None):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = rough
    if flat is not None:
        bsdf.inputs["Base Color"].default_value = flat
        return mat
    uv = nt.nodes.new("ShaderNodeUVMap")
    uv.uv_map = "UVMap"
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (tile, tile, 1)
    nt.links.new(uv.outputs["UV"], mp.inputs["Vector"])
    img = nt.nodes.new("ShaderNodeTexImage")
    img.image = bpy.data.images.load(os.path.join(TEX, tex + "_basecolor.png"))
    nt.links.new(mp.outputs["Vector"], img.inputs["Vector"])
    nt.links.new(img.outputs["Color"], bsdf.inputs["Base Color"])
    nimg = nt.nodes.new("ShaderNodeTexImage")
    nimg.image = bpy.data.images.load(os.path.join(TEX, tex + "_normal.png"))
    nimg.image.colorspace_settings.name = "Non-Color"
    nt.links.new(mp.outputs["Vector"], nimg.inputs["Vector"])
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nm.inputs["Strength"].default_value = 0.6
    nt.links.new(nimg.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


cloth = material("cloth", "suit_jacket", rough=0.75)
button = material("button", None, rough=0.35, flat=(0.03, 0.025, 0.02, 1))
for i, m in enumerate(jacket.data.materials):
    jacket.data.materials[i] = button if m and "Button" in m.name else cloth
for i, m in enumerate(shirt.data.materials):
    shirt.data.materials[i] = material("shirt", "shirt", rough=0.7) if m.name.startswith("M_shirt") else \
        material("tie", "tie", rough=0.45)
skin = material("skin", None, rough=0.55, flat=(0.55, 0.42, 0.36, 1))
for o in bodies:
    o.data.materials.clear()
    o.data.materials.append(skin)
for o in (jacket, shirt):
    for p in o.data.polygons:
        p.use_smooth = True
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.render.resolution_x = SIZE
sc.render.resolution_y = int(SIZE * 1.25)
sc.view_settings.view_transform = "AgX"
w = bpy.data.worlds.new("overcast")
w.use_nodes = True
bg = w.node_tree.nodes["Background"]
sky = w.node_tree.nodes.new("ShaderNodeTexSky")
try:
    sky.sky_type = "HOSEK_WILKIE"
    sky.turbidity = 8.0
    sky.sun_direction = (0.3, -0.5, 0.8)
except Exception:
    pass
bg.inputs["Strength"].default_value = 0.9
bg.inputs["Color"].default_value = (0.75, 0.78, 0.82, 1)
sc.world = w
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.lens = 85
J = Vector((0, 0, 1.25))
for name, ang, at, dist in (("front", 0, J, 4.6), ("three-quarter", 35, J, 4.6), ("side", 90, J, 4.6),
                            ("back", 180, J, 4.6), ("close", 30, Vector((0, 0, 1.45)), 1.9)):
    a = math.radians(ang)
    d = Vector((math.sin(a), -math.cos(a), 0.06))
    cam.location = at + d * dist
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = "%s-%s.png" % (PREFIX, name)
    bpy.ops.render.render(write_still=True)
print("DRESSED", PREFIX, flush=True)
