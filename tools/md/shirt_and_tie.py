"""A shirt front, shirt collar, shirt cuffs and a tie, fitted to a MetaHuman body in its reference pose, to go under
the proof jacket (Jafar's proof: "a 1990 single-breasted charcoal wool suit jacket ... with a shirt and tie under").

    blender -b -P tools/md/shirt_and_tie.py -- BODY.fbx OUT_PREFIX [--with-body]

OUT_PREFIX.fbx: one mesh, three materials (shirt, tie, and the knot under the tie's), centimetres, the body's own
skeleton beside it, for the builder; with --with-body also OUT_PREFIX-avatar.fbx, the body and the shirt and tie as
the body with its skin pushed out to the shirt and tie, the avatar the jacket is draped over in Marvelous Designer.

WHY, 2 October. The jacket's V runs to its top button at the waist (a 1990 two-button stance), so the shirt and tie
show from the collar to the waist, and the shirt's collar above the jacket's at the back and its cuffs below the
sleeves. Only those parts of a shirt are ever seen under a buttoned jacket, so they are what is made here, from the
body itself: the shirt front is the body's front between the lapels, smoothed (a shirt hides the muscles) and lifted
6 mm clear of it; the collar a stand and a fall round the neck, lower at the front, its points spreading either side
of the knot; the cuffs short tubes at the wrists; the tie 9 cm across at its foot (1990's width, 3 1/2 in), from a
four-in-hand knot at the collar to just above the waist, lying on the shirt. The earlier suit's shirt front and tie
(MakeHuman's, CC0) stop 15 cm short of this jacket's V. Sizes from the body's own joints, so they fit Darren as
they fit Ron.
"""
import math
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, PREFIX = argv[0], argv[1]
WITH_BODY = "--with-body" in argv
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = sorted([o for o in bpy.data.objects if o.type == "MESH"], key=lambda o: -len(o.data.vertices))[0]
for o in [o for o in bpy.data.objects if o.type == "MESH" and o is not body]:
    bpy.data.objects.remove(o, do_unlink=True)
J = lambda n: arm.matrix_world @ arm.pose.bones[n].head  # noqa: E731
dg = bpy.context.evaluated_depsgraph_get()
bm_body = bmesh.new()
bm_body.from_object(body, dg)
bm_body.transform(body.matrix_world)
BVH = BVHTree.FromBMesh(bm_body)


def surface(origin, direction, far=0.6):
    hit = BVH.ray_cast(origin, direction.normalized(), far)
    return hit[0], hit[1]


neck, neck2, spine5 = J("neck_01"), J("neck_02"), J("spine_05")
pelvis, spine2 = J("pelvis"), J("spine_02")
# the body faces -y; heights from the joints
z_neck = neck.z                      # the base of the neck, where a shirt collar sits
z_waist = spine2.z                   # as tools/meshgen/blender/body_measurements.py takes the waist
front_y = -1.0

shirt = bmesh.new()
uv_s = shirt.loops.layers.uv.new("UVMap")
mat_of = {}


def grid(rows, cols, point_at, mat, size=(0.25, 0.25)):
    """A quad grid of points point_at(u, v) (u across, v down), faces given material index mat, its UVs one unit to
    25 cm of cloth (size: the grid's width and height in metres), so the textures (tools/md/cloth_textures.py) lie
    at their real scale."""
    vs = [[shirt.verts.new(point_at(c / (cols - 1), r / (rows - 1))) for c in range(cols)] for r in range(rows)]
    for r in range(rows - 1):
        for c in range(cols - 1):
            f = shirt.faces.new((vs[r][c], vs[r][c + 1], vs[r + 1][c + 1], vs[r + 1][c]))
            f.material_index = mat
            for lp, (uu, vv) in zip(f.loops, ((c, r), (c + 1, r), (c + 1, r + 1), (c, r + 1))):
                lp[uv_s].uv = (uu / (cols - 1) * size[0] / 0.25, (1 - vv / (rows - 1)) * size[1] / 0.25)
    return vs


# THE SHIRT FRONT: the body's front from the waist (and 3 cm below) to the base of the neck, 34 cm across at the
# chest, each point found by a ray from in front, smoothed over a 4 cm window and lifted 6 mm off the skin
TOP = z_neck - 0.015
BOT = z_waist - 0.03
HALF = 0.17


def front_point(u, v, lift=0.008):
    x = (u - 0.5) * 2 * HALF
    z = TOP + (BOT - TOP) * v
    # narrower towards the neck: the shirt front there is only what the collar opening shows; and narrower below
    # the chest, where the jacket's fronts close over it (full width there poked out by the pockets)
    x *= 0.55 + 0.45 * min(1.0, (TOP - z) / 0.12)
    x *= 1.0 - 0.45 * max(0.0, min(1.0, (z_waist + 0.12 - z) / 0.15))
    acc, n = Vector(), 0
    for dx in (-0.02, 0.0, 0.02):
        for dz in (-0.02, 0.0, 0.02):
            p, _ = surface(Vector((x + dx, -0.6, z + dz)), Vector((0, 1, 0)))
            if p is not None:
                acc += p
                n += 1
    p = acc / max(n, 1)
    q, nrm = surface(Vector((x, -0.6, z)), Vector((0, 1, 0)))
    y = min(p.y, q.y if q is not None else p.y) - lift      # never inside the skin where the smoothing cut a hollow
    return Vector((x, y, z))


grid(44, 23, front_point, 0, (2 * HALF, TOP - BOT))

# THE COLLAR: a stand 3.5 cm high at the back round the base of the neck, 2 cm lower at the front, 6 mm off the
# skin; then the fall, turned down over the stand, 4 cm at the back to 7 cm at its points, either side of the knot
centre = Vector((neck.x, (neck.y + neck2.y) / 2, 0))
OPEN = math.radians(18)                 # the gap at the front where the knot sits, each side


def neck_radius(theta, z):
    d = Vector((math.sin(theta), -math.cos(theta), 0))     # theta 0 is straight ahead (-y)
    p, _ = surface(Vector((centre.x, centre.y, z)) + d * 0.25, -d)   # from outside in
    return (Vector((p.x, p.y, 0)) - centre).length if p is not None else 0.07


def collar_point(theta, h, out):
    drop = 0.02 * (0.5 + 0.5 * math.cos(theta))           # lower towards the front
    z = z_neck + 0.005 - drop + h
    r = neck_radius(theta, z) + out
    return Vector((centre.x + r * math.sin(theta), centre.y - r * math.cos(theta), z))


# the collar only where it can show: round the front and sides, to 115 degrees from the front each way; at the back
# the jacket's own collar covers it (drawn all round, it came through the jacket's collar at the back of the neck)
BACK = math.radians(115)
SPANS = [(OPEN, BACK), (2 * math.pi - BACK, 2 * math.pi - OPEN)]
for a0, a1 in SPANS:
    grid(2, 24, lambda u, v, a0=a0, a1=a1: collar_point(a0 + (a1 - a0) * u, 0.035 * (1 - v), 0.006), 0, (0.2, 0.035))


def fall_point(u, v, a0=OPEN, a1=2 * math.pi - OPEN):
    th = a0 + (a1 - a0) * u
    front = 0.5 + 0.5 * math.cos(th)                       # 1 at the front, 0 at the back
    depth = 0.04 + 0.03 * front ** 3                       # the points longer
    top = collar_point(th, 0.036, 0.008)
    # the fall hangs close round the stand (the neck's girth at the stand's foot, not the shoulders' below it: the
    # first try followed the shoulders and the collar stood out like wings)
    # close round the stand all the way (the jacket's collar lies over it at the back: 16 mm out, the fall came
    # through it)
    base = collar_point(th, 0.0, 0.010 if front < 0.5 else 0.014)
    low = Vector((base.x, base.y, top.z - depth * (0.75 if front < 0.5 else 1.0)))
    p = top.lerp(low, v)
    if front > 0.9 and v > 0.5:                            # the points spread a little, away from the knot
        s = 1 if math.sin(th) > 0 else -1
        p.x += s * 0.008 * (v - 0.5) * 2 * (front - 0.9) * 10
    return p


for a0, a1 in SPANS:
    grid(6, 24, lambda u, v, a0=a0, a1=a1: fall_point(u, v, a0, a1), 0, (0.21, 0.05))

# THE CUFFS: 6 cm tubes round each wrist, from 1.5 cm over the hand to 4.5 cm up the forearm, 7 mm off the skin
for s in "lr":
    w, e = J("hand_" + s), J("lowerarm_" + s)
    ax = (w - e).normalized()
    side = ax.cross(Vector((0, 0, 1))).normalized()
    up = side.cross(ax).normalized()

    def cuff_point(u, v, w=w, ax=ax, side=side, up=up):
        a = 2 * math.pi * u
        d = side * math.cos(a) + up * math.sin(a)
        c = w + ax * (0.015 - 0.06 * v)
        p, _ = surface(c + d * 0.2, -d)
        r = (p - c).length if p is not None else 0.035
        return c + d * (r + 0.007)

    grid(4, 32, cuff_point, 0, (0.24, 0.06))

# THE TIE: a four-in-hand knot at the collar's front and a blade to 2 cm above the waist, 4 cm wide under the knot,
# 9 cm at its foot, its point 4 cm deep, lying 3 mm on the shirt
knot_top = collar_point(0.0, 0.03, 0.012)
knot_bot = collar_point(0.0, -0.015, 0.016)
KT, KB = 0.022, 0.016                                     # the knot's half-widths, top and bottom
knot = grid(6, 6, lambda u, v: Vector(((u - 0.5) * 2 * (KT + (KB - KT) * v), 0, 0)) + knot_top.lerp(knot_bot, v)
            + Vector((0, -0.012 * math.sin(math.pi * u), 0)), 1, (0.045, 0.045))
z0, z1 = knot_bot.z + 0.004, z_waist + 0.02


def blade_point(u, v):
    z = z0 + (z1 - z0) * v
    half = 0.02 + 0.025 * v                                # 4 cm under the knot to 9 cm at the foot
    x = (u - 0.5) * 2 * half
    if v > 0.93:                                           # the point: the foot's middle carried 4 cm lower
        t = (v - 0.93) / 0.07
        z -= 0.04 * t * (1 - abs(u - 0.5) * 2)
    p = front_point(0.5 + x / (2 * HALF), (z - TOP) / (BOT - TOP), lift=0.009)
    return Vector((x, p.y - 0.004 * math.cos(math.pi * (u - 0.5)), z))


grid(30, 7, blade_point, 1, (0.09, z0 - z1))
bmesh.ops.remove_doubles(shirt, verts=shirt.verts, dist=0.0005)
me = bpy.data.meshes.new("shirt_and_tie")
shirt.to_mesh(me)
obj = bpy.data.objects.new(PREFIX.replace("\\", "/").split("/")[-1], me)
bpy.context.scene.collection.objects.link(obj)
for name, col in (("M_shirt", (0.86, 0.88, 0.90, 1)), ("M_tie", (0.32, 0.08, 0.10, 1))):
    m = bpy.data.materials.new(name)
    m.diffuse_color = col
    me.materials.append(m)
for p in me.polygons:
    p.use_smooth = True
# the shirt and tie bound to the body's skeleton like the body (each point the body's nearest point's weights)
mod = obj.modifiers.new("Armature", "ARMATURE")
mod.object = arm
groups = {g.index: g.name for g in body.vertex_groups}
kd_src = [body.matrix_world @ v.co for v in body.data.vertices]
from mathutils.kdtree import KDTree  # noqa: E402
kd = KDTree(len(kd_src))
for i, c in enumerate(kd_src):
    kd.insert(c, i)
kd.balance()
for v in me.vertices:
    _, i, _ = kd.find(obj.matrix_world @ v.co)
    for g in body.data.vertices[i].groups:
        if g.weight > 0.01:
            vg = obj.vertex_groups.get(groups[g.group]) or obj.vertex_groups.new(name=groups[g.group])
            vg.add([v.index], g.weight, "REPLACE")
print("SHIRT", {"points": len(me.vertices), "faces": len(me.polygons), "front": [round(TOP, 3), round(BOT, 3)],
                "tie": [round(z0, 3), round(z1, 3)]}, flush=True)
bpy.ops.object.select_all(action="DESELECT")
obj.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_scene.fbx(filepath=PREFIX + ".fbx", use_selection=True, object_types={"ARMATURE", "MESH"},
                         add_leaf_bones=False, global_scale=1.0, apply_unit_scale=True, bake_anim=False,
                         mesh_smooth_type="FACE")
if WITH_BODY:
    # the avatar for Marvelous: the body's own skin pushed out to the shirt's and tie's surface where they cover it
    # (the farthest within 3.5 cm along the skin's normal), so the jacket lies on a shirted body with no loose edges.
    # (The shirt as separate panels joined to the body let the jacket's fronts slide under the shirt front's edges
    # as the body grew, and the jacket stayed open.)
    sb = bmesh.new()
    sb.from_object(obj, bpy.context.evaluated_depsgraph_get())
    sb.transform(obj.matrix_world)
    SB = BVHTree.FromBMesh(sb)
    mw = body.matrix_world
    inv = mw.inverted()
    nmat = mw.to_3x3()
    moved = 0
    orig = [v.co.copy() for v in body.data.vertices]
    for v in body.data.vertices:
        w = mw @ v.co
        n = (nmat @ v.normal).normalized()
        best, start, left = None, w, 0.035
        while left > 0:
            hit = SB.ray_cast(start + n * 1e-4, n, left)
            if hit[0] is None:
                break
            best = hit[0]
            left -= (hit[0] - start).length + 1e-4
            start = hit[0]
        if best is not None:
            v.co = inv @ best
            moved += 1
    body.data.update()
    # the pushed skin smoothed among itself (rays meeting the collar's edge side-on threw spikes that came through
    # the jacket's collar and chest)
    bmb = bmesh.new()
    bmb.from_mesh(body.data)
    pushed = [v for v, o in zip(bmb.verts, orig) if (v.co - o).length > 1e-5]
    for _ in range(6):
        bmesh.ops.smooth_vert(bmb, verts=pushed, factor=0.6, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    bmb.to_mesh(body.data)
    body.data.update()
    print("AVATAR skin pushed out under the shirt and tie:", moved, "points", flush=True)
    bpy.ops.object.select_all(action="DESELECT")
    body.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.export_scene.fbx(filepath=PREFIX + "-avatar.fbx", use_selection=True, object_types={"ARMATURE", "MESH"},
                             add_leaf_bones=False, global_scale=1.0, apply_unit_scale=True, bake_anim=False,
                             mesh_smooth_type="FACE")
print("WROTE", PREFIX, flush=True)
