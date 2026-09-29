"""Work trousers finished: waistband, belt and belt loops, the fly, slanted front pockets, back welts, a render mesh.

    blender -b -P tools/meshgen/blender/finish_trousers.py -- TROUSERS.blend TITAN.json CHARLIE.json OUT_DIR [--name ron_trousers]

WHY, 29 September (the clothing session, CLOTHES.md item 4). The drape
(sew_trousers.py) is the cloth; what a 1990 working man's trousers show on
top of it is made here, each part found on the drape by its place on the flat
pattern (as finish_donkey.py finds the jacket's), so it sits where the
pattern puts it whatever the drape did:
  - the waistband, 34 mm (Charlie's 3% of the waist-to-floor length), sewn
    above the trousers' top edge all round, and a black leather belt over it
    through seven belt loops, a plain buckle at the front (the research:
    production/research/clothing-pipeline/TROUSERS-AND-CAP-2026-09-29.md;
    the photographs: production/reference/work-trousers-and-flat-cap-1990.md);
  - the fly: the left front's shield lying over the centre line, 11 cm long
    (Charlie's 45% of this low front's crotch), curved at its foot;
  - Charlie's slanted front pockets: a lip from 78 mm in from the side on
    the waist down to the side seam 12 cm lower;
  - a welt on each back, 14 cm, 7 cm below the band.
The trousers are skinned in the game, not simulated (the research: close
garments are skinned), so there is one mesh, the render mesh, and no
simulation mesh. OUT_DIR gets NAME_render_static.fbx, NAME.blend, the
pictures and finish.json.
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
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, TITAN, CHARLIE, OUT = argv[0], argv[1], argv[2], argv[3]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "ron_trousers", str)
BAND = opt("--band", 34.0)                  # mm
TWILL_T = 0.0015
log = {"blend": BLEND, "pattern": TITAN}


def say(*a):
    print("FINISH", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=BLEND)
trousers = bpy.data.objects["Trousers"]
body = next(o for o in bpy.data.objects if o.type == "MESH" and o is not trousers and not o.hide_render)
for o in list(bpy.data.objects):
    if o.type == "MESH" and o not in (trousers, body):
        bpy.data.objects.remove(o, do_unlink=True)

# ---- the pattern, as sew_trousers.py laid it out -------------------------------------------

pat = json.load(open(TITAN))
parts = pat["parts"]
PART = {"front": next(k for k in parts if k.endswith(".front")), "back": next(k for k in parts if k.endswith(".back"))}
LAYOUT = {("front", 1): (-0.3, 0.0, 1.0), ("back", 1): (0.9, 0.0, 1.0),
          ("front", -1): (-0.8, 0.0, -1.0), ("back", -1): (1.4, 0.0, -1.0)}
ch = json.load(open(CHARLIE))["parts"]
CH_F = ch[next(k for k in ch if k.endswith(".front"))]["points"]


def outline(piece):
    P = parts[PART[piece]]["points"]
    poly = tailor.closed(parts[PART[piece]]["paths"]["seam"]["points"])
    return {"waist": tailor.seg(poly, P["styleWaistOut"], P["styleWaistIn"]),
            "crotch": tailor.seg(poly, P["styleWaistIn"], P["fork"]),
            "outseam": tailor.seg(poly, P["floorOut"], P["styleWaistOut"]), "P": P}


O = {"front": outline("front"), "back": outline("back")}

# ---- the drape found by the pattern's coordinates -------------------------------------------

me = trousers.data
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


def on_drape(u, v):
    hit = UVBVH.ray_cast(Vector((u, v, 1.0)), Vector((0, 0, -1)), 2.0)
    if hit[2] is None:
        hit = UVBVH.find_nearest(Vector((u, v, 0.0)), 0.006)
        if hit[2] is None:
            return None
    i = hit[2]
    a, b, c = (Vector(x) for x in tri_uv[i])
    A, B_, C = (Vector(x) for x in tri_xyz[i])
    return barycentric_transform(Vector((u, v, 0.0)), a, b, c, A, B_, C)


def at(piece, side, x, y):
    lx, ly, sx = LAYOUT[(piece, side)]
    return on_drape(lx + sx * x / 1000.0, ly - y / 1000.0)


bmt = bmesh.new()
bmt.from_mesh(me)
bmt.normal_update()
TBVH = BVHTree.FromBMesh(bmt)
bmt.free()
_bev = tailor.evaluated_copy(body, "BodyNow")
BODY_BVH = tailor.bvh_of(_bev)
bpy.data.objects.remove(_bev, do_unlink=True)


def outward(p):
    _h, n, _i, _d = TBVH.find_nearest(p)
    hit, bn, _i2, _d2 = BODY_BVH.find_nearest(p)
    if n is None:
        return bn if bn is not None else Vector((0, 0, 1))
    away = (p - hit) if hit is not None else Vector((p.x, p.y, 0.0))
    if away.length < 1e-6 and bn is not None:
        away = bn
    return n if n.dot(away) >= 0 else -n


# ---- materials -------------------------------------------------------------------------

twill = tailor.material("M_TrouserTwill", tuple(float(c) for c in opt("--rgb", "0.072,0.072,0.078", str).split(",")), 0.85)
leather = tailor.material("M_BeltLeather", (0.012, 0.010, 0.009), 0.4)
metal = tailor.material("M_BuckleSteel", (0.35, 0.35, 0.36), 0.35)
grey = tailor.material("M_Body", (0.5, 0.5, 0.5))
extras = []


def sheet(name, rows, mat, thickness=TWILL_T, offset=1.0, closed_rows=False):
    verts, faces = [], []
    w = len(rows[0])
    for r in rows:
        verts.extend(tuple(p) for p in r)
    for i in range(len(rows) - 1):
        for j in range(w - 1 + (1 if closed_rows else 0)):
            j1 = (j + 1) % w
            faces.append((i * w + j, i * w + j1, (i + 1) * w + j1, (i + 1) * w + j))
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
    extras.append(o)
    return o


def lift(p, d):
    return p + outward(p) * d


# ---- the waistband, all round, above the trousers' top edge ------------------------------------------
#
# Round the body from the left front's centre line: left front (centre to
# side), left back (side to centre back), right back, right front.

def waist_pts(piece, side, n, reverse):
    line = tailor.resample(O[piece]["waist"], n)          # from the side to the centre
    if reverse:
        line = line[::-1]
    out = []
    for x, y in line:
        p = at(piece, side, x, y)
        below = at(piece, side, x, y + 30.0)
        out.append((p, below))
    return out


ring = (waist_pts("front", 1, 30, True) + waist_pts("back", 1, 30, False)[1:] +
        waist_pts("back", -1, 30, True)[1:] + waist_pts("front", -1, 30, False)[1:])
ring = [(p, q) for p, q in ring if p is not None and q is not None]
band_rows = []
for f in (0.0, 0.5, 1.0):
    row = []
    for p, q in ring:
        up = (p - q).normalized()
        r = p + up * (BAND / 1000.0) * f
        hit, nrm, _i, _d = BODY_BVH.find_nearest(r)
        if hit is not None and (r - hit).dot(nrm) < 0.004:
            r = hit + nrm * 0.004
        row.append(lift(r, 0.001) if f == 0.0 else r)
    band_rows.append(row)
sheet("Waistband", band_rows, twill, thickness=0.003, offset=-1.0, closed_rows=False)
BAND_ROWS = band_rows


def band_point(frac, h, off):
    """A point on the band, `frac` of the way round from the left front's centre line, `h` of the way up it,
    `off` metres out from it."""
    k = frac * (len(ring) - 1)
    i = int(min(len(ring) - 2, math.floor(k)))
    t = k - i
    lo = band_rows[0][i].lerp(band_rows[0][i + 1], t)
    hi = band_rows[2][i].lerp(band_rows[2][i + 1], t)
    p = lo.lerp(hi, h)
    return p + outward(p) * off


# ---- the belt through its loops, a plain buckle at the front -------------------------------------------

belt_rows = []
for h in (0.08, 0.5, 0.92):
    belt_rows.append([band_point(j / 240.0, h, 0.0045) for j in range(241)])
sheet("Belt", belt_rows, leather, thickness=0.004, offset=-1.0)
# the buckle a little left of the centre front, a frame 46 by 42 mm
bk = band_point(0.012, 0.5, 0.009)
n_b = outward(bk)
upb = Vector((0, 0, 1))
side_b = upb.cross(n_b).normalized()
for (cx, cz, w_, h_) in ((0.0, 0.021, 0.046, 0.005), (0.0, -0.021, 0.046, 0.005), (-0.021, 0.0, 0.005, 0.042), (0.021, 0.0, 0.005, 0.042)):
    c = bk + side_b * cx + upb * cz
    rows = [[c + side_b * (sx * w_ / 2) + upb * (sz * h_ / 2) for sx in (-1, 1)] for sz in (-1, 1)]
    sheet("Buckle", rows, metal, thickness=0.004, offset=-1.0)
# seven belt loops: the centre back, each back's middle, each side just behind its seam, each front near its pocket
LOOPS = (0.10, 0.25, 0.375, 0.5, 0.625, 0.75, 0.90)
for fr in LOOPS:
    # FLAT STRIPS SEWN TO THE BAND (the first blind review: 'rods standing off
    # the belt'): down on the cloth at both ends, over the belt between
    rows = []
    for h, dz, off in ((0.0, -0.008, 0.0015), (0.06, 0.0, 0.0062), (0.5, 0.0, 0.0065), (0.94, 0.0, 0.0062), (1.0, 0.004, 0.0015)):
        rows.append([band_point(fr + d / 1600.0, h, off) + Vector((0, 0, dz)) for d in (-5, 0, 5)])
    sheet("BeltLoop", rows, twill, thickness=0.0015, offset=-1.0)
log["waist"] = {"bandMm": BAND, "ringPoints": len(ring), "loops": len(LOOPS)}

# ---- the fly: the left front's shield over the centre line, curved at its foot ---------------------------

P_F = O["front"]["P"]
crotch_f = O["front"]["crotch"]
cf_y = np.array([p[1] for p in crotch_f])
cf_x = np.array([p[0] for p in crotch_f])
order = np.argsort(cf_y)
FLY = opt("--fly", 110.0)
top_y = P_F["styleWaistIn"][1]
fly_rows = []
for j in range(12):
    y = top_y + 3.0 + (FLY - 3.0) * j / 11
    xc = float(np.interp(y, cf_y[order], cf_x[order]))
    width = 36.0 if y < top_y + FLY - 32 else 36.0 * math.sqrt(max(0.0, 1 - ((y - (top_y + FLY - 32)) / 32.0) ** 2))
    row = []
    for i in range(6):
        x = xc - 2.0 - (width - 2.0) * i / 5
        p = at("front", 1, x, y)
        row.append(lift(p, 0.0016) if p is not None else None)
    if all(r is not None for r in row):
        fly_rows.append(row)
if len(fly_rows) > 2:
    sheet("Fly", fly_rows, twill, thickness=0.0015, offset=-1.0)
log["fly"] = {"lengthMm": FLY, "rows": len(fly_rows)}

# ---- Charlie's slanted front pockets: a lip from the waist down to the side seam ---------------------------

st, sb = CH_F.get("slantTop", [73, 134]), CH_F.get("slantBottom", [22, 257])
for side in (1, -1):
    rows = []
    for off in (-2.5, 2.5):
        row = []
        for j in range(12):
            t = j / 11
            x = st[0] + (sb[0] - st[0]) * t
            y = st[1] + (sb[1] - st[1]) * t
            # the lip square to the slant, 8 mm wide
            dx, dy = sb[0] - st[0], sb[1] - st[1]
            L_ = math.hypot(dx, dy)
            p = at("front", side, x + off * dy / L_, y - off * dx / L_)
            row.append(lift(p, 0.0006) if p is not None else None)
        rows.append(row)
    if all(r is not None for rr in rows for r in rr):
        sheet("PocketLip", rows, twill, thickness=0.001, offset=-1.0)
log["frontPockets"] = {"slantTop": st, "slantBottom": sb}

# ---- a welt on each back, 14 cm wide, 7 cm below the band -------------------------------------------------

P_B = O["back"]["P"]
for side in (1, -1):
    wo, wi = P_B["styleWaistOut"], P_B["styleWaistIn"]
    mid_x = 0.5 * (wo[0] + wi[0])
    top_at = 0.5 * (wo[1] + wi[1])
    rows = []
    for dy in (70.0, 82.0):
        row = []
        for i in range(8):
            x = mid_x - 70.0 + 140.0 * i / 7
            p = at("back", side, x, top_at + dy)
            row.append(lift(p, 0.0014) if p is not None else None)
        rows.append(row)
    if all(r is not None for rr in rows for r in rr):
        sheet("BackWelt", rows, twill, thickness=0.002, offset=-1.0)

# ---- worn creases: behind the knees, a bag at each knee, a fold above the hem ----------------------------------
#
# THE FIRST BLIND REVIEW (29 September): 'nowhere is there a crease ... the
# man in 149-009 has bagged knees and soft horizontal folds behind the knees'.
# Skinned trousers make no creases of their own, so the worn ones are laid
# into the cloth: soft, uneven, a few millimetres.
# THE SEAT HANGS, NOT FOLLOWING THE CLEFT (the second blind review: 'at rest
# the seat hugs the buttocks and runs into the cleft'): bridged again, deeper
log["seatBridged"] = tailor.bridge_slices(trousers, opt("--crotch", 0.885) - 0.12, 1.08, opt("--crotch", 0.885),
                                          deepest=opt("--seat-bridge", 0.06), smooth_rounds=16)
log["pushedOut"] = tailor.push_out(trousers, BODY_BVH, 0.003)     # anything the bridging's smoothing left inside
KNEE_Z = opt("--knee-z", 0.54)
KNEE_BAG = opt("--knee-bag", 0.013)
_tco0 = np.array([v.co[:] for v in me.vertices])
_ang0 = np.degrees(np.arctan2(_tco0[:, 0], _tco0[:, 1] + 0.03)) // 10
_top = {}
for a_, z_ in zip(_ang0, _tco0[:, 2]):
    _top[a_] = max(_top.get(a_, -9.0), z_)


def TOP_AT(p):
    return _top.get(math.degrees(math.atan2(p.x, p.y + 0.03)) // 10, p.z)
rng = np.random.default_rng(7)
tco = np.array([v.co[:] for v in me.vertices])
moved_c = 0
for vi, v in enumerate(me.vertices):
    p = Vector(tco[vi])
    if p.z > 0.75:
        continue
    n = outward(p)
    side = 1.0 if p.x > 0 else -1.0
    d = 0.0
    zk = p.z - KNEE_Z
    if n.y > 0.25 and -0.07 < zk < 0.10:                      # behind the knee: three soft folds, tilted a little
        w = math.sin(math.pi * (zk + 0.07) / 0.17) ** 2
        d += 0.0026 * w * math.cos(2 * math.pi * (zk - 0.012 * side * (abs(p.x) - 0.13) / 0.05) / 0.043) * min(1.0, (n.y - 0.25) / 0.4)
    if n.y < -0.25 and -0.06 < zk < 0.15:                     # the knee bagged forward, 1 to 2 cm (the research)
        d += KNEE_BAG * math.exp(-((zk - 0.04) / 0.055) ** 2) * min(1.0, (-n.y - 0.25) / 0.4)
    if n.y < -0.3 and p.z < 0.11:                             # a soft break above the hem where it rests on the foot
        d += 0.006 * math.sin(math.pi * max(0.0, min(1.0, (p.z - 0.03) / 0.08)))
    below_band = TOP_AT(p) - p.z
    if 0.0 < below_band < 0.07 and n.y < 0.2:                 # gathers under the cinched belt, front and sides
        a_ = math.atan2(p.x, -(p.y + 0.03))
        d += 0.0045 * max(0.0, math.cos(7.0 * a_ + 0.6)) ** 2 * (1.0 - below_band / 0.07)
    if d:
        me.vertices[vi].co = tco[vi] + np.array(n) * d
        moved_c += 1
me.update()
log["creases"] = {"points": moved_c, "kneeZ": KNEE_Z}

# ---- the render mesh ------------------------------------------------------------------------------------

render = trousers.copy()
render.data = trousers.data.copy()
render.name = "TrousersRender"
bpy.context.collection.objects.link(render)
render.data.materials.clear()
render.data.materials.append(twill)
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
sol = render.modifiers.new("Solidify", "SOLIDIFY")
sol.thickness, sol.offset = TWILL_T, -1.0
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
say("render", log["render"])

# ---- files and pictures -----------------------------------------------------------------------------------

bpy.ops.object.select_all(action="DESELECT")
render.select_set(True)
bpy.context.view_layer.objects.active = render
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, "%s_render_static.fbx" % NAME), use_selection=True,
                         object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
trousers.hide_render = True
trousers.hide_set(True)
body.data.materials.clear()
body.data.materials.append(grey)
MID = Vector((0.0, -0.02, 0.62))
tailor.pictures(os.path.join(OUT, "finished"), MID,
                views=(("front", (0, -3.6, 0.0)), ("side", (3.6, 0, 0.0)), ("back", (0, 3.6, 0.0)), ("three-quarter", (2.5, -2.6, 0.2))))
tailor.pictures(os.path.join(OUT, "finished-close"), Vector((0.0, -0.05, 0.93)),
                views=(("front", (0, -1.5, 0.05)), ("back", (0, 1.5, 0.05)), ("three-quarter", (1.0, -1.1, 0.15))))
tailor.pictures(os.path.join(OUT, "finished-hem"), Vector((0.0, -0.02, 0.2)),
                views=(("front", (0, -1.4, 0.1)), ("side", (1.4, 0, 0.1))))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "finish.json"), "w"), indent=1)
say("done", json.dumps(log))
