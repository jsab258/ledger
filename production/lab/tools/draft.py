"""A tailor's draft as code: named points, each made by one written rule, every rule checkable.

Units are inches, as the period manuals draft; x to the right, y DOWN (the
tailor squares down from the top), so a draft reads the way the book's diagram does.

    d = Draft("forepart", measures)
    d.at("O", 0, 0, step="F1")
    d.down("1", "O", d.m.breast / 4, step="F2", rule="O to 1 = 1/4 breast")
    ...
    d.check()   # every recorded rule re-measured from the finished points

Each point carries the book's step id and its rule as printed; check() measures
the finished geometry again and reports any rule it no longer satisfies.
"""
import math
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Rule:
    point: str
    step: str
    text: str
    kind: str            # at, down, up, left, right, along, dist, intersect, onx, ony
    args: tuple
    value: float = None


class Measures(dict):
    __getattr__ = dict.__getitem__


@dataclass
class Draft:
    name: str
    m: Measures
    P: dict = field(default_factory=dict)
    rules: list = field(default_factory=list)
    curves: dict = field(default_factory=dict)

    # --- making points -------------------------------------------------------
    def _set(self, name, x, y, rule):
        self.P[name] = np.array([float(x), float(y)])
        self.rules.append(rule)
        return self.P[name]

    def at(self, name, x, y, step="", rule=""):
        return self._set(name, x, y, Rule(name, step, rule, "at", (x, y)))

    def down(self, name, frm, dist, step="", rule=""):
        p = self.P[frm]
        return self._set(name, p[0], p[1] + dist, Rule(name, step, rule, "down", (frm,), dist))

    def up(self, name, frm, dist, step="", rule=""):
        p = self.P[frm]
        return self._set(name, p[0], p[1] - dist, Rule(name, step, rule, "up", (frm,), dist))

    def right(self, name, frm, dist, step="", rule=""):
        p = self.P[frm]
        return self._set(name, p[0] + dist, p[1], Rule(name, step, rule, "right", (frm,), dist))

    def left(self, name, frm, dist, step="", rule=""):
        p = self.P[frm]
        return self._set(name, p[0] - dist, p[1], Rule(name, step, rule, "left", (frm,), dist))

    def along(self, name, frm, to, dist, step="", rule=""):
        """dist from `frm` toward `to` (negative: beyond frm, away from to)."""
        a, b = self.P[frm], self.P[to]
        u = (b - a) / np.linalg.norm(b - a)
        p = a + u * dist
        return self._set(name, p[0], p[1], Rule(name, step, rule, "along", (frm, to), dist))

    def beyond(self, name, frm, through, dist, step="", rule=""):
        """dist past `through` on the line frm->through."""
        a, b = self.P[frm], self.P[through]
        u = (b - a) / np.linalg.norm(b - a)
        p = b + u * dist
        return self._set(name, p[0], p[1], Rule(name, step, rule, "beyond", (frm, through), dist))

    def circle_line(self, name, centre, radius, a, b, pick="near_b", step="", rule=""):
        """Point on line a-b at `radius` from `centre` (sweeping a tape from a point)."""
        c, A, B = self.P[centre], self.P[a], self.P[b]
        d = B - A
        f = A - c
        qa, qb, qc = d @ d, 2 * f @ d, f @ f - radius ** 2
        disc = qb * qb - 4 * qa * qc
        if disc < 0:
            raise ValueError("%s: no intersection" % name)
        ts = [(-qb - math.sqrt(disc)) / (2 * qa), (-qb + math.sqrt(disc)) / (2 * qa)]
        pts = [A + t * d for t in ts]
        p = min(pts, key=lambda q: np.linalg.norm(q - B)) if pick == "near_b" else min(pts, key=lambda q: np.linalg.norm(q - A))
        return self._set(name, p[0], p[1], Rule(name, step, rule, "dist", (centre,), radius))

    def intersect(self, name, a1, a2, b1, b2, step="", rule=""):
        A, B, C, D = (self.P[k] for k in (a1, a2, b1, b2))
        r, s = B - A, D - C
        den = r[0] * s[1] - r[1] * s[0]
        t = ((C - A)[0] * s[1] - (C - A)[1] * s[0]) / den
        p = A + t * r
        return self._set(name, p[0], p[1], Rule(name, step, rule, "intersect", (a1, a2, b1, b2)))

    def onx(self, name, x_of, y_of, step="", rule=""):
        """x of one point, y of another: where a square line from each meets."""
        return self._set(name, self.P[x_of][0], self.P[y_of][1], Rule(name, step, rule, "onx", (x_of, y_of)))

    # --- curves ---------------------------------------------------------------
    def curve(self, name, pts, tangents=None, n=24):
        """A smooth curve through named points (Catmull-Rom, or Hermite with given
        unit tangents at the ends as {point: (dx, dy)}), stored as a polyline."""
        P = [self.P[k] for k in pts]
        tangents = tangents or {}
        T = []
        for i, k in enumerate(pts):
            if k in tangents:
                t = np.array(tangents[k], float)
                seg = np.linalg.norm(P[min(i + 1, len(P) - 1)] - P[max(i - 1, 0)])
                T.append(t / np.linalg.norm(t) * seg * (0.5 if 0 < i < len(P) - 1 else 1.0))
            elif 0 < i < len(P) - 1:
                T.append((P[i + 1] - P[i - 1]) / 2)
            elif i == 0:
                T.append(P[1] - P[0])
            else:
                T.append(P[-1] - P[-2])
        out = []
        for i in range(len(P) - 1):
            p0, p1, m0, m1 = P[i], P[i + 1], T[i], T[i + 1]
            for s in np.linspace(0, 1, n, endpoint=False):
                h00, h10 = 2 * s ** 3 - 3 * s ** 2 + 1, s ** 3 - 2 * s ** 2 + s
                h01, h11 = -2 * s ** 3 + 3 * s ** 2, s ** 3 - s ** 2
                out.append(h00 * p0 + h10 * m0 + h01 * p1 + h11 * m1)
        out.append(P[-1])
        self.curves[name] = np.array(out)
        return self.curves[name]

    def line(self, name, pts):
        self.curves[name] = np.array([self.P[k] for k in pts])
        return self.curves[name]

    def outline(self, parts):
        """Join curves/lines (names, optionally reversed with a leading '-') into one closed polyline."""
        seq = []
        for c in parts:
            pts = self.curves[c.lstrip("-")]
            pts = pts[::-1] if c.startswith("-") else pts
            if seq and np.allclose(seq[-1], pts[0], atol=1e-6):
                pts = pts[1:]
            seq.extend(pts)
        if np.allclose(seq[0], seq[-1], atol=1e-6):
            seq = seq[:-1]
        return np.array(seq)

    # --- the check ----------------------------------------------------------------
    def check(self, tol=1 / 32):
        """Re-measure every rule on the finished points. Returns failures."""
        bad = []
        for r in self.rules:
            p = self.P[r.point]
            if r.kind in ("down", "up", "left", "right"):
                q = self.P[r.args[0]]
                got = {"down": p[1] - q[1], "up": q[1] - p[1], "right": p[0] - q[0], "left": q[0] - p[0]}[r.kind]
                off = abs(p[0] - q[0]) if r.kind in ("down", "up") else abs(p[1] - q[1])
                if abs(got - r.value) > tol or off > tol:
                    bad.append((r.step, r.point, r.text, r.value, got))
            elif r.kind in ("along", "dist"):
                q = self.P[r.args[0]]
                got = float(np.linalg.norm(p - q))
                if abs(got - abs(r.value)) > tol:
                    bad.append((r.step, r.point, r.text, r.value, got))
            elif r.kind == "beyond":
                q = self.P[r.args[1]]
                got = float(np.linalg.norm(p - q))
                if abs(got - abs(r.value)) > tol:
                    bad.append((r.step, r.point, r.text, r.value, got))
        return bad


def frac(s):
    """'1/4' or '1 1/2' -> float."""
    s = s.strip()
    if " " in s:
        a, b = s.split()
        return float(a) + frac(b)
    if "/" in s:
        a, b = s.split("/")
        return float(a) / float(b)
    return float(s)
