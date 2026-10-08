"""Ron's plain 1990 clothes as FLAT PATTERN PIECES a cloth simulator can sew (Marvelous Designer).

Derived from lab test 4's pattern.json (../../4-plain-clothes/target/) plus the amendments A1-A12 in
TARGET.md beside this file. The Thornton trouser draft is rerun through test 4's own functions
(draft_clothes.py) with the amended hem height and hem width; every unchanged jumper number is read
from test 4's pattern.json.

    python draft_md.py        -> writes pattern_md.json beside this file (then run self_check_md.py)

Output frame: centimetres, x right, y UP, every outline counter-clockwise. Each piece lists its edges
as point-index lists in the edge's own direction (start label -> end label); each seam pairs two
edges given in sewing order (index lists that run from the matching start to the matching end).
Mirrored pieces (the second leg, the second sleeve, the second cuff) are written out in full.
"""
import importlib.util
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
T4 = os.path.normpath(os.path.join(HERE, "..", "..", "4-plain-clothes", "target"))
PAT4 = json.load(open(os.path.join(T4, "pattern.json")))
JT4 = PAT4["table"]["jumper_cm"]
LV4 = PAT4["jumper_levels_cm"]
RJ4 = PAT4["jumper_rules"]
IN = 2.54
RON_PARTS = r"F:/LedgerTools/lab/clothes/ron_parts.npz"

# ======================================================================== the amendments (TARGET.md)
A = dict(
    # A1 sleeve ease (finished sleeve girth minus Ron's arm girth, cm)
    ease_biceps=12.0, ease_elbow=10.0, ease_forearm=9.0,
    sleeve_bottom_width=30.0,          # A1/A6: sleeve above the cuff, bloused over the rib (photo 1, 2, 3)
    cuff_blouse_length=2.0,            # A6: extra sleeve length that bunches over the cuff (photo 1, 3)
    # A2 trousers
    trouser_hem_back_z=0.025,          # back of the hem 2.5 cm off the floor, on the boot heel
    trouser_half_foot_in=10.375,       # bottom 20 3/4 + 1/2 in = 21 1/4 in = 54.0 cm round one leg
    pleat1_cm=3.5, pleat2_cm=2.5,      # A3 two forward pleats each side (photo 1)
    pleat_tack_cm=1.5,                 # how far the pleat is caught below the waist seam (sim needs > 0)
    fly_length_cm=20.0,                # A4 fly opening from the waist seam down the front rise
    fly_facing_w=4.5, fly_shield_w=5.0,
    # A5 ribs
    hem_rib_depth=7.0,                 # photo 1 (scaled from the face), test 4 had 6
    hem_rib_ratio=0.80,                # relaxed rib length / body hem edge
    cuff_rib_depth=6.0, cuff_rib_relaxed=19.0,
    neck_rib_depth=2.5, neck_rib_ratio=0.88,
    body_blouse_length=1.5,            # A5: body lengthened so the bloused hem lands where test 4's did
    # A7 shoulder line
    shoulder_drop_cm=6.0,              # the shoulder seam 6 cm past the shoulder point, on the upper arm
    armhole_deeper_cm=2.0,             # a dropped shoulder's armhole is deeper
)

# Ron's arm stations, distance s (m) down the arm axis from the shoulder point (test 4's SH_PT -> SHJ -> elbow -> wrist)
SH_PT = np.array([0.235, 0.015, 1.600]); SHJ = np.array([0.235, 0.017, 1.585])
ELBOW = np.array([0.272, -0.005, 1.215]); WRIST = np.array([0.318, -0.170, 1.035])


def arm_axis_point(s):
    pts = [SH_PT, SHJ, ELBOW, WRIST]
    seg = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(3)]
    acc = 0.0
    for i in range(3):
        if s <= acc + seg[i] or i == 2:
            t = (s - acc) / seg[i]
            return pts[i] + (pts[i + 1] - pts[i]) * t, (pts[i + 1] - pts[i]) / seg[i]
        acc += seg[i]


S_ELBOW = float(np.linalg.norm(SHJ - SH_PT) + np.linalg.norm(ELBOW - SHJ))      # 0.387


def arm_girths():
    """Ron's left-arm girths (tape round the convex hull of the plane section square to the axis), ron_parts.npz."""
    from scipy.spatial import ConvexHull
    d = np.load(RON_PARTS)
    V, F, arm = d["V"], d["F"], d["arm"]
    sel = arm & (V[:, 0] > 0)
    FF = F[sel[F].all(1)]

    def girth(s):
        p0, n = arm_axis_point(s)
        sd = (V - p0) @ n
        P = []
        for a, b in ((0, 1), (1, 2), (2, 0)):
            ia, ib = FF[:, a], FF[:, b]
            m = sd[ia] * sd[ib] < 0
            t = sd[ia][m] / (sd[ia][m] - sd[ib][m])
            P.append(V[ia[m]] + (V[ib[m]] - V[ia[m]]) * t[:, None])
        P = np.vstack(P)
        u = np.cross(n, [0, 0, 1.0]); u /= np.linalg.norm(u); w = np.cross(n, u)
        Q = np.c_[(P - p0) @ u, (P - p0) @ w]
        Q = Q[np.linalg.norm(Q, axis=1) < 0.09]
        return float(ConvexHull(Q).area) * 100            # cm
    ss = np.arange(0.08, 0.30, 0.01)
    bic = max((girth(s), s) for s in ss)
    elb = (girth(S_ELBOW), S_ELBOW)
    fa = max((girth(s), s) for s in np.arange(S_ELBOW + 0.04, S_ELBOW + 0.12, 0.01))
    return dict(biceps=bic, elbow=elb, forearm=fa, wrist=(girth(0.62), 0.62))


# ======================================================================== geometry helpers
def plen(P):
    P = np.asarray(P, float)
    return float(np.linalg.norm(np.diff(P, axis=0), axis=1).sum())


def resample(P, n):
    P = np.asarray(P, float)
    d = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    t = np.linspace(0, d[-1], n)
    return np.stack([np.interp(t, d, P[:, 0]), np.interp(t, d, P[:, 1])], 1)


def piece(name, edges, fabric, grain, cut_note, internal=None, y_down=True):
    """edges: ordered list of (edge name, polyline, start label, end label) walking round the piece.
    Returns the piece dict with a CCW outline (y up) and each edge's indices in its own direction."""
    pts, idx = [], {}
    for en, P, a, b in edges:
        P = np.asarray(P, float)
        i0 = len(pts)
        pts += [tuple(p) for p in P[:-1]]
        idx[en] = (i0, len(P), a, b)
    n = len(pts)
    out = np.array(pts)
    if y_down:
        out[:, 1] *= -1
    eds = {}
    for en, (i0, m, a, b) in idx.items():
        eds[en] = dict(indices=[(i0 + k) % n for k in range(m)], start=a, end=b)
    area = 0.5 * float(np.sum(out[:, 0] * np.roll(out[:, 1], -1) - np.roll(out[:, 0], -1) * out[:, 1]))
    if area < 0:                                        # make it CCW: reverse the order, remap indices
        out = out[::-1].copy()
        for e in eds.values():
            e["indices"] = [n - 1 - i for i in e["indices"]]
    g = np.asarray(grain, float)
    if y_down:
        g[:, 1] *= -1
    il = []
    for nm, P, kind in (internal or []):
        P = np.asarray(P, float).copy()
        if y_down:
            P[:, 1] *= -1
        il.append(dict(name=nm, kind=kind, points=np.round(P, 3).tolist()))
    for e in eds.values():
        e["length_cm"] = round(plen(out[e["indices"]]), 3)
    return dict(name=name, fabric=fabric, cut=cut_note, outline=np.round(out, 3).tolist(),
                grain=np.round(g, 3).tolist(), edges=eds, internal_lines=il, area_cm2=round(abs(area), 1))


def mirror(p, name, cut_note):
    q = json.loads(json.dumps(p))
    out = np.array(q["outline"]); n = len(out)
    out[:, 0] *= -1
    out = out[::-1]
    q["outline"] = np.round(out, 3).tolist()
    for e in q["edges"].values():
        e["indices"] = [n - 1 - i for i in e["indices"]]
    q["grain"] = [[-x, y] for x, y in q["grain"]]
    for il in q["internal_lines"]:
        il["points"] = [[-x, y] for x, y in il["points"]]
    q["name"], q["cut"] = name, cut_note
    return q


FAB_JERSEY = "wool jersey knit: plain machine-knitted stockinette, fine gauge (about 7 stitches/inch), mid-grey"
FAB_RIB = "wool rib knit, 1x1 rib (2x2 acceptable), same yarn; very low weft (crosswise) stretch stiffness so it draws in"
FAB_WORSTED = "wool worsted trousering, plain weave or twill, about 300-340 g/m2, mid or charcoal grey"


# ======================================================================== JUMPER
def jumper(G):
    nx = RJ4[[k for k in RJ4 if k.startswith("J10")][0]] / 2            # 9.0
    drop = LV4["drop"]                                                    # 6.8
    xb = JT4["cross_back"]                                                # 45.61
    hx = JT4["chest_finished"] / 4                                        # quarter chest
    fnd = RJ4[[k for k in RJ4 if k.startswith("J12")][0]]
    bnd = RJ4[[k for k in RJ4 if k.startswith("J11")][0]]
    sp = np.array([xb / 2, drop])                                         # shoulder point on the piece
    u = (sp - np.array([nx, 0])) / np.linalg.norm(sp - np.array([nx, 0]))
    se = sp + u * A["shoulder_drop_cm"]                                   # A7 dropped shoulder end
    y_under = LV4["y_under"] + A["armhole_deeper_cm"]
    blen = JT4["back_length_hps_to_hem"] + A["body_blouse_length"]
    y_bot = blen - A["hem_rib_depth"]
    step = hx - se[0]
    arm = [(se[0] + step * (1 - math.cos(t)), (y_under - 6.0) + 6.0 * math.sin(t)) for t in np.linspace(0, math.pi / 2, 10)]
    arm = [tuple(se)] + arm                                               # straight drop then a quarter curve (6 cm)

    def body(nd, nm, plus_side, minus_side):
        neck = [(nx * math.cos(t), nd * math.sin(t)) for t in np.linspace(0, math.pi, 17)]       # +x neck pt -> centre -> -x
        A_ = [("shoulder_" + plus_side, [(nx, 0.0), tuple(se)], "neck_pt_" + plus_side, "shoulder_end_" + plus_side),
              ("armhole_" + plus_side, arm, "shoulder_end_" + plus_side, "underarm_" + plus_side),
              ("side_" + plus_side, [(hx, y_under), (hx, y_bot)], "underarm_" + plus_side, "bottom_" + plus_side),
              ("bottom", [(hx, y_bot), (-hx, y_bot)], "bottom_" + plus_side, "bottom_" + minus_side),
              ("side_" + minus_side, [(-hx, y_bot), (-hx, y_under)], "bottom_" + minus_side, "underarm_" + minus_side),
              ("armhole_" + minus_side, [(-x, y) for x, y in reversed(arm)], "underarm_" + minus_side, "shoulder_end_" + minus_side),
              ("shoulder_" + minus_side, [(-se[0], se[1]), (-nx, 0.0)], "shoulder_end_" + minus_side, "neck_pt_" + minus_side),
              ("neckline", neck[::-1], "neck_pt_" + minus_side, "neck_pt_" + plus_side)]
        return piece(nm, A_, FAB_JERSEY, [(0, 15), (0, 55)], "1, on the fold of nothing (full width)")

    # front seen from outside: +x is the wearer's LEFT; back seen from outside: +x is the wearer's RIGHT
    front = body(fnd, "jumper_front", "L", "R")
    back = body(bnd, "jumper_back", "R", "L")
    arm_each = plen(arm)
    # ---- sleeve (A1): top width at the underarm, then the stations from Ron's girths
    W0 = G["biceps"][0] + A["ease_biceps"]
    y_el = (S_ELBOW * 100) - A["shoulder_drop_cm"]
    y_fa = G["forearm"][1] * 100 - A["shoulder_drop_cm"]
    W_el, W_fa = G["elbow"][0] + A["ease_elbow"], G["forearm"][0] + A["ease_forearm"]
    sl_len = JT4["sleeve_length_shoulder_to_cuff_edge"] - A["shoulder_drop_cm"]   # cap top to cuff edge
    y_bot_s = sl_len - A["cuff_rib_depth"] + A["cuff_blouse_length"]
    Wb = A["sleeve_bottom_width"]

    def cap(h, n=31):
        ts = np.linspace(-1, 1, n)
        return np.array([(t * W0 / 2, h * (1 - (0.5 + 0.5 * math.cos(math.pi * t)))) for t in ts])
    lo, hi = 0.5, 25.0
    for _ in range(80):
        h = (lo + hi) / 2
        lo, hi = (h, hi) if plen(cap(h)) < 2 * arm_each else (lo, h)
    C = cap(h)
    mid = len(C) // 2
    cap_back = C[:mid + 1][::-1]            # top -> -x underarm
    cap_front = C[mid:]                     # top -> +x underarm
    right = [(W0 / 2, h), (W_el / 2, y_el), (W_fa / 2, y_fa), (Wb / 2, y_bot_s)]
    left = [(-x, y) for x, y in right]
    S_ = [("cap_front", cap_front, "cap_top", "underarm_f"),
          ("underarm_f", right, "underarm_f", "bottom_f"),
          ("bottom", [(Wb / 2, y_bot_s), (-Wb / 2, y_bot_s)], "bottom_f", "bottom_b"),
          ("underarm_b", left[::-1], "bottom_b", "underarm_b"),
          ("cap_back", cap_back[::-1], "underarm_b", "cap_top")]
    crease_none = []
    sleeve_R = piece("jumper_sleeve_R", S_, FAB_JERSEY, [(0, 8), (0, 45)], "2 (mirrored pair); this is the wearer's right", crease_none)
    sleeve_L = mirror(sleeve_R, "jumper_sleeve_L", "2 (mirrored pair); the wearer's left")
    # ---- ribs (A5)
    def band(nm, length, depth, cut, extra_split=None, fab=FAB_RIB):
        xs = [0.0] + (extra_split or []) + [length]
        lower = []
        E = []
        for i in range(len(xs) - 1):
            E.append(("seam_%d" % i, [(xs[i], 0.0), (xs[i + 1], 0.0)], "s%d" % i, "s%d" % (i + 1)))
        E += [("end_b", [(length, 0.0), (length, -depth)], "s%d" % (len(xs) - 1), "top_b"),
              ("free", [(length, -depth), (0.0, -depth)], "top_b", "top_a"),
              ("end_a", [(0.0, -depth), (0.0, 0.0)], "top_a", "s0")]
        return piece(nm, E, fab, [(length / 2, 0), (length / 2, -depth)], cut)
    hem_len = A["hem_rib_ratio"] * 2 * hx
    hem_rib_front = band("hem_rib_front", hem_len, A["hem_rib_depth"], "1 (wales run across the band, i.e. along y)")
    hem_rib_back = band("hem_rib_back", hem_len, A["hem_rib_depth"], "1 (wales along y)")
    cuff_R = band("cuff_R", A["cuff_rib_relaxed"], A["cuff_rib_depth"], "2 (pair); wearer's right")
    cuff_L = band("cuff_L", A["cuff_rib_relaxed"], A["cuff_rib_depth"], "2 (pair); wearer's left")
    nl_f = front["edges"]["neckline"]["length_cm"]; nl_b = back["edges"]["neckline"]["length_cm"]
    r = A["neck_rib_ratio"]
    neck_rib = band("neck_rib", r * (nl_f + nl_b), A["neck_rib_depth"], "1 (single layer, wales along y); its join at the wearer's left neck point",
                    extra_split=[r * nl_f])
    pieces = {p["name"]: p for p in (front, back, sleeve_R, sleeve_L, hem_rib_front, hem_rib_back, cuff_R, cuff_L, neck_rib)}
    nums = dict(W_biceps=W0, W_elbow=W_el, W_forearm=W_fa, W_bottom=Wb, y_elbow=y_el, y_forearm=y_fa, cap_height=h,
                y_underarm_on_body=y_under, body_bottom=y_bot, half_body=hx, shoulder_end=list(se), sleeve_bottom=y_bot_s,
                armhole_each=arm_each, back_length_to_hem_edge=blen, hem_rib_relaxed=2 * hem_len, neckline=nl_f + nl_b)
    return pieces, nums


# ======================================================================== TROUSERS (Thornton, rerun with A2)
def load_t4_draft():
    spec = importlib.util.spec_from_file_location("draft_clothes_t4", os.path.join(T4, "draft_clothes.py"))
    dc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dc)
    return dc


def trousers():
    dc = load_t4_draft()
    dc.HEM_Z = A["trouser_hem_back_z"]                                    # A2 length
    m = dc.ron_trouser_measures()
    m["half_foot"] = A["trouser_half_foot_in"]                            # A2 taper
    d, dispro = dc.trousers(m, stout=True)
    pcs = dc.trouser_pieces(d, m, True)
    P = {k: np.asarray(v, float) * IN for k, v in d.P.items()}
    cm = lambda c: np.asarray(c, float) * IN
    fs, bs = pcs["front"][1], pcs["back"][1]
    fall, inseam_f, hem_f, out_f = cm(fs["fall"]), cm(fs["inseam"]), cm(fs["hem"]), cm(fs["outseam"])
    seat_b, inseam_b, hem_b, out_b, waist_b = cm(bs["seat"]), cm(bs["inseam"]), cm(bs["hem"]), cm(bs["outseam"]), cm(bs["waist"])
    yw = P["Q"][1]; yK = P["K"][1]; yE = P["E"][1]
    # crease (and grain): through the middle of the knee line and of the hem line, produced to the waist
    k_mid = np.array([(P["K"][0] + P["O"][0]) / 2, yK]); h_mid = np.array([(P["L"][0] + P["P"][0]) / 2, P["L"][1]])
    def crease_x(y):
        return k_mid[0] + (h_mid[0] - k_mid[0]) * (y - yK) / (h_mid[1] - yK)
    xc = crease_x(yw)
    xq = P["Q"][0]
    x2 = (xc + xq) / 2
    p1, p2 = A["pleat1_cm"], A["pleat2_cm"]
    t1 = lambda y: float(np.clip((yK - y) / (yK - yw), 0, 1))            # pleat 1 spread, full at the waist, 0 at the knee
    t2 = lambda y: float(np.clip((yE - y) / (yE - yw), 0, 1))            # pleat 2, 0 at the seat line
    def spread(Pts):
        Q = np.asarray(Pts, float).copy()
        for i, (x, y) in enumerate(Q):
            if x < crease_x(y) - 1e-6:
                Q[i, 0] -= p1 * t1(y)
            if x < x2 - 1e-6:
                Q[i, 0] -= p2 * t2(y)
        return Q
    out_f = spread(out_f)
    Qs = out_f[-1]
    Nf = fall[0]
    def wy(x):                                                           # waist line height (straight Q-Nf in Thornton)
        return P["Q"][1] + (Nf[1] - P["Q"][1]) * (x - P["Q"][0]) / (Nf[0] - P["Q"][0])
    tk = A["pleat_tack_cm"]
    T2a = np.array([x2 - p1 - p2, wy(x2)]); T2m = np.array([x2 - p1 - p2 / 2, wy(x2) + tk]); T2b = np.array([x2 - p1, wy(x2)])
    T1a = np.array([xc - p1, wy(xc)]); T1m = np.array([xc - p1 / 2, wy(xc) + tk]); T1b = np.array([xc, wy(xc)])
    # fly: split the fall (front rise) A["fly_length_cm"] below the waist
    dd = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(fall, axis=0), axis=1))])
    fb = A["fly_length_cm"]
    k = int(np.searchsorted(dd, fb))
    Fb = fall[k - 1] + (fall[k] - fall[k - 1]) * (fb - dd[k - 1]) / (dd[k] - dd[k - 1])
    fall_up = np.vstack([fall[:k], Fb]); fall_lo = np.vstack([Fb, fall[k:]])
    E = [("waist_side", [Qs, T2a], "side_top", "p2a"), ("pleat2_out", [T2a, T2m], "p2a", "p2m"), ("pleat2_in", [T2m, T2b], "p2m", "p2b"),
         ("waist_mid", [T2b, T1a], "p2b", "p1a"), ("pleat1_out", [T1a, T1m], "p1a", "p1m"), ("pleat1_in", [T1m, T1b], "p1m", "p1b"),
         ("waist_cf", [T1b, Nf], "p1b", "cf_top"), ("fall_upper", fall_up, "cf_top", "fly_bottom"), ("fall_lower", fall_lo, "fly_bottom", "fork"),
         ("inseam", inseam_f, "fork", "hem_in"), ("hem", hem_f, "hem_in", "hem_out"), ("outseam", out_f, "hem_out", "side_top")]
    crease = [(xc - p1 / 2, wy(xc) + tk), (crease_x(yK), yK), tuple(h_mid)]
    internal = [("crease_front", crease, "fold line, pressed crease (pleat 1 folds into it)"),
                ("pleat2_fold", [(x2 - p1 - p2 / 2, wy(x2) + tk), (x2 - p1 - p2 / 2, wy(x2) + 12)], "fold line, soft pleat, dies out by the hip"),
                ("fly_topstitch", resample(fall_up + np.array([-3.5, 0]), 8), "topstitch line, fly (shown on the left front only)"),
                ("slant_pocket", [(Qs[0] + 3.5, wy(Qs[0] + 3.5)), (Qs[0] + 0.3, wy(Qs[0]) + 17)], "pocket opening line (on-seam slant pocket, photo 1), not cut")]
    grain = [crease[1], crease[2]]
    fr_R = piece("trouser_front_R", E, FAB_WORSTED, grain, "2 (mirrored pair); the wearer's right (carries the fly shield)", internal)
    fr_L = mirror(fr_R, "trouser_front_L", "2 (mirrored pair); the wearer's left (carries the fly facing)")
    # back: Thornton's seat seam, leg, hem, side, waist with its two darts (test 4 A-T8)
    w8, d1a, d1m, d1b, d2a, d2m, d2b, w5 = waist_b
    Eb = [("seat", seat_b, "cb_top", "fork"), ("inseam", inseam_b, "fork", "hem_in"), ("hem", hem_b, "hem_in", "hem_out"),
          ("outseam", out_b, "hem_out", "side_top"), ("waist_side", [w8, d1a], "side_top", "d1a"), ("dart1_out", [d1a, d1m], "d1a", "d1m"),
          ("dart1_in", [d1m, d1b], "d1m", "d1b"), ("waist_mid", [d1b, d2a], "d1b", "d2a"), ("dart2_out", [d2a, d2m], "d2a", "d2m"),
          ("dart2_in", [d2m, d2b], "d2m", "d2b"), ("waist_cb", [d2b, w5], "d2b", "cb_top")]
    bk_mid_k = np.array([(P["3"][0] + P["o"][0]) / 2, P["3"][1]]); bk_mid_h = np.array([(P["4"][0] + P["13"][0]) / 2, P["4"][1]])
    bk_R = piece("trouser_back_R", Eb, FAB_WORSTED, [bk_mid_k, bk_mid_h], "2 (mirrored pair); the wearer's right",
                 [("crease_back", [tuple(bk_mid_h), tuple(bk_mid_k), (bk_mid_k[0], P["2"][1] + 8)], "fold line, pressed back crease, dies out below the seat")])
    bk_L = mirror(bk_R, "trouser_back_L", "2 (mirrored pair); the wearer's left")
    # waistband halves: lower edge in segments matching the front then back waist segments (CF -> CB)
    segF = [plen([T1b, Nf]), plen([T2b, T1a]), plen([Qs, T2a])]
    segB = [plen([w8, d1a]), plen([d1b, d2a]), plen([d2b, w5])]
    depth = m.band * IN
    def wband(nm, ext, cut):
        xs = [0.0]
        for s in segF + segB:
            xs.append(xs[-1] + s)
        names = ["band_cf", "band_fmid", "band_fside", "band_bside", "band_bmid", "band_cb"]
        Eb_ = []
        if ext > 0:
            Eb_.append(("fly_ext_lower", [(-ext, 0.0), (0.0, 0.0)], "ext_end", "b0"))
        for i, nmn in enumerate(names):
            Eb_.append((nmn, [(xs[i], 0.0), (xs[i + 1], 0.0)], "b%d" % i, "b%d" % (i + 1)))
        L = xs[-1]
        Eb_ += [("cb_end", [(L, 0.0), (L, -depth)], "b6", "cb_top"), ("top", [(L, -depth), (-ext, -depth)], "cb_top", "cf_top"),
                ("cf_end", [(-ext, -depth), (-ext, 0.0)], "cf_top", "ext_end" if ext > 0 else "b0")]
        return piece(nm, Eb_, FAB_WORSTED, [(L / 2, 0), (L / 2 + 10, 0)], cut), L
    band_R, LbR = wband("waistband_R", A["fly_shield_w"] - 1.2, "1; wearer's right, with the fly underlap extension (3.8 cm, test 4)")
    band_L, LbL = wband("waistband_L", 0.0, "1; wearer's left, ends at the front edge")
    fl = plen(fall_up)
    def strip(nm, w, cut):
        E_ = [("attach", [(0.0, 0.0), (0.0, -fl)], "top", "bottom"), ("bottom", [(0.0, -fl), (w, -fl + 2.0)], "bottom", "b_out"),
              ("outer", [(w, -fl + 2.0), (w, 0.0)], "b_out", "t_out"), ("top", [(w, 0.0), (0.0, 0.0)], "t_out", "top")]
        return piece(nm, E_, FAB_WORSTED, [(w / 2, -2), (w / 2, -fl + 3)], cut)
    facing = strip("fly_facing_L", A["fly_facing_w"], "1; inside the left front, behind its fly edge")
    shield = strip("fly_shield_R", A["fly_shield_w"], "1 (cut double and bagged in real tailoring; one layer here); behind the right front's fly edge")
    pcs_out = {p["name"]: p for p in (fr_R, fr_L, bk_R, bk_L, band_R, band_L, facing, shield)}
    nums = dict(measures_in=dict(m), disproportion_in=dispro, crease_x_waist=xc, pleat_lines=[xc, x2], fly_length=fl,
                yw=yw, yK=yK, yE=yE, yH=P["H"][1], y_hem=P["L"][1], band_depth=depth, band_len=LbL,
                seat_line_x=[float(P["D"][0]), float(P["E"][0])], points={k: np.round(v, 3).tolist() for k, v in P.items()},
                pleat_spread_at_seat=p1 * t1(yE), knee_line=yK)
    return pcs_out, nums


# ======================================================================== seams
def seam_list(pieces):
    S = []

    def sew(sid, pa, ea, pb, eb, a_from=None, b_from=None, ratio=None, note=""):
        A_ = pieces[pa]["edges"][ea]; B_ = pieces[pb]["edges"][eb]
        ia, ib = list(A_["indices"]), list(B_["indices"])
        if a_from and A_["start"] != a_from:
            ia = ia[::-1]
        if b_from and B_["start"] != b_from:
            ib = ib[::-1]
        la, lb = A_["length_cm"], B_["length_cm"]
        S.append(dict(id=sid, a=dict(piece=pa, edge=ea, indices=ia, length_cm=la), b=dict(piece=pb, edge=eb, indices=ib, length_cm=lb),
                      ease=(dict(kind="ratio", b_over_a=ratio, why=note) if ratio else dict(kind="equal", why=note))))
    # jumper
    for side in ("L", "R"):
        sew("shoulder_" + side, "jumper_front", "shoulder_" + side, "jumper_back", "shoulder_" + side, "neck_pt_" + side, "neck_pt_" + side)
        sew("side_" + side, "jumper_front", "side_" + side, "jumper_back", "side_" + side, "underarm_" + side, "underarm_" + side)
        sl = "jumper_sleeve_" + side
        sew("armhole_front_" + side, sl, "cap_front", "jumper_front", "armhole_" + side, "cap_top", "shoulder_end_" + side)
        sew("armhole_back_" + side, sl, "cap_back", "jumper_back", "armhole_" + side, "cap_top", "shoulder_end_" + side)
        sew("sleeve_underarm_" + side, sl, "underarm_f", sl, "underarm_b", "underarm_f", "underarm_b")
        sew("cuff_" + side, sl, "bottom", "cuff_" + side, "seam_0", "bottom_f", "s0", ratio=round(A["cuff_rib_relaxed"] / A["sleeve_bottom_width"], 4),
            note="rib cuff relaxed 19 cm onto a 30 cm sleeve: the sleeve gathers and bunches over the cuff (A5, A6)")
        sew("cuff_join_" + side, "cuff_" + side, "end_a", "cuff_" + side, "end_b", "top_a", "top_b", note="the cuff's own seam, in line with the sleeve's underarm seam")
    sew("hem_rib_front", "jumper_front", "bottom", "hem_rib_front", "seam_0", "bottom_L", "s0", ratio=A["hem_rib_ratio"],
        note="hem rib 0.80 of the body edge: the body is gathered onto it and blouses over (A5)")
    sew("hem_rib_back", "jumper_back", "bottom", "hem_rib_back", "seam_0", "bottom_R", "s0", ratio=A["hem_rib_ratio"], note="as the front")
    sew("hem_rib_side_L", "hem_rib_front", "end_a", "hem_rib_back", "end_b", "top_a", "top_b", note="rib side seam, wearer's left")
    sew("hem_rib_side_R", "hem_rib_front", "end_b", "hem_rib_back", "end_a", "top_b", "top_a", note="rib side seam, wearer's right")
    sew("neck_rib_front", "jumper_front", "neckline", "neck_rib", "seam_0", "neck_pt_L", "s0", ratio=A["neck_rib_ratio"],
        note="neck rib 0.88 of the neckline: stretched on, it lies flat against the neck (A5)")
    sew("neck_rib_back", "jumper_back", "neckline", "neck_rib", "seam_1", "neck_pt_R", "s1", ratio=A["neck_rib_ratio"], note="as the front")
    sew("neck_rib_join", "neck_rib", "end_a", "neck_rib", "end_b", "top_a", "top_b", note="at the wearer's left neck point")
    # trousers
    for side in ("L", "R"):
        f, b, wb = "trouser_front_" + side, "trouser_back_" + side, "waistband_" + side
        sew("outseam_" + side, f, "outseam", b, "outseam", "hem_out", "hem_out", ratio="eased",
            note="Thornton's side seam: lengths as drafted (pleat spread adds a little to the front); ease the longer side in")
        sew("inseam_" + side, f, "inseam", b, "inseam", "hem_in", "hem_in", ratio="eased",
            note="Thornton's leg seam: the under side is stretched onto the top side between fork and knee, as tailors do")
        sew("pleat1_" + side, f, "pleat1_out", f, "pleat1_in", "p1a", "p1b", note="pleat 1 tack (A3)")
        sew("pleat2_" + side, f, "pleat2_out", f, "pleat2_in", "p2a", "p2b", note="pleat 2 tack (A3)")
        sew("dart1_" + side, b, "dart1_out", b, "dart1_in", "d1a", "d1b", note="back dart (test 4 A-T8)")
        sew("dart2_" + side, b, "dart2_out", b, "dart2_in", "d2a", "d2b", note="back dart (test 4 A-T8)")
        sew("band_cf_" + side, f, "waist_cf", wb, "band_cf", "cf_top", "b0", note="waistband flush with the front (A4)")
        sew("band_fmid_" + side, f, "waist_mid", wb, "band_fmid", "p1a", "b1")
        sew("band_fside_" + side, f, "waist_side", wb, "band_fside", "p2a", "b2")
        sew("band_bside_" + side, b, "waist_side", wb, "band_bside", "side_top", "b3")
        sew("band_bmid_" + side, b, "waist_mid", wb, "band_bmid", "d1b", "b4")
        sew("band_cb_" + side, b, "waist_cb", wb, "band_cb", "d2b", "b5")
    sew("seat_seam", "trouser_back_L", "seat", "trouser_back_R", "seat", "cb_top", "cb_top", note="centre-back seam")
    sew("front_rise", "trouser_front_L", "fall_lower", "trouser_front_R", "fall_lower", "fly_bottom", "fly_bottom", note="front rise below the fly")
    sew("fly_closed", "trouser_front_L", "fall_upper", "trouser_front_R", "fall_upper", "cf_top", "cf_top",
        note="the fly shown closed: the two front edges meet (a cloth simulator cannot do a zip)")
    sew("fly_facing", "trouser_front_L", "fall_upper", "fly_facing_L", "attach", "cf_top", "top", note="facing behind the left fly edge (third layer on that line)")
    sew("fly_shield", "trouser_front_R", "fall_upper", "fly_shield_R", "attach", "cf_top", "top", note="underlap behind the right fly edge (third layer on that line)")
    sew("band_cb_join", "waistband_L", "cb_end", "waistband_R", "cb_end", "b6", "b6", note="waistband centre-back seam")
    for s in S:
        if s["ease"].get("b_over_a") == "eased":
            la, lb = s["a"]["length_cm"], s["b"]["length_cm"]
            s["ease"] = dict(kind="eased", difference_cm=round(lb - la, 3), why=s["ease"]["why"])
    return S


def main():
    G = arm_girths()
    jp, jn = jumper(G)
    tp, tn = trousers()
    pieces = {**jp, **tp}
    seams = seam_list(pieces)
    TT4 = PAT4["table"]["trousers_cm"]
    out = dict(
        units="cm", frame="x right, y up; outlines counter-clockwise; edges as point-index lists in their own direction (start -> end labels); "
                           "seams pair two index lists in sewing order (first points meet)",
        made_by="draft_md.py from ../../4-plain-clothes/target/pattern.json (test 4) plus amendments A1-A12 (TARGET.md)",
        amendments=A,
        ron_arm_girths_cm={k: dict(girth=round(v[0], 1), s_from_shoulder_point_m=round(v[1], 3)) for k, v in G.items()},
        pieces=pieces, seams=seams,
        numbers=dict(jumper={k: (np.round(v, 3).tolist() if isinstance(v, (list, np.ndarray)) else round(float(v), 3)) for k, v in jn.items()},
                     trousers={k: v for k, v in tn.items()}),
        test4_trousers_cm=TT4,
    )
    json.dump(out, open(os.path.join(HERE, "pattern_md.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("pieces", len(pieces), "seams", len(seams))
    print("arm girths", out["ron_arm_girths_cm"])
    print("jumper", out["numbers"]["jumper"])
    return out


if __name__ == "__main__":
    main()
