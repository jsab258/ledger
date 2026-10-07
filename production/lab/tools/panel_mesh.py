"""Flat pattern pieces to even triangle meshes, for sewing in Blender's cloth.

A piece is a closed outline (x, y in centimetres, counter-clockwise or not).
Its outline is resampled at a fixed spacing, the inside filled with a
triangular lattice at the same spacing, and Delaunay-triangulated; triangles
outside the outline are dropped. Seams are sewn by matching outline stretches,
so each piece also returns the index of every outline point in order.

    V, F, ring = mesh_panel(outline_cm, spacing_cm=1.5)
"""
import numpy as np
from matplotlib.path import Path
from scipy.spatial import Delaunay


def resample_closed(P, spacing):
    P = np.asarray(P, float)
    if np.allclose(P[0], P[-1]):
        P = P[:-1]
    Q = np.vstack([P, P[:1]])
    seg = np.linalg.norm(np.diff(Q, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    n = max(8, int(round(s[-1] / spacing)))
    t = np.linspace(0, s[-1], n, endpoint=False)
    x = np.interp(t, s, Q[:, 0])
    y = np.interp(t, s, Q[:, 1])
    return np.stack([x, y], 1), t


def resample_keep_corners(P, spacing, corners):
    """Resample each stretch between named corner indices separately, so the
    corners (seam ends) stay exact vertices."""
    P = np.asarray(P, float)
    if np.allclose(P[0], P[-1]):
        P = P[:-1]
    corners = sorted(set(corners))
    out, corner_at = [], {}
    for k, c0 in enumerate(corners):
        c1 = corners[(k + 1) % len(corners)]
        idx = list(range(c0, c1 + 1)) if c1 > c0 else list(range(c0, len(P))) + list(range(0, c1 + 1))
        S = P[idx]
        seg = np.linalg.norm(np.diff(S, axis=0), axis=1)
        s = np.concatenate([[0], np.cumsum(seg)])
        n = max(1, int(round(s[-1] / spacing)))
        t = np.linspace(0, s[-1], n, endpoint=False)
        corner_at[c0] = len(out)
        for tt in t:
            out.append((np.interp(tt, s, S[:, 0]), np.interp(tt, s, S[:, 1])))
    return np.array(out), corner_at


def mesh_panel(outline, spacing=1.5, corners=None):
    if corners:
        ring, corner_at = resample_keep_corners(outline, spacing, corners)
    else:
        ring, _ = resample_closed(outline, spacing)
        corner_at = {}
    path = Path(np.vstack([ring, ring[:1]]))
    x0, y0 = ring.min(0)
    x1, y1 = ring.max(0)
    h = spacing * np.sqrt(3) / 2
    pts = []
    for j, y in enumerate(np.arange(y0 + h / 2, y1, h)):
        off = (spacing / 2) * (j % 2)
        for x in np.arange(x0 + off, x1, spacing):
            pts.append((x, y))
    pts = np.array(pts) if pts else np.zeros((0, 2))
    if len(pts):
        inside = path.contains_points(pts, radius=-spacing * 0.45)  # keep clear of the edge
        pts = pts[inside]
        # drop lattice points too near the outline
        if len(pts):
            d = np.min(np.linalg.norm(pts[:, None, :] - ring[None, :, :], axis=2), axis=1)
            pts = pts[d > spacing * 0.55]
    V = np.vstack([ring, pts])
    tri = Delaunay(V).simplices
    cen = V[tri].mean(1)
    keep = path.contains_points(cen)
    F = tri[keep]
    # orient all triangles the same way (counter-clockwise in x, y)
    # every outline vertex must belong to a triangle, or the cloth holds it by seams alone and it
    # flies off (lab test 3, run v2): a lone one is tied to its two outline neighbours
    used = np.zeros(len(V), bool)
    used[F.ravel()] = True
    extra = []
    nr = len(ring)
    for i in range(nr):
        if not used[i]:
            extra.append((i - 1) % nr)
            extra.append(i)
            extra.append((i + 1) % nr)
    if extra:
        F = np.vstack([F, np.array(extra).reshape(-1, 3)])
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    cross = (b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0])
    F[cross < 0] = F[cross < 0][:, [0, 2, 1]]
    return V, F, np.arange(len(ring)), corner_at


def stretch(ring_len, a, b):
    """Outline indices from a to b going forward (inclusive), wrapping."""
    return list(range(a, b + 1)) if b >= a else list(range(a, ring_len)) + list(range(0, b + 1))


def _selftest():
    sq = [(0, 0), (20, 0), (20, 10), (0, 10)]
    V, F, ring, ca = mesh_panel(sq, spacing=1.0, corners=[0, 1, 2, 3])
    area = 0.5 * np.abs(np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])).sum()
    assert abs(area - 200) < 1.0, area
    assert set(ca) == {0, 1, 2, 3} and len(ring) == 60, (ca, len(ring))
    print("panel_mesh selftest ok", len(V), "verts", len(F), "tris")


if __name__ == "__main__":
    _selftest()
