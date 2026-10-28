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
PLAN_NAMES = ["frontL", "frontR", "back", "sleeveR", "sleeveL", "bandFrontR", "cuffR", "bandFrontL", "cuffL", "bandBack",
              "collar", "tapeR", "tapeL"]
# THE CUFFS FACE AWAY FROM THE FOREARM, FACE BY FACE (28 October 2026, drape 19: Marvelous turned each gripped cuff inside
# out through itself at its seam with the sleeve, so wound on from the sleeve 74 and 75% of each cuff faced the wrist; a
# one-sided material would cull it in the game, the binder finds no body facing its way, and the bake read the knot's
# far sides). A tube round the wrist faces away from the forearm's axis (elbow joint to hand joint); the knot itself
# stays, a listed fault. A drape whose cuffs face out (drape 6) is unchanged.
arm_ = next((o for o in bpy.data.objects if o.type == "ARMATURE"), None)
CUFF_AXES = {}
for cname_, side_ in (("cuffR", "r"), ("cuffL", "l")):
    if arm_ is not None and "lowerarm_" + side_ in arm_.pose.bones and "hand_" + side_ in arm_.pose.bones:
        e_ = arm_.matrix_world @ arm_.pose.bones["lowerarm_" + side_].head
        h_ = arm_.matrix_world @ arm_.pose.bones["hand_" + side_].head
        CUFF_AXES[PLAN_NAMES.index(cname_)] = (e_, (h_ - e_).normalized())
cuffs_turned = {}


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
    bm.normal_update()
    pl_ = bm.faces.layers.int.get("piece")
    if pl_ is not None and CUFF_AXES:
        turned = []
        for f in bm.faces:
            ax_ = CUFF_AXES.get(f[pl_])
            if ax_ is None:
                continue
            d_ = mw @ f.calc_center_median() - ax_[0]
            if (mw.to_3x3() @ f.normal).dot(d_ - ax_[1] * d_.dot(ax_[1])) < 0:
                turned.append(f)
        if turned:
            bmesh.ops.reverse_faces(bm, faces=turned)
        cuffs_turned[o.name] = len(turned)
    bm.to_mesh(o.data)
    bm.free()
    return flipped


# the floaters too (the first look: the welts' lips were wound inward, their shading and occlusion read from inside
# and they baked as black slashes), and the game mesh smooth-shaded as the game draws it (baked flat and drawn smooth,
# the cloth showed its grid as quilting)
log["flipped"] = {o.name: face_outward(o) for o in [low, drape] + floaters}
log["cuffFacesTurned"] = cuffs_turned
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

# (3) THE NORMAL MAP, EACH PIECE FROM ITS OWN PIECE OF THE DRAPE (the first fresh review, 27 October night: one cuff's
# normals 80% wrong, a black slab over the hand at the game's distance, the other 11%; dark spikes along the deep side
# folds: rays from one piece met another, the sleeve's end folded over the cuff, a fold's far side). Each piece of the
# game mesh is baked from the drape's same piece only (the tapes with the teeth and stops, the fronts with their welts),
# the rays' reach held to --ray, and the pieces put together by the layout's own piece map.
RAY = opt("--ray", 0.014)
scn.render.bake.cage_extrusion = opt("--cage-normal", 0.006)
scn.render.bake.max_ray_distance = RAY
# the layout rasterised: each pixel's piece, and its place in the piece's own pattern (for the rib's ridges)
lay_piece = np.full((TEX, TEX), -1, dtype=np.int32)
lay_px = np.zeros((TEX, TEX), dtype=np.float32)
uvl = low.data.uv_layers["UVMap"].data
pat_l = low.data.uv_layers["pattern"].data
pattr = low.data.attributes["piece"].data
for poly in low.data.polygons:
    li = list(poly.loop_indices)
    for j in range(1, len(li) - 1):
        tri = (li[0], li[j], li[j + 1])
        xs = [uvl[k].uv.x * TEX for k in tri]
        ys = [uvl[k].uv.y * TEX for k in tri]
        x0, x1 = max(0, int(min(xs))), min(TEX - 1, int(max(xs)) + 1)
        y0, y1 = max(0, int(min(ys))), min(TEX - 1, int(max(ys)) + 1)
        if x1 < x0 or y1 < y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        d = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
        if abs(d) < 1e-12:
            continue
        l1 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / d
        l2 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / d
        l3 = 1 - l1 - l2
        ins = (l1 >= -1e-4) & (l2 >= -1e-4) & (l3 >= -1e-4)
        lay_piece[y0:y1 + 1, x0:x1 + 1][ins] = pattr[poly.index].value
        pxs = [pat_l[k].uv.x for k in tri]
        lay_px[y0:y1 + 1, x0:x1 + 1][ins] = (l1 * pxs[0] + l2 * pxs[1] + l3 * pxs[2])[ins]
# the drape cut into its pieces, each with the floaters that lie on it
dsrc = bmesh.new()
dsrc.from_mesh(drape.data)
dpl = dsrc.faces.layers.int["piece"]
piece_src = {}
for k, pname in enumerate(PLAN_NAMES):
    bk = dsrc.copy()
    kl = bk.faces.layers.int["piece"]
    bmesh.ops.delete(bk, geom=[f for f in bk.faces if f[kl] != k], context="FACES")
    me_k = bpy.data.meshes.new("src_" + pname)
    bk.to_mesh(me_k)
    bk.free()
    for m in drape.data.materials:
        me_k.materials.append(m)
    o_k = bpy.data.objects.new("src_" + pname, me_k)
    o_k.matrix_world = drape.matrix_world
    bpy.context.scene.collection.objects.link(o_k)
    extra = [floaters[0], floaters[1]] if pname.startswith("tape") else [floaters[2]] if pname.startswith("front") else []
    parts_ = [o_k]
    for f_ in extra:
        c = f_.copy()
        c.data = f_.data.copy()
        bpy.context.scene.collection.objects.link(c)
        parts_.append(c)
    if len(parts_) > 1:
        for o in bpy.context.view_layer.objects:
            o.select_set(False)
        for p_ in parts_:
            p_.hide_set(False)
            p_.select_set(True)
        bpy.context.view_layer.objects.active = o_k
        bpy.ops.object.join()
    o_k.hide_render = True
    piece_src[k] = o_k
src.hide_render = True
nrm = np.zeros((TEX, TEX, 4), dtype=np.float32)
got = np.zeros((TEX, TEX), dtype=bool)
nrm_im = target_image("_normal")
for k, o_k in piece_src.items():
    o_k.hide_render = False
    o_k.hide_set(False)
    scn.cycles.samples = 4
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    o_k.select_set(True)
    low.select_set(True)
    bpy.context.view_layer.objects.active = low
    bpy.ops.object.bake(type="NORMAL")
    nk = np.array(nrm_im.pixels[:], dtype=np.float32).reshape(TEX, TEX, 4)
    sel = lay_piece == k
    nrm[sel] = nk[sel]
    got |= sel
    o_k.hide_render = True
    o_k.hide_set(True)
# the margin round each island: filled from the island outward
for _ in range(8):
    acc = np.zeros_like(nrm)
    cnt = np.zeros((TEX, TEX), dtype=np.float32)
    for dy, dx_ in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        sh_ok = np.roll(np.roll(got, dy, 0), dx_, 1)
        acc += np.roll(np.roll(nrm, dy, 0), dx_, 1) * sh_ok[..., None]
        cnt += sh_ok
    fill = (~got) & (cnt > 0)
    nrm[fill] = acc[fill] / cnt[fill][:, None]
    got |= fill
nrm[~got] = (0.5, 0.5, 1.0, 1.0)
# THE RIB'S RIDGES, drawn from the pattern (the drape has none: the review's "rib bakes smooth"): wales 4 mm apart
# along the piece's own x, 0.4 mm high, their slope laid along that direction in the layout and added to the bake
RIB_PITCH, RIB_H = opt("--rib-pitch", 0.004), opt("--rib-height", 0.0004)
rib_ix = [k for k, n in enumerate(PLAN_NAMES) if n.startswith(("band", "cuff"))]
on_rib_px = np.isin(lay_piece, rib_ix)
gx_ = np.gradient(lay_px, axis=1)
gy_ = np.gradient(lay_px, axis=0)
glen = np.sqrt(gx_ ** 2 + gy_ ** 2) + 1e-12
slope = -RIB_H * (2 * math.pi / RIB_PITCH) * np.sin(2 * math.pi * lay_px / RIB_PITCH)
vx, vy = 2 * nrm[..., 0] - 1, 2 * nrm[..., 1] - 1
vx = np.where(on_rib_px, vx - slope * gx_ / glen, vx)
vy = np.where(on_rib_px, vy - slope * gy_ / glen, vy)
vz = 2 * nrm[..., 2] - 1
ln = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2) + 1e-12
nrm[..., 0], nrm[..., 1], nrm[..., 2] = (vx / ln + 1) / 2, (vy / ln + 1) / 2, (vz / ln + 1) / 2
log["checks"]["ribPixels"] = int(on_rib_px.sum())
# each piece's share of texels whose normal leans more than 60 degrees off the surface (the review's measure)
offs = {}
for k, n in enumerate(PLAN_NAMES):
    sel = lay_piece == k
    if sel.any():
        offs[n] = round(float(((2 * nrm[..., 2] - 1)[sel] < 0.5).mean()), 4)
log["checks"]["normalsOver60PerPiece"] = offs
gl = nrm.copy()
dx = nrm.copy()
dx[:, :, 1] = 1.0 - dx[:, :, 1]
for o_k in piece_src.values():
    bpy.data.objects.remove(o_k, do_unlink=True)
src.hide_render = False
scn.render.bake.cage_extrusion = CAGE
scn.render.bake.max_ray_distance = 0.0

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
