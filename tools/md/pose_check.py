"""A skinned garment tried in Kiln's test poses on its wearer's skeleton, without Blender: Kiln M5 step 3
(KILN-M5-RIGGING-METHOD-2026-11-17.md section 4, checks 2 to 4). Per pose: body points through the cloth and cloth
points inside the body (over 3 mm), and the cloth's stretch; sitting, the shape check beside the counts.

    python tools/md/pose_check.py GARMENT_skinned.fbx WEIGHTS_BODY.fbx OUT.json
        [--poses rest,walk,sit,arms up] [--shape-bars REFERENCE.json] [--name NAME]
    python tools/md/pose_check.py --selftest

WHY, 17 November 2026. The method note's check 2 asks, per pose, for body through cloth, cloth inside body and the
worst stretch; pose_skinned.py (Blender) counts only cloth inside, and the note names Kiln's test poses for body
through cloth. Its check 3 sets the tool bar: Kiln's parity bar, at most 299 body points through and 44 cloth points
inside over 3 mm in every test pose (MECHANICS.md "Pass/fail" items 1, 2 and 8). It is M5's offline bar only; the
packaged film's RUBRIC lines 9 to 11 decide ("nothing passes through"). Its check 4 adds, sitting on the heavy body,
the gap from the seat and thighs to the cloth over them and the hem's height and shape against rest, because a count
once fell from 328 to 10 while the hem still ballooned; those bars are taken from Tom's passed jeans in the same
pose (--shape-bars: a report of this tool on them). This is Kiln's own measure, ported so the skinned FBX that
skin_transfer.py (step 2) writes is judged by the numbers Kiln's bar was set on, in seconds, beside other jobs.

HOW (Kiln: F:/LedgerTools/tool-dev/kiln/src/fit.rs pose_mats, job.rs test poses, through_idx, count_inside,
bvh.rs outward_signs, rim_points, hit_on_rim, inside_parity; read 17 Nov 2026).
- Poses: per bone a turn about its own bind joint in the body's axes (Blender's frame, the same as Kiln's working
  frame: metres, z up, facing -y), each bone carrying its parent's move (move = parent's move x own turn). Walk: thigh
  l -28 and r +18 about x, calf l +12 and r +40, upper arm l +18 and r -22, both forearms -20. Sit: both thighs -88,
  both calves +88, spine_03 -6, both upper arms -25, both forearms -40. Arms up: upper arm l -95 and r +95 about y,
  clavicle l -12 and r +12 about y, both forearms -15 about x. "rest" is the bind pose.
- Body and garment ride the same moves by their own skin weights (linear blend, each point's weights normalised;
  a point with none stays put).
- Body through cloth over 3 mm: body points within the posed garment's height whose nearest cloth (within 40 mm)
  they lie more than 3 mm outside of, by that cloth face's outward side; left out when that nearest point is on an
  open edge, or within 15 mm of an open edge or a rim point (Kiln's opening_skip_mm). Outward sides: each cloth face
  against the body's surface nearest its middle; one side for the whole garment unless 3% or more of the faces
  disagree, then a side per face (rim points are where the two sides meet). Kiln finds the sides afresh in each pose
  ("throughKilnPoseSides"); a pose that folds 3% of the faces over (Ron's jeans sitting, 3.1%) then switches to a
  side per face and its new rim points hide body points from the count (131 of Ron's seat points). A face's outward
  side belongs to the garment, so the count is also made with the rest pose's sides ("throughRestSides"), and the
  larger of the two is the pose's count and goes to the bar.
- Cloth inside body over 3 mm: cloth points over 3 mm from the posed body and inside it by Kiln's parity (8
  horizontal rays, inside when 5 or more cross the body an odd number of times).
- Stretch: every polygon edge over 0.5 mm at rest, posed length over rest length; edges over 1.2x counted, the worst
  given.
- Where: through points by the body point's main bone (trunk, head, each side's thigh, calf, foot, arm) and front or
  back of the pelvis at rest; "throughCoveredAtRest" counts those the cloth covered at rest (a hand resting outside
  the lap, or a toe beyond a hem, is through by Kiln's measure but was never under the cloth). Cloth inside and
  stretched edges by the cloth point's main bone ("insideByArea", "stretchedByArea"), and where the worst edge lies.
- Sitting shape: seat and thighs are the body points whose main bone is a thigh (or the pelvis, below its joint)
  and that the cloth covers at rest; their gap to the posed cloth (median and 90th percentile, mm) and how many are
  through. Hems are the open loops below the knees: each taken back through its leg's calf move and compared with
  rest (the rise up the shin, the worst change of shape, height range and back-minus-front drop).
- Bars: tool bar 299/44 in every pose listed (rest included, as Kiln's items 1 and 2). Shape bars, when a reference
  report is given: the reference's sitting gap p90 and worst hem shape change, each plus 10% plus 1 mm (Kiln's band
  tolerance with a floor so a reference of 0 does not demand 0: inferred, not a published number). Without a
  reference the shape check is measured and its pass left null (U until measured on Tom's jeans).
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import bend_back  # noqa: E402
import fbx_skin  # noqa: E402

LIMIT = 0.003           # over 3 mm
REACH = 0.04            # nearest cloth looked for within 40 mm (Kiln's cloth.nearest(p, 0.04))
SKIP = 0.015            # Kiln's opening_skip_mm default, 15 mm
STRETCH = 1.2
MIN_EDGE = 5e-4
FLIP_SHARE = 0.03
BAR_THROUGH = 299
BAR_INSIDE = 44
SHAPE_TOL = 0.10
SHAPE_FLOOR_MM = 1.0
NEAREST_K = 16
POSE_ORDER = ["rest", "walk", "sit", "arms up"]

# Kiln's fit.rs pose_mats, as written there (axis, degrees)
KILN_POSES = {
    "rest": {},
    "arms up": {"upperarm_l": ("y", -95.0), "upperarm_r": ("y", 95.0), "clavicle_l": ("y", -12.0),
                "clavicle_r": ("y", 12.0), "lowerarm_l": ("x", -15.0), "lowerarm_r": ("x", -15.0)},
    "walk": {"thigh_l": ("x", -28.0), "thigh_r": ("x", 18.0), "calf_l": ("x", 12.0), "calf_r": ("x", 40.0),
             "upperarm_l": ("x", 18.0), "upperarm_r": ("x", -22.0), "lowerarm_l": ("x", -20.0), "lowerarm_r": ("x", -20.0)},
    "sit": {"thigh_l": ("x", -88.0), "thigh_r": ("x", -88.0), "calf_l": ("x", 88.0), "calf_r": ("x", 88.0),
            "spine_03": ("x", -6.0), "upperarm_l": ("x", -25.0), "upperarm_r": ("x", -25.0),
            "lowerarm_l": ("x", -40.0), "lowerarm_r": ("x", -40.0)},
}


# ---- poses --------------------------------------------------------------------------------------------------------

def rot(axis, deg):
    """3x3, Kiln's M4::rot_x / rot_y / rot_z (right-handed, column vectors)."""
    s, c = math.sin(math.radians(deg)), math.cos(math.radians(deg))
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype=float)
    if axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype=float)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def bone_order(bones, parent):
    order, seen = [], set()

    def visit(b):
        if b in seen:
            return
        p = parent.get(b)
        if p in bones:
            visit(p)
        seen.add(b)
        order.append(b)
    for b in sorted(bones):
        visit(b)
    return order


def pose_moves(bones, parent, pose):
    """{bone: 4x4 move in world space from bind to pose}: a turn about the bone's bind joint, after its parent's."""
    spec = KILN_POSES[pose] if isinstance(pose, str) else pose
    out = {}
    for b in bone_order(bones, parent):
        M = out.get(parent.get(b), np.eye(4)).copy() if parent.get(b) in bones else np.eye(4)
        if b in spec:
            ax, deg = spec[b]
            j = bones[b][:3, 3]
            own = np.eye(4)
            own[:3, :3] = rot(ax, deg)
            own[:3, 3] = j - own[:3, :3] @ j
            M = M @ own
        out[b] = M
    return out


def lbs(verts, weights, moves):
    """Linear blend of the moves by each point's weights (normalised); points with no weight stay put."""
    acc = np.zeros_like(verts, dtype=float)
    tot = np.zeros(len(verts))
    for b, (idx, w) in weights.items():
        M = moves.get(b)
        if M is None:
            continue
        p = verts[idx]
        np.add.at(acc, idx, w[:, None] * (p @ M[:3, :3].T + M[:3, 3]))
        np.add.at(tot, idx, w)
    out = np.array(verts, dtype=float, copy=True)
    ok = tot > 1e-9
    out[ok] = acc[ok] / tot[ok, None]
    return out


# ---- surfaces -----------------------------------------------------------------------------------------------------

def tri_normals(V, T):
    n = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    ln = np.linalg.norm(n, axis=1, keepdims=True)
    ln[ln == 0] = 1.0
    return n / ln


def nearest(V, T, P, k=NEAREST_K):
    """Nearest surface point of triangles T to each of P: (point (M, 3), distance (M,), triangle (M,), bary (M, 3)),
    from the k triangles with the nearest middles (bend_back.transfer's search)."""
    from scipy.spatial import cKDTree
    P = np.asarray(P, dtype=float)
    if len(P) == 0:
        return np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64), np.zeros((0, 3))
    k = min(k, len(T))
    _, cand = cKDTree(V[T].mean(axis=1)).query(P, k=k)
    cand = np.asarray(cand).reshape(len(P), k)
    TT = T[cand.ravel()]
    q, bary = bend_back.closest_on_triangles(np.repeat(P, k, axis=0), V[TT[:, 0]], V[TT[:, 1]], V[TT[:, 2]])
    d = np.linalg.norm(np.repeat(P, k, axis=0) - q, axis=1).reshape(len(P), k)
    best = np.argmin(d, axis=1)
    rows = np.arange(len(P))
    sel = rows * k + best
    return q[sel], d[rows, best], cand[rows, best], bary[sel]


def open_points(n, T):
    """Points on a triangle edge only one triangle uses (the cloth's openings; Kiln's open_vert)."""
    e = np.sort(np.concatenate([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]), axis=1)
    u, c = np.unique(e, axis=0, return_counts=True)
    out = np.zeros(n, bool)
    out[u[c == 1].ravel()] = True
    return out


def face_signs(CV, CT, BV, BT):
    """(signs (F,), share flipped): +1 where a cloth face faces the way the body surface nearest its middle does.
    One sign for all unless FLIP_SHARE or more disagree (Kiln's outward_signs)."""
    q, d, ti, _ = nearest(BV, BT, CV[CT].mean(axis=1))
    s = np.where(np.einsum("ij,ij->i", tri_normals(CV, CT), tri_normals(BV, BT)[ti]) < 0, -1.0, 1.0)
    major = 1.0 if np.sum(s > 0) * 2 >= len(s) else -1.0
    flipped = float(np.mean(s != major)) if len(s) else 0.0
    return (np.full(len(s), major) if flipped < FLIP_SHARE else s), flipped


def rim_points(n, T, signs):
    pos, neg = np.zeros(n, bool), np.zeros(n, bool)
    pos[T[signs > 0].ravel()] = True
    neg[T[signs < 0].ravel()] = True
    return pos & neg


def through(CV, CT, P, BV, BT, limit=LIMIT, skip=SKIP, reach=REACH, signs=None):
    """Kiln's through_idx: (indices of P through the cloth, their depth (m), the cloth's signs)."""
    from scipy.spatial import cKDTree
    if signs is None:
        signs, _ = face_signs(CV, CT, BV, BT)
    opn = open_points(len(CV), CT)
    bnd = opn | rim_points(len(CV), CT, signs)
    zlo, zhi = CV[:, 2].min(), CV[:, 2].max()
    cand = np.nonzero((P[:, 2] >= zlo) & (P[:, 2] <= zhi))[0]
    q, d, ti, bary = nearest(CV, CT, P[cand])
    fn = tri_normals(CV, CT)[ti] * signs[ti, None]
    sd = np.einsum("ij,ij->i", P[cand] - q, fn)
    ok = (d <= reach) & (sd > limit)
    # the nearest point on an open edge: every corner it leans on is open
    corner_open = opn[CT[ti]]
    on_rim = np.all(corner_open | (bary <= 1e-9), axis=1) & np.any(bary > 1e-9, axis=1)
    ok &= ~on_rim
    if bnd.any() and ok.any():
        dd, _ = cKDTree(CV[bnd]).query(q[ok])
        sub = np.nonzero(ok)[0]
        ok[sub[dd < skip]] = False
    return cand[ok], sd[ok], signs


def parity_inside(P, V, T, slab=0.01, chunk=4_000_000):
    """Kiln's inside_parity for each of P against the closed-ish surface (V, T): 8 horizontal rays at k*45 deg + 0.07
    rad, inside when 5 or more cross an odd number of times (Moller-Trumbore, triangles bucketed by height). Each ray
    starts 0.13 micrometres above its point: a point level with a ring of horizontal edges (a mesh's own rows, or a
    garment made on the body's rows) would otherwise send its rays along shared edges and count them twice."""
    P = np.asarray(P, dtype=float) + np.array([0.0, 0.0, 1.3e-7])
    out = np.zeros(len(P), bool)
    if not len(P):
        return out
    A, B, C = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    zlo = np.minimum(np.minimum(A[:, 2], B[:, 2]), C[:, 2])
    zhi = np.maximum(np.maximum(A[:, 2], B[:, 2]), C[:, 2])
    e1, e2 = B - A, C - A
    dirs = [np.array([math.cos(k * math.pi / 4 + 0.07), math.sin(k * math.pi / 4 + 0.07), 0.0]) for k in range(8)]
    bins = np.floor(P[:, 2] / slab).astype(np.int64)
    for bval in np.unique(bins):
        pid = np.nonzero(bins == bval)[0]
        lo, hi = bval * slab, (bval + 1) * slab
        tid = np.nonzero((zlo <= hi) & (zhi >= lo))[0]
        if not len(tid):
            continue
        odd = np.zeros(len(pid), np.int64)
        step = max(1, chunk // max(1, len(tid) * 3))
        for s0 in range(0, len(pid), step):
            ps = pid[s0:s0 + step]
            tv = P[ps][:, None, :] - A[tid][None, :, :]                 # (m, n, 3)
            qv = np.cross(tv, e1[tid][None, :, :])                         # (m, n, 3)
            tq = np.einsum("mnk,nk->mn", qv, e2[tid])
            for d in dirs:
                pv = np.cross(d, e2[tid])                                  # (n, 3)
                det = np.einsum("nk,nk->n", e1[tid], pv)
                good = np.abs(det) > 1e-14
                inv = np.where(good, 1.0 / np.where(good, det, 1.0), 0.0)
                u = np.einsum("mnk,nk->mn", tv, pv) * inv
                v = (qv @ d) * inv
                t = tq * inv
                hit = good[None, :] & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 0)
                odd[s0:s0 + step] += (hit.sum(axis=1) % 2)
        out[pid] = odd >= 5
    return out


def inside(CP, BV, BT, limit=LIMIT):
    """Kiln's count_inside: cloth points over `limit` from the body and inside it by parity. Returns (mask, distance)."""
    _, d, _, _ = nearest(BV, BT, CP)
    m = d > limit
    res = np.zeros(len(CP), bool)
    idx = np.nonzero(m)[0]
    res[idx] = parity_inside(CP[idx], BV, BT)
    return res, d


def stretch(rest, posed, edges, limit=STRETCH, fam=None):
    ls = np.linalg.norm(rest[edges[:, 0]] - rest[edges[:, 1]], axis=1)
    ok = ls > MIN_EDGE
    e = edges[ok]
    r = np.linalg.norm(posed[e[:, 0]] - posed[e[:, 1]], axis=1) / ls[ok]
    out = {"edgesStretchedOver1_2x": int(np.sum(r > limit)), "worstStretch": round(float(r.max()), 3) if len(r) else 1.0,
           "stretchP99": round(float(np.percentile(r, 99)), 3) if len(r) else 1.0}
    if len(r) and fam is not None:
        k = int(np.argmax(r))
        out["worstStretchAt"] = {"restPoint": [round(float(x), 3) for x in rest[e[k, 0]]], "mainBones": [fam[e[k, 0]], fam[e[k, 1]]]}
        over = e[r > limit]
        if len(over):
            out["stretchedByArea"] = _count(fam[over[:, 0]])
    return out


def _count(labels):
    u, c = np.unique(np.asarray(labels, dtype=str), return_counts=True)
    return dict(sorted(((str(a), int(b)) for a, b in zip(u, c)), key=lambda kv: -kv[1]))


# ---- where --------------------------------------------------------------------------------------------------------

def main_bone(verts_n, weights):
    """Each point's heaviest bone name ('' if none)."""
    best_w = np.zeros(verts_n)
    best = np.array([""] * verts_n, dtype=object)
    for b, (idx, w) in weights.items():
        m = w > best_w[idx]
        best_w[idx[m]] = w[m]
        best[idx[m]] = b
    return best


def family(b):
    side = "_l" if b.endswith("_l") else "_r" if b.endswith("_r") else ""
    n = b.lower()
    if n.startswith(("thigh",)):
        return "thigh" + side
    if n.startswith(("calf",)):
        return "calf" + side
    if n.startswith(("foot", "ball", "toe", "bigtoe", "indextoe", "middletoe", "ringtoe", "littletoe")):
        return "foot" + side
    if n.startswith(("clavicle", "upperarm", "lowerarm", "hand", "thumb", "index", "middle", "ring", "pinky", "wrist")):
        return "arm" + side
    if n.startswith(("neck", "head", "facial")):
        return "head"
    return "trunk"


def by_area(idx, fam, rest_y, pelvis_y):
    out = {}
    for i in idx:
        k = "%s %s" % (fam[i], "front" if rest_y[i] < pelvis_y else "back")
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


# ---- the sitting shape --------------------------------------------------------------------------------------------

def boundary_loops(g):
    """Open loops of the garment's polygon edges (edges one polygon uses), each as an ordered point list."""
    a = g.corners
    nxt = np.arange(len(a)) + 1
    nxt[g.poly_start[1:] - 1] = g.poly_start[:-1]
    e = np.sort(np.stack([a, a[nxt]], axis=1), axis=1)
    e = e[e[:, 0] != e[:, 1]]
    u, c = np.unique(e, axis=0, return_counts=True)
    open_e = u[c == 1]
    nb = {}
    for p, q in open_e:
        nb.setdefault(int(p), []).append(int(q))
        nb.setdefault(int(q), []).append(int(p))
    seen, loops = set(), []
    for start in sorted(nb):
        if start in seen:
            continue
        loop, prev, cur = [start], None, start
        seen.add(start)
        while True:
            nx = [x for x in nb[cur] if x != prev and x not in seen]
            if not nx:
                break
            prev, cur = cur, nx[0]
            seen.add(cur)
            loop.append(cur)
        loops.append(loop)
    return loops


def hem_report(g, rest, posed, moves, body):
    knee_z = np.mean([body.bones[b][:3, 3][2] for b in ("calf_l", "calf_r") if b in body.bones])
    mid_x = body.bones["pelvis"][:3, 3][0] if "pelvis" in body.bones else 0.0
    hems = []
    for loop in boundary_loops(g):
        ids = np.array(loop)
        if len(ids) < 6 or rest[ids, 2].mean() >= knee_z:
            continue
        side = "r" if rest[ids, 0].mean() < mid_x else "l"
        M = moves.get("calf_" + side, np.eye(4))
        Minv = np.linalg.inv(M)
        back = posed[ids] @ Minv[:3, :3].T + Minv[:3, 3]
        dv = back - rest[ids]
        shape = np.linalg.norm(dv - dv.mean(axis=0), axis=1)
        cy = rest[ids, 1].mean()
        front, rear = rest[ids, 1] < cy, rest[ids, 1] >= cy

        def drop(z):
            return round(1000 * float(z[front].mean() - z[rear].mean()), 1) if front.any() and rear.any() else None
        hems.append({"side": side, "points": int(len(ids)), "restZ": round(float(rest[ids, 2].mean()), 3),
                     "riseMm": round(1000 * float(dv[:, 2].mean()), 1),
                     "shapeChangeMm": round(1000 * float(shape.max()), 1),
                     "heightRangeMm": {"rest": round(1000 * float(np.ptp(rest[ids, 2])), 1),
                                       "posed": round(1000 * float(np.ptp(back[:, 2])), 1)},
                     "backMinusFrontDropMm": {"rest": drop(rest[ids, 2]), "posed": drop(back[:, 2])}})
    return hems


def seat_report(seat_ids, PB, CV, CT, signs, through_ids, limit=LIMIT):
    """The seat's and thighs' gap to the posed cloth over them: points through (by the pose's own through measure)
    are counted, the rest give the gap (outside-the-body distance to the nearest cloth face, by its outward side)."""
    if not len(seat_ids):
        return {"points": 0}
    thr = np.isin(seat_ids, through_ids)
    q, d, ti, _ = nearest(CV, CT, PB[seat_ids])
    sd = np.einsum("ij,ij->i", PB[seat_ids] - q, tri_normals(CV, CT)[ti] * signs[ti, None])
    keep = ~thr & (sd <= limit)
    gap = np.maximum(-sd[keep] * 1000.0, 0.0)
    return {"points": int(len(seat_ids)), "throughOver3mm": int(thr.sum()),
            "outsideButNotCountedThrough": int(np.sum(~thr & (sd > limit))),
            "gapMedianMm": round(float(np.median(gap)), 1) if len(gap) else None,
            "gapP90Mm": round(float(np.percentile(gap, 90)), 1) if len(gap) else None}


# ---- the check ----------------------------------------------------------------------------------------------------

def skeleton_report(gs, body):
    common = [b for b in gs.bones if b in body.bones]
    worst = max((1000 * float(np.abs(gs.bones[b][:3, 3] - body.bones[b][:3, 3]).max()) for b in common), default=0.0)
    used = sorted(gs.weights)
    missing = [b for b in used if b not in body.bones]
    return {"garmentBones": len(gs.bones), "weightedBones": len(used), "weightedNotOnBody": missing[:20],
            "worstJointMm": round(worst, 4), "pass": not missing and worst <= 0.01}


def check(garment_fbx, body_fbx, poses=None, shape_bars=None, name=None):
    import skin_transfer as stf
    poses = list(poses or POSE_ORDER)
    body = fbx_skin.load_skinned(body_fbx)
    gs = fbx_skin.load_skinned(garment_fbx)
    g = stf.read_fbx(garment_fbx)
    rest_c = g.verts
    rep = {"tool": "tools/md/pose_check.py", "name": name or os.path.splitext(os.path.basename(garment_fbx))[0],
           "garment": garment_fbx.replace("\\", "/"), "garmentSha256_16": bend_back.sha16(garment_fbx),
           "body": body_fbx.replace("\\", "/"), "bodySha256_16": bend_back.sha16(body_fbx),
           "points": int(len(rest_c)), "bodyPoints": int(len(body.verts)),
           "bars": {"bodyThroughClothOver3mm": BAR_THROUGH, "clothInsideBodyOver3mm": BAR_INSIDE,
                    "source": "Kiln parity bar, MECHANICS.md Pass/fail 1, 2, 8 (method note section 4 check 3); the tool's bar, not the floor"},
           "skeleton": skeleton_report(gs, body)}
    tot = np.zeros(len(rest_c))
    for _, (idx, w) in gs.weights.items():
        np.add.at(tot, idx, w)
    rep["unweightedPoints"] = int(np.sum(tot <= 1e-9))
    CT = g.tris()[0]
    edges = g.edges()
    fam = np.array([family(b) for b in main_bone(len(body.verts), body.weights)], dtype=object)
    pelvis_y = body.bones["pelvis"][:3, 3][1] if "pelvis" in body.bones else 0.0
    # covered at rest: body points the rest cloth lies over (within reach, not through)
    signs0, flip0 = face_signs(rest_c, CT, body.verts, body.tris)
    cand = np.nonzero((body.verts[:, 2] >= rest_c[:, 2].min()) & (body.verts[:, 2] <= rest_c[:, 2].max()))[0]
    q, d, ti, _ = nearest(rest_c, CT, body.verts[cand])
    sd0 = np.einsum("ij,ij->i", body.verts[cand] - q, tri_normals(rest_c, CT)[ti] * signs0[ti, None])
    covered = np.zeros(len(body.verts), bool)
    covered[cand[(d <= REACH) & (sd0 <= LIMIT)]] = True
    rep["bodyPointsCoveredAtRest"] = int(covered.sum())
    pz = body.bones["pelvis"][:3, 3][2] if "pelvis" in body.bones else 1.0
    seat_ids = np.nonzero(covered & (np.char.startswith(fam.astype(str), "thigh") |
                                     ((fam == "trunk") & (body.verts[:, 2] < pz))))[0]
    gfam = np.array([family(b) for b in main_bone(len(rest_c), gs.weights)], dtype=object)
    results = []
    for pose in poses:
        moves = pose_moves(body.bones, body.parent, pose)
        PB = lbs(body.verts, body.weights, moves)
        PC = lbs(rest_c, gs.weights, moves)
        idx_k, depth_k, signs_k = through(PC, CT, PB, PB, body.tris)
        idx_r, depth_r, _ = through(PC, CT, PB, PB, body.tris, signs=signs0)
        idx, depth, signs = (idx_r, depth_r, signs0) if len(idx_r) >= len(idx_k) else (idx_k, depth_k, signs_k)
        ins, _ = inside(PC, PB, body.tris)
        r = {"pose": pose, "bodyThroughClothOver3mm": int(len(idx)),
             "throughKilnPoseSides": int(len(idx_k)), "throughRestSides": int(len(idx_r)),
             "throughCoveredAtRest": int(covered[idx].sum()),
             "throughByArea": by_area(idx, fam, body.verts[:, 1], pelvis_y),
             "deepestThroughMm": round(1000 * float(depth.max()), 1) if len(depth) else 0.0,
             "clothInsideBodyOver3mm": int(ins.sum()),
             "insideByArea": _count(gfam[ins]) if ins.any() else {},
             "flippedFaceShare": round(float(np.mean(signs_k != (1.0 if np.sum(signs_k > 0) * 2 >= len(signs_k) else -1.0))), 4)}
        r.update(stretch(rest_c, PC, edges, fam=gfam))
        r["pass"] = r["bodyThroughClothOver3mm"] <= BAR_THROUGH and r["clothInsideBodyOver3mm"] <= BAR_INSIDE
        if pose == "sit":
            r["shape"] = {"seatAndThighs": seat_report(seat_ids, PB, PC, CT, signs, idx),
                          "hems": hem_report(g, rest_c, PC, moves, body)}
        results.append(r)
    rep["poses"] = results
    rep["restFlippedFaceShare"] = round(flip0, 4)
    rep["toolBarPass"] = all(r["pass"] for r in results)
    sit = next((r for r in results if r["pose"] == "sit"), None)
    if sit is not None:
        rep["shapeCheck"] = shape_verdict(sit["shape"], shape_bars)
    rep["pass"] = rep["toolBarPass"] and rep["skeleton"]["pass"] and (rep.get("shapeCheck", {}).get("pass") is not False)
    return rep


def shape_numbers(shape):
    hems = shape.get("hems") or []
    return {"gapP90Mm": shape.get("seatAndThighs", {}).get("gapP90Mm"),
            "hemShapeChangeMm": max((h["shapeChangeMm"] for h in hems), default=None)}


def shape_verdict(shape, ref):
    """ref: a report of this tool on the reference garment (Tom's passed jeans), or None."""
    mine = shape_numbers(shape)
    out = {"measured": mine}
    if not ref:
        out.update({"bars": None, "pass": None, "note": "no reference: bars U until measured on Tom's passed jeans"})
        return out
    rs = next((r for r in ref.get("poses", []) if r["pose"] == "sit"), None)
    if rs is None or "shape" not in rs:
        out.update({"bars": None, "pass": None, "note": "the reference has no sitting shape"})
        return out
    refn = shape_numbers(rs["shape"])
    bars, fails = {}, []
    for k in ("gapP90Mm", "hemShapeChangeMm"):
        if refn[k] is None:
            continue
        bars[k] = round(refn[k] * (1 + SHAPE_TOL) + SHAPE_FLOOR_MM, 1)
        if mine[k] is None or mine[k] > bars[k]:
            fails.append("%s %s over %s" % (k, mine[k], bars[k]))
    out.update({"reference": ref.get("garment"), "referenceNumbers": refn, "bars": bars, "pass": not fails, "fails": fails})
    return out


def main(argv):
    if "--selftest" in argv:
        import unittest
        suite = unittest.defaultTestLoader.loadTestsFromName("test_pose_check")
        res = unittest.TextTestRunner(verbosity=1).run(suite)
        n, bad = res.testsRun, len(res.failures) + len(res.errors)
        print("pose_check selftest: passed=%d/%d failed=%d" % (n - bad, n, bad))
        return 0 if res.wasSuccessful() else 4
    valued = ("--poses", "--shape-bars", "--name")
    pos, k = [], 0
    while k < len(argv):
        if argv[k] in valued:
            k += 2
            continue
        if not argv[k].startswith("--"):
            pos.append(argv[k])
        k += 1

    def opt(nm, default=None):
        return argv[argv.index(nm) + 1] if nm in argv else default
    if len(pos) != 3:
        print(__doc__)
        return 2
    ref = None
    if opt("--shape-bars"):
        with open(opt("--shape-bars"), encoding="utf-8") as f:
            ref = json.load(f)
    poses = [p.strip() for p in opt("--poses", ",".join(POSE_ORDER)).split(",")]
    rep = check(pos[0], pos[1], poses, ref, opt("--name"))
    with open(pos[2], "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=1)
    print("POSE CHECK " + json.dumps({"pass": rep["pass"], "poses": [{k: r[k] for k in ("pose", "bodyThroughClothOver3mm",
          "clothInsideBodyOver3mm", "worstStretch")} for r in rep["poses"]], "shape": rep.get("shapeCheck")}), flush=True)
    return 0 if rep["pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
