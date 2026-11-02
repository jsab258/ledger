"""A CORRECTIVE SHAPE THAT STANDS A STAND COLLAR'S FRONT OFF THE THROAT AS THE HEAD TIPS AND TURNS (2 November 2026, Tom).

    blender -b --factory-startup -P tools/meshgen/blender/collar_corrective.py -- JACKET.fbx BODY.fbx FACE.fbx OUT_DIR
        [--name collar_open] [--margin-mm 3] [--depth-mm 90] [--rings 2] [--split 0.4,0.3,0.3]
        [--pitch-full 25] [--yaw-full 45] [--iterations 6] [--no-fbx] [--cap-mm X]

JACKET.fbx is the garment's skinned game file on the MetaHuman body skeleton, at rest (its weights are kept exactly);
BODY.fbx the full body with its neck and skeleton (LOD0 is used); FACE.fbx the head mesh as the game builds it (LOD0's
skin section). OUT_DIR gets the jacket again under its own file name with one shape key, NAME, exported so Unreal
imports it as a morph target; collar-corrective-record.json; collar-corrective-preview.png. --no-fbx measures only;
--cap-mm X (a what-if, with --no-fbx) caps the push at X mm, to measure what a smaller shape leaves.

WHY (2 November 2026). Tom wears a zip jacket with a stand collar. As his head tips down or turns, skin of his throat
comes through the collar's front either side of the zip: on the full body 20 degrees down brings the throat 19.4 mm
through. The skin that crosses is skin that shows above the collar at rest, so a head hidden-face map cannot hide it
(tools/ue/blender_head_hidden_face_map.py, its record of 2 November), and two tries on the jacket's weights failed
(following the neck made a choker ring under the jaw: production/art/clothing/tom-outfit/BAKE-PLAN-2026-10-27.md, 30
October). His yes of 31 October: a corrective shape on the jacket, as MetaHumans' own correctives are driven by the
pose. The jacket's weights stay; one shape key stands the collar's front off the throat, and the game sets its weight
each frame from the head's tilt and turn against the chest (LedgerGarments.h, DriveCorrectives):
w = clamp(max(pitch_down / PITCH_FULL, |yaw| / YAW_FULL), 0, 1), nil at rest.

WHAT IT DOES (the FBX import, posing by joint name, collar-top detection and skin-crosses-cloth test are the head-map
tool's):
  1. imports the jacket (first, so its armature keeps the FBX's own node name), the full body and the head mesh, and
     poses all three skeletons alike by joint name: the head down 10, 20, 25; turned 45 left and right; down 20 with
     45 turned each way, the rotation split over neck_01, neck_02 and head (--split), each about the joint's own axes;
     each pose's weight is the game's own formula on the posed body skeleton (the head's forward against the chest);
  2. the collar: jacket points within --depth-mm of the collar's top edge, measured by angle round the neck's line
     (neck_01 to head); coincident points welded so seams never part. Each point's push runs along its rest-space
     outward normal (smoothed over two rings); posed, the push moves it by the skinning's own blend of that normal,
     measured by a unit trial shape. Per pose, its clearance along that posed direction: a ray out that leaves the
     skin (full body or head) means the point lies inside the skin by that much; else a ray in to the skin behind it
     gives the gap. The point needs push = (target - clearance) / (posed length of a unit push) / w, the target being
     --margin-mm (3), or the rest clearance where that is already less (never asked to be better than at rest). A
     chin hanging over the rim, the rim in its crease, is outside the skin: no push (the head-map tool's note);
  3. the shape: the worst need over the poses whose weight is 1, spread 20 degrees round the neck beside each point
     that needs it, the column above it lifted with it and the column below tapered to nothing at --depth-mm below
     the top, nothing past 10 degrees beyond the farthest angle any pose needs (and never past the front half unless
     one does), smoothed over --rings rings never below the need; loose parts in the band (a zip's tape or teeth not
     joined to the cloth) move as the nearest cloth point (Tom's tape is joined, so it moves with the cloth round
     it); no point moves inward. Then every weight-1 pose is measured with the shape at its weight; where one still
     lacks clearance or crosses, the missing push is added and the shape rebuilt (--iterations);
  4. checks per pose, the shape at the pose's weight: skin triangles crossing collar triangles (full body and head),
     before and after; collar points inside the skin, deepest, before and after; the top edge's stretch (edge length
     over rest), at most 1.2; the gap from the top edge's front to the neck at most 15 mm; at rest nothing changes;
     the weight each pose would need for the shape to clear it;
  5. writes the jacket with the shape key and compares it, imported again, with the input: counts, points, weights
     (largest difference, must be 0), UVs, material slots, bone names and rest matrices.
"""
import json
import math
import os
import re
import struct
import sys
import zlib

import numpy as np


# ---- THE PURE RULES ---------------------------------------------------------------------------------------------------
def smoothstep(x):
    x = np.clip(np.asarray(x, float), 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def weight_of(pitch_down, yaw, pitch_full, yaw_full):
    """The game's corrective weight (LedgerGarments.h, DriveCorrectives)."""
    return float(np.clip(max(pitch_down / pitch_full, abs(yaw) / yaw_full), 0.0, 1.0))


# ---- BLENDER ----------------------------------------------------------------------------------------------------------
import bpy  # noqa: E402
from mathutils import Matrix, Quaternion, Vector  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402
from mathutils.kdtree import KDTree  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
JACKET, BODY, FACE, OUT = argv[:4]


def opt(n, d, f=float):
    return f(argv[argv.index(n) + 1]) if n in argv else d


NAME = opt("--name", "collar_open", str)
MARGIN = opt("--margin-mm", 3.0) / 1000.0
DEPTH = opt("--depth-mm", 90.0) / 1000.0
RINGS = opt("--rings", 2, int)
SPLIT = [float(x) for x in opt("--split", "0.4,0.3,0.3", str).split(",")]
PITCH_FULL = opt("--pitch-full", 25.0)
YAW_FULL = opt("--yaw-full", 45.0)
ITER = opt("--iterations", 6, int)
WRITE = "--no-fbx" not in argv
CAP = opt("--cap-mm", 0.0) / 1000.0     # a what-if only: the push capped, to measure what a smaller shape leaves
JOINTS = ("neck_01", "neck_02", "head")
POSES = [("rest", 0, 0), ("down10", 10, 0), ("down20", 20, 0), ("down25", 25, 0), ("left45", 0, 45),
         ("right45", 0, -45), ("down20_left45", 20, 45), ("down20_right45", 20, -45)]
COLLAR_RHO = 0.13    # jacket points this close to the neck's line give the collar's top by angle (m; the head-map tool's)
BAND_RHO = 0.20      # the band's points lie this close to the neck's line (m)
BINS = 72
SKIN_REACH = 0.30    # skin triangles this close to the neck's middle are measured (m)
RAY_OUT, RAY_IN = 0.08, 0.06
FRONT_DEG = 45.0     # "in front" for the gap: within this angle of straight ahead
STRETCH_MAX, GAP_MAX = 1.2, 0.015
UNIT = 0.01          # the trial shape's push (m)
os.makedirs(OUT, exist_ok=True)


def log(*a):
    print("CORRECTIVE", *a, flush=True)


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
for o in bmeshes + fmeshes:          # only LOD0 is measured; the rest would only slow every pose
    if o not in (body, face):
        bpy.data.objects.remove(o, do_unlink=True)
ARMS = {"face": farm, "body": barm, "jacket": jarm}
log("imported", {k: a.name for k, a in ARMS.items()}, "jacket", jacket.name, "body", body.name, "face", face.name)


# ---- THE NECK'S LINE (the full body's neck_01 to head, at rest) AND THE POSES (the head-map tool's) -------------------
def joint(arm, name):
    return np.array(arm.matrix_world @ arm.data.bones[name].head_local)


AX_O = joint(barm, "neck_01")
AX_A = joint(barm, "head") - AX_O
AX_A /= np.linalg.norm(AX_A)
FRONT = np.array([0.0, -1.0, 0.0])   # the engine's +Y after the FBX's axis change
AX_U = FRONT - (FRONT @ AX_A) * AX_A
AX_U /= np.linalg.norm(AX_U)
AX_W = np.cross(AX_A, AX_U)


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
log("signs", SIGN, "rest joints differ by at most", max(rest_check.values()))


def game_angles():
    """The game's HeadAgainstChest on the posed body skeleton: the head's rotation since rest with the chest's taken
    out, applied to the body's forward (the engine's +Y, Blender's -Y here); pitch down and yaw in degrees."""
    def delta(bone):
        M = barm.matrix_world @ barm.pose.bones[bone].matrix
        R = barm.matrix_world @ barm.data.bones[bone].matrix_local
        return M.to_3x3().normalized().to_quaternion() @ R.to_3x3().normalized().to_quaternion().inverted()
    F = np.array((delta("spine_05").inverted() @ delta("head")) @ Vector(FRONT))
    return math.degrees(math.asin(max(-1.0, min(1.0, -F[2])))), math.degrees(math.atan2(F[0], -F[1]))


# ---- THE SKIN: the full body's LOD0 near the neck and the head mesh's skin section ------------------------------------
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
    # the winding faces outward? (round the neck, between neck_01 and the head joint)
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
    log("skin", k, "triangles near the neck", len(s["T"]), "outward fraction", s["outward_fraction"], "flipped", s["flipped"])

# ---- THE JACKET: welded points, edges, parts, normals; the collar's top by angle; the band -----------------------------
jme = jacket.data
JA = np.array(jacket.matrix_world)
NV = len(jme.vertices)
jme.calc_loop_triangles()
JT = np.zeros(len(jme.loop_triangles) * 3, int)
jme.loop_triangles.foreach_get("vertices", JT)
JT = JT.reshape(-1, 3)
JMI = np.zeros(len(jme.loop_triangles), int)
jme.loop_triangles.foreach_get("material_index", JMI)
J0 = evaluated_world(jacket)
CO0 = np.zeros(NV * 3)
jme.vertices.foreach_get("co", CO0)
CO0 = CO0.reshape(-1, 3)
log("rest pose moves the jacket's points by at most %.2e m" % float(np.abs(J0 - to_world(JA, CO0)).max()))

kd = KDTree(NV)
for i, p in enumerate(J0):
    kd.insert(p, i)
kd.balance()
par = list(range(NV))


def find(i):
    while par[i] != i:
        par[i] = par[par[i]]
        i = par[i]
    return i


for i, p in enumerate(J0):
    for _c, j, _d in kd.find_range(p, 1e-5):
        a, b = find(i), find(j)
        if a != b:
            par[max(a, b)] = min(a, b)
_u, PID = np.unique([find(i) for i in range(NV)], return_inverse=True)
NP = int(PID.max()) + 1
REP = np.zeros(NP, int)
REP[PID[::-1]] = np.arange(NV)[::-1]
P0 = J0[REP]
TP = PID[JT]
TP = TP[(TP[:, 0] != TP[:, 1]) & (TP[:, 1] != TP[:, 2]) & (TP[:, 2] != TP[:, 0])]
E = np.sort(np.concatenate([TP[:, [0, 1]], TP[:, [1, 2]], TP[:, [2, 0]]]), 1)
EU, ECNT = np.unique(E, axis=0, return_counts=True)
NBR = [[] for _ in range(NP)]
for a, b in EU:
    NBR[a].append(b)
    NBR[b].append(a)
# connected parts
part = np.full(NP, -1)
npart = 0
for s in range(NP):
    if part[s] >= 0:
        continue
    st = [s]
    while st:
        v = st.pop()
        if part[v] >= 0:
            continue
        part[v] = npart
        st.extend(n for n in NBR[v] if part[n] < 0)
    npart += 1
log("jacket vertices", NV, "welded points", NP, "parts", npart, "welded copies", NV - NP)

JE = np.unique(np.sort(np.concatenate([JT[:, [0, 1]], JT[:, [1, 2]], JT[:, [2, 0]]]), 1), axis=0)


def collar_top(Jw):
    """The head-map tool's: the highest jacket point per 5 degrees round the neck's line, from points every few
    millimetres along the jacket's edges near it."""
    a, b = Jw[JE[:, 0]], Jw[JE[:, 1]]
    keep = (cyl(a)[2] < COLLAR_RHO) & (cyl(b)[2] < COLLAR_RHO)
    t = np.linspace(0.0, 1.0, 9)
    pts = (a[keep][:, None, :] * (1 - t)[None, :, None] + b[keep][:, None, :] * t[None, :, None]).reshape(-1, 3)
    h, th, _r, _rd = cyl(pts)
    return angle_table(th, h)


TOP, top_empty = collar_top(J0)
FLIP = 1.0


def tri_normals(Jw):
    a, b, c = Jw[JT[:, 0]], Jw[JT[:, 1]], Jw[JT[:, 2]]
    n = np.cross(b - a, c - a)
    return n * FLIP   # area-weighted


nA = tri_normals(J0)
cen = J0[JT].mean(1)
ch, cth, crho, crad = cyl(cen)
bandf = (crho < COLLAR_RHO) & (ch > at_angle(TOP, cth) - 0.06)
nn = nA / np.maximum(np.linalg.norm(nA, axis=1, keepdims=True), 1e-15)
radial = np.einsum("ij,ij->i", nn[bandf], crad[bandf])
facing = np.abs(radial) > 0.5
OUT_FRAC = float((radial[facing] > 0).mean()) if facing.any() else float("nan")
if OUT_FRAC < 0.5:
    FLIP = -1.0
    nA = -nA
log("collar's faces facing round the neck", int(facing.sum()), "outward fraction %.3f" % OUT_FRAC, "flip", FLIP < 0)

# rest normals per welded point, smoothed over two rings
VN = np.zeros((NP, 3))
for k in range(3):
    np.add.at(VN, PID[JT[:, k]], nA)
VN /= np.maximum(np.linalg.norm(VN, axis=1, keepdims=True), 1e-15)
for _r in range(2):
    nxt = VN.copy()
    for i in range(NP):
        if NBR[i]:
            nxt[i] = VN[[i] + NBR[i]].sum(0)
    VN = nxt / np.maximum(np.linalg.norm(nxt, axis=1, keepdims=True), 1e-15)

h0, th0, rho0, rad0 = cyl(P0)
BELOW = at_angle(TOP, th0) - h0           # how far below the collar's top, at the same angle (m)
BAND = (BELOW <= DEPTH) & (BELOW >= -0.01) & (rho0 < BAND_RHO)
parts_in_band = np.bincount(part[BAND], minlength=npart)
MAIN = int(parts_in_band.argmax())
CLOTH = BAND & (part == MAIN)
FOLLOW = BAND & (part != MAIN)
mat_names = [m.name if m else None for m in jme.materials]
band_tris = np.nonzero(BAND[PID[JT]].all(1))[0]
log("collar top above neck_01 %.1f..%.1f mm, empty bins %d; band points %d (cloth %d, loose parts %d in %d parts); band triangles by material %s" % (
    1000 * TOP.min(), 1000 * TOP.max(), top_empty, int(BAND.sum()), int(CLOTH.sum()), int(FOLLOW.sum()),
    int((parts_in_band[np.arange(npart) != MAIN] > 0).sum()),
    {mat_names[m]: int(c) for m, c in zip(*np.unique(JMI[band_tris], return_counts=True))}))
for p_ in np.nonzero(parts_in_band)[0]:
    sel = part == p_
    mats = np.unique(JMI[np.isin(PID[JT], np.nonzero(sel)[0]).any(1)])
    log("  part", int(p_), "points", int(sel.sum()), "in band", int(parts_in_band[p_]), "materials", [mat_names[m] for m in mats],
        "angle %.0f..%.0f" % (th0[sel & BAND].min(), th0[sel & BAND].max()))

# the collar's top edge: open edges of the cloth within 4 mm of its top
OPEN = EU[ECNT == 1]
TOPE = OPEN[CLOTH[OPEN].all(1) & (BELOW[OPEN] <= 0.004).all(1) & (rho0[OPEN] < COLLAR_RHO).all(1)]
TOPP = np.unique(TOPE)
log("top edge: edges %d, points %d, length %.3f m, angles %.0f..%.0f" % (
    len(TOPE), len(TOPP), float(np.linalg.norm(P0[TOPE[:, 0]] - P0[TOPE[:, 1]], axis=1).sum()), th0[TOPP].min(), th0[TOPP].max()))

# ---- SHAPE KEYS: the basis, the corrective, a unit trial push along each band point's rest normal ---------------------
A3i = np.linalg.inv(JA[:3, :3])
jacket.shape_key_add(name="Basis", from_mix=False)
KEY = jacket.shape_key_add(name=NAME, from_mix=False)
TRIAL = jacket.shape_key_add(name="trial_unit", from_mix=False)
KEY.value, TRIAL.value = 0.0, 0.0
UNITV = np.zeros((NV, 3))
UNITV[BAND[PID]] = VN[PID[BAND[PID]]] * UNIT
TRIAL.data.foreach_set("co", (CO0 + UNITV @ A3i.T).ravel())


def set_shape(push_world_per_point):
    """The corrective's points: rest plus each welded point's push (world vector), in the mesh's own space."""
    d = push_world_per_point[PID]
    KEY.data.foreach_set("co", (CO0 + d @ A3i.T).ravel())
    jme.update()


def jacket_at(w_key, w_trial=0.0):
    KEY.value = w_key
    if TRIAL is not None:
        TRIAL.value = w_trial
    bpy.context.view_layer.update()
    X = evaluated_world(jacket)
    KEY.value = 0.0
    if TRIAL is not None:
        TRIAL.value = 0.0
    return X


# ---- THE POSES: the jacket without and with the trial push, the skin, the game's weight -------------------------------
def bvh_of(Pw, T):
    return BVHTree.FromPolygons(Pw.tolist(), T.tolist(), all_triangles=True)


POSE = {}
for name, pitch, yaw in POSES:
    set_pose(pitch, yaw)
    gp, gy = game_angles()
    J = jacket_at(0.0)
    Jt = jacket_at(0.0, 1.0)
    e = (Jt[REP] - J[REP]) / UNIT                        # the posed move of a unit rest push, per welded point
    skin = {}
    for k, s in SKIN.items():
        Pw = evaluated_world(s["obj"])
        skin[k] = {"P": Pw, "bvh": bvh_of(Pw, s["T"])}
    POSE[name] = {"pitch": pitch, "yaw": yaw, "w_nominal": weight_of(pitch, yaw, PITCH_FULL, YAW_FULL),
                  "game_pitch": gp, "game_yaw": gy, "w": weight_of(gp, gy, PITCH_FULL, YAW_FULL),
                  "J": J, "e": e, "skin": skin}
    log("pose %-15s game pitch %6.2f yaw %7.2f  w %.3f (nominal %.3f)  unit push moves %.3f..%.3f" % (
        name, gp, gy, POSE[name]["w"], POSE[name]["w_nominal"], np.linalg.norm(e[BAND], axis=1).min(),
        np.linalg.norm(e[BAND], axis=1).max()))
set_pose(0, 0)


# ---- CLEARANCE: along the posed push direction, each band point's gap to the skin (+) or depth inside it (-) ----------
def clearance(X, U, skin):
    """X: posed points; U: unit posed push directions. Per point the least over the full body and the head: -t where a
    ray out leaves the skin at t (the point is inside), else +t where a ray in meets the skin's outside at t; inf if
    nothing within reach. Also how many points lie with skin in front (a ray out enters skin: the rim in a crease)."""
    out = np.full(len(X), np.inf)
    tucked = np.zeros(len(X), bool)
    odd = 0
    for s in skin.values():
        bvh = s["bvh"]
        for i in range(len(X)):
            x, u = Vector(X[i]), Vector(U[i])
            loc, nrm, _ix, dist = bvh.ray_cast(x, u, RAY_OUT)
            if loc is not None and nrm.dot(u) > 0:
                out[i] = min(out[i], -dist)
                continue
            if loc is not None:
                tucked[i] = True
            loc, nrm, _ix, dist = bvh.ray_cast(x, -u, RAY_IN)
            if loc is not None:
                if nrm.dot(-u) < 0:
                    out[i] = min(out[i], dist)
                else:
                    odd += 1
    return out, tucked, odd


BI = np.nonzero(BAND)[0]
CLEAR0 = {}
for name, *_ in POSES:
    p = POSE[name]
    U = p["e"][BI] / np.maximum(np.linalg.norm(p["e"][BI], axis=1, keepdims=True), 1e-12)
    p["U"] = U
    c, tk, odd = clearance(p["J"][REP][BI], U, p["skin"])
    CLEAR0[name] = c
    p["tucked0"], p["odd0"] = int(tk.sum()), odd
REST_CLEAR = CLEAR0["rest"]
TARGET = np.minimum(MARGIN, REST_CLEAR)
for name, *_ in POSES:
    c = CLEAR0[name]
    fin = np.isfinite(c)
    log("pose %-15s clearance least %.2f mm; inside the skin %d points, deepest %.2f mm; short of target %d; rim tucked %d; odd %d" % (
        name, 1000 * c[fin].min(), int((c < 0).sum()), -1000 * c.min() if (c < 0).any() else 0.0,
        int((c < TARGET).sum()), POSE[name]["tucked0"], POSE[name]["odd0"]))


def need_of(name, clear):
    p = POSE[name]
    el = np.linalg.norm(p["e"][BI], axis=1)
    return np.maximum(0.0, TARGET - clear) / np.maximum(el, 0.3) / max(p["w"], 1e-6)


def table(vals, label):
    """vals over the band's points: the largest by angle (15 degree columns) and depth below the top (10 mm rows)."""
    rows = []
    th, b = th0[BI], BELOW[BI]
    cols = list(range(-165, 181, 15))
    for r in range(0, int(DEPTH * 1000) + 1, 10):
        sel_r = (b * 1000 >= r - 10) & (b * 1000 < r) if r else (b * 1000 < 0)
        row = []
        for c0 in cols:
            s = sel_r & (th >= c0 - 7.5) & (th < c0 + 7.5)
            row.append("%5.1f" % (1000 * vals[s].max()) if s.any() else "    .")
        rows.append("%3d %s" % (r, " ".join(row)))
    log(label + " (mm; rows: mm below the top, up to; columns: degrees from straight ahead, + his left)\n    " +
        " ".join("%5d" % c for c in cols) + "\n" + "\n".join(rows))


W1 = [n for n, *_ in POSES if POSE[n]["w_nominal"] >= 1.0]
log("the poses whose weight is 1:", W1)

# ---- THE SHAPE --------------------------------------------------------------------------------------------------------
TH_FALL = 20.0       # the push spreads this far round the neck beside a point that needs it (degrees)
TH_B, B_B = th0[BI], BELOW[BI]
RING = [np.array([i] + NBR[i]) for i in BI]
CLOTH_B, FOLLOW_B = CLOTH[BI], FOLLOW[BI]
if FOLLOW_B.any():   # loose parts (a zip's tape or teeth not joined to the cloth) move with the nearest cloth point
    kdc = KDTree(int(CLOTH_B.sum()))
    for k, i in enumerate(BI[CLOTH_B]):
        kdc.insert(P0[i], k)
    kdc.balance()
    FOLLOWS = np.array([np.nonzero(CLOTH_B)[0][kdc.find(P0[i])[1]] for i in BI[FOLLOW_B]])


def wrap180(a):
    return (np.asarray(a) + 180.0) % 360.0 - 180.0


def build(N):
    """The push per band point (m, along its rest normal) from the need N: spread round the neck over TH_FALL degrees;
    the column above a point that needs it lifted with it, the column below tapered to nothing at DEPTH below the top;
    nothing beyond 10 degrees past the farthest angle any pose needs, and never past the front half unless one does;
    smoothed over RINGS rings, never below the need, the smoothing's spill faded out over the band's last 20 mm."""
    needy = np.nonzero(N > 1e-5)[0]
    if not len(needy):
        return np.zeros(len(BI)), 90.0
    reach = max(90.0, float(np.abs(TH_B[needy]).max()) + 10.0)
    dth = np.abs(wrap180(TH_B[:, None] - TH_B[None, needy]))
    kt = smoothstep(1.0 - dth / TH_FALL)
    bc, bn = B_B[:, None], B_B[None, needy]
    kb = np.where(bc <= bn, 1.0, smoothstep((DEPTH - bc) / np.maximum(DEPTH - bn, 1e-6)))
    env = (N[needy][None, :] * kt * kb).max(1) * smoothstep((reach - np.abs(TH_B)) / 10.0)
    p = np.maximum(N, env)
    full = np.zeros(NP)
    for _r in range(RINGS):
        full[BI] = p
        p = np.maximum(p, np.array([full[r].mean() for r in RING]))
    # the smoothing's spill into the band's last 20 mm faded out, so the push is nothing at DEPTH below the top
    p = np.maximum(N, p * smoothstep((DEPTH - B_B) / 0.02))
    return p, reach


def displacement(p):
    """Per welded point, the shape's move (world, at rest): along the rest normal; loose parts as their cloth point."""
    D = np.zeros((NP, 3))
    D[BI] = VN[BI] * p[:, None]
    if FOLLOW_B.any():
        D[BI[FOLLOW_B]] = D[BI[FOLLOWS]]
    return D


BAND_T = JT[band_tris]
BIX = np.full(NP, -1)
BIX[BI] = np.arange(len(BI))
BAND_TB = BIX[PID[BAND_T]]          # each band triangle's corners as band points (all in the band)


def crossings(J, skin):
    """The head-map tool's test, on the collar's band: skin triangles (full body, head) crossing its triangles."""
    bb = bvh_of(J, BAND_T)
    res = {}
    for k, s in skin.items():
        pairs = np.array(s["bvh"].overlap(bb), int).reshape(-1, 2)
        res[k] = pairs
    return res


def place(name, w):
    P = POSE[name]
    set_pose(P["pitch"], P["yaw"])
    return jacket_at(w)


# the need: the worst over the poses whose weight is 1, each divided by its own (game) weight
NEED0 = np.max([need_of(n, CLEAR0[n]) for n in W1], axis=0)
N = np.minimum(NEED0, CAP) if CAP > 0 else NEED0.copy()
history = []
for it in range(ITER + 1):
    p, reach = build(N)
    D = displacement(p)
    set_shape(D)
    miss = np.zeros(len(BI))
    step = {"iteration": it, "largest_push_mm": round(1000 * float(p.max()), 2), "poses": {}}
    for name in W1:
        P = POSE[name]
        w = P["w"]
        J = place(name, w)
        c, _tk, _odd = clearance(J[REP][BI], P["U"], P["skin"])
        el = np.maximum(np.linalg.norm(P["e"][BI], axis=1), 0.3)
        a = np.maximum(0.0, TARGET - c) / el / max(w, 1e-6)
        cr = crossings(J, P["skin"])
        add = np.zeros(len(BI))
        for k, pairs in cr.items():
            if not len(pairs):
                continue
            Sk = P["skin"][k]["P"][SKIN[k]["T"][pairs[:, 0]]]          # (n, 3, 3) skin corners
            Ct = J[BAND_T[pairs[:, 1]]]                                 # (n, 3, 3) collar corners
            n = np.cross(Ct[:, 1] - Ct[:, 0], Ct[:, 2] - Ct[:, 0]) * FLIP
            n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-15)
            d = np.einsum("nkj,nj->nk", Sk - Ct[:, :1, :], n).max(1)
            inc = np.minimum(np.maximum(d, 0.0) + MARGIN, 0.01) / max(w, 1e-6)
            for t, v in zip(pairs[:, 1], inc):
                for q in BAND_TB[t]:
                    add[q] = max(add[q], v)
        m = np.maximum(a, add)
        miss = np.maximum(miss, m)
        step["poses"][name] = {"short_points": int((a > 5e-5).sum()), "most_short_mm": round(1000 * float(a.max()), 2),
                               "crossing_skin_triangles": {k: int(len(np.unique(v[:, 0]))) for k, v in cr.items()}}
    history.append(step)
    log("iteration", it, json.dumps(step))
    if miss.max() < 5e-5 or it == ITER:
        break
    N = np.maximum(N, np.where(miss > 5e-5, p + miss, 0.0))
    if CAP > 0:
        N = np.minimum(N, CAP)
set_pose(0, 0)
PUSH = p
DISP = displacement(PUSH)
table(NEED0, "the need, worst of the weight-1 poses")
table(PUSH, "the shape's push")

# ---- THE CHECKS, per pose, before (v30) and with the shape at the pose's weight ---------------------------------------
NEAR_COLLAR = 0.03
EDGE_RATIO = 0.5
SKIN_V = {}
for k, s in SKIN.items():
    v = np.unique(s["T"])
    h, th, rho, _r = cyl(s["W0"][v])
    SKIN_V[k] = v[(rho < BAND_RHO) & (h > at_angle(TOP, th) - DEPTH - 0.02) & (h < at_angle(TOP, th) + 0.12)]
REST_TOP_LEN = np.linalg.norm(P0[TOPE[:, 0]] - P0[TOPE[:, 1]], axis=1)
BAND_E = EU[BAND[EU].all(1)]
REST_BAND_LEN = np.linalg.norm(P0[BAND_E[:, 0]] - P0[BAND_E[:, 1]], axis=1)
TOP_FRONT = TOPP[np.abs(th0[TOPP]) <= FRONT_DEG]


def skin_through(J, skin, buried):
    """Skin points in front of a collar triangle buried in the skin (one of its points inside it): skin come through
    the collar. The nearest collar point, signed by the collar's outward normal; beside its edge is not through (the
    head-map tool's depth). Per mesh (count, deepest m)."""
    bb = bvh_of(J, BAND_T)
    a, b, c = J[BAND_T[:, 0]], J[BAND_T[:, 1]], J[BAND_T[:, 2]]
    tn = np.cross(b - a, c - a) * FLIP
    tn /= np.maximum(np.linalg.norm(tn, axis=1, keepdims=True), 1e-15)
    tri_buried = buried[BAND_TB].any(1)
    res = {}
    for k, s in skin.items():
        n, deep = 0, 0.0
        for q in s["P"][SKIN_V[k]]:
            hit = bb.find_nearest(Vector(q), NEAR_COLLAR)
            if hit[0] is None or not tri_buried[hit[2]]:
                continue
            d = q - np.array(hit[0])
            sd = float(d @ tn[hit[2]])
            if hit[3] > 1e-7 and abs(sd) < EDGE_RATIO * hit[3]:
                continue
            if sd > 0:
                n += 1
                deep = max(deep, sd)
        res[k] = (n, deep)
    return res


def mm(x, nd=2):
    return None if x is None or not np.isfinite(x) else round(1000 * float(x), nd)


CHECK = {}
for name, *_ in POSES:
    P = POSE[name]
    row = {"pitch_down_deg": P["pitch"], "turn_left_deg": P["yaw"],
           "game_pitch_down_deg": round(P["game_pitch"], 2), "game_yaw_deg": round(P["game_yaw"], 2),
           "weight_nominal": round(P["w_nominal"], 3), "weight": round(P["w"], 3)}
    for label, w in (("before", 0.0), ("after", P["w"])):
        J = place(name, w)
        X = J[REP]
        c, tk, odd = clearance(X[BI], P["U"], P["skin"])
        cr = crossings(J, P["skin"])
        thr = skin_through(J, P["skin"], c < 0)
        top_st = np.linalg.norm(X[TOPE[:, 0]] - X[TOPE[:, 1]], axis=1) / REST_TOP_LEN
        band_st = np.linalg.norm(X[BAND_E[:, 0]] - X[BAND_E[:, 1]], axis=1) / REST_BAND_LEN
        cf = c[BIX[TOP_FRONT]]
        gaps = np.where(cf < 0, 0.0, cf)
        gi = int(np.argmax(np.where(np.isfinite(gaps), gaps, RAY_IN + 1e-3)))
        row[label] = {
            "crossing_skin_triangles": {k: int(len(np.unique(v[:, 0]))) for k, v in cr.items()},
            "crossed_collar_triangles": int(len(np.unique(np.concatenate([v[:, 1] for v in cr.values()])))),
            "collar_points_inside_skin": int((c < 0).sum()),
            "deepest_collar_point_inside_skin_mm": mm(-c.min()) if (c < 0).any() else 0.0,
            "collar_points_short_of_target": int((c < TARGET - 5e-5).sum()),
            "skin_points_through": {k: v[0] for k, v in thr.items()},
            "skin_points_through_deepest_mm": {k: mm(v[1]) for k, v in thr.items()},
            "rim_tucked_under_skin_points": int(tk.sum()),
            "top_edge_stretch_max": round(float(top_st.max()), 3),
            "top_edge_stretch_min": round(float(top_st.min()), 3),
            "band_edge_stretch_max": round(float(band_st.max()), 3),
            "front_top_edge_gap_to_neck_max_mm": mm(gaps[gi]) if np.isfinite(gaps[gi]) else "over %d" % int(1000 * RAY_IN),
            "front_top_edge_gap_at_angle_deg": round(float(th0[TOP_FRONT[gi]]), 1),
            "front_top_edge_gap_median_mm": mm(float(np.median(np.where(np.isfinite(gaps), gaps, RAY_IN)))),
        }
        if label == "after" and name == "rest":
            row["rest_moves_max_m"] = float(np.abs(X - POSE["rest"]["J"][REP]).max())
    # the weight this pose would need for the shape to clear it
    el = np.maximum(np.linalg.norm(P["e"][BI], axis=1), 0.3)
    a = np.maximum(0.0, TARGET - CLEAR0[name]) / el
    sel = a > 5e-5
    if sel.any():
        ratio = np.where(PUSH[sel] > 1e-6, a[sel] / np.maximum(PUSH[sel], 1e-9), np.inf)
        row["weight_needed_to_clear"] = round(float(ratio.max()), 3) if np.isfinite(ratio.max()) else "none suffices"
    else:
        row["weight_needed_to_clear"] = 0.0
    row["clears_at_its_weight"] = (row["after"]["collar_points_short_of_target"] == 0
                                   and sum(row["after"]["crossing_skin_triangles"].values()) == 0)
    CHECK[name] = row
    log("check", name, json.dumps(row))
set_pose(0, 0)

moved_v = np.linalg.norm(DISP[PID], axis=1)
TAPE_B = np.isin(BI, np.unique(PID[JT[JMI == mat_names.index("Tape")]])) if "Tape" in mat_names else np.zeros(len(BI), bool)
SUMMARY = {
    "push_largest_mm": mm(PUSH.max()),
    "push_median_of_moved_mm": mm(float(np.median(PUSH[PUSH > 1e-5]))) if (PUSH > 1e-5).any() else 0.0,
    "points_moved": int((moved_v > 1e-5).sum()), "points_moved_over_1mm": int((moved_v > 1e-3).sum()),
    "points_moved_note": "jacket vertices the full shape moves more than 0.01 mm (and more than 1 mm)",
    "least_move_along_rest_outward_normal_mm": mm(float(np.min(np.einsum("ij,ij->i", DISP[BI], VN[BI]))), 4),
    "least_move_along_neck_radial_mm": mm(float(np.min(np.einsum("ij,ij->i", DISP[BI], rad0[BI]))), 4),
    "zip_tape_push_mm": [mm(PUSH[TAPE_B].min()), mm(PUSH[TAPE_B].max())] if TAPE_B.any() else None,
    "zip_tape_note": "the zip's tape is joined to the cloth (one part), so it moves with the cloth round it",
}
log("summary", json.dumps(SUMMARY))


# ---- THE FILE: the input jacket plus the shape key; read back and compared with the input -------------------------------
def plain(name):
    return re.sub(r"\.\d{3}$", "", name) if name else name


def snapshot(path):
    """An FBX imported into this scene: its jacket mesh and armature as arrays, then removed again."""
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
    wts = {}
    for v in me.vertices:
        for g in v.groups:
            wts[(v.index, gname[g.group])] = g.weight
    uvs = {}
    for lay in me.uv_layers:
        a = np.zeros(nl * 2)
        lay.data.foreach_get("uv", a)
        uvs[lay.name] = a
    mi = np.zeros(len(me.polygons), int)
    me.polygons.foreach_get("material_index", mi)
    lv = np.zeros(nl, int)
    me.loops.foreach_get("vertex_index", lv)
    cn = np.zeros(nl * 3)
    me.corner_normals.foreach_get("vector", cn)
    keys = {}
    if me.shape_keys:
        base = np.zeros(nv * 3)
        me.shape_keys.key_blocks[0].data.foreach_get("co", base)
        for kb in me.shape_keys.key_blocks[1:]:
            a = np.zeros(nv * 3)
            kb.data.foreach_get("co", a)
            keys[kb.name] = (a - base).reshape(-1, 3)
    snap = {"arm_name": plain(arm.name), "mesh_name": plain(mo.name),
            "counts": [nv, len(me.edges), len(me.polygons), nl], "co": co.reshape(-1, 3),
            "mesh_matrix": np.array(mo.matrix_world), "arm_matrix": np.array(arm.matrix_world),
            "weights": wts, "groups": sorted(gname.values()), "uvs": uvs, "uv_names": [u.name for u in me.uv_layers],
            "materials": [plain(m.name) if m else None for m in me.materials], "mi": mi, "lv": lv, "cn": cn,
            "bones": [b.name for b in arm.data.bones], "parents": [b.parent.name if b.parent else None for b in arm.data.bones],
            "bone_matrices": np.array([np.array(arm.matrix_world @ b.matrix_local) for b in arm.data.bones]),
            "key_names": [kb.name for kb in me.shape_keys.key_blocks] if me.shape_keys else [], "keys": keys}
    for o in new:
        bpy.data.objects.remove(o, do_unlink=True)
    return snap


def compare(a, b):
    """The second file against the first: what must be identical, and how far the rest pose moved in the round trip."""
    keys = set(a["weights"]) | set(b["weights"])
    rot, wb = {}, {k[1] for k, w in a["weights"].items() if w > 0}
    if a["bones"] == b["bones"]:
        na = a["bone_matrices"][:, :3, :3] / np.linalg.norm(a["bone_matrices"][:, :3, :3], axis=1, keepdims=True)
        nb = b["bone_matrices"][:, :3, :3] / np.linalg.norm(b["bone_matrices"][:, :3, :3], axis=1, keepdims=True)
        for n, ra, rb in zip(a["bones"], na, nb):
            rot[n] = math.degrees(Matrix(ra.tolist()).to_quaternion().rotation_difference(Matrix(rb.tolist()).to_quaternion()).angle)
    wdiff = max((abs(a["weights"].get(k, 0.0) - b["weights"].get(k, 0.0)) for k in keys), default=0.0)
    same_bones = a["bones"] == b["bones"] and a["parents"] == b["parents"]
    return {
        "counts_vertices_edges_faces_corners": [a["counts"], b["counts"]], "counts_equal": a["counts"] == b["counts"],
        "points_largest_difference_m": float(np.abs(a["co"] - b["co"]).max()) if a["counts"] == b["counts"] else None,
        "weights_pairs": [len(a["weights"]), len(b["weights"])], "weights_largest_difference": float(wdiff),
        "weight_groups_equal": a["groups"] == b["groups"],
        "uv_layers": [a["uv_names"], b["uv_names"]],
        "uv_largest_difference": max((float(np.abs(a["uvs"][n] - b["uvs"][n]).max()) for n in a["uv_names"] if n in b["uvs"]), default=None),
        "material_slots": [a["materials"], b["materials"]], "material_slots_equal": a["materials"] == b["materials"],
        "face_materials_equal": bool(np.array_equal(a["mi"], b["mi"])), "corners_equal": bool(np.array_equal(a["lv"], b["lv"])),
        "corner_normals_largest_difference": float(np.abs(a["cn"] - b["cn"]).max()) if len(a["cn"]) == len(b["cn"]) else None,
        "bones": [len(a["bones"]), len(b["bones"])], "bone_names_and_parents_equal": same_bones,
        "bone_rest_matrices_largest_difference": float(np.abs(a["bone_matrices"] - b["bone_matrices"]).max()) if same_bones else None,
        "bone_rest_positions_largest_difference_mm": float(1000 * np.linalg.norm(a["bone_matrices"][:, :3, 3] - b["bone_matrices"][:, :3, 3], axis=1).max()) if same_bones else None,
        "bone_rest_rotations_largest_difference_deg": max(rot.values()) if same_bones else None,
        "bones_turned_over_0.01_deg": {n: round(d, 4) for n, d in rot.items() if d > 0.01} if same_bones else None,
        "weighted_bones_rest_rotations_largest_difference_deg": max(d for n, d in rot.items() if n in wb) if same_bones else None,
        "object_names": [[a["arm_name"], a["mesh_name"]], [b["arm_name"], b["mesh_name"]]],
        "object_matrices_largest_difference": float(max(np.abs(a["mesh_matrix"] - b["mesh_matrix"]).max(),
                                                        np.abs(a["arm_matrix"] - b["arm_matrix"]).max())),
        "shape_keys": [a["key_names"], b["key_names"]],
    }


OUT_FBX = os.path.join(OUT, os.path.basename(JACKET))
VERIFY = None
pose_dev = max(max(abs(x) for x in pb.location) + max(abs(x - y) for x, y in zip(pb.rotation_quaternion, (1, 0, 0, 0)))
               + max(abs(x - 1) for x in pb.scale) for pb in jarm.pose.bones)
if WRITE:
    assert jarm.name == JARM_NAME and jacket.name == JACKET_NAME
    jacket.shape_key_remove(TRIAL)
    TRIAL = None
    KEY.value = 0.0
    set_pose(0, 0)
    bpy.ops.object.select_all(action="DESELECT")
    jarm.select_set(True)
    jacket.select_set(True)
    bpy.context.view_layer.objects.active = jarm
    # skin_garment.py's export, the one v30 was written with
    bpy.ops.export_scene.fbx(filepath=OUT_FBX, use_selection=True, object_types={"ARMATURE", "MESH"}, add_leaf_bones=False,
                             mesh_smooth_type="OFF", use_tspace=True, colors_type="LINEAR", bake_anim=False)
    log("wrote", OUT_FBX)
    A_ = snapshot(JACKET)
    B_ = snapshot(OUT_FBX)
    VERIFY = compare(A_, B_)
    want = DISP[PID] @ A3i.T
    got = B_["keys"].get(NAME)
    VERIFY["shape_key_present"] = got is not None
    if got is not None:
        VERIFY["shape_key_largest_difference_from_intended_m"] = float(np.abs(got - want).max())
        VERIFY["shape_key_points_moved"] = int((np.linalg.norm(got, axis=1) > 1e-5).sum())
        VERIFY["shape_key_largest_move_m"] = float(np.linalg.norm(got, axis=1).max())
    VERIFY["pass"] = bool(VERIFY["counts_equal"] and VERIFY["points_largest_difference_m"] == 0.0
                          and VERIFY["weights_largest_difference"] == 0.0 and VERIFY["weight_groups_equal"]
                          and VERIFY["uv_largest_difference"] == 0.0 and VERIFY["material_slots_equal"]
                          and VERIFY["face_materials_equal"] and VERIFY["corners_equal"]
                          and VERIFY["bone_names_and_parents_equal"] and VERIFY["shape_key_present"]
                          and VERIFY["shape_keys"][1] == ["Basis", NAME])
    log("VERIFY", json.dumps(VERIFY))


# ---- THE PREVIEW: front and side, at rest and at 25 down with the shape at its weight; the collar coloured by push -----
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"], "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"], "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"], "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"], "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."], "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"], "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."], "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"], "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"], "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."], "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."], "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."], "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."], "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."], ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    " ": ["....."] * 7, "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
}


def text(img, s, x, y, scale=3, colour=(20, 20, 20)):
    for ch in s.upper():
        g = FONT.get(ch, FONT[" "])
        for r, line in enumerate(g):
            for c, on in enumerate(line):
                if on == "#":
                    img[y + r * scale:y + (r + 1) * scale, x + c * scale:x + (c + 1) * scale] = colour
        x += 6 * scale


PW, PH, MPP = 640, 720, 0.0005          # panel size (px) and metres a pixel
CEN = AX_O + 0.035 * AX_A
SKIN_RGB, CLOTH_RGB = np.array([0.80, 0.66, 0.58]), np.array([0.45, 0.48, 0.53])


def push_rgb(t, on):
    """Where on (the push is over 0.5 mm): yellow rising to red at the largest push; else the cloth's grey."""
    t = np.clip(t, 0.0, 1.0)
    col = np.stack([0.95 - 0.10 * t, 0.85 * (1.0 - t) + 0.10, 0.15 * (1.0 - t) + 0.05], -1)
    return np.where(np.asarray(on)[..., None], col, CLOTH_RGB)


def panel(view, skin_pts, Jw, vpush, pmax):
    img = np.full((PH, PW, 3), 245, np.uint8)
    zb = np.full((PH, PW), np.inf)
    if view == "front":       # from in front (Blender -Y), his left on the right
        ax, dz_, look = 0, 1, np.array([0.0, 1.0, 0.0])
        sx = 1.0
    else:                     # from his left (+X), his front on the left
        ax, dz_, look = 1, 0, np.array([-1.0, 0.0, 0.0])
        sx = 1.0
    light = -look + np.array([0.0, 0.0, 0.6])
    light /= np.linalg.norm(light)

    def put(X, T, cols):
        x = (sx * (X[:, ax] - CEN[ax])) / MPP + PW / 2.0
        y = PH * 0.42 - (X[:, 2] - CEN[2]) / MPP
        z = X[:, dz_] * (1.0 if view == "front" else -1.0)
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
    for k, s in SKIN.items():
        put(skin_pts[k], s["T"], np.repeat(SKIN_RGB[None], len(s["T"]), 0))
    jt_push = vpush[JT].mean(1)
    put(Jw, JT, push_rgb(jt_push / max(pmax, 1e-9), jt_push > 0.0005))
    return img


def preview(path):
    pmax = float(PUSH.max())
    vpush = np.zeros(NV)
    vpush[:] = 0.0
    full = np.zeros(NP)
    full[BI] = PUSH
    vpush = full[PID]
    rows = []
    for name, w, label in (("rest", 0.0, "REST"), ("down25", POSE["down25"]["w"], "DOWN 25 SHAPE AT %.1f" % POSE["down25"]["w"])):
        Jw = place(name, w)
        skin_pts = {k: POSE[name]["skin"][k]["P"] for k in SKIN}
        pair = []
        for view in ("front", "side"):
            im = panel(view, skin_pts, Jw, vpush, pmax)
            text(im, "%s %s" % (label, view.upper()), 12, 12)
            pair.append(im)
        rows.append(np.concatenate(pair, 1))
    set_pose(0, 0)
    img = np.concatenate(rows, 0)
    bar = np.full((70, img.shape[1], 3), 245, np.uint8)
    ramp = push_rgb(np.linspace(0.0, 1.0, 400), np.ones(400, bool))
    bar[30:50, 150:550] = (np.repeat(ramp[None], 20, 0) * 255).astype(np.uint8)
    text(bar, "PUSH 0.5", 12, 33, 2)
    text(bar, "%d MM" % round(1000 * pmax), 560, 33, 2)
    img = np.concatenate([img, bar], 0)
    img[:, PW - 1:PW + 1] = 120
    img[PH - 1:PH + 1, :] = 120
    write_png(path, np.ascontiguousarray(img))


def write_png(path, a):
    raw = b"".join(b"\x00" + row.tobytes() for row in a)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", a.shape[1], a.shape[0], 8, 2, 0, 0, 0))
                 + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


PREVIEW = os.path.join(OUT, "collar-corrective-preview.png")
preview(PREVIEW)
log("wrote", PREVIEW)


# ---- THE RECORD -------------------------------------------------------------------------------------------------------
def grid(vals):
    """vals over the band's points: the largest per 15 degrees round the neck (columns) and 10 mm below the top (rows)."""
    cols = list(range(-165, 181, 15))
    out = {"columns_deg_from_front_his_left_positive": cols, "rows_mm_below_top_up_to": [], "mm": []}
    for r in range(10, int(round(DEPTH * 1000)) + 1, 10):
        sel_r = (B_B * 1000 < r) & (B_B * 1000 >= r - 10 if r > 10 else True)
        row = []
        for c0 in cols:
            sel = sel_r & (TH_B >= c0 - 7.5) & (TH_B < c0 + 7.5)
            row.append(round(1000 * float(vals[sel].max()), 1) if sel.any() else None)
        out["rows_mm_below_top_up_to"].append(r)
        out["mm"].append(row)
    return out


w1_rows = [CHECK[n] for n in W1]
after_all = [CHECK[n]["after"] for n, *_ in POSES if n != "rest"]
VERDICT = {
    "clears_every_weight1_pose": all(r["clears_at_its_weight"] for r in w1_rows),
    "clears_every_pose_at_its_weight": all(CHECK[n]["clears_at_its_weight"] for n, *_ in POSES),
    "crossing_after_total": int(sum(sum(r["crossing_skin_triangles"].values()) for r in after_all)),
    "top_edge_stretch_max_after": max(r["top_edge_stretch_max"] for r in after_all),
    "stretch_within_%.1f" % STRETCH_MAX: max(r["top_edge_stretch_max"] for r in after_all) <= STRETCH_MAX,
    "front_gap_max_after_mm": max((r["front_top_edge_gap_to_neck_max_mm"] if isinstance(r["front_top_edge_gap_to_neck_max_mm"], float)
                                   else 1000 * RAY_IN) for r in after_all),
    "gap_within_%d_mm" % round(1000 * GAP_MAX): all(isinstance(r["front_top_edge_gap_to_neck_max_mm"], float)
                                                   and r["front_top_edge_gap_to_neck_max_mm"] <= 1000 * GAP_MAX for r in after_all),
    "rest_unchanged": CHECK["rest"]["rest_moves_max_m"] < 1e-9,
}
record = {
    "made": "2026-11-02", "tool": "tools/meshgen/blender/collar_corrective.py",
    "inputs": {"jacket": JACKET, "body": BODY, "face": FACE},
    "outputs": {"fbx": OUT_FBX if WRITE else None, "preview": PREVIEW,
                "preview_layout": "top row at rest, bottom row 25 degrees down with the shape at its weight; left front, right "
                                  "from his left; the jacket grey where the shape moves it under 0.5 mm, yellow to red up to the largest push"},
    "settings": {"shape_key": NAME, "margin_mm": 1000 * MARGIN, "depth_mm": 1000 * DEPTH, "rings": RINGS,
                 "split_neck01_neck02_head": SPLIT, "pitch_full_deg": PITCH_FULL, "yaw_full_deg": YAW_FULL,
                 "spread_round_neck_deg": TH_FALL, "front_for_gap_deg": FRONT_DEG, "ray_out_mm": 1000 * RAY_OUT,
                 "ray_in_mm": 1000 * RAY_IN, "cap_mm_what_if": 1000 * CAP if CAP > 0 else None,
                 "weight_formula": "w = clamp(max(pitch_down / %g, |yaw| / %g), 0, 1), pitch and yaw as LedgerGarments.h "
                                   "HeadAgainstChest measures them on the body skeleton" % (PITCH_FULL, YAW_FULL)},
    "skeleton": {"rest_joint_max_difference": max(rest_check.values()), "signs": SIGN, "jacket_pose_at_import_max_deviation": pose_dev,
                 "neck_axis_from": AX_O.round(4).tolist(), "neck_axis_dir": AX_A.round(4).tolist()},
    "jacket": {"vertices": NV, "welded_points": NP, "parts": npart, "band_points": int(len(BI)),
               "band_triangles_by_material": {mat_names[m]: int(c) for m, c in zip(*np.unique(JMI[band_tris], return_counts=True))},
               "top_edge_points": int(len(TOPP)), "top_edge_length_m": round(float(REST_TOP_LEN.sum()), 4),
               "collar_top_above_neck01_mm": [round(1000 * TOP.min(), 1), round(1000 * TOP.max(), 1)],
               "outward_fraction": round(OUT_FRAC, 3), "flipped": FLIP < 0,
               "skinned_push_length_per_unit": [round(float(min(np.linalg.norm(POSE[n]["e"][BI], axis=1).min() for n in POSE)), 4),
                                                round(float(max(np.linalg.norm(POSE[n]["e"][BI], axis=1).max() for n in POSE)), 4)]},
    "skin": {k: {"triangles_near_neck": int(len(s["T"])), "outward_fraction": s["outward_fraction"], "flipped": s["flipped"]}
             for k, s in SKIN.items()},
    "rest_clearance_least_mm": mm(float(REST_CLEAR[np.isfinite(REST_CLEAR)].min())),
    "need_mm_worst_of_weight1_poses": grid(NEED0),
    "push_mm": grid(PUSH),
    "push_summary": SUMMARY,
    "iterations": history,
    "per_pose": CHECK,
    "verdict": VERDICT,
    "fbx_check_against_input": VERIFY,
    "notes": [
        "clearance is along each collar point's posed push direction: a ray out that leaves the skin means the point "
        "is inside it by that much (the push must carry it out that way); the probe of 30 October measured the nearest "
        "skin instead (19.4 mm at 20 down), which is shorter where the collar's front lies inside the jaw",
        "a ray out that enters skin (the rim tucked in a crease under the chin) is not a clip: counted as rim_tucked",
        "skin crossing is counted on the collar's band (within depth_mm of the top), the head-map tool's overlap test",
        "the full body's head and the head mesh are the same skin at the neck here (their numbers agree)",
        "skin_points_through is searched within 30 mm of the collar: a deepest of 29.99 means 30 mm or more",
        "a what-if with the push capped at 15 mm (--cap-mm 15 --no-fbx, same day) still stretched the top edge 1.38 and "
        "left 55 to 76 skin triangles crossing at the weight-1 poses: an outward push cannot clear the chin",
        "Blender cannot run the face rig's own neck joints: the game moves the throat further (UNVERIFIED here)",
    ],
}
with open(os.path.join(OUT, "collar-corrective-record.json"), "w", encoding="utf-8") as fh:
    json.dump(record, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
log("DONE", json.dumps({"verdict": VERDICT, "summary": SUMMARY, "fbx_check_pass": VERIFY["pass"] if VERIFY else None}))
