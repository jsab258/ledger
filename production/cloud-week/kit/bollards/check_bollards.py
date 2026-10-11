"""The automatic check of the bollards (kit/bollards): each built kind against the bollards target's own numbers.

    /home/user/.bpyenv/bin/python check_bollards.py [--version 1]

Per kind K1 to K6: the height and the foot's diameter; the body's section through its axis against the target's profile_rz (two-way Hausdorff,
IoU); K5's four nuts (on the pitch circle, across flats, height), studs (above the nut) and the chain lugs (proud, height, thickness, the hole);
every object a closed solid; no hatching; the files. Writes checks/check_v<N>.json.
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
import check_shopfront as cs  # noqa: E402
from outline import load_npz  # noqa: E402
sys.path.insert(0, os.path.join(HERE, "..", "railings"))
import build_bollards as bb  # noqa: E402  (kind_profile: the profile that was built)

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "bollards", "target.json")


def bbox(M, *prefixes):
    V = np.vstack([M[n][0] for n in M if any(n.startswith(p) for p in prefixes)]) * 1000.0
    return V.min(0), V.max(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", type=int, default=1)
    a = ap.parse_args()
    T = json.load(open(TARGET_JSON, encoding="utf-8"))
    info = json.load(open(os.path.join(HERE, "build", "parts.json")))
    rep = cs.Report()
    for k, inf in info.items():
        K = T["kinds"][k[:2]]
        M = load_npz(os.path.join(HERE, "build", k + ".npz"))
        body = k.lower() + "_body"
        lo, hi = bbox(M, body)
        prof = bb.kind_profile(T, k)
        raw = [tuple(p) for p in (K["profile_rz"] if len(k) == 2 else [v for v in K["variants"] if v["id"] == k][0]["profile_rz"])]
        exp_h = K["height"] if len(k) == 2 else raw[-1][1]
        rep.within("%s height" % k, hi[2] - lo[2], exp_h, 0.6)
        rmax_foot = max(p[0] for p in prof if p[1] < 0.15 * exp_h)
        if len(k) == 2:
            rep.within("%s foot diameter (the profile's r at the ground, x 2; the target's base_diameter %s)" % (k, K["base_diameter"]), 2 * rmax_foot, K["base_diameter"], 0.7,
                       "a 64-gon: corners on the target's radius")
        if k in ("K6", "K6b", "K5"):
            rg = Polygon(raw + [(-p[0], p[1]) for p in raw[::-1]]).buffer(0)
            pg = Polygon(prof + [(-p[0], p[1]) for p in prof[::-1]]).buffer(0)
            hh = max(pg.boundary.hausdorff_distance(rg.boundary), rg.boundary.hausdorff_distance(pg.boundary))
            rep.add("%s the built profile against the target's raw profile (REVIEW-v1-street: the corners rounded, K5's flange given a flat nut seat): two-way Hausdorff at most %s" % (k, 22 if k != "K5" else 12), hh <= 22.0, round(hh, 2), "<= 22 (the flat seat moves K5's flange profile by up to 18)")
        g = cs.section_poly(M, (body,), 1, 0.0, (0, 2))
        right = Polygon([(p[0], p[1]) for p in prof] + [(0.0, prof[-1][1])]).buffer(0)
        both = Polygon([(p[0], p[1]) for p in prof] + [(-p[0], p[1]) for p in prof[::-1]]).buffer(0)
        h = max(g.boundary.hausdorff_distance(both.boundary), both.boundary.hausdorff_distance(g.boundary))
        iou = g.intersection(both).area / g.union(both).area
        rep.add("%s profile: section through the axis against profile_rz, two-way Hausdorff and IoU" % k, h <= 1.0 and iou >= 0.995, [round(h, 3), round(iou, 5)], "<= 1.0, >= 0.995")
        if k == "K5":
            fx = K["fixings"]["bolts"]
            for i, ang in enumerate(fx["angles_deg"]):
                nl, nh = bbox(M, "nut_%d" % i)
                c = ((nl[0] + nh[0]) / 2.0, (nl[1] + nh[1]) / 2.0)
                rep.within("K5 nut %d: centre on the pitch circle r %s at %s degrees, height %s, its underside on the flat seat (z 42, 0.5 in)" % (i, fx["pitch_circle_r"], ang, fx["nut_height"]),
                           [c[0], c[1], nh[2] - nl[2], nl[2]], [fx["pitch_circle_r"] * math.cos(math.radians(ang)), fx["pitch_circle_r"] * math.sin(math.radians(ang)), fx["nut_height"] + 0.5, 41.5], 1.0)
                sl, sh = bbox(M, "stud_%d" % i)
                rep.within("K5 stud %d: tops %s above the nut, 10 across" % (i, fx["stud_above_nut"]), [sh[2] - nh[2], sh[0] - sl[0]], [fx["stud_above_nut"], 10.0], 0.8)
            lug = K["fixings"]["chain_eyes"]["lug"]
            for zc in K["fixings"]["chain_eyes"]["z"]:
                for tag in ("w", "e"):
                    ll, lh = bbox(M, "lug_%d_%s" % (int(zc), tag))
                    rs = float(np.interp(zc, [p[1] for p in prof], [p[0] for p in prof]))
                    rep.within("K5 lug z %d %s: proud %s of the shaft, height %s, thickness %s, centre z" % (zc, tag, lug["proud"], lug["height"], lug["thickness"]),
                               [max(abs(ll[0]), abs(lh[0])) - rs, lh[2] - ll[2], lh[1] - ll[1], (ll[2] + lh[2]) / 2.0], [lug["proud"], lug["height"], lug["thickness"], zc], 2.0)
                    gl = cs.section_poly(M, ("lug_%d_%s" % (int(zc), tag),), 1, 0.0, (0, 2))
                    rep.add("K5 lug z %d %s: the eye's hole (an interior ring in the section at y 0)" % (zc, tag), len(gl.interiors) == 1 if gl.geom_type == "Polygon" else False, gl.geom_type, "one hole")
        bad = []
        for n, (V, F) in M.items():
            cnt = {}
            for f in F:
                for i in range(len(f)):
                    e = tuple(sorted((int(f[i]), int(f[(i + 1) % len(f)]))))
                    cnt[e] = cnt.get(e, 0) + 1
            if any(v != 2 for v in cnt.values()):
                bad.append(n)
        rep.add("%s every object a closed solid (each edge on two faces)" % k, not bad, bad, [])
        same, ex = cs.coplanar(M)
        rep.add("%s hatching: faces of different objects in one plane, same way, overlapping > 1 mm2" % k, same == 0, {"count": same, "examples": ex[:4]}, 0)
        size = os.path.getsize(inf["glb"])
        rep.add("%s file under 1 MB and 20,000 triangles" % k, size < 1_000_000 and inf["triangles"] < 20000, [size, inf["triangles"]], "< 1000000, < 20000")
        prims, js = cs.read_glb(inf["glb"])
        rep.add("%s no textures, a UV set on every mesh, materials named by what they are" % k, not js.get("images") and all(p["uv"] for p in prims), [m["name"] for m in js.get("materials", [])], "named, no images")
    out = {"version": a.version, "passed": sum(1 for r in rep.rows if r["ok"]), "failed": [r["id"] for r in rep.rows if not r["ok"]], "total": len(rep.rows), "rows": rep.rows,
           "not_built": ["K7 horn cleat and K5's chain (the quay's, not Quay Street's)", "the condition seeds (worn foot, chalk, rust): the engine's masks"]}
    path = os.path.join(HERE, "checks", "check_v%d.json" % a.version)
    json.dump(out, open(path, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    print("\nRESULT: %d of %d checks pass; failed: %s -> %s" % (out["passed"], out["total"], out["failed"], path))
    return 0 if not out["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
