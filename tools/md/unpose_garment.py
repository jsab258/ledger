"""A garment draped on a posed drape body (tools/md/pose_body.py) bent back with the body's own skeleton to the reference
pose the game's bodies stand in.

    blender -b --factory-startup -P tools/md/unpose_garment.py -- DRAPE_BODY.fbx DRAPE_BODY.json GARMENT.obj OUT.obj
        [--resolve Z0,Z1,XMAX] [--resolve-clear 0.2] [--resolve-rounds 12]     # the crotch put out of the bent-back body

WHY, 28 October 2026 (the sleeve's end, fourth round; production/research/game-clothing-pipeline/SLEEVE-END-2026-10-28.md).
Tom's elbows bend 36.6 degrees in his reference pose and Marvelous wraps each sleeve round one straight volume per arm,
so the sleeve's narrow end closed beside the forearm and the hand came through it. Draped on the same body with the
elbows straight (pose_body.py --keep-arms --straight-elbows), the sleeve goes round the forearm to its end. Loading the
reference pose in Marvelous (ImportPose) did not return the arm to it (the hand ended 154 mm low), so the garment is
taken back here, the way the game will move it: each garment vertex takes the skin weights of the nearest point of the
drape body's surface, and the skeleton turns each recorded joint back by its recorded turn.

HOW. Marvelous's OBJ (millimetres, y up) is read as Blender's (x, -z, y) / 1000; each group ("g name") becomes an
object; weights by Blender's data transfer (nearest face, interpolated); the elbow turns of DRAPE_BODY.json undone in
reverse order (the upper arm turns too, if the drape body has them, and the thighs about the hips); written back as Marvelous's OBJ, one group per
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

# the recorded turns undone: the elbows first, then the upper arms (they were made in the other order); the thighs
# (pose_body.py --thighs-apart, 30 October 2026, the jeans' crotch) on their own chain, about each hip
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
W = arm.matrix_world
for s, t in turns.items():
    for bone, rec, pivot_key in (("lowerarm_", t.get("elbow"), "elbow"), ("upperarm_", t if "turnDeg" in t else None, "shoulder"),
                                 ("thigh_", t.get("thigh"), "hip")):
        if not rec:
            continue
        pb = arm.pose.bones[bone + s]
        p = Vector(rec[pivot_key])
        R = Matrix.Rotation(-math.radians(rec["turnDeg"]), 4, Vector(rec["axis"]))
        pb.matrix = W.inverted() @ Matrix.Translation(p) @ R @ Matrix.Translation(-p) @ W @ pb.matrix
        bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode="OBJECT")

# WRITTEN BACK AS MARVELOUS WROTE IT, only the positions bent (28 October: the bake chain's importer reads the
# pattern's coordinates from the OBJ's "vt" lines, which a positions-and-faces file lost): every line kept but the
# "v" lines, each a vertex's new place; the "vn" lines dropped and faces' normal indices with them, since the bend
# changed the normals (the importer recomputes them)
dg = bpy.context.evaluated_depsgraph_get()
world, links = {}, {}
for name, (ob, used) in pieces.items():
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    for k, i in enumerate(used):
        world[i] = ev.matrix_world @ me.vertices[k].co
    for e in me.edges:
        a, b = used[e.vertices[0]], used[e.vertices[1]]
        links.setdefault(a, []).append(b)
        links.setdefault(b, []).append(a)
    ev.to_mesh_clear()

# --resolve Z0,Z1,XMAX (30 October 2026, Tom's jeans, drape n3): bent back, the thighs come together again (0 to 5 mm
# apart below his crotch) and each leg's cloth follows its own thigh into the other: 38 points over 3 mm inside him.
# Where two surfaces touch, cloth can only lie on the line where they meet, as a real pair of jeans lies pressed there.
# So inside that box (heights in metres, the middle within XMAX), each garment point inside the bent-back body (the
# OBJ's own body group) is put out on its surface plus --resolve-clear mm, a few rounds, each followed by one light
# smoothing of the points moved, the last a push alone. Off by default: every other garment is bent back as before.
resolved = None
if "--resolve" in argv:
    from mathutils.bvhtree import BVHTree
    z0, z1, xmax = (float(t) for t in argv[argv.index("--resolve") + 1].split(","))
    clear = float(argv[argv.index("--resolve-clear") + 1]) / 1000.0 if "--resolve-clear" in argv else 0.0002
    rounds = int(argv[argv.index("--resolve-rounds") + 1]) if "--resolve-rounds" in argv else 12
    body_name = max(pieces, key=lambda n: (n.endswith("_LOD0"), len(pieces[n][1])))
    bob, bused = pieces[body_name]
    bev = bob.evaluated_get(dg)
    bme = bev.to_mesh()
    bme.calc_loop_triangles()
    bvh = BVHTree.FromPolygons([tuple(bev.matrix_world @ v.co) for v in bme.vertices], [tuple(t.vertices) for t in bme.loop_triangles])
    bev.to_mesh_clear()
    body_verts = set(bused)
    zone = [i for i, c in world.items() if i not in body_verts and z0 <= c.z <= z1 and abs(c.x) <= xmax]
    touched = set()

    def push():
        n_ = 0
        for i in zone:
            loc, nrm, _fi, _d = bvh.find_nearest(world[i])
            if loc is not None and (world[i] - loc).dot(nrm) < clear:
                world[i] = loc + nrm * clear
                touched.add(i)
                n_ += 1
        return n_
    # a seam's two sides are separate points at one place (one group per piece): they move as one
    twins = {}
    for i in zone:
        twins.setdefault(tuple(round(c * 1e5) for c in world[i]), []).append(i)
    first = push()
    for _ in range(rounds):
        new = {i: world[i].lerp(sum((world[j] for j in links.get(i, [])), Vector()) / max(1, len(links.get(i, []))), 0.5)
               for i in touched if links.get(i)}
        world.update(new)
        for grp in twins.values():
            if len(grp) > 1:
                m_ = sum((world[i] for i in grp), Vector()) / len(grp)
                for i in grp:
                    world[i] = m_.copy()
        push()
    resolved = {"zone": [z0, z1, xmax], "zonePoints": len(zone), "insideBefore": first, "moved": len(touched),
                "insideAfter": sum(1 for i in zone if (lambda r: r[0] is not None and (world[i] - r[0]).dot(r[1]) < 0)(bvh.find_nearest(world[i])))}
moved = {i: (c.x * 1000.0, c.z * 1000.0, -c.y * 1000.0) for i, c in world.items()}
out, vi = [], 0
for line in open(GARMENT, encoding="utf-8", errors="replace"):
    if line.startswith("v "):
        if vi in moved:
            out.append("v %.4f %.4f %.4f\n" % moved[vi])
        else:
            out.append(line)
        vi += 1
    elif line.startswith("vn "):
        continue
    elif line.startswith("f "):
        toks = line.split()[1:]
        out.append("f " + " ".join("/".join(t.split("/")[:2]).rstrip("/") for t in toks) + "\n")
    else:
        out.append(line)
open(OUT, "w", encoding="utf-8").write("".join(out))
print("UNPOSED", OUT, {n: len(ob.data.vertices) for n, (ob, _) in pieces.items()}, flush=True)
if resolved is not None:
    print("RESOLVED", json.dumps(resolved), flush=True)
