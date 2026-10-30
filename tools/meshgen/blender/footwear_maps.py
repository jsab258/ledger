"""A finished, skinned pair of boots or shoes given its texture maps: UVs once, then the project's three maps drawn by
script from the surface itself, its occlusion baked; the same UVs carried to every pair of the same mesh.

    blender -b --factory-startup -P tools/meshgen/blender/footwear_maps.py -- SRC_SKINNED.fbx OUT_DIR
        [--name boots] [--tex 1024] [--pad 8] [--carry OTHER_SKINNED.fbx OTHER_OUT_DIR] [--ao-samples 128]
        [--seed 1990] [--stage all|uv] [--keep-uvs] [--no-export] [--welt-stitch 2.8]

WHY, 30 October 2026 (Ron's and Tom's work boots: plain black leather derbies made by script, four slots with flat
colours, read in the game as flat black blobs; their README: "leather grain, stitching and scuffs are for textures").
The project's map convention (production/art/clothing/tom-outfit/BAKE-PLAN-2026-10-27.md; tools/ue/import_garments.py's
packed_material): a colour map with occlusion in alpha (tinted by the ID: 0 times Tint, 0.5 times TapeColour, 0.75 the
flat TeethColour), a DirectX normal map, and a packed map with roughness (R), the part ID (G) and metal (B); 1024 for
footwear (production/specs/asset-budgets.json, garment_shoes).

THE METHOD:
1. UVS, ONCE, FROM THE MESH'S OWN PARTS: each boot's upper is a solidified shell (its outer and inner halves by vertex
   order, the rim between); its outer shell cut where a derby's own seams are: the vamp from the quarters along the
   quarter line (from the throat down to the welt on each side), the quarters open up the instep's middle from the throat
   to the collar and joined round the heel; the part under the foot (inside the sole) cut off at the welt and drawn
   small; the inner shell and its bottom drawn small (seen only at the collar); the sole cut into its welt top, its edge
   (two strips, cut at the heel and the toe) and its tread; laces and eyelets by smart projection. Unwrapped by angle,
   islands scaled to one texel density (the hidden ones smaller), packed with --pad pixels between islands.
2. THE MAPS DRAWN FROM THE SURFACE, NOT FROM THE LAYOUT: every texel's place on the mesh (position, normal, the
   MikkTSpace tangent and bitangent the game and Blender both use), so every feature is a function of the 3D surface
   and no UV seam can show in it: the leather's pebble grain (cellular noise in 3D), the vamp's creases at the ball
   line, a derby's construction (the quarters lying over the vamp, the eyelet facings, the back stay, the collar's
   stitch, each edge a step with its stitch rows), the welt's stitch round the foot, the sole's edge as a band (its
   rounded top and bottom edges, the welt line, the heel's breast), a tread underneath, laces braided, eyelets plain
   metal; the wear: the toe and heel scuffed (rougher, a little lighter, scratches), dust low on the upper. Heights in
   millimetres, turned into tangent-space normals from their surface gradient in the texel's own tangent frame.
3. OCCLUSION baked by Cycles on the pair itself (no body: the game shades the body against the boot), into alpha.
4. THE PAIRS: the same UVs written into every given skinned FBX loop for loop (the meshes must match face for face),
   re-exported with the settings they were written with (pose_skinned.py --export's: smoothing by face, no leaf bones,
   no animation), the weights untouched, and checked point for point against the original.

OUT_DIR gets NAME_colour_ao.png, NAME_normal_dx.png (green flipped, for Unreal), NAME_normal_gl.png (for Blender),
NAME_packed.png, NAME_uv_layout.png, NAME_skinned.fbx (the source pair with the UVs), NAME_maps.blend and NAME_maps.json
(the checks); each --carry OUT_DIR gets its NAME_skinned.fbx and maps-carry.json.
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
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT = argv[0], argv[1]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
NAME = opt("--name", "boots", str)
TEX = opt("--tex", 1024, int)
PAD = opt("--pad", 8, int)
AO_SAMPLES = opt("--ao-samples", 128, int)
SEED = opt("--seed", 1990, int)
STAGE = opt("--stage", "all", str)
# --keep-uvs: the pair already carries this tool's UVs (a reshaped pair, its points moved): no unwrap and no pack, the
# islands read from the UVs, the hidden parts (the upper's foot, the lining's) from their islands' texel density; the
# maps drawn afresh on the new surface. --no-export: no FBX written (the reshape wrote it)
KEEP_UVS = "--keep-uvs" in argv
NO_EXPORT = "--no-export" in argv
WSTITCH = opt("--welt-stitch", 2.8)    # mm in from the welt's edge (2.2 for a welt drawn in to 3 to 4 mm)
CARRY = []
for i_, a_ in enumerate(argv):
    if a_ == "--carry":
        CARRY.append((argv[i_ + 1], argv[i_ + 2]))
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
LOG = {"src": SRC, "tex": TEX, "pad": PAD, "checks": {}}


def say(*a):
    print("FOOTMAPS %6.1fs" % (time.time() - T0), *a, flush=True)


# ---- the pair ------------------------------------------------------------------------------------------------------
def load_pair(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    mesh = next(o for o in new if o.type == "MESH")
    arm = next((o for o in new if o.type == "ARMATURE"), None)
    return mesh, arm


bpy.ops.wm.read_factory_settings(use_empty=True)
pair, arm = load_pair(SRC)
me = pair.data
MW = pair.matrix_world.copy()
SLOT = {m.name.split(".")[0]: i for i, m in enumerate(me.materials)}
say("pair", pair.name, len(me.vertices), "points", len(me.polygons), "faces", SLOT)
CO = np.array([MW @ v.co for v in me.vertices])
FACE_MAT = np.array([p.material_index for p in me.polygons])
FACE_C = np.array([MW @ p.center for p in me.polygons])
FACE_N = np.array([(MW.to_3x3() @ p.normal).normalized() for p in me.polygons])

# connected parts
bm = bmesh.new()
bm.from_mesh(me)
bm.verts.ensure_lookup_table()
bm.faces.ensure_lookup_table()
comp_of = np.full(len(me.polygons), -1)
comps = []
for f in bm.faces:
    if comp_of[f.index] >= 0:
        continue
    stack, cur = [f], []
    comp_of[f.index] = len(comps)
    while stack:
        g = stack.pop()
        cur.append(g.index)
        for v in g.verts:
            for h in v.link_faces:
                if comp_of[h.index] < 0:
                    comp_of[h.index] = len(comps)
                    stack.append(h)
    comps.append(np.array(sorted(cur)))
# each part's side by its weights (the left boot weighted to *_l)
gname = {g.index: g.name for g in pair.vertex_groups}
vside = np.zeros(len(me.vertices))
for v in me.vertices:
    for g in v.groups:
        n_ = gname[g.group]
        vside[v.index] += g.weight * (1 if n_.endswith("_l") else -1 if n_.endswith("_r") else 0)
comp_side = []
comp_verts = []
for c in comps:
    vs = sorted({v.index for i in c for v in bm.faces[int(i)].verts})
    comp_verts.append(np.array(vs))
    comp_side.append(0 if vside[vs].sum() > 0 else 1)          # 0 left, 1 right
comp_mat = [int(np.bincount(FACE_MAT[c]).argmax()) for c in comps]
say("parts", len(comps), "by slot", {k: sum(1 for m in comp_mat if m == i) for k, i in SLOT.items()})

# ---- each boot's frame: along the foot (heel to toe), across it (to the outside), up -------------------------------
Z = np.array([0.0, 0.0, 1.0])
BOOT = {}
for side in (0, 1):
    up_c = [i for i, c in enumerate(comps) if comp_mat[i] == SLOT["M_Upper"] and comp_side[i] == side]
    so_c = [i for i, c in enumerate(comps) if comp_mat[i] == SLOT["M_Sole"] and comp_side[i] == side]
    assert len(up_c) == 1 and len(so_c) == 1, (up_c, so_c)
    uv_ = comp_verts[up_c[0]]
    nh = len(uv_) // 2
    outer, inner = uv_[:nh], uv_[nh:]
    thick = np.linalg.norm(CO[outer] - CO[inner], axis=1)
    assert thick.std() < 1e-4, "the upper is not a solidified shell in vertex order"
    sp = CO[comp_verts[so_c[0]]]
    c2 = sp[:, :2].mean(axis=0)
    _u, _s, vt = np.linalg.svd(sp[:, :2] - c2)
    D = np.array([vt[0, 0], vt[0, 1], 0.0])
    if D[1] > 0:                                             # the figure faces -y: the toe is the -y end
        D = -D
    E = np.cross(Z, D) * (1 if side == 0 else -1)            # to the boot's outside (+x on the left foot)
    po = CO[outer]
    s_raw = po @ D
    s0 = float(s_raw.min())
    L = float(s_raw.max() - s0)
    BOOT[side] = dict(upper=up_c[0], sole=so_c[0], outer=outer, inner=inner, thick=float(thick.mean()), D=D, E=E, s0=s0,
                      L=L)
say("boots", {k: dict(L=round(v["L"], 4), D=v["D"].round(3).tolist(), thick=round(v["thick"], 4)) for k, v in BOOT.items()})


def s_of(p, b):
    return p @ b["D"] - b["s0"]


def e_of(p, b):
    return p @ b["E"]


# the upper's own floor and middle along the foot (5 mm bins of its outer points)
for side, b in BOOT.items():
    po = CO[b["outer"]]
    ss, ee = s_of(po, b), e_of(po, b)
    bins = np.arange(-0.005, b["L"] + 0.01, 0.005)
    zf, ec, sb = [], [], []
    for x0 in bins:
        sel = np.abs(ss - x0) < 0.006
        if sel.sum() < 4:
            continue
        zf.append(po[sel, 2].min())
        ec.append(0.5 * (ee[sel].max() + ee[sel].min()))
        sb.append(x0)
    sb, zf, ec = np.array(sb), np.array(zf), np.array(ec)
    for _ in range(3):
        zf[1:-1] = 0.25 * zf[:-2] + 0.5 * zf[1:-1] + 0.25 * zf[2:]
        ec[1:-1] = 0.25 * ec[:-2] + 0.5 * ec[1:-1] + 0.25 * ec[2:]
    b.update(sb=sb, zf=zf, ec=ec)
    b["top"] = float(po[:, 2].max())
    # the ball joint along the foot
    if arm is not None:
        bn = arm.data.bones.get("ball_" + ("l" if side == 0 else "r"))
        hd = np.array(arm.matrix_world @ bn.head_local) if bn else None
        b["s_ball"] = float(s_of(hd, b)) if bn else 0.72 * b["L"]
    else:
        b["s_ball"] = 0.72 * b["L"]


def zfloor(s, b):
    return np.interp(s, b["sb"], b["zf"])


def ecentre(s, b):
    return np.interp(s, b["sb"], b["ec"])


def h_of(p, b):
    return p[..., 2] - zfloor(s_of(p, b), b)


def erel(p, b):
    s = s_of(p, b)
    return e_of(p, b) - ecentre(s, b)


def emid(p, b):
    """Across the foot from its middle line: the width's middle at the heel, the lacing's middle over the instep."""
    s = s_of(p, b)
    w = np.clip((s - 0.15 * b["L"]) / (0.30 * b["L"]), 0.0, 1.0)
    w = w * w * (3 - 2 * w)
    lace = np.interp(s, b["lace_s"], b["lace_e"]) if "lace_s" in b else ecentre(s, b)
    return e_of(p, b) - (w * lace + (1 - w) * ecentre(s, b))


def elace(p, b):
    """Across the foot from the lacing's middle line (the instep's top; the width's middle beyond the lacing)."""
    s = s_of(p, b)
    if "lace_s" not in b:
        return erel(p, b)
    return e_of(p, b) - np.interp(s, b["lace_s"], b["lace_e"])


# ---- the lacing: the eyelets' rows, the throat, the quarter lines --------------------------------------------------
def bvh_of_faces(fids):
    bm_ = bmesh.new()
    vmap = {}
    for fi in fids:
        f = bm.faces[int(fi)]
        vs = []
        for v in f.verts:
            if v.index not in vmap:
                vmap[v.index] = bm_.verts.new(MW @ v.co)
            vs.append(vmap[v.index])
        bm_.faces.new(vs)
    bm_.normal_update()
    return BVHTree.FromBMesh(bm_), bm_


for side, b in BOOT.items():
    eyes = [i for i, c in enumerate(comps) if comp_mat[i] == SLOT["M_Eyelet"] and comp_side[i] == side]
    cen = np.array([CO[comp_verts[i]].mean(axis=0) for i in eyes])
    # the eyelets in pairs by height (each pair one across the lacing), the inner (medial) one of each nearer the middle
    cen = cen[np.argsort(cen[:, 2])]
    med, lat = [], []
    for k in range(0, len(cen) - 1, 2):
        a_, c_ = cen[k], cen[k + 1]
        (med if e_of(a_, b) < e_of(c_, b) else lat).append(a_)
        (lat if e_of(a_, b) < e_of(c_, b) else med).append(c_)
    med, lat = np.array(med), np.array(lat)
    b["eyes_med"], b["eyes_lat"] = med, lat
    # the lacing's middle along the foot (the instep's top), from the pairs' middles
    lm = 0.5 * (med + lat)
    ls_ = s_of(lm, b)
    o_ = np.argsort(ls_)
    b["lace_s"], b["lace_e"] = ls_[o_], e_of(lm, b)[o_]
    oset_ = set(b["outer"].tolist())
    outer_faces = np.array([fi for fi in comps[b["upper"]] if all(v in oset_ for v in me.polygons[int(fi)].vertices)])
    b["outer_faces"] = outer_faces
    b["bvh"], b["bvh_bm"] = bvh_of_faces(outer_faces)
    mids = 0.5 * (med + lat)
    down = mids[0] - mids[1]
    down /= np.linalg.norm(down)
    thr = mids[0] + down * 0.014
    hit = b["bvh"].find_nearest(Vector(thr))[0]
    b["throat"] = np.array(hit)
    say("side", side, "eyelets", len(med), "pairs; throat s %.3f h %.3f; ball s %.3f; L %.3f" % (
        s_of(b["throat"], b), h_of(b["throat"], b), b["s_ball"], b["L"]))


def snap(points, b):
    out = []
    for p in points:
        out.append(np.array(b["bvh"].find_nearest(Vector(p))[0]))
    return np.array(out)


def resample(poly, step=0.001, closed=False):
    P = np.array(poly)
    if closed:
        P = np.vstack([P, P[:1]])
    seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    n = max(2, int(cum[-1] / step) + 1)
    t = np.linspace(0, cum[-1], n)
    return np.column_stack([np.interp(t, cum, P[:, k]) for k in range(3)])


def plane_curve(b, p0, nrm, keep):
    """The outer shell cut by a plane: its section's points (ordered along the cut), those passing keep(p)."""
    bm_ = b["bvh_bm"].copy()
    res = bmesh.ops.bisect_plane(bm_, geom=bm_.verts[:] + bm_.edges[:] + bm_.faces[:], plane_co=Vector(p0),
                                 plane_no=Vector(nrm), dist=1e-7)
    cut = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    pts_ok = {}
    adj = {}
    for e in cut:
        a, c = e.verts
        for v in (a, c):
            pts_ok[v] = keep(np.array(v.co))
        if pts_ok[a] and pts_ok[c]:
            adj.setdefault(a, []).append(c)
            adj.setdefault(c, []).append(a)
    # the longest chain
    best = []
    seen = set()
    for st in adj:
        if st in seen:
            continue
        comp = []
        stack = [st]
        while stack:
            v = stack.pop()
            if v in seen:
                continue
            seen.add(v)
            comp.append(v)
            stack.extend(adj[v])
        if len(comp) > len(best):
            best = comp
    ends = [v for v in best if len(adj[v]) == 1] or best[:1]
    chain = [ends[0]]
    prev = None
    while True:
        nx = [w for w in adj[chain[-1]] if w is not prev and w not in chain]
        if not nx:
            break
        prev = chain[-1]
        chain.append(nx[0])
    out = np.array([tuple(v.co) for v in chain])
    bm_.free()
    return out


for side, b in BOOT.items():
    D, E = b["D"], b["E"]
    T_ = b["throat"]
    # THE QUARTER LINE, each side: from the throat down to the welt a little behind it (a derby's quarters lie over the
    # vamp from the bottom of the facing to the sole), the plane through the throat, that welt point and across the foot
    curves = {}
    for sg, nm in ((1, "lat"), (-1, "med")):
        sw = s_of(T_, b) - (0.016 if sg > 0 else 0.008)
        Wp = np.array([0.0, 0.0, 0.0]) + D * (sw + b["s0"]) + E * (ecentre(sw, b) + sg * 0.05)
        Wp[2] = zfloor(sw, b)
        # the plane contains the line throat -> W and the across-the-foot direction at the throat
        n_ = np.cross(Wp - T_, E)
        n_ /= np.linalg.norm(n_)
        if n_ @ D < 0:
            n_ = -n_
        c = plane_curve(b, T_, n_, lambda p, sg=sg: sg * elace(p, b) > -0.002 and h_of(p, b) > 0.003)
        if np.linalg.norm(c[0] - T_) > np.linalg.norm(c[-1] - T_):
            c = c[::-1]
        curves["quarter_" + nm] = (resample(c), n_)
    # THE FACINGS: each row of eyelets, its inner edge 7 mm in from the eyelets' centres towards the middle, from the
    # throat up past the top eyelet to the collar
    med, lat = b["eyes_med"], b["eyes_lat"]
    for rows, nm in ((med, "med"), (lat, "lat")):
        other = lat if rows is med else med
        pts = [T_]
        for i in range(len(rows)):
            to_mid = 0.5 * (rows[i] + other[i]) - rows[i]
            pts.append(rows[i] + to_mid / np.linalg.norm(to_mid) * 0.007)
        up = pts[-1] - pts[-2]
        up /= np.linalg.norm(up)
        for k in range(1, 6):
            pts.append(pts[len(rows)] + up * 0.006 * k)
        raw = resample(pts, 0.002)
        c = snap(raw, b)
        c = c[np.linalg.norm(c - raw, axis=1) < 0.004]        # past the collar the snap jumps: cut there
        curves["facing_" + nm] = (snap(resample(c, 0.001), b), None)
    # THE BACK STAY: two lines up the heel's back, 10 mm either side of its middle at the welt, 7 mm at the collar
    sb_ = 0.004
    for sg, nm in ((1, "lat"), (-1, "med")):
        A = D * (sb_ + b["s0"]) + E * (ecentre(sb_, b) + sg * 0.010)
        A[2] = zfloor(sb_, b) + 0.004
        Bp = D * (sb_ + b["s0"]) + E * (ecentre(sb_, b) + sg * 0.007)
        Bp[2] = b["top"]
        n_ = np.cross(Bp - A, D)
        n_ /= np.linalg.norm(n_)
        c = plane_curve(b, A, n_, lambda p: s_of(p, b) < 0.06 and h_of(p, b) > 0.003)
        if c[0][2] > c[-1][2]:
            c = c[::-1]
        curves["backstay_" + nm] = (resample(c), n_)
    # THE COLLAR: the outer shell's top edge
    obm = b["bvh_bm"]
    bnd = [e for e in obm.edges if e.is_boundary]
    adj = {}
    for e in bnd:
        a, c = e.verts
        adj.setdefault(a, []).append(c)
        adj.setdefault(c, []).append(a)
    # the collar is the boundary loop with the highest points (the other is the welt-side bottom, if open)
    loops = []
    seen = set()
    for st in adj:
        if st in seen:
            continue
        lp = [st]
        seen.add(st)
        while True:
            nx = [w for w in adj[lp[-1]] if w not in seen]
            if not nx:
                break
            seen.add(nx[0])
            lp.append(nx[0])
        loops.append(np.array([tuple(v.co) for v in lp]))
    collar = max(loops, key=lambda l_: l_[:, 2].mean())
    curves["collar"] = (resample(collar, 0.001, closed=True), None)
    b["curves"] = curves
    say("side", side, "curves", {k: (len(v[0]), round(float(np.sum(np.linalg.norm(np.diff(v[0], axis=0), axis=1))), 3))
                                for k, v in curves.items()})

# THE SOLE'S TWO RINGS (its top edge and its bottom edge, each in order round the foot) from its side faces; the heel's
# front where the top steps down from the heel's height to the forepart's
for side, b in BOOT.items():
    sf = comps[b["sole"]]
    zmid = 0.5 * (CO[comp_verts[b["sole"]], 2].max() + CO[comp_verts[b["sole"]], 2].min())
    rings = {}
    for top in (True, False):
        adj = {}
        for fi in sf:
            f = bm.faces[int(fi)]
            # an edge of the ring: both its ends on this ring, on a face reaching the other ring (the side's faces; read
            # from the points, not the faces' tilt, which a sprung toe changes)
            if all((CO[v.index, 2] > zmid) == top for v in f.verts):
                continue
            for e in f.edges:
                a_, c_ = e.verts
                if all((CO[v.index, 2] > zmid) == top for v in (a_, c_)):
                    adj.setdefault(a_.index, set()).add(c_.index)
                    adj.setdefault(c_.index, set()).add(a_.index)
        st = next(iter(adj))
        ring = [st]
        prev = None
        while True:
            nx = [w for w in adj[ring[-1]] if w != prev and w not in ring]
            if not nx:
                break
            prev = ring[-1]
            ring.append(nx[0])
        rings[top] = CO[np.array(ring)]
        b["ring_top_ix" if top else "ring_bot_ix"] = np.array(ring)
    b["ring_top"], b["ring_bot"] = rings[True], rings[False]
    # the heel's front: where the bottom's waist starts to lift off the ground, going forward from the heel
    rb_ = rings[False]
    sb_ = s_of(rb_, b)
    zb_ = rb_[:, 2]
    lift = [sb_[i] for i in np.argsort(sb_) if sb_[i] < 0.5 * b["L"] and zb_[i] > zb_.min() + 0.0008]
    b["s_heelfront"] = float(min(lift)) - 0.004 if lift else 0.25 * b["L"]
    b["sole_top"] = float(rings[True][:, 2].max())
    b["sole_bot"] = float(CO[comp_verts[b["sole"]], 2].min())
    say("side", side, "sole rings", len(rings[True]), len(rings[False]), "heel front s %.3f" % b["s_heelfront"])

# ---- 1. THE UVS ----------------------------------------------------------------------------------------------------
# each face's island class: (side, kind); kinds and their scale against the shared texel density
# (the sole's top is one face of rim-to-rim slivers, so its visible welt cannot be drawn larger than the part under the
# upper: it is drawn at 0.7, the welt's stitch still about 1 px a millimetre)
KIND_SCALE = {"vamp": 1.0, "quarters": 1.0, "bottom": 0.15, "inner": 0.25, "inner_bottom": 0.10,
              "sole_top": 0.70, "sole_side_lat": 1.0, "sole_side_med": 1.0, "tread": 0.40, "eyelet": 1.0, "lace": 1.0}
KIND_CODE = {k: i for i, k in enumerate(KIND_SCALE)}
nf = len(me.polygons)
kind = np.empty(nf, dtype=object)
fside = np.zeros(nf, dtype=int)
for ci, c in enumerate(comps):
    side = comp_side[ci]
    b = BOOT[side]
    fside[c] = side
    if comp_mat[ci] == SLOT["M_Eyelet"]:
        kind[c] = "eyelet"
        continue
    if comp_mat[ci] == SLOT["M_Lace"]:
        kind[c] = "lace"
        continue
    if comp_mat[ci] == SLOT["M_Sole"]:
        for fi in c:
            n_ = FACE_N[fi]
            if n_[2] > 0.6:
                kind[fi] = "sole_top"
            elif n_[2] < -0.6:
                kind[fi] = "tread"
            else:
                kind[fi] = "sole_side_lat" if erel(FACE_C[fi], b) >= 0 else "sole_side_med"
        continue
    # the upper
    oset = set(b["outer"].tolist())
    iset = set(b["inner"].tolist())
    T_ = b["throat"]
    for fi in c:
        vs = me.polygons[fi].vertices
        cc = FACE_C[fi]
        if all(v in oset for v in vs):
            part = "outer"
        elif all(v in iset for v in vs):
            part = "inner"
        else:
            kind[fi] = "quarters"                         # the collar's cut edge goes with the quarters it tops
            continue
        n_ = FACE_N[fi]
        bottom = h_of(cc, b) < 0.004 and (n_[2] < -0.3 if part == "outer" else n_[2] > 0.3)
        if part == "inner":
            kind[fi] = "inner_bottom" if bottom else "inner"
            continue
        if bottom:
            kind[fi] = "bottom"
            continue
        sg = 1 if elace(cc, b) >= 0 else -1
        _c, n_q = b["curves"]["quarter_" + ("lat" if sg > 0 else "med")]
        kind[fi] = "vamp" if (cc - T_) @ n_q > 0 else "quarters"
say("faces by kind", {k: int((kind == k).sum()) for k in KIND_SCALE})

def islands_of(bm_, uvk):
    isl = np.full(len(bm_.faces), -1)
    n = 0
    for f in bm_.faces:
        if isl[f.index] >= 0:
            continue
        stack = [f]
        isl[f.index] = n
        while stack:
            g = stack.pop()
            for lp in g.loops:
                e = lp.edge
                if e.seam:
                    continue
                for h in e.link_faces:
                    if isl[h.index] >= 0:
                        continue
                    # joined only if the shared edge's two ends have the same UVs on both faces
                    ok = True
                    for v in e.verts:
                        u1 = next(l_[uvk].uv for l_ in g.loops if l_.vert == v)
                        u2 = next(l_[uvk].uv for l_ in h.loops if l_.vert == v)
                        if (u1 - u2).length > 1e-6:
                            ok = False
                    if ok:
                        isl[h.index] = n
                        stack.append(h)
        n += 1
    return isl, n


if KEEP_UVS:
    for e in bm.edges:
        e.seam = False
    bm.faces.ensure_lookup_table()
    ISL, NISL = islands_of(bm, bm.loops.layers.uv["UVMap"])
    # the hidden kinds from their islands' density (drawn at 0.10 to 0.25 of the rest by this tool)
    uvk_ = bm.loops.layers.uv["UVMap"]
    dens_f = np.zeros(nf)
    for f in bm.faces:
        uvs = [l_[uvk_].uv for l_ in f.loops]
        a2_ = 0.0
        for j in range(1, len(uvs) - 1):
            a2_ += abs((uvs[j] - uvs[0]).cross(uvs[j + 1] - uvs[0])) / 2
        dens_f[f.index] = math.sqrt(a2_ * TEX * TEX / max(f.calc_area() * 1e6, 1e-12))
    ref = float(np.median(dens_f[np.isin(kind, ["vamp", "quarters"])]))
    isl_d = {k: float(np.median(dens_f[ISL == k])) / ref for k in range(NISL)}
    changed = 0
    for fi in range(nf):
        k0 = kind[fi]
        rd = isl_d[ISL[fi]]
        if k0 in ("vamp", "quarters", "bottom"):
            k1 = "bottom" if rd < 0.4 else (k0 if k0 != "bottom" else "quarters")
        elif k0 in ("inner", "inner_bottom"):
            k1 = "inner_bottom" if rd < 0.17 else "inner"
        else:
            k1 = k0
        changed += k1 != k0
        kind[fi] = k1
    LOG["keepUvs"] = {"islands": int(NISL), "kindsSetByTheirIslands": int(changed)}
    UV = np.zeros((len(me.loops), 2))
    me.uv_layers["UVMap"].data.foreach_get("uv", UV.ravel())
    say("UVs kept:", LOG["keepUvs"], "faces by kind", {k: int((kind == k).sum()) for k in KIND_SCALE})
else:
    # seams: between faces of different (side, kind); the quarters also up the instep's middle in front of the heel
    bm.edges.ensure_lookup_table()
    n_seam = 0
    for e in bm.edges:
        lf = e.link_faces
        if len(lf) != 2:
            e.seam = True
            continue
        a, c = lf[0].index, lf[1].index
        seam = (kind[a], fside[a]) != (kind[c], fside[c])
        if not seam and kind[a] == "quarters":
            # the quarters open up the instep's middle (between the facings) and down the heel's back (the back stay's middle)
            b = BOOT[fside[a]]
            if np.sign(emid(FACE_C[a], b)) != np.sign(emid(FACE_C[c], b)):
                seam = True
        if not seam and kind[a] in ("inner", "inner_bottom"):
            # the inner shell cut as the outer is: up its back and front middles, so it lies flat
            b = BOOT[fside[a]]
            if np.sign(emid(FACE_C[a], b)) != np.sign(emid(FACE_C[c], b)):
                seam = True
        e.seam = seam
        n_seam += seam
    bm.to_mesh(me)
    LOG["seamEdges"] = n_seam
    say("seams", n_seam)


    def select_faces(pred):
        bpy.ops.object.mode_set(mode="OBJECT")
        for p in me.polygons:
            p.select = bool(pred(p.index))
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type="FACE")


    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    pair.select_set(True)
    bpy.context.view_layer.objects.active = pair
    me.uv_layers.active = me.uv_layers["UVMap"]
    select_faces(lambda i: kind[i] not in ("eyelet", "lace"))
    bpy.ops.uv.unwrap(method="ANGLE_BASED", fill_holes=True, correct_aspect=True, margin=0.0)
    select_faces(lambda i: kind[i] in ("eyelet", "lace"))
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.0, area_weight=0.0, correct_aspect=True,
                             scale_to_bounds=False)
    select_faces(lambda i: True)
    bpy.ops.uv.select_all(action="SELECT")
    bpy.ops.uv.average_islands_scale()
    bpy.ops.object.mode_set(mode="OBJECT")

    # the islands (faces joined across non-seam edges with shared UVs), each scaled by its kind about its own middle
    uvl = me.uv_layers["UVMap"].data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.faces.ensure_lookup_table()
    uvk = bm.loops.layers.uv["UVMap"]


    ISL, NISL = islands_of(bm, uvk)
    say("islands", NISL)
    for k in range(NISL):
        fs = np.where(ISL == k)[0]
        kinds_ = set(kind[fs])
        sc = min(KIND_SCALE[x] for x in kinds_)
        if abs(sc - 1.0) < 1e-6:
            continue
        pts = [l_[uvk].uv.copy() for fi in fs for l_ in bm.faces[int(fi)].loops]
        cu = sum(pts, Vector((0, 0))) / len(pts)
        for fi in fs:
            for l_ in bm.faces[int(fi)].loops:
                l_[uvk].uv = cu + (l_[uvk].uv - cu) * sc
    bm.to_mesh(me)
    bm.free()
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.select_all(action="SELECT")
    bpy.ops.uv.pack_islands(udim_source="CLOSEST_UDIM", rotate=True, rotate_method="ANY", scale=True, merge_overlap=False,
                            margin_method="FRACTION", margin=0.5 * PAD / TEX, pin=False, shape_method="CONCAVE")
    bpy.ops.object.mode_set(mode="OBJECT")
    UV = np.zeros((len(me.loops), 2))
    uvl = me.uv_layers["UVMap"].data
    uvl.foreach_get("uv", UV.ravel())
    # held PAD pixels off the square's edges too (the packer leaves half its margin there; textures wrap in the game)
    lo_, hi_ = UV.min(axis=0), UV.max(axis=0)
    fit = (1.0 - 2.0 * PAD / TEX) / float((hi_ - lo_).max())
    UV = (UV - lo_) * min(1.0, fit) + PAD / TEX
    uvl.foreach_set("uv", UV.ravel())
    me.update()
    LOG["uvBounds"] = [UV.min(axis=0).round(4).tolist(), UV.max(axis=0).round(4).tolist()]
    say("uv bounds", LOG["uvBounds"])

# ---- the game's own triangles: n-gons triangulated as the import will, tangents by MikkTSpace (Blender's and Unreal's) -
FORIG = np.arange(len(me.polygons))
for nm_, vals in (("fkind", [KIND_CODE[kind[i]] for i in range(nf)]), ("fside", fside.tolist()), ("fcomp", comp_of.tolist()),
                  ("forig", FORIG.tolist())):
    at = me.attributes.get(nm_) or me.attributes.new(nm_, "INT", "FACE")
    at.data.foreach_set("value", np.array(vals, dtype=np.int32))
for m_ in pair.modifiers:
    m_.show_viewport = False
    m_.show_render = False
tri_mod = pair.modifiers.new("ngons", "TRIANGULATE")
tri_mod.min_vertices = 5
dg = bpy.context.evaluated_depsgraph_get()
ev = pair.evaluated_get(dg)
em = ev.to_mesh()
em.calc_tangents(uvmap="UVMap")
R3 = np.array(MW.to_3x3())
nl = len(em.loops)
LV = np.zeros(nl, dtype=np.int64)
em.loops.foreach_get("vertex_index", LV)
VCO = np.zeros(len(em.vertices) * 3)
em.vertices.foreach_get("co", VCO)
VCO = VCO.reshape(-1, 3) @ np.array(MW.to_3x3()).T + np.array(MW.translation)
LP = VCO[LV]
LN = np.zeros(nl * 3)
em.corner_normals.foreach_get("vector", LN)
LN = LN.reshape(-1, 3) @ R3.T
LT = np.zeros(nl * 3)
em.loops.foreach_get("tangent", LT)
LT = LT.reshape(-1, 3) @ R3.T
LS = np.zeros(nl)
em.loops.foreach_get("bitangent_sign", LS)
LUV = np.zeros(nl * 2)
em.uv_layers["UVMap"].data.foreach_get("uv", LUV)
LUV = LUV.reshape(-1, 2)
em.calc_loop_triangles()
nt_ = len(em.loop_triangles)
TL = np.zeros(nt_ * 3, dtype=np.int64)
em.loop_triangles.foreach_get("loops", TL)
TL = TL.reshape(-1, 3)
TP = np.zeros(nt_, dtype=np.int64)
em.loop_triangles.foreach_get("polygon_index", TP)


def face_attr(name):
    a = np.zeros(len(em.polygons), dtype=np.int64)
    em.attributes[name].data.foreach_get("value", a)
    return a


EKIND, ESIDE, ECOMP, EORIG = face_attr("fkind"), face_attr("fside"), face_attr("fcomp"), face_attr("forig")
EPOLY_LOOPS = [(p.loop_start, p.loop_total) for p in em.polygons]
EDGE_KEYS = [tuple(sorted(e.vertices)) for e in em.edges]
ev.to_mesh_clear()
pair.modifiers.remove(tri_mod)
for m_ in pair.modifiers:
    m_.show_viewport = True
    m_.show_render = True
KIND_OF = {v: k for k, v in KIND_CODE.items()}
tk = np.array([KIND_OF[c] for c in EKIND[TP]], dtype=object)
P3, U2 = LP[TL], LUV[TL]
say("game triangles", nt_, "loops", nl)

# ---- the layout rasterised: each texel's triangle and its barycentrics, at texel centres --------------------------
TRI_ID = np.full((TEX, TEX), -1, dtype=np.int64)
BARY = np.zeros((TEX, TEX, 3), dtype=np.float64)
ISL_PIX = np.full((TEX, TEX), -1, dtype=np.int64)
OVER = np.zeros((TEX, TEX), dtype=bool)
ISL_OF_TRI = ISL[EORIG[TP]]
for ti in range(nt_):
    xs, ys = U2[ti, :, 0] * TEX - 0.5, U2[ti, :, 1] * TEX - 0.5
    x0, x1 = max(0, int(math.floor(xs.min()))), min(TEX - 1, int(math.ceil(xs.max())))
    y0, y1 = max(0, int(math.floor(ys.min()))), min(TEX - 1, int(math.ceil(ys.max())))
    if x1 < x0 or y1 < y0:
        continue
    gx, gy = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
    d = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
    if abs(d) < 1e-14:
        continue
    l1 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / d
    l2 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / d
    l3 = 1 - l1 - l2
    ins = (l1 >= -1e-9) & (l2 >= -1e-9) & (l3 >= -1e-9)
    if not ins.any():
        continue
    yy, xx = gy[ins], gx[ins]
    fresh = TRI_ID[yy, xx] < 0
    OVER[yy[~fresh], xx[~fresh]] |= ISL_PIX[yy[~fresh], xx[~fresh]] != ISL_OF_TRI[ti]
    TRI_ID[yy[fresh], xx[fresh]] = ti
    BARY[yy[fresh], xx[fresh]] = np.column_stack([l1[ins][fresh], l2[ins][fresh], l3[ins][fresh]])
    ISL_PIX[yy[fresh], xx[fresh]] = ISL_OF_TRI[ti]
INSIDE = TRI_ID >= 0
# THE ISLANDS' BORDER TEXELS (centres up to 1.5 px outside every triangle) drawn from the nearest triangle's own plane,
# its barycentrics carried past its edge, as a baker's conservative raster does: so the texels a seam's two sides
# sample are the surface's own values, not a neighbour's copied out (the first seam check: 2x the ordinary edges')
EXT_ID = TRI_ID.copy()
EXT_B = BARY.copy()
best = np.where(INSIDE, 0.0, -1e9)
for ti in range(nt_):
    xs, ys = U2[ti, :, 0] * TEX - 0.5, U2[ti, :, 1] * TEX - 0.5
    x0, x1 = max(0, int(math.floor(xs.min())) - 2), min(TEX - 1, int(math.ceil(xs.max())) + 2)
    y0, y1 = max(0, int(math.floor(ys.min())) - 2), min(TEX - 1, int(math.ceil(ys.max())) + 2)
    d = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
    if abs(d) < 1e-14 or x1 < x0 or y1 < y0:
        continue
    gx, gy = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
    l1 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / d
    l2 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / d
    l3 = 1 - l1 - l2
    g1 = math.hypot((ys[1] - ys[2]) / d, (xs[2] - xs[1]) / d)
    g2 = math.hypot((ys[2] - ys[0]) / d, (xs[0] - xs[2]) / d)
    g3 = math.hypot((ys[0] - ys[1]) / d, (xs[1] - xs[0]) / d)
    md = np.minimum(np.minimum(l1 / max(g1, 1e-12), l2 / max(g2, 1e-12)), l3 / max(g3, 1e-12))
    sub = best[y0:y1 + 1, x0:x1 + 1]
    take = (md >= -1.5) & (md < 0) & (md > sub) & (TRI_ID[y0:y1 + 1, x0:x1 + 1] < 0)
    if not take.any():
        continue
    yy, xx = gy[take], gx[take]
    EXT_ID[yy, xx] = ti
    EXT_B[yy, xx] = np.column_stack([l1[take], l2[take], l3[take]])
    best[yy, xx] = md[take]
DRAWN = EXT_ID >= 0

# ---- the UV checks: texel density per kind, its spread, overlap, the gap between islands, the share used ------------
a3 = 0.5 * np.linalg.norm(np.cross(P3[:, 1] - P3[:, 0], P3[:, 2] - P3[:, 0]), axis=1)
a2 = 0.5 * np.abs((U2[:, 1, 0] - U2[:, 0, 0]) * (U2[:, 2, 1] - U2[:, 0, 1]) - (U2[:, 2, 0] - U2[:, 0, 0]) * (U2[:, 1, 1] - U2[:, 0, 1]))
dens = np.sqrt(a2 * TEX * TEX / np.maximum(a3 * 1e6, 1e-12))      # pixels per millimetre
LOG["checks"]["pxPerMm"] = {}
LOG["checks"]["densityRatio1to99"] = {}
for k in KIND_SCALE:
    sel = (tk == k) & (a3 > 1e-12)
    if sel.any():
        w = a3[sel]
        mean_ = float(np.average(dens[sel], weights=w))
        LOG["checks"]["pxPerMm"][k] = round(mean_, 3)
        r = dens[sel] / mean_
        LOG["checks"]["densityRatio1to99"][k] = [round(float(np.percentile(r, 1)), 3), round(float(np.percentile(r, 99)), 3)]
say("px/mm", LOG["checks"]["pxPerMm"])
say("density against its kind's mean, 1st-99th percentile", LOG["checks"]["densityRatio1to99"])
LOG["checks"]["layoutShare"] = round(float(INSIDE.mean()), 4)
LOG["checks"]["overlapTexels"] = int(OVER.sum())


def min_island_gap(lab, most):
    cur = lab.copy()
    for r in range(1, most + 1):
        nxt = cur.copy()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sh = np.roll(np.roll(cur, dy, 0), dx, 1)
            if dy == 1:
                sh[0, :] = -1
            if dy == -1:
                sh[-1, :] = -1
            if dx == 1:
                sh[:, 0] = -1
            if dx == -1:
                sh[:, -1] = -1
            if ((cur >= 0) & (sh >= 0) & (sh != cur)).any():
                return 2 * r - 1
            take = (nxt < 0) & (sh >= 0)
            nxt[take] = sh[take]
        cur = nxt
    return 2 * most


LOG["checks"]["minIslandGapPx"] = min_island_gap(ISL_PIX, PAD + 2)
ys_, xs_ = np.where(INSIDE)
LOG["checks"]["minBorderPx"] = int(min(xs_.min(), ys_.min(), TEX - 1 - xs_.max(), TEX - 1 - ys_.max()))
LOG["checks"]["islands"] = int(NISL)
say("layout share %.3f, overlapping texels %d, gap between islands about %d px, to the border %d px" % (
    LOG["checks"]["layoutShare"], LOG["checks"]["overlapTexels"], LOG["checks"]["minIslandGapPx"], LOG["checks"]["minBorderPx"]))


def write_png(path, arr):
    """8-bit PNG (grey, RGB or RGBA), rows top first, by zlib alone (Blender's Python has no imaging library)."""
    import struct
    import zlib
    arr = np.ascontiguousarray(arr, dtype=np.uint8)
    h, w = arr.shape[:2]
    c = 1 if arr.ndim == 2 else arr.shape[2]
    ct = {1: 0, 3: 2, 4: 6}[c]
    raw = b"".join(b"\x00" + arr[y].tobytes() for y in range(h))

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, ct, 0, 0, 0))
                 + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))


KIND_RGB = {"vamp": (200, 90, 60), "quarters": (60, 120, 200), "bottom": (90, 90, 90), "inner": (120, 60, 160),
            "inner_bottom": (70, 50, 90), "sole_top": (200, 180, 60), "sole_side_lat": (60, 190, 90),
            "sole_side_med": (40, 150, 70), "tread": (100, 140, 100), "eyelet": (250, 250, 250), "lace": (160, 110, 70)}
lay = np.zeros((TEX, TEX, 3), dtype=np.uint8)
tk_pix = np.where(INSIDE, tk[np.maximum(TRI_ID, 0)], None)
for k, rgb in KIND_RGB.items():
    lay[tk_pix == k] = rgb
edge_ = INSIDE & ~(np.roll(INSIDE, 1, 0) & np.roll(INSIDE, -1, 0) & np.roll(INSIDE, 1, 1) & np.roll(INSIDE, -1, 1))
lay[edge_] = (255, 255, 255)
write_png(os.path.join(OUT, NAME + "_uv_layout.png"), lay[::-1])
SRC_UV = np.zeros((len(me.loops), 2))
me.uv_layers["UVMap"].data.foreach_get("uv", SRC_UV.ravel())
SRC_LOOPV = np.zeros(len(me.loops), dtype=np.int64)
me.loops.foreach_get("vertex_index", SRC_LOOPV)
np.savez_compressed(os.path.join(OUT, "_uv.npz"), uv=SRC_UV, loopv=SRC_LOOPV)
if STAGE == "uv":
    json.dump(LOG, open(os.path.join(OUT, NAME + "_maps.json"), "w"), indent=1, default=str)
    say("uv stage written")
    sys.exit(0)

# ---- 2. EVERY TEXEL'S PLACE ON THE SURFACE ----------------------------------------------------------------------------
iy, ix = np.where(DRAWN)
NPX = len(iy)
ti_ = EXT_ID[iy, ix]
bc = EXT_B[iy, ix]
lo3 = TL[ti_]                                          # (n, 3) loops
P = np.einsum("nk,nkj->nj", bc, LP[lo3])
Nn = np.einsum("nk,nkj->nj", bc, LN[lo3])
Nn /= np.linalg.norm(Nn, axis=1)[:, None]
Tt = np.einsum("nk,nkj->nj", bc, LT[lo3])
Tt -= (Tt * Nn).sum(1)[:, None] * Nn
Tt /= np.maximum(np.linalg.norm(Tt, axis=1), 1e-12)[:, None]
SG = np.sign(LS[lo3[:, 0]])
SG[SG == 0] = 1
Bt = SG[:, None] * np.cross(Nn, Tt)
PK = np.array([KIND_OF[c] for c in EKIND[TP[ti_]]], dtype=object)
PS = ESIDE[TP[ti_]]
PC = ECOMP[TP[ti_]]
say("texels", NPX)
rng = np.random.default_rng(SEED)

# ---- noise, in 3D (so it runs across every seam) ---------------------------------------------------------------------
MASK64 = np.int64(0xFFFFFF)


def hash3(ix_, iy_, iz_, k=0):
    h = ix_ * np.int64(73856093) ^ iy_ * np.int64(19349663) ^ iz_ * np.int64(83492791) ^ np.int64(k * 2654435 + SEED * 97)
    h = (h ^ (h >> np.int64(13))) * np.int64(1274126177)
    h = h ^ (h >> np.int64(16))
    return (h & MASK64).astype(np.float64) / float(0xFFFFFF)


def vnoise(X, scale, k=0):
    Y = X / scale
    i0 = np.floor(Y).astype(np.int64)
    f = Y - i0
    u = f * f * (3 - 2 * f)
    acc = np.zeros(len(X))
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (u[:, 0] if dx else 1 - u[:, 0]) * (u[:, 1] if dy else 1 - u[:, 1]) * (u[:, 2] if dz else 1 - u[:, 2])
                acc += w * hash3(i0[:, 0] + dx, i0[:, 1] + dy, i0[:, 2] + dz, k)
    return acc


def fbm(X, scale, octaves=3, k=0):
    acc, norm, a = np.zeros(len(X)), 0.0, 1.0
    for o in range(octaves):
        acc += a * vnoise(X, scale / (2 ** o), k + 17 * o)
        norm += a
        a *= 0.5
    return acc / norm


def worley(X, cell, k=0):
    Y = X / cell
    i0 = np.floor(Y).astype(np.int64)
    F1 = np.full(len(X), 9.0)
    F2 = np.full(len(X), 9.0)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                c0, c1, c2 = i0[:, 0] + dx, i0[:, 1] + dy, i0[:, 2] + dz
                fx = c0 + hash3(c0, c1, c2, k)
                fy = c1 + hash3(c0, c1, c2, k + 1)
                fz = c2 + hash3(c0, c1, c2, k + 2)
                d = np.sqrt((Y[:, 0] - fx) ** 2 + (Y[:, 1] - fy) ** 2 + (Y[:, 2] - fz) ** 2)
                F2 = np.where(d < F1, F1, np.minimum(F2, d))
                F1 = np.minimum(F1, d)
    return F1 * cell, F2 * cell


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def G(u):
    return np.exp(-u * u)


def chunked(fn, X, *rest, size=120000):
    outs = None
    for a in range(0, len(X), size):
        r = fn(X[a:a + size], *[q[a:a + size] if isinstance(q, np.ndarray) and len(q) == len(X) else q for q in rest])
        r = r if isinstance(r, tuple) else (r,)
        if outs is None:
            outs = [[] for _ in r]
        for o, x in zip(outs, r):
            o.append(x)
    outs = [np.concatenate(o) for o in outs]
    return outs if len(outs) > 1 else outs[0]


def curve_coords(X, C, Nref, closed=False):
    """Each point's nearest place on the polyline C: distance (m), arc length there (m), the line's direction there, and
    the side (+1 / -1) by the surface's normal crossed with the line's direction."""
    A, B_ = C[:-1], C[1:]
    AB = B_ - A
    L2 = np.maximum((AB * AB).sum(1), 1e-18)
    seg = np.sqrt(L2)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    dist = np.empty(len(X))
    tt = np.empty(len(X))
    tau = np.empty((len(X), 3))
    side = np.empty(len(X))
    for a in range(0, len(X), 2048):
        x = X[a:a + 2048]
        rel = x[:, None, :] - A[None, :, :]
        t = np.clip((rel * AB[None]).sum(2) / L2[None], 0.0, 1.0)
        q = A[None] + t[..., None] * AB[None]
        d2 = ((x[:, None, :] - q) ** 2).sum(2)
        j = d2.argmin(1)
        r_ = np.arange(len(x))
        qq = q[r_, j]
        dist[a:a + 2048] = np.sqrt(d2[r_, j])
        tt[a:a + 2048] = cum[j] + t[r_, j] * seg[j]
        tu = AB[j] / seg[j][:, None]
        tau[a:a + 2048] = tu
        side[a:a + 2048] = np.sign(((x - qq) * np.cross(Nref[a:a + 2048], tu)).sum(1))
    side[side == 0] = 1
    return dist, tt, tau, side, float(cum[-1])


def stitch_row(d, t, d0, pitch=3.6, frac=0.72, width=0.42, hgt=0.16, phase=0.0):
    """One row of stitches along a line (millimetres): the thread proud, the holes and the channel pressed in."""
    dd = d - d0
    across = G(dd / width)
    u = np.mod(t / pitch + phase, 1.0)
    on = u < frac
    along = np.where(on, np.sqrt(np.clip(np.sin(np.pi * np.clip(u / frac, 0, 1)), 0, 1)), -0.8)
    h = hgt * across * along - 0.045 * G(dd / 0.8)
    thread = across * on * np.sqrt(np.clip(np.sin(np.pi * np.clip(u / frac, 0, 1)), 0, 1))
    return h, thread


def overlap_edge(d, hgt=0.42, w1=0.9, w2=4.0):
    """The edge of a piece lying over another (d > 0 on the upper piece, millimetres): its cut edge rounding down
    steeply, the piece under it rising gently back."""
    return np.where(d >= 0, -hgt * (1 - smoothstep(0, w1, d)), -hgt * (1 - smoothstep(0, w2, -d)))


# ---- 3. THE FEATURES, AS HEIGHTS IN MILLIMETRES (at the texel and half a texel either way along its tangent frame) --
EPS = 0.5 / max(1e-6, LOG["checks"]["pxPerMm"]["vamp"]) * 1e-3     # half a texel, in metres
OFFS = [np.zeros(3)]
SHIFT = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
H5 = np.zeros((5, NPX))
THREAD = np.zeros(NPX)
EDGEHI = np.zeros(NPX)
SHADOW = np.zeros(NPX)
CREASE = np.zeros(NPX)
GROOVE = np.zeros(NPX)


def shifted(sel, k):
    a, b_ = SHIFT[k]
    return P[sel] + EPS * (a * Tt[sel] + b_ * Bt[sel])


LEATHER = np.isin(PK, ["vamp", "quarters"])
SOLE = np.isin(PK, ["sole_top", "sole_side_lat", "sole_side_med", "tread"])
for side, b in BOOT.items():
    upi = np.where(LEATHER & (PS == side))[0]
    # (a) the grain: pebbles about 1.7 mm across (cellular noise), their borders grooves; a slow unevenness over it
    for k in range(5):
        X = shifted(upi, k)
        F1, F2 = chunked(lambda x: worley(x, 0.0017, 11), X)
        groove = 1 - smoothstep(0.0, 0.00045, F2 - F1)
        H5[k, upi] += -0.09 * groove - 0.05 * (F1 / 0.0017) ** 2 + 0.05 * (chunked(lambda x: fbm(x, 0.007, 2, 31), X) - 0.5)
        if k == 0:
            GROOVE[upi] = groove
        # (b) the vamp's creases across the ball line, wavy, broken, fading down the sides; the welt's pinch low down
        s = s_of(X, b)
        x = emid(X, b)
        h = h_of(X, b)
        fade = smoothstep(0.012, 0.03, h) * (1 - smoothstep(0.032, 0.056, np.abs(x)))
        prm = b.setdefault("creases", None)
        if prm is None:
            r_ = np.random.default_rng(SEED + 7 * side)
            prm = [(dk, dep, sig, r_.uniform(0.0008, 0.0016), r_.uniform(0.022, 0.045), r_.uniform(0, 6.3))
                   for dk, dep, sig in ((-0.006, 0.30, 1.1), (0.0, 0.45, 1.4), (0.006, 0.38, 1.2), (0.013, 0.30, 1.1),
                                        (0.020, 0.18, 0.9))]
            prm += [(r_.uniform(-0.012, 0.03), r_.uniform(0.08, 0.15), r_.uniform(0.6, 0.8), r_.uniform(0.0005, 0.0012),
                     r_.uniform(0.015, 0.03), r_.uniform(0, 6.3)) for _ in range(6)]
            b["creases"] = prm
        cm = np.zeros(len(upi))
        for j, (dk, dep, sig, amp, lam, ph) in enumerate(prm):
            sc = b["s_ball"] + dk - 0.22 * x - 1.2 * x * x + amp * np.sin(2 * np.pi * x / lam + ph)
            u = (s - sc) * 1000.0 / sig
            brk = 0.35 + 0.65 * chunked(lambda q: vnoise(q, 0.009, 50 + j), X)
            H5[k, upi] += dep * fade * brk * (-G(u) + 0.35 * (G(u - 1.7) + G(u + 1.7)))
            cm += G(u) * fade * brk * min(1.0, dep / 0.3)
        H5[k, upi] += -0.12 * G((h - 0.0025) / 0.0008)
        if k == 0:
            CREASE[upi] = np.clip(cm, 0, 1)
    # (c) the construction: each line a piece's edge lying over the next, with its stitch rows on the upper piece
    for cname, (C, _n) in b["curves"].items():
        closed = cname == "collar"
        lo_b, hi_b = C.min(axis=0) - 0.009, C.max(axis=0) + 0.009
        cand = upi[np.all((P[upi] >= lo_b) & (P[upi] <= hi_b), axis=1)]
        if not len(cand):
            continue
        # which side is the upper piece: towards the heel for a quarter, towards the eyelets for a facing, towards the
        # back's middle for the back stay, below the edge for the collar
        mid = C[len(C) // 2]
        nm_ = np.array(b["bvh"].find_nearest(Vector(mid))[1])
        if cname.startswith("quarter"):
            ref = -b["D"]
        elif cname.startswith("facing"):
            row = b["eyes_lat"] if cname.endswith("lat") else b["eyes_med"]
            ref = row.mean(axis=0) - mid
        elif cname.startswith("backstay"):
            ref = -b["E"] * (1 if cname.endswith("lat") else -1)
        else:
            ref = -Z
        _d, _t, tau_m, _s, _L = curve_coords(mid[None] + 0.002 * ref[None] / np.linalg.norm(ref), C, nm_[None])
        csign = _s[0]
        for k in range(5):
            X = shifted(cand, k)
            dist, tt, tau, sd, Lc = curve_coords(X, C, Nn[cand])
            d = dist * 1000.0 * sd * csign
            t = tt * 1000.0
            Lmm = Lc * 1000.0
            fe = np.ones(len(cand)) if closed else smoothstep(0, 3, t) * smoothstep(0, 3, Lmm - t)
            if cname == "collar":
                dd = np.abs(d)
                hh = -0.35 * (1 - smoothstep(0, 1.6, dd)) + 0.22 * G((dd - 8.0) / 3.5)
                hs, th = stitch_row(dd, t, 5.5)
                hh = hh + hs
            else:
                hh = overlap_edge(d)
                rows = (2.0, 4.0) if cname.startswith("quarter") else (2.2,) if cname.startswith("facing") else (2.0,)
                th = np.zeros(len(cand))
                for ri, d0 in enumerate(rows):
                    hs, t_ = stitch_row(d, t, d0, phase=0.5 * ri)
                    hh = hh + hs
                    th = np.maximum(th, t_)
            H5[k, cand] += hh * fe
            if k == 0:
                THREAD[cand] = np.maximum(THREAD[cand], th * fe)
                if cname != "collar":
                    EDGEHI[cand] = np.maximum(EDGEHI[cand], (d >= 0) * (1 - smoothstep(0.3, 1.0, d)) * fe)
                    SHADOW[cand] = np.maximum(SHADOW[cand], (d < 0) * (1 - smoothstep(0.0, 3.0, -d)) * fe)
    say("side", side, "upper features drawn")

# ---- the sole: its edge a band (rounded top and bottom, the welt's line, the heel's breast and lift), the welt's
# stitch round its top, a tread under it
SOLE_D = {}
for side, b in BOOT.items():
    si = np.where(SOLE & (PS == side))[0]
    rt = np.vstack([b["ring_top"], b["ring_top"][:1]])
    rb = np.vstack([b["ring_bot"], b["ring_bot"][:1]])
    rt2 = rt.copy()
    rt2[:, 2] = 0.0
    rb2 = rb.copy()
    rb2[:, 2] = 0.0
    for k in range(5):
        X = shifted(si, k)
        kk = PK[si]
        s = s_of(X, b)
        e_ = e_of(X, b)
        hh = np.zeros(len(si))
        on_side = np.char.startswith(kk.astype(str), "sole_side")
        on_top = kk == "sole_top"
        on_tr = kk == "tread"
        d_top, _t1, _a, _b, _l = curve_coords(X, rt, Nn[si])
        d_bot, _t2, _a, _b, _l = curve_coords(X, rb, Nn[si])
        X2 = X.copy()
        X2[:, 2] = 0.0
        dr, tr, _a, _b, Lr = curve_coords(X2, rt2, np.tile(Z, (len(si), 1)))
        drb, _t3, _a, _b, _l = curve_coords(X2, rb2, np.tile(Z, (len(si), 1)))
        dt_, db_, dr_, tr_, drb_ = d_top * 1000, d_bot * 1000, dr * 1000, tr * 1000, drb * 1000
        r_ = 0.9                                      # (1.6 at first: read in the game as a soft, thick welt)
        # the edge band
        hs = -0.5 * r_ * np.clip(1 - dt_ / r_, 0, 1) ** 2 - 0.5 * r_ * np.clip(1 - db_ / r_, 0, 1) ** 2
        hs += -0.35 * G((dt_ - 6.0) / 0.5)
        hf = b["s_heelfront"] * 1000
        hs += -0.25 * G((s * 1000 - hf) / 0.5) * smoothstep(6.0, 7.0, dt_) * (s * 1000 < hf + 3)
        hs += -0.18 * G((db_ - 8.0) / 0.4) * smoothstep(hf + 1, hf - 1, s * 1000)
        hs += 0.02 * (chunked(lambda q: fbm(q, 0.0015, 2, 71), X) - 0.5)
        # the welt's top: rounded at its edge, the stitch round it 2.8 mm in, its channel
        ht = -0.5 * r_ * np.clip(1 - dr_ / r_, 0, 1) ** 2
        st_h, st_t = stitch_row(dr_, tr_, WSTITCH, pitch=4.2, frac=0.7, width=0.45, hgt=0.18)
        ht += st_h - 0.06 * G((dr_ - WSTITCH) / 1.0)
        # the tread: blocks under the forepart, bars under the heel, the waist plain, a plain border
        sm = s * 1000
        row = np.floor(sm / 11.0)
        fs_ = np.mod(sm / 11.0, 1.0)
        fe_ = np.mod(e_ * 1000 / 8.0 + 0.5 * (row % 2), 1.0)
        gfore = 1 - smoothstep(0.0, 1.2, np.minimum(np.minimum(fs_, 1 - fs_) * 11.0, np.minimum(fe_, 1 - fe_) * 8.0))
        fh = np.mod(sm / 7.0, 1.0)
        gheel = 1 - smoothstep(0.0, 1.0, np.minimum(fh, 1 - fh) * 7.0)
        fore = smoothstep(b["s_ball"] * 1000 - 40, b["s_ball"] * 1000 - 30, sm)
        heel = 1 - smoothstep(hf - 4, hf - 2, sm)
        grv = (gfore * fore + gheel * heel) * smoothstep(4.0, 6.0, drb_)
        htr = -0.7 * grv + 0.03 * (chunked(lambda q: fbm(q, 0.002, 2, 81), X) - 0.5)
        H5[k, si] += np.where(on_side, hs, np.where(on_top, ht, np.where(on_tr, htr, 0.0)))
        if k == 0:
            SOLE_D[side] = dict(si=si, dt=dt_, db=db_, dr=dr_, grv=grv, thread=st_t * on_top, side=on_side, top=on_top, tr=on_tr, s=s)
    say("side", side, "sole features drawn")

# ---- the laces braided (diagonal ridges along each lace) ------------------------------------------------------------
LACE = PK == "lace"
lace_frames = {}
for ci in np.unique(PC[LACE]):
    pts = CO[comp_verts[ci]]
    c0 = pts.mean(axis=0)
    _u, _s, vt = np.linalg.svd(pts - c0)
    lace_frames[ci] = (c0, vt)
li = np.where(LACE)[0]
for k in range(5):
    X = shifted(li, k)
    a_ = np.zeros(len(li))
    q_ = np.zeros(len(li))
    for ci, (c0, vt) in lace_frames.items():
        sel = PC[li] == ci
        rel = X[sel] - c0
        a_[sel] = rel @ vt[0]
        q_[sel] = rel @ vt[1] + rel @ vt[2]
    H5[k, li] += 0.10 * np.cos(2 * np.pi * (a_ * 1000 / 1.4 + q_ * 1000 / 1.8)) + 0.03 * np.cos(2 * np.pi * (a_ * 1000 / 1.4 - q_ * 1000 / 1.8))

# ---- the normals: each texel's height gradient in its own tangent frame (OpenGL's green: +V) --------------------------
dHdT = (H5[1] - H5[2]) / (2 * EPS * 1000.0)
dHdB = (H5[3] - H5[4]) / (2 * EPS * 1000.0)
NTS = np.column_stack([-dHdT, -dHdB, np.ones(NPX)])
NTS /= np.linalg.norm(NTS, axis=1)[:, None]

# ---- 4. COLOUR (the factor the material multiplies by Tint or TapeColour), ROUGHNESS, ID, METAL -----------------------
ML = np.zeros((NPX, 3))
RO = np.zeros(NPX)
IDv = np.zeros(NPX)
ME_ = np.zeros(NPX)
ID_OF = {"sole_top": 0.5, "sole_side_lat": 0.5, "sole_side_med": 0.5, "tread": 0.5, "eyelet": 0.75}
for k_, v_ in ID_OF.items():
    IDv[PK == k_] = v_
# the leather: black, pebbled, polished on the vamp, creases and edges a little worn, the toe and heel scuffed
SCUFF = np.zeros(NPX)
SCRATCH = np.zeros(NPX)
DUST = np.zeros(NPX)
for side, b in BOOT.items():
    upi = np.where(LEATHER & (PS == side))[0]
    X = P[upi]
    s, h, x = s_of(X, b), h_of(X, b), emid(X, b)
    L = b["L"]
    n1 = fbm(X, 0.004, 4, 101 + side)
    w_toe = smoothstep(L - 0.045, L - 0.010, s) * (1 - smoothstep(0.028, 0.048, h))
    w_heel = (1 - smoothstep(0.010, 0.034, s)) * (1 - smoothstep(0.030, 0.055, h))
    w_kick = (1 - smoothstep(0.004, 0.018, h)) * smoothstep(0.5, 0.75, fbm(X, 0.02, 2, 131 + side))
    SCUFF[upi] = np.clip(((w_toe + 0.8 * w_heel) * (0.3 + 1.3 * n1) - 0.5) * 2.0, 0, 1) + 0.5 * w_kick * n1
    SCUFF[upi] = np.clip(SCUFF[upi], 0, 1)
    DUST[upi] = (1 - smoothstep(0.003, 0.014, h)) * (0.55 + 0.45 * fbm(X, 0.004, 2, 141 + side))
    # scratches: short lines on the toe and the heel, mostly along the foot
    r_ = np.random.default_rng(SEED + 1000 + side)
    for _ in range(46):
        toe = r_.random() < 0.6
        ss = (L - r_.uniform(0.004, 0.040)) if toe else r_.uniform(0.0, 0.03)
        hh_ = r_.uniform(0.004, 0.035 if toe else 0.045)
        sgn = 1 if r_.random() < 0.5 else -1
        th_ = math.radians(r_.uniform(0, 75))
        dirv = -(b["E"] * sgn) * math.cos(th_) + (b["D"] if toe else -b["D"]) * (-math.sin(th_))
        tgt = b["D"] * (ss + b["s0"]) + b["E"] * float(ecentre(ss, b))
        tgt[2] = float(zfloor(ss, b)) + hh_
        org = tgt - dirv * 0.2
        hit, hn, _i, _dd = b["bvh"].ray_cast(Vector(org), Vector(dirv), 0.4)
        if hit is None:
            continue
        p0, nn = np.array(hit), np.array(hn)
        v = b["D"] + np.array([0, 0, r_.uniform(-0.5, 0.5)])
        v = v - (v @ nn) * nn
        v /= np.linalg.norm(v)
        ln_ = r_.uniform(0.004, 0.014)
        line = snap([p0 + v * ln_ * (j / 4.0 - 0.5) for j in range(5)], b)
        wd = r_.uniform(0.25, 0.55)
        it = r_.uniform(0.45, 1.0)
        lo_b, hi_b = line.min(axis=0) - 0.002, line.max(axis=0) + 0.002
        cand = np.where(np.all((X >= lo_b) & (X <= hi_b), axis=1))[0]
        if len(cand):
            dd_, _t, _a, _b, _l = curve_coords(X[cand], line, Nn[upi][cand])
            SCRATCH[upi[cand]] = np.maximum(SCRATCH[upi[cand]], it * (1 - smoothstep(0.0, wd, dd_ * 1000)))
    mott = fbm(X, 0.015, 3, 151 + side) - 0.5
    polish = smoothstep(b["s_ball"] - 0.06, b["s_ball"] - 0.03, s) * smoothstep(0.015, 0.035, h)
    base = 0.40 - 0.06 * GROOVE[upi] + 0.08 * mott + 0.07 * CREASE[upi] + 0.05 * EDGEHI[upi]
    base *= 1 - 0.12 * SHADOW[upi]
    col = np.tile(base[:, None], (1, 3))
    col = col * (1 - THREAD[upi][:, None]) + 0.90 * THREAD[upi][:, None]
    scuff_rgb = np.array([0.90, 0.82, 0.72]) * (0.75 + 0.25 * n1)[:, None]
    a_ = (0.5 * SCUFF[upi])[:, None]
    col = col * (1 - a_) + scuff_rgb * a_
    a_ = (0.9 * SCRATCH[upi])[:, None]
    col = col * (1 - a_) + np.array([0.98, 0.92, 0.84]) * a_
    a_ = (0.35 * DUST[upi])[:, None]
    col = col * (1 - a_) + np.array([0.80, 0.76, 0.70]) * a_
    ML[upi] = col
    ro = 0.53 - 0.08 * polish + 0.02 * (PK[upi] == "quarters") - 0.02 + 0.07 * GROOVE[upi] + 0.05 * mott + 0.12 * CREASE[upi]
    ro = ro * (1 - THREAD[upi]) + 0.62 * THREAD[upi]
    ro = ro * (1 - SCUFF[upi]) + 0.78 * SCUFF[upi]
    ro = ro * (1 - SCRATCH[upi]) + 0.82 * SCRATCH[upi]
    ro = ro * (1 - 0.6 * DUST[upi]) + 0.78 * 0.6 * DUST[upi]
    RO[upi] = np.clip(ro, 0.42, 0.88)
# the lining and the parts out of sight
for k_, rgb, ro_ in (("inner", (0.55, 0.45, 0.38), 0.75), ("inner_bottom", (0.50, 0.42, 0.36), 0.8),
                     ("bottom", (0.40, 0.40, 0.40), 0.6)):
    sel = PK == k_
    ML[sel] = rgb
    RO[sel] = ro_
# the sole (times TapeColour): its edge band a touch lighter than its top and tread, the welt band between, dust on the
# welt by the upper, scuffs at the toe and heel corners, dirt in the tread
for side, b in BOOT.items():
    sd = SOLE_D[side]
    si = sd["si"]
    X = P[si]
    n2 = fbm(X, 0.006, 3, 201 + side)
    s = sd["s"]
    L = b["L"]
    # the welt band (the side's top 6 mm) and the welt's top lighter and smoother than the outsole's edge under them
    val = np.where(sd["side"], np.where(sd["dt"] < 6.0, 0.60, 0.50), np.where(sd["top"], np.where(sd["dr"] < 6.5, 0.56, 0.45), 0.42))
    val = val + 0.05 * (n2 - 0.5)
    ro = np.where(sd["side"], np.where(sd["dt"] < 6.0, 0.70, 0.82), np.where(sd["top"], 0.78, 0.86)) + 0.04 * (n2 - 0.5)
    edge_corner = sd["side"] * (smoothstep(L - 0.05, L - 0.01, s) + 1 - smoothstep(0.01, 0.045, s)) * smoothstep(0.45, 0.7, n2 + 0.2)
    edge_corner = np.clip(edge_corner * (1 - smoothstep(4.0, 12.0, sd["db"])), 0, 1)
    val = val * (1 - edge_corner) + 0.72 * edge_corner
    ro = ro * (1 - edge_corner) + 0.9 * edge_corner
    rnd = sd["top"] * (1 - smoothstep(0.4, 0.9, sd["dr"])) * 0.5
    val = val + 0.08 * rnd
    dust = sd["top"] * smoothstep(3.6, 4.6, sd["dr"]) * (0.5 + 0.5 * fbm(X, 0.003, 2, 211 + side))
    val = val * (1 - 0.4 * dust) + 0.78 * 0.4 * dust
    ro = ro * (1 - dust) + 0.9 * dust
    val = val * (1 - sd["thread"]) + 0.85 * sd["thread"]
    ro = ro * (1 - sd["thread"]) + 0.65 * sd["thread"]
    dirt = sd["tr"] * sd["grv"]
    val = val * (1 - 0.6 * dirt) + 0.68 * 0.6 * dirt
    ro = ro * (1 - dirt) + 0.92 * dirt
    ML[si] = np.tile(val[:, None], (1, 3))
    RO[si] = np.clip(ro, 0.6, 0.95)
# laces: dark brown-black (times Tint), fibre-mottled; eyelets: the flat TeethColour, metal
lx = fbm(P[li], 0.0012, 2, 301)
ML[li] = np.array([0.50, 0.34, 0.24]) * (0.88 + 0.24 * lx)[:, None]
RO[li] = 0.68 + 0.06 * (lx - 0.5)
ei = PK == "eyelet"
ML[ei] = 0.5
RO[ei] = 0.38 + 0.04 * (fbm(P[ei], 0.002, 2, 311) - 0.5)
ME_[ei] = 1.0
NTS[ei] = (0.0, 0.0, 1.0)
for k_ in ("inner", "inner_bottom", "bottom"):
    NTS[PK == k_] = (0.0, 0.0, 1.0)
LOG["checks"]["normalsOver60"] = {k: round(float((NTS[PK == k, 2] < 0.5).mean()), 5) for k in KIND_SCALE if (PK == k).any()}
say("normals over 60 degrees off", LOG["checks"]["normalsOver60"])

# ---- 5. OCCLUSION, baked by Cycles on the pair alone (no body, no ground) ---------------------------------------------
scn = bpy.context.scene
scn.render.engine = "CYCLES"
scn.cycles.device = "CPU"
scn.cycles.samples = AO_SAMPLES
scn.world = scn.world or bpy.data.worlds.new("w")
scn.world.light_settings.distance = 0.06
scn.render.bake.margin = 3
scn.render.bake.margin_type = "ADJACENT_FACES"
scn.render.bake.use_selected_to_active = False
ao_im = bpy.data.images.new(NAME + "_ao", TEX, TEX, alpha=False, float_buffer=True)
ao_im.colorspace_settings.name = "Non-Color"
for m in me.materials:
    m.use_nodes = True
    nd = m.node_tree.nodes.new("ShaderNodeTexImage")
    nd.image = ao_im
    m.node_tree.nodes.active = nd
for o in bpy.context.view_layer.objects:
    o.select_set(False)
pair.select_set(True)
bpy.context.view_layer.objects.active = pair
tb = time.time()
bpy.ops.object.bake(type="AO")
AOI = np.array(ao_im.pixels[:], dtype=np.float32).reshape(TEX, TEX, 4)[:, :, 0]
LOG["checks"]["aoBakeSeconds"] = round(time.time() - tb, 1)
AO = AOI[iy, ix].astype(np.float64)
AO[ei] = np.maximum(AO[ei], 0.8)
say("occlusion baked in %.0f s; mean %.3f over the leather" % (time.time() - tb, AO[LEATHER].mean()))


# ---- 6. THE MAPS WRITTEN: the islands' own texels, then each padding texel from its nearest island texel -------------
def srgb(x):
    x = np.clip(x, 0.0, 1.0)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)


src = np.full((TEX, TEX), -1, dtype=np.int64)
src[iy, ix] = np.arange(NPX)
for _ in range(3 * PAD):
    miss = src < 0
    if not miss.any():
        break
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        sh = np.roll(np.roll(src, dy, 0), dx, 1)
        take = (src < 0) & (sh >= 0)
        src[take] = sh[take]
filled = src >= 0
fi_ = src[filled]


def to_map(vals, fill):
    out = np.empty((TEX, TEX, vals.shape[1]))
    out[:] = fill
    out[filled] = vals[fi_]
    return out


colour = to_map(np.column_stack([srgb(ML), AO]), (srgb(np.array([0.4]))[0],) * 3 + (1.0,))
nrm_gl = to_map((NTS + 1) / 2, (0.5, 0.5, 1.0))
packed = to_map(np.column_stack([RO, IDv, ME_]), (0.6, 0.0, 0.0))
nrm_dx = nrm_gl.copy()
nrm_dx[..., 1] = 1.0 - nrm_dx[..., 1]
q8 = lambda a: np.clip(np.round(a * 255.0), 0, 255).astype(np.uint8)[::-1]  # noqa: E731
PATHS = {"colour": os.path.join(OUT, NAME + "_colour_ao.png"), "normal": os.path.join(OUT, NAME + "_normal_dx.png"),
         "normal_gl": os.path.join(OUT, NAME + "_normal_gl.png"), "packed": os.path.join(OUT, NAME + "_packed.png")}
write_png(PATHS["colour"], q8(colour))
write_png(PATHS["normal"], q8(nrm_dx))
write_png(PATHS["normal_gl"], q8(nrm_gl))
write_png(PATHS["packed"], q8(packed))
LOG["maps"] = PATHS
# the values as written, by part (linear factor; roughness)
LOG["checks"]["byPart"] = {}
for k in KIND_SCALE:
    sel = PK == k
    if sel.any():
        LOG["checks"]["byPart"][k] = {"factorMean": ML[sel].mean(axis=0).round(3).tolist(),
                                      "roughness5_50_95": np.percentile(RO[sel], [5, 50, 95]).round(3).tolist(),
                                      "id": sorted(set(np.round(IDv[sel], 2).tolist())), "aoMean": round(float(AO[sel].mean()), 3)}
LOG["checks"]["scuffShareOfLeather"] = round(float((SCUFF[LEATHER] > 0.3).mean()), 4)
LOG["checks"]["threadShareOfLeather"] = round(float((THREAD[LEATHER] > 0.3).mean()), 4)
say("maps written", PATHS)

# ---- 7. NO SEAM ON THE UPPER: at each UV seam's edge midpoints, the two sides' maps sampled where they meet ----------
NRM_DEC = q8(nrm_gl)[::-1].astype(np.float64) / 255.0 * 2 - 1
COL_DEC = q8(colour)[::-1].astype(np.float64) / 255.0
PK_DEC = q8(packed)[::-1].astype(np.float64) / 255.0


def bilinear(img, uv):
    x = uv[0] * TEX - 0.5
    y = uv[1] * TEX - 0.5
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    fx, fy = x - x0, y - y0
    x0, y0 = np.clip([x0, x0 + 1], 0, TEX - 1), np.clip([y0, y0 + 1], 0, TEX - 1)
    return ((1 - fx) * (1 - fy) * img[y0[0], x0[0]] + fx * (1 - fy) * img[y0[0], x0[1]]
            + (1 - fx) * fy * img[y0[1], x0[0]] + fx * fy * img[y0[1], x0[1]])


edge_faces = {}
for pi, (ls_, lt_) in enumerate(EPOLY_LOOPS):
    vs = LV[ls_:ls_ + lt_]
    for j in range(lt_):
        key = tuple(sorted((int(vs[j]), int(vs[(j + 1) % lt_]))))
        edge_faces.setdefault(key, []).append((pi, ls_ + j, ls_ + (j + 1) % lt_))
MEAS = {}
for key, fl in edge_faces.items():
    if len(fl) != 2:
        continue
    (pa, la0, la1), (pb, lb0, lb1) = fl
    if KIND_OF[EKIND[pa]] not in ("vamp", "quarters") or KIND_OF[EKIND[pb]] not in ("vamp", "quarters"):
        continue
    if LV[la0] != LV[lb0]:
        lb0, lb1 = lb1, lb0
    is_seam = not (np.abs(LUV[la0] - LUV[lb0]).max() < 1e-7 and np.abs(LUV[la1] - LUV[lb1]).max() < 1e-7)
    # near a drawn line (stitches, edges) or away from them: a seam is compared with ordinary edges in the same company
    mid3 = 0.5 * (LP[la0] + LP[la1])
    bb = BOOT[int(ESIDE[pa])]
    dn = min(float(np.min(np.linalg.norm(C_[0] - mid3, axis=1))) for C_ in bb["curves"].values())
    near = dn < 0.007
    ang, dcol, drough = MEAS.setdefault((is_seam, near), ([], [], []))
    for f in (0.25, 0.5, 0.75):
        out_ = []
        for l0, l1 in ((la0, la1), (lb0, lb1)):
            uv = (1 - f) * LUV[l0] + f * LUV[l1]
            # a hair inside its own face (the edge itself is the island's border)
            pc_ = EPOLY_LOOPS[pa if l0 == la0 else pb]
            cuv = LUV[pc_[0]:pc_[0] + pc_[1]].mean(axis=0)
            uv = uv + (cuv - uv) * (0.5 / max(0.5, np.linalg.norm((cuv - uv) * TEX)))
            n_ = (1 - f) * LN[l0] + f * LN[l1]
            n_ /= np.linalg.norm(n_)
            t_ = (1 - f) * LT[l0] + f * LT[l1]
            t_ -= (t_ @ n_) * n_
            t_ /= np.linalg.norm(t_)
            b_ = np.sign(LS[l0] or 1) * np.cross(n_, t_)
            ts = bilinear(NRM_DEC, uv)
            w_ = ts[0] * t_ + ts[1] * b_ + ts[2] * n_
            out_.append((w_ / np.linalg.norm(w_), bilinear(COL_DEC, uv), bilinear(PK_DEC, uv)))
        ang.append(math.degrees(math.acos(float(np.clip(out_[0][0] @ out_[1][0], -1, 1)))))
        dcol.append(float(np.abs(out_[0][1][:3] - out_[1][1][:3]).max()) * 255)
        drough.append(float(abs(out_[0][2][0] - out_[1][2][0])) * 255)
# against the same measure across the ordinary (non-seam) edges of the same parts: a seam shows only if it differs more
LOG["checks"]["upperSeams"] = {}
for (is_seam, near), (ang, dcol, drough) in sorted(MEAS.items()):
    LOG["checks"]["upperSeams"][("seams" if is_seam else "ordinaryEdges") + ("NearLines" if near else "Away")] = {
        "samples": len(ang), "normalDeg50_95_99": np.percentile(ang, [50, 95, 99]).round(2).tolist(),
        "colour255_50_95_99": np.percentile(dcol, [50, 95, 99]).round(2).tolist(),
        "rough255_50_95_99": np.percentile(drough, [50, 95, 99]).round(2).tolist()}
say("upper seams", LOG["checks"]["upperSeams"])
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_maps.blend"))
json.dump(LOG, open(os.path.join(OUT, NAME + "_maps.json"), "w"), indent=1, default=str)
say("maps stage written")

# ---- 8. THE PAIRS WRITTEN WITH THE UVS, each from a fresh import, and checked against its original -----------------
SRC_UVS = SRC_UV.copy()
RINGS = {side: (b["ring_top_ix"], b["outer"]) for side, b in BOOT.items()}
FACE_KIND = kind.copy()


def welt_clearance(co):
    """Each boot: how far (in plan) the upper's foot stands in from the welt's edge, over the upper's points in the
    5 mm just above the welt's top (millimetres; the welt's stitch is drawn --welt-stitch mm in from the edge)."""
    out = {}
    for side, (rix, oix) in RINGS.items():
        ring = co[rix]
        ring = np.vstack([ring, ring[:1]])
        pts = co[oix]
        # each upper point's height over the welt's top at its nearest rim point
        d2 = ((pts[:, None, :2] - ring[None, :-1, :2]) ** 2).sum(2)
        j = d2.argmin(1)
        dz = pts[:, 2] - ring[j, 2]
        sel = (dz > 0.0) & (dz < 0.005)
        r2 = ring.copy()
        r2[:, 2] = 0.0
        q = pts[sel].copy()
        q[:, 2] = 0.0
        d, _t, _a, _b, _l = curve_coords(q, r2, np.tile(Z, (len(q), 1)))
        out["left" if side == 0 else "right"] = np.percentile(d * 1000, [0, 1, 5, 50]).round(2).tolist()
    return out


def face_areas(mesh):
    return np.array([p_.area for p_ in mesh.data.polygons])


SRC_AREAS = face_areas(pair)


def export_with_uvs(fbx, out_dir, name):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mesh, arm_ = load_pair(fbx)
    lv = np.zeros(len(mesh.data.loops), dtype=np.int64)
    mesh.data.loops.foreach_get("vertex_index", lv)
    rep = {"from": fbx, "loopsMatchSource": bool(len(lv) == len(SRC_LOOPV) and np.array_equal(lv, SRC_LOOPV))}
    if not rep["loopsMatchSource"]:
        rep["written"] = None
        return rep
    uvl_ = mesh.data.uv_layers
    while len(uvl_) > 1:
        uvl_.remove(uvl_[-1])
    uvl_[0].data.foreach_set("uv", SRC_UVS.ravel())
    mesh.data.update()
    path = os.path.join(out_dir, name + "_skinned.fbx")
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    arm_.select_set(True)
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = arm_
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, object_types={"ARMATURE", "MESH"}, add_leaf_bones=False,
                             mesh_smooth_type="FACE", bake_anim=False, colors_type="LINEAR")
    rep["written"] = path

    # read both back and compare point for point
    def read(p_):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        m_, a_ = load_pair(p_)
        co = np.array([m_.matrix_world @ v.co for v in m_.data.vertices])
        gn = {g.index: g.name for g in m_.vertex_groups}
        W = {}
        for v in m_.data.vertices:
            for g in v.groups:
                W[(v.index, gn[g.group])] = g.weight
        bones = {bn.name: (np.array(a_.matrix_world @ bn.head_local), np.array(a_.matrix_world @ bn.tail_local)) for bn in a_.data.bones}
        uv_ = np.zeros(len(m_.data.loops) * 2)
        m_.data.uv_layers[0].data.foreach_get("uv", uv_)
        nrm = np.zeros(len(m_.data.loops) * 3)
        m_.data.corner_normals.foreach_get("vector", nrm)
        return dict(co=co, W=W, bones=bones, uv=uv_.reshape(-1, 2), uvn=len(m_.data.uv_layers), n=nrm.reshape(-1, 3),
                    mats=[x.name.split(".")[0] for x in m_.data.materials], faces=len(m_.data.polygons), arm=a_.name)
    areas = face_areas(mesh)
    o_, n_ = read(fbx), read(path)
    keys = set(o_["W"]) | set(n_["W"])
    ratio = np.sqrt(areas / np.maximum(SRC_AREAS, 1e-12))
    rep["sizeAgainstSource1_50_99"] = {k_: np.percentile(ratio[FACE_KIND == k_], [1, 50, 99]).round(3).tolist()
                                       for k_ in ("vamp", "quarters", "sole_top", "sole_side_lat", "sole_side_med")}
    rep["weltClearanceMm0_1_5_50"] = welt_clearance(n_["co"])
    rep.update({
        "points": len(n_["co"]), "faces": [o_["faces"], n_["faces"]], "materials": n_["mats"], "uvLayers": n_["uvn"],
        "maxPointMoveMm": round(float(np.abs(o_["co"] - n_["co"]).max() * 1000), 6),
        "weightsCompared": len(keys),
        "maxWeightChange": float(max(abs(o_["W"].get(k_, 0.0) - n_["W"].get(k_, 0.0)) for k_ in keys)),
        "bones": [len(o_["bones"]), len(n_["bones"])],
        "maxBoneMoveMm": round(float(max(max(np.abs(o_["bones"][k_][0] - n_["bones"][k_][0]).max(),
                                             np.abs(o_["bones"][k_][1] - n_["bones"][k_][1]).max()) for k_ in o_["bones"]) * 1000), 6),
        "maxNormalChange": round(float(np.abs(o_["n"] - n_["n"]).max()), 6),
        "maxUvError": float(np.abs(n_["uv"] - SRC_UVS).max()),
    })
    return rep


LOG["checks"]["weltClearanceMm0_1_5_50"] = welt_clearance(CO)
say("welt clearance (mm, min 1st 5th 50th)", LOG["checks"]["weltClearanceMm0_1_5_50"])
LOG["exports"] = [] if NO_EXPORT else [export_with_uvs(SRC, OUT, NAME)]
for fbx, odir in ([] if NO_EXPORT else CARRY):
    os.makedirs(odir, exist_ok=True)
    nm_ = os.path.basename(fbx).replace("_skinned.fbx", "")
    rep = export_with_uvs(fbx, odir, nm_)
    LOG["exports"].append(rep)
    json.dump({"source": SRC, "maps": PATHS, "export": rep}, open(os.path.join(odir, "maps-carry.json"), "w"), indent=1, default=str)
for r_ in LOG["exports"]:
    say("export", json.dumps(r_, default=str))
LOG["seconds"] = round(time.time() - T0, 1)
json.dump(LOG, open(os.path.join(OUT, NAME + "_maps.json"), "w"), indent=1, default=str)
say("done")
