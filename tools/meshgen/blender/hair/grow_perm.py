"""Grow a 1990 set or perm as hair curves on a MetaHuman head, by script, in Blender.

    blender -b -P tools/meshgen/blender/hair/grow_perm.py -- HEAD.fbx STYLE OUT_DIR

STYLE is one of STYLES below (sheila: a short shampoo-and-set; darren: a
grown-out perm). Writes OUT_DIR/<style>.abc (the curves alone, for Unreal's
groom importer), OUT_DIR/<style>.blend, four preview pictures and
OUT_DIR/<style>.json with what it grew and the checks.

WHY, 29 September (Jafar's ruling: the hair is curls made in Blender, free,
judged on his page; production/research/character-pipeline/hair-groom-script-
2026-09-29.md). No MetaHuman groom has a set or a perm.

ATTEMPT 3, the last under the two-tries rule, follows the research after two
failures (production/research/character-pipeline/hair-set-groom-2026-09-29.md):
attempt 1's independent strands made a mushroom of fuzz with a false parting,
attempt 2's clumps along random guides came out as flat ribbons and a
windblown wig. A set is made on ROLLERS, so it is grown as one:

1. an ENVELOPE above the skin by region (fullest at the crown, close at the
   nape, close over the forehead), which every point stays inside;
2. a FLOW away from a side parting in front of the crown's whorl and straight
   down from the whorl behind it (no left/right rule behind the crown);
3. ROLLERS, each a patch of scalp whose hair ends roll under round one axis
   (the surface normal x the flow at its centre) by one radius and angle;
4. LENGTHS by position, not by chance (at most +-4%);
5. about 150 FLOW GUIDES with no randomness: rising off the scalp, then along
   the envelope, the last part rolled under round the roller's axis;
6. CLUMP GUIDES blended from the nearest flow guides of the SAME roller and
   the same side of the parting, with a small ripple in one phase per roller;
7. STRANDS round each clump guide in a ROUND disc across the hair (in frames
   carried along it without twisting), narrowing to the tips, 0-8% shorter;
8. a tidy: kept off the skin and inside the envelope, smoothed, a little frizz.

THE SCALP is found from the head's own shape: the head faces -Y (the nose is
the head's lowest y), its crown is its highest point, and the hairline runs
from about 7 cm below the crown at the forehead to about 15 cm at the nape,
on the skin's faces only.
"""
import collections
import json
import math
import os
import random
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Quaternion, Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

argv = sys.argv[sys.argv.index("--") + 1:]
HEAD, STYLE, OUT = argv[0], argv[1], argv[2]
os.makedirs(OUT, exist_ok=True)
MM = 0.001

# A roller: (azimuth from the front towards +X, elevation from the head's
# centre, both in degrees; roll radius in mm; roll angle in degrees).
STYLES = {
    # A SHORT SHAMPOO-AND-SET, 53, greying brown (Sheila's sheet and her
    # approved portrait: soft, rounded, side-parted, swept off the face, to the
    # earlobe or upper jaw at the sides, a tapered nape, fullest at the crown).
    # The parting is on her right: the left of the picture from the front
    # (the front camera shows +X on the right).
    "sheila": {
        "strands": 22000, "flow_guides": 150, "clumps": 620, "points": 24, "seed": 1990,
        "front_drop": 0.070, "nape_drop": 0.150, "part_x": -0.035, "whorl": (0.45, 1.0),
        # the envelope above the skin, mm, by depth below the top of the head (m)
        "envelope": [(0.0, 30), (0.04, 28), (0.07, 21), (0.11, 14), (0.15, 9), (0.18, 6)],
        "envelope_face": 6, "tip_off_skin": 3.5,
        # lengths, mm, by depth below the top: at the sides and in front, and at the back
        "length_side": [(0.0, 92), (0.04, 90), (0.08, 72), (0.14, 66)],
        "length_back": [(0.0, 92), (0.04, 90), (0.09, 70), (0.13, 50), (0.17, 40)],
        "length_fringe": 82,
        "rise_deg": (45, 60), "rise_mm": 10,
        "rollers": {
            "top": [(20, 30, 16, 150), (20, 50, 16, 150), (30, 68, 16, 150), (60, 84, 16, 150)],
            "side": [(a, 12, 12, 180) for a in (55, 85, 115, -55, -85, -115)],
            "back": [(a, 45, 13, 150) for a in (150, 180, 210)] + [(a, 15, 12, 150) for a in (135, 165, 195, 225)],
            "nape": [(a, -18, 9.5, 120) for a in (165, 195)],
        },
        "roll_share_max": 0.40,
        "ripple_mm": 2.0, "ripple_wave_mm": 25, "ripple_jitter": 0.1,
        "disc_mm": (3.5, 1.5), "shorter": 0.08, "frizz_mm": 0.8, "frizz_share": 0.02,
        "colour": (0.30, 0.25, 0.21), "grey": (0.60, 0.58, 0.55), "grey_share": (0.15, 0.55),
    },
    # A GROWN-OUT PERM, 25 (Darren): to be set when his hair is made; the same
    # method with longer lengths, a looser roll and a stronger ripple.
    "darren": {
        "strands": 18000, "flow_guides": 150, "clumps": 560, "points": 28, "seed": 1965,
        "front_drop": 0.065, "nape_drop": 0.165, "part_x": 0.0, "whorl": (0.45, 1.0),
        "envelope": [(0.0, 26), (0.04, 25), (0.07, 20), (0.11, 15), (0.15, 11), (0.19, 8)],
        "envelope_face": 7, "tip_off_skin": 4.0,
        "length_side": [(0.0, 120), (0.04, 115), (0.08, 95), (0.14, 90)],
        "length_back": [(0.0, 120), (0.04, 118), (0.09, 105), (0.13, 90), (0.17, 80)],
        "length_fringe": 100,
        "rise_deg": (40, 55), "rise_mm": 10,
        "rollers": {
            "top": [(0, 30, 12, 200), (0, 50, 12, 200), (0, 68, 12, 200), (0, 84, 12, 200)],
            "side": [(a, 12, 11, 220) for a in (55, 85, 115, -55, -85, -115)],
            "back": [(a, 45, 11, 220) for a in (150, 180, 210)] + [(a, 15, 11, 220) for a in (135, 165, 195, 225)],
            "nape": [(a, -18, 10, 200) for a in (165, 195)],
        },
        "roll_share_max": 0.45,
        "ripple_mm": 3.5, "ripple_wave_mm": 20, "ripple_jitter": 0.1,
        "disc_mm": (4.0, 2.0), "shorter": 0.08, "frizz_mm": 1.2, "frizz_share": 0.04,
        "colour": (0.36, 0.27, 0.18), "grey": (0.36, 0.27, 0.18), "grey_share": (0.0, 0.0),
    },
}
S = STYLES[STYLE]
rng = random.Random(S["seed"])
STRAND_RADIUS = 0.00004          # m (the research: about 0.00004; Unreal reads widths as radius x 2)


def interp(table, x):
    if x <= table[0][0]:
        return table[0][1]
    for (x0, y0), (x1, y1) in zip(table, table[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return table[-1][1]


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


# ---- the head -------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=HEAD)
meshes = sorted([o for o in bpy.context.scene.objects if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
head = meshes[0]
for o in meshes[1:]:
    bpy.data.objects.remove(o, do_unlink=True)
me = head.data
M = head.matrix_world
# THE SKIN IS THE SLOT WITH BY FAR THE MOST FACES: Unreal's FBX export
# scrambles the material names against the slots (on Sheila's head the slot
# named teeth holds 23,860 of the faces, the skin), so names are not trusted.
_count = collections.Counter(p.material_index for p in me.polygons)
SKIN = max(_count, key=_count.get)
verts_w = [M @ v.co for v in me.vertices]
top_z = max(p.z for p in verts_w)
y_front = min(p.y for p in verts_w)
y_back = max(p.y for p in verts_w)
cx = sum(p.x for p in verts_w) / len(verts_w)

# the skin alone, for the distance to the head (not the eyes, lashes or teeth)
_b = bmesh.new()
_b.from_mesh(me)
_b.transform(M)
bmesh.ops.delete(_b, geom=[f for f in _b.faces if f.material_index != SKIN], context="FACES")
BVH = BVHTree.FromBMesh(_b)


def yfrac(p):
    return max(0.0, min(1.0, (p.y - y_front) / (y_back - y_front)))


def hairline_z(y):
    u = max(0.0, min(1.0, (y - y_front) / (y_back - y_front)))
    u = u * u * (3 - 2 * u)
    return top_z - (S["front_drop"] + (S["nape_drop"] - S["front_drop"]) * u)


def surface(p):
    """The nearest skin point, its outward normal, and p's height above it."""
    loc, nrm, _i, _d = BVH.find_nearest(p)
    return loc, nrm, (p - loc).dot(nrm)


def envelope(q):
    """How far above the skin point q the hair may stand, in metres."""
    e = interp(S["envelope"], top_z - q.z)
    face = smooth((0.38 - yfrac(q)) / 0.10) * smooth((hairline_z(q.y) - q.z) / 0.012)
    return (e * (1 - face) + S["envelope_face"] * face) * MM


# the scalp's faces, as triangles, with their areas
tris = []
for poly in me.polygons:
    if poly.material_index != SKIN:
        continue
    pts = [verts_w[i] for i in poly.vertices]
    c = sum(pts, Vector()) / len(pts)
    if c.z < hairline_z(c.y):
        continue
    n = (M.to_3x3() @ poly.normal).normalized()
    for k in range(1, len(pts) - 1):
        a, b, d = pts[0], pts[k], pts[k + 1]
        area = (b - a).cross(d - a).length / 2
        if area > 0:
            tris.append((a, b, d, n, area))
total = sum(t[4] for t in tris)
cum = np.cumsum([t[4] for t in tris])


def sample_root(r):
    i = min(int(np.searchsorted(cum, r.random() * total)), len(tris) - 1)
    a, b, d, n, _ = tris[i]
    r1, r2 = r.random(), r.random()
    if r1 + r2 > 1:
        r1, r2 = 1 - r1, 1 - r2
    return a + (b - a) * r1 + (d - a) * r2, n


def farthest(points, k, first):
    """k of the points spread evenly (farthest-point sampling), deterministic."""
    P = np.array([tuple(p) for p in points])
    chosen = [first]
    dist = np.linalg.norm(P - P[first], axis=1)
    for _ in range(k - 1):
        i = int(np.argmax(dist))
        chosen.append(i)
        dist = np.minimum(dist, np.linalg.norm(P - P[i], axis=1))
    return chosen


# ---- the whorl, the parting and the flow ------------------------------------
C = Vector((cx, (y_front + y_back) / 2 + 0.01, top_z - 0.105))     # the head's centre, about
X, BACK, DOWN = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, -1))
PART_X = cx + S["part_x"]


def cast(direction):
    hit = BVH.ray_cast(C, direction.normalized())
    return hit[0], hit[1]


W = cast(Vector((0.0, S["whorl"][0], S["whorl"][1])))[0]


def tangent(v, n):
    t = v - n * v.dot(n)
    return t.normalized() if t.length > 1e-9 else t


def side_of(p):
    return 1 if p.x >= PART_X else -1


def behind(p):
    """0 in front of the crown's whorl, 1 behind it."""
    return smooth((p.y - W.y) / 0.03 + 0.5)


def flow_at(q, n):
    s = side_of(q)
    depth = top_z - q.z
    front = X * s + DOWN * (0.25 + 4.0 * depth) + BACK * 0.25
    fringe = smooth((0.22 - yfrac(q)) / 0.08) * (1.0 if s > 0 else 0.0)
    front = front.normalized() * (1 - fringe) + (X + DOWN * 0.3 - BACK * 0.3).normalized() * fringe
    away = q - W
    w = behind(q)
    f = front.normalized() * (1 - w) + (away.normalized() if away.length > 1e-6 else DOWN) * w
    t = tangent(f, n)
    return t if t.length > 0 else tangent(DOWN, n)


# ---- the rollers -------------------------------------------------------------
class Roller:
    pass


rollers = []
for kind, rows in S["rollers"].items():
    for az, el, radius, angle in rows:
        a, e = math.radians(az), math.radians(el)
        loc, nrm = cast(Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))))
        if loc is None:
            continue
        r = Roller()
        r.kind, r.centre, r.radius, r.angle = kind, loc, radius * MM, math.radians(angle)
        r.axis = nrm.cross(flow_at(loc, nrm)).normalized()
        r.side = side_of(loc)
        r.phase = (len(rollers) * 2.39996) % (2 * math.pi)          # the golden angle: phases spread, fixed
        rollers.append(r)


def roller_of(p):
    """The nearest roller; in front of the whorl only one on p's side of the parting."""
    front = behind(p) < 0.5
    best, bd = None, 1e9
    for i, r in enumerate(rollers):
        if front and r.side != side_of(p) and behind(r.centre) < 0.5:
            continue
        d = (r.centre - p).length
        if d < bd:
            best, bd = i, d
    return best


def group_of(p):
    """Hair is only blended within a roller and, in front of the whorl, one side of the parting."""
    return (roller_of(p), side_of(p) if behind(p) < 0.5 else 0)


def length_at(p):
    depth = top_z - p.z
    side = interp(S["length_side"], depth)
    back = interp(S["length_back"], depth)
    L = side + (back - side) * smooth((yfrac(p) - 0.5) / 0.2)
    fringe = smooth((0.22 - yfrac(p)) / 0.08) * (1.0 if side_of(p) > 0 else 0.0) * (1 - behind(p))
    L = L * (1 - fringe) + S["length_fringe"] * fringe
    return L * MM * (1 + 0.04 * math.sin(137 * p.x + 91 * p.y + 53 * p.z))     # +-4%, fixed by place


def keep_off(p, arc, envelope_extra=2 * MM):
    """Keep p between the skin (a little off it once past the root) and the envelope."""
    q, n, h = surface(p)
    lo = min(S["tip_off_skin"] * MM, arc * 0.5)
    hi = envelope(q) + envelope_extra
    if h < lo:
        return q + n * lo
    if h > hi:
        return q + n * hi
    return p


def resample(pts, n):
    seg = [(pts[i + 1] - pts[i]).length for i in range(len(pts) - 1)]
    acc = [0.0]
    for s in seg:
        acc.append(acc[-1] + s)
    L = acc[-1]
    out, j = [], 0
    for k in range(n):
        t = L * k / (n - 1)
        while j < len(seg) - 1 and acc[j + 1] < t:
            j += 1
        f = 0.0 if seg[j] == 0 else (t - acc[j]) / seg[j]
        out.append(pts[j].lerp(pts[j + 1], max(0.0, min(1.0, f))))
    return out


# ---- flow guides: no randomness beyond where they stand ----------------------
cand = [sample_root(rng) for _ in range(6000)]
w_i = min(range(len(cand)), key=lambda i: (cand[i][0] - W).length)
guides = []                      # (root, points, group, roller)
for i in farthest([c[0] for c in cand], S["flow_guides"], w_i):
    root, n = cand[i]
    grp = group_of(root)
    r = rollers[grp[0]]
    L = length_at(root)
    steps = 80
    ds = L / steps
    e_root = envelope(root)
    rise = math.radians(interp([(6 * MM, S["rise_deg"][0]), (30 * MM, S["rise_deg"][1])], e_root))
    d = (flow_at(root, n) * math.cos(rise) + n * math.sin(rise)).normalized()
    roll_len = min(r.radius * r.angle, S["roll_share_max"] * L)
    radius = roll_len / r.angle
    pos, arc, axis = root.copy(), 0.0, None
    pts = [pos.copy()]
    for k in range(steps):
        arc += ds
        if arc <= S["rise_mm"] * MM:
            pass
        elif arc < L - roll_len:
            q, nq, h = surface(pos)
            climb = max(-0.6, min(0.6, (envelope(q) - h) / (6 * MM)))
            d = (d * 0.6 + (flow_at(q, nq) + nq * climb).normalized() * 0.4).normalized()
        else:
            if axis is None:
                axis = (r.axis - d * r.axis.dot(d)).normalized()
            d = (Quaternion(axis, ds / radius) @ d).normalized()
        pos = keep_off(pos + d * ds, arc)
        pts.append(pos.copy())
    guides.append((root, resample(pts, S["points"]), grp, grp[0]))

by_group = collections.defaultdict(list)
for gi, g in enumerate(guides):
    by_group[g[2]].append(gi)

# ---- clump guides ----------------------------------------------------------
crng = random.Random(S["seed"] + 1)
ccand = [sample_root(crng) for _ in range(12000)]
clumps = []                      # (root, points, group, frames)
for i in farthest([c[0] for c in ccand], S["clumps"], 0):
    root, n = ccand[i]
    grp = group_of(root)
    pool = by_group.get(grp) or [gi for gi, g in enumerate(guides) if g[2][1] == grp[1]] or list(range(len(guides)))
    near = sorted(pool, key=lambda gi: (guides[gi][0] - root).length)[:4]
    ws = [1.0 / ((guides[gi][0] - root).length ** 2 + (2 * MM) ** 2) for gi in near]
    sw = sum(ws)
    pts = []
    for k in range(S["points"]):
        off = Vector()
        for gi, w in zip(near, ws):
            off += (guides[gi][1][k] - guides[gi][0]) * (w / sw)
        pts.append(root + off)
    # the ripple: one phase per roller, a little jitter per clump
    r = rollers[grp[0]]
    phase = r.phase + crng.uniform(-S["ripple_jitter"], S["ripple_jitter"])
    L = sum((pts[k + 1] - pts[k]).length for k in range(len(pts) - 1))
    roll_from = 1 - min(r.radius * r.angle, S["roll_share_max"] * L) / L
    for k in range(1, S["points"]):
        s = k / (S["points"] - 1)
        fade = smooth(s / 0.15) * (1 - smooth((s - roll_from) / 0.1))
        _q, nq, _h = surface(pts[k])
        pts[k] = pts[k] + nq * (S["ripple_mm"] * MM * math.sin(2 * math.pi * s * L / (S["ripple_wave_mm"] * MM) + phase) * fade)
        pts[k] = keep_off(pts[k], s * L)
    # frames carried along the clump without twisting
    T = [(pts[min(k + 1, len(pts) - 1)] - pts[max(k - 1, 0)]).normalized() for k in range(len(pts))]
    U = [T[0].cross(n).normalized() if T[0].cross(n).length > 1e-6 else T[0].orthogonal().normalized()]
    for k in range(1, len(T)):
        u = T[k - 1].rotation_difference(T[k]) @ U[-1]
        u = (u - T[k] * u.dot(T[k])).normalized()
        U.append(u)
    V = [T[k].cross(U[k]).normalized() for k in range(len(T))]
    clumps.append((root, pts, grp, U, V, L))

kd = KDTree(len(clumps))
for ci, c in enumerate(clumps):
    kd.insert(c[0], ci)
kd.balance()

# ---- strands ---------------------------------------------------------------
srng = random.Random(S["seed"] + 2)
positions, sizes, colours = [], [], []
NP = S["points"]
checks = collections.Counter()
over_max = 0.0
for _ in range(S["strands"]):
    root, n = sample_root(srng)
    side = side_of(root) if behind(root) < 0.5 else 0
    ci = None
    for _co, cj, _d in kd.find_n(root, 6):
        if clumps[cj][2][1] in (side, 0) or side == 0:
            ci = cj
            break
    if ci is None:
        ci = kd.find(root)[1]
    croot, cpts, _grp, U, V, L = clumps[ci]
    root_off = root - croot
    ang = srng.uniform(0, 2 * math.pi)
    rad = math.sqrt(srng.random())
    keep = 1 - srng.uniform(0, S["shorter"])
    grey = srng.uniform(*S["grey_share"])
    frizz = srng.random() < S["frizz_share"]
    pts = []
    for k in range(NP):
        s = keep * k / (NP - 1)
        f = s * (NP - 1)
        j = min(int(f), NP - 2)
        t = f - j
        gp = cpts[j].lerp(cpts[j + 1], t)
        u = U[j].lerp(U[j + 1], t).normalized()
        v = V[j].lerp(V[j + 1], t).normalized()
        disc_r = S["disc_mm"][0] + (S["disc_mm"][1] - S["disc_mm"][0]) * max(0.0, (s - 0.15) / 0.85)
        disc = (u * math.cos(ang) + v * math.sin(ang)) * (rad * disc_r * MM)
        w = smooth(s / 0.15)
        p = gp + root_off * (1 - w) + disc * w
        if frizz and k > 2:
            p = p + Vector((srng.uniform(-1, 1), srng.uniform(-1, 1), srng.uniform(-1, 1))) * S["frizz_mm"] * MM
        pts.append(p if k == 0 else keep_off(p, s * L))
    pts[0] = root
    # smooth: 0.3, three times, the root fixed
    for _it in range(3):
        pts = [pts[0]] + [pts[k] + ((pts[k - 1] + pts[k + 1]) * 0.5 - pts[k]) * 0.3 for k in range(1, NP - 1)] + [pts[-1]]
    for k in range(1, NP):
        pts[k] = keep_off(pts[k], keep * k / (NP - 1) * L)
    # the checks
    q, nq, h = surface(pts[0])
    if abs(h) > 1 * MM:
        checks["roots_off_skin_over_1mm"] += 1
    for p in pts[1:]:
        q, nq, h = surface(p)
        over = h - envelope(q)
        over_max = max(over_max, over)
        if over > 3 * MM:
            checks["points_beyond_envelope_3mm"] += 1
    positions.extend(pts)
    sizes.append(NP)
    c = [S["colour"][i] + (S["grey"][i] - S["colour"][i]) * grey for i in range(3)]
    colours.extend([c] * NP)

curves = bpy.data.hair_curves.new(STYLE)
curves.add_curves(sizes)
curves.attributes["position"].data.foreach_set("vector", [c for p in positions for c in (p.x, p.y, p.z)])
if "radius" not in curves.attributes:
    curves.attributes.new("radius", "FLOAT", "POINT")
curves.attributes["radius"].data.foreach_set("value", [STRAND_RADIUS] * len(positions))
hair = bpy.data.objects.new("Hair_" + STYLE, curves)
bpy.context.scene.collection.objects.link(hair)

# ---- the Alembic: the curves alone, in centimetres ------------------------
for o in bpy.context.scene.objects:
    o.select_set(o == hair)
bpy.context.view_layer.objects.active = hair
abc = os.path.join(OUT, STYLE + ".abc")
bpy.ops.wm.alembic_export(filepath=abc, selected=True, global_scale=100.0, start=1, end=1)

# the preview's colour, greying strand by strand (after the export: not in the groom)
coloured = False
try:
    col = curves.color_attributes.new("Col", "FLOAT_COLOR", "POINT")
    col.data.foreach_set("color", [v for c in colours for v in (c[0], c[1], c[2], 1.0)])
    curves.color_attributes.active_color = col
    coloured = True
except Exception as exc:                       # the preview falls back to one colour
    print("COLOUR", exc, flush=True)

# ---- pictures -------------------------------------------------------------
scn = bpy.context.scene
scn.render.engine = "BLENDER_WORKBENCH"
sh = scn.display.shading
sh.light = "STUDIO"
sh.color_type = "VERTEX" if coloured else "OBJECT"
sh.show_shadows = True
sh.shadow_intensity = 0.45
sh.show_cavity = True
sh.cavity_type = "WORLD"
scn.display.render_aa = "16"
if scn.world is None:
    scn.world = bpy.data.worlds.new("World")
scn.world.color = (0.42, 0.42, 0.44)
head.color = (0.72, 0.6, 0.55, 1)
hair.color = tuple(S["colour"]) + (1,)
if coloured:                                   # the head keeps its own colour in VERTEX mode
    hm = bpy.data.materials.new("skin")
    hm.diffuse_color = (0.72, 0.6, 0.55, 1)
    head.data.materials.clear()
    head.data.materials.append(hm)
scn.render.resolution_x, scn.render.resolution_y = 800, 800
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
scn.collection.objects.link(cam)
scn.camera = cam
cam.data.lens = 85
centre = Vector((cx, (y_front + y_back) / 2, top_z - 0.12))
views = {"front": Vector((0, -1, 0.05)), "side": Vector((1, 0, 0.05)), "back": Vector((0, 1, 0.05)),
         "three-quarter": Vector((0.7, -0.7, 0.15))}
if os.environ.get("LEDGER_HAIR_PICTURES", "1") == "0":      # the graphics card busy elsewhere
    views = {}
for name, d in views.items():
    cam.location = centre + d.normalized() * 1.1
    cam.rotation_euler = (centre - cam.location).to_track_quat("-Z", "Y").to_euler()
    scn.render.filepath = os.path.join(OUT, "%s-%s.png" % (STYLE, name))
    bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, STYLE + ".blend"))
report = {"style": STYLE, "head": HEAD, "attempt": 3, "curves": len(sizes), "points": len(positions),
          "flow_guides": len(guides), "clumps": len(clumps), "rollers": len(rollers),
          "scalp_triangles": len(tris), "scalp_area_m2": round(total, 4), "top_z": round(top_z, 3),
          "whorl": [round(v, 4) for v in W], "part_x": round(PART_X, 4),
          "checks": {"points_beyond_envelope_3mm": checks["points_beyond_envelope_3mm"],
                     "roots_off_skin_over_1mm": checks["roots_off_skin_over_1mm"],
                     "most_beyond_envelope_mm": round(over_max / MM, 2)},
          "coloured_preview": coloured,
          "abc": abc, "abc_bytes": os.path.getsize(abc) if os.path.exists(abc) else 0, "settings": S}
json.dump(report, open(os.path.join(OUT, STYLE + ".json"), "w"), indent=1)
print("GROW", json.dumps({k: v for k, v in report.items() if k != "settings"}), flush=True)
