"""Pictures of a game-mesh garment on its body, as the game draws it: its baked colour and normal map, rendered by
Cycles on the processor (short: --samples, small pictures), for the gate's reviewer.

    blender -b -P tools/meshgen/blender/look_garment.py -- GARMENT.blend OUT_PREFIX --garment ron_donkey [--hide Name,Name]

OUT_PREFIX-front.png, -back.png, -side.png, -three-quarter.png, and close views of the chest, the back's yoke and a
shoulder (-close-front, -close-back, -close-side).
"""
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, PREFIX = argv[0], argv[1]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


bpy.ops.wm.open_mainfile(filepath=BLEND)
g = bpy.data.objects[opt("--garment", "garment", str)]
hide = set(opt("--hide", "", str).split(",")) - {""}
for o in bpy.data.objects:
    if o.type == "MESH":
        o.hide_render = not (o is g or "Body" in o.name) or o.name in hide
body = next((o for o in bpy.data.objects if o.type == "MESH" and "Body" in o.name and not o.hide_render), None)
# --hide-covered M: the body's faces the garment always covers (within M metres of it) hidden, as the game hides them
# (MetaHuman's hidden-face map); what shows then is what a player sees
if body is not None and "--hide-covered" in argv:
    import bmesh
    from mathutils.bvhtree import BVHTree
    GT = BVHTree.FromObject(g, bpy.context.evaluated_depsgraph_get())
    arm_ = next(o for o in bpy.data.objects if o.type == "ARMATURE")
    Jh = lambda n: arm_.matrix_world @ arm_.pose.bones[n].head  # noqa: E731
    neck_z = Jh("neck_01").z - 0.02
    hem_z = min((g.matrix_world @ v.co).z for v in g.data.vertices) + 0.04     # below the hem nothing is covered
    hands_ = [Jh("hand_l"), Jh("hand_r")]
    near_ = []
    for v in body.data.vertices:
        w_ = body.matrix_world @ v.co
        if w_.z > neck_z or w_.z < hem_z or min((w_ - h_).length for h_ in hands_) < 0.12:
            continue                          # the neck and hands always show
        d_ = GT.find_nearest(w_)[3]
        if d_ is not None and d_ < opt("--hide-covered", 0.025):
            near_.append(v.index)
    vg_ = body.vertex_groups.new(name="_shown")
    vg_.add([i for i in range(len(body.data.vertices)) if i not in set(near_)], 1.0, "REPLACE")
    mk = body.modifiers.new("Covered", "MASK")
    mk.vertex_group = "_shown"
if body is not None:
    body.data.materials.clear()
    body.data.materials.append(tailor.material("M_Skin", tuple(float(c) for c in opt("--body-rgb", "0.55,0.42,0.36", str).split(",")), 0.6))
scn = bpy.context.scene
scn.render.engine = "CYCLES"
scn.cycles.device = "CPU"
scn.cycles.samples = opt("--samples", 24, int)
scn.cycles.use_denoising = True
scn.view_settings.view_transform = "Standard"
world = scn.world or bpy.data.worlds.new("World")
scn.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs["Color"].default_value = (0.72, 0.72, 0.74, 1)
bg.inputs["Strength"].default_value = 0.9
for name, rot, energy in (("Key", (0.9, 0.2, 0.6), 3.5), ("Fill", (1.1, 0.0, -2.2), 1.2), ("Rim", (0.8, 0.0, 3.0), 2.0)):
    L = bpy.data.objects.get(name)
    if L is None:
        L = bpy.data.objects.new(name, bpy.data.lights.new(name, "SUN"))
        scn.collection.objects.link(L)
    L.data.energy = energy
    L.rotation_euler = rot
res = tuple(int(x) for x in opt("--res", "600,760", str).split(","))


def pictures(prefix, centre, views, res, lens=60):
    """tailor.pictures, drawn by Cycles (tailor's are Workbench, which shows no normal map)."""
    cam = scn.camera
    if cam is None:
        cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
        scn.collection.objects.link(cam)
        scn.camera = cam
    cam.data.lens = lens
    scn.render.resolution_x, scn.render.resolution_y = res
    for label, off in views:
        cam.location = centre + Vector(off)
        cam.rotation_euler = (centre - cam.location).to_track_quat("-Z", "Y").to_euler()
        scn.render.filepath = "%s-%s.png" % (prefix, label)
        bpy.ops.render.render(write_still=True)


c = Vector((0, 0, opt("--centre-z", 1.2)))
pictures(PREFIX, c, views=(("front", (0, -2.9, 0.15)), ("back", (0, 2.9, 0.15)), ("side", (2.9, 0, 0.15)),
                                  ("three-quarter", (2.0, -2.1, 0.35))), res=res)
pictures(PREFIX + "-close", Vector((0, 0, 1.4)), views=(("front", (0, -1.25, 0.05)), ("back", (0, 1.25, 0.05)),
                                                               ("side", (1.0, 0.75, 0.05))), res=res)
