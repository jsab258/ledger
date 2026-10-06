"""The south quay kit's geometry, in plain Python (no Blender), so the selftest can build it whole.

What it is: the closure of Quay Street's south end as the town really has it (the adopted atlas,
production/art/atlas-01/data/atlas.json): the street running on to its junction, the junction's
three arms, the open quay apron, the quay edge, the Old Basin's water, the stone jetty with its
harbour light, the Hook's dockside warehouses along the east quay, and a walled yard on the west
flank. Research: production/research/south-quay/METHOD-2026-10-06.md. README:
production/art/south-quay/README.md.

THE FRAME is terrace-front.py's: x along Quay Street (0 at its south end, + north), y across it
(EAST = +y), z up, metres, the road crown z = 0. This module builds in that frame; the Blender
step reflects y to -y at export, as the street's own export does (production/assets/street/
quay-street.json "mirror"), so the glb drops in beside quay-street.glb with no transform.

ONE HOME PER FACT. The street's levels (road half width, crossfall, kerb, footway, frontage, where
its road ends) are READ from tools/art-recipes/terrace-front.py; the street's material table is READ
from the same file; the junction, the roads and the coast are READ from the atlas. Nothing those
files already say is typed here a second time.
"""
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TERRACE_REL = "tools/art-recipes/terrace-front.py"
ATLAS_REL = "production/art/atlas-01/data/atlas.json"

#: The street constants this kit reads from terrace-front.py (name -> its value there).
STREET_CONSTANTS = ("ROAD_HALF_M", "ROAD_CROSSFALL", "KERB_W_M", "KERB_UPSTAND_M", "FOOTWAY_CROSSFALL",
                    "STREET_FRONTAGE_M", "THRESHOLD_ABOVE_CROWN_M", "BACKDROP_ROAD_END")

#: The materials no street material fits (README says so). Linear RGB, roughness, why.
KIT_NEW_MATERIALS = {
    "quay_stone": ((0.150, 0.146, 0.138), 0.80, "granite setts, quay walls and the jetty's masonry: "
                   "the atlas's Hook 'quay stone', darkened to the street's wet palette"),
    "harbour_water": ((0.014, 0.020, 0.019), 0.22, "the Old Basin and the sea: dark green-grey, "
                      "wind-ruffled (0.22), so grazing views do not mirror the sky whole"),
    "iron_black": ((0.012, 0.012, 0.013), 0.50, "black-painted cast iron: bollards, mooring rings, "
                   "the harbour light's gallery and roof"),
    "rope": ((0.200, 0.150, 0.085), 0.90, "a coil of manila mooring rope"),
}

# ---- the kit's own dimensions, each from the research note (METHOD-2026-10-06.md) ------------------
#: The quay's working level: the S kerb's top (the apron is laid flush with it) and the coping's top.
APRON_ABOVE_CROWN_M = None          # read: the kerb top, terrace-front's kerb_top_z()
COPING_W_M = 0.60                   # granite cope 0.6 m across (research section 2)
COPING_T_M = 0.30                   # and 0.30 deep on the face
COPING_NOSE_M = 0.05                # the cope stands 50 mm proud of the wall face below it
QUAY_BATTER = 1.0 / 20.0            # the wall leans back 1 in 20
#: Half-tide below the cope (research section 3): Newlyn's springs are 5.6 and 0.8 m above chart
#: datum, so half-tide (3.2 m) is 2.4 m under MHWS; an old quay's cope about 0.8 to 1.0 m above MHWS
#: puts half-tide 3.2 to 3.4 m under the cope (today's design rule, 1.5 m above MHWS, would give 3.9).
HALF_TIDE_BELOW_COPE_M = 3.20
WALL_BELOW_WATER_M = 1.0            # the quay face carries on under the water
WATER_FAR_X_M = -8000.0             # see README: at -4000 the sky's lower half shows in the corners
WATER_HALF_Y_M = 8000.0
KERB_RADIUS_NW_M = 8.0              # junction kerb radii: CHOSEN, no source reached (research section 6)
KERB_RADIUS_NE_M = 6.0
KERB_RADIUS_S_M = 12.0
FOOTWAY_W_M = 2.0
EAST_LAND_TO_Y_M = 220.0            # the east land is built out to here (the atlas coast's (620,195))
FORECOURT_TO_Y_M = 130.0            # the NE ground and the Harbour Board's forecourt, out to here
WEST_LAND_TO_Y_M = -200.0
YARD_WALL_T_M = 0.34                # one and a half bricks
YARD_WALL_H_M = 1.40                # above the footway's back
#: Bollards, rings, ladder, boxes, rope, dustbin: sizes in the research note, places here.
BOLLARD_PROFILE = ((0.25, 0.00), (0.25, 0.04), (0.19, 0.06), (0.17, 0.08), (0.15, 0.47),
                   (0.13, 0.51), (0.13, 0.55), (0.21, 0.59), (0.22, 0.63), (0.20, 0.67),
                   (0.11, 0.71), (0.0, 0.72))
FISH_BOX_M = (0.84, 0.51, 0.248)    # FAO type C, 840 x 510 x 248 mm
FISH_BOX_WALL_M = 0.018
DUSTBIN_D_M, DUSTBIN_H_M = 0.47, 0.66
LADDER_W_M, LADDER_RUNG_M, LADDER_OFF_M = 0.45, 0.30, 0.15
LIGHT_TOWER_H_M = 4.6               # the harbour light: Watchet's is 6.5 m with its lantern
STOREY_GROUND_M, STOREY_UPPER_M = 3.4, 3.0
ROOF_PITCH_DEG = 35.0

TRI_BUDGET = 80000


# =================================================================================================
# reading the homes
# =================================================================================================
def read_street_constants(root=ROOT):
    src = open(os.path.join(root, TERRACE_REL), encoding="utf-8").read()
    out = {}
    for name in STREET_CONSTANTS:
        m = re.search(r"^%s\s*=\s*([-+0-9.eE]+)" % name, src, re.M)
        if not m:
            raise AssertionError("terrace-front.py no longer defines %s" % name)
        out[name] = float(m.group(1))
    return out


def read_street_materials(root=ROOT):
    """{name: ((r, g, b), roughness)} from terrace-front.py's MATERIALS table."""
    src = open(os.path.join(root, TERRACE_REL), encoding="utf-8").read()
    i = src.index("\nMATERIALS = (")
    j = src.index("\n)\n", i)
    rows = re.findall(r'\(\s*"(\w+)",\s*\(\s*([-0-9.]+),\s*([-0-9.]+),\s*([-0-9.]+)\s*\),\s*([-0-9.]+)\s*\)',
                      src[i:j])
    return {n: ((float(r), float(g), float(b)), float(ro)) for n, r, g, b, ro in rows}


def all_materials(root=ROOT):
    mats = dict(read_street_materials(root))
    for n, (rgb, ro, _why) in KIT_NEW_MATERIALS.items():
        if n in mats:
            # since the kit went into the street (terrace-front.py, 6 October) its four are the
            # street's own too: they must agree, value for value
            srgb, sro = mats[n][0], mats[n][1]
            if any(abs(a - b) > 1e-6 for a, b in zip(srgb, rgb)) or abs(sro - ro) > 1e-6:
                raise AssertionError("%s is a street material with other values: reuse it" % n)
        mats[n] = (rgb, ro)
    return mats


def atlas_to_recipe(p, anchor=(400.0, 350.0)):
    """Atlas [east, north] -> recipe (x, y): x = north - 350, y = east - 400 (atlas street_anchor)."""
    return (float(p[1]) - anchor[1], float(p[0]) - anchor[0])


def read_atlas(root=ROOT):
    """The junction, the two roads leaving it and the coast, from the adopted atlas."""
    A = json.load(open(os.path.join(root, ATLAS_REL), encoding="utf-8"))
    sa = A["street_anchor"]
    anchor = tuple(float(v) for v in sa["origin_atlas"])
    if "east=400+z_m" not in sa["source_to_atlas"].replace(" ", "") or anchor != (400.0, 350.0):
        raise AssertionError("the atlas's street anchor changed: %r %r" % (sa["origin_atlas"], sa["source_to_atlas"]))
    routes = {r["id"]: r for r in A["routes"]}
    quay = [tuple(p) for p in routes["quay"]["points"]]
    jn = quay.index((400, 320))                       # where Quay Street turns west
    west_end = quay[jn - 1]                           # (310, 300): the turn toward the jetty root
    hb = [tuple(p) for p in routes["harbourlink"]["points"]]
    if hb[0] != (400, 320):
        raise AssertionError("the Harbour Board approach no longer leaves Quay Street's junction")
    land = [tuple(p) for p in A["land"]]
    need = [(300, 280), (440, 280), (440, 180), (620, 195), (300, 240), (385, 240), (385, 220), (300, 220)]
    for p in need:
        if p not in land:
            raise AssertionError("the atlas coast moved: %r is not a land vertex" % (p,))
    return {
        "junction": atlas_to_recipe((400, 320)),
        "west_end": atlas_to_recipe(west_end),
        "harbour_board": [atlas_to_recipe(p) for p in hb],
        "north_quay_x": 280.0 - 350.0,                 # the basin's north edge, atlas north 280
        "basin_west_y": 300.0 - 400.0,                 # its west edge, atlas east 300
        "basin_east_y": 440.0 - 400.0,                 # its east edge, atlas east 440
        "jetty_x": (220.0 - 350.0, 240.0 - 350.0),     # the jetty strip, atlas north 220 to 240
        "jetty_end_y": 385.0 - 400.0,                  # to atlas east 385
        "east_coast": (atlas_to_recipe((440, 180)), atlas_to_recipe((620, 195))),
        "atlas": A,
    }


# =================================================================================================
# 2D / 3D helpers
# =================================================================================================
def v2(a, b):
    return (b[0] - a[0], b[1] - a[1])


def norm2(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


def add2(a, b, s=1.0):
    return (a[0] + b[0] * s, a[1] + b[1] * s)


def dot2(a, b):
    return a[0] * b[0] + a[1] * b[1]


def left2(d):
    """d turned a quarter turn anticlockwise (to its left, in the recipe's own maths)."""
    return (-d[1], d[0])


def line_x(p, u, q, w):
    """Intersection of p + s u and q + t w."""
    den = u[0] * w[1] - u[1] * w[0]
    if abs(den) < 1e-12:
        raise ValueError("parallel lines")
    s = ((q[0] - p[0]) * w[1] - (q[1] - p[1]) * w[0]) / den
    return add2(p, u, s)


def seg_dist(p, a, b):
    ab = v2(a, b)
    L2 = dot2(ab, ab)
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, dot2(v2(a, p), ab) / L2))
    c = add2(a, ab, t)
    return math.hypot(p[0] - c[0], p[1] - c[1])


def poly_dist(p, pts):
    return min(seg_dist(p, pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def sub3(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross3(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def newell(pts):
    n = [0.0, 0.0, 0.0]
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        n[0] += (a[1] - b[1]) * (a[2] + b[2])
        n[1] += (a[2] - b[2]) * (a[0] + b[0])
        n[2] += (a[0] - b[0]) * (a[1] + b[1])
    return tuple(n)


def signed_area(poly):
    return 0.5 * sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                     for i in range(len(poly)))


def ear_clip(poly):
    """Triangulate a simple polygon (list of (x, y)); returns index triples, anticlockwise."""
    n = len(poly)
    idx = list(range(n))
    if signed_area(poly) < 0:
        idx.reverse()
    tris = []

    def is_convex(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 1e-12

    def inside(p, a, b, c):
        d1 = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        d2 = (c[0] - b[0]) * (p[1] - b[1]) - (c[1] - b[1]) * (p[0] - b[0])
        d3 = (a[0] - c[0]) * (p[1] - c[1]) - (a[1] - c[1]) * (p[0] - c[0])
        return d1 >= -1e-12 and d2 >= -1e-12 and d3 >= -1e-12

    guard = 0
    while len(idx) > 3 and guard < 100000:
        guard += 1
        m = len(idx)
        cut = False
        # the ear with the best (largest) smallest angle, not just the first: fewer slivers
        best = None
        for k in range(m):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % m]
            a, b, c = poly[i0], poly[i1], poly[i2]
            if not is_convex(a, b, c):
                continue
            if any(inside(poly[j], a, b, c) for j in idx if j not in (i0, i1, i2)):
                continue
            q = _min_angle(a, b, c)
            if best is None or q > best[0]:
                best = (q, k)
        if best is not None:
            k = best[1]
            tris.append((idx[k - 1], idx[k], idx[(k + 1) % m]))
            idx.pop(k)
            cut = True
        if not cut:
            raise AssertionError("ear clipping failed: the polygon is not simple")
    tris.append(tuple(idx))
    return tris


def _min_angle(a, b, c):
    def ang(p, q, r):
        u, w = v2(p, q), v2(p, r)
        lu, lw = math.hypot(*u), math.hypot(*w)
        if lu * lw == 0:
            return 0.0
        return math.acos(max(-1.0, min(1.0, dot2(u, w) / (lu * lw))))
    return min(ang(a, b, c), ang(b, c, a), ang(c, a, b))


# =================================================================================================
# the kit: pieces, each one material, named "<material>__<piece>"
# =================================================================================================
class Kit:
    def __init__(self, materials):
        self.materials = materials
        self.pieces = {}

    def piece(self, material, name, smooth=False):
        if material not in self.materials:
            raise AssertionError("unknown material %r for %s" % (material, name))
        key = "%s__%s" % (material, name)
        p = self.pieces.get(key)
        if p is None:
            p = self.pieces[key] = {"name": key, "material": material, "verts": [], "faces": [],
                                    "smooth": smooth}
        return p

    @staticmethod
    def verts(p, pts):
        base = len(p["verts"])
        p["verts"].extend(tuple(float(c) for c in q) for q in pts)
        return list(range(base, base + len(pts)))

    def face(self, p, pts, hint=None):
        """One face from its corners, anticlockwise seen from outside; with a hint vector, turned to
        face that way if it does not already."""
        if hint is not None and dot3(newell(pts), hint) < 0:
            pts = list(reversed(pts))
        ids = self.verts(p, pts)
        p["faces"].append(tuple(ids))

    def box(self, p, x0, x1, y0, y1, z0, z1, skip=()):
        self.obox(p, ((x0 + x1) / 2.0, (y0 + y1) / 2.0), (1.0, 0.0), (x1 - x0) / 2.0, (y1 - y0) / 2.0,
                  z0, z1, skip)

    def obox(self, p, c, u, hu, hv, z0, z1, skip=()):
        """A box in plan turned to u (unit), half sizes hu along u and hv across, z0..z1."""
        u = norm2(u)
        w = left2(u)
        corners = []
        for z in (z0, z1):
            for a, b in ((-hu, -hv), (hu, -hv), (hu, hv), (-hu, hv)):
                q = add2(add2(c, u, a), w, b)
                corners.append((q[0], q[1], z))
        self._box8(p, corners, skip)

    def _box8(self, p, v, skip=()):
        quads = {"bottom": (0, 3, 2, 1), "top": (4, 5, 6, 7), "ymin": (0, 1, 5, 4),
                 "xmax": (1, 2, 6, 5), "ymax": (2, 3, 7, 6), "xmin": (3, 0, 4, 7)}
        ids = self.verts(p, v)
        for k, q in quads.items():
            if k in skip:
                continue
            p["faces"].append(tuple(ids[i] for i in q))

    def strut(self, p, a, b, h):
        """A square bar of half side h from 3D point a up to 3D point b (near vertical)."""
        v = []
        for c in (a, b):
            for dx, dy in ((-h, -h), (h, -h), (h, h), (-h, h)):
                v.append((c[0] + dx, c[1] + dy, c[2]))
        self._box8(p, v)

    def frame_box(self, p, O, U, N, u0, u1, v0, v1, d0, d1, skip=("ymax",)):
        """A box in a facade's frame: u along it, v = z, depth d into the wall (d < 0 is proud)."""
        def P(u, d, v):
            return (O[0] + U[0] * u - N[0] * d, O[1] + U[1] * u - N[1] * d, v)
        v8 = [P(u0, d0, v0), P(u1, d0, v0), P(u1, d1, v0), P(u0, d1, v0),
              P(u0, d0, v1), P(u1, d0, v1), P(u1, d1, v1), P(u0, d1, v1)]
        self._box8(p, v8, skip)

    def ribbon(self, p, rows, hint=None, close=False):
        """Quads between consecutive rows (each a list of 3D points of one length)."""
        grid = [self.verts(p, r) for r in rows]
        for a, b in zip(grid[:-1], grid[1:]):
            n = len(a)
            for i in range(n if close else n - 1):
                j = (i + 1) % n
                q = (a[i], a[j], b[j], b[i])
                pts = [p["verts"][k] for k in q]
                h = hint(pts) if callable(hint) else hint
                if h is not None and dot3(newell(pts), h) < 0:
                    q = tuple(reversed(q))
                p["faces"].append(q)

    def lathe(self, p, c, profile, seg, z0=0.0, phase=0.0):
        """A surface of revolution about the vertical through c, profile (r, z) bottom to top."""
        rings = []
        for r, z in profile:
            if r <= 1e-9:
                rings.append(self.verts(p, [(c[0], c[1], z0 + z)]))
            else:
                rings.append(self.verts(p, [(c[0] + r * math.cos(phase + 2 * math.pi * k / seg),
                                             c[1] + r * math.sin(phase + 2 * math.pi * k / seg), z0 + z)
                                            for k in range(seg)]))
        for a, b in zip(rings[:-1], rings[1:]):
            for k in range(seg):
                k1 = (k + 1) % seg
                if len(a) == 1 and len(b) == 1:
                    continue
                if len(b) == 1:
                    p["faces"].append((a[k], a[k1], b[0]))
                elif len(a) == 1:
                    p["faces"].append((a[0], b[k1], b[k]))
                else:
                    p["faces"].append((a[k], a[k1], b[k1], b[k]))

    def torus(self, p, c, axis_u, axis_v, R, r, segR=16, segr=6):
        """A ring of radius R and bar r, in the plane of axis_u and axis_v (3D unit vectors)."""
        n = cross3(axis_u, axis_v)
        rings = []
        for i in range(segR):
            t = 2 * math.pi * i / segR
            radial = tuple(axis_u[k] * math.cos(t) + axis_v[k] * math.sin(t) for k in range(3))
            centre = tuple(c[k] + radial[k] * R for k in range(3))
            ring = []
            for j in range(segr):
                s = 2 * math.pi * j / segr
                ring.append(tuple(centre[k] + r * (radial[k] * math.cos(s) + n[k] * math.sin(s)) for k in range(3)))
            rings.append(self.verts(p, ring))
        for i in range(segR):
            a, b = rings[i], rings[(i + 1) % segR]
            for j in range(segr):
                j1 = (j + 1) % segr
                q = (a[j], a[j1], b[j1], b[j])
                pts = [p["verts"][k] for k in q]
                ctr = tuple(sum(x[k] for x in pts) / 4.0 for k in range(3))
                # outward from the bar's own centre line
                ti = 2 * math.pi * (i + 0.5) / segR
                radial = tuple(axis_u[k] * math.cos(ti) + axis_v[k] * math.sin(ti) for k in range(3))
                bar = tuple(c[k] + radial[k] * R for k in range(3))
                if dot3(newell(pts), sub3(ctr, bar)) < 0:
                    q = tuple(reversed(q))
                p["faces"].append(q)

    def fill(self, p, poly, z):
        """A horizontal polygon at height z (or z(x, y)), facing up."""
        zf = z if callable(z) else (lambda x, y, zz=z: zz)
        tris = ear_clip(poly)
        ids = self.verts(p, [(x, y, zf(x, y)) for x, y in poly])
        for a, b, c in tris:
            p["faces"].append((ids[a], ids[b], ids[c]))


def tri_count(pieces):
    return sum(len(f) - 2 for p in pieces.values() for f in p["faces"])


# =================================================================================================
# the junction: three arms, filleted kerbs
# =================================================================================================
class Stations:
    """A kerb line as stations: point, unit normal INTO THE LAND, miter scale. offset(d) moves each
    station d into the land; concentric arcs and mitred bends follow by construction."""

    def __init__(self):
        self.pts, self.nrm, self.scl = [], [], []

    def add(self, p, n, s=1.0):
        if self.pts and math.hypot(p[0] - self.pts[-1][0], p[1] - self.pts[-1][1]) < 1e-6:
            return
        self.pts.append(p)
        self.nrm.append(n)
        self.scl.append(s)

    def offset(self, d):
        return [add2(p, n, d * s) for p, n, s in zip(self.pts, self.nrm, self.scl)]


def fillet(pA, uA, pB, uB, R, land_n_A, land_n_B, step_deg=7.5):
    """The corner between line A (through pA, heading uA INTO the corner) and line B (through pB,
    heading uB OUT of it), rounded to radius R with the land inside the circle. Returns (T1, T2,
    arc points with their land normals, centre)."""
    C = line_x(pA, uA, pB, uB)
    back = (-uA[0], -uA[1])
    theta = math.acos(max(-1.0, min(1.0, dot2(back, uB))))
    t = R / math.tan(theta / 2.0)
    T1 = add2(C, uA, -t)
    T2 = add2(C, uB, t)
    O = add2(T1, land_n_A, R)
    a1 = math.atan2(T1[1] - O[1], T1[0] - O[0])
    a2 = math.atan2(T2[1] - O[1], T2[0] - O[0])
    da = a2 - a1
    while da > math.pi:
        da -= 2 * math.pi
    while da < -math.pi:
        da += 2 * math.pi
    n = max(2, int(math.ceil(abs(math.degrees(da)) / step_deg)))
    arc = []
    for k in range(n + 1):
        a = a1 + da * k / n
        q = (O[0] + R * math.cos(a), O[1] + R * math.sin(a))
        arc.append((q, norm2(v2(q, O))))           # into the land is toward the centre
    return T1, T2, arc, O


class Junction:
    def __init__(self, sc, at):
        self.half = sc["ROAD_HALF_M"]
        self.fall = sc["ROAD_CROSSFALL"]
        self.kerb_w = sc["KERB_W_M"]
        self.kerb_up = sc["KERB_UPSTAND_M"]
        self.foot_fall = sc["FOOTWAY_CROSSFALL"]
        self.join_x = sc["BACKDROP_ROAD_END"]
        self.J = at["junction"]
        self.W_end = at["west_end"]
        hb = at["harbour_board"]
        self.E_pts = [hb[0], hb[1], hb[2]]
        self.N_pts = [(self.join_x, 0.0), self.J]
        self.W_pts = [self.J, self.W_end]
        self.network = [self.N_pts, self.W_pts, self.E_pts]
        self.channel_z = -self.half * self.fall
        self.kerb_top = self.channel_z + self.kerb_up
        self._build()

    # the street's own sections, terrace-front's road_z / kerb_top_z / footway_z
    def road_z(self, p):
        d = min(poly_dist(p, pl) for pl in self.network)
        return -min(d, self.half) * self.fall

    def footway_z_at(self, off_from_kerb_back):
        return self.kerb_top + max(0.0, min(off_from_kerb_back, FOOTWAY_W_M)) * self.foot_fall

    def _arm_line(self, pts, side, k=0):
        """Segment k of a polyline offset by the road half to one side (+1 left, -1 right)."""
        a, b = pts[k], pts[k + 1]
        d = norm2(v2(a, b))
        n = left2(d)
        off = (n[0] * side * self.half, n[1] * side * self.half)
        return add2(a, off), d, (n[0] * side, n[1] * side)

    def _build(self):
        h = self.half
        dN = norm2(v2(*self.N_pts))                   # (-1, 0)
        dW = norm2(v2(*self.W_pts))
        dE1 = norm2(v2(self.E_pts[0], self.E_pts[1]))
        dE2 = norm2(v2(self.E_pts[1], self.E_pts[2]))
        # Arm N: left is west (-y). Arm W: left is north (+x). Arm E: left is south (-x).
        nN_left = left2(dN)                            # (0, -1)
        nW_left = left2(dW)
        nE1_left = left2(dE1)
        nE2_left = left2(dE2)
        J = self.J
        # ---- the NW kerb: arm N's west kerb, round to arm W's north kerb ----
        pA = add2(self.N_pts[0], nN_left, h)
        pB = add2(J, nW_left, h)
        landA = nN_left                                # west of arm N's kerb is land
        landB = nW_left                                # north of arm W's kerb is land
        T1, T2, arc, O = fillet(pA, dN, pB, dW, KERB_RADIUS_NW_M, landA, landB)
        nw = Stations()
        nw.add(pA, landA)
        nw.add(T1, landA)
        for q, n in arc[1:-1]:
            nw.add(q, n)
        nw.add(T2, landB)
        nw.add(add2(self.W_end, nW_left, h), landB)
        self.nw = nw
        self.nw_T = (T1, T2)
        # ---- the NE kerb: arm N's east kerb, round to arm E's north (right-hand) kerb ----
        nN_right = (-nN_left[0], -nN_left[1])
        nE1_right = (-nE1_left[0], -nE1_left[1])
        nE2_right = (-nE2_left[0], -nE2_left[1])
        pA = add2(self.N_pts[0], nN_right, h)
        pB = add2(J, nE1_right, h)
        T1, T2, arc, O = fillet(pA, dN, pB, dE1, KERB_RADIUS_NE_M, nN_right, nE1_right)
        ne = Stations()
        ne.add(pA, nN_right)
        ne.add(T1, nN_right)
        for q, n in arc[1:-1]:
            ne.add(q, n)
        ne.add(T2, nE1_right)
        self._mitre(ne, self.E_pts[1], nE1_right, nE2_right, h)
        ne.add(add2(self.E_pts[2], nE2_right, h), nE2_right)
        self.ne = ne
        self.ne_T = (T1, T2)
        # ---- the S kerb: arm W's south (right-hand) kerb, round to arm E's south (left) kerb ----
        nW_right = (-nW_left[0], -nW_left[1])
        pA = add2(self.W_end, nW_right, h)
        uA = (-dW[0], -dW[1])                          # heading from arm W's end into the corner
        pB = add2(J, nE1_left, h)
        T1, T2, arc, O = fillet(pA, uA, pB, dE1, KERB_RADIUS_S_M, nW_right, nE1_left)
        s = Stations()
        s.add(pA, nW_right)
        s.add(T1, nW_right)
        for q, n in arc[1:-1]:
            s.add(q, n)
        s.add(T2, nE1_left)
        self._mitre(s, self.E_pts[1], nE1_left, nE2_left, h)
        s.add(add2(self.E_pts[2], nE2_left, h), nE2_left)
        self.s = s
        self.s_T = (T1, T2)
        # ---- where each arm's own ribbon starts: past both its corners' tangent points ----
        self.xN_in = max(self.nw_T[0][0], self.ne_T[0][0])
        self.sW_in = max(dot2(v2(J, self.nw_T[1]), dW), dot2(v2(J, self.s_T[0]), dW))
        self.sE_in = max(dot2(v2(J, self.ne_T[1]), dE1), dot2(v2(J, self.s_T[1]), dE1))
        self.dN, self.dW, self.dE1, self.dE2 = dN, dW, dE1, dE2
        self.nW_left, self.nE1_left, self.nE2_left = nW_left, nE1_left, nE2_left

    @staticmethod
    def _mitre(st, bend, n1, n2, h):
        m = norm2(add2(n1, n2))
        s = 1.0 / max(1e-6, dot2(m, n1))
        st.add(add2(bend, m, h * s), m, s)

    def arm_section(self, c, n_left):
        """A cross-section of an arm at centre c: left kerb face, crown, right kerb face."""
        h = self.half
        return [add2(c, n_left, h), c, add2(c, n_left, -h)]


def _clip_stations(st, keep):
    """The stations whose points pass keep(p)."""
    out = Stations()
    for p, n, s in zip(st.pts, st.nrm, st.scl):
        if keep(p):
            out.add(p, n, s)
    return out


# =================================================================================================
# building the kit
# =================================================================================================
def build(root=ROOT):
    sc = read_street_constants(root)
    at = read_atlas(root)
    mats = all_materials(root)
    kit = Kit(mats)
    jn = Junction(sc, at)
    info = {"street": sc, "junction": jn.J, "west_end": jn.W_end, "harbour_board": jn.E_pts}
    z_ground = jn.kerb_top                       # the apron is laid flush with the S kerb's top
    info["apron_z"] = z_ground
    info["coping_top_z"] = z_ground
    z_water = z_ground - HALF_TIDE_BELOW_COPE_M
    info["water_z"] = z_water
    yard_z = jn.footway_z_at(FOOTWAY_W_M)        # the footway's back, = the street's threshold
    info["yard_z"] = yard_z

    _roads(kit, jn)
    _kerbs_and_footways(kit, jn)
    _markings(kit, jn)
    quay = _quay(kit, jn, at, z_ground, z_water, yard_z)
    info.update(quay)
    _yard_wall_and_store(kit, jn, yard_z)
    _buildings(kit, z_ground, yard_z)
    _quay_furniture(kit, at, z_ground, z_water, jn)
    _boats(kit, z_water, z_ground)
    _harbour_light(kit, at, z_ground)
    for k in [k for k, p in kit.pieces.items() if not p["faces"]]:
        del kit.pieces[k]
    info["tris"] = tri_count(kit.pieces)
    return kit, jn, info


def _roads(kit, jn):
    road = kit.piece("asphalt", "road_quay_street_south")
    zf = jn.road_z
    # ARM N: the street's own section, carried from its end to the junction's corners
    secA = [(jn.join_x, -jn.half), (jn.join_x, 0.0), (jn.join_x, jn.half)]
    secB = [(jn.xN_in, -jn.half), (jn.xN_in, 0.0), (jn.xN_in, jn.half)]
    up = (0.0, 0.0, 1.0)
    kit.ribbon(road, [[(x, y, zf((x, y))) for x, y in secA], [(x, y, zf((x, y))) for x, y in secB]], up)
    # ARM W
    cW0 = add2(jn.J, jn.dW, jn.sW_in)
    rows = []
    for c in (cW0, jn.W_end):
        rows.append([(x, y, zf((x, y))) for x, y in jn.arm_section(c, jn.nW_left)])
    kit.ribbon(kit.piece("asphalt", "road_quay_street_west"), rows, up)
    # ARM E: the Harbour Board approach, with its bend mitred
    cE0 = add2(jn.J, jn.dE1, jn.sE_in)
    m = norm2(add2(jn.nE1_left, jn.nE2_left))
    s = 1.0 / dot2(m, jn.nE1_left)
    b = jn.E_pts[1]
    sec_bend = [add2(b, m, jn.half * s), b, add2(b, m, -jn.half * s)]
    rows = [[(x, y, zf((x, y))) for x, y in jn.arm_section(cE0, jn.nE1_left)],
            [(x, y, zf((x, y))) for x, y in sec_bend],
            [(x, y, zf((x, y))) for x, y in jn.arm_section(jn.E_pts[2], jn.nE2_left)]]
    kit.ribbon(kit.piece("asphalt", "road_harbour_board_approach"), rows, up)
    # THE JUNCTION PAD: a fan from the junction's centre round its boundary, anticlockwise
    loop = []
    loop += [(jn.xN_in, -jn.half), (jn.xN_in, 0.0), (jn.xN_in, jn.half)]
    secE = jn.arm_section(cE0, jn.nE1_left)            # left (south), crown, right (north)
    ne_in = [p for p in jn.ne.pts if p[0] < jn.xN_in - 1e-6 and dot2(v2(jn.J, p), jn.dE1) < jn.sE_in - 1e-6]
    loop += ne_in
    loop += [secE[2], secE[1], secE[0]]
    s_in = [p for p in jn.s.pts if dot2(v2(jn.J, p), jn.dE1) < jn.sE_in - 1e-6
            and dot2(v2(jn.J, p), jn.dW) < jn.sW_in - 1e-6]
    loop += list(reversed(s_in))
    secW = jn.arm_section(cW0, jn.nW_left)             # left (north), crown, right (south)
    loop += [secW[2], secW[1], secW[0]]
    nw_in = [p for p in jn.nw.pts if p[0] < jn.xN_in - 1e-6 and dot2(v2(jn.J, p), jn.dW) < jn.sW_in - 1e-6]
    loop += list(reversed(nw_in))
    # order by angle about the centre (the pad is star-shaped about it by construction)
    J = jn.J
    loop = sorted(set((round(p[0], 6), round(p[1], 6)) for p in loop),
                  key=lambda p: math.atan2(p[1] - J[1], p[0] - J[0]))
    pad = kit.piece("asphalt", "road_junction")
    jid = kit.verts(pad, [(J[0], J[1], 0.0)])[0]
    ids = kit.verts(pad, [(x, y, zf((x, y))) for x, y in loop])
    for k in range(len(ids)):
        pad["faces"].append((jid, ids[k], ids[(k + 1) % len(ids)]))
    jn.pad_loop = loop


def _kerb_run(kit, jn, st, name, cap_start=True, cap_end=True):
    """A kerb along a station line: its face to the road, 10 mm arris, top; ends capped."""
    p = kit.piece("kerbstone", name)
    lo, cz, top, kw = -0.30, jn.channel_z, jn.kerb_top, jn.kerb_w
    prof = [(0.0, lo), (0.0, top - 0.010), (0.010, top), (kw, top)]   # (into the land, z)
    rows = []
    for k in range(len(st.pts)):
        rows.append([(st.pts[k][0] + st.nrm[k][0] * d * st.scl[k], st.pts[k][1] + st.nrm[k][1] * d * st.scl[k], z)
                     for d, z in prof])
    # the faces must face the road (away from the land) or up
    cols = list(zip(*rows))                        # each column: one profile point along the run
    for i in range(len(prof) - 1):
        a, b = cols[i], cols[i + 1]
        for k in range(len(a) - 1):
            q = [a[k], a[k + 1], b[k + 1], b[k]]
            n = st.nrm[k]
            hint = (-n[0], -n[1], 0.6) if i < 2 else (0.0, 0.0, 1.0)
            kit.face(p, q, hint)
    for k, on in ((0, cap_start), (len(rows) - 1, cap_end)):
        if not on:
            continue
        ring = rows[k] + [(rows[k][-1][0], rows[k][-1][1], lo)]
        t = norm2(v2(st.pts[1], st.pts[0])) if k == 0 else norm2(v2(st.pts[-2], st.pts[-1]))
        kit.face(p, ring, (t[0], t[1], 0.0))


def _kerbs_and_footways(kit, jn):
    _kerb_run(kit, jn, jn.nw, "kerb_northwest_corner", cap_start=False)
    _kerb_run(kit, jn, jn.ne, "kerb_northeast_corner", cap_start=False)
    _kerb_run(kit, jn, jn.s, "kerb_south_quay_side")
    up = (0.0, 0.0, 1.0)
    for st, name in ((jn.nw, "footway_northwest_corner"), (jn.ne, "footway_northeast_corner")):
        p = kit.piece("paving", name)
        a = [(q[0], q[1], jn.kerb_top) for q in st.offset(jn.kerb_w)]
        b = [(q[0], q[1], jn.footway_z_at(FOOTWAY_W_M)) for q in st.offset(jn.kerb_w + FOOTWAY_W_M)]
        kit.ribbon(p, [a, b], up)
        # the footway's far end, faced, down to the road's base
        n = len(a) - 1
        t = norm2(v2(st.pts[-2], st.pts[-1]))
        kit.face(p, [a[n], b[n], (b[n][0], b[n][1], -0.30), (a[n][0], a[n][1], -0.30)], (t[0], t[1], 0.0))


def _markings(kit, jn):
    """The street's lines carried on (terrace-front.py: double yellows 2.5/2.7 m from the centre,
    the diagram 1008 centre line 2 m marks 4 m gaps from x = -2), and the diagram 1003 give-way
    line across the Harbour Board approach's mouth (research section 6)."""
    y_p = kit.piece("paint_yellow", "double_yellow_lines_south")
    for sgn, x_end in ((-1.0, jn.nw_T[0][0]), (1.0, jn.ne_T[0][0])):
        for across in (2.5, 2.7):
            a, b = sgn * across, sgn * (across + 0.1)
            za = -min(abs(a), jn.half) * jn.fall
            zb = -min(abs(b), jn.half) * jn.fall
            kit.box(y_p, x_end, jn.join_x, min(a, b), max(a, b), zb - 0.006, za + 0.012, skip=("bottom",))
    w_p = kit.piece("paint_white", "road_markings_south")
    # arm N: the street's marks run -2..0, 4..6 ... so the ones south of it are -8..-6, -14..-12 ...
    xm = jn.join_x - 4.0
    while xm - 2.0 >= jn.xN_in + 0.5:
        kit.box(w_p, xm - 2.0, xm, -0.05, 0.05, -0.004, 0.003, skip=("bottom",))
        xm -= 6.0
    # arm W: on its crown from 2 m past its corners
    L = math.hypot(*v2(jn.J, jn.W_end))
    s = jn.sW_in + 2.0
    while s + 2.0 <= L - 1.0:
        c = add2(jn.J, jn.dW, s + 1.0)
        kit.obox(w_p, c, jn.dW, 1.0, 0.05, -0.004, 0.003, skip=("bottom",))
        s += 6.0
    # arm E: give way, two broken lines 200 mm wide 300 mm apart, 600 mm marks 300 mm gaps, across
    # the entry half (south of the crown, where traffic for the junction keeps left)
    for k, off in enumerate((0.0, 0.5)):
        sc = jn.sE_in + 0.2 + off
        u = 0.0
        while u + 0.6 <= jn.half - 0.15 + 1e-9:
            c = add2(add2(jn.J, jn.dE1, sc + 0.1), jn.nE1_left, u + 0.3 + 0.05)
            z0 = -min(u + 0.65, jn.half) * jn.fall
            z1 = -min(u, jn.half) * jn.fall
            kit.obox(w_p, c, jn.dE1, 0.1, 0.3, z0 - 0.004, z1 + 0.003, skip=("bottom",))
            u += 0.9
    # and its own centre line on past the give way
    LE = math.hypot(*v2(jn.E_pts[0], jn.E_pts[1]))
    s = jn.sE_in + 3.0
    while s + 2.0 <= LE - 0.5:
        kit.obox(w_p, add2(jn.J, jn.dE1, s + 1.0), jn.dE1, 1.0, 0.05, -0.004, 0.003, skip=("bottom",))
        s += 6.0


# ---- the quay ------------------------------------------------------------------------------------
def _quay(kit, jn, at, zg, zw, yard_z):
    xq = at["north_quay_x"]                        # -70
    yw = at["basin_west_y"]                        # -100
    ye = at["basin_east_y"]                        # +40
    jx0, jx1 = at["jetty_x"]                       # -130, -110
    jy = at["jetty_end_y"]                         # -15
    cA, cB = at["east_coast"]                      # (-170, 40), (-155, 220)
    cw = COPING_W_M
    # the coast of the east land, from the basin's corner out, and where it reaches EAST_LAND_TO_Y
    cdir = norm2(v2(cA, cB))
    c_far = add2(cA, cdir, (EAST_LAND_TO_Y_M - cA[1]) / cdir[1])
    c_in = (cdir[1], -cdir[0])                    # into the land (toward +x)
    if c_in[0] < 0:
        c_in = (-c_in[0], -c_in[1])

    # ---- the ground: one level apron, laid flush with the S kerb's top ----
    sback = jn.s.offset(jn.kerb_w)
    corner_e = line_x((xq, ye + cw), (1.0, 0.0), add2(cA, c_in, cw), cdir)
    poly = list(sback)
    poly += [(sback[-1][0], EAST_LAND_TO_Y_M), add2(c_far, c_in, cw), corner_e,
             (xq + cw, ye + cw), (xq + cw, yw - cw), (jx1 - cw, yw - cw), (jx1 - cw, jy - cw),
             (jx0 + cw, jy - cw), (jx0 + cw, WEST_LAND_TO_Y_M), (sback[0][0], WEST_LAND_TO_Y_M)]
    kit.fill(kit.piece("quay_stone", "apron_setts"), poly, zg)
    # the kit's open ends (east land's far edge, west land's far edge): faced down to the water
    edge = kit.piece("quay_stone", "ground_edges")
    zb = zw - WALL_BELOW_WATER_M
    for a, b, out in ((poly[len(sback)], poly[len(sback) + 1], (0.0, 1.0)),        # the east land's far edge
                      (poly[-2], poly[-1], (0.0, -1.0)),                            # the west land's far edge
                      (sback[-1], poly[len(sback)], (1.0, 0.0)),                    # past the approach's end
                      ((sback[0][0], WEST_LAND_TO_Y_M), (-2.0, WEST_LAND_TO_Y_M), (0.0, -1.0)),  # the west land's end
                      ((-2.0, WEST_LAND_TO_Y_M), (-2.0, -91.2), (1.0, 0.0))):
        kit.face(edge, [(a[0], a[1], zg), (b[0], b[1], zg), (b[0], b[1], zb), (a[0], a[1], zb)],
                 (out[0], out[1], 0.0))
    # the NE ground: behind the NE footway, level with its back, out to the lane by Mickey's flank
    neb = jn.ne.offset(jn.kerb_w + FOOTWAY_W_M)
    poly_ne = list(neb) + [(neb[-1][0], FORECOURT_TO_Y_M), (jn.join_x, FORECOURT_TO_Y_M), (jn.join_x, 25.0),
                           (3.0, 25.0), (3.0, 13.725), (jn.join_x, 13.725)]
    kit.fill(kit.piece("quay_stone", "hard_standing_northeast"), poly_ne, yard_z)
    # the Harbour Board's forecourt where the approach ends: flush with the kerbs, a kerb's step up
    # from the road's end, between the apron's edge and the NE footway's back
    end_s = sback[-1]
    end_n = neb[-1]
    kit.fill(kit.piece("quay_stone", "harbour_board_forecourt"),
             [end_s, end_n, (end_n[0], FORECOURT_TO_Y_M), (end_s[0], FORECOURT_TO_Y_M)], zg)
    d2 = jn.dE2
    secE = jn.arm_section(jn.E_pts[2], jn.nE2_left)
    step = kit.piece("kerbstone", "kerb_harbour_board_forecourt")
    for a, b in zip(secE[:-1], secE[1:]):
        za, zb_ = jn.road_z(a), jn.road_z(b)
        kit.face(step, [(a[0], a[1], za - 0.01), (b[0], b[1], zb_ - 0.01), (b[0], b[1], zg), (a[0], a[1], zg)],
                 (-d2[0], -d2[1], 0.0))
    # the west land past the west road's end, out to the cold stores
    wend_s = sback[0]
    nwb_ = jn.nw.offset(jn.kerb_w + FOOTWAY_W_M)
    wend_n = nwb_[-1]
    kit.fill(kit.piece("quay_stone", "west_land"),
             [wend_s, (wend_s[0], WEST_LAND_TO_Y_M), (jn.join_x, WEST_LAND_TO_Y_M), (jn.join_x, wend_n[1]), wend_n], zg)
    secW = jn.arm_section(jn.W_end, jn.nW_left)
    for a, b in zip(secW[:-1], secW[1:]):
        za, zb_ = jn.road_z(a), jn.road_z(b)
        kit.face(kit.piece("kerbstone", "kerb_west_road_end"),
                 [(a[0], a[1], za - 0.01), (b[0], b[1], zb_ - 0.01), (b[0], b[1], zg), (a[0], a[1], zg)],
                 (-jn.dW[0], -jn.dW[1], 0.0))
    # the NW yard, behind its wall
    nwb = jn.nw.offset(jn.kerb_w + FOOTWAY_W_M)
    poly_nw = list(nwb) + [(jn.join_x, nwb[-1][1])]
    kit.fill(kit.piece("quay_stone", "yard_northwest"), poly_nw, yard_z)

    # ---- copings and quay walls: (start, end) of the nose line, the land on the left or right ----
    runs = [
        # name, nose from, nose to, land normal, extend at start, extend at end
        ("north_quay", (xq, yw - cw), (xq, ye + cw), (1.0, 0.0)),
        ("east_quay", (cA[0], ye), (xq, ye), (0.0, 1.0)),
        ("west_quay", (jx1, yw), (xq, yw), (0.0, -1.0)),
        ("jetty_north", (jx1, yw - cw), (jx1, jy), (-1.0, 0.0)),
        ("jetty_end", (jx0, jy), (jx1 - cw, jy), (0.0, -1.0)),
        ("jetty_south_and_west_shore", (jx0, WEST_LAND_TO_Y_M), (jx0, jy - cw), (1.0, 0.0)),
        ("east_shore", add2(cA, cdir, cw / cdir[1]), c_far, c_in),
    ]
    cope = kit.piece("stone", "quay_coping")
    wall = kit.piece("quay_stone", "quay_walls")
    edges = {}
    for name, a, b, n in runs:
        _coping_run(kit, cope, wall, a, b, n, zg, zw)
        edges[name] = (a, b)
    # ---- the water: the basin and the sea, out to the horizon ----
    w = kit.piece("harbour_water", "harbour_and_sea")
    xs = [xq, -150.0, -400.0, -1200.0, WATER_FAR_X_M]
    ys = [-WATER_HALF_Y_M, -1200.0, -300.0, 0.0, 300.0, 1200.0, WATER_HALF_Y_M]
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            x0, x1 = xs[i + 1], xs[i]
            y0, y1 = ys[j], ys[j + 1]
            kit.face(w, [(x0, y0, zw), (x1, y0, zw), (x1, y1, zw), (x0, y1, zw)], (0, 0, 1))
    return {"quay_edge_x": xq, "edges": edges, "water_far_x": WATER_FAR_X_M,
            "water_half_y": WATER_HALF_Y_M, "ground_poly": poly}


def _coping_run(kit, cope, wall, a, b, n, zg, zw):
    """A cope along the nose line a->b with the land toward n: 0.6 m of granite, its nose rounded
    off in two steps, 50 mm proud of the battered wall below, which runs down under the water."""
    t = norm2(v2(a, b))
    L = math.hypot(*v2(a, b))
    # profile across, (into the land, z): the nose to the back
    prof = [(0.0, zg - COPING_T_M), (0.0, zg - 0.035), (0.010, zg - 0.010), (0.035, zg),
            (COPING_W_M, zg)]
    rows = [[(a[0] + n[0] * d, a[1] + n[1] * d, z) for d, z in prof],
            [(b[0] + n[0] * d, b[1] + n[1] * d, z) for d, z in prof]]
    for i in range(len(prof) - 1):
        q = [rows[0][i], rows[1][i], rows[1][i + 1], rows[0][i + 1]]
        kit.face(cope, q, (-n[0], -n[1], 1.0) if i < 3 else (0, 0, 1))
    # the coping's underside where it overhangs the wall
    kit.face(cope, [rows[0][0], (a[0] + n[0] * COPING_NOSE_M, a[1] + n[1] * COPING_NOSE_M, zg - COPING_T_M),
                    (b[0] + n[0] * COPING_NOSE_M, b[1] + n[1] * COPING_NOSE_M, zg - COPING_T_M), rows[1][0]],
             (0, 0, -1))
    # its two ends
    for P, sgn in ((rows[0], -1.0), (rows[1], 1.0)):
        ring = P + [(P[-1][0], P[-1][1], zg - COPING_T_M)]
        kit.face(cope, ring, (t[0] * sgn, t[1] * sgn, 0.0))
    # the wall: from under the coping, leaning back 1 in 20, to a metre under half-tide
    top = zg - COPING_T_M
    bot = zw - WALL_BELOW_WATER_M
    lean = (top - bot) * QUAY_BATTER
    w0 = (a[0] + n[0] * COPING_NOSE_M, a[1] + n[1] * COPING_NOSE_M)
    w1 = (b[0] + n[0] * COPING_NOSE_M, b[1] + n[1] * COPING_NOSE_M)
    f0 = (w0[0] - n[0] * lean, w0[1] - n[1] * lean)
    f1 = (w1[0] - n[0] * lean, w1[1] - n[1] * lean)
    kit.face(wall, [(w0[0], w0[1], top), (f0[0], f0[1], bot), (f1[0], f1[1], bot), (w1[0], w1[1], top)],
             (-n[0], -n[1], 0.0))
    # its ends, so an outside corner shows no slot
    for w_, f_, sgn in ((w0, f0, -1.0), (w1, f1, 1.0)):
        back = (w_[0] + n[0] * (COPING_W_M - COPING_NOSE_M), w_[1] + n[1] * (COPING_W_M - COPING_NOSE_M))
        kit.face(wall, [(w_[0], w_[1], top), (back[0], back[1], top), (back[0], back[1], bot), (f_[0], f_[1], bot)],
                 (t[0] * sgn, t[1] * sgn, 0.0))


# ---- the west flank: a yard wall and a net store ------------------------------------------------
def _yard_wall_and_store(kit, jn, yard_z):
    """Brick yard walls along both corners' footway backs: on the west round the corner and along
    the west road, with a net store behind it, gable on; on the east round the corner and along the
    Harbour Board approach to the store there, the wall across the street's corner footway making
    the south side of Mickey's yard lane."""
    _yard_wall(kit, jn, jn.nw, "northwest", yard_z, gate=(jn.join_x - 14.5, jn.join_x - 17.5),
               stop_y=None, cross_to_y=-13.725)
    _yard_wall(kit, jn, jn.ne, "northeast", yard_z, gate=(jn.join_x - 9.0, jn.join_x - 12.0),
               stop_y=42.5, cross_to_y=25.0)
    _building(kit, "net_store", -16.0, -5.2, -14.5, -7.0, yard_z, 1, "gable_x", "brick_grey",
              faces={"xmin": {"bays": 1, "door_bays": [0], "gable_door": True},
                     "xmax": {"bays": 1, "door_bays": [0]},
                     "ymax": {"bays": 3}},
              chimneys=[])


def _cut_at_y(line, y_stop):
    """The polyline up to where it first passes y = y_stop (moving away from the street)."""
    out = [line[0]]
    for a, b in zip(line[:-1], line[1:]):
        if (a[1] - y_stop) * (b[1] - y_stop) <= 0 and abs(b[1] - a[1]) > 1e-9:
            t = (y_stop - a[1]) / (b[1] - a[1])
            out.append((a[0] + (b[0] - a[0]) * t, y_stop))
            return out
        out.append(b)
    return out


def _yard_wall(kit, jn, st, side, yard_z, gate, stop_y, cross_to_y):
    brick = kit.piece("brick_red", "yard_wall_" + side)
    cope = kit.piece("stone", "yard_wall_coping_" + side)
    t = YARD_WALL_T_M
    base = yard_z - 0.04
    top = yard_z + YARD_WALL_H_M
    off0 = jn.kerb_w + FOOTWAY_W_M
    inner = st.offset(off0)                        # the face to the footway
    outer = st.offset(off0 + t)                    # the yard's side
    if stop_y is not None:
        inner = _cut_at_y(inner, stop_y)
        outer = _cut_at_y(outer, stop_y)
        n = min(len(inner), len(outer))
        inner, outer = inner[:n], outer[:n]
    gate_from, gate_to = gate                      # x, on the first straight

    def cut(line):
        first, rest = [line[0]], []
        for q in line[1:]:
            (first if q[0] > gate_from + 1e-6 else rest).append(q)
        y0 = line[0][1]
        return first + [(gate_from, y0)], [(gate_to, y0)] + rest

    ia, ib = cut(inner)
    oa, ob = cut(outer)
    for I, Ou in ((ia, oa), (ib, ob)):
        for k in range(len(I) - 1):
            a0, a1, b0, b1 = I[k], I[k + 1], Ou[k], Ou[k + 1]
            mid_in = ((a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2)
            mid_out = ((b0[0] + b1[0]) / 2, (b0[1] + b1[1]) / 2)
            r = norm2(v2(mid_out, mid_in))            # toward the road
            kit.face(brick, [(a0[0], a0[1], base), (a1[0], a1[1], base), (a1[0], a1[1], top),
                             (a0[0], a0[1], top)], (r[0], r[1], 0))
            kit.face(brick, [(b0[0], b0[1], base), (b1[0], b1[1], base), (b1[0], b1[1], top),
                             (b0[0], b0[1], top)], (-r[0], -r[1], 0))
            ci0, ci1 = add2(a0, r, 0.05), add2(a1, r, 0.05)
            co0, co1 = add2(b0, r, -0.05), add2(b1, r, -0.05)
            for p0, p1, hh in ((ci0, ci1, r), (co0, co1, (-r[0], -r[1]))):
                kit.face(cope, [(p0[0], p0[1], top), (p1[0], p1[1], top), (p1[0], p1[1], top + 0.08),
                                (p0[0], p0[1], top + 0.08)], (hh[0], hh[1], 0))
            kit.face(cope, [(ci0[0], ci0[1], top + 0.08), (ci1[0], ci1[1], top + 0.08),
                            (co1[0], co1[1], top + 0.08), (co0[0], co0[1], top + 0.08)], (0, 0, 1))
            kit.face(cope, [(ci0[0], ci0[1], top), (ci1[0], ci1[1], top),
                            (co1[0], co1[1], top), (co0[0], co0[1], top)], (0, 0, -1))
        for k, sgn in ((0, -1.0), (len(I) - 1, 1.0)):
            d = norm2(v2(I[0], I[1])) if k == 0 else norm2(v2(I[-2], I[-1]))
            kit.face(brick, [(I[k][0], I[k][1], base), (Ou[k][0], Ou[k][1], base),
                             (Ou[k][0], Ou[k][1], top + 0.08), (I[k][0], I[k][1], top + 0.08)],
                     (d[0] * sgn, d[1] * sgn, 0))
    # piers every 4.5 m along the wall's middle line, at the gate posts and at the ends
    mid = [((q[0] + o[0]) / 2, (q[1] + o[1]) / 2) for q, o in zip(inner, outer)]
    piers, run, need = [], 0.0, 4.5
    for k in range(len(mid) - 1):
        a, b = mid[k], mid[k + 1]
        L = math.hypot(*v2(a, b))
        s = need - run
        while s <= L - 0.8:
            q = add2(a, norm2(v2(a, b)), s)
            if not (gate_to - 0.6 < q[0] < gate_from + 0.6 and abs(q[1] - mid[0][1]) < 0.5):
                piers.append((q, norm2(v2(a, b))))
            s += need
        run = (run + L) % need
    yc = mid[0][1]
    piers += [(mid[0], norm2(v2(mid[0], mid[1]))), (mid[-1], norm2(v2(mid[-2], mid[-1]))),
              ((gate_from, yc), (1.0, 0.0)), ((gate_to, yc), (1.0, 0.0))]
    pier = kit.piece("brick_red", "yard_wall_piers_" + side)
    pcap = kit.piece("stone", "yard_wall_pier_caps_" + side)
    for c, u in piers:
        kit.obox(pier, c, u, 0.23, 0.23, base, top + 0.20, skip=("bottom",))
        kit.obox(pcap, c, u, 0.29, 0.29, top + 0.20, top + 0.30, skip=("bottom",))
    # the gates, a pair of boarded leaves, shut, with their meeting stile
    gate_p = kit.piece("paint_door", "yard_gates_" + side)
    kit.box(gate_p, gate_to + 0.23, gate_from - 0.23, yc - 0.03, yc + 0.03, yard_z + 0.05, top + 0.05,
            skip=("bottom",))
    kit.box(gate_p, (gate_to + gate_from) / 2 - 0.04, (gate_to + gate_from) / 2 + 0.04, yc - 0.05, yc + 0.05,
            yard_z + 0.05, top + 0.05, skip=("bottom",))
    # the wall across the street's corner footway's end (x just south of the street's end), from
    # this wall's back out to cross_to_y
    x0 = jn.join_x - t
    yb = inner[0][1] + math.copysign(t, inner[0][1])
    y_a, y_b = min(yb, cross_to_y), max(yb, cross_to_y)
    kit.box(brick, x0, jn.join_x, y_a, y_b, base, top, skip=("bottom",))
    kit.box(cope, x0 - 0.05, jn.join_x + 0.05, y_a, y_b, top, top + 0.08, skip=("bottom",))
    kit.box(pier, x0 - 0.06, jn.join_x + 0.06, cross_to_y - 0.23 if cross_to_y > 0 else cross_to_y,
            cross_to_y if cross_to_y > 0 else cross_to_y + 0.23, base, top + 0.20, skip=("bottom",))


# ---- boats alongside -------------------------------------------------------------------------------
#: Three inshore boats lying alongside at half tide, generic (no names, no numbers, no maker):
#: (name, centre (x, y), bow heading (unit), length, beam, hull material, quay side +1 port / -1 starboard,
#:  the bollards their lines go to). Sizes CHOSEN, no source reached (research section 7).
BOATS = (
    ("boat_north_quay", (-72.55, -8.0), (0.0, 1.0), 12.0, 4.2, "frame_painted", -1, ((-69.25, 2.0), (-69.25, -28.0))),
    ("boat_east_quay", (-100.0, 37.45), (-1.0, 0.0), 13.0, 4.4, "paint_door", -1, ((-115.0, 40.75), (-95.0, 40.75))),
    ("boat_jetty", (-107.75, -58.0), (0.0, 1.0), 10.0, 3.8, "paint_door", 1, ((-110.75, -45.0), (-110.75, -80.0))),
)
BOAT_FREEBOARD_M, BOAT_DRAUGHT_M = 1.10, 1.6


def _boats(kit, zw, zg):
    for name, c, h, L, B, hull_mat, quay_side, lines in BOATS:
        _boat(kit, name, c, h, L, B, hull_mat, quay_side, lines, zw, zg)


def _boat(kit, name, c, h, L, B, hull_mat, quay_side, lines, zw, zg):
    h = norm2(h)
    port = left2(h)

    def W_(a, b, z):
        q = add2(add2(c, h, a), port, b)
        return (q[0], q[1], z)
    F, D = BOAT_FREEBOARD_M, BOAT_DRAUGHT_M
    N = 10
    st = []
    for k in range(N + 1):
        tt = k / N
        a = -L / 2 + L * tt
        if tt <= 0.45:
            f = 0.84 + 0.16 * math.sin(math.pi * tt / 0.9)
        else:
            f = max(0.03, math.sqrt(max(0.0, 1.0 - ((tt - 0.45) / 0.55) ** 2)))
        hb = B / 2 * f
        zd = zw + F + 0.55 * tt ** 2
        keel = zw - D * (1.0 if tt < 0.85 else max(0.2, 1.0 - (tt - 0.85) / 0.15 * 0.8))
        sec = [(hb, zd), (0.92 * hb, zw + 0.15), (0.62 * hb, zw - 0.65 * D), (0.0, keel),
               (-0.62 * hb, zw - 0.65 * D), (-0.92 * hb, zw + 0.15), (-hb, zd)]
        st.append((a, sec))
    hull = kit.piece(hull_mat, name + "_hull")
    rows = [[W_(a, b, z) for b, z in sec] for a, sec in st]
    for k in range(N):
        for i in range(len(rows[0]) - 1):
            q = [rows[k][i], rows[k + 1][i], rows[k + 1][i + 1], rows[k][i + 1]]
            mid = tuple(sum(p[j] for p in q) / 4 for j in range(3))
            axis = W_((st[k][0] + st[k + 1][0]) / 2, 0.0, zw - 0.3)
            kit.face(hull, q, (mid[0] - axis[0], mid[1] - axis[1], mid[2] - axis[2]))
    # the transom and the stem
    kit.face(hull, rows[0], (-h[0], -h[1], 0.0))
    kit.face(hull, list(reversed(rows[-1])), (h[0], h[1], 0.0))
    # deck, a white gunwale, the wheelhouse aft, a mast forward
    deck = kit.piece("prop_timber", name + "_deck")
    plan = [(a, sec[0][0]) for a, sec in st] + [(a, sec[-1][0]) for a, sec in reversed(st)]
    zs = [sec[0][1] for a, sec in st] + [sec[-1][1] for a, sec in reversed(st)]
    tris = ear_clip(plan)
    ids = kit.verts(deck, [W_(a, b, z - 0.12) for (a, b), z in zip(plan, zs)])
    for a_, b_, c_ in tris:
        f = (ids[a_], ids[b_], ids[c_])
        pts = [deck["verts"][i] for i in f]
        if newell(pts)[2] < 0:
            f = (f[0], f[2], f[1])
        deck["faces"].append(f)
    white = kit.piece("paint_white", name + "_gunwale_and_wheelhouse")
    for side in (0, -1):
        top_row = [W_(a, sec[side][0] * 1.005, sec[side][1] + 0.10) for a, sec in st]
        bot_row = [W_(a, sec[side][0] * 1.005, sec[side][1] - 0.06) for a, sec in st]
        sgn = 1.0 if side == 0 else -1.0
        kit.ribbon(white, [bot_row, top_row], lambda pts, s=sgn: (port[0] * s, port[1] * s, 0.0))
    ta = -0.22 * L
    zd0 = zw + F + 0.55 * 0.28 ** 2
    cwh = add2(c, h, ta)
    kit.obox(white, cwh, h, 0.11 * L, 0.33 * B, zd0 - 0.2, zd0 + 2.05, skip=("bottom",))
    kit.obox(white, cwh, h, 0.11 * L + 0.12, 0.33 * B + 0.12, zd0 + 2.05, zd0 + 2.15, skip=())
    glass = kit.piece("glass", name + "_wheelhouse_windows")
    kit.obox(glass, add2(cwh, h, 0.11 * L + 0.004), h, 0.006, 0.30 * B, zd0 + 1.25, zd0 + 1.85, skip=("bottom",))
    for s in (-1.0, 1.0):
        kit.obox(glass, add2(add2(cwh, port, s * (0.33 * B + 0.004)), h, 0.02 * L), h, 0.06 * L, 0.006,
                 zd0 + 1.25, zd0 + 1.85, skip=("bottom",))
    metal = kit.piece("galvanised", name + "_mast")
    am = 0.24 * L
    zdm = zw + F + 0.55 * 0.74 ** 2
    pm = add2(c, h, am)
    kit.strut(metal, (pm[0], pm[1], zdm - 0.1), (pm[0], pm[1], zdm + 6.4), 0.07)
    # a derrick from the mast's foot aft and up, at rest
    pd = add2(c, h, am - 3.0)
    kit.strut(metal, (pm[0], pm[1], zdm + 1.0), (pd[0], pd[1], zdm + 3.2), 0.05)
    # lines to the quay: bow and stern, each sagging once on its way to its bollard
    rope = kit.piece("rope", "mooring_lines")
    ends = (W_(0.42 * L, quay_side * st[9][1][0][0] * 0.7, zw + F + 0.5), W_(-0.45 * L, quay_side * B * 0.38, zw + F + 0.05))
    for e, bol in zip(ends, lines):
        top = (bol[0], bol[1], zg + 0.55)
        mid = ((e[0] + top[0]) / 2, (e[1] + top[1]) / 2, (e[2] + top[2]) / 2 - 0.35)
        for p0, p1 in ((e, mid), (mid, top)):
            _rope_seg(kit, rope, p0, p1, 0.016)


def _rope_seg(kit, p, a, b, r):
    """A thin square rope between two points at any angle."""
    d = sub3(b, a)
    L = math.sqrt(dot3(d, d))
    u = (d[0] / L, d[1] / L, d[2] / L)
    ref = (0.0, 0.0, 1.0) if abs(u[2]) < 0.9 else (1.0, 0.0, 0.0)
    s = cross3(u, ref)
    sl = math.sqrt(dot3(s, s))
    s = (s[0] / sl, s[1] / sl, s[2] / sl)
    t = cross3(u, s)
    ring = []
    for c in (a, b):
        for e1, e2 in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            ring.append(tuple(c[k] + r * (e1 * s[k] + e2 * t[k]) for k in range(3)))
    ids = kit.verts(p, ring)
    for i in range(4):
        j = (i + 1) % 4
        q = (ids[i], ids[j], ids[4 + j], ids[4 + i])
        pts = [p["verts"][k] for k in q]
        ctr = tuple(sum(x[k] for x in pts) / 4 for k in range(3))
        axis = tuple((a[k] + b[k]) / 2 for k in range(3))
        if dot3(newell(pts), sub3(ctr, axis)) < 0:
            q = tuple(reversed(q))
        p["faces"].append(q)


# ---- buildings ------------------------------------------------------------------------------------
#: The Hook's dockside row along the east quay, and a store north of the approach. Each wall's spec:
#: bays (windows evenly spaced, one per bay per storey), from_floor (the lowest storey with windows),
#: door_bays, loading (the bay that is a hauling way: a cart door, loading doors above, a hood),
#: gable_window / gable_door (in the gable over the eaves), band (the blank painted name band),
#: party (a wall against a neighbour: no gutter).
BUILDINGS = (
    # name, x0, x1, y0, y1, storeys, roof, wall, faces, chimneys (x, y)
    ("b1_store_by_the_approach", -24.0, -4.0, 44.0, 56.0, 2, "gable_x", "brick_red",
     {"xmin": {"bays": 4, "door_bays": [1], "loading": 2}, "xmax": {"bays": 4},
      "ymin": {"bays": 6}}, [(-6.5, 50.0)]),
    ("b3_warehouse", -86.0, -61.0, 58.0, 71.0, 3, "gable_x", "brick_red",
     {"ymin": {"bays": 8, "loading": 4}, "xmax": {"bays": 4, "door_bays": [1], "gable_window": True},
      "xmin": {"party": True}}, [(-64.0, 64.5), (-83.0, 64.5)]),
    ("b4_warehouse_name_band", -112.0, -86.0, 58.4, 71.4, 4, "gable_x", "brick_grey",
     {"ymin": {"bays": 7, "loading": 3, "band": True}, "xmax": {"party": True, "gable_window": True},
      "xmin": {"party": True, "gable_window": True}}, [(-89.0, 64.9), (-109.0, 64.9)]),
    ("b5_fish_store", -127.0, -112.0, 58.2, 68.4, 2, "gable_y", "brick_red",
     {"ymin": {"bays": 3, "loading": 1, "gable_door": True}, "xmin": {"party": True},
      "xmax": {"party": True}}, []),
    # the atlas's H04 (east 450..550, north 335..390): its front range, behind Mickey's yard lane
    ("b2_back_range", -2.0, 18.0, 52.0, 64.0, 2, "gable_x", "brick_grey",
     {"ymin": {"bays": 7, "door_bays": [2]}, "xmin": {"bays": 3}}, [(15.5, 58.0)]),
    # the Harbour Board's office where its approach ends (atlas landmark H3, (510, 320))
    # (its south side kept clear of the atlas's Sea Road, which leaves the approach's bend at
    # (460, 315) for (580, 300) and passes about x = -41 here)
    ("harbour_board_office", -36.0, -13.0, 112.0, 126.0, 2, "hip", "brick_red",
     {"ymin": {"bays": 7, "door_bays": [3]}, "xmin": {"bays": 3}, "xmax": {"bays": 3}},
     [(-17.0, 119.0), (-32.0, 119.0)]),
    # the atlas's H05 (east 475..570, north 230..280), behind the quay row: two ranges
    ("b7_rear_range", -118.0, -72.0, 76.0, 92.0, 3, "gable_x", "brick_grey",
     {"xmax": {"bays": 4, "loading": 1}, "ymin": {"bays": 11}}, [(-80.0, 84.0), (-110.0, 84.0)]),
    ("b8_rear_store", -118.0, -72.0, 96.0, 126.0, 2, "hip", "brick_red",
     {"xmax": {"bays": 7, "door_bays": [3]}, "ymin": {"bays": 10, "loading": 4}}, [(-95.0, 111.0)]),
    ("b9_rear_range_south", -118.0, -72.0, 130.0, 148.0, 3, "gable_x", "brick_red",
     {"xmax": {"bays": 4, "loading": 1}, "ymin": {"bays": 10}}, [(-80.0, 139.0), (-110.0, 139.0)]),
    ("b10_rear_range_far", -118.0, -76.0, 152.0, 170.0, 2, "gable_x", "brick_grey",
     {"xmax": {"bays": 4}, "ymin": {"bays": 9}}, [(-97.0, 161.0)]),
    # the Old Basin Cold Stores where the west road turns for the jetty (atlas WT_COLD, (245, 310)):
    # an adapted older shed, its gable to the junction
    ("cold_stores", -54.0, -24.0, -178.0, -136.0, 2, "gable_y", "brick_grey",
     {"ymax": {"bays": 4, "loading": 1, "gable_door": True}, "xmax": {"bays": 9, "door_bays": [4]},
      "xmin": {"bays": 9}}, [(-39.0, -140.0)]),
    ("b6_warehouse_hipped", -160.0, -127.0, 58.6, 72.6, 3, "hip", "brick_red",
     {"ymin": {"bays": 10, "loading": 6}, "xmin": {"bays": 4},
      "xmax": {"party": True, "bays": 4, "from_floor": 2}}, [(-136.0, 65.6), (-151.0, 65.6)]),
)


def _buildings(kit, zg, yard_z):
    for name, x0, x1, y0, y1, n, roof, wall, faces, chim in BUILDINGS:
        z = yard_z if name.startswith(("b1", "b2")) else zg
        _building(kit, name, x0, x1, y0, y1, z, n, roof, wall, faces, chim)


def _face_frames(x0, x1, y0, y1):
    """Each wall: (origin, U along it seen from outside, outward N, width)."""
    return {
        "ymin": ((x0, y0), (1.0, 0.0), (0.0, -1.0), x1 - x0),
        "ymax": ((x1, y1), (-1.0, 0.0), (0.0, 1.0), x1 - x0),
        "xmin": ((x0, y1), (0.0, -1.0), (-1.0, 0.0), y1 - y0),
        "xmax": ((x1, y0), (0.0, 1.0), (1.0, 0.0), y1 - y0),
    }


def _storeys(zg, n):
    floors = [zg]
    for k in range(1, n):
        floors.append(zg + STOREY_GROUND_M + STOREY_UPPER_M * (k - 1))
    eaves = zg + STOREY_GROUND_M + STOREY_UPPER_M * (n - 1)
    return floors, eaves


def _openings(W, floors, spec):
    """Rectangular openings (u0, u1, z0, z1, kind) for a wall of width W."""
    ops = []
    nb = spec.get("bays", 0)
    load = spec.get("loading")
    doors = spec.get("door_bays", [])
    f0 = spec.get("from_floor", 0)
    for i in range(nb):
        uc = W * (i + 0.5) / nb
        for k, fz in enumerate(floors):
            if i == load:
                if k == 0:
                    ops.append((uc - 1.30, uc + 1.30, fz, fz + 3.0, "cart_door"))
                else:
                    ops.append((uc - 0.65, uc + 0.65, fz + 0.05, fz + 2.15, "loading_door"))
            elif k == 0 and i in doors:
                ops.append((uc - 0.50, uc + 0.50, fz, fz + 2.20, "door"))
            elif k < f0:
                continue
            elif k == 0:
                ops.append((uc - 0.475, uc + 0.475, fz + 0.95, fz + 2.65, "window"))
            else:
                ops.append((uc - 0.475, uc + 0.475, fz + 0.85, fz + 2.40, "window"))
    return ops


#: Wide sheds take a lower pitch than the terrace's 35 degrees (CHOSEN, research section 8): over a
#: 30 m span a 35-degree slate roof would stand 10 m tall.
ROOF_PITCH_OVERRIDE_DEG = {"cold_stores": 22.0, "b8_rear_store": 25.0}


def _building(kit, name, x0, x1, y0, y1, zg, n, roof, wall_mat, faces, chimneys):
    floors, eaves = _storeys(zg, n)
    pitch = math.radians(ROOF_PITCH_OVERRIDE_DEG.get(name, ROOF_PITCH_DEG))
    base = zg - 0.25
    frames = _face_frames(x0, x1, y0, y1)
    wall = kit.piece(wall_mat, name + "_walls")
    for key, (O, U, N, W) in frames.items():
        spec = faces.get(key, {})
        ops = _openings(W, floors, spec)
        gable = (roof == "gable_x" and key in ("xmin", "xmax")) or (roof == "gable_y" and key in ("ymin", "ymax"))
        rise = (W / 2.0) * math.tan(pitch) if gable else 0.0
        uc = W / 2.0
        if gable and spec.get("gable_door"):
            ops.append((uc - 0.6, uc + 0.6, eaves + 0.15, eaves + 2.0, "loading_door"))
        elif gable and spec.get("gable_window") and rise > 2.2:
            ops.append((uc - 0.45, uc + 0.45, eaves + 0.35, eaves + 1.65, "window"))
        _facade(kit, name, wall, O, U, N, W, base, eaves, ops, gable_rise=rise,
                band=spec.get("band", False), floors=floors, loading=spec.get("loading"),
                nbays=spec.get("bays", 0))
    _roof(kit, name, x0, x1, y0, y1, eaves, roof, pitch)
    brick = kit.piece(wall_mat, name + "_chimneys")
    pots = kit.piece("pot_clay", name + "_chimney_pots")
    if roof == "gable_x":
        ridge = eaves + (y1 - y0) / 2.0 * math.tan(pitch)
    elif roof == "gable_y":
        ridge = eaves + (x1 - x0) / 2.0 * math.tan(pitch)
    else:
        ridge = eaves + min(x1 - x0, y1 - y0) / 2.0 * math.tan(pitch)
    for cx, cy in chimneys:
        kit.box(brick, cx - 0.45, cx + 0.45, cy - 0.30, cy + 0.30, ridge - 1.2, ridge + 1.1, skip=("bottom",))
        kit.box(brick, cx - 0.52, cx + 0.52, cy - 0.37, cy + 0.37, ridge + 1.0, ridge + 1.15, skip=("bottom",))
        for dx in (-0.22, 0.22):
            kit.lathe(pots, (cx + dx, cy), ((0.13, 0.0), (0.12, 0.30), (0.10, 0.42), (0.11, 0.45), (0.0, 0.45)),
                      8, z0=ridge + 1.15)
    # gutters along each eaves wall that is not against a neighbour, a downpipe at each end
    lead = kit.piece("lead", name + "_rainwater")
    if roof in ("gable_x", "hip"):
        walls = (("ymin", y0, -1.0), ("ymax", y1, 1.0))
    else:
        walls = (("xmin", x0, -1.0), ("xmax", x1, 1.0))
    for key, c, s in walls:
        if faces.get(key, {}).get("party"):
            continue
        o = c + s * 0.28
        if key in ("ymin", "ymax"):
            kit.box(lead, x0 - 0.05, x1 + 0.05, min(o, o + s * 0.12), max(o, o + s * 0.12), eaves - 0.15, eaves - 0.04)
            for xp in (x0 + 0.3, x1 - 0.3):
                kit.box(lead, xp - 0.035, xp + 0.035, min(c + s * 0.06, c + s * 0.13), max(c + s * 0.06, c + s * 0.13),
                        zg, eaves - 0.10, skip=("bottom",))
        else:
            kit.box(lead, min(o, o + s * 0.12), max(o, o + s * 0.12), y0 - 0.05, y1 + 0.05, eaves - 0.15, eaves - 0.04)
            for yp in (y0 + 0.3, y1 - 0.3):
                kit.box(lead, min(c + s * 0.06, c + s * 0.13), max(c + s * 0.06, c + s * 0.13), yp - 0.035, yp + 0.035,
                        zg, eaves - 0.10, skip=("bottom",))


def _facade(kit, name, wall, O, U, N, W, zb, ze, ops, gable_rise=0.0, band=False, floors=(),
            loading=None, nbays=0):
    def P(u, z, d=0.0):
        return (O[0] + U[0] * u - N[0] * d, O[1] + U[1] * u - N[1] * d, z)
    hint = (N[0], N[1], 0.0)
    low = [o for o in ops if o[3] <= ze + 1e-9]
    high = [o for o in ops if o[2] >= ze - 1e-9]
    # the wall, cut round its openings, cells merged along each row
    us = sorted(set([0.0, W] + [o[0] for o in low] + [o[1] for o in low]))
    zs = sorted(set([zb, ze] + [o[2] for o in low] + [o[3] for o in low]))
    for j in range(len(zs) - 1):
        za, zb_ = zs[j], zs[j + 1]
        zm = (za + zb_) / 2
        run = None
        for i in range(len(us) - 1):
            ua, ub = us[i], us[i + 1]
            um = (ua + ub) / 2
            hole = any(o[0] < um < o[1] and o[2] < zm < o[3] for o in low)
            if not hole:
                run = (run[0], ub) if run else (ua, ub)
            if hole or i == len(us) - 2:
                if run:
                    kit.face(wall, [P(run[0], za), P(run[1], za), P(run[1], zb_), P(run[0], zb_)], hint)
                run = None
    # the gable over the eaves, with its one opening if it has one
    if gable_rise > 0:
        apex = P(W / 2.0, ze + gable_rise)
        if high:
            u0, u1, z0, z1 = high[0][:4]

            def zg_at(u):
                return ze + gable_rise * (1.0 - abs(u - W / 2.0) / (W / 2.0))
            kit.face(wall, [P(0.0, ze), P(u0, ze), P(u0, zg_at(u0))], hint)
            kit.face(wall, [P(u1, ze), P(W, ze), P(u1, zg_at(u1))], hint)
            kit.face(wall, [P(u0, ze), P(u1, ze), P(u1, z0), P(u0, z0)], hint)
            kit.face(wall, [P(u0, z1), P(u1, z1), P(u1, zg_at(u1)), apex, P(u0, zg_at(u0))], hint)
        else:
            kit.face(wall, [P(0.0, ze), P(W, ze), apex], hint)
    # each opening: reveals, then glass and a sash frame, or a boarded door
    stone = kit.piece("stone", name + "_sills_and_lintels")
    glass = kit.piece("glass", name + "_windows")
    joinery = kit.piece("paint_joinery", name + "_window_frames")
    door = kit.piece("paint_door", name + "_doors")
    for (u0, u1, z0, z1, kind) in low + high:
        d = 0.12 if kind == "window" else 0.16
        kit.face(wall, [P(u0, z0, 0), P(u0, z0, d), P(u0, z1, d), P(u0, z1, 0)], (U[0], U[1], 0))
        kit.face(wall, [P(u1, z0, 0), P(u1, z1, 0), P(u1, z1, d), P(u1, z0, d)], (-U[0], -U[1], 0))
        kit.face(wall, [P(u0, z1, 0), P(u0, z1, d), P(u1, z1, d), P(u1, z1, 0)], (0, 0, -1))
        kit.face(stone, [P(u0, z0, 0), P(u1, z0, 0), P(u1, z0, d), P(u0, z0, d)], (0, 0, 1))
        if kind == "window":
            kit.frame_box(stone, O, U, N, u0 - 0.07, u1 + 0.07, z0 - 0.08, z0 - 0.005, -0.05, 0.0)
            kit.frame_box(stone, O, U, N, u0 - 0.10, u1 + 0.10, z1 + 0.005, z1 + 0.20, -0.01, 0.0)
            kit.face(glass, [P(u0, z0, d), P(u1, z0, d), P(u1, z1, d), P(u0, z1, d)], hint)
            fw, fd = 0.065, 0.075
            for (a0, a1, b0, b1) in ((u0, u1, z0, z0 + fw), (u0, u1, z1 - fw, z1), (u0, u0 + fw, z0 + fw, z1 - fw),
                                     (u1 - fw, u1, z0 + fw, z1 - fw),
                                     (u0 + fw, u1 - fw, (z0 + z1) / 2 - 0.03, (z0 + z1) / 2 + 0.03)):
                kit.frame_box(joinery, O, U, N, a0, a1, b0, b1, fd, d - 0.002)
        else:
            kit.face(door, [P(u0, z0, d), P(u1, z0, d), P(u1, z1, d), P(u0, z1, d)], hint)
            if kind in ("cart_door", "loading_door"):
                kit.frame_box(door, O, U, N, (u0 + u1) / 2 - 0.03, (u0 + u1) / 2 + 0.03, z0, z1, d - 0.03, d - 0.001)
            kit.frame_box(stone, O, U, N, u0 - 0.10, u1 + 0.10, z1 + 0.005, z1 + 0.22, -0.01, 0.0)
    # the hauling way's hood and hoist beam, over the topmost loading door on this wall
    tops = [o for o in low + high if o[4] == "loading_door"]
    if loading is not None and nbays and tops:
        o = max(tops, key=lambda q: q[3])
        uc = (o[0] + o[1]) / 2
        tim = kit.piece("prop_timber", name + "_hoist_hood")
        zt = o[3] + 0.85
        kit.frame_box(tim, O, U, N, uc - 0.10, uc + 0.10, zt - 0.35, zt - 0.15, -1.25, 0.0)
        for uu in (uc - 0.85, uc + 0.85):
            tri = [P(uu, zt - 0.6, 0.0), P(uu, zt - 0.6, -1.0), P(uu, zt + 0.25, 0.0)]
            kit.face(tim, tri, (U[0], U[1], 0))
            kit.face(tim, list(reversed(tri)), (-U[0], -U[1], 0))
        a = P(uc - 0.9, zt - 0.6, -1.05)
        b = P(uc + 0.9, zt - 0.6, -1.05)
        c = P(uc + 0.9, zt + 0.3, 0.0)
        e = P(uc - 0.9, zt + 0.3, 0.0)
        kit.face(tim, [a, b, c, e], (N[0], N[1], 1.0))
        kit.face(tim, [a, e, c, b], (-N[0], -N[1], -1.0))
    # the painted name band, left blank: between the ground floor's heads and the first floor's
    # sills, broken by the hauling way
    if band and len(floors) >= 2:
        cream = kit.piece("render_cream", name + "_name_band")
        z0 = floors[0] + 3.30
        z1 = floors[1] + 0.62
        spans = [(0.8, W - 0.8)]
        if loading is not None and nbays:
            uc = W * (loading + 0.5) / nbays
            spans = [(0.8, uc - 1.0), (uc + 1.0, W - 0.8)]
        for a0, a1 in spans:
            kit.frame_box(cream, O, U, N, a0, a1, z0, z1, -0.012, 0.0)


def _roof(kit, name, x0, x1, y0, y1, eaves, roof, pitch):
    slate = kit.piece("slate", name + "_roof")
    tp = math.tan(pitch)
    ov_e, ov_v, th = 0.30, 0.20, 0.12
    if roof == "hip":
        X0, X1, Y0, Y1 = x0 - ov_e, x1 + ov_e, y0 - ov_e, y1 + ov_e
        ze = eaves - ov_e * tp
        h = (Y1 - Y0) / 2.0
        zr = ze + h * tp
        ym = (Y0 + Y1) / 2.0
        r0, r1 = (X0 + h, ym, zr), (X1 - h, ym, zr)
        c00, c10, c11, c01 = (X0, Y0, ze), (X1, Y0, ze), (X1, Y1, ze), (X0, Y1, ze)
        up = (0, 0, 1)
        kit.face(slate, [c00, c10, r1, r0], up)
        kit.face(slate, [c11, c01, r0, r1], up)
        kit.face(slate, [c10, c11, r1], up)
        kit.face(slate, [c01, c00, r0], up)
        # fascia round the eaves and a flat soffit
        for a, b in ((c00, c10), (c10, c11), (c11, c01), (c01, c00)):
            mid = ((a[0] + b[0]) / 2 - (X0 + X1) / 2, (a[1] + b[1]) / 2 - ym, 0.0)
            kit.face(slate, [a, b, (b[0], b[1], b[2] - th), (a[0], a[1], a[2] - th)], mid)
        kit.face(slate, [(X0, Y0, ze - th), (X1, Y0, ze - th), (X1, Y1, ze - th), (X0, Y1, ze - th)], (0, 0, -1))
        return
    # gable: build in the ridge's own frame (a along the ridge, b across), turned into the world
    if roof == "gable_x":
        a0, a1, b0, b1 = x0, x1, y0, y1
        def W_(a, b, z):
            return (a, b, z)
    else:   # gable_y: a = y, b = -x (a quarter turn, so faces keep their winding)
        a0, a1, b0, b1 = y0, y1, -x1, -x0
        def W_(a, b, z):
            return (-b, a, z)
    bm = (b0 + b1) / 2.0
    rise = (b1 - b0) / 2.0 * tp
    zr = eaves + rise
    A0, A1 = a0 - ov_v, a1 + ov_v
    B0, B1 = b0 - ov_e, b1 + ov_e
    ze = eaves - ov_e * tp
    top = [(B0, ze), (bm, zr), (B1, ze)]
    for k in range(2):
        (ba, za), (bb, zb) = top[k], top[k + 1]
        q = [W_(A0, ba, za), W_(A1, ba, za), W_(A1, bb, zb), W_(A0, bb, zb)]
        kit.face(slate, q, (0, 0, 1))
        q = [W_(A0, ba, za - th), W_(A1, ba, za - th), W_(A1, bb, zb - th), W_(A0, bb, zb - th)]
        kit.face(slate, q, (0, 0, -1))
    # eaves fascias
    for B, z, s in ((B0, ze, -1.0), (B1, ze, 1.0)):
        q = [W_(A0, B, z), W_(A1, B, z), W_(A1, B, z - th), W_(A0, B, z - th)]
        c = W_(0, s, 0)
        kit.face(slate, q, (c[0], c[1], 0))
    # verges
    for A, s in ((A0, -1.0), (A1, 1.0)):
        c = W_(s, 0, 0)
        for k in range(2):
            (ba, za), (bb, zb) = top[k], top[k + 1]
            q = [W_(A, ba, za), W_(A, bb, zb), W_(A, bb, zb - th), W_(A, ba, za - th)]
            kit.face(slate, q, (c[0], c[1], 0))
    # a ridge roll
    kit.piece("slate", name + "_roof")
    ra = W_(A0, bm, zr)
    rb = W_(A1, bm, zr)
    d = norm2(v2(ra, rb))
    kit.obox(slate, ((ra[0] + rb[0]) / 2, (ra[1] + rb[1]) / 2), d, math.hypot(*v2(ra, rb)) / 2, 0.11,
             zr - 0.06, zr + 0.08, skip=("bottom",))


# ---- quay furniture ------------------------------------------------------------------------------
BOLLARDS = ((-69.25, -88.0), (-69.25, -58.0), (-69.25, -28.0), (-69.25, 2.0), (-69.25, 30.0),
            (-110.75, -80.0), (-110.75, -45.0), (-95.0, 40.75), (-115.0, 40.75), (-140.0, 40.75))
RINGS_NORTH_QUAY_Y = (-73.0, -43.0, -13.0, 16.0)
LADDER_Y = -36.0


def _quay_furniture(kit, at, zg, zw, jn):
    iron = kit.piece("iron_black", "bollards", smooth=True)
    for c in BOLLARDS:
        kit.lathe(iron, c, BOLLARD_PROFILE, 16, z0=zg)
    # mooring rings on the north quay's face and the jetty's, hanging from an eye under the cope
    rings = kit.piece("iron_black", "mooring_rings", smooth=True)
    xq = at["north_quay_x"]
    top = zg - COPING_T_M
    for y in RINGS_NORTH_QUAY_Y:
        _ring(kit, rings, (xq + COPING_NOSE_M, y), (-1.0, 0.0), top - 0.15, top, zw)
    jx1 = at["jetty_x"][1]
    for y in (-62.0, -32.0):
        _ring(kit, rings, (jx1 - COPING_NOSE_M, y), (1.0, 0.0), top - 0.15, top, zw)
    # the ladder down the north quay, its stiles up over the cope as handholds
    lad = kit.piece("galvanised", "quay_ladder")
    face_top = (xq + COPING_NOSE_M, LADDER_Y)
    lean = QUAY_BATTER
    bot = zw - WALL_BELOW_WATER_M + 0.3
    out = -1.0                                      # away from the land
    for s in (-LADDER_W_M / 2, LADDER_W_M / 2):
        y = LADDER_Y + s
        # stile: a bar standing off the face, following the batter
        x_top = face_top[0] + out * LADDER_OFF_M
        x_bot = x_top + out * (top - bot) * lean
        kit.strut(lad, (x_bot, y, bot), (x_top, y, top), 0.03)
        # the handhold over the cope: up, back over, down onto the cope
        kit.box(lad, x_top - 0.03, x_top + 0.03, y - 0.03, y + 0.03, top, zg + 0.95)
        kit.box(lad, x_top - 0.03, xq + 0.45, y - 0.03, y + 0.03, zg + 0.89, zg + 0.95)
        kit.box(lad, xq + 0.39, xq + 0.45, y - 0.03, y + 0.03, zg, zg + 0.95)
    z = top - LADDER_RUNG_M
    while z > bot + 0.05:
        x = face_top[0] + out * LADDER_OFF_M + out * (top - z) * lean
        kit.box(lad, x - 0.015, x + 0.015, LADDER_Y - LADDER_W_M / 2, LADDER_Y + LADDER_W_M / 2, z - 0.015, z + 0.015)
        z -= LADDER_RUNG_M
    # fish boxes: a stack of three and two set down, on the apron by the cope
    tim = kit.piece("prop_timber", "fish_boxes")
    L, Wd, H = FISH_BOX_M
    for c, ang, k in (((-66.2, -12.0), 0.0, 0), ((-66.2, -12.0), 0.0, 1), ((-66.2, -12.0), 4.0, 2),
                      ((-65.3, -10.6), 12.0, 0), ((-64.9, -13.6), -7.0, 0)):
        _fish_box(kit, tim, c, math.radians(ang), zg + k * H)
    # two more stacks along the quay, by the ladder and at the east quay's corner
    for c, ang, k in (((-67.0, -41.5), 3.0, 0), ((-67.0, -41.5), 3.0, 1), ((-67.0, -41.5), -2.0, 2),
                      ((-67.0, -41.5), 1.0, 3), ((-66.1, -42.6), 80.0, 0), ((-66.1, -42.6), 84.0, 1),
                      ((-73.0, 43.2), 0.0, 0), ((-73.0, 43.2), 2.0, 1), ((-74.0, 43.4), 5.0, 0)):
        _fish_box(kit, tim, c, math.radians(ang), zg + k * H)
    # coils of rope beside them
    rope = kit.piece("rope", "rope_coil", smooth=True)
    for cx, cy in ((-65.6, -8.6), (-71.6, 44.6)):
        for k, (r, dz) in enumerate(((0.36, 0.025), (0.30, 0.025), (0.24, 0.025), (0.33, 0.072), (0.27, 0.072))):
            kit.torus(rope, (cx, cy, zg + dz), (1, 0, 0), (0, 1, 0), r, 0.024, 20, 6)
    # rope fenders hung over the north quay's face where the boat lies
    fend = kit.piece("rope", "rope_fenders", smooth=True)
    for y in (-12.5, -6.0, 0.5):
        x = xq - 0.22
        kit.lathe(fend, (x, y), ((0.0, 0.0), (0.10, 0.03), (0.15, 0.15), (0.15, 0.65), (0.10, 0.77), (0.0, 0.80)),
                  10, z0=top - 1.6)
        _rope_seg(kit, fend, (x, y, top - 0.8), (x + 0.1, y, top - 0.2), 0.012)
        _rope_seg(kit, fend, (x + 0.1, y, top - 0.2), (xq + 0.3, y, zg + 0.02), 0.012)
    # a galvanised dustbin on the NW footway against the yard wall
    bin_ = kit.piece("galvanised", "dustbin", smooth=True)
    fy = -(jn.half + jn.kerb_w + FOOTWAY_W_M) + DUSTBIN_D_M / 2 + 0.06
    fz = jn.footway_z_at(abs(fy) - jn.half - jn.kerb_w)
    r = DUSTBIN_D_M / 2
    kit.lathe(bin_, (-15.0, fy), ((r - 0.02, 0.0), (r - 0.01, 0.02), (r, 0.05), (r, 0.20), (r + 0.006, 0.21),
                                  (r, 0.22), (r, 0.42), (r + 0.006, 0.43), (r, 0.44), (r, 0.60),
                                  (r + 0.02, 0.605), (r + 0.02, 0.625), (r - 0.04, 0.655),
                                  (0.06, 0.66), (0.05, 0.69), (0.0, 0.70)), 20, z0=fz)


def _ring(kit, p, at, n, z_eye, z_top, zw):
    """A mooring ring hanging on the wall face at plan point at, the face's outward normal n."""
    R, r = 0.11, 0.016
    c = (at[0] + n[0] * 0.07, at[1] + n[1] * 0.07, z_eye - R)
    t = (-n[1], n[0], 0.0)
    kit.torus(p, c, t, (0.0, 0.0, 1.0), R, r, 14, 6)
    # the eye bolt it hangs from
    kit.box(p, min(at[0], at[0] + n[0] * 0.09) - 0.015, max(at[0], at[0] + n[0] * 0.09) + 0.015,
            at[1] - 0.025, at[1] + 0.025, z_eye - 0.02, z_eye + 0.03)


def _fish_box(kit, p, c, ang, z0):
    L, W, H = FISH_BOX_M
    t = FISH_BOX_WALL_M
    u = (math.cos(ang), math.sin(ang))
    w = left2(u)
    # bottom, two sides, two ends: an open box
    kit.obox(p, c, u, L / 2, W / 2, z0, z0 + t, skip=())
    for s in (-1.0, 1.0):
        kit.obox(p, add2(c, w, s * (W / 2 - t / 2)), u, L / 2, t / 2, z0 + t, z0 + H, skip=("bottom",))
        kit.obox(p, add2(c, u, s * (L / 2 - t / 2)), u, t / 2, W / 2 - t, z0 + t, z0 + H - 0.05, skip=("bottom",))


def _harbour_light(kit, at, zg):
    """A small cast-iron harbour light on the jetty's end: a hexagonal tapered tower, a gallery
    with a rail, a lantern, a domed roof (Watchet's of 1862 is the type, research section 5)."""
    jx0, jx1 = at["jetty_x"]
    c = ((jx0 + jx1) / 2.0, at["jetty_end_y"] - 4.5)
    st = kit.piece("quay_stone", "harbour_light_plinth")
    kit.box(st, c[0] - 1.4, c[0] + 1.4, c[1] - 1.4, c[1] + 1.4, zg - 0.05, zg + 0.45, skip=("bottom",))
    tower = kit.piece("paint_white", "harbour_light_tower")
    z = zg + 0.45
    Ht = LIGHT_TOWER_H_M
    kit.lathe(tower, c, ((1.05, 0.0), (1.05, 0.25), (0.92, 0.32), (0.70, Ht - 0.15), (0.70, Ht)), 6,
              z0=z, phase=math.pi / 6)
    iron = kit.piece("iron_black", "harbour_light_ironwork", smooth=False)
    zt = z + Ht
    kit.lathe(iron, c, ((0.0, 0.0), (1.05, 0.0), (1.05, 0.10), (0.0, 0.10)), 12, z0=zt)  # gallery floor
    for zz in (0.55, 0.95):
        kit.torus(iron, (c[0], c[1], zt + 0.10 + zz), (1, 0, 0), (0, 1, 0), 1.0, 0.018, 24, 4)
    for k in range(8):
        a = 2 * math.pi * k / 8
        q = (c[0] + 1.0 * math.cos(a), c[1] + 1.0 * math.sin(a))
        kit.box(iron, q[0] - 0.02, q[0] + 0.02, q[1] - 0.02, q[1] + 0.02, zt + 0.10, zt + 1.08)
    lamp = kit.piece("lamp_red", "harbour_light_lantern")
    kit.lathe(lamp, c, ((0.55, 0.0), (0.55, 1.05)), 8, z0=zt + 0.10, phase=math.pi / 8)
    kit.lathe(iron, c, ((0.62, 0.0), (0.62, 0.08), (0.45, 0.30), (0.12, 0.52), (0.0, 0.56)), 8,
              z0=zt + 1.15, phase=math.pi / 8)
    kit.lathe(iron, c, ((0.0, 0.0), (0.08, 0.05), (0.08, 0.16), (0.0, 0.22)), 8, z0=zt + 1.69)
    # the lantern's frame: a base ring and astragals
    kit.lathe(iron, c, ((0.60, 0.0), (0.60, 0.08), (0.55, 0.08)), 8, z0=zt + 0.10, phase=math.pi / 8)
    for k in range(8):
        a = math.pi / 8 + 2 * math.pi * k / 8
        q = (c[0] + 0.57 * math.cos(a), c[1] + 0.57 * math.sin(a))
        kit.box(iron, q[0] - 0.02, q[0] + 0.02, q[1] - 0.02, q[1] + 0.02, zt + 0.10, zt + 1.15)
    # the jetty's parapet on its seaward side, stone, with a cope
    par = kit.piece("quay_stone", "jetty_parapet")
    pc = kit.piece("stone", "jetty_parapet_coping")
    x_a = jx0 + COPING_W_M
    kit.box(par, x_a, x_a + 0.80, -100.0 - COPING_W_M, at["jetty_end_y"] - 8.0, zg - 0.05, zg + 1.10,
            skip=("bottom",))
    kit.box(pc, x_a - 0.04, x_a + 0.84, -100.0 - COPING_W_M, at["jetty_end_y"] - 8.0 + 0.04, zg + 1.10,
            zg + 1.22, skip=("bottom",))
    info = {"light_at": c}
    return info


# =================================================================================================
# export frame and checks
# =================================================================================================
def reflected(pieces):
    """The pieces with y -> -y and every face re-wound, as the street's export does."""
    out = {}
    for k, p in pieces.items():
        out[k] = dict(p)
        out[k]["verts"] = [(x, -y, z) for x, y, z in p["verts"]]
        out[k]["faces"] = [tuple(reversed(f)) for f in p["faces"]]
    return out


def street_profile_z(sc, y):
    """terrace-front.py's road_z / kerb_top_z / footway_z, as the street builds them: the section's
    height at |y| (both limits returned at the kerb face, where the section is vertical)."""
    half, fall = sc["ROAD_HALF_M"], sc["ROAD_CROSSFALL"]
    kw, ku, ff = sc["KERB_W_M"], sc["KERB_UPSTAND_M"], sc["FOOTWAY_CROSSFALL"]
    front = sc["STREET_FRONTAGE_M"]
    a = abs(y)
    road = -min(a, half) * fall
    kerb = -half * fall + ku
    if a < half - 1e-6:
        return [road]
    if abs(a - half) <= 1e-6:
        return [road, kerb]
    if a <= half + kw + 1e-6:
        return [kerb]
    if a <= front + 1e-6:
        return [kerb + (min(a, front) - half - kw) * ff]
    return [kerb + (front - half - kw) * ff]


def read_glb_positions(path, mesh_names):
    """{mesh name: [(x, y_recipe, z)]} from a glb, plain Python (y up in glTF; the export reflected
    y, and glTF z = -y_export = y_recipe)."""
    import struct
    data = open(path, "rb").read()
    magic, ver, length = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF":
        raise ValueError("not a glb")
    off = 12
    js, binb = None, None
    while off < length:
        clen, ctype = struct.unpack_from("<I4s", data, off)
        chunk = data[off + 8: off + 8 + clen]
        if ctype == b"JSON":
            js = json.loads(chunk.decode("utf-8"))
        elif ctype == b"BIN\x00":
            binb = chunk
        off += 8 + clen
    out = {}
    for m in js.get("meshes", []):
        if m.get("name") not in mesh_names:
            continue
        pts = []
        for prim in m["primitives"]:
            acc = js["accessors"][prim["attributes"]["POSITION"]]
            bv = js["bufferViews"][acc["bufferView"]]
            stride = bv.get("byteStride", 12)
            base = bv.get("byteOffset", 0) + acc.get("byteOffset", 0)
            for i in range(acc["count"]):
                x, y, z = struct.unpack_from("<fff", binb, base + i * stride)
                pts.append((x, z, y))      # (along, across recipe-east, up)
        out[m["name"]] = pts
    return out


def selftest(root=ROOT, street_glb=None, verbose=True):
    """Plain-Python checks. Returns (ok, lines)."""
    lines = []
    ok = True

    def check(cond, what):
        nonlocal ok
        lines.append(("PASS " if cond else "FAIL ") + what)
        ok = ok and bool(cond)

    kit, jn, info = build(root)
    sc = info["street"]
    mats = all_materials(root)
    street_mats = read_street_materials(root)
    # 1. the joint with the street: the kit's section at the street's road end equals the street's
    join = sc["BACKDROP_ROAD_END"]
    worst = 0.0
    n = 0
    for key in ("asphalt__road_quay_street_south", "kerbstone__kerb_northwest_corner",
                "kerbstone__kerb_northeast_corner", "paving__footway_northwest_corner",
                "paving__footway_northeast_corner"):
        for (x, y, z) in kit.pieces[key]["verts"]:
            if abs(x - join) < 1e-6 and z > -0.29 and abs(y) <= sc["STREET_FRONTAGE_M"] + 1e-6:
                want = street_profile_z(sc, y)
                # the kerb's 10 mm arris is the kit's: allow it
                err = min(abs(z - w) for w in want)
                if abs(abs(y) - sc["ROAD_HALF_M"]) < 1e-6 and abs(z - (want[-1] - 0.010)) < 1e-6:
                    err = 0.0
                worst = max(worst, err)
                n += 1
    check(n >= 9 and worst < 1e-6,
          "the kit meets the street where the street's road ends (x = %.2f): %d section points, worst %.4f m "
          "from terrace-front's road_z/kerb_top_z/footway_z; the street's section is the same at x = 0"
          % (join, n, worst))
    # and against the street's exported glb, where it is on this disk
    if street_glb and os.path.isfile(street_glb):
        pos = read_glb_positions(street_glb, ("street_asphalt", "street_kerbstone", "street_paving"))
        worst_g, ng = 0.0, 0
        for name, pts in pos.items():
            for (x, y, z) in pts:
                if abs(x - join) < 0.002 and z > -0.29 and abs(y) <= sc["STREET_FRONTAGE_M"] + 0.01:
                    want = street_profile_z(sc, y)
                    err = min(abs(z - w) for w in want)
                    worst_g = max(worst_g, err)
                    ng += 1
        check(ng >= 10 and worst_g <= 0.0075,
              "the street's own glb at x = %.2f (%d top vertices) sits on the same section, worst %.4f m "
              "(its 6 mm bevels)" % (join, ng, worst_g))
    else:
        lines.append("SKIP the street's glb not found (%s)" % street_glb)
    # 2. the quay edge at x = -70
    cope = [v for v in kit.pieces["stone__quay_coping"]["verts"] if -101 < v[1] < 41 and -75 < v[0] < -65]
    check(abs(info["quay_edge_x"] - (-70.0)) < 1e-9 and cope and abs(min(v[0] for v in cope) - (-70.0)) < 1e-6,
          "the quay edge (the cope's nose) at x = %.2f, from the atlas's north 280" % min(v[0] for v in cope))
    # 3. the water reaches the horizon
    wv = kit.pieces["harbour_water__harbour_and_sea"]["verts"]
    check(min(v[0] for v in wv) <= -4000.0 and min(v[1] for v in wv) <= -2000.0 and max(v[1] for v in wv) >= 2000.0,
          "the water reaches x = %.0f, y %.0f..%.0f, at z = %.2f (%.2f m under the cope)"
          % (min(v[0] for v in wv), min(v[1] for v in wv), max(v[1] for v in wv), info["water_z"],
             info["coping_top_z"] - info["water_z"]))
    # 4. every piece is "<material>__<piece>", its material known, new ones only the listed four
    bad = [k for k, p in kit.pieces.items()
           if "__" not in k or k.split("__", 1)[0] != p["material"] or p["material"] not in mats
           or not re.match(r"^[a-z0-9_]+$", k) or len(k) > 63]
    used = sorted(set(p["material"] for p in kit.pieces.values()))
    new = [m for m in used if m not in street_mats]
    check(not bad and set(new) <= set(KIT_NEW_MATERIALS),
          "%d pieces, every name <material>__<piece> with a known material (%d materials, new: %s)%s"
          % (len(kit.pieces), len(used), ", ".join(new) or "none", ("; bad: %s" % bad) if bad else ""))
    # 5. triangles under budget
    tris = tri_count(kit.pieces)
    check(tris < TRI_BUDGET, "triangles %d, under %d" % (tris, TRI_BUDGET))
    # 6. the top surfaces face up; no degenerate faces
    down = 0
    for key in ("asphalt__road_quay_street_south", "asphalt__road_quay_street_west",
                "asphalt__road_harbour_board_approach", "asphalt__road_junction", "quay_stone__apron_setts",
                "quay_stone__hard_standing_northeast", "quay_stone__yard_northwest",
                "paving__footway_northwest_corner", "paving__footway_northeast_corner",
                "harbour_water__harbour_and_sea"):
        p = kit.pieces[key]
        for f in p["faces"]:
            nn = newell([p["verts"][i] for i in f])
            if abs(nn[2]) > 1e-9 and nn[2] < 0 and abs(nn[2]) > 0.5 * math.sqrt(dot3(nn, nn)):
                down += 1
    degen = 0
    for p in kit.pieces.values():
        for f in p["faces"]:
            nn = newell([p["verts"][i] for i in f])
            if dot3(nn, nn) < 1e-16:
                degen += 1
    check(down == 0 and degen == 0, "every ground face faces up (%d down), no degenerate faces (%d)" % (down, degen))
    # 7. the layout agrees with the atlas: junction, roads, coast
    A = read_atlas(root)
    check(jn.J == (-30.0, 0.0) and A["west_end"] == (-50.0, -90.0) and A["harbour_board"][1] == (-35.0, 60.0),
          "the junction at x = %.0f (atlas north 320), the west road to (%.0f, %.0f), the Harbour Board "
          "approach by (%.0f, %.0f) to (%.0f, %.0f), all read from the atlas"
          % (jn.J[0], jn.W_end[0], jn.W_end[1], A["harbour_board"][1][0], A["harbour_board"][1][1],
             A["harbour_board"][2][0], A["harbour_board"][2][1]))
    # 8. the levels: the apron flush with the kerb top; the footway backs at the threshold
    check(abs(info["apron_z"] - (-sc["ROAD_HALF_M"] * sc["ROAD_CROSSFALL"] + sc["KERB_UPSTAND_M"])) < 1e-9
          and abs(info["yard_z"] - sc["THRESHOLD_ABOVE_CROWN_M"]) < 1e-9,
          "the apron and copes at %.3f (the kerb's top), the yards at %.3f (the street's threshold)"
          % (info["apron_z"], info["yard_z"]))
    # 9. the reflection keeps every face's facing (the export frame)
    r = reflected(kit.pieces)
    flips = 0
    for k in ("asphalt__road_junction", "quay_stone__apron_setts"):
        for f0, f1 in zip(kit.pieces[k]["faces"], r[k]["faces"]):
            n0 = newell([kit.pieces[k]["verts"][i] for i in f0])
            n1 = newell([r[k]["verts"][i] for i in f1])
            if n0[2] * n1[2] < 0:
                flips += 1
    check(flips == 0, "reflected y to -y for the export, re-wound: tops still face up (%d flipped)" % flips)
    if verbose:
        for ln in lines:
            print(ln)
    return ok, lines, info, kit
