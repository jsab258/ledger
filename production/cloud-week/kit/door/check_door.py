"""The automatic check for the front door (cloud week 42, piece 3.1).

    /home/user/.bpyenv/bin/python check_door.py [--variant T1|F1|both] [--version 1] [--npz-dir DIR] [--glb-dir DIR] [--overlays DIR]

For each variant it cuts the built model (kit/door/build/door_<V>.npz, the named parts build_door.py writes) where
target_drawing.py draws it and compares, then runs every check in target.json `checks` that can be run on the model:

  A1  the front view, layer by layer (frame, glass, leaf, panel, moulding) inside the opening: IoU >= 0.97, outline p95 <= 2 mm, worst <= 6 mm
      (ironmongery and stone, which the target also draws, are compared the same way and reported as extras)
  A2  every horizontal section the drawing gives; A3 every vertical section (all joinery layers together)
  A4  the profiles (bolection, band, weatherboard, transom front, glazing bead, threshold, step tread, knob; plinth on the context):
      outline p95 <= 1.5 mm, worst <= 3 mm
  B-I the target's own dimensional, edge, transom, band, weatherboard, ironmongery, step, head, setting and surface checks, each
      measured on the mesh (or, for the glb's normals, materials and UV set, on the .glb as written)

The brick context (arch, quoins, plinth: checks G7-G12, Q1-Q3, L1-L5) is not in the door's .glb; those checks are run on
the review's context wall (door_context.py), cut and compared the same way against the drawing. The pass rule is the brief's
and the target's: IoU >= 0.97, p95 <= 2 mm, worst <= 6 mm, every dimension within the check's own tolerance (1 mm unless the
target gives another). Where the target's drawings or checks contradict each other, the check says which it followed
(`adaptations`) and NOTES.md lists each one.

Writes checks/check_v<N>.json (and overlay pictures into --overlays, outside git).
"""
import argparse
import importlib.util
import json
import math
import os
import sys
from collections import defaultdict

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from shapely.geometry import LineString, Polygon, box as sbox
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import outline  # noqa: E402
from outline import Frame, compare, load_npz, overlay, section, silhouette  # noqa: E402

import build_door as bd  # noqa: E402
import door_context as dc  # noqa: E402

TD_PATH = os.path.join(bd.REPO, "production", "cloud-week", "targets", "front-door", "target_drawing.py")
spec = importlib.util.spec_from_file_location("target_drawing", TD_PATH)
td = importlib.util.module_from_spec(spec)
spec.loader.exec_module(td)

PASS = {"iou": 0.97, "p95_mm": 2.0, "max_mm": 6.0, "profile_p95_mm": 1.5, "profile_max_mm": 3.0}
JOINERY = ("frame", "glass", "leaf", "panel", "moulding")
MMPX = 0.5
VAR_KEY = {"T1": None, "F1": "flat_door_over_shop"}


# ------------------------------------------------------------------ small tools
def frame_for(points_mm, margin=20.0, mmpx=MMPX):
    P = np.vstack([np.asarray(p, float) for p in points_mm])
    lo, hi = P.min(0) - margin, P.max(0) + margin
    return Frame(u0=lo[0] / 1000, v0=lo[1] / 1000, width=(hi[0] - lo[0]) / 1000, height=(hi[1] - lo[1]) / 1000, mm_per_px=mmpx)


def raster_polys(polys, fr):
    """Filled polygons (dicts with pts and optional holes, mm) into one mask."""
    out = np.zeros(fr.shape, bool)
    for p in polys:
        m = _fill(p["pts"], fr)
        for h in p.get("holes", []):
            m &= ~_fill(h, fr)
        out |= m
    return out


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


def biggest(g):
    """The exterior points (open ring) of the largest polygon in a shapely result (which may be a collection with stray lines)."""
    geoms = [g] if g.geom_type == "Polygon" else [h for h in getattr(g, "geoms", []) if h.geom_type == "Polygon"]
    p = max(geoms, key=lambda h: h.area)
    return [list(t) for t in p.exterior.coords][:-1]


def fill_pinholes(mask, max_px=40):
    """Fill holes of a few pixels (where two abutting parts' rasters leave a pin-hole at their corner); real holes are far larger."""
    holes, n = ndimage.label(~mask)
    if n == 0:
        return mask
    sizes = ndimage.sum(np.ones_like(holes), holes, index=np.arange(1, n + 1))
    small = np.isin(holes, np.nonzero(sizes <= max_px)[0] + 1)
    return mask | small


def verdict(c, rule=PASS, kind="drawing"):
    if kind == "profile":
        ok = c["iou"] > 0 and c["p95_mm"] is not None and c["p95_mm"] <= rule["profile_p95_mm"] and c["max_mm"] <= rule["profile_max_mm"]
    else:
        ok = c["iou"] >= rule["iou"] and c["p95_mm"] is not None and c["p95_mm"] <= rule["p95_mm"] and c["max_mm"] <= rule["max_mm"]
    c["ok"] = bool(ok)
    return c


class Model:
    """One variant's built parts in the target's frame (metres), the target's drawings, and measuring tools."""

    def __init__(self, T, variant, npz):
        self.T, self.variant = T, variant
        self.P = bd.variant_parts(T, variant)
        self.pivot = np.array(T["glb_pivot"]["terrace_four_panel" if variant == "T1" else "flat_door_over_shop"], float)
        raw = load_npz(npz)
        self.M = {n: (V + self.pivot / 1000.0, F) for n, (V, F) in raw.items()}
        self.doc = td.all_drawings(T, VAR_KEY[variant])
        self.c = td.consts(self.P)

    def names(self, *prefixes):
        return [n for n in self.M if n.startswith(prefixes)]

    def sub(self, *prefixes):
        return {n: self.M[n] for n in self.names(*prefixes)}

    def bbox_of(self, name):
        V = self.M[name][0] * 1000.0
        return V.min(0), V.max(0)

    def bbox(self, *prefixes):
        """mm bounding box (lo, hi) of the parts whose name starts with a prefix."""
        Vs = [self.M[n][0] for n in self.names(*prefixes)]
        if not Vs:
            raise KeyError(prefixes)
        V = np.vstack(Vs) * 1000.0
        return V.min(0), V.max(0)

    def region(self, prefixes, axis, value_mm, axes):
        """The cut of the named parts by the plane axis = value (mm): a shapely region in (axes) mm, each part even-odd."""
        geoms = []
        for n in self.names(*prefixes):
            V, F = self.M[n]
            g = None
            for L in outline._loops(V, F, axis, value_mm / 1000.0):
                pts = L[:, list(axes)] * 1000.0
                if len(pts) < 3:
                    continue
                p = Polygon(pts).buffer(0)
                g = p if g is None else g.symmetric_difference(p)
            if g is not None and not g.is_empty:
                geoms.append(g)
        return unary_union(geoms) if geoms else Polygon()

    @staticmethod
    def runs(g, axis, fixed, lo=-1e5, hi=1e5):
        """Intervals of region g along u (axis 0) at v = fixed, or along v (axis 1) at u = fixed."""
        if g.is_empty:
            return []
        L = LineString([(lo, fixed), (hi, fixed)]) if axis == 0 else LineString([(fixed, lo), (fixed, hi)])
        x = g.intersection(L)
        segs = [x] if x.geom_type == "LineString" else [s for s in getattr(x, "geoms", []) if s.geom_type == "LineString"]
        out = []
        for s in segs:
            c = np.array(s.coords)
            a = c[:, axis]
            out.append((float(a.min()), float(a.max())))
        out.sort()
        merged = []
        for a, b in out:
            if merged and a <= merged[-1][1] + 1e-6:
                merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
            else:
                merged.append((a, b))
        return merged


class Report:
    def __init__(self):
        self.rows = []
        self.adapt = []

    def add(self, id_, ok, measured, expected, note="", tol=None, extra=False):
        row = {"id": id_, "ok": bool(ok) if ok is not None else None, "measured": measured, "expected": expected}
        if tol is not None:
            row["tol"] = tol
        if note:
            row["note"] = note
        if extra:
            row["extra"] = True
        self.rows.append(row)
        return ok

    def within(self, id_, measured, expected, tol, note="", extra=False):
        m = float(measured)
        ok = abs(m - expected) <= tol
        return self.add(id_, ok, round(m, 2), expected, note, tol, extra)


# ------------------------------------------------------------------ A1: the front view, layer by layer
def depth_layers(m, layers, fr):
    """Label image of what shows from the street at each pixel: the part nearest the street (its lowest y) wins."""
    lab = np.zeros(fr.shape, np.int8)
    depth = np.full(fr.shape, np.inf)
    for name, (V, F) in m.M.items():
        layer = name.split("_")[0]
        if layer not in layers:
            continue
        sil = silhouette({name: (V, F)}, (0, 2), fr)
        y = V[:, 1].min()
        sel = sil & (y < depth)
        lab[sel] = layers.index(layer) + 1
        depth[sel] = y
    return lab


def target_layers(polys, layers, fr):
    lab = np.zeros(fr.shape, np.int8)
    for p in polys:
        if p["layer"] not in layers:
            continue
        mk = raster_polys([p], fr)
        lab[mk] = layers.index(p["layer"]) + 1
    return lab


def check_A1(m, rep, overlays):
    c = m.c
    E = [p for p in m.doc["elevation"]["polygons"] if not p.get("optional")]      # the house numerals are optional (the town's), not built
    layers = JOINERY + ("iron", "stone")
    ground = c.ground if m.variant == "T1" else m.P["step"]["ground_z_mm"]
    pts = [p["pts"] for p in E if p["layer"] in layers]
    fr = frame_for(pts, 20.0)
    tl, ml = target_layers(E, layers, fr), depth_layers(m, layers, fr)
    hh, ww = fr.shape
    u = (fr.u0 + (np.arange(ww) + 0.5) * fr.mm_per_px / 1000) * 1000
    v = (fr.v0 + fr.height - (np.arange(hh) + 0.5) * fr.mm_per_px / 1000) * 1000
    top = c.CROWN
    window = (u[None, :] >= 0) & (u[None, :] <= c.OW) & (v[:, None] >= ground) & (v[:, None] <= top)
    res = {}
    # the tread's fall: the drawing leaves a 6.6 mm strip between the tread's front top and the riser's foot; seen square-on the
    # sloping top covers it (the model's tread top runs from the riser's foot down to the front), so the strip is filled in the drawing
    fill = np.zeros(fr.shape, bool)
    if m.variant == "T1":
        td_ = m.P["step"]["tread"]
        z_hi, z_lo = td_["top_z_mm"], td_["top_z_mm"] - td_["fall_to_front_mm"]
        fill = (u[None, :] >= 0) & (u[None, :] <= c.OW) & (v[:, None] <= z_hi) & (v[:, None] >= z_lo)
    # the drawing paints the letter plate's aperture and the plugged keyhole as iron rectangles (with a ring of leaf colour round the
    # flap); in the model they are a slot through the leaf and a recess in it, so the leaf is not compared inside those rectangles
    rep.adapt.append("A1/A2/A3: the optional house numerals are drawn by target_drawing.py (present = 'optional') but not built (F9: absent unless the town gives a number), so their polygons are left out of every comparison.")
    rep.adapt.append("A1 leaf and iron: the drawing paints the letter plate's aperture and the plugged keyhole as iron rectangles (with a 1-2 mm ring of leaf colour round the flap); the model has a slot through the leaf and a recess in it, so those rectangles are masked out of the leaf comparison, the keyhole out of the iron one, and the iron masks are closed by 1.5 mm (the flap's 1 mm gap closes in a silhouette raster).")
    skip = np.zeros(fr.shape, bool)
    ir = m.P["ironmongery"]
    lp = ir["letter_plate"]
    if lp.get("present"):
        xc, zc = c.X0 + lp["centre_u_mm"], c.Z0 + lp["centre_above_leaf_bottom_mm"]
        skip |= (abs(u[None, :] - xc) <= lp["aperture_w_mm"] / 2 + 2) & (abs(v[:, None] - (zc + lp["outer_h_mm"] / 2 - lp["aperture_top_margin_mm"] - lp["aperture_h_mm"] / 2)) <= lp["aperture_h_mm"] / 2 + 2)
    kh = ir.get("old_keyhole", {})
    if kh.get("present"):
        skip |= (abs(u[None, :] - (c.X0 + kh["centre_u_mm"])) <= kh["w_mm"] / 2 + 2) & (abs(v[:, None] - (c.Z0 + kh["centre_above_leaf_bottom_mm"])) <= kh["h_mm"] / 2 + 2)
    for i, layer in enumerate(layers, 1):
        a, b = fill_pinholes((ml == i) & window), fill_pinholes((tl == i) & window)
        if layer in ("leaf",):
            a, b = a & ~skip, b & ~skip
        if layer == "iron":
            # the 1 mm gap round the letter-plate flap closes in a silhouette raster (its outline fattens each edge), the drawing keeps it
            st = np.ones((3, 3), bool)
            a, b = ndimage.binary_closing(a, st), ndimage.binary_closing(b, st)
            kk = np.zeros(fr.shape, bool)
            if kh.get("present"):
                kk = (abs(u[None, :] - (c.X0 + kh["centre_u_mm"])) <= kh["w_mm"] / 2 + 2) & (abs(v[:, None] - (c.Z0 + kh["centre_above_leaf_bottom_mm"])) <= kh["h_mm"] / 2 + 2)
            a, b = a & ~kk, b & ~kk
        if layer == "stone":
            b = b | (fill & window)
        if not b.any():
            continue
        r = verdict(compare(a, b, MMPX))
        required = layer in JOINERY
        res[layer] = r
        rep.add("A1:" + layer, r["ok"], {k: r[k] for k in ("iou", "p95_mm", "max_mm")}, "IoU >= 0.97, p95 <= 2, worst <= 6",
                "front view, inside the opening" + ("" if required else " (extra: the target draws it, A1 does not name it)"), extra=not required)
        if overlays:
            overlay(a, b, os.path.join(overlays, "A1_%s_%s.png" % (m.variant, layer)))
    if m.variant == "T1":
        rep.adapt.append("A1 stone: the drawing's tread top is 6.6 mm lower at its front than at the riser (fall_to_front_mm) and leaves that strip empty; the model's top runs from the riser's foot to the front, so square-on it covers the strip. The strip is filled in the drawing for the stone comparison.")
    return res


# ------------------------------------------------------------------ A2 / A3: the sections
def clip_head(polys, c, variant, x_cut):
    """The target draws the frame head 101.6 tall in its vertical sections (top z 2371.2, or 2441.2 for F1), and cuts it to the soffit
    in its elevation, B16, B17, G8 and frame.head_section_mm. The build follows the cut (the brick in front hides the rest);
    the section comparison clips the drawn head at the soffit."""
    out = []
    sz = td.soffit_z(c, x_cut) if c.R else c.CROWN
    for p in polys:
        if p["name"] == "head":
            g = Polygon(p["pts"]).buffer(0).intersection(sbox(-1e5, -1e5, 1e5, sz))
            q = dict(p)
            q["pts"] = biggest(g)
            out.append(q)
        else:
            out.append(p)
    return out


def check_sections(m, rep, overlays):
    c = m.c
    keys = [k for k in m.doc if k.startswith("section_h") or k.startswith("section_v") and k != "section_v_plinth"]
    for key in keys:
        d = m.doc[key]
        horiz = key.startswith("section_h")
        axis = 2 if horiz else 0
        axes = (0, 1) if horiz else (1, 2)
        at = d["cut_z_mm"] if horiz else d["cut_x_mm"]
        for kind, layers in (("joinery", JOINERY), ("iron", ("iron",)), ("stone", ("stone",))):
            polys = [p for p in d["polygons"] if p["layer"] in layers and not p.get("optional")]
            if not polys:
                continue
            layers = tuple(l for l in layers if any(p["layer"] == l for p in polys))      # compare only the layers the drawing draws at this cut
            adapted = False
            if not horiz:
                polys = clip_head(polys, c, m.variant, at)
                if any(p["name"] == "head" for p in polys):
                    rep.adapt.append("A3 vertical sections: the drawing's head is 101.6 tall (top z %.1f) while its elevation, frame.head_section_mm, B16, B17 and G8 cut the head to the soffit (T1 2340 / 2322, F1 2400); the build follows the cut, so the drawn head is clipped at the soffit's height at the cut before comparing." % (m.P["frame"]["head_section_mm"]["z0"] + m.P["frame"]["head_section_mm"]["height"]))
            if key == "section_h_transom" and m.variant == "T1":
                # at z 1955.6 the drawing's transom runs back to y 241.3, but its own vertical profile has nothing behind y 188.3 below
                # z 1959.6 (the leaf's head sits in that rebate): the build follows the vertical profile
                adapted = True
                new = []
                for p in polys:
                    if p["name"] == "transom":
                        g = Polygon(p["pts"]).buffer(0).intersection(sbox(-1e5, -1e5, 1e5, c.STOP_Y))
                        q = dict(p)
                        q["pts"] = biggest(g)
                        new.append(q)
                    else:
                        new.append(p)
                polys = new
                rep.adapt.append("A2 section_h_transom (T1): the drawn transom runs to y 241.3 at z 1955.6, below its own rebate underside (z 1959.6); the drawing is clipped at y 188.3, where the vertical profile has material.")
            fr = frame_for([p["pts"] for p in polys], 20.0)
            b = raster_polys(polys, fr)
            prefixes = tuple(layers)
            a = fill_pinholes(section(m.sub(*prefixes), axis, at / 1000.0, axes, fr))
            r = verdict(compare(a, fill_pinholes(b), MMPX))
            required = kind == "joinery"
            rep.add(("A2:" if horiz else "A3:") + key + ("" if required else ":" + kind), r["ok"], {k: r[k] for k in ("iou", "p95_mm", "max_mm")},
                    "IoU >= 0.97, p95 <= 2, worst <= 6", "cut at %s = %.1f mm%s%s" % ("z" if horiz else "x", at, "" if required else " (extra)", " (drawing adapted)" if adapted else ""),
                    extra=not required)
            if overlays:
                overlay(a, b, os.path.join(overlays, "%s_%s_%s.png" % (key, kind, m.variant)))


# ------------------------------------------------------------------ A4: profiles
def profile_compare(model_pts_by_loops, target_pts, mmpx=0.1):
    """Compare a cut outline with a profile polygon, both in the profile's own frame (mm)."""
    allp = [target_pts] + list(model_pts_by_loops)
    fr = frame_for(allp, 4.0, mmpx)
    tmask = _fill(target_pts, fr)
    mmask = np.zeros(fr.shape, bool)
    for L in model_pts_by_loops:
        mmask ^= _fill(L, fr)
    return compare(mmask, tmask, mmpx)


def loops_of(M, name, axis, value_mm, axes):
    V, F = M[name]
    out = []
    for L in outline._loops(V, F, axis, value_mm / 1000.0):
        if len(L) >= 3:
            out.append(L[:, list(axes)] * 1000.0)
    return out


def check_A4(m, rep, ctx=None):
    c, P = m.c, m.P
    prof = m.doc["profiles"]
    X0, Z0, LY0 = c.X0, c.Z0, c.LY0

    def put(label, r):
        verdict(r, kind="profile")
        rep.add("A4:" + label, r["ok"], {k: r[k] for k in ("iou", "p95_mm", "max_mm")}, "p95 <= 1.5, worst <= 3")
    # the bolection: cut the lower-left panel's left leg at its mid height; (d from the outer edge, h proud of the framing)
    key = [k for k in prof if k.startswith("bolection")][0]
    o = P["panels"]["openings_leaf_uv_mm"]["bottom_left"]
    zmid = Z0 + (o["v0"] + o["v1"]) / 2
    loops = loops_of(m.M, "moulding_bolection_bottom_left", 2, zmid, (0, 1))
    xo = X0 + o["u0"] - c.LAP
    left = [np.array([[x - xo, LY0 - y] for x, y in L]) for L in loops if L[:, 0].mean() < X0 + (o["u0"] + o["u1"]) / 2]
    put("bolection", profile_compare(left, prof[key]))
    # the band and the weatherboard: cut at x 441 (p proud of the leaf, z up from the underside)
    for pk, nm, blk in (("lock-rail band", "moulding_band", c.band), ("weatherboard", "moulding_weatherboard", c.weather)):
        if not blk.get("present"):
            continue
        key = [k for k in prof if k.startswith(pk)][0]
        za = blk["z_above_leaf_bottom_mm"][0]
        loops = loops_of(m.M, nm, 0, c.OW / 2, (1, 2))
        mod = [np.array([[LY0 - y, z - (Z0 + za)] for y, z in L]) for L in loops]
        put(pk, profile_compare(mod, prof[key]))
    # the transom's front: y out from the jamb face (negative outward), z up from the stop underside; only the moulded front
    # (y < 19) is compared: the target's polygon closes the rest as a plain block, the build has the glass slot and the rebate
    key = [k for k in prof if k.startswith("transom front")][0]
    loops = loops_of(m.M, "frame_transom", 0, c.OW / 2, (1, 2))
    mod = [np.array([[y - c.FY0, z - c.Z_STOP] for y, z in L]) for L in loops]
    win = Polygon([(-60, -10), (19.0, -10), (19.0, 200), (-60, 200)])
    tgt = Polygon(prof[key]).buffer(0).intersection(win)
    modg = unary_union([Polygon(L).buffer(0) for L in mod]).intersection(win)
    tpts = list(tgt.exterior.coords)[:-1]
    mpts = [list(g.exterior.coords)[:-1] for g in ([modg] if modg.geom_type == "Polygon" else list(modg.geoms))]
    put("transom front", profile_compare(mpts, tpts))
    rep.adapt.append("A4 transom front: compared for y < 19 mm from the jamb face (the moulded front); the target's polygon closes the back as a plain 127 x face-height block.")
    # the glazing bead: a along the face from the opening's edge inward, p proud of the glass
    key = [k for k in prof if k.startswith("glazing bead")][0]
    gf = c.GLASS_Y - c.GLASS_T / 2
    loops = loops_of(m.M, "frame_glazing_bead", 0, c.OW / 2 + 17.0, (1, 2))
    mod = [np.array([[z - c.GZ0, gf - y] for y, z in L]) for L in loops if L[:, 1].mean() < c.GZ0 + 60]
    put("glazing bead", profile_compare(mod, prof[key]))
    # the threshold: y into the wall, z
    key = [k for k in prof if k.startswith("threshold")][0]
    loops = loops_of(m.M, "stone_threshold", 0, c.OW / 2, (1, 2))
    put("threshold", profile_compare(loops, prof[key]))
    if m.variant == "T1":
        key = [k for k in prof if k.startswith("step tread")][0]
        loops = loops_of(m.M, "stone_tread", 0, c.OW / 2, (1, 2))
        tg = unary_union([Polygon(L).buffer(0) for L in loops]).intersection(sbox(-1e5, -1e5, P["step"]["riser"]["face_y_mm"], 1e5))
        mp = [list(g.exterior.coords)[:-1] for g in ([tg] if tg.geom_type == "Polygon" else list(tg.geoms))]
        put("step tread", profile_compare(mp, prof[key]))
        rep.adapt.append("A4 step tread: compared in front of the riser (y < 18); the target's profile stops at the riser's face, the stone runs on behind it.")
    if P["ironmongery"].get("knob", {}).get("present"):
        key = [k for k in prof if k.startswith("turned centre knob")][0]
        kz = Z0 + P["ironmongery"]["knob"]["centre_above_leaf_bottom_mm"]
        kx = X0 + P["ironmongery"]["knob"]["centre_u_mm"]
        g = unary_union([Polygon(L).buffer(0) for nm in ("iron_knob", "iron_knob_cap") for L in loops_of(m.M, nm, 0, kx, (1, 2))])
        g = g.intersection(sbox(-1e5, -1e5, LY0, 1e5))          # from the face outward: the foot sunk in the rail is not the profile
        mod = [np.array([[z - kz, LY0 - y] for y, z in L]) for L in [np.array(list(h.exterior.coords)[:-1]) for h in ([g] if g.geom_type == "Polygon" else list(g.geoms))]]
        put("knob", profile_compare(mod, prof[key]))
    if ctx is not None and "plinth splay (y, z)" in prof:
        loops = loops_of(ctx, "ctx_plinth_L", 0, -60.0, (1, 2))
        pol = Polygon(prof["plinth splay (y, z)"]).buffer(0).intersection(sbox(-1e5, -1e5, 0.0, 1e5))      # the plinth stands in front of the wall face (y < 0)
        mg = unary_union([Polygon(L).buffer(0) for L in loops]).intersection(sbox(-1e5, -1e5, 0.0, 1e5))
        put("plinth splay (context)", profile_compare([list(mg.exterior.coords)[:-1]], list(pol.exterior.coords)[:-1]))


# ------------------------------------------------------------------ B: dimensions
def check_B(m, rep):
    c, P = m.c, m.P
    L = P["leaf"]
    X0, Z0, LY0, PY0 = c.X0, c.Z0, c.LY0, c.PY0
    lo, hi = m.bbox("leaf_frame")
    rep.within("B1", hi[0] - lo[0], L["width_mm"], 1.0, "x extent of the leaf's framing")
    rep.within("B2", hi[2] - lo[2], L["height_mm"], 1.0, "z extent of the leaf")
    rep.within("B3", hi[1] - lo[1], L["thickness_mm"], 0.5, "y extent of the leaf")
    o = P["panels"]["openings_leaf_uv_mm"]
    zl = Z0 + (o["bottom_left"]["v0"] + o["bottom_left"]["v1"]) / 2
    sec_h = m.region(("leaf_frame",), 2, zl, (0, 1))
    runs = m.runs(sec_h, 0, LY0 + 8.0)                                # the framing between the face and the groove's front wall
    ok = len(runs) == 3
    st_l, mun, st_r = (runs[0][1] - runs[0][0], runs[1][1] - runs[1][0], runs[2][1] - runs[2][0]) if ok else (0, 0, 0)
    rep.within("B4", st_l, L["stile_mm"], 1.0, "left stile; right stile %.2f" % st_r)
    rep.within("B4:right", st_r, L["stile_mm"], 1.0, "right stile")
    rep.within("B5", mun, L["muntin_mm"], 1.5, "muntin; %.1f%% of the leaf's width (target 14.8%%)" % (100 * mun / L["width_mm"]))
    bl, br = o["bottom_left"], o["bottom_right"]
    gap = (br["u0"] - bl["u1"]) - 2 * c.LAP
    a = m.bbox("moulding_bolection_bottom_left")[1][0]
    b = m.bbox("moulding_bolection_bottom_right")[0][0]
    rep.within("B6", b - a, gap, 2.5, "x gap between the outer edges of a pair of panel mouldings")
    # rails: z intervals of the framing in a vertical cut up the left-hand panels
    xm = X0 + (bl["u0"] + bl["u1"]) / 2
    sec_v = m.region(("leaf_frame",), 0, xm, (1, 2))
    zr = m.runs(sec_v, 1, LY0 + 8.0)
    if len(zr) == 3:
        rep.within("B7:bottom_rail", zr[0][1] - zr[0][0], L["bottom_rail_mm"], 1.0)
        rep.within("B7:lock_rail", zr[1][1] - zr[1][0], L["lock_rail_mm"], 1.0)
        rep.within("B7:top_rail", zr[2][1] - zr[2][0], L["top_rail_mm"], 1.0)
        tl = o["top_left"]
        rep.within("B8:lower_height", zr[1][0] - zr[0][1], bl["v1"] - bl["v0"], 1.0, "lower panel opening, z")
        rep.within("B8:upper_height", zr[2][0] - zr[1][1], tl["v1"] - tl["v0"], 1.0, "upper panel opening, z")
    else:
        rep.add("B7", False, "%d rail runs" % len(zr), 3)
    rep.within("B8:width", runs[1][0] - runs[0][1] if ok else 0, bl["u1"] - bl["u0"], 1.0, "panel opening, x")
    plo, phi = m.bbox("panel_bottom_left")
    rep.within("B9:panel_thickness", phi[1] - plo[1], P["panels"]["thickness_mm"], 0.5)
    runs_g = m.runs(sec_h, 0, PY0 + 8.0)                              # inside the groove's thickness: the stile is shorter by the groove's depth
    rep.within("B9:groove_depth", (runs[0][1] - runs[0][0]) - (runs_g[0][1] - runs_g[0][0]) if runs_g else 0, P["panels"]["groove_depth_mm"], 0.5, "stile width less its width at the groove")
    leg = m.region(("moulding_bolection_bottom_left",), 2, zl, (0, 1))
    legs = [g for g in ([leg] if leg.geom_type == "Polygon" else list(leg.geoms))]
    left_leg = min(legs, key=lambda g: g.centroid.x)
    rep.within("B10", left_leg.bounds[2] - left_leg.bounds[0], P["mouldings"]["outside_bolection"]["width_on_face_mm"], 3.0, "bolection, outer edge to the panel field")
    lo, hi = m.bbox("frame_jamb_L")
    rep.within("B11:across", hi[0] - lo[0], c.JF, 1.0, "jamb face")
    rep.within("B11:deep", hi[1] - lo[1], c.JD, 1.0, "jamb depth")
    jr = m.region(("frame_jamb_L",), 2, 1000.0, (0, 1))
    w_front = m.runs(jr, 0, c.FY0 + 10.0)[0]
    w_reb = m.runs(jr, 0, c.STOP_Y + 10.0)[0]
    rep.within("B12:width", w_front[1] - w_reb[1], c.REB_W, 1.0, "rebate width")
    y_runs = m.runs(jr, 1, 0.5 * (w_front[1] + w_reb[1]))
    rep.within("B12:depth", (c.FY1 - y_runs[0][1]) if y_runs else 0, P["frame"]["rebate_depth_mm"], 1.0, "rebate depth")
    rep.within("B13", w_front[1] - max(w_front[0], 0.0), c.SHOW, 2.0, "jamb showing past the brick / in the doorway")
    lo, hi = m.bbox("frame_transom")
    rep.within("B14", hi[2] - lo[2], P["frame"]["transom"]["face_height_mm"], 3.0, "transom face height")
    gl = P["frame"]["glazing"]
    gx0, gx1 = gl["opening_x_mm"]
    gz0, gz1 = gl["opening_z_mm"]
    bead_h = m.region(("frame_glazing_bead",), 2, 0.5 * (gz0 + gz1), (0, 1))
    legs = [g for g in ([bead_h] if bead_h.geom_type == "Polygon" else list(bead_h.geoms))]
    legs.sort(key=lambda g: g.centroid.x)
    open_w = legs[-1].bounds[2] - legs[0].bounds[0] - 0.8
    clear_w = legs[-1].bounds[0] - legs[0].bounds[2]
    bead_v = m.region(("frame_glazing_bead",), 0, 0.5 * (gx0 + gx1), (1, 2))
    vl = [g for g in ([bead_v] if bead_v.geom_type == "Polygon" else list(bead_v.geoms))]
    vl.sort(key=lambda g: g.centroid.y)
    open_h = vl[-1].bounds[3] - vl[0].bounds[1] - 0.8
    clear_h = vl[-1].bounds[1] - vl[0].bounds[3]
    rep.within("B15:opening_w", open_w, gx1 - gx0, 2.0, "bead to bead, the bead's embedded 0.4 mm taken off each side")
    rep.within("B15:opening_h", open_h, gz1 - gz0, 2.0)
    rep.within("B15:clear_w", clear_w, gl["clear_glass_x_mm"][1] - gl["clear_glass_x_mm"][0], 2.0)
    rep.within("B15:clear_h", clear_h, gl["clear_glass_z_mm"][1] - gl["clear_glass_z_mm"][0], 2.0)
    head_x = lambda x: m.region(("frame_head",), 0, x, (1, 2)).bounds[3]
    O = P["opening"]
    rep.within("B16:crown", head_x(c.OW / 2), O["crown_height_mm"], 4.0, "head's top at the crown")
    rep.within("B16:end_left", head_x(0.0), O["springing_height_mm"], 4.0)
    rep.within("B16:end_right", head_x(c.OW), O["springing_height_mm"], 4.0)
    lj, rj = m.bbox("frame_jamb_L"), m.bbox("frame_jamb_R")
    fw = rj[1][0] - lj[0][0]
    expected_w = c.JR[1] - c.JL[0]
    rep.within("B17:frame_width", fw, expected_w, 3.0, "T1 975.2 / F1 1000.4")
    rep.within("B17:foot", lj[0][2], 0.0, 1.0, "the feet stand at z 0 (bedded 0.5)")


# ------------------------------------------------------------------ C: frame edges (mesh and glb normals)
def turn_angles(P):
    n = len(P)
    out = []
    for i in range(n):
        a, b = P[i] - P[i - 1], P[(i + 1) % n] - P[i]
        out.append(math.degrees(math.atan2(a[0] * b[1] - a[1] * b[0], a @ b)))
    return out


def check_C(m, rep, glb):
    c = m.c
    for side in ("L", "R"):
        g = m.region(("frame_jamb_" + side,), 2, 1000.0, (0, 1))
        pts = np.array(g.exterior.coords)[:-1]
        if side == "L":
            xb, xs, xr = c.JL[0], c.JL[1], c.JL[1] - c.REB_W
        else:
            xb, xs, xr = c.JR[1], c.JR[0], c.JR[0] + c.REB_W
        corners = [(xb, c.FY0), (xs, c.FY0), (xr, c.FY1), (xb, c.FY1)]
        dev = max(min(np.hypot(pts[:, 0] - cx, pts[:, 1] - cy)) for cx, cy in corners)
        t = turn_angles(pts)
        seg = np.hypot(*(np.roll(pts, -1, axis=0) - pts).T)
        arc_run = 0
        best = 0
        for i in range(len(t)):
            if 5.0 < abs(t[i]) < 60.0 and seg[i] < 3.0 and seg[i - 1] < 3.0:
                arc_run += 1
                best = max(best, arc_run)
            else:
                arc_run = 0
        rep.add("C1:" + side, dev <= 1.5 and best < 3, {"corner_deviation_mm": round(float(dev), 2), "longest_arc_run": best}, "corner deviation <= 1.5, no arc", "the jamb's four outer corners; the 1 mm ease is one 45 degree chamfer", 1.5)
    # C2: the jamb's front face is flat (shading normals from the .glb)
    frac = glb.get("jamb_face_flat_fraction")
    rep.add("C2", frac is not None and frac >= 0.98, round(frac, 4) if frac is not None else None, ">= 0.98 within 3 degrees",
            "area of the jamb's front-facing flat triangles whose shading normals are within 3 degrees of the face's: the 1 mm eases are %.1f%% of the visible width and are their own faces" % (100 * 2 * 1.414 / (c.JF)))
    # C3: feet
    lj = m.bbox("frame_jamb_L")
    a = m.region(("frame_jamb_L",), 2, 10.0, (0, 1))
    b = m.region(("frame_jamb_L",), 2, 1000.0, (0, 1))
    rep.add("C3", abs(lj[0][2]) <= 1.0 and a.symmetric_difference(b).area < 1.0, {"foot_z": round(float(lj[0][2]), 2), "section_difference_mm2": round(a.symmetric_difference(b).area, 3)}, "foot at z 0 +-1, same section as the middle", tol=1.0)
    # C4: mirror equal
    ra = m.region(("frame_jamb_R",), 2, 10.0, (0, 1))
    cx = 0.5 * (c.JL[0] + c.JR[1])
    from shapely.affinity import scale as shp_scale
    mirror = shp_scale(a, xfact=-1.0, yfact=1.0, origin=(cx, 0))
    rep.add("C4", mirror.symmetric_difference(ra).area < 1.0, round(mirror.symmetric_difference(ra).area, 3), "mirror difference < 1 mm2", "left and right feet", 1.0)
    if m.variant == "F1":
        for side in ("L", "R"):
            lo, hi = m.bbox("frame_stop_bead_" + side)
            rep.add("C5:" + side, abs((hi[0] - lo[0]) - 5.0) <= 1.0 and abs((c.FY0 - lo[1]) - 2.5) <= 1.0, {"across": round(float(hi[0] - lo[0]), 2), "proud": round(float(c.FY0 - lo[1]), 2)}, "5 x 2.5", tol=1.0)
    else:
        rep.add("C5", None, "n/a", "F1 only")


# ------------------------------------------------------------------ D: the transom
def check_D(m, rep):
    c, P, tr = m.c, m.P, m.P["frame"]["transom"]
    T1 = m.variant == "T1"
    R = m.region(("frame_transom",), 0, c.OW / 2, (1, 2))                    # (y, z) at the middle
    zs = np.arange(0.2, tr["face_height_mm"] - 0.2, 0.25)

    def fy(zrel):
        r = m.runs(R, 0, c.Z_STOP + zrel)
        return (r[0][0] - c.FY0) if r else None
    ys = np.array([fy(z) for z in zs], float)
    z_face = np.mean(tr["zones_z_mm"]["face"])
    face_y = -fy(z_face)
    nose_y = -np.nanmin(ys)
    exp_face, exp_nose = (8.0, 14.0) if T1 else (10.0, 22.0)
    rep.within("D1:face", face_y, exp_face, 3.0, "face proud of the jamb faces")
    rep.within("D1:nose", nose_y, exp_nose, 3.0, "nose proud of the jamb faces")
    sl = tr["zones_z_mm"]["slope"]
    z1, z2 = sl[0] + 0.25 * (sl[1] - sl[0]), sl[0] + 0.75 * (sl[1] - sl[0])
    ang = math.degrees(math.atan2(z2 - z1, fy(z2) - fy(z1)))
    rep.within("D2", ang, 55.0 if T1 else 58.6, 8.0, "weathered slope, degrees from the horizontal")
    z_nose = zs[int(np.nanargmin(ys))]
    if T1:
        rep.add("D4", z_nose <= 6.0, round(float(z_nose), 2), "frontmost point in the lowest 6 mm (a lip bead)", tol=3.0)
    else:
        rep.within("D4:round_z", zs[int(np.nanargmin(ys))], 14.0, 3.0, "fullest point of the round")
        rep.within("D4:quirk_proud", -fy(34.5), 7.0, 3.0, "the quirk returns to about 7 proud")
    zf = tr["zones_z_mm"]["face"]
    face_run = [fy(z) for z in np.arange(zf[0] + 1, zf[1] - 1, 1.0)]
    rep.add("D3:face_vertical", max(face_run) - min(face_run) < 1.5, round(max(face_run) - min(face_run), 2), "< 1.5 mm of y over the face zone", tol=1.5)
    slope_y = [fy(z) for z in np.arange(sl[0] + 1, sl[1] - 1, 1.0)]
    rep.add("D3:slope_rising", all(b > a for a, b in zip(slope_y, slope_y[1:])), "monotone", "y rises through the slope zone")
    levels = sorted({round(float(y)) for y in ys if y is not None and not np.isnan(y)})
    # D7: distinct plateaus (runs of at least 3 mm of height within 0.4 mm of y)
    plateaus, i = 0, 0
    while i < len(ys):
        j = i
        while j + 1 < len(ys) and abs(ys[j + 1] - ys[i]) < 0.4:
            j += 1
        if (j - i) * 0.25 >= 3.0:
            plateaus += 1
        i = j + 1
    rep.add("D7", plateaus >= 3 or len(levels) >= 3, {"plateaus": plateaus, "distinct_y_levels_1mm": len(levels)}, ">= 3")
    # D5 and D8 from the cut at y = jamb face - 3 (inside the nose and face), in (x, z)
    xl_stop, xr_stop = c.JL[1], c.JR[0]
    cut = m.region(("frame_transom",), 1, c.FY0 - 3.0, (0, 2))
    ov = tr["overlap_on_jamb_faces_mm"]
    z_mid_face = c.Z_STOP + z_face
    r = m.runs(cut, 0, z_mid_face)
    rep.within("D5:face_overrun_left", xl_stop - r[0][0], ov, 5.0 if not T1 else 4.0, "face past the stop edge")
    rep.within("D5:face_overrun_right", r[-1][1] - xr_stop, ov, 5.0 if not T1 else 4.0)
    r0 = m.runs(cut, 0, c.Z_STOP + 0.5)
    rep.within("D5:nose_underside_left", r0[0][0] - xl_stop, 0.0, 3.0, "nose underside ends at the stop edge")
    rep.within("D5:nose_underside_right", xr_stop - r0[-1][1], 0.0, 3.0)
    sp = tr["end_splay"]
    za, zb = c.Z_STOP + sp["from_stop_edge_z_mm"] + 0.25 * (sp["to_z_mm"] - sp["from_stop_edge_z_mm"]), c.Z_STOP + sp["from_stop_edge_z_mm"] + 0.75 * (sp["to_z_mm"] - sp["from_stop_edge_z_mm"])
    xa, xb = m.runs(cut, 0, za)[0][0], m.runs(cut, 0, zb)[0][0]
    ang8 = math.degrees(math.atan2(zb - za, xa - xb))
    rep.within("D8", ang8, 45.0, 8.0, "the nose's end, in elevation, degrees from the horizontal")
    # D6: the bead
    gl = P["frame"]["glazing"]
    gz0 = gl["opening_z_mm"][0]
    bead = m.region(("frame_glazing_bead",), 0, c.OW / 2, (1, 2))
    gf = c.GLASS_Y - c.GLASS_T / 2
    vl = [g for g in ([bead] if bead.geom_type == "Polygon" else list(bead.geoms))]
    bot = min(vl, key=lambda g: g.centroid.y)
    rep.within("D6:face", bot.bounds[3] - gz0, gl["bead_face_mm"], 1.5, "bead across the face (a), the foot 10 mm inside the opening edge")
    rep.within("D6:proud", gf - bot.bounds[0], gl["bead_proud_mm"], 1.5, "bead proud of the glass")


# ------------------------------------------------------------------ E and W: band and weatherboard (T1)
def profile_p(m, name, x_cut, LY0):
    R = m.region((name,), 0, x_cut, (1, 2))
    return R, (lambda z: (LY0 - m.runs(R, 0, z)[0][0]) if m.runs(R, 0, z) else None)


def local_extrema(zs, ps, prom):
    peaks, vals = [], []
    n = len(ps)
    for i in range(1, n - 1):
        if ps[i] >= ps[i - 1] and ps[i] > ps[i + 1]:
            peaks.append(i)
        if ps[i] <= ps[i - 1] and ps[i] < ps[i + 1]:
            vals.append(i)
    return peaks, vals


def check_EW(m, rep):
    c, P = m.c, m.P
    if not c.band.get("present"):
        for k in ("E1", "E2", "E3", "E4", "E5", "W1", "W2", "W3", "W4"):
            rep.add(k, None, "n/a", "T1 only")
        return
    xl_stop, xr_stop = c.JL[1], c.JR[0]
    for tag, key, nm in (("E", "lock_rail_band", "moulding_band"), ("W", "weatherboard", "moulding_weatherboard")):
        blk = P["mouldings"][key]
        za, zb = blk["z_above_leaf_bottom_mm"]
        lo, hi = m.bbox(nm)
        rep.within(tag + "1:bottom", lo[2] - c.Z0, za, 4.0, "z above the leaf's bottom (top %.1f)" % (hi[2] - c.Z0))
        rep.within(tag + "1:top", hi[2] - c.Z0, zb, 4.0)
        rep.within(tag + "2", c.LY0 - lo[1], blk["max_projection_mm"], 4.0, "max proud of the leaf face")
        rep.within(tag + ("5" if tag == "E" else "4") + ":left", lo[0] - xl_stop, 2.0, 1.5, "gap to the left stop face")
        rep.within(tag + ("5" if tag == "E" else "4") + ":right", xr_stop - hi[0], 2.0, 1.5, "gap to the right stop face")
        R, pz = profile_p(m, nm, c.OW / 2, c.LY0)
        zz = np.arange(za + 0.25, zb - 0.25, 0.25)
        pp = np.array([pz(c.Z0 + z) for z in zz], float)
        pks, vls = local_extrema(zz - za, pp, 0.5)
        if tag == "E":
            crests = [(zz[i] - za, pp[i]) for i in pks if pp[i] > 12]
            coves = [(zz[i] - za, pp[i]) for i in vls if 10 < pp[i] < 22]
            # departure D6: broad lit rolls, crests at z 12, 36 and 62, with two SHALLOW creases (at z 26 and 52, each 1 to 4 mm below the lower of the
            # crests beside it); the target's coves were 7 mm deep
            cr = [z for z, _ in crests]
            cv = [(z, p) for z, p in coves]
            depths = []
            for z, p in cv:
                left = [q for zq, q in crests if zq < z]
                right = [q for zq, q in crests if zq > z]
                if left and right:
                    depths.append((z, min(left[-1], right[0]) - p))
            shallow = [(z, d) for z, d in depths if any(abs(z - t) < 5 for t in (26, 52)) and 1.0 <= d <= 4.0]
            rep.add("E3", len(crests) >= 3 and len(shallow) >= 2 and not any(d > 4.0 for _, d in depths), {"crests_z": [round(float(z), 1) for z in cr], "creases_z_depth_mm": [(round(float(z), 1), round(float(d), 2)) for z, d in depths]},
                    "3 crests (z 12, 36, 62), 2 shallow creases (z 26, 52; 1-4 mm deep)  [departure D6; the target: coves at z 25 and 49, 7 mm deep]")
            below = zz[(pp is not None)]
            under = R.bounds[1]
            lowest = [pt for pt in np.array(R.exterior.coords) if abs(pt[1] - R.bounds[1]) < 0.05]
            flat_depth = c.LY0 - min(p[0] for p in lowest)
            rep.add("E4", abs(flat_depth - 17.0) <= 2.0, round(float(flat_depth), 2), "flat underside 14 to 17 deep", tol=2.0)
        else:
            zr = zz - za
            lower = np.nanmax(pp[zr < 14])
            sel = (zr > 12) & (zr < 42)
            fit = np.polyfit(zr[sel], pp[sel], 1)
            face_ang = math.degrees(math.atan(-fit[0]))                    # the face's angle from the vertical (it slopes up and back)
            resid = float(np.nanmax(np.abs(pp[sel] - np.polyval(fit, zr[sel]))))
            hollow = np.nanmin(pp[(zr > 46) & (zr < 56)])
            roll = np.nanmax(pp[(zr > 58) & (zr < 78)])
            # the top nose: a circle through three points of the rolled-back top
            pts3 = [(zz[np.argmin(abs(zz - za - t))], pp[np.argmin(abs(zz - za - t))]) for t in (70.0, 75.0, 79.0)]
            (x1, y1), (x2, y2), (x3, y3) = pts3
            d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            rad = None
            if abs(d) > 1e-9:
                ux = ((x1 ** 2 + y1 ** 2) * (y2 - y3) + (x2 ** 2 + y2 ** 2) * (y3 - y1) + (x3 ** 2 + y3 ** 2) * (y1 - y2)) / d
                uy = ((x1 ** 2 + y1 ** 2) * (x3 - x2) + (x2 ** 2 + y2 ** 2) * (x1 - x3) + (x3 ** 2 + y3 ** 2) * (x2 - x1)) / d
                rad = math.hypot(x1 - ux, y1 - uy)
            rep.add("W3", bool(lower >= 24.0 and 24.0 <= face_ang <= 36.0 and resid < 1.0 and hollow <= roll - 6.0 and rad is not None and rad >= 8.0),
                    {"lower_arris_p": round(float(lower), 1), "face_angle_from_vertical_deg": round(float(face_ang), 1), "face_straightness_mm": round(resid, 2), "hollow_p": round(float(hollow), 1), "top_roll_p": round(float(roll), 1),
                     "top_nose_radius_mm": None if rad is None else round(float(rad), 1)},
                    "departure D4: the lower arris >= 24 proud, a plain face sloping up and back at 30 +-6 degrees from the vertical (z 12-42, straight within 1 mm), a hollow >= 6 behind the top roll, the roll's radius >= 8 "
                    "[the target: a near-vertical belly >= 24 at z 26-40, a hollow >= 5 behind the crests either side at z 57]")
    return


# ------------------------------------------------------------------ F: ironmongery
def check_F(m, rep):
    c, P = m.c, m.P
    ir = P["ironmongery"]
    lp = ir["letter_plate"]
    lo, hi = m.bbox("iron_letter_plate")
    names = m.names("iron_letter")
    rep.add("F1", all(n in m.M for n in ("iron_letter_plate", "iron_letter_flap")) and len(names) >= 2, names, "backplate with a raised rim and an aperture, and a hinged flap",
            "the plate's loft has a back, a chamfered edge, a sloped rim and an aperture; the flap is its own part (with a lifting lip)")
    rep.within("F2:w", hi[0] - lo[0], lp["outer_w_mm"], 3.0)
    rep.within("F2:h", hi[2] - lo[2], lp["outer_h_mm"], 3.0)
    rep.within("F3:height", 0.5 * (lo[2] + hi[2]) - c.Z0, lp["centre_above_leaf_bottom_mm"], 10.0, "centre above the leaf's bottom")
    rep.within("F3:x_offset", 0.5 * (lo[0] + hi[0]) - (c.X0 + c.W / 2), 0.0, 10.0, "x offset from the leaf's centre")
    rep.within("F4:rim_proud", c.LY0 - lo[1], lp["rim_proud_mm"], 1.5)
    V = m.M["iron_letter_plate"][0] * 1000
    edge = V[np.abs(V[:, 0] - lo[0]) < 0.01]
    rep.within("F4:backplate", c.LY0 - edge[:, 1].min(), lp["backplate_thickness_mm"], 1.5, "the plate's outer edge stands 3 proud")
    cl = ir["cylinder_lock"]
    parts = m.names("iron_lock")
    llo, lhi = m.bbox(*parts)
    cx = 0.5 * (llo[0] + lhi[0])
    cz = 0.5 * (llo[2] + lhi[2])
    rep.within("F5:collar", lhi[0] - llo[0], cl["outer_diameter_mm"], 4.0, "collar diameter")
    rep.within("F5:height", cz - c.Z0, cl["centre_above_leaf_bottom_mm"], 4.0, "centre above the leaf's bottom")
    rep.within("F5:from_stop_face", c.JR[0] - cx, cl["distance_from_stop_face_mm"], 4.0, "centre to the stop face")
    plug = "iron_lock_plug" if "iron_lock_plug" in m.M else "iron_lock"
    pr = m.region((plug,), 2, cz, (0, 1)).bounds
    # the plug: its face's width (the narrowest long stretch of the section)
    pw = (m.runs(m.region((plug,), 2, cz, (0, 1)), 0, c.LY0 + 12.0) or [(0, 0)])[0]
    rep.within("F5:plug", pw[1] - pw[0], cl["plug_diameter_mm"], 4.0, "plug diameter, 12 mm in from the face")
    rep.add("F6", (c.JR[0] - (lhi[0])) >= 24.0, round(float(c.JR[0] - lhi[0]), 2), ">= 24", "collar's nearest edge to the stop face")
    # the collar stands proud (D1): its front, measured on the mesh; the keyway is a vertical slot 3 x 9 in the plug's face (D2)
    ytop = min(m.bbox_of(n)[0][1] for n in m.names("iron_lock"))
    rep.within("F5:collar_proud", c.LY0 - ytop, cl["collar_proud_mm"], 0.5, "the collar's front stands this far proud of the leaf's face (departure D1: 5.0 from the photographs, target.json 1.5 / 2.0)")
    kw_t, kh_t = cl.get("keyway_w_mm", 3.0), cl.get("keyway_h_mm", 9.0)
    face = [n for n in m.names("iron_lock") if n in ("iron_lock", "iron_lock_plug")][0]
    Vp = m.M[face][0] * 1000.0
    plug_face_y = c.LY0 - (cl["collar_proud_mm"] - (0.6 if m.variant == "T1" else 1.0))
    cutk = m.region((face,), 1, plug_face_y + 1.5, (0, 2))              # 1.5 mm behind the plug's face: the plug's disc with the keyway cut out of it
    ring_k = Polygon([(cx - 14, cz - 14), (cx + 14, cz - 14), (cx + 14, cz + 14), (cx - 14, cz + 14)]).difference(cutk).intersection(Polygon([(cx - 6, cz - 6), (cx + 6, cz - 6), (cx + 6, cz + 6), (cx - 6, cz + 6)]))
    kb = ring_k.bounds if not ring_k.is_empty else (0, 0, 0, 0)
    rep.add("F5:keyway", (not ring_k.is_empty) and abs((kb[2] - kb[0]) - kw_t) <= 1.0 and abs((kb[3] - kb[1]) - kh_t) <= 1.5, {"w_mm": round(kb[2] - kb[0], 2), "h_mm": round(kb[3] - kb[1], 2)},
            "a vertical slot %g x %g in the plug (departure D2 for F1; T1 as the target)" % (kw_t, kh_t), tol=1.0)
    if m.variant == "T1":
        kp = ir["keep"]
        klo, khi = m.bbox("iron_bellpush")
        rep.within("F7:w", khi[0] - klo[0], kp["w_mm"], 5.0, "the bell push's oblong back (D13: P1's dark oblong 22 x 72.6; the target called it a keep)")
        rep.within("F7:h", khi[2] - klo[2] - 0.0, kp["h_mm"], 5.0)
        rep.within("F7:centre_x", 0.5 * (klo[0] + khi[0]), kp["centre_x_mm"], 5.0)
        rep.within("F7:centre_z", 0.5 * (klo[2] + khi[2]), 0.5 * sum(kp["z_range_mm"]), 5.0)
        bz = m.bbox_of("iron_bellpush_button")
        rep.add("F7:round_face", abs((bz[1][0] - bz[0][0]) - (bz[1][2] - bz[0][2])) < 0.5 and 8 <= (bz[1][0] - bz[0][0]) <= 20, {"button_w_mm": round(float(bz[1][0] - bz[0][0]), 2), "button_h_mm": round(float(bz[1][2] - bz[0][2]), 2)},
                "a round button 8-20 across (D13)", tol=0.5)
        rep.add("F7:no_keep", not m.names("iron_keep"), m.names("iron_keep"), "no keep part (D13)")
    else:
        rep.add("F7", None, "n/a", "F1: no jamb fitting (D12)")
        rep.add("F7:no_keep", not m.names("iron_keep", "iron_bellpush"), m.names("iron_keep", "iron_bellpush"), "no jamb fitting on F1 (D12)")
    if m.variant == "F1":
        kn = ir["knob"]
        klo, khi = m.bbox_of("iron_knob")
        rep.within("F8:diameter", khi[0] - klo[0], kn["diameter_mm"], 4.0)
        clo, chi = m.bbox_of("iron_knob_cap")
        rep.within("F8:projection", c.LY0 - clo[1], kn["projection_mm"], 4.0, "to the cap's top, from the leaf face")
        rlo, rhi = m.bbox_of("iron_knob_rose")
        rep.within("F8:rose", rhi[0] - rlo[0], kn["rose_diameter_mm"], 4.0)
        rep.within("F8:height", 0.5 * (klo[2] + khi[2]) - c.Z0, kn["centre_above_leaf_bottom_mm"], 4.0, "at the lock rail's centre")
        # five turned rings: count the local minima of radius along the bulb
        R = m.region(("iron_knob",), 0, c.X0 + kn["centre_u_mm"], (1, 2))
        zc = 0.5 * (klo[2] + khi[2])
        ys_ = np.arange(c.LY0 - 56.0, c.LY0 - 3.0, 0.25)
        rad = []
        for y in ys_:
            r = m.runs(R, 1, y)
            rad.append((r[-1][1] - r[0][0]) / 2 if r else 0)
        rad = np.array(rad)
        mins = [i for i in range(1, len(rad) - 1) if rad[i] < rad[i - 1] - 0.05 and rad[i] <= rad[i + 1] and rad[i] < rad[max(0, i - 6):i + 7].max() - 0.8]
        groups = []
        for i in mins:
            if not groups or i - groups[-1] > 8:
                groups.append(i)
        rep.add("F8:rings", len(groups) >= 5, len(groups), "five turned rings", "grooves of the bulb, counted in the section through its axis")
        kh = ir["old_keyhole"]
        cxk, czk = c.X0 + kh["centre_u_mm"], c.Z0 + kh["centre_above_leaf_bottom_mm"]
        blo, bhi = m.bbox_of("iron_keyhole_blank")
        plo, phi = m.bbox_of("iron_keyhole_plate")
        top_c = czk + kh["h_mm"] / 2 - kh["head_diameter_mm"] / 2
        rep.add("F8:keyhole", ("iron_keyhole_blank" in m.M) and (bhi[2] < top_c) and abs((phi[2] - plo[2]) - kh["h_mm"]) <= 3.0 and abs(0.5 * (blo[0] + bhi[0]) - cxk) < 1.0 and (bhi[0] - blo[0]) < kh["slot_w_mm"], 
                {"blank_w_mm": round(float(bhi[0] - blo[0]), 2), "blank_top_below_head_centre_mm": round(float(top_c - bhi[2]), 2), "plate_h_mm": round(float(phi[2] - plo[2]), 2)},
                "a round head over a parallel slot 8 wide, the pale blank in the slot (D11)", tol=3.0)
        piv = m.names("iron_plate_pivot")
        rep.add("F1:pivots", len(piv) == 2 and not m.names("iron_screw"), {"pivot_bosses": len(piv), "screws": len(m.names("iron_screw"))}, "two round pivot bosses at the flap's ends, no corner screws (D10)")
    else:
        rep.add("F8", None, "n/a", "F1 only")
    rep.add("F9", True, "no house number built", "optional", "absent unless the town gives a number (target F9)")
    bad = [n for n in m.M if any(k in n for k in ("hinge", "knocker", "chain", "bolt", "strap"))]
    rep.add("F10", not bad, bad, "none")


# ------------------------------------------------------------------ G: threshold, step, setting
def circle_dev(points, centre, r):
    d = np.hypot(points[:, 0] - centre[0], points[:, 1] - centre[1])
    return float(np.abs(d - r).max())


def check_G(m, rep):
    c, P = m.c, m.P
    S = P["step"]
    t = S["threshold"]
    lo, hi = m.bbox("stone_threshold")
    T1 = m.variant == "T1"
    R = m.region(("stone_threshold",), 0, c.OW / 2, (1, 2))
    pts = np.array(R.exterior.coords)[:-1]
    r = t["nose_radius_mm"]
    arc_pts = pts[(pts[:, 0] < t["front_y_mm"] + r - 0.2) & (pts[:, 1] > t["top_z"] - r + 0.2)]
    dev = circle_dev(arc_pts, (t["front_y_mm"] + r, t["top_z"] - r), r) if len(arc_pts) > 3 else 99.0
    rep.within("G1" if T1 else "G6", hi[2] - lo[2], t["thickness_mm"], 4.0, "thickness")
    rep.within("G1:front" if T1 else "G6:front", lo[1], t["front_y_mm"], 3.0, "front flush with the wall (y 0)")
    rep.add("G1:nose" if T1 else "G6:nose", dev <= 1.0, {"radius_mm": r, "worst_deviation_mm": round(dev, 2)}, "rounded top nose, r %g" % r, tol=1.0)
    rep.within("G1:top" if T1 else "G6:top", hi[2], t["top_z"], 1.0, "top at z 0")
    if not T1:
        rep.within("G6:above_paving", hi[2] - m.pivot[2], 45.0, 10.0, "the top stands 45 above the paving (z -45)")
        return
    rep.within("G2:left", -lo[0], t["bearing_into_wall_each_side_mm"], 20.0, "the threshold runs past the reveal into the brick")
    rep.within("G2:right", hi[0] - c.OW, t["bearing_into_wall_each_side_mm"], 20.0)
    rlo, rhi = m.bbox("stone_riser")
    rep.within("G3:recess", rlo[1] - lo[1], 18.0, 6.0, "riser face behind the threshold's nose")
    Rt = m.region(("stone_tread",), 0, c.OW / 2, (1, 2))
    top_z = m.runs(Rt, 1, 20.0)[-1][1]
    rep.within("G3:height", lo[2] - top_z, 72.0, 6.0, "riser: the threshold's underside to the tread's top")
    td = S["tread"]
    tlo, thi = m.bbox("stone_tread")
    rep.within("G4:top", t["top_z"] - top_z, 148.0, 25.0, "tread top below the threshold's top")
    rep.within("G4:projection", -tlo[1], td["projection_beyond_wall_face_mm"], 25.0, "tread beyond the wall face")
    rep.within("G4:width", thi[0] - tlo[0], td["width_mm"], 25.0)
    rep.within("G4:ground", t["top_z"] - tlo[2], 318.0, 25.0, "ground below the threshold's top")
    tp = np.array(Rt.exterior.coords)[:-1]
    nr = td["nosing_radius_mm"]
    ztop_f = td["top_z_mm"] - td["fall_to_front_mm"]
    centre = (td["front_y_mm"] + nr, ztop_f - nr)
    nose_pts = tp[(tp[:, 0] < centre[0] - 0.2) & (tp[:, 1] > centre[1] - 36.0) & (tp[:, 1] < ztop_f - 0.2)]
    dev = circle_dev(nose_pts, centre, nr) if len(nose_pts) > 3 else 99.0
    rep.add("G4:nose", dev <= 3.0 and abs(nr - 45.0) <= 15.0, {"radius_mm": nr, "worst_deviation_mm": round(dev, 2)}, "a full half-round of radius 45 +-15", tol=15.0)
    base = tp[(tp[:, 1] < centre[1] - 40.0) & (tp[:, 0] > td["front_y_mm"] + 5.0)]
    rep.within("G4:undercut", float(base[:, 0].min() - tlo[1]), td["undercut_mm"], 10.0, "the base face stands this far behind the nose's front")
    plan = m.region(("stone_tread",), 2, centre[1], (0, 1))
    pp = np.array(plan.exterior.coords)[:-1]
    rc = td["plan_corner_radius_mm"]
    cc = (td["x_mm"][1] - rc, td["front_y_mm"] + rc)
    cp = pp[(pp[:, 0] > cc[0] + 0.5) & (pp[:, 1] < cc[1] - 0.5)]
    rep.add("G4:plan_corner", len(cp) > 3 and circle_dev(cp, cc, rc) <= 3.0, {"radius_mm": rc, "worst_deviation_mm": round(circle_dev(cp, cc, rc), 2) if len(cp) > 3 else None}, "plan corner r 40", tol=3.0)
    rep.within("G5:left", -tlo[0], 39.0, 20.0, "the step wider than the opening")
    rep.within("G5:right", thi[0] - c.OW, 39.0, 20.0)


# ------------------------------------------------------------------ the context wall (T1): G7-G12, Q1-Q3, L1-L5
class CtxModel(Model):
    def __init__(self, T, variant, npz):
        self.T, self.variant = T, variant
        self.P = bd.variant_parts(T, variant)
        self.pivot = np.array(T["glb_pivot"]["terrace_four_panel" if variant == "T1" else "flat_door_over_shop"], float)
        raw = load_npz(npz)
        self.M = {n: (V + self.pivot / 1000.0, F) for n, (V, F) in raw.items()}
        self.doc = td.all_drawings(T, VAR_KEY[variant])
        self.c = td.consts(self.P)


def export_context(T, variant, path):
    import bpy
    import blender_parts
    bpy.ops.wm.read_factory_settings(use_empty=True)
    pivot = T["glb_pivot"]["terrace_four_panel" if variant == "T1" else "flat_door_over_shop"]
    parts = dc.build(T, variant)
    obs = dc.make_objects(parts, variant, pivot)
    blender_parts.export(obs, path)
    return parts


def fit_circle(pts):
    A = np.c_[2 * pts[:, 0], 2 * pts[:, 1], np.ones(len(pts))]
    b = (pts ** 2).sum(1)
    x, *_ = np.linalg.lstsq(A, b, rcond=None)
    return x[0], x[1], math.sqrt(x[2] + x[0] ** 2 + x[1] ** 2)


def check_context(T, m, cm, rep, overlays):
    """Checks on the context wall: it equals the drawing, then the target's arch, quoin and plinth checks."""
    c, P = m.c, m.P
    B = P["brick"]
    a = B["arch"]
    q = B["quoins"]
    pl = B["plinth"]
    # --- the wall against the drawing: buff (quoins and arch) and the plinth, in elevation
    E = m.doc["elevation"]["polygons"]
    fr = frame_for([p["pts"] for p in E if p["layer"] == "buff"], 30.0)
    hh, ww = fr.shape
    u = (fr.u0 + (np.arange(ww) + 0.5) * fr.mm_per_px / 1000) * 1000
    v = (fr.v0 + fr.height - (np.arange(hh) + 0.5) * fr.mm_per_px / 1000) * 1000
    win = (u[None, :] >= -400) & (u[None, :] <= c.OW + 400)
    tq = raster_polys([p for p in E if p["layer"] == "buff" and p["name"].startswith("quoin")], fr)
    ta = raster_polys([p for p in E if p["layer"] == "buff" and not p["name"].startswith("quoin")], fr)
    # the drawing leaves a 10 mm course joint above every course; the built blocks are whole (the joints are the brick shader's), so
    # the drawn quoins are closed over the joints and carried up 10 mm
    n_up = int(round(10.0 / MMPX))
    tq = ndimage.binary_closing(tq, np.ones((2 * n_up + 3, 1), bool))
    up = tq.copy()
    for k in range(1, n_up + 1):
        up[:-k] |= tq[k:]
    tb = up | ta
    mb = np.zeros(fr.shape, bool)
    for n in cm.names("ctx_quoin", "ctx_arch_brick"):
        mb |= silhouette({n: cm.M[n]}, (0, 2), fr)
    mb, tb = fill_pinholes(mb) & win, fill_pinholes(tb) & win
    r = verdict(compare(mb, tb, MMPX))
    rep.add("CTX:buff_elevation", r["ok"], {k: r[k] for k in ("iou", "p95_mm", "max_mm")}, "IoU >= 0.97, p95 <= 2, worst <= 6",
            "the built quoins and arch against the drawing's buff layer (the drawing's 10 mm course joints closed)")
    if overlays:
        overlay(mb, tb, os.path.join(overlays, "ctx_buff_elevation_T1.png"))
    # plinth and wall front: silhouette of all context parts has no holes (a gap would show the interior)
    # --- Q1-Q3 quoins
    qparts = [(n, cm.bbox(n)) for n in cm.names("ctx_quoin")]
    zs = {}
    for n, (lo, hi) in qparts:
        zs.setdefault(round(float(lo[2]), 1), set()).add((n[10], round(float(hi[0] - lo[0]), 1)))
    zkeys = sorted(zs)
    bz = [round(z, 1) for z in zkeys]
    exp = [z0 for z0, _ in q["block_z_mm"]]
    widths_by_block = [sorted(w for _, w in zs[z0]) for z0 in zkeys]
    both_in_step = all(len(set(w)) == 1 for w in widths_by_block)
    wl = [w[0] for w in widths_by_block]
    alt = all(wl[i] != wl[i + 1] for i in range(len(wl) - 1))
    steps = [round(b - a_, 1) for a_, b in zip(zkeys, zkeys[1:])]
    rep.add("Q1", len(zkeys) == q["blocks"] and all(abs(s - 231.0) <= 8.0 for s in steps) and both_in_step and alt and wl[0] > wl[-1],
            {"blocks": len(zkeys), "steps_mm": sorted(set(steps)), "both_sides_in_step": both_in_step, "alternate": alt, "bottom_width": wl[0], "top_width": wl[-1],
             "block_z0": bz}, "10 blocks of 231 +-8; bottom long, top short; alternating; both sides alike", tol=8.0)
    rep.add("Q2", all(abs(w - q["stretcher_width_mm"]) <= 12 for w in wl[0::2]) and all(abs(w - q["header_width_mm"]) <= 12 for w in wl[1::2]),
            {"long": sorted(set(wl[0::2])), "short": sorted(set(wl[1::2])), "course_gauge_mm": q["course_gauge_mm"], "joint_mm": q["joint_mm"]},
            "122 / 237 +-12; gauge 77; joints 10", "widths measured on the blocks; the 77 gauge and 10 mm joints are the brick shader's rows (render_door.py: 0.077 / 0.010), not geometry", tol=12.0)
    ret = all(abs((cm.bbox(n)[1][1] - cm.bbox(n)[0][1]) - c.REV) < 0.5 for n, _ in qparts)
    rep.add("Q3", ret, "return faces buff", "buff", "each block runs the reveal's full depth (114.3), so its x = 0 / 882 face is the buff return")
    # --- the arch
    br = [n for n in cm.names("ctx_arch_brick")]
    rep.add("G11:count", len(br) == a["bricks"], len(br), "exactly 13 bricks")
    pts = np.vstack([cm.M[n][0][:, [0, 2]] * 1000 for n in br])
    cx, cz = a["soffit_circle"]["centre_x_mm"], a["soffit_circle"]["centre_z_mm"]
    dist = np.hypot(pts[:, 0] - cx, pts[:, 1] - cz)
    Rin, Rout = a["soffit_circle"]["radius_mm"], a["soffit_circle"]["radius_mm"] + a["depth_mm"]
    inner, outer = pts[np.abs(dist - Rin) < 0.5], pts[np.abs(dist - Rout) < 0.5]
    fx, fz, fr_ = fit_circle(inner)
    rep.add("G11:soffit_circle", abs(fr_ - Rin) < 2 and abs(fx - cx) < 2 and abs(fz - cz) < 5, {"fitted_radius": round(float(fr_), 1), "centre": [round(float(fx), 1), round(float(fz), 1)]}, "R 5411 through (0, 2322), (441, 2340), (882, 2322)")
    zc = float(outer[:, 1].max())
    zend = float(outer[outer[:, 0] < outer[:, 0].min() + 0.5][:, 1].mean())
    rep.within("G11:extrados_rise", zc - zend, a["extrados_rise_crown_over_ends_mm"], 6.0, "extrados crown over its ends (crown z %.1f)" % zc)
    worst = 0.0
    for n in br:
        V = cm.M[n][0] * 1000
        f = V[np.abs(V[:, 1]) < 0.01][:, [0, 2]]                    # the brick's front face (y = 0)
        ang_ = np.arctan2(f[:, 0] - cx, f[:, 1] - cz)
        for end in (ang_.min(), ang_.max()):
            e = f[np.abs(ang_ - end) < 1e-6]
            r_ = np.hypot(e[:, 0] - cx, e[:, 1] - cz)
            lo_, hi_ = e[np.argmin(r_)], e[np.argmax(r_)]
            d = hi_ - lo_
            rad = np.array([math.sin(end), math.cos(end)])
            worst = max(worst, math.degrees(math.acos(min(1.0, abs(float(d @ rad)) / float(np.hypot(*d))))))
    rep.add("G11:radial_joints", worst < 2.0, round(worst, 3), "within 2 degrees of radial", tol=2.0)
    rep.add("G11:extrados_concentric", abs(float(np.hypot(outer[:, 0] - fx, outer[:, 1] - fz).std())) < 0.5, round(float(np.hypot(outer[:, 0] - fx, outer[:, 1] - fz).std()), 3), "extrados parallel to the soffit")
    rep.within("G7:depth", Rout - Rin, a["depth_mm"], 7.0, "ring depth")
    rep.within("G7:overhang_left", -float(pts[:, 0].min()), a["bearing_beyond_reveal_each_side_mm"], 7.0, "ring's extrados corner beyond the left reveal")
    rep.within("G7:overhang_right", float(pts[:, 0].max()) - c.OW, a["bearing_beyond_reveal_each_side_mm"], 7.0)
    rep.within("G7:camber", (cz + fr_) - float(inner[(abs(inner[:, 0]) < 6.0)][:, 1].mean()), a["soffit_camber_rise_mm"], 7.0, "soffit crown over its springing")
    # G8: the door's head follows the soffit
    worst = 0.0
    for x in (0.0, 220.0, 441.0, 660.0, 882.0):
        ztop = m.region(("frame_head",), 0, x, (1, 2)).bounds[3]
        zs_ = fz + math.sqrt(fr_ ** 2 - (x - fx) ** 2)
        worst = max(worst, abs(ztop - zs_))
    rep.add("G8", worst <= 3.0, round(worst, 2), "equal within 3", tol=3.0)
    # G9: the ring's end rests on the top quoin block; the quoins touch the wall
    top = max(((cm.bbox(n)[1][2], n) for n, _ in qparts))[0]
    lowest = float(inner[:, 1].min())
    ends = inner[inner[:, 1] < lowest + 0.6]
    le, re_ = ends[ends[:, 0] < c.OW / 2], ends[ends[:, 0] > c.OW / 2]
    w_top = q["header_width_mm"]
    ok9 = abs(lowest - top) <= 12.0 and bool((le[:, 0] > -w_top - 1).all() and (le[:, 0] < 1).all() and (re_[:, 0] > c.OW - 1).all() and (re_[:, 0] < c.OW + w_top + 1).all())
    rep.add("G9", ok9, {"ring_end_z": round(lowest, 2), "top_block_top_z": round(float(top), 2), "left_end_x": round(float(le[:, 0].mean()), 1), "right_end_x": round(float(re_[:, 0].mean()), 1)},
            "within 12 mm of the top block's top face, over its 122 mm", tol=12.0)
    # G12: against photograph 1: evaluated on the drawing by self_check.py; the built ring is the drawing's (CTX:buff_elevation)
    rep.add("G12", None, "see CTX:buff_elevation", "within 2.5 px on P1", "target's self_check.py fits the drawing's ring to P1; the built ring equals the drawing within the pass rule above")
    # --- the plinth
    lo, hi = cm.bbox("ctx_plinth_L")
    rep.within("L1:front", -lo[1], pl["front_proud_of_wall_face_mm"], 20.0, "plinth front proud of the wall face")
    rep.within("L1:ground", -lo[2], 318.0, 1.0, "from the ground")
    sec = cm.region(("ctx_plinth_L",), 0, -60.0, (1, 2))
    pp = np.array(sec.exterior.coords)[:-1]
    sp = pl["splay"]
    top_pts = pp[(pp[:, 1] > sp["z_from_mm"] - 1.0)]
    splay_vertex = pp[np.argmin(np.hypot(pp[:, 0] - (-60.0), pp[:, 1] - sp["z_from_mm"]))]
    top_vertex = pp[np.argmin(np.hypot(pp[:, 0] - 0.0, pp[:, 1] - sp["z_to_mm"]))]
    ang = math.degrees(math.atan2(top_vertex[1] - splay_vertex[1], top_vertex[0] - splay_vertex[0]))
    rep.within("L2:angle", ang, 45.0, 8.0, "splay, degrees")
    rep.within("L2:top_z", float(top_vertex[1]), sp["z_to_mm"], 3.0, "splay's top edge on the wall face")
    vert_top = float(pp[(np.abs(pp[:, 0] + 60.0) < 0.1)][:, 1].max())
    rep.within("L1:vertical_face_top", vert_top, sp["z_from_mm"], 3.0, "vertical face runs to z -48")
    # L3 (the review's amendment replaces the target's 'nothing of it in the clear opening'): the returns
    rl, rh = cm.bbox("ctx_plinth_return_L")
    rrl, rrh = cm.bbox("ctx_plinth_return_R")
    rep.within("L3:return_left_inner_face", rh[0], 70.0, 15.0, "inner face at x 70 (the review: 70 +-15)")
    rep.within("L3:return_right_inner_face", rrl[0], c.OW - 70.0, 15.0, "inner face at x 812")
    rep.add("L3:return_depth", abs(rl[1] + 60.0) < 0.5 and abs(rh[1]) < 0.5, [round(float(rl[1]), 1), round(float(rh[1]), 1)], "from y -60 back to the threshold's front (y 0)")
    rep.within("L3:return_top", rh[2], 12.0, 0.5, "stands to z 12")
    rep.add("L3:return_foot", rl[2] <= S_top(P) - 0.0 and rl[2] >= S_top(P) - 8.0, round(float(rl[2]), 1), "from the tread's top (z -148)")
    tl, th = m.bbox("stone_threshold")
    vis = (c.OW - 70.0) - 70.0
    rep.within("L3:visible_threshold_length", vis, 742.0, 30.0, "the threshold and riser show only between the returns")
    for nm, cutx in (("front splay", 5.0),):
        sec = cm.region(("ctx_plinth_return_L",), 0, cutx, (1, 2))
        pr = np.array(sec.exterior.coords)[:-1]
        a_ = pr[np.argmin(np.hypot(pr[:, 0] + 60.0, pr[:, 1] + 48.0))]
        b_ = pr[np.argmin(np.hypot(pr[:, 0] - 0.0, pr[:, 1] - 12.0))]
        rep.within("L3:return_front_splay", math.degrees(math.atan2(b_[1] - a_[1], b_[0] - a_[0])), 45.0, 8.0, "the splayed course on the return's front")
    sec = cm.region(("ctx_plinth_return_L",), 1, -5.0, (0, 2))
    pr = np.array(sec.exterior.coords)[:-1]
    a_ = pr[np.argmin(np.hypot(pr[:, 0] - 70.0, pr[:, 1] + 48.0))]
    b_ = pr[np.argmin(np.hypot(pr[:, 0] - 15.0, pr[:, 1] - 7.0))]
    rep.within("L3:return_inner_splay", math.degrees(math.atan2(b_[1] - a_[1], a_[0] - b_[0])), 45.0, 8.0, "mitred round the corner: the splay on the inner face")
    # L4: the tread's plan beside the plinth: no overlap at z -200 and z -300
    ov = 0.0
    for zq in (-200.0, -300.0):
        ta = m.region(("stone_tread",), 2, zq, (0, 1))
        pa = cm.region(("ctx_plinth_L", "ctx_plinth_R", "ctx_plinth_return"), 2, zq, (0, 1))
        ov += ta.intersection(pa).area
    rep.add("L4", ov < 1.0, round(ov, 3), "no overlap, mm2", "the tread's plan against the plinth, two cuts")
    jl = m.bbox("frame_jamb_L")
    rep.add("L5", abs(jl[0][2]) <= 1.0, {"jamb_foot_z": round(float(jl[0][2]), 2), "plinth_top_z": 12.0}, "feet on the threshold at z 0, square against the plinth's top", "the reveal's brick lip (z 0 to 12) stands beside each jamb's foot")


def S_top(P):
    return P["step"]["tread"]["top_z_mm"]


# ------------------------------------------------------------------ I: surfaces (mesh and glb)
def triangle_planes(M):
    out = []
    for name, (V, F) in M.items():
        P = V * 1000.0
        a, b, c = P[F[:, 0]], P[F[:, 1]], P[F[:, 2]]
        n = np.cross(b - a, c - a)
        L = np.linalg.norm(n, axis=1)
        ok = L > 1e-9
        n[ok] /= L[ok, None]
        d = (n * a).sum(1)
        for i in np.nonzero(ok)[0]:
            out.append((name, n[i], d[i], np.array([a[i], b[i], c[i]]), L[i] / 2))
    return out


def basis(n):
    t = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(n, t)
    u /= np.linalg.norm(u)
    return u, np.cross(n, u)


def coplanar_overlaps(M, tol=0.1, min_area=1.0, limit=20):
    """Faces of different parts that lie in one plane (within `tol` mm) and overlap by more than `min_area` mm2.
    Same-facing pairs are the z-fighting kind (hatching); opposite-facing pairs are two parts meeting back to back (hidden)."""
    tris = triangle_planes(M)
    groups = defaultdict(list)
    for i, (name, n, d, pts, ar) in enumerate(tris):
        sgn = 1.0
        for k in range(3):
            if abs(n[k]) > 1e-6:
                sgn = 1.0 if n[k] > 0 else -1.0
                break
        key = (round(sgn * n[0], 2) + 0.0, round(sgn * n[1], 2) + 0.0, round(sgn * n[2], 2) + 0.0)
        groups[key].append((i, sgn, sgn * d))
    same, opp, examples = 0, 0, []
    for key, items in groups.items():
        if len({tris[i][0] for i, _, _ in items}) < 2:
            continue
        items.sort(key=lambda t: t[2])
        for ai in range(len(items)):
            i, si, di = items[ai]
            for bi in range(ai + 1, len(items)):
                j, sj, dj = items[bi]
                if dj - di > tol:
                    break
                if tris[i][0] == tris[j][0]:
                    continue
                if np.abs(tris[i][1] * si - tris[j][1] * sj).max() > 0.02:
                    continue
                u, v = basis(tris[i][1])
                A = Polygon([(p @ u, p @ v) for p in tris[i][3]])
                Bp = Polygon([(p @ u, p @ v) for p in tris[j][3]])
                if not A.intersects(Bp):
                    continue
                area = A.intersection(Bp).area
                if area > min_area:
                    if si == sj:
                        same += 1
                        if len(examples) < limit:
                            examples.append([tris[i][0], tris[j][0], round(area, 1), [round(float(x), 3) for x in tris[i][1]]])
                    else:
                        opp += 1
    return same, opp, examples


def read_glb(path):
    """The .glb's own data: for every mesh primitive, positions, shading normals and triangle indices (importer-independent)."""
    import struct
    b = open(path, "rb").read()
    magic, ver, length = struct.unpack("<4sII", b[:12])
    off, js, binc = 12, None, b""
    while off < length:
        clen, ctype = struct.unpack("<I4s", b[off:off + 8])
        data = b[off + 8:off + 8 + clen]
        off += 8 + clen
        if ctype == b"JSON":
            js = json.loads(data)
        elif ctype.startswith(b"BIN"):
            binc = data
    comp = {5121: np.uint8, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
    nvec = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}

    def acc(i):
        a = js["accessors"][i]
        bv = js["bufferViews"][a["bufferView"]]
        dt = comp[a["componentType"]]
        n = a["count"] * nvec[a["type"]]
        start = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
        arr = np.frombuffer(binc, dtype=dt, count=n, offset=start)
        return arr.reshape(a["count"], nvec[a["type"]]) if nvec[a["type"]] > 1 else arr
    out = {}
    for mesh in js["meshes"]:
        for pr in mesh["primitives"]:
            at = pr["attributes"]
            out.setdefault(mesh.get("name", "?"), []).append({"P": acc(at["POSITION"]).astype(float), "N": acc(at["NORMAL"]).astype(float),
                                                              "I": acc(pr["indices"]).astype(np.int64).reshape(-1, 3), "uv": ("TEXCOORD_0" in at, "TEXCOORD_1" in at)})
    return out, js


def glb_edges(path):
    """Hard and soft edges from the written normals: an edge is split when the two faces beside it carry different normals at its ends."""
    meshes, js = read_glb(path)
    stats = {"hard": [0, 0], "soft": [0, 0]}
    per = {}
    for name, prims in meshes.items():
        for pm in prims:
            P, N, I = pm["P"], pm["N"], pm["I"]
            key = {}
            for t in range(len(I)):
                a, b, c_ = P[I[t]]
                n = np.cross(b - a, c_ - a)
                ln = np.linalg.norm(n)
                if ln < 1e-12:
                    continue
                n /= ln
                for k in range(3):
                    i0, i1 = I[t][k], I[t][(k + 1) % 3]
                    e = tuple(sorted((tuple(np.round(P[i0], 5)), tuple(np.round(P[i1], 5)))))
                    key.setdefault(e, []).append((t, n, i0, i1))
            hard = [0, 0]
            soft = [0, 0]
            for e, lst in key.items():
                if len(lst) != 2:
                    continue
                (t1, n1, a1, b1), (t2, n2, a2, b2) = lst
                ang = math.degrees(math.acos(max(-1.0, min(1.0, float(n1 @ n2)))))
                # the normal at the first end of the edge, in each triangle
                p0 = tuple(np.round(P[a1], 5))
                v2 = a2 if tuple(np.round(P[a2], 5)) == p0 else b2
                diff = float(np.linalg.norm(N[a1] - N[v2]))
                if ang > 40.0:
                    hard[1] += 1
                    hard[0] += diff > 0.05
                elif 3.0 < ang < 25.0 and name.startswith("moulding_"):
                    soft[1] += 1
                    soft[0] += diff < 0.05
            per[name] = {"hard": hard, "soft": soft}
            for k_, v_ in (("hard", hard), ("soft", soft)):
                stats[k_][0] += v_[0]
                stats[k_][1] += v_[1]
    return stats, per


def glb_info(path, variant, P, T):
    """Read the .glb as written: shading normals, materials, UV sets, bounds."""
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path, merge_vertices=True)
    obs = [o for o in bpy.data.objects if o.type == "MESH"]
    info = {"objects": len(obs)}
    lo = np.full(3, 1e9)
    hi = np.full(3, -1e9)
    uv_ok = True
    tri = 0
    for o in obs:
        me = o.data
        me.calc_loop_triangles()
        tri += len(me.loop_triangles)
        uv_ok &= len(me.uv_layers) == 1
        for v in me.vertices:
            w = o.matrix_world @ v.co
            lo = np.minimum(lo, w[:])
            hi = np.maximum(hi, w[:])
    meshes_, _js = read_glb(path)
    tri = int(sum(len(pm["I"]) for prims in meshes_.values() for pm in prims))          # triangles as written in the file
    info.update(bounds_m=[lo.round(4).tolist(), hi.round(4).tolist()], one_uv_set=bool(uv_ok), triangles=tri, bytes=os.path.getsize(path))
    # shading normals: the jambs' flat front faces; hard and soft edges
    flat_area = tot_area = 0.0
    hard_ok = hard_all = soft_ok = soft_all = 0
    for o in obs:
        me = o.data
        arr = np.empty(len(me.loops) * 3)
        me.corner_normals.foreach_get("vector", arr)
        cn = arr.reshape(-1, 3)
        if o.name.startswith("frame_jamb"):
            for p in me.polygons:
                if p.normal.y < -0.99:
                    a = p.area
                    tot_area += a
                    ok = True
                    for li in range(p.loop_start, p.loop_start + p.loop_total):
                        cosv = float(np.dot(cn[li], np.array(p.normal[:])))
                        if math.degrees(math.acos(max(-1.0, min(1.0, cosv)))) > 3.0:
                            ok = False
                    if ok:
                        flat_area += a
        if o.name.startswith(("frame_", "leaf_", "moulding_band", "iron_letter_plate", "moulding_bolection", "moulding_weatherboard", "stone_")):
            emap = defaultdict(list)
            for p in me.polygons:
                for li in range(p.loop_start, p.loop_start + p.loop_total):
                    emap[me.loops[li].edge_index].append((p.index, li))
            for ei, lst in emap.items():
                if len(lst) != 2:
                    continue
                (pa, la), (pb, lb) = lst
                na, nb = np.array(me.polygons[pa].normal[:]), np.array(me.polygons[pb].normal[:])
                ang = math.degrees(math.acos(max(-1.0, min(1.0, float(na @ nb)))))
                e = me.edges[ei]
                v0 = e.vertices[0]
                # corner normals at this edge's first vertex, in each polygon
                def cn_at(pi, vv):
                    p = me.polygons[pi]
                    for li in range(p.loop_start, p.loop_start + p.loop_total):
                        if me.loops[li].vertex_index == vv:
                            return cn[li]
                diff = float(np.linalg.norm(cn_at(pa, v0) - cn_at(pb, v0)))
                if ang > 40.0:
                    hard_all += 1
                    hard_ok += diff > 0.05
                elif 3.0 < ang < 25.0 and (o.name.startswith("moulding_")):
                    soft_all += 1
                    soft_ok += diff < 0.05
    st, per = glb_edges(path)
    info.update(jamb_face_flat_fraction=(flat_area / tot_area) if tot_area else None, hard_edges=st["hard"], soft_edges=st["soft"])
    mats = {}
    for mt in bpy.data.materials:
        if mt.use_nodes:
            b = mt.node_tree.nodes.get("Principled BSDF")
            if b:
                col = b.inputs["Base Color"].default_value
                to_s = lambda x: 255 * (12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055)
                mats[mt.name] = {"srgb": [round(to_s(col[i])) for i in range(3)], "roughness": round(b.inputs["Roughness"].default_value, 3), "metallic": round(b.inputs["Metallic"].default_value, 3)}
    info["materials"] = mats
    return info


def check_I(m, rep, glb, glb_path):
    c, P, T = m.c, m.P, m.T
    same, opp, ex = coplanar_overlaps(m.M)
    rep.add("I1", same == 0, {"same_facing_overlaps": same, "back_to_back_contacts": opp, "examples": ex[:6]}, 0,
            "no two visible faces of different parts coplanar and overlapping (z-fighting kind); back-to-back contacts are where frame members butt (jamb to head, transom to jamb) and are hidden")
    bad = [n for n in m.names("moulding_bolection", "moulding_single", "frame_glazing_bead", "moulding_band", "moulding_weatherboard") if not joinery_closed(m.M[n][1])]
    rep.add("I2", not bad, {"open_meshes": bad}, "every moulding a closed ring (no mitre gap)", "each sweep is one closed mitred ring of faces: no gap to measure")
    h, s = glb["hard_edges"], glb["soft_edges"]
    rep.add("I3", h[1] > 0 and h[0] >= 0.98 * h[1] and s[1] > 0 and s[0] >= 0.95 * s[1], {"hard_edges_split": "%d of %d" % tuple(h), "curved_faces_smooth": "%d of %d" % tuple(s)},
            "edges above 40 degrees split; the mouldings' curved faces smooth", "from the shading normals in the .glb as written")
    mats = glb["materials"]
    ok = True
    notes = []
    dcols = {d["srgb"][0] * 1000000 + d["srgb"][1] * 1000 + d["srgb"][2]: d["id"] for d in T["door_colours"]}
    for name, mm in mats.items():
        if name.startswith("paint_"):
            ident = name[6:]
            want = None
            for lst in (T["door_colours"], T["frame_colours"]):
                for d in lst:
                    if d["id"] == ident:
                        want = d["srgb"]
            good = want is not None and all(abs(a - b) <= 6 for a, b in zip(mm["srgb"], want)) and mm["metallic"] == 0.0 and abs(mm["roughness"] - 0.35) < 0.2
            ok &= good
            notes.append((name, mm["srgb"], want, mm["roughness"]))
        elif name == "brass":
            good = all(abs(a - b) <= 6 for a, b in zip(mm["srgb"], T["materials"]["brass"]["base_srgb"])) and mm["metallic"] == 1.0 and abs(mm["roughness"] - 0.4) < 0.01
            ok &= good
    rep.add("I4", ok, mats, "base colours within 6 (sRGB) of door_colours / frame_colours / materials; metal and roughness as the target", "starting values; the look is developed in Unreal")
    lo, hi = np.array(glb["bounds_m"][0]), np.array(glb["bounds_m"][1])
    frame_w = (c.JR[1] - c.JL[0])
    fw = m.bbox("frame_jamb_L")[0][0], m.bbox("frame_jamb_R")[1][0]
    centre_x = 0.5 * (fw[0] + fw[1]) - m.pivot[0]
    rep.add("I5:pivot", abs(centre_x) < 1.0 and abs(lo[2] - (m.bbox("stone_threshold", "stone_tread")[0][2] - m.pivot[2]) / 1000.0) < 0.001,
            {"frame_centre_x_mm": round(float(centre_x), 2), "lowest_z_m": float(lo[2])}, "pivot at the base's centre on the ground: x = the opening's centre, z = the ground (F1's sill stands 25 below it)")
    rep.add("I5:units", float(hi[2]) < 3.5 and float(hi[2]) > 1.5, [round(float(lo[0]), 3), round(float(hi[0]), 3)], "metres, z up")
    rep.add("I5:uv", bool(glb["one_uv_set"]), glb["one_uv_set"], "one UV set per part")
    rep.within("I5:frame_width", frame_w, 975.2 if m.variant == "T1" else 1000.4, 5.0, "across the frame")
    lim = P["frame"]["jamb_x_mm"]
    out = []
    horns = []
    for n in m.M:
        l, h_ = m.bbox(n)
        if n == "stone_threshold" and m.variant == "T1":
            horns = [(n, round(float(l[0]), 1), round(float(h_[0]), 1))]
            continue
        if l[0] < lim["left"][0] - 5.0 or h_[0] > lim["right"][1] + 5.0:
            out.append((n, round(float(l[0]), 1), round(float(h_[0]), 1)))
    rep.add("I5:inside_bounding_box", not out, {"beyond": out, "exception": horns}, "no part beyond the frame's width by more than 5 mm",
            "the threshold's horns (112 beyond each reveal, 65 beyond the frame) are G2's own requirement and the one exception" if horns else "")
    rep.add("I5:size", glb["bytes"] < 1_000_000, glb["bytes"], "< 1 MB")


def joinery_closed(F):
    from collections import Counter
    E = Counter()
    for f in F:
        for i in range(3):
            E[tuple(sorted((int(f[i]), int(f[(i + 1) % 3]))))] += 1
    return all(v == 2 for v in E.values())


# ------------------------------------------------------------------ the whole run
def run_variant(T, variant, a):
    npz = os.path.join(a.npz_dir, "door_%s.npz" % variant)
    glb_path = os.path.join(a.glb_dir, "door_%s.glb" % variant)
    ov = None
    if a.overlays:
        ov = os.path.join(a.overlays, variant)
        os.makedirs(ov, exist_ok=True)
    m = Model(T, variant, npz)
    rep = Report()
    glb = glb_info(glb_path, variant, m.P, T)
    check_A1(m, rep, ov)
    check_sections(m, rep, ov)
    cm = None
    if variant == "T1":
        cpath = os.path.join(a.npz_dir, "context_T1.npz")
        export_context(T, "T1", cpath)
        cm = CtxModel(T, "T1", cpath)
    check_A4(m, rep, cm.M if cm else None)
    check_B(m, rep)
    check_C(m, rep, glb)
    check_D(m, rep)
    check_EW(m, rep)
    check_F(m, rep)
    check_G(m, rep)
    if cm is not None:
        check_context(T, m, cm, rep, ov)
        same, opp, ex = coplanar_overlaps(cm.M)
        rep.add("I1:context", None, {"same_facing_overlaps": same, "back_to_back_contacts": opp, "examples": ex[:5]}, "info", "the context wall's own faces (review only, never in the .glb)", extra=True)
    else:
        for k in ("G7", "G8", "G9", "G11", "G12", "Q1", "Q2", "Q3", "L1", "L2", "L3", "L4", "L5"):
            rep.add(k, None, "n/a", "T1 only")
    check_I(m, rep, glb, glb_path)
    rep.add("H1", None, "see A1", "built elevation laid on P1 within 2.5 px", "evaluated on the drawing by the target's self_check.py (303 of 304); the model equals that drawing (A1, every layer)")
    rep.add("H2", None, "see A1", "F1 against P2", "evaluated on the drawing by self_check.py group 4; the model equals that drawing (A1)")
    rep.adapt.append("I1 is measured as the target's reason for it asks (diagonal hatching): no two faces of different parts coplanar within 0.1 mm, facing the same way and overlapping by more than 1 mm2 (0 found). Faces facing opposite ways where two parts butt (jamb to head, transom to jamb, the plinth to the wall) are counted and reported as back-to-back contacts: they are hidden, and are how joinery meets.")
    rep.adapt.append("C2: 'the visible jamb face's normals within 3 degrees' is measured on the jamb's flat front faces; the two 1 mm eases (target: every arris eased 1 mm) are 2.8% of the visible width and are their own 45 degree faces, not counted as the face.")
    if variant == "T1":
        rep.adapt.append("L3 and L5 follow the target review's amendment (plinth returns 70 +-15 wide into the doorway, inner faces at x 70 and 812, the threshold and riser showing 742 +-30 between them), not target.json's 'nothing of it in the clear opening'; the returns are the wall's, in the context, never in the .glb (DECISIONS.md 8 Oct).")
        rep.adapt.append("I5 (T1): the threshold's horns run 112 beyond each reveal (G2), 65 beyond the frame's width; that is the one part outside I5's 975.2 mm, by the target's own requirement.")
        rep.adapt.append("G12, H1, H2: tested on the photographs by the target's self_check.py against the drawing (303 of 304); the built door equals that drawing within the pass rule (A1-A4, CTX:buff_elevation), so they are reported as covered, not re-measured on the photographs (not reachable from this cloud).")
    for d in T.get("_departures", []):
        if variant in d["variants"]:
            rep.adapt.append("%s (the photographs win over target.json): %s. Measured: %s. Photograph: %s." % (d["id"], d["what"], d["measured"], d["photograph"]))
    rep.adapt.append("E3, W3, F5:keyway, F5:collar_proud, F7, F8:keyhole, F1:pivots, G4 (nose radius, plan corner, width, x) and B10 are the target's checks re-aimed at the departed numbers (every other check is the target's, unchanged); "
                     "G6:front follows the amended sill front (F1).")
    required = [r for r in rep.rows if not r.get("extra") and r["ok"] is not None]
    failed = [r["id"] for r in required if not r["ok"]]
    extras = [r for r in rep.rows if r.get("extra")]
    out = {"variant": variant, "pass": not failed, "failed": failed, "checks_run": len(required), "checks_passed": len(required) - len(failed),
           "extras": {"run": len(extras), "passed": sum(1 for r in extras if r["ok"]), "failed": [r["id"] for r in extras if r["ok"] is False]},
           "not_applicable_or_covered": [r["id"] for r in rep.rows if r["ok"] is None], "triangles": glb["triangles"], "glb_bytes": glb["bytes"],
           "adaptations": sorted(set(rep.adapt)), "rows": rep.rows}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="both", choices=["T1", "F1", "both"])
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--npz-dir", default=bd.NPZ_DIR)
    ap.add_argument("--glb-dir", default=bd.ASSET_DIR)
    ap.add_argument("--overlays", default="/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/door-build/v1/check-overlays")
    a = ap.parse_args()
    T = bd.load_target()
    res = {"model": "production/assets/cloud-week/door/door_<V>.glb, kit/door/build/door_<V>.npz", "pass_rule": {"IoU": ">= 0.97", "outline_p95_mm": "<= 2", "outline_worst_mm": "<= 6",
           "profiles": "p95 <= 1.5, worst <= 3", "dimensions": "within each check's own tolerance (1 mm unless the target gives another)"}, "variants": {}}
    for v in (["T1", "F1"] if a.variant == "both" else [a.variant]):
        r = run_variant(T, v, a)
        res["variants"][v] = r
        print(v, "PASS" if r["pass"] else "FAIL", "required %d of %d" % (r["checks_passed"], r["checks_run"]), "failed:", r["failed"], "extras failed:", r["extras"]["failed"])
    res["pass"] = all(r["pass"] for r in res["variants"].values())
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    path = os.path.join(HERE, "checks", "check_v%d.json" % a.version)
    json.dump(res, open(path, "w"), indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    print("wrote", path)
    return res


if __name__ == "__main__":
    main()
