"""The silhouette of a reduced mesh against its scan, and a texture layout's padding (30 October 2026, Tom's shoes;
the system Python with NumPy, SciPy and Pillow, beside tools/meshgen/blender/scan_lods.py).

    python tools/meshgen/silhouette_check.py SILHOUETTES.npz OUT.json [--px-mm 0.1] [--layout LAYOUT_OWNER.npy]

Each level's and the scan's triangles are drawn filled in three orthographic projections (front, side, top; a
silhouette is the same from the opposite side) at --px-mm; the deviation is the Hausdorff distance between the
two filled silhouettes, in millimetres (the largest distance of any pixel of one outside the other). With --layout,
the smallest gap between two different islands of a layout (texels), from the owner raster scan_lods.py writes.
"""
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

args = sys.argv[1:]
NPZ, OUT = args[0], args[1]
PX = float(args[args.index("--px-mm") + 1]) / 1000 if "--px-mm" in args else 0.0001
LAYOUT = args[args.index("--layout") + 1] if "--layout" in args else None
d = np.load(NPZ)
names = sorted({k[:-3] for k in d.files if k.endswith("_co")})
VIEWS = {"front": (1, 2), "side": (0, 2), "top": (0, 1)}
allco = np.vstack([d[n + "_co"] for n in names])
lo = allco.min(0) - 0.003
hi = allco.max(0) + 0.003


def mask(co, tris, ax):
    i, j = ax
    w = int((hi[i] - lo[i]) / PX) + 1
    h = int((hi[j] - lo[j]) / PX) + 1
    im = Image.new("1", (w, h), 0)
    dr = ImageDraw.Draw(im)
    P = np.stack([(co[:, i] - lo[i]) / PX, (co[:, j] - lo[j]) / PX], 1)
    for t in tris:
        dr.polygon([tuple(P[t[0]]), tuple(P[t[1]]), tuple(P[t[2]])], fill=1)
    return np.array(im, bool)


ref = {v: mask(d["scan_co"], d["scan_tris"], ax) for v, ax in VIEWS.items()}
dist_out = {v: ndimage.distance_transform_edt(~m) * PX * 1000 for v, m in ref.items()}
dist_in = {v: ndimage.distance_transform_edt(m) * PX * 1000 for v, m in ref.items()}
rep = {"pxMm": PX * 1000, "levels": {}}
for n in names:
    if n == "scan":
        continue
    r = {}
    for v, ax in VIEWS.items():
        m = mask(d[n + "_co"], d[n + "_tris"], ax)
        grow = float(dist_out[v][m & ~ref[v]].max()) if (m & ~ref[v]).any() else 0.0
        mdist_out = ndimage.distance_transform_edt(~m) * PX * 1000
        shrink = float(mdist_out[ref[v] & ~m].max()) if (ref[v] & ~m).any() else 0.0
        r[v] = {"outsideScanMm": round(grow, 3), "scanOutsideMm": round(shrink, 3), "hausdorffMm": round(max(grow, shrink), 3)}
    r["worstMm"] = max(x["hausdorffMm"] for x in r.values())
    rep["levels"][n] = r
    print("SIL", n, json.dumps(r))
if LAYOUT:
    own = np.load(LAYOUT)
    occ = own >= 0
    big = own.max() + 1
    gap = None
    for rad in range(1, 33):
        y, x = np.ogrid[-rad:rad + 1, -rad:rad + 1]
        fp = x * x + y * y <= rad * rad
        mx = ndimage.maximum_filter(own, footprint=fp, mode="constant", cval=-1)
        mn = ndimage.minimum_filter(np.where(occ, own, big), footprint=fp, mode="constant", cval=big)
        clash = occ & ((mx != own) | ((mn != own) & (mn != big)))
        if clash.any():
            gap = rad - 1          # empty texels between the two islands
            break
    # the edge of the square counts as a neighbour too (bleeding wraps under tiling)
    ys, xs = np.where(occ)
    edge = int(min(xs.min(), ys.min(), own.shape[1] - 1 - xs.max(), own.shape[0] - 1 - ys.max()))
    rep["layout"] = {"islands": int(len(np.unique(own[occ]))), "smallestGapTexels": gap, "edgeGapTexels": edge,
                     "usedShare": round(float(occ.mean()), 4)}
    print("LAYOUT", json.dumps(rep["layout"]))
json.dump(rep, open(OUT, "w"), indent=1)
