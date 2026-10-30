"""The baked game mesh seen with its maps: at the third-person camera's distance and close up.

    blender -b --factory-startup -P tools/meshgen/blender/look_baked.py -- LOW.blend BAKED_DIR [--name zip_jacket]
        [--tint 0.55,0.55,0.55] [--samples 32] [--out DIR] [--around 1.5,4] [--aim 0.8] [--soft] [--tag new]
    (30 October 2026, Tom's jeans' construction details: --around D1,D2 draws front, back and side views at each
    distance in metres, the camera at eye height 1.6 m aimed at --aim metres up the body, in place of the jacket's four;
    --soft lights it by a large soft key beside the camera and a soft fill from the sky instead of the sun; --out puts
    the pictures there, named look_<tag>_<view>_<distance>.png)

WHY, 27 October 2026 (Tom's zip jacket, the bake chain's step 7 check: production/art/clothing/tom-outfit/
BAKE-PLAN-2026-10-27.md, "pictures at the game camera"). The game mesh gets its normal map (OpenGL green for Blender),
its colour times --tint (the jacket's colour is still to be chosen; neutral grey until then) and its occlusion, its
roughness and metal from the packed map, and is drawn on the body by Cycles from the front at 2.6 m (about where the
game's camera follows Tom), three-quarter at 1.2 m, and close on the zip and a pocket.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
LOW, BAKED = argv[0], argv[1]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
NAME = opt("--name", "zip_jacket", str)
TINT = [float(x) for x in opt("--tint", "0.55,0.55,0.55", str).split(",")]
SAMPLES = opt("--samples", 32, int)
OUT = opt("--out", BAKED, str)
AROUND = [float(x) for x in opt("--around", "", str).split(",") if x]
AIM = opt("--aim", 0.8)
SOFT = "--soft" in argv
TAG = opt("--tag", "", str)
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=LOW)
low = bpy.data.objects["Low"]
for o in bpy.data.objects:
    if o.type == "MESH":
        o.hide_render = o.name not in ("Low", "Body")
m = bpy.data.materials.new("baked")
m.use_nodes = True
nt = m.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
out = nt.nodes.new("ShaderNodeOutputMaterial")
bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
nt.links.new(bsdf.outputs[0], out.inputs[0])
uv = nt.nodes.new("ShaderNodeUVMap")
uv.uv_map = "UVMap"


def tex(fname, colour):
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = bpy.data.images.load(os.path.join(BAKED, fname))
    t.image.colorspace_settings.name = "sRGB" if colour else "Non-Color"
    nt.links.new(uv.outputs[0], t.inputs[0])
    return t


col = tex(NAME + "_colour_ao.png", True)
pk = tex(NAME + "_packed.png", False)
nm = tex(NAME + "_normal_gl.png", False)
tint = nt.nodes.new("ShaderNodeMix")
tint.data_type = "RGBA"
tint.blend_type = "MULTIPLY"
tint.inputs[0].default_value = 1.0
nt.links.new(col.outputs["Color"], tint.inputs[6])
tint.inputs[7].default_value = (*TINT, 1.0)
ao = nt.nodes.new("ShaderNodeMix")
ao.data_type = "RGBA"
ao.blend_type = "MULTIPLY"
ao.inputs[0].default_value = 1.0
nt.links.new(tint.outputs[2], ao.inputs[6])
nt.links.new(col.outputs["Alpha"], ao.inputs[7])
nt.links.new(ao.outputs[2], bsdf.inputs["Base Color"])
sep = nt.nodes.new("ShaderNodeSeparateColor")
nt.links.new(pk.outputs["Color"], sep.inputs[0])
nt.links.new(sep.outputs[0], bsdf.inputs["Roughness"])
nt.links.new(sep.outputs[2], bsdf.inputs["Metallic"])
nmap = nt.nodes.new("ShaderNodeNormalMap")
nmap.uv_map = "UVMap"
nt.links.new(nm.outputs["Color"], nmap.inputs["Color"])
nt.links.new(nmap.outputs[0], bsdf.inputs["Normal"])
low.data.materials.clear()
low.data.materials.append(m)
for poly in low.data.polygons:
    poly.use_smooth = True

scn = bpy.context.scene
scn.render.engine = "CYCLES"
scn.cycles.device = "CPU"
scn.cycles.samples = SAMPLES
scn.render.resolution_x, scn.render.resolution_y = 1000, 1200
world = scn.world or bpy.data.worlds.new("w")
scn.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.35, 0.36, 0.38, 1)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
cam.data.lens = 50
scn.collection.objects.link(cam)
scn.camera = cam
if SOFT:
    # an overcast street's light: the sky's even fill, and one large soft key a little above and beside the camera
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.62, 0.64, 0.67, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.3
    key = bpy.data.objects.new("key", bpy.data.lights.new("key", "AREA"))
    key.data.shape, key.data.size = "DISK", 2.5
    key.data.energy = 300.0
    scn.collection.objects.link(key)
else:
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(-30))
    scn.collection.objects.link(sun)
zs = [(low.matrix_world @ v.co) for v in low.data.vertices]
cz = (max(p.z for p in zs) + min(p.z for p in zs)) / 2
if AROUND:
    # the body faces -y; side is his right, seen from -x
    views = []
    for dist in AROUND:
        for vn, d in (("front", (0, -1)), ("back", (0, 1)), ("side", (-1, 0))):
            views.append(("%s_%s_%gm" % (TAG or "look", vn, dist), (d[0] * dist, d[1] * dist, 1.6), (0, 0, AIM), d))
    for nm_, loc, tgt, d in views:
        cam.location = Vector(loc)
        cam.rotation_euler = (Vector(tgt) - cam.location).to_track_quat("-Z", "Y").to_euler()
        if SOFT:
            side_ = Vector((-d[1], d[0], 0.0))
            key.location = Vector((d[0] * 2.2, d[1] * 2.2, 2.4)) + side_ * 1.2
            key.rotation_euler = (Vector((0, 0, 1.0)) - key.location).to_track_quat("-Z", "Y").to_euler()
        scn.render.filepath = os.path.join(OUT, nm_ + ".png")
        bpy.ops.render.render(write_still=True)
else:
    for nm_, loc, tgt in (("game", (0.4, -2.6, 1.6), (0, 0, cz)), ("threequarter", (0.7, -1.0, 1.35), (0, 0, cz + 0.05)),
                          ("zip", (0.08, -0.45, 1.3), (0.0, -0.12, 1.22)), ("pocket", (0.25, -0.5, 1.05), (0.1, -0.1, 1.05))):
        cam.location = Vector(loc)
        cam.rotation_euler = (Vector(tgt) - cam.location).to_track_quat("-Z", "Y").to_euler()
        scn.render.filepath = os.path.join(OUT, "look_%s.png" % nm_)
        bpy.ops.render.render(write_still=True)
print("LOOKED")
