"""The bus stop of a 1990 high street, by script: a pole, the flag (TSRGD diagram 970) and a timetable case.

    blender --background --factory-startup --python tools/meshgen/blender/clutter/bus_stop.py -- --out F:/LedgerTools/tmp/clutter/bus-stop/script-1.glb

The script route of the builder's list, item 10. From the research
(production/research/street-clutter-1990: diagram 970, 450 by 375 mm, near
the top of a steel pole about 3 m tall, a timetable case at eye height; after
the 1986 deregulation operators added their own flags, which would be brands,
so this carries the plain diagram only) and the diagram itself (Wikimedia
Commons, UK traffic sign 970: a white plate, black border, black bus). The
flag faces -y here for the pictures; in the street it stands across the kerb.
"""
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "bus-stop.glb"

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


POLE = material("pole-grey", srgb(120, 124, 120), 0.6, 0.4)     # galvanised, weathered
WHITE = material("sign-white", srgb(238, 238, 232), 0.4)
BLACK = material("sign-black", srgb(15, 15, 15), 0.5)
CASE = material("case-grey", srgb(70, 74, 70), 0.5, 0.3)
PERSPEX = material("case-perspex", srgb(225, 228, 225), 0.1)


def box(name, size, loc, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.scale = size
    bpy.ops.object.transform_apply(scale=True)
    ob.data.materials.append(mat)
    return ob


# THE POLE: 76 mm, 3.0 m, a cap on top.
bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.038, depth=3.0, location=(0, 0, 1.5))
bpy.context.object.name = "pole"
bpy.context.object.data.materials.append(POLE)
bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.042, location=(0, 0, 3.0))
bpy.context.object.data.materials.append(POLE)

# THE FLAG: 450 by 375 mm, its top at 2.95 m, clamped to the pole's front.
FW, FH, FT = 0.45, 0.375, 0.006
fz = 2.95 - FH / 2
fy = -0.038 - FT / 2 - 0.01
box("flag", (FW, FT, FH), (0, fy, fz), WHITE)
for sy in (-1, 1):
    y = fy + sy * (FT / 2 + 0.0008)
    # the black border, 12 mm, as four strips
    box("border-top", (FW, 0.0015, 0.012), (0, y, fz + FH / 2 - 0.006), BLACK)
    box("border-bottom", (FW, 0.0015, 0.012), (0, y, fz - FH / 2 + 0.006), BLACK)
    box("border-left", (0.012, 0.0015, FH), (-FW / 2 + 0.006, y, fz), BLACK)
    box("border-right", (0.012, 0.0015, FH), (FW / 2 - 0.006, y, fz), BLACK)
    # THE DIAGRAM AS DRAWN (the review: without the "Bus Stop" panel the plate
    # reads as a generic picture sign): a black line divides off the lower
    # quarter, which reads "Bus Stop"; the bus above, a single-decker side on,
    # its tall windscreen at the front, four windows, wheels with white hubs.
    by = y + sy * 0.0008
    box("divider", (FW, 0.0015, 0.012), (0, y, fz - FH / 2 + 0.095), BLACK)
    bpy.ops.object.text_add(location=(0, by, fz - FH / 2 + 0.047), rotation=(1.5708, 0, 0 if sy < 0 else 3.14159))
    t = bpy.context.object
    t.data.body = "Bus Stop"
    t.data.size = 0.052
    t.data.extrude = 0.0006
    t.data.offset = 0.0012
    t.data.align_x = "CENTER"
    t.data.align_y = "CENTER"
    bpy.ops.object.convert(target="MESH")
    bpy.context.object.data.materials.append(BLACK)
    bz = fz + 0.055                                # the bus's centre in the upper panel
    box("bus-body", (0.32, 0.0015, 0.13), (0.0, by, bz), BLACK)
    front = -0.16 if sy < 0 else 0.16             # the bus faces the same way on both faces' viewers' left
    box("bus-windscreen", (0.035, 0.0016, 0.085), (front + (0.03 if sy < 0 else -0.03), by + sy * 0.0003, bz + 0.012), WHITE)
    for wx in (-0.075, -0.015, 0.045, 0.105):
        box("bus-window", (0.048, 0.0016, 0.035), (wx * (1 if sy < 0 else -1), by + sy * 0.0003, bz + 0.025), WHITE)
    for wx in (-0.09, 0.09):
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.026, depth=0.0015, location=(wx, by + sy * 0.0002, bz - 0.068),
                                            rotation=(1.5708, 0, 0))
        bpy.context.object.data.materials.append(BLACK)
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.011, depth=0.0015, location=(wx, by + sy * 0.0006, bz - 0.068),
                                            rotation=(1.5708, 0, 0))
        bpy.context.object.data.materials.append(WHITE)
box("clamp", (0.09, 0.03, 0.04), (0, -0.03, fz + 0.12), POLE)
box("clamp2", (0.09, 0.03, 0.04), (0, -0.03, fz - 0.12), POLE)

# THE TIMETABLE CASE: 0.35 by 0.45, 6 cm deep, its centre 1.55 m up, on the pole's front.
box("case", (0.35, 0.06, 0.45), (0, -0.038 - 0.03, 1.55), CASE)
box("case-face", (0.31, 0.004, 0.41), (0, -0.038 - 0.061, 1.55), PERSPEX)
for k, zz in enumerate((1.70, 1.66, 1.62, 1.55, 1.51, 1.47, 1.40)):
    box("times-%d" % k, (0.24, 0.001, 0.012), (0, -0.038 - 0.0635, zz), BLACK)

bpy.ops.object.select_all(action="SELECT")
bpy.context.view_layer.objects.active = bpy.data.objects["pole"]
bpy.ops.object.join()
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
print("bus_stop triangles:", sum(len(p.vertices) - 2 for p in bpy.context.object.data.polygons))
bpy.ops.export_scene.gltf(filepath=OUT)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace(".glb", ".blend"))
print("bus_stop written:", OUT)
