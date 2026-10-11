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


def fillet(pts, radii, n_arc=6):
    """round the corners of a polyline: radii maps a vertex index to its radius (mm); the arc is sampled at 12 degrees or less"""
    P = [np.array(p, float) for p in pts]
    out = [P[0]]
    for i in range(1, len(P) - 1):
        r = radii.get(i, 0.0)
        if r <= 0:
            out.append(P[i])
            continue
        a, b, c = P[i - 1], P[i], P[i + 1]
        u, v = (a - b), (c - b)
        lu, lv = np.linalg.norm(u), np.linalg.norm(v)
        u, v = u / lu, v / lv
        ang = math.acos(float(np.clip(np.dot(u, v), -1, 1)))
        if ang > math.pi - 1e-3:
            out.append(b)
            continue
        tl = min(r / math.tan(ang / 2.0), 0.45 * lu, 0.45 * lv)
        rr = tl * math.tan(ang / 2.0)
        p0, p1 = b + u * tl, b + v * tl
        bis = (u + v) / np.linalg.norm(u + v)
        cen = b + bis * (rr / math.sin(ang / 2.0))
        a0 = math.atan2(*(p0 - cen)[::-1])
        a1 = math.atan2(*(p1 - cen)[::-1])
        d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        k = max(2, int(math.ceil(abs(math.degrees(d)) / 12.0)))
        for j in range(k + 1):
            aa = a0 + d * j / k
            out.append(cen + rr * np.array([math.cos(aa), math.sin(aa)]))
    out.append(P[-1])
    return [(float(x), float(y)) for x, y in out]


def k6_profile():
    """REVIEW-v1-street fault 1: K6's head rounded. The target's unsoftened polyline (r, z): the rim's three corners (210, 590), (220, 630), (200, 670) become one
    bull-nose arc (centre (158.3, 624.2), radius 61.9), the top one dome of radius 425 centred on the axis at z 295, the other corners filleted (R20 at the barrel's
    shoulder and the neck, R10 on the flange, R5 on its foot edge)."""
    cen, rr = (158.3, 624.2), 61.9
    a0, a1 = math.atan2(590 - cen[1], 210 - cen[0]), math.atan2(670 - cen[1], 200 - cen[0])
    k = int(math.ceil(math.degrees(a1 - a0) / 6.0))
    rim = [(cen[0] + rr * math.cos(a0 + (a1 - a0) * j / k), cen[1] + rr * math.sin(a0 + (a1 - a0) * j / k)) for j in range(k + 1)]
    th1 = math.atan2(200.0, 375.0)
    nd = int(math.ceil(math.degrees(th1) / 4.0))
    dome = [(425.0 * math.sin(th1 * (1 - j / nd)), 295.0 + 425.0 * math.cos(th1 * (1 - j / nd))) for j in range(1, nd + 1)]
    pts = [(0.0, 0.0), (250.0, 0.0), (250.0, 40.0), (190.0, 60.0), (170.0, 80.0), (150.0, 470.0), (130.0, 510.0), (130.0, 550.0)]
    radii = {1: 5.0, 2: 10.0, 3: 10.0, 4: 10.0, 5: 20.0, 6: 20.0, 7: 20.0}
    radii2 = dict(radii)
    radii2[len(pts)] = 20.0                                   # the join of the underside and the rim's arc
    main = fillet(pts + [rim[0], rim[1]], radii2)
    return main[:-1] + rim[1:] + dome


def k5_profile(prof):
    """REVIEW-v1-street narrow point 1: K5's flange gets a flat seat for its four nuts (the target's profile slopes where its close-up photograph shows a seat):
    (141, 40), (125, 50), (105, 72), (95, 90), (91, 100) become (141, 40), (139, 42), (108, 42), (100, 52), (95, 70), (91, 100)"""
    out = []
    for r, z in prof:
        if (r, z) in ((125.0, 50.0), (105.0, 72.0), (95.0, 90.0)):
            continue
        out.append((r, z))
        if (r, z) == (141.0, 40.0):
            out += [(139.0, 42.0), (108.0, 42.0), (100.0, 52.0), (95.0, 70.0)]
    return out


def kind_profile(T, name):
    """the profile built for a kind or variant: the target's profile_rz, with the first review's fixes"""
    if name == "K6":
        return k6_profile()
    if name == "K5":
        return k5_profile([tuple(p) for p in T["kinds"]["K5"]["profile_rz"]])
    if name in ("K2b", "K6b"):
        v = [x for x in T["kinds"][name[:2]]["variants"] if x["id"] == name][0]["profile_rz"]
        pts = [tuple(p) for p in v]
        if name == "K6b":
            return fillet(pts, {i: 6.0 for i in range(1, len(pts) - 1)})
        return pts
    return [tuple(p) for p in T["kinds"][name]["profile_rz"]]


def radius_at(profile, z):
    zs = [p[1] for p in profile]
    rs = [p[0] for p in profile]
    return float(np.interp(z, zs, rs))


def prism_y(profile_xz, y0, y1):
    """an (x, z) profile extruded along y"""
    P = np.asarray(profile_xz, float)
    n = len(P)
    V = np.zeros((2 * n, 3))
    for k_, y in enumerate((y0, y1)):
        V[k_ * n:(k_ + 1) * n] = np.column_stack([P[:, 0], np.full(n, y), P[:, 1]])
    F = [tuple(range(n)), tuple(range(n, 2 * n))[::-1]] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return V, F


def build_kind(T, name, paint, out_dir, npz_dir):
    import bpy
    k = name[:2]
    K = T["kinds"][k]
    prof = kind_profile(T, name)
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
    B.add(name.lower() + "_body", lathe(prof), mname, bev=None)
    if k == "K5":
        fx = K["fixings"]["bolts"]
        R, af, nh, up = fx["pitch_circle_r"], fx["nut_across_flats"], fx["nut_height"], fx["stud_above_nut"]
        zf = next(z0 for (r0, z0), (r1, z1) in zip(prof[:-1], prof[1:]) if abs(z0 - z1) < 1e-6 and 0 < z0 < 60 and min(r0, r1) <= R <= max(r0, r1))   # the flat seat the nuts stand on
        for i, ang in enumerate(fx["angles_deg"]):
            cx, cy = R * math.cos(math.radians(ang)), R * math.sin(math.radians(ang))
            hexp = [(cx + af / math.sqrt(3.0) * math.cos(math.radians(60 * j + ang)), cy + af / math.sqrt(3.0) * math.sin(math.radians(60 * j + ang))) for j in range(6)]
            B.add("nut_%d" % i, bs.prism_ud([(x, -y) for x, y in hexp], zf - 0.5, zf + nh), mname, bev=1.0)
            rings = [[(cx + 5.0 * math.cos(2 * math.pi * j / 12), cy + 5.0 * math.sin(2 * math.pi * j / 12), z) for j in range(12)] for z in (zf, zf + nh + up)]
            B.add("stud_%d" % i, bs.loft_rings(rings), "bare_steel", bev=None)
        lug = K["fixings"]["chain_eyes"]["lug"]
        hc, rc = lug["hole_centre_from_shaft_face"], lug["proud"] - lug["hole_centre_from_shaft_face"]          # 22 from the shaft face, the outer end a half-round of radius 18
        for zc in K["fixings"]["chain_eyes"]["z"]:
            rs = radius_at(prof, zc)
            for sx, tag in ((-1.0, "w"), (1.0, "e")):
                # REVIEW-v1-street narrow point 2: a cast D lug: 55 high at the shaft, tapering to 36 at the hole centre, closed by a half-round about the hole, R3 edges
                d_ = [(-4.0, -27.5), (hc, -rc)] + [(hc + rc * math.cos(math.radians(a_)), rc * math.sin(math.radians(a_))) for a_ in range(-80, 81, 20)] + [(hc, rc), (-4.0, 27.5)]
                xz = [(sx * (rs + dx), zc + dz) for dx, dz in d_]
                if sx < 0:
                    xz = xz[::-1]
                ob = B.add("lug_%d_%s" % (int(zc), tag), prism_y(xz, -lug["thickness"] / 2.0, lug["thickness"] / 2.0), mname, bev=2.0)
                hx = sx * (rs + hc)
                rings = [[(hx + 12.0 * math.cos(2 * math.pi * j / 20), y_, zc + 12.0 * math.sin(2 * math.pi * j / 20)) for j in range(20)] for y_ in (-lug["thickness"], lug["thickness"])]
                Vc, Fc = bs.loft_rings([[(p[0], p[1], p[2]) for p in r] for r in rings])
                bs.bool_op(ob, Vc, Fc, "DIFFERENCE")
    obs = bs.finish(B, mats, 0.0)
    return bs.write(obs, name, 0.0, out_dir, npz_dir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="K1,K2,K2b,K3,K4,K5,K6,K6b")
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
