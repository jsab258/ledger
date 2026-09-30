"""BIND A GARMENT TO A METAHUMAN'S SKELETON, the way games make clothes (Jafar,
30 September: "game clothes are not simulated cloth. A garment is a skeletal
mesh skinned to the MetaHuman skeleton, with skin weights transferred from the
body mesh and fixes at the shoulders, elbows and hips so it bends cleanly";
production/research/game-clothing-pipeline/NOTE-2026-09-30.md).

    blender -b -P tools/meshgen/blender/bind_garment.py -- BODY.fbx GARMENT.fbx OUT_DIR NAME [--tris 40000] [--reach 0.06] [--angle 50]

BODY.fbx is the body the garment was made on (F:/LedgerTools/bodies/<name>/<name>_Body.fbx,
its skeleton and skin weights, in MetaHuman's reference pose); GARMENT.fbx a
static mesh in the same space (a finished garment's _render_static.fbx).

1. The garment reduced to game weight (--tris triangles), its shape kept.
2. Each of its points takes the skin weights of the nearest point on the body,
   interpolated across that point's triangle.
3. THE REPAIR AT THE ARMPITS, HIPS AND SHOULDERS: nearest-point copying tears
   where the nearest body point jumps between torso and arm (Epic's own
   documentation warns of it). So a copy counts only where it is reliable: the
   body within --reach metres and its surface facing within --angle degrees of
   the garment's there; every other point's weights are filled in from its
   reliable neighbours across the garment (the "inpaint" repair), so it bends
   as a blend of the parts round it rather than following one bone.
4. EACH PANEL TO ITS OWN BONES (30 September, after the first binding's
   poses): the sleeves copy their weights only from the body's arm, and the
   jacket's own body only from the body's trunk, with no arm bones at all;
   where the two are sewn together (the armhole seam) a point takes the mean
   of both, and the smoothing spreads that over a few centimetres. The
   panels are the garment's sewing pattern (its "pattern" UV layer: each
   panel one island), and a panel is a sleeve when it sits out beyond the
   shoulder joint. Copying from the nearest body point alone gave the sides
   of the jacket the arm's bones, and with the arms raised its sides rose
   with them in wings down to the hip. Every bone under the upper arm counts
   as the arm: Epic's shoulder correctives hang there and turn with it.
   --no-panels copies from the nearest point as before. --keep-correctives
   leaves the trunk Epic's shoulder correctives (the bones under
   upperarm_correctiveRoot, which Unreal drives to keep the shoulder's
   shape, where Blender only turns them with the arm), taking away only the
   arm itself.
5. A light smoothing everywhere, at most eight bones a point, normalised.
6. Written as NAME_skinned.fbx on the body's own skeleton (the export the
   boots used: armature and mesh, no leaf bones), with bind.json.
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.interpolate import poly_3d_calc

argv = sys.argv[sys.argv.index("--") + 1:]
BODY, GARMENT, OUT, NAME = argv[:4]


def opt(name, default):
    return float(argv[argv.index(name) + 1]) if name in argv else default


TRIS = int(opt("--tris", 40000))
PANELS = "--no-panels" not in argv
KEEP_CORRECTIVES = "--keep-correctives" in argv
REACH = opt("--reach", 0.06)
ANGLE = opt("--angle", 50.0)
os.makedirs(OUT, exist_ok=True)
log = {"body": BODY, "garment": GARMENT, "tris": TRIS, "reach": REACH, "angle": ANGLE}

# 1. The body: its armature and its finest mesh.
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY)
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
meshes = sorted([o for o in bpy.context.scene.objects if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
body = meshes[0]
for o in meshes[1:]:
    bpy.data.objects.remove(o, do_unlink=True)
log["bodyPoints"] = len(body.data.vertices)

# The garment, joined into one mesh.
before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=GARMENT)
parts = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
for o in [o for o in bpy.data.objects if o not in before and o.type != "MESH"]:
    bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.object.select_all(action="DESELECT")
for o in parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
if len(parts) > 1:
    bpy.ops.object.join()
gar = bpy.context.view_layer.objects.active
gar.name = NAME
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# The panels, read at full resolution before the reduction: a vertex group
# per kind, which the reduction carries along (and which is removed again
# before the bones' groups are made).
pb = arm.pose.bones
shoulder = {s: arm.matrix_world @ pb["upperarm_" + s].head for s in "lr"}
mid = (shoulder["l"] + shoulder["r"]) / 2
side = (shoulder["l"] - shoulder["r"]).normalized()
half = (shoulder["l"] - mid).length
KINDS = ("arm_l", "arm_r", "trunk")
if PANELS and "pattern" in gar.data.uv_layers:
    pm = bmesh.new()
    pm.from_mesh(gar.data)
    uv = pm.loops.layers.uv["pattern"]
    pm.faces.ensure_lookup_table()
    isl = [-1] * len(pm.faces)
    k = 0
    for f in pm.faces:
        if isl[f.index] >= 0:
            continue
        isl[f.index] = k
        stack = [f]
        while stack:
            x = stack.pop()
            for lp in x.loops:
                va, ua, ub = lp.vert, lp[uv].uv, lp.link_loop_next[uv].uv
                for l2 in lp.edge.link_loops:
                    y = l2.face
                    if y is x or isl[y.index] >= 0:
                        continue
                    wa, wb = (l2[uv].uv, l2.link_loop_next[uv].uv) if l2.vert is va else (l2.link_loop_next[uv].uv, l2[uv].uv)
                    if (ua - wa).length < 1e-5 and (ub - wb).length < 1e-5:
                        isl[y.index] = k
                        stack.append(y)
        k += 1
    count = [0] * k
    centre = [Vector() for _ in range(k)]
    for f in pm.faces:
        count[isl[f.index]] += 1
        centre[isl[f.index]] += f.calc_center_median()
    kind_of = []
    for i in range(k):
        across = (centre[i] / count[i] - mid).dot(side) / half
        kind_of.append("arm_l" if across > 1.3 else "arm_r" if across < -1.3 else "trunk")
    log["panels"] = [[count[i], kind_of[i]] for i in range(k)]
    groups = {kd: gar.vertex_groups.new(name="_panel_" + kd) for kd in KINDS}
    members = {kd: set() for kd in KINDS}
    for f in pm.faces:
        for v in f.verts:
            members[kind_of[isl[f.index]]].add(v.index)
    for kd in KINDS:
        if members[kd]:
            groups[kd].add(sorted(members[kd]), 1.0, "REPLACE")
    pm.free()
else:
    PANELS = False
log["byPanel"] = PANELS
tris_before = sum(len(p.vertices) - 2 for p in gar.data.polygons)
log["trisBefore"] = tris_before
if tris_before > TRIS:
    dec = gar.modifiers.new("Decimate", "DECIMATE")
    dec.ratio = TRIS / tris_before
    dec.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier=dec.name)
log["tris"] = sum(len(p.vertices) - 2 for p in gar.data.polygons)
log["points"] = len(gar.data.vertices)
mask = {kd: np.zeros(len(gar.data.vertices), dtype=np.float32) for kd in KINDS}
if PANELS:
    gi = {gar.vertex_groups["_panel_" + kd].index: kd for kd in KINDS}
    for v in gar.data.vertices:
        for g in v.groups:
            if g.group in gi:
                mask[gi[g.group]][v.index] = g.weight
    for kd in KINDS:
        gar.vertex_groups.remove(gar.vertex_groups["_panel_" + kd])

# 2. The body's surface in world space, and its weights as a matrix.
bb = bmesh.new()
bb.from_mesh(body.data)
bb.transform(body.matrix_world)
bmesh.ops.triangulate(bb, faces=bb.faces[:])
bb.faces.ensure_lookup_table()
bb.verts.ensure_lookup_table()
bvh = BVHTree.FromBMesh(bb)
names = [g.name for g in body.vertex_groups]
W = np.zeros((len(body.data.vertices), len(names)), dtype=np.float32)
for v in body.data.vertices:
    for g in v.groups:
        W[v.index, g.group] = g.weight

gm = gar.data
gm.calc_normals_split() if hasattr(gm, "calc_normals_split") else None
n = len(gm.vertices)
G = np.zeros((n, len(names)), dtype=np.float32)
reliable = np.zeros(n, dtype=bool)
cos_limit = math.cos(math.radians(ANGLE))


# The arm: the upper arm and every bone under it, on each side.
def under(bone):
    out = [bone.name]
    for c in bone.children:
        out += under(c)
    return out


chain = {s: [names.index(b) for b in under(arm.data.bones["upperarm_" + s]) if b in names] for s in "lr"}
arm_share = {s: W[:, chain[s]].sum(axis=1) for s in "lr"}
# What the trunk may not follow: the arm, and unless kept, its correctives.
kept = set()
if KEEP_CORRECTIVES:
    for s in "lr":
        root = arm.data.bones.get("upperarm_correctiveRoot_" + s)
        kept |= set(under(root)) if root else set()
not_trunk = [j for j in chain["l"] + chain["r"] if names[j] not in kept]
log["keepCorrectives"] = sorted(kept)
# The body's surface split the same way: a triangle is the arm's where its
# points hang mostly on that arm's bones, the trunk's otherwise.
tri_kind = []
for f in bb.faces:
    ids = [x.index for x in f.verts]
    al, ar = arm_share["l"][ids].mean(), arm_share["r"][ids].mean()
    tri_kind.append("arm_l" if al >= 0.5 else "arm_r" if ar >= 0.5 else "trunk")
verts_co = [v.co.copy() for v in bb.verts]
surface = {}
for kd in KINDS:
    faces = [f for f, tk in zip(bb.faces, tri_kind) if tk == kd]
    surface[kd] = (BVHTree.FromPolygons(verts_co, [[x.index for x in f.verts] for f in faces]), faces)
surface["all"] = (bvh, list(bb.faces))


def copy_from(kd, p, normal):
    tree, faces = surface[kd]
    loc, fnorm, fi, dist = tree.find_nearest(p)
    if loc is None:
        return None, 1e9, 0.0
    f = faces[fi]
    bary = poly_3d_calc([x.co for x in f.verts], loc)
    w = sum(b * W[x.index] for b, x in zip(bary, f.verts))
    if kd == "trunk":
        w = w.copy()
        w[not_trunk] = 0.0
    return w, dist, abs(normal.dot(fnorm.normalized()))


seam = 0
for v in gm.vertices:
    p = gar.matrix_world @ v.co
    nrm = v.normal.normalized()
    if PANELS:
        ml, mr, mt = mask["arm_l"][v.index], mask["arm_r"][v.index], mask["trunk"][v.index]
        sleeve = "arm_l" if ml >= mr else "arm_r"
        ms = max(ml, mr)
        kinds = [(sleeve, ms), ("trunk", mt)] if ms > 0.25 and mt > 0.25 else [(sleeve if ms > mt else "trunk", 1.0)]
    else:
        kinds = [("all", 1.0)]
    seam += len(kinds) > 1
    acc, ok = np.zeros(len(names), dtype=np.float32), True
    for kd, share in kinds:
        w, dist, facing = copy_from(kd, p, nrm)
        if w is None or w.sum() < 1e-6:
            ok = False
            continue
        acc += share * w / w.sum()
        ok = ok and dist <= REACH and facing >= cos_limit
    G[v.index] = acc
    reliable[v.index] = ok and acc.sum() > 1e-6
log["seamPoints"] = seam
log["reliable"] = int(reliable.sum())
log["inpainted"] = int(n - reliable.sum())

# 3. The repair: unreliable points take their weights from their neighbours.
gb = bmesh.new()
gb.from_mesh(gm)
gb.verts.ensure_lookup_table()
nbrs = [[e.other_vert(v).index for e in v.link_edges] for v in gb.verts]
unrel = np.where(~reliable)[0]
if len(unrel) and reliable.any():
    for _ in range(400):
        new = G.copy()
        for i in unrel:
            if nbrs[i]:
                new[i] = G[nbrs[i]].mean(axis=0)
        G = new

# 4. A light smoothing everywhere, at most eight bones, normalised.
for _ in range(3):
    S = G.copy()
    for i in range(n):
        if nbrs[i]:
            S[i] = 0.5 * G[i] + 0.5 * G[nbrs[i]].mean(axis=0)
    G = S
keep = 8
if G.shape[1] > keep:
    cut = np.argsort(G, axis=1)[:, :-keep]
    np.put_along_axis(G, cut, 0.0, axis=1)
sums = G.sum(axis=1, keepdims=True)
sums[sums == 0] = 1.0
G = G / sums
used = [j for j in range(len(names)) if G[:, j].max() > 1e-4]
log["bones"] = [names[j] for j in used]

# 5. Onto the skeleton, and out.
for j in used:
    vg = gar.vertex_groups.new(name=names[j])
    for i in np.where(G[:, j] > 1e-4)[0]:
        vg.add([int(i)], float(G[i, j]), "REPLACE")
gar.parent = arm
gar.matrix_parent_inverse = arm.matrix_world.inverted()
mod = gar.modifiers.new("Armature", "ARMATURE")
mod.object = arm
bpy.data.objects.remove(body, do_unlink=True)
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
gar.select_set(True)
bpy.context.view_layer.objects.active = arm
out_fbx = os.path.join(OUT, NAME + "_skinned.fbx")
bpy.ops.export_scene.fbx(filepath=out_fbx, use_selection=True, object_types={"ARMATURE", "MESH"},
                         add_leaf_bones=False, mesh_smooth_type="FACE", bake_anim=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_skinned.blend"))
log["fbx"] = out_fbx
json.dump(log, open(os.path.join(OUT, "bind.json"), "w"), indent=1)
print("BIND", json.dumps({k: v for k, v in log.items() if k != "bones"}), "bones=%d" % len(log["bones"]), flush=True)
