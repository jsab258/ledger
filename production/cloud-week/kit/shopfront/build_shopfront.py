"""The shopfront's parts and Rita's assembled front, built by script from target.json alone (cloud week 42, unit 3.2).

    /home/user/.bpyenv/bin/python build_shopfront.py [--shop ritas] [--only pilaster,console,...] [--out-dir DIR] [--npz-dir DIR]

Reads production/cloud-week/targets/shopfronts/target.json (target_drawing.py, the check's reference, is not read here).
Writes, each under 1 MB,
    production/assets/cloud-week/shopfront/pilaster.glb, console.glb, fascia_board.glb, cornice.glb, sill.glb,
        stallriser.glb, window_frame.glb          one model per part (Rita's variants: panel pilaster, scroll console,
                                                    panel stallriser, T1 window frame)
    production/assets/cloud-week/shopfront/shopfront_ritas.glb      Rita's front (bay 2, the model) assembled from them
    kit/shopfront/build/<name>.npz and parts.json                    the named parts, in metres, for check_shopfront.py

Frame and pivots. Everything is worked in the target's own frame, millimetres: u across the bay from the viewer's left
party-wall line, d out from the wall face (Blender y = -d, the street toward -y) and z up from the footway. A model is then
metres, z up, scale 1, the street toward -y, with the pivot on the street datum (the existing shopfront kit's convention,
production/art/shopfront-kit/README.md): y = 0 the wall face, z = 0 the footway, x = 0 at the middle of the piece's width
(pilaster and console at their slot's middle u 175, the others at the bay's middle for the full-width ones, the sill,
stallriser and window frame at the middle of the window zone u 3975); the assembly's x = 0 is the bay's middle (u 3000).
So every part drops into the bay with a shift along x only (PLACEMENT below).

How the pieces are made: closed solids by construction, no hidden coplanar faces (members that overlap sit 0.3 to 12 mm
into what they stand on, never in one plane), booleans only for the grooves of the console's sides and the downpipe's
chase; profiles are the target's own point lists (smoothed arcs are the target's own points); smooth shading by angle (35
degrees), arrises 1 mm chamfered on joinery; UVs by cube projection at real scale (1 UV unit = 1 m); materials named by
what they are with the target's paint colours (shop's paints[]), roughness and metal.
"""
import argparse
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "shopfronts", "target.json")
ASSET_DIR = os.path.join(REPO, "production", "assets", "cloud-week", "shopfront")
NPZ_DIR = os.path.join(HERE, "build")

import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Matrix  # noqa: E402
from shapely.geometry import LineString, Point, Polygon, box as sbox  # noqa: E402
from shapely.geometry.polygon import orient  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

import blender_parts  # noqa: E402
import joinery  # noqa: E402
import departures  # noqa: E402

BEVEL = 1.0           # mm: the chamfer that eases a timber arris (the target: eased 1 to 2.5 by repainting)
SEAT_EMBED = 12.0     # mm a frame member's foot goes into the sill (it is scribed down to the weathering)


# ------------------------------------------------------------------ the target
def load_target():
    """target.json with try 2's departures written into a copy (departures.py); the target file is untouched."""
    return departures.apply(json.load(open(TARGET_JSON, encoding="utf-8")))


def shop_of(T, ident):
    for s in T["shops"]:
        if s["id"] == ident:
            return s
    raise SystemExit("unknown shop " + ident)


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


def setup_materials(T, shop):
    """paint_<colour> per shop role (named by what they are), glass. Colours, roughness, metal from target.json's paints."""
    s = shop_of(T, shop)
    mats = {}
    for role, key in (("oxblood", "pilaster"), ("white", "window_frame")):
        pid = s["paints"][key]
        p = T["paints"][pid]
        mats[role] = make_material("paint_" + pid, p["srgb"], p["rough"], p["metal"])
    mats["glass"] = make_material("glass", (121, 131, 139), 0.05, 0.0, 1.0, 1.5)
    return mats


# ------------------------------------------------------------------ meshes (mm, bay frame: x = u, y = -d, z)
def new_obj(name, V, F):
    return blender_parts.make_object(name, np.asarray(V, float), [tuple(int(i) for i in f) for f in F])


def prism_dz(profile, u0, u1, y_off=0.0):
    """A (d, z) profile extruded along u from u0 to u1. Returns (V, F)."""
    P = np.asarray(profile, float)
    n = len(P)
    V = np.zeros((2 * n, 3))
    for k, u in enumerate((u0, u1)):
        V[k * n:(k + 1) * n, 0] = u
        V[k * n:(k + 1) * n, 1] = -P[:, 0] + y_off
        V[k * n:(k + 1) * n, 2] = P[:, 1]
    F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return V, F


def prism_ud(profile, z0, z1):
    """A (u, d) plan profile extruded along z. Returns (V, F)."""
    P = np.asarray(profile, float)
    n = len(P)
    V = np.zeros((2 * n, 3))
    for k, z in enumerate((z0, z1)):
        V[k * n:(k + 1) * n, 0] = P[:, 0]
        V[k * n:(k + 1) * n, 1] = -P[:, 1]
        V[k * n:(k + 1) * n, 2] = z
    F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return V, F


def box(u0, u1, d0, d1, z0, z1):
    return prism_ud([(u0, d0), (u1, d0), (u1, d1), (u0, d1)], z0, z1)


def poly_prism_u(poly_dz, u0, u1):
    """A (d, z) polygon (shapely exterior) extruded along u."""
    pts = list(poly_dz)
    if np.allclose(pts[0], pts[-1]):
        pts = pts[:-1]
    return prism_dz(pts, u0, u1)


def loft_rings(rings):
    """A solid through rings (each a list of 3D points, same count, a closed convex-ish cross-section) with flat end caps.
    Two rings at one height (a ledge) are set 0.01 mm apart, so that no strip between them has zero area."""
    R = [np.asarray(r, float).copy() for r in rings]
    for k in range(1, len(R)):
        if abs(R[k][0, 2] - R[k - 1][0, 2]) < 1e-9:
            R[k][:, 2] += 0.01
    n = len(R[0])
    V = np.vstack(R)
    F = [tuple(range(n))[::-1], tuple(range(n * (len(R) - 1), n * len(R)))]
    for k in range(len(R) - 1):
        a, b = k * n, (k + 1) * n
        for i in range(n):
            j = (i + 1) % n
            F.append((a + i, a + j, b + j, b + i))
    return V, F


def sweep_path(profile_tz, path_fn, y_floor=None):
    """A closed profile (t, z) swept along an open path. path_fn(t) gives the 3D points (x, y, z-free) of the path offset
    outward by t: returns a list of (x, y) points. Strips join consecutive profile points; the two ends are capped.
    Coincident points (degenerate strips) are merged afterwards."""
    P = np.asarray(profile_tz, float)
    n = len(P)
    rings = []
    for t, z in P:
        xy = np.asarray(path_fn(t), float)
        rings.append(np.column_stack([xy[:, 0], xy[:, 1], np.full(len(xy), z)]))
    m = len(rings[0])
    V = np.vstack(rings)
    F = []
    for i in range(n):
        j = (i + 1) % n
        for s in range(m - 1):
            F.append((i * m + s, i * m + s + 1, j * m + s + 1, j * m + s))
    F.append(tuple(i * m for i in range(n))[::-1])                 # start cap
    F.append(tuple(i * m + m - 1 for i in range(n)))              # end cap
    return V, F


def merge_doubles(V, F, dist=1e-4):
    """Weld coincident vertices and drop faces that collapse (used for sweeps whose profile touches the wall line)."""
    V = np.asarray(V, float)
    key = np.round(V / dist).astype(np.int64)
    idx, remap, uniq = {}, np.zeros(len(V), int), []
    for i, k in enumerate(map(tuple, key)):
        if k not in idx:
            idx[k] = len(uniq)
            uniq.append(V[i])
        remap[i] = idx[k]
    out = []
    for f in F:
        g = []
        for i in f:
            r = int(remap[i])
            if not g or g[-1] != r:
                g.append(r)
        if len(g) > 1 and g[0] == g[-1]:
            g.pop()
        if len(set(g)) >= 3:
            out.append(tuple(g))
    return np.array(uniq), out


def hf_slab(us, zs, D, d_back=0.0):
    """A slab whose back face is the plane d = d_back and whose front is the height field d = D[i][j] over the grid (us, zs):
    one closed mesh. D is (len(us), len(zs))."""
    us, zs, D = list(us), list(zs), np.asarray(D, float)
    nu, nz = len(us), len(zs)
    V = [(us[i], -D[i][j], zs[j]) for i in range(nu) for j in range(nz)]
    vid = lambda i, j: i * nz + j
    bk = {}
    for name, (i, j) in {"bl": (0, 0), "br": (nu - 1, 0), "tr": (nu - 1, nz - 1), "tl": (0, nz - 1)}.items():
        V.append((us[i], -d_back, zs[j]))
        bk[name] = len(V) - 1
    F = []
    for i in range(nu - 1):
        for j in range(nz - 1):
            F.append((vid(i, j), vid(i + 1, j), vid(i + 1, j + 1), vid(i, j + 1)))      # front
    F.append((bk["bl"], bk["tl"], bk["tr"], bk["br"]))                                   # back
    # bottom (z = zs[0]): back-left, front along u, back-right
    F.append(tuple([bk["bl"]] + [vid(i, 0) for i in range(nu)] + [bk["br"]]))
    F.append(tuple([bk["tl"]] + [vid(i, nz - 1) for i in range(nu)] + [bk["tr"]])[::-1])
    F.append(tuple([bk["bl"]] + [vid(0, j) for j in range(nz)] + [bk["tl"]])[::-1])
    F.append(tuple([bk["br"]] + [vid(nu - 1, j) for j in range(nz)] + [bk["tr"]]))
    return np.array(V, float), F


def front_grid(breaks_u, breaks_z, fu, fz, base):
    """D[i][j] = base(z) - min(fu(u), fz(z)) for the pocket depth functions fu, fz (0 outside the pocket)."""
    D = np.zeros((len(breaks_u), len(breaks_z)))
    for i, u in enumerate(breaks_u):
        for j, z in enumerate(breaks_z):
            D[i][j] = base(z) - min(fu(u), fz(z))
    return D


def lerp_table(pts):
    """A piecewise-linear function from (x, y) points (x ascending)."""
    X = [p[0] for p in pts]
    Y = [p[1] for p in pts]
    return lambda x: float(np.interp(x, X, Y))


def uniq_sorted(vals, tol=1e-6):
    out = []
    for v in sorted(vals):
        if not out or v - out[-1] > tol:
            out.append(float(v))
    return out


# ------------------------------------------------------------------ bpy operations
def _drop(ob):
    me = ob.data
    bpy.data.objects.remove(ob, do_unlink=True)
    bpy.data.meshes.remove(me)


def bool_op(ob, V, F, op):
    other = blender_parts.make_object("_cutter", np.asarray(V, float), [tuple(int(i) for i in f) for f in F])
    m = ob.modifiers.new("b", "BOOLEAN")
    m.operation, m.object, m.solver = op, other, "EXACT"
    with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob]):
        bpy.ops.object.modifier_apply(modifier=m.name)
    _drop(other)
    return ob


def bevel_obj(ob, width, min_angle=50.0):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    lim = math.radians(min_angle)
    sel = [e for e in bm.edges if len(e.link_faces) == 2 and e.calc_face_angle(0.0) >= lim]
    if sel:
        bmesh.ops.bevel(bm, geom=sel, offset=width, segments=1, affect="EDGES", clamp_overlap=True)
    bm.to_mesh(ob.data)
    bm.free()


def box_uv(me):
    """Cube projection: each face takes the pair of axes across its dominant normal; metres, one UV unit = 1 m."""
    bm = bmesh.new()
    bm.from_mesh(me)
    layer = bm.loops.layers.uv.verify()
    for f in bm.faces:
        n = f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for l in f.loops:
            c = l.vert.co
            l[layer].uv = (c.x, c.z) if ax == 1 else ((c.y, c.z) if ax == 0 else (c.x, c.y))
    bm.to_mesh(me)
    bm.free()


def mirror_u(ob, c):
    """Mirror an object about the plane u = c (mm), keeping the outward normals."""
    me = ob.data
    n = len(me.vertices)
    co = np.empty(n * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    co[:, 0] = 2 * c - co[:, 0]
    me.vertices.foreach_set("co", co.ravel())
    me.update()
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()


def shift_u(ob, du):
    ob.data.transform(Matrix.Translation((du, 0, 0)))
    ob.data.update()


# ------------------------------------------------------------------ a part set builder
class Builder:
    """Collects the objects of one model. Objects are named <group><tag>_<piece>; tag is '' in a part file and L or R in the assembly."""

    def __init__(self, T, shop):
        self.T, self.shop = T, shop
        self.S = shop_of(T, shop)
        self.P = T["parts"]
        self.B = T["bay"]
        self.objs = []
        self.meta = {}

    def add(self, name, VF, mat, bev=BEVEL, min_angle=50.0):
        ob = new_obj(name, VF[0], VF[1])
        self.meta[ob.name] = (mat, bev, min_angle)
        self.objs.append(ob)
        return ob

    def get(self, name):
        for o in self.objs:
            if o.name == name:
                return o
        raise KeyError(name)

    # ---------------------------------------------------------- pilaster (panel variant, Rita's), the left pier
    def pilaster(self, tag=""):
        pil = self.P["pilaster"]
        d = pil["dims"]
        pr = pil["profiles"]
        mat = "oxblood"
        n = lambda s: "pil%s_%s" % (tag, s)
        W = d["slot_width"]                                   # 350
        sh0, sh1 = d["shaft_u_in_slot"]                       # 30, 320
        SP, PP = d["shaft_proud"], d["plinth_proud"]          # 140, 180
        PT, NK, TOP = d["plinth_top_z"], d["neck_z"], d["capital_top_z"]
        chase = d["downpipe_chase"]
        cw, cd = chase["width"] / 2.0, chase["from_d"]        # 38, 50

        def chase_cut(ob, z0, z1):
            """the downpipe's chase through the plinth and the capital at the party line (u 0 on this pier)"""
            V, F = box(-1.0, cw, cd, 400.0, z0, z1)
            bool_op(ob, V, F, "DIFFERENCE")

        # -- plinth body, z 0 to 520: a skirting 120, stiles 50, a sunk panel (12) with a quarter-round bead 12 on its sides
        #    and 45 degree sticking top and bottom (plinth_panel_side_through_field)
        sunk = PP - 168.0                                     # 12: the field's floor stands at d 168
        th = [math.radians(a) for a in range(0, 91, 15)]
        bead_x = [sunk * math.sin(t) for t in th]
        # the bead's centre is in the wall's angle: its surface is d = 168 + sqrt(12^2 - x^2), x from the stile's edge
        gu = lerp_table([(x, sunk - math.sqrt(max(0.0, sunk ** 2 - x ** 2))) for x in bead_x] + [(1e6, sunk)])
        sticking = lerp_table([(0.0, 0.0), (sunk, sunk), (1e6, sunk)])
        pu0, pu1 = 50.0, W - 50.0
        pz0, pz1 = 120.0, 520.0

        def fu(u):
            return 0.0 if (u <= pu0 or u >= pu1) else gu(min(u - pu0, pu1 - u))

        def fz(z):
            return 0.0 if (z <= pz0 or z >= pz1) else sticking(min(z - pz0, pz1 - z))
        us = uniq_sorted([0, W, pu0, pu1] + [pu0 + x for x in bead_x] + [pu1 - x for x in bead_x])
        zs = uniq_sorted([0, 120, 132, 508, 520])
        D = front_grid(us, zs, fu, fz, lambda z: PP)
        ob = self.add(n("plinth_body"), hf_slab(us, zs, D), mat)
        chase_cut(ob, -1.0, 521.0)
        # -- plinth cap, z 520 to 600: plinth_cap_side across the slot
        ob = self.add(n("plinth_cap"), prism_dz(pr["plinth_cap_side"]["points"], 0.0, W), mat)
        chase_cut(ob, 519.0, 601.0)
        # -- the backing core: as deep as the window frame's jamb, from the shaft's party side (u 30) to the slot's free edge
        #    (350), plinth top to neck, so the frames close against it; the party-side strip stays open for the downpipe
        core_d = d["relief_beside_frames"]["frame_fronts_d"]["T1"]           # 95
        self.add(n("core"), box(sh0, W, 0.0, core_d, PT, NK), mat)
        # -- the shaft, panelled: stiles 45, rails 80 and 110, the field sunk 12 behind a 10 cove (shaft_panel_plan), on the core
        plan = pr["shaft_panel_plan"]["points"]
        arc = sorted([(p[0], p[1]) for p in plan if 265.0 <= p[0] <= 275.0 and p[1] < 140.0], key=lambda p: -p[0])
        cx = [(275.0 - p[0], 140.0 - p[1]) for p in arc]      # (x in from the field's edge, depth below 140): (0, 2) (1.5, 7.1) (5, 11) (10, 12)
        cove = lerp_table([(-0.5, 0.0)] + cx + [(1e6, cx[-1][1])])
        fx0, fx1 = 75.0, 275.0
        fz0, fz1 = d["shaft_bottom_rail_top_z"], d["shaft_top_rail_bottom_z"]     # 740, 2430

        def su(u):
            return 0.0 if (u <= fx0 - 0.5 or u >= fx1 + 0.5) else cove(min(u - fx0, fx1 - u))

        def sz(z):
            return 0.0 if (z <= fz0 - 0.5 or z >= fz1 + 0.5) else cove(min(z - fz0, fz1 - z))
        us = uniq_sorted([sh0, sh1, fx0 - 0.5, fx1 + 0.5] + [fx0 + x for x, _ in cx] + [fx1 - x for x, _ in cx])
        zs = uniq_sorted([PT, NK, fz0 - 0.5, fz1 + 0.5] + [fz0 + x for x, _ in cx] + [fz1 - x for x, _ in cx])
        D = front_grid(us, zs, su, sz, lambda z: SP)
        self.add(n("shaft"), hf_slab(us, zs, D, d_back=core_d), mat)
        # -- the base ogee: the kit's moulding made 15 proud, 60 high, returned on both sides of the shaft (the free side's leg
        #    stops at the core's front)
        og = pr["base_ogee"]["points"]
        prof = [(p[0] - SP, p[1]) for p in og]

        def path(t):
            return [(sh0 - t, -2.0), (sh0 - t, -(SP + t)), (sh1 + t, -(SP + t)), (sh1 + t, -core_d)]
        V, F = merge_doubles(*sweep_path(prof, path))
        self.add(n("ogee"), (V, F), mat, bev=None)               # its own profile is the moulding: no further chamfer
        # -- the capital: astragal, fillet, die, hollow flare, abacus, ovolo top, lofted from capital_side (z local from the neck)
        cap = pr["capital_side"]["points"]
        front = [p for p in cap[1:] if p[0] > 0.0]            # from (140, 0) to (172, 310)
        uc = W / 2.0
        elev = {q["name"]: q["pts"] for q in pil["variants"]["panel"]["elevation"]}
        ast, fil, die = elev["astragal"], elev["neck_fillet"], elev["die"]
        w_ast = (ast[1][0] - ast[0][0]) / 2.0                 # 157: round, 12 proud all round
        w_fil = (fil[1][0] - fil[0][0]) / 2.0                 # 148
        w_die = (die[1][0] - die[0][0]) / 2.0                 # 145
        w_top = (elev["abacus"][1][0] - elev["abacus"][0][0]) / 2.0     # 175
        z_ast, z_fil, z_die = ast[2][1] - NK, fil[2][1] - NK, die[2][1] - NK   # 24, 34, 154
        z_fl1 = elev["flare"][2][1] - NK                      # 244

        def halfw(dv, z):
            if z < z_ast or (z == z_ast and dv <= SP + 1e-9):
                return w_die + (dv - SP)
            if z <= z_fil:
                return w_fil if dv > w_die else w_die
            if z <= z_die:
                return w_die
            if z <= z_fl1:
                return w_die + (w_top - w_die) * (z - z_die) / (z_fl1 - z_die)
            return w_top
        rings = []
        for dv, z in front:
            w = halfw(dv, z)
            zz = NK + z
            # each ring is the rectangle with the downpipe's chase cut from its party-side corner (u < 38, d > 50): an L
            rings.append([(uc - w, 0.0, zz), (uc + w, 0.0, zz), (uc + w, -dv, zz), (cw, -dv, zz), (cw, -cd, zz), (uc - w, -cd, zz)])
        self.add(n("capital"), loft_rings(rings), mat)
        # -- the die's tablet: 170 x 80, 8 proud (elevation: u 90..260, z 2594..2674)
        tz = elev["die_tablet"]
        dd = d["capital_die_d"]
        self.add(n("tablet"), box(tz[0][0], tz[1][0], dd - 0.5, dd + d["die_tablet_proud"], tz[0][1], tz[2][1]), mat, bev=d.get("die_tablet_chamfer", BEVEL))
        return self

    # ---------------------------------------------------------- console (scroll), centred on slot middle u 175
    def console(self, tag="", uc=175.0):
        C = self.P["console"]
        d = C["dims"]
        pr = C["profiles"]
        mat = "oxblood"
        z0 = d["z_bottom"]
        n = lambda s: "con%s_%s" % (tag, s)
        sil = pr["side_silhouette"]["points"]
        hw, ch = d["width"] / 2.0, d["side_chamfer"]
        front = sil[1:-1]                                      # from (172, 0) to (205, 550)
        rings = []
        for dv, z in front:
            zz = z0 + z
            rings.append([(uc - hw, 0.0, zz), (uc + hw, 0.0, zz), (uc + hw, -(dv - ch), zz), (uc + hw - ch, -dv, zz),
                          (uc - hw + ch, -dv, zz), (uc - hw, -(dv - ch), zz)])
        ob = self.add(n("body"), loft_rings(rings), mat, bev=None)
        # D2 the side spirals: raised fillets 10 wide standing 6 proud on each side, and the eye bosses 8 proud (4 into the body)
        fd = d["side_fillets"]
        sides = (("r", (uc + hw - 0.4, uc + hw + fd["proud"]), (uc + hw - 0.7, uc + hw + fd["eye_boss_proud"])),
                 ("l", (uc - hw - fd["proud"], uc - hw + 0.4), (uc - hw - fd["eye_boss_proud"], uc - hw + 0.7)))
        for key, bk, tag_ in (("volute_upper_spiral", "eye_boss_upper", "u"), ("volute_lower_spiral", "eye_boss_lower", "l")):
            line = LineString([(p[0], z0 + p[1]) for p in pr[key]["points"]])
            rib = line.buffer(fd["width"] / 2.0, cap_style=2, join_style=1, resolution=3)
            geoms = [rib] if rib.geom_type == "Polygon" else list(rib.geoms)
            # the board's face is d 120: what lies behind d 121 is hidden by the board (and would run into it), so it is not built
            keep = sbox(121.0, -1e5, 1e5, 1e5).difference(sbox(-1e5, -1e5, 133.0, z0 + 42.0))      # and clear of the board's bed mould (d 132, z to 40)
            boss = Polygon([(p[0], z0 + p[1]) for p in pr[bk]["points"]]).buffer(0).intersection(keep)
            boss = list(orient(boss, 1.0).exterior.coords)[:-1]
            for side, (ua, ub), (ba, bb) in sides:
                gi = 0
                for g in geoms:
                    g = g.intersection(keep)
                    for gg in ([g] if g.geom_type == "Polygon" else list(g.geoms)):
                        if gg.is_empty or gg.geom_type != "Polygon":
                            continue
                        self.add(n("fillet_%s%d_%s" % (tag_, gi, side)), poly_prism_u(list(orient(gg, 1.0).exterior.coords), ua, ub), mat, bev=None)
                        gi += 1
                self.add(n("boss_%s_%s" % (tag_, side)), prism_dz(boss, ba, bb), mat, bev=None)
        # D3 the acanthus leaf on the face: raised rib, chevron veins, domed lobes
        self.add(n("leaf"), self._leaf(C, uc, z0, front), mat, bev=None)
        return self

    def _leaf(self, C, uc, z0, front):
        """D3, the acanthus pendant on the console's face (REVIEW-v1-close fault 2): a 3 mm base that rolls off to nothing at the outline,
        each lobe domed on its own (12 at its middle, 0 at its veins), a vein 3 wide and 2 deep from each notch up and inward to the
        rib at 35 degrees (a chevron), a raised rib 8 wide and 4 proud the length of the leaf, each lobe tip turned 6 forward, and the
        head carried 50 up over the upper roll (the outline's head_extension). One skin on the face (its edge 0.3 inside it) and
        one 6 inside the body, same grid, closed along the edge."""
        ld = C["dims"]["leaf"]
        L = ld["try2"]
        outline = C["profiles"]["leaf_outline"]["points"]
        right = sorted([tuple(p) for p in outline if p[0] >= 0.0 and p[1] < 419.9], key=lambda p: p[1]) + [tuple(p) for p in ld["head_extension"]]
        hwz = lerp_table([(p[1], p[0]) for p in right])
        F_of_z = lerp_table([(p[1], p[0]) for p in front])
        zlo, zhi = right[0][1], right[-1][1]
        rl = LineString([(p[0], p[1]) for p in right])
        notches, tips = [], []
        for i in range(1, len(right) - 1):
            a, b, c = np.array(right[i - 1]), np.array(right[i]), np.array(right[i + 1])
            cr = (b - a)[0] * (c - b)[1] - (b - a)[1] * (c - b)[0]
            if b[1] < 419.0 and b[0] > 5.0:
                (notches if cr > 0 else tips).append((float(b[0]), float(b[1])))
        tang = math.tan(math.radians(L["vein_angle_deg"]))
        veins = [LineString([(wn - 1.0, zn), (L["rib_w"] / 2.0, zn + (wn - L["rib_w"] / 2.0) * tang)]) for wn, zn in notches]
        zs = list(np.arange(zlo, zhi, 5.0)) + [p[1] for p in right] + [zhi]
        zs = uniq_sorted(zs, 0.6)
        nc = 25
        S = np.linspace(-1.0, 1.0, nc)
        D, R, rp, rw = L["dome_mm"], L["dome_radius"], L["rib_proud"], L["rib_w"] / 2.0
        base = 3.0

        def height(u, z, w):
            u = abs(u)
            if u >= w - 1e-6:
                return 0.0
            P = Point(u, z)
            d_out = P.distance(rl)
            d_vein = min(v.distance(P) for v in veins) if veins else 1e9
            e = min(d_out, d_vein)
            h = base * min(1.0, d_out / 3.0) + (D - base) * (1.0 - (1.0 - min(1.0, e / R)) ** 2) * min(1.0, d_out / 3.0)
            h -= L["vein_depth"] * min(1.0, max(0.0, (2.2 - d_vein) / 1.0))
            h = max(h, 1.0 if d_out > 3.0 else 0.0)
            if u < rw:
                h += rp * (1.0 - (u / rw) ** 2) * min(1.0, max(0.0, (zhi - 12.0 - z) / 20.0))
            for tu, tz in tips:
                h += L["tip_forward"] * math.exp(-((u - tu) ** 2 + (z - tz) ** 2) / 81.0) * min(1.0, d_out / 0.1 + 0.0) * (1.0 if d_out < 6.0 else 0.0)
            return h

        V = []
        for z in zs:
            w = max(hwz(z), 0.4)
            for s in S:
                u = w * s
                h = height(u, z, w)
                V.append((uc + u, -(F_of_z(z) + h - 0.3), z0 + z))
        nr = len(zs)
        idx = lambda r, c: r * nc + c
        F = []
        for r in range(nr - 1):
            for c in range(nc - 1):
                F.append((idx(r, c), idx(r, c + 1), idx(r + 1, c + 1), idx(r + 1, c)))
        # the back: the edge loop dropped to a flat plane d 120 inside the body (the body's front is never nearer than 140), closed by a
        # constrained triangulation of the loop; the wall between the loop and its drop is hidden inside the console
        loop = [idx(r, 0) for r in range(nr)] + [idx(nr - 1, c) for c in range(1, nc)] + [idx(r, nc - 1) for r in range(nr - 2, -1, -1)] + [idx(0, c) for c in range(nc - 2, 0, -1)]
        base_i = len(V)
        for i in loop:
            V.append((V[i][0], -120.0, V[i][2]))
        m = len(loop)
        cu, cz = uc, z0 + 0.5 * (zlo + zhi)
        for k in range(m):
            a_, b_ = loop[k], loop[(k + 1) % m]
            quad = (a_, b_, base_i + (k + 1) % m, base_i + k)
            Q = [np.array(V[i]) for i in quad]
            nrm = np.cross(Q[1] - Q[0], Q[2] - Q[0])
            mid = (Q[0] + Q[1] + Q[2] + Q[3]) / 4.0
            if nrm[0] * (mid[0] - cu) + nrm[2] * (mid[2] - cz) < 0:
                quad = quad[::-1]
            F.append(quad)
        poly = Polygon([(V[i][0], V[i][2]) for i in loop]).buffer(0)
        key = {(round(V[base_i + k][0], 3), round(V[base_i + k][2], 3)): base_i + k for k in range(m)}
        import shapely
        for tri in shapely.constrained_delaunay_triangles(poly).geoms:
            ids = [key[(round(x, 3), round(y, 3))] for x, y in list(tri.exterior.coords)[:3]]
            A_, B_, C_ = (np.array(V[i]) for i in ids)
            if np.cross(B_ - A_, C_ - A_)[1] > 0:        # the back faces the wall: its normal points toward +y... fixed below by sign
                pass
            nrm = np.cross(B_ - A_, C_ - A_)
            F.append(tuple(ids) if nrm[1] > 0 else tuple(ids[::-1]))
        V, F = merge_doubles(V, F, 1e-3)
        return V, F

    # ---------------------------------------------------------- fascia board (with its bed mould)
    def fascia_board(self):
        fb = self.P["fascia_board"]
        u0, u1 = fb["dims"]["u_range"]
        z0 = fb["dims"]["z_range"][0]
        prof = [(p[0], p[1] + z0) for p in fb["profiles"]["section"]["points"]]
        self.add("fas_board", prism_dz(prof, u0, u1), "oxblood")
        bm = fb["dims"].get("bed_mould_cyma")
        if bm:                                                 # D5: a cyma reversa 40 high, d 120 to 150, between the consoles, 1 into the board
            (zb0, zb1), (db0, db1), (ub0, ub1) = bm["z"], bm["d"], bm["u"]
            pts = [(db0 - 1.0, zb0)] + [(db0 + (db1 - db0) * (3 * (i / 16.0) ** 2 - 2 * (i / 16.0) ** 3), zb0 + (zb1 - zb0) * i / 16.0) for i in range(17)] + [(db0 - 1.0, zb1)]
            self.add("fas_mould", prism_dz(pts, ub0, ub1), "oxblood", bev=None)
        return self

    # ---------------------------------------------------------- cornice with its mitred returns
    def cornice(self):
        c = self.P["cornice"]
        sec = c["profiles"]["section"]["points"]
        z0 = c["dims"]["z_bottom"]
        u0, u1 = c["dims"]["u_range"]                        # 54, 5946
        depth = c["dims"]["depth"]
        prof = [(p[0], p[1] + z0) for p in sec]

        def path(dv):
            ul = u0 + (depth - dv)
            ur = u1 - (depth - dv)
            return [(ul, 0.0), (ul, -dv), (ur, -dv), (ur, 0.0)]
        P = np.asarray(prof, float)
        V, F = sweep_path(P, lambda dv: path(dv))
        V, F = merge_doubles(V, F)
        main_ob = self.add("cor_cornice", (V, F), "oxblood")
        bf = c["dims"].get("break_forward")
        if bf:                                                # D4: broken forward over each console, with mitred returns
            front = Polygon(prof).buffer(0).intersection(sbox(depth - bf["forward"], z0 - 1.0, depth + 1.0, z0 + 151.0))
            Q = list(front.exterior.coords)[:-1]
            if (Polygon(Q).exterior.is_ccw) != (Polygon(prof).exterior.is_ccw):
                Q = Q[::-1]
            for tag_, (ua, ub) in (("l", bf["left_u"]), ("r", bf["right_u"])):
                def bpath(dv, ua=ua, ub=ub):
                    k = depth - dv
                    return [(ua + k, -(depth - k)), (ua + k, -(bf["nose_d"] - k)), (ub - k, -(bf["nose_d"] - k)), (ub - k, -(depth - k))]
                V, F = sweep_path(np.asarray(Q, float), bpath)
                V, F = merge_doubles(V, F)
                vol = sum(np.dot(V[f[0]], np.cross(V[f[i]], V[f[i + 1]])) for f in F for i in range(1, len(f) - 1)) / 6.0
                if vol < 0:
                    F = [tuple(f[::-1]) for f in F]
                bool_op(main_ob, V, F, "UNION")                  # one solid: no coplanar overlaps where the breaks meet the run
        return self

    # ---------------------------------------------------------- sill
    def sill(self, u0=None, u1=None):
        s = self.P["sill"]
        z = self.B["z"]
        win = self.S["zones_u"]["window"]
        u0 = win[0] if u0 is None else u0
        u1 = win[1] - 3.0 if u1 is None else u1               # the sill stops 3 short of the plinth's side (meets: sill and plinth)
        self.add("sil_sill", prism_dz(s["profiles"]["section"]["points"], u0, u1), "white")
        return self

    # ---------------------------------------------------------- stallriser (panel variant)
    def stallriser(self):
        sv = self.P["stallriser"]["variants"]["panel"]
        dm = sv["dims"]
        u0, u1 = self.S["zones_u"]["window"]
        top = self.P["stallriser"]["dims"]["z_range"][1]                  # 525
        face = self.P["stallriser"]["dims"]["face_d"]                     # 125
        sec = sv["section"]["points"]                                     # (0,0) (135,0) (135,105) (131,112) (125,120) (125,525) (0,525)
        base_pts = [(sec[1][1], sec[1][0]), (sec[2][1], sec[2][0]), (sec[3][1], sec[3][0]), (sec[4][1], sec[4][0]), (top, face)]
        base = lerp_table(base_pts)
        inset, margin, rise, bead = dm["panel_inset"], dm["field_margin"], dm["field_rise"], dm["bead"]
        zr0, zr1 = dm["bottom_rail"][1], dm["top_rail"][0]                # 200, 445
        stile = dm["stile"]
        gl = self.S["glazing_layout"]
        # three panels between 80 stiles and 80 muntins on the window's mullion lines (the drawing's)
        cuts = [u0 + m for m in gl["mullion_centres"]]
        edges = [u0 + stile] + [x for c in cuts for x in (c - stile / 2.0, c + stile / 2.0)] + [u1 - stile]
        openings = [(edges[2 * i], edges[2 * i + 1]) for i in range(len(cuts) + 1)]
        # across an opening: a convex quarter-round bead (14, centre in the angle), a flat margin, a bevel rising `rise` to the field
        th = [math.radians(a) for a in range(0, 91, 18)]
        prof = [(bead * math.sin(t), inset - bead * math.cos(t)) for t in th]       # depth below the frame's face: 0 at the edge, `inset` at x = bead
        prof += [(bead + 7.0, inset), (margin, inset - rise)]
        pocket = lerp_table(prof + [(1e6, inset - rise)])

        def fu(u):
            for a, b in openings:
                if a < u < b:
                    return pocket(min(u - a, b - u))
            return 0.0

        def fz(z):
            return pocket(min(z - zr0, zr1 - z)) if zr0 < z < zr1 else 0.0
        us = [u0, u1]
        for a, b in openings:
            us += [a, b] + [a + x for x, _ in prof] + [b - x for x, _ in prof]
        us = uniq_sorted([u for u in us if u0 <= u <= u1])
        zs = [0.0, top, zr0, zr1] + [p[0] for p in base_pts] + [zr0 + x for x, _ in prof] + [zr1 - x for x, _ in prof]
        zs = uniq_sorted([z for z in zs if 0.0 <= z <= top])
        D = np.zeros((len(us), len(zs)))
        for i, u in enumerate(us):
            for j, z in enumerate(zs):
                D[i][j] = base(z) - min(fu(u), fz(z))
        self.add("sta_panel", hf_slab(us, zs, D), "oxblood")
        self.openings = openings
        return self

    # ---------------------------------------------------------- window frame, T1 (jambs, seat, mullions, transom, bars, head, glass, beads)
    def window_frame(self):
        W = self.P["window_frame"]
        d = W["dims"]
        pr = W["profiles"]
        gl = self.S["glazing_layout"]
        win = self.S["zones_u"]["window"]
        u0, u1 = win
        z_seat0, z_seat1 = d["bottom_rail"]                   # 600, 625
        z_tr0, z_tr1 = d["transom"]                           # 2400, 2480
        z_h0, z_h1 = d["head"]                                # 2790, 2850
        jf = d["jamb_face"]
        z_foot = z_seat0 - SEAT_EMBED
        # jambs (jamb_t1_plan: outer face at local u 0, inner at 50), left as drawn, right mirrored; they stand on the sill's flat bed
        # (d 0 to 60) and their front 35 overhangs the weathering, so a foot wedge (d 60.5 to 95, z 588 to 600) is scribed into the sill
        jp = pr["jamb_t1_plan"]["points"]
        jl = [(u0 + p[0], p[1]) for p in jp]
        jr = [(u1 - p[0], p[1]) for p in jp][::-1]
        self.add("win_jamb_l", prism_ud(jl, z_seat0, z_h1), "white")
        self.add("win_jamb_r", prism_ud(jr, z_seat0, z_h1), "white")
        for nm, poly in (("win_jamb_foot_l", jl), ("win_jamb_foot_r", jr)):
            # past the flat bed (d 60) so that no top face is coplanar with the sill's, and 0.3 in from the jamb's outer face
            xs = [p[0] for p in poly]
            clip = Polygon(poly).buffer(0).intersection(sbox(min(xs) + (0.3 if nm.endswith("_l") else 0.0), 60.5, max(xs) - (0.3 if nm.endswith("_r") else 0.0), 1e5))
            self.add(nm, prism_ud(list(clip.exterior.coords)[:-1], z_foot, z_seat0), "white", bev=None)
        ui0, ui1 = u0 + jf, u1 - jf                            # between the jambs
        # the seat: 25 high, 60 deep (the flat bed of the sill), between the jambs
        self.add("win_seat", box(ui0, ui1, 0.0, 60.0, z_seat0, z_seat1), "white")
        # transom (transom_t1, z local from 2400), between the jambs
        tz = [(p[0], p[1] + z_tr0) for p in pr["transom_t1"]["points"]]
        self.add("win_transom", prism_dz(tz, ui0, ui1), "white")
        # head: a plain 95 x 60 rail under the fascia's foot
        hz = [(p[0], p[1] + z_h0) for p in pr["head_section"]["points"]]
        self.add("win_head", prism_dz(hz, ui0, ui1), "white")
        # mullions (mullion_t1_plan, centred on the line), z seat top to transom underside
        mp = pr["mullion_t1_plan"]["points"]
        mc = [u0 + c for c in gl["mullion_centres"]]
        for k, c in enumerate(mc):
            self.add("win_mullion_%d" % k, prism_ud([(c + p[0], p[1]) for p in mp], z_seat1, z_tr0), "white")
        # toplight bars (toplight_bar_plan), from 6 into the transom to 3 into the head; their backs 1 off the wall
        bp = pr["toplight_bar_plan"]["points"]
        bc = [u0 + c for c in gl["toplight_bar_centres"]]
        for k, c in enumerate(bc):
            self.add("win_bar_%d" % k, prism_ud([(c + p[0], max(p[1], 1.0)) for p in bp], z_tr1 - 6.0, z_h0 + 3.0), "white")
        mbc = [u0 + c for c in gl.get("toplight_mullion_bar_centres", [])]       # D6: the mullions carried up through the toplights, 70 wide
        for k, c in enumerate(mbc):
            self.add("win_mbar_%d" % k, prism_ud([(c + p[0], max(p[1], 1.0)) for p in mp], z_tr1 - 6.0, z_h0 + 3.0), "white")
        tb = sorted([(c, 14.0, 4.0) for c in bc] + [(c, d["mullion_face"] / 2.0, 8.0) for c in mbc])   # (centre, half face, rebate)
        # glass: 6 plate, d 27 to 33, edges 10 into the jambs' rebates, 8 into the mullions', 4 into the bars'
        gz = d["glass_d"]
        gt = d["glass_thickness"]
        g0, g1 = gz, gz + gt                                  # the target's drawing: glass d 30 to 36, in the 12 rebates (d 24 to 36)
        rjamb, rmull, rbar = 10.0, 8.0, 4.0
        lower_edges = [(ui0 - rjamb)] + [x for c in mc for x in (c - d["mullion_face"] / 2.0 + rmull, c + d["mullion_face"] / 2.0 - rmull)] + [ui1 + rjamb]
        for k in range(len(mc) + 1):
            a, b = lower_edges[2 * k], lower_edges[2 * k + 1]
            self.add("win_glass_lower_%d" % k, box(a, b, g0, g1, z_seat1, z_tr0), "glass", bev=None)
        up = [(ui0 - rjamb)] + [x for c, hw_, rb_ in tb for x in (c - hw_ + rb_, c + hw_ - rb_)] + [ui1 + rjamb]
        for k in range(len(tb) + 1):
            a, b = up[2 * k], up[2 * k + 1]
            self.add("win_glass_top_%d" % k, box(a, b, g0, g1, z_tr1, z_h0), "glass", bev=None)
        # ovolo glazing beads (glazing_bead_ovolo: 16 along the face x 12 proud) round every light, on the glass's front face (d 36 to 48)
        bd = pr["glazing_bead_ovolo"]["points"]
        prof = [(p[0], -p[1]) for p in bd]
        lights = []
        edges_l = [ui0] + [x for c in mc for x in (c - d["mullion_face"] / 2.0, c + d["mullion_face"] / 2.0)] + [ui1]
        for k in range(len(mc) + 1):
            lights.append((edges_l[2 * k], z_seat1, edges_l[2 * k + 1], z_tr0))
        edges_t = [ui0] + [x for c, hw_, rb_ in tb for x in (c - hw_, c + hw_)] + [ui1]
        for k in range(len(tb) + 1):
            lights.append((edges_t[2 * k], z_tr1, edges_t[2 * k + 1], z_h0))
        for k, (a, b, c2, e) in enumerate(lights):
            V, F = joinery.sweep_frame(prof, a, b, c2, e, -g1)
            self.add("win_bead_%d" % k, (V, [tuple(int(i) for i in f) for f in F]), "white", bev=None)
        return self


# ------------------------------------------------------------------ finishing and export
PIVOT_U = {"pilaster": 175.0, "console": 175.0, "fascia_board": 3000.0, "cornice": 3000.0, "sill": None,
           "stallriser": None, "window_frame": None, "shopfront_ritas": 3000.0}


def finish(B, mats, pivot_u):
    """Chamfers (mm), then metres at the pivot, UVs, smooth shading by angle, materials."""
    M = Matrix.Scale(0.001, 4) @ Matrix.Translation((-pivot_u, 0.0, 0.0))
    out = []
    for ob in B.objs:
        mat, bev, bmin = B.meta[ob.name]
        if bev:
            bevel_obj(ob, bev, bmin)
        me = ob.data
        me.transform(M)
        me.update()
        box_uv(me)
        me.shade_smooth()
        me.set_sharp_from_angle(angle=math.radians(35.0))
        me.materials.clear()
        me.materials.append(mats[mat])
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


def pivot_for(T, shop, name):
    s = shop_of(T, shop)
    win = s["zones_u"]["window"]
    if name in ("sill", "stallriser", "window_frame"):
        return (win[0] + win[1]) / 2.0                     # 3975 for Rita's
    return PIVOT_U[name]


def build_part(T, shop, name, out_dir, npz_dir):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mats = setup_materials(T, shop)
    B = Builder(T, shop)
    getattr(B, name)()
    pv = pivot_for(T, shop, name)
    obs = finish(B, mats, pv)
    return write(obs, name, pv, out_dir, npz_dir)


def write(obs, name, pivot_u, out_dir, npz_dir):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(npz_dir, exist_ok=True)
    glb = os.path.join(out_dir, name + ".glb")
    npz = os.path.join(npz_dir, name + ".npz")
    blender_parts.export(obs, npz)
    export_glb(glb)
    info = {"name": name, "pivot_u_mm": pivot_u, "glb": glb, "npz": npz, "glb_bytes": os.path.getsize(glb), "triangles": tri_count(obs),
            "objects": {o.name: len(o.data.polygons) for o in obs},
            "materials": sorted({o.data.materials[0].name for o in obs if o.data.materials and o.data.materials[0]})}
    return info


def build_assembly(T, shop, out_dir, npz_dir):
    """Rita's front: left and right pilasters (the right one mirrored), the two consoles, the board, the cornice, the sill, the
    stallriser and the window frame, each at its own place in the bay (every part is already built there)."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mats = setup_materials(T, shop)
    B = Builder(T, shop)
    B.pilaster("L")
    B.pilaster("R")
    # the right pier: the left one mirrored about the bay's middle (u 3000)
    for o in B.objs:
        if o.name.startswith("pilR_"):
            mirror_u(o, 3000.0)
    B.console("L", uc=175.0)
    B.console("R", uc=5825.0)
    B.fascia_board()
    B.cornice()
    B.sill()
    B.stallriser()
    B.window_frame()
    obs = finish(B, mats, 3000.0)
    return write(obs, "shopfront_ritas", 3000.0, out_dir, npz_dir)


PARTS = ["pilaster", "console", "fascia_board", "cornice", "sill", "stallriser", "window_frame"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shop", default="ritas")
    ap.add_argument("--only")
    ap.add_argument("--out-dir", default=ASSET_DIR)
    ap.add_argument("--npz-dir", default=NPZ_DIR)
    a = ap.parse_args()
    T = load_target()
    res = {}
    names = a.only.split(",") if a.only else PARTS + ["shopfront_ritas"]
    for nme in names:
        if nme == "shopfront_ritas":
            res[nme] = build_assembly(T, a.shop, a.out_dir, a.npz_dir)
        else:
            res[nme] = build_part(T, a.shop, nme, a.out_dir, a.npz_dir)
        print(nme, "triangles", res[nme]["triangles"], "glb bytes", res[nme]["glb_bytes"], flush=True)
    os.makedirs(a.npz_dir, exist_ok=True)
    pj = os.path.join(a.npz_dir, "parts.json")
    old = json.load(open(pj)) if os.path.exists(pj) else {}
    old.update(res)
    json.dump(old, open(pj, "w"), indent=1)
    return res


if __name__ == "__main__":
    main()
