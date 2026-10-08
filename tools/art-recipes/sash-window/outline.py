"""Outlines of a mesh, drawn and compared without any renderer.

The lab's automatic check (production/lab): a model's front outline, side
outline and sections are computed straight from its triangles, rasterised at a
known scale, and compared with a target drawn from measured numbers. Nothing
here uses a graphics card.

    meshes = load_npz("window.npz")             # {name: (V (n,3) metres, F (m,3))}
    a = silhouette(meshes, axes=(0, 2), frame=fr)            # front, x right, z up
    b = section(meshes, axis=0, value=0.0, axes=(1, 2), frame=fr)
    m = compare(a, target, mm_per_px=fr.mm_per_px)

Frame: the window of the plane drawn and its scale, shared by target and model.
Sections fill each closed loop even-odd, so a hollow (a weight box) stays empty.
"""
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage


@dataclass
class Frame:
    u0: float          # metres at the left edge (first axis)
    v0: float          # metres at the bottom edge (second axis)
    width: float       # metres
    height: float      # metres
    mm_per_px: float = 1.0

    @property
    def shape(self):
        return (int(round(self.height * 1000 / self.mm_per_px)),
                int(round(self.width * 1000 / self.mm_per_px)))

    def to_px(self, u, v):
        s = 1000.0 / self.mm_per_px
        h = self.shape[0]
        return (u - self.u0) * s, h - (v - self.v0) * s


def load_npz(path):
    d = np.load(path, allow_pickle=False)
    names = sorted({k[:-2] for k in d.files if k.endswith("_V")})
    return {n: (d[n + "_V"].astype(np.float64), d[n + "_F"].astype(np.int64)) for n in names}


def blank(frame):
    h, w = frame.shape
    return Image.new("1", (w, h), 0)


def silhouette(meshes, axes, frame, only=None):
    """Union of all triangles projected on the plane of `axes`."""
    img = blank(frame)
    dr = ImageDraw.Draw(img)
    for name, (V, F) in meshes.items():
        if only and not any(name.startswith(p) for p in only):
            continue
        P = np.stack(frame.to_px(V[:, axes[0]], V[:, axes[1]]), axis=1)
        for t in F:
            dr.polygon([tuple(P[i]) for i in t], fill=1, outline=1)
    return np.array(img, dtype=bool)


def _loops(V, F, axis, value):
    """Closed loops where the plane axis=value cuts the mesh, as lists of 3D points."""
    d = V[:, axis] - value
    d[np.abs(d) < 1e-9] = 1e-9          # never exactly on the plane
    pts, adj = {}, {}

    def cut(i, j):
        key = (i, j) if i < j else (j, i)
        if key not in pts:
            t = d[key[0]] / (d[key[0]] - d[key[1]])
            pts[key] = V[key[0]] + t * (V[key[1]] - V[key[0]])
        return key

    for a, b, c in F:
        s = [d[a] > 0, d[b] > 0, d[c] > 0]
        if all(s) or not any(s):
            continue
        ks = [cut(i, j) for i, j in ((a, b), (b, c), (c, a)) if (d[i] > 0) != (d[j] > 0)]
        if len(ks) == 2:
            adj.setdefault(ks[0], []).append(ks[1])
            adj.setdefault(ks[1], []).append(ks[0])
    loops, seen = [], set()
    for start in adj:
        if start in seen:
            continue
        loop, prev, cur = [start], None, start
        seen.add(start)
        while True:
            nxt = [n for n in adj[cur] if n != prev and n not in seen]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            seen.add(cur)
            loop.append(cur)
        if len(loop) >= 3:
            loops.append(np.array([pts[k] for k in loop]))
    return loops


def section(meshes, axis, value, axes, frame, only=None):
    """Cut through every mesh at axis=value; each mesh's loops filled even-odd."""
    out = np.zeros(frame.shape, dtype=bool)
    for name, (V, F) in meshes.items():
        if only and not any(name.startswith(p) for p in only):
            continue
        acc = np.zeros(frame.shape, dtype=bool)
        for L in _loops(V, F, axis, value):
            img = blank(frame)
            P = np.stack(frame.to_px(L[:, axes[0]], L[:, axes[1]]), axis=1)
            ImageDraw.Draw(img).polygon([tuple(p) for p in P], fill=1, outline=1)
            acc ^= np.array(img, dtype=bool)
        out |= acc
    return out


def boundary(mask):
    return mask & ~ndimage.binary_erosion(mask, border_value=0)


def compare(model, target, mm_per_px):
    """Overlap and outline distance, in millimetres."""
    inter = np.logical_and(model, target).sum()
    union = np.logical_or(model, target).sum()
    bm, bt = boundary(model), boundary(target)
    if not bm.any() or not bt.any():
        return {"iou": 0.0, "mean_mm": None, "p95_mm": None, "max_mm": None}
    dt_t = ndimage.distance_transform_edt(~bt) * mm_per_px   # distance to target outline
    dt_m = ndimage.distance_transform_edt(~bm) * mm_per_px
    d = np.concatenate([dt_t[bm], dt_m[bt]])                  # both ways
    return {"iou": round(float(inter / union), 4),
            "mean_mm": round(float(d.mean()), 2),
            "p95_mm": round(float(np.percentile(d, 95)), 2),
            "max_mm": round(float(d.max()), 2)}


def overlay(model, target, path, scale=1):
    """Green = both, red = model only, blue = target only, white = neither."""
    h, w = model.shape
    rgb = np.full((h, w, 3), 255, np.uint8)
    rgb[model & target] = (60, 160, 60)
    rgb[model & ~target] = (220, 40, 40)
    rgb[~model & target] = (40, 80, 220)
    im = Image.fromarray(rgb)
    if scale != 1:
        im = im.resize((int(w * scale), int(h * scale)), Image.NEAREST)
    im.save(path)
    return path


def _selftest():
    # a 1 m cube with a 0.5 m square hole through it along y: front silhouette
    # shows the hole, a section at y=0 is a square ring.
    def box(x0, x1, y0, y1, z0, z1):
        V = np.array([[x, y, z] for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)], float)
        F = np.array([[0, 1, 3], [0, 3, 2], [4, 6, 7], [4, 7, 5], [0, 4, 5], [0, 5, 1],
                      [2, 3, 7], [2, 7, 6], [0, 2, 6], [0, 6, 4], [1, 5, 7], [1, 7, 3]])
        return V, F
    parts = {"a": box(-.5, -.25, -.5, .5, -.5, .5), "b": box(.25, .5, -.5, .5, -.5, .5),
             "c": box(-.25, .25, -.5, .5, -.5, -.25), "d": box(-.25, .25, -.5, .5, .25, .5)}
    fr = Frame(-.6, -.6, 1.2, 1.2, mm_per_px=5)
    s = silhouette(parts, (0, 2), fr)
    area = s.sum() * (fr.mm_per_px / 1000) ** 2
    assert abs(area - 0.75) < 0.04, area   # outlines add up to half a pixel each side
    c = section(parts, 1, 0.0, (0, 2), fr)
    assert abs(c.sum() * (fr.mm_per_px / 1000) ** 2 - 0.75) < 0.04
    m = compare(s, c, fr.mm_per_px)
    assert m["iou"] > 0.97, m
    # a single closed box with an inner box (hollow): section filled even-odd
    V1, F1 = box(-.5, .5, -.5, .5, -.5, .5)
    V2, F2 = box(-.25, .25, -.25, .25, -.25, .25)
    hollow = {"h": (np.vstack([V1, V2]), np.vstack([F1, F2 + 8]))}
    c2 = section(hollow, 1, 0.0, (0, 2), fr)
    assert abs(c2.sum() * (fr.mm_per_px / 1000) ** 2 - 0.75) < 0.04
    print("outline selftest ok")


if __name__ == "__main__":
    _selftest()
