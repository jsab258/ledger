"""A garment draped on a standard body (Kiln, since 16 Nov 2026: forearms straightened) bent back to the wearer's
reference pose, the pose the game's bodies stand in, by the body's own skin weights and the standard body's turns
record (tools/md/standard_turns.py).

    python tools/md/bend_back.py STANDARD_BODY.fbx STANDARD_BODY.json GARMENT.obj OUT.obj
        [--mode exact|lbs] [--report OUT.report.json]
    python tools/md/bend_back.py --selftest

WHY, 17 November 2026 (Kiln M5 step a, KILN-M5-RIGGING-METHOD-2026-11-17.md section 3 and its review's fix 1): Kiln
drapes only on the standard bodies, whose forearms are turned about each elbow onto the upper arm's line, so every
drape must come back to the reference pose before weld, game mesh and skinning (skin weights come from the reference
body, never the standard one). tools/md/unpose_garment.py does this in Blender for pose_body.py's drape bodies; this
does the same in plain Python (numpy and scipy), so it runs in seconds beside other jobs and its maths is tested on
synthetic meshes.

HOW.
- The body (FBX, read by fbx_skin.py) gives its skin points, triangles, bone tree and skin weights.
- The record's turns (pose_body.py's layout: per side an "elbow" {turnDeg, axis, elbow}, optionally the upper arm's
  {turnDeg, axis, shoulder} on the side itself and a "thigh" {turnDeg, axis, hip}), in Blender's world frame in metres,
  are taken in the order they were made (upper arms, elbows, thighs). Each turns its bone and every bone below it
  about its pivot. Each bone's whole move is the product of the turns above it; bones with the same moves form one
  group, and each skin point's weights become the share of its weight in each group (Blender's armature modifier
  divides by the point's total weight in the same way).
- Each garment point takes those shares from the nearest point of the body's surface, interpolated across its
  triangle (as unpose_garment.py's nearest-face data transfer does).
- --mode exact (the default): each point is moved by the exact inverse of its blended forward move, so a point lying
  on the skin goes back to exactly where that skin point came from. --mode lbs: each point is moved by the blend of
  the turns' inverses, as unpose_garment.py does with the skeleton; it is not an exact inverse where an elbow point is
  weighted to both arm bones, and is kept only to compare with that tool.
- The OBJ is Marvelous's or Kiln's layout (millimetres, y up, the body facing +z), read as Blender's (x, -z, y)/1000.
  It is written back line for line: each "v" line a point's new place (left as it was when the point moved less than
  0.0001 mm), the "vn" lines and faces' normal indices dropped since the bend changed the normals, all else kept.
- A drape body raised for shoes (pose_body.py --raise, raiseMm in its record) is refused: the standard bodies are not
  raised, and that case belongs to unpose_garment.py.
"""
import hashlib
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# A point that moved less than this (millimetres) keeps its own "v" line, byte for byte.
KEEP_LINE_MM = 1e-4
# Nearest triangles tried for each garment point, by their middles.
NEAREST_TRIS = 24


# ---- turns ------------------------------------------------------------------------------------------------------

def rotation_about(axis, deg, pivot):
    """4x4: a right-handed turn of `deg` degrees about the unit `axis` through `pivot` (Blender's Matrix.Rotation)."""
    a = np.asarray(axis, dtype=float)
    a = a / np.linalg.norm(a)
    t = math.radians(deg)
    K = np.array([[0.0, -a[2], a[1]], [a[2], 0.0, -a[0]], [-a[1], a[0], 0.0]])
    R = np.eye(3) + math.sin(t) * K + (1.0 - math.cos(t)) * (K @ K)
    p = np.asarray(pivot, dtype=float)
    M = np.eye(4)
    M[:3, :3] = R
    M[:3, 3] = p - R @ p
    return M


def turn_from_joints(shoulder, elbow, hand):
    """The forearm's turn as standard_body.py and pose_body.py --straight-elbows make it: the angle between upper arm
    and forearm, about forearm x upper arm, through the elbow. Returns {turnDeg, axis, elbow} (axis None if straight)."""
    s, e, h = (np.asarray(x, dtype=float) for x in (shoulder, elbow, hand))
    up = (e - s) / np.linalg.norm(e - s)
    fore = (h - e) / np.linalg.norm(h - e)
    ang = math.acos(max(-1.0, min(1.0, float(fore @ up))))
    cr = np.cross(fore, up)
    axis = (cr / np.linalg.norm(cr)).tolist() if np.linalg.norm(cr) > 1e-12 else None
    return {"turnDeg": math.degrees(ang), "axis": axis, "elbow": e.tolist()}


def turn_list(record):
    """The record's turns in the order they were made: [{bone, pivot, axis, deg, side, kind}]."""
    if float(record.get("raiseMm", 0.0) or 0.0):
        raise ValueError("the record raises the body (raiseMm): bend it back with tools/md/unpose_garment.py")
    turns = record["turns"]
    out = []
    for kind, bone, key in (("shoulder", "upperarm_", "shoulder"), ("elbow", "lowerarm_", "elbow"), ("thigh", "thigh_", "hip")):
        for s in sorted(turns):
            t = turns[s]
            rec = t if (kind == "shoulder" and "turnDeg" in t) else (t.get(kind) if kind != "shoulder" else None)
            if not rec or rec.get("axis") is None or not float(rec.get("turnDeg", 0.0)):
                continue
            out.append({"bone": bone + s, "pivot": rec[key], "axis": rec["axis"], "deg": float(rec["turnDeg"]),
                        "side": s, "kind": kind})
    return out


def bone_groups(turns, subtree_of, bones):
    """Bones grouped by which turns move them. Returns (bone -> group index, list of 4x4 forward moves); group 0 is
    the bones no turn moves (the identity)."""
    under = [set(subtree_of(t["bone"])) for t in turns]
    masks = {b: tuple(b in u for u in under) for b in bones}
    keys = [tuple(False for _ in turns)]
    for m in sorted(set(masks.values())):
        if m not in keys:
            keys.append(m)
    mats = []
    for m in keys:
        M = np.eye(4)
        for k, t in enumerate(turns):
            if m[k]:
                M = rotation_about(t["axis"], t["deg"], t["pivot"]) @ M
        mats.append(M)
    index = {m: i for i, m in enumerate(keys)}
    return {b: index[m] for b, m in masks.items()}, np.array(mats)


def group_shares(n_points, weights, bone_group, n_groups):
    """(n_points, n_groups): each point's share of its skin weight in each group. Points with no weight stay put."""
    acc = np.zeros((n_points, n_groups))
    for bone, (idx, w) in weights.items():
        g = bone_group.get(bone, 0)
        np.add.at(acc[:, g], idx, w)
    tot = acc.sum(axis=1)
    out = np.zeros_like(acc)
    ok = tot > 1e-4
    out[ok] = acc[ok] / tot[ok, None]
    out[~ok, 0] = 1.0
    return out


def blend(shares, mats):
    """(N, 4, 4): each point's blended forward move."""
    return np.einsum("ng,gij->nij", shares, mats)


def forward(points, shares, mats):
    M = blend(shares, mats)
    return np.einsum("nij,nj->ni", M[:, :3, :3], points) + M[:, :3, 3]


def bend_back_points(points, shares, mats, mode="exact"):
    """Points on (or near) the posed body taken back. exact: the inverse of each point's blended move; lbs: the blend
    of the moves' inverses (unpose_garment.py's way)."""
    points = np.asarray(points, dtype=float)
    if mode == "exact":
        M = blend(shares, mats)
        A, t = M[:, :3, :3], M[:, :3, 3]
        det = np.linalg.det(A)
        if np.any(det < 1e-3):
            raise ValueError("a blended move cannot be undone at %d points (turns near half a circle)" % int(np.sum(det < 1e-3)))
        return np.linalg.solve(A, (points - t)[:, :, None])[:, :, 0]
    if mode == "lbs":
        inv = np.array([np.linalg.inv(m) for m in mats])
        return forward(points, shares, inv)
    raise ValueError("mode is exact or lbs, not %r" % mode)


# ---- nearest surface point ----------------------------------------------------------------------------------------

def closest_on_triangles(p, a, b, c):
    """Closest points of triangles (a, b, c) to points p, all (M, 3) (Ericson, Real-Time Collision Detection 5.1.5).
    Returns (closest points (M, 3), barycentric weights (M, 3) for a, b, c)."""
    p, a, b, c = (np.asarray(x, dtype=float) for x in (p, a, b, c))
    ab, ac, ap = b - a, c - a, p - a
    d1, d2 = np.einsum("ij,ij->i", ab, ap), np.einsum("ij,ij->i", ac, ap)
    bp = p - b
    d3, d4 = np.einsum("ij,ij->i", ab, bp), np.einsum("ij,ij->i", ac, bp)
    cp = p - c
    d5, d6 = np.einsum("ij,ij->i", ab, cp), np.einsum("ij,ij->i", ac, cp)
    vc = d1 * d4 - d3 * d2
    vb = d5 * d2 - d1 * d6
    va = d3 * d6 - d5 * d4
    with np.errstate(divide="ignore", invalid="ignore"):
        den = va + vb + vc
        v_in = np.where(den != 0, vb / den, 1.0 / 3.0)
        w_in = np.where(den != 0, vc / den, 1.0 / 3.0)
        bary = np.stack([1.0 - v_in - w_in, v_in, w_in], axis=1)
        # the regions, the last assigned winning, so they go from the least to the most particular
        t = np.clip((d4 - d3) / ((d4 - d3) + (d5 - d6)), 0, 1)
        m = (va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0)
        bary[m] = np.stack([np.zeros(m.sum()), 1 - t[m], t[m]], axis=1)
        t = np.clip(d2 / (d2 - d6), 0, 1)
        m = (vb <= 0) & (d2 >= 0) & (d6 <= 0)
        bary[m] = np.stack([1 - t[m], np.zeros(m.sum()), t[m]], axis=1)
        m = (d6 >= 0) & (d5 <= d6)
        bary[m] = [0.0, 0.0, 1.0]
        t = np.clip(d1 / (d1 - d3), 0, 1)
        m = (vc <= 0) & (d1 >= 0) & (d3 <= 0)
        bary[m] = np.stack([1 - t[m], t[m], np.zeros(m.sum())], axis=1)
        m = (d3 >= 0) & (d4 <= d3)
        bary[m] = [0.0, 1.0, 0.0]
        m = (d1 <= 0) & (d2 <= 0)
        bary[m] = [1.0, 0.0, 0.0]
    q = bary[:, :1] * a + bary[:, 1:2] * b + bary[:, 2:] * c
    return q, bary


def transfer(body_verts, tris, data, points, k=NEAREST_TRIS):
    """Per-point data of the body (N, D) at each of `points`, from the nearest surface point, interpolated across its
    triangle. Returns (data (M, D), distance to the surface (M,), triangle index (M,))."""
    from scipy.spatial import cKDTree
    body_verts = np.asarray(body_verts, dtype=float)
    tris = np.asarray(tris, dtype=np.int64)
    points = np.asarray(points, dtype=float)
    mids = body_verts[tris].mean(axis=1)
    k = min(k, len(tris))
    _, cand = cKDTree(mids).query(points, k=k)
    cand = np.asarray(cand).reshape(len(points), k)
    flat = cand.ravel()
    P = np.repeat(points, k, axis=0)
    T = tris[flat]
    q, bary = closest_on_triangles(P, body_verts[T[:, 0]], body_verts[T[:, 1]], body_verts[T[:, 2]])
    d = np.linalg.norm(P - q, axis=1).reshape(len(points), k)
    best = np.argmin(d, axis=1)
    rows = np.arange(len(points))
    ti = cand[rows, best]
    bb = bary.reshape(len(points), k, 3)[rows, best]
    vt = tris[ti]
    out = np.einsum("mk,mkd->md", bb, np.asarray(data)[vt])
    return out, d[rows, best], ti


# ---- OBJ ----------------------------------------------------------------------------------------------------------

def mm_to_blender(xyz_mm):
    x = np.asarray(xyz_mm, dtype=float)
    return np.stack([x[:, 0], -x[:, 2], x[:, 1]], axis=1) / 1000.0


def blender_to_mm(xyz):
    x = np.asarray(xyz, dtype=float) * 1000.0
    return np.stack([x[:, 0], x[:, 2], -x[:, 1]], axis=1)


def read_obj(path):
    """(lines, the index of each "v" line, its points in millimetres, the groups as {name: set of point indices})."""
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    vidx, pts, groups, cur = [], [], {}, None
    for i, line in enumerate(lines):
        if line.startswith("v "):
            vidx.append(i)
            pts.append([float(t) for t in line.split()[1:4]])
        elif line.startswith("g "):
            cur = line[2:].strip()
            groups.setdefault(cur, set())
        elif line.startswith("f ") and cur is not None:
            for t in line.split()[1:]:
                j = int(t.split("/")[0])
                groups[cur].add(j - 1 if j > 0 else len(pts) + j)
    return lines, vidx, np.array(pts, dtype=float).reshape(-1, 3), groups


def write_obj(path, lines, vidx, old_mm, new_mm):
    vset = dict(zip(vidx, range(len(vidx))))
    moved = np.linalg.norm(new_mm - old_mm, axis=1)
    out = []
    for i, line in enumerate(lines):
        if i in vset:
            k = vset[i]
            if moved[k] < KEEP_LINE_MM:
                out.append(line)
            else:
                out.append("v %.4f %.4f %.4f\n" % tuple(new_mm[k]))
        elif line.startswith("vn "):
            continue
        elif line.startswith("f "):
            toks = line.split()[1:]
            out.append("f " + " ".join("/".join(t.split("/")[:2]).rstrip("/") for t in toks) + "\n")
        else:
            out.append(line)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(out))


# ---- the run ------------------------------------------------------------------------------------------------------

def sha16(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def body_shares(body, record):
    """(turns, shares (N, G), forward moves (G, 4, 4), bone -> group) for a body read by fbx_skin.load_skinned."""
    turns = turn_list(record)
    for t in turns:
        if t["bone"] not in body.bones:
            raise ValueError("the body has no %s bone for the record's %s turn" % (t["bone"], t["kind"]))
    bone_group, mats = bone_groups(turns, body.subtree, list(body.bones))
    shares = group_shares(len(body.verts), body.weights, bone_group, len(mats))
    return turns, shares, mats, bone_group


def run(body_fbx, record_json, garment_obj, out_obj, mode="exact", report=None):
    from fbx_skin import load_skinned
    with open(record_json, encoding="utf-8") as f:
        record = json.load(f)
    body = load_skinned(body_fbx)
    turns, shares, mats, _ = body_shares(body, record)
    lines, vidx, pts_mm, groups = read_obj(garment_obj)
    pts = mm_to_blender(pts_mm)
    g_shares, dist, _ = transfer(body.verts, body.tris, shares, pts)
    back = bend_back_points(pts, g_shares, mats, mode)
    new_mm = blender_to_mm(back)
    moved = np.linalg.norm(new_mm - pts_mm, axis=1)
    if os.path.abspath(out_obj) == os.path.abspath(garment_obj):
        raise ValueError("refusing to write over the garment")
    write_obj(out_obj, lines, vidx, pts_mm, new_mm)
    rep = {"tool": "tools/md/bend_back.py", "mode": mode,
           "body": body_fbx.replace("\\", "/"), "bodySha256_16": sha16(body_fbx),
           "record": record_json.replace("\\", "/"), "recordSha256_16": sha16(record_json),
           "garment": garment_obj.replace("\\", "/"), "garmentSha256_16": sha16(garment_obj),
           "out": out_obj.replace("\\", "/"),
           "turns": [{k: t[k] for k in ("bone", "kind", "deg")} for t in turns],
           "points": int(len(pts)), "pointsMovedOver0p1mm": int(np.sum(moved > 0.1)),
           "movedMmMax": round(float(moved.max()) if len(moved) else 0.0, 3),
           "movedMmMedian": round(float(np.median(moved)) if len(moved) else 0.0, 4),
           "distanceToBodyMm": {"median": round(1000 * float(np.median(dist)), 2), "p99": round(1000 * float(np.percentile(dist, 99)), 2),
                                "max": round(1000 * float(dist.max()), 2)},
           "pointsTakingTurnedWeight": int(np.sum(g_shares[:, 1:].sum(axis=1) > 1e-6)) if g_shares.shape[1] > 1 else 0,
           "groups": {}}
    for name, ids in groups.items():
        ids = np.array(sorted(ids), dtype=np.int64)
        if len(ids):
            rep["groups"][name] = {"points": int(len(ids)), "movedMmMax": round(float(moved[ids].max()), 3),
                                   "movedOver0p1mm": int(np.sum(moved[ids] > 0.1))}
    if report:
        with open(report, "w", encoding="utf-8") as f:
            json.dump(rep, f, indent=1)
    print("BENT BACK " + json.dumps({k: rep[k] for k in ("points", "pointsMovedOver0p1mm", "movedMmMax", "distanceToBodyMm")}), flush=True)
    return rep


def main(argv):
    if "--selftest" in argv:
        import unittest
        suite = unittest.defaultTestLoader.loadTestsFromName("test_bend_back")
        res = unittest.TextTestRunner(verbosity=1).run(suite)
        n = res.testsRun
        bad = len(res.failures) + len(res.errors)
        print("bend_back selftest: passed=%d/%d failed=%d" % (n - bad, n, bad))
        return 0 if res.wasSuccessful() else 4
    pos = [a for a in argv if not a.startswith("--")]
    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv else default
    for name in ("--mode", "--report"):
        if name in argv:
            pos.remove(argv[argv.index(name) + 1])
    if len(pos) != 4:
        print(__doc__)
        return 2
    run(pos[0], pos[1], pos[2], pos[3], mode=opt("--mode", "exact"), report=opt("--report"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
