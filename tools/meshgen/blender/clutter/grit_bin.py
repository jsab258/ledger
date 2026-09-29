"""The council grit bin of a northern street in winter, by script, at real size.

    blender --background --factory-startup --python tools/meshgen/blender/clutter/grit_bin.py -- --out F:/LedgerTools/tmp/clutter/grit-bin/script-1.glb

The script route of the builder's list, item 10. From the research
(production/research/street-clutter-1990: a yellow glass-fibre bin with a
hinged lid, marked GRIT, about 0.7 m tall, 0.9 m wide, 0.6 m deep; whether
glass-fibre had displaced the older concrete and timber bins by 1990 is
uncertain, and the page says so): a slightly tapered body, a sloping hinged
lid with a lip, GRIT in raised capitals on the front.
"""
import sys

import bmesh
import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "grit-bin.glb"

bpy.ops.wm.read_factory_settings(use_empty=True)


def srgb(r, g, b):
    f = lambda c: (c / 255.0) ** 2.2
    return (f(r), f(g), f(b))


def material(name, rgb, rough=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    b.inputs["Roughness"].default_value = rough
    return m


YELLOW = material("grit-yellow", srgb(232, 180, 20), 0.55)       # weathered safety yellow
BLACK = material("grit-black", srgb(25, 25, 25), 0.6)


def hull(name, bottom, top, mat):
    """A box from a bottom rectangle (w, d, z) to a top quad of four (x, y, z) corners."""
    bm = bmesh.new()
    w, d, z = bottom
    b = [bm.verts.new(v) for v in ((-w / 2, -d / 2, z), (w / 2, -d / 2, z), (w / 2, d / 2, z), (-w / 2, d / 2, z))]
    t = [bm.verts.new(v) for v in top]
    bm.faces.new(list(reversed(b)))
    bm.faces.new(t)
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((b[i], b[j], t[j], t[i]))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    return ob


# THE BODY: 0.80 by 0.52 at the foot, widening to 0.90 by 0.60 at 0.58 m.
hull("body", (0.80, 0.52, 0.0), ((-0.45, -0.30, 0.58), (0.45, -0.30, 0.58), (0.45, 0.30, 0.66), (-0.45, 0.30, 0.66)), YELLOW)
# THE LID: sloping, front lower than back, overhanging 3 cm all round, 4 cm thick.
hull("lid", (0.0, 0.0, 0.0), ((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)), YELLOW)
bpy.data.objects.remove(bpy.data.objects["lid"])
bm = bmesh.new()
lo = [(-0.48, -0.33, 0.575), (0.48, -0.33, 0.575), (0.48, 0.33, 0.66), (-0.48, 0.33, 0.66)]
vs = [bm.verts.new(v) for v in lo] + [bm.verts.new((x, y, z + 0.04)) for x, y, z in lo]
bm.faces.new(list(reversed(vs[:4])))
bm.faces.new(vs[4:])
for i in range(4):
    j = (i + 1) % 4
    bm.faces.new((vs[i], vs[j], vs[4 + j], vs[4 + i]))
me = bpy.data.meshes.new("lid")
bm.to_mesh(me)
bm.free()
lid = bpy.data.objects.new("lid", me)
bpy.context.scene.collection.objects.link(lid)
lid.data.materials.append(YELLOW)
# A front lip to lift the lid by, and two hinge knuckles at the back.
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.335, 0.585))
bpy.context.object.scale = (0.22, 0.03, 0.03)
bpy.context.object.data.materials.append(YELLOW)
for x in (-0.3, 0.3):
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.018, depth=0.08, location=(x, 0.33, 0.665), rotation=(0, 1.5708, 0))
    bpy.context.object.data.materials.append(BLACK)
# GRIT, raised on the front face.
bpy.ops.object.text_add(location=(0, -0.2868, 0.33), rotation=(1.5708 - 0.069, 0, 0))   # the face slopes 0.04 m in 0.58 m
t = bpy.context.object
t.data.body = "GRIT"
t.data.size = 0.17
t.data.extrude = 0.006
t.data.offset = 0.004
t.data.align_x = "CENTER"
t.data.align_y = "CENTER"
bpy.ops.object.convert(target="MESH")
bpy.context.object.data.materials.append(BLACK)

bpy.ops.object.select_all(action="SELECT")
bpy.context.view_layer.objects.active = bpy.data.objects["body"]
bpy.ops.object.join()
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
print("grit_bin triangles:", sum(len(p.vertices) - 2 for p in bpy.context.object.data.polygons))
bpy.ops.export_scene.gltf(filepath=OUT)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace(".glb", ".blend"))
print("grit_bin written:", OUT)
