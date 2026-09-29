"""A close garment tested as the game wears it, skinned to the body: arms down, arms raised, walking, sitting.

    blender -b -P tools/meshgen/blender/pose_skinned.py -- FINISHED.blend OUT_DIR --render CardiganRender [--poses down,up,walk,sit]

(Written 29 September for Sheila's cardigan, from pose_trousers.py: a close
knit is skinned from the body with no cloth, the research says,
SHEILA-CLOTHES-2026-09-29.md. Its weights are the body's own, each point
those of the nearest place on her skin, smoothed; the small pieces sewn on it
(bands, buttons, the collar) take the weights of the knit's nearest point,
so nothing parts from it; the body the garment always covers is hidden in
the pictures, as the game hides it. What follows is pose_trousers.py's own
note, most of which applies.)

WHY, 29 September (the clothing session; Jafar's rule: every garment tested
walking, sitting and with arms raised before it goes to the builder; the
arms do not move trousers). Close garments are skinned in games, not
simulated (production/research/clothing-pipeline/TROUSERS-AND-CAP-2026-09-29.md),
so the test is the skinning: the finished render mesh takes the body's own
skin weights (each point those of the nearest place on the body, the arms'
and hands' taken off, smoothed over the cloth), rides the skeleton into each
pose (tailor.make_pose), and is measured there against the posed body
without its parted thighs (the true body): points of the trousers inside
it, and how far the skinning stretches the cloth's edges.

OUT_DIR gets pose-NAME-front.png, -side.png, -three-quarter.png and
pose-test.json.
"""
import json
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, OUT = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


POSES = opt("--poses", "down,up,walk,sit", str).split(",")
RENDER = opt("--render", "TrousersRender", str)


def say(*a):
    print("POSE", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=BLEND)
garment = bpy.data.objects[RENDER]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = next(o for o in bpy.data.objects if o.type == "MESH" and o is not garment
            and any(m.type == "ARMATURE" for m in o.modifiers))
for o in list(bpy.data.objects):
    if o.type == "MESH" and o not in (garment, body):
        bpy.data.objects.remove(o, do_unlink=True)
if body.data.shape_keys and body.data.shape_keys.key_blocks.get("apart"):
    body.data.shape_keys.key_blocks["apart"].value = 0.0         # the true body, thighs touching
body.hide_render = False
body.hide_set(False)
if arm.animation_data:
    arm.animation_data_clear()
for pb in arm.pose.bones:
    pb.rotation_mode = "QUATERNION"
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()

# ---- the body's own weights, the small pieces glued to the garment -------------------------------------

for g in list(garment.vertex_groups):
    garment.vertex_groups.remove(g)
dt = garment.modifiers.new("Weights", "DATA_TRANSFER")
dt.object = body
dt.use_vert_data = True
dt.data_types_verts = {"VGROUP_WEIGHTS"}
dt.vert_mapping = "POLYINTERP_NEAREST"
dt.layers_vgroup_select_src = "ALL"
dt.layers_vgroup_select_dst = "NAME"
bpy.ops.object.select_all(action="DESELECT")
garment.select_set(True)
bpy.context.view_layer.objects.active = garment
bpy.ops.object.datalayout_transfer(modifier="Weights")
bpy.ops.object.modifier_apply(modifier="Weights")
# ZONE WEIGHTS (--zones; JUMPER-2026-09-30.md, after two reviews failed Ron's
# jumper: fins at the armpits, the known fault of copying the nearest skin's
# weights onto a sweater): below the armpit the side panel carries no arm, its
# arm share going to the spine and a little clavicle; the arm's share rises
# over 9 cm out from the side; the sleeve's last part rides the forearm's
# twist bone and the forearm, no hand
ZONES = "--zones" in argv
if ZONES:
    ARMPIT_Z, SIDE_X = opt("--armpit-z", 1.39), opt("--side-x", 0.215)
    ARMISH_ = ("upperarm", "lowerarm", "hand", "thumb", "index", "middle", "ring", "pinky", "wrist")
    gnames = {g.index: g.name for g in garment.vertex_groups}

    def grp_(nm):
        return garment.vertex_groups.get(nm) or garment.vertex_groups.new(name=nm)
    zoned = 0
    for v in garment.data.vertices:
        p_ = garment.matrix_world @ v.co
        ax_ = abs(p_.x)
        sd = "l" if p_.x > 0 else "r"
        BL = opt("--arm-blend", 0.09)
        if p_.z < ARMPIT_Z + 0.04 and ax_ < SIDE_X + BL:
            f = 0.0 if (ax_ < SIDE_X or p_.z < ARMPIT_Z - 0.06) else (ax_ - SIDE_X) / BL
            f = max(0.0, min(1.0, f))
            if p_.z < ARMPIT_Z - 0.06 and ax_ >= SIDE_X:
                f = max(f, min(1.0, (ax_ - SIDE_X - 0.03) / BL))       # the sleeve hanging beside the body stays on the arm
            freed = 0.0
            for g in list(v.groups):
                if gnames[g.group].startswith(ARMISH_):
                    freed += g.weight * (1.0 - f)
                    garment.vertex_groups[g.group].add([v.index], g.weight * f, "REPLACE")
            if freed > 0:
                for nm, share in (("spine_04", 0.5), ("spine_03", 0.3), ("clavicle_" + sd, 0.2)):
                    gg = grp_(nm)
                    cur = next((g.weight for g in v.groups if g.group == gg.index), 0.0)
                    gg.add([v.index], cur + freed * share, "REPLACE")
                zoned += 1
    CUFF_T = opt("--cuff-zone-t", 0.0)
    if CUFF_T > 0:
        for v in garment.data.vertices:
            p_ = garment.matrix_world @ v.co
            sd = "l" if p_.x > 0 else "r"
            if abs(p_.x) < 0.25:
                continue
            a_ = arm.matrix_world @ arm.pose.bones["lowerarm_" + sd].head
            h_ = arm.matrix_world @ arm.pose.bones["hand_" + sd].head
            t = (p_ - a_).dot(h_ - a_) / (h_ - a_).length_squared
            if t > CUFF_T:
                for gidx in [g.group for g in v.groups]:
                    garment.vertex_groups[gidx].remove([v.index])
                grp_("lowerarm_twist_01_" + sd).add([v.index], 0.6, "REPLACE")
                grp_("lowerarm_" + sd).add([v.index], 0.4, "REPLACE")
bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
bpy.ops.object.vertex_group_smooth(group_select_mode="ALL", factor=0.5, repeat=opt("--smooth", 6, int))
bpy.ops.object.vertex_group_normalize_all(group_select_mode="ALL", lock_active=False)
bpy.ops.object.mode_set(mode="OBJECT")
from mathutils.kdtree import KDTree
bm_ = bmesh.new()
bm_.from_mesh(garment.data)
comp = [-1] * len(bm_.verts)
sizes = []
bm_.verts.ensure_lookup_table()
for v0 in bm_.verts:
    if comp[v0.index] >= 0:
        continue
    cid, stack, n_ = len(sizes), [v0], 0
    comp[v0.index] = cid
    while stack:
        v = stack.pop()
        n_ += 1
        for e in v.link_edges:
            o = e.other_vert(v)
            if comp[o.index] < 0:
                comp[o.index] = cid
                stack.append(o)
    sizes.append(n_)
bm_.free()
main = int(np.argmax(sizes))
gco = np.array([garment.matrix_world @ v.co for v in garment.data.vertices])
cloth_ids = [i for i, c in enumerate(comp) if c == main]
kd = KDTree(len(cloth_ids))
for k, i in enumerate(cloth_ids):
    kd.insert(Vector(gco[i]), k)
kd.balance()
names = {g.index: g for g in garment.vertex_groups}
wmap = {i: [(g.group, g.weight) for g in garment.data.vertices[i].groups] for i in cloth_ids}
glued = 0
# the small pieces by their place (--zones): the welt's points take the knit's weights at the same angle a
# little above the welt (the same up each column: nearest-point copies stepped and stood out as a shelf); the
# neckband blends from the knit's edge to spine_05 and neck_01 at its top; the cuffs ride the forearm's twist
comp_z = {}
for i, c in enumerate(comp):
    comp_z.setdefault(c, []).append(gco[i][2])
HEM = opt("--hem", 0.0)
cxy = np.array([float(np.mean(gco[:, 0])), float(np.mean(gco[:, 1]))])
for i, c in enumerate(comp):
    if c == main:
        continue
    zc = float(np.mean(comp_z[c]))
    target = Vector(gco[i])
    if ZONES and HEM > 0 and zc < HEM + 0.08:
        d_ = Vector((gco[i][0] - cxy[0], gco[i][1] - cxy[1], 0.0))
        target = Vector((gco[i][0], gco[i][1], HEM + opt("--welt", 0.05) + 0.02)) + (d_.normalized() * 0.01 if d_.length > 0 else Vector())
    _p, k, _d = kd.find(target)
    if ZONES and zc > opt("--neck-above", 9.0):
        z0, z1 = min(comp_z[c]), max(comp_z[c])
        t_ = (gco[i][2] - z0) / max(1e-6, z1 - z0)
        for gidx in [g.group for g in garment.data.vertices[i].groups]:   # indices first: removing while reading them went stale
            garment.vertex_groups[gidx].remove([i])
        for gi, w in wmap[cloth_ids[k]]:
            names[gi].add([i], w * (1.0 - t_), "REPLACE")
        front = gco[i][1] < cxy[1]
        for nm, w in (("spine_05", 0.7 if front else 0.55), ("neck_01", 0.3 if front else 0.45)):
            gg = garment.vertex_groups.get(nm) or garment.vertex_groups.new(name=nm)
            names[gg.index] = gg
            cur = next((g.weight for g in garment.data.vertices[i].groups if g.group == gg.index), 0.0)
            gg.add([i], cur + w * t_, "REPLACE")
        glued += 1
        continue
    for gidx in [g.group for g in garment.data.vertices[i].groups]:
        garment.vertex_groups[gidx].remove([i])
    for gi, w in wmap[cloth_ids[k]]:
        names[gi].add([i], w, "REPLACE")
    glued += 1
# the body the garment always covers, hidden in the pictures (not in the measure)
covered = body.vertex_groups.get("covered") or body.vertex_groups.new(name="covered")
bco = np.array([body.matrix_world @ v.co for v in body.data.vertices])
kd2 = KDTree(len(cloth_ids))
for k, i in enumerate(cloth_ids):
    kd2.insert(Vector(gco[i]), k)
kd2.balance()
# only well inside the garment's edges (the first cardigan review: white at
# the hips below the hem, at the neck, between cuff and hand, where the body
# was hidden past the cardigan's edge): a body point is hidden if the garment
# is within 3 cm of it and that garment point is 4 cm or more from an edge
_bmg = bmesh.new()
_bmg.from_mesh(garment.data)
_edge_pts = [garment.matrix_world @ v.co for v in _bmg.verts if v.is_boundary and comp[v.index] == main]
_bmg.free()
kd3 = KDTree(max(1, len(_edge_pts)))
for k, q in enumerate(_edge_pts):
    kd3.insert(q, k)
kd3.balance()
deep_cloth = [i for i in cloth_ids if not _edge_pts or kd3.find(Vector(gco[i]))[2] > opt("--edge-keep", 0.08)]
kd2 = KDTree(max(1, len(deep_cloth)))
for k, i in enumerate(deep_cloth):
    kd2.insert(Vector(gco[i]), k)
kd2.balance()
# and never above --hide-below (the neck's base showed through at the throat when hidden near it)
ids_cov = [i for i, q in enumerate(bco) if kd2.find(Vector(q))[2] < opt("--cover", 0.025) and opt("--hide-above", -9.0) < q[2] < opt("--hide-below", 9.0)]
# ERODED (Ron's second review: square holes at the waist, wrists and seat,
# where a hidden point took its whole large face of the body with it): a
# point stays hidden only if all its neighbours are covered too, twice over,
# so no removed face reaches past the covered skin
_cov = set(ids_cov)
_bb = bmesh.new()
_bb.from_mesh(body.data)
_bb.verts.ensure_lookup_table()
for _ in range(opt("--erode", 2, int)):
    _cov = {i for i in _cov if all(e.other_vert(_bb.verts[i]).index in _cov for e in _bb.verts[i].link_edges)}
_bb.free()
ids_cov = sorted(_cov)
covered.add(ids_cov, 1.0, "REPLACE")
mask = body.modifiers.new("Covered", "MASK")
mask.vertex_group = "covered"
mask.invert_vertex_group = True
mask.show_viewport = False
log_rigid = glued
side_cut = 0
# TRIMS THAT ARE PART OF THE ONE MESH (--grown; the jacket's last attempt grows its collar, waistband and cuffs
# from its own edges, so they are no longer separate pieces to glue): the waistband's points below the hem take
# the weights of the knit just above them at the same place round (the same all down each column: copied from
# the nearest skin, the seated band crumpled into sawtooth layers); the collar's points above --neck-above blend
# onto spine_05 and neck_01 towards its top
if "--grown" in argv:
    HEM_G = opt("--hem", 0.0)
    NECK_G = opt("--neck-above", 9.0)
    top_g = float(gco[:, 2].max())
    wmap2 = {i: [(g.group, g.weight) for g in garment.data.vertices[i].groups] for i in cloth_ids}
    grown = 0
    for i in cloth_ids:
        z = gco[i][2]
        if HEM_G > 0 and z < HEM_G - 0.002:
            _p, k, _d = kd.find(Vector((gco[i][0], gco[i][1], HEM_G + 0.03)))
            src = wmap2[cloth_ids[k]]
            for gidx in [g.group for g in garment.data.vertices[i].groups]:
                garment.vertex_groups[gidx].remove([i])
            for gi, w in src:
                garment.vertex_groups[gi].add([i], w, "REPLACE")
            grown += 1
        elif z > NECK_G:
            t_ = min(1.0, (z - NECK_G) / max(1e-6, top_g - NECK_G))
            for gidx, w in [(g.group, g.weight) for g in garment.data.vertices[i].groups]:
                garment.vertex_groups[gidx].add([i], w * (1.0 - t_), "REPLACE")
            front = gco[i][1] < cxy[1]
            for nm, w in (("spine_05", 0.7 if front else 0.55), ("neck_01", 0.3 if front else 0.45)):
                gg = garment.vertex_groups.get(nm) or garment.vertex_groups.new(name=nm)
                cur = next((g.weight for g in garment.data.vertices[i].groups if g.group == gg.index), 0.0)
                gg.add([i], cur + w * t_, "REPLACE")
            grown += 1
    log_rigid = grown
# SITTING (CARDIGAN-BUILD-2026-09-29.md): below the waist the back rides the
# pelvis and lower spine, no thigh; the front's sides take at most 30% of a
# thigh (the second review: the back ballooned into a hump when she sat)
Z_WAIST = opt("--waist-z", 0.0)
if Z_WAIST > 0:
    cy_g = float(np.mean(gco[:, 1]))
    names = {g.index: g for g in garment.vertex_groups}
    pel_g = garment.vertex_groups.get("pelvis") or garment.vertex_groups.new(name="pelvis")
    sp_g = garment.vertex_groups.get("spine_01") or garment.vertex_groups.new(name="spine_01")
    for v in garment.data.vertices:
        p_ = gco[v.index]
        if p_[2] > Z_WAIST:
            continue
        thigh_w = sum(g.weight for g in v.groups if names[g.group].name.startswith("thigh"))
        if thigh_w <= 0:
            continue
        cap = 0.0 if p_[1] > cy_g else 1.0            # the front keeps its own (capped at 30%, the thighs came through it)
        if thigh_w > cap:
            k_ = cap / thigh_w
            for g in list(v.groups):
                if names[g.group].name.startswith("thigh"):
                    names[g.group].add([v.index], g.weight * k_, "REPLACE")
            freed = thigh_w - cap
            cur_p = next((g.weight for g in v.groups if g.group == pel_g.index), 0.0)
            cur_s = next((g.weight for g in v.groups if g.group == sp_g.index), 0.0)
            pel_g.add([v.index], cur_p + freed * 0.7, "REPLACE")
            sp_g.add([v.index], cur_s + freed * 0.3, "REPLACE")
am = garment.modifiers.new("Armature", "ARMATURE")
am.object = arm

bm = bmesh.new()
bm.from_mesh(garment.data)
EDGES = np.array([[e.verts[0].index, e.verts[1].index] for e in bm.edges])
bm.free()
REST = tailor.coords(garment)
L0 = np.linalg.norm(REST[EDGES[:, 1]] - REST[EDGES[:, 0]], axis=1)
log = {"blend": BLEND, "poses": {}, "gluedToCloth": log_rigid, "bodyHidden": len(ids_cov)}
grey = tailor.material("M_Body", (0.5, 0.5, 0.5))
body.data.materials.clear()
body.data.materials.append(grey)

for name in POSES:
    for pb in arm.pose.bones:
        pb.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()
    tailor.make_pose(arm, name)
    bpy.context.view_layer.update()
    co = tailor.coords(garment)
    bev = tailor.evaluated_copy(body, "BodyPosed")
    bvh = tailor.bvh_of(bev)
    bpy.data.objects.remove(bev, do_unlink=True)
    deep = np.array([tailor.depth_inside(bvh, Vector(p)) for p in co])
    ln = np.linalg.norm(co[EDGES[:, 1]] - co[EDGES[:, 0]], axis=1)
    r = ln / np.maximum(L0, 1e-9)
    ok = L0 > 1e-6
    lo_z, hi_z = float(co[:, 2].min()), float(co[:, 2].max())
    worst = [[round(float(c), 3) for c in co[i]] for i in np.argsort(-deep)[:4] if deep[i] > 0.003]
    log["poses"][name] = {"insideOver3mm": int((deep > 0.003).sum()), "deepestMm": round(float(deep.max()) * 1000, 1),
                          "whereDeepest": worst,
                          "stretch95": round(float(np.percentile(r[ok], 95)), 3), "stretchMax": round(float(r[ok].max()), 2),
                          "squeeze5": round(float(np.percentile(r[ok], 5)), 3)}
    say(name, json.dumps(log["poses"][name]))
    mid = Vector((float(co[:, 0].mean()), float(co[:, 1].mean()), 0.5 * (lo_z + hi_z)))
    tailor.pictures(os.path.join(OUT, "pose-%s" % name), mid,
                    views=(("front", (0, -3.2, 0.2)), ("side", (3.2, 0, 0.2)), ("three-quarter", (2.2, -2.3, 0.4))))
json.dump(log, open(os.path.join(OUT, "pose-test.json"), "w"), indent=1)
say("done")
