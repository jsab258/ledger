"""The zip jacket's game mesh baked: its normal map from the drape and the floaters, its occlusion, and one packed map
holding roughness, the parts' ID and metal.

    blender -b --factory-startup -P tools/meshgen/blender/zip_bake.py -- LOW.blend OUT_DIR [--name zip_jacket]
        [--tex 2048] [--cage 0.008] [--ao-samples 64]

WHY, 27 October 2026 (Tom's zip jacket, the bake chain's step 7: production/art/clothing/tom-outfit/
BAKE-PLAN-2026-10-27.md). The game mesh ("Low", its "UVMap" from uv_pack_low.py) takes the drape's folds and the
floaters' teeth, stops and welts (zip_floaters.py) as a normal map; their occlusion, the body hidden (the game
shades the body against the cloth itself), goes into the colour map's alpha; and SPEC's three maps stay three: the
third packs roughness (R), the parts' ID (G: cloth 0, rib 0.25, tape 0.5, teeth and stops 0.75, welt 1; snapped to
those five values, never blurred, so a material can switch on it) and metal (B, the teeth and stops).

The jacket's colour is not chosen yet (a taste decision for his page): the colour map is the parts' neutral greys,
which the material tints, with the occlusion beside them.

Writes NAME_normal_dx.png (green flipped, for Unreal) and NAME_normal_gl.png, NAME_colour_ao.png (RGB greys, A
occlusion), NAME_packed.png and bake.json (the share of the layout's pixels whose rays found the drape, each ID
value's share of the layout against the low mesh's own areas, the time).
"""
import json
import math
import os
import sys
import time

import bmesh
import bpy
import numpy as np
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
LOW, OUT = argv[0], argv[1]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
NAME = opt("--name", "zip_jacket", str)
TEX = opt("--tex", 2048, int)
CAGE = opt("--cage", 0.008)
AO_SAMPLES = opt("--ao-samples", 64, int)
os.makedirs(OUT, exist_ok=True)
t0 = time.time()
log = {"low": LOW, "tex": TEX, "checks": {}}
ID = {"Shell": 0.0, "Rib": 0.25, "Tape": 0.5, "Teeth": 0.75, "Stop": 0.75, "Welt": 1.0}
ROUGH = {0.0: 0.82, 0.25: 0.88, 0.5: 0.78, 0.75: 0.35, 1.0: 0.80}
GREY = {0.0: 0.55, 0.25: 0.50, 0.5: 0.45, 0.75: 0.70, 1.0: 0.50}

bpy.ops.wm.open_mainfile(filepath=LOW)
low = bpy.data.objects["Low"]
drape = bpy.data.objects["Jacket"]
floaters = [bpy.data.objects[n] for n in ("Teeth", "Stops", "Welts")]
for o in bpy.data.objects:
    if o.type == "MESH" and o.name not in ("Low", "Jacket", "Teeth", "Stops", "Welts"):
        o.hide_render = True
        o.hide_set(True)
drape.hide_render = False
axis = sum((drape.matrix_world @ v.co for v in drape.data.vertices), Vector()) / len(drape.data.vertices)


def face_outward(o):
    """All of a sheet's faces turned to face away from the garment's axis (by their majority)."""
    bm = bmesh.new()
    bm.from_mesh(o.data)
    # one winding across the whole sheet first (the first bake: the pieces' grids were wound both ways, so one flip of
    # the whole could not turn them all out; the zip's tapes faced in and the rays met the cloth before the teeth)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.normal_update()
    mw = o.matrix_world
    votes = 0
    for f in bm.faces:
        c = mw @ f.calc_center_median()
        away = Vector((c.x - axis.x, c.y - axis.y, 0.0))
        votes += 1 if (mw.to_3x3() @ f.normal).dot(away) >= 0 else -1
    flipped = votes < 0
    if flipped:
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
    bm.to_mesh(o.data)
    bm.free()
    return flipped


# the floaters too (the first look: the welts' lips were wound inward, their shading and occlusion read from inside
# and they baked as black slashes), and the game mesh smooth-shaded as the game draws it (baked flat and drawn smooth,
# the cloth showed its grid as quilting)
log["flipped"] = {o.name: face_outward(o) for o in [low, drape] + floaters}
for poly in low.data.polygons:
    poly.use_smooth = True

# the source: the drape and the floaters joined into one object (a copy; the file is not saved over)
srcs = []
for o in [drape] + floaters:
    c = o.copy()
    c.data = o.data.copy()
    bpy.context.scene.collection.objects.link(c)
    srcs.append(c)
for o in bpy.context.view_layer.objects:
    o.select_set(False)
for c in srcs:
    c.select_set(True)
bpy.context.view_layer.objects.active = srcs[0]
bpy.ops.object.join()
src = bpy.context.view_layer.objects.active
src.name = "BakeSource"
for o in [drape] + floaters:
    o.hide_render = True
    o.hide_set(True)

scn = bpy.context.scene
scn.render.engine = "CYCLES"
scn.cycles.device = "CPU"
scn.render.bake.use_selected_to_active = True
scn.render.bake.use_cage = False
scn.render.bake.cage_extrusion = CAGE
scn.render.bake.max_ray_distance = 0.0
scn.render.bake.margin = 8
low.data.uv_layers.active = low.data.uv_layers["UVMap"]


def target_image(label, colour=False):
    im = bpy.data.images.new(NAME + label, TEX, TEX, alpha=True, float_buffer=True)
    im.colorspace_settings.name = "sRGB" if colour else "Non-Color"
    for m in low.data.materials:
        m.use_nodes = True
        nt = m.node_tree
        node = next((n for n in nt.nodes if n.type == "TEX_IMAGE" and n.name == "bake_target"), None) or nt.nodes.new("ShaderNodeTexImage")
        node.name = "bake_target"
        node.image = im
        nt.nodes.active = node
    return im


def set_emission(o, values):
    """Each of the object's materials made to glow at its value (grey), lit by nothing else."""
    saved = []
    for m in o.data.materials:
        m.use_nodes = True
        b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        saved.append((b, tuple(b.inputs["Emission Color"].default_value), b.inputs["Emission Strength"].default_value))
        v = values(m.name.split(".")[0])
        b.inputs["Emission Color"].default_value = (v, v, v, 1.0)
        b.inputs["Emission Strength"].default_value = 1.0
    return saved


def unset(saved):
    for b, c, s in saved:
        b.inputs["Emission Color"].default_value = c
        b.inputs["Emission Strength"].default_value = s


def bake(kind, im, samples=4):
    scn.cycles.samples = samples
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    src.select_set(True)
    low.select_set(True)
    bpy.context.view_layer.objects.active = low
    bpy.ops.object.bake(type=kind)
    return np.array(im.pixels[:], dtype=np.float32).reshape(TEX, TEX, 4)


# the layout's own pixels (the low mesh's islands), for the shares
mask_im = target_image("_mask")
saved = set_emission(low, lambda n: 1.0)
scn.render.bake.use_selected_to_active = False
scn.cycles.samples = 1
for o in bpy.context.view_layer.objects:
    o.select_set(False)
low.select_set(True)
bpy.context.view_layer.objects.active = low
scn.render.bake.margin = 0
bpy.ops.object.bake(type="EMIT")
inside = np.array(mask_im.pixels[:], dtype=np.float32).reshape(TEX, TEX, 4)[:, :, 0] > 0.5
unset(saved)
# THE LAYOUT'S OWN PARTS (the low mesh's material at each pixel): the ID is held to what can lie on that part (the
# second bake: cloth-coloured specks along the zip, every 10 mm, where rays near the low mesh's vertices on the zip line
# met cloth, not teeth): on tape only tape or teeth, on rib only rib, on cloth only cloth or welt
part_im = target_image("_part")
saved = set_emission(low, lambda n: ID.get(n, 0.0))
bpy.ops.object.bake(type="EMIT")
part = np.array(part_im.pixels[:], dtype=np.float32).reshape(TEX, TEX, 4)[:, :, 0]
unset(saved)
scn.render.bake.margin = 8
scn.render.bake.use_selected_to_active = True

# (1) where the rays found the source: everything of the source glowing white
hit_im = target_image("_hit")
saved = set_emission(src, lambda n: 1.0)
hit = bake("EMIT", hit_im, 1)[:, :, 0]
unset(saved)
log["checks"]["hitShare"] = round(float((hit[inside] > 0.5).mean()), 4)

# (2) the ID: each part glowing at its value, snapped to the five values
id_im = target_image("_id")
saved = set_emission(src, lambda n: ID.get(n, 0.0))
idv = bake("EMIT", id_im, 4)[:, :, 0]
unset(saved)
np.save(os.path.join(OUT, "debug_idraw.npy"), idv)
np.save(os.path.join(OUT, "debug_hit.npy"), hit)
levels = np.array(sorted(set(ID.values())))
idq = levels[np.abs(idv[..., None] - levels[None, None, :]).argmin(axis=2)]
on_tape, on_rib = np.abs(part - 0.5) < 0.125, np.abs(part - 0.25) < 0.125
on_cloth = inside & ~on_tape & ~on_rib
log["checks"]["idHeldToPart"] = int(((on_tape & ~np.isin(idq, [0.5, 0.75])) | (on_rib & (idq != 0.25)) | (on_cloth & ~np.isin(idq, [0.0, 1.0]))).sum())
idq = np.where(on_tape, np.where(idv >= 0.625, 0.75, 0.5), idq)
idq = np.where(on_rib, 0.25, idq)
idq = np.where(on_cloth, np.where(idv >= 0.875, 1.0, 0.0), idq)
shares = {str(v): round(float((idq[inside] == v).mean()), 4) for v in levels}
log["checks"]["idShares"] = shares
# against the low mesh's own areas in the layout (cloth, rib, tape by its material; teeth and welts are floaters)
uv_area = {}
for poly in low.data.polygons:
    uvs = [low.data.uv_layers["UVMap"].data[li].uv for li in poly.loop_indices]
    a = 0.0
    for j in range(1, len(uvs) - 1):
        a += abs((uvs[j] - uvs[0]).cross(uvs[j + 1] - uvs[0])) / 2
    mname = low.data.materials[poly.material_index].name.split(".")[0]
    uv_area[mname] = uv_area.get(mname, 0.0) + a
tot = sum(uv_area.values())
log["checks"]["layoutShares"] = {k: round(v / tot, 4) for k, v in uv_area.items()}

# (3) the normal map, tangent space (OpenGL: green up), then flipped for Unreal
nrm_im = target_image("_normal")
nrm = bake("NORMAL", nrm_im, 4)
gl = nrm.copy()
dx = nrm.copy()
dx[:, :, 1] = 1.0 - dx[:, :, 1]

# (4) occlusion, the body hidden, from the source onto the low mesh
ao_im = target_image("_ao")
ao = bake("AO", ao_im, AO_SAMPLES)[:, :, 0]

# the packed map and the colour map
rough = np.vectorize(lambda v: ROUGH[float(v)])(idq).astype(np.float32)
grey = np.vectorize(lambda v: GREY[float(v)])(idq).astype(np.float32)
metal = (idq == 0.75).astype(np.float32)


def save(arr, label, colour=False):
    im = bpy.data.images.new(NAME + label, TEX, TEX, alpha=True, float_buffer=False)
    im.colorspace_settings.name = "sRGB" if colour else "Non-Color"
    im.pixels[:] = arr.reshape(-1).tolist()
    im.filepath_raw = os.path.join(OUT, NAME + label + ".png")
    im.file_format = "PNG"
    im.save()


one = np.ones((TEX, TEX), dtype=np.float32)
save(np.stack([rough, idq.astype(np.float32), metal, one], axis=2), "_packed")
save(np.stack([grey, grey, grey, ao], axis=2), "_colour_ao", colour=True)
save(gl, "_normal_gl")
save(dx, "_normal_dx")
log["checks"]["aoMedianInside"] = round(float(np.median(ao[inside])), 3)
# the low mesh kept as baked (its faces outward), the joined source dropped
bpy.data.objects.remove(src, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=LOW)
log["seconds"] = round(time.time() - t0, 1)
json.dump(log, open(os.path.join(OUT, "bake.json"), "w", encoding="utf-8"), indent=1)
print("BAKE", json.dumps({**log["checks"], "seconds": log["seconds"], "flipped": log["flipped"]}))
