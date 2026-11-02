"""PAINT A METAHUMAN HEAD HIDDEN FACE MAP THAT SHRINKS THE THROAT BEHIND A COLLAR (2 November 2026, Tom).

    blender -b --factory-startup -P tools/ue/blender_head_hidden_face_map.py -- FACE.fbx BODY.fbx JACKET.fbx OUT_DIR
        [--size 2048] [--margin-mm 3] [--below-top-mm 10] [--above-seam-mm 15] [--rings 2] [--floor 0.12]
        [--split 0.4,0.3,0.3] [--poses down20:20:0,up20:-20:0,...]

FACE.fbx is the head (face) mesh as the game builds it (every LOD, UV layer "DiffuseUV"); BODY.fbx the full body with
its skeleton (the neck's joints); JACKET.fbx the jacket's skinned game file on the same skeleton, at rest.

WHY (2 November 2026). Tom wears a zip jacket with a stand collar. When his head tips down (sitting down, standing
up) skin of his throat comes through the collar's front: up to 19.4 mm at 20 degrees down (the probe of 30 October,
garments/tom/zip_jacket/collar2/probe3-v30.json). That throat belongs to the HEAD mesh, which runs down the neck
under the collar. Two tries on the jacket's weights failed; this third try uses Epic's own tool, a head hidden-face
map on the wardrobe item, which moves head vertices inward when the character is built.

THE ENGINE'S RULES (UE 5.8, MetaHumanGeometryRemoval.cpp, read 2 November 2026):
  - the map is sampled once per render vertex at its UV: pixel = floor(Wrap((UV + 1e-4) * Res, 0, Res - 1)), V the
    engine's V, top down, which is 1 - Blender's v for an FBX the engine wrote (GetHiddenFaceMapPixelForUV 333-340);
  - a value <= MaxCullValue (0.1) cuts faces (never here: no pixel at or below --floor, 0.12); >= MinKeepValue (0.9)
    leaves the vertex alone; in between it moves opposite its normal by MaxShrinkDistance * (1 - (value - 0.1) / 0.8)
    (ComputeShrinkWeight 404-410, RemoveAndShrinkGeometry 602-636);
  - a 3D point with several render copies (UV seams, hard edges) moves by the average of its shrinking copies'
    moves (ShrinkDelta / ShrinkCount, 625-627 and 730);
  - the shrink is applied once, to the bind pose, before skinning: not per pose;
  - on the face mesh only the skin material slots are processed (MetaHumanDefaultEditorPipelineBase.cpp 755-763);
  - the texture is read from its source, as linear only when its sRGB box is OFF (Texture.cpp,
    FTextureSource::GetGammaSpace 3189-3211): with sRGB on, 0.12 reads as about 0.013 and CUTS the throat;
  - MaxShrinkDistance is in the mesh's units, the engine's centimetres (UNVERIFIED: read from the code, no build).

WHAT IT DOES:
  1. poses the three skeletons identically by joint name (head down 0, 10, 20, 25, 30 degrees; turned 45 left and
     right; 20 down with 45 turned each way), the rotation split over neck_01, neck_02 and head (--split), each about
     the joint's own side-to-side axis (and its own long axis for the turn), and prints the head joint's world
     rotation in each skeleton per pose;
  2. per head skin point and pose, its signed depth through the posed jacket: the nearest cloth point, signed by the
     cloth's outward normal (tested, flipped if inward), positive = skin outside the cloth; a nearest point beside an
     edge of the cloth (above the collar's top) is not "through". Skin that was behind the cloth at rest and ends
     outside it came THROUGH; skin that showed above the collar at rest and ends in front of it below the collar's
     top went OVER THE RIM (the rim sinks into visible skin): counted apart, a head map cannot fix it;
  3. at rest, "under the collar": behind the cloth (a ray out from the neck axis through the point meets it within
     60 mm), at least --below-top-mm below the collar's top edge at the same angle round the neck axis (neck_01 to
     head), at least --above-seam-mm above the head's open seam with the body, by angle and by distance;
  4. need = max(0, worst depth + --margin-mm) under the collar, 0 elsewhere, smoothed over --rings rings without
     falling below the need and without touching a point not under the collar;
  5. MaxShrinkDistance = the largest need; grey = 0.9 - 0.8 * need / max, clamped to [--floor, 1], white at no need;
  6. paints the map (white, triangles with a grey corner filled by interpolation, each vertex's own pixel and a
     2-pixel ring set to its value, nearest vertex winning), reads the PNG back and samples it at every vertex of
     every LOD as the engine does;
  7. moves every point in as the engine would and measures every pose again, for every LOD.

OUT_DIR gets tom_head_hidden_faces.png (8-bit grey, linear: import with sRGB OFF), head-map-record.json and
head-map-preview.png (the map over the UV layout; shrunk points red, points it cannot fix green).
"""
import json
import math
import os
import struct
import sys
import zlib

import numpy as np

# ---- THE PURE RULES (no Blender needed) ----------------------------------------------------------------------------
CULL, KEEP = 0.1, 0.9          # the engine's MaxCullValue and MinKeepValue defaults (MetaHumanGeometryRemovalTypes.h)


def clamp(x, lo, hi):
    return np.minimum(np.maximum(x, lo), hi)


def need_of(worst_depth, margin):
    """How far a point must move in: its worst depth through the cloth plus the margin, never below 0 (metres)."""
    return np.maximum(0.0, np.asarray(worst_depth, float) + margin)


def grey_of(need, max_need, floor):
    """The map's value for a need: 0.9 at no shrink falling to 0.1 at max_need, clamped to [floor, 1]; white where
    nothing is needed."""
    need = np.asarray(need, float)
    g = clamp(KEEP - (KEEP - CULL) * need / max(max_need, 1e-12), floor, 1.0)
    return np.where(need > 0.0, g, 1.0)


def shrink_weight(value):
    """The engine's ComputeShrinkWeight (MetaHumanGeometryRemoval.cpp 404-410): 1 at CULL, 0 at KEEP and above."""
    return 1.0 - clamp((np.asarray(value, float) - CULL) / (KEEP - CULL), 0.0, 1.0)


def wrap(x, span):
    """FMath::Wrap(x, 0, span) for arrays."""
    x = np.asarray(x, float)
    return np.where(x < 0, x + span * np.ceil(-x / span), np.where(x > span, x - span * np.ceil((x - span) / span), x))


def engine_pixel(u, v_engine, size):
    """GetHiddenFaceMapPixelForUV (333-340): floor(Wrap((UV + KINDA_SMALL_NUMBER) * Res, 0, Res - 1))."""
    return (np.floor(wrap((np.asarray(u) + 1e-4) * size, size - 1.0)).astype(int),
            np.floor(wrap((np.asarray(v_engine) + 1e-4) * size, size - 1.0)).astype(int))


def byte_of(grey, floor):
    """8-bit value of a grey: rounded, never at or below the floor, white kept 255."""
    lo = int(math.floor(floor * 255.0)) + 1
    b = np.rint(np.asarray(grey, float) * 255.0)
    return np.where(np.asarray(grey) >= 1.0, 255, np.maximum(lo, b)).astype(np.uint8)


# ---- BLENDER --------------------------------------------------------------------------------------------------------
import bpy  # noqa: E402
from mathutils import Quaternion, Vector  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402
from mathutils.kdtree import KDTree  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
FACE, BODY, JACKET, OUT = argv[:4]


def opt(n, d, f=float):
    return f(argv[argv.index(n) + 1]) if n in argv else d


SIZE = opt("--size", 2048, int)
MARGIN = opt("--margin-mm", 3.0) / 1000.0
BELOW_TOP = opt("--below-top-mm", 10.0) / 1000.0
ABOVE_SEAM = opt("--above-seam-mm", 15.0) / 1000.0
RINGS = opt("--rings", 2, int)
FLOOR = opt("--floor", 0.12)
SPLIT = [float(x) for x in opt("--split", "0.4,0.3,0.3", str).split(",")]
assert FLOOR > CULL, "the floor must stay above the engine's cut value"
JOINTS = ("neck_01", "neck_02", "head")
POSES = [("rest", 0, 0), ("down10", 10, 0), ("down20", 20, 0), ("down25", 25, 0), ("down30", 30, 0),
         ("left45", 0, 45), ("right45", 0, -45), ("down20_left45", 20, 45), ("down20_right45", 20, -45)]
if "--poses" in argv:   # name:down:left,... (degrees; negative down tips the head back); rest is always first
    POSES = [("rest", 0, 0)] + [(n, float(p), float(y)) for n, p, y in
                                (s.split(":") for s in opt("--poses", "", str).split(",") if s)]
NEAR = 0.10         # nearest-cloth search (m)
REACH = 0.06        # the ring test: a ray out from the point meets the cloth within this (m)
EDGE_RATIO = 0.5    # an offset to the nearest cloth point lying more along the cloth than across it: beside an edge
COLLAR_RHO = 0.13   # jacket points this close to the neck axis give the collar's top by angle (m)
BINS = 72
os.makedirs(OUT, exist_ok=True)


def log(*a):
    print("HEADMAP", *a, flush=True)


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


bpy.ops.wm.read_factory_settings(use_empty=True)
farm, fmeshes = import_fbx(FACE)
lods = {}
for o in fmeshes:
    n = o.name.rsplit("_LOD", 1)
    lods[int(n[1]) if len(n) == 2 and n[1].isdigit() else 0] = o
barm, _bm = import_fbx(BODY)
jarm, jmeshes = import_fbx(JACKET)
jacket = max(jmeshes, key=lambda m: len(m.data.vertices))
ARMS = {"face": farm, "body": barm, "jacket": jarm}
log("imported", {k: a.name for k, a in ARMS.items()}, "lods", sorted(lods), "jacket", jacket.name)


# ---- PER LOD: skin triangles, welded 3D points, render copies --------------------------------------------------------
def lod_data(o):
    me = o.data
    A = np.array(o.matrix_world)
    nv, nl, npo = len(me.vertices), len(me.loops), len(me.polygons)
    co = np.zeros(nv * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    mi = np.zeros(npo, int)
    me.polygons.foreach_get("material_index", mi)
    ls = np.zeros(npo, int)
    me.polygons.foreach_get("loop_start", ls)
    lt = np.zeros(npo, int)
    me.polygons.foreach_get("loop_total", lt)
    lv = np.zeros(nl, int)
    me.loops.foreach_get("vertex_index", lv)
    lay = me.uv_layers.get("DiffuseUV") or me.uv_layers.active
    luv = np.zeros(nl * 2)
    lay.data.foreach_get("uv", luv)
    luv = luv.reshape(-1, 2)
    cn = np.zeros(nl * 3)
    me.corner_normals.foreach_get("vector", cn)
    cn = cn.reshape(-1, 3)
    # the skin section: the largest (the FBX's slot names do not follow the polygons' indices on this file)
    skin = int(np.bincount(mi).argmax())
    T = [(ls[p], ls[p] + k, ls[p] + k + 1) for p in np.nonzero(mi == skin)[0] for k in range(1, lt[p] - 1)]
    TL = np.array(T, int)
    TV = lv[TL]
    sv = np.unique(TV)
    Wd = to_world(A, co)
    ln = cn @ np.linalg.inv(A[:3, :3])     # normals by the inverse transpose
    ln /= np.maximum(np.linalg.norm(ln, axis=1, keepdims=True), 1e-12)
    vuv = np.zeros((nv, 2))
    vuv[lv] = luv
    spread = np.zeros(nv)
    np.maximum.at(spread, lv, np.abs(luv - vuv[lv]).max(1))
    # weld copies at one position into 3D points
    kd = KDTree(len(sv))
    for i, v in enumerate(sv):
        kd.insert(Wd[v], i)
    kd.balance()
    par = list(range(len(sv)))

    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    for i, v in enumerate(sv):
        for _c, j, _d in kd.find_range(Wd[v], 1e-6):
            a, b = find(i), find(j)
            if a != b:
                par[max(a, b)] = min(a, b)
    _u, pidx = np.unique([find(i) for i in range(len(sv))], return_inverse=True)
    pid = np.full(nv, -1)
    pid[sv] = pidx
    NP = int(pidx.max()) + 1
    rep = np.zeros(NP, int)
    rep[pidx[::-1]] = sv[::-1]
    # render copies: the skin's corners by (vertex, normal)
    flat = TL.ravel()
    keys = np.concatenate([lv[flat][:, None].astype(float), np.round(ln[flat], 4)], 1)
    _k, first = np.unique(keys, axis=0, return_index=True)
    cl = flat[first]
    return {"obj": o, "me": me, "A": A, "co": co, "W": Wd, "skin": skin, "skin_slot": me.materials[skin].name if me.materials[skin] else None,
            "TV": TV, "TP": pid[TV], "sv": sv, "pid": pid, "rep": rep, "NP": NP, "vuv": vuv,
            "uv_spread": float(spread[sv].max()), "copy_v": lv[cl], "copy_n": ln[cl]}


L = {k: lod_data(o) for k, o in sorted(lods.items())}
L0 = L[0]
for k, d in L.items():
    log("lod", k, "skin slot", d["skin"], "triangles", len(d["TV"]), "vertices", len(d["sv"]), "points", d["NP"],
        "copies", len(d["copy_v"]), "uv spread per vertex", round(d["uv_spread"], 6))

# welded edges and neighbours of LOD0
TP0 = L0["TP"]
TP0 = TP0[(TP0[:, 0] != TP0[:, 1]) & (TP0[:, 1] != TP0[:, 2]) & (TP0[:, 2] != TP0[:, 0])]
E = np.sort(np.concatenate([TP0[:, [0, 1]], TP0[:, [1, 2]], TP0[:, [2, 0]]]), 1)
EU, ECNT = np.unique(E, axis=0, return_counts=True)
NBR = [[] for _ in range(L0["NP"])]
for a, b in EU:
    NBR[a].append(b)
    NBR[b].append(a)
badj = {}
for a, b in EU[ECNT == 1]:
    badj.setdefault(a, set()).add(b)
    badj.setdefault(b, set()).add(a)
seen, loops = set(), []
for s in badj:
    if s in seen:
        continue
    st, comp = [s], []
    while st:
        v = st.pop()
        if v in seen:
            continue
        seen.add(v)
        comp.append(v)
        st.extend(badj[v] - seen)
    loops.append(np.array(comp))
P0 = L0["W"][L0["rep"]]
SEAM_P = min(loops, key=lambda c: P0[c, 2].mean())
log("welded open boundaries", len(loops), "seam with the body: points", len(SEAM_P),
    "z %.4f..%.4f" % (P0[SEAM_P, 2].min(), P0[SEAM_P, 2].max()))

# ---- THE NECK AXIS (the full body's neck_01 to head, at rest) AND THE POSES -----------------------------------------
def joint(arm, name):
    return np.array(arm.matrix_world @ arm.data.bones[name].head_local)


AX_O = joint(barm, "neck_01")
AX_A = joint(barm, "head") - AX_O
AX_A /= np.linalg.norm(AX_A)
FRONT = np.array([0.0, -1.0, 0.0])   # the engine's +Y after the FBX's axis change (checked on the zip below)
AX_U = FRONT - (FRONT @ AX_A) * AX_A
AX_U /= np.linalg.norm(AX_U)
AX_W = np.cross(AX_A, AX_U)          # +90 degrees: towards +X


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
        d = max(abs(m[i][j] - ref[i][j]) for i in range(3) for j in range(4))
        rest_check["%s_%s_vs_face" % (name, k)] = round(d, 6)
log("rest joints differ from the face skeleton's by at most", max(rest_check.values()))


def own_axis(arm, name, world_axis):
    """The joint's own local axis lying nearest the world axis, signed to point along it, in the bone's frame."""
    R = np.array((arm.matrix_world.to_3x3().normalized() @ arm.data.bones[name].matrix_local.to_3x3()))
    k = int(np.argmax(np.abs(world_axis @ R)))
    e = np.zeros(3)
    e[k] = np.sign(world_axis @ R[:, k])
    return Vector(e), round(float(abs(world_axis @ R[:, k])), 4)


AXES = {}
axis_alignment = {}
for k, arm in ARMS.items():
    for name in JOINTS:
        side, cs = own_axis(arm, name, np.array([1.0, 0.0, 0.0]))
        up, cu = own_axis(arm, name, np.array([0.0, 0.0, 1.0]))
        AXES[(k, name)] = (side, up)
        axis_alignment["%s_%s" % (k, name)] = {"side_cos_to_x": cs, "long_cos_to_z": cu}
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


# which sign tips the face down and turns it to his left (+X, where the _l joints are)
probe = joint(farm, "head") + 0.10 * FRONT
set_pose(10, 0)
if head_moves(farm, probe)[2] > probe[2]:
    SIGN["pitch"] = -1.0
set_pose(0, 10)
LEFT = np.sign(joint(farm, "clavicle_l")[0]) or 1.0
if (head_moves(farm, probe)[0] - probe[0]) * LEFT < 0:
    SIGN["yaw"] = -1.0
set_pose(0, 0)
log("signs", SIGN, "his left is", "+X" if LEFT > 0 else "-X")

# ---- THE JACKET -------------------------------------------------------------------------------------------------------
jme = jacket.data
jme.calc_loop_triangles()
JT = np.zeros(len(jme.loop_triangles) * 3, int)
jme.loop_triangles.foreach_get("vertices", JT)
JT = JT.reshape(-1, 3)
JMI = np.zeros(len(jme.loop_triangles), int)
jme.loop_triangles.foreach_get("material_index", JMI)
FLIP = 1.0


def jacket_bvh(Jw):
    a, b, c = Jw[JT[:, 0]], Jw[JT[:, 1]], Jw[JT[:, 2]]
    n = np.cross(b - a, c - a)
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-15)
    return BVHTree.FromPolygons(Jw.tolist(), JT.tolist(), all_triangles=True), n * FLIP


JE = np.unique(np.sort(np.concatenate([JT[:, [0, 1]], JT[:, [1, 2]], JT[:, [2, 0]]]), 1), axis=0)


def collar_top(Jw):
    """The collar's top edge by angle round the neck axis: the highest jacket point per 5 degrees, taken from points
    every few millimetres along the jacket's edges near the axis (its rim's corners lie about 7 degrees apart)."""
    a, b = Jw[JE[:, 0]], Jw[JE[:, 1]]
    ra, rb = cyl(a)[2], cyl(b)[2]
    keep = (ra < COLLAR_RHO) & (rb < COLLAR_RHO)
    t = np.linspace(0.0, 1.0, 9)
    pts = (a[keep][:, None, :] * (1 - t)[None, :, None] + b[keep][:, None, :] * t[None, :, None]).reshape(-1, 3)
    h, th, _r, _rd = cyl(pts)
    return angle_table(th, h)


J0 = evaluated_world(jacket)
TOP, top_empty = collar_top(J0)
ph, pth, _pr, _prad = cyl(P0[SEAM_P])
SEAM, seam_empty = angle_table(pth, ph)
log("collar top above neck_01: %.1f..%.1f mm (z %.4f..%.4f); seam %.1f..%.1f mm; empty bins %d / %d" % (
    1000 * TOP.min(), 1000 * TOP.max(), (AX_O + TOP.min() * AX_A)[2], (AX_O + TOP.max() * AX_A)[2],
    1000 * SEAM.min(), 1000 * SEAM.max(), top_empty, seam_empty))

# outward normals: in the collar's band, faces facing round the neck should face away from it
bvh0, tn0 = jacket_bvh(J0)
cen = (J0[JT[:, 0]] + J0[JT[:, 1]] + J0[JT[:, 2]]) / 3.0
ch, cth, crho, crad = cyl(cen)
band = (crho < COLLAR_RHO) & (ch > at_angle(TOP, cth) - 0.06)
radial = np.einsum("ij,ij->i", tn0[band], crad[band])
facing = np.abs(radial) > 0.5
out_frac = float((radial[facing] > 0).mean()) if facing.any() else float("nan")
if out_frac < 0.5:
    FLIP = -1.0
    bvh0, tn0 = jacket_bvh(J0)
log("collar band faces facing round the neck:", int(facing.sum()), "outward fraction %.3f" % out_frac, "flip", FLIP < 0)
# layers: rays out from the axis through the collar, 12 angles x 3 heights
layers = []
for th in range(0, 360, 30):
    t = math.radians(th - 360.0 if th > 180 else th)
    d = math.cos(t) * AX_U + math.sin(t) * AX_W
    for dz in (0.012, 0.025, 0.040):
        hh = float(at_angle(TOP, [math.degrees(t)])[0]) - dz
        p = Vector(AX_O + hh * AX_A)
        n_hits = 0
        for _ in range(8):
            hit = bvh0.ray_cast(p, Vector(d), 0.3)
            if hit[0] is None:
                break
            n_hits += 1
            p = hit[0] + Vector(d) * 1e-5
        layers.append(n_hits)
zip_check = None
for i, m in enumerate(jme.materials):
    if m and any(s in m.name.lower() for s in ("tape", "zip")):
        sel = JMI == i
        if sel.any():
            zc = cen[sel].mean(0)
            zip_check = {"material": m.name, "angle_deg_round_neck": round(float(cyl(zc[None])[1][0]), 1)}
log("cloth layers per ray through the collar:", dict(zip(*np.unique(layers, return_counts=True))), "zip", zip_check)


def depths(Pw, bvh, tn):
    """Signed depth through the cloth, positive = skin outside it; beside an edge of the cloth = -distance."""
    out = np.full(len(Pw), -NEAR)
    for i, p in enumerate(Pw):
        hit = bvh.find_nearest(Vector(p), NEAR)
        if hit[0] is None:
            continue
        d = p - np.array(hit[0])
        s = float(d @ tn[hit[2]])
        out[i] = -hit[3] if (hit[3] > 1e-7 and abs(s) < EDGE_RATIO * hit[3]) else s
    return out


def behind_cloth(Pw, bvh):
    """At rest: a ray out from the neck axis through the point meets the cloth within REACH beyond it."""
    _h, _t, _r, rad = cyl(Pw)
    out = np.zeros(len(Pw), bool)
    for i in range(len(Pw)):
        d = Vector(rad[i])
        out[i] = bvh.ray_cast(Vector(Pw[i]) + d * 1e-5, d, REACH)[0] is not None
    return out


# ---- AT REST: which points are under the collar ---------------------------------------------------------------------
h0, th0, rho0, rad0 = cyl(P0)
top0 = at_angle(TOP, th0)
seam0 = at_angle(SEAM, th0)
kd = KDTree(len(SEAM_P))
for i, p in enumerate(SEAM_P):
    kd.insert(P0[p], i)
kd.balance()
dseam = np.array([kd.find(P0[i])[2] for i in range(L0["NP"])])
for d in L.values():
    d["behind"] = behind_cloth(d["W"][d["rep"]], bvh0)
behind0 = L0["behind"]
UNDER = behind0 & (top0 - h0 >= BELOW_TOP) & (h0 - seam0 >= ABOVE_SEAM) & (dseam >= ABOVE_SEAM)
VIS0 = h0 > top0
log("points", L0["NP"], "behind the cloth", int(behind0.sum()), "under the collar", int(UNDER.sum()),
    "visible above the collar", int(VIS0.sum()))

def crossings(Pall, bvh_j):
    """Skin triangles of LOD0 that cross cloth triangles (the visible clip line), sorted by where their points lie at
    rest: all under the collar (a head map can fix), any above the collar's top (skin that shows at rest: it cannot),
    or the rest (the 0-10 mm band under the top, near the seam, off the neck)."""
    sb = BVHTree.FromPolygons(Pall.tolist(), L0["TV"].tolist(), all_triangles=True)
    tris = np.unique([p[0] for p in sb.overlap(bvh_j)]).astype(int)
    pts = L0["TP"][tris] if len(tris) else np.zeros((0, 3), int)
    under_t = UNDER[pts].all(1)
    above_t = VIS0[pts].any(1)
    rel = (h0 - top0)[pts.ravel()] if len(tris) else np.zeros(0)
    return {"skin_triangles": int(len(tris)), "all_points_under_collar": int(under_t.sum()),
            "touching_skin_above_collar_top_at_rest": int(above_t.sum()), "other": int((~under_t & ~above_t).sum()),
            "rest_height_vs_collar_top_mm": [round(1000 * float(rel.min()), 1), round(1000 * float(rel.max()), 1)] if len(rel) else None}


# ---- THE POSES, BEFORE ----------------------------------------------------------------------------------------------
pose_log, JW, over_rim, cross_b, cross_a = {}, {}, {}, {}, {}
before = {k: {} for k in L}
for name, pitch, yaw in POSES:
    set_pose(pitch, yaw)
    rots = {}
    for k, arm in ARMS.items():
        M = arm.matrix_world @ arm.pose.bones["head"].matrix
        R = arm.matrix_world @ arm.data.bones["head"].matrix_local
        q, q0 = M.to_3x3().normalized().to_quaternion(), R.to_3x3().normalized().to_quaternion()
        rots[k] = (q, q @ q0.inverted())
    world = rots["face"][1].to_euler("XYZ")
    spread = max(rots["face"][0].rotation_difference(rots[k][0]).angle for k in ARMS)
    pose_log[name] = {"pitch_down_deg": pitch, "turn_left_deg": yaw,
                      "head_world_rotation_from_rest_xyz_deg": [round(math.degrees(a), 2) for a in world],
                      "head_angle_from_rest_deg": round(math.degrees(rots["face"][1].angle), 2),
                      "head_rotation_spread_between_skeletons_deg": round(math.degrees(spread), 4)}
    log("pose", name, "head joint world rotation from rest (x, y, z deg)", pose_log[name]["head_world_rotation_from_rest_xyz_deg"],
        "angle", pose_log[name]["head_angle_from_rest_deg"], "spread between face/body/jacket skeletons",
        pose_log[name]["head_rotation_spread_between_skeletons_deg"])
    JW[name] = evaluated_world(jacket)
    bvh, tn = jacket_bvh(JW[name])
    for k, d in L.items():
        Pall = evaluated_world(d["obj"])
        Pp = Pall[d["rep"]]
        before[k][name] = depths(Pp, bvh, tn)
        if k == 0:
            cross_b[name] = crossings(Pall, bvh)
            topp, _e = collar_top(JW[name])
            hp, tp, _r, _rd = cyl(Pp)
            # skin that was NOT behind the cloth at rest and now lies in front of it, below the collar's top: the
            # collar's rim sinks into skin that shows at rest (a head map could only fix it by moving visible skin)
            OVER = ~behind0 & (before[0][name] > 0) & (hp < at_angle(topp, tp))
            over_rim[name] = OVER
set_pose(0, 0)

D0 = np.stack([before[0][n] for n, _p, _y in POSES])
WORST = D0.max(0)
rest_gap = before[0]["rest"]

# ---- THE NEED, SMOOTHED; THE GREYS ----------------------------------------------------------------------------------
need = np.where(UNDER, need_of(WORST, MARGIN), 0.0)
smooth = need.copy()
for _r in range(RINGS):
    nxt = smooth.copy()
    for i in np.nonzero(UNDER)[0]:
        ring = [i] + NBR[i]
        nxt[i] = max(smooth[i], float(smooth[ring].mean()))
    smooth = nxt
MAXS = float(smooth.max())
GREY = grey_of(smooth, MAXS, FLOOR) if MAXS > 0 else np.ones(L0["NP"])
through = behind0 & (WORST > 0)
unfixable = through & ~UNDER
OVER_ANY = np.any(np.stack([over_rim[n] for n, _p, _y in POSES]), 0)
log("max shrink %.2f mm; points shrunk %d; through in some pose %d, of them not under the collar %d" % (
    1000 * MAXS, int((smooth > 0).sum()), int(through.sum()), int(unfixable.sum())))

# ---- THE MAP ----------------------------------------------------------------------------------------------------------
W = H = SIZE
img = np.ones((H, W))
vgrey = np.ones(len(L0["co"]))
vgrey[L0["sv"]] = GREY[L0["pid"][L0["sv"]]]


def pix_coords(d):
    u, ve = d["vuv"][:, 0], 1.0 - d["vuv"][:, 1]
    return wrap((u + 1e-4) * SIZE, SIZE - 1.0), wrap((ve + 1e-4) * SIZE, SIZE - 1.0)


X0, Y0 = pix_coords(L0)
filled = 0
for t in L0["TV"]:
    g = vgrey[t]
    if g.min() >= 1.0:
        continue
    xs, ys = X0[t], Y0[t]
    den = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
    if abs(den) < 1e-9:
        continue
    x_lo, x_hi = max(0, int(math.floor(xs.min())) - 1), min(W - 1, int(math.ceil(xs.max())) + 1)
    y_lo, y_hi = max(0, int(math.floor(ys.min())) - 1), min(H - 1, int(math.ceil(ys.max())) + 1)
    gx, gy = np.meshgrid(np.arange(x_lo, x_hi + 1) + 0.5, np.arange(y_lo, y_hi + 1) + 0.5)
    l0 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / den
    l1 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / den
    l2 = 1.0 - l0 - l1
    lam = np.stack([l0, l1, l2])
    inside = (lam >= -0.05).all(0)
    lam = clamp(lam, 0.0, 1.0)
    lam /= lam.sum(0)
    val = lam[0] * g[0] + lam[1] * g[1] + lam[2] * g[2]
    sub = img[y_lo:y_hi + 1, x_lo:x_hi + 1]
    sub[inside] = np.minimum(sub[inside], val[inside])
    filled += 1
sv0 = L0["sv"]
px0, py0 = engine_pixel(L0["vuv"][sv0, 0], 1.0 - L0["vuv"][sv0, 1], SIZE)
grey_px = img[py0, px0].copy()          # what the fill alone gave each vertex's own pixel
cx, cy, cv, cd = [], [], [], []
for dy in range(-2, 3):
    for dx in range(-2, 3):
        x, y = px0 + dx, py0 + dy
        ok = (x >= 0) & (x < W) & (y >= 0) & (y < H)
        cx.append(x[ok]); cy.append(y[ok]); cv.append(vgrey[sv0][ok])
        cd.append(np.hypot(x[ok] + 0.5 - X0[sv0][ok], y[ok] + 0.5 - Y0[sv0][ok]))
cx, cy, cv, cd = (np.concatenate(a) for a in (cx, cy, cv, cd))
key = cy * W + cx
order = np.lexsort((cd, key))
firsts = order[np.r_[True, key[order][1:] != key[order][:-1]]]
img[cy[firsts], cx[firsts]] = cv[firsts]
# each vertex's own pixel, exact; two vertices on one pixel with different values are counted
own_key = py0 * W + px0
own_order = np.lexsort((np.hypot(px0 + 0.5 - X0[sv0], py0 + 0.5 - Y0[sv0]), own_key))
ok_first = own_order[np.r_[True, own_key[own_order][1:] != own_key[own_order][:-1]]]
img[py0[ok_first], px0[ok_first]] = vgrey[sv0][ok_first]
shared = {}
for k, v in zip(own_key, vgrey[sv0]):
    shared.setdefault(int(k), set()).add(round(float(v), 4))
pixel_conflicts = sum(1 for s in shared.values() if len(s) > 1)
BYTES = byte_of(img, FLOOR)


def write_png(path, a):
    colour = 0 if a.ndim == 2 else 2
    raw = b"".join(b"\x00" + row.tobytes() for row in a)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", a.shape[1], a.shape[0], 8, colour, 0, 0, 0))
                 + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


MAP = os.path.join(OUT, "tom_head_hidden_faces.png")
write_png(MAP, BYTES)

# ---- READ IT BACK AND SAMPLE IT AS THE ENGINE DOES ------------------------------------------------------------------
im = bpy.data.images.load(MAP)
im.colorspace_settings.name = "Non-Color"
iw, ih = im.size
READ = np.array(im.pixels[:], np.float32).reshape(ih, iw, -1)[::-1][..., 0]   # top row first, as the engine reads


def sample(d):
    u, ve = d["vuv"][d["sv"], 0], 1.0 - d["vuv"][d["sv"], 1]
    x, y = engine_pixel(u, ve, iw)
    return READ[y, x]


checks = {"png_size": [iw, ih], "png_min": round(float(READ.min()), 4), "png_bytes_min": int(BYTES.min()),
          "pixels_at_or_below_floor": int((READ <= FLOOR).sum()), "pixels_at_or_below_cull": int((READ <= CULL).sum()),
          "lod0_vertex_pixels_shared_with_a_different_value": pixel_conflicts,
          "lod0_triangles_filled": filled,
          "lod0_white_vertices_whose_pixel_the_fill_made_grey": int(((vgrey[sv0] >= 1.0) & (grey_px < KEEP)).sum())}
s0 = sample(L0)
diff = np.abs(s0 - vgrey[sv0])
checks["lod0"] = {"vertices": int(len(sv0)), "min": round(float(s0.min()), 4),
                  "at_or_below_floor": int((s0 <= FLOOR).sum()), "max_diff_from_intended_255ths": round(float(diff.max() * 255), 2),
                  "over_2_255ths": int((diff > 2 / 255.0).sum()), "shrinking": int((s0 < KEEP).sum())}
jit = 0
for ddx, ddy in ((-0.5, 0), (0.5, 0), (0, -0.5), (0, 0.5)):
    x = np.floor(wrap(X0[sv0] + ddx, SIZE - 1.0)).astype(int)
    y = np.floor(wrap(Y0[sv0] + ddy, SIZE - 1.0)).astype(int)
    jit += int((np.abs(READ[y, x] - vgrey[sv0]) > 2 / 255.0).sum())
checks["lod0"]["half_pixel_jitter_over_2_255ths"] = jit

# the LODs' UV layout against LOD0's, and their samples
tri0 = BVHTree.FromPolygons(L0["W"].tolist(), L0["TV"].tolist(), all_triangles=True)
uvp = L0["vuv"]
for k, d in L.items():
    if k == 0:
        continue
    s = sample(d)
    P = d["W"][d["sv"]]
    hh, tt, _r, _rd = cyl(P)
    vis = hh > at_angle(TOP, tt)
    dpx = []
    for i, p in enumerate(P):
        hit = tri0.find_nearest(Vector(p), 0.01)
        if hit[0] is None:
            dpx.append(np.nan)
            continue
        # every LOD0 triangle about as near (both sides of a UV seam), the closest UV kept
        best = np.inf
        for loc, _n, ti, _dist in tri0.find_nearest_range(Vector(p), hit[3] + 0.001):
            a, b, c = (L0["W"][j] for j in L0["TV"][ti])
            v0, v1, v2 = b - a, c - a, np.array(loc) - a
            d00, d01, d11, d20, d21 = v0 @ v0, v0 @ v1, v1 @ v1, v2 @ v0, v2 @ v1
            den = d00 * d11 - d01 * d01
            bb = (d11 * d20 - d01 * d21) / den if den else 0.0
            cc = (d00 * d21 - d01 * d20) / den if den else 0.0
            uvq = (1 - bb - cc) * uvp[L0["TV"][ti][0]] + bb * uvp[L0["TV"][ti][1]] + cc * uvp[L0["TV"][ti][2]]
            best = min(best, float(np.abs(uvq - d["vuv"][d["sv"][i]]).max() * SIZE))
        dpx.append(best)
    dpx = np.array(dpx)
    neck = P[:, 2] < 1.70
    checks["lod%d" % k] = {"vertices": int(len(s)), "min": round(float(s.min()), 4), "at_or_below_floor": int((s <= FLOOR).sum()),
                           "shrinking": int((s < KEEP).sum()), "shrinking_above_the_collar_at_rest": int(((s < KEEP) & vis).sum()),
                           "uv_vs_lod0_px_median": round(float(np.nanmedian(dpx)), 2),
                           "uv_vs_lod0_px_p95": round(float(np.nanpercentile(dpx, 95)), 2),
                           "uv_vs_lod0_px_p95_neck": round(float(np.nanpercentile(dpx[neck], 95)), 2) if neck.any() else None,
                           "uv_vs_lod0_over_8px": int((dpx > 8).sum())}
log("sample check", json.dumps(checks))

# ---- SIMULATE THE BUILD: every LOD moved in as the engine would, then the poses again ---------------------------------
def shrink_lod(d):
    s = np.ones(len(d["co"]))
    s[d["sv"]] = sample(d)
    w = shrink_weight(s)[d["copy_v"]]
    p = d["pid"][d["copy_v"]]
    acc = np.zeros((d["NP"], 3))
    np.add.at(acc, p, -(w[:, None] * d["copy_n"]))
    cnt = np.bincount(p[w > 0], minlength=d["NP"]).astype(float)
    delta = MAXS * acc / np.maximum(cnt, 1.0)[:, None]
    Wn = d["W"].copy()
    Wn[d["sv"]] += delta[d["pid"][d["sv"]]]
    loc = (Wn - d["A"][:3, 3]) @ np.linalg.inv(d["A"][:3, :3]).T
    d["me"].vertices.foreach_set("co", loc.ravel())
    if d["me"].shape_keys:
        d["me"].shape_keys.reference_key.data.foreach_set("co", loc.ravel())
    d["me"].update()
    return delta


DELTA = {k: shrink_lod(d) for k, d in L.items()}
after = {k: {} for k in L}
r_disp = np.einsum("ij,ij->i", DELTA[0], rad0)
steps_pose = {}
for name, pitch, yaw in POSES:
    set_pose(pitch, yaw)
    bvh, tn = jacket_bvh(JW[name])
    for k, d in L.items():
        Pall = evaluated_world(d["obj"])
        Pp = Pall[d["rep"]]
        after[k][name] = depths(Pp, bvh, tn)
        if k == 0:
            cross_a[name] = crossings(Pall, bvh)
            topp, _e = collar_top(JW[name])
            hp, tp, _r, _rd = cyl(Pp)
            visp = hp > at_angle(topp, tp)
            both = visp[EU[:, 0]] & visp[EU[:, 1]]
            st = np.abs(r_disp[EU[both, 0]] - r_disp[EU[both, 1]])
            moved = np.linalg.norm(DELTA[0], axis=1) > 1e-4
            steps_pose[name] = {"largest_radial_step_between_neighbours_above_the_collar_mm": round(1000 * float(st.max()) if len(st) else 0.0, 2),
                                "shrunk_points_above_the_collar": int((visp & moved).sum()),
                                "their_largest_shrink_mm": round(1000 * float(np.linalg.norm(DELTA[0][visp & moved], axis=1).max()) if (visp & moved).any() else 0.0, 2)}
set_pose(0, 0)


def deepest(arr, sel):
    return round(1000 * float(arr[sel].max()), 2) if sel.any() else None


per_pose = {}
for name, _p, _y in POSES:
    b, a = before[0][name], after[0][name]
    per_pose[name] = {"deepest_before_mm": deepest(b, behind0), "deepest_after_mm": deepest(a, behind0),
                      "under_collar_deepest_before_mm": deepest(b, UNDER), "under_collar_deepest_after_mm": deepest(a, UNDER),
                      "not_under_deepest_before_mm": deepest(b, behind0 & ~UNDER), "not_under_deepest_after_mm": deepest(a, behind0 & ~UNDER),
                      "points_through_before": int((behind0 & (b > 0)).sum()), "points_through_after": int((behind0 & (a > 0)).sum()),
                      "crossing_before": cross_b[name], "crossing_after": cross_a[name],
                      "over_the_rim_points": int(over_rim[name].sum()), "over_the_rim_deepest_mm": deepest(b, over_rim[name]),
                      "over_the_rim_rest_height_above_collar_top_mm": [round(1000 * float((h0 - top0)[over_rim[name]].min()), 1),
                                                                      round(1000 * float((h0 - top0)[over_rim[name]].max()), 1)] if over_rim[name].any() else None,
                      "lods_deepest_before_after_mm": {k: [deepest(before[k][name], L[k]["behind"]), deepest(after[k][name], L[k]["behind"])]
                                                       for k in L if k},
                      **steps_pose[name]}
    log("pose", name, json.dumps(per_pose[name]))

vis_edges = VIS0[EU[:, 0]] & VIS0[EU[:, 1]]
rest_step = float(np.abs(r_disp[EU[vis_edges, 0]] - r_disp[EU[vis_edges, 1]]).max()) if vis_edges.any() else 0.0
all_step = float(np.abs(r_disp[EU[:, 0]] - r_disp[EU[:, 1]]).max())
shrunk = smooth > 0
uf = np.nonzero(unfixable)[0]
uf = uf[np.argsort(-WORST[uf])]
record = {
    "made": "2026-11-02", "tool": "tools/ue/blender_head_hidden_face_map.py",
    "inputs": {"face": FACE, "body": BODY, "jacket": JACKET},
    "settings": {"size": SIZE, "margin_mm": MARGIN * 1000, "below_top_mm": BELOW_TOP * 1000, "above_seam_mm": ABOVE_SEAM * 1000,
                 "rings": RINGS, "floor": FLOOR, "split_neck01_neck02_head": SPLIT, "edge_ratio": EDGE_RATIO, "reach_mm": REACH * 1000,
                 "cull": CULL, "keep": KEEP},
    "texture_import": "PNG is 8-bit linear grey: import with sRGB OFF (else 0.12 reads ~0.013 and cuts); "
                      "MinKeepValue 0.9, MaxCullValue 0.1 (defaults); MaxShrinkDistance below, in cm",
    "MaxShrinkDistance_mm": round(1000 * MAXS, 3), "MaxShrinkDistance_cm": round(100 * MAXS, 4),
    "MaxShrinkDistance_unit_note": "the engine moves ImportedData points in the mesh's units, centimetres (UNVERIFIED, read from code)",
    "skeleton": {"rest_joint_max_difference": max(rest_check.values()), "signs": SIGN, "axes": axis_alignment,
                 "neck_axis_from": AX_O.round(4).tolist(), "neck_axis_dir": AX_A.round(4).tolist(), "front": FRONT.tolist(),
                 "zip_check": zip_check},
    "poses": pose_log,
    "jacket": {"collar_band_faces_facing_round": int(facing.sum()), "outward_fraction": round(out_frac, 3), "flipped": FLIP < 0,
               "layers_per_ray_through_collar": {int(k): int(v) for k, v in zip(*np.unique(layers, return_counts=True))},
               "collar_top_above_neck01_mm": [round(1000 * TOP.min(), 1), round(1000 * TOP.max(), 1)],
               "collar_top_z_m": [round(float((AX_O + TOP.min() * AX_A)[2]), 4), round(float((AX_O + TOP.max() * AX_A)[2]), 4)]},
    "head": {"lod0_points": L0["NP"], "lod0_render_vertices": int(len(sv0)), "lod0_copies": int(len(L0["copy_v"])),
             "uv_spread_per_vertex": {k: d["uv_spread"] for k, d in L.items()},
             "skin_section": {k: [d["skin"], d["skin_slot"]] for k, d in L.items()},
             "seam_z_m": [round(float(P0[SEAM_P, 2].min()), 4), round(float(P0[SEAM_P, 2].max()), 4)],
             "seam_above_neck01_mm": [round(1000 * SEAM.min(), 1), round(1000 * SEAM.max(), 1)],
             "rest_gap_under_collar_mm": {"closest": deepest(rest_gap, UNDER)}},
    "counts": {"behind_cloth_at_rest": int(behind0.sum()), "under_collar": int(UNDER.sum()),
               "through_in_some_pose": int(through.sum()), "through_and_under": int((through & UNDER).sum()),
               "through_not_under_cannot_fix": int(unfixable.sum()),
               "shown_at_rest_then_in_front_of_collar_below_its_top_in_some_pose": int(OVER_ANY.sum()),
               "note": "the clip itself is per_pose.crossing_* (skin triangles crossing cloth); in-front-below-top "
                       "also counts the chin hanging over a rim tucked in its crease, which is not a clip",
               "points_shrunk": int(shrunk.sum()), "render_vertices_shrunk_lod0": checks["lod0"]["shrinking"]},
    "not_fixable": [{"worst_mm": round(1000 * WORST[i], 1), "z_m": round(float(P0[i, 2]), 4), "below_top_mm": round(1000 * float(top0[i] - h0[i]), 1),
                     "above_seam_mm": round(1000 * float(h0[i] - seam0[i]), 1), "angle_deg": round(float(th0[i]), 0),
                     "worst_pose": POSES[int(D0[:, i].argmax())][0]} for i in uf[:80]],
    "need_mm": {"max": round(1000 * MAXS, 2), "median_of_shrunk": round(1000 * float(np.median(smooth[shrunk])), 2) if shrunk.any() else 0.0},
    "per_pose": per_pose,
    "steps": {"largest_radial_step_between_neighbours_visible_at_rest_mm": round(1000 * rest_step, 3),
              "largest_shrink_of_a_point_visible_at_rest_mm": round(1000 * float(np.linalg.norm(DELTA[0][VIS0], axis=1).max()), 3),
              "largest_radial_step_between_any_neighbours_mm": round(1000 * all_step, 2)},
    "sample_check": checks,
}
with open(os.path.join(OUT, "head-map-record.json"), "w", encoding="utf-8") as fh:
    json.dump(record, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))

# ---- PREVIEW: the map over the UV layout (left), a close view of the shrunk part (right) ------------------------------
def draw_segments(canvas, p0, p1, colour):
    ch_, cw_ = canvas.shape[:2]
    n = np.minimum(np.ceil(np.linalg.norm(p1 - p0, axis=1)).astype(int) + 1, 4096)
    idx = np.repeat(np.arange(len(p0)), n)
    t = (np.arange(n.sum()) - np.repeat(np.cumsum(n) - n, n)) / np.repeat(np.maximum(n - 1, 1), n)
    pts = p0[idx] + (p1 - p0)[idx] * t[:, None]
    x, y = pts[:, 0].astype(int), pts[:, 1].astype(int)
    ok = (x >= 0) & (x < cw_) & (y >= 0) & (y < ch_)
    canvas[y[ok], x[ok]] = colour


def dots(canvas, pts, colours, r):
    ch_, cw_ = canvas.shape[:2]
    for (x, y), c in zip(pts.astype(int), colours):
        canvas[max(0, y - r):min(ch_, y + r + 1), max(0, x - r):min(cw_, x + r + 1)] = c


HALF = SIZE // 2
left = np.repeat(BYTES.reshape(HALF, 2, HALF, 2).min((1, 3))[..., None], 3, 2).copy()
ev = np.unique(np.sort(np.concatenate([L0["TV"][:, [0, 1]], L0["TV"][:, [1, 2]], L0["TV"][:, [2, 0]]]), 1), axis=0)
XY = np.stack([X0, Y0], 1)
draw_segments(left, XY[ev[:, 0]] / 2, XY[ev[:, 1]] / 2, (175, 175, 175))
sv_need = sv0[smooth[L0["pid"][sv0]] > 0]
sv_bad = sv0[unfixable[L0["pid"][sv0]]]
dots(left, XY[sv_need] / 2, [(215, 30, 30)] * len(sv_need), 1)
dots(left, XY[sv_bad] / 2, [(20, 150, 20)] * len(sv_bad), 1)
focus = sv_need if len(sv_need) else sv0[UNDER[L0["pid"][sv0]]]
if len(focus):
    lo, hi = XY[focus].min(0) - 40, XY[focus].max(0) + 40
else:
    lo, hi = np.array([0.0, 0.0]), np.array([SIZE, SIZE], float)
side = float(max(hi - lo))
lo = clamp((lo + hi) / 2 - side / 2, 0, SIZE - side)
sc = SIZE / 2 / side
gy, gx = np.meshgrid(np.arange(HALF), np.arange(HALF), indexing="ij")
sy = clamp((lo[1] + gy / sc).astype(int), 0, SIZE - 1)
sx = clamp((lo[0] + gx / sc).astype(int), 0, SIZE - 1)
right = np.repeat(BYTES[sy, sx][..., None], 3, 2).copy()
draw_segments(right, (XY[ev[:, 0]] - lo) * sc, (XY[ev[:, 1]] - lo) * sc, (150, 150, 150))
if len(sv_need):
    nn = smooth[L0["pid"][sv_need]] / max(MAXS, 1e-9)
    dots(right, (XY[sv_need] - lo) * sc, [(int(120 + 135 * v), 20, 20) for v in nn], 3)
dots(right, (XY[sv_bad] - lo) * sc, [(20, 160, 20)] * len(sv_bad), 3)
right[:, :2] = (60, 60, 200)
write_png(os.path.join(OUT, "head-map-preview.png"), np.ascontiguousarray(np.concatenate([left, right], 1)))
log("DONE", json.dumps({"MaxShrinkDistance_mm": record["MaxShrinkDistance_mm"], "counts": record["counts"],
                        "steps": record["steps"]}))
