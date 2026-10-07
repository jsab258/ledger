"""Place flat pattern pieces round a body before sewing: each piece is bent onto
an elliptic cylinder (torso) or a round one (sleeve, collar) just outside the body.

    P3 = wrap_torso(V2_cm, anchor_u_cm, theta0, centre_xy, radii_xy, z_top, gap, direction)

V2 is the flat piece (x right, y down, centimetres, as the draft draws it).
`anchor_u_cm` is the x of the piece's line that sits at angle theta0 (the
centre-front or centre-back line); u = x - anchor is laid round the ellipse by
arc length (positive u goes toward `direction` = +1 counter-clockwise seen from
above, -1 clockwise). z falls from z_top as y grows. Lengths along the girth are
kept by walking the ellipse's arc length, so a piece is bent, not stretched.
"""
import math

import numpy as np


def _ellipse_table(a, b, n=4000):
    t = np.linspace(-math.pi, math.pi, n + 1)
    x, y = a * np.cos(t), b * np.sin(t)
    s = np.concatenate([[0], np.cumsum(np.hypot(np.diff(x), np.diff(y)))])
    return t, s


def wrap_torso(V2, anchor_u, theta0, centre, radii, z_top, gap=0.02, direction=1, z_scale=1.0):
    """Returns (n,3) metres. theta measured from +x toward +y (Blender: -y is the front, so
    the centre front is theta = -pi/2 and the centre back +pi/2)."""
    a, b = radii[0] + gap, radii[1] + gap
    t, s = _ellipse_table(a, b)
    s0 = np.interp(theta0, t, s)
    u = (V2[:, 0] - anchor_u) / 100.0 * direction
    sp = s0 + u
    total = s[-1]
    sp = np.mod(sp - s[0], total) + s[0]
    th = np.interp(sp, s, t)
    x = centre[0] + a * np.cos(th)
    y = centre[1] + b * np.sin(th)
    z = z_top - V2[:, 1] / 100.0 * z_scale
    return np.stack([x, y, z], 1)


def wrap_tube(V2, anchor_u, axis_p0, axis_p1, radius, theta0=0.0, direction=1, ref=(0, -1, 0), v_from_p0=True):
    """A sleeve or collar round a straight axis from p0 to p1. The piece's x
    becomes the girth (u = x - anchor at angle theta0 from `ref`), its y runs
    along the axis from p0 (centimetres)."""
    p0, p1 = np.asarray(axis_p0, float), np.asarray(axis_p1, float)
    ax = (p1 - p0) / np.linalg.norm(p1 - p0)
    r0 = np.asarray(ref, float)
    e1 = r0 - ax * (r0 @ ax)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(ax, e1)
    th = theta0 + direction * (V2[:, 0] - anchor_u) / 100.0 / radius
    along = V2[:, 1] / 100.0
    pts = p0[None, :] + along[:, None] * ax[None, :] + radius * (np.cos(th)[:, None] * e1 + np.sin(th)[:, None] * e2)
    return pts


def torso_ellipse(body_V, z, band=0.01, xmax=0.26):
    """The body's torso at height z: centre and half-widths (x, y) from vertices in a band."""
    S = body_V[(np.abs(body_V[:, 2] - z) < band) & (np.abs(body_V[:, 0]) < xmax)]
    cx, cy = (S[:, 0].max() + S[:, 0].min()) / 2, (S[:, 1].max() + S[:, 1].min()) / 2
    return (cx, cy), ((S[:, 0].max() - S[:, 0].min()) / 2, (S[:, 1].max() - S[:, 1].min()) / 2)


def fold_2d(V2, p0, p1, region, r=0.8):
    """Turn a region of a flat piece over a line, as a lapel turns on its roll line.

    p0, p1: two points on the fold line (cm, flat-pattern space); region: boolean
    mask of the vertices on the side that turns over. Within pi*r of the line
    the cloth rolls round a half cylinder of radius r (cm); beyond it the cloth
    lies flat, mirrored back over the piece, 2r above it. Returns the new flat
    positions and each vertex's height above the piece (cm), to be added along
    the outward normal after wrapping. The rest shape so made keeps the roll."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    t = (p1 - p0) / np.linalg.norm(p1 - p0)
    n = np.array([-t[1], t[0]])
    rel = V2 - p0
    d = rel @ n
    s = rel @ t
    # n must point into the region
    if region.any() and np.median(d[region]) < 0:
        n, d = -n, -d
    out = V2.copy()
    h = np.zeros(len(V2))
    sel = region & (d > 0)
    phi = np.clip(d[sel] / r, 0, math.pi)
    roll = d[sel] <= math.pi * r
    dn = np.where(roll, r * np.sin(phi), -(d[sel] - math.pi * r))
    hh = np.where(roll, r * (1 - np.cos(phi)), 2 * r)
    out[sel] = p0 + np.outer(s[sel], t) + np.outer(dn, n)
    h[sel] = hh
    return out, h


def push_out(P3, h_cm, centre_xy):
    """Move wrapped points outward from the torso's axis by h (cm)."""
    radial = P3[:, :2] - np.asarray(centre_xy)[None, :]
    radial /= np.linalg.norm(radial, axis=1, keepdims=True)
    Q = P3.copy()
    Q[:, :2] += radial * (h_cm / 100.0)[:, None]
    return Q
