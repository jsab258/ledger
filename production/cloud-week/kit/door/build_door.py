"""The front door, built by script from target.json alone (cloud week 42, piece 3.1).

    /home/user/.bpyenv/bin/python build_door.py [--variant T1|F1|both] [--door-colour ID] [--frame-colour ID]
                                                [--out-dir DIR] [--npz-dir DIR]

Two variants: T1, the terrace four-panel front door in its brick opening (default paint black), and F1, the
side door to a flat over a shop (default paint dark green). Both are read from production/cloud-week/targets/
front-door/target.json; target_drawing.py (the check's reference) is not read here. A few small section numbers that target.json
does not give are the ones target_drawing.py draws, taken over by hand because the check compares with those drawings: the
inside moulding's section points (4, 10/6, 16/4 of its 22), the letter plate's 2 x 1 chamfer, the flap's 1 and 2 mm clearances
and its 2.6 thickness, the collar flange's 4 mm depth and the F1 stop bead's section points. NOTES.md lists them as judgements.

The model holds the leaf, frame, transom, fanlight and glazing, ironmongery, threshold and step (T1), and no
wall. Metres, z up, scale 1, the pivot at the base's centre on the ground (target.json glb_pivot), the wall
face at y = 0, the street toward -y. Writes
    production/assets/cloud-week/door/door_T1.glb, door_F1.glb   (each under 1 MB)
    kit/door/build/door_T1.npz, door_F1.npz                      (named parts, for check_door.py)

How the pieces are made (all in the target's millimetres, then moved to the pivot and scaled):
  - every outline that the target gives as points is smoothed where it is a curve (short segments, small turns)
    and left sharp where it is an arris (long segments, large turns): the mouldings are not faceted;
  - the leaf's framing is ONE solid (slab minus the four panel openings and their grooves), so stile, rail and
    muntin have no internal faces; the panels float in their grooves with 0.1 mm of clearance;
  - mouldings, band, weatherboard, beads and ironmongery sit 0.3 to 0.5 mm INTO what they stand on, so no two
    visible faces are coplanar and nothing has a gap behind it; frame members that butt (jamb to head,
    transom to jamb) meet exactly on the plane across the joint, not on a visible face;
  - arrises get the bevel the target gives: the frame 1 mm and the leaf 1.5 mm (a chamfer on the sharp edges, the leaf's on its twelve
    outer edges only, so the stile-rail joints stay closed), stone 2 mm; the metal's own rounds are in its profiles (plate 2 x 1
    chamfer, collar 0.9 bevel, keep square); smooth shading by angle (35 degrees) with the arrises kept sharp; UVs by cube projection
    at real scale (1 UV unit = 1 m); materials named by what they are (paint_<colour>, glass, brass, chrome_nickel, steel_dark,
    stone_step, timber_threshold) with the target's base colour, roughness (the "new" 0.35 for paint: wear masks add the rest in the
    engine) and metal.
"""
import argparse
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "front-door", "target.json")
ASSET_DIR = os.path.join(REPO, "production", "assets", "cloud-week", "door")
NPZ_DIR = os.path.join(HERE, "build")

import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Matrix  # noqa: E402
from shapely.geometry import Polygon, box as sbox  # noqa: E402

import blender_parts  # noqa: E402
import joinery  # noqa: E402

VARIANT_KEY = {"T1": None, "F1": "flat_door_over_shop"}
DEFAULT_PAINT = {"T1": "black", "F1": "dark_green"}


# ------------------------------------------------------------------ the target
def load_target(amended=True):
    """target.json, with the try-2 departures (where the photographs win) written in unless amended=False (departures.py lists each)."""
    T = json.load(open(TARGET_JSON, encoding="utf-8"))
    if amended:
        import departures
        T, _ = departures.apply(T)
    return T


def variant_parts(T, variant):
    """The blocks of one variant: T1 is the top level, F1 its own 'parts'."""
    return T if VARIANT_KEY[variant] is None else T["variants"][VARIANT_KEY[variant]]["parts"]


# ------------------------------------------------------------------ small geometry
AX = {"x": 0, "y": 1, "z": 2}


def prism(poly, plane, axis, a, b):
    """The polygon `poly` (2D points in the world axes named by `plane`) extruded along `axis` from a to b."""
    P = np.asarray(poly, float)
    keep = [0] + [i for i in range(1, len(P)) if np.linalg.norm(P[i] - P[i - 1]) > 1e-9]
    P = P[keep]
    if len(P) > 1 and np.linalg.norm(P[0] - P[-1]) < 1e-9:
        P = P[:-1]
    n = len(P)
    ia, ib, ic = AX[plane[0]], AX[plane[1]], AX[axis]
    V = np.zeros((2 * n, 3))
    for k, t in enumerate((a, b)):
        V[k * n:(k + 1) * n, ia] = P[:, 0]
        V[k * n:(k + 1) * n, ib] = P[:, 1]
        V[k * n:(k + 1) * n, ic] = t
    F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))]
    F += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return V, F


def box(x0, y0, z0, x1, y1, z1):
    return prism([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], ("x", "y"), "z", z0, z1)


def arc(cx, cy, r, a0, a1, n=10):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def lathe(profile, nseg=40, hollow=False):
    """A solid of revolution about the local z axis. profile: (r, h) points. Solid: from the axis (r = 0) up to the axis again;
    hollow=True: a ring section whose last point joins its first (a tube or a collar)."""
    V, idx = [], []
    for r, h in profile:
        if r < 1e-9:
            V.append((0.0, 0.0, h))
            idx.append([len(V) - 1])
        else:
            ids = []
            for k in range(nseg):
                a = 2 * math.pi * k / nseg
                V.append((r * math.cos(a), r * math.sin(a), h))
                ids.append(len(V) - 1)
            idx.append(ids)
    F = []
    pairs = list(zip(range(len(profile) - 1), range(1, len(profile))))
    if hollow:
        pairs.append((len(profile) - 1, 0))
    for i, j in pairs:
        a, b = idx[i], idx[j]
        if len(a) == 1 and len(b) == 1:
            continue
        for k in range(nseg):
            k1 = (k + 1) % nseg
            if len(a) == 1:
                F.append((a[0], b[k1], b[k]))
            elif len(b) == 1:
                F.append((a[k], a[k1], b[0]))
            else:
                F.append((a[k], a[k1], b[k1], b[k]))
    if not hollow:
        if len(idx[0]) > 1:
            F.append(tuple(idx[0][::-1]))
        if len(idx[-1]) > 1:
            F.append(tuple(idx[-1]))
    return np.array(V, float), F


def place_axis_y(V, ox, oy, oz):
    """Local lathe axis z -> world -y (proud toward the street); local x, y -> world x, z."""
    V = np.asarray(V, float)
    return np.stack([ox + V[:, 0], oy - V[:, 2], oz + V[:, 1]], axis=1)


def loft_rings(rings):
    """A closed ring-shaped solid lofted through rectangles (each ring = 4 corners, same order); last joins first."""
    n = len(rings)
    V = np.vstack([np.asarray(r, float) for r in rings])
    F = []
    for i in range(n):
        j = (i + 1) % n
        for k in range(4):
            k1 = (k + 1) % 4
            F.append((4 * i + k, 4 * i + k1, 4 * j + k1, 4 * j + k))
    return V, F


def rect_ring(x0, z0, x1, z1, y):
    return [(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)]


def smooth_open(pts, l_max=9.0, turn_max=55.0, step=1.0, kmax=8):
    """Smooth an open outline where it is a curve (neighbouring segments short, turn small); keep corners sharp."""
    P = np.asarray(pts, float)
    n = len(P)
    seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
    corner = [True] * n
    for i in range(1, n - 1):
        a, b = P[i] - P[i - 1], P[i + 1] - P[i]
        turn = abs(math.degrees(math.atan2(a[0] * b[1] - a[1] * b[0], a @ b)))
        corner[i] = bool(seg[i - 1] > l_max or seg[i] > l_max or turn > turn_max)
    tang = [None] * n
    for i in range(1, n - 1):
        if not corner[i]:
            t = P[i + 1] - P[i - 1]
            tang[i] = t / np.linalg.norm(t)
    out = [tuple(P[0])]
    for i in range(n - 1):
        p0, p1, L = P[i], P[i + 1], seg[i]
        if (corner[i] and corner[i + 1]) or L < 1.0:
            out.append(tuple(p1))
            continue
        k = int(min(kmax, max(2, math.ceil(L / step))))
        m0 = tang[i] * L if tang[i] is not None else (p1 - p0)
        m1 = tang[i + 1] * L if tang[i + 1] is not None else (p1 - p0)
        for j in range(1, k + 1):
            t = j / k
            q = (2 * t ** 3 - 3 * t ** 2 + 1) * p0 + (t ** 3 - 2 * t ** 2 + t) * m0 + (-2 * t ** 3 + 3 * t ** 2) * p1 + (t ** 3 - t ** 2) * m1
            out.append(tuple(q))
        out[-1] = tuple(p1)
    return out


def clip_poly(poly, x0=-1e9, x1=1e9, y0=-1e9, y1=1e9):
    """The part of a polygon inside a box, as a list of polygons (each a list of points)."""
    g = Polygon(poly).buffer(0).intersection(sbox(x0, y0, x1, y1))
    geoms = [g] if g.geom_type == "Polygon" else [h for h in getattr(g, "geoms", []) if h.geom_type == "Polygon"]
    return [list(h.exterior.coords)[:-1] for h in geoms if h.area > 1e-6]


# ------------------------------------------------------------------ bpy objects and operations
def new_obj(name, V, F, material=None):
    return blender_parts.make_object(name, V, F, material)


def _drop(ob):
    me = ob.data
    bpy.data.objects.remove(ob, do_unlink=True)
    bpy.data.meshes.remove(me)


def _bool(ob, V, F, op):
    other = blender_parts.make_object("_cutter", V, F)
    m = ob.modifiers.new("b", "BOOLEAN")
    m.operation, m.object, m.solver = op, other, "EXACT"
    with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob]):
        bpy.ops.object.modifier_apply(modifier=m.name)
    _drop(other)
    return ob


def cut(ob, V, F):
    return _bool(ob, V, F, "DIFFERENCE")


def keep_inside(ob, V, F):
    return _bool(ob, V, F, "INTERSECT")


def unite(ob, V, F):
    return _bool(ob, V, F, "UNION")


def unite_objs(name, objs):
    """Boolean-union several objects into the first (renamed), removing the others."""
    base = objs[0]
    for o in objs[1:]:
        m = base.modifiers.new("u", "BOOLEAN")
        m.operation, m.object, m.solver = "UNION", o, "EXACT"
        with bpy.context.temp_override(object=base, active_object=base, selected_objects=[base]):
            bpy.ops.object.modifier_apply(modifier=m.name)
        _drop(o)
    base.name = name
    base.data.name = name
    return base


def bevel(ob, width, pred=None, min_angle=30.0, segments=1):
    """Chamfer (or round) the sharp edges of a mesh; pred(co0, co1) chooses which."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    sel = []
    lim = math.radians(min_angle)
    for e in bm.edges:
        if len(e.link_faces) != 2:
            continue
        if e.calc_face_angle(0.0) < lim:
            continue
        if pred is not None and not pred(e.verts[0].co, e.verts[1].co):
            continue
        sel.append(e)
    if sel:
        bmesh.ops.bevel(bm, geom=sel, offset=width, segments=segments, affect="EDGES", clamp_overlap=True)
    bm.to_mesh(ob.data)
    bm.free()


def on_planes(co0, co1, planes, tol=1e-3, need=2):
    """True when both points lie on at least `need` of the axis-aligned planes [(axis, value), ...]."""
    n = 0
    for ax, v in planes:
        if abs(co0[ax] - v) < tol and abs(co1[ax] - v) < tol:
            n += 1
    return n >= need


def box_uv(me):
    """Cube projection: each face takes the pair of axes across its dominant normal. Metres, one UV unit = 1 m."""
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.faces.ensure_lookup_table()
    layer = bm.loops.layers.uv.verify()
    for f in bm.faces:
        n = f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for l in f.loops:
            c = l.vert.co
            l[layer].uv = (c.x, c.z) if ax == 1 else ((c.y, c.z) if ax == 0 else (c.x, c.y))
    bm.to_mesh(me)
    bm.free()


# ------------------------------------------------------------------ materials
def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def make_material(name, srgb, rough, metal=0.0, transmission=0.0, ior=None):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (lin(srgb[0]), lin(srgb[1]), lin(srgb[2]), 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if transmission:
        b.inputs["Transmission Weight"].default_value = transmission
    if ior:
        b.inputs["IOR"].default_value = ior
    return m


def pick(lst, ident):
    for d in lst:
        if d["id"] == ident:
            return d
    raise SystemExit("unknown colour id %r (have %s)" % (ident, [d["id"] for d in lst]))


def setup_materials(T, variant, door_colour, frame_colour):
    """Named by what they are, with the target's base colour, roughness and metal as starting values."""
    M = T["materials"]
    dc = pick(T["door_colours"], door_colour)
    fc = pick(T["frame_colours"], frame_colour)
    mats = {
        "door": make_material("paint_" + dc["id"], dc["srgb"], M["painted_timber_door"]["roughness_new"]),
        "frame": make_material("paint_" + fc["id"], fc["srgb"], M["painted_timber_frame"]["roughness_new"]),
        "brass": make_material("brass", M["brass"]["base_srgb"], M["brass"]["roughness"], 1.0),
        "chrome_nickel": make_material("chrome_nickel", M["chrome_nickel"]["base_srgb"], M["chrome_nickel"]["roughness"], 1.0),
        "steel_dark": make_material("steel_dark", M["steel_dark"]["base_srgb"], M["steel_dark"]["roughness"], 1.0),
        "glass": make_material("glass", M["glass"]["base_srgb"], M["glass"]["roughness"], 0.0, 1.0, M["glass"]["ior"]),
    }
    if variant == "T1":
        mats["stone"] = make_material("stone_step", M["stone_step"]["base_srgb"], M["stone_step"]["roughness"])
    else:
        mats["stone"] = make_material("timber_threshold", M["timber_threshold_flat"]["base_srgb"], M["timber_threshold_flat"]["roughness"])
    return mats


# ------------------------------------------------------------------ the door
class Door:
    """One variant, built part by part in the target's millimetres."""

    def __init__(self, T, variant, door_colour, frame_colour):
        self.T, self.variant = T, variant
        self.P = P = variant_parts(T, variant)
        self.pivot = T["glb_pivot"]["terrace_four_panel" if variant == "T1" else "flat_door_over_shop"]
        self.mats = setup_materials(T, variant, door_colour, frame_colour)
        self.objs = []          # (object, material key, bevel spec) in the order built
        self.notes = {}
        L, F, O, S = P["leaf"], P["frame"], P["opening"], P["step"]
        self.L, self.F, self.O, self.S = L, F, O, S
        self.OW = O["width_mm"]
        self.X0, self.Z0, self.W, self.H, self.TH = L["x0_mm"], L["z0_mm"], L["width_mm"], L["height_mm"], L["thickness_mm"]
        self.LY0 = L["outside_face_y_mm"]
        self.LY1 = self.LY0 + self.TH
        self.PT = P["panels"]["thickness_mm"]
        self.GR, self.PLAY = P["panels"]["groove_depth_mm"], P["panels"]["side_play_mm"]
        self.PY0 = self.LY0 + (self.TH - self.PT) / 2
        self.PY1 = self.PY0 + self.PT
        self.SHOW, self.JF = F["jamb_showing_past_brick_mm"], F["jamb_face_mm"]
        self.REB_W = F["rebate_width_mm"]
        self.FY0, self.FY1 = F["frame_outside_face_y_mm"], F["frame_inside_face_y_mm"]
        self.STOP_Y = self.FY0 + F["stop_depth_mm"]
        tr, gl, hd = F["transom"], F["glazing"], F["head_section_mm"]
        self.tr, self.gl, self.hd = tr, gl, hd
        self.Z_STOP, self.Z_TR_TOP, self.Z_REB = tr["z_stop_underside"], tr["z_top"], tr["rebate_underside_z"]
        self.GX0, self.GX1 = gl["opening_x_mm"]
        self.GZ0, self.GZ1 = gl["opening_z_mm"]
        self.GLASS_Y, self.GLASS_T, self.GLASS_RB = gl["glass_y_mm"], gl["glass_thickness_mm"], gl["glass_rebate_mm"]
        self.HEAD_Z0 = hd["z0"]
        self.JL, self.JR = F["jamb_x_mm"]["left"], F["jamb_x_mm"]["right"]
        rise = O["camber_rise_mm"]
        half = self.OW / 2
        if rise > 0:
            self.R = (half ** 2 + rise ** 2) / (2 * rise)
            self.CZ = O["crown_height_mm"] - self.R
        else:
            self.R = None
            self.CROWN = O["crown_height_mm"]
        self.CROWN = O["crown_height_mm"]

    # -- helpers
    def soffit_z(self, x):
        if not self.R:
            return self.CROWN
        return self.CZ + math.sqrt(self.R ** 2 - (x - self.OW / 2) ** 2)

    def add(self, name, V, F, mat, bev=None, prep=None):
        """Create the object now (so booleans can follow); `bev` = (width_mm, pred, segments) applied at the end."""
        ob = new_obj(name, V, F)
        self.objs.append({"ob": ob, "mat": mat, "bev": bev})
        return ob

    def get(self, name):
        for d in self.objs:
            if d["ob"].name == name:
                return d["ob"]
        raise KeyError(name)

    # -- the frame
    def build_frame(self):
        T, F = self.T, self.F
        x_lo, x_hi = self.JL[0], self.JR[1]
        z_foot = -0.5          # the jambs stand 0.5 mm into the threshold (no coplanar contact; no bevel on their feet)
        bead_stop = bool(F.get("stop_inner_bead"))
        slot_y0, slot_y1 = self.GLASS_Y - 2.0, self.GLASS_Y + 2.0
        for side, (xb, xs, sgn) in (("L", (self.JL[0], self.JL[1], 1)), ("R", (self.JR[1], self.JR[0], -1))):
            xr = xs - sgn * self.REB_W
            plan = [(xb, self.FY0), (xs, self.FY0), (xs, self.STOP_Y), (xr, self.STOP_Y), (xr, self.FY1), (xb, self.FY1)]
            V, Fc = prism(plan, ("x", "y"), "z", z_foot, self.GZ1)
            ob = self.add("frame_jamb_" + side, V, Fc, "frame")
            # the glass is held in a slot in the jamb as well as in the head and the transom
            xa, xbn = (xs - self.GLASS_RB - 0.4, xs + 0.2) if sgn == 1 else (xs - 0.2, xs + self.GLASS_RB + 0.4)
            Vc, Fcut = box(xa, slot_y0, self.Z_TR_TOP - self.GLASS_RB, xbn, slot_y1, self.GZ1 + 0.2)
            cut(ob, Vc, Fcut)

            def pred(a, b, xs=xs, bead_stop=bead_stop):
                if a.z < 0.6 and b.z < 0.6:
                    return False        # the foot stays square, bedded 0.5 into the threshold
                if 0.5 * (a.y + b.y) > slot_y0 - 0.5 and 0.5 * (a.y + b.y) < slot_y1 + 0.5 and abs(a.y - b.y) < 0.1:
                    return False        # inside the glass slot
                if bead_stop and abs(a.x - xs) < 1e-3 and abs(b.x - xs) < 1e-3 and abs(a.y - self.FY0) < 1e-3 and abs(b.y - self.FY0) < 1e-3:
                    return False        # the quarter-round bead stands on this edge
                return True
            self.objs[-1]["bev"] = (F.get("arris_ease_mm", 1.0), pred, 1)
        if bead_stop:
            for side, sgn, xs in (("L", -1, self.JL[1]), ("R", 1, self.JR[0])):
                w, pr = 5.0, 2.5
                poly = [(xs, self.FY0), (xs + sgn * w, self.FY0), (xs + sgn * w, self.FY0 - 0.6), (xs + sgn * 0.82 * w, self.FY0 - 1.7),
                        (xs + sgn * 0.45 * w, self.FY0 - 2.4), (xs, self.FY0 - pr)]
                V, Fc = prism(poly, ("x", "y"), "z", 0.0, self.Z_STOP)
                self.add("frame_stop_bead_" + side, V, Fc, "frame")
        # the head: cut to the soffit's circle on top (crown and ends, G8), grooved for the glass underneath
        n = 49
        xs_ = [x_lo + (x_hi - x_lo) * i / (n - 1) for i in range(n)]
        outline = [(x_lo, self.HEAD_Z0), (x_hi, self.HEAD_Z0)] + [(x, self.soffit_z(x)) for x in xs_[::-1]]
        V, Fc = prism(outline, ("x", "z"), "y", self.FY0, self.FY1)
        ob = self.add("frame_head", V, Fc, "frame")
        Vc, Fcut = box(self.GX0 - self.GLASS_RB - 0.4, slot_y0, self.HEAD_Z0 - 0.2, self.GX1 + self.GLASS_RB + 0.4, slot_y1, self.HEAD_Z0 + self.GLASS_RB)
        cut(ob, Vc, Fcut)

        def pred_h(a, b):
            ym = 0.5 * (a.y + b.y)
            return not (slot_y0 - 0.5 < ym < slot_y1 + 0.5 and abs(a.y - b.y) < 0.1)
        self.objs[-1]["bev"] = (F.get("arris_ease_mm", 1.0), pred_h, 1)
        self.build_transom()
        self.build_glazing()

    def transom_profile(self):
        """The transom's vertical outline in (y, z), absolute: the stop's underside, the moulded front, the slope, the glass slot, the rebate."""
        P, tr = self.P, self.tr
        fp = [(y, z) for y, z in tr["front_profile_yz_mm"]]       # (0,0) first: the jamb face plane at the stop underside
        front = smooth_open([(self.FY0 + y, self.Z_STOP + z) for y, z in fp[1:]])
        ga, gb = self.GLASS_Y - 2.0, self.GLASS_Y + 2.0
        pts = [(self.STOP_Y, self.Z_STOP)] + front
        pts += [(ga, self.Z_TR_TOP), (ga, self.Z_TR_TOP - self.GLASS_RB), (gb, self.Z_TR_TOP - self.GLASS_RB), (gb, self.Z_TR_TOP),
                (self.FY1, self.Z_TR_TOP), (self.FY1, self.Z_REB), (self.STOP_Y, self.Z_REB)]
        return pts

    def build_transom(self):
        tr = self.tr
        prof = self.transom_profile()
        xl_stop, xr_stop = self.JL[1], self.JR[0]
        ov = tr["overlap_on_jamb_faces_mm"]
        sp = tr["end_splay"]
        zf, zt = self.Z_STOP + sp["from_stop_edge_z_mm"], self.Z_STOP + sp["to_z_mm"]
        # three slabs of the one outline: the moulded front (past the jamb faces), the part between the stops, the rebate part
        # (the outline's points are (y, z): clip_poly's first axis is y)
        front = clip_poly(prof, x1=self.FY0)
        mid = clip_poly(prof, x0=self.FY0, x1=self.STOP_Y)
        back = clip_poly(prof, x0=self.STOP_Y)
        parts = []
        for k, poly in enumerate(front):
            V, Fc = prism(poly, ("y", "z"), "x", xl_stop - ov, xr_stop + ov)
            o = new_obj("_tr_front%d" % k, V, Fc)
            # the nose's ends are cut back on a 45 degree splay (in elevation) from the stop edge at the nose's underside
            keep = [(xl_stop, self.Z_STOP - 5), (xl_stop, zf), (xl_stop - ov, zt), (xl_stop - ov, self.Z_STOP + 400),
                    (xr_stop + ov, self.Z_STOP + 400), (xr_stop + ov, zt), (xr_stop, zf), (xr_stop, self.Z_STOP - 5)]
            Vk, Fk = prism(keep, ("x", "z"), "y", self.FY0 - 80, self.FY0 + 5)
            keep_inside(o, Vk, Fk)
            parts.append(o)
        for k, poly in enumerate(mid):
            V, Fc = prism(poly, ("y", "z"), "x", xl_stop, xr_stop)
            parts.append(new_obj("_tr_mid%d" % k, V, Fc))
        for k, poly in enumerate(back):
            V, Fc = prism(poly, ("y", "z"), "x", xl_stop - self.REB_W, xr_stop + self.REB_W)
            parts.append(new_obj("_tr_back%d" % k, V, Fc))
        ob = unite_objs("frame_transom", parts)
        self.objs.append({"ob": ob, "mat": "frame", "bev": (self.F.get("arris_ease_mm", 1.0), lambda a, b: max(a.y, b.y) < self.FY0 + 12, 1)})

    def build_glazing(self):
        gl = self.gl
        # the pane, 3 mm, in the slots of head, transom and jambs (0.3 to 0.5 mm of clearance at every edge)
        gx0, gx1 = self.GX0 - self.GLASS_RB + 0.4, self.GX1 + self.GLASS_RB - 0.4
        gz0, gz1 = self.Z_TR_TOP - self.GLASS_RB + 0.3, self.GZ1 + self.GLASS_RB - 0.3
        V, Fc = box(gx0, self.GLASS_Y - self.GLASS_T / 2, gz0, gx1, self.GLASS_Y + self.GLASS_T / 2, gz1)
        self.add("glass_fanlight", V, Fc, "glass")
        # the bead (T1) or the putty fillet (F1): one mitred sweep round the opening. Profile (a, p): a along the face
        # from the opening's edge inward, p proud of the glass front. It stands 0.3 into the glass and 0.4 into the frame.
        prof = [tuple(q) for q in gl["bead_profile_ap_mm"]]
        gf = self.GLASS_Y - self.GLASS_T / 2
        (a1, p1), (a2, p2) = prof[1], prof[2]
        foot_x = a1 + (a2 - a1) * ((-0.3 - p1) / (p2 - p1)) if p2 != p1 else a1
        front = smooth_open(prof[1:]) if len(prof) > 3 else prof[1:]
        poly = [(-0.4, -0.3), (foot_x, -0.3)] + front + [(-0.4, prof[-1][1])]
        dt = [(d, gf - p) for d, p in poly]
        V, Fc = joinery.sweep_frame(dt, self.GX0, self.GZ0, self.GX1, self.GZ1, 0.0)
        self.add("frame_glazing_bead", V, Fc, "frame")

    # -- the leaf
    def build_leaf(self):
        P, X0, Z0, W, H = self.P, self.X0, self.Z0, self.W, self.H
        LY0, LY1, PY0, PY1, GR = self.LY0, self.LY1, self.PY0, self.PY1, self.GR
        V, Fc = box(X0, LY0, Z0, X0 + W, LY1, Z0 + H)
        ob = self.add("leaf_frame", V, Fc, "door")
        self.open = {}
        for k, o in P["panels"]["openings_leaf_uv_mm"].items():
            x0, x1, z0, z1 = X0 + o["u0"], X0 + o["u1"], Z0 + o["v0"], Z0 + o["v1"]
            self.open[k] = (x0, z0, x1, z1)
            cut(ob, *box(x0, LY0 - 1, z0, x1, LY1 + 1, z1))                                   # the opening
            cut(ob, *box(x0 - GR, PY0 - 0.1, z0 - GR, x1 + GR, PY1 + 0.1, z1 + GR))          # the groove all round it, 0.1 loose
        ir = self.P["ironmongery"]
        lp = ir["letter_plate"]
        if lp.get("present"):                                  # the slot through the muntin behind the plate
            xc, zc = X0 + lp["centre_u_mm"], Z0 + lp["centre_above_leaf_bottom_mm"]
            ztop_ap = zc + lp["outer_h_mm"] / 2 - lp["aperture_top_margin_mm"]
            zbot_ap = ztop_ap - lp["aperture_h_mm"]
            hw = lp["aperture_w_mm"] / 2 + 0.5
            cut(ob, *box(xc - hw, LY0 - 1, zbot_ap - 0.5, xc + hw, LY1 + 1, ztop_ap + 0.5))
        cl = ir.get("cylinder_lock", {})
        if cl.get("present"):                                  # the bore for the cylinder (1 mm of relief round the collar)
            cx, cz = X0 + cl["centre_u_mm"], Z0 + cl["centre_above_leaf_bottom_mm"]
            circ = arc(cx, cz, cl["outer_diameter_mm"] / 2 + 1.0, 0, 360, 48)[:-1]
            cut(ob, *prism(circ, ("x", "z"), "y", LY0 - 1, LY0 + 30.0))
        kn = ir.get("knob", {})
        if kn.get("present"):                                  # the rose is let into the rail: a round recess, 3 mm
            kx, kz = X0 + kn["centre_u_mm"], Z0 + kn["centre_above_leaf_bottom_mm"]
            circ = arc(kx, kz, kn["rose_diameter_mm"] / 2 + 0.5, 0, 360, 64)[:-1]
            cut(ob, *prism(circ, ("x", "z"), "y", LY0 - 1, LY0 + 3.0))
        kh = ir.get("old_keyhole", {})
        if kh.get("present"):                                  # the plugged mortice keyhole: a round head over a parallel slot, a recess 2 mm deep
            cut(ob, *prism(self.keyhole_outline(X0 + kh["centre_u_mm"], Z0 + kh["centre_above_leaf_bottom_mm"], kh["head_diameter_mm"], kh["slot_w_mm"], kh["h_mm"]),
                           ("x", "z"), "y", LY0 - 1, LY0 + 2.0))
        self.cut_joints(ob)
        planes = [(0, X0), (0, X0 + W), (1, LY0), (1, LY1), (2, Z0), (2, Z0 + H)]
        self.objs[-1]["bev"] = (self.L["arris_ease_mm"], lambda a, b: on_planes(a, b, planes), 1)
        # the panels, floating in their grooves (1.6 mm side play, 0.1 mm everywhere else)
        for k, (x0, z0, x1, z1) in self.open.items():
            V, Fc = box(x0 - GR + self.PLAY / 2, PY0, z0 - GR + 0.1, x1 + GR - self.PLAY / 2, PY1, z1 + GR - 0.1)
            self.add("panel_" + k, V, Fc, "door")
        self.build_mouldings()

    @staticmethod
    def keyhole_outline(cx, cz, head_d, slot_w, h):
        """A keyhole, overall h high, its top at cz + h/2: a round head of diameter head_d over a parallel slot slot_w wide with a round foot."""
        from shapely.geometry import LineString, Point
        r = head_d / 2
        top = cz + h / 2 - r
        foot = cz - h / 2 + slot_w / 2
        g = Point(cx, top).buffer(r, 20).union(LineString([(cx, top), (cx, foot)]).buffer(slot_w / 2, 10))
        pts = list(g.exterior.coords)[:-1]
        return [(float(x), float(z)) for x, z in pts]

    def cut_joints(self, ob):
        """The joint lines where the rails meet the stiles and the muntin meets the rails: grooves, 0.8 wide and 0.8 deep, in the framing's face.
        They stop 5 mm short of each panel opening (the moulding's lap hides that) and 3 mm short of the leaf's outer edge (the arris is eased)."""
        jg = self.L.get("joint_groove_mm")
        if not jg:
            return
        w, dpt = jg["width"], jg["depth"]
        o = self.P["panels"]["openings_leaf_uv_mm"]
        X0, Z0, LY0 = self.X0, self.Z0, self.LY0
        gap = self.P["mouldings"]["outside_bolection"]["lap_over_framing_mm"] + 0.2
        edge = 3.0
        bl, tl = o["bottom_left"], o["top_left"]
        br = o["bottom_right"]
        rails = [(edge, bl["v0"] - gap), (bl["v1"] + gap, tl["v0"] - gap), (tl["v1"] + gap, self.H - edge)]     # (v from, v to) of the bottom, lock and top rails
        for u in (bl["u0"], br["u1"]):                                                          # the stiles' inner edges
            for v0, v1 in rails:
                cut(ob, *box(X0 + u - w / 2, LY0 - 1.0, Z0 + v0, X0 + u + w / 2, LY0 + dpt, Z0 + v1))
        u0, u1 = bl["u1"] + gap, o["bottom_right"]["u0"] - gap                                  # across the muntin
        for v in (bl["v0"], bl["v1"], tl["v0"], tl["v1"]):
            cut(ob, *box(X0 + u0, LY0 - 1.0, Z0 + v - w / 2, X0 + u1, LY0 + dpt, Z0 + v + w / 2))

    def build_mouldings(self):
        P = self.P
        X0, Z0, LY0, LY1, PY1 = self.X0, self.Z0, self.LY0, self.LY1, self.PY1
        bol = P["mouldings"]["outside_bolection"]
        lap, bw, below = bol["lap_over_framing_mm"], bol["width_on_face_mm"], bol["panel_face_below_framing_mm"]
        dh = [tuple(q) for q in bol["profile_dh_mm"]]
        # the outside bolection: (d from the outer edge, h proud of the framing). The first point sits 0.5 mm into the framing,
        # the underside 0.5 mm into the framing and the panel, so nothing is coplanar and nothing has a gap behind it.
        open_line = smooth_open([(0.0, -0.5)] + dh[1:])
        poly = open_line + [(bw, -below - 0.5), (lap - 0.5, -below - 0.5), (lap - 0.5, -0.5)]
        dt = [(d, LY0 - h) for d, h in poly]
        sgl_w = P["mouldings"]["inside_single"]["width_on_face_mm"]
        single = [(0.0, LY1), (4.0, LY1), (10.0, LY1 - 6.0), (16.0, PY1 + 4.0), (sgl_w, PY1), (0.0, PY1)]
        for k, (x0, z0, x1, z1) in self.open.items():
            V, Fc = joinery.sweep_frame(dt, x0 - lap, z0 - lap, x1 + lap, z1 + lap, 0.0)
            self.add("moulding_bolection_" + k, V, Fc, "door")
            V, Fc = joinery.sweep_frame(single, x0, z0, x1, z1, 0.0)
            self.add("moulding_single_" + k, V, Fc, "door")
        for key in ("lock_rail_band", "weatherboard"):
            blk = P["mouldings"][key]
            if not blk.get("present"):
                continue
            za, zb = blk["z_above_leaf_bottom_mm"]
            x0, x1 = blk["x_mm"]
            zp = [tuple(q) for q in blk["profile_zp_mm"]]
            line = smooth_open([(zp[0][0], -0.5)] + zp[1:-1] + [(zp[-1][0], -0.5)])
            outline = [(LY0 - p, Z0 + za + z) for z, p in line]
            V, Fc = prism(outline, ("y", "z"), "x", x0, x1)
            self.add("moulding_" + ("band" if key == "lock_rail_band" else "weatherboard"), V, Fc, "door")

    # -- ironmongery
    def build_ironmongery(self):
        ir = self.P["ironmongery"]
        X0, Z0, LY0 = self.X0, self.Z0, self.LY0
        t1 = self.variant == "T1"
        plate_mat = "brass" if t1 else "chrome_nickel"
        lp = ir["letter_plate"]
        if lp.get("present"):
            self.build_letter_plate(lp, plate_mat)
        cl = ir.get("cylinder_lock", {})
        if cl.get("present"):
            self.build_cylinder(cl, "brass" if t1 else "chrome_nickel")
        kp = ir.get("keep", {})
        if kp.get("present"):
            self.build_bell_push(kp)
        kn = ir.get("knob", {})
        if kn.get("present"):
            self.build_knob(kn)
        kh = ir.get("old_keyhole", {})
        if kh.get("present"):
            # the plugged mortice keyhole: the recess is cut in the leaf (2 mm); a dark iron blank fills it, 1.1 mm below the face, and a pale
            # metal blank fills the slot (0.4 mm of it let into the dark one)
            from shapely.geometry import LineString, Polygon as SPoly
            cx, cz = X0 + kh["centre_u_mm"], Z0 + kh["centre_above_leaf_bottom_mm"]
            hd, sw, hh = kh["head_diameter_mm"], kh["slot_w_mm"], kh["h_mm"]
            outline = SPoly(self.keyhole_outline(cx, cz, hd, sw, hh)).buffer(-0.5, join_style=1)
            V, Fc = prism(list(outline.exterior.coords)[:-1], ("x", "z"), "y", LY0 + 1.1, LY0 + 2.4)
            self.add("iron_keyhole_plate", V, Fc, "steel_dark")
            top = cz + hh / 2 - hd / 2
            foot = cz - hh / 2 + sw / 2
            blank = LineString([(cx, top - hd / 2 + 1.5), (cx, foot)]).buffer((sw - 1.8) / 2, 10, cap_style=1)
            V, Fc = prism(list(blank.exterior.coords)[:-1], ("x", "z"), "y", LY0 + 0.4, LY0 + 1.5)
            self.add("iron_keyhole_blank", V, Fc, plate_mat)

    def build_bell_push(self, kp):
        """T1's fitting on the right jamb's stop (P1's dark oblong, 22 x 72.6): a period bell push, a dark oblong back with a round brass bezel and a
        round dark button on it. Stands 0.4 into the stop's face."""
        xk = kp["centre_x_mm"]
        z0k, z1k = kp["z_range_mm"]
        zm = 0.5 * (z0k + z1k)
        w, h, r = kp["w_mm"], z1k - z0k, 6.0
        pts = []
        for (cx_, cz_, a0) in ((xk + w / 2 - r, z1k - r, 0), (xk - w / 2 + r, z1k - r, 90), (xk - w / 2 + r, z0k + r, 180), (xk + w / 2 - r, z0k + r, 270)):
            pts += arc(cx_, cz_, r, a0, a0 + 90, 6)
        V, Fc = prism(pts, ("x", "z"), "y", self.FY0 - 3.0, self.FY0 + 0.4)
        self.add("iron_bellpush", V, Fc, "steel_dark")
        # the bezel (a ring, 17 across, rounded, 4.9 proud of the stop face) and the button (a dome of 11 across, 5.8 proud); both start 0.4 into the back
        Vb, Fb = lathe([(8.5, 2.6), (8.5, 4.1), (7.7, 4.9), (6.7, 4.9), (6.0, 4.1), (6.0, 2.6)], 40, hollow=True)
        self.add("iron_bellpush_bezel", place_axis_y(Vb, xk, self.FY0, zm), Fb, "brass")
        Vd, Fd = lathe([(0.0, 2.6), (5.6, 2.6), (5.6, 3.8), (4.4, 5.0), (2.2, 5.6), (0.0, 5.8)], 40)
        self.add("iron_bellpush_button", place_axis_y(Vd, xk, self.FY0, zm), Fd, "steel_dark")

    def build_letter_plate(self, lp, mat):
        X0, Z0, LY0 = self.X0, self.Z0, self.LY0
        xc, zc = X0 + lp["centre_u_mm"], Z0 + lp["centre_above_leaf_bottom_mm"]
        w, h, aw, ah = lp["outer_w_mm"], lp["outer_h_mm"], lp["aperture_w_mm"], lp["aperture_h_mm"]
        bt, rp = lp["backplate_thickness_mm"], lp["rim_proud_mm"]
        ch = lp.get("rim_chamfer_mm", rp - bt)                 # the rim's outer edge: 45 degrees from the rim's height down to the backplate's edge
        ztop, zbot = zc + h / 2, zc - h / 2
        ztop_ap = ztop - lp["aperture_top_margin_mm"]
        zbot_ap = ztop_ap - ah
        yb = LY0 + 0.4                       # the plate's back stands 0.4 into the leaf
        rings = [rect_ring(xc - w / 2, zbot, xc + w / 2, ztop, yb),
                 rect_ring(xc - w / 2, zbot, xc + w / 2, ztop, LY0 - bt),                              # the edge, 3 proud
                 rect_ring(xc - w / 2 + ch, zbot + ch, xc + w / 2 - ch, ztop - ch, LY0 - bt - ch),     # the 45 degree chamfer, 3 x 3, up to the rim's flat
                 rect_ring(xc - aw / 2, zbot_ap, xc + aw / 2, ztop_ap, LY0 - rp),                       # the rim's flat, 6 proud, to the aperture
                 rect_ring(xc - aw / 2, zbot_ap, xc + aw / 2, ztop_ap, yb)]
        V, Fc = loft_rings(rings)
        self.add("iron_letter_plate", V, Fc, mat)
        # the sprung flap, hinged along its top (2 mm shadow gap), dished 3 mm inward, 1 mm clear at the sides and foot; the dish is
        # centred on the drawing's flat flap (front at LY0 - 2): 1.5 mm proud at its edges, 1.5 mm behind it at its middle
        fw = aw / 2 - 1.0
        xs_ = [xc - fw + 2 * fw * i / 12 for i in range(13)]
        front = [(x, LY0 - 3.5 + 3.0 * (1 - ((x - xc) / fw) ** 2)) for x in xs_]
        back = [(x, y + 2.6) for x, y in front[::-1]]
        V, Fc = prism(front + back, ("x", "y"), "z", zbot_ap + 1.0, ztop_ap - 2.0)
        self.add("iron_letter_flap", V, Fc, mat)
        # the lifting lip: the flap's foot, 4 mm high, standing 1.8 mm proud of the flap (a hair narrower, lower and deeper, so no face is shared)
        sel = [i for i, (x, y) in enumerate(front) if abs(x - xc) <= fw - 0.3]
        front2 = [(front[i][0], front[i][1] - 1.8) for i in sel]
        back2 = [(back[len(back) - 1 - i][0], back[len(back) - 1 - i][1] + 0.3) for i in sel[::-1]]
        V, Fc = prism(front2 + back2, ("x", "y"), "z", zbot_ap + 0.6, zbot_ap + 5.0)
        self.add("iron_letter_lip", V, Fc, mat)
        pb = lp.get("pivot_bosses")
        if pb:                                # F1: no corner screws; the two round bosses at the flap's hinge ends are its pivots (P2)
            r_b, up = pb["diameter_mm"] / 2, pb["proud_of_rim_mm"]
            for sx, tag in ((-1, "l"), (1, "r")):
                cx_, cz_ = xc + sx * pb["x_from_centre_mm"], ztop_ap - 4.5
                Vh, Fh = lathe([(0.0, -1.0), (r_b, -1.0), (r_b, up - 1.6), (r_b - 1.0, up - 0.6), (r_b - 2.2, up - 0.1), (0.0, up)], 24)
                o = new_obj("iron_plate_pivot_" + tag, place_axis_y(Vh, cx_, LY0 - rp, cz_), Fh)
                self.objs.append({"ob": o, "mat": mat, "bev": None})

    def build_cylinder(self, cl, mat):
        """The cylinder lock: a collar flange 4 deep let into a bore, standing proud with a rounded edge, the plug behind it 28 (T1) or 18 (F1) across;
        a vertical keyway 3 x 9 in the plug. T1 is one solid of revolution; F1's collar is a ring of 8 rounded scallops round its own plug."""
        X0, Z0, LY0 = self.X0, self.Z0, self.LY0
        cx, cz = X0 + cl["centre_u_mm"], Z0 + cl["centre_above_leaf_bottom_mm"]
        ro, rpl, proud = cl["outer_diameter_mm"] / 2, cl["plug_diameter_mm"] / 2, cl["collar_proud_mm"]
        depth = 30.3                                  # 0.3 into the bore's floor
        if self.variant == "T1":
            # one solid of revolution (r, s: s proud of the leaf face): the collar's front a flat annulus with a 3 mm round on its outer edge and a small
            # round on its inner, the plug's face 0.6 behind the collar's, a dark gap ring 0.3 wide and 2.5 deep between plug and collar
            rr = 3.0
            outer = [(ro - rr + rr * math.cos(math.radians(a)), proud - rr + rr * math.sin(math.radians(a))) for a in (90, 75, 60, 45, 30, 15, 0)]
            prof = [(0.0, proud - 0.6), (rpl - 0.4, proud - 0.6), (rpl, proud - 1.0), (rpl, -2.5), (rpl + 0.3, -2.5), (rpl + 0.3, proud - 1.0),
                    (rpl + 0.7, proud - 0.3), (rpl + 1.3, proud)] + outer + [(ro, -4.0), (rpl, -4.0), (rpl, -depth), (0.0, -depth)]
            V, Fc = lathe(prof, 56)
            V = place_axis_y(V, cx, LY0, cz)
            o = self.add("iron_lock", V, Fc, mat)
        else:
            # a collar of rounded scallops round a plug whose face stands 1 mm behind it (the collar's inner edge is 0.3 into the plug); the collar's
            # front edge is rounded (1.2 mm, two steps)
            n = int(cl.get("scallops", 8))
            lobe_r, lobe_c = 7.0, ro - 7.0
            per = 14
            outer = []
            for i in range(n):
                for k in range(per):
                    a = 2 * math.pi * (i + k / per) / n - math.pi / n          # from one cusp round the lobe to the next
                    # the lobe i is a circle of radius lobe_r centred at lobe_c in direction a_i = 2 pi i / n; the rim's radius there
                    best = 0.0
                    for j in (i - 1, i, i + 1):
                        aj = 2 * math.pi * j / n
                        dl = a - aj
                        v = lobe_c * math.cos(dl) + math.sqrt(max(lobe_r ** 2 - (lobe_c * math.sin(dl)) ** 2, 0.0))
                        best = max(best, v)
                    outer.append((cx + best * math.cos(a), cz + best * math.sin(a)))
            Nn = len(outer)
            inner = [(cx + (rpl - 0.3) * math.cos(2 * math.pi * k / Nn), cz + (rpl - 0.3) * math.sin(2 * math.pi * k / Nn)) for k in range(Nn)]
            V, Fc = self.ring_prism(outer, inner, LY0 - proud, LY0 + 4.0)
            o0 = self.add("iron_lock_collar", V, Fc, mat)
            ytop = LY0 - proud
            self.objs[-1]["bev"] = (1.2, lambda a, b: abs(a.y - ytop) < 1e-3 and abs(b.y - ytop) < 1e-3, 2)
            V, Fc = lathe([(0.0, -depth), (rpl, -depth), (rpl, proud - 1.0 - 0.4), (rpl - 0.4, proud - 1.0), (0.0, proud - 1.0)], 48)
            o = self.add("iron_lock_plug", place_axis_y(V, cx, LY0, cz), Fc, mat)
        kw, kh = cl.get("keyway_w_mm", 3.0), cl.get("keyway_h_mm", 9.0)                 # the keyway: a vertical slot, cut from in front of the plug's face
        cut(o, *box(cx - kw / 2, LY0 - proud - 1.0, cz - kh / 2, cx + kw / 2, LY0 + 2.0, cz + kh / 2))

    @staticmethod
    def ring_prism(outer, inner, a, b):
        """A ring-shaped prism along y between y = a and y = b; outer and inner outlines (x, z) have the same number of points."""
        N = len(outer)
        assert N == len(inner)
        V = []
        for y in (a, b):
            V += [(x, y, z) for x, z in outer] + [(x, y, z) for x, z in inner]
        V = np.array(V, float)
        oa, ia, ob, ib = 0, N, 2 * N, 3 * N
        F = []
        for i in range(N):
            j = (i + 1) % N
            F += [(oa + i, oa + j, ob + j, ob + i), (ia + i, ib + i, ib + j, ia + j), (oa + i, ia + i, ia + j, oa + j), (ob + i, ob + j, ib + j, ib + i)]
        return V, F

    def build_knob(self, kn):
        X0, Z0, LY0 = self.X0, self.Z0, self.LY0
        kx, kz = X0 + kn["centre_u_mm"], Z0 + kn["centre_above_leaf_bottom_mm"]
        rz = [tuple(q) for q in kn["profile_rz_mm"]]
        # the bulb up to z 58 (the brass cap takes the last 4), its foot 3.5 mm down into the rose's recess
        bulb = smooth_open([rz[1]] + [q for q in rz[2:] if q[1] < 58.0] + [(8.0, 58.0), (0.0, 58.0)], l_max=20.0, turn_max=70.0, step=1.6)
        prof0 = [(0.0, -3.5), (rz[1][0], -3.5)] + bulb
        def r_at(zq):
            for (ra, za), (rb, zb) in zip(prof0, prof0[1:]):
                if za < zb and za <= zq <= zb:
                    return ra + (rb - ra) * (zq - za) / (zb - za)
            return prof0[-1][0]
        rings, hw, depth = (10.0, 19.0, 28.0, 37.0, 46.0), 1.3, 1.5          # five turned rings, V-cut 1.5 deep
        prof, pending = [], list(rings)
        for r, z in prof0:
            while pending and z >= pending[0] - hw and z > 5.0:
                zg = pending.pop(0)
                prof += [(r_at(zg - hw), zg - hw), (r_at(zg) - depth, zg), (r_at(zg + hw), zg + hw)]
            if any(abs(z - zg) < hw for zg in rings):
                continue
            prof.append((r, z))
        V, Fc = lathe(prof, 44)
        self.add("iron_knob", place_axis_y(V, kx, LY0, kz), Fc, "steel_dark")
        V, Fc = lathe([(0.0, 57.9), (8.1, 57.9), (7.2, 59.4), (4.2, 61.2), (0.0, 62.0)], 40)
        self.add("iron_knob_cap", place_axis_y(V, kx, LY0, kz), Fc, "brass")
        rr = kn["rose_diameter_mm"] / 2          # the dished rose ring, let 3 mm into the rail
        V, Fc = lathe([(31.0, -2.6), (rr, -2.6), (rr, 0.3), (rr - 1.0, 0.5), (31.0, -1.2)], 48, hollow=True)
        self.add("iron_knob_rose", place_axis_y(V, kx, LY0, kz), Fc, "steel_dark")

    # -- threshold, riser, tread (T1) or the sill (F1)
    def build_step(self):
        S = self.S
        t = S["threshold"]
        zt1, thick, r = t["top_z"], t["thickness_mm"], t["nose_radius_mm"]
        fy, by = t["front_y_mm"], t["back_y_mm"]
        if self.variant == "T1":
            b = t["bearing_into_wall_each_side_mm"]
            x_lo, x_hi = -b, self.OW + b
        else:
            x_lo, x_hi = self.JL[0], self.JR[1]       # the sill runs under the whole frame (the jambs stand on it)
        prof = [(fy, zt1 - thick), (fy, zt1 - r)] + arc(fy + r, zt1 - r, r, 180, 90, 12)[1:] + [(by, zt1), (by, zt1 - thick)]
        V, Fc = prism(prof, ("y", "z"), "x", x_lo, x_hi)
        self.add("stone_threshold", V, Fc, "stone")
        self.objs[-1]["bev"] = (2.0, None, 1) if self.variant == "T1" else (1.5, None, 1)
        if self.variant != "T1":
            return
        # the recessed riser: its top and foot 0.5 mm into the threshold and the tread
        rz0, rz1 = S["riser"]["z_mm"]
        V, Fc = box(0.5, S["riser"]["face_y_mm"], rz0 - 0.5, self.OW - 0.5, by - 1.0, rz1 + 0.5)
        self.add("stone_riser", V, Fc, "stone")
        self.objs[-1]["bev"] = (2.0, lambda a, b_: a.y < S["riser"]["face_y_mm"] + 0.1 and b_.y < S["riser"]["face_y_mm"] + 0.1 and min(a.z, b_.z) > rz0 + 0.6 and max(a.z, b_.z) < rz1 - 0.6 or False, 1)
        # the tread: a loft of horizontal rings, each the plan outline drawn in by the nose's section at that height, so the half-round nose and its
        # undercut run along the front AND round both ends (P1 x 87-95 and 283-291), the plan corners being the same section swept round
        td = S["tread"]
        nr = td["nosing_radius_mm"]
        ztop_f = td["top_z_mm"] - td["fall_to_front_mm"]
        yf = td["front_y_mm"]
        zc = ztop_f - nr
        cos_t = (td["undercut_mm"] - nr) / nr
        th_end = 360.0 - math.degrees(math.acos(cos_t))
        x0, x1 = td["x_mm"]
        rc = td["plan_corner_radius_mm"]
        yp = -self.P["brick"]["plinth"]["front_proud_of_wall_face_mm"]
        ground = td["ground_z_mm"]
        # the section: (inset d from the plan outline, z) from the top tangent round the nose to where the base face begins, then down to the ground
        sec = [(nr * (1.0 + math.cos(math.radians(a))), zc + nr * math.sin(math.radians(a))) for a in np.linspace(90.0, th_end, 22)]
        sec.append((td["undercut_mm"], ground))
        kc = 10
        y_r = S["riser"]["face_y_mm"]

        def ring(d, z):
            pts = [(x0 + d, yp), (0.0, yp), (0.0, y_r), (0.0, by + 1.0), (self.OW, by + 1.0), (self.OW, y_r), (self.OW, yp), (x1 - d, yp), (x1 - d, yf + rc)]
            r = rc - d
            pts += [(x1 - rc + r * math.cos(math.radians(-90.0 * k / kc)), yf + rc + r * math.sin(math.radians(-90.0 * k / kc))) for k in range(kc + 1)][1:]
            pts += [(x0 + rc + r * math.cos(math.radians(-90.0 - 90.0 * k / kc)), yf + rc + r * math.sin(math.radians(-90.0 - 90.0 * k / kc))) for k in range(1, kc + 1)]
            return [(x, y, z) for x, y in pts]
        rings = [ring(d, z) for d, z in sec]
        n = len(rings[0])
        V = np.array([p for r_ in rings for p in r_], float)
        # the top falls 6.6 mm toward the front: a shear of the whole solid, nothing at the ground, the full fall at the top, none in front of the nose's tangent
        y_n = yf + nr
        g = td["fall_to_front_mm"] / (y_r - y_n)
        om = np.clip((V[:, 2] - ground) / (ztop_f - ground), 0.0, 1.0)
        V[:, 2] += g * np.clip(V[:, 1] - y_n, 0.0, y_r - y_n) * om
        P0 = np.array([(p[0], p[1]) for p in rings[0]])
        area = 0.5 * float(np.sum(P0[:, 0] * np.roll(P0[:, 1], -1) - np.roll(P0[:, 0], -1) * P0[:, 1]))        # > 0: counter-clockwise seen from above
        F = []
        for i in range(len(rings) - 1):
            for k in range(n):
                k1 = (k + 1) % n
                q = (i * n + k, (i + 1) * n + k, (i + 1) * n + k1, i * n + k1)             # outward for a counter-clockwise ring
                F.append(q if area > 0 else q[::-1])
        # the top: two planar faces split on the riser's face line (the fall to the front stops there; behind it the top is level)
        bot = tuple(range((len(rings) - 1) * n, len(rings) * n))[::-1]
        front_top = tuple(list(range(0, 3)) + list(range(5, n)))                  # ring vertices 0-2 and 5..n-1 (the chord from (0, y_r) to (OW, y_r))
        back_top = (2, 3, 4, 5)
        for cap in (front_top, back_top):
            F.append(cap if area > 0 else cap[::-1])
        F.append(bot if area > 0 else bot[::-1])
        vol = sum(np.dot(V[f[0]], np.cross(V[f[j]], V[f[j + 1]])) / 6.0 for f in F for j in range(1, len(f) - 1))
        assert vol > 0, "tread faces point inward"
        o = self.add("stone_tread", V, F, "stone")
        self.objs[-1]["bev"] = (2.0, None, 1)

    # -- everything, then finish
    def build(self):
        self.build_frame()
        self.build_leaf()
        self.build_ironmongery()
        self.build_step()
        return self

    def finish(self):
        """Bevels (mm), then metres at the pivot, UVs, smooth shading by angle, materials."""
        px, py, pz = self.pivot
        M = Matrix.Scale(0.001, 4) @ Matrix.Translation((-px, -py, -pz))
        out = []
        for d in self.objs:
            ob = d["ob"]
            if d["bev"]:
                w, pred, seg = d["bev"]
                bevel(ob, w, pred, 30.0, seg)
            me = ob.data
            me.transform(M)
            me.update()
            box_uv(me)
            me.shade_smooth()
            me.set_sharp_from_angle(angle=math.radians(35.0))
            me.materials.clear()
            me.materials.append(self.mats[d["mat"]])
            out.append(ob)
        return out


def tri_count(obs):
    n = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for o in obs:
        e = o.evaluated_get(dg)
        m = e.to_mesh()
        m.calc_loop_triangles()
        n += len(m.loop_triangles)
        e.to_mesh_clear()
    return n


def export_glb(path):
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", export_apply=True, export_materials="EXPORT",
                              export_cameras=False, export_lights=False, export_yup=True)


def build_variant(T, variant, door_colour, frame_colour, out_dir, npz_dir):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    d = Door(T, variant, door_colour, frame_colour).build()
    obs = d.finish()
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(npz_dir, exist_ok=True)
    glb = os.path.join(out_dir, "door_%s.glb" % variant)
    npz = os.path.join(npz_dir, "door_%s.npz" % variant)
    blender_parts.export(obs, npz)
    export_glb(glb)
    info = {"variant": variant, "door_colour": door_colour, "frame_colour": frame_colour, "glb": glb, "npz": npz,
            "glb_bytes": os.path.getsize(glb), "triangles": tri_count(obs), "parts": {o.name: len(o.data.polygons) for o in obs},
            "pivot_mm": d.pivot}
    json.dump({o.name: {"material": o.data.materials[0].name} for o in obs}, open(os.path.join(npz_dir, "door_%s.parts.json" % variant), "w"), indent=1)
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="both", choices=["T1", "F1", "both"])
    ap.add_argument("--door-colour")
    ap.add_argument("--frame-colour", default="white")
    ap.add_argument("--out-dir", default=ASSET_DIR)
    ap.add_argument("--npz-dir", default=NPZ_DIR)
    a = ap.parse_args()
    T = load_target()
    res = {}
    for v in (["T1", "F1"] if a.variant == "both" else [a.variant]):
        res[v] = build_variant(T, v, a.door_colour or DEFAULT_PAINT[v], a.frame_colour, a.out_dir, a.npz_dir)
        print(v, "triangles", res[v]["triangles"], "glb bytes", res[v]["glb_bytes"])
    return res


if __name__ == "__main__":
    main()
