"""HOW A SKINNED PAIR OF SHOES BENDS, measured before Unreal (30 October 2026, Tom's shoes; garment_pose_check.py's
poses, with the feet moved too, and its measure turned round: for shoes the fault is the body coming out through
them, not the garment sinking into the body).

    blender -b -P tools/meshgen/blender/shoe_pose_check.py -- SKINNED.blend OUT.json [--pair tom_shoes_LOD0]
        [--depth 0.003] [--render DIR]

SKINNED.blend is skin_shoes.py's: the skeleton, the body (its finest mesh, with the "in_shoe" group the Body Hidden
Face Map hides) and the pair. Poses from the reference pose: rest; walking (garment_pose_check.py's stride, the
front foot's toes up 12 degrees at heel strike, the back foot's heel up 20 degrees and its toes bent up 35 at the
ball for the push-off); sitting (thighs forward 90, knees 90, the feet relaxed 10 down); a stair (the shin 25
degrees forward over a flat foot); a deep toe bend (45 at the ball).

Per pose and foot:
  - visible: the body's points the face map keeps (the leg above the shoe's opening) that pass through the shoe:
    each one taken into its foot's own frame (the shoe is rigid on the foot behind the ball), the straight path
    from where it sat at rest to where the pose puts it crossing the shoe's surface and ending more than --depth
    beyond it, or ending more than --depth inside the leather;
  - foot: the hidden points (the foot under the shoe) covered at rest that the pose puts more than --depth outside
    the shoe (they are not drawn, so nothing shows: listed for the record);
  - the worst stretch of the shoe's edges against rest, and where (the ball's blend).
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, OUT = argv[:2]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
PAIR = opt("--pair", "tom_shoes_LOD0", str)
DEPTH = opt("--depth", 0.003)
RENDER = opt("--render", None, str)

bpy.ops.wm.open_mainfile(filepath=BLEND)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
pair = bpy.data.objects[PAIR]
body = next(o for o in bpy.data.objects if o.type == "MESH" and "in_shoe" in o.vertex_groups)
for o in [o for o in bpy.data.objects if o.type == "MESH" and o not in (pair, body)]:
    o.hide_render = True
    o.hide_viewport = True
pb = arm.pose.bones
gi = body.vertex_groups["in_shoe"].index
HID = np.array([any(g.group == gi and g.weight > 0.5 for g in v.groups) for v in body.data.vertices])


def update():
    bpy.context.view_layer.update()


def reset():
    for p in pb:
        p.matrix_basis = Matrix.Identity(4)
    update()


def head(b):
    return arm.matrix_world @ pb[b].head


def tail(b):
    return arm.matrix_world @ pb[b].tail


def rotate_world(bone, axis, degrees):
    p = pb[bone]
    update()
    hw = arm.matrix_world @ p.head
    R = Matrix.Translation(hw) @ Matrix.Rotation(math.radians(degrees), 4, axis) @ Matrix.Translation(-hw)
    p.matrix = arm.matrix_world.inverted() @ R @ arm.matrix_world @ p.matrix
    update()


def turn_toward(bone, tip_fn, direction, deg):
    update()
    h = head(bone)
    t = tip_fn()
    axis = (t - h).cross(direction)
    if axis.length < 1e-6:
        return
    rotate_world(bone, axis.normalized(), deg)


reset()
fwd = (head("ball_l") - head("foot_l"))
fwd.z = 0
fwd.normalize()
UP = Vector((0, 0, 1))
TOE = {s: (lambda s=s: head("ball_" + s) + (head("ball_" + s) - head("foot_" + s)).normalized() * 0.06) for s in "lr"}


def flex_foot(s, deg):
    """The foot about the ankle: positive raises the toes (dorsiflexion)."""
    turn_toward("foot_" + s, lambda: head("ball_" + s), UP if deg > 0 else -UP, abs(deg))


def bend_toes(s, deg):
    """The toes about the ball, up."""
    turn_toward("ball_" + s, TOE[s], UP, deg)


def pose(name):
    reset()
    if name == "walking":
        turn_toward("thigh_l", lambda: head("calf_l"), fwd, 28)
        turn_toward("thigh_r", lambda: head("calf_r"), -fwd, 18)
        turn_toward("calf_r", lambda: head("foot_r"), -fwd, 35)
        flex_foot("l", 12)
        flex_foot("r", -20)
        bend_toes("r", 35)
    elif name == "sitting":
        for s in "lr":
            turn_toward("thigh_" + s, lambda s=s: head("calf_" + s), fwd, 90)
            turn_toward("calf_" + s, lambda s=s: head("foot_" + s), Vector((0, 0, -1)), 90)
            flex_foot(s, -10)
    elif name == "stair":
        for s in "lr":
            turn_toward("calf_" + s, lambda s=s: head("foot_" + s), -fwd, 25)   # the shin forward over the foot
            flex_foot(s, 25)                                                    # the foot back to flat
    elif name == "toe bend":
        for s in "lr":
            bend_toes(s, 45)


def evaluated(o):
    dg = bpy.context.evaluated_depsgraph_get()
    e = o.evaluated_get(dg)
    m = e.to_mesh()
    P = np.array([tuple(o.matrix_world @ v.co) for v in m.vertices])
    tris = [tuple(t.vertices) for t in m.loop_triangles] if m.loop_triangles else None
    if tris is None:
        m.calc_loop_triangles()
        tris = [tuple(t.vertices) for t in m.loop_triangles]
    e.to_mesh_clear()
    return P, tris


def foot_matrix(s):
    """The foot bone's deformation in the world (rest to pose)."""
    p = pb["foot_" + s]
    return arm.matrix_world @ p.matrix @ p.bone.matrix_local.inverted() @ arm.matrix_world.inverted()


def inside(bvh, p):
    k = 0
    for d in (Vector((0, 0, 1)), Vector((0.31, 0.95, 0.02)), Vector((-0.6, -0.3, 0.74))):
        n, t = 0, 0.0
        for _ in range(30):
            loc, nr, fi, dd = bvh.ray_cast(p + d * (t + 1e-6), d, 1.0)
            if loc is None:
                break
            t = (loc - p).length
            n += 1
        k += n % 2
    return k >= 2


reset()
B0, _ = evaluated(body)
S0, ST = evaluated(pair)
bvh0 = BVHTree.FromPolygons([tuple(v) for v in S0], ST)
FLOOR = float(B0[:, 2].min())
top = float(S0[:, 2].max())
side_of = np.where(B0[:, 0] > 0, "l", "r")
near = B0[:, 2] < top + 0.15
vis_ids = np.where(near & ~HID)[0]
hid_ids = np.where(near & HID)[0]
covered0 = np.array([inside(bvh0, Vector(B0[i])) for i in hid_ids])
edges = set()
for t in ST:
    for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
        edges.add((min(a, b), max(a, b)))
E = np.array(sorted(edges))
L0 = np.linalg.norm(S0[E[:, 0]] - S0[E[:, 1]], axis=1)
ball_w = np.zeros(len(S0))
for v in pair.data.vertices:
    for g in v.groups:
        if pair.vertex_groups[g.group].name.startswith("ball_"):
            ball_w[v.index] = g.weight
rep = {"blend": BLEND, "pair": PAIR, "depthMm": DEPTH * 1000, "visiblePoints": int(len(vis_ids)),
       "hiddenPoints": int(len(hid_ids)), "hiddenCoveredAtRest": int(covered0.sum()), "poses": {}}
for name in ("rest", "walking", "sitting", "stair", "toe bend"):
    pose(name)
    B1, _ = evaluated(body)
    S1, _ = evaluated(pair)
    bvh1 = BVHTree.FromPolygons([tuple(v) for v in S1], ST)
    r = {}
    for s in "lr":
        Mi = foot_matrix(s).inverted()
        vis, vis_worst, into, into_worst = 0, 0.0, 0, 0.0
        for i in vis_ids[side_of[vis_ids] == s]:
            a = Vector(B0[i])
            q = Mi @ Vector(B1[i])
            seg = q - a
            L = seg.length
            if L > 1e-6:
                # every crossing of the shoe's surface on the way from rest to the pose: an even number (two or
                # more) means the point went in through one face of the leather and out through the other (a
                # poke through, seen); an odd number that it ends in the leather (the collar pressing into the leg,
                # covered by the leather itself)
                d_ = seg / L
                t, n, last = 0.0, 0, None
                for _ in range(20):
                    hit = bvh0.ray_cast(a + d_ * (t + 1e-6), d_, L - t - 1e-6)
                    if hit[0] is None:
                        break
                    t = (hit[0] - a).length
                    n += 1
                    last = hit[0]
                if n >= 2 and n % 2 == 0 and (q - last).length > DEPTH:
                    vis += 1
                    vis_worst = max(vis_worst, (q - last).length)
                    continue
                if n % 2 == 1:
                    loc, nrm, fi, d = bvh0.find_nearest(q)
                    if d > DEPTH:
                        into += 1
                        into_worst = max(into_worst, d)
                    continue
            loc, nrm, fi, d = bvh0.find_nearest(q)
            if loc is not None and d > DEPTH and inside(bvh0, q) and not inside(bvh0, a):
                into += 1
                into_worst = max(into_worst, d)
        out_n, out_w = 0, 0.0
        sel = side_of[hid_ids] == s
        for i, cov in zip(hid_ids[sel], covered0[sel]):
            if not cov:
                continue
            p = Vector(B1[i])
            loc, nrm, fi, d = bvh1.find_nearest(p)
            if loc is not None and d > DEPTH and not inside(bvh1, p):
                out_n += 1
                out_w = max(out_w, d)
        r[s] = {"visibleThrough": vis, "visibleThroughWorstMm": round(vis_worst * 1000, 1),
                "visibleIntoLeather": into, "visibleIntoLeatherWorstMm": round(into_worst * 1000, 1),
                "hiddenFootOut": out_n, "hiddenFootOutWorstMm": round(out_w * 1000, 1)}
    L1 = np.linalg.norm(S1[E[:, 0]] - S1[E[:, 1]], axis=1)
    ratio = L1 / np.maximum(L0, 1e-9)
    k = int(np.argmax(np.abs(np.log(ratio))))
    bw = (ball_w[E[k, 0]] + ball_w[E[k, 1]]) / 2
    r["stretch"] = {"worst": round(float(ratio[k]), 3), "p99": round(float(np.percentile(ratio, 99)), 3),
                    "p1": round(float(np.percentile(ratio, 1)), 3),
                    "worstEdgeBallWeight": round(float(bw), 2), "worstEdgeRestMm": round(float(L0[k]) * 1000, 1)}
    rep["poses"][name] = r
    print("SHOEPOSE", name, json.dumps(r), flush=True)
    if RENDER:
        os.makedirs(RENDER, exist_ok=True)
        sc = bpy.context.scene
        sc.render.engine = "BLENDER_WORKBENCH"
        sc.display.shading.light = "STUDIO"
        sc.display.shading.color_type = "OBJECT"
        sc.render.resolution_x, sc.render.resolution_y = 1000, 700
        if "hide" not in body.modifiers:
            m = body.modifiers.new("hide", "MASK")
            m.vertex_group = "in_shoe"
            m.invert_vertex_group = True
            m.show_viewport = False          # the counts read the whole body; only the pictures hide the feet
        body.color = (0.78, 0.66, 0.58, 1)
        pair.color = (0.18, 0.11, 0.07, 1)
        cam = bpy.data.objects.get("cam") or bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
        if cam.name not in sc.collection.objects:
            sc.collection.objects.link(cam)
        sc.camera = cam
        c = Vector(tuple(S1[S1[:, 0] < 0].mean(0)))       # the right shoe
        c.z += 0.04
        for view, d in (("side", Vector((-1, 0.1, 0.15))), ("front", Vector((-0.3, -1, 0.3))), ("back", Vector((-0.3, 1, 0.5)))):
            cam.location = c + d.normalized() * 0.75
            cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
            sc.render.filepath = os.path.join(RENDER, "%s-%s.png" % (name.replace(" ", "-"), view))
            bpy.ops.render.render(write_still=True)
reset()
json.dump(rep, open(OUT, "w"), indent=1)
print("SHOEPOSE written", OUT)
