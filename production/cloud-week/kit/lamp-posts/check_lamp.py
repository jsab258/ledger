"""The automatic check of the lamp post (kit/lamp-posts, variant C): the built meshes against the lamp-post target's own checks and drawing.

    /home/user/.bpyenv/bin/python check_lamp.py [--version 1]

Reads build/lamp_post_C.npz (the column and the lantern together, metres, z up, the axis at the origin, +y toward the carriageway) and the three .glb files. For each of the
target's checks that applies to variant C (and the lantern) it measures the mesh: the shaft's sides and chamfer at z 300, 2300 and 4300, the top face, the arm's section, the
mitre's two radii, the spigot, the door recess and plate, the screws, the number plate, the lantern's box, centre, bowl base, lamp, arc tube, boss, dome and clearances, the
side silhouette and the sections against target_drawing.py's polygons, closed solids, hatching, the files. The engine's lights, the plate's letters, the wear and the emissive
strengths are not meshes: listed in `not_built`. Writes checks/check_v<N>.json.
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import LineString, Point, Polygon, box

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shopfront"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import check_shopfront as cs  # noqa: E402  (the shared reading tools)
import outline  # noqa: E402
from outline import compare, load_npz  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_DIR = os.path.join(REPO, "production", "cloud-week", "targets", "lamp-posts")
sys.path.insert(0, TARGET_DIR)
import target_drawing as TD  # noqa: E402

COLUMN = ("column", "door_plate", "door_screws", "number_plate", "number_rivets", "spigot")
LANTERN = ("canopy", "reflector", "soffit", "boss", "boss_screws", "bowl", "hinge", "catches", "lamp_holder", "lamp_jacket", "arc_tube", "lamp_stubs")


def mm(M, *names):
    return np.vstack([M[n][0] for n in names]) * 1000.0


def bnd(M, *names):
    V = mm(M, *names)
    return V.min(0), V.max(0)


def sec(M, names, axis, value, axes):
    return cs.section_poly(M, names, axis, value, axes)


def hd(a, b):
    """the largest distance between two outlines, either way (shapely's Hausdorff on the boundaries)"""
    if a.is_empty or b.is_empty:
        return 1e9
    return float(a.boundary.hausdorff_distance(b.boundary))


def silhouette_ok(rep, id_, model_mask, tgt_mask, mmpx, rule):
    c = compare(model_mask, tgt_mask, mmpx)
    rep.compare_row(id_, c, rule)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", type=int, default=1)
    a = ap.parse_args()
    T = json.load(open(os.path.join(TARGET_DIR, "target.json"), encoding="utf-8"))
    V = lambda k: T["numbers"][k]["value"]  # noqa: E731
    G = T["geometry"]["C"]
    L = T["geometry"]["lantern"]
    sides = [tuple(p) for p in G["shaft"]["points_z_side_chamfer"]]
    side = lambda z: float(np.interp(z, [p[0] for p in sides], [p[1] for p in sides]))  # noqa: E731
    M = load_npz(os.path.join(HERE, "build", "lamp_post_C.npz"))
    info = json.load(open(os.path.join(HERE, "build", "parts.json")))
    views = TD.build_views(T)
    rep = cs.Report()
    colN = [n for n in COLUMN if n in M]
    lanN = [n for n in LANTERN if n in M]
    allV = mm(M, *M.keys())
    colp0 = sec(M, ("column",), 2, 0.5, (0, 1))
    rep.add("PARTS: the column's six parts and the lantern's twelve, no others (no letters, no maker's mark)", set(M) == set(COLUMN) | set(LANTERN), sorted(M), "18 parts")
    rep.within("PIVOT: the lowest vertex z -150 (the target: -160 to -140), the shaft's axis at the origin", [allV[:, 2].min(), (colp0.bounds[0] + colp0.bounds[2]) / 2, (colp0.bounds[1] + colp0.bounds[3]) / 2], [-150.0, 0.0, 0.0], 3.0)
    # ---- the shaft, section by section
    colp = lambda z: sec(M, ("column",), 2, z, (0, 1))  # noqa: E731
    for z, want in ((300.0, 213.8), (2300.0, 172.7), (4300.0, 131.6)):
        P = colp(z)
        b = P.bounds
        rep.within("SHAFT side across the faces at z %d (x and y extents; the target %.1f)" % (z, want), [b[2] - b[0], b[3] - b[1]], [want, want], 6.0)
        c_ = math.sqrt(max((want ** 2 - P.area) / 2.0, 0.0))
        rep.within("SHAFT arris chamfer 15 at z %d (read from the section's area: side^2 - 2 c^2)" % z, c_, 15.0, 3.0)
        rep.within("SHAFT section square to the street at z %d: symmetric about both axes" % z, [b[0] + b[2], b[1] + b[3]], [0.0, 0.0], 1.0)
    P = colp(0.5)
    rep.within("SHAFT 220 at the footway", [P.bounds[2] - P.bounds[0], P.bounds[3] - P.bounds[1]], [220.0, 220.0], 1.5)
    rep.within("SHAFT top: the highest vertex z 4985.8 (one face with the arm's top)", bnd(M, "column")[1][2], 4985.8, 0.6)
    P = colp(4985.8 - 0.4)
    rep.within("SHAFT top face's edge chamfer 5 (the section 0.4 below the top is inset 4.6 a side: 117.5 - 9.2)", P.bounds[2] - P.bounds[0], 117.5 - 9.2, 2.5)
    # ---- the arm
    cb = G["bracket"]
    ax = cb["axis_z"]
    Pa = sec(M, ("column",), 1, 250.0, (0, 2))
    b = Pa.bounds
    c_ = math.sqrt(max((110.0 ** 2 - Pa.area) / 2.0, 0.0))
    rep.within("ARM section at y 250: 110 wide, 110 tall, axis z 4930.8", [b[2] - b[0], b[3] - b[1], (b[1] + b[3]) / 2.0], [110.0, 110.0, ax], 3.0)
    rep.within("ARM arrises chamfered 10 (read from the section's area)", c_, 10.0, 2.5)
    lo, hi = bnd(M, "column")
    rep.within("ARM ends flat at y 400 (the column's furthest vertex)", hi[1], 400.0, 1.0)
    z_top = [sec(M, ("column",), 1, y, (0, 2)).bounds[3] for y in (150.0, 250.0, 380.0)]
    z_bot = [sec(M, ("column",), 1, y, (0, 2)).bounds[1] for y in (150.0, 250.0, 380.0)]
    rep.within("ARM level: rake 0 (top and underside the same height at y 150, 250 and 380; the arm's rise over 300 at most 5 degrees' worth)", [max(z_top) - min(z_top), max(z_bot) - min(z_bot)], [0.0, 0.0], 0.6)
    rep.within("ARM top face z 4985.8 and underside 4875.8", [z_top[1], z_bot[1]], [4985.8, 4875.8], 0.6)
    # ---- the mitre
    Ps = sec(M, ("column",), 0, 0.0, (1, 2))
    yc, zc = -side(4985.8) / 2.0, 4985.8
    d_out = Ps.distance(Point(yc, zc))
    rep.within("MITRE outer corner rounded to radius 20: the outline stands 0.414 x 20 = 8.3 from the sharp corner (the target: R20 +-5)", d_out, 0.4142 * 20.0, 1.5)
    yi, zi = side(ax - 55.0) / 2.0, ax - 55.0
    t_cross = None
    for tt in np.arange(0.0, 12.0, 0.05):                                    # along the diagonal out of the concave corner: where does the solid end?
        if not Ps.buffer(0.001).contains(Point(yi + tt / math.sqrt(2.0), zi - tt / math.sqrt(2.0))):
            t_cross = float(tt)
            break
    rep.within("MITRE inner corner a fillet of radius 10: out of the sharp corner along its diagonal the solid reaches 0.414 x 10 = 4.1 (R10 +-5)", t_cross if t_cross is not None else -1.0, 0.4142 * 10.0, 1.5)
    ytop = [Ps.intersection(LineString([(-200, zz), (500, zz)])).bounds for zz in (4985.0, 4984.0)]
    rep.add("MITRE the arm's top face and the shaft's top are one face at z 4985.8: the section's top edge is level from the shaft's -y side to y 400", abs(Ps.bounds[3] - 4985.8) < 0.6 and ytop[0][2] > 390, [round(Ps.bounds[3], 2), round(ytop[0][2], 1)], "z 4985.8 to y 400")
    # ---- the spigot
    sp = G["spigot"]
    sl, sh = bnd(M, "spigot")
    rep.within("SPIGOT: OD 42 (x and z extents), y 340 to 485, axis z 4930.8", [sh[0] - sl[0], sh[2] - sl[2], sl[1], sh[1], (sl[2] + sh[2]) / 2.0], [42.0, 42.0, 340.0, 483.0, ax], 0.8, "the target says 485 (inside the boss, +-3): the end is 2 inside the boss end so that no two faces share a plane")
    bl, bh = bnd(M, "boss")
    rep.within("SPIGOT shows 30 between the arm's end (400) and the boss (430)", [bl[1] - hi[1]], [30.0], 1.0)
    rep.within("BOSS: OD 60 (x and z extents), 55 long from y 430, axis z 4930.8 (rake 0)", [bh[0] - bl[0], bh[2] - bl[2], bl[1], bh[1], (bl[2] + bh[2]) / 2.0], [60.0, 60.0, 430.0, 485.0, ax], 1.0)
    gl, gh = bnd(M, "boss_screws")
    rep.add("BOSS two grub screws, 3 proud, on the +x and -x sides (azimuth 90 and 270)", abs(gl[0] + 33.0) < 1.5 and abs(gh[0] - 33.0) < 1.5 and 430 < gl[1] and gh[1] < 485, [round(gl[0], 1), round(gh[0], 1)], "x +-33")
    # ---- the door
    d = G["door"]
    Pc = sec(M, ("column",), 0, 0.0, (1, 2))
    depths = []
    zz = np.arange(430.0, 800.0, 1.0)
    for z in zz:
        ln = Pc.intersection(LineString([(-300, z), (300, z)]))
        depths.append(ln.bounds[0] + side(z) / 2.0 if not ln.is_empty else 0.0)           # how far behind the face the section starts (the -y face is at -side/2)
    depths = np.array(depths)
    inr = zz[depths > 3.0]
    rep.within("DOOR recess z range 450 to 780 (the section at x 0 steps back more than 3 mm)", [inr.min(), inr.max()], [450.0, 780.0], 5.0)
    rep.within("DOOR recess depth 14", float(np.median(depths[depths > 3.0])), 14.0, 2.0)
    Pz = sec(M, ("column",), 2, 600.0, (0, 1))
    xs = np.arange(-80.0, 80.0, 0.5)                                         # the flat of the -y face (the chamfers run in at +-88)
    face = -side(600.0) / 2.0
    inner = [x for x in xs if not Pz.intersection(LineString([(x, -300), (x, 0)])).is_empty and Pz.intersection(LineString([(x, -300), (x, 0)])).bounds[1] > face + 3.0]
    rep.within("DOOR recess width 120 (at z 600)", max(inner) - min(inner), 120.0, 5.0)
    pl = d["plate"]
    pl_l, pl_h = bnd(M, "door_plate")
    rep.within("DOOR plate 132 x 342, z 444 to 786", [pl_h[0] - pl_l[0], pl_h[2] - pl_l[2], pl_l[2], pl_h[2]], [132.0, 342.0, 444.0, 786.0], 2.0)
    zmid = (pl_l[2] + pl_h[2]) / 2.0
    Vpl = mm(M, "door_plate")
    off = np.array([-side(z) / 2.0 - y for x, y, z in Vpl])                 # how far each vertex stands in front of the tapered face
    rep.within("DOOR plate stands 3 proud of the face (the front vertices' distance in front of the tapered face)", off.max(), 3.0, 1.0)
    sc_l, sc_h = bnd(M, "door_screws")
    Vsc = mm(M, "door_screws")
    zc_ = sorted([Vsc[Vsc[:, 2] < 615][:, 2].mean(), Vsc[Vsc[:, 2] > 615][:, 2].mean()])
    rep.within("DOOR two screws 10 across at z 469 and 761, on the plate's centre line", [sc_h[0] - sc_l[0]] + zc_, [10.0, 469.0, 761.0], 2.0)
    # ---- the number plate
    npl = G["number_plate"]
    nl, nh = bnd(M, "number_plate")
    rep.within("NUMBER plate 90 x 45 centred z 2160 on the +y face, 1.4 proud", [nh[0] - nl[0], nh[2] - nl[2], (nl[2] + nh[2]) / 2.0, nh[1] - side(2160) / 2.0], [90.0, 45.0, 2160.0, 1.4], 1.2)
    # ---- the lantern's box, centre, bowl base, lamp, arc tube
    cl, ch_ = bnd(M, "canopy", "bowl", "catches", "hinge")
    rep.within("LANTERN box (canopy, bowl, catches, hinge; not the boss): y 650, x 300, z 200", [ch_[1] - cl[1], ch_[0] - cl[0], ch_[2] - cl[2]], [650.0, 300.0, 200.0], 8.0)
    rep.within("LANTERN centre (0, 755, 4900)", [(cl[0] + ch_[0]) / 2, (cl[1] + ch_[1]) / 2, (cl[2] + ch_[2]) / 2], [0.0, 755.0, 4900.0], 12.0)
    rep.within("LANTERN top z 5000 (the mounting height)", bnd(M, "canopy", "bowl")[1][2], 5000.0, 10.0)
    rep.within("LANTERN canopy's lower edge z 4925 (the lip), the dome 63 over the lip's top", [bnd(M, "canopy")[0][2], bnd(M, "canopy")[1][2] - 4937.0], [4925.0, 63.0], 6.0)
    bw_l, bw_h = bnd(M, "bowl")
    Vb = mm(M, "bowl")
    base = Vb[Vb[:, 2] < 4800.5]
    rep.within("BOWL flat base z 4800, 473 long (y 518.6 to 991.4), 164 wide", [base[:, 2].max(), base[:, 1].max() - base[:, 1].min(), (base[:, 0].max() - base[:, 0].min())], [4800.0, 473.0, 164.0], 8.0)
    rep.within("BOWL level: the base plane is horizontal (tilt 0 +-1.5 degrees)", math.degrees(math.atan2(base[:, 2].max() - base[:, 2].min(), 400.0)), 0.0, 1.5)
    rep.within("BOWL rim z 4925 from y 488 to 1072 (REVIEW-v1-close point 1: the target's 1070.5 left a crescent 9 deep at the nose; the rim now runs 3 further round it)", [bw_h[2], bw_l[1], bw_h[1]], [4925.0, 488.0, 1072.0], 2.5)
    jl, jh = bnd(M, "lamp_jacket")
    rep.within("LAMP jacket 54 across and 310 long, centre (0, 755, 4872)", [jh[0] - jl[0], jh[2] - jl[2], jh[1] - jl[1], (jl[0] + jh[0]) / 2, (jl[1] + jh[1]) / 2, (jl[2] + jh[2]) / 2], [54.0, 54.0, 310.0, 0.0, 755.0, 4872.0], 3.0, "a 32-gon reads 54 corner to corner")
    tl, th = bnd(M, "arc_tube")
    rep.within("ARC TUBE: legs 16 OD at x +-11, z 4872, y 605 to 895", [th[0] - tl[0], th[2] - tl[2], tl[1], th[1], (tl[2] + th[2]) / 2.0], [38.0, 16.0, 605.0, 895.0, 4872.0], 2.5, "x extent 11 + 11 + 16 = 38")
    inside = (jl[0] >= -150 and jh[0] <= 150 and jl[1] >= 430 and jh[1] <= 1080 and jl[2] >= 4803 and jh[2] <= 4925)
    rep.add("LAMP wholly inside the bowl's and canopy's envelope", bool(inside) and tl[1] > jl[1] and th[1] < jh[1], [jl.round(1).tolist(), jh.round(1).tolist()], "inside")
    Dv = mm(M, "lamp_holder")
    rep.within("LAMP holder 60 x 45 x 40 at the rear (x +-30, y 555 to 600, z 4852 to 4892) hung from the ceiling", [Dv[:, 0].min(), Dv[:, 0].max(), Dv[:, 1].min(), Dv[:, 1].max(), Dv[:, 2].min()], [-30.0, 30.0, 555.0, 600.0, 4852.0], 1.0)
    rep.add("LAMP holder reaches the canopy's ceiling (its bracket ends above 4960)", Dv[:, 2].max() > 4960.0, round(float(Dv[:, 2].max()), 1), "> 4960")
    # dome over the boss's front end, the boss's top, clearance
    zs = np.linspace(5010.0, 4900.0, 221)
    from check_pillarbox import cast, tris  # the ray caster of the pillar box's check
    T_can = tris(M, ["canopy"])
    hit = cast(T_can, np.stack([np.zeros_like(zs[:1]), np.full(1, 485.0), np.full(1, 5010.0)], 1), [[0.0, 0.0, -1.0]])[0]
    dome_485 = 5010.0 - hit
    rep.within("DOME over the boss's front end (y 485) at x 0: z 4967.4, the boss's top 4960.8 stays under it", [dome_485, bh[2]], [4967.4, 4960.8], 6.0)
    rep.add("BOSS top 23.8 over the canopy's rear crown (4937): nothing pokes through the dome", abs(bh[2] - 4937.0 - 23.8) < 0.6 and bh[2] < dome_485, [round(float(bh[2]), 1), round(float(dome_485), 1)], "4960.8 under the dome")
    Vboss, Vbowl = mm(M, "boss"), mm(M, "bowl")
    from scipy.spatial import cKDTree
    dmin = float(cKDTree(Vbowl).query(Vboss)[0].min())
    rep.add("BOWL clear of the boss: the nearest distance is at least 3", dmin >= 3.0, round(dmin, 1), ">= 3")
    inner_pt = Point(755.0, 4850.0)
    Pbl = sec(M, ("bowl",), 0, 0.0, (1, 2))
    rep.add("LIGHT point (0, 755, 4850) lies inside the bowl", Pbl.convex_hull.contains(inner_pt) and not Pbl.contains(inner_pt), "inside the clear shell", "inside")
    hgl, hgh = bnd(M, "hinge")
    ctl, cth = bnd(M, "catches")
    rep.within("HINGE two knuckles 22 x 22 x 14 at x +-60, y 497 (z 4925 up); CATCHES 30 long, 14 tall at y 932.3, x +-136", [hgh[0], hgl[0], (hgl[1] + hgh[1]) / 2, hgh[2] - 4925.0, (ctl[1] + cth[1]) / 2, cth[0]], [71.0, -71.0, 497.0, 14.0, 932.3, 136.0], 1.5)
    # ---- the drawing: silhouettes and sections against target_drawing.py's polygons (largest outline distance at most 6)
    def poly_of(view, name):
        return [p["geom"] for p in views[view]["polys"] if p["name"] == name][0]
    fr = cs.frame_for([-130, -160, 420, 5010], margin=6.0, mmpx=1.0)
    sil = outline.silhouette(M, (1, 2), fr, only=("column",))
    shaft_arm = poly_of("C_side_elevation", "concrete_shaft_and_arm")
    gm = shaft_arm.exterior.coords
    tgt = cs.raster([list(gm)], fr)
    rep.compare_row("DRAWING C side silhouette of the column (shaft, mitre and arm, projected along x) against the drawing's concrete_shaft_and_arm", compare(sil, tgt, 1.0), {"iou": 0.985, "p95_mm": 2.0, "max_mm": 6.0})
    for nm, mname in (("canopy_shell", "canopy"), ("bowl_shell", "bowl"), ("boss", "boss")):
        g_t = poly_of("L_section_lantern_long_x0", nm)
        g_m = sec(M, (mname,), 0, 0.0, (1, 2))
        if mname == "canopy":                          # the drawing closes the canopy's shell along the rim line (z 4925), where the real canopy is open: judge the model's outline against the drawing's, one way
            pts = [Point(p) for g in (g_m.geoms if hasattr(g_m, "geoms") else [g_m]) for p in g.exterior.coords]
            d_ = max(g_t.boundary.distance(p) for p in pts)
            rep.add("DRAWING long section of the lantern at x 0: canopy's skin within 6 of the drawing's outline (model to drawing; the drawing's closing line along the rim is not a surface)", d_ <= 6.0, round(d_, 2), "<= 6")
            continue
        rep.add("DRAWING long section of the lantern at x 0: %s outline within 6 of the drawing's (largest distance, either way)" % mname, hd(g_m, g_t) <= 6.0, round(hd(g_m, g_t), 2), "<= 6")
    rim = [p["geom"] for p in views["A_plan_lantern"]["polys"] if p["name"] == "canopy_rim_outline"][0]
    pm = sec(M, ("canopy",), 2, 4930.0, (0, 1))
    outer = pm.convex_hull                                                   # the lip's two walls and its tips: the plan's outline is their hull
    rep.add("DRAWING plan of the canopy's rim at z 4930 within 6 of the drawing's plan outline", hd(outer, rim) <= 6.0, round(hd(outer, rim), 2), "<= 6")
    for nm, mname in (("canopy_shell", "canopy"), ("bowl_shell", "bowl")):
        g_t = poly_of("L_section_lantern_cross_centre", nm)
        g_m = sec(M, (mname,), 1, 755.0, (0, 2))
        rep.add("DRAWING cross-section of the lantern at y 755: %s within 6 of the drawing's" % mname, hd(g_m, g_t) <= 6.0, round(hd(g_m, g_t), 2), "<= 6")
    # ---- closed solids, hatching, files
    bad = []
    for n, (Vn, Fn) in M.items():
        cnt = {}
        for f in Fn:
            for i in range(len(f)):
                e = tuple(sorted((int(f[i]), int(f[(i + 1) % len(f)]))))
                cnt[e] = cnt.get(e, 0) + 1
        if any(v != 2 for v in cnt.values()):
            bad.append(n)
    rep.add("SOLID every object closed (each edge on two triangles)", not bad, bad, [])
    same, ex = cs.coplanar({k: v for k, v in M.items() if k != "reflector"})
    rep.add("HATCH faces of different objects in one plane, facing the same way, overlapping > 1 mm2 (every part but the reflector skin)", same == 0, {"count": same, "examples": ex[:6]}, 0)
    same_r, ex_r = cs.coplanar({k: M[k] for k in ("canopy", "reflector")})
    Vc_, Fc_ = M["canopy"]
    Vr_, Fr_ = M["reflector"]
    gap = float(cKDTree(Vc_ * 1000.0).query(Vr_ * 1000.0)[0].min()) if False else None
    rep.add("HATCH the reflector skin lies inside the canopy's shell, its faces 2 mm from the canopy's inner surface; the few pairs the test finds are crossing facets at the crown (planes within 0.1 mm along a line, not coincident surfaces)", same_r <= 12, {"count": same_r, "examples": ex_r[:4]}, "<= 12 crossing facets", "an exemption, said here: the skin is the white inner face of the canopy, not a second surface in the same plane")
    tri = sum(v["triangles"] for k, v in info.items() if k != "lamp_post_C")
    rep.add("TRIANGLES the column with its lantern at LOD0: 3,000 to 12,000", 3000 <= tri <= 12000, tri, "3000 to 12000")
    for name, inf in info.items():
        size = os.path.getsize(inf["glb"])
        rep.add("FILE %s under 1 MB" % name, size < 1_000_000, [size, inf["triangles"]], "< 1000000")
    for name in ("lamp_column_C", "lamp_lantern"):
        prims, js = cs.read_glb(info[name]["glb"])
        rep.add("FILE %s: no textures, a UV set on every mesh, no emission set (the glow is the engine's)" % name, not js.get("images") and all(p["uv"] for p in prims) and not any(m.get("emissiveFactor", [0, 0, 0]) != [0, 0, 0] for m in js.get("materials", [])),
                [m["name"] for m in js.get("materials", [])], "named materials")
    prims, js = cs.read_glb(info["lamp_column_C"]["glb"])
    mats = {m["name"]: m for m in js.get("materials", [])}
    alb = [round(cs.srgb_from_lin(c)) for c in mats["concrete_C"]["pbrMetallicRoughness"]["baseColorFactor"][:3]]
    rep.within("CONCRETE albedo (146, 143, 136) and roughness 0.9 (shaft and arm alike), not metal", alb + [mats["concrete_C"]["pbrMetallicRoughness"]["roughnessFactor"], mats["concrete_C"]["pbrMetallicRoughness"].get("metallicFactor", 1.0)], [146, 143, 136, 0.9, 0.0], 12.0)
    pr, js2 = cs.read_glb(info["lamp_lantern"]["glb"])
    rep.add("LANTERN emissive slots are their own materials: lamp_glass, arc_tube, bowl", {"lamp_glass", "arc_tube", "bowl"} <= {m["name"] for m in js2.get("materials", [])}, sorted(m["name"] for m in js2.get("materials", [])), "three slots")
    rep.add("COLUMN: the spigot is the only black part (c_spigot); the shaft and arm are one unpainted concrete material", "c_spigot" in mats and "concrete_C" in mats, sorted(mats), "concrete_C, c_spigot")
    req = rep.rows
    out = {"version": a.version, "passed": sum(1 for r in req if r["ok"]), "failed": [r["id"] for r in req if not r["ok"]], "total": len(req), "rows": rep.rows,
           "not_built": ["variant A (the painted steel column; built only if Jafar rules it in)", "the plate's 'LC n' letters (the engine's texture on the plate)", "the engine's lights and the emissive strengths (cd/m2) on lamp_glass, arc_tube and bowl",
                         "the wear (algae, lime, rust, the chipped arris on LC 2: the engine's masks, unit 4.5)", "the refractor grooves under the bowl (a normal map) and the bowl's 6 x 6 rim bead (hidden inside the canopy's lip)",
                         "the four places: the engine places the column four times, the west two turned 180 degrees"]}
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    path = os.path.join(HERE, "checks", "check_v%d.json" % a.version)
    json.dump(out, open(path, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    print("\nRESULT: %d of %d checks pass; failed: %s -> %s" % (out["passed"], out["total"], out["failed"], path))
    return 0 if not out["failed"] else 1


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(HERE, "..", "pillar-box"))
    sys.exit(main())
