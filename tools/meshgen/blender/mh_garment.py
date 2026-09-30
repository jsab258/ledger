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

# ---- the cloth bridges the body's hollows (30 September: on Ron, arms raised, his belly's folds showed through the
# suit jacket; three reviewers had failed the donkey jacket for the body showing through stiff wool). Round an
# upright axis, the trunk's outer radius on a grid of heights and angles is filled from above: each cell takes the
# larger of itself and the smoothed grid, round after round, so dents (the folds under a belly, the groove of the
# spine, the hollows beside the chest) fill and bulges stay; each point then moves out by its cell's fill. Points
# near the arm (the sleeves, the armholes) are left, easing in over 6 cm beyond --arm-r.
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

    ARM_R = opt("--arm-r", 0.11)
    wa = np.clip((arm_dist(GP0) - ARM_R) / 0.06, 0, 1)
    wa = wa * wa * (3 - 2 * wa)
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

    for i in np.where(is_cloth_s & (fk_ > -0.5) & (fk_ < Ks - 0.5))[0]:
        d_ = fill_at(i) * wa[i]
        new_s[i, 0] += d_ * math.cos(angs[i])
        new_s[i, 1] += d_ * math.sin(angs[i])
        most_s = max(most_s, d_)
    # the pieces on it (a shirt front, a tie, buttons, flaps) move with the cloth nearest them
    from mathutils.kdtree import KDTree as _KD2
    cl_ = np.where(is_cloth_s)[0]
    kd2_ = _KD2(len(cl_))
    for j_, i in enumerate(cl_):
        kd2_.insert(Vector(tuple(GP0[i])), j_)
    kd2_.balance()
    for i in np.where(~is_cloth_s)[0]:
        j_ = cl_[kd2_.find(Vector(tuple(GP0[i])))[1]]
        new_s[i] = GP0[i] + (new_s[j_] - GP0[j_])
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
    raised = 0
    floor_ = hem_level - opt("--hem-drop", 0.006)
    for i, v in enumerate(me.vertices):
        if GP2[i, 2] < floor_:
            q_ = GP2[i].copy()
            q_[2] = floor_ - (floor_ - GP2[i, 2]) * 0.15
            v.co = mw.inverted() @ Vector(tuple(q_))
            raised += 1
    me.update()
    log["hemLevel"] = {"z": round(hem_level, 3), "raised": raised}
    log["straightSkirt"] = {"top": round(float(top), 3), "moved": int(moved_), "mostMm": round(most_ * 1000, 1)}
    say("skirt straightened", moved_, "points, most", round(most_ * 1000, 1), "mm")
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
        Lb = blur(np.where(m_, L, np.nan_to_num(L[m_].mean())), opt("--plain", 3.0))
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
    shutil.copy(nrm_src, os.path.join(OUT, NAME + "_normal.png"))
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
