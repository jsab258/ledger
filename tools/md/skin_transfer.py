"""A garment given its wearer's skin weights, without Blender: Kiln M5 step 2 (KILN-M5-RIGGING-METHOD-2026-11-17.md
sections 1, 3 f and 4). The bent-back drape (tools/md/bend_back.py, step 1) or any game mesh on the wearer's
reference-pose body takes the weights of that wearer's full body, after a check that the full body matches the Body
file the passed garments were bound on, with the joint rules the passed jeans needed, and is written as a skinned FBX
on the body's own skeleton.

    python tools/md/skin_transfer.py WEIGHTS_BODY.fbx GARMENT.obj|.fbx OUT_DIR NAME [options]
        --match-body BODY.fbx        the match check first (section 1); a failed check stops the run
        --reach 0.06 --angle 50      a copy is trusted only where the body is this near and faces this way
        --pieces auto|groups|pattern|none   the garment's pattern pieces (auto: OBJ groups, else the FBX's
                                     "pattern" UV islands, else none)
        --no-panels                  copy from the nearest body point, every piece from the whole body
        --no-keep-correctives        the trunk loses Epic's shoulder correctives with the arm
        --leg-sides auto|R:L         trousers: each leg from its own leg (R:L piece numbers or OBJ group names)
        --crotch-fade 0.07 --centre-seam auto|R:L   trousers: the thighs fade to the pelvis at the centre seam
        --max-influences 8           bones a point at most
        --compare ACCEPTED.fbx       per-point difference from an accepted skinned garment with the same points
    python tools/md/skin_transfer.py --match WEIGHTS_BODY.fbx BODY.fbx      the match check alone
    python tools/md/skin_transfer.py --selftest

WHY, 17 November 2026. The method note's step f is skin_garment.py, which calls bind_garment.py; both run inside
Blender. Kiln's drapes now come back through bend_back.py in plain Python, and the session decided (section 1) that
each wearer's weights come from his full reference-pose body (Ron: MH_RoccoP2_FullBody.fbx, which has the head the
Body file lacks) after a check that its skeleton and weights equal the Body file's. This file is that check and the
two Blender scripts' weight rules, ported line for line so their results can be compared point for point with a
garment they skinned (Ron's passed jeans), testable on synthetic meshes, and runnable in seconds beside other jobs.

HOW (bind_garment.py's steps, then skin_garment.py's, in their order).
1. Pieces. Each face belongs to a pattern piece: the OBJ's groups (Marvelous and Kiln write one per piece), or the
   islands of the FBX's "pattern" UV layer (as bind_garment.py finds them). A piece is a sleeve of one side when its
   centre lies beyond 1.3 half shoulder widths from the middle, the trunk otherwise.
2. Copy. The body's triangles are split into the left arm's, the right arm's and the trunk's (a triangle is an arm's
   where its points' weight on that arm's bones, the upper arm and all below it, averages 0.5 or more). Each garment
   point takes the weights of the nearest point of its own piece's surface, interpolated across that triangle; the
   trunk's copy has the arm bones taken out (Epic's shoulder correctives kept unless --no-keep-correctives). A point
   on both a sleeve and the trunk takes the sum of both copies, each normalised. A copy is reliable when the body is
   within --reach metres and the triangle faces within --angle degrees of the point's normal (either way round).
3. Inpaint. Unreliable points take the mean of their neighbours (the mesh's own edges, quads not split), 400 rounds.
4. Smooth 3 rounds (half the point, half its neighbours' mean), keep the 8 largest, normalise, drop weights at or
   under 0.0001 (Blender stores a group weight only above it; the binder's FBX holds no smaller one).
5. skin_garment.py's rules for trousers: --leg-sides (on a point of one side's pieces only, each bone of the other
   leg, thigh and everything under it, gives its weight to the same bone of its own leg), --crotch-fade (the centre
   seam is every point on both a right and a left piece; within the fade every bone named thigh* gives a smoothstep
   share of its weight to the pelvis, all of it on the seam); loose pieces inside the shoulders lose the arm (and the
   correctives) to spine_05 if nothing is left; head and facial weights go to neck_02; loose pieces smoothed over
   themselves 6 rounds; at most --max-influences bones, normalised.
   Not ported (step 3 adds them when a garment needs them): the skirt rule (skin_garment.py's default, off for
   trousers by --no-skirt), --collar-attr, the buttons, --also, the binder's decimation (the game mesh is already at
   its weight) and the maps-layout-first UV order (uv_order.py).
6. Out: OUT_DIR/NAME_skinned.fbx (binary FBX 7.4, centimetres, z up, the body facing -y as 3ds Max writes; the
   mesh with its UV layers, every bone of the body as a LimbNode placed by its bind pose, one cluster per used bone,
   the bind pose), NAME_weights.npz (the point by bone matrix) and skin.json (every count the Blender scripts log,
   the inputs' hashes, the match check, the comparison).
   Auto sides (trousers): a leg piece reaches below the knees (the calf joints); its side is its centre's (x below
   the pelvis is the right leg: the body faces -y). Other pieces (a waistband, pockets) belong to neither leg.
The match check (section 1): the same bone names; each bone's bind matrix equal to 0.01 mm (rotation entries to
1e-5); every Body point found on the full body within 0.01 mm, and on those points the same weight on every bone to
0.001.
"""
import hashlib
import json
import math
import os
import struct
import sys
import zlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import bend_back  # noqa: E402
import fbx_skin  # noqa: E402

REACH = 0.06
ANGLE = 50.0
INPAINT_ROUNDS = 400
SMOOTH_ROUNDS = 3
COLLAR_SMOOTH = 6
MAX_INFLUENCES = 8
KEEP_MIN = 1e-4
SLEEVE_ACROSS = 1.3
MATCH_MM = 0.01
MATCH_ROT = 1e-5
MATCH_W = 0.001


# ---- the garment --------------------------------------------------------------------------------------------------

class Garment:
    """Points (N, 3) in Blender's frame (metres, z up, facing -y); polygons as corner lists; per corner a UV index
    per layer; per face a piece number and the pieces' names."""

    def __init__(self):
        self.verts = None
        self.poly_start = None     # (F + 1,) offsets into corners
        self.corners = None        # (C,) point index per corner
        self.uv_layers = []        # [(name, uv (U, 2), index per corner (C,))]
        self.face_piece = None     # (F,) piece number, -1 none
        self.piece_names = []
        self.source = None

    @property
    def n_faces(self):
        return len(self.poly_start) - 1

    def faces(self):
        for f in range(self.n_faces):
            yield self.corners[self.poly_start[f]:self.poly_start[f + 1]]

    def tris(self):
        """Fans, as fbx_skin.py splits polygons: (T, 3) points, (T,) face of each, (T, 3) corner indices."""
        out, face, corner = [], [], []
        for f in range(self.n_faces):
            a, b = self.poly_start[f], self.poly_start[f + 1]
            for k in range(a + 1, b - 1):
                corner.append((a, k, k + 1))
                face.append(f)
        corner = np.array(corner, dtype=np.int64).reshape(-1, 3)
        return self.corners[corner], np.array(face, dtype=np.int64), corner

    def edges(self):
        """Unique point pairs along each polygon's boundary (Blender's mesh edges)."""
        a = self.corners
        nxt = np.arange(len(a)) + 1
        nxt[self.poly_start[1:] - 1] = self.poly_start[:-1]
        e = np.sort(np.stack([a, a[nxt]], axis=1), axis=1)
        e = e[e[:, 0] != e[:, 1]]
        return np.unique(e, axis=0)


def read_obj(path):
    """An OBJ in Marvelous's or Kiln's layout (millimetres, y up, facing +z), as bend_back.py reads it."""
    g = Garment()
    g.source = path
    pts, uvs, corners, cuv, starts, piece = [], [], [], [], [0], []
    names, cur = [], -1
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("v "):
                pts.append([float(t) for t in line.split()[1:4]])
            elif line.startswith("vt "):
                uvs.append([float(t) for t in line.split()[1:3]])
            elif line.startswith("g ") or line.startswith("o "):
                nm = line[2:].strip()
                if nm not in names:
                    names.append(nm)
                cur = names.index(nm)
            elif line.startswith("f "):
                for t in line.split()[1:]:
                    p = t.split("/")
                    j = int(p[0])
                    corners.append(j - 1 if j > 0 else len(pts) + j)
                    if len(p) > 1 and p[1]:
                        k = int(p[1])
                        cuv.append(k - 1 if k > 0 else len(uvs) + k)
                    else:
                        cuv.append(-1)
                starts.append(len(corners))
                piece.append(cur)
    g.verts = bend_back.mm_to_blender(np.array(pts, dtype=float).reshape(-1, 3))
    g.corners = np.array(corners, dtype=np.int64)
    g.poly_start = np.array(starts, dtype=np.int64)
    g.face_piece = np.array(piece, dtype=np.int64)
    g.piece_names = names
    cuv = np.array(cuv, dtype=np.int64)
    if len(uvs) and np.all(cuv >= 0):
        g.uv_layers.append(("UVMap", np.array(uvs, dtype=float), cuv))
    return g


def _model_is_identity(path, mesh_name):
    root, _ = fbx_skin.parse_fbx(path, max_array=fbx_skin.BIG)
    for n in root.find("Objects").children:
        if n.name == "Model" and fbx_skin._name(n.props[1]) == mesh_name:
            p70 = n.find("Properties70")
            for p in (p70.find_all("P") if p70 is not None else []):
                if p.props and p.props[0] in ("Lcl Translation", "Lcl Rotation", "Lcl Scaling", "GeometricTranslation",
                                              "GeometricRotation", "GeometricScaling"):
                    v = np.array([x for x in p.props[4:]], dtype=float)
                    want = np.ones(3) if "Scaling" in p.props[0] else np.zeros(3)
                    if np.abs(v - want).max() > 1e-6:
                        return False
    return True


def read_fbx(path, mesh=None):
    """A garment FBX (skinned, as skin_garment.py writes it, or static) through fbx_skin.py: points, polygons and every
    UV layer. A static mesh is taken as stored, so its model must carry no transform."""
    s = fbx_skin.load_skinned(path, mesh=mesh, need_weights=False)
    if not s.bones and not _model_is_identity(path, s.mesh_name):
        raise ValueError("%s: a static mesh whose model is moved, turned or scaled; export it with the transform applied" % path)
    geo = s.geometry
    pvi = np.array(geo.find("PolygonVertexIndex").props[0], dtype=np.int64)
    g = Garment()
    g.source = path
    g.verts = s.verts
    g.corners = np.where(pvi < 0, -pvi - 1, pvi)
    g.poly_start = np.concatenate([[0], np.nonzero(pvi < 0)[0] + 1]).astype(np.int64)
    for le in geo.find_all("LayerElementUV"):
        name = fbx_skin._name(le.find("Name").props[0]) if le.find("Name") is not None else "UV%d" % len(g.uv_layers)
        uv = np.array(le.find("UV").props[0], dtype=float).reshape(-1, 2)
        mapping = le.find("MappingInformationType").props[0]
        ref = le.find("ReferenceInformationType").props[0]
        if mapping != "ByPolygonVertex":
            continue
        idx = np.array(le.find("UVIndex").props[0], dtype=np.int64) if ref == "IndexToDirect" else np.arange(len(g.corners))
        g.uv_layers.append((name, uv, idx))
    g.face_piece = np.full(g.n_faces, -1, dtype=np.int64)
    g.skinned = s if s.bones else None
    return g


def read_garment(path, mesh=None):
    return read_obj(path) if path.lower().endswith(".obj") else read_fbx(path, mesh)


def uv_islands(g, layer="pattern"):
    """(F,) island number per face: faces joined across an edge whose two ends carry the same UVs (bind_garment.py's
    rule, 1e-5 apart)."""
    lay = next((x for x in g.uv_layers if x[0] == layer), None)
    if lay is None:
        return None
    _, uv, idx = lay
    cuv = uv[idx]
    edge_faces = {}
    for f in range(g.n_faces):
        a, b = g.poly_start[f], g.poly_start[f + 1]
        for k in range(a, b):
            k2 = k + 1 if k + 1 < b else a
            p, q = int(g.corners[k]), int(g.corners[k2])
            key = (p, q) if p < q else (q, p)
            uvp, uvq = (cuv[k], cuv[k2]) if p < q else (cuv[k2], cuv[k])
            edge_faces.setdefault(key, []).append((f, uvp, uvq))
    parent = list(range(g.n_faces))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for lst in edge_faces.values():
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                fa, ua, va = lst[i]
                fb, ub, vb = lst[j]
                if np.abs(ua - ub).max() < 1e-5 and np.abs(va - vb).max() < 1e-5:
                    ra, rb = find(fa), find(fb)
                    if ra != rb:
                        parent[max(ra, rb)] = min(ra, rb)
    roots = np.array([find(f) for f in range(g.n_faces)])
    _, out = np.unique(roots, return_inverse=True)
    return out.astype(np.int64)


def set_pieces(g, how="auto"):
    """Fill g.face_piece. Returns the way used: groups, pattern or none."""
    if how in ("auto", "groups") and g.piece_names and np.all(g.face_piece >= 0) and len(g.piece_names) > 1:
        return "groups"
    if how in ("auto", "pattern"):
        isl = uv_islands(g)
        if isl is not None:
            g.face_piece = isl
            g.piece_names = ["island%d" % i for i in range(int(isl.max()) + 1)]
            return "pattern"
    if how == "groups" and g.piece_names:
        return "groups"
    g.face_piece = np.full(g.n_faces, -1, dtype=np.int64)
    return "none"


def point_normals(g):
    """Angle-weighted point normals from each polygon's Newell normal (Blender's vertex normals)."""
    n = np.zeros_like(g.verts)
    for f in range(g.n_faces):
        ids = g.corners[g.poly_start[f]:g.poly_start[f + 1]]
        P = g.verts[ids]
        Q = np.roll(P, -1, axis=0)
        fn = np.array([np.sum((P[:, 1] - Q[:, 1]) * (P[:, 2] + Q[:, 2])), np.sum((P[:, 2] - Q[:, 2]) * (P[:, 0] + Q[:, 0])),
                       np.sum((P[:, 0] - Q[:, 0]) * (P[:, 1] + Q[:, 1]))])
        ln = np.linalg.norm(fn)
        if ln < 1e-15:
            continue
        fn /= ln
        prev, nxt = np.roll(P, 1, axis=0) - P, np.roll(P, -1, axis=0) - P
        cosang = np.einsum("ij,ij->i", prev, nxt) / np.maximum(np.linalg.norm(prev, axis=1) * np.linalg.norm(nxt, axis=1), 1e-15)
        ang = np.arccos(np.clip(cosang, -1, 1))
        np.add.at(n, ids, ang[:, None] * fn[None, :])
    ln = np.linalg.norm(n, axis=1, keepdims=True)
    ln[ln == 0] = 1.0
    return n / ln


def neighbours_matrix(n, edges):
    """Sparse (n, n): each row the mean of the point's edge neighbours (rows of lone points are empty)."""
    from scipy.sparse import csr_matrix
    if len(edges) == 0:
        return csr_matrix((n, n)), np.zeros(n, bool)
    r = np.concatenate([edges[:, 0], edges[:, 1]])
    c = np.concatenate([edges[:, 1], edges[:, 0]])
    deg = np.bincount(r, minlength=n).astype(float)
    M = csr_matrix((1.0 / deg[r], (r, c)), shape=(n, n))
    return M, deg > 0


def components(n, edges):
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import connected_components
    if len(edges) == 0:
        return np.arange(n)
    A = csr_matrix((np.ones(len(edges)), (edges[:, 0], edges[:, 1])), shape=(n, n))
    return connected_components(A, directed=False)[1]


# ---- the body ------------------------------------------------------------------------------------------------------

def dense_weights(body, names=None):
    """(N, B) float64 weights and the bone names of the columns (the body's weighted bones, sorted)."""
    names = sorted(body.weights) if names is None else list(names)
    col = {b: j for j, b in enumerate(names)}
    W = np.zeros((len(body.verts), len(names)))
    for b, (idx, w) in body.weights.items():
        if b in col:
            np.add.at(W[:, col[b]], idx, w)
    return W, names


def match_check(full, body, mm=MATCH_MM, rot=MATCH_ROT, wtol=MATCH_W):
    """The section 1 check: full (the weights body) against body (the Body file the passed garments were bound on)."""
    from scipy.spatial import cKDTree
    rep = {"tolerances": {"boneMm": mm, "rotation": rot, "weight": wtol, "pointMm": mm}}
    a, b = set(full.bones), set(body.bones)
    rep["bones"] = {"full": len(a), "body": len(b), "onlyFull": sorted(a - b)[:20], "onlyBody": sorted(b - a)[:20]}
    worst_t, worst_r, worst_bone = 0.0, 0.0, None
    for nm in sorted(a & b):
        dt = 1000.0 * float(np.abs(full.bones[nm][:3, 3] - body.bones[nm][:3, 3]).max())
        dr = float(np.abs(full.bones[nm][:3, :3] - body.bones[nm][:3, :3]).max())
        if dt > worst_t and dt > 0:
            worst_bone = nm
        worst_t, worst_r = max(worst_t, dt), max(worst_r, dr)
    parents_same = all(full.parent.get(n) == body.parent.get(n) for n in a & b)
    rep["bones"].update({"worstMm": round(worst_t, 6), "worstRotation": float("%.3g" % worst_r), "worstBone": worst_bone,
                         "parentsSame": parents_same})
    d, j = cKDTree(full.verts).query(body.verts)
    found = d * 1000.0 <= mm
    rep["points"] = {"body": int(len(body.verts)), "foundOnFull": int(found.sum()),
                     "worstFoundMm": round(1000.0 * float(d[found].max()) if found.any() else 0.0, 6),
                     "nearestMissMm": round(1000.0 * float(d[~found].min()), 3) if (~found).any() else None}
    names = sorted(set(full.weights) | set(body.weights))
    Wf, _ = dense_weights(full, names)
    Wb, _ = dense_weights(body, names)
    diff = np.abs(Wf[j[found]] - Wb[found])
    per_point = diff.max(axis=1) if diff.size else np.zeros(0)
    rep["weights"] = {"pointsCompared": int(found.sum()), "worst": float("%.3g" % (per_point.max() if per_point.size else 0.0)),
                      "pointsOver": int(np.sum(per_point > wtol)),
                      "bonesOnlyFull": sorted(set(full.weights) - set(body.weights))[:40],
                      "bonesOnlyBody": sorted(set(body.weights) - set(full.weights))[:40]}
    if per_point.size and per_point.max() > wtol:
        k = int(np.argmax(per_point))
        bone = names[int(np.argmax(diff[k]))]
        rep["weights"]["worstAt"] = {"bodyPoint": int(np.nonzero(found)[0][k]), "bone": bone}
    fails = []
    if a != b:
        fails.append("bone names differ")
    if not parents_same:
        fails.append("bone tree differs")
    if worst_t > mm or worst_r > rot:
        fails.append("bind matrices differ (%.4f mm, %.2g)" % (worst_t, worst_r))
    if not found.all():
        fails.append("%d Body points not on the full body" % int((~found).sum()))
    if per_point.size and per_point.max() > wtol:
        fails.append("%d shared points' weights differ by over %.3f" % (int(np.sum(per_point > wtol)), wtol))
    rep["pass"] = not fails
    rep["fails"] = fails
    return rep


# ---- step 2: the copy (bind_garment.py) -------------------------------------------------------------------------

def _tri_normals(V, T):
    n = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    ln = np.linalg.norm(n, axis=1, keepdims=True)
    ln[ln == 0] = 1.0
    return n / ln


def bind(body, g, reach=REACH, angle=ANGLE, panels=True, keep_correctives=True, log=None):
    """bind_garment.py's weights for every garment point: (G (N, B), bone names, reliable (N,))."""
    log = {} if log is None else log
    W, names = dense_weights(body)
    col = {b: j for j, b in enumerate(names)}
    n = len(g.verts)
    nrm = point_normals(g)
    # pieces as sleeves or trunk
    kinds = ("arm_l", "arm_r", "trunk")
    mask = {k: np.zeros(n) for k in kinds}
    use_panels = panels and g.face_piece is not None and np.any(g.face_piece >= 0)
    if use_panels:
        sh = {s: body.joint("upperarm_" + s) for s in "lr"}
        mid = (sh["l"] + sh["r"]) / 2
        side = (sh["l"] - sh["r"]) / np.linalg.norm(sh["l"] - sh["r"])
        half = np.linalg.norm(sh["l"] - mid)
        npieces = int(g.face_piece.max()) + 1
        fcentre = np.array([g.verts[ids].mean(axis=0) for ids in g.faces()])
        kind_of, plog = [], []
        for i in range(npieces):
            fs = g.face_piece == i
            if not fs.any():
                kind_of.append("trunk")
                continue
            across = float((fcentre[fs].mean(axis=0) - mid) @ side / half)
            kd = "arm_l" if across > SLEEVE_ACROSS else "arm_r" if across < -SLEEVE_ACROSS else "trunk"
            kind_of.append(kd)
            plog.append([int(fs.sum()), kd])
        log["panels"] = plog
        for f, ids in enumerate(g.faces()):
            p = g.face_piece[f]
            if p >= 0:
                mask[kind_of[p]][ids] = 1.0
    log["byPanel"] = bool(use_panels)
    # the body's surface split into the arms' and the trunk's
    chain = {s: [col[b] for b in body.subtree("upperarm_" + s) if b in col] for s in "lr"}
    arm_share = {s: W[:, chain[s]].sum(axis=1) for s in "lr"}
    kept = set()
    if keep_correctives:
        for s in "lr":
            r = "upperarm_correctiveRoot_" + s
            if r in body.bones:
                kept |= set(body.subtree(r))
    not_trunk = [j for j in chain["l"] + chain["r"] if names[j] not in kept]
    log["keepCorrectives"] = sorted(kept)
    T = body.tris
    al, ar = arm_share["l"][T].mean(axis=1), arm_share["r"][T].mean(axis=1)
    tri_kind = np.where(al >= 0.5, 0, np.where(ar >= 0.5, 1, 2))
    tnorm = _tri_normals(body.verts, T)

    def copy_from(kd, pts, pnorm):
        sel = np.arange(len(T)) if kd == "all" else np.nonzero(tri_kind == kinds.index(kd))[0]
        if len(sel) == 0 or len(pts) == 0:
            return np.zeros((len(pts), len(names))), np.full(len(pts), 1e9), np.zeros(len(pts))
        w, dist, ti = bend_back.transfer(body.verts, T[sel], W, pts, k=32)
        if kd == "trunk":
            w[:, not_trunk] = 0.0
        facing = np.abs(np.einsum("ij,ij->i", pnorm, tnorm[sel[ti]]))
        return w, dist, facing

    G = np.zeros((n, len(names)))
    ok = np.ones(n, bool)
    cos_limit = math.cos(math.radians(angle))
    if use_panels:
        ml, mr, mt = mask["arm_l"], mask["arm_r"], mask["trunk"]
        sleeve = np.where(ml >= mr, 0, 1)
        ms = np.maximum(ml, mr)
        two = (ms > 0.25) & (mt > 0.25)
        single_sleeve = ~two & (ms > mt)
        jobs = []      # (kind, point ids, share)
        for s in (0, 1):
            jobs.append((kinds[s], np.nonzero(two & (sleeve == s))[0], ms))
            jobs.append((kinds[s], np.nonzero(single_sleeve & (sleeve == s))[0], None))
        jobs.append(("trunk", np.nonzero(two)[0], mt))
        jobs.append(("trunk", np.nonzero(~two & ~single_sleeve)[0], None))
        log["seamPoints"] = int(two.sum())
    else:
        jobs = [("all", np.arange(n), None)]
        log["seamPoints"] = 0
    for kd, ids, share in jobs:
        if len(ids) == 0:
            continue
        w, dist, facing = copy_from(kd, g.verts[ids], nrm[ids])
        s = w.sum(axis=1)
        good = s > 1e-6
        sh = np.ones(len(ids)) if share is None else share[ids]
        G[ids[good]] += sh[good, None] * w[good] / s[good, None]
        ok[ids[~good]] = False
        ok[ids] &= (dist <= reach) & (facing >= cos_limit)
    reliable = ok & (G.sum(axis=1) > 1e-6)
    log["reliable"] = int(reliable.sum())
    log["inpainted"] = int(n - reliable.sum())
    # the repair, then the light smoothing, the cap
    M, has = neighbours_matrix(n, g.edges())
    unrel = np.nonzero(~reliable & has)[0]
    if len(unrel) and reliable.any():
        Mu = M[unrel]
        for _ in range(INPAINT_ROUNDS):
            G[unrel] = Mu @ G
    for _ in range(SMOOTH_ROUNDS):
        S = M @ G
        G = np.where(has[:, None], 0.5 * G + 0.5 * S, G)
    G = cap_normalise(G, MAX_INFLUENCES)
    G[G <= KEEP_MIN] = 0.0
    used = [names[j] for j in range(len(names)) if G[:, j].max() > KEEP_MIN]
    log["bones"] = len(used)
    return G, names, reliable


def cap_normalise(W, keep):
    W = W.copy()
    if W.shape[1] > keep:
        cut = np.argsort(W, axis=1, kind="stable")[:, :-keep]
        np.put_along_axis(W, cut, 0.0, axis=1)
    s = W.sum(axis=1, keepdims=True)
    s[s == 0] = 1.0
    return W / s


# ---- step 2: the joints (skin_garment.py's trouser rules) ---------------------------------------------------------

def parse_sides(spec, g):
    """'R:L' (piece numbers or OBJ group names, comma separated) as (set, set) of piece numbers."""
    r, l = spec.split(":")

    def one(txt):
        out = set()
        for t in txt.split(","):
            t = t.strip()
            if not t:
                continue
            out.add(int(t) if t.lstrip("-").isdigit() else g.piece_names.index(t))
        return out
    return one(r), one(l)


def auto_sides(g, body):
    """Leg pieces: reaching below the knees (the calf joints); right when their centre lies on the right of the pelvis
    (x below it: the body faces -y). Returns (right set, left set)."""
    knee_z = (body.joint("calf_l")[2] + body.joint("calf_r")[2]) / 2
    mid_x = body.joint("pelvis")[0]
    R, L = set(), set()
    fcentre = np.array([g.verts[ids].mean(axis=0) for ids in g.faces()])
    for p in range(int(g.face_piece.max()) + 1 if g.n_faces else 0):
        fs = g.face_piece == p
        if not fs.any():
            continue
        ids = np.unique(np.concatenate([ids for f, ids in enumerate(g.faces()) if fs[f]]))
        if g.verts[ids, 2].min() >= knee_z:
            continue
        (R if fcentre[fs].mean(axis=0)[0] < mid_x else L).add(p)
    return R, L


def point_sides(g, R, L, tags=("r", "l", "x")):
    """Per point the set of sides of the faces round it."""
    out = [set() for _ in range(len(g.verts))]
    for f, ids in enumerate(g.faces()):
        p = g.face_piece[f]
        t = tags[0] if p in R else tags[1] if p in L else tags[2]
        for i in ids:
            out[i].add(t)
    return out


def correct(body, g, G, names, leg_sides=None, crotch_fade=0.0, centre_seam=None, max_influences=MAX_INFLUENCES, log=None):
    """skin_garment.py's rules after the binder, in its order (the skirt rule off, as --no-skirt)."""
    from scipy.spatial import cKDTree
    log = {} if log is None else log
    names = list(names)
    col = {b: j for j, b in enumerate(names)}
    W = G.copy()

    def ensure(b):
        nonlocal W
        if b not in col:
            col[b] = len(names)
            names.append(b)
            W = np.hstack([W, np.zeros((len(W), 1))])
        return col[b]
    P = g.verts
    edges = g.edges()
    comp = components(len(P), edges)
    main = np.bincount(comp).argmax() if len(comp) else 0
    pelvis = ensure("pelvis")
    log["skirt"] = {"off": True}
    if leg_sides is not None:
        R2, L2 = leg_sides
        leg_of = {"l": set(body.subtree("thigh_l")), "r": set(body.subtree("thigh_r"))}
        vside = point_sides(g, R2, L2)
        swapped, moved_w = 0, 0.0
        for own, other in (("r", "l"), ("l", "r")):
            pairs = [(col[nm], ensure(nm[:-2] + "_" + own)) for nm in list(names)
                     if nm in leg_of[other] and nm.endswith("_" + other) and (nm[:-2] + "_" + own) in body.bones]
            if not pairs:
                continue
            ids = np.array([i for i, s in enumerate(vside) if s == {own}], dtype=np.int64)
            if not len(ids):
                continue
            a = np.array([p[0] for p in pairs])
            b = np.array([p[1] for p in pairs])
            w = W[ids][:, a].sum(axis=1)
            hit = ids[w > 1e-6]
            for aj, bj in pairs:
                W[hit, bj] += W[hit, aj]
                W[hit, aj] = 0.0
            swapped += len(hit)
            moved_w += float(w[w > 1e-6].sum())
        log["legSides"] = {"right": sorted(int(x) for x in R2), "left": sorted(int(x) for x in L2),
                           "pointsSwapped": swapped, "meanWeightMoved": round(moved_w / max(swapped, 1), 3)}
    if crotch_fade > 0 and centre_seam is not None:
        R, L = centre_seam
        sides = point_sides(g, R, L, tags=("R", "L", ""))
        seam = np.array([i for i, s in enumerate(sides) if "R" in s and "L" in s], dtype=np.int64)
        thigh = [col[nm] for nm in names if nm.startswith("thigh")]
        faded, given = 0, 0.0
        if len(seam):
            d, _ = cKDTree(P[seam]).query(P)
            x = 1.0 - d / crotch_fade
            t = x * x * (3 - 2 * x)
            th = W[:, thigh].sum(axis=1)
            hit = (d < crotch_fade) & (th > 0)
            W[hit, pelvis] += t[hit] * th[hit]
            W[np.ix_(hit, thigh)] *= (1 - t[hit])[:, None]
            faded, given = int(hit.sum()), float((t[hit] * th[hit]).sum())
        log["crotch"] = {"fadeM": crotch_fade, "seamPoints": int(len(seam)), "pointsFaded": faded,
                         "meanThighShareGiven": round(given / max(faded, 1), 3),
                         "seamZ": [round(float(P[seam, 2].min()), 3), round(float(P[seam, 2].max()), 3)] if len(seam) else None}
    # loose pieces inside the shoulders carry no arm
    arm_bones = set(body.subtree("upperarm_l")) | set(body.subtree("upperarm_r"))
    for s in "lr":
        if "upperarm_correctiveRoot_" + s in body.bones:
            arm_bones |= set(body.subtree("upperarm_correctiveRoot_" + s))
    arm_cols = [col[nm] for nm in names if nm in arm_bones]
    shoulder_x = min(abs(body.joint("upperarm_l")[0]), abs(body.joint("upperarm_r")[0]))
    loose = np.nonzero(comp != main)[0]
    pieces_ids = np.array([i for i in loose if abs(P[comp == comp[i]].mean(axis=0)[0]) < shoulder_x], dtype=np.int64)
    spine5 = ensure("spine_05")
    if len(pieces_ids) and arm_cols:
        W[np.ix_(pieces_ids, arm_cols)] = 0.0
        empty = pieces_ids[W[pieces_ids].sum(axis=1) < 1e-6]
        W[empty, spine5] = 1.0
    log["loosePiecePoints"] = int(len(pieces_ids))
    # no head or face bones
    face = [col[nm] for nm in names if nm == "head" or nm.startswith(("FACIAL", "facial", "head_"))]
    neck2 = col.get("neck_02", col.get("neck_01"))
    if face and neck2 is not None:
        W[:, neck2] += W[:, face].sum(axis=1)
        W[:, face] = 0.0
    log["headWeightsMoved"] = len(face)
    # the loose pieces smoothed over themselves
    if len(pieces_ids):
        M, has = neighbours_matrix(len(P), edges)
        for _ in range(COLLAR_SMOOTH):
            S = M @ W
            W[pieces_ids] = np.where(has[pieces_ids, None], 0.5 * W[pieces_ids] + 0.5 * S[pieces_ids], W[pieces_ids])
    W = cap_normalise(W, max_influences)
    W[W <= KEEP_MIN] = 0.0
    log["maxInfluences"] = int((W > 0).sum(axis=1).max()) if len(W) else 0
    return W, names


# ---- comparison ----------------------------------------------------------------------------------------------------

def compare(W, names, ref):
    """Per point, half the sum of absolute weight differences over all bones (0 the same, 1 nothing shared), against
    a fbx_skin.Skinned with the same points."""
    allnames = sorted(set(names) | set(ref.weights))
    A = np.zeros((len(W), len(allnames)))
    ci = {b: j for j, b in enumerate(allnames)}
    for j, b in enumerate(names):
        A[:, ci[b]] = W[:, j]
    B, _ = dense_weights(ref, allnames)
    if len(B) != len(A):
        raise ValueError("the accepted garment has %d points, this one %d" % (len(B), len(A)))
    tv = 0.5 * np.abs(A - B).sum(axis=1)
    top = np.argmax(A, axis=1) == np.argmax(B, axis=1)
    per_bone = {allnames[j]: round(float(np.abs(A[:, j] - B[:, j]).max()), 4) for j in range(len(allnames))
                if np.abs(A[:, j] - B[:, j]).max() > 0.05}
    return {"points": int(len(tv)), "tvMedian": round(float(np.median(tv)), 5), "tvMean": round(float(tv.mean()), 5),
            "tvP95": round(float(np.percentile(tv, 95)), 4), "tvP99": round(float(np.percentile(tv, 99)), 4),
            "tvMax": round(float(tv.max()), 4), "pointsOver0p05": int(np.sum(tv > 0.05)),
            "pointsOver0p2": int(np.sum(tv > 0.2)), "sameTopBone": round(float(top.mean()), 4),
            "bonesDifferingOver0p05": dict(sorted(per_bone.items(), key=lambda kv: -kv[1])[:12]), "tv": tv}


# ---- the FBX writer ------------------------------------------------------------------------------------------------
# Binary FBX 7.4 written from the format's published layout (node records of three uint32, a 13-byte null record
# closing every nested list, zlib arrays); the header, file id, creation time and footer constants are the format's
# own (the values every FBX file carries for the SDK's check).

_HEAD = b"Kaydara FBX Binary  \x00\x1a\x00"
_FILE_ID = b"\x28\xb3\x2a\xeb\xb6\x24\xcc\xc2\xbf\xc8\xb0\x2a\xa9\x2b\xfc\xf1"
_TIME_ID = b"1970-01-01 10:00:00:000"
_FOOT_ID = b"\xfa\xbc\xab\x09\xd0\xc8\xd4\x66\xb1\x76\xfb\x83\x1c\xf7\x26\x7e"
_FOOT_MAGIC = b"\xf8\x5a\x8c\x6a\xde\xf5\xd9\x7e\xec\xe9\x0c\xe3\x75\x8f\x29\x0b"
_VERSION = 7400


class N:
    """A node: name, properties (python values; tagged tuples for typed ones), children."""

    def __init__(self, name, *props, kids=None):
        self.name, self.props, self.kids = name, list(props), list(kids or [])

    def add(self, *nodes):
        self.kids.extend(nodes)
        return self


def I32(v):
    return ("I", int(v))


def I64(v):
    return ("L", int(v))


def _prop(v):
    if isinstance(v, tuple) and len(v) == 2 and v[0] in ("I", "L", "D", "C", "R"):
        k, x = v
        if k == "I":
            return b"I" + struct.pack("<i", x)
        if k == "L":
            return b"L" + struct.pack("<q", x)
        if k == "D":
            return b"D" + struct.pack("<d", x)
        if k == "C":
            return b"C" + struct.pack("<?", x)
        return b"R" + struct.pack("<I", len(x)) + x
    if isinstance(v, bool):
        return b"C" + struct.pack("<?", v)
    if isinstance(v, int):
        return b"I" + struct.pack("<i", v)
    if isinstance(v, float):
        return b"D" + struct.pack("<d", v)
    if isinstance(v, (bytes, str)):
        b = v.encode("utf-8") if isinstance(v, str) else v
        return b"S" + struct.pack("<I", len(b)) + b
    if isinstance(v, np.ndarray):
        code = {np.dtype(np.float64): b"d", np.dtype(np.float32): b"f", np.dtype(np.int32): b"i",
                np.dtype(np.int64): b"l"}[v.dtype]
        raw = np.ascontiguousarray(v).astype(v.dtype.newbyteorder("<")).tobytes()
        if len(raw) > 128:
            data = zlib.compress(raw, 6)
            return code + struct.pack("<3I", v.size, 1, len(data)) + data
        return code + struct.pack("<3I", v.size, 0, len(raw)) + raw
    raise TypeError("no FBX property for %r" % type(v))


def _encode(node, offset):
    props = b"".join(_prop(p) for p in node.props)
    name = node.name.encode("ascii")
    head_len = 13 + len(name) + len(props)
    body = b""
    pos = offset + head_len
    for k in node.kids:
        b = _encode(k, pos)
        body += b
        pos += len(b)
    if node.kids or not node.props:
        body += b"\x00" * 13
    end = offset + head_len + len(body)
    return struct.pack("<3I", end, len(node.props), len(props)) + bytes([len(name)]) + name + props + body


def write_fbx(path, nodes):
    out = bytearray(_HEAD + struct.pack("<I", _VERSION))
    for n in nodes:
        out += _encode(n, len(out))
    out += b"\x00" * 13
    out += _FOOT_ID + b"\x00" * 4
    pad = ((len(out) + 15) & ~15) - len(out)
    out += b"\x00" * (pad or 16)
    out += struct.pack("<I", _VERSION) + b"\x00" * 120 + _FOOT_MAGIC
    with open(path, "wb") as f:
        f.write(bytes(out))


def _p(name, kind, label, flags, *vals):
    return N("P", name, kind, label, flags, *vals)


def _p70(*ps):
    return N("Properties70", kids=list(ps))


def euler_xyz(R):
    """Degrees (x, y, z) with R = Rz Ry Rx (FBX's default rotation order, column vectors)."""
    sy = -R[2, 0]
    if abs(sy) < 1 - 1e-12:
        y = math.asin(max(-1.0, min(1.0, sy)))
        x = math.atan2(R[2, 1], R[2, 2])
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        y = math.copysign(math.pi / 2, sy)
        x = math.atan2(-R[1, 2], R[1, 1])
        z = 0.0
    return [math.degrees(x), math.degrees(y), math.degrees(z)]


def rot_xyz(deg):
    x, y, z = (math.radians(d) for d in deg)
    Rx = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])
    Ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    Rz = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def _arr16(M):
    return np.ascontiguousarray(np.asarray(M, dtype=float).T).reshape(16)


def write_skinned_fbx(path, g, bones, parent, W, names, mesh_name="garment"):
    """The garment's points and polygons, its UV layers, the skeleton (bones {name: 4x4 world, metres, Blender's
    frame}, parent {name: parent}) and the weights W (N, B) on bone columns `names`, as a skinned binary FBX in
    centimetres (z up, facing -y, as 3ds Max writes). The mesh sits at the origin unturned; each bone's local
    transform matches its bind pose."""
    S = 100.0
    uid = [1000000]

    def new_id():
        uid[0] += 1
        return uid[0]
    order, seen = [], set()

    def visit(b):
        if b in seen:
            return
        if parent.get(b) in bones:
            visit(parent[b])
        seen.add(b)
        order.append(b)
    for b in sorted(bones):
        visit(b)
    world = {b: np.array(bones[b], dtype=float) for b in order}
    for b in order:
        world[b] = world[b].copy()
        world[b][:3, 3] *= S
    objects, conns = [], []
    mesh_id, geo_id, skin_id = new_id(), new_id(), new_id()
    # geometry
    pvi = g.corners.astype(np.int32).copy()
    last = g.poly_start[1:] - 1
    pvi[last] = -pvi[last] - 1
    geo = N("Geometry", I64(geo_id), mesh_name + "\x00\x01Geometry", "Mesh", kids=[
        _p70(), N("GeometryVersion", I32(124)),
        N("Vertices", np.ascontiguousarray(g.verts * S, dtype=np.float64).reshape(-1)),
        N("PolygonVertexIndex", pvi)])
    layer = N("Layer", I32(0), kids=[N("Version", I32(100))])
    for li, (uvname, uv, idx) in enumerate(g.uv_layers):
        geo.add(N("LayerElementUV", I32(li), kids=[
            N("Version", I32(101)), N("Name", uvname), N("MappingInformationType", "ByPolygonVertex"),
            N("ReferenceInformationType", "IndexToDirect"), N("UV", np.ascontiguousarray(uv, dtype=np.float64).reshape(-1)),
            N("UVIndex", np.ascontiguousarray(idx, dtype=np.int32))]))
    geo.add(N("LayerElementMaterial", I32(0), kids=[
        N("Version", I32(101)), N("Name", ""), N("MappingInformationType", "AllSame"),
        N("ReferenceInformationType", "IndexToDirect"), N("Materials", np.zeros(1, dtype=np.int32))]))
    layer.add(N("LayerElement", kids=[N("Type", "LayerElementMaterial"), N("TypedIndex", I32(0))]))
    if g.uv_layers:
        layer.add(N("LayerElement", kids=[N("Type", "LayerElementUV"), N("TypedIndex", I32(0))]))
    geo.add(layer)
    for li in range(1, len(g.uv_layers)):
        geo.add(N("Layer", I32(li), kids=[N("Version", I32(100)), N("LayerElement", kids=[
            N("Type", "LayerElementUV"), N("TypedIndex", I32(li))])]))
    objects.append(geo)
    objects.append(N("Model", I64(mesh_id), mesh_name + "\x00\x01Model", "Mesh", kids=[
        N("Version", I32(232)), _p70(_p("DefaultAttributeIndex", "int", "Integer", "", I32(0)),
                                     _p("InheritType", "enum", "", "", I32(1))),
        N("Shading", ("C", True)), N("Culling", "CullingOff")]))
    mat_id = new_id()
    objects.append(N("Material", I64(mat_id), mesh_name + "_material\x00\x01Material", "", kids=[
        N("Version", I32(102)), N("ShadingModel", "lambert"), N("MultiLayer", I32(0)), _p70()]))
    conns += [(mesh_id, 0), (geo_id, mesh_id), (mat_id, mesh_id)]
    # bones
    bone_id = {}
    for b in order:
        bid, aid = new_id(), new_id()
        bone_id[b] = bid
        pa = parent.get(b) if parent.get(b) in world else None
        local = np.linalg.inv(world[pa]) @ world[b] if pa else world[b]
        t, r = local[:3, 3], euler_xyz(local[:3, :3])
        objects.append(N("NodeAttribute", I64(aid), b + "\x00\x01NodeAttribute", "LimbNode", kids=[
            _p70(_p("Size", "double", "Number", "", ("D", 1.0))), N("TypeFlags", "Skeleton")]))
        objects.append(N("Model", I64(bid), b + "\x00\x01Model", "LimbNode", kids=[
            N("Version", I32(232)), _p70(
                _p("InheritType", "enum", "", "", I32(1)), _p("DefaultAttributeIndex", "int", "Integer", "", I32(0)),
                _p("Lcl Translation", "Lcl Translation", "", "A", *[("D", float(x)) for x in t]),
                _p("Lcl Rotation", "Lcl Rotation", "", "A", *[("D", float(x)) for x in r]),
                _p("Lcl Scaling", "Lcl Scaling", "", "A", ("D", 1.0), ("D", 1.0), ("D", 1.0))),
            N("Shading", ("C", True)), N("Culling", "CullingOff")]))
        conns += [(aid, bid), (bid, bone_id[pa] if pa else 0)]
    # skin and clusters
    objects.append(N("Deformer", I64(skin_id), "\x00\x01Deformer", "Skin", kids=[
        N("Version", I32(101)), N("Link_DeformAcuracy", ("D", 50.0))]))
    conns.append((skin_id, geo_id))
    used = 0
    for j, b in enumerate(names):
        if b not in bone_id:
            if np.any(W[:, j] > 0):
                raise ValueError("weights on %s, which the skeleton lacks" % b)
            continue
        ix = np.nonzero(W[:, j] > 0)[0]
        if not len(ix):
            continue
        cid = new_id()
        objects.append(N("Deformer", I64(cid), b + "\x00\x01SubDeformer", "Cluster", kids=[
            N("Version", I32(100)), N("UserData", "", ""),
            N("Indexes", ix.astype(np.int32)), N("Weights", W[ix, j].astype(np.float64)),
            N("Transform", _arr16(np.linalg.inv(world[b]))), N("TransformLink", _arr16(world[b]))]))
        conns += [(cid, skin_id), (bone_id[b], cid)]
        used += 1
    pose_nodes = [N("PoseNode", kids=[N("Node", I64(mesh_id)), N("Matrix", _arr16(np.eye(4)))])]
    pose_nodes += [N("PoseNode", kids=[N("Node", I64(bone_id[b])), N("Matrix", _arr16(world[b]))]) for b in order]
    objects.append(N("Pose", I64(new_id()), "BindPose\x00\x01Pose", "BindPose", kids=[
        N("Type", "BindPose"), N("Version", I32(100)), N("NbPoseNodes", I32(len(pose_nodes)))] + pose_nodes))
    counts = {"Model": 1 + len(order), "Geometry": 1, "Material": 1, "NodeAttribute": len(order), "Deformer": 1 + used, "Pose": 1}
    defs = N("Definitions", kids=[N("Version", I32(100)), N("Count", I32(sum(counts.values()) + 1)),
                                  N("ObjectType", "GlobalSettings", kids=[N("Count", I32(1))])] +
             [N("ObjectType", k, kids=[N("Count", I32(v))]) for k, v in counts.items()])
    gs = N("GlobalSettings", kids=[N("Version", I32(1000)), _p70(
        _p("UpAxis", "int", "Integer", "", I32(2)), _p("UpAxisSign", "int", "Integer", "", I32(1)),
        _p("FrontAxis", "int", "Integer", "", I32(1)), _p("FrontAxisSign", "int", "Integer", "", I32(-1)),
        _p("CoordAxis", "int", "Integer", "", I32(0)), _p("CoordAxisSign", "int", "Integer", "", I32(1)),
        _p("OriginalUpAxis", "int", "Integer", "", I32(2)), _p("OriginalUpAxisSign", "int", "Integer", "", I32(1)),
        _p("UnitScaleFactor", "double", "Number", "", ("D", 1.0)),
        _p("OriginalUnitScaleFactor", "double", "Number", "", ("D", 1.0)))])
    header = N("FBXHeaderExtension", kids=[
        N("FBXHeaderVersion", I32(1003)), N("FBXVersion", I32(_VERSION)), N("EncryptionType", I32(0)),
        N("CreationTimeStamp", kids=[N("Version", I32(1000))] + [N(k, I32(v)) for k, v in (
            ("Year", 1970), ("Month", 1), ("Day", 1), ("Hour", 10), ("Minute", 0), ("Second", 0), ("Millisecond", 0))]),
        N("Creator", "LEDGER tools/md/skin_transfer.py")])
    conn_node = N("Connections", kids=[N("C", "OO", I64(a), I64(b)) for a, b in conns])
    write_fbx(path, [header, N("FileId", ("R", _FILE_ID)), N("CreationTime", _TIME_ID),
                     N("Creator", "LEDGER tools/md/skin_transfer.py"), gs,
                     N("Documents", kids=[N("Count", I32(1)), N("Document", I64(new_id()), "", "Scene", kids=[
                         _p70(), N("RootNode", I64(0))])]),
                     N("References"), defs, N("Objects", kids=objects), conn_node,
                     N("Takes", kids=[N("Current", "")])])
    return {"bones": len(order), "clusters": used}


# ---- the run -------------------------------------------------------------------------------------------------------

def sha16(path):
    return bend_back.sha16(path)


def skin(body, g, pieces="auto", reach=REACH, angle=ANGLE, panels=True, keep_correctives=True, leg_sides=None,
         crotch_fade=0.0, centre_seam=None, max_influences=MAX_INFLUENCES):
    """The whole step on loaded inputs: (W (N, B), bone names, log). leg_sides / centre_seam: None, 'auto', 'R:L'
    or a (set, set)."""
    log = {"reach": reach, "angle": angle}
    log["pieces"] = set_pieces(g, pieces)
    binder = {}
    G, names, _ = bind(body, g, reach=reach, angle=angle, panels=panels, keep_correctives=keep_correctives, log=binder)
    log["binder"] = binder

    def sides(v):
        if v is None:
            return None
        if v == "auto":
            return auto_sides(g, body)
        if isinstance(v, str):
            return parse_sides(v, g)
        return v
    W, names = correct(body, g, G, names, leg_sides=sides(leg_sides), crotch_fade=crotch_fade,
                       centre_seam=sides(centre_seam), max_influences=max_influences, log=log)
    return W, names, log


def run(weights_body, garment, out_dir, name, match_body=None, compare_to=None, **kw):
    os.makedirs(out_dir, exist_ok=True)
    rep = {"tool": "tools/md/skin_transfer.py", "weightsBody": weights_body.replace("\\", "/"),
           "weightsBodySha256_16": sha16(weights_body), "garment": garment.replace("\\", "/"),
           "garmentSha256_16": sha16(garment), "name": name}
    body = fbx_skin.load_skinned(weights_body)
    if match_body:
        rep["match"] = match_check(body, fbx_skin.load_skinned(match_body))
        rep["match"]["bodyFile"] = match_body.replace("\\", "/")
        if not rep["match"]["pass"]:
            _dump(rep, out_dir)
            raise SystemExit("SKIN TRANSFER the weights body does not match %s: %s" % (match_body, "; ".join(rep["match"]["fails"])))
    g = read_garment(garment)
    W, names, log = skin(body, g, **kw)
    rep.update(log)
    rep["points"] = int(len(g.verts))
    out_fbx = os.path.join(out_dir, name + "_skinned.fbx")
    rep["fbx"] = write_skinned_fbx(out_fbx, g, body.bones, body.parent, W, names, mesh_name=name)
    rep["fbx"]["path"] = out_fbx.replace("\\", "/")
    used = [j for j in range(len(names)) if W[:, j].max() > 0]
    np.savez_compressed(os.path.join(out_dir, name + "_weights.npz"), W=W[:, used].astype(np.float32),
                        names=np.array([names[j] for j in used]))
    rep["bones"] = [names[j] for j in used]
    if compare_to:
        ref = fbx_skin.load_skinned(compare_to)
        off = float(np.abs(ref.verts - g.verts).max()) if len(ref.verts) == len(g.verts) else None
        c = compare(W, names, ref)
        c.pop("tv")
        c["accepted"] = compare_to.replace("\\", "/")
        c["pointMismatchMm"] = None if off is None else round(1000 * off, 4)
        rep["compare"] = c
    _dump(rep, out_dir)
    print("SKIN TRANSFER " + json.dumps({k: rep.get(k) for k in ("points", "pieces", "legSides", "crotch", "compare")})[:900], flush=True)
    return rep


def _dump(rep, out_dir):
    with open(os.path.join(out_dir, "skin.json"), "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=1)


def main(argv):
    if "--selftest" in argv:
        import unittest
        suite = unittest.defaultTestLoader.loadTestsFromName("test_skin_transfer")
        res = unittest.TextTestRunner(verbosity=1).run(suite)
        n, bad = res.testsRun, len(res.failures) + len(res.errors)
        print("skin_transfer selftest: passed=%d/%d failed=%d" % (n - bad, n, bad))
        return 0 if res.wasSuccessful() else 4
    if "--match" in argv:
        i = argv.index("--match")
        rep = match_check(fbx_skin.load_skinned(argv[i + 1]), fbx_skin.load_skinned(argv[i + 2]))
        print("MATCH " + json.dumps(rep))
        return 0 if rep["pass"] else 3
    valued = ("--match-body", "--reach", "--angle", "--pieces", "--leg-sides", "--crotch-fade", "--centre-seam",
              "--max-influences", "--compare")
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
    if len(pos) != 4:
        print(__doc__)
        return 2
    run(pos[0], pos[1], pos[2], pos[3], match_body=opt("--match-body"), compare_to=opt("--compare"),
        pieces=opt("--pieces", "auto"), reach=float(opt("--reach", REACH)), angle=float(opt("--angle", ANGLE)),
        panels="--no-panels" not in argv, keep_correctives="--no-keep-correctives" not in argv,
        leg_sides=opt("--leg-sides"), crotch_fade=float(opt("--crotch-fade", 0.0)), centre_seam=opt("--centre-seam"),
        max_influences=int(opt("--max-influences", MAX_INFLUENCES)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
