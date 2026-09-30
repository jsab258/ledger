"""An inner garment fitted under an outer one (a jumper under a jacket), so the layers never cross.

    blender -b -P tools/meshgen/blender/fit_under.py -- OUTER.blend INNER.fbx OUT_DIR --outer JacketRender --name ron_jumper_under

WHY, 30 September (Ron's jumper under his donkey jacket: made on its own it stood 26 mm off him and came out
through the closer-fitting jacket almost everywhere; the builder's layer fix, NOW.md: "a shirt collar in the
opening (the throat is bare)"). For each point of the inner garment: from the nearest place on his body, along
its outward normal, the distance to the outer garment's first surface there; where the inner point stands within
--gap of that, it is drawn in to --gap inside it (never nearer him than --min-off); the moves are smoothed over the
inner garment so no step shows. Points where the outer garment is not found above them (his throat inside the
collar, below the jacket's hem) keep their place. The inner garment's layers (its "pattern" UV) are kept.
OUT_DIR gets NAME_render_static.fbx, NAME.blend (both garments and his body), under.json and pictures.
"""
import json
import os
import sys

import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
OUTER_BLEND, INNER, OUT = argv[0], argv[1], argv[2]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "inner", str)
GAP, MINOFF = opt("--gap", 0.006), opt("--min-off", 0.003)
bpy.ops.wm.open_mainfile(filepath=OUTER_BLEND)
outer = bpy.data.objects[opt("--outer", "JacketRender", str)]
for o in bpy.data.objects:
    if o.type == "MESH" and o.name in ("Jacket", "JacketSim"):
        o.hide_render = True
body = next(o for o in bpy.data.objects if o.type == "MESH" and "Body" in o.name)
BBVH = tailor.bvh_of(body)
dg = bpy.context.evaluated_depsgraph_get()
OBVH = BVHTree.FromObject(outer, dg)
before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=INNER)
inner = next(o for o in bpy.data.objects if o not in before and o.type == "MESH")
inner.name = "InnerRender"
bpy.ops.object.select_all(action="DESELECT")
inner.select_set(True)
bpy.context.view_layer.objects.active = inner
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = inner.data
P = np.array([tuple(v.co) for v in me.vertices])
n = len(P)
disp = np.zeros_like(P)
fixed = np.zeros(n, bool)
for i in range(n):
    p = Vector(tuple(P[i]))
    h, nn, _f, _d = BBVH.find_nearest(p)
    if h is None:
        continue
    off = (p - h).dot(nn)
    hit = OBVH.ray_cast(h + nn * 0.001, nn, 0.25)[0]
    if hit is None:
        continue
    dj = (hit - h).length
    fixed[i] = True
    target = max(MINOFF, min(off, dj - GAP))
    if target < off:
        disp[i] = np.array(tuple(nn)) * (target - off)
# SECOND, BY THE OUTER GARMENT'S NEAREST POINT (at the armpits the ray out from his body passed between the
# jacket's side and sleeve, and the jumper came out there): an inner point within 3 cm of the outer garment is
# drawn to --gap inside it, inward being from that outer point towards his body
for i in range(n):
    p = Vector(tuple(P[i])) + Vector(tuple(disp[i]))
    q, _qn, _f, dq = OBVH.find_nearest(p)
    if q is None or dq > 0.03:
        continue
    h, hn, _f2, _d2 = BBVH.find_nearest(q)
    if h is None:
        continue
    u = (h - q)
    if u.length < 1e-6:
        continue
    u.normalize()
    depth = (p - q).dot(u)
    if depth < GAP:
        p2 = p + u * (GAP - depth)
        hb, hbn, _f3, _d3 = BBVH.find_nearest(p2)
        if hb is not None and (p2 - hb).dot(hbn) < MINOFF:
            p2 = hb + hbn * MINOFF
        disp[i] = np.array(tuple(p2)) - P[i]
        fixed[i] = True
# smoothed so no step shows, never undoing a needed move
ed = np.array([e.vertices[:] for e in me.edges])
deg = np.bincount(ed.ravel(), minlength=n).astype(float)
need = disp.copy()
for _ in range(opt("--smooth", 12, int)):
    acc = np.column_stack([np.bincount(ed[:, 0], weights=disp[ed[:, 1], k], minlength=n) + np.bincount(ed[:, 1], weights=disp[ed[:, 0], k], minlength=n)
                           for k in range(3)])
    avg = acc / np.maximum(deg, 1)[:, None]
    # keep the deeper of the two inward moves
    deeper = np.linalg.norm(avg, axis=1) > np.linalg.norm(need, axis=1)
    disp = np.where(deeper[:, None], 0.5 * (disp + avg), need)
P = P + disp
for i, v in enumerate(me.vertices):
    v.co = Vector(tuple(P[i]))
me.update()
# THE UNSEEN PARTS REMOVED (--cull-deep D; games remove what an outer layer always hides: at the armpits the jacket
# lies too close to him for a jumper between, and it showed through): an inner face goes when the outer garment is
# over it and it lies more than D from every opening of the outer garment (the edges of its single-layer mesh:
# neck, front opening, cuffs, hem), so what can show at the openings when he moves is kept
CULL = opt("--cull-deep", 0.0)
culled = 0
if CULL > 0:
    import bmesh
    from mathutils.kdtree import KDTree
    src = bpy.data.objects.get(opt("--outer-edges", "JacketSim", str))
    bs = bmesh.new()
    bs.from_mesh(src.data)
    bs.transform(src.matrix_world)
    edge_pts = []
    for e in bs.edges:
        if e.is_boundary:
            a, b = e.verts[0].co, e.verts[1].co
            for t in np.linspace(0, 1, 6):
                edge_pts.append(a.lerp(b, t))
    bs.free()
    kd = KDTree(len(edge_pts))
    for k, q in enumerate(edge_pts):
        kd.insert(q, k)
    kd.balance()
    bi = bmesh.new()
    bi.from_mesh(me)
    bi.verts.ensure_lookup_table()
    # kept whole round the neck (culled there, its cut edges showed as torn scraps through the jacket's collar)
    KZ = opt("--keep-neck-above", 9.0)
    KR = opt("--keep-neck-r", 0.13)
    deep = np.array([fixed[v.index] and kd.find(v.co)[2] > CULL
                     and not (v.co.z > KZ and abs(v.co.x) < KR) for v in bi.verts])
    gone = [f for f in bi.faces if all(deep[v.index] for v in f.verts)]
    culled = len(gone)
    bmesh.ops.delete(bi, geom=gone, context="FACES")
    bmesh.ops.delete(bi, geom=[v for v in bi.verts if not v.link_faces], context="VERTS")
    bi.to_mesh(me)
    bi.free()
    me.update()
    P = np.array([tuple(v.co) for v in me.vertices])
    n = len(P)
if "--cull-out" in argv:
    # WHAT STILL COMES OUT THROUGH THE OUTER GARMENT REMOVED (under the collar the jumper kept whole came out
    # through the jacket's front as pale scraps): a face goes when any of its points lies outside the outer garment
    # above it
    import bmesh
    bi = bmesh.new()
    bi.from_mesh(me)
    bi.verts.ensure_lookup_table()
    outside = np.zeros(len(bi.verts), bool)
    for v in bi.verts:
        h, nn, _f, _d = BBVH.find_nearest(v.co)
        if h is None:
            continue
        hit = OBVH.ray_cast(h + nn * 0.001, nn, 0.25)[0]
        if hit is not None and (v.co - h).dot(nn) > (hit - h).length - 0.002:
            outside[v.index] = True
        q, _qn, _f2, dq = OBVH.find_nearest(v.co)
        if q is not None and dq < 0.004:
            outside[v.index] = True
    gone = [f for f in bi.faces if any(outside[v.index] for v in f.verts)]
    culled += len(gone)
    bmesh.ops.delete(bi, geom=gone, context="FACES")
    bmesh.ops.delete(bi, geom=[v for v in bi.verts if not v.link_faces], context="VERTS")
    bi.to_mesh(me)
    bi.free()
    me.update()
    P = np.array([tuple(v.co) for v in me.vertices])
    n = len(P)
# checked: inner points still out through the outer garment, and inner points inside him
out_n = inside_n = 0
for i in range(n):
    p = Vector(tuple(P[i]))
    h, nn, _f, _d = BBVH.find_nearest(p)
    if h is not None and (p - h).dot(nn) < 0.0:
        inside_n += 1
    if h is not None:
        hit = OBVH.ray_cast(h + nn * 0.001, nn, 0.25)[0]
        if hit is not None and (p - h).dot(nn) > (hit - h).length - 0.001:
            out_n += 1
log = {"outer": OUTER_BLEND, "inner": INNER, "points": n, "underOuter": int(fixed.sum()),
       "movedIn": int((np.linalg.norm(disp, axis=1) > 0.0005).sum()), "mostMm": round(float(np.linalg.norm(disp, axis=1).max()) * 1000, 1),
       "stillOut": out_n, "insideHim": inside_n, "facesCulled": culled, "pointsLeft": n}
print("UNDER", json.dumps(log), flush=True)
inner.data.materials.clear()
inner.data.materials.append(tailor.material("M_Inner", tuple(float(c) for c in opt("--rgb", "0.30,0.30,0.31", str).split(",")), 0.95))
for p_ in inner.data.polygons:
    p_.material_index = 0
tailor.pictures(os.path.join(OUT, "worn"), Vector((0, 0, 1.25)), views=(("front", (0, -2.6, 0.1)), ("side", (2.6, 0, 0.1)),
                                                                        ("back", (0, 2.6, 0.1)), ("three-quarter", (1.8, -1.9, 0.3))), res=(700, 800))
tailor.pictures(os.path.join(OUT, "worn-close"), Vector((0, -0.05, 1.50)), views=(("front", (0, -0.9, 0.08)), ("three-quarter", (0.62, -0.62, 0.1))),
                res=(700, 600))
bpy.ops.object.select_all(action="DESELECT")
inner.select_set(True)
bpy.context.view_layer.objects.active = inner
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_render_static.fbx"), use_selection=True,
                         object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "under.json"), "w"), indent=1)
