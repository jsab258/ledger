"""Tests for tools/lane/furniture_check.py. Run: python -m unittest tools/lane/test_furniture_check.py"""
import json
import math
import os
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import furniture_check as fc  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def write_glb(path, gltf):
    data = json.dumps(gltf).encode("utf-8")
    data += b" " * ((4 - len(data) % 4) % 4)
    with open(path, "wb") as fh:
        fh.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(data)))
        fh.write(struct.pack("<II", len(data), 0x4E4F534A))
        fh.write(data)


def box_gltf(lo, hi, node_extra=None, parent=None):
    node = {"mesh": 0}
    node.update(node_extra or {})
    nodes = [node]
    roots = [0]
    if parent is not None:
        nodes = [dict(parent, children=[1]), node]
        roots = [0]
    return {"asset": {"version": "2.0"}, "scene": 0, "scenes": [{"nodes": roots}], "nodes": nodes,
            "meshes": [{"name": "m", "primitives": [{"attributes": {"POSITION": 0}}]}],
            "accessors": [{"min": list(lo), "max": list(hi), "count": 8, "type": "VEC3", "componentType": 5126}]}


def piece(name, x, z, sx=0.2, sy=1.0, sz=0.2, bom="E", asset=None):
    return {"name": name, "x_m": x, "y_m": 0.5, "z_m": z, "sx_m": sx, "sy_m": sy, "sz_m": sz, "bom": bom, "asset": asset}


def good_street():
    p = []
    for i, (x, s) in enumerate([(8.0, 1), (18.0, -1), (28.0, 1), (38.0, -1)]):
        p.append(piece("column%d_base" % i, x, s * 3.725, bom="E1_lighting_column"))
    p.append(piece("kiosk_plinth", 16.5, 3.675, 0.89, 0.15, 0.89, bom="E3_telephone_kiosk"))
    p.append(piece("rail_post0", 10.0, 3.375, 0.05, 1.0, 0.05, bom="E8_guard_railing"))
    p.append(piece("rail_post1", 12.0, 3.375, 0.05, 1.0, 0.05, bom="E8_guard_railing"))
    for k in range(17):
        p.append(piece("rail_inf0_%d" % k, 10.1 + k * 0.11, 3.375, 0.012, 0.9, 0.012, bom="E8_guard_railing"))
    p.append(piece("prop_grate", 12.0, 2.8, 0.44, 0.015, 0.29, bom="A7_gully_grate", asset="g"))
    p.append(piece("prop_decorative_bollard_02_0", 20.7, -3.5, asset="decorative_bollard_02", bom="E5_bollards"))
    p.append(piece("prop_decorative_bollard_02_1", 24.3, -3.5, asset="decorative_bollard_02", bom="E5_bollards"))
    p.append(piece("prop_swing_bin_0", 6.6, 3.65, 0.33, 0.7, 0.32, asset="swing_bin", bom="E6_public_bins"))
    p.append(piece("name_plate_0", 20.47, -5.0, bom="E10_street_name_plate"))
    p.append(piece("bus_stop_0", 46.0, -3.5, bom="E20_bus_stop"))
    return p


GOOD_MODELS = {"bollard": (0.21, 1.08, 0.21), "litter-bin": (0.36, 1.255, 0.4), "kx100-kiosk": (0.89, 2.192, 0.89),
               "pillar-box": (0.49, 1.50, 0.49)}


def verdicts(lines):
    return [(l["row"], l["what"], l["verdict"]) for l in lines]


class GlbBounds(unittest.TestCase):
    def test_plain_box(self):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "a.glb")
            write_glb(f, box_gltf((-0.1, 0, -0.2), (0.1, 1.5, 0.2)))
            self.assertEqual(fc.model_size(f), (0.2, 1.5, 0.4))

    def test_translation_does_not_change_size(self):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "a.glb")
            write_glb(f, box_gltf((0, 0, 0), (1, 2, 3), {"translation": [5, 6, 7]}))
            self.assertEqual(fc.model_size(f), (1.0, 2.0, 3.0))

    def test_scale_and_quarter_turn(self):
        # 90 degrees about y swaps x and z; scale 2 on x first.
        q = [0, math.sin(math.pi / 4), 0, math.cos(math.pi / 4)]
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "a.glb")
            write_glb(f, box_gltf((0, 0, 0), (1, 1, 3), {"rotation": q, "scale": [2, 1, 1]}))
            self.assertEqual(fc.model_size(f), (3.0, 1.0, 2.0))

    def test_parent_matrix_scales_child(self):
        parent = {"matrix": [0.5, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 1, 1, 1, 1]}
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "a.glb")
            write_glb(f, box_gltf((0, 0, 0), (2, 4, 2), parent=parent))
            self.assertEqual(fc.model_size(f), (1.0, 2.0, 1.0))

    def test_not_a_glb_is_none(self):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "a.glb")
            with open(f, "wb") as fh:
                fh.write(b"NOPE" + b"\0" * 20)
            self.assertIsNone(fc.model_size(f))
            self.assertIsNone(fc.model_size(os.path.join(d, "missing.glb")))


class Walk(unittest.TestCase):
    def test_gap_front_and_back(self):
        # centre 3.5, depth 0.2: front 0.4, back 1.4
        self.assertEqual(fc.clear_walk_m(3.5, 0.2), 1.4)
        self.assertEqual(fc.clear_walk_m(-3.5, 0.2), 1.4)

    def test_mid_footway_box_can_block(self):
        # a 1.0 m deep box in the middle of a 2.0 m footway leaves 0.5 each side
        self.assertEqual(fc.clear_walk_m(4.0, 1.0), 0.5)


class Gaps(unittest.TestCase):
    def test_two_pieces_side_by_side_add_up(self):
        # each alone leaves 1.2 m, but one at the kerb and one at the wall leave 0.6 between them
        items = [("a", 10.0, 10.5, 3.0, 3.7), ("b", 10.2, 10.8, 4.3, 5.0)]
        rows = fc.walker_gaps(items)
        self.assertEqual([r["found"] for r in rows], [0.6, 0.6])
        self.assertEqual({r["verdict"] for r in rows}, {"FAIL"})

    def test_other_side_and_other_x_do_not_count(self):
        items = [("a", 10.0, 10.5, 3.0, 3.7), ("b", 10.2, 10.8, -5.0, -4.3), ("c", 12.0, 12.5, 4.3, 5.0)]
        self.assertEqual([r["found"] for r in fc.walker_gaps(items)], [1.3, 1.3, 1.3])

    def test_drawn_model_uses_measured_size_and_turn(self):
        models = {"litter-bin": (0.4, 1.0, 0.5), "a-board": (0.6, 1.0, 0.4)}
        items = fc.footed([], [("litter-bin", 8.9, 3.65, ""), ("a-board", 14.0, 4.6, "")], models)
        self.assertEqual([round(i[4] - i[3], 3) for i in items], [0.5, 0.6])


class Check(unittest.TestCase):
    def test_good_street_has_no_fail_or_missing(self):
        lines = fc.check(good_street(), GOOD_MODELS)
        bad = [v for v in verdicts(lines) if v[2] in ("FAIL", "MISSING")]
        # the research line on the pillar box is advisory and fails on the target's 1.5 m by design
        self.assertEqual([v for v in bad if v[0] != "S8 (lane research)"], [])

    def test_lamp_out_of_step_fails(self):
        p = good_street()
        p[1]["z_m"] = 3.725  # the second column on the wrong side
        lines = fc.check(p, GOOD_MODELS)
        self.assertIn(("S1", "lamp columns: four, 10 m staggered, axis 3.725 m", "FAIL"), verdicts(lines))

    def test_tube_rail_fails(self):
        p = [x for x in good_street() if not x["name"].startswith("rail_inf")]
        p += [piece("rail_inf0_%d" % k, 10.3 + k * 0.3, 3.375, bom="E8_guard_railing") for k in range(5)]
        lines = fc.check(p, GOOD_MODELS)
        self.assertIn("FAIL", [l["verdict"] for l in lines if "infill" in l["what"]])

    def test_short_bollard_fails_and_unmeasured_does_not(self):
        m = dict(GOOD_MODELS, bollard=(0.21, 0.765, 0.21))
        self.assertIn("FAIL", [l["verdict"] for l in fc.check(good_street(), m) if l["what"] == "bollard model height"])
        m = dict(GOOD_MODELS, bollard=None)
        self.assertIn("UNMEASURED", [l["verdict"] for l in fc.check(good_street(), m)])

    def test_square_grate_fails(self):
        p = good_street()
        for x in p:
            if x["bom"] == "A7_gully_grate":
                x["sx_m"] = x["sz_m"] = 0.4
        self.assertIn("FAIL", [l["verdict"] for l in fc.check(p, GOOD_MODELS) if l["row"] == "S12"])

    def test_fourth_bin_fails(self):
        p = good_street() + [piece("prop_swing_bin_%d" % k, 20 + k, 3.65, asset="swing_bin") for k in range(1, 4)]
        self.assertIn("FAIL", [l["verdict"] for l in fc.check(p, GOOD_MODELS) if l["what"].startswith("public litter")])

    def test_recipe_plate_size_differs_but_does_not_fail(self):
        p = [x for x in good_street() if x["name"] != "name_plate_0"]
        lines = fc.check(p, GOOD_MODELS, (), (20.02, 20.92, 2.50, 2.76))
        self.assertEqual([l["verdict"] for l in lines if l["row"] == "S9"], ["DIFFERS"])
        lines = fc.check(p, GOOD_MODELS, (), (20.0, 20.98, 2.53, 2.73))
        self.assertEqual([l["verdict"] for l in lines if l["row"] == "S9"], ["PASS"])

    def test_missing_plate_and_stop_are_missing_not_fail(self):
        p = [x for x in good_street() if x["name"] not in ("name_plate_0", "bus_stop_0")]
        lines = fc.check(p, GOOD_MODELS)
        self.assertEqual({l["verdict"] for l in lines if l["row"] in ("S9", "S10")}, {"MISSING"})

    def test_blocking_piece_fails_walk(self):
        p = good_street() + [piece("dustbin9", 30.0, 4.0, 1.0, 0.6, 1.0)]
        self.assertIn("FAIL", [l["verdict"] for l in fc.check(p, GOOD_MODELS) if "dustbin9" in l["what"]])


class RealFiles(unittest.TestCase):
    @unittest.skipUnless(os.path.exists(os.path.join(ROOT, "production/specs/vignette-pieces.json")), "no street file")
    def test_runs_on_the_street(self):
        pieces, models, drawn, plate = fc.load(ROOT)
        lines = fc.check(pieces, models, drawn, plate)
        rows = {l["row"] for l in lines}
        for r in ("S1", "S5", "S6", "S7", "S9", "S10", "S11", "S12"):
            self.assertIn(r, rows)

    @unittest.skipUnless(os.path.exists(os.path.join(ROOT, "tools/art-recipes/terrace-front.py")), "no recipe")
    def test_recipe_view_is_used(self):
        pieces, models, drawn, plate = fc.load(ROOT)
        self.assertTrue(drawn, "the recipe's clutter_placements should import here")
        lines = fc.check(pieces, models, drawn, plate)
        walk = [l["what"] for l in lines if l["row"] == "W"]
        # the bin the recipe moves 0.9 m clear of column 0, and the two pieces it adds
        self.assertTrue(any("litter-bin (drawn), x 8.90" in w for w in walk))
        self.assertTrue(any(w.startswith("walker's gap at grit-bin") for w in walk))
        self.assertTrue(any(w.startswith("walker's gap at milk-crates") for w in walk))
        self.assertIn("DIFFERS", [l["verdict"] for l in lines if l["row"] == "S9"])


if __name__ == "__main__":
    unittest.main()
