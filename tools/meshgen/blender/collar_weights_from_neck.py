"""A skinned garment's collar made to follow the neck: its weights near the collar taken again from a body that has a
neck, blended into the garment's own weights below.

    blender -b SKINNED.blend -P tools/meshgen/blender/collar_weights_from_neck.py -- FULLBODY.fbx OUT_DIR NAME
            [--depth 0.09] [--max-influences 8] [--fold head,neck_02:neck_01] [--ease-front 0.006]

WHY, 30 October 2026 (his order C9, the jacket's collar, second try): as Tom stands his throat's skin shows through the
collar's front. Measured (production/art/clothing/tom-outfit/BAKE-PLAN-2026-10-27.md, the collar's second try): at the
bind pose the collar stands about 4.5 mm off his neck all round, but with the head tipped only 10 degrees down the
throat comes 9 mm through the collar's front (19 mm at 20 degrees), because the garment's weights were taken from a
body mesh with no neck (MH_TomL1_Body.fbx ends at the neck's base), so the collar's nearest skin was his shoulders and
chest and it follows the trunk while the throat follows the neck. Mafia's jacket's collar rides the neck (its weights
neck_twist_01 76%, spine_04 20%: production/research/game-clothing-pipeline/MAFIA-JACKET-2026-10-28.md, section 4).

WHAT IT DOES: the collar is NAME's highest open ring. Each point within DEPTH below the collar's top takes the full
body's weights at its nearest skin (barycentric over that triangle, the strongest MAX kept, summing to one), blended
with its own by a factor running from one at the collar's top to nil at DEPTH below (smoothstep), so the change dies out
on the shoulders and chest. --fold moves the weights of the bones named before the colon onto the one after it (the
collar rides the neck's base and never turns with the head: Mafia's collar has no head weight). --ease-front stands the
collar's front off the throat by that much, radially from the neck's line (neck_01 to the head bone): in full from 10 to
60 mm below the collar's top within 25 degrees of straight ahead, tapering to nil at 50 degrees and 80 mm, for the
depth the throat still comes through with the head tipped down as the held face allows. OUT_DIR gets NAME_skinned.fbx (skin_garment.py's export), NAME_skinned.blend and
collar_weights.json.
"""
import json
import os
import sys
from collections import defaultdict

import bmesh
import bpy
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
FULL, OUT, NAME = argv[:3]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


DEPTH, MAXI = opt("--depth", 0.09), opt("--max-influences", 8, int)
FOLD = {}
if "--fold" in argv:
    src, dst = argv[argv.index("--fold") + 1].split(":")
    FOLD = {b: dst for b in src.split(",")}
EASE = opt("--ease-front", 0.0)
os.makedirs(OUT, exist_ok=True)
g = bpy.data.objects[NAME]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=FULL)
new = [o for o in bpy.data.objects if o not in before]
body = next(o for o in new if o.type == "MESH" and o.name.endswith("_LOD0"))

# THE FULL BODY'S SKIN, in the world, and each corner's weights by bone name
dg = bpy.context.evaluated_depsgraph_get()
bme = body.data
bme.calc_loop_triangles()
bw = body.matrix_world
bverts = [bw @ v.co for v in bme.vertices]
btris = [tuple(t.vertices) for t in bme.loop_triangles]
tree = BVHTree.FromPolygons(bverts, btris)
bnames = {gr.index: gr.name for gr in body.vertex_groups}
bweights = [{bnames[e.group]: e.weight for e in v.groups if e.weight > 1e-4} for v in bme.vertices]


def body_weights_at(p):
    hit, _n, fi, _d = tree.find_nearest(p)
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
    return mix


# THE COLLAR'S TOP: the highest open ring
bm = bmesh.new()
bm.from_mesh(g.data)
adj = defaultdict(list)
for e in bm.edges:
    if e.is_boundary:
        a, b = e.verts[0].index, e.verts[1].index
        adj[a].append(b)
        adj[b].append(a)
gw = g.matrix_world
P = [gw @ v.co for v in g.data.vertices]
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
bm.free()
collar = max(rings, key=lambda r: max(P[i].z for i in r))
top = max(P[i].z for i in collar)

gnames = {gr.index: gr.name for gr in g.vertex_groups}
changed, strongest = 0, defaultdict(int)
for v in g.data.vertices:
    below = top - P[v.index].z
    if below > DEPTH:
        continue
    x = max(0.0, min(1.0, 1.0 - below / DEPTH))
    t = x * x * (3.0 - 2.0 * x)
    own = {gnames[e.group]: e.weight for e in v.groups if e.weight > 1e-5}
    neck = {}
    for b, w in body_weights_at(P[v.index]).items():
        neck[FOLD.get(b, b)] = neck.get(FOLD.get(b, b), 0.0) + w
    mix = {b: (1.0 - t) * own.get(b, 0.0) + t * neck.get(b, 0.0) for b in set(own) | set(neck)}
    top_ = sorted(((b, w) for b, w in mix.items() if w > 1e-4), key=lambda kv: -kv[1])[:MAXI]
    s = sum(w for _b, w in top_) or 1.0
    for e in list(v.groups):
        g.vertex_groups[e.group].remove([v.index])
    for b, w in top_:
        (g.vertex_groups.get(b) or g.vertex_groups.new(name=b)).add([v.index], w / s, "REPLACE")
    changed += 1
    strongest[top_[0][0]] += 1

# THE FRONT EASED OFF THE THROAT
import math  # noqa: E402
from mathutils import Vector  # noqa: E402
eased, peak = 0, 0.0
if EASE > 0:
    aw = arm.matrix_world
    N1 = aw @ arm.data.bones["neck_01"].head_local
    HB = aw @ arm.data.bones["head"].head_local
    up = (HB - N1).normalized()
    fwd = Vector((0.0, -1.0, 0.0))
    gwi = gw.inverted()
    for v in g.data.vertices:
        below = top - P[v.index].z
        if below < 0 or below > 0.08:
            continue
        rel = P[v.index] - N1
        rad = rel - up * rel.dot(up)
        if rad.length < 1e-6:
            continue
        ang = math.degrees(math.acos(max(-1.0, min(1.0, rad.normalized().dot(fwd)))))
        wa = 1.0 if ang <= 25 else max(0.0, 1.0 - (ang - 25) / 25.0)
        wh = 1.0 if 0.01 <= below <= 0.06 else (0.5 + 50.0 * below if below < 0.01 else max(0.0, 1.0 - (below - 0.06) / 0.02))
        d = EASE * wa * wh
        if d <= 0:
            continue
        v.co = gwi @ (P[v.index] + rad.normalized() * d)
        eased += 1
        peak = max(peak, d)
    g.data.update()

for o in new:
    bpy.data.objects.remove(o, do_unlink=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uv_order import maps_layout_first  # noqa: E402

reordered = maps_layout_first(g)
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
g.select_set(True)
bpy.context.view_layer.objects.active = arm
for o in bpy.data.objects:
    if o.type == "MESH" and o is not g:
        o.select_set(False)
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_skinned.fbx"), use_selection=True,
                         object_types={"ARMATURE", "MESH"}, add_leaf_bones=False, mesh_smooth_type="OFF", use_tspace=True,
                         colors_type="LINEAR", bake_anim=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_skinned.blend"))
rep = {"collar_top_z": round(top, 4), "depth_m": DEPTH, "points_reweighted": changed,
       "strongest_bone_counts": dict(sorted(strongest.items(), key=lambda kv: -kv[1])), "uvReordered": reordered,
       "fold": FOLD, "ease_front_m": EASE, "points_eased": eased, "ease_peak_m": round(peak, 4)}
json.dump(rep, open(os.path.join(OUT, "collar_weights.json"), "w"), indent=1)
print("COLLAR-WEIGHTS " + json.dumps(rep), flush=True)
