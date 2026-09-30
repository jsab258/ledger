"""A MakeHuman garment (CC0) carried onto a MetaHuman body through MakeHuman's own base body.

    blender -b -P tools/meshgen/blender/fit_mhclo.py -- BASE.obj GARMENT_DIR BODY_FullBody.fbx OUT_DIR [--name tom_suit]

WHY, 30 September (Jafar's list, item 2: free ready-made tailored clothes from MakeHuman's CC0 libraries; the
research: production/research/clothing-pipeline/FREE-BASES-AND-COLLARS-2026-09-30.md, section c). A MakeHuman
garment (.mhclo) is fitted to MakeHuman's base body, hm08 (base.obj, CC0 since September 2020): each of its points
is three of the body's points, weighted, plus an offset scaled by distances on the body. So the garment follows
any shape the base body takes. The first fitter moved the garment itself and left its sleeves beside the arms;
here the base body is moved instead:
  1. base.obj read (decimetres, y up, facing +z), its joint markers (the joint-* helper groups) taken as a skeleton;
  2. the base body posed on that skeleton, bone by bone, onto the MetaHuman's joints (each limb turned and
     stretched to his; the torso stretched to his), by automatic weights;
  3. drawn onto his surface by a smoothed displacement, round after round (the two bodies' shapes differ);
  4. the garment rebuilt on the moved base body by its own .mhclo, then kept 4 mm out of him.
OUT_DIR gets NAME.blend ("GarmentRender" beside his body), NAME_render_static.fbx, fit.json and pictures.
"""
import glob
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
BASE, GDIR, BODY, OUT = argv[0], argv[1], argv[2], argv[3]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "garment", str)
log = {"garment": GDIR, "body": BODY}


def say(*a):
    print("MHCLO", *a, flush=True)


def to_bl(p):
    """MakeHuman (x, y up, z front; decimetres) to Blender here (x, y back, z up; metres, facing -y)."""
    p = np.asarray(p, dtype=float)
    return np.stack([p[..., 0] * 0.1, -p[..., 2] * 0.1, p[..., 1] * 0.1], axis=-1)


def from_bl(p):
    p = np.asarray(p, dtype=float)
    return np.stack([p[..., 0] * 10.0, p[..., 2] * 10.0, -p[..., 1] * 10.0], axis=-1)


# ---- 1. the base body and its joints ------------------------------------------------------------------------------
verts, groups, cur, faces_body, faces_help = [], {}, None, [], []
for line in open(BASE, encoding="utf-8", errors="ignore"):
    if line.startswith("v "):
        verts.append([float(x) for x in line.split()[1:4]])
    elif line.startswith("g "):
        cur = line.split()[1].strip()
        groups.setdefault(cur, set())
    elif line.startswith("f ") and cur is not None:
        idx = [int(t.split("/")[0]) - 1 for t in line.split()[1:]]
        groups[cur].update(idx)
        if cur == "body":
            faces_body.append(idx)
        elif cur.startswith("helper-"):
            faces_help.append(idx)
V_mh = np.array(verts)
joint = {g[6:]: V_mh[sorted(v)].mean(axis=0) for g, v in groups.items() if g.startswith("joint-")}
body_ids = sorted(groups["body"])
# (garments are fitted to the helper shells round the body as well, the tights and the skirt: they move with it)
help_ids = sorted(set().union(*[v for g_, v in groups.items() if g_.startswith("helper-")]) - set(body_ids))
all_ids = body_ids + help_ids
say("base", len(V_mh), "points,", len(faces_body), "body faces,", len(joint), "joints")
JB = {k: to_bl(v) for k, v in joint.items()}

arm, body = tailor.load_body(BODY, lod=1)
BVH = tailor.bvh_of(body)
REAL_BVH = BVH
# THE JACKET FORM (30 September, the suit jacket's second blind review: "the body shows through the jacket ... like a
# wetsuit ... every reference jacket hangs straight down from a padded chest"; production/research/clothing-pipeline/
# TAILORED-FIT-2026-09-30.md: fit to a smooth form, as Roblox's cages, Marvelous's fitting suits and Daz's projection
# templates do, never to the skin, whose change then *is* the muscle). A copy of his body made into a tailor's form:
#   the torso, from --form-below-hips under the hip joints up to --form-top-below-shoulder under the shoulder joints:
#     each 1 cm slice (his arms left out) replaced by its convex outline round an upright axis, never coming back in
#     going down (a jacket falls plumb from the fullest point of the chest and the shoulder blades), the outline
#     smoothed over height and angle (filled, never drawn in);
#   a shoulder pad (--pad metres at the shoulder point, thinning to nothing at the neck and the upper arm);
#   everything else (the arms, the neck's base) smoothed outward only, --form-rounds rounds, so muscles and folds
#     fill; the head, hands and feet as they are.
# The garment is drawn onto this form; only at the end is it pushed out of his real body, where needed.
if "--no-form" not in argv:
    import bmesh as _bm
    fbm = _bm.new()
    fbm.from_mesh(body.data)
    fbm.transform(body.matrix_world)
    fbm.verts.ensure_lookup_table()
    Vf = np.array([tuple(v.co) for v in fbm.verts])
    V0f = Vf.copy()
    gib = {vg.index: vg.name for vg in body.vertex_groups}
    ARMS_ = ("upperarm", "lowerarm", "hand", "thumb", "index", "middle", "ring", "pinky")
    armw = np.array([sum(ge.weight for ge in v.groups if gib.get(ge.group, "").startswith(ARMS_)) for v in body.data.vertices])
    Jw = lambda n: np.array(tuple(arm.matrix_world @ arm.pose.bones[n].head))  # noqa: E731
    hipz = (Jw("thigh_l")[2] + Jw("thigh_r")[2]) / 2
    shz = min(Jw("upperarm_l")[2], Jw("upperarm_r")[2])
    z_top = shz - opt("--form-top-below-shoulder", 0.07)
    z_bot = hipz - opt("--form-below-hips", 0.06)
    trunk_pts = Vf[(armw < 0.3) & (Vf[:, 2] > hipz) & (Vf[:, 2] < z_top)]
    AXf = trunk_pts[:, :2].mean(axis=0)
    NBf, DZf = 144, 0.01
    Kf = int(math.ceil((z_top - z_bot) / DZf)) + 1
    dirs_f = np.stack([np.cos(np.arange(NBf) * 2 * math.pi / NBf), np.sin(np.arange(NBf) * 2 * math.pi / NBf)], axis=1)
    HULL = np.zeros((Kf, NBf))
    for k_ in range(Kf):
        z_ = z_top - k_ * DZf
        sl = Vf[(armw < 0.3) & (np.abs(Vf[:, 2] - z_) < 0.012)][:, :2] - AXf
        HULL[k_] = (sl @ dirs_f.T).max(axis=0) if len(sl) >= 6 else (HULL[k_ - 1] if k_ else 0)
    Rf = np.maximum.accumulate(HULL, axis=0)

    def gsm(a_, sz, sa):
        r1 = int(math.ceil(3 * sa))
        k1 = np.exp(-(np.arange(-r1, r1 + 1) / sa) ** 2 / 2)
        k1 /= k1.sum()
        a_ = np.apply_along_axis(lambda x: np.convolve(np.pad(x, r1, mode="wrap"), k1, mode="valid"), 1, a_)
        r0 = int(math.ceil(3 * sz))
        k0 = np.exp(-(np.arange(-r0, r0 + 1) / sz) ** 2 / 2)
        k0 /= k0.sum()
        return np.apply_along_axis(lambda x: np.convolve(np.pad(x, r0, mode="edge"), k0, mode="valid"), 0, a_)

    for _ in range(20):
        Rf = np.maximum(Rf, gsm(Rf, 2.0, 2.0))
    # each torso point moved out to the form's outline at its height and angle (never in); eased in over 6 cm above
    # the top and near the arms
    angf = np.mod(np.arctan2(Vf[:, 1] - AXf[1], Vf[:, 0] - AXf[0]), 2 * math.pi)
    radf = np.linalg.norm(Vf[:, :2] - AXf, axis=1)
    fk = (z_top - Vf[:, 2]) / DZf
    fbn = angf / (2 * math.pi) * NBf

    def r_at(i):
        k0 = int(math.floor(fk[i]))
        b0 = int(math.floor(fbn[i]))
        tk, tb = fk[i] - k0, fbn[i] - b0
        k0c, k1c = min(max(k0, 0), Kf - 1), min(max(k0 + 1, 0), Kf - 1)
        b0c, b1c = b0 % NBf, (b0 + 1) % NBf
        return ((1 - tk) * ((1 - tb) * Rf[k0c, b0c] + tb * Rf[k0c, b1c]) + tk * ((1 - tb) * Rf[k1c, b0c] + tb * Rf[k1c, b1c]))

    moved_f = 0
    for i in range(len(Vf)):
        z_ = Vf[i, 2]
        if z_ < z_bot or z_ > z_top + 0.06 or armw[i] > 0.6:
            continue
        w_top = 1.0 if z_ <= z_top else 1.0 - (z_ - z_top) / 0.06
        w_arm = 1.0 - min(1.0, armw[i] / 0.6)
        w_bot = min(1.0, (z_ - z_bot) / 0.04)
        w_ = max(0.0, w_top * w_arm * w_bot)
        w_ = w_ * w_ * (3 - 2 * w_)
        rt = r_at(i)
        if rt > radf[i] and w_ > 0:
            d_ = (rt - radf[i]) * w_
            Vf[i, 0] += d_ * math.cos(angf[i])
            Vf[i, 1] += d_ * math.sin(angf[i])
            moved_f += 1
    # the shoulder pad
    for i in range(len(Vf)):
        for s_ in ("l", "r"):
            spt = Jw("upperarm_" + s_) + np.array([0.0, 0.0, 0.03])
            d_ = np.linalg.norm(Vf[i] - spt)
            if d_ < 0.11 and Vf[i, 2] > shz - 0.04:
                t_ = 1.0 - d_ / 0.11
                out_ = np.array([Vf[i, 0] - AXf[0], Vf[i, 1] - AXf[1], 0.0])
                out_ = out_ / max(1e-9, np.linalg.norm(out_))
                dirp = out_ * 0.5 + np.array([0.0, 0.0, 0.85])
                dirp /= np.linalg.norm(dirp)
                Vf[i] += dirp * opt("--pad", 0.015) * (t_ * t_ * (3 - 2 * t_))
    # everything smoothed outward only (muscles and folds fill); the head, hands and feet kept
    edf = np.array([(e.verts[0].index, e.verts[1].index) for e in fbm.edges])
    dgf = np.bincount(edf.ravel(), minlength=len(Vf)).astype(float)
    keepf = np.zeros(len(Vf), bool)
    for jn, rr in (("head", 0.14), ("neck_02", 0.05), ("hand_l", 0.11), ("hand_r", 0.11), ("foot_l", 0.14), ("foot_r", 0.14)):
        keepf |= np.linalg.norm(V0f - Jw(jn), axis=1) < rr
    for rnd_ in range(opt("--form-rounds", 60, int)):
        if rnd_ % 10 == 0:
            for i_, v in enumerate(fbm.verts):
                v.co = Vector(tuple(Vf[i_]))
            fbm.normal_update()
            Nf = np.array([tuple(v.normal) for v in fbm.verts])
        acc_ = np.zeros_like(Vf)
        np.add.at(acc_, edf[:, 0], Vf[edf[:, 1]])
        np.add.at(acc_, edf[:, 1], Vf[edf[:, 0]])
        d_ = acc_ / np.maximum(dgf, 1)[:, None] - Vf
        mv = ~keepf & ((d_ * Nf).sum(axis=1) > 0)
        Vf[mv] += 0.5 * d_[mv]
    for i_, v in enumerate(fbm.verts):
        v.co = Vector(tuple(Vf[i_]))
    fbm.normal_update()
    from mathutils.bvhtree import BVHTree as _BVH
    BVH = _BVH.FromBMesh(fbm)
    fill_f = np.linalg.norm(Vf - V0f, axis=1)
    log["form"] = {"top": round(float(z_top), 3), "bottom": round(float(z_bot), 3), "torsoPointsOut": moved_f,
                   "meanMm": round(float(fill_f.mean()) * 1000, 1), "mostMm": round(float(fill_f.max()) * 1000, 1),
                   "padM": opt("--pad", 0.015)}
    say("jacket form", json.dumps(log["form"]))
    if "--save-form" in argv:
        fme = bpy.data.meshes.new("JacketForm")
        fbm.to_mesh(fme)
        fob = bpy.data.objects.new("JacketForm", fme)
        bpy.context.collection.objects.link(fob)
J = lambda n: np.array(tuple(arm.matrix_world @ arm.pose.bones[n].head))
# which of the base body's sides is the MetaHuman's left (+x)
flip = JB["l-shoulder"][0] < 0
side_of = {"l": "r" if flip else "l", "r": "l" if flip else "r"}
log["baseLeftIsMinusX"] = bool(flip)

# the base body as a Blender mesh (body faces only), in Blender's frame
PB = to_bl(V_mh)
remap = {old: i for i, old in enumerate(all_ids)}
me = bpy.data.meshes.new("Base")
me.from_pydata([tuple(PB[i]) for i in all_ids], [], [[remap[i] for i in f] for f in faces_body + faces_help if all(i in remap for i in f)])
me.validate()
base = bpy.data.objects.new("Base", me)
bpy.context.collection.objects.link(base)

# ---- 2. a skeleton from its joints, posed onto his --------------------------------------------------------------
CHAIN = [  # (bone, head joint, tail joint, parent, MetaHuman head, MetaHuman tail)
    ("spine", "pelvis", "neck", None, "pelvis", "neck_01"),
    ("head", "neck", "head", "spine", "neck_01", "head"),
]
for s in ("l", "r"):
    m = side_of[s]
    CHAIN += [
        ("upperarm_" + s, s + "-shoulder", s + "-elbow", "spine", "upperarm_" + m, "lowerarm_" + m),
        ("lowerarm_" + s, s + "-elbow", s + "-hand", "upperarm_" + s, "lowerarm_" + m, "hand_" + m),
        ("thigh_" + s, s + "-upper-leg", s + "-knee", "spine", "thigh_" + m, "calf_" + m),
        ("calf_" + s, s + "-knee", s + "-ankle", "thigh_" + s, "calf_" + m, "foot_" + m),
    ]
ad = bpy.data.armatures.new("BaseRig")
rig = bpy.data.objects.new("BaseRig", ad)
bpy.context.collection.objects.link(rig)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="EDIT")
for bn, h, t, par, _mh, _mt in CHAIN:
    eb = ad.edit_bones.new(bn)
    eb.head, eb.tail = Vector(tuple(JB[h])), Vector(tuple(JB[t]))
    if par:
        eb.parent = ad.edit_bones[par]
        eb.use_connect = False
bpy.ops.object.mode_set(mode="OBJECT")
bpy.ops.object.select_all(action="DESELECT")
base.select_set(True)
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.parent_set(type="ARMATURE_AUTO")
say("bound", len(base.vertex_groups), "groups")
# EACH BONE PLACED DIRECTLY (30 September, the suit on Darren: its sleeves ended 70 to 75 per cent of the way from
# elbow to wrist; stretching bones in the pose made each child inherit its parent's stretch at an angle, skewing the
# forearm): for every bone a map of its own, from the base body's joint pair to his (moved to his head joint, turned
# to his direction, stretched along it to his length), and each point of the base body moved by the maps of its
# bones, weighted as the automatic weights say
bpy.context.view_layer.update()
maps = {}
for bn, h, t, par, mh, mt in CHAIN:
    h0, t0 = Vector(tuple(JB[h])), Vector(tuple(JB[t]))
    h1, t1 = Vector(tuple(J(mh))), Vector(tuple(J(mt)))
    d0, d1 = (t0 - h0), (t1 - h1)
    R = d0.normalized().rotation_difference(d1.normalized()).to_matrix().to_4x4()
    u = d0.normalized()
    k = d1.length / max(1e-9, d0.length)
    S = Matrix.Identity(4)
    for i_ in range(3):
        for j_ in range(3):
            S[i_][j_] = (1.0 if i_ == j_ else 0.0) + (k - 1.0) * u[i_] * u[j_]
    maps[bn] = Matrix.Translation(h1) @ R @ S @ Matrix.Translation(-h0)
gi = {vg.index: vg.name for vg in base.vertex_groups}
# the helper shells round the body (the tights, the skirt; clothes are often fitted to them: the suit's cuffs are) get
# no weights of their own from the automatic binding, being separate pieces, so each takes the weights of the body
# point nearest it (30 September: unweighted, they moved with the spine and the suit's cuffs landed 13 cm up the arm)
from mathutils.kdtree import KDTree as _KD  # noqa: E402
NB_REST = len(body_ids)
_kd = _KD(NB_REST)
for i_ in range(NB_REST):
    _kd.insert(me.vertices[i_].co, i_)
_kd.balance()


def weights_of(v):
    src = v if v.index < NB_REST else me.vertices[_kd.find(v.co)[1]]
    return [(gi.get(ge.group), ge.weight) for ge in src.groups]


P = np.zeros((len(me.vertices), 3))
for v in me.vertices:
    co = v.co
    acc, wsum = Vector(), 0.0
    for bn, w_ in weights_of(v):
        if bn in maps and w_ > 0:
            acc += (maps[bn] @ co) * w_
            wsum += w_
    P[v.index] = tuple(acc / wsum) if wsum > 0 else tuple(maps["spine"] @ co)
for m_ in list(base.modifiers):
    base.modifiers.remove(m_)
say("posed onto his joints")

# ---- 3. drawn onto his surface ------------------------------------------------------------------------------------
NB_ = len(body_ids)
edges_all = np.array([e.vertices[:] for e in me.edges])
edges = edges_all[(edges_all[:, 0] < NB_) & (edges_all[:, 1] < NB_)]
deg = np.bincount(edges.ravel(), minlength=len(P)).astype(float)
from mathutils.kdtree import KDTree
kdb = KDTree(NB_)
for i in range(NB_):
    kdb.insert(Vector(tuple(P[i])), i)
kdb.balance()
near_body = np.array([kdb.find(Vector(tuple(P[i])))[1] for i in range(NB_, len(P))], dtype=int)
for rnd in range(opt("--rounds", 8, int)):
    disp = np.zeros_like(P)
    for i in range(NB_):
        p = P[i]
        hit, nn, _f, dist = BVH.find_nearest(Vector(tuple(p)))
        if hit is not None and dist < 0.15:
            disp[i] = np.array(tuple(hit)) - p
    for _ in range(opt("--smooth", 20, int)):
        acc = np.zeros_like(disp)
        np.add.at(acc, edges[:, 0], disp[edges[:, 1]])
        np.add.at(acc, edges[:, 1], disp[edges[:, 0]])
        disp = 0.5 * disp + 0.5 * acc / np.maximum(deg, 1)[:, None]
    if len(near_body):
        disp[NB_:] = disp[near_body]                   # each helper point moves as the body point nearest it
    P = P + disp * 0.8
    say("round", rnd, "moved most mm", round(float(np.linalg.norm(disp, axis=1).max()) * 1000, 1))
# the whole base body, moved (helpers ignored: only body points are ever referenced by clothes on the body)
V_fit = V_mh.copy()
V_fit[all_ids] = from_bl(P)

# ---- 4. the garment rebuilt ---------------------------------------------------------------------------------------
mhclo = glob.glob(os.path.join(GDIR, "*.mhclo"))[0]
refs, scales, obj_file, reading = [], {}, None, False
for line in open(mhclo, encoding="utf-8", errors="ignore"):
    w = line.split()
    if not w or w[0].startswith("#"):
        continue
    if w[0] == "obj_file":
        obj_file = os.path.join(GDIR, w[1])
    elif w[0] in ("x_scale", "y_scale", "z_scale"):
        scales[w[0][0]] = (int(w[1]), int(w[2]), float(w[3]))
    elif w[0] == "verts":
        reading = True
    elif reading and not w[0].lstrip("-").replace(".", "").isdigit():
        reading = False
    elif reading and len(w) == 9:
        refs.append(([int(x) for x in w[:3]], [float(x) for x in w[3:6]], [float(x) for x in w[6:9]]))
    elif reading and len(w) == 1:
        refs.append(([int(w[0])] * 3, [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]))
    elif reading and w[0] in ("delete_verts", "weights", "material", "z_depth", "max_pole"):
        reading = False
ax = {"x": 0, "y": 1, "z": 2}
S = {}
for k, (a_, b_, f_) in scales.items():
    S[k] = abs(V_fit[a_][ax[k]] - V_fit[b_][ax[k]]) / f_ if f_ else 1.0
G = np.array([sum(w * V_fit[i] for i, w in zip(ix, ws)) + np.array([d[0] * S.get("x", 1), d[1] * S.get("y", 1), d[2] * S.get("z", 1)])
              for ix, ws, d in refs])
# CARRIED BY THE BASE BODY'S OWN CHANGE (30 September, the suit jacket's first review: lapels crumpled with ragged
# edges, the shirt showing through beside them, the sleeves' layers crossing): a .mhclo's offsets lie along fixed
# directions, so wherever the fitted body faces another way than hm08 (the chest's slope under the lapels, the arms
# turned), the garment's stacked layers cross. Instead each garment point, as it sits on the untouched base body,
# moves by the base body's change round it: the moves of the body points near it, weighted by a Gaussian of their
# distance (--field-sigma, decimetres), so neighbouring layers move together (the donkey jacket's carry to Darren,
# carry_garment.py). --mhclo-offsets returns to the .mhclo's own way.
if "--mhclo-offsets" not in argv:
    from mathutils.kdtree import KDTree as _KDf
    G0 = np.array([sum(w * V_mh[i] for i, w in zip(ix, ws)) + np.array(d) for ix, ws, d in refs])
    ids_f = np.array(body_ids)
    kdf = _KDf(len(ids_f))
    for j_, i_ in enumerate(ids_f):
        kdf.insert(Vector(tuple(V_mh[i_])), j_)
    kdf.balance()
    dV = V_fit[ids_f] - V_mh[ids_f]
    SIGF = opt("--field-sigma", 0.25)
    G = np.empty_like(G0)
    for k_, g0 in enumerate(G0):
        near = kdf.find_range(Vector(tuple(g0)), 3.0 * SIGF)
        if len(near) < 6:
            near = kdf.find_n(Vector(tuple(g0)), 24)
        jj = np.array([n_[1] for n_ in near])
        dd = np.array([n_[2] for n_ in near])
        ww = np.exp(-(dd / SIGF) ** 2 / 2.0) + 1e-12
        G[k_] = g0 + (ww[:, None] * dV[jj]).sum(0) / ww.sum()
    log["carry"] = {"field": True, "sigmaDm": SIGF}
before = set(bpy.data.objects)
bpy.ops.wm.obj_import(filepath=obj_file, forward_axis="NEGATIVE_Z", up_axis="Y")
g = next(o for o in bpy.data.objects if o not in before and o.type == "MESH")
g.name = "GarmentRender"
g.matrix_world = Matrix.Identity(4)
if len(g.data.vertices) != len(G):
    raise SystemExit("the garment's points (%d) and its .mhclo lines (%d) differ" % (len(g.data.vertices), len(G)))
GB = to_bl(G)
for i, v in enumerate(g.data.vertices):
    v.co = Vector(tuple(GB[i]))
g.data.update()
# kept out of him by smoothed pushes (moved point by point, the faces between still cut through at the calves)
ge = np.array([e.vertices[:] for e in g.data.edges])
gdeg = np.bincount(ge.ravel(), minlength=len(g.data.vertices)).astype(float)
MINE = opt("--min-ease", 0.004)
pushed = 0
from mathutils.kdtree import KDTree as _KDp
PUSH_R = opt("--push-r", 0.02)
for rnd in range(opt("--push-rounds", 3, int)):
    Q = np.array([tuple(v.co) for v in g.data.vertices])
    need = np.zeros_like(Q)
    for i, q in enumerate(Q):
        hit, nn, _f, _d = REAL_BVH.find_nearest(Vector(tuple(q)))
        if hit is not None:
            off = (Vector(tuple(q)) - hit).dot(nn)
            if off < MINE:
                need[i] = np.array(tuple(nn)) * (MINE - off)
    # each point moves by the largest push of the points round it (within --push-r), weighted by nearness, so the
    # layers stacked there (a lapel, its facing, a pocket) move as one (the research: "push only the innermost layer
    # out of the body and give every layer above it the same shift")
    idx_need = np.where(np.linalg.norm(need, axis=1) > 0)[0]
    pushed = len(idx_need)
    if not pushed:
        break
    kdp = _KDp(len(idx_need))
    for j_, i in enumerate(idx_need):
        kdp.insert(Vector(tuple(Q[i])), j_)
    kdp.balance()
    disp = np.zeros_like(Q)
    for i, q in enumerate(Q):
        best = None
        for _c, j_, d_ in kdp.find_range(Vector(tuple(q)), PUSH_R):
            w_ = 1.0 - d_ / PUSH_R
            cand = need[idx_need[j_]] * w_
            if best is None or np.linalg.norm(cand) > np.linalg.norm(best):
                best = cand
        if best is not None:
            disp[i] = best
    Q = Q + disp
    for i, v in enumerate(g.data.vertices):
        v.co = Vector(tuple(Q[i]))
log["garmentPoints"] = len(G)
log["pushedOut"] = pushed

# ---- 5. colour, pictures, files -----------------------------------------------------------------------------------
bpy.data.objects.remove(base, do_unlink=True)
bpy.data.objects.remove(rig, do_unlink=True)
RGB = opt("--rgb", "", str)
if RGB:
    g.data.materials.clear()
    g.data.materials.append(tailor.material("M_Suit", tuple(float(c) for c in RGB.split(",")), 0.8))
for p_ in g.data.polygons:
    p_.use_smooth = True
body.data.materials.clear()
body.data.materials.append(tailor.material("M_Body", (0.55, 0.55, 0.56)))
log["render"] = {"verts": len(g.data.vertices), "tris": sum(len(p_.vertices) - 2 for p_ in g.data.polygons)}
tailor.pictures(os.path.join(OUT, "fit"), Vector((0, 0, 1.0)), views=(("front", (0, -3.4, 0.1)), ("side", (3.4, 0, 0.1)),
                                                                       ("back", (0, 3.4, 0.1)), ("three-quarter", (2.3, -2.4, 0.4))))
tailor.pictures(os.path.join(OUT, "fit-close"), Vector((0, 0, 1.3)), views=(("front", (0, -1.3, 0.1)), ("three-quarter", (0.9, -0.9, 0.2)),
                                                                             ("back", (0, 1.3, 0.1))), res=(700, 700))
bpy.ops.object.select_all(action="DESELECT")
g.select_set(True)
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_render_static.fbx"), use_selection=True,
                         object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "fit.json"), "w"), indent=1)
say("done", json.dumps(log))
