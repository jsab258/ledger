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
# the whole: moved so the pelvises meet, scaled to his height from pelvis to neck first
for bn, h, t, par, mh, mt in CHAIN:
    pb = rig.pose.bones[bn]
    bpy.context.view_layer.update()
    head_w = rig.matrix_world @ pb.head
    tail_w = rig.matrix_world @ pb.tail
    d_now = (tail_w - head_w)
    d_to = Vector(tuple(J(mt) - J(mh)))
    q = d_now.normalized().rotation_difference(d_to.normalized())
    # in the bone's own space: turn it so its direction is his, and stretch it to his length
    M = pb.matrix.copy()
    R = q.to_matrix().to_4x4()
    pb.matrix = Matrix.Translation(head_w) @ R @ Matrix.Translation(-head_w) @ M
    bpy.context.view_layer.update()
    pb.scale = (1.0, d_to.length / max(1e-6, d_now.length), 1.0)
    bpy.context.view_layer.update()
bpy.context.view_layer.update()
rig.location = Vector(tuple(J("pelvis"))) - (rig.matrix_world @ rig.pose.bones["spine"].head) + rig.location
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
ev = base.evaluated_get(dg).to_mesh()
P = np.array([tuple(base.matrix_world @ v.co) for v in ev.vertices])
base.evaluated_get(dg).to_mesh_clear()
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
MINE = opt("--min-ease", 0.006)
pushed = 0
for rnd in range(opt("--push-rounds", 4, int)):
    Q = np.array([tuple(v.co) for v in g.data.vertices])
    disp = np.zeros_like(Q)
    for i, q in enumerate(Q):
        hit, nn, _f, _d = BVH.find_nearest(Vector(tuple(q)))
        if hit is not None:
            off = (Vector(tuple(q)) - hit).dot(nn)
            if off < MINE:
                disp[i] = np.array(tuple(nn)) * (MINE - off)
    for _ in range(6):
        acc = np.zeros_like(disp)
        np.add.at(acc, ge[:, 0], disp[ge[:, 1]])
        np.add.at(acc, ge[:, 1], disp[ge[:, 0]])
        disp = np.maximum(disp, 0) * 0 + np.where(np.linalg.norm(disp, axis=1)[:, None] > 0, disp, 0.5 * acc / np.maximum(gdeg, 1)[:, None])
    Q = Q + disp
    pushed = int((np.linalg.norm(disp, axis=1) > 1e-5).sum())
    for i, v in enumerate(g.data.vertices):
        v.co = Vector(tuple(Q[i]))
for v in g.data.vertices:
    hit, nn, _f, _d = BVH.find_nearest(v.co)
    if hit is not None and (v.co - hit).dot(nn) < 0.003:
        v.co = hit + nn * 0.003
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
