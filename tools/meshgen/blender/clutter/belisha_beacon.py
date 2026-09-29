"""The Belisha beacon of a 1990 zebra crossing, by script, at real size.

    blender --background --factory-startup --python tools/meshgen/blender/clutter/belisha_beacon.py -- --out F:/LedgerTools/tmp/clutter/belisha-beacon/script-1.glb

The script route of the builder's list, item 10. From the research
(production/research/street-clutter-1990: the 1971 regulations, amended 1990;
globe 275 to 335 mm, its centre 2.1 to 3.1 m up; post bands 275 to 335 mm,
the lowest black; a 76 mm post) and the photograph of the classic beacon in
Fetter Lane (Basher Eyre, 2010, CC BY-SA): one post of the pair, a 30 cm
amber globe on a black collar, its centre 2.5 m up, the post banded black and
white in 30 cm bands above a black foot. The globe's material glows; the game
flashes it (0.75 s on, 0.75 s off).
"""
import math
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "belisha.glb"

bpy.ops.wm.read_factory_settings(use_empty=True)


def srgb(r, g, b):
    f = lambda c: (c / 255.0) ** 2.2
    return (f(r), f(g), f(b))


def material(name, rgb, rough=0.5, emit=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
        b.inputs["Emission Strength"].default_value = emit
    return m


BLACK = material("black", srgb(20, 20, 20), 0.5)
WHITE = material("white", srgb(232, 232, 228), 0.5)
AMBER = material("globe-amber", srgb(255, 165, 0), 0.25, emit=0.4)   # saturated amber-yellow, lit or not

R = 0.038                 # the post's radius (76 mm)
GLOBE_Z = 2.50            # the globe's centre
GLOBE_R = 0.15            # 30 cm across


def cyl(name, r, z0, z1, mat, verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=z1 - z0, location=(0, 0, (z0 + z1) / 2))
    ob = bpy.context.object
    ob.name = name
    ob.data.materials.append(mat)
    return ob


# THE FOOT: a wider black base, then the black lowest band up to 0.9 m.
cyl("foot", 0.068, 0.0, 0.10, BLACK)
cyl("band-0", R, 0.10, 0.90, BLACK)
# THE BANDS: 30 cm, white and black, up to the collar.
z, k = 0.90, 0
top = GLOBE_Z - GLOBE_R - 0.10
while z < top - 0.01:
    z1 = min(z + 0.30, top)
    cyl("band-%d" % (k + 1), R, z, z1, WHITE if k % 2 == 0 else BLACK)
    z, k = z1, k + 1
# THE COLLAR: a black cup under the globe.
bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.045, radius2=0.085, depth=0.10, location=(0, 0, top + 0.05))
bpy.context.object.data.materials.append(BLACK)
# THE GLOBE and a small black cap on top.
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=GLOBE_R, location=(0, 0, GLOBE_Z))
bpy.context.object.data.materials.append(AMBER)
for p in bpy.context.object.data.polygons:
    p.use_smooth = True
cyl("cap", 0.02, GLOBE_Z + GLOBE_R - 0.005, GLOBE_Z + GLOBE_R + 0.015, BLACK, verts=12)

bpy.ops.object.select_all(action="SELECT")
bpy.context.view_layer.objects.active = bpy.data.objects["foot"]
bpy.ops.object.join()
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
print("belisha triangles:", sum(len(p.vertices) - 2 for p in bpy.context.object.data.polygons))
bpy.ops.export_scene.gltf(filepath=OUT)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace(".glb", ".blend"))
print("belisha written:", OUT)
