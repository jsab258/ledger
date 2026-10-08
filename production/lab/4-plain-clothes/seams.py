"""The seams where the pattern puts them, laid on the modelled surfaces.

Each seam is found from the pattern's own construction, never from the target's seam lines:
- jumper side seams: front and back pieces are equal widths (pattern J03), so at each height
  the side seam is halfway round the jumper between the centre front and the centre back;
- the hem edge and the rib top at their levels;
- shoulder seams: from the neck point (half the neck width, J10) to the end of the cross back
  (J08) along the top of the shoulder;
- armholes: straight down from the cross-back end to the armhole's step line (the lower third
  of the armhole depth, J13), then a quarter curve out to the underarm on the side seam;
- sleeve underarm seams: along the sleeve's inner side from its underarm to the cuff; cuff edges;
- the neck rib seam: the neckline round the neck (back neck, neck points, front neck);
- trousers: side seams (outseam) plumb on the leg's outer side and up the hip to the waist,
  inside leg seams from the fork to the hem, the hems, the waistband's edges, and the crotch
  seam down the centre front, through the fork and up the centre back.
"""
import math

import numpy as np
from scipy.spatial import cKDTree


def ring_crossings(R):
    """Centre front and centre back of a horizontal ring: where it crosses x = 0 (front y < 0)."""
    out = {}
    n = len(R)
    for i in range(n):
        a, b = R[i], R[(i + 1) % n]
        if (a[0] <= 0 < b[0]) or (b[0] <= 0 < a[0]):
            t = a[0] / (a[0] - b[0])
            p = a + t * (b - a)
            out["front" if p[1] < 0 else "back"] = (i, t, p)
    return out


def half_way_side(R, sgn):
    """The point halfway round a ring from centre front to centre back, on the side sgn."""
    c = ring_crossings(R)
    if "front" not in c or "back" not in c:
        return None
    n = len(R)
    i0 = c["front"][0]
    # walk from the centre front toward the side with x * sgn > 0
    step = 1 if R[(i0 + 1) % n][0] * sgn > 0 else -1
    pts = [c["front"][2]]
    j = (i0 + 1) % n if step == 1 else i0
    for _ in range(n):
        pts.append(R[j])
        if np.sign(R[j][0]) != np.sign(sgn) and len(pts) > 3:
            break
        j = (j + step) % n
    pts[-1] = c["back"][2]
    P = np.array(pts)
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    h = s[-1] / 2
    k = int(np.searchsorted(s, h)) - 1
    t = (h - s[k]) / max(s[k + 1] - s[k], 1e-12)
    return P[k] + t * (P[k + 1] - P[k])


def on_surface(V, pts):
    return V[cKDTree(V).query(pts)[1]]


def band(V, z, tol=0.004, mask=None):
    m = np.abs(V[:, 2] - z) < tol
    if mask is not None:
        m &= mask
    Q = V[m]
    if len(Q) == 0:
        return Q
    c = Q.mean(0)
    order = np.argsort(np.arctan2(Q[:, 1] - c[1], Q[:, 0] - c[0]))
    return Q[order]


def surface_section(V, z, tol=0.003):
    """The jumper surface's outline at a height, ordered round (for the side seams)."""
    Q = V[np.abs(V[:, 2] - z) < tol]
    c = Q.mean(0)
    ang = np.arctan2(Q[:, 1] - c[1], Q[:, 0] - c[0])
    bins = np.linspace(-math.pi, math.pi, 145)
    R = []
    for a, b in zip(bins[:-1], bins[1:]):
        s = Q[(ang >= a) & (ang < b)]
        if len(s):
            d = np.hypot(s[:, 0] - c[0], s[:, 1] - c[1])
            R.append(s[np.argmax(d)])            # the outer surface
    return np.array(R)


def plane_cut(V, F, x0, z_min):
    """Points where the surface's edges cross the plane x = x0, above z_min, ordered round."""
    E = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
    a, b = V[E[:, 0], 0] - x0, V[E[:, 1], 0] - x0
    m = (a * b) < 0
    t = a[m] / (a[m] - b[m])
    P = V[E[m, 0]] + t[:, None] * (V[E[m, 1]] - V[E[m, 0]])
    P = P[P[:, 2] >= z_min]
    if len(P) == 0:
        return P
    c = P[:, 1:].mean(0)
    return P[np.argsort(np.arctan2(P[:, 2] - c[1], P[:, 1] - c[0]))]


def jumper_seams(P, JV, JF, sleeves, neckline_z, body_rings):
    S = {}
    z_hem, z_rib = P["jumper_hem_z"], P["jumper_hem_z"] + P["jumper_rib_m"]
    z_under = P["jumper_underarm_z"]
    xb = P["cross_back_m"] / 2
    z_step = P["neck_point"][2] - (P["shoulder_drop_m"] + P["armhole_depth_m"] * (1 - 1 / 3))
    for side, sgn in (("L", 1), ("R", -1)):
        # side seams at the body section's extreme (O12), laid on the surface
        R = body_rings[(body_rings[:, 0, 2] >= z_hem - 1e-6) & (body_rings[:, 0, 2] <= z_under + 1e-6)]
        S["side_seam_" + side] = on_surface(JV, np.array([r[np.argmax(r[:, 0] * sgn)] for r in R]))
        # shoulder seam: the top of the surface along the line from the neck point to the cross-back end
        y0, y1 = P["neck_point"][1], P["shoulder_point"][1]
        sh = []
        for x in np.linspace(P["neck_point"][0] + 0.006, xb, 24):
            y = y0 + (y1 - y0) * (x - P["neck_point"][0]) / (xb - P["neck_point"][0])
            m = (np.abs(JV[:, 0] - sgn * x) < 0.004) & (np.abs(JV[:, 1] - y) < 0.006) & (JV[:, 2] > 1.5)
            if m.any():
                sh.append(JV[m][np.argmax(JV[m][:, 2])])
        S["shoulder_seam_" + side] = np.array(sh)
        # armhole: where the surface crosses the plane x = +-cross back / 2, above the underarm (O12)
        S["armhole_seam_" + side] = plane_cut(JV, JF, sgn * xb, z_under - 0.005)
        # the sleeve: underarm seam along the inner side, the cuff edge
        R = sleeves[side]
        s0 = P["sleeve_seam_from_s"]
        k0 = int(round((s0 - P["sleeve_s_top"]) / 0.01))
        S["sleeve_underarm_seam_" + side] = on_surface(JV, np.array([r[np.argmin(r[:, 0] * sgn)] for r in R[k0:]]))
        S["cuff_edge_" + side] = on_surface(JV, R[-1])
    # the neck rib seam: round the neck, at the neckline's height, the surface point nearest the neck
    cb, npnt, cf = P["neck_back"], P["neck_point"], P["neck_front"]
    yc = 0.5 * (cb[1] + cf[1])
    ry = 0.5 * (cb[1] - cf[1])
    e = np.hypot(JV[:, 0] / npnt[0], (JV[:, 1] - yc) / ry)
    m = (e < 1.6) & (np.abs(JV[:, 2] - neckline_z(JV)) < 0.004)
    Q, eq = JV[m], e[m]
    ang = np.arctan2(Q[:, 0] / npnt[0], (Q[:, 1] - yc) / ry)
    neck = []
    for a0 in np.linspace(-math.pi, math.pi, 73)[:-1]:
        sel = np.abs(((ang - a0 + math.pi) % (2 * math.pi)) - math.pi) < math.pi / 72
        if sel.any():
            neck.append(Q[sel][np.argmin(eq[sel])])
    S["neck_rib_seam"] = np.array(neck)
    # the hem edge and the rib top: rings of the body (not the cuffs, which hang at the same height)
    def body_band(z, tol):
        r = body_rings[int(np.argmin(np.abs(body_rings[:, 0, 2] - z)))]
        Q = JV[np.abs(JV[:, 2] - z) < tol]
        d = cKDTree(r[:, :2]).query(Q[:, :2])[0]
        Q = Q[d < 0.02]
        c = Q.mean(0)
        return Q[np.argsort(np.arctan2(Q[:, 1] - c[1], Q[:, 0] - c[0]))]
    S["hem_edge"] = body_band(JV[:, 2].min() + 0.002, 0.003)
    S["hem_rib_top"] = body_band(z_rib, 0.003)
    return S


def trouser_seams(P, TV, leg_rings, seat_rings):
    S = {}
    zb, zf = P["trouser_hem_back_z"], P["trouser_hem_front_z"]
    z_fork = P["trouser_crotch_z"]
    for side, sgn in (("L", 1), ("R", -1)):
        L = leg_rings[side]
        out, ins = [], []
        for z in np.arange(zf + 0.004, P["waistband_lower_z"] + 1e-6, 0.005):
            Q = TV[(np.abs(TV[:, 2] - z) < 0.003)]
            Qs = Q[Q[:, 0] * sgn > 0]
            if len(Qs) < 5:
                continue
            out.append(Qs[np.argmax(Qs[:, 0] * sgn)])
            if z <= z_fork:
                ins.append(Qs[np.argmin(Qs[:, 0] * sgn)])
        S["outseam_" + side] = np.array(out)
        S["inseam_" + side] = np.array(ins)
        side_m = TV[:, 0] * sgn > 0.02
        hemz = TV[:, 2] - (zb + (zf - zb) * np.clip((L[-1][:, 1].max() - TV[:, 1]) / (L[-1][:, 1].max() - L[-1][:, 1].min()), 0, 1))
        S["hem_" + side] = TV[side_m & (np.abs(hemz) < 0.004) & (TV[:, 2] < 0.12)]
    S["waistband_lower_edge"] = band(TV, P["waistband_lower_z"], 0.003)
    S["waistband_top_edge"] = band(TV, TV[:, 2].max() - 0.002, 0.003)
    m = (np.abs(TV[:, 0]) < 0.003) & (TV[:, 2] > z_fork - 0.02) & (TV[:, 2] < P["waistband_lower_z"] + 0.001)
    Q = TV[m]
    c = np.array([Q[:, 1].mean(), Q[:, 2].max()])
    order = np.argsort(np.arctan2(Q[:, 1] - c[0], -(Q[:, 2] - c[1])))
    S["crotch_seam_front_to_back"] = Q[order]
    return S
