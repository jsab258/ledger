"""Sew and drape FreeSewing's Florent flat cap in Blender, on a head of the pattern's size.

    blender -b -P tools/meshgen/blender/sew_cap.py -- PATTERN.json OUT_DIR [frames]

WHY, 25 September: Jafar's clothing ruling, FreeSewing's open patterns sewn
and draped in Blender; the flat cap first. pattern_panels.py showed the
panels; this sews them. Each panel is cut from the pattern's own seam lines
with the same number of points along both sides of every seam, so the seam
can be sewn point to point; Blender's cloth pulls the seams shut ("sewing
springs") over a head whose hat-line girth is the pattern's head measurement,
and gravity drapes the crown. The brim is the same cloth made stiff, as its
interfacing makes it.

The half on the wearer's left is built and mirrored: the side band and the
brim are each one piece cut on the fold, so their halves are joined at the
fold; the two crown pieces meet at a real centre seam, sewn like the rest.

Writes cap.blend, cap.fbx (metres, Z up, the head's hat-line centre at the
origin, the face towards -Y), four pictures, and cap.json (seam gaps after
sewing, size, triangle count).
"""
import json
import math
import os
import sys
import time

import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT = argv[0], argv[1]
FRAMES = int(argv[2]) if len(argv) > 2 else 90
os.makedirs(OUT, exist_ok=True)
T0 = time.time()

EDGE = 10.0                 # cloth triangle edge, mm
pattern = json.load(open(SRC, encoding="utf-8"))
HEAD = float(pattern["measurements"]["head"])
# The head at the hat line: an ellipse whose girth is the head measurement,
# 80 by 101 mm half-widths (a head is about 1.26 times as long as wide);
# the crown rises 95 mm above it and the face falls 130 mm below.
HA, HB = 80.0 * HEAD / 570.0, 101.0 * HEAD / 570.0
CROWN, FACE = 95.0, 130.0
R_EQ = HEAD / (2 * math.pi)


# ---- the pattern's seam lines ------------------------------------------------

def part(name):
    return pattern["parts"]["florent." + name]


def closed(pts):
    pts = [tuple(p) for p in pts]
    return pts[:-1] if pts[0] == pts[-1] else pts


def near(poly, p):
    d = [(q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 for q in poly]
    return d.index(min(d))


def walk(poly, a, b):
    """Along a closed outline from named point a to b, forwards."""
    i, j, n = near(poly, a), near(poly, b), len(poly)
    out = [poly[i]]
    while i != j:
        i = (i + 1) % n
        out.append(poly[i])
    return out


def length(poly):
    return sum(math.dist(poly[k], poly[k - 1]) for k in range(1, len(poly)))


def resample(poly, n):
    """n equal steps along a polyline: n + 1 points, ends kept."""
    cum = [0.0]
    for k in range(1, len(poly)):
        cum.append(cum[-1] + math.dist(poly[k], poly[k - 1]))
    out = []
    for s in np.linspace(0, cum[-1], n + 1):
        k = max(1, min(len(poly) - 1, int(np.searchsorted(cum, s))))
        t = 0.0 if cum[k] == cum[k - 1] else (s - cum[k - 1]) / (cum[k] - cum[k - 1])
        a, b = poly[k - 1], poly[k]
        out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out


def split_at(poly, s):
    """A polyline cut at arc length s: (before, after), the cut in both."""
    run = 0.0
    for k in range(1, len(poly)):
        d = math.dist(poly[k], poly[k - 1])
        if run + d >= s:
            t = (s - run) / d
            a, b = poly[k - 1], poly[k]
            m = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            return poly[:k] + [m], [m] + poly[k:]
        run += d
    return poly, [poly[-1]]


def steps(*polys):
    return max(2, round(sum(length(p) for p in polys) / len(polys) / EDGE))


top, side, brim = part("top"), part("side"), part("brimTop")
tp, sp, bp = top["points"], side["points"], brim["points"]
top_out = closed(top["paths"]["seam"]["points"])
side_path = [tuple(p) for p in side["paths"]["side"]["points"]]
brim_out = closed(brim["paths"]["seam"]["points"])

# crown piece: the side seam, the back of the head opening, the centre seam
top_side = walk(top_out, tp["midFront"], tp["backEdge"])
top_back = walk(top_out, tp["backEdge"], tp["midBack"])
top_centre = walk(top_out, tp["midBack"], tp["midFront"])
# side band, one half: its upper edge sews to the crown, its lower edge is
# the head opening, whose front part takes the brim
k_tip = near(side_path, sp["tip"])
band_upper = side_path[:k_tip + 1]                  # foldTop -> tip
band_lower = side_path[k_tip:]                      # tip -> foldBottom
# brim, one half: inner edge innerMid -> tipRight sews to the band's front
brim_inner = list(reversed(walk(brim_out, bp["tipRight"], bp["innerMid"])))
brim_outer = walk(brim_out, bp["outerMid"], bp["tipRight"])
brim_front_len = length(brim_inner)
lower_front, lower_back = split_at(list(reversed(band_lower)), brim_front_len)
# lower_front: foldBottom -> where the brim ends; lower_back: on to the tip

N_SIDE = steps(top_side, band_upper)
N_CENTRE = steps(top_centre)
N_BACK = steps(top_back)
N_BRIM = steps(brim_inner, lower_front)
N_LBACK = steps(lower_back)
N_FOLD = steps([sp["foldBottom"], sp["foldTop"]])
N_BOUT = steps(brim_outer)
N_BFOLD = steps([bp["outerMid"], bp["innerMid"]])


def loop(segments):
    """A closed boundary from (name, polyline, steps): its points, and each
    named segment's point indices in order, both ends included."""
    pts, idx = [], {}
    for name, poly, n in segments:
        r = resample(poly, n)
        start = len(pts)
        pts.extend(r[:-1])
        idx[name] = list(range(start, start + n)) + [None]
    total = len(pts)
    for name in idx:
        s = idx[name]
        s[-1] = (s[-2] + 1) % total
    return pts, idx


def inside(poly, xy):
    poly = np.asarray(poly)
    x, y = xy[:, 0][:, None], xy[:, 1][:, None]
    x1, y1 = poly[:, 0][None], poly[:, 1][None]
    x2, y2 = np.roll(poly[:, 0], -1)[None], np.roll(poly[:, 1], -1)[None]
    cross = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1)
    return cross.sum(axis=1) % 2 == 1


def clearance(poly, xy):
    a = np.asarray(poly)
    b = np.roll(a, -1, axis=0)
    ab = b - a
    t = np.clip(((xy[:, None] - a[None]) * ab[None]).sum(-1) / ((ab * ab).sum(-1)[None] + 1e-12), 0, 1)
    proj = a[None] + t[..., None] * ab[None]
    return np.sqrt(((xy[:, None] - proj) ** 2).sum(-1)).min(axis=1)


def panel(boundary):
    """Even triangles filling a boundary: a hexagonal lattice inside it,
    kept half a triangle clear of the edge, joined by constrained Delaunay."""
    b = np.asarray(boundary)
    lo, hi = b.min(axis=0), b.max(axis=0)
    rows = np.arange(lo[1], hi[1] + EDGE, EDGE * math.sqrt(3) / 2)
    grid = []
    for r, y in enumerate(rows):
        xs = np.arange(lo[0] + (EDGE / 2 if r % 2 else 0), hi[0] + EDGE, EDGE)
        grid.extend((x, y) for x in xs)
    grid = np.asarray(grid)
    keep = inside(boundary, grid)
    grid = grid[keep]
    grid = grid[clearance(boundary, grid) > EDGE * 0.55]
    verts = [Vector(p) for p in boundary] + [Vector(p) for p in grid]
    nb = len(boundary)
    edges = [(k, (k + 1) % nb) for k in range(nb)]
    out_v, _e, out_f, orig_v, _oe, _of = delaunay_2d_cdt(verts, edges, [list(range(nb))], 1, 1e-6, True)
    # keep the input order: boundary first, so seam indices stay valid; a
    # point the triangulation adds (where two lines cross) goes on the end
    remap, flat = {}, [tuple(v) for v in verts]
    for k, ov in enumerate(orig_v):
        if ov:
            remap[k] = ov[0]
        else:
            remap[k] = len(flat)
            flat.append(tuple(out_v[k]))
    if len(flat) > len(verts):
        print("SEW %d points added where lines cross" % (len(flat) - len(verts)))
    faces = [[remap[k] for k in f] for f in out_f]
    return flat, faces


# ---- where each piece starts, around the head --------------------------------

def ring(alpha):
    """The hat line at azimuth alpha (0 at the front, rising to the left)."""
    return np.array([HA * math.sin(alpha), -HB * math.cos(alpha), 0.0])


def outward(alpha):
    n = np.array([math.sin(alpha) / HA, -math.cos(alpha) / HB, 0.0])
    return n / np.linalg.norm(n)


def circle(poly):
    """Least-squares circle through a polyline: centre, radius."""
    a = np.asarray(poly)
    A = np.c_[2 * a, np.ones(len(a))]
    c = np.linalg.lstsq(A, (a ** 2).sum(1), rcond=None)[0]
    return c[:2], math.sqrt(c[2] + c[0] ** 2 + c[1] ** 2)


def wrap(flat, edge, start, tilt, drop=0.0, clear=6.0):
    """A piece shaped like a cone's unrolled strip, rolled round the hat line:
    its edge `edge` (a polyline that starts at `start`) lies along the hat
    line from the front, the rest leans away from it at `tilt` degrees
    (outward and up; `drop` tips it down instead)."""
    c, r0 = circle(edge)
    s0 = np.asarray(start) - c
    a0 = math.atan2(s0[1], s0[0])
    far = np.asarray(edge[-1]) - c
    sign = 1.0 if math.remainder(math.atan2(far[1], far[0]) - a0, 2 * math.pi) > 0 else -1.0
    out = []
    t, d = math.radians(tilt), math.radians(drop)
    for p in flat:
        v = np.asarray(p) - c
        phi = sign * math.remainder(math.atan2(v[1], v[0]) - a0, 2 * math.pi)
        alpha = r0 * phi / R_EQ
        h = abs(np.linalg.norm(v) - r0)
        n = outward(alpha)
        if drop:
            pos = ring(alpha) + n * (h * math.cos(d) + clear) + np.array([0, 0, -h * math.sin(d) - 2.0])
        else:
            pos = ring(alpha) + n * (h * math.sin(t) + clear) + np.array([0, 0, h * math.cos(t) + 2.0])
        out.append(pos)
    return out


def roof(flat, centre):
    """The crown piece laid over the head like a roof: its centre seam runs
    front to back over the top, its side edge hangs down the left."""
    c = np.asarray(sorted(centre))
    xmax = max(p[0] for p in flat)
    out = []
    for x, y in flat:
        yc = np.interp(x, c[:, 0], c[:, 1])      # the centre seam's own curve
        psi = math.pi * min(max(x / xmax, 0.0), 1.0)
        qy, qz = -1.3 * HB * math.cos(psi), 25.0 + (CROWN + 8.0) * math.sin(psi)
        th = max(y - yc, 0.0) / 100.0
        out.append(np.array([100.0 * math.sin(th), qy, qz - 100.0 * (1 - math.cos(th))]))
    return out


# ---- build the pieces --------------------------------------------------------

pieces = {}
tb, t_idx = loop([("side", top_side, N_SIDE), ("back", top_back, N_BACK), ("centre", top_centre, N_CENTRE)])
tv, tf = panel(tb)
pieces["top"] = dict(flat=tv, faces=tf, idx=t_idx, pos=roof(tv, top_centre))

bb, b_idx = loop([("upper", band_upper, N_SIDE),
                  ("lower_back", list(reversed(lower_back)), N_LBACK),
                  ("lower_front", list(reversed(lower_front)), N_BRIM),
                  ("fold", [sp["foldBottom"], sp["foldTop"]], N_FOLD)])
bv, bf = panel(bb)
pieces["band"] = dict(flat=bv, faces=bf, idx=b_idx,
                      pos=wrap(bv, list(reversed(band_lower)), sp["foldBottom"], tilt=35))

rb, r_idx = loop([("inner", brim_inner, N_BRIM), ("outer", list(reversed(brim_outer)), N_BOUT),
                  ("fold", [bp["outerMid"], bp["innerMid"]], N_BFOLD)])
rv, rf = panel(rb)
pieces["brim"] = dict(flat=rv, faces=rf, idx=r_idx,
                      pos=wrap(rv, brim_inner, bp["innerMid"], tilt=0, drop=8))

verts, faces, uvs, groups = [], [], [], {"brim": [], "band": [], "top": [], "opening": []}
at = {}                                  # (piece, side, local index) -> global
UV_SCALE = 1.0 / 800.0                   # the flat pattern is the UV map

for name, pc in pieces.items():
    welded = set(pc["idx"]["fold"]) if "fold" in pc["idx"] else set()
    for side_ in (1, -1):
        for k, (p, f2) in enumerate(zip(pc["pos"], pc["flat"])):
            if side_ == -1 and k in welded:
                at[(name, -1, k)] = at[(name, 1, k)]
                continue
            at[(name, side_, k)] = len(verts)
            verts.append(((p[0] * side_) / 1000.0, p[1] / 1000.0, p[2] / 1000.0))
            uvs.append((f2[0] * UV_SCALE * side_ + 0.5, f2[1] * UV_SCALE))
            groups[name].append(len(verts) - 1)
            if (name == "band" and (k in pc["idx"]["lower_back"] or k in pc["idx"]["lower_front"])) or                     (name == "brim" and k in pc["idx"]["inner"]):
                groups["opening"].append(len(verts) - 1)
        for f in pc["faces"]:
            g = [at[(name, side_, k)] for k in f]
            faces.append(g if side_ == 1 else list(reversed(g)))


SEAMS = {}


def seam(a, b, reverse=False):
    """Pairs of global vertices sewn together, point for point."""
    pa, sa, sega = a
    pb, sb, segb = b
    ia = pieces[pa]["idx"][sega]
    ib = pieces[pb]["idx"][segb]
    if reverse:
        ib = list(reversed(ib))
    assert len(ia) == len(ib), (sega, segb, len(ia), len(ib))
    pairs = [(at[(pa, sa, x)], at[(pb, sb, y)]) for x, y in zip(ia, ib)]
    SEAMS.setdefault("%s %s to %s %s" % (pa, sega, pb, segb), []).extend(pairs)
    return pairs


sewing = []
for s in (1, -1):
    sewing += seam(("top", s, "side"), ("band", s, "upper"))              # crown to band
    sewing += seam(("brim", s, "inner"), ("band", s, "lower_front"), reverse=True)
sewing += seam(("top", 1, "centre"), ("top", -1, "centre"))               # centre seam
sewing = [(a, b) for a, b in sewing if a != b]
sewing = list(dict.fromkeys(tuple(sorted(p)) for p in sewing))

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene

me = bpy.data.meshes.new("cap")
me.from_pydata(verts, sewing, faces)
me.validate()
uv = me.uv_layers.new(name="pattern")
for poly in me.polygons:
    for li in poly.loop_indices:
        uv.data[li].uv = uvs[me.loops[li].vertex_index]
cap = bpy.data.objects.new("FlatCap", me)
scn.collection.objects.link(cap)
for gname, ids in groups.items():
    vg = cap.vertex_groups.new(name=gname)
    vg.add(ids, 1.0, "REPLACE")

# the head: an egg, 95 mm of crown above the hat line, the face below
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0)
head = bpy.context.active_object
head.name = "Head"
for v in head.data.vertices:
    x, y, z = v.co
    v.co = Vector((x * HA / 1000.0, y * HB / 1000.0, z * (CROWN if z > 0 else FACE) / 1000.0))
head.modifiers.new("Collision", "COLLISION")
head.collision.thickness_outer = 0.001
head.collision.cloth_friction = 20.0

cl = cap.modifiers.new("Cloth", "CLOTH")
st, cs = cl.settings, cl.collision_settings
st.quality = 12
st.mass = 0.01
st.air_damping = 5.0
st.tension_stiffness = st.compression_stiffness = 40.0
st.shear_stiffness = 30.0
st.bending_stiffness = 5.0       # tweed holds its shape: at 2 it crumpled, at 10 it stood up like a bag
# the head opening stays on the hat line, as a cap's band does once it is on:
# unpinned, the sewing drew the band up off the head and the cap rode away
st.vertex_group_mass = "opening"
st.pin_stiffness = 5.0
st.use_sewing_springs = True
st.sewing_force_max = 5.0        # at 0.3 the seams stayed open; 8 balled the cloth before the opening was pinned
# the brim is the same cloth stiffened (its interfacing)
st.vertex_group_bending = "brim"
st.bending_stiffness_max = 400.0
st.vertex_group_structural_stiffness = "brim"
st.tension_stiffness_max = st.compression_stiffness_max = 200.0
cs.use_collision = True
# thin margins: the band sits a few millimetres off the head, and a wide
# margin both stretches it and throws the cap off the head at the start
cs.distance_min = 0.0015
cs.collision_quality = 4
cs.use_self_collision = False     # the sewn edges start touching
cs.self_distance_min = 0.0015
# sewn first, weightless, then let the crown fall: with gravity from the
# start the pieces slid off the head before the seams had closed
SEWN = min(40, FRAMES)
gw = st.effector_weights
gw.gravity = 0.0
gw.keyframe_insert("gravity", frame=1)
gw.keyframe_insert("gravity", frame=SEWN)
gw.gravity = 1.0
gw.keyframe_insert("gravity", frame=SEWN + 10)
cl.point_cache.frame_start = 1
cl.point_cache.frame_end = FRAMES
scn.frame_start, scn.frame_end = 1, FRAMES

gaps = []
for fr in range(1, FRAMES + 1):
    scn.frame_set(fr)
    if fr % 15 == 0 or fr in (1, FRAMES):
        ev = cap.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
        g = [(ev.vertices[a].co - ev.vertices[b].co).length * 1000 for a, b in sewing]
        gaps.append((fr, round(max(g), 1), round(sum(g) / len(g), 2)))
        zs = [v.co.z * 1000 for v in ev.vertices]
        worst = {k: round(max((ev.vertices[a].co - ev.vertices[b].co).length * 1000 for a, b in v), 1)
                 for k, v in SEAMS.items()}
        print("SEW   widest by seam: %s" % worst, flush=True)
        if fr == 1:
            for k, v in SEAMS.items():
                a_, b_ = max(v, key=lambda ab: (ev.vertices[ab[0]].co - ev.vertices[ab[1]].co).length)
                print("SEW   %s worst pair %d %s / %d %s" % (k, a_, tuple(round(c * 1000) for c in ev.vertices[a_].co),
                                                         b_, tuple(round(c * 1000) for c in ev.vertices[b_].co)))
        print("SEW frame %d: widest seam gap %.1f mm, mean %.2f mm; cap from %.0f to %.0f mm high"
              % (fr, max(g), sum(g) / len(g), min(zs), max(zs)), flush=True)

# keep the draped shape: close each seam at its midpoint, drop the threads
ev = cap.evaluated_get(bpy.context.evaluated_depsgraph_get())
done = bpy.data.meshes.new_from_object(ev)
cap.modifiers.clear()
old = cap.data
cap.data = done
bpy.data.meshes.remove(old)
bm = bmesh.new()
bm.from_mesh(done)
bm.verts.ensure_lookup_table()
for a, b in sewing:
    m = (bm.verts[a].co + bm.verts[b].co) / 2
    bm.verts[a].co = m
    bm.verts[b].co = m
bmesh.ops.delete(bm, geom=[e for e in bm.edges if not e.link_faces], context="EDGES")
bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.0005)
# ONE WAY OUT: each piece was cut facing whichever way its outline ran, so
# neighbours faced opposite ways, and the thickness stepped in and out at
# every seam, which showed as a ragged dark line. Face them all alike, away
# from the head.
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
if sum(f.normal.dot(f.calc_center_median()) for f in bm.faces) < 0:
    bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
bm.to_mesh(done)
bm.free()
for p in done.polygons:
    p.use_smooth = True
# the simulation's crumples are sharper than wool's: soften them, then a
# finer surface, then the cloth's thickness
sm = cap.modifiers.new("Soften", "SMOOTH")
sm.factor, sm.iterations = 0.5, 4
cap.modifiers.new("Finer", "SUBSURF").levels = 1
sol = cap.modifiers.new("Thickness", "SOLIDIFY")
sol.thickness = 0.002
sol.offset = 1.0

# ---- pictures, file, report ---------------------------------------------------

mat = bpy.data.materials.new("TweedDark")   # a new name: Unreal keeps an old material of the same name
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.07, 0.06, 0.05, 1)
mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
cap.data.materials.append(mat)
skin = bpy.data.materials.new("Head")
skin.diffuse_color = (0.55, 0.42, 0.36, 1)
head.data.materials.append(skin)
scn.render.engine = "BLENDER_WORKBENCH"
scn.display.shading.light = "STUDIO"
scn.display.shading.color_type = "MATERIAL"
scn.render.resolution_x = scn.render.resolution_y = 720
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
scn.collection.objects.link(cam)
scn.camera = cam
cam.data.lens = 85
for label, az, el in (("front", 0, 8), ("side", 90, 8), ("three-quarter", 40, 18), ("back", 180, 12)):
    a, e = math.radians(az), math.radians(el)
    d = 1.1
    cam.location = (d * math.sin(a) * math.cos(e), -d * math.cos(a) * math.cos(e), 0.03 + d * math.sin(e))
    direction = Vector((0, 0, 0.03)) - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    scn.render.filepath = os.path.join(OUT, "cap-%s.png" % label)
    bpy.ops.render.render(write_still=True)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "cap.blend"))
bpy.ops.object.select_all(action="DESELECT")
cap.select_set(True)
bpy.context.view_layer.objects.active = cap
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, "cap.fbx"), use_selection=True,
                         apply_scale_options="FBX_SCALE_UNITS", use_mesh_modifiers=True,
                         axis_forward="-Y", axis_up="Z", mesh_smooth_type="FACE")
dims = [round(v * 1000, 1) for v in cap.dimensions]
report = {"headMm": HEAD, "vertices": len(done.vertices), "triangles": len(done.polygons),
          "seamPairs": len(sewing), "gapsByFrame": gaps, "sizeMm": dims,
          "minutes": round((time.time() - T0) / 60, 1)}
json.dump(report, open(os.path.join(OUT, "cap.json"), "w"), indent=1)
print("CAP " + json.dumps(report))
