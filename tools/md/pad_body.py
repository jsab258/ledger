"""A MetaHuman body made into the tailor's form a jacket is draped on in Marvelous Designer: light shoulder pads.

    blender -b -P tools/md/pad_body.py -- FULLBODY.fbx OUT.fbx [--pad 0.012] [--lod 0]

WHY, 1 October (Jafar's Marvelous proof: "soft shoulders"; a 1990 suit's shoulder is lightly padded, the research
says, production/research/clothing-pipeline/MD-TAILORED-JACKET-2026-10-01.md: "a rigid shoulder-pad object ... its
shape stays in the drape"; Marvelous has no script call for shoulder pads). The pad is built into the body the jacket
is draped on: the skin round each shoulder point raised by --pad metres at the point, falling smoothly to nothing over
--pad-r metres, more along the shoulder line than down the arm, so the cloth drapes over a padded shoulder and keeps
that shape. The rest of the body is as exported (Marvelous makes its own smooth fitting suit over it). Written as
FBX in centimetres with its skeleton, as the builder exports bodies.
"""
import math
import sys

import bpy
import numpy as np
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT = argv[0], argv[1]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


PAD, PAD_R = opt("--pad", 0.012), opt("--pad-r", 0.09)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
meshes = sorted([o for o in bpy.data.objects if o.type == "MESH"], key=lambda o: -len(o.data.vertices))
lod = opt("--lod", 0, int)
keep = next((o for o in meshes if o.name.endswith("_LOD%d" % lod)), meshes[0])
for o in meshes:
    if o is not keep:
        bpy.data.objects.remove(o, do_unlink=True)
J = lambda n: arm.matrix_world @ arm.pose.bones[n].head  # noqa: E731
mw = keep.matrix_world
inv = mw.inverted()
me = keep.data
moved = 0
for s in "lr":
    sp = J("upperarm_" + s)
    neck = J("neck_01")
    along = (sp - neck)
    along.z = 0
    along.normalize()                     # the shoulder line, outward
    centre = sp + Vector((0, 0, 0.035)) - along * 0.02
    for v in me.vertices:
        w = mw @ v.co
        d = w - centre
        a = d.dot(along)
        # an ellipse: long along the shoulder line, shorter down the front and back, short down the arm
        r = math.sqrt((a / (PAD_R * (1.0 if a < 0 else 0.6))) ** 2 + (d.y / (PAD_R * 0.85)) ** 2 + (min(0.0, d.z) / (PAD_R * 0.5)) ** 2)
        if r >= 1.0 or w.z < sp.z - 0.06:
            continue
        t = 1.0 - r
        t = t * t * (3 - 2 * t)
        n = (mw.to_3x3() @ v.normal).normalized()
        v.co = inv @ (w + n * PAD * t)
        moved += 1
me.update()
print("PAD", {"points": moved, "padMm": PAD * 1000, "radiusMm": PAD_R * 1000, "lod": keep.name}, flush=True)
bpy.ops.object.select_all(action="DESELECT")
keep.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = keep
bpy.ops.export_scene.fbx(filepath=OUT, use_selection=True, object_types={"ARMATURE", "MESH"}, add_leaf_bones=False,
                         global_scale=1.0, apply_unit_scale=True, bake_anim=False, mesh_smooth_type="FACE")
