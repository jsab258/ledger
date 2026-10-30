"""A pair of boots or shoes seen with its baked maps, through the garment material's own ID tints, under a soft light.

    blender -b --factory-startup -P tools/meshgen/blender/look_footwear_maps.py -- SKINNED.fbx MAPS_DIR MAPS_NAME OUT_DIR
        [--tag tom] [--tint 0.032,0.032,0.034] [--tape 0.045,0.045,0.045] [--teeth 0.16,0.155,0.15]
        [--body BODY.blend --body-object NAME] [--hide-below 0.125] [--dist 1,3] [--samples 64] [--lens 35]
        [--res 1600,1000] [--flat] [--cull]

WHY, 30 October 2026 (Ron's and Tom's boots given maps by footwear_maps.py): the maps judged on the pair as the game
draws it. The material is tools/ue/import_garments.py's M_LedgerGarmentPacked rebuilt in Blender: base colour the
colour map times Tint where the packed map's G is 0, times TapeColour at 0.5, the flat TeethColour at 0.75 (each part
by saturate(1 - |G - v| x 8)), roughness R, metal B, the normal map (OpenGL green here; Unreal reads the DirectX copy);
the occlusion in the colour map's alpha multiplied into the base colour, as look_baked.py does. --flat draws the pair
with its old flat slot colours instead, for the before picture. Lit by a grey sky and one large soft key, on a grey
floor (--cull: faces seen from behind see-through, as the game's one-sided material draws them); the body (if given) with its feet hidden under the boots, as the game hides them. Views: front three-quarter,
side (the outside of the left boot) and back, the camera at each --dist metres from the pair, 25 degrees above it.
"""
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
FBX, MAPS, MNAME, OUT = argv[:4]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
vec = lambda s: tuple(float(x) for x in s.split(","))  # noqa: E731
TAG = opt("--tag", "look", str)
TINT = vec(opt("--tint", "0.032,0.032,0.034", str))
TAPE = vec(opt("--tape", "0.045,0.045,0.045", str))
TEETH = vec(opt("--teeth", "0.16,0.155,0.15", str))
BODY = opt("--body", "", str)
BODY_OBJ = opt("--body-object", "", str)
HIDE = opt("--hide-below", 0.125)
DISTS = vec(opt("--dist", "1,3", str))
SAMPLES = opt("--samples", 64, int)
LENS = opt("--lens", 35.0)
RES = [int(x) for x in vec(opt("--res", "1600,1000", str))]
FLAT = "--flat" in argv
CULL = "--cull" in argv        # faces seen from behind drawn see-through, as the game's one-sided material culls them
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=FBX)
pair = next(o for o in bpy.data.objects if o.type == "MESH")
for m_ in pair.modifiers:
    m_.show_render = m_.show_viewport = False                 # the reference pose, undeformed
co = np.array([pair.matrix_world @ v.co for v in pair.data.vertices])
lo, hi = co.min(axis=0), co.max(axis=0)
CEN = Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2] + 0.06))
FLOOR = float(lo[2])


def tex(nt, path, colour):
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = bpy.data.images.load(path)
    t.image.colorspace_settings.name = "sRGB" if colour else "Non-Color"
    t.image.alpha_mode = "CHANNEL_PACKED"
    t.interpolation = "Cubic"
    return t


def math_(nt, op, a, b=None, clamp=False):
    n = nt.nodes.new("ShaderNodeMath")
    n.operation = op
    n.use_clamp = clamp
    for i, x in enumerate((a, b)):
        if x is None:
            continue
        if isinstance(x, (int, float)):
            n.inputs[i].default_value = x
        else:
            nt.links.new(x, n.inputs[i])
    return n.outputs[0]


def mix_rgb(nt, fac, a, b, blend="MIX"):
    n = nt.nodes.new("ShaderNodeMix")
    n.data_type = "RGBA"
    n.blend_type = blend
    for slot, x in ((0, fac), (6, a), (7, b)):
        if isinstance(x, tuple):
            n.inputs[slot].default_value = (*x, 1.0) if slot else x[0]
        elif isinstance(x, (int, float)):
            n.inputs[slot].default_value = x
        else:
            nt.links.new(x, n.inputs[slot])
    return n.outputs[2]


if not FLAT:
    m = bpy.data.materials.new("M_LedgerGarmentPacked_look")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    c = tex(nt, os.path.join(MAPS, MNAME + "_colour_ao.png"), True)
    p = tex(nt, os.path.join(MAPS, MNAME + "_packed.png"), False)
    nmt = tex(nt, os.path.join(MAPS, MNAME + "_normal_gl.png"), False)
    p.interpolation = "Closest"                            # the ID point-sampled, as a mask
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(p.outputs["Color"], sep.inputs[0])

    def is_part(v):
        d = math_(nt, "SUBTRACT", sep.outputs[1], v)
        d = math_(nt, "ABSOLUTE", d)
        d = math_(nt, "MULTIPLY", d, 8.0)
        return math_(nt, "SUBTRACT", 1.0, d, clamp=True)

    cloth = mix_rgb(nt, 1.0, c.outputs["Color"], TINT, "MULTIPLY")
    tapec = mix_rgb(nt, 1.0, c.outputs["Color"], TAPE, "MULTIPLY")
    l1 = mix_rgb(nt, is_part(0.5), cloth, tapec)
    l2 = mix_rgb(nt, is_part(0.75), l1, TEETH)
    base = mix_rgb(nt, 1.0, l2, c.outputs["Alpha"], "MULTIPLY")
    nt.links.new(base, bsdf.inputs["Base Color"])
    rsep = nt.nodes.new("ShaderNodeSeparateColor")
    p2 = tex(nt, os.path.join(MAPS, MNAME + "_packed.png"), False)
    nt.links.new(p2.outputs["Color"], rsep.inputs[0])
    nt.links.new(rsep.outputs[0], bsdf.inputs["Roughness"])
    nt.links.new(sep.outputs[2], bsdf.inputs["Metallic"])
    nmap = nt.nodes.new("ShaderNodeNormalMap")
    nmap.uv_map = pair.data.uv_layers[0].name
    nt.links.new(nmt.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs[0], bsdf.inputs["Normal"])
    if CULL:
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(geo.outputs["Backfacing"], mx.inputs[0])
        nt.links.new(bsdf.outputs[0], mx.inputs[1])
        nt.links.new(tr.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], out.inputs[0])
    nslots = len(pair.data.materials)
    pair.data.materials.clear()
    for _ in range(max(1, nslots)):
        pair.data.materials.append(m)

if BODY:
    with bpy.data.libraries.load(BODY, link=False) as (src, dst):
        dst.objects = [n for n in src.objects if n in (BODY_OBJ, "root")]
    for o in dst.objects:
        bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.update()
    for o in [o for o in dst.objects if o.type == "MESH"]:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
        for m_ in list(o.modifiers):
            o.modifiers.remove(m_)
        g = o.vertex_groups.new(name="shown")
        g.add([v.index for v in o.data.vertices if (o.matrix_world @ v.co).z >= HIDE], 1.0, "REPLACE")
        mk = o.modifiers.new("feet_hidden", "MASK")
        mk.vertex_group = "shown"
        clay = bpy.data.materials.new("clay")
        clay.use_nodes = True
        clay.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.18, 0.17, 0.16, 1)
        clay.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.6
        o.data.materials.clear()
        o.data.materials.append(clay)
    for o in [o for o in dst.objects if o.type != "MESH"]:
        bpy.data.objects.remove(o, do_unlink=True)

# the floor, the sky, the key
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, FLOOR - 0.0005))
fl = bpy.context.active_object
fm = bpy.data.materials.new("floor")
fm.use_nodes = True
fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.30, 0.30, 0.30, 1)
fm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
fl.data.materials.append(fm)
scn = bpy.context.scene
scn.render.engine = "CYCLES"
scn.cycles.device = "CPU"
scn.cycles.samples = SAMPLES
scn.cycles.use_denoising = True
scn.render.resolution_x, scn.render.resolution_y = RES
scn.view_settings.view_transform = "AgX"
scn.view_settings.look = "None"
w = bpy.data.worlds.new("sky")
scn.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.60, 0.62, 0.66, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.35
key = bpy.data.objects.new("key", bpy.data.lights.new("key", "AREA"))
key.data.shape, key.data.size = "DISK", 2.0
key.data.energy = 220.0
scn.collection.objects.link(key)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
cam.data.lens = LENS
scn.collection.objects.link(cam)
scn.camera = cam
VIEWS = (("three-quarter", math.radians(-40)), ("side", math.radians(0)), ("back", math.radians(180)))
EL = math.radians(25)
for dist in DISTS:
    for vn, az in VIEWS:
        # azimuth from the figure's front (-y); 0 for the side is the left boot's outside (+x)
        if vn == "side":
            d = Vector((1.0, 0.0, 0.0))
        else:
            d = Vector((math.sin(az), -math.cos(az), 0.0))
        loc = CEN + d * dist * math.cos(EL) + Vector((0, 0, dist * math.sin(EL)))
        cam.location = loc
        cam.rotation_euler = (CEN - loc).to_track_quat("-Z", "Y").to_euler()
        side_ = Vector((-d.y, d.x, 0.0))
        key.location = CEN + d * 2.2 + side_ * 1.4 + Vector((0, 0, 2.2))
        key.rotation_euler = (CEN - key.location).to_track_quat("-Z", "Y").to_euler()
        scn.render.filepath = os.path.join(OUT, "%s_%s_%gm.png" % (TAG, vn, dist))
        bpy.ops.render.render(write_still=True)
        print("LOOKED", scn.render.filepath, flush=True)
