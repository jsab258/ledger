"""The ten door kinds (cottage T1 to T3, flat F1 to F7), built on the 3.1 door's own class (kit/door/build_door.py, class Door).

A kind is its frame (the 3.1 frame set T or F: jambs, head, weathered transom, fanlight, glazing bead, step or sill, all inherited unchanged), its leaf
(built here from the target's numbers), and the glazing. No furniture is in a kind: letter plates, handles, latches, keyholes, numbers, the bell push and the
scraper are separate parts (doors_furniture.py) placed per house by data. Nothing is cut in a leaf for a fitting (the 3.1 leaf's slot behind its plate, the
bores for its lock, the rose's recess are gone): every fitting stands on the face, 0.4 mm into it, and carries what it needs (the plate its own dark liner).

Parts are named by the layer the check reads: frame_, glass_, leaf_, panel_, moulding_, stone_, timber_ (the F sill), bead_ (glazing beads), lead_ (the leaded
came), net_ (the white net card behind T2's lights, a render aid in the file), iron_ (the spyhole's ring and the F7 nail heads).
"""
import copy
import json
import math
import os
import sys

import numpy as np
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doors_lib as L  # noqa: E402
from doors_lib import bd  # noqa: E402

REPO = bd.REPO
NEW_TARGET = os.path.join(REPO, "production", "cloud-week", "targets", "front-doors-all", "target.json")

KINDS = ["T1", "T2", "T3", "F1", "F2", "F3", "F4", "F5", "F6", "F7"]


def load_new_target():
    return json.load(open(NEW_TARGET, encoding="utf-8"))


def first_house(N, kind):
    return [h for h in N["street"]["houses"] if h["kind"] == kind][0]


def prepared_31(T31, N):
    """The amended 3.1 target (departures applied) with every ironmongery block switched off (the fittings are separate parts here), and the new target's paints
    and frame colours added to its lists so build_door.pick and setup_materials find them."""
    T = copy.deepcopy(T31)
    for parts in (T, T["variants"]["flat_door_over_shop"]["parts"]):
        for key in ("letter_plate", "cylinder_lock", "keep", "knob", "old_keyhole", "house_number", "knocker"):
            if key in parts["ironmongery"]:
                parts["ironmongery"][key]["present"] = False
    have = {d["id"] for d in T["door_colours"]}
    for p in N["paints"]:
        if p["id"] not in have:
            T["door_colours"].append({"id": p["id"], "srgb": p["srgb"]})
    haveF = {d["id"] for d in T["frame_colours"]}
    for p in N["frame_colours"]:
        if p["id"] not in haveF:
            T["frame_colours"].append({"id": p["id"], "srgb": p["srgb"]})
    return T


def smooth_cove(d0, h0, h1, width=14.0, n=8):
    """The target's smoothstep cove (T3): (d, depth) points from d0 over `width`."""
    out = []
    for i in range(n):
        t = i / (n - 1.0)
        sm = t * t * (3.0 - 2.0 * t)
        out.append((d0 + width * t, h0 + (h1 - h0) * sm))
    return out


class KindDoor(bd.Door):
    """One kind in its frame, in the condition and paint of a house (default: the kind's first street house). Built part by part in millimetres."""

    def __init__(self, T31, N, kind, paint=None, frame_colour=None, condition=None):
        self.N, self.kind = N, kind
        self.spec = N["kinds"][kind]
        self.fsid = self.spec["frame_set"][0]
        self.fs = N["frame_sets"][self.fsid]
        h0 = first_house(N, kind)
        self.paint = paint or h0["paint"]
        self.frame_colour = frame_colour or h0["frame_colour"]
        self.condition = condition or h0["condition"]
        T = prepared_31(T31, N)
        variant = "T1" if self.fsid == "T" else "F1"
        super().__init__(T, variant, self.paint, self.frame_colour)
        self.T31 = T
        lf = self.spec["leaf"]
        assert abs(lf["w"] - self.W) < 1e-6 and abs(lf["h"] - self.H) < 1e-6, (kind, lf["w"], self.W)
        self.TH = lf["t"]
        self.LY1 = self.LY0 + self.TH
        self.PY0 = self.LY0 + (self.TH - self.PT) / 2
        self.PY1 = self.PY0 + self.PT
        cond = N["conditions"][self.condition]
        pcol = [p for p in N["paints"] if p["id"] == self.paint][0]
        self.mats["door"] = bd.make_material("paint_" + self.paint, pcol["srgb"], cond["roughness"])
        M = self.T31["materials"]
        self.mats["lead"] = bd.make_material("lead_came", [90, 92, 95], 0.5, 0.8)
        self.mats["net"] = bd.make_material("net_white", [200, 198, 190], 0.9)
        self.mats["timber_bare"] = bd.make_material("timber_bare", [118, 110, 100], 0.85)
        self.mats["iron_black"] = bd.make_material("cast_iron", [30, 30, 32], 0.65, 1.0)
        self.lap = self.P["mouldings"]["outside_bolection"]["lap_over_framing_mm"]
        self.below = self.P["mouldings"]["outside_bolection"]["panel_face_below_framing_mm"]
        self.leaf_entry = None
        self.notes["kind"] = kind

    # -------------------------------------------------------------- helpers
    def uabs(self, u):
        return self.X0 + u

    def vabs(self, v):
        return self.Z0 + v

    def open_poly(self, o):
        x0, x1, z0, z1 = self.uabs(o["u0"]), self.uabs(o["u1"]), self.vabs(o["v0"]), self.vabs(o["v1"])
        if o.get("head") == "raked":
            return L.raked_rect_pts(x0, z0, x1, z1, o["head_rise"], o["rise_toward"])
        if o["type"] == "small_light":
            return L.round_top_rect_pts(x0, z0, x1, z1, o.get("corner_r", 0.0))
        if o["type"] == "spyhole":
            cx, cz, r = 0.5 * (x0 + x1), 0.5 * (z0 + z1), 0.5 * (x1 - x0)
            return L.dedupe(L.arc_pts(cx, cz, r, 0, 360, 32)[:-1])
        return L.rect_pts(x0, z0, x1, z1)

    def new_slab(self, name="leaf_frame"):
        V, Fc = bd.box(self.X0, self.LY0, self.Z0, self.X0 + self.W, self.LY1, self.Z0 + self.H)
        ob = self.add(name, V, Fc, "door")
        self.leaf_entry = self.objs[-1]
        return ob

    def leaf_edges_bevel(self):
        planes = [(0, self.X0), (0, self.X0 + self.W), (1, self.LY0), (1, self.LY1), (2, self.Z0), (2, self.Z0 + self.H)]
        self.leaf_entry["bev"] = (self.L["arris_ease_mm"], lambda a, b: bd.on_planes(a, b, planes), 1)

    def cut_poly(self, ob, pts, a, b):
        bd.cut(ob, *bd.prism(pts, ("x", "z"), "y", a, b))

    # -------------------------------------------------------------- the condition: the rotted foot of a neglected door
    def hinge_side_u(self):
        """u range of the notch: 130 wide at the hinge-side end of the bottom edge (the target: 60 to 200 wide, 25 high, 3 deep, in the lower arris at the hinge side)."""
        w = 130.0
        return (0.0, w) if self.spec["leaf"]["lock_side"] == "right" else (self.W - w, self.W)

    def notch(self, ob):
        """The eroded notch in the lower arris at the hinge side: 25 high, 130 wide, 3 deep (from the face), cut from the leaf; bare grey wood lines it (leaf_notch_bare)."""
        if self.condition != "neglected":
            return
        u0, u1 = self.hinge_side_u()
        a, b = self.X0 + u0, self.X0 + u1
        # open at the end of the leaf: the cutter runs past the leaf's edge, so the notch begins at the corner
        ca, cb = (a - 1.0 if u0 == 0.0 else a), (b + 1.0 if u1 == self.W else b)
        bd.cut(ob, *bd.box(ca, self.LY0 - 1.0, self.Z0 - 1.0, cb, self.LY0 + 3.0, self.Z0 + 25.0))
        t = 0.3
        liners = [bd.box(a - t, self.LY0 + 2.7, self.Z0 + 0.4, b + t, self.LY0 + 3.3, self.Z0 + 25.3),            # the back wall
                  bd.box(a - t, self.LY0 + 0.4, self.Z0 + 24.7, b + t, self.LY0 + 3.3, self.Z0 + 25.3)]            # the roof
        if u0 != 0.0:
            liners.append(bd.box(a - t, self.LY0 + 0.4, self.Z0 + 0.4, a + t, self.LY0 + 3.3, self.Z0 + 25.3))
        if u1 != self.W:
            liners.append(bd.box(b - t, self.LY0 + 0.4, self.Z0 + 0.4, b + t, self.LY0 + 3.3, self.Z0 + 25.3))
        Vs, Fs, off = [], [], 0
        for V, Fc in liners:
            Vs.append(V)
            Fs += [tuple(i + off for i in f) for f in Fc]
            off += len(V)
        self.add("leaf_notch_bare", np.vstack(Vs), Fs, "timber_bare")
        self.notes["notch_u"] = [u0, u1]

    # -------------------------------------------------------------- panelled leaves: T1 F1 F2 F3
    def groups_of_rows(self, ops):
        return sorted({(round(o["v0"], 3), round(o["v1"], 3)) for o in ops})

    def cut_joints_general(self, ob, ops, gap):
        """The joint lines (D15: 0.8 wide, 0.8 deep): down both stiles' inner edges at each rail's height, and across the muntin at each panel row's foot and head."""
        jg = self.L.get("joint_groove_mm")
        if not jg:
            return
        w, dpt = jg["width"], jg["depth"]
        edge = 3.0
        rows = self.groups_of_rows(ops)
        u_left = min(o["u0"] for o in ops)
        u_right = max(o["u1"] for o in ops)
        rails = [(edge, rows[0][0] - gap)]
        for (a0, a1), (b0, b1) in zip(rows[:-1], rows[1:]):
            rails.append((a1 + gap, b0 - gap))
        rails.append((rows[-1][1] + gap, self.H - edge))
        for u in (u_left, u_right):
            for v0, v1 in rails:
                bd.cut(ob, *bd.box(self.uabs(u) - w / 2, self.LY0 - 1.0, self.vabs(v0), self.uabs(u) + w / 2, self.LY0 + dpt, self.vabs(v1)))
        cols = sorted({(o["u0"], o["u1"]) for o in ops})
        if len(cols) >= 2:
            ua, ub = cols[0][1] + gap, cols[1][0] - gap
            for v0, v1 in rows:
                for v in (v0, v1):
                    bd.cut(ob, *bd.box(self.uabs(ua), self.LY0 - 1.0, self.vabs(v) - w / 2, self.uabs(ub), self.LY0 + dpt, self.vabs(v) + w / 2))

    def build_leaf_panelled(self):
        spec, lf = self.spec, self.spec["leaf"]
        ops = lf["openings"]
        GR, PLAY = self.GR, self.PLAY
        ob = self.new_slab()
        polys = {}
        for o in ops:
            poly = L.ccw(self.open_poly(o))
            polys[o["id"]] = poly
            self.cut_poly(ob, poly, self.LY0 - 1.0, self.LY1 + 1.0)                        # the opening
            if L.is_rect(poly):
                x0, x1 = min(p[0] for p in poly), max(p[0] for p in poly)
                z0, z1 = min(p[1] for p in poly), max(p[1] for p in poly)
                bd.cut(ob, *bd.box(x0 - GR, self.PY0 - 0.1, z0 - GR, x1 + GR, self.PY1 + 0.1, z1 + GR))         # the groove all round it, 0.1 loose
            else:
                self.cut_poly(ob, L.offset_poly(poly, -GR), self.PY0 - 0.1, self.PY1 + 0.1)
        mo = spec["mouldings"]["outside"]
        gap = (self.lap if mo["kind"] == "bolection" else 0.0) + 0.2
        self.cut_joints_general(ob, ops, gap)
        self.notch(ob)
        self.leaf_edges_bevel()
        for o in ops:                                                                       # the panels, floating in their grooves
            poly = polys[o["id"]]
            if L.is_rect(poly):
                x0, x1 = min(p[0] for p in poly), max(p[0] for p in poly)
                z0, z1 = min(p[1] for p in poly), max(p[1] for p in poly)
                V, Fc = bd.box(x0 - GR + PLAY / 2, self.PY0, z0 - GR + 0.1, x1 + GR - PLAY / 2, self.PY1, z1 + GR - 0.1)
            else:
                V, Fc = bd.prism(L.offset_poly(poly, -(GR - 0.8)), ("x", "z"), "y", self.PY0, self.PY1)
            self.add("panel_" + o["id"], V, Fc, "door")
        # the mouldings: the target's profile (d from the moulding's outer edge, h above the framing face), the outside edge standing `lap` over the framing
        dh = [tuple(q) for q in mo["profile_dh"]]
        bw = mo["width_on_face"]
        lap = self.lap if mo["kind"] == "bolection" else 0.0
        if mo["kind"] != "bolection":
            dh = dh[:-1]                                                                    # the stuck ovolo's last point drops to the framing plane: the closure below takes it down to the panel
        open_line = bd.smooth_open([(0.0, -0.5)] + dh[1:])
        poly_m = open_line + [(bw, -self.below - 0.5), (lap - 0.5, -self.below - 0.5), (lap - 0.5, -0.5)]
        dt = [(d, self.LY0 - h) for d, h in poly_m]
        sgl_w = self.P["mouldings"]["inside_single"]["width_on_face_mm"]
        single = [(0.0, self.LY1), (4.0, self.LY1), (10.0, self.LY1 - 6.0), (16.0, self.PY1 + 4.0), (sgl_w, self.PY1), (0.0, self.PY1)]
        for o in ops:
            poly = polys[o["id"]]
            V, Fc = L.sweep_poly(dt, L.offset_poly(poly, -lap))
            self.add("moulding_" + ("bolection_" if mo["kind"] == "bolection" else "ovolo_") + o["id"], V, Fc, "door")
            if mo["kind"] == "bolection":
                V, Fc = L.sweep_poly(single, poly)
                self.add("moulding_single_" + o["id"], V, Fc, "door")
        if self.kind == "T1":                                                              # the lock-rail band and the weatherboard (3.1, D4 and D6)
            for key in ("lock_rail_band", "weatherboard"):
                blk = self.P["mouldings"][key]
                if not blk.get("present"):
                    continue
                za, zb = blk["z_above_leaf_bottom_mm"]
                x0, x1 = blk["x_mm"]
                zp = [tuple(q) for q in blk["profile_zp_mm"]]
                line = bd.smooth_open([(zp[0][0], -0.5)] + zp[1:-1] + [(zp[-1][0], -0.5)])
                outline = [(self.LY0 - p, self.Z0 + za + z) for z, p in line]
                V, Fc = bd.prism(outline, ("y", "z"), "x", x0, x1)
                self.add("moulding_" + ("band" if key == "lock_rail_band" else "weatherboard"), V, Fc, "door")

    # -------------------------------------------------------------- glazed leaves: T2 and F4
    def bead_dt(self, glass_front_y):
        """The 3.1 glazing bead's section, as build_glazing makes it: (d inward from the opening's edge, y), standing on the glass front, 0.4 into the frame."""
        gl = self.gl
        prof = [tuple(q) for q in gl["bead_profile_ap_mm"]]
        (a1, p1), (a2, p2) = prof[1], prof[2]
        foot_x = a1 + (a2 - a1) * ((-0.3 - p1) / (p2 - p1)) if p2 != p1 else a1
        front = bd.smooth_open(prof[1:]) if len(prof) > 3 else prof[1:]
        poly = [(-0.4, -0.3), (foot_x, -0.3)] + front + [(-0.4, prof[-1][1])]
        return [(d, glass_front_y - p) for d, p in poly]

    def build_leaf_glazed(self):
        spec, lf = self.spec, self.spec["leaf"]
        ops = lf["openings"]
        ob = self.new_slab()
        for o in ops:
            self.cut_poly(ob, self.open_poly(o), self.LY0 - 1.0, self.LY1 + 1.0)
        # the bars are 22 deep: the leaf is hollowed behind them, over the whole run of lights
        u0 = min(o["u0"] for o in ops)
        u1 = max(o["u1"] for o in ops)
        v0 = min(o["v0"] for o in ops)
        v1 = max(o["v1"] for o in ops)
        bar_depth = 22.0
        bd.cut(ob, *bd.box(self.uabs(u0), self.LY0 + bar_depth, self.vabs(v0), self.uabs(u1), self.LY1 + 1.0, self.vabs(v1)))
        gy0, gy1 = self.LY0 + 14.0, self.LY0 + 17.0                       # the pane, 3 mm, in a 4 mm slot 13.5 to 17.5 behind the face, 6.4 into the framing
        for o in ops:
            x0, x1, z0, z1 = self.uabs(o["u0"]), self.uabs(o["u1"]), self.vabs(o["v0"]), self.vabs(o["v1"])
            bd.cut(ob, *bd.box(x0 - 6.4, gy0 - 0.5, z0 - 6.4, x1 + 6.4, gy1 + 0.5, z1 + 6.4))
        self.notch(ob)
        self.leaf_edges_bevel()
        dt = self.bead_dt(gy0)
        for i, o in enumerate(ops, 1):
            x0, x1, z0, z1 = self.uabs(o["u0"]), self.uabs(o["u1"]), self.vabs(o["v0"]), self.vabs(o["v1"])
            V, Fc = bd.box(x0 - 6.0, gy0, z0 - 6.0, x1 + 6.0, gy1, z1 + 6.0)
            self.add("glass_" + o["id"], V, Fc, "glass")
            V, Fc = L.sweep_poly(dt, L.rect_pts(x0, z0, x1, z1))
            self.add("bead_" + o["id"], V, Fc, "door")
            if self.kind == "T2":                                          # D3 shows a white net behind the lights: a pale card 1.5 behind the pane
                V, Fc = bd.box(x0 + 0.3, gy1 + 1.5, z0 + 0.3, x1 - 0.3, gy1 + 2.0, z1 - 0.3)
                self.add("net_" + o["id"], V, Fc, "net")

    # -------------------------------------------------------------- flush leaves: F5 F6
    def lipping_lines(self, ob):
        """The hairline round the lipping (target: 1 mm), 6 mm in from each edge, 0.6 deep: one ring-shaped cutter, so no two cutters share a face."""
        ins = 6.0
        prof = [(ins, self.LY0 - 1.0), (ins + 1.0, self.LY0 - 1.0), (ins + 1.0, self.LY0 + 0.6), (ins, self.LY0 + 0.6)]
        V, Fc = L.sweep_poly(prof, L.rect_pts(self.X0, self.Z0, self.X0 + self.W, self.Z0 + self.H))
        bd.cut(ob, V, Fc)

    def build_leaf_flush(self):
        spec, lf = self.spec, self.spec["leaf"]
        ob = self.new_slab()
        o = lf["openings"][0]
        if o["type"] == "slit_light":
            poly = L.rect_pts(self.uabs(o["u0"]), self.vabs(o["v0"]), self.uabs(o["u1"]), self.vabs(o["v1"]))
            self.cut_poly(ob, poly, self.LY0 - 1.0, self.LY1 + 1.0)
            gy0, gy1 = self.LY0 + 12.0, self.LY0 + 15.0
            x0, x1, z0, z1 = poly[0][0], poly[1][0], poly[0][1], poly[2][1]
            bd.cut(ob, *bd.box(x0 - 6.4, gy0 - 0.5, z0 - 6.4, x1 + 6.4, gy1 + 0.5, z1 + 6.4))
        else:                                                                               # the spyhole: a round hole through the leaf
            poly = self.open_poly(o)
            self.cut_poly(ob, poly, self.LY0 - 1.0, self.LY1 + 1.0)
        self.lipping_lines(ob)
        self.notch(ob)
        self.leaf_edges_bevel()
        if o["type"] == "slit_light":
            V, Fc = bd.box(x0 - 6.0, gy0, z0 - 6.0, x1 + 6.0, gy1, z1 + 6.0)
            self.add("glass_slit", V, Fc, "glass")
            # a 15 mm square timber bead, 4 proud, planted on the face round the slit (outside its edge, 0.6 clear so no face is shared)
            outer = L.rect_pts(x0 - 15.6, z0 - 15.6, x1 + 15.6, z1 + 15.6)
            prof = [(0.0, self.LY0 + 0.4), (0.0, self.LY0 - 4.0), (15.0, self.LY0 - 4.0), (15.0, self.LY0 + 0.4)]
            V, Fc = L.sweep_poly(prof, outer)
            self.add("bead_slit", V, Fc, "door")
        else:
            cx, cz = 0.5 * (self.uabs(o["u0"]) + self.uabs(o["u1"])), 0.5 * (self.vabs(o["v0"]) + self.vabs(o["v1"]))
            V, Fc = bd.lathe([(0.0, 0.0), (6.6, 0.0), (6.6, 3.0), (0.0, 3.0)], 24)       # the lens: a glass disc 14 across, 3 thick, 8 behind the face
            self.add("glass_lens", np.stack([cx + V[:, 0], self.LY0 + 8.0 + V[:, 2], cz + V[:, 1]], axis=1), Fc, "glass")

    # -------------------------------------------------------------- T3: the moulded sheet with two embossed panels and a small light
    def build_leaf_moulded(self):
        spec, lf = self.spec, self.spec["leaf"]
        ob = self.new_slab()
        by_id = {o["id"]: o for o in lf["openings"]}
        prof_cove = smooth_cove(0.0, 0.0, 3.0)                                              # (d, depth): the outer cove, 0 to 3 over 14 mm
        prof_cove2 = smooth_cove(0.0, 3.0, 6.0)                                             # the inner cove, 3 to 6 over 14 mm
        for oid in ("upper_panel", "lower_panel"):
            o = by_id[oid]
            outer = L.ccw(L.rect_pts(self.uabs(o["u0"]), self.vabs(o["v0"]), self.uabs(o["u1"]), self.vabs(o["v1"])))
            iv = o["inner"]
            ix = (self.uabs(iv["u0"]), self.vabs(iv["v0"]), self.uabs(iv["u1"]), self.vabs(iv["v1"]))
            inner = L.ccw(L.segmental_rect_pts(*ix, iv["springing_below_crown"]) if iv["head"] == "segmental" else L.rect_pts(*ix))
            # cutter 1: from above the face down the cove to the margin's floor (3 deep); cutter 2: from the inner outline down its cove to the field (6 deep)
            for poly, prof, top in ((outer, prof_cove, 0.0), (inner, prof_cove2, 3.0)):
                rings = [(L.offset_poly(poly, -0.05), self.LY0 + top - 1.0)]
                rings += [(L.offset_poly(poly, d), self.LY0 + h) for d, h in prof]
                end_d, end_h = prof[-1]
                V, Fc = L.loft_rings(rings)
                bd.cut(ob, V, Fc)
        light = by_id["small_light"]
        lp = L.round_top_rect_pts(self.uabs(light["u0"]), self.vabs(light["v0"]), self.uabs(light["u1"]), self.vabs(light["v1"]), light["corner_r"])
        self.cut_poly(ob, lp, self.LY0 - 1.0, self.LY1 + 1.0)
        # the glass sits in a rebate cut from the back (10 mm of framing all round, 8 deep), under a moulded bead
        reb = L.offset_poly(L.ccw(lp), -10.0)
        self.cut_poly(ob, reb, self.LY1 - 8.0, self.LY1 + 1.0)
        self.notch(ob)
        self.leaf_edges_bevel()
        g = L.offset_poly(L.ccw(lp), -9.6)
        V, Fc = bd.prism(g, ("x", "z"), "y", self.LY1 - 8.0 + 0.5, self.LY1 - 8.0 + 3.5)
        self.add("glass_small_light", V, Fc, "glass")
        # the moulded bead on the inside: a ring behind the glass (hidden from the street), from the rebate's wall in to the hole's edge, 4.4 to 0.5 in front of the sheet's back
        bead = [(-0.4, self.LY1 - 4.4), (-0.4, self.LY1 - 0.5), (6.0, self.LY1 - 0.5), (10.0, self.LY1 - 2.5), (10.0, self.LY1 - 4.4)]
        V, Fc = L.sweep_poly(bead, reb)
        self.add("bead_small_light", V, Fc, "door")

    # -------------------------------------------------------------- F7: the ledged and braced service door
    def build_leaf_ledged(self):
        spec, lf = self.spec, self.spec["leaf"]
        bw, bt = lf["board_w"], lf["board_t"]
        edges = lf["board_edges_u"]
        n = len(edges) - 1
        tongue_len, tongue_t, groove_d = 6.0, 7.0, 6.5
        yc = bt / 2.0
        gap = 0.2
        for k in range(n):
            xl = self.uabs(edges[k]) + (gap / 2 if k > 0 else 0.0)
            xr = self.uabs(edges[k + 1]) - (gap / 2 if k < n - 1 else 0.0)
            y0, y1 = self.LY0, self.LY0 + bt
            pts = []
            # a closed outline in (x, y) walking the board's section: back-left, up the left edge (with its groove), the face with its two chamfers, down the right edge (with its tongue), back
            pts.append((xl, y1))
            if k > 0:
                pts += [(xl, y0 + yc + 3.75), (xl + groove_d, y0 + yc + 3.75), (xl + groove_d, y0 + yc - 3.75), (xl, y0 + yc - 3.75), (xl, y0 + 2.0), (xl + 3.0, y0)]
            else:
                pts += [(xl, y0)]
            if k < n - 1:
                pts += [(xr - 3.0, y0), (xr, y0 + 2.0), (xr, y0 + yc - tongue_t / 2), (xr + tongue_len, y0 + yc - tongue_t / 2), (xr + tongue_len, y0 + yc + tongue_t / 2), (xr, y0 + yc + tongue_t / 2)]
            else:
                pts += [(xr, y0)]
            pts.append((xr, y1))
            V, Fc = bd.prism(pts, ("x", "y"), "z", self.Z0, self.Z0 + self.H)
            ob = self.add("leaf_board_%d" % (k + 1), V, Fc, "door")
            hinge_first = (k == 0 and lf["lock_side"] == "right") or (k == n - 1 and lf["lock_side"] == "left")
            if hinge_first:
                self.notch(ob)
        # the ledges, 16 thick behind the boards (the leaf is 38 thick: 22 + 16), the two braces 15 thick
        ledge_t = self.TH - bt
        led = lf["ledges_v"]
        for i, (v0, v1) in enumerate(led, 1):
            V, Fc = bd.box(self.X0 + 20.0, self.LY0 + bt - 0.4, self.vabs(v0), self.X0 + self.W - 20.0, self.LY0 + self.TH, self.vabs(v1))
            self.add("leaf_ledge_%d" % i, V, Fc, "door")
        hinge_left = lf["lock_side"] == "right"
        for i in range(len(led) - 1):
            z_lo, z_hi = led[i][0] + 6.0, led[i + 1][1] - 6.0                 # from the foot of the lower ledge to the head of the upper one (its ends 6 inside each ledge)
            xa, xb = (self.X0 + 30.0, self.X0 + self.W - 30.0)
            if not hinge_left:
                xa, xb = xb, xa
            wdt = 90.0
            sgn = 1.0 if xb > xa else -1.0
            poly = [(xa, self.vabs(z_lo)), (xa + sgn * wdt, self.vabs(z_lo)), (xb, self.vabs(z_hi)), (xb - sgn * wdt, self.vabs(z_hi))]
            V, Fc = bd.prism(L.ccw(poly), ("x", "z"), "y", self.LY0 + bt - 0.7, self.LY1 - 1.0)
            self.add("leaf_brace_%d" % (i + 1), V, Fc, "door")
        # the nail heads: 18 low domes, 9 across, 3 proud, one head per board at each ledge (one part)
        nh = lf["nail_heads"]
        # a dome standing 3 proud (toward -y) of the face, 0.4 into it
        Vs, Fs, off = [], [], 0
        for u, v in nh["at"]:
            Vd, Fd = bd.lathe([(0.0, -0.4), (4.5, -0.4), (4.5, 1.2), (3.2, 2.4), (1.6, 2.9), (0.0, 3.0)], 16)
            Vd = bd.place_axis_y(Vd, self.uabs(u), self.LY0, self.vabs(v))
            Vs.append(Vd)
            Fs += [tuple(i + off for i in f) for f in Fd]
            off += len(Vd)
        self.add("iron_nail_heads", np.vstack(Vs), Fs, "iron_black")

    # -------------------------------------------------------------- the glazing of the transom: leaded (T2), reeded (F6)
    def build_glazing(self):
        super().build_glazing()
        g = self.spec["glass"]["transom"]
        if g == "leaded_diamond":
            self.build_came()
        elif g == "reeded_4mm":
            self.build_reeded()

    def swap_glass(self, name, V, Fc):
        for d in self.objs:
            if d["ob"].name == name:
                bd._drop(d["ob"])
                self.objs.remove(d)
                break
        self.add(name, V, Fc, "glass")

    def build_came(self):
        """T2's fanlight (D3): the upper 144 of the 267 one plain pane; under it a band 83 high of crossed diagonal came at a 145 pitch (lozenges 145 x 83, five whole,
        a tip at each end), a horizontal came at the band's head and one 40 above the foot, an upright under each lozenge point. Came 6 wide, 3 proud of the glass."""
        gl = self.N["glass"]["leaded_diamond"]
        cw, pr = gl["came_w"], gl["came_proud"]
        P, Hh = gl["lozenge"]
        gx0, gx1, gz0, gz1 = self.GX0, self.GX1, self.GZ0, self.GZ1
        zt = gz1 - gl["plain_pane_h"]
        zb = gz0 + gl["foot_came_above_foot"]
        cx = 0.5 * (gx0 + gx1)
        glass_front = self.GLASS_Y - self.GLASS_T / 2.0
        y_back, y_front = glass_front + 0.55, glass_front - pr
        win = Polygon(L.rect_pts(gx0, gz0, gx1, gz1))
        band = Polygon(L.rect_pts(gx0, zb, gx1, zt))
        pieces = []
        nk = int((gx1 - gx0) / P) + 3
        for k in range(-nk, nk + 1):
            xk = cx + k * P
            for seg in (((xk, zb), (xk + P, zt)), ((xk, zt), (xk + P, zb))):
                pieces.append(LineString(seg).buffer(cw / 2.0, cap_style=2).intersection(band))
        pieces.append(Polygon(L.rect_pts(gx0, zb - cw / 2.0, gx1, zb + cw / 2.0)))
        pieces.append(Polygon(L.rect_pts(gx0, zt - cw / 2.0, gx1, zt + cw / 2.0)))
        for k in range(-(gl["whole_lozenges"] // 2), gl["whole_lozenges"] // 2 + 1):
            xk = cx + k * P
            pieces.append(Polygon(L.rect_pts(xk - cw / 2.0, gz0, xk + cw / 2.0, zb)))
        objs = []
        for g in pieces:
            g = g.intersection(win)
            for h in ([g] if g.geom_type == "Polygon" else [q for q in getattr(g, "geoms", []) if q.geom_type == "Polygon"]):
                if h.area < 4.0:
                    continue
                V, Fc = bd.prism(L.ccw(list(h.exterior.coords)[:-1]), ("x", "z"), "y", y_front, y_back)
                objs.append(bd.new_obj("_came", V, Fc))
        ob = bd.unite_objs("lead_came", objs)
        self.objs.append({"ob": ob, "mat": "lead", "bev": None})
        self.notes["came_parts"] = len(objs)

    def build_reeded(self):
        """F6's transom glass (Judgement): a 2.8 base with vertical flutes of circular segments, pitch 6, 1.2 deep, on the street face (4.0 in all)."""
        g = self.N["glass"]["reeded_4mm"]
        pitch, depth = g["flute_pitch"], g["flute_depth"]
        gx0, gx1 = self.GX0 - self.GLASS_RB + 0.4, self.GX1 + self.GLASS_RB - 0.4
        gz0, gz1 = self.Z_TR_TOP - self.GLASS_RB + 0.3, self.GZ1 + self.GLASS_RB - 0.3
        y_mid = self.GLASS_Y
        base_t = g["thickness"] - depth
        V, Fc = bd.box(gx0, y_mid - base_t / 2.0, gz0, gx1, y_mid + base_t / 2.0, gz1)
        self.swap_glass("glass_fanlight", V, Fc)
        yf = y_mid - base_t / 2.0                                                            # the base's street face
        nflute = int((self.GX1 - self.GX0 - 2.0) / pitch)            # whole flutes, 1 to 2 mm short of the pane's edges
        wtot = nflute * pitch
        xs = 0.5 * (self.GX0 + self.GX1) - wtot / 2.0
        R = (pitch * pitch / 4.0 + depth * depth) / (2.0 * depth)
        pts = [(xs, yf + 0.6)]
        for i in range(nflute):
            c = xs + (i + 0.5) * pitch
            for j in range(0, 9):
                a = -math.asin((pitch / 2.0) / R) + 2 * math.asin((pitch / 2.0) / R) * j / 8.0
                x = c + R * math.sin(a)
                y = yf - (R * math.cos(a) - (R - depth))
                pts.append((x, y))
        pts.append((xs + wtot, yf + 0.6))
        # the profile polygon in (x, y); dedupe, then extrude along z over the opening's height (inside the putty fillet's reach)
        pts = L.dedupe(pts)
        pts = pts if _area(pts) > 0 else pts[::-1]
        V, Fc = bd.prism(pts, ("x", "y"), "z", self.GZ0 + 0.5, self.GZ1 - 0.5)
        self.add("glass_fanlight_flutes", V, Fc, "glass")

    # -------------------------------------------------------------- build
    def build_leaf(self):
        if self.kind in ("T1", "F1", "F2", "F3"):
            self.build_leaf_panelled()
        elif self.kind in ("T2", "F4"):
            self.build_leaf_glazed()
        elif self.kind in ("F5", "F6"):
            self.build_leaf_flush()
        elif self.kind == "T3":
            self.build_leaf_moulded()
        elif self.kind == "F7":
            self.build_leaf_ledged()
        else:
            raise SystemExit("unknown kind " + self.kind)

    def build_ironmongery(self):
        return                                                  # no fitting is part of a kind: see doors_furniture.py

    def build(self):
        self.build_frame()
        self.build_leaf()
        self.build_step()
        return self


def _area(pts):
    a = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        a += x0 * y1 - x1 * y0
    return a / 2.0
