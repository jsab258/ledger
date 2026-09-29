"""Trousers tested as the game wears them, skinned to the body: walking, sitting, a foot up a stair.

    blender -b -P tools/meshgen/blender/pose_trousers.py -- FINISHED.blend OUT_DIR [--poses walk,sit,stair]

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


POSES = opt("--poses", "walk,sit,stair", str).split(",")
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

# ---- the body's weights, the arms' off, smoothed ------------------------------------------------

# ZONE WEIGHTS ON THE MAIN BONES (production/research/clothing-pipeline/
# SKINNING-TROUSERS-2026-09-29.md, after two blind reviews failed the posed
# trousers: copied from the nearest skin, the waist fell away sitting, the
# hems cinched round the ankles, the belt folded like a concertina). Each
# point's weights come from where it is, not from the skin under it:
#   the belt, band, loops and the cloth's top 3 cm: one ring on the pelvis,
#     the spine (spine_01) taking up to 40% at the centre back, no leg;
#   below it the pelvis gives way to the thigh of its own side: at the front
#     from 3 cm under the top to 12 cm (the lap folds under the belt, not
#     through it); at the back by the seat's height (0.7 at its top, 0.5 at
#     the buttock's widest, 0.2 at its fold, none below);
#   by the middle seam each side's thigh fades to the pelvis over 7 cm;
#   the knee blends thigh to calf over 15 cm; below it the calf alone, the
#   same all round every ring, so the hem hangs open (no foot, no ankle).
for g in list(garment.vertex_groups):
    garment.vertex_groups.remove(g)
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
AXC = np.array([0.0, float(gco[:, 1].mean())])
ang = np.arctan2(gco[:, 0] - AXC[0], gco[:, 1] - AXC[1])        # 0 at the centre back (+y), pi at the front
back_f = np.clip(np.cos(ang), 0.0, 1.0)                          # 1 at the centre back, 0 at the sides and front
front_f = np.clip(-np.cos(ang), 0.0, 1.0)
sector = ((np.degrees(ang) + 180.0) // 10).astype(int)
top_by = {}
for sct, z, c in zip(sector, gco[:, 2], comp):
    if c == main:
        top_by[sct] = max(top_by.get(sct, -9.0), z)
KNEE = float(tailor.joint(arm, "calf_l").z)
CROTCH = opt("--crotch", 0.885)
SEAT_Z = [(1.10, 0.7), (1.00, 0.7), (0.97, 0.5), (0.87, 0.2), (0.82, 0.0), (-1.0, 0.0)]
bones = {}


def grp(name):
    if name not in bones:
        bones[name] = garment.vertex_groups.get(name) or garment.vertex_groups.new(name=name)
    return bones[name]


def seat_share(z):
    zs = [a for a, _ in SEAT_Z][::-1]
    ws = [b for _, b in SEAT_Z][::-1]
    return float(np.interp(z, zs, ws))


# which small pieces are the belt, band and loops (at the top: the ring) and which are sewn onto the cloth
# lower down (the pockets' lips and welts, the fly: they follow the cloth under them; as part of the ring the
# back welts stood off the seat like rods when he sat)
comp_top = {}
for i, c in enumerate(comp):
    if c != main:
        comp_top[c] = min(comp_top.get(c, 9.0), top_by.get(sector[i], gco[i, 2]) - gco[i, 2])
RING = {c for c, d in comp_top.items() if d < 0.02}
cloth_w = {}
for i, (p, c) in enumerate(zip(gco, comp)):
    side = "_l" if p[0] > 0 else "_r"
    spine = 0.4 * back_f[i]
    if c in RING:                                                # the belt, band and loops: the ring
        w = {"pelvis": 1.0 - spine, "spine_01": spine}
    elif c != main:
        continue                                                 # sewn-on pieces: after the cloth, from it
    else:
        depth = top_by.get(sector[i], p[2]) - p[2]
        if depth < 0.03:
            pel, sp = 1.0 - spine, spine
        else:
            fade = min(1.0, (depth - 0.03) / 0.03)
            sp = spine * (1.0 - fade)
            front_pel = float(np.interp(depth, [0.03, 0.12, 0.25], [1.0, 0.3, 0.0]))
            back_pel = seat_share(p[2])
            pel = (front_f[i] * front_pel + (1.0 - front_f[i]) * max(back_pel, front_pel * (1.0 - back_f[i]))) * (1.0 - sp)
        if p[2] > CROTCH - 0.03 and abs(p[0]) < 0.07:               # by the middle seam, towards the pelvis
            pel = pel + (1.0 - pel - sp) * (1.0 - abs(p[0]) / 0.07)
        leg = max(0.0, 1.0 - pel - sp)
        k = float(np.clip((KNEE + 0.075 - p[2]) / 0.15, 0.0, 1.0))  # 0 above the knee's blend, 1 below it
        w = {"pelvis": pel, "spine_01": sp, "thigh" + side: leg * (1.0 - k), "calf" + side: leg * k}
    tot = sum(w.values())
    w = {nm: wt / tot for nm, wt in w.items() if wt > 1e-4}
    if c == main:
        cloth_w[i] = w
    for nm, wt in w.items():
        grp(nm).add([i], wt, "REPLACE")
cloth_ids = list(cloth_w)
kd = KDTree(len(cloth_ids))
for k, i in enumerate(cloth_ids):
    kd.insert(Vector(gco[i]), k)
kd.balance()
for i, c in enumerate(comp):
    if c == main or c in RING:
        continue
    _p, k, _d = kd.find(Vector(gco[i]))
    for nm, wt in cloth_w[cloth_ids[k]].items():
        grp(nm).add([i], wt, "REPLACE")
side_cut = 0
log_rigid = sum(1 for c in comp if c != main)
# THE BODY THE TROUSERS ALWAYS COVER IS HIDDEN, as the game's Body Hidden Face
# Map hides it (the research): the legs from 8 cm above the hem to 6 cm under
# the band's lowest point, where the cloth never leaves them
lo_z = float(gco[comp == np.int64(main) if False else [c == main for c in comp], 2].min()) if False else float(min(gco[i, 2] for i, c in enumerate(comp) if c == main))
band_lo = min(top_by.values()) - 0.06
cover = body.vertex_groups.get("covered") or body.vertex_groups.new(name="covered")
bco = np.array([body.matrix_world @ v.co for v in body.data.vertices])
ids_cov = [i for i, q in enumerate(bco) if lo_z + 0.08 < q[2] < band_lo and abs(q[0]) < 0.3]
cover.add(ids_cov, 1.0, "REPLACE")
mask = body.modifiers.new("Covered", "MASK")
mask.vertex_group = "covered"
mask.invert_vertex_group = True
mask.show_viewport = False              # measured against the whole body; the pictures (render) hide the covered part
am = garment.modifiers.new("Armature", "ARMATURE")
am.object = arm

bm = bmesh.new()
bm.from_mesh(garment.data)
EDGES = np.array([[e.verts[0].index, e.verts[1].index] for e in bm.edges])
bm.free()
REST = tailor.coords(garment)
L0 = np.linalg.norm(REST[EDGES[:, 1]] - REST[EDGES[:, 0]], axis=1)
log = {"blend": BLEND, "poses": {}, "gluedToCloth": log_rigid, "otherLegWeightsCut": side_cut}
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
