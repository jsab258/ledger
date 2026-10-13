"""Shared geometry for the front-doors-all kit (cloud week 42, unit 9): polygons, sweeps, lofts, a small stroke font.

Everything is millimetres in the target's frame (x across from the left reveal, y into the wall with the street toward -y,
z up from the threshold's top) until a part is moved to its pivot and scaled to metres by the builder.

Nothing here touches Blender: functions return (V, F) as numpy vertices and faces (n-gons allowed) for build_door.new_obj.
"""
import math
import os
import sys

import numpy as np
from shapely.geometry import LineString, Point, Polygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "door"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import build_door as bd  # noqa: E402  (prism, box, arc, lathe and the rest of the 3.1 method)


# ------------------------------------------------------------------ polygons
def ccw(pts):
    """The points of a polygon, counter-clockwise (x right, z up, seen from the street), open ring."""
    P = [tuple(map(float, p)) for p in pts]
    if len(P) > 1 and P[0] == P[-1]:
        P = P[:-1]
    a = 0.0
    for i in range(len(P)):
        x0, z0 = P[i]
        x1, z1 = P[(i + 1) % len(P)]
        a += x0 * z1 - x1 * z0
    return P if a > 0 else P[::-1]


def rect_pts(x0, z0, x1, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def is_rect(pts, tol=1e-6):
    P = ccw(pts)
    if len(P) != 4:
        return False
    xs = sorted({round(p[0], 6) for p in P})
    zs = sorted({round(p[1], 6) for p in P})
    return len(xs) == 2 and len(zs) == 2


def offset_poly(pts, d):
    """Offset every vertex of a counter-clockwise polygon along its mitre: d > 0 moves inward, d < 0 outward. The edges move by |d| (a mitre join)."""
    P = ccw(pts)
    n = len(P)
    out = []
    for i in range(n):
        p0, p1, p2 = np.array(P[i - 1]), np.array(P[i]), np.array(P[(i + 1) % n])
        e0, e1 = p1 - p0, p2 - p1
        e0 /= np.linalg.norm(e0)
        e1 /= np.linalg.norm(e1)
        n0, n1 = np.array([-e0[1], e0[0]]), np.array([-e1[1], e1[0]])        # inward normals of a counter-clockwise polygon
        m = (n0 + n1) / (1.0 + float(n0 @ n1))
        q = p1 + d * m
        out.append((float(q[0]), float(q[1])))
    return out


def dedupe(pts, tol=1e-6):
    out = []
    for p in pts:
        if not out or math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > tol:
            out.append(p)
    if len(out) > 1 and math.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) <= tol:
        out = out[:-1]
    return out


def arc_pts(cx, cz, r, a0, a1, n):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cz + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def round_top_rect_pts(x0, z0, x1, z1, r, n=8):
    """A rectangle whose two top corners are rounded to radius r (T3's small light), counter-clockwise."""
    pts = [(x0, z0), (x1, z0), (x1, z1 - r)]
    pts += arc_pts(x1 - r, z1 - r, r, 0, 90, n)[1:]
    pts += arc_pts(x0 + r, z1 - r, r, 90, 180, n)[1:]
    pts += [(x0, z1 - r)]
    return dedupe(pts)


def segmental_rect_pts(x0, z0, x1, z1, spring, n=24):
    """A rectangle whose head is a segmental arch: the crown at z1, the springing `spring` lower (the drawing's own construction)."""
    c = (x1 - x0) / 2.0
    R = (c * c + spring * spring) / (2.0 * spring)
    cx, cz = (x0 + x1) / 2.0, z1 - R
    pts = [(x0, z0), (x1, z0), (x1, z1 - spring)]
    for i in range(1, n):
        x = x1 - (x1 - x0) * i / n
        pts.append((x, cz + math.sqrt(max(R * R - (x - cx) ** 2, 0.0))))
    pts.append((x0, z1 - spring))
    return dedupe(pts)


def raked_rect_pts(x0, z0, x1, z1, rise, toward):
    """A panel whose head is raked: `rise` lower at the outer corner than at the muntin end (toward = 'right' puts the high end at x1)."""
    if toward == "right":
        return [(x0, z0), (x1, z0), (x1, z1), (x0, z1 - rise)]
    return [(x0, z0), (x1, z0), (x1, z1 - rise), (x0, z1)]


# ------------------------------------------------------------------ solids
def sweep_poly(profile, pts, y0=0.0):
    """A moulding profile run round a counter-clockwise polygon in (x, z), mitred at every vertex, as one closed ring solid.
    profile: closed polygon of (d, t): d = distance inward from the polygon's edge, t = y (absolute, mm). Returns (V, F)."""
    P = ccw(pts)
    n = len(P)
    prof = [tuple(map(float, q)) for q in profile]
    if len(prof) > 1 and prof[0] == prof[-1]:
        prof = prof[:-1]
    m = len(prof)
    rings = []
    ms = []
    for i in range(n):
        p0, p1, p2 = np.array(P[i - 1]), np.array(P[i]), np.array(P[(i + 1) % n])
        e0, e1 = p1 - p0, p2 - p1
        e0 /= np.linalg.norm(e0)
        e1 /= np.linalg.norm(e1)
        n0, n1 = np.array([-e0[1], e0[0]]), np.array([-e1[1], e1[0]])
        ms.append((n0 + n1) / (1.0 + float(n0 @ n1)))
    V = np.zeros((n * m, 3))
    for i in range(n):
        for k, (d, t) in enumerate(prof):
            V[i * m + k] = (P[i][0] + d * ms[i][0], y0 + t, P[i][1] + d * ms[i][1])
    F = []
    for i in range(n):
        j = (i + 1) % n
        for k in range(m):
            k1 = (k + 1) % m
            F.append((i * m + k, j * m + k, j * m + k1, i * m + k1))
    return V, F


def loft_rings(rings, cap=True):
    """A closed solid through horizontal rings: rings = [(pts (x, z) counter-clockwise, y), ...], all the same vertex count. The first and last are capped."""
    n = len(rings[0][0])
    V = np.array([(x, y, z) for pts, y in rings for (x, z) in pts], float)
    F = []
    for r in range(len(rings) - 1):
        for i in range(n):
            j = (i + 1) % n
            F.append((r * n + i, r * n + j, (r + 1) * n + j, (r + 1) * n + i))
    if cap:
        F.append(tuple(range(n))[::-1])
        F.append(tuple(range((len(rings) - 1) * n, len(rings) * n)))
    return V, F


# ------------------------------------------------------------------ a small stroke font (no real typeface): digits as strokes, rounded ends
# Each digit is a list of polylines in a box 0..1 wide and 0..1 high (z up). The strokes are buffered by half the stroke width.
_G = {
    "0": [[(0.1, 0.0), (0.9, 0.0), (0.9, 1.0), (0.1, 1.0), (0.1, 0.0)]],
    "1": [[(0.25, 0.8), (0.55, 1.0), (0.55, 0.0)]],
    "2": [[(0.1, 1.0), (0.9, 1.0), (0.9, 0.55), (0.1, 0.45), (0.1, 0.0), (0.9, 0.0)]],
    "3": [[(0.1, 1.0), (0.9, 1.0), (0.9, 0.0), (0.1, 0.0)], [(0.3, 0.5), (0.9, 0.5)]],
    "4": [[(0.15, 1.0), (0.1, 0.4), (0.9, 0.4)], [(0.7, 1.0), (0.7, 0.0)]],
    "5": [[(0.9, 1.0), (0.1, 1.0), (0.1, 0.55), (0.9, 0.5), (0.9, 0.0), (0.1, 0.0)]],
    "6": [[(0.9, 1.0), (0.1, 1.0), (0.1, 0.0), (0.9, 0.0), (0.9, 0.5), (0.1, 0.5)]],
    "7": [[(0.1, 1.0), (0.9, 1.0), (0.4, 0.0)]],
    "8": [[(0.1, 0.0), (0.9, 0.0), (0.9, 1.0), (0.1, 1.0), (0.1, 0.0)], [(0.1, 0.5), (0.9, 0.5)]],
    "9": [[(0.1, 0.0), (0.9, 0.0), (0.9, 1.0), (0.1, 1.0), (0.1, 0.5), (0.9, 0.5)]],
}


def digit_polygon(ch, w, h, stroke, cx=0.0, cz=0.0):
    """A digit as a shapely polygon of width w and height h (mm), centred on (cx, cz); the strokes are `stroke` wide."""
    strokes = []
    r = stroke / 2.0
    for line in _G[ch]:
        pts = [(cx - w / 2.0 + r + (px) * (w - 2 * r), cz - h / 2.0 + r + py * (h - 2 * r)) for px, py in line]
        strokes.append(LineString(pts).buffer(r, resolution=3, cap_style=1, join_style=1))
    return unary_union(strokes)


def row_polygons(text, w, h, stroke, gap, cx, cz):
    """A row of digits centred on (cx, cz): the union polygon of each digit separately (a list)."""
    n = len(text)
    total = n * w + (n - 1) * gap
    x = cx - total / 2.0 + w / 2.0
    out = []
    for ch in text:
        out.append(digit_polygon(ch, w, h, stroke, x, cz))
        x += w + gap
    return out


def stack_polygons(text, w, h, stroke, gap, cx, zs):
    """Digits stacked one above the other (T1's two digits on the muntin): the i-th digit centred at height zs[i]."""
    return [digit_polygon(ch, w, h, stroke, cx, z) for ch, z in zip(text, zs)]


def lin(c):
    return bd.lin(c)
