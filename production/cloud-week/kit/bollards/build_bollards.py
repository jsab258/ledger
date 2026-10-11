"""The bollards (bollards target, kinds K1 to K6; cloud week 42, unit 3.4), built by script from target.json.

    /home/user/.bpyenv/bin/python build_bollards.py [--only K1,K2,...] [--paint black|galvanised] [--out-dir DIR] [--npz-dir DIR]

Reads production/cloud-week/targets/bollards/target.json (kinds.K1 to K6, each its profile_rz, the revolved outline in millimetres: r and z, z up from
the ground, the pivot the axis at the ground). Writes production/assets/cloud-week/bollards/bollard_<K>.glb (K1 the cast-iron domed street bollard,
K2 the plain tapered iron bollard, K3 the round precast concrete bollard, K4 the steel tube bollard with its welded cap, K5 the bolted cast-iron chain
post with its four nuts and two pairs of chain lugs, K6 the quay mooring bollard) and kit/bollards/build/<K>.npz for check_bollards.py.
K7 (the horn cleat) and K5's chain are not built in this unit (the quay's, not Quay Street's). The conditions (the worn foot, the chalky paint, rust at
the foot) are the engine's masks, not geometry. 64 sides round the axis; smooth shading by angle.
"""
import argparse
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shopfront"))
sys.path.insert(0, os.path.join(HERE, "..", "railings"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import build_shopfront as bs  # noqa: E402
from build_railings import Parts, prism_x  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "bollards", "target.json")
ASSET_DIR = os.path.join(REPO, "production", "assets", "cloud-week", "bollards")
NPZ_DIR = os.path.join(HERE, "build")
N = 64


def lathe(profile, n=N):
    """A solid of revolution about z from a (r, z) outline from the foot to the top; points on the axis become apexes."""
    P = [(float(r), float(z)) for r, z in profile]
    rings, apex = [], []
    V = []
    idx = []
    for r, z in P:
        if r < 1e-6:
            V.append((0.0, 0.0, z))
            idx.append([len(V) - 1] * n)
        else:
            base = len(V)
            for k in range(n):
                a = 2 * math.pi * k / n
                V.append((r * math.cos(a), r * math.sin(a), z))
            idx.append(list(range(base, base + n)))
    F = []
    for i in range(len(P) - 1):
        for k in range(n):
            a, b = idx[i][k], idx[i][(k + 1) % n]
            c, d = idx[i + 1][(k + 1) % n], idx[i + 1][k]
            quad = [a, b, c, d]
            quad = [q for j, q in enumerate(quad) if q not in quad[:j]]       # drop the repeats at an apex
            if len(quad) >= 3:
                F.append(tuple(quad))
    if P[0][0] > 1e-6:                                                         # the foot: a flat disc
        F.append(tuple(idx[0][::-1]))
    if P[-1][0] > 1e-6:
        F.append(tuple(idx[-1]))
    Vn = np.array(V)
    vol = 0.0
    for f in F:
        for i in range(1, len(f) - 1):
            vol += np.dot(Vn[f[0]], np.cross(Vn[f[i]], Vn[f[i + 1]])) / 6.0
    if vol < 0:
        F = [tuple(f[::-1]) for f in F]
    return Vn, F


def radius_at(profile, z):
    zs = [p[1] for p in profile]
    rs = [p[0] for p in profile]
    return float(np.interp(z, zs, rs))


def build_kind(T, k, paint, out_dir, npz_dir):
    import bpy
    K = T["kinds"][k]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    pa = K["paint"]
    if k == "K3":
        mname, srgb, rough, metal = "concrete", (152, 150, 144), 0.9, 0.0
    elif k == "K4" and paint == "galvanised":
        mname, srgb, rough, metal = "galvanised_steel", (120, 122, 124), 0.4, 1.0
    else:
        mname, srgb, rough, metal = "paint_black", (24, 24, 26), float(pa.get("roughness", 0.5)), 0.0
    mats = {mname: bs.make_material(mname, srgb, rough, metal), "bare_steel": bs.make_material("bare_steel", (150, 150, 152), 0.5, 1.0)}
    B = Parts()
    B.add(k.lower() + "_body", lathe(K["profile_rz"]), mname, bev=None)
    if k == "K5":
        fx = K["fixings"]["bolts"]
        R, af, nh, up = fx["pitch_circle_r"], fx["nut_across_flats"], fx["nut_height"], fx["stud_above_nut"]
        zf = max(p[1] for p in K["profile_rz"] if abs(p[0]) > 0 and p[1] < 40)         # the flange's top
        for i, ang in enumerate(fx["angles_deg"]):
            cx, cy = R * math.cos(math.radians(ang)), R * math.sin(math.radians(ang))
            hexp = [(cx + af / math.sqrt(3.0) * math.cos(math.radians(60 * j + ang)), cy + af / math.sqrt(3.0) * math.sin(math.radians(60 * j + ang))) for j in range(6)]
            B.add("nut_%d" % i, bs.prism_ud([(x, -y) for x, y in hexp], zf - 0.5, zf + nh), mname, bev=1.0)
            rings = [[(cx + 5.0 * math.cos(2 * math.pi * j / 12), cy + 5.0 * math.sin(2 * math.pi * j / 12), z) for j in range(12)] for z in (zf, zf + nh + up)]
            B.add("stud_%d" % i, bs.loft_rings(rings), "bare_steel", bev=None)
        lug = K["fixings"]["chain_eyes"]["lug"]
        for zc in K["fixings"]["chain_eyes"]["z"]:
            rs = radius_at(K["profile_rz"], zc)
            for sx, tag in ((-1.0, "w"), (1.0, "e")):
                x0, x1 = sorted((sx * (rs - 4.0), sx * (rs + lug["proud"])))
                ob = B.add("lug_%d_%s" % (int(zc), tag), prism_x([(-lug["thickness"] / 2.0, zc - lug["height"] / 2.0), (lug["thickness"] / 2.0, zc - lug["height"] / 2.0),
                                                               (lug["thickness"] / 2.0, zc + lug["height"] / 2.0), (-lug["thickness"] / 2.0, zc + lug["height"] / 2.0)], x0, x1), mname, bev=2.0)
                hx = sx * (rs + lug["hole_centre_from_shaft_face"])
                rings = [[(hx + 12.0 * math.cos(2 * math.pi * j / 20), y_, zc + 12.0 * math.sin(2 * math.pi * j / 20)) for j in range(20)] for y_ in (-lug["thickness"], lug["thickness"])]
                Vc, Fc = bs.loft_rings([[(p[0], p[1], p[2]) for p in r] for r in rings])
                bs.bool_op(ob, Vc, Fc, "DIFFERENCE")
    obs = bs.finish(B, mats, 0.0)
    return bs.write(obs, k, 0.0, out_dir, npz_dir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="K1,K2,K3,K4,K5,K6")
    ap.add_argument("--paint", default="black", choices=["black", "galvanised"])
    ap.add_argument("--out-dir", default=ASSET_DIR)
    ap.add_argument("--npz-dir", default=NPZ_DIR)
    a = ap.parse_args()
    T = json.load(open(TARGET_JSON, encoding="utf-8"))
    pj = os.path.join(a.npz_dir, "parts.json")
    os.makedirs(a.npz_dir, exist_ok=True)
    res = json.load(open(pj)) if os.path.exists(pj) else {}
    for k in a.only.split(","):
        res[k] = build_kind(T, k, a.paint, a.out_dir, a.npz_dir)
        os.rename(os.path.join(a.out_dir, k + ".glb"), os.path.join(a.out_dir, "bollard_%s.glb" % k)) if os.path.exists(os.path.join(a.out_dir, k + ".glb")) else None
        res[k]["glb"] = os.path.join(a.out_dir, "bollard_%s.glb" % k)
        print(k, "triangles", res[k]["triangles"], "glb bytes", os.path.getsize(res[k]["glb"]), flush=True)
    json.dump(res, open(pj, "w"), indent=1)


if __name__ == "__main__":
    main()
