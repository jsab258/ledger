"""The 1990 telephone kiosk, by script: a KX100 in its 1985 to 1991 livery, at real size.

    blender --background --factory-startup --python tools/meshgen/blender/clutter/kx100_kiosk.py -- --out F:/LedgerTools/tmp/clutter/kx100-kiosk/script-1.glb

The script route of the builder's list, item 10. Its form comes from the
research (production/research/street-clutter-1990: 0.89 m square, about
2.18 m tall, stainless frame, back and roof, glazed front and sides in black
frames with a black modesty band, a black header with "Telephone" in yellow,
a yellow handle on a coin kiosk) and two photographs (the Maraig kiosk in the
1985 livery; Paythorne 2017 for the shape). Front faces -y.

NO OPERATOR MARK (29 September): canon makes every brand fictional and lists
the telephone operator's mark and lettering as owed by the brand bible, so the
real British Telecom "T" is left off; the word "Telephone" is generic and stays.
"""
import math
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "kx100.glb"
W = 0.89            # square
H = 2.18            # to the roof's top
POST = 0.04

bpy.ops.wm.read_factory_settings(use_empty=True)


def srgb(r, g, b):
    f = lambda c: (c / 255.0) ** 2.2
    return (f(r), f(g), f(b))


def material(name, rgb, rough=0.5, metal=0.0, glass=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if glass:
        b.inputs["Transmission Weight"].default_value = 1.0
        b.inputs["IOR"].default_value = 1.5
        b.inputs["Alpha"].default_value = 0.25
        if hasattr(m, "blend_method"):
            m.blend_method = "BLEND"
    return m


STEEL = material("stainless", srgb(200, 202, 205), 0.35, 1.0)
BLACK = material("black", srgb(18, 18, 18), 0.6)
YELLOW = material("yellow", srgb(245, 200, 0), 0.45)
GLASS = material("glass", srgb(200, 205, 208), 0.05, 0.0, glass=True)
GREY = material("phone-grey", srgb(110, 112, 115), 0.5, 0.3)


def box(name, size, loc, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.scale = size
    bpy.ops.object.transform_apply(scale=True)
    ob.data.materials.append(mat)
    return ob


def text(name, body, size, loc, rot, mat, depth=0.002):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    t = bpy.context.object
    t.data.body = body
    t.data.size = size
    t.data.extrude = depth
    t.data.align_x = "CENTER"
    t.data.align_y = "CENTER"
    t.data.offset = 0.0025             # bold, upright: the 1985 livery (italic came with 1991's)
    bpy.ops.object.convert(target="MESH")
    ob = bpy.context.object
    ob.name = name
    ob.data.materials.append(mat)
    return ob


h = W / 2
# NO PLINTH: the corner posts run down to the pavement as feet, and the front
# and sides stop 12 cm short of it for ventilation (the review: the real
# kiosk is open at the foot). A low floor plate inside.
for sx in (-1, 1):
    for sy in (-1, 1):
        box("post", (POST, POST, H - 0.05), (sx * (h - POST / 2), sy * (h - POST / 2), (H - 0.05) / 2), STEEL)
box("floor", (W - 2 * POST, W - 2 * POST, 0.03), (0, 0, 0.10), BLACK)
box("roof", (W + 0.03, W + 0.03, 0.05), (0, 0, H - 0.025), STEEL)

# THE BACK: solid stainless steel, the payphone on its inside face.
box("back", (W - 2 * POST, 0.02, H - 0.13), (0, h - 0.01, 0.08 + (H - 0.13) / 2), STEEL)
box("phone", (0.30, 0.15, 0.45), (0, h - 0.02 - 0.075, 1.30), GREY)
box("handset", (0.06, 0.05, 0.22), (-0.18, h - 0.06, 1.30), BLACK)
box("keypad", (0.12, 0.005, 0.12), (0.03, h - 0.02 - 0.1525, 1.25), STEEL)

# THE THREE GLAZED FACES: front (the door, -y), left (-x), right (+x).
# Each: lower pane 0.11 to 1.00 m, the black band 1.00 to 1.12 m, upper pane
# 1.12 to 1.93 m, the black header 1.93 to 2.13 m, thin black frames.
faces = [("front", (0, -1)), ("left", (-1, 0)), ("right", (1, 0))]
inner = W - 2 * POST
for name, (nx, ny) in faces:
    def panel(label, zc, hh, thick, mat, inset=0.0):
        if ny:
            return box("%s-%s" % (name, label), (inner, thick, hh), (0, ny * (h - 0.01 - inset), zc), mat)
        return box("%s-%s" % (name, label), (thick, inner, hh), (nx * (h - 0.01 - inset), 0, zc), mat)
    panel("glass-low", 0.61, 0.78, 0.008, GLASS)
    panel("glass-up", 1.525, 0.81, 0.008, GLASS)
    # the chest-height band: on the coin kiosk's door it is the yellow moulded
    # handle panel, running across the door; on the sides it is black
    panel("band", 1.06, 0.12, 0.012, YELLOW if name == "front" else BLACK)
    panel("header", 2.03, 0.20, 0.03, BLACK)
    panel("frame-bottom", 0.215, 0.03, 0.025, BLACK)
    panel("frame-top", 1.915, 0.03, 0.025, BLACK)
    # the word on the header, facing out
    if ny:
        text("%s-word" % name, "Telephone", 0.12, (0, ny * (h + 0.007), 2.03), (math.radians(90), 0, 0), YELLOW)
    else:
        text("%s-word" % name, "Telephone", 0.12, (nx * (h + 0.007), 0, 2.03), (math.radians(90), 0, math.radians(90 * nx)), YELLOW)

# THE DOOR: its vertical frame bars and the yellow handle strip at its right edge.
for x in (-inner / 2 + 0.015, inner / 2 - 0.015):
    box("door-bar", (0.03, 0.025, 1.71), (x, -h + 0.01, 1.055), BLACK)
box("pull", (0.06, 0.035, 0.10), (inner / 2 - 0.06, -h - 0.012, 1.06), YELLOW)   # the pull at the band's end

bpy.ops.object.select_all(action="SELECT")
bpy.context.view_layer.objects.active = bpy.data.objects["floor"]
bpy.ops.object.join()
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
tris = sum(len(p.vertices) - 2 for p in bpy.context.object.data.polygons)
print("kx100 triangles:", tris)
bpy.ops.export_scene.gltf(filepath=OUT)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace(".glb", ".blend"))
print("kx100 written:", OUT)
