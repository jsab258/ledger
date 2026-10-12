"""Quay Street's kerbs, channel, crossover, gully grates and covers (kerbs-and-covers target; cloud week 42, unit 3.7), built by script from target.json.

    /home/user/.bpyenv/bin/python build_kerbs.py [--out-dir DIR] [--npz-dir DIR]

One .glb per piece, metres, z up, scale 1, in the target's frame: x along the kerb, y across (0 = the kerb face line at the channel, + toward the carriageway, the block's
back at y -170), z up from the top of the channel setts (the kerb top at +115); the pivot of a kerb block is its centre on the face line at channel level, of the crossing
the middle of the gap between its two end blocks, of a grate or a cover the centre of the lid at its top surface (z 0). The cast patterns carry no lettering and no maker's mark
(the target's no_lettering); the colour variants, the wear and the tyre and weed states are the engine's (materials by name; masks in unit 4.5).

Built: kerb_granite, kerb_concrete, channel_setts (a 1.2 m run of the two courses), channel_concrete, crossover_A (end blocks, flank strips, ramp, the row of 19 setts as the lip),
gully_grate_A (the street's) and gully_grate_B, cover_stud_square, cover_round_600, cover_recessed_footway, cover_recessed_road, cover_road_double_leaf, service_stopcock,
service_gas, service_telecom. Not built (the target itself leaves them out of today's street): the two kerb corners, the taper (dropper) variant, tactile paving (none in 1990).
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box as sbox, Point
from shapely.geometry.polygon import orient as sorient
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shopfront"))
sys.path.insert(0, os.path.join(HERE, "..", "railings"))
sys.path.insert(0, os.path.join(HERE, "..", "bollards"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import build_shopfront as bs  # noqa: E402
from build_railings import Parts, rrect, prism_x  # noqa: E402
from build_bollards import lathe, prism_y  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "kerbs-and-covers", "target.json")
ASSET_DIR = os.path.join(REPO, "production", "assets", "cloud-week", "kerbs-covers")
NPZ_DIR = os.path.join(HERE, "build")


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


def extrude(poly, z0, z1):
    """a shapely polygon (holes allowed) as a closed prism from z0 to z1; caps by constrained Delaunay"""
    import shapely
    poly = sorient(poly, 1.0)
    rings = [list(poly.exterior.coords)[:-1]] + [list(r.coords)[:-1] for r in poly.interiors]
    index, V = {}, []
    for ri, ring in enumerate(rings):
        for p in ring:
            for z in (z0, z1):
                index[(round(p[0], 4), round(p[1], 4), z)] = len(V)
                V.append((p[0], p[1], z))
    F = []
    for ring in rings:
        n = len(ring)
        for i in range(n):
            a, b = ring[i], ring[(i + 1) % n]
            ka0, kb0 = index[(round(a[0], 4), round(a[1], 4), z0)], index[(round(b[0], 4), round(b[1], 4), z0)]
            ka1, kb1 = index[(round(a[0], 4), round(a[1], 4), z1)], index[(round(b[0], 4), round(b[1], 4), z1)]
            F.append((ka0, kb0, kb1, ka1))
    for tri in shapely.constrained_delaunay_triangles(poly).geoms:
        c = list(tri.exterior.coords)[:-1]
        t = Polygon(c)
        ids1 = [index[(round(p[0], 4), round(p[1], 4), z1)] for p in c]
        ids0 = [index[(round(p[0], 4), round(p[1], 4), z0)] for p in c]
        if not t.exterior.is_ccw:
            ids1, ids0 = ids1[::-1], ids0[::-1]
        F.append(tuple(ids1))
        F.append(tuple(ids0[::-1]))
    return orient(np.array(V), F)


def box3(x0, x1, y0, y1, z0, z1):
    return extrude(sbox(x0, y0, x1, y1), z0, z1)


def cyl_z(cx, cy, z0, z1, r, n=24):
    ang = np.linspace(0.0, 2 * math.pi, n, endpoint=False)
    return extrude(Polygon([(cx + r * math.cos(a), cy + r * math.sin(a)) for a in ang]), z0, z1)


def ring_solid(sect_rz, n=96):
    """a closed (r, z) section swept all the way round the z axis (an annulus: no apex, no caps)"""
    P = np.asarray(sect_rz, float)
    m = len(P)
    V = []
    for k in range(n):
        a = 2 * math.pi * k / n
        for r, z in P:
            V.append((r * math.cos(a), r * math.sin(a), z))
    F = []
    for k in range(n):
        k2 = (k + 1) % n
        for i in range(m):
            j = (i + 1) % m
            F.append((k * m + i, k2 * m + i, k2 * m + j, k * m + j))
    return orient(np.array(V), F)


def rot(poly, deg):
    return affinity.rotate(poly, deg, origin=(0, 0))


def mats_for(T):
    M = T["materials"]
    out = {}
    for k, v in M.items():
        if isinstance(v, dict) and "srgb" in v:
            out[k] = bs.make_material(k, v["srgb"], v.get("roughness", 0.7), float(v.get("metal", 0)))
    out["pot_black"] = bs.make_material("pot_black", (8, 8, 8), 0.9, 0.0)
    return out


# ------------------------------------------------------------------------------------------------------------------------------------ the kerb blocks and the channel
def kerb_block(P, length, B, mat, bev, name="block"):
    V, F = prism_x([tuple(p) for p in P["section_yz"]], -length / 2.0, length / 2.0)
    B.add(name, orient(V, F), mat, bev=bev, min_angle=60.0)


def setts_run(P, B, rng, x0, x1, name_prefix="sett", along=(120.0, 210.0), joint=11.0, courses=None):
    """two courses of setts, long side along the kerb, in running bond: each a domed prism (4 mm of dome), the tops scattering 3 mm and the far course up to 5 lower where worn"""
    courses = courses or [("A", 0.0, 104.0), ("B", 104.0, 204.0)]
    mats = ["sett_pale_worn", "sett_dull", "granite_blue_grey"]
    share = [0.35, 0.5, 0.15]
    out = {m: [] for m in mats}
    joints_a = []                                                                  # course A's joint positions: course B's must not fall within 40 of one (running bond, REVIEW-v1-street)
    for ci, (nm, y0, y1) in enumerate(courses):
        x = x0 - (0.0 if ci == 0 else float(rng.uniform(40.0, 90.0)))
        while x < x1:
            L = float(rng.uniform(*along))
            if ci == 1:
                for _ in range(40):
                    if all(abs((x + L + joint / 2.0) - ja) > 40.0 for ja in joints_a):
                        break
                    L = float(rng.uniform(*along))
            else:
                joints_a.append(x + L + joint / 2.0)
            xa, xb = max(x, x0), min(x + L, x1)
            if xb - xa > 20.0:
                dz = -float(rng.uniform(0.0, 3.0)) - (float(rng.uniform(0.0, 5.0)) if (ci == 1 and rng.random() < 0.3) else 0.0)
                ym = (y0 + y1) / 2.0
                sect = [(y0 + 0.5, -140.0), (y1 - 0.5, -140.0), (y1 - 0.5, -4.0 + dz), (ym, 0.0 + dz), (y0 + 0.5, -4.0 + dz)]
                m = mats[int(rng.choice(3, p=share))]
                out[m].append(prism_x(sect, xa + 0.5, xb - 0.5))
            x += L + joint
    for m, parts in out.items():
        if parts:
            B.add("%s_%s" % (name_prefix, m), orient(*merge(*parts)), m, bev=1.5, min_angle=60.0)


def piece_kerb_granite(T, B):
    kerb_block(T["pieces"]["kerb_granite"], 900.0, B, "granite_grey", bev=10.0)


def piece_kerb_concrete(T, B):
    kerb_block(T["pieces"]["kerb_concrete"], 915.0, B, "concrete_kerb", bev=3.0)


def piece_channel_setts(T, B):
    P = T["pieces"]["channel_setts"]
    rng = np.random.default_rng(1990)
    setts_run(P, B, rng, -600.0, 600.0)
    B.add("mortar", box3(-599.0, 599.0, 1.0, 203.0, -141.0, -8.0), "bitumen_joint", bev=None)          # the recessed dark mortar: 8 under the setts' tops


def piece_channel_concrete(T, B):
    P = T["pieces"]["channel_concrete"]
    B.add("block", prism_x([tuple(p) for p in P["section_yz"]], -P["length_mm"] / 2.0, P["length_mm"] / 2.0), "concrete_kerb", bev=3.0, min_angle=60.0)


# ------------------------------------------------------------------------------------------------------------------------------------ the crossover
def piece_crossover(T, B):
    P = T["pieces"]["crossover"]
    K = T["pieces"]["kerb_granite"]
    W = P["width_between_kerb_ends"] / 2.0                               # 1500
    rng = np.random.default_rng(22)
    for sx in (-1.0, 1.0):
        xa, xb = (W, W + 900.0) if sx > 0 else (-W - 900.0, -W)
        V, F = prism_x([tuple(p) for p in K["section_yz"]], xa, xb)
        B.add("end_block_%s" % ("r" if sx > 0 else "l"), orient(V, F), "granite_grey", bev=8.0, min_angle=60.0)
    fl = P["flank_strips"]
    for sx in (-1.0, 1.0):
        xa, xb = (W, W + fl["width_mm"]) if sx > 0 else (-W - fl["width_mm"], -W)
        B.add("flank_%s" % ("r" if sx > 0 else "l"), box3(xa, xb, fl["plan_y"][0], fl["plan_y"][1], -100.0, fl["top_z"]), "granite_grey", bev=3.0, min_angle=60.0)
    rp = P["ramp"]
    sect = [(rp["plan_y"][1], -120.0), (rp["plan_y"][1], rp["z_at_lip"]), (rp["plan_y"][0], rp["z_at_back"]), (rp["plan_y"][0], -120.0)]
    sect = [(-124.0, -120.0), (-124.0, rp["z_at_lip"]), (-845.0, rp["z_at_back"]), (-845.0, -120.0)]
    B.add("ramp", orient(*prism_x(sect, rp["plan_x"][0], rp["plan_x"][1])), "concrete_ramp", bev=None)
    lip = P["lip_row"]
    n = int(math.ceil(P["width_between_kerb_ends"] / (lip["sett_along_mm"] + lip["joint_mm"])))
    pitch = P["width_between_kerb_ends"] / n
    parts = {"granite_blue_grey": [], "granite_grey": [], "granite_pink_grey": []}
    for i in range(n):
        xa = -W + i * pitch + lip["joint_mm"] / 2.0
        xb = -W + (i + 1) * pitch - lip["joint_mm"] / 2.0
        m = "granite_pink_grey" if (i % 8 == 5) else ("granite_grey" if i % 3 == 1 else "granite_blue_grey")
        sect = [(lip["y0"], -140.0), (0.0, -140.0), (0.0, lip["top_z"] - 1.5), (-3.0, lip["top_z"]), (lip["y0"] + 3.0, lip["top_z"]), (lip["y0"], lip["top_z"] - 1.5)]
        parts[m].append(prism_x(sect, xa, xb))
    for m, ps in parts.items():
        if ps:
            B.add("lip_%s" % m, orient(*merge(*ps)), m, bev=1.0, min_angle=60.0)


# ------------------------------------------------------------------------------------------------------------------------------------ the gully grates
def grate_plate(L, Wd, depth, slots, B, mat="cast_iron_grate", name="grate", taper=2.0, holes=()):
    """a plate L along the kerb x Wd across, `depth` thick, its top at z 0, with tapered slots (top wide, 4 narrower at the bottom): slots = [(cx, cy, w, length)]"""
    V, F = box3(-L / 2.0, L / 2.0, -Wd / 2.0, Wd / 2.0, -depth, 0.0)
    ob = B.add(name, (V, F), mat, bev=None)
    for cx, cy, w, ln in slots:
        top = sbox(cx - w / 2.0, cy - ln / 2.0, cx + w / 2.0, cy + ln / 2.0)
        bot = sbox(cx - w / 2.0 + taper, cy - ln / 2.0 + taper, cx + w / 2.0 - taper, cy + ln / 2.0 - taper)
        a, b = extrude(top, -depth * 0.35, 1.0), extrude(bot, -depth - 1.0, -depth * 0.35)
        bs.bool_op(ob, *a, "DIFFERENCE")
        bs.bool_op(ob, *b, "DIFFERENCE")
    for cx, cy, d in holes:
        bs.bool_op(ob, *cyl_z(cx, cy, -depth - 1.0, 1.0, d / 2.0, 18), "DIFFERENCE")
    return ob


def gully_pot(L, Wd, B, depth=300.0, top=-45.0):
    outer = extrude(sbox(-L / 2.0 + 20.0, -Wd / 2.0 + 20.0, L / 2.0 - 20.0, Wd / 2.0 - 20.0), top - depth, top)
    ob = B.add("pot", outer, "pot_black", bev=None)
    bs.bool_op(ob, *extrude(sbox(-L / 2.0 + 30.0, -Wd / 2.0 + 30.0, L / 2.0 - 30.0, Wd / 2.0 - 30.0), top - depth + 15.0, top + 1.0), "DIFFERENCE")


def piece_gully_A(T, B):
    P = T["pieces"]["gully_grate_A"]
    slots = [(cx, 0.0, P["slot_width"], P["slot_length"]) for cx in P["slot_centres_x"]]
    grate_plate(P["overall_along_kerb"], P["overall_across"], P["bar_depth_z"], slots, B)
    gully_pot(P["overall_along_kerb"], P["overall_across"], B)


def piece_gully_B(T, B):
    P = T["pieces"]["gully_grate_B"]
    n = P["slot_count"]
    xs = [(i - (n - 1) / 2.0) * P["slot_pitch"] for i in range(n)]
    slots = [(x, 0.0, P["slot_width"], ln) for x, ln in zip(xs, P["slot_lengths"])]
    h = P["lifting_holes"]
    holes = [(sx * (xs[-1] + h["beyond_end_slot_centres_mm"]), 0.0, h["diameter"]) for sx in (-1.0, 1.0)]
    grate_plate(P["overall_along_kerb"], P["overall_across"], 45.0, slots, B, holes=holes)
    gully_pot(P["overall_along_kerb"], P["overall_across"], B)


# ------------------------------------------------------------------------------------------------------------------------------------ the covers
def lattice_studs(leaf, stud, pitch, nx, ny, rot_deg=0.0, shrink=0.0):
    """square studs on a lattice (nx x ny, centred), clipped to the leaf: the studs the joint crosses are cut to half-studs"""
    out = []
    c0 = -(nx - 1) / 2.0
    r0 = -(ny - 1) / 2.0
    for i in range(nx):
        for j in range(ny):
            cx, cy = (c0 + i) * pitch, (r0 + j) * pitch
            s = sbox(cx - stud / 2.0, cy - stud / 2.0, cx + stud / 2.0, cy + stud / 2.0)
            if rot_deg:
                s = rot(s, rot_deg)
            g = s.intersection(leaf.buffer(-shrink))
            if not g.is_empty and g.area > 4.0:
                for gg in (g.geoms if hasattr(g, "geoms") else [g]):
                    if gg.geom_type == "Polygon" and gg.area > 4.0:
                        out.append(gg)
    return out


def piece_cover_stud(T, B):
    P = T["pieces"]["cover_stud_square"]
    o, r = P["outer"][0] / 2.0, P["frame_rim"]
    li = o - r
    frame = sbox(-o, -o, o, o).difference(sbox(-li, -li, li, li))
    B.add("frame", extrude(frame, -40.0, 0.0), "cast_iron_cover", bev=1.5, min_angle=60.0)
    jt = P["leaves"]["joint_mm"] / 2.0
    d = jt * math.sqrt(2.0)
    big = sbox(-li + 1.0, -li + 1.0, li - 1.0, li - 1.0)
    diag = Polygon([(-2 * li, -2 * li - d), (2 * li, 2 * li - d), (2 * li, 2 * li + d), (-2 * li, -2 * li + d)])
    leaves = big.difference(diag)
    parts = list(leaves.geoms)
    st = P["pattern"]
    studs, leafv = [], []
    for k, lf in enumerate(sorted(parts, key=lambda g: g.centroid.x)):
        leafv.append(extrude(lf, -20.0, 0.0))
        studs += [extrude(g, -0.5, st["stud_height_mm"]) for g in lattice_studs(lf, st["stud_mm"], st["pitch_mm"], st["count"][0], st["count"][1], 0.0, 1.0)]
    lv = B.add("lid_leaves", orient(*merge(*leafv)), "cast_iron_cover", bev=None)
    kh = P["keyhole_diameter_mm"] / 2.0
    cents = sorted(parts, key=lambda g: g.centroid.x)
    for g in cents:
        c = g.centroid
        bs.bool_op(lv, *cyl_z(c.x, c.y, -21.0, 1.0, kh, 16), "DIFFERENCE")
    B.add("studs", orient(*merge(*studs)), "cast_iron_cover", bev=None)
    bo = P["boss"]["size_mm"]
    bx, by = -li * 0.62, -li * 0.62
    bpoly = affinity.translate(rot(sbox(-bo[0] / 2.0, -bo[1] / 2.0, bo[0] / 2.0, bo[1] / 2.0), 45.0), bx, by)
    B.add("boss", extrude(bpoly, -0.3, P["boss"]["height_mm"]), "cast_iron_cover", bev=None)


def basket_lugs(clip, cell=(71.4, 83.5), lug=(36.0, 10.5)):
    """the basket-lug tread: per cell two horizontal and two vertical lugs, rows shifted 35.7 (the target's pattern 2)"""
    out = []
    cx0, cy0 = cell
    rx, ry = clip.bounds[2], clip.bounds[3]
    nx, ny = int(math.ceil(rx / cx0)) + 1, int(math.ceil(ry / cy0)) + 1
    lugs = [((0.0, 0.0), 0), ((35.7, 41.75), 0), ((35.7, 6.0), 90), ((0.0, 47.75), 90)]
    for i in range(-nx, nx + 1):
        for j in range(-ny, ny + 1):
            for (dx, dy), ori in lugs:
                x, y = i * cx0 + dx, j * cy0 + dy
                w, h = (lug[0], lug[1]) if ori == 0 else (lug[1], lug[0])
                s = sbox(x - w / 2.0, y - h / 2.0, x + w / 2.0, y + h / 2.0)
                if clip.contains(s):
                    out.append(s)
    return out


def piece_cover_round(T, B):
    P = T["pieces"]["cover_round_600"]
    ro, ri, dep = P["frame_outer_diameter"] / 2.0, P["lid_diameter"] / 2.0, P["frame_depth"]
    B.add("frame", ring_solid([(ri + 0.5, -dep), (ro, -dep), (ro, 0.0), (ri + 0.5, 0.0)], 96), "cast_iron_cover", bev=None)
    lv, lf = lathe([(0.0, -22.0), (ri - 0.5, -22.0), (ri - 0.5, 0.0), (0.0, 0.0)], 96)
    B.add("lid", orient(lv, lf), "cast_iron_cover", bev=None)
    clip = Point(0, 0).buffer(ri - P["pattern"]["rim_plain_mm"], resolution=24)
    lugs = basket_lugs(clip)
    B.add("lugs", orient(*merge(*[extrude(g, -0.5, P["pattern"]["lug_height_mm"]) for g in lugs])), "cast_iron_cover", bev=None)


def piece_cover_footway(T, B):
    P = T["pieces"]["cover_recessed_footway"]
    ow, oh = P["outer"][0] / 2.0, P["outer"][1] / 2.0
    fl, lg, step = P["frame_flange_mm"], P["frame_ledge_mm"], P["ledge_step_mm"]
    flange = sbox(-ow, -oh, ow, oh).difference(sbox(-ow + fl, -oh + fl, ow - fl, oh - fl))
    ledge = sbox(-ow + fl, -oh + fl, ow - fl, oh - fl).difference(sbox(-ow + fl + lg, -oh + fl + lg, ow - fl - lg, oh - fl - lg))
    B.add("frame_flange", extrude(flange, -60.0, 0.0), "cast_iron_cover", bev=1.5, min_angle=60.0)
    B.add("frame_ledge", extrude(ledge, -60.0, -step), "cast_iron_cover", bev=1.0, min_angle=60.0)
    iw, ih = P["infill"][0] / 2.0, P["infill"][1] / 2.0
    ch = P["infill_chamfer_mm"]
    infill_top = -8.0
    # the tray lid: its top edge chamfered 22 (a stepped section keeps it a plain prism pair)
    B.add("infill", orient(*merge(extrude(sbox(-iw, -ih, iw, ih), -40.0, infill_top - ch * 0.5), extrude(sbox(-iw + ch, -ih + ch, iw - ch, ih - ch), infill_top - ch * 0.5 - 0.5, infill_top))), "flag_pale", bev=None)
    lg_ = P["frame_lugs"]
    lw, lh = lg_["lug_mm"]
    lugs = []
    for k in range(int((2 * ow - 2 * fl) // 71.4)):
        x = -ow + fl + 40.0 + k * 71.4
        for sy in (-1.0, 1.0):
            lugs.append(sbox(x - lw / 2.0, sy * (oh - fl / 2.0) - lh / 2.0, x + lw / 2.0, sy * (oh - fl / 2.0) + lh / 2.0))
            xs = x + 35.7
            if xs < ow - fl - 40.0:
                lugs.append(sbox(xs - lw / 2.0, sy * (oh - fl - lg / 2.0) - lh / 2.0, xs + lw / 2.0, sy * (oh - fl - lg / 2.0) + lh / 2.0))
    for col, sx, count in ((0, -1.0, 3), (1, 1.0, 2)):
        for c in range(count):
            x = sx * (ow - fl / 2.0 - c * 14.0) if c == 0 else sx * (ow - fl - 18.0 - (c - 1) * 15.0)
            for k in range(int((2 * oh - 2 * fl - 60.0) // 41.75)):
                y = -oh + fl + 40.0 + k * 41.75
                lugs.append(sbox(x - lh / 2.0, y - lw / 2.0, x + lh / 2.0, y + lw / 2.0))
    B.add("lugs", orient(*merge(*[extrude(g, -0.5, lg_["height_mm"]) for g in lugs])), "cast_iron_cover", bev=None)


def piece_cover_road(T, B):
    P = T["pieces"]["cover_recessed_road"]
    ow, oh = P["outer"][0] / 2.0, P["outer"][1] / 2.0
    rim, hl = P["frame_rim"], P["hairline_mm"]
    frame = sbox(-ow, -oh, ow, oh).difference(sbox(-ow + rim, -oh + rim, ow - rim, oh - rim))
    B.add("frame", extrude(frame, -40.0, 0.0), "cast_iron_cover", bev=1.0, min_angle=60.0)
    B.add("infill", extrude(sbox(-ow + rim + hl, -oh + rim + hl, ow - rim - hl, oh - rim - hl), -40.0, -1.0), "tarmac_infill", bev=None)


def piece_cover_double_leaf(T, B):
    P = T["pieces"]["cover_road_double_leaf"]
    ow, oh = P["outer"][0] / 2.0, P["outer"][1] / 2.0
    rim = 20.0
    frame = sbox(-ow, -oh, ow, oh).difference(sbox(-ow + rim, -oh + rim, ow - rim, oh - rim))
    B.add("frame", extrude(frame, -40.0, 0.0), "cast_iron_cover", bev=1.5, min_angle=60.0)
    gap = P["leaf_split"].count("15") and 15.0
    li, lw = ow - rim, oh - rim
    leaves = [sbox(-li + 1.0, -lw + 1.0, -gap / 2.0, lw - 1.0), sbox(gap / 2.0, -lw + 1.0, li - 1.0, lw - 1.0)]
    B.add("lid_leaves", orient(*merge(*[extrude(g, -22.0, 0.0) for g in leaves])), "cast_iron_cover", bev=None)
    st = P["pattern"]
    studs = []
    n = int(math.ceil(max(li, lw) * 1.6 / st["pitch_mm"]))
    p = st["pitch_mm"] / math.sqrt(2.0)                                                  # a square lattice of pitch 31 turned 45 degrees: points at ((i - j) p, (i + j) p)
    hd = st["stud_mm"] * math.sqrt(2.0) / 2.0                                            # the studs are squares turned with it (diamonds), 17 across the flats
    for lf in leaves:
        inner = lf.buffer(-st["edge_margin_mm"])
        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                x, y = (i - j) * p, (i + j) * p
                s_ = Polygon([(x, y - hd), (x + hd, y), (x, y + hd), (x - hd, y)])
                if inner.contains(s_):
                    studs.append(extrude(s_, -0.5, st["stud_height_mm"]))
    B.add("studs", orient(*merge(*studs)), "cast_iron_cover", bev=None)


def piece_service(T, B, kind):
    P = T["pieces"]["service_small"]
    if kind == "stopcock":
        s = P["water_stopcock"]
        ro, ri = s["frame"] / 2.0, s["lid"][0] / 2.0
        B.add("frame", ring_solid([(ri + 0.5, -40.0), (ro, -40.0), (ro, 0.0), (ri + 0.5, 0.0)], 48), "cast_iron_cover", bev=None)
        lid = B.add("lid", orient(*lathe([(0.0, -20.0), (ri - 0.5, -20.0), (ri - 0.5, 0.0), (0.0, 0.0)], 48)), "cast_iron_cover", bev=None)
        bs.bool_op(lid, *box3(-15.0, 15.0, -4.0, 4.0, -25.0, 1.0), "DIFFERENCE")
    elif kind == "gas":
        s = P["gas_box"]
        lw, lh, fw, fh = s["lid"][0] / 2.0, s["lid"][1] / 2.0, s["frame"][0] / 2.0, s["frame"][1] / 2.0
        B.add("frame", extrude(sbox(-fw, -fh, fw, fh).difference(sbox(-lw - 0.5, -lh - 0.5, lw + 0.5, lh + 0.5)), -40.0, 0.0), "cast_iron_cover", bev=1.0, min_angle=60.0)
        lid = B.add("lid", box3(-lw, lw, -lh, lh, -20.0, 0.0), "cast_iron_cover", bev=None)
        for sx in (-1.0, 1.0):
            bs.bool_op(lid, *box3(sx * (lw - 25.0) - 12.5, sx * (lw - 25.0) + 12.5, -4.0, 4.0, -25.0, 1.0), "DIFFERENCE")
    else:
        s = P["telecom_blank"]
        lw, lh, fw, fh = s["lid"][0] / 2.0, s["lid"][1] / 2.0, s["frame"][0] / 2.0, s["frame"][1] / 2.0
        B.add("frame", extrude(sbox(-fw, -fh, fw, fh).difference(sbox(-lw - 0.5, -lh - 0.5, lw + 0.5, lh + 0.5)), -40.0, 0.0), "cast_iron_cover", bev=1.0, min_angle=60.0)
        B.add("infill", box3(-lw, lw, -lh, lh, -40.0, -6.0), "flag_pale", bev=None)
        m = s["surround"].count("28") and 28.0
        B.add("mortar", extrude(sbox(-fw - m, -fh - m, fw + m, fh + m).difference(sbox(-fw, -fh, fw, fh)), -40.0, 0.0), "mortar_pale", bev=None)


class Shift:
    """a Parts look-alike that moves every added object by (dx, dy, dz): the review composition places the kit's own pieces, built by their own functions"""
    def __init__(self, B, dx=0.0, dy=0.0, dz=0.0, rot_deg=0.0, deferred=False):
        self.B, self.d, self.rot, self.deferred, self.objs = B, np.array([dx, dy, dz], float), math.radians(rot_deg), deferred, []

    def add(self, name, VF, mat, bev=None, min_angle=50.0):
        V = np.asarray(VF[0], float)
        if self.rot:
            c, s_ = math.cos(self.rot), math.sin(self.rot)
            V = np.column_stack([V[:, 0] * c - V[:, 1] * s_, V[:, 0] * s_ + V[:, 1] * c, V[:, 2]])
        if self.deferred:                                                           # the piece's own boolean cutters work at the origin: the objects are moved when it is finished (REVIEW-v1-street fault 1)
            ob = self.B.add(name, (V, VF[1]), mat, bev=bev, min_angle=min_angle)
            self.objs.append(ob)
            return ob
        return self.B.add(name, (V + self.d, VF[1]), mat, bev=bev, min_angle=min_angle)

    def apply(self):
        from mathutils import Matrix
        for ob in self.objs:
            ob.data.transform(Matrix.Translation(tuple(self.d)))
            ob.data.update()

    def bounds(self):
        V = np.vstack([np.array([v.co[:] for v in ob.data.vertices]) for ob in self.objs])
        return V.min(0), V.max(0)


def cut(ob, box):
    bs.bool_op(ob, *box3(*box), "DIFFERENCE")


def piece_review(T, B):
    """not a kit piece: the pieces together as a player meets them, for the two review views: a run of kerb (granite in blocks of 750 to 1050, then a stretch of concrete laid to the
    granite's line and level) with its channel, a gully grate and a round cover in the road, a stud cover in the footway, and (at x 8 to 12.8 m) the dropped crossover. After
    REVIEW-v1-street: the holed pieces are built at the origin and moved when finished, the grate stands flush with the setts, the ground is cut round every cover and grate, the
    concrete meets the granite with an 8 mm joint at the granite's level"""
    K = T["pieces"]["kerb_granite"]
    grng = np.random.default_rng(21)
    x, prev, x_end = -3550.0, 0.0, 2798.0
    while x < x_end - 1.0:
        L = float(grng.uniform(750.0, 1050.0))
        while abs(L - prev) < 20.0:
            L = float(grng.uniform(750.0, 1050.0))
        if x_end - (x + L) < 400.0:
            L = x_end - x                                                           # the last block is cut to close the run
        kerb_block(K, L, Shift(B, x + L / 2.0), "granite_grey", bev=10.0)
        prev, x = L, x + L + 8.0
    X0C = 3263.5                                                                    # the first concrete block's centre: 8 mm after the granite's end, both at the granite's top (+20 on its bed)
    for i in range(4):
        kerb_block(T["pieces"]["kerb_concrete"], 915.0, Shift(B, X0C + i * 923.0, 0.0, 20.0), "concrete_kerb", bev=3.0)
    rng = np.random.default_rng(7)
    setts_run(T["pieces"]["channel_setts"], Shift(B), rng, -3550.0, 2802.0)
    Shift(B).add("mortar", box3(-3549.0, 2801.0, 1.0, 203.0, -141.0, -8.0), "bitumen_joint")
    for i in range(4):
        Shift(B, X0C + i * 923.0, 0.0, 20.0).add("channel", prism_x([tuple(p) for p in T["pieces"]["channel_concrete"]["section_yz"]], -457.5, 457.5), "concrete_kerb", bev=None)
    setts_run(T["pieces"]["channel_setts"], Shift(B), np.random.default_rng(8), 7300.0, 12900.0, name_prefix="sett_b")
    Shift(B).add("mortar_b", box3(7301.0, 12899.0, 1.0, 203.0, -141.0, -8.0), "bitumen_joint")
    # the street's own ground, for the pictures only: the footway flags (top 110, behind the kerb and round the crossing) and the road (top 6, flat)
    for (xa, xb, ya, yb) in ((-3600.0, 2802.0, -40000.0, -170.0), (2802.0, 8000.0, -40000.0, -125.0), (8000.0, 12900.0, -40000.0, -845.0), (8000.0, 8760.0, -845.0, -170.0), (12040.0, 12900.0, -845.0, -170.0)):
        Shift(B).add("ground_footway", box3(xa, xb, ya, yb, -300.0, 110.0), "flag_pale")
    Shift(B).add("ground_road_a", box3(-3600.0, 2806.0, 204.0, 40000.0, -300.0, 6.0), "tarmac_infill")
    Shift(B).add("ground_road_b", box3(2806.0, 6498.0, 255.0, 40000.0, -300.0, 6.0), "tarmac_infill")
    Shift(B).add("ground_road_c", box3(6498.0, 12900.0, 204.0, 40000.0, -300.0, 6.0), "tarmac_infill")
    # the holed pieces: at the origin, then moved
    g = Shift(B, 800.0, 235.0, 0.0, deferred=True)
    piece_gully_A(T, g)
    g.apply()
    rc = Shift(B, 300.0, 1300.0, 6.0, deferred=True)
    piece_cover_round(T, rc)
    rc.apply()
    sc = Shift(B, 1500.0, -800.0, 110.0, deferred=True)
    piece_cover_stud(T, sc)
    sc.apply()
    piece_crossover(T, Shift(B, 10400.0, 0.0, 0.0))
    # the ground and the channel are cut round what stands in them
    glo, ghi = g.bounds()
    slo, shi = sc.bounds()
    rlo, rhi = rc.bounds()
    for ob in list(B.objs):
        if ob.name.startswith(("sett_", "mortar")) and not ob.name.endswith("_b"):
            cut(ob, (glo[0] - 0.5, ghi[0] + 0.5, glo[1] - 0.5, 204.0, -300.0, 10.0))
        if ob.name.startswith("ground_road_a"):
            cut(ob, (glo[0] - 0.5, ghi[0] + 0.5, glo[1] - 0.5, ghi[1] + 0.5, -300.0, 10.0))
            bs.bool_op(ob, *cyl_z(300.0, 1300.0, -300.0, 10.0, 346.0, 96), "DIFFERENCE")
        if ob.name.startswith("ground_footway"):
            cut(ob, (slo[0] - 0.5, shi[0] + 0.5, slo[1] - 0.5, shi[1] + 0.5, -300.0, 120.0))


PIECES = [
    ("kerb_granite", piece_kerb_granite), ("kerb_concrete", piece_kerb_concrete), ("channel_setts", piece_channel_setts), ("channel_concrete", piece_channel_concrete),
    ("crossover_A", piece_crossover), ("gully_grate_A", piece_gully_A), ("gully_grate_B", piece_gully_B), ("cover_stud_square", piece_cover_stud), ("cover_round_600", piece_cover_round),
    ("cover_recessed_footway", piece_cover_footway), ("cover_recessed_road", piece_cover_road), ("cover_road_double_leaf", piece_cover_double_leaf),
    ("review_scene", piece_review),
    ("service_stopcock", lambda T, B: piece_service(T, B, "stopcock")), ("service_gas", lambda T, B: piece_service(T, B, "gas")), ("service_telecom", lambda T, B: piece_service(T, B, "telecom")),
]


def bevel_ends(ob, width, min_angle=50.0):
    """the shared bevel, but for a kerb block only the edges of its two end faces (the end arris), not the long back and foot edges; clamp on for the others"""
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    lim = math.radians(min_angle)
    sel = [e for e in bm.edges if len(e.link_faces) == 2 and e.calc_face_angle(0.0) >= lim]
    if ob.name.startswith(("block", "end_block")):
        xm = max(abs(v.co.x) for v in bm.verts)
        xmin = min(abs(v.co.x) for v in bm.verts)
        sel = [e for e in sel if all(abs(abs(v.co.x) - xm) < 0.01 or abs(abs(v.co.x) - xmin) < 0.01 for v in e.verts) and abs(e.verts[0].co.x - e.verts[1].co.x) < 0.01]
    if sel:
        bmesh.ops.bevel(bm, geom=sel, offset=width, segments=3 if width >= 8.0 else 1, affect="EDGES", clamp_overlap=True)
    bm.to_mesh(ob.data)
    bm.free()


def build(T, out_dir, npz_dir, only=None):
    import bpy
    bs.bevel_obj = bevel_ends
    out = {}
    for name, fn in PIECES:
        if only and name not in only:
            continue
        bpy.ops.wm.read_factory_settings(use_empty=True)
        mats = mats_for(T)
        B = Parts()
        fn(T, B)
        obs = bs.finish(B, mats, 0.0)
        out[name] = bs.write(obs, name, 0.0, out_dir, npz_dir)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=ASSET_DIR)
    ap.add_argument("--npz-dir", default=NPZ_DIR)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    T = json.load(open(TARGET_JSON, encoding="utf-8"))
    res = build(T, a.out_dir, a.npz_dir, set(x for x in a.only.split(",") if x))
    for k, v in res.items():
        print("%-26s triangles %6d  glb bytes %8d" % (k, v["triangles"], v["glb_bytes"]))
    os.makedirs(a.npz_dir, exist_ok=True)
    path = os.path.join(a.npz_dir, "parts.json")
    old = json.load(open(path)) if (a.only and os.path.exists(path)) else {}
    old.update(res)
    json.dump(old, open(path, "w"), indent=1)


if __name__ == "__main__":
    main()
