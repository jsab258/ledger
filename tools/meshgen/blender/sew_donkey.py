"""Ron's donkey jacket: FreeSewing's Brian sewn and draped round his body in Blender, arms held out, then posed back.

    blender -b -P tools/meshgen/blender/sew_donkey.py -- BRIAN.json BODY.fbx OUT_DIR [--pose 40] [--place-only] [--frames N]

WHY, 29 September (the clothing session, CLOTHES.md item 2; Jafar's ruling of
29 September: drape with the arms held out from the body and pose
afterwards). The builder's pattern route (sew_jacket.py, production/art/
clothing/donkey-jacket-pattern) made a clean body but lost the sleeves three
ways. Two things change here:

1. THE PATTERN. The earlier draft took Ron's armpit 15 cm under his shoulder
   (a rule of 9 cm under the arm's joint, in a pose whose arms are raised),
   so Brian drew a shirt's 17 cm armhole whose foot sat above his real
   armpit, inside the root of the arm, and a 4 cm sleeve cap on a sleeve
   54 cm wide. body_measurements.py now finds the armpit on the body (22 cm
   under the shoulder) and takes shoulder to shoulder round the back, as
   FreeSewing does; the draft (armholeDepth 6%, bicepsEase 12%, a 5 degree
   shoulder, the raised shoulders of the pose it is exported in) has a 25
   cm armhole and a 12.4 cm cap, a work jacket's.
2. THE ORDER (after the research, SLEEVES-RECIPE-2026-09-29.md, and
   sixteen runs; production/art/clothing/donkey-jacket-sewn/README.md).
   Everything is placed at once round the posed body, arms present: the
   body pieces hung on a curtain from the shoulders at the heights they have
   on the pattern, the sleeves as unstretched tubes hanging on the arms,
   nothing starting inside the body; each piece remembers the shape it was
   laid in. Sewn weightless with the sewing force drawn in over 15 frames to
   as good as unlimited, slippery on the body: gaps of 10 to 25 cm close.
   The seams are welded, the cloth settles under gravity remembering the
   pattern's own lengths, and the body's own skeleton carries it back to the
   rest pose (its points first taken back through the skin, tailor.unpose),
   the cloth on top settling it. press_garment.py then irons out the
   crinkles the sewing leaves.

OUT_DIR gets place-*.png (the placement), stitched-*.png, settled-*.png and
settled.blend (the sewing pose), jacket-*.png and jacket.blend (the body's
rest pose, for press_garment.py and finish_donkey.py, which writes the files
for Unreal) and jacket.json.
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brian  # noqa: E402
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, BODY, OUT = argv[0], argv[1], argv[2]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


POSE = opt("--pose", 40.0)                  # the arms held out: degrees below the horizontal while sewn
EDGE = opt("--edge", 12.0)                  # cloth triangle edge while draping, mm
CLEAR = opt("--clear", 0.035)               # the body pieces start this far out from the torso, m
LIFT = opt("--lift", 0.0)
SEW_FRAMES = opt("--sew", 60, int)          # weightless sewing
DROP_FRAMES = opt("--drop", 60, int)        # gravity ramped in and settled
RETURN_FRAMES = opt("--return", 60, int)    # the arms back to the rest pose
PLACE_ONLY = "--place-only" in argv
NAME = opt("--name", "ron_donkey", str)
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
log = {"pattern": SRC, "body": BODY, "pose": POSE, "edge": EDGE}


def say(*a):
    print("SEW", *a, flush=True)


# ---- the pattern's pieces ----------------------------------------------------------

P = brian.pieces(SRC, EDGE)
B, F, S, cap = P["B"], P["F"], P["S"], P["cap"]
sp = P["points"]["sleeve"]
L = tailor.length
PIECES, IDX = P["pieces"], P["idx"]
b_idx, f_idx = IDX["back"], IDX["front"]
log["lengthsMm"] = P["lengths"]
say("lengths", log["lengthsMm"])

# ---- the body, arms held out ------------------------------------------------------

arm, body_src = tailor.load_body(BODY, lod=opt("--lod", 1, int))
REST_DEG = tailor.arm_angle(arm, "l")
REST_ROT = tailor.pose_arms(arm, POSE)
say("arms %.1f degrees below the horizontal at rest, sewn at %.1f" % (REST_DEG, tailor.arm_angle(arm, "l")))
body = tailor.evaluated_copy(body_src, "BodyPosed")
body_src.hide_set(True)
body_src.hide_render = True
BVH = tailor.bvh_of(body)
bones = tailor.dominant_bones(body_src)
bco = tailor.coords(body, evaluated=False)
is_arm = np.array([b.startswith(tailor.ARMISH) for b in bones])
J = lambda n: tailor.joint(arm, n)
up = {1: J("upperarm_l"), -1: J("upperarm_r")}
el = {1: J("lowerarm_l"), -1: J("lowerarm_r")}
wr = {1: J("hand_l"), -1: J("hand_r")}
torso = bco[~is_arm]

meas = json.load(open(opt("--measure", os.path.join(os.path.dirname(BODY), "measurements.json"), str)))
HPS_Z = meas["heights_m"]["hps"]
CHEST_Z = meas["heights_m"]["chest"]
sl = torso[np.abs(torso[:, 2] - CHEST_Z) < 0.01]
sl = sl[np.abs(sl[:, 0]) < abs(up[1].x)]
CX, CY = 0.0, float((sl[:, 1].max() + sl[:, 1].min()) / 2)
HALF_W0 = float(sl[:, 0].max() - sl[:, 0].min()) / 2 + CLEAR
HALF_D0 = float(sl[:, 1].max() - sl[:, 1].min()) / 2 + CLEAR

# ---- placing the body pieces: rolled round an ellipse of the pieces' own girth -----

ANG = np.linspace(0, 2 * math.pi, 4001)
GIRTH = 4 * L(B["hem"]) / 1000.0


def perim(a, b):
    return float(np.hypot(np.diff(a * np.sin(ANG)), np.diff(b * np.cos(ANG))).sum())


SCALE = GIRTH / perim(HALF_W0, HALF_D0)
HW, HD = HALF_W0 * SCALE, HALF_D0 * SCALE
EX, EY = HW * np.sin(ANG) + CX, HD * np.cos(ANG) + CY
ARC = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(EX), np.diff(EY)))])
PER = ARC[-1]
say("ellipse %.3f x %.3f m (torso %.3f x %.3f + %.3f), girth %.3f" % (HW, HD, HALF_W0 - CLEAR, HALF_D0 - CLEAR, CLEAR, GIRTH))


def on_ellipse(s):
    a = np.interp(s % PER, ARC, ANG)
    return Vector((HW * math.sin(a) + CX, HD * math.cos(a) + CY, 0.0)), Vector((math.sin(a) / HW, math.cos(a) / HD, 0.0)).normalized()


# THE SHOULDERS: above the chest each piece leans in over the shoulder, so
# that front and back meet on top of it. Each column of the piece (a fixed x
# on the pattern) is laid along the body's own outline in the vertical plane
# through its place on the ellipse: from the top of the shoulder (the body
# there, lifted by the clearance) over and down to the ellipse's wall, then
# straight down. The path is found from the body by rays, so the shoulder
# seam lies on the shoulder and the back of the neck on the neck.


# THE CURTAIN (the placement's shape above the chest): each column of a body
# piece, a fixed place round the ellipse, hangs at the height its point has
# on the pattern, and as far out from the torso's axis as the torso itself
# (plus the clearance) reaches at that height OR ANYWHERE ABOVE IT, as a
# curtain falls from the shoulders over the chest; never further out than
# the ellipse. So the tops lie on the shoulders and round the neck, the fronts
# fall from the chest, and the hem is level. The torso alone is used (the
# arms pass through the armholes). A table over the ellipse's round and the
# height, found by rays, then read by interpolation.
_torso = tailor.evaluated_copy(body_src, "TorsoOnly")
_tb = bmesh.new()
_tb.from_mesh(_torso.data)
_tb.verts.ensure_lookup_table()
bmesh.ops.delete(_tb, geom=[_tb.verts[i] for i in range(len(_tb.verts)) if is_arm[i]], context="VERTS")
from mathutils.bvhtree import BVHTree  # noqa: E402
TORSO = BVHTree.FromBMesh(_tb)
_tb.free()
bpy.data.objects.remove(_torso, do_unlink=True)
S_STEP, Z_STEP = 0.005, 0.005
S_ROWS = np.arange(0.0, PER, S_STEP)
Z_TOP_T = HPS_Z + 0.03
Z_ROWS = np.arange(Z_TOP_T, HPS_Z - 1.0, -Z_STEP)
CURTAIN = np.zeros((len(S_ROWS), len(Z_ROWS)))      # how far in from the wall, m (0 = on the wall)
for i, s in enumerate(S_ROWS):
    P, n = on_ellipse(float(s))
    reach = -1.0                                   # the furthest out, along n from the axis side, seen so far
    first = None
    for j, z in enumerate(Z_ROWS):
        o = Vector((P.x, P.y, z)) + n * 0.25
        hit = TORSO.ray_cast(o, -n, 0.7)
        if hit[0] is not None:
            out_from_wall = (hit[0] - Vector((P.x, P.y, z))).dot(n) + CLEAR   # >0: the body pokes past the wall
            reach = max(reach, out_from_wall) if reach > -1.0 else out_from_wall
        CURTAIN[i, j] = 0.0 if reach == -1.0 else max(0.0, -reach)
        if reach != -1.0 and first is None:
            first = j
    # ABOVE THE BODY'S TOP (a column whose top edge stands higher than the
    # shoulder under it) the column leans in as far as the first row that met
    # the body: with nothing hit it stood on the ellipse's wall, 15 cm behind
    # the shoulder seam it is sewn to (run 5: edges stretched 21 times)
    if first is not None:
        CURTAIN[i, :first] = CURTAIN[i, first]
say("curtain table %d x %d" % CURTAIN.shape)


def lean_at(s, z):
    i = (s % PER) / S_STEP
    j = (Z_TOP_T - z) / Z_STEP
    i0, j0 = int(math.floor(i)) % len(S_ROWS), max(0, min(len(Z_ROWS) - 1, int(math.floor(j))))
    i1, j1 = (i0 + 1) % len(S_ROWS), min(len(Z_ROWS) - 1, j0 + 1)
    fi, fj = i - math.floor(i), max(0.0, min(1.0, j - j0))
    a = CURTAIN[i0, j0] * (1 - fj) + CURTAIN[i0, j1] * fj
    b = CURTAIN[i1, j0] * (1 - fj) + CURTAIN[i1, j1] * fj
    return a * (1 - fi) + b * fi


def place_body(flat, start_s, direction, curtain=True):
    """Each point of a body piece: round the ellipse by its x, at its pattern height; in on the curtain,
    or (curtain=False) on the ellipse's wall itself, the piece rolled without stretching: its rest shape."""
    out = []
    for x, y in flat:
        s = start_s + direction * x / 1000.0
        P, n = on_ellipse(s)
        z = HPS_Z + LIFT - y / 1000.0
        q = P - n * lean_at(s, z) if curtain else P
        out.append((q.x, q.y, z))
    return out


def mirror3(pts):
    return [(2 * CX - x, y, z) for x, y, z in pts]


# THE ARMHOLE GOES ROUND THE ARM (29 September, run 10): the curtain is laid
# on the torso with the arms left out, so near the armhole it lay inside the
# root of the arm, and no sleeve round the arm could reach it without passing
# through the arm. Every body-piece point nearer the upper arm's axis than
# the arm's own radius and a clearance goes out from that axis, square to
# it, so the armhole wraps round the arm's root, over the top of the shoulder
# and under the arm, as a real armhole does.
ARM_CLEAR = opt("--arm-clear", 0.012)
R_ARM_ROOT = meas["measurements"]["biceps"] / 2000.0 / math.pi


def round_the_arm(pts, side):
    sh, e = up[side], el[side]
    a = (e - sh).normalized()
    out = []
    moved = 0
    for q in pts:
        v = Vector(q)
        t = (v - sh).dot(a)
        if t < -0.03 or t > (e - sh).length:
            out.append(q)
            continue
        c = sh + a * max(0.0, t)
        d = v - c
        r = d.length
        want = R_ARM_ROOT + ARM_CLEAR
        if r >= want or r < 1e-6:
            out.append(q)
            continue
        out.append(tuple(c + d * (want / r)))
        moved += 1
    return out, moved


def body_round_arms(pts):
    left, n1 = round_the_arm(pts, 1)
    both, n2 = round_the_arm(left, -1)
    return both, n1 + n2


QUARTER = GIRTH / 4
G = tailor.Garment()
bflat, bfaces = PIECES["back"]
fflat, ffaces = PIECES["front"]
sflat, sfaces = PIECES["sleeve"]
AT = {}
b_on, b_rest = place_body(bflat, 0.0, 1), place_body(bflat, 0.0, 1, curtain=False)
b_on, _moved_b = body_round_arms(b_on)
AT[("back", 1)] = G.add("back", bflat, bfaces, b_on, rest=b_rest)
fold = {k: AT[("back", 1)][k] for k in b_idx["fold"]}
AT[("back", -1)] = G.add("back", bflat, bfaces, mirror3(b_on), mirror=True, share=fold, rest=mirror3(b_rest))
f_on, f_rest = place_body(fflat, 2 * QUARTER, -1), place_body(fflat, 2 * QUARTER, -1, curtain=False)
f_on, _moved_f = body_round_arms(f_on)
say("body points moved out round the arms: back %d, front %d" % (_moved_b, _moved_f))
AT[("front", 1)] = G.add("front_l", fflat, ffaces, f_on, layout=(1.0, 0.0), rest=f_rest)
AT[("front", -1)] = G.add("front_r", fflat, ffaces, mirror3(f_on), layout=(-1.0, 0.0), mirror=True, rest=mirror3(f_rest))

# ---- placing the sleeves: tubes round the arms, blended into their armholes -------------

W_TOP, W_CUFF = 2 * sp["bicepsRight"][0], 2 * sp["wristRight"][0]
Y_CUFF = sp["centerWrist"][1]
Y_CROWN = min(y for _, y in cap)
R_BICEPS = meas["measurements"]["biceps"] / 2000.0 / math.pi
R_WRIST = meas["measurements"]["wrist"] / 2000.0 / math.pi


def tube(side, x, y):
    """A point of the flat sleeve on a tube round the arm: y down the arm from the crown, x round it (0 on top).
    Rolled without stretching: the tube's girth at each height is the sleeve's own width there."""
    sh, e, w = up[side], el[side], wr[side]
    a1, a2 = e - sh, w - e
    sa = 0.02 + (y - Y_CROWN) / 1000.0                  # the crown just outside the joint, over the shoulder point
    if sa < a1.length:
        ax, base = a1.normalized(), sh + a1.normalized() * sa
    else:
        ax, base = a2.normalized(), e + a2.normalized() * (sa - a1.length)
    t = max(0.0, min(1.0, y / Y_CUFF))
    wdt = W_TOP + (W_CUFF - W_TOP) * t
    r = wdt / (2 * math.pi) / 1000.0
    across = ax.cross(Vector((0, 0, 1))).normalized()
    over = across.cross(ax).normalized()
    th = math.pi * x / (wdt / 2)
    # A SLEEVE HANGS ON THE TOP OF THE ARM (run 6): centred on the arm, the
    # tube's underarm stood 5 cm above the armhole it is sewn to and the relax
    # stretched it half again; lowered so its top lies just over the arm, the
    # room between sleeve and arm is all underneath, as a sleeve hangs
    r_arm = (R_BICEPS + (R_WRIST - R_BICEPS) * max(0.0, min(1.0, (sa - 0.12) / 0.5)))
    base = base - over * max(0.0, r - r_arm - 0.006)
    return base + (over * math.cos(th) + across * math.sin(th) * side) * r


armhole_pos = {}
for side in (1, -1):
    for sseg, piece in (("capBack", "back"), ("capFront", "front")):
        ia = IDX[piece]["armhole"]
        ib = IDX["sleeve"][sseg]
        if sseg == "capFront":
            ib = list(reversed(ib))
        for x_, y_ in zip(ia, ib):
            armhole_pos[(side, y_)] = Vector(G.verts[AT[(piece, side)][x_]])
BLEND = opt("--blend", 0.0)                 # 0: the sleeves start unstretched and the sewing brings them to the armholes
cap_ids = sorted({k for (_, k) in armhole_pos})
# THE TUBE MOVED WHOLE TO ITS ARMHOLE (29 September, run 10): unstretched
# and unblended, the tubes' cap edges lay 9 to 12 cm from their armholes,
# though a cap loop and its armhole are near enough the same size and height
# along the arm; so each tube is first moved, rigidly (it stays unstretched),
# to where its cap edge fits its armhole best by least squares
FIT = {1: Vector(), -1: Vector()}
if "--fit" in argv:
    for side in (1, -1):
        d = [armhole_pos[(side, k)] - tube(side, *sflat[k]) for k in cap_ids]
        FIT[side] = sum(d, Vector()) / len(d)
        say("sleeve %d moved %.1f cm to its armhole" % (side, FIT[side].length * 100))
if "--probe" in argv:
    sh, e = up[1], el[1]
    ax = (e - sh).normalized()
    across = ax.cross(Vector((0, 0, 1))).normalized()
    over = across.cross(ax).normalized()
    for lab, pts_ in (("armhole", [armhole_pos[(1, k)] for k in cap_ids]), ("tubecap", [tube(1, *sflat[k]) for k in cap_ids])):
        for q in pts_[::4]:
            d = q - sh
            t = d.dot(ax)
            rad = d - ax * t
            angle = math.degrees(math.atan2(rad.dot(across), rad.dot(over)))
            say("PROBE %s t %.3f r %.3f angle %.0f  xyz %.3f %.3f %.3f" % (lab, t, rad.length, angle, q.x, q.y, q.z))
_tube = tube


def tube(side, x, y):  # noqa: F811
    return _tube(side, x, y) + FIT[side]


for side in (1, -1):
    ring = sorted(((sflat[k][0], sflat[k][1], armhole_pos[(side, k)] - tube(side, *sflat[k])) for k in cap_ids), key=lambda r: r[0])
    rx = np.array([r[0] for r in ring])
    placed, rest = [], []
    for k, (x, y) in enumerate(sflat):
        p = tube(side, x, y)
        rest.append(tuple(p))
        if BLEND > 0:
            j = int(np.argmin(np.abs(rx - x)))
            down = max(0.0, (y - ring[j][1]) / 1000.0)
            b = max(0.0, min(1.0, 1.0 - down / BLEND))
            p = p + ring[j][2] * (b * b * (3 - 2 * b))
        placed.append(tuple(p))
    AT[("sleeve", side)] = G.add("sleeve_l" if side > 0 else "sleeve_r", sflat, sfaces, placed,
                                 layout=(2.0 if side > 0 else -2.0, 0.0), mirror=side < 0, rest=rest)

# ---- the seams ---------------------------------------------------------------------


def pairs(p1, s1, seg1, p2, s2, seg2, rev=False):
    ia = [AT[(p1, s1)][k] for k in IDX[p1][seg1]]
    ib = [AT[(p2, s2)][k] for k in IDX[p2][seg2]]
    return ia, list(reversed(ib)) if rev else ib


for s_ in (1, -1):
    G.seam("shoulder", *pairs("back", s_, "shoulder", "front", s_, "shoulder"))
    G.seam("side", *pairs("back", s_, "side", "front", s_, "side"))
    G.seam("armhole back", *pairs("back", s_, "armhole", "sleeve", s_, "capBack"))
    G.seam("armhole front", *pairs("front", s_, "armhole", "sleeve", s_, "capFront", rev=True))
    G.seam("underarm", *pairs("sleeve", s_, "right", "sleeve", s_, "left", rev=True))
G.seam("centre front", *pairs("front", 1, "cf", "front", -1, "cf"))

# NOTHING STARTS INSIDE THE BODY: points inside it go out along the nearest
# surface's normal, sleeve points out from the arm's own axis
pushed = 0
for i, co in enumerate(G.verts):
    v = Vector(co)
    if tailor.depth_inside(BVH, v) <= 0.0:
        continue
    pushed += 1
    piece = G.piece_of[i]
    if piece.startswith("sleeve"):
        side = 1 if piece.endswith("_l") else -1
        sh, e = up[side], el[side]
        a = e - sh
        t = max(0.0, min(1.0, (v - sh).dot(a) / a.length_squared))
        c = sh + a * t
        dr = (v - c).normalized()
        r = (v - c).length
        for _ in range(40):
            r += 0.005
            if tailor.depth_inside(BVH, c + dr * r) <= 0.0 and BVH.find_nearest(c + dr * r)[3] > 0.004:
                break
        G.verts[i] = tuple(c + dr * r)
    else:
        hit, nrm, _f, _d = BVH.find_nearest(v)
        G.verts[i] = tuple(hit + nrm * 0.006)
say("pushed %d points out of the body" % pushed)

# SEAMS THAT START SHUT STAY SHUT: the pairs placed together (the sides, the
# front, the underarms, and the armholes when the sleeves are blended in) and
# the shoulders (a few cm apart over the ridge) go to their midpoint, clear of
# the body; the pull of the rest shape takes up the difference
SNAP = ["side", "centre front", "underarm"] + (["armhole back", "armhole front"] if BLEND > 0 else []) +     (["shoulder"] if "--snap-shoulder" in argv else [])
# a point in two such seams (the shoulder point, the armpit) moves once, with
# everything joined to it: each joined group to its mean
_par = list(range(len(G.verts)))


def _find(i):
    while _par[i] != i:
        _par[i] = _par[_par[i]]
        i = _par[i]
    return i


for lab in SNAP:
    for a, b in G.seams[lab]:
        ra, rb = _find(a), _find(b)
        if ra != rb:
            _par[max(ra, rb)] = min(ra, rb)
_grp = {}
for i in range(len(G.verts)):
    _grp.setdefault(_find(i), []).append(i)
for members in _grp.values():
    if len(members) < 2:
        continue
    m = Vector(np.mean([G.verts[i] for i in members], axis=0))
    if tailor.depth_inside(BVH, m) > 0.0 or BVH.find_nearest(m)[3] < 0.004:
        hit, nrm, _f, _d = BVH.find_nearest(m)
        m = hit + nrm * 0.006
    for i in members:
        G.verts[i] = tuple(m)
# and anything the moves left inside goes out along the nearest normal
for i, co in enumerate(G.verts):
    v = Vector(co)
    if tailor.depth_inside(BVH, v) > 0.0:
        hit, nrm, _f, _d = BVH.find_nearest(v)
        G.verts[i] = tuple(hit + nrm * 0.006)
# THE BODY PIECES REMEMBER WHERE THEY WERE PLACED (29 September, run 3):
# with the straight wrap as their rest shape, its bending fought the fold over
# the shoulders, and the whole jacket slid down, weightless, to where a
# straight tube fits, the chest, the shoulders bare. Placed on the curtain
# their lengths are the pattern's within 4% (the placement's check), and the
# fold over the shoulder is the one they keep. The sleeves keep their
# unstretched tube: their blend into the armhole stretches the cap by up to
# three quarters, which a rest shape would keep.
if opt("--body-rest", "placed", str) == "placed":
    for i in range(len(G.verts)):
        if not G.piece_of[i].startswith("sleeve"):
            G.rest[i] = G.verts[i]
jacket = G.build("Jacket")
co0 = tailor.coords(jacket, evaluated=False)
inside0 = tailor.inside_count(BVH, co0, range(len(co0)))
log["place"] = {"points": len(G.verts), "triangles": len(G.faces), "pushedOut": pushed, "insideAfter": inside0,
                "seamGapsMm": tailor.seam_gaps(co0, G.seams), "strainVsPattern": tailor.strain(jacket, co0, G.groups, G.flat),
                "worstEdges": tailor.worst_edges(jacket, co0, G.flat, G.piece_of)}
say("placed", json.dumps(log["place"]))

wool = tailor.material("M_DonkeyWool", (0.02, 0.022, 0.032), 0.95)
jacket.data.materials.append(wool)
grey = tailor.material("M_Body", (0.5, 0.5, 0.5))
body.data.materials.append(grey)
MID = Vector((CX, CY, HPS_Z - 0.42))
tailor.pictures(os.path.join(OUT, "place"), MID)
if PLACE_ONLY:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "place.blend"))
    json.dump(log, open(os.path.join(OUT, "jacket.json"), "w"), indent=1)
    say("placed only, %.1f min" % ((time.time() - T0) / 60))
    sys.exit(0)

# ---- 1. the sleeves relaxed, their tops held on the armholes ------------------------------
#
# THE SLEEVE MEETS ITS ARMHOLE BY RELAXING, NOT BY TUG OF WAR (29 September,
# runs 3 and 4): pulled by sewing springs from its tube to the armhole, a
# sleeve's own rest shape pulled back and the armhole stood 6 cm open; and
# the blend that starts the cap on the armhole stretches it by up to three
# quarters. So first the body pieces and the sleeve caps' edges are held
# where they were placed (the caps' edges on the armholes they are sewn to),
# and each sleeve, weightless, relaxes towards its unstretched tube round the
# arm: it finds a shape near the pattern's lengths with its top on the
# armhole. Then every seam lies shut, and the seams are welded as they are.

scn = bpy.context.scene
CL = dict(mass=opt("--mass", 0.006), tension=opt("--tension", 40.0), compression=opt("--compression", 60.0),
          shear=opt("--shear", 15.0), bending=opt("--bending", 60.0))
# SETTLED AND CARRIED AT MELTON'S TRUE WEIGHT (FIT-AND-STIFFNESS-2026-09-29.md:
# at 0.006 kg a point the jacket weighed 84 kg, and sagged, clung, hung out
# behind and stretched into a sail), with the bending that keeps a melton-
# stiff line at that weight (a bending length near 8 cm by the helper's
# estimate); the sewing itself, weightless, keeps what worked
HANG = dict(CL, mass=None, bending=opt("--hang-bending", 10.0))
log["cloth"] = CL
# THE STITCH, 29 September run 9 (runs 3 to 8: a rest shape that bends one
# way fought the fold over the shoulder, and friction 60 held the sleeves
# where the blend had stretched them): the pieces remember their unstretched
# wraps (the pattern's lengths), bend almost freely, and slide on the body,
# so each settles where its seams hold it; normal stiffness after the weld
tailor.collider(body, friction=opt("--stitch-friction", 5.0))
stitch = dict(CL, bending=opt("--stitch-bending", 25.0))
cl = tailor.cloth(jacket, sewing=True, rest_key="rest", frames=SEW_FRAMES, **stitch)
cl.settings.effector_weights.gravity = 0.0
# THE SEAMS DRAWN IN OVER 15 FRAMES, not at once (run 12: pulled shut in a
# frame or two, the sleeves were jerked up their arms and crinkled); by then
# the cap is far above any force the gaps call for, as good as unlimited
cl.settings.sewing_force_max = 5.0
cl.settings.keyframe_insert("sewing_force_max", frame=1)
cl.settings.sewing_force_max = 500.0
cl.settings.keyframe_insert("sewing_force_max", frame=15)
if "--hold" in argv:
    held = jacket.vertex_groups.new(name="held")
    held.add([i for i in range(len(G.verts)) if not G.piece_of[i].startswith("sleeve")], 1.0, "REPLACE")
    held.add([b for lab in ("armhole back", "armhole front") for _a, b in G.seams[lab]], 1.0, "REPLACE")
    cl.settings.vertex_group_mass = "held"
scn.frame_start, scn.frame_end = 1, SEW_FRAMES
gaps = []
for f in range(1, SEW_FRAMES + 1):
    scn.frame_set(f)
    if f % 10 == 0 or f == 1:
        c = tailor.coords(jacket)
        g = tailor.seam_gaps(c, G.seams)
        gaps.append((f, g))
        say("stitch frame %d gaps %s strain %s" % (f, g, {k: v for k, v in tailor.strain(jacket, c, G.groups, G.flat).items() if k.startswith("sleeve")}))
co = tailor.coords(jacket)
log["stitch"] = {"gapsByFrame": gaps, "strainVsPattern": tailor.strain(jacket, co, G.groups, G.flat),
                "worstEdges": tailor.worst_edges(jacket, co, G.flat, G.piece_of),
                "inside": tailor.inside_count(BVH, co, range(len(co))), "minutes": round((time.time() - T0) / 60, 1)}
say("stitched", json.dumps({k: v for k, v in log["stitch"].items() if k != "gapsByFrame"}))
tailor.apply_frame(jacket)
if jacket.vertex_groups.get("held"):
    jacket.vertex_groups.remove(jacket.vertex_groups["held"])
tailor.pictures(os.path.join(OUT, "stitched"), MID, views=(("front", (0, -3.4, 0.1)), ("three-quarter", (2.3, -2.4, 0.4)), ("back", (0, 3.4, 0.1))))

# ---- 2. weld the seams, then settle under gravity ------------------------------------------

body.collision.cloth_friction = opt("--friction", 20.0)
merged = tailor.weld(jacket, G.sewing, co)
out_ = tailor.push_out(jacket, BVH, 0.003)
log["weld"] = {"pairsMerged": merged, "of": len(G.sewing), "points": len(jacket.data.vertices), "pushedOut": out_}
say("welded", log["weld"])
scn.frame_set(1)
REST_STRAIN = tailor.pattern_rest(jacket)
log["weld"]["restVsPattern"] = REST_STRAIN
say("rest shape from the pattern's lengths, edges against the pattern (5/50/95%)", REST_STRAIN)
cl = tailor.cloth(jacket, frames=DROP_FRAMES, self_collision=True, rest_key="rest", **HANG)
gw = cl.settings.effector_weights
gw.gravity = 0.15
gw.keyframe_insert("gravity", frame=1)
gw.gravity = 1.0
gw.keyframe_insert("gravity", frame=12)
scn.frame_end = DROP_FRAMES
prev = None
for f in range(1, DROP_FRAMES + 1):
    scn.frame_set(f)
    if f % 10 == 0:
        c = tailor.coords(jacket)
        if prev is not None:
            say("settle frame %d, largest move over 10 frames %.1f mm" % (f, float(np.max(np.linalg.norm(c - prev, axis=1))) * 1000))
        prev = c
co = tailor.coords(jacket)
log["settle"] = {"inside": tailor.inside_count(BVH, co, range(len(co))), "minutes": round((time.time() - T0) / 60, 1)}
tailor.apply_frame(jacket)
tailor.pictures(os.path.join(OUT, "settled"), MID)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "settled.blend"))

# ---- 3. the arms back down to the body's rest pose, the jacket carried on them ----------------

body.modifiers.clear()
body.hide_set(True)
body.hide_render = True
body_src.hide_set(False)
body_src.hide_render = False
body_src.data.materials.clear()
body_src.data.materials.append(grey)
tailor.collider(body_src, friction=opt("--friction", 20.0))
for side in ("l", "r"):
    pb = arm.pose.bones["upperarm_" + side]
    pb.keyframe_insert("rotation_quaternion", frame=1)
    pb.rotation_quaternion = REST_ROT[side]
    pb.keyframe_insert("rotation_quaternion", frame=RETURN_FRAMES)
LOWER = RETURN_FRAMES + 30
scn.frame_set(1)
LOWER_BY = opt("--lower-by", "skin", str)
if LOWER_BY == "skin":
    # THE JACKET RIDES THE SKELETON DOWN (29 September, run 14): pushed down
    # by the arms alone, the sleeves levered the whole jacket up (the hem back
    # at the crotch) and the body came through at an armpit. As the research
    # has it, the jacket takes the posed body's skin weights and is carried
    # back to the body's rest pose on the skeleton; the cloth on top, held to
    # that most at the shoulders and least at the hem, settles it and keeps it
    # off the body and itself.
    dt = jacket.modifiers.new("Weights", "DATA_TRANSFER")
    dt.object = body_src
    dt.use_vert_data = True
    dt.data_types_verts = {"VGROUP_WEIGHTS"}
    dt.vert_mapping = "POLYINTERP_NEAREST"
    dt.layers_vgroup_select_src = "ALL"
    dt.layers_vgroup_select_dst = "NAME"
    bpy.context.view_layer.objects.active = jacket
    bpy.ops.object.datalayout_transfer(modifier="Weights")
    bpy.ops.object.modifier_apply(modifier="Weights")
    # THE BODY'S OWN SKELETON CARRIES IT (a second skeleton whose rest was the
    # sewing pose did nothing in a background run: the arms came down out of
    # the sleeves): the jacket's points are taken back through the pose to the
    # rest pose by its own skin weights, so the Armature modifier puts them
    # where they are now, and brings them down with the arms
    say("arm weights taken off the body pieces:", tailor.torso_weights(jacket))
    say("points taken back to the rest pose through the skin:", tailor.unpose(jacket, arm))
    am = jacket.modifiers.new("Armature", "ARMATURE")
    am.object = arm
    scn.frame_set(1)
    uvj = jacket.data.uv_layers["pattern"]
    vuv = {lp.vertex_index: tuple(uvj.data[lp.index].uv) for lp in jacket.data.loops}
    cj = tailor.coords(jacket, evaluated=False)
    top_, bot_ = float(cj[:, 2].max()), float(cj[:, 2].min())
    hold = jacket.vertex_groups.new(name="hold")
    for i, pco in enumerate(cj):
        u, v = vuv.get(i, (0.0, 0.0))
        if abs(u) > 1.5:
            w = 0.8 - 0.3 * max(0.0, min(1.0, -v / 0.53))
        else:
            w = 1.0 - 0.8 * max(0.0, min(1.0, (top_ - 0.3 - pco[2]) / max(0.05, top_ - 0.3 - bot_)))
        hold.add([i], w, "REPLACE")
log["lower"] = {"by": LOWER_BY, "restVsPattern": tailor.pattern_rest(jacket)}
cl = tailor.cloth(jacket, frames=LOWER, self_collision=True, rest_key="rest", **HANG)
if LOWER_BY == "skin":
    cl.settings.vertex_group_mass = "hold"
    cl.settings.pin_stiffness = 1.0
scn.frame_end = LOWER
for f in range(1, LOWER + 1):
    scn.frame_set(f)
    if f % 20 == 0:
        say("lower frame %d, arm %.1f degrees" % (f, tailor.arm_angle(arm, "l")))
body_rest = tailor.evaluated_copy(body_src, "BodyRest")
BVH_REST = tailor.bvh_of(body_rest)
bpy.data.objects.remove(body_rest, do_unlink=True)
co = tailor.coords(jacket)
tailor.apply_frame(jacket)
if LOWER_BY == "skin":
    # the jacket stays where it is, in the body's rest pose, its borrowed weights gone
    for g in list(jacket.vertex_groups):
        jacket.vertex_groups.remove(g)
    co = tailor.coords(jacket, evaluated=False)

# ---- the checks, the pictures, the files -----------------------------------------------------

near = [BVH_REST.find_nearest(Vector(p)) for p in co]
clear_mm = sorted(n[3] * 1000.0 for n in near if n[0] is not None)
hem_z = float(co[:, 2].min())
hem = co[co[:, 2] < hem_z + 0.02]
chest = co[(np.abs(co[:, 2] - CHEST_Z) < 0.01) & (np.abs(co[:, 0] - CX) < HW + 0.03)]
log["rest"] = {"armDeg": round(tailor.arm_angle(arm, "l"), 1), "inside": tailor.inside_count(BVH_REST, co, range(len(co))),
               "clearanceMm": {"p05": round(clear_mm[len(clear_mm) // 20], 1), "median": round(clear_mm[len(clear_mm) // 2], 1),
                               "p95": round(clear_mm[len(clear_mm) * 19 // 20], 1)},
               "hemWidthM": round(float(np.ptp(hem[:, 0])), 3), "chestWidthM": round(float(np.ptp(chest[:, 0])), 3) if len(chest) else None,
               "hemHeightM": round(hem_z, 3), "minutes": round((time.time() - T0) / 60, 1)}
say("rest", json.dumps(log["rest"]))
for p in jacket.data.polygons:
    p.use_smooth = True
tailor.pictures(os.path.join(OUT, "jacket"), MID)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "jacket.blend"))
json.dump(log, open(os.path.join(OUT, "jacket.json"), "w"), indent=1)
say("done, %.1f min" % ((time.time() - T0) / 60))
