"""The automatic check of the guard rail panel (kit/railings): the built mesh against the railings target's A1 numbers.

    /home/user/.bpyenv/bin/python check_railings.py [--version 1]

Cuts the built meshes (build/<name>.npz from build_railings.py) and reads: the overall box, the posts and caps, the rails and end plates,
the 17 bars (centres, diameter, length, the clear gaps against the 100 mm rule), the four studs and nuts, the post's and the top rail's
section against the target's own profiles (IoU, outline distance), closed solids, no hatching (coplanar same-way overlaps), the files.
Writes checks/check_v<N>.json.
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from shapely.geometry import Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shopfront"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import check_shopfront as cs  # noqa: E402  (the shared reading tools)
import outline  # noqa: E402
from outline import compare, load_npz, section  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "railings", "target.json")
SCRATCH = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/kit-railings"


def bbox(M, *prefixes):
    V = np.vstack([M[n][0] for n in M if any(n.startswith(p) for p in prefixes)]) * 1000.0
    return V.min(0), V.max(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", type=int, default=1)
    a = ap.parse_args()
    T = json.load(open(TARGET_JSON, encoding="utf-8"))
    A = T["kinds"]["A1"]
    P = A["panel"]
    M = load_npz(os.path.join(HERE, "build", "guard_rail_A1.npz"))
    Mp = load_npz(os.path.join(HERE, "build", "guard_rail_A1_ground_patch.npz"))
    info = json.load(open(os.path.join(HERE, "build", "parts.json")))
    rep = cs.Report()
    lo, hi = bbox(M, "")
    rep.within("BOX overall x, y, z (the target's bbox, patches excluded)", [lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]], [-1036.0, 1036.0, -25.0, 25.0, 0.0, 1030.0], 1.0)
    for tag, x in (("l", -1000.0), ("r", 1000.0)):
        pl, ph = bbox(M, "post_" + tag, "cap_" + tag)
        rep.within("POST %s: x range, y range, z range (post and cap)" % tag, [pl[0], ph[0], pl[1], ph[1], pl[2], ph[2]], [x - 25.0, x + 25.0, -15.0, 15.0, 0.0, 1030.0], 0.6)
        cl, ch = bbox(M, "cap_" + tag)
        rep.within("CAP %s: z range 1027 to 1030" % tag, [cl[2], ch[2]], [1027.0, 1030.0], 0.6)
    tl, th = bbox(M, "top_rail", "top_plate")
    rep.within("TOP RAIL (with its plates): x +-975, y +-25, z 970 to 1000", [tl[0], th[0], tl[1], th[1], tl[2], th[2]], [-975.0, 975.0, -25.0, 25.0, 970.0, 1000.0], 0.6)
    bl, bh = bbox(M, "bottom_rail", "bot_plate")
    rep.within("BOTTOM RAIL (with its plates): x +-975, y +-20, z 190 to 210", [bl[0], bh[0], bl[1], bh[1], bl[2], bh[2]], [-975.0, 975.0, -20.0, 20.0, 190.0, 210.0], 0.6)
    bars = sorted(n for n in M if n.startswith("bar_"))
    cx = [sum(bbox(M, n)[i][0] for i in (0, 1)) / 2.0 for n in bars]
    rep.add("BARS: seventeen", len(bars) == 17, len(bars), 17)
    rep.within("BARS: centres along x (pitch 109.09)", cx, P["infill"]["x"], 0.5)
    bz = [bbox(M, n) for n in bars]
    rep.within("BARS: z from 209.5 to 970.5 (210 to 970 with 0.5 into each rail), all bars", [min(b[0][2] for b in bz), max(b[1][2] for b in bz)], [209.5, 970.5], 0.3)
    fr = cs.frame_for([-30, 400, 30, 600], margin=2.0, mmpx=0.1)
    d_ = [Polygon([(p[0], p[1]) for p in cs.section_poly(M, (n,), 2, 500.0, (0, 1))]) if False else cs.section_poly(M, (n,), 2, 500.0, (0, 1)) for n in bars]
    widths = [g.bounds[2] - g.bounds[0] for g in d_]
    rep.within("BARS: diameter 12 at z 500 (a 12-gon: 12 corner to corner, 11.6 across flats)", [min(widths), max(widths)], [11.8, 12.0], 0.3)
    edges = [-975.0] + [c for c in cx] + [975.0]
    gaps = []
    for i in range(len(edges) - 1):
        w0 = 0.0 if i == 0 else 6.0
        w1 = 0.0 if i == len(edges) - 2 else 6.0
        gaps.append(edges[i + 1] - edges[i] - w0 - w1 - (25.0 if i == 0 else 0.0) - (25.0 if i == len(edges) - 2 else 0.0) + (25.0 if i == 0 else 0.0) + (25.0 if i == len(edges) - 2 else 0.0))
    # clear gaps: bar to bar, and the end bars to the post faces (the end plates stand at +-975, the posts' inner faces)
    rep.add("GAPS: every clear gap at most 100 (the sphere rule), bar to bar and bar to post face", max(gaps) <= 100.0, [round(min(gaps), 2), round(max(gaps), 2)], "<= 100")
    for b in P["bolts"]["list"]:
        tag = ("l" if b["post_x"] < 0 else "r") + ("t" if b["z"] > 500 else "b")
        sl, sh = bbox(M, "stud_" + tag)
        nl, nh = bbox(M, "nut_" + tag)
        sx = 1.0 if b["post_x"] > 0 else -1.0
        s_exp = sorted((b["plate_x"][1] - sx * 1.0, b["thread_end_x"]))
        n_exp = sorted(b["nut_x"])
        rep.within("STUD %s: x range, diameter 10 (y and z extents), centre z" % tag, [sl[0], sh[0], sh[1] - sl[1], sh[2] - sl[2], (sl[2] + sh[2]) / 2.0], [s_exp[0], s_exp[1], 10.0, 10.0, b["z"]], 0.6,
                   "a 12-gon: 11.6 across flats reads 10 +-0.6")
        rep.within("NUT %s: x range 1025 to 1033, across flats 17 (z), corner to corner (y), centre z" % tag, [nl[0], nh[0], nh[2] - nl[2], nh[1] - nl[1], (nl[2] + nh[2]) / 2.0], [n_exp[0], n_exp[1], 17.0, 17.0 * 2 / math.sqrt(3.0), b["z"]], 1.0, "1 mm chamfer")
    rep.add("STUDS: the thread stands 3 beyond the nut (1036 against 1033)", all(abs(bbox(M, "stud_" + t)[1][0] * (1 if "r" in t else -1) - 1036.0) < 0.6 or abs(bbox(M, "stud_" + t)[0][0] - (-1036.0)) < 0.6 for t in ("lt", "lb", "rt", "rb")), True, True)
    # sections against the target's profiles
    pro = A["profiles"]
    outer = [(p[0], p[1]) for p in pro["post_section"]["outer"]]
    fr = cs.frame_for([-30, -20, 30, 20], margin=2.0, mmpx=0.05)
    mod = section(M, 2, 0.5, (0, 1), fr, only=("post_l",))
    from outline import Frame
    fr2 = Frame((-1000 - 30 - 2) / 1000.0, (-20 - 2) / 1000.0, (60 + 4) / 1000.0, 44 / 1000.0, 0.05)
    mod = section(M, 2, 0.5, (0, 1), fr2, only=("post_l",))
    tgt = cs.raster([[(p[0] - 1000.0, p[1]) for p in outer]], fr2)
    c = compare(mod, tgt, 0.05)
    rep.compare_row("SECTION post plan at z 500 against the target's outer profile (RHS 50 x 30, R4.5)", c, {"iou": 0.97, "p95_mm": 0.3, "max_mm": 0.8})
    trp = [(p[0], p[1]) for p in pro["top_rail_section"]["outer"]] if "top_rail_section" in pro else None
    if trp:
        fr3 = Frame((-30) / 1000.0, (985 - 22) / 1000.0, 60 / 1000.0, 44 / 1000.0, 0.05)
        mod = section(M, 0, 0.0, (1, 2), fr3, only=("top_rail",))
        tgt = cs.raster([[(p[0], p[1] + 985.0) for p in trp]], fr3)
        rep.compare_row("SECTION top rail at x 0 against the target's profile (RHS 50 x 30 laid flat)", compare(mod, tgt, 0.05), {"iou": 0.97, "p95_mm": 0.3, "max_mm": 0.8})
    # closed solids, hatching, files
    bad = []
    for n, (V, F) in M.items():
        cnt = {}
        for f in F:
            for i in range(len(f)):
                e = tuple(sorted((int(f[i]), int(f[(i + 1) % len(f)]))))
                cnt[e] = cnt.get(e, 0) + 1
        if any(v != 2 for v in cnt.values()):
            bad.append(n)
    rep.add("SOLID every object closed (each edge on two triangles)", not bad, bad, [])
    same, ex = cs.coplanar(M)
    rep.add("HATCH faces of different objects in one plane, facing the same way, overlapping > 1 mm2", same == 0, {"count": same, "examples": ex[:6]}, 0)
    for name, inf in info.items():
        size = os.path.getsize(inf["glb"])
        rep.add("FILE %s under 1 MB, under 20,000 triangles" % name, size < 1_000_000 and inf["triangles"] < 20000, [size, inf["triangles"]], "< 1000000, < 20000")
    prims, js = cs.read_glb(info["A1"]["glb"])
    rep.add("FILE A1: no textures, a UV set on every mesh, materials named by what they are", not js.get("images") and all(p["uv"] for p in prims) and all(m["name"] in ("galvanised_steel", "bare_zinc", "paint_black") for m in js.get("materials", [])),
            [m["name"] for m in js.get("materials", [])], "galvanised_steel, bare_zinc")
    req = rep.rows
    out = {"version": a.version, "passed": sum(1 for r in req if r["ok"]), "failed": [r["id"] for r in req if not r["ok"]], "total": len(req), "rows": rep.rows,
           "not_built": ["Q2 quay tube railing (the jetty only: not on Quay Street)", "R3A, R3B, R3D cast-iron reserve kinds (unplaced)", "the seeds: lean, bent bars, polish, stickers (the engine's variants and masks)"]}
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    path = os.path.join(HERE, "checks", "check_v%d.json" % a.version)
    json.dump(out, open(path, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    print("\nRESULT: %d of %d checks pass; failed: %s -> %s" % (out["passed"], out["total"], out["failed"], path))
    return 0 if not out["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
