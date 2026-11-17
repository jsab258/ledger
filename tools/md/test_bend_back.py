"""Unit tests for tools/md/bend_back.py, standard_turns.py and fbx_skin.py on synthetic meshes (no files of the
project are read or written; temporary files only).

    python -m unittest tools/md/test_bend_back.py        (or: python tools/md/bend_back.py --selftest)

The synthetic body is one tube along hand_r, elbow_r, shoulder_r, shoulder_l, elbow_l, hand_l, the elbows bent
forward and down as a MetaHuman's are in its reference pose, each arm's skin shared between upperarm and lowerarm over
10 cm round the elbow; a small separate piece stands for the eyes and teeth the standard leaves out.
"""
import json
import math
import os
import sys
import tempfile
import unittest

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import bend_back as bb  # noqa: E402
import fbx_skin  # noqa: E402
import standard_turns as st  # noqa: E402

RADIUS = 0.04
BLEND = 0.10


def put(path, data):
    with open(path, "wb" if isinstance(data, bytes) else "w", encoding=None if isinstance(data, bytes) else "utf-8") as f:
        f.write(data)


def get(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def tube(path, radius, segs=12):
    """Rings round a polyline (each ring square to the mean of its two segments); returns verts, tris, ring centres."""
    path = np.asarray(path, dtype=float)
    verts, centres = [], []
    ref = np.array([0.0, 1.0, 0.0])
    for i, c in enumerate(path):
        a = path[max(i - 1, 0)]
        b = path[min(i + 1, len(path) - 1)]
        t = (b - a) / np.linalg.norm(b - a)
        u = np.cross(t, ref)
        if np.linalg.norm(u) < 1e-6:
            u = np.cross(t, [1.0, 0.0, 0.0])
        u /= np.linalg.norm(u)
        v = np.cross(t, u)
        for k in range(segs):
            ang = 2 * math.pi * k / segs
            verts.append(c + radius * (math.cos(ang) * u + math.sin(ang) * v))
            centres.append(i)
    tris = []
    for i in range(len(path) - 1):
        for k in range(segs):
            a, b = i * segs + k, i * segs + (k + 1) % segs
            c, d = a + segs, b + segs
            tris += [(a, b, d), (a, d, c)]
    return np.array(verts), np.array(tris, dtype=np.int64), np.array(centres)


def lerp_path(a, b, n):
    return [np.asarray(a) + (np.asarray(b) - np.asarray(a)) * t for t in np.linspace(0, 1, n)]


def joints():
    S = np.array([0.20, 0.0, 1.55])
    E = np.array([0.39, 0.012, 1.31])
    H = E + 0.30 * np.array([0.35, -0.55, -0.76]) / np.linalg.norm([0.35, -0.55, -0.76])
    m = np.array([-1.0, 1.0, 1.0])
    return {"l": (S, E, H), "r": (S * m, E * m, H * m)}


def synthetic_reference(with_stray=True):
    """A Skinned reference body: the arms' tube, bones and weights (and a stray piece first, left out by the standard)."""
    J = joints()
    Sr, Er, Hr = J["r"]
    Sl, El, Hl = J["l"]
    path = lerp_path(Hr, Er, 9) + lerp_path(Er, Sr, 9)[1:] + lerp_path(Sr, Sl, 9)[1:] + lerp_path(Sl, El, 9)[1:] + lerp_path(El, Hl, 9)[1:]
    verts, tris, ring = tube(path, RADIUS)
    path = np.array(path)
    # signed distance along the arm from each elbow (forearm side positive), per ring
    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))])
    i_er, i_sr, i_sl, i_el = 8, 16, 24, 32
    w = {b: np.zeros(len(verts)) for b in ("spine", "upperarm_l", "lowerarm_l", "upperarm_r", "lowerarm_r")}
    for v in range(len(verts)):
        i = ring[v]
        if i <= i_sr:
            s = arc[i_er] - arc[i]                       # forearm side of the right elbow positive
            f = float(np.clip(0.5 + s / BLEND, 0.0, 1.0))
            w["lowerarm_r"][v], w["upperarm_r"][v] = f, 1.0 - f
        elif i >= i_sl:
            s = arc[i] - arc[i_el]
            f = float(np.clip(0.5 + s / BLEND, 0.0, 1.0))
            w["lowerarm_l"][v], w["upperarm_l"][v] = f, 1.0 - f
        else:
            w["spine"][v] = 1.0
    body = fbx_skin.Skinned()
    off = 0
    if with_stray:
        sv, stt, _ = tube([[0.0, -0.05, 1.70], [0.0, -0.05, 1.72]], 0.01, segs=6)
        verts = np.concatenate([sv, verts])
        tris = np.concatenate([stt, tris + len(sv)])
        off = len(sv)
        w = {b: np.concatenate([np.zeros(len(sv)), x]) for b, x in w.items()}
        w["head"] = np.concatenate([np.ones(len(sv)), np.zeros(len(verts) - len(sv))])
    body.verts, body.tris = verts, tris
    body.weights = {b: (np.nonzero(x)[0], x[np.nonzero(x)[0]]) for b, x in w.items() if np.any(x)}
    pos = {"root": [0, 0, 0], "spine": [0, 0, 1.4], "head": [0, 0, 1.65]}
    for s in "lr":
        pos["upperarm_" + s], pos["lowerarm_" + s], pos["hand_" + s] = J[s]
        pos["index_01_" + s] = J[s][2] + (J[s][2] - J[s][1]) * 0.2
    for b, p in pos.items():
        M = np.eye(4)
        M[:3, 3] = p
        body.bones[b] = M
    body.parent = {"spine": "root", "head": "spine"}
    for s in "lr":
        body.parent.update({"upperarm_" + s: "spine", "lowerarm_" + s: "upperarm_" + s, "hand_" + s: "lowerarm_" + s,
                            "index_01_" + s: "hand_" + s})
    return body, off


def record_for(body):
    rec = {"turns": {}}
    for s in "lr":
        t = bb.turn_from_joints(body.joint("upperarm_" + s), body.joint("lowerarm_" + s), body.joint("hand_" + s))
        rec["turns"][s] = {"elbow": t}
    return rec


def standardise(ref, off):
    """The standard body as standard_body.py makes it: the stray piece left out, the forearms turned, posed = rest."""
    rec = record_for(ref)
    turns, shares, mats, group = bb.body_shares(ref, rec)
    std = fbx_skin.Skinned()
    std.verts = bb.forward(ref.verts, shares, mats)[off:]
    std.tris = ref.tris[np.all(ref.tris >= off, axis=1)] - off
    std.weights = {}
    for b, (i, w) in ref.weights.items():
        k = i >= off
        if np.any(k):
            std.weights[b] = (i[k] - off, w[k])
    std.parent = dict(ref.parent)
    for b, W in ref.bones.items():
        std.bones[b] = mats[group[b]] @ W
    return std, rec


class Turns(unittest.TestCase):
    def test_rotation_about_pivot_and_hand(self):
        M = bb.rotation_about([0, 0, 1], 90.0, [1.0, 0.0, 0.0])
        np.testing.assert_allclose(M[:3, :3] @ [2.0, 0.0, 0.0] + M[:3, 3], [1.0, 1.0, 0.0], atol=1e-12)
        np.testing.assert_allclose(M[:3, :3] @ [1.0, 0.0, 5.0] + M[:3, 3], [1.0, 0.0, 5.0], atol=1e-12)

    def test_turn_straightens_forearm_onto_upper_arm(self):
        S, E, H = joints()["l"]
        t = bb.turn_from_joints(S, E, H)
        up, fore = (E - S) / np.linalg.norm(E - S), (H - E) / np.linalg.norm(H - E)
        self.assertAlmostEqual(t["turnDeg"], math.degrees(math.acos(up @ fore)), places=9)
        M = bb.rotation_about(t["axis"], t["turnDeg"], t["elbow"])
        h2 = M[:3, :3] @ H + M[:3, 3]
        np.testing.assert_allclose((h2 - E) / np.linalg.norm(h2 - E), up, atol=1e-12)
        self.assertAlmostEqual(np.linalg.norm(h2 - E), np.linalg.norm(H - E), places=12)
        self.assertIsNone(bb.turn_from_joints(S, E, E + (E - S))["axis"])

    def test_turn_list_order_and_raise_refused(self):
        rec = {"turns": {"r": {"turnDeg": 5.0, "axis": [0, 1, 0], "shoulder": [0, 0, 0],
                               "elbow": {"turnDeg": 30.0, "axis": [1, 0, 0], "elbow": [0, 0, 0]},
                               "thigh": {"turnDeg": 4.0, "axis": [0, 1, 0], "hip": [0, 0, 1]}},
                         "l": {"elbow": {"turnDeg": 30.0, "axis": [1, 0, 0], "elbow": [0, 0, 0]}}}}
        order = [(t["kind"], t["side"]) for t in bb.turn_list(rec)]
        self.assertEqual(order, [("shoulder", "r"), ("elbow", "l"), ("elbow", "r"), ("thigh", "r")])
        rec["raiseMm"] = 20
        with self.assertRaises(ValueError):
            bb.turn_list(rec)

    def test_bone_groups_follow_the_tree(self):
        ref, _ = synthetic_reference()
        turns, shares, mats, group = bb.body_shares(ref, record_for(ref))
        self.assertEqual(group["spine"], 0)
        self.assertEqual(group["upperarm_l"], 0)
        self.assertEqual(group["lowerarm_l"], group["index_01_l"])
        self.assertNotEqual(group["lowerarm_l"], group["lowerarm_r"])
        self.assertEqual(len(mats), 3)
        np.testing.assert_allclose(shares.sum(axis=1), 1.0, atol=1e-12)

    def test_shoulder_then_elbow_compose(self):
        ref, _ = synthetic_reference(with_stray=False)
        rec = {"turns": {"l": {"turnDeg": 12.0, "axis": [0, 1, 0], "shoulder": ref.joint("upperarm_l").tolist()}}}
        M_sh = bb.rotation_about([0, 1, 0], 12.0, ref.joint("upperarm_l"))
        e2 = M_sh[:3, :3] @ ref.joint("lowerarm_l") + M_sh[:3, 3]
        rec["turns"]["l"]["elbow"] = {"turnDeg": 20.0, "axis": [1, 0, 0], "elbow": e2.tolist()}
        turns, shares, mats, group = bb.body_shares(ref, rec)
        M_el = bb.rotation_about([1, 0, 0], 20.0, e2)
        np.testing.assert_allclose(mats[group["hand_l"]], M_el @ M_sh, atol=1e-12)
        np.testing.assert_allclose(mats[group["upperarm_l"]], M_sh, atol=1e-12)
        posed = bb.forward(ref.verts, shares, mats)
        np.testing.assert_allclose(bb.bend_back_points(posed, shares, mats, "exact"), ref.verts, atol=1e-10)


class BendBack(unittest.TestCase):
    def setUp(self):
        self.ref, self.off = synthetic_reference()
        self.std, self.rec = standardise(self.ref, self.off)
        self.turns, self.shares, self.mats, self.group = bb.body_shares(self.std, self.rec)

    def test_exact_inverse_returns_the_reference_skin(self):
        back = bb.bend_back_points(self.std.verts, self.shares, self.mats, "exact")
        np.testing.assert_allclose(back, self.ref.verts[self.off:], atol=1e-10)

    def test_blend_of_inverses_misses_at_the_elbow_only(self):
        back = bb.bend_back_points(self.std.verts, self.shares, self.mats, "lbs")
        err = np.linalg.norm(back - self.ref.verts[self.off:], axis=1)
        pure = np.isclose(self.shares.max(axis=1), 1.0)
        self.assertLess(err[pure].max(), 1e-10)
        self.assertGreater(err[~pure].max(), 1e-3)      # millimetres off where the elbow's skin is shared

    def test_sleeve_bent_back_with_the_arm(self):
        """A sleeve 5 mm off the straightened left forearm comes back 5 mm off the bent forearm."""
        S, E, _ = joints()["l"]
        Hs = self.std.joint("hand_l")
        path = lerp_path(E + (Hs - E) * 0.3, Hs, 8)
        sv, _, _ = tube(path, RADIUS + 0.005, segs=16)
        g_sh, dist, _ = bb.transfer(self.std.verts, self.std.tris, self.shares, sv)
        self.assertLess(dist.max(), 0.0065)
        back = bb.bend_back_points(sv, g_sh, self.mats, "exact")
        _, Eref, Href = joints()["l"]
        # distance of each point to the reference forearm's axis
        ax = (Href - Eref) / np.linalg.norm(Href - Eref)
        rel = back - Eref
        radial = np.linalg.norm(rel - np.outer(rel @ ax, ax), axis=1)
        pure = g_sh[:, self.group["lowerarm_l"]] > 1 - 1e-9
        self.assertGreater(pure.sum(), 50)
        np.testing.assert_allclose(radial[pure], RADIUS + 0.005, atol=2e-3)   # tube facets: the chord, not the arc
        np.testing.assert_allclose(np.linalg.norm(rel[pure], axis=1), np.linalg.norm(sv[pure] - E, axis=1), atol=1e-10)
        # the cuff's middle lands on the reference hand joint
        cuff = back[-16:].mean(axis=0)
        self.assertLess(np.linalg.norm(cuff - Href), 1e-3)

    def test_points_far_from_the_arms_do_not_move(self):
        """Trousers-like points round the trunk take no forearm weight and stay exactly where they are."""
        ring = [np.array([0.12 * math.cos(a), 0.12 * math.sin(a), 1.45]) for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
        pts = np.array(ring)
        g_sh, _, _ = bb.transfer(self.std.verts, self.std.tris, self.shares, pts)
        back = bb.bend_back_points(pts, g_sh, self.mats, "exact")
        np.testing.assert_array_equal(back, pts)

    def test_refuses_a_blend_it_cannot_undo(self):
        mats = np.array([np.eye(4), bb.rotation_about([0, 0, 1], 180.0, [0, 0, 0])])
        with self.assertRaises(ValueError):
            bb.bend_back_points(np.zeros((1, 3)), np.array([[0.5, 0.5]]), mats, "exact")


class Surface(unittest.TestCase):
    def test_closest_point_every_region(self):
        a, b, c = np.array([0.0, 0, 0]), np.array([1.0, 0, 0]), np.array([0.0, 1, 0])
        pts = np.array([[0.2, 0.2, 0.3], [-1, -1, 0.1], [2, -0.5, 0], [-0.5, 2, 0.2], [0.5, -1, 0], [-1, 0.5, 0], [1, 1, 0.4], [0.3, 0.3, -2]])
        q, bary = bb.closest_on_triangles(pts, *(np.tile(x, (len(pts), 1)) for x in (a, b, c)))
        # brute force on a fine barycentric grid
        n = 400
        u, v = np.meshgrid(np.linspace(0, 1, n + 1), np.linspace(0, 1, n + 1))
        keep = (u + v) <= 1
        grid = np.stack([u[keep], v[keep], np.zeros(keep.sum())], axis=1)
        for p, qq, bw in zip(pts, q, bary):
            self.assertAlmostEqual(bw.sum(), 1.0, places=12)
            self.assertTrue(np.all(bw >= -1e-12))
            best = np.linalg.norm(grid - p, axis=1).min()
            self.assertLess(abs(np.linalg.norm(qq - p) - best), 2e-3)
            np.testing.assert_allclose(bw[0] * a + bw[1] * b + bw[2] * c, qq, atol=1e-12)

    def test_transfer_interpolates_across_the_triangle(self):
        xs = np.linspace(0, 1, 11)
        verts = np.array([[x, y, 0.0] for y in xs for x in xs])
        tris = []
        for j in range(10):
            for i in range(10):
                a = j * 11 + i
                tris += [(a, a + 1, a + 12), (a, a + 12, a + 11)]
        data = np.stack([verts[:, 0] * 2 + verts[:, 1], np.ones(len(verts))], axis=1)
        pts = np.array([[0.33, 0.71, 0.05], [0.5, 0.5, -0.2], [0.07, 0.93, 0.01]])
        out, dist, _ = bb.transfer(verts, np.array(tris), data, pts)
        np.testing.assert_allclose(out[:, 0], pts[:, 0] * 2 + pts[:, 1], atol=1e-12)
        np.testing.assert_allclose(out[:, 1], 1.0, atol=1e-12)
        np.testing.assert_allclose(dist, np.abs(pts[:, 2]), atol=1e-12)


class Files(unittest.TestCase):
    def test_obj_written_line_for_line(self):
        src = ("# Drape Studio garment (welded seams)\nv 10.0 1000.0 20.0\nvn 0 1 0\nv 11.0 1001.0 21.0\nvn 0 1 0\n"
               "v 12.0 1002.0 22.0\nvn 0 1 0\nvt 0.1 0.2\nvt 0.3 0.4\nvt 0.5 0.6\ng frontR\nf 1/1/1 2/2/2 3/3/3\n")
        with tempfile.TemporaryDirectory() as d:
            p, q = os.path.join(d, "a.obj"), os.path.join(d, "b.obj")
            put(p, src)
            lines, vidx, pts, groups = bb.read_obj(p)
            self.assertEqual(groups, {"frontR": {0, 1, 2}})
            np.testing.assert_allclose(bb.blender_to_mm(bb.mm_to_blender(pts)), pts, atol=1e-12)
            np.testing.assert_allclose(bb.mm_to_blender(pts)[0], [0.010, -0.020, 1.0])
            new = pts.copy()
            new[1] += [0.5, 0.0, -0.25]
            bb.write_obj(q, lines, vidx, pts, new)
            out = get(q).splitlines()
        self.assertEqual(out[1], "v 10.0 1000.0 20.0")
        self.assertEqual(out[2], "v 11.5000 1001.0000 20.7500")
        self.assertFalse([l for l in out if l.startswith("vn ")])
        self.assertEqual(out[-1], "f 1/1 2/2 3/3")
        self.assertIn("vt 0.3 0.4", out)

    def test_axes_to_blender(self):
        np.testing.assert_allclose(fbx_skin.axis_matrix(2, 1, 1, -1, 0, 1), np.eye(3))       # Unreal's FBX, z up
        C = fbx_skin.axis_matrix(1, 1, 2, 1, 0, 1)                                            # Blender's export, y up
        np.testing.assert_allclose(C @ [0, 1, 0], [0, 0, 1])
        np.testing.assert_allclose(C @ [0, 0, 1], [0, -1, 0])
        np.testing.assert_allclose(C @ [1, 0, 0], [1, 0, 0])
        with self.assertRaises(ValueError):
            fbx_skin.axis_matrix(1, 1, 1, 1, 0, 1)

    def test_run_end_to_end_on_an_obj(self):
        """The whole run with the body reader replaced by the synthetic standard body."""
        ref, off = synthetic_reference()
        std, rec = standardise(ref, off)
        S, E, _ = joints()["l"]
        Hs = std.joint("hand_l")
        sv, stris, _ = tube(lerp_path(E + (Hs - E) * 0.5, Hs, 6), RADIUS + 0.004, segs=10)
        mm = bb.blender_to_mm(sv)
        keep = fbx_skin.load_skinned
        with tempfile.TemporaryDirectory() as d:
            paths = {k: os.path.join(d, k) for k in ("body.fbx", "body.json", "g.obj", "out.obj", "rep.json")}
            put(paths["body.fbx"], b"synthetic")
            put(paths["body.json"], json.dumps(rec))
            with open(paths["g.obj"], "w", encoding="utf-8") as f:
                f.write("".join("v %.5f %.5f %.5f\n" % tuple(p) for p in mm))
                f.write("g sleeveL\n" + "".join("f %d %d %d\n" % tuple(t + 1) for t in stris))
            fbx_skin.load_skinned = lambda path, mesh=None: std
            try:
                rep = bb.run(paths["body.fbx"], paths["body.json"], paths["g.obj"], paths["out.obj"], report=paths["rep.json"])
            finally:
                fbx_skin.load_skinned = keep
            _, _, out_mm, _ = bb.read_obj(paths["out.obj"])
            self.assertTrue(os.path.isfile(paths["rep.json"]))
        back = bb.mm_to_blender(out_mm)
        _, Eref, Href = joints()["l"]
        self.assertLess(np.linalg.norm(back[-10:].mean(axis=0) - Href), 1e-3)
        self.assertEqual(rep["points"], len(sv))
        self.assertGreater(rep["movedMmMax"], 50.0)


class Record(unittest.TestCase):
    def _files(self, d):
        a, b = os.path.join(d, "ref.fbx"), os.path.join(d, "std.fbx")
        put(a, b"ref")
        put(b, b"std")
        return a, b

    def test_components_join_points_at_one_place(self):
        v = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0], [5, 5, 5], [6, 5, 5], [5, 6, 5]], dtype=float)
        t = np.array([[0, 1, 2], [3, 4, 2], [5, 6, 7]])
        parts = st.components(v, t)
        self.assertEqual([p.tolist() for p in parts], [[0, 1, 2, 3, 4], [5, 6, 7]])

    def test_record_from_synthetic_bodies_passes(self):
        ref, off = synthetic_reference()
        std, rec0 = standardise(ref, off)
        with tempfile.TemporaryDirectory() as d:
            a, b = self._files(d)
            rec, chk = st.make_record(ref, std, a, b)
        self.assertEqual(chk["verdict"], "PASS", json.dumps(chk, indent=1)[:2000])
        for s in "lr":
            self.assertAlmostEqual(rec["turns"][s]["elbow"]["turnDeg"], rec0["turns"][s]["elbow"]["turnDeg"], places=5)
            np.testing.assert_allclose(rec["turns"][s]["elbow"]["axis"], rec0["turns"][s]["elbow"]["axis"], atol=1e-8)
        self.assertEqual(chk["skin"]["leftOut"], {"parts": 1, "points": off})
        self.assertLess(chk["skin"]["standardBentBackVsReferenceMm"]["max"], 1e-3)
        self.assertGreater(chk["skin"]["blendOfInversesVsReferenceMm"]["max"], 1.0)
        self.assertEqual(rec["bonesTurned"], {"l": 3, "r": 3})
        # the record bend_back.py reads gives the same turns
        self.assertEqual([t["bone"] for t in bb.turn_list(rec)], ["lowerarm_l", "lowerarm_r"])

    def test_record_fails_when_the_standard_moved_a_point_otherwise(self):
        ref, off = synthetic_reference()
        std, _ = standardise(ref, off)
        std.verts = std.verts.copy()
        std.verts[200] += [0.002, 0.0, 0.0]
        with tempfile.TemporaryDirectory() as d:
            a, b = self._files(d)
            _, chk = st.make_record(ref, std, a, b)
        self.assertEqual(chk["verdict"], "FAIL")
        self.assertEqual(chk["skin"]["pointsMovedOtherwise"], 1)

    def test_record_fails_when_a_bone_moved_otherwise(self):
        ref, off = synthetic_reference()
        std, _ = standardise(ref, off)
        std.bones["spine"] = std.bones["spine"].copy()
        std.bones["spine"][2, 3] += 0.01
        with tempfile.TemporaryDirectory() as d:
            a, b = self._files(d)
            _, chk = st.make_record(ref, std, a, b)
        self.assertEqual(chk["verdict"], "FAIL")
        self.assertEqual([o["bone"] for o in chk["bonesOtherwise"]], ["spine"])


if __name__ == "__main__":
    unittest.main()
