"""Construction detail drawn into a garment's baked maps by its pattern's own measures: seams, felled bands, stitch
rows, patch pockets, openings, a fly, belt loops and bar tacks, each placed in a pattern piece's millimetres.

    python tools/meshgen/garment_details.py RASTER.npz PLAN.json SPEC.json MAPS_DIR OUT_DIR [--name jeans] [--margin 8]

WHY, 30 October 2026 (Tom's jeans: a fresh reviewer of the game's film read them as plain blue trousers, with no back
pockets, yoke, fly, front-pocket edges or seams; the game-garment skill, steps 6 and 8: the silhouette in the mesh;
seams, stitch lines and pocket edges in the normal map, and a faint thread line in the colour map, as Mafia draws its
stitch lines and pocket flaps). A pattern maker marks a pocket by its distance from a seam or a corner, so the detail
here is placed the same way: every point is a corner of the plan's piece, a distance along one of its edges, or built
from those; RASTER.npz (layout_raster.py) gives each texel its piece and its place on that piece's pattern, so the
detail lands on the cloth where the pattern puts it, whatever the packing did to the island, and the left pieces (the
plan's mirror of the right) get it mirrored with them. Give it a raster made with --flat (each piece of the game mesh
flattened itself and laid onto its pattern) when the game mesh is stretched against its pattern: a line straight in
the pattern is then straight on the surface the game draws (Tom's jeans: on the pattern's own layout the back pockets'
edges zigzagged across the seat). Nothing in this file knows a garment: SPEC.json holds the
garment's construction (what, where, how high), and its sources.

The detail is a height field in millimetres (grooves at seams, raised fells and pockets, stitch rows with their holes),
its slopes taken in the pattern's millimetres (drawn again a twentieth of a millimetre each way) and turned into the
island's axes by its own scale and turn, then laid over the baked normal map (reoriented normal blending); the
thread is drawn lighter in the colour map by SPEC's "thread"/"lighter"; shadows beside raised edges go into the colour
map's alpha (occlusion) and darken its colour a little. The packed map is copied unchanged (the part's ID stays cloth).
Each island's margin is filled again from its edge, 8 texels, as the bake fills it.

SPEC.json (lengths in mm; "{s}" in a name is each side's letter, the left pieces mirrored in x; literal vectors are
given for the right side):
  "sides": ["R", "L"],                       the default sides of every feature
  "thread": {"lighter": 0.10, "stitchMm": 3.0, "halfMm": 0.35},
  "points": {name: POINT}, "curves": {name: CURVE},   named, per side
  "features": [FEATURE...], "measure": [point names], "clearance": [{"a": CURVE, "b": CURVE, "min": mm}]
  POINT: {"corner": c} | {"along": [c0, c1], "mm": s, "in": d} (along the piece's edge from corner c0 toward c1, then
         d inward) | {"mid": [P, Q]} | {"from": P, "d": [dx, dy]} | {"from": P, "frame": [c0, c1], "d": [a, b]} (a along
         that edge, b inward) | {"from": P, "dir": DIR, "mm": m} | {"x": P, "yOn": CURVE, "dy": m} (straight below or
         above P on CURVE, then m in y) | "name"
  DIR:   [dx, dy] | {"inward": [c0, c1]} | {"along": [c0, c1]}
  CURVE: {"edge": [c0, c1], "from": s0, "to": s1} | {"offsetEdge": [c0, c1], "in": d, "from": s0, "to": s1} |
         {"line": [P, Q], "extend": e} | {"bezier": [P0, P1, P2, P3]} | {"poly": [P...]} | {"chain": [CURVE...]} |
         {"extended": CURVE, "by": [e0, e1]} (carried on straight past its ends) | "name"
  FEATURE kinds, each with "piece" (e.g. "back{s}") and optional "sides" and "name":
    groove {curve, depth, half}                                   a crease along a seam line
    fell   {curve, side?: DIR, width, height, soft, rows: [..], groove?: {depth, half}}   a raised band beside a line
           (on the side DIR points to; an edge's band lies inside the piece), its rows at those distances
    rows   {curve, offsets: [..], side?: DIR}                     stitch rows parallel to a curve
    patch  {outline: [CURVE...] (closed, in order), height, soft, round?: [part indices], shadow?: {ao, dark, mm},
            rows?: [{part, in|out: [..]}], clip?: [CURVE...] (a closed region it is cut to), covers?: true}
           a layer laid on the piece (a pocket, a loop, a facing under an opening when its height is negative)
    tack   {curve, width, height}                                 a bar tack: dense thread across
"""
import argparse
import json
import math
import os
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import cKDTree

ap = argparse.ArgumentParser()
ap.add_argument("raster")
ap.add_argument("plan")
ap.add_argument("spec")
ap.add_argument("maps")
ap.add_argument("out")
ap.add_argument("--name", default="jeans")
ap.add_argument("--margin", type=int, default=8)
A = ap.parse_args()
t0 = time.time()
os.makedirs(A.out, exist_ok=True)

R = np.load(A.raster)
PIECE = R["piece"].astype(np.int32)
PX, PY, POS = R["px"].astype(np.float64), R["py"].astype(np.float64), R["pos"]
NAMES = [str(n) for n in R["names"]]
TEX = int(R["tex"])
PLAN = json.load(open(A.plan, encoding="utf-8"))
SPEC = json.load(open(A.spec, encoding="utf-8"))
TH = SPEC.get("thread", {})
LIGHTER = float(TH.get("lighter", 0.10))
STITCH = float(TH.get("stitchMm", 3.0))
THALF = float(TH.get("halfMm", 0.35))
ROW = SPEC.get("row", {})
ROW_DEPTH, ROW_HALF = float(ROW.get("depth", 0.15)), float(ROW.get("half", 0.9))
HOLE_DEPTH = float(ROW.get("hole", 0.08))
STEP = 0.25                                   # curve sampling, mm
log = {"spec": A.spec, "raster": A.raster, "maps": A.maps, "tex": TEX, "checks": {}, "features": [], "points": {}}


def smooth(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def bump(x):
    """1 at 0, 0 at |x| >= 1, smooth."""
    y = np.clip(1 - x * x, 0.0, 1.0)
    return y * y


# ---- each piece: its texels, its outline (from the mesh), its corners and edges --------------------------------
class Piece:
    def __init__(self, k):
        self.k, self.name = k, NAMES[k]
        self.mask = PIECE == k
        self.idx = np.nonzero(self.mask)
        self.p = np.stack([PX[self.idx], PY[self.idx]], axis=1)
        self.tree = cKDTree(self.p)
        sel = R["seg_piece"] == k
        a_, b_ = R["seg_a"][sel].astype(np.float64), R["seg_b"][sel].astype(np.float64)
        # the pattern's own places of the outline's points, where the raster's places are the piece's flattening
        # (layout_raster.py --flat): the plan's corners are found by those
        has_pat = "seg_a_pat" in R.files
        ap_ = R["seg_a_pat"][sel].astype(np.float64) if has_pat else a_
        bp_ = R["seg_b_pat"][sel].astype(np.float64) if has_pat else b_
        key = lambda q: (round(float(q[0]), 2), round(float(q[1]), 2))  # noqa: E731
        adj, pt, ptp = {}, {}, {}
        for u, v, up, vp in zip(a_, b_, ap_, bp_):
            ku, kv = key(u), key(v)
            pt[ku], pt[kv] = u, v
            ptp[ku], ptp[kv] = up, vp
            adj.setdefault(ku, []).append(kv)
            adj.setdefault(kv, []).append(ku)
        start = next(iter(adj))
        loop, prev, cur = [start], None, start
        while True:
            nxt = [n for n in adj[cur] if n != prev and n not in loop[1:]]
            if not nxt or nxt[0] == start:
                break
            prev, cur = cur, nxt[0]
            loop.append(cur)
        self.loop = np.array([pt[q] for q in loop])
        self.loop_pat = np.array([ptp[q] for q in loop])
        self.closed_ok = len(loop) == len(a_)
        x, y = self.loop[:, 0], self.loop[:, 1]
        self.ccw = (np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y) / 2) > 0
        self.corners = {}
        for cname, cx, cy in PLAN["corners"].get(self.name, []):
            d = np.hypot(self.loop_pat[:, 0] - cx, self.loop_pat[:, 1] - cy)
            self.corners[cname] = int(np.argmin(d))
        # the texel size here: millimetres per texel, from the raster's own pattern coordinates
        gxx = np.gradient(PX, axis=1)[self.idx]
        gyx = np.gradient(PY, axis=1)[self.idx]
        gxy = np.gradient(PX, axis=0)[self.idx]
        gyy = np.gradient(PY, axis=0)[self.idx]
        det = np.abs(gxx * gyy - gxy * gyx)
        er = ndimage.binary_erosion(self.mask, iterations=2)[self.idx]
        self.mm_per_texel = float(np.sqrt(np.median(det[er])))

    def inside(self, q):
        """Points (N x 2) inside the piece's outline (ray casting)."""
        q = np.atleast_2d(q)
        x, y = self.loop[:, 0], self.loop[:, 1]
        x2, y2 = np.roll(x, -1), np.roll(y, -1)
        res = np.zeros(len(q), dtype=bool)
        for j in range(len(x)):
            c = ((y[j] > q[:, 1]) != (y2[j] > q[:, 1]))
            with np.errstate(divide="ignore", invalid="ignore"):
                xi = (x2[j] - x[j]) * (q[:, 1] - y[j]) / (y2[j] - y[j]) + x[j]
            res ^= c & (q[:, 0] < xi)
        return res

    def edge(self, c0, c1):
        i0, i1 = self.corners[c0], self.corners[c1]
        n = len(self.loop)
        others = {v for kk, v in self.corners.items() if kk not in (c0, c1)}
        fwd = [(i0 + j) % n for j in range((i1 - i0) % n + 1)]
        bwd = [(i0 - j) % n for j in range((i0 - i1) % n + 1)]
        path = fwd if not (set(fwd[1:-1]) & others) else bwd
        return self.loop[path]


PIECES = {NAMES[k]: Piece(k) for k in range(len(NAMES)) if (PIECE == k).any()}
log["checks"]["outlinesClosed"] = {n: p.closed_ok for n, p in PIECES.items()}
log["checks"]["mmPerTexel"] = {n: round(p.mm_per_texel, 4) for n, p in PIECES.items()}


# ---- curves: dense samples with arc length and tangents ---------------------------------------------------------
class Curve:
    def __init__(self, pts):
        pts = np.asarray(pts, dtype=np.float64)
        keep = np.concatenate([[True], np.hypot(*np.diff(pts, axis=0).T) > 1e-9])
        pts = pts[keep]
        seg = np.hypot(*np.diff(pts, axis=0).T)
        cum = np.concatenate([[0.0], np.cumsum(seg)])
        L = cum[-1]
        n = max(2, int(math.ceil(L / STEP)) + 1)
        s = np.linspace(0, L, n)
        self.p = np.stack([np.interp(s, cum, pts[:, 0]), np.interp(s, cum, pts[:, 1])], axis=1)
        self.s, self.L = s, L
        t = np.gradient(self.p, axis=0)
        self.t = t / (np.linalg.norm(t, axis=1, keepdims=True) + 1e-12)
        self.tree = cKDTree(self.p)

    def at(self, s):
        s = float(np.clip(s, 0, self.L))
        j = int(np.clip(np.searchsorted(self.s, s), 1, len(self.s) - 1))
        f = (s - self.s[j - 1]) / max(1e-12, self.s[j] - self.s[j - 1])
        return self.p[j - 1] * (1 - f) + self.p[j] * f, self.t[j]

    def sub(self, s0, s1):
        s0, s1 = float(np.clip(s0, 0, self.L)), float(np.clip(s1, 0, self.L))
        if s0 <= s1:
            m = (self.s > s0) & (self.s < s1)
            pts = [self.at(s0)[0]] + list(self.p[m]) + [self.at(s1)[0]]
        else:
            m = (self.s > s1) & (self.s < s0)
            pts = [self.at(s0)[0]] + list(self.p[m][::-1]) + [self.at(s1)[0]]
        return Curve(pts)


def bez(p0, p1, p2, p3, n=400):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3


class Ctx:
    """One feature on one side: names with {s} filled, literal vectors mirrored for the left."""

    def __init__(self, side, piece):
        self.side, self.piece = side, PIECES[piece.replace("{s}", side)]
        self.mx = -1.0 if side in SPEC.get("mirrorSides", ["L"]) else 1.0

    def nm(self, s):
        return s.replace("{s}", self.side)

    def vec(self, v):
        return np.array([v[0] * self.mx, v[1]], dtype=np.float64)

    def edge_curve(self, c0, c1):
        return Curve(self.piece.edge(self.nm(c0), self.nm(c1)))

    def inward(self, c0, c1, q):
        e = self.edge_curve(c0, c1)
        _d, j = e.tree.query(q)
        t = e.t[j]
        n = np.array([-t[1], t[0]])
        return n if self.piece.inside(e.p[j] + n * 0.5)[0] else -n

    def P(self, ps):
        if isinstance(ps, str):
            return self.P(SPEC["points"][ps])
        if isinstance(ps, list):
            return self.vec(ps)
        if "corner" in ps:
            return self.piece.loop[self.piece.corners[self.nm(ps["corner"])]].copy()
        if "along" in ps:
            c0, c1 = ps["along"]
            e = self.edge_curve(c0, c1)
            q, _t = e.at(ps["mm"])
            d = ps.get("in", 0.0)
            return q + self.inward(c0, c1, q) * d if d else q
        if "mid" in ps:
            return (self.P(ps["mid"][0]) + self.P(ps["mid"][1])) / 2
        if "x" in ps:
            base = self.P(ps["x"])
            c = self.C(ps["yOn"])
            j = int(np.argmin(np.abs(c.p[:, 0] - base[0])))
            return np.array([base[0], c.p[j, 1] + ps.get("dy", 0.0)])
        if "from" in ps:
            base = self.P(ps["from"])
            if "frame" in ps:
                c0, c1 = ps["frame"]
                e = self.edge_curve(c0, c1)
                _d, j = e.tree.query(base)
                return base + e.t[j] * ps["d"][0] + self.inward(c0, c1, base) * ps["d"][1]
            if "d" in ps:
                return base + self.vec(ps["d"])
            return base + self.D(ps["dir"], base) * ps["mm"]
        raise ValueError("point %r" % (ps,))

    def D(self, ds, base):
        if isinstance(ds, list):
            v = self.vec(ds)
            return v / np.linalg.norm(v)
        if "inward" in ds:
            return self.inward(ds["inward"][0], ds["inward"][1], base)
        if "along" in ds:
            e = self.edge_curve(*ds["along"])
            _d, j = e.tree.query(base)
            return e.t[j]
        raise ValueError("dir %r" % (ds,))

    def C(self, cs):
        if isinstance(cs, str):
            return self.C(SPEC["curves"][cs])
        if "edge" in cs:
            e = self.edge_curve(*cs["edge"])
            return e.sub(cs.get("from", 0.0), cs.get("to", e.L)) if ("from" in cs or "to" in cs) else e
        if "offsetEdge" in cs:
            c0, c1 = cs["offsetEdge"]
            e = self.edge_curve(c0, c1)
            s0, s1 = cs.get("from", 0.0), cs.get("to", e.L)
            sub = e.sub(s0, s1)
            n = np.stack([-sub.t[:, 1], sub.t[:, 0]], axis=1)
            mid = len(sub.p) // 2
            if not self.piece.inside(sub.p[mid] + n[mid] * 0.5)[0]:
                n = -n
            return Curve(sub.p + n * cs["in"])
        if "line" in cs:
            p, q = self.P(cs["line"][0]), self.P(cs["line"][1])
            u = (q - p) / np.linalg.norm(q - p)
            e = cs.get("extend", 0.0)
            return Curve([p - u * e, q + u * e])
        if "bezier" in cs:
            return Curve(bez(*[self.P(x) for x in cs["bezier"]]))
        if "poly" in cs:
            return Curve([self.P(x) for x in cs["poly"]])
        if "chain" in cs:
            parts = [self.C(c) for c in cs["chain"]]
            return Curve(np.concatenate([c.p for c in parts]))
        if "extended" in cs:
            c = self.C(cs["extended"])
            e0, e1 = cs["by"]
            return Curve(np.concatenate([[c.p[0] - c.t[0] * e0], c.p, [c.p[-1] + c.t[-1] * e1]]))
        raise ValueError("curve %r" % (cs,))


# ---- the fields: height (mm), colour factor, occlusion factor ---------------------------------------------------
H = np.zeros((TEX, TEX))
COL = np.ones((TEX, TEX))
AO = np.ones((TEX, TEX))
THREAD = np.zeros((TEX, TEX))       # thread coverage (for the record and the colour)


def near(piece, curve, reach):
    """The piece's texels within reach of the curve: their flat indices, distance, nearest sample."""
    lo, hi = curve.p.min(axis=0) - reach, curve.p.max(axis=0) + reach
    m = (piece.p[:, 0] >= lo[0]) & (piece.p[:, 0] <= hi[0]) & (piece.p[:, 1] >= lo[1]) & (piece.p[:, 1] <= hi[1])
    sel = np.nonzero(m)[0]
    if len(sel) == 0:
        return sel, np.zeros(0), np.zeros(0, dtype=int)
    d, j = curve.tree.query(piece.p[sel], distance_upper_bound=reach)
    ok = np.isfinite(d)
    return sel[ok], d[ok], j[ok]


def signed(piece, curve, sel, j):
    q = piece.p[sel] - curve.p[j]
    t = curve.t[j]
    return np.sign(t[:, 0] * q[:, 1] - t[:, 1] * q[:, 0])


def put(piece, sel, field, values, op="add"):
    rr, cc = piece.idx[0][sel], piece.idx[1][sel]
    if op == "add":
        np.add.at(field, (rr, cc), values)
    elif op == "mul":
        np.multiply.at(field, (rr, cc), values)
    elif op == "max":
        np.maximum.at(field, (rr, cc), values)


def stitch_row(piece, e, t_along, weight=1.0):
    """A row of stitches at e (signed mm from the row's line, per texel) and t (mm along it): the cloth pulled into a
    groove, deeper at each stitch's hole, the thread lighter between the holes. BAND-LIMITED (the first run drew sharp
    holes and a proud thread, each narrower than a texel: every seventh hole fell on a texel's centre and the rows
    showed dark dots 21 mm apart): along the row one smooth wave per stitch, across it the groove alone."""
    wave = 0.5 + 0.5 * np.cos(2 * math.pi * t_along / STITCH)          # 1 at a hole, 0 mid-stitch
    h = -(ROW_DEPTH + HOLE_DEPTH * wave) * bump(e / ROW_HALF)
    cov = np.clip(1 - np.abs(e) / (THALF + piece.mm_per_texel / 2), 0, 1) * (1 - 0.6 * wave)
    return h * weight, cov * weight


def rows_along(piece, curve, offsets, side=None, mask_fn=None, sgn_dir=None):
    reach = max([abs(o) for o in offsets] + [0]) + 2.5
    sel, d, j = near(piece, curve, reach)
    if len(sel) == 0:
        return 0
    if side is not None:
        s = signed(piece, curve, sel, j)
        dd = d * s * side
    else:
        dd = d
    keep = np.ones(len(sel), dtype=bool)
    if mask_fn is not None:
        keep &= mask_fn(sel)
    # not past the curve's ends (a row stops where its line stops)
    end = (j > 0) & (j < len(curve.p) - 1)
    keep &= end | (d < 0.6)
    sel, dd, j = sel[keep], dd[keep], j[keep]
    tot = 0
    for o in offsets:
        e = dd - o
        m = np.abs(e) < ROW_HALF + 0.3
        h, cov = stitch_row(piece, e[m], curve.s[j[m]])
        put(piece, sel[m], H, h)
        put(piece, sel[m], THREAD, cov, "max")
        tot += int(m.sum())
    return tot


def region_raster(poly, res=0.25):
    lo = poly.min(axis=0) - 1
    hi = poly.max(axis=0) + 1
    w, h = int((hi[0] - lo[0]) / res) + 2, int((hi[1] - lo[1]) / res) + 2
    im = Image.new("L", (w, h), 0)
    ImageDraw.Draw(im).polygon([tuple(((q - lo) / res).tolist()) for q in poly], fill=255)
    arr = np.asarray(im) > 127

    def test(q):
        ix = ((q[:, 0] - lo[0]) / res).astype(int)
        iy = ((q[:, 1] - lo[1]) / res).astype(int)
        ok = (ix >= 0) & (iy >= 0) & (ix < w) & (iy < h)
        out = np.zeros(len(q), dtype=bool)
        out[ok] = arr[iy[ok], ix[ok]]
        return out
    return test


feat_masks = []   # (name, side, piece, flat indices) for the record and the mirror check
CURVES_USED = {}


def feature(f, side):
    ctx = Ctx(side, f["piece"])
    pc = ctx.piece
    kind = f["kind"]
    name = f.get("name", kind) + "/" + side
    touched = np.zeros(len(pc.p), dtype=bool)
    if kind == "groove":
        c = ctx.C(f["curve"])
        sel, d, j = near(pc, c, f["half"])
        put(pc, sel, H, -f["depth"] * bump(d / f["half"]))
        touched[sel] = True
    elif kind in ("fell", "rows"):
        c = ctx.C(f["curve"])
        CURVES_USED[name] = c
        side_v = None
        if "side" in f:
            dv = ctx.D(f["side"], c.p[len(c.p) // 2])
            mid = len(c.p) // 2
            n_left = np.array([-c.t[mid][1], c.t[mid][0]])
            side_v = 1.0 if n_left.dot(dv) > 0 else -1.0
        if kind == "fell":
            w, h, soft = f["width"], f["height"], f.get("soft", 1.2)
            sel, d, j = near(pc, c, w + soft + 1)
            dd = d * (signed(pc, c, sel, j) * side_v if side_v is not None else 1.0)
            end = (j > 0) & (j < len(c.p) - 1)
            band = h * smooth(dd / soft) * smooth((w - dd) / soft) * end
            put(pc, sel, H, band)
            touched[sel[band > 0.05 * h]] = True
            if f.get("groove"):
                g = f["groove"]
                m = d < g["half"]
                put(pc, sel[m], H, -g["depth"] * bump(d[m] / g["half"]) * end[m])
        rows = f.get("rows", f.get("offsets", []))
        rows_along(pc, c, rows, side=side_v)
    elif kind == "patch":
        parts = [ctx.C(cs) for cs in f["outline"]]
        poly = np.concatenate([c.p for c in parts])
        inside = region_raster(poly)
        clip = region_raster(np.concatenate([ctx.C(cs).p for cs in f["clip"]])) if "clip" in f else None
        whole = Curve(np.concatenate([poly, poly[:1]]))
        rnd = [parts[i] for i in f.get("round", range(len(parts)))]
        soft, h = f.get("soft", 1.5), f["height"]
        reach = soft + f.get("shadow", {}).get("mm", 0) * 3 + 2
        ins = inside(pc.p)
        if clip is not None:
            ins &= clip(pc.p)
        # distance to the rounded parts only (an edge on the piece's own outline stays hard)
        dr = np.full(len(pc.p), np.inf)
        for c in rnd:
            sel, d, _j = near(pc, c, reach)
            dr[sel] = np.minimum(dr[sel], d)
        lift = np.where(ins, smooth(dr / soft), 0.0)
        if f.get("covers"):
            # what lay under it is hidden: the earlier detail faded out under the layer
            rr, cc = pc.idx
            keep = 1 - lift
            H[rr, cc] *= keep
            THREAD[rr, cc] *= keep
        put(pc, np.arange(len(pc.p)), H, h * lift)
        touched |= ins
        sh = f.get("shadow")
        if sh:
            # the low side of the edge: outside a raised layer, inside a sunk one
            low = (~ins) if h > 0 else ins
            # (a layer cut by a region casts its shadow only inside that region: the first run drew the coin pocket's
            # whole outline, hidden part and all, as a faint line on the front)
            m = low & np.isfinite(dr) & (clip(pc.p) if clip is not None else True)
            fall = np.exp(-dr[m] / max(0.3, sh["mm"]))
            sel = np.nonzero(m)[0]
            put(pc, sel, AO, 1 - sh.get("ao", 0.15) * fall, "mul")
            put(pc, sel, COL, 1 - sh.get("dark", 0.03) * fall, "mul")
        for r in f.get("rows", []):
            c = parts[r["part"]]
            if "in" in r:
                rows_along(pc, c, r["in"], mask_fn=lambda sel_: inside(pc.p[sel_]) & (clip(pc.p[sel_]) if clip is not None else True))
            else:
                rows_along(pc, c, r["out"], mask_fn=lambda sel_: ~inside(pc.p[sel_]))
        CURVES_USED[name] = whole
    elif kind == "tack":
        c = ctx.C(f["curve"])
        w, h = f["width"], f.get("height", 0.3)
        sel, d, j = near(pc, c, w / 2 + 1)
        end = (j > 0) & (j < len(c.p) - 1)
        cov = smooth((w / 2 - d) / 0.6) * end
        put(pc, sel, H, h * cov)
        put(pc, sel, THREAD, cov * 0.9, "max")
        touched[sel[cov > 0.1]] = True
    else:
        raise ValueError(kind)
    feat_masks.append((name, side, pc.name, np.nonzero(touched)[0]))


# THE SLOPES FROM THE PATTERN, NOT FROM THE TEXELS (the first run took the height's slope across texels: at every
# island's edge, a staircase in texel space, the height carried past the edge gave a sawtooth crease along each seam).
# The detail is drawn again with every texel's pattern place moved a little each way, and the height's slope taken in
# the pattern's millimetres, then turned into the layout's axes by the island's own scale and turn.
DELTA = 0.05
for pc in PIECES.values():
    pc.p0 = pc.p.copy()
H_PASS = {}
for tag, off in (("x+", (DELTA, 0)), ("x-", (-DELTA, 0)), ("y+", (0, DELTA)), ("y-", (0, -DELTA)), ("0", (0, 0))):
    H[:] = 0
    COL[:] = 1
    AO[:] = 1
    THREAD[:] = 0
    feat_masks.clear()
    for pc in PIECES.values():
        pc.p = pc.p0 + np.array(off)
    for f in SPEC["features"]:
        for side in f.get("sides", SPEC.get("sides", ["R", "L"])):
            feature(f, side)
    H_PASS[tag] = H.copy()
HX = (H_PASS["x+"] - H_PASS["x-"]) / (2 * DELTA)
HY = (H_PASS["y+"] - H_PASS["y-"]) / (2 * DELTA)

# ---- the maps -----------------------------------------------------------------------------------------------------
def load(fn):
    im = Image.open(os.path.join(A.maps, fn))
    return np.asarray(im.convert("RGBA")).astype(np.float64)[::-1] / 255.0     # row 0 at v = 0, as the raster


col0 = load(A.name + "_colour_ao.png")
nrm0 = load(A.name + "_normal_gl.png")
packed = Image.open(os.path.join(A.maps, A.name + "_packed.png"))
inside_any = PIECE >= 0

# the slopes, piece by piece, each from its own texel size; the height carried a few texels past the island so the
# edge's slope is the island's own
SX = np.zeros((TEX, TEX))
SY = np.zeros((TEX, TEX))
jac = {}
for pname, pc in PIECES.items():
    # the island's own scale and turn: pattern millimetres per texel along u and along v (medians inside the island)
    er = ndimage.binary_erosion(pc.mask, iterations=3)
    a_ = float(np.median(np.gradient(PX, axis=1)[er]))   # d px / d u
    b_ = float(np.median(np.gradient(PX, axis=0)[er]))   # d px / d v
    c_ = float(np.median(np.gradient(PY, axis=1)[er]))   # d py / d u
    d_ = float(np.median(np.gradient(PY, axis=0)[er]))   # d py / d v
    jac[pname] = [round(a_, 4), round(b_, 4), round(c_, 4), round(d_, 4)]
    m = pc.mask
    if "jq" in R.files:
        # each texel's own triangle's rates (the place per texel, the body's millimetres per texel)
        J, MET = R["jq"], R["met"]
        SX[m] = (HX[m] * J[..., 0][m] + HY[m] * J[..., 2][m]) / np.maximum(MET[..., 0][m], 1e-6)
        SY[m] = (HX[m] * J[..., 1][m] + HY[m] * J[..., 3][m]) / np.maximum(MET[..., 1][m], 1e-6)
    else:
        SX[m] = (HX[m] * a_ + HY[m] * c_) / math.hypot(a_, c_)
        SY[m] = (HX[m] * b_ + HY[m] * d_) / math.hypot(b_, d_)
log["checks"]["islandMmPerTexel_dpx_du_dv_dpy_du_dv"] = jac

nb = nrm0[..., :3] * 2 - 1
nb /= np.linalg.norm(nb, axis=2, keepdims=True) + 1e-12
nd = np.stack([-SX, -SY, np.ones_like(SX)], axis=2)
nd /= np.linalg.norm(nd, axis=2, keepdims=True)
# reoriented normal blending (Barre-Brisebois and Hill, 2012): the detail turned onto the baked normal
tt = nb + np.array([0, 0, 1.0])
uu = nd * np.array([-1.0, -1.0, 1.0])
n_new = tt * (np.sum(tt * uu, axis=2, keepdims=True) / np.maximum(tt[..., 2:3], 1e-4)) - uu
n_new /= np.linalg.norm(n_new, axis=2, keepdims=True) + 1e-12
n_out = np.where(inside_any[..., None], n_new, nb)

colour = col0.copy()
lift = 1 + LIGHTER * np.clip(THREAD, 0, 1)
colour[..., :3] = np.clip(col0[..., :3] * (COL * lift)[..., None], 0, 1)
colour[..., 3] = np.clip(col0[..., 3] * AO, 0, 1)

# the margin: each island's edge carried outward ring by ring, each new texel the mean of its filled neighbours, as
# zip_bake.py fills it (the first run copied each margin texel from its single nearest island texel: the island's
# texel staircase came out as scallops along every edge)
got = inside_any.copy()
for _ in range(A.margin):
    acc_n = np.zeros_like(n_out)
    acc_c = np.zeros_like(colour)
    cnt = np.zeros((TEX, TEX))
    for dy, dx_ in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        ok_ = np.roll(np.roll(got, dy, 0), dx_, 1)
        acc_n += np.roll(np.roll(n_out, dy, 0), dx_, 1) * ok_[..., None]
        acc_c += np.roll(np.roll(colour, dy, 0), dx_, 1) * ok_[..., None]
        cnt += ok_
    new = (~got) & (cnt > 0)
    n_out[new] = acc_n[new] / cnt[new][:, None]
    colour[new] = acc_c[new] / cnt[new][:, None]
    got |= new
n_out /= np.linalg.norm(n_out, axis=2, keepdims=True) + 1e-12
n_out[~got] = nb[~got]
colour[~got] = col0[~got]

gl = np.concatenate([(n_out + 1) / 2, nrm0[..., 3:4]], axis=2)
dx = gl.copy()
dx[..., 1] = 1 - dx[..., 1]


def save(arr, fn):
    a8 = np.clip(np.round(arr[::-1] * 255), 0, 255).astype(np.uint8)
    Image.fromarray(a8, "RGBA").save(os.path.join(A.out, fn))


save(gl, A.name + "_normal_gl.png")
save(dx, A.name + "_normal_dx.png")
save(colour, A.name + "_colour_ao.png")
packed.save(os.path.join(A.out, A.name + "_packed.png"))

# ---- checks -------------------------------------------------------------------------------------------------------
over60_new, over60_old = {}, {}
for pname, pc in PIECES.items():
    over60_new[pname] = round(float((n_out[..., 2][pc.mask] < 0.5).mean()), 4)
    over60_old[pname] = round(float((nb[..., 2][pc.mask] < 0.5).mean()), 4)
log["checks"]["normalsOver60PerPiece"] = over60_new
log["checks"]["normalsOver60PerPieceBefore"] = over60_old
tilt = np.degrees(np.arccos(np.clip(np.sum(n_out * nb, axis=2), -1, 1)))
log["checks"]["detailTiltDeg"] = {"p99": round(float(np.percentile(tilt[inside_any], 99)), 1),
                                  "max": round(float(tilt[inside_any].max()), 1)}
grey0 = col0[..., :3][inside_any].mean()
log["checks"]["threadLighterMax"] = round(float((lift[inside_any]).max() - 1), 4)
log["checks"]["threadTexels"] = int((THREAD[inside_any] > 0.5).sum())
log["checks"]["colourMapGreyBefore"] = round(float(grey0), 4)
# where each feature lies on the body: its texels' centroid (world metres) and its piece
cent = {}
for name, side, pname, sel in feat_masks:
    pc = PIECES[pname]
    if len(sel) == 0:
        log["features"].append({"name": name, "piece": pname, "texels": 0})
        continue
    q = POS[pc.idx[0][sel], pc.idx[1][sel]]
    c = q.mean(axis=0)
    cent[name] = c
    log["features"].append({"name": name, "piece": pname, "texels": int(len(sel)),
                            "centroidM": [round(float(v), 4) for v in c],
                            "zRangeM": [round(float(q[:, 2].min()), 4), round(float(q[:, 2].max()), 4)]})
# mirror: the right side's and the left side's of one feature, mirrored in x on the body
mirror = {}
for name, c in cent.items():
    base, side = name.rsplit("/", 1)
    if side == "R" and base + "/L" in cent:
        cl = cent[base + "/L"]
        mirror[base] = {"xSumMm": round(1000 * float(c[0] + cl[0]), 1), "dyMm": round(1000 * float(c[1] - cl[1]), 1),
                        "dzMm": round(1000 * float(c[2] - cl[2]), 1), "rightX": round(float(c[0]), 4)}
log["checks"]["mirror"] = mirror
# named points on the body (pattern mm and world metres)
for pn in SPEC.get("measure", []):
    for side in SPEC.get("sides", ["R", "L"]):
        spec_p = SPEC["points"][pn]
        piece_name = spec_p.get("piece", "").replace("{s}", side) if isinstance(spec_p, dict) else ""
        if not piece_name:
            continue
        ctx = Ctx(side, spec_p["piece"])
        q = ctx.P({k: v for k, v in spec_p.items() if k != "piece"})
        d, j = ctx.piece.tree.query(q)
        w = POS[ctx.piece.idx[0][j], ctx.piece.idx[1][j]]
        log["points"][pn + "/" + side] = {"patternMm": [round(float(v), 1) for v in q], "offLayoutMm": round(float(d), 2),
                                           "bodyM": [round(float(v), 4) for v in w]}
# clearances: the least distance between two curves (e.g. a pocket and the seam it must not reach)
cl = []
for c in SPEC.get("clearance", []):
    for side in c.get("sides", SPEC.get("sides", ["R", "L"])):
        a = CURVES_USED.get(c["a"] + "/" + side)
        b = CURVES_USED.get(c["b"] + "/" + side)
        if a is None or b is None:
            continue
        d, _ = b.tree.query(a.p)
        cl.append({"a": c["a"], "b": c["b"], "side": side, "minMm": round(float(d.min()), 1), "need": c["min"],
                   "ok": bool(d.min() >= c["min"])})
log["checks"]["clearance"] = cl
# every feature kept to its own piece's outline (none reaching past a seam): the share of each closed feature's
# outline lying outside its piece
past = {}
for name, c in CURVES_USED.items():
    base, side = name.rsplit("/", 1)
    f = next(x for x in SPEC["features"] if x.get("name") == base)
    if f["kind"] != "patch" or "clip" in f:
        continue
    pc = PIECES[f["piece"].replace("{s}", side)]
    past[name] = round(float((~pc.inside(c.p[::8])).mean()), 4)
log["checks"]["closedOutlineShareOutsidePiece"] = past
log["seconds"] = round(time.time() - t0, 1)
json.dump(log, open(os.path.join(A.out, "details.json"), "w", encoding="utf-8"), indent=1)
print("DETAILS", json.dumps({k: log["checks"][k] for k in ("normalsOver60PerPiece", "detailTiltDeg", "threadLighterMax",
                                                            "clearance", "closedOutlineShareOutsidePiece")}))
print("MIRROR", json.dumps(mirror))
print("SECONDS", log["seconds"])
