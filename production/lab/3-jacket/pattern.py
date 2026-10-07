"""The lounge jacket's pattern pieces for any measures: Thornton's rules for every
ruled point, Plates 16, 46 and 49 for the shapes the text leaves to the diagram.

    python pattern.py ron        -> pattern_ron.json and a sheet on F:
    python pattern.py example    -> the book's own example size

Each diagram curve is carried from the plate to the customer by a thin-plate warp
fixed on that plate's ruled points (plate pixels -> customer inches), so a curve
passes exactly through the ruled points it joins and keeps the plate's shape
between them. Seams are named with the two outline stretches they join.
"""
import json
import math
import os
import sys

import numpy as np
from scipy.interpolate import RBFInterpolator

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import thornton as th  # noqa: E402
from draft import Measures  # noqa: E402

OUT = r"F:/LedgerTools/lab/jacket"
FALL_IN = 1.625     # the collar's fall, plate49 note: a judgement between 1 1/2 and 1 7/8
STAND_IN = 1.25     # 'E from D, the stand, 1 1/4 in.'

# Ron (MH_RoccoP2): body measures from F:/LedgerTools/bodies/MH_RoccoP2/measurements.json and
# the posed mesh (ron_down.npz), turned into Thornton's measures (NOTES.md, "Ron's measures").
RON = Measures(
    natural_waist_length=18.25,   # C7 at about 1.59 m to the waist hollow at 1.139 m, over the back's curve
    fashion_length=31.5,          # the book's 29 for a 16 1/2 waist length, scaled by Ron's 18 1/4 (31.6), rounded
    across_back=8.25,             # half back at blade level on the mesh, 8.2 in, over the coat
    elbow_length=21.5,            # across back + shoulder joint to elbow (12.0 in) + 1 in to the elbow point
    sleeve_length=33.5,           # + elbow to wrist (11.7 in) + 1/4 in below the wrist bone
    half_breast=24.75,            # chest 123.1 cm (48.5 in) + 1 in over shirt and waistcoat, halved
    half_waist=21.75,             # waist 107.9 cm (42.5 in) + 1 in over the waistcoat, halved
    half_seat=23.25,              # hips 115.6 cm (45.5 in) + 1 in over trousers, halved
)


def tps(src, dst):
    return RBFInterpolator(np.asarray(src, float), np.asarray(dst, float), kernel="thin_plate_spline", smoothing=0.0)


def resample(P, step=0.25):
    P = np.asarray(P, float)
    seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    n = max(2, int(math.ceil(s[-1] / step)) + 1)
    t = np.linspace(0, s[-1], n)
    return np.stack([np.interp(t, s, P[:, 0]), np.interp(t, s, P[:, 1])], 1)


def smooth_through(P, n=12):
    """Catmull-Rom through digitised points, for a smooth outline."""
    P = np.asarray(P, float)
    if len(P) < 3:
        return resample(P)
    Q = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P[-1])
    return np.array(out)


def body(m):
    """The back and forepart for measures m: returns (draft, curves in inches, diagram points)."""
    from warp_local import local_affine, map_curve
    plate = th.load_plate()
    ex, _ = th.lounge(th.EXAMPLE)
    A, _ = th.check_plate(ex, plate)
    plate.update(th.plate_offsets(ex, A, plate))
    d, s = th.lounge(m)
    take = th.finish(d, m, plate)
    pp = plate["points_px"]
    names = [k for k in dict.fromkeys(th.FIT_POINTS + ["TT", "QQ", "6", "5", "BB", "SSS"]) if k in d.P and k in pp]
    src = [pp[k] for k in names]
    dst = [d.P[k] for k in names]
    dp = plate["diagram_points_px"]
    D = {}
    for k in ("back_side_top", "fore_side_top", "lapel_point"):
        D[k] = local_affine(src, dst, dp[k])
    # below 6 the forepart's side seam runs on in the direction QQ-6, straightening (on Plate 16 it
    # carries on at 0.45 of that slant) to the bottom, 0.22 in above the back's bottom line
    k_ = s / 18.0
    q6 = d.P["6"] - d.P["QQ"]
    yb = d.P["B"][1] - 0.22 * k_
    D["fore_bottom_side"] = np.array([d.P["6"][0] + q6[0] * (yb - d.P["6"][1]) / q6[1] * 0.45, yb])
    D["front_bottom"] = local_affine(src, dst, plate["curves_px"]["front_edge"][-1])
    D["back_bottom_side"] = np.array([d.P["4"][0], d.P["B"][1]])     # 'Curve line M, Q, and 4 to bottom': straight below 4
    D["back_bottom_seam"] = np.array([d.P["3"][0], d.P["B"][1]])     # the back seam straight below 3 (diagram)
    D["front_shoulder_end"] = d.P["X"] + np.array([0, 0.5])          # 1/2 in below X, written on Plate 16
    D["buttons"] = np.array([local_affine(src, dst, b) for b in dp["buttons"]])
    D["pocket_mouth"] = np.array([local_affine(src, dst, b) for b in dp["pocket_mouth"]])
    anchors = [(pp[k], d.P[k]) for k in names]
    px_of = {"back_side_top": dp["back_side_top"], "fore_side_top": dp["fore_side_top"], "fore_bottom_side": dp["fore_bottom_side"],
             "lapel_point": dp["lapel_point"], "front_bottom": plate["curves_px"]["front_edge"][-1],
             "back_bottom_side": dp["back_bottom_side"], "back_bottom_seam": dp["back_bottom_seam"],
             "front_shoulder_end": dp["front_shoulder_end"]}
    anchors += [(px_of[k], D[k]) for k in px_of]
    C = {}
    for k, v in plate["curves_px"].items():
        if k.startswith("fish") or k == "lapel_edge":
            continue
        C[k] = map_curve(v, anchors)
    # 'X from C, 1/4 inch less than back shoulder seam': applied, as Plate 16 shows it, to the front
    # seam's own length (the plate's front seam, bowed and ending 1/2 in below X, measures 0.28 in less
    # than its back seam). X slides along C-L until the drawn front seam is the back's less 1/4.
    want = float(np.linalg.norm(d.P["LL"] - d.P["GG"])) - 0.25
    cl = (d.P["L"] - d.P["C"]) / np.linalg.norm(d.P["L"] - d.P["C"])
    perp = np.array([-cl[1], cl[0]])
    if perp[1] < 0:
        perp = -perp                                                     # 'below' the line, toward the scye
    lo, hi = want * 0.8, want * 1.05
    for _ in range(40):
        t = (lo + hi) / 2
        end = d.P["C"] + cl * t + perp * 0.5
        a2 = [a for a in anchors if not np.allclose(a[0], dp["front_shoulder_end"])] + [(dp["front_shoulder_end"], end)]
        seam = smooth_through(map_curve(plate["curves_px"]["front_shoulder"], a2))
        Ls = float(np.sum(np.linalg.norm(np.diff(seam, axis=0), axis=1)))
        lo, hi = (t, hi) if Ls < want else (lo, t)
    d.P["X"] = d.P["C"] + cl * t
    D["front_shoulder_end"] = end
    anchors = [a for a in anchors if not np.allclose(a[0], dp["front_shoulder_end"])] + [(dp["front_shoulder_end"], end)]
    for k in ("front_shoulder", "front_scye"):
        C[k] = map_curve(plate["curves_px"][k], anchors)
    # the fish: two-thirds of the suppression, half each side of P on the waist line (p. 54); its
    # top on the scye's bottom and its foot at the pocket mouth, placed from the plate in scale units
    k = s / 18.0
    fish_w = 2 * take / 3
    Px = d.P["T"][0] - 1.0 * k                                          # P about 1 in behind T (plate)
    top = np.array([d.P["T"][0] - 1.4 * k, d.P["T"][1]])               # on the scye bottom, 1.4 in behind T (plate)
    foot = np.array([Px + 0.2 * k, d.P["E"][1] + 4.3 * k])             # at the pocket mouth (plate)
    waist = d.P["E"][1]
    C["fish_left"] = np.array([top, [Px - fish_w / 2 * 0.55, (top[1] + waist) / 2], [Px - fish_w / 2, waist],
                               [Px - fish_w / 2 * 0.5, (waist + foot[1]) / 2], foot])
    C["fish_right"] = np.array([top, [Px + fish_w / 2 * 0.55, (top[1] + waist) / 2], [Px + fish_w / 2, waist],
                                [Px + fish_w / 2 * 0.5, (waist + foot[1]) / 2], foot])
    return d, C, D, take, None


def back_outline(d, C, D):
    P = d.P
    parts = [("back_neck", smooth_through(C["back_neck"])),
             ("back_shoulder", np.array([P["GG"], P["LL"]])),
             ("back_scye", smooth_through(C["back_scye"])),
             ("back_side", smooth_through(C["back_side"])),
             ("back_hem", np.array([C["back_side"][-1], C["back_seam"][-1]])),
             ("back_cb", smooth_through(C["back_seam"])[::-1])]
    return parts


def fore_outline(d, C, D):
    P = d.P
    neck = smooth_through(C["neck"])
    gorge = np.array([P["NN"], P["XX"], D["lapel_point"]])
    lapel = np.array([D["lapel_point"], P["JJ"]])
    front = smooth_through(C["front_edge"])
    bottom = smooth_through(C["fore_bottom"])
    side = smooth_through(C["fore_side"])[::-1]
    scye = smooth_through(C["front_scye"])[::-1]          # from the side top up to the shoulder end
    scye[-1] = D["front_shoulder_end"]  # already the slid end
    # the fish opens on the scye's bottom: cut the scye where it passes nearest the fish's top
    top = (C["fish_left"][0] + C["fish_right"][0]) / 2
    i = int(np.argmin(np.linalg.norm(scye - top, axis=1)))
    fish_l = smooth_through(C["fish_left"])
    fish_r = smooth_through(C["fish_right"])
    gap = np.array([0.15, 0])                                    # the fish's mouth on the scye, 0.3 in open
    shoulder = smooth_through(C["front_shoulder"])
    shoulder[0] = D["front_shoulder_end"]
    parts = [("neck", neck), ("gorge", gorge), ("lapel_edge", lapel), ("front_edge", front), ("fore_hem", bottom),
             ("fore_side", side), ("scye_low", scye[:i + 1]),
             ("fish_a", np.vstack([scye[i] - gap, fish_l[1:]])), ("fish_b", np.vstack([fish_r[::-1][:-1], scye[i] + gap])),
             ("scye_high", scye[i + 1:]), ("front_shoulder", shoulder)]
    return parts


def sleeve(m, d, C):
    """Plate 46's standard sleeve for measures m, A at the origin, the hand to the left (-x), up = -y."""
    s = th.scale_of(m)
    P = d.P
    xn = float(np.linalg.norm(np.array([0.0, P["N"][1]]) - P["N"]))   # X on the back seam level with N, to N
    # scye readings on the body draft: hind-arm pitch N to forearm pitch RR (round the bottom), NN to RR
    scye = np.vstack([smooth_through(C["back_scye"]), smooth_through(C["front_scye"])[::-1][::-1]])
    bs = smooth_through(C["back_scye"])
    iN = int(np.argmin(np.linalg.norm(bs - P["N"], axis=1)))
    fs = smooth_through(C["front_scye"])                               # shoulder end -> side top
    rr = P["T"] + np.array([0.6, -0.4]) * (s / 18.0)                   # forearm pitch: plate, 0.6 in forward of T, 0.4 up
    iR = int(np.argmin(np.linalg.norm(fs - rr, axis=1)))
    def L(a):
        return float(np.sum(np.linalg.norm(np.diff(a, axis=0), axis=1)))
    # N to RR runs OVER THE TOP of the scye (N up to the shoulder, down the front to RR): on the
    # example draft that reads 9.0 in against the book's 'say 9 1/2'; round the bottom it reads 7.4.
    n_rr = L(bs[:iN + 1]) + L(fs[:iR + 1])
    nn = P["N"] + np.array([0, 0.5])
    iNN = int(np.argmin(np.linalg.norm(bs - nn, axis=1)))
    nn_rr = L(bs[iNN:]) + L(fs[iR:][::-1])
    S = {}
    S["A"] = np.array([0.0, 0.0])
    S["C"] = np.array([-((2 * s / 3 - 1) - xn), 0.0])
    S["F"] = np.array([-(m.elbow_length - xn), 0.0])
    S["B"] = np.array([-(m.sleeve_length - xn), 0.0])
    S["D"] = S["C"] + np.array([0, -(s / 2 - 0.5)])
    S["H"] = np.array([S["F"][0], S["D"][1]])
    S["I"] = S["H"] + np.array([1.0, 0])
    S["J"] = S["I"] + np.array([0, 1.0])
    # K on C-D produced beyond D, A-K = the scye reading N-RR
    dy = math.sqrt(max(n_rr ** 2 - S["C"][0] ** 2, 0))
    S["K"] = np.array([S["C"][0], -dy])
    S["E"] = (S["C"] + S["D"]) / 2
    S["L"] = S["E"] + np.array([np.linalg.norm(S["K"] - S["A"]) / 2 + 0.5, 0])
    # BB: on the arc from F through B, 1/3 scale from G (G squared from D toward the hand, above B)
    S["G"] = np.array([S["B"][0], S["D"][1]])
    r = np.linalg.norm(S["B"] - S["F"])
    # the first point up the arc from B that lies 1/3 scale from G (the cuff G-BB at the hand end;
    # the arc meets that distance a second time near the elbow, which is not the cuff)
    S["BB"] = None
    for a in np.linspace(0, math.pi / 2, 4000):
        q = S["F"] + r * np.array([-math.cos(a), -math.sin(a)])
        if np.linalg.norm(q - S["G"]) <= s / 3:
            S["BB"] = q
            break
    pl = json.load(open(os.path.join(HERE, "plate46-49-digitized.json")))
    sp = pl["sleeve_points_px"]
    names = ["A", "C", "F", "B", "D", "K", "E", "L", "H", "I", "J", "G", "BB"]
    from warp_local import local_affine, map_curve
    anchors = [(sp[k], S[k]) for k in names]
    anchors.append((sp["M"], local_affine([sp[k] for k in names], [S[k] for k in names], sp["M"])))
    Cs = {k: map_curve(v, anchors) for k, v in pl["sleeve_curves_px"].items()}
    # M: K to M along the under-sleeve curve = NN-RR + 1/2 (the plate's curve, cut or run on to length)
    ut = smooth_through(Cs["under_top"])
    want = nn_rr + 0.5
    seg = np.linalg.norm(np.diff(ut, axis=0), axis=1)
    cs = np.concatenate([[0], np.cumsum(seg)])
    if want <= cs[-1]:
        j = int(np.searchsorted(cs, want))
        ut = ut[:j + 1]
    S["M"] = ut[-1]
    top = [("forearm_t", smooth_through(Cs["forearm"])[::-1]),           # K -> G? keep G -> K order below
           ("head", smooth_through(Cs["head"])),
           ("hind_t", smooth_through(Cs["hindarm"])),
           ("cuff_t", np.array([S["BB"], S["G"]]))]
    top[0] = ("forearm_t", smooth_through(Cs["forearm"]))               # G -> K
    top = [top[0], top[1], top[2], top[3]]
    # order round the piece: G->K (forearm), K->A (head), A->BB (hind), BB->G (cuff)
    under_hind = smooth_through(np.vstack([[S["M"]], Cs["under_hind"][1:], Cs["hindarm"][5:]]))
    under = [("forearm_u", smooth_through(Cs["forearm"])), ("under_top", ut), ("hind_u", under_hind), ("cuff_u", np.array([S["BB"], S["G"]]))]
    readings = {"X-N": round(xn, 3), "N-RR": round(n_rr, 3), "NN-RR": round(nn_rr, 3), "K-M": round(want, 3)}
    return S, top, under, readings


def collar(m, d, C, D, fore_parts):
    """Plate 49 Dia. 2 for measures m, drafted on the forepart (inches, forepart frame)."""
    P = d.P
    cc = P["C"]
    sh_dir = (cc - D["front_shoulder_end"]) / np.linalg.norm(cc - D["front_shoulder_end"])
    K = {"CC": cc, "A": P["JJ"], "lapel_point": D["lapel_point"]}
    K["C"] = cc + sh_dir * 0.75                                          # 'C from CC, 3/4 in. always'
    u = (K["C"] - K["A"]) / np.linalg.norm(K["C"] - K["A"])            # crease row A -> C -> B
    back_neck = smooth_through(C["back_neck"])
    bn = float(np.sum(np.linalg.norm(np.diff(back_neck, axis=0), axis=1)))
    K["B"] = K["C"] + u * bn                                             # 'B from C, same as A-B on back'
    nrm = np.array([-u[1], u[0]])                                        # square to the crease row
    if nrm @ (D["front_shoulder_end"] - cc) < 0:
        nrm = -nrm                                                       # toward the shoulder side
    K["D"] = K["B"] + nrm * 0.5                                          # 'D from B, 1/2 in.'
    dB = (K["D"] - K["B"]) / np.linalg.norm(K["D"] - K["B"])
    K["E"] = K["D"] + dB * STAND_IN                                      # the stand, on B-D produced
    K["F"] = K["D"] - dB * FALL_IN                                       # the full measure, the other side
    # G: crease row meets the gorge (the forepart's neck line through NN, XX)
    g0, g1 = P["NN"], P["XX"]
    a = np.array([[u[0], -(g1 - g0)[0]], [u[1], -(g1 - g0)[1]]])
    t, _ = np.linalg.solve(a, g0 - K["A"])
    K["G"] = K["A"] + u * t
    pl = json.load(open(os.path.join(HERE, "plate46-49-digitized.json")))
    cp = pl["collar_points_px"]
    names = ["A", "G", "C", "CC", "B", "D", "E", "F", "lapel_point"]
    from warp_local import local_affine, map_curve
    srcc, dstc = [cp[k] for k in names], [K[k] for k in names]
    K["collar_point"] = local_affine(srcc, dstc, cp["collar_point"], k=5)
    K["notch"] = local_affine(srcc, dstc, cp["notch"], k=5)
    anchors = [(cp[k], K[k]) for k in names] + [(cp["collar_point"], K["collar_point"]), (cp["notch"], K["notch"])]
    Cc = {k: map_curve(v, anchors) for k, v in pl["collar_curves_px"].items()}
    neck_edge = smooth_through(Cc["neck_edge"])
    fall = smooth_through(Cc["fall_edge"])
    parts = [("collar_cb", np.array([K["F"], K["E"]])), ("collar_neck", neck_edge),
             ("collar_end", np.array([K["notch"], K["collar_point"]])), ("collar_fall", fall[::-1])]
    crease = smooth_through(np.array([K["D"], K["C"], K["G"]]))
    return K, parts, crease


def closed(parts):
    pts, marks, n = [], {}, 0
    for name, P in parts:
        P = np.asarray(P, float)
        if pts and np.linalg.norm(pts[-1] - P[0]) < 1e-6:
            P = P[1:]
        marks[name] = (n, n + len(P) - 1)
        pts.extend(P)
        n += len(P)
    return np.array(pts), marks


def build(m, tag):
    d, C, D, take, _ = body(m)
    back = back_outline(d, C, D)
    fore = fore_outline(d, C, D)
    S, top, under, readings = sleeve(m, d, C)
    K, col, crease = collar(m, d, C, D, fore)
    out = {"tag": tag, "measures": dict(m), "scale": th.scale_of(m), "suppression_TT_Q": take,
           "sleeve_readings": readings, "points": {k: list(map(float, v)) for k, v in d.P.items()},
           "lapel": {"break": list(map(float, d.P["JJ"])), "crease_far": list(map(float, K["C"])),
                     "lapel_point": list(map(float, D["lapel_point"])), "notch": list(map(float, K["notch"]))},
           "collar_crease": crease.tolist(), "collar_points": {k: list(map(float, v)) for k, v in K.items()},
           "buttons": D["buttons"].tolist(), "pieces": {}}
    for name, parts in (("back", back), ("forepart", fore), ("top_sleeve", top), ("under_sleeve", under), ("collar", col)):
        P, marks = closed(parts)
        out["pieces"][name] = {"outline_in": P.tolist(), "stretches": marks}
    path = os.path.join(HERE, "pattern_%s.json" % tag)
    json.dump(out, open(path, "w"), indent=0)
    return out, path


def sheet(out, path):
    from PIL import Image, ImageDraw
    k = 18  # px per inch
    W, H = 70 * k, 42 * k
    im = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(im)
    offs = {"back": (2, 2), "forepart": (2, 2), "collar": (2, 2), "top_sleeve": (40, 30), "under_sleeve": (40, 30)}
    cols = {"back": (30, 30, 160), "forepart": (160, 30, 30), "collar": (30, 120, 30), "top_sleeve": (120, 60, 0), "under_sleeve": (0, 120, 120)}
    for name, pc in out["pieces"].items():
        ox, oy = offs[name]
        P = np.array(pc["outline_in"])
        if "sleeve" in name:
            P = P + np.array([out["measures"]["sleeve_length"], 6])
        pts = [((x + ox) * k, (y + oy) * k) for x, y in P]
        dr.line(pts + [pts[0]], fill=cols[name], width=2)
    for x, y in [out["lapel"]["break"], out["lapel"]["crease_far"]]:
        dr.ellipse([(x + 2) * k - 4, (y + 2) * k - 4, (x + 2) * k + 4, (y + 2) * k + 4], outline=(0, 0, 0))
    a, b = out["lapel"]["break"], out["lapel"]["crease_far"]
    dr.line([((a[0] + 2) * k, (a[1] + 2) * k), ((b[0] + 2) * k, (b[1] + 2) * k)], fill=(0, 0, 0), width=1)
    im.save(path)
    return path


if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else "ron"
    m = RON if tag == "ron" else th.EXAMPLE
    out, path = build(m, tag)
    print("wrote", path, "| scale", out["scale"], "| suppression", round(out["suppression_TT_Q"], 3), "| sleeve", out["sleeve_readings"])
    for n, pc in out["pieces"].items():
        P = np.array(pc["outline_in"])
        x, y = P[:, 0], P[:, 1]
        area = 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        print("  %-13s %4d pts, %.0f sq in, stretches %s" % (n, len(P), area, list(pc["stretches"])))
    print("sheet", sheet(out, os.path.join(OUT, "pattern_%s.png" % tag)))
