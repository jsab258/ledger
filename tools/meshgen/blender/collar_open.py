"""A STAND COLLAR WORN WITH ITS ZIP A FEW CENTIMETRES DOWN: THE CENTRE FRONT SPLIT AND THE TWO FRONTS PARTED (2 November 2026, Tom).

    blender -b --factory-startup -P tools/meshgen/blender/collar_open.py -- JACKET.fbx BODY.fbx FACE.fbx OUT_DIR
        --body-map BODY_MAP.png [--head-map HEAD_MAP.png] [--open-cm 6] [--gap-cm X | --gaps 5,6,7,8,9,10,12,14]
        [--reach-deg 90] [--taper smooth|linear] [--split 0.4,0.3,0.3] [--no-fbx] [--no-preview]

JACKET.fbx is the garment's skinned game file on the MetaHuman body skeleton, at rest (its weights are kept exactly);
BODY.fbx the full body with its skeleton (LOD0: the body and the head in one mesh, the body's UVs in the second tile);
FACE.fbx the head mesh as the game builds it (LOD0's skin section). BODY_MAP.png is the game's body hidden-face map
(tools/ue/blender_hidden_face_map.py: black cuts; engine V = 1 - Blender v); HEAD_MAP.png the head's shrink map
(tools/ue/blender_head_hidden_face_map.py; its head-map-record.json beside it gives MaxShrinkDistance). OUT_DIR gets the
jacket again under its own file name, the collar opened; collar-open-record.json; collar-open-preview.png. Without
--gap-cm the gaps in --gaps are measured and the least that clears every pose is chosen. --no-fbx measures only.

WHY (2 November 2026). Tom wears a zip jacket with a stand collar zipped to the top. As his head tips down (sitting,
standing up; his face at most 25 degrees below level) or turns, his chin and jaw come through the collar's top front:
skin triangles crossing collar triangles, 51 to 60 tipped down, 30 and 32 turned 45 degrees, 58 and 60 both
(tools/meshgen/blender/collar_corrective.py, its record of 2 November). Two tries on the weights failed (30 October),
a head hidden-face map cannot hide skin that shows above the collar at rest, and an outward corrective shape could not
clear the chin without flaring the collar (the corrective's record: a 52 mm push, the top edge stretched 2.19). His
yes of 2 November, 11:47: the jacket worn with its zip about 6 cm lower, as many 1990 blousons were, the top of the
zip open so the two front edges of the collar part and the chin falls between them.

WHAT IT DOES (the FBX import, posing by joint name, collar-top detection and skin-crosses-cloth test are the
corrective's, so its numbers and these agree):
  1. imports the jacket (first, so its armature keeps the FBX's own node name), the full body and the head mesh, and
     poses all three skeletons alike: rest; head down 10, 20, 25; turned 45 left and right; down 20 with 45 turned
     each way, the rotation split over neck_01, neck_02 and head (--split);
  2. finds the zip line: from the collar's top edge at the front, the chain of the mesh's own edges nearest the
     centre-front plane (the zip's tape is welded into the cloth), followed down until its length is nearest
     --open-cm; the slider sits at the chain's last point;
  3. opens it: the chain's edges are split (each point above the slider gets one copy, keeping its weights; the
     faces on his right take the copies; UVs and material slots are per face corner and do not change), then each
     side turns round the neck's line (neck_01 to head), outward toward its own side and so slightly back, which never
     brings a point nearer that line: by A0 * V(depth) * F(angle), A0 such that the two top tips part by GAP, V a
     smoothstep from 1 at the collar's top to 0 at the slider's depth (below the slider nothing moves), F a
     smoothstep from 1 at the centre front to 0 at --reach-deg round the neck (the back and the sides stay);
  4. measures per pose, before (the input) and after: skin triangles of the full body and of the head mesh crossing
     the collar's band (within 90 mm of its top) and the whole jacket; the top edge's and the band's stretch (edge
     length over rest, at most 1.2) and squeeze; at rest the gap between the opened edges and the neck, the V's width
     down the split, how far any moved point came nearer the neck's line or the skin;
  5. what the opening shows at rest: full-body skin points under the collar's top, in the opened front, that the
     jacket covered from a viewpoint and no longer covers (front, from 20 and 40 degrees above, 35 degrees to either
     side), their depth below the collar's top, which mesh they belong to in the game (the body's UVs sit in the
     second tile, the head's in the first), and for body points whether the body map cuts them (a hole), for head
     points how far the head map shrinks them; also the collar's inside faces newly seen (the material draws one side);
  6. writes the opened jacket (the export the earlier skinned files were written with) and compares it, imported
     again, with the input: counts, unchanged points identical, every original point's weights identical, each copy's
     weights its source's, UVs, material slots, bone names and rest matrices; then a preview (front and three-quarter,
     at rest and 25 down, before and after).
"""
import json
import math
import os
import re
import struct
import sys
import time
import zlib

import numpy as np


# ---- THE PURE RULES ---------------------------------------------------------------------------------------------------
def smoothstep(x):
    x = np.clip(np.asarray(x, float), 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def half_angle_for_gap(gap, rho):
    """The turn each side's top tip needs round the neck's line so the two tips, starting together at radius rho,
    part by gap (a chord of 2 rho sin a)."""
    return math.asin(min(1.0, gap / (2.0 * rho)))


# ---- BLENDER ----------------------------------------------------------------------------------------------------------
import bmesh  # noqa: E402
import bpy  # noqa: E402
from mathutils import Matrix, Quaternion, Vector  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402
from mathutils.kdtree import KDTree  # noqa: E402

T_START = time.time()
argv = sys.argv[sys.argv.index("--") + 1:]
JACKET, BODY, FACE, OUT = argv[:4]


def opt(n, d, f=float):
    return f(argv[argv.index(n) + 1]) if n in argv else d


BODY_MAP = opt("--body-map", None, str)
HEAD_MAP = opt("--head-map", None, str)
OPEN = opt("--open-cm", 6.0) / 100.0
GAP_FIXED = opt("--gap-cm", 0.0) / 100.0
GAPS = [float(x) / 100.0 for x in opt("--gaps", "5,6,7,8,9,10,12,14", str).split(",")]
REACH = opt("--reach-deg", 90.0)
TAPER = opt("--taper", "smooth", str)          # the V's edges: smooth (smoothstep) or linear from the top to the slider
SPLIT = [float(x) for x in opt("--split", "0.4,0.3,0.3", str).split(",")]
WRITE = "--no-fbx" not in argv
PREVIEW_ON = "--no-preview" not in argv
JOINTS = ("neck_01", "neck_02", "head")
POSES = [("rest", 0, 0), ("down10", 10, 0), ("down20", 20, 0), ("down25", 25, 0), ("left45", 0, 45),
         ("right45", 0, -45), ("down20_left45", 20, 45), ("down20_right45", 20, -45)]
COLLAR_RHO = 0.13    # jacket points this close to the neck's line give the collar's top by angle (m; the head-map tool's)
BAND_RHO = 0.20
DEPTH = 0.09         # the collar's band: within this of its top (the corrective's)
BINS = 72
SKIN_REACH = 0.30
STRETCH_MAX = 1.2
VIEWS = {            # from the skin toward the viewer (Blender: front is -Y, his left +X, up +Z)
    "front": (0.0, -1.0, 0.0),
    "front_above20": (0.0, -math.cos(math.radians(20)), math.sin(math.radians(20))),
    "front_above40": (0.0, -math.cos(math.radians(40)), math.sin(math.radians(40))),
    "his_left35": (math.sin(math.radians(35)), -math.cos(math.radians(35)), 0.0),
    "his_right35": (-math.sin(math.radians(35)), -math.cos(math.radians(35)), 0.0),
}
os.makedirs(OUT, exist_ok=True)


def log(*a):
    print("COLLAR-OPEN", "%6.1fs" % (time.time() - T_START), *a, flush=True)


def import_fbx(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    return next((o for o in new if o.type == "ARMATURE"), None), [o for o in new if o.type == "MESH"]


def to_world(A, X):
    return X @ A[:3, :3].T + A[:3, 3]


def evaluated_world(o):
    dg = bpy.context.evaluated_depsgraph_get()
    e = o.evaluated_get(dg)
    m = e.to_mesh()
    X = np.zeros(len(m.vertices) * 3)
    m.vertices.foreach_get("co", X)
    e.to_mesh_clear()
    return to_world(np.array(o.matrix_world), X.reshape(-1, 3))


def lod0(meshes):
    for o in meshes:
        if o.name.endswith("_LOD0"):
            return o
    return max(meshes, key=lambda m: len(m.data.vertices))


bpy.ops.wm.read_factory_settings(use_empty=True)
jarm, jmeshes = import_fbx(JACKET)
jacket = max(jmeshes, key=lambda m: len(m.data.vertices))
JARM_NAME, JACKET_NAME = jarm.name, jacket.name
barm, bmeshes = import_fbx(BODY)
body = lod0(bmeshes)
farm, fmeshes = import_fbx(FACE)
face = lod0(fmeshes)
for o in bmeshes + fmeshes:
    if o not in (body, face):
        bpy.data.objects.remove(o, do_unlink=True)
ARMS = {"face": farm, "body": barm, "jacket": jarm}
log("imported", {k: a.name for k, a in ARMS.items()}, "jacket", jacket.name, "body", body.name, "face", face.name)


# ---- THE NECK'S LINE AND THE POSES (the corrective's) -----------------------------------------------------------------
def joint(arm, name):
    return np.array(arm.matrix_world @ arm.data.bones[name].head_local)


AX_O = joint(barm, "neck_01")
AX_A = joint(barm, "head") - AX_O
AX_A /= np.linalg.norm(AX_A)
FRONT = np.array([0.0, -1.0, 0.0])
AX_U = FRONT - (FRONT @ AX_A) * AX_A
AX_U /= np.linalg.norm(AX_U)
AX_W = np.cross(AX_A, AX_U)          # his left


def cyl(X):
    r = np.asarray(X) - AX_O
    h = r @ AX_A
    ru, rw = r @ AX_U, r @ AX_W
    rho = np.hypot(ru, rw)
    rad = (np.outer(ru, AX_U) + np.outer(rw, AX_W)) / np.maximum(rho, 1e-9)[:, None]
    return h, np.degrees(np.arctan2(rw, ru)), rho, rad


def angle_table(th, vals):
    b = np.floor((np.asarray(th) + 180.0) / 360.0 * BINS).astype(int) % BINS
    t = np.full(BINS, np.nan)
    for i in range(BINS):
        s = vals[b == i]
        if len(s):
            t[i] = s.max()
    good = ~np.isnan(t)
    if not good.all():
        idx = np.arange(BINS)
        t = np.interp(idx, idx[good], t[good], period=BINS)
    return t, int((~good).sum())


def at_angle(t, th):
    return np.interp((np.asarray(th) + 180.0) / 360.0 * BINS - 0.5, np.arange(BINS), t, period=BINS)


def turn_round_neck(X, ang):
    """Points X turned by ang (radians, per point) round the neck's line; + toward his left."""
    v = np.asarray(X) - AX_O
    par = (v @ AX_A)[:, None] * AX_A
    perp = v - par
    c, s = np.cos(ang)[:, None], np.sin(ang)[:, None]
    return AX_O + par + perp * c + np.cross(AX_A, perp) * s


rest_check = {}
for name in JOINTS:
    ref = farm.matrix_world @ farm.data.bones[name].matrix_local
    for k, arm in ARMS.items():
        m = arm.matrix_world @ arm.data.bones[name].matrix_local
        rest_check["%s_%s_vs_face" % (name, k)] = round(max(abs(m[i][j] - ref[i][j]) for i in range(3) for j in range(4)), 6)


def own_axis(arm, name, world_axis):
    R = np.array((arm.matrix_world.to_3x3().normalized() @ arm.data.bones[name].matrix_local.to_3x3()))
    k = int(np.argmax(np.abs(world_axis @ R)))
    e = np.zeros(3)
    e[k] = np.sign(world_axis @ R[:, k])
    return Vector(e), round(float(abs(world_axis @ R[:, k])), 4)


AXES = {}
for k, arm in ARMS.items():
    for name in JOINTS:
        AXES[(k, name)] = (own_axis(arm, name, np.array([1.0, 0.0, 0.0]))[0], own_axis(arm, name, np.array([0.0, 0.0, 1.0]))[0])
SIGN = {"pitch": 1.0, "yaw": 1.0}


def set_pose(pitch, yaw):
    for k, arm in ARMS.items():
        for name, frac in zip(JOINTS, SPLIT):
            side, up = AXES[(k, name)]
            pb = arm.pose.bones[name]
            pb.rotation_mode = "QUATERNION"
            pb.rotation_quaternion = (Quaternion(up, math.radians(yaw * frac * SIGN["yaw"]))
                                      @ Quaternion(side, math.radians(pitch * frac * SIGN["pitch"])))
    bpy.context.view_layer.update()


def head_moves(arm, point):
    M = arm.matrix_world @ arm.pose.bones["head"].matrix
    R = arm.matrix_world @ arm.data.bones["head"].matrix_local
    return np.array((M @ R.inverted()) @ Vector(point))


probe = joint(farm, "head") + 0.10 * FRONT
set_pose(10, 0)
if head_moves(farm, probe)[2] > probe[2]:
    SIGN["pitch"] = -1.0
set_pose(0, 10)
LEFT = np.sign(joint(farm, "clavicle_l")[0]) or 1.0
if (head_moves(farm, probe)[0] - probe[0]) * LEFT < 0:
    SIGN["yaw"] = -1.0
set_pose(0, 0)
log("signs", SIGN, "rest joints differ by at most", max(rest_check.values()), "his left is +x:", LEFT > 0)


def game_angles():
    def delta(bone):
        M = barm.matrix_world @ barm.pose.bones[bone].matrix
        R = barm.matrix_world @ barm.data.bones[bone].matrix_local
        return M.to_3x3().normalized().to_quaternion() @ R.to_3x3().normalized().to_quaternion().inverted()
    F = np.array((delta("spine_05").inverted() @ delta("head")) @ Vector(FRONT))
    return math.degrees(math.asin(max(-1.0, min(1.0, -F[2])))), math.degrees(math.atan2(F[0], -F[1]))


# ---- THE SKIN (the corrective's) ---------------------------------------------------------------------------------------
NECK_MID = AX_O + 0.04 * AX_A


def skin_of(o, largest_material):
    me = o.data
    me.calc_loop_triangles()
    T = np.zeros(len(me.loop_triangles) * 3, int)
    me.loop_triangles.foreach_get("vertices", T)
    T = T.reshape(-1, 3)
    mi = np.zeros(len(me.loop_triangles), int)
    me.loop_triangles.foreach_get("material_index", mi)
    if largest_material:
        pm = np.zeros(len(me.polygons), int)
        me.polygons.foreach_get("material_index", pm)
        T = T[mi == int(np.bincount(pm).argmax())]
    W0 = evaluated_world(o)
    c = W0[T].mean(1)
    T = T[np.linalg.norm(c - NECK_MID, axis=1) < SKIN_REACH]
    a, b, cc = W0[T[:, 0]], W0[T[:, 1]], W0[T[:, 2]]
    n = np.cross(b - a, cc - a)
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-15)
    h, _t, rho, rad = cyl((a + b + cc) / 3.0)
    sel = (h > 0.0) & (h < 0.08) & (rho < 0.09)
    out = float((np.einsum("ij,ij->i", n[sel], rad[sel]) > 0).mean()) if sel.any() else float("nan")
    if out < 0.5:
        T = T[:, ::-1].copy()
    return {"obj": o, "T": T, "outward_fraction": round(out, 3), "flipped": out < 0.5, "W0": W0}


SKIN = {"body": skin_of(body, False), "face": skin_of(face, True)}
for k, s in SKIN.items():
    log("skin", k, "triangles near the neck", len(s["T"]), "outward fraction", s["outward_fraction"])


def bvh_of(Pw, T):
    return BVHTree.FromPolygons(np.asarray(Pw).tolist(), np.asarray(T).tolist(), all_triangles=True)


# ---- THE JACKET ---------------------------------------------------------------------------------------------------------
jme = jacket.data
JA = np.array(jacket.matrix_world)
A3i = np.linalg.inv(JA[:3, :3])
NV = len(jme.vertices)
jme.calc_loop_triangles()
JT = np.zeros(len(jme.loop_triangles) * 3, int)
jme.loop_triangles.foreach_get("vertices", JT)
JT = JT.reshape(-1, 3)
JTP = np.zeros(len(jme.loop_triangles), int)
jme.loop_triangles.foreach_get("polygon_index", JTP)
JMI = np.zeros(len(jme.loop_triangles), int)
jme.loop_triangles.foreach_get("material_index", JMI)
CO0 = np.zeros(NV * 3)
jme.vertices.foreach_get("co", CO0)
CO0 = CO0.reshape(-1, 3)
J0 = evaluated_world(jacket)
log("rest pose moves the jacket's points by at most %.2e m" % float(np.abs(J0 - to_world(JA, CO0)).max()))
mat_names = [m.name if m else None for m in jme.materials]
HAD_CUSTOM_NORMALS = bool(getattr(jme, "has_custom_normals", False))

kd = KDTree(NV)
for i, p in enumerate(J0):
    kd.insert(p, i)
kd.balance()
COINCIDENT = sum(1 for i, p in enumerate(J0) if len(kd.find_range(p, 1e-5)) > 1)
# the mesh's own edges and how many faces each has
EV = np.zeros(len(jme.edges) * 2, int)
jme.edges.foreach_get("vertices", EV)
EV = EV.reshape(-1, 2)
LE = np.zeros(len(jme.loops), int)
jme.loops.foreach_get("edge_index", LE)
EFC = np.bincount(LE, minlength=len(EV))
NBR = [[] for _ in range(NV)]
EDGE_OF = {}
for e, (a, b) in enumerate(EV):
    NBR[a].append(b)
    NBR[b].append(a)
    EDGE_OF[(min(a, b), max(a, b))] = e
POLY_V = [list(p.vertices) for p in jme.polygons]
PCEN = np.array([J0[v].mean(0) for v in POLY_V])
log("jacket vertices", NV, "edges", len(EV), "faces", len(POLY_V), "coincident points", COINCIDENT,
    "custom normals", HAD_CUSTOM_NORMALS, "materials", mat_names)

JE = np.unique(np.sort(np.concatenate([JT[:, [0, 1]], JT[:, [1, 2]], JT[:, [2, 0]]]), 1), axis=0)


def collar_top(Jw):
    a, b = Jw[JE[:, 0]], Jw[JE[:, 1]]
    keep = (cyl(a)[2] < COLLAR_RHO) & (cyl(b)[2] < COLLAR_RHO)
    t = np.linspace(0.0, 1.0, 9)
    pts = (a[keep][:, None, :] * (1 - t)[None, :, None] + b[keep][:, None, :] * t[None, :, None]).reshape(-1, 3)
    h, th, _r, _rd = cyl(pts)
    return angle_table(th, h)


TOP, top_empty = collar_top(J0)
FLIP = 1.0


def tri_normals(Jw, T):
    a, b, c = Jw[T[:, 0]], Jw[T[:, 1]], Jw[T[:, 2]]
    return np.cross(b - a, c - a) * FLIP


nA = tri_normals(J0, JT)
cen = J0[JT].mean(1)
ch, cth, crho, crad = cyl(cen)
bandf = (crho < COLLAR_RHO) & (ch > at_angle(TOP, cth) - 0.06)
nn = nA / np.maximum(np.linalg.norm(nA, axis=1, keepdims=True), 1e-15)
radial = np.einsum("ij,ij->i", nn[bandf], crad[bandf])
facing = np.abs(radial) > 0.5
OUT_FRAC = float((radial[facing] > 0).mean()) if facing.any() else float("nan")
if OUT_FRAC < 0.5:
    FLIP = -1.0
log("collar's faces outward fraction %.3f, flip %s" % (OUT_FRAC, FLIP < 0))

h0, th0, rho0, rad0 = cyl(J0)
RW0 = (J0 - AX_O) @ AX_W                    # signed distance from the centre-front plane, + his left
BELOW = at_angle(TOP, th0) - h0
BAND = (BELOW <= DEPTH) & (BELOW >= -0.01) & (rho0 < BAND_RHO)
band_tris = np.nonzero(BAND[JT].all(1))[0]
OPEN_E = EV[EFC == 1]
TOPE = OPEN_E[BAND[OPEN_E].all(1) & (BELOW[OPEN_E] <= 0.004).all(1) & (rho0[OPEN_E] < COLLAR_RHO).all(1)]
REST_TOP_LEN = np.linalg.norm(J0[TOPE[:, 0]] - J0[TOPE[:, 1]], axis=1)
BAND_E = EV[BAND[EV].all(1)]
REST_BAND_LEN = np.linalg.norm(J0[BAND_E[:, 0]] - J0[BAND_E[:, 1]], axis=1)
log("collar top above neck_01 %.1f..%.1f mm; band points %d, triangles %d; top edge %d edges, %.3f m" % (
    1000 * TOP.min(), 1000 * TOP.max(), int(BAND.sum()), len(band_tris), len(TOPE), float(REST_TOP_LEN.sum())))

# ---- THE ZIP LINE: from the top edge at the front down the edges nearest the centre-front plane ------------------------
top_pts = np.unique(TOPE)
front_top = top_pts[np.abs(th0[top_pts]) < 30.0]
c0 = int(front_top[np.argmin(np.abs(RW0[front_top]))])
chain = [c0]
arc = [0.0]
while True:
    cur = chain[-1]
    down = [n for n in NBR[cur] if BELOW[n] > BELOW[cur] + 0.001 and n not in chain]
    if not down:
        break
    nxt = min(down, key=lambda n: abs(RW0[n]) + 0.2 * abs(RW0[n] - RW0[cur]))
    step = float(np.linalg.norm(J0[nxt] - J0[cur]))
    if arc[-1] + step > OPEN and (arc[-1] + step - OPEN) > (OPEN - arc[-1]):
        break
    chain.append(nxt)
    arc.append(arc[-1] + step)
    if arc[-1] >= OPEN:
        break
chain = np.array(chain)
K = len(chain) - 1                        # points split: all but the slider
SLIDER = int(chain[-1])
D_S = float(BELOW[SLIDER])
chain_edges = [EDGE_OF[(min(a, b), max(a, b))] for a, b in zip(chain[:-1], chain[1:])]
log("zip line: points %s, length %.1f mm (asked %.1f), off the centre plane at most %.2f mm, slider %.1f mm below the "
    "collar's top, edges' face counts %s, materials round it %s" % (
        chain.tolist(), 1000 * arc[-1], 1000 * OPEN, 1000 * float(np.abs(RW0[chain]).max()), 1000 * D_S,
        EFC[chain_edges].tolist(),
        sorted({mat_names[jme.polygons[p].material_index] for p in range(len(POLY_V)) if set(POLY_V[p]) & set(chain.tolist())})))
assert (EFC[chain_edges] == 2).all(), "a zip-line edge is not between two faces"
assert COINCIDENT == 0, "coincident points: the split would need welding first"

# which side of the zip line each face touching it lies on (his left +1, his right -1)
POLY_SIDE = np.zeros(len(POLY_V), int)
SPLIT_SET = set(chain[:-1].tolist())
for p, vs in enumerate(POLY_V):
    if SPLIT_SET & set(vs):
        ref = np.mean([RW0[v] for v in vs if v in SPLIT_SET or v == SLIDER])
        POLY_SIDE[p] = 1 if (RW0[vs].mean() - ref) > 0 else -1
for v in chain[:-1]:
    sides = {POLY_SIDE[p] for p, vs in enumerate(POLY_V) if v in vs}
    assert sides == {1, -1}, "zip-line point %d has faces on one side only" % v

# the opened mesh as arrays: the copies appended, his right's faces take them
SRC = np.concatenate([np.arange(NV), chain[:-1]])
DUP = {int(v): NV + j for j, v in enumerate(chain[:-1])}
JT2 = JT.copy()
for t in range(len(JT2)):
    if POLY_SIDE[JTP[t]] < 0:
        JT2[t] = [DUP.get(int(v), int(v)) for v in JT2[t]]
SIDE2 = np.where(RW0[SRC] >= 0, 1, -1)
SIDE2[chain[:-1]] = 1
SIDE2[NV:] = -1
REMAPPED_CORNERS = int((JT2 != JT).sum())
RHO_TIP = float(rho0[c0])
# the edges of the opened mesh: an edge of his right's faces ends at the copies; a split edge is there twice
EDGE_SIDE = {}
for p, vs in enumerate(POLY_V):
    for a, b in zip(vs, vs[1:] + vs[:1]):
        EDGE_SIDE.setdefault((min(a, b), max(a, b)), set()).add(int(POLY_SIDE[p]))
CHAIN_KEYS = {(min(a, b), max(a, b)) for a, b in zip(chain[:-1], chain[1:])}


def after_edges(E):
    """Edges of the input (pairs of points) as edges of the opened mesh, and which input edge each one was."""
    out, was = [], []
    for k, (a, b) in enumerate(E):
        key = (min(a, b), max(a, b))
        if key in CHAIN_KEYS:
            out += [(a, b), (DUP.get(int(a), a), DUP.get(int(b), b))]
            was += [k, k]
        elif -1 in EDGE_SIDE.get(key, {0}):
            out.append((DUP.get(int(a), a), DUP.get(int(b), b)))
            was.append(k)
        else:
            out.append((a, b))
            was.append(k)
    return np.array(out, int), np.array(was, int)


TOPE2, _w = after_edges(TOPE)
REST_TOP_LEN2 = REST_TOP_LEN[_w]
BAND_E2, _w = after_edges(BAND_E)
REST_BAND_LEN2 = REST_BAND_LEN[_w]


def opened_rest(gap):
    """The opened jacket at rest (world), its points as SRC with SIDE2: each side turned round the neck's line."""
    X = J0[SRC]
    if gap <= 0:
        return X.copy(), 0.0
    a0 = half_angle_for_gap(gap, RHO_TIP)
    d = BELOW[SRC]
    V = smoothstep((D_S - d) / D_S) if TAPER == "smooth" else np.clip((D_S - d) / D_S, 0.0, 1.0)
    th = th0[SRC]
    F = smoothstep((REACH - np.abs(th)) / REACH)
    M = smoothstep((COLLAR_RHO + 0.02 - rho0[SRC]) / 0.02)
    ang = SIDE2 * a0 * V * F * M
    m = ang != 0.0                      # points not turned stay bit for bit
    X[m] = turn_round_neck(X[m], ang[m])
    return X, a0


# ---- THE POSES: each jacket point's skinning as a linear map, the skin's posed triangles -------------------------------
def set_co(co):
    jme.vertices.foreach_set("co", np.ascontiguousarray(co).ravel())
    jme.update()


POSE = {}
DELTA = 0.01
for name, pitch, yaw in POSES:
    set_pose(pitch, yaw)
    gp, gy = game_angles()
    base = evaluated_world(jacket)
    L = np.zeros((NV, 3, 3))
    for k in range(3):
        co = CO0.copy()
        co[:, k] += DELTA
        set_co(co)
        bpy.context.view_layer.update()
        L[:, :, k] = (evaluated_world(jacket) - base) / DELTA
    set_co(CO0)
    bpy.context.view_layer.update()
    Lw = np.einsum("nij,jk->nik", L, A3i)          # posed world per rest-world move
    skin = {}
    for k, s in SKIN.items():
        Pw = evaluated_world(s["obj"])
        skin[k] = {"P": Pw, "bvh": bvh_of(Pw, s["T"])}
    POSE[name] = {"pitch": pitch, "yaw": yaw, "game_pitch": gp, "game_yaw": gy, "base": base, "Lw": Lw, "skin": skin}
    log("pose %-15s game pitch %6.2f yaw %7.2f" % (name, gp, gy))
set_pose(0, 0)


def posed(name, Xr):
    """The jacket (opened or not) posed: each point as its source's skinning of its own rest place."""
    P = POSE[name]
    return P["base"][SRC[:len(Xr)]] + np.einsum("nij,nj->ni", P["Lw"][SRC[:len(Xr)]], Xr - J0[SRC[:len(Xr)]])


def crossings(J, T, skin):
    bb = bvh_of(J, T)
    out = {}
    for k, s in skin.items():
        out[k] = np.array(s["bvh"].overlap(bb), int).reshape(-1, 2)
    return out


def count(cr):
    return {k: int(len(np.unique(v[:, 0]))) if len(v) else 0 for k, v in cr.items()}


BAND_T1, BAND_T2 = JT[band_tris], JT2[band_tris]


ZIP_E2 = np.array([k for k, (a, b) in enumerate(BAND_E2)
                   if (min(SRC[a], SRC[b]), max(SRC[a], SRC[b])) in CHAIN_KEYS], int)


def measure(gap):
    Xr, a0 = opened_rest(gap)
    res = {}
    for name, *_ in POSES:
        J = posed(name, Xr)
        res[name] = count(crossings(J, BAND_T2, POSE[name]["skin"]))
    st = np.linalg.norm(Xr[BAND_E2[:, 0]] - Xr[BAND_E2[:, 1]], axis=1) / REST_BAND_LEN2
    return res, a0, {"zip_edge_stretch_max_rest": round(float(st[ZIP_E2].max()), 3),
                     "band_stretch_max_rest": round(float(st.max()), 3), "band_squeeze_min_rest": round(float(st.min()), 3)}


BEFORE = {}
for name, *_ in POSES:
    BEFORE[name] = count(crossings(posed(name, J0), BAND_T1, POSE[name]["skin"]))
log("before (the input): skin triangles crossing the collar's band", json.dumps(BEFORE))

SWEEP = []
for g in sorted(set(GAPS + ([GAP_FIXED] if GAP_FIXED > 0 else []))):
    res, a0, st = measure(g)
    tot = sum(sum(v.values()) for v in res.values())
    SWEEP.append({"gap_cm": round(100 * g, 2), "tip_turn_deg": round(math.degrees(a0), 2), "per_pose": res,
                  "total_body_plus_face": tot, "clears_all": tot == 0, **st})
    log("gap %.1f cm (tips turned %.1f deg): %s total %d %s" % (100 * g, math.degrees(a0), json.dumps(res), tot, json.dumps(st)))
if GAP_FIXED > 0:
    GAP, HOW = GAP_FIXED, "given (--gap-cm)" + ("" if any(s["clears_all"] for s in SWEEP) else "; NO measured gap clears every pose")
else:
    clear = [s for s in SWEEP if s["clears_all"]]
    if clear:
        GAP, HOW = clear[0]["gap_cm"] / 100.0, "the least measured gap that clears every pose"
    else:
        best = min(SWEEP, key=lambda s: (s["total_body_plus_face"], s["gap_cm"]))
        GAP, HOW = best["gap_cm"] / 100.0, "NO measured gap clears every pose: the gap with the fewest crossings"
log("GAP %.1f cm: %s" % (100 * GAP, HOW))

# ---- THE CHECKS AT THE CHOSEN GAP --------------------------------------------------------------------------------------
X2, A0 = opened_rest(GAP)
MOVE = np.linalg.norm(X2 - J0[SRC], axis=1)
MOVED = MOVE > 1e-7
rho2 = cyl(X2)[2]
CHECK = {}
for name, *_ in POSES:
    P = POSE[name]
    row = {"pitch_down_deg": P["pitch"], "turn_left_deg": P["yaw"], "game_pitch_down_deg": round(P["game_pitch"], 2),
           "game_yaw_deg": round(P["game_yaw"], 2)}
    for label, Xr, T, TB, TE, TL, BE, BL in (("before", J0, JT, BAND_T1, TOPE, REST_TOP_LEN, BAND_E, REST_BAND_LEN),
                                             ("after", X2, JT2, BAND_T2, TOPE2, REST_TOP_LEN2, BAND_E2, REST_BAND_LEN2)):
        J = posed(name, Xr)
        crb = crossings(J, TB, P["skin"])
        crw = crossings(J, T, P["skin"])
        top_st = np.linalg.norm(J[TE[:, 0]] - J[TE[:, 1]], axis=1) / TL
        band_st = np.linalg.norm(J[BE[:, 0]] - J[BE[:, 1]], axis=1) / BL
        row[label] = {"band_crossing_skin_triangles": count(crb),
                      "band_crossed_collar_triangles": int(len(np.unique(np.concatenate([v[:, 1] for v in crb.values()])))),
                      "whole_jacket_crossing_skin_triangles": count(crw),
                      "top_edge_stretch_max": round(float(top_st.max()), 3), "top_edge_squeeze_min": round(float(top_st.min()), 3),
                      "band_edge_stretch_max": round(float(band_st.max()), 3), "band_edge_squeeze_min": round(float(band_st.min()), 3)}
        P[label + "_J"] = J
        P[label + "_cross"] = crb
        if label == "after" and name == "rest":
            for what, k in (("stretched", int(np.argmax(band_st))), ("squeezed", int(np.argmin(band_st)))):
                a, b = BE[k]
                row["band_edge_most_%s" % what] = {
                    "ratio": round(float(band_st[k]), 3), "rest_length_mm": round(1000 * float(BL[k]), 1),
                    "ends_angle_deg": [round(float(th0[SRC[a]]), 1), round(float(th0[SRC[b]]), 1)],
                    "ends_depth_below_top_mm": [round(1000 * float(BELOW[SRC[a]]), 1), round(1000 * float(BELOW[SRC[b]]), 1)],
                    "ends_moved_mm": [round(1000 * float(MOVE[a]), 1), round(1000 * float(MOVE[b]), 1)]}
                log("band edge most %s at rest" % what, json.dumps(row["band_edge_most_%s" % what]))
    row["clears"] = sum(row["after"]["band_crossing_skin_triangles"].values()) == 0
    CHECK[name] = row
    log("check %-15s before %s after %s whole jacket after %s top stretch %.3f squeeze %.3f" % (
        name, row["before"]["band_crossing_skin_triangles"], row["after"]["band_crossing_skin_triangles"],
        row["after"]["whole_jacket_crossing_skin_triangles"], row["after"]["top_edge_stretch_max"], row["after"]["top_edge_squeeze_min"]))

# at rest: the opened edges against the neck, the V's width, nothing nearer the neck's line or the skin
REST_SKIN = {k: POSE["rest"]["skin"][k] for k in SKIN}
body_bvh = REST_SKIN["body"]["bvh"]


def signed_to_skin(X):
    out = np.zeros(len(X))
    for i, x in enumerate(X):
        loc, nrm, _ix, dist = body_bvh.find_nearest(Vector(x), 0.5)
        out[i] = np.inf if loc is None else (dist if (Vector(x) - loc).dot(nrm) >= 0 else -dist)
    return out


edge_pts = np.concatenate([chain[:-1], NV + np.arange(K)])
edge_gap = signed_to_skin(X2[edge_pts])
V_ROWS = []
for j, v in enumerate(chain[:-1]):
    V_ROWS.append({"point": int(v), "depth_below_top_mm": round(1000 * float(BELOW[v]), 1),
                   "zip_length_from_top_mm": round(1000 * arc[j], 1),
                   "v_width_mm": round(1000 * float(np.linalg.norm(X2[v] - X2[NV + j])), 1),
                   "his_left_edge_to_skin_mm": round(1000 * float(edge_gap[j]), 1),
                   "his_right_edge_to_skin_mm": round(1000 * float(edge_gap[K + j]), 1)})
mv = np.nonzero(MOVED)[0]
skin_before = signed_to_skin(J0[SRC[mv]])
skin_after = signed_to_skin(X2[mv])
REST = {
    "v_down_the_split": V_ROWS,
    "top_tips_apart_mm": round(1000 * float(np.linalg.norm(X2[c0] - X2[NV])), 1),
    "opened_edges_to_skin_mm": {"least": round(1000 * float(edge_gap.min()), 1), "most": round(1000 * float(edge_gap.max()), 1),
                                "median": round(1000 * float(np.median(edge_gap)), 1)},
    "points_moved": int(MOVED.sum()), "points_moved_over_1mm": int((MOVE > 1e-3).sum()),
    "largest_move_mm": round(1000 * float(MOVE.max()), 1),
    "moved_angle_round_neck_deg": [round(float(th0[SRC][MOVED].min()), 1), round(float(th0[SRC][MOVED].max()), 1)],
    "moved_depth_below_top_mm": [round(1000 * float(BELOW[SRC][MOVED].min()), 1), round(1000 * float(BELOW[SRC][MOVED].max()), 1)],
    "nearer_the_neck_line_most_mm": round(-1000 * float(min(0.0, (rho2 - rho0[SRC])[MOVED].min())), 4),
    "moved_points_to_skin_least_mm_before_after": [round(1000 * float(skin_before.min()), 2), round(1000 * float(skin_after.min()), 2)],
    "moved_points_nearer_the_skin_by_most_mm": round(1000 * float(max(0.0, (skin_before - skin_after).max())), 2),
    "moved_points_inside_skin_after": int((skin_after < 0).sum()),
}
log("rest", json.dumps({k: v for k, v in REST.items() if k != "v_down_the_split"}))
for r in V_ROWS:
    log("  V", json.dumps(r))


# ---- WHAT THE OPENING SHOWS AT REST ------------------------------------------------------------------------------------
def read_grey(path):
    im = bpy.data.images.load(path)
    im.colorspace_settings.name = "Non-Color"
    w, h = im.size
    px = np.array(im.pixels[:], np.float32).reshape(h, w, 4)[::-1]     # top row first
    return px[..., :3].max(-1)


def wrap(x, lo, hi):
    size = hi - lo
    while x < lo:
        x += size
    while x > hi:
        x -= size
    return x


def sample(im, u, v_engine):
    h, w = im.shape
    x = math.floor(wrap((u + 1e-4) * w, 0.0, w - 1.0))
    y = math.floor(wrap((v_engine + 1e-4) * h, 0.0, h - 1.0))
    return float(im[y, x])


bme = body.data
BUV = {}
uvl = bme.uv_layers.get("DiffuseUV") or bme.uv_layers.active
uva = np.zeros(len(bme.loops) * 2)
uvl.data.foreach_get("uv", uva)
uva = uva.reshape(-1, 2)
blv = np.zeros(len(bme.loops), int)
bme.loops.foreach_get("vertex_index", blv)
for li, vi in enumerate(blv):
    BUV.setdefault(int(vi), []).append(uva[li])
# the head mesh's own UVs: a head point is sampled at its nearest head-mesh point (the game's mesh), distance recorded
fme = face.data
fuvl = fme.uv_layers.get("DiffuseUV") or fme.uv_layers.active
fua = np.zeros(len(fme.loops) * 2)
fuvl.data.foreach_get("uv", fua)
fua = fua.reshape(-1, 2)
flv = np.zeros(len(fme.loops), int)
fme.loops.foreach_get("vertex_index", flv)
FUV = {}
for li, vi in enumerate(flv):
    FUV.setdefault(int(vi), []).append(fua[li])
FW = SKIN["face"]["W0"]
fskin = np.unique(SKIN["face"]["T"])
fkd = KDTree(len(fskin))
for k_, v_ in enumerate(fskin):
    fkd.insert(FW[v_], k_)
fkd.balance()
BMAP = read_grey(BODY_MAP) if BODY_MAP else None
HMAP = read_grey(HEAD_MAP) if HEAD_MAP else None
HEAD_SHRINK_MM = None
if HEAD_MAP:
    rec = os.path.join(os.path.dirname(HEAD_MAP), "head-map-record.json")
    if os.path.exists(rec):
        HEAD_SHRINK_MM = json.load(open(rec, encoding="utf-8")).get("MaxShrinkDistance_mm")

BW = REST_SKIN["body"]["P"]
BT = SKIN["body"]["T"]
bn = np.zeros((len(BW), 3))
tn = np.cross(BW[BT[:, 1]] - BW[BT[:, 0]], BW[BT[:, 2]] - BW[BT[:, 0]])
for k in range(3):
    np.add.at(bn, BT[:, k], tn)
bn /= np.maximum(np.linalg.norm(bn, axis=1, keepdims=True), 1e-15)
cand = np.unique(BT)
hc, thc, rhoc, _ = cyl(BW[cand])
below_c = at_angle(TOP, thc) - hc
moved_th = np.abs(th0[SRC][MOVED])
cand_sel = (below_c > 0.0) & (np.abs(thc) <= (moved_th.max() + 10.0 if len(moved_th) else 0.0)) & (rhoc < BAND_RHO) & (below_c < D_S + 0.03)
cand, below_c, thc = cand[cand_sel], below_c[cand_sel], thc[cand_sel]
jb1, jb2 = bvh_of(J0, JT), bvh_of(X2, JT2)


def seen(x, n, d, cloth):
    if n @ d <= 0.05:
        return False
    o = Vector(x + 0.0005 * n)
    dv = Vector(d)
    if cloth.ray_cast(o, dv, 1.0)[0] is not None:
        return False
    return body_bvh.ray_cast(o, dv, 1.0)[0] is None


EXPOSED = np.zeros(len(cand), bool)
by_view = {}
for vn, d in VIEWS.items():
    d = np.array(d) / np.linalg.norm(d)
    newly = np.array([(not seen(BW[v], bn[v], d, jb1)) and seen(BW[v], bn[v], d, jb2) for v in cand], bool)
    by_view[vn] = int(newly.sum())
    EXPOSED |= newly
ex = cand[EXPOSED]
ex_below = below_c[EXPOSED]
rows = []
n_body = n_head = n_cut_all = n_cut_any = n_shrunk = 0
shrinks = []
for v, b in zip(ex, ex_below):
    uvs = BUV.get(int(v), [])
    in_body = bool(uvs) and all(u[0] >= 1.0 for u in uvs)
    r = {"point": int(v), "depth_below_top_mm": round(1000 * float(b), 1), "mesh": "body" if in_body else "head"}
    if in_body:
        n_body += 1
        if BMAP is not None:
            vals = [sample(BMAP, u[0], 1.0 - u[1]) for u in uvs]
            r["body_map"] = round(min(vals), 3)
            n_cut_all += all(x <= 0.1 for x in vals)
            n_cut_any += any(x <= 0.1 for x in vals)
    else:
        n_head += 1
        _co, fk, fdist = fkd.find(Vector(BW[v]))
        fv = int(fskin[fk])
        r["head_mesh_point"], r["head_mesh_point_away_mm"] = fv, round(1000 * fdist, 2)
        r["full_body_vs_head_mesh_uv_diff"] = round(float(min(np.abs(np.array(a) - np.array(b)).max()
                                                            for a in uvs for b in FUV.get(fv, []))), 5) if uvs and FUV.get(fv) else None
        if HMAP is not None:
            vals = [sample(HMAP, u[0], 1.0 - u[1]) for u in FUV.get(fv, uvs)]
            val = min(vals)
            r["head_map"] = round(val, 3)
            if val < 0.9 and HEAD_SHRINK_MM is not None:
                s = HEAD_SHRINK_MM * min(1.0, 1.0 - (val - 0.1) / 0.8)
                r["head_shrink_mm"] = round(s, 2)
                shrinks.append(s)
                n_shrunk += 1
    rows.append(r)
EXPOSE = {
    "views": {k: [round(x, 3) for x in v] for k, v in VIEWS.items()},
    "candidates": int(len(cand)), "newly_seen_by_view": by_view, "newly_seen_any_view": int(len(ex)),
    "depth_below_top_mm": [round(1000 * float(ex_below.min()), 1), round(1000 * float(ex_below.max()), 1)] if len(ex) else None,
    "angle_round_neck_deg": [round(float(thc[EXPOSED].min()), 1), round(float(thc[EXPOSED].max()), 1)] if len(ex) else None,
    "body_points": n_body, "head_points": n_head,
    "body_points_cut_by_body_map_all_uvs": n_cut_all, "body_points_cut_by_body_map_any_uv": n_cut_any,
    "head_points_shrunk_by_head_map": n_shrunk,
    "head_shrink_mm_most": round(max(shrinks), 2) if shrinks else 0.0,
    "body_map": BODY_MAP, "head_map": HEAD_MAP, "head_max_shrink_mm": HEAD_SHRINK_MM,
    "points": rows,
}
log("exposed", json.dumps({k: v for k, v in EXPOSE.items() if k != "points"}))

# the collar's inside faces newly seen (one-sided material: seen from inside, the cloth is not drawn)
band_cen1 = J0[BAND_T1].mean(1)
band_cen2 = X2[BAND_T2].mean(1)
bn1 = tri_normals(J0, BAND_T1)
bn2 = tri_normals(X2, BAND_T2)
bn1 /= np.maximum(np.linalg.norm(bn1, axis=1, keepdims=True), 1e-15)
bn2 /= np.maximum(np.linalg.norm(bn2, axis=1, keepdims=True), 1e-15)
area2 = 0.5 * np.linalg.norm(np.cross(X2[BAND_T2[:, 1]] - X2[BAND_T2[:, 0]], X2[BAND_T2[:, 2]] - X2[BAND_T2[:, 0]]), axis=1)
INSIDE = {}
for vn, d in VIEWS.items():
    d = np.array(d) / np.linalg.norm(d)
    cnt = []
    for cen_, nrm_, cloth in ((band_cen1, bn1, jb1), (band_cen2, bn2, jb2)):
        c = 0
        a = 0.0
        for i in range(len(cen_)):
            if nrm_[i] @ d >= -0.05:
                continue
            o = Vector(cen_[i] + 0.0005 * d)
            if cloth.ray_cast(o, Vector(d), 1.0)[0] is None and body_bvh.ray_cast(o, Vector(d), 1.0)[0] is None:
                c += 1
                a += float(area2[i]) if cloth is jb2 else 0.0
        cnt.append(c)
    INSIDE[vn] = {"before": cnt[0], "after": cnt[1]}
log("collar inside faces seen (triangles), before/after", json.dumps(INSIDE))


# ---- THE FILE ----------------------------------------------------------------------------------------------------------
def plain(name):
    return re.sub(r"\.\d{3}$", "", name) if name else name


def snapshot(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    arm = next(o for o in new if o.type == "ARMATURE")
    mo = max((o for o in new if o.type == "MESH"), key=lambda o: len(o.data.vertices))
    me = mo.data
    nv, nl = len(me.vertices), len(me.loops)
    co = np.zeros(nv * 3)
    me.vertices.foreach_get("co", co)
    gname = {g.index: g.name for g in mo.vertex_groups}
    wts = [dict() for _ in range(nv)]
    for v in me.vertices:
        for g in v.groups:
            wts[v.index][gname[g.group]] = g.weight
    uvs = {}
    for lay in me.uv_layers:
        a = np.zeros(nl * 2)
        lay.data.foreach_get("uv", a)
        uvs[lay.name] = a
    mi = np.zeros(len(me.polygons), int)
    me.polygons.foreach_get("material_index", mi)
    lv = np.zeros(nl, int)
    me.loops.foreach_get("vertex_index", lv)
    snap = {"arm_name": plain(arm.name), "mesh_name": plain(mo.name),
            "counts": [nv, len(me.edges), len(me.polygons), nl], "co": co.reshape(-1, 3),
            "mesh_matrix": np.array(mo.matrix_world), "arm_matrix": np.array(arm.matrix_world),
            "weights": wts, "groups": sorted(gname.values()), "uvs": uvs, "uv_names": [u.name for u in me.uv_layers],
            "materials": [plain(m.name) if m else None for m in me.materials], "mi": mi, "lv": lv,
            "bones": [b.name for b in arm.data.bones], "parents": [b.parent.name if b.parent else None for b in arm.data.bones],
            "bone_matrices": np.array([np.array(arm.matrix_world @ b.matrix_local) for b in arm.data.bones]),
            "shape_keys": [kb.name for kb in me.shape_keys.key_blocks] if me.shape_keys else []}
    for o in new:
        bpy.data.objects.remove(o, do_unlink=True)
    return snap


OUT_FBX = os.path.join(OUT, os.path.basename(JACKET))
VERIFY = None
SPLIT_INFO = None
if WRITE:
    assert jarm.name == JARM_NAME and jacket.name == JACKET_NAME
    set_pose(0, 0)
    bm = bmesh.new()
    bm.from_mesh(jme)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    edges = [bm.edges.get((bm.verts[int(a)], bm.verts[int(b)])) for a, b in zip(chain[:-1], chain[1:])]
    bmesh.ops.split_edges(bm, edges=edges)
    bm.verts.index_update()
    bm.verts.ensure_lookup_table()
    nv_new = len(bm.verts)
    # each copy's source (same place) and each split point's side from its faces (faces keep their indices)
    real_src = np.arange(nv_new)
    real_side = np.zeros(nv_new, int)
    for i in range(NV, nv_new):
        co_ = np.array(bm.verts[i].co)
        j = int(np.argmin(np.linalg.norm(CO0[chain[:-1]] - co_, axis=1)))
        real_src[i] = int(chain[j])
    for i in list(chain[:-1]) + list(range(NV, nv_new)):
        s = {int(POLY_SIDE[f.index]) for f in bm.verts[int(i)].link_faces}
        assert len(s) == 1, "a split point still has faces on both sides"
        real_side[int(i)] = s.pop()
    # model index for each real point: originals keep theirs unless the original took his right's faces
    perm = np.arange(nv_new)
    for i in range(NV, nv_new):
        j = list(chain[:-1]).index(real_src[i])
        if real_side[i] > 0:          # the copy took his left: swap with the model's
            perm[i], perm[int(chain[j])] = int(chain[j]), NV + j
        else:
            perm[i] = NV + j
    newco = CO0[real_src] + (X2[perm] - J0[real_src]) @ A3i.T
    for i, v in enumerate(bm.verts):
        v.co = Vector(newco[i])
    bm.to_mesh(jme)
    bm.free()
    jme.update()
    bpy.context.view_layer.update()
    # the real mesh posed by Blender against the model's linear skinning
    model_err = {}
    for name in ("rest", "down25", "down20_left45"):
        P = POSE[name]
        set_pose(P["pitch"], P["yaw"])
        model_err[name] = float(np.abs(evaluated_world(jacket) - P["after_J"][perm]).max())
    set_pose(0, 0)
    SPLIT_INFO = {"vertices_after": nv_new, "copies": nv_new - NV, "copies_on_his_right": int((real_side[NV:] < 0).sum()),
                  "blender_posing_vs_model_largest_m": model_err}
    log("split", json.dumps(SPLIT_INFO))
    bpy.ops.object.select_all(action="DESELECT")
    jarm.select_set(True)
    jacket.select_set(True)
    bpy.context.view_layer.objects.active = jarm
    bpy.ops.export_scene.fbx(filepath=OUT_FBX, use_selection=True, object_types={"ARMATURE", "MESH"}, add_leaf_bones=False,
                             mesh_smooth_type="OFF", use_tspace=True, colors_type="LINEAR", bake_anim=False)
    log("wrote", OUT_FBX)
    A_ = snapshot(JACKET)
    B_ = snapshot(OUT_FBX)
    nva = A_["counts"][0]
    unchanged = np.nonzero(MOVE[perm[:nva]] <= 1e-7)[0] if B_["counts"][0] >= nva else np.array([], int)
    wdiff_orig = max((abs(A_["weights"][i].get(g, 0.0) - B_["weights"][i].get(g, 0.0))
                      for i in range(nva) for g in set(A_["weights"][i]) | set(B_["weights"][i])), default=0.0)
    wdiff_copy = max((abs(B_["weights"][int(real_src[i])].get(g, 0.0) - B_["weights"][i].get(g, 0.0))
                      for i in range(nva, B_["counts"][0]) for g in set(B_["weights"][int(real_src[i])]) | set(B_["weights"][i])), default=0.0)
    lv_changed = np.nonzero(A_["lv"] != B_["lv"])[0] if len(A_["lv"]) == len(B_["lv"]) else None
    want = CO0[real_src] + (X2[perm] - J0[real_src]) @ A3i.T
    rot = {}
    if A_["bones"] == B_["bones"]:
        na = A_["bone_matrices"][:, :3, :3] / np.linalg.norm(A_["bone_matrices"][:, :3, :3], axis=1, keepdims=True)
        nb = B_["bone_matrices"][:, :3, :3] / np.linalg.norm(B_["bone_matrices"][:, :3, :3], axis=1, keepdims=True)
        for n, ra, rb in zip(A_["bones"], na, nb):
            rot[n] = math.degrees(Matrix(ra.tolist()).to_quaternion().rotation_difference(Matrix(rb.tolist()).to_quaternion()).angle)
    wb = {g for w in A_["weights"] for g, x in w.items() if x > 0}
    VERIFY = {
        "counts_vertices_edges_faces_corners": [A_["counts"], B_["counts"]],
        "vertices_added": B_["counts"][0] - A_["counts"][0], "edges_added": B_["counts"][1] - A_["counts"][1],
        "faces_and_corners_equal": A_["counts"][2:] == B_["counts"][2:],
        "unchanged_points": int(len(unchanged)),
        "unchanged_points_largest_difference_m": float(np.abs(A_["co"][unchanged] - B_["co"][unchanged]).max()) if len(unchanged) else None,
        "all_points_largest_difference_from_intended_m": float(np.abs(B_["co"] - want).max()),
        "original_points_weights_largest_difference": float(wdiff_orig),
        "copies_weights_largest_difference_from_source": float(wdiff_copy),
        "weights_pairs": [sum(len(w) for w in A_["weights"]), sum(len(w) for w in B_["weights"])],
        "weight_groups_equal": A_["groups"] == B_["groups"],
        "uv_layers": [A_["uv_names"], B_["uv_names"]],
        "uv_largest_difference": max((float(np.abs(A_["uvs"][n] - B_["uvs"][n]).max()) for n in A_["uv_names"] if n in B_["uvs"]), default=None),
        "material_slots": [A_["materials"], B_["materials"]], "material_slots_equal": A_["materials"] == B_["materials"],
        "face_materials_equal": bool(np.array_equal(A_["mi"], B_["mi"])),
        "corners_moved_to_a_copy": int(len(lv_changed)) if lv_changed is not None else None,
        "corners_moved_all_to_copies_of_their_point": bool(lv_changed is not None and all(
            B_["lv"][c] >= nva and int(real_src[B_["lv"][c]]) == A_["lv"][c] for c in lv_changed)),
        "bones": [len(A_["bones"]), len(B_["bones"])],
        "bone_names_and_parents_equal": A_["bones"] == B_["bones"] and A_["parents"] == B_["parents"],
        "bone_rest_positions_largest_difference_mm": float(1000 * np.linalg.norm(A_["bone_matrices"][:, :3, 3] - B_["bone_matrices"][:, :3, 3], axis=1).max()) if A_["bones"] == B_["bones"] else None,
        "weighted_bones_rest_rotations_largest_difference_deg": max((d for n, d in rot.items() if n in wb), default=None),
        "object_names": [[A_["arm_name"], A_["mesh_name"]], [B_["arm_name"], B_["mesh_name"]]],
        "shape_keys": [A_["shape_keys"], B_["shape_keys"]],
    }
    VERIFY["pass"] = bool(VERIFY["vertices_added"] == K and VERIFY["faces_and_corners_equal"]
                          and VERIFY["unchanged_points_largest_difference_m"] == 0.0
                          and VERIFY["original_points_weights_largest_difference"] == 0.0
                          and VERIFY["copies_weights_largest_difference_from_source"] == 0.0
                          and VERIFY["weight_groups_equal"] and VERIFY["uv_largest_difference"] == 0.0
                          and VERIFY["material_slots_equal"] and VERIFY["face_materials_equal"]
                          and VERIFY["corners_moved_all_to_copies_of_their_point"]
                          and VERIFY["bone_names_and_parents_equal"] and VERIFY["all_points_largest_difference_from_intended_m"] < 1e-5)
    log("VERIFY", json.dumps(VERIFY))

# ---- THE PREVIEW: front and three-quarter, at rest and 25 down, before and after --------------------------------------
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"], "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"], "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"], "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."], "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."], "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"], "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"], "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."], "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."], "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."], "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"], "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."], "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."], "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"], "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."], "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."], "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."], "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."], " ": ["....."] * 7,
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
}


def text(img, s, x, y, scale=3, colour=(20, 20, 20)):
    for ch in s.upper():
        g = FONT.get(ch, FONT[" "])
        for r, line in enumerate(g):
            for c, on in enumerate(line):
                if on == "#":
                    img[y + r * scale:y + (r + 1) * scale, x + c * scale:x + (c + 1) * scale] = colour
        x += 6 * scale


def write_png(path, a):
    raw = b"".join(b"\x00" + row.tobytes() for row in a)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", a.shape[1], a.shape[0], 8, 2, 0, 0, 0))
                 + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


PW, PH, MPP = 560, 640, 0.0005
CEN = AX_O + 0.03 * AX_A
SKIN_RGB, CLOTH_RGB = np.array([0.80, 0.66, 0.58]), np.array([0.45, 0.48, 0.53])
MOVE_RGB, CROSS_RGB = np.array([0.95, 0.60, 0.15]), np.array([0.85, 0.10, 0.75])
SHOWN_RGB, CUT_RGB, SHRUNK_RGB = np.array([0.20, 0.70, 0.30]), np.array([0.90, 0.10, 0.10]), np.array([0.95, 0.85, 0.20])


def panel(d, skin_pts, skin_cols, Jw, Tj, jcols):
    img = np.full((PH, PW, 3), 245, np.uint8)
    zb = np.full((PH, PW), np.inf)
    d = np.asarray(d, float) / np.linalg.norm(d)
    right = np.cross(np.array([0.0, 0.0, 1.0]), d)
    right /= np.linalg.norm(right)
    up = np.cross(d, right)
    light = d + np.array([0.0, 0.0, 0.6])
    light /= np.linalg.norm(light)

    def put(X, T, cols):
        x = ((X - CEN) @ right) / MPP + PW / 2.0
        y = PH * 0.42 - ((X - CEN) @ up) / MPP
        z = -(X @ d)
        a, b, c = X[T[:, 0]], X[T[:, 1]], X[T[:, 2]]
        n = np.cross(b - a, c - a)
        n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-15)
        shade = 0.35 + 0.65 * np.abs(n @ light)
        rgb = np.clip(cols * shade[:, None] * 255.0, 0, 255).astype(np.uint8)
        for t, col in zip(T, rgb):
            xs, ys, zs = x[t], y[t], z[t]
            x0, x1 = max(int(xs.min()), 0), min(int(xs.max()) + 1, PW - 1)
            y0, y1 = max(int(ys.min()), 0), min(int(ys.max()) + 1, PH - 1)
            if x0 > x1 or y0 > y1:
                continue
            den = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
            if abs(den) < 1e-9:
                continue
            gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            l0 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / den
            l1 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / den
            l2 = 1.0 - l0 - l1
            inside = (l0 >= 0) & (l1 >= 0) & (l2 >= 0)
            if not inside.any():
                continue
            zz = l0 * zs[0] + l1 * zs[1] + l2 * zs[2]
            sub = zb[y0:y1 + 1, x0:x1 + 1]
            win = inside & (zz < sub)
            sub[win] = zz[win]
            img[y0:y1 + 1, x0:x1 + 1][win] = col
    put(skin_pts, BT, skin_cols)
    put(Jw, Tj, jcols)
    return img


PREVIEW = os.path.join(OUT, "collar-open-preview.png")
if PREVIEW_ON:
    ex_kind = {}
    for r in rows:
        ex_kind[r["point"]] = (CUT_RGB if r.get("body_map", 1.0) <= 0.1 else
                               SHRUNK_RGB if r.get("head_shrink_mm", 0.0) > 0.05 else SHOWN_RGB)
    mt = MOVE[JT2].mean(1)
    jcol_after = np.where((mt > 0.0005)[:, None], CLOTH_RGB + (MOVE_RGB - CLOTH_RGB) * np.clip(mt / max(MOVE.max(), 1e-9), 0.3, 1.0)[:, None], CLOTH_RGB)
    jcol_before = np.repeat(CLOTH_RGB[None], len(JT), 0)
    VIEW_PREV = (("FRONT", np.array([0.0, -1.0, 0.0])), ("3-4 HIS LEFT", np.array([math.sin(math.radians(40)), -math.cos(math.radians(40)), 0.0])))
    grid_rows = []
    for name, label in (("rest", "REST"), ("down25", "DOWN 25")):
        P = POSE[name]
        cols = []
        for vlabel, d in VIEW_PREV:
            for state in ("before", "after"):
                cross = P[state + "_cross"]["body"]
                bad = np.zeros(len(BT), bool)
                if len(cross):
                    bad[np.unique(cross[:, 0])] = True
                scol = np.repeat(SKIN_RGB[None], len(BT), 0)
                if state == "after" and name == "rest":
                    for k, t in enumerate(BT):
                        if all(int(v) in ex_kind for v in t):
                            scol[k] = ex_kind[int(t[0])]
                scol[bad] = CROSS_RGB
                if state == "before":
                    im = panel(d, P["skin"]["body"]["P"], scol, P["before_J"], JT, jcol_before)
                else:
                    im = panel(d, P["skin"]["body"]["P"], scol, P["after_J"], JT2, jcol_after)
                text(im, "%s %s %s" % (label, vlabel, state.upper()), 10, 10, 2)
                c_ = P[state + "_cross"]
                text(im, "CROSSING %d" % len(np.unique(c_["body"][:, 0])) if len(c_["body"]) else "CROSSING 0", 10, 30, 2)
                cols.append(im)
        grid_rows.append(np.concatenate(cols, 1))
    img = np.concatenate(grid_rows, 0)
    bar = np.full((60, img.shape[1], 3), 245, np.uint8)
    text(bar, "GAP %.1f CM  OPEN %.1f CM   ORANGE MOVED  MAGENTA SKIN CROSSING  GREEN SHOWN  YELLOW HEAD SHRUNK  RED BODY CUT" % (
        100 * GAP, 100 * arc[-1]), 10, 20, 2)
    img = np.concatenate([img, bar], 0)
    for k in range(1, 4):
        img[:, k * PW - 1:k * PW + 1] = 120
    img[PH - 1:PH + 1, :] = 120
    write_png(PREVIEW, np.ascontiguousarray(img))
    log("wrote", PREVIEW)

# ---- THE RECORD -------------------------------------------------------------------------------------------------------
after_all = [CHECK[n]["after"] for n, *_ in POSES]
VERDICT = {
    "gap_cm": round(100 * GAP, 2), "gap_chosen": HOW, "open_cm_asked": round(100 * OPEN, 2),
    "open_cm_along_zip": round(100 * arc[-1], 2),
    "clears_every_pose": all(CHECK[n]["clears"] for n, *_ in POSES),
    "crossing_before_total": int(sum(sum(CHECK[n]["before"]["band_crossing_skin_triangles"].values()) for n, *_ in POSES)),
    "crossing_after_total": int(sum(sum(r["band_crossing_skin_triangles"].values()) for r in after_all)),
    "top_edge_stretch_max_after": max(r["top_edge_stretch_max"] for r in after_all),
    "stretch_within_1.2": max(r["top_edge_stretch_max"] for r in after_all) <= STRETCH_MAX,
    "top_edge_squeeze_min_after": min(r["top_edge_squeeze_min"] for r in after_all),
    "no_point_nearer_the_neck_line": REST["nearer_the_neck_line_most_mm"] < 0.001,
    "exposed_points": EXPOSE["newly_seen_any_view"], "exposed_body_points_cut": EXPOSE["body_points_cut_by_body_map_any_uv"],
    "fbx_check_pass": VERIFY["pass"] if VERIFY else None,
}
record = {
    "made": "2026-11-02", "tool": "tools/meshgen/blender/collar_open.py",
    "inputs": {"jacket": JACKET, "body": BODY, "face": FACE, "body_map": BODY_MAP, "head_map": HEAD_MAP},
    "outputs": {"fbx": OUT_FBX if WRITE else None, "preview": PREVIEW if PREVIEW_ON else None,
                "preview_layout": "top row at rest, bottom row 25 degrees down; columns: front before, front after, three-quarter "
                                  "from his left before, after; jacket grey, orange where the opening moved it; skin magenta "
                                  "where it crosses the collar; at rest after, newly shown skin green (yellow: the head map "
                                  "shrinks it; red: the body map cuts it)"},
    "settings": {"open_cm": 100 * OPEN, "gaps_measured_cm": [round(100 * g, 2) for g in GAPS], "reach_deg": REACH,
                 "split_neck01_neck02_head": SPLIT, "band_depth_mm": 1000 * DEPTH,
                 "opening": "each side turned round the neck's line (neck_01 to head) by A0 * smoothstep((slider depth - depth) / "
                            "slider depth) * smoothstep((reach - |angle|) / reach); A0 = asin(gap / (2 * the top tip's radius))"},
    "skeleton": {"rest_joint_max_difference": max(rest_check.values()), "signs": SIGN,
                 "neck_axis_from": AX_O.round(4).tolist(), "neck_axis_dir": AX_A.round(4).tolist()},
    "jacket": {"vertices": NV, "coincident_points": COINCIDENT, "band_points": int(BAND.sum()), "band_triangles": int(len(band_tris)),
               "top_edge_edges": int(len(TOPE)), "top_edge_length_m": round(float(REST_TOP_LEN.sum()), 4),
               "collar_top_above_neck01_mm": [round(1000 * TOP.min(), 1), round(1000 * TOP.max(), 1)],
               "outward_fraction": round(OUT_FRAC, 3), "had_custom_normals": HAD_CUSTOM_NORMALS},
    "zip_line": {"points_top_to_slider": chain.tolist(), "length_mm": round(1000 * arc[-1], 1),
                 "off_centre_plane_most_mm": round(1000 * float(np.abs(RW0[chain]).max()), 2),
                 "slider_depth_below_top_mm": round(1000 * D_S, 1), "points_split": K, "corners_moved_to_copies": REMAPPED_CORNERS,
                 "top_tip_radius_mm": round(1000 * RHO_TIP, 1), "tip_turn_deg": round(math.degrees(A0), 2)},
    "before_from_corrective_tool_check": BEFORE,
    "gap_sweep": SWEEP,
    "per_pose": CHECK,
    "rest": REST,
    "exposed_at_rest": EXPOSE,
    "collar_inside_faces_seen": INSIDE,
    "split": SPLIT_INFO,
    "fbx_check_against_input": VERIFY,
    "verdict": VERDICT,
    "notes": [
        "crossing = skin triangles (full body LOD0 near the neck; head mesh LOD0 skin section) overlapping the collar's band "
        "triangles (within 90 mm of its top), the corrective tool's test; whole_jacket counts every jacket triangle",
        "the jacket is posed by each point's own skinning taken from Blender as a linear map (verified against Blender's "
        "posing of the written mesh: split.blender_posing_vs_model_largest_m)",
        "exposed: a point counts when, from that viewpoint, the input jacket hid it and the opened one does not, and nothing "
        "of the body is in front; the head mesh is the same skin as the full body's head part at the neck",
        "a body point is cut where the body map is black (<= 0.1) at its UV (engine V = 1 - Blender v); the engine cuts a "
        "triangle only when every pixel it touches is black; the head map never cuts (its least grey 0.12), it shrinks",
        "Blender cannot run the face rig's own neck joints: the game moves the throat further (UNVERIFIED here)",
        "what-ifs the same day (--no-fbx, gaps 5 to 16 cm): a linear V (--taper linear), --reach-deg 60 and 120, and the "
        "zip open 8 cm (--open-cm 8) all agree: the head tipped down clears only from a 12 cm parting (the front tips "
        "turned 42 degrees round the neck), 45 degrees turned from 12 to 14 cm, and 20 down with 45 turned never "
        "(27 to 42 skin triangles still crossing at every gap): the jaw sinks into the collar's side, which no opening "
        "at the front moves",
        "the zip's opened edges are as long as the zip: hinged at the slider 56 mm below the collar's top, a 62 mm edge "
        "lets the two tips part only about 6 cm at the collar's height without stretching (the sweep's "
        "zip_edge_stretch_max_rest: 1.22 at 6 cm, 1.79 at 12 cm), so a 12 cm parting is not a zip opened 6 cm",
    ],
}
with open(os.path.join(OUT, "collar-open-record.json"), "w", encoding="utf-8") as fh:
    json.dump(record, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
log("DONE", json.dumps(VERDICT))
