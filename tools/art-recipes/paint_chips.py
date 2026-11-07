#!/usr/bin/env python3
"""WORN PAINT AT THE EDGES OF MICKEY'S FRONT, AS SMALL FLAKES OF GEOMETRY (n02-9-front-edge-wear, 7 November 2026).

    python tools/art-recipes/paint_chips.py GLB SIDECAR     # add the two rows to an exported street
    python tools/art-recipes/paint_chips.py --selftest

WHY, Mafia's painted joinery is chipped to the wood at its edges, 3 to 10% of the area, all within 5 cm of an edge or a
handle (production/research/street-wear/MAFIA-WEAR-2026-10-28.md, S2). Its way is a mask in the material; the street's
shared joinery meshes carry no edge mask, and a rebuilt front mesh lit the chandler's pier at night, cause never found
(DECISIONS 30 Oct 17:33, 18:29), so that route stays closed. Projected marks on this paint land on nothing or streak
(street_wear.py, 7 October). So the front's own convex arrises are read from the exported model and small irregular
flakes are laid over them, half a millimetre proud: the passed meshes are not touched, nothing needs a new material,
picture or UV set, and taking the two rows out takes the wear out.

Each flake folds over its arris, its body on the member's face. Only outer arrises (chips on every moulding read
as a dotted frame: the tea rooms' gate, 23 October): one face wide enough to be a member, not a moulding's facet, at
least one facing the street. Knocks fall low (whole below USE_FULL_M, thinning above) and in clusters, so some lengths
stay clean. Flakes are added until they cover TARGET_COVER of the joinery's area as the street sees it.

Runs at the end of terrace-front.py's --export-glb (Blender's numpy) so a re-export keeps them; alone, it refuses a
street that already has them. All numbers seeded: the same model gives the same flakes.
"""
import json
import math
import os
import random
import struct
import sys

import numpy as np

#: The front's box in the exported model's metres, and the rows that are its painted joinery.
BOX_LO, BOX_HI = np.array([2.9, 0.0, 4.7]), np.array([9.1, 3.6, 5.3])
JOINERY = ("street_frame_painted", "street_fascia_slate_blue", "street_mickeys_frame_painted")
SEED = 19900
TARGET_COVER = 0.035        # the method's 3 to 10%; the low end, read on dark paint
PROUD_M = 0.0005
MIN_FACE_M, MIN_EDGE_M = 0.015, 0.08
USE_FULL_M, USE_TOP = 1.3, 0.3
#: Earlier coats and primer; bare wood, about one flake in three. Linear colours, the joinery's own paint is about 0.09.
ROWS = (("street_paint_chip_primer", "paint_chip_primer", [0.30, 0.29, 0.25], 0.8, 0.68),
        ("street_paint_chip_wood", "paint_chip_wood", [0.11, 0.075, 0.05], 0.85, 0.32))
_CT = {5126: "f4", 5125: "u4", 5123: "u2", 5121: "u1"}
_NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}


def read_glb(path):
    with open(path, "rb") as f:
        f.read(12)
        n = struct.unpack("<I", f.read(4))[0]
        f.read(4)
        j = json.loads(f.read(n))
        n2 = struct.unpack("<I", f.read(4))[0]
        f.read(4)
        return j, bytearray(f.read(n2))


def write_glb(path, j, b):
    while len(b) % 4:
        b.append(0)
    j["buffers"][0]["byteLength"] = len(b)
    t = json.dumps(j, separators=(",", ":")).encode("utf-8")
    t += b" " * ((4 - len(t) % 4) % 4)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(t) + 8 + len(b)))
        f.write(struct.pack("<I", len(t)) + b"JSON" + t)
        f.write(struct.pack("<I", len(b)) + b"BIN\0" + bytes(b))
    os.replace(tmp, path)


def _acc(j, b, i):
    a = j["accessors"][i]
    v = j["bufferViews"][a["bufferView"]]
    start = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    return np.frombuffer(b, _CT[a["componentType"]], a["count"] * _NC[a["type"]], start).reshape(a["count"], -1)


def triangles(j, b, names):
    out = []
    for nd in j["nodes"]:
        if nd.get("name") in names and "mesh" in nd:
            for pr in j["meshes"][nd["mesh"]]["primitives"]:
                pos = _acc(j, b, pr["attributes"]["POSITION"]).astype(float)
                idx = _acc(j, b, pr["indices"]).reshape(-1, 3)
                t = pos[idx]
                c = t.mean(1)
                out.append(t[np.all((c > BOX_LO) & (c < BOX_HI), 1)])
    return np.concatenate(out) if out else np.zeros((0, 3, 3))


def arrises(tris):
    """Convex edges between two faces: (a, b, n1, n2, w1, w2), n the faces' normals, w the room across each face;
    and the area of the joinery as the street sees it (street on the -z side)."""
    edges = {}
    seen = 0.0
    normals = []
    for k, t in enumerate(tris):
        n = np.cross(t[1] - t[0], t[2] - t[0])
        a = np.linalg.norm(n)
        n = n / a if a > 1e-12 else n
        normals.append(n)
        seen += 0.5 * a * max(0.0, -n[2])
        for i in range(3):
            p, q = t[i], t[(i + 1) % 3]
            key = tuple(sorted((tuple(np.round(p, 4)), tuple(np.round(q, 4)))))
            edges.setdefault(key, []).append(k)
    out = []
    for key, ks in edges.items():
        if len(ks) != 2:
            continue
        p, q = np.array(key[0]), np.array(key[1])
        ln = np.linalg.norm(q - p)
        if ln < MIN_EDGE_M:
            continue
        n1, n2 = normals[ks[0]], normals[ks[1]]
        if np.dot(n1, n2) > 0.95:   # the same face's diagonal; a 45-degree bevel between two faces counts (the street's joinery is bevelled 3 mm)
            continue
        if max(-n1[2], -n2[2]) < 0.5:   # neither face turned to the street
            continue
        c1, c2 = tris[ks[0]].mean(0), tris[ks[1]].mean(0)
        if np.dot(c2 - c1, n1) > 1e-6:  # concave
            continue

        def room(t, n):
            u = (q - p) / ln
            return max(np.linalg.norm(np.cross(v - p, u)) for v in t)
        w1, w2 = room(tris[ks[0]], n1), room(tris[ks[1]], n2)
        if max(w1, w2) < MIN_FACE_M:
            continue
        out.append((p, q, n1, n2, w1, w2))
    out.sort(key=lambda e: tuple(e[0]) + tuple(e[1]))
    return out, seen


def _cluster(p, s):
    """A broad noise, about 40 cm across, so some lengths are chipped and others clean."""
    return (math.sin(p[0] * 7.3 + s) + math.sin(p[1] * 5.9 + s * 2.1) + math.sin((p[0] + p[1]) * 3.7 + s * 0.7) +
            math.sin(p[2] * 11.0 + s * 1.3)) / 4.0


def _use(y):
    return 1.0 if y < USE_FULL_M else max(USE_TOP, 1.0 - (y - USE_FULL_M) * 0.45)


def flake(r, e):
    """One flake on one arris: its triangles (world, n), its seen area, or None when the arris says no here."""
    p, q, n1, n2, w1, w2 = e
    ln = np.linalg.norm(q - p)
    u = (q - p) / ln
    at = r.random() * ln
    c = p + u * at
    if r.random() > _use(c[1]) or _cluster(c, 1.7) < -0.02:
        return None
    long_m = min(0.07, max(0.004, r.lognormvariate(math.log(0.026), 0.7)))
    a0, a1 = max(0.0, at - long_m / 2), min(ln, at + long_m / 2)
    if a1 - a0 < 0.003:
        return None
    if w1 < w2:   # the flake's body on the member's face, its fold over the bevel
        n1, n2, w1, w2 = n2, n1, w2, w1
    tris, seen = [], 0.0
    for n, w, wide in ((n1, w1, 1.0), (n2, w2, 0.45)):
        across = np.cross(n, u)
        # the face runs away from the arris, against the other face's normal
        other = n2 if n is n1 else n1
        if np.dot(across, other) > 0:
            across = -across
        width = min(0.9 * w, 0.025, max(0.002, r.lognormvariate(math.log(0.009), 0.6)) * wide)
        n_pts = 3
        ring = [(a0 + (a1 - a0) * k / (n_pts - 1), 0.0) for k in range(n_pts)]
        top = []
        for k in range(n_pts):
            f = k / (n_pts - 1)
            bulge = math.sin(f * math.pi) ** 0.7
            top.append((a0 + (a1 - a0) * (f + r.uniform(-0.08, 0.08)), width * bulge * r.uniform(0.55, 1.0)))
        pts = ring + top[::-1][1:-1]
        world = [p + u * a + across * d + n * PROUD_M for a, d in pts]
        centre = sum(world) / len(world)
        for k in range(len(world)):
            a, b = world[k], world[(k + 1) % len(world)]
            tn = np.cross(a - centre, b - centre)
            if np.dot(tn, n) < 0:
                a, b = b, a
                tn = -tn
            tris.append((centre.copy(), a.copy(), b.copy()))
            seen += 0.5 * np.linalg.norm(tn) * max(0.0, -n[2])
    return tris, seen


def make_flakes(tris, seed=SEED, target=TARGET_COVER):
    """{row index: [triangles]}, the seen cover reached, the number of flakes, of arrises."""
    es, seen_all = arrises(tris)
    r = random.Random(seed)
    if not es:
        return {0: [], 1: []}, 0.0, 0, 0
    weights = [np.linalg.norm(e[1] - e[0]) for e in es]
    rows = {0: [], 1: []}
    cover, count, tries = 0.0, 0, 0
    while cover < target * seen_all and tries < 400000:
        tries += 1
        got = flake(r, r.choices(es, weights)[0])
        if got is None:
            continue
        rows[0 if r.random() < ROWS[0][4] else 1] += got[0]
        cover += got[1]
        count += 1
    return rows, cover / seen_all if seen_all else 0.0, count, len(es)


def _add(j, b, data, ctype, kind, target=None, bounds=False):
    while len(b) % 4:
        b.append(0)
    raw = data.tobytes()
    view = {"buffer": 0, "byteOffset": len(b), "byteLength": len(raw)}
    if target:
        view["target"] = target
    j["bufferViews"].append(view)
    b.extend(raw)
    a = {"bufferView": len(j["bufferViews"]) - 1, "componentType": ctype, "count": len(data), "type": kind}
    if bounds:
        a["min"] = [float(x) for x in data.min(0)]
        a["max"] = [float(x) for x in data.max(0)]
    j["accessors"].append(a)
    return len(j["accessors"]) - 1


def append_to(glb, sidecar):
    j, b = read_glb(glb)
    with open(sidecar, encoding="utf-8") as f:
        side = json.load(f)
    if any(nd.get("name") == ROWS[0][0] for nd in j["nodes"]):
        raise SystemExit("paintChips status=REFUSED: this street already has them")
    tris = triangles(j, b, JOINERY)
    rows, cover, count, n_edges = make_flakes(tris)
    template = next(m for m in side["meshes"] if m["mesh"] == "street_frame_painted")
    faces = 0
    for i, (mesh, base, rgb, rough, _) in enumerate(ROWS):
        t = np.array(rows[i], dtype="f4").reshape(-1, 3)
        faces += len(t) // 3
        n = np.cross(t[1::3] - t[0::3], t[2::3] - t[0::3])
        n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
        nrm = np.repeat(n, 3, axis=0).astype("f4")
        uv = np.stack([t[:, 0] + t[:, 2], t[:, 1]], axis=1).astype("f4")
        idx = np.arange(len(t), dtype="u4")
        col = np.tile(np.array([1.0, 0.0, 1.0, 1.0], dtype="f4"), (len(t), 1))
        attrs = {"POSITION": _add(j, b, t, 5126, "VEC3", 34962, True), "NORMAL": _add(j, b, nrm, 5126, "VEC3", 34962),
                 "TEXCOORD_0": _add(j, b, uv, 5126, "VEC2", 34962), "COLOR_0": _add(j, b, col, 5126, "VEC4", 34962)}
        j["meshes"].append({"name": mesh, "primitives": [{"attributes": attrs, "indices": _add(j, b, idx, 5125, "SCALAR", 34963)}]})
        j["nodes"].append({"name": mesh, "mesh": len(j["meshes"]) - 1})
        j["scenes"][j.get("scene", 0)]["nodes"].append(len(j["nodes"]) - 1)
        row = dict(template)
        row.update({"mesh": mesh, "material": base, "base_material": base, "linear_rgb": rgb, "roughness": rough,
                    "faces": len(t) // 3})
        side["meshes"].append(row)
    write_glb(glb, j, b)
    with open(sidecar, "w", encoding="utf-8", newline="\n") as f:
        json.dump(side, f, indent=1)
    print("paintChips status=OK cover=%.4f flakes=%d arrises=%d faces=%d" % (cover, count, n_edges, faces))
    return 0


def selftest():
    # A window member, 6 by 8 cm and 1 m long, its front to the street (-z); and a lone facet too small to chip.
    def box(x0, x1, y0, y1, z0, z1):
        v = [np.array(c, float) for c in ((x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                          (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1))]
        q = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (1, 2, 6, 5), (0, 4, 7, 3)]
        return [[v[a], v[b], v[c]] for a, b, c, d in q] + [[v[a], v[c], v[d]] for a, b, c, d in q]
    t = np.array(box(5.0, 5.06, 0.2, 1.2, 5.0, 5.08))
    es, seen = arrises(t)
    fails = []
    if len(es) != 2:   # its two long ones; the 6 cm ends are under MIN_EDGE_M
        fails.append("the member's two long street-side arrises, found %d" % len(es))
    if abs(seen - 0.06) > 1e-6:
        fails.append("seen area %.4f, not 0.06" % seen)
    rows, cover, count, _ = make_flakes(t)
    if not (0.03 <= cover <= 0.10) or count == 0:
        fails.append("cover %.3f from %d flakes" % (cover, count))
    pts = np.array(rows[0] + rows[1]).reshape(-1, 3)
    if pts[:, 0].min() < 5.0 - 2 * PROUD_M or pts[:, 0].max() > 5.06 + 2 * PROUD_M or pts[:, 2].min() < 5.0 - 2 * PROUD_M \
            or pts[:, 1].min() < 0.2 - 1e-6 or pts[:, 1].max() > 1.2 + 1e-6:
        fails.append("a flake left its member")
    near = np.minimum(np.minimum(np.abs(pts[:, 0] - 5.0), np.abs(pts[:, 0] - 5.06)), np.abs(pts[:, 2] - 5.0))
    if near.max() > 0.05:
        fails.append("a flake %.3f m from an edge" % near.max())
    again, _, _, _ = make_flakes(t)
    if len(again[0]) != len(rows[0]) or not np.allclose(np.array(again[0]), np.array(rows[0])):
        fails.append("not the same each run")
    print("paintChips selftest %s" % ("PASS" if not fails else "FAIL " + "; ".join(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(append_to(sys.argv[1], sys.argv[2]))
