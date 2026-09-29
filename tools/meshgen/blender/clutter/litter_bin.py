"""The council litter bin of a 1990 high street, by script, at real size.

    blender --background --factory-startup --python tools/meshgen/blender/clutter/litter_bin.py -- --out F:/LedgerTools/tmp/clutter/litter-bin/script-1.glb

The script route of the builder's list, item 10. The research found no dated
source for the usual type (production/research/street-clutter-1990, the
weakest piece); its first candidate, an open-top steel bin on a post marked
LITTER, in a council colour, is made here: a round bin about 0.40 m across and
0.55 m deep, its rim at about 0.95 m, on a 76 mm post, with a rolled rim, a
row of drainage holes at the foot and LITTER in white on the front.
"""
import math
import sys

import bmesh
import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "litter-bin.glb"

bpy.ops.wm.read_factory_settings(use_empty=True)


def srgb(r, g, b):
    f = lambda c: (c / 255.0) ** 2.2
    return (f(r), f(g), f(b))


def material(name, rgb, rough=0.5, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


GREEN = material("council-green", srgb(30, 62, 40), 0.5, 0.3)
WHITE = material("letters-white", srgb(235, 235, 228), 0.5)
DARK = material("inside-dark", srgb(12, 12, 12), 0.9)

# THE POST, 76 mm, to 1.0 m.
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.038, depth=1.0, location=(0, 0.25, 0.5))
bpy.context.object.name = "post"
bpy.context.object.data.materials.append(GREEN)

# THE BIN: an open cylinder with a floor, walls 3 mm, rim rolled; its back
# against the post, its floor at 0.40 m, its rim at 0.95 m.
R, Z0, Z1 = 0.20, 0.40, 0.95
bm = bmesh.new()
seg = 32
outer_b = [bm.verts.new((R * math.cos(2 * math.pi * i / seg), R * math.sin(2 * math.pi * i / seg), Z0)) for i in range(seg)]
outer_t = [bm.verts.new((R * math.cos(2 * math.pi * i / seg), R * math.sin(2 * math.pi * i / seg), Z1)) for i in range(seg)]
inner_t = [bm.verts.new(((R - 0.004) * math.cos(2 * math.pi * i / seg), (R - 0.004) * math.sin(2 * math.pi * i / seg), Z1)) for i in range(seg)]
inner_b = [bm.verts.new(((R - 0.004) * math.cos(2 * math.pi * i / seg), (R - 0.004) * math.sin(2 * math.pi * i / seg), Z0 + 0.004)) for i in range(seg)]
for i in range(seg):
    j = (i + 1) % seg
    bm.faces.new((outer_b[i], outer_b[j], outer_t[j], outer_t[i]))
    bm.faces.new((outer_t[i], outer_t[j], inner_t[j], inner_t[i]))
    bm.faces.new((inner_t[i], inner_t[j], inner_b[j], inner_b[i]))
bm.faces.new(list(reversed(outer_b)))
bm.faces.new(inner_b)
me = bpy.data.meshes.new("bin")
bm.to_mesh(me)
bm.free()
b = bpy.data.objects.new("bin", me)
bpy.context.scene.collection.objects.link(b)
b.data.materials.append(GREEN)
for p in b.data.polygons:
    p.use_smooth = True
# the dark inside, so the open top reads as a bin
bpy.ops.mesh.primitive_cylinder_add(vertices=seg, radius=R - 0.005, depth=0.005, location=(0, 0, Z0 + 0.01))
bpy.context.object.data.materials.append(DARK)
# the rolled rim
bpy.ops.mesh.primitive_torus_add(major_segments=seg, minor_segments=6, major_radius=R, minor_radius=0.008, location=(0, 0, Z1))
bpy.context.object.data.materials.append(GREEN)
# the bracket to the post
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.215, 0.80))
bpy.context.object.scale = (0.08, 0.04, 0.06)
bpy.context.object.data.materials.append(GREEN)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.215, 0.55))
bpy.context.object.scale = (0.08, 0.04, 0.06)
bpy.context.object.data.materials.append(GREEN)

# LITTER in white on the front, bent round the bin.
bpy.ops.object.text_add(location=(0, 0, 0.78), rotation=(1.5708, 0, 0))
t = bpy.context.object
t.data.body = "LITTER"
t.data.size = 0.075
t.data.extrude = 0.0008
t.data.offset = 0.002
t.data.align_x = "CENTER"
t.data.align_y = "CENTER"
bpy.ops.object.convert(target="MESH")
lt = bpy.context.object
lt.data.materials.append(WHITE)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
for v in lt.data.vertices:
    depth = v.co.y + 0.0008                      # 0 at the back face
    v.co.y = -math.sqrt(max((R + 0.0012) ** 2 - v.co.x ** 2, 0.0)) + depth

bpy.ops.object.select_all(action="SELECT")
bpy.context.view_layer.objects.active = bpy.data.objects["bin"]
bpy.ops.object.join()
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
print("litter_bin triangles:", sum(len(p.vertices) - 2 for p in bpy.context.object.data.polygons))
bpy.ops.export_scene.gltf(filepath=OUT)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace(".glb", ".blend"))
print("litter_bin written:", OUT)
