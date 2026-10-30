"""PAINT A METAHUMAN BODY HIDDEN FACE MAP FROM THE GARMENTS THAT COVER IT (30 October 2026, Tom).

    blender -b --factory-startup -P tools/ue/blender_hidden_face_map.py -- BODY.fbx OUT_DIR
        --garment jacket=JACKET.fbx --garment jeans=JEANS.fbx --garment boots=BOOTS.fbx
        [--size 2048] [--cuff-mm 30] [--collar-mm 20] [--hem-mm 30] [--boot-mm 20]
        [--dg DG_MASK.png] [--reach-out-mm 150] [--reach-in-mm 30] [--island 40]

BODY.fbx is the whole body as the MetaHuman editor exports it (every face, LOD0 to LOD3, UV layer
"DiffuseUV"); each garment FBX is its skinned game file on the same skeleton, at rest.

WHAT THE MAP IS (the engine's rules, UE 5.8 MetaHuman plugin; HIDDEN-FACES-2026-10-30.md): painted on the
body's UVs, black (<= 0.1) cut, white (>= 0.9) kept; a triangle is cut only when every pixel it touches
is black (MetaHumanGeometryRemoval.cpp ShouldHideTriangle 342-402); pixel row = V * height with V the
engine's V, top down (GetHiddenFaceMapPixelForUV 333-340), which is 1 - Blender's v for an FBX the engine
wrote.

WHICH SKIN IS HIDDEN, at rest, per body point:
  - covered by a garment: a ray from the point along its normal meets that garment within --reach-out-mm,
    or one into the body meets it within --reach-in-mm (the skin standing outside the cloth), or five of
    eight rays 50 degrees off the normal meet it within --reach-out-mm (the crotch and the armpits, whose
    own rays slip out between two layers of cloth);
  - and clear of that garment's openings by the margins: the jacket's cuffs (--cuff-mm, measured up the
    forearm from the cuff's edge at the same angle round the arm) and its collar (--collar-mm, measured down
    the neck from the collar's top edge at the same angle round the neck); the jeans' hems (--hem-mm above
    each hem at its highest point, up the shin); the boots' collar (--boot-mm below the boot's top at the
    same angle round the shin; the boot is one closed shell, so its top is its highest point at each angle).
A face is hidden when its three points are; hidden islands under --island faces are given back and shown
islands under --island faces inside a hidden region are taken (stray rays at seams and the zip).

The map: white, every pixel a hidden face touches painted black, then the engine's own test run on every
LOD's triangles against it (and against the union with --dg, the default garment's map, which the build
adds); any shown face it would cut gets back a white pixel of its own, so no visible skin is cut.

OUT_DIR gets tom_body_hidden_faces.png (8-bit grey), map-record.json (margins, counts, predicted cuts per
LOD), hidden_vertices.json (LOD0 point indices hidden) and map-preview.png (the map over the UV layout).
"""
import json
import math
import os
import struct
import sys
import zlib
from collections import Counter, deque

import bmesh
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
BODY, OUT = argv[:2]


def opt(n, d, f=float):
    return f(argv[argv.index(n) + 1]) if n in argv else d


GARMENTS = {}
for i, a in enumerate(argv):
    if a == "--garment":
        k, v = argv[i + 1].split("=", 1)
        GARMENTS[k] = v
SIZE = opt("--size", 2048, int)
CUFF = opt("--cuff-mm", 30.0) / 1000.0
COLLAR = opt("--collar-mm", 20.0) / 1000.0
HEM = opt("--hem-mm", 30.0) / 1000.0
BOOT = opt("--boot-mm", 20.0) / 1000.0
REACH_OUT = opt("--reach-out-mm", 150.0) / 1000.0
REACH_IN = opt("--reach-in-mm", 30.0) / 1000.0
ISLAND = opt("--island", 40, int)
DG = opt("--dg", None, str)
CULL = 0.1
BINS = 36
os.makedirs(OUT, exist_ok=True)


def import_fbx(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    return next((o for o in new if o.type == "ARMATURE"), None), [o for o in new if o.type == "MESH"]


def world_bm(o):
    dg = bpy.context.evaluated_depsgraph_get()
    e = o.evaluated_get(dg)
    m = e.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(m)
    bm.transform(o.matrix_world)
    e.to_mesh_clear()
    bm.normal_update()
    return bm


bpy.ops.wm.read_factory_settings(use_empty=True)
arm, meshes = import_fbx(BODY)
lods = {}
for o in meshes:
    n = o.name.rsplit("_LOD", 1)
    lods[int(n[1]) if len(n) == 2 and n[1].isdigit() else 0] = o
body = lods[0]
bbm = world_bm(body)
bbm.verts.ensure_lookup_table()
bbm.faces.ensure_lookup_table()
NV = len(bbm.verts)
P = np.array([v.co[:] for v in bbm.verts])
N = np.array([v.normal[:] for v in bbm.verts])
groups = {g.index: g.name for g in body.vertex_groups}
dominant = []
for v in body.data.vertices:
    best = max(v.groups, key=lambda g: g.weight, default=None)
    dominant.append(groups[best.group] if best else "none")


def bone_head(name):
    return arm.matrix_world @ arm.data.bones[name].head_local


gar = {}
for k, path in GARMENTS.items():
    _a, ms = import_fbx(path)
    o = max(ms, key=lambda m: len(m.data.vertices))
    gbm = world_bm(o)
    tri = gbm.copy()
    bmesh.ops.triangulate(tri, faces=tri.faces[:])
    gar[k] = {"obj": o, "bm": gbm, "bvh": BVHTree.FromBMesh(tri), "path": path}
    tri.free()


def boundary_loops(bm):
    adj = {}
    for e in bm.edges:
        if e.is_boundary:
            a, b = e.verts
            adj.setdefault(a.index, set()).add(b.index)
            adj.setdefault(b.index, set()).add(a.index)
    seen, loops = set(), []
    for s in adj:
        if s in seen:
            continue
        stack, comp = [s], []
        while stack:
            v = stack.pop()
            if v in seen:
                continue
            seen.add(v)
            comp.append(v)
            stack.extend(adj[v] - seen)
        loops.append(comp)
    bm.verts.ensure_lookup_table()
    return [np.array([bm.verts[i].co[:] for i in c]) for c in loops]


def frame(a):
    a = a / np.linalg.norm(a)
    t = np.array([0.0, 0.0, 1.0]) if abs(a[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    u = np.cross(a, t)
    u /= np.linalg.norm(u)
    return a, u, np.cross(a, u)


class Opening:
    """An opening's edge, as depth into the garment along `axis` at each angle round it."""

    def __init__(self, name, pts, axis, centre, mode, margin, radius, side=0.0):
        self.name, self.margin, self.radius, self.mode, self.side = name, margin, radius, mode, side
        self.a, self.u, self.w = frame(np.asarray(axis, float))
        self.c = np.asarray(centre, float)
        d, th = self.depth_angle(pts)
        b = ((th + math.pi) / (2 * math.pi) * BINS).astype(int) % BINS
        edge = np.full(BINS, np.nan)
        for i in range(BINS):
            sel = d[b == i]
            if len(sel):
                # the rim at that angle: the deepest rim point (cuffs, collar), or the shallowest garment point
                # (a closed boot's top), or one level for all angles (a hem at its highest)
                edge[i] = sel.max() if mode == "rim" else sel.min()
        if mode == "highest":
            edge[:] = d.max()
        good = ~np.isnan(edge)
        if not good.all():
            idx = np.arange(BINS)
            edge = np.interp(idx, idx[good], edge[good], period=BINS)
        self.edge = edge
        self.span_mm = [round(1000 * float(edge.min()), 1), round(1000 * float(edge.max()), 1)]

    def depth_angle(self, pts):
        r = np.asarray(pts) - self.c
        return r @ self.a, np.arctan2(r @ self.w, r @ self.u)

    def clear(self, pts):
        """True where a point lies past the edge by the margin, or outside this opening's reach."""
        d, th = self.depth_angle(pts)
        b = ((th + math.pi) / (2 * math.pi) * BINS).astype(int) % BINS
        near = np.linalg.norm(np.asarray(pts) - self.c, axis=1) < self.radius
        if self.side:
            near &= np.sign(np.asarray(pts)[:, 0]) == np.sign(self.side)   # a limb's opening rules its own limb only
        return ~near | (d - self.edge[b] >= self.margin), d - self.edge[b]


openings = {k: [] for k in gar}
if "jacket" in gar:
    loops = boundary_loops(gar["jacket"]["bm"])
    collar = max(loops, key=lambda L: L[:, 2].mean())
    neck_axis = np.array(bone_head("neck_01") - bone_head("head"))
    openings["jacket"].append(Opening("collar", collar, neck_axis, collar.mean(0), "rim", COLLAR, 0.30))
    for s in ("l", "r"):
        wrist = np.array(bone_head("hand_" + s))
        cuff = min(loops, key=lambda L: np.linalg.norm(L.mean(0) - wrist))
        axis = np.array(bone_head("lowerarm_" + s)) - wrist
        openings["jacket"].append(Opening("cuff_" + s, cuff, axis, cuff.mean(0), "rim", CUFF, 0.30, side=wrist[0]))
if "jeans" in gar:
    loops = boundary_loops(gar["jeans"]["bm"])
    for s in ("l", "r"):
        ankle = np.array(bone_head("foot_" + s))
        hem = min(loops, key=lambda L: np.linalg.norm(L.mean(0) - ankle))
        axis = np.array(bone_head("calf_" + s)) - ankle
        openings["jeans"].append(Opening("hem_" + s, hem, axis, hem.mean(0), "highest", HEM, 0.40, side=ankle[0]))
if "boots" in gar:
    gp = np.array([v.co[:] for v in gar["boots"]["bm"].verts])
    for s in ("l", "r"):
        ankle = np.array(bone_head("foot_" + s))
        knee = np.array(bone_head("calf_" + s))
        side = gp[np.sign(gp[:, 0]) == np.sign(ankle[0])]
        top = side[side[:, 2] > side[:, 2].max() - 0.06]
        openings["boots"].append(Opening("boot_" + s, top, ankle - knee, top.mean(0), "top", BOOT, 0.45, side=ankle[0]))

# COVERAGE, per garment and point: the normal's ray out, a ray in, or most of a cone of eight rays 50 degrees
# off the normal (the crotch's skin faces down between two trouser legs and the armpit's into the sleeve's
# seam: its own ray slips out between them, the cone's meet the cloth on both sides)
eps = 1e-5
covered = {k: np.zeros(NV, bool) for k in gar}
through = {k: np.zeros(NV) for k in gar}
by_cone = {k: 0 for k in gar}
CONE = [(math.cos(math.radians(50)), math.sin(math.radians(50)) * math.cos(f), math.sin(math.radians(50)) * math.sin(f))
        for f in np.linspace(0, 2 * math.pi, 8, endpoint=False)]
for k, g in gar.items():
    bvh = g["bvh"]
    for i in range(NV):
        p = Vector(P[i])
        n = Vector(N[i])
        hit_out = bvh.ray_cast(p + n * eps, n, REACH_OUT)
        hit_in = bvh.ray_cast(p + n * eps, -n, REACH_IN)
        if hit_in[0] is not None:
            through[k][i] = hit_in[3]
        if hit_out[0] is not None or hit_in[0] is not None:
            covered[k][i] = True
            continue
        _a, uu, ww = frame(np.array(n))
        hits = 0
        for c0, c1, c2 in CONE:
            d = Vector(c0 * np.array(n) + c1 * uu + c2 * ww)
            if bvh.ray_cast(p + n * eps, d, REACH_OUT)[0] is not None:
                hits += 1
        if hits >= 5:
            covered[k][i] = True
            by_cone[k] += 1

hidden_by = {}
clearance = {}
for k in gar:
    ok = covered[k].copy()
    for op in openings[k]:
        c, d = op.clear(P)
        ok &= c
        clearance[op.name] = d
    hidden_by[k] = ok
hidden_v = np.zeros(NV, bool)
for k in gar:
    hidden_v |= hidden_by[k]

# FACES: hidden when all three points are; small islands cleaned
F = np.array([[v.index for v in f.verts] for f in bbm.faces])
hid_f = hidden_v[F].all(1)
nbr = [[] for _ in range(len(F))]
edge_faces = {}
for fi, f in enumerate(bbm.faces):
    for e in f.edges:
        edge_faces.setdefault(e.index, []).append(fi)
for fl in edge_faces.values():
    for a in fl:
        for b in fl:
            if a != b:
                nbr[a].append(b)


def islands(mask):
    seen = np.zeros(len(mask), bool)
    out = []
    for s in np.nonzero(mask)[0]:
        if seen[s]:
            continue
        q, comp = deque([s]), []
        seen[s] = True
        while q:
            f = q.popleft()
            comp.append(f)
            for g in nbr[f]:
                if mask[g] and not seen[g]:
                    seen[g] = True
                    q.append(g)
        out.append(comp)
    return out


given_back = taken = 0
for comp in islands(hid_f):
    if len(comp) < ISLAND:
        hid_f[comp] = False
        given_back += len(comp)
for comp in islands(~hid_f):
    if len(comp) < ISLAND:
        # only a shown island wholly inside hidden faces is taken
        cs = set(comp)
        if all(hid_f[g] for f in comp for g in nbr[f] if g not in cs):
            hid_f[comp] = True
            taken += len(comp)

# THE MAP
uv_layer = bbm.loops.layers.uv.active


def face_uvs(bm_):
    lay = bm_.loops.layers.uv.active
    return np.array([[l[lay].uv[:] for l in f.loops] for f in bm_.faces])


UV0 = face_uvs(bbm)                        # Blender's u, v
ENG0 = np.stack([UV0[..., 0], 1.0 - UV0[..., 1]], -1)   # the engine's U, V
W = H = SIZE
img = np.full((H, W), 255, np.uint8)




# THE ENGINE'S OWN TEST (MetaHumanGeometryRemoval.cpp 232-402), ported line for line
def wrap(x, lo, hi):
    size = hi - lo
    while x < lo:
        x += size
    while x > hi:
        x -= size
    return x


def rnd(x):
    return int(math.floor(x + 0.5))


def seg(a0, a1, b0, b1):
    va, vb = a1 - a0, b1 - b0
    den = -vb[0] * va[1] + va[0] * vb[1]
    if den == 0:
        return False
    s = (-va[1] * (a0[0] - b0[0]) + va[0] * (a0[1] - b0[1])) / den
    t = (vb[0] * (a0[1] - b0[1]) - vb[1] * (a0[0] - b0[0])) / den
    return 0 <= s <= 1 and 0 <= t <= 1


def intersect(tri, bmin, bmax):
    tmin, tmax = tri.min(0), tri.max(0)
    if rnd(tmin[0]) >= rnd(bmax[0]) or rnd(bmin[0]) >= rnd(tmax[0]):
        return False
    if rnd(tmin[1]) >= rnd(bmax[1]) or rnd(bmin[1]) >= rnd(tmax[1]):
        return False
    for p in tri:
        if rnd(bmin[0]) <= rnd(p[0]) <= rnd(bmax[0]) and rnd(bmin[1]) <= rnd(p[1]) <= rnd(bmax[1]):
            return True
    ext = 2.0 * np.linalg.norm(bmax - bmin) + 2.0 * np.linalg.norm(tmax - tmin)

    def inside(pt):
        far = pt + np.array([ext, ext])
        return sum(seg(tri[i], tri[(i + 1) % 3], pt, far) for i in range(3)) == 1
    for c in (bmin, bmax, np.array([bmin[0], bmax[1]]), np.array([bmax[0], bmin[1]])):
        if inside(c):
            return True
    edges = [(bmin, np.array([bmin[0], bmax[1]])), (bmax, np.array([bmin[0], bmax[1]])),
             (bmax, np.array([bmax[0], bmin[1]])), (bmin, np.array([bmax[0], bmin[1]]))]
    for i in range(3):
        for e0, e1 in edges:
            if seg(tri[i], tri[(i + 1) % 3], e0, e1):
                return True
    return False


def engine_px(t):
    """A triangle's corners in the engine's pixels (its UVs plus KINDA_SMALL_NUMBER, floored, wrapped), and its box."""
    px = np.array([[math.floor(wrap(u * W, 0.0, W - 1.0)), math.floor(wrap(v * H, 0.0, H - 1.0))] for u, v in t + 1e-4], float)
    return px, px.min(0).astype(int), px.max(0).astype(int)


def own_pixel(t):
    """A pixel the engine counts as touching this triangle: white there keeps it."""
    px, mn, mx = engine_px(t)
    if mn[0] == mx[0] or mn[1] == mx[1]:
        return int(mn[0]), int(mn[1])
    for y in range(mn[1], mx[1] + 1):
        for x in range(mn[0], mx[0] + 1):
            if intersect(px, np.array([x, y], float), np.array([x + 1, y + 1], float)):
                return x, y
    return int(mn[0]), int(mn[1])


def engine_hides(eng_uvs, im):
    """Per triangle (engine U, V), True when the build would cut it against image im (0..1 floats, rows = V)."""
    h, w = im.shape
    out = np.zeros(len(eng_uvs), bool)
    first = [None] * len(eng_uvs)
    for k, t in enumerate(eng_uvs + 1e-4):
        px = np.array([[math.floor(wrap(u * w, 0.0, w - 1.0)), math.floor(wrap(v * h, 0.0, h - 1.0))] for u, v in t], float)
        mn, mx = px.min(0).astype(int), px.max(0).astype(int)
        if mn[0] == mx[0] or mn[1] == mx[1]:
            out[k] = im[mn[1], mn[0]] <= CULL
            first[k] = (mn[0], mn[1])
            continue
        hide = True
        wy, wx = np.nonzero(im[mn[1]:mx[1] + 1, mn[0]:mx[0] + 1] > CULL)   # only the white pixels can keep it
        for y, x in zip(wy + mn[1], wx + mn[0]):
            if intersect(px, np.array([x, y], float), np.array([x + 1, y + 1], float)):
                hide = False
                break
        out[k] = hide
        first[k] = (int(px[0][0]), int(px[0][1]))
    return out, first


def touching(px, mn, mx):
    """The pixels of a triangle's box that touch it, as the engine counts (its rounded box test keeps columns
    mn..mx-1 and rows mn..mx-1; then closed overlap, here by separating axes, a superset at worst)."""
    xs, ys = np.meshgrid(np.arange(mn[0], mx[0]), np.arange(mn[1], mx[1]))
    xs, ys = xs.ravel(), ys.ravel()
    keep = np.ones(len(xs), bool)
    corners = [(0, 0), (1, 0), (0, 1), (1, 1)]
    for i in range(3):
        a, b, c = px[i], px[(i + 1) % 3], px[(i + 2) % 3]
        n = np.array([b[1] - a[1], a[0] - b[0]])
        t0, t1 = sorted((float(n @ a), float(n @ c)))
        proj = np.stack([(xs + cx) * n[0] + (ys + cy) * n[1] for cx, cy in corners])
        keep &= ~((proj.max(0) < t0) | (proj.min(0) > t1))
    return xs[keep], ys[keep]


def paint_engine(tris_eng, value):
    """Every pixel the engine's test counts as touching each triangle, set to value: black there cuts it."""
    for t in tris_eng:
        px, mn, mx = engine_px(t)
        if mn[0] == mx[0] or mn[1] == mx[1]:
            img[mn[1]:mx[1] + 1, mn[0]:mx[0] + 1] = value
            continue
        xs, ys = touching(px, mn, mx)
        img[ys, xs] = value


# THE BODY'S UVS SIT IN THE SECOND TILE (u 1.01 to 1.99, the UDIM 1002 layout): the engine wraps them by
# FMath::Wrap(U * Res, 0, Res - 1) (ShouldHideTriangle 362-364), a period of Res - 1, so u maps to pixel
# u * Res - (Res - 1), one pixel right of (u - 1) * Res; engine_px does the same.
paint_engine(ENG0[hid_f], 0)

# Shown faces the test would cut get a white pixel of their own, up to three rounds
fixed = 0
for _round in range(3):
    pred, first = engine_hides(ENG0, img / 255.0)
    bad = np.nonzero(pred & ~hid_f)[0]
    if not len(bad):
        break
    for k in bad:
        x, y = own_pixel(ENG0[k])
        img[y, x] = 255
        fixed += 1
pred0, _ = engine_hides(ENG0, img / 255.0)


def write_png_grey(path, a):
    raw = b"".join(b"\x00" + row.tobytes() for row in a)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", a.shape[1], a.shape[0], 8, 0, 0, 0, 0))
                 + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def read_png(path):
    im = bpy.data.images.load(path)
    im.colorspace_settings.name = "Non-Color"
    w, h = im.size
    px = np.array(im.pixels[:], np.float32).reshape(h, w, 4)[::-1]   # top row first
    return px[..., :3].max(-1)


map_path = os.path.join(OUT, "tom_body_hidden_faces.png")
write_png_grey(map_path, img)

record = {"body": BODY, "garments": GARMENTS, "size": SIZE, "uv": "engine V = 1 - Blender v",
          "margins_mm": {"cuff": CUFF * 1000, "collar": COLLAR * 1000, "jeans_hem_above_highest": HEM * 1000, "boot_collar": BOOT * 1000},
          "reach_mm": {"out": REACH_OUT * 1000, "in": REACH_IN * 1000}, "island_faces": ISLAND,
          "openings": {op.name: {"edge_depth_mm": op.span_mm, "centre": [round(c, 4) for c in op.c], "mode": op.mode}
                       for k in openings for op in openings[k]},
          "points": NV, "faces": len(F),
          "covered_points": {k: int(covered[k].sum()) for k in gar}, "covered_by_cone_only": by_cone,
          "hidden_points_by": {k: int(hidden_by[k].sum()) for k in gar},
          "hidden_points": int(hidden_v.sum()),
          "hidden_faces_lod0": int(hid_f.sum()), "islands_given_back": given_back, "islands_taken": taken,
          "shown_faces_given_a_white_pixel": fixed,
          "predicted_cut_lod0": int(pred0.sum()), "predicted_cut_but_meant_shown": int((pred0 & ~hid_f).sum()),
          "predicted_kept_but_meant_hidden": int((~pred0 & hid_f).sum()),
          "hidden_by_region": Counter(dominant[i] for i in np.nonzero(hidden_v)[0]).most_common(40),
          "black_pixels": int((img <= 25).sum())}

# The other LODs against the same map, and the union with the default garment's map
preds = {0: pred0}
for L in sorted(lods):
    if L == 0:
        continue
    lb = world_bm(lods[L])
    lb.faces.ensure_lookup_table()
    preds[L], _ = engine_hides(np.stack([face_uvs(lb)[..., 0], 1.0 - face_uvs(lb)[..., 1]], -1), img / 255.0)
    record.setdefault("lods", {})[L] = {"faces": len(lb.faces), "predicted_cut": int(preds[L].sum())}
    lb.free()
record.setdefault("lods", {})[0] = {"faces": len(F), "predicted_cut": int(pred0.sum())}
if DG and os.path.exists(DG):
    dg = read_png(DG)
    record["dg_size"] = list(dg.shape)
    # The convention check: the default garment's own map, read at each LOD0 point's UV both ways
    pv = np.array([bbm.verts[i].link_loops[0][uv_layer].uv[:] if bbm.verts[i].link_loops else (0.0, 0.0) for i in range(NV)])
    dh, dw = dg.shape
    for name, vv in (("engine_v_is_1_minus_blender_v", 1.0 - pv[:, 1]), ("engine_v_is_blender_v", pv[:, 1])):
        xs = np.array([math.floor(wrap(u * dw, 0.0, dw - 1.0)) for u in pv[:, 0] + 1e-4], int)
        ys = np.array([math.floor(wrap(v * dh, 0.0, dh - 1.0)) for v in vv + 1e-4], int)
        cut = dg[ys, xs] <= CULL
        record.setdefault("dg_check", {})[name] = {
            "points_cut": int(cut.sum()), "cut_z_m": [round(float(P[cut, 2].min()), 3), round(float(P[cut, 2].max()), 3)] if cut.any() else None,
            "cut_regions": Counter(dominant[i] for i in np.nonzero(cut)[0]).most_common(8),
            "cut_inside_ours": round(float((cut & hidden_v).sum()) / max(1, int(cut.sum())), 3)}
    # the build's union: the lowest value wins, on the larger of the two sizes (MetaHumanGeometryRemoval.cpp 22-182)
    S = max(dh, H)
    yy = ((np.arange(S) + 0.5) / S)
    a = (img / 255.0)[(yy * H).astype(int)][:, (yy * W).astype(int)]
    b = dg[(yy * dh).astype(int)][:, (yy * dw).astype(int)]
    union = np.minimum(np.where(a >= CULL, 1.0, 0.0), np.where(b >= CULL, 1.0, 0.0))
    pu, _ = engine_hides(ENG0, union)
    record["union_with_default_garment"] = {"size": S, "predicted_cut_lod0": int(pu.sum()),
                                            "cut_but_meant_shown": int((pu & ~hid_f).sum())}
    for L in sorted(lods):
        if L == 0:
            continue
        lb = world_bm(lods[L])
        pl, _ = engine_hides(np.stack([face_uvs(lb)[..., 0], 1.0 - face_uvs(lb)[..., 1]], -1), union)
        record["union_with_default_garment"]["predicted_cut_lod%d" % L] = int(pl.sum())
        lb.free()

with open(os.path.join(OUT, "map-record.json"), "w", encoding="utf-8") as fh:
    json.dump(record, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
with open(os.path.join(OUT, "hidden_vertices.json"), "w", encoding="utf-8") as fh:
    json.dump({"lod0_points_hidden": [int(i) for i in np.nonzero(hidden_v)[0]],
               "lod0_faces_hidden": [int(i) for i in np.nonzero(hid_f)[0]],
               "through_mm_rest": {k: {int(i): round(1000 * float(through[k][i]), 1) for i in np.nonzero(through[k] > 0.001)[0]} for k in gar}}, fh)

# PREVIEW: the map at 1024 with the UV layout's edges drawn grey
pv_img = np.repeat(np.repeat(img[::2, ::2, None], 3, 2), 1, 0).astype(np.uint8)
for t in ENG0:
    t = np.array([[wrap(u * W, 0.0, W - 1.0) / 2, wrap(v * H, 0.0, H - 1.0) / 2] for u, v in t])
    for i in range(3):
        a0, a1 = t[i], t[(i + 1) % 3]
        n = int(max(abs(a1 - a0)) + 1)
        for s in np.linspace(0, 1, n):
            x, y = (a0 + (a1 - a0) * s)
            xi, yi = int(min(W // 2 - 1, x)), int(min(H // 2 - 1, y))
            pv_img[yi, xi] = (150, 150, 150) if img[min(H - 1, yi * 2), min(W - 1, xi * 2)] > 127 else (110, 40, 40)
prev = bpy.data.images.new("preview", W // 2, H // 2, alpha=False)
rgba = np.concatenate([pv_img[::-1].astype(np.float32) / 255.0, np.ones((H // 2, W // 2, 1), np.float32)], 2)
prev.pixels.foreach_set(rgba.ravel())
prev.filepath_raw = os.path.join(OUT, "map-preview.png")
prev.file_format = "PNG"
prev.save()
print("HIDDEN_FACE_MAP " + json.dumps({k: record[k] for k in ("hidden_points", "hidden_faces_lod0", "predicted_cut_lod0",
                                                               "predicted_cut_but_meant_shown", "predicted_kept_but_meant_hidden", "lods")}), flush=True)
