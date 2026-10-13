"""The door kinds of the front-doors-all target, built as numbers from the 3.1 door (as built: target.json plus departures.py)
and the photographs' measurements. Everything is in millimetres in the leaf's own frame: u across from the leaf's left edge seen
from outside, v up from the leaf's bottom. The frame set (T or F) is the 3.1 frame's, copied in make_target.py.
Kinds: T1 T2 T3 (the cottage frame T) and F1 F2 F3 F4 F5 F6 F7 (the flat frame F)."""
import math
import sys

from td_data import MEAS

sys.dont_write_bytecode = True


def _r(x, n=1):
    return round(float(x), n)


# The leaf laps its rebate: 20.4 mm of each side and of the head hide behind the stops and the transom (3.1: leaf 812.8 in a clear 772;
# 838 in a clear 797.2). Photographs show the visible face, so a photograph's fraction of the visible face maps to the structural leaf as
# u = LAP + fraction x visible width, v = fraction x visible height (the foot hides nothing).
LAP = 20.4
VIS = {"T": (772.0, 1927.6), "F": (797.2, 1960.6)}


def to_struct(frame, box_u, box_v):
    vw, vh = VIS[frame]
    return (LAP + box_u[0] * vw, LAP + box_u[1] * vw, box_v[0] * vh, box_v[1] * vh)


def px_to_mm(meas, photo_scale):
    return photo_scale


# ---- photograph-derived fractions, recomputed from MEAS (the self-check recomputes them again)
def d3_fractions():
    b = MEAS["D3_leaf"]["box"]
    h = b[3] - b[1]
    w = b[2] - b[0]
    rows = MEAS["D3_rows"]["rows_px"]
    top_rail = (rows["light1"][0] - b[1]) / h
    bar = [(rows["light%d" % (i + 1)][0] - rows["light%d" % i][1]) / h for i in range(1, 4)]
    light = [(rows["light%d" % i][1] - rows["light%d" % i][0]) / h for i in range(1, 5)]
    bottom_rail = (b[3] - rows["light4"][1]) / h
    st = MEAS["D3_stiles"]
    return {"top_rail": top_rail, "bar": sum(bar) / 3.0, "light": sum(light) / 4.0, "bottom_rail": bottom_rail,
            "stile_left": (st["left_px"][1] - st["left_px"][0]) / w, "stile_right": (st["right_px"][1] - st["right_px"][0]) / w,
            "scale_mm_px": MEAS["D3_leaf"]["leaf_mm"][1] / h}


def d4_t3_fractions():
    b = MEAS["D4_T3_leaf"]["box"]
    w, h = b[2] - b[0], b[3] - b[1]

    def uv(box):
        return {"u": [(box[0] - b[0]) / w, (box[2] - b[0]) / w], "v": [1.0 - (box[3] - b[1]) / h, 1.0 - (box[1] - b[1]) / h]}

    return {"upper": uv(MEAS["D4_T3_upper"]["box"]), "light": uv(MEAS["D4_T3_light"]["box"]), "plate": uv(MEAS["D4_T3_plate"]["box"]),
            "lower": uv(MEAS["D4_T3_lower"]["box"]), "handle": uv(MEAS["D4_T3_handle"]["box"]), "scale_mm_px": MEAS["D4_T3_leaf"]["leaf_mm"][1] / h}


def d2_f5_fractions():
    b = MEAS["D2_F5_leaf"]["box"]
    w, h = b[2] - b[0], b[3] - b[1]

    def uv(box):
        return {"u": [(box[0] - b[0]) / w, (box[2] - b[0]) / w], "v": [1.0 - (box[3] - b[1]) / h, 1.0 - (box[1] - b[1]) / h]}

    return {"slit": uv(MEAS["D2_F5_slit"]["box"]), "plate": uv(MEAS["D2_F5_plate"]["box"]), "handle": uv(MEAS["D2_F5_handle"]["box"]),
            "scale_mm_px_v": MEAS["D2_F5_leaf"]["leaf_mm"][1] / h, "scale_mm_px_u": MEAS["D2_F5_leaf"]["leaf_mm"][0] / w}


def d5_fractions():
    b = MEAS["D5_leaf"]["box"]
    w, h = b[2] - b[0], b[3] - b[1]

    def uv(box):
        return {"u": [(box[0] - b[0]) / w, (box[2] - b[0]) / w], "v": [1.0 - (box[3] - b[1]) / h, 1.0 - (box[1] - b[1]) / h]}

    return {"plate": uv(MEAS["D5_plate"]["box"]), "handle": uv(MEAS["D5_handle"]["box"]), "spy": uv(MEAS["D5_spy"]["box"]),
            "ratio_w_h": w / h, "scale_mm_px": MEAS["D5_leaf"]["leaf_mm"][1] / h}


def d2_f4_fractions():
    m = MEAS["D2_F4_cols"]
    x0 = m["leaf_x_px"][0]
    s = m["scale_mm_px"]
    return {"lights_mm": [[LAP + (a - x0) * s, LAP + (b - x0) * s] for a, b in m["light_x_px"]], "bars_mm": [[LAP + (a - x0) * s, LAP + (b - x0) * s] for a, b in m["bar_x_px"]],
            "scale_mm_px": s}


def d1_r_fractions():
    m = MEAS["D1_R"]
    t, b = m["leaf_rows_px"]
    h = b - t
    return {"lights_v": [[1.0 - (hi - t) / h, 1.0 - (lo - t) / h] for lo, hi in m["light_rows_px"]],
            "plate_v": [1.0 - (m["plate_rows_px"][1] - t) / h, 1.0 - (m["plate_rows_px"][0] - t) / h], "scale_mm_px": 1981.0 / h}


# ---- mouldings
def stuck_ovolo_profile():
    """A stuck (planted) ovolo moulding round a flat panel of an inter-war two-panel door, (d across the face from the moulding's outer edge, h above the
    framing face). 20 wide, 6.5 proud, quarter-round with a 1.5 mm fillet. Judgement: D1 shows the panels as narrow lit edges, no bolection."""
    pts = [(0.0, 0.0), (0.0, 1.5)]
    for i in range(1, 11):
        a = math.radians(90.0 * i / 10)
        pts.append((_r(1.5 + 14.0 * (1 - math.cos(a)), 2), _r(1.5 + 5.0 * math.sin(a), 2)))
    pts += [(18.0, 6.5), (20.0, 5.5), (20.0, 0.0)]
    return [[a, b] for a, b in pts]


def embossed_step_profile():
    """The edge of an embossed panel of a moulded door (D4 right door): the field 6 mm below the border, a 14 mm wide cove (d, depth below the border face)."""
    return [[0.0, 0.0], [1.5, 0.4], [4.0, 3.0], [8.0, 5.2], [12.0, 5.9], [14.0, 6.0], [40.0, 6.0]]


def reeded_section(width=24.0, pitch=6.0, depth=1.2):
    """Reeded glass seen in section: flutes of a 6 mm pitch, each a circular segment 1.2 mm deep (D5's transom and sidelight)."""
    pts = [[0.0, 4.0]]
    n = int(round(width / pitch))
    for i in range(n):
        x0 = i * pitch
        for j in range(0, 7):
            t = j / 6.0
            pts.append([_r(x0 + t * pitch, 3), _r(4.0 + depth * math.sin(math.pi * t), 3)])
    pts.append([width, 0.0])
    pts.append([0.0, 0.0])
    return pts


def v_joint_profile(w=6.0, d=2.0):
    """A V joint between two matchboards (F7): 6 mm wide, 2 mm deep, (d across, h from the face)."""
    return [[-w / 2.0, 0.0], [0.0, -d], [w / 2.0, 0.0]]


# ---- the kinds
def build_kinds(A):
    """A = the 3.1 target as built (departures applied). Returns the kinds dictionary."""
    T1 = A
    F1 = A["variants"]["flat_door_over_shop"]["parts"]
    tl = T1["leaf"]
    fl = F1["leaf"]
    t_open = T1["panels"]["openings_leaf_uv_mm"]
    f_open = F1["panels"]["openings_leaf_uv_mm"]
    bol_t = T1["mouldings"]["outside_bolection"]
    bol_f = F1["mouldings"]["outside_bolection"]
    K = {}

    def opening(id_, typ, u0, u1, v0, v1, **kw):
        d = {"id": id_, "type": typ, "u0": _r(u0), "u1": _r(u1), "v0": _r(v0), "v1": _r(v1)}
        d.update(kw)
        return d

    # ------------------------------------------------------------------ T1 (kept, 3.1 T1 as built)
    ops = [opening(k, "panel", o["u0"], o["u1"], o["v0"], o["v1"], moulding="bolection_outside", glass=None) for k, o in t_open.items()]
    K["T1"] = {
        "name": "four-panel front door with a transom, in its brick opening (3.1 T1)", "frame_set": "T", "family": "cottage front door",
        "leaf": {"w": tl["width_mm"], "h": tl["height_mm"], "t": tl["thickness_mm"], "construction": "framed", "lock_side": "right",
                 "stile_left": tl["stile_mm"], "stile_right": tl["stile_mm"], "top_rail": tl["top_rail_mm"], "bottom_rail": tl["bottom_rail_mm"],
                 "lock_rail": tl["lock_rail_mm"], "lock_rail_centre_v": tl["lock_rail_centre_above_leaf_bottom_mm"], "muntin": tl["muntin_mm"], "openings": ops},
        "mouldings": {"outside": {"kind": "bolection", "width_on_face": 46.0, "profile_dh": bol_t["profile_dh_mm"], "src": "3.1 as built (departures D7: 46, target 36)"},
                      "band_and_weatherboard": "kept: lock-rail band 72.5 high and weatherboard 80 high as built (3.1 D4, D6)"},
        "glass": {"transom": "plain_3mm", "leaf": None},
        "photographs": ["P1"],
        "parts_vs_3_1": [
            ("frame_jamb_l/r, frame_head, frame_transom, glass_fanlight, frame_glazing_bead", "kept", "the passed frame set T and its transom, untouched"),
            ("leaf_frame, panel_*, moulding_bolection_*, moulding_single_*, moulding_band, moulding_weatherboard", "kept", "passed in 3.1 (fresh reviews of 9 October)"),
            ("iron_letter_plate, flap, lip", "kept", "LP1, the vertical brass plate"),
            ("iron_lock, collar, plug", "kept", "LK1, the rim night latch (the 3.1 name for it was cylinder lock)"),
            ("iron_bellpush", "kept", "the plain dark oblong of P1: one part, 22 x 72.6, 3 proud; the handover's fix"),
            ("iron_bellpush_bezel, iron_bellpush_button", "removed", "the two-part push read as a modern video doorbell (3.1 review v2 close); deleted, not replaced by any ring or lens"),
            ("stone_threshold, stone_riser, stone_tread", "kept", "the step of 3.1; the wall's plinth returns stay with the wall kit"),
            ("iron_keyhole_*, iron_knob_*", "not present", "T1 never had them"),
        ],
    }

    # ------------------------------------------------------------------ T2 (four stacked lights, leaded fanlight; D3, D1 right door)
    f3 = d3_fractions()
    lh = tl["height_mm"]
    # visible top rail 0.030 of the visible height (58 mm) plus the 20.4 hidden behind the transom's stop = 78.4 structural; stiles 114.3 (3.1's; visible 93.9, D3 reads 92)
    top_rail, bottom_rail, bar, stile = 78.4, 205.0, 30.0, tl["stile_mm"]
    light_h = (lh - top_rail - bottom_rail - 3 * bar) / 4.0
    lights = []
    v = bottom_rail
    for i in range(4):
        lights.append(opening("light%d" % (i + 1), "light", stile, tl["width_mm"] - stile, v, v + light_h, glass="plain_3mm", bead="planted_quarter_round_10x8"))
        v += light_h + bar
    K["T2"] = {
        "name": "four stacked lights over a low rail, a leaded diamond fanlight (D3, D1)", "frame_set": "T", "family": "cottage front door",
        "leaf": {"w": tl["width_mm"], "h": lh, "t": tl["thickness_mm"], "construction": "framed, glazed", "lock_side": "left",
                 "stile_left": stile, "stile_right": stile, "top_rail": top_rail, "bottom_rail": bottom_rail, "bar": bar, "light_h": _r(light_h, 2), "openings": lights,
                 "visible_note": "structural numbers; the visible top rail is 58 (78.4 less the 20.4 behind the transom's stop) and the visible stiles 93.9"},
        "mouldings": {"outside": {"kind": "none", "note": "glazing bars 30 wide x 22 deep, square, eased 1 mm; stiles and rails square, eased 1.5; the bead is the 3.1 planted quarter-round 10 x 8 on all four sides of each light"}},
        "glass": {"transom": "leaded_diamond", "leaf": "plain_3mm", "nets_behind": "white net card behind the lights (D3 shows one), the windows target's net N1 white"},
        "photographs": ["D3", "D1"],
        "measured_fractions_of_leaf_height": {"top_rail": _r(f3["top_rail"], 4), "bar": _r(f3["bar"], 4), "light": _r(f3["light"], 4), "bottom_rail": _r(f3["bottom_rail"], 4)},
        "parts_vs_3_1": [
            ("frame_jamb_l/r, frame_head, frame_transom, frame_glazing_bead (transom)", "kept", "frame set T"),
            ("glass_fanlight", "changed", "plain 3 mm glass becomes a leaded diamond light (came 6 wide, diamonds 95 x 70): D3 shows a leaded fanlight over this door; the height (P6's is 624 mm) is not taken, the T frame's 267 mm stays"),
            ("leaf_frame", "changed", "stiles 114.3 (visible 93.9), top rail 78.4 (visible 58), bottom rail 205, no lock rail, no muntin; four openings 584.2 x 393.7 with 30 mm bars (D3's fractions of the visible face 0.030, 0.2066, 0.0158, 0.105)"),
            ("panel_*, moulding_bolection_*, moulding_single_*, moulding_band, moulding_weatherboard", "removed", "a glazed door has no panels or mouldings; D3 and D1 show none"),
            ("glass (new parts glass_light1..4) and bead", "added", "four panes of 3 mm glass, each with the 3.1 planted bead"),
            ("iron_letter_plate", "changed", "LP5, a pale low plate in the bottom rail, as D1 and D4 show (the vertical brass plate has no muntin to sit on)"),
            ("iron_lock, collar, plug", "removed", "no latch cylinder is read on D3's leaf; a bar pull stands in (HD3)"),
            ("iron_bellpush", "removed", "none on D3"),
            ("stone_*", "kept", "the step of 3.1 under the same opening"),
        ],
    }

    # ------------------------------------------------------------------ T3 (moulded modern door, small arched light; D4 right door)
    f4 = d4_t3_fractions()
    w3, h3 = tl["width_mm"], tl["height_mm"]
    up = to_struct("T", f4["upper"]["u"], f4["upper"]["v"])
    li = to_struct("T", f4["light"]["u"], f4["light"]["v"])
    lo = to_struct("T", f4["lower"]["u"], f4["lower"]["v"])
    ops3 = [
        opening("upper_panel", "embossed_panel", up[0], up[1], up[2], up[3], moulding="embossed_step"),
        opening("small_light", "arched_light", li[0], li[1], li[2], li[3], glass="plain_3mm", head="semicircle", bead="moulded"),
        opening("lower_panel", "embossed_panel", lo[0], lo[1], lo[2], lo[3], moulding="embossed_step"),
    ]
    K["T3"] = {
        "name": "white moulded modern door with a small arched light (D4 right door)", "frame_set": "T", "family": "modernised cottage",
        "leaf": {"w": w3, "h": h3, "t": 44.0, "construction": "moulded flush sheet over a core, painted-look gloss", "lock_side": "right", "border": 65.0, "openings": ops3},
        "mouldings": {"outside": {"kind": "embossed panel step", "profile_dh": embossed_step_profile(), "note": "each embossed panel is a field 6 mm below the border face, edged by a 14 mm cove; the border is 65 wide all round; no applied mouldings"}},
        "glass": {"transom": "plain_3mm", "leaf": "plain_3mm"},
        "photographs": ["D4"],
        "measured_fractions_of_leaf": {k: v for k, v in f4.items() if k != "scale_mm_px"},
        "parts_vs_3_1": [
            ("frame_jamb_l/r, frame_head, frame_transom, glass_fanlight, frame_glazing_bead", "kept", "frame set T; D4's door has a plain dark transom light over it"),
            ("leaf_frame, panel_*, moulding_*", "changed", "no stiles or rails: one moulded sheet 44 thick with two embossed panels and a small arched light (D4's fractions)"),
            ("glass_light (new part)", "added", "one pane about 200 x 460 with a semicircular head, glazed from inside with a moulded bead"),
            ("iron_letter_plate", "changed", "LP6, a white oblong 270 x 50 in the border between the panels (D4: 0.448 of the visible height)"),
            ("iron_lock, collar, plug", "removed", "D4 shows none outside; a small lever HD2c at the lock edge"),
            ("iron_bellpush, stone_*", "removed / kept", "no push; the step of 3.1 stays"),
        ],
    }

    # ------------------------------------------------------------------ F1 (kept, 3.1 F1 as built)
    opsf1 = [opening(k, "panel", o["u0"], o["u1"], o["v0"], o["v1"], moulding="bolection_outside", glass=None) for k, o in f_open.items()]
    K["F1"] = {
        "name": "four-panel flat door (3.1 F1)", "frame_set": "F", "family": "side door to a flat",
        "leaf": {"w": fl["width_mm"], "h": fl["height_mm"], "t": fl["thickness_mm"], "construction": "framed", "lock_side": "right",
                 "stile_left": fl["stile_mm"], "stile_right": fl["stile_mm"], "top_rail": fl["top_rail_mm"], "bottom_rail": fl["bottom_rail_mm"],
                 "lock_rail": fl["lock_rail_mm"], "lock_rail_centre_v": fl["lock_rail_centre_above_leaf_bottom_mm"], "muntin": fl["muntin_mm"], "openings": opsf1},
        "mouldings": {"outside": {"kind": "bolection", "width_on_face": 43.0, "profile_dh": bol_f["profile_dh_mm"], "src": "3.1 as built (departures D8: 43)"}},
        "glass": {"transom": "plain_3mm", "leaf": None},
        "photographs": ["P2", "P1"],
        "parts_vs_3_1": [
            ("everything of door_F1.glb", "kept", "passed in 3.1 (street and close views); the street's F1 is that model, unchanged"),
            ("iron_knob_*, iron_keyhole_*", "kept", "F1's turned centre knob and plugged keyhole as built; on the houses given F1 the knob is HD0 'none' unless the house table says HD1 (F1 has the rose and knob in 3.1: kept as an option, not on a house)"),
        ],
    }

    # ------------------------------------------------------------------ F2 (six panels, P2 via 3.1's option; its fractions are of the VISIBLE face 797.2 x 1960.6)
    opt = A["variants"]["option_six_panel"]
    fh = opt["fractions_of_visible_height"]
    fw = opt["fractions_of_visible_width"]
    VW, VH = VIS["F"]
    W, H = fl["width_mm"], fl["height_mm"]
    bot_rail = fh["bottom_rail"] * VH
    bot_panel = fh["bottom_panels"] * VH
    lock_rail = fh["lock_rail"] * VH
    long_panel = fh["long_panels"] * VH
    frieze = fh["frieze_rail"] * VH
    small_up = fh["small_upper_panels"] * VH
    top_rail2 = fh["top_rail"] * VH + LAP
    stile2 = fw["stile"] * VW + LAP
    muntin2 = fw["muntin"] * VW
    pw = (W - 2 * stile2 - muntin2) / 2.0
    cols = [(stile2, stile2 + pw), (stile2 + pw + muntin2, W - stile2)]
    rows = []
    v = bot_rail
    for name, hh in (("bottom", bot_panel), ("lock_rail", lock_rail), ("long", long_panel), ("frieze", frieze), ("small_upper", small_up)):
        rows.append((name, v, v + hh))
        v += hh
    ops2 = []
    for name, v0, v1 in rows:
        if name in ("lock_rail", "frieze"):
            continue
        for ci, (u0, u1) in enumerate(cols):
            ops2.append(opening("%s_%s" % (name, "lr"[ci]), "panel", u0, u1, v0, v1, moulding="bolection_outside"))
    K["F2"] = {
        "name": "six-panel flat door (P2)", "frame_set": "F", "family": "side door to a flat",
        "leaf": {"w": W, "h": H, "t": fl["thickness_mm"], "construction": "framed", "lock_side": "right", "stile_left": _r(stile2), "stile_right": _r(stile2), "top_rail": _r(top_rail2),
                 "bottom_rail": _r(bot_rail), "lock_rail": _r(lock_rail), "frieze_rail": _r(frieze), "muntin": _r(muntin2), "openings": ops2},
        "mouldings": {"outside": {"kind": "bolection", "width_on_face": 43.0, "profile_dh": bol_f["profile_dh_mm"], "src": "3.1 F1 as built (P2, 43)"}},
        "glass": {"transom": "plain_3mm", "leaf": None},
        "photographs": ["P2"],
        "fractions_of_visible_height": fh, "fractions_of_visible_width": fw,
        "parts_vs_3_1": [
            ("frame_*, glass_fanlight, timber sill", "kept", "frame set F, the 49 mm jambs, the weathered transom, the sill"),
            ("leaf_frame, panel_*, moulding_bolection_*", "changed", "six panels (two small, two long, two small) from 3.1's option_six_panel fractions of P2; the same bolection profile at 43"),
            ("iron_knob_*, iron_keyhole_*, iron_lock_*", "kept", "the centre knob on the lock rail and the plugged keyhole, at P2's heights (fractions 0.305, 0.606, cylinder 0.546)"),
            ("iron_letter_plate", "changed", "LP2, the horizontal brass plate 195 x 70 at 0.788 of the height, P2's"),
        ],
    }

    # ------------------------------------------------------------------ F3 (two long panels, D1 left door)
    ops_f3 = [opening("long_l", "panel", f_open["bottom_left"]["u0"], f_open["bottom_left"]["u1"], fl["bottom_rail_mm"], 1854.0, moulding="stuck_ovolo"),
              opening("long_r", "panel", f_open["bottom_right"]["u0"], f_open["bottom_right"]["u1"], fl["bottom_rail_mm"], 1854.0, moulding="stuck_ovolo")]
    K["F3"] = {
        "name": "two long panels (D1 left door)", "frame_set": "F", "family": "side door to a flat",
        "leaf": {"w": fl["width_mm"], "h": fl["height_mm"], "t": fl["thickness_mm"], "construction": "framed", "lock_side": "left", "stile_left": fl["stile_mm"],
                 "stile_right": fl["stile_mm"], "top_rail": fl["top_rail_mm"], "bottom_rail": fl["bottom_rail_mm"], "muntin": fl["muntin_mm"], "openings": ops_f3},
        "mouldings": {"outside": {"kind": "stuck ovolo", "width_on_face": 20.0, "profile_dh": stuck_ovolo_profile(), "src": "Judgement: D1 shows two long flat panels with narrow lit edges, no bolection"}},
        "glass": {"transom": "plain_3mm", "leaf": None},
        "photographs": ["D1"],
        "parts_vs_3_1": [
            ("frame_*, glass_fanlight, sill", "kept", "frame set F"),
            ("leaf_frame, panel_*", "changed", "no lock rail: the muntin runs the full height between the 127 top rail and the 192.8 bottom rail; two panels 244.7 x 1661.2 (D1 shows no cross rail on this door)"),
            ("moulding_bolection_*", "changed", "a stuck ovolo moulding 20 wide, 6.5 proud, replaces the 43 mm bolection (D1 shows thin lit edges)"),
            ("iron_letter_plate", "kept", "LP1 on the muntin, at the 3.1 height 1617"),
            ("iron_knob_*, iron_keyhole_*", "removed", "a bar pull HD3 on the left stile (D1 shows a vertical metal strip on that stile)"),
        ],
    }

    # ------------------------------------------------------------------ F4 (three long narrow lights, D2 left door)
    fx = d2_f4_fractions()
    lock_st, hinge_st, barw = 184.0, 114.3, 36.0      # structural; visible 164 and 93.9 (D2 at 23.3 mm a pixel: lock stile 7 px, lights 140 to 155, bars 35, the hinge stile hidden)
    lw = (W - lock_st - hinge_st - 2 * barw) / 3.0
    top_r4, bot_r4 = 90.4, 200.0                      # visible top rail 70 (D2: 3 px at 23.3) + 20.4 behind the transom's stop
    ops4 = []
    u = lock_st
    for i in range(3):
        ops4.append(opening("light%d" % (i + 1), "light", u, u + lw, bot_r4, H - top_r4, glass="plain_3mm", bead="putty_fillet"))
        u += lw + barw
    K["F4"] = {
        "name": "three long narrow lights over a low rail (D2 left door)", "frame_set": "F", "family": "side door to a flat",
        "leaf": {"w": W, "h": H, "t": fl["thickness_mm"], "construction": "framed, glazed", "lock_side": "left", "stile_left": lock_st, "stile_right": hinge_st, "top_rail": top_r4,
                 "bottom_rail": bot_r4, "bar": barw, "light_w": _r(lw, 2), "openings": ops4},
        "mouldings": {"outside": {"kind": "none", "note": "bars 36 wide, square; putty fillet on the glass as F1's"}},
        "glass": {"transom": "plain_3mm", "leaf": "plain_3mm", "nets_behind": "none (D2 shows a dark hall)"},
        "photographs": ["D2"],
        "measured_from_left_edge_mm": {"lights": [[_r(a, 1), _r(b, 1)] for a, b in fx["lights_mm"]], "bars": [[_r(a, 1), _r(b, 1)] for a, b in fx["bars_mm"]], "scale_mm_px": fx["scale_mm_px"]},
        "parts_vs_3_1": [
            ("frame_*, glass_fanlight, sill", "kept", "frame set F"),
            ("leaf_frame, panel_*, moulding_*", "changed", "stiles 184 and 114.3 (visible 164 and 93.9), top rail 90.4 (visible 70), bottom rail 200, three lights 155.9 wide with 36 mm bars (D2 at 23.3 mm a pixel: lights 140 to 152, bars 35)"),
            ("glass_light1..3", "added", "three tall panes of 3 mm glass, putty fillet as F1's"),
            ("iron_letter_plate", "changed", "LP5, the low plate in the bottom rail"),
            ("iron_knob_*, iron_keyhole_*, iron_lock_*", "removed", "a lever HD2b at the left stile"),
        ],
    }

    # ------------------------------------------------------------------ F5 (flush door with a slit light, D2 middle, D4 left)
    f5 = d2_f5_fractions()
    s_u0, s_u1, s_v0, s_v1 = to_struct("F", f5["slit"]["u"], f5["slit"]["v"])
    K["F5"] = {
        "name": "flush door with a tall slit light (D2 middle door, D4 left door)", "frame_set": "F", "family": "side door to a flat, modernised",
        "leaf": {"w": W, "h": H, "t": 44.0, "construction": "flush, hardboard-faced, lipped", "lock_side": "left", "lipping": 6.0,
                 "openings": [opening("slit", "slit_light", s_u0, s_u1, s_v0, s_v1, glass="plain_3mm", bead="timber_bead_15")]},
        "mouldings": {"outside": {"kind": "none", "note": "flat painted face; a 1 mm hairline round the lipping; the slit has a 15 mm square timber bead, 4 proud"}},
        "glass": {"transom": "plain_3mm", "leaf": "plain_3mm"},
        "photographs": ["D2", "D4"],
        "measured_fractions_of_leaf": {k: v for k, v in f5.items() if not k.startswith("scale")},
        "parts_vs_3_1": [
            ("frame_*, glass_fanlight, sill", "kept", "frame set F"),
            ("leaf_frame, panel_*, moulding_*", "changed", "one flush slab 44 thick, lipped; no panels or mouldings"),
            ("glass_slit (new)", "added", "one pane about 205 x 900 centred on the leaf (D2: 8.8 x 37.5 px at 23 to 24 mm a pixel)"),
            ("iron_letter_plate", "changed", "LP7, a pale 265 x 50 plate under the slit, centre about 829"),
            ("iron_knob_*, iron_keyhole_*, iron_lock_*", "removed", "a lever HD2b at the left edge, v 1093"),
        ],
    }

    # ------------------------------------------------------------------ F6 (council flush door, D5), leaf 762 in the F frame (stops move in)
    f6 = d5_fractions()
    w6 = 762.0
    K["F6"] = {
        "name": "council-style flush door, olive in D5, turquoise in D9 (leaf 762, shown whole)", "frame_set": "F, with planted inside stops (frame_change)", "family": "council or modernised",
        "leaf": {"w": w6, "h": H, "t": 44.0, "construction": "flush, plywood-faced, lipped", "lock_side": "right", "lipping": 6.0,
                 "openings": [opening("spyhole", "spyhole", w6 * 0.5 - 7.0, w6 * 0.5 + 7.0, 1502.0, 1516.0, glass="lens_14")]},
        "frame_change": {"clear_between_faces": 765.2, "jamb_showing": 117.6, "stops": "planted on the inside face: the leaf shows whole, nothing laps in front, the 1.6 mm margins show the stop behind (not the hall)",
                         "why": "D5's leaf is 325 x 835 px = 0.389 of its height, a 2 ft 6 in (762) leaf seen whole, with a white frame about 130 wide beside it (55 px at 2.37 mm); 3.1's lapped 838 leaf would read 0.407. The frame's outer width 1000.4 is kept, so the jambs show (1000.4 - 765.2) / 2 = 117.6"},
        "mouldings": {"outside": {"kind": "none", "note": "flat face; the lipping line 1 mm; no panel, no moulding"}},
        "glass": {"transom": "reeded_4mm", "leaf": None, "sidelight": "none in the street (D5's reeded sidelight is not built)"},
        "photographs": ["D5", "D9"],
        "measured_fractions_of_leaf": {k: v for k, v in f6.items() if not k.startswith("scale")},
        "parts_vs_3_1": [
            ("frame_jamb_l/r, frame_stop_bead_*", "changed", "the stops are planted on the inside face and the jambs show 117.6 each (clear between faces 765.2); the leaf shows whole"),
            ("frame_transom, glass_fanlight", "changed", "the transom's x range shortens to the jambs' inner faces; its glass is reeded 4 mm (D5: ribbed transom)"),
            ("leaf_frame, panel_*, moulding_*", "changed", "one flush slab 762 x 1981 x 44, lipped"),
            ("iron_letter_plate", "changed", "LP4, a chrome-look oblong 250 x 70, flush, at u 386, v 912 (D5)"),
            ("iron_knob_*, iron_keyhole_*, iron_lock_*", "removed", "lever HD2a at the right edge, v 902; a spyhole 14 across at v 1509 (D5, place only)"),
        ],
    }

    # ------------------------------------------------------------------ F7 (ledged and braced service door; Hasluck)
    w7 = fl["width_mm"]
    bw = w7 / 6.0
    boards = [_r(i * bw, 2) for i in range(7)]
    ledges = [[100.0, 240.0], [920.0, 1060.0], [1741.0, 1881.0]]
    nails = []
    for lv in ledges:
        for i in range(6):
            nails.append([_r(i * bw + bw / 2.0, 1), _r((lv[0] + lv[1]) / 2.0, 1)])
    K["F7"] = {
        "name": "ledged and braced service door (Hasluck; no period photograph read)", "frame_set": "F", "family": "service door",
        "leaf": {"w": w7, "h": H, "t": 38.0, "construction": "ledged and braced matchboarding", "lock_side": "right", "board_w": _r(bw, 2), "boards": 6, "board_edges_u": boards,
                 "board_t": 22.0, "joint": "tongued and grooved with a V joint 6 wide, 2 deep", "ledges_v": ledges, "ledge_t": 25.0, "braces": "two, back, from the foot of the hinge ledge to the head of the lock ledge",
                 "nail_heads": {"dia": 9.0, "proud": 3.0, "at": nails, "note": "one head per board at each ledge, driven from the face and clenched behind (Hasluck p.316)"}, "openings": []},
        "mouldings": {"outside": {"kind": "v_joint", "profile": v_joint_profile()}},
        "glass": {"transom": "plain_3mm", "leaf": None},
        "photographs": [],
        "sources": "Read: Hasluck pp.312-317, Figs. 1015-1039: boards 3 to 7 in wide (139.7 mm = 5.5 in used, six across 838), 3/4 to 1 1/4 in thick (22.2 used), grooved and tongued, V joint; ledges nailed with wrought nails driven from the face and clenched; hook-and-plate hinges inside for an inward door. Sizes of ledges, nail heads and leaf: Judgement (no photograph of such a door on these streets was reached).",
        "parts_vs_3_1": [
            ("frame_*, glass_fanlight, sill", "kept", "frame set F; a service door also takes the transom light"),
            ("leaf_frame, panel_*, moulding_*", "changed", "six matchboards 139.7 wide, V-jointed, 22 thick, three ledges and two braces behind (not visible), nail heads in rows on the face"),
            ("iron_letter_plate, iron_knob_*, iron_keyhole_*, iron_lock_*", "removed", "a service door has no letter plate; HD4, a thumb latch, on the lock side"),
        ],
    }
    return K
