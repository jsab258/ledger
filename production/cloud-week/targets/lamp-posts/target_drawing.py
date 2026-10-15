#!/usr/bin/env python
"""Draws the lamp-post target from target.json alone: elevations, plans and sections as filled polygons in MILLIMETRES.

    /home/user/.bpyenv/bin/python target_drawing.py OUT_DIR [--json POLYGONS.json] [--target target.json] [--mm 1.0] [--no-pictures]

Writes POLYGONS.json (default OUT_DIR/lamp_posts_polygons.json):
    {"units": "mm", "views": {name: {"u": "...", "v": "...", "polygons": [{"name", "role", "points": [[u, v], ...]}]}}}
and one PNG per view in OUT_DIR at --mm millimetres a pixel (default 1). Pictures never go into git outside production/previews/.

Axes of every view (u across the picture, v up it):
  *_side_elevation        u = y (toward the carriageway), v = z   looking along -x: the arm is seen in profile
  *_front_elevation       u = x, v = z   seen from the carriageway;  *_back_elevation: seen from the building line (the door)
  *_plan_*                u = x, v = y   (y up the page, toward the carriageway)
  *_section_*             as named in the view's own "u" and "v"
Variant C (the main build) and variant A are both drawn in full, the lantern's sections once (L_), P and W1 as elevations. The module is imported by self_check.py (build_views, lower_edges, c_side)."""
import argparse
import json
import math
import os
import sys

from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
ROLE_COLOUR = {"paint": (38, 38, 42), "canopy": (126, 124, 120), "bowl": (222, 214, 178), "lamp": (255, 176, 28), "bowl_glow": (255, 137, 0), "detail": (190, 60, 50),
               "groove": (10, 10, 10), "plate": (232, 230, 222), "concrete": (150, 147, 140), "outline": (0, 0, 0), "steel": (70, 70, 76), "pod": (96, 98, 110),
               "wall": (200, 190, 175)}


def load(path=None):
    return json.load(open(path or os.path.join(HERE, "target.json")))


# ---------------------------------------------------------------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------------------------------------------------------------
def profile_poly(rz):
    """(radius, z) outline of a lathe -> the whole elevation polygon in (u, v) (mirrored about the axis)"""
    pts = [(r, z) for r, z in rz] + [(-r, z) for r, z in reversed(rz)]
    out = []
    for p in pts:
        if not out or abs(p[0] - out[-1][0]) > 1e-9 or abs(p[1] - out[-1][1]) > 1e-9:
            out.append(p)
    return Polygon(out).buffer(0)


def tube_poly(centreline, od):
    return LineString([tuple(p) for p in centreline]).buffer(od / 2.0, cap_style=2, join_style=1, resolution=24)


def interp(table, y):
    if y <= table[0][0]:
        return table[0][1]
    if y >= table[-1][0]:
        return table[-1][1]
    for (y0, v0), (y1, v1) in zip(table, table[1:]):
        if y0 <= y <= y1:
            return v0 + (v1 - v0) * (y - y0) / (y1 - y0) if y1 > y0 else v0
    return table[-1][1]


def dome_points(w, base, top, n=40):
    xs = [-w + 2 * w * i / n for i in range(n + 1)]
    return [(x, base + (top - base) * math.sqrt(max(0.0, 1 - (x / w) ** 2))) for x in xs]


def P(name, role, geom):
    return {"name": name, "role": role, "geom": geom}


# ---------------------------------------------------------------------------------------------------------------------------------
# the lantern (variants A and C share it): T["geometry"]["lantern"], its centre y is envelope.centre[1] (705 since try 2)
# ---------------------------------------------------------------------------------------------------------------------------------
def lantern_parts(T):
    L = T["geometry"]["lantern"]
    can, bowl, lamp = L["canopy"], L["bowl"], L["lamp"]
    rim, dome0 = can["rim_z"], can["dome_base_z"]
    plan_half, top = can["plan_half_width"], can["top_z_along_y"]
    y0, y1 = plan_half[0][0], plan_half[-1][0]
    yc = L["envelope"]["centre"][1]
    rim_plan = Polygon([(w, y) for y, w in plan_half] + [(-w, y) for y, w in reversed(plan_half)]).buffer(0)
    bowl_rim_plan = rim_plan.buffer(-bowl["rim_inset"])
    base_half = bowl["base_plan_half_width"]
    base_plan = Polygon([(w, y) for y, w in base_half] + [(-w, y) for y, w in reversed(base_half)]).buffer(0)
    side_top = [(y, interp(top, y)) for y in range(int(y0), int(y1) + 1, 5)]
    canopy_side = Polygon(side_top + [(y1, rim), (y0, rim)]).buffer(0)
    curve = [tuple(p) for p in bowl["long_section_rear_curve_yz"]]               # rim (rear) -> base
    front = [tuple(p) for p in bowl["long_section_front_curve_yz"]]               # base -> rim (front): written out since the second review (narrow point 2)
    bowl_side = Polygon(curve + front).buffer(0)
    lamp_side = box(lamp["centre"][1] - lamp["length"] / 2, lamp["centre"][2] - lamp["od"] / 2, lamp["centre"][1] + lamp["length"] / 2, lamp["centre"][2] + lamp["od"] / 2)
    h = lamp["holder"]
    holder_side = box(h["y"][0], h["z"][0], h["y"][1], h["z"][1])
    tube = lamp["arc_tube"]
    ty0, ty1 = tube["y"]
    # the half-torus: centre between the legs at (0, legs_straight_to_y), radius 11, from the left leg round the front to the right leg
    arc = [(tube["bend_centreline_radius"] * math.cos(math.radians(a)), tube["legs_straight_to_y"] + tube["bend_centreline_radius"] * math.sin(math.radians(a))) for a in range(0, 181, 10)]
    tube_plan = unary_union([box(x - tube["leg_od"] / 2, ty0, x + tube["leg_od"] / 2, tube["legs_straight_to_y"]) for x in tube["leg_x"]] + [LineString(arc).buffer(tube["leg_od"] / 2.0)])
    tube_side = box(ty0, tube["z"] - tube["leg_od"] / 2, ty1, tube["z"] + tube["leg_od"] / 2)

    def canopy_cross(y):
        w = interp(plan_half, y)
        t = interp(top, y)
        if w < 1:
            return Polygon()
        pts = dome_points(w, dome0, t) if t > dome0 + 0.01 else [(-w, dome0), (w, dome0)]
        return Polygon([(-w, rim), (w, rim)] + [(x, z) for x, z in reversed(pts)]).buffer(0)

    def bowl_cross(y):
        wr = interp(plan_half, y) - bowl["rim_inset"]
        bw = interp(base_half, y) if base_half[0][0] <= y <= base_half[-1][0] else 0.0
        sec = bowl["section_at_centre_half_width_z"]
        h0, h1 = sec[0][0], sec[-1][0]
        pts = [((hw - h0) / (h1 - h0) * (wr - bw) + bw, z) for hw, z in sec]
        return Polygon([(x, z) for x, z in pts] + [(-x, z) for x, z in reversed(pts)]).buffer(0)
    boss = L["boss"]
    a0 = boss["axis_from"]
    ang = math.radians(boss["axis_deg_above_horizontal"])
    a1 = (a0[1] + boss["length"] * math.cos(ang), a0[2] + boss["length"] * math.sin(ang))
    boss_side = LineString([(a0[1], a0[2]), a1]).buffer(boss["od"] / 2.0, cap_style=2)
    hg = L["hinge"]
    hinge_side = box(hg["y"] - hg["size"][0] / 2, rim, hg["y"] + hg["size"][0] / 2, rim + hg["size"][2])
    cs = L["catches"]
    catch_side = box(cs["y"] - cs["size_y_z_proud"][0] / 2, rim - cs["size_y_z_proud"][1] / 2, cs["y"] + cs["size_y_z_proud"][0] / 2, rim + cs["size_y_z_proud"][1] / 2)
    return {"rim_plan": rim_plan, "bowl_rim_plan": bowl_rim_plan, "base_plan": base_plan, "canopy_side": canopy_side, "bowl_side": bowl_side, "lamp_side": lamp_side,
            "holder_side": holder_side, "boss_side": boss_side, "hinge_side": hinge_side, "catch_side": catch_side, "canopy_cross": canopy_cross, "bowl_cross": bowl_cross,
            "tube_plan": tube_plan, "tube_side": tube_side, "y0": y0, "y1": y1, "yc": yc, "rim": rim, "dome0": dome0, "L": L}


def lower_edges(T, z):
    """(left, right) x of variant A's lower column outline at height z (mm), centred on the axis; None outside the profile"""
    rz = T["geometry"]["A"]["lower"]["outer_rz"]
    for (r0, z0), (r1, z1) in zip(rz[1:-1], rz[2:-1]):
        if z0 <= z <= z1 and z1 > z0:
            r = r0 + (r1 - r0) * (z - z0) / (z1 - z0)
            return -r, r
    return None


def c_side(T, z):
    """the concrete shaft's side (mm) at height z, linear between the listed (z, side, chamfer) points"""
    pts = T["geometry"]["C"]["shaft"]["points_z_side_chamfer"]
    for (z0, s0, _), (z1, s1, _) in zip(pts, pts[1:]):
        if z0 <= z <= z1 and z1 > z0:
            return s0 + (s1 - s0) * (z - z0) / (z1 - z0)
    return pts[-1][1]


def chamfered_square(side, ch):
    h = side / 2.0
    return Polygon([(-h + ch, -h), (h - ch, -h), (h, -h + ch), (h, h - ch), (h - ch, h), (-h + ch, h), (-h, h - ch), (-h, -h + ch)])


def rounded_box(x0, z0, x1, z1, r):
    return box(x0 + r, z0 + r, x1 - r, z1 - r).buffer(r, resolution=8)


# ---------------------------------------------------------------------------------------------------------------------------------
# views
# ---------------------------------------------------------------------------------------------------------------------------------
def build_views(T):
    V = {}
    A = T["geometry"]["A"]
    low = A["lower"]
    lp = lantern_parts(T)
    yc = lp["yc"]
    column_sil = profile_poly(low["outer_rz"])
    br = A["bracket"]
    stem_arm = tube_poly(br["centreline_yz"], br["tube_od_stem"])
    sk = A["socket"]
    door, pl = A["door"], A["plate"]
    sl_r = low["outer_rz"][2][0]
    rz = low["outer_rz"]
    socket_r = sk["od"] / 2.0

    # ---- A: side elevation (u = y, v = z) --------------------------------------------------------------------------------------------
    side = [P("sleeve_cone_shaft_socket", "paint", column_sil), P("stem_bend_arm", "paint", stem_arm), P("boss", "canopy", lp["boss_side"]),
            P("canopy", "canopy", lp["canopy_side"]), P("bowl", "bowl", lp["bowl_side"]), P("lamp", "lamp", lp["lamp_side"]), P("lamp_holder", "canopy", lp["holder_side"]),
            P("hinge", "canopy", lp["hinge_side"]), P("catch", "canopy", lp["catch_side"]),
            P("door_proud_edge_on_minus_y", "detail", box(-sl_r - door["proud"], door["z"][0], -sl_r, door["z"][1]))]
    V["A_side_elevation"] = {"u": "y (toward the carriageway)", "v": "z", "polys": side}

    # ---- A: carriageway-side elevation (u = x, v = z) ------------------------------------------------------------------------------
    can_front = unary_union([lp["canopy_cross"](y) for y in range(int(lp["y0"]) + 5, int(lp["y1"]) - 4, 10)])
    bowl_front = unary_union([lp["bowl_cross"](y) for y in range(int(lp["y0"]) + 100, int(lp["y1"]) - 70, 15)])
    arm_top = br["arm_end"][1] + br["tube_od_stem"] / 2
    front_common = [P("sleeve_cone_shaft_socket", "paint", column_sil),
                    P("stem_and_arm_end_on", "paint", box(-br["tube_od_stem"] / 2, br["stem_from_z"], br["tube_od_stem"] / 2, arm_top)),
                    P("canopy", "canopy", can_front), P("bowl", "bowl", bowl_front)]
    plate_w = 2 * 33.0 * math.sin(math.radians(pl["arc_deg"] / 2.0))
    front = list(front_common) + [P("number_plate", "plate", box(-plate_w / 2, pl["z_centre"] - pl["size"][1] / 2, plate_w / 2, pl["z_centre"] + pl["size"][1] / 2))]
    V["A_front_elevation_carriageway_side"] = {"u": "x", "v": "z", "polys": front}

    # ---- A: back elevation (from the building line: the door and the socket's two set screws) ----------------------------------------------
    dw = 2 * sl_r * math.sin(math.radians(door["arc_deg"] / 2.0))
    dr = door["corner_radius"]
    dbox = rounded_box(-dw / 2, door["z"][0], dw / 2, door["z"][1], dr)
    groove = rounded_box(-dw / 2 - door["joint_groove"]["width"], door["z"][0] - door["joint_groove"]["width"], dw / 2 + door["joint_groove"]["width"], door["z"][1] + door["joint_groove"]["width"],
                         door["joint_groove"]["corner_radius"] + door["joint_groove"]["width"]).difference(dbox)
    back = list(front_common) + [P("door", "detail", dbox), P("door_groove", "groove", groove)]
    for zs in door["screws"]["z"]:
        back.append(P("door_screw", "detail", Point(0, zs).buffer(door["screws"]["head_od"] / 2.0, resolution=16)))
    for zs in sk["set_screws"]["z"]:
        back.append(P("socket_set_screw", "detail", Point(0, zs).buffer(sk["set_screws"]["head_od"] / 2.0, resolution=12)))
    V["A_back_elevation_building_side"] = {"u": "x (seen from the building line)", "v": "z", "polys": back}

    # ---- A: plans (u = x, v = y) -----------------------------------------------------------------------------------------------------
    sleeve = Point(0, 0).buffer(sl_r, resolution=48)
    th0, th1 = -90 - door["arc_deg"] / 2.0, -90 + door["arc_deg"] / 2.0
    ring = lambda r: [(r * math.cos(math.radians(th0 + (th1 - th0) * i / 24)), r * math.sin(math.radians(th0 + (th1 - th0) * i / 24))) for i in range(25)]  # noqa: E731
    door_sector = Polygon(ring(sl_r + door["proud"]) + list(reversed(ring(sl_r - 4)))).buffer(0)
    V["A_plan_z500_sleeve_and_door"] = {"u": "x", "v": "y", "polys": [P("sleeve", "paint", sleeve), P("door_plate", "detail", door_sector)]}
    shaft_r = lambda z: lower_edges(T, z)[1]  # noqa: E731
    V["A_plan_z2000_shaft"] = {"u": "x", "v": "y", "polys": [P("shaft", "paint", Point(0, 0).buffer(shaft_r(2000), resolution=48)),
                                                              P("number_plate_z2160_arc", "plate", Point(0, 0).buffer(shaft_r(2160) + pl["proud"], resolution=48).difference(Point(0, 0).buffer(shaft_r(2160))).intersection(
                                                                  Polygon([(0, 0)] + [(100 * math.cos(math.radians(90 - pl["arc_deg"] / 2 + pl["arc_deg"] * i / 20)), 100 * math.sin(math.radians(90 - pl["arc_deg"] / 2 + pl["arc_deg"] * i / 20))) for i in range(21)])))]}
    ss = sk["set_screws"]
    V["A_plan_z4500_socket_and_stem"] = {"u": "x", "v": "y", "polys": [P("socket", "paint", Point(0, 0).buffer(socket_r, resolution=48)), P("stem", "steel", Point(0, 0).buffer(br["tube_od_stem"] / 2.0, resolution=32)),
                                                                     P("set_screw_upper", "detail", Point(0, -socket_r).buffer(ss["head_od"] / 2.0)),
                                                                     P("set_screw_lower_same_azimuth", "detail", Point(0, -socket_r).buffer(ss["head_od"] / 2.0 * 0.6))]}
    lamp_l = lp["L"]["lamp"]
    lamp_plan = box(-lamp_l["od"] / 2, lamp_l["centre"][1] - lamp_l["length"] / 2, lamp_l["od"] / 2, lamp_l["centre"][1] + lamp_l["length"] / 2)
    arm_plan = LineString([(0, 0), (0, br["arm_end"][0])]).buffer(br["tube_od_stem"] / 2.0, cap_style=2)
    boss_plan = box(-30, br["arm_end"][0], 30, br["arm_end"][0] + lp["L"]["boss"]["length"])
    lantern_plan_polys = [P("canopy_rim_outline", "canopy", lp["rim_plan"]), P("bowl_rim", "bowl", lp["bowl_rim_plan"]), P("bowl_flat_base", "bowl_glow", lp["base_plan"]),
                          P("lamp", "lamp", lamp_plan), P("arc_tube", "bowl_glow", lp["tube_plan"]), P("boss", "canopy", boss_plan)]
    V["A_plan_lantern"] = {"u": "x", "v": "y", "polys": lantern_plan_polys + [P("arm_and_stem_in_plan", "steel", arm_plan), P("socket_top", "paint", Point(0, 0).buffer(socket_r, resolution=48))]}

    # ---- the lantern's sections (shared by A and C) ---------------------------------------------------------------------------------------
    cano = lp["canopy_side"]
    can_in = Polygon([(y, interp(T["geometry"]["lantern"]["canopy"]["top_z_along_y"], y) - 2.5) for y in range(int(lp["y0"]) + 3, int(lp["y1"]) - 2, 5)] + [(lp["y1"] - 3, lp["rim"]), (lp["y0"] + 3, lp["rim"])]).buffer(0)
    canopy_shell = cano.difference(can_in)
    bowl_o = lp["bowl_side"]
    bowl_shell = bowl_o.difference(bowl_o.buffer(-3.0))
    V["L_section_lantern_long_x0"] = {"u": "y", "v": "z", "polys": [P("canopy_shell", "canopy", canopy_shell), P("bowl_shell", "bowl", bowl_shell), P("lamp", "lamp", lp["lamp_side"]),
                                                                    P("arc_tube", "bowl_glow", lp["tube_side"]), P("lamp_holder", "canopy", lp["holder_side"]), P("boss", "canopy", lp["boss_side"]), P("hinge", "canopy", lp["hinge_side"])]}
    cc, bc = lp["canopy_cross"](yc), lp["bowl_cross"](yc)
    V["L_section_lantern_cross_centre"] = {"u": "x", "v": "z", "polys": [P("canopy_shell", "canopy", cc.difference(cc.buffer(-2.5))), P("bowl_shell", "bowl", bc.difference(bc.buffer(-3.0))),
                                                                         P("lamp_jacket_end_on", "lamp", Point(0, 4872).buffer(27, resolution=24)),
                                                                         P("arc_tube_legs_end_on", "bowl_glow", unary_union([Point(x, 4872).buffer(8, resolution=12) for x in lp["L"]["lamp"]["arc_tube"]["leg_x"]])),
                                                                         P("catch_left", "canopy", box(-136 - 3 - 7, lp["rim"] - 7, -136 - 3, lp["rim"] + 7)),
                                                                         P("catch_right", "canopy", box(136 + 3, lp["rim"] - 7, 136 + 3 + 7, lp["rim"] + 7))]}
    V["A_section_bracket_detail"] = {"u": "y", "v": "z", "polys": [P("socket_and_shaft_top", "paint", column_sil.intersection(box(-80, 4300, 80, 4700))), P("stem_bend_arm", "steel", stem_arm), P("boss", "canopy", lp["boss_side"]),
                                                                   P("canopy", "canopy", lp["canopy_side"].intersection(box(400, 4900, 640, 5010)))]}
    V["A_section_lower_profile_rz"] = {"u": "r (radius)", "v": "z", "polys": [P("lathe_outline_half", "paint", Polygon([(r, z) for r, z in rz]).buffer(0).intersection(box(0, -160, 80, 1200)))]}

    # ---- C: the precast concrete column, the main build ----------------------------------------------------------------------------------
    C = T["geometry"]["C"]
    cs_ = C["shaft"]
    cb = C["bracket"]
    sp = C["spigot"]
    cd = C["door"]
    foot, topw, ch = cs_["side_at_z0"], cs_["side_at_top"], cs_["chamfer"]
    zt = cs_["top_z"]
    hid = cs_["hidden_root"]
    spts = cs_["points_z_side_chamfer"]
    c_shaft_side = Polygon([(s_ / 2, z_) for z_, s_, _ in spts] + [(-s_ / 2, z_) for z_, s_, _ in reversed(spts)])
    # the concrete arm (second review, R1): 110 square, level at the axis, from the shaft's -y face to y 400, a sharp mitre (outer corner R20, inner fillet R10)
    ax, half, aend, ach = cb["axis_z"], cb["section"]["square"] / 2.0, cb["arm_end_y"], 5.0
    ytop, ybot = -c_side(T, ax + half) / 2.0, c_side(T, ax - half) / 2.0
    r_out, r_in = cb["mitre"]["outer_corner_radius"], cb["mitre"]["inner_fillet_radius"]
    arm_side = Polygon([(-40.0, ax - half), (aend - ach, ax - half), (aend, ax - half + ach), (aend, ax + half - ach), (aend - ach, ax + half), (-40.0, ax + half)])
    outer_cut = box(ytop - 2.0, ax + half - r_out, ytop + r_out, ax + half + 2.0).difference(Point(ytop + r_out, ax + half - r_out).buffer(r_out, resolution=24))
    inner_fill = box(ybot, ax - half - r_in, ybot + r_in, ax - half).difference(Point(ybot + r_in, ax - half - r_in).buffer(r_in, resolution=24))
    c_shaft_arm = unary_union([c_shaft_side, arm_side, inner_fill]).difference(outer_cut)
    spigot_side = box(sp["y"][0], ax - sp["od"] / 2.0, sp["y"][1], ax + sp["od"] / 2.0)
    arm_end_on = chamfered_square(2 * half, cb["section"]["chamfer"])
    arm_end_on = Polygon([(x, z + ax) for x, z in arm_end_on.exterior.coords])
    spigot_end_on = Point(0, ax).buffer(sp["od"] / 2.0, resolution=32)
    zr0, zr1 = cd["recess"]["z"]
    p0, p1 = cd["plate"]["z"]
    pr = cd["plate"]["proud"]
    plate_edge = Polygon([(-c_side(T, p0) / 2 - pr, p0), (-c_side(T, p0) / 2, p0), (-c_side(T, p1) / 2, p1), (-c_side(T, p1) / 2 - pr, p1)])
    npl = C["number_plate"]
    npz0, npz1 = npl["z_centre"] - npl["size"][1] / 2, npl["z_centre"] + npl["size"][1] / 2
    num_edge = Polygon([(c_side(T, npz0) / 2, npz0), (c_side(T, npz0) / 2 + npl["proud"], npz0), (c_side(T, npz1) / 2 + npl["proud"], npz1), (c_side(T, npz1) / 2, npz1)])
    V["C_side_elevation"] = {"u": "y (toward the carriageway)", "v": "z", "polys": [P("concrete_shaft_and_arm", "concrete", c_shaft_arm), P("steel_spigot_od42", "paint", spigot_side),
                                                                                    P("boss", "canopy", lp["boss_side"]), P("canopy", "canopy", lp["canopy_side"]), P("bowl", "bowl", lp["bowl_side"]), P("lamp", "lamp", lp["lamp_side"]),
                                                                                    P("door_plate_edge_on", "detail", plate_edge), P("number_plate_edge_on", "plate", num_edge)]}
    # front (the +y face seen from the carriageway)
    c_front_shaft = c_shaft_side
    chamfer_lines = [P("arris_chamfer_line_left", "groove", Polygon([(-foot / 2 + ch - 1, 0), (-foot / 2 + ch + 1, 0)] + [(-s_ / 2 + ch + 1, z_) for z_, s_, _ in spts[1:]] + [(-s_ / 2 + ch - 1, z_) for z_, s_, _ in reversed(spts[1:])])),
                     P("arris_chamfer_line_right", "groove", Polygon([(foot / 2 - ch - 1, 0), (foot / 2 - ch + 1, 0)] + [(s_ / 2 - ch + 1, z_) for z_, s_, _ in spts[1:]] + [(s_ / 2 - ch - 1, z_) for z_, s_, _ in reversed(spts[1:])]))]
    c_front_common = [P("concrete_shaft", "concrete", c_front_shaft), P("concrete_arm_end_on", "concrete", arm_end_on), P("steel_spigot_end_on", "paint", spigot_end_on),
                      P("canopy", "canopy", can_front), P("bowl", "bowl", bowl_front)]
    V["C_front_elevation_carriageway_side"] = {"u": "x", "v": "z", "polys": c_front_common + chamfer_lines + [P("number_plate", "plate", box(-npl["size"][0] / 2, npz0, npl["size"][0] / 2, npz1))]}
    # back (the -y face: the recess, the plate and its two screws)
    rec_w, pl_w = cd["recess"]["width"], cd["plate"]["width"]
    c_back = c_front_common + chamfer_lines + [P("door_recess", "groove", box(-rec_w / 2, zr0, rec_w / 2, zr1)), P("door_plate", "detail", rounded_box(-pl_w / 2, p0, pl_w / 2, p1, cd["plate"]["corner_radius"]))]
    for zs in cd["plate"]["screws"]["z"]:
        c_back.append(P("door_plate_screw", "groove", Point(0, zs).buffer(cd["plate"]["screws"]["head_od"] / 2.0, resolution=16)))
    V["C_back_elevation_building_side"] = {"u": "x (seen from the building line)", "v": "z", "polys": c_back}
    # plans
    s500 = c_side(T, 500)
    c_cut = chamfered_square(s500, ch)
    recess = box(-rec_w / 2, -s500 / 2, rec_w / 2, -s500 / 2 + cd["recess"]["depth"])
    plate = box(-pl_w / 2, -s500 / 2 - pr, pl_w / 2, -s500 / 2)
    V["C_plan_z500"] = {"u": "x", "v": "y", "polys": [P("concrete_section_chamfered", "concrete", c_cut.difference(recess)), P("door_plate", "detail", plate)]}
    s2160 = c_side(T, npl["z_centre"])
    V["C_plan_z2160_number_plate"] = {"u": "x", "v": "y", "polys": [P("concrete_section_chamfered", "concrete", chamfered_square(s2160, ch)),
                                                                   P("number_plate_on_plus_y", "plate", box(-npl["size"][0] / 2, s2160 / 2, npl["size"][0] / 2, s2160 / 2 + npl["proud"]))]}
    top_sq = chamfered_square(topw, ch)
    arm_plan_poly = box(-half, ytop, half, aend)
    spigot_plan = box(-sp["od"] / 2.0, sp["y"][0], sp["od"] / 2.0, sp["y"][1])
    V["C_plan_z4985_arm_and_top"] = {"u": "x", "v": "y", "polys": [P("concrete_top_section", "concrete", top_sq), P("concrete_arm_in_plan", "concrete", arm_plan_poly), P("top_face_chamfer_inner_edge", "groove", top_sq.difference(top_sq.buffer(-cs_["top_face_chamfer_mm"], join_style=2))),
                                                                  P("steel_spigot_in_plan", "paint", spigot_plan)]}
    V["C_plan_lantern"] = {"u": "x", "v": "y", "polys": lantern_plan_polys + [P("concrete_top_and_arm", "concrete", unary_union([top_sq, arm_plan_poly])), P("steel_spigot_in_plan", "paint", spigot_plan)]}
    V["C_section_shaft_half_profile"] = {"u": "half side (x)", "v": "z", "polys": [P("concrete_half_outline", "concrete", Polygon([(0, -hid), (foot / 2, -hid), (foot / 2, 0), (topw / 2, zt), (0, zt)]))]}
    V["C_section_bracket_detail"] = {"u": "y", "v": "z", "polys": [P("concrete_shaft_top_and_arm", "concrete", c_shaft_arm.intersection(box(-100, 4300, aend + 5, zt + 5))), P("steel_spigot_od42", "paint", spigot_side),
                                                                    P("boss", "canopy", lp["boss_side"]), P("canopy", "canopy", lp["canopy_side"].intersection(box(400, 4900, 640, 5010)))]}

    # ---- P: post-top ----------------------------------------------------------------------------------------------------------------
    Pv = T["variants"]["P"]
    r4300 = lower_edges(T, 4300)[1]
    rz_p = [p for p in low["outer_rz"] if p[1] <= 1044] + [[r4300, 4300], [0, 4300]]
    pod = Pv["pod"]["profile_rz"]
    V["P_side_elevation"] = {"u": "y", "v": "z", "polys": [P("lower_column", "paint", profile_poly(rz_p)), P("pod", "pod", profile_poly(pod))]}

    # ---- W1: wall bracket -----------------------------------------------------------------------------------------------------------
    W = T["variants"]["W1"]
    wp = W["plate"]
    arm0 = (0.0, W["arm"]["from"][1] + 0.0)
    arm_end_y = W["arm"]["to_y"]
    arm_end_z = arm0[1] + arm_end_y * math.tan(math.radians(W["arm"]["rake_deg"]))
    arm_poly = LineString([arm0, (arm_end_y, arm_end_z)]).buffer(W["arm"]["od"] / 2.0, cap_style=2)
    strut_poly = LineString([(0, W["arm"]["strut"]["from"][1]), (W["arm"]["strut"]["to_arm_at_y"], arm0[1] + W["arm"]["strut"]["to_arm_at_y"] * math.tan(math.radians(W["arm"]["rake_deg"])))]).buffer(W["arm"]["strut"]["od"] / 2.0, cap_style=2)
    wall = box(-300, wp["z_centre"] - 600, 0, wp["z_centre"] + 600)
    W_plate = box(-wp["thickness"], wp["z_centre"] - wp["height"] / 2, 0, wp["z_centre"] + wp["height"] / 2)
    # the lantern's rear boss at the arm's end: the lantern is L1 shifted so that its boss axis point lies at the arm's end
    dz = arm_end_z - lp["L"]["boss"]["axis_from"][2]
    from shapely.affinity import translate
    sh = lambda g: translate(g, xoff=0, yoff=dz)  # noqa: E731
    V["W1_side_elevation"] = {"u": "y (out from the wall)", "v": "z", "polys": [P("wall", "wall", wall), P("wall_plate", "steel", W_plate), P("arm", "steel", arm_poly), P("strut", "steel", strut_poly),
                                                                             P("canopy", "canopy", sh(lp["canopy_side"])), P("bowl", "bowl", sh(lp["bowl_side"])), P("lamp", "lamp", sh(lp["lamp_side"]))]}
    return V


# ---------------------------------------------------------------------------------------------------------------------------------
# output
# ---------------------------------------------------------------------------------------------------------------------------------
def polys_of(geom):
    if geom.is_empty:
        return []
    if geom.geom_type == "Polygon":
        return [geom]
    return [g for g in getattr(geom, "geoms", []) if g.geom_type == "Polygon"]


def to_json(views):
    out = {"units": "mm", "views": {}}
    for name, v in views.items():
        items = []
        for p in v["polys"]:
            for g in polys_of(p["geom"]):
                items.append({"name": p["name"], "role": p["role"], "points": [[round(x, 3), round(y, 3)] for x, y in g.exterior.coords],
                              "holes": [[[round(x, 3), round(y, 3)] for x, y in h.coords] for h in g.interiors]})
        out["views"][name] = {"u": v["u"], "v": v["v"], "polygons": items}
    return out


def render(views, outdir, mm=1.0, margin=24):
    from PIL import Image, ImageDraw
    os.makedirs(outdir, exist_ok=True)
    paths = []
    for name, v in views.items():
        geoms = [g for p in v["polys"] for g in polys_of(p["geom"])]
        if not geoms:
            continue
        minx = min(g.bounds[0] for g in geoms)
        miny = min(g.bounds[1] for g in geoms)
        maxx = max(g.bounds[2] for g in geoms)
        maxy = max(g.bounds[3] for g in geoms)
        W = int((maxx - minx) / mm) + 2 * margin
        H = int((maxy - miny) / mm) + 2 * margin
        im = Image.new("RGB", (W, H), (244, 242, 236))
        d = ImageDraw.Draw(im)

        def px(pt):
            return ((pt[0] - minx) / mm + margin, H - ((pt[1] - miny) / mm + margin))
        # light grid every 100 mm
        gx = math.ceil(minx / 100.0) * 100
        while gx <= maxx:
            d.line([px((gx, miny)), px((gx, maxy))], fill=(222, 220, 214), width=1)
            gx += 100
        gy = math.ceil(miny / 100.0) * 100
        while gy <= maxy:
            d.line([px((minx, gy)), px((maxx, gy))], fill=(222, 220, 214), width=1)
            gy += 100
        for p in v["polys"]:
            col = ROLE_COLOUR.get(p["role"], (120, 120, 120))
            for g in polys_of(p["geom"]):
                mask = Image.new("L", (W, H), 0)
                md = ImageDraw.Draw(mask)
                md.polygon([px(c) for c in g.exterior.coords], fill=255)
                for h in g.interiors:
                    md.polygon([px(c) for c in h.coords], fill=0)
                im.paste(Image.new("RGB", (W, H), col), (0, 0), mask)
                d.line([px(c) for c in g.exterior.coords], fill=(0, 0, 0), width=1)
                for h in g.interiors:
                    d.line([px(c) for c in h.coords], fill=(0, 0, 0), width=1)
        path = os.path.join(outdir, name + ".png")
        im.save(path)
        paths.append((path, im.size))
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("--json", default=None)
    ap.add_argument("--target", default=None)
    ap.add_argument("--mm", type=float, default=1.0)
    ap.add_argument("--no-pictures", action="store_true")
    a = ap.parse_args()
    T = load(a.target)
    views = build_views(T)
    os.makedirs(a.outdir, exist_ok=True)
    jpath = a.json or os.path.join(a.outdir, "lamp_posts_polygons.json")
    json.dump(to_json(views), open(jpath, "w"))
    print("wrote", jpath, len(views), "views")
    if not a.no_pictures:
        for path, size in render(views, a.outdir, a.mm):
            print("wrote", path, size)


if __name__ == "__main__":
    main()
