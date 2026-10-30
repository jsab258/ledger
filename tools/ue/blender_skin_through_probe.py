"""HOW MUCH OF A BODY'S SKIN COMES THROUGH THE GARMENTS ON IT, posed (30 October 2026, Tom's hidden faces).

    blender -b --factory-startup -P tools/ue/blender_skin_through_probe.py -- BODY.fbx OUT.json
        --garment jacket=JACKET.fbx --garment jeans=JEANS.fbx --garment boots=BOOTS.fbx
        [--garment jumper=JUMPER.fbx@Shown] [--depth-mm 1] [--reach-mm 30]

BODY.fbx is a body as the game draws it: a built MetaHuman body exported from Unreal (faces under the
clothes already cut, or not), or the whole body for comparison. Each garment FBX is its skinned game file
on the same skeleton; "@Mat1,Mat2" keeps only the faces of those material slots (the jumper draws only its
"Shown" neckband, LedgerGarments.h 137-152).

THE MEASURE. A body point can come through a garment only where that garment covers it at rest (a ray
out along its normal meets the garment within 10 cm, or one into the body within --reach-mm), so a hand
pressed into a thigh is not "skin through the jeans". Posed, it is through when a ray from it into the
body meets the garment within --reach-mm (garment_pose_check.py's test) and it stands more than --depth-mm
outside the garment's nearest surface, that surface's normal taken away from the body as at rest (so a
forearm reaching the sleeve's far side is not counted); a closed shell (the boots: leather and lining, no
open edge) is measured against its outside faces only, so toes inside the leather or the foot's cavity are
not counted. The depth
reported is that distance to the nearest surface. Only the body's points that exist are measured, so a
cut body has fewer to come through.

POSES from the bind pose (the garments' rest, arms about 53 degrees below level): rest; arms hanging (the
upper arms turned down about the body's forward axis by 30, 40 and 50 degrees, the elbows bent forward 10,
10 and 15; 30 leaves them about 83 degrees below level, a natural hang, and 40 and 50 carry them into the
hips, named as the elbow probe of 30 October named its poses, down40_elbow10 and down50_elbow15); a walking stride (thighs 28 forward and 18 back,
the back knee 35); sitting (thighs forward 90, knees 90).

REGIONS: elbows (points within 8 cm of either elbow joint), forearms (below the elbow, above the wrist),
crotch (within 12 cm of the point midway between the hip joints, 6 cm under it), feet (below 16 cm above
the floor), neck (above the shoulders' joints); per region and garment: points through, worst mm.
Also each garment's ten worst bones (the body point's heaviest bone): [points, worst mm].
"""
import json
import math
import sys
from collections import defaultdict

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
BODY, OUT = argv[:2]


def opt(n, d, f=float):
    return f(argv[argv.index(n) + 1]) if n in argv else d


GARMENTS = {}
for i, a in enumerate(argv):
    if a == "--garment":
        k, v = argv[i + 1].split("=", 1)
        path, _, mats = v.partition("@")
        GARMENTS[k] = (path, [m for m in mats.split(",") if m])
DEPTH = opt("--depth-mm", 1.0) / 1000.0
REACH = opt("--reach-mm", 30.0) / 1000.0


def import_fbx(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    return next((o for o in new if o.type == "ARMATURE"), None), [o for o in new if o.type == "MESH"]


bpy.ops.wm.read_factory_settings(use_empty=True)
arm, meshes = import_fbx(BODY)
body = max(meshes, key=lambda o: len(o.data.vertices))
for o in meshes:
    if o is not body:
        bpy.data.objects.remove(o, do_unlink=True)
groups = {g.index: g.name for g in body.vertex_groups}
dominant = []
for v in body.data.vertices:
    best = max(v.groups, key=lambda g: g.weight, default=None)
    dominant.append(groups[best.group] if best else "none")

gar = {}
for k, (path, mats) in GARMENTS.items():   # noqa: B007
    a2, ms = import_fbx(path)
    o = max(ms, key=lambda m: len(m.data.vertices))
    for m in ms:
        if m is not o:
            bpy.data.objects.remove(m, do_unlink=True)
    mw = o.matrix_world.copy()
    o.parent = None
    o.matrix_world = mw
    for md in o.modifiers:
        if md.type == "ARMATURE":
            md.object = arm
    if a2 is not None:
        bpy.data.objects.remove(a2, do_unlink=True)
    keep = None
    if mats:
        names = [m.name if m else "" for m in o.data.materials]
        keep = {i for i, n in enumerate(names) if any(n == w or n.startswith(w + ".") for w in mats)}
    # The triangles, fixed once: (point indices), kept material slots only
    tris = []
    for poly in o.data.polygons:
        if keep is not None and poly.material_index not in keep:
            continue
        vs = list(poly.vertices)
        for j in range(1, len(vs) - 1):
            tris.append((vs[0], vs[j], vs[j + 1]))
    gar[k] = {"obj": o, "keep": keep, "tris": tris}

pb = arm.pose.bones


def reset():
    for p in pb:
        p.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()


def head_world(b):
    return arm.matrix_world @ pb[b].head


def tail_world(b):
    bpy.context.view_layer.update()
    return arm.matrix_world @ pb[b].tail


def rotate_world(bone, axis, degrees):
    p = pb[bone]
    bpy.context.view_layer.update()
    hw = arm.matrix_world @ p.head
    R = Matrix.Translation(hw) @ Matrix.Rotation(math.radians(degrees), 4, axis) @ Matrix.Translation(-hw)
    p.matrix = arm.matrix_world.inverted() @ R @ arm.matrix_world @ p.matrix
    bpy.context.view_layer.update()


def turn_toward(bone, tip, direction, deg):
    bpy.context.view_layer.update()
    h = head_world(bone)
    t = head_world(tip)
    axis = (t - h).cross(direction)
    if axis.length < 1e-6:
        return
    rotate_world(bone, axis.normalized(), deg)


reset()
fwd = head_world("ball_l") - head_world("foot_l")
fwd.z = 0
fwd.normalize()


def arms_down(deg):
    for s in ("l", "r"):
        start = pb["upperarm_" + s].matrix_basis.copy()
        for trial in (deg, -deg):
            z0 = head_world("hand_" + s).z
            rotate_world("upperarm_" + s, fwd, trial)
            if head_world("hand_" + s).z < z0:
                break
            pb["upperarm_" + s].matrix_basis = start
            bpy.context.view_layer.update()


def pose(name):
    reset()
    if name.startswith("down"):
        d, e = name[4:].split("_elbow")
        arms_down(float(d))
        for s in ("l", "r"):
            turn_toward("lowerarm_" + s, "hand_" + s, fwd, float(e))
    elif name == "stride":
        turn_toward("thigh_l", "calf_l", fwd, 28)
        turn_toward("thigh_r", "calf_r", -fwd, 18)
        turn_toward("calf_r", "foot_r", -fwd, 35)
        arms_down(40)
    elif name == "sit":
        arms_down(40)
        for s in ("l", "r"):
            turn_toward("thigh_" + s, "calf_" + s, fwd, 90)
            turn_toward("calf_" + s, "foot_" + s, Vector((0, 0, -1)), 90)


def evaluated(o):
    dg = bpy.context.evaluated_depsgraph_get()
    e = o.evaluated_get(dg)
    m = e.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(m)
    bm.transform(o.matrix_world)
    e.to_mesh_clear()
    bm.normal_update()
    return bm


def garment_bvh(g):
    bm = evaluated(g["obj"])
    bm.verts.ensure_lookup_table()
    co = [v.co.copy() for v in bm.verts]
    bm.free()
    return BVHTree.FromPolygons(co, g["tris"]), co


def _edges(o):
    bm = bmesh.new()
    bm.from_mesh(o.data)
    out = [type("E", (), {"is_boundary": e.is_boundary})() for e in bm.edges]
    bm.free()
    return out


def tri_normal(co, t):
    return (co[t[1]] - co[t[0]]).cross(co[t[2]] - co[t[0]]).normalized()


# AT REST: each triangle's normal turned away from the body, and the body points each garment covers
reset()
rest_body = evaluated(body)
rest_bvh = BVHTree.FromBMesh(rest_body)
for k, g in gar.items():
    bvh, co = garment_bvh(g)
    # A CLOSED SHELL (a boot: leather with its lining, no open edge) is measured against its outside only:
    # the triangles whose normal's ray sees out past the shell (the lining's meets the shell across the foot).
    # Inside the leather or in the foot's cavity is unseen; only past the outside is through.
    closed = all(e.is_boundary is False for e in _edges(g["obj"]))
    if closed:
        outer = []
        for t in g["tris"]:
            c = (co[t[0]] + co[t[1]] + co[t[2]]) / 3
            nn = tri_normal(co, t)
            if bvh.ray_cast(c + nn * 1e-4, nn, 1.0)[0] is None:
                outer.append(t)
        g["tris"] = outer
        g["shell_outer_triangles"] = len(outer)
        bvh, co = garment_bvh(g)
        g["flip"] = [1.0] * len(outer)
    else:
        flip = []
        for t in g["tris"]:
            c = (co[t[0]] + co[t[1]] + co[t[2]]) / 3
            loc, _n, _i, _d = rest_bvh.find_nearest(c)
            flip.append(-1.0 if loc is not None and (c - loc).dot(tri_normal(co, t)) < 0 else 1.0)
        g["flip"] = flip
    cov = set()
    for v in rest_body.verts:
        if bvh.ray_cast(v.co + v.normal * 1e-5, v.normal, 0.10)[0] is not None or                 bvh.ray_cast(v.co + v.normal * 1e-5, -v.normal, REACH)[0] is not None:
            cov.add(v.index)
    g["covers"] = cov
rest_body.free()
report_shells = {k: g.get("shell_outer_triangles") for k, g in gar.items()}


REGIONS = ("elbows", "forearms", "crotch", "feet", "neck")


def regions_at(co):
    """The regions a posed body point is in, from the posed joints."""
    out = []
    for s in ("l", "r"):
        el = J["lowerarm_" + s]
        if (co - el).length < 0.08:
            out.append("elbows")
        wr = J["hand_" + s]
        seg = wr - el
        t = (co - el).dot(seg) / max(seg.length_squared, 1e-9)
        if 0.15 < t < 0.95 and (co - (el + seg * t)).length < 0.07:
            out.append("forearms")
    mid = (J["thigh_l"] + J["thigh_r"]) / 2 - Vector((0, 0, 0.06))
    if (co - mid).length < 0.12:
        out.append("crotch")
    if co.z < J["floor"] + 0.16 and min((co - J["foot_l"]).length, (co - J["foot_r"]).length) < 0.30:
        out.append("feet")
    if co.z > max(J["upperarm_l"].z, J["upperarm_r"].z) and abs(co.x) < 0.09:
        out.append("neck")
    return out


report = {"body": BODY, "garments": {k: v[0] + ("@" + ",".join(v[1]) if v[1] else "") for k, v in GARMENTS.items()},
          "depth_mm": DEPTH * 1000, "reach_mm": REACH * 1000, "body_points": len(body.data.vertices),
          "body_faces": len(body.data.polygons), "closed_shells_outer_triangles": report_shells,
          "covered_at_rest": {k: len(g["covers"]) for k, g in gar.items()}, "poses": {}}
for name in ("rest", "down30_elbow10", "down40_elbow10", "down50_elbow15", "stride", "sit"):
    pose(name)
    bpy.context.view_layer.update()
    J = {b: head_world(b) for b in ("lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "thigh_l", "thigh_r",
                                    "foot_l", "foot_r", "upperarm_l", "upperarm_r")}
    bb = evaluated(body)
    J["floor"] = min(v.co.z for v in bb.verts)
    out = {}
    for k, g in gar.items():
        bvh, co = garment_bvh(g)
        by_bone = defaultdict(lambda: [0, 0.0])
        reg = {r: [0, 0.0] for r in REGIONS}
        n1 = n3 = 0
        worst = 0.0
        for v in bb.verts:
            if v.index not in g["covers"]:
                continue
            hit = bvh.ray_cast(v.co + v.normal * 1e-5, -v.normal, REACH)
            if hit[0] is None or hit[3] <= DEPTH:
                continue
            loc, _n, fi, _dist = bvh.find_nearest(v.co)
            if loc is None:
                continue
            sd = (v.co - loc).dot(tri_normal(co, g["tris"][fi]) * g["flip"][fi])
            if sd <= DEPTH:
                continue
            d = sd * 1000
            n1 += 1
            n3 += d > 3
            worst = max(worst, d)
            bb_ = by_bone[dominant[v.index]]
            bb_[0] += 1
            bb_[1] = max(bb_[1], round(d, 1))
            for r in regions_at(v.co):
                reg[r][0] += 1
                reg[r][1] = max(reg[r][1], round(d, 1))
        out[k] = {"through_1mm": n1, "through_3mm": n3, "worst_mm": round(worst, 1), "regions": reg,
                  "bones": dict(sorted(by_bone.items(), key=lambda kv: -kv[1][0])[:10])}
    report["poses"][name] = out
    print("POSE", name, json.dumps({k: [v["through_1mm"], v["worst_mm"]] for k, v in out.items()}), flush=True)
    bb.free()

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(report, fh, indent=1)
print("SKIN_THROUGH done " + OUT, flush=True)
