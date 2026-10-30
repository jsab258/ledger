"""A scanned solid brought to a game mesh and its levels of detail by careful decimation, its texture layout packed
for a bake, and checked (30 October 2026, Tom's shoes from the scanned oxford).

    blender -b --factory-startup -P tools/meshgen/blender/scan_lods.py -- SRC.blend OBJECT OUT_DIR
        [--tris 3000] [--lods 0.5,0.25,0.1] [--tex 1024] [--margin-px 8] [--name shoe]

WHY: a photo scan arrives as one closed, dense, triangulated solid with its own texture layout (here 19,982
triangles for one shoe; the game's budget about 3,000). Retopology by hand keeps edge flow for deforming cloth; a
rigid, barely bending piece (a shoe, a prop) keeps its shape as well by quadric edge collapse, which Blender's
Decimate (Collapse) does while keeping the layout's seams as borders, so the scan's islands survive and can be
re-packed. The bake (scan_bake.py) then carries the scan's maps onto the new layout.

OUT_DIR gets NAME_game.blend (OBJECT_LOD0 to _LOD3, each with the scan's layout "UVMap" and the packed "game"
layout, which is first) and lods.json:
  - triangles per level, against --tris and --lods;
  - non-manifold edges and boundary edges per level (a closed scan stays closed: both 0);
  - the shape: each level's distance from the scan (scan points to the level's surface: median, 99th percentile,
    worst) and the silhouette's deviation in six orthographic views (silhouettes.npz, read by
    silhouette_check.py, which needs SciPy, so runs in the system Python);
  - the "game" layout: islands, the square used, overlap (texels covered twice at --tex) and the smallest gap
    between two islands in texels (padding, against --margin-px).
"""
import json
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, OBJ, OUT = argv[:3]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
TRIS = opt("--tris", 3000, int)
LODS = [float(x) for x in opt("--lods", "0.5,0.25,0.1", str).split(",")]
TEX = opt("--tex", 1024, int)
MARGIN = opt("--margin-px", 8, int)
NAME = opt("--name", "shoe", str)
os.makedirs(OUT, exist_ok=True)
log = {"src": SRC, "object": OBJ, "targetTris": TRIS, "lods": LODS, "tex": TEX, "marginPx": MARGIN, "levels": {}}


def say(*a):
    print("LODS", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=SRC)
src = bpy.data.objects[OBJ]
for o in list(bpy.data.objects):
    if o is not src:
        bpy.data.objects.remove(o, do_unlink=True)
src.data.transform(src.matrix_world)
src.matrix_world.identity()
SP = np.array([tuple(v.co) for v in src.data.vertices])
src_tris = sum(len(p.vertices) - 2 for p in src.data.polygons)
log["srcTris"] = src_tris


def tri_count(o):
    return sum(len(p.vertices) - 2 for p in o.data.polygons)


def decimated(base, target, name):
    """A copy of base decimated (collapse, triangulated) to about target triangles: the ratio found by bisection."""
    lo, hi = 0.0, 1.0
    best = None
    for _ in range(14):
        r = (lo + hi) / 2
        o = base.copy()
        o.data = base.data.copy()
        bpy.context.scene.collection.objects.link(o)
        m = o.modifiers.new("dec", "DECIMATE")
        m.decimate_type = "COLLAPSE"
        m.ratio = r
        m.use_collapse_triangulate = True
        dg = bpy.context.evaluated_depsgraph_get()
        me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
        bpy.data.objects.remove(o, do_unlink=True)
        n = sum(len(p.vertices) - 2 for p in me.polygons)
        if best is None or abs(n - target) < abs(best[1] - target):
            if best is not None:
                bpy.data.meshes.remove(best[0])
            best = (me, n, r)
        else:
            bpy.data.meshes.remove(me)
        if abs(n - target) <= max(4, target * 0.005):
            break
        if n > target:
            hi = r
        else:
            lo = r
    me, n, r = best
    me.name = name
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    return o, r


def topology(o):
    bm = bmesh.new()
    bm.from_mesh(o.data)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    bd = sum(1 for e in bm.edges if e.is_boundary)
    bm.free()
    return nm, bd


def shape(o):
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bvh = BVHTree.FromBMesh(bm)
    d = np.array([bvh.find_nearest(tuple(p))[3] for p in SP])
    bm.free()
    # and the other way: the level's points to the scan
    bm2 = bmesh.new()
    bm2.from_mesh(src.data)
    bvh2 = BVHTree.FromBMesh(bm2)
    d2 = np.array([bvh2.find_nearest(v.co)[3] for v in o.data.vertices])
    bm2.free()
    return {"scanToLevelMm": {"median": round(float(np.median(d)) * 1000, 3), "p99": round(float(np.percentile(d, 99)) * 1000, 3),
                              "max": round(float(d.max()) * 1000, 3)},
            "levelToScanMm": {"median": round(float(np.median(d2)) * 1000, 3), "max": round(float(d2.max()) * 1000, 3)}}


VIEWS = {"front": (1, 2), "side": (0, 2), "top": (0, 1)}   # axes kept: world x/y/z; a silhouette is the same from
# the opposite side, so three projections give the six views


def projected(o):
    co = np.array([tuple(v.co) for v in o.data.vertices])
    tris = np.array([tuple(t.vertices) for t in o.data.loop_triangles])
    return co, tris


# ---- LOD0 and the reduced levels -----------------------------------------------------------------------------------
levels = []
lod0, r0 = decimated(src, TRIS, "%s_LOD0" % OBJ)
levels.append((lod0, r0))
for k, f in enumerate(LODS, 1):
    o, r = decimated(lod0, int(round(TRIS * f)), "%s_LOD%d" % (OBJ, k))
    levels.append((o, r))
sil = {}
for o, r in levels:
    o.data.calc_loop_triangles()
    nm, bd = topology(o)
    lv = {"tris": tri_count(o), "ratio": round(r, 5), "nonManifoldEdges": nm, "boundaryEdges": bd}
    lv.update(shape(o))
    log["levels"][o.name] = lv
    say(o.name, json.dumps(lv))
    co, tris = projected(o)
    sil[o.name + "_co"] = co
    sil[o.name + "_tris"] = tris
src.data.calc_loop_triangles()
co, tris = projected(src)
sil["scan_co"] = co
sil["scan_tris"] = tris
np.savez(os.path.join(OUT, "silhouettes.npz"), **sil)

# ---- the "game" layout: the scan's islands kept, packed again with the margin, shared by every level --------------
# (the reduced levels come from LOD0, so their layout is LOD0's islands; packing is done on LOD0 and copied by
# nearest point to the levels below: each level's loops take the packed position of the same island's nearest LOD0
# loop, found through the scan layout's own coordinates)


def pack(o):
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    uv = o.data.uv_layers
    src_uv = uv["UVMap"] if "UVMap" in uv else uv[0]
    game = uv.new(name="game")
    for i, l in enumerate(src_uv.data):
        game.data[i].uv = l.uv
    uv.active = game
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.select_all(action="SELECT")
    bpy.ops.uv.pack_islands(udim_source="CLOSEST_UDIM", rotate=True, margin_method="FRACTION", margin=MARGIN / TEX * 1.25,
                            shape_method="CONCAVE")
    bpy.ops.object.mode_set(mode="OBJECT")


def islands_of(o, layer):
    """Islands of a layout: faces joined where they share an edge with the same coordinates on both sides."""
    bm = bmesh.new()
    bm.from_mesh(o.data)
    uvl = bm.loops.layers.uv[layer]
    bm.faces.ensure_lookup_table()
    lab = [-1] * len(bm.faces)
    n = 0
    for f0 in bm.faces:
        if lab[f0.index] >= 0:
            continue
        lab[f0.index] = n
        st = [f0]
        while st:
            f = st.pop()
            for l in f.loops:
                e = l.edge
                for l2 in e.link_loops:
                    g = l2.face
                    if g is f or lab[g.index] >= 0:
                        continue
                    # same coordinates at both ends of the shared edge
                    a1, b1 = l[uvl].uv, l.link_loop_next[uvl].uv
                    if l2.vert is l.vert:
                        a2, b2 = l2[uvl].uv, l2.link_loop_next[uvl].uv
                    else:
                        a2, b2 = l2.link_loop_next[uvl].uv, l2[uvl].uv
                    if (a1 - a2).length < 1e-5 and (b1 - b2).length < 1e-5:
                        lab[g.index] = n
                        st.append(g)
        n += 1
    tris = []
    for f in bm.faces:
        uvs = [tuple(l[uvl].uv) for l in f.loops]
        for k in range(1, len(uvs) - 1):
            tris.append((lab[f.index], uvs[0], uvs[k], uvs[k + 1]))
    bm.free()
    return n, tris


def raster_layout(tris, size):
    """Each texel's island (or -1) and the count of islands covering it, by the triangles' coverage of texel centres."""
    own = np.full((size, size), -1, int)
    count = np.zeros((size, size), np.int16)
    for isl, a, b, c in tris:
        P = np.array([a, b, c]) * size - 0.5
        x0, y0 = np.floor(P.min(0)).astype(int)
        x1, y1 = np.ceil(P.max(0)).astype(int)
        x0, y0 = max(x0, 0), max(y0, 0)
        x1, y1 = min(x1, size - 1), min(y1, size - 1)
        if x1 < x0 or y1 < y0:
            continue
        X, Y = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
        p = np.stack([X.ravel(), Y.ravel()], 1).astype(float)
        v0, v1 = P[1] - P[0], P[2] - P[0]
        den = v0[0] * v1[1] - v1[0] * v0[1]
        if abs(den) < 1e-12:
            continue
        w = p - P[0]
        u = (w[:, 0] * v1[1] - v1[0] * w[:, 1]) / den
        v = (v0[0] * w[:, 1] - w[:, 0] * v0[1]) / den
        m = (u >= -1e-6) & (v >= -1e-6) & (u + v <= 1 + 1e-6)
        xs, ys = X.ravel()[m], Y.ravel()[m]
        prev = own[ys, xs]
        newc = (prev != isl)
        count[ys[newc], xs[newc]] += 1
        own[ys, xs] = np.where(prev == -1, isl, prev)
    return own, count


pack(lod0)
n_isl, tris = islands_of(lod0, "game")
own, count = raster_layout(tris, TEX)
overlap = int((count > 1).sum())
np.save(os.path.join(OUT, "layout_owner.npy"), own)
log["layout"] = {"islands": n_isl, "usedShare": round(float((own >= 0).mean()), 4), "overlapTexels": overlap}
say("layout", log["layout"])


def per_island_affine(o_from, o_to):
    """Copy the packed layout to a reduced level: for each of its loops, the island's affine map from the scan layout
    to the game layout (fitted on LOD0's loops of that island) applied to its scan-layout coordinate."""
    n0, tris0 = islands_of(o_from, "UVMap")
    bm = bmesh.new()
    bm.from_mesh(o_from.data)
    us, gs = bm.loops.layers.uv["UVMap"], bm.loops.layers.uv["game"]
    lab = {}
    k = 0
    # islands again, by face, to group loops
    n_, t_ = n0, tris0
    face_isl = []
    for f in bm.faces:
        face_isl.append(None)
    # rebuild face labels from the triangles' order (islands_of walks faces in order, fan triangles per face)
    idx = 0
    for f in bm.faces:
        face_isl[f.index] = tris0[idx][0]
        idx += len(f.loops) - 2
    maps = {}
    pts = {}
    for f in bm.faces:
        for l in f.loops:
            pts.setdefault(face_isl[f.index], []).append((tuple(l[us].uv), tuple(l[gs].uv)))
    for isl, pr in pts.items():
        A = np.array([[a[0], a[1], 1.0] for a, _ in pr])
        B = np.array([b for _, b in pr])
        M, *_ = np.linalg.lstsq(A, B, rcond=None)
        maps[isl] = (M, np.array([a for a, _ in pr]))
    bm.free()
    # each target loop: the island whose scan-layout points lie nearest
    allp = np.vstack([v[1] for v in maps.values()])
    alli = np.concatenate([[k_] * len(v[1]) for k_, v in maps.items()])
    uv = o_to.data.uv_layers
    game = uv.new(name="game")
    src_uv = uv["UVMap"]
    for f in o_to.data.polygons:
        cen = np.mean([tuple(src_uv.data[li].uv) for li in f.loop_indices], axis=0)
        isl = alli[np.argmin(((allp - cen) ** 2).sum(1))]
        M = maps[isl][0]
        for li in f.loop_indices:
            a = src_uv.data[li].uv
            game.data[li].uv = tuple(np.array([a[0], a[1], 1.0]) @ M)
    uv.active = game


for o, r in levels[1:]:
    per_island_affine(lod0, o)
# the maps' layout first, as the game reads the first (uv_order.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uv_order import maps_layout_first  # noqa: E402
for o, r in levels:
    uv = o.data.uv_layers
    # uv_order moves "UVMap" first; here the maps' layout is "game": rename so the shared convention holds
    uv["UVMap"].name = "scan"
    uv["game"].name = "UVMap"
    log["levels"][o.name]["uvOrder"] = maps_layout_first(o)
    log["levels"][o.name]["uvLayers"] = [u.name for u in o.data.uv_layers]
# padding: the smallest distance in texels between two different islands (computed in the system Python from
# layout_owner.npy by silhouette_check.py --layout, which has SciPy)
bpy.data.objects.remove(src, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_game.blend"))
json.dump(log, open(os.path.join(OUT, "lods.json"), "w"), indent=1)
say("done", json.dumps({k: v["tris"] for k, v in log["levels"].items()}))
