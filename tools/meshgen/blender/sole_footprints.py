"""Each boot's footprint on the floor, measured from the finished, skinned pair, for the contact decals the game lays
under a wearer's soles (ue-probe LedgerGarments.h, "contact" in production/specs/garments.json).

    blender -b --factory-startup -P tools/meshgen/blender/sole_footprints.py -- PAIR_SKINNED.fbx OUT.json [--rise 0.025]

WHY, 30 October 2026 (his order C9, Tom's boots in the game; a fresh reviewer: "a pale band under both soles on the
wet paving"): the street's reflections are Lumen's in software, which traces only static meshes (Epic's Lumen
technical details, read 30 October: "Only Static Meshes, Instanced Static Meshes, Hierarchical Instanced Static Meshes,
and Landscape terrain are represented in the Lumen Scene"); a skinned boot is seen only on screen, so where the wet
floor under a toe looks up at the sole's underside, which the camera never sees, the reflection falls back to the sky.
A hidden stand-in the light alone sees (Affect Indirect Lighting While Hidden) was the engine's route, but Lumen's own
culling drops every mesh under 30 cm in radius (r.Lumen.DiffuseIndirect.MeshSDF.RadiusThreshold, LumenMeshSDFCulling)
and a boot is about 15. So the floor's own shine is taken away where a sole stands on it, as the floor itself would
show it: a deferred decal under each half of each sole writes Specular 0 through the DBuffer (Epic's
DBufferDecalShared.ush applies Specular with roughness), soft at its rim.

WHAT IT MEASURES, in terms that need no axis convention (Blender's and Unreal's differ by a mirror): each boot's
points within RISE of its lowest point (the sole, its welt and the toe's spring), split at the ball joint; in plan,
along the foot (the line from the foot joint's head to the ball joint's, flat) and across it (flat, outward from the
body's middle), each half's range in centimetres from the ball joint's head; and the sole's lowest height. The game
rebuilds the same frame from the same two joints of the body's own reference pose.
"""
import json
import sys

import bpy
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
PAIR, OUT = argv[:2]
RISE = float(argv[argv.index("--rise") + 1]) if "--rise" in argv else 0.025
OVERLAP = 0.01                  # each half reaches a centimetre past the ball line, so the two decals leave no seam

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=PAIR)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
pts = []
for o in bpy.data.objects:
    if o.type != "MESH":
        continue
    m = o.matrix_world
    pts += [tuple(m @ v.co) for v in o.data.vertices]
P = np.array(pts)
head = {b.name: np.array(arm.matrix_world @ b.head_local) for b in arm.data.bones}
rep = {"pair": PAIR, "rise_m": RISE, "sides": []}
for sn in ("l", "r"):
    F, B = head["foot_" + sn], head["ball_" + sn]
    side = P[(P[:, 0] > 0) == (B[0] > 0)]
    floor = float(side[:, 2].min())
    low = side[side[:, 2] < floor + RISE]
    f = (B - F) * np.array([1.0, 1.0, 0.0])
    f /= np.linalg.norm(f)
    a = np.array([-f[1], f[0], 0.0])
    if np.dot(a, B * np.array([1.0, 1.0, 0.0])) < 0:   # outward from the body's middle (its origin lies between the feet)
        a = -a
    u = (low - B) @ f
    v = (low - B) @ a
    parts = []
    for bone, sel in (("foot_" + sn, u <= OVERLAP), ("ball_" + sn, u >= -OVERLAP)):
        parts.append({"bone": bone,
                      "along_cm": [round(float(u[sel].min()) * 100, 1), round(float(u[sel].max()) * 100, 1)],
                      "across_cm": [round(float(v[sel].min()) * 100, 1), round(float(v[sel].max()) * 100, 1)],
                      "points": int(sel.sum())})
    rep["sides"].append({"side": sn, "floor_cm": round(floor * 100, 2), "ball_head_cm": [round(float(x) * 100, 1) for x in B],
                         "foot_head_cm": [round(float(x) * 100, 1) for x in F], "parts": parts})
json.dump(rep, open(OUT, "w"), indent=1)
print("FOOTPRINTS " + json.dumps(rep), flush=True)
