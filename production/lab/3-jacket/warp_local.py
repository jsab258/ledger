"""Carry a plate's curves to a customer's draft the grader's way.

Each curve is cut at its anchors (the ruled points it passes, and its ends); each
stretch between two anchors is moved by the similarity (turn, uniform scale, shift)
that takes the plate's two anchor positions to the draft's. So every stretch keeps
the plate's shape and passes exactly through the draft's points. A point the text
leaves to the diagram is placed by an affine fit on the nearest ruled points.
"""
import numpy as np


def similarity(p0, p1, q0, q1):
    """Map taking p0->q0, p1->q1 (complex-number similarity)."""
    a, b = complex(*p0), complex(*p1)
    c, d = complex(*q0), complex(*q1)
    if abs(b - a) < 1e-9:
        return lambda P: np.asarray(P) - np.array(p0) + np.array(q0)
    k = (d - c) / (b - a)
    def f(P):
        z = (np.asarray(P)[:, 0] + 1j * np.asarray(P)[:, 1] - a) * k + c
        return np.stack([z.real, z.imag], 1)
    return f


def local_affine(src_pts, dst_pts, p, k=6):
    """Affine from the k ruled points nearest p (plate px -> draft in)."""
    src, dst = np.asarray(src_pts, float), np.asarray(dst_pts, float)
    i = np.argsort(np.linalg.norm(src - np.asarray(p, float), axis=1))[:k]
    X = np.c_[src[i], np.ones(len(i))]
    A, *_ = np.linalg.lstsq(X, dst[i], rcond=None)
    return np.r_[np.asarray(p, float), 1.0] @ A


def map_curve(curve_px, anchors, tol=40.0):
    """curve_px (n,2); anchors: list of (px, target) pairs. The curve's two ends are
    always anchors (their targets must be among `anchors`, matched by distance)."""
    C = np.asarray(curve_px, float)
    marks = []
    for px, tgt in anchors:
        d = np.linalg.norm(C - np.asarray(px, float), axis=1)
        i = int(np.argmin(d))
        if d[i] <= tol:
            marks.append((i, np.asarray(px, float), np.asarray(tgt, float)))
    marks.sort(key=lambda m: m[0])
    if not marks or marks[0][0] != 0 or marks[-1][0] != len(C) - 1:
        raise ValueError("curve ends are not anchored: %s" % [m[0] for m in marks])
    out = [None] * len(C)
    for (i0, p0, q0), (i1, p1, q1) in zip(marks[:-1], marks[1:]):
        f = similarity(C[i0], C[i1], q0, q1)
        seg = f(C[i0:i1 + 1])
        for j, v in zip(range(i0, i1 + 1), seg):
            out[j] = v
    return np.array(out)
