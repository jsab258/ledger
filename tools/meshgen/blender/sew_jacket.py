"""Sew and drape a jacket cut from FreeSewing's Brian block round a MetaHuman body, in Blender.

    blender -b -P tools/meshgen/blender/sew_jacket.py -- BRIAN.json BODY.fbx OUT_DIR [frames]

WHY, 29 September (Jafar's list, item 5; production/research/clothing-
pipeline/pattern-jacket-2026-09-29.md): the jacket made by reshaping a shell
of the body's own skin failed three blind reviews, and a real jacket is cut
from a pattern. The pattern is Brian drafted to Ron's measurements
(tools/meshgen/freesewing_draft.mjs; production/art/clothing/
donkey-jacket-pattern). The pieces: the back, one piece across its fold; two
fronts, sewn to each other down the centre for now (the overlapping front
edge is added to the render mesh); two sleeves. Each is cut from the
pattern's own seam lines with the same number of points along both sides of
every seam (the cap's method, sew_cap.py), filled with even triangles, placed
round the body loosely (the body pieces on an elliptical cylinder a few
centimetres out from the torso, the sleeves on cylinders along the arms in
the body's rest pose) and sewn shut by Blender's sewing springs, weightless,
then draped under gravity.

THE FIRST FRAME IS THE PATTERN'S OWN SHAPE (the research: the cap was lumpy
because Blender takes the cloth's first frame as its natural shape, and the
cap's first frame was stretched): each piece is rolled onto a cylinder whose
girth is the piece's own width, which a flat piece takes without stretching,
so the lengths the cloth remembers are the pattern's. (A rest shape key with
the pass-through workaround started the cloth from the flat layout itself,
every seam a metre and more open, 29 September.) The flat pattern is kept as
the UV map.

Writes jacket.blend, jacket_render_static.fbx and jacket_sim_static.fbx (the
body's frame, metres), four pictures, and jacket.json (seam gaps by frame,
clearance from the body, the hem's width against the chest's).
"""
import json
import math
import os
import sys
import time

import bmesh
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import delaunay_2d_cdt

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, BODY, OUT = argv[0], argv[1], argv[2]
FRAMES = int(argv[3]) if len(argv) > 3 and not argv[3].startswith("--") else 120
# --body: the body alone, the back and fronts sewn and draped without sleeves
# (the first stage: the sleeves go on the settled armholes after)
BODY_ONLY = "--body" in argv
# --from SETTLED.npy: the body stage's settled points; the body starts there and
# each sleeve starts with its top on the settled armhole (the second stage)
FROM = argv[argv.index("--from") + 1] if "--from" in argv else None
# --pose DEG: the whole jacket sewn and draped with the arms raised to DEG
# below the horizontal, then the arms lowered to the rest pose over RETURN
# frames with the cloth carried on them (29 September: in the rest pose the
# arms, 45 degrees down, close the armpits and the sleeves cannot form)
POSE = float(argv[argv.index("--pose") + 1]) if "--pose" in argv else None
RETURN = 60
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
EDGE = 10.0                       # cloth triangle edge, mm (the research: drape at about 10 mm)
CLEAR_TORSO = 0.045               # the body pieces start this far out from the torso, metres
CLEAR_ARM = 0.04
LIFT = 0.12                       # the body pieces start this far above where they hang, so the shoulders close over him
if "--lift" in argv:
    LIFT = float(argv[argv.index("--lift") + 1])
Y_BEND, R_BEND = 150.0, 0.06      # above this far down the pattern (mm) each body piece bends in over the shoulder, round this radius (m)

pattern = json.load(open(SRC, encoding="utf-8"))


# ---- the pattern's lines (sew_cap.py's helpers, the same method) --------------

def closed(pts):
    pts = [tuple(p) for p in pts]
    return pts[:-1] if pts[0] == pts[-1] else pts


def near(poly, p):
    d = [(q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 for q in poly]
    return d.index(min(d))


def walk(poly, a, b):
    i, j, n = near(poly, a), near(poly, b), len(poly)
    out = [poly[i]]
    while i != j:
        i = (i + 1) % n
        out.append(poly[i])
    return out


def length(poly):
    return sum(math.dist(poly[k], poly[k - 1]) for k in range(1, len(poly)))


def resample(poly, n):
    cum = [0.0]
    for k in range(1, len(poly)):
        cum.append(cum[-1] + math.dist(poly[k], poly[k - 1]))
    out = []
    for s in np.linspace(0, cum[-1], n + 1):
        k = max(1, min(len(poly) - 1, int(np.searchsorted(cum, s))))
        t = 0.0 if cum[k] == cum[k - 1] else (s - cum[k - 1]) / (cum[k] - cum[k - 1])
        a, b = poly[k - 1], poly[k]
        out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out


def split_at(poly, s):
    run = 0.0
    for k in range(1, len(poly)):
        d = math.dist(poly[k], poly[k - 1])
        if run + d >= s:
            t = (s - run) / d
            a, b = poly[k - 1], poly[k]
            m = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            return poly[:k] + [m], [m] + poly[k:]
        run += d
    return poly, [poly[-1]]


def steps(*polys):
    return max(2, round(sum(length(p) for p in polys) / len(polys) / EDGE))


def loop(segments):
    pts, idx = [], {}
    for name, poly, n in segments:
        r = resample(poly, n)
        start = len(pts)
        pts.extend(r[:-1])
        idx[name] = list(range(start, start + n)) + [None]
    total = len(pts)
    for name in idx:
        s = idx[name]
        s[-1] = (s[-2] + 1) % total
    return pts, idx


def inside(poly, xy):
    poly = np.asarray(poly)
    x, y = xy[:, 0][:, None], xy[:, 1][:, None]
    x1, y1 = poly[:, 0][None], poly[:, 1][None]
    x2, y2 = np.roll(poly[:, 0], -1)[None], np.roll(poly[:, 1], -1)[None]
    cross = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1)
    return cross.sum(axis=1) % 2 == 1


def clearance2d(poly, xy):
    a = np.asarray(poly)
    b = np.roll(a, -1, axis=0)
    ab = b - a
    t = np.clip(((xy[:, None] - a[None]) * ab[None]).sum(-1) / ((ab * ab).sum(-1)[None] + 1e-12), 0, 1)
    proj = a[None] + t[..., None] * ab[None]
    return np.sqrt(((xy[:, None] - proj) ** 2).sum(-1)).min(axis=1)


def panel(boundary):
    b = np.asarray(boundary)
    lo, hi = b.min(axis=0), b.max(axis=0)
    rows = np.arange(lo[1], hi[1] + EDGE, EDGE * math.sqrt(3) / 2)
    grid = []
    for r, y in enumerate(rows):
        xs = np.arange(lo[0] + (EDGE / 2 if r % 2 else 0), hi[0] + EDGE, EDGE)
        grid.extend((x, y) for x in xs)
    grid = np.asarray(grid)
    grid = grid[inside(boundary, grid)]
    grid = grid[clearance2d(boundary, grid) > EDGE * 0.55]
    verts = [Vector(p) for p in boundary] + [Vector(p) for p in grid]
    nb = len(boundary)
    edges = [(k, (k + 1) % nb) for k in range(nb)]
    out_v, _e, out_f, orig_v, _oe, _of = delaunay_2d_cdt(verts, edges, [list(range(nb))], 1, 1e-6, True)
    remap, flat = {}, [tuple(v) for v in verts]
    for k, ov in enumerate(orig_v):
        if ov:
            remap[k] = ov[0]
        else:
            remap[k] = len(flat)
            flat.append(tuple(out_v[k]))
    return flat, [[remap[k] for k in f] for f in out_f]


# ---- the pieces, as drafted (mm, y down) ---------------------------------------

back, front, sleeve = (pattern["parts"][k] for k in ("brian.back", "brian.front", "library.sleeve"))
bp, fp, sp = back["points"], front["points"], sleeve["points"]
back_out = closed(back["paths"]["seam"]["points"])
front_out = closed(front["paths"]["seam"]["points"])
sleeve_out = closed(sleeve["paths"]["seam"]["points"])


def seg(poly, a, b):
    """The outline from a to b, the shorter way round by length (not by points: a curve is sampled densely,
    and by points the armhole ran the long way round the straight edges, 2 m of it)."""
    fwd = walk(poly, a, b)
    bwd = list(reversed(walk(poly, b, a)))
    return fwd if length(fwd) <= length(bwd) else bwd


B = {n: seg(back_out, *ab) for n, ab in {
    "fold": (bp["cbNeck"], bp["cbHem"]), "hem": (bp["cbHem"], bp["hem"]), "side": (bp["hem"], bp["armhole"]),
    "armhole": (bp["armhole"], bp["shoulder"]), "shoulder": (bp["shoulder"], bp["neck"]), "neckline": (bp["neck"], bp["cbNeck"])}.items()}
F = {n: seg(front_out, *ab) for n, ab in {
    "cf": (fp["cfNeck"], fp["cfHem"]), "hem": (fp["cfHem"], fp["hem"]), "side": (fp["hem"], fp["armhole"]),
    "armhole": (fp["armhole"], fp["shoulder"]), "shoulder": (fp["shoulder"], fp["neck"]), "neckline": (fp["neck"], fp["cfNeck"])}.items()}
# the sleeve: its cap runs from the back (bicepsLeft) over the top to the front
cap_poly = seg(sleeve_out, sp["bicepsLeft"], sp["bicepsRight"])
if min(y for _, y in cap_poly) > -10:           # took the wrist way round: the cap is the other way
    cap_poly = list(reversed(seg(sleeve_out, sp["bicepsRight"], sp["bicepsLeft"])))
cap_back, cap_front = split_at(cap_poly, length(B["armhole"]) / (length(B["armhole"]) + length(F["armhole"])) * length(cap_poly))
S = {"capBack": cap_back, "capFront": list(reversed(cap_front)),   # both from the underarm up to the shoulder
     "right": seg(sleeve_out, sp["bicepsRight"], sp["wristRight"]), "cuff": seg(sleeve_out, sp["wristRight"], sp["wristLeft"]),
     "left": seg(sleeve_out, sp["wristLeft"], sp["bicepsLeft"])}

N = {"side": steps(B["side"], F["side"]), "shoulder": steps(B["shoulder"], F["shoulder"]),
     "armB": steps(B["armhole"], S["capBack"]), "armF": steps(F["armhole"], S["capFront"]),
     "under": steps(S["right"], S["left"]), "cf": steps(F["cf"])}
for k in ("fold", "hem", "neckline"):
    N["b" + k] = steps(B[k])
for k in ("hem", "neckline"):
    N["f" + k] = steps(F[k])
N["cuff"] = steps(S["cuff"])

pieces = {}
bb, b_idx = loop([("fold", B["fold"], N["bfold"]), ("hem", B["hem"], N["bhem"]), ("side", B["side"], N["side"]),
                  ("armhole", B["armhole"], N["armB"]), ("shoulder", B["shoulder"], N["shoulder"]),
                  ("neckline", B["neckline"], N["bneckline"])])
pieces["back"] = dict(zip(("flat", "faces"), panel(bb)), idx=b_idx)
fb, f_idx = loop([("cf", F["cf"], N["cf"]), ("hem", F["hem"], N["fhem"]), ("side", F["side"], N["side"]),
                  ("armhole", F["armhole"], N["armF"]), ("shoulder", F["shoulder"], N["shoulder"]),
                  ("neckline", F["neckline"], N["fneckline"])])
pieces["front"] = dict(zip(("flat", "faces"), panel(fb)), idx=f_idx)
cap_whole = S["capBack"] + list(reversed(S["capFront"]))[1:]
sb_, s_idx = loop([("capBack", S["capBack"], N["armB"]), ("capFront", list(reversed(S["capFront"])), N["armF"]),
                   ("right", S["right"], N["under"]), ("cuff", S["cuff"], N["cuff"]), ("left", S["left"], N["under"])])
if not BODY_ONLY:
    pieces["sleeve"] = dict(zip(("flat", "faces"), panel(sb_)), idx=s_idx)


# ---- the body ---------------------------------------------------------------

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY)
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
meshes = sorted([o for o in bpy.context.scene.objects if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
body_src = meshes[0]
for o in meshes[1:]:
    bpy.data.objects.remove(o, do_unlink=True)


def joint(name):
    if POSE is not None:
        return arm.matrix_world @ arm.pose.bones[name].head
    return arm.matrix_world @ arm.data.bones[name].head_local


# THE ARMS RAISED (--pose): each upper arm turned about the axis square to it
# and to the vertical, at its own joint, until the elbow is DEG below the
# shoulder's horizontal; the forearm and hand follow as its children.
REST_ROT = {}
if POSE is not None:
    bpy.context.view_layer.objects.active = arm
    for side in ("l", "r"):
        pb = arm.pose.bones["upperarm_" + side]
        REST_ROT[side] = pb.rotation_quaternion.copy() if pb.rotation_mode == "QUATERNION" else pb.rotation_euler.copy()
        bpy.context.view_layer.update()
        sh_w = arm.matrix_world @ pb.head
        el_w = arm.matrix_world @ arm.pose.bones["lowerarm_" + side].head
        d = (el_w - sh_w).normalized()
        now = math.degrees(math.asin(max(-1.0, min(1.0, -d.z))))       # degrees below horizontal
        ax = d.cross(Vector((0, 0, 1))).normalized()
        from mathutils import Matrix
        Rw = Matrix.Rotation(math.radians(POSE - now) * -1.0, 4, ax)     # turns d up by (now - POSE)
        test = (Rw.to_3x3() @ d)
        if test.z < d.z:                                                  # the axis's sign: the elbow must rise
            Rw = Matrix.Rotation(math.radians(now - POSE) * -1.0, 4, ax)
        M = arm.matrix_world
        Ra = (M.inverted() @ Rw @ M).to_3x3().to_4x4()
        head_a = pb.head.copy()
        T = Matrix.Translation(head_a) @ Ra @ Matrix.Translation(-head_a)
        pb.matrix = T @ pb.matrix
        bpy.context.view_layer.update()
        el2 = arm.matrix_world @ arm.pose.bones["lowerarm_" + side].head
        d2 = (el2 - sh_w).normalized()
        print("POSE arm %s: %.1f degrees below horizontal, now %.1f" % (side, now, math.degrees(math.asin(-d2.z))), flush=True)
    dg = bpy.context.evaluated_depsgraph_get()
    body_me = bpy.data.meshes.new_from_object(body_src.evaluated_get(dg))
else:
    body_me = body_src.data.copy()
body_me.transform(body_src.matrix_world)
body = bpy.data.objects.new("Body", body_me)
bpy.context.collection.objects.link(body)
body_src.hide_render = True
body_src.hide_set(True)
_bmb = bmesh.new()
_bmb.from_mesh(body_me)
BVH = BVHTree.FromBMesh(_bmb)
names = {g.index: g.name for g in body_src.vertex_groups}
ARMISH = ("upperarm", "lowerarm", "hand", "thumb", "index", "middle", "ring", "pinky", "wrist", "elbow", "clavicle")
torso_pts = []
for v in body_me.vertices:
    best, w = "", 0.0
    for g in v.groups:
        if g.weight > w:
            best, w = names.get(g.group, ""), g.weight
    if not best.startswith(ARMISH):
        torso_pts.append(v.co.copy())
# THE BODY STAGE COLLIDES WITH THE TORSO ALONE: a cylinder of the pattern's
# girth passes through the arms of the rest pose, which hang out at 45
# degrees, and the arms shoved the side seams apart (29 September). The
# shoulders (the clavicles' points) stay; the arms come back for the sleeves.
if BODY_ONLY:
    _bt = bmesh.new()
    _bt.from_mesh(body_me)
    _dl = _bt.verts.layers.deform.active
    _arms = []
    for v in _bt.verts:
        best, w = "", 0.0
        for gi, wt in (v[_dl].items() if _dl is not None else []):
            if wt > w:
                best, w = names.get(gi, ""), wt
        if best.startswith(ARMISH) and not best.startswith("clavicle"):
            _arms.append(v)
    bmesh.ops.delete(_bt, geom=_arms, context="VERTS")
    _bt.to_mesh(body_me)
    _bt.free()

up_l, up_r = joint("upperarm_l"), joint("upperarm_r")
low_l, low_r, hand_l, hand_r = joint("lowerarm_l"), joint("lowerarm_r"), joint("hand_l"), joint("hand_r")
neck = joint("neck_01")
top_z = max(v.co.z for v in body_me.vertices)
# the HPS height: where the pattern's top (y = 0) hangs
HPS_Z = top_z - 0.012
chest_z = up_l.z - 0.09
chest_sl = [p for p in torso_pts if abs(p.z - chest_z) < 0.01 and abs(p.x) < abs(up_l.x)]
CX = sum(p.x for p in chest_sl) / len(chest_sl)
CY = (max(p.y for p in chest_sl) + min(p.y for p in chest_sl)) / 2
HALF_W = (max(p.x for p in chest_sl) - min(p.x for p in chest_sl)) / 2 + CLEAR_TORSO
HALF_D = (max(p.y for p in chest_sl) - min(p.y for p in chest_sl)) / 2 + CLEAR_TORSO


# the ellipse the body pieces are wrapped round, parameterised by arc length
# from the back centre (+Y), running towards the wearer's left (+X) and round
ANG = np.linspace(0, 2 * math.pi, 4001)
TOTAL = (length(B["hem"]) * 2 + length(F["hem"]) * 2) / 1000.0      # the pieces' own girth at the hem


def perimeter(a, b):
    xs, ys = a * np.sin(ANG), b * np.cos(ANG)
    return float(np.hypot(np.diff(xs), np.diff(ys)).sum())


# the ellipse keeps the torso's proportions and takes the pieces' own girth,
# so rolling them onto it stretches nothing
SCALE = TOTAL / perimeter(HALF_W, HALF_D)
HALF_W, HALF_D = HALF_W * SCALE, HALF_D * SCALE
EX, EY = HALF_W * np.sin(ANG) + CX, HALF_D * np.cos(ANG) + CY
ARC = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(EX), np.diff(EY)))])
PERIM = ARC[-1]


def on_ellipse(s):
    """A point s metres along the ellipse from the back centre, scaled so the pieces' girth fits."""
    s = s % PERIM
    a = np.interp(s, ARC, ANG)
    return HALF_W * math.sin(a) + CX, HALF_D * math.cos(a) + CY


def normal_at(s):
    s = s % PERIM
    a = np.interp(s, ARC, ANG)
    n = Vector((math.sin(a) / HALF_W, math.cos(a) / HALF_D, 0.0))
    return n.normalized()


def place_body_piece(flat, start_s, direction):
    """A body piece round the ellipse: its x (mm from its centre line) runs round from start_s, its y down.
    Below Y_BEND it hangs straight; above, it bends in over the shoulder round R_BEND and runs inward,
    so front and back shoulders start close (lengths down the piece are kept; the shoulder line is a
    little gathered round, which the sewing and the cloth let out)."""
    out = []
    z_bend = HPS_Z + LIFT - Y_BEND / 1000.0
    for x, y in flat:
        s_ = start_s + direction * x / 1000.0
        px, py = on_ellipse(s_)
        if y >= Y_BEND:
            out.append((px, py, HPS_Z + LIFT - y / 1000.0))
            continue
        n = normal_at(s_)
        d = (Y_BEND - y) / 1000.0
        phi = d / R_BEND
        if phi <= math.pi / 2:
            inward, up = R_BEND * (1 - math.cos(phi)), R_BEND * math.sin(phi)
        else:
            inward, up = R_BEND + (d - R_BEND * math.pi / 2), R_BEND
        out.append((px - n.x * inward, py - n.y * inward, z_bend + up))
    return out


def place_sleeve(flat, side):
    """A sleeve round a cylinder along the arm (rest pose): its y runs down the arm from the biceps line, its x round it."""
    sh, el, wr = (up_l, low_l, hand_l) if side > 0 else (up_r, low_r, hand_r)
    axis = (wr - sh).normalized()
    up = Vector((0, 0, 1))
    across = axis.cross(up).normalized()             # horizontal, square to the arm
    over = across.cross(axis).normalized()           # the top of the arm
    bic = sh + axis * 0.13 + Vector((0, 0, LIFT if POSE is None else 0.0))   # the biceps line, 13 cm down the arm, clear of the armpit
    width_top = 2 * sp["bicepsRight"][0]
    width_cuff = 2 * sp["wristRight"][0]
    out = []
    for x, y in flat:
        t = max(0.0, min(1.0, y / sp["centerWrist"][1]))
        w = width_top + (width_cuff - width_top) * t
        # THE PATTERN'S OWN GIRTH, as the body pieces' ellipse: a radius of
        # w / 2 pi rolls the flat piece without stretching it; the ease is the
        # pattern's (bicepsEase), and 4 cm more stretched the first frame by
        # half again, which the cloth then kept (29 September)
        r = w / (2 * math.pi) / 1000.0 + (CLEAR_ARM if POSE is None else 0.0)
        th = math.pi * x / (w / 2)                   # 0 on top of the arm, +-pi underneath
        # the front of the arm towards -Y: turn so that +x runs forward
        pos = bic + axis * (y / 1000.0) + (over * math.cos(th) + across * math.sin(th) * side) * r
        out.append(tuple(pos))
    return out


QUARTER = TOTAL / 4
place = {
    ("back", 1): place_body_piece(pieces["back"]["flat"], 0.0, 1),          # the wearer's left half of the back
    ("back", -1): None,
    ("front", 1): place_body_piece(pieces["front"]["flat"], 2 * QUARTER, -1),  # left front: from the front centre back towards the left side
    ("front", -1): None,
}
if not BODY_ONLY:
    place[("sleeve", 1)] = place_sleeve(pieces["sleeve"]["flat"], 1)
    place[("sleeve", -1)] = place_sleeve(pieces["sleeve"]["flat"], -1)
place[("back", -1)] = [(2 * CX - x, y, z) for x, y, z in place[("back", 1)]]
place[("front", -1)] = [(2 * CX - x, y, z) for x, y, z in place[("front", 1)]]

verts, flat_co, faces, groups, at = [], [], [], {}, {}
LAYOUT = {"back": (0.0, 0.0), "front": (0.9, 0.0), "sleeve": (1.8, 0.0)}
for name, pc in pieces.items():
    welded = set(pc["idx"]["fold"]) if name == "back" else set()
    groups[name] = []
    for side in (1, -1):
        for k, f2 in enumerate(pc["flat"]):
            if side == -1 and k in welded:
                at[(name, -1, k)] = at[(name, 1, k)]
                continue
            at[(name, side, k)] = len(verts)
            verts.append(place[(name, side)][k])
            ox, oy = LAYOUT[name]
            flat_co.append((ox * side + side * f2[0] / 1000.0, oy - f2[1] / 1000.0, 0.0))
            groups[name].append(len(verts) - 1)
        for f in pc["faces"]:
            g = [at[(name, side, k)] for k in f]
            faces.append(g if side == 1 else list(reversed(g)))

# THE SECOND STAGE'S START: the body where the first stage left it, and each
# sleeve hung from the settled armhole. The sleeve's top points sit on the
# armhole points they are sewn to, and the rest runs down the arm from there
# as a tube that narrows as the sleeve does, so the armhole seams start shut.
if FROM and not BODY_ONLY:
    settled = np.load(FROM)
    for i in range(len(settled)):
        verts[i] = tuple(settled[i])
    armhole_of = {}
    for side in (1, -1):
        for bseg, sseg, rev in (("armhole", "capBack", False), ("armhole", "capFront", True)):
            body_piece = "back" if sseg == "capBack" else "front"
            ia = pieces[body_piece]["idx"][bseg]
            ib = pieces["sleeve"]["idx"][sseg]
            if rev:
                ib = list(reversed(ib))
            for x, y in zip(ia, ib):
                armhole_of[(side, y)] = Vector(verts[at[(body_piece, side, x)]])
    flat_s = pieces["sleeve"]["flat"]
    cap_ids = sorted({k for (_, k) in armhole_of})
    width_top, width_cuff = 2 * sp["bicepsRight"][0], 2 * sp["wristRight"][0]
    for side in (1, -1):
        sh, wr = (up_l, hand_l) if side > 0 else (up_r, hand_r)
        axis = (wr - sh).normalized()
        ring = [(flat_s[k][0], flat_s[k][1], armhole_of[(side, k)]) for k in cap_ids]
        ring.sort(key=lambda r: r[0])
        centre = sum((r[2] for r in ring), Vector()) / len(ring)
        rx = [r[0] for r in ring]
        for k, (x, y) in enumerate(flat_s):
            if (side, k) in armhole_of:
                verts[at[("sleeve", side, k)]] = tuple(armhole_of[(side, k)])
                continue
            j = min(range(len(rx)), key=lambda q: abs(rx[q] - x))
            ycap, rpos = ring[j][1], ring[j][2]
            down = max(0.0, y - ycap) / 1000.0
            t = max(0.0, min(1.0, y / sp["centerWrist"][1]))
            scale = (width_top + (width_cuff - width_top) * t) / width_top
            pos = centre + axis * down + (rpos - centre) * scale
            verts[at[("sleeve", side, k)]] = tuple(pos)
    print("SECOND STAGE: the body from %s, the sleeves from the settled armholes" % FROM, flush=True)

SEAMS = {}


def seam(label, a, b, reverse=False):
    pa, sa, sega = a
    pb, sb, segb = b
    ia, ib = pieces[pa]["idx"][sega], pieces[pb]["idx"][segb]
    if reverse:
        ib = list(reversed(ib))
    assert len(ia) == len(ib), (label, len(ia), len(ib))
    pairs = [(at[(pa, sa, x)], at[(pb, sb, y)]) for x, y in zip(ia, ib)]
    SEAMS.setdefault(label, []).extend(pairs)
    return pairs


sewing = []
for s in (1, -1):
    sewing += seam("shoulder", ("back", s, "shoulder"), ("front", s, "shoulder"))
    sewing += seam("side", ("back", s, "side"), ("front", s, "side"))
    if not BODY_ONLY:
        sewing += seam("armhole back", ("back", s, "armhole"), ("sleeve", s, "capBack"))
        sewing += seam("armhole front", ("front", s, "armhole"), ("sleeve", s, "capFront"), reverse=True)
        sewing += seam("underarm", ("sleeve", s, "right"), ("sleeve", s, "left"), reverse=True)
sewing += seam("centre front", ("front", 1, "cf"), ("front", -1, "cf"))
sewing = list(dict.fromkeys(tuple(sorted(p)) for p in sewing if p[0] != p[1]))

print("BUILT %d points, %d triangles; pieces %s" % (len(verts), len(faces),
      {n: (len(pc["flat"]), len(pc["faces"])) for n, pc in pieces.items()}), flush=True)
me = bpy.data.meshes.new("jacket")
me.from_pydata(verts, sewing, faces)
me.validate()
jacket = bpy.data.objects.new("Jacket", me)
bpy.context.collection.objects.link(jacket)
for gname, ids in groups.items():
    vg = jacket.vertex_groups.new(name=gname)
    vg.add(ids, 1.0, "REPLACE")
# the flat pattern, as the UV map
uv = me.uv_layers.new(name="pattern")
for poly in me.polygons:
    for li in poly.loop_indices:
        c = flat_co[me.loops[li].vertex_index]
        uv.data[li].uv = (c[0] / 3.0 + 0.5, c[1] / 3.0 + 0.9)

# POSED, the collider is the body on its skeleton, so it moves as the arms come
# down; otherwise the still copy
collider = body_src if POSE is not None else body
if POSE is not None:
    body_src.hide_set(False)
    body_src.hide_render = False
    body.hide_render = True
    body.hide_set(True)
col = collider.modifiers.new("Collision", "COLLISION")
collider.collision.thickness_outer = 0.002
collider.collision.cloth_friction = 10.0

cl = jacket.modifiers.new("Cloth", "CLOTH")
st, cs = cl.settings, cl.collision_settings
st.quality = 16
st.mass = 0.004                   # per point, of about 20,000: 0.6 (the old jacket's, on 2,500 points) made it hundreds of kilograms, and it tore through the body
st.air_damping = 3.0
st.tension_stiffness = st.compression_stiffness = 60.0
st.shear_stiffness = 30.0
st.bending_stiffness = 15.0       # heavy wool: broad folds
st.use_sewing_springs = True
st.sewing_force_max = 10.0
cs.use_collision = True
cs.distance_min = 0.002           # the research: about 2 mm; wider rests on air and looks padded
cs.collision_quality = 4
cs.use_self_collision = False
SEWN = min(100, FRAMES - 40)
if POSE is not None:
    # sewn by SEWN, settled under gravity 40 frames, the arms brought down over
    # RETURN frames, then 30 to settle
    F0 = SEWN + 40
    FRAMES = max(FRAMES, F0 + RETURN + 30) if "--noreturn" not in argv else F0
    for side in ("l", "r"):
        pb = arm.pose.bones["upperarm_" + side]
        path = "rotation_quaternion" if pb.rotation_mode == "QUATERNION" else "rotation_euler"
        pb.keyframe_insert(path, frame=1)
        pb.keyframe_insert(path, frame=F0)
        setattr(pb, path, REST_ROT[side])
        pb.keyframe_insert(path, frame=F0 + RETURN)
    scn0 = bpy.context.scene
    scn0.frame_set(1)
gw = st.effector_weights
gw.gravity = 0.0
gw.keyframe_insert("gravity", frame=1)
gw.keyframe_insert("gravity", frame=SEWN)
gw.gravity = 1.0
gw.keyframe_insert("gravity", frame=SEWN + 20)
cl.point_cache.frame_start = 1
cl.point_cache.frame_end = FRAMES
scn = bpy.context.scene
scn.frame_start, scn.frame_end = 1, FRAMES

gaps = []
for fr in range(1, FRAMES + 1):
    scn.frame_set(fr)
    if fr % 20 == 0 or fr in (1, FRAMES):
        ev = jacket.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
        worst = {k: round(max((ev.vertices[a].co - ev.vertices[b].co).length * 1000 for a, b in v), 1) for k, v in SEAMS.items()}
        g = [(ev.vertices[a].co - ev.vertices[b].co).length * 1000 for a, b in sewing]
        gaps.append((fr, round(max(g), 1), round(sum(g) / len(g), 2), worst))
        print("SEW frame %d: widest gap %.1f mm, mean %.2f; by seam %s" % (fr, max(g), sum(g) / len(g), worst), flush=True)

ev = jacket.evaluated_get(bpy.context.evaluated_depsgraph_get())
if BODY_ONLY:
    np.save(os.path.join(OUT, "settled_body.npy"), np.array([tuple(v.co) for v in ev.data.vertices]))
done = bpy.data.meshes.new_from_object(ev)
jacket.modifiers.clear()
old = jacket.data
jacket.data = done
bm = bmesh.new()
bm.from_mesh(done)
bm.verts.ensure_lookup_table()
for a, b in sewing:
    m = (bm.verts[a].co + bm.verts[b].co) / 2
    bm.verts[a].co = m
    bm.verts[b].co = m
bmesh.ops.delete(bm, geom=[e for e in bm.edges if not e.link_faces], context="EDGES")
bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.0005)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
cen = Vector((CX, CY, (HPS_Z + chest_z) / 2))
if sum(f.normal.dot(f.calc_center_median() - cen) for f in bm.faces) < 0:
    bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
# how far off the body it sits, and the hem's width against the chest's
if POSE is not None:
    # measured against the body where it ended, back in its rest pose
    _fin = bpy.data.meshes.new_from_object(body_src.evaluated_get(bpy.context.evaluated_depsgraph_get()))
    _fin.transform(body_src.matrix_world)
    _bf = bmesh.new()
    _bf.from_mesh(_fin)
    BVH = BVHTree.FromBMesh(_bf)
near = [BVH.find_nearest(v.co) for v in bm.verts]
clear_mm = sorted((n[3] * 1000.0) for n in near if n[0] is not None)
hem_z = min(v.co.z for v in bm.verts)
hem_ring = [v.co for v in bm.verts if v.co.z < hem_z + 0.02]
chest_ring = [v.co for v in bm.verts if abs(v.co.z - chest_z) < 0.01 and abs(v.co.x - CX) < HALF_W + 0.02]
width = lambda ring: (max(p.x for p in ring) - min(p.x for p in ring)) if ring else 0.0
bm.to_mesh(done)
bm.free()
for p in done.polygons:
    p.use_smooth = True

# ---- pictures, files, report ---------------------------------------------------

wool = bpy.data.materials.new("M_DonkeyWool")
wool.use_nodes = True
wool.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.022, 0.032, 1)
wool.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
wool.diffuse_color = (0.05, 0.06, 0.09, 1)
jacket.data.materials.append(wool)
grey = bpy.data.materials.new("M_Body")
grey.diffuse_color = (0.5, 0.5, 0.5, 1)
collider.data.materials.clear()
collider.data.materials.append(grey)
scn.render.engine = "BLENDER_WORKBENCH"
scn.display.shading.light = "STUDIO"
scn.display.shading.color_type = "MATERIAL"
scn.render.resolution_x, scn.render.resolution_y = 900, 1200
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
scn.collection.objects.link(cam)
scn.camera = cam
cam.data.lens = 70
mid = Vector((CX, CY, (HPS_Z + hem_z) / 2))
for label, off in (("front", (0, -3.4, 0.1)), ("side", (3.4, 0, 0.1)), ("back", (0, 3.4, 0.1)), ("three-quarter", (2.3, -2.4, 0.4))):
    cam.location = mid + Vector(off)
    cam.rotation_euler = (mid - cam.location).to_track_quat("-Z", "Y").to_euler()
    scn.render.filepath = os.path.join(OUT, "jacket-%s.png" % label)
    bpy.ops.render.render(write_still=True)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "jacket.blend"))
report = {"pattern": SRC, "body": BODY, "frames": FRAMES, "pose": POSE, "lift": LIFT, "vertices": len(done.vertices), "triangles": len(done.polygons),
          "seamPairs": len(sewing), "gapsByFrame": gaps,
          "clearanceMm": {"min": round(clear_mm[0], 1), "p05": round(clear_mm[len(clear_mm) // 20], 1),
                          "median": round(clear_mm[len(clear_mm) // 2], 1)},
          "hemWidthM": round(width(hem_ring), 3), "chestWidthM": round(width(chest_ring), 3),
          "minutes": round((time.time() - T0) / 60, 1)}
json.dump(report, open(os.path.join(OUT, "jacket.json"), "w"), indent=1)
print("SEWN " + json.dumps({k: v for k, v in report.items() if k != "gapsByFrame"}))
