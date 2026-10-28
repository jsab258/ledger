"""A garment draped on a posed drape body (tools/md/pose_body.py) bent back with the body's own skeleton to the reference
pose the game's bodies stand in.

    blender -b --factory-startup -P tools/md/unpose_garment.py -- DRAPE_BODY.fbx DRAPE_BODY.json GARMENT.obj OUT.obj

WHY, 28 October 2026 (the sleeve's end, fourth round; production/research/game-clothing-pipeline/SLEEVE-END-2026-10-28.md).
Tom's elbows bend 36.6 degrees in his reference pose and Marvelous wraps each sleeve round one straight volume per arm,
so the sleeve's narrow end closed beside the forearm and the hand came through it. Draped on the same body with the
elbows straight (pose_body.py --keep-arms --straight-elbows), the sleeve goes round the forearm to its end. Loading the
reference pose in Marvelous (ImportPose) did not return the arm to it (the hand ended 154 mm low), so the garment is
taken back here, the way the game will move it: each garment vertex takes the skin weights of the nearest point of the
drape body's surface, and the skeleton turns each recorded joint back by its recorded turn.

HOW. Marvelous's OBJ (millimetres, y up) is read as Blender's (x, -z, y) / 1000; each group ("g name") becomes an
object; weights by Blender's data transfer (nearest face, interpolated); the elbow turns of DRAPE_BODY.json undone in
reverse order (the upper arm turns too, if the drape body has them); written back as Marvelous's OBJ, one group per
piece, faces as read.
"""
import json
import math
import sys

import bpy
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:]
BODY_FBX, BODY_JSON, GARMENT, OUT = argv[:4]
turns = json.load(open(BODY_JSON, encoding="utf-8"))["turns"]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY_FBX)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = sorted([o for o in bpy.data.objects if o.type == "MESH"], key=lambda o: -len(o.data.vertices))[0]

# the garment, group by group, in Blender's frame
verts, groups, cur = [], {}, None
for line in open(GARMENT, encoding="utf-8", errors="replace"):
    if line.startswith("v "):
        x, y, z = (float(t) for t in line.split()[1:4])
        verts.append((x / 1000.0, -z / 1000.0, y / 1000.0))
    elif line.startswith("g "):
        cur = line[2:].strip()
        groups.setdefault(cur, [])
    elif line.startswith("f ") and cur is not None:
        groups[cur].append([int(t.split("/")[0]) - 1 for t in line.split()[1:]])
pieces = {}
for name, faces in groups.items():
    if not faces:
        continue
    used = sorted({i for f in faces for i in f})
    remap = {i: k for k, i in enumerate(used)}
    me = bpy.data.meshes.new(name)
    me.from_pydata([verts[i] for i in used], [], [[remap[i] for i in f] for f in faces])
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    pieces[name] = (ob, used)

# the body's skin weights onto each piece
for name, (ob, _) in pieces.items():
    for g in body.vertex_groups:
        ob.vertex_groups.new(name=g.name)
    m = ob.modifiers.new("weights", "DATA_TRANSFER")
    m.object = body
    m.use_vert_data = True
    m.data_types_verts = {"VGROUP_WEIGHTS"}
    m.vert_mapping = "POLYINTERP_NEAREST"
    m.layers_vgroup_select_src = "ALL"
    m.layers_vgroup_select_dst = "NAME"
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.modifier_apply(modifier=m.name)
    a = ob.modifiers.new("Armature", "ARMATURE")
    a.object = arm

# the recorded turns undone: the elbows first, then the upper arms (they were made in the other order)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
W = arm.matrix_world
for s, t in turns.items():
    for bone, rec, pivot_key in (("lowerarm_", t.get("elbow"), "elbow"), ("upperarm_", t if "turnDeg" in t else None, "shoulder")):
        if not rec:
            continue
        pb = arm.pose.bones[bone + s]
        p = Vector(rec[pivot_key])
        R = Matrix.Rotation(-math.radians(rec["turnDeg"]), 4, Vector(rec["axis"]))
        pb.matrix = W.inverted() @ Matrix.Translation(p) @ R @ Matrix.Translation(-p) @ W @ pb.matrix
        bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode="OBJECT")

# written back as Marvelous's OBJ
dg = bpy.context.evaluated_depsgraph_get()
out, base = [], 0
for name, (ob, _) in pieces.items():
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    out.append("g %s\n" % name)
    for v in me.vertices:
        c = ev.matrix_world @ v.co
        out.append("v %.4f %.4f %.4f\n" % (c.x * 1000.0, c.z * 1000.0, -c.y * 1000.0))
    for f in me.polygons:
        out.append("f " + " ".join(str(base + i + 1) for i in f.vertices) + "\n")
    base += len(me.vertices)
    ev.to_mesh_clear()
open(OUT, "w", encoding="utf-8").write("".join(out))
print("UNPOSED", OUT, {n: len(ob.data.vertices) for n, (ob, _) in pieces.items()}, flush=True)
