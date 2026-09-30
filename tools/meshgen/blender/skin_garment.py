"""A game-mesh garment skinned to a MetaHuman's skeleton, its joints corrected, ready for the builder.

    blender -b -P tools/meshgen/blender/skin_garment.py -- BODY.fbx GAME.blend OUT_DIR NAME [options]

WHY, 30 September (Jafar, after an outside audit: "one properly skinned jacket: shape, retopology, skinning, joint
weights corrected, only loose parts simulated"). GAME.blend is retopo_garment.py's (or carry_garment.py's) game
mesh, object NAME, on the body BODY.fbx (F:/LedgerTools/bodies/<body>/<body>_Body.fbx, its skeleton and weights).

1. THE WEIGHTS COPIED FROM THE BODY by the builder's binder (tools/meshgen/blender/bind_garment.py, the binding the
   sewn jacket walked and raised its arms cleanly with in Unreal on 30 September): each piece of the pattern from
   its own part of the body (the sleeves from the arm, the fronts and back from the trunk, never the arm, so no
   wings), only where the body is near and faces the same way, the rest filled in from the reliable neighbours
   (Epic's inpainting idea); Epic's shoulder correctives kept in the trunk (--keep-correctives, which the builder
   found keeps his skin from showing at the yoke sitting).
2. THE JOINTS CORRECTED:
   the skirt (below the hip joints, --skirt-from metres above them): a share of the thighs' weight given to the
   pelvis, rising to --skirt-pelvis at the hem, so the skirt follows the hips and not each leg (skinned to the legs
   it read as shorts sitting; it is cloth in Unreal, painted by its SimMaxDistance colour);
   the collar and the neck: no head or face bones (the collar followed the jaw);
   the buttons: each moves as one piece (the average of its points);
   the collar smoothed over itself (--collar-smooth rounds), so its fold never parts.
3. At most --max-influences bones a point (8: Unreal's TransferSkinWeights default), normalised.
OUT_DIR gets NAME_skinned.fbx (armature and mesh on the body's own skeleton; the "UVMap" and "pattern" layers, the
SimMaxDistance colour and the materials kept), NAME_skinned.blend (with the body, for the pose test:
pose_skinned.py --own-weights) and skin.json.
"""
import json
import os
import subprocess
import sys

import bmesh
import bpy
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
BODY, GAME, OUT, NAME = argv[:4]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


HERE = os.path.dirname(os.path.abspath(__file__))
log = {"body": BODY, "game": GAME, "name": NAME}


def say(*a):
    print("SKIN", *a, flush=True)


# ---- 1. the binder, on the game mesh as a static FBX ---------------------------------------------------------
bpy.ops.wm.open_mainfile(filepath=GAME)
g = bpy.data.objects[NAME]
static = os.path.join(OUT, NAME + "_for_binder.fbx")
bpy.ops.object.select_all(action="DESELECT")
g.select_set(True)
bpy.context.view_layer.objects.active = g
bpy.ops.export_scene.fbx(filepath=static, use_selection=True, object_types={"MESH"}, mesh_smooth_type="OFF",
                         add_leaf_bones=False)
bind_dir = os.path.join(OUT, "bind")
cmd = [bpy.app.binary_path, "-b", "-P", os.path.join(HERE, "bind_garment.py"), "--", BODY, static, bind_dir, NAME]
if "--no-keep-correctives" not in argv:
    cmd.append("--keep-correctives")
for k in ("--reach", "--angle"):
    if k in argv:
        cmd += [k, argv[argv.index(k) + 1]]
r = subprocess.run(cmd, capture_output=True, text=True)
line = [x for x in r.stdout.splitlines() if x.startswith("BIND")]
say("binder:", line[-1][:300] if line else r.stdout[-800:] + r.stderr[-800:])
if r.returncode or not line:
    raise SystemExit("SKIN the binder failed")
log["binder"] = json.load(open(os.path.join(bind_dir, "bind.json")))

# ---- the binder's weights read back, point for point ---------------------------------------------------------
with bpy.data.libraries.load(os.path.join(bind_dir, NAME + "_skinned.blend")) as (src, dst):
    dst.objects = [NAME]
bound = dst.objects[0]
me, bme = g.data, bound.data
if len(me.vertices) != len(bme.vertices):
    raise SystemExit("SKIN the binder's mesh has %d points, the game mesh %d" % (len(bme.vertices), len(me.vertices)))
P = np.array([tuple(g.matrix_world @ v.co) for v in me.vertices])
Q = np.array([tuple(bound.matrix_world @ v.co) for v in bme.vertices])
if np.isnan(P).any():
    raise SystemExit("SKIN the game mesh has points with no position")
off = float(np.abs(P - Q).max())
log["bindPointMismatchM"] = round(off, 6)
if off > 1e-3:
    raise SystemExit("SKIN the binder's points are not the game mesh's (%.4f m apart)" % off)
names = [vg.name for vg in bound.vertex_groups]
W = np.zeros((len(me.vertices), len(names)))
for v in bme.vertices:
    for ge in v.groups:
        W[v.index, ge.group] = ge.weight
bpy.data.objects.remove(bound, do_unlink=True)
col = {n: i for i, n in enumerate(names)}


def ensure(bone):
    if bone not in col:
        col[bone] = len(names)
        names.append(bone)
        global W
        W = np.hstack([W, np.zeros((W.shape[0], 1))])
    return col[bone]


# ---- the body's skeleton (everything else in the file cleared first, so the skeleton keeps its own name) -------
for o in list(bpy.data.objects):
    if o is not g:
        bpy.data.objects.remove(o, do_unlink=True)
for a in list(bpy.data.armatures):
    if a.users == 0:
        bpy.data.armatures.remove(a)
before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=BODY)
new = [o for o in bpy.data.objects if o not in before]
arm = next(o for o in new if o.type == "ARMATURE")
bodies = sorted([o for o in new if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
body = bodies[0]
for o in bodies[1:]:
    bpy.data.objects.remove(o, do_unlink=True)
say("skeleton", arm.name, "body", body.name)
J = lambda n: arm.matrix_world @ arm.pose.bones[n].head  # noqa: E731

# ---- 2. the joints corrected -----------------------------------------------------------------------------------
bm = bmesh.new()
bm.from_mesh(me)
bm.verts.ensure_lookup_table()
bm.faces.ensure_lookup_table()
panel = me.attributes.get("panel")
pan = np.array([d.value for d in panel.data]) if panel else np.zeros(len(me.polygons), int)
mat_names = [m.name if m else "" for m in me.materials]
# pieces: connected parts of the mesh
comp = np.full(len(bm.verts), -1)
for v0 in bm.verts:
    if comp[v0.index] >= 0:
        continue
    comp[v0.index] = v0.index
    st = [v0]
    while st:
        v = st.pop()
        for e in v.link_edges:
            w = e.other_vert(v)
            if comp[w.index] < 0:
                comp[w.index] = v0.index
                st.append(w)
main = np.bincount(comp[comp >= 0]).argmax()
is_button = np.zeros(len(bm.verts), bool)
piece_attr = me.attributes.get("piece")                 # mh_garment.py's: 0 cloth, 1 shirt, 2 tie, 3 button
for f in bm.faces:
    if "Button" in mat_names[f.material_index] or (piece_attr is not None and piece_attr.data[f.index].value == 3):
        for v in f.verts:
            is_button[v.index] = True
# the pieces on the trunk (a collar, a shirt front, a tie, the front's buttons): inside the shoulders; the ones on
# the arms (a shirt's cuffs, a sleeve's buttons) keep the arm
is_collar = (comp != main) & ~is_button
# the skirt, below the hip joints: its front takes the mean of the two thighs (walking, the legs swing opposite
# ways and the front stays with the hips, never parting into shorts; sitting, both come forward and it lies over
# the lap), its back mostly the pelvis (--skirt-pelvis at the hem), the change from front to back over the side
hip_l, hip_r = J("thigh_l"), J("thigh_r")
hip_z = (hip_l.z + hip_r.z) / 2 + opt("--skirt-from", 0.0)
hip_y = (hip_l.y + hip_r.y) / 2
hem_z = P[comp == main, 2].min()
leg = [n for n in names if n.startswith(("thigh", "calf", "foot", "ball"))]
pelvis = ensure("pelvis")
th_l, th_r = ensure("thigh_l"), ensure("thigh_r")
PEL = opt("--skirt-pelvis", 0.7)
# the front is open below its last button (retopo_garment.py): each half leans to its own thigh (--own-thigh), so
# walking the halves part over the forward leg; a point's side is that of the faces round it (the two copies of a
# point on the opening lie on different sides)
OWN = opt("--own-thigh", 0.65)
CUT_X = opt("--cut-x", -0.019)
fx = np.zeros(len(P))
fn = np.zeros(len(P))
for p_ in me.polygons:
    for vi in p_.vertices:
        fx[vi] += (g.matrix_world @ p_.center).x
        fn[vi] += 1
side_x = fx / np.maximum(fn, 1)
moved = 0
for i in range(len(P)):
    if comp[i] != main or P[i, 2] >= hip_z:
        continue
    t = min(1.0, (hip_z - P[i, 2]) / max(1e-6, (hip_z - hem_z) * 0.45))
    t = t * t * (3 - 2 * t)
    T = sum(W[i, col[b_]] for b_ in leg)
    if T <= 0:
        continue
    front = min(1.0, max(0.0, (hip_y - P[i, 1]) / 0.08 + 0.5))
    front = front * front * (3 - 2 * front)
    left = side_x[i] > CUT_X
    own = 0.5 + (OWN - 0.5) * min(1.0, abs(side_x[i] - CUT_X) / 0.02 + 0.5)
    fl = own if left else 1 - own
    want = np.zeros(W.shape[1])
    want[th_l] += T * (front * fl + (1 - front) * (1 - PEL) * 0.5)
    want[th_r] += T * (front * (1 - fl) + (1 - front) * (1 - PEL) * 0.5)
    want[pelvis] += T * (1 - front) * PEL
    for b_ in leg:
        W[i, col[b_]] *= 1 - t
    W[i] += t * want
    moved += 1
log["skirt"] = {"hipZ": round(float(hip_z), 3), "hemZ": round(float(hem_z), 3), "backToPelvis": PEL, "points": moved}
# the collar and the buttons carry no arm (nor Epic's shoulder correctives, which hang under it): they sit at the
# neck and on the front
def under(bone):
    out = [bone.name]
    for c_ in bone.children:
        out += under(c_)
    return out


arm_bones = set(under(arm.data.bones["upperarm_l"])) | set(under(arm.data.bones["upperarm_r"]))
for s_ in "lr":
    cr = arm.data.bones.get("upperarm_correctiveRoot_" + s_)
    if cr is not None:
        arm_bones |= set(under(cr))
arm_cols = [col[n] for n in names if n in arm_bones]
shoulder_x = min(abs(J("upperarm_l").x), abs(J("upperarm_r").x))
pcentre = {}
for c_ in np.unique(comp[comp != main]):
    pcentre[c_] = P[comp == c_].mean(axis=0)
pieces_ids = np.array([i for i in np.where(comp != main)[0] if abs(pcentre[comp[i]][0]) < shoulder_x], dtype=int)
is_collar = np.zeros(len(P), bool)
is_collar[pieces_ids] = True
is_collar &= ~is_button
spine5 = ensure("spine_05")
for i in pieces_ids:
    lost = W[i, arm_cols].sum()
    W[i, arm_cols] = 0.0
    if W[i].sum() < 1e-6:
        W[i, spine5] = 1.0
log["piecesArmWeightRemoved"] = int((W[pieces_ids][:, arm_cols].sum(axis=1) >= 0).sum()) if arm_cols else 0
# no head or face bones anywhere (the collar followed the jaw)
face = [col[n] for n in names if n == "head" or n.startswith(("FACIAL", "facial", "head_"))]
neck2 = col.get("neck_02", col.get("neck_01"))
if face and neck2 is not None:
    W[:, neck2] += W[:, face].sum(axis=1)
    W[:, face] = 0.0
log["headWeightsMoved"] = len(face)
# the collar smoothed over itself
nbrs = [[e.other_vert(v).index for e in v.link_edges] for v in bm.verts]
cidx = np.where(is_collar)[0]
for _ in range(opt("--collar-smooth", 6, int)):
    S = W.copy()
    for i in cidx:
        if nbrs[i]:
            S[i] = 0.5 * W[i] + 0.5 * W[nbrs[i]].mean(axis=0)
    W = S
# each button one piece
for c in np.unique(comp[is_button]):
    ids = np.where((comp == c) & is_button)[0]
    W[ids] = W[ids].mean(axis=0)
# at most N bones a point, normalised
N = opt("--max-influences", 8, int)
if W.shape[1] > N:
    cut = np.argsort(W, axis=1)[:, :-N]
    np.put_along_axis(W, cut, 0.0, axis=1)
s = W.sum(axis=1, keepdims=True)
s[s == 0] = 1.0
W = W / s
bm.free()

# ---- 3. onto the skeleton, and out ----------------------------------------------------------------------------
for vg in list(g.vertex_groups):
    g.vertex_groups.remove(vg)
used = [j for j in range(len(names)) if W[:, j].max() > 1e-4]
for j in used:
    vg = g.vertex_groups.new(name=names[j])
    for i in np.where(W[:, j] > 1e-4)[0]:
        vg.add([int(i)], float(W[i, j]), "REPLACE")
log["bones"] = [names[j] for j in used]
g.parent = arm
g.matrix_parent_inverse = arm.matrix_world.inverted()
for m in list(g.modifiers):
    g.modifiers.remove(m)
mod = g.modifiers.new("Armature", "ARMATURE")
mod.object = arm
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
g.select_set(True)
bpy.context.view_layer.objects.active = arm
out_fbx = os.path.join(OUT, NAME + "_skinned.fbx")
bpy.ops.export_scene.fbx(filepath=out_fbx, use_selection=True, object_types={"ARMATURE", "MESH"}, add_leaf_bones=False,
                         mesh_smooth_type="OFF", use_tspace=True, colors_type="LINEAR", bake_anim=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_skinned.blend"))
os.remove(static)
json.dump(log, open(os.path.join(OUT, "skin.json"), "w"), indent=1)
say("done", json.dumps({k: v for k, v in log.items() if k not in ("bones", "binder")}), "bones=%d" % len(log["bones"]))
