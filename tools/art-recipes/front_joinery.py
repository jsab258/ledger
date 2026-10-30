#!/usr/bin/env python3
"""A CLOUD SHOPFRONT'S PAINTED JOINERY MAPPED ONTO THE WOOD TRIM SHEET, WITH ITS EDGES DRAWN FOR THE CHIPPED-PAINT LAYER
(his order D11, the look; production/research/street-wear/MAFIA-WEAR-2026-10-28.md, section 5, the chandler's S2).

    python tools/art-recipes/front_joinery.py production/specs/shop-fronts/chandler-front-joinery.json
    python tools/art-recipes/front_joinery.py --selftest

WHY, 30 October 2026. Mafia's painted joinery is one master, paint over wood from a trim sheet, chipped to the wood at
its edges (the study, sections 1 and 2). A front made ready by tools/art-recipes/front_for_game.py and worn by
tools/art-recipes/front_wear.py carries one UV set, its paints' own unwrap, which the baked paint pictures need; the
trim sheet needs a second. So this reads the worn front's glb and, for each paint the spec names:
  * THE TRIM UV SET (TEXCOORD_2; TEXCOORD_1 a copy of the first, which Unreal's import may take for a generated
    lightmap: 30 October, the front imported with its lightmap written into UV 1, over the trim) onto
    tools/art-recipes/wood_trim.py's sheet, at the sheet's own 487.6 px/m: each
    loose part's grain runs along its longest side; each face is laid flat in its own plane, its width across the
    grain, in the BOARDS strip, or in the NARROW strip when the part is under narrow_m across, or in the END GRAIN strip
    when the face is cut across the grain (its normal within end_dot of the grain); each part at its own place along the
    strip (a seeded draw), so neighbours do not repeat one figure. The faces are unshared first (one vertex a corner),
    so a face never borrows a neighbour's place on the sheet.
    * THE CHIP PICTURE, on the paint's own first UV, mask_px square: R the bare wood's cover, G the worn rim's, B the edge
    term they come from, baked by the material's own law (chip_layer) at the trim sheet's chip noise, 2 by 2 within each
    texel. The edge term: the nearness of a convex arris (two faces meeting at more than sharp_deg; 1 at it, nothing at
    edge_m) shaped by Wood Mask Edge, times where knocks fall ("use": whole below full_below_m, down to "upper" from
    upper_from_m) times a broad 3D noise ("cluster", about size_m across), so some lengths of arris are chipped and
    others clean (the tea rooms' gate of 23 October: chips round every edge of a rail read as a dotted frame, not
    wear); or the door knob's nearness (the spec's handle points and the named handle materials' vertices, reach_m). Measured in the front's own metres from
    each texel's place on the model (its triangle's corners, by barycentric weights) to the nearest point of an edge
    sampled every 2 mm. Spread 16 px past each island, so the picture's smaller copies do not pull black in.
  * A paint whose first UV repeats (the fascia's lettering, "edges": "box") takes no picture: the material measures its
    edges from its own box (min and max written to the made file, in Unreal's centimetres and axes), weighted by its
    height's "use" and clustered by the trim sheet's broad noise (B) instead.
THE CHIP AMOUNT is set here, not guessed: the one ChipAmount that makes worn and bare paint target_seen of the
joinery's area as the street sees it (each face weighted by how squarely it faces out; the method's 3 to 10%), predicted texel by texel from the edge pictures and the trim
sheet's chip noise at their sheet places by the material's own law, found by halving, written to the made file.
Every other primitive is left as it was, its TEXCOORD_1 and TEXCOORD_2 its TEXCOORD_0. The glb goes beside the front's own on F:'s game
inputs as the spec's "out", the pictures beside it, and the made file (densities, the layer's predicted cover) to
production/specs/shop-fronts/<out>-made.json.

The layer's own law is chip_layer() here and make_paint_wood_master in tools/ue/make_kit_materials.py; the selftest holds
them to the same numbers.
"""
import json
import math
import os
import struct
import sys

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wood_trim  # noqa: E402

GAME_INPUTS = "F:/LedgerTools/game-inputs"
FRONTS_REL = "production/assets/shop-fronts"
SPECS = os.path.join(REPO, "production", "specs", "shop-fronts")
CT = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}
SAMPLE_M = 0.002
BLEED_PX = 16


# ---- glb in and out ------------------------------------------------------------------------------------------------

def read_glb(path):
    data = open(path, "rb").read()
    if data[:4] != b"glTF":
        raise SystemExit("front_joinery: %s is not a glb" % path)
    jlen = struct.unpack("<I", data[12:16])[0]
    j = json.loads(data[20:20 + jlen])
    blen = struct.unpack("<I", data[20 + jlen:24 + jlen])[0]
    return j, bytearray(data[28 + jlen:28 + jlen + blen])


def accessor(j, binbuf, i):
    a = j["accessors"][i]
    bv = j["bufferViews"][a["bufferView"]]
    n = NC[a["type"]]
    dt = np.dtype(CT[a["componentType"]])
    stride = bv.get("byteStride", 0) or dt.itemsize * n
    off = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    if stride == dt.itemsize * n:
        arr = np.frombuffer(bytes(binbuf), dtype=dt, count=a["count"] * n, offset=off).copy()
    else:
        raw = np.frombuffer(bytes(binbuf), dtype=np.uint8, count=stride * a["count"], offset=off).reshape(a["count"], stride)
        arr = raw[:, :dt.itemsize * n].copy().view(dt).ravel()
    return arr.reshape(a["count"], n) if n > 1 else arr


def append_accessor(j, binbuf, arr, gltf_type, target=None):
    """Appends one array to the BIN chunk as its own buffer view and accessor; returns the accessor's index."""
    arr = np.ascontiguousarray(arr)
    comp = {np.dtype(np.float32): 5126, np.dtype(np.uint32): 5125}[arr.dtype]
    while len(binbuf) % 4:
        binbuf.append(0)
    off = len(binbuf)
    binbuf.extend(arr.tobytes())
    bv = {"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes}
    if target:
        bv["target"] = target
    j["bufferViews"].append(bv)
    acc = {"bufferView": len(j["bufferViews"]) - 1, "componentType": comp, "count": int(arr.shape[0]), "type": gltf_type}
    if gltf_type == "VEC3" and comp == 5126:
        acc["min"] = [float(v) for v in arr.min(axis=0)]
        acc["max"] = [float(v) for v in arr.max(axis=0)]
    j["accessors"].append(acc)
    return len(j["accessors"]) - 1


def write_glb(path, j, binbuf):
    while len(binbuf) % 4:
        binbuf.append(0)
    j["buffers"][0]["byteLength"] = len(binbuf)
    body = json.dumps(j, separators=(",", ":")).encode("utf-8")
    body += b" " * ((4 - len(body) % 4) % 4)
    total = 12 + 8 + len(body) + 8 + len(binbuf)
    with open(path, "wb") as f:
        f.write(b"glTF" + struct.pack("<II", 2, total))
        f.write(struct.pack("<I", len(body)) + b"JSON" + body)
        f.write(struct.pack("<I", len(binbuf)) + b"BIN\x00" + bytes(binbuf))


# ---- the model's own shape -------------------------------------------------------------------------------------------

def weld(P, tol):
    """Each vertex's welded index (vertices within tol of each other share one), so faces split for their normals or
    their unwrap still meet."""
    key = np.round(np.asarray(P, dtype=np.float64) / tol).astype(np.int64)
    _, inv = np.unique(key, axis=0, return_inverse=True)
    return inv.ravel()


def face_normals(V):
    n = np.cross(V[:, 1] - V[:, 0], V[:, 2] - V[:, 0])
    a = np.linalg.norm(n, axis=1)
    return n / np.maximum(a, 1e-20)[:, None], 0.5 * a


def parts(T, nverts):
    """Loose parts: triangles joined through their welded vertices (a union by vertex)."""
    parent = np.arange(nverts)

    def find(x):
        r = x
        while parent[r] != r:
            r = parent[r]
        while parent[x] != r:
            parent[x], x = r, parent[x]
        return r
    for a, b, c in T:
        ra, rb, rc = find(a), find(b), find(c)
        parent[rb] = ra
        parent[find(rc)] = ra
    roots = np.array([find(t[0]) for t in T])
    _, label = np.unique(roots, return_inverse=True)
    return label.ravel()


def sharp_edges(T, Pw, N, sharp_deg):
    """Edges two faces share at more than sharp_deg: (convex [(a, b)], concave [(a, b)]) as welded vertex pairs."""
    edges = {}
    for f, t in enumerate(T):
        for k in range(3):
            a, b = int(t[k]), int(t[(k + 1) % 3])
            edges.setdefault((min(a, b), max(a, b)), []).append(f)
    cos_lim = math.cos(math.radians(sharp_deg))
    centroid = Pw[T].mean(axis=1)
    convex, concave = [], []
    for (a, b), fs in edges.items():
        if len(fs) != 2:
            continue
        f, g = fs
        if float(N[f] @ N[g]) > cos_lim:
            continue
        mid = 0.5 * (Pw[a] + Pw[b])
        # convex when the other face's middle lies behind this face's plane
        (convex if float(N[f] @ (centroid[g] - mid)) < 0.0 else concave).append((a, b))
    return convex, concave


def outer_arrises(pairs, Pw, part_of, boxes, nested, outer_m):
    """The arrises that chip: each member's outer ones, on its own bounds (both ends within outer_m of two of its box's
    sides: a door's perimeter, a pilaster's corners, a cornice's nose), and none on a member nested in another's bounds
    (a planted panel moulding, a console in its block). 30 October, the side door's square view: every panel's moulding
    chipped round, the dotted frame the tea rooms' gate of 23 October read as a plate, not wear."""
    keep = []
    for a, b in pairs:
        k = part_of[a]
        if nested[k]:
            continue
        lo, hi = boxes[k]
        ok = True
        for v in (Pw[a], Pw[b]):
            sides = int((np.abs(v - lo) < outer_m).sum() + (np.abs(hi - v) < outer_m).sum())
            ok &= sides >= 2
        if ok:
            keep.append((a, b))
    return keep


def part_boxes(V, label, tol):
    """Each loose part's bounds, and whether it lies inside a larger part's (within tol)."""
    n = label.max() + 1
    boxes = []
    for k in range(n):
        pts = V[label == k].reshape(-1, 3)
        boxes.append((pts.min(axis=0), pts.max(axis=0)))
    vol = [float(np.prod(np.maximum(hi - lo, 1e-4))) for lo, hi in boxes]
    nested = []
    for k, (lo, hi) in enumerate(boxes):
        nested.append(any(j != k and vol[j] > vol[k] and (boxes[j][0] - tol <= lo).all() and (hi <= boxes[j][1] + tol).all()
                          for j in range(n)))
    return boxes, nested


def edge_samples(Pw, pairs, step=SAMPLE_M):
    pts = []
    for a, b in pairs:
        p, q = Pw[a], Pw[b]
        n = max(1, int(math.ceil(np.linalg.norm(q - p) / step)))
        t = np.linspace(0.0, 1.0, n + 1)[:, None]
        pts.append(p[None, :] * (1 - t) + q[None, :] * t)
    return np.concatenate(pts) if pts else np.zeros((0, 3))


# ---- the second UV set -------------------------------------------------------------------------------------------------

def trim_uv(V, N, label, narrow_m, end_dot, seed=1990):
    """Per corner (F, 3, 2): the face laid flat on the trim sheet in metres / the sheet's size. V (F, 3, 3) the faces'
    corners, N (F, 3) their normals, label (F,) their loose part. Returns (uv, strip per face: 0 boards, 1 narrow, 2 end)."""
    rng = np.random.default_rng(seed)
    S = wood_trim.SHEET_M
    uv = np.zeros(V.shape[:2] + (2,))
    strip = np.zeros(len(V), dtype=int)
    for k in range(label.max() + 1):
        fs = np.nonzero(label == k)[0]
        pts = V[fs].reshape(-1, 3)
        lo, hi = pts.min(axis=0), pts.max(axis=0)
        ext = hi - lo
        order = np.argsort(ext)[::-1]
        g = np.eye(3)[order[0]]                   # the grain: the part's longest side
        c = 0.5 * (lo + hi)
        across = np.sort(ext)[1]                  # its width across the grain
        r_side = 0.5 * float(np.linalg.norm(ext[order[1:]]))
        r_end = 0.5 * float(np.linalg.norm(ext[order[1:]]))
        narrow = across < narrow_m
        side_strip = wood_trim.NARROW if narrow else wood_trim.BOARDS
        u_off = rng.random()
        room = (side_strip[1] - side_strip[0]) - 2 * r_side / S
        v_off = side_strip[0] + (rng.random() * room if room > 0 else 0.0) + r_side / S
        e_room = (wood_trim.END[1] - wood_trim.END[0]) - 2 * r_end / S
        e_off = wood_trim.END[0] + (rng.random() * e_room if e_room > 0 else 0.0) + r_end / S
        a1, a2 = np.eye(3)[order[1]], np.eye(3)[order[2]]
        for f in fs:
            n = N[f]
            if abs(float(n @ g)) > end_dot:
                # cut across the grain: laid on the end-grain strip by the part's other two sides
                q = V[f] - c
                uv[f, :, 0] = q @ a1 / S + u_off
                uv[f, :, 1] = q @ a2 / S + e_off
                strip[f] = 2
                continue
            # the grain in the face's own plane, and across it: laid flat, so the sheet's density holds on every face
            gp = g - (g @ n) * n
            gp /= max(np.linalg.norm(gp), 1e-12)
            t = np.cross(n, gp)
            q = V[f] - c
            uv[f, :, 0] = q @ gp / S + u_off
            uv[f, :, 1] = q @ t / S + v_off
            strip[f] = 1 if narrow else 0
    return uv, strip


def texel_density(V, uv, px=wood_trim.PX):
    """Per face: px per metre on the sheet (the square root of its sheet area over its own), and its own area."""
    _, a3 = face_normals(V)
    w = uv
    a2 = 0.5 * np.abs((w[:, 1, 0] - w[:, 0, 0]) * (w[:, 2, 1] - w[:, 0, 1]) - (w[:, 2, 0] - w[:, 0, 0]) * (w[:, 1, 1] - w[:, 0, 1]))
    ok = a3 > 1e-10
    return px * np.sqrt(a2[ok] / a3[ok]), a3[ok]


def weighted_percentile(x, w, q):
    o = np.argsort(x)
    cw = np.cumsum(w[o])
    return float(x[o][np.searchsorted(cw, q / 100.0 * cw[-1])])


# ---- the edge picture --------------------------------------------------------------------------------------------------

def rasterise(UV0, V, px, values_at):
    """Each texel of a px-square picture inside a face of the unwrap: its place on the model by barycentric weights.
    values_at(points (n, 3), faces (n,), bary (n, 3)) -> (n, c). Returns (picture (px, px, c), covered (px, px),
    per-texel face index (-1 none), per-texel barycentric weights)."""
    face = -np.ones((px, px), dtype=np.int32)
    bary = np.zeros((px, px, 3), dtype=np.float32)
    xy = UV0 * px - 0.5                         # pixel centres at integers; v runs down the picture (glTF)
    for f in range(len(V)):
        a, b, c = xy[f]
        x0, x1 = int(max(0, math.floor(min(a[0], b[0], c[0])))), int(min(px - 1, math.ceil(max(a[0], b[0], c[0]))))
        y0, y1 = int(max(0, math.floor(min(a[1], b[1], c[1])))), int(min(px - 1, math.ceil(max(a[1], b[1], c[1]))))
        if x1 < x0 or y1 < y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
        d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(d) < 1e-14:
            continue
        l1 = ((b[1] - c[1]) * (gx - c[0]) + (c[0] - b[0]) * (gy - c[1])) / d
        l2 = ((c[1] - a[1]) * (gx - c[0]) + (a[0] - c[0]) * (gy - c[1])) / d
        l3 = 1.0 - l1 - l2
        m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
        if not m.any():
            continue
        face[gy[m], gx[m]] = f
        bary[gy[m], gx[m]] = np.stack([l1[m], l2[m], l3[m]], axis=1)
    covered = face >= 0
    ys, xs = np.nonzero(covered)
    fs = face[ys, xs]
    bw = bary[ys, xs]
    pts = (V[fs] * bw[:, :, None].astype(np.float64)).sum(axis=1)
    vals = values_at(pts, fs, bw)
    pic = np.zeros((px, px, vals.shape[1]), dtype=np.float32)
    pic[ys, xs] = vals
    return pic, covered, face, bary


def bleed(pic, covered, px_out=BLEED_PX):
    from scipy import ndimage
    if covered.all():
        return pic
    dist, (iy, ix) = ndimage.distance_transform_edt(~covered, return_indices=True)
    out = pic[iy, ix]
    out[dist > px_out] = 0.0
    return out


# ---- where knocks fall --------------------------------------------------------------------------------------------------

def use_weight(height_m, use):
    """1 below full_below_m (feet, bins, bicycles, bags), straight down to `upper` at upper_from_m and above."""
    a, b, u = use["full_below_m"], use["upper_from_m"], use["upper"]
    return np.clip(1.0 - (np.asarray(height_m) - a) / (b - a) * (1.0 - u), u, 1.0)


def value_noise3(p, size_m, seed):
    """A smooth 3D value noise (0 to 1) of features about size_m across, from a seeded lattice."""
    rng = np.random.default_rng(seed)
    lat = rng.random((64, 64, 64))
    q = np.asarray(p, dtype=np.float64) / size_m + 1000.0
    i = np.floor(q).astype(np.int64)
    f = q - i
    f = f * f * (3.0 - 2.0 * f)
    out = np.zeros(len(q))
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (f[:, 0] if dx else 1 - f[:, 0]) * (f[:, 1] if dy else 1 - f[:, 1]) * (f[:, 2] if dz else 1 - f[:, 2])
                out += w * lat[(i[:, 0] + dx) % 64, (i[:, 1] + dy) % 64, (i[:, 2] + dz) % 64]
    return out


def cluster_weight(v, cluster):
    return np.clip((np.asarray(v) - cluster["from"]) * cluster["gain"], 0.0, 1.0)


# ---- the layer's law (the material's, in numbers) ----------------------------------------------------------------------

def edge_term(edge, weight, handle, k, law="gain"):
    """The layer's edge: the arris's nearness (0 to 1, 1 at it) shaped by Wood Mask Edge, times where knocks fall and
    the cluster (0 to 1); or the knob's nearness shaped the same, whichever is more. The shaping is inferred (Mafia's
    wiring is not readable): "gain" (30 October, try 2) multiplies the nearness by it and clamps, so the edge band is
    whole for its first edge_m / k and falls to nothing at edge_m; "power" (try 1) raised it to k, which left the
    arrises nearly bare of chips (1.0% of the square view's joinery against the 3 to 10% asked)."""
    def shape(v):
        v = np.clip(v, 0.0, 1.0)
        return np.clip(v * k, 0.0, 1.0) if law == "gain" else np.power(v, k)
    return np.maximum(shape(edge) * np.clip(weight, 0.0, 1.0), shape(handle))


def chip_layer(e, noise, layer):
    """Bare and worn (0 to 1) from the edge term (edge_term, 0 to 1) and the chip noise (0 to 1, even): bare where the
    noise passes 1 - ChipAmount x the term; the worn rim WornWidth times as wide."""
    e = np.clip(e, 0.0, 1.0)
    s = layer["ChipSharpness"]
    bare = np.clip((noise - (1.0 - layer["ChipAmount"] * e)) * s, 0.0, 1.0)
    worn = np.clip((noise - (1.0 - layer["ChipAmount"] * layer["WornWidth"] * e)) * s, 0.0, 1.0)
    return bare, np.clip(worn - bare, 0.0, 1.0)


def find_amount(pred, layer, target, lo=0.0, hi=1.0, steps=30):
    """The ChipAmount at which worn and bare paint cover `target` of the street-facing joinery (all paints by area)."""
    def cover(a):
        h = w_all = 0.0
        for _, e, n, w, seen, _ in pred:
            bare, worn = chip_layer(e, n, dict(layer, ChipAmount=a))
            h += float((w * seen)[(bare + worn) > 0.5].sum())
            w_all += float((w * seen).sum())
        return h / w_all
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if cover(mid) < target else (lo, mid)
    return 0.5 * (lo + hi)


def box_edge(p, lo, hi):
    """A point on a box's face: its distance to the face's nearest edge (the middle of its three distances to the box's
    sides, the smallest being the face it lies on)."""
    a = np.minimum(p - lo, hi - p)
    return a.sum(axis=-1) - a.min(axis=-1) - a.max(axis=-1)


def gltf_to_unreal_cm(p):
    """The front's glTF frame (x across, y up, z out, metres) to its Unreal mesh's own (cm): X = x, Y = z, Z = y."""
    p = np.asarray(p, dtype=np.float64)
    return np.stack([p[..., 0], p[..., 2], p[..., 1]], axis=-1) * 100.0


def sample_noise(noise, uv, tiling):
    px = noise.shape[0]
    x = np.mod(uv[:, 0] * tiling, 1.0) * px - 0.5
    y = np.mod(uv[:, 1] * tiling, 1.0) * px - 0.5
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = x - x0, y - y0
    g = lambda yy, xx: noise[np.mod(yy, px), np.mod(xx, px)]  # noqa: E731
    return ((1 - fx) * (1 - fy) * g(y0, x0) + fx * (1 - fy) * g(y0, x0 + 1) + (1 - fx) * fy * g(y0 + 1, x0)
            + fx * fy * g(y0 + 1, x0 + 1))


# ---- the front -------------------------------------------------------------------------------------------------------

def main(spec_path):
    t0 = __import__("time").time()
    from PIL import Image
    from scipy.spatial import cKDTree
    spec = json.load(open(spec_path, encoding="utf-8"))
    src = os.path.join(GAME_INPUTS, FRONTS_REL, spec["front"] + ".glb")
    out_dir = os.path.join(GAME_INPUTS, FRONTS_REL)
    j, binbuf = read_glb(src)
    mats = [m.get("name") for m in j["materials"]]
    layer = spec["layer"]
    masks = np.asarray(Image.open(os.path.join(GAME_INPUTS, wood_trim.REL, wood_trim.NAMES["masks"])).convert("RGB"),
                       dtype=np.float64) / 255.0
    chip_noise, dirt_noise = masks[..., 1], masks[..., 2]
    pred, bake = [], []
    # the knob: its points and its own vertices
    hand = [np.asarray(spec["handles"].get("points", []), dtype=np.float64).reshape(-1, 3)]
    for pr in j["meshes"][0]["primitives"]:
        if mats[pr["material"]] in spec["handles"].get("materials", []):
            hand.append(accessor(j, binbuf, pr["attributes"]["POSITION"]).astype(np.float64))
    hand = np.concatenate(hand)
    hand_tree = cKDTree(hand) if len(hand) else None
    made = {"front": spec["front"], "out": spec["out"], "paints": {}, "trim": {"px": wood_trim.PX, "sheet_m": wood_trim.SHEET_M,
            "density_px_m": round(wood_trim.DENSITY, 1)}, "layer": {k: v for k, v in layer.items() if k != "note"}}
    all_d, all_a = [], []
    for pr in j["meshes"][0]["primitives"]:
        name = mats[pr["material"]]
        at = pr["attributes"]
        if name not in spec["paints"]:
            at["TEXCOORD_1"] = at["TEXCOORD_0"]
            at["TEXCOORD_2"] = at["TEXCOORD_0"]
            continue
        cfg = spec["paints"][name]
        P = accessor(j, binbuf, at["POSITION"]).astype(np.float64)
        Nv = accessor(j, binbuf, at["NORMAL"]).astype(np.float64)
        UV = accessor(j, binbuf, at["TEXCOORD_0"]).astype(np.float64)
        I = accessor(j, binbuf, pr["indices"]).astype(np.int64).reshape(-1, 3)
        V = P[I]
        Nf, area = face_normals(V)
        keep = area > 1e-12
        I, V, Nf, area = I[keep], V[keep], Nf[keep], area[keep]
        w = weld(P, spec["weld_m"])
        T = w[I]
        Pw = np.zeros((w.max() + 1, 3))
        Pw[w] = P
        label = parts(T, w.max() + 1)
        uv1, strip = trim_uv(V, Nf, label, spec["narrow_m"], spec["end_dot"])
        dens, a3 = texel_density(V, uv1)
        all_d.append(dens)
        all_a.append(a3)
        row = {"faces": int(len(V)), "parts": int(label.max() + 1), "area_m2": round(float(area.sum()), 3),
               "strips_m2": {s: round(float(area[strip == k].sum()), 3) for k, s in enumerate(("boards", "narrow", "end"))},
               "density_px_m": {"p5": round(weighted_percentile(dens, a3, 5), 1), "median": round(weighted_percentile(dens, a3, 50), 1),
                                "p95": round(weighted_percentile(dens, a3, 95), 1)}}
        # the faces unshared (one vertex a corner, each with the face's own place on the sheet), then shared again
        # wherever two corners agree in every attribute, so a face's triangles meet as the model's did (30 October:
        # left one a corner, the front lit the alley's brick at night in Unreal, the old paints on it or ours)
        corners = I.ravel()
        rows = np.concatenate([P[corners], Nv[corners], UV[corners], uv1.reshape(-1, 2)], axis=1).astype(np.float32)
        uniq, inv = np.unique(rows, axis=0, return_inverse=True)
        row["vertices"] = {"model": int(len(P)), "corners": int(len(corners)), "written": int(len(uniq))}
        new = {"POSITION": append_accessor(j, binbuf, np.ascontiguousarray(uniq[:, 0:3]), "VEC3", 34962),
               "NORMAL": append_accessor(j, binbuf, np.ascontiguousarray(uniq[:, 3:6]), "VEC3", 34962),
               "TEXCOORD_0": append_accessor(j, binbuf, np.ascontiguousarray(uniq[:, 6:8]), "VEC2", 34962),
               "TEXCOORD_2": append_accessor(j, binbuf, np.ascontiguousarray(uniq[:, 8:10]), "VEC2", 34962)}
        new["TEXCOORD_1"] = new["TEXCOORD_0"]
        pr["attributes"] = new
        pr["indices"] = append_accessor(j, binbuf, inv.ravel().astype(np.uint32), "SCALAR", 34963)
        if cfg["edges"] == "box":
            lo, hi = P.min(axis=0), P.max(axis=0)
            ulo, uhi = gltf_to_unreal_cm(lo), gltf_to_unreal_cm(hi)
            row["box_cm"] = {"min": [round(float(v), 2) for v in np.minimum(ulo, uhi)], "max": [round(float(v), 2) for v in np.maximum(ulo, uhi)]}
            # the predicted cover on its own faces: each face's middle sampled on a grid of its plane is the material's
            # law at the box's edges (measured over its corners' sheet places)
            pts, ws, nz, uvs = [], [], [], []
            for f in range(len(V)):
                n_s = max(2, int(math.sqrt(area[f]) / 0.005))
                r1, r2 = np.meshgrid(np.linspace(0, 1, n_s), np.linspace(0, 1, n_s))
                m = (r1 + r2) <= 1.0
                b = np.stack([1 - r1[m] - r2[m], r1[m], r2[m]], axis=1)
                pts.append(b @ V[f])
                uvs.append(b @ uv1[f])
                ws.append(np.full(len(b), area[f] / len(b)))
                nz.append(np.full(len(b), Nf[f][2]))
            pts, ws, nz, uvs = np.concatenate(pts), np.concatenate(ws), np.concatenate(nz), np.concatenate(uvs)
            box_w = float(use_weight(0.5 * (lo[1] + hi[1]), spec["use"]))
            row["box_weight"] = round(box_w, 3)
            e = edge_term(np.clip(1.0 - box_edge(pts, lo, hi) / spec["edge_m"], 0.0, 1.0),
                          box_w * cluster_weight(sample_noise(dirt_noise, uvs, 1.0), spec["cluster"]), 0.0, layer["WoodMaskEdge"],
                          spec["edge_law"])
            n = sample_noise(chip_noise, uvs, layer["PaintCracksTiling"])
            pred.append((name, e, n, ws, np.clip(nz, 0.0, 1.0), None))
            made["paints"][name] = row
            continue
        # THE EDGE PICTURE
        convex, concave = sharp_edges(T, Pw, Nf, spec["sharp_deg"])
        boxes, nested = part_boxes(V, label, spec["nested_tol_m"])
        part_of = np.zeros(len(Pw), dtype=np.int64)
        part_of[T.ravel()] = np.repeat(label, 3)
        all_convex = len(convex)
        convex = outer_arrises(convex, Pw, part_of, boxes, nested, spec["outer_m"])
        row["nested_parts"] = int(sum(nested))
        row["convex_edges_all"] = all_convex
        ct = cKDTree(edge_samples(Pw, convex)) if convex else None
        it = cKDTree(edge_samples(Pw, concave)) if concave else None
        px = int(cfg["mask_px"])
        UVf = UV[I]

        def values_at(pts, fs, bw):
            # the arris's nearness, the knob's, where knocks fall times the cluster, inside corners; the texel's place
            # on the sheet, its share of the model's area, its face's facing
            out = np.zeros((len(pts), 9), dtype=np.float32)
            if ct is not None:
                out[:, 0] = np.clip(1.0 - ct.query(pts, distance_upper_bound=spec["edge_m"] * 1.01)[0] / spec["edge_m"], 0, 1)
            if hand_tree is not None:
                out[:, 1] = np.clip(1.0 - hand_tree.query(pts, distance_upper_bound=spec["handles"]["reach_m"] * 1.01)[0]
                                    / spec["handles"]["reach_m"], 0, 1)
            out[:, 2] = use_weight(pts[:, 1], spec["use"]) * cluster_weight(
                value_noise3(pts, spec["cluster"]["size_m"], spec["cluster"]["seed"]), spec["cluster"])
            if it is not None:
                out[:, 3] = np.clip(1.0 - it.query(pts, distance_upper_bound=spec["inside_m"] * 1.01)[0] / spec["inside_m"], 0, 1)
            uvt = (uv1[fs] * bw[:, :, None]).sum(axis=1)
            out[:, 4:6] = uvt
            out[:, 6] = area[fs]                                       # for the texel's share of the model's area
            out[:, 7] = Nf[fs][:, 2]
            return out
        pic, covered, face, _ = rasterise(UVf, V, px, values_at)
        # each texel's area on the model: its face's area over the texels its face covers
        counts = np.bincount(face[covered], minlength=len(V)).astype(np.float64)
        fc = face[covered]
        vals = pic[covered]
        tw = vals[:, 6] / np.maximum(counts[fc], 1.0)
        edge = edge_term(vals[:, 0], vals[:, 2], vals[:, 1], layer["WoodMaskEdge"], spec["edge_law"])
        near = np.maximum(vals[:, 0], vals[:, 1]) > 0.0
        uvc = vals[:, 4:6].astype(np.float64)
        row.update({"convex_edges": len(convex), "inside_edges": len(concave), "mask_px": px,
                    "within_reach_share": round(float(tw[near].sum() / tw.sum()), 4)})
        pred.append((name, edge, sample_noise(chip_noise, uvc, layer["PaintCracksTiling"]), tw, np.clip(vals[:, 7], 0.0, 1.0), near))
        # each face's sheet place against its own unwrap (d uv1 / d uv0), for the texel's corners below
        a0 = np.stack([UVf[:, 1] - UVf[:, 0], UVf[:, 2] - UVf[:, 0]], axis=2)
        a1 = np.stack([uv1[:, 1] - uv1[:, 0], uv1[:, 2] - uv1[:, 0]], axis=2)
        det = a0[:, 0, 0] * a0[:, 1, 1] - a0[:, 0, 1] * a0[:, 1, 0]
        inv = np.zeros_like(a0)
        okd = np.abs(det) > 1e-14
        inv[okd, 0, 0], inv[okd, 1, 1] = a0[okd, 1, 1] / det[okd], a0[okd, 0, 0] / det[okd]
        inv[okd, 0, 1], inv[okd, 1, 0] = -a0[okd, 0, 1] / det[okd], -a0[okd, 1, 0] / det[okd]
        jac = np.einsum("fij,fjk->fik", a1, inv)
        bake.append((name, row, px, covered, fc, uvc, jac, edge))
        # texels per edge_m at the picture's thinnest (the low faces are unwrapped denser, the high ones less)
        dpx = px * np.sqrt(np.bincount(fc, minlength=len(V)) / (px * px) / np.maximum(area, 1e-12))
        row["mask_px_per_m_p5"] = round(weighted_percentile(dpx[dpx > 0], area[dpx > 0], 5), 1)
        del pic, vals
        made["paints"][name] = row
    amount = find_amount(pred, layer, spec["target_seen"])
    layer = dict(layer, ChipAmount=round(amount, 4))
    made["layer"]["ChipAmount"] = layer["ChipAmount"]
    made["layer"]["chip_amount_from"] = "target_seen %.3f (front_joinery.py find_amount)" % spec["target_seen"]
    tot = {"all": [0.0, 0.0], "seen": [0.0, 0.0]}
    for name, e, n, w, seen, near in pred:
        bare, worn = chip_layer(e, n, layer)
        hit = (bare + worn) > 0.5
        r = made["paints"][name]
        r["predicted"] = {"worn_or_bare_all": round(float(w[hit].sum() / w.sum()), 4),
                          "worn_or_bare_seen": round(float((w * seen)[hit].sum() / (w * seen).sum()), 4),
                          "bare_all": round(float(w[bare > 0.5].sum() / w.sum()), 4)}
        if near is not None:
            r["predicted"]["outside_reach_texels"] = int((hit & ~near).sum())
        tot["all"][0] += float(w[hit].sum())
        tot["all"][1] += float(w.sum())
        tot["seen"][0] += float((w * seen)[hit].sum())
        tot["seen"][1] += float((w * seen).sum())
    made["predicted"] = {k: round(v[0] / v[1], 4) for k, v in tot.items()}
    # THE CHIPS BAKED AS COVERAGE (30 October, try 2): thresholded in the material, the chip noise lost its extremes in
    # its smaller copies, so chips thinned with distance (try 1: 1.0% of the square view's joinery at 7.4 m against 4.2%
    # predicted); baked here at the noise's own resolution, 2 by 2 within each texel, a smaller copy of the picture
    # averages chips and paint and keeps their area. R bare, G worn (the rim), B the edge term.
    for name, row, px, covered, fc, uvc, jac, edge in bake:
        cov = np.zeros((len(uvc), 2), dtype=np.float32)
        for dx, dy in ((-0.25, -0.25), (0.25, -0.25), (-0.25, 0.25), (0.25, 0.25)):
            d0 = np.array([dx, dy]) / px
            uvs = uvc + np.einsum("nij,j->ni", jac[fc], d0)
            b_, w_ = chip_layer(edge, sample_noise(chip_noise, uvs, layer["PaintCracksTiling"]), layer)
            cov[:, 0] += 0.25 * b_
            cov[:, 1] += 0.25 * w_
        pic = np.zeros((px, px, 3), dtype=np.float32)
        pic[covered] = np.stack([cov[:, 0], cov[:, 1], edge.astype(np.float32)], axis=1)
        rgb = bleed(pic, covered)
        name_png = "%s_%s_edges.png" % (spec["out"], name.replace("paint_", ""))
        Image.fromarray((rgb.clip(0, 1) * 255 + 0.5).astype(np.uint8), mode="RGB").save(os.path.join(out_dir, name_png))
        row["edges_png"] = name_png
        _, _, _, w, seen, _ = next(q for q in pred if q[0] == name)
        row["baked"] = {"bare_seen": round(float((w * seen * cov[:, 0]).sum() / (w * seen).sum()), 4),
                        "worn_seen": round(float((w * seen * cov[:, 1]).sum() / (w * seen).sum()), 4)}
        del pic, rgb, cov
    d, a = np.concatenate(all_d), np.concatenate(all_a)
    made["trim"]["measured_px_m"] = {"p5": round(weighted_percentile(d, a, 5), 1), "median": round(weighted_percentile(d, a, 50), 1),
                                     "p95": round(weighted_percentile(d, a, 95), 1)}
    made["trim"]["density_ok"] = bool(all(410.0 <= made["trim"]["measured_px_m"][k] <= 614.0 for k in ("p5", "median", "p95")))
    out = os.path.join(out_dir, spec["out"] + ".glb")
    write_glb(out, j, binbuf)
    made["glb"] = out
    made["seconds"] = round(__import__("time").time() - t0, 1)
    json.dump(made, open(os.path.join(SPECS, spec["out"] + "-made.json"), "w", encoding="utf-8"), indent=1)
    for name, r in made["paints"].items():
        print("frontJoinery %-22s faces=%d parts=%d area=%.2f m2 density p5/50/95 %s px/m predicted worn-or-bare %.1f%% "
              "(seen %.1f%%, bare %.1f%%)%s" % (name, r["faces"], r["parts"], r["area_m2"],
                                                "/".join(str(r["density_px_m"][k]) for k in ("p5", "median", "p95")),
                                                100 * r["predicted"]["worn_or_bare_all"], 100 * r["predicted"]["worn_or_bare_seen"],
                                                100 * r["predicted"]["bare_all"],
                                                (" edges %d convex, %d inside, %.0f%% of it within reach, %d texels outside"
                                                 % (r["convex_edges"], r["inside_edges"], 100 * r["within_reach_share"],
                                                    r["predicted"]["outside_reach_texels"])) if "convex_edges" in r else
                                                " (box, weight %.2f)" % r["box_weight"]))
    print("frontJoinery=%s glb=%s density %s px/m (512 within 20%%) ChipAmount %.4f predicted worn-or-bare %.1f%% of the "
          "street-facing joinery (%.1f%% of all) seconds=%.0f" % (
              "OK" if made["trim"]["density_ok"] else "FAIL", out, made["trim"]["measured_px_m"], layer["ChipAmount"],
              100 * made["predicted"]["seen"], 100 * made["predicted"]["all"], made["seconds"]))
    return 0 if made["trim"]["density_ok"] else 1


def selftest():
    ok = []
    # a unit box: 12 faces, 12 convex edges, none inside
    c = np.array([[x, y, z] for x in (0, 1) for y in (0, 1) for z in (0, 1)], dtype=float)
    quads = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    T = np.array([t for a, b, cc, d in quads for t in ((a, b, cc), (a, cc, d))])
    N, area = face_normals(c[T])
    cx, cc = sharp_edges(T, c, N, 35.0)
    ok.append(len(cx) == 12 and len(cc) == 0)
    lab = parts(T, 8)
    ok.append(lab.max() == 0)
    # a box's twelve arrises are all its outer ones; a small box inside a big one is nested and keeps none
    bx, ne = part_boxes(c[T], lab, 0.01)
    ok.append(len(outer_arrises(cx, c, np.zeros(8, dtype=int), bx, ne, 0.015)) == 12)
    small = c * 0.2 + 0.4
    both = np.concatenate([c[T], small[T]])
    lab2 = np.concatenate([np.zeros(12, dtype=int), np.ones(12, dtype=int)])
    ok.append(part_boxes(both, lab2, 0.01)[1] == [False, True])
    # a long bar: its grain along x, laid flat at the sheet's density on every face
    bar = c * np.array([2.0, 0.06, 0.05])
    uv, strip = trim_uv(bar[T], face_normals(bar[T])[0], np.zeros(len(T), dtype=int), 0.08, 0.75)
    dens, _ = texel_density(bar[T], uv)
    ok.append(np.allclose(dens, wood_trim.DENSITY, rtol=1e-6))
    ok.append(set(strip.tolist()) == {1, 2})          # 6 cm by 5 cm: a narrow member; its two ends end grain
    # the layer: nothing past the edge's reach, more at the arris than half way
    layer = {"WoodMaskEdge": 2.3, "ChipSharpness": 20.0, "ChipAmount": 0.45, "WornWidth": 1.6}
    n = np.linspace(0, 1, 10001)
    b0, w0 = chip_layer(np.zeros_like(n), n, layer)
    b1, w1 = chip_layer(np.ones_like(n), n, layer)
    bh, wh = chip_layer(np.full_like(n, 0.5), n, layer)
    ok.append(b0.max() == 0.0 and w0.max() == 0.0)
    # at the arris: bare where the noise passes 1 - 0.45 (less the half a sharpness step), worn or bare 1 - 0.72
    ok.append(abs(float((b1 > 0.5).mean()) - (0.45 - 0.5 / 20)) < 0.005 and (bh > 0.5).mean() < (b1 > 0.5).mean())
    ok.append(abs(float(((b1 + w1) > 0.5).mean()) - (0.72 - 0.5 / 20)) < 0.005)
    # the box edge: a point on a face's middle is half its narrow side from an edge
    ok.append(abs(float(box_edge(np.array([0.5, 0.3, 1.0]), np.zeros(3), np.array([1.0, 0.6, 1.0]))) - 0.3) < 1e-9)
    ok.append(np.allclose(gltf_to_unreal_cm([1.0, 2.0, 3.0]), [100.0, 300.0, 200.0]))
    use = {"full_below_m": 0.8, "upper_from_m": 1.8, "upper": 0.45}
    ok.append(np.allclose(use_weight([0.2, 1.3, 3.0], use), [1.0, 0.725, 0.45]))
    ok.append(np.allclose(edge_term(np.array([1.0, 0.6, 0.3]), 1.0, 0.0, 2.3, "gain"), [1.0, 1.0, 0.69])
              and np.allclose(edge_term(np.array([0.5]), 1.0, 0.0, 2.0, "power"), [0.25]))
    vn = value_noise3(np.random.default_rng(2).random((2000, 3)) * 3, 0.4, 1)
    ok.append(0.0 <= vn.min() and vn.max() <= 1.0 and 0.3 < vn.mean() < 0.7)
    pred = [("x", np.ones(20000), np.linspace(0, 1, 20000), np.ones(20000), np.ones(20000), None)]
    a = find_amount(pred, layer, 0.06)
    b, w = chip_layer(np.ones(20000), np.linspace(0, 1, 20000), dict(layer, ChipAmount=a))
    ok.append(abs(float(((b + w) > 0.5).mean()) - 0.06) < 0.002)
    # the rasteriser: a triangle over half a 32 px picture covers about half of it, each texel's place interpolated
    UVt = np.array([[[0, 0], [1, 0], [0, 1]]], dtype=float)
    Vt = np.array([[[0, 0, 0], [1, 0, 0], [0, 1, 0]]], dtype=float)
    pic, cov, _, _ = rasterise(UVt, Vt, 32, lambda p, f, b: p[:, :1])
    ok.append(0.45 < cov.mean() < 0.56 and abs(pic[0, 30, 0] - (30.5 / 32)) < 0.01)
    print("front_joinery selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv or len(sys.argv) < 2:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1]))
