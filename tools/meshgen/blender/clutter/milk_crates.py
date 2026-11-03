"""The grocer's stack of three milk crates with six empty pint bottles (variant MC3), by script, at real size,
from its target.

    F:/LedgerTools/blender52/blender-5.2.2-windows-x64/blender.exe --background --factory-startup --python tools/meshgen/blender/clutter/milk_crates.py -- --out F:/LedgerTools/tmp/clutter/milk-crates/script-1.glb

Every number comes from the target, production/cloud-week/targets/street-dressing/milk-crates/target.json
(millimetres, z up, the long side's front looking -y, the pivot at the base's centre on the paving): variant
MC3's 93 parts, boxes by centre and size, the bottles by their two cylinders each; the materials' sRGB and
roughness. Written in metres as one .glb, one mesh per material under one root (the street names a clutter
row by its material, so one mesh a material keeps each row's id single).

What the target leaves to the builder, and what was chosen (3 November, the corner plan's step 10):
- the name band is plain moulded plastic, with no lettering: the dairy's name is a placeholder until the town
  mints it (target H1), and placeholders never reach his page (RULINGS 3 Oct); a moulded name in the crate's own
  colour does not read at the street's distances anyway;
- the rims' tops and the stacking lugs are a second, faded material (crate_rim): the target's wear says the
  plastic is chalkier and scuffed pale along the rim's top, which a flat colour per part can carry; the slots'
  dirt is the dark the open slots already show; the floor's 36 drain slots (a mask in the target) are left out,
  as nothing but the top crate's floor is ever seen, and that under its bottles;
- each bottle is one lathe inside its two target cylinders (body r 32 to z 650, a shoulder narrowing to the
  neck's r 14 by z 676, a lip ring r 16 at the top), not two stacked tubes; 12 sides;
- THE LATTICE, after its first editor pictures: the target's full-height slots, with one rib on each end wall,
  read in the game camera as an open red rack, not a crate. Every wall gets a lower bar 14 high at z 50 to 64,
  and the name band (z 118 to 184) runs round the end walls too, so each wall is the grid of openings the
  photograph S2 shows; the hand holds stay as the openings above the band;
- THE BOTTLES' GLASS, after the same pictures: the street's window glass is dark and mirror-like, and the six
  bottles all but vanished in it; they wear their own glass, a milk-filmed grey-green (sRGB 150, 165, 158)
  nearly as smooth as the target's, the way empty bottles read at a few metres;
- the 2 to 4 mm edge radii and the lugs' recesses are not modelled (below what any view of the street resolves).
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
OUT = arg("--out", "milk_crates.glb")
TARGET = arg("--target", os.path.join(REPO, "production", "cloud-week", "targets", "street-dressing", "milk-crates",
                                      "target.json"))
SIDES = 12
#: THE FADED RIM, a Judgement within the target's wear: its body red (168, 40, 36) lifted and greyed the way
#: sun-faded polypropylene goes, chalkier and paler along the top.
RIM_SRGB = (184, 74, 66)
BOTTLE_SRGB = (150, 165, 158)
#: The lattice's added bar and the band carried round the ends (millimetres, in each crate's own height).
BAR_Z = (50.0, 64.0)
BAND_Z = (118.0, 184.0)

bpy.ops.wm.read_factory_settings(use_empty=True)
target = json.load(open(TARGET, encoding="utf-8"))
mats_t = target["materials"]


def lin(c):
    return (c / 255.0) ** 2.2


def material(name, srgb, rough):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (lin(srgb[0]), lin(srgb[1]), lin(srgb[2]), 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = 0.0
    return m


MATS = {
    "crate_plastic": material("crate_plastic", mats_t["crate_plastic"]["srgb"], mats_t["crate_plastic"]["rough"]),
    "crate_rim": material("crate_rim", RIM_SRGB, 0.65),
    "bottle_glass": material("bottle_glass", BOTTLE_SRGB, 0.08),
}
BMS = {k: bmesh.new() for k in MATS}


def box(bm, c, s):
    x0, x1 = (c[0] - s[0] / 2) / 1000.0, (c[0] + s[0] / 2) / 1000.0
    y0, y1 = (c[1] - s[1] / 2) / 1000.0, (c[1] + s[1] / 2) / 1000.0
    z0, z1 = (c[2] - s[2] / 2) / 1000.0, (c[2] + s[2] / 2) / 1000.0
    v = [bm.verts.new(p) for p in ((x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                   (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1))]
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        bm.faces.new([v[i] for i in f])


def bottle(bm, cx, cy, z0, z_neck_top, r_body, r_neck):
    """One milk bottle by lathe, inside the target's body and neck cylinders (millimetres in, metres out)."""
    prof = [(0.0, z0), (r_body - 3, z0), (r_body, z0 + 4), (r_body, 650.0), (r_body - 6, 662.0),
            (r_neck + 4, 674.0), (r_neck, 680.0), (r_neck, z_neck_top - 6), (r_neck + 2, z_neck_top - 5),
            (r_neck + 2, z_neck_top - 1), (r_neck, z_neck_top), (0.0, z_neck_top)]
    rings = []
    for r, z in prof:
        if r == 0.0:
            rings.append([bm.verts.new((cx / 1000.0, cy / 1000.0, z / 1000.0))])
            continue
        rings.append([bm.verts.new(((cx + r * math.cos(2 * math.pi * i / SIDES)) / 1000.0,
                                    (cy + r * math.sin(2 * math.pi * i / SIDES)) / 1000.0, z / 1000.0))
                      for i in range(SIDES)])
    for a, b in zip(rings, rings[1:]):
        for i in range(SIDES):
            j = (i + 1) % SIDES
            if len(a) == 1:
                bm.faces.new((a[0], b[j], b[i]))
            elif len(b) == 1:
                bm.faces.new((a[i], a[j], b[0]))
            else:
                bm.faces.new((a[i], a[j], b[j], b[i]))


parts = {p["id"]: p for p in target["variants"]["MC3"]["parts"]}
n_box = n_bottle = 0
for pid, p in parts.items():
    if p["type"] == "box":
        mat = "crate_rim" if ("_rim_" in pid or "_lug_" in pid) else p["material"]
        box(BMS[mat], p["c"], p["s"])
        n_box += 1
    elif pid.split("_")[1].startswith("bottle"):
        neck = parts[pid.replace("bottle", "neck")]
        bottle(BMS["bottle_glass"], p["p0"][0], p["p0"][1], p["p0"][2], neck["p1"][2], p["r0"], neck["r0"])
        n_bottle += 1

# THE LATTICE (see the docstring): each crate's floor sets its height; a lower bar on all four walls inside its
# posts, and the name band round the two end walls, each 4 thick like the walls they cross.
for k in (1, 2, 3):
    z0 = parts["c%d_floor" % k]["c"][2] - 5.0
    for zlo, zhi, walls in ((BAR_Z[0], BAR_Z[1], "fblr"), (BAND_Z[0], BAND_Z[1], "lr")):
        zc, zs = z0 + (zlo + zhi) / 2.0, zhi - zlo
        for w in walls:
            if w in "fb":
                box(BMS["crate_plastic"], (0.0, -147.0 if w == "f" else 147.0, zc), (376.0, 4.0, zs))
            else:
                box(BMS["crate_plastic"], (-202.0 if w == "l" else 202.0, 0.0, zc), (4.0, 266.0, zs))
            n_box += 1

root = bpy.data.objects.new("milk_crates", None)
bpy.context.scene.collection.objects.link(root)
tris = 0
for name, bm in BMS.items():
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = root
    ob.data.materials.append(MATS[name])
    if name == "glass":
        for poly in me.polygons:
            poly.use_smooth = True
    tris += sum(len(poly.vertices) - 2 for poly in me.polygons)

lo = [min(v.co[k] for ob in bpy.data.objects if ob.type == "MESH" for v in ob.data.vertices) for k in range(3)]
hi = [max(v.co[k] for ob in bpy.data.objects if ob.type == "MESH" for v in ob.data.vertices) for k in range(3)]
print("milk-crates boxes=%d bottles=%d triangles=%d size_mm=%s" % (
    n_box, n_bottle, tris, [round((h - l) * 1000.0, 1) for l, h in zip(lo, hi)]))
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB")
print("milk-crates written:", OUT)
