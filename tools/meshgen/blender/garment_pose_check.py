"""HOW A BOUND GARMENT BENDS, measured before Unreal (30 September). Poses the
wearer's body and the garment bound to it (bind_garment.py) together, and
counts, for each pose, where the garment fails the way skinned clothes fail:
the body coming through it, and its surface stretched or crushed where the
weights pull two neighbouring points apart (the armpits, the sides, the hips).
No rendering: numbers only, on the processor, so the graphics card stays free.

    blender -b -P tools/meshgen/blender/garment_pose_check.py -- BODY.fbx BOUND.blend OUT.json [--render DIR] [--sit SIT.fbx]

--sit takes the sitting pose from the last frame of a sit made on the same
skeleton (F:/LedgerTools/tmp/drape/ron_sit.fbx, made by sit_anim.py, the one
the game plays); without it the thighs and knees are bent here by hand.

--render DIR also draws each pose from the front, the side and the back
(Blender's plain Workbench look, the garment dark and the body light), for
looking, not for judging: the judging is in Unreal.

Poses, each from MetaHuman's reference pose: rest; arms raised (upper arms
lifted 110 degrees); arms forward (reaching, elbows bent); a walking stride;
sitting (thighs forward 90 degrees, knees bent 90). The corrective bones Unreal
drives from the arms (the MetaHuman body's pose drivers) stay put here, for
the body and the garment alike, so both bend the same way.

For each pose: through, the share of the garment's points more than 5 mm
inside the body that were outside it at rest (the collar stands inside the
body mesh's open neck ring even at rest, so rest is the baseline), with the
worst places by the bone that moves each point most;
stretched and crushed, the share of its edges longer than 1.35 times or
shorter than 0.65 times their rest length; and the worst regions by bone.
bodyStretched and bodyCrushed give the same for the body's own skin, the
floor a garment copying its weights can reach.
"""
import json
import math
import sys
from collections import Counter

import bmesh
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
BODY, BOUND, OUT = argv[:3]
RENDER = argv[argv.index("--render") + 1] if "--render" in argv else None
SIT = argv[argv.index("--sit") + 1] if "--sit" in argv else None

bpy.ops.wm.open_mainfile(filepath=BOUND)
gar = next(o for o in bpy.data.objects if o.type == "MESH")
old_arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=BODY)
new = [o for o in bpy.data.objects if o not in before]
arm = next(o for o in new if o.type == "ARMATURE")
meshes = sorted([o for o in new if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
body = meshes[0]
for o in meshes[1:]:
    bpy.data.objects.remove(o, do_unlink=True)
# The garment onto the freshly imported skeleton (the same bones, the same rest).
mw = gar.matrix_world.copy()
gar.parent = None
gar.matrix_world = mw
for m in gar.modifiers:
    if m.type == "ARMATURE":
        m.object = arm
bpy.data.objects.remove(old_arm, do_unlink=True)

pb = arm.pose.bones
sit_pose = {}
if SIT:
    had = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=SIT)
    sit_objs = [o for o in bpy.data.objects if o not in had]
    sa = next(o for o in sit_objs if o.type == "ARMATURE")
    act = sa.animation_data.action if sa.animation_data else None
    if act is not None:
        bpy.context.scene.frame_set(int(act.frame_range[1]))
    bpy.context.view_layer.update()
    # Each bone's place in the world at the sit's last frame, taken into
    # this skeleton's own space.
    for b in sa.pose.bones:
        sit_pose[b.name] = arm.matrix_world.inverted() @ sa.matrix_world @ b.matrix
    bpy.context.scene.frame_set(1)
    for o in sit_objs:
        bpy.data.objects.remove(o, do_unlink=True)
dominant = []
groups = {g.index: g.name for g in gar.vertex_groups}
for v in gar.data.vertices:
    best = max(v.groups, key=lambda g: g.weight, default=None)
    dominant.append(groups[best.group] if best else "none")


def world_axis(name):
    # The body stands up +Z; its facing is found from the feet and the head.
    return {"up": Vector((0, 0, 1))}[name]


def head_world(b):
    return arm.matrix_world @ pb[b].head


def rotate_world(bone, axis, degrees):
    """Turn a bone about a world axis through its own head (its children follow)."""
    p = pb[bone]
    bpy.context.view_layer.update()
    hw = arm.matrix_world @ p.head
    R = Matrix.Translation(hw) @ Matrix.Rotation(math.radians(degrees), 4, axis) @ Matrix.Translation(-hw)
    p.matrix = arm.matrix_world.inverted() @ R @ arm.matrix_world @ p.matrix
    bpy.context.view_layer.update()


def reset():
    for p in pb:
        p.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()


def point(b):
    bpy.context.view_layer.update()
    return arm.matrix_world @ pb[b].tail


reset()
# The body's own directions: side (left hand minus right hand), forward (the toes' way).
side = (head_world("upperarm_l") - head_world("upperarm_r")).normalized()
fwd = (point("ball_l") - head_world("foot_l"))
fwd.z = 0
fwd.normalize()


def lift_arms(deg):
    for s, sgn in (("l", 1), ("r", -1)):
        # About the forward axis, the way that takes the hand up.
        for trial in (deg, -deg):
            reset_arm = pb["upperarm_" + s].matrix_basis.copy()
            before_z = point("hand_" + s).z
            rotate_world("upperarm_" + s, fwd, trial * sgn)
            if point("hand_" + s).z > before_z:
                break
            pb["upperarm_" + s].matrix_basis = reset_arm
            bpy.context.view_layer.update()


def turn_toward(bone, tip, direction, deg):
    """Turn a bone about the axis that swings its tip toward a direction."""
    bpy.context.view_layer.update()
    h = head_world(bone)
    t = point(tip) if tip else point(bone)
    axis = (t - h).cross(direction)
    if axis.length < 1e-6:
        return
    rotate_world(bone, axis.normalized(), deg)


def pose(name):
    reset()
    if name == "arms raised":
        lift_arms(110)
    elif name == "arms forward":
        for s in ("l", "r"):
            turn_toward("upperarm_" + s, "lowerarm_" + s, fwd, 70)
            turn_toward("lowerarm_" + s, "hand_" + s, Vector((0, 0, 1)), 80)
    elif name == "walking stride":
        turn_toward("thigh_l", "calf_l", fwd, 28)
        turn_toward("thigh_r", "calf_r", -fwd, 18)
        turn_toward("calf_r", "foot_r", -fwd, 35)
        turn_toward("upperarm_l", "lowerarm_l", -fwd, 22)
        turn_toward("upperarm_r", "lowerarm_r", fwd, 22)
        turn_toward("lowerarm_r", "hand_r", fwd, 25)
    elif name == "sitting" and sit_pose:
        # Parents before children, so each bone lands where the sit put it.
        def depth(b):
            return 0 if b.parent is None else 1 + depth(b.parent)
        for b in sorted(pb, key=depth):
            if b.name in sit_pose:
                b.matrix = sit_pose[b.name]
                bpy.context.view_layer.update()
    elif name == "sitting":
        for s in ("l", "r"):
            turn_toward("thigh_" + s, "calf_" + s, fwd, 90)
            turn_toward("calf_" + s, "foot_" + s, Vector((0, 0, -1)), 90)
            turn_toward("upperarm_" + s, "lowerarm_" + s, fwd, 25)
            turn_toward("lowerarm_" + s, "hand_" + s, fwd, 45)


def evaluated(o):
    dg = bpy.context.evaluated_depsgraph_get()
    e = o.evaluated_get(dg)
    m = e.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(m)
    bm.transform(o.matrix_world)
    e.to_mesh_clear()
    return bm


def edges_of(bm):
    return [(e.verts[0].index, e.verts[1].index) for e in bm.edges], [e.calc_length() for e in bm.edges]


def strain(bm, pairs, lengths):
    bm.verts.ensure_lookup_table()
    s, c = [], []
    for (a, b), L0 in zip(pairs, lengths):
        if L0 < 1e-6:
            continue
        r = (bm.verts[a].co - bm.verts[b].co).length / L0
        if r > 1.35:
            s.append(a)
        elif r < 0.65:
            c.append(a)
    return s, c


reset()
body_rest = evaluated(body)
body_pairs, body_len = edges_of(body_rest)
rest = evaluated(gar)
rest.verts.ensure_lookup_table()
rest_len = [e.calc_length() for e in rest.edges]
edge_verts = [(e.verts[0].index, e.verts[1].index) for e in rest.edges]
report = {"body": BODY, "bound": BOUND, "points": len(rest.verts), "edges": len(rest_len), "poses": {}}
at_rest = None

for name in ("rest", "arms raised", "arms forward", "walking stride", "sitting"):
    pose(name)
    bb = evaluated(body)
    bs, bc = strain(bb, body_pairs, body_len)
    bmesh.ops.triangulate(bb, faces=bb.faces[:])
    bvh = BVHTree.FromBMesh(bb)
    g = evaluated(gar)
    g.verts.ensure_lookup_table()
    inside = []
    for v in g.verts:
        loc, nrm, fi, d = bvh.find_nearest(v.co)
        if loc is not None and (v.co - loc).dot(nrm) < 0 and d > 0.005:
            inside.append((d, v.index))
    if at_rest is None:
        at_rest = {i for _, i in inside}
    inside = [(d, i) for d, i in inside if i not in at_rest]
    stretched, crushed = strain(g, edge_verts, rest_len)
    worst = sorted(inside, reverse=True)[:1]
    report["poses"][name] = {
        "through": round(len(inside) / len(g.verts), 4),
        "throughDeepestMm": round(worst[0][0] * 1000, 1) if worst else 0.0,
        "throughWhere": Counter(dominant[i] for _, i in inside).most_common(4),
        "stretched": round(len(stretched) / len(rest_len), 4),
        "crushed": round(len(crushed) / len(rest_len), 4),
        "badWhere": Counter(dominant[i] for i in stretched + crushed).most_common(4),
        "bodyStretched": round(len(bs) / len(body_len), 4),
        "bodyCrushed": round(len(bc) / len(body_len), 4),
    }
    print("POSE", name, json.dumps(report["poses"][name]), flush=True)
    bb.free()
    g.free()

def draw(name):
    import os
    os.makedirs(RENDER, exist_ok=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light = "STUDIO"
    sc.display.shading.color_type = "OBJECT"
    sc.render.resolution_x = sc.render.resolution_y = 1100
    body.color = (0.8, 0.78, 0.74, 1)
    gar.color = (0.12, 0.16, 0.3, 1)
    bpy.context.view_layer.update()
    pts = [gar.matrix_world @ v.co for v in gar.data.vertices]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    mid = (lo + hi) / 2
    mid.z = (arm.matrix_world @ pb["spine_04"].head).z - 0.1
    cam_data = bpy.data.cameras.new("c")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = 1.6
    cam = bpy.data.objects.new("c", cam_data)
    sc.collection.objects.link(cam)
    sc.camera = cam
    for view, d in (("front", fwd), ("side", side), ("back", -fwd)):
        cam.location = mid + d * 4.0
        cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = os.path.join(RENDER, "%s-%s.png" % (name.replace(" ", "-"), view))
        bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)


if RENDER:
    for name in ("rest", "arms raised", "arms forward", "walking stride", "sitting"):
        pose(name)
        draw(name)

json.dump(report, open(OUT, "w"), indent=1)
print("CHECK written", OUT, flush=True)
