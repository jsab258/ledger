"""Work trousers sewn from a FreeSewing pattern (Titan or Charlie) round a MetaHuman body in its rest pose.

    blender -b -P tools/meshgen/blender/sew_trousers.py -- PATTERN.json BODY.fbx OUT_DIR [--edge 12] [--place-only]

WHY, 29 September (the clothing session, CLOTHES.md item 4: proper work
trousers). The jacket's method (sew_donkey.py), without its hardest part:
the legs hang in the body's own rest pose, so nothing is posed and lowered.
The four pieces (front and back of each leg) are cut from the pattern, laid
round the body at their pattern heights, sewn weightless with unlimited
sewing force, welded, given the pattern's own lengths as their rest shape,
and settled under the cloth's true weight with the waist held where a belt
holds it.

THE LAYING OUT. Each row of the pattern (a height below the waist) is laid
along the body's section at that height, round the axis of that side (the
middle of the left half above the crotch, of the left leg below it): the
front from the front's middle line (above the fork, where the fly is) or the
inside of the leg (below it) round to the side seam, the back likewise, each
point as far along the section as it lies from the crotch or inside seam on
the pattern, and the whole row set out from the body by the ease that makes
its length the pattern's width. The crotch seams lie on the body's middle
line: each point of a crotch curve goes as far down the body's profile, front
or back, as it lies along the curve from the waist, so the fork lands under
the crotch where the front and back meet.

THE THIGHS PARTED (tailor.part_thighs): Ron's touch for 8 cm below his
crotch; the collider has them 16 mm apart there so the cloth fits between.
"""
import json
import math
import os
import sys
import time

import bpy
import numpy as np
from mathutils import Vector

sys.path.insert(0, os.path.dirname(__file__))
import tailor  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
SRC, BODY, OUT = argv[0], argv[1], argv[2]
os.makedirs(OUT, exist_ok=True)


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


EDGE = opt("--edge", 12.0)                   # cloth triangle edge while draping, mm
SEW_FRAMES = opt("--sew", 40, int)
DROP_FRAMES = opt("--drop", 80, int)
DENSITY = opt("--density", 0.28)             # kg per square metre: a work-trouser twill
MIN_CLEAR = opt("--min-clear", 0.004)
MAX_CLEAR = opt("--max-clear", 0.07)
HOLD_MM = opt("--hold", 30.0)                # the waist held this far down from its edge, mm
NAME = opt("--name", "ron_trousers", str)
PLACE_ONLY = "--place-only" in argv
T0 = time.time()
log = {"pattern": SRC, "body": BODY, "edge": EDGE, "density": DENSITY}


def say(*a):
    print("TROUSERS", *a, flush=True)


# ---- the pattern's pieces ---------------------------------------------------------------

pat = json.load(open(SRC))
parts = pat["parts"]
fk = next(k for k in parts if k.endswith(".front"))
bk = next(k for k in parts if k.endswith(".back"))
L = tailor.length


def outline(part):
    P = parts[part]["points"]
    poly = tailor.closed(parts[part]["paths"]["seam"]["points"])
    wi, wo = P["styleWaistIn"], P["styleWaistOut"]
    fork, hi, ho = P["fork"], P["floorIn"], P["floorOut"]
    return {"waist": tailor.seg(poly, wo, wi), "crotch": tailor.seg(poly, wi, fork),
            "inseam": tailor.seg(poly, fork, hi), "hem": tailor.seg(poly, hi, ho), "outseam": tailor.seg(poly, ho, wo)}


FO, BO = outline(fk), outline(bk)
N = {}
for s in ("outseam", "inseam"):
    N[s] = max(2, round(max(L(FO[s]), L(BO[s])) / EDGE))
for s in ("waist", "crotch", "hem"):
    N["F" + s] = max(2, round(L(FO[s]) / EDGE))
    N["B" + s] = max(2, round(L(BO[s]) / EDGE))
ORDER = ("waist", "crotch", "inseam", "hem", "outseam")


def piece(O, pre):
    segs = [(s, O[s], N[s] if s in ("outseam", "inseam") else N[pre + s]) for s in ORDER]
    pts, idx = tailor.loop(segs)
    flat, faces = tailor.panel(pts, EDGE)
    return flat, faces, idx


F_flat, F_faces, F_idx = piece(FO, "F")
B_flat, B_faces, B_idx = piece(BO, "B")
log["pattern"] = {"lengthsMm": {p + s: round(L(O[s])) for p, O in (("F", FO), ("B", BO)) for s in ORDER}}
say("pattern", json.dumps(log["pattern"]))


def side_fn(poly_list):
    """x as a function of y along a pattern line (y made increasing)."""
    pts = np.array([p for poly in poly_list for p in poly])
    order = np.argsort(pts[:, 1], kind="stable")
    ys, xs = pts[order, 1], pts[order, 0]
    return lambda y: float(np.interp(y, ys, xs))


def crotch_arc(O):
    """Along the crotch curve from the waist: (y, arc length mm) pairs, and the fork's arc."""
    c = O["crotch"]
    s = np.concatenate([[0.0], np.cumsum([math.dist(c[k], c[k - 1]) for k in range(1, len(c))])])
    ys = np.maximum.accumulate(np.array([p[1] for p in c]))
    return ys, s


# the side (outseam, then the waist line above its top) and the middle (crotch, then inseam)
F_side = side_fn([FO["outseam"], FO["waist"]])
B_side = side_fn([BO["outseam"], BO["waist"]])
F_mid = side_fn([FO["crotch"], FO["inseam"]])
B_mid = side_fn([BO["crotch"], BO["inseam"]])
F_cy, F_cs = crotch_arc(FO)
B_cy, B_cs = crotch_arc(BO)
F_fork_y, B_fork_y = parts[fk]["points"]["fork"][1], parts[bk]["points"]["fork"][1]
F_top_y, B_top_y = min(p[1] for p in FO["waist"]), min(p[1] for p in BO["waist"])
F_side_top, B_side_top = parts[fk]["points"]["styleWaistOut"][1], parts[bk]["points"]["styleWaistOut"][1]
BOTTOM_Y = max(p[1] for p in FO["hem"] + BO["hem"])

# ---- the body, its thighs parted ------------------------------------------------------

arm, body = tailor.load_body(BODY, lod=opt("--lod", 1, int))
log["thighsParted"] = tailor.part_thighs(body, apart=opt("--apart", 0.008))
bpy.context.view_layer.update()
_ev = tailor.evaluated_copy(body, "BodyParted")
BVH = tailor.bvh_of(_ev)
meas = json.load(open(opt("--measure", os.path.join(os.path.dirname(BODY), "measurements.json"), str)))
Z_W = meas["heights_m"]["waist"] + opt("--waist-shift", 0.0)
Z_CROTCH = meas["heights_m"]["crotch"]


def resample_line(p, step=0.004):
    d = np.linalg.norm(np.diff(p, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(d)])
    if s[-1] < step:
        return p
    t = np.arange(0.0, s[-1], step)
    return np.stack([np.interp(t, s, p[:, k]) for k in range(3)], axis=1)


# the axis of the left side at each height: the middle of the body's section there, left of the middle line
AX_Z = np.arange(-0.02, Z_W + 0.12, 0.01)
AX = []
for z in AX_Z:
    pts = [resample_line(lp) for lp in tailor.section_loops(_ev, (0, 0, max(0.005, z)), (0, 0, 1))]
    pts = np.concatenate(pts) if pts else np.zeros((0, 3))
    pts = pts[(pts[:, 0] > 0.002) & (pts[:, 0] < 0.26)]
    AX.append(pts[:, :2].mean(axis=0) if len(pts) else (AX[-1] if AX else np.array([0.12, 0.0])))
AX = np.array(AX)
for _ in range(3):                                     # smoothed up and down
    AX[1:-1] = 0.25 * AX[:-2] + 0.5 * AX[1:-1] + 0.25 * AX[2:]


def axis(z):
    return Vector((float(np.interp(z, AX_Z, AX[:, 0])), float(np.interp(z, AX_Z, AX[:, 1])), z))


# the body's middle line, front and back, from the crotch up (the profile in the plane x = 0)
_loop = max(tailor.section_loops(_ev, (0, 0, 0), (1, 0, 0)), key=len)     # in order along the line
prof = _loop[(_loop[:, 2] > Z_CROTCH - 0.05) & (_loop[:, 2] < Z_W + 0.15)]
# WHERE THE FRONT AND BACK CROTCH SEAMS MEET (29 September, the second laying
# out): Ron's crotch is a flat stretch 20 cm long; its lowest point lay 5 cm in
# front of his legs' middle, and the back seam was laid along the whole of it.
# The fork goes under the middle of the legs, as an inside leg seam runs.
_bottom = prof[(prof[:, 2] < Z_CROTCH + 0.025) & (np.abs(prof[:, 1]) < 0.3)]
_legs_y = float(np.interp(Z_CROTCH - 0.03, AX_Z, AX[:, 1]))
CROTCH_PT = Vector(_bottom[int(np.argmin(np.abs(_bottom[:, 1] - _legs_y)))])


def _chain(step):
    """Along the middle line from the crotch point up to above the waist, then turned to run top down."""
    i = int(np.argmin(np.linalg.norm(_loop - np.array(CROTCH_PT), axis=1)))
    out = [np.array(CROTCH_PT)]
    for _ in range(len(_loop)):
        i = (i + step) % len(_loop)
        out.append(_loop[i])
        if _loop[i][2] > Z_W + 0.12:
            break
    return resample_line(np.array(out[::-1]), 0.003)


_c1, _c2 = _chain(1), _chain(-1)
if _c1[:, 1].mean() < _c2[:, 1].mean():
    PF, PB = _c1, _c2
else:
    PF, PB = _c2, _c1





def arc_of(line):
    return np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))])


PF_s, PB_s = arc_of(PF), arc_of(PB)


def at_height(line, z):
    k = int(np.argmin(np.abs(line[:, 2] - z)))
    return Vector(line[k])


def first_below(line, z):
    """Walking down the middle line from the top, the first point at or below height z."""
    k = int(np.argmax(line[:, 2] <= z)) if (line[:, 2] <= z).any() else len(line) - 1
    return Vector(line[k])


def at_arc(line, s_arr, s):
    return Vector([float(np.interp(s, s_arr, line[:, k])) for k in range(3)])


def middle_end(front, y):
    """Where the row at pattern height y ends at the middle: on the profile (above the fork), else inside the leg."""
    fork_y, cy, cs, line, ls, top_y = ((F_fork_y, F_cy, F_cs, PF, PF_s, F_top_y) if front else
                                       (B_fork_y, B_cy, B_cs, PB, PB_s, B_top_y))
    z = Z_W - y / 1000.0
    if y >= fork_y:
        return None, z                                   # below the fork: the inside of the leg, found by the sweep
    if y < top_y:
        return at_height(line, z), z                     # above this piece: the middle line at the row's height
    # down the profile as far as along the crotch curve, the waist-top matched to the profile at its own height
    s_pat = float(np.interp(y, cy, cs)) / 1000.0
    top = at_height(line, Z_W - top_y / 1000.0)
    s0 = float(ls[int(np.argmin(np.linalg.norm(line - np.array(top), axis=1)))])
    lam = (ls[-1] - s0) / max(1e-6, cs[-1] / 1000.0)     # the curve's length fitted to the profile's
    return at_arc(line, ls, s0 + s_pat * lam), z


def cast(origin, theta, z):
    d = Vector((math.cos(theta), math.sin(theta), 0.0))
    o = Vector((origin.x, origin.y, z))
    hit, _n, _f, dist = BVH.ray_cast(o, d, 0.6)
    return (hit, d) if hit is not None else (o + d * 0.1, d)


def profile_path(line, ls, a, b, clear):
    """The body's middle line between two of its points (a to b, in that order), set out by `clear` in its plane."""
    sa = float(ls[int(np.argmin(np.linalg.norm(line - np.array(a), axis=1)))])
    sb = float(ls[int(np.argmin(np.linalg.norm(line - np.array(b), axis=1)))])
    if abs(sb - sa) < 1e-4:
        return np.zeros((0, 3))
    ss = np.linspace(sa, sb, max(2, int(abs(sb - sa) / 0.006) + 1))
    out = []
    for s_ in ss:
        q = at_arc(line, ls, s_)
        _h, nrm, _f, _d = BVH.find_nearest(q)
        n2 = Vector((0.0, nrm.y, nrm.z))
        n2 = n2.normalized() if n2.length > 1e-6 else Vector((0, 0, -1))
        out.append(np.array(q + n2 * clear))
    return np.array(out)


def row_curve(y, clear):
    """The left side at the row's height, set out by `clear`: from the front's crotch point up or down the body's
    middle line to the row's height, round the side, and down or up the back's middle line to its crotch point;
    below the fork, round the leg."""
    mf, _zf = middle_end(True, y)
    mb, _zb = middle_end(False, y)
    z = Z_W - y / 1000.0
    A = axis(z)
    # the middle line at the row's own height, where the sweep round the side starts and ends
    # below the crotch the section is two legs: the sweep goes round the leg from its inside, and the crotch
    # point (still above the fork) is joined to that by a short straight run
    below = z < CROTCH_PT.z
    pf = None if (mf is None or below) else first_below(PF, z)
    pb = None if (mb is None or below) else first_below(PB, z)
    tf = -math.pi if pf is None else math.atan2(pf.y - A.y, pf.x - A.x)
    tb = math.pi if pb is None else math.atan2(pb.y - A.y, pb.x - A.x)
    if tf > 0:
        tf -= 2 * math.pi                                # the front goes round through negative angles
    if tb < 0:
        tb += 2 * math.pi
    us = np.linspace(0.0, 1.0, 97)
    pts = []
    for u in us:
        th = tf + u * (tb - tf)
        hit, d = cast(A, th, z)
        p = hit + d * clear
        if p.x < 0.004:                                  # never past the middle line
            p.x = 0.004 if (pf is None and pb is None) or (0.05 < u < 0.95) else 0.0
        pts.append(np.array(p))
    pts = np.array(pts)
    # CLOTH BRIDGES HOLLOWS (29 September, the first laying out): each point
    # of the sweep goes out along its ray to the row's hull
    hull = np.array(tailor._hull2(pts[:, :2]))
    if len(hull) >= 3:
        a2 = np.array([A.x, A.y])
        for i in range(1, len(pts) - 1):
            d = pts[i, :2] - a2
            t0 = float(np.linalg.norm(d))
            if t0 < 1e-6:
                continue
            d /= t0
            best = t0
            for k in range(len(hull)):
                q0, q1 = hull[k], hull[(k + 1) % len(hull)]
                e = q1 - q0
                den = d[0] * (-e[1]) + d[1] * e[0]
                if abs(den) < 1e-12:
                    continue
                w = q0 - a2
                t = (w[0] * (-e[1]) + w[1] * e[0]) / den
                u = (d[0] * w[1] - d[1] * w[0]) / den
                if t > best and -1e-9 <= u <= 1 + 1e-9:
                    best = t
            pts[i, :2] = a2 + d * best
    # THE CROTCH SEAMS FOLLOW THE BODY'S MIDDLE LINE (29 September, the second
    # laying out: swept round by angle, a row just above the fork ran along the
    # middle plane through the body to reach its crotch point)
    parts_ = []
    if mf is not None and pf is not None:
        parts_.append(profile_path(PF, PF_s, mf, pf, clear))
    elif mf is not None:
        parts_.append(np.linspace(np.array(mf), pts[0], 6)[:-1])
    parts_.append(pts)
    if mb is not None and pb is not None:
        parts_.append(profile_path(PB, PB_s, pb, mb, clear))
    elif mb is not None:
        parts_.append(np.linspace(pts[-1], np.array(mb), 6)[1:])
    return np.concatenate([q for q in parts_ if len(q)])


def curve_len(c):
    return float(np.linalg.norm(np.diff(c, axis=0), axis=1).sum())


ANKLE_Z = opt("--ankle", 0.14)


def foot_row(z, want):
    """Below the ankle a row is a circle of the pattern's own width round the ankle's middle, what lies inside
    the foot lifted onto its top: the hem falls over the foot, as it does over a boot.

    WHY, 29 September (run 5): laid round the section at the hem's height, the
    rows wrapped the whole foot, stretched sixteen times, and the legs rode up
    the calves as the seams pulled them in."""
    A = axis(ANKLE_Z)
    R = want / (2 * math.pi)
    pts = []
    for th in np.linspace(-math.pi, math.pi, 97):
        p = Vector((A.x + R * math.cos(th), A.y + R * math.sin(th), z))
        if tailor.depth_inside(BVH, p) > 0.0:
            hit, _n, _f, _d = BVH.ray_cast(p, Vector((0, 0, 1)), 0.4)
            if hit is not None:
                p = hit + Vector((0, 0, 0.006))
        pts.append(np.array(p))
    return np.array(pts)


def row(y):
    """The row's curve with the ease that makes it the pattern's width, and the front's and back's widths (m)."""
    wf = (F_mid(y) - F_side(y)) / 1000.0 if F_top_y <= y <= BOTTOM_Y else 0.0
    wb = (B_side(y) - B_mid(y)) / 1000.0 if B_top_y <= y <= BOTTOM_Y else 0.0
    want = abs(wf) + abs(wb)
    z = Z_W - y / 1000.0
    if z < ANKLE_Z:
        return foot_row(z, want), abs(wf), abs(wb), 0.0
    lo, hi = MIN_CLEAR, MAX_CLEAR
    c_lo = row_curve(y, lo)
    if curve_len(c_lo) >= want:
        return c_lo, abs(wf), abs(wb), lo
    c_hi = row_curve(y, hi)
    if curve_len(c_hi) <= want:
        return c_hi, abs(wf), abs(wb), hi
    for _ in range(8):                                   # halving: length grows with the ease
        mid = 0.5 * (lo + hi)
        if curve_len(row_curve(y, mid)) < want:
            lo = mid
        else:
            hi = mid
    c = 0.5 * (lo + hi)
    return row_curve(y, c), abs(wf), abs(wb), c


if "--debug-row" in argv:
    y = opt("--debug-row", 218.0)
    wf, wb = F_mid(y) - F_side(y), B_side(y) - B_mid(y)
    say("debug row", y, "wf", round(wf), "wb", round(wb), "ends", middle_end(True, y), middle_end(False, y))
    for c in (0.004, 0.01, 0.02, 0.03, 0.05, 0.07):
        cv = row_curve(y, c)
        np.save(os.path.join(OUT, "row-%d-%d.npy" % (int(y), int(c * 1000))), cv)
        if c == 0.004:
            for zz in (Z_W - y / 1000.0,):
                secs = tailor.section_loops(_ev, (0, 0, zz), (0, 0, 1))
                np.save(os.path.join(OUT, "sec-%d.npy" % int(y)), np.concatenate([np.vstack([q, [[np.nan] * 3]]) for q in secs]))
            np.save(os.path.join(OUT, "prof.npy"), prof)
        say("  clear %.3f length %.0f mm; x<0.005 at %d of %d; first %s last %s" % (c, curve_len(cv) * 1000, int((cv[:, 0] < 0.005).sum()), len(cv),
            np.round(cv[0], 3).tolist(), np.round(cv[-1], 3).tolist()))
ROW_Y = np.arange(min(F_top_y, B_top_y), BOTTOM_Y + 5.0, 5.0)
ROWS = [row(float(y)) for y in ROW_Y]
log["ease"] = {"mm": [round(r[3] * 1000, 1) for r in ROWS[::20]], "atRowsEveryMm": 100}
say("rows laid", len(ROWS), "ease every 100 mm (mm):", log["ease"]["mm"], "%.1f min" % ((time.time() - T0) / 60))


def along(curve, s, from_front):
    """The point `s` metres along the row curve from its front end (or back end)."""
    c = curve if from_front else curve[::-1]
    a = arc_of(c)
    k = min(1.0, a[-1] / max(1e-6, s)) if s > a[-1] else 1.0
    return np.array([np.interp(s * k, a, c[:, j]) for j in range(3)])


def place(flat, front):
    """Each pattern point on its row, as far from the middle end as it lies from the crotch or inseam."""
    mid, side = (F_mid, F_side) if front else (B_mid, B_side)
    out = []
    for x, y in flat:
        k = int(np.clip(np.searchsorted(ROW_Y, y), 1, len(ROW_Y) - 1))
        y0, y1 = ROW_Y[k - 1], ROW_Y[k]
        t = float(np.clip((y - y0) / (y1 - y0), 0, 1))
        ps = []
        for r in (ROWS[k - 1], ROWS[k]):
            curve, wf, wb, _c = r
            span = wf + wb
            # a full row (both pieces reach the side seam) fills its line exactly,
            # stretched a little where the body's line is longer than the pattern
            # (the cloth bridges the hollow once it has its own lengths); a row
            # above a side seam's top leaves the side open, as the waist dips there
            full = y >= max(F_side_top, B_side_top)
            scale = curve_len(curve) / max(1e-6, span) if full else min(1.0, curve_len(curve) / max(1e-6, span))
            d = abs(mid(y) - x) / 1000.0 * scale
            ps.append(along(curve, d, from_front=front))
        out.append(tuple(ps[0] * (1 - t) + ps[1] * t))
    return out


def mirror(pts):
    return [(-p[0], p[1], p[2]) for p in pts]


F_place = place(F_flat, True)
B_place = place(B_flat, False)
G = tailor.Garment()
AT = {}
AT["FL"] = G.add("front_l", F_flat, F_faces, F_place, layout=(-0.3, 0.0))
AT["BL"] = G.add("back_l", B_flat, B_faces, B_place, layout=(0.9, 0.0))
AT["FR"] = G.add("front_r", F_flat, F_faces, mirror(F_place), layout=(-0.8, 0.0), mirror=True)
AT["BR"] = G.add("back_r", B_flat, B_faces, mirror(B_place), layout=(1.4, 0.0), mirror=True)


def ids(p, idx, s):
    return [AT[p][k] for k in idx[s]]


for sd in ("L", "R"):
    G.seam("outseam", ids("F" + sd, F_idx, "outseam"), ids("B" + sd, B_idx, "outseam"))
    G.seam("inseam", ids("F" + sd, F_idx, "inseam"), ids("B" + sd, B_idx, "inseam"))
G.seam("front crotch", ids("FL", F_idx, "crotch"), ids("FR", F_idx, "crotch"))
G.seam("back crotch", ids("BL", B_idx, "crotch"), ids("BR", B_idx, "crotch"))

# nothing starts inside the body
pushed = 0
for i, c in enumerate(G.verts):
    v = Vector(c)
    if tailor.depth_inside(BVH, v) > 0.0 or BVH.find_nearest(v)[3] < 0.002:
        hit, nrm, _f, _d = BVH.find_nearest(v)
        G.verts[i] = tuple(hit + nrm * 0.004)
        pushed += 1
for i in range(len(G.verts)):                          # the pieces remember where they were laid while sewn
    G.rest[i] = G.verts[i]
trousers = G.build("Trousers")
co0 = tailor.coords(trousers, evaluated=False)
log["place"] = {"points": len(G.verts), "triangles": len(G.faces), "pushedOut": pushed,
                "seamGapsMm": tailor.seam_gaps(co0, G.seams), "strainVsPattern": tailor.strain(trousers, co0, G.groups, G.flat),
                "worstEdges": tailor.worst_edges(trousers, co0, G.flat, G.piece_of)}
say("placed", json.dumps(log["place"]))

twill = tailor.material("M_TrouserTwill", (0.075, 0.075, 0.08), 0.9)
trousers.data.materials.append(twill)
grey = tailor.material("M_Body", (0.5, 0.5, 0.5))
body.data.materials.append(grey)
bpy.data.objects.remove(_ev, do_unlink=True)
MID = Vector((0.0, -0.02, 0.62))
VIEWS = (("front", (0, -3.6, 0.0)), ("side", (3.6, 0, 0.0)), ("back", (0, 3.6, 0.0)), ("three-quarter", (2.5, -2.6, 0.2)))
tailor.pictures(os.path.join(OUT, "place"), MID, views=VIEWS)
if PLACE_ONLY:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "place.blend"))
    json.dump(log, open(os.path.join(OUT, "trousers.json"), "w"), indent=1)
    say("placed only, %.1f min" % ((time.time() - T0) / 60))
    sys.exit(0)

# ---- 1. sewn, weightless ---------------------------------------------------------------------

# THE WAIST HELD WHERE THE BELT HOLDS IT, FROM THE START (29 September, run 4:
# weightless and slippery, squeezed by the sewing, the trousers slid down the
# cones of the hips and thighs to the knees and crumpled there): points within HOLD_MM of the waist's edge on the flat pattern
me = trousers.data
uv = me.uv_layers["pattern"]
vuv = {lp.vertex_index: tuple(uv.data[lp.index].uv) for lp in me.loops}
held = trousers.vertex_groups.new(name="held")
waist_uv = []
for pname, flat, O, lay, mir in (("front_l", F_flat, FO, (-0.3, 0.0), False), ("back_l", B_flat, BO, (0.9, 0.0), False),
                                  ("front_r", F_flat, FO, (-0.8, 0.0), True), ("back_r", B_flat, BO, (1.4, 0.0), True)):
    sx = -1.0 if mir else 1.0
    waist_uv.append(np.array([(lay[0] + sx * x / 1000.0, lay[1] - y / 1000.0) for x, y in tailor.resample(O["waist"], 60)]))
waist_uv = np.concatenate(waist_uv)
n_held = 0
for i, (u, v) in vuv.items():
    d = float(np.min(np.hypot(waist_uv[:, 0] - u, waist_uv[:, 1] - v))) * 1000.0
    if d < HOLD_MM:
        held.add([i], 1.0 if d < HOLD_MM * 0.6 else 0.6, "REPLACE")
        n_held += 1
log["place"]["held"] = n_held

scn = bpy.context.scene
CL = dict(tension=opt("--tension", 30.0), compression=opt("--compression", 30.0), shear=opt("--shear", 10.0))
tailor.collider(body, friction=opt("--friction", 10.0))

# ---- 1. sewn by projection (tailor.relax), the waist held -------------------------------------

trousers.shape_key_clear()
pin_ids = [i for i in range(len(trousers.data.vertices))
           if any(g.group == held.index and g.weight >= 0.99 for g in trousers.data.vertices[i].groups)]
gap, edges_ = tailor.relax(trousers, G.sewing, pin_ids, BVH, iterations=opt("--relax", 300, int), clear=0.004, report=say,
                           bend=opt("--bend", 0.0))
co = tailor.coords(trousers, evaluated=False)
log["stitch"] = {"by": "projection", "widestGapMm": gap, "seamGapsMm": tailor.seam_gaps(co, G.seams), "edgesVsPattern": edges_,
                 "strainVsPattern": tailor.strain(trousers, co, G.groups, G.flat),
                 "worstEdges": tailor.worst_edges(trousers, co, G.flat, G.piece_of),
                 "inside": tailor.inside_count(BVH, co, range(len(co))), "minutes": round((time.time() - T0) / 60, 1)}
say("stitched", json.dumps(log["stitch"]))
tailor.pictures(os.path.join(OUT, "stitched"), MID, views=VIEWS[:1] + VIEWS[3:])

# ---- 2. welded, the pattern's lengths, settled at the cloth's weight with the waist held ---------------

body.collision.cloth_friction = opt("--friction", 10.0)
_ev = tailor.evaluated_copy(body, "BodyParted")
BVH = tailor.bvh_of(_ev)
bpy.data.objects.remove(_ev, do_unlink=True)
merged = tailor.weld(trousers, G.sewing, co)
out_ = tailor.push_out(trousers, BVH, 0.003)
log["weld"] = {"pairsMerged": merged, "of": len(G.sewing), "points": len(trousers.data.vertices), "pushedOut": out_}
say("welded", log["weld"])
# settled by projection too: a small step down each round, the pattern's lengths and the body taking it back
pin_ids = [i for i in range(len(trousers.data.vertices))
           if any(g.group == held.index and g.weight >= 0.99 for g in trousers.data.vertices[i].groups)]
gap, edges_ = tailor.relax(trousers, [], pin_ids, BVH, iterations=opt("--settle", 200, int), clear=0.004, report=say,
                           gravity=opt("--gravity", 0.0004), length_rounds=opt("--length-rounds", 4, int),
                           bend=opt("--bend", 0.0))
log["settle"] = {"by": "projection", "edgesVsPattern": edges_}
say("settled by projection", edges_)
press_ = tailor.press(trousers, BVH, rounds=opt("--press", 30, int), smooth=opt("--smooth", 0.25), lengths=10)
log["press"] = press_
say("pressed", press_)
# twill spans the seat's cleft and the hollows below the buttocks (the first blind review), and the hem is a
# clean edge
log["bridged"] = tailor.bridge_slices(trousers, Z_CROTCH - 0.20, Z_W - 0.03, Z_CROTCH, deepest=opt("--bridge", 0.04))
log["hemSmoothed"] = tailor.smooth_edges_of(trousers, 0.2)
say("bridged", log["bridged"], "hem points smoothed", log["hemSmoothed"])
co = tailor.coords(trousers, evaluated=False)
trousers.vertex_groups.clear()

# ---- the checks, the pictures, the file ---------------------------------------------------------------

near = [BVH.find_nearest(Vector(p)) for p in co]
clear_mm = sorted(n[3] * 1000.0 for n in near if n[0] is not None)
hem_z = float(co[:, 2].min())
log["rest"] = {"inside": tailor.inside_count(BVH, co, range(len(co))),
                 "clearanceMm": {"p05": round(clear_mm[len(clear_mm) // 20], 1), "median": round(clear_mm[len(clear_mm) // 2], 1),
                                 "p95": round(clear_mm[len(clear_mm) * 19 // 20], 1)},
                 "hemLowestM": round(hem_z, 3), "waistTopM": round(float(co[:, 2].max()), 3),
                 "minutes": round((time.time() - T0) / 60, 1)}
say("rest", json.dumps(log["rest"]))
for p in trousers.data.polygons:
    p.use_smooth = True
tailor.pictures(os.path.join(OUT, "trousers"), MID, views=VIEWS)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "trousers.blend"))
json.dump(log, open(os.path.join(OUT, "trousers.json"), "w"), indent=1)
say("done, %.1f min" % ((time.time() - T0) / 60))
