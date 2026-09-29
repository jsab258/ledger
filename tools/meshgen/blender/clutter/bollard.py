"""The old cast-iron cannon bollard of a terrace corner, by script, at real size.

    blender --background --factory-startup --python tools/meshgen/blender/clutter/bollard.py -- --out F:/LedgerTools/tmp/clutter/bollard/script-1.glb

The script route of the builder's list, item 10. From the research
(production/research/street-clutter-1990: cast-iron cannon bollards at terrace
corners) and the listed cast-iron cannon-and-ball bollards of Leeds (about
0.75 m, a cylindrical shaft, a roll moulding and a ball top): plain black.
"""
import math
import sys

import bmesh
import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "bollard.glb"

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


BLACK = material("bollard-black", srgb(22, 22, 22), 0.55)
WHITE = material("bollard-white", srgb(225, 225, 220), 0.6)


def lathe(name, profile, mat, segments=32):
    bm = bmesh.new()
    rings = [[bm.verts.new((r * math.cos(2 * math.pi * i / segments), r * math.sin(2 * math.pi * i / segments), z))
              for i in range(segments)] for r, z in profile]
    for k in range(len(rings) - 1):
        for i in range(segments):
            j = (i + 1) % segments
            bm.faces.new((rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


# THE CANNON-AND-BALL, as the listed Leeds bollards (Historic England's list
# text, Queen Street, Leeds: mid 19th century cast iron, about 0.75 m, a
# cylindrical shaft, a roll moulding and a cannon-ball top): a slightly tapered
# shaft, a roll moulding under a short neck, the ball on top.
shaft = [(0.105, 0.0), (0.105, 0.015), (0.100, 0.03), (0.090, 0.58)]
roll = [(0.090, 0.585), (0.104, 0.595), (0.108, 0.61), (0.104, 0.625), (0.085, 0.635), (0.050, 0.645), (0.045, 0.66)]
lathe("bollard", shaft + roll + [(0.0, 0.66)], BLACK)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.065, location=(0, 0, 0.70))
ball = bpy.context.object
ball.data.materials.append(BLACK)
for p in ball.data.polygons:
    p.use_smooth = True

bpy.ops.object.select_all(action="SELECT")
bpy.context.view_layer.objects.active = bpy.data.objects["bollard"]
bpy.ops.object.join()
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
print("bollard triangles:", sum(len(p.vertices) - 2 for p in bpy.context.object.data.polygons))
bpy.ops.export_scene.gltf(filepath=OUT)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace(".glb", ".blend"))
print("bollard written:", OUT)
