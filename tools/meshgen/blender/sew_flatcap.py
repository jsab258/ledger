"""A flat cap from FreeSewing's Florent, sewn round the wearer's own head, its crown pulled forward onto the peak.

    blender -b -P tools/meshgen/blender/sew_flatcap.py -- FLORENT.json BODY.fbx OUT_DIR [--name ron_flatcap]

WHY, 29 September (the clothing session, CLOTHES.md item 4). The cap of 25
September (sew_cap.py) was rejected by Jafar ("not like this"): draped on an
egg of the pattern's girth, its front band stood up and its crown domed, an
eight-panel cap's shape, not a flat cap's. The research
(production/research/clothing-pipeline/TROUSERS-AND-CAP-2026-09-29.md) and the
photographs (production/reference/work-trousers-and-flat-cap-1990.md: Peter
Fryer's Smith's Dock, 1990 to 1991) say a flat cap's crown is pulled forward
and fixed to a short stiff peak, so its front is nearly level and it sits low
and close. Florent is drafted for the head's girth; its pieces are the crown
(two halves, a centre seam), the band (one piece on the fold, 77 mm tall at
the front, running out to nothing at the sides) and the peak.

HOW (the trousers' way, tailor.relax, no Blender cloth):
  - the head's hat line: a section through the head 9 cm under its top,
    tipped 5 degrees up at the front; the cap's opening (the band's lower
    edge, then the crown's back edges) is held on it, 3 mm out;
  - the peak is rigid (buckram-stiffened): the brim pattern's inner edge on
    the hat line across the forehead, the peak running out forward and 12
    degrees down;
  - the crown and band laid over the head, sewn by projection with a small
    pull down, the crown's front centre held on the peak's top 15 mm behind
    its edge (the snap), so the band folds under and the crown lies forward;
  - pressed, then a render mesh: tweed, the peak 5 mm thick.
OUT_DIR gets NAME.blend, NAME_render_static.fbx, pictures and cap.json.
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, BODY, OUT = argv[0], argv[1], argv[2]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


EDGE = opt("--edge", 7.0)
NAME = opt("--name", "ron_flatcap", str)
DROP = opt("--drop", 0.098)           # the hat line under the top of the head, m (its middle)
TILT = opt("--tilt", 7.0)             # degrees, the front higher
PEAK_DOWN = opt("--peak-down", 12.0)
SNAP_BACK = opt("--snap-back", 3.0)   # mm behind the peak's edge
CLEAR = opt("--clear", 0.004)
log = {"pattern": SRC, "body": BODY}


def say(*a):
    print("CAP", *a, flush=True)


pat = json.load(open(SRC))
parts = pat["parts"]
TP, SP, BP = parts["florent.top"], parts["florent.side"], parts["florent.brimTop"]
T, S, B = TP["points"], SP["points"], BP["points"]
L = tailor.length

# ---- the pieces --------------------------------------------------------------------------------

top_poly = tailor.closed(TP["paths"]["seam"]["points"])
top_segs = {"centre": tailor.seg(top_poly, T["midFront"], T["midMid"]) + tailor.seg(top_poly, T["midMid"], T["midBack"])[1:],
            "back": tailor.seg(top_poly, T["midBack"], T["backEdge"]),
            "side": tailor.seg(top_poly, T["backEdge"], T["midFront"])}
side_poly = tailor.closed(SP["paths"]["seam"]["points"])
def way_through(poly, a, b, via):
    """The outline from a to b the way that passes `via` (seg's shorter way was the wrong one for the band's
    upper edge: fold and lower edge together are shorter, and the band was sewn to the crown by its lower edge)."""
    fwd = tailor.walk(poly, a, b)
    bwd = list(reversed(tailor.walk(poly, b, a)))
    d = lambda line: min(math.dist(q, via) for q in line)
    return fwd if d(fwd) <= d(bwd) else bwd


band_segs = {"upper": way_through(side_poly, S["foldTop"], S["tip"], S["outerTop"]),
             "lower": tailor.seg(side_poly, S["tip"], S["foldBottom"]),
             "fold": tailor.seg(side_poly, S["foldBottom"], S["foldTop"])}
brim_poly = tailor.closed(BP["paths"]["seam"]["points"])
N = {"centre": max(2, round(L(top_segs["centre"]) / EDGE)), "back": max(2, round(L(top_segs["back"]) / EDGE)),
     "side": max(2, round(max(L(top_segs["side"]), L(band_segs["upper"])) / EDGE)),
     "lower": max(2, round(L(band_segs["lower"]) / EDGE)), "fold": max(2, round(L(band_segs["fold"]) / EDGE))}
top_pts, top_idx = tailor.loop([("centre", top_segs["centre"], N["centre"]), ("back", top_segs["back"], N["back"]),
                                ("side", top_segs["side"], N["side"])])
band_pts, band_idx = tailor.loop([("upper", band_segs["upper"], N["side"]), ("lower", band_segs["lower"], N["lower"]),
                                  ("fold", band_segs["fold"], N["fold"])])
top_flat, top_faces = tailor.panel(top_pts, EDGE)
band_flat, band_faces = tailor.panel(band_pts, EDGE)
log["pattern"] = {k: round(L(v)) for k, v in list(top_segs.items()) + [("band " + k, v) for k, v in band_segs.items()]}
say("pattern mm", log["pattern"])

# ---- the head and its hat line ------------------------------------------------------------------

arm, body = tailor.load_body(BODY, lod=opt("--lod", 1, int))
BVH = tailor.bvh_of(body)
hco = np.array([body.matrix_world @ v.co for v in body.data.vertices])
TOP_Z = float(hco[:, 2].max())
hd = hco[hco[:, 2] > TOP_Z - 0.25]
CY = float(0.5 * (hd[:, 1].min() + hd[:, 1].max()))
t = math.radians(TILT)
PLANE_NO = Vector((0.0, math.sin(t), math.cos(t)))    # the front higher (29 September: the sign sat the first cap at the eyes)
ring = max(tailor.section_loops(body, (0.0, CY, TOP_Z - DROP), PLANE_NO), key=len)
# OVER THE EARS, NOT ROUND THEM (the first review: the cap sat high; lower,
# the section runs round the ears): the hat line is the section's hull, each
# hull point put back on the tipped plane
_h2 = np.array(tailor._hull2(ring[:, :2]))
_p0 = np.array([0.0, CY, TOP_Z - DROP])
_z = _p0[2] - (PLANE_NO.y * (_h2[:, 1] - _p0[1])) / PLANE_NO.z
ring = np.column_stack([_h2, _z])
_d = np.linalg.norm(np.diff(np.vstack([ring, ring[:1]]), axis=0), axis=1)
_s = np.concatenate([[0.0], np.cumsum(_d)])
_t = np.arange(0.0, _s[-1], 0.004)
ring = np.column_stack([np.interp(_t, _s, np.append(ring[:, k], ring[0, k])) for k in range(3)])
# in order round the head from the front centre towards the wearer's left (+x), resampled every 2 mm
c2 = ring[:, :2].mean(axis=0)
ang = np.arctan2(ring[:, 1] - c2[1], ring[:, 0] - c2[0])
ring = ring[np.argsort(ang)]
k0 = int(np.argmin(ring[:, 1]))                                  # the front (-y)
ring = np.roll(ring, -k0, axis=0)
if ring[len(ring) // 8, 0] < 0:                                  # the wearer's left first
    ring = np.concatenate([ring[:1], ring[1:][::-1]])
ring = np.vstack([ring, ring[:1]])
seglen = np.linalg.norm(np.diff(ring, axis=0), axis=1)
RS = np.concatenate([[0.0], np.cumsum(seglen)])
GIRTH = float(RS[-1])
log["hatLine"] = {"girthMm": round(GIRTH * 1000), "frontZ": round(float(ring[0, 2]), 3)}
say("hat line", log["hatLine"])


def ring_at(s):
    """The hat line `s` metres round from the front centre towards the left (negative: towards the right), 3 mm out."""
    s = s % GIRTH
    p = Vector([float(np.interp(s, RS, ring[:, k])) for k in range(3)])
    q = Vector([float(np.interp((s + 0.004) % GIRTH, RS, ring[:, k])) for k in range(3)])
    tang = (q - p).normalized()
    out = tang.cross(PLANE_NO).normalized()
    if out.dot(Vector((p.x - c2[0], p.y - c2[1], 0.0))) < 0:
        out = -out
    return p + out * 0.003, out


# the pattern's opening round the head: the band's lower edge from the front centre, then the crown's back edge
band_lower = L(band_segs["lower"]) / 1000.0
crown_back = L(top_segs["back"]) / 1000.0
OPEN = 2 * (band_lower + crown_back)
SCALE = GIRTH / OPEN
log["opening"] = {"patternMm": round(OPEN * 1000), "scaleToHatLine": round(SCALE, 3)}
say("opening", log["opening"])

# ---- the peak: rigid, its inner edge along the forehead -------------------------------------------------

brim_in = tailor.seg(brim_poly, B["tipLeft"], B["tipRight"])
if min(p[1] for p in brim_in) < 20:                              # the inner (concave) edge runs through innerMid
    brim_in = [p for p in brim_in]
inner_len = L(tailor.seg(brim_poly, B["tipRight"], B["innerMid"])) + L(tailor.seg(brim_poly, B["innerMid"], B["tipLeft"]))
brim_flat, brim_faces = tailor.panel(brim_poly, 6.0)
bin_line = tailor.resample(tailor.seg(brim_poly, B["tipRight"], B["innerMid"]) + tailor.seg(brim_poly, B["innerMid"], B["tipLeft"])[1:], 80)
bin_arr = np.array(bin_line)
bin_s = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(bin_arr, axis=0), axis=1))])
down = math.radians(PEAK_DOWN)


# the inner edge as a function of x (the pattern is symmetric about x = 0, y down): its height and the arc
# along it from the right tip
_ix = np.array([p[0] for p in bin_line])
_iy = np.array([p[1] for p in bin_line])
_io = np.argsort(_ix)


_ox = np.array([p[0] for p in tailor.seg(brim_poly, B["tipRight"], B["outerMid"]) + tailor.seg(brim_poly, B["outerMid"], B["tipLeft"])])
_oy = np.array([p[1] for p in tailor.seg(brim_poly, B["tipRight"], B["outerMid"]) + tailor.seg(brim_poly, B["outerMid"], B["tipLeft"])])
_oo = np.argsort(_ox)
PEAK_W = opt("--peak-width", 0.8)                                # of the pattern's width across the forehead
DEPTH = (B["outerMid"][1] - B["innerMid"][1]) / 1000.0 * opt("--peak-depth", 0.85)


def peak_point(x, y):
    """A peak pattern point: across the forehead by where it lies across the peak (its x, as arc along the inner
    edge); out from the hat line by the same share of the peak's depth there as it has of the pattern's (the
    peak's true depth, 58 mm at the middle, running out to nothing at the tips), and down. (Measured straight
    down the pattern, the first tries threw the ends of the peak out sideways, a halo.)"""
    y_in = float(np.interp(x, _ix[_io], _iy[_io]))
    y_out = float(np.interp(x, _ox[_oo], _oy[_oo]))
    s_in = float(np.interp(x, _ix[_io], bin_s[_io])) / bin_s[-1]
    share = max(0.0, min(1.0, (y - y_in) / max(1e-6, y_out - y_in)))
    u_ = 2.0 * s_in - 1.0
    dist = share * DEPTH * max(0.0, 1.0 - u_ * u_) ** 0.6
    s_ring = (s_in - 0.5) * (inner_len / 1000.0) * SCALE * PEAK_W
    p, out = ring_at(s_ring)
    return p + out * dist * math.cos(down) - Vector((0, 0, 1)) * dist * math.sin(down)


peak_co = [peak_point(x, y) for x, y in brim_flat]
pm = bpy.data.meshes.new("Peak")
pm.from_pydata([tuple(p) for p in peak_co], [], brim_faces)
pm.validate()
peak = bpy.data.objects.new("Peak", pm)
bpy.context.collection.objects.link(peak)
PEAK_BVH = tailor.bvh_of(peak)
edge_front = peak_point(B["outerMid"][0], B["outerMid"][1])
inner_front = peak_point(B["innerMid"][0], B["innerMid"][1])
fwd = (edge_front - inner_front)
SNAP = edge_front - fwd.normalized() * (SNAP_BACK / 1000.0) + Vector((0, 0, 0.006))
SEW_ON = opt("--sew-on", 105.0)                                  # mm of the crown's front edge each way from the middle


def snap_line(t):
    """A point `t` metres across the peak from its middle (left positive) on the line SNAP_BACK behind its edge,
    6 mm above it."""
    s_mid = 0.5 + t / (inner_len / 1000.0 * SCALE * PEAK_W) * 0.9  # a little inside, as the peak narrows
    x_ = float(np.interp(s_mid * bin_s[-1], bin_s, bin_arr[:, 0]))
    y_out = float(np.interp(x_, _ox[_oo], _oy[_oo]))
    q = peak_point(x_, y_out - SNAP_BACK)
    return q + Vector((0, 0, 0.0025))                             # on the peak, the cloth's thickness above it
log["peak"] = {"depthMm": round(fwd.length * 1000), "downDeg": PEAK_DOWN, "snap": [round(c, 3) for c in SNAP]}
say("peak", log["peak"])

# ---- the crown and band laid over the head ------------------------------------------------------------

C3 = Vector((float(c2[0]), float(c2[1]), TOP_Z - 0.10))       # the head's middle, under the crown
front_top = ring_at(0.0)[0] + Vector((0, 0, 0.077))


def over_head(u, v):
    """The crown half's pattern point: `u` 0..1 front to back along its centre line, `v` metres out to the side;
    the centre line runs from above the band's front up over the head to the back of the hat line."""
    back_pt = ring_at(GIRTH / 2)[0]
    a0 = math.atan2(front_top.z - C3.z, front_top.y - C3.y)
    a1 = math.atan2(back_pt.z - C3.z, back_pt.y - C3.y)
    # over the top: from the front (about 130 degrees) down through straight up (90) to the back (about 0)
    while a1 > a0:
        a1 -= 2 * math.pi
    a = a0 + (a1 - a0) * u
    dirv = Vector((0.0, math.cos(a), math.sin(a)))
    hit, _n, _i, _d = BVH.ray_cast(C3 + dirv * 0.25, -dirv, 0.3)
    base = hit if hit is not None else C3 + dirv * 0.11
    r = (base - C3).length + 0.012
    phi = v / max(0.05, r)
    # turned about the front-back axis through the head's middle, towards the wearer's left (+x)
    p = C3 + dirv * r
    local = p - C3
    R = Matrix.Rotation(phi, 3, Vector((0, 1, 0)))
    return C3 + R @ local


centre_line = np.array(top_segs["centre"])
cs = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(centre_line, axis=0), axis=1))])


def crown_point(x, y):
    """The crown half laid as a wide, shallow disc: its centre line along the head's middle a little above it,
    each point out to the side by its distance from the centre line, dropping gently towards the edge."""
    d2 = np.hypot(centre_line[:, 0] - x, centre_line[:, 1] - y)
    k = int(np.argmin(d2))
    mid = over_head(cs[k] / cs[-1], 0.0)
    v = float(d2[k]) / 1000.0
    return Vector((v, mid.y, max(ring_at(0.0)[0].z + 0.01, mid.z + 0.012 - 1.2 * v * v)))


lower_line = np.array(band_segs["lower"])[::-1]                  # from the front centre to the tip
ls_ = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(lower_line, axis=0), axis=1))])


FLARE = math.radians(opt("--flare", 55.0))


def band_point(x, y):
    """The band flared out from the hat line, as its pattern asks: its upper edge (422 mm a side) is far longer
    than its lower (245), so it stands out like a cone's skirt under a crown about 30 cm across. (Laid upright,
    the first runs crumpled that length into a ridge along the seam, a pillbox's wall.)"""
    d2 = np.hypot(lower_line[:, 0] - x, lower_line[:, 1] - y)
    k = int(np.argmin(d2))
    p, out = ring_at(ls_[k] / 1000.0 * SCALE)
    d = float(d2[k]) / 1000.0
    return p + (Vector((0, 0, 1)) * math.cos(FLARE) + out * math.sin(FLARE)) * d + out * 0.004


def mirror(pts):
    return [(-p[0], p[1], p[2]) for p in pts]


G = tailor.Garment()
top_l = [tuple(crown_point(x, y)) for x, y in top_flat]
band_l = [tuple(band_point(x, y)) for x, y in band_flat]
AT = {}
AT["TL"] = G.add("crown_l", top_flat, top_faces, top_l, layout=(0.0, 0.0))
AT["TR"] = G.add("crown_r", top_flat, top_faces, mirror(top_l), layout=(0.0, -0.3), mirror=True)
AT["BL"] = G.add("band", band_flat, band_faces, band_l, layout=(0.5, 0.0))
fold = {k: AT["BL"][k] for k in band_idx["fold"]}
# THE BAND'S OTHER HALF IS FLIPPED ACROSS ITS FOLD, which runs along the
# pattern's x (foldBottom to foldTop at y = 0), so y changes sign; flipped
# across x instead (as the jacket's back is, whose fold runs down y) the shared
# fold points carried the other half's lengths, 30 cm long, and threw a strip
# of cloth out sideways (the cap's sixth to eighth runs)
band_flat_r = [(x, -y) for x, y in band_flat]
band_faces_r = [list(reversed(f)) for f in band_faces]
AT["BR"] = G.add("band", band_flat_r, band_faces_r, mirror(band_l), layout=(0.5, 0.0), share=fold)


def ids(p, idx, s):
    return [AT[p][k] for k in idx[s]]


G.seam("crown centre", ids("TL", top_idx, "centre"), ids("TR", top_idx, "centre"))
G.seam("crown to band", ids("TL", top_idx, "side"), list(reversed(ids("BL", band_idx, "upper"))))
G.seam("crown to band", ids("TR", top_idx, "side"), list(reversed(ids("BR", band_idx, "upper"))))
cap = G.build("Cap")
cap.shape_key_clear()
co0 = tailor.coords(cap, evaluated=False)
log["place"] = {"points": len(G.verts), "seamGapsMm": tailor.seam_gaps(co0, G.seams)}
say("placed", log["place"])
grey0 = tailor.material("M_Body", (0.5, 0.5, 0.5))
body.data.materials.append(grey0)
HEADC = Vector((0.0, CY, TOP_Z - 0.09))
CAP_VIEWS = (("front", (0, -1.1, 0.02)), ("side", (1.1, 0, 0.02)), ("back", (0, 1.1, 0.02)), ("three-quarter", (0.75, -0.8, 0.12)))
tailor.pictures(os.path.join(OUT, "place"), HEADC, views=CAP_VIEWS, res=(700, 600))

# ---- the opening held on the hat line, the crown's front on the peak ---------------------------------------

me = cap.data
fixed = []
for side_, (tk, bk_) in ((1, ("TL", "BL")), (-1, ("TR", "BR"))):
    lower = ids(bk_, band_idx, "lower")[::-1]                    # front centre to tip
    for j, vi in enumerate(lower):
        s_ = j / max(1, len(lower) - 1) * band_lower * SCALE
        me.vertices[vi].co = ring_at(side_ * s_)[0]
        fixed.append(vi)
    back = ids(tk, top_idx, "back")[::-1]                        # tip end (backEdge) to the centre back
    for j, vi in enumerate(back):
        s_ = (band_lower + j / max(1, len(back) - 1) * crown_back) * SCALE
        me.vertices[vi].co = ring_at(side_ * s_)[0]
        fixed.append(vi)
    # THE CROWN'S FRONT SEWN ONTO THE PEAK (the research: the top's front 'sewn
    # or pinned to the brim's upper face 1 to 2 cm behind the brim's edge'):
    # the crown's side edge from its front centre, SEW_ON mm each way, along a
    # line on the peak's top SNAP_BACK mm behind its edge (with the band's top
    # edge sewn to it); a single snap point left the band's front to stand up
    side_ids = ids(tk, top_idx, "side")[::-1]                    # from the front centre (midFront) back
    band_up = ids(bk_, band_idx, "upper")                         # from the fold (foldTop) back
    side_pts = np.array([top_flat[k] for k in top_idx["side"][::-1]])
    run_ = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(side_pts, axis=0), axis=1))])
    for j, vi in enumerate(side_ids):
        if run_[j] > SEW_ON:
            break
        q = snap_line(side_ * run_[j] / 1000.0)
        me.vertices[vi].co = q
        fixed.append(vi)
        if j < len(band_up):
            me.vertices[band_up[j]].co = q
            fixed.append(band_up[j])
# BLOCKED (a flat cap is shaped on a block): the middle of the crown's centre line held level a little above
# the top of the head, so the top lies flat instead of following the head's dome
BLOCK = opt("--block", 0.0)                                      # m above the top of the head; 0 = not blocked
if BLOCK > 0:
    cen = ids("TL", top_idx, "centre")
    cpts = np.array([top_flat[k] for k in top_idx["centre"]])
    crun = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(cpts, axis=0), axis=1))])
    y_front, y_back = CY - opt("--block-front", 0.075), CY + opt("--block-back", 0.035)
    for j, vi in enumerate(cen):
        u = crun[j] / crun[-1]
        if 0.28 <= u <= 0.62:
            yy = y_front + (y_back - y_front) * (u - 0.28) / 0.34
            me.vertices[vi].co = Vector((0.0, yy, TOP_Z + BLOCK))
            fixed.append(vi)
            fixed.append(ids("TR", top_idx, "centre")[j])
            me.vertices[ids("TR", top_idx, "centre")[j]].co = Vector((0.0, yy, TOP_Z + BLOCK))
me.update()
# the head and the peak together are what the cloth lies on
col = body.copy()
col.data = body.data.copy()
bpy.context.collection.objects.link(col)
bpy.ops.object.select_all(action="DESELECT")
col.select_set(True)
peak_c = peak.copy()
peak_c.data = peak.data.copy()
bpy.context.collection.objects.link(peak_c)
# the peak as one surface facing up, the cloth to lie on its top (as a thin solid, a point caught inside it
# was pushed from face to face and walked 30 cm out sideways: the cap's sixth run)
_pb = bmesh.new()
_pb.from_mesh(peak_c.data)
_pb.normal_update()
for f in _pb.faces:
    if f.normal.z < 0:
        f.normal_flip()
_pb.to_mesh(peak_c.data)
_pb.free()
peak_c.select_set(True)
bpy.context.view_layer.objects.active = col
bpy.ops.object.join()
COL_BVH = tailor.bvh_of(col)
bpy.data.objects.remove(col, do_unlink=True)
gap, edges_ = tailor.relax(cap, G.sewing, fixed, COL_BVH, iterations=opt("--relax", 300, int), clear=CLEAR, report=say)
log["sew"] = {"widestGapMm": gap, "edgesVsPattern": edges_}
say("sewn", log["sew"])
tailor.pictures(os.path.join(OUT, "sewn"), HEADC, views=CAP_VIEWS, res=(700, 600))
co = tailor.coords(cap, evaluated=False)
_wide = [i for i in range(len(co)) if abs(co[i][0]) > 0.16]
say("wider than the head after sewing:", len(_wide), sorted(set(G.piece_of[i] for i in _wide)),
    [(i, G.piece_of[i], [round(float(c), 3) for c in co[i]], [round(float(c), 3) for c in G.flat[i]], i in fixed) for i in _wide[:6]])
merged = tailor.weld(cap, G.sewing, co, max_gap=0.02)
fixed_now = []
bm = bmesh.new()
bm.from_mesh(cap.data)
bm.verts.ensure_lookup_table()
fx_co = [Vector(co[i]) for i in fixed]
for v in bm.verts:
    if min((v.co - f).length for f in fx_co) < 1e-5:
        fixed_now.append(v.index)
bm.free()
gap2, edges2 = tailor.relax(cap, [], fixed_now, COL_BVH, iterations=opt("--settle", 150, int), clear=CLEAR, report=say,
                            gravity=opt("--gravity", 0.0001), length_rounds=8)
_before = tailor.coords(cap, evaluated=False)
press_ = tailor.press(cap, COL_BVH, rounds=opt("--press", 60, int), smooth=opt("--smooth", 0.35), lengths=opt("--press-lengths", 5, int))
_after = tailor.coords(cap, evaluated=False)
_mv = np.linalg.norm(_after - _before, axis=1)
say("press moved most", [(int(i), round(float(_mv[i]) * 1000), [round(float(c), 3) for c in _before[i]]) for i in np.argsort(-_mv)[:4]])
log["edgeSmoothed"] = tailor.smooth_edges_of(cap, float(ring[:, 2].max()) + 0.03, rounds=16)
# THE SEAM BETWEEN CROWN AND BAND SMOOTHED ALONG ITSELF (the close views: it
# came out crinkled where the band's extra length gathered into it)
seam_line = {}
cco = tailor.coords(cap, evaluated=False)
from mathutils.kdtree import KDTree as _KD
_kd = _KD(len(cco))
for i, q in enumerate(cco):
    _kd.insert(Vector(q), i)
_kd.balance()
for side_, (tk, bk_) in ((1, ("TL", "BL")), (-1, ("TR", "BR"))):
    line_ids = []
    for a_, b_ in zip(ids(tk, top_idx, "side"), list(reversed(ids(bk_, band_idx, "upper")))):
        mid_ = Vector((co[a_] + co[b_]) / 2)
        _p, j, _d = _kd.find(mid_)
        if _d < 0.02 and (not line_ids or line_ids[-1] != j):
            line_ids.append(j)
    seam_line[side_] = line_ids
cme = cap.data
for _ in range(20):
    for side_, line_ids in seam_line.items():
        new = {}
        for k in range(1, len(line_ids) - 1):
            a_, b_, c_ = (cme.vertices[line_ids[k + d]].co for d in (-1, 0, 1))
            new[line_ids[k]] = b_ * 0.5 + (a_ + c_) * 0.25
        for j, v in new.items():
            cme.vertices[j].co = v
cme.update()
# THE CLOTH ON THE PEAK LIES ON IT (the close views: kept 4 mm off by the
# collision, the band's front stood clear of the peak and the forehead showed
# through the gap, a second brim): anything within 12 mm above the peak's top (22 left a sawtooth edge)
# goes down to 1.5 mm above it
_pb2 = bmesh.new()
_pb2.from_mesh(peak.data)
_pb2.transform(peak.matrix_world)
PEAK_TREE = BVHTree.FromBMesh(_pb2)
_pb2.free()
laid = 0
for v in cme.vertices:
    w = cap.matrix_world @ v.co
    hit, _n, _i, dist = PEAK_TREE.ray_cast(w, Vector((0, 0, -1)), opt("--lay", 0.012))
    if hit is not None:
        v.co = cap.matrix_world.inverted() @ (hit + Vector((0, 0, 0.0015)))
        laid += 1
cme.update()
log["laidOnPeak"] = laid
# and nothing inside the head after the smoothing (the second attempt's back: the head came through at two
# corners where the edge smoothing pulled the cloth in)
log["pushedOutOfHead"] = tailor.push_out(cap, BVH, 0.003)
log["seamSmoothed"] = {k: len(v) for k, v in seam_line.items()}
log["settle"] = {"welded": merged, "edgesVsPattern": edges2, "press": press_}
say("settled", log["settle"])

# ---- the render mesh: tweed, the peak 5 mm thick ----------------------------------------------------------

tweed = tailor.material("M_CapTweed", tuple(float(c) for c in opt("--rgb", "0.16,0.13,0.10", str).split(",")), 0.9)
grey = tailor.material("M_Body", (0.5, 0.5, 0.5))
render = cap.copy()
render.data = cap.data.copy()
render.name = "CapRender"
bpy.context.collection.objects.link(render)
rb = bmesh.new()
rb.from_mesh(render.data)
# SMALL HOLES FILLED (the second attempt's back: two holes where the band's
# tip meets the crown, three pieces at one corner): any opening of up to 14
# edges; the cap's own opening round the head has hundreds
filled = bmesh.ops.holes_fill(rb, edges=[e for e in rb.edges if e.is_boundary], sides=14)
log["holesFilled"] = len(filled.get("faces", []))
bmesh.ops.recalc_face_normals(rb, faces=rb.faces[:])
rb.normal_update()
vote = sum(f.normal.dot(f.calc_center_median() - C3) for f in list(rb.faces)[::5])
if vote < 0:
    bmesh.ops.reverse_faces(rb, faces=rb.faces[:])
rb.to_mesh(render.data)
rb.free()
render.data.materials.clear()
render.data.materials.append(tweed)
s1 = render.modifiers.new("Solidify", "SOLIDIFY")
s1.thickness, s1.offset = 0.002, -1.0
peak.data.materials.append(tweed)
# every face of the peak up before it is thickened (turned either way, its rim came out speckled)
_pk = bmesh.new()
_pk.from_mesh(peak.data)
_pk.normal_update()
for f in _pk.faces:
    if f.normal.z < 0:
        f.normal_flip()
_pk.to_mesh(peak.data)
_pk.free()
s2 = peak.modifiers.new("Solidify", "SOLIDIFY")
s2.thickness, s2.offset = 0.0035, -1.0
bv = peak.modifiers.new("Bevel", "BEVEL")
bv.width, bv.segments = 0.0016, 3
for o in (render, peak):
    for p in o.data.polygons:
        p.use_smooth = True
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    for mdf in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=mdf.name)
bpy.ops.object.select_all(action="DESELECT")
render.select_set(True)
peak.select_set(True)
bpy.context.view_layer.objects.active = render
bpy.ops.object.join()
render = bpy.context.active_object
log["render"] = {"verts": len(render.data.vertices), "tris": sum(len(p.vertices) - 2 for p in render.data.polygons)}
say("render", log["render"])
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, "%s_render_static.fbx" % NAME), use_selection=True,
                         object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
cap.hide_render = True
cap.hide_set(True)
body.data.materials.clear()
body.data.materials.append(grey)
HEADC = Vector((0.0, CY, TOP_Z - 0.09))
tailor.pictures(os.path.join(OUT, "cap"), HEADC,
                views=(("front", (0, -1.1, 0.02)), ("side", (1.1, 0, 0.02)), ("back", (0, 1.1, 0.02)), ("three-quarter", (0.75, -0.8, 0.12))),
                res=(700, 600))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "cap.json"), "w"), indent=1)
say("done")
