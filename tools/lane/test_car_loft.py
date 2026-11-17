"""Tests for the loft generator (python -m pytest tools/lane/test_car_loft.py, or run directly)."""
import math
import os
import sys
import tempfile
import unittest
from dataclasses import replace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_loft as c  # noqa: E402


class LoftTests(unittest.TestCase):
    def setUp(self):
        self.p = c.HatchParams()

    def test_default_passes_every_check(self):
        self.assertEqual(c.check(self.p), [])

    def test_twelve_stations_in_order_with_fixed_topology(self):
        st = c.build(self.p)
        self.assertEqual(len(st), 12)
        xs = [s["x"] for s in st]
        self.assertEqual(xs, sorted(xs))
        self.assertEqual(len(set(xs)), 12)
        for s in st:
            self.assertEqual(len(s["half_section"]), len(c.SECTION_POINTS))

    def test_measured_size_matches_the_numbers_given(self):
        m = c.measure(self.p)
        self.assertAlmostEqual(m["length"], self.p.length, places=3)
        self.assertAlmostEqual(m["width"], self.p.width, places=3)
        self.assertAlmostEqual(m["height"], self.p.height, places=3)

    def test_glass_only_between_screen_and_hatch(self):
        d = self.p.derived()
        for s in c.build(self.p):
            inside = d["screen_base"] + 1e-4 < s["x"] < d["hatch_base"] - 1e-4
            self.assertEqual(s["glass"], inside, s["name"])

    def test_glasshouse_narrows_to_the_roof(self):
        st = {s["name"]: s for s in c.build(self.p)}
        hs = st["b_pillar"]["half_section"]
        belt_y = hs[c.SECTION_POINTS.index("belt")][0]
        cant_y = hs[c.SECTION_POINTS.index("cant")][0]
        self.assertAlmostEqual(belt_y - cant_y, self.p.glass_inset, places=3)

    def test_loop_is_mirrored_and_closed_without_doubles(self):
        s = c.build(self.p)[5]
        loop = c.full_loop(s)
        self.assertEqual(len(loop), 2 * (len(c.SECTION_POINTS) - 1))
        ys = sorted(round(y, 6) for _, y, _ in loop if abs(y) > 1e-9)
        self.assertEqual(ys, sorted(-y for y in ys))
        self.assertEqual(len(set(loop)), len(loop))

    def test_out_of_class_length_fails(self):
        bad = replace(self.p, length=4.6)
        self.assertTrue(any("length" in f for f in c.check(bad)))

    def test_too_tall_fails(self):
        bad = replace(self.p, height=1.55)
        self.assertTrue(any("height" in f for f in c.check(bad)))

    def test_upright_screen_breaks_order_or_ratio(self):
        # a near-flat screen pushes the roof's front past its back
        bad = replace(self.p, screen_rake_deg=8.0)
        self.assertTrue(c.check(bad))

    def test_wide_track_fails(self):
        bad = replace(self.p, track=1.60)
        self.assertTrue(any("stick out" in f for f in c.check(bad)))

    def test_triangle_budget(self):
        self.assertLessEqual(c.measure(self.p)["triangles_estimate"], c.TRIANGLE_BUDGET)
        heavy = replace(self.p, subdivision_levels=4)
        self.assertTrue(any("budget" in f for f in c.check(heavy)))

    def test_ratios_within_the_eight_real_cars(self):
        m = c.measure(self.p)
        self.assertTrue(0.329 <= m["height_over_length"] <= 0.370)
        self.assertTrue(0.600 <= m["wheelbase_over_length"] <= 0.645)

    def test_class_extremes_still_build(self):
        # the shortest and the longest of the class both make a valid car
        for L, wb in ((3.96, 2.44), (4.24, 2.55)):
            q = replace(self.p, length=L, wheelbase=wb)
            fails = [f for f in c.check(q) if "over_length" not in f]
            self.assertEqual(fails, [], (L, wb, fails))

    def test_views_write_four_svgs(self):
        with tempfile.TemporaryDirectory() as d:
            names = c.write_views(self.p, d)
            self.assertEqual(names, ["front", "rear", "side", "three-quarter"])
            for n in names:
                with open(os.path.join(d, "hatch-%s.svg" % n)) as f:
                    txt = f.read()
                self.assertTrue(txt.startswith("<svg"))
                self.assertIn("polygon", txt)

    def test_some_glass_faces_and_mostly_paint(self):
        q = c.quads(self.p)
        g = sum(1 for _, flag in q if flag)
        self.assertGreater(g, 4)
        self.assertLess(g, len(q) / 2)

    def test_round3_proposal_passes_checks_and_drops_the_roof(self):
        q = c.HatchParams(**c.ROUND3_PROPOSAL)
        self.assertEqual(c.check(q), [])
        st = {s["name"]: s for s in c.build(q)}
        self.assertLess(st["roof_back"]["half_section"][-1][1], st["roof_front"]["half_section"][-1][1])


if __name__ == "__main__":
    unittest.main()
