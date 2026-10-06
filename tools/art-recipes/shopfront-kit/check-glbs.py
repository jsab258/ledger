"""Re-import every shopfront-kit glb into an empty Blender scene and check it: its objects and
parenting, one UV map with no overlapping UV pixels at 2048 x 2048, all UVs inside 0..1, custom
normals, the COLOR_0 masks (red = ao, green = edges) against the bake kept in the .blend, the
measured size against the piece's report, its base on the pavement datum and the file under 1 MB.

    blender.exe -b --factory-startup -P tools/art-recipes/shopfront-kit/check-glbs.py

Writes F:\\LedgerTools\\shopfront-kit\\blend\\glb-check.json and prints one line per glb.
"""
import json
import math
import os

import bpy
import numpy as np
from mathutils import Vector

GLB_DIR = r"F:\LedgerTools\game-inputs\production\assets\shopfront-kit"
BLEND_DIR = r"F:\LedgerTools\shopfront-kit\blend"
PIECES = ["pilaster", "stallriser_panelled", "stallriser_tile", "window_frame", "shop_door", "side_door"]


def uv_overlap(objs, res=2048):
    """Every UV triangle rasterised at res x res; a pixel strictly inside two triangles overlaps."""
    owner = np.zeros((res, res), dtype=np.int64)
    over, gid, inside = 0, 0, True
    for o in objs:
        me = o.data
        me.calc_loop_triangles()
        uv = me.uv_layers.active.data
        n = len(me.loop_triangles)
        loops = np.zeros(n * 3, dtype=np.int64)
        me.loop_triangles.foreach_get("loops", loops)
        uvs = np.zeros(len(uv) * 2)
        uv.foreach_get("uv", uvs)
        uvs = uvs.reshape(-1, 2)
        if uvs.min() < -1e-6 or uvs.max() > 1 + 1e-6:
            inside = False
        for t in uvs[loops].reshape(-1, 3, 2) * res:
            gid += 1
            (x0, y0), (x1, y1), (x2, y2) = t
            area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
            if abs(area) < 1e-12:
                continue
            ix0, ix1 = int(max(math.floor(min(x0, x1, x2)), 0)), int(min(math.ceil(max(x0, x1, x2)), res - 1))
            iy0, iy1 = int(max(math.floor(min(y0, y1, y2)), 0)), int(min(math.ceil(max(y0, y1, y2)), res - 1))
            if ix1 < ix0 or iy1 < iy0:
                continue
            px, py = np.meshgrid(np.arange(ix0, ix1 + 1) + 0.5, np.arange(iy0, iy1 + 1) + 0.5)
            w0 = ((x1 - px) * (y2 - py) - (x2 - px) * (y1 - py)) / area
            w1 = ((x2 - px) * (y0 - py) - (x0 - px) * (y2 - py)) / area
            m = (w0 > 1e-5) & (w1 > 1e-5) & (1.0 - w0 - w1 > 1e-5)
            sub = owner[iy0:iy1 + 1, ix0:ix1 + 1]
            over += int((sub[m] > 0).sum())
            sub[m] = gid
    return over, inside


def colour_stats(o, name=None):
    ca = o.data.color_attributes[name] if name else o.data.color_attributes[0]
    v = np.zeros(len(ca.data) * 4)
    ca.data.foreach_get("color", v)
    v = v.reshape(-1, 4)
    return {"name": ca.name, "domain": ca.domain, "red_mean": round(float(v[:, 0].mean()), 3),
            "green_mean": round(float(v[:, 1].mean()), 3), "blue_max": round(float(v[:, 2].max()), 3),
            "alpha_min": round(float(v[:, 3].min()), 3)}


def mask_means(blend, names):
    """The 'ao' and 'edges' bakes' means as the .blend keeps them (point domain)."""
    with bpy.data.libraries.load(blend) as (src, dst):
        dst.meshes = [m for m in src.meshes if m in names]
    out = {}
    for me in dst.meshes:
        r = {}
        for nm in ("ao", "edges"):
            ca = me.color_attributes.get(nm)
            if ca:
                v = np.zeros(len(ca.data) * 4)
                ca.data.foreach_get("color", v)
                r[nm] = round(float(v.reshape(-1, 4)[:, 0].mean()), 3)
        out[me.name] = r
    return out


results = {}
for p in PIECES:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    glb = os.path.join(GLB_DIR, p + ".glb")
    rep = json.load(open(os.path.join(BLEND_DIR, p + ".report.json")))
    bpy.ops.import_scene.gltf(filepath=glb)
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = [min(q[i] for q in pts) for i in range(3)]
    hi = [max(q[i] for q in pts) for i in range(3)]
    size = [round(hi[i] - lo[i], 4) for i in range(3)]
    want = [rep["size_m"][k] for k in ("x", "y", "z")]
    over, inside = uv_overlap(objs)
    tris = 0
    for o in objs:
        o.data.calc_loop_triangles()
        tris += len(o.data.loop_triangles)
    blend_masks = mask_means(os.path.join(BLEND_DIR, p + ".blend"), [o.data.name for o in objs] + [o.name for o in objs])
    r = {"glb_bytes": os.path.getsize(glb), "under_1MB": os.path.getsize(glb) < 1024 * 1024,
         "objects": {o.name: (o.parent.name if o.parent else None) for o in objs},
         "uv_maps": {o.name: [u.name for u in o.data.uv_layers] for o in objs},
         "one_uv_map": all(len(o.data.uv_layers) == 1 for o in objs),
         "uv_overlap_px_2048": over, "uv_inside_0_1": inside,
         "custom_normals": all(o.data.has_custom_normals for o in objs),
         "colour_sets": {o.name: [c.name for c in o.data.color_attributes] for o in objs},
         "COLOR_0": {o.name: colour_stats(o) for o in objs if o.data.color_attributes},
         "blend_masks": blend_masks,
         "size_m": size, "size_matches_report": all(abs(a - b) < 1e-3 for a, b in zip(size, want)),
         "base_z": round(lo[2], 4), "triangles": tris, "materials": sorted({s.material.name for o in objs for s in o.material_slots if s.material})}
    results[p] = r
    print("GLBCHECK", p, json.dumps(r))

with open(os.path.join(BLEND_DIR, "glb-check.json"), "w") as f:
    json.dump(results, f, indent=1)
