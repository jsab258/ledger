"""A 1990 donkey jacket, made by script around MetaHuman's own template body.

    blender -b -P tools/meshgen/blender/donkey_jacket.py -- BODY.fbx OUT_DIR [--offset 0.03] [--girth 0.12 --name donkey_jacket_l]

WHY, 25 September. Jafar's clothing item: one donkey jacket fitted on two
bodies, moving, imported and packaged, trying the cheapest routes first. No
free one exists on Fab; image-to-3D on this card needs a licence ruling
(DINOv3) or money; and the Blender route had stopped at a crash exporting a
MetaHuman body. The crash was the command-line editor having no renderer
(tools/ue/export_body_fbx.py runs the export in the full editor), and the
plugin's own template body (/MetaHumanCharacter/Body/IdentityTemplate/SKM_Body)
exports whole. So the jacket is made from that body, FROM DIMENSIONS, as
CLAUDE.md allows once references alone will not do:

- the body's torso and arms, cut at the hips, the neck and the wrists;
- pushed out along their normals and smoothed, so the cloth stands off the
  body and hides its muscle;
- hung straight down from the chest in front and the shoulder blades behind,
  the way heavy donkey cloth falls, instead of following the waist;
- a hem let down to the top of the thigh, loose cuffs, a turned collar;
- a black yoke across the shoulders, front and back (the jacket's one mark:
  it was leather, later PVC, on navy or black wool), four big buttons;
- the body's own skin weights kept on it (it was cut from the body), so every
  MetaHuman skeleton moves it (in the game it follows the body as a
  leader-pose component).

WHAT COMES OUT, in OUT_DIR: donkey_jacket.fbx (the jacket and the body's
armature, nothing of the body mesh), donkey_jacket_front.png and _side.png
(the check pictures, on the grey body), donkey_jacket.json (counts, sizes,
the weights' coverage).

Nothing of Epic's body is kept in the jacket file: its vertices are new
positions of our own, and the armature is the skeleton every MetaHuman shares.
"""
import json
import math
import os
import sys

import bpy
import bmesh
from mathutils import Vector
from mathutils.kdtree import KDTree

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
BODY, OUT = argv[0], argv[1]
OFFSET = float(argv[argv.index("--offset") + 1]) if "--offset" in argv else 0.03
# SIZES, as a tailor has them: leader pose carries a wearer's bones, not his
# girth, so on Ron (a big man) the regular cut had his belly through its
# front (25 September). --girth adds room in front, less at the sides and
# back, a little in the sleeves. Made at 0.05 (regular, SKM_DonkeyJacket) and
# 0.13 (large, SKM_DonkeyJacket_L); the template's narrow waist let a man's
# shirt show at the sides at 0.
GIRTH = float(argv[argv.index("--girth") + 1]) if "--girth" in argv else 0.0
NAME = argv[argv.index("--name") + 1] if "--name" in argv else "donkey_jacket"
os.makedirs(OUT, exist_ok=True)

NAVY = (0.035, 0.043, 0.075, 1.0)      # navy wool, dark in the street's light
YOKE = (0.012, 0.012, 0.012, 1.0)      # the black shoulder panel
BUTTON = (0.02, 0.018, 0.016, 1.0)

TORSO_BONES = ("pelvis", "spine_", "clavicle", "upperarm", "lowerarm", "neck_01")
HAND_BONES = ("hand", "thumb", "index", "middle", "ring", "pinky", "wrist")

# ---------------------------------------------------------------- the body
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY)
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
body = max(meshes, key=lambda o: len(o.data.vertices))           # LOD0
for o in meshes:
    if o is not body:
        bpy.data.objects.remove(o, do_unlink=True)
bpy.context.view_layer.update()

def world(o, v):
    return o.matrix_world @ v.co

def joint(name):
    b = arm.data.bones.get(name)
    return arm.matrix_world @ b.head_local

pelvis, spine5, neck = joint("pelvis"), joint("spine_05"), joint("neck_01")
wrist_l, wrist_r = joint("hand_l"), joint("hand_r")
elbow_l = joint("lowerarm_l")

gnames = {g.index: g.name for g in body.vertex_groups}

def dominant(v):
    best, w = None, 0.0
    for g in v.groups:
        if g.weight > w:
            best, w = gnames.get(g.group), g.weight
    return best or ""

HEM_CUT = pelvis.z - 0.015          # the body is cut just below the waist ...
NECK_CUT = neck.z - 0.045           # ... and at the base of the neck

keep = set()
for v in body.data.vertices:
    d = dominant(v)
    p = world(body, v)
    if any(d.startswith(h) for h in HAND_BONES):
        continue
    if not any(d.startswith(t) for t in TORSO_BONES):
        continue
    if p.z < HEM_CUT or p.z > NECK_CUT:
        continue
    keep.add(v.index)

# ---------------------------------------------------------------- the shell
jacket = body.copy()
jacket.data = body.data.copy()
jacket.name = "DonkeyJacket"
bpy.context.collection.objects.link(jacket)
for mod in list(jacket.modifiers):
    jacket.modifiers.remove(mod)
# IN METRES, IN THE WORLD: the imported body's mesh sits in its own scaled,
# turned space (the first try put the collar at 107 units), and every
# measure below is against the skeleton's joints, which are in the world.
from mathutils import Matrix
jacket.parent = None
jacket.data.transform(body.matrix_world)
jacket.matrix_world = Matrix.Identity(4)
bm = bmesh.new()
bm.from_mesh(jacket.data)
bm.verts.ensure_lookup_table()
drop = [f for f in bm.faces if not all(v.index in keep for v in f.verts)]
bmesh.ops.delete(bm, geom=drop, context="FACES")
loose = [v for v in bm.verts if not v.link_faces]
bmesh.ops.delete(bm, geom=loose, context="VERTS")
# The exported body is split along its texture seams; weld them, or the shell
# is a dozen separate panels.
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0002)
# the largest connected piece only (stray islands of the cut)
bm.verts.ensure_lookup_table()
seen, pieces = set(), []
for v in bm.verts:
    if v in seen:
        continue
    stack, piece = [v], []
    seen.add(v)
    while stack:
        x = stack.pop()
        piece.append(x)
        for e in x.link_edges:
            y = e.other_vert(x)
            if y not in seen:
                seen.add(y)
                stack.append(y)
    pieces.append(piece)
pieces.sort(key=len, reverse=True)
stray = sum(len(p) for p in pieces[1:])
for piece in pieces[1:]:
    bmesh.ops.delete(bm, geom=piece, context="VERTS")
bm.normal_update()

# Stand the cloth off the body.
arm_axis_x = abs(elbow_l.x)
for v in bm.verts:
    on_arm = abs(v.co.x) > 0.17 and v.co.z < spine5.z + 0.05
    v.co += v.normal * (OFFSET * (0.8 if on_arm else 1.0))
# Smooth away the body's muscle, keeping the edges where they are.
inner = [v for v in bm.verts if not v.is_boundary]
for _ in range(12):
    bmesh.ops.smooth_vert(bm, verts=inner, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
bm.normal_update()
for v in inner:                      # smoothing shrinks: give back what it took
    v.co += v.normal * 0.006

# Hang it (the body faces -Y): heavy cloth falls straight down from the most
# forward point above it in front, and from the shoulder blades behind, so it
# bridges the waist instead of following it. Full at the centre, fading out
# towards the side seams, or the sides stand up as ridges (the first try).
HANG_TOP = spine5.z + 0.02
cols = {}
for v in bm.verts:
    if abs(v.co.x) < 0.2 and v.co.z < HANG_TOP + 0.08:
        cols.setdefault((round(v.co.x / 0.015), v.co.y < pelvis.y), []).append(v)
# THE TEMPLATE BODY IS A WOMAN'S (the only MetaHuman body that exports whole;
# the male source bodies crash the exporter, 25 September), and the jackets
# are for men: so the front is one flat panel at the chest's depth, sloping
# into the shoulders over the top 9 cm, which hides the bust and is how a
# stiff donkey jacket stands off anybody's chest.
BLEND = 0.09
for (_, front), vs in cols.items():
    below = [v.co.y for v in vs if v.co.z <= HANG_TOP]
    if not below:
        continue
    plane = min(below) if front else max(below)
    for v in vs:
        if v.co.z > HANG_TOP:
            continue
        ax = abs(v.co.x)
        wx = 1.0 if ax < 0.10 else max(0.0, 1.0 - (ax - 0.10) / 0.09)
        wz = min(1.0, (HANG_TOP - v.co.z) / BLEND)
        v.co.y += (plane - v.co.y) * wx * wz
inner = [v for v in bm.verts if not v.is_boundary]
torso_inner = [v for v in inner if abs(v.co.x) < 0.2]
for _ in range(4):
    bmesh.ops.smooth_vert(bm, verts=inner, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
for _ in range(10):                  # the body's lines still showed through the panel
    bmesh.ops.smooth_vert(bm, verts=torso_inner, factor=0.5, use_axis_x=False, use_axis_y=True, use_axis_z=True)
bm.normal_update()
if GIRTH > 0:
    for v in bm.verts:
        ax = abs(v.co.x)
        if ax >= 0.2 or v.co.z > HANG_TOP:          # the sleeves
            if ax > 0.17:
                v.co += v.normal * GIRTH * 0.3
            continue
        t = min(1.0, (HANG_TOP - v.co.z) / 0.15)
        wz = t * t * (3 - 2 * t)                    # none at the chest, full from the belly down
        wx = 1.0 if ax < 0.12 else max(0.4, 1.0 - (ax - 0.12) / 0.08 * 0.6)
        if v.co.y < pelvis.y:
            v.co.y -= GIRTH * wz * wx
        else:
            v.co.y += GIRTH * 0.3 * wz
        if ax > 0.08:
            v.co.x += math.copysign(GIRTH * 0.45 * wz * min(1.0, (ax - 0.08) / 0.08), v.co.x)
    for _ in range(4):
        bmesh.ops.smooth_vert(bm, verts=[v for v in bm.verts if not v.is_boundary], factor=0.5,
                              use_axis_x=True, use_axis_y=True, use_axis_z=True)
    bm.normal_update()

# Boundary loops: the hem (lowest), the neck (highest), two cuffs (the rest).
edges = [e for e in bm.edges if e.is_boundary]
loops, used = [], set()
for e in edges:
    if e in used:
        continue
    loop, stack = [], [e]
    used.add(e)
    while stack:
        x = stack.pop()
        loop.append(x)
        for v in x.verts:
            for y in v.link_edges:
                if y.is_boundary and y not in used:
                    used.add(y)
                    stack.append(y)
    loops.append(loop)
def centre(loop):
    vs = {v for e in loop for v in e.verts}
    return sum((v.co for v in vs), Vector()) / len(vs), vs
info = [(centre(l), l) for l in loops]
hem = min(info, key=lambda t: t[0][0].z)
collar = max(info, key=lambda t: t[0][0].z)
cuffs = [t for t in info if t is not hem and t is not collar and abs(t[0][0].x) > 0.25]

def extrude(loop, move):
    r = bmesh.ops.extrude_edge_only(bm, edges=loop)
    new = [g for g in r["geom"] if isinstance(g, bmesh.types.BMVert)]
    for v in new:
        move(v)
    return [g for g in r["geom"] if isinstance(g, bmesh.types.BMEdge) and g.is_boundary]

# The hem down to the top of the thigh, flaring a little. Two rows, so the
# weights have somewhere to blend.
(hc, _), hloop = hem
HEM_Z = pelvis.z - 0.16
def hem_row(depth):
    def move(v):
        out = Vector((v.co.x - hc.x, v.co.y - hc.y, 0.0))
        v.co.z = hc.z - depth
        if out.length > 1e-6:
            v.co += out.normalized() * (0.01 * depth / 0.08)
    return move
row = extrude(hloop, hem_row((hc.z - HEM_Z) * 0.5))
extrude(row, hem_row(hc.z - HEM_Z))

# Loose cuffs, past the wrist bone a little.
for (cc, cvs), cloop in cuffs:
    wrist = wrist_l if cc.x > 0 else wrist_r
    along = (wrist - cc)
    along = along.normalized() if along.length > 1e-6 else Vector((0, 0, -1))
    def cuff(v, along=along, cc=cc):
        out = v.co - cc
        v.co += along * 0.03 + out * 0.08
    extrude(cloop, cuff)

# A turned collar: up the neck, then out and down over itself. The cut
# neckline zig-zags along the body's triangles (the first try grew teeth), so
# it is made a level, smooth ring first.
(nc, ncv), nloop = collar
ring = list(ncv)
for v in ring:
    v.co.z = nc.z
for _ in range(6):
    new = {}
    for v in ring:
        nb = [e.other_vert(v) for e in v.link_edges if e.is_boundary]
        if len(nb) == 2:
            new[v] = (v.co + nb[0].co + nb[1].co) / 3
    for v, c in new.items():
        v.co = c
def up(v):
    out = Vector((v.co.x - nc.x, v.co.y - nc.y, 0.0))
    v.co.z += 0.045
    v.co += out * 0.05
row = extrude(nloop, up)
def over(v):
    out = Vector((v.co.x - nc.x, v.co.y - nc.y, 0.0))
    v.co.z -= 0.05
    v.co += out * 0.09
extrude(row, over)
bm.normal_update()

# Materials: navy wool, the black yoke across the shoulders, buttons.
jacket.data.materials.clear()
def mat(name, rgba, rough):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = rough
    m.diffuse_color = rgba
    return m
jacket.data.materials.append(mat("MI_DonkeyJacket_Wool", NAVY, 0.95))
jacket.data.materials.append(mat("MI_DonkeyJacket_Yoke", YOKE, 0.45))
jacket.data.materials.append(mat("MI_DonkeyJacket_Button", BUTTON, 0.6))
YOKE_FRONT = spine5.z + 0.02
YOKE_BACK = spine5.z - 0.05
# A clean edge to the yoke: cut the cloth along its lines first (the first
# one in the game had a ragged edge, faces taken whole either side of it).
for co, no in (((0, 0, YOKE_FRONT), (0, 0, 1)), ((0, 0, YOKE_BACK), (0, 0, 1)),
               ((0.21, 0, 0), (1, 0, 0)), ((-0.21, 0, 0), (1, 0, 0))):
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=no)
yoke_faces = 0
for f in bm.faces:
    c = f.calc_center_median()
    line = YOKE_FRONT if c.y < pelvis.y else YOKE_BACK
    f.material_index = 1 if (c.z > line and abs(c.x) < 0.21 and c.z < nc.z) else 0
    yoke_faces += f.material_index == 1

bm.to_mesh(jacket.data)
bm.free()

# Thickness: heavy cloth, outward.
sol = jacket.modifiers.new("Thickness", "SOLIDIFY")
sol.thickness = 0.008
sol.offset = 1.0
sol.use_rim = True
bpy.context.view_layer.objects.active = jacket
jacket.select_set(True)
bpy.ops.object.modifier_apply(modifier=sol.name)

# Four big buttons down the centre front.
bm = bmesh.new()
bm.from_mesh(jacket.data)
bm.verts.ensure_lookup_table()
kd = KDTree(len(bm.verts))
for v in bm.verts:
    kd.insert(v.co, v.index)
kd.balance()
front_verts = [v for v in bm.verts if abs(v.co.x) < 0.015 and v.co.y < pelvis.y]
buttons = 0
for z in [spine5.z - 0.06 - i * 0.105 for i in range(4)]:
    near = [v for v in front_verts if abs(v.co.z - z) < 0.02]
    if not near:
        continue
    y = min(v.co.y for v in near) - 0.003
    r = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, radius1=0.013, radius2=0.013, depth=0.006,
                              matrix=__import__("mathutils").Matrix.Translation((0.0, y, z)) @
                              __import__("mathutils").Matrix.Rotation(math.radians(90), 4, "X"))
    for v in r["verts"]:
        for f in v.link_faces:
            f.material_index = 2
    buttons += 1
bm.to_mesh(jacket.data)
bm.free()

# ---------------------------------------------------------------- the weights
# The shell was cut from the body, so each of its vertices still carries the
# body's own weights for the point it came from, and the extruded hem, cuffs
# and collar and the solidified inside copied them from their neighbours.
# Only the buttons are new: each takes the weights of the nearest weighted
# vertex of the cloth it sits on.
vs = jacket.data.vertices
has = [any(g.weight > 0.001 for g in v.groups) for v in vs]
kd = KDTree(sum(has))
for v, h in zip(vs, has):
    if h:
        kd.insert(v.co, v.index)
kd.balance()
filled = 0
for v, h in zip(vs, has):
    if h:
        continue
    _, src, _ = kd.find(v.co)
    for g in vs[src].groups:
        jacket.vertex_groups[g.group].add([v.index], g.weight, "REPLACE")
    filled += 1
weighted = sum(1 for v in jacket.data.vertices if any(g.weight > 0.001 for g in v.groups))
size_m = [round(d, 3) for d in jacket.dimensions]
# The imported skeleton object is scaled by 0.01 (the engine's centimetres):
# parent without moving the jacket, or it shrinks a hundredfold.
jacket.parent = arm
jacket.matrix_parent_inverse = arm.matrix_world.inverted()
am = jacket.modifiers.new("Armature", "ARMATURE")
am.object = arm
bpy.context.view_layer.update()
# WHERE THE SKIN PUTS IT, the check the first parented try failed (the jacket
# a hundredth of its size at the feet): top and bottom, skinned, in metres.
_ev = jacket.evaluated_get(bpy.context.evaluated_depsgraph_get())
_zs = [(jacket.matrix_world @ v.co).z for v in _ev.data.vertices]
skinned_z = (round(min(_zs), 3), round(max(_zs), 3))

# ---------------------------------------------------------------- pictures
def shoot(name, cam_loc, look):
    scn = bpy.context.scene
    cam = bpy.data.objects.get("Cam") or bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    if cam.name not in scn.objects:
        scn.collection.objects.link(cam)
    cam.location = cam_loc
    direction = Vector(look) - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 50
    scn.camera = cam
    scn.render.engine = "BLENDER_WORKBENCH"
    scn.display.shading.light = "STUDIO"
    scn.display.shading.color_type = "MATERIAL"
    scn.render.resolution_x, scn.render.resolution_y = 640, 900
    scn.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
grey = mat("Body_Grey", (0.55, 0.52, 0.5, 1.0), 0.8)
body.data.materials.clear()
body.data.materials.append(grey)
mid = Vector((0.0, 0.0, (HEM_Z + nc.z) / 2))
shoot(NAME + "_front.png", (0.0, -3.2, mid.z + 0.1), mid)
shoot(NAME + "_side.png", (2.4, -2.2, mid.z + 0.15), mid)
shoot(NAME + "_back.png", (0.0, 3.2, mid.z + 0.1), mid)

# ---------------------------------------------------------------- export
bpy.ops.object.select_all(action="DESELECT")
body_name = body.name
bpy.data.objects.remove(body, do_unlink=True)
jacket.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + ".fbx"), use_selection=True,
                         object_types={"ARMATURE", "MESH"}, add_leaf_bones=False, bake_anim=False,
                         mesh_smooth_type="FACE")
dims = jacket.dimensions
report = {"body": os.path.basename(BODY), "cutFrom": body_name, "verts": len(jacket.data.vertices),
          "faces": len(jacket.data.polygons), "weightedVerts": weighted, "groups": len(jacket.vertex_groups),
          "yokeFaces": yoke_faces, "buttons": buttons, "weightsFilledFromNeighbour": filled, "offsetM": OFFSET, "girthM": GIRTH, "name": NAME,
          "hemZ": round(HEM_Z, 3), "collarZ": round(nc.z, 3), "cuffs": len(cuffs),
          "size": size_m, "skinnedZ": skinned_z, "strayVertsDropped": stray}
with open(os.path.join(OUT, NAME + ".json"), "w", encoding="utf-8") as fh:
    json.dump(report, fh, indent=1)
print("JACKET " + json.dumps(report))
