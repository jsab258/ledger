"""Tests for car_kit.py (lane session, 17 November 2026).

Run from the repository root: python3 -m unittest tools/lane/test_car_kit.py
"""
import json
import os
import sys
import unittest
from dataclasses import replace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_kit  # noqa: E402
from car_loft import HatchParams, ROUND3_PROPOSAL  # noqa: E402


class CarKitTest(unittest.TestCase):
    def setUp(self):
        self.p = HatchParams()
        self.kit = car_kit.derive(self.p)

    def test_default_and_round3_pass(self):
        self.assertEqual(car_kit.check(self.p), [])
        self.assertEqual(car_kit.check(HatchParams(**ROUND3_PROPOSAL)), [])

    def test_four_wheels_mirrored(self):
        w = {q["name"]: q for q in self.kit["wheels"]}
        self.assertEqual(sorted(w), ["FL", "FR", "RL", "RR"])
        for f, r in (("FL", "FR"), ("RL", "RR")):
            self.assertAlmostEqual(w[f]["hub"][1], -w[r]["hub"][1])
            self.assertGreater(w[f]["hub"][1], 0)
            self.assertEqual(w[f]["hub"][0], w[r]["hub"][0])
        self.assertEqual(len({q["bone"] for q in w.values()}), 4)
        self.assertEqual(w["FL"]["radius"], self.p.wheel_radius)
        self.assertEqual(w["FL"]["width"], self.p.tyre_width)

    def test_right_hand_drive_seat(self):
        self.assertLess(self.kit["sockets"]["driver_seat"]["pos"][1], 0)
        self.assertLess(self.kit["sockets"]["camera_driver_head"]["pos"][1], 0)

    def test_collision_count_and_bounds(self):
        boxes = self.kit["collision"]
        self.assertLessEqual(len(boxes), 6)
        m = car_kit.measure(self.p)
        for b in boxes:
            c, h = b["centre"], b["half_extent"]
            self.assertGreaterEqual(c[0] - h[0], -car_kit.BOX_MARGIN)
            self.assertLessEqual(c[0] + h[0], self.p.length + car_kit.BOX_MARGIN)
            self.assertLessEqual(h[1], m["width"] / 2 + car_kit.BOX_MARGIN)
            self.assertLessEqual(c[2] + h[2], m["height"] + car_kit.BOX_MARGIN)
            self.assertGreaterEqual(c[1] - h[1], -m["width"] / 2 - car_kit.BOX_MARGIN)
            self.assertGreaterEqual(c[2] - h[2], self.p.keel_z - car_kit.BOX_MARGIN)
        self.assertGreaterEqual(car_kit.box_side_cover(self.p, boxes), 0.85)

    def test_panels_have_bands_and_hinges(self):
        pn = {q["name"]: q for q in self.kit["panels"]}
        for q in pn.values():
            self.assertLess(q["x"][0], q["x"][1])
            self.assertLess(q["z"][0], q["z"][1])
            self.assertIn(q["material"], car_kit.MATERIALS)
        for n in ("bonnet", "tailgate", "front_door_left", "rear_door_right"):
            self.assertIn("hinge", pn[n])

    def test_tailgate_holds_its_glass(self):
        for p in (self.p, HatchParams(**ROUND3_PROPOSAL)):
            kit = car_kit.derive(p)
            tg = [q for q in kit["panels"] if q["name"] == "tailgate"][0]
            rs = [g for g in kit["glass"] if g["name"] == "rear_screen"][0]
            self.assertLessEqual(tg["x"][0], rs["x"][0])
            self.assertGreaterEqual(tg["x"][1], rs["x"][1])
            self.assertLessEqual(tg["z"][0], rs["z"][0])
            self.assertGreaterEqual(tg["z"][1], rs["z"][1])

    def _bad(self, kit, text):
        fails = car_kit.check(self.p, kit)
        self.assertTrue(any(text in f for f in fails), fails)

    def test_wrong_data_fails(self):
        cases = [
            (lambda k: k["wheels"][0]["hub"].__setitem__(2, 0.5), "hub height"),
            (lambda k: k["wheels"][2].__setitem__("steers", True), "front wheels only"),
            (lambda k: k["wheels"][1].__setitem__("spin_axis", [1.0, 0.0, 0.0]), "spin axis"),
            (lambda k: k["wheels"][1]["hub"].__setitem__(1, -0.6), "not mirrored"),
            (lambda k: k["collision"][1]["centre"].__setitem__(1, -0.3), "outside the body bounds"),
            (lambda k: k["collision"][1]["centre"].__setitem__(2, 0.1), "outside the body bounds"),
            (lambda k: k.__setitem__("collision", [b for b in k["collision"] if b["name"] != "cabin"]),
             "side area"),
            (lambda k: k.__setitem__("panels", [q for q in k["panels"] if q["name"] != "front_door_left"]),
             "in no panel"),
            (lambda k: [q for q in k["panels"] if q["name"] == "rear_bumper"][0]["z"].__setitem__(1, 0.7),
             "overlap"),
            (lambda k: [q for q in k["panels"] if q["name"] == "tailgate"][0]["x"].__setitem__(1, 3.9),
             "not inside its panel"),
            (lambda k: k["sockets"]["driver_seat"]["pos"].__setitem__(0, 2.6), "front door's span"),
            (lambda k: k["sockets"]["driver_seat"]["pos"].__setitem__(1, -0.7), "shoulders"),
            (lambda k: k["sockets"]["door_handle_front_left"]["pos"].__setitem__(0, 2.4), "not on the front door"),
            (lambda k: k["sockets"].pop("door_handle_rear_right"), "door_handle_rear_right missing"),
            (lambda k: k["sockets"]["tail_lamp_left"].pop("material"), "lens material"),
            (lambda k: k["materials"].remove("lens"), "material slots"),
            (lambda k: k["mass_and_size"].__setitem__("kerb_mass_kg", 1200.0), "kerb mass"),
            (lambda k: k["mass_and_size"]["centre_of_mass"].__setitem__(0, 2.4), "forward of mid-wheelbase"),
            (lambda k: k["mass_and_size"]["centre_of_mass"].__setitem__(2, 0.9), "not low"),
        ]
        for change, text in cases:
            kit = car_kit.derive(self.p)
            change(kit)
            with self.subTest(text=text):
                self._bad(kit, text)

    def test_seat_and_handle_follow_b_pillar(self):
        p = replace(self.p, screen_base_x=1.10, wheelbase=2.35)
        kit = car_kit.derive(p)
        ln = car_kit.lines(p)
        self.assertLess(kit["sockets"]["driver_seat"]["pos"][0], ln["b_line"])
        h = kit["sockets"]["door_handle_front_left"]["pos"][0]
        self.assertTrue(ln["a_line"] < h < ln["b_line"])
        r = kit["sockets"]["door_handle_rear_left"]["pos"][0]
        self.assertTrue(ln["b_line"] < r < ln["rear_door_end"])
        kit_fails = [f for f in car_kit.check(p) if not f.startswith("loft:")]
        self.assertEqual(kit_fails, [])

    def test_wheel_details(self):
        for q in self.kit["wheels"]:
            self.assertAlmostEqual(q["hub"][2], q["radius"])
            self.assertEqual(q["spin_axis"], [0.0, 1.0, 0.0])
            front = q["name"].startswith("F")
            self.assertEqual(q["steers"], front)
            self.assertEqual(q["driven"], front)

    def test_materials_and_lamps(self):
        self.assertEqual(set(self.kit["materials"]),
                         {"paint", "glass", "chrome", "black_plastic", "rubber", "lens", "plate", "interior"})
        lamps = [n for n in self.kit["sockets"] if n.startswith(car_kit.LAMP_PREFIXES)]
        self.assertEqual(len(lamps), 12)
        for n in lamps:
            self.assertEqual(self.kit["sockets"][n]["material"], "lens")
            self.assertIn("glow", self.kit["sockets"][n])

    def test_sockets_present_and_unique(self):
        s = self.kit["sockets"]
        for n in ("headlamp_left", "tail_lamp_right", "brake_lamp_left", "indicator_front_right",
                  "indicator_rear_left", "plate_front", "plate_rear", "driver_seat",
                  "camera_driver_head", "camera_chase_anchor", "engine_sound", "exhaust", "interior",
                  "door_handle_front_left", "door_handle_rear_left", "door_handle_rear_right"):
            self.assertIn(n, s)
        self.assertEqual(s["plate_rear"]["size"], [0.520, 0.111])
        names = list(s) + [g["name"] for g in self.kit["glass"]] + [q["name"] for q in self.kit["panels"]]
        self.assertEqual(len(names), len(set(names)))

    def test_glass_slots(self):
        names = {g["name"] for g in self.kit["glass"]}
        self.assertTrue({"windscreen", "front_side_window_left", "front_side_window_right",
                         "rear_side_window_left", "rear_side_window_right", "rear_screen"} <= names)

    def test_json_round_trip(self):
        again = json.loads(json.dumps(self.kit))
        self.assertEqual(again, json.loads(json.dumps(again)))
        self.assertEqual(again["wheels"][0]["bone"], self.kit["wheels"][0]["bone"])

    def test_main_writes_json(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "kit.json")
            self.assertEqual(car_kit.main(["--out", path]), 0)
            with open(path) as f:
                self.assertEqual(len(json.load(f)["wheels"]), 4)

    def test_tiny_arch_fails(self):
        fails = car_kit.check(replace(self.p, arch_clearance=0.005))
        self.assertTrue(any("arch lip gap" in f for f in fails), fails)

    def test_huge_wheel_fails(self):
        fails = car_kit.check(replace(self.p, wheel_radius=0.42))
        self.assertTrue(any("wheelhouse room" in f for f in fails), fails)


if __name__ == "__main__":
    unittest.main()
