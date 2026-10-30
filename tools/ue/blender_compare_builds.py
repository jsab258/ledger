"""WHAT A METAHUMAN REBUILD CHANGED, from two exports of the same character (30 October 2026, Tom's hidden faces).

    blender -b --factory-startup -P tools/ue/blender_compare_builds.py -- BEFORE_DIR AFTER_DIR OUT.json

Each directory is tools/ue/hidden_faces.py's record: SKM_*.fbx (every LOD, no morph targets), a few baked
textures as PNG, record.json (assets, mesh stats, every material instance's parameters).

Per mesh and LOD: points and faces before and after; when the counts match, the largest move of any point
(the same index); when they do not (the body, cut), the largest distance from each point after to the nearest
point before (a kept point must not move) and the faces gone. Per skeleton: bones before and after, and the
largest move of any bone's head and tail at rest (the armature's own space, in mm). Per texture: size, the
largest and mean difference in 8-bit steps, and the share of pixels that differ. Materials: every parameter
that differs. Assets: added and gone.
"""
import json
import os
import sys

import bpy
import numpy as np
from mathutils.kdtree import KDTree

argv = sys.argv[sys.argv.index("--") + 1:]
BEFORE, AFTER, OUT = argv[:3]


def load(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=path)
    arm = next((o for o in bpy.data.objects if o.type == "ARMATURE"), None)
    lods = {}
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        n = o.name.rsplit("_LOD", 1)
        lod = int(n[1]) if len(n) == 2 and n[1].isdigit() else 0
        co = np.zeros(len(o.data.vertices) * 3)
        o.data.vertices.foreach_get("co", co)
        co = co.reshape(-1, 3)
        M = np.array(o.matrix_world)
        co = co @ M[:3, :3].T + M[:3, 3]
        lods[lod] = {"co": co, "faces": len(o.data.polygons)}
    bones = {}
    if arm is not None:
        A = np.array(arm.matrix_world)
        for b in arm.data.bones:
            h = A[:3, :3] @ np.array(b.head_local) + A[:3, 3]
            t = A[:3, :3] @ np.array(b.tail_local) + A[:3, 3]
            bones[b.name] = (h, t)
    return lods, bones


def compare_mesh(name):
    a, b = os.path.join(BEFORE, name), os.path.join(AFTER, name)
    if not (os.path.exists(a) and os.path.exists(b)):
        return {"missing": [p for p in (a, b) if not os.path.exists(p)]}
    la, ba = load(a)
    lb, bb = load(b)
    out = {"lods": {}}
    for lod in sorted(set(la) | set(lb)):
        if lod not in la or lod not in lb:
            out["lods"][lod] = {"before": lod in la, "after": lod in lb}
            continue
        A, B = la[lod]["co"], lb[lod]["co"]
        r = {"points": [len(A), len(B)], "faces": [la[lod]["faces"], lb[lod]["faces"]],
             "faces_gone": la[lod]["faces"] - lb[lod]["faces"]}
        if len(A) == len(B):
            r["max_move_same_index_mm"] = round(float(np.abs(A - B).max()) * 1000, 4)
        kd = KDTree(len(A))
        for i, c in enumerate(A):
            kd.insert(c, i)
        kd.balance()
        d = np.array([kd.find(c)[2] for c in B])
        r["after_to_nearest_before_mm"] = {"max": round(float(d.max()) * 1000, 4), "p99": round(float(np.percentile(d, 99)) * 1000, 4)}
        out["lods"][lod] = r
    common = set(ba) & set(bb)
    moves = sorted(((max(np.abs(ba[n][0] - bb[n][0]).max(), np.abs(ba[n][1] - bb[n][1]).max()) * 1000, n) for n in common), reverse=True)
    out["bones"] = {"before": len(ba), "after": len(bb), "only_before": sorted(set(ba) - set(bb))[:20],
                    "only_after": sorted(set(bb) - set(ba))[:20],
                    "max_move_mm": round(float(moves[0][0]), 5) if moves else None, "worst": [[n, round(float(m), 5)] for m, n in moves[:5]]}
    return out


def png(path):
    im = bpy.data.images.load(path)
    im.colorspace_settings.name = "Non-Color"
    w, h = im.size
    px = np.empty(w * h * im.channels, np.float32)
    im.pixels.foreach_get(px)
    bpy.data.images.remove(im)
    return np.round(px.reshape(h, w, -1) * 255).astype(np.uint8)


report = {"before": BEFORE, "after": AFTER, "meshes": {}, "textures": {}}
names = sorted(n for n in os.listdir(BEFORE) if n.endswith(".fbx"))
for n in names:
    report["meshes"][n] = compare_mesh(n)
    print("MESH", n, json.dumps(report["meshes"][n])[:600], flush=True)
for n in sorted(x for x in os.listdir(BEFORE) if x.endswith(".png")):
    a, b = os.path.join(BEFORE, n), os.path.join(AFTER, n)
    if not os.path.exists(b):
        report["textures"][n] = "missing after"
        continue
    A, B = png(a), png(b)
    if A.shape != B.shape:
        report["textures"][n] = {"shape": [list(A.shape), list(B.shape)]}
        continue
    D = np.abs(A.astype(np.int16) - B.astype(np.int16)).astype(np.uint8)
    size = list(A.shape[:2])
    del A, B
    report["textures"][n] = {"size": size, "max_step": int(D.max()), "mean_step": round(float(D.mean()), 4),
                             "pixels_differing": round(float((D.max(-1) > 0).mean()), 5)}
    print("TEX", n, report["textures"][n], flush=True)
ra = json.load(open(os.path.join(BEFORE, "record.json"), encoding="utf-8"))
rb = json.load(open(os.path.join(AFTER, "record.json"), encoding="utf-8"))
strip = lambda p: p.split("/")[-1]  # noqa: E731  the two builds sit in different folders
aa = {strip(p): c for p, c in ra["assets"].items()}
ab = {strip(p): c for p, c in rb["assets"].items()}
report["assets"] = {"before": len(aa), "after": len(ab), "gone": sorted(set(aa) - set(ab)), "added": sorted(set(ab) - set(aa))}
ma = {strip(p): v for p, v in ra["materials"].items()}
mb = {strip(p): v for p, v in rb["materials"].items()}
diffs = {}
for n in sorted(set(ma) & set(mb)):
    d = {}
    for k in sorted(set(ma[n]) | set(mb[n])):
        va, vb = ma[n].get(k), mb[n].get(k)
        if isinstance(va, str) and isinstance(vb, str) and k.startswith("t:"):
            va, vb = strip(va), strip(vb)
        if k == "parent":
            continue
        if va != vb:
            d[k] = [va, vb]
    if d:
        diffs[n] = d
report["materials"] = {"compared": len(set(ma) & set(mb)), "differing": diffs}
report["mesh_stats"] = {"before": ra.get("meshes"), "after": rb.get("meshes")}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(report, fh, indent=1, default=str)
print("COMPARE done " + OUT, flush=True)
