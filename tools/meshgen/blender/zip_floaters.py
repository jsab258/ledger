"""The zip's teeth and stops and the hip welts' lips, built as thin shapes floating just over the drape, to be baked
into the game mesh's textures.

    blender -b --factory-startup -P tools/meshgen/blender/zip_floaters.py -- LOW.blend PLAN.json IMPORT.json
        [--pitch 0.0017] [--proud 0.0003] [--lip 0.0015]

WHY, 27 October 2026 (Tom's zip jacket, the bake chain's step 6: production/art/clothing/tom-outfit/
BAKE-PLAN-2026-10-27.md; the route: production/research/game-clothing-pipeline/ZIP-POCKETS-2026-10-26.md). At the
game's distance a zip's teeth and a welt's lips are a few pixels: games bake them from detail floated over the
cloth, not model them into the mesh (CLO's own advice for games; the Polycount wiki). The detail follows the drape:

- THE TEETH: one interleaved row of metal elements (DECISIONS, 27 October: metal, as cotton blousons of the cut
  carried; moulded plastic belongs to nylon anoraks) along the line where the two tapes are sewn to each other,
  alternating sides every --pitch, each about a #5 zip's element (across 6 mm, along 1.5 mm, 1.6 mm high), --proud
  over the tape; one frame per element from the line's direction and the drape's own normal there.
- THE STOPS: a bottom stop over the zip's first 8 mm; a top clip on each tape 1 to 8 mm under the collar's top.
- THE WELTS: each a rectangle from the plan's place (each front's pattern millimetres, its lean from upright), its
  two lips 7 mm wide with a 1 mm slit between, rounded --lip high, lifted onto the drape through the front's own
  pattern, with a bar tack at each end.

Writes the objects Teeth, Stops and Welts into LOW.blend (materials Teeth, Stop, Welt: the ID mask's sources) and
floaters.json beside it with its checks: the count of teeth against the zip's length over the pitch, the gap from
every floater point to the drape, and each welt's place and lean measured back on the drape.
"""
import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform, intersect_point_tri_2d
from mathutils.kdtree import KDTree

argv = sys.argv[sys.argv.index("--") + 1:]
LOW, PLAN, IMPORT = argv[0], argv[1], argv[2]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
PITCH = opt("--pitch", 0.0017)          # along the chain, element to element (alternating sides)
PROUD = opt("--proud", 0.0003)
LIP = opt("--lip", 0.0015)
EL_ACROSS, EL_ALONG, EL_HIGH = 0.006, 0.0015, 0.0016
plan = json.load(open(PLAN, encoding="utf-8"))
imp = json.load(open(IMPORT, encoding="utf-8"))
NAMES = [p["key"] for p in plan["pieces"]]
log = {"low": LOW, "pitch": PITCH, "checks": {}}

bpy.ops.wm.open_mainfile(filepath=LOW)
drape = bpy.data.objects["Jacket"]
body = bpy.data.objects["Body"]
db = bmesh.new()
db.from_mesh(drape.data)
db.transform(drape.matrix_world)
db.normal_update()
db.faces.ensure_lookup_table()
pl = db.faces.layers.int["piece"]
pat = db.loops.layers.uv["pattern"]
BVH = BVHTree.FromBMesh(db)
# the garment's own vertical axis (its placed points' mean), to turn the drape's normals outward (the first run took
# the body's raw vertex numbers, in centimetres and unplaced: the axis fell 9 m in front, and every floater went inside)
axis_x = sum(v.co.x for v in db.verts) / len(db.verts)
axis_y = sum(v.co.y for v in db.verts) / len(db.verts)


def outward(p, n):
    away = Vector((p.x - axis_x, p.y - axis_y, 0.0))
    return n if n.dot(away) >= 0 else -n


def mat(name, col, metal=0.0, rough=0.5):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*col, 1.0)
    bsdf.inputs["Metallic"].default_value = metal
    bsdf.inputs["Roughness"].default_value = rough
    return m


def new_obj(name, bm_, m):
    me = bpy.data.meshes.new(name)
    bm_.to_mesh(me)
    bm_.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(m)
    return o


def box(bm_, centre, t, b, n, along, across, high):
    """A box centred at centre: along t, across b, high along n (its base on the centre's plane)."""
    vs = []
    for sz in (0.0, high):
        for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            vs.append(bm_.verts.new(centre + t * (sa * along / 2) + b * (sb * across / 2) + n * sz))
    for q in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
        bm_.faces.new([vs[i] for i in q])


def pillow(bm_, centre, t, b, n, along, across, high, nu=4, nv=6):
    """A rounded element: its top a grid domed across and along (a box's flat top faces the way the cloth does and
    bakes no relief into a normal map: the first bake's teeth were invisible in it), its edges a quarter of its
    height, a skirt down to its base."""
    top = [[None] * (nv + 1) for _ in range(nu + 1)]
    for i in range(nu + 1):
        u = -1.0 + 2.0 * i / nu
        for j in range(nv + 1):
            v = -1.0 + 2.0 * j / nv
            z = high * (0.25 + 0.75 * math.sqrt(max(0.0, 1 - u * u)) * math.sqrt(max(0.0, 1 - v * v)))
            top[i][j] = bm_.verts.new(centre + t * (u * along / 2) + b * (v * across / 2) + n * z)
    for i in range(nu):
        for j in range(nv):
            bm_.faces.new((top[i][j], top[i + 1][j], top[i + 1][j + 1], top[i][j + 1]))
    ring = [top[i][0] for i in range(nu + 1)] + [top[nu][j] for j in range(1, nv + 1)] + \
           [top[i][nv] for i in range(nu - 1, -1, -1)] + [top[0][j] for j in range(nv - 1, 0, -1)]
    base = [bm_.verts.new(v.co - n * (v.co - centre).dot(n)) for v in ring]
    for k in range(len(ring)):
        a, c = ring[k], ring[(k + 1) % len(ring)]
        bm_.faces.new((base[k], base[(k + 1) % len(ring)], c, a))


# ---- the zip's line: where the two tapes are sewn to each other, bottom to top ---------------------------------
iR, iL = NAMES.index("tapeR"), NAMES.index("tapeL")
line_edges = [e for e in db.edges if {f[pl] for f in e.link_faces} == {iR, iL}]
adj = {}
for e in line_edges:
    a, b = e.verts
    adj.setdefault(a, []).append(b)
    adj.setdefault(b, []).append(a)
ends = [v for v, nb in adj.items() if len(nb) == 1]
start = min(ends, key=lambda v: v.co.z)
path, prev, cur = [start], None, start
while True:
    nxt = [x for x in adj[cur] if x is not prev]
    if not nxt:
        break
    prev, cur = cur, nxt[0]
    path.append(cur)
P = [v.co.copy() for v in path]
N = []
for v in path:
    n = sum((f.normal for f in v.link_faces), Vector())
    N.append(outward(v.co, n.normalized()))
cum = [0.0]
for a, b in zip(P, P[1:]):
    cum.append(cum[-1] + (b - a).length)
L = cum[-1]
log["checks"]["zipLengthMm"] = round(1000 * L, 1)


def at(s):
    """The zip line's point, direction and outward normal at s metres from its bottom."""
    s = max(0.0, min(L, s))
    j = max(0, min(len(P) - 2, next((k for k in range(len(cum) - 1) if cum[k + 1] >= s), len(P) - 2)))
    seg = cum[j + 1] - cum[j]
    t_ = 0.0 if seg < 1e-12 else (s - cum[j]) / seg
    p = P[j].lerp(P[j + 1], t_)
    tan = (P[j + 1] - P[j]).normalized()
    n = N[j].lerp(N[j + 1], t_).normalized()
    n = (n - tan * n.dot(tan)).normalized()
    return p, tan, n


# ---- the teeth --------------------------------------------------------------------------------------------------
tb = bmesh.new()
STOP_LOW, STOP_TOP = 0.008, 0.008
s, k = STOP_LOW + PITCH / 2, 0
while s < L - STOP_TOP:
    p, tan, n = at(s)
    b = tan.cross(n).normalized()
    side = 1 if k % 2 == 0 else -1
    # each element reaches from its own tape across the centre into the gap between the other side's elements
    centre = p + b * (side * EL_ACROSS / 6) + n * PROUD
    pillow(tb, centre, tan, b, n, EL_ALONG, EL_ACROSS * 2 / 3, EL_HIGH)
    s += PITCH
    k += 1
log["checks"]["teeth"] = k
log["checks"]["teethExpected"] = int((L - STOP_LOW - STOP_TOP) / PITCH)
teeth = new_obj("Teeth", tb, mat("Teeth", (0.62, 0.60, 0.56), metal=1.0, rough=0.35))

# ---- the stops: a bottom box, a top clip on each tape -----------------------------------------------------------
sb_ = bmesh.new()
p, tan, n = at(STOP_LOW / 2)
pillow(sb_, p + n * PROUD, tan, tan.cross(n).normalized(), n, STOP_LOW, 0.007, 0.0028)
for side in (1, -1):
    p, tan, n = at(L - 0.0045)
    b = tan.cross(n).normalized()
    pillow(sb_, p + b * (side * 0.0022) + n * PROUD, tan, b, n, 0.0035, 0.0025, 0.0018)
stops = new_obj("Stops", sb_, mat("Stop", (0.55, 0.53, 0.50), metal=1.0, rough=0.4))

# ---- the welts: lifted through each front's own pattern ---------------------------------------------------------
tris = {}
for f in db.faces:
    name = NAMES[f[pl]]
    if not name.startswith("front"):
        continue
    ls = f.loops
    for j in range(1, len(ls) - 1):
        a, b, c = ls[0], ls[j], ls[j + 1]
        tris.setdefault(name, []).append(((a[pat].uv.to_3d(), b[pat].uv.to_3d(), c[pat].uv.to_3d()),
                                          (a.vert.co.copy(), b.vert.co.copy(), c.vert.co.copy()), f.normal.copy()))
kds = {}
for name, ts in tris.items():
    kd = KDTree(len(ts))
    for j, (u3, _p, _n) in enumerate(ts):
        kd.insert((u3[0] + u3[1] + u3[2]) / 3, j)
    kd.balance()
    kds[name] = kd


def lift(name, u, v):
    q = Vector((u, v, 0.0))
    for _co, j, _d in kds[name].find_n(q, 32):
        (a, b, c), (p, r, s_), n = tris[name][j]
        if intersect_point_tri_2d(q, a, b, c):
            x = barycentric_transform(q, a, b, c, p, r, s_)
            return x, outward(x, n), True
    _co, j, _d = kds[name].find(q)
    (a, b, c), (p, r, s_), n = tris[name][j]
    x = barycentric_transform(q, a, b, c, p, r, s_)
    return x, outward(x, n), False


wb = bmesh.new()
welt_log, welt_miss = [], 0
for w in plan["welts"]:
    name = w["piece"]
    off = imp["pieces"][name]["layoutOffsetM"]
    cx, cy = w["centre"][0] / 1000.0 + off, w["centre"][1] / 1000.0
    lam = math.radians(w["leanDegreesFromUpright"])
    ax = Vector((math.sin(lam), math.cos(lam)))          # along the welt, from its foot to its top
    cr = Vector((ax.y, -ax.x))                           # across it
    Lw = w["length"] / 1000.0
    NU, NV = 40, 6
    for lip_lo, lip_hi in ((-0.0075, -0.0005), (0.0005, 0.0075)):
        grid = []
        for i in range(NU + 1):
            row = []
            for j in range(NV + 1):
                fu = -Lw / 2 + Lw * i / NU
                fv = lip_lo + (lip_hi - lip_lo) * j / NV
                uv = Vector((cx, cy)) + ax * fu + cr * fv
                x, nrm, ok = lift(name, uv.x, uv.y)
                welt_miss += not ok
                h = LIP * math.sin(math.pi * j / NV) + 0.0002
                row.append(wb.verts.new(x + nrm * h))
            grid.append(row)
        for i in range(NU):
            for j in range(NV):
                wb.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))
    # the bar tacks at the welt's two ends
    for e in (-1, 1):
        uv = Vector((cx, cy)) + ax * (e * Lw / 2)
        x, nrm, _ok = lift(name, uv.x, uv.y)
        u2 = Vector((cx, cy)) + ax * (e * Lw / 2 + 0.001)
        x2, _n2, _ok2 = lift(name, u2.x, u2.y)
        t3 = (x2 - x).normalized() if (x2 - x).length > 1e-9 else Vector((0, 0, 1))
        box(wb, x + nrm * 0.0002, t3, t3.cross(nrm).normalized(), nrm, 0.003, 0.016, 0.0009)
    # measured back on the drape: the welt's centre over the front's hem seam, and its lean from upright
    c3, nc3, _ok = lift(name, cx, cy)
    top3, _n, _ok = lift(name, cx + ax.x * Lw / 2, cy + ax.y * Lw / 2)
    foot3, _n, _ok = lift(name, cx - ax.x * Lw / 2, cy - ax.y * Lw / 2)
    band = NAMES.index("bandFront" + name[-1])
    seam = [v.co for e in db.edges if {f[pl] for f in e.link_faces} == {NAMES.index(name), band} for v in e.verts]
    hem_z = sum(s3.z for s3 in seam) / len(seam)
    d3 = top3 - foot3
    # the lean along the cloth: the welt's direction and the upright, both laid in the cloth's own plane at the welt
    # (seen from the front it reads nearly upright, 0.5 to 1.6 degrees, because 55% of the way to the side seam the
    # front is turning back round the body; the straight line from foot to top read 26, its depth counted as lean)
    up_t = (Vector((0, 0, 1)) - nc3 * nc3.z).normalized()
    d_t = (d3 - nc3 * nc3.dot(d3)).normalized()
    lean3 = math.degrees(math.acos(max(-1.0, min(1.0, d_t.dot(up_t)))))
    welt_log.append({"piece": name, "centreAboveBandSeamMm": round(1000 * (c3.z - hem_z), 1), "leanDegrees": round(lean3, 1),
                     "lengthMm": round(1000 * d3.length, 1)})
welts = new_obj("Welts", wb, mat("Welt", (0.30, 0.31, 0.33), metal=0.0, rough=0.7))
log["checks"]["welts"] = welt_log
log["checks"]["weltLiftMisses"] = welt_miss

# ---- every floater point's gap to the drape --------------------------------------------------------------------
# each object's points: its base (the lowest point of each element or lip, which should sit just over the cloth)
# and its whole height, separately
for o in (teeth, stops, welts):
    gaps = []
    for v in o.data.vertices:
        hit = BVH.find_nearest(o.matrix_world @ v.co)
        if hit[0] is not None:
            gaps.append(hit[3])
    gaps.sort()
    log["checks"]["gapMm_" + o.name] = {"min": round(1000 * gaps[0], 2), "p5": round(1000 * gaps[len(gaps) // 20], 2),
                                         "median": round(1000 * gaps[len(gaps) // 2], 2), "max": round(1000 * gaps[-1], 2)}
bpy.ops.wm.save_as_mainfile(filepath=LOW)
json.dump(log, open(os.path.join(os.path.dirname(LOW), "floaters.json"), "w", encoding="utf-8"), indent=1)
print("FLOATERS", json.dumps(log["checks"]))
