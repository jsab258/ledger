#!/usr/bin/env python3
"""How far round Tom's forearm a sleeve's cloth goes, slab by slab (the sleeve's end, fourth round, 28 October 2026).

    python tools/md-bridge/sleeve_wrap.py AVATAR.obj GARMENT.obj [GARMENT.obj ...] [--piece sleeveL] [--json OUT.json] [--joints J.json]

WHY. In every drape of Tom's zip jacket the sleeve's lower end lay as a flat flap past the hand and the hand came out
through its side (production/research/game-clothing-pipeline/RIB-CUFFS-2026-10-27.md, the third try's root fault), so
every cuff sewn to it failed. A sleeve's end can only close round the wrist if its cloth goes round the forearm. This
reads that off Marvelous's OBJ exports, arranged or draped.

HOW. The forearm's axis and the wrist come from tools/md-bridge/cuff_measure.py (found on the body as a tape finds
them). The piece's vertices are put in that frame and cut into 25 mm slabs along the axis, from 300 mm above the wrist
to 50 mm past it. For each slab: how much of the circle round the axis the cloth covers (36 ten-degree sectors, a
sector counted when a vertex lies in it), the median distance of the cloth from the axis, and how far the slab's
centroid lies off the axis. A sleeve round the arm covers most sectors with its centroid near the axis; a flap beside
the arm covers a few sectors with its centroid off to one side.
"""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cuff_measure import forearm, frame, hull_perimeter, load  # noqa: E402

SLABS = [(s, s + 25.0) for s in np.arange(-300.0, 50.0, 25.0)]


def forearm_from_joints(body, elbow, hand):
    """The forearm found from the skeleton's elbow and hand joints (Marvelous's millimetres), for a body the density
    finder in cuff_measure.py misreads (28 October: the straight-elbowed drape body, whose hand lies further out);
    the wrist is the narrowest cut within 40 mm of the hand joint."""
    elbow, hand = np.array(elbow, float), np.array(hand, float)
    a, u, w = frame(hand - elbow)
    rel = body - elbow
    along = rel @ a
    radial = np.linalg.norm(rel - np.outer(along, a), axis=1)
    L = float(np.linalg.norm(hand - elbow))
    prof = []
    for t in np.arange(L - 160.0, L + 60.0, 4.0):
        sel = (np.abs(along - t) < 4.0) & (radial < 75.0)
        if sel.sum() >= 10:
            q = rel[sel]
            prof.append((float(t), hull_perimeter(np.c_[q @ u, q @ w]), q))
    k = min((k for k in range(len(prof)) if abs(prof[k][0] - L) <= 40.0), key=lambda k: prof[k][1])
    t, g, q = prof[k]
    ctr = elbow + a * t + u * float((q @ u).mean()) + w * float((q @ w).mean())
    return {"centre": ctr, "axis": a, "u": u, "w": w, "girth": g, "profile": [(x - t, gg) for x, gg, _ in prof]}


def wrap(verts, f):
    rel = verts - f["centre"]
    along = rel @ f["axis"]
    x, y = rel @ f["u"], rel @ f["w"]
    out = []
    for s0, s1 in SLABS:
        sel = (along >= s0) & (along < s1)
        if sel.sum() < 3:
            out.append({"from": s0, "n": int(sel.sum())})
            continue
        ang = np.degrees(np.arctan2(y[sel], x[sel])) % 360.0
        cover = len(set((ang // 10).astype(int).tolist())) / 36.0
        r = np.hypot(x[sel], y[sel])
        out.append({"from": s0, "n": int(sel.sum()), "coverPct": round(100 * cover), "medianRadiusMm": round(float(np.median(r)), 1),
                    "centroidOffAxisMm": round(float(math.hypot(x[sel].mean(), y[sel].mean())), 1)})
    return out


def main(a):
    piece = a[a.index("--piece") + 1] if "--piece" in a else "sleeveL"
    out = a[a.index("--json") + 1] if "--json" in a else None
    files = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--piece", "--json", "--joints"))]
    _, groups = load(files[0])
    body = next(v for k, v in groups.items() if k.endswith("LOD0"))
    if "--joints" in a:
        j = json.load(open(a[a.index("--joints") + 1], encoding="utf-8"))
        side = "r" if piece.endswith("R") else "l"
        f = forearm_from_joints(body, j["lowerarm_" + side], j["hand_" + side])
    else:
        f = forearm(body, -1.0 if piece.endswith("R") else 1.0)
    res = {"wristGirthMm": round(f["girth"], 1), "garments": {}}
    print("wrist girth %.1f mm; slabs: mm from the wrist (- above it); cover %% round the axis / median radius / centroid off axis" % f["girth"])
    for p in files[1:]:
        _, g = load(p)
        if piece not in g:
            print("%s: no %s" % (p, piece))
            continue
        w = wrap(g[piece], f)
        res["garments"][p] = w
        print("%-22s " % os.path.basename(p)[:22] + " ".join("%+4d:%3s/%3s/%3s" % (d["from"], d.get("coverPct", "-"), int(d["medianRadiusMm"]) if "medianRadiusMm" in d else "-",
                                                                                   int(d["centroidOffAxisMm"]) if "centroidOffAxisMm" in d else "-") for d in w[::2]))
    if out:
        json.dump(res, open(out, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
