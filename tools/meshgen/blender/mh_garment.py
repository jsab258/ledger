"""A MakeHuman garment fitted to a MetaHuman (fit_mhclo.py) made ready for the game: the parts wanted kept, re-coloured
for 1990, its sewing pattern marked, its loose part marked for cloth.

    blender -b -P tools/meshgen/blender/mh_garment.py -- FITTED.blend GARMENT_DIR OUT_DIR --name tom_suit_jacket --drop-below-hips [options]

WHY, 30 September (Jafar's list after the outside audit: "one properly skinned jacket ... proven on two approved
bodies"; his ruling of the same day, DECISIONS.md: suits and coats from the free MakeHuman ones, CC0, refitted in
Blender and bound as skinned meshes panel by panel). A MakeHuman garment is already a game mesh: modelled by hand,
four-sided faces, loops at the joints, unwrapped with a texture (the retopology stage done by its maker). The shape
comes from a tailor's model, not from Blender's cloth, which gave the donkey jacket a padded look three reviews
running (production/art/clothing/donkey-jacket-game/review-3.md). What this adds:
  --drop-below-hips   the pieces whose middle lies below the hip joints left out (a suit's trousers: the jacket is
                      proven alone first; the audit stops new garment families);
  the pieces:         the largest is the garment; the others (a shirt front, a tie, cuffs, buttons) stay with it;
  the colours:        the maker's texture re-coloured piece by piece: the garment's own (--cloth-srgb, the maker's
                      weave and shading kept, its pattern such as a pinstripe softened away by --plain pixels), the
                      shirt (--shirt-srgb), the tie (--tie-srgb), buttons (--button-srgb); the maker's normal map kept;
  "pattern":          a copy of the maker's UV layout (one island a panel), which the builder's binder reads;
  SimMaxDistance:     the loose part below --sim-below (metres; default 4 cm under the hip joints) marked for cloth.
OUT_DIR gets NAME.blend (the object NAME beside the body), NAME_static.fbx, NAME_basecolor.png, NAME_normal.png and
garment.json (with the maker's name, source and licence read from the pack record).
"""
import json
import math
import os
import shutil
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
FITTED, GDIR, OUT = argv[0], argv[1], argv[2]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


def rgb(name, default):
    return np.array([float(c) for c in opt(name, default, str).split(",")])


NAME = opt("--name", "garment", str)
log = {"fitted": FITTED, "garmentDir": GDIR, "name": NAME}


def say(*a):
    print("MHG", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=FITTED)
g = bpy.data.objects["GarmentRender"]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE" and "Base" not in o.name)
J = lambda n: arm.matrix_world @ arm.pose.bones[n].head  # noqa: E731
hip_z = (J("thigh_l").z + J("thigh_r").z) / 2

# ---- the pieces ---------------------------------------------------------------------------------------------------
bm = bmesh.new()
bm.from_mesh(g.data)
bm.faces.ensure_lookup_table()
comp = [-1] * len(bm.faces)
for f0 in bm.faces:
    if comp[f0.index] >= 0:
        continue
    comp[f0.index] = f0.index
    st = [f0]
    while st:
        f = st.pop()
        for e in f.edges:
            for f2 in e.link_faces:
                if comp[f2.index] < 0:
                    comp[f2.index] = f0.index
                    st.append(f2)
pieces = {}
for f in bm.faces:
    pieces.setdefault(comp[f.index], []).append(f)
mw = g.matrix_world


def centre(fs):
    return sum((mw @ f.calc_center_median() for f in fs), Vector()) / len(fs)


def zrange(fs):
    zs = [(mw @ v.co).z for f in fs for v in f.verts]
    return min(zs), max(zs)


def xwidth(fs):
    xs = [(mw @ v.co).x for f in fs for v in f.verts]
    return max(xs) - min(xs)


dropped = []
if "--drop-below-hips" in argv:
    dropped = [k for k, fs in pieces.items() if centre(fs).z < hip_z]
main = max((k for k in pieces if k not in dropped), key=lambda k: len(pieces[k]))
kind = {}
for k, fs in pieces.items():
    if k in dropped:
        continue
    c = centre(fs)
    lo, hi = zrange(fs)
    if k == main:
        kind[k] = "cloth"
    elif len(fs) <= opt("--button-faces", 64, int):
        kind[k] = "button"
    elif abs(c.x) < 0.03 and hi - lo > 0.12 and c.y < 0 and xwidth(fs) < 0.06:
        kind[k] = "tie"
    elif abs(c.x) > min(abs(J("upperarm_l").x), abs(J("upperarm_r").x)) and "--keep-cuffs" not in argv:
        dropped.append(k)                     # a shirt's cuff: the sleeve hides it, and it came through as shards
    else:
        kind[k] = "shirt"
log["pieces"] = {kd: sum(len(pieces[k]) for k in kind if kind[k] == kd) for kd in set(kind.values())}
log["droppedFaces"] = sum(len(pieces[k]) for k in dropped)
say("pieces", json.dumps(log["pieces"]), "dropped", log["droppedFaces"])
gone = [f for k in dropped for f in pieces[k]]
face_kind = {f.index: kind.get(comp[f.index]) for f in bm.faces}
kinds_left = [face_kind[f.index] for f in bm.faces if f.index not in {x.index for x in gone}]
bmesh.ops.delete(bm, geom=gone, context="FACES")
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
bm.to_mesh(g.data)
bm.free()
g.data.update()
me = g.data
pk = me.attributes.new("piece", "INT", "FACE")
KINDS = ["cloth", "shirt", "tie", "button"]
for i, kd in enumerate(kinds_left):
    pk.data[i].value = KINDS.index(kd)

# ---- the breast pocket's handkerchief pressed flat: the cloth's faces the maker's texture paints white (a pocket
# square), on the chest, are laid onto the jacket's surface round them, so a plain welt pocket is left
if "--remove-pocket-square" in argv:
    _img = None
    _mhm = next((os.path.join(GDIR, f) for f in os.listdir(GDIR) if f.endswith(".mhmat")), None)
    for line in open(_mhm, encoding="utf-8", errors="ignore"):
        w_ = line.split()
        if len(w_) >= 2 and w_[0] == "diffuseTexture":
            _img = bpy.data.images.load(os.path.join(GDIR, w_[1]))
    Wd, Hd = _img.size
    Dd = np.array(_img.pixels[:]).reshape(Hd, Wd, 4)[:, :, :3]
    uvd0 = me.uv_layers["UVMap"].data
    chest_lo = hip_z + 0.2
    sq = []
    for p_ in me.polygons:
        if pk.data[p_.index].value != 0:
            continue
        u_ = np.mean([uvd0[li].uv[0] for li in p_.loop_indices])
        v_ = np.mean([uvd0[li].uv[1] for li in p_.loop_indices])
        if Dd[min(Hd - 1, int(v_ * Hd)), min(Wd - 1, int(u_ * Wd))].mean() > 0.35 and (mw @ p_.center).z > chest_lo:
            sq.append(p_.index)
    # the welt it sat in goes too (the fit crumpled the welt's end on the curved chest, and the review saw it torn):
    # any small piece of the maker's texture layout (under --welt-faces faces) touching the square
    if "--keep-welt" not in argv and sq:
        bw = bmesh.new()
        bw.from_mesh(me)
        uvw = bw.loops.layers.uv["UVMap"]
        bw.faces.ensure_lookup_table()
        islw = {}
        kw = 0
        for f in bw.faces:
            if f.index in islw:
                continue
            islw[f.index] = kw
            st_ = [f]
            while st_:
                x_ = st_.pop()
                for lp in x_.loops:
                    va, ua, ub = lp.vert, lp[uvw].uv, lp.link_loop_next[uvw].uv
                    for l2 in lp.edge.link_loops:
                        y_ = l2.face
                        if y_ is x_ or y_.index in islw:
                            continue
                        wa_, wb_ = (l2[uvw].uv, l2.link_loop_next[uvw].uv) if l2.vert is va else (l2.link_loop_next[uvw].uv, l2[uvw].uv)
                        if (ua - wa_).length < 1e-5 and (ub - wb_).length < 1e-5:
                            islw[y_.index] = kw
                            st_.append(y_)
            kw += 1
        sqset0 = set(sq)
        sqv0 = {v.index for i in sq for v in bw.faces[i].verts}
        size_ = {}
        for f in bw.faces:
            size_[islw[f.index]] = size_.get(islw[f.index], 0) + 1
        sq_c = sum((mw @ bw.faces[i].calc_center_median() for i in sq), Vector()) / len(sq)
        isl_c = {}
        for f in bw.faces:
            isl_c.setdefault(islw[f.index], []).append(mw @ f.calc_center_median())
        touch = {k_ for k_, cs in isl_c.items() if (sum(cs, Vector()) / len(cs) - sq_c).length < opt("--welt-reach", 0.04)
                 and not (set(i for i in range(len(bw.faces)) if islw[i] == k_) & sqset0)}
        welt = [f.index for f in bw.faces if islw[f.index] in touch and size_[islw[f.index]] < opt("--welt-faces", 150, int)]
        bw.free()
        log["weltFaces"] = len(welt)
        sq += welt
    sqv = sorted({vi for i in sq for vi in me.polygons[i].vertices})
    if sq:
        # taken out, and the slit it leaves closed (laid flat onto the chest it crumpled)
        bq = bmesh.new()
        bq.from_mesh(me)
        bq.faces.ensure_lookup_table()
        sqs = set(sq)
        bmesh.ops.delete(bq, geom=[bq.faces[i] for i in sq], context="FACES")
        bmesh.ops.delete(bq, geom=[v for v in bq.verts if not v.link_faces], context="VERTS")
        loops_ = []
        adj_ = {}
        for e in bq.edges:
            if e.is_boundary:
                a_, b_ = e.verts
                adj_.setdefault(a_, []).append(e)
                adj_.setdefault(b_, []).append(e)
        seen_ = set()
        small = []
        for e0 in [e for e in bq.edges if e.is_boundary]:
            if e0 in seen_:
                continue
            st_, comp_e = [e0], []
            while st_:
                e = st_.pop()
                if e in seen_:
                    continue
                seen_.add(e)
                comp_e.append(e)
                for v in e.verts:
                    st_ += [x for x in adj_[v] if x not in seen_]
            if len(comp_e) <= opt("--pocket-hole", 80, int):
                c_ = sum(((mw @ v.co) for e in comp_e for v in e.verts), Vector()) / (2 * len(comp_e))
                if c_.z > chest_lo:
                    small += comp_e
        if small:
            bmesh.ops.holes_fill(bq, edges=small, sides=0)
        bq.to_mesh(me)
        bq.free()
        me.update()
        # the "piece" attribute follows the faces kept (the new faces are cloth)
        pk = me.attributes["piece"]
    log["pocketSquare"] = {"faces": len(sq)}
    say("pocket square taken out", len(sq), "faces")
# ---- the breast pocket pressed flatter (the first review: "a thick, puffy, lifted flap ... a pouch stuck onto the
# chest"; taking its handkerchief out left the lapel's layers in shards, so nothing is taken out): the points of the
# jacket within --pocket-r of the pocket's middle, standing more than 3 mm proud of the chest round it, are brought
# down to 3 mm plus a third of their height (the pocket stays, low)
if "--press-pocket" in argv:
    from mathutils.bvhtree import BVHTree as _BVp
    _mhm2 = next((os.path.join(GDIR, f) for f in os.listdir(GDIR) if f.endswith(".mhmat")), None)
    for line in open(_mhm2, encoding="utf-8", errors="ignore"):
        w_ = line.split()
        if len(w_) >= 2 and w_[0] == "diffuseTexture":
            _img2 = bpy.data.images.load(os.path.join(GDIR, w_[1]))
    Wd2, Hd2 = _img2.size
    Dd2 = np.array(_img2.pixels[:]).reshape(Hd2, Wd2, 4)[:, :, :3]
    uvp = me.uv_layers["UVMap"].data
    white = []
    for p_ in me.polygons:
        if pk.data[p_.index].value != 0:
            continue
        u_ = np.mean([uvp[li].uv[0] for li in p_.loop_indices])
        v_ = np.mean([uvp[li].uv[1] for li in p_.loop_indices])
        cz = (mw @ p_.center).z
        if Dd2[min(Hd2 - 1, int(v_ * Hd2)), min(Wd2 - 1, int(u_ * Wd2))].mean() > 0.35 and cz > hip_z + 0.2:
            white.append(mw @ p_.center)
    if white:
        pc_ = sum(white, Vector()) / len(white)
        PR = opt("--pocket-r", 0.075)
        GPp = [mw @ v.co for v in me.vertices]
        ring_ = [i for i, q in enumerate(GPp) if PR < (q - pc_).length < PR + 0.04 and pk.data is not None]
        near_ = [i for i, q in enumerate(GPp) if (q - pc_).length < PR]
        # the chest round it: a plane through the ring's points (least squares), its normal outward
        R_ = np.array([tuple(GPp[i]) for i in ring_])
        cen = R_.mean(axis=0)
        _u, _s, vt = np.linalg.svd(R_ - cen)
        nrm = vt[2] if vt[2][1] < 0 else -vt[2]         # outward is towards -y (the front)
        inv_p = mw.inverted()
        pressed = 0
        for i in near_:
            q = np.array(tuple(GPp[i]))
            h_ = (q - cen) @ nrm
            if h_ > 0.003:
                w_ = 1.0 - max(0.0, ((GPp[i] - pc_).length - PR * 0.6) / (PR * 0.4))
                new_h = 0.003 + (h_ - 0.003) / 3.0
                q2 = q - nrm * (h_ - new_h) * max(0.0, min(1.0, w_))
                me.vertices[i].co = inv_p @ Vector(tuple(q2))
                pressed += 1
        me.update()
        log["pocketPressed"] = pressed
        say("breast pocket pressed", pressed, "points")
# ---- the shirt front and tie lowered under the jacket (the first review: white flecks of shirt beside the lapel's
# edge): every point of them moves --inner-sink towards his body, never nearer it than 2 mm
if opt("--inner-sink", 0.0) > 0:
    from mathutils.bvhtree import BVHTree as _BV3
    body3 = next(o for o in bpy.data.objects if o.type == "MESH" and "Body" in o.name)
    b3 = bmesh.new()
    b3.from_mesh(body3.data)
    b3.transform(body3.matrix_world)
    b3.normal_update()
    T3 = _BV3.FromBMesh(b3)
    b3.free()
    inner = {vi for p_ in me.polygons if pk.data[p_.index].value in (1, 2) for vi in p_.vertices}
    inv3 = mw.inverted()
    for vi in inner:
        w3 = mw @ me.vertices[vi].co
        h3, n3, _i, _d = T3.find_nearest(w3)
        if h3 is None:
            continue
        off3 = (w3 - h3).dot(n3)
        new_off = max(0.002, off3 - opt("--inner-sink", 0.003))
        me.vertices[vi].co = inv3 @ (w3 - n3 * (off3 - new_off))
    me.update()
    log["innerSunk"] = len(inner)
# ---- the cloth bridges the body's hollows (30 September: on Ron, arms raised, his belly's folds showed through the
# suit jacket; three reviewers had failed the donkey jacket for the body showing through stiff wool). Round an
# upright axis, the trunk's outer radius on a grid of heights and angles is filled from above: each cell takes the
# larger of itself and the smoothed grid, round after round, so dents (the folds under a belly, the groove of the
# spine, the hollows beside the chest) fill and bulges stay; each point then moves out by its cell's fill. Points
# near the arm (the sleeves, the armholes) are left, easing in over --arm-blend beyond --arm-r (at 11 cm and 6 cm
# the trunk moved while the sleeve beside it did not, and the seam at the back of the armpit opened).
if "--no-stiff" not in argv:
    body_s = next(o for o in bpy.data.objects if o.type == "MESH" and "Body" in o.name)
    GP0 = np.array([tuple(mw @ v.co) for v in me.vertices])
    chains_ = {s_: [np.array(tuple(J(n + s_))) for n in ("upperarm_", "lowerarm_", "hand_")] for s_ in "lr"}

    def arm_dist(P_):
        best = np.full(len(P_), 9.0)
        for s_ in "lr":
            for a_, b_ in ((chains_[s_][0], chains_[s_][1]), (chains_[s_][1], chains_[s_][2])):
                ab = b_ - a_
                t_ = np.clip(((P_ - a_) @ ab) / (ab @ ab), 0, 1)
                best = np.minimum(best, np.linalg.norm(P_ - (a_ + t_[:, None] * ab), axis=1))
        return best

    ARM_R = opt("--arm-r", 0.15)
    wa = np.clip((arm_dist(GP0) - ARM_R) / opt("--arm-blend", 0.08), 0, 1)
    wa = wa * wa * (3 - 2 * wa)
    # nor the front's opening above the top button (the lapels, the shirt and tie: layers a few millimetres apart,
    # which the stiffening parted, and the shirt showed through in flecks), easing in over 5 cm round it
    btn_z = max(((mw @ p_.center).z for p_ in me.polygons if pk.data[p_.index].value == 3 and abs((mw @ p_.center).x) < 0.06),
                default=hip_z + 0.3)
    vx = np.clip((np.abs(GP0[:, 0]) - opt("--v-half", 0.11)) / 0.05, 0, 1)
    vz = np.clip((btn_z - GP0[:, 2]) / 0.05, 0, 1)
    front_ = GP0[:, 1] < 0
    wv = np.where(front_, np.maximum(vx, vz), 1.0)
    wa = wa * (wv * wv * (3 - 2 * wv))
    is_cloth_s = np.zeros(len(GP0), bool)
    for p_ in me.polygons:
        if pk.data[p_.index].value == 0:
            is_cloth_s[list(p_.vertices)] = True
    z_lo = hip_z - 0.02
    z_hi = min(J("upperarm_l").z, J("upperarm_r").z) - opt("--stiff-below-shoulder", 0.04)
    NBs, DZs = 96, 0.012
    band_ = GP0[is_cloth_s & (GP0[:, 2] > z_lo) & (GP0[:, 2] < z_hi) & (wa > 0.99)]
    AXs = band_[:, :2].mean(axis=0)
    angs = np.mod(np.arctan2(GP0[:, 1] - AXs[1], GP0[:, 0] - AXs[0]), 2 * math.pi)
    rads = np.linalg.norm(GP0[:, :2] - AXs, axis=1)
    Ks = int(math.ceil((z_hi - z_lo) / DZs)) + 1
    ks = np.round((GP0[:, 2] - z_lo) / DZs).astype(int)
    bs = np.round(angs / (2 * math.pi) * NBs).astype(int) % NBs
    # each cell's mean radius (the largest let a pocket flap's face stand for its cell, and the flaps' edges tore)
    grid = np.full((Ks, NBs), np.nan)
    sel_ = is_cloth_s & (ks >= 0) & (ks < Ks) & (wa > 0.5)
    acc_ = np.zeros((Ks, NBs))
    cnt_ = np.zeros((Ks, NBs))
    np.add.at(acc_, (ks[sel_], bs[sel_]), rads[sel_])
    np.add.at(cnt_, (ks[sel_], bs[sel_]), 1)
    grid[cnt_ > 0] = acc_[cnt_ > 0] / cnt_[cnt_ > 0]
    known = ~np.isnan(grid)
    for k_ in range(Ks):
        row = grid[k_]
        ok = ~np.isnan(row)
        if ok.any() and not ok.all():
            idx = np.arange(NBs)
            row[~ok] = np.interp(idx[~ok], idx[ok], row[ok], period=NBs)
    for b_ in range(NBs):
        col_ = grid[:, b_]
        ok = ~np.isnan(col_)
        if ok.any() and not ok.all():
            idx = np.arange(Ks)
            col_[~ok] = np.interp(idx[~ok], idx[ok], col_[ok])
    grid = np.nan_to_num(grid)

    def gsmooth(a_, sg_z, sg_a):
        r1 = int(math.ceil(3 * sg_a))
        k1 = np.exp(-(np.arange(-r1, r1 + 1) / sg_a) ** 2 / 2)
        k1 /= k1.sum()
        a_ = np.apply_along_axis(lambda x: np.convolve(np.pad(x, r1, mode="wrap"), k1, mode="valid"), 1, a_)
        r0 = int(math.ceil(3 * sg_z))
        k0 = np.exp(-(np.arange(-r0, r0 + 1) / sg_z) ** 2 / 2)
        k0 /= k0.sum()
        return np.apply_along_axis(lambda x: np.convolve(np.pad(x, r0, mode="edge"), k0, mode="valid"), 0, a_)

    filled = grid.copy()
    for _ in range(opt("--stiff-rounds", 40, int)):
        filled = np.maximum(filled, gsmooth(filled, opt("--stiff-sz", 2.0), opt("--stiff-sa", 2.0)))
    fill = np.clip(gsmooth(filled - grid, 2.0, 2.5), 0, None)     # smooth, so neighbouring points move together
    # eased in at the top and bottom edges of the band
    wz = np.minimum(np.clip(np.arange(Ks) * DZs / 0.04, 0, 1), np.clip((Ks - 1 - np.arange(Ks)) * DZs / 0.05, 0, 1))
    fill *= (wz * wz * (3 - 2 * wz))[:, None]
    new_s = GP0.copy()
    most_s = 0.0
    fk_ = (GP0[:, 2] - z_lo) / DZs
    fb_ = angs / (2 * math.pi) * NBs

    def fill_at(i):
        k0 = int(math.floor(fk_[i]))
        b0 = int(math.floor(fb_[i]))
        tk, tb = fk_[i] - k0, fb_[i] - b0
        k0c, k1c = min(max(k0, 0), Ks - 1), min(max(k0 + 1, 0), Ks - 1)
        b0c, b1c = b0 % NBs, (b0 + 1) % NBs
        return ((1 - tk) * ((1 - tb) * fill[k0c, b0c] + tb * fill[k0c, b1c]) + tk * ((1 - tb) * fill[k1c, b0c] + tb * fill[k1c, b1c]))

    # every layer at a place (the jacket, the half beneath it, the shirt and tie) moves out by the same amount there,
    # so their order is kept (moved with the nearest jacket point, the shirt crossed the jacket's inner front)
    for i in np.where((fk_ > -0.5) & (fk_ < Ks - 0.5))[0]:
        d_ = fill_at(i) * wa[i]
        new_s[i, 0] += d_ * math.cos(angs[i])
        new_s[i, 1] += d_ * math.sin(angs[i])
        most_s = max(most_s, d_)
    inv_ = mw.inverted()
    for i, v in enumerate(me.vertices):
        v.co = inv_ @ Vector(tuple(new_s[i]))
    me.update()
    log["stiff"] = {"from": round(float(z_lo), 3), "to": round(float(z_hi), 3), "mostMm": round(most_s * 1000, 1),
                    "meanFillMm": round(float(fill[known].mean()) * 1000, 1) if known.any() else 0}
    say("stiffened", json.dumps(log["stiff"]))
# ---- the skirt falls straight (30 September, the suit jacket on Darren: MakeHuman's base body draws the jacket's
# skirt round each thigh, so its hem pinched in between the legs and read as shorts). Below --straight-from metres
# above the hip joints, each point is set at the radius (round an upright axis through his hips) the jacket has at
# that angle at the top of the skirt, or the body's own outline there (its convex hull, the legs bridged) plus
# --ease, whichever is more, and never back in going down (a jacket falls plumb); the jacket's own small forms
# (pockets, flaps, the front's overlap) ride on that as they were, measured against its own smoothed radius; the
# change eases in over 5 cm below the top.
if "--no-straight" not in argv:
    body = next(o for o in bpy.data.objects if o.type == "MESH" and "Body" in o.name)
    BP = np.array([tuple(body.matrix_world @ v.co) for v in body.data.vertices])
    armg = {vg.index for vg in body.vertex_groups if vg.name.startswith(("upperarm", "lowerarm", "hand", "thumb", "index", "middle", "ring", "pinky"))}
    keep_b = np.array([sum(ge.weight for ge in v.groups if ge.group in armg) < 0.3 for v in body.data.vertices])
    BP = BP[keep_b]
    NB, DZ = 144, 0.01
    top = hip_z + opt("--straight-from", 0.03)
    GP = np.array([tuple(mw @ v.co) for v in me.vertices])
    band = BP[(BP[:, 2] > hip_z) & (BP[:, 2] < hip_z + 0.25)]
    AX = band[:, :2].mean(axis=0)
    ang = np.mod(np.arctan2(GP[:, 1] - AX[1], GP[:, 0] - AX[0]), 2 * math.pi)
    rad = np.linalg.norm(GP[:, :2] - AX, axis=1)
    bb = np.round(ang / (2 * math.pi) * NB).astype(int) % NB
    is_cloth_v = np.zeros(len(GP), bool)
    for p_ in me.polygons:
        if pk.data[p_.index].value == 0:
            is_cloth_v[list(p_.vertices)] = True
    low = GP[:, 2].min()
    K = int(math.ceil((top - low) / DZ)) + 2
    kk = np.clip(np.round((top - GP[:, 2]) / DZ).astype(int), 0, K - 1)

    def fill_circ(a_):
        ok = ~np.isnan(a_)
        if ok.all() or not ok.any():
            return np.nan_to_num(a_)
        idx = np.arange(len(a_))
        a_ = a_.copy()
        a_[~ok] = np.interp(idx[~ok], idx[ok], a_[ok], period=len(a_))
        return a_

    def smooth_circ(a_, sg):
        r_ = int(math.ceil(3 * sg))
        kx = np.exp(-(np.arange(-r_, r_ + 1) / sg) ** 2 / 2)
        kx /= kx.sum()
        return np.convolve(np.pad(a_, r_, mode="wrap"), kx, mode="valid")

    # the jacket's own radius, per row and angle (its outer face: the largest radius in each cell), smoothed
    RO = np.full((K, NB), np.nan)
    sel = is_cloth_v & (GP[:, 2] <= top + 0.02)
    for k_, b_, r_ in zip(kk[sel], bb[sel], rad[sel]):
        if np.isnan(RO[k_, b_]) or r_ > RO[k_, b_]:
            RO[k_, b_] = r_
    for k_ in range(K):
        RO[k_] = smooth_circ(fill_circ(RO[k_]), 2.0)
    r_top = smooth_circ(np.nanmax(np.vstack([RO[0], RO[min(1, K - 1)]]), axis=0), 2.0)
    EASE = opt("--ease", 0.02)
    HULL = np.zeros((K, NB))
    dirs = np.stack([np.cos(np.arange(NB) * 2 * math.pi / NB), np.sin(np.arange(NB) * 2 * math.pi / NB)], axis=1)
    for k_ in range(K):
        z_ = top - k_ * DZ
        sl = BP[np.abs(BP[:, 2] - z_) < 0.015][:, :2] - AX
        if len(sl) < 6:
            HULL[k_] = HULL[k_ - 1] if k_ else 0
            continue
        proj = sl @ dirs.T                        # the hull's support in each direction
        HULL[k_] = proj.max(axis=0) + EASE
    R = np.maximum(r_top[None, :], np.maximum.accumulate(HULL, axis=0))
    w_row = np.clip(np.arange(K) * DZ / 0.05, 0, 1)
    w_row = w_row * w_row * (3 - 2 * w_row)
    moved_, most_ = 0, 0.0
    new_co = GP.copy()
    for i in np.where(is_cloth_v & (GP[:, 2] < top))[0]:
        k_, b_ = kk[i], bb[i]
        detail = rad[i] - RO[k_, b_]
        target = R[k_, b_] + min(detail, 0.03)
        d_ = (target - rad[i]) * w_row[k_]
        if abs(d_) > 1e-4:
            moved_ += 1
            most_ = max(most_, abs(d_))
        new_co[i, 0] += d_ * math.cos(ang[i])
        new_co[i, 1] += d_ * math.sin(ang[i])
    # the pieces sewn on the skirt (buttons, flaps) move with the cloth nearest them
    from mathutils.kdtree import KDTree as _KD
    cl = np.where(is_cloth_v)[0]
    kd_ = _KD(len(cl))
    for j_, i in enumerate(cl):
        kd_.insert(Vector(tuple(GP[i])), j_)
    kd_.balance()
    for i in np.where(~is_cloth_v & (GP[:, 2] < top))[0]:
        j_ = cl[kd_.find(Vector(tuple(GP[i])))[1]]
        new_co[i] = GP[i] + (new_co[j_] - GP[j_])
    inv = mw.inverted()
    for i, v in enumerate(me.vertices):
        v.co = inv @ Vector(tuple(new_co[i]))
    me.update()
    # the hem levelled (on Ron a pouch hung between the legs at the front, below the rest of the hem): the hem's
    # height is the median of each angle's lowest point; nothing of the cloth hangs more than --hem-drop below it
    GP2 = np.array([tuple(mw @ v.co) for v in me.vertices])
    lowest = np.full(NB, np.nan)
    for b_, z_ in zip(bb[is_cloth_v], GP2[is_cloth_v, 2]):
        if np.isnan(lowest[b_]) or z_ < lowest[b_]:
            lowest[b_] = z_
    hem_level = float(np.nanmedian(lowest))
    floor_ = hem_level - opt("--hem-drop", 0.006)
    need_ = np.maximum(0.0, floor_ - GP2[:, 2]) * 0.85
    need_[~is_cloth_v] = 0.0
    lift_ = need_.copy()
    ed2 = np.array([e.vertices[:] for e in me.edges])
    dg2 = np.bincount(ed2.ravel(), minlength=len(GP2)).astype(float)
    for _ in range(opt("--hem-smooth", 25, int)):
        acc2 = np.zeros(len(GP2))
        np.add.at(acc2, ed2[:, 0], lift_[ed2[:, 1]])
        np.add.at(acc2, ed2[:, 1], lift_[ed2[:, 0]])
        lift_ = np.maximum(need_, 0.5 * lift_ + 0.5 * acc2 / np.maximum(dg2, 1))
    raised = int((lift_ > 1e-4).sum())
    inv2 = mw.inverted()
    for i, v in enumerate(me.vertices):
        if lift_[i] > 1e-5:
            q_ = GP2[i].copy()
            q_[2] += lift_[i]
            v.co = inv2 @ Vector(tuple(q_))
    me.update()
    log["hemLevel"] = {"z": round(hem_level, 3), "raised": raised}
    log["straightSkirt"] = {"top": round(float(top), 3), "moved": int(moved_), "mostMm": round(most_ * 1000, 1)}
    say("skirt straightened", moved_, "points, most", round(most_ * 1000, 1), "mm")
# ---- the shirt and tie set under the jacket, the collars as a pair (the second review: "the back edge of the shirt
# collar ragged: a jagged white rim with dark slivers across the nape"; the research: fit the two collars together
# with a fixed gap). Along the line out from his body at each shirt or tie point: where the jacket lies over it, the
# point is set --under metres inside the jacket (never nearer him than 1 mm); where nothing of the jacket is over it
# (the collar band above the jacket's collar, the V), it stays.
if "--no-under" not in argv:
    from mathutils.bvhtree import BVHTree as _BV5
    body5 = next(o for o in bpy.data.objects if o.type == "MESH" and "Body" in o.name)
    b5_ = bmesh.new()
    b5_.from_mesh(body5.data)
    b5_.transform(body5.matrix_world)
    b5_.normal_update()
    TB5 = _BV5.FromBMesh(b5_)
    b5_.free()
    Vw5 = [mw @ v.co for v in me.vertices]
    TC5 = _BV5.FromPolygons(Vw5, [list(p_.vertices) for p_ in me.polygons if pk.data[p_.index].value == 0])
    # the collars only (set everywhere, the shirt went under the jacket's hidden under-front in the V, which then showed)
    collar_z = J("neck_01").z - opt("--under-below-neck", 0.04)
    inner5 = sorted({vi for p_ in me.polygons if pk.data[p_.index].value in (1, 2) for vi in p_.vertices
                     if (mw @ me.vertices[vi].co).z > collar_z})
    UNDER = opt("--under", 0.003)
    inv5 = mw.inverted()
    set_under = 0
    for vi in inner5:
        w5 = Vw5[vi]
        h5, n5, _i, _d = TB5.find_nearest(w5)
        if h5 is None:
            continue
        off5 = (w5 - h5).dot(n5)
        hit5 = TC5.ray_cast(h5 + n5 * 0.0005, n5, 0.10)
        if hit5[0] is None:
            continue
        dj = (hit5[0] - h5).dot(n5)
        target = max(0.001, dj - UNDER)
        if off5 > target:
            me.vertices[vi].co = inv5 @ (h5 + n5 * target + (w5 - h5 - n5 * off5))
            set_under += 1
    me.update()
    log["setUnder"] = set_under
    say("shirt and tie set under the jacket", set_under, "points")
# ---- the layers that never show taken out (30 September: on Darren the jacket's inner front, the half that buttons
# underneath, came through the shirt in the opening as dark shards, and the shirt showed in white flecks beside the
# lapels; games remove what an outer layer always hides, as fit_under.py does under the donkey jacket). Along the
# line out from his body at each face's middle: a jacket face lying under the shirt there goes, and a shirt or tie
# face lying outside the jacket there goes. Above the hips only; the neck and cuffs are left.
if "--cull" in argv:
    from mathutils.bvhtree import BVHTree as _BV4
    body4 = next(o for o in bpy.data.objects if o.type == "MESH" and "Body" in o.name)
    b4 = bmesh.new()
    b4.from_mesh(body4.data)
    b4.transform(body4.matrix_world)
    b4.normal_update()
    TB = _BV4.FromBMesh(b4)
    b4.free()
    Vw4 = [mw @ v.co for v in me.vertices]
    kind_of_face = [pk.data[p_.index].value for p_ in me.polygons]
    cloth_faces = [p_ for p_ in me.polygons if kind_of_face[p_.index] == 0]
    inner_faces = [p_ for p_ in me.polygons if kind_of_face[p_.index] in (1, 2)]
    TC = _BV4.FromPolygons(Vw4, [list(p_.vertices) for p_ in cloth_faces])
    TI = _BV4.FromPolygons(Vw4, [list(p_.vertices) for p_ in inner_faces]) if inner_faces else None
    neck4 = J("neck_01").z - 0.01
    GAPC = opt("--cull-gap", 0.001)
    gone4 = []
    for p_ in me.polygons:
        k4 = kind_of_face[p_.index]
        if k4 == 3:
            continue
        c4 = mw @ p_.center
        if c4.z < hip_z + 0.1 or c4.z > neck4:
            continue
        h4, n4, _i, _d = TB.find_nearest(c4)
        if h4 is None:
            continue
        d_self = (c4 - h4).dot(n4)
        if d_self <= 0:
            continue
        other = TI if k4 == 0 else TC
        if other is None:
            continue
        hit = other.ray_cast(h4 + n4 * 0.0005, n4, 0.12)
        if hit[0] is None:
            continue
        d_other = (hit[0] - h4).dot(n4)
        if k4 == 0 and d_other > d_self + GAPC:
            gone4.append(p_.index)          # the jacket under the shirt: never seen
        elif k4 in (1, 2) and d_other < d_self - GAPC:
            gone4.append(p_.index)          # the shirt outside the jacket: it would show through
    if gone4:
        b5 = bmesh.new()
        b5.from_mesh(me)
        b5.faces.ensure_lookup_table()
        bmesh.ops.delete(b5, geom=[b5.faces[i] for i in gone4], context="FACES")
        bmesh.ops.delete(b5, geom=[v for v in b5.verts if not v.link_faces], context="VERTS")
        b5.to_mesh(me)
        b5.free()
        me.update()
        pk = me.attributes["piece"]
    log["culled"] = len(gone4)
    say("hidden layers taken out", len(gone4), "faces")
# ---- the colours ---------------------------------------------------------------------------------------------------
mhmat = next((os.path.join(GDIR, f) for f in os.listdir(GDIR) if f.endswith(".mhmat")), None)
tex = {}
for line in open(mhmat, encoding="utf-8", errors="ignore"):
    w = line.split()
    if len(w) >= 2 and w[0] in ("diffuseTexture", "normalmapTexture", "bumpmapTexture"):
        tex[w[0]] = os.path.join(GDIR, w[1])
diff = bpy.data.images.load(tex["diffuseTexture"])
W_, H_ = diff.size
D = np.array(diff.pixels[:]).reshape(H_, W_, 4)[:, :, :3]


def srgb_to_lin(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def blur(a, sigma):
    if sigma <= 0:
        return a
    r = int(math.ceil(3 * sigma))
    k = np.exp(-(np.arange(-r, r + 1) / sigma) ** 2 / 2)
    k /= k.sum()
    a = np.apply_along_axis(lambda x: np.convolve(np.pad(x, r, mode="edge"), k, mode="valid"), 0, a)
    return np.apply_along_axis(lambda x: np.convolve(np.pad(x, r, mode="edge"), k, mode="valid"), 1, a)


# which piece each texel belongs to (rasterised from the UVs)
owner = np.full((H_, W_), -1, int)
uvd = me.uv_layers["UVMap"].data
for p_ in me.polygons:
    kd = pk.data[p_.index].value
    uvs = [np.array(uvd[li].uv) * (W_, H_) for li in p_.loop_indices]
    for j in range(1, len(uvs) - 1):
        a_, b_, c_ = uvs[0], uvs[j], uvs[j + 1]
        x0, y0 = np.floor(np.minimum(np.minimum(a_, b_), c_)).astype(int) - 1
        x1, y1 = np.ceil(np.maximum(np.maximum(a_, b_), c_)).astype(int) + 1
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W_ - 1, x1), min(H_ - 1, y1)
        if x1 < x0 or y1 < y0:
            continue
        m_ = np.array([[b_[0] - a_[0], c_[0] - a_[0]], [b_[1] - a_[1], c_[1] - a_[1]]])
        if abs(np.linalg.det(m_)) < 1e-9:
            continue
        inv = np.linalg.inv(m_)
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        l1 = inv[0, 0] * (xs - a_[0]) + inv[0, 1] * (ys - a_[1])
        l2 = inv[1, 0] * (xs - a_[0]) + inv[1, 1] * (ys - a_[1])
        ins = (l1 >= -0.02) & (l2 >= -0.02) & (l1 + l2 <= 1.02)
        blk = owner[y0:y1 + 1, x0:x1 + 1]
        blk[ins] = kd
# the maker's shading (its light and dark, the weave), kept as a multiplier round each piece's own mean; the pattern
# (a pinstripe) softened away
lum = D.mean(axis=2)
out = np.array(D)
targets = {"cloth": rgb("--cloth-srgb", "0.16,0.17,0.21"), "shirt": rgb("--shirt-srgb", "0.86,0.87,0.88"),
           "tie": rgb("--tie-srgb", "0.20,0.12,0.13"), "button": rgb("--button-srgb", "0.05,0.05,0.05")}
for i, kd in enumerate(KINDS):
    m_ = owner == i
    if not m_.any():
        continue
    L = lum.copy()
    if kd == "cloth":
        Lb = blur(np.where(m_, L, np.nan_to_num(L[m_].mean())), opt("--plain", 8.0))
        L = Lb
    shade = L / max(1e-6, float(L[m_].mean()))
    shade = np.clip(1 + (shade - 1) * opt("--shade", 0.6), 0.5, 1.5)
    col = srgb_to_lin(targets[kd])[None, None, :] * shade[:, :, None]
    lin_out = np.clip(col, 0, 1)
    out[m_] = np.where(lin_out[m_] <= 0.0031308, 12.92 * lin_out[m_], 1.055 * np.power(lin_out[m_], 1 / 2.4) - 0.055)
img_c = bpy.data.images.new(NAME + "_basecolor", W_, H_, alpha=False)
px = np.ones((H_, W_, 4))
px[:, :, :3] = out
img_c.pixels[:] = px.ravel()
img_c.filepath_raw = os.path.join(OUT, NAME + "_basecolor.png")
img_c.file_format = "PNG"
img_c.save()
nrm_src = tex.get("normalmapTexture")
if nrm_src:
    _ni = bpy.data.images.load(nrm_src)
    _ni.colorspace_settings.name = "Non-Color"
    Wn, Hn = _ni.size
    Nm = np.array(_ni.pixels[:]).reshape(Hn, Wn, 4)
    for c_ in (0, 1):
        Nm[:, :, c_] = 0.5 + (blur(Nm[:, :, c_], opt("--normal-soft", 2.5)) - 0.5) * opt("--normal-strength", 0.8)
    v3n = Nm[:, :, :3] * 2 - 1
    v3n[:, :, 2] = np.sqrt(np.clip(1 - v3n[:, :, 0] ** 2 - v3n[:, :, 1] ** 2, 0, 1))
    Nm[:, :, :3] = (v3n + 1) / 2
    img_nn = bpy.data.images.new(NAME + "_normal", Wn, Hn, alpha=False)
    img_nn.colorspace_settings.name = "Non-Color"
    img_nn.pixels[:] = Nm.ravel()
    img_nn.filepath_raw = os.path.join(OUT, NAME + "_normal.png")
    img_nn.file_format = "PNG"
    img_nn.save()
log["textures"] = {"basecolor": NAME + "_basecolor.png", "normal": NAME + "_normal.png" if nrm_src else None,
                   "normalFrom": os.path.basename(nrm_src) if nrm_src else None}
mat = bpy.data.materials.new("M_" + NAME)
mat.use_nodes = True
nt = mat.node_tree
bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
nc = nt.nodes.new("ShaderNodeTexImage")
nc.image = img_c
nt.links.new(nc.outputs["Color"], bsdf.inputs["Base Color"])
if nrm_src:
    img_n = bpy.data.images.load(os.path.join(OUT, NAME + "_normal.png"))
    img_n.colorspace_settings.name = "Non-Color"
    nn = nt.nodes.new("ShaderNodeTexImage")
    nn.image = img_n
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(nn.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
bsdf.inputs["Roughness"].default_value = opt("--rough", 0.85)
me.materials.clear()
me.materials.append(mat)
for p_ in me.polygons:
    p_.use_smooth = True

# ---- the pattern, and the loose part ---------------------------------------------------------------------------
pat = me.uv_layers.new(name="pattern")
src = me.uv_layers["UVMap"]
for i in range(len(src.data)):
    pat.data[i].uv = src.data[i].uv
me.uv_layers.active_index = 0
SIM_BELOW = opt("--sim-below", hip_z - 0.04)
Z = np.array([(mw @ v.co).z for v in me.vertices])
hem_z = Z.min()
ca = me.color_attributes.new(name="SimMaxDistance", type="FLOAT_COLOR", domain="POINT")
cloth_v = np.zeros(len(me.vertices), bool)
for p_ in me.polygons:
    if pk.data[p_.index].value == 0:
        cloth_v[list(p_.vertices)] = True
for i in range(len(me.vertices)):
    t = 0.0
    if cloth_v[i] and Z[i] < SIM_BELOW:
        t = (SIM_BELOW - Z[i]) / max(1e-6, SIM_BELOW - hem_z)
        t = t * t * (3 - 2 * t)
    ca.data[i].color = (t, t, t, 1.0)
log["simMaxDistance"] = {"below": round(float(SIM_BELOW), 3), "hemZ": round(float(hem_z), 3), "maxM": opt("--sim-max", 0.04)}

# ---- the maker's record ----------------------------------------------------------------------------------------------
key = os.path.basename(os.path.normpath(GDIR))
rec = None
packs = os.path.join(os.path.dirname(os.path.dirname(os.path.normpath(GDIR))), "packs")
if os.path.isdir(packs):
    for f in os.listdir(packs):
        d = json.load(open(os.path.join(packs, f), encoding="utf-8"))
        if key in d:
            rec = {k: d[key].get(k) for k in ("author", "license", "source", "created", "changed")}
log["asset"] = {"key": key, "record": rec}
g.name = NAME
me.name = NAME
log["faces"] = len(me.polygons)
log["tris"] = sum(len(p_.vertices) - 2 for p_ in me.polygons)
log["points"] = len(me.vertices)
bpy.ops.object.select_all(action="DESELECT")
g.select_set(True)
bpy.context.view_layer.objects.active = g
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_static.fbx"), use_selection=True, object_types={"MESH"},
                         mesh_smooth_type="OFF", use_tspace=True, add_leaf_bones=False, colors_type="LINEAR")
img_c.pack()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "garment.json"), "w"), indent=1)
say("done", json.dumps({k: log[k] for k in ("faces", "tris", "points")}), json.dumps(rec))
