"""A Marvelous Designer drape made ready for the garment bake chain: one welded mesh with a true-size "pattern" layer,
on the MetaHuman body and armature it was draped on.

    blender -b --factory-startup -P tools/meshgen/blender/import_md_drape.py -- DRAPE.obj PLAN.json OUT.blend
        [--body F:/LedgerTools/bodies/MH_TomL1/MH_TomL1_FullBody.fbx] [--gap 0.05]
        [--object Jacket] [--materials denim:Denim,knit:Knit]   (30 October: any garment; the jacket's defaults kept)

WHY, 27 October 2026 (Tom's zip jacket, the bake chain's step 1: production/art/clothing/tom-outfit/
BAKE-PLAN-2026-10-27.md). tools/meshgen/blender/retopo_garment.py takes one .blend with the garment as a mesh welded
at its seams, a "pattern" UV layer holding each piece flat at true size in metres, and the body and its armature.
Marvelous's OBJ is not that (measured on drape 4): millimetres, Y up, one object per piece, and each piece's UVs
centred on (0, 0) in its fabric's tile units, so every island overlaps. The plan the job was made from
(tools/md-bridge/zip_jacket.py) holds each piece's outline in pattern millimetres, so each piece's UVs are put back
on it: p = uv x tile + the outline's box centre, the tile fitted per piece from the two boxes and checked against
the other pieces of the same fabric; every boundary vertex then lies on the plan's outline (checked, --tol mm).

WHAT IT WRITES: OUT.blend with "Jacket" (the 13 pieces joined; face attribute "piece", the plan's order; materials
Shell, Rib and Tape by the plan's fabric; "pattern" in metres, each piece shifted along x by its layout offset so no
two islands overlap), "Body" (the MetaHuman full body, its LOD0, from the FBX) and the FBX's armature; and import.json
beside it: the tiles, the offsets, and the checks (boundary error, non-manifold edges, openings, parts, body fit).
"""
import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
DRAPE, PLAN, OUT = argv[0], argv[1], argv[2]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
BODY = opt("--body", "F:/LedgerTools/bodies/MH_TomL1/MH_TomL1_FullBody.fbx", str)
GAP = opt("--gap", 0.05)            # metres between islands in the pattern layout
TOL = opt("--tol", 0.05)            # millimetres: a boundary vertex's furthest allowed distance from the plan outline
WELD = opt("--weld", 0.00001)       # metres (0.01 mm): seam partners sit at the same point
# ANY GARMENT'S FABRICS (30 October 2026, Tom's jeans and jumper: denim, knit, rib): the jacket's three keep their names;
# any other fabric's material is its name capitalised ("denim" Denim), or as --materials denim:Denim,knit:Knit says.
# --object names the welded drape (the jacket's "Jacket", which the later steps look for by default).
MATS = {"shell": "Shell", "rib": "Rib", "tape": "Tape"}
if "--materials" in argv:
    MATS.update(dict(kv.split(":") for kv in argv[argv.index("--materials") + 1].split(",")))
OBJ_NAME = opt("--object", "Jacket", str)

plan = json.load(open(PLAN, encoding="utf-8"))
for _p in plan["pieces"]:
    MATS.setdefault(_p["fabric"], _p["fabric"].capitalize())
pieces = {p["key"]: p for p in plan["pieces"]}
log = {"drape": DRAPE, "plan": PLAN, "pieces": {}, "checks": {}}

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=DRAPE, global_scale=0.001, forward_axis="NEGATIVE_Z", up_axis="Y", use_split_groups=True)
objs = {o.name: o for o in bpy.data.objects if o.type == "MESH"}
lod0 = next((o for n, o in objs.items() if n.endswith("_LOD0")), None)
for n, o in list(objs.items()):
    if "_LOD" in n and not n.endswith("_LOD0"):
        bpy.data.objects.remove(o, do_unlink=True)
missing = [k for k in pieces if k not in objs]
assert not missing, "pieces missing from the drape: %s" % missing
# THE IMPORT'S SCALE AND TURN APPLIED TO THE MESHES (the first run: the importer leaves 0.001 on each object, so the
# meshes stayed in millimetres and a 0.01 mm weld in metres welded nothing; 88 openings instead of 4)
for o in bpy.data.objects:
    o.select_set(o.type == "MESH")
bpy.context.view_layer.objects.active = next(o for o in bpy.data.objects if o.type == "MESH")
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


def outline(p):
    return [(x, y) for x, y, _t in p["points"]]


def seg_dist(q, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, ((q[0] - ax) * dx + (q[1] - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(q[0] - ax - t * dx, q[1] - ay - t * dy)


def poly_dist(q, pts):
    return min(seg_dist(q, pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))


# EACH PIECE'S UVs BACK ON ITS PLAN OUTLINE, in millimetres; then laid out along x in metres
x_at = 0.0
tiles = {}
for idx, (key, p) in enumerate(pieces.items()):
    o = objs[key]
    me = o.data
    uv = me.uv_layers.active
    assert uv is not None, "no UVs on %s" % key
    us = [d.uv[0] for d in uv.data]
    vs = [d.uv[1] for d in uv.data]
    pts = outline(p)
    px = [a for a, _ in pts]
    py = [b for _, b in pts]
    tile = ((max(px) - min(px)) / (max(us) - min(us)), (max(py) - min(py)) / (max(vs) - min(vs)))
    centre = ((max(px) + min(px)) / 2, (max(py) + min(py)) / 2)
    ucentre = ((max(us) + min(us)) / 2, (max(vs) + min(vs)) / 2)
    tiles.setdefault(p["fabric"], []).append(tile)
    # the boundary vertices (edges with one face) checked against the outline, in millimetres
    bm = bmesh.new()
    bm.from_mesh(me)
    uvl = bm.loops.layers.uv.active
    worst = 0.0
    for e in bm.edges:
        if len(e.link_faces) != 1:
            continue
        for lp in e.link_loops:
            u, v = lp[uvl].uv
            q = ((u - ucentre[0]) * tile[0] + centre[0], (v - ucentre[1]) * tile[1] + centre[1])
            worst = max(worst, poly_dist(q, pts))
    bm.free()
    off = x_at - min(px) / 1000.0
    for d in uv.data:
        u, v = d.uv
        d.uv = (((u - ucentre[0]) * tile[0] + centre[0]) / 1000.0 + off, ((v - ucentre[1]) * tile[1] + centre[1]) / 1000.0)
    uv.name = "pattern"
    x_at += (max(px) - min(px)) / 1000.0 + GAP
    # the piece's index on every face, and its fabric's material
    attr = me.attributes.new("piece", "INT", "FACE")
    for f in attr.data:
        f.value = idx
    me.materials.clear()
    mname = MATS[p["fabric"]]
    me.materials.append(bpy.data.materials.get(mname) or bpy.data.materials.new(mname))
    log["pieces"][key] = {"index": idx, "fabric": p["fabric"], "tileMm": [round(tile[0], 3), round(tile[1], 3)],
                          "uvCentre": [round(ucentre[0], 5), round(ucentre[1], 5)], "layoutOffsetM": round(off, 5),
                          "boundaryWorstMm": round(worst, 4)}

# the tiles of each fabric agree (one fabric, one tile)
for fab, ts in tiles.items():
    spread = max(max(abs(t[0] - ts[0][0]) / ts[0][0], abs(t[1] - ts[0][1]) / ts[0][1]) for t in ts)
    log["checks"]["tileSpread_" + fab] = round(spread, 5)

# JOINED AND WELDED: the 13 pieces one mesh, seam partners merged
for o in bpy.data.objects:
    o.select_set(False)
garment = [objs[k] for k in pieces]
for o in garment:
    o.select_set(True)
bpy.context.view_layer.objects.active = garment[0]
bpy.ops.object.join()
jacket = bpy.context.view_layer.objects.active
jacket.name = jacket.data.name = OBJ_NAME
log["object"] = OBJ_NAME
log["materials"] = {f: MATS[f] for f in dict.fromkeys(p["fabric"] for p in plan["pieces"])}
bm = bmesh.new()
bm.from_mesh(jacket.data)
before = len(bm.verts)
bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=WELD)
log["checks"]["welded"] = before - len(bm.verts)
log["checks"]["nonManifoldEdges"] = sum(1 for e in bm.edges if len(e.link_faces) > 2)
# the openings: loops of boundary edges
bnd = {e for e in bm.edges if len(e.link_faces) == 1}
seen, loops = set(), 0
for e in bnd:
    if e in seen:
        continue
    loops += 1
    stack = [e]
    while stack:
        a = stack.pop()
        if a in seen:
            continue
        seen.add(a)
        for v in a.verts:
            stack += [x for x in v.link_edges if x in bnd and x not in seen]
log["checks"]["openings"] = loops
# connected parts
vseen, parts = set(), 0
for v in bm.verts:
    if v in vseen:
        continue
    parts += 1
    stack = [v]
    while stack:
        a = stack.pop()
        if a in vseen:
            continue
        vseen.add(a)
        stack += [e.other_vert(a) for e in a.link_edges]
log["checks"]["parts"] = parts
bm.to_mesh(jacket.data)
bm.free()
log["checks"]["boundaryWorstMm"] = max(p["boundaryWorstMm"] for p in log["pieces"].values())

# THE BODY AND ITS ARMATURE from the MetaHuman FBX, checked against the drape's own body (LOD0), which then goes
before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=BODY)
new = [o for o in bpy.data.objects if o not in before]
arm = next((o for o in new if o.type == "ARMATURE"), None)
meshes = [o for o in new if o.type == "MESH"]
body = max(meshes, key=lambda o: len(o.data.vertices)) if meshes else None
assert arm is not None and body is not None, "no armature or body mesh in %s" % BODY


def bounds(o):
    bpy.context.view_layer.update()
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [min(c[i] for c in cs) for i in range(3)], [max(c[i] for c in cs) for i in range(3)]


if lod0 is not None:
    (a0, a1), (b0, b1) = bounds(lod0), bounds(body)
    log["checks"]["bodyFitMm"] = round(1000 * max(max(abs(a0[i] - b0[i]), abs(a1[i] - b1[i])) for i in range(3)), 2)
    bpy.data.objects.remove(lod0, do_unlink=True)
for o in meshes:
    if o is not body:
        bpy.data.objects.remove(o, do_unlink=True)
body.name = "Body"
log["armature"] = arm.name
log["bones"] = len(arm.data.bones)
log["body"] = {"verts": len(body.data.vertices)}

ok = (log["checks"]["boundaryWorstMm"] <= TOL and log["checks"]["nonManifoldEdges"] == 0 and log["checks"]["parts"] == 1
      and all(v < 0.005 for k, v in log["checks"].items() if k.startswith("tileSpread_"))
      and log["checks"].get("bodyFitMm", 99) <= 2.0)
log["ok"] = ok
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT))
json.dump(log, open(os.path.join(os.path.dirname(os.path.abspath(OUT)), "import.json"), "w", encoding="utf-8"), indent=1)
print("IMPORT", json.dumps({"ok": ok, **log["checks"], "bones": log["bones"]}))
