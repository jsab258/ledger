"""Unit tests for tools/md/pose_check.py on synthetic meshes (no project files read or written; temporary files only).

    python -m unittest tools/md/test_pose_check.py      (or: python tools/md/pose_check.py --selftest)

The synthetic body (Blender's frame: metres, z up, facing -y, the left side at +x) is a trunk tube and two leg tubes,
all built upwards so their faces point outwards as a real skin's do. Bones: root, pelvis, spine_03; per side thigh
and calf. The garment is a pair of trouser legs round the legs.
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
import pose_check as pc  # noqa: E402
import skin_transfer as stf  # noqa: E402
from test_bend_back import lerp_path, tube  # noqa: E402
from test_skin_transfer import quad_garment, join  # noqa: E402

POS = {"root": (0, 0, 0), "pelvis": (0, 0, 1.0), "spine_03": (0, 0, 1.3),
       "thigh_l": (0.1, 0, 0.95), "calf_l": (0.1, 0, 0.5), "thigh_r": (-0.1, 0, 0.95), "calf_r": (-0.1, 0, 0.5),
       "upperarm_l": (0.2, 0, 1.4), "upperarm_r": (-0.2, 0, 1.4)}
PARENT = {"pelvis": "root", "spine_03": "pelvis", "thigh_l": "pelvis", "calf_l": "thigh_l", "thigh_r": "pelvis",
          "calf_r": "thigh_r", "upperarm_l": "spine_03", "upperarm_r": "spine_03"}


def bones():
    out = {}
    for b, p in POS.items():
        M = np.eye(4)
        M[:3, 3] = p
        out[b] = M
    return out


def smooth(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def body(segs=24):
    parts, weights = [], []

    def add(path, r, wfun):
        v, t, _ = tube(path, r, segs)
        parts.append((v, t))
        weights.append(wfun(v))
    add(lerp_path((0, 0, 0.98), (0, 0, 1.5), 14), 0.17, lambda v: {"pelvis": 1 - smooth((v[:, 2] - 1.2) / 0.1),
                                                                     "spine_03": smooth((v[:, 2] - 1.2) / 0.1)})
    for s, x in (("l", 1.0), ("r", -1.0)):
        add(lerp_path((0.1 * x, 0, 0.02), (0.1 * x, 0, 0.97), 39), 0.07,
            lambda v, s=s: {"calf_" + s: 1 - smooth((v[:, 2] - 0.45) / 0.1), "thigh_" + s: smooth((v[:, 2] - 0.45) / 0.1)})
    verts, tris, off, W = [], [], 0, {}
    total = sum(len(v) for v, _ in parts)
    for (v, t), w in zip(parts, weights):
        verts.append(v)
        tris.append(t + off)
        for b, x in w.items():
            W.setdefault(b, np.zeros(total))[off:off + len(v)] = x
        off += len(v)
    b = fbx_skin.Skinned()
    b.verts, b.tris = np.concatenate(verts), np.concatenate(tris)
    b.weights = {k: (np.nonzero(x > 1e-9)[0], x[x > 1e-9]) for k, x in W.items() if np.any(x > 1e-9)}
    b.bones, b.parent = bones(), dict(PARENT)
    return b


def legs(r=0.085, segs=24):
    return join(*[quad_garment(lerp_path((0.1 * x, 0, 0.1), (0.1 * x, 0, 0.9), 33), r, segs) for x in (-1, 1)])


def write_body(path, b):
    g = stf.Garment()
    g.verts, g.corners = b.verts, b.tris.reshape(-1)
    g.poly_start = np.arange(0, len(g.corners) + 1, 3)
    W, n = stf.dense_weights(b)
    stf.write_skinned_fbx(path, g, b.bones, b.parent, W, n, mesh_name="body")


class TestPoses(unittest.TestCase):
    def test_rotations_are_kilns(self):
        np.testing.assert_allclose(pc.rot("x", 90) @ [0, 1, 0], [0, 0, 1], atol=1e-12)
        np.testing.assert_allclose(pc.rot("y", 90) @ [0, 0, 1], [1, 0, 0], atol=1e-12)
        self.assertEqual(set(pc.KILN_POSES), {"rest", "walk", "sit", "arms up"})
        self.assertEqual(pc.KILN_POSES["sit"]["thigh_l"], ("x", -88.0))
        self.assertEqual(pc.KILN_POSES["arms up"]["upperarm_r"], ("y", 95.0))

    def test_sit_moves_compound_down_the_leg(self):
        b = bones()
        m = pc.pose_moves(b, PARENT, "sit")
        knee = m["calf_l"][:3, :3] @ b["calf_l"][:3, 3] + m["calf_l"][:3, 3]
        self.assertLess(knee[1], -0.4)                                     # forward (the body faces -y)
        self.assertAlmostEqual(knee[2], 0.95, delta=0.02)                  # up at the hip's height
        foot = np.array([0.1, 0, 0.05, 1.0])
        f = m["calf_l"] @ foot
        self.assertAlmostEqual(f[1], knee[1], delta=0.01)                  # the shin hangs straight down again
        np.testing.assert_allclose(m["root"], np.eye(4))
        np.testing.assert_allclose(m["pelvis"], np.eye(4))
        self.assertFalse(np.allclose(m["spine_03"], np.eye(4)))
        rest = pc.pose_moves(b, PARENT, "rest")
        for M in rest.values():
            np.testing.assert_allclose(M, np.eye(4))

    def test_arms_up_raises_the_left_arm(self):
        b = {"root": np.eye(4), "upperarm_l": np.eye(4)}
        b["upperarm_l"][:3, 3] = (0.2, 0, 1.4)
        m = pc.pose_moves(b, {"upperarm_l": "root"}, "arms up")
        hand = m["upperarm_l"] @ np.array([0.7, 0, 1.4, 1.0])
        self.assertGreater(hand[2], 1.85)

    def test_lbs_rigid_blend_and_unweighted(self):
        V = np.array([[0, 0, 0.0], [1, 0, 0.0], [2, 0, 0.0]])
        M = np.eye(4)
        M[:3, 3] = (0, 0, 1)
        w = {"a": (np.array([0, 1]), np.array([1.0, 0.5])), "b": (np.array([1]), np.array([0.5]))}
        P = pc.lbs(V, w, {"a": M, "b": np.eye(4)})
        np.testing.assert_allclose(P, [[0, 0, 1], [1, 0, 0.5], [2, 0, 0]])


class TestMeasures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        v, t, _ = tube(lerp_path((0, 0, 0.0), (0, 0, 1.0), 21), 0.1, 32)
        cls.BV, cls.BT = v, t

    def cloth(self, r, flip=False):
        v, t, _ = tube(lerp_path((0, 0, 0.2), (0, 0, 0.8), 13), r, 32)
        return v, (t[:, ::-1] if flip else t)

    def test_clear_cloth_has_none_through(self):
        CV, CT = self.cloth(0.12)
        idx, _, _ = pc.through(CV, CT, self.BV, self.BV, self.BT)
        self.assertEqual(len(idx), 0)

    def test_tight_cloth_is_through_and_sides_found_either_winding(self):
        CV, CT = self.cloth(0.092)                      # the body 8 mm outside it
        a, depth, signs = pc.through(CV, CT, self.BV, self.BV, self.BT)
        self.assertGreater(len(a), 0)
        self.assertTrue(np.all(depth > pc.LIMIT))
        CVf, CTf = self.cloth(0.092, flip=True)
        b, _, signs_f = pc.through(CVf, CTf, self.BV, self.BV, self.BT)
        self.assertEqual(len(a), len(b))
        self.assertTrue(np.all(signs == 1.0) and np.all(signs_f == -1.0))

    def test_openings_and_height_leave_points_out(self):
        CV, CT = self.cloth(0.092)
        idx, _, _ = pc.through(CV, CT, self.BV, self.BV, self.BT)
        z = self.BV[idx, 2]
        self.assertTrue(np.all(z >= 0.2 + pc.SKIP - 0.012) and np.all(z <= 0.8 - pc.SKIP + 0.012))
        # 3 mm and under is not through
        CV2, CT2 = self.cloth(0.098)
        self.assertEqual(len(pc.through(CV2, CT2, self.BV, self.BV, self.BT)[0]), 0)

    def test_parity_inside(self):
        P = np.array([[0, 0, 0.5], [0.05, 0.02, 0.3], [0.2, 0, 0.5], [0, 0.3, 0.5]])
        np.testing.assert_array_equal(pc.parity_inside(P, self.BV, self.BT), [True, True, False, False])

    def test_cloth_inside_over_3mm(self):
        CV, _ = self.cloth(0.094)
        m, d = pc.inside(CV, self.BV, self.BT)
        self.assertEqual(int(m.sum()), len(CV))
        CV2, _ = self.cloth(0.098)
        self.assertEqual(int(pc.inside(CV2, self.BV, self.BT)[0].sum()), 0)
        CV3, _ = self.cloth(0.12)
        self.assertEqual(int(pc.inside(CV3, self.BV, self.BT)[0].sum()), 0)

    def test_stretch(self):
        g = quad_garment(lerp_path((0, 0, 0.2), (0, 0, 0.8), 7), 0.1, 12)
        e = g.edges()
        P = g.verts.copy()
        P[:, 2] = 0.2 + (P[:, 2] - 0.2) * 1.3
        s = pc.stretch(g.verts, P, e)
        self.assertAlmostEqual(s["worstStretch"], 1.3, places=6)
        self.assertEqual(s["edgesStretchedOver1_2x"], 6 * 12)              # the edges along z only
        self.assertEqual(pc.stretch(g.verts, g.verts, e)["worstStretch"], 1.0)

    def test_boundary_loops(self):
        g = quad_garment(lerp_path((0, 0, 0.2), (0, 0, 0.8), 7), 0.1, 12)
        loops = pc.boundary_loops(g)
        self.assertEqual(sorted(len(x) for x in loops), [12, 12])
        self.assertEqual(sorted(round(float(g.verts[x, 2].mean()), 3) for x in loops), [0.2, 0.8])

    def test_families(self):
        self.assertEqual(pc.family("thigh_twist_01_l"), "thigh_l")
        self.assertEqual(pc.family("calf_r"), "calf_r")
        self.assertEqual(pc.family("ball_l"), "foot_l")
        self.assertEqual(pc.family("hand_r"), "arm_r")
        self.assertEqual(pc.family("FACIAL_C_Jaw"), "head")
        self.assertEqual(pc.family("pelvis"), "trunk")


class TestShapeVerdict(unittest.TestCase):
    def ref(self, gap, hem):
        return {"garment": "ref.fbx", "poses": [{"pose": "sit", "shape": {"seatAndThighs": {"gapP90Mm": gap},
                                                                             "hems": [{"shapeChangeMm": hem}]}}]}

    def test_bars_from_reference(self):
        mine = {"seatAndThighs": {"gapP90Mm": 20.0}, "hems": [{"shapeChangeMm": 1.0}, {"shapeChangeMm": 0.5}]}
        v = pc.shape_verdict(mine, self.ref(18.6, 0.0))
        self.assertEqual(v["bars"], {"gapP90Mm": 21.5, "hemShapeChangeMm": 1.0})
        self.assertTrue(v["pass"])
        v = pc.shape_verdict({"seatAndThighs": {"gapP90Mm": 25.0}, "hems": [{"shapeChangeMm": 3.0}]}, self.ref(18.6, 0.0))
        self.assertFalse(v["pass"])
        self.assertEqual(len(v["fails"]), 2)

    def test_no_reference_leaves_pass_open(self):
        v = pc.shape_verdict({"seatAndThighs": {"gapP90Mm": 5.0}, "hems": []}, None)
        self.assertIsNone(v["pass"])
        self.assertIsNone(v["measured"]["hemShapeChangeMm"])


class TestCheckEndToEnd(unittest.TestCase):
    def test_trousers_in_every_pose(self):
        b = body()
        g = legs()
        W, names, _ = stf.skin(b, g, pieces="groups", panels=False, leg_sides="auto")
        with tempfile.TemporaryDirectory() as d:
            bp, gp = os.path.join(d, "body.fbx"), os.path.join(d, "legs.fbx")
            write_body(bp, b)
            stf.write_skinned_fbx(gp, g, b.bones, b.parent, W, names, mesh_name="legs")
            rep = pc.check(gp, bp)
            self.assertEqual([r["pose"] for r in rep["poses"]], pc.POSE_ORDER)
            self.assertTrue(rep["skeleton"]["pass"], rep["skeleton"])
            self.assertEqual(rep["unweightedPoints"], 0)
            rest = rep["poses"][0]
            self.assertEqual(rest["bodyThroughClothOver3mm"], 0)
            self.assertEqual(rest["clothInsideBodyOver3mm"], 0)
            self.assertEqual(rest["worstStretch"], 1.0)
            up = rep["poses"][3]                                     # the arms move nothing here
            self.assertEqual(up["bodyThroughClothOver3mm"], 0)
            self.assertEqual(up["worstStretch"], 1.0)
            sit = rep["poses"][2]
            self.assertGreater(sit["worstStretch"], 1.0)             # the knee bends 88 degrees
            for k in ("throughKilnPoseSides", "throughRestSides", "throughByArea", "insideByArea"):
                self.assertIn(k, sit)
            self.assertEqual(sit["bodyThroughClothOver3mm"], max(sit["throughKilnPoseSides"], sit["throughRestSides"]))
            hems = sit["shape"]["hems"]
            self.assertEqual(sorted(h["side"] for h in hems), ["l", "r"])
            for h in hems:                                           # hems ride the calf alone: no change of shape
                self.assertLess(h["shapeChangeMm"], 0.5)
            self.assertGreater(sit["shape"]["seatAndThighs"]["points"], 0)
            self.assertIsNone(rep["shapeCheck"]["pass"])
            # judged against itself: the shape check passes
            rep2 = pc.check(gp, bp, shape_bars=rep)
            self.assertTrue(rep2["shapeCheck"]["pass"])
            self.assertEqual(rep2["toolBarPass"], all(r["pass"] for r in rep2["poses"]))
            # the command line writes the report
            out = os.path.join(d, "r.json")
            code = pc.main([gp, bp, out, "--poses", "rest,walk"])
            self.assertTrue(os.path.exists(out))
            self.assertIn(code, (0, 1))


if __name__ == "__main__":
    unittest.main()
