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
    def hull_ring(zz, cen=None):
        """The torso's outline at height zz as a tape takes it (its hull), as radii by angle about `cen`."""
        loops = tailor.section_loops(body, Vector((0, 0, zz)), Vector((0, 0, 1)))
        torso = max(loops, key=lambda l_: len(l_) - 1000 * abs(float(np.mean(l_[:, 0]))))
        hull = np.array(tailor._hull2(torso[:, :2]))
        cen = hull.mean(axis=0) if cen is None else cen
        out = []
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
            out.append((a_, best))
        return out, cen

    ring, cen = hull_ring(z_belt)
    # its lower and upper edges laid on the outline at their own heights too (on the one at its middle, the top of
    # his seat, and the jeans' band over it, came through its lower edge at the back)
    ring_lo, _c = hull_ring(z_belt - 0.019, cen)
    ring_hi, _c = hull_ring(z_belt + 0.019, cen)
    ring = [(a_, max(r_, ring_lo[i_][1], ring_hi[i_][1])) for i_, (a_, r_) in enumerate(ring)]
    # a jeans belt 38 by 3.5 mm (at 35 it read as a dress belt), set on the jeans' waistband: 3 mm of denim and
    # 1.5 mm clear of it (BELT-2026-09-30.md)
    BELT_H, BELT_T, JEANS = 0.038, 0.0035, 0.0045
    RA = np.array([a_ for a_, _r in ring])
    RR = np.array([r_ for _a, r_ in ring])

    def belt_r(a_):
        return float(np.interp(a_, np.concatenate([RA - 2 * math.pi, RA, RA + 2 * math.pi]), np.concatenate([RR, RR, RR])))

    def belt_pt(a_, r_extra, z_):
        r0 = belt_r(a_)
        return Vector((cen[0] + math.cos(a_) * (r0 + r_extra), cen[1] + math.sin(a_) * (r0 + r_extra), z_))

    def ring_strip(bm_, a0, a1, r_in, r_out, zhalf, mat, n=16):
        """A closed strip along the belt's own curve between two angles: rectangular in section, its half-height
        zhalf(t) along it (t from 0 to 1)."""
        secs = []
        for i_ in range(n + 1):
            t = i_ / n
            a_ = a0 + (a1 - a0) * t
            zh = zhalf(t)
            secs.append([bm_.verts.new(belt_pt(a_, r_, z_belt + zz)) for r_, zz in
                         ((r_in, -zh), (r_out, -zh), (r_out, zh), (r_in, zh))])
        for i_ in range(n):
            for j_ in range(4):
                j2 = (j_ + 1) % 4
                f_ = bm_.faces.new((secs[i_][j_], secs[i_][j2], secs[i_ + 1][j2], secs[i_ + 1][j_]))
                f_.material_index = mat
        for sec, rev in ((secs[0], True), (secs[-1], False)):
            f_ = bm_.faces.new(sec[::-1] if rev else sec)
            f_.material_index = mat

    bb = bmesh.new()
    rows = []
    for r_extra, z_ in ((JEANS + 0.002, z_belt - BELT_H / 2), (JEANS + BELT_T + 0.002, z_belt - BELT_H / 2),
                        (JEANS + BELT_T, z_belt + BELT_H / 2), (JEANS, z_belt + BELT_H / 2)):   # a cone, the foot out
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
    # (a bare frame read as a strap slider; then a flat box for the end lifted off the belt like a board): a heavier
    # frame 50 by 48 mm with 6 mm bars, the prong through a hole, and the belt's end as a strip along the belt's own
    # curve 95 mm to the wearer's left, its tip pointed, under a keeper loop
    # (the third reviewer: the prong lies across the frame from the keeper's side to rest on the far bar, the end's
    # leather showing through the frame under it; heavier bars)
    for sz, off, mt in (((0.050, 0.005, 0.006), (0, -0.0035, 0.021), 1), ((0.050, 0.005, 0.006), (0, -0.0035, -0.021), 1),
                        ((0.006, 0.005, 0.048), (-0.022, -0.0035, 0), 1), ((0.006, 0.005, 0.048), (0.022, -0.0035, 0), 1),
                        ((0.042, 0.003, 0.004), (0.0, -0.0072, 0), 1)):
        box(bb, sz, tuple(front + Vector(off)), bevel=0.0012, segs=1, mat=mt)
    r_f = belt_r(a_f)
    a_end0, a_end1 = a_f - 0.016 / r_f, a_f + 0.175 / r_f
    ring_strip(bb, a_end0, a_end1, JEANS + BELT_T + 0.0003, JEANS + BELT_T + 0.0033,
               lambda t: 0.0175 if t < 0.92 else 0.0175 - (0.0175 - 0.006) * (t - 0.92) / 0.08, 0)
    a_k = a_f + 0.043 / r_f
    ring_strip(bb, a_k - 0.008 / r_f, a_k + 0.008 / r_f, JEANS - 0.0006, JEANS + BELT_T + 0.0045, lambda t: 0.0205, 0, n=2)
    bme = bpy.data.meshes.new("darren_belt")
    bb.to_mesh(bme)
    bb.free()
    bme.materials.append(tailor.material("M_Belt", (0.028, 0.02, 0.014), 0.55))
    bme.materials.append(tailor.material("M_Buckle", (0.55, 0.52, 0.45), 0.3))
    belt = bpy.data.objects.new("darren_belt", bme)
    bpy.context.collection.objects.link(belt)
    pieces.append((belt, "SKIN", "darren_belt"))
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
    box(bm, (0.042, 0.0016, 0.020), (0, body_y + T / 2 + 0.0004, top - 0.017), bevel=0.0009, segs=1, mat=0)
    box(bm, (0.034, 0.0016, 0.012), (0, body_y + T / 2 + 0.0002, top - 0.017), bevel=0.0005, segs=1, mat=1)
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
    for mname, rgb, rough in (("M_Case", (0.018, 0.018, 0.018), 0.7), ("M_Screen", (0.10, 0.12, 0.085), 0.25),
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
    pieces.append((piece, ("FOLLOW", belt), NAME))
elif KIND == "handbag":
    # ---- Sheila's "brown leather handbag": a structured frame bag about 27 by 19 by 8 cm with a gold-coloured
    # clasp (the V&A's handbag of about 1990, the note's source 7), two short handles meeting in her right hand.
    # Placed with her arms down (the idle) and her fingers curled round the handles, then carried back to her
    # reference pose on the hand, to which it is skinned wholly; in the game her hand takes a holding pose -------
    tailor.make_pose(arm, "down")
    J = lambda n: arm.matrix_world @ arm.pose.bones[n].head
    across0 = (J("index_metacarpal_r") - J("pinky_metacarpal_r")).normalized()
    along0 = (J("middle_01_r") - J("hand_r")).normalized()
    palm = along0.cross(across0).normalized()
    if palm.x < 0:                                          # her right hand's palm faces her thigh (+x)
        palm = -palm
    for f in ("index", "middle", "ring", "pinky"):
        for seg, deg in (("_01_r", 65.0), ("_02_r", 80.0), ("_03_r", 45.0)):
            bone = f + seg
            if bone not in arm.pose.bones:
                continue
            child = f + {"_01_r": "_02_r", "_02_r": "_03_r"}.get(seg, "")
            if child in arm.pose.bones and child != f:
                tailor.turn(arm, bone, across0, deg, child, palm)
    bpy.context.view_layer.update()
    grip = 0.5 * (J("middle_01_r") + J("middle_02_r")) + palm * 0.012
    A = Vector((across0.x, across0.y, 0.0)).normalized()     # the handles run across her palm
    Zv = Vector((0, 0, 1))
    Dp = Zv.cross(A).normalized()
    if Dp.dot(palm) > 0:
        Dp = -Dp                                            # the front face (the clasp's) away from her thigh
    W, Dd, Hh, HANDLE = 0.27, 0.08, 0.19, 0.115                # handles 11.5 cm (at 9 her knuckles sat on the frame)
    bm = bmesh.new()
    box(bm, (W, Dd, Hh), (0, 0, -HANDLE - Hh / 2), bevel=0.016, segs=3, mat=0)
    for v in bm.verts:                                      # the top narrower than the base, as a frame bag
        f_ = max(0.0, min(1.0, (v.co.z + HANDLE + Hh) / Hh))
        v.co.y *= 1.0 - 0.35 * f_ ** 2
        v.co.x *= 1.0 - 0.06 * f_
    box(bm, (W * 0.93, 0.012, 0.010), (0, 0, -HANDLE + 0.002), bevel=0.003, segs=2, mat=1)        # the frame
    box(bm, (0.032, 0.006, 0.024), (0, (Dd * 0.66) / 2 + 0.004, -HANDLE - 0.016), bevel=0.002, segs=1, mat=1)  # clasp, outer face
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(NAME)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(tailor.material("M_Leather", (0.16, 0.075, 0.032), 0.5))      # chestnut, as her shoes
    me.materials.append(tailor.material("M_Gilt", (0.72, 0.56, 0.28), 0.3))
    bag = bpy.data.objects.new(NAME, me)
    bpy.context.collection.objects.link(bag)
    # the two handles: arcs from the top's front and back up to meet in her grip
    parts = [bag]
    for side in (-1.0, 1.0):
        cu = bpy.data.curves.new("handle", "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth, cu.bevel_resolution = 0.0045, 2
        sp = cu.splines.new("POLY")
        pts = []
        for t in np.linspace(0.0, 1.0, 13):
            ang = math.pi * t
            pts.append((-0.065 * math.cos(ang), side * 0.018 * math.sin(ang) * 0.3 + side * 0.012 * (1 - math.sin(ang)),
                        -HANDLE + 0.004 + (HANDLE - 0.004) * math.sin(ang)))
        sp.points.add(len(pts) - 1)
        for i_, q in enumerate(pts):
            sp.points[i_].co = (q[0], q[1], q[2], 1.0)
        ho = bpy.data.objects.new("handle", cu)
        bpy.context.collection.objects.link(ho)
        cu.materials.append(me.materials[0])
        parts.append(ho)
    for o in parts[1:]:
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.convert(target="MESH")
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = bag
    bpy.ops.object.join()
    piece = bpy.context.active_object
    rot = Matrix((A, Dp, Zv)).transposed()
    if rot.determinant() < 0:
        rot = Matrix((-A, Dp, Zv)).transposed()
    piece.matrix_world = Matrix.Translation(grip) @ rot.to_4x4()
    bpy.context.view_layer.update()
    POSED_HAND = arm.matrix_world @ arm.pose.bones["hand_r"].matrix
    REST_HAND = arm.matrix_world @ arm.data.bones["hand_r"].matrix_local
    pieces.append((piece, "hand_r", NAME))
elif KIND == "spectacles":
    # ---- Sheila's "large square tinted spectacles on a thin gold chain" (the note: a rigid piece on the head, 1 to
    # 2 mm clear of the nose; the chain a thin strip round the back of the neck, weighted head to neck; lenses a
    # light brown tint, darker at the top). Fitted to her own head: the frame 12 mm in front of her eyes, its bridge
    # on her nose, the arms along her head to her ears ----------------------------------------------------------
    hv = co[co[:, 2] > meas["hps"] + 0.03]
    mid_ = hv[np.abs(hv[:, 0]) < 0.004]
    nose_tip = mid_[np.argmin(mid_[:, 1])]
    prof = []
    for zz in np.arange(nose_tip[2], nose_tip[2] + 0.07, 0.002):
        sl = mid_[np.abs(mid_[:, 2] - zz) < 0.0015]
        if len(sl):
            prof.append((float(zz), float(sl[:, 1].min())))
    prof = np.array(prof)
    rng = (prof[:, 0] > nose_tip[2] + 0.015) & (prof[:, 0] < nose_tip[2] + 0.06)
    nasion = prof[rng][np.argmax(prof[rng][:, 1])]
    # the eyes' height: 20 mm below the deepest point of the nose's bridge (at 8 mm the first fit sat 10 to 15 mm
    # too high, to its reviewer; the eye sockets' deepest point, tried next, was the hollow under the eye)
    eye_z = float(nasion[0]) - opt("--eye-drop", 0.024)          # 4 mm lower still, to the second reviewer
    log["nasionZ"] = round(float(nasion[0]), 4)
    ys = []
    for sx in (-1.0, 1.0):
        h_ = BVH.ray_cast(Vector((sx * 0.032, nose_tip[1] - 0.2, eye_z)), Vector((0, 1, 0)), 0.4)[0]
        ys.append(h_.y if h_ is not None else nasion[1])
    y_eye = min(ys)
    y_nose_b = float(np.interp(eye_z - 0.006, prof[:, 0], prof[:, 1]))
    FW, FH, FWB, BR, RIM, RD = 0.0535, 0.050, 0.0495, 0.018, 0.005, 0.004     # 5 mm narrower overall (review 2)
    y_f = min(y_eye - 0.012, y_nose_b - 0.002 - RD / 2)
    zc = eye_z + 0.002                                  # the pupils a little above the lens's middle
    log.update({"eyeZ": round(eye_z, 4), "frameY": round(y_f, 4), "noseBridgeY": round(y_nose_b, 4)})

    def outline(n=48):
        """The lens's outline, a large rounded square narrowing a little to its foot, about its centre (x, z)."""
        pts = []
        r_ = 0.012
        for k in range(n):
            t = 2 * math.pi * k / n
            cx, cz = math.cos(t), math.sin(t)
            # a superellipse square, then its lower half narrowed
            ex = FW / 2 * math.copysign(abs(cx) ** (2 / 4.0), cx)
            ez = FH / 2 * math.copysign(abs(cz) ** (2 / 4.0), cz)
            if ez < 0:
                ex *= 1.0 - (FW - FWB) / FW * (-ez / (FH / 2))
            pts.append((ex, ez))
        return pts

    bm = bmesh.new()
    lens_faces = []
    for sx in (-1.0, 1.0):
        cxl = sx * (BR / 2 + FW / 2)
        ol = outline()
        inner, outer = [], []
        for ex, ez in ol:
            d_ = Vector((ex, 0, ez))
            n_ = d_.normalized() if d_.length > 1e-9 else Vector((1, 0, 0))
            inner.append([bm.verts.new((cxl + ex, y_ - 0.0, zc + ez)) for y_ in (-RD / 2, RD / 2)])
            outer.append([bm.verts.new((cxl + ex + n_.x * RIM, y_, zc + ez + n_.z * RIM)) for y_ in (-RD / 2, RD / 2)])
        n = len(ol)
        for k in range(n):
            k2 = (k + 1) % n
            bm.faces.new((inner[k][0], inner[k2][0], outer[k2][0], outer[k][0])).material_index = 0   # front
            bm.faces.new((outer[k][1], outer[k2][1], inner[k2][1], inner[k][1])).material_index = 0   # back
            bm.faces.new((outer[k][0], outer[k2][0], outer[k2][1], outer[k][1])).material_index = 0   # outside
            bm.faces.new((inner[k][1], inner[k2][1], inner[k2][0], inner[k][0])).material_index = 0   # inside
        lv = [bm.verts.new((cxl + ex, 0.0, zc + ez)) for ex, ez in ol]
        f_ = bm.faces.new(lv)
        lens_faces.append(f_)
        # the end piece: a small block at the outer top corner, back towards the hinge
        box(bm, (0.006, 0.010, 0.008), (sx * (BR / 2 + FW + RIM - 0.001), RD / 2 + 0.004, zc + FH / 6), bevel=0.001,
            segs=1, mat=0)
    # the bridge: moulded, across at the lenses' upper third, resting on her nose (a thin rod along the very top
    # read as modern)
    box(bm, (BR + 0.008, RD + 0.0015, 0.011), (0, 0.0004, zc + FH / 2 - 0.017), bevel=0.003, segs=3, mat=0)
    # the lenses split at their upper third, the top a darker tint
    res = bmesh.ops.triangulate(bm, faces=lens_faces)
    lens_tris = res["faces"]
    for f_ in lens_tris:
        f_.material_index = 1
    bmesh.ops.bisect_plane(bm, geom=list({v for f_ in lens_tris for v in f_.verts}) + list({e for f_ in lens_tris for e in f_.edges}) + lens_tris,
                           plane_co=Vector((0, 0, zc + FH / 6)), plane_no=Vector((0, 0, 1)))
    for f_ in bm.faces:
        if f_.material_index == 1 and f_.calc_center_median().z > zc + FH / 6:
            f_.material_index = 2
    bmesh.ops.recalc_face_normals(bm, faces=[f_ for f_ in bm.faces if f_.material_index == 0])
    # face-form and tilt: each half turned 5 degrees about its inner edge, the whole tilted 8 degrees, foot in
    for v in bm.verts:
        sx = 1.0 if v.co.x > 0 else -1.0
        ax = abs(v.co.x) - BR / 2
        if ax > 0:
            a5 = math.radians(5.0)
            v.co.y += ax * math.sin(a5)
            v.co.x = sx * (BR / 2 + ax * math.cos(a5))
        dz = v.co.z - zc
        a8 = math.radians(8.0)
        v.co.y, v.co.z = v.co.y - dz * math.sin(a8), zc + dz * math.cos(a8)
    bmesh.ops.translate(bm, vec=Vector((0, y_f, 0)), verts=bm.verts[:])
    me = bpy.data.meshes.new(NAME)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(tailor.material("M_Frame", (0.12, 0.06, 0.03), 0.35))
    lens_m = tailor.material("M_Lens", (0.55, 0.40, 0.25), 0.1)
    lens_top = tailor.material("M_LensTop", (0.38, 0.25, 0.14), 0.1)
    for lm, a_ in ((lens_m, 0.35), (lens_top, 0.6)):
        lm.diffuse_color = (lm.diffuse_color[0], lm.diffuse_color[1], lm.diffuse_color[2], a_)
        lm.blend_method = "BLEND"
    me.materials.append(lens_m)
    me.materials.append(lens_top)
    frame = bpy.data.objects.new(NAME, me)
    bpy.context.collection.objects.link(frame)
    # the arms: from each end piece back along her head, 3 mm off it, to the top of her ear, then down behind it
    hinge_z = zc + FH / 6                               # the hinges a third of the way down, as the period's frames
    parts = [frame]
    tips = []
    for sx in (-1.0, 1.0):
        x0 = sx * (BR / 2 + FW + RIM) * math.cos(math.radians(5.0))
        y0 = y_f + RD / 2 + 0.009 + (FW + RIM) * math.sin(math.radians(5.0))
        pts = [(x0, y0, hinge_z)]
        ear_z = eye_z + opt("--ear-up", 0.006)           # where the ear's rim joins the head (6 mm lower, it cut the rim)
        y_ear = y0 + opt("--ear-back", 0.092)

        def side_at(yy, zz):
            """The head's side: from outside in front of the ear (from inside, in front of the face, the ray met
            nothing and the arm went through her cheekbone), from inside at the ear (its rim is not the head)."""
            if yy < y_ear - 0.012:
                h_ = BVH.ray_cast(Vector((sx * 0.25, yy, zz)), Vector((-sx, 0.0, 0.0)), 0.3)[0]
            else:
                h_ = BVH.ray_cast(Vector((0.0, yy, zz)), Vector((sx, 0.0, 0.0)), 0.2)[0]
            return abs(h_.x) if h_ is not None else abs(x0)

        n_s = 14
        for k in range(1, n_s + 1):
            t = k / n_s
            yy = y0 + (y_ear - y0) * t
            zz = hinge_z + (ear_z - hinge_z) * (t ** 1.3)
            xx = max(abs(x0), side_at(yy, zz) + 0.003) if t < 0.5 else side_at(yy, zz) + 0.003
            pts.append((sx * xx, float(yy), float(zz)))
        # over the ear's root and down behind it, following the head
        last = pts[-1]
        for k in range(1, 7):
            t = k / 6.0
            yy = last[1] + 0.018 * math.sin(t * math.pi / 2)
            zz = last[2] - 0.018 * (1 - math.cos(t * math.pi / 2)) - 0.002 * t
            pts.append((sx * (side_at(yy, zz) + 0.0025), float(yy), float(zz)))
        tips.append(Vector(pts[-1]))
        cu = bpy.data.curves.new("temple", "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth, cu.bevel_resolution = 0.0019, 1
        sp = cu.splines.new("POLY")
        sp.points.add(len(pts) - 1)
        for i_, q in enumerate(pts):
            sp.points[i_].co = (q[0], q[1], q[2], 1.0)
        to = bpy.data.objects.new("temple", cu)
        bpy.context.collection.objects.link(to)
        cu.materials.append(me.materials[0])
        parts.append(to)
    for o in parts[1:]:
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.convert(target="MESH")
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = frame
    bpy.ops.object.join()
    piece = bpy.context.active_object
    # ---- the chain: from each arm's tip down round the back of her neck, 2 mm off it, lowest at her nape -------
    z_low = meas["hps"] + 0.012
    cpts = []
    for k in range(41):
        t = k / 40.0                                     # 0 at her left tip, 1 at her right
        zz = z_low + (0.5 * (tips[0].z + tips[1].z) - z_low) * (2 * t - 1) ** 2
        sl = co[(np.abs(co[:, 2] - zz) < 0.004) & (np.abs(co[:, 0]) < 0.09)]
        half = float(np.abs(sl[:, 0]).max()) if len(sl) else 0.06
        tip_x = tips[0].x * (1 - t) + tips[1].x * t
        xx = math.copysign(min(abs(tip_x), 0.8 * half), tip_x) if abs(2 * t - 1) < 0.999 else tip_x
        h_ = BVH.ray_cast(Vector((xx, 0.4, zz)), Vector((0, -1, 0)), 0.8)[0]
        yy = (h_.y + 0.002) if h_ is not None else float(sl[:, 1].max()) + 0.002
        cpts.append(Vector((xx, yy, zz)))
    for _ in range(4):                                   # eased along its length (from point to point it zigzagged)
        cpts = [cpts[0]] + [(cpts[i_ - 1] + cpts[i_] * 2 + cpts[i_ + 1]) / 4 for i_ in range(1, len(cpts) - 1)] + [cpts[-1]]
    for i_ in range(1, len(cpts) - 1):
        hit, nn, _f, _d = BVH.find_nearest(cpts[i_])
        if hit is not None and (cpts[i_] - hit).dot(nn) < 0.002:
            cpts[i_] = hit + nn * 0.002
    cpts[0], cpts[-1] = tips[0] + Vector((0, 0.001, 0.0)), tips[1] + Vector((0, 0.001, 0.0))   # at the tips (2 mm forward, it came through the ear)
    cu = bpy.data.curves.new("chain", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth, cu.bevel_resolution = 0.0010, 1     # 2 mm (at 1.4 it would flicker away at game distance)
    sp = cu.splines.new("POLY")
    sp.points.add(len(cpts) - 1)
    for i_, q in enumerate(cpts):
        sp.points[i_].co = (q.x, q.y, q.z, 1.0)
    ch = bpy.data.objects.new("sheila_glasses_chain", cu)
    bpy.context.collection.objects.link(ch)
    cu.materials.append(tailor.material("M_Gilt", (0.72, 0.56, 0.28), 0.3))
    bpy.ops.object.select_all(action="DESELECT")
    ch.select_set(True)
    bpy.context.view_layer.objects.active = ch
    bpy.ops.object.convert(target="MESH")
    ch = bpy.context.active_object
    pieces.append((piece, "head", NAME))
    pieces.append((ch, "SKIN", "sheila_glasses_chain"))
    log["chainLowZ"] = round(z_low, 3)
else:
    raise SystemExit("unknown kind " + KIND)

BODY_GROUPS = [g_.name for g_ in body.vertex_groups]


def body_weights_at(p):
    """The body's skin weights at the nearest place on it: its face's corners, nearer ones counting more."""
    hit, _n, fi, _d = BVH.find_nearest(p)
    w = {}
    if hit is None:
        return w
    poly = body.data.polygons[fi]
    tot = 0.0
    for vi in poly.vertices:
        v = body.data.vertices[vi]
        k = 1.0 / max(1e-4, ((body.matrix_world @ v.co) - hit).length)
        tot += k
        for g_ in v.groups:
            w[BODY_GROUPS[g_.group]] = w.get(BODY_GROUPS[g_.group], 0.0) + g_.weight * k
    return {n: x / tot for n, x in w.items()}


def write_weights(obj, per_vert):
    for vi, w in per_vert.items():
        top = sorted(w.items(), key=lambda kv: -kv[1])[:4]
        tot = sum(x for _n, x in top) or 1.0
        for n, x in top:
            if x / tot < 0.01:
                continue
            g_ = obj.vertex_groups.get(n) or obj.vertex_groups.new(name=n)
            g_.add([vi], x / tot, "REPLACE")


def skin_weights(obj):
    """A strap's weights from the skin under it (fixed to the pelvis alone, the hip came through it walking),
    eased along it; the buckle's pieces held together at their middle's."""
    me_ = obj.data
    per = {v.index: body_weights_at(obj.matrix_world @ v.co) for v in me_.vertices}
    nbr = {v.index: [] for v in me_.vertices}
    for e in me_.edges:
        a, b = e.vertices
        nbr[a].append(b)
        nbr[b].append(a)
    for _ in range(3):
        new = {}
        for vi, w in per.items():
            acc = dict((n, x * 0.5) for n, x in w.items())
            for nb in nbr[vi]:
                for n, x in per[nb].items():
                    acc[n] = acc.get(n, 0.0) + x * 0.5 / max(1, len(nbr[vi]))
            new[vi] = acc
        per = new
    for vi, w in per.items():                         # two bones: the spine's share to spine_01, the rest the pelvis
        sp_ = sum(x for n, x in w.items() if n.startswith("spine"))
        tot = sum(w.values()) or 1.0
        per[vi] = {"pelvis": (tot - sp_) / tot, "spine_01": sp_ / tot}
    xy = np.array([tuple((obj.matrix_world @ v.co).xy) for v in me_.vertices])
    col = {}
    for vi in per:                                    # the same across the width: each column's mean
        near = np.where(np.sum((xy - xy[vi]) ** 2, axis=1) < 0.008 ** 2)[0]
        col[vi] = {n: float(np.mean([per[int(j)].get(n, 0.0) for j in near])) for n in ("pelvis", "spine_01")}
    per = col
    # the main strap: the largest connected piece; the others (the belt's end, the keeper, the buckle) take the
    # strap's own weights at its nearest point (weighted from the skin, the end lifted off it like a board)
    seen, islands = set(), []
    for v0 in range(len(me_.vertices)):
        if v0 in seen:
            continue
        stack, isl = [v0], []
        seen.add(v0)
        while stack:
            a_ = stack.pop()
            isl.append(a_)
            for b_ in nbr[a_]:
                if b_ not in seen:
                    seen.add(b_)
                    stack.append(b_)
        islands.append(isl)
    main = max(islands, key=len)
    mco = np.array([tuple(obj.matrix_world @ me_.vertices[i_].co) for i_ in main])
    for isl in islands:
        if isl is main:
            continue
        for vi in isl:
            q = np.array(tuple(obj.matrix_world @ me_.vertices[vi].co))
            per[vi] = per[main[int(np.argmin(np.sum((mco - q) ** 2, axis=1)))]]
    metal = {vi for f in me_.polygons if f.material_index == 1 for vi in f.vertices}
    if metal:
        avg = {}
        for vi in metal:
            for n, x in per[vi].items():
                avg[n] = avg.get(n, 0.0) + x / len(metal)
        for vi in metal:
            per[vi] = avg
    write_weights(obj, per)


def follow_weights(obj, host):
    """A piece clipped on another: every point of it takes the host's weights where it clips on, averaged."""
    c = sum((obj.matrix_world @ v.co for v in obj.data.vertices), Vector()) / len(obj.data.vertices)
    names = [g_.name for g_ in host.vertex_groups]
    near = [v for v in host.data.vertices if ((host.matrix_world @ v.co) - c).length < 0.05]
    avg = {}
    for v in near:
        for g_ in v.groups:
            avg[names[g_.group]] = avg.get(names[g_.group], 0.0) + g_.weight / len(near)
    write_weights(obj, {v.index: avg for v in obj.data.vertices})


log["pieces"] = {}
if KIND == "handbag":
    POSED_MW = pieces[0][0].matrix_world.copy()
    pieces[0][0].matrix_world = REST_HAND @ POSED_HAND.inverted() @ POSED_MW
for piece_, bone_, fname in pieces:
    bpy.context.view_layer.update()
    bpy.ops.object.select_all(action="DESELECT")
    piece_.select_set(True)
    bpy.context.view_layer.objects.active = piece_
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(40))
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if bone_ == "SKIN":
        skin_weights(piece_)
    elif isinstance(bone_, tuple):
        follow_weights(piece_, bone_[1])
    else:
        g = piece_.vertex_groups.new(name=bone_)
        g.add(list(range(len(piece_.data.vertices))), 1.0, "REPLACE")
    log["pieces"][fname] = {"tris": sum(len(p_.vertices) - 2 for p_ in piece_.data.polygons),
                            "bones": sorted({piece_.vertex_groups[g_.group].name for v in piece_.data.vertices for g_ in v.groups})}
# ---- pictures: close at the piece and the whole figure (a handbag seen in her hand, arms down) ----------------
if KIND == "handbag":
    mdf = pieces[0][0].modifiers.new("Armature", "ARMATURE")
    mdf.object = arm
    bpy.context.view_layer.update()
body.data.materials.clear()
body.data.materials.append(tailor.material("M_Body", (0.55, 0.55, 0.56)))
_ev = pieces[-1][0].evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh()
c_ = sum((pieces[-1][0].matrix_world @ v.co for v in _ev.vertices), Vector()) / len(_ev.vertices)
pieces[-1][0].evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh_clear()
CLOSE = {"pager": 0.45, "handbag": 0.9, "spectacles": 0.34}[KIND]
VIEWS = (("front", (0.0, -CLOSE, 0.05)), ("side", (-CLOSE, 0.0, 0.03)),
         ("three-quarter", (-0.71 * CLOSE, -0.71 * CLOSE, 0.27 * CLOSE)))
if KIND == "spectacles":
    c_ = sum((pieces[0][0].matrix_world @ v.co for v in pieces[0][0].data.vertices), Vector()) / len(pieces[0][0].data.vertices)
    c_ = c_ + Vector((0, 0.04, -0.03))
    VIEWS = VIEWS + (("back", (0.15, CLOSE * 1.2, 0.02)),)
tailor.pictures(os.path.join(OUT, "close"), c_, views=VIEWS, res=(700, 500))
tailor.pictures(os.path.join(OUT, "whole"), Vector((0, 0, meas["hips"])), views=(("front", (0.0, -3.0, 0.1)),
                                                                                  ("three-quarter", (-2.1, -2.1, 0.3))),
                res=(500, 900))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
# ---- the export: each piece on the skeleton in the reference pose, skinned wholly to its bone -----------------
bpy.data.objects.remove(body, do_unlink=True)
for pb in arm.pose.bones:
    pb.matrix_basis.identity()
for piece_, bone_, fname in pieces:
    for old in list(piece_.modifiers):
        piece_.modifiers.remove(old)
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
