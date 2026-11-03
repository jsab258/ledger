"""The 1990 telephone kiosk (variant KX1, the door kiosk in its 1985 to 1991 livery), by script, at real size,
from its target.

    F:/LedgerTools/blender52/blender-5.2.2-windows-x64/blender.exe --background --factory-startup --python tools/meshgen/blender/clutter/kx100_kiosk.py -- --out F:/LedgerTools/tmp/clutter/kx100-kiosk/script-2.glb

REBUILT 3 November (the corner plan's step 10, "mend the kiosk"): the 29 September script's kiosk disagreed with
its target's photograph in six places and had no payphone a passer-by could see (the target's reuse table:
production/cloud-week/targets/street-dressing/phone-box, which replaces it). Every number now comes from that
target's target.json (millimetres, z up, the door looking -y, the pivot at the base's centre on the paving):
KX1's 44 parts, boxes by centre and size and the three hinges as cylinders, and the materials' sRGB, roughness
and metal. Written in metres as one .glb, one mesh per material (the street names a clutter row by its
material). The material names are the old kiosk's (stainless, black, yellow, glass, phone-grey), so the street
reads the kiosk's glass as its own glass as before (terrace-front.py CLUTTER_SAME_AS); the header's word is a
sixth, letter.

What the target leaves to the builder, and what was chosen:
- THE WORD: "Telephone" in the project's OFL grotesque Libre Franklin (production/fonts/evening-paper; the
  target asks for an OFL grotesque such as Liberation Sans), its capitals 100 mm tall, centred on the header,
  pale yellow-white (240, 224, 150), 2 mm proud. On the door's header and on both sides' fascias, as the old
  kiosk had it: the target's one photograph is head on and shows only the door's header, and a kiosk's word is
  read from up and down the street; the target forbids anything but the word, which this keeps;
- the upper pane's logo zone stays empty (the target's text.logo_zone);
- the lid's folded edges, the posts' fixings and the payphone's slots are not modelled (below what the street's
  views resolve); the target's wear (the panes' tide mark, rain streaks, scratches, the faded frame, the litter
  under the rail) is not drawn: flat colours carry the street's clutter, and it is listed as a shortfall.
"""
import json
import math
import os
import sys

import bmesh
import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default


try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("--python") + 1]))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = arg("--out", "kx100.glb")
TARGET = arg("--target", os.path.join(REPO, "production", "cloud-week", "targets", "street-dressing", "phone-box",
                                      "target.json"))
FONT = os.path.join(REPO, "production", "fonts", "evening-paper", "LibreFranklin-500.ttf")
CAP_MM = 100.0
LETTER_SRGB = (240, 224, 150)
#: The target's material, the name it keeps in the model (the old kiosk's names).
NAMES = {"stainless": "stainless", "black_plastic": "black", "handle_yellow": "yellow", "glass": "glass",
         "phone_grey": "phone-grey"}
SIDES = 12

bpy.ops.wm.read_factory_settings(use_empty=True)
target = json.load(open(TARGET, encoding="utf-8"))
mats_t = target["materials"]


def lin(c):
    return (c / 255.0) ** 2.2


def material(name, srgb, rough, metal):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (lin(srgb[0]), lin(srgb[1]), lin(srgb[2]), 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = 1.0 if metal else 0.0
    return m


MATS = {NAMES[k]: material(NAMES[k], v["srgb"], v["rough"], v["metal"]) for k, v in mats_t.items()}
MATS["letter"] = material("letter", LETTER_SRGB, 0.5, False)
BMS = {k: bmesh.new() for k in MATS if k != "letter"}


def box(bm, c, s):
    x0, x1 = (c[0] - s[0] / 2) / 1000.0, (c[0] + s[0] / 2) / 1000.0
    y0, y1 = (c[1] - s[1] / 2) / 1000.0, (c[1] + s[1] / 2) / 1000.0
    z0, z1 = (c[2] - s[2] / 2) / 1000.0, (c[2] + s[2] / 2) / 1000.0
    v = [bm.verts.new(p) for p in ((x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                   (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1))]
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        bm.faces.new([v[i] for i in f])


def cyl(bm, p0, p1, r):
    """An upright cylinder (the hinges run along z)."""
    rings = []
    for z in (p0[2], p1[2]):
        rings.append([bm.verts.new(((p0[0] + r * math.cos(2 * math.pi * i / SIDES)) / 1000.0,
                                    (p0[1] + r * math.sin(2 * math.pi * i / SIDES)) / 1000.0, z / 1000.0))
                      for i in range(SIDES)])
    for i in range(SIDES):
        j = (i + 1) % SIDES
        bm.faces.new((rings[0][i], rings[0][j], rings[1][j], rings[1][i]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[1])


parts = target["variants"]["KX1"]["parts"]
for p in parts:
    if p["type"] == "box":
        box(BMS[NAMES[p["material"]]], p["c"], p["s"])
    elif p["type"] == "cyl":
        cyl(BMS[NAMES[p["material"]]], p["p0"], p["p1"], p["r0"])

objs = []
for name, bm in BMS.items():
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(MATS[name])
    objs.append(ob)


def word(header, outward):
    """'Telephone' on a header's outer face: capitals CAP_MM tall, centred, 2 mm proud; outward is the
    header's outer normal in plan, (0, -1) for the door's, (-1, 0) and (1, 0) for the sides'."""
    c, s = header["c"], header["s"]
    bpy.ops.object.text_add()
    t = bpy.context.object
    t.data.body = "Telephone"
    t.data.font = bpy.data.fonts.load(FONT)
    t.data.size = 1.0
    # a flat face 2 mm proud, its curves at two steps a segment: extruded at Blender's twelve the three words
    # alone were 29,000 triangles, four times the old kiosk whole
    t.data.extrude = 0.0
    t.data.resolution_u = 2
    t.data.align_x = "CENTER"
    t.data.align_y = "BOTTOM_BASELINE"
    bpy.ops.object.convert(target="MESH")
    ob = bpy.context.object
    # the baseline is the text's y 0 and its tallest letters set the height: scale them to CAP_MM
    k = (CAP_MM / 1000.0) / max(v.co.y for v in ob.data.vertices)
    ob.scale = (k, k, k)
    bpy.ops.object.transform_apply(scale=True)
    # stand it up on the header's face: the text lies in x-y facing +z; a quarter turn about x faces it -y,
    # then a turn about z faces it `outward`, reading left to right from outside
    half = (s[1] if outward[1] else s[0]) / 2.0 / 1000.0
    face = (c[0] / 1000.0 + outward[0] * (half + 0.002), c[1] / 1000.0 + outward[1] * (half + 0.002))
    yaw = {(0, -1): 0.0, (-1, 0): -math.pi / 2, (1, 0): math.pi / 2}[outward]
    ob.rotation_euler = (math.pi / 2, 0.0, yaw)
    ob.location = (face[0], face[1], c[2] / 1000.0 - CAP_MM / 2000.0)
    bpy.ops.object.transform_apply(location=True, rotation=True)
    ob.data.materials.clear()
    ob.data.materials.append(MATS["letter"])
    ob.name = "letter_" + header["id"]
    return ob


by_id = {p["id"]: p for p in parts}
letters = [word(by_id["f_header"], (0, -1)), word(by_id["sl_header"], (-1, 0)), word(by_id["sr_header"], (1, 0))]
bpy.ops.object.select_all(action="DESELECT")
for ob in letters:
    ob.select_set(True)
bpy.context.view_layer.objects.active = letters[0]
bpy.ops.object.join()
letters[0].name = "letter"
letters[0].data.name = "letter"
objs.append(letters[0])

root = bpy.data.objects.new("kx100_kiosk", None)
bpy.context.scene.collection.objects.link(root)
tris = 0
for ob in objs:
    ob.parent = root
    tris += sum(len(poly.vertices) - 2 for poly in ob.data.polygons)
meshes = [ob for ob in bpy.data.objects if ob.type == "MESH"]
lo = [min((ob.matrix_world @ v.co)[k] for ob in meshes for v in ob.data.vertices) for k in range(3)]
hi = [max((ob.matrix_world @ v.co)[k] for ob in meshes for v in ob.data.vertices) for k in range(3)]
print("kx100 parts=%d triangles=%d size_mm=%s" % (len(parts), tris, [round((h - l) * 1000.0, 1) for l, h in zip(lo, hi)]))
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB")
print("kx100 written:", OUT)
