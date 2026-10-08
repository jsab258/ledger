"""Ron's jumper and trousers MODELLED on his body to a pattern (no cloth simulation).

    python model_clothes.py [version]  -> F:/LedgerTools/lab/clothes/clothes_<version>.npz

Inputs (model_inputs.json): the pattern's girths and lengths (target/pattern.json), Ron's
measures as TARGET.md states them, and the levels and rules TARGET.md writes (O1-O13), read
as a modeller reads a dimensioned drawing. The outline polygons and seam lines in target.json
are never read here; only check_clothes.py reads them.

How it is made (no simulation; the body never moves):
- Sections. The jumper's body and the trouser seat are horizontal sections every 5 mm, the
  sleeves sections square to the arm, the trouser legs horizontal sections. Each is the body's
  own section as a tape takes it (its convex hull), grown evenly to the pattern's girth, or by
  the rules' stand-off where the cloth hangs free of it.
- The shoulders and neck rib: a layer lifted off the body (18 mm, the chest ease; the rib 3 mm).
- The parts are fused into one surface per garment (solidify.py) and the seams are laid on
  it where the pattern puts them (seams.py).
"""
import json
import math
import os
import sys

import numpy as np
from scipy.spatial import ConvexHull, cKDTree

import solidify

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r"F:/LedgerTools/lab/clothes"


def hull(P):
    if len(P) < 3:
        return P
    h = ConvexHull(P)
    return P[h.vertices]


def perimeter(P):
    Q = np.vstack([P, P[:1]])
    return float(np.sum(np.linalg.norm(np.diff(Q, axis=0), axis=1)))


def resample_loop(P, n):
    Q = np.vstack([P, P[:1]])
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))])
    t = np.linspace(0, s[-1], n, endpoint=False)
    return np.stack([np.interp(t, s, Q[:, 0]), np.interp(t, s, Q[:, 1])], 1)


def offset_convex(P, d, n=96):
    """A convex loop let out by d all round (rounded corners), resampled to n points."""
    Pr = resample_loop(P, 400)
    c = Pr.mean(0)
    # outward normals of the resampled loop
    T = np.roll(Pr, -1, 0) - np.roll(Pr, 1, 0)
    N = np.stack([T[:, 1], -T[:, 0]], 1)
    N /= np.linalg.norm(N, axis=1, keepdims=True)
    if np.mean(np.einsum("ij,ij->i", N, Pr - c)) < 0:
        N = -N
    Q = Pr + N * d
    return resample_loop(hull(Q), n)


def let_out_to(P, girth, min_ease, n=96):
    """Let a convex section out until its girth is `girth` (at least min_ease over the hull)."""
    p0 = perimeter(P)
    target = max(girth, p0 + min_ease)
    d = (target - p0) / (2 * math.pi)
    Q = offset_convex(P, d, n)
    for _ in range(3):                      # correct for resampling
        d += (target - perimeter(Q)) / (2 * math.pi)
        Q = offset_convex(P, d, n)
    return Q


def align_loops(loops):
    """Rotate each ring's start to its predecessor's nearest point, so the strip does not twist."""
    out = [loops[0]]
    for L in loops[1:]:
        k = int(np.argmin(np.linalg.norm(L - out[-1][0], axis=1)))
        L = np.roll(L, -k, axis=0)
        # keep the same winding
        a = out[-1] - out[-1].mean(0)
        b = L - L.mean(0)
        if np.cross(a[0], a[len(a) // 4]) * np.cross(b[0], b[len(b) // 4]) < 0:
            L = np.vstack([L[:1], L[1:][::-1]])
        out.append(L)
    return out


def align3d(rings):
    """Roll each ring so it starts nearest its predecessor's start and keeps its winding."""
    out = [rings[0]]
    for R in rings[1:]:
        k = int(np.argmin(np.linalg.norm(R - out[-1][0], axis=1)))
        R = np.roll(R, -k, axis=0)
        prev = out[-1]
        fwd = np.linalg.norm(R[1:len(R) // 4] - prev[1:len(R) // 4]).sum()
        Rr = np.vstack([R[:1], R[1:][::-1]])
        bwd = np.linalg.norm(Rr[1:len(R) // 4] - prev[1:len(R) // 4]).sum()
        out.append(R if fwd <= bwd else Rr)
    return out


RING_META = {}


def tube(rings3d, name=None, axes=None):
    """Quad-strip mesh from a list of rings (each (n,3), same n)."""
    n = len(rings3d[0])
    if name:
        C = np.array([r.mean(0) for r in rings3d])
        A = np.array(axes) if axes is not None else np.tile([0, 0, 1.0], (len(rings3d), 1))
        RING_META[name] = (n, C, A)
    V = np.vstack(rings3d)
    F = []
    for i in range(len(rings3d) - 1):
        a, b = i * n, (i + 1) * n
        for j in range(n):
            k = (j + 1) % n
            F.append((a + j, a + k, b + k))
            F.append((a + j, b + k, b + j))
    return V, np.array(F)


def vertex_normals(V, F):
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    vn = np.zeros_like(V)
    for k in range(3):
        np.add.at(vn, F[:, k], n)
    return vn / np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-12)


class Body:
    def __init__(self):
        d = np.load(os.path.join(OUT, "ron_parts.npz"))
        self.V, self.F = d["V"], d["F"]
        self.arm, self.torso, self.legs = d["arm"], d["torso"], d["legs"]
        self.N = vertex_normals(self.V, self.F)
        E = np.vstack([self.F[:, [0, 1]], self.F[:, [1, 2]], self.F[:, [2, 0]]])
        self.E = np.unique(np.sort(E, axis=1), axis=0)

    def plane_section(self, mask, c, n):
        """The body's exact cross-section by the plane through c with normal n: where the edges
        of the masked surface cross it (a tape round the body there), in 3D."""
        E = self.E[mask[self.E[:, 0]] & mask[self.E[:, 1]]]
        a = (self.V[E[:, 0]] - c) @ n
        b = (self.V[E[:, 1]] - c) @ n
        m = (a * b) <= 0
        t = a[m] / np.where(a[m] - b[m] == 0, 1e-12, a[m] - b[m])
        return self.V[E[m, 0]] + t[:, None] * (self.V[E[m, 1]] - self.V[E[m, 0]])

    def section(self, mask, z, band=None):
        """The horizontal cross-section at height z (x, y)."""
        P = self.plane_section(mask, np.array([0, 0, z]), np.array([0, 0, 1.0]))
        return P[:, :2]


def girth_fn(table):
    """Pattern girths [(z_m, girth_m), ...] -> interpolating function of z."""
    t = sorted(table)
    zs = np.array([a for a, b in t])
    gs = np.array([b for a, b in t])
    return lambda z: float(np.interp(z, zs, gs))



def neckline_z(V, P):
    """The neckline seam's height round the neck: the pattern's neckline is a quarter-ellipse on
    each piece (half-width the neck width J10, depth the back J11 or front J12 neck depth), so
    below the neck point's height it drops by depth * sqrt(1 - (x / half-width)^2)."""
    cb, npnt, cf = P["neck_back"], P["neck_point"], P["neck_front"]
    yc = 0.5 * (cb[1] + cf[1])
    depth = np.where(V[:, 1] >= yc, npnt[2] - cb[2], npnt[2] - cf[2])
    u = np.clip(1 - (V[:, 0] / npnt[0]) ** 2, 0, 1)
    return npnt[2] - depth * np.sqrt(u)


def neck_ceiling(X, P):
    """Over the neck opening, and behind and in front of the neck, the yoke stops at the
    neckline's height (as the target grows each height's section, not the surface's normal);
    over the shoulders it has no ceiling."""
    cb, npnt, cf = P["neck_back"], P["neck_point"], P["neck_front"]
    yc, ry = 0.5 * (cb[1] + cf[1]), 0.5 * (cb[1] - cf[1])
    e = np.hypot(X[:, 0] / npnt[0], (X[:, 1] - yc) / ry)
    a = np.arctan2(np.abs(X[:, 0]) / npnt[0], (X[:, 1] - yc) / ry)      # 0 at the back, pi at the front
    near_cb_cf = (e < 1.8) & ((a < math.pi / 4) | (a > 3 * math.pi / 4))  # behind and in front of the neck
    return np.where((e < 1.0) | near_cb_cf, neckline_z(X, P), 9.0)


def neck_rib_sheet(P, n=96, m=6):
    """The crew-neck rib (J14): a band 2.5 cm deep standing on the neckline (back neck, neck
    points, front neck), its foot just outside the neckline seam, as a sheet of points."""
    cb, npnt, cf = P["neck_back"], P["neck_point"], P["neck_front"]
    yc, ry = 0.5 * (cb[1] + cf[1]), 0.5 * (cb[1] - cf[1])
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    off = P.get("rib_centre_off_m", 0.003)                         # the wall's centre just outside the seam
    x = (npnt[0] + off) * np.sin(th)
    y = yc + (ry + off) * np.cos(th)
    z0 = neckline_z(np.stack([x, y, np.zeros(n)], 1), P)
    pts = []
    top = P["neck_rib_m"] - P.get("rib_thickness_m", 0.004)     # the wall's outer top at the rib depth
    for t in (np.linspace(0, 1, m) if m > 1 else [0.0]):
        pts.append(np.stack([x, y, z0 + t * top], 1))
    return np.vstack(pts)


def by_angle(Q, c, n=96):
    """A convex loop as radii at n even angles about c (for blending two loops)."""
    Q = resample_loop(Q, 720)
    ang = np.arctan2(Q[:, 1] - c[1], Q[:, 0] - c[0])
    r = np.hypot(Q[:, 0] - c[0], Q[:, 1] - c[1])
    o = np.argsort(ang)
    t = np.linspace(-math.pi, math.pi, n, endpoint=False)
    return np.interp(t, ang[o], r[o], period=2 * math.pi), t


def blend(Q0, Q1, w, n=96):
    c = 0.5 * (Q0.mean(0) + Q1.mean(0))
    r0, t = by_angle(Q0, c, n)
    r1, _ = by_angle(Q1, c, n)
    r = (1 - w) * r0 + w * r1
    return c + r[:, None] * np.stack([np.cos(t), np.sin(t)], 1)


def grow(H, girth, so):
    """O2: the section grown evenly to the girth; never less than the stand-off (O1)."""
    d = max((girth - perimeter(H)) / (2 * math.pi), so)
    Q = offset_convex(H, d)
    if d > so:
        for _ in range(3):
            d += (girth - perimeter(Q)) / (2 * math.pi)
            Q = offset_convex(H, max(d, so))
    return Q


def jumper_body(B, P, over):
    """O3-O7: above the underarm the upper body grown by the chest ease; below it the hull of the
    eased chest and the body (or the trousers) + 3 mm, falling straight; the rib grips the hip
    over the trousers and blouses into the body over 4 cm."""
    z_hem, z_un, z_band = P["jumper_hem_z"], P["jumper_underarm_z"], P["shoulder_band_z"]
    z_rib = z_hem + P["jumper_rib_m"]
    so, yoke, blouse = P["stand_off_m"], P["yoke_offset_m"], P["rib_blouse_m"]
    torso_only = B.torso & ~B.arm

    def under(z):
        S = B.section(torso_only, z)
        if over is not None:
            zs = np.array([o[0, 2] for o in over])
            if zs.min() - 0.003 <= z <= zs.max() + 0.003:
                S = np.vstack([S, over[int(np.argmin(np.abs(zs - z)))][:, :2]])
        return offset_convex(hull(S), so)

    # the eased chest: the torso's section at the chest line (Ron's measured chest height) grown to
    # the finished chest
    zc = P["chest_line_z"]                    # measurements.json heights_m.chest
    Hc = grow(hull(B.section(torso_only, zc)), P["chest_finished_m"], so)
    # knit falls smoothly over what is beneath it: each height takes in the sections within 2 cm
    # above and below it (the waistband's top edge and small hollows do not print through)
    zz = np.arange(z_hem - 0.02, zc + 1e-6, 0.005)
    U = {round(z, 4): under(z) for z in zz}
    win = P.get("drape_window_m", 0.02)

    def under_smooth(z):
        near = [U[k] for k in U if abs(k - z) <= win + 1e-9]
        return hull(np.vstack(near)) if near else under(z)
    rings = []
    for z in np.arange(z_hem - 0.02, z_band + 1e-6, 0.005):
        if z >= zc:
            Q = offset_convex(hull(B.section(torso_only, z)), so + (yoke - so) * min((z - z_un) / P.get("yoke_ramp_m", 0.05), 1.0))
        else:
            # below the chest line the jumper falls straight from the eased chest (O5); between the
            # underarm and the chest line the upper body is still the chest ease off the body (O3)
            ramp = so + (yoke - so) * min((z - z_un) / P.get("yoke_ramp_m", 0.05), 1.0)
            Hb = offset_convex(hull(B.section(torso_only, z)), ramp) if z > z_un else under_smooth(z)
            straight = resample_loop(hull(np.vstack([Hc, Hb])), 96)
            if z <= z_rib + blouse:
                rib = Hb if perimeter(Hb) >= P["rib_girth_m"] else grow(Hb, P["rib_girth_m"], so)
                rib = resample_loop(rib, 96)
                w = 0.0 if z <= z_rib else math.sin(min((z - z_rib) / blouse, 1.0) * math.pi / 2)
                Q = blend(rib, straight, w)
            else:
                Q = straight
        rings.append(np.c_[Q, np.full(len(Q), z)])
    return tube(align3d(rings), "jumper_body")


def limb_tube(B, mask, axis_pts, girths, s_top, s_end, so, step=0.01, n=64, name=None, bend=0.07, cap=None):
    """O8: sections square to the arm's axis, each the arm's section grown to the pattern's width."""
    A = np.asarray(axis_pts, float)
    seg = np.linalg.norm(np.diff(A, axis=0), axis=1)
    cs = np.concatenate([[0], np.cumsum(seg)])
    G = girth_fn(girths)
    pts = B.V[mask]
    rings, axes = [], []
    for s in np.arange(s_top, s_end + 1e-6, step):
        k = min(int(np.searchsorted(cs, s, side="right")) - 1, len(A) - 2)
        t = (s - cs[k]) / max(seg[k], 1e-9)
        c = A[k] + t * (A[k + 1] - A[k])
        ax = np.zeros(3)                         # the axis averaged over a window: rings turn round the elbow
        for u in np.linspace(s - bend, s + bend, 13):
            kk = min(max(int(np.searchsorted(cs, u, side="right")) - 1, 0), len(A) - 2)
            ax += (A[kk + 1] - A[kk]) / seg[kk]
        ax /= np.linalg.norm(ax)
        e1 = np.cross(ax, [0, 0, 1.0]) if abs(ax[2]) < 0.99 else np.array([1.0, 0, 0])
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(ax, e1)
        sl = B.plane_section(mask, c, ax)
        sl = sl[np.linalg.norm(sl - c, axis=1) < 0.15]
        if len(sl) >= 3:
            H = hull(np.stack([(sl - c) @ e1, (sl - c) @ e2], 1))
        else:
            H = np.array([[0.03, 0], [0, 0.03], [-0.03, 0], [0, -0.03]])
        # O8 and C4: below the cap the arm's section grown to the pattern's width; over the cap the
        # stand-off grows from 3 mm at the shoulder point to the biceps line's along a quarter-sine
        if cap is not None and s < cap[0]:
            e = so + (cap[1] - so) * math.sin(math.pi / 2 * max(s, 0.0) / cap[0])
            Q = resample_loop(offset_convex(H, e), n)
        else:
            Q = resample_loop(grow(H, G(s), so), n)
        rings.append(c + Q[:, :1] * e1 + Q[:, 1:] * e2)
        axes.append(ax)
    return tube(align3d(rings), name, axes)


def biceps_ease(B, mask, axis_pts, h, girth, so):
    """The sleeve's ease at the biceps line (the cap height): (sleeve width - arm girth) / 2 pi."""
    A = np.asarray(axis_pts, float)
    seg = np.linalg.norm(np.diff(A, axis=0), axis=1)
    cs = np.concatenate([[0], np.cumsum(seg)])
    k = min(int(np.searchsorted(cs, h, side="right")) - 1, len(A) - 2)
    c = A[k] + (h - cs[k]) / seg[k] * (A[k + 1] - A[k])
    ax = (A[k + 1] - A[k]) / seg[k]
    sl = B.plane_section(mask, c, ax)
    sl = sl[np.linalg.norm(sl - c, axis=1) < 0.15]
    e1 = np.cross(ax, [0, 0, 1.0]); e1 /= np.linalg.norm(e1); e2 = np.cross(ax, e1)
    H = hull(np.stack([(sl - c) @ e1, (sl - c) @ e2], 1))
    return max((girth - perimeter(H)) / (2 * math.pi), so)


def superellipse(x0, x1, y0, y1, p=2.6, n=64):
    t = np.linspace(0, 2 * math.pi, n, endpoint=False)
    c, s = np.cos(t), np.sin(t)
    xc, yc, a, b = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    return np.stack([xc + a * np.sign(c) * np.abs(c) ** (2 / p), yc + b * np.sign(s) * np.abs(s) ** (2 / p)], 1)


def trousers(B, P):
    """O9-O11: the waistband grown to its girth, the girth running straight down to the seat at
    the seat line; from the knee line up to the seat line each leg's edges run straight to the
    seat's side, the fork, the seat's front and its fullest back; below the knee a round tube of
    the pattern's girth. Returns (seat rings, leg rings by side)."""
    so = P["stand_off_m"]
    V = B.V
    z_band_top, z_band_low = P["trouser_waist_z"], P["waistband_lower_z"]
    z_seat, z_fork, z_knee = P["trouser_seat_line_z"], P["trouser_crotch_z"], P["trouser_knee_line_z"]
    G = girth_fn([[z_seat, P["seat_m"]], [z_band_low, P["waistband_m"]], [z_band_top, P["waistband_m"]]])
    seat = []
    for z in np.arange(z_seat, z_band_top + 0.02 + 1e-6, 0.005):
        H = hull(B.section(B.torso | B.legs, min(z, z_band_top)))
        seat.append(np.c_[resample_loop(grow(H, G(z), so), 96), np.full(96, z)])
    S0 = seat[0][:, :2]
    # the seat's fullest back: the farthest back the body reaches between the fork and the band, + stand-off
    zone = (B.torso | B.legs) & (V[:, 2] > z_fork) & (V[:, 2] < z_band_low)
    back_y = max(float(V[zone, 1].max()) + so, float(S0[:, 1].max()))
    LG = girth_fn([[P["trouser_hem_back_z"], P["hem_one_leg_m"]], [z_knee, P["knee_one_leg_m"]]])
    legs = {}
    for side, sgn in (("R", -1), ("L", 1)):
        lmask = B.legs & (np.sign(V[:, 0]) == sgn)

        def centre(z):                           # the middle of the leg's extremes at that height
            H = hull(B.section(lmask, z))
            return 0.5 * (H.min(0) + H.max(0))
        ck, ca = centre(z_knee), centre(0.10)
        rings = []
        rk = LG(z_knee) / (2 * math.pi)
        # the knee ring's extremes, where the straight edges above it start
        kx_out, kx_in = sgn * ck[0] + rk, sgn * ck[0] - rk
        ky_f, ky_b = ck[1] - rk, ck[1] + rk
        sx_out = float((S0[:, 0] * sgn).max())
        sy_f = float(S0[:, 1].min())
        for z in np.arange(z_seat, P["trouser_hem_back_z"] - 0.03, -0.005):
            if z <= z_knee:
                t = min((z_knee - z) / (z_knee - 0.10), 1.0)
                # the leg hangs plumb from the knee side to side, and follows the shin front to back
                c = np.array([ck[0], ck[1] + t * (ca[1] - ck[1])])
                r = LG(z) / (2 * math.pi)
                tt = np.linspace(0, 2 * math.pi, 64, endpoint=False)
                Q = c + r * np.stack([np.cos(tt), np.sin(tt)], 1)
            else:
                f = (z - z_knee) / (z_seat - z_knee)
                x_out = kx_out + f * (sx_out - kx_out)
                fi = min((z - z_knee) / (z_fork - z_knee), 1.0)
                x_in = kx_in + fi * (0.0 - kx_in)
                y_f = ky_f + f * (sy_f - ky_f)
                y_b = ky_b + f * (back_y - ky_b)
                Q = superellipse(x_in, x_out, y_f, y_b, p=2.0 + 0.6 * f)
                Q[:, 0] *= sgn
            S = B.section(lmask, z) if z >= 0.12 else np.zeros((0, 2))   # below 0.12 the foot is not the leg (C2)
            if len(S) >= 3:                       # O1: never closer than the stand-off
                Hb = offset_convex(hull(S), so)
                if not solidify.in_poly(Hb, Q).all():
                    Q = resample_loop(hull(np.vstack([Q, Hb])), 64)
            rings.append(np.c_[Q, np.full(len(Q), z)])
        legs[side] = rings
    # from the fork up to the seat line the trousers are one section round both legs (O10)
    crotch = []
    for z in np.arange(z_fork, z_seat - 1e-6, 0.005):
        k = int(round((z_seat - z) / 0.005))
        Q = hull(np.vstack([legs["L"][k][:, :2], legs["R"][k][:, :2]]))
        crotch.append(np.c_[resample_loop(Q, 96), np.full(96, z)])
    seat = crotch + seat
    return seat, legs


def build(P, ver):
    B = Body()
    V = B.V
    so = P["stand_off_m"]
    h = P.get("grid_m", 0.005)
    seat, legs = trousers(B, P)
    parts = {"trouser_seat": tube(align3d(seat), "trouser_seat")}
    for side in ("R", "L"):
        parts["trouser_leg_" + side] = tube(align3d(legs[side]), "trouser_leg_" + side, [[0, 0, -1.0]] * len(legs[side]))
    parts["jumper_body"] = jumper_body(B, P, over=seat)
    sleeves, sleeve_end = {}, {}
    for side, sgn in (("R", -1), ("L", 1)):
        ax = [np.array(p) * np.array([sgn, 1, 1]) for p in P["arm_axis_L"]]
        mask = B.arm & (np.sign(V[:, 0]) == sgn)
        e_h = biceps_ease(B, mask, ax, P["sleeve_seam_from_s"], P["sleeve_biceps_m"], so)
        parts["sleeve_" + side] = limb_tube(B, mask, ax, P["sleeve_girths"], P["sleeve_s_top"], P["sleeve_s_cuff"] + 0.02, so,
                                            name="sleeve_" + side, cap=(P["sleeve_seam_from_s"], e_h))
        sleeves[side] = parts["sleeve_" + side][0].reshape(-1, 64, 3)
        n_, C_, A_ = RING_META["sleeve_" + side]
        kc = int(round((P["sleeve_s_cuff"] - P["sleeve_s_top"]) / 0.01))
        sleeve_end[side] = (C_[kc], A_[kc])

    # ---- the jumper: the body with its yoke and rib as one solid, each sleeve its own, united
    #      at the armholes; the openings cut crisp at the hem and the cuffs
    nl = neckline_z(V, P)
    top = nl + P["neck_rib_m"]
    up = (B.arm | B.torso) & (V[:, 2] > P["jumper_underarm_z"] - 0.02) & (V[:, 2] < top) & (np.abs(V[:, 0]) < 0.31)
    allj = np.vstack([parts[k][0] for k in parts if not k.startswith("trouser")] + [V[up]])
    lo, hi = allj.min(0) - 0.05, allj.max(0) + 0.05
    gj = solidify.Grid(lo, hi, h)
    gj.add_slices(parts["jumper_body"][0].reshape(-1, 96, 3))
    below = up & (V[:, 2] < nl + 0.004)
    zr = np.clip((V[below, 2] - P["jumper_underarm_z"]) / P.get("yoke_ramp_m", 0.05), 0, 1)
    # C7: near the neck the yoke's ease tapers to the rib's 3 mm at the seam over the last 8 cm
    seam = neck_rib_sheet(P, m=1)
    ds = cKDTree(seam).query(V[below])[0]
    zn = np.clip(ds / P.get("neck_taper_m", 0.08), 0, 1)
    dist = so + (P["yoke_offset_m"] - so) * np.minimum(zr, zn)   # in over 5 cm above the underarm, out near the neck
    gj.add_near(V, B.N, below, dist, ceiling=lambda X: neck_ceiling(X, P),   # the yoke stops at the neckline seam
                zscale=P.get("yoke_zscale", 3.0))                         # and is grown sideways (O3), resting on top
    gj.add_wall(neck_rib_sheet(P), P.get("rib_thickness_m", 0.004))
    rib_zone = up & (V[:, 2] >= nl - 0.004) & (V[:, 2] < top) & (np.abs(V[:, 0]) < P["neck_point"][0] + 0.02)
    gj.add_near(V, B.N, rib_zone, np.full(rib_zone.sum(), so))        # the rib hugs the neck inside it
    gj.finish(P.get("blur_m", 0.004))
    gs = []
    for side in ("R", "L"):
        g_ = solidify.Grid(lo, hi, h)
        n_, C_, A_ = RING_META["sleeve_" + side]
        g_.add_tube(sleeves[side], C_, A_)
        g_.finish(P.get("blur_m", 0.004))
        gs.append(g_)
    gj.merge_max(gs)
    JV, JF = gj.surface()
    JV, JF = solidify.clip_open(JV, JF, np.array([0, 0, P["jumper_hem_z"]]), np.array([0, 0, -1.0]))
    for side in ("R", "L"):
        cuff_c, cuff_a = sleeve_end[side]
        JV, JF = solidify.clip_open(JV, JF, cuff_c, cuff_a)

    # ---- the trousers, fused; the hem level at the back and an inch higher at the front (T27)
    allt = np.vstack([parts[k][0] for k in parts if k.startswith("trouser")])
    gt = solidify.Grid(allt.min(0) - 0.03, allt.max(0) + 0.03, h)
    gt.add_slices(np.array(seat))
    for side in ("R", "L"):
        gt.add_slices(np.array(legs[side]))
    hem = np.array(legs["L"][-1])
    yb, yf = float(hem[:, 1].max()), float(hem[:, 1].min())
    zb_, zf_ = P["trouser_hem_back_z"], P["trouser_hem_front_z"]
    k = (zf_ - zb_) / (yb - yf)
    gt.finish(P.get("blur_m", 0.004))
    TV, TF = gt.surface()
    TV, TF = solidify.clip_open(TV, TF, np.array([0, 0, P["trouser_waist_z"]]), np.array([0, 0, 1.0]))
    # T27: the hem hollowed an inch at the front: one plane from the back of the hem to its front,
    # set a little low (hem_drop_m) so that its sides also sit near the level hem of the front view
    zd = P.get("hem_drop_m", 0.0045)
    TV, TF = solidify.clip_open(TV, TF, np.array([0, yb, zb_ - zd]), -np.array([0, k, 1.0]) / math.hypot(k, 1.0))

    import seams as SM
    kc = int(round((P["sleeve_s_cuff"] - P["sleeve_s_top"]) / 0.01))
    S = SM.jumper_seams(P, JV, JF, {sd: r[:kc + 1] for sd, r in sleeves.items()}, lambda X: neckline_z(X, P),
                        parts["jumper_body"][0].reshape(-1, 96, 3), neck_rib_sheet(P, m=1))
    S.update(SM.trouser_seams(P, TV, TF, legs, seat))
    out = {"jumper_V": JV, "jumper_F": JF, "trousers_V": TV, "trousers_F": TF}
    for kk, (Vk, Fk) in parts.items():
        out[kk + "_PV"], out[kk + "_PF"] = Vk, Fk
    for g, gr in (("jumper", gj), ("trousers", gt)):
        out["sdf_" + g] = gr.field.astype(np.float32)
        out["sdf_" + g + "_lo"] = gr.lo
        out["sdf_" + g + "_h"] = np.array(gr.h)
    for kk, v in S.items():
        out["seam_" + kk] = np.asarray(v)
    path = os.path.join(OUT, "clothes_%s.npz" % ver)
    np.savez_compressed(path, **out)
    return path, {"jumper": (JV, JF), "trousers": (TV, TF)}


if __name__ == "__main__":
    ver = sys.argv[1] if len(sys.argv) > 1 else "v1"
    P = json.load(open(os.path.join(HERE, "model_inputs.json")))
    path, parts = build(P, ver)
    print("wrote", path, {k: len(v[0]) for k, v in parts.items()})
