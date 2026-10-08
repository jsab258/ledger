"""Ron's plain 1990 clothes drafted by written rules: Thornton's trousers (International
System, 2nd ed., c. 1911, p. 286 / Plate 110 and p. 288 / Plate 112) and a plain crew-neck
jumper drafted the same way (proportional rules, every number sourced or marked judgement).

    python draft_clothes.py      -> checks the book's worked values, drafts for Ron,
                                    writes pattern.json beside this file

Rule ids (T.., S.., J.., A..) are the ones TARGET.md cites. Trousers draft in inches (as the
book), y DOWN from the top line G, the construction line F-G at x = 0, the fork (inseam) side
+x, the side seam -x. Everything in pattern.json is in cm, x right, y down.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from draft import Draft, Measures, Rule  # noqa: E402

IN = 2.54

# ---------------------------------------------------------------- Ron's measures
# measurements.json (MH_RoccoP2) and the posed mesh ronfull_down.npz LOD0 (sections by
# convex hull = tape measure; see TARGET.md "Ron's measures").
RON_BODY = dict(
    chest_mm=1231.4, waist_mm=1078.5, waist_z=1.139, hips_mm=1155.8, hips_z=1.019,
    seat_full_mm=1187.0, seat_z=0.95,          # mesh: fullest girth below the waist, z 0.95
    neck_mm=441.5, biceps_mm=441.9, wrist_mm=217.3, shoulder_to_shoulder_mm=446.1,
    shoulder_to_wrist_mm=636.1, crotch_z=0.826,  # mesh: lowest body point on x = 0 between the legs
    neck_point=(0.090, 0.010, 1.668),           # mesh: where the side of the neck meets the shoulder top
    shoulder_point=(0.235, 0.015, 1.600),       # mesh: top contour at the arm's outer edge
    back_neck=(0.0, 0.095, 1.635), front_neck=(0.0, -0.070, 1.620),
    knee_z=0.48, ankle_z=0.10,
)

# ================================================================= TROUSERS (Thornton)
NORMAL = Measures(band=1.75, side=42, leg=31, half_waist=15, half_seat=18, half_knee=9, half_foot=8.5)
STOUT = Measures(band=1.75, side=42, leg=30, half_waist=21, half_seat=21.5, half_knee=10, half_foot=9)


def trousers(m, stout=False, seat_for_disproportion=None):
    """Thornton's Normal Trousers (Dia. 1, p. 286) with the Stout Man's exceptions (Dia. 8, p. 288)."""
    d = Draft("trousers", m)
    seat, bottom, knee = m.half_seat, 2 * m.half_foot, 2 * m.half_knee
    d.at("G", 0, 0, "T01", "Draw lines F, G, C (construction line F-G)")
    d.down("F", "G", m.side, "T03", "G from F, the side length")
    d.up("H", "F", m.leg, "T02", "H from F, the leg length")
    d.down("N", "G", m.band, "T04", "N from G, the band")
    d.down("J", "H", m.leg / 2 - 2, "T05", "J from H, half leg - 2")
    d.up("E", "H", seat / 6, "T06", "E from H, 1/6 seat")
    d.right("K", "J", (knee) / 12, "T07", "K from J, 1/12 total knee")
    d.right("L", "F", bottom / 12, "T08", "L from F, 1/12 bottom")
    d.right("I", "H", seat / 6, "T09", "I from H, 1/6 seat")
    dispro = 0.0
    if stout:
        sd = seat_for_disproportion if seat_for_disproportion is not None else seat
        dispro = m.half_waist - (sd - 3)                       # S01 seat less 3 is normal waist
        d.right("NN", "N", dispro / 4, "S02", "NN from N is 1/4 of disproportion")
        d.left("Q", "NN", m.half_waist / 2, "S03", "Q - NN, 1/2 waist")
        d.left("D", "E", seat / 2 - 0.5, "S04", "D - E, 1/2 seat less 1/2 inch")
        d.up("GG", "G", dispro / 4, "S05", "GG from G same as N to NN, at front")
    else:
        d.left("Q", "N", m.half_waist / 2, "T10", "Q from N, 1/2 waist")
        d.left("D", "E", seat / 2, "T11", "D from E, 1/2 seat")
    d.left("O", "K", m.half_knee - 0.25, "T12", "O from K, 1/2 knee less 1/4 inch")
    d.left("P", "L", m.half_foot - 1, "T13", "P from L, 1/2 bottom less 1 inch")
    mh = seat / 12 + 0.25
    d._set("M", d.P["H"][0] + mh / math.sqrt(2), d.P["H"][1] - mh / math.sqrt(2),
           Rule("M", "T14", "M from H, 1/12 seat plus 1/4 inch (on the 45-degree line, plate)", "dist", ("H",), mh))
    # C: no printed rule; Plates 110/112 put it on G's square line, the side seam Q produced (A-T1)
    q, dd = d.P["Q"], d.P["D"]
    t = (0 - q[1]) / (q[1] - dd[1])
    d.at("C", q[0] + t * (q[0] - dd[0]), 0.0, "A-T1", "C on G's square line, side seam D-Q produced (plate)")
    # ---- under side
    d.right("2", "I", seat / 12, "T15", "2 from I, 1/12 seat")
    d.right("3", "K", 1.5, "T16", "3 from K, always 1 1/2 inch")
    d.right("4", "L", bottom / 12, "T17", "4 from L, 1/12 bottom")
    d.left("5", "N", seat / 8, "T18", "5 from N, 1/8 seat")
    d._set("MM", d.P["M"][0] + 0.25 / math.sqrt(2), d.P["M"][1] - 0.25 / math.sqrt(2),
           Rule("MM", "T19", "MM from M, always 1/4 inch (on H-M produced)", "dist", ("M",), 0.25))
    a, b = d.P["MM"], d.P["5"]
    u = (b - a) / np.linalg.norm(b - a)
    tg = (0 - a[1]) / u[1]                                     # where line MM-5 crosses G's square line
    g_cross = a + u * tg
    p6 = g_cross + u * (seat / 4 - 0.5)
    d._set("6", p6[0], p6[1], Rule("6", "T20", "6 from G line, 1/4 seat - 1/2 (on line MM, 5 produced)", "x", (), seat / 4 - 0.5))
    d.P["g_cross"] = g_cross
    nrm = np.array([u[1], -u[0]])                              # squared off the seat line, toward the fork side (+x)
    if nrm[0] < 0:
        nrm = -nrm
    p7 = p6 + nrm * 1.0
    d._set("7", p7[0], p7[1], Rule("7", "T21", "7 from 6, always 1 inch (squared off the seat line, plate)", "dist", ("6",), 1.0))
    front_w = d.P["Q"][0] - (d.P["NN"][0] if stout else d.P["N"][0])
    # T22 'Measure N to Q and X to 8, the waist measure plus 1 1/2 inch': X read as 5 (the
    # small-waist draft on p. 288 prints '5 to 8'); 8 on N's square line, toward the side seam.
    d.left("8", "5", (m.half_waist + 1.5) - abs(front_w), "T22", "N to Q and 5 to 8, the waist plus 1 1/2 inch")
    d.at("10", *_on_line_at_dist(d.P["E"], d.P["MM"], d.P["5"], seat / 6), step="T23", rule="10 from E, 1/6 seat (on the seat line MM-5, plate)")
    d.beyond("11", "10", "D", seat / 2 + 1.25 - np.linalg.norm(d.P["D"] - d.P["10"]), "T24", "11 from 10, 1/2 seat plus 1 1/4 inch (line 10 through D)")
    d.left("o", "3", (knee + 1) - (d.P["K"][0] - d.P["O"][0]), "T25", "K to O and 3 to o, the knee measure plus 1 inch")
    d.left("13", "4", (bottom + 0.5) - (d.P["L"][0] - d.P["P"][0]), "T26", "L to P and 4 to 13, the bottom measure plus 1/2 inch")
    # 9: no printed rule; plates put it on G's square line, the side seam 11-8 produced (A-T2)
    p8, p11 = d.P["8"], d.P["11"]
    t = (0 - p8[1]) / (p8[1] - p11[1])
    d.at("9", p8[0] + t * (p8[0] - p11[0]), 0.0, "A-T2", "9 on G's square line, side seam 11-8 produced (plate)")
    return d, dispro


def _on_line_at_dist(c, a, b, r):
    """Point on line a-b at distance r from c, the one nearer b."""
    dvec = b - a
    f = a - c
    qa, qb, qc = dvec @ dvec, 2 * f @ dvec, f @ f - r * r
    disc = math.sqrt(qb * qb - 4 * qa * qc)
    ts = [(-qb - disc) / (2 * qa), (-qb + disc) / (2 * qa)]
    p = [a + t * dvec for t in ts]
    return min(p, key=lambda q: np.linalg.norm(q - b))


PRINTED_NORMAL = [  # p. 286, Dia. 1: (point, base, printed value in inches)
    ("H", "F", 31), ("G", "F", 42), ("N", "G", 1.75), ("J", "H", 13.5), ("E", "H", 3), ("K", "J", 1.5),
    ("L", "F", 1.375), ("I", "H", 3), ("Q", "N", 7.5), ("D", "E", 9), ("O", "K", 8.75), ("P", "L", 7.5),
    ("M", "H", 1.75), ("2", "I", 1.5), ("3", "K", 1.5), ("4", "L", 1.375), ("5", "N", 2.25), ("MM", "M", 0.25),
    ("6", "g_cross", 4), ("7", "6", 1), ("10", "E", 3), ("11", "10", 10.25),
]


def check_normal():
    d, _ = trousers(NORMAL)
    out = []
    for k, base, val in PRINTED_NORMAL:
        got = float(np.linalg.norm(d.P[k] - d.P[base]))
        out.append(dict(point=k, base=base, printed=val, drafted=round(got, 4), ok=abs(got - val) <= 1 / 16 + 1e-9))
    tot = [("N-Q + 5-8", 16.5, abs(d.P["Q"][0]) + (d.P["5"][0] - d.P["8"][0])),
           ("K-O + 3-o", 19.0, (d.P["K"][0] - d.P["O"][0]) + (d.P["3"][0] - d.P["o"][0])),
           ("L-P + 4-13", 17.5, (d.P["L"][0] - d.P["P"][0]) + (d.P["4"][0] - d.P["13"][0]))]
    for name, val, got in tot:
        out.append(dict(point=name, base="total", printed=val, drafted=round(float(got), 4), ok=abs(got - val) < 1e-6))
    return d, out


def check_stout():
    """Dia. 8: the text works the disproportion with seat 21 (21 - 3 = 18; 21 - 18 = 3; NN 3/4),
    though its measure line prints seat 21 1/2 (which would give 2 1/2 and 5/8). Reproduced as printed."""
    d, dispro = trousers(STOUT, stout=True, seat_for_disproportion=21.0)
    out = [dict(point="disproportion", printed=3.0, drafted=dispro, ok=abs(dispro - 3) < 1e-9),
           dict(point="NN-N", printed=0.75, drafted=round(float(d.P["NN"][0] - d.P["N"][0]), 4), ok=abs(d.P["NN"][0] - d.P["N"][0] - 0.75) < 1e-9),
           dict(point="Q-NN", printed=10.5, drafted=round(float(d.P["NN"][0] - d.P["Q"][0]), 4), ok=abs(d.P["NN"][0] - d.P["Q"][0] - 10.5) < 1e-9),
           dict(point="D-E", printed=10.25, drafted=round(float(d.P["E"][0] - d.P["D"][0]), 4), ok=abs(d.P["E"][0] - d.P["D"][0] - 10.25) < 1e-9),
           dict(point="GG-G", printed=0.75, drafted=round(float(d.P["G"][1] - d.P["GG"][1]), 4), ok=abs(d.P["G"][1] - d.P["GG"][1] - 0.75) < 1e-9)]
    return d, out


# ---- Ron's trouser measures (inches), each from the body or an adaptation (TARGET.md T-rules)
HEM_Z = 0.040            # A-T5 judgement: hem 4 cm off the floor at the side (on the shoe top), level
FORK_DROP = 0.010        # A-T6 judgement: the fork 1 cm below the body's crotch
SEAT_OVER = 0.5          # Thornton measures the seat 'over the trousers': + 1/2 inch on the body's (A-T4)


def ron_trouser_measures():
    b = RON_BODY
    half_waist = b["waist_mm"] / 25.4 / 2                       # 21.23
    half_seat = (b["seat_full_mm"] / 25.4 + SEAT_OVER) / 2       # 23.62
    leg = (b["crotch_z"] - FORK_DROP - HEM_Z) / 0.0254          # fork to hem
    side_to_hollow = (b["waist_z"] - HEM_Z) / 0.0254 + 0.2       # + the hip's curve on the side (mesh, 5 mm)
    r = lambda v: round(v * 8) / 8                               # the tailor's eighth
    m = Measures(band=1.75, side=r(side_to_hollow + 1.75), leg=r(leg), half_waist=r(half_waist), half_seat=r(half_seat),
                 # A-T3: 1990 straight leg, knee and foot in Thornton's normal proportion to the seat (9/18, 8.5/18)
                 half_knee=r(half_seat * 9 / 18), half_foot=r(half_seat * 8.5 / 18))
    return m


def polyline_len(P):
    P = np.asarray(P)
    return float(np.linalg.norm(np.diff(P, axis=0), axis=1).sum())


def trouser_pieces(d, m, stout):
    """1990 adaptation (A-T7): the trousers are cut at the waist-hollow line (front N/NN-Q, back 5-8);
    the 1 3/4 band above becomes a separate straight waistband; two back darts take the back to
    the band (Thornton's own 'reduce back waist to measure by two V's', p. 288)."""
    P = d.P
    top_front = P["NN"] if stout else P["N"]
    # front (top side): fall line top_front -> M -> I, leg seam I-K-L, hem L-P (hollowed 1 in, T27), side seam P-O-D-Q
    d.P["Nf"] = top_front
    fall = d.curve("fall", ["Nf", "M", "I"], tangents={"Nf": (0, 1), "I": (1, 0.15)}, n=16)
    legseam = d.curve("legseam_f", ["I", "K", "L"], n=20)
    mid = (P["L"] + P["P"]) / 2
    d.P["hem_f_mid"] = mid + np.array([0, -1.0])                 # T27 'At foot, P from O 1 inch': front hem hollowed 1 in
    hem = d.curve("hem_f", ["L", "hem_f_mid", "P"], n=10)
    side = d.curve("side_f", ["P", "O", "D", "Q"], tangents={"Q": (0, -1)}, n=20)
    waist = d.line("waist_f", ["Q", "Nf"])
    front = d.outline(["fall", "legseam_f", "hem_f", "side_f", "waist_f"])
    # back (under side): seat seam 5 -> MM -> 2 (cut at the waist line: the seat seam from 5), leg seam 2-3-4,
    # hem 4-13 (straight), side seam 13-o-11-8, waist 8 -> 5 with two darts
    seat = d.curve("seat_b", ["5", "MM", "2"], tangents={"2": (0.4, 1)}, n=16)
    legb = d.curve("legseam_b", ["2", "3", "4"], n=20)
    hemb = d.line("hem_b", ["4", "13"])
    sideb = d.curve("side_b", ["13", "o", "11", "8"], tangents={"8": (0.2, -1)}, n=20)
    excess = (P["5"][0] - P["8"][0]) - (m.half_waist / 2 + 0.5)  # back waist less (its share of band = half waist/2 + 1/2 ease)
    dart_w, dart_len = excess / 2, 3.5                             # A-T8: two darts, 3 1/2 in long (judgement)
    w8, w5 = P["8"], P["5"]
    wpts = [w8]
    for f in (1 / 3, 2 / 3):
        c = w8 + (w5 - w8) * f
        wpts += [c + np.array([-dart_w / 2, 0]), c + np.array([0, dart_len]), c + np.array([dart_w / 2, 0])]
    wpts.append(w5)
    d.curves["waist_b"] = np.array(wpts)
    back = d.outline(["seat_b", "legseam_b", "hem_b", "side_b", "waist_b"])
    # waistband (A-T7): straight band, length = front + back waist after darts, depth 1 3/4 in, + 1 1/2 in fly extension
    front_w = abs(P["Q"][0] - top_front[0])
    back_w = (P["5"][0] - P["8"][0]) - 2 * dart_w
    band_len = front_w + back_w
    band = np.array([[0, 0], [band_len + 1.5, 0], [band_len + 1.5, m.band], [0, m.band]])
    return dict(front=(front, {"fall": fall, "inseam": legseam, "hem": hem, "outseam": side, "waist": waist}),
                back=(back, {"seat": seat, "inseam": legb, "hem": hemb, "outseam": sideb, "waist": d.curves["waist_b"]}),
                waistband=(band, {"lower_edge": band[:2], "top_edge": band[2:], "fly_extension": band[1:3]}),
                numbers=dict(front_waist=front_w, back_waist=back_w, dart_width=dart_w, dart_length=dart_len, band_half=band_len))


def trouser_table(d, m, pcs):
    P = d.P
    def width_at(curve_a, curve_b, y):
        xa = np.interp(y, *_sorted_xy(curve_a)); xb = np.interp(y, *_sorted_xy(curve_b))
        return abs(xa - xb)
    f, fs = pcs["front"]; b, bs = pcs["back"]
    yH = P["H"][1]
    xo_f = np.interp(yH, *_sorted_xy(fs["outseam"])); xo_b = np.interp(yH, *_sorted_xy(bs["outseam"]))
    thigh = (P["I"][0] - xo_f) + (P["2"][0] - xo_b)              # one leg, front + back at the fork line
    front_top = P["NN"] if "NN" in P else P["N"]
    seat = (P["E"][0] - P["D"][0]) + np.linalg.norm(P["11"] - P["10"])   # half the body
    t = dict(waist_band=2 * pcs["numbers"]["band_half"],
             waist_line_before_darts=2 * ((front_top[0] - P["Q"][0]) + (P["5"][0] - P["8"][0])),
             seat=2 * seat, thigh_at_fork_one_leg=thigh,
             knee_one_leg=(P["K"][0] - P["O"][0]) + (P["3"][0] - P["o"][0]),
             hem_one_leg=(P["L"][0] - P["P"][0]) + (P["4"][0] - P["13"][0]),
             rise_fork_to_waistline=P["H"][1] - P["N"][1], waistband_depth=m.band,
             inseam=polyline_len(fs["inseam"]), outside_leg_waistline_to_hem=polyline_len(fs["outseam"]),
             outside_leg_band_top_to_hem=polyline_len(fs["outseam"]) + m.band,
             front_crotch_seam=polyline_len(fs["fall"]), back_crotch_seam=polyline_len(bs["seat"]))
    return t


def _sorted_xy(c):
    c = np.asarray(c)
    o = np.argsort(c[:, 1])
    return c[o, 1], c[o, 0]


# ================================================================= JUMPER (Thornton's method, knit rules)
CYC = {  # Craft Yarn Council, Man size chart (craftyarncouncil.com/standards/man-size), read 8 Oct 2026, inches
    "XL": dict(chest=(46, 48), back_hip_length=28, armhole_depth=(10, 10.5), cross_back=(18, 18.5), upper_arm=15.5),
    "2X": dict(chest=(50, 52), back_hip_length=29, armhole_depth=(11, 11), cross_back=(19, 20), upper_arm=16.5),
}


def cyc_interp(key, chest_in):
    a, b = CYC["XL"], CYC["2X"]
    ca, cb = np.mean(a["chest"]), np.mean(b["chest"])
    va, vb = np.mean(a[key]), np.mean(b[key])
    return float(va + (vb - va) * (chest_in - ca) / (cb - ca))


def jumper(back_length_cm=None):
    b = RON_BODY
    chest = b["chest_mm"] / 10
    J = {}
    J["J01 ease (4 in, CYC 'standard fit' upper bound; judgement within the source)"] = ease = 4 * IN
    J["J02 finished chest = chest + ease"] = fchest = chest + ease
    J["J03 front width = back width = finished chest / 2"] = half = fchest / 2
    J["J04 back length HPS to hem edge = CYC back hip length interpolated to Ron's chest"] = blen = back_length_cm or cyc_interp("back_hip_length", chest / IN) * IN
    J["J05 hem rib depth (judgement)"] = rib = 6.0
    J["J06 hem rib relaxed width = 0.90 x body width (judgement: ribbing on ~10% fewer stitches)"] = ribw = 0.90 * half
    J["J07 armhole depth, shoulder line to underarm = CYC interpolated"] = ahd = cyc_interp("armhole_depth", chest / IN) * IN
    J["J08 cross back = Ron's shoulder-to-shoulder + 1 cm (judgement: seam just outside the shoulder bone)"] = xb = b["shoulder_to_shoulder_mm"] / 10 + 1.0
    J["J09 shoulder drop = Ron's neck point to shoulder point, vertical (mesh)"] = drop = (b["neck_point"][2] - b["shoulder_point"][2]) * 100
    J["J10 neck width = 2 x Ron's neck point offset from the centre (mesh)"] = nw = 2 * b["neck_point"][0] * 100
    J["J11 back neck depth = neck point to back neck (C7) height (mesh)"] = bnd = (b["neck_point"][2] - b["back_neck"][2]) * 100
    J["J12 front neck depth = neck point to 2 cm below the front neck notch (mesh + judgement 2 cm)"] = fnd = (b["neck_point"][2] - b["front_neck"][2]) * 100 + 2.0
    J["J13 armhole shaping: the width steps in from body to cross back over the lower 1/3 of the armhole (judgement, set-in knit sleeve)"] = 1 / 3
    J["J14 neck rib depth (judgement)"] = nrd = 2.5
    J["J15 neck rib length = 0.85 x neckline seam (judgement: rib hugs)"] = 0.85
    J["J16 sleeve width at underarm = biceps + 3 in (judgement)"] = sw = b["biceps_mm"] / 10 + 3 * IN
    J["J17 sleeve length shoulder point to cuff edge = Ron's shoulder to wrist + 1 cm over the elbow's bend (judgement)"] = sl = b["shoulder_to_wrist_mm"] / 10 + 1.0
    J["J18 cuff rib depth (judgement)"] = crd = 6.0
    J["J19 cuff rib relaxed girth = 22 cm, about Ron's wrist (judgement: grips, stretches over the hand)"] = cuffg = 22.0
    J["J20 sleeve width at the top of the cuff = 26 cm (judgement)"] = swc = 26.0
    J["J21 sleeve cap seam length = armhole seam length (the set-in rule)"] = 1.0
    # ---- back and front (full width, x = 0 at the centre, y down from the neck point line)
    y_hem = blen
    y_rib = blen - rib
    y_under = drop + ahd                                    # underarm below the neck-point line
    y_step = y_under - ahd / 3
    hx, xbx, nx = half / 2, xb / 2, nw / 2

    def body_piece(neck_depth, name):
        right = [(nx, 0.0), (xbx, drop), (xbx, y_step)]
        # armhole curve from the cross-back line down to the underarm (quarter-ellipse)
        arm = [(xbx + (hx - xbx) * (1 - math.cos(t)), y_step + (y_under - y_step) * math.sin(t)) for t in np.linspace(0, math.pi / 2, 9)[1:]]
        right += arm
        right += [(hx, y_rib), (ribw / 2, y_rib + 0.01), (ribw / 2, y_hem)]
        left = [(-x, y) for x, y in reversed(right)]
        neck = [(nx * math.cos(t), neck_depth * math.sin(t)) for t in np.linspace(0, math.pi, 13)]  # from right neck point round to left
        poly = [(ribw / 2, y_hem)] + left[0:0]
        outline = right + [(-x, y) for x, y in reversed(right)]
        # close: right side (neck point -> hem), hem across, left side up, neck back to start
        outline = right + [(-ribw / 2, y_hem)] + [(-x, y) for x, y in reversed(right[:-1])] + neck[::-1][1:-1]
        outline = [(x, y) for x, y in outline]
        seams = dict(shoulder_R=[(nx, 0.0), (xbx, drop)], shoulder_L=[(-nx, 0.0), (-xbx, drop)],
                     armhole_R=[(xbx, drop), (xbx, y_step)] + arm, armhole_L=[(-xbx, drop), (-xbx, y_step)] + [(-x, y) for x, y in arm],
                     side_R=[(hx, y_under), (hx, y_rib), (ribw / 2, y_rib + 0.01), (ribw / 2, y_hem)],
                     side_L=[(-hx, y_under), (-hx, y_rib), (-ribw / 2, y_rib + 0.01), (-ribw / 2, y_hem)],
                     hem=[(ribw / 2, y_hem), (-ribw / 2, y_hem)], hem_rib_top=[(hx, y_rib), (-hx, y_rib)],
                     neckline=[(x, y) for x, y in neck])
        return outline, seams

    back, back_s = body_piece(bnd, "back")
    front, front_s = body_piece(fnd, "front")
    arm_len = polyline_len(back_s["armhole_R"]) + polyline_len(front_s["armhole_R"])
    neck_len = polyline_len(back_s["neckline"]) + polyline_len(front_s["neckline"])
    # ---- sleeve: cap height solved so the cap seam equals the armhole (J21)
    def cap(h, n=25):
        ts = np.linspace(-1, 1, n)
        # a symmetrical bell: x across (-sw/2..sw/2), y down from the cap top
        return np.array([(t * sw / 2, h * (1 - (0.5 + 0.5 * math.cos(math.pi * t)))) for t in ts])
    lo, hi = 2.0, 30.0
    for _ in range(60):
        h = (lo + hi) / 2
        if polyline_len(cap(h)) < arm_len:
            lo = h
        else:
            hi = h
    capc = cap(h)
    under_len = sl - h                                      # underarm level to cuff edge, along the sleeve's centre
    y_cuff_top = h + under_len - crd
    y_cuff = h + under_len
    y_elbow = h + (y_cuff_top - h) * 0.55                    # elbow at 55% of the way to the cuff (body: 39 of 63.6 cm from shoulder ~ judgement)
    sleeve = list(map(tuple, capc[::-1])) if False else None
    right_side = [(sw / 2, h), (swc / 2, y_cuff_top), (cuffg / 2, y_cuff_top + 0.01), (cuffg / 2, y_cuff)]
    sl_outline = [tuple(p) for p in capc] + right_side[1:] + [(-cuffg / 2, y_cuff), (-cuffg / 2, y_cuff_top + 0.01), (-swc / 2, y_cuff_top)]
    sl_seams = dict(cap=[tuple(p) for p in capc], underarm_R=[(sw / 2, h), (swc / 2, y_cuff_top), (cuffg / 2, y_cuff_top + 0.01), (cuffg / 2, y_cuff)],
                    underarm_L=[(-sw / 2, h), (-swc / 2, y_cuff_top), (-cuffg / 2, y_cuff_top + 0.01), (-cuffg / 2, y_cuff)],
                    cuff_edge=[(cuffg / 2, y_cuff), (-cuffg / 2, y_cuff)], cuff_rib_top=[(swc / 2, y_cuff_top), (-swc / 2, y_cuff_top)])
    w_elbow = sw + (swc - sw) * (y_elbow - h) / (y_cuff_top - h)
    rib_len = 0.85 * neck_len
    neck_rib = [(0, 0), (rib_len, 0), (rib_len, nrd), (0, nrd)]
    table = dict(chest_finished=fchest, waist_finished=fchest, hip_hem_rib_relaxed=2 * ribw, body_tube=fchest,
                 back_length_hps_to_hem=blen, armhole_depth=ahd, cross_back=xb, armhole_seam_each=arm_len,
                 neckline_seam=neck_len, neck_rib_length=rib_len, sleeve_cap_height=h, sleeve_length_shoulder_to_cuff_edge=sl,
                 sleeve_underarm_seam=under_len, sleeve_width_biceps=sw, sleeve_width_elbow=w_elbow,
                 sleeve_width_cuff_top=swc, cuff_rib_relaxed=cuffg, elbow_y_on_sleeve=y_elbow)
    return dict(rules=J, back=(back, back_s), front=(front, front_s), sleeve=(sl_outline, sl_seams),
                neck_rib=(neck_rib, {"seam_edge": neck_rib[:2], "fold_edge": neck_rib[2:]}), table=table,
                levels=dict(y_under=y_under, y_rib=y_rib, y_hem=y_hem, drop=drop))


# ================================================================= run
def cm(P):
    return [[round(float(x) * IN, 3), round(float(y) * IN, 3)] for x, y in np.asarray(P)]


def cmr(P):
    return [[round(float(x), 3), round(float(y), 3)] for x, y in np.asarray(P)]


def main(write=True, jumper_back_length=None):
    dn, chk = check_normal()
    ds, chk_s = check_stout()
    m = ron_trouser_measures()
    dispro = m.half_waist - (m.half_seat - 3)
    stout = dispro > 0
    d, _ = trousers(m, stout=stout)
    bad = d.check(tol=1 / 32)
    bad = [b for b in bad if b[1] not in ()]
    pcs = trouser_pieces(d, m, stout)
    tt = trouser_table(d, m, pcs)
    jm = jumper(jumper_back_length)
    out = dict(
        units="cm; x right, y down; trousers one leg (cut two, mirrored); jumper pieces full width",
        source="Thornton, International System of Garment Cutting, 2nd ed. (c. 1911), pp. 286, 288, Plates 110, 112; jumper by the rules in TARGET.md",
        trouser_check_normal=chk, trouser_check_stout=chk_s, trouser_rules_remeasured_failures=[list(map(str, b)) for b in bad],
        trouser_measures_inches=dict(m), trouser_disproportion_in=dispro, trouser_draft="Stout Man's (Dia. 8)" if stout else "Normal (Dia. 1)",
        trouser_points_cm={k: [round(float(v[0]) * IN, 3), round(float(v[1]) * IN, 3)] for k, v in d.P.items()},
        pieces={
            "trouser_front": dict(outline=cm(pcs["front"][0]), seams={k: cm(v) for k, v in pcs["front"][1].items()}),
            "trouser_back": dict(outline=cm(pcs["back"][0]), seams={k: cm(v) for k, v in pcs["back"][1].items()}),
            "trouser_waistband": dict(outline=cm(pcs["waistband"][0]), seams={k: cm(v) for k, v in pcs["waistband"][1].items()}),
            "jumper_back": dict(outline=cmr(jm["back"][0]), seams={k: cmr(v) for k, v in jm["back"][1].items()}),
            "jumper_front": dict(outline=cmr(jm["front"][0]), seams={k: cmr(v) for k, v in jm["front"][1].items()}),
            "jumper_sleeve": dict(outline=cmr(jm["sleeve"][0]), seams={k: cmr(v) for k, v in jm["sleeve"][1].items()}),
            "jumper_neck_rib": dict(outline=cmr(jm["neck_rib"][0]), seams={k: cmr(v) for k, v in jm["neck_rib"][1].items()}),
        },
        table=dict(trousers_cm={k: round(float(v) * IN, 2) for k, v in tt.items()},
                   trouser_darts_in={k: round(float(v), 3) for k, v in pcs["numbers"].items()},
                   jumper_cm={k: round(float(v), 2) for k, v in jm["table"].items()}),
        jumper_rules={k: (round(float(v), 3)) for k, v in jm["rules"].items()},
        jumper_levels_cm={k: round(float(v), 3) for k, v in jm["levels"].items()},
    )
    if write:
        json.dump(out, open(os.path.join(HERE, "pattern.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
    return out, d, pcs, jm


if __name__ == "__main__":
    out, d, pcs, jm = main()
    print("NORMAL (Dia. 1) worked values:", sum(c["ok"] for c in out["trouser_check_normal"]), "of", len(out["trouser_check_normal"]))
    for c in out["trouser_check_normal"]:
        if not c["ok"]:
            print("  MISMATCH", c)
    print("STOUT (Dia. 8) worked values:", [(c["point"], c["printed"], c["drafted"], c["ok"]) for c in out["trouser_check_stout"]])
    print("rules re-measured:", out["trouser_rules_remeasured_failures"] or "all hold")
    print("Ron trouser measures (in):", out["trouser_measures_inches"], "disproportion", round(out["trouser_disproportion_in"], 3), out["trouser_draft"])
    print("trousers cm:", out["table"]["trousers_cm"])
    print("darts:", out["table"]["trouser_darts_in"])
    print("jumper cm:", out["table"]["jumper_cm"])
