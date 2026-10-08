"""Test target.json against its own sources before anything is built to it.

    python self_check.py

Groups:
  1 printed      every printed (book) dimension used comes back from target.json
  2 photo wins   every disagreement settled for the photograph is the photograph's value, not the book's
  3 photo P1     the drawing's edges (taken from target_drawing.py's polygons, not from the numbers) laid on
                 photograph P1 at a scale fitted on one dimension only, and the fractions of P1's door
  4 photo P2     the flat door variant against P2's proportions (reported where it disagrees)
  5 consistency  parts add up, nothing overlaps that should not, nothing floats (shapely on the drawings)
  6 checks       the builder's checks in target.json, evaluated on the drawings: they must hold for the target
Writes the result into target.json under "self_check" and prints a Markdown table.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import target_drawing as td  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402

TP = HERE / "target.json"
T = json.loads(TP.read_text(encoding="utf-8"))
IN = 25.4
rows = []


def check(group, name, ok, detail, kind="check"):
    rows.append({"group": group, "check": name, "pass": bool(ok), "detail": detail, "kind": kind})


def near(a, b, tol=0.15):
    return abs(a - b) <= tol


def shp(d):
    return Polygon(d["pts"], d.get("holes") or None).buffer(0)


def by_name(polys):
    return {d["name"]: d for d in polys}


P1 = T
P2 = T["variants"]["flat_door_over_shop"]["parts"]
c1, c2 = td.consts(P1), td.consts(P2)
E1 = by_name(td.elevation(P1))
E2 = by_name(td.elevation(P2))


def bnd(E, name):
    b = shp(E[name]).bounds
    return b      # x0, z0, x1, z1


L, M, F, O = P1["leaf"], P1["mouldings"], P1["frame"], P1["opening"]

# ---------------------------------------------------------------- 1. printed dimensions
printed = [
    ("leaf width 2 ft 8 in, Hasluck p.347", 32 * IN, L["width_mm"]),
    ("leaf thickness 2 in, Ellis p.93 / Hasluck p.398", 2 * IN, L["thickness_mm"]),
    ("stile 4 1/2 in, Ellis p.93 / Riley p.357", 4.5 * IN, L["stile_mm"]),
    ("top rail 5 in, Riley p.357 (Ellis 4 1/2 in overridden by P1, D8)", 5 * IN, L["top_rail_mm"]),
    ("lock rail 9 in, Ellis p.93 (P1 agrees)", 9 * IN, L["lock_rail_mm"]),
    ("groove 1/2 in, Ellis p.92", 0.5 * IN, P1["panels"]["groove_depth_mm"]),
    ("panel side play 1/8 in, Ellis p.92", IN / 8, P1["panels"]["side_play_mm"]),
    ("bolection lap 3/16 in, Ellis p.92", 3 * IN / 16, M["outside_bolection"]["lap_over_framing_mm"]),
    ("reveal 4 1/2 in, Hasluck p.346", 4.5 * IN, O["reveal_depth_mm"]),
    ("frame 4 in across, Riley p.357", 4 * IN, F["jamb_face_mm"]),
    ("frame 5 in deep, Riley p.357", 5 * IN, F["jamb_depth_mm"]),
    ("panel one-third of the door, Riley p.353", 2 * IN / 3, P1["panels"]["thickness_mm"]),
    ("F1 transom 5 x 4, Riley p.357 Fig. 667 (P2 agrees, D6)", 4 * IN, P2["frame"]["transom"]["face_height_mm"]),
    ("lab band/weatherboard: none printed anywhere", None, None),
]
for name, src, val in printed:
    if src is None:
        continue
    tol = 2.5 if "F1 transom" in name else 0.15
    check("1 printed", name, near(src, val, tol), f"source {src:.1f}, target {val:.1f}")
check("1 printed", "Ellis p.93: the handle in the middle of the lock rail's depth (F1 knob at the lock rail's centre)",
      near(P2["ironmongery"]["knob"]["centre_above_leaf_bottom_mm"], P2["leaf"]["lock_rail_centre_above_leaf_bottom_mm"], 0.5),
      f"knob {P2['ironmongery']['knob']['centre_above_leaf_bottom_mm']}, lock rail centre {P2['leaf']['lock_rail_centre_above_leaf_bottom_mm']}")
check("1 printed", "Hasluck p.398: a 'weathered' transom (sloped top zone present, both variants)",
      "slope" in F["transom"]["zones_z_mm"] and "slope" in P2["frame"]["transom"]["zones_z_mm"], "slope zone listed in both")
check("1 printed", "Ellis p.111-112: the sill's horns run beyond the frame into the wall (>= 100 mm each side)",
      P1["step"]["threshold"]["bearing_into_wall_each_side_mm"] >= 100, f"{P1['step']['threshold']['bearing_into_wall_each_side_mm']}")
check("1 printed", "Ellis p.112 Fig. 355: a brick arch on the head (T1)", P1["brick"]["arch"]["present"], "present")
check("1 printed", "Hasluck p.346: stile rebated from the solid, a stop on the outside, the leaf opening inwards",
      near(F["stop_depth_mm"] + F["rebate_depth_mm"], F["jamb_depth_mm"]) and P1["leaf"]["outside_face_y_mm"] == F["frame_outside_face_y_mm"] + F["stop_depth_mm"], "stop + rebate = frame depth")

# ---------------------------------------------------------------- 2. photographs win
IA = IN
overrides = [  # id, what, book value, target value, photo value, tolerance
    ("D1", "leaf height 6 ft 8 in, Hasluck p.347", 80 * IA, L["height_mm"], 1948.0, 0.6),
    ("D2", "muntin 4 in, Ellis p.93 / Riley p.357 (revised from the lab's 132.2)", 4 * IA, L["muntin_mm"], 120.0, 0.6),
    ("D3", "lock rail centre 2 ft 8 in less 6 in from a step, Ellis p.93", 26 * IA, L["lock_rail_centre_above_leaf_bottom_mm"], 787.0, 0.6),
    ("D4", "bottom rail 9 in, Ellis p.93", 9 * IA, L["bottom_rail_mm"], 192.8, 0.6),
    ("D5", "jamb showing past brick, Hasluck Fig. 1148 scaled 39", 39.0, F["jamb_showing_past_brick_mm"], 55.0, 0.6),
    ("D6", "transom 4 in, Riley p.357 (T1)", 4 * IA, F["transom"]["face_height_mm"], 65.0, 0.6),
    ("D7", "fanlight 1 ft 6 in hung sash, Hasluck p.347", 18 * IA, F["glazing"]["opening_z_mm"][1] - F["glazing"]["opening_z_mm"][0], 267.0, 0.6),
    ("D10", "frame ovolo 19 mm, Hasluck p.346 / Riley Fig. 671 (the lab drew it)", 19.0, M["frame_ovolo_radius_mm"], 0.0, 0.01),
    ("D11", "transom flush with the jamb faces, Riley Fig. 667 (T1 projects: nose 14 forward of the jamb faces)", 0.0, -min(y for y, z in F["transom"]["front_profile_yz_mm"]), 14.0, 1.0),
    ("D12", "stone sill as a thin slab, 76 mm, no step (the lab's)", 0.0, abs(P1["step"]["tread"]["top_z_mm"]), 148.0, 0.6),
    ("D13", "weatherboard 72 high (the lab's)", 72.0, M["weatherboard"]["height_mm"], 80.0, 0.6),
    ("D14", "bolection width 36 (Riley), F1 from P2", 36.0, P2["mouldings"]["outside_bolection"]["width_on_face_mm"], 42.0, 0.6),
    ("D15", "letter plate centre 1000 mm (SCENE-SLOTS)", 1000.0, P1["ironmongery"]["letter_plate"]["centre_above_leaf_bottom_mm"], 1617.0, 0.6),
    ("D16", "knob near the edge, ~25 mm from the stop (the lab's)", 25.0, P1["ironmongery"]["cylinder_lock"]["distance_from_stop_face_mm"], 46.6, 0.6),
    ("D17", "flat head (the lab's)", 0.0, O["camber_rise_mm"], 18.0, 0.6),
]
for did, name, book, tgt, photo, tol in overrides:
    check("2 photo wins", f"{did}: {name}", near(tgt, photo, tol), f"book/lab {book:.1f}, photograph {photo:.1f}, target {tgt:.1f}")

# ---------------------------------------------------------------- 3. photograph P1
ph = T["photo"]["P1"]
s = ph["scale"]["mm_per_px"]
ax, ox = ph["scale"]["x_anchor_px_at_opening_centre_x_mm"]
zr, zz = ph["scale"]["z_anchor_row_at_z_mm"]
ed = ph["edges"]


def px_x(x):
    return ax + (x - ox) / s


def px_z(z):
    return zr - (z - zz) / s


def row_test(name, pred, meas, err, wallplane=False):
    tol = max(2.5, err + 1.0) + (1.5 if wallplane else 0.0)
    check("3 photo P1", name, abs(pred - meas) <= tol, f"drawing {pred:.1f} px, photograph {meas:.1f} px, diff {pred - meas:+.1f} (allowed {tol:.1f}{', wall plane' if wallplane else ''})")


lv = bnd(E1, "leaf_visible")
row_test("leaf visible top (the transom's lower edge)", px_z(lv[3]), *ed["vis_top"])
for i, (nm, poly_n, side) in enumerate([("top panel top", "bolection_top_left", 3), ("top panel bottom", "bolection_top_left", 1), ("bottom panel top", "bolection_bottom_left", 3), ("bottom panel bottom", "bolection_bottom_left", 1)]):
    row_test(f"panel moulding z edge: {nm}", px_z(bnd(E1, poly_n)[side]), *ed["moulding_z"][i])
xs_pred = [bnd(E1, "bolection_top_left")[0], bnd(E1, "bolection_top_left")[2], bnd(E1, "bolection_top_right")[0], bnd(E1, "bolection_top_right")[2]]
for i, x in enumerate(xs_pred):
    row_test(f"panel moulding x edge {i + 1} (the muntin's pair 2 and 3)", px_x(x), *ed["moulding_x"][i])
bb = bnd(E1, "lock_rail_band")
row_test("lock-rail band top", px_z(bb[3]), *ed["band_top"])
row_test("lock-rail band bottom", px_z(bb[1]), *ed["band_bottom"])
wb = bnd(E1, "weatherboard")
row_test("weatherboard top", px_z(wb[3]), *ed["weather_top"])
row_test("weatherboard bottom", px_z(wb[1]), *ed["weather_bottom"])
gb = bnd(E1, "glazing_bead")
row_test("transom's top edge (glass opening bottom)", px_z(gb[1]), *ed["transom_top_glass_bottom"])
row_test("glass opening top", px_z(gb[3]), *ed["glass_opening_top"])
gc = bnd(E1, "glass_clear")
row_test("clear glass top (inside the bead)", px_z(gc[3]), *ed["clear_glass_top"])
row_test("head's top edge at the crown", px_z(td.soffit_z(c1, c1.OW / 2)), *ed["head_crown_top"])
row_test("head's top edge at the ends", px_z(td.soffit_z(c1, 5.0)), *ed["head_end_top"])
row_test("left brick edge", px_x(0.0), ed["brick_left"][0], ed["brick_left"][1])
row_test("right brick edge", px_x(c1.OW), ed["brick_right"][0], ed["brick_right"][1])
lp = bnd(E1, "letter_plate")
row_test("letter plate left edge", px_x(lp[0]), ed["plate_x"][0], ed["plate_x"][2])
row_test("letter plate right edge", px_x(lp[2]), ed["plate_x"][1], ed["plate_x"][2])
row_test("letter plate top", px_z(lp[3]), ed["plate_rows"][0], ed["plate_rows"][2])
row_test("letter plate bottom", px_z(lp[1]), ed["plate_rows"][1], ed["plate_rows"][2])
cl = bnd(E1, "cylinder_collar")
row_test("cylinder lock centre x", px_x((cl[0] + cl[2]) / 2), ed["lock_centre_px"][0], ed["lock_centre_px"][2])
row_test("cylinder lock centre row", px_z((cl[1] + cl[3]) / 2), ed["lock_centre_px"][1], ed["lock_centre_px"][2])
row_test("cylinder lock diameter (px)", (cl[2] - cl[0]) / s, ed["lock_diameter_px"][0], ed["lock_diameter_px"][1])
kp = bnd(E1, "keep")
row_test("keep left edge", px_x(kp[0]), ed["keep_x"][0], ed["keep_x"][2])
row_test("keep right edge", px_x(kp[2]), ed["keep_x"][1], ed["keep_x"][2])
row_test("keep top", px_z(kp[3]), ed["keep_rows"][0], ed["keep_rows"][2])
row_test("keep bottom", px_z(kp[1]), ed["keep_rows"][1], ed["keep_rows"][2])
n0 = bnd(E1, "house_number_0")
n1 = bnd(E1, "house_number_1")
row_test("numeral '9' bottom", px_z(n0[1]), ed["numeral_rows"][1][1], 1.5)
row_test("numeral '6' top", px_z(n1[3]), ed["numeral_rows"][0][0], 1.5)
ab = [d for n, d in E1.items() if n.startswith("arch_brick")]
ax0 = min(shp(d).bounds[0] for d in ab)
ax1 = max(shp(d).bounds[2] for d in ab)
atop = max(shp(d).bounds[3] for d in ab)
row_test("arch ring left end", px_x(ax0), ed["arch_x"][0], ed["arch_x"][2], True)
row_test("arch ring right end", px_x(ax1), ed["arch_x"][1], ed["arch_x"][2], True)
row_test("arch ring top (wall plane: the scale is 3% finer there)", px_z(atop), ed["arch_top_row"][0], ed["arch_top_row"][1], True)
nb = len([n for n in E1 if n.startswith("arch_brick")])
check("3 photo P1", "arch ring: 11 or 12 bricks counted on P1", nb in (11, 12), f"{nb} in the target")
# the quoins: course pitch against the photograph (15.2-15.4 px at the wall face)
q = P1["brick"]["quoins"]
pitch_px = q["course_gauge_mm"] / (s * 0.968)
check("3 photo P1", "quoin course pitch at the wall plane (photograph 15.2-15.4 px)", 15.0 <= pitch_px <= 15.7, f"{pitch_px:.2f} px at 0.968 x {s} mm a pixel (camera 5.8 m)")
# perspective: the step's tread is nearer the camera than the door
tw = P1["step"]["tread"]["width_mm"]
s_tread = tw / (ed["tread_x"][1] - ed["tread_x"][0])
dd = (P1["leaf"]["outside_face_y_mm"] + P1["step"]["tread"]["projection_beyond_wall_face_mm"]) / (1 - s_tread / s)
dw = P1["leaf"]["outside_face_y_mm"] / (1 - 4.95 / s)
check("3 photo P1", "tread width agrees with a camera 3 to 8 m away (from the tread's 204 px)", 3000 <= dd <= 8000, f"tread 960 mm over 204 px = {s_tread:.2f} mm/px, camera {dd / 1000:.1f} m")
check("3 photo P1", "brick course scale and tread scale give camera distances within a factor 1.8", max(dd, dw) / min(dd, dw) <= 1.8, f"from the courses {dw / 1000:.1f} m, from the tread {dd / 1000:.1f} m")
# fractions
vh = F["transom"]["z_stop_underside"] - L["z0_mm"]
vw = c1.OW - 2 * c1.SHOW
vis_top, leaf_bot = ed["vis_top"][0], zr
vis_h_px = leaf_bot - vis_top
for name, t, p, e in [
    ("visible height / visible width", vh / vw, vis_h_px / 149.9, 0.045),
    ("muntin's visible gap / visible width (the review's 14%)", (bnd(E1, "bolection_top_right")[0] - bnd(E1, "bolection_top_left")[2]) / vw, (ed["moulding_x"][2][0] - ed["moulding_x"][1][0]) / 149.9, 0.02),
    ("top rail showing / visible height", (F["transom"]["z_stop_underside"] - bnd(E1, "bolection_top_left")[3]) / vh, (ed["moulding_z"][0][0] - vis_top) / vis_h_px, 0.01),
    ("lock rail showing / visible height", (bnd(E1, "bolection_top_left")[1] - bnd(E1, "bolection_bottom_left")[3]) / vh, (ed["moulding_z"][2][0] - ed["moulding_z"][1][0]) / vis_h_px, 0.01),
    ("bottom rail showing / visible height", (bnd(E1, "bolection_bottom_left")[1] - L["z0_mm"]) / vh, (leaf_bot - ed["moulding_z"][3][0]) / vis_h_px, 0.01),
    ("band height / visible height", (bb[3] - bb[1]) / vh, (ed["band_bottom"][0] - ed["band_top"][0]) / vis_h_px, 0.008),
    ("weatherboard height / visible height", (wb[3] - wb[1]) / vh, (ed["weather_bottom"][0] - ed["weather_top"][0]) / vis_h_px, 0.01),
    ("transom bar height / visible width", F["transom"]["face_height_mm"] / vw, (ed["vis_top"][0] - ed["transom_top_glass_bottom"][0]) / 149.9, 0.015),
]:
    check("3 photo P1 fraction", name, abs(t - p) <= e, f"target {t:.3f}, photograph {p:.3f} +-{e}")

# ---------------------------------------------------------------- 4. photograph P2 against the flat door
p2 = T["photo"]["P2"]["edges"]
vw2 = p2["vis_right"] - p2["vis_left"]
vh2 = p2["leaf_bottom"] - p2["leaf_top"]
vw_t = c2.OW - 2 * c2.SHOW
vh_t = P2["frame"]["transom"]["z_stop_underside"] - P2["leaf"]["z0_mm"]


def p2row(name, t, p, e, kind="check"):
    check("4 photo P2", name, abs(t - p) <= e, f"flat door {t:.3f}, photograph {p:.3f} +-{e}", kind)


p2row("transom bar height / visible width", P2["frame"]["transom"]["face_height_mm"] / vw_t, (p2["transom_rows"][1] - p2["transom_rows"][0]) / vw2, 0.012)
zn = P2["frame"]["transom"]["zones_z_mm"]
fh = P2["frame"]["transom"]["face_height_mm"]
p2row("transom slope share of the bar", (zn["slope"][1] - zn["slope"][0]) / fh, (p2["transom_slope_rows"][1] - p2["transom_slope_rows"][0]) / (p2["transom_rows"][1] - p2["transom_rows"][0]), 0.08)
p2row("transom face share of the bar", (zn["face"][1] - zn["face"][0]) / fh, (p2["transom_face_rows"][1] - p2["transom_face_rows"][0]) / (p2["transom_rows"][1] - p2["transom_rows"][0]), 0.08)
p2row("transom nose share of the bar", (zn["lip_and_cove"][1] - zn["lip_and_cove"][0]) / fh, (p2["transom_nose_rows"][1] - p2["transom_nose_rows"][0]) / (p2["transom_rows"][1] - p2["transom_rows"][0]), 0.08)
mo = bnd(E2, "bolection_top_left")
p2row("stile showing / visible width", (mo[0] - c2.SHOW) / vw_t, p2["stile_px"] / vw2, 0.015)
p2row("bolection width / visible width", P2["mouldings"]["outside_bolection"]["width_on_face_mm"] / vw_t, p2["mould_width_px"] / vw2, 0.01)
p2row("bottom rail showing / visible height", (bnd(E2, "bolection_bottom_left")[1] - P2["leaf"]["z0_mm"]) / vh_t, p2["bottom_rail_px"] / vh2, 0.012)
cl2 = bnd(E2, "cylinder_collar")
vis_r2 = c2.OW - c2.SHOW
p2row("cylinder lock: distance of its centre from the visible edge / visible width", (vis_r2 - (cl2[0] + cl2[2]) / 2) / vw_t, (p2["vis_right"] - p2["cylinder_centre"][0]) / vw2, 0.01)
p2row("cylinder lock diameter / visible width", (cl2[2] - cl2[0]) / vw_t, p2["cylinder_diameter_px"] / vw2, 0.006)
kn2 = bnd(E2, "knob")
p2row("knob diameter / visible width", (kn2[2] - kn2[0]) / vw_t, p2["knob_diameter_px"] / vw2, 0.006)
p2row("knob centred across the leaf", ((kn2[0] + kn2[2]) / 2 - c2.OW / 2) / vw_t, (p2["knob_centre"][0] - (p2["vis_left"] + p2["vis_right"]) / 2) / vw2, 0.012)
p2row("visible height / visible width (the six-panel door of P2 is squatter than 0.838 x 1.981)", vh_t / vw_t, vh2 / vw2, 0.04, "reported")

# ---------------------------------------------------------------- 5. consistency (numbers and shapes)
o = L and P1["panels"]["openings_leaf_uv_mm"]
W, H = L["width_mm"], L["height_mm"]
for tag, PP, cc in (("T1", P1, c1), ("F1", P2, c2)):
    LL, OO = PP["leaf"], PP["panels"]["openings_leaf_uv_mm"]
    pw = OO["top_left"]["u1"] - OO["top_left"]["u0"]
    check("5 consistency", f"{tag}: stiles + muntin + two panel openings = leaf width", near(2 * LL["stile_mm"] + LL["muntin_mm"] + 2 * pw, LL["width_mm"], 0.3), f"{2 * LL['stile_mm'] + LL['muntin_mm'] + 2 * pw:.1f} vs {LL['width_mm']}")
    sumv = LL["bottom_rail_mm"] + (OO["bottom_left"]["v1"] - OO["bottom_left"]["v0"]) + LL["lock_rail_mm"] + (OO["top_left"]["v1"] - OO["top_left"]["v0"]) + LL["top_rail_mm"]
    check("5 consistency", f"{tag}: rails + panel openings = leaf height", near(sumv, LL["height_mm"], 0.3), f"{sumv:.1f} vs {LL['height_mm']}")
    check("5 consistency", f"{tag}: lock rail centred on its stated height", near((OO["bottom_left"]["v1"] + OO["top_left"]["v0"]) / 2, LL["lock_rail_centre_above_leaf_bottom_mm"], 0.3), "")
    check("5 consistency", f"{tag}: muntin centred on the leaf", near((OO["top_left"]["u1"] + OO["top_right"]["u0"]) / 2, LL["width_mm"] / 2, 0.3), "")
    check("5 consistency", f"{tag}: bolection leaves a field of more than 100 mm", pw - 2 * (PP["mouldings"]["outside_bolection"]["width_on_face_mm"] - 4.8) > 100, f"{pw - 2 * (PP['mouldings']['outside_bolection']['width_on_face_mm'] - 4.8):.1f}")
    reb_l = PP["frame"]["jamb_x_mm"]["left"][1] - PP["frame"]["rebate_width_mm"]
    reb_r = PP["frame"]["jamb_x_mm"]["right"][0] + PP["frame"]["rebate_width_mm"]
    check("5 consistency", f"{tag}: leaf + two clearances = rebate to rebate", near(LL["width_mm"] + 2 * LL["edge_clearance_mm"], reb_r - reb_l, 0.15), f"{LL['width_mm'] + 3.2:.1f} vs {reb_r - reb_l:.1f}")
    check("5 consistency", f"{tag}: leaf starts one clearance from the left rebate", near(LL["x0_mm"], reb_l + LL["edge_clearance_mm"], 0.15), f"x0 {LL['x0_mm']}")
    check("5 consistency", f"{tag}: leaf thickness fits the rebate depth", LL["thickness_mm"] < PP["frame"]["rebate_depth_mm"], "")
    check("5 consistency", f"{tag}: stop + rebate = frame depth", near(PP["frame"]["stop_depth_mm"] + PP["frame"]["rebate_depth_mm"], PP["frame"]["jamb_depth_mm"], 0.15), "")
    check("5 consistency", f"{tag}: leaf top + clearance = transom rebate underside", near(LL["z0_mm"] + LL["height_mm"] + LL["edge_clearance_mm"], PP["frame"]["transom"]["rebate_underside_z"], 0.15), "")
    check("5 consistency", f"{tag}: transom stop covers the leaf top by the rebate width", near(PP["frame"]["transom"]["rebate_underside_z"] - PP["frame"]["transom"]["z_stop_underside"], PP["frame"]["rebate_width_mm"], 0.15), "")
    check("5 consistency", f"{tag}: transom top = glass opening bottom, opening top = head underside", near(PP["frame"]["transom"]["z_top"], PP["frame"]["glazing"]["opening_z_mm"][0], 0.15) and near(PP["frame"]["glazing"]["opening_z_mm"][1], PP["frame"]["head_section_mm"]["z0"], 0.15), "")
    check("5 consistency", f"{tag}: opening = clear between stops + two jambs showing", near(PP["opening"]["width_mm"], PP["opening"]["clear_between_stops_mm"] + 2 * PP["frame"]["jamb_showing_past_brick_mm"], 0.15), "")
    check("5 consistency", f"{tag}: jamb showing + hidden part = jamb face", near(PP["frame"]["jamb_showing_past_brick_mm"] - PP["frame"]["jamb_x_mm"]["left"][0], PP["frame"]["jamb_face_mm"], 0.15), "")
    g = PP["frame"]["glazing"]
    check("5 consistency", f"{tag}: clear glass = opening less a bead each side", near(g["clear_glass_x_mm"][0] - g["opening_x_mm"][0], g["bead_face_mm"], 0.15) and near(g["opening_z_mm"][1] - g["clear_glass_z_mm"][1], g["bead_face_mm"], 0.15), "")
    check("5 consistency", f"{tag}: head's top at the crown = opening crown", near(PP["frame"]["head_section_mm"]["z0"] + PP["frame"]["head_section_mm"]["showing_below_brick_at_crown"], PP["opening"]["crown_height_mm"], 0.15), "")
    bd, wd = PP["mouldings"]["lock_rail_band"], PP["mouldings"]["weatherboard"]
    if bd.get("present"):
        o_ = PP["panels"]["openings_leaf_uv_mm"]
        check("5 consistency", f"{tag}: band lies on the lock rail between the mouldings", o_["bottom_left"]["v1"] - 4.8 <= bd["z_above_leaf_bottom_mm"][0] and bd["z_above_leaf_bottom_mm"][1] <= o_["top_left"]["v0"] + 4.8, f"{bd['z_above_leaf_bottom_mm']}")
        check("5 consistency", f"{tag}: band stops {bd['end_gap_to_stop_mm']} short of each stop face", near(bd["x_mm"][0] - PP["frame"]["jamb_showing_past_brick_mm"], bd["end_gap_to_stop_mm"], 0.15) and near(PP["opening"]["width_mm"] - PP["frame"]["jamb_showing_past_brick_mm"] - bd["x_mm"][1], bd["end_gap_to_stop_mm"], 0.15), f"{bd['x_mm']}")
        check("5 consistency", f"{tag}: weatherboard under the bottom moulding, stops short of each stop", wd["z_above_leaf_bottom_mm"][1] <= o_["bottom_left"]["v0"] - 4.8 and near(wd["x_mm"][0] - PP["frame"]["jamb_showing_past_brick_mm"], wd["end_gap_to_stop_mm"], 0.15), f"{wd['z_above_leaf_bottom_mm']}")
        check("5 consistency", f"{tag}: band profile spans its height; weatherboard profile spans its height", near(bd["profile_zp_mm"][-1][0], bd["height_mm"], 0.1) and near(wd["profile_zp_mm"][-1][0], wd["height_mm"], 0.1), "")
    ir = PP["ironmongery"]
    plp = ir["letter_plate"]
    mid = PP["leaf"]["muntin_mm"]
    check("5 consistency", f"{tag}: letter plate fits on the muntin with 20 mm either side", plp["outer_w_mm"] <= mid - 40, f"{plp['outer_w_mm']} in {mid}")
    check("5 consistency", f"{tag}: letter plate lies on the upper panels' height, clear of the band and the top rail", PP["leaf"]["lock_rail_centre_above_leaf_bottom_mm"] + 114.3 + 100 < plp["centre_above_leaf_bottom_mm"] - plp["outer_h_mm"] / 2 and plp["centre_above_leaf_bottom_mm"] + plp["outer_h_mm"] / 2 < PP["leaf"]["height_mm"] - PP["leaf"]["top_rail_mm"], "")
    cyl = ir["cylinder_lock"]
    vis_edge_u = PP["opening"]["width_mm"] - PP["frame"]["jamb_showing_past_brick_mm"] - PP["leaf"]["x0_mm"]
    check("5 consistency", f"{tag}: cylinder lock lies wholly on the lock stile, 24 mm or more from the stop face", vis_edge_u - cyl["centre_u_mm"] - cyl["outer_diameter_mm"] / 2 >= 24 and cyl["centre_u_mm"] - cyl["outer_diameter_mm"] / 2 > PP["leaf"]["width_mm"] - PP["leaf"]["stile_mm"] + 4.8 - 0.5, f"edge distance {vis_edge_u - cyl['centre_u_mm'] - cyl['outer_diameter_mm'] / 2:.1f}")
    check("5 consistency", f"{tag}: keep lies on the visible face of the right jamb's stop", PP["opening"]["width_mm"] - PP["frame"]["jamb_showing_past_brick_mm"] <= ir["keep"]["centre_x_mm"] - 11 and ir["keep"]["centre_x_mm"] + 11 <= PP["opening"]["width_mm"], f"x {ir['keep']['centre_x_mm']}")
    check("5 consistency", f"{tag}: the nose projects less than the frame's rebate and the stop is deeper than the nose", -min(y for y, z in PP["frame"]["transom"]["front_profile_yz_mm"]) < PP["frame"]["stop_depth_mm"], "")
    check("5 consistency", f"{tag}: transom's front member overlaps each jamb face by its stated amount and stays within the jamb", near(PP["frame"]["jamb_x_mm"]["left"][1] - PP["frame"]["transom"]["x_mm"][0], PP["frame"]["transom"]["overlap_on_jamb_faces_mm"], 0.2) and PP["frame"]["transom"]["overlap_on_jamb_faces_mm"] < PP["frame"]["jamb_showing_past_brick_mm"], "")
    st = PP["step"]
    if st["tread"].get("present", True):
        td_ = st["tread"]
        check("5 consistency", f"{tag}: tread is wider than the opening on both sides and centred on it", td_["x_mm"][0] < 0 and td_["x_mm"][1] > PP["opening"]["width_mm"] and near((td_["x_mm"][0] + td_["x_mm"][1]) / 2, PP["opening"]["width_mm"] / 2, 0.5), f"{td_['x_mm']}")
        check("5 consistency", f"{tag}: tread top = riser bottom; riser top = threshold bottom", near(td_["top_z_mm"], st["riser"]["z_mm"][0], 0.1) and near(st["riser"]["z_mm"][1], st["threshold"]["top_z"] - st["threshold"]["thickness_mm"], 0.1), "")
        check("5 consistency", f"{tag}: ground = tread top less its thickness", near(td_["ground_z_mm"], td_["top_z_mm"] - td_["thickness_mm"], 0.5), f"{td_['ground_z_mm']}")
    a = PP["brick"]["arch"]
    if a.get("present"):
        check("5 consistency", f"{tag}: arch ring ends lie the stated bearing past each reveal", near(-a["ends_x_mm"][0], a["bearing_beyond_reveal_each_side_mm"], 0.1) and near(a["ends_x_mm"][1] - PP["opening"]["width_mm"], a["bearing_beyond_reveal_each_side_mm"], 0.1), "")
        check("5 consistency", f"{tag}: the ring's depth at the crown = its top less the crown", near(a["top_z_mm"] - PP["opening"]["crown_height_mm"], 215.0, 0.5), f"{a['top_z_mm'] - PP['opening']['crown_height_mm']}")
        qq = PP["brick"]["quoins"]
        check("5 consistency", f"{tag}: the quoins end at the arch's springing (+-3 mm)", near(qq["z_start_mm"] + qq["courses"] * qq["course_gauge_mm"], PP["opening"]["springing_height_mm"], 3.0), f"{qq['z_start_mm'] + qq['courses'] * qq['course_gauge_mm']} vs {PP['opening']['springing_height_mm']}")
        check("5 consistency", f"{tag}: the ring's end bears on the top quoin: width 112 >= 100", qq["header_width_mm"] >= 100 and a["bearing_on_quoin_top_course_mm"] >= 100, "")

# shapes: shapely on the drawings
docs = {"T1": td.all_drawings(T, None), "F1": td.all_drawings(T, "flat_door_over_shop")}
for tag, doc in docs.items():
    for key in [k for k in doc if k.startswith("section_h")]:
        P_ = doc[key]["polygons"]
        shapes = {d["name"]: shp(d) for d in P_ if d["layer"] != "brick"}
        joinery = {n: g for n, g in shapes.items()}
        names = list(joinery)
        bad = []
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                ia = joinery[a].intersection(joinery[b]).area
                if ia > 0.05:
                    bad.append((a, b, round(ia, 2)))
        check("5 consistency", f"{tag} {key}: no two parts overlap (area > 0.05 mm2)", not bad, "none" if not bad else str(bad[:4]))
        floats = [n for n in names if not any(joinery[n].buffer(0.1).intersects(joinery[m]) for m in names if m != n)]
        check("5 consistency", f"{tag} {key}: nothing floats (each part touches another within 0.1 mm)", not floats, "none" if not floats else str(floats[:5]))
    for key in ("section_v", "section_v_muntin", "plan"):
        P_ = doc[key]["polygons"]
        shapes = {d["name"]: shp(d) for d in P_}
        names = list(shapes)
        allowed = lambda a, b: key == "plan" and ({a, b} & {"threshold", "wall_left", "wall_right"} and (a.startswith(("wall", "tread", "jamb")) or b.startswith(("wall", "tread", "jamb")) or {a, b} == {"threshold", "tread"}))
        bad = [(a, b, round(shapes[a].intersection(shapes[b]).area, 2)) for i, a in enumerate(names) for b in names[i + 1:] if shapes[a].intersection(shapes[b]).area > 0.05 and not allowed(a, b)]
        # profile mouldings sit in the leaf's grooves/faces: allow nothing but the glass slot, which is a gap
        check("5 consistency", f"{tag} {key}: no two parts overlap (area > 0.05 mm2)", not bad, "none" if not bad else str(bad[:4]))
        floats = [n for n in names if not any(shapes[n].buffer(0.1).intersects(shapes[m]) for m in names if m != n)]
        check("5 consistency", f"{tag} {key}: nothing floats", not floats, "none" if not floats else str(floats[:5]))
    E = by_name(doc["elevation"]["polygons"])
    bad = []
    skip = ("brick_wall",)
    names = [n for n in E if n not in skip and E[n]["layer"] in ("frame", "leaf", "panel", "moulding", "iron", "glass")]
# the band and the weatherboard keep clear of the jambs in the band section (T1)
SB = by_name(docs["T1"]["section_h_band"]["polygons"])
for nm in ("lock_rail_band",):
    gl = shp(SB[nm]).distance(shp(SB["jamb_left"]))
    gr = shp(SB[nm]).distance(shp(SB["jamb_right"]))
    check("5 consistency", "T1 band section: the band's ends are 2 +-0.5 mm from both jamb stops (from the drawing)", near(gl, 2.0, 0.5) and near(gr, 2.0, 0.5), f"{gl:.2f} and {gr:.2f}")
SH = by_name(docs["T1"]["section_h"]["polygons"])
reb_l_x = F["jamb_x_mm"]["left"][1] - F["rebate_width_mm"]
reb_r_x = F["jamb_x_mm"]["right"][0] + F["rebate_width_mm"]
gl_ = shp(SH["stile_left"]).bounds[0] - reb_l_x
gr_ = reb_r_x - shp(SH["stile_right"]).bounds[2]
check("5 consistency", "T1 lower-panel section: the leaf is 1.6 mm clear of both rebate walls (from the drawing)", near(gl_, 1.6, 0.3) and near(gr_, 1.6, 0.3), f"{gl_:.2f} and {gr_:.2f}")
check("5 consistency", "T1 lower-panel section: the leaf's face sits on the stops (touching, no overlap)", shp(SH["stile_left"]).distance(shp(SH["jamb_left"])) < 0.05 and shp(SH["stile_left"]).intersection(shp(SH["jamb_left"])).area < 0.05, "")
SV = by_name(docs["T1"]["section_v"]["polygons"])
check("5 consistency", "T1 vertical section: head and transom do not overlap the arch ring", shp(SV["head"]).intersection(shp(SV["arch_ring"])).area < 0.05 and shp(SV["transom"]).intersection(shp(SV["arch_ring"])).area < 0.05, "")
check("5 consistency", "T1 vertical section: the glass stands in the transom's and the head's slots (no overlap, 0.5 mm play)", shp(SV["glass"]).intersection(shp(SV["transom"])).area < 0.05 and shp(SV["glass"]).intersection(shp(SV["head"])).area < 0.05, "")
gz = min(p[1] for p in SV["transom"]["pts"] if p[0] > c1.STOP_Y + 1) - shp(SV["top_rail"]).bounds[3]
check("5 consistency", "T1 vertical section: the leaf's top is 1.6 mm below the transom's rebate (from the drawing)", near(gz, 1.6, 0.3), f"{gz:.2f}")

# ---------------------------------------------------------------- 6. the builder's checks, evaluated on the drawings
SM = by_name(docs["T1"]["section_v_muntin"]["polygons"])
PL = by_name(docs["T1"]["plan"]["polygons"])
S3 = by_name(docs["T1"]["section_h_transom"]["polygons"])
PLATE = docs["T1"]["section_h_plate"]["polygons"]


def ck(cid, name, got, want, tol):
    check("6 checks", f"{cid}: {name}", abs(got - want) <= tol, f"drawing {got:.2f}, check expects {want} +-{tol}")


b = bnd(E1, "lock_rail_band")
ck("B6", "gap between the pair of mouldings", bnd(E1, "bolection_top_right")[0] - bnd(E1, "bolection_top_left")[2], L["muntin_mm"] - 9.6, 2.5)
ck("B11", "jamb section width", shp(SH["jamb_left"]).bounds[2] - shp(SH["jamb_left"]).bounds[0], 101.6, 1.0)
ck("B11", "jamb section depth", shp(SH["jamb_left"]).bounds[3] - shp(SH["jamb_left"]).bounds[1], 127.0, 1.0)
ck("B15", "clear glass width", bnd(E1, "glass_clear")[2] - bnd(E1, "glass_clear")[0], 752.0, 2.0)
ck("B15", "clear glass height", bnd(E1, "glass_clear")[3] - bnd(E1, "glass_clear")[1], 247.0, 2.0)
ck("E1", "band height", b[3] - b[1], 72.5, 3.0)
ck("E1", "band underside above the leaf bottom", b[1] - L["z0_mm"], 785.0, 5.0)
bp = M["lock_rail_band"]["profile_zp_mm"]
ck("E2", "band max projection", max(p for z, p in bp), 22.0, 4.0)
ck("E5", "band end gap (x to the left stop face)", M["lock_rail_band"]["x_mm"][0] - c1.SHOW, 2.0, 1.5)
w_ = bnd(E1, "weatherboard")
ck("W1", "weatherboard height", w_[3] - w_[1], 80.0, 4.0)
ck("W1", "weatherboard bottom at the leaf's bottom", w_[1] - L["z0_mm"], 0.0, 2.0)
wp = M["weatherboard"]["profile_zp_mm"]
ck("W2", "weatherboard max projection", max(p for z, p in wp), 26.0, 4.0)
lpb = bnd(E1, "letter_plate")
ck("F2", "letter plate width", lpb[2] - lpb[0], 76.0, 3.0)
ck("F2", "letter plate height", lpb[3] - lpb[1], 242.0, 3.0)
ck("F3", "letter plate centre above the leaf's bottom", (lpb[1] + lpb[3]) / 2 - L["z0_mm"], 1617.0, 10.0)
ck("F3", "letter plate centred across the leaf", (lpb[0] + lpb[2]) / 2, c1.OW / 2, 4.0)
cb = bnd(E1, "cylinder_collar")
ck("F5", "cylinder collar diameter", cb[2] - cb[0], 43.5, 3.0)
ck("F5", "cylinder centre above the leaf's bottom", (cb[1] + cb[3]) / 2 - L["z0_mm"], 1235.0, 8.0)
ck("F5", "cylinder centre from the stop face", (c1.OW - c1.SHOW) - (cb[0] + cb[2]) / 2, 46.6, 4.0)
kb = bnd(E1, "keep")
ck("F7", "keep height", kb[3] - kb[1], 72.6, 3.0)
ck("F7", "keep centre x", (kb[0] + kb[2]) / 2, 859.4, 5.0)
sr = shp(SM["threshold"]).bounds
ck("G1", "threshold thickness", sr[3] - sr[1], 76.0, 4.0)
ck("G1", "threshold front at the wall face", sr[0], 0.0, 3.0)
pb = shp(PL["threshold"]).bounds
ck("G2", "threshold bearing past the opening (left)", -pb[0], 112.0, 20.0)
ck("G2", "threshold bearing past the opening (right)", pb[2] - c1.OW, 112.0, 20.0)
rb = shp(SV["riser"]).bounds
ck("G3", "riser height", rb[3] - rb[1], 72.0, 6.0)
ck("G3", "riser face behind the threshold's nose", rb[0], 18.0, 6.0)
tb = shp(SV["tread"]).bounds
ck("G4", "tread projection beyond the wall face", -tb[0], 312.0, 25.0)
ck("G4", "tread top below the threshold top", -tb[3], 148.0, 25.0)
tp = shp(PL["tread"]).bounds
ck("G4", "tread width", tp[2] - tp[0], 960.0, 25.0)
ck("G5", "tread beyond the left reveal", -tp[0], 39.0, 25.0)
ck("G7", "arch ring left end beyond the reveal", -min(shp(d).bounds[0] for d in [E1[n] for n in E1 if n.startswith("arch_brick")]), 22.0, 6.0)
ck("G7", "arch ring depth at the crown", max(shp(E1[n]).bounds[3] for n in E1 if n.startswith("arch_brick")) - td.soffit_z(c1, c1.OW / 2), 215.0, 6.0)
ck("G7", "soffit camber", td.soffit_z(c1, c1.OW / 2) - td.soffit_z(c1, 0.0), 18.0, 6.0)
hd_ = by_name(td.elevation(P1))["head"]["pts"]
dev = max(abs(p[1] - td.soffit_z(c1, p[0])) for p in hd_ if p[1] > c1.GZ1 + 1)
check("6 checks", "G8: the head's top edge follows the brick soffit (max deviation over its vertices)", dev <= 0.5, f"{dev:.2f} mm")
# the transom: projection, slope, lip
fp = F["transom"]["front_profile_yz_mm"]
ck("D1", "transom nose projection beyond the jamb faces", -min(y for y, z in fp), 14.0, 3.0)
face_y = [y for y, z in fp if 14.0 <= z <= 40.0]
ck("D1", "transom face proud of the jamb faces", -max(face_y) if face_y else 0, 8.0, 3.0)
(y0, z0_), (y1, z1_) = fp[-2], fp[-1]
ck("D2", "weathered slope angle", math.degrees(math.atan2(z1_ - z0_, y1 - y0)), 55.0, 8.0)
lip_y = min(fp, key=lambda p: p[0])
ck("D4", "frontmost point of the transom within the lip zone (z)", lip_y[1], 2.6, 3.0)
ck("D5", "transom overlap on a jamb face", c1.SHOW - c1.TR_X0, 10.0, 4.0)
ck("D3", "transom face zone from z 14 to 40", F["transom"]["zones_z_mm"]["face"][1] - F["transom"]["zones_z_mm"]["face"][0], 26.0, 3.0)
levels = sorted({round(y) for y, z in fp})
check("6 checks", "D7: the transom's front has at least 3 distinct y levels", len(levels) >= 3, f"{len(levels)} levels")
# crests of the band and weatherboard
def crests(prof):
    pts = [(z, p) for z, p in prof[1:-1]]
    cr, co = [], []
    for i in range(1, len(pts) - 1):
        if pts[i][1] >= pts[i - 1][1] and pts[i][1] >= pts[i + 1][1] and pts[i][1] > pts[i - 1][1] - 1e-9:
            cr.append(pts[i])
        if pts[i][1] <= pts[i - 1][1] and pts[i][1] <= pts[i + 1][1]:
            co.append(pts[i])
    return cr, co


cr, co = crests(bp)
cz = sorted({round(z) for z, p in cr if p >= 17.5})
check("6 checks", "E3: the band's outline has crests near z 6, 37 and 62 and coves near z 25 and 49", any(abs(z - 37) <= 4 for z in cz) and any(abs(z - 62) <= 4 for z in cz) and any(abs(z - 25) <= 4 for z, p in co) and any(abs(z - 49) <= 4 for z, p in co), f"crests {cz}, coves {[round(z) for z, p in co]}")
cr, co = crests(wp)
check("6 checks", "W3: the weatherboard's outline has a hollow near z 57 and two crests", any(abs(z - 57) <= 4 for z, p in co) and len([1 for z, p in cr if p > 22]) >= 2, f"coves {[round(z) for z, p in co]}")
# frame edges square: the jamb outline has no vertex that is not on its rectangle outline within 1.5 mm
jam = SH["jamb_left"]["pts"]
xs_ = sorted({round(p[0], 1) for p in jam})
ys_ = sorted({round(p[1], 1) for p in jam})
check("6 checks", "C1: the jamb section is a rectilinear polygon (every edge axis-parallel): no ovolo, no round", all(abs(a[0] - b_[0]) < 1e-6 or abs(a[1] - b_[1]) < 1e-6 for a, b_ in zip(jam, jam[1:] + jam[:1])), f"{len(jam)} vertices")
tpl = S3["transom"]["pts"]
check("6 checks", "C1: the transom's plan section is rectilinear (square ends, no returns or rounds)", all(abs(a[0] - b_[0]) < 1e-6 or abs(a[1] - b_[1]) < 1e-6 for a, b_ in zip(tpl, tpl[1:] + tpl[:1])), f"{len(tpl)} vertices")
# the lab's failing: lintel / sill rest on something
check("6 checks", "G9: the arch's ends overlap the top quoin course in x (22 mm past the reveal onto a 112 mm quoin)", c1.brick["arch"]["bearing_beyond_reveal_each_side_mm"] > 0 and c1.brick["quoins"]["header_width_mm"] > c1.brick["arch"]["bearing_beyond_reveal_each_side_mm"], "")

# ---------------------------------------------------------------- the result
npass = sum(r["pass"] for r in rows)
reported = [r for r in rows if not r["pass"] and r["kind"] == "reported"]
failed = [r for r in rows if not r["pass"] and r["kind"] != "reported"]
summary = f"{npass} of {len(rows)} checks pass; {len(failed)} fail; {len(reported)} reported disagreement(s) kept visible"
T["self_check"] = {"run": "self_check.py, 8 Oct 2026 (cloud week 42)", "summary": summary, "photo_scale_mm_per_px_P1": s,
                   "failures": failed, "reported_disagreements": reported, "rows": rows}
TP.write_text(json.dumps(T, indent=1, ensure_ascii=False), encoding="utf-8")
print(summary)
print("| Group | Check | Result | Detail |\n|---|---|---|---|")
for r in rows:
    print(f"| {r['group']} | {r['check']} | {'pass' if r['pass'] else ('REPORTED' if r['kind'] == 'reported' else 'FAIL')} | {r['detail']} |")
sys.exit(0 if not failed else 1)
