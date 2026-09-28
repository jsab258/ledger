"""A donkey jacket hung on a MetaHuman body by Blender's cloth simulation: a simulation mesh and a render mesh.

    blender -b -P tools/meshgen/blender/drape_jacket.py -- BODY.fbx OUT_DIR [--name NAME] [--offset 0.025] [--frames 60]

WHY, 28 September (Jafar's list, item 5, and production/research/character-
pipeline/clothing-and-face-lighting-2026-09-27.md): "sew the garment around
the actual MetaHuman body in Blender, with a separate simulation mesh". The
25 September jacket (donkey_jacket.py) was the body's own skin pushed out and
smoothed: it did not hang or swing like cloth (FINDINGS). This one starts the
same way, a shell cut from the body's torso and arms and stood off it, but
from a coarser level of the body, so its triangles are even and a few
centimetres across, which is what a simulation mesh wants (the research:
"thin, single-sided and simplified"). The hem is let down to the top of the
thigh. Then Blender's cloth simulation hangs it on the body under gravity,
held at the shoulders and collar, so it falls into folds against the body as
heavy wool does. What it settles into is the SIMULATION MESH; the RENDER
MESH is that, subdivided once, given the cloth's thickness, the black yoke
across the shoulders, four buttons and two patch pockets. Both carry the
body's skin weights (copied from the nearest part of the body), so either
moves with any MetaHuman skeleton.

OUT_DIR gets NAME.fbx (the render mesh, the simulation mesh and the armature,
nothing of the body), NAME_front.png and NAME_side.png (the check pictures,
on the grey body) and NAME.json (counts, sizes, the drape's settling).
"""
import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
BODY, OUT = argv[0], argv[1]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "donkey_jacket_draped", str)
OFFSET = opt("--offset", 0.03)
FRAMES = opt("--frames", 90, int)
SOURCE_LOD = opt("--lod", 1, int)       # the body level the shell is cut from: even, few-centimetre triangles
SMOOTH = opt("--smooth", 40, int)      # smoothing passes over the shell before it hangs
os.makedirs(OUT, exist_ok=True)

NAVY = (0.035, 0.043, 0.075, 1.0)       # navy wool, dark in the street's light
YOKE = (0.012, 0.012, 0.013, 1.0)       # the black leather (later PVC) panel
BUTTON = (0.02, 0.018, 0.016, 1.0)
TORSO_BONES = ("pelvis", "spine_", "clavicle", "upperarm", "lowerarm", "neck_01")
HAND_BONES = ("hand", "thumb", "index", "middle", "ring", "pinky", "wrist")

# ---------------------------------------------------------------- the body
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY)
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
meshes = sorted([o for o in bpy.context.scene.objects if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
body, source = meshes[0], meshes[min(SOURCE_LOD, len(meshes) - 1)]
for o in meshes:
    if o is not body and o is not source:
        bpy.data.objects.remove(o, do_unlink=True)
bpy.context.view_layer.update()


def joint(name):
    return arm.matrix_world @ arm.data.bones[name].head_local


pelvis, spine5, neck = joint("pelvis"), joint("spine_05"), joint("neck_01")
upperarm_l, thigh_l = joint("upperarm_l"), joint("thigh_l")
HEM = thigh_l.z - 0.11               # the top of the thigh
NECK_CUT = neck.z - 0.02             # close round the base of the neck
ARMPIT = upperarm_l.z - 0.09
# THE NECK'S RADIUS, from the body at the neck bone's height.
_ring = [body.matrix_world @ v.co for v in body.data.vertices if abs((body.matrix_world @ v.co).z - neck.z) < 0.01]
_ring = [p for p in _ring if (Vector((p.x, p.y, 0.0)) - Vector((neck.x, neck.y, 0.0))).length < 0.12]
NECK_R = sorted((Vector((p.x, p.y, 0.0)) - Vector((neck.x, neck.y, 0.0))).length for p in _ring)[len(_ring) // 2] if _ring else 0.06


def dominant(o, v, names):
    best, w = "", 0.0
    for g in v.groups:
        if g.weight > w:
            best, w = names.get(g.group, ""), g.weight
    return best


def shell_from(src):
    """The torso and arms of src, cut at the hips, the neck and the wrists, in world metres, welded, one piece."""
    # BY HEIGHT, not by bone: the bone cut followed the thighs up round the
    # seat and left tabs on the hem (first try, 28 September). Everything
    # between the hips and the base of the neck but the hands.
    names = {g.index: g.name for g in src.vertex_groups}
    keep = set()
    for v in src.data.vertices:
        d = dominant(src, v, names)
        p = src.matrix_world @ v.co
        if any(d.startswith(h) for h in HAND_BONES) or d.startswith("head") or d.startswith("neck_02"):
            continue
        if p.z < pelvis.z - 0.015 or p.z > NECK_CUT + 0.03:
            continue
        # ROUND THE NECK, not across it: a cut by height alone left a hole as
        # wide as the shoulders' slope and a collar like a ring (third try).
        if p.z > NECK_CUT - 0.07 and (Vector((p.x, p.y, 0.0)) - Vector((neck.x, neck.y, 0.0))).length < NECK_R + 0.012:
            continue
        keep.add(v.index)
    me = src.data.copy()
    me.transform(src.matrix_world)
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if not all(v.index in keep for v in f.verts)], context="FACES")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
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
    for piece in pieces[1:]:
        bmesh.ops.delete(bm, geom=piece, context="VERTS")
    bm.normal_update()
    return bm


bm = shell_from(source)
for v in bm.verts:
    v.co += v.normal * OFFSET
inner = [v for v in bm.verts if not v.is_boundary]
# AWAY WITH THE BODY'S MUSCLE: on Ron's own body 20 passes still showed his
# chest and shoulders through the cloth (first try on him, 28 September).
for _ in range(SMOOTH):
    bmesh.ops.smooth_vert(bm, verts=inner, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
bm.normal_update()
for v in inner:                      # smoothing shrinks: give back what it took
    v.co += v.normal * (0.006 + 0.0002 * SMOOTH)

# HUNG STRAIGHT FROM THE CHEST: heavy wool bridges the waist instead of
# following it. Round the body's upright axis, each torso point below the
# chest is pushed out to at least the chest's own distance in its direction,
# fully 8 cm under the chest, not at all at the chest.
AX = Vector((pelvis.x, pelvis.y, 0.0))
CHEST = ARMPIT - 0.03
BINS = 72
arm_names = ("upperarm", "lowerarm")


def angle_bin(co):
    return int(((math.atan2(co.y - AX.y, co.x - AX.x) + math.pi) / (2 * math.pi)) * BINS) % BINS


def radius(co):
    return (Vector((co.x, co.y, 0.0)) - AX).length


# THE ARMS are told apart by their bones (the shell keeps the body's weights).
src_names = {g.index: g.name for g in source.vertex_groups}
dl = bm.verts.layers.deform.active


def on_arm(v):
    if dl is None:
        return abs(v.co.x - AX.x) > abs(upperarm_l.x) - 0.02
    best, w = "", 0.0
    for gi, wt in v[dl].items():
        if wt > w:
            best, w = src_names.get(gi, ""), wt
    return best.startswith(arm_names)


# THE OUTERMOST POINT in each direction anywhere from the armpits to the
# hips (a chest, a bust, a belly or a seat): the cloth hangs from it (the
# second try took the chest at armpit height, above the fullest part, and
# the front still followed the body).
chest_r = [0.0] * BINS
for v in bm.verts:
    if CHEST - 0.35 < v.co.z < CHEST + 0.02 and not on_arm(v):
        k = angle_bin(v.co)
        chest_r[k] = max(chest_r[k], radius(v.co))
for k in range(BINS):                         # fill any empty direction from its neighbours
    if chest_r[k] == 0.0:
        chest_r[k] = max(chest_r[(k - 1) % BINS], chest_r[(k + 1) % BINS])


def hang(v, extra=0.0):
    k = angle_bin(v.co)
    want = chest_r[k] + 0.01 + extra      # a centimetre of ease
    r = radius(v.co)
    if r <= 1e-6:
        return
    w = min(1.0, max(0.0, (CHEST - v.co.z) / 0.08))
    if r < want:
        d = (Vector((v.co.x, v.co.y, 0.0)) - AX).normalized()
        v.co += d * (want - r) * w


for v in bm.verts:
    if v.co.z < CHEST and not on_arm(v):
        hang(v)

# THE HEM LET DOWN: the cut at the hips is carried down to the top of the
# thigh in four rows, at the chest's distance, flaring a centimetre, as a
# jacket's skirt stands off the seat.
bm.edges.ensure_lookup_table()
bottom = [e for e in bm.edges if e.is_boundary and all(v.co.z < pelvis.z + 0.02 for v in e.verts)]
rows = 4
edges = bottom
for r in range(rows):
    res = bmesh.ops.extrude_edge_only(bm, edges=edges)
    new_verts = [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]
    drop = (pelvis.z - 0.015 - HEM) / rows
    for v in new_verts:
        v.co.z -= drop
        hang(v, extra=0.01 * (r + 1) / rows)
    edges = [g for g in res["geom"] if isinstance(g, bmesh.types.BMEdge) and all(v in new_verts for v in g.verts)]
bm.normal_update()
# The push is made direction by direction, so it leaves upright ridges; a few
# passes of smoothing below the chest take them out without undoing the hang.
lower = [v for v in bm.verts if v.co.z < CHEST and not v.is_boundary and not on_arm(v)]
for _ in range(6):
    bmesh.ops.smooth_vert(bm, verts=lower, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=False)
bm.normal_update()

jacket_me = bpy.data.meshes.new(NAME + "_sim")
bm.to_mesh(jacket_me)
bm.free()
sim = bpy.data.objects.new(NAME + "_sim", jacket_me)
bpy.context.collection.objects.link(sim)

# THE HOLD: the shoulders and collar are held (they rest on the body in a
# real jacket); everything below the armpits hangs free, the sleeves too.
pin = sim.vertex_groups.new(name="hold")
for v in sim.data.vertices:
    p = v.co
    if p.z > ARMPIT + 0.03 and abs(p.x) < abs(upperarm_l.x) + 0.02:
        w = min(1.0, (p.z - ARMPIT - 0.03) / 0.06)
        pin.add([v.index], w, "REPLACE")

# ---------------------------------------------------------------- the drape
body_world = body.copy()
body_world.data = body.data.copy()
body_world.data.transform(body.matrix_world)
body_world.parent = None
body_world.matrix_world = Matrix.Identity(4)
for m in list(body_world.modifiers):
    body_world.modifiers.remove(m)
bpy.context.collection.objects.link(body_world)
col = body_world.modifiers.new("Collision", "COLLISION")
body_world.collision.thickness_outer = 0.004
body_world.collision.cloth_friction = 5.0

cloth = sim.modifiers.new("Cloth", "CLOTH")
s = cloth.settings
s.quality = 10
s.mass = 0.6                          # heavy melton wool: about 600 g a square metre
s.air_damping = 2.0
s.tension_stiffness = s.compression_stiffness = 60.0
s.shear_stiffness = 40.0
s.bending_stiffness = 8.0             # stiff cloth folds broadly
s.vertex_group_mass = "hold"
s.pin_stiffness = 1.0
cloth.collision_settings.distance_min = 0.005
cloth.collision_settings.use_self_collision = False
scene = bpy.context.scene
scene.frame_start, scene.frame_end = 1, FRAMES
cloth.point_cache.frame_start, cloth.point_cache.frame_end = 1, FRAMES
before = [v.co.copy() for v in sim.data.vertices]
prev = None
for f in range(1, FRAMES + 1):
    scene.frame_set(f)
    if f == FRAMES - 1:
        prev = [v.co.copy() for v in sim.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.vertices]
dg = bpy.context.evaluated_depsgraph_get()
final = sim.evaluated_get(dg).to_mesh()
last_move = max((a.co - b).length for a, b in zip(final.vertices, prev)) if prev else 0.0
drop_max = max((b - a.co).length for a, b in zip(final.vertices, before))
settled = bpy.data.meshes.new_from_object(sim.evaluated_get(dg))
sim.modifiers.clear()
sim.data = settled

# ---------------------------------------------------------------- the render mesh
render = sim.copy()
render.data = sim.data.copy()
render.name = NAME
bpy.context.collection.objects.link(render)
sub = render.modifiers.new("Subdivision", "SUBSURF")
sub.levels = sub.render_levels = 1
thick = render.modifiers.new("Solidify", "SOLIDIFY")
thick.thickness = 0.006
thick.offset = 1.0
for m in list(render.modifiers):
    bpy.context.view_layer.objects.active = render
    bpy.ops.object.modifier_apply(modifier=m.name)


def material(name, rgba, rough=0.9):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = rgba
    b.inputs["Roughness"].default_value = rough
    m.diffuse_color = rgba
    return m


wool, yoke = material("M_DonkeyWool", NAVY), material("M_DonkeyYoke", YOKE, 0.45)
render.data.materials.append(wool)
render.data.materials.append(yoke)
# THE YOKE: the panel across the shoulders, front and back, down to a little
# above the armpits behind and about a hand's width below the collar in front.
YOKE_BACK, YOKE_FRONT = ARMPIT + 0.02, NECK_CUT - 0.11
for poly in render.data.polygons:
    c = poly.center
    line = YOKE_FRONT if c.y < pelvis.y else YOKE_BACK
    if c.z > line and abs(c.x) < abs(upperarm_l.x) + 0.05:
        poly.material_index = 1

# THE COLLAR, made as its own clean band round the neck (extruded from the
# shell's uneven neckline it came out blocky, fourth try): a 3.5 cm stand,
# turned over into a 6 cm fall that lies out on the yoke, open at the front
# where the jacket buttons.
def collar():
    cm = bmesh.new()
    rings = [(-0.012, 0.016), (0.022, 0.018), (0.034, 0.026), (0.02, 0.045), (-0.02, 0.062)]
    n, gap = 40, math.radians(28)       # the front opening either side of straight ahead (-Y)
    angles = [(-math.pi / 2) + gap + (2 * math.pi - 2 * gap) * k / (n - 1) for k in range(n)]
    grid = []
    for dz, dr in rings:
        row = []
        for a in angles:
            r = NECK_R + dr
            row.append(cm.verts.new((neck.x + math.cos(a) * r * 1.12, neck.y + math.sin(a) * r, NECK_CUT + dz)))
        grid.append(row)
    for i in range(len(grid) - 1):
        for k in range(n - 1):
            cm.faces.new((grid[i][k], grid[i][k + 1], grid[i + 1][k + 1], grid[i + 1][k]))
    me = bpy.data.meshes.new("Collar")
    cm.to_mesh(me)
    cm.free()
    o = bpy.data.objects.new("Collar", me)
    bpy.context.collection.objects.link(o)
    so = o.modifiers.new("Solidify", "SOLIDIFY")
    so.thickness = 0.006
    sb = o.modifiers.new("Subdivision", "SUBSURF")
    sb.levels = sb.render_levels = 1
    bpy.context.view_layer.objects.active = o
    for m in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=m.name)
    o.data.materials.append(wool)
    return o


# BUTTONS AND POCKETS, as small solid pieces joined to the render mesh.
def front_point(x, z):
    """The most forward point of the settled jacket near (x, z) (the body faces -Y)."""
    near = [v.co for v in sim.data.vertices if abs(v.co.x - x) < 0.02 and abs(v.co.z - z) < 0.02]
    return min(near, key=lambda c: c.y) if near else None


extras = [collar()]
btn_mat = material("M_DonkeyButton", BUTTON, 0.35)
top_btn, low_btn = NECK_CUT - 0.14, HEM + 0.12
for k in range(4):
    z = top_btn + (low_btn - top_btn) * k / 3
    p = front_point(0.0, z)
    if p is None:
        continue
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.012, depth=0.006, location=(p.x, p.y - 0.006, p.z), rotation=(math.pi / 2, 0, 0))
    b = bpy.context.active_object
    b.data.materials.append(btn_mat)
    extras.append(b)
# PATCH POCKETS: the render mesh's own faces in a hand-sized patch low on
# each front, copied and stood 3 mm off, so they lie on the cloth.
pocket_faces = []
for side in (-1, 1):
    cx, cz = side * 0.11, HEM + 0.11
    for poly in render.data.polygons:
        c = poly.center
        if abs(c.x - cx) < 0.08 and abs(c.z - cz) < 0.085 and c.y < pelvis.y and poly.normal.y < -0.3:
            pocket_faces.append(poly.index)
if pocket_faces:
    bpy.context.view_layer.objects.active = render
    pbm = bmesh.new()
    pbm.from_mesh(render.data)
    pbm.faces.ensure_lookup_table()
    got = bmesh.ops.duplicate(pbm, geom=[pbm.faces[i] for i in pocket_faces])
    for g in got["geom"]:
        if isinstance(g, bmesh.types.BMVert):
            g.co += Vector((0.0, -0.003, 0.0))
    pbm.to_mesh(render.data)
    pbm.free()
bpy.ops.object.select_all(action="DESELECT")
for o in extras + [render]:
    o.select_set(True)
bpy.context.view_layer.objects.active = render
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.join()

# ---------------------------------------------------------------- the weights
# body_world is the body in world metres with its own weights; each target
# takes the weights of the nearest point of the body's surface.
for target in (render, sim):
    dt = target.modifiers.new("Weights", "DATA_TRANSFER")
    dt.object = body_world
    dt.use_vert_data = True
    dt.data_types_verts = {"VGROUP_WEIGHTS"}
    dt.vert_mapping = "POLYINTERP_NEAREST"
    dt.layers_vgroup_select_src = "ALL"
    dt.layers_vgroup_select_dst = "NAME"
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.datalayout_transfer(modifier="Weights")
    bpy.ops.object.modifier_apply(modifier="Weights")
    target.parent = arm
    target.matrix_parent_inverse = arm.matrix_world.inverted()   # stays where it is: the armature is imported turned and scaled
    am = target.modifiers.new("Armature", "ARMATURE")
    am.object = arm
covered = sum(1 for v in render.data.vertices if v.groups) / max(1, len(render.data.vertices))

# ---------------------------------------------------------------- the pictures
grey = material("M_Body", (0.5, 0.5, 0.5, 1.0))
body_world.data.materials.clear()
body_world.data.materials.append(grey)
body.hide_render = True
if source is not body:
    source.hide_render = True
sim.hide_render = True
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_specular_highlight = False   # the check picture shows shape; the shine read as leather
scene.render.resolution_x, scene.render.resolution_y = 900, 1200
cam_data = bpy.data.cameras.new("Cam")
cam_data.lens = 70
cam = bpy.data.objects.new("Cam", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam
mid = Vector((0.0, pelvis.y, (HEM + neck.z) / 2))
for tag, off in (("front", Vector((0.0, -3.2, 0.1))), ("side", Vector((3.2, 0.0, 0.1)))):
    cam.location = mid + off
    cam.rotation_euler = (mid - cam.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(OUT, "%s_%s.png" % (NAME, tag))
    bpy.ops.render.render(write_still=True)

# ---------------------------------------------------------------- out
bpy.ops.object.select_all(action="DESELECT")
for o in (render, sim, arm):
    o.hide_render = False
    o.select_set(True)
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + ".fbx"), use_selection=True, add_leaf_bones=False,
                         mesh_smooth_type="FACE", object_types={"ARMATURE", "MESH"})
report = {
    "body": BODY, "offset": OFFSET, "frames": FRAMES, "sourceLod": SOURCE_LOD,
    "sim": {"verts": len(sim.data.vertices), "tris": sum(len(p.vertices) - 2 for p in sim.data.polygons)},
    "render": {"verts": len(render.data.vertices)},
    "hem": round(HEM, 3), "neck": round(NECK_CUT, 3), "neckRadius": round(NECK_R, 3),
    "settling": {"largestFallM": round(drop_max, 3), "lastFrameMoveM": round(last_move, 4)},
    "weightsCoverage": round(covered, 3),
}
json.dump(report, open(os.path.join(OUT, NAME + ".json"), "w"), indent=1)
print("DRAPE", json.dumps(report))
