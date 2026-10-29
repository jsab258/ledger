#!/usr/bin/env python3
"""Two of a cuff's pass marks the other measures do not count: the arm's centre line through the cuff's cloth, and the
cuff's points inside the wrist (the game-garment skill, step 4; 29 October 2026).

    python tools/md-bridge/cuff_faults.py GARMENT_UNPOSED.obj [--joints J.json] [--piece cuffL] [--json OUT.json]
    python tools/md-bridge/cuff_faults.py --selftest

WHY. Drape 19 failed on both (2 cuff triangles crossed by the arm's centre line at each wrist; 8 and 5 points pulled
7 to 22 mm inside the wrist: production/research/game-clothing-pipeline/SLEEVE-END-2026-10-28.md), counted then by
hand. tools/md-bridge/cuff_measure.py and sleeve_wrap.py give place, gap and cover; this gives the other two, so each
try of the cuffs is judged on every mark by a tool.

HOW. Marvelous's OBJ in its millimetres, the garment bent back to his reference pose (tools/md/unpose_garment.py) with
its body group (the name ending LOD0). The centre line runs from the elbow joint to 80 mm past the hand joint
(J.json, default his body's joints-md-mm.json), and each of the piece's triangles is tested against it (Moller and
Trumbore). A cuff point is inside when it lies more than TOL_MM behind the body's surface at the body's nearest vertex
(the vertex normal from the body's own faces): the skin offset is 3 mm, so a point within 1 mm of the skin is not
counted.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cuff_measure import load  # noqa: E402

JOINTS = r"F:\LedgerTools\bodies\MH_TomL1\joints-md-mm.json"
PAST_HAND_MM = 80.0
TOL_MM = 1.0


def tris(v, faces):
    out = []
    for f in faces:
        for i in range(1, len(f) - 1):
            out.append((f[0], f[i], f[i + 1]))
    t = np.array(out, dtype=int)
    return v[t[:, 0]], v[t[:, 1]], v[t[:, 2]]


def crossings(a, b, p0, p1):
    """How many triangles (a, b, c arrays) the segment p0 to p1 passes through."""
    c = b[1]
    a, b = a, b[0]
    d = p1 - p0
    e1, e2 = b - a, c - a
    h = np.cross(d, e2)
    det = np.einsum("ij,ij->i", e1, h)
    ok = np.abs(det) > 1e-9
    inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
    s = p0 - a
    u = inv * np.einsum("ij,ij->i", s, h)
    q = np.cross(s, e1)
    w = inv * (q @ d)
    t = inv * np.einsum("ij,ij->i", e2, q)
    hit = ok & (u >= 0) & (w >= 0) & (u + w <= 1) & (t >= 0) & (t <= 1)
    return int(hit.sum())


def vertex_normals(v, faces):
    n = np.zeros_like(v)
    a, b, c = tris(v, faces)
    fn = np.cross(b - a, c - a)
    idx = []
    for f in faces:
        for i in range(1, len(f) - 1):
            idx.append((f[0], f[i], f[i + 1]))
    idx = np.array(idx, dtype=int)
    for k in range(3):
        np.add.at(n, idx[:, k], fn)
    ln = np.linalg.norm(n, axis=1, keepdims=True)
    return n / np.where(ln > 0, ln, 1.0)


def inside(points, body_v, body_n, chunk=256):
    """Each point's depth behind the body's surface at its nearest body vertex (mm, positive = inside)."""
    depth = np.empty(len(points))
    for s in range(0, len(points), chunk):
        p = points[s:s + chunk]
        d2 = ((p[:, None, :] - body_v[None, :, :]) ** 2).sum(axis=2)
        j = d2.argmin(axis=1)
        depth[s:s + chunk] = -np.einsum("ij,ij->i", p - body_v[j], body_n[j])
    return depth


def measure(path, piece, joints):
    v, fs = load(path, faces=True)
    body_key = next(k for k in fs if k.endswith("LOD0"))
    side = "l" if piece.endswith("L") else "r"
    elbow, hand = np.array(joints["lowerarm_" + side]), np.array(joints["hand_" + side])
    axis = (hand - elbow) / np.linalg.norm(hand - elbow)
    a, b, c = tris(v, fs[piece])
    cross = crossings(a, (b, c), elbow, hand + PAST_HAND_MM * axis)
    used = sorted({i for f in fs[piece] for i in f})
    body_used = sorted({i for f in fs[body_key] for i in f})
    bn = vertex_normals(v, fs[body_key])
    near = np.linalg.norm(v[body_used] - hand, axis=1) < 250.0       # the wrist and hand's own skin, not the hip's
    bv, bnn = v[body_used][near], bn[body_used][near]
    depth = inside(v[used], bv, bnn)
    deep = depth[depth > TOL_MM]
    return {"centreLineCrossings": cross, "pointsInside": int(len(deep)),
            "deepestMm": round(float(deep.max()), 1) if len(deep) else 0.0, "points": len(used)}


def selftest():
    p0, p1 = np.array([0.0, 0, -1]), np.array([0.0, 0, 1])
    a = np.array([[-1.0, -1, 0], [5.0, 5, 0]])
    b = np.array([[1.0, -1, 0], [6.0, 5, 0]])
    c = np.array([[0.0, 1, 0], [5.0, 6, 0]])
    ok = int(crossings(a, (b, c), p0, p1) == 1)
    bv = np.array([[0.0, 0, 0]])
    bn = np.array([[0.0, 0, 1]])
    d = inside(np.array([[0.0, 0, -5], [0.0, 0, 5]]), bv, bn)
    ok2 = int(abs(d[0] - 5) < 1e-9 and abs(d[1] + 5) < 1e-9)
    print("cuff_faults selftest: passed=%d/2 failed=%d" % (ok + ok2, 2 - ok - ok2))
    return 0 if ok and ok2 else 1


def main(a):
    if "--selftest" in a:
        return selftest()
    piece = a[a.index("--piece") + 1] if "--piece" in a else "cuffL"
    jp = a[a.index("--joints") + 1] if "--joints" in a else JOINTS
    out = a[a.index("--json") + 1] if "--json" in a else None
    files = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--piece", "--json", "--joints"))]
    joints = json.load(open(jp, encoding="utf-8"))
    res = {}
    for f in files:
        res[f] = measure(f, piece, joints)
        print(f, piece, json.dumps(res[f]))
    if out:
        json.dump(res, open(out, "w", encoding="utf-8"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
