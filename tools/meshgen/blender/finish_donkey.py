"""The draped donkey jacket made a game garment: its yoke, collar, overlapping front, buttons and pockets, and the
render and simulation meshes for Unreal's cloth, in the body's rest pose.

    blender -b -P tools/meshgen/blender/finish_donkey.py -- JACKET.blend BRIAN.json OUT_DIR [--name ron_donkey]

WHY, 29 September (the clothing session, CLOTHES.md item 2). sew_donkey.py
leaves the jacket as one sewn, draped, welded piece of cloth in the body's
rest pose, its flat pattern kept as its UVs. Everything that makes it a
donkey jacket (production/reference/donkey-jacket-1990.md; the V&A's
T.561-1993, seen 29 September) is placed here by the pattern's own
coordinates, found on the drape through those UVs, so it sits where a tailor
would put it whatever the drape did:

- the yoke: black PVC across the shoulders, front to 10 cm under the shoulder
  seam with a straight lower edge, back to about the armpits, 29 cm under the
  collar seam; a raised layer of its own over the wool;
- the collar: a stand and a pointed fall turned down over it, round the neck;
- the front: the left front laps over the right by 4 cm (a man's jacket),
  four dark buttons on the centre line, the top one under the collar;
- two flapless patch pockets, 19 by 20 cm, their feet 8 cm above the hem;
- the wool 3 mm thick.

The SIMULATION MESH is the pattern cut again at 25 mm (the research: a
simplified single-sided mesh, triangles 2 to 3 cm), each coarse point put on
the drape through the shared flat pattern, the seams welded; its UVs are the
flat pattern at true size, from which Unreal can take the pattern's lengths.

OUT_DIR gets NAME_render_static.fbx, NAME_sim_static.fbx (both in the body's
world space, metres, as the builder's make_cloth_jacket.py reads them),
NAME.blend, finished-*.png and finish.json.
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brian  # noqa: E402
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, SRC, OUT = argv[0], argv[1], argv[2]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "ron_donkey", str)
WOOL_T = 0.003
os.makedirs(OUT, exist_ok=True)
log = {"blend": BLEND, "pattern": SRC}


def say(*a):
    print("FINISH", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=BLEND)
jacket = bpy.data.objects["Jacket"]
body = next(o for o in bpy.data.objects if o.type == "MESH" and o is not jacket and not o.hide_render)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
for o in list(bpy.data.objects):
    if o.type == "MESH" and o not in (jacket, body):
        bpy.data.objects.remove(o, do_unlink=True)
P = brian.pieces(SRC, 12.0)
pts = P["points"]
HEM_Y = pts["back"]["cbHem"][1]

# ---- the drape found by the pattern's coordinates ---------------------------------

me = jacket.data
uvl = me.uv_layers["pattern"]
co = np.array([v.co[:] for v in me.vertices])
tri_uv, tri_xyz = [], []
for poly in me.polygons:
    li = list(poly.loop_indices)
    for k in range(1, len(li) - 1):
        a, b, c = li[0], li[k], li[k + 1]
        tri_uv.append([tuple(uvl.data[x].uv) + (0.0,) for x in (a, b, c)])
        tri_xyz.append([co[me.loops[x].vertex_index] for x in (a, b, c)])
UVBVH = BVHTree.FromPolygons([v for t in tri_uv for v in t], [(3 * i, 3 * i + 1, 3 * i + 2) for i in range(len(tri_uv))])
NRM = {}


def on_drape(u, v):
    """The drape's point at flat-pattern place (u, v) (m, the layout's), or None off the pattern."""
    hit = UVBVH.ray_cast(Vector((u, v, 1.0)), Vector((0, 0, -1)), 2.0)
    if hit[2] is None:
        hit = UVBVH.find_nearest(Vector((u, v, 0.0)), 0.004)
        if hit[2] is None:
            return None
    i = hit[2]
    a, b, c = (Vector(x) for x in tri_uv[i])
    A, B_, C = (Vector(x) for x in tri_xyz[i])
    return barycentric_transform(Vector((u, v, 0.0)), a, b, c, A, B_, C)


def piece_uv(piece, side, x, y):
    lx, ly = brian.LAYOUT[(piece, side)]
    return lx + side * x / 1000.0, ly - y / 1000.0


def at(piece, side, x, y):
    return on_drape(*piece_uv(piece, side, x, y))


bmj = bmesh.new()
bmj.from_mesh(me)
bmj.normal_update()
JBVH = BVHTree.FromBMesh(bmj)
CEN = Vector((0.0, float(co[:, 1].mean()), 0.0))
_bev = tailor.evaluated_copy(body, "BodyNow")
BODY_BVH = tailor.bvh_of(_bev)
bpy.data.objects.remove(_bev, do_unlink=True)


def outward(p):
    """The drape's normal near p, turned away from the body (the pieces were laid with their faces turned
    either way, and a direction from the body's axis is no guide on top of the shoulders)."""
    _h, n, _i, _d = JBVH.find_nearest(p)
    if n is None:
        return Vector((0, 0, 1))
    hit, bn, _i2, _d2 = BODY_BVH.find_nearest(p)
    away = (p - hit) if hit is not None else Vector((p.x - CEN.x, p.y - CEN.y, 0.0))
    if away.length < 1e-6 and bn is not None:
        away = bn
    return n if n.dot(away) >= 0 else -n


# ---- materials ------------------------------------------------------------------------

wool = tailor.material("M_DonkeyWool", (0.018, 0.02, 0.03), 0.95)
yoke_m = tailor.material("M_DonkeyYoke", tuple(float(c) for c in opt("--yoke-rgb", "0.004,0.004,0.004", str).split(",")), 0.32)
button_m = tailor.material("M_DonkeyButton", (0.01, 0.009, 0.008), 0.45)
grey = tailor.material("M_Body", (0.5, 0.5, 0.5))


def sheet(name, rows, mat, thickness=WOOL_T, offset=1.0):
    """A surface from a grid of points (rows of equal length), solidified."""
    verts, faces = [], []
    w = len(rows[0])
    for r in rows:
        verts.extend(tuple(p) for p in r)
    for i in range(len(rows) - 1):
        for j in range(w - 1):
            faces.append((i * w + j, i * w + j + 1, (i + 1) * w + j + 1, (i + 1) * w + j))
    m = bpy.data.meshes.new(name)
    m.from_pydata(verts, [], faces)
    m.validate()
    o = bpy.data.objects.new(name, m)
    bpy.context.collection.objects.link(o)
    m.materials.append(mat)
    for p in m.polygons:
        p.use_smooth = True
    if thickness:
        s = o.modifiers.new("Solidify", "SOLIDIFY")
        s.thickness = thickness
        s.offset = offset
    return o


def grid(piece, side, x0, x1, y0, y1, nx, ny, lift):
    """Points over a rectangle of the pattern, on the drape, lifted `lift` off it along its outward normal."""
    rows = []
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        row = []
        for i in range(nx + 1):
            x = x0 + (x1 - x0) * i / nx
            p = at(piece, side, x, y)
            if p is None:
                return None
            row.append(p + outward(p) * lift)
        rows.append(row)
    return rows


extras = []

# ---- the yoke: a raised black layer over the shoulders ----------------------------------------

FRONT_YOKE = opt("--front-yoke", 130.0)        # mm under the shoulder seam's lowest point
BACK_YOKE = opt("--back-yoke", 290.0)          # mm under the back neck (centre back)
YOKE_LIFT = opt("--yoke-lift", 0.0025)         # off the wool, clear of its small folds
fp, bp = pts["front"], pts["back"]
front_yoke_y = max(fp["shoulder"][1], fp["neck"][1]) + FRONT_YOKE
back_yoke_y = bp["cbNeck"][1] + BACK_YOKE


def top_edge(segs):
    """The piece's top edge (neckline, shoulder, armhole) as y for a given x, mm."""
    pts_ = [q for sg in segs for q in sg]
    xs = np.array([q[0] for q in pts_])
    ys = np.array([q[1] for q in pts_])
    order = np.argsort(xs)
    xs, ys = xs[order], ys[order]

    def f(x):
        m = np.abs(xs - x) < 4.0
        return float(ys[m].min()) if m.any() else float(np.interp(x, xs, ys))
    return f, float(xs.max())


def yoke_panel(piece, side, segs, y_low, name):
    """A panel over the pattern from the top edge down to a straight line y_low, column by column, on the drape,
    lifted off it: its lower edge straight across, its top edge along the seams."""
    f, xmax = top_edge(segs)
    nx, ny = 36, 14
    rows = [[] for _ in range(ny + 1)]
    for i in range(nx + 1):
        x = xmax * i / nx
        yt = min(f(x), y_low)
        for j in range(ny + 1):
            y = yt + (y_low - yt) * j / ny
            q = at(piece, side, x, y)
            if q is None:
                q = at(piece, side, max(0.0, x - 2.0), y + 1.0)
            rows[j].append(q + outward(q) * YOKE_LIFT if q is not None else None)
    rows = [[q for q in r] for r in rows]
    if any(q is None for r in rows for q in r):
        say("yoke %s: points off the drape, filled from their neighbours" % name)
        for r in rows:
            for k in range(len(r)):
                if r[k] is None:
                    r[k] = next((r[j] for j in range(k, len(r)) if r[j] is not None), None) or next(
                        (r[j] for j in range(k, -1, -1) if r[j] is not None))
    return sheet(name, rows, yoke_m, thickness=0.0015, offset=1.0)


B_, F_ = P["B"], P["F"]
for side in (1, -1):
    extras.append(yoke_panel("back", side, [B_["neckline"], B_["shoulder"], B_["armhole"]], back_yoke_y,
                             "YokeBack_%s" % ("l" if side > 0 else "r")))
    extras.append(yoke_panel("front", side, [F_["neckline"], F_["shoulder"], F_["armhole"]], front_yoke_y,
                             "YokeFront_%s" % ("l" if side > 0 else "r")))
log["yoke"] = {"frontMmUnderShoulder": FRONT_YOKE, "backMmUnderNeck": BACK_YOKE}

# ---- the front: the left front laps 4 cm over the right; four buttons on the centre line ---------

LAP = opt("--lap", 40.0)
cf_top = fp["cfNeck"][1]
rows = []
for j in range(41):
    y = cf_top + (HEM_Y - cf_top) * j / 40
    row = []
    for x in (0.0, LAP * 0.5, LAP):
        p = at("front", -1, x, y)                   # over the wearer's right front
        row.append(p + outward(p) * (WOOL_T + 0.0005) if p is not None else None)
    rows.append(row)
rows = [r for r in rows if None not in r]
flap = sheet("FrontLap", rows, wool)
extras.append(flap)
BUTTONS = [cf_top + 25.0 + k * 160.0 for k in range(4)]
for k, y in enumerate(BUTTONS):
    p = at("front", 1, 0.0, y)
    if p is None:
        continue
    n = outward(p)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.011, depth=0.004, location=p + n * (2 * WOOL_T + 0.002))
    b = bpy.context.active_object
    b.name = "Button%d" % k
    b.rotation_euler = n.to_track_quat("Z", "Y").to_euler()
    b.data.materials.append(button_m)
    bev = b.modifiers.new("Bevel", "BEVEL")
    bev.width, bev.segments = 0.0015, 2
    extras.append(b)
log["front"] = {"lapMm": LAP, "buttonsMmFromTop": [round(y) for y in BUTTONS]}

# ---- the pockets ----------------------------------------------------------------------------

PW, PH, PFOOT, PX = 190.0, 200.0, 80.0, 70.0      # width, height, foot above the hem, inner edge from centre front
for side in (1, -1):
    x0 = PX + (LAP if side < 0 else 0.0)          # the right front's pocket clears the lap
    rows = grid("front", side, x0, x0 + PW, HEM_Y - PFOOT - PH, HEM_Y - PFOOT, 12, 12, WOOL_T + 0.0008)
    if rows:
        extras.append(sheet("Pocket_%s" % ("l" if side > 0 else "r"), rows, wool, thickness=0.003))
log["pockets"] = {"widthMm": PW, "heightMm": PH, "footAboveHemMm": PFOOT}

# ---- the collar: a stand round the neckline, a pointed fall turned down over it --------------------
#
# Found through the pattern, as everything else here: the neckline's own
# points (the fronts' from centre front to the neck point, the back's round
# the back neck) are the collar's sewn edge; the fall's outer edge lies on
# the jacket FALL mm down the cloth from the neckline, square to it on the
# pattern, so it spreads broad over the yoke as a donkey jacket's does (the
# V&A's T.561-1993); at the fronts it runs further and out to the points.

STAND, FALL, POINT = opt("--stand", 0.03), opt("--fall", 55.0), opt("--point", 30.0)


def along(poly, n):
    return tailor.resample(poly, n)


def normal2d(poly, k):
    a, b = poly[max(0, k - 1)], poly[min(len(poly) - 1, k + 1)]
    tx, ty = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(tx, ty) or 1.0
    return ty / ln, -tx / ln


ring = []          # (piece, side, x, y, nx, ny, end): end 0 at centre front, 1 at centre back
fl = along(F_["neckline"], 24)                     # neck point -> cfNeck
bl = along(B_["neckline"], 16)                     # neck point -> cbNeck
for side in (1, -1):
    seq = []
    for k, (x, y) in enumerate(reversed(fl)):      # cfNeck -> neck point
        seq.append(("front", side, x, y, k / (len(fl) - 1) * 0.5))
    for k, (x, y) in enumerate(bl[1:]):            # neck point -> cbNeck
        seq.append(("back", side, x, y, 0.5 + (k + 1) / (len(bl) - 1) * 0.5))
    ring.append(seq)
ring = ring[0] + list(reversed(ring[1]))[1:]       # left front, left back, right back, right front
cols = []
up = Vector((0, 0, 1))
for piece, side, x, y, end in ring:
    poly = F_["neckline"] if piece == "front" else B_["neckline"]
    k = min(range(len(poly)), key=lambda i: (poly[i][0] - x) ** 2 + (poly[i][1] - y) ** 2)
    nx, ny = normal2d(poly, k)
    if ny < 0:                                     # into the piece: down the pattern, away from the neck
        nx, ny = -nx, -ny
    p = at(piece, side, x, y)
    if p is None:
        continue
    toward = min(end, 1.0) * 2 if end <= 0.5 else 1.0     # 0 at the front ends, 1 from the neck point back
    width = FALL + POINT * max(0.0, 1.0 - toward / 0.35)
    fx, fy = x + nx * width, y + ny * width
    if piece == "front" and toward < 0.35:         # the point: out from centre front as well as down
        fx += POINT * 0.6 * (1.0 - toward / 0.35)
    q_out = at(piece, side, max(0.0, fx), fy)
    if q_out is None:
        continue
    n_out = outward(q_out)
    m = Vector((p.x - CEN.x, p.y - CEN.y, 0.0)).normalized()
    stand_top = p + up * STAND - m * 0.003
    fold = stand_top + m * 0.008 + up * 0.003
    down = q_out + n_out * (WOOL_T * 2 + 0.0015)
    mid = fold.lerp(down, 0.45) + m * 0.008 + up * 0.004
    cols.append([p + outward(p) * 0.001, p.lerp(stand_top, 0.5) - m * 0.001, stand_top, fold, mid, down])
rows = [list(r) for r in zip(*cols)]
collar = sheet("Collar", rows, wool, thickness=0.0035, offset=0.0)
extras.append(collar)
log["collar"] = {"standM": STAND, "fallMm": FALL, "pointMm": POINT, "ringPoints": len(cols)}

# ---- the render mesh ------------------------------------------------------------------------

render = jacket.copy()
render.data = jacket.data.copy()
render.name = "JacketRender"
bpy.context.collection.objects.link(render)
render.data.materials.clear()
render.data.materials.append(wool)
# ONE WAY OUT: the pieces were laid with their faces turned either way; the
# welded cloth's faces are made to agree, then all turned away from the body,
# so the wool's thickness goes inwards everywhere
rb = bmesh.new()
rb.from_mesh(render.data)
bmesh.ops.recalc_face_normals(rb, faces=rb.faces[:])
rb.normal_update()
vote = 0.0
for f in list(rb.faces)[::7]:
    c = f.calc_center_median()
    hit, _n, _i, _d = BODY_BVH.find_nearest(c)
    if hit is not None:
        vote += f.normal.dot(c - hit)
if vote < 0:
    bmesh.ops.reverse_faces(rb, faces=rb.faces[:])
rb.to_mesh(render.data)
rb.free()
for p in render.data.polygons:
    p.use_smooth = True
sub = render.modifiers.new("Subdivision", "SUBSURF")
sub.levels = sub.render_levels = 1
sol = render.modifiers.new("Solidify", "SOLIDIFY")
sol.thickness, sol.offset = WOOL_T, -1.0
bpy.ops.object.select_all(action="DESELECT")
for o in [render] + extras:
    o.hide_set(False)
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    for mdf in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=mdf.name)
bpy.context.view_layer.objects.active = render
bpy.ops.object.join()
render = bpy.context.active_object
log["render"] = {"verts": len(render.data.vertices), "tris": sum(len(p.vertices) - 2 for p in render.data.polygons)}

# ---- the simulation mesh: the pattern cut again at 25 mm, on the drape ------------------------

C = brian.pieces(SRC, opt("--sim-edge", 25.0))
sv, sf, suv = [], [], []
for piece in ("back", "front", "sleeve"):
    flat, faces = C["pieces"][piece]
    for side in (1, -1):
        base = len(sv)
        for x, y in flat:
            u, v = piece_uv(piece, side, x, y)
            p = on_drape(u, v)
            sv.append(tuple(p) if p is not None else (0.0, 0.0, 0.0))
            suv.append((u, v))
        for f in faces:
            g = [base + k for k in f]
            sf.append(list(reversed(g)) if side < 0 else g)
smesh = bpy.data.meshes.new("JacketSim")
smesh.from_pydata(sv, [], sf)
uvs = smesh.uv_layers.new(name="pattern")
for poly in smesh.polygons:
    for li in poly.loop_indices:
        uvs.data[li].uv = suv[smesh.loops[li].vertex_index]
sbm = bmesh.new()
sbm.from_mesh(smesh)
before = len(sbm.verts)
bmesh.ops.remove_doubles(sbm, verts=sbm.verts[:], dist=0.002)
bmesh.ops.recalc_face_normals(sbm, faces=sbm.faces[:])
sbm.to_mesh(smesh)
sbm.free()
sim = bpy.data.objects.new("JacketSim", smesh)
bpy.context.collection.objects.link(sim)
smesh.materials.append(wool)
missing = sum(1 for p in sv if p == (0.0, 0.0, 0.0))
log["sim"] = {"verts": len(smesh.vertices), "merged": before - len(smesh.vertices), "tris": len(smesh.polygons), "offPattern": missing}
say("sim", log["sim"])

# ---- files and pictures ---------------------------------------------------------------------

for obj, tag in ((render, "render"), (sim, "sim")):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, "%s_%s_static.fbx" % (NAME, tag)), use_selection=True,
                             object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
jacket.hide_render = True
jacket.hide_set(True)
sim.hide_render = True
body.data.materials.clear()
body.data.materials.append(grey)
top = max(v.co.z for v in body.data.vertices) if body.matrix_world.is_identity else None
mid = Vector((0.0, float(co[:, 1].mean()), float(co[:, 2].min() + co[:, 2].max()) / 2))
tailor.pictures(os.path.join(OUT, "finished"), mid)
tailor.pictures(os.path.join(OUT, "finished-close"), mid + Vector((0, 0, 0.25)),
                views=(("front", (0, -1.9, 0.05)), ("back", (0, 1.9, 0.05)), ("three-quarter", (1.3, -1.4, 0.2))))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "finish.json"), "w"), indent=1)
say("done", json.dumps(log))
