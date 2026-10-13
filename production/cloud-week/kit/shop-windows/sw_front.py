"""Rita's whole front, assembled in Blender from the 3.2 kit's parts and the doors, the band above them, the fascia, the signs and the grille.

Used by build_ritas.py (stage `front`). Run inside a Python that has bpy (Blender 5.2.2 as a module).

Frame (the kit's, millimetres while building): x = u across the bay from the viewer's LEFT (bay middle u 3000 = model x 0), y = -d (d out from the
wall face, the street toward -y), z up from the footway. Written in metres, z up, scale 1, pivot at the bay's middle on the footway.

What is made here, from target.json (production/cloud-week/targets/shop-windows/) and the 3.2 kit (production/cloud-week/kit/shopfront/build_shopfront.py, imported):
  the kit's Builder: pilasters, consoles, fascia board, cornice, sill, stallriser, window frame (build_assembly's own calls)
  the shop door T1 (target 4.2: photograph numbers, D1), its frame, threshold, bell, OPEN sign, letter plate, lever, kick plate, hinges
  the band above the doors (4.1a): door frame head, fanlight, transom, three toplights, panel over the side door, head
  the side door: the door family's F1 (production/assets/cloud-week/door/door_F1.glb), mirrored, trimmed at z 2400 and to its slot
  the 4.1 fascia board textures on the board, the glass lettering rows, the three balls on their bracket
  the night grille (4.3): top rail, bottom channel and fixing plates stand by day (in the front); the lattice is its own model
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
KIT = os.path.join(REPO, "production", "cloud-week", "kit", "shopfront")
sys.path.insert(0, KIT)
sys.path.insert(0, os.path.join(REPO, "production", "cloud-week", "kit", "tools"))

import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402
import build_shopfront as bs  # noqa: E402  (the 3.2 kit: Builder, prism_ud, prism_dz, box, finish, materials)
import joinery  # noqa: E402

SHOP = "ritas"
F1_GLB = os.path.join(REPO, "production", "assets", "cloud-week", "door", "door_F1.glb")
BAY_MID = 3000.0
Y_WALL = 5.295   # street y of the wall face (d 0): the kit's glass back face (d 30) stands at the street model's 5.265
# the brick piers the gate stands behind each pilaster (13 Oct, from the try 1 street review, N2): model x, y 0 to 0.30 back, z 0 to 3.56. The pilaster's shaft and core stop 30 mm
# short of the bay's edge (x 2.970) and the street model's wall opening is the whole bay, so without a pier the outer 30 to 54 mm of the bay shows the sky at STREET_30.
PIERS_X = ((-3.0, -2.65), (2.65, 3.0))
PIER_Y = (0.0, 0.30)
PIER_Z = (0.0, 3.56)
# the hall behind the side door (N3): from the frame's back face (d 0) back to d -HALL_DEPTH, a closed box. The review words it 1.2 m deep; the card stands 0.58 behind the wall
# (d -580), so a box deeper than that would cut through the card and the card would show inside the hall: 0.50 keeps the hall's back wall 0.08 in front of the card
HALL_DEPTH = 500.0
HALL_Z = (25.0, 2420.0)


def load_sw_target():
    return json.load(open(os.path.join(REPO, "production", "cloud-week", "targets", "shop-windows", "target.json"), encoding="utf-8"))


def lin(c):
    return bs.lin(c)


# ---------------------------------------------------------------------------------------------------------------- small geometry helpers
def bx(u0, u1, d0, d1, z0, z1):
    return bs.box(u0, u1, d0, d1, z0, z1)


def cyl_z(u, d, z0, z1, r, n=12):
    """A vertical cylinder (axis z) as (V, F), mm."""
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    ring = np.stack([u + r * np.cos(a), -(d + r * np.sin(a))], axis=1)
    return bs.prism_ud([(p[0], -p[1]) for p in ring], z0, z1)


def cyl_d(u, z, d0, d1, r, n=12):
    """A cylinder whose axis runs out along d (toward the street), mm."""
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    V = []
    for d in (d0, d1):
        for t in a:
            V.append((u + r * math.cos(t), -d, z + r * math.sin(t)))
    V = np.array(V)
    F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return V, F


def rod(p0, p1, r, n=8):
    """A straight round rod from p0 to p1, each (u, d, z) in mm, radius r, as (V, F) (closed ends)."""
    a = np.array([p0[0], -p0[1], p0[2]], float)
    b = np.array([p1[0], -p1[1], p1[2]], float)
    ax = b - a
    ax /= np.linalg.norm(ax)
    helper = np.array([0.0, 1.0, 0.0]) if abs(ax[1]) < 0.9 else np.array([1.0, 0.0, 0.0])
    e1 = np.cross(ax, helper)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(ax, e1)
    V = []
    for c in (a, b):
        for k in range(n):
            t = 2 * math.pi * k / n
            V.append(c + r * (math.cos(t) * e1 + math.sin(t) * e2))
    F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return np.array(V), F


def torus_d(u, z, d, R, r, nm=16, nn=6):
    """A torus whose axis runs along d (the ring stands in the u-z plane, facing the street): centre (u, d, z), major radius R, minor radius r, as (V, F), mm."""
    V, F = [], []
    for i in range(nm):
        a = 2 * math.pi * i / nm
        for j in range(nn):
            b = 2 * math.pi * j / nn
            rho = R + r * math.cos(b)
            V.append((u + rho * math.cos(a), -(d + r * math.sin(b)), z + rho * math.sin(a)))
    for i in range(nm):
        for j in range(nn):
            i2, j2 = (i + 1) % nm, (j + 1) % nn
            F.append((i * nn + j, i2 * nn + j, i2 * nn + j2, i * nn + j2))
    return np.array(V), F


def lathe(profile_rz, u, d, z, n=14):
    """A solid of revolution about the vertical axis through (u, d), profile = [(radius, dz), ...] from the top down, closed on the axis. mm."""
    P = [(max(r, 0.0), dz) for r, dz in profile_rz]
    V = []
    rings = []
    for r, dz in P:
        if r < 1e-6:
            V.append((u, -d, z + dz))
            rings.append(("pole", len(V) - 1))
        else:
            idx = []
            for k in range(n):
                t = 2 * math.pi * k / n
                V.append((u + r * math.cos(t), -(d + r * math.sin(t)), z + dz))
                idx.append(len(V) - 1)
            rings.append(("ring", idx))
    F = []
    for (ka, a), (kb, b) in zip(rings[:-1], rings[1:]):
        if ka == "ring" and kb == "ring":
            for k in range(n):
                k2 = (k + 1) % n
                F += [(a[k], a[k2], b[k2], b[k])]
        elif ka == "pole":
            for k in range(n):
                F += [(a, b[(k + 1) % n], b[k])]
        else:
            for k in range(n):
                F += [(a[k], a[(k + 1) % n], b)]
    return np.array(V), F


def polyline_strip(pts_dz, u0, u1, thick):
    """A thin strip of constant width u0..u1 following a (d, z) polyline, `thick` mm thick (offset along the polyline's normal). Returns (V, F)."""
    P = np.asarray(pts_dz, float)
    n = len(P)
    tang = np.gradient(P, axis=0)
    tang /= np.linalg.norm(tang, axis=1)[:, None]
    nor = np.stack([-tang[:, 1], tang[:, 0]], axis=1)
    A = P + nor * thick / 2
    B = P - nor * thick / 2
    ring = np.vstack([A, B[::-1]])
    return bs.prism_dz([tuple(p) for p in ring], u0, u1)


# ---------------------------------------------------------------------------------------------------------------- mesh clipping for F1
def clip_object(ob, co, no):
    """Cut a mesh object by a plane (world point co, normal no), removing the side the normal points to and capping the cut."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    r = bmesh.ops.bisect_plane(bm, geom=geom, dist=1e-9, plane_co=co, plane_no=no, clear_outer=True, clear_inner=False)
    cut = [e for e in r["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    if cut:
        bmesh.ops.holes_fill(bm, edges=cut, sides=0)
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()


# ---------------------------------------------------------------------------------------------------------------- the build
class Front:
    def __init__(self, scratch, T):
        self.scratch = scratch
        self.T = T
        self.SW = load_sw_target()
        self.R = next(s for s in self.SW["shops"] if s["id"] == SHOP)
        self.kt = bs.load_target()          # the 3.2 kit's target with its departures
        self.B = bs.Builder(self.kt, SHOP)
        self.mats = bs.setup_materials(self.kt, SHOP)
        m = self.mats
        m["buttermilk"] = bs.make_material("paint_buttermilk", self.R["front"]["paint_srgb"]["side_door"], 0.5, 0.0)
        m["brass"] = bs.make_material("brass", (160, 120, 55), 0.38, 1.0)
        m["steel"] = bs.make_material("steel_dark", (60, 60, 62), 0.5, 0.7)
        m["terrazzo"] = bs.make_material("terrazzo", (176, 170, 158), 0.35, 0.0)
        m["black"] = bs.make_material("powder_black", (37, 35, 34), 0.45, 0.0)
        m["black_iron"] = bs.make_material("sign_black_iron", (30, 29, 28), 0.6, 0.5)
        # the hall behind the side door: plaster and ceiling at about half the room's brightness (the room's plaster is (0.95, 0.86, 0.66) on a light texture), unlit at night
        m["hall_plaster"] = bs.make_material("hall_plaster", (150, 142, 124), 0.9, 0.0)
        m["hall_dark"] = bs.make_material("hall_floor", (82, 72, 60), 0.8, 0.0)
        self.members = {}        # name -> dict(u, d, z ranges in mm) for the checks
        self.extra = []          # objects made outside the Builder (textured quads, F1)

    # ----------------------------------------------------------------------------------------------- the kit's own parts
    def kit_parts(self):
        B = self.B
        B.pilaster("L")
        B.pilaster("R")
        for o in B.objs:
            if o.name.startswith("pilR_"):
                bs.mirror_u(o, 3000.0)
        B.console("L", uc=175.0)
        B.console("R", uc=5825.0)
        B.fascia_board()
        B.cornice()
        B.sill()
        B.stallriser()
        B.window_frame()

    def add(self, name, VF, mat, bev=bs.BEVEL, min_angle=50.0):
        return self.B.add(name, VF, mat, bev=bev, min_angle=min_angle)

    # ----------------------------------------------------------------------------------------------- the shop door T1 (target 4.2)
    def shop_door(self):
        R = self.R
        D = R["door"]
        pr = self.kt["parts"]["shop_door"]["profiles"]
        slot = R["front"]["zones_u_mm"]["shop_door"]            # [1294, 2300]
        u_in0, u_in1 = slot[0] + 50.0, slot[1] - 50.0           # 1344, 2250
        uc = (slot[0] + slot[1]) / 2.0                          # 1797
        z_foot, z_top = 28.0, 2068.0
        # frame jambs (frame_jamb_plan: 50 face x 100 deep, rebated 14 x 42 for the stop), from the threshold to the head
        jp = pr["frame_jamb_plan"]["points"]
        jl = [(u_in0 - p[0], p[1]) for p in jp]                 # inner face at u_in0, outer at the slot's edge
        jr = [(u_in1 + p[0], p[1]) for p in jp]
        self.add("door_jamb_l", bs.prism_ud(jl, 25.0, 2790.0), "white")
        self.add("door_jamb_r", bs.prism_ud(jr, 25.0, 2790.0), "white")
        # the frame's head rail under the fanlight (60 over the leaf's 3 clear)
        self.add("door_frame_head", bx(u_in0, u_in1, 0.0, 100.0, 2071.0, 2131.0), "white")
        # threshold: terrazzo, the full frame width, threshold_section (d, z)
        th = [(p[0], p[1]) for p in pr["threshold_section"]["points"]]
        self.add("door_threshold", bs.prism_dz(th, slot[0], slot[1]), "terrazzo", bev=None)
        # leaf: 900 x 2040 at z 28, hinge on the viewer's RIGHT, lever on the LEFT
        lu0, lu1 = uc - 450.0, uc + 450.0                       # 1347, 2247
        st = 115.0
        d0, d1 = 20.0, 70.0
        self.add("door_leaf_stile_lever", bx(lu0, lu0 + st, d0, d1, z_foot, z_top), "white")
        self.add("door_leaf_stile_hinge", bx(lu1 - st, lu1, d0, d1, z_foot, z_top), "white")
        ru0, ru1 = lu0 + st, lu1 - st
        rails = D["t1_rails_mm"]
        self.add("door_rail_bottom", bx(ru0, ru1, d0, d1, rails["bottom_rail"][0], rails["bottom_rail"][1]), "white")
        self.add("door_rail_lock", bx(ru0, ru1, d0, d1, rails["lock_rail"][0], rails["lock_rail"][1]), "white")
        self.add("door_rail_top", bx(ru0, ru1, d0, d1, rails["top_rail"][0], rails["top_rail"][1]), "white")
        bar = rails["glazing_bar"]
        self.add("door_glazing_bar", bx(ru0, ru1, d0, d1, bar["z"] - bar["width"] / 2, bar["z"] + bar["width"] / 2), "white")
        # lower panel: raised and fielded (raised_field_edge: flat margin 32, bevel 8 rising 10), tongues 10 into the rails and stiles
        V, F = joinery.fielded_panel(ru0 - 10.0, rails["bottom_rail"][1] - 10.0, ru1 + 10.0, rails["lock_rail"][0] + 10.0, -26.0, 14.0, 24.0, 8.0, margin=32.0)
        self.add("door_lower_panel", (V, F), "white", bev=None)
        # glass: two panes of 6 mm at d 40 to 46 in 12 rebates, an ovolo bead 14 x 11 round each (glazing_bead)
        bead = [(p[0], -p[1]) for p in pr["glazing_bead"]["points"]]
        panes = [(ru0, rails["lock_rail"][1], ru1, bar["z"] - bar["width"] / 2), (ru0, bar["z"] + bar["width"] / 2, ru1, rails["top_rail"][0])]
        for k, (a, b, c, e) in enumerate(panes):
            self.add("door_glass_%d" % k, bx(a - 10.0, c + 10.0, 40.0, 46.0, b - 8.0, e + 8.0), "glass", bev=None)
            V, F = joinery.sweep_frame(bead, a, b, c, e, -46.0)
            self.add("door_bead_%d" % k, (V, [tuple(int(i) for i in f) for f in F]), "white", bev=None)
        # furniture (brass): kick plate 770 x 170 with 8 screws, a 30 high foot strip 3 proud, letter plate 250 x 40 at z 678 centred, lever 240 x 40
        # backplate at z 1000 with the keyhole at 950, three butts 100 x 75 on the hinge edge
        self.add("door_kick_plate", bx(uc - 385.0, uc + 385.0, 70.0, 73.0, 28.0, 198.0), "brass", bev=None)
        for k, (du, z) in enumerate(((-350, 55), (-350, 171), (0, 55), (0, 171), (350, 55), (350, 171), (-175, 113), (175, 113))):
            self.add("door_kick_screw_%d" % k, cyl_d(uc + du, z, 73.0, 74.5, 4.0, 8), "steel", bev=None)
        self.add("door_foot_strip", bx(lu0, lu1, 70.0, 76.0, 28.0, 58.0), "brass", bev=None)
        lp = D["letter_plate"]
        self.add("door_letter_plate", bx(uc - 125.0, uc + 125.0, 70.0, 73.0, lp["z_mm"] - 20.0, lp["z_mm"] + 20.0), "brass", bev=None)
        self.add("door_letter_slot", bx(uc - 100.0, uc + 100.0, 73.0, 73.6, lp["z_mm"] - 6.0, lp["z_mm"] + 6.0), "steel", bev=None)
        lx = lu0 + st / 2.0
        self.add("door_lever_backplate", bx(lx - 20.0, lx + 20.0, 70.0, 73.0, 880.0, 1120.0), "brass", bev=None)
        self.add("door_lever_rose", cyl_d(lx, 1000.0, 73.0, 80.0, 17.0, 16), "brass", bev=None)
        self.add("door_lever_arm", bx(lx - 9.0, lx + 120.0, 80.0, 98.0, 991.0, 1009.0), "brass", bev=None)
        self.add("door_keyhole", bx(lx - 4.0, lx + 4.0, 73.0, 73.6, 938.0, 962.0), "steel", bev=None)
        for k, z in enumerate((178.0, 1048.0, 1918.0)):
            self.add("door_butt_%d" % k, cyl_z(lu1 + 1.0, 62.0, z - 50.0, z + 50.0, 5.5, 10), "brass", bev=None)
        # the leaf's stops behind its 3 mm clearances (left, right, head and foot) and the hall floor behind both doors: what stands behind a gap in the real door, so the front has no
        # see-through crack (FRN-07): 14 wide stops on the room side of the leaf's back face (d 4 to 20), a floor slab inside from the pilaster to the window frame
        self.add("door_stop_l", bx(u_in0, u_in0 + 14.0, 4.0, 20.0, 25.0, 2071.0), "white", bev=None)
        self.add("door_stop_r", bx(u_in1 - 14.0, u_in1, 4.0, 20.0, 25.0, 2071.0), "white", bev=None)
        self.add("door_stop_head", bx(u_in0, u_in1, 4.0, 20.0, 2060.0, 2071.0), "white", bev=None)
        self.add("door_stop_foot", bx(u_in0, u_in1, 4.0, 20.0, 25.0, 40.0), "white", bev=None)
        self.add("hall_floor_behind_doors", bx(slot[0] - 944.0, slot[1], -160.0, 4.0, 0.0, 58.0), "terrazzo", bev=None)
        # the bell (target 4.2): a spring strip 20 x 3, 220 long, on the INSIDE of the top rail, 90 from the hanging stile; the bell hung 80 below
        bd = D["bell"]
        ub = lu1 - 90.0
        # the strip spans z 1950 to 2050 and is 220 long (target 4.2): a quarter ellipse, 171 into the room and 100 down (arc length 220)
        a_h, b_v = 171.0, 100.0
        cen = (20.0, 2050.0 - b_v)
        arc = [(cen[0] + a_h * math.cos(t), cen[1] + b_v * math.sin(t)) for t in np.linspace(math.pi / 2, math.pi, 14)]
        self.add("bell_spring_strip", polyline_strip(arc, ub - 10.0, ub + 10.0, 3.0), "steel", bev=None)
        end = arc[-1]
        bz = end[1] - 80.0
        self.add("bell_hanger", cyl_z(ub, end[0] + 0.0, bz + 2.0, end[1], 1.6, 6), "steel", bev=None)
        # the bell (13 Oct, from the try 1 close review, narrow 8): a crown loop, a dome to a flared lip, 70 mm across the lip, 55 high, a 3 mm wall (outer profile down, inner profile back
        # up, so the cup is hollow), the clapper showing under the lip
        outer = [(0.0, 0.0), (4.0, -0.8), (9.0, -3.0), (14.0, -7.0), (18.0, -12.5), (21.0, -19.0), (23.0, -26.0), (25.0, -33.0), (28.0, -40.0), (32.0, -46.5), (35.0, -52.0), (35.0, -55.0)]
        inner = [(32.0, -55.0), (29.0, -49.5), (25.5, -43.0), (22.5, -36.0), (20.5, -29.0), (18.5, -22.0), (15.5, -15.5), (11.5, -10.0), (6.5, -6.0), (0.0, -3.0)]
        self.add("bell_brass", lathe(outer + inner, ub, end[0], bz + 2.0, 20), "brass", bev=None)
        self.add("bell_crown_loop", torus_d(ub, bz + 2.0 + 6.0, end[0], 5.5, 1.5), "brass", bev=None)
        self.add("bell_clapper", lathe([(0.0, 0.0), (4.0, -2.0), (7.0, -7.0), (4.0, -12.0), (0.0, -13.0)], ub, end[0], bz - 58.0, 10), "steel", bev=None)
        self.add("bell_clapper_rod", cyl_z(ub, end[0], bz - 58.0, bz - 3.0, 1.2, 6), "steel", bev=None)
        self.add("bell_clapper_bracket", bx(ub - 1.5, ub + 1.5, end[0] - 1.5, 20.0, bz - 48.0, bz - 46.0), "steel", bev=None)
        # note the fixed clapper bracket is a hint: the bell rings against a clapper on the frame (Judgement), not modelled further
        return {"uc": uc, "leaf": (lu0, lu1)}

    # ----------------------------------------------------------------------------------------------- the band above the doors (4.1a)
    def band(self):
        R = self.R
        D = R["door"]
        wp = self.kt["parts"]["window_frame"]["profiles"]
        slot_s = R["front"]["zones_u_mm"]["side_door"]          # 350..1294
        slot_d = R["front"]["zones_u_mm"]["shop_door"]          # 1294..2300
        u_in0, u_in1 = slot_d[0] + 50.0, slot_d[1] - 50.0       # 1344, 2250
        # transom (transom_t1, z from 2400) over the side door slot and between the shop door's jambs, as the window's runs on
        tz = [(p[0], p[1] + 2400.0) for p in wp["transom_t1"]["points"]]
        self.add("band_transom_side", bs.prism_dz(tz, slot_s[0], slot_s[1]), "white")
        self.add("band_transom_door", bs.prism_dz(tz, u_in0, u_in1), "white")
        # head (head_section 95 x 60 from z 2790) from the pilaster to the window frame's jamb
        hz = [(p[0], p[1] + 2790.0) for p in wp["head_section"]["points"]]
        self.add("band_head", bs.prism_dz(hz, slot_s[0], slot_d[1]), "white")
        # fanlight: one pane 6 mm at d 30 to 36 between the door frame's jambs, an ovolo bead round it
        fl = D["fanlight"]
        bd = [(p[0], -p[1]) for p in wp["glazing_bead_ovolo"]["points"]]
        self.add("fanlight_glass", bx(fl["u_mm"][0] - 2.0, fl["u_mm"][1] + 2.0, 30.0, 36.0, fl["z_mm"][0] - 4.0, fl["z_mm"][1] + 4.0), "glass", bev=None)
        V, F = joinery.sweep_frame(bd, fl["u_mm"][0], fl["z_mm"][0], fl["u_mm"][1], fl["z_mm"][1], -36.0)
        self.add("fanlight_bead", (V, [tuple(int(i) for i in f) for f in F]), "white", bev=None)
        # three toplights over the shop door: two 28 bars (toplight_bar_plan) at 1641.33 and 1952.67, glass and beads as the window's
        t = D["toplights_over_shop_door"]
        bp = wp["toplight_bar_plan"]["points"]
        for k, bar in enumerate(t["bars"]):
            self.add("band_bar_%d" % k, bs.prism_ud([(bar["centre"] + p[0], max(p[1], 1.0)) for p in bp], 2474.0, 2793.0), "white")
        for k, (a, b) in enumerate(t["panes"]):
            self.add("band_toplight_glass_%d" % k, bx(a - 4.0, b + 4.0, 30.0, 36.0, 2480.0, 2790.0), "glass", bev=None)
            V, F = joinery.sweep_frame(bd, a, 2480.0, b, 2790.0, -36.0)
            self.add("band_toplight_bead_%d" % k, (V, [tuple(int(i) for i in f) for f in F]), "white", bev=None)
        # the panel over the side door: backing board, the frame round the raised-and-fielded panel (stiles and rails 50), the field 844 wide
        p = D["panel_over_side_door"]
        (pu0, pu1), (pz0, pz1) = p["u_mm"], p["z_mm"]
        self.add("band_panel_board", bx(pu0, pu1, 0.0, 30.0, pz0, pz1), "white", bev=None)
        self.add("band_panel_stile_l", bx(pu0, p["field_u_mm"][0], 30.0, 70.0, pz0, pz1), "white")
        self.add("band_panel_stile_r", bx(p["field_u_mm"][1], pu1, 30.0, 70.0, pz0, pz1), "white")
        self.add("band_panel_rail_b", bx(p["field_u_mm"][0], p["field_u_mm"][1], 30.0, 70.0, pz0, pz0 + 50.0), "white")
        self.add("band_panel_rail_t", bx(p["field_u_mm"][0], p["field_u_mm"][1], 30.0, 70.0, pz1 - 50.0, pz1), "white")
        V, F = joinery.fielded_panel(p["field_u_mm"][0] - 8.0, pz0 + 50.0 - 8.0, p["field_u_mm"][1] + 8.0, pz1 - 50.0 + 8.0, -30.0, 14.0, 24.0, 8.0, margin=32.0)
        self.add("band_panel_field", (V, F), "white", bev=None)

    # ----------------------------------------------------------------------------------------------- the grille's day state (4.3): top rail, channel, fixing plates
    def grille_fixed(self):
        win = self.R["front"]["zones_u_mm"]["window"]            # 2300..5650
        d_plane = 36.0 + 100.0                                   # the lattice plane 100 in front of the glass front
        dd = (d_plane - 20.0, d_plane + 20.0)
        # top rail: a 40 x 40 box at the transom (z 2400 to 2440); the bottom channel: a 40 x 40 U, z 600 to 640
        self.add("grille_top_rail", bx(win[0], win[1], dd[0], dd[1], 2400.0, 2440.0), "black", bev=None)
        ch = [(dd[0], 600.0), (dd[1], 600.0), (dd[1], 640.0), (dd[1] - 4.0, 640.0), (dd[1] - 4.0, 604.0), (dd[0] + 4.0, 604.0), (dd[0] + 4.0, 640.0), (dd[0], 640.0)]
        self.add("grille_bottom_channel", bs.prism_dz(ch, win[0], win[1]), "black", bev=None)
        # fixing plates on the pilaster shaft (right end) and on the door frame's right jamb (left end): 60 x 110 x 6 with two bolts
        for nm, u_edge, side in (("r", win[1], +1), ("l", win[0], -1)):
            for zc in (2420.0, 620.0):
                ua, ub = (u_edge, u_edge + 60.0) if side > 0 else (u_edge - 60.0, u_edge)
                self.add("grille_plate_%s_%d" % (nm, int(zc)), bx(ua, ub, 100.0, 136.0, zc - 55.0, zc + 55.0), "black", bev=None)

    def lattice(self):
        """The night lattice as one model: flat bars 20 x 4 at 45 degrees, the diamond 120 across, rivets at every crossing, d 136 to 140 (+ 4)."""
        win = self.R["front"]["zones_u_mm"]["window"]
        u0, u1, z0, z1 = win[0] + 10.0, win[1] - 10.0, 640.0, 2400.0
        Vs, Fs = [], []

        def add(V, F):
            off = sum(len(v) for v in Vs)
            Vs.append(np.asarray(V, float))
            Fs.extend([tuple(int(i) + off for i in f) for f in F])
        sq = math.sqrt(0.5)
        for sgn, (da, db) in ((1, (136.0, 138.0)), (-1, (138.0, 140.0))):
            # lines z = z0 + sgn*(x - ux) + c, intercepts every 120 (diamond 120 across)
            cmin, cmax = -(u1 - u0) - 240.0, (z1 - z0) + (u1 - u0) + 240.0
            c = math.floor(cmin / 120.0) * 120.0
            while c <= cmax:
                # a line through (u0, z0 + c) with slope sgn if sgn>0, through (u0, z0 + c) down if sgn<0 (c measured at u0); clip to the rectangle
                if sgn > 0:
                    pa, pb = np.array([u0, z0 + c]), np.array([u1, z0 + c + (u1 - u0)])
                else:
                    pa, pb = np.array([u0, z0 + c]), np.array([u1, z0 + c - (u1 - u0)])
                seg = _clip_segment(pa, pb, u0, u1, z0, z1)
                if seg is not None and np.linalg.norm(seg[1] - seg[0]) > 10.0:
                    a, b = seg
                    t = (b - a) / np.linalg.norm(b - a)
                    nrm = np.array([-t[1], t[0]])
                    w = 10.0
                    corners = [a + nrm * w, b + nrm * w, b - nrm * w, a - nrm * w]
                    V = []
                    for dd in (da, db):
                        for p in corners:
                            V.append((p[0], -dd, p[1]))
                    F = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
                    add(V, F)
                c += 120.0
        # rivets at every crossing: points (u0' + 60 i, z0' + 60 j) with i + j even, standing 3 proud of the front bars
        rv = []
        ox = math.ceil((u0 - 0.0) / 60.0) * 60.0
        oz = math.ceil((z0) / 60.0) * 60.0
        i = 0
        x = ox
        while x <= u1:
            j = 0
            z = oz
            while z <= z1:
                if (i + j) % 2 == 0:
                    rv.append((x, z))
                z += 60.0
                j += 1
            x += 60.0
            i += 1
        n = 8
        for (x, z) in rv:
            V = []
            for dd in (140.0, 143.0):
                for k in range(n):
                    t = 2 * math.pi * k / n
                    V.append((x + 4.5 * math.cos(t), -dd, z + 4.5 * math.sin(t)))
            F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
            add(V, F)
        V = np.vstack(Vs)
        ob = bs.new_obj("grille_lattice", V, Fs)
        return ob, len(rv)

    # ----------------------------------------------------------------------------------------------- the side door (the door family's F1)
    def side_door(self):
        s = self.R["front"]["zones_u_mm"]["side_door"]          # [350, 1294]
        uc = (s[0] + s[1]) / 2.0                                # 822
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=F1_GLB)
        new = [o for o in bpy.data.objects if o not in before]
        out = []
        for o in new:
            if o.type != "MESH":
                continue
            o.parent = None
        for o in [o for o in new if o.type != "MESH"]:
            bpy.data.objects.remove(o, do_unlink=True)
        meshes = [o for o in new if o.type == "MESH" and o.name in bpy.data.objects]
        # F1 (glb: metres, x centred on its opening, y into the building from the brick face, z = bay z): bay u = uc + x*1000 (mirrored: uc - x*1000),
        # bay y = (y_glb - 0.2143) m  (d = 214.3 - y_F1)
        mir = True            # the door end is the viewer's left (Rita's): hinge on the shop-door side, knob on the pier side
        M = Matrix.Translation(((uc - BAY_MID) / 1000.0, -0.2143, 0.0)) @ Matrix.Scale(-1.0 if mir else 1.0, 4, (1, 0, 0))
        for o in meshes:
            me = o.data
            me.transform(o.matrix_world)       # the importer's own world matrix (Z-up conversion) is baked first
            o.matrix_world = Matrix.Identity(4)
            me.transform(M)
            if mir:
                bm = bmesh.new()
                bm.from_mesh(me)
                bmesh.ops.reverse_faces(bm, faces=bm.faces)
                bm.to_mesh(me)
                bm.free()
            me.update()
            out.append(o)
        # trim at the shop transom (z 2400) and to the slot (the door's frame is 1000 wide, the slot 944): the fillers hide the 28 either side
        zcut = 2.400
        lo, hi = (s[0] - BAY_MID) / 1000.0, (s[1] - BAY_MID) / 1000.0
        for o in out:
            clip_object(o, Vector((0, 0, zcut)), Vector((0, 0, 1)))
            clip_object(o, Vector((lo, 0, 0)), Vector((-1, 0, 0)))
            clip_object(o, Vector((hi, 0, 0)), Vector((1, 0, 0)))
        # the F1 paint: leaf and mouldings buttermilk, the frame its white joinery, as 3.1 built them
        for o in out:
            for slot in o.material_slots:
                nm = slot.material.name if slot.material else ""
                if nm.startswith("paint_dark_green") or nm == "paint_dark_green":
                    slot.material = self.mats["buttermilk"]
                elif nm.startswith("paint_white"):
                    slot.material = self.mats["white"]
        # 24.4 filler strips (the pilaster return, the pier's colour) each side, d 0 to 100, z 25 to 2400
        for nm, (a, b) in (("l", (s[0], s[0] + 24.4)), ("r", (s[1] - 24.4, s[1]))):
            self.add("side_filler_" + nm, bx(a, b, 0.0, 100.0, 25.0, 2400.0), "oxblood", bev=None)
        # F1's own frame jambs, put back (13 Oct, from the try 1 close review, fault 5): the leaf (u 403 to 1241) sits between fillers that end at 374.4 and 1269.6, which left two open
        # slots 28.6 wide and 100 deep onto the unlit space behind the front. White joinery (226, 224, 214), d 0 to 100, z 25 to 2400: 838 + 2 x 28.6 + 2 x 24.4 = 944
        for nm, (a, b) in (("l", (s[0] + 24.4, s[0] + 24.4 + 28.6)), ("r", (s[1] - 24.4 - 28.6, s[1] - 24.4))):
            self.add("side_jamb_" + nm, bx(a, b, 0.0, 100.0, 25.0, 2400.0), "white", bev=None)
        self.extra += out
        # the sealing strip where the sill's end stands 3 short of the pilaster's plinth (the kit's meets row), so no crack shows
        win = self.R["front"]["zones_u_mm"]["window"]
        self.add("sill_end_seal", bx(win[1] - 8.0, win[1], 0.0, 60.0, 525.0, 600.0), "white", bev=None)
        return out

    # ----------------------------------------------------------------------------------------------- the hall behind the side door (N3)
    def hall(self):
        """The side door leads to the stair for the flat above, not into the shop (13 Oct, from the try 1 street review, N3): a closed box over the side door's slot from the frame's
        back face (d 0) back HALL_DEPTH, plaster walls, ceiling and back wall at about half the room's brightness, a darker floor, no light of its own (unlit at night). Seen through
        the fanlight it hides the room's card, so no wall clock or pegboard shows over the buttermilk door."""
        s = self.R["front"]["zones_u_mm"]["side_door"]          # 350..1294
        u0, u1 = s[0], s[1]
        z0, z1 = HALL_Z
        t = 20.0
        dd = HALL_DEPTH
        self.add("hall_wall_l", bx(u0, u0 + t, -dd, 0.0, z0, z1), "hall_plaster", bev=None)
        self.add("hall_wall_r", bx(u1 - t, u1, -dd, 0.0, z0, z1), "hall_plaster", bev=None)
        self.add("hall_ceiling", bx(u0 + t, u1 - t, -dd, 0.0, z1 - t, z1), "hall_plaster", bev=None)
        self.add("hall_back", bx(u0 + t, u1 - t, -dd - t, -dd, z0, z1), "hall_plaster", bev=None)
        self.add("hall_floor", bx(u0 + t, u1 - t, -dd, 0.0, z0, z0 + 20.0), "hall_dark", bev=None)

    # ----------------------------------------------------------------------------------------------- finishing: the builder's objects to metres, UVs, materials
    def finish(self):
        obs = bs.finish(self.B, self.mats, BAY_MID)
        return obs


def _clip_segment(p0, p1, xmin, xmax, ymin, ymax):
    """Liang-Barsky clip of a segment to a rectangle; None if outside."""
    d = p1 - p0
    t0, t1 = 0.0, 1.0
    for p, q in ((-d[0], p0[0] - xmin), (d[0], xmax - p0[0]), (-d[1], p0[1] - ymin), (d[1], ymax - p0[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return None
        else:
            r = q / p
            if p < 0:
                if r > t1:
                    return None
                t0 = max(t0, r)
            else:
                if r < t0:
                    return None
                t1 = min(t1, r)
    return p0 + d * t0, p0 + d * t1


# ---------------------------------------------------------------------------------------------------------------- textured quads, balls, bracket
def quad_obj(name, u0, u1, z0, z1, d, flip=False):
    """A one-sided quad facing the street (-y) at depth d (mm), in metres, with UV 0..1 (u from the viewer's left)."""
    x0, x1 = (u0 - BAY_MID) / 1000.0, (u1 - BAY_MID) / 1000.0
    y = -d / 1000.0
    V = [(x0, y, z0 / 1000.0), (x1, y, z0 / 1000.0), (x1, y, z1 / 1000.0), (x0, y, z1 / 1000.0)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(V, [], [(0, 1, 2, 3)])
    me.update()
    uv = me.uv_layers.new(name="UVMap")
    for loop, (a, b) in zip(me.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        uv.data[loop.index].uv = (a, b)
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def image_material(name, path, alpha=False, rough=0.5, metal=0.0, orm=None, emissive=None, nonc=False, double=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = bpy.data.images.load(path, check_existing=True)
    t.image.colorspace_settings.name = "sRGB"
    nt.links.new(t.outputs["Color"], p.inputs["Base Color"])
    if alpha:
        nt.links.new(t.outputs["Alpha"], p.inputs["Alpha"])
        m.blend_method = "BLEND" if hasattr(m, "blend_method") else None
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    if orm:
        o = nt.nodes.new("ShaderNodeTexImage")
        o.image = bpy.data.images.load(orm, check_existing=True)
        o.image.colorspace_settings.name = "Non-Color"
        sep = nt.nodes.new("ShaderNodeSeparateColor")
        nt.links.new(o.outputs["Color"], sep.inputs["Color"])
        nt.links.new(sep.outputs["Green"], p.inputs["Roughness"])
        nt.links.new(sep.outputs["Blue"], p.inputs["Metallic"])
    return m


def set_fascia_uvs(ob, u0=295.0, u1=5705.0, z0=2850.0, z1=3400.0):
    """The 4.1 board on the fascia board's front face: u_tex from the viewer's left over u 295 to 5705, v_tex up over z 2850 to 3400 (the board is 5410 x 550)."""
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    layer = bm.loops.layers.uv.verify()
    for f in bm.faces:
        for l in f.loops:
            c = l.vert.co
            u = c.x * 1000.0 + BAY_MID
            z = c.z * 1000.0
            l[layer].uv = ((u - u0) / (u1 - u0), (z - z0) / (z1 - z0))
    bm.to_mesh(me)
    bm.free()


def make_balls_and_bracket(front, fasc_dir):
    """Rita's three balls on their wrought-iron bracket (4.1 ritas_three_balls): plate on the brick above the cornice, an arm 850 out, a hanger, a ring, three gilt balls."""
    import colorsys
    objs = []
    uc = 175.0           # the pilaster at the door end (viewer's left)
    z_arm = 3750.0
    plate = bs.new_obj("sign_plate", *bx(uc - 90.0, uc + 90.0, 0.0, 8.0, 3600.0, 3900.0))
    objs.append(("black_iron", plate))
    for k, (du, dz) in enumerate(((-65, 100), (65, 100), (-65, -100), (65, -100))):
        objs.append(("black_iron", bs.new_obj("sign_bolt_%d" % k, *cyl_d(uc + du, z_arm + dz, 8.0, 14.0, 6.0, 8))))
    objs.append(("black_iron", bs.new_obj("sign_arm", *bx(uc - 4.0, uc + 4.0, 8.0, 850.0, z_arm - 10.0, z_arm + 10.0))))
    # a diagonal brace from the plate's foot to the arm at d 600, and two scrolls (C curves in the d-z plane)
    brace = polyline_strip([(8.0, 3640.0), (200.0, 3690.0), (420.0, 3730.0), (600.0, z_arm - 10.0)], uc - 4.0, uc + 4.0, 20.0)
    objs.append(("black_iron", bs.new_obj("sign_brace", *brace)))
    for k, (cd, cz, r0, flip) in enumerate(((300.0, 3640.0, 70.0, 1), (700.0, 3690.0, 55.0, -1))):
        pts = [(cd + (r0 * (1 - t / 4.0)) * math.cos(t * 1.1 + (0 if flip > 0 else math.pi)), cz + (r0 * (1 - t / 4.0)) * math.sin(t * 1.1 + (0 if flip > 0 else math.pi))) for t in np.linspace(0.0, 4.0, 18)]
        objs.append(("black_iron", bs.new_obj("sign_scroll_%d" % k, *polyline_strip(pts, uc - 4.0, uc + 4.0, 20.0))))
    d_h = 570.0
    objs.append(("black_iron", bs.new_obj("sign_hanger", *cyl_z(uc, d_h, 3180.0, z_arm - 10.0, 5.0, 8))))
    # ring over the top balls (a small torus in the u-z plane)
    ring = []
    for k in range(16):
        t = 2 * math.pi * k / 16
        ring.append((uc + 28.0 * math.cos(t), 3150.0 + 28.0 * math.sin(t)))
    rv = [(p[0], -d_h - 5.0, p[1]) for p in ring] + [(p[0], -d_h + 5.0, p[1]) for p in ring]
    rf = [tuple(range(16))[::-1], tuple(range(16, 32))] + [(i, (i + 1) % 16, 16 + (i + 1) % 16, 16 + i) for i in range(16)]
    # (a flat ring plate rather than a torus: 10 thick, the inner hole left out is a flat disc)
    objs.append(("black_iron", bs.new_obj("sign_ring", np.array(rv), rf)))
    # the three balls: 0.26 m, centres (out 0.57; height 3.0 / 3.0 / 2.78 m; along the street +-0.14)
    balls = []
    cen = ((0.57, 3.0, -0.14), (0.57, 3.0, 0.14), (0.57, 2.78, 0.0))
    # three 10 mm rods from the ring to each ball's top (13 Oct, N4: the top balls stood 38 mm clear of the ring, the lower one 0.2 m): each rod runs from the ring's edge toward the ball's
    # top and 6 mm into the ball, so the balls hang from the ring
    ring_c = np.array([uc, 3150.0])
    for k, (out, h, along) in enumerate(cen):
        top = np.array([uc + along * 1000.0, h * 1000.0 + 130.0])
        dirv = (top - ring_c) / np.linalg.norm(top - ring_c)
        p0 = ring_c + dirv * 26.0
        p1 = top - dirv * 6.0
        objs.append(("black_iron", bs.new_obj("sign_rod_%d" % (k + 1), *rod((p0[0], d_h, p0[1]), (p1[0], d_h, p1[1]), 5.0, 8))))
    for k, (out, h, along) in enumerate(cen):
        bm = bmesh.new()
        bm.loops.layers.uv.new("UVMap")          # the layer must exist before calc_uvs has anywhere to write
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=20, radius=0.13, calc_uvs=True)       # with UVs (13 Oct, N4): the 4.1 face maps land
        me = bpy.data.meshes.new("sign_ball_%d" % (k + 1))
        bm.to_mesh(me)
        bm.free()
        for p in me.polygons:
            p.use_smooth = True
        # sphere uv from Blender: u round the ball, v pole to pole (the 4.1 maps are equirectangular)
        ob = bpy.data.objects.new("sign_ball_%d" % (k + 1), me)
        bpy.context.scene.collection.objects.link(ob)
        # model frame: x = (uc + along*1000 - 3000)/1000 across the bay (+x the viewer's right); out from the wall = -y
        ob.location = ((uc - BAY_MID) / 1000.0 + along, -out, h)
        base = os.path.join(fasc_dir, "signs", "ritas_three_balls", "ball_%d_" % (k + 1))
        m = image_material("gilt_ball_%d" % (k + 1), base + "basecolour.png", orm=base + "orm.png")
        me.materials.append(m)
        balls.append(ob)
    return objs, balls


GLASS_ROW_HEAD = {7: 18.132, 8: 17.025, 9: 15.918}       # row id -> street x of the ink's centre (WATCHES, JEWELLERY, LOANS)


def make_glass_rows(fasc_dir):
    """The 4.1 glass lettering rows (RGBA) on the glass: WATCHES, JEWELLERY, LOANS on the three lights' toplights, the 5 on the shop door's fanlight, the hours plate
    on the door's lower pane. Planes just behind the glass (applied inside it). Returns [(object, info)]."""
    man = json.load(open(os.path.join(fasc_dir, "manifest.json")))
    rows = {g["row"]: g for g in man["glass_lettering"] if g["shop"] == "ritas"}
    out = []
    for rid, g in sorted(rows.items()):
        w, h = g["size_mm"]
        pl = g["place"]
        xs = pl["x_street_m_of_ink_centre"]
        ink_c = (g["ink_box_in_tile_mm"][0] + g["ink_box_in_tile_mm"][2]) / 2.0
        base_from_bottom = pl["tile_baseline_from_tile_bottom_mm"]
        z_base = pl["z_baseline_m"] * 1000.0 - 100.0           # street z above the crown -> above the footway (crown + 0.10 = footway)
        d = 29.0
        if rid in GLASS_ROW_HEAD:
            # 13 Oct, from the try 1 street review, F2: WATCHES, JEWELLERY and LOANS at the head of the three main lights, the ink centred on each light (street x 18.132, 17.025,
            # 15.918 = u 2868, 3975, 5082), baseline 2250 above the footway, 4.1's sizes: the cap top is at about 2336, below the transom's glass edge at 2400, and each row fits inside
            # its light's 1037 of clear glass. The toplights stay clear: no bar, mullion or bead crosses a row
            xs = GLASS_ROW_HEAD[rid]
            z_base = 2250.0
        if rid == 10:
            xs = 19.203                                         # the shop door's centre (target 4.1a: moved from the side door's)
            z_base = 2200.0
        if rid == 24:
            xs = 19.203
            z_base = 1040.0 + base_from_bottom                  # the door's lower pane (the glazing bar at 1423 crosses 4.1's z 1.38)
            d = 39.0
        u_ink = BAY_MID + (18.0 - xs) * 1000.0                  # u from the viewer's left: street x 18.0 is the bay's middle
        u0 = u_ink - ink_c
        z0 = z_base - base_from_bottom
        ob = quad_obj("glass_row_%d_%s" % (rid, g["string"].split(" ")[0].lower()), u0, u0 + w, z0, z0 + h, d)
        path = os.path.join(fasc_dir, g["files"]["rgba"]["file"])
        m = image_material("glass_row_%d" % rid, path, alpha=True, rough=0.3)
        ob.data.materials.append(m)
        out.append((ob, {"id": g["id"], "string": g["string"], "u_mm": [round(u0, 1), round(u0 + w, 1)], "z_mm": [round(z0, 1), round(z0 + h, 1)], "d_mm": d}))
    return out


def to_metres(ob, mat=None):
    """An object built in mm in the bay frame: to metres at the bay's middle, UVs by cube projection, smooth by angle, one material."""
    M = Matrix.Scale(0.001, 4) @ Matrix.Translation((-BAY_MID, 0.0, 0.0))
    me = ob.data
    me.transform(M)
    me.update()
    bs.box_uv(me)
    me.shade_smooth()
    me.set_sharp_from_angle(angle=math.radians(35.0))
    if mat is not None:
        me.materials.clear()
        me.materials.append(mat)
    return ob


def bbox_mm(ob):
    me = ob.data
    n = len(me.vertices)
    co = np.empty(n * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3) * 1000.0
    co[:, 0] += BAY_MID
    return {"u": [float(co[:, 0].min()), float(co[:, 0].max())], "d": [float((-co[:, 1]).min()), float((-co[:, 1]).max())], "z": [float(co[:, 2].min()), float(co[:, 2].max())]}


def tri_count(ob):
    me = ob.data
    me.calc_loop_triangles()
    return len(me.loop_triangles)


def fascia_maps(base, out_dir):
    """The fascia board's two derived maps (written beside the build, not over the 4.1 files):
    ritas_basecolour_worn.png  the 4.1 base colour with the wear darkened in: x (1 - 0.25 x the strongest of the wear map's three masks), as the build had it in Blender's node tree;
    ritas_normal.png           a tangent-space normal map from ritas_height.png (16-bit, mean 0.526; 1 px a mm): h in mm = (H - 32768) / 25600, n = normalize(-dh/dcolumn, +dh/drow, 1)
                               (green up as glTF reads it), RGB = 127.5 (n + 1)
    Returns (colour path, normal path, info)."""
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    col = np.asarray(Image.open(base + "basecolour.png").convert("RGB")).astype(np.float32)
    wear = np.asarray(Image.open(base + "wear.png").convert("RGB")).astype(np.float32) / 255.0
    m = wear.max(axis=2)
    worn = np.clip(col * (1.0 - 0.25 * m)[..., None] + 0.5, 0, 255).astype(np.uint8)
    col_path = os.path.join(out_dir, "ritas_basecolour_worn.png")
    Image.fromarray(worn).save(col_path)
    h = np.asarray(Image.open(base + "height.png")).astype(np.float32)
    hmm = (h - 32768.0) / 25600.0
    dx = np.gradient(hmm, axis=1)
    dr = np.gradient(hmm, axis=0)
    n = np.stack([-dx, dr, np.ones_like(hmm)], axis=-1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    rgb = np.clip(127.5 * (n + 1.0) + 0.5, 0, 255).astype(np.uint8)
    nrm_path = os.path.join(out_dir, "ritas_normal.png")
    Image.fromarray(rgb).save(nrm_path)
    return col_path, nrm_path, {"wear_mean_mask": float(m.mean()), "relief_mm": [float(hmm.min()), float(hmm.max())], "normal_mean_rgb": [float(v) for v in rgb.reshape(-1, 3).mean(axis=0)]}


# ---------------------------------------------------------------------------------------------------------------- the build
def build_front(out_dir, work_dir, fasc_dir, paper_dir, log=print):
    """Builds the front; writes out_dir/ritas_front.glb and ritas_grille_night.glb and work_dir/front_members.json. Returns the info dict."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(work_dir, exist_ok=True)
    T = load_sw_target()
    F = Front(work_dir, T)
    F.kit_parts()
    door = F.shop_door()
    F.band()
    F.grille_fixed()
    F.side_door()
    F.hall()
    obs = F.finish()
    def srgb_of(ob):
        if not ob.data.materials or ob.data.materials[0] is None:
            return None
        bc = ob.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value
        f = lambda v: 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
        return [int(round(255 * f(bc[i]))) for i in range(3)]
    members = {ob.name: dict(bbox_mm(ob), material=ob.data.materials[0].name if ob.data.materials else None, base_srgb=srgb_of(ob)) for ob in obs}
    for ob in F.extra:
        members[ob.name] = dict(bbox_mm(ob), material=ob.data.materials[0].name if ob.data.materials else None, base_srgb=srgb_of(ob), group="side_door_F1")
    # the 4.1 fascia board on the board's face (13 Oct, from the try 1 street review, F1): the exported material carries the base colour with the wear darkening baked in, the orm and a
    # REAL tangent-space normal map made from the 4.1 height map. Try 1 linked a Bump node, which the glTF exporter turned into the 16-bit grey height map used as a normal map
    # (grey read as a normal points 55 degrees off the face and flips with the grain: the black streaks); a Mix node for the wear did not survive export either
    fb = F.B.get("fas_board")
    set_fascia_uvs(fb)
    base = os.path.join(fasc_dir, "fascias", "ritas", "ritas_")
    exp_dir = os.path.join(work_dir, "fascia_export")
    col_path, nrm_path, fa_info = fascia_maps(base, exp_dir)
    fm = image_material("fascia_ritas", col_path, orm=base + "orm.png")
    nt = fm.node_tree
    pb = nt.nodes["Principled BSDF"]
    ni = nt.nodes.new("ShaderNodeTexImage")
    ni.image = bpy.data.images.load(nrm_path, check_existing=True)
    ni.image.colorspace_settings.name = "Non-Color"
    nmap = nt.nodes.new("ShaderNodeNormalMap")
    nmap.space = "TANGENT"
    nmap.inputs["Strength"].default_value = 1.0
    nt.links.new(ni.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"], pb.inputs["Normal"])
    fb.data.materials.clear()
    fb.data.materials.append(fm)
    # the three balls and their bracket
    parts, balls = make_balls_and_bracket(F, fasc_dir)
    sign_objs = []
    for matkey, ob in parts:
        to_metres(ob, F.mats[matkey])
        members[ob.name] = dict(bbox_mm(ob), material=F.mats[matkey].name, group="hanging_sign")
        sign_objs.append(ob)
    for ob in balls:
        members[ob.name] = {"centre_m": [round(v, 4) for v in ob.location], "radius_m": 0.13, "group": "hanging_sign"}
    # the glass lettering rows
    rows = make_glass_rows(fasc_dir)
    glass_rows = []
    for ob, info in rows:
        members[ob.name] = dict(info, group="glass_rows")
        glass_rows.append(ob)
    # the OPEN sign (4.2: the plastic card, 200 x 110, face OPEN by day) inside the door glass at z 1500, hung by a suction cup
    uc = door["uc"]
    sign = quad_obj("door_sign_open", uc - 100.0, uc + 100.0, 1445.0, 1555.0, 37.0)
    spath = os.path.join(paper_dir, "K03a", "K03a_B_basecolour.png")
    sign.data.materials.append(image_material("door_sign", spath, alpha=True, rough=0.35))
    members[sign.name] = {"u": [uc - 100.0, uc + 100.0], "z": [1445.0, 1555.0], "d": [37.0, 37.0], "group": "door_sign", "image": spath}
    cup = bs.new_obj("door_sign_cup", *cyl_d(uc, 1548.0, 36.0, 38.0, 12.0, 12))
    to_metres(cup, F.mats["steel"])
    # the lattice (night grille) as its own object
    lat, nrivets = F.lattice()
    to_metres(lat, F.mats["black"])
    members["grille_lattice"] = dict(bbox_mm(lat), material="powder_black", group="grille_night", rivets=nrivets)
    day_objs = [o for o in bpy.data.objects if o.type == "MESH" and o is not lat]
    # FRN-07: the elevation drawn from the built meshes (u 350 to 5650, z 0 to 2850, 1 mm a pixel): every triangle of every part of the front, seen from the street
    elevation_mask(day_objs, os.path.join(work_dir, "front_elevation_mask.png"))
    # export: the front (day state) and the lattice (night)
    front_glb = os.path.join(out_dir, "ritas_front.glb")
    grille_glb = os.path.join(out_dir, "ritas_grille_night.glb")
    _export(day_objs, front_glb)
    _export([lat], grille_glb)
    info = {
        "front_glb": front_glb, "front_bytes": os.path.getsize(front_glb), "front_triangles": sum(tri_count(o) for o in day_objs),
        "grille_glb": grille_glb, "grille_bytes": os.path.getsize(grille_glb), "grille_triangles": tri_count(lat), "rivets": nrivets,
        "objects": len(day_objs), "uc_door": uc,
    }
    json.dump({"members": members, "info": info}, open(os.path.join(work_dir, "front_members.json"), "w"), indent=1)
    log("front: %d objects, %d triangles, %d bytes; grille %d triangles, %d bytes" % (info["objects"], info["front_triangles"], info["front_bytes"], info["grille_triangles"], info["grille_bytes"]))
    return info


HALL_NAMES = ("hall_wall_l", "hall_wall_r", "hall_ceiling", "hall_back", "hall_floor")


def elevation_mask(objs, path, u0=0.0, u1=6000.0, z0=0.0, z1=2850.0):
    """Draw every triangle of the front's parts (not the lettering planes, the sign or the hanging sign, nor the side door's hall, which would hide a defect behind the door) on a 1 mm
    raster of the elevation, u 0 to 6000 (the whole bay, 13 Oct: try 1 drew u 350 to 5650 and could not see the bay's outer 30 to 54 mm); white = a part is there. The gate stands a
    brick pier behind each pilaster (PIERS_X): those are drawn as 'the wall' in a second mask. Returns (path, path of the parts-only mask)."""
    from PIL import Image, ImageDraw
    w, h = int(u1 - u0), int(z1 - z0)
    im = Image.new("L", (w, h), 0)
    dr = ImageDraw.Draw(im)
    skip = ("glass_row", "door_sign", "sign_", "grille_lattice")
    for ob in objs:
        if ob.name.startswith(skip) or ob.name in HALL_NAMES:
            continue
        me = ob.data
        me.calc_loop_triangles()
        n = len(me.vertices)
        co = np.empty(n * 3)
        me.vertices.foreach_get("co", co)
        co = co.reshape(-1, 3)
        U = co[:, 0] * 1000.0 + BAY_MID - u0
        Z = (z1 - co[:, 2] * 1000.0)
        for t in me.loop_triangles:
            a, b, c = t.vertices
            dr.polygon([(U[a], Z[a]), (U[b], Z[b]), (U[c], Z[c])], fill=255, outline=255)
    parts_only = os.path.splitext(path)[0] + "_parts.png"
    im.save(parts_only)
    for (xa, xb) in PIERS_X:
        ua, ub = xa * 1000.0 + BAY_MID - u0, xb * 1000.0 + BAY_MID - u0
        dr.rectangle([ua, 0, ub, h], fill=255)
    im.save(path)
    return path, parts_only


def _export(objs, path):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_apply=True, export_materials="EXPORT",
                              export_cameras=False, export_lights=False, export_yup=True)


if __name__ == "__main__":
    scratch = os.environ.get("LEDGER_SW_SCRATCH", "/home/user/ledger-scratch")
    out = os.path.join(REPO, "production", "assets", "cloud-week", "shop-windows")
    build_front(out, os.path.join(scratch, "shop-windows"), os.path.join(scratch, "shop-windows", "fascias"), os.path.join(scratch, "shop-windows", "paper"))
