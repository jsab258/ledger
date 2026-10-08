"""Joinery shapes that are not plain prisms, as closed triangle meshes in metres.

- sweep_frame: a moulding profile run round a rectangle with mitred corners (a panel's
  stuck or planted moulding, an architrave), as one closed ring.
- fielded_panel: a panel with a flat margin, a bevel and a raised field (or a flat panel
  when the bevel is zero), on one face or both.

Coordinates: x across the door, z up, y through it (outside -y). A profile is given in
(d, t): d = distance in from the rectangle's edge toward its middle, t = depth along +y
from the reference face; polygon closed, counter-clockwise in (d, t), no repeat.
"""
import numpy as np


def sweep_frame(profile, x0, z0, x1, z1, y0):
    """Sweep `profile` round the rectangle (x0, z0)-(x1, z1), the d axis pointing inward,
    mitred at the corners. Returns (V, F)."""
    P = np.asarray(profile, float)
    n = len(P)
    # the four corners, walked anticlockwise seen from -y: bottom-left, bottom-right, top-right, top-left
    C = np.array([[x0, z0], [x1, z0], [x1, z1], [x0, z1]], float)
    inward = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]], float)     # mitre direction (diagonal)
    rings = []
    for k in range(4):
        R = np.zeros((n, 3))
        R[:, 0] = C[k, 0] + inward[k, 0] * P[:, 0]
        R[:, 2] = C[k, 1] + inward[k, 1] * P[:, 0]
        R[:, 1] = y0 + P[:, 1]
        rings.append(R)
    V = np.vstack(rings)
    F = []
    for k in range(4):
        a, b = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            F += [(a + i, b + i, b + j), (a + i, b + j, a + j)]
    return V, np.array(F)


def fielded_panel(x0, z0, x1, z1, y_back, t_margin, t_field, bevel, margin=0.0, both=False):
    """A panel spanning (x0, z0)-(x1, z1) in its frame (tongues included), its back face at
    y_back, `t_margin` thick at the edge. Seen from -y the field rises by (t_field - t_margin)
    over a bevel `bevel` wide starting `margin` in from the edge; with both=True the back is
    raised the same way. Returns (V, F), a closed mesh (normals left to the builder)."""
    rise = t_field - t_margin
    yf = y_back - t_margin

    def ring(d, y):
        return [[x0 + d, y, z0 + d], [x1 - d, y, z0 + d], [x1 - d, y, z1 - d], [x0 + d, y, z1 - d]]
    rings = [ring(0.0, yf), ring(margin, yf), ring(margin + bevel, yf - rise),
             ring(0.0, y_back), ring(margin, y_back), ring(margin + bevel, y_back + (rise if both else 0.0))]
    V = np.array([p for r in rings for p in r], float)
    F = []

    def strip(a, b):
        for i in range(4):
            j = (i + 1) % 4
            F.extend([(4 * a + i, 4 * a + j, 4 * b + j), (4 * a + i, 4 * b + j, 4 * b + i)])
    strip(0, 1); strip(1, 2); strip(3, 4); strip(4, 5); strip(0, 3)
    F.extend([(8, 9, 10), (8, 10, 11), (20, 21, 22), (20, 22, 23)])
    return V, np.array(F)


def is_closed(F):
    """Every edge shared by exactly two faces."""
    from collections import Counter
    E = Counter()
    for f in F:
        for i in range(3):
            e = tuple(sorted((int(f[i]), int(f[(i + 1) % 3]))))
            E[e] += 1
    return all(v == 2 for v in E.values())


def orient_outward(V, F):
    """Flip faces so normals point away from the mesh's centre (good enough for convex-ish solids)."""
    c = V.mean(0)
    out = []
    for f in F:
        a, b, d = V[f[0]], V[f[1]], V[f[2]]
        n = np.cross(b - a, d - a)
        out.append(f if np.dot(n, (a + b + d) / 3 - c) >= 0 else (f[0], f[2], f[1]))
    return np.array(out)
