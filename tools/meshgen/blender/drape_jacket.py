"""A donkey jacket hung on a MetaHuman body by Blender's cloth simulation: a simulation mesh and a render mesh.

    blender -b -P tools/meshgen/blender/drape_jacket.py -- BODY.fbx OUT_DIR [--name NAME] [--offset 0.025] [--frames 60]

WHY, 28 September (Jafar's list, item 5, and production/research/character-
pipeline/clothing-and-face-lighting-2026-09-27.md): "sew the garment around
the actual MetaHuman body in Blender, with a separate simulation mesh". The
25 September jacket (donkey_jacket.py) was the body's own skin pushed out and
smoothed: it did not hang or swing like cloth (FINDINGS). This one starts the
same way, a shell cut from the body's torso and arms and stood off it, but
from a coarser level of the body, so its triangles are even and a few
centimetres across, which is what a simulation mesh wants (the research:
"thin, single-sided and simplified"). The hem is let down to the top of the
thigh. Then Blender's cloth simulation hangs it on the body under gravity,
held at the shoulders and collar, so it falls into folds against the body as
heavy wool does. What it settles into is the SIMULATION MESH; the RENDER
MESH is that, subdivided once, given the cloth's thickness, the black yoke
across the shoulders, four buttons and two patch pockets. Both carry the
body's skin weights (copied from the nearest part of the body), so either
moves with any MetaHuman skeleton.

OUT_DIR gets NAME.fbx (the render mesh, the simulation mesh and the armature,
nothing of the body), NAME_front.png and NAME_side.png (the check pictures,
on the grey body) and NAME.json (counts, sizes, the drape's settling).
"""
import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
BODY, OUT = argv[0], argv[1]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "donkey_jacket_draped", str)
OFFSET = opt("--offset", 0.03)
FRAMES = opt("--frames", 90, int)
SOURCE_LOD = opt("--lod", 1, int)       # the body level the shell is cut from: even, few-centimetre triangles
SMOOTH = opt("--smooth", 120, int)     # smoothing passes over the shell before it hangs
SLEEVE_SMOOTH = opt("--sleeve-smooth", 40, int)
# EASE over the outermost point: 5 cm, since the jacket goes over a jumper
# (1 cm let Ron's navy jumper through across his belly in the game, first
# wearing; 3 cm still did low on the belly with his arms forward, 28 September).
EASE = opt("--ease", 0.05)
os.makedirs(OUT, exist_ok=True)

NAVY = (0.02, 0.022, 0.032, 1.0)        # dark navy melton, near black (the first was too blue in the game)
YOKE = (0.004, 0.004, 0.0045, 1.0)      # the black leather (later PVC) panel, glossy and blacker than the wool
BUTTON = (0.02, 0.018, 0.016, 1.0)
TORSO_BONES = ("pelvis", "spine_", "clavicle", "upperarm", "lowerarm", "neck_01")
HAND_BONES = ("hand", "thumb", "index", "middle", "ring", "pinky", "wrist")

# ---------------------------------------------------------------- the body
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY)
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
meshes = sorted([o for o in bpy.context.scene.objects if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
body, source = meshes[0], meshes[min(SOURCE_LOD, len(meshes) - 1)]
for o in meshes:
    if o is not body and o is not source:
        bpy.data.objects.remove(o, do_unlink=True)
bpy.context.view_layer.update()


def joint(name):
    return arm.matrix_world @ arm.data.bones[name].head_local


pelvis, spine5, neck = joint("pelvis"), joint("spine_05"), joint("neck_01")
upperarm_l, thigh_l = joint("upperarm_l"), joint("thigh_l")
# THE HEM at mid-thigh: the references give a back length of 81 to 90 cm
# (production/reference/donkey-jacket-1990.md); the top of the thigh gave 72.
HEM = thigh_l.z - 0.21
NECK_CUT = neck.z - 0.02             # close round the base of the neck
ARMPIT = upperarm_l.z - 0.09
# THE NECK'S RADIUS, from the body at the neck bone's height.
_ring = [body.matrix_world @ v.co for v in body.data.vertices if abs((body.matrix_world @ v.co).z - neck.z) < 0.01]
_ring = [p for p in _ring if (Vector((p.x, p.y, 0.0)) - Vector((neck.x, neck.y, 0.0))).length < 0.12]
NECK_R = sorted((Vector((p.x, p.y, 0.0)) - Vector((neck.x, neck.y, 0.0))).length for p in _ring)[len(_ring) // 2] if _ring else 0.06


def dominant(o, v, names):
    best, w = "", 0.0
    for g in v.groups:
        if g.weight > w:
            best, w = names.get(g.group, ""), g.weight
    return best


def shell_from(src):
    """The torso and arms of src, cut at the hips, the neck and the wrists, in world metres, welded, one piece."""
    # BY HEIGHT, not by bone: the bone cut followed the thighs up round the
    # seat and left tabs on the hem (first try, 28 September). Everything
    # between the hips and the base of the neck but the hands.
    names = {g.index: g.name for g in src.vertex_groups}
    keep = set()
    for v in src.data.vertices:
        d = dominant(src, v, names)
        p = src.matrix_world @ v.co
        if any(d.startswith(h) for h in HAND_BONES) or d.startswith("head") or d.startswith("neck_02"):
            continue
        if p.z < pelvis.z - 0.015 or p.z > NECK_CUT + 0.03:
            continue
        # ROUND THE NECK, not across it: a cut by height alone left a hole as
        # wide as the shoulders' slope and a collar like a ring (third try).
        if p.z > NECK_CUT - 0.07 and (Vector((p.x, p.y, 0.0)) - Vector((neck.x, neck.y, 0.0))).length < NECK_R + 0.012:
            continue
        keep.add(v.index)
    me = src.data.copy()
    me.transform(src.matrix_world)
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if not all(v.index in keep for v in f.verts)], context="FACES")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
    bm.verts.ensure_lookup_table()
    seen, pieces = set(), []
    for v in bm.verts:
        if v in seen:
            continue
        stack, piece = [v], []
        seen.add(v)
        while stack:
            x = stack.pop()
            piece.append(x)
            for e in x.link_edges:
                y = e.other_vert(x)
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        pieces.append(piece)
    pieces.sort(key=len, reverse=True)
    for piece in pieces[1:]:
        bmesh.ops.delete(bm, geom=piece, context="VERTS")
    bm.normal_update()
    return bm


bm = shell_from(source)
for v in bm.verts:
    v.co += v.normal * OFFSET
inner = [v for v in bm.verts if not v.is_boundary]
# AWAY WITH THE BODY'S MUSCLE: on Ron's own body 20 passes still showed his
# chest and shoulders through the cloth (first try on him, 28 September).
# The torso takes the heavy smoothing; the sleeves only 40 passes, since more
# slimmed them and opened the cuffs until they slid off his hands.
_names = {g.index: g.name for g in source.vertex_groups}
_dl = bm.verts.layers.deform.active


def _arm(v):
    if _dl is None:
        return False
    best, w = "", 0.0
    for gi, wt in v[_dl].items():
        if wt > w:
            best, w = _names.get(gi, ""), wt
    return best.startswith(("upperarm", "lowerarm"))


# ...and only well inside the armholes: smoothed far more than the sleeves
# next to it, the torso pulled away from them there and the sleeves hung
# like flaps (28 September).
torso_inner = [v for v in inner if not _arm(v) and abs(v.co.x) < abs(upperarm_l.x) - 0.05]
arm_inner = [v for v in inner if v not in set(torso_inner)]
for n in range(SMOOTH):
    bmesh.ops.smooth_vert(bm, verts=inner if n < SLEEVE_SMOOTH else torso_inner, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
bm.normal_update()
# CLEARANCE, not a guessed push-back: smoothing shrinks the shell, so every
# point that came nearer the body than the standoff is carried straight back
# out to it. Heavy smoothing then takes the muscle away without the cloth
# ever passing into the body (40 passes and a fixed push still showed Ron's
# chest in the game, 28 September).
from mathutils.bvhtree import BVHTree
_bm_body = bmesh.new()
_bm_body.from_mesh(body.data)
_bm_body.transform(body.matrix_world)
BODY_BVH = BVHTree.FromBMesh(_bm_body)


def clearance(verts, need):
    moved = 0
    for v in verts:
        hit = BODY_BVH.find_nearest(v.co)
        if hit[0] is None:
            continue
        loc, _n, _i, dist = hit
        if dist < need:
            d = (v.co - loc)
            d = d.normalized() if d.length > 1e-9 else v.normal
            v.co = loc + d * need
            moved += 1
    return moved


CLEARED = clearance(torso_inner, OFFSET)
for v in arm_inner:                  # the sleeves: the push-back that kept them on
    v.co += v.normal * (0.006 + 0.0002 * SLEEVE_SMOOTH)

# HUNG STRAIGHT FROM THE CHEST: heavy wool bridges the waist instead of
# following it. Round the body's upright axis, each torso point below the
# chest is pushed out to at least the chest's own distance in its direction,
# fully 8 cm under the chest, not at all at the chest.
AX = Vector((pelvis.x, pelvis.y, 0.0))
CHEST = ARMPIT - 0.03
BINS = 72
arm_names = ("upperarm", "lowerarm")


def angle_bin(co):
    return int(((math.atan2(co.y - AX.y, co.x - AX.x) + math.pi) / (2 * math.pi)) * BINS) % BINS


def radius(co):
    return (Vector((co.x, co.y, 0.0)) - AX).length


# THE ARMS are told apart by their bones (the shell keeps the body's weights).
src_names = {g.index: g.name for g in source.vertex_groups}
dl = bm.verts.layers.deform.active


def on_arm(v):
    if dl is None:
        return abs(v.co.x - AX.x) > abs(upperarm_l.x) - 0.02
    best, w = "", 0.0
    for gi, wt in v[dl].items():
        if wt > w:
            best, w = src_names.get(gi, ""), wt
    return best.startswith(arm_names)


def hull2d(pts):
    """The convex hull of flat points, anticlockwise (Andrew's monotone chain)."""
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def hull_reach(hull, d):
    """How far out from the axis, along the flat unit direction d, the hull's edge lies (hull points relative to the axis)."""
    best = 0.0
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        ex, ey = b[0] - a[0], b[1] - a[1]
        den = d[0] * ey - d[1] * ex
        if abs(den) < 1e-12:
            continue
        t = (a[0] * ey - a[1] * ex) / den
        u = (a[0] * d[1] - a[1] * d[0]) / den
        if t > 0 and -1e-9 <= u <= 1 + 1e-9:
            best = max(best, t)
    return best


# ACROSS THE HOLLOWS: stiff melton spans the chest from one high point to the
# next instead of dipping between them; with the shell stood off the body
# point by point, Ron's pectorals showed through the cloth in the game (28
# September). In 2 cm slices from under the chest to below the collar, each
# point is pushed out to the slice's convex outline (at most 4 cm), then the
# slices are smoothed together.
chest_band = [v for v in bm.verts if CHEST - 0.10 < v.co.z < NECK_CUT - 0.04 and not on_arm(v)]
_slices = {}
for v in chest_band:
    _slices.setdefault(int((v.co.z - CHEST) // 0.02), []).append(v)
FILLED = 0
for vs in _slices.values():
    hull = hull2d([(round(v.co.x - AX.x, 5), round(v.co.y - AX.y, 5)) for v in vs]) if len(vs) >= 6 else []
    if len(hull) < 3:
        continue
    for v in vs:
        rel = Vector((v.co.x - AX.x, v.co.y - AX.y, 0.0))
        r = rel.length
        if r < 1e-6:
            continue
        d = rel / r
        out = hull_reach(hull, (d.x, d.y)) - r
        if 0.001 < out < 0.04:
            v.co.x += d.x * out
            v.co.y += d.y * out
            FILLED += 1
for _ in range(4):
    bmesh.ops.smooth_vert(bm, verts=[v for v in chest_band if not v.is_boundary], factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=False)
bm.normal_update()

# THE OUTERMOST POINT in each direction anywhere from the armpits to the
# hips (a chest, a bust, a belly or a seat): the cloth hangs from it (the
# second try took the chest at armpit height, above the fullest part, and
# the front still followed the body).
chest_r = [0.0] * BINS
for v in bm.verts:
    if CHEST - 0.35 < v.co.z < CHEST + 0.02 and not on_arm(v):
        k = angle_bin(v.co)
        chest_r[k] = max(chest_r[k], radius(v.co))
for k in range(BINS):                         # fill any empty direction from its neighbours
    if chest_r[k] == 0.0:
        chest_r[k] = max(chest_r[(k - 1) % BINS], chest_r[(k + 1) % BINS])
# the outline it hangs from is convex too: no groove down the breastbone
_ang = [(k + 0.5) / BINS * 2 * math.pi - math.pi for k in range(BINS)]
_ch = hull2d([(round(math.cos(a) * r, 5), round(math.sin(a) * r, 5)) for a, r in zip(_ang, chest_r)])
if len(_ch) >= 3:
    chest_r = [max(r, hull_reach(_ch, (math.cos(a), math.sin(a)))) for a, r in zip(_ang, chest_r)]


def hang(v, extra=0.0):
    k = angle_bin(v.co)
    want = chest_r[k] + EASE + extra      # room over the clothes beneath
    r = radius(v.co)
    if r <= 1e-6:
        return
    w = min(1.0, max(0.0, (CHEST - v.co.z) / 0.08))
    if r < want:
        d = (Vector((v.co.x, v.co.y, 0.0)) - AX).normalized()
        v.co += d * (want - r) * w


for v in bm.verts:
    if v.co.z < CHEST and not on_arm(v):
        hang(v)

# THE HEM LET DOWN: the cut at the hips is carried down to the top of the
# thigh in four rows, at the chest's distance, flaring a centimetre, as a
# jacket's skirt stands off the seat.
bm.edges.ensure_lookup_table()
bottom = [e for e in bm.edges if e.is_boundary and all(v.co.z < pelvis.z + 0.02 for v in e.verts)]
rows = max(4, round((pelvis.z - 0.015 - HEM) / 0.05))   # rows about 5 cm apart
edges = bottom
for r in range(rows):
    res = bmesh.ops.extrude_edge_only(bm, edges=edges)
    new_verts = [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]
    drop = (pelvis.z - 0.015 - HEM) / rows
    for v in new_verts:
        v.co.z -= drop
        hang(v, extra=0.01 * (r + 1) / rows)
    edges = [g for g in res["geom"] if isinstance(g, bmesh.types.BMEdge) and all(v in new_verts for v in g.verts)]
bm.normal_update()
# The push is made direction by direction, so it leaves upright ridges; a few
# passes of smoothing below the chest take them out without undoing the hang.
lower = [v for v in bm.verts if v.co.z < CHEST and not v.is_boundary and not on_arm(v)]
for _ in range(6):
    bmesh.ops.smooth_vert(bm, verts=lower, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=False)
bm.normal_update()

jacket_me = bpy.data.meshes.new(NAME + "_sim")
bm.to_mesh(jacket_me)
bm.free()
sim = bpy.data.objects.new(NAME + "_sim", jacket_me)
bpy.context.collection.objects.link(sim)

# THE HOLD: the shoulders and collar are held (they rest on the body in a
# real jacket); everything below the armpits hangs free, the sleeves too.
pin = sim.vertex_groups.new(name="hold")
for v in sim.data.vertices:
    p = v.co
    if p.z > ARMPIT + 0.03 and abs(p.x) < abs(upperarm_l.x) + 0.02:
        w = min(1.0, (p.z - ARMPIT - 0.03) / 0.06)
        pin.add([v.index], w, "REPLACE")

# ---------------------------------------------------------------- the drape
body_world = body.copy()
body_world.data = body.data.copy()
body_world.data.transform(body.matrix_world)
body_world.parent = None
body_world.matrix_world = Matrix.Identity(4)
for m in list(body_world.modifiers):
    body_world.modifiers.remove(m)
bpy.context.collection.objects.link(body_world)
col = body_world.modifiers.new("Collision", "COLLISION")
body_world.collision.thickness_outer = 0.004
body_world.collision.cloth_friction = 5.0

cloth = sim.modifiers.new("Cloth", "CLOTH")
s = cloth.settings
s.quality = 10
s.mass = 0.6                          # heavy melton wool: about 600 g a square metre
s.air_damping = 2.0
s.tension_stiffness = s.compression_stiffness = 60.0
s.shear_stiffness = 40.0
s.bending_stiffness = 8.0             # stiff cloth folds broadly (20 made the sleeves rigid tubes that slid off his arms)
s.vertex_group_mass = "hold"
s.pin_stiffness = 1.0
cloth.collision_settings.distance_min = 0.005
cloth.collision_settings.use_self_collision = False
scene = bpy.context.scene
scene.frame_start, scene.frame_end = 1, FRAMES
cloth.point_cache.frame_start, cloth.point_cache.frame_end = 1, FRAMES
before = [v.co.copy() for v in sim.data.vertices]
prev = None
for f in range(1, FRAMES + 1):
    scene.frame_set(f)
    if f == FRAMES - 1:
        prev = [v.co.copy() for v in sim.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.vertices]
dg = bpy.context.evaluated_depsgraph_get()
final = sim.evaluated_get(dg).to_mesh()
last_move = max((a.co - b).length for a, b in zip(final.vertices, prev)) if prev else 0.0
drop_max = max((b - a.co).length for a, b in zip(final.vertices, before))
settled = bpy.data.meshes.new_from_object(sim.evaluated_get(dg))
sim.modifiers.clear()
sim.data = settled
# CLEAR OF THE JUMPER, after it has settled: the front falls back onto his
# belly as it settles, to 1 cm of his skin, and his jumper, which lies on the
# skin, came through it in the game (28 September, measured after the fourth
# film). Every point of the body of the jacket nearer his skin than 3.5 cm is
# carried straight back out to 3.5 cm; the folds stay where they fell.
JUMPER_CLEAR = opt("--jumper-clear", 0.035)
_cb = bmesh.new()
_cb.from_mesh(sim.data)
_cb.normal_update()
_bnames = {g.index: g.name for g in body.vertex_groups}


def nearest_is_arm(co):
    """Whether the body's nearest point is on an arm (the sleeves keep their own fit)."""
    hit = BODY_BVH.find_nearest(co)
    if hit[0] is None:
        return False
    v = body.data.vertices[body.data.polygons[hit[2]].vertices[0]]
    best, w = "", 0.0
    for g in v.groups:
        if g.weight > w:
            best, w = _bnames.get(g.group, ""), g.weight
    return best.startswith(("upperarm", "lowerarm", "hand"))


# from the chest down only: taken up to the neckline, the smoothing moved the
# cloth the collar is laid on and the collar crumpled in the game (sixth try)
_torso = [v for v in _cb.verts if v.co.z < NECK_CUT - 0.10 and not nearest_is_arm(v.co)]
# HUNG STRAIGHT AGAIN, and the chest filled across again: settling let the
# front fall back in under the chest, and pushed off the body by a fixed
# distance it then followed his chest's shape: two rounded bulges that read
# as a bust (seventh try, 29 September). Stiff melton hangs straight from the
# fullest point and spans the chest.
for v in _torso:
    if v.co.z < CHEST:
        hang(v)
_band = [v for v in _torso if v.co.z >= CHEST - 0.02]
_bs = {}
for v in _band:
    _bs.setdefault(int((v.co.z - CHEST) // 0.02), []).append(v)
for vs in _bs.values():
    hull = hull2d([(round(v.co.x - AX.x, 5), round(v.co.y - AX.y, 5)) for v in vs]) if len(vs) >= 6 else []
    if len(hull) < 3:
        continue
    for v in vs:
        rel = Vector((v.co.x - AX.x, v.co.y - AX.y, 0.0))
        r = rel.length
        if r < 1e-6:
            continue
        d = rel / r
        out = hull_reach(hull, (d.x, d.y)) - r
        if 0.001 < out < 0.04:
            v.co.x += d.x * out
            v.co.y += d.y * out
_cb.normal_update()
RECLEARED = clearance(_torso, JUMPER_CLEAR)
# SMOOTHED BACK TOGETHER: pushed point by point, the cloth kept small creases
# where pushed points met unpushed ones, dark pinches on the chest in every
# film (fifth try, 28 September); a few rounds of smoothing, each followed by
# the same clearance, leave it even and still clear.
_inner = [v for v in _torso if not v.is_boundary]
for _ in range(4):
    bmesh.ops.smooth_vert(_cb, verts=_inner, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    bmesh.ops.smooth_vert(_cb, verts=_inner, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    _cb.normal_update()
    clearance(_torso, JUMPER_CLEAR)
# THE SLEEVES AS STRAIGHT TUBES: stood off his arm point by point they kept
# the shape of his biceps and forearm and read as a quilted puffer's sleeves
# (the blind reviewer, 29 September). Round each arm's bones, shoulder to
# elbow to wrist, every sleeve point is set at a radius tapering evenly from
# the upper arm's to the cuff's, blended in from the armhole so the sleeve
# still meets the body; then kept clear of the arm.
_sleeve = [v for v in _cb.verts if v.co.z < NECK_CUT - 0.03 and nearest_is_arm(v.co)]
SLEEVED = 0
for side in ("l", "r"):
    sh, el, wr = joint("upperarm_" + side), joint("lowerarm_" + side), joint("hand_" + side)
    L1, L2 = (el - sh).length, (wr - el).length
    mine = [v for v in _sleeve if (v.co.x > 0) == (sh.x > 0)]

    def along(co):
        """(t in metres from the shoulder along the arm, the nearest point on the arm's axis)."""
        best = None
        for a, b, t0, ln in ((sh, el, 0.0, L1), (el, wr, L1, L2)):
            u = max(0.0, min(1.0, (co - a).dot(b - a) / max(1e-9, ln * ln)))
            q = a + (b - a) * u
            d = (co - q).length
            if best is None or d < best[0]:
                best = (d, t0 + u * ln, q)
        return best[1], best[2]
    info = [(v,) + along(v.co) for v in mine]
    L = L1 + L2
    top = sorted((v.co - q).length for v, t, q in info if 0.15 * L < t < 0.3 * L)
    cuff = sorted((v.co - q).length for v, t, q in info if t > 0.85 * L)
    if not top or not cuff:
        continue
    r_top, r_cuff = top[int(len(top) * 0.8)], max(0.065, cuff[int(len(cuff) * 0.8)])
    for v, t, q in info:
        w = max(0.0, min(1.0, (t - 0.1 * L) / (0.15 * L)))
        w = w * w * (3 - 2 * w)
        if w <= 0.0:
            continue
        d = v.co - q
        if d.length < 1e-6:
            continue
        want = r_top + (r_cuff - r_top) * min(1.0, t / L)
        v.co = q + d.normalized() * (d.length + (want - d.length) * w)
        SLEEVED += 1
clearance(_sleeve, 0.012)
# THE JOIN, blended: pushed 3.5 cm off the body on one side and 1.2 cm on
# the other, the cloth was torn open where the back meets the sleeves (the
# second blind review, 29 September). The points within three edges of the
# join are smoothed together, then both kept clear again.
_tset, _sset = set(_torso), set(_sleeve)
band = {v for v in _tset if any(e.other_vert(v) in _sset for e in v.link_edges)}
band |= {v for v in _sset if any(e.other_vert(v) in _tset for e in v.link_edges)}
for _ in range(3):
    band |= {e.other_vert(v) for v in list(band) for e in v.link_edges if e.other_vert(v).co.z < NECK_CUT - 0.03}
band = [v for v in band if not v.is_boundary]
for _ in range(8):
    bmesh.ops.smooth_vert(_cb, verts=band, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
_cb.normal_update()
clearance(_torso, JUMPER_CLEAR)
clearance(_sleeve, 0.012)
_cb.normal_update()
_cb.to_mesh(sim.data)
_cb.free()

# ---------------------------------------------------------------- the render mesh
render = sim.copy()
render.data = sim.data.copy()
render.name = NAME
bpy.context.collection.objects.link(render)
sub = render.modifiers.new("Subdivision", "SUBSURF")
sub.levels = sub.render_levels = 1
bpy.context.view_layer.objects.active = render
bpy.ops.object.modifier_apply(modifier=sub.name)
# THE FRONT OPENING: a donkey jacket buttons down the front, the wearer's left
# front over the right, so the edge of the overlapping front runs a few
# centimetres to one side of the buttons. Made as a 5 mm groove pressed 5 mm
# in, from below the collar to the hem, so its shadow reads as the opening (the
# first jacket had buttons on a front with no opening; a slit cut right through
# showed the jumper beneath, which a buttoned overlap never does, 28 September).
SLIT_X, SLIT_W = -0.03, 0.005
_sbm = bmesh.new()
_sbm.from_mesh(render.data)
for x in (SLIT_X - SLIT_W / 2, SLIT_X, SLIT_X + SLIT_W / 2):
    bmesh.ops.bisect_plane(_sbm, geom=list(_sbm.verts) + list(_sbm.edges) + list(_sbm.faces), plane_co=(x, 0.0, 0.0), plane_no=(1.0, 0.0, 0.0))
_slit = [f for f in _sbm.faces if abs(f.calc_center_median().x - SLIT_X) < SLIT_W / 2
         and f.calc_center_median().y < pelvis.y and f.calc_center_median().z < NECK_CUT - 0.02]
for v in {v for f in _slit for v in f.verts}:
    if abs(v.co.x - SLIT_X) < 1e-4:          # the groove's floor, down its middle
        v.co.y += 0.005                      # towards the body (it faces -Y)
_sbm.to_mesh(render.data)
_sbm.free()
thick = render.modifiers.new("Solidify", "SOLIDIFY")
thick.thickness = 0.006
thick.offset = 1.0
bpy.ops.object.modifier_apply(modifier=thick.name)


def material(name, rgba, rough=0.9):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = rgba
    b.inputs["Roughness"].default_value = rough
    m.diffuse_color = rgba
    return m


wool, yoke = material("M_DonkeyWool", NAVY), material("M_DonkeyYoke", YOKE, 0.3)
render.data.materials.append(wool)
render.data.materials.append(yoke)
# THE YOKE: the panel across the shoulders, front and back, down to a little
# above the armpits behind and about a hand's width below the collar in front.
# The back's depth from the references: to about the armpits, 28 to 32 cm
# below the collar seam (ARMPIT + 0.02 gave a shallow band under the collar, 29 September).
YOKE_BACK, YOKE_FRONT = NECK_CUT - 0.30, NECK_CUT - 0.11
# A CLEAN EDGE: the mesh is cut along both lines first, so the panel's edge
# follows them instead of the triangles' zig-zag (ragged in the game, 28 September).
YOKE_X = abs(upperarm_l.x) + 0.05
_ybm = bmesh.new()
_ybm.from_mesh(render.data)
for z in (YOKE_FRONT, YOKE_BACK):
    bmesh.ops.bisect_plane(_ybm, geom=list(_ybm.verts) + list(_ybm.edges) + list(_ybm.faces), plane_co=(0.0, 0.0, z), plane_no=(0.0, 0.0, 1.0))
# and straight across the top of each shoulder, where the yoke meets the
# sleeve (its ends were torn saw edges, the blind reviewer, 29 September)
for x in (-YOKE_X, YOKE_X):
    bmesh.ops.bisect_plane(_ybm, geom=list(_ybm.verts) + list(_ybm.edges) + list(_ybm.faces), plane_co=(x, 0.0, 0.0), plane_no=(1.0, 0.0, 0.0))
_ybm.to_mesh(render.data)
_ybm.free()
for poly in render.data.polygons:
    c = poly.center
    line = YOKE_FRONT if c.y < pelvis.y else YOKE_BACK
    if c.z > line and abs(c.x) < YOKE_X:
        poly.material_index = 1

# THE COLLAR, made as its own clean band round the neck (extruded from the
# shell's uneven neckline it came out blocky, fourth try): a 3.5 cm stand,
# turned over into a broad fall that lies out on the yoke and comes to a point
# either side of the front opening, as the references' stiff pointed collar
# does (the first fall, 6 cm and square, read as two small tabs, 28 September).
# The fall is laid on the jacket: any point of it inside the cloth or closer
# than 8 mm is put 8 mm out from it.
def collar():
    from mathutils.bvhtree import BVHTree
    cm = bmesh.new()
    # a 3.5 cm stand, then a fall that drops close round the neck onto the
    # yoke rather than out over the shoulders (the wider fall lay like a
    # sailor's collar or a cape, the second blind review, 29 September)
    rings = [(-0.012, 0.016), (0.022, 0.018), (0.036, 0.028), (0.02, 0.042), (-0.008, 0.05), (-0.035, 0.056)]
    n, gap = 48, math.radians(28)       # the front opening either side of straight ahead (-Y)
    angles = [(-math.pi / 2) + gap + (2 * math.pi - 2 * gap) * k / (n - 1) for k in range(n)]
    span = 2 * math.pi - 2 * gap
    _sb = bmesh.new()
    _sb.from_mesh(sim.data)
    cloth_bvh = BVHTree.FromBMesh(_sb)
    grid = []
    for i, (dz, dr) in enumerate(rings):
        row = []
        for k, a in enumerate(angles):
            # the points: towards either end of the fall, the last two rings
            # run further down and out
            end = min(k, n - 1 - k) / (n - 1) * span
            e = max(0.0, 1.0 - end / math.radians(50)) if i >= len(rings) - 2 else 0.0
            # the points run down onto the upper chest and in towards the buttons
            a = a + (-math.pi / 2 - a) * (0.35 if i == len(rings) - 1 else 0.2) * e
            r = NECK_R + dr + 0.012 * e
            co = Vector((neck.x + math.cos(a) * r * 1.12, neck.y + math.sin(a) * r, NECK_CUT + dz - 0.075 * e ** 1.5))
            if i >= 3:
                hit = cloth_bvh.find_nearest(co)
                if hit[0] is not None:
                    loc, nrm, _f, dist = hit
                    if nrm.dot(co - loc) < 0.012:
                        co = loc + nrm * 0.012
            row.append(cm.verts.new(co))
        grid.append(row)
    _sb.free()
    for i in range(len(grid) - 1):
        for k in range(n - 1):
            cm.faces.new((grid[i][k], grid[i][k + 1], grid[i + 1][k + 1], grid[i + 1][k]))
    me = bpy.data.meshes.new("Collar")
    cm.to_mesh(me)
    cm.free()
    # A PIECE OF ITS OWN, fixed to his upper back in the game (LedgerJacket.h):
    # stiff melton barely moves. As part of the cloth's render mesh with no
    # cloth beneath it, it flew out in spikes (28 September); as a second
    # simulated layer 12 mm over the yoke, the collar's points and the yoke's
    # were drawn to the wrong layer, a torn collar and a blotchy yoke (29
    # September). It is written as NAME_collar_static.fbx.
    o = bpy.data.objects.new("Collar", me)
    bpy.context.collection.objects.link(o)
    so = o.modifiers.new("Solidify", "SOLIDIFY")
    so.thickness = 0.006
    sb = o.modifiers.new("Subdivision", "SUBSURF")
    sb.levels = sb.render_levels = 1
    bpy.context.view_layer.objects.active = o
    for m in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=m.name)
    o.data.materials.append(wool)
    return o


# BUTTONS AND POCKETS, as small solid pieces joined to the render mesh.
def front_point(x, z):
    """The most forward point of the settled jacket near (x, z) (the body faces -Y)."""
    near = [v.co for v in sim.data.vertices if abs(v.co.x - x) < 0.02 and abs(v.co.z - z) < 0.02]
    return min(near, key=lambda c: c.y) if near else None


COLLAR = collar()
extras = []
btn_mat = material("M_DonkeyButton", BUTTON, 0.35)
# FIVE BUTTONS TO THE NECK, evenly spaced, as the references have them (four
# to five, about 16 cm apart; four starting below the yoke looked stopped
# short and uneven, the blind reviewer, 29 September).
top_btn = NECK_CUT - 0.05
BTN_STEP = min(0.17, (top_btn - (HEM + 0.10)) / 4)
for k in range(5):
    z = top_btn - BTN_STEP * k
    p = front_point(0.0, z)
    if p is None:
        continue
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.012, depth=0.006, location=(p.x, p.y - 0.006, p.z), rotation=(math.pi / 2, 0, 0))
    b = bpy.context.active_object
    b.data.materials.append(btn_mat)
    extras.append(b)
# PATCH POCKETS: the render mesh's own faces in a hand-sized patch low on
# each front, copied and stood 3 mm off, so they lie on the cloth.
pocket_faces = []
for side in (-1, 1):
    # the pocket's foot about 8 cm above the hem, clear of the front opening
    cx, cz = side * 0.12, HEM + 0.165
    # STRAIGHT EDGES: the mesh is cut along the pocket's four sides first, so
    # the patch is a clean rectangle (by triangle centres its top was a saw
    # edge in the game, 28 September).
    _pb = bmesh.new()
    _pb.from_mesh(render.data)
    for co, no in (((cx - 0.075, 0, 0), (1, 0, 0)), ((cx + 0.075, 0, 0), (1, 0, 0)), ((0, 0, cz - 0.085), (0, 0, 1)), ((0, 0, cz + 0.085), (0, 0, 1))):
        # only near the pocket, on the front: cut right across, the lines
        # showed round the whole jacket in the game
        near = [f for f in _pb.faces if abs(f.calc_center_median().x - cx) < 0.11 and abs(f.calc_center_median().z - cz) < 0.12
                and f.calc_center_median().y < pelvis.y and f.normal.y < 0]
        vs = {v for f in near for v in f.verts}
        es = {e for f in near for e in f.edges}
        bmesh.ops.bisect_plane(_pb, geom=list(vs) + list(es) + near, plane_co=co, plane_no=no)
    _pb.to_mesh(render.data)
    _pb.free()
    for poly in render.data.polygons:
        c = poly.center
        if abs(c.x - cx) < 0.075 and abs(c.z - cz) < 0.085 and c.y < pelvis.y and poly.normal.y < -0.3:
            pocket_faces.append(poly.index)
if pocket_faces:
    # EACH POCKET A SOLID PATCH: the pocket's faces copied out as their own
    # piece, 1 mm off the cloth and 4 mm thick, so its edge is a closed rim
    # that catches the light (a single layer did not show at all; a lip turned
    # back from it rendered as black slots, the blind reviewer, 29 September).
    pbm = bmesh.new()
    pbm.from_mesh(render.data)
    pbm.faces.ensure_lookup_table()
    keep = set(pocket_faces)
    bmesh.ops.delete(pbm, geom=[f for f in pbm.faces if f.index not in keep], context="FACES")
    bmesh.ops.delete(pbm, geom=[v for v in pbm.verts if not v.link_faces], context="VERTS")
    for v in pbm.verts:
        v.co += Vector((0.0, -0.001, 0.0))
    pme = bpy.data.meshes.new("Pockets")
    pbm.to_mesh(pme)
    pbm.free()
    pockets = bpy.data.objects.new("Pockets", pme)
    bpy.context.collection.objects.link(pockets)
    pso = pockets.modifiers.new("Solidify", "SOLIDIFY")
    pso.thickness = 0.004
    pso.offset = 1.0
    bpy.context.view_layer.objects.active = pockets
    bpy.ops.object.modifier_apply(modifier=pso.name)
    pockets.data.materials.append(wool)
    extras.append(pockets)
bpy.ops.object.select_all(action="DESELECT")
for o in extras + [render]:
    o.select_set(True)
bpy.context.view_layer.objects.active = render
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.join()


# ---------------------------------------------------------------- plain meshes for Unreal's cloth
# Epic's cloth template (DF_StaticMeshClothTemplate) takes a render and a
# simulation mesh as plain static meshes in the body's rest pose, and copies
# the skin weights from the body itself (its TransferSkinWeights node); so
# both are written here as they are, before any weights, in the body's
# world space: NAME_render_static.fbx and NAME_sim_static.fbx.
for obj, tag in ((render, "render"), (sim, "sim"), (COLLAR, "collar")):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, "%s_%s_static.fbx" % (NAME, tag)), use_selection=True,
                             object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)

# ---------------------------------------------------------------- the weights
# body_world is the body in world metres with its own weights; each target
# takes the weights of the nearest point of the body's surface.
for target in (render, sim):
    dt = target.modifiers.new("Weights", "DATA_TRANSFER")
    dt.object = body_world
    dt.use_vert_data = True
    dt.data_types_verts = {"VGROUP_WEIGHTS"}
    dt.vert_mapping = "POLYINTERP_NEAREST"
    dt.layers_vgroup_select_src = "ALL"
    dt.layers_vgroup_select_dst = "NAME"
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.datalayout_transfer(modifier="Weights")
    bpy.ops.object.modifier_apply(modifier="Weights")
    target.parent = arm
    target.matrix_parent_inverse = arm.matrix_world.inverted()   # stays where it is: the armature is imported turned and scaled
    am = target.modifiers.new("Armature", "ARMATURE")
    am.object = arm
covered = sum(1 for v in render.data.vertices if v.groups) / max(1, len(render.data.vertices))

# ---------------------------------------------------------------- the pictures
grey = material("M_Body", (0.5, 0.5, 0.5, 1.0))
body_world.data.materials.clear()
body_world.data.materials.append(grey)
body.hide_render = True
if source is not body:
    source.hide_render = True
sim.hide_render = True
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_specular_highlight = False   # the check picture shows shape; the shine read as leather
scene.render.resolution_x, scene.render.resolution_y = 900, 1200
cam_data = bpy.data.cameras.new("Cam")
cam_data.lens = 70
cam = bpy.data.objects.new("Cam", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam
mid = Vector((0.0, pelvis.y, (HEM + neck.z) / 2))
for tag, off in (("front", Vector((0.0, -3.2, 0.1))), ("side", Vector((3.2, 0.0, 0.1))), ("back", Vector((0.0, 3.2, 0.1)))):
    cam.location = mid + off
    cam.rotation_euler = (mid - cam.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(OUT, "%s_%s.png" % (NAME, tag))
    bpy.ops.render.render(write_still=True)

# ---------------------------------------------------------------- out
bpy.ops.object.select_all(action="DESELECT")
for o in (render, sim, arm):
    o.hide_render = False
    o.select_set(True)
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + ".fbx"), use_selection=True, add_leaf_bones=False,
                         mesh_smooth_type="FACE", object_types={"ARMATURE", "MESH"})
report = {
    "body": BODY, "offset": OFFSET, "frames": FRAMES, "sourceLod": SOURCE_LOD,
    "sim": {"verts": len(sim.data.vertices), "tris": sum(len(p.vertices) - 2 for p in sim.data.polygons)},
    "render": {"verts": len(render.data.vertices)},
    "hem": round(HEM, 3), "neck": round(NECK_CUT, 3), "neckRadius": round(NECK_R, 3),
    "settling": {"largestFallM": round(drop_max, 3), "lastFrameMoveM": round(last_move, 4)}, "chestFilled": FILLED, "reclearedToJumper": RECLEARED, "sleevePointsTubed": SLEEVED, "clearedToStandoff": CLEARED,
    "weightsCoverage": round(covered, 3),
}
json.dump(report, open(os.path.join(OUT, NAME + ".json"), "w"), indent=1)
print("DRAPE", json.dumps(report))
