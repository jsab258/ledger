"""Ron's torso as a shell to lay cloth on before sewing (A-pose body, arms clear).

  hulls = Hulls()                 # 2D convex hull of the torso every centimetre of height
  P = hulls.push_out(P, gap)      # any point inside (or nearer than gap) moved out to hull + gap
  ridge(side, u)                  # the shoulder ridge, neck side (u=0) to shoulder tip (u=1)
  neck_ring(side, phi, z)         # a point round the neck
"""
import math
import os

import numpy as np
from matplotlib.path import Path
from scipy.spatial import ConvexHull

OUT = r"F:/LedgerTools/lab/jacket"


class Hulls:
    def __init__(self, path=os.path.join(OUT, "ronfull_apose.npz")):
        V = np.load(path)["LOD0_V"]
        self.V = V
        self.zs = np.arange(0.60, 1.72, 0.01)
        self.polys, self.cent = [], []
        for z in self.zs:
            xmax = 0.36 if z > 1.47 else 0.255
            if z > 1.64:
                xmax = 0.10                                   # the neck, not the shoulders' top
            S = V[(np.abs(V[:, 2] - z) < 0.006) & (np.abs(V[:, 0]) < xmax)][:, :2]
            if len(S) < 6:
                self.polys.append(self.polys[-1] if self.polys else np.zeros((3, 2)))
                self.cent.append(self.cent[-1] if self.cent else np.zeros(2))
                continue
            h = ConvexHull(S)
            P = S[h.vertices]
            self.polys.append(P)
            self.cent.append(P.mean(0))

    def push_out(self, P, gap):
        P = P.copy()
        gap = np.broadcast_to(np.asarray(gap, float), (len(P),))
        for i, p in enumerate(P):
            k = int(np.clip(round((p[2] - self.zs[0]) / 0.01), 0, len(self.zs) - 1))
            poly, c = self.polys[k], self.cent[k]
            d = p[:2] - c
            n = np.linalg.norm(d)
            if n < 1e-6:
                continue
            u = d / n
            # distance from the centre to the hull along u
            best = None
            m = len(poly)
            for j in range(m):
                a, b = poly[j], poly[(j + 1) % m]
                e = b - a
                den = u[0] * (-e[1]) - u[1] * (-e[0])
                if abs(den) < 1e-12:
                    continue
                t = ((a - c)[0] * (-e[1]) - (a - c)[1] * (-e[0])) / den
                s = (u[0] * (a - c)[1] - u[1] * (a - c)[0]) / den
                if t > 0 and -1e-9 <= s <= 1 + 1e-9:
                    best = t if best is None else min(best, t)
            if best is not None and n < best + gap[i]:
                P[i, :2] = c + u * (best + gap[i])
        return P

    def top(self, x, y=None, band=0.012):
        """Highest point of the body near lateral x (and depth y, if given), above the chest: (y, z)."""
        m = (np.abs(self.V[:, 0] - x) < band) & (self.V[:, 2] > 1.3) & (self.V[:, 2] < 1.70) & (self.V[:, 1] > -0.08)
        if y is not None:
            m &= np.abs(self.V[:, 1] - y) < 0.02
        S = self.V[m]
        if not len(S):
            return 0.02, 1.5
        i = int(np.argmax(S[:, 2]))
        return float(S[i, 1]), float(S[i, 2])


H = None


def hulls():
    global H
    if H is None:
        H = Hulls()
    return H


NECK_R, NECK_YC, NECK_SIDE_DEG = 0.068, 0.045, 172.0
TIP_X = 0.265


def ridge(side, u, gap=0.012):
    """Shoulder ridge from the neck side (u=0) to the shoulder tip (u=1): along the top of the
    body (its highest point at each lateral position), plus gap."""
    h = hulls()
    sgn = -1.0 if side == "R" else 1.0
    x0 = NECK_R + 0.012
    xs = x0 + (TIP_X - x0) * np.atleast_1d(np.asarray(u, float))
    out = []
    for x, uu in zip(xs, np.atleast_1d(np.asarray(u, float))):
        yy = 0.05 + (0.01 - 0.05) * uu                 # the side of the neck to the middle of the shoulder
        y, z = h.top(sgn * x, yy)
        out.append((sgn * x, yy, z + gap))
    return np.array(out)


def neck_ring(side, phi_deg, z, gap=0.012):
    """A point round the neck; phi in degrees as seen from above for the RIGHT side
    (90 = centre back, 180 = right side, 270 = centre front); mirrored for the left."""
    phi = np.radians(np.asarray(phi_deg, float))
    x = (NECK_R + gap) * np.cos(phi)
    y = NECK_YC + (NECK_R + gap) * 1.1 * np.sin(phi)
    if side == "L":
        x = -x
    return np.stack([np.atleast_1d(x), np.atleast_1d(y), np.atleast_1d(z) * np.ones_like(np.atleast_1d(x))], 1)
