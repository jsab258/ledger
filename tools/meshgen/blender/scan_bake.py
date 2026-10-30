"""A scan's maps carried onto its game mesh (30 October 2026, Tom's shoes from the scanned oxford): colour with
occlusion, normal, and the packed map, as the garments' material reads them.

    blender -b --factory-startup -P tools/meshgen/blender/scan_bake.py -- GAME.blend LOW HIGH.blend HIGH OUT_DIR
        --albedo A --normal N --rough R --ao O [--tex 1024] [--name tom_shoes] [--extrude 0.004] [--reach 0.010]
        [--owner LAYOUT_OWNER.npy] [--poison-rect u0,v0,u1,v1]

WHY: the game mesh (scan_lods.py's LOD0, its packed layout "UVMap" first) takes the scan's own photographed maps
through the scan's layout, by Cycles' selected-to-active bake on the processor: the colour, roughness and occlusion
as emission (a straight copy of the texture under each ray's hit), the normal as Cycles' tangent-space normal of
the scan's surface with its own normal map (OpenGL, measured: the map's green rises with v). Packed as the garment
material reads them (tools/ue/import_garments.py, M_LedgerGarmentPacked): NAME_colour_ao.png (the scan's colour,
its occlusion in alpha), NAME_packed.png (roughness R, the part's ID G = 0 everywhere, metal B = 0; the material's
tint must then be white so the colour is the scan's own), NAME_normal_dx.png (green flipped, for Unreal) and
NAME_normal_gl.png.

Checks in bake.json: the share of the layout's texels whose ray found the scan (a white emission baked onto black);
the share of texels whose baked normal leans more than 60 degrees off the surface; and, with --poison-rect (a part
of the scan's square that no island covers: the scanner's copyright line), the colour baked once more from a copy
of the colour map with that rectangle painted pure magenta: any magenta texel means the rectangle reaches the
surface.
"""
import json
import os
import sys
import time

import bpy
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
GAME, LOW, HIGHF, HIGH, OUT = argv[:5]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
TEX = opt("--tex", 1024, int)
NAME = opt("--name", "tom_shoes", str)
EXTRUDE = opt("--extrude", 0.004)
REACH = opt("--reach", 0.010)
MAPS = {k: opt("--" + k, None, str) for k in ("albedo", "normal", "rough", "ao")}
OWNER = opt("--owner", None, str)
POISON = opt("--poison-rect", None, str)
os.makedirs(OUT, exist_ok=True)
t0 = time.time()
log = {"game": GAME, "low": LOW, "high": HIGHF, "tex": TEX, "maps": MAPS, "extrudeM": EXTRUDE, "reachM": REACH}


def say(*a):
    print("BAKE", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=GAME)
low = bpy.data.objects[LOW]
for o in list(bpy.data.objects):
    if o is not low:
        bpy.data.objects.remove(o, do_unlink=True)
with bpy.data.libraries.load(HIGHF) as (src, dst):
    dst.objects = [HIGH]
high = dst.objects[0]
bpy.context.scene.collection.objects.link(high)
high.name = "ScanHigh"
low.data.uv_layers.active = low.data.uv_layers[0]
log["lowUV"] = low.data.uv_layers[0].name

sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 16
sc.render.bake.use_selected_to_active = True
sc.render.bake.cage_extrusion = EXTRUDE
sc.render.bake.max_ray_distance = REACH
sc.render.bake.margin = 8
sc.render.bake.margin_type = "EXTEND"


def image(path, colour):
    im = bpy.data.images.load(path)
    im.colorspace_settings.name = "sRGB" if colour else "Non-Color"
    return im


# ---- the scan's material: its maps, the normal through a normal map node; an emission switch for copies ----------
hm = bpy.data.materials.new("ScanMat")
hm.use_nodes = True
nt = hm.node_tree
bsdf = nt.nodes["Principled BSDF"]
outn = nt.nodes["Material Output"]
tx = {}
for k, colour in (("albedo", True), ("normal", False), ("rough", False), ("ao", False)):
    n = nt.nodes.new("ShaderNodeTexImage")
    n.image = image(MAPS[k], colour)
    n.interpolation = "Cubic"
    tx[k] = n
nmap = nt.nodes.new("ShaderNodeNormalMap")
nmap.uv_map = high.data.uv_layers[0].name
nt.links.new(tx["normal"].outputs["Color"], nmap.inputs["Color"])
nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
nt.links.new(tx["albedo"].outputs["Color"], bsdf.inputs["Base Color"])
nt.links.new(tx["rough"].outputs["Color"], bsdf.inputs["Roughness"])
emit = nt.nodes.new("ShaderNodeEmission")
white = nt.nodes.new("ShaderNodeRGB")
white.outputs[0].default_value = (1, 1, 1, 1)
high.data.materials.clear()
high.data.materials.append(hm)

# ---- the game mesh's material: one image node, the bake's target ---------------------------------------------------
lm = bpy.data.materials.new("GameMat")
lm.use_nodes = True
target = lm.node_tree.nodes.new("ShaderNodeTexImage")
lm.node_tree.nodes.active = target
low.data.materials.clear()
low.data.materials.append(lm)


def bake(kind, source=None, colour=False, margin=8):
    im = bpy.data.images.new("bake_" + kind, TEX, TEX, alpha=False, float_buffer=not colour)
    im.colorspace_settings.name = "sRGB" if colour else "Non-Color"
    im.generated_color = (0, 0, 0, 1)
    target.image = im
    for l in list(nt.links):
        if l.to_node is outn:
            nt.links.remove(l)
    if kind == "normal":
        nt.links.new(bsdf.outputs[0], outn.inputs["Surface"])
        btype = "NORMAL"
    else:
        nt.links.new(source, emit.inputs["Color"])
        nt.links.new(emit.outputs[0], outn.inputs["Surface"])
        btype = "EMIT"
    sc.render.bake.margin = margin
    bpy.ops.object.select_all(action="DESELECT")
    high.select_set(True)
    low.select_set(True)
    bpy.context.view_layer.objects.active = low
    t = time.time()
    bpy.ops.object.bake(type=btype, normal_space="TANGENT", normal_r="POS_X", normal_g="POS_Y", normal_b="POS_Z",
                        use_selected_to_active=True, cage_extrusion=EXTRUDE, max_ray_distance=REACH, margin=margin,
                        margin_type="EXTEND")
    px = np.empty(TEX * TEX * 4, np.float32)
    im.pixels.foreach_get(px)
    say(kind, "%.1f s" % (time.time() - t))
    return px.reshape(TEX, TEX, 4), im


# the layout's own texels (scan_lods.py's owner raster, rows from v = 0)
mask = None
if OWNER:
    own = np.load(OWNER)
    mask = own >= 0
    log["layoutTexels"] = int(mask.sum())

hit, _ = bake("hit", white.outputs[0], margin=0)
if mask is not None:
    log["hitShare"] = round(float((hit[..., 0][mask] > 0.5).mean()), 5)
    say("hits", log["hitShare"])
col, col_im = bake("colour", tx["albedo"].outputs["Color"], colour=True)
rough, _ = bake("rough", tx["rough"].outputs["Color"])
ao, _ = bake("ao", tx["ao"].outputs["Color"])
nrm, _ = bake("normal")
# the normal's lean off the surface
nv = nrm[..., :3] * 2 - 1
lean = np.degrees(np.arccos(np.clip(nv[..., 2] / np.maximum(np.linalg.norm(nv, axis=-1), 1e-6), -1, 1)))
if mask is not None:
    log["normalsOver60Share"] = round(float((lean[mask] > 60).mean()), 5)
    log["normalLeanMedianDeg"] = round(float(np.median(lean[mask])), 2)
    log["normalsOver30Share"] = round(float((lean[mask] > 30).mean()), 5)
    say("normals over 60", log["normalsOver60Share"])

# the poison test: the copyright corner painted magenta and the colour baked again
if POISON:
    u0, v0, u1, v1 = [float(x) for x in POISON.split(",")]
    src_im = tx["albedo"].image
    w, h = src_im.size
    px = np.empty(w * h * 4, np.float32)
    src_im.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)
    px[int(v0 * h):int(v1 * h), int(u0 * w):int(u1 * w), :3] = (1.0, 0.0, 1.0)
    pim = bpy.data.images.new("poisoned", w, h, alpha=False)
    pim.colorspace_settings.name = "sRGB"
    pim.pixels.foreach_set(px.ravel())
    tx["albedo"].image = pim
    pc, _ = bake("poison", tx["albedo"].outputs["Color"], colour=True)
    mag = (pc[..., 0] > 0.6) & (pc[..., 1] < 0.25) & (pc[..., 2] > 0.6)
    log["poison"] = {"rectUV": [u0, v0, u1, v1], "magentaTexels": int(mag.sum())}
    say("poison", log["poison"])
    tx["albedo"].image = src_im


def save(name, arr, colour):
    im = bpy.data.images.new(name, TEX, TEX, alpha=True, float_buffer=False)
    im.colorspace_settings.name = "sRGB" if colour else "Non-Color"
    im.pixels.foreach_set(arr.astype(np.float32).ravel())
    im.filepath_raw = os.path.join(OUT, name + ".png")
    im.file_format = "PNG"
    im.save()
    return im.filepath_raw


# the colour came back through the sRGB target as display values; occlusion into its alpha
ca = col.copy()
ca[..., 3] = ao[..., 0]
files = {"colour_ao": save(NAME + "_colour_ao", ca, True)}
pk = np.zeros_like(col)
pk[..., 0] = rough[..., 0]
pk[..., 3] = 1.0
files["packed"] = save(NAME + "_packed", pk, False)
gl = nrm.copy()
gl[..., 3] = 1.0
files["normal_gl"] = save(NAME + "_normal_gl", gl, False)
dx = gl.copy()
dx[..., 1] = 1.0 - dx[..., 1]
files["normal_dx"] = save(NAME + "_normal_dx", dx, False)
log["files"] = files
if mask is not None:
    log["roughMedian"] = round(float(np.median(rough[..., 0][mask])), 3)
    log["aoMedian"] = round(float(np.median(ao[..., 0][mask])), 3)
# texel density: texels over the surface area
area = sum(p.area for p in low.data.polygons)
if mask is not None:
    log["texelsPerMm"] = round(float(np.sqrt(mask.sum() / (area * 1e6))), 3)
log["seconds"] = round(time.time() - t0, 1)
json.dump(log, open(os.path.join(OUT, "bake.json"), "w"), indent=1)
say("done", json.dumps({k: v for k, v in log.items() if k not in ("maps", "files")}))
