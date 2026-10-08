"""THE OUTLINE RON'S PLAIN CLOTHES SHOULD SHOW, standing, derived from pattern.json and the body
by the numbered rules O1-O14 in TARGET.md. Writes target.json (polygons in metres, body frame:
x lateral (+x his left), y depth (front -y), z up), the seams as 3D polylines, the covered body
regions, and masks/pictures (2 mm per pixel, tools/outline.py Frame) in F:/LedgerTools/lab/clothes/target.

    python target_outline.py
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import ConvexHull
from matplotlib import path as mpath
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from outline import Frame, silhouette  # noqa: E402

BODY = r"F:/LedgerTools/lab/jacket/ronfull_down.npz"
OUT = r"F:/LedgerTools/lab/clothes/target"
T = 0.003                       # O1 cloth thickness / minimum stand-off from the body, 3 mm (judgement)

pat = json.load(open(os.path.join(HERE, "pattern.json")))
JT, TT = pat["table"]["jumper_cm"], pat["table"]["trousers_cm"]
RB = None

d = np.load(BODY)
V, F = d["LOD0_V"].astype(float), d["LOD0_F"].astype(int)
E = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); E.sort(1); E = np.unique(E, axis=0)


def cut(z):
    a, b = V[E[:, 0]], V[E[:, 1]]
    da, db = a[:, 2] - z, b[:, 2] - z
    m = (da * db) < 0
    t = da[m] / (da[m] - db[m])
    return (a[m] + t[:, None] * (b[m] - a[m]))[:, :2]


def hull(P):
    P = np.asarray(P)
    return P[ConvexHull(P).vertices]


def per(P):
    Q = np.vstack([P, P[:1]])
    return float(np.linalg.norm(np.diff(Q, axis=0), axis=1).sum())


CIRC = np.stack([np.cos(np.linspace(0, 2 * np.pi, 24, endpoint=False)), np.sin(np.linspace(0, 2 * np.pi, 24, endpoint=False))], 1)


def offset(P, r):
    """Convex section grown by r all round (perimeter + 2 pi r): O2."""
    return hull((P[:, None, :] + r * CIRC[None]).reshape(-1, 2))


def arm_line(z):
    return 0.215 - 0.1 * (z - 1.0)          # between torso and hanging arm, z < 1.30 (mesh gap, see sections)


def torso(z):
    P = cut(z)
    if z < 0.826:
        return None
    if z < 1.30:
        P = P[np.abs(P[:, 0]) < arm_line(z)]
    else:
        P = P[np.abs(P[:, 0]) < 0.19]       # chest: the torso inside the arms (mesh, z 1.46 loops)
    return hull(P)


def leg(z, side=+1):
    P = cut(z)
    P = P[P[:, 0] * side > 0]
    if z < 0.11:
        P = P[P[:, 1] > -0.075]              # the ankle, not the foot
    return hull(P)


# ---------------------------------------------------------------- levels on Ron
NECK_PT = np.array([0.090, 0.010, 1.668]); SH_PT = np.array([0.235, 0.015, 1.600])
BACK_NECK = np.array([0.0, 0.095, 1.635]); FRONT_NECK_SEAM = np.array([0.0, -0.075, 1.600])
WRIST = np.array([0.318, -0.170, 1.035]); ELBOW = np.array([0.272, -0.005, 1.215]); SHJ = np.array([0.235, 0.017, 1.585])
Z_UNDER = NECK_PT[2] - pat["jumper_levels_cm"]["y_under"] / 100           # O3


def back_profile_hem(length_m):
    """O4: the hem where the back length from the neck point, measured down the back over the
    hollows (cloth bridges them: the convex hull of the centre-back profile), reaches the pattern's."""
    zs = np.arange(1.635, 0.80, -0.005)
    ys = []
    for z in zs:
        P = cut(z); P = P[np.abs(P[:, 0]) < 0.02]
        ys.append(P[:, 1].max() if len(P) else np.nan)
    pts = np.c_[ys, zs]
    pts = pts[~np.isnan(pts[:, 0])]
    run = np.hypot(NECK_PT[2] - BACK_NECK[2], 0.06)   # neck point to C7 over the trapezius
    prev = pts[0]; zmax = prev
    best = prev[0]
    for p in pts[1:]:
        q = np.array([max(p[0], best if p[1] > 1.0 else p[0]), p[1]])
        best = max(best, p[0]) if p[1] > 1.20 else best
        run += float(np.linalg.norm(q - prev)); prev = q
        if run >= length_m:
            return float(p[1])
    return float(pts[-1, 1])


Z_HEM = back_profile_hem(JT["back_length_hps_to_hem"] / 100)
Z_RIB = Z_HEM + 0.06
Z_BAND_LO = 1.139; Z_BAND_HI = Z_BAND_LO + TT["waistband_depth"] / 100       # O9
Z_HEM_T = 0.040; Z_FORK = 0.826 - 0.010
Z_SEATLINE = Z_FORK + pat["trouser_measures_inches"]["half_seat"] / 6 * 0.0254
Z_KNEE = Z_FORK - (pat["trouser_measures_inches"]["leg"] / 2 - 2) * 0.0254
G_BAND, G_SEAT = TT["waist_band"] / 100, TT["seat"] / 100
G_THIGH, G_KNEE, G_HEM = TT["thigh_at_fork_one_leg"] / 100, TT["knee_one_leg"] / 100, TT["hem_one_leg"] / 100

# ---------------------------------------------------------------- trouser sections (O9-O11)
def trouser_torso(z):
    B = torso(z)
    if z >= Z_BAND_LO:
        G = G_BAND
    elif z >= Z_SEATLINE:
        G = G_SEAT + (G_BAND - G_SEAT) * (z - Z_SEATLINE) / (Z_BAND_LO - Z_SEATLINE)
    else:
        G = G_SEAT
    return offset(B, max(T, (G - per(B)) / (2 * np.pi)))


def leg_centre(z, side):
    zs = [0.10, Z_KNEE]
    a, b = leg(0.12, side).mean(0), leg(Z_KNEE, side).mean(0)
    return a + (b - a) * (z - 0.12) / (Z_KNEE - 0.12)


def trouser_leg(z, side):
    if z > Z_KNEE:
        B = leg(min(z, 0.82), side)
        G = G_KNEE + (G_THIGH - G_KNEE) * (z - Z_KNEE) / (Z_FORK - Z_KNEE)
        return offset(B, max(T, (G - per(B)) / (2 * np.pi)))
    G = G_HEM + (G_KNEE - G_HEM) * (z - Z_HEM_T) / (Z_KNEE - Z_HEM_T)
    c = leg_centre(z, side)
    circ = c + CIRC * G / (2 * np.pi)
    if z > 0.12:
        circ = hull(np.vstack([circ, offset(leg(z, side), T)]))
    return circ


# ---------------------------------------------------------------- jumper sections (O2-O7)
G_CHEST = JT["chest_finished"] / 100
CHEST = torso(1.45)
D_CHEST = (G_CHEST - per(CHEST)) / (2 * np.pi)
CHEST_G = offset(CHEST, D_CHEST)


def jumper_body(z):
    under = trouser_torso(z) if z <= Z_BAND_HI else torso(z)     # O7 worn over the trousers
    if z < Z_RIB:                                                  # O6 the rib grips
        G = JT["hip_hem_rib_relaxed"] / 100
        return offset(under, max(T, (G - per(under)) / (2 * np.pi)))
    fall = hull(np.vstack([CHEST_G, offset(under, T)]))           # O5 falls straight from the chest
    if z < Z_RIB + 0.04:                                           # blouse over the rib, 4 cm (judgement)
        rib = jumper_body(Z_RIB - 1e-4)
        f = (z - Z_RIB) / 0.04
        cx = lambda P: np.array([P[:, 0].min(), P[:, 0].max(), P[:, 1].min(), P[:, 1].max()])
        return ("blend", cx(rib) * (1 - f) + cx(fall) * f)
    return fall


def ext(S):
    if isinstance(S, tuple):
        return S[1]
    return np.array([S[:, 0].min(), S[:, 0].max(), S[:, 1].min(), S[:, 1].max()])


def yoke_ext(z):
    """O3 above the underarm the jumper is the whole upper body (torso and the arm's root) grown by the chest ease."""
    P = cut(z)
    P = P[(np.abs(P[:, 0]) < 0.30) & (np.abs(P[:, 1]) < 0.20)]
    H = offset(hull(P), D_CHEST)
    e = ext(H)
    if z < 1.45:                                   # O5 still falls from the chest below the chest line
        e2 = ext(hull(np.vstack([CHEST_G, offset(hull(P), T)])))
        e[2], e[3] = e2[2], e2[3]
    return e


# ---------------------------------------------------------------- sleeves (O8)
def sleeve_axis():
    """The arm's axis: shoulder point, elbow, wrist (mesh), sampled by arc length from the shoulder point."""
    pts = np.array([SH_PT, SHJ, ELBOW, WRIST])
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    S = np.linspace(0, s[-1], 60)
    A = np.stack([np.interp(S, s, pts[:, k]) for k in range(3)], 1)
    return S, A


def sleeve_radius(s):
    """Width W from the pattern at each distance s down the sleeve from the shoulder point; r = W / 2 pi (O8)."""
    h = JT["sleeve_cap_height"] / 100
    L = JT["sleeve_length_shoulder_to_cuff_edge"] / 100
    ye, yct = JT["elbow_y_on_sleeve"] / 100, L - 0.06
    W = np.interp(s, [0, h, ye, yct, yct + 1e-4, L], [JT["sleeve_width_biceps"], JT["sleeve_width_biceps"], JT["sleeve_width_elbow"],
                                                      JT["sleeve_width_cuff_top"], JT["cuff_rib_relaxed"], JT["cuff_rib_relaxed"]]) / 100
    return W / (2 * np.pi)


ARM_S = [0.0, 0.19, 0.37, 0.60, 0.636]          # distance down the arm from the shoulder point, m
ARM_AX = [0.050, 0.044, 0.048, 0.037, 0.0346]   # arm half-width seen from the front (mesh sections; forearm round)
ARM_AY = [0.085, 0.080, 0.048, 0.037, 0.0346]   # arm half-depth seen from the side


def ellipse_per(a, b):
    return np.pi * (3 * (a + b) - np.sqrt((3 * a + b) * (a + 3 * b)))


def sleeve_half_widths(s):
    """O8: the sleeve is the arm's own section grown by d = (pattern width - arm girth) / 2 pi,
    never less than 3 mm; returns (front-view half-width, side-view half-depth)."""
    ax, ay = np.interp(s, ARM_S, ARM_AX), np.interp(s, ARM_S, ARM_AY)
    W = sleeve_radius(s) * 2 * np.pi
    dd = np.maximum(T, (W - ellipse_per(ax, ay)) / (2 * np.pi))
    return ax + dd, ay + dd


def axis_param(P3, A, S):
    """Arc length s of the nearest point on the axis polyline A(S) for each 3D point."""
    best_d, best_s = np.full(len(P3), np.inf), np.zeros(len(P3))
    for i in range(len(A) - 1):
        a, b = A[i], A[i + 1]
        ab = b - a; L2 = ab @ ab
        t = np.clip((P3 - a) @ ab / L2, 0, 1)
        q = a + t[:, None] * ab
        dd = np.linalg.norm(P3 - q, axis=1)
        m = dd < best_d
        best_d[m], best_s[m] = dd[m], S[i] + t[m] * (S[i + 1] - S[i])
    return best_s


def arm_cover_points(sgn):
    """The jumper-covered vertices of one arm (C1): below z 1.30 outside the torso line, above it |x| > 0.19,
    up to the yoke; the hand (beyond the wrist plane) is already out of the covered list."""
    cv = cover()["jumper"]
    P = V[cv]
    z = P[:, 2]
    arm = np.where(z < 1.30, sgn * P[:, 0] > arm_line(z), sgn * P[:, 0] > 0.19) & (z < SH_PT[2] + 0.02)
    return P[arm]


def union_outline(polys, u0, v0, w, h, res=0.001):
    """One outer polygon round the union of polygons, traced on a 1 mm grid (matplotlib contour)."""
    W, H = int(w / res), int(h / res)
    img = Image.new("1", (W, H), 0); dr = ImageDraw.Draw(img)
    for P in polys:
        dr.polygon([((p[0] - u0) / res, (p[1] - v0) / res) for p in P], fill=1, outline=1)
    m = np.array(img, dtype=float)
    m = np.pad(m, 1)
    fig = plt.figure()
    cs = plt.contour(np.arange(-1, W + 1) * res + u0, np.arange(-1, H + 1) * res + v0, m, levels=[0.5])
    segs = cs.allsegs[0]
    plt.close(fig)
    return max(segs, key=len)


def arm_sections(sgn, S, As):
    """C5: Ron's arm cut square to its axis at each station: the cut points (3D) and the girth (convex hull
    perimeter in the cutting plane), keeping only that arm's side (as arm_cover_points) and points within
    10 cm of the axis, and nothing beyond the wrist plane."""
    tw = (WRIST - ELBOW) / np.linalg.norm(WRIST - ELBOW) * np.array([sgn, 1, 1])
    Wp = WRIST * np.array([sgn, 1, 1])
    a, b = V[E[:, 0]], V[E[:, 1]]
    out_pts, girth = [], np.full(len(S), np.nan)
    tg = np.gradient(As, axis=0); tg /= np.linalg.norm(tg, axis=1)[:, None]
    for i in range(len(S)):
        n = tg[i]
        da, db = (a - As[i]) @ n, (b - As[i]) @ n
        m = (da * db) < 0
        t = da[m] / (da[m] - db[m])
        P = a[m] + t[:, None] * (b[m] - a[m])
        z = P[:, 2]
        keep = (np.linalg.norm(P - As[i], axis=1) < 0.10) & np.where(z < 1.30, sgn * P[:, 0] > arm_line(z), sgn * P[:, 0] > 0.19)
        keep &= ((P - Wp) @ tw) <= 1e-4
        P = P[keep]
        out_pts.append(P)
        if len(P) >= 6:
            u = np.cross(n, [0, 0, 1.0]); u /= np.linalg.norm(u); w = np.cross(n, u)
            try:
                girth[i] = per(hull(np.c_[(P - As[i]) @ u, (P - As[i]) @ w]))
            except Exception:
                pass
    return out_pts, girth


def sleeve_outline(view_axes, sides):
    """C1/C4/O8: the sleeve from the shoulder point to the cuff, one side at a time in each view.
    At each station s along the arm's axis the sleeve edge stands off the arm's own covered points
    (C5: the arm cut square to its axis at s, its furthest reach on that side) by an ease e(s):
      cap (s < cap height h, C4): e = 3 mm + (e_h - 3 mm) * sin(pi/2 * s/h), a quarter-sine from the
        shoulder point to the biceps line, so the cap's girth grows smoothly to the biceps width (J21);
      below the cap: e = max(3 mm, (pattern width - Ron's arm girth at s) / 2 pi) (O8, C5).
    Then joined with the arm's covered points grown by 3 mm, chunk by chunk (C1), so it is never inside
    the arm + 3 mm (O1); the cuff end is the wrist plane that also ends the covered list (O13)."""
    S, A = sleeve_axis()
    h = JT["sleeve_cap_height"] / 100
    W = sleeve_radius(S) * 2 * np.pi                                  # pattern width at each station
    polys = []
    for sgn in sides:
        As = A * np.array([sgn, 1, 1])
        secs, girth = arm_sections(sgn, S, As)                       # C5: Ron's own arm girth, square to the axis
        ease = np.maximum(T, (W - girth) / (2 * np.pi))               # O8 / O2
        ok = ~np.isnan(ease)
        ease = np.interp(S, S[ok], ease[ok])
        e_h = float(np.interp(h, S, ease))
        e = np.where(S < h, T + (e_h - T) * np.sin(np.pi / 2 * np.clip(S / h, 0, 1)), ease)   # C4 cap
        P = arm_cover_points(sgn)
        sp = axis_param(P, As, S)
        P2 = As[:, list(view_axes)]
        t2 = np.gradient(P2, axis=0); t2 /= np.linalg.norm(t2, axis=1)[:, None] + 1e-12
        n2 = np.stack([-t2[:, 1], t2[:, 0]], 1)
        Q = P[:, list(view_axes)]
        plus, minus = np.full(len(S), np.nan), np.full(len(S), np.nan)
        for i in range(len(S)):
            C = secs[i]
            if len(C) < 3:                                           # no clean cut (the cap): the covered points near s
                m = np.abs(sp - S[i]) < 0.0075
                if m.sum() < 3:
                    continue
                C = P[m]
            q = (C[:, list(view_axes)] - P2[i]) @ n2[i]
            plus[i], minus[i] = max(q.max(), 0.0), max(-q.min(), 0.0)
        ok = ~np.isnan(plus)
        plus = np.interp(S, S[ok], plus[ok]) + e
        minus = np.interp(S, S[ok], minus[ok]) + e
        polys.append(np.vstack([P2 + n2 * plus[:, None], (P2 - n2 * minus[:, None])[::-1]]))
        for s0 in np.arange(-0.015, S[-1] + 0.015, 0.0075):                # C1 safety: arm + 3 mm, 1.5 cm chunks
            m = (sp >= s0) & (sp < s0 + 0.015)
            if m.sum() >= 3:
                try:
                    polys.append(offset(hull(Q[m]), T))
                except Exception:
                    pass
    Pall = np.vstack(polys)
    u0, v0 = Pall[:, 0].min() - 0.01, Pall[:, 1].min() - 0.01
    return union_outline(polys, u0, v0, Pall[:, 0].max() - u0 + 0.01, Pall[:, 1].max() - v0 + 0.01)


def band_polygon(P2, r):
    """A tube of radius r(s) about a 2D projected axis: the axis offset +-r (orthographic projection of a round tube)."""
    t = np.gradient(P2, axis=0); t /= np.linalg.norm(t, axis=1)[:, None] + 1e-12
    n = np.stack([-t[:, 1], t[:, 0]], 1)
    return np.vstack([P2 + n * r[:, None], (P2 - n * r[:, None])[::-1]])


# ---------------------------------------------------------------- build the views
def zs(a, b, step=0.005):
    return np.arange(a, b + 1e-9, step)


def neck_ring(n=41):
    """The neckline seam (J10-J12 on Ron): neck points at the sides, back neck and front seam at the centre."""
    th = np.linspace(0, 2 * np.pi, n)
    return np.array([[NECK_PT[0] * math.sin(a), (BACK_NECK[1] + FRONT_NECK_SEAM[1]) / 2 + (BACK_NECK[1] - FRONT_NECK_SEAM[1]) / 2 * math.cos(a),
                      NECK_PT[2] - (NECK_PT[2] - (BACK_NECK[2] if math.cos(a) > 0 else FRONT_NECK_SEAM[2])) * abs(math.cos(a)) ** 1.5] for a in th])


def jumper_views():
    zb = zs(Z_HEM, Z_UNDER)
    X = np.array([ext(jumper_body(z)) for z in zb])
    zy = zs(Z_UNDER, SH_PT[2])
    Y = np.array([yoke_ext(z) for z in zy])
    # C7: the neck region from what the rules build: the yoke up to the neckline seam (O3, the ease tapering
    # to 3 mm at the seam over the last 8 cm, judgement), and the rib as a band 2.5 cm tall standing on the
    # seam (J14), both projected into each view and joined with the body by a 1 mm union.
    rib = pat["jumper_rules"].get("J14 neck rib depth (judgement)", 2.5) / 100
    right = [(x[1], z) for x, z in zip(X, zb)] + [(y[1], z) for y, z in zip(Y, zy)]
    front = right + [(-x, z) for x, z in reversed(right)]
    yb = [(x[2], z) for x, z in zip(X, zb)] + [(y[2], z) for y, z in zip(Y, zy)]
    yk = [(x[3], z) for x, z in zip(X, zb)] + [(y[3], z) for y, z in zip(Y, zy)]
    side_body = yb + list(reversed(yk))
    ring3 = neck_ring(181)
    cv = cover()["jumper"]
    Pn = V[cv]; Pn = Pn[Pn[:, 2] > SH_PT[2] - 0.06]
    dn = np.min(np.linalg.norm(Pn[:, None, :] - ring3[None, ::4, :], axis=2), axis=1)
    en = T + (D_CHEST - T) * np.clip(dn / 0.08, 0, 1)
    def neck_polys(ax):
        out = []
        for i in range(len(ring3) - 1):                                   # the rib band, quad by quad
            a, b = ring3[i], ring3[i + 1]
            q = np.array([a, b, b + [0, 0, rib], a + [0, 0, rib]])[:, list(ax)]
            if np.ptp(q[:, 0]) > 1e-6 or np.ptp(q[:, 1]) > 1e-6:
                out.append(q)
        Q = Pn[:, list(ax)]
        for u0 in np.arange(Q[:, 0].min() - 0.01, Q[:, 0].max() + 0.01, 0.005):   # the yoke top, 1 cm chunks
            m = (Q[:, 0] >= u0) & (Q[:, 0] < u0 + 0.01)
            if m.sum() >= 3:
                C = (Q[m][:, None, :] + en[m][:, None, None] * CIRC[None]).reshape(-1, 2)
                out.append(hull(C))
        return out
    def joined(base, ax):
        polys = [np.asarray(base)] + neck_polys(ax)
        Pall = np.vstack(polys)
        u0, v0 = Pall[:, 0].min() - 0.01, Pall[:, 1].min() - 0.01
        return union_outline(polys, u0, v0, Pall[:, 0].max() - u0 + 0.01, Pall[:, 1].max() - v0 + 0.01)
    front = joined(front, (0, 2))
    side_body = joined(side_body, (1, 2))
    # sleeves
    S, A = sleeve_axis()
    r = sleeve_radius(S)
    k = S >= JT["sleeve_cap_height"] / 100 - 0.02
    sl_front_L = sleeve_outline((0, 2), (+1,))
    sl_front_R = sleeve_outline((0, 2), (-1,))
    sl_side = sleeve_outline((1, 2), (+1, -1))
    return dict(front=[np.array(front), sl_front_L, sl_front_R], side=[np.array(side_body), sl_side], X=X, zb=zb, S=S, A=A, r=r)


def leg_ext(z, side):
    """O10: below the knee line the leg is its pattern girth as a round tube (O11); from the knee line
    up to the seat line each edge runs straight (the cloth hangs from the hip and seat): outer edge to
    the seat-line garment's side, inner edge to the fork at x = 0, front to the seat-line front, back to
    the fullest seat's back. Never inside the body + 3 mm."""
    if z <= Z_KNEE:
        return ext(trouser_leg(z, side))
    k = ext(trouser_leg(Z_KNEE, side))
    top = ext(trouser_torso(Z_SEATLINE))
    back = max(ext(trouser_torso(zz))[3] for zz in (Z_SEATLINE, 0.94, 0.96))
    if side > 0:
        tx_out, tx_in = top[1], 0.0
        f_out = (z - Z_KNEE) / (Z_SEATLINE - Z_KNEE); f_in = min(1.0, (z - Z_KNEE) / (Z_FORK - Z_KNEE))
        xmin, xmax = k[0] + (tx_in - k[0]) * f_in, k[1] + (tx_out - k[1]) * f_out
    else:
        tx_out, tx_in = top[0], 0.0
        f_out = (z - Z_KNEE) / (Z_SEATLINE - Z_KNEE); f_in = min(1.0, (z - Z_KNEE) / (Z_FORK - Z_KNEE))
        xmin, xmax = k[0] + (tx_out - k[0]) * f_out, k[1] + (tx_in - k[1]) * f_in
    ymin = k[2] + (top[2] - k[2]) * f_out
    ymax = k[3] + (back - k[3]) * f_out
    if z < 0.826:
        b = ext(offset(leg(z, side), T))
        xmin, xmax, ymin, ymax = min(xmin, b[0]), max(xmax, b[1]), min(ymin, b[2]), max(ymax, b[3])
    return np.array([xmin, xmax, ymin, ymax])


def trouser_views():
    zl = zs(Z_HEM_T, Z_FORK)
    LR = np.array([leg_ext(z, +1) for z in zl])
    LL = np.array([leg_ext(z, -1) for z in zl])
    zt = np.append(zs(Z_FORK, Z_BAND_HI)[:-1], Z_BAND_HI)     # C3: top edge exactly at the band top
    TO = []
    for z in zt:
        t = ext(trouser_torso(max(z, 0.83)))
        if z < Z_SEATLINE:
            a, b = leg_ext(z, +1), leg_ext(z, -1)
            t = np.array([min(t[0], b[0]), max(t[1], a[1]), min(t[2], a[2], b[2]), max(t[3], a[3], b[3])])
        TO.append(t)
    TO = np.array(TO)
    outer_R = [(x[1], z) for x, z in zip(LR, zl)] + [(t[1], z) for t, z in zip(TO, zt)]
    outer_L = [(x[0], z) for x, z in zip(LL, zl)] + [(t[0], z) for t, z in zip(TO, zt)]
    inner_R = [(max(x[0], 0.0), z) for x, z in zip(LR, zl)]
    inner_L = [(min(x[1], 0.0), z) for x, z in zip(LL, zl)]
    front = outer_R + list(reversed(outer_L)) + inner_L + list(reversed(inner_R))
    fr = [(min(a[2], b[2]), z) for a, b, z in zip(LR, LL, zl)] + [(t[2], z) for t, z in zip(TO, zt)]
    bk = [(max(a[3], b[3]), z) for a, b, z in zip(LR, LL, zl)] + [(t[3], z) for t, z in zip(TO, zt)]
    fr = [(fr[0][0], Z_HEM_T + 0.0254)] + [p for p in fr[1:] if p[1] > Z_HEM_T + 0.0254]   # O11/C6: front of the hem 1 in higher, no spike
    side = fr + list(reversed(bk))
    return dict(front=[np.array(front)], side=[np.array(side)], LR=LR, LL=LL, zl=zl, TO=TO, zt=zt)


# ---------------------------------------------------------------- seams (3D) and cover
def ring(S2, z):
    return [[float(x), float(y), float(z)] for x, y in np.vstack([S2, S2[:1]])]


def seams(jv, tv):
    out = {"jumper": {}, "trousers": {}}
    J = out["jumper"]
    for sgn, nm in ((+1, "L"), (-1, "R")):
        pts = []
        for z in jv["zb"]:
            S = jumper_body(z)
            if isinstance(S, tuple):
                pts.append([sgn * S[1][1], 0.0, z])
            else:
                i = np.argmax(sgn * S[:, 0]); pts.append([float(S[i, 0]), float(S[i, 1]), float(z)])
        J["side_seam_" + nm] = pts
        xs = np.linspace(NECK_PT[0], SH_PT[0], 8)
        J["shoulder_seam_" + nm] = [[float(sgn * x), float(NECK_PT[1] + (SH_PT[1] - NECK_PT[1]) * (x - NECK_PT[0]) / (SH_PT[0] - NECK_PT[0])),
                                     float(_top_z(x) + D_CHEST)] for x in xs]
        th = np.linspace(0, 2 * np.pi, 33)
        xa, yc, hy = sgn * 0.228, 0.0225, 0.0755 + D_CHEST
        zc, hz = (Z_UNDER + SH_PT[2] + D_CHEST) / 2, (SH_PT[2] + D_CHEST - Z_UNDER) / 2
        J["armhole_seam_" + nm] = [[float(xa), float(yc + hy * math.sin(t)), float(zc + hz * math.cos(t))] for t in th]
        S, A, r = jv["S"], jv["A"].copy(), jv["r"]
        A[:, 0] *= sgn
        h = JT["sleeve_cap_height"] / 100
        k = S >= h
        hw, _ = sleeve_half_widths(S)
        J["sleeve_underarm_seam_" + nm] = [[float(a[0] - sgn * rr), float(a[1]), float(a[2])] for a, rr in zip(A[k], hw[k])]
        t = (WRIST - ELBOW) / np.linalg.norm(WRIST - ELBOW)
        u = np.cross(t, [0, 0, 1.0]); u /= np.linalg.norm(u); w = np.cross(t, u)
        rc = JT["cuff_rib_relaxed"] / 100 / (2 * np.pi)
        W = WRIST * np.array([sgn, 1, 1])
        J["cuff_edge_" + nm] = [list(map(float, W + rc * (math.cos(a) * u * np.array([sgn, 1, 1]) + math.sin(a) * w * np.array([sgn, 1, 1])))) for a in th]
    th = np.linspace(0, 2 * np.pi, 41)
    J["neck_rib_seam"] = [[float(NECK_PT[0] * math.sin(a)), float((BACK_NECK[1] + FRONT_NECK_SEAM[1]) / 2 + (BACK_NECK[1] - FRONT_NECK_SEAM[1]) / 2 * math.cos(a)),
                           float(NECK_PT[2] - (NECK_PT[2] - (BACK_NECK[2] if math.cos(a) > 0 else FRONT_NECK_SEAM[2])) * abs(math.cos(a)) ** 1.5)] for a in th]
    J["hem_edge"] = ring(jumper_body(Z_HEM + 1e-4), Z_HEM)
    J["hem_rib_top"] = ring(jumper_body(Z_RIB - 1e-4), Z_RIB)
    Tz = out["trousers"]
    for sgn, nm in ((+1, "L"), (-1, "R")):
        o, i_ = [], []
        for z, e in zip(tv["zl"], tv["LR"] if sgn > 0 else tv["LL"]):
            yc = float((e[2] + e[3]) / 2)
            xo, xi = (e[1], e[0]) if sgn > 0 else (e[0], e[1])
            o.append([float(xo), yc, float(z)])
            if z <= Z_FORK:
                i_.append([float(np.clip(xi, 0, None) if sgn > 0 else np.clip(xi, None, 0)), yc, float(z)])
        for z in tv["zt"]:
            S = trouser_torso(max(z, 0.83)); a = np.argmax(sgn * S[:, 0]); o.append([float(S[a, 0]), float(S[a, 1]), float(z)])
        Tz["outseam_" + nm] = o
        Tz["inseam_" + nm] = i_
        c = leg_centre(Z_HEM_T, sgn); rr = G_HEM / (2 * np.pi)
        Tz["hem_" + nm] = [[float(c[0] + rr * math.cos(a)), float(c[1] + rr * math.sin(a)), float(Z_HEM_T + (0.0254 if math.sin(a) < 0 else 0) * abs(math.sin(a)))] for a in th]
    Tz["waistband_lower_edge"] = ring(trouser_torso(Z_BAND_LO), Z_BAND_LO)
    Tz["waistband_top_edge"] = ring(trouser_torso(Z_BAND_HI), Z_BAND_HI)
    fr, bk = [], []
    for z in zs(Z_FORK, Z_BAND_LO, 0.01):
        S = trouser_torso(max(z, 0.83))
        near = S[np.abs(S[:, 0]) < 0.06]
        if len(near) == 0:
            near = S
        fr.append([0.0, float(near[:, 1].min()), float(z)]); bk.append([0.0, float(near[:, 1].max()), float(z)])
    Tz["crotch_seam_front_to_back"] = list(reversed(fr)) + [[0.0, float((fr[0][1] + bk[0][1]) / 2), float(Z_FORK)]] + bk
    return out


def _top_z(x):
    m = (np.abs(V[:, 0] - x) < 0.006) & (V[:, 2] < 1.70) & (V[:, 2] > 1.4) & (np.abs(V[:, 1]) < 0.1)
    return float(V[m, 2].max())


def cover():
    z, x, y = V[:, 2], V[:, 0], V[:, 1]
    arm = (z < 1.30) & (z > 0.85) & (np.abs(x) > arm_line(z))
    t = (WRIST - ELBOW) / np.linalg.norm(WRIST - ELBOW)
    Vm = V * np.c_[np.sign(x), np.ones(len(x)), np.ones(len(x))]
    hand = ((Vm - WRIST) @ t > 0) & (np.abs(x) > 0.2) & (z < 1.12)
    neck_z = np.where(y < 0.0, FRONT_NECK_SEAM[2], BACK_NECK[2]) + (NECK_PT[2] - np.where(y < 0, FRONT_NECK_SEAM[2], BACK_NECK[2])) * np.clip(np.abs(x) / NECK_PT[0], 0, 1) ** 2
    head = (z > neck_z) & (np.abs(x) < 0.13)
    jumper = (z >= Z_HEM) & ~hand & ~head & (z < 1.75)
    trousers = (z >= Z_HEM_T) & (z <= Z_BAND_HI) & ~arm & ~hand
    # C2: the feet are not trousers: drop points below the hem line (0.040 at the back rising
    # to 0.0654 at the front, O11) or outside the leg tube, below z 0.12
    for sgn in (+1, -1):
        c = leg_centre(Z_HEM_T, sgn); rr = G_HEM / (2 * np.pi)
        yb, yf = c[1] + rr, c[1] - rr
        low = (z < 0.12) & (sgn * x > 0)
        zline = Z_HEM_T + 0.0254 * np.clip((yb - y) / (yb - yf), 0, 1)
        out = np.zeros(len(z), bool)
        for i in np.where(low & trousers)[0]:
            Sx = trouser_leg(max(z[i], Z_HEM_T), sgn)
            out[i] = (not mpath.Path(Sx).contains_point((x[i], y[i]))) or z[i] < zline[i]
        trousers &= ~out
    return dict(jumper=np.where(jumper)[0], trousers=np.where(trousers)[0], hands=np.where(hand)[0], head=np.where(head)[0])


# ---------------------------------------------------------------- masks and pictures
FRONT = Frame(u0=-0.45, v0=-0.02, width=0.90, height=2.00, mm_per_px=2)
SIDE = Frame(u0=-0.40, v0=-0.02, width=0.70, height=2.00, mm_per_px=2)


def mask(polys, fr):
    img = Image.new("1", (fr.shape[1], fr.shape[0]), 0)
    dr = ImageDraw.Draw(img)
    for P in polys:
        Q = np.stack(fr.to_px(P[:, 0], P[:, 1]), 1)
        dr.polygon([tuple(q) for q in Q], fill=1, outline=1)
    return np.array(img, dtype=bool)


def picture(body, jm, tm, path, mirror=False):
    h, w = body.shape
    rgb = np.full((h, w, 3), 255, np.uint8)
    rgb[body] = (205, 205, 205)
    for m, col in ((tm, (60, 80, 160)), (jm, (160, 60, 50))):
        a = 0.75
        rgb[m] = (rgb[m] * (1 - a) + np.array(col) * a).astype(np.uint8)
    im = Image.fromarray(rgb[:, ::-1] if mirror else rgb)
    im.save(path)


def self_check(cv, masks, tol_mm=3.0):
    """Every covered point must fall inside its garment's outline in every view, within 3 mm."""
    out = {}
    for g in ("jumper", "trousers"):
        P = V[cv[g]]
        for view, fr, ax in (("front", FRONT, (0, 2)), ("side", SIDE, (1, 2))):
            m = masks["%s_%s" % (g, view)]
            dist = ndimage.distance_transform_edt(~m) * fr.mm_per_px
            u, v = fr.to_px(P[:, ax[0]], P[:, ax[1]])
            i = np.clip(np.floor(v).astype(int), 0, m.shape[0] - 1); j = np.clip(np.floor(u).astype(int), 0, m.shape[1] - 1)
            dd = dist[i, j]
            out["%s_%s" % (g, view)] = dict(points=int(len(P)), outside_3mm=int((dd > tol_mm).sum()), worst_mm=round(float(dd.max()), 1))
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    jv, tv = jumper_views(), trouser_views()
    sm = seams(jv, tv)
    cv = cover()
    np.savez_compressed(os.path.join(OUT, "cover_lod0.npz"), **{k: v.astype(np.int32) for k, v in cv.items()})
    meshes = {"ron": (V, F)}
    bf = silhouette(meshes, (0, 2), FRONT)
    bs = silhouette(meshes, (1, 2), SIDE)
    masks = {}
    for g, v in (("jumper", jv), ("trousers", tv)):
        masks[g + "_front"] = mask(v["front"], FRONT)
        masks[g + "_side"] = mask(v["side"], SIDE)
    for k, m in masks.items():
        Image.fromarray((m * 255).astype(np.uint8)).save(os.path.join(OUT, "mask_%s.png" % k))
    picture(bf, masks["jumper_front"], masks["trousers_front"], os.path.join(OUT, "target_front.png"))
    picture(bf, masks["jumper_front"], masks["trousers_front"], os.path.join(OUT, "target_back.png"), mirror=True)
    picture(bs, masks["jumper_side"], masks["trousers_side"], os.path.join(OUT, "target_side.png"))
    check = self_check(cv, masks)
    area = lambda m: round(float(m.sum()) * 4e-6, 4)
    poly = lambda Ps: [[[round(float(a), 4), round(float(b), 4)] for a, b in P] for P in Ps]
    tj = dict(
        frame="metres; x lateral (+x his left), y depth (front -y), z up, feet at z = 0; front/back views on (x, z) "
              "(identical silhouettes: the back picture is the front mirrored); side view on (y, z), front to the left",
        body=BODY, rules="TARGET.md O1-O14", pattern="pattern.json",
        levels=dict(jumper_hem=round(Z_HEM, 4), jumper_rib_top=round(Z_RIB, 4), jumper_underarm=round(Z_UNDER, 4),
                    waistband_lower=Z_BAND_LO, waistband_top=round(Z_BAND_HI, 4), trouser_seat_line=round(Z_SEATLINE, 4),
                    trouser_fork=Z_FORK, trouser_knee_line=round(Z_KNEE, 4), trouser_hem_back=Z_HEM_T, trouser_hem_front=round(Z_HEM_T + 0.0254, 4),
                    chest_ease_offset_m=round(D_CHEST, 4)),
        views=dict(jumper=dict(front=poly(jv["front"]), back=poly(jv["front"]), side=poly(jv["side"])),
                   trousers=dict(front=poly(tv["front"]), back=poly(tv["front"]), side=poly(tv["side"]))),
        view_parts=dict(jumper_front=["body and yoke", "left sleeve (+x)", "right sleeve (-x)"], jumper_side=["body and yoke", "sleeve"],
                        trousers_front=["trousers"], trousers_side=["trousers"]),
        masks=dict(mm_per_px=2, front_frame=FRONT.__dict__, side_frame=SIDE.__dict__,
                   area_m2={k: area(m) for k, m in masks.items()}, files={k: "mask_%s.png" % k for k in masks}),
        seams=sm,
        covered=dict(
            jumper="torso from the neckline (back neck z 1.635, neck points z 1.668, front z 1.600) down to the hem z %.3f; both arms from the shoulder to the wrist (cuff edge at the wrist point %s); not the head, neck above the neckline, or the hands" % (Z_HEM, list(WRIST)),
            trousers="from the waistband top z %.4f down to the hem (z 0.040 at the back, 0.065 at the front); both legs; not the feet, hands or arms" % Z_BAND_HI,
            lod0_vertex_counts={k: int(len(v)) for k, v in cv.items()}, indices_file="cover_lod0.npz (LOD0 vertex indices)"),
        self_check=check,
        not_in_outline="head, neck above the rib, hands beyond the cuff, feet below the hem: clothes only",
    )
    json.dump(tj, open(os.path.join(HERE, "target.json"), "w"), indent=None, separators=(",", ":"))
    print("levels", tj["levels"])
    print("self-check (covered points outside own outline by > 3 mm):", check)
    if any(v["outside_3mm"] for v in check.values()):
        raise SystemExit("SELF-CHECK FAILED")
    print("areas", tj["masks"]["area_m2"], "cover", tj["covered"]["lod0_vertex_counts"])


if __name__ == "__main__":
    main()
