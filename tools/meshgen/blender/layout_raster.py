"""A game mesh's texture layout rasterised: for every texel, which pattern piece it lies on, where on that piece's own
pattern it is (millimetres), and where on the body it sits (the mesh's own pose); and each piece's outline as runs of
segments in its pattern. The input for drawing construction detail (seams, stitch rows, pockets) into baked maps by
the pattern's own measures (garment_details.py).

    blender -b --factory-startup -P tools/meshgen/blender/layout_raster.py -- LOW.blend OUT.npz
        [--object Low] [--layout UVMap] [--pattern pattern] [--tex 2048] [--import IMPORT.json] [--flat]

WHY, 30 October 2026 (Tom's jeans: a fresh reviewer read them as plain blue trousers, with no pockets, yoke, fly or
seams; the game-garment skill, steps 6 and 8: the silhouette in the mesh, seams, stitch lines and pocket edges in the
normal map). The low mesh carries two layouts: the maps' (--layout, packed by uv_pack_low.py) and the flat pattern's
(--pattern, metres, each piece shifted along x by its layoutOffsetM in the import record). Every detail is placed in a
piece's pattern millimetres, as a pattern maker marks it, and found in the maps through this raster, so it lands on the
cloth where the pattern puts it whatever the packing did to the island.

--flat (30 October, the first look on the body: the back pockets' straight inner edges came out ragged on the seat):
the low mesh's pattern layout is not its own surface flattened. Its points took their pattern places from the drape,
whose folds it does not keep, so from face to face it is stretched and sheared against the pattern (5% to 95% of its
texels between 0.82 and 1.18), and a line straight in the pattern zigzags across the low mesh's smooth surface. With
--flat each piece of the low mesh is flattened itself (Blender's minimum-stretch unwrap, the pieces cut apart at their
seams) and laid onto its pattern by the best turn, scale and shift (least squares over its points, a mirror allowed), so
px, py are a place on the piece that is straight on the surface the game draws and within a few millimetres of the
pattern's (the RASTER line's "flat" gives how far, per piece); the pattern's own places are kept as px_pat, py_pat.
Either way jq (the place's rates per texel: dpx/du, dpx/dv, dpy/du, dpy/dv) and met (the body's millimetres per texel
along u and along v) are written per texel, from each triangle.

The file is opened and never saved. Writes OUT.npz: piece (int16, -1 off the layout), px, py (pattern mm, the import's
offset taken off), pos (world metres) and nrm (the face's world normal), all TEX x TEX with row 0 at v = 0 (Blender's
order); seg_piece, seg_a, seg_b (each outline segment's piece and its two ends in pattern mm), seg_pa, seg_pb (the same
ends on the body), seg_a_pat, seg_b_pat (the ends' pattern places, for finding the plan's corners), seg_other (the piece across that edge, -1 for an open edge); names (the pieces' names by index,
from the mesh's "piece" attribute order in the import record).
"""
import json
import sys

import bmesh
import bpy
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
LOW, OUT = argv[0], argv[1]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
OBJ = opt("--object", "Low", str)
LAYOUT = opt("--layout", "UVMap", str)
PATTERN = opt("--pattern", "pattern", str)
TEX = opt("--tex", 2048, int)
IMPORT = opt("--import", "", str)
FLAT = "--flat" in argv

bpy.ops.wm.open_mainfile(filepath=LOW)
o = bpy.data.objects[OBJ]
me = o.data
mw = o.matrix_world
nm3 = mw.to_3x3()
# the pieces' names and offsets from the import record (its "pieces" in index order), else bare numbers and no offset
names, offs = {}, {}
if IMPORT:
    imp = json.load(open(IMPORT, encoding="utf-8"))
    for k, v in imp["pieces"].items():
        names[v["index"]] = k
        offs[v["index"]] = v.get("layoutOffsetM", 0.0)
stats = {}
if FLAT:
    me.uv_layers.new(name="flat_tmp")
    me.uv_layers.active = me.uv_layers["flat_tmp"]
    for ob in bpy.context.view_layer.objects:
        ob.select_set(ob == o)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(me)
    lay = bm.faces.layers.int["piece"]
    for e in bm.edges:
        fs = e.link_faces
        e.seam = len(fs) == 2 and fs[0][lay] != fs[1][lay]
    for f in bm.faces:
        f.select = True
    bmesh.update_edit_mesh(me)
    bpy.ops.uv.unwrap(method="MINIMUM_STRETCH", margin=0.0)
    bpy.ops.object.mode_set(mode="OBJECT")
uvl = me.uv_layers[LAYOUT].data
pat = me.uv_layers[PATTERN].data
pattr = me.attributes["piece"].data
# every loop's place on its piece, mm: the pattern's, or (--flat) the piece's own flattening laid onto the pattern
NL = len(me.loops)
loop_piece = np.zeros(NL, dtype=np.int32)
for poly in me.polygons:
    for t in poly.loop_indices:
        loop_piece[t] = pattr[poly.index].value
pp = np.array([((pat[t].uv.x - offs.get(int(loop_piece[t]), 0.0)) * 1000.0, pat[t].uv.y * 1000.0) for t in range(NL)])
place = pp.copy()
if FLAT:
    fl = me.uv_layers["flat_tmp"].data
    ff = np.array([(fl[t].uv.x, fl[t].uv.y) for t in range(NL)])
    for k in np.unique(loop_piece):
        m = loop_piece == k
        F, Pp = ff[m], pp[m]
        fc, pc_ = F.mean(axis=0), Pp.mean(axis=0)
        U, S, Vt = np.linalg.svd((Pp - pc_).T @ (F - fc))
        Rm = U @ Vt
        sc = S.sum() / ((F - fc) ** 2).sum()
        q = (sc * (Rm @ (F - fc).T)).T + pc_
        place[m] = q
        err = np.hypot(*(q - Pp).T)
        stats[names.get(int(k), str(k))] = {"pattern_rms_mm": round(float(np.sqrt((err ** 2).mean())), 2),
                                             "pattern_max_mm": round(float(err.max()), 2),
                                             "mirrored": bool(np.linalg.det(Rm) < 0)}

piece = np.full((TEX, TEX), -1, dtype=np.int16)
px = np.zeros((TEX, TEX), dtype=np.float32)
py = np.zeros((TEX, TEX), dtype=np.float32)
px_pat = np.zeros((TEX, TEX), dtype=np.float32)
py_pat = np.zeros((TEX, TEX), dtype=np.float32)
pos = np.zeros((TEX, TEX, 3), dtype=np.float32)
nrm = np.zeros((TEX, TEX, 3), dtype=np.float32)
jq = np.zeros((TEX, TEX, 4), dtype=np.float32)
met = np.zeros((TEX, TEX, 2), dtype=np.float32)
co = np.array([tuple(mw @ v.co) for v in me.vertices], dtype=np.float64)
for poly in me.polygons:
    li = list(poly.loop_indices)
    k = pattr[poly.index].value
    fn = (nm3 @ poly.normal).normalized()
    for j in range(1, len(li) - 1):
        tri = (li[0], li[j], li[j + 1])
        xs = [uvl[t].uv.x * TEX for t in tri]
        ys = [uvl[t].uv.y * TEX for t in tri]
        x0, x1 = max(0, int(min(xs))), min(TEX - 1, int(max(xs)) + 1)
        y0, y1 = max(0, int(min(ys))), min(TEX - 1, int(max(ys)) + 1)
        if x1 < x0 or y1 < y0:
            continue
        d = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
        if abs(d) < 1e-12:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        l1 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / d
        l2 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / d
        l3 = 1 - l1 - l2
        ins = (l1 >= -1e-4) & (l2 >= -1e-4) & (l3 >= -1e-4)
        if not ins.any():
            continue
        sl = (slice(y0, y1 + 1), slice(x0, x1 + 1))
        piece[sl][ins] = k
        pxs = [place[t, 0] for t in tri]
        pys = [place[t, 1] for t in tri]
        px[sl][ins] = (l1 * pxs[0] + l2 * pxs[1] + l3 * pxs[2])[ins]
        py[sl][ins] = (l1 * pys[0] + l2 * pys[1] + l3 * pys[2])[ins]
        px_pat[sl][ins] = (l1 * pp[tri[0], 0] + l2 * pp[tri[1], 0] + l3 * pp[tri[2], 0])[ins]
        py_pat[sl][ins] = (l1 * pp[tri[0], 1] + l2 * pp[tri[1], 1] + l3 * pp[tri[2], 1])[ins]
        vs = [me.loops[t].vertex_index for t in tri]
        for c in range(3):
            pos[sl + (c,)][ins] = (l1 * co[vs[0], c] + l2 * co[vs[1], c] + l3 * co[vs[2], c])[ins]
            nrm[sl + (c,)][ins] = fn[c]
        # the triangle's own rates: its place (mm) and its body (mm) per texel along u and v
        Ti = np.linalg.inv(np.array([[xs[1] - xs[0], xs[2] - xs[0]], [ys[1] - ys[0], ys[2] - ys[0]]]))
        Jq = np.array([[pxs[1] - pxs[0], pxs[2] - pxs[0]], [pys[1] - pys[0], pys[2] - pys[0]]]) @ Ti
        Jx = (np.array([co[vs[1]] - co[vs[0]], co[vs[2]] - co[vs[0]]]).T * 1000.0) @ Ti
        for c, v in enumerate((Jq[0, 0], Jq[0, 1], Jq[1, 0], Jq[1, 1])):
            jq[sl + (c,)][ins] = v
        met[sl + (0,)][ins] = np.linalg.norm(Jx[:, 0])
        met[sl + (1,)][ins] = np.linalg.norm(Jx[:, 1])

# each piece's outline: the edges with one face, in the pattern (mm) and on the body
edge_faces = {}
for poly in me.polygons:
    for (a, b) in poly.edge_keys:
        edge_faces.setdefault((a, b), []).append(poly.index)
loop_of = {}
for poly in me.polygons:
    for t in poly.loop_indices:
        loop_of[(poly.index, me.loops[t].vertex_index)] = t
# (a welded mesh: a seam's edge has a face of each piece, and gives a segment to each, in that piece's own pattern; an
# open edge, the waist's top or a hem, gives one)
seg_piece, seg_a, seg_b, seg_pa, seg_pb, seg_other, seg_a_pat, seg_b_pat = [], [], [], [], [], [], [], []
for (a, b), fs in edge_faces.items():
    ks = [pattr[f].value for f in fs]
    if len(fs) == 2 and ks[0] == ks[1]:
        continue
    for f, k in zip(fs, ks):
        ta, tb = loop_of[(f, a)], loop_of[(f, b)]
        seg_piece.append(k)
        seg_other.append(next((kk for kk in ks if kk != k), -1))
        seg_a.append(tuple(place[ta]))
        seg_b.append(tuple(place[tb]))
        seg_a_pat.append(tuple(pp[ta]))
        seg_b_pat.append(tuple(pp[tb]))
        seg_pa.append(co[a])
        seg_pb.append(co[b])
np.savez_compressed(OUT, piece=piece, px=px, py=py, px_pat=px_pat, py_pat=py_pat, jq=jq, met=met, flat=np.array(FLAT),
                    pos=pos, nrm=nrm, seg_piece=np.array(seg_piece, dtype=np.int16),
                    seg_other=np.array(seg_other, dtype=np.int16),
                    seg_a=np.array(seg_a, dtype=np.float32), seg_b=np.array(seg_b, dtype=np.float32),
                    seg_a_pat=np.array(seg_a_pat, dtype=np.float32), seg_b_pat=np.array(seg_b_pat, dtype=np.float32),
                    seg_pa=np.array(seg_pa, dtype=np.float32), seg_pb=np.array(seg_pb, dtype=np.float32),
                    names=np.array([names.get(i, str(i)) for i in range(max(names) + 1 if names else int(piece.max()) + 1)]),
                    tex=np.array(TEX))
cover = float((piece >= 0).mean())
print("RASTER", json.dumps({"out": OUT, "tex": TEX, "cover": round(cover, 4), "segments": len(seg_piece), "flat": stats,
                            "pieces": {names.get(int(k), str(k)): int((piece == k).sum()) for k in np.unique(piece) if k >= 0}}))
