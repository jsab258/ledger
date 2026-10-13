"""sd_lib: the shared tools of the street-dressing targets (cloud week 42, unit 13).

Everything is in MILLIMETRES, z up, the front of a piece faces -y, the pivot is the base's centre on the ground.
A part is a dict in target.json; this file turns the dicts into convex pieces and then answers, from the pieces
alone: the overall box, which parts meet which, which float, which interpenetrate, which closed faces let a ray
through (square on and at angles), the silhouettes and sections for the drawing, and the checks' bookkeeping.
Nothing here knows any family; the families only supply their own target.json.
"""
import copy
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time

import numpy as np
import shapely
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
from shapely.geometry import MultiPoint, Polygon
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PREVIEWS = os.path.join(REPO, "production", "previews", "cloud-week", "refs", "street-dressing")
UA_PAGE = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36 "
           "LedgerProject-reference-research")
UA_API = "LedgerProject-reference-research/1.0 (street furniture measurement; no contact)"
LANTERN_LINEAR = [1.0, 0.25, 0.0]
STALE_NIGHT = "(1, 0.7055, 0)"

# Real makers, operators, firms and marks that must not appear anywhere in a target (text, data, scripts).
BLOCKLIST = [
    "british telecom", "telecom", "gpo", "post office", "royal mail", "bt", "mercury", "cable and wireless", "kingston communications",
    "kcom", "adshel", "clear channel", "jcdecaux", "stagecoach", "arriva", "firstgroup", "go-ahead", "national express",
    "national bus", "london transport", "northern general", "yorkshire traction", "midland red", "ribble", "leyland",
    "glasdon", "marshalls", "biffa", "cleanaway", "hss", "speedy", "sunbelt", "hiremaster",
    "unigate", "express dairy", "dairy crest", "united dairies", "northern dairies",
    "raleigh", "dawes", "claud butler", "brompton", "peugeot", "halfords", "sturmey", "reynolds", "shimano",
    "campagnolo", "sachs", "dunlop", "pashley",
    "chep", "lpr", "pallet network", "palletways", "euro pool",
    "coca-cola", "pepsi", "guinness", "carling", "tennent", "heineken", "embassy",
    "silk cut", "marlboro", "rothmans", "woodbine", "capstan",
    "union jack", "crown copyright", "ordnance survey", "kindersley", "rowntree",
]
# words that are fine as plain English although they sit in the list above
BLOCK_OK_CONTEXT = {}


# ------------------------------------------------------------------------------------------------ geometry
def rot(yaw=0.0, pitch=0.0, roll=0.0):
    """Rz(yaw) Ry(pitch) Rx(roll), degrees."""
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll))
    Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])
    Ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]])
    Rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]])
    return Rz @ Ry @ Rx


class Piece:
    """One convex solid, from its vertices (millimetres)."""
    __slots__ = ("V", "N", "D", "lo", "hi", "tri")

    def __init__(self, V):
        V = np.asarray(V, float)
        self.V = V
        h = ConvexHull(V)
        eq = h.equations
        key = np.round(eq, 5)
        _, idx = np.unique(key, axis=0, return_index=True)
        eq = eq[np.sort(idx)]
        self.N = eq[:, :3].copy()
        self.D = eq[:, 3].copy()
        self.lo = V.min(0)
        self.hi = V.max(0)
        self.tri = h.simplices

    def inside(self, P, tol=0.0):
        return np.all(P @ self.N.T + self.D <= tol, axis=1)


def _ring(p0, p1, r0, r1, n=24):
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    a = p1 - p0
    L = np.linalg.norm(a)
    e = a / L
    t = np.array([1.0, 0, 0]) if abs(e[0]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(e, t)
    u /= np.linalg.norm(u)
    v = np.cross(e, u)
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    ring = np.outer(np.cos(ang), u) + np.outer(np.sin(ang), v)
    return np.vstack([p0 + ring * r0, p1 + ring * r1])


def _prism_pieces(d):
    plane = d["plane"]
    outer = d["poly"]
    holes = d.get("holes", [])
    poly = Polygon(outer, holes)
    if not poly.is_valid:
        poly = poly.buffer(0)
    tris = shapely.constrained_delaunay_triangles(poly)
    out = []
    lo, hi = d["w"]
    for t in tris.geoms:
        if t.area < 1e-6:
            continue
        pts = list(t.exterior.coords)[:3]
        V = []
        for (a, b) in pts:
            for w in (lo, hi):
                if plane == "xz":
                    V.append([a, w, b])
                elif plane == "yz":
                    V.append([w, a, b])
                else:  # xy
                    V.append([a, b, w])
        out.append(Piece(V))
    return out


def part_pieces(d):
    """The convex pieces of one part dict (before its optional xf)."""
    k = d["type"]
    if k == "box":
        s = np.array(d["s"], float)
        c = np.array(d["c"], float)
        R = rot(*d.get("rot", [0, 0, 0]))
        corners = np.array([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]) * s / 2.0
        return [Piece(c + corners @ R.T)]
    if k == "cyl":
        return [Piece(_ring(d["p0"], d["p1"], d["r0"], d.get("r1", d["r0"]), d.get("n", 24)))]
    if k == "wire":
        pts = np.asarray(d["pts"], float)
        return [Piece(_ring(pts[i], pts[i + 1], d["r"], d["r"], d.get("n", 6))) for i in range(len(pts) - 1)]
    if k == "sphere":
        c = np.array(d["c"], float)
        r = np.array(d["r"] if isinstance(d["r"], list) else [d["r"]] * 3, float)
        V = []
        for la in np.linspace(-80, 80, 9):
            for lo in np.linspace(0, 360, 16, endpoint=False):
                V.append([math.cos(math.radians(la)) * math.cos(math.radians(lo)),
                          math.cos(math.radians(la)) * math.sin(math.radians(lo)), math.sin(math.radians(la))])
        V += [[0, 0, 1], [0, 0, -1]]
        return [Piece(c + np.array(V) * r)]
    if k == "prism":
        return _prism_pieces(d)
    raise ValueError("unknown part type %r" % k)


class PartSet:
    """All the parts of one variant, as pieces."""

    def __init__(self, parts):
        self.parts = parts
        self.names = [p["id"] for p in parts]
        self.pieces = []  # list of lists
        for p in parts:
            pcs = part_pieces(p)
            xf = p.get("xf")
            if xf:
                R = rot(*xf.get("rot", [0, 0, 0]))
                t = np.array(xf.get("t", [0, 0, 0]), float)
                o = np.array(xf.get("pivot", [0, 0, 0]), float)
                pcs = [Piece((pc.V - o) @ R.T + o + t) for pc in pcs]
            self.pieces.append(pcs)
        self.index = {n: i for i, n in enumerate(self.names)}

    def bbox(self, include_transparent=True, only=None):
        lo = np.full(3, np.inf)
        hi = np.full(3, -np.inf)
        for p, pcs in zip(self.parts, self.pieces):
            if only is not None and p["id"] not in only:
                continue
            if not include_transparent and p.get("transparent"):
                continue
            for pc in pcs:
                lo = np.minimum(lo, pc.lo)
                hi = np.maximum(hi, pc.hi)
        return lo, hi

    def part_bbox(self, name):
        i = self.index[name]
        lo = np.min([pc.lo for pc in self.pieces[i]], axis=0)
        hi = np.max([pc.hi for pc in self.pieces[i]], axis=0)
        return lo, hi

    def volume(self, name):
        tot = 0.0
        for pc in self.pieces[self.index[name]]:
            tot += ConvexHull(pc.V).volume
        return tot


# ------------------------------------------------------------------------------------------------ contacts
def _lp_depth(Pa, Pb, tol_a):
    """Largest t with a point x that is inside A inflated by tol_a and inside B by margin t (None if infeasible)."""
    A = np.vstack([Pa.N, Pb.N])
    b = np.concatenate([-Pa.D + tol_a, -Pb.D])
    A = np.hstack([A, np.ones((A.shape[0], 1))])
    c = np.array([0, 0, 0, -1.0])
    r = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)] * 3 + [(None, 2000.0)], method="highs")
    if r.status != 0:
        return None
    return float(-r.fun)


def contact_table(ps, tol=2.0):
    """For every pair of parts: ('touch', 0) when within tol, ('overlap', depth) when they interpenetrate, else absent.
    depth is the radius of the largest ball inside both (millimetres)."""
    res = {}
    n = len(ps.parts)
    for i in range(n):
        for j in range(i + 1, n):
            best = None
            for pa in ps.pieces[i]:
                for pb in ps.pieces[j]:
                    if np.any(pa.lo - tol > pb.hi) or np.any(pb.lo - tol > pa.hi):
                        continue
                    t = _lp_depth(pa, pb, tol)
                    if t is None or t < 0:
                        continue
                    t0 = _lp_depth(pa, pb, 0.0)
                    depth = max(0.0, t0) if t0 is not None else 0.0
                    if best is None or depth > best[1]:
                        best = ("overlap" if depth > 0.05 else "touch", depth)
            if best:
                res[(ps.names[i], ps.names[j])] = best
    return res


def grounded(ps, tol=2.0):
    g = set()
    for p, pcs in zip(ps.parts, ps.pieces):
        if min(pc.lo[2] for pc in pcs) <= tol and not p.get("hangs"):
            g.add(p["id"])
    return g


def components(ps, contacts, ground):
    """Parts connected to the ground through the contact graph."""
    adj = {n: set() for n in ps.names}
    for (a, b) in contacts:
        adj[a].add(b)
        adj[b].add(a)
    seen = set(ground)
    stack = list(ground)
    while stack:
        a = stack.pop()
        for b in adj[a]:
            if b not in seen:
                seen.add(b)
                stack.append(b)
    return seen, adj


# ------------------------------------------------------------------------------------------------ closed faces (rays)
def solid_inside(ps, P, skip_transparent=True):
    """Boolean per point: inside any non-transparent part."""
    out = np.zeros(len(P), bool)
    lo = P.min(0)
    hi = P.max(0)
    for p, pcs in zip(ps.parts, ps.pieces):
        if skip_transparent and p.get("transparent"):
            continue
        for pc in pcs:
            if np.any(pc.lo > hi) or np.any(pc.hi < lo):
                continue
            m = (~out) & np.all(P >= pc.lo - 1e-9, axis=1) & np.all(P <= pc.hi + 1e-9, axis=1)
            if m.any():
                idx = np.where(m)[0]
                out[idx[pc.inside(P[idx])]] = True
    return out


def face_rays(ps, face, step=None, angles=None, sample=1.0):
    """Shoot rays at a closed face. face: {id, o:[x,y,z] a corner, u, v: unit vectors along the face, n: OUTWARD unit,
    nu, nv: its size along u and v, depth: the wall's thickness plus play (mm), apertures: [[u0,v0,u1,v1]..] (glazing,
    openings that are meant to be open)}. Two grids are shot: one fine across u (1 mm) and coarse along v (30 mm), which
    finds vertical slots, and one the other way round, which finds horizontal slots. Each is shot square on and leaning
    30 and 45 degrees across its fine direction. A ray starts 0.5 mm outside the face and goes inward; it is blocked
    when it enters a solid (not transparent) part within depth / cos(angle). Returns (rays, leaks): leaks is a list of
    (u, v, lean in degrees, set) that got through."""
    o = np.array(face["o"], float)
    u = np.array(face["u"], float)
    v = np.array(face["v"], float)
    nrm = np.array(face["n"], float)
    nu, nv = face["nu"], face["nv"]
    ap = face.get("apertures", [])
    fine = face.get("fine", 1.0)
    coarse = face.get("coarse", 30.0)
    nrays = 0
    leaks = []
    for setname, (su, sv, axis) in (("A", (fine, coarse, u)), ("B", (coarse, fine, v))):
        us = np.arange(su / 2, nu, su)
        vs = np.arange(sv / 2, nv, sv)
        UU, VV = np.meshgrid(us, vs)
        UU = UU.ravel()
        VV = VV.ravel()
        keep = np.ones(len(UU), bool)
        for a in ap:
            keep &= ~((UU >= a[0]) & (UU <= a[2]) & (VV >= a[1]) & (VV <= a[3]))
        UU, VV = UU[keep], VV[keep]
        if not len(UU):
            continue
        for lean in (0, 30, -30, 45, -45):
            d = -nrm + axis * math.tan(math.radians(lean))
            d = d / np.linalg.norm(d)
            depth = face["depth"] / float(np.dot(d, -nrm))
            ts = np.arange(0.0, depth + sample, sample)
            reach = ts[-1] * float(np.dot(d, axis))
            inside_end = (UU + reach >= 0) & (UU + reach <= nu) if axis is u else (VV + reach >= 0) & (VV + reach <= nv)
            UU_k, VV_k = UU[inside_end], VV[inside_end]
            if not len(UU_k):
                continue
            starts = o + np.outer(UU_k, u) + np.outer(VV_k, v) + nrm * 0.5
            P = starts[:, None, :] + ts[None, :, None] * d[None, None, :]
            ins = solid_inside(ps, P.reshape(-1, 3)).reshape(len(UU_k), len(ts))
            blocked = ins.any(axis=1)
            nrays += len(UU_k)
            for k in np.where(~blocked)[0]:
                leaks.append((round(float(UU_k[k]), 1), round(float(VV_k[k]), 1), lean, setname))
    return nrays, leaks


# ------------------------------------------------------------------------------------------------ drawing
VIEWS = {
    # name: (right axis, up axis, forward (viewing) axis) in world coordinates
    "front": ((1, 0, 0), (0, 0, 1), (0, 1, 0)),
    "back": ((-1, 0, 0), (0, 0, 1), (0, -1, 0)),
    "left": ((0, -1, 0), (0, 0, 1), (1, 0, 0)),
    "right": ((0, 1, 0), (0, 0, 1), (-1, 0, 0)),
    "plan": ((1, 0, 0), (0, 1, 0), (0, 0, -1)),
}


def view_axes(view):
    """(world axis of the picture's horizontal, sign): the horizontal runs along +x for front, -x for back, -y for left, +y for right."""
    return {"front": (0, 1), "back": (0, -1), "left": (1, -1), "right": (1, 1)}[view]


def project_part(ps, name, view):
    r, u, f = [np.array(a, float) for a in VIEWS[view]]
    polys = []
    for pc in ps.pieces[ps.index[name]]:
        pts = np.c_[pc.V @ r, pc.V @ u]
        h = MultiPoint(pts).convex_hull
        if h.geom_type == "Polygon" and h.area > 1e-6:
            polys.append(h)
    if not polys:
        return None
    g = unary_union(polys)
    return g


def silhouette(ps, view, include_transparent=True, only=None):
    gs = []
    for p in ps.parts:
        if only is not None and p["id"] not in only:
            continue
        if not include_transparent and p.get("transparent"):
            continue
        g = project_part(ps, p["id"], view)
        if g is not None:
            gs.append(g)
    return unary_union(gs)


def _plane_section_piece(pc, axis, val):
    pts = []
    V = pc.V
    ax = "xyz".index(axis)
    edges = set()
    for t in pc.tri:
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            edges.add((min(a, b), max(a, b)))
    for a, b in edges:
        da, db = V[a, ax] - val, V[b, ax] - val
        if da == 0:
            pts.append(V[a])
        if da * db < 0:
            s = da / (da - db)
            pts.append(V[a] + s * (V[b] - V[a]))
    if len(pts) < 3:
        return None
    pts = np.array(pts)
    other = [i for i in range(3) if i != ax]
    h = MultiPoint(pts[:, other]).convex_hull
    if h.geom_type != "Polygon" or h.area < 1e-6:
        return None
    return h


def section_polys(ps, axis, val):
    """Per part, the polygon of its cut by the plane axis=val. Section axes: 'x' gives (y, z); 'y' gives (x, z);
    'z' gives (x, y)."""
    out = {}
    for p, pcs in zip(ps.parts, ps.pieces):
        gs = []
        for pc in pcs:
            g = _plane_section_piece(pc, axis, val)
            if g is not None:
                gs.append(g)
        if gs:
            out[p["id"]] = unary_union(gs)
    return out


def poly_coords(g):
    if g.geom_type == "Polygon":
        return [[[round(x, 2), round(y, 2)] for x, y in g.exterior.coords]]
    return [[[round(x, 2), round(y, 2)] for x, y in q.exterior.coords] for q in g.geoms if q.geom_type == "Polygon"]


def draw_json(T, variant=None, sections=None):
    """The drawing as filled polygons in millimetres: every view's silhouettes part by part, and the named sections."""
    parts = variant_parts(T, variant)
    ps = PartSet(parts)
    out = {"family": T["family"], "variant": variant or T.get("sample"), "units": "mm", "views": {}, "sections": {}}
    for vname in T.get("drawing", {}).get("views", ["front", "left", "plan"]):
        r, u, f = [np.array(a, float) for a in VIEWS[vname]]
        entries = []
        for p in parts:
            g = project_part(ps, p["id"], vname)
            if g is None:
                continue
            c = np.mean([pc.V.mean(0) for pc in ps.pieces[ps.index[p["id"]]]], axis=0)
            entries.append({"part": p["id"], "material": p.get("material"), "transparent": bool(p.get("transparent")),
                            "depth": round(float(c @ f), 1), "polygons": poly_coords(g)})
        entries.sort(key=lambda e: -e["depth"])
        out["views"][vname] = entries
    for s in (sections or T.get("drawing", {}).get("sections", [])):
        polys = section_polys(ps, s["axis"], s["at"])
        out["sections"][s["id"]] = {"axis": s["axis"], "at": s["at"],
                                    "parts": [{"part": k, "material": parts[ps.index[k]].get("material"),
                                               "polygons": poly_coords(g)} for k, g in polys.items()]}
    return out


def hex_of(rgb):
    return "#%02x%02x%02x" % tuple(int(x) for x in rgb)


def draw_pictures(T, dj, outdir, px_per_mm=0.3):
    from PIL import Image, ImageDraw
    os.makedirs(outdir, exist_ok=True)
    mats = T.get("materials", {})

    def col(m, transparent):
        rgb = mats.get(m, {}).get("srgb", [150, 150, 150])
        return tuple(rgb) if not transparent else tuple(int(0.55 * c + 0.45 * 235) for c in rgb)

    made = []
    items = [("view-" + k, v) for k, v in dj["views"].items()] + [("section-" + k, v) for k, v in dj["sections"].items()]
    for name, ent in items:
        polys = ent if isinstance(ent, list) else [{"part": q["part"], "material": q["material"], "polygons": q["polygons"], "transparent": False}
                                                     for q in ent["parts"]]
        allpts = [pt for e in polys for poly in e["polygons"] for pt in poly]
        if not allpts:
            continue
        xs = [p[0] for p in allpts]
        ys = [p[1] for p in allpts]
        pad = 40
        s = px_per_mm
        W = int((max(xs) - min(xs)) * s) + 2 * pad
        H = int((max(ys) - min(ys)) * s) + 2 * pad
        im = Image.new("RGB", (max(W, 50), max(H, 50)), (250, 250, 248))
        d = ImageDraw.Draw(im)
        over = Image.new("RGBA", im.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(over)
        for e in polys:
            for poly in e["polygons"]:
                pts = [((x - min(xs)) * s + pad, H - ((y - min(ys)) * s + pad)) for x, y in poly]
                if e.get("transparent"):
                    od.polygon(pts, fill=(170, 200, 215, 90), outline=(60, 110, 130, 255))
                else:
                    d.polygon(pts, fill=col(e.get("material"), False), outline=(30, 30, 30))
        im = Image.alpha_composite(im.convert("RGBA"), over).convert("RGB")
        d = ImageDraw.Draw(im)
        d.text((6, 4), "%s %s (mm; %.0f x %.0f)" % (T["family"], name, max(xs) - min(xs), max(ys) - min(ys)), fill=(0, 0, 0))
        p = os.path.join(outdir, "%s-%s.png" % (T["family"], name))
        im.save(p)
        made.append(p)
    return made


def variant_parts(T, variant=None):
    v = variant or T.get("sample")
    if "variants" in T and v in T["variants"]:
        return T["variants"][v]["parts"]
    return T["parts"]


# ------------------------------------------------------------------------------------------------ photographs
def load_gray(path):
    from PIL import Image
    im = Image.open(path).convert("L")
    return np.asarray(im, float)


def _smooth(a, s=1.2):
    from scipy.ndimage import gaussian_filter1d
    return gaussian_filter1d(a, s)


def edge_pos(gray, axis, band, win, pol="any", sigma=1.2):
    """One edge. axis 'x': the edge is a vertical line; average the grey over rows band=[r0,r1], search columns
    win=[c0,c1]. axis 'y': a horizontal line; average over columns band, search rows win. pol '+' brighter after,
    '-' darker after, 'any'. Returns (position in pixels, contrast, spread) where spread is the difference between the
    positions found in the two halves of the band (the error's measure)."""
    def one(b0, b1):
        if axis == "x":
            prof = gray[int(b0):int(b1) + 1, :].mean(axis=0)
        else:
            prof = gray[:, int(b0):int(b1) + 1].mean(axis=1)
        pr = _smooth(prof, sigma)
        g = np.gradient(pr)
        w0, w1 = int(win[0]), int(win[1])
        seg = g[w0:w1 + 1]
        if pol == "+":
            k = int(np.argmax(seg))
        elif pol == "-":
            k = int(np.argmin(seg))
        else:
            k = int(np.argmax(np.abs(seg)))
        i = w0 + k
        if 0 < k < len(seg) - 1:
            a, b, c = abs(g[i - 1]), abs(g[i]), abs(g[i + 1])
            den = a - 2 * b + c
            off = 0.5 * (a - c) / den if den != 0 else 0.0
            off = max(-1, min(1, off))
        else:
            off = 0.0
        return i + off + 0.5, abs(g[i])
    b0, b1 = band
    mid = (b0 + b1) // 2
    p, c = one(b0, b1)
    p1, _ = one(b0, mid)
    p2, _ = one(mid, b1)
    return p, c, abs(p1 - p2)


def measure_features(gray, feats):
    out = {}
    for f in feats:
        p, c, sp = edge_pos(gray, f["axis"], f["band"], f["win"], f.get("pol", "any"))
        out[f["id"]] = (p, c, sp)
    return out


def geograph_page(gid, cache_dir):
    """Read a Geograph photo page: title, author, licence, taken date, description. Cached as html in cache_dir."""
    os.makedirs(cache_dir, exist_ok=True)
    p = os.path.join(cache_dir, "page_%s.html" % gid)
    if not os.path.exists(p) or os.path.getsize(p) < 2000:
        subprocess.run(["curl", "-sS", "-m", "60", "-A", UA_PAGE, "https://www.geograph.org.uk/photo/%s" % gid, "-o", p], check=False)
    h = open(p, encoding="utf-8", errors="replace").read()
    title = re.search(r"<title>(.*?)&copy;\s*(.*?) ::", h, re.S)
    lic = re.search(r'rel="license" href="([^"]+)"', h)
    taken = re.search(r"taken=(\d{4}-\d{2}-\d{2})", h)
    if not taken:
        taken = re.search(r"taken_start=(\d{4}-\d{2}-\d{2})", h)
    img = re.search(r'https://s\d\.geograph\.org\.uk/geophotos/[0-9/]+/%s_[0-9a-f]+\.jpg' % gid, h)
    desc = re.search(r'<div class="caption640"[^>]*>(.*?)</div>', h, re.S)
    return {"id": gid, "title": title.group(1).strip() if title else None, "author": title.group(2).strip() if title else None,
            "licence": lic.group(1) if lic else None, "taken": taken.group(1) if taken else None,
            "image": img.group(0) if img else None, "ok": bool(title and lic)}


def fetch_image(url, path):
    if not os.path.exists(path) or os.path.getsize(path) < 5000:
        subprocess.run(["curl", "-sS", "-m", "90", "-A", UA_PAGE, url, "-o", path], check=False)
    return os.path.exists(path) and os.path.getsize(path) > 5000


# ------------------------------------------------------------------------------------------------ the check harness
class Rows:
    def __init__(self):
        self.rows = []

    def add(self, group, name, ok, detail=""):
        self.rows.append({"group": group, "name": name, "ok": bool(ok), "detail": str(detail)[:400]})

    def near(self, group, name, got, want, tol, unit="mm"):
        ok = abs(float(got) - float(want)) <= tol
        self.add(group, name, ok, "%.2f %s against %.2f +- %.2f" % (got, unit, want, tol))

    def at_least(self, group, name, got, lim, unit="mm"):
        self.add(group, name, got >= lim, "%.2f %s, at least %.2f" % (got, unit, lim))

    def at_most(self, group, name, got, lim, unit="mm"):
        self.add(group, name, got <= lim, "%.2f %s, at most %.2f" % (got, unit, lim))


def words_scan(text):
    """Blocklisted words in a text: whole words only."""
    hits = []
    low = text.lower()
    for b in BLOCKLIST:
        for m in re.finditer(r"(?<![a-z0-9'])" + re.escape(b) + r"(?![a-z0-9'])", low):
            ctx = low[max(0, m.start() - 20):m.end() + 20]
            if b in BLOCK_OK_CONTEXT and any(c in ctx for c in BLOCK_OK_CONTEXT[b]):
                continue
            hits.append(b)
            break
    return hits


def strings(o, path=""):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, path + "/" + str(k))
    elif isinstance(o, (list, tuple)):
        for i, v in enumerate(o):
            yield from strings(v, path + "[%d]" % i)


def jhash(o):
    return hashlib.sha1(json.dumps(o, sort_keys=True, default=str).encode()).hexdigest()


def run_controls(T, controls, checks_fn, baseline_rows, **kw):
    """controls: list of (name, mutate(T)->None, row_prefix). A control is caught when a row whose name starts with the
    prefix fails in the mutated target and passed in the baseline. Returns a list of results."""
    base = {r["name"]: r["ok"] for r in baseline_rows}
    res = []
    for name, mut, prefix in controls:
        T2 = copy.deepcopy(T)
        try:
            mut(T2)
            rows = checks_fn(T2, **kw)
            failed = [r["name"] for r in rows if (not r["ok"]) and r["name"].startswith(prefix)]
            was_ok = [n for n, ok in base.items() if n.startswith(prefix) and ok]
            caught = bool(failed) and bool(was_ok)
            res.append({"control": name, "row": prefix, "caught": caught, "failed_rows": failed[:3]})
        except Exception as e:  # a control that crashes the check is a caught fault only if named so; record it
            res.append({"control": name, "row": prefix, "caught": False, "error": "%s: %s" % (type(e).__name__, e)})
    return res


def print_and_store(family, T, tpath, rows, ctl, options):
    n = len(rows)
    p = sum(1 for r in rows if r["ok"])
    f = n - p
    c_ok = sum(1 for c in ctl if c["caught"])
    line = "SELF-CHECK %s: %d checks, %d passed, %d failed; negative controls %d of %d caught (%s)" % (
        family, n, p, f, c_ok, len(ctl), options)
    print(line)
    for r in rows:
        if not r["ok"]:
            print("  FAIL [%s] %s: %s" % (r["group"], r["name"], r["detail"]))
    for c in ctl:
        if not c["caught"]:
            print("  NOT CAUGHT: %s (row %s) %s" % (c["control"], c["row"], c.get("error", "")))
    try:
        T = json.load(open(tpath))
        T["self_check"] = {"line": line, "checks": n, "passed": p, "failed": f, "controls": len(ctl), "controls_caught": c_ok,
                           "options": options, "failing": [r["name"] for r in rows if not r["ok"]],
                           "uncaught": [c["control"] for c in ctl if not c["caught"]]}
        with open(tpath, "w") as fh:
            json.dump(T, fh, indent=1)
    except Exception as e:
        print("could not write self_check into target.json:", e)
    return line, f + (len(ctl) - c_ok)


def r1(x, n=1):
    return round(float(x), n)


# ------------------------------------------------------------------------------------------------ part makers
def B(id, x0, x1, y0, y1, z0, z1, mat, **kw):
    """A box from its extents (mm)."""
    d = {"id": id, "type": "box", "c": [round((x0 + x1) / 2, 3), round((y0 + y1) / 2, 3), round((z0 + z1) / 2, 3)],
         "s": [round(x1 - x0, 3), round(y1 - y0, 3), round(z1 - z0, 3)], "material": mat}
    d.update(kw)
    return d


def CY(id, p0, p1, r, mat, r1=None, **kw):
    d = {"id": id, "type": "cyl", "p0": list(p0), "p1": list(p1), "r0": r, "material": mat}
    if r1 is not None:
        d["r1"] = r1
    d.update(kw)
    return d


def PR(id, plane, poly, w0, w1, mat, **kw):
    d = {"id": id, "type": "prism", "plane": plane, "poly": [list(map(float, p)) for p in poly], "w": [w0, w1], "material": mat}
    d.update(kw)
    return d


def WIRE(id, pts, r, mat, **kw):
    d = {"id": id, "type": "wire", "pts": [list(map(float, p)) for p in pts], "r": r, "material": mat}
    d.update(kw)
    return d


def SPH(id, c, r, mat, **kw):
    d = {"id": id, "type": "sphere", "c": list(c), "r": r, "material": mat}
    d.update(kw)
    return d


def sampled_photo(gid, key, scratch):
    """Page and image of one Geograph photograph into the scratch folder; returns (page dict, image path)."""
    pg = geograph_page(gid, scratch)
    path = os.path.join(scratch, "%s.jpg" % key)
    if pg.get("image"):
        for suffix in ("_1024x1024.jpg", ".jpg"):
            url = pg["image"].replace(".jpg", suffix) if suffix != ".jpg" else pg["image"]
            if fetch_image(url, path):
                try:
                    from PIL import Image
                    Image.open(path).verify()
                    break
                except Exception:
                    os.remove(path)
    return pg, path


def drawing_main(here, argv):
    """target_drawing.py of every family: reads target.json alone, writes target_drawing.json (polygons in mm) next to
    it and the pictures into the folder named on the command line."""
    T = json.load(open(os.path.join(here, "target.json")))
    out = {"family": T["family"], "variants": {}}
    for V in T["variants"]:
        out["variants"][V] = draw_json(T, V)
    json.dump(out, open(os.path.join(here, "target_drawing.json"), "w"))
    n = sum(len(v["views"]) + len(v["sections"]) for v in out["variants"].values())
    pics = []
    if argv:
        for V, dj in out["variants"].items():
            sub = dict(T)
            sub["family"] = T["family"] + "-" + V
            pics += draw_pictures(sub, dj, argv[0], px_per_mm=float(os.environ.get("SD_PX_PER_MM", "0.3")))
    print("%s: %d drawings in target_drawing.json%s" % (T["family"], n, ("; %d pictures in %s" % (len(pics), argv[0])) if pics else ""))
    return out
