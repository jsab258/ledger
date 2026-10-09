"""Profile builders for the shopfront target. Every function returns a list of [a, b] points in
millimetres. Profiles are closed polygons (the last point joins the first), wound counter-clockwise
with the first axis to the right and the second up, unless a note says otherwise.

Section planes used in target.json:
  "d-z"  d = distance OUT from the wall face (positive toward the street), z = up. A side section.
  "u-d"  u = across the part (viewer's left to right), d = out from the wall. A plan section.
  "a-p"  a = along a bead's face, p = proud of the member it is planted on. A small moulding.
  "u-z"  an elevation (the face seen from the street).
"""
import math


def r1(v):
    v = round(float(v), 2)
    return 0.0 if v == 0 else v


def pts(lst, closed=True):
    """Round to 0.01 mm. A closed outline is also de-duplicated and wound counter-clockwise."""
    lst = [tuple(p) for p in lst]
    if closed:
        lst = ccw(dedupe(lst))
    return [[r1(a), r1(b)] for a, b in lst]


def arc(cx, cz, r, a0, a1, n=8, include_end=True):
    """Points on a circle of radius r about (cx, cz), from angle a0 to a1 (degrees, 0 = +first axis,
    90 = +second axis), n segments."""
    out = []
    for k in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * k / n)
        out.append((cx + r * math.cos(a), cz + r * math.sin(a)))
    return out if include_end else out[:-1]


def dedupe(p, eps=1e-6):
    out = [p[0]]
    for q in p[1:]:
        if abs(q[0] - out[-1][0]) > eps or abs(q[1] - out[-1][1]) > eps:
            out.append(q)
    if len(out) > 1 and abs(out[0][0] - out[-1][0]) < eps and abs(out[0][1] - out[-1][1]) < eps:
        out.pop()
    return out


def area2(p):
    s = 0.0
    for i in range(len(p)):
        x0, y0 = p[i]
        x1, y1 = p[(i + 1) % len(p)]
        s += x0 * y1 - x1 * y0
    return s


def ccw(p):
    return p if area2(p) > 0 else list(reversed(p))


def bezier(p0, p1, p2, p3, n=12):
    out = []
    for k in range(n + 1):
        t = k / n
        a = (1 - t) ** 3
        b = 3 * (1 - t) ** 2 * t
        c = 3 * (1 - t) * t ** 2
        d = t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def spiral(cx, cz, r0, r1_, a0, turns, n=24):
    """An Archimedean spiral about (cx, cz): radius from r0 to r1_ over `turns` turns, starting at
    angle a0 degrees, turning counter-clockwise."""
    out = []
    for k in range(n + 1):
        t = k / n
        r = r0 + (r1_ - r0) * t
        a = math.radians(a0 + 360.0 * turns * t)
        out.append((cx + r * math.cos(a), cz + r * math.sin(a)))
    return out
