"""The proof jacket as Marvelous Designer draped it, made a game mesh for the skinning chain (tools/meshgen/blender/
skin_garment.py): one welded mesh on the body it was draped on, at game weight, with edge thickness, buttons, its
pattern islands, a cloth-scale UV and the skirt marked to simulate; and the shell-only simulation mesh.

    blender -b -P tools/md/finish_md_jacket.py -- DRAPE.obj SPEC.json BODY.fbx OUT.blend NAME [--tris 30000]
        [--thick 0.003] [--tile 0.25] [--sim-tris 4000] [--skirt-from 0.04] [--lift MM]

DRAPE.obj is Marvelous's export (garment, and the avatar, which is dropped), millimetres, y up; SPEC.json the
jacket's specification (tools/md/jaeger_spec.py: each piece's outline, the buttons' places); BODY.fbx the body it
was draped on (its skeleton gives the hip line). OUT.blend holds NAME (the render mesh) and NAME_sim (the sim mesh).

WHY, 2 October (the jacket proof): the chain that skins a garment (bind_garment.py, skin_garment.py; the builder's
in-game findings of 1 October) takes a game mesh whose sewing panels are its "pattern" UV islands, a "UVMap" for the
cloth's texture, materials, and a SimMaxDistance colour for the part Chaos simulates. Marvelous gives the drape as
one mesh a piece, its UVs each piece centred and scaled by its fabric's texture size; so here:
1. the pieces joined, their seams welded (boundary to boundary only: the lapels, flaps and welt lie a few
   millimetres over the fronts and must not fuse to them);
2. "pattern" from Marvelous's UVs (one island a piece); "UVMap" the same, scaled per piece to millimetres by the
   piece's outline in SPEC (so the twill runs at one size and along the grain on every piece), over --tile metres;
3. reduced to --tris triangles, then given --thick metres of thickness with closed edges (a single sheet showed no
   edge to the lapel: in the grey looks the lapels vanished into the fronts);
4. buttons: two on the left front at the buttons' places (as they show through the buttonholes, the jacket done
   up), three on each cuff beside the hindarm seam, each a 20 or 15 mm horn disc;
5. SimMaxDistance 0 above the hip joints less --skirt-from, rising to 1 at the hem (the skirt as cloth, the rest
   skinned: the builder's 1 October finding that 4 cm still followed the thighs, now 12 cm in garment.json);
6. NAME_sim: the outer shell alone (fronts, side bodies, backs, sleeves), single layer, --sim-tris triangles.
"""
import json
import math
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.kdtree import KDTree

argv = sys.argv[sys.argv.index("--") + 1:]
DRAPE, SPEC, BODY, OUT, NAME = argv[:5]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


TRIS, THICK, TILE = opt("--tris", 30000, int), opt("--thick", 0.003), opt("--tile", 0.25)
SIM_TRIS, SKIRT_FROM = opt("--sim-tris", 4000, int), opt("--skirt-from", 0.04)
spec = json.load(open(SPEC, encoding="utf-8"))
pieces = {p["key"]: p for p in spec["pieces"]}
SHELL = {"frontL", "frontR", "sideL", "sideR", "backL", "backR", "topsleeveL", "topsleeveR", "undersleeveL", "undersleeveR"}

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
J = lambda n: arm.matrix_world @ arm.pose.bones[n].head  # noqa: E731
hip_z = (J("thigh_l").z + J("thigh_r").z) / 2
for o in [o for o in bpy.data.objects]:
    bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.wm.obj_import(filepath=DRAPE, up_axis="Y", forward_axis="NEGATIVE_Z", use_split_objects=True,
                      use_split_groups=True, global_scale=0.001)
objs = {o.name.split(".")[0]: o for o in bpy.data.objects if o.type == "MESH"}
LIFT = opt("--lift", 0.0)                                  # mm the body was raised for the drape (grow_drape.py)
for o in objs.values():
    o.location.z -= LIFT / 1000.0
bpy.context.view_layer.update()
for k, o in list(objs.items()):
    if k not in pieces:
        bpy.data.objects.remove(o, do_unlink=True)
        del objs[k]
missing = set(pieces) - set(objs)
if missing:
    raise SystemExit("FINISH pieces missing from the drape: %s" % sorted(missing))

# ---- 2. the pattern islands and the cloth-scale UV, per piece -------------------------------------------------------
scale_mm = {}
for k, o in objs.items():
    me = o.data
    pat = me.uv_layers.active
    pat.name = "pattern"
    us = np.array([d.uv[0] for d in pat.data])
    vs = np.array([d.uv[1] for d in pat.data])
    pts = np.array(pieces[k]["points"])
    # Marvelous's UVs are the pattern over its fabric's texture size, which need not be square (the canvas's ran
    # 41 mm a unit across and 21 mm down): a scale for each direction
    su = np.ptp(pts[:, 0]) / max(np.ptp(us), 1e-9)
    sv = np.ptp(pts[:, 1]) / max(np.ptp(vs), 1e-9)
    scale_mm[k] = (round(su, 2), round(sv, 2))
    uvm = me.uv_layers.new(name="UVMap")
    cx, cy = (pts[:, 0].min() + pts[:, 0].max()) / 2, (pts[:, 1].min() + pts[:, 1].max()) / 2
    for d, p in zip(uvm.data, pat.data):
        d.uv = ((p.uv[0] * su + cx) / (TILE * 1000), (p.uv[1] * sv + cy) / (TILE * 1000))
    # the piece's own frame: pattern UV to millimetres (for the buttons below)
    o["mm_su"], o["mm_sv"], o["mm_cx"], o["mm_cy"] = su, sv, cx, cy
    pan = me.attributes.new("panel", "INT", "FACE")
    for i in range(len(me.polygons)):
        pan.data[i].value = sorted(pieces).index(k)
print("FINISH uv scale (mm per unit across, down):", scale_mm, flush=True)


# ---- 4. buttons, placed from the pattern before the pieces are joined -------------------------------------------
def on_piece(k, p_mm):
    """The point of piece k at pattern millimetres p_mm, and the surface's normal there, in the drape."""
    o = objs[k]
    me = o.data
    pat = me.uv_layers["pattern"].data
    su, sv, cx, cy = o["mm_su"], o["mm_sv"], o["mm_cx"], o["mm_cy"]
    target = Vector(((p_mm[0] - cx) / su, (p_mm[1] - cy) / sv))
    for poly in me.polygons:
        li = list(poly.loop_indices)
        for t in range(1, len(li) - 1):
            a, b, c = (Vector(pat[li[0]].uv), Vector(pat[li[t]].uv), Vector(pat[li[t + 1]].uv))
            v0, v1, v2 = b - a, c - a, target - a
            den = v0.x * v1.y - v1.x * v0.y
            if abs(den) < 1e-12:
                continue
            u = (v2.x * v1.y - v1.x * v2.y) / den
            w = (v0.x * v2.y - v2.x * v0.y) / den
            if u >= -1e-6 and w >= -1e-6 and u + w <= 1 + 1e-6:
                P = [o.matrix_world @ me.vertices[me.loops[x].vertex_index].co for x in (li[0], li[t], li[t + 1])]
                pos = P[0] + (P[1] - P[0]) * u + (P[2] - P[0]) * w
                nrm = (P[1] - P[0]).cross(P[2] - P[0]).normalized()
                return pos, nrm
    raise SystemExit("FINISH no point of %s at %s" % (k, p_mm))


def outward(pos, nrm):
    """The normal turned to face away from the body's axis (the pieces' normals are not all one way)."""
    axis = Vector((0, 0, pos.z)) if abs(pos.x) < 0.25 else Vector((math.copysign(0.25, pos.x), 0, pos.z))
    return nrm if nrm.dot(pos - axis) > 0 else -nrm


buttons = bmesh.new()
uvb = buttons.loops.layers.uv.new("UVMap")


def button(pos, nrm, d):
    nrm = outward(pos, nrm)
    rot = nrm.to_track_quat("Z", "Y").to_matrix().to_4x4()
    m = Matrix.Translation(pos + nrm * (THICK / 2 + 0.0012)) @ rot
    res = bmesh.ops.create_cone(buttons, cap_ends=True, segments=16, radius1=d / 2, radius2=d / 2 * 0.92,
                                depth=0.003, matrix=m)
    return res


placed = []
for bx, by in spec["pockets"]["buttons"]:
    pos, n = on_piece("frontL", (bx, by))
    button(pos, n, 0.020)
    placed.append(("front", [round(c, 3) for c in pos]))
for s in "LR":
    pts = pieces["topsleeve" + s]["points"]
    h, nxt, last = Vector(pts[0]), Vector(pts[1]), Vector(pts[-1])
    up = (nxt - h).normalized()                            # up the hindarm seam from the cuff
    inward = (last - h).normalized()                       # along the cuff into the top sleeve
    inward = (inward - up * inward.dot(up)).normalized()
    for k in range(3):
        p = h + up * (32 + 19 * k) + inward * 16
        pos, n = on_piece("topsleeve" + s, (p.x, p.y))
        button(pos, n, 0.015)
        placed.append(("cuff" + s, [round(c, 3) for c in pos]))
print("FINISH buttons", placed, flush=True)

# ---- 1. joined, the seams welded boundary to boundary --------------------------------------------------------------
bpy.ops.object.select_all(action="DESELECT")
for o in objs.values():
    o.select_set(True)
bpy.context.view_layer.objects.active = objs["frontL"]
bpy.ops.object.join()
g = bpy.context.view_layer.objects.active
g.name = NAME
bm = bmesh.new()
bm.from_mesh(g.data)
pan = bm.faces.layers.int.get("panel")
edge_vs = [v for v in bm.verts if v.is_boundary]
kd = KDTree(len(edge_vs))
for i, v in enumerate(edge_vs):
    kd.insert(v.co, i)
kd.balance()
target = {}
for i, v in enumerate(edge_vs):
    if v in target:
        continue
    for co, j, d in kd.find_range(v.co, 0.0025):
        w = edge_vs[j]
        if w is not v and w not in target:
            # only across pieces: a piece's own boundary is never folded onto itself
            fa = {f[pan] for f in v.link_faces}
            fb = {f[pan] for f in w.link_faces}
            if not (fa & fb):
                target[w] = v
bmesh.ops.weld_verts(bm, targetmap=target)
welded = len(target)
bm.to_mesh(g.data)
bm.free()
print("FINISH welded", welded, "seam points", flush=True)

# ---- 6. the sim mesh: the shell, before the thickness ---------------------------------------------------------------
sim = g.copy()
sim.data = g.data.copy()
sim.name = NAME + "_sim"
bpy.context.scene.collection.objects.link(sim)
bm = bmesh.new()
bm.from_mesh(sim.data)
pan = bm.faces.layers.int.get("panel")
keep = {sorted(pieces).index(k) for k in SHELL}
bmesh.ops.delete(bm, geom=[f for f in bm.faces if f[pan] not in keep], context="FACES")
bm.to_mesh(sim.data)
bm.free()


def decimate(o, tris):
    now = sum(len(p.vertices) - 2 for p in o.data.polygons)
    if now <= tris:
        return now
    m = o.modifiers.new("dec", "DECIMATE")
    m.ratio = tris / now
    m.use_collapse_triangulate = True
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier=m.name)
    return sum(len(p.vertices) - 2 for p in o.data.polygons)


# ---- 3. game weight, then the thickness; the buttons joined after ----------------------------------------------------
before = sum(len(p.vertices) - 2 for p in g.data.polygons)
after = decimate(g, TRIS)
sim_tris = decimate(sim, SIM_TRIS)
m = g.modifiers.new("thick", "SOLIDIFY")
m.thickness = THICK
m.offset = 0.0
m.use_rim = True
m.use_even_offset = True
bpy.context.view_layer.objects.active = g
bpy.ops.object.modifier_apply(modifier=m.name)
bme = bpy.data.meshes.new("buttons")
buttons.to_mesh(bme)
bo = bpy.data.objects.new("buttons", bme)
bpy.context.scene.collection.objects.link(bo)
for name, col in (("M_" + NAME, (0.13, 0.13, 0.14, 1)), ("M_Button", (0.06, 0.05, 0.05, 1))):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = col
g.data.materials.clear()
g.data.materials.append(bpy.data.materials["M_" + NAME])
sim.data.materials.clear()
sim.data.materials.append(bpy.data.materials["M_" + NAME])
bme.materials.append(bpy.data.materials["M_" + NAME])
bme.materials.append(bpy.data.materials["M_Button"])
for p in bme.polygons:
    p.material_index = 1
bpy.ops.object.select_all(action="DESELECT")
bo.select_set(True)
g.select_set(True)
bpy.context.view_layer.objects.active = g
bpy.ops.object.join()
for p in g.data.polygons:
    p.use_smooth = True


# ---- 5. SimMaxDistance: the skirt below the hips -------------------------------------------------------------------
def paint(o):
    me = o.data
    zs = [(o.matrix_world @ v.co).z for v in me.vertices]
    hem = min(zs)
    top = hip_z - SKIRT_FROM
    col = me.color_attributes.new("SimMaxDistance", "FLOAT_COLOR", "POINT")
    for v, z in zip(me.vertices, zs):
        t = 0.0 if z >= top else min(1.0, (top - z) / max(top - hem, 1e-6))
        col.data[v.index].color = (t, t, t, 1.0)
    return round(top, 3), round(hem, 3)


skirt = paint(g)
paint(sim)
tri = sum(len(p.vertices) - 2 for p in g.data.polygons)
print("FINISH", json.dumps({"drapeTris": before, "decimatedTris": after, "renderTris": tri, "simTris": sim_tris,
                            "points": len(g.data.vertices), "thicknessM": THICK, "skirtFromTo": skirt,
                            "hipJointZ": round(hip_z, 3)}), flush=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
