"""Unit tests for tools/md/skin_transfer.py on synthetic meshes (no files of the project are read or written; temporary
files only).

    python -m unittest tools/md/test_skin_transfer.py      (or: python tools/md/skin_transfer.py --selftest)

The synthetic body (Blender's frame: metres, z up, facing -y, the left side at +x) is five tubes, a trunk, two legs
and two arms, plus a head tube that only the "full" body has (as MH_RoccoP2_FullBody has the head its Body file
lacks). Bones: root, pelvis, spine_05, neck_02, head; per side thigh, thigh_twist_01 under it, calf; upperarm, the
correctives' root and upperarm_fwd under it, lowerarm.
"""
import math
import os
import sys
import tempfile
import unittest

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import fbx_skin  # noqa: E402
import skin_transfer as stf  # noqa: E402
from test_bend_back import lerp_path, tube  # noqa: E402

POS = {"root": (0, 0, 0), "pelvis": (0, 0, 1.0), "spine_05": (0, 0, 1.4), "neck_02": (0, 0, 1.5), "head": (0, 0, 1.6)}
PARENT = {"pelvis": "root", "spine_05": "pelvis", "neck_02": "spine_05", "head": "neck_02"}
for _s, _x in (("l", 1.0), ("r", -1.0)):
    POS.update({"thigh_" + _s: (0.1 * _x, 0, 0.95), "thigh_twist_01_" + _s: (0.1 * _x, 0, 0.75),
                "calf_" + _s: (0.1 * _x, 0, 0.5), "upperarm_" + _s: (0.2 * _x, 0, 1.4),
                "upperarm_correctiveRoot_" + _s: (0.2 * _x, 0, 1.4), "upperarm_fwd_" + _s: (0.22 * _x, -0.03, 1.4),
                "lowerarm_" + _s: (0.45 * _x, 0, 1.4)})
    PARENT.update({"thigh_" + _s: "pelvis", "thigh_twist_01_" + _s: "thigh_" + _s, "calf_" + _s: "thigh_" + _s,
                   "upperarm_" + _s: "spine_05", "upperarm_correctiveRoot_" + _s: "upperarm_" + _s,
                   "upperarm_fwd_" + _s: "upperarm_correctiveRoot_" + _s, "lowerarm_" + _s: "upperarm_" + _s})


def bone_mats():
    out = {}
    for i, (b, p) in enumerate(sorted(POS.items())):
        M = np.eye(4)
        a = 0.3 * i
        M[:3, :3] = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
        M[:3, 3] = p
        out[b] = M
    return out


def smooth(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def synthetic_body(full=True, segs=16):
    parts, weights = [], []

    def add(path, r, wfun):
        v, t, _ = tube(path, r, segs)
        parts.append((v, t))
        weights.append(wfun(v))

    def trunk(v):
        up = smooth((v[:, 2] - 1.05) / 0.1)
        return {"spine_05": up, "pelvis": 1 - up}
    add(lerp_path((0, 0, 0.98), (0, 0, 1.5), 14), 0.15, trunk)
    for s, x in (("l", 1.0), ("r", -1.0)):
        def leg(v, s=s):
            th = smooth((v[:, 2] - 0.45) / 0.1)
            tw = th * 0.4 * smooth((0.9 - v[:, 2]) / 0.1)
            return {"thigh_" + s: th - tw, "thigh_twist_01_" + s: tw, "calf_" + s: 1 - th}
        add(lerp_path((0.1 * x, 0, 0.95), (0.1 * x, 0, 0.05), 19), 0.07, leg)

        def armw(v, s=s):
            lo = smooth((np.abs(v[:, 0]) - 0.4) / 0.1)
            fwd = 0.3 * smooth((0.32 - np.abs(v[:, 0])) / 0.05) * (1 - lo)
            return {"upperarm_" + s: 1 - lo - fwd, "upperarm_fwd_" + s: fwd, "lowerarm_" + s: lo}
        add(lerp_path((0.16 * x, 0, 1.4), (0.7 * x, 0, 1.4), 12), 0.05, armw)
    if full:
        add(lerp_path((0, 0, 1.52), (0, 0, 1.75), 5), 0.08, lambda v: {"head": np.ones(len(v))})
    verts, tris, off, W = [], [], 0, {}
    total = sum(len(v) for v, _ in parts)
    for (v, t), w in zip(parts, weights):
        verts.append(v)
        tris.append(t + off)
        for b, x in w.items():
            W.setdefault(b, np.zeros(total))[off:off + len(v)] = x
        off += len(v)
    body = fbx_skin.Skinned()
    body.verts, body.tris = np.concatenate(verts), np.concatenate(tris)
    body.weights = {b: (np.nonzero(x > 1e-9)[0], x[x > 1e-9]) for b, x in W.items() if np.any(x > 1e-9)}
    body.bones, body.parent = bone_mats(), dict(PARENT)
    return body


def quad_garment(path_pts, r, segs=16, piece_of_ring=None):
    """A garment tube of quads round a polyline (one piece unless piece_of_ring(ring) says otherwise)."""
    v, t, ring = tube(path_pts, r, segs)
    g = stf.Garment()
    g.verts = v
    faces, piece = [], []
    for i in range(len(path_pts) - 1):
        for k in range(segs):
            a, b = i * segs + k, i * segs + (k + 1) % segs
            faces.append([a, b, b + segs, a + segs])
            piece.append(0 if piece_of_ring is None else piece_of_ring(i, k))
    g.corners = np.array(faces, dtype=np.int64).reshape(-1)
    g.poly_start = np.arange(0, len(g.corners) + 1, 4, dtype=np.int64)
    g.face_piece = np.array(piece, dtype=np.int64)
    g.piece_names = ["p%d" % i for i in range(int(g.face_piece.max()) + 1)]
    return g


def join(*gs):
    out = stf.Garment()
    vs, cs, ps, fp, off, poff = [], [], [0], [], 0, 0
    for g in gs:
        vs.append(g.verts)
        cs.append(g.corners + off)
        ps.extend((g.poly_start[1:] + poff).tolist())
        fp.append(g.face_piece + (max(fp[-1].max() + 1, 0) if fp else 0))
        off += len(g.verts)
        poff += len(g.corners)
    out.verts, out.corners = np.concatenate(vs), np.concatenate(cs)
    out.poly_start = np.array(ps, dtype=np.int64)
    out.face_piece = np.concatenate(fp)
    out.piece_names = ["p%d" % i for i in range(int(out.face_piece.max()) + 1)]
    return out


def strip_pair():
    """Two flat pieces of quads meeting on a seam at x = 0 (right piece x < 0, left x > 0), at crotch height, facing -y:
    columns at x = -0.15 .. 0.15 by 0.03, rows z = 0.8 .. 1.0 by 0.05."""
    xs = np.round(np.arange(-0.15, 0.1501, 0.03), 6)
    zs = np.arange(0.80, 1.0001, 0.05)
    g = stf.Garment()
    g.verts = np.array([[x, -0.12, z] for z in zs for x in xs])
    nx = len(xs)
    faces, piece = [], []
    for j in range(len(zs) - 1):
        for i in range(nx - 1):
            a = j * nx + i
            faces.append([a, a + 1, a + 1 + nx, a + nx])
            piece.append(0 if xs[i] < 0 else 1)
    g.corners = np.array(faces, dtype=np.int64).reshape(-1)
    g.poly_start = np.arange(0, len(g.corners) + 1, 4, dtype=np.int64)
    g.face_piece = np.array(piece)
    g.piece_names = ["right", "left"]
    return g, xs


class TestEncodingAndRoundTrip(unittest.TestCase):
    def test_euler_round_trip(self):
        rng = np.random.default_rng(1)
        for _ in range(50):
            deg = rng.uniform([-180, -89, -180], [180, 89, 180])
            R = stf.rot_xyz(deg)
            self.assertLess(np.abs(stf.rot_xyz(stf.euler_xyz(R)) - R).max(), 1e-10)
        R = stf.rot_xyz([10, 90, 0])
        self.assertLess(np.abs(stf.rot_xyz(stf.euler_xyz(R)) - R).max(), 1e-9)

    def test_written_fbx_reads_back(self):
        body = synthetic_body()
        g = quad_garment(lerp_path((0, 0, 1.0), (0, 0, 1.45), 8), 0.17)
        g.uv_layers = [("UVMap", np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float), np.tile(np.arange(4), g.n_faces)),
                       ("pattern", np.array([[0, 0], [2, 0], [2, 2], [0, 2]], float), np.tile(np.arange(4), g.n_faces))]
        W, names = stf.dense_weights(body)
        Wg = np.zeros((len(g.verts), len(names)))
        Wg[:, names.index("spine_05")] = np.linspace(0, 1, len(g.verts))
        Wg[:, names.index("pelvis")] = 1 - Wg[:, names.index("spine_05")]
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "g.fbx")
            info = stf.write_skinned_fbx(p, g, body.bones, body.parent, Wg, names, mesh_name="gar")
            self.assertEqual(info["bones"], len(body.bones))
            with open(p, "rb") as f:
                raw = f.read()
            self.assertTrue(raw.startswith(b"Kaydara FBX Binary  \x00\x1a\x00"))
            self.assertTrue(raw.endswith(stf._FOOT_MAGIC))
            back = fbx_skin.load_skinned(p)
            self.assertEqual(back.mesh_name, "gar")
            self.assertLess(np.abs(back.verts - g.verts).max(), 1e-9)
            self.assertEqual(len(back.tris), 2 * g.n_faces)
            self.assertEqual(set(back.bones), set(body.bones))
            for b in body.bones:
                self.assertLess(np.abs(back.bones[b] - body.bones[b]).max(), 1e-9, b)
            self.assertEqual(back.parent, body.parent)
            Wb, nb = stf.dense_weights(back, names)
            self.assertLess(np.abs(Wb - Wg).max(), 1e-12)
            # local transforms agree with the bind pose: compose Lcl down the tree
            root, _ = fbx_skin.parse_fbx(p, max_array=fbx_skin.BIG)
            lcl = {}
            for n in root.find("Objects").children:
                if n.name == "Model" and n.props[2] == "LimbNode":
                    vals = {pp.props[0]: [float(x) for x in pp.props[4:]] for pp in n.find("Properties70").find_all("P")}
                    M = np.eye(4)
                    M[:3, :3] = stf.rot_xyz(vals["Lcl Rotation"])
                    M[:3, 3] = np.array(vals["Lcl Translation"]) / 100.0
                    lcl[fbx_skin._name(n.props[1])] = M

            def world(b):
                return world(body.parent[b]) @ lcl[b] if b in body.parent else lcl[b]
            for b in body.bones:
                self.assertLess(np.abs(world(b) - body.bones[b]).max(), 1e-9, b)
            # the garment read again (as a skinned FBX garment) keeps its polygons and both UV layers
            g2 = stf.read_fbx(p)
            self.assertEqual(g2.n_faces, g.n_faces)
            self.assertEqual([u[0] for u in g2.uv_layers], ["UVMap", "pattern"])
            self.assertLess(np.abs(g2.uv_layers[1][1][g2.uv_layers[1][2]] - g.uv_layers[1][1][g.uv_layers[1][2]]).max(), 1e-12)

    def test_weights_on_a_missing_bone_refused(self):
        body = synthetic_body()
        g = quad_garment(lerp_path((0, 0, 1.0), (0, 0, 1.2), 3), 0.17)
        Wg = np.zeros((len(g.verts), 1))
        Wg[:, 0] = 1.0
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                stf.write_skinned_fbx(os.path.join(d, "x.fbx"), g, body.bones, body.parent, Wg, ["nosuchbone"])


class TestMatchCheck(unittest.TestCase):
    def test_full_body_with_head_matches_body(self):
        rep = stf.match_check(synthetic_body(full=True), synthetic_body(full=False))
        self.assertTrue(rep["pass"], rep["fails"])
        self.assertEqual(rep["points"]["foundOnFull"], rep["points"]["body"])
        self.assertIn("head", rep["weights"]["bonesOnlyFull"])

    def test_changed_weight_fails(self):
        full, body = synthetic_body(True), synthetic_body(False)
        idx, w = full.weights["pelvis"]
        w = w.copy()
        w[5] += 0.002
        full.weights["pelvis"] = (idx, w)
        rep = stf.match_check(full, body)
        self.assertFalse(rep["pass"])
        self.assertEqual(rep["weights"]["pointsOver"], 1)

    def test_moved_bone_fails(self):
        full, body = synthetic_body(True), synthetic_body(False)
        full.bones["calf_l"] = full.bones["calf_l"].copy()
        full.bones["calf_l"][0, 3] += 0.00002
        rep = stf.match_check(full, body)
        self.assertFalse(rep["pass"])
        self.assertAlmostEqual(rep["bones"]["worstMm"], 0.02, places=6)

    def test_moved_point_fails(self):
        full, body = synthetic_body(True), synthetic_body(False)
        body.verts = body.verts.copy()
        body.verts[0, 2] += 0.0001
        rep = stf.match_check(full, body)
        self.assertFalse(rep["pass"])
        self.assertEqual(rep["points"]["foundOnFull"], rep["points"]["body"] - 1)


class TestPiecesAndReading(unittest.TestCase):
    def test_uv_islands(self):
        g = stf.Garment()
        g.verts = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0], [0, 0, 1], [1, 0, 1], [2, 0, 1]], float)
        g.corners = np.array([0, 1, 4, 3, 1, 2, 5, 4])
        g.poly_start = np.array([0, 4, 8])
        uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [5, 0], [6, 0], [6, 1], [5, 1]], float)
        g.uv_layers = [("pattern", uv, np.array([0, 1, 2, 3, 1, 4, 5, 2]))]    # shared edge, same UVs
        self.assertEqual(stf.uv_islands(g).tolist(), [0, 0])
        g.uv_layers = [("pattern", uv, np.array([0, 1, 2, 3, 4, 5, 6, 7]))]    # cut along the edge
        self.assertEqual(stf.uv_islands(g).tolist(), [0, 1])
        self.assertIsNone(stf.uv_islands(g, "nolayer"))

    def test_read_obj_groups_and_frame(self):
        txt = "v 0 1000 0\nv 100 1000 0\nv 100 1100 0\nv 0 1100 -50\nvt 0 0\nvt 1 0\nvt 1 1\nvt 0 1\n" \
              "g Front\nf 1/1 2/2 3/3\ng Back\nf 1/1 3/3 4/4\n"
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "g.obj")
            with open(p, "w") as f:
                f.write(txt)
            g = stf.read_garment(p)
        self.assertEqual(g.piece_names, ["Front", "Back"])
        self.assertEqual(g.face_piece.tolist(), [0, 1])
        self.assertLess(np.abs(g.verts[3] - [0, 0.05, 1.1]).max(), 1e-12)
        self.assertEqual(stf.set_pieces(g, "auto"), "groups")
        self.assertEqual(len(g.uv_layers), 1)

    def test_edges_are_the_polygons_own(self):
        g = quad_garment(lerp_path((0, 0, 1.0), (0, 0, 1.1), 2), 0.1, segs=4)
        self.assertEqual(len(g.edges()), 4 + 4 + 4)            # two rings and the uprights, no diagonals

    def test_auto_sides(self):
        body = synthetic_body()
        legs = [quad_garment(lerp_path((0.1 * x, 0, 0.95), (0.1 * x, 0, 0.1), 10), 0.085) for x in (-1, 1)]
        band = quad_garment(lerp_path((0, 0, 0.98), (0, 0, 1.05), 2), 0.17)
        g = join(legs[0], legs[1], band)
        R, L = stf.auto_sides(g, body)
        self.assertEqual((R, L), ({0}, {1}))


class TestBind(unittest.TestCase):
    def setUp(self):
        self.body = synthetic_body()

    def test_constant_region_copies_its_bone(self):
        g = quad_garment(lerp_path((0.1, 0, 0.42), (0.1, 0, 0.1), 5), 0.08)     # round the left calf only
        log = {}
        G, names, rel = stf.bind(self.body, g, log=log)
        self.assertTrue(rel.all())
        self.assertLess(np.abs(G[:, names.index("calf_l")] - 1.0).max(), 1e-9)
        self.assertEqual(log["inpainted"], 0)

    def test_blend_is_interpolated_and_capped(self):
        g = quad_garment(lerp_path((0.1, 0, 0.9), (0.1, 0, 0.1), 17), 0.075)
        G, names, _ = stf.bind(self.body, g)
        self.assertLessEqual(int((G > 0).sum(axis=1).max()), stf.MAX_INFLUENCES)
        self.assertLess(np.abs(G.sum(axis=1) - 1).max(), 1e-9)
        z = g.verts[:, 2]
        th = G[:, names.index("thigh_l")] + G[:, names.index("thigh_twist_01_l")]
        self.assertGreater(th[z > 0.7].min(), 0.95)
        self.assertGreater(G[z < 0.3, names.index("calf_l")].min(), 0.95)
        mid = np.abs(z - 0.5) < 0.03
        self.assertTrue(np.all((th[mid] > 0.2) & (th[mid] < 0.8)))

    def test_trunk_piece_never_takes_the_arm_but_keeps_correctives(self):
        # a vest round the trunk whose shoulder ring reaches the arm's root: its nearest skin there is the arm's
        g = quad_garment(lerp_path((0, 0, 1.2), (0, 0, 1.45), 6), 0.21)
        # angle 90: every copy trusted, so the panel rule alone keeps the arm out (at 50 degrees the shoulder ring's
        # copies face the arm's skin sideways and are inpainted from the trunk anyway)
        G, names, _ = stf.bind(self.body, g, angle=90)
        for b in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r"):
            self.assertEqual(G[:, names.index(b)].max(), 0.0, b)
        G2, n2, _ = stf.bind(self.body, g, panels=False, angle=90)
        self.assertGreater(G2[:, n2.index("upperarm_l")].max(), 0.05)     # the tear the panels rule prevents

    def test_sleeve_piece_takes_the_arm(self):
        sleeve = quad_garment(lerp_path((0.3, 0, 1.4), (0.65, 0, 1.4), 8), 0.065)
        G, names, _ = stf.bind(self.body, sleeve)
        arm = sum(G[:, names.index(b)] for b in ("upperarm_l", "upperarm_fwd_l", "lowerarm_l"))
        self.assertGreater(arm.min(), 0.99)

    def test_far_point_is_inpainted_from_neighbours(self):
        g = quad_garment(lerp_path((0.1, 0, 0.42), (0.1, 0, 0.1), 5), 0.08)
        g.verts = g.verts.copy()
        far = 2 * 16 + 3
        g.verts[far] += (g.verts[far] - [0.1, 0, g.verts[far, 2]]) * 1.5        # 12 cm out: beyond the reach
        log = {}
        G, names, rel = stf.bind(self.body, g, log=log)
        self.assertFalse(rel[far])
        self.assertEqual(log["inpainted"], 1)
        self.assertGreater(G[far, names.index("calf_l")], 0.99)

    def test_skin_trousers_end_to_end(self):
        legs = [quad_garment(lerp_path((0.1 * x, 0, 0.97), (0.1 * x, 0, 0.1), 10), 0.085) for x in (-1, 1)]
        g = join(legs[0], legs[1])
        # weld the two legs' top inner points into a centre seam: the closest pairs at the top ring
        W, names, log = stf.skin(self.body, g, pieces="groups", leg_sides="auto", crotch_fade=0.07, centre_seam="auto")
        self.assertEqual(log["pieces"], "groups")
        self.assertEqual(log["legSides"]["right"], [0])
        right_pts = np.unique(g.corners[np.isin(np.repeat(np.arange(g.n_faces), 4), np.nonzero(g.face_piece == 0)[0])])
        left_bones = [names.index(b) for b in ("thigh_l", "thigh_twist_01_l", "calf_l") if b in names]
        self.assertEqual(W[np.ix_(right_pts, left_bones)].max(), 0.0)
        self.assertEqual(log["crotch"]["seamPoints"], 0)         # unwelded legs share no point
        # weights at or under 0.0001 are dropped after normalising, as Blender stores them (Unreal renormalises)
        self.assertLess(np.abs(W.sum(axis=1) - 1).max(), stf.MAX_INFLUENCES * stf.KEEP_MIN)


class TestCorrect(unittest.TestCase):
    def setUp(self):
        self.body = synthetic_body()
        self.g, self.xs = strip_pair()
        names = sorted(self.body.weights)
        self.names = names
        G = np.zeros((len(self.g.verts), len(names)))
        x = self.g.verts[:, 0]
        # the right piece's inner side wrongly carries some left thigh, as nearest-skin copying gives between touching thighs
        G[:, names.index("thigh_r")] = np.where(x < 0, 0.8, 0.1)
        G[:, names.index("thigh_l")] = np.where(x < 0, 0.2, 0.8)
        G[:, names.index("thigh_twist_01_l")] = np.where(x <= 0, 0.0, 0.1)
        G[:, names.index("head")] = np.where(np.abs(x) > 0.14, 0.05, 0.0)
        self.G = G / G.sum(axis=1, keepdims=True)

    def test_leg_sides_swap_only_one_sided_points(self):
        log = {}
        W, names = stf.correct(self.body, self.g, self.G, self.names, leg_sides=({0}, {1}), log=log)
        x = self.g.verts[:, 0]
        right_only, seam = x < -1e-9, np.abs(x) < 1e-9
        self.assertEqual(W[right_only, names.index("thigh_l")].max(), 0.0)
        self.assertEqual(W[x > 1e-9, names.index("thigh_r")].max(), 0.0)
        self.assertGreater(W[seam, names.index("thigh_l")].min(), 0.1)          # the seam keeps both
        self.assertEqual(log["legSides"]["pointsSwapped"], int((~seam).sum()))

    def test_crotch_fade(self):
        log = {}
        W, names = stf.correct(self.body, self.g, self.G, self.names, crotch_fade=0.07, centre_seam=({0}, {1}), log=log)
        x = self.g.verts[:, 0]
        thighs = [names.index(n) for n in names if n.startswith("thigh")]
        seam = np.abs(x) < 1e-9
        self.assertEqual(log["crotch"]["seamPoints"], int(seam.sum()))
        self.assertLess(W[np.ix_(seam, thighs)].max(), 1e-12)                   # all of it on the seam
        far = np.abs(x) > 0.07
        before = self.G.copy()
        hw = before[:, self.names.index("head")]
        expect = before[far][:, [self.names.index(n) for n in names if n.startswith("thigh")]].sum(axis=1) / (1.0)
        self.assertLess(np.abs(W[np.ix_(far, thighs)].sum(axis=1) - expect).max(), 1e-9)   # untouched beyond
        x6 = np.abs(np.abs(x) - 0.03) < 1e-9
        t = 1 - 0.03 / 0.07
        share = t * t * (3 - 2 * t)
        self.assertLess(np.abs(W[x6, names.index("pelvis")] - share * before[x6][:, [self.names.index(n) for n in names
                                                                                       if n.startswith("thigh")]].sum(axis=1)).max(), 1e-9)
        self.assertGreater(hw.max(), 0)

    def test_head_goes_to_the_neck_and_cap(self):
        W, names = stf.correct(self.body, self.g, self.G, self.names, max_influences=2)
        self.assertEqual(W[:, names.index("head")].max(), 0.0)
        self.assertLessEqual(int((W > 0).sum(axis=1).max()), 2)
        self.assertLess(np.abs(W.sum(axis=1) - 1).max(), 1e-9)

    def test_loose_piece_inside_shoulders_loses_the_arm(self):
        g = join(quad_garment(lerp_path((0, 0, 1.0), (0, 0, 1.45), 6), 0.17),
                 quad_garment(lerp_path((0, -0.17, 1.3), (0, -0.17, 1.32), 2), 0.01, segs=6))    # a small tab in front
        names = sorted(self.body.weights)
        G = np.zeros((len(g.verts), len(names)))
        G[:, names.index("spine_05")] = 0.5
        G[:, names.index("upperarm_fwd_l")] = 0.5
        log = {}
        W, nn = stf.correct(self.body, g, G, names, log=log)
        tab = np.arange(len(g.verts)) >= 6 * 16
        self.assertEqual(W[tab, nn.index("upperarm_fwd_l")].max(), 0.0)
        self.assertGreater(W[~tab, nn.index("upperarm_fwd_l")].min(), 0.4)
        self.assertEqual(log["loosePiecePoints"], int(tab.sum()))


class TestRun(unittest.TestCase):
    def test_run_end_to_end_with_match_and_compare(self):
        full, body = synthetic_body(True), synthetic_body(False)
        g = quad_garment(lerp_path((0.1, 0, 0.9), (0.1, 0, 0.1), 9), 0.08)
        with tempfile.TemporaryDirectory() as d:
            fb, bb_, gp = os.path.join(d, "full.fbx"), os.path.join(d, "body.fbx"), os.path.join(d, "g.fbx")
            for path, b in ((fb, full), (bb_, body)):
                bg = stf.Garment()
                bg.verts = b.verts
                bg.corners = b.tris.reshape(-1)
                bg.poly_start = np.arange(0, len(bg.corners) + 1, 3)
                Wb, nb = stf.dense_weights(b)
                stf.write_skinned_fbx(path, bg, b.bones, b.parent, Wb, nb, mesh_name="body")
            Wz, nz = stf.dense_weights(full)
            stf.write_skinned_fbx(gp, g, full.bones, full.parent, np.zeros((len(g.verts), len(nz))) + (np.array(nz) == "root"), nz)
            out = os.path.join(d, "out")
            rep = stf.run(fb, gp, out, "leg", match_body=bb_, pieces="none")
            self.assertTrue(rep["match"]["pass"], rep["match"]["fails"])
            self.assertTrue(os.path.exists(os.path.join(out, "leg_skinned.fbx")))
            # comparing the output with itself: no difference
            rep2 = stf.run(fb, gp, os.path.join(d, "out2"), "leg", pieces="none", compare_to=os.path.join(out, "leg_skinned.fbx"))
            self.assertEqual(rep2["compare"]["tvMax"], 0.0)
            self.assertEqual(rep2["compare"]["pointMismatchMm"], 0.0)
            # a body whose weights differ stops the run
            idx, w = full.weights["calf_l"]
            full.weights["calf_l"] = (idx, w * 0.99)
            bg = stf.Garment()
            bg.verts, bg.corners = full.verts, full.tris.reshape(-1)
            bg.poly_start = np.arange(0, len(bg.corners) + 1, 3)
            Wb, nb = stf.dense_weights(full)
            stf.write_skinned_fbx(fb, bg, full.bones, full.parent, Wb, nb, mesh_name="body")
            with self.assertRaises(SystemExit):
                stf.run(fb, gp, os.path.join(d, "out3"), "leg", match_body=bb_, pieces="none")


def with_uvs(g, names=("pattern", "UVMap")):
    """Give a quad garment one UV layer per name: per corner, distinct values (the layer's number in the integer part)."""
    g.uv_layers = []
    C = len(g.corners)
    for k, n in enumerate(names):
        uv = np.stack([k + np.arange(C) / (C + 1.0), (np.arange(C) * 7 % C) / float(C)], axis=1)
        g.uv_layers.append((n, uv, np.arange(C, dtype=np.int64)))
    return g


OBJ = """# a tiny drape: two quads, two pieces, normals as Marvelous writes them
v 0 1000 0
v 100 1000 0
v 100 900 0
v 0 900 0
v 200 1000 0
v 200 900 0
vt 0.0 0.0
vt 0.5 0.0
vt 0.5 0.5
vt 0.0 0.5
vt 0.75 0.0
vt 0.75 0.5
vt 0.25 0.25
vn 0 0 1
g front
f 1/1/1 4/4/1 3/3/1 2/2/1
g back
f 2/7/1 3/3/1 6/6/1 5/5/1
"""


class TestUvOrder(unittest.TestCase):
    def test_maps_layout_first(self):
        g = with_uvs(quad_garment(lerp_path((0, 0, 0.2), (0, 0, 0.8), 4), 0.1, 6), ("pattern", "UVMap", "extra"))
        before = stf.corner_uvs(g)
        self.assertTrue(stf.maps_layout_first(g))
        self.assertEqual([n for n, _, _ in g.uv_layers], ["UVMap", "pattern", "extra"])
        for n, uv in stf.corner_uvs(g).items():
            np.testing.assert_array_equal(uv, before[n])
        self.assertFalse(stf.maps_layout_first(g))                       # already first
        self.assertFalse(stf.maps_layout_first(g, "nothing"))            # no such layer: left alone

    def test_fbx_read_back_keeps_every_corner_and_catches_changes(self):
        b = synthetic_body(True)
        g = with_uvs(quad_garment(lerp_path((0.1, 0, 0.9), (0.1, 0, 0.1), 6), 0.08, 8), ("UVMap", "pattern"))
        W, names = stf.dense_weights(b)
        Wg = np.zeros((len(g.verts), len(names)))
        Wg[:, names.index("thigh_l")] = 1.0
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "g.fbx")
            stf.write_skinned_fbx(p, g, b.bones, b.parent, Wg, names)
            back = stf.read_fbx(p)
            rep = stf.uv_check(g, back)
            self.assertTrue(rep["pass"], rep["fails"])
            self.assertEqual(rep["first"], "UVMap")
            self.assertEqual(rep["worstDifference"], {"UVMap": 0.0, "pattern": 0.0})
            # one corner's UV changed, or the layers swapped, or a polygon turned: each fails
            n, uv, idx = back.uv_layers[1]
            uv = uv.copy()
            uv[idx[5]] += 0.01
            back.uv_layers[1] = (n, uv, idx)
            self.assertFalse(stf.uv_check(g, back)["pass"])
            back = stf.read_fbx(p)
            back.uv_layers = back.uv_layers[::-1]
            self.assertIn("layer order", " ".join(stf.uv_check(g, back)["fails"]))
            back = stf.read_fbx(p)
            back.corners = back.corners.copy()
            back.corners[:4] = back.corners[:4][::-1]
            self.assertFalse(stf.uv_check(g, back)["polygonsSame"])

    def test_obj_missing_uv_is_counted(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "m.obj")
            with open(p, "w") as f:
                f.write(OBJ.replace("f 2/7/1 3/3/1 6/6/1 5/5/1", "f 2 3 6 5"))
            g = stf.read_obj(p)
            self.assertEqual(g.uv_missing, 4)
            self.assertEqual(g.uv_layers, [])
            with open(p, "w") as f:
                f.write(OBJ)
            self.assertEqual(stf.read_obj(p).uv_missing, 0)

    def test_chain_from_kiln_obj_through_bend_back_to_fbx(self):
        import bend_back
        b = synthetic_body(True)
        with tempfile.TemporaryDirectory() as d:
            k, bent, fb = (os.path.join(d, x) for x in ("kiln.obj", "bent.obj", "s.fbx"))
            with open(k, "w") as f:
                f.write(OBJ)
            lines, vidx, pts, _ = bend_back.read_obj(k)
            moved = pts + np.array([3.0, -2.0, 1.5])                       # every point moves, as a bend-back does
            bend_back.write_obj(bent, lines, vidx, pts, moved)
            g = stf.read_obj(bent)
            self.assertEqual(g.uv_missing, 0)
            W, names = stf.dense_weights(b)
            Wg = np.zeros((len(g.verts), len(names)))
            Wg[:, names.index("spine_05")] = 1.0
            stf.write_skinned_fbx(fb, g, b.bones, b.parent, Wg, names)
            rep = stf.uv_chain(k, bent, fb)
            self.assertTrue(rep["pass"], (rep["kilnToBent"]["fails"], rep["bentToFbx"]["fails"]))
            self.assertEqual(rep["fbxFirst"], "UVMap")
            # a bent OBJ whose face took another vt fails the chain
            txt = open(bent).read().replace("f 2/7 3/3 6/6 5/5", "f 2/1 3/3 6/6 5/5")
            self.assertNotEqual(txt, open(bent).read())
            with open(bent, "w") as f:
                f.write(txt)
            self.assertFalse(stf.uv_chain(k, bent, fb)["pass"])

    def test_run_puts_the_maps_layout_first_and_checks_the_fbx(self):
        full = synthetic_body(True)
        g = with_uvs(quad_garment(lerp_path((0.1, 0, 0.9), (0.1, 0, 0.1), 9), 0.08), ("pattern", "UVMap"))
        with tempfile.TemporaryDirectory() as d:
            fb, gp = os.path.join(d, "full.fbx"), os.path.join(d, "g.fbx")
            bg = stf.Garment()
            bg.verts, bg.corners = full.verts, full.tris.reshape(-1)
            bg.poly_start = np.arange(0, len(bg.corners) + 1, 3)
            Wb, nb = stf.dense_weights(full)
            stf.write_skinned_fbx(fb, bg, full.bones, full.parent, Wb, nb, mesh_name="body")
            stf.write_skinned_fbx(gp, g, full.bones, full.parent, np.zeros((len(g.verts), len(nb))) + (np.array(nb) == "root"), nb)
            rep = stf.run(fb, gp, os.path.join(d, "out"), "leg", pieces="none")
            self.assertTrue(rep["uvReordered"])
            self.assertTrue(rep["uv"]["pass"], rep["uv"]["fails"])
            self.assertEqual(rep["uv"]["layersAsRead"], ["pattern", "UVMap"])
            out = stf.read_fbx(os.path.join(d, "out", "leg_skinned.fbx"))
            self.assertEqual([n for n, _, _ in out.uv_layers], ["UVMap", "pattern"])
            src = stf.corner_uvs(g)
            for n, uv in stf.corner_uvs(out).items():
                np.testing.assert_array_equal(uv, src[n])
            rep2 = stf.run(fb, gp, os.path.join(d, "out2"), "leg", pieces="none", uv_first="")
            self.assertFalse(rep2["uvReordered"])
            self.assertEqual(rep2["uv"]["first"], "pattern")


if __name__ == "__main__":
    unittest.main()
