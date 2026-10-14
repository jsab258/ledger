"""The automatic check for the front doors of every house kind (cloud week 42, unit 9).

    nice -n 15 /home/user/.bpyenv/bin/python check_doors.py [--version 1] [--kinds T1,F2] [--controls] [--overlays DIR] [--renders DIR]

It reads the built parts (build/door_<K>.npz, build/furniture_<ID>.npz), the .glb files as written, houses.json, paints.json and conditions.json, and:
  A  cuts each kind's mesh where the target draws it (target_drawing.py draws target.json alone; kit/tools/outline.py rasterises both at 0.5 mm a pixel) and compares:
     A1 the front view by layer (frame, transom glass with its bead, leaf: what shows from the street, the nearest part winning) against the drawing;
     A2 the openings, as the holes the leaf is cut with (sections of the leaf at set depths) against the drawn openings; A3 the mouldings, the lead came, the F7 nails
     and each fitting (extras where the drawing is not a pass test); A4 the profiles (bolection, stuck ovolo, T3's coves, the V joint) against the target's own sections.
     Pass rule as the brief and 3.1: IoU >= 0.97, outline p95 <= 2 mm, worst <= 6 mm; profiles p95 <= 1.5, worst <= 3; overall dimensions within 1 mm unless the target sets another.
  B  every record of target.json `checks` (162: PL panel layout, CV nothing shows through, FU furniture, BP the bell push, AD the street, PN paints, GL glass, WR wear,
     NM names, PH photographs, GA views), each measured on the mesh, the .glb or the data the doors are built and placed from, with the record's own id;
  C  the .glb files as written: size under 1 MB, UV sets on every primitive, no texture (a height map can never be exported as a normal map), named materials, closed
     parts, no two parts sharing a visible face plane (the shop windows' lesson), per kind and per house (kind plus its fittings);
  D  --controls: wrong copies (a bar moved 20 mm, a bezel on the push, a plate 40 mm off, a leaf shifted, two neighbours alike, a stale night colour ...), each of which
     must make its named row fail, so a row that cannot fail is found.
Writes checks/check_doors_v<N>.json and prints "N of M rows pass" (the required rows; extras are listed beside).
"""
import argparse
import copy
import importlib.util
import json
import math
import os
import re
import sys
import time
from collections import defaultdict

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from shapely.geometry import LineString, Point, Polygon, box as sbox
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "door"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import outline  # noqa: E402
from outline import Frame, compare, load_npz, overlay, silhouette  # noqa: E402

import doors_lib as L  # noqa: E402
from doors_lib import bd  # noqa: E402
import doors_street as DS  # noqa: E402
import check_door as cd  # noqa: E402   (the 3.1 check's glb reader, coplanar-overlap finder and closed-part test)

REPO = bd.REPO
TARGET_DIR = os.path.join(REPO, "production", "cloud-week", "targets", "front-doors-all")
sys.path.insert(0, TARGET_DIR)
spec = importlib.util.spec_from_file_location("target_drawing_all", os.path.join(TARGET_DIR, "target_drawing.py"))
td = importlib.util.module_from_spec(spec)
spec.loader.exec_module(td)
import td_common as TC  # noqa: E402
import td_kinds as TK  # noqa: E402

ASSET = os.path.join(REPO, "production", "assets", "cloud-week", "front-doors-all")
NPZ = os.path.join(HERE, "build")
KINDS = ["T1", "T2", "T3", "F1", "F2", "F3", "F4", "F5", "F6", "F7"]
PASS = {"iou": 0.97, "p95_mm": 2.0, "max_mm": 6.0, "profile_p95_mm": 1.5, "profile_max_mm": 3.0}
MMPX = 0.5
LAP = 20.4
VIS = TK.VIS
FORBID_BELL = ("bezel", "button", "ring", "lens", "led", "camera", "speaker", "video")
ALLOWED_MATERIALS = {"paint_", "frame_", "glass", "brass", "chrome_nickel", "steel_dark", "cast_iron", "aluminium_pale", "plastic_", "slot_interior", "stone_step",
                     "timber_threshold", "lead_came", "net_voile", "timber_bare", "paint_numeral_white"}


# ------------------------------------------------------------------ the report
class Report:
    def __init__(self):
        self.rows, self.adapt = [], []

    def add(self, id_, ok, measured, expected="", note="", tol=None, group="", extra=False, kind=None):
        row = {"id": id_, "group": group, "ok": bool(ok) if ok is not None else None, "measured": measured, "expected": expected}
        if kind:
            row["kind"] = kind
        if tol is not None:
            row["tol"] = tol
        if note:
            row["note"] = note
        if extra:
            row["extra"] = True
        self.rows.append(row)
        return bool(ok)

    def within(self, id_, measured, expected, tol, note="", group="", extra=False, kind=None):
        m = float(measured)
        return self.add(id_, abs(m - expected) <= tol, round(m, 2), expected, note, tol, group, extra, kind)

    def summary(self):
        req = [r for r in self.rows if not r.get("extra") and r["ok"] is not None]
        ext = [r for r in self.rows if r.get("extra") and r["ok"] is not None]
        return {"required_run": len(req), "required_passed": sum(1 for r in req if r["ok"]), "required_failed": [r["id"] for r in req if not r["ok"]],
                "extras_run": len(ext), "extras_passed": sum(1 for r in ext if r["ok"]), "extras_failed": [r["id"] for r in ext if not r["ok"]]}


def verdict(c, kind="drawing"):
    if kind == "profile":
        ok = c["p95_mm"] is not None and c["p95_mm"] <= PASS["profile_p95_mm"] and c["max_mm"] <= PASS["profile_max_mm"]
    else:
        ok = c["iou"] >= PASS["iou"] and c["p95_mm"] is not None and c["p95_mm"] <= PASS["p95_mm"] and c["max_mm"] <= PASS["max_mm"]
    c["ok"] = bool(ok)
    return c


# ------------------------------------------------------------------ the model of one kind (or one house: kind plus fittings), in the target's frame
def layer_of(name):
    if name.startswith("frame_glazing_bead") or name.startswith("glass_fanlight") or name == "lead_came":
        return "tglass"
    if name.startswith("frame_"):
        return "frame"
    if name.startswith("stone_") or name.startswith("timber_"):
        return "stone"
    if name.startswith("fit:"):
        return "fitting"
    return "leaf"


class Model:
    """Parts in the target's frame (metres in M, millimetres through the methods), cut and measured."""

    def __init__(self, N, kind, M, pivot):
        self.N, self.kind = N, kind
        self.spec = N["kinds"][kind]
        self.fsid = self.spec["frame_set"][0]
        self.fs = N["frame_sets"][self.fsid]
        self.M = M
        self.pivot = np.asarray(pivot, float)
        self.X0, self.Z0, self.W, self.H = self.fs["leaf_x0"], self.fs["leaf_z0"], self.spec["leaf"]["w"], self.spec["leaf"]["h"]
        self.LY0 = self.fs["leaf_front_y"]
        self.TH = self.spec["leaf"]["t"]

    @classmethod
    def load(cls, N, kind, npz=None):
        fs = N["frame_sets"][N["kinds"][kind]["frame_set"][0]]
        raw = load_npz(npz or os.path.join(NPZ, "door_%s.npz" % kind))
        piv = np.array(fs["glb_pivot"], float)
        return cls(N, kind, {n: (V + piv / 1000.0, F) for n, (V, F) in raw.items()}, piv)

    def copy_with(self, extra=None, drop=(), shift=None):
        M = {n: (V.copy(), F) for n, (V, F) in self.M.items() if n not in drop}
        if shift:
            for n in list(M):
                if shift[0](n):
                    M[n] = (M[n][0] + np.array(shift[1]) / 1000.0, M[n][1])
        if extra:
            M.update(extra)
        return Model(self.N, self.kind, M, self.pivot)

    def names(self, *prefixes):
        return [n for n in self.M if n.startswith(prefixes)]

    def where(self, pred):
        return [n for n in self.M if pred(n)]

    def sub(self, names):
        return {n: self.M[n] for n in names}

    def bbox(self, names):
        names = [names] if isinstance(names, str) else names
        V = np.vstack([self.M[n][0] for n in names]) * 1000.0
        return V.min(0), V.max(0)

    def region(self, names, axis, value_mm, axes):
        """The cut of the named parts by the plane axis = value (mm): a shapely region in (axes) mm, each part even-odd."""
        geoms = []
        for n in ([names] if isinstance(names, str) else names):
            V, F = self.M[n]
            g = None
            for Lp in outline._loops(V, F, axis, value_mm / 1000.0):
                pts = Lp[:, list(axes)] * 1000.0
                if len(pts) < 3:
                    continue
                p = Polygon(pts).buffer(0)
                g = p if g is None else g.symmetric_difference(p)
            if g is not None and not g.is_empty:
                geoms.append(g)
        return unary_union(geoms) if geoms else Polygon()

    # ---- the leaf's slab: the part the openings are cut in
    def slab_names(self):
        return ["leaf_frame"] if "leaf_frame" in self.M else self.names("leaf_board_")

    def holes(self, y_mm, min_area=40.0):
        """The openings: the holes in a section of the slab at depth y (mm, the target's y), as shapely polygons in (x, z) mm, not touching the leaf's outer edge."""
        slab = self.region(self.slab_names(), 1, y_mm, (0, 2))
        leaf = sbox(self.X0, self.Z0, self.X0 + self.W, self.Z0 + self.H)
        g = leaf.difference(slab)
        polys = [g] if g.geom_type == "Polygon" else [h for h in getattr(g, "geoms", []) if h.geom_type == "Polygon"]
        inner = leaf.buffer(-1.0)
        return [p for p in polys if p.area >= min_area and inner.contains(p)]

    def leaf_bounds_mm(self):
        lo, hi = self.bbox(self.slab_names())
        return lo, hi


def assemble(N, mod, rec, furn_cache):
    """The kind plus a house's fittings, in the target's frame: parts named fit:<slot>:<part>."""
    M = dict(mod.M)
    for fur in rec["furniture"]:
        vid = fur["glb"]
        if vid not in furn_cache:
            furn_cache[vid] = load_npz(os.path.join(NPZ, "furniture_%s.npz" % vid))
        mx = np.array(fur["frame_mm"], float) / 1000.0
        for pn, (V, F) in furn_cache[vid].items():
            V2 = V.copy()
            F2 = F
            if fur.get("mirror_x"):
                V2[:, 0] = -V2[:, 0]
                F2 = F[:, ::-1]
            M["fit:%s:%s" % (fur["slot"], pn)] = (V2 + mx, F2)
    return Model(N, mod.kind, M, mod.pivot)


# ------------------------------------------------------------------ raster helpers (as 3.1's check)
def frame_for(points_mm, margin=10.0, mmpx=MMPX):
    P = np.vstack([np.asarray(p, float) for p in points_mm])
    lo, hi = P.min(0) - margin, P.max(0) + margin
    return Frame(u0=lo[0] / 1000, v0=lo[1] / 1000, width=(hi[0] - lo[0]) / 1000, height=(hi[1] - lo[1]) / 1000, mm_per_px=mmpx)


def _fill(pts, fr):
    img = Image.new("1", (fr.shape[1], fr.shape[0]), 0)
    P = np.asarray(pts, float) / 1000.0
    Q = np.stack(fr.to_px(P[:, 0], P[:, 1]), 1)
    ImageDraw.Draw(img).polygon([tuple(q) for q in Q], fill=1, outline=1)
    return np.array(img, bool)


def raster_geom(g, fr):
    out = np.zeros(fr.shape, bool)
    geoms = [g] if g.geom_type == "Polygon" else list(getattr(g, "geoms", []))
    for p in geoms:
        if p.geom_type != "Polygon" or p.is_empty:
            continue
        m = _fill(list(p.exterior.coords), fr)
        for h in p.interiors:
            m &= ~_fill(list(h.coords), fr)
        out |= m
    return out


def fill_pinholes(mask, max_px=40):
    holes, n = ndimage.label(~mask)
    if n == 0:
        return mask
    sizes = ndimage.sum(np.ones_like(holes), holes, index=np.arange(1, n + 1))
    return mask | np.isin(holes, np.nonzero(sizes <= max_px)[0] + 1)


def depth_labels(M, fr, layers):
    """What shows from the street at each pixel: the part with the lowest y (nearest the street) wins; labels are layer numbers (1-based)."""
    lab = np.zeros(fr.shape, np.int8)
    depth = np.full(fr.shape, np.inf)
    for name, (V, F) in M.items():
        layer = layer_of(name)
        if layer not in layers:
            continue
        sil = silhouette({name: (V, F)}, (0, 2), fr)
        y = V[:, 1].min()
        sel = sil & (y < depth)
        lab[sel] = layers.index(layer) + 1
        depth[sel] = y
    return lab


def union_sil(M, names, fr):
    if not names:
        return np.zeros(fr.shape, bool)
    return silhouette({n: M[n] for n in names}, (0, 2), fr)


def shp_poly(g):
    """A drawing's polygons ({'exterior': pts, 'holes': [...]}) as one shapely geometry."""
    out = []
    for p in g:
        pg = Polygon(p["exterior"], p.get("holes", []))
        out.append(pg.buffer(0))
    return unary_union(out) if out else Polygon()


# ------------------------------------------------------------------ A: the drawing comparisons
def check_drawings(N, mod, rep, overlays):
    k = mod.kind
    D = td.draw_kind(N, k)
    fs = mod.fs
    jl, jr = fs["jamb_x"]["left"][0], fs["jamb_x"]["right"][1]
    top = fs["head_top"]
    layers = ("frame", "tglass", "leaf", "stone")
    fr = frame_for([[jl - 5, -5], [jr + 5, top + 5]], 0.0)
    lab = depth_labels(mod.M, fr, layers)
    hh, ww = fr.shape
    u = (fr.u0 + (np.arange(ww) + 0.5) * fr.mm_per_px / 1000) * 1000
    v = (fr.v0 + fr.height - (np.arange(hh) + 0.5) * fr.mm_per_px / 1000) * 1000
    window = (u[None, :] >= jl) & (u[None, :] <= jr) & (v[:, None] >= 0) & (v[:, None] <= top)
    pairs = [("frame", "frame", D["frame"]), ("tglass", "transom_glass", D["transom_glass"]), ("leaf", "visible", D["visible"])]
    for layer, dname, geom in pairs:
        a = fill_pinholes((lab == layers.index(layer) + 1) & window)
        b = fill_pinholes(raster_geom(geom, fr) & window)
        c = verdict(compare(a, b, MMPX))
        rep.add("A1:%s:%s" % (k, dname), c["ok"], {x: c[x] for x in ("iou", "p95_mm", "max_mm")}, "IoU >= 0.97, p95 <= 2, worst <= 6",
                "front view, what shows from the street (the nearest part wins), inside the frame", group="A", kind=k)
        if overlays:
            overlay(a, b, os.path.join(overlays, "A1_%s_%s.png" % (k, dname)))
    # the openings: holes in the slab (T3: at three depths), against the drawn openings
    spec = mod.spec
    # the openings are THROUGH holes: sections at depth 5 (T3: the outer pockets at 0.1, the small light at 20, below the field's 12); a keyhole's blind pocket (2.2 deep) is not an opening
    depth_sets = [("t3", 3.2, ("upper_panel", "lower_panel")), ("t3", 20.0, ("small_light",))] if k == "T3" else [("all", 5.0, None)]
    got = []
    for tag, dy, ids in depth_sets:
        for h in mod.holes(mod.LY0 + dy):
            got.append(h)
    drawn = unary_union([g for g in D["openings"].values()]) if D["openings"] else Polygon()
    if got and not drawn.is_empty:
        m = unary_union(got)
        px = 0.25 if k == "F6" else MMPX                                    # the spyhole is 14 across: 0.25 mm a pixel
        fr2 = frame_for([[mod.X0, mod.Z0], [mod.X0 + mod.W, mod.Z0 + mod.H]], 5.0, px)
        c = verdict(compare(raster_geom(m, fr2), raster_geom(drawn, fr2), px))
        rep.add("A2:%s:openings" % k, c["ok"], {x: c[x] for x in ("iou", "p95_mm", "max_mm")}, "IoU >= 0.97, p95 <= 2, worst <= 6",
                "the holes the leaf is cut with (sections at depth) against the drawn openings", group="A", kind=k)
    elif not spec["leaf"]["openings"]:
        rep.add("A2:%s:openings" % k, True, "none, as drawn", "no opening", group="A", kind=k)
    else:
        rep.add("A2:%s:openings" % k, False, "no hole found in the leaf", "the drawn openings", group="A", kind=k)
    # mouldings: the ring of the target's drawing, grown by the lap the 3.1 build gives a bolection (4.8): the drawing's ring starts at the opening's edge
    mo = spec["mouldings"]["outside"]
    if k in ("T1", "F1", "F2", "F3"):
        names = mod.names("moulding_bolection_", "moulding_ovolo_")
        fr3 = frame_for([[mod.X0, mod.Z0], [mod.X0 + mod.W, mod.Z0 + mod.H]], 5.0)
        a = union_sil(mod.M, names, fr3)
        lap = mo.get("lap_over_framing_mm", 4.8) if mo["kind"] == "bolection" else 0.0
        rings = []
        for o in spec["leaf"]["openings"]:
            if o["type"] != "panel":
                continue
            outer = D["openings"][o["id"]]
            emb = 0.0 if lap else 0.5                       # a stuck moulding stands 0.5 into the framing (the build's embed)
            rings.append(outer.buffer(lap + emb, join_style=2).difference(outer.buffer(-(mo["width_on_face"] - lap), join_style=2)))
        c = verdict(compare(a, raster_geom(unary_union(rings), fr3), MMPX))
        rep.add("A3:%s:mouldings" % k, c["ok"], {x: c[x] for x in ("iou", "p95_mm", "max_mm")}, "IoU >= 0.97, p95 <= 2, worst <= 6",
                "the moulding rings against the drawn ring grown by the moulding's lap over the framing (%.1f): the target's ring starts at the opening's edge" % lap, group="A", kind=k)
        if lap:
            # 14 Oct (try 3): target_drawing.py now draws the ring with the lap (it was owed the change by both try 2 reviews), so the drawing's own ring is the comparison
            c = verdict(compare(a, raster_geom(D["mouldings"], fr3), MMPX))
            rep.add("A3:%s:mouldings_literal" % k, c["ok"], {x: c[x] for x in ("iou", "p95_mm", "max_mm")}, "IoU >= 0.97, p95 <= 2, worst <= 6",
                    "EXTRA: the same against the drawing's ring exactly as drawn (target_drawing.py draws the ring %.1f outside the opening's edge since the try 2 reviews)" % lap,
                    group="A", extra=True, kind=k)
    if k == "T2":
        fr4 = frame_for([[fs["glass_opening_x"][0], fs["glass_opening_z"][0]], [fs["glass_opening_x"][1], fs["glass_opening_z"][1]]], 5.0, 0.25)
        a = union_sil(mod.M, ["lead_came"], fr4)
        b = raster_geom(D["lead_came"], fr4)
        c = verdict(compare(a, b, 0.25))
        rep.add("A3:%s:lead_came" % k, c["ok"], {x: c[x] for x in ("iou", "p95_mm", "max_mm")}, "IoU >= 0.97, p95 <= 2, worst <= 6", "the leaded fanlight's came against the drawn came (6 mm bars, at 0.25 mm a pixel)",
                group="A", kind=k)
    if k == "F7":
        fr5 = frame_for([[mod.X0, mod.Z0], [mod.X0 + mod.W, mod.Z0 + mod.H]], 5.0, 0.25)
        a = union_sil(mod.M, ["iron_nail_heads"], fr5)
        c = verdict(compare(a, raster_geom(D["nail_heads"], fr5), 0.25))
        rep.add("A3:%s:nail_heads" % k, c["ok"], {x: c[x] for x in ("iou", "p95_mm", "max_mm")}, "IoU >= 0.97, p95 <= 2, worst <= 6", "the 18 nail heads against the drawn ones", group="A", kind=k)
    return D


def check_fitting_drawings(N, rec_mod, rep, D, house):
    """Extras: each placed fitting's silhouette against the drawing's own polygon for the kind's first house."""
    k = rec_mod.kind
    fr = frame_for([[rec_mod.X0, rec_mod.Z0], [rec_mod.X0 + rec_mod.W, rec_mod.Z0 + rec_mod.H]], 5.0)
    for key, g in D["furniture"].items():
        slot = key.split(":")[0]
        if slot in ("scraper", "bell", "fixing"):
            continue
        names = [n for n in rec_mod.M if n.startswith("fit:%s:" % slot) and not n.endswith("liner")]
        if not names:
            continue
        a = ndimage.binary_fill_holes(union_sil(rec_mod.M, names, fr))
        b = raster_geom(g, fr)
        if slot == "handle" and "lever" in json.dumps(N["furniture"]["handle"].get(key.split(":")[1], {})).lower() and False:
            continue
        c = verdict(compare(a, b, MMPX))
        rep.add("A3:%s:%s" % (k, key), c["ok"], {x: c[x] for x in ("iou", "p95_mm", "max_mm")}, "IoU >= 0.97, p95 <= 2, worst <= 6",
                "EXTRA: the fitting's silhouette against the drawing's polygon (the target draws each fitting as a simple shape)", group="A", extra=True, kind=k)


def surface_profile(region, axes_d_h, d_samples):
    """The upper (street-side) surface of a section region: for each d, the greatest h at that d."""
    out = []
    for d in d_samples:
        x = region.intersection(LineString([(d, -50.0), (d, 50.0)]))
        pts = []
        for g in ([x] if x.geom_type != "GeometryCollection" and not hasattr(x, "geoms") else list(x.geoms)):
            pts += list(g.coords) if hasattr(g, "coords") else []
        out.append(max(p[1] for p in pts) if pts else None)
    return out


def profile_rows(N, mod, rep):
    k = mod.kind
    spec = N["kinds"][k]
    mo = spec["mouldings"]["outside"]
    ops = {o["id"]: o for o in spec["leaf"]["openings"]}

    def compare_profile(rid, poly, prof, note, hmin=None):
        """Distances (mm) from the target's profile line, sampled every 0.25 mm, to the model's section boundary (both in d, h): p95 and worst. With hmin only the
        boundary above that h counts (a moulding's closing edges on the panel face are not its profile)."""
        from shapely.geometry import MultiLineString
        line = LineString([(d, h) for d, h in prof])
        pts = [line.interpolate(s) for s in np.arange(0.0, line.length, 0.25)] + [Point(prof[-1])]
        if hmin is None:
            bnd = poly.boundary
        else:
            segs = []
            for g in ([poly] if poly.geom_type == "Polygon" else list(poly.geoms)):
                cs = list(g.exterior.coords)
                segs += [(a_, b_) for a_, b_ in zip(cs[:-1], cs[1:]) if a_[1] > hmin and b_[1] > hmin]
            bnd = MultiLineString(segs) if segs else poly.boundary
        ds = [bnd.distance(p) for p in pts]
        c = {"iou": 1.0, "p95_mm": round(float(np.percentile(ds, 95)), 2), "max_mm": round(float(max(ds)), 2)}
        verdict(c, "profile")
        rep.add(rid, c["ok"], {x: c[x] for x in ("p95_mm", "max_mm")}, "p95 <= 1.5, worst <= 3", note, group="A", kind=k)

    def section_poly(reg, f):
        polys = [reg] if reg.geom_type == "Polygon" else [g for g in reg.geoms if g.geom_type == "Polygon"]
        return unary_union([Polygon([f(px, py) for px, py in g.exterior.coords]) for g in polys])
    if k in ("T1", "F1", "F2"):                         # a bolection on the top edge of the top-left (or the last) panel: section at the panel's middle
        o = list(ops.values())[-1] if k == "F2" else ops["top_left"]
        x = mod.X0 + 0.5 * (o["u0"] + o["u1"])
        name = [n for n in mod.M if n.startswith("moulding_bolection_") and n.endswith(o["id"])][0]
        reg = mod.region(name, 0, x, (1, 2))                    # (y, z)
        z_outer = mod.Z0 + o["v1"] + 4.8
        poly = section_poly(reg, lambda y, z: (z_outer - z, mod.LY0 - y))
        compare_profile("A4:%s:bolection" % k, poly, mo["profile_dh"], "the moulding's section across the top edge of panel %s (d from the moulding's outer edge, h proud of the framing) against the target's profile line (the moulding's own surface, not its closing edges on the panel)" % o["id"], hmin=-17.2)
    if k == "F3":
        o = ops["long_l"]
        z = mod.Z0 + 0.5 * (o["v0"] + o["v1"])
        reg = mod.region("moulding_ovolo_long_l", 2, z, (0, 1))     # (x, y)
        x_outer = mod.X0 + o["u0"]
        poly = section_poly(reg, lambda px, py: (px - x_outer, mod.LY0 - py))
        compare_profile("A4:F3:stuck_ovolo", poly, mo["profile_dh"][:-1], "the stuck ovolo's section across the left edge of long_l against the target's profile line (its surface, not its closing edges)", hmin=-17.2)
    if k == "T3":
        o = ops["lower_panel"]
        z = mod.Z0 + 0.5 * (o["v0"] + o["v1"])
        reg = mod.region("leaf_frame", 2, z, (0, 1))
        x_outer = mod.X0 + o["u0"]
        poly = section_poly(reg, lambda px, py: (px - x_outer, py - mod.LY0))
        prof = [(d, h) for d, h in mo["profile_dh"] if d <= 60.0]
        compare_profile("A4:T3:embossed_step", poly, prof, "the sheet's section over the lower panel's left edge (d inward from the outer outline, depth below the border face): the outer cove and the margin (d to 60) against the target's profile line")
        inner = o["inner"]
        xm = mod.X0 + 0.5 * (inner["u0"] + inner["u1"])
        seg = reg.intersection(LineString([(xm, mod.LY0 - 10.0), (xm, mod.LY0 + 60.0)]))
        ys = [p[1] for g in ([seg] if hasattr(seg, "coords") else list(seg.geoms)) for p in g.coords] if not seg.is_empty else []
        rep.within("A4:T3:field_depth", (min(ys) - mod.LY0) if ys else -1.0, 12.0, 0.2, "the field inside the inner outline lies 12 below the border face (13 Oct, from the try 1 reviews: two steps of 6; was 6 in all)", group="A", kind=k)
    if k == "F7":
        jx = mod.X0 + spec["leaf"]["board_edges_u"][1]
        reg = mod.region(mod.names("leaf_board_"), 2, mod.Z0 + 600.0, (0, 1))
        poly = section_poly(reg, lambda px, py: (px - jx, -(py - mod.LY0)))
        compare_profile("A4:F7:v_joint", poly, [tuple(q) for q in mo["profile"]], "the V joint between two boards in section (h negative below the face) against the target's profile line")
    if k == "F6":
        flutes = "glass_fanlight_flutes"
        fs = mod.fs
        xs = 0.5 * (fs["glass_opening_x"][0] + fs["glass_opening_x"][1])
        reg = mod.region(flutes, 2, 0.5 * (fs["glass_opening_z"][0] + fs["glass_opening_z"][1]), (0, 1))
        g = N["glass"]["reeded_4mm"]
        ys_by_x = []
        for xx in np.arange(xs - 30.0, xs + 30.0, 0.25):
            seg = reg.intersection(LineString([(xx, 0.0), (xx, 400.0)]))
            ys = [p[1] for gg in ([seg] if hasattr(seg, "coords") else list(seg.geoms)) for p in gg.coords] if not seg.is_empty else []
            ys_by_x.append(min(ys) if ys else None)
        arr = np.array([y for y in ys_by_x if y is not None])
        depth = float(arr.max() - arr.min())
        # crest positions: local minima of y (nearest the street)
        yy = np.array([y if y is not None else np.nan for y in ys_by_x])
        crests = [i for i in range(1, len(yy) - 1) if yy[i] <= yy[i - 1] and yy[i] < yy[i + 1] and yy[i] < np.nanmin(yy) + 0.2]
        xs_arr = np.arange(xs - 30.0, xs + 30.0, 0.25)
        pitch = float(np.mean(np.diff([xs_arr[i] for i in crests]))) if len(crests) > 2 else 0.0
        rep.add("A4:F6:reeded", abs(depth - g["flute_depth"]) <= 0.15 and abs(pitch - g["flute_pitch"]) <= 0.1, {"depth": round(depth, 2), "pitch": round(pitch, 2)},
                {"depth": g["flute_depth"], "pitch": g["flute_pitch"]}, "the reeded glass in section: flutes 6 apart, 1.2 deep", group="A", kind=k)


# ------------------------------------------------------------------ B: the target's own records
def interior_holes(mod):
    """{id: shapely hole} matched to the spec's openings by nearest centre; T3 reads three depths."""
    spec = mod.spec
    ops = spec["leaf"]["openings"]
    out, inner = {}, {}
    if mod.kind == "T3":
        cand = {"upper_panel": None, "lower_panel": None}
        # 14 Oct (try 3): a quirk groove 3 deep lies outside each outline (in the face, and in the margin), so a section at 0.1 below the face would take the groove's outer edge for the pocket:
        # the pockets are read below the grooves, at 3.2 (outer) and 9.2 (inner), where the quarter-circle coves stand 0.89 inside the outline (well inside the 3 mm opening tolerance)
        outer_h = mod.holes(mod.LY0 + 3.2)
        inner_h = mod.holes(mod.LY0 + 9.2)                       # the margin lies 6 below the face and its quirk 3 deeper: the inner pockets are read below it
        light_h = mod.holes(mod.LY0 + 20.0)                      # the field lies 12 below the face: only the small light is a hole at 20
        for o in ops:
            c = Point(mod.X0 + 0.5 * (o["u0"] + o["u1"]), mod.Z0 + 0.5 * (o["v0"] + o["v1"]))
            pool = light_h if o["id"] == "small_light" else outer_h
            if pool:
                out[o["id"]] = min(pool, key=lambda p: p.centroid.distance(c))
            if o.get("inner") and inner_h:
                iv = o["inner"]
                ci = Point(mod.X0 + 0.5 * (iv["u0"] + iv["u1"]), mod.Z0 + 0.5 * (iv["v0"] + iv["v1"]))
                inner[o["id"]] = min(inner_h, key=lambda p: p.centroid.distance(ci))
        return out, inner
    hs = mod.holes(mod.LY0 + 5.0)
    used = set()
    for o in ops:
        c = Point(mod.X0 + 0.5 * (o["u0"] + o["u1"]), mod.Z0 + 0.5 * (o["v0"] + o["v1"]))
        free = [(i, h) for i, h in enumerate(hs) if i not in used]
        if not free:
            break
        i, h = min(free, key=lambda t: t[1].centroid.distance(c))
        used.add(i)
        out[o["id"]] = h
    return out, inner


def bounds_u_v(mod, g):
    b = g.bounds
    return [b[0] - mod.X0, b[2] - mod.X0, b[1] - mod.Z0, b[3] - mod.Z0]


def row_PL(N, mod, rep, holes, inner_holes):
    k = mod.kind
    spec = mod.spec
    lf = spec["leaf"]
    ops = lf["openings"]
    for c in N["checks"]:
        if c["group"] != "PL" or c["kind"] != k:
            continue
        t, rid = c["type"], c["id"]
        if t == "count":
            n = len(holes)
            rep.add(rid, n == c["expect"], n, c["expect"], "openings found in the leaf by sections at depth (%s)" % ("panel and light holes" if k != "T3" else "outer pockets and the light"), group="PL", kind=k)
        elif t == "opening_bounds":
            g = holes.get(c["opening"])
            if g is None:
                rep.add(rid, False, "no hole", c["expect"], group="PL", kind=k)
                continue
            got = bounds_u_v(mod, g)
            rep.add(rid, all(abs(got[i] - c["expect"][i]) <= c["tol"] for i in range(4)), [round(x, 1) for x in got], c["expect"], tol=c["tol"], group="PL", kind=k)
        elif t == "inner_bounds":
            g = inner_holes.get(c["opening"])
            if g is None:
                rep.add(rid, False, "no inner outline", c["expect"], group="PL", kind=k)
                continue
            got = bounds_u_v(mod, g)
            rep.add(rid, all(abs(got[i] - c["expect"][i]) <= c["tol"] for i in range(4)), [round(x, 1) for x in got], c["expect"], tol=c["tol"], group="PL", kind=k)
        elif t == "raked_head":
            g = holes.get(c["opening"])
            b = g.bounds
            coords = list(g.exterior.coords)
            left_z = max(p[1] for p in coords if abs(p[0] - b[0]) < 0.3)
            right_z = max(p[1] for p in coords if abs(p[0] - b[2]) < 0.3)
            rise = (right_z - left_z) if c["expect"]["rise_toward"] == "right" else (left_z - right_z)
            rep.add(rid, abs(rise - c["expect"]["head_rise"]) <= c["tol"], round(rise, 2), c["expect"], tol=c["tol"], group="PL", kind=k)
        elif t == "members":
            m = measured_members(mod, holes, inner_holes)
            want = c["expect"]
            ok = all(key in m and abs(m[key] - v) <= c["tol"] for key, v in want.items())
            rep.add(rid, ok, {key: round(m.get(key, float("nan")), 1) for key in want}, want, tol=c["tol"], group="PL", kind=k,
                    note=("" if k != "T3" else "T3: border 65 has no feature in the target's own T3 outlines; measured here as the flat margin between the outer and the inner outline at the sides (62.5)"))
        elif t == "framing":
            leaf = sbox(mod.X0, mod.Z0, mod.X0 + mod.W, mod.Z0 + mod.H)
            allh = list(holes.values())
            bad = [i for i, g in enumerate(allh) if not leaf.buffer(-c["expect"]["min_framing_mm"]).contains(g)]
            rep.add(rid, not bad, "min framing %.1f mm" % (min(min(g.bounds[0] - mod.X0, mod.X0 + mod.W - g.bounds[2], g.bounds[1] - mod.Z0, mod.Z0 + mod.H - g.bounds[3]) for g in allh) if allh else 99.0),
                    ">= 20 mm", "every opening lies inside the leaf with at least 20 mm of framing to its edge", group="PL", kind=k)


def measured_members(mod, holes, inner_holes):
    """Stiles, rails, muntin, bars (structural mm) from the holes the leaf is cut with."""
    k = mod.kind
    ids = [o["id"] for o in mod.spec["leaf"]["openings"]]
    gs = {i: bounds_u_v(mod, holes[i]) for i in ids if i in holes}
    W, H = mod.W, mod.H
    out = {}
    if not gs:
        return out
    if k == "T3":
        up, lo = gs["upper_panel"], gs["lower_panel"]
        iu = bounds_u_v(mod, inner_holes["upper_panel"])
        out["border"] = iu[0] - up[0]
        return out
    u0s, u1s, v0s, v1s = [g[0] for g in gs.values()], [g[1] for g in gs.values()], [g[2] for g in gs.values()], [g[3] for g in gs.values()]
    out["stile_left"], out["stile_right"] = min(u0s), W - max(u1s)
    out["top_rail"], out["bottom_rail"] = H - max(v1s), min(v0s)
    rows = sorted({(round(g[2], 1), round(g[3], 1)) for g in gs.values()})
    cols = sorted({(round(g[0], 1), round(g[1], 1)) for g in gs.values()})
    if k in ("T1", "F1"):
        out["lock_rail"] = rows[1][0] - rows[0][1]
        out["muntin"] = cols[1][0] - cols[0][1]
    elif k == "F2":
        out["lock_rail"] = rows[1][0] - rows[0][1]
        out["frieze_rail"] = rows[2][0] - rows[1][1]
        out["muntin"] = cols[1][0] - cols[0][1]
    elif k == "F3":
        out["muntin"] = cols[1][0] - cols[0][1]
    elif k == "T2":
        out["bar"] = rows[1][0] - rows[0][1]
        out["light_h"] = rows[0][1] - rows[0][0]
    elif k == "F4":
        out["bar"] = cols[1][0] - cols[0][1]
        out["light_w"] = cols[0][1] - cols[0][0]
    return out


# ---- CV
def ray_first_hit(M, origin, d, names=None):
    """First triangle hit along a ray (Moller-Trumbore, all parts): returns (t, part name) or None. Millimetres."""
    best = (1e18, None)
    o = np.asarray(origin, float)
    d = np.asarray(d, float)
    for n, (V, F) in M.items():
        P = V * 1000.0
        a, b, c = P[F[:, 0]], P[F[:, 1]], P[F[:, 2]]
        e1, e2 = b - a, c - a
        h = np.cross(d, e2)
        det = (e1 * h).sum(1)
        ok = np.abs(det) > 1e-12
        inv = np.zeros_like(det)
        inv[ok] = 1.0 / det[ok]
        s = o - a
        u = (s * h).sum(1) * inv
        q = np.cross(s, e1)
        v = (q @ d) * inv
        t = (e2 * q).sum(1) * inv
        hit = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-6)
        if hit.any():
            tm = t[hit].min()
            if tm < best[0]:
                best = (float(tm), n)
    return best if best[1] else None


def row_CV(N, mod, rep):
    k = mod.kind
    fs = mod.fs
    for c in N["checks"]:
        if c["group"] != "CV" or c["kind"] != k:
            continue
        rid, t = c["id"], c["type"]
        if t == "coverage_elevation":
            x0, x1 = fs["stop_edges_x"]
            gz = fs["glass_opening_z"][1]
            fr = frame_for([[x0, 0.0], [x1, gz]], 0.0, 0.5)
            cov = np.zeros(fr.shape, bool)
            for n, (V, F) in mod.M.items():
                if n.startswith("fit:") or n.startswith("net_"):
                    continue
                cov |= silhouette({n: (V, F)}, (0, 2), fr)
            hh, ww = fr.shape
            u = (fr.u0 + (np.arange(ww) + 0.5) * fr.mm_per_px / 1000) * 1000
            v = (fr.v0 + fr.height - (np.arange(hh) + 0.5) * fr.mm_per_px / 1000) * 1000
            allowed_gap = (v[:, None] < c["expect"]["foot_gap_mm"] + 0.5)
            inside = (u[None, :] > x0 + 0.3) & (u[None, :] < x1 - 0.3) & (v[:, None] > 0.3) & (v[:, None] < gz - 0.3)
            holes_ = inside & ~cov & ~allowed_gap
            area = float(holes_.sum() * (MMPX ** 2))
            rep.add(rid, area <= c["expect"]["max_hole_mm2"], {"uncovered_mm2": round(area, 2)}, c["expect"], "union of every part's front view inside the clear opening, except the 10 mm foot gap", group="CV", kind=k)
        elif t == "coverage_angle":
            res = angle_rows(N, mod, c)
            rep.add(rid, res["ok"], res["measured"], c["expect"], res["note"], c["tol"], group="CV", kind=k)
        elif t == "inward":
            lo, hi = mod.bbox(mod.slab_names())
            jam = mod.bbox("frame_jamb_L")
            stop_rear = fs["frame_front_y"] + fs["stop_depth"]
            tr_lo = mod.bbox("frame_transom")[0][2]
            leaf_front = float(lo[1])
            ok = leaf_front >= stop_rear - 1e-3 and hi[2] > tr_lo
            rep.add(rid, ok, {"leaf_front_y": round(leaf_front, 2), "stops_rear_y": stop_rear, "leaf_head_z": round(float(hi[2]), 2), "transom_underside_z": round(float(tr_lo), 2)}, c["expect"],
                    "leaf front face at or behind the stops' rear face; its head above the transom's underside", group="CV", kind=k)
        elif t == "joints":
            res = joints_row(N, mod, c)
            rep.add(rid, res["ok"], res["measured"], c["expect"], res["note"], c["tol"], group="CV", kind=k)


def angle_rows(N, mod, c):
    """The 60 degree plan row on the mesh: stop edges, leaf edges and the transom's underside read from the parts, and real rays grazing each stop's rear corner."""
    fs = mod.fs
    M = mod.M
    jl = mod.bbox("frame_jamb_L")
    jr = mod.bbox("frame_jamb_R")
    lo, hi = mod.bbox(mod.slab_names())
    tr = mod.bbox("frame_transom")
    stop_l, stop_r = float(jl[1][0]), float(jr[0][0])
    lap_left, lap_right = stop_l - float(lo[0]), float(hi[0]) - stop_r
    lap_head = float(hi[2]) - float(tr[0][2])
    stop_rear_y = fs["frame_front_y"] + fs["stop_depth"]
    setback = float(lo[1]) - stop_rear_y
    reach = setback * math.tan(math.radians(60.0))
    need = max(5 * c["expect"]["margin_mm"], c["expect"]["margin_mm"] + reach)
    got = {"lap_left_mm": round(lap_left, 2), "lap_right_mm": round(lap_right, 2), "lap_head_mm": round(lap_head, 2), "setback_mm": round(setback, 2), "sideways_reach_mm": round(reach, 2), "min_lap_mm": round(need, 2)}
    ok = all(abs(got[a] - c["expect"][a]) <= c["tol"] for a in got) and min(lap_left, lap_right, lap_head) >= need
    # real rays: from far on the street side, at 60 degrees from the normal, grazing each stop's rear corner (0.05 clear), at several heights; the first hit must be the leaf
    s60, c60 = math.sin(math.radians(60.0)), math.cos(math.radians(60.0))
    hits = []
    for z in np.linspace(mod.Z0 + 100.0, mod.Z0 + mod.H - 150.0, 7):
        for side, (xc, dx) in (("left", (stop_l, -s60)), ("right", (stop_r, s60))):
            d = np.array([dx, c60, 0.0])
            corner = np.array([xc, stop_rear_y, z])
            origin = corner - 120.0 * d + np.array([-0.05 * np.sign(dx) * -1.0, 0.0, 0.0])
            origin[0] += 0.05 * (1.0 if side == "left" else -1.0)
            h = ray_first_hit(M, origin, d)
            hits.append((side, round(float(z), 0), h[1] if h else None))
    for xq in np.linspace(mod.X0 + 150.0, mod.X0 + mod.W - 150.0, 5):
        d = np.array([0.0, c60, s60])
        corner = np.array([xq, stop_rear_y, float(tr[0][2])])
        origin = corner - 120.0 * d + np.array([0.0, 0.0, -0.05])
        h = ray_first_hit(M, origin, d)
        hits.append(("head", round(float(xq), 0), h[1] if h else None))
    bad = [(s, p, n) for s, p, n in hits if n is None or layer_of(n) not in ("leaf",)]
    ok = ok and not bad
    note = "stop edges, leaf edges and the transom's underside read from the parts; %d rays at 60 degrees grazing the stops' rear corners all land on the leaf" % len(hits) if not bad else "rays that did not land on the leaf: %s" % bad[:4]
    return {"ok": ok, "measured": {**got, "rays": len(hits), "rays_off_leaf": len(bad)}, "note": note}


def joints_row(N, mod, c):
    names = sorted(mod.names("leaf_board_"), key=lambda n: int(n.split("_")[-1]))
    tongues = []
    for n in names[:-1]:
        V = mod.M[n][0] * 1000.0
        edge = float(V[np.abs(V[:, 1] - (mod.LY0 + 2.0)) < 0.01][:, 0].max())
        tongues.append(float(V[:, 0].max() - edge))
    rays = []
    s60, c60 = math.sin(math.radians(60.0)), math.cos(math.radians(60.0))
    miss = 0
    edges = N["kinds"]["F7"]["leaf"]["board_edges_u"][1:-1]
    for u in edges:
        for ang in (0.0, 60.0, -60.0):
            d = np.array([math.sin(math.radians(ang)), math.cos(math.radians(ang)), 0.0])
            x = mod.X0 + u
            for z in (400.0, 1200.0):
                origin = np.array([x, mod.LY0 - 60.0, z]) - np.array([d[0], 0, 0]) * (60.0 / d[1])
                h = ray_first_hit(mod.M, origin, d)
                rays.append(h)
                if h is None:
                    miss += 1
    ok = min(tongues) >= c["expect"]["tongue_mm"] - c["tol"] and miss == 0
    return {"ok": ok, "measured": {"tongue_mm": [round(t, 2) for t in tongues], "rays": len(rays), "rays_through": miss}, "note": "the tongue of each joint, and rays at 0 and 60 degrees through every joint's line"}


# ---- FU
ANCHORS = {"letter_plate": "iron_letter_plate", "latch": ("iron_lock", "iron_lock_collar"), "keyhole": "iron_keyhole_plate", "number": None, "scraper": None, "bell": "iron_bellpush"}
# the part(s) whose bounding box is the handle's place and size; and the part(s) that lie ON the leaf (the footprint the FIT rows test against mouldings and beads): a lever stands 55 proud, so
# only its rose (or boss) and its long backplate lie on the leaf; a bar pull's posts' roses; a thumb latch's plate
HANDLE_ANCHOR = {"HD1": ("iron_knob_rose",), "HD2a": ("iron_rose",), "HD2b": ("iron_rose",), "HD2c": ("iron_rose",), "HD3": ("iron_pull_bar", "iron_pull_post_u", "iron_pull_post_l"), "HD4": ("iron_latch_plate",)}
HANDLE_FOOT = {"HD1": ("iron_knob_rose",), "HD2a": ("iron_rose",), "HD2b": ("iron_rose", "iron_backplate"), "HD2c": ("iron_rose", "iron_backplate"), "HD3": ("iron_pull_post_u", "iron_pull_post_l"),
               "HD4": ("iron_latch_plate",)}


def fitting_centre(mod, slot, variant):
    """The fitting's anchor part's bbox centre and size in the target's frame (mm), from the assembled house."""
    if slot == "handle":
        an = list(HANDLE_ANCHOR[variant])
    elif slot == "number":
        an = [n.split(":", 2)[2] for n in mod.M if n.startswith("fit:number:")]
    elif slot == "scraper":
        an = [n.split(":", 2)[2] for n in mod.M if n.startswith("fit:scraper:")]
    else:
        a = ANCHORS[slot]
        an = list(a) if isinstance(a, tuple) else [a]
    names = [n for n in mod.M if n.startswith("fit:%s:" % slot) and n.split(":", 2)[2] in an]
    if not names:
        return None
    lo, hi = mod.bbox(names)
    return (lo + hi) / 2.0, hi - lo


def row_FU(N, kind, mod_house, rep):
    spec = N["kinds"][kind]
    lf = spec["leaf"]
    fs = mod_house.fs
    for c in N["checks"]:
        if c["group"] != "FU" or c["kind"] != kind or c.get("type") in ("kind_fixing", "grip_gap", "thumb_reach", "scraper_facets"):
            continue
        slot, var = c["slot"], c["variant"]
        got = fitting_centre(mod_house, slot, var)
        if got is None:
            rep.add(c["id"], False, "no part placed", c["expect"], group="FU", kind=kind)
            continue
        ctr, size = got
        u, v = ctr[0] - mod_house.X0, ctr[2] - mod_house.Z0
        ex = c["expect"]
        pl = ex["place"]
        want_u = DS.leaf_u(N, kind, pl) if pl.get("u") is not None else None
        want_v = pl.get("v")
        ok = True
        note = []
        if slot == "number" and kind == "T1":
            want_v = 0.5 * (1207.0 + 1373.0)
        if want_u is not None and slot not in ("bell", "scraper"):
            ok &= abs(u - want_u) <= c["tol"]
        if want_v is not None and slot not in ("bell", "scraper"):
            ok &= abs(v - want_v) <= c["tol"]
        if slot == "bell":
            ok &= abs(ctr[0] - pl["x"]) <= c["tol"] and pl["z_range"][0] - c["tol"] <= ctr[2] - 0.0 <= pl["z_range"][1] + c["tol"]
        sz = ex.get("size")
        sz_got = None
        if sz:
            if slot == "scraper":
                sz_got = [round(float(size[0]), 1), round(float(size[1]), 1), round(float(size[2]), 1)]
                ok &= all(abs(sz_got[i] - sz[i]) <= c["tol"] for i in range(3))
            elif slot == "number":
                if kind == "T1":
                    sz_got = [round(float(size[0]), 1), round(float(size[2]), 1)]
                    ok &= abs(size[0] - 39.0) <= c["tol"] and abs(size[2] - (1373.0 - 1207.0)) <= c["tol"]
                else:
                    sz_got = [round(float(size[0]), 1), round(float(size[2]), 1)]
                    ok &= abs(size[2] - sz[1]) <= c["tol"]
            else:
                sz_got = [round(float(size[0]), 1), round(float(size[2]), 1)]
                if slot == "latch":
                    ok &= abs(size[0] - sz[0]) <= c["tol"]
                else:
                    ok &= abs(size[0] - sz[0]) <= c["tol"] and abs(size[2] - sz[1]) <= c["tol"]
        rep.add(c["id"], ok, {"u": round(float(u), 1), "v": round(float(v), 1), "size": sz_got}, {"u": want_u, "v": want_v, "size": sz}, c["tol"] and "the fitting's anchor part: its centre in the leaf frame and its size (a number: the digits' height; T1 stacked: 39 wide, 1207 to 1373)", c["tol"], group="FU", kind=kind)


def assemble_variants(mod_house):
    """The handle variant of an assembled house, read back from the part names (a lever has an iron_rose and an iron_lever; a knob its iron_knob_rose; a bar pull its bar; a thumb latch its plate)."""
    names = {n.split(":", 2)[2] for n in mod_house.M if n.startswith("fit:handle:")}
    for var, anchor in HANDLE_ANCHOR.items():
        if all(a in names for a in anchor):
            return [var]
    return [""]


def row_FIT(N, mod_house, rep, house):
    """A fitting stands clear of the leaf's mouldings and beads (raised features of the leaf) and of every other fitting: the first full-size close picture of F2 showed its letter plate
    lying on the long panels' moulding lip, which no row of the target covers. Footprints are the fittings' front views at 0.5 mm a pixel; the allowed overlap is 2 mm2."""
    k = mod_house.kind
    fr = frame_for([[mod_house.X0, mod_house.Z0], [mod_house.X0 + mod_house.W, mod_house.Z0 + mod_house.H]], 5.0)
    raised = [n for n in mod_house.M if n.startswith(("moulding_", "bead_")) and not n.startswith("moulding_single_")]
    slots = sorted({n.split(":")[1] for n in mod_house.M if n.startswith("fit:") and n.split(":")[1] not in ("scraper", "bell")})
    rs = union_sil(mod_house.M, raised, fr)
    foot = {}
    for s in slots:
        names = [n for n in mod_house.M if n.startswith("fit:%s:" % s) and not n.endswith("liner")]
        if s == "handle":                                   # a lever stands 55 proud: only its rose or boss and its backplate lie on the leaf (a pull's roses, a latch's plate)
            var = [f for f in assemble_variants(mod_house) if f][0]
            on_leaf = set(HANDLE_FOOT.get(var, ())) | (set(HANDLE_FOOT["HD2b"]) if var in ("HD2a", "HD2b", "HD2c") else set())
            names = [n for n in names if n.split(":", 2)[2] in on_leaf] or names
        foot[s] = ndimage.binary_fill_holes(union_sil(mod_house.M, names, fr))
    px2 = MMPX * MMPX
    over_m = {s: round(float((foot[s] & rs).sum() * px2), 1) for s in slots}
    over_f = {}
    for i, a in enumerate(slots):
        for b in slots[i + 1:]:
            v = float((foot[a] & foot[b]).sum() * px2)
            if v > 0:
                over_f["%s/%s" % (a, b)] = round(v, 1)
    ok = all(v <= 2.0 for v in over_m.values()) and all(v <= 2.0 for v in over_f.values())
    rep.add("FIT:%s:%s:clear_of_mouldings" % (k, house), ok, {"on_mouldings_mm2": over_m, "on_each_other_mm2": over_f}, "no more than 2 mm2 on a moulding, a bead or another fitting",
            "each fitting's front view against the leaf's raised mouldings and beads, and against the other fittings of the house", group="FIT", kind=k)


# ---- BP and the street
def row_BP(N, H, mods, furn_cache, rep):
    bl = N["furniture"]["bell"]["BL1"]
    names = [n for n in furn_cache["BL1"]]
    V = furn_cache["BL1"]["iron_bellpush"][0] * 1000.0 if "iron_bellpush" in furn_cache["BL1"] else None
    lo, hi = (V.min(0), V.max(0)) if V is not None else (None, None)
    reg = None
    if V is not None:
        m = Model(N, "T1", {"iron_bellpush": (furn_cache["BL1"]["iron_bellpush"][0], furn_cache["BL1"]["iron_bellpush"][1])}, np.zeros(3))
        front_y = float(lo[1])
        sec = m.region("iron_bellpush", 1, front_y + 2.0, (0, 2))
        bx = sec.bounds
        r_est = math.sqrt(max((((bx[2] - bx[0]) * (bx[3] - bx[1])) - sec.area), 0.0) / (4.0 * (1.0 - math.pi / 4.0)))
        zg = -bl["groove"]["below_centre"]
        gp = V[(np.abs(V[:, 1] - (front_y + bl["groove"]["depth"])) < 1e-3) & (np.abs(V[:, 2] - zg) <= 1.2)]
        gw = float(gp[:, 0].max() - gp[:, 0].min()) if len(gp) else 0.0
        gh = float(gp[:, 2].max() - gp[:, 2].min()) if len(gp) else 0.0
        size = [float(hi[0] - lo[0]), float(hi[2] - lo[2])]
        proud = -front_y
        t1_names = [n for n in mods["T1"].M]
        bad_names = [n for n in t1_names + names if any(w in re.split(r"[_:]", n.lower()) for w in FORBID_BELL)]
        ok = (names == ["iron_bellpush"] and abs(size[0] - 22.0) <= 0.5 and abs(size[1] - 72.6) <= 0.5 and abs(proud - 3.0) <= 0.5 and r_est <= 1.0 + 0.5 and abs(gw - 14.0) <= 0.5 and abs(gh - 2.0) <= 0.5
              and not bad_names)
        rep.add("BP-form", ok, {"parts": names, "size": [round(s, 2) for s in size], "proud": round(proud, 2), "corner_radius": round(r_est, 2), "groove": [round(gw, 2), round(gh, 2), bl["groove"]["depth"]],
                                "forbidden_names_found": bad_names}, "one part named iron_bellpush, 22 x 72.6 x 3 proud, corners at most 1, groove 14 x 2 x 1, none of bezel, button, ring, lens, led, camera, speaker",
                tol=0.5, group="BP", kind="T1")
    else:
        rep.add("BP-form", False, "no iron_bellpush in BL1", "one part", group="BP", kind="T1")
    other = []
    for k, mod in mods.items():
        for n in mod.M:
            if "bell" in n.lower() and not n.startswith("fit:"):
                other.append((k, n))
    for vid, parts in furn_cache.items():
        if "bellpush" in " ".join(parts) and vid != "BL1":
            other.append((vid, "bellpush"))
    rep.add("BP-none-elsewhere", not other, other or "only BL1 carries a bell push", {"kinds_with_bell": ["T1"]}, "no part of any kind or any other fitting is named for a bell push; BL1 is placed on T1 only", group="BP")
    modern = []
    for vid in ("BL1", "BL2"):
        parts = list(furn_cache[vid])
        if len(parts) > 1:
            modern.append((vid, parts))
        for n in parts:
            if any(w in re.split(r"[_:]", n.lower()) for w in FORBID_BELL):
                modern.append((vid, n))
    rep.add("BP-no-modern", not modern, modern or "BL1 and BL2 are one part each, no bezel, button, ring, lens, led, camera or speaker", {"max_parts_per_bell": 1}, group="BP")
    houses = [h["house"] for h in H["houses"] if any(f["variant"] == "BL1" for f in h["furniture"])]
    rep.add("BP-houses", houses == ["west_south_bay2"], houses, ["west_south_bay2"], group="BP")


def srgb_of_linear(c):
    return 255.0 * (c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)


def glb_materials(path):
    meshes, js = cd.read_glb(path)
    mats = {}
    for m in js.get("materials", []):
        pbr = m.get("pbrMetallicRoughness", {})
        mats[m.get("name")] = {"base": pbr.get("baseColorFactor"), "rough": pbr.get("roughnessFactor"), "metal": pbr.get("metallicFactor")}
    return mats, js


def row_AD_PN_WR_NM(N, H, rep, tgt_checks, paint_json, cond_json, glb_paths, texts):
    rules = {r[0]: r for r in DS.rules(H, N)}
    byid = {h["house"]: h for h in H["houses"]}
    for c in tgt_checks:
        t, rid = c["type"], c["id"]
        if t == "adjacent":
            r = rules["AD-adjacent-%s" % c["side"]]
            rep.add(rid, r[1] and c["expect"] == N["street"]["order"][c["side"]], r[2], c["what"], group="AD")
        elif t == "opposite":
            r = rules["AD-opposite"]
            rep.add(rid, r[1], r[2], c["what"], group="AD")
        elif t == "houses":
            have = [h["house"] for h in H["houses"]]
            rep.add(rid, have == c["expect"] and "east_parade_bay5" not in have, have, c["expect"], group="AD")
        elif t == "frame_set":
            r = rules["AD-frame-set"]
            rep.add(rid, r[1], r[2], c["expect"], group="AD")
        elif t == "kinds_used":
            r = rules["AD-kinds-used"]
            rep.add(rid, r[1] and sorted(r[2]) == c["expect"], r[2], c["expect"], group="AD")
        elif t == "backdrop":
            r = rules["AD-backdrop"]
            rep.add(rid, r[1] and [{"id": d["id"], "kind": d["kind"], "paint": d["paint"]} for d in H["hill"]] == c["expect"], r[2], "the hill's 12 doors as the target's rule gives them", group="AD")
        elif t == "palette":
            pal = [p["id"] for p in paint_json["door_paints"]]
            ok = pal == c["expect"] and all(h["paint"] in pal for h in H["houses"] + H["hill"])
            rep.add(rid, ok, pal, c["expect"], group="PN")
        elif t == "frames":
            fr = [f["id"] for f in paint_json["frame_colours"]]
            used = {h["frame_colour"] for h in H["houses"]}
            mats = set()
            for k, p in glb_paths.items():
                pj = json.load(open(os.path.join(NPZ, "door_%s.parts.json" % k)))
                mats |= {v["material"] for n, v in pj.items() if n.startswith("frame_")}
            rep.add(rid, fr == c["expect"] and used <= {"white", "white_grimy"} and mats <= {"paint_white", "paint_white_grimy"}, {"colours": fr, "used": sorted(used), "materials of the frame parts in the kinds": sorted(mats)}, c["expect"], group="PN")
        elif t == "light_count":
            r = rules["PN-light-doors"]
            rep.add(rid, r[1], r[2], c["expect"], group="PN")
        elif t == "srgb":
            bad = []
            seen = {}
            for k, p in glb_paths.items():
                ms, _ = glb_materials(p)
                for n, m in ms.items():
                    if n and n.startswith("paint_") and n[6:] in c["expect"]:
                        got = [round(srgb_of_linear(x)) for x in m["base"][:3]]
                        seen[n] = got
                        if any(abs(got[i] - c["expect"][n[6:]][i]) > 1 for i in range(3)):
                            bad.append((n, got))
            pal = {p["id"]: p["srgb"] for p in paint_json["door_paints"]}
            ok = not bad and all(pal[n] == v for n, v in c["expect"].items()) and all(0 <= x <= 255 for v in pal.values() for x in v)
            rep.add(rid, ok, {"paint_ids_found_in_glb": seen, "wrong": bad}, c["expect"], "the paints' sRGB in paints.json and, where a kind is built in that paint, in the .glb's own material", group="PN")
        elif t == "wear_order":
            cn = cond_json["conditions"]
            got = [cn[x]["paint_flake_share"] for x in ("kept", "tired", "neglected")]
            rep.add(rid, got == c["expect"] and got[0] < got[1] < got[2], got, c["expect"], group="WR")
        elif t == "wear_numbers":
            W = TC.load_json(TC.WEAR_T)
            pf = W["kinds"]["paint_flake"]["where"]["density"]
            hw = W["kinds"]["handle_wear"]["geometry"]["halo_eqd_mm"]
            cn = cond_json["conditions"]
            ok = (pf["range"][0] == cn["kept"]["paint_flake_share"] and pf["typical"] == cn["tired"]["paint_flake_share"] and cn["neglected"]["paint_flake_share"] == c["expect"]["neglected"]
                  and hw["p50"] == c["expect"]["halo_p50_m"] * 1000)
            rep.add(rid, ok, {"wear target range": pf["range"], "typical": pf["typical"], "halo_p50_mm": hw["p50"]}, c["expect"], "conditions.json against the wear target's own file", group="WR")
        elif t == "wear_houses":
            cnt = {kk: sum(1 for h in H["houses"] if h["condition"] == kk) for kk in ("kept", "tired", "neglected")}
            rep.add(rid, cnt == c["expect"], cnt, c["expect"], group="WR")
        elif t == "blocklist":
            hits = []
            for name, txt in texts.items():
                low = txt.lower()
                for b in TC.BLOCKLIST:
                    if re.search(r"(?<![a-z0-9'])" + re.escape(b) + r"(?![a-z0-9'])", low):
                        hits.append((name, b))
            rep.add(rid, not hits, hits or "none in %d files" % len(texts), [], "whole-word blocklist of real makers over houses.json, paints.json, conditions.json, manifest.json and every script and note of this kit", group="NM")
        elif t == "night":
            blob = re.sub(r"\s+", "", " ".join(texts.values()))
            stale = "0." + "7055"                    # the older yellow's green channel: nowhere in any text of the kit
            ok = "[1.0,0.25,0.0]" in blob and stale not in blob
            rep.add(rid, ok, {"lantern_colour_linear": H["night"]["lantern_colour_linear"]}, c["expect"], "the lantern colour (1.0, 0.25, 0.0) is in houses.json; the older yellow is nowhere", group="NM")
        elif t == "owed_text":
            lines = [txt for name, txt in texts.items() if name.startswith("NOTES")]
            bad = [i for i, s in enumerate(lines) if "—" in s or "–" in s]
            rep.add(rid, not bad, "no em dash or en dash in NOTES.md" if lines else "NOTES.md not written yet", "no em dash, en dash or italic marker", group="NM", note="NOTES.md and the lines for Jafar")


def row_MIX(N, H, rep):
    """The mixer's sample (houses_mixed_sample.json, seed 1) obeys every street rule, and the mixer gives the same street again (deterministic for a seed)."""
    s = json.load(open(os.path.join(ASSET, "houses_mixed_sample.json")))
    Hm = {"houses": s["houses"], "hill": H["hill"]}
    rows = DS.rules(Hm, N)
    bad = [r[0] for r in rows if not r[1]]
    rep.add("MIX:sample_obeys_the_street_rules", not bad, bad or [r[0] for r in rows], "every neighbour and facing rule holds on the mixed street", group="MIX")
    slots = [{"house": h["house"], "side": h["side"], "x_centre_m": h["x_centre_m"], "frame_set": h["frame_set"], "modernised": h["windows_modernised"]} for h in N["street"]["houses"]]
    again = DS.mix_new_street(N, slots, seed=1)
    same = [(a["house"], a["kind"], a["paint"]) for a in again] == [(a["house"], a["kind"], a["paint"]) for a in s["houses"]]
    rep.add("MIX:deterministic", same, same, True, "the same seed gives the same street", group="MIX")


def row_GL(N, mods, rep, tgt_checks):
    for c in tgt_checks:
        if c["type"] == "glass_keys":
            used = {v["glass"]["transom"] for v in N["kinds"].values()} | {v["glass"]["leaf"] for v in N["kinds"].values() if v["glass"]["leaf"]}
            used |= {"lens_14"}                                              # F6's spyhole lens (a leaf opening of type spyhole)
            built = {"plain_3mm": True, "leaded_diamond": "lead_came" in mods["T2"].M, "reeded_4mm": "glass_fanlight_flutes" in mods["F6"].M, "lens_14": "glass_lens" in mods["F6"].M}
            reserve = {"frosted", "wired"}
            ok = used <= set(N["glass"]) and all(built.get(u, False) for u in used) and reserve <= set(N["glass"])
            rep.add(c["id"], ok, {"used": sorted(used), "built": built, "reserve_not_placed": sorted(reserve)}, c["expect"], "every glass a kind names exists in the table and is built; frosted and wired are reserve, placed nowhere", group="GL")
        elif c["type"] == "glass_values" and c["glass"] == "reeded_4mm":
            m = mods["F6"]
            fs = m.fs
            if "glass_fanlight_flutes" not in m.M:
                rep.add(c["id"], False, "no flutes built", c["expect"], group="GL", kind="F6")
                continue
            reg = m.region("glass_fanlight_flutes", 2, 0.5 * (fs["glass_opening_z"][0] + fs["glass_opening_z"][1]), (0, 1))
            xs = 0.5 * (fs["glass_opening_x"][0] + fs["glass_opening_x"][1])
            xa = np.arange(xs - 30.0, xs + 30.0, 0.1)
            yy = []
            for x in xa:
                seg = reg.intersection(LineString([(x, 0.0), (x, 400.0)]))
                ys = [p[1] for g in ([seg] if hasattr(seg, "coords") else list(seg.geoms)) for p in g.coords] if not seg.is_empty else []
                yy.append(min(ys) if ys else np.nan)
            yy = np.array(yy)
            depth = float(np.nanmax(yy) - np.nanmin(yy))
            crest = [i for i in range(1, len(yy) - 1) if yy[i] <= yy[i - 1] and yy[i] < yy[i + 1] and yy[i] < np.nanmin(yy) + 0.15]
            cx_ = [xa[i] for i in crest]
            merged = []
            for x in cx_:
                if merged and x - merged[-1][-1] < 1.0:
                    merged[-1].append(x)
                else:
                    merged.append([x])
            cps = [float(np.mean(g)) for g in merged]
            pitch = float(np.mean(np.diff(cps))) if len(cps) > 2 else 0.0
            rep.add(c["id"], abs(depth - c["expect"]["depth"]) <= c["tol"] + 0.05 and abs(pitch - c["expect"]["pitch"]) <= c["tol"], {"pitch": round(pitch, 3), "depth": round(depth, 3), "flutes_counted": len(cps)}, c["expect"],
                    "measured in a section of the F6 transom glass", c["tol"], group="GL", kind="F6")
        elif c["type"] == "glass_values" and c["glass"] == "leaded_diamond":
            try:
                res = leaded_numbers(N, mods["T2"])
            except Exception as e:                                         # a fanlight with no came is a failing row, never a crash
                rep.add(c["id"], False, "no leaded came found: %s" % type(e).__name__, c["expect"], group="GL", kind="T2")
                continue
            ex = c["expect"]
            ok = (abs(res["came_w"] - ex["came_w"]) <= c["tol"] + 0.1 and abs(res["plain_pane_h"] - ex["plain_pane_h"]) <= c["tol"] + 0.6 and abs(res["band_h"] - ex["band_h"]) <= c["tol"] + 0.6
                  and abs(res["lozenge_w"] - ex["lozenge"][0]) <= 0.6 and abs(res["lozenge_h"] - ex["lozenge"][1]) <= 0.6 and abs(res["foot_came_above_foot"] - ex["foot_came_above_foot"]) <= c["tol"] + 0.6
                  and res["whole_lozenges"] == ex["whole_lozenges"])
            rep.add(c["id"], ok, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in res.items()}, ex, "measured on the lead came's mesh (silhouette and sections), the glass opening's own edges", c["tol"], group="GL", kind="T2")


def leaded_numbers(N, mod):
    fs = mod.fs
    gz0, gz1 = fs["glass_opening_z"]
    gx0, gx1 = fs["glass_opening_x"]
    V, F = mod.M["lead_came"]
    cx = 0.5 * (gx0 + gx1)
    # a section at x between two uprights: the horizontal cames and the crossing of the diagonals
    xm = cx + 72.5
    reg = mod.region("lead_came", 0, xm, (1, 2))                       # (y, z): came's cross-sections at that x
    zs = sorted([(g.bounds[1], g.bounds[3]) for g in ([reg] if reg.geom_type == "Polygon" else list(reg.geoms))])
    horiz = [(a, b) for a, b in zs if (b - a) <= 6.6]
    lo = zs[0]
    hi = zs[-1]
    zb = 0.5 * (lo[0] + lo[1])
    zt = 0.5 * (hi[0] + hi[1])
    came_w = lo[1] - lo[0]
    fr = frame_for([[gx0, gz0], [gx1, gz1]], 2.0, 0.25)
    sil = union_sil(mod.M, ["lead_came"], fr)
    hh, ww = fr.shape
    zmid = 0.5 * (zb + zt)
    row = int(round((fr.v0 + fr.height - zmid / 1000.0) * 1000.0 / fr.mm_per_px))
    runs = ndimage.label(sil[row])[0]
    centres = [float(np.mean(np.nonzero(runs == i)[0])) * fr.mm_per_px + fr.u0 * 1000 for i in range(1, runs.max() + 1)]
    pitch = float(np.mean(np.diff(centres))) if len(centres) > 2 else 0.0
    # uprights: runs just under the foot came, counted at a row between the glass foot and the foot came
    row2 = int(round((fr.v0 + fr.height - (0.5 * (gz0 + zb)) / 1000.0) * 1000.0 / fr.mm_per_px))
    up = ndimage.label(sil[row2])[1]
    return {"came_w": float(came_w), "plain_pane_h": float(gz1 - zt), "band_h": float(zt - zb), "lozenge_w": pitch, "lozenge_h": float(zt - zb), "foot_came_above_foot": float(zb - gz0), "whole_lozenges": int(up) - 0 - 0 if False else int(up) - 0,
            "uprights_counted": int(up)}


def row_PH(N, mods, houses_mods, H, rep, tgt_checks):
    table = TK.photo_table(N)
    for c in tgt_checks:
        k, ph = c["kind"], c["photo"]
        feats = table[(k, ph)]
        mod = houses_mods[k]
        meas = mesh_features(N, k, ph, mod)
        res, ok = {}, True
        for name, f in feats.items():
            want = f["meas"]
            got = meas.get(name)
            if got is None:
                ok = False
                res[name] = "not measurable on the mesh"
                continue
            fo = True
            for ax in ("u", "v"):
                if want[ax] is None:
                    continue
                g = got.get(ax)
                if g is None:
                    fo = False
                    continue
                fo &= max(abs(a - b) for a, b in zip(want[ax], g)) <= f["tol"][ax] + 1e-9
            ok &= fo
            res[name] = {"ok": fo, "mesh": {a: ([round(x, 4) for x in got[a]] if got.get(a) else None) for a in ("u", "v")}, "photo": want, "tol": f["tol"]}
        rep.add(c["id"], ok, {n: (r if isinstance(r, str) else ("ok" if r["ok"] else r)) for n, r in res.items()}, "every feature's fractions of the visible face within the box's own error of the photograph's recorded boxes", group="PH", kind=k,
                note="the mesh's openings (sections), fittings (anchor parts), bead and came, in fractions of the visible face")


def mesh_features(N, k, ph, mod):
    vw, vh = VIS[N["kinds"][k]["frame_set"][0]]
    holes, inner = interior_holes(mod)
    f = {}

    def box_f(g):
        b = bounds_u_v(mod, g)
        return {"u": [(b[0] - LAP) / vw, (b[1] - LAP) / vw], "v": [b[2] / vh, b[3] / vh]}

    def pt(slot, var):
        got = fitting_centre(mod, slot, var)
        if not got:
            return None
        c, _ = got
        return {"u": [(c[0] - mod.X0 - LAP) / vw] * 2, "v": [(c[2] - mod.Z0) / vh] * 2}
    if (k, ph) == ("T2", "D3") or (k, ph) == ("T2", "D1"):
        lights = sorted([(g.bounds[1], g) for g in holes.values()], key=lambda t: t[0])
        for i, (_, g) in enumerate(lights, 1):
            b = bounds_u_v(mod, g)
            f["light%d_rows" % i] = {"u": None, "v": [b[2] / vh, b[3] / vh]}
        if ph == "D3":
            first = lights[0][1]
            last_b = bounds_u_v(mod, first)
            # the bead's width on the glass: a section of the first light's bead
            bead = [n for n in mod.M if n.startswith("bead_")]
            nm = [n for n in bead if n.endswith("light1")][0]
            zmid = 0.5 * (first.bounds[1] + first.bounds[3])
            reg = mod.region(nm, 2, zmid, (0, 1))
            polys = [reg] if reg.geom_type == "Polygon" else list(reg.geoms)
            left = max(g.bounds[2] for g in polys if g.centroid.x < first.centroid.x)
            right = min(g.bounds[0] for g in polys if g.centroid.x > first.centroid.x)
            wl, wr = left - mod.X0, right - mod.X0                      # the clear glass between the beads, structural u
            f["white_left"] = {"u": [0.0, (wl - LAP) / vw], "v": None}
            f["white_right"] = {"u": [1.0 - (mod.W - wr - LAP) / vw, 1.0], "v": None}
            f["glass_width"] = {"u": [(wl - LAP) / vw, (wr - LAP) / vw], "v": None}
            res = leaded_numbers(N, mod)
            fs = mod.fs
            lh = fs["glass_opening_z"][1] - fs["glass_opening_z"][0]
            f["fan_foot_strip"] = {"u": None, "v": [0.0, res["foot_came_above_foot"] / lh]}
            f["fan_band"] = {"u": None, "v": [res["foot_came_above_foot"] / lh, (res["foot_came_above_foot"] + res["band_h"]) / lh]}
            f["fan_plain_pane"] = {"u": None, "v": [1.0 - res["plain_pane_h"] / lh, 1.0]}
            f["fan_lozenge_pitch"] = {"u": [0.0, res["lozenge_w"] / vw], "v": None}
    elif (k, ph) == ("T3", "D4"):
        for name, key, inn in (("small_light", "small_light", False), ("upper_outer", "upper_panel", False), ("upper_inner", "upper_panel", True), ("lower_outer", "lower_panel", False), ("lower_inner", "lower_panel", True)):
            g = (inner if inn else holes).get(key)
            if g is not None:
                f[name] = box_f(g)
        p = pt("letter_plate", "LP6")
        h = pt("handle", "HD2c")
        f["plate_v"] = {"u": None, "v": p["v"]} if p else None
        f["lever_v"] = {"u": None, "v": h["v"]} if h else None
    elif (k, ph) == ("F5", "D2"):
        f["slit"] = box_f(holes["slit"])
        f["plate"] = pt("letter_plate", "LP7")
        f["lever"] = pt("handle", "HD2b")
    elif (k, ph) == ("F4", "D2"):
        for i, o in enumerate(sorted(holes.items(), key=lambda t: t[1].bounds[0]), 1):
            b = bounds_u_v(mod, o[1])
            f["light%d_across" % i] = {"u": [(b[0] - LAP) / vw, (b[1] - LAP) / vw], "v": None}
    elif (k, ph) == ("F6", "D5"):
        f["plate"] = pt("letter_plate", "LP4")
        f["lever"] = pt("handle", "HD2a")
        f["lock"] = pt("latch", "LK3")
        g = holes.get("spyhole")
        if g is not None:
            b = bounds_u_v(mod, g)
            f["spyhole"] = {"u": [(0.5 * (b[0] + b[1]) - LAP) / vw] * 2, "v": [0.5 * (b[2] + b[3]) / vh] * 2}
    return f


def row_GA(N, rep, tgt_checks, renders):
    for c in tgt_checks:
        if c.get("type") != "views":
            continue
        k = c["kind"]
        views = N["gate"]["views"][k]
        names = [v["name"] for v in views]
        need = ["front", "street", "close", "low", "front_head", "front_foot", "close_plate"]
        low_plate = any(f["variant"] in ("LP5",) for f in [x for h in N["street"]["houses"] if h["kind"] == k for x in [{"variant": d["variant"]} for d in h["furniture"].values()]])
        ok = len(views) == c["expect"] and all(n in names for n in need) and (("close_foot" in names) == low_plate)
        have = []
        if renders and os.path.isdir(renders):
            for n in ("street", "close"):
                have += [f for f in os.listdir(renders) if f.startswith("%s-%s-v" % (k, n))]
        rep.add(c["id"], ok, {"views": names, "previews_street_close": sorted(have)}, c["expect"], "the gate's cameras for the kind (target.json gate.views, the 3.1 views json lowered to the kind's fittings) and its street and close previews", group="GA", kind=k)


# ------------------------------------------------------------------ C: dimensions, .glb files, coplanar faces
def row_DIM(N, mod, rep):
    k, fs = mod.kind, mod.fs
    lo, hi = mod.leaf_bounds_mm()
    spec = mod.spec["leaf"]
    sz = hi - lo
    rep.within("DIM:%s:leaf_w" % k, sz[0], spec["w"], 1.0, "the leaf's width (the slab, or the boards with their tongues beyond the last joint: none)", group="DIM", kind=k)
    rep.within("DIM:%s:leaf_h" % k, sz[2], spec["h"], 1.0, group="DIM", kind=k)
    if k == "F7":
        lo2, hi2 = mod.bbox(mod.names("leaf_board_", "leaf_ledge_", "leaf_brace_"))
        rep.within("DIM:%s:leaf_t" % k, hi2[1] - lo2[1], spec["t"], 1.0, "boards 22 and ledges 25 behind them, braces under the ledges' backs (47: the target's thickness since the try 1 reviews)", group="DIM", kind=k)
    else:
        rep.within("DIM:%s:leaf_t" % k, sz[1], spec["t"], 1.0, group="DIM", kind=k)
    rep.within("DIM:%s:leaf_x0" % k, lo[0], fs["leaf_x0"], 1.0, group="DIM", kind=k)
    rep.within("DIM:%s:leaf_z0" % k, lo[2], fs["leaf_z0"], 1.0, group="DIM", kind=k)
    jl, jr = mod.bbox("frame_jamb_L"), mod.bbox("frame_jamb_R")
    rep.within("DIM:%s:jamb_left_outer" % k, jl[0][0], fs["jamb_x"]["left"][0], 1.0, group="DIM", kind=k)
    rep.within("DIM:%s:jamb_right_outer" % k, jr[1][0], fs["jamb_x"]["right"][1], 1.0, group="DIM", kind=k)
    rep.within("DIM:%s:stop_left" % k, jl[1][0], fs["stop_edges_x"][0], 1.0, group="DIM", kind=k)
    rep.within("DIM:%s:stop_right" % k, jr[0][0], fs["stop_edges_x"][1], 1.0, group="DIM", kind=k)
    tr = mod.bbox("frame_transom")
    rep.within("DIM:%s:transom_underside" % k, tr[0][2], fs["transom_z"][0], 1.0, group="DIM", kind=k)
    rep.within("DIM:%s:transom_top" % k, tr[1][2], fs["transom_z"][1], 1.0, group="DIM", kind=k)
    hd = mod.bbox("frame_head")
    rep.within("DIM:%s:head_top" % k, hd[1][2], fs["head_top"], 1.0, "the head's crown (T: the cambered soffit)", group="DIM", kind=k)
    gl = mod.bbox("glass_fanlight" if "glass_fanlight" in mod.M else "glass_fanlight_flutes")
    rep.within("DIM:%s:fanlight_opening_h" % k, fs["glass_opening_z"][1] - fs["glass_opening_z"][0], 267.0 if k[0] == "T" else 267.0, 1.0, "the fanlight's opening height (kept as 3.1)", group="DIM", kind=k)
    ov = mod.bbox(list(mod.M))
    rep.add("DIM:%s:overall" % k, True, {"x_mm": [round(float(ov[0][0]), 1), round(float(ov[1][0]), 1)], "z_mm": [round(float(ov[0][2]), 1), round(float(ov[1][2]), 1)], "y_mm": [round(float(ov[0][1]), 1), round(float(ov[1][1]), 1)]},
            "recorded", "the kind's overall box in the target's frame (the glb's own pivot is %s)" % fs["glb_pivot"], group="DIM", kind=k)


def row_GLB(N, mod, rep, path):
    k = mod.kind
    size = os.path.getsize(path)
    meshes, js = cd.read_glb(path)
    rep.add("GLB:%s:size" % k, size < 1_000_000, size, "< 1,000,000 bytes", group="GLB", kind=k)
    no_uv = [n for n, prims in meshes.items() for p in prims if not p["uv"][0]]
    rep.add("GLB:%s:uv" % k, not no_uv, no_uv or "TEXCOORD_0 on every primitive", "every primitive has UVs", group="GLB", kind=k)
    tex = len(js.get("textures", [])) + len(js.get("images", []))
    rep.add("GLB:%s:no_textures" % k, tex == 0, tex, 0, "no image in the file: a height map can never be exported as a normal map (the shop windows' first lesson); the engine's tiling materials are made from the UVs (1 UV unit = 1 m)", group="GLB", kind=k)
    nz = [n for n, prims in meshes.items() for p in prims if len(p["N"]) != len(p["P"])]
    rep.add("GLB:%s:normals" % k, not nz, nz or "a normal on every vertex", group="GLB", kind=k)
    bad = [m.get("name") for m in js.get("materials", []) if not m.get("name") or not any(m.get("name").startswith(a) for a in ALLOWED_MATERIALS)]
    rep.add("GLB:%s:material_names" % k, not bad, bad or [m.get("name") for m in js.get("materials", [])], "named by what they are (paint_<colour>, glass, glass_reeded, lead_came, net_voile, timber_bare, stone_step, timber_threshold ...)", group="GLB", kind=k)
    unit = js["asset"].get("generator", "")
    lo = np.full(3, 1e9)
    hi = np.full(3, -1e9)
    for n, prims in meshes.items():
        for p in prims:
            lo = np.minimum(lo, p["P"].min(0))
            hi = np.maximum(hi, p["P"].max(0))
    # glTF is y up: our z is its y; metres: the base's centre on the ground, the door within 3 m
    rep.add("GLB:%s:metres_pivot" % k, abs(lo[1]) <= 0.4 and hi[1] <= 3.0 and abs(0.5 * (lo[0] + hi[0])) < 0.2, {"lowest_z_m": round(float(lo[1]), 3), "highest_z_m": round(float(hi[1]), 3), "x_centre_m": round(float(0.5 * (lo[0] + hi[0])), 3)},
            "metres, z up (glTF y), the pivot at the base's centre on the ground", group="GLB", kind=k)
    open_parts = [n for n, (V, F) in mod.M.items() if not L_closed(F) and not n.startswith("fit:")]
    rep.add("GLB:%s:closed_parts" % k, not open_parts, open_parts or "every part closed (every edge shared by two faces)", group="GLB", kind=k)


def L_closed(F):
    from collections import Counter
    E = Counter()
    for f in F:
        for i in range(3):
            e = tuple(sorted((int(f[i]), int(f[(i + 1) % 3]))))
            E[e] += 1
    return all(v == 2 for v in E.values())


def row_coplanar(N, mod, rep, label):
    same, opp, ex = cd.coplanar_overlaps({n: v for n, v in mod.M.items()}, tol=0.1, min_area=1.0, limit=40)
    rep.add("GLB:%s:no_shared_face_plane" % label, same == 0, {"same_facing_overlaps": same, "hidden_back_to_back": opp, "examples": ex[:5]},
            "no two parts share a visible face plane (faces of different parts coplanar within 0.1 mm, facing the same way, overlapping by more than 1 mm2)", group="GLB", kind=mod.kind)
    return same


def load_furniture_checks(rep, N, furn_cache):
    for vid, parts in furn_cache.items():
        path = os.path.join(ASSET, "furniture", vid + ".glb")
        size = os.path.getsize(path)
        meshes, js = cd.read_glb(path)
        no_uv = [n for n, prims in meshes.items() for p in prims if not p["uv"][0]]
        tex = len(js.get("textures", [])) + len(js.get("images", []))
        bad = [m.get("name") for m in js.get("materials", []) if not m.get("name") or not any(m.get("name").startswith(a) for a in ALLOWED_MATERIALS)]
        ok = size < 1_000_000 and not no_uv and tex == 0 and not bad
        rep.add("GLB:fitting:%s" % vid, ok, {"bytes": size, "primitives_without_uv": no_uv, "textures": tex, "unnamed_materials": bad, "parts": sorted(parts)}, "under 1 MB, UVs on every primitive, no texture, named materials", group="GLB")
        V = np.vstack([v for v, f in parts.values()]) * 1000.0
        # the fitting stands on its face: nothing behind y = +5 mm (into the leaf) and something proud
        sunk = vid in ("KH1",)                                  # the sunk keyhole sits in a pocket 2.2 deep: everything of it is behind the face (y > 0), none of it proud
        ok2 = V[:, 1].max() <= 5.0 and (V[:, 1].min() < -0.2 or (sunk and V[:, 1].min() >= 0.3))
        rep.add("GLB:fitting:%s:on_the_face" % vid, ok2, {"y_range_mm": [round(float(V[:, 1].min()), 2), round(float(V[:, 1].max()), 2)]},
                "origin on the face: stands proud (y < 0) and goes into the face by at most a few mm (KH1: sunk in its pocket, all of it behind the face, y 0.3 to 5)", group="GLB")
        row_flat_shading(rep, meshes, "fitting:%s" % vid)
        row_near_coplanar(rep, parts, "fitting:%s" % vid)
        names_bad = [n for n in parts if n.startswith("glass") or "label" in n.lower()]
        rep.add("GLB:fitting:%s:own_parts" % vid, True, sorted(parts), "separate part, not merged into a kind", group="GLB", extra=True)


# ------------------------------------------------------------------ new in try 2: the fresh reviews of 13 October (street and close)
def planar_faces_shading(meshes, min_area_mm2=100.0, min_side_mm=8.0, max_deg=5.0):
    """The close review's fault, as a row: a large flat face must be shaded flat. A large flat face is a planar face (connected triangles in one plane, edge-connected through welded
    vertices, seeded by the biggest) of more than `min_area_mm2` whose narrower side is at least `min_side_mm` (a strip a few mm wide is a facet of a moulding's curve, shaded
    smooth on purpose, and is not a flat face). Its shading is off by the area-weighted mean angle between its vertex normals, as the .glb carries them, and its own face normal:
    at most `max_deg`. F7's boards carried the averaged normals of their V-joint chamfers, 17 degrees off at each edge (8.5 on average across the face), and read as rounded staves
    in raking light. (A mean, not the worst vertex, so that a flat strip joining a rounded corner of a sweep is not charged for the two vertices of the join.)
    Returns (faces found, [violations])."""
    big, bad = 0, []
    for name, prims in meshes.items():
        for pi, pr in enumerate(prims):
            P = pr["P"] * 1000.0
            I = pr["I"]
            if len(I) == 0:
                continue
            a, b, c = P[I[:, 0]], P[I[:, 1]], P[I[:, 2]]
            cr = np.cross(b - a, c - a)
            ar = 0.5 * np.linalg.norm(cr, axis=1)
            ok = ar > 1e-9
            fn = np.zeros_like(cr)
            fn[ok] = cr[ok] / (2.0 * ar[ok, None])
            d = (fn * a).sum(1)
            _, wid = np.unique(np.round(P, 3), axis=0, return_inverse=True)
            wid = wid.reshape(-1)
            edges = defaultdict(list)
            for t in range(len(I)):
                if not ok[t]:
                    continue
                w = wid[I[t]]
                for e in ((w[0], w[1]), (w[1], w[2]), (w[2], w[0])):
                    edges[tuple(sorted((int(e[0]), int(e[1]))))].append(t)
            nbr = defaultdict(set)
            for ts in edges.values():
                for x in ts:
                    for y in ts:
                        if x != y:
                            nbr[x].add(y)
            seen = np.zeros(len(I), bool)
            for seed in np.argsort(-ar):
                if seen[seed] or not ok[seed]:
                    continue
                comp, stack = [], [int(seed)]
                seen[seed] = True
                while stack:
                    t = stack.pop()
                    comp.append(t)
                    for u in nbr[t]:
                        if not seen[u] and ok[u] and float(fn[u] @ fn[seed]) > 0.99995 and abs(float(d[u] - d[seed])) < 0.02:
                            seen[u] = True
                            stack.append(u)
                area = float(ar[comp].sum())
                if area < min_area_mm2:
                    continue
                u_, v_ = cd.basis(fn[seed])
                polys = [Polygon([(p @ u_, p @ v_) for p in (a[t], b[t], c[t])]) for t in comp]
                rect = unary_union([q.buffer(0.001) for q in polys if q.area > 0]).minimum_rotated_rectangle
                xy = list(rect.exterior.coords)
                sides = sorted([math.dist(xy[0], xy[1]), math.dist(xy[1], xy[2])])
                if sides[0] < min_side_mm:
                    continue
                big += 1
                vn = pr["N"][I[comp]]                                                   # (m, 3, 3)
                vn = vn / np.maximum(np.linalg.norm(vn, axis=2, keepdims=True), 1e-12)
                ang = np.degrees(np.arccos(np.clip(vn @ fn[seed], -1.0, 1.0)))             # (m, 3)
                mean = float((ang.mean(1) * ar[comp]).sum() / ar[comp].sum())
                if mean > max_deg:
                    bad.append({"part": name, "area_mm2": round(area, 1), "mean_deg": round(mean, 1), "worst_deg": round(float(ang.max()), 1), "normal": [round(float(x), 2) for x in fn[seed]]})
    return big, bad


def row_flat_shading(rep, meshes, label, kind=None):
    big, bad = planar_faces_shading(meshes)
    rep.add("GLB:%s:flat_faces_flat_shaded" % label, not bad, {"large_flat_faces": big, "shaded_off_by_more_than_5_deg_on_average": bad[:6]},
            "every large flat face (a planar face over 100 mm2 and at least 8 mm across) is shaded flat: its vertex normals are on average within 5 degrees of its own face normal (the close review: F7's boards read as rounded staves)", group="GLB", kind=kind)
    return not bad


def near_coplanar_overlaps(M, tol=0.1, max_deg=2.0, min_area=1.0, limit=20):
    """The wider form of 3.1's coplanar test (the close review's narrow point 2): faces of different parts that face the same way within `max_deg` (2 degrees: the review asked for under 1; LP1's flap has facets 1.2 degrees off the liner), overlap by more than `min_area` mm2
    seen along one face's normal, and lie within `tol` mm of each other over that overlap (the distance of the overlap's corners, lifted onto one face, from the other's plane). The first
    test grouped faces by normals rounded to two decimals, so a dished flap whose middle facets tilt 0.3 degrees did not meet the flat liner lying 0.1 mm behind its deepest point."""
    from scipy.spatial import cKDTree
    tris = cd.triangle_planes(M)
    if len(tris) < 2:
        return 0, []
    names = sorted({t[0] for t in tris})
    pid = np.array([names.index(t[0]) for t in tris])
    Nn = np.array([t[1] for t in tris])
    Dd = np.array([t[2] for t in tris])
    Pt = np.array([t[3] for t in tris])
    lo, hi = Pt.min(1) - tol, Pt.max(1) + tol
    pairs = cKDTree(Nn).query_pairs(2.0 * math.sin(math.radians(max_deg) / 2.0), output_type="ndarray")
    if len(pairs) == 0:
        return 0, []
    i, j = pairs[:, 0], pairs[:, 1]
    keep = pid[i] != pid[j]
    i, j = i[keep], j[keep]
    keep = np.all(lo[i] <= hi[j], axis=1) & np.all(lo[j] <= hi[i], axis=1)
    i, j = i[keep], j[keep]
    n, ex = 0, []
    for a, b in zip(i, j):
        u, v = cd.basis(Nn[a])
        A = Polygon([(p @ u, p @ v) for p in Pt[a]])
        B = Polygon([(p @ u, p @ v) for p in Pt[b]])
        if not A.intersects(B):
            continue
        ov = A.intersection(B)
        if ov.area <= min_area:
            continue
        polys = [ov] if ov.geom_type == "Polygon" else [g for g in ov.geoms if g.geom_type == "Polygon"]
        worst = 0.0
        for g in polys:
            for (x, y) in g.exterior.coords:
                q = Dd[a] * Nn[a] + x * u + y * v                      # the overlap's corner lifted onto face a's plane (Nn[a] is a unit normal: its point nearest the origin is Dd[a] * Nn[a])
                worst = max(worst, abs(float(Nn[b] @ q - Dd[b])))
        if worst <= tol:
            n += 1
            if len(ex) < limit:
                ex.append([names[pid[a]], names[pid[b]], round(float(ov.area), 1), round(worst, 3)])
    return n, ex


def row_near_coplanar(rep, M, label, kind=None):
    n, ex = near_coplanar_overlaps(M)
    rep.add("GLB:%s:no_near_coplanar_faces" % label, n == 0, {"overlaps": n, "examples": ex[:5]},
            "no two parts have faces facing the same way within 2 degrees and lying within 0.1 mm of each other's planes, overlapping by more than 1 mm2 (the dished flap of LP1 and LP2 against its liner)",
            group="GLB", kind=kind)
    return n == 0


def glass_rows(rep, kind, path, parts_json, expect_reeded=False, nets=False, mats=None):
    """The glass of the files: every glass material is clear (the 3.1 kit's base colour tinted every pane dark: the close review's point 7); F6's reeded glass is its own rough material
    (street review 6); T2's net cards carry the windows' net material (street review 1)."""
    ms = mats if mats is not None else glb_materials(path)[0]
    glass = {n: m for n, m in ms.items() if n and n.startswith("glass")}
    lin_min = min((min(m["base"][:3]) for m in glass.values()), default=1.0)
    rep.add("GLB:%s:glass_clear" % kind, glass and lin_min >= 0.75, {n: [round(srgb_of_linear(x)) for x in m["base"][:3]] for n, m in glass.items()},
            "every glass material's base colour is clear (each channel at least 0.75 linear, about 225 of 255)", group="GLB", kind=kind)
    if expect_reeded:
        r = glass.get("glass_reeded")
        used = {n: v["material"] for n, v in parts_json.items() if n.startswith("glass_fanlight")}
        ok = r is not None and r["rough"] >= 0.2 and set(used.values()) == {"glass_reeded"} and len(used) == 2
        rep.add("GLB:%s:reeded_glass_own_material" % kind, ok, {"glass_reeded": r, "parts": used},
                "the transom's two glass parts carry their own material glass_reeded, rough in transmission (roughness at least 0.2), no texture", group="GLB", kind=kind)
    if nets:
        used = {n: v["material"] for n, v in parts_json.items() if n.startswith("net_")}
        rep.add("GLB:%s:nets_net_voile" % kind, len(used) == 4 and set(used.values()) == {"net_voile"}, used, "the four net cards carry the windows kit's net material net_voile (a plain card: the PC builds the folded net)",
                group="GLB", kind=kind)


def row_hinge_fixing(N, mod, rep, parts_json=None):
    """T2's small dark two-part fitting on the hinge stile (target kinds.T2.small_fixings, record FU-T2-hinge_fixing): the first build left it out and no row looked for it."""
    for c in N["checks"]:
        if c.get("type") != "kind_fixing" or c["kind"] != mod.kind:
            continue
        ex = c["expect"]
        names = sorted(n for n in mod.M if n.startswith("iron_hinge_fixing_"))
        if len(names) != ex["parts"]:
            rep.add(c["id"], False, {"parts": names}, ex, c["what"], c["tol"], group="FU", kind=mod.kind)
            continue
        lo, hi = mod.bbox(names)
        ctr, size = (lo + hi) / 2.0, hi - lo
        zs = sorted((float(mod.bbox(n)[0][2]), float(mod.bbox(n)[1][2])) for n in names)
        gap = zs[1][0] - zs[0][1]
        mat = {parts_json[n]["material"] for n in names} if parts_json else {"steel_dark"}
        got = {"u": round(float(ctr[0] - mod.X0), 1), "v": round(float(ctr[2] - mod.Z0), 1), "size": [round(float(size[0]), 1), round(float(size[2]), 1)], "proud": round(float(mod.LY0 - lo[1]), 2),
               "gap_mm": round(float(gap), 1), "material": sorted(mat)}
        ok = (abs(got["u"] - ex["u"]) <= c["tol"] and abs(got["v"] - ex["v"]) <= c["tol"] and abs(size[0] - ex["size"][0]) <= 1.0 and abs(size[2] - ex["size"][1]) <= c["tol"]
              and abs(got["proud"] - ex["proud"]) <= 0.5 and abs(gap - 10.0) <= 1.0 and mat == {"steel_dark"})
        rep.add(c["id"], ok, got, ex, c["what"], c["tol"], group="FU", kind=mod.kind)


def row_kh_pocket(N, mod, rep):
    """KH1 is sunk: where the target places KH1 for this kind the leaf has a blind keyhole-shaped pocket, 2.2 deep (at 2.0 below the face the keyhole is open, at 2.4 it is solid), whose
    outline is the keyhole's (IoU at least 0.9). Not through, so nothing can show through."""
    kh = N["furniture"]["keyhole"]["KH1"]
    pl = kh["place"].get(mod.kind)
    if not pl:
        return
    cx, cz = mod.X0 + pl["u"], mod.Z0 + pl["v"]
    want = Polygon(bd.Door.keyhole_outline(cx, cz, kh["head_dia"], kh["slot_w"], kh["size"][1]))
    from shapely.geometry import Point as _P
    got = {}
    ok = True
    for tag, dy in (("front", 1.0), ("floor_minus", 2.0), ("floor_plus", 2.4)):
        hs = [h for h in mod.holes(mod.LY0 + dy) if h.contains(_P(cx, cz))]
        got[tag] = round(float(hs[0].area), 1) if hs else 0.0
        if tag == "front":
            iou = float(hs[0].intersection(want).area / hs[0].union(want).area) if hs else 0.0
            got["iou_with_the_keyhole"] = round(iou, 3)
            ok &= iou >= 0.9
        elif tag == "floor_minus":
            ok &= got[tag] > 0.0
        else:
            ok &= got[tag] == 0.0
    rep.add("FU-%s-keyhole-pocket" % mod.kind, ok, got, "a keyhole-shaped blind pocket 2.2 deep at u %s, v %s: open at 1.0 and 2.0 below the face, solid at 2.4" % (pl["u"], pl["v"]),
            "KH1 is SUNK, as the target says (close review 10): the leaf is cut with a pocket, the fitting sits in it", group="FU", kind=mod.kind)


def notch_measure(void, X0, W, Z0, left):
    """The cavity of a notch from the section of the leaf at 0.3 mm below its face (`void`: the missing material at the hinge-side foot), in leaf millimetres: its width, the greatest
    and the mean height of its top edge, the top edge's wander (peak to peak over s 15 to 90), the height in the last 8 mm. s runs from the leaf's end in."""
    if void is None or void.is_empty:
        return None
    b = void.bounds
    xs = np.arange(b[0] + 0.5, b[2] - 0.4, 1.0)
    tops = []
    for x in xs:
        seg = void.intersection(LineString([(x, Z0 - 5.0), (x, Z0 + 60.0)]))
        tops.append(seg.bounds[3] - Z0 if not seg.is_empty else 0.0)
    tops = np.array(tops)
    s = (xs - X0) if left else (X0 + W - xs)
    order = np.argsort(s)
    s, tops = s[order], tops[order]
    mid = (s >= 15.0) & (s <= 90.0)
    return {"width_mm": round(float(b[2] - b[0]), 1), "max_height_mm": round(float(tops.max()), 1), "mean_height_mid_mm": round(float(tops[mid].mean()), 1),
            "wander_pp_mm": round(float(tops[mid].max() - tops[mid].min()), 1), "height_at_free_end_mm": round(float(tops[-8:].mean()), 1)}


def notch_ok(m):
    """The street review's point 8: an irregular worn edge, not a crisp rectangle: 25 high on average (20 to 30), the top edge wandering by at least 4 mm peak to peak (and under 14),
    the free end tapering to under 6 mm over its last 8 mm, 100 to 135 wide."""
    return (m is not None and 100.0 <= m["width_mm"] <= 135.0 and 18.0 <= m["mean_height_mid_mm"] <= 30.0 and m["max_height_mm"] <= 33.0 and 4.0 <= m["wander_pp_mm"] <= 14.0
            and m["height_at_free_end_mm"] <= 6.0)


def camera_px(view, pts_m, W=1600, H=1200, sensor=36.0):
    """Project points (metres, the kind's glb frame) with a gate view (loc, target, lens mm), as Blender does for a camera that tracks its target (-Z) with Y up, sensor 36 wide."""
    loc, tgt = np.array(view["loc"], float), np.array(view["target"], float)
    f = tgt - loc
    f /= np.linalg.norm(f)
    right = np.cross(f, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right)
    up = np.cross(right, f)
    fpx = view["lens"] / sensor * W
    Q = np.asarray(pts_m, float) - loc
    z = Q @ f
    return np.stack([W / 2.0 + fpx * (Q @ right) / z, H / 2.0 - fpx * (Q @ up) / z], axis=1)


def luma(path):
    im = np.asarray(Image.open(path).convert("RGB"), float)
    return 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2], im.shape[1], im.shape[0]


def row_t3_street_dip(N, rep, picture, label="v2"):
    """PL-T3-street-dip (the street review's fault 1): on the street picture, across each of the 16 outlines of T3's two panels the brightness changes by at least 10 per cent of the leaf
    face's within 4 px of where the outline projects. The picture is the same flat overcast light as D4's, whose outlines dip 14 to 40 per cent."""
    from scipy.ndimage import map_coordinates
    c = [x for x in N["checks"] if x["id"] == "PL-T3-street-dip"][0]
    if not os.path.exists(picture):
        rep.add(c["id"], False, "no picture %s" % picture, c["expect"], c["what"], group="PL", kind="T3")
        return
    Y, W, H = luma(picture)
    fs = N["frame_sets"]["T"]
    px, py, pz = fs["glb_pivot"]
    X0, Z0, LY0 = fs["leaf_x0"], fs["leaf_z0"], fs["leaf_front_y"]
    view = [v for v in N["gate"]["views"]["T3"] if v["name"] == "street"][0]
    ops = {o["id"]: o for o in N["kinds"]["T3"]["leaf"]["openings"]}

    def pt(u, v):
        return np.array([(X0 + u - px) / 1000.0, LY0 / 1000.0, (Z0 + v - pz) / 1000.0])
    lines = []
    for pid in ("upper_panel", "lower_panel"):
        o = ops[pid]
        iv = o["inner"]
        umid, vmid = 0.5 * (o["u0"] + o["u1"]), 0.5 * (o["v0"] + o["v1"])
        for tag, box_ in (("outer", (o["u0"], o["u1"], o["v0"], o["v1"])), ("inner", (iv["u0"], iv["u1"], iv["v0"], iv["v1"]))):
            u0, u1, v0, v1 = box_
            lines.append(("%s_%s_left" % (pid, tag), pt(u0, vmid), pt(u0, vmid + 20.0)))
            lines.append(("%s_%s_right" % (pid, tag), pt(u1, vmid), pt(u1, vmid + 20.0)))
            lines.append(("%s_%s_foot" % (pid, tag), pt(umid, v0), pt(umid + 20.0, v0)))
            top_u = umid
            lines.append(("%s_%s_top" % (pid, tag), pt(top_u, v1), pt(top_u + 20.0, v1)))
    # the leaf face: the left stile, between the leaf's edge and the outer outlines
    gy, gx = np.mgrid[0:6, 0:6]
    face_pts = np.array([pt(35.0 + 70.0 * a / 5.0, 960.0 + 700.0 * b / 5.0) for a in range(6) for b in range(6)])
    fq = camera_px(view, face_pts, W, H)
    face = float(np.median(map_coordinates(Y, [fq[:, 1], fq[:, 0]], order=1)))
    res = {}
    worst = 9.0
    for name, p0, p1 in lines:
        q = camera_px(view, np.array([p0, p1]), W, H)
        t = q[1] - q[0]
        t /= np.linalg.norm(t)
        nrm = np.array([-t[1], t[0]])
        offs = np.arange(-6.0, 6.01, 0.5)
        prof = []
        for o_ in offs:
            ss = np.arange(-8.0, 8.01, 1.0)
            xx = q[0][0] + o_ * nrm[0] + ss * t[0]
            yy = q[0][1] + o_ * nrm[1] + ss * t[1]
            prof.append(float(map_coordinates(Y, [yy, xx], order=1).mean()))
        prof = np.array(prof)
        win = np.abs(offs) <= 4.0
        dip = float((prof[win].max() - prof[win].min()) / face)
        res[name] = round(dip, 3)
        worst = min(worst, dip)
    ok = worst >= c["expect"]["min_dip_fraction"] and len(res) == c["expect"]["outlines"]
    by = {"foot_and_top_outlines_least": min(v for k_, v in res.items() if k_.endswith(("_foot", "_top"))), "right_hand_outlines_least": min(v for k_, v in res.items() if k_.endswith("_right")),
          "left_hand_outlines_least": min(v for k_, v in res.items() if k_.endswith("_left"))}
    fails = sorted(k_ for k_, v in res.items() if v < c["expect"]["min_dip_fraction"])
    rep.add(c["id"], ok, {"face_brightness": round(face, 1), "least_dip": round(worst, 3), "by_orientation": by, "outlines_under_the_limit": fails, "dips": res}, c["expect"], c["what"] + " [measured on %s]" % os.path.basename(picture), group="PL", kind="T3")


def row_t2_nets_lit(N, rep, picture):
    """GA-T2-nets-lit (street review of 14 October, point 2; the first form, 'at least 75 per cent of the jamb's white', let the nets come out brighter than the frame): on the street
    picture the four lights' median brightness (less their bars) is 0.80 to 0.90 of the transom bar's front face (D3's nets read 0.84 to 0.87 of its stile's white)."""
    from scipy.ndimage import map_coordinates
    c = [x for x in N["checks"] if x["id"] == "GA-T2-nets-lit"][0]
    lo_, hi_ = c["expect"]["ratio_of_transom_bar"]
    want = "%.2f to %.2f of the transom bar's face" % (lo_, hi_)
    if not os.path.exists(picture):
        rep.add("GA-T2-nets-lit", False, "no picture %s" % picture, want, group="GA", kind="T2")
        return
    Y, W, H = luma(picture)
    fs = N["frame_sets"]["T"]
    px, py, pz = fs["glb_pivot"]
    X0, Z0, LY0 = fs["leaf_x0"], fs["leaf_z0"], fs["leaf_front_y"]
    view = [v for v in N["gate"]["views"]["T2"] if v["name"] == "street"][0]
    pts = []
    for o in N["kinds"]["T2"]["leaf"]["openings"]:
        for a in range(8):
            for b in range(5):
                u = o["u0"] + 25.0 + (o["u1"] - o["u0"] - 50.0) * a / 7.0
                v = o["v0"] + 25.0 + (o["v1"] - o["v0"] - 50.0) * b / 4.0
                pts.append(((X0 + u - px) / 1000.0, (LY0 + 14.0) / 1000.0, (Z0 + v - pz) / 1000.0))
    q = camera_px(view, np.array(pts), W, H)
    nets = float(np.median(map_coordinates(Y, [q[:, 1], q[:, 0]], order=1)))
    z0, z1 = fs["transom_z"]
    xa, xb = fs["stop_edges_x"]
    tp = np.array([((xa + 60.0 + (xb - xa - 120.0) * a / 11.0 - px) / 1000.0, fs["frame_front_y"] / 1000.0, (z0 + (z1 - z0) * f - pz) / 1000.0) for a in range(12) for f in (0.3, 0.5, 0.7)])
    tq = camera_px(view, tp, W, H)
    bar = float(np.median(map_coordinates(Y, [tq[:, 1], tq[:, 0]], order=1)))
    ratio = nets / bar
    rep.add("GA-T2-nets-lit", lo_ <= ratio <= hi_, {"nets_median": round(nets, 1), "transom_bar_median": round(bar, 1), "ratio": round(ratio, 3)}, want,
            "T2's four lights, on the street picture, read 0.80 to 0.90 of the transom bar's front face: pale like D3's nets, and a little darker than the white frame [measured on %s]" % os.path.basename(picture), group="GA", kind="T2")


# ------------------------------------------------------------------ new in try 3: the second fresh reviews of 14 October (street and close)
def row_try3_FU(N, kind, mod_house, rep):
    """The close review's points 1, 2 and 6 as rows, on the built parts of a house: the grip's clear gap (FU-*-grip_gap), the thumb lever's reach (FU-F7-thumb), the scraper's scrolls (FU-T1-scraper-facets)."""
    LY0 = mod_house.LY0
    for c in N["checks"]:
        if c["group"] != "FU" or c["kind"] != kind or c.get("type") not in ("grip_gap", "thumb_reach", "scraper_facets"):
            continue
        t, rid, ex = c["type"], c["id"], c["expect"]
        M = mod_house.M
        if t in ("grip_gap", "thumb_reach"):
            grip = "fit:handle:iron_pull_bar" if c["variant"] == "HD3" else "fit:handle:iron_latch_bow"
            plate = "fit:handle:iron_latch_plate"
            if grip not in M:
                rep.add(rid, False, "no %s placed" % grip, ex, c["what"], group="FU", kind=kind)
                continue
            G = M[grip][0] * 1000.0
            face = float((M[plate][0] * 1000.0)[:, 1].min()) if c["variant"] == "HD4" else LY0              # the leaf's face (HD3) or the plate's front face (HD4)
            if t == "grip_gap":
                gap = face - float(G[:, 1].max())
                rep.add(rid, gap >= ex["min_gap"] - 1e-6 and abs(gap - ex["gap"]) <= c["tol"], {"gap_mm": round(gap, 2)}, ex, c["what"], group="FU", kind=kind)
            else:
                th = "fit:handle:iron_latch_thumb"
                if th not in M:
                    rep.add(rid, False, "no thumb lever", ex, c["what"], group="FU", kind=kind)
                    continue
                T_ = M[th][0] * 1000.0
                P_ = M[plate][0] * 1000.0
                out_ = face - float(T_[:, 1].min())
                slot_z = 0.5 * (float(P_[:, 2].min()) + float(P_[:, 2].max())) + N["furniture"]["handle"]["HD4"]["slot_z"]
                rise = float(T_[:, 2].max()) - slot_z
                over = T_[(T_[:, 1] >= G[:, 1].min()) & (T_[:, 1] <= G[:, 1].max())]
                clear = float(over[:, 2].min() - G[:, 2].max()) if len(over) else 99.0
                rep.add(rid, out_ >= ex["out_min"] and rise <= ex["rise_max"] and clear >= ex["clear_over_bow_min"],
                        {"out_mm": round(out_, 1), "rise_above_slot_mm": round(rise, 1), "clear_over_bow_mm": round(clear, 1)}, ex, c["what"], group="FU", kind=kind)
        else:
            names = [n for n in M if n.startswith("fit:scraper:iron_scraper_standard_r")]
            if not names:
                rep.add(rid, False, "no standard placed", ex, c["what"], group="FU", kind=kind)
                continue
            V, F = M[names[0]]
            y_mid = float(V[:, 1].min() + V[:, 1].max()) * 500.0
            reg = mod_house.region(names[0].replace("fit:scraper:", "fit:scraper:"), 1, y_mid, (0, 2))
            polys = [reg] if reg.geom_type == "Polygon" else [g for g in reg.geoms if g.geom_type == "Polygon"]
            ring = list(max(polys, key=lambda g: g.area).exterior.coords)[:-1]
            tp_ = N["furniture"]["scraper"]["BS1"]["standard_profile_xz"]

            def runs(pts):
                """The ring's segments with every straight run merged (a mesh splits a long straight side into pieces; a facet of a curve turns by degrees, a straight run by none)."""
                n_ = len(pts)
                keep = []
                for i_ in range(n_):
                    p0, p1, p2 = pts[i_ - 1], pts[i_], pts[(i_ + 1) % n_]
                    a1 = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
                    a2 = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
                    turn = abs((a2 - a1 + math.pi) % (2 * math.pi) - math.pi)
                    if turn > math.radians(0.5):
                        keep.append(p1)
                return [math.hypot(b_[0] - a_[0], b_[1] - a_[1]) for a_, b_ in zip(keep, keep[1:] + keep[:1])]
            segs = runs(ring)
            n_long = sum(1 for d_ in segs if d_ > ex["max_facet_mm"])
            n_target = sum(1 for d_ in runs([tuple(q_) for q_ in tp_]) if d_ > ex["max_facet_mm"])
            rep.add(rid, n_long == n_target, {"segments_over_5mm_built": n_long, "straight_sides_in_the_target": n_target, "longest_mm": round(max(segs), 1)}, ex, c["what"] + " (the long segments are the bar's and the lip's straight sides, as many as the target's own list has)", group="FU", kind=kind)


def depth_along(reg, line_pts, LY0):
    """Depth below the face (mm) of the front surface of a section region (coordinates c, y) at each coordinate c in line_pts: the least y of the region on the vertical line there."""
    out = []
    for c in line_pts:
        seg = reg.intersection(LineString([(c, LY0 - 30.0), (c, LY0 + 80.0)]))
        ys = [p[1] for g in ([seg] if hasattr(seg, "coords") else list(getattr(seg, "geoms", []))) for p in g.coords] if not seg.is_empty else []
        out.append(min(ys) - LY0 if ys else None)
    return out


def row_quirk(N, mod, rep):
    """PL-T3-quirk (street review of 14 Oct, point 1): in six sections the surface just outside each outline is a groove 3 below the surface it cuts, 5 wide, and beyond it the surface is back at its level."""
    c = [x for x in N["checks"] if x["id"] == "PL-T3-quirk"][0]
    q = N["kinds"]["T3"]["mouldings"]["outside"]["quirk"]
    ex = c["expect"]
    ops = {o["id"]: o for o in N["kinds"]["T3"]["leaf"]["openings"]}
    lo, up = ops["lower_panel"], ops["upper_panel"]
    gap, gw, gd = q["gap_to_outline"], ex["width"], ex["depth"]
    LY0 = mod.LY0
    # (label, axis of the section plane, its position, the section axes, the coordinate of the outline across the groove, the direction away from the outline, the surface the groove cuts)
    zl = mod.Z0 + 0.5 * (lo["v0"] + lo["v1"])
    xm = mod.X0 + 0.5 * (lo["u0"] + lo["u1"])
    probes = [("lower_outer_left", 2, zl, (0, 1), mod.X0 + lo["u0"], -1.0, 0.0), ("lower_inner_left", 2, zl, (0, 1), mod.X0 + lo["inner"]["u0"], -1.0, 6.0),
              ("lower_outer_foot", 0, xm, (2, 1), mod.Z0 + lo["v0"], -1.0, 0.0), ("lower_inner_foot", 0, xm, (2, 1), mod.Z0 + lo["inner"]["v0"], -1.0, 6.0),
              ("upper_outer_head", 0, mod.X0 + 0.5 * (up["u0"] + up["u1"]), (2, 1), mod.Z0 + up["v1"], +1.0, 0.0),
              ("upper_inner_crown", 0, mod.X0 + 0.5 * (up["inner"]["u0"] + up["inner"]["u1"]), (2, 1), mod.Z0 + up["inner"]["v1"], +1.0, 6.0)]
    res, ok = {}, True
    for label, axis, pos, axes, edge, sgn, level in probes:
        reg = mod.region("leaf_frame", axis, pos, axes)
        if reg.is_empty:
            res[label] = "no section"
            ok = False
            continue
        xs = [edge + sgn * (gap + 0.025 + k * 0.05) for k in range(int((gw + 8.0) / 0.05))]      # from the groove's inner edge outward (the cove inside the outline also passes through the floor's depth)
        d = depth_along(reg, xs, LY0)
        inside = [x_ for x_, d_ in zip(xs, d) if d_ is not None and abs(d_ - (level + gd)) <= 0.3]
        width = (max(inside) - min(inside) + 0.05) if inside else 0.0
        beyond = depth_along(reg, [edge + sgn * (gap + gw + 3.0)], LY0)[0]
        mid = depth_along(reg, [edge + sgn * (gap + gw / 2.0)], LY0)[0]
        good = mid is not None and abs(mid - (level + gd)) <= c["tol"] and abs(width - gw) <= c["tol"] and beyond is not None and abs(beyond - level) <= 0.3
        res[label] = {"floor_depth": None if mid is None else round(mid, 2), "width": round(width, 2), "surface_beyond": None if beyond is None else round(beyond, 2)}
        ok &= bool(good)
    rep.add("PL-T3-quirk", ok and len(res) == ex["sections"], res, "groove %.1f wide and %.1f deep below the surface it cuts (face 0, margin 6), in %d sections" % (gw, gd, ex["sections"]),
            c["what"], group="PL", kind="T3")


def srgb_of_linear(c):
    return 255.0 * (12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055)


def row_chrome(N, rep, glb_dirs=None, want=None):
    """MAT-chrome_nickel (close review 4): the material chrome_nickel has the target's colour in every furniture file that uses it and in door_F6.glb (the spyhole ring)."""
    c = [x for x in N["checks"] if x["id"] == "MAT-chrome_nickel"][0]
    want = want or c["expect"]["srgb"]
    files = [os.path.join(ASSET, "furniture", "%s.glb" % v) for v in ("LP2", "LP4", "HD2a", "HD2b", "HD2c", "LK1", "LK2")] + [os.path.join(ASSET, "door_F6.glb")]
    got, ok = {}, True
    for f in files:
        _, js = cd.read_glb(f)
        mats = [m for m in js.get("materials", []) if m.get("name", "").startswith("chrome_nickel")]
        if not mats:
            got[os.path.basename(f)] = "no chrome_nickel"
            ok = False
            continue
        bc = mats[0]["pbrMetallicRoughness"]["baseColorFactor"][:3]
        srgb = [round(srgb_of_linear(x), 1) for x in bc]
        got[os.path.basename(f)] = srgb
        ok &= all(abs(a - b) <= c["tol"] for a, b in zip(srgb, want))
    rep.add("MAT-chrome_nickel", ok, got, want, c["what"], group="MAT", kind="all")


def row_makers_frozen(N, rep, texts=None):
    """TG-makers-frozen (street review 3, close review 7): the first-draft makers refuse to run without --first-draft (so cannot put the old numbers back into target.json). With `texts` (a control)
    only their text is read; otherwise make_target.py is also run, and target.json must come out byte for byte as it was."""
    import hashlib
    import subprocess
    c = [x for x in N["checks"] if x["id"] == "TG-makers-frozen"][0]
    files = c["expect"]["files"]
    txt = texts or {f: open(os.path.join(TARGET_DIR, f), encoding="utf-8").read() for f in files}
    guard = all(c["expect"]["guard"] in txt.get(f, "") and "--first-draft" in txt.get(f, "") for f in files)
    got = {"guard_in_text": guard}
    ok = guard
    if texts is None and guard:
        tj = os.path.join(TARGET_DIR, "target.json")
        h0 = hashlib.sha256(open(tj, "rb").read()).hexdigest()
        r = subprocess.run([sys.executable, "-B", os.path.join(TARGET_DIR, "make_target.py")], capture_output=True, text=True, cwd=TARGET_DIR)
        h1 = hashlib.sha256(open(tj, "rb").read()).hexdigest()
        got.update({"exit_code": r.returncode, "says_frozen": "frozen" in r.stderr + r.stdout, "target_json_unchanged": h0 == h1})
        ok = r.returncode != 0 and "frozen" in r.stderr + r.stdout and h0 == h1
    rep.add("TG-makers-frozen", ok, got, c["expect"], c["what"], group="TG", kind="all")


def lab_of_srgb(rgb):
    def f(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = [f(x) for x in rgb]
    X, Y, Z = 0.4124 * r + 0.3576 * g + 0.1805 * b, 0.2126 * r + 0.7152 * g + 0.0722 * b, 0.0193 * r + 0.1192 * g + 0.9505 * b

    def ff(t):
        return t ** (1.0 / 3.0) if t > 0.008856 else 7.787 * t + 16.0 / 116.0
    fx, fy, fz = ff(X / 0.95047), ff(Y), ff(Z / 1.08883)
    return (116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz))


def row_street_extra(N, H, rep, numbers=None):
    """Rows the street review of 13 October added (its points 3, 4 and 7), on the house table and the placeholder numbers:
    AD-neighbours-deltaE: every neighbouring pair's paints differ by a CIELAB colour difference of at least 20 (F3 dark green beside F7 deep teal measured 8.4 on the render, 13.8 on the paints,
    against 25 to 80 for every other pair); AD-same-kind-other-paint: no two houses of one kind share a paint (two F1 doors were maroon twins);
    AD-numbers: the placeholder house numbers are British: odd on the west side, even on the east, rising from the quay, two digits at most, none a number read from a photograph (69, 178)."""
    byid = {h["house"]: h for h in H["houses"]}
    pal = {p["id"]: p["srgb"] for p in N["paints"]}
    bad, mn = [], 1e9
    for side in ("east", "west"):
        order = N["street"]["order"][side]
        for a, b in zip(order[:-1], order[1:]):
            if a in byid and b in byid:
                de = math.dist(lab_of_srgb(pal[byid[a]["paint"]]), lab_of_srgb(pal[byid[b]["paint"]]))
                mn = min(mn, de)
                if de < 20.0:
                    bad.append((a, byid[a]["paint"], b, byid[b]["paint"], round(de, 1)))
    rep.add("AD-neighbours-deltaE", not bad, bad or {"least_deltaE": round(mn, 1)}, ">= 20 between neighbouring doors' paints (CIELAB)", "street review point 7", group="AD")
    twins = []
    for k in sorted({h["kind"] for h in H["houses"]}):
        ps = [h["paint"] for h in H["houses"] if h["kind"] == k]
        if len(ps) != len(set(ps)):
            twins.append((k, ps))
    rep.add("AD-same-kind-other-paint", not twins, twins or "no two houses of a kind share a paint", "no twins", "street review point 7 (two F1 doors were the same maroon)", group="AD")
    digits = numbers if numbers is not None else H.get("numbers", {}).get("digits", {})
    placed = []
    for h in H["houses"]:
        for f in h["furniture"]:
            if f["slot"] == "number":
                key = "%s:%s" % (f["glb"].replace("_stacked", ""), h["kind"])
                placed.append((h["side"], h["x_centre_m"], h["house"], digits.get(key)))
    bad = []
    for side, parity in (("west", 1), ("east", 0)):
        row = sorted([p for p in placed if p[0] == side], key=lambda p: p[1])
        nums = [p[3] for p in row]
        if any(n is None or not n.isdigit() or int(n) % 2 != parity or len(n) > 2 or int(n) in (69, 178) for n in nums):
            bad.append((side, nums, "odd on the west, even on the east, two digits at most, none from a photograph"))
        elif [int(n) for n in nums] != sorted(int(n) for n in nums):
            bad.append((side, nums, "rising from the quay"))
    rep.add("AD-numbers", not bad and len(placed) == 4, bad or {"placed": [(p[2], p[3]) for p in placed]}, "odd on the west side, even on the east, rising from the quay, two digits at most",
            "street review points 3 and 4 (the first build had 34, 21 and 15 on one side and a 246 on a street 48 m long): the digits stay placeholders, the town assigns the real ones", group="AD")


# ------------------------------------------------------------------ the run
def run(args):
    t0 = time.time()
    N = json.load(open(os.path.join(TARGET_DIR, "target.json"), encoding="utf-8"))
    H = json.load(open(os.path.join(ASSET, "houses.json")))
    paint_json = json.load(open(os.path.join(ASSET, "paints.json")))
    cond_json = json.load(open(os.path.join(ASSET, "conditions.json")))
    kinds = args.kinds.split(",") if args.kinds else KINDS
    rep = Report()
    rep.adapt += [
        "Frame sets T and F only (the target's FIXES-APPLIED.md: the planted-stop frame FF6 and its frame_change are gone; F6 stands in frame F, an inward-opening 838 leaf).",
        "A1: the drawing's frame, transom glass and visible leaf are compared as what shows from the street (the nearest part wins), because a pane is let 6 mm into its frame's slot and a leaf laps 20.4 behind its stops; the glazing bead counts as glass (it stands on the pane inside the opening).",
        "A3 mouldings: the 3.1 build's bolection stands 4.8 outside the opening's edge (its lap over the framing) and so reaches 41.2 or 38.2 in from it (T1 46, F1 and F2 43 wide). The target states that lap (kinds.*.mouldings.outside.lap_over_framing_mm 4.8) and, since the try 2 reviews (14 Oct, try 3), target_drawing.py draws the ring with it: the required row compares with the ring grown by it, and the literal extra with the drawing's own ring, and both pass.",
        "T3 (changed 13 Oct, from the try 1 reviews): the target's profile is two steps 6 mm deep over 6 mm across (the margin 6 below the face, the field 12), the second cove at d 62.5 to 68.5, built to it; the first target's coves (3 deep over 14, the second at d 76 to 90) dipped 1 to 3 per cent in the street view against D4's 14 to 40.",
        "PL-T3-members (changed 13 Oct): the target's border is now 62.5, the flat margin between the outer and the inner outline at the sides.",
        "F7 (changed 13 Oct): the target's leaf is now 47 thick (boards 22, ledges 25, braces 25); the first build had thin 16 mm ledges (the leaf 38).",
        "BS1 (changed 13 Oct): the target's point list now has the scroll outside its standard, curling outward (D10); the first build, to the first list, curled it inward over the blade. Overall length 404.",
        "The reeded section the target draws (reeded_section) is a 4.0 base with flutes on top (5.2 in all); the glass table says thickness 4.0: built 2.8 + 1.2 = 4.0, flutes of circular segments pitch 6, depth 1.2.",
    ]
    mods = {k: Model.load(N, k) for k in KINDS if os.path.exists(os.path.join(NPZ, "door_%s.npz" % k))}
    furn_cache = {}
    for fn in sorted(os.listdir(NPZ)):
        if fn.startswith("furniture_") and fn.endswith(".npz"):
            furn_cache[fn[len("furniture_"):-4]] = load_npz(os.path.join(NPZ, fn))
    byhouse = {h["house"]: h for h in H["houses"]}
    first_house = {k: [h for h in H["houses"] if h["kind"] == k][0] for k in KINDS}
    houses_mods = {k: assemble(N, mods[k], first_house[k], furn_cache) for k in KINDS if k in mods}
    for h in H["houses"]:
        assemble(N, mods[h["kind"]], h, furn_cache)
    overlays = args.overlays
    if overlays:
        os.makedirs(overlays, exist_ok=True)
    tgt = defaultdict(list)
    for c in N["checks"]:
        tgt[c["group"]].append(c)
    for k in kinds:
        t1 = time.time()
        mod = mods[k]
        D = check_drawings(N, mod, rep, overlays)
        profile_rows(N, mod, rep)
        holes, inner = interior_holes(mod)
        row_PL(N, mod, rep, holes, inner)
        row_CV(N, mod, rep)
        row_FU(N, k, houses_mods[k], rep)
        row_try3_FU(N, k, houses_mods[k], rep)
        if k == "T3":
            row_quirk(N, mod, rep)
        row_DIM(N, mod, rep)
        row_GLB(N, mod, rep, os.path.join(ASSET, "door_%s.glb" % k))
        meshes_k, _ = cd.read_glb(os.path.join(ASSET, "door_%s.glb" % k))
        row_flat_shading(rep, meshes_k, k, k)
        parts_k = json.load(open(os.path.join(NPZ, "door_%s.parts.json" % k)))
        glass_rows(rep, k, os.path.join(ASSET, "door_%s.glb" % k), parts_k, expect_reeded=(k == "F6"), nets=(k == "T2"))
        row_hinge_fixing(N, mod, rep, parts_k)
        row_kh_pocket(N, mod, rep)
        row_coplanar(N, mod, rep, k)
        row_near_coplanar(rep, mod.M, k, k)
        for h in H["houses"]:
            if h["kind"] == k:
                mh = assemble(N, mod, h, furn_cache)
                row_coplanar(N, mh, rep, "%s@%s" % (k, h["house"]))
                row_near_coplanar(rep, mh.M, "%s@%s" % (k, h["house"]), k)
        for h in H["houses"]:
            if h["kind"] == k and h["furniture"]:
                row_FIT(N, assemble(N, mod, h, furn_cache), rep, h["house"])
        check_fitting_drawings(N, houses_mods[k], rep, D, first_house[k]["house"])
        print("  %s done in %.1f s" % (k, time.time() - t1), flush=True)
    full = len(kinds) == len(KINDS)
    if full:
        row_BP(N, H, mods, furn_cache, rep)
        texts = {}
        for fn in sorted(os.listdir(HERE)):
            if fn.endswith(".py") or fn.startswith("NOTES"):
                texts[fn] = open(os.path.join(HERE, fn), encoding="utf-8").read()
        for fn in ("houses.json", "paints.json", "conditions.json", "manifest.json"):
            texts[fn] = open(os.path.join(ASSET, fn), encoding="utf-8").read()
        glb_paths = {k: os.path.join(ASSET, "door_%s.glb" % k) for k in KINDS}
        row_AD_PN_WR_NM(N, H, rep, [c for g in ("AD", "PN", "WR", "NM") for c in tgt[g]], paint_json, cond_json, glb_paths, texts)
        row_street_extra(N, H, rep)
        row_GL(N, mods, rep, tgt["GL"])
        row_MIX(N, H, rep)
        row_PH(N, mods, houses_mods, H, rep, tgt["PH"])
        row_GA(N, rep, tgt["GA"], args.renders)
        ver, date = args.picture_version, args.date
        row_t3_street_dip(N, rep, os.path.join(args.renders, "T3-street-v%d-%s.jpg" % (ver, date)))
        row_t2_nets_lit(N, rep, os.path.join(args.renders, "T2-street-v%d-%s.jpg" % (ver, date)))
        load_furniture_checks(rep, N, furn_cache)
        row_chrome(N, rep)
        row_makers_frozen(N, rep)
        # the notch of a neglected door, and the kept copies: built to prove the condition parameter
        notch_rows(N, rep)
    out = {"model": "production/assets/cloud-week/front-doors-all/", "target": "production/cloud-week/targets/front-doors-all/target.json", "pass_rule": PASS, "adaptations": rep.adapt, "rows": rep.rows,
           "summary": rep.summary(), "seconds": round(time.time() - t0, 1)}
    return out, rep, N, H, mods, houses_mods, furn_cache


def notch_void(m):
    """The cavity of the notch in a model's leaf: the missing material at 0.3 mm below the face near the hinge-side foot (clear of the V joint of F7's boards: s under 135)."""
    left = m.spec["leaf"]["lock_side"] == "right"
    slab = m.region(m.slab_names(), 1, m.LY0 + 0.3, (0, 2))
    leaf = sbox(m.X0, m.Z0, m.X0 + m.W, m.Z0 + m.H)
    box_ = sbox(m.X0 - 1.0, m.Z0 - 1.0, m.X0 + 135.0, m.Z0 + 45.0) if left else sbox(m.X0 + m.W - 135.0, m.Z0 - 1.0, m.X0 + m.W + 1.0, m.Z0 + 45.0)
    g = leaf.difference(slab).intersection(box_)
    g = g.buffer(-0.8, join_style=2).buffer(0.8, join_style=2)               # the 1.5 mm bevel of the foot is a strip a millimetre high along the whole bottom edge: not the notch
    polys = [g] if g.geom_type == "Polygon" else [h for h in getattr(g, "geoms", []) if h.geom_type == "Polygon"]
    polys = [p for p in polys if p.area > 100.0]
    return unary_union(polys) if polys else None


def notch_depths(m):
    """The depth of the notch along its length: the section of the leaf at 2.0 below the face still has the void in the middle; at 0.7 it reaches nearer the free end (0.5 deep there)."""
    left = m.spec["leaf"]["lock_side"] == "right"
    out = {}
    for tag, dy in (("at_0.7", 0.7), ("at_2.0", 2.0), ("at_3.4", 3.4)):
        slab = m.region(m.slab_names(), 1, m.LY0 + dy, (0, 2))
        leaf = sbox(m.X0, m.Z0, m.X0 + m.W, m.Z0 + m.H)
        box_ = sbox(m.X0 - 1.0, m.Z0 - 1.0, m.X0 + 135.0, m.Z0 + 45.0) if left else sbox(m.X0 + m.W - 135.0, m.Z0 - 1.0, m.X0 + m.W + 1.0, m.Z0 + 45.0)
        g = leaf.difference(slab).intersection(box_).buffer(-0.8, join_style=2).buffer(0.8, join_style=2)
        out[tag] = float(g.area)
    return out


def notch_rows(N, rep, neglected_npz=None, void_override=None):
    """The neglected doors of the street carry the notch; a kept door does not: read from the built parts (F4 and F7 are neglected, F4 also exists kept). The notch is an irregular worn edge
    (the street review's point 8; the first build's was a crisp 130 x 25 x 3 rectangle that read as a fitted strip): the cavity's top edge wanders, its free end tapers, it is 3 deep along
    its length and 0.5 at the free end."""
    for k in ("F4", "F7"):
        m = Model.load(N, k, neglected_npz if (neglected_npz and k == "F4") else None)
        has = "leaf_notch_bare" in m.M
        if has:
            lo, hi = m.bbox("leaf_notch_bare")
            left = m.spec["leaf"]["lock_side"] == "right"
            hinge_ok = (lo[0] - m.X0 < 5.0) if left else (m.X0 + m.W - hi[0] < 5.0)
            meas = notch_measure(void_override(m) if void_override else notch_void(m), m.X0, m.W, m.Z0, left)
            dep = notch_depths(m)
            depth_ok = dep["at_0.7"] - dep["at_2.0"] >= 50.0 and dep["at_3.4"] < 1.0                # shallower toward the free end, nothing at 3.4
            depth_max = float(hi[1] - m.LY0) - 0.3
            ok = hinge_ok and notch_ok(meas) and depth_ok and 2.5 <= depth_max <= 3.5
            rep.add("WR:%s:notch" % k, ok, {**(meas or {}), "depth_mm": round(depth_max, 2), "void_area_at_depth_mm2": {a: round(b_, 0) for a, b_ in dep.items()}, "at_hinge_side": hinge_ok},
                    "an irregular worn edge: 100 to 135 wide, 25 high on average (18 to 30, at most 33), the top edge wandering 4 to 14 mm, the free end tapering under 6 mm, 3 deep along its length and less toward the free end",
                    "the neglected door's eroded notch, read from the built leaf (a section 0.3 below its face) and its bare-wood part", group="WR", kind=k)
        else:
            rep.add("WR:%s:notch" % k, False, "no leaf_notch_bare", "a notch in a neglected door", group="WR", kind=k)
    kp = os.path.join(NPZ, "door_F4_kept.npz")
    if os.path.exists(kp):
        m = Model.load(N, "F4", kp)
        rep.add("WR:F4:kept_has_no_notch", "leaf_notch_bare" not in m.M, "a kept copy of F4 has no notch part" if "leaf_notch_bare" not in m.M else "notch present", "no notch on a kept door", group="WR", kind="F4")
    else:
        rep.add("WR:F4:kept_has_no_notch", False, "door_F4_kept.npz not built", "a kept copy", group="WR", kind="F4")


def load_for_controls():
    N = json.load(open(os.path.join(TARGET_DIR, "target.json"), encoding="utf-8"))
    H = json.load(open(os.path.join(ASSET, "houses.json")))
    mods = {k: Model.load(N, k) for k in KINDS}
    furn_cache = {}
    for fn in sorted(os.listdir(NPZ)):
        if fn.startswith("furniture_") and fn.endswith(".npz"):
            furn_cache[fn[len("furniture_"):-4]] = load_npz(os.path.join(NPZ, fn))
    first = {k: [h for h in H["houses"] if h["kind"] == k][0] for k in KINDS}
    houses_mods = {k: assemble(N, mods[k], first[k], furn_cache) for k in KINDS}
    return N, H, mods, houses_mods, furn_cache


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--controls-only", action="store_true")
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--kinds")
    ap.add_argument("--overlays")
    ap.add_argument("--renders", default=os.path.join(REPO, "production", "previews", "cloud-week", "front-doors-all"))
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--picture-version", type=int, default=2, help="the pictures the rows that measure pixels read: <kind>-street-v<N>-<date>.jpg")
    ap.add_argument("--date", default="2026-10-13")
    a = ap.parse_args()
    if a.controls_only:
        import check_controls
        N, H, mods, houses_mods, furn_cache = load_for_controls()
        res = check_controls.run_controls(N, H, mods, houses_mods, furn_cache, sys.modules[__name__])
        print("controls: %d of %d caught" % (res["caught"], res["run"]))
        for r in res["rows"]:
            print(("ok   " if r["caught"] else "MISS "), r["name"], "->", r["row"], r.get("crash", ""), "" if r["caught"] else r.get("failed_rows"))
        json.dump(res, open(os.path.join(HERE, "checks", "controls_only.json"), "w"), indent=1)
        return
    out, rep, N, H, mods, houses_mods, furn_cache = run(a)
    if a.controls:
        import check_controls
        out["controls"] = check_controls.run_controls(N, H, mods, houses_mods, furn_cache, sys.modules[__name__])
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    path = os.path.join(HERE, "checks", "check_doors_v%d.json" % a.version)
    json.dump(out, open(path, "w"), indent=1, default=str)
    s = out["summary"]
    print("%d of %d rows pass" % (s["required_passed"], s["required_run"]))
    print("failed:", s["required_failed"])
    print("extras: %d of %d pass; failed: %s" % (s["extras_passed"], s["extras_run"], s["extras_failed"]))
    if "controls" in out:
        c = out["controls"]
        print("controls: %d of %d caught" % (c["caught"], c["run"]), [r["name"] for r in c["rows"] if not r["caught"]])
    print("wrote", path)


if __name__ == "__main__":
    main()
