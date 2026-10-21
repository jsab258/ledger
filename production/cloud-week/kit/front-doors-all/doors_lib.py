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


def annulus_loft(outer, inner, y0, y1):
    """A closed ring-shaped solid (the cutter of a groove) between two counter-clockwise (x, z) rings of the same vertex count, from y0 to y1 (y1 > y0; mm): returns (V, F)
    with the faces turned outward (the signed volume is checked, so the boolean sees a proper solid)."""
    n = len(outer)
    if len(inner) != n:
        raise ValueError("annulus_loft: the two rings need the same vertex count (%d, %d)" % (n, len(inner)))
    rings = [(outer, y0), (inner, y0), (inner, y1), (outer, y1)]
    V = np.array([(x, y, z) for pts, y in rings for (x, z) in pts], float)
    F = []
    for r in range(4):
        s = (r + 1) % 4
        for i in range(n):
            j = (i + 1) % n
            F.append((r * n + i, r * n + j, s * n + j, s * n + i))
    vol = 0.0
    for f in F:
        a, b, c, d = (V[k] for k in f)
        vol += float(a @ np.cross(b, c) + a @ np.cross(c, d))
    if vol < 0:
        F = [tuple(reversed(f)) for f in F]
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


# ------------------------------------------------------------------ a small stroke font (no real typeface): digits as strokes with round bowls, rounded ends
# Each digit is a list of polylines in a box 0..1 wide and 0..1 high (z up). The strokes are buffered by half the stroke width. Round bowls (the first build's digits were
# square, in the seven-segment look of a digital display, which the street and close reviews of 13 October both named): 2 with a curved neck, 3 with two round bowls,
# 4 closed with a diagonal, 5 and 6 and 9 with a round bowl, 8 with two loops, 0 an oval.
def _arc(cx, cz, rx, rz, a0, a1, n=14):
    """Points of an elliptical arc in the unit box, from angle a0 to a1 (degrees, counter-clockwise from +x; a1 < a0 runs clockwise)."""
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cz + rz * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


_G = {
    "0": [_arc(0.5, 0.5, 0.5, 0.5, 0, 360, 28)],
    "1": [[(0.12, 0.76), (0.58, 1.0), (0.58, 0.0)]],
    "2": [_arc(0.5, 0.72, 0.42, 0.28, 160, -40, 14) + [(0.08, 0.0), (0.92, 0.0)]],
    "3": [_arc(0.5, 0.75, 0.40, 0.25, 150, -90, 12) + _arc(0.5, 0.25, 0.44, 0.25, 90, -150, 12)],
    "4": [[(0.66, 1.0), (0.04, 0.30), (0.96, 0.30)], [(0.66, 1.0), (0.66, 0.0)]],
    "5": [[(0.88, 1.0), (0.18, 1.0), (0.12, 0.56)] + _arc(0.47, 0.31, 0.43, 0.31, 115, -150, 14)],
    "6": [_arc(0.50, 0.52, 0.42, 0.46, 50, 180, 14) + [(0.08, 0.30)], _arc(0.5, 0.30, 0.42, 0.30, 0, 360, 24)],       # 14 Oct (try 3, close review 5): the stem runs straight down into the bowl's leftmost point (0.08, 0.30): no nick where the two met
    "7": [[(0.06, 1.0), (0.94, 1.0), (0.36, 0.0)]],
    "8": [_arc(0.5, 0.75, 0.34, 0.25, 0, 360, 22), _arc(0.5, 0.25, 0.42, 0.25, 0, 360, 24)],
}
_G["9"] = [[(1.0 - x, 1.0 - z) for x, z in line] for line in _G["6"]]


def digit_polygon(ch, w, h, stroke, cx=0.0, cz=0.0):
    """A digit as a shapely polygon of width w and height h (mm), centred on (cx, cz); the strokes are `stroke` wide."""
    strokes = []
    r = stroke / 2.0
    for line in _G[ch]:
        pts = [(cx - w / 2.0 + r + (px) * (w - 2 * r), cz - h / 2.0 + r + py * (h - 2 * r)) for px, py in line]
        strokes.append(LineString(pts).buffer(r, resolution=3, cap_style=1, join_style=1))
    return unary_union(strokes).simplify(0.04, preserve_topology=True)


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


# ------------------------------------------------------------------ a round bar along z (a grip), straight or bowed
def tube_z(length, radius, yc_of_z=None, y0=0.0, m=20, cap_n=4, zc=0.0):
    """A round bar along z of the given length (its two ends hemispheres, so `length` is the overall length), centre line at y = y0 + yc_of_z(z) (z measured from the bar's
    middle), centred at z = zc. Returns (V, F) in mm: closed, (x, y, z) with the same axes as the kit (y into the wall)."""
    r = radius
    half = length / 2.0
    rings = []
    for j in range(cap_n + 1):                                   # the lower cap from the apex up to the full radius
        ph = math.radians(90.0 * (1.0 - j / float(cap_n)))
        rings.append((-half + r - r * math.sin(ph), r * math.cos(ph)))
    n_mid = 12
    for i in range(1, n_mid):
        rings.append((-half + r + (length - 2 * r) * i / n_mid, r))
    for j in range(cap_n + 1):
        ph = math.radians(90.0 * (j / float(cap_n)))
        rings.append((half - r + r * math.sin(ph), r * math.cos(ph)))
    V, idx = [], []
    for z, rad in rings:
        yc = y0 + (yc_of_z(z) if yc_of_z else 0.0)
        if rad < 1e-6:
            V.append((0.0, yc, zc + z))
            idx.append([len(V) - 1])
        else:
            ids = []
            for k in range(m):
                a = 2 * math.pi * k / m
                V.append((rad * math.cos(a), yc + rad * math.sin(a), zc + z))
                ids.append(len(V) - 1)
            idx.append(ids)
    F = []
    for a, b in zip(idx[:-1], idx[1:]):
        for k in range(m):
            k1 = (k + 1) % m
            if len(a) == 1:
                F.append((a[0], b[k1], b[k]))
            elif len(b) == 1:
                F.append((a[k], a[k1], b[0]))
            else:
                F.append((a[k], a[k1], b[k1], b[k]))
    return np.array(V, float), F
