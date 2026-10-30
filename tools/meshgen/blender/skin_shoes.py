"""A pair of rigid shoes skinned to a MetaHuman's feet, each level of detail exported as one skinned FBX the way
skin_garment.py exports garments (30 October 2026, Tom's shoes from the scanned oxford).

    blender -b --factory-startup -P tools/meshgen/blender/skin_shoes.py -- BODY.fbx GAME.blend OUT_DIR NAME
        --objects ShoeR_LOD0,ShoeR_LOD1,ShoeR_LOD2,ShoeR_LOD3 [--side r] [--blend 0.02] [--slant 0.015]
        [--hidden FIT.blend]

WHY: a shoe is a stiff solid; only its toe bends, at the ball, as the sole flexes there (production/research/
clothing-pipeline/FOOTWEAR-2026-09-30.md: heel, quarters and the sole under the arch on foot, the toe box on ball,
no toe bones; model_footwear.py's weigh()). Each given object is one shoe (--side, as placed on the body); its
mirror across the body's middle (faces turned back out, the layout shared) is the other. Weights: foot_<side>
behind the ball line, ball_<side> in front, smoothly over --blend metres across a line through the ball joint,
square to the foot, slanted so its inner side lies --slant metres further forward (the joints' own slant). Two
influences a point at most. The armature is the body FBX's own (as skin_garment.py: everything else cleared first,
the body imported, its finest mesh kept for the pose check), the export skin_garment.py's settings, the maps'
layout first (uv_order.py).

OUT_DIR gets NAME_LODk_skinned.fbx for each object in order (LOD0 first; NAME_skinned.fbx is LOD0 again, the name
the garment path takes), NAME_skinned.blend (the pair at every level, the body and its skeleton, for
shoe_pose_check.py) and skin.json. With --hidden, the fit's "in_shoe" vertex group of the body (the foot hidden
under the shoes) is copied onto this body, listed in hidden_body_vertices.json, and drawn in the body's first UV
layout as hidden_face_map.png (white = hidden, a face hidden when all its points are), for the Body Hidden Face Map.
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
BODY, GAME, OUT, NAME = argv[:4]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
OBJS = opt("--objects", "ShoeR_LOD0", str).split(",")
SIDE = opt("--side", "r", str)
BLEND = opt("--blend", 0.02)
SLANT = opt("--slant", 0.015)
HIDDEN = opt("--hidden", None, str)
os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
log = {"body": BODY, "game": GAME, "objects": OBJS, "side": SIDE, "blendM": BLEND, "slantM": SLANT, "levels": {}}


def say(*a):
    print("SHOESKIN", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=GAME)
shoes = [bpy.data.objects[n] for n in OBJS]
for o in list(bpy.data.objects):
    if o not in shoes:
        bpy.data.objects.remove(o, do_unlink=True)
for o in shoes:
    o.data.transform(o.matrix_world)
    o.matrix_world.identity()
before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=BODY)
new = [o for o in bpy.data.objects if o not in before]
arm = next(o for o in new if o.type == "ARMATURE")
bodies = sorted([o for o in new if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
body = bodies[0]
for o in bodies[1:]:
    bpy.data.objects.remove(o, do_unlink=True)
CO = np.array([tuple(body.matrix_world @ v.co) for v in body.data.vertices])
FLOOR = float(CO[:, 2].min())
J = lambda n: np.array(arm.matrix_world @ arm.pose.bones[n].head)  # noqa: E731


def frame(side):
    sg = 1.0 if side == "l" else -1.0
    sole = CO[(CO[:, 0] * sg > 0.04) & (CO[:, 2] < FLOOR + 0.03)]
    c2 = sole[:, :2].mean(0)
    _, _, vt = np.linalg.svd(sole[:, :2] - c2)
    d = vt[0] if vt[0][1] < 0 else -vt[0]
    D = np.array([d[0], d[1], 0.0])
    lat = np.cross([0, 0, 1.0], D) * sg
    foot = CO[(CO[:, 0] * sg > 0.03) & (CO[:, 2] < FLOOR + 0.06)]
    heel = np.array([c2[0], c2[1], FLOOR]) + D * ((foot[:, :2] - c2) @ d).min()
    sb = float((J("ball_" + side) - heel) @ D)
    return {"D": D, "lat": lat, "heel": heel, "sBall": sb}


FRM = {s: frame(s) for s in "lr"}
log["ballLineSMm"] = {s: round(FRM[s]["sBall"] * 1000, 1) for s in "lr"}


def weigh(o, side):
    F = FRM[side]
    P = np.array([tuple(v.co) for v in o.data.vertices])
    q = P - F["heel"]
    s, e = q @ F["D"], q @ F["lat"]
    line = F["sBall"] + SLANT * np.clip(-e / 0.04, -1.0, 1.0)      # the inner side (e < 0) further forward
    t = np.clip((s - line + BLEND / 2) / BLEND, 0.0, 1.0)
    wb = t * t * (3 - 2 * t)
    wf = 1.0 - wb
    for vg in list(o.vertex_groups):
        o.vertex_groups.remove(vg)
    gf = o.vertex_groups.new(name="foot_" + side)
    gb = o.vertex_groups.new(name="ball_" + side)
    for i in range(len(P)):
        if wf[i] > 1e-4:
            gf.add([i], float(wf[i]), "REPLACE")
        if wb[i] > 1e-4:
            gb.add([i], float(wb[i]), "REPLACE")
    return {"points": len(P), "onBallOnly": int((wb > 0.9999).sum()), "blended": int(((wb > 1e-4) & (wb < 0.9999)).sum())}


other = "l" if SIDE == "r" else "r"
sys.path.insert(0, HERE)
from uv_order import maps_layout_first  # noqa: E402
pairs = []
for k, o in enumerate(shoes):
    m = o.copy()
    m.data = o.data.copy()
    bpy.context.scene.collection.objects.link(m)
    for v in m.data.vertices:
        v.co.x = -v.co.x
    bm = bmesh.new()
    bm.from_mesh(m.data)
    bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
    bm.to_mesh(m.data)
    bm.free()
    m.data.update()
    wa = weigh(o, SIDE)
    wo = weigh(m, other)
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    m.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.join()
    pair = bpy.context.active_object
    pair.name = "%s_LOD%d" % (NAME, k)
    pair.data.name = pair.name
    for p in pair.data.polygons:
        p.use_smooth = True
    # at most two influences: checked
    inf = max(len([g for g in v.groups if g.weight > 1e-4]) for v in pair.data.vertices)
    sums = np.array([sum(g.weight for g in v.groups) for v in pair.data.vertices])
    mw = pair.matrix_world.copy()
    pair.parent = arm
    pair.matrix_world = mw
    mod = pair.modifiers.new("Armature", "ARMATURE")
    mod.object = arm
    uvr = maps_layout_first(pair)
    tris = sum(len(p.vertices) - 2 for p in pair.data.polygons)
    log["levels"][pair.name] = {"tris": tris, SIDE: wa, other: wo, "maxInfluences": inf,
                                "weightSumMin": round(float(sums.min()), 4), "weightSumMax": round(float(sums.max()), 4),
                                "uvLayers": [u.name for u in pair.data.uv_layers], "uvReordered": uvr}
    say(pair.name, json.dumps(log["levels"][pair.name]))
    pairs.append(pair)

for k, pair in enumerate(pairs):
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    pair.select_set(True)
    bpy.context.view_layer.objects.active = arm
    for path in ([os.path.join(OUT, "%s_LOD%d_skinned.fbx" % (NAME, k))] +
                 ([os.path.join(OUT, NAME + "_skinned.fbx")] if k == 0 else [])):
        bpy.ops.export_scene.fbx(filepath=path, use_selection=True, object_types={"ARMATURE", "MESH"},
                                 add_leaf_bones=False, mesh_smooth_type="OFF", use_tspace=True, colors_type="LINEAR",
                                 bake_anim=False)
log["files"] = sorted(f for f in os.listdir(OUT) if f.endswith(".fbx"))

# the body's hidden part, from the fit
if HIDDEN:
    with bpy.data.libraries.load(HIDDEN) as (src, dst):
        dst.objects = [n for n in src.objects if n not in ("ShoeR", "ShoeL")]
    fb = next(o for o in dst.objects if o is not None and o.type == "MESH" and "in_shoe" in o.vertex_groups)
    if len(fb.data.vertices) != len(body.data.vertices):
        raise SystemExit("SHOESKIN the fit's body has %d points, this body %d" % (len(fb.data.vertices), len(body.data.vertices)))
    gi = fb.vertex_groups["in_shoe"].index
    ids = [v.index for v in fb.data.vertices if any(g.group == gi and g.weight > 0.5 for g in v.groups)]
    vg = body.vertex_groups.new(name="in_shoe")
    vg.add(ids, 1.0, "REPLACE")
    json.dump({"body": BODY, "mesh": body.name, "vertices": ids}, open(os.path.join(OUT, "hidden_body_vertices.json"), "w"))
    hid = np.zeros(len(body.data.vertices), bool)
    hid[ids] = True
    faces = [p for p in body.data.polygons if all(hid[i] for i in p.vertices)]
    log["hidden"] = {"vertices": len(ids), "faces": len(faces), "uvLayer": body.data.uv_layers[0].name}
    try:
        from PIL import Image, ImageDraw  # noqa: F401
        have_pil = True
    except Exception:
        have_pil = False
    size = 2048
    im = bpy.data.images.new("hidden_face_map", size, size, alpha=False)
    px = np.zeros((size, size, 4), np.float32)
    px[..., 3] = 1
    uv = body.data.uv_layers[0].data
    for p in faces:
        pts = np.array([tuple(uv[li].uv) for li in p.loop_indices]) * size - 0.5
        for a in range(1, len(pts) - 1):
            T = np.array([pts[0], pts[a], pts[a + 1]])
            x0, y0 = np.floor(T.min(0)).astype(int)
            x1, y1 = np.ceil(T.max(0)).astype(int)
            x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, size - 1), min(y1, size - 1)
            if x1 < x0 or y1 < y0:
                continue
            X, Y = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
            v0, v1 = T[1] - T[0], T[2] - T[0]
            den = v0[0] * v1[1] - v1[0] * v0[1]
            if abs(den) < 1e-12:
                continue
            wx, wy = X - T[0][0], Y - T[0][1]
            u_ = (wx * v1[1] - v1[0] * wy) / den
            v_ = (v0[0] * wy - wx * v0[1]) / den
            m_ = (u_ >= -0.02) & (v_ >= -0.02) & (u_ + v_ <= 1.02)
            px[Y[m_], X[m_], :3] = 1.0
    im.pixels.foreach_set(px.ravel())
    im.filepath_raw = os.path.join(OUT, "hidden_face_map.png")
    im.file_format = "PNG"
    im.save()
    for o in dst.objects:
        if o is not None and o.users == 0:
            bpy.data.objects.remove(o)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_skinned.blend"))
json.dump(log, open(os.path.join(OUT, "skin.json"), "w"), indent=1)
say("done", json.dumps({k: v["tris"] for k, v in log["levels"].items()}), log.get("hidden"))
