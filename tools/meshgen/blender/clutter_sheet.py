"""The street clutter's gate pictures: one piece, three views, a figure for scale, its measured size.

    blender --background --factory-startup --python tools/meshgen/blender/clutter_sheet.py -- \
        --piece F:/LedgerTools/tmp/clutter/<id>/<id>.glb --out F:/LedgerTools/tmp/clutter/<id>/sheet

WHY, 29 September (the builder's list, item 10: ten pieces of 1990 British
street clutter, each made against two reference photographs, through the
quality gate, the live Blender route timed against the script route). Both
routes hand this the piece as a .glb, so the pictures the gate judges are made
the same way whichever route made the piece: front, side (from the left) and three-quarter at
eye height (1.6 m), in plain overcast daylight on a grey pavement, a 1.8 m
grey figure a metre to one side for scale, 1024 square each, and the piece's
measured width, depth and height (metres, from its bounding box) written
beside them as dims.json, to be checked against the real thing's.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default


piece = arg("--piece")
out = arg("--out")
if not piece or not out:
    print("clutter_sheet: --piece and --out are needed")
    sys.exit(2)
os.makedirs(out, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=piece)
parts = [o for o in bpy.context.scene.objects if o.type == "MESH"]
if not parts:
    print("clutter_sheet: no mesh in", piece)
    sys.exit(1)

# THE MEASURED SIZE, from every mesh's world bounding box.
lo = Vector((1e9, 1e9, 1e9))
hi = Vector((-1e9, -1e9, -1e9))
for o in parts:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        lo = Vector((min(lo.x, w.x), min(lo.y, w.y), min(lo.z, w.z)))
        hi = Vector((max(hi.x, w.x), max(hi.y, w.y), max(hi.z, w.z)))
size = hi - lo
dims = {"widthM": round(size.x, 3), "depthM": round(size.y, 3), "heightM": round(size.z, 3),
        "baseZ": round(lo.z, 3), "meshes": len(parts),
        "triangles": sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in parts)}
json.dump(dims, open(os.path.join(out, "dims.json"), "w"), indent=1)
print("clutter_sheet dims:", json.dumps(dims))

centre = (lo + hi) / 2
scene = bpy.context.scene

# THE PAVEMENT, THE FIGURE AND THE LIGHT.
bpy.ops.mesh.primitive_plane_add(size=12, location=(centre.x, centre.y, lo.z - 0.001))
ground = bpy.context.object
gmat = bpy.data.materials.new("pavement")
gmat.use_nodes = True
gmat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.32, 0.32, 0.31, 1)
gmat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
ground.data.materials.append(gmat)

fmat = bpy.data.materials.new("figure")
fmat.use_nodes = True
fmat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.55, 0.55, 0.55, 1)
fx = hi.x + 0.9
fy = centre.y + 0.9          # back and to one side, so no view has it in front of the piece
bpy.ops.mesh.primitive_cylinder_add(radius=0.17, depth=1.56, location=(fx, fy, lo.z + 0.78))
body = bpy.context.object
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(fx, fy, lo.z + 1.68))   # the top at 1.80 m
head = bpy.context.object
for o in (body, head):
    o.data.materials.append(fmat)

world = bpy.data.worlds.new("overcast")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.78, 0.8, 0.83, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.2
bpy.ops.object.light_add(type="SUN", location=(centre.x + 3, centre.y - 3, lo.z + 6))
sun = bpy.context.object
sun.data.energy = 2.0
sun.rotation_euler = (math.radians(50), 0, math.radians(35))

scene.render.engine = "CYCLES"
# TRUE COLOURS FOR THE GATE: the default view transform (AgX) washes strong
# colours out (a Belisha globe came out tan), so the pictures use Standard.
scene.view_settings.view_transform = "Standard"
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = scene.render.resolution_y = 1024
scene.render.image_settings.file_format = "PNG"

# THREE VIEWS AT EYE HEIGHT, framed on the piece and the figure together.
span = max(size.x + 1.4, size.y, size.z, 1.9)
target = Vector((centre.x + 0.5, centre.y, lo.z + max(size.z, 1.8) / 2))
for name, yaw in (("front", 0.0), ("three-quarter", 35.0), ("side", -90.0)):
    dist = span * 2.4
    d = Vector((math.sin(math.radians(yaw)), -math.cos(math.radians(yaw)), 0))
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = 50
    cam = bpy.data.objects.new(name, cam_data)
    scene.collection.objects.link(cam)
    cam.location = Vector((target.x, target.y, lo.z + 1.6)) + d * dist
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    scene.camera = cam
    scene.render.filepath = os.path.join(out, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("clutter_sheet view:", scene.render.filepath)
print("clutter_sheet done:", out)
