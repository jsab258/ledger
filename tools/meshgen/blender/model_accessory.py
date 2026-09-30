"""Small worn pieces modelled in place on the wearer's own body and skinned wholly to one bone, for a MetaHuman.

    blender -b -P tools/meshgen/blender/model_accessory.py -- BODY_FullBody.fbx OUT_DIR --kind pager [--name darren_pager]

WHY, 30 September (the clothing session, CLOTHES.md item 6: Darren's "black
pager on his belt"; the research, production/research/clothing-pipeline/
ACCESSORIES-2026-09-30.md). A pager of 1990 (the Science Museum's BT and
Motorola pagers): black matt plastic about 80 by 50 by 25 mm, a small
numeric screen, a spring clip on the back. It is worn on the belt at the
right front hip, so it is placed there on his own body, its clip behind the
belt 3 mm off the skin for the jeans, the case in front of the belt, upright, and skinned wholly to the pelvis: the builder
imports it on his skeleton like the boots, with no socket to set (the note's
socket on the pelvis comes to the same thing). He needs a belt, which comes
with his jeans.

OUT_DIR gets NAME_skinned.fbx (the piece on his skeleton, reference pose), NAME.blend and pictures.
"""
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
BODY, OUT = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


KIND = opt("--kind", "pager", str)
NAME = opt("--name", KIND, str)
log = {"body": BODY, "kind": KIND}
arm, body = tailor.load_body(BODY, lod=1)
BVH = tailor.bvh_of(body)
co = np.array([body.matrix_world @ v.co for v in body.data.vertices])
meas = json.load(open(os.path.join(os.path.dirname(BODY), "measurements.json")))["heights_m"]


def box(bm, size, centre=(0, 0, 0), bevel=0.0, segs=2, mat=0):
    """A bevelled box into bm (local coordinates)."""
    geom = bmesh.ops.create_cube(bm, size=1.0)
    vs = geom["verts"]
    bmesh.ops.scale(bm, vec=Vector(size), verts=vs)
    bmesh.ops.translate(bm, vec=Vector(centre), verts=vs)
    faces = list({f for v in vs for f in v.link_faces})
    for f in faces:
        f.material_index = mat                           # set first: the bevel's new faces take their neighbours'
    if bevel > 0:
        edges = list({e for f in faces for e in f.edges})
        bmesh.ops.bevel(bm, geom=edges, offset=bevel, segments=segs, affect="EDGES", profile=0.5)


pieces = []                                                 # (object, bone, file name)
if KIND == "pager":
    # ---- the belt he needs for it (the note: "Darren needs a belt"): a plain dark leather strap 35 mm deep and
    # 4 mm thick round the torso's own hull at the belt line, 3 mm out for the jeans, a square buckle in front ------
    z_belt = meas["hips"] + 0.6 * (meas["waist"] - meas["hips"])
    loops = tailor.section_loops(body, Vector((0, 0, z_belt)), Vector((0, 0, 1)))
    torso = max(loops, key=lambda l_: len(l_) - 1000 * abs(float(np.mean(l_[:, 0]))))
    hull = np.array(tailor._hull2(torso[:, :2]))
    cen = hull.mean(axis=0)
    ang = np.arctan2(hull[:, 1] - cen[1], hull[:, 0] - cen[0])
    ring = []
    for a_ in np.linspace(-math.pi, math.pi, 72, endpoint=False):
        d_ = np.array([math.cos(a_), math.sin(a_)])
        best = 0.0
        for i_ in range(len(hull)):
            q0, q1 = hull[i_], hull[(i_ + 1) % len(hull)]
            ed = q1 - q0
            den = d_[0] * (-ed[1]) + d_[1] * ed[0]
            if abs(den) < 1e-12:
                continue
            w_ = q0 - cen
            t_ = (w_[0] * (-ed[1]) + w_[1] * ed[0]) / den
            u_ = (d_[0] * w_[1] - d_[1] * w_[0]) / den
            if t_ > 0 and -1e-9 <= u_ <= 1 + 1e-9:
                best = max(best, t_)
        ring.append((a_, best))
    BELT_H, BELT_T, JEANS = 0.035, 0.004, 0.003

    def belt_pt(a_, r_extra, z_):
        r0 = dict(ring)[a_] if a_ in dict(ring) else None
        return Vector((cen[0] + math.cos(a_) * (r0 + r_extra), cen[1] + math.sin(a_) * (r0 + r_extra), z_))

    bb = bmesh.new()
    rows = []
    for r_extra, z_ in ((JEANS, z_belt - BELT_H / 2), (JEANS + BELT_T, z_belt - BELT_H / 2),
                        (JEANS + BELT_T, z_belt + BELT_H / 2), (JEANS, z_belt + BELT_H / 2)):
        rows.append([bb.verts.new(belt_pt(a_, r_extra, z_)) for a_, _r in ring])
    n_ = len(ring)
    for j_ in range(4):
        A, B = rows[j_], rows[(j_ + 1) % 4]
        for i_ in range(n_):
            k_ = (i_ + 1) % n_
            bb.faces.new((A[i_], A[k_], B[k_], B[i_]))
    bmesh.ops.recalc_face_normals(bb, faces=bb.faces[:])
    # the buckle: a square frame 45 by 40 mm, 3 mm proud, on the front of the belt (the ring point facing -y)
    a_f = min((a_ for a_, _r in ring), key=lambda a_: abs(a_ + math.pi / 2))
    front = belt_pt(a_f, JEANS + BELT_T, z_belt)
    for sz, off in (((0.045, 0.004, 0.005), (0, -0.002, 0.0175)), ((0.045, 0.004, 0.005), (0, -0.002, -0.0175)),
                    ((0.005, 0.004, 0.040), (-0.020, -0.002, 0)), ((0.005, 0.004, 0.040), (0.020, -0.002, 0)),
                    ((0.003, 0.003, 0.034), (-0.004, -0.0035, 0))):
        box(bb, sz, tuple(front + Vector(off)), bevel=0.001, segs=1, mat=1)
    bme = bpy.data.meshes.new("darren_belt")
    bb.to_mesh(bme)
    bb.free()
    bme.materials.append(tailor.material("M_Belt", (0.028, 0.02, 0.014), 0.55))
    bme.materials.append(tailor.material("M_Buckle", (0.55, 0.52, 0.45), 0.3))
    belt = bpy.data.objects.new("darren_belt", bme)
    bpy.context.collection.objects.link(belt)
    pieces.append((belt, "pelvis", "darren_belt"))
    # ---- the pager's place: on the belt at the right front hip, 40 degrees round from the front; its clip behind
    # the belt, on the jeans ---------------------------------------------------------------------------------
    th = math.radians(opt("--round", 85.0))              # at the side (at the front hip the thigh met it seated)
    a_p = min((a_ for a_, _r in ring), key=lambda a_: abs(a_ - (-math.pi / 2 - th)))
    hit = belt_pt(a_p, 0.0, z_belt)
    nrm = Vector((math.cos(a_p), math.sin(a_p), 0.0))
    log["beltZ"] = round(z_belt, 3)
    # ---- the piece, in its own frame: x across, y outward from the body, z up; the clip's back at y = 0 --------
    W, T, H = 0.050, 0.022, opt("--height", 0.072)
    GAP, CLIP_T = 0.004, 0.0015
    bm = bmesh.new()
    body_y = CLIP_T + GAP + T / 2
    top = 0.018                                             # the case's top 18 mm above the belt's middle
    box(bm, (W, T, H), (0, body_y, top - H / 2), bevel=0.0045, segs=3, mat=0)
    # the screen: a dark window near the top of the face, set in 0.8 mm
    box(bm, (0.036, 0.0012, 0.013), (0, body_y + T / 2 - 0.0002, top - 0.017), bevel=0.0008, segs=1, mat=1)
    # two buttons on the top edge
    for x_ in (-0.011, 0.011):
        box(bm, (0.009, 0.007, 0.0025), (x_, body_y, top + 0.0008), bevel=0.001, segs=1, mat=0)
    # the clip: a plate down the back, joined at the top, the belt passing between
    box(bm, (0.030, CLIP_T, 0.050), (0, CLIP_T / 2, top - 0.006 - 0.025), bevel=0.0012, segs=1, mat=2)
    box(bm, (0.030, GAP + CLIP_T, 0.006), (0, (GAP + CLIP_T) / 2, top - 0.003), bevel=0.0012, segs=1, mat=2)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(NAME)
    bm.to_mesh(me)
    bm.free()
    for mname, rgb, rough in (("M_Case", (0.018, 0.018, 0.018), 0.7), ("M_Screen", (0.05, 0.06, 0.045), 0.25),
                              ("M_Clip", (0.025, 0.025, 0.025), 0.5)):
        me.materials.append(tailor.material(mname, rgb, rough))
    piece = bpy.data.objects.new(NAME, me)
    bpy.context.collection.objects.link(piece)
    # tilted to the hip as a clip lies (upright, the hip's widening below the belt came through its foot): its back
    # kept 3 mm off the body 55 mm below the belt too
    low = BVH.ray_cast(hit + nrm * 0.3 + Vector((0, 0, -0.055)), -nrm, 0.6)[0]
    upv = Vector((0, 0, 1))
    if low is not None:
        lowp = low + nrm * JEANS
        topp = hit + nrm * JEANS
        d_ = (topp - lowp)
        if (lowp - topp).dot(nrm) > 0:                     # the hip stands out below: lean the piece out to it
            upv = d_.normalized()
    xa = nrm.cross(upv).normalized()                       # a right-handed frame (the first was a mirror)
    nrm2 = upv.cross(xa).normalized()
    rot = Matrix((xa, nrm2, upv)).transposed().to_4x4()
    piece.matrix_world = Matrix.Translation(hit + nrm * JEANS) @ rot
    pieces.append((piece, "pelvis", NAME))
else:
    raise SystemExit("unknown kind " + KIND)

log["pieces"] = {}
for piece_, bone_, fname in pieces:
    bpy.context.view_layer.update()
    bpy.ops.object.select_all(action="DESELECT")
    piece_.select_set(True)
    bpy.context.view_layer.objects.active = piece_
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(40))
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    g = piece_.vertex_groups.new(name=bone_)
    g.add(list(range(len(piece_.data.vertices))), 1.0, "REPLACE")
    log["pieces"][fname] = {"tris": sum(len(p_.vertices) - 2 for p_ in piece_.data.polygons), "bone": bone_}
# ---- pictures: close at the hip and the whole figure --------------------------------------------------------
body.data.materials.clear()
body.data.materials.append(tailor.material("M_Body", (0.55, 0.55, 0.56)))
c_ = sum((pieces[-1][0].matrix_world @ v.co for v in pieces[-1][0].data.vertices), Vector()) / len(pieces[-1][0].data.vertices)
tailor.pictures(os.path.join(OUT, "close"), c_, views=(("front", (0.0, -0.45, 0.05)), ("side", (-0.45, 0.0, 0.03)),
                                                        ("three-quarter", (-0.32, -0.32, 0.12))), res=(700, 500))
tailor.pictures(os.path.join(OUT, "whole"), Vector((0, 0, meas["hips"])), views=(("front", (0.0, -3.0, 0.1)),
                                                                                  ("three-quarter", (-2.1, -2.1, 0.3))),
                res=(500, 900))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
# ---- the export: each piece on the skeleton in the reference pose, skinned wholly to its bone -----------------
bpy.data.objects.remove(body, do_unlink=True)
for pb in arm.pose.bones:
    pb.matrix_basis.identity()
for piece_, bone_, fname in pieces:
    m = piece_.modifiers.new("Armature", "ARMATURE")
    m.object = arm
    mw = piece_.matrix_world.copy()
    piece_.parent = arm
    piece_.matrix_world = mw
for piece_, bone_, fname in pieces:
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    piece_.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, fname + "_skinned.fbx"), use_selection=True,
                             object_types={"ARMATURE", "MESH"}, add_leaf_bones=False, mesh_smooth_type="FACE",
                             bake_anim=False)
json.dump(log, open(os.path.join(OUT, "accessory.json"), "w"), indent=1)
print("ACCESSORY", json.dumps(log), flush=True)
