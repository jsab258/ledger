"""A skinned garment's faces split between two material slots, "Shown" and "Hidden", for a garment worn under another,
whose covered parts the game hides with an invisible material on one slot.

    blender -b SKINNED.blend -P tools/meshgen/blender/garment_slots.py -- PLAN.json OUT_DIR NAME
            --shown neckband,cuffL,cuffR [--beside 0.020] [--names Shown,Hidden]

WHY, 30 October 2026 (Tom's jumper, his order C9; JUMPER-PLAN-2026-10-29.md, "Under the jacket"): under the jacket
only the jumper's neckband and, where the sleeves ride up, its cuffs show. Mafia hides a garment's covered parts by a
slot whose material draws nothing (production/research/game-clothing-pipeline/MAFIA-SWEATER-2026-10-29.md, 2), so the
jumper's listed faults under the jacket (the sleeves' last stretch above the cuffs, the armpits) never draw.

WHAT IT DOES: the pieces named by --shown (the plan's keys, read from the garment's "piece" face attribute, the plan's
order) and every face of any other piece reaching within --beside metres of them (any of its points nearer), measured along the
garment's own edges from the points they share (so the shell's rows covering at least that band), take the first slot; every other face
the second. The garment's own materials are replaced by the two slots (the baked maps carry the parts' ID, so the
slots say only what draws). OUT_DIR gets NAME_skinned.fbx (skin_garment.py's export: the maps' layout first),
NAME_skinned.blend and slots.json (the faces in each slot by piece, the distance used, the shared points).
"""
import heapq
import json
import os
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
PLAN, OUT, NAME = argv[:3]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


SHOWN = opt("--shown", "", str).split(",")
BESIDE = opt("--beside", 0.020)
SLOT_SHOWN, SLOT_HIDDEN = opt("--names", "Shown,Hidden", str).split(",")
os.makedirs(OUT, exist_ok=True)
names = [p["key"] for p in json.load(open(PLAN, encoding="utf-8"))["pieces"]]
missing = [s for s in SHOWN if s not in names]
if missing:
    raise SystemExit("SLOTS pieces not in the plan: %s" % missing)
g = bpy.data.objects[NAME]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
me = g.data
pa = me.attributes["piece"].data
piece_of = [names[pa[p.index].value] for p in me.polygons]
P = [g.matrix_world @ v.co for v in me.vertices]

# the points of the shown pieces, and the distance of every point from them along the garment's edges
shown_pts = {i for p, n in zip(me.polygons, piece_of) if n in SHOWN for i in p.vertices}
adj = [[] for _ in P]
for e in me.edges:
    a, b = e.vertices
    d = (P[a] - P[b]).length
    adj[a].append((b, d))
    adj[b].append((a, d))
dist = [float("inf")] * len(P)
heap = [(0.0, i) for i in shown_pts]
for _d, i in heap:
    dist[i] = 0.0
heapq.heapify(heap)
while heap:
    d, i = heapq.heappop(heap)
    if d > dist[i] or d > BESIDE + 0.001:
        continue
    for j, w in adj[i]:
        if d + w < dist[j]:
            dist[j] = d + w
            heapq.heappush(heap, (d + w, j))

slot = []
for p, n in zip(me.polygons, piece_of):
    # a face reaching into the band beside (any of its points nearer than --beside), so the whole of it is covered
    near = n in SHOWN or min(dist[i] for i in p.vertices) < BESIDE - 1e-6
    slot.append(0 if near else 1)
me.materials.clear()
for nm in (SLOT_SHOWN, SLOT_HIDDEN):
    me.materials.append(bpy.data.materials.get(nm) or bpy.data.materials.new(nm))
for p, s in zip(me.polygons, slot):
    p.material_index = s
me.update()

by_piece = {}
for n, s in zip(piece_of, slot):
    b = by_piece.setdefault(n, [0, 0])
    b[s] += 1
shown_v = sorted({i for p, s in zip(me.polygons, slot) if s == 0 for i in p.vertices})
rep = {"shownPieces": SHOWN, "besideM": BESIDE, "slots": [SLOT_SHOWN, SLOT_HIDDEN],
       "facesBySlot": {SLOT_SHOWN: slot.count(0), SLOT_HIDDEN: slot.count(1)},
       "facesByPiece": {n: {SLOT_SHOWN: b[0], SLOT_HIDDEN: b[1]} for n, b in by_piece.items()},
       "shownPoints": len(shown_v),
       "shownFaces": [i for i, s in enumerate(slot) if s == 0]}

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uv_order import maps_layout_first  # noqa: E402

rep["uvReordered"] = maps_layout_first(g)
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
g.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_skinned.fbx"), use_selection=True,
                         object_types={"ARMATURE", "MESH"}, add_leaf_bones=False, mesh_smooth_type="OFF", use_tspace=True,
                         colors_type="LINEAR", bake_anim=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_skinned.blend"))
json.dump(rep, open(os.path.join(OUT, "slots.json"), "w"), indent=1)
json.dump({"shown": shown_v, "hidden": sorted(set(range(len(P))) - set(shown_v))},
          open(os.path.join(OUT, "slot_points.json"), "w"))
print("SLOTS " + json.dumps({k: v for k, v in rep.items() if k != "shownFaces"}), flush=True)
