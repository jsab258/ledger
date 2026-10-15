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
    sv = MEAS["D3_leaf"]["leaf_mm"][1] / h                 # 10.07 mm a pixel, fitted on the height only
    rows = MEAS["D3_rows"]["rows_px"]
    top_rail = (rows["light1"][0] - b[1]) / h
    bar = [(rows["light%d" % (i + 1)][0] - rows["light%d" % i][1]) / h for i in range(1, 4)]
    light = [(rows["light%d" % i][1] - rows["light%d" % i][0]) / h for i in range(1, 5)]
    bottom_rail = (b[3] - rows["light4"][1]) / h
    st = MEAS["D3_stiles"]
    return {"top_rail": top_rail, "bar": sum(bar) / 3.0, "light": sum(light) / 4.0, "bottom_rail": bottom_rail,
            "white_left_mm": (st["left_px"][1] - st["left_px"][0]) * sv, "white_right_mm": (st["right_px"][1] - st["right_px"][0]) * sv,
            "scale_mm_px": sv}


# T3: the review's u values (each outline centred on the leaf's centre line: the door is seen a little obliquely, so u is not scaled off the columns) and v from the rows,
# v = (foot row - row) x 21.66 mm a pixel.
T3_U = {"outer": (119.9, 692.9), "inner": (182.4, 630.4), "light": (297.4, 515.4)}
T3_HEAD_RISE = 22.0        # the inner outline's segmental head: springing 22 below the crown (the arched moulding line, rows 358.5 in the middle, 359 at the sides)


def d4_t3_v(row):
    m = MEAS["D4_T3_leaf"]
    return (m["box"][3] - row) * m["scale_mm_px"]


def t3_mm():
    """T3's outlines in the leaf frame (mm): u from the review, v from the rows of the recorded boxes."""
    def vv(key):
        b = MEAS[key]["box"]
        return (d4_t3_v(b[3]), d4_t3_v(b[1]))
    lt, up, upi, lo, loi = vv("D4_T3_light"), vv("D4_T3_upper"), vv("D4_T3_upper_inner"), vv("D4_T3_lower"), vv("D4_T3_lower_inner")
    r = lambda x: round(x, 1)
    return {
        "light": [T3_U["light"][0], T3_U["light"][1], r(lt[0]), r(lt[1])],
        "upper_outer": [T3_U["outer"][0], T3_U["outer"][1], r(up[0]), r(up[1])],
        "upper_inner": {"u0": T3_U["inner"][0], "u1": T3_U["inner"][1], "v0": r(upi[0]), "v1": r(upi[1]), "head": "segmental", "springing_below_crown": T3_HEAD_RISE},
        "lower_outer": [T3_U["outer"][0], T3_U["outer"][1], r(lo[0]), r(lo[1])],
        "lower_inner": {"u0": T3_U["inner"][0], "u1": T3_U["inner"][1], "v0": r(loi[0]), "v1": r(loi[1]), "head": "flat"},
    }


def d4_t3_fractions():
    """The measured side: each recorded box as fractions of the leaf box (u of its width, v of its height from the foot); the plate and the lever v are what the furniture uses."""
    b = MEAS["D4_T3_leaf"]["box"]
    w, h = b[2] - b[0], b[3] - b[1]

    def uv(box):
        return {"u": [(box[0] - b[0]) / w, (box[2] - b[0]) / w], "v": [1.0 - (box[3] - b[1]) / h, 1.0 - (box[1] - b[1]) / h]}

    return {"upper": uv(MEAS["D4_T3_upper"]["box"]), "upper_inner": uv(MEAS["D4_T3_upper_inner"]["box"]), "light": uv(MEAS["D4_T3_light"]["box"]), "plate": uv(MEAS["D4_T3_plate"]["box"]),
            "lower": uv(MEAS["D4_T3_lower"]["box"]), "lower_inner": uv(MEAS["D4_T3_lower_inner"]["box"]), "handle": uv(MEAS["D4_T3_handle"]["box"]), "scale_mm_px": MEAS["D4_T3_leaf"]["scale_mm_px"]}


def d2_f5_fractions():
    b = MEAS["D2_F5_leaf"]["box"]
    w, h = b[2] - b[0], b[3] - b[1]

    def uv(box):
        return {"u": [(box[0] - b[0]) / w, (box[2] - b[0]) / w], "v": [1.0 - (box[3] - b[1]) / h, 1.0 - (box[1] - b[1]) / h]}

    return {"slit": uv(MEAS["D2_F5_slit"]["box"]), "plate": uv(MEAS["D2_F5_plate"]["box"]), "handle": uv(MEAS["D2_F5_handle"]["box"]),
            "scale_mm_px_v": MEAS["D2_F5_leaf"]["leaf_mm"][1] / h, "scale_mm_px_u": MEAS["D2_F5_leaf"]["leaf_mm"][0] / w}


# F5's v numbers are the review's (the box [561, 280.5, 594.5, 360] gives 875.5 to 1800.3, 776.8 and 1054.3: 5 to 11 mm more, inside the +-24; the review's figures are kept as chosen, the box's are the measured side)
F5_V = {"slit": (870.0, 1789.0), "plate": 772.0, "handle": 1048.0}


def d5_fractions():
    """D5 is an INDOOR landing door: only the fractions of its face are used (the places of the plate, lever, lock and spyhole), never its width or its frame."""
    b = MEAS["D5_leaf"]["box"]
    w, h = b[2] - b[0], b[3] - b[1]

    def uv(box):
        return {"u": [(box[0] - b[0]) / w, (box[2] - b[0]) / w], "v": [1.0 - (box[3] - b[1]) / h, 1.0 - (box[1] - b[1]) / h]}

    return {"plate": uv(MEAS["D5_plate"]["box"]), "handle": uv(MEAS["D5_handle"]["box"]), "lock": uv(MEAS["D5_lock"]["box"]), "spy": uv(MEAS["D5_spy"]["box"]),
            "scale_mm_px": MEAS["D5_leaf"]["leaf_mm"][1] / h}


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


# ---- the photograph table: every feature a photograph measures, as fractions of the kind's visible face, measured side and drawn side, with the allowed difference
BEAD = 10.0     # the planted bead round a light (3.1): part of the white beside the glass


def photo_table(T):
    """{(kind, photo): {feature: {"meas": {"u": [a, b] or None, "v": [a, b] or None}, "tol": {"u": x, "v": y}, "drawn": {...}}}}, all fractions of the kind's visible face
    (u of its width from the visible left edge, v of its height from the foot; the fanlight's features are fractions of its own light). "meas" comes from the recorded boxes in
    T["sources"]["measurements"], "drawn" from the kind's own openings and fittings in T, so a wrong copy of either side changes the difference. A point feature is [c, c]."""
    M = T["sources"]["measurements"]
    K = T["kinds"]
    FU = T["furniture"]
    out = {}

    def vis(k):
        return VIS[K[k]["frame_set"][0]]

    def opn(k, oid):
        return [o for o in K[k]["leaf"]["openings"] if o["id"] == oid][0]

    def dr_open(k, o):
        vw, vh = vis(k)
        return {"u": [(o["u0"] - LAP) / vw, (o["u1"] - LAP) / vw], "v": [o["v0"] / vh, o["v1"] / vh]}

    def dr_point(k, pl):
        vw, vh = vis(k)
        return {"u": [(pl["u"] - LAP) / vw] * 2, "v": [pl["v"] / vh] * 2}

    def rd(d):
        return {a: ([round(x, 4) for x in v] if v is not None else None) for a, v in d.items()}

    def feat(table, name, meas, drawn, tol_u, tol_v):
        table[name] = {"meas": rd(meas), "drawn": rd(drawn), "tol": {"u": round(tol_u, 4) if tol_u is not None else None, "v": round(tol_v, 4) if tol_v is not None else None}}

    # ---- T2 against D3 (square on; the scale is fitted on the height only)
    t = {}
    b = M["D3_leaf"]["box"]
    vw, vh = VIS["T"]
    sv = M["D3_leaf"]["leaf_mm"][1] / (b[3] - b[1])
    rows = M["D3_rows"]["rows_px"]
    tv = (M["D3_rows"]["error_px"] * sv + 8.0) / vh
    for i in range(1, 5):
        o = opn("T2", "light%d" % (5 - i))      # D3's light1 is the top one, T2's light1 the bottom one
        feat(t, "light%d_rows" % (5 - i), {"u": None, "v": [(b[3] - rows["light%d" % i][1]) * sv / vh, (b[3] - rows["light%d" % i][0]) * sv / vh]}, {"u": None, "v": [o["v0"] / vh, o["v1"] / vh]}, None, tv)
    st = M["D3_stiles"]
    tu = (st["error_px"] * sv + 5.0) / vw
    lf = K["T2"]["leaf"]
    feat(t, "white_left", {"u": [0.0, (st["left_px"][1] - st["left_px"][0]) * sv / vw], "v": None}, {"u": [0.0, (lf["stile_left"] - LAP + BEAD) / vw], "v": None}, tu, None)
    feat(t, "white_right", {"u": [1.0 - (st["right_px"][1] - st["right_px"][0]) * sv / vw, 1.0], "v": None}, {"u": [1.0 - (lf["stile_right"] - LAP + BEAD) / vw, 1.0], "v": None}, tu, None)
    feat(t, "glass_width", {"u": [(st["left_px"][1] - b[0]) * sv / vw, (st["right_px"][0] - b[0]) * sv / vw], "v": None},
         {"u": [(lf["stile_left"] + BEAD - LAP) / vw, (lf["w"] - lf["stile_right"] - BEAD - LAP) / vw], "v": None}, tu, None)
    fl = M["D3_fanlight"]
    fr_ = fl["rows_px"]
    fh = fr_["foot_strip"][1] - fr_["plain_pane"][0]
    g = T["glass"]["leaded_diamond"]
    light_h = 267.0
    ft = (fl["error_px"] / fh) + 0.02
    feat(t, "fan_foot_strip", {"u": None, "v": [0.0, (fr_["foot_strip"][1] - fr_["foot_strip"][0]) / fh]}, {"u": None, "v": [0.0, g["foot_came_above_foot"] / light_h]}, None, ft)
    feat(t, "fan_band", {"u": None, "v": [(fr_["foot_strip"][1] - fr_["foot_strip"][0]) / fh, 1.0 - (fr_["plain_pane"][1] - fr_["plain_pane"][0]) / fh]},
         {"u": None, "v": [g["foot_came_above_foot"] / light_h, (g["foot_came_above_foot"] + g["band_h"]) / light_h]}, None, ft)
    feat(t, "fan_plain_pane", {"u": None, "v": [1.0 - (fr_["plain_pane"][1] - fr_["plain_pane"][0]) / fh, 1.0]}, {"u": None, "v": [1.0 - g["plain_pane_h"] / light_h, 1.0]}, None, ft)
    feat(t, "fan_lozenge_pitch", {"u": [0.0, fl["lozenge_pitch_px"] * sv / vw], "v": None}, {"u": [0.0, g["lozenge"][0] / vw], "v": None}, (fl["error_px"] * sv) / vw + 0.01, None)
    out[("T2", "D3")] = t
    # ---- T2 against D1's blue door (oblique: rows only, 0.045)
    t = {}
    d1 = M["D1_R"]
    t0, bt = d1["leaf_rows_px"]
    for i, (lo, hi) in enumerate(d1["light_rows_px"]):
        o = opn("T2", "light%d" % (4 - i))
        feat(t, "light%d_rows" % (4 - i), {"u": None, "v": [1.0 - (hi - t0) / (bt - t0), 1.0 - (lo - t0) / (bt - t0)]}, {"u": None, "v": [o["v0"] / VIS["T"][1], o["v1"] / VIS["T"][1]]}, None, 0.045)
    out[("T2", "D1")] = t
    # ---- T3 against D4 (v from the rows; u centred on the leaf, widths from the columns at 21.66 mm a pixel)
    t = {}
    lb = M["D4_T3_leaf"]["box"]
    vw, vh = VIS["T"]
    sc = M["D4_T3_leaf"]["scale_mm_px"]

    def mv(box):
        return [1.0 - (box[3] - lb[1]) / (lb[3] - lb[1]), 1.0 - (box[1] - lb[1]) / (lb[3] - lb[1])]

    def mu(box):
        w = (box[2] - box[0]) * sc / vw
        return [0.5 - w / 2.0, 0.5 + w / 2.0]

    tu4 = 1.5 * sc / vw
    tv4 = 1.5 * sc / vh
    for name, key, oid, sub in (("small_light", "D4_T3_light", "small_light", None), ("upper_outer", "D4_T3_upper", "upper_panel", None), ("upper_inner", "D4_T3_upper_inner", "upper_panel", "inner"),
                                ("lower_outer", "D4_T3_lower", "lower_panel", None), ("lower_inner", "D4_T3_lower_inner", "lower_panel", "inner")):
        o = opn("T3", oid)
        src = o.get("inner") if sub else o
        if src is None:        # a panel with no inner outline has no such feature (the self-check's row on the two outlines fails)
            continue
        feat(t, name, {"u": mu(M[key]["box"]), "v": mv(M[key]["box"])}, {"u": [(src["u0"] - LAP) / vw, (src["u1"] - LAP) / vw], "v": [src["v0"] / vh, src["v1"] / vh]}, tu4, tv4)
    pl = FU["letter_plate"]["LP6"]["place"]["T3"]
    pb = M["D4_T3_plate"]["box"]
    feat(t, "plate_v", {"u": None, "v": [sum(mv(pb)) / 2.0] * 2}, {"u": None, "v": [pl["v"] / vh] * 2}, None, tv4)
    hp = FU["handle"]["HD2c"]["place"]["T3"]
    hb = M["D4_T3_handle"]["box"]
    feat(t, "lever_v", {"u": None, "v": [sum(mv(hb)) / 2.0] * 2}, {"u": None, "v": [hp["v"] / vh] * 2}, None, tv4 + 0.005)
    out[("T3", "D4")] = t
    # ---- F5 against D2's middle door
    t = {}
    vw, vh = VIS["F"]
    lb = M["D2_F5_leaf"]["box"]
    w_, h_ = lb[2] - lb[0], lb[3] - lb[1]
    sv5 = M["D2_F5_leaf"]["leaf_mm"][1] / h_

    def uv5(box):
        return {"u": [(box[0] - lb[0]) / w_, (box[2] - lb[0]) / w_], "v": [1.0 - (box[3] - lb[1]) / h_, 1.0 - (box[1] - lb[1]) / h_]}

    def uvc(box):
        m = uv5(box)
        return {"u": [sum(m["u"]) / 2.0] * 2, "v": [sum(m["v"]) / 2.0] * 2}

    e5 = (M["D2_F5_slit"]["error_px"] * sv5 + 12.0) / vh
    feat(t, "slit", uv5(M["D2_F5_slit"]["box"]), dr_open("F5", opn("F5", "slit")), e5 * vh / vw, e5)
    feat(t, "plate", uvc(M["D2_F5_plate"]["box"]), dr_point("F5", FU["letter_plate"]["LP7"]["place"]["F5"]), 0.03, 0.03)
    feat(t, "lever", uvc(M["D2_F5_handle"]["box"]), dr_point("F5", FU["handle"]["HD2b"]["place"]["F5"]), 0.03, 0.03)
    out[("F5", "D2")] = t
    # ---- F4 against D2's left door: the lights across, from the leaf's visible left edge
    t = {}
    c = M["D2_F4_cols"]
    x0 = c["leaf_x_px"][0]
    s4 = c["scale_mm_px"]
    for i, (a, bb) in enumerate(c["light_x_px"]):
        o = opn("F4", "light%d" % (i + 1))
        feat(t, "light%d_across" % (i + 1), {"u": [(a - x0) * s4 / vw, (bb - x0) * s4 / vw], "v": None}, {"u": [(o["u0"] - LAP) / vw, (o["u1"] - LAP) / vw], "v": None}, (c["error_px"] * s4 + 10.0) / vw, None)
    out[("F4", "D2")] = t
    # ---- F6 against D5 (an indoor door: the places of the fittings as fractions of its face)
    t = {}
    lb = M["D5_leaf"]["box"]
    w_, h_ = lb[2] - lb[0], lb[3] - lb[1]

    def c5(box):
        return {"u": [((box[0] + box[2]) / 2.0 - lb[0]) / w_] * 2, "v": [1.0 - ((box[1] + box[3]) / 2.0 - lb[1]) / h_] * 2}

    for name, key, pl in (("plate", "D5_plate", FU["letter_plate"]["LP4"]["place"]["F6"]), ("lever", "D5_handle", FU["handle"]["HD2a"]["place"]["F6"]), ("lock", "D5_lock", FU["latch"]["LK3"]["place"]["F6"])):
        feat(t, name, c5(M[key]["box"]), dr_point("F6", pl), M[key]["error_px"] / w_ + 0.008, M[key]["error_px"] / h_ + 0.008)
    sp = opn("F6", "spyhole")
    feat(t, "spyhole", c5(M["D5_spy"]["box"]), {"u": [((sp["u0"] + sp["u1"]) / 2.0 - LAP) / vw] * 2, "v": [((sp["v0"] + sp["v1"]) / 2.0) / vh] * 2}, M["D5_spy"]["error_px"] / w_ + 0.01, M["D5_spy"]["error_px"] / h_ + 0.01)
    out[("F6", "D5")] = t
    return out


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


def embossed_step_profile(margin=62.0):
    """The edge of a moulded panel of the moulded door (D4 right door), which has TWO outlines: from the outer outline inwards (d across the face, h below the border face):
    a 14 mm cove down 3 mm to the margin, the margin flat and raised (62 wide: the 70 to 85 mm the photograph shows, less the two coves' halves), a second 14 mm cove down
    another 3 mm to the field, which lies 6 mm below the border face. Depth and shape are Judgement (a 22 mm a pixel photograph cannot show them); the two lines are Photo."""
    def cove(d0, h0, h1):
        out = []
        for i in range(8):
            t = i / 7.0
            sm = t * t * (3.0 - 2.0 * t)
            out.append([_r(d0 + 14.0 * t, 2), _r(h0 + (h1 - h0) * sm, 3)])
        return out
    pts = cove(0.0, 0.0, 3.0)
    pts += cove(14.0 + margin, 3.0, 6.0)
    pts.append([_r(28.0 + margin + 20.0, 2), 6.0])
    return pts


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
            ("iron_lock, collar, plug", "kept", "LK1, the rim night latch, as built in 3.1"),
            ("iron_bellpush", "changed", "rebuilt square-cornered (r 1, was r 6), groove added: the plain dark oblong of P1, one part, 22 x 72.6, 3 proud, with the 14 x 2 x 1 groove a little below its middle; 3.1 built it with r 6 corners and no groove (build_door.py line 664); the handover's fix"),
            ("iron_bellpush_bezel, iron_bellpush_button", "removed", "the two-part push read as a modern video doorbell (3.1 review v2 close); deleted, not replaced by any ring or lens"),
            ("stone_threshold, stone_riser, stone_tread", "kept", "the step of 3.1; the wall's plinth returns stay with the wall kit"),
            ("iron_keyhole_*, iron_knob_*", "not present", "T1 never had them"),
        ],
    }

    # ------------------------------------------------------------------ T2 (four stacked lights, leaded fanlight; D3, D1 right door)
    f3 = d3_fractions()
    lh = tl["height_mm"]
    # visible top rail 0.030 of the visible height (58 mm) plus the 20.4 hidden behind the transom's stop = 78.4 structural. Stiles (the review's re-measure on the leaf's own face,
    # row 470, 10.07 mm a pixel): the white beside the glass is 84 mm on the lock (left) side and 58 mm on the hinge (right) side, the glass about 625 wide; the 10 mm planted bead is
    # part of the white, so the visible stiles are 73.6 and 48.6 and the structural stiles (plus the 20.4 behind the stops) 94.0 and 69.0.
    top_rail, bottom_rail, bar = 78.4, 205.0, 30.0
    stile_l, stile_r = 94.0, 69.0
    light_h = (lh - top_rail - bottom_rail - 3 * bar) / 4.0
    lights = []
    v = bottom_rail
    for i in range(4):
        lights.append(opening("light%d" % (i + 1), "light", stile_l, tl["width_mm"] - stile_r, v, v + light_h, glass="plain_3mm", bead="planted_quarter_round_10x8"))
        v += light_h + bar
    K["T2"] = {
        "name": "four stacked lights over a low rail, a fanlight with a plain pane over a band of leaded lozenges (D3, D1)", "frame_set": "T", "family": "cottage front door",
        "leaf": {"w": tl["width_mm"], "h": lh, "t": tl["thickness_mm"], "construction": "framed, glazed", "lock_side": "left",
                 "stile_left": stile_l, "stile_right": stile_r, "top_rail": top_rail, "bottom_rail": bottom_rail, "bar": bar, "light_h": _r(light_h, 2), "openings": lights,
                 "visible_note": "structural numbers; the visible top rail is 58 (78.4 less the 20.4 behind the transom's stop) and the visible stiles 73.6 (lock side, left) and 48.6 (hinge side, right), which with the 10 mm bead are 84 and 59 of white (D3 reads 84 and 58)"},
        "small_fixings": [{"id": "T2_hinge_fixing", "name": "a small dark two-part fitting on the hinge stile (D3)", "u": 753.0, "v": 1390.0, "size_mm": [20.0, 60.0], "proud_mm": 8.0, "srgb": [40, 40, 42],
                           "src": "Photo D3 box [116.5, 492.5, 118.5, 498.5]: its centre 2.2 px (22 mm) beyond the glass edge and 4.2 px (42 mm) in from the leaf's right edge, so u about 753 (+-10) on the white of the hinge stile (733.8 to 792.4), v about 1390 (+-15), about 25 x 60 mm",
                           "what_it_is_not": "not a rim night latch, a bell push, a knocker, a letter plate or a handle (none of those is read on the hinge stile); what it is cannot be told at 10 mm a pixel (a bolt keep or a stop screw): it is added as a small dark box, two parts 20 x 25 mm apart, and no more"}],
        "mouldings": {"outside": {"kind": "none", "note": "glazing bars 30 wide x 22 deep, square, eased 1 mm; stiles and rails square, eased 1.5; the bead is the 3.1 planted quarter-round 10 x 8 on all four sides of each light"}},
        "glass": {"transom": "leaded_diamond", "leaf": "plain_3mm", "nets_behind": "white net card behind the lights (D3 shows one), the windows target's net N1 white"},
        "photographs": ["D3", "D1"],
        "measured_fractions_of_leaf_height": {"top_rail": _r(f3["top_rail"], 4), "bar": _r(f3["bar"], 4), "light": _r(f3["light"], 4), "bottom_rail": _r(f3["bottom_rail"], 4)},
        "parts_vs_3_1": [
            ("frame_jamb_l/r, frame_head, frame_transom, frame_glazing_bead (transom)", "kept", "frame set T"),
            ("glass_fanlight", "changed", "plain 3 mm glass becomes a leaded light as D3 shows it: the upper 144 of the 267 one plain pane; under it a band 83 high of crossed diagonal came at a 145 pitch (lozenges 145 x 83, 5 whole, a tip of a lozenge at each end); a horizontal came 40 above the foot with an upright under each lozenge point; came 6 wide. The T frame's 267 mm light is kept (the wall kit owns the head)"),
            ("leaf_frame", "changed", "stiles 94.0 (lock side, left) and 69.0 (hinge side, right), visible 73.6 and 48.6, with the bead 84 and 59 of white (D3: 84 and 58); top rail 78.4 (visible 58), bottom rail 205, no lock rail, no muntin; four openings 649.8 x 393.7 with 30 mm bars (D3's fractions of the visible face 0.030, 0.2066, 0.0158, 0.105)"),
            ("iron_numerals (new)", "added", "NM6: small dark metal numerals 30 high centred on the visible top rail, v 1898.6 (D3; the number is not on the fanlight glass)"),
            ("small fitting on the hinge stile (new)", "added", "the small dark two-part fitting D3 shows on the hinge stile (T2_hinge_fixing, u 753, v 1390): what it is cannot be told, so it is a small dark box and nothing more"),
            ("panel_*, moulding_bolection_*, moulding_single_*, moulding_band, moulding_weatherboard", "removed", "a glazed door has no panels or mouldings; D3 and D1 show none"),
            ("glass (new parts glass_light1..4) and bead", "added", "four panes of 3 mm glass, each with the 3.1 planted bead"),
            ("iron_letter_plate", "changed", "LP5, a pale low plate in the bottom rail, as D1 and D4 show (the vertical brass plate has no muntin to sit on)"),
            ("iron_lock, collar, plug", "removed", "no latch cylinder is read on D3's leaf; a bar pull stands in (HD3)"),
            ("iron_bellpush", "removed", "none on D3"),
            ("stone_*", "kept", "the step of 3.1 under the same opening"),
        ],
    }

    # ------------------------------------------------------------------ T3 (moulded modern door, small flat-topped light; D4 right door)
    f4 = d4_t3_fractions()
    w3, h3 = tl["width_mm"], tl["height_mm"]
    mm = t3_mm()
    ops3 = [
        opening("upper_panel", "embossed_panel", *mm["upper_outer"], moulding="embossed_step", inner=mm["upper_inner"]),
        opening("small_light", "small_light", *mm["light"], glass="plain_3mm", head="flat", corner_r=20.0, bead="moulded"),
        opening("lower_panel", "embossed_panel", *mm["lower_outer"], moulding="embossed_step", inner=mm["lower_inner"]),
    ]
    K["T3"] = {
        "name": "white moulded modern door with a small flat-topped light (D4 right door)", "frame_set": "T", "family": "modernised cottage",
        "leaf": {"w": w3, "h": h3, "t": 44.0, "construction": "moulded flush sheet over a core, painted-look gloss", "lock_side": "right", "border": 65.0, "openings": ops3},
        "mouldings": {"outside": {"kind": "embossed panel step", "profile_dh": embossed_step_profile(), "note": "each moulded panel has TWO outlines (D4): an outer and an inner outline, a margin of about 70 to 85 between them; the margin is a flat raised border with a 14 mm cove at each line (3 mm down at the outer line to the margin, 3 mm more at the inner line to the field, which is 6 below the border face); the border is 65 wide all round; the upper panel's inner outline has a segmental head (crown v 1646, springing 22 lower) under a flat outer top; no applied mouldings"}},
        "glass": {"transom": "plain_3mm", "leaf": "plain_3mm"},
        "photographs": ["D4"],
        "measured_fractions_of_leaf": {k: v for k, v in f4.items() if k != "scale_mm_px"},
        "parts_vs_3_1": [
            ("frame_jamb_l/r, frame_head, frame_transom, glass_fanlight, frame_glazing_bead", "kept", "frame set T; D4's door has a plain dark transom light over it"),
            ("leaf_frame, panel_*, moulding_*", "changed", "no stiles or rails: one moulded sheet 44 thick with two moulded panels, each with two outlines, and a small flat-topped light (D4, re-measured on the leaf's own face)"),
            ("glass_light (new part)", "added", "one pane 218 x 446 with a flat head (top corners r 20; the head rises at most 22 mm), glazed from inside with a moulded bead; the arch D4 shows is the moulding round it"),
            ("iron_letter_plate", "changed", "LP6, a white oblong 270 x 50 in the margin between the panels (D4: 0.45 of the visible height)"),
            ("iron_lock, collar, plug", "removed", "D4 shows none outside; a small lever HD2c at the lock edge, v 910"),
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
            ("iron_knob_*, iron_keyhole_*, iron_lock_*", "kept", "F1's turned centre knob (HD1), plugged keyhole and knurled rim night latch (LK2) as built"),
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
    # D1: the teal door's panel heads are raked, rising toward the muntin (the left panel's top line runs (47.5, 526.7) to (56.7, 522.9) at 13.2 mm a pixel: a rise of 50 mm, +-25)
    ops_f3 = [opening("long_l", "panel", f_open["bottom_left"]["u0"], f_open["bottom_left"]["u1"], fl["bottom_rail_mm"], 1854.0, moulding="stuck_ovolo", head="raked", head_rise=50.0, rise_toward="right"),
              opening("long_r", "panel", f_open["bottom_right"]["u0"], f_open["bottom_right"]["u1"], fl["bottom_rail_mm"], 1854.0, moulding="stuck_ovolo", head="raked", head_rise=50.0, rise_toward="left")]
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
            ("moulding_bolection_*", "changed", "a stuck ovolo moulding 20 wide, 6.5 proud, replaces the 43 mm bolection (D1 shows thin lit edges); each panel's head is raked, 50 mm lower at the stile than at the muntin (D1)"),
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
    s_v0, s_v1 = F5_V["slit"]
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
            ("glass_slit (new)", "added", "one pane about 210 x 920 (v 870 to 1789) on the leaf's face (D2: 8.8 x 37.5 px at 24.7 mm a pixel, on the leaf's own box, foot at row 360)"),
            ("iron_letter_plate", "changed", "LP7, a pale 265 x 50 plate under the slit, centre v 772"),
            ("iron_knob_*, iron_keyhole_*, iron_lock_*", "removed", "a lever HD2b at the left edge, v 1048"),
        ],
    }

    # ------------------------------------------------------------------ F6 (council-style flush door): the street frame F, an inward-opening 838 leaf
    # D5 is an INDOOR landing door (Commons: "View of hallway and door inside one of Hazlehead I blocks"): its lining, its stops and its leaf's width are not copied. What is
    # taken from it is the flush face and the PLACES of the plate, lever, lock and spyhole as fractions of that face.
    f6 = d5_fractions()
    sp = to_struct("F", f6["spy"]["u"], f6["spy"]["v"])
    spx, spz = (sp[0] + sp[1]) / 2.0, (sp[2] + sp[3]) / 2.0
    K["F6"] = {
        "name": "council-style flush door: a plain flush leaf in the street frame F (fittings placed from D5, an indoor door; the turquoise from D9; a flush face in a white street frame as D4's middle door)",
        "frame_set": "F", "family": "council or modernised",
        "leaf": {"w": W, "h": H, "t": 44.0, "construction": "flush, plywood-faced, lipped", "lock_side": "right", "lipping": 6.0,
                 "openings": [opening("spyhole", "spyhole", spx - 7.0, spx + 7.0, spz - 7.0, spz + 7.0, glass="lens_14")]},
        "mouldings": {"outside": {"kind": "none", "note": "flat face; the lipping line 1 mm; no panel, no moulding"}},
        "glass": {"transom": "reeded_4mm", "leaf": None, "sidelight": "none in the street (D5's reeded sidelight is indoors and is not built)"},
        "photographs": ["D4", "D5", "D9"],
        "measured_fractions_of_leaf": {k: v for k, v in f6.items() if not k.startswith("scale")},
        "parts_vs_3_1": [
            ("frame_*, sill", "kept", "frame set F unchanged: the stops stand in front of the leaf, which laps 20.4 behind each stop and the transom (an inward-opening door, hinges inside); the jambs show 49, the visible face is 797.2 x 1960.6; D5's indoor lining is not copied"),
            ("glass_fanlight", "changed", "reeded 4 mm glass in the transom: Judgement (D5's ribbed light is indoors; no outdoor photograph read shows one)"),
            ("leaf_frame, panel_*, moulding_*", "changed", "one flush slab 838 x 1981 x 44, lipped (a flush leaf in a white street frame: D4's middle door)"),
            ("iron_letter_plate", "changed", "LP4, a chrome-look oblong 250 x 70, flush, by D5's fractions of the visible face"),
            ("iron_knob_*, iron_keyhole_*", "removed", "lever HD2a at the right stile; a spyhole 14 across above the plate (D5, places only)"),
            ("iron_lock_*", "changed", "LK3, a small dark 18 mm lock face under the lever (D5 columns 766 to 771, rows 617 to 626), by D5's fractions of the visible face"),
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
        "mouldings": {"outside": {"kind": "v_joint", "profile": v_joint_profile(), "note": "no applied moulding; a V joint 6 wide and 2 deep between tongued and grooved matchboards (profile (d across, h from the face) in target.json)"}},
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
