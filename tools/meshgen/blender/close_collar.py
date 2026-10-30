"""A skinned garment's neck closed inside, as Mafia closes its collar: an inner facing from the collar's top edge down to
the neck, its top riding with the collar and its foot with the neck.

    blender -b SKINNED.blend -P tools/meshgen/blender/close_collar.py -- OUT_DIR NAME BODY_OBJECT
            [--lip 0.008] [--depth 0.05] [--gap 0.003] [--max-influences 8]

WHY, 30 October 2026 (his order C9; Tom's jacket passed in the packaged game, its collar listed): as he straightens
from the bench the collar's front pulls off his neck and the inside of the jacket shows black for two frames
(F:/LedgerTools/tmp/ai-tester/film/2026-10-30-0603, f-62 and f-63), the notch seen standing since drape 4 the same
fault. The jacket's only open edges are the collar's top ring, the cuffs and the hem, and its material draws one side,
so through the collar's ring nothing closes the view. Reference first: Mafia's jacket closes every visible edge, its
collar with a wall about 1 cm deep inside and its neck by a hidden cap (production/research/game-clothing-pipeline/
MAFIA-JACKET-2026-10-28.md, sections 3 and "What LEDGER should copy", 1 and 3).

WHAT IT DOES: the collar is the highest open ring of NAME (the cuffs and hem lie lower). From each of its points the
facing turns in over a lip (LIP toward the neck's axis and half as much down, never more than half the way to the skin)
and runs down DEPTH to a foot GAP off the body's skin at its nearest point. Its faces look toward the neck's axis, so
from the front the far side of the facing shows and the near side, culled, does not; its material is the collar's,
its UVs the collar edge's own (stretched: it is dark and inside). The edge ring and lip take the collar point's
weights; the foot takes the body's at its nearest skin, so the facing spans the gap as the collar pulls away, like a
dickey. OUT_DIR gets NAME_skinned.fbx (the same export as skin_garment.py), NAME_skinned.blend and collar.json.
"""
import json
import math
import os
import sys
from collections import defaultdict

import bmesh
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
OUT, NAME, BODY = argv[:3]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


LIP, DEPTH, GAP = opt("--lip", 0.008), opt("--depth", 0.05), opt("--gap", 0.003)
MAXI = opt("--max-influences", 8, int)
os.makedirs(OUT, exist_ok=True)

g = bpy.data.objects[NAME]
body = bpy.data.objects[BODY]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
gw, gwi = g.matrix_world, g.matrix_world.inverted()

# THE BODY'S SKIN: triangles in the world, each corner's weights by bone name
bmb = body.data
bmb.calc_loop_triangles()
bw = body.matrix_world
bverts = [bw @ v.co for v in bmb.vertices]
btris = [tuple(t.vertices) for t in bmb.loop_triangles]
tree = BVHTree.FromPolygons(bverts, btris)
bnames = {gr.index: gr.name for gr in body.vertex_groups}
bweights = [{bnames[e.group]: e.weight for e in v.groups if e.weight > 1e-4} for v in bmb.vertices]


def body_weights_at(p):
    """The body's weights at its skin nearest p (barycentric over that triangle), the strongest MAXI, summing to 1;
    and the nearest point and its normal."""
    hit, nrm, fi, _d = tree.find_nearest(p)
    a, b, c = (bverts[i] for i in btris[fi])
    v0, v1, v2 = b - a, c - a, hit - a
    d00, d01, d11, d20, d21 = v0.dot(v0), v0.dot(v1), v1.dot(v1), v2.dot(v0), v2.dot(v1)
    den = d00 * d11 - d01 * d01
    wb = (d11 * d20 - d01 * d21) / den if abs(den) > 1e-12 else 0.0
    wc = (d00 * d21 - d01 * d20) / den if abs(den) > 1e-12 else 0.0
    mix = {}
    for corner, share in zip(btris[fi], (1.0 - wb - wc, wb, wc)):
        for bone, w in bweights[corner].items():
            mix[bone] = mix.get(bone, 0.0) + max(0.0, share) * w
    top = sorted(mix.items(), key=lambda kv: -kv[1])[:MAXI]
    s = sum(w for _b, w in top) or 1.0
    return {bone: w / s for bone, w in top}, hit, nrm


# THE COLLAR: the highest open ring, walked in order
bm = bmesh.new()
bm.from_mesh(g.data)
bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()
adj = defaultdict(list)
for e in bm.edges:
    if e.is_boundary:
        a, b = e.verts[0].index, e.verts[1].index
        adj[a].append(b)
        adj[b].append(a)
rings, seen = [], set()
for v in list(adj):
    if v in seen:
        continue
    ring, prev, cur = [], None, v
    while cur is not None and cur not in seen:
        seen.add(cur)
        ring.append(cur)
        nxt = [n for n in adj[cur] if n != prev and n not in seen]
        prev, cur = cur, (nxt[0] if nxt else None)
    rings.append(ring)
collar = max(rings, key=lambda r: max((gw @ bm.verts[i].co).z for i in r))
P = [gw @ bm.verts[i].co for i in collar]
C = sum(P, Vector()) / len(P)
length = sum((P[k] - P[(k + 1) % len(P)]).length for k in range(len(P)))

# the collar edge's material and each point's UVs (from a face using that point, every UV layer)
edge_face = {}
for i in collar:
    for f in bm.verts[i].link_faces:
        edge_face.setdefault(i, f)
mat_index = edge_face[collar[0]].material_index
uv_layers = list(bm.loops.layers.uv.values())
uv_of = {}
for i in collar:
    f = edge_face[i]
    loop = next(l for l in f.loops if l.vert.index == i)
    uv_of[i] = [tuple(loop[layer].uv) for layer in uv_layers]

# THE FACING'S RINGS: the lip, then the foot off the skin
weights_of = {}
dg = {gr.index: gr.name for gr in g.vertex_groups}
for i in collar:
    weights_of[i] = {dg[e.group]: e.weight for e in g.data.vertices[i].groups}
# THE NECK (30 October): the body mesh here ends at the neck's base and, with the parts under the jacket cut away, its
# open ring runs round the chest, so the neck is taken from the skeleton: its line from neck_01 to the head bone in the
# pose the garment was bound in, its radius from his measured girth (--neck-girth, his measurements.json's 420 mm).
# The foot's weights split as Mafia's collar's do (neck_twist_01 76%, spine_04 20%: MAFIA-JACKET-2026-10-28.md,
# section 4), on this skeleton neck_01 and spine_05.
NECK_GIRTH = opt("--neck-girth", 0.420)
aw = arm.matrix_world
S = aw @ arm.data.bones["neck_01"].head_local
H = aw @ arm.data.bones["head"].head_local
r_neck = NECK_GIRTH / (2.0 * math.pi)
FOOT_W = {"neck_01": 0.79, "spine_05": 0.21}


def axis_at(z):
    k = (z - S.z) / (H.z - S.z) if abs(H.z - S.z) > 1e-6 else 0.0
    return S + (H - S) * k


def seam_weights(d):
    return dict(FOOT_W)


lip_pts, foot_pts, foot_w, gaps = [], [], [], []
for p in P:
    a = axis_at(p.z)
    out = Vector((p.x - a.x, p.y - a.y, 0.0))
    room = out.length - r_neck
    d = out.normalized()
    lip = max(0.0, min(LIP, 0.5 * room))
    lip_pts.append(p - d * lip + Vector((0.0, 0.0, -0.5 * lip)))
    hf = max(p.z - DEPTH, S.z + 0.005)
    foot_pts.append(axis_at(hf) + d * (r_neck + GAP))
    foot_w.append(seam_weights(d))
    gaps.append(room)

# THE FACES: edge to lip, lip to foot, round the ring, looking toward the neck's axis
new_lip = [bm.verts.new(gwi @ q) for q in lip_pts]
new_foot = [bm.verts.new(gwi @ q) for q in foot_pts]
bm.verts.ensure_lookup_table()
made, flipped = [], 0
n = len(collar)
for k in range(n):
    k2 = (k + 1) % n
    for quad in ((bm.verts[collar[k]], bm.verts[collar[k2]], new_lip[k2], new_lip[k]),
                 (new_lip[k], new_lip[k2], new_foot[k2], new_foot[k])):
        f = bm.faces.new(quad)
        f.material_index = mat_index
        f.normal_update()
        centre = gw @ f.calc_center_median()
        toward = Vector((C.x - centre.x, C.y - centre.y, 0.0))
        if (gw.to_3x3() @ f.normal).dot(toward) < 0:
            f.normal_flip()
            flipped += 1
        made.append((f, k, k2))
# UVs: each corner the collar point's own, the lip and foot rings stepping down a little in v
step = {0: 0.0, 1: 0.004, 2: 0.012}
ring_of = {}
for k in range(n):
    ring_of[bm.verts[collar[k]]] = (0, k)     # keyed by the vertex itself: new ones have no index yet
    ring_of[new_lip[k]] = (1, k)
    ring_of[new_foot[k]] = (2, k)
for f, _k, _k2 in made:
    for loop in f.loops:
        r, k = ring_of[loop.vert]
        for li, layer in enumerate(uv_layers):
            u, v = uv_of[collar[k]][li]
            loop[layer].uv = (u, v - step[r])
bm.verts.index_update()
ids_lip = [v.index for v in new_lip]
ids_foot = [v.index for v in new_foot]
bm.to_mesh(g.data)
bm.free()
g.data.update()

# WEIGHTS: the lip with its collar point, the foot with the body at its skin
for k in range(n):
    for bone, w in weights_of[collar[k]].items():
        (g.vertex_groups.get(bone) or g.vertex_groups.new(name=bone)).add([ids_lip[k]], w, "REPLACE")
    for bone, w in foot_w[k].items():
        (g.vertex_groups.get(bone) or g.vertex_groups.new(name=bone)).add([ids_foot[k]], w, "REPLACE")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uv_order import maps_layout_first  # noqa: E402

reordered = maps_layout_first(g)
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
g.select_set(True)
bpy.context.view_layer.objects.active = arm
body.select_set(False)
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_skinned.fbx"), use_selection=True,
                         object_types={"ARMATURE", "MESH"}, add_leaf_bones=False, mesh_smooth_type="OFF", use_tspace=True,
                         colors_type="LINEAR", bake_anim=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_skinned.blend"))
foot_off = [Vector((q.x - axis_at(q.z).x, q.y - axis_at(q.z).y, 0.0)).length - r_neck for q in foot_pts]
rep = {"neck_base_z": round(S.z, 3), "neck_radius_m": round(r_neck, 4), "collar_points": n, "collar_round_m": round(length, 3), "collar_height_m": [round(min(p.z for p in P), 3), round(max(p.z for p in P), 3)],
       "lip_m": LIP, "depth_m": DEPTH, "gap_m": GAP, "faces": len(made), "flipped": flipped,
       "edge_to_neck_m": [round(min(gaps), 4), round(sum(gaps) / n, 4), round(max(gaps), 4)],
       "foot_off_neck_m": [round(min(foot_off), 4), round(max(foot_off), 4)],
       "foot_strongest_bones": sorted({max(w, key=w.get) for w in foot_w}), "uvReordered": reordered,
       "material_index": mat_index, "uv_layers": len(uv_layers)}
json.dump(rep, open(os.path.join(OUT, "collar.json"), "w"), indent=1)
print("COLLAR " + json.dumps(rep), flush=True)
