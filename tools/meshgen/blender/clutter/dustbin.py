"""The galvanised steel dustbin of a 1990 back yard, by script, at real size.

    blender --background --factory-startup --python tools/meshgen/blender/clutter/dustbin.py -- --out F:/LedgerTools/tmp/clutter/dustbin/script-1.glb

The script route of the builder's list, item 10. From the research
(production/research/street-clutter-1990: a round galvanised bin to BS 792,
about 575 mm tall, 450 mm across the top and 400 mm at the foot, pressed ribs,
two side handles, a domed lid with a handle; dull, dented grey): the bin with
its lid on.
"""
import math
import sys

import bmesh
import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "dustbin.glb"

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


ZINC = material("galvanised", srgb(150, 152, 150), 0.55, 0.85)     # dull, weathered zinc


def lathe(name, profile, mat, segments=40, cap_bottom=True, cap_top=True):
    bm = bmesh.new()
    rings = []
    for r, z in profile:
        rings.append([bm.verts.new((r * math.cos(2 * math.pi * i / segments), r * math.sin(2 * math.pi * i / segments), z))
                      for i in range(segments)])
    for k in range(len(rings) - 1):
        for i in range(segments):
            j = (i + 1) % segments
            bm.faces.new((rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]))
    if cap_bottom:
        bm.faces.new(list(reversed(rings[0])))
    if cap_top:
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


# THE BIN: a frustum 0.40 m at the foot to 0.45 m at the rim, 0.55 m tall to the rim,
# a rolled foot ring, three pressed ribs, a rolled rim.
prof = [(0.200, 0.0), (0.206, 0.006), (0.206, 0.02), (0.201, 0.03)]
for zc in (0.13, 0.28, 0.43):                  # the ribs: a raised band 2 cm tall, 6 mm proud
    r = 0.200 + 0.025 * (zc / 0.55)
    prof += [(r, zc - 0.012), (r + 0.006, zc - 0.006), (r + 0.006, zc + 0.006), (r, zc + 0.012)]
prof += [(0.224, 0.535), (0.231, 0.542), (0.231, 0.552), (0.224, 0.556)]
lathe("bin", prof, ZINC)

# THE LID: a shallow dome overlapping the rim, from 0.548 to about 0.60 m, and its handle.
lathe("lid", [(0.236, 0.548), (0.236, 0.558), (0.225, 0.566), (0.19, 0.582), (0.12, 0.595), (0.0, 0.600)], ZINC,
      cap_top=False)
bpy.ops.mesh.primitive_torus_add(major_segments=20, minor_segments=6, major_radius=0.05, minor_radius=0.008, location=(0, 0, 0.60),
                                 rotation=(math.radians(90), 0, 0))
bpy.context.object.scale = (1.0, 1.0, 0.5)
bpy.context.object.data.materials.append(ZINC)

# THE SIDE HANDLES: a loop on each side, 0.44 m up.
for sx in (-1, 1):
    bpy.ops.mesh.primitive_torus_add(major_segments=16, minor_segments=6, major_radius=0.05, minor_radius=0.007, location=(sx * 0.235, 0, 0.44),
                                     rotation=(0, math.radians(90), 0))
    bpy.context.object.scale = (0.45, 1.0, 1.0)
    bpy.context.object.data.materials.append(ZINC)

bpy.ops.object.select_all(action="SELECT")
bpy.context.view_layer.objects.active = bpy.data.objects["bin"]
bpy.ops.object.join()
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
print("dustbin triangles:", sum(len(p.vertices) - 2 for p in bpy.context.object.data.polygons))
bpy.ops.export_scene.gltf(filepath=OUT)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace(".glb", ".blend"))
print("dustbin written:", OUT)
