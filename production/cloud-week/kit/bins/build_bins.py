"""Quay Street's litter bins and household dustbins (cloud week 42, unit 3.5), built by script from targets/litter-bins/target.json.

    /home/user/.bpyenv/bin/python build_bins.py [--only K1,K2,D1] [--out-dir DIR] [--npz-dir DIR]

Nine models, three conditions of each kind (the shape never varies, the damage does): K1_pole_open_A, _B, _C (the open-top steel bin hung on its own 76 mm post), K2_hooded_drum_a,
_b, _c (the hooded glass-fibre drum, with its galvanised liner as a separate object), D1_dustbin_a, _b, _c (the galvanised household dustbin; in b the lid is a separate object
leaning off the bin). Millimetres in the script, metres in the .glb, z up. K1: the post axis at the origin on the flag top (a hidden skirt to z -150), the bin on +x (the engine
mirrors it for B2); K2 and D1: the base centre at the origin (+x is K2's aperture side). Geometric damage only where it is 5 mm or deeper (dents, the bent rim, the burnt hood's
hole, the lean and the tilt); the small dents, scuffs, chalk, rust, stickers, gum, scorch and the overflowing litter (a separate dressing set) are the engine's masks and
instances. The lettering (LITTER, LB n, the dustbin's number) is the engine's decal. Departures, each small: the dustbin is a solid of revolution closed at the rim (the sheet's 0.6 is not modelled; with its lid off a dark disc of contents stands under the rim), the K2 shell is 5 thick as the target says, the dents are a smooth bump, not a crease.
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
sys.path.insert(0, os.path.join(HERE, "..", "bollards"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import build_shopfront as bs  # noqa: E402
from build_railings import Parts, rrect  # noqa: E402
from build_bollards import lathe, prism_y  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "litter-bins", "target.json")
ASSET_DIR = os.path.join(REPO, "production", "assets", "cloud-week", "bins")
NPZ_DIR = os.path.join(HERE, "build")

BURN_AZ = -58.0              # the burnt hole's azimuth: the target's -28 would merge it with the aperture (now 230 wide), so it moves to the hood's upper left, clear of the aperture's edge
BIN_OFFSET = 232.0           # post axis to bin axis (TARGET-REVIEW fault 1: the target's 232): the rim bead stands 7 clear of the post
SIDES_K1, SIDES_K2, SIDES_D1 = 36, 34, 36


# ------------------------------------------------------------------------------------------------------------------------------------ helpers
def merge(*parts):
    Vs, Fs, k = [], [], 0
    for V, F in parts:
        V = np.asarray(V, float)
        Vs.append(V)
        Fs += [tuple(i + k for i in f) for f in F]
        k += len(V)
    return np.vstack(Vs), Fs


def volume(V, F):
    V = np.asarray(V, float)
    return sum(np.dot(V[f[0]], np.cross(V[f[i]], V[f[i + 1]])) / 6.0 for f in F for i in range(1, len(f) - 1))


def orient(V, F):
    return (V, F) if volume(V, F) >= 0 else (V, [tuple(f[::-1]) for f in F])


def revolve(sec_rz, n, cap=True):
    """a closed section (r, z) revolved about z: points on the axis collapse to one vertex per ring; the result is outward-facing"""
    P = [(float(r), float(z)) for r, z in sec_rz]
    m = len(P)
    V, idx = [], []
    for r, z in P:
        if r < 1e-6:
            V.append((0.0, 0.0, z))
            idx.append([len(V) - 1] * n)
        else:
            b = len(V)
            for k in range(n):
                a = 2 * math.pi * k / n
                V.append((r * math.cos(a), r * math.sin(a), z))
            idx.append(list(range(b, b + n)))
    F = []
    for i in range(m):
        j = (i + 1) % m
        for k in range(n):
            q = [idx[i][k], idx[i][(k + 1) % n], idx[j][(k + 1) % n], idx[j][k]]
            q = [x for t, x in enumerate(q) if x not in q[:t]]
            if len(q) >= 3:
                F.append(tuple(q))
    return orient(np.array(V), F)


def band(profile, t):
    """the closed section of a thin shell: the (r, z) outline from the foot to the crown and its offset t inward"""
    from shapely.geometry import LineString
    L = LineString([tuple(p) for p in profile])
    inner = L.offset_curve(-t if True else t, join_style=2, mitre_limit=2.0)
    ip = list(inner.coords)
    # the offset runs the other way round when it lands on the wrong side: take the one with the smaller radius at mid height
    mid = len(profile) // 2
    if np.mean([p[0] for p in ip]) > np.mean([p[0] for p in profile]):
        inner = L.offset_curve(t, join_style=2, mitre_limit=2.0)
        ip = list(inner.coords)
    if ip[0][1] > ip[-1][1]:
        ip = ip[::-1]
    ip = [(max(0.0, r), z) for r, z in ip]
    return [tuple(p) for p in profile] + ip[::-1]


def resample(profile, step):
    """add points along the long segments so that no segment is longer than step (so that a dent has vertices to move)"""
    out = [tuple(profile[0])]
    for a, b in zip(profile[:-1], profile[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        k = max(1, int(math.ceil(d / step)))
        for i in range(1, k + 1):
            out.append((a[0] + (b[0] - a[0]) * i / k, a[1] + (b[1] - a[1]) * i / k))
    return out


def dent(V, axis_xy, z0, az_deg, d, depth, radial_from=None):
    """a smooth inward bump: vertices within d/2 of the point (azimuth az about the axis, height z0) move toward the axis by depth * (1 - s^2)^2"""
    V = np.array(V, float)
    ax, ay = axis_xy
    rel = V[:, :2] - np.array([ax, ay])
    r = np.hypot(rel[:, 0], rel[:, 1])
    ang = np.degrees(np.arctan2(rel[:, 1], rel[:, 0]))
    da = (ang - az_deg + 180.0) % 360.0 - 180.0
    arc = np.radians(da) * np.maximum(r, 1.0)
    s = np.hypot(arc, V[:, 2] - z0) / (d / 2.0)
    w = np.where(s < 1.0, (1.0 - s * s) ** 2, 0.0)
    w = w * (r > 20.0)
    u = rel / np.maximum(r, 1e-9)[:, None]
    V[:, 0] -= u[:, 0] * depth * w
    V[:, 1] -= u[:, 1] * depth * w
    return V


def rot_y(V, deg, about_xz):
    """rotate about the y axis through (x, z) = about_xz (positive tilts the top toward +x)"""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    V = np.array(V, float)
    x, z = V[:, 0] - about_xz[0], V[:, 2] - about_xz[1]
    V[:, 0] = about_xz[0] + x * c + z * s
    V[:, 2] = about_xz[1] - x * s + z * c
    return V


def box3(x0, x1, y0, y1, z0, z1):
    V = np.array([(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)], float)
    F = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    return orient(V, F)


def cyl_z(x, y, z0, z1, r, n=16):
    V, F = lathe([(0.0, z0), (r, z0), (r, z1), (0.0, z1)], n)
    V = np.array(V)
    V[:, 0] += x
    V[:, 1] += y
    return V, F


def extrude_poly(poly_xy, z0, z1):
    """a prism of a convex-or-star polygon (x, y) from z0 to z1, built as a fan from its centroid (closed, outward-facing)"""
    P = np.array(poly_xy, float)
    c = P.mean(0)
    n = len(P)
    V = np.vstack([np.column_stack([P, np.full(n, z0)]), np.column_stack([P, np.full(n, z1)]), [[c[0], c[1], z0]], [[c[0], c[1], z1]]])
    F = []
    for i in range(n):
        j = (i + 1) % n
        F.append((i, j, n + j, n + i))
        F.append((2 * n, j, i))
        F.append((2 * n + 1, n + i, n + j))
    return orient(V, F)


def cyl_x(y, z, x0, x1, r, n=12):
    V, F = lathe([(0.0, x0), (r, x0), (r, x1), (0.0, x1)], n)
    V = np.array(V)
    out = np.stack([V[:, 2], V[:, 1] + y, V[:, 0] + z], 1)       # (r cos, r sin, along) -> (along, y, z)
    return orient(out, F)


def cyl_y(x, z, y0, y1, r, n=16):
    V, F = lathe([(0.0, y0), (r, y0), (r, y1), (0.0, y1)], n)
    V = np.array(V)
    out = np.stack([V[:, 0] + x, V[:, 2], V[:, 1] + z], 1)       # (r cos, r sin, along) -> (x, along, z)
    return orient(out, F)


def hex_y(x, z, y0, y1, af):
    pts = [(x + af / math.sqrt(3.0) * math.cos(math.radians(60 * j)), z + af / math.sqrt(3.0) * math.sin(math.radians(60 * j))) for j in range(6)]
    return orient(*prism_y(pts, y0, y1))


def dome_y(x, z, y_base, dy, r, n=12):
    """a rivet or bolt end: a cap of radius r and height dy standing from y_base toward +y (dy < 0: toward -y)"""
    prof = [(0.0, 0.0), (r, 0.0), (r * 0.92, abs(dy) * 0.45), (r * 0.6, abs(dy) * 0.85), (0.0, abs(dy))]
    V, F = lathe(prof, n)
    V = np.array(V)
    sgn = 1.0 if dy >= 0 else -1.0
    out = np.stack([V[:, 0] + x, y_base + sgn * V[:, 2], V[:, 1] + z], 1)
    return orient(out, F)


def dome_z(x, y, z_base, dz, r, n=10):
    """a rivet head of radius r and height |dz| standing from z_base toward +z (dz > 0) or -z"""
    prof = [(0.0, 0.0), (r, 0.0), (r * 0.92, abs(dz) * 0.45), (r * 0.6, abs(dz) * 0.85), (0.0, abs(dz))]
    V, F = lathe(prof, n)
    V = np.array(V)
    V[:, 2] = z_base + (1.0 if dz >= 0 else -1.0) * V[:, 2]
    V[:, 0] += x
    V[:, 1] += y
    return orient(V, F)


def sack(centre, w, d, h, n=14, rows=8, seed=3):
    """a black refuse sack: a lumpy squashed ellipsoid, closed (a separate object)"""
    rng = np.random.default_rng(seed)
    prof = []
    for i in range(rows + 1):
        a = math.pi * i / rows
        prof.append((math.sin(a), -math.cos(a)))
    V = []
    idx = []
    for i, (rr, zz) in enumerate(prof):
        if rr < 1e-6:
            V.append((centre[0], centre[1], centre[2] + zz * h / 2.0))
            idx.append([len(V) - 1] * n)
        else:
            b = len(V)
            for k in range(n):
                a = 2 * math.pi * k / n
                lump = 1.0 + 0.05 * math.sin(3 * a + i) + 0.015 * rng.standard_normal()
                V.append((centre[0] + rr * math.cos(a) * w / 2.0 * lump, centre[1] + rr * math.sin(a) * d / 2.0 * lump, centre[2] + zz * h / 2.0))
            idx.append(list(range(b, b + n)))
    F = []
    for i in range(rows):
        for k in range(n):
            q = [idx[i][k], idx[i][(k + 1) % n], idx[i + 1][(k + 1) % n], idx[i + 1][k]]
            q = [x for t, x in enumerate(q) if x not in q[:t]]
            if len(q) >= 3:
                F.append(tuple(q))
    return orient(np.array(V), F)


def irregular_prism_dir(poly_uv, centre, direction, depth0, depth1, rng=None):
    """a prism whose axis runs along direction (a unit xy vector with z 0), the polygon in (lateral, z): used for the burnt hole through a wall"""
    ux, uy = -direction[1], direction[0]
    V = []
    for d_ in (depth0, depth1):
        for u, z in poly_uv:
            V.append((centre[0] + direction[0] * d_ + ux * u, centre[1] + direction[1] * d_ + uy * u, z))
    m = len(poly_uv)
    F = [tuple(range(m))[::-1], tuple(range(m, 2 * m))]
    for i in range(m):
        j = (i + 1) % m
        F.append((i, j, m + j, m + i))
    return orient(np.array(V), F)


def mats_for(T, names):
    out = {}
    for nm, key in names.items():
        m = T["materials"][key]
        out[nm] = bs.make_material(nm, tuple(m["srgb"]), float(m["rough"]), float(m.get("metal", 0.0)))
    return out


# ------------------------------------------------------------------------------------------------------------------------------------ K1
def build_k1(T, cond, out_dir, npz_dir):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    K = T["kinds"]["K1"]
    C = K["conditions"][cond]
    Bn, Po, Br = K["bin"], K["post"], K["bracket"]
    mats = mats_for(T, {"paint_green": C["paint"], "zinc_galv": "zinc_new"})
    mats["bin_sack_black"] = bs.make_material("bin_sack_black", (18, 18, 20), 0.55, 0.0)
    B = Parts()
    parts = {}                                                          # name -> (V, F, mat, bevel, group)   group "post" or "bin"
    # the post: a tube with its pressed cap, a hidden skirt to -150
    pp = [(0.0, -150.0), (Po["od"] / 2.0, -150.0)] + [tuple(p) for p in Po["profile_rz"][2:]]
    V, F = lathe(pp, 20)
    parts["post"] = (V, F, "paint_green", None, "post")
    # the bin: the closed wall section revolved (the base plate with it), the rim bead in the profile; resampled so that the dents have vertices
    sec = resample([tuple(p) for p in Bn["wall_section_rz"]], 70.0)
    Vb, Fb = revolve(sec, SIDES_K1)
    Vb = np.array(Vb)
    Vb[:, 0] += BIN_OFFSET
    ax = (BIN_OFFSET, 0.0)
    for dd in C["dents"]:
        if dd["depth"] >= 5.0:
            Vb = dent(Vb, ax, dd["z"], dd["az"], dd["d"], dd["depth"])
    rd = C.get("rim_dent")
    if rd:                                                              # the rim bent in and down over its whole length (REVIEW-v1-street point 3): a cosine falloff, deepest at the middle
        span = rd["length"]
        rel = Vb[:, :2] - np.array(ax)
        ang = np.degrees(np.arctan2(rel[:, 1], rel[:, 0]))
        da = np.radians((ang - rd["az"] + 180.0) % 360.0 - 180.0)
        rr = np.maximum(np.hypot(rel[:, 0], rel[:, 1]), 1.0)
        arc = np.abs(da) * rr
        wz = np.where(arc < span / 2.0, 0.5 * (1.0 + np.cos(np.pi * arc / (span / 2.0))), 0.0)
        # the height weight: the rim's top 25 (the bead and the wall under it), fading to nothing by z 1010
        hz = np.clip((Vb[:, 2] - 1010.0) / 30.0, 0.0, 1.0)
        w = wz * hz
        u = rel / rr[:, None]
        Vb[:, 0] -= u[:, 0] * rd["depth"] * w
        Vb[:, 1] -= u[:, 1] * rd["depth"] * w
        Vb[:, 2] -= rd["depth"] * 0.4 * w
    # drain holes: four 8 mm holes in the base plate on r 100
    parts["bin"] = (Vb, Fb, "paint_green", None, "bin")
    # the back strap: a wedge bar from the post's face to the tapering wall, 40 wide, z 590 to 1030 (the wall's x at a height is BIN_OFFSET - r(z))
    def wall_x(z):
        return BIN_OFFSET - (165.0 + (180.5 - 165.0) * (z - 560.0) / (1038.0 - 560.0))
    xs0, xs1 = wall_x(Br["back_strap"]["z0"]) + 0.6, wall_x(Br["back_strap"]["z1"]) + 0.6
    xf = Br["back_strap"]["x_from"] - 0.55                              # the spacer bar: its post face on the clamp rings' outer face (x 43.05), 0.55 into them; its bin face on the wall
    st = [(xf, Br["back_strap"]["z0"]), (xs0, Br["back_strap"]["z0"]), (xs1, Br["back_strap"]["z1"]), (xf, Br["back_strap"]["z1"])]
    Vs, Fs = prism_y(st, -Br["back_strap"]["width"] / 2.0, Br["back_strap"]["width"] / 2.0)
    parts["strap"] = (Vs, Fs, "paint_green", 2.0, "bin")
    # the two clamps: a ring 40 x 5 round the post, an ear pair on the far side with one M8 bolt through, the nut on the other side
    for i, c in enumerate(Br["clamps"]):
        ring = revolve([(37.55, c["z0"]), (Po["od"] / 2.0 + c["ring_t"], c["z0"]), (Po["od"] / 2.0 + c["ring_t"], c["z1"]), (37.55, c["z1"])], 20)
        parts["clamp_%d" % i] = (ring[0], ring[1], "paint_green", 1.5, "bin")
        zc = (c["z0"] + c["z1"]) / 2.0
        # ears: two 12 thick plates on the far side (-x), 22 long, 40 high, 6 apart in y
        for sy in (-1.0, 1.0):
            ear = prism_y([(-37.0, c["z0"] + 2.0), (-60.0, c["z0"] + 2.0), (-60.0, c["z1"] - 2.0), (-37.0, c["z1"] - 2.0)], sy * 6.0 if sy > 0 else -18.0, 18.0 if sy > 0 else -6.0)
            parts["ear_%d_%s" % (i, "p" if sy > 0 else "m")] = (ear[0], ear[1], "paint_green", 1.5, "bin")
        bolt = cyl_y(-50.0, zc, -24.0, 24.0, 4.0, 12)
        parts["bolt_%d" % i] = (bolt[0], bolt[1], "paint_green", None, "bin")
        head = hex_y(-50.0, zc, 18.0, 26.0, 13.0)
        parts["bolthead_%d" % i] = (head[0], head[1], "paint_green", 0.8, "bin")
        nut = dome_y(-50.0, zc, -18.0, -8.0, 7.5, 12)
        parts["nut_%d" % i] = (nut[0], nut[1], "paint_green", None, "bin")
    # the tilt of the bin on its clamps and the lean of the post
    for nm, (V, F, mat, bev, grp) in parts.items():
        V = np.array(V, float)
        if grp == "bin" and C["bin_tilt_deg"]:
            V = rot_y(V, C["bin_tilt_deg"], (Po["od"] / 2.0, 640.0))
        if C["post_lean_deg"]:
            V = rot_y(V, -C["post_lean_deg"], (0.0, 0.0))                # the post leans toward the roadway side by its lean (-x here is the far side from the bin)
        parts[nm] = (V, F, mat, bev, grp)
    if C["liner_sack"]:
        # REVIEW-v1-street point 1: the sack fills the bin down to the floor, its mouth turns over the rim and hangs 120 outside (gathered), and it stands no more than 75 above the rim
        def r_in(z):
            return 165.0 + (K1["bin"]["r_top"] - 165.0) * (z - 560.0) / (1038.0 - 560.0) - 6.0
        prof_s = [(0.0, 1124.0), (70.0, 1118.0), (r_in(1050.0) - 14.0, 1100.0), (r_in(1050.0) - 4.0, 1070.0), (r_in(1050.0), 1050.0), (r_in(900.0), 900.0), (r_in(700.0), 700.0), (r_in(570.0), 570.0), (0.0, 566.0)]
        Vs_, Fs_ = revolve(prof_s, 24)
        Vs_ = np.array(Vs_)
        Vs_[:, 0] += BIN_OFFSET
        cuff = [(r_in(1050.0) + 4.0, 1046.0), (r_in(1050.0) + 4.0, 1058.0), (K1["bin"]["r_top"] + 8.0, 1058.0), (K1["bin"]["r_top"] + 8.0, 930.0), (K1["bin"]["r_top"] + 4.0, 930.0), (K1["bin"]["r_top"] + 4.0, 1052.0)]
        Vc_, Fc_ = revolve(cuff, 24)
        Vc_ = np.array(Vc_)
        a_c = np.arctan2(Vc_[:, 1], Vc_[:, 0])
        gath = 1.0 + 0.018 * np.sin(5.0 * a_c) + 0.008 * np.sin(11.0 * a_c + 1.0)               # the gathers
        rr_c = np.hypot(Vc_[:, 0], Vc_[:, 1])
        Vc_[:, 0], Vc_[:, 1] = rr_c * gath * np.cos(a_c) + BIN_OFFSET, rr_c * gath * np.sin(a_c)
        sk = merge((Vs_, Fs_), (Vc_, Fc_))
        V = np.array(sk[0])
        if C["bin_tilt_deg"]:
            V = rot_y(V, C["bin_tilt_deg"], (Po["od"] / 2.0, 640.0))
        if C["post_lean_deg"]:
            V = rot_y(V, -C["post_lean_deg"], (0.0, 0.0))
        parts["sack"] = (V, sk[1], "bin_sack_black", None, "bin")
    for nm, (V, F, mat, bev, grp) in parts.items():
        ob = B.add("k1_" + nm, (V, F), mat, bev=bev)
        if nm == "bin":
            for k_ in range(Bn["base_plate"]["drain_holes"]["count"]):
                a_ = math.radians(Bn["base_plate"]["drain_holes"]["first_azimuth"] + 90.0 * k_)
                r_ = Bn["base_plate"]["drain_holes"]["on_radius"]
                cx, cy = BIN_OFFSET + r_ * math.cos(a_), r_ * math.sin(a_)
                cv = cyl_z(cx, cy, 540.0, 560.0, Bn["base_plate"]["drain_holes"]["diameter"] / 2.0, 8)
                if C["bin_tilt_deg"] or C["post_lean_deg"]:
                    Vc = np.array(cv[0])
                    if C["bin_tilt_deg"]:
                        Vc = rot_y(Vc, C["bin_tilt_deg"], (Po["od"] / 2.0, 640.0))
                    if C["post_lean_deg"]:
                        Vc = rot_y(Vc, -C["post_lean_deg"], (0.0, 0.0))
                    cv = (Vc, cv[1])
                bs.bool_op(ob, cv[0], cv[1], "DIFFERENCE")
    obs = bs.finish(B, mats, 0.0)
    return bs.write(obs, "K1_pole_open_" + cond, 0.0, out_dir, npz_dir)


# ------------------------------------------------------------------------------------------------------------------------------------ K2
def build_k2(T, cond, out_dir, npz_dir):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    K = T["kinds"]["K2"]
    C = K["conditions"][cond]
    ap = K["aperture"]
    mats = mats_for(T, {"gel_green": C["gel"], "zinc_liner": "zinc_weathered"})
    mats["lock_steel"] = bs.make_material("lock_steel", (150, 150, 152), 0.45, 1.0)
    gpm = K["parts"]["ground_patch"]
    mats["cement_patch"] = bs.make_material("cement_patch", tuple(gpm["srgb"]), gpm["rough"], 0.0)
    B = Parts()
    prof = [tuple(p) for p in K["outer_profile_rz"]]
    sec = band(prof, K["shell"])
    # the shell: the outer profile and its inner offset, closed at the foot and the crown; resampled on the hood skirt for the aperture's corners
    sec = resample(sec, 40.0)
    V, F = revolve(sec, SIDES_K2)
    body = B.add("k2_shell", (V, F), "gel_green", bev=None)
    # the aperture through the hood skirt, on +x: a rounded rectangle, through the wall (a prism along x), its sill's return flange left to the normal map
    rr = [(p[0], (ap["sill_z"] + ap["top_z"]) / 2.0 + p[1]) for p in rrect(ap["width"], ap["top_z"] - ap["sill_z"], ap["corner_r"], 4)]
    Vp, Fp = prism_y(rr, 0.0, 300.0)                                    # lateral (x of the profile) and z; the extrusion along y
    Vp = np.array(Vp)
    Va, Fa = orient(np.stack([Vp[:, 1], Vp[:, 0], Vp[:, 2]], 1), Fp)    # turned so that the axis runs along +x: (x, y, z) = (extrusion, lateral, z)
    bs.bool_op(body, Va, Fa, "DIFFERENCE")
    # the burnt hood (condition c): an irregular hole melted through the skirt on the upper left, 115 x 85, at azimuth -28, z 770
    if C.get("burn"):
        bn = C["burn"]
        a_ = math.radians(BURN_AZ)
        dirv = (math.cos(a_), math.sin(a_))
        w_, h_ = bn["w"], bn["h"]
        rng = np.random.default_rng(11)
        poly = []
        for k in range(18):
            t = 2 * math.pi * k / 18
            rad = 1.0 + 0.16 * math.sin(3 * t + 0.6) + 0.07 * math.sin(5 * t)
            poly.append((math.cos(t) * w_ / 2.0 * rad, bn["z"] + 10.0 + math.sin(t) * h_ / 2.0 * rad))
        Vh, Fh = irregular_prism_dir(poly, (0.0, 0.0), dirv, 150.0, 300.0)
        bs.bool_op(body, Vh, Fh, "DIFFERENCE")
    # the barrel lock at the back of the join: an escutcheon 40 across, 4 proud, a 22 barrel, at azimuth 180, z 650 (a 2 mm slot cut across the barrel is the engine's normal map)
    lock = revolve([(0.0, -2.0), (20.0, -2.0), (20.0, 2.0), (11.0, 2.5), (11.0, 6.0), (0.0, 6.0)], 20)
    Vl = np.array(lock[0])
    Vl = np.stack([-(206.0 - 2.0 + Vl[:, 2]), Vl[:, 1], K["parts"]["lock"]["z"] + Vl[:, 0]], 1)    # the disc's axis along -x, 4 proud of the groove's r 206 at z 640
    B.add("k2_lock", (Vl, lock[1]), "lock_steel", bev=None)
    # the liner (a separate object): a galvanised sheet can with a rolled rim, 1.6 thick here
    lp = [tuple(p) for p in K["parts"]["liner"]["profile_rz"]]
    lsec = band(lp, 1.6)
    Vq, Fq = revolve(resample(lsec, 60.0), 40)
    B.add("k2_liner", (Vq, Fq), "zinc_liner", bev=None)
    # the cement patch the photographed bin stands on (TARGET-REVIEW fault 6): an irregular flush disc r 290 to 330, seeded, its top 1 over the flag, a separate object
    gp = K["parts"]["ground_patch"]
    prng = np.random.default_rng(12)
    ang = np.linspace(0.0, 2 * math.pi, 28, endpoint=False)
    rad = [float(gp["r"][0] + (gp["r"][1] - gp["r"][0]) * (0.5 + 0.5 * math.sin(3 * a + 0.7) * 0.8 + 0.2 * prng.standard_normal())) for a in ang]
    rad = [min(max(r, gp["r"][0]), gp["r"][1]) for r in rad]
    pv = extrude_poly([(r * math.cos(a), r * math.sin(a)) for r, a in zip(rad, ang)], -4.0, 1.0)
    B.add("k2_ground_patch", pv, "cement_patch", bev=None)
    obs = bs.finish(B, mats, 0.0)
    return bs.write(obs, "K2_hooded_drum_" + cond, 0.0, out_dir, npz_dir)


# ------------------------------------------------------------------------------------------------------------------------------------ D1
def build_d1(T, cond, out_dir, npz_dir):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    K = T["kinds"]["D1"]
    C = K["conditions"][cond]
    mats = mats_for(T, {"zinc": "zinc_weathered" if cond != "c" else "zinc_worn_dirty"})
    mats["bin_sack_black"] = bs.make_material("bin_sack_black", (18, 18, 20), 0.55, 0.0)
    mats["zinc_new"] = bs.make_material("zinc_new", tuple(T["materials"]["zinc_new"]["srgb"]), float(T["materials"]["zinc_new"]["rough"]), 1.0)
    B = Parts()
    prof = [tuple(p) for p in K["outer_profile_rz"]]
    t = 1.5
    # the body: a solid of revolution closed at the rim (the sheet's thickness is not modelled: 0.6 mm); where the lid is off (b) a dark disc of contents stands just under the rim
    V, F = lathe(resample(prof, 45.0), SIDES_D1)
    V, F = orient(np.array(V), F)
    V = np.array(V)
    rng = np.random.default_rng(1990 + ord(cond))
    n_d = int(C["dents"])
    for k in range(n_d):
        V = dent(V, (0.0, 0.0), float(rng.uniform(70, 540)), float(rng.uniform(0, 360)), float(rng.uniform(55, 110)), float(rng.uniform(3.0, 6.5 if cond == "c" else 5.0)))
    B.add("d1_body", (V, F), "zinc", bev=None)
    if cond == "b":
        cv = lathe([(0.0, 603.5), (221.0, 603.5), (221.0, 604.5), (0.0, 604.5)], 24)
        B.add("d1_contents", orient(np.array(cv[0]), cv[1]), "bin_sack_black", bev=None)
    # the lid: a pressed dome with its skirt (a shell 1.5 thick), a flat strap handle on its crown with two rivets
    lp = [tuple(p) for p in K["lid"]["profile_rz"]]
    lsec = band(lp, t)
    Vl, Fl = revolve(lsec, SIDES_D1)
    Vl = np.array(Vl)
    hw, ht, hl, hr = K["lid"]["handle"]["strap_w"], K["lid"]["handle"]["strap_t"], K["lid"]["handle"]["length"], K["lid"]["handle"]["rise"]
    arch = [(-hl / 2.0, 641.0 - 3.0), (-hl / 2.0 + 8.0, 641.0 + hr * 0.8), (-hl / 2.0 + 22.0, 641.0 + hr), (hl / 2.0 - 22.0, 641.0 + hr), (hl / 2.0 - 8.0, 641.0 + hr * 0.8), (hl / 2.0, 641.0 - 3.0),
            (hl / 2.0 - 5.0, 641.0 - 3.0), (hl / 2.0 - 13.0, 641.0 + hr - ht), (hl / 2.0 - 24.0, 641.0 + hr - ht), (-hl / 2.0 + 24.0, 641.0 + hr - ht), (-hl / 2.0 + 13.0, 641.0 + hr - ht), (-hl / 2.0 + 5.0, 641.0 - 3.0)]
    Vh, Fh = prism_y([(x, z) for x, z in arch], -hw / 2.0, hw / 2.0)
    riv = [dome_y(sx * (hl / 2.0 - 3.0), 641.0, hw / 2.0, 3.0, 4.0, 10) for sx in (-1.0, 1.0)] + [dome_y(sx * (hl / 2.0 - 3.0), 641.0, -hw / 2.0, -3.0, 4.0, 10) for sx in (-1.0, 1.0)]
    lid = merge((Vl, Fl), (Vh, Fh), *riv)
    LV = np.array(lid[0])
    if cond == "b":
        # off the bin, leaning against the wall: a separate object stood on its skirt edge at x 330, tilted 72 degrees from the horizontal, its top edge toward the bin
        LV = LV.copy()
        LV[:, 2] -= 588.0
        a = math.radians(72.0)
        c, s = math.cos(a), math.sin(a)
        x, z = LV[:, 0].copy(), LV[:, 2].copy()
        LV[:, 0] = x * c - z * s
        LV[:, 2] = x * s + z * c
        LV[:, 2] -= LV[:, 2].min()
        it = int(np.argmax(LV[:, 2]))                                         # its top edge rests against the can's wall (REVIEW-v1-street point 4)
        zt = float(LV[it, 2])
        LV[:, 0] += (199.0 + 25.0 * (min(zt, 560.0) - 28.0) / (582.0 - 28.0) + 3.0) - LV[it, 0]
    elif C.get("lid_tilt_deg"):
        LV = rot_y(LV, C["lid_tilt_deg"], (231.0, 588.0))
    B.add("d1_lid", (LV, lid[1]), "zinc", bev=None)
    # the two side handles (TARGET-REVIEW fault 3): a horizontal 12 mm round-bar grip 170 long standing 38 proud, bent down at each end into a lug 25 x 55 x 3 held by two 8 mm
    # dome rivets one above the other (40 apart), at z 470 on the +-y sides
    sh = K["side_handles"]
    r_h = 199.0 + 25.0 * (sh["z"] - 28.0) / (582.0 - 28.0)           # the body's radius at the handles' height (the target's taper)
    half = sh["length"] / 2.0
    yb = r_h + sh["proud"] - sh["bar_d"] / 2.0                 # the bar's axis: its outer face stands `proud` from the body's surface at the middle
    for sgn in (1.0, -1.0):
        ys = math.sqrt(r_h * r_h - half * half)                # the body's surface at the lug's x
        parts = [cyl_x(sgn * yb, sh["z"], -half - 3.0, half + 3.0, sh["bar_d"] / 2.0, 12)]
        for sx in (-1.0, 1.0):
            lug = box3(sx * half - sh["strap_w"] / 2.0, sx * half + sh["strap_w"] / 2.0, min(sgn * (ys - 2.0), sgn * (ys + sh["strap_t"])), max(sgn * (ys - 2.0), sgn * (ys + sh["strap_t"])), sh["z"] - sh["height"] / 2.0, sh["z"] + sh["height"] / 2.0)
            parts.append(lug)
            parts.append(cyl_y(sx * half, sh["z"], min(sgn * (ys + sh["strap_t"] - 0.5), sgn * yb), max(sgn * (ys + sh["strap_t"] - 0.5), sgn * yb), sh["bar_d"] / 2.0, 12))
        B.add("d1_handle_%s" % ("p" if sgn > 0 else "m"), merge(*parts), "zinc", bev=None)
        for sx in (-1.0, 1.0):
            for dz in (-sh["rivet_pitch"] / 2.0, sh["rivet_pitch"] / 2.0):
                rv = dome_y(sx * half, sh["z"] + dz, sgn * (ys + sh["strap_t"]), sgn * 3.0, sh["rivet_d"] / 2.0, 10)
                B.add("d1_rivet_%d_%d_%d" % (int(sgn), int(dz), int(sx)), rv, "zinc", bev=None)
    obs = bs.finish(B, mats, 0.0)
    return bs.write(obs, "D1_dustbin_" + cond, 0.0, out_dir, npz_dir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="K1,K2,D1")
    ap.add_argument("--out-dir", default=ASSET_DIR)
    ap.add_argument("--npz-dir", default=NPZ_DIR)
    a = ap.parse_args()
    T = json.load(open(TARGET_JSON, encoding="utf-8"))
    os.makedirs(a.npz_dir, exist_ok=True)
    pj = os.path.join(a.npz_dir, "parts.json")
    res = json.load(open(pj)) if os.path.exists(pj) else {}
    for kind in a.only.split(","):
        conds = ("A", "B", "C") if kind == "K1" else ("a", "b", "c")
        for c in conds:
            fn = {"K1": build_k1, "K2": build_k2, "D1": build_d1}[kind]
            r = fn(T, c, a.out_dir, a.npz_dir)
            nm = {"K1": "K1_pole_open_", "K2": "K2_hooded_drum_", "D1": "D1_dustbin_"}[kind] + c
            res[nm] = r
            print(nm, "triangles", r["triangles"], "glb bytes", r["glb_bytes"], flush=True)
    json.dump(res, open(pj, "w"), indent=1)


if __name__ == "__main__":
    main()
