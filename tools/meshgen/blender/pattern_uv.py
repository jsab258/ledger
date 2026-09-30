"""A "pattern" UV layer for a garment made without a sewing pattern, so the builder's binder can bind it panel by
panel (tools/meshgen/blender/bind_garment.py; NOW.md, Handovers to clothing, 30 September: "please keep that layer,
one island a panel, in every garment you hand over").

    blender -b -P tools/meshgen/blender/pattern_uv.py -- GARMENT.blend OUT_DIR --render CardiganRender --name ron_jumper

Each face is given to a panel: a sleeve when its middle lies beyond the shoulder joint and within --arm-r of the
arm's bones, else the trunk; every separate piece (a band, a cuff, a button) goes with the panel its middle falls in.
Each panel is laid flat by its own projection (the trunk by x and height, a sleeve along and round its arm) in its
own region of the UV square, so the panels are separate islands and the binder's rule (a panel's middle out beyond
1.3 times the half-shoulder is an arm) reads them rightly. The garment's other UV layers are kept.
OUT_DIR gets NAME_render_static.fbx (with the layer) and NAME.blend.
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, OUT = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "garment", str)
RENDER = opt("--render", "CardiganRender", str)
bpy.ops.wm.open_mainfile(filepath=BLEND)
g = bpy.data.objects[RENDER]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
J = lambda n: arm.matrix_world @ arm.pose.bones[n].head
chains = {s: [J("upperarm_" + s), J("lowerarm_" + s), J("hand_" + s)] for s in "lr"}
ARM_R = opt("--arm-r", 0.12)


def seg(p, a, b):
    ab = b - a
    t = max(0.0, min(1.0, (p - a).dot(ab) / max(1e-9, ab.length_squared)))
    return (p - (a + ab * t)).length, t


bm = bmesh.new()
bm.from_mesh(g.data)
bm.transform(g.matrix_world)
bm.faces.ensure_lookup_table()
# separate pieces
comp = {}
for f0 in bm.faces:
    if f0.index in comp:
        continue
    stack, cid = [f0], f0.index
    comp[f0.index] = cid
    while stack:
        f = stack.pop()
        for e in f.edges:
            for f2 in e.link_faces:
                if f2.index not in comp:
                    comp[f2.index] = cid
                    stack.append(f2)
pieces = {}
for f in bm.faces:
    pieces.setdefault(comp[f.index], []).append(f)


def panel_of(c):
    for s in "lr":
        sh = chains[s][0]
        beyond = c.x * (1 if s == "l" else -1) > abs(sh.x) - 0.01
        d = min(seg(c, chains[s][0], chains[s][1])[0], seg(c, chains[s][1], chains[s][2])[0])
        if beyond and d < ARM_R:
            return "arm_" + s
    return "trunk"


main = max(pieces, key=lambda k: len(pieces[k]))
face_panel = {}
for cid, fs in pieces.items():
    if cid == main:
        for f in fs:
            face_panel[f.index] = panel_of(f.calc_center_median())
    else:
        c = sum((f.calc_center_median() for f in fs), Vector()) / len(fs)
        p_ = panel_of(c)
        for f in fs:
            face_panel[f.index] = p_
uvl = bm.loops.layers.uv.get("pattern") or bm.loops.layers.uv.new("pattern")
OFF = {"trunk": (0.0, 0.0), "arm_l": (1.2, 0.0), "arm_r": (2.4, 0.0)}
for f in bm.faces:
    pn = face_panel[f.index]
    ox, oy = OFF[pn]
    for lp in f.loops:
        p = lp.vert.co
        if pn == "trunk":
            u, v = 0.5 + p.x, p.z - 0.5 + (0.0 if p.y < 0 else 1.2 * 0)   # front and back share one island (joined round the sides)
        else:
            s = pn[-1]
            a, b = chains[s][0], chains[s][2]
            ax = (b - a).normalized()
            t = (p - a).dot(ax)
            rad = (p - a) - ax * t
            ang = math.atan2(rad.dot(Vector((0, 1, 0))), rad.dot(ax.cross(Vector((0, 1, 0))).normalized()))
            u, v = 0.5 + ang / (2 * math.pi) * 0.9, t
        lp[uvl].uv = (u + ox, v + oy)
bm.transform(g.matrix_world.inverted())
bm.to_mesh(g.data)
bm.free()
counts = {}
for pn in face_panel.values():
    counts[pn] = counts.get(pn, 0) + 1
print("PATTERN", json.dumps(counts), flush=True)
bpy.ops.object.select_all(action="DESELECT")
g.select_set(True)
bpy.context.view_layer.objects.active = g
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_render_static.fbx"), use_selection=True,
                         object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump({"blend": BLEND, "panels": counts}, open(os.path.join(OUT, "pattern.json"), "w"), indent=1)
