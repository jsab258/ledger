#!/usr/bin/env python3
"""Where a cuff sits on Tom's left wrist, measured off Marvelous's own OBJ exports (the cuffs' third try, 27 October 2026).

    python tools/md-bridge/cuff_measure.py AVATAR.obj CUFF.obj [CUFF.obj ...] [--piece cuffL] [--json OUT.json]

WHY. The research (production/research/game-clothing-pipeline/RIB-CUFFS-2026-10-27.md, section 3) sets pass marks a
cuff must meet before the jacket is baked: its ring's centre within 30 mm of the wrist along the forearm and within
30 mm of the forearm's axis (round it, not beside it), its lower edge's loop no looser than the wrist's girth plus the
avatar's skin offset and a few millimetres, and no gap over 5 mm beyond that offset. Two drapes failed by eye; this
puts numbers on each try.

HOW. The wrist is found on the body itself, as a tape finds it: the forearm's axis is fitted to the arm's own vertices
(the slab centres between the elbow and the hand, then refined by the points' principal direction), the body is cut
square to that axis every 4 mm, and each cut's girth is the length round its convex outline (a tape bridges hollows).
The wrist is the narrowest cut between the forearm's thick part and the hand's widening. The cuff's vertices (the OBJ
group named --piece) are then put in the forearm's frame: along (mm past the wrist toward the hand, + is onto the
hand), off the axis (mm), the girth round its lowest row, and its gap to the skin (the body cut's radius at that
angle subtracted from the cuff's), all in Marvelous's millimetres.
"""
import json
import math
import sys

import numpy as np


def load(path, faces=False):
    verts, groups, fs, cur = [], {}, {}, None
    for line in open(path, encoding="utf-8", errors="replace"):
        if line.startswith("v "):
            verts.append([float(x) for x in line.split()[1:4]])
        elif line.startswith("g "):
            cur = line[2:].strip()
            groups.setdefault(cur, set())
            fs.setdefault(cur, [])
        elif line.startswith("f ") and cur:
            f = [int(t.split("/")[0]) - 1 for t in line.split()[1:]]
            groups[cur].update(f)
            fs[cur].append(f)
    v = np.array(verts)
    if faces:
        return v, fs
    return v, {k: v[sorted(s)] for k, s in groups.items()}


def boundary_loops(faces):
    """The piece's open edges (each used by one face) chained into loops of vertex indices."""
    count = {}
    for f in faces:
        for i in range(len(f)):
            e = tuple(sorted((f[i], f[(i + 1) % len(f)])))
            count[e] = count.get(e, 0) + 1
    nbr = {}
    for (a, b), n in count.items():
        if n == 1:
            nbr.setdefault(a, []).append(b)
            nbr.setdefault(b, []).append(a)
    loops, seen = [], set()
    for start in nbr:
        if start in seen:
            continue
        loop, prev, cur = [start], None, start
        seen.add(start)
        while True:
            nxt = [x for x in nbr[cur] if x != prev and x not in seen]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            seen.add(cur)
            loop.append(cur)
        loops.append(loop)
    return loops


def hull_perimeter(p2):
    """The length round the convex outline of 2D points (monotone chain)."""
    pts = sorted(map(tuple, np.round(p2, 4)))
    if len(pts) < 3:
        return 0.0
    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and (out[-1][0] - out[-2][0]) * (p[1] - out[-2][1]) - (out[-1][1] - out[-2][1]) * (p[0] - out[-2][0]) <= 0:
                out.pop()
            out.append(p)
        return out
    h = half(pts)[:-1] + half(pts[::-1])[:-1]
    return float(sum(math.dist(h[i], h[(i + 1) % len(h)]) for i in range(len(h))))


def frame(axis):
    a = axis / np.linalg.norm(axis)
    t = np.cross(a, [0.0, 1.0, 0.0])
    if np.linalg.norm(t) < 1e-6:
        t = np.cross(a, [1.0, 0.0, 0.0])
    u = t / np.linalg.norm(t)
    return a, u, np.cross(a, u)


def forearm(body, side=1.0):
    """The left forearm's axis (a point and a unit direction toward the hand) and the wrist on it."""
    # the arm clear of the torso (MetaHuman's A pose holds it out from 330 mm)
    arm = body[body[:, 0] * side > 330.0]
    # slab centres every 5 mm along x trace the arm; the hand begins where the mesh turns dense (the fingers): the
    # first slab holding over twice the forearm's usual vertex count
    cents = []
    for x0 in np.arange(330.0, 600.0, 5.0):
        s = arm[(arm[:, 0] * side >= x0) & (arm[:, 0] * side < x0 + 5.0)]
        if len(s) > 8:
            cents.append((x0, s.mean(0), len(s)))
    usual = float(np.median([n for _, _, n in cents[: len(cents) // 3]]))
    hand_i = next(i for i, (_, _, n) in enumerate(cents) if i > 6 and n > 2.0 * usual)
    # the forearm's axis: the line through the slab centres from 90 mm to 10 mm (in x) before the hand
    x_hand = cents[hand_i][0]
    pts = np.array([p for x0, p, _ in cents if x_hand - 90.0 <= x0 <= x_hand - 10.0])
    c = pts.mean(0)
    _, _, vt = np.linalg.svd(pts - c)
    d = vt[0] if vt[0][0] * side > 0 else -vt[0]
    a, u, w = frame(d)
    # girth every 4 mm square to the axis, each cut 8 mm thick (the arm's mesh is sparse)
    rel = arm - c
    along = rel @ a
    radial = np.linalg.norm(rel - np.outer(along, a), axis=1)
    s_hand = float((cents[hand_i][1] - c) @ a)
    prof = []
    for s in np.arange(s_hand - 160.0, s_hand + 60.0, 4.0):
        sel = (np.abs(along - s) < 4.0) & (radial < 75.0)
        if sel.sum() >= 10:
            q = rel[sel]
            prof.append((float(s), hull_perimeter(np.c_[q @ u, q @ w]), q))
    # the wrist: the narrowest cut in the 100 mm before the hand begins
    lo = [k for k in range(len(prof)) if s_hand - 100.0 <= prof[k][0] <= s_hand + 10.0]
    k = min(lo, key=lambda k: prof[k][1])
    wrist_s, wrist_g, wrist_q = prof[k]
    # the axis passes through the wrist cut's own centre
    q2 = np.c_[wrist_q @ u, wrist_q @ w]
    ctr = c + a * wrist_s + u * float(q2[:, 0].mean()) + w * float(q2[:, 1].mean())
    return {"centre": ctr, "axis": a, "u": u, "w": w, "girth": wrist_g, "profile": [(s - wrist_s, g) for s, g, _ in prof],
            "arm": arm}


def skin_radius(arm, f, s, ang):
    """The body's radius round the axis at distance s and angle ang (the farthest skin point in a 30 degree wedge)."""
    rel = arm - f["centre"]
    along = rel @ f["axis"]
    sel = np.abs(along - s) < 4.0
    q = rel[sel]
    x, y = q @ f["u"], q @ f["w"]
    r = np.hypot(x, y)
    keep = r < 90.0
    if not keep.any():
        return float("nan")
    da = np.abs((np.arctan2(y[keep], x[keep]) - ang + math.pi) % (2 * math.pi) - math.pi)
    wedge = da < math.radians(15)
    return float(r[keep][wedge].max()) if wedge.any() else float("nan")


def measure_cuff(cuff, f, verts=None, loops=None):
    rel = cuff - f["centre"]
    along = rel @ f["axis"]
    x, y = rel @ f["u"], rel @ f["w"]
    centre_along = float(along.mean())
    off_axis = float(math.hypot(x.mean(), y.mean()))
    # its lower edge: of its open edges' loops, the one lying farthest toward the hand, its length measured along
    # the edge itself (a cuff not yet closed into a ring has one open loop round its whole outline: then 0)
    # Marvelous exports a sewn seam unwelded, so a cuff sewn into a tube still has one open outline: its lower edge is
    # then the longest run of that outline lying in its hand-side half, and the ring is closed across the seam's gap
    loop, seam_gap = 0.0, float("nan")
    if loops:
        rings = [l for l in loops if len(l) >= 8]
        if len(rings) >= 2:
            low = max(rings, key=lambda l: float(np.mean((verts[l] - f["centre"]) @ f["axis"])))
            p = verts[low]
            loop = float(np.sum(np.linalg.norm(p - np.roll(p, -1, axis=0), axis=1)))
        elif rings:
            ring = rings[0]
            s = (verts[ring] - f["centre"]) @ f["axis"]
            half = s > (s.min() + s.max()) / 2.0
            n, best = len(ring), (0, 0)
            for i in range(n):
                if half[i] and not half[i - 1]:
                    j = i
                    while half[j % n] and j - i < n:
                        j += 1
                    best = max(best, (j - i, i))
            if best[0] >= 3:
                run = [ring[(best[1] + k) % n] for k in range(best[0])]
                p = verts[run]
                seam_gap = float(np.linalg.norm(p[0] - p[-1]))
                loop = float(np.sum(np.linalg.norm(p[1:] - p[:-1], axis=1))) + seam_gap
    # gaps: each cuff vertex's radius less the skin's at its own place and angle
    gaps = []
    for i in range(len(cuff)):
        r = math.hypot(x[i], y[i])
        sr = skin_radius(f["arm"], f, along[i], math.atan2(y[i], x[i]))
        if not math.isnan(sr):
            gaps.append(r - sr)
    gaps = np.array(gaps) if gaps else np.array([float("nan")])
    return {"centrePastWristMm": round(centre_along, 1), "centreOffAxisMm": round(off_axis, 1),
            "spanAlongMm": [round(float(along.min()), 1), round(float(along.max()), 1)],
            "lowerLoopMm": round(loop, 1), "seamGapMm": round(seam_gap, 1), "gapMedianMm": round(float(np.median(gaps)), 1),
            "gapMaxMm": round(float(np.max(gaps)), 1), "vertices": int(len(cuff))}


def main(a):
    piece = a[a.index("--piece") + 1] if "--piece" in a else "cuffL"
    out = a[a.index("--json") + 1] if "--json" in a else None
    files = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--piece", "--json"))]
    _, groups = load(files[0])
    body = next(v for k, v in groups.items() if k.endswith("LOD0"))
    f = forearm(body, -1.0 if piece.endswith("R") else 1.0)
    res = {"wrist": {"girthMm": round(f["girth"], 1), "centre": [round(float(x), 1) for x in f["centre"]],
                     "axis": [round(float(x), 3) for x in f["axis"]]}, "cuffs": {}}
    print("wrist girth %.1f mm at %s, forearm axis %s" % (f["girth"], res["wrist"]["centre"], res["wrist"]["axis"]))
    for p in files[1:]:
        v, fs = load(p, faces=True)
        if piece not in fs:
            print("%s: no group %s" % (p, piece))
            continue
        idx = sorted({i for face in fs[piece] for i in face})
        m = measure_cuff(v[idx], f, v, boundary_loops(fs[piece]))
        res["cuffs"][p] = m
        print("%-60s %s" % (p[-60:], json.dumps(m)))
    if out:
        json.dump(res, open(out, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
