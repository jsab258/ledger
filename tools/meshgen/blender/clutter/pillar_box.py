"""The 1990 pillar box, by script: an EIIR Type B (Carron), at real size.

    blender --background --factory-startup --python tools/meshgen/blender/clutter/pillar_box.py -- --out F:/LedgerTools/tmp/clutter/pillar-box/script-1.glb

The script route of the builder's list, item 10 (the live route is
tools/blender-live/live_piece.py). Its form comes from the research
(production/research/street-clutter-1990) and two photographs of EIIR Type B
boxes by Carron (Liverpool 2020, Haydock 2021; links in the brief), measured
from the first on the body's 39 cm diameter: 1.48 m above the pavement, a
24 cm black base, the cap's rim band 54 cm across, the hooded slot centred
1.17 m up, the collection plate below it. Front faces -y.

NO CIPHER, CROWN OR LETTERING YET (29 September): canon makes every brand
fictional and lists the postal cypher as owed by the brand bible, so the real
EIIR and POST OFFICE are not cast on; the door is left plain where they go
(0.30 to 0.62 m) until Jafar mints them, and relief_text() is kept for then.
"""
import math
import sys

import bmesh
import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "pillar-box.glb"
R = 0.195                       # the body's radius

bpy.ops.wm.read_factory_settings(use_empty=True)


def material(name, rgb, rough=0.5, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


def srgb(r, g, b):
    f = lambda c: (c / 255.0) ** 2.2
    return (f(r), f(g), f(b))


RED = material("pillar-red", srgb(190, 30, 35), 0.45)
BLACK = material("base-black", srgb(20, 20, 20), 0.5)
WHITE = material("plate-white", srgb(235, 235, 228), 0.4)
DARK = material("slot-dark", srgb(8, 8, 8), 0.9)
INK = material("plate-ink", srgb(40, 40, 45), 0.6)


def lathe(name, profile, mat, segments=40):
    """A solid of revolution from (radius, z) points, bottom to top, closed at both ends."""
    bm = bmesh.new()
    rings = []
    for r, z in profile:
        ring = []
        for i in range(segments):
            a = 2 * math.pi * i / segments
            ring.append(bm.verts.new((r * math.cos(a), r * math.sin(a), z)))
        rings.append(ring)
    for k in range(len(rings) - 1):
        for i in range(segments):
            j = (i + 1) % segments
            bm.faces.new((rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def box(name, size, loc, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.scale = size
    bpy.ops.object.transform_apply(scale=True)
    ob.data.materials.append(mat)
    return ob


def wrap_front(ob, radius):
    """Bends a flat relief (made facing -y, its back at y = 0) round the body's curve:
    each vertex keeps its depth in front of the surface at its own x."""
    for v in ob.data.vertices:
        w = ob.matrix_world @ v.co
        depth = -w.y
        yy = -math.sqrt(max(radius * radius - w.x * w.x, 0.0)) - depth
        v.co = ob.matrix_world.inverted() @ type(w)((w.x, yy, w.z))


def panel(name, w, d, h, zc, mat, over=0.0, cuts=14):
    """A flat panel (w wide, d proud, h tall) centred at height zc, bent round the body so its
    back lies on the surface (plus `over`) and its face stays d in front of it everywhere."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, zc))
    ob = bpy.context.object
    ob.name = name
    ob.scale = (w, d, h)
    bpy.ops.object.transform_apply(location=False, scale=True)
    for v in ob.data.vertices:
        v.co.y -= d / 2                # its back at y = 0, its face at y = -d
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    for i in range(1, cuts):
        x = -w / 2 + w * i / cuts
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(x, 0, 0), plane_no=(1, 0, 0))
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.materials.append(mat)
    wrap_front(ob, R + over)
    return ob


def relief_text(name, text, size, z, depth, mat):
    bpy.ops.object.text_add(location=(0, 0, z), rotation=(math.radians(90), 0, 0))
    t = bpy.context.object
    t.data.body = text
    t.data.size = size
    t.data.extrude = depth / 2
    t.data.align_x = "CENTER"
    t.data.align_y = "CENTER"
    bpy.ops.object.convert(target="MESH")
    ob = bpy.context.object
    ob.name = name
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    # the text's back face onto y = 0
    ymax = max(v.co.y for v in ob.data.vertices)
    for v in ob.data.vertices:
        v.co.y -= ymax
    ob.data.materials.append(mat)
    wrap_front(ob, R + 0.004)
    return ob


# THE SILHOUETTE, turned: base, body, ring moulding, collar, cap rim, shallow dome.
lathe("base", [(0.21, 0.0), (0.21, 0.24), (0.196, 0.24)], BLACK)
lathe("body", [(R, 0.235), (R, 1.30), (0.22, 1.30), (0.22, 1.33), (0.205, 1.34),
               (0.215, 1.355), (0.245, 1.372), (0.27, 1.38), (0.27, 1.46), (0.262, 1.462),
               (0.22, 1.472), (0.12, 1.479), (0.0, 1.48)], RED, segments=48)

# THE BEADS round the cap's rim band.
for i in range(36):
    a = 2 * math.pi * i / 36
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.008, segments=6, ring_count=4,
                                         location=(0.272 * math.cos(a), 0.272 * math.sin(a), 1.42))
    bpy.context.object.data.materials.append(RED)

# THE DOOR: a raised panel following the curve, 0.30 to 1.22 m.
panel("door", 0.30, 0.003, 0.92, 0.76, RED, over=-0.001)

# THE SLOT: surround, dark opening, hood.
# the surround follows the body's curve, 1.5 cm proud, as on the photographs
panel("slot-surround", 0.25, 0.015, 0.09, 1.17, RED)
panel("slot", 0.20, 0.002, 0.03, 1.165, DARK, over=0.015)
panel("hood", 0.23, 0.025, 0.012, 1.19, RED, over=0.004)
panel("tablet", 0.05, 0.012, 0.05, 1.245, WHITE, cuts=2)

# THE COLLECTION PLATE: frame, white plate, lines of small print.
panel("plate-frame", 0.19, 0.014, 0.26, 0.95, RED, over=0.004)
panel("plate", 0.17, 0.004, 0.24, 0.95, WHITE, over=0.016)
for k, (zz, w) in enumerate(((1.045, 0.12), (1.03, 0.08), (1.0, 0.13), (0.985, 0.13), (0.97, 0.10),
                             (0.93, 0.08), (0.915, 0.13), (0.88, 0.12), (0.865, 0.07))):
    panel("print-%d" % k, w, 0.001, 0.008, zz, INK, over=0.0195, cuts=6)

# THE LOCK PLATE at the door's right edge.
box("lock", (0.03, 0.016, 0.05), (0.13, -0.152, 0.80), RED)

# ONE OBJECT PER MATERIAL IS PLENTY: join everything, apply, export.
bpy.ops.object.select_all(action="SELECT")
bpy.context.view_layer.objects.active = bpy.data.objects["body"]
bpy.ops.object.join()
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
tris = sum(len(p.vertices) - 2 for p in bpy.context.object.data.polygons)
print("pillar_box triangles:", tris)
bpy.ops.export_scene.gltf(filepath=OUT)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace(".glb", ".blend"))
print("pillar_box written:", OUT)
