"""Quay Street's lamp post, variant C (cloud week 42, unit 3.8), built by script from targets/lamp-posts/target.json (the second review's fixes applied).

    /home/user/.bpyenv/bin/python build_lamp.py [--out-dir DIR] [--npz-dir DIR]

Two models in the column's own frame (millimetres in the script, metres in the .glb, z up, the axis at the origin on the footway surface, +y toward the carriageway,
the shaft's hidden skirt to z -150): lamp_column_C.glb (the precast concrete shaft with its mitred concrete arm, the 42 steel spigot, the door plate on -y, the number plate
on +y) and lamp_lantern.glb (the boat-shaped canopy over the clear bowl, its reflector, soffit, rear boss, hinge, catches, the lamp's holder, the glass jacket and the arc
tube; the emissive parts are their own material slots: lamp_glass, arc_tube, bowl). Variant A (painted steel) is written in the target and not built (built only if Jafar rules
the steel column in). The cypher-free plate carries no letters here: 'LC n' is the engine's texture.
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
from build_railings import Parts, rrect, prism_x  # noqa: E402
from build_bollards import lathe, prism_y  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "lamp-posts", "target.json")
ASSET_DIR = os.path.join(REPO, "production", "assets", "cloud-week", "lamp-posts")
NPZ_DIR = os.path.join(HERE, "build")


# ------------------------------------------------------------------------------------------------------------------------------------ helpers
def merge(*parts):
    """one (V, F) from several that share no vertices"""
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


def lerp(tbl, y):
    """linear between (y, v) stations, held outside"""
    if y <= tbl[0][0]:
        return tbl[0][1]
    for (y0, v0), (y1, v1) in zip(tbl, tbl[1:]):
        if y0 <= y <= y1:
            return v0 + (v1 - v0) * (y - y0) / (y1 - y0) if y1 > y0 else v0
    return tbl[-1][1]


def oct_ring(side, ch, z):
    h = side / 2.0
    return [(-h + ch, -h, z), (h - ch, -h, z), (h, -h + ch, z), (h, h - ch, z), (h - ch, h, z), (-h + ch, h, z), (-h, h - ch, z), (-h, -h + ch, z)]


def cyl_y(x, z, y0, y1, r, n=24, rr1=None):
    rr1 = r if rr1 is None else rr1
    rings = []
    for y, rad in ((y0, r), (y1, rr1)):
        rings.append([(x + rad * math.cos(2 * math.pi * k / n), y, z + rad * math.sin(2 * math.pi * k / n)) for k in range(n)])
    return orient(*bs.loft_rings(rings))


def dome(base, axis, r, h, n=14):
    """a round-headed screw: a dome of radius r and height h standing on `base`, pointing along `axis` (a unit vector)"""
    prof = [(0.0, -0.5), (r, -0.5), (r, 0.0), (0.93 * r, 0.35 * h), (0.72 * r, 0.7 * h), (0.4 * r, 0.93 * h), (0.0, h)]
    V, F = lathe(prof, n)
    a = np.asarray(axis, float)
    a /= np.linalg.norm(a)
    z = np.array([0.0, 0.0, 1.0])
    v = np.cross(z, a)
    c = float(np.dot(z, a))
    if np.linalg.norm(v) < 1e-9:
        R = np.eye(3) if c > 0 else np.diag([1.0, -1.0, -1.0])
    else:
        vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        R = np.eye(3) + vx + vx @ vx * (1.0 / (1.0 + c))
    return np.asarray(V) @ R.T + np.asarray(base, float), F


def swap_yz(V, F):
    return np.asarray(V)[:, [0, 2, 1]], [tuple(f[::-1]) for f in F]


def prism_z(poly_xy, z0, z1):
    """a plan polygon (x, y) extruded along z (z0 < z1)"""
    V, F = prism_y(poly_xy, z0, z1)
    return orient(*swap_yz(V, F))


def side_at(sides, z):
    """the shaft's side across the faces at height z, linear between the (z, side, chamfer) points"""
    for (z0, s0, _), (z1, s1, _) in zip(sides, sides[1:]):
        if z0 <= z <= z1 and z1 > z0:
            return s0 + (s1 - s0) * (z - z0) / (z1 - z0)
    return sides[-1][1]


# ------------------------------------------------------------------------------------------------------------------------------------ the column
def column(T, B, mats):
    G = T["geometry"]["C"]
    sh = G["shaft"]
    sides = [tuple(p) for p in sh["points_z_side_chamfer"]]                     # (z, side, chamfer)
    ch = sh["chamfer"]
    zt = sh["top_z"]
    cb = G["bracket"]
    ax, half, aend = cb["axis_z"], cb["section"]["square"] / 2.0, cb["arm_end_y"]
    # the shaft: octagonal rings (a square with its arrises chamfered 15) through the four heights; the top face's edge is eased by the bevel
    slope = (sides[-1][1] - sides[-2][1]) / (sides[-1][0] - sides[-2][0])
    rings = [oct_ring(s, ch, z) for z, s, _ in sides] + [oct_ring(sides[-1][1] + 3.0 * slope, ch, zt + 3.0)]          # 3 taller: the top face is made by one cut below
    Vs, Fs = orient(*bs.loft_rings(rings))
    col = B.add("column", (Vs, Fs), "concrete_C", bev=sh["top_face_chamfer_mm"], min_angle=50.0)
    # the arm: an octagon 110 with its arrises chamfered 10, level at the axis height, from inside the shaft to the flat end face at y 400
    ac = cb["section"]["chamfer"]
    arm_rings = []
    for y in (-40.0, aend):
        o = oct_ring(2 * half, ac, 0.0)
        arm_rings.append([(x, y, ax + zz + (0.5 if zz > 50.0 else 0.0)) for (x, zz, _) in o])                          # 0.5 tall at the top: cut flat below
    Va, Fa = orient(*bs.loft_rings(arm_rings))
    bs.bool_op(col, Va, Fa, "UNION")
    top_cut = prism_x([(-300.0, zt), (700.0, zt), (700.0, zt + 20.0), (-300.0, zt + 20.0)], -300.0, 300.0)
    bs.bool_op(col, *orient(*top_cut), "DIFFERENCE")
    # the mitre: the outer corner (the top face meeting the shaft's -y face) rounded to radius 20, the inner corner (underside meeting the +y face) a fillet of radius 10
    R_out, R_in = cb["mitre"]["outer_corner_radius"], cb["mitre"]["inner_fillet_radius"]
    yc, zc = -side_at(sides, zt) / 2.0, zt
    arc = [(yc + R_out + R_out * math.cos(math.radians(a)), zc - R_out + R_out * math.sin(math.radians(a))) for a in np.linspace(90.0, 180.0, 13)]
    cut = [(yc - 2.0, zc + 2.0), (yc + R_out, zc + 2.0)] + arc + [(yc - 2.0, zc - R_out)]
    Vc, Fc = prism_x(cut, -70.0, 70.0)
    bs.bool_op(col, *orient(Vc, Fc), "DIFFERENCE")
    yi, zi = side_at(sides, ax - half) / 2.0, ax - half
    arc = [(yi + R_in + R_in * math.cos(math.radians(a)), zi - R_in + R_in * math.sin(math.radians(a))) for a in np.linspace(90.0, 180.0, 11)]
    fill = [(yi - 1.0, zi + 1.0), (yi + R_in, zi + 1.0)] + arc + [(yi - 1.0, zi - R_in)]
    Vf, Ff = prism_x(fill, -43.0, 43.0)
    bs.bool_op(col, *orient(Vf, Ff), "UNION")
    # the door: a recess 120 x 330 x 14 at z 450 to 780 on -y, 6 mm corner radii; the plate 132 x 342 x 3 over it, 3 proud, two screws
    d = G["door"]
    rz = d["recess"]["z"]
    rec = [(p[0], (rz[0] + rz[1]) / 2.0 + p[1]) for p in rrect(d["recess"]["width"], d["recess"]["height"], 6.0, 3)]
    Vr, Fr = prism_y(rec, -5.0, d["recess"]["depth"])
    Vr = np.array([(x, -side_at(sides, z) / 2.0 + y, z) for x, y, z in Vr])
    bs.bool_op(col, *orient(Vr, Fr), "DIFFERENCE")
    pl = d["plate"]
    pz = pl["z"]
    prof = [(p[0], (pz[0] + pz[1]) / 2.0 + p[1]) for p in rrect(pl["width"], pl["height"], pl["corner_radius"], 4)]
    Vp, Fp = prism_y(prof, -pl["proud"], 1.0)
    Vp = np.array([(x, -side_at(sides, z) / 2.0 + y, z) for x, y, z in Vp])
    B.add("door_plate", orient(Vp, Fp), "c_door_plate", bev=0.8)
    screws = []
    for zs in pl["screws"]["z"]:
        yf = -side_at(sides, zs) / 2.0 - pl["proud"]
        screws.append(dome((0.0, yf, zs), (0.0, -1.0, 0.0), pl["screws"]["head_od"] / 2.0, 2.0))
    B.add("door_screws", orient(*merge(*screws)), "c_door_plate", bev=None)
    # the number plate on +y: a flat 90 x 45 x 1.2 plate, 1.4 proud, two domed rivets 5 across at 8 from each end
    npl = G["number_plate"]
    z0 = npl["z_centre"]
    prof = [(p[0], z0 + p[1]) for p in rrect(npl["size"][0], npl["size"][1], 3.0, 3)]
    Vn, Fn = prism_y(prof, -0.5, npl["proud"])
    Vn = np.array([(x, side_at(sides, z) / 2.0 + y, z) for x, y, z in Vn])
    B.add("number_plate", orient(Vn, Fn), "plate", bev=0.5)
    rv = []
    for sx in (-1.0, 1.0):
        yf = side_at(sides, z0) / 2.0 + npl["proud"]
        rv.append(dome((sx * (npl["size"][0] / 2.0 - 8.0), yf - 0.5, z0), (0.0, 1.0, 0.0), 2.5, 1.0, 10))
    B.add("number_rivets", orient(*merge(*rv)), "plate", bev=None)
    # the spigot: a steel tube OD 42 on the arm's axis from y 340 (60 cast into the arm) to y 485 (inside the lantern's boss)
    sp = G["spigot"]
    B.add("spigot", cyl_y(0.0, ax, sp["y"][0], sp["y"][1] - 2.0, sp["od"] / 2.0, 24), "c_spigot", bev=None)           # its end 2 inside the boss (the boss ends at 485): no two end faces in one plane


# ------------------------------------------------------------------------------------------------------------------------------------ the lantern
def arch_ring(w, zt, zb, rim, t_out, t_in, n=21):
    """the canopy's section at one station as a closed band between two offsets of its outer arch (the lip from the rim to the dome's base, then the half ellipse)"""
    def curve(t):
        ww = max(w - t, 0.6)
        top = max(zt, zb + 4.0) - t                      # at the tips (where the dome is no higher than its base) the skin keeps 4 of rise, so that no two offsets collapse onto one surface
        pts = [(-ww, rim)]
        for k in range(n):
            th = math.pi * k / (n - 1)
            pts.append((-ww * math.cos(th), zb + (top - zb) * math.sin(th)))
        pts.append((ww, rim))
        return pts
    return curve(t_out) + curve(t_in)[::-1]


def canopy_shell(L, t_out, t_in, y_from, y_to):
    can = L["canopy"]
    rim, zb = can["rim_z"], can["dome_base_z"]
    pw, tz = [tuple(p) for p in can["plan_half_width"]], [tuple(p) for p in can["top_z_along_y"]]
    ys = sorted({y for y, _ in pw} | {y for y, _ in tz} | {(a + b) / 2.0 for (a, _), (b, _) in zip(pw, pw[1:])})
    ys = [y for y in ys if y_from <= y <= y_to]
    keep = [ys[0]]
    for y in ys[1:]:                                   # no two stations within 4 mm (slivers whose triangles turn over)
        if y - keep[-1] >= 4.0 or y == ys[-1]:
            keep.append(y)
    ys = keep
    ys[0], ys[-1] = ys[0] + 1.2, ys[-1] - 1.2
    rings = []
    for y in ys:
        w = max(lerp(pw, y), 0.0) + (3.0 if y in (ys[0], ys[-1]) else 0.0)
        r2 = arch_ring(w, lerp(tz, y), zb, rim, t_out, t_in)
        rings.append([(x, y, z) for x, z in r2])
    return orient(*bs.loft_rings(rings))


def bowl_rings(L, inner=False):
    bw = L["bowl"]
    base_tbl = [tuple(p) for p in bw["base_plan_half_width"]]
    pw = [tuple(p) for p in L["canopy"]["plan_half_width"]]
    rear = [tuple(p) for p in bw["long_section_rear_curve_yz"]]        # (y, z) rim -> base
    front = [tuple(p) for p in bw["long_section_front_curve_yz"]]      # base -> rim
    sec = [tuple(p) for p in bw["section_at_centre_half_width_z"]]     # (half width, z)
    inset = bw["rim_inset"]
    t = 3.0
    z_lo, z_hi = 4800.0, 4925.0
    h0, h1 = sec[0][0], sec[-1][0]

    def s_of(z):
        for (ha, za), (hb, zb) in zip(sec, sec[1:]):
            if za <= z <= zb:
                return (ha + (hb - ha) * (z - za) / (zb - za) - h0) / (h1 - h0)
        return 1.0 if z > sec[-1][1] else 0.0

    def y_rear(z):
        pts = sorted([(zz, yy) for yy, zz in rear])
        return float(np.interp(z, [p[0] for p in pts], [p[1] for p in pts]))

    def y_front(z):
        pts = sorted([(zz, yy) for yy, zz in front])
        return float(np.interp(z, [p[0] for p in pts], [p[1] for p in pts]))
    zs = sorted(set([z_lo] + [z for _, z in sec] + [z_hi]))
    rings = []
    for k, z in enumerate(zs):
        s = s_of(z)
        yr, yf = y_rear(z), y_front(z)
        n = 26
        d = t if inner else 0.0
        ys = np.linspace(yr + d + 0.6, yf - d - 0.6, n)
        left, right = [], []
        zz = z + (t if (inner and k == 0) else 0.0)               # the inner floor stands 3 above the outer base
        for y in ys:
            bwy = lerp(base_tbl, y) if base_tbl[0][0] <= y <= base_tbl[-1][0] else 0.0
            rw = max(lerp(pw, y) - inset, 0.0)
            hw = bwy + (rw - bwy) * s
            hw = max(hw - d, 0.4)
            left.append((-hw, y, zz))
            right.append((hw, y, zz))
        rings.append(right + left[::-1])
    return rings


def bowl_shell(L):
    """the clear bowl as one closed solid with a cavity: the outer surface from the base to the rim, the inner surface 3 inside it (the floor 3 above the base), the rim
    between them as an annulus; built face by face (no boolean)"""
    O, I = bowl_rings(L, False), bowl_rings(L, True)
    m, n = len(O), len(O[0])
    V = np.vstack([np.asarray(r, float) for r in O + I])
    F = []
    for k in range(m - 1):
        a, b = k * n, (k + 1) * n
        for i in range(n):
            j = (i + 1) % n
            F.append((a + i, a + j, b + j, b + i))                                               # the outer surface, facing out
            F.append((m * n + b + i, m * n + b + j, m * n + a + j, m * n + a + i))                # the inner surface, facing the cavity
    F.append(tuple(range(n))[::-1])                                                               # the outer base, facing down
    F.append(tuple(range(m * n, m * n + n)))                                                      # the cavity's floor, facing up
    top_o, top_i = (m - 1) * n, m * n + (m - 1) * n
    for i in range(n):
        j = (i + 1) % n
        F.append((top_o + i, top_o + j, top_i + j, top_i + i))                                   # the rim, facing up
    return orient(V, F)


def lantern(T, B, mats):
    L = T["geometry"]["lantern"]
    can, lamp, boss = L["canopy"], L["lamp"], L["boss"]
    y_lo, y_hi = L["envelope"]["length_y"]
    # the canopy: a shell 2.5 thick (the outer paint), and the white reflector as a thin skin inside it
    B.add("canopy", canopy_shell(L, 0.0, 2.5, y_lo, y_hi), "canopy", bev=1.5, min_angle=60.0)
    B.add("reflector", canopy_shell(L, 2.5, 4.5, y_lo + 6.0, y_hi - 6.0), "reflector", bev=None)
    # the flat cast soffit closing the canopy's underside at z 4925 from y 430 to 488, in the canopy's material (the boss's lower 24 mm hang below it)
    pw = [tuple(p) for p in can["plan_half_width"]]
    ysf = [431.5, 435.9, 453.6, 483.2, 488.0]
    left = [(-lerp(pw, y) if y > 432 else -3.0, y) for y in ysf]
    right = [(lerp(pw, y) if y > 432 else 3.0, y) for y in ysf]
    poly = right + left[::-1]
    B.add("soffit", prism_z(poly, can["rim_z"] - 2.5, can["rim_z"] + 0.8), "canopy", bev=None)           # 0.8 into the canopy over it: no face in the lip's plane
    # the rear boss: OD 60, 55 long, level on the arm's axis, with two M8 round-headed grub screws (azimuth 90 and 270 about the axis, so on +-x), 3 proud
    az = boss["axis_from"][2]
    B.add("boss", cyl_y(0.0, az, boss["axis_from"][1], boss["axis_from"][1] + boss["length"], boss["od"] / 2.0, 24), "canopy", bev=1.5, min_angle=60.0)
    gs = [dome((sx * (boss["od"] / 2.0 - 0.5), boss["axis_from"][1] + 27.0, az), (sx, 0.0, 0.0), 5.0, 3.5, 10) for sx in (-1.0, 1.0)]
    B.add("boss_screws", orient(*merge(*gs)), "canopy", bev=None)
    # the bowl: a clear shell 3 thick from the flat refractor base (z 4800) to the rim (z 4925), clear of the boss (the rim starts at y 488)
    B.add("bowl", bowl_shell(L), "bowl", bev=None)
    # the hinge (two knuckles 22 x 22 x 14 at x +-60, y 497, on the rim) and the two spring catches 30 x 14 x 7 proud at y 932.3, x +-136
    hg = L["hinge"]
    hv = []
    for sx in hg["x"]:
        xa, xb = sx - hg["size"][0] / 2.0, sx + hg["size"][0] / 2.0
        ya, yb = hg["y"] - hg["size"][1] / 2.0, hg["y"] + hg["size"][1] / 2.0
        hv.append(prism_z([(xa, ya), (xb, ya), (xb, yb), (xa, yb)], hg["z"] - 1.0, hg["z"] + hg["size"][2]))
    B.add("hinge", merge(*hv), "canopy", bev=1.0)
    cs = L["catches"]
    cv = []
    for sx in (-1.0, 1.0):
        xa, xb = sorted((sx * (cs["x_abs"] - cs["size_y_z_proud"][2]), sx * cs["x_abs"]))
        ya, yb = cs["y"] - cs["size_y_z_proud"][0] / 2.0, cs["y"] + cs["size_y_z_proud"][0] / 2.0
        cv.append(prism_z([(xa, ya), (xb, ya), (xb, yb), (xa, yb)], cs["z"] - cs["size_y_z_proud"][1] / 2.0, cs["z"] + cs["size_y_z_proud"][1] / 2.0))
    B.add("catches", merge(*cv), "canopy", bev=1.0)
    # the lamp holder (60 x 45 x 40 at the rear, y 555 to 600) hung from the canopy's ceiling by a bracket, with two stubs where the tube's legs start
    hd = lamp["holder"]
    xa, xb = hd["x"]
    ya, yb = hd["y"]
    za, zb = hd["z"]
    top = lerp([tuple(p) for p in can["top_z_along_y"]], (ya + yb) / 2.0) - 2.5
    parts = [prism_z([(xa, ya), (xb, ya), (xb, yb), (xa, yb)], za, zb), prism_z([(-12.0, ya + 8.0), (12.0, ya + 8.0), (12.0, yb - 8.0), (-12.0, yb - 8.0)], zb - 1.0, top + 1.5)]
    B.add("lamp_holder", merge(*parts), "canopy", bev=None)
    # the lamp's glass jacket 54 x 310 along y at (0, 755, 4872); the arc tube inside it (a U: two legs of 16 OD at x +-11, y 605 to 876, a half-torus of centreline radius 11 to 895)
    cz = lamp["centre"][2]
    B.add("lamp_jacket", cyl_y(0.0, cz, lamp["centre"][1] - lamp["length"] / 2.0, lamp["centre"][1] + lamp["length"] / 2.0, lamp["od"] / 2.0, 32), "lamp_glass", bev=None)
    tb = lamp["arc_tube"]
    tr = tb["leg_od"] / 2.0
    legs = [cyl_y(sx, tb["z"], tb["y"][0], tb["legs_straight_to_y"] + 1.0, tr, 14) for sx in tb["leg_x"]]
    stubs = [cyl_y(sx, tb["z"], hd["y"][1] - 5.0, tb["y"][0] + 1.0, 5.0, 10) for sx in tb["leg_x"]]
    Rb = tb["bend_centreline_radius"]
    rings = []
    for k in range(0, 13):
        phi = math.pi * k / 12.0
        p = np.array([Rb * math.cos(phi), tb["legs_straight_to_y"] + Rb * math.sin(phi), tb["z"]])
        e1 = np.array([math.cos(phi), math.sin(phi), 0.0])
        e2 = np.array([0.0, 0.0, 1.0])
        rings.append([tuple(p + tr * (math.cos(a) * e1 + math.sin(a) * e2)) for a in np.linspace(0.0, 2 * math.pi, 14, endpoint=False)])
    tor = orient(*bs.loft_rings(rings))
    B.add("arc_tube", merge(*legs, tor), "arc_tube", bev=None)
    B.add("lamp_stubs", merge(*stubs), "arc_tube", bev=None)


def bevel_noclamp(ob, width, min_angle=50.0):
    """the shared bevel with the overlap clamp off: the column's many short edges (the mitre's arc facets, the arm's chamfers) made the clamp take the 5 mm top chamfer to nothing"""
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    lim = math.radians(min_angle)
    sel = [e for e in bm.edges if len(e.link_faces) == 2 and e.calc_face_angle(0.0) >= lim]
    if sel:
        bmesh.ops.bevel(bm, geom=sel, offset=width, segments=1, affect="EDGES", clamp_overlap=False)
    bm.to_mesh(ob.data)
    bm.free()


def build(T, out_dir, npz_dir):
    import bpy
    bs.bevel_obj = bevel_noclamp
    out = {}
    for what in ("column", "lantern", "assembly"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        V = lambda k: T["numbers"][k]["value"]  # noqa: E731
        mats = {"concrete_C": bs.make_material("concrete_C", V("c_albedo_srgb"), V("c_roughness"), 0.0),
                "c_door_plate": bs.make_material("c_door_plate", T["materials"]["c_door_plate"]["srgb"], T["materials"]["c_door_plate"]["roughness"], 0.0),
                "plate": bs.make_material("plate", T["materials"]["plate"]["srgb_white"], T["materials"]["plate"]["roughness"], 0.0),
                "c_spigot": bs.make_material("c_spigot", V("paint_black_srgb"), 0.42, 0.0),
                "canopy": bs.make_material("canopy", V("canopy_srgb"), T["materials"]["canopy"]["roughness"], 0.0),
                "reflector": bs.make_material("reflector", V("reflector_srgb"), 0.35, 0.0),
                "bowl": bs.make_material("bowl", V("bowl_unlit_srgb"), 0.15, 0.0, transmission=0.85, ior=1.49),
                "lamp_glass": bs.make_material("lamp_glass", T["materials"]["lamp_glass"]["srgb_unlit"], 0.10, 0.0),
                "arc_tube": bs.make_material("arc_tube", T["materials"]["arc_tube"]["srgb_unlit"], 0.2, 0.0)}
        B = Parts()
        if what in ("column", "assembly"):
            column(T, B, mats)
        if what in ("lantern", "assembly"):
            lantern(T, B, mats)
        name = {"column": "lamp_column_C", "lantern": "lamp_lantern", "assembly": "lamp_post_C"}[what]
        obs = bs.finish(B, mats, 0.0)
        out[name] = bs.write(obs, name, 0.0, out_dir, npz_dir)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=ASSET_DIR)
    ap.add_argument("--npz-dir", default=NPZ_DIR)
    a = ap.parse_args()
    T = json.load(open(TARGET_JSON, encoding="utf-8"))
    res = build(T, a.out_dir, a.npz_dir)
    for k, v in res.items():
        print(k, "triangles", v["triangles"], "glb bytes", v["glb_bytes"], v["objects"])
    os.makedirs(a.npz_dir, exist_ok=True)
    json.dump(res, open(os.path.join(a.npz_dir, "parts.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
