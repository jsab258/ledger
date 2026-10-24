"""IN PROGRESS, parked 23 October 2026 (his message): the launderette's washing (its close review's fault 2) by Blender's cloth simulation,
a prototype run outside the build, not yet wired into sw_shops_laundry.display.

What it does: three cotton sheets 0.9 x 0.7 m (40 x 30 quads) dropped one after another from 0.3 m above wicker_basket_01's rim, each
applied and made a collider for the next; then a subdivision and 2 mm of thickness.
What was learnt (each run about 1 to 3.5 minutes on the PC):
  - shrink 0.5, quality 5, distances 1.5 / 3 mm, 120 frames, the wicker as collider: the cloth stays in the basket but crumples into
    sharp teeth and slips through the weave's gaps (cloth_proto_0.5.png in the session's scratch).
  - quality 8, distances 3 / 4 mm, collision quality 5, 150 frames: every sheet blew away (to 7 m), with the wicker or with an inner box.
  - back to the first settings with shrink 0.65, 120 frames: stable again, the sheets inside the basket (sheet 2 took 200 s).
  - judged by eye (24 Oct, 02:10): with the wicker as collider the cloth fell through its floor and gaps (shrink 0.65); with an
    open box just inside the weave as collider (its faces turned inward, the first settings, shrink 0.6, three sheets) it lies
    as soft cloth in the basket, a blue sheet under cream and a crumpled red one, in 45 s: the best so far, but low (top 0.088
    against the rim's 0.117).
  - five sheets (shrink 0.7): the later ones crumple into small balls and the run takes 13 minutes: no.
Next: three sheets with less shrink (0.8), so the cloth heaps over the rim; then the weave tile at 3 mm cells and a normal map,
and DSP-03 inside the group (the review's exact fix).
Run: F:/LedgerTools/bpyenv/Scripts/python.exe sw_cloth_proto.py <shrink> <frames> [wicker|proxy] [sheets]
"""
"""Prototype: three cotton sheets dropped into wicker_basket_01 by Blender's cloth simulation (the launderette's close review, fault 2).
Run with the bpy module's python. Writes a render and timings to the scratchpad."""
import math
import os
import random
import sys
import time

import bpy
import bmesh

OUT = os.path.dirname(os.path.abspath(__file__))
SHRINK = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
FRAMES = int(sys.argv[2]) if len(sys.argv) > 2 else 120

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
bpy.ops.import_scene.gltf(filepath="F:/LedgerTools/polyhaven/wicker_basket_01/1k/wicker_basket_01_1k.gltf")
basket = [o for o in sc.objects if o.type == "MESH"]
mn = [min((o.matrix_world @ v.co)[i] for o in basket for v in o.data.vertices) for i in range(3)]
mx = [max((o.matrix_world @ v.co)[i] for o in basket for v in o.data.vertices) for i in range(3)]
print("basket", [round(v, 3) for v in mn], [round(v, 3) for v in mx])
bx, by = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
rim = mx[2]
# the wicker has gaps the cloth slips through: an open box just inside its weave stands for it (removed after)
inset = 0.012
bm = bmesh.new()
x0, x1, y0, y1, z0, z1 = mn[0] + inset, mx[0] - inset, mn[1] + inset, mx[1] - inset, mn[2] + 0.012, rim - 0.004
vs = [bm.verts.new(c) for c in ((x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1))]
for f in ((0, 1, 2, 3), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
    bm.faces.new([vs[i] for i in f])
# and the rim, a flat ring out to the weave's outer edge
r_ = [bm.verts.new(c) for c in ((mn[0], mn[1], rim), (mx[0], mn[1], rim), (mx[0], mx[1], rim), (mn[0], mx[1], rim))]
for a, b in ((0, 1), (1, 2), (2, 3), (3, 0)):
    bm.faces.new([vs[4 + a], vs[4 + b], r_[b], r_[a]])
import mathutils
cen = mathutils.Vector(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
for f in bm.faces:
    f.normal_update()
    fc = f.calc_center_median()
    want = mathutils.Vector((0, 0, 1)) if abs(fc.z - rim) < 1e-4 else (cen - fc)
    if f.normal.dot(want) < 0:
        f.normal_flip()
pm = bpy.data.meshes.new("proxy")
bm.to_mesh(pm)
bm.free()
proxy = bpy.data.objects.new("proxy", pm)
sc.collection.objects.link(proxy)
USE_PROXY = len(sys.argv) > 3 and sys.argv[3] == "proxy"
if USE_PROXY:
    proxy.modifiers.new("Collision", "COLLISION")
else:
    for o in basket:
        o.modifiers.new("Collision", "COLLISION")
        o.collision.thickness_outer = 0.003
        o.collision.cloth_friction = 8.0
if USE_PROXY:
    proxy.collision.thickness_outer = 0.004
    proxy.collision.thickness_inner = 0.004
    proxy.collision.cloth_friction = 5.0
proxy.hide_render = True
# the bed under it
bpy.ops.mesh.primitive_plane_add(size=3.0, location=(bx, by, mn[2] - 0.0005))
bed = bpy.context.object
bed.modifiers.new("Collision", "COLLISION")
bed.collision.thickness_outer = 0.003

rnd = random.Random(4)
sheets = []
t0 = time.time()
NSHEETS = int(sys.argv[4]) if len(sys.argv) > 4 else 3
for i in range(NSHEETS):
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=40, y_segments=30, size=0.5)
    for v in bm.verts:
        v.co.x *= 0.9
        v.co.y *= 0.7
    me = bpy.data.meshes.new("sheet_%d" % i)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("sheet_%d" % i, me)
    sc.collection.objects.link(ob)
    ob.location = (bx + rnd.uniform(-0.03, 0.03), by + rnd.uniform(-0.03, 0.03), rim + 0.30 + 0.02 * i)
    ob.rotation_euler = (math.radians(rnd.uniform(-8, 8)), math.radians(rnd.uniform(-8, 8)), rnd.uniform(0, 6.28))
    cl = ob.modifiers.new("Cloth", "CLOTH")
    s = cl.settings
    s.quality = 5
    s.mass = 0.3
    s.air_damping = 1.0
    s.tension_stiffness = s.compression_stiffness = 15.0
    s.shear_stiffness = 5.0
    s.bending_stiffness = 0.5
    s.shrink_min = SHRINK
    c = cl.collision_settings
    c.use_self_collision = True
    c.self_distance_min = 0.0015
    c.distance_min = 0.003
    c.collision_quality = 4
    cl.point_cache.frame_start = 1
    cl.point_cache.frame_end = FRAMES
    sc.frame_start, sc.frame_end = 1, FRAMES
    for f in range(1, FRAMES + 1):
        sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    new = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    ob.modifiers.clear()
    ob.data = new
    ob.matrix_world = ob.matrix_world   # the evaluated mesh is in object space
    sc.frame_set(1)
    m = ob.modifiers.new("Collision", "COLLISION")
    ob.collision.thickness_outer = 0.003
    sheets.append(ob)
    print("sheet", i, "done", round(time.time() - t0, 1), "s")
# extents
for ob in sheets:
    ws = [ob.matrix_world @ v.co for v in ob.data.vertices]
    print(ob.name, "x", round(min(w.x for w in ws) - bx, 3), round(max(w.x for w in ws) - bx, 3), "y", round(min(w.y for w in ws) - by, 3), round(max(w.y for w in ws) - by, 3),
          "z", round(min(w.z for w in ws), 3), round(max(w.z for w in ws), 3), "rim", round(rim, 3))
for ob in sheets:
    ob.modifiers.clear()
    sd = ob.modifiers.new("Sub", "SUBSURF")
    sd.levels = sd.render_levels = 1
    so = ob.modifiers.new("Solid", "SOLIDIFY")
    so.thickness = 0.002
    so.offset = 0.0
    dg = bpy.context.evaluated_depsgraph_get()
    new = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    ob.modifiers.clear()
    ob.data = new
    print(ob.name, "faces", len(ob.data.polygons))
cols = [(0.43, 0.55, 0.65), (0.78, 0.70, 0.55), (0.43, 0.15, 0.12), (0.62, 0.45, 0.24), (0.36, 0.48, 0.38)]
for ob, cc in zip(sheets, cols):
    mat = bpy.data.materials.new(ob.name)
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*cc, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
# render a look
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam)
cam.location = (bx, by - 1.1, rim + 0.45)
cam.rotation_euler = (math.radians(68), 0, 0)
cam.data.lens = 50
sc.camera = cam
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sc.collection.objects.link(sun)
sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(30))
sun.data.energy = 3.0
w = bpy.data.worlds.new("w")
sc.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.8
sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = 960, 720
sc.render.filepath = os.path.join(OUT, "cloth_proto_%s_%d.png" % (SHRINK, NSHEETS))
bpy.ops.render.render(write_still=True)
print("rendered", sc.render.filepath, round(time.time() - t0, 1), "s")
