"""Thornton's Standard Lounge Coat (International System, 2nd ed., c. 1911, p. 54, Plate 16) as code.

Every ruled point is made by its printed rule (step ids from draft-source.json),
for any measures. Three checks, all automatic:

  check_examples()  the worked values printed in brackets on p. 54, reproduced
                    exactly for the book's own example measures;
  check_rules()     every rule re-measured on the finished points (tools/draft.py);
  check_plate()     the example draft laid over Plate 16 by a least-squares affine
                    fit on the ruled points: each point's distance from where the
                    book drew it, in inches.

What the text leaves to the diagram (the curves, the lapel, the front's rounding,
the fish, the buttons and pocket) is taken from Plate 16 as digitised
(plate16-digitized.json) and carried to other measures by a thin-plate warp fixed
on the ruled points, the way a cutter scales a diagram to a customer.

    python thornton.py            # runs the three checks for the example measures
"""
import json
import math
import os
import sys

import numpy as np
from scipy.interpolate import RBFInterpolator

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from draft import Draft, Measures  # noqa: E402

EXAMPLE = Measures(natural_waist_length=16.5, fashion_length=29, across_back=7.5, elbow_length=20.5,
                   sleeve_length=31, width_shoulder=27, depth_shoulder=28, half_breast=18, half_waist=16,
                   half_seat=19)


def scale_of(m):
    """'Two-thirds of width shoulder gives the scale'; without shoulder measures the
    Normal Model divides the half breast (p. 22)."""
    if m.get("width_shoulder"):
        return m.width_shoulder * 2 / 3
    return m.half_breast


def lounge(m):
    s = scale_of(m)
    d = Draft("lounge", m)
    # ---- framework (F01-F09) -------------------------------------------------
    d.at("A", 0, 0, "F01", "Draw lines A B and A C")
    d.down("D", "A", 0.5, "F02", "D from A, 1/2 inch")
    d.down("E", "D", m.natural_waist_length, "F03", "E from D waist length")
    d.down("B", "D", m.fashion_length, "F04", "B from D, fashion length")
    d.down("2", "E", 9.0, "F05", "2-E, 9 inches")
    d.down("H", "A", s / 2, "F06", "H from A, 1/2 scale measure (9)")
    if m.get("width_shoulder") and m.get("depth_shoulder"):
        d.down("I", "H", (m.depth_shoulder - m.width_shoulder) / 2, "F07", "I from H, half difference between width and depth (1/2)")
    else:
        d.down("I", "H", 0.5, "F08", "In the absence of shoulder measures make I from H a 1/2 inch")
    # ---- back (B01-B19) ------------------------------------------------------
    d.right("F", "E", 1.25, "B01", "F from E, 1 1/4 inches")
    fe = 1.25
    d.right("O", "I", fe / 2, "B02", "O from I, half of F-E")
    d.right("3", "2", fe / 2, "B03", "3-2, half of F-E")
    d.right("G", "A", s / 6 - 0.5, "B05", "G from A, 1/6 scale less 1/2 inch (2 1/2)")
    d.up("K", "I", s / 3, "B06", "K from I, 1/3 scale (6)")
    d.right("L", "K", s / 3 + 1.5, "B07", "L from K, 1/3 scale plus 1 1/2 inches (7 1/2)")
    d.onx("M", "L", "I", "B08", "M is squared down from L")
    d.down("GG", "G", 0.125, "B09", "GG to G, 1/8 inch")
    d.down("N", "L", 2.0, "B11", "L to N, 2 inches")
    w = s / 12
    d._set("W", d.P["M"][0] + w / math.sqrt(2), d.P["M"][1] - w / math.sqrt(2),
           __import__("draft").Rule("W", "B12", "W from M, 1/12 scale (1 1/2), diagonally up and forward (diagram)", "dist", ("M",), w))
    d.beyond("LL", "GG", "L", 0.5, "B13", "LL to L, 1/2 inch (shoulder seam produced)")
    # B14/B15, the first printed pair (5 1/3; as Q to F plus 1), is not in the French or German
    # columns nor on the plate; the second pair is in all three (MANUAL.md section 6). Second used.
    d.right("Q", "F", m.half_waist / 3 + 0.25, "B17", "Q from F, 1/3 waist, plus 1/4 inch (5 5/8)")
    d.right("4", "3", m.half_seat / 3 + 0.25, "B18", "4 from 3, 1/3 seat measure, plus 1/4 inch (6 5/8)")
    # ---- forepart (P01-P26) --------------------------------------------------
    d.right("R", "O", 2 * s / 3, "P01", "R from O, 2/3 scale (12)")
    d.onx("S", "R", "E", "P02", "S is squared down from R")
    d.left("T", "R", 0.5, "P03", "T from R is 1/2 inch")
    d.up("U", "T", s / 12, "P04", "U from T, 1/12 scale (1 1/2)")
    d.right("V", "T", s / 6, "P05", "V from T, 1/6 scale (3)")
    d.onx("C", "V", "A", "P06", "C is squared up from V")
    # 'back shoulder seam' is GG to LL, the seam as finally drawn (LL is L produced 1/2 inch):
    # read so from Plate 16, where C-X is 1/4 inch less than GG-LL, not GG-L (the first reading,
    # GG-L, put X 0.86 in from the plate's X; check_plate found it).
    back_shoulder = float(np.linalg.norm(d.P["LL"] - d.P["GG"]))
    d.along("X", "C", "L", back_shoulder - 0.25, "P08", "X from C, 1/4 inch less than back shoulder seam (GG-LL)")
    d.right("Y", "U", (d.P["T"][1] - d.P["U"][1]) / 2, "P09", "Y from U, one half of T-U (3/4)")
    d.right("Z", "O", m.half_breast, "P11", "Z from O, the breast measure (18)")
    d.down("NN_c", "C", s / 6, "P12", "C to NN, 1/6 scale")
    d.onx("NN", "Z", "NN_c", "P13", "Curve neck C through NN (NN on the line up from Z)")
    # P14: the printed 'half waist' is half the (half) waist measure: 16/2 + 1/4 = 8 1/4, as the
    # bracket and the French (1/2 de ceinture plus 1 cm, 22 1/2 cm of 43) show.
    d.right("SS", "S", m.half_waist / 2 + 0.25, "P14", "SS from S half waist plus 1/4 inch (8 1/4)")
    d.right("J", "Z", 2.25, "P15", "J from Z, 2 1/4 inches")
    d.right("XX", "NN", 1.0, "P16", "NN to XX, 1 inch")
    d.right("JJ", "J", 1.0, "P24", "JJ from J, 1 inch")
    d.right("12", "SS", 1.25, "P25", "12 from SS, 1 1/4 inches")
    # front line points 5 and BB: no rule; the plate puts them on the front line produced
    # from J through SS (diagram) where it meets the hip and bottom lines.
    return d, s


def finish(d, m, plate):
    """The ruled points that depend on curves and on diagram points (TT, QQ, P, 6,
    BB, SSS), after the plate's front line has placed 5 and BB."""
    P = d.P
    # 5 and BB on the front line (plate): measured where the plate's front line from SS
    # meets the hip and bottom lines, carried by the plate's own offsets in scale units.
    s = scale_of(m)
    off5, offBB = plate["front_line_offsets_scale"]
    d.at("5", P["SS"][0] + off5 * s, P["2"][1], "P17", "5 on the front line at the hip line (diagram)")
    d.at("BB", P["SS"][0] + offBB * s, P["B"][1], "P17", "BB on the front line at the bottom line (diagram)")
    fq = P["Q"][0] - P["F"][0]
    d.left("TT", "SS", (m.half_waist + 2.5) - fq, "P18", "Place F-Q at SS and measure out to TT, the waist measure plus 2 1/2 (18 1/2)")
    take = P["TT"][0] - P["Q"][0]
    d.right("QQ", "Q", take / 3, "P19", "Take out from Q to QQ one third of TT-Q")
    s34 = P["4"][0] - P["3"][0]
    d.left("6", "5", (m.half_seat + 3) - s34, "P21", "Place 3-4 at 5 and measure out to 6, the seat plus 3 inches (22)")
    d.down("SSS", "BB", m.half_waist / 12, "P23", "SSS from BB, 1/12 waist")
    return take


# ---- the checks -----------------------------------------------------------------------
PRINTED = {   # p. 54's bracketed worked values: distance of each point from its base, inches
    "G": ("A", 2.5), "H": ("A", 9), "I": ("H", 0.5), "K": ("I", 6), "L": ("K", 7.5), "W": ("M", 1.5),
    "Q": ("F", 5 + 5 / 8), "4": ("3", 6 + 5 / 8), "R": ("O", 12), "U": ("T", 1.5), "V": ("T", 3),
    "Y": ("U", 0.75), "Z": ("O", 18), "SS": ("S", 8.25), "TT_total": (None, 18.5), "6_total": (None, 22),
}


def check_examples(d, take):
    P, out = d.P, []
    for k, (base, val) in PRINTED.items():
        if base is None:
            continue
        got = float(np.linalg.norm(P[k] - P[base]))
        # the book prints its worked values to the tailor's eighth of an inch
        out.append((k, base, val, round(got, 4), abs(got - val) <= 1 / 16 + 1e-9))
    # the two totals the text measures out
    tt = (P["SS"][0] - P["TT"][0]) + (P["Q"][0] - P["F"][0])
    out.append(("TT", "SS-TT plus F-Q", 18.5, round(tt, 4), abs(tt - 18.5) < 1e-6))
    six = (P["5"][0] - P["6"][0]) + (P["4"][0] - P["3"][0])
    out.append(("6", "5-6 plus 3-4", 22.0, round(six, 4), abs(six - 22) < 1e-6))
    return out


def load_plate():
    return json.load(open(os.path.join(HERE, "plate16-digitized.json")))


def affine_fit(src, dst):
    """Least-squares affine map src (n,2) -> dst (n,2)."""
    X = np.c_[src, np.ones(len(src))]
    A, *_ = np.linalg.lstsq(X, dst, rcond=None)
    return A


def apply(A, pts):
    pts = np.asarray(pts, float)
    return np.c_[pts, np.ones(len(pts))] @ A


FIT_POINTS = ["A", "D", "G", "GG", "K", "H", "I", "O", "L", "N", "M", "C", "NN_c", "NN", "XX", "T", "R", "U", "Y",
              "V", "Z", "J", "JJ", "E", "F", "Q", "S", "SS", "12", "2", "3", "4", "B", "W", "X", "LL"]


def check_plate(d, plate):
    """Fit plate px -> draft inches on the ruled points; report residuals in inches."""
    names = [k for k in FIT_POINTS if k in d.P and k in plate["points_px"]]
    src = np.array([plate["points_px"][k] for k in names], float)
    dst = np.array([d.P[k] for k in names])
    A = affine_fit(src, dst)
    res = np.linalg.norm(apply(A, src) - dst, axis=1)
    return A, {k: round(float(r), 3) for k, r in zip(names, res)}


def plate_offsets(d, A, plate):
    """The diagram-only quantities the draft needs, read off the plate in inches
    through the fit and expressed in scale units so they scale with the customer."""
    s = 18.0
    pp = plate["points_px"]
    p5, pBB, pSS = apply(A, [pp["5"], pp["BB"], pp["SS"]])
    return {"front_line_offsets_scale": ((p5[0] - pSS[0]) / s, (pBB[0] - pSS[0]) / s)}


def warp_from_example(ex, cu, names):
    """Thin-plate warp fixed on the ruled points: example inches -> customer inches."""
    src = np.array([ex.P[k] for k in names])
    dst = np.array([cu.P[k] for k in names])
    return RBFInterpolator(src, dst, kernel="thin_plate_spline", smoothing=0.0)


def run_example(verbose=True):
    plate = load_plate()
    d, s = lounge(EXAMPLE)
    # a first fit without 5/BB to read their offsets, then finish and refit
    A, _ = check_plate(d, plate)
    plate.update(plate_offsets(d, A, plate))
    take = finish(d, EXAMPLE, plate)
    ex = check_examples(d, take)
    rules = d.check()
    A, res = check_plate(d, plate)
    if verbose:
        print("scale", s, "| fish/suppression TT-Q =", round(take, 4))
        print("WORKED VALUES (p. 54 brackets):")
        for r in ex:
            print("  %-4s from %-14s printed %7.4f  drafted %7.4f  %s" % (r[0], r[1], r[2], r[3], "ok" if r[4] else "MISMATCH"))
        print("RULES re-measured:", "all hold" if not rules else rules)
        worst = sorted(res.items(), key=lambda kv: -kv[1])
        print("PLATE 16 residuals (in): mean %.3f, worst %s" % (np.mean(list(res.values())), worst[:6]))
    return d, plate, A, ex, rules, res


if __name__ == "__main__":
    run_example()
