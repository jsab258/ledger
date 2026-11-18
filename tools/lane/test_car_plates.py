"""Tests for car_plates.py (lane session, 17 November 2026).

Run from the repo root: python3 -m unittest tools/lane/test_car_plates.py
"""
import json
import os
import re
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_plates as cp  # noqa: E402

SVG_NS = "{http://www.w3.org/2000/svg}"


class TestRegistrations(unittest.TestCase):
    def setUp(self):
        self.regs = cp.generate_registrations(seed=7, count=500)

    def test_format(self):
        pat = re.compile(r"^[A-G][1-9][0-9]{1,2} [A-Z]{3}$")
        for reg in self.regs:
            self.assertRegex(reg, pat)
            self.assertTrue(cp.is_valid_registration(reg), reg)

    def test_forbidden_letters(self):
        for reg in self.regs:
            self.assertNotIn(reg[0], "IOQUZ", reg)
            for ch in reg.split(" ")[1]:
                self.assertNotIn(ch, "IQZ", reg)

    def test_year_letters_spread(self):
        years = {r[0] for r in self.regs}
        self.assertTrue(years <= set("ABCDEFG"))
        self.assertGreaterEqual(len(years), 6)

    def test_h_only_after_august_1990(self):
        import datetime
        early = cp.generate_registrations(1, 2000, game_date=datetime.date(1990, 7, 31))
        self.assertNotIn("H", {r[0] for r in early})
        late = cp.generate_registrations(1, 2000, game_date=datetime.date(1990, 8, 1))
        self.assertIn("H", {r[0] for r in late})
        flagged = cp.generate_registrations(1, 2000, allow_h=True)
        self.assertIn("H", {r[0] for r in flagged})

    def test_numbers_and_triples(self):
        regs = cp.generate_registrations(seed=42, count=20000)
        for reg in regs:
            n = int(reg.split(" ")[0][1:])
            self.assertGreaterEqual(n, 21, reg)
            self.assertNotIn(n, (69, 666), reg)
            s = reg.split(" ")[1]
            self.assertFalse(s[0] == s[1] == s[2], reg)
        for bad in ("F8 CYW", "C20 KKU", "E69 ABC", "B666 ABC", "D678 HHH"):
            self.assertFalse(cp.is_valid_registration(bad), bad)
        self.assertTrue(cp.is_valid_registration("C21 KKU"))

    def test_count_limits(self):
        with self.assertRaises(ValueError):
            cp.generate_registrations(1, -1)
        with self.assertRaises(ValueError):
            cp.generate_registrations(1, cp.capacity() // 2 + 1)
        with self.assertRaises(ValueError):
            cp.generate_registrations(None, 5)
        self.assertEqual(cp.generate_registrations(1, 0), [])

    def test_unique(self):
        self.assertEqual(len(self.regs), len(set(self.regs)))

    def test_deterministic(self):
        self.assertEqual(self.regs, cp.generate_registrations(seed=7, count=500))
        self.assertNotEqual(self.regs, cp.generate_registrations(seed=8, count=500))

    def test_blocklist_honoured(self):
        regs = cp.generate_registrations(seed=123, count=3000)
        for reg in regs:
            self.assertNotIn(reg.split(" ")[1], cp.BLOCKLIST, reg)
        self.assertFalse(cp.is_valid_registration("G123 BUM"))
        self.assertFalse(cp.is_valid_registration("G123 GIN"))
        for word in ("WOG FAG FGT PAK WOP POM NIG KEG SOT TOT VAT LSD POT DOP "
                     "UDA UVF IRA BNP KGB PRK TWT YOB").split():
            self.assertIn(word, cp.BLOCKLIST)
            self.assertFalse(cp.is_valid_registration(f"G123 {word}"), word)
        self.assertNotIn("BEER", cp.BLOCKLIST)
        self.assertTrue(all(len(w) == 3 for w in cp.BLOCKLIST))

    def test_validator_rejects_bad(self):
        for bad in ("I123 ABC", "O32 ABC", "Z31 ABC", "G0 ABC", "G1234 ABC",
                    "G123 AQC", "G123 ABZ", "G123ABC", "J123 ABC"):
            self.assertFalse(cp.is_valid_registration(bad), bad)


class TestLayout(unittest.TestCase):
    def test_fit_and_margins(self):
        for reg in cp.generate_registrations(seed=1, count=300) + ["H888 WXY", "A21 ABC"]:
            boxes = cp.layout(reg, (520, 111))
            left = boxes[0]["x"]
            right = 520 - (boxes[-1]["x"] + boxes[-1]["w"])
            top = boxes[0]["y"]
            bottom = 111 - (top + boxes[0]["h"])
            for m in (left, right, top, bottom):
                self.assertGreaterEqual(m, 11.0, reg)
            self.assertAlmostEqual(left, right, places=3)
            self.assertAlmostEqual(top, bottom, places=3)

    def test_widest_plate_numbers(self):
        self.assertEqual(cp.text_width("G888 ABC"), 7 * 57 + 5 * 11 + 33)
        self.assertEqual(cp.text_width("G888 ABC"), 487)

    def test_spacing(self):
        boxes = cp.layout("G123 ABC")
        gaps = [boxes[i + 1]["x"] - (boxes[i]["x"] + boxes[i]["w"]) for i in range(6)]
        self.assertEqual([round(g, 3) for g in gaps], [11, 11, 11, 33, 11, 11])

    def test_too_small_plate_raises(self):
        with self.assertRaises(cp.PlateFitError):
            cp.layout("G888 ABC", (480, 111))
        with self.assertRaises(cp.PlateFitError):
            cp.layout("G888 ABC", (520, 95))

    def test_char_widths(self):
        for reg in cp.generate_registrations(seed=2, count=300):
            for b in cp.layout(reg):
                if b["char"] == "1":
                    self.assertLess(b["w"], 57)
                else:
                    self.assertEqual(b["w"], 57, b)
                self.assertEqual(b["h"], 79)

    def test_glyphs_inside_box(self):
        half = cp.STROKE / 2
        for ch, lines in cp.GLYPHS.items():
            w = cp.char_width(ch)
            for line in lines:
                self.assertGreaterEqual(len(line), 2)
                for x, y in line:
                    self.assertTrue(half - 1e-9 <= x <= w - half + 1e-9, (ch, x))
                    self.assertTrue(half - 1e-9 <= y <= 79 - half + 1e-9, (ch, y))

    def test_every_used_char_has_glyph(self):
        needed = set("ABCDEFGH") | set(cp.SERIAL_LETTERS) | set("0123456789")
        self.assertTrue(needed <= set(cp.GLYPHS), needed - set(cp.GLYPHS))


class TestOutput(unittest.TestCase):
    def test_svg_well_formed(self):
        for side, colour in (("front", "#ffffff"), ("rear", cp.PLATE_COLOURS["rear"])):
            root = ET.fromstring(cp.plate_svg("G123 ABC", side))
            self.assertEqual(root.tag, SVG_NS + "svg")
            rect = root.find(SVG_NS + "rect")
            self.assertEqual(rect.get("fill"), colour)
            self.assertGreater(len(root.iter(SVG_NS + "polyline").__next__().get("points")), 0)
        self.assertNotEqual(cp.PLATE_COLOURS["front"], cp.PLATE_COLOURS["rear"])

    def test_json_round_trip(self):
        data = cp.plate_data("F42 KLM", "front")
        back = json.loads(cp.plate_json("F42 KLM", "front"))
        self.assertEqual(back, json.loads(json.dumps(data)))
        self.assertEqual(back["registration"], "F42 KLM")
        self.assertEqual(back["colour"], "#ffffff")
        self.assertEqual(len(back["characters"]), 6)
        self.assertEqual([c["char"] for c in back["characters"]], list("F42KLM"))

    def test_bad_side(self):
        with self.assertRaises(ValueError):
            cp.plate_data("G123 ABC", "side")
        with self.assertRaises(ValueError):
            cp.plate_svg("G123 ABC", "side")

    def test_output_validates(self):
        for bad in ("G123 BUM", "H1", "G123  ABC", "G5 ABC"):
            for fn in (cp.plate_data, cp.plate_svg, cp.plate_json, cp.layout):
                with self.assertRaises(ValueError, msg=(fn.__name__, bad)):
                    fn(bad)

    def test_main_pass(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cp.main(["--seed", "5", "--count", "40"])
        self.assertEqual(rc, 0)
        self.assertIn("PASS", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
