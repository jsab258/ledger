"""The wooden telegraph pole of a 1990 terraced street, by script, at real size.

    blender --background --factory-startup --python tools/meshgen/blender/clutter/telegraph_pole.py -- --out F:/LedgerTools/tmp/clutter/telegraph-pole/script-1.glb

The script route of the builder's list, item 10 (a reserve from the research,
production/research/street-clutter-1990, taken because the street already has
its lamp column). A creosoted timber pole about 8.5 m above the pavement,
tapering from 0.24 m at the foot to 0.17 m at the top, steel climbing steps
from about 2.4 m, a pole-top distribution point (a ring with insulated drop
wires fanning out to the houses; short stubs here, the wires themselves drawn
by the street to each house), a small number plate. No operator's mark.
"""
import math
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "telegraph-pole.glb"

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


TIMBER = material("creosote-timber", srgb(78, 60, 42), 0.85)
STEEL = material("galvanised", srgb(130, 132, 130), 0.5, 0.8)
BLACK = material("wire-black", srgb(15, 15, 15), 0.6)
PLATE = material("plate", srgb(210, 210, 200), 0.5)
H = 8.5

bpy.ops.mesh.primitive_cone_add(vertices=20, radius1=0.12, radius2=0.085, depth=H, location=(0, 0, H / 2))
pole = bpy.context.object
pole.name = "pole"
pole.data.materials.append(TIMBER)
for p in pole.data.polygons:
    p.use_smooth = True
bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.086, location=(0, 0, H))
bpy.context.object.scale = (1, 1, 0.4)
bpy.context.object.data.materials.append(TIMBER)


def radius_at(z):
    return 0.12 - 0.035 * z / H


# THE STEPS: short steel bars, alternating sides, every 0.45 m from 2.4 m up to 7.5 m.
z, side = 2.4, 1
while z < 7.5:
    r = radius_at(z)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.012, depth=0.22,
                                        location=(side * (r + 0.09), 0, z), rotation=(0, math.radians(90), 0))
    bpy.context.object.data.materials.append(STEEL)
    z, side = z + 0.45, -side

# THE DISTRIBUTION POINT: a steel band and ring near the top, drop wires fanning out.
top = H - 0.35
bpy.ops.mesh.primitive_torus_add(major_segments=24, minor_segments=6, major_radius=0.16, minor_radius=0.012, location=(0, 0, top))
bpy.context.object.data.materials.append(STEEL)
bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=radius_at(top) + 0.01, depth=0.10, location=(0, 0, top))
bpy.context.object.data.materials.append(STEEL)
for k, ang in enumerate((-150, -110, -70, -30, 20, 70, 130)):
    a = math.radians(ang)
    length = 1.6
    dx, dy = math.cos(a), math.sin(a)
    mid = (0.16 * dx + dx * length / 2, 0.16 * dy + dy * length / 2, top - 0.02 - math.sin(math.radians(12)) * length / 2)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.004, depth=length, location=mid,
                                        rotation=(0, math.radians(90 + 12), a))   # falling away towards the houses
    bpy.context.object.data.materials.append(BLACK)

# THE NUMBER PLATE at 2.0 m, facing -y.
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -radius_at(2.0) - 0.004, 2.0))
bpy.context.object.scale = (0.07, 0.006, 0.10)
bpy.context.object.data.materials.append(PLATE)

bpy.ops.object.select_all(action="SELECT")
bpy.context.view_layer.objects.active = pole
bpy.ops.object.join()
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
print("telegraph_pole triangles:", sum(len(p.vertices) - 2 for p in bpy.context.object.data.polygons))
bpy.ops.export_scene.gltf(filepath=OUT)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace(".glb", ".blend"))
print("telegraph_pole written:", OUT)
