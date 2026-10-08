"""The seams where the pattern puts them, read from the model's own construction.

Each seam comes from the rules (TARGET.md O12 and the pattern), never from the target's seam lines:
- jumper side seams: the extreme of each body section at the side, hem to underarm (O12);
- the hem edge and the rib top: the jumper's outline round the body at those heights;
- shoulder seams: along the top of the shoulder from the neck point to the cross-back end (J08-J10);
- armholes: where the surface crosses the plane x = +-cross back / 2, above the underarm (O12);
- sleeve underarm seams: the extreme of each sleeve section toward the body, cap height to cuff;
- cuff edges: the sleeve's section at the wrist plane;
- the neck rib seam: the foot of the rib, on the pattern's neckline (J10-J12);
- trousers: outseams at the outer extreme of each section from the hem to the band top, inseams
  at the inner extreme from the hem to the fork, the hems on the hem plane, the waistband's
  edges, and the crotch seam on x = 0 (O12).
"""
import math

import numpy as np


def outer_ring(Q, c, bins=144):
    """The outermost point of a set of points in each angle bin about c (x, y): an outline round."""
    ang = np.arctan2(Q[:, 1] - c[1], Q[:, 0] - c[0])
    r = np.hypot(Q[:, 0] - c[0], Q[:, 1] - c[1])
    edges = np.linspace(-math.pi, math.pi, bins + 1)
    out = []
    for a, b in zip(edges[:-1], edges[1:]):
        s = (ang >= a) & (ang < b)
        if s.any():
            out.append(Q[s][np.argmax(r[s])])
    return np.array(out)


def extreme(r, sgn, flat=0.002):
    """A section's extreme on one side: the middle of the points within `flat` of the farthest,
    so the seam does not jump from front to back along a flat side."""
    x = r[:, 0] * sgn
    m = x >= x.max() - flat
    return r[m].mean(0)


def band_ring(V, z, tol, keep=None):
    m = np.abs(V[:, 2] - z) < tol
    if keep is not None:
        m &= keep(V)
    Q = V[m]
    return outer_ring(Q, Q[:, :2].mean(0))


def plane_cut(V, F, x0, z_min):
    """Points where the surface's edges cross the plane x = x0, above z_min: its outermost loop."""
    E = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
    a, b = V[E[:, 0], 0] - x0, V[E[:, 1], 0] - x0
    m = (a * b) < 0
    t = a[m] / (a[m] - b[m])
    P = V[E[m, 0]] + t[:, None] * (V[E[m, 1]] - V[E[m, 0]])
    P = P[P[:, 2] >= z_min]
    if len(P) == 0:
        return P
    c = np.array([P[:, 1].mean(), P[:, 2].mean()])
    Q = outer_ring(P[:, [1, 2]], c, 72)
    return np.c_[np.full(len(Q), x0), Q]


def jumper_seams(P, JV, JF, sleeves, neckline_z, body_rings, rib_foot):
    S = {}
    z_hem, z_rib = P["jumper_hem_z"], P["jumper_hem_z"] + P["jumper_rib_m"]
    z_under = P["jumper_underarm_z"]
    xb = P["cross_back_m"] / 2
    R = body_rings[(body_rings[:, 0, 2] >= z_hem - 1e-6) & (body_rings[:, 0, 2] <= z_under + 1e-6)]
    half = np.abs(R[..., 0]).max() + 0.005
    body_x = lambda X: np.abs(X[:, 0]) < half
    for side, sgn in (("L", 1), ("R", -1)):
        S["side_seam_" + side] = np.array([r[np.argmax(r[:, 0] * sgn)] for r in R])
        y0, y1 = P["neck_point"][1], P["shoulder_point"][1]
        sh = []
        for x in np.linspace(P["neck_point"][0] + 0.006, xb, 24):
            y = y0 + (y1 - y0) * (x - P["neck_point"][0]) / (xb - P["neck_point"][0])
            m = (np.abs(JV[:, 0] - sgn * x) < 0.004) & (np.abs(JV[:, 1] - y) < 0.006) & (JV[:, 2] > 1.5)
            if m.any():
                sh.append(JV[m][np.argmax(JV[m][:, 2])])
        S["shoulder_seam_" + side] = np.array(sh)
        S["armhole_seam_" + side] = plane_cut(JV, JF, sgn * xb, z_under - 0.005)
        Rs = sleeves[side]
        k0 = int(round((P["sleeve_seam_from_s"] - P["sleeve_s_top"]) / 0.01))
        # toward the body, on the sleeve's visible part (not where it runs into the jumper's body)
        zs_b = R[:, 0, 2]
        und = []
        for r in Rs[k0:]:
            hw = half if r[:, 2].mean() < zs_b.min() else np.abs(R[int(np.argmin(np.abs(zs_b - r[:, 2].mean())))][:, 0]).max()
            v = r[np.abs(r[:, 0]) > hw + 0.005] if r[:, 2].mean() <= z_under + 0.08 else r
            if len(v):
                und.append(extreme(v, -sgn))
        S["sleeve_underarm_seam_" + side] = np.array(und)
        S["cuff_edge_" + side] = Rs[-1]
    S["neck_rib_seam"] = rib_foot
    S["hem_edge"] = band_ring(JV, JV[:, 2].min() + 0.002, 0.003, body_x)
    S["hem_rib_top"] = band_ring(JV, z_rib, 0.003, body_x)
    return S


def trouser_seams(P, TV, TF, legs, seat):
    S = {}
    zb, zf = P["trouser_hem_back_z"], P["trouser_hem_front_z"]
    z_fork, z_seat = P["trouser_crotch_z"], P["trouser_seat_line_z"]
    zd = P.get("hem_drop_m", 0.0)
    hem0 = np.array(legs["L"][-1])
    ybk, yfr = hem0[:, 1].max(), hem0[:, 1].min()
    hem_z = lambda y: zb - zd + (zf - zb) * np.clip((ybk - y) / (ybk - yfr), 0, 1)
    seat_up = [r for r in seat if r[0, 2] >= z_seat - 1e-6]
    for side, sgn in (("L", 1), ("R", -1)):
        L = [np.asarray(r) for r in legs[side]]
        out, ins = [], []
        for r in L[::-1]:
            z = r[0, 2]
            po = extreme(r, sgn)
            pi = extreme(r, -sgn)
            if po[2] >= hem_z(po[1]) - 1e-6:
                out.append(po)
            if z <= z_fork + 1e-6 and pi[2] >= hem_z(pi[1]) - 1e-6:
                ins.append(pi)
        out += [extreme(r, sgn) for r in seat_up if r[0, 2] <= P["trouser_waist_z"] + 1e-6]
        S["outseam_" + side] = np.array(out)
        S["inseam_" + side] = np.array(ins)
        on = (TV[:, 0] * sgn > 0.02) & (np.abs(TV[:, 2] - hem_z(TV[:, 1])) < 0.003) & (TV[:, 2] < 0.12)
        Q = TV[on]
        S["hem_" + side] = outer_ring(Q, Q[:, :2].mean(0), 72)
    S["waistband_lower_edge"] = band_ring(TV, P["waistband_lower_z"], 0.003)
    S["waistband_top_edge"] = band_ring(TV, TV[:, 2].max() - 0.002, 0.003)
    cut = plane_cut(TV, TF, 0.0, z_fork - 0.005)
    S["crotch_seam_front_to_back"] = cut[cut[:, 2] <= P["waistband_lower_z"] + 0.001]
    return S
