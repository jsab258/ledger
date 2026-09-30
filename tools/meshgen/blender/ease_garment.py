"""A finished garment eased for the game: more room where the layers under it need it, a crease pressed out, its
loose part marked for cloth, and exported with its sewing pattern kept.

    blender -b -P tools/meshgen/blender/ease_garment.py -- GARMENT.blend OUT_DIR --name ron_donkey [options]

WHY, 30 September (the builder's test of the sewn donkey jacket bound panel by panel and filmed moving in Unreal:
production/art/clothing/jacket-bound-test-2026-09-30; NOW.md, Handovers to clothing). The jacket walks and raises
its arms cleanly bound that way; what it still has to meet is its own shape's:
  --room MM --room-lo Z --room-hi Z    more room at the belly and hips (Epic's trousers come up to 118 cm and showed
                                       through its lower front walking): every point of the trunk between the two
                                       heights moved MM straight out from the body's middle line, all of a piece
                                       (buttons and pockets ride along), easing to nothing over 8 cm above and below;
  --press-lo Z --press-hi Z            a crease pressed out of the trunk between two heights (the builder: a crease
                                       across the chest): the wool's own points evened by Taubin's two passes, many
                                       rounds, the yoke's edge and small pieces (buttons) left as they are;
  --sim-below Z --sim-max M            the loose part (the skirt, below the hips) marked for Unreal's cloth: a vertex
                                       colour "SimMaxDistance" (0 skinned, 1 free to M metres) rising from Z to the hem,
                                       on the render mesh and on the coarse simulation mesh if the file has one.
The sleeves are never moved: a point is sleeve when it lies within --arm-r of the arm's bones.
The garment keeps its "pattern" UV layer (one island a panel), which the builder's binder reads.
OUT_DIR gets NAME_render_static.fbx, NAME_sim_static.fbx (if a sim mesh), NAME.blend, ease.json and pictures.
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
BLEND, OUT = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


NAME = opt("--name", "garment", str)
RENDER = opt("--render", "JacketRender", str)
SIM = opt("--sim", "JacketSim", str)
log = {"blend": BLEND}


def say(*a):
    print("EASE", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=BLEND)
g = bpy.data.objects[RENDER]
sim = bpy.data.objects.get(SIM)
arm = next((o for o in bpy.data.objects if o.type == "ARMATURE"), None)
body = next(o for o in bpy.data.objects if o.type == "MESH" and o.name not in (RENDER, SIM, "Jacket") and "Body" in o.name)
BVH = tailor.bvh_of(body)
bco = np.array([tuple(body.matrix_world @ v.co) for v in body.data.vertices])
if arm is not None:
    J = lambda n: np.array(tuple(arm.matrix_world @ arm.pose.bones[n].head))
else:
    J = None


def seg_d(P, a, b):
    ab = b - a
    t = np.clip(((P - a) @ ab) / max(1e-9, ab @ ab), 0.0, 1.0)
    return np.linalg.norm(P - (a + t[:, None] * ab), axis=1)


def sleeve_mask(P):
    if J is None:
        return np.zeros(len(P), bool)
    R = opt("--arm-r", 0.11)
    m = np.zeros(len(P), bool)
    for s in ("l", "r"):
        chain = [J("upperarm_" + s), J("lowerarm_" + s), J("hand_" + s)]
        d = np.minimum(seg_d(P, chain[0], chain[1]), seg_d(P, chain[1], chain[2]))
        # beyond the shoulder joint and near the arm
        out = (P[:, 0] * (1 if s == "l" else -1)) > abs(chain[0][0]) - 0.02
        m |= (d < R) & out
    return m


def ease(obj, label):
    me = obj.data
    P = np.array([tuple(obj.matrix_world @ v.co) for v in me.vertices])
    sl = sleeve_mask(P)
    # the small pieces (buttons): connected islands of fewer than 2% of the points
    n = len(P)
    ed = np.array([e.vertices[:] for e in me.edges])
    parent = np.arange(n)

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for a, b in ed:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    roots = np.array([find(i) for i in range(n)])
    _u, inv, cnt = np.unique(roots, return_inverse=True, return_counts=True)
    small = cnt[inv] < 0.02 * n
    moved_room = 0
    ROOM = opt("--room", 0.0) / 1000.0
    if ROOM > 0:
        lo, hi = opt("--room-lo", 0.85), opt("--room-hi", 1.25)
        cy = float(np.median(bco[(bco[:, 2] > lo) & (bco[:, 2] < hi) & (np.abs(bco[:, 0]) < 0.25), 1]))
        z = P[:, 2]
        w = np.clip(np.minimum((z - (lo - 0.08)) / 0.08, ((hi + 0.08) - z) / 0.08), 0.0, 1.0)
        w = w * w * (3 - 2 * w)
        w[sl] = 0.0
        d = np.column_stack([P[:, 0], P[:, 1] - cy, np.zeros(n)])
        L = np.linalg.norm(d, axis=1)
        d = d / np.maximum(L, 1e-9)[:, None]
        # a button or pocket island moves as its own middle does (all of a piece)
        for r in np.unique(roots[small]):
            ids = np.where(roots == r)[0]
            c = P[ids].mean(axis=0)
            wc = float(np.clip(min((c[2] - (lo - 0.08)) / 0.08, ((hi + 0.08) - c[2]) / 0.08), 0.0, 1.0))
            dc = np.array([c[0], c[1] - cy, 0.0])
            dc = dc / max(1e-9, np.linalg.norm(dc))
            d[ids] = dc
            w[ids] = wc * wc * (3 - 2 * wc) if not sl[ids].any() else 0.0
        P = P + d * (ROOM * w)[:, None]
        moved_room = int((w > 0.01).sum())
    moved_press = 0
    plo, phi = opt("--press-lo", 0.0), opt("--press-hi", 0.0)
    if phi > plo:
        z = P[:, 2]
        # the pressed band, faded over 4 cm at each end; the sleeves, small pieces and colour boundaries held
        wz = np.clip(np.minimum((z - plo) / 0.04, (phi - z) / 0.04), 0.0, 1.0)
        mats = np.zeros(n, int)
        border = np.zeros(n, bool)
        for poly in me.polygons:
            for vi in poly.vertices:
                if mats[vi] and mats[vi] != poly.material_index + 1:
                    border[vi] = True
                mats[vi] = poly.material_index + 1
        wz[sl | small | border] = 0.0
        e2 = ed[~(small[ed[:, 0]] | small[ed[:, 1]])]
        deg = np.bincount(e2.ravel(), minlength=n).astype(float)
        a0, a1 = e2[:, 0], e2[:, 1]
        for rnd in range(opt("--press-rounds", 60, int)):
            lam = 0.5 if rnd % 2 == 0 else -0.53
            # (sums by bincount: np.add.at was too slow for the hundreds of rounds a broad crease needs)
            acc = np.column_stack([np.bincount(a0, weights=P[a1, k], minlength=n) + np.bincount(a1, weights=P[a0, k], minlength=n)
                                   for k in range(3)])
            avg = acc / np.maximum(deg, 1)[:, None]
            ok = deg > 0
            P[ok] = P[ok] + (avg[ok] - P[ok]) * (lam * wz[ok])[:, None]
        moved_press = int((wz > 0.01).sum())
    ulo, uhi = opt("--unfold-lo", 0.0), opt("--unfold-hi", 0.0)
    if uhi > ulo:
        # FOLDS TAKEN OUT UP AND DOWN (Taubin's passes kept the broad horizontal fold across the chest and the sag
        # under the back yoke: they keep broad shapes by design). Round the body's middle line, the trunk's radius
        # is averaged in cells of angle and height, the cells' radii smoothed up and down only (a Gaussian of
        # --unfold-sigma metres), and each point moved by its cell's change: horizontal folds go, while everything
        # that runs up and down (the front band, the side seams) and every small piece (riding at its middle's
        # change) stays; the yoke and the wool under it move together, so the yoke's thickness is kept
        cy = float(np.median(bco[(bco[:, 2] > ulo) & (bco[:, 2] < uhi) & (np.abs(bco[:, 0]) < 0.25), 1]))
        th = np.arctan2(P[:, 0], -(P[:, 1] - cy))
        r = np.hypot(P[:, 0], P[:, 1] - cy)
        z = P[:, 2]
        NA, DZ = opt("--unfold-na", 180, int), opt("--unfold-dz", 0.003)     # fine cells (1 cm ones kept the ripples inside them)
        z0 = ulo - 0.10
        NZ = int(math.ceil((uhi + 0.10 - z0) / DZ))
        ia = np.clip(((th + math.pi) / (2 * math.pi) * NA).astype(int), 0, NA - 1)
        iz = np.clip(((z - z0) / DZ).astype(int), 0, NZ - 1)
        use = (~sl) & (~small) & (z > z0) & (z < uhi + 0.10)
        S = np.zeros((NA, NZ))
        C = np.zeros((NA, NZ))
        np.add.at(S, (ia[use], iz[use]), r[use])
        np.add.at(C, (ia[use], iz[use]), 1.0)
        R = np.where(C > 0, S / np.maximum(C, 1), np.nan)
        # empty cells filled from their column
        for a_ in range(NA):
            col = R[a_]
            ok = ~np.isnan(col)
            if ok.sum() >= 2:
                R[a_] = np.interp(np.arange(NZ), np.where(ok)[0], col[ok])
            else:
                R[a_] = np.nan
        sig = opt("--unfold-sigma", 0.04) / DZ
        kz = np.arange(-int(3 * sig), int(3 * sig) + 1)
        ker = np.exp(-0.5 * (kz / sig) ** 2)
        ker /= ker.sum()
        Rs = np.array([np.convolve(np.pad(R[a_], len(kz) // 2, mode="edge"), ker, mode="valid") if not np.isnan(R[a_]).any() else R[a_]
                       for a_ in range(NA)])
        delta = np.nan_to_num(Rs - R)
        # smoothed round the body a little too, and read between cells (cell by cell, the steps showed as a check)
        for _ in range(3):
            delta = 0.5 * delta + 0.25 * (np.roll(delta, 1, axis=0) + np.roll(delta, -1, axis=0))

        def sample(th_, z_):
            fa = (th_ + math.pi) / (2 * math.pi) * NA - 0.5
            fz = (z_ - z0) / DZ - 0.5
            a0_ = np.floor(fa).astype(int)
            z0_ = np.clip(np.floor(fz).astype(int), 0, NZ - 2)
            ta = fa - a0_
            tz = np.clip(fz - z0_, 0.0, 1.0)
            a0m, a1m = a0_ % NA, (a0_ + 1) % NA
            return ((delta[a0m, z0_] * (1 - ta) + delta[a1m, z0_] * ta) * (1 - tz)
                    + (delta[a0m, z0_ + 1] * (1 - ta) + delta[a1m, z0_ + 1] * ta) * tz)
        # faded over 4 cm at each end of the band; no change on the sleeves
        wz = np.clip(np.minimum((z - ulo) / 0.04, (uhi - z) / 0.04), 0.0, 1.0)
        wz[sl] = 0.0
        dr = sample(th, z) * wz
        for rr in np.unique(roots[small]):
            ids = np.where(roots == rr)[0]
            c_ = P[ids].mean(axis=0)
            a_c = int(np.clip((math.atan2(c_[0], -(c_[1] - cy)) + math.pi) / (2 * math.pi) * NA, 0, NA - 1))
            z_c = int(np.clip((c_[2] - z0) / DZ, 0, NZ - 1))
            wc = float(np.clip(min((c_[2] - ulo) / 0.04, (uhi - c_[2]) / 0.04), 0.0, 1.0))
            dr[ids] = 0.0 if sl[ids].any() else float(sample(np.array([math.atan2(c_[0], -(c_[1] - cy))]), np.array([c_[2]]))[0]) * wc
        dirs = np.column_stack([np.sin(th), -np.cos(th), np.zeros(n)])
        P = P + dirs * dr[:, None]
        log.setdefault("unfold", {})[label] = {"moved": int((np.abs(dr) > 0.0005).sum()), "mostMm": round(float(np.abs(dr).max()) * 1000, 1)}
    RZ = opt("--relax-zones", "", str)
    if RZ:
        # A TUCK UNFOLDED (the chest's crease is the surface folding under itself, found by its downward-facing
        # faces at 1.40 to 1.45 m, which no smoothing of the radius can reach): in each zone (front or back, a height
        # and a half-height), the wool's points drawn plainly towards their neighbours' middle, weighted by a
        # Gaussian in height, kept 4 mm off him every few rounds; sleeves, small pieces and colour borders held
        cy = float(np.median(bco[(np.abs(bco[:, 0]) < 0.25) & (bco[:, 2] > 1.0) & (bco[:, 2] < 1.5), 1]))
        mats = np.zeros(n, int)
        border = np.zeros(n, bool)
        for poly in me.polygons:
            for vi in poly.vertices:
                if mats[vi] and mats[vi] != poly.material_index + 1:
                    border[vi] = True
                mats[vi] = poly.material_index + 1
        wr = np.zeros(n)
        for zone in RZ.split(","):
            side_, zc_, hw_ = zone.split(":")
            zc_, hw_ = float(zc_), float(hw_)
            on = (P[:, 1] < cy) if side_ == "front" else (P[:, 1] > cy)
            wr = np.maximum(wr, np.where(on, np.exp(-0.5 * ((P[:, 2] - zc_) / hw_) ** 2), 0.0))
        wr[sl | small | border] = 0.0
        wr[wr < 0.02] = 0.0
        e2 = ed[~(small[ed[:, 0]] | small[ed[:, 1]])]
        deg = np.bincount(e2.ravel(), minlength=n).astype(float)
        a0, a1 = e2[:, 0], e2[:, 1]
        act = np.where(wr > 0)[0]
        for rnd in range(opt("--relax-rounds", 150, int)):
            acc = np.column_stack([np.bincount(a0, weights=P[a1, k], minlength=n) + np.bincount(a1, weights=P[a0, k], minlength=n)
                                   for k in range(3)])
            avg = acc / np.maximum(deg, 1)[:, None]
            P[act] = P[act] + (avg[act] - P[act]) * (0.5 * wr[act])[:, None]
            if rnd % 10 == 9:
                for i in act:
                    hit, nn, _f, _d = BVH.find_nearest(Vector(tuple(P[i])))
                    if hit is not None and (Vector(tuple(P[i])) - hit).dot(nn) < 0.004:
                        P[i] = np.array(tuple(hit + nn * 0.004))
        log.setdefault("relaxed", {})[label] = int(len(act))
    YO = opt("--yoke-over", 0.0)
    YM = opt("--yoke-mat", 1, int)
    if YO > 0:
        # THE YOKE KEPT OVER THE WOOL (its side edges read as torn, the wool coming through them in blotches): each
        # point of a yoke piece at least YO outside the wool's nearest surface, the lifts smoothed over the piece so
        # its two faces move together
        from mathutils.bvhtree import BVHTree
        wool_f = [pl for pl in me.polygons if pl.material_index != YM]
        wv = [tuple(obj.matrix_world @ me.vertices[i].co) for i in range(n)]
        WB = BVHTree.FromPolygons([tuple(P[i]) for i in range(n)], [tuple(pl.vertices) for pl in wool_f])
        yv = sorted({vi for pl in me.polygons if pl.material_index == YM for vi in pl.vertices})
        lift = np.zeros((n, 3))
        for i in yv:
            hit, nn, _f, dd = WB.find_nearest(Vector(tuple(P[i])))
            if hit is None or dd > 0.02:
                continue
            o_ = (Vector(tuple(P[i])) - hit).dot(nn)
            if o_ < YO:
                lift[i] = np.array(tuple(nn)) * (YO - o_)
        ymask = np.zeros(n, bool)
        ymask[yv] = True
        ey = ed[ymask[ed[:, 0]] & ymask[ed[:, 1]]]
        degy = np.bincount(ey.ravel(), minlength=n).astype(float)
        need_ = lift.copy()
        for _ in range(8):
            acc = np.column_stack([np.bincount(ey[:, 0], weights=lift[ey[:, 1], k], minlength=n) + np.bincount(ey[:, 1], weights=lift[ey[:, 0], k], minlength=n) for k in range(3)])
            avg = acc / np.maximum(degy, 1)[:, None]
            bigger = np.linalg.norm(avg, axis=1) > np.linalg.norm(need_, axis=1)
            lift = np.where((bigger & ymask)[:, None], 0.5 * (lift + avg), need_)
        P = P + lift
        log.setdefault("yokeLifted", {})[label] = int((np.linalg.norm(lift, axis=1) > 1e-4).sum())
    # nothing inside him
    inside = 0
    for i in range(n):
        hit, nn, _f, _d = BVH.find_nearest(Vector(tuple(P[i])))
        if hit is not None and (Vector(tuple(P[i])) - hit).dot(nn) < 0.004 and not small[i]:
            P[i] = np.array(tuple(hit + nn * 0.004))
            inside += 1
    Mi = obj.matrix_world.inverted()
    for i, v in enumerate(me.vertices):
        v.co = Mi @ Vector(tuple(P[i]))
    me.update()
    # the loose part for Unreal's cloth
    SB = opt("--sim-below", 0.0)
    if SB > 0:
        hem = float(P[:, 2].min())
        ca = me.color_attributes.get("SimMaxDistance") or me.color_attributes.new("SimMaxDistance", "FLOAT_COLOR", "POINT")
        for i in range(n):
            t = 0.0 if sl[i] else max(0.0, min(1.0, (SB - P[i, 2]) / max(1e-6, SB - hem)))
            ca.data[i].color = (t, t, t, 1.0)
    say(label, {"points": n, "sleeve": int(sl.sum()), "small": int(small.sum()), "room": moved_room, "pressed": moved_press,
                "keptOut": inside})
    return {"points": n, "room": moved_room, "pressed": moved_press, "keptOut": inside}


log["render"] = ease(g, "render")
if sim is not None:
    log["sim"] = ease(sim, "sim")
log["room"] = {"mm": opt("--room", 0.0), "lo": opt("--room-lo", 0.85), "hi": opt("--room-hi", 1.25)}
log["press"] = {"lo": opt("--press-lo", 0.0), "hi": opt("--press-hi", 0.0)}
log["simBelow"] = {"z": opt("--sim-below", 0.0), "maxM": opt("--sim-max", 0.08)}
log["uv"] = [u.name for u in g.data.uv_layers]

for o in list(bpy.data.objects):
    if o.type == "MESH" and o not in (g, sim, body):
        o.hide_render = True
if sim is not None:
    sim.hide_render = True
body.hide_render = False
tailor.pictures(os.path.join(OUT, "eased"), Vector((0, 0, 1.25)), views=(("front", (0, -2.6, 0.1)), ("side", (2.6, 0, 0.1)),
                                                                         ("back", (0, 2.6, 0.1)), ("three-quarter", (1.8, -1.9, 0.3))),
                res=(700, 800))
tailor.pictures(os.path.join(OUT, "eased-close"), Vector((0, 0, 1.30)), views=(("front", (0, -1.2, 0.05)), ("three-quarter", (0.85, -0.85, 0.1)),
                                                                               ("back", (0, 1.2, 0.05))), res=(700, 700))
for o, suffix in ((g, "render"), (sim, "sim")):
    if o is None:
        continue
    bpy.ops.object.select_all(action="DESELECT")
    o.hide_set(False)
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, "%s_%s_static.fbx" % (NAME, suffix)), use_selection=True,
                             object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False, colors_type="LINEAR")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + ".blend"))
json.dump(log, open(os.path.join(OUT, "ease.json"), "w"), indent=1)
say("done", json.dumps(log))
