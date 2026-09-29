"""A knee-length pleated skirt, modelled round the wearer's own body from a pleated skirt's pattern sizes.

    blender -b -P tools/meshgen/blender/model_skirt.py -- BODY.fbx MEASURE.json OUT_DIR [--name sheila_skirt]

WHY, 29 September (the clothing session, CLOTHES.md item 5: Sheila's clothes;
production/research/clothing-pipeline/SHEILA-CLOTHES-2026-09-29.md). Sheila's
casting sheet: "a brown knee-length pleated skirt"; her approved concept
(production/casting/sheila-dunn/full.jpg) shows soft pleats all round, a
little A-line, just below the knee; the nearest dated reference, Dot Cotton's
skirt of about 1985 at the V&A (S.109-2023), is brown, knee length, side
pleated, 66 cm long, its hem about twice its waist round. FreeSewing has no
pleated skirt; the traditional rule gives one: knife pleats stitched down from
the waist to the hip, the cloth at the hem three times the finished width of
a touching pleat. Sewn by projection the jacket, the trousers and the cap
failed their reviews on gathers, crumples and ragged joins, and game artists
model stiff and pleated garments; so the skirt is modelled, its sizes from
that rule and her measurements:
  - the waist at her natural waist, a 30 mm band, fitted to the hip 16 cm down
    (the pleats stitched flat there), 3 to 8 mm off her body;
  - below the hip it hangs as a curtain: at each angle round her, as far out as
    her body reaches there or anywhere above, the section's hull spanning the
    gap between her legs, flaring 4 degrees;
  - PLEATS knife pleats all round, opening below the stitching, soft-edged;
  - the hem LENGTH below the waist.
One render mesh; in the game the band and hip are skinned to the pelvis and the
rest is Chaos cloth (the research). OUT_DIR gets NAME_render_static.fbx,
NAME.blend, pictures and skirt.json.
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
BODY, MEASURE, OUT = argv[0], argv[1], argv[2]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "sheila_skirt", str)
LENGTH = opt("--length", 0.62)            # waist to hem, m
PLEATS = opt("--pleats", 16, int)
DEPTH = opt("--depth", 0.010)             # how far a pleat's fold stands out from its hollow, m
FLARE = math.radians(opt("--flare", 4.0))
HIP_DROP = opt("--hip", 0.16)             # the pleats stitched down this far below the waist, m
log = {"body": BODY, "length": LENGTH, "pleats": PLEATS}


def say(*a):
    print("SKIRT", *a, flush=True)


meas = json.load(open(MEASURE))
Z_W = meas["heights_m"]["waist"]
Z_HIP = Z_W - HIP_DROP
Z_HEM = Z_W - LENGTH
arm, body = tailor.load_body(BODY, lod=opt("--lod", 1, int))
BVH = tailor.bvh_of(body)
co = np.array([body.matrix_world @ v.co for v in body.data.vertices])
torso = co[(co[:, 2] > Z_HEM - 0.05) & (co[:, 2] < Z_W + 0.05) & (np.abs(co[:, 0]) < 0.28)]
CX, CY = 0.0, float(0.5 * (torso[:, 1].min() + torso[:, 1].max()))
NPHI = opt("--around", 256, int)
ANG = np.linspace(0.0, 2 * math.pi, NPHI, endpoint=False)       # 0 at +x (her left), counter-clockwise seen from above


def hull_radius(z):
    """The body's section at height z as its hull, the distance from the middle to the hull at each angle."""
    loops = tailor.section_loops(body, (0, 0, z), (0, 0, 1))
    pts = np.concatenate(loops) if loops else np.zeros((0, 3))
    pts = pts[np.abs(pts[:, 0]) < 0.28]
    if len(pts) < 3:
        return np.zeros(NPHI)
    hull = np.array(tailor._hull2(pts[:, :2]))
    c = np.array([CX, CY])
    out = np.zeros(NPHI)
    for k, a in enumerate(ANG):
        d = np.array([math.cos(a), math.sin(a)])
        best = 0.0
        for i in range(len(hull)):
            q0, q1 = hull[i], hull[(i + 1) % len(hull)]
            e = q1 - q0
            den = d[0] * (-e[1]) + d[1] * e[0]
            if abs(den) < 1e-12:
                continue
            w = q0 - c
            t = (w[0] * (-e[1]) + w[1] * e[0]) / den
            u = (d[0] * w[1] - d[1] * w[0]) / den
            if t > best and -1e-9 <= u <= 1 + 1e-9:
                best = t
        out[k] = best
    return out


# rows from the waist down: the body's hull radius at each, the curtain's running maximum below the hip
ROW_Z = np.concatenate([np.linspace(Z_W, Z_HIP, 14), np.linspace(Z_HIP, Z_HEM, 40)[1:]])
radius = []
running = np.zeros(NPHI)
for z in ROW_Z:
    r = hull_radius(z)
    if z >= Z_HIP:
        ease = 0.003 + 0.005 * (Z_W - z) / HIP_DROP                     # 3 mm at the waist to 8 mm at the hip
        rr = r + ease
        running = np.maximum(running, rr)
        radius.append(rr)
    else:
        running = np.maximum(running, r + 0.008)
        radius.append(running + (Z_HIP - z) * math.tan(FLARE))
radius = np.array(radius)
# a little smoothing round each row (the hull's corners)
for _ in range(6):
    radius = 0.5 * radius + 0.25 * (np.roll(radius, 1, axis=1) + np.roll(radius, -1, axis=1))

# ---- the pleats: knife pleats all round, stitched flat to the hip, opening below ----------------------


def pleat(a):
    """A soft knife pleat's profile across one pleat (0..1): the fold's edge at 0, the face sloping in to the
    next pleat's hollow."""
    u = (a * PLEATS / (2 * math.pi)) % 1.0
    return (1.0 - u) - 0.5 * (1.0 - math.exp(-u / 0.06))


verts, grid = [], []
for j, z in enumerate(ROW_Z):
    open_ = 0.0 if z >= Z_HIP else min(1.0, (Z_HIP - z) / 0.10)
    row = []
    for k, a in enumerate(ANG):
        r = radius[j, k] + DEPTH * open_ * pleat(a)
        row.append(len(verts))
        verts.append((CX + r * math.cos(a), CY + r * math.sin(a), float(z)))
    grid.append(row)
faces = []
for j in range(len(ROW_Z) - 1):
    for k in range(NPHI):
        k2 = (k + 1) % NPHI
        faces.append((grid[j][k], grid[j][k2], grid[j + 1][k2], grid[j + 1][k]))
me = bpy.data.meshes.new("Skirt")
me.from_pydata(verts, [], faces)
me.validate()
skirt = bpy.data.objects.new("Skirt", me)
bpy.context.collection.objects.link(skirt)
uvl = me.uv_layers.new(name="pattern")
for poly in me.polygons:
    for li in poly.loop_indices:
        vi = me.loops[li].vertex_index
        j, k = divmod(vi, NPHI)
        uvl.data[li].uv = (k / NPHI * 2 * math.pi * float(np.mean(radius[j])), float(ROW_Z[j]))
log["pushedOut"] = tailor.push_out(skirt, BVH, 0.003)
hem = radius[-1]
log["sizes"] = {"waistRoundMm": round(float(np.sum(np.hypot(np.diff(np.append(radius[0], radius[0][0]) * np.cos(np.append(ANG, 0))), 0))) * 0 + 2 * math.pi * float(np.mean(radius[0])) * 1000),
                "hipRoundMm": round(2 * math.pi * float(np.mean(radius[13])) * 1000),
                "hemRoundMm": round(2 * math.pi * float(np.mean(hem)) * 1000), "hemZ": round(Z_HEM, 3)}
say("sizes", log["sizes"])

# ---- the simulation mesh: the same skirt without its pleats, 64 round and every second row --------------------
#
# In the game the pleated render mesh rides a coarse cloth (the research: a
# coarse sim cone that drives the pleated render mesh); the test does the same.
SIM_AROUND = opt("--sim-around", 64, int)
step = NPHI // SIM_AROUND
srows = list(range(0, len(ROW_Z), 2)) + ([len(ROW_Z) - 1] if (len(ROW_Z) - 1) % 2 else [])
sverts, sgrid = [], []
for j in srows:
    row = []
    for k in range(0, NPHI, step):
        a = ANG[k]
        r = radius[j, k] + (0.0 if ROW_Z[j] >= Z_HIP else DEPTH * 0.25)
        row.append(len(sverts))
        sverts.append((CX + r * math.cos(a), CY + r * math.sin(a), float(ROW_Z[j])))
    sgrid.append(row)
sfaces = []
n_ = len(sgrid[0])
for j in range(len(sgrid) - 1):
    for k in range(n_):
        k2 = (k + 1) % n_
        sfaces.append((sgrid[j][k], sgrid[j][k2], sgrid[j + 1][k2], sgrid[j + 1][k]))
sm = bpy.data.meshes.new("SkirtSim")
sm.from_pydata(sverts, [], sfaces)
sm.validate()
sim = bpy.data.objects.new("SkirtSim", sm)
bpy.context.collection.objects.link(sim)
sim.hide_render = True
log["sim"] = {"verts": len(sverts), "hipZ": round(Z_HIP, 3)}

# ---- the waistband, and the render mesh ------------------------------------------------------------------

wool = tailor.material("M_SkirtWool", tuple(float(c) for c in opt("--rgb", "0.13,0.075,0.045", str).split(",")), 0.9)
grey = tailor.material("M_Body", (0.5, 0.5, 0.5))
me.materials.append(wool)
band_rows = []
for dz in (0.0, -0.015, -0.030):
    j = int(np.argmin(np.abs(ROW_Z - (Z_W + dz))))
    band_rows.append([Vector(verts[grid[j][k]]) + Vector((math.cos(a), math.sin(a), 0)) * 0.0015 for k, a in enumerate(ANG)])
bverts, bfaces = [], []
for r_ in band_rows:
    bverts.extend(tuple(p) for p in r_)
for i in range(len(band_rows) - 1):
    for k in range(NPHI):
        k2 = (k + 1) % NPHI
        bfaces.append((i * NPHI + k, i * NPHI + k2, (i + 1) * NPHI + k2, (i + 1) * NPHI + k))
bm_ = bpy.data.meshes.new("Band")
bm_.from_pydata(bverts, [], bfaces)
band = bpy.data.objects.new("Band", bm_)
bpy.context.collection.objects.link(band)
bm_.materials.append(wool)
render = skirt.copy()
render.data = skirt.data.copy()
render.name = "SkirtRender"
bpy.context.collection.objects.link(render)
rb = bmesh.new()
rb.from_mesh(render.data)
bmesh.ops.recalc_face_normals(rb, faces=rb.faces[:])
rb.normal_update()
vote = sum(f.normal.dot(f.calc_center_median() - Vector((CX, CY, f.calc_center_median().z))) for f in list(rb.faces)[::7])
if vote < 0:
    bmesh.ops.reverse_faces(rb, faces=rb.faces[:])
rb.to_mesh(render.data)
rb.free()
for o, th in ((render, 0.0025), (band, 0.003)):
    for p in o.data.polygons:
        p.use_smooth = True
    s_ = o.modifiers.new("Solidify", "SOLIDIFY")
    s_.thickness, s_.offset = th, -1.0
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    for mdf in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=mdf.name)
bpy.ops.object.select_all(action="DESELECT")
render.select_set(True)
band.select_set(True)
bpy.context.view_layer.objects.active = render
bpy.ops.object.join()
render = bpy.context.active_object
log["render"] = {"verts": len(render.data.vertices), "tris": sum(len(p.vertices) - 2 for p in render.data.polygons)}
say("render", log["render"])
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, "%s_render_static.fbx" % NAME), use_selection=True,
                         object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
skirt.hide_render = True
skirt.hide_set(True)
body.data.materials.clear()
body.data.materials.append(grey)
MID = Vector((0.0, CY, 0.78))
tailor.pictures(os.path.join(OUT, "skirt"), MID,
                views=(("front", (0, -2.6, 0.1)), ("side", (2.6, 0, 0.1)), ("back", (0, 2.6, 0.1)), ("three-quarter", (1.8, -1.9, 0.3))))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "skirt.json"), "w"), indent=1)
say("done")
