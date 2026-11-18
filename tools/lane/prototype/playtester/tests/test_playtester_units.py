"""Unit checks for the playtester's own judgement (no browser). Written by the cloud lane, 18 Nov 2026."""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
PT = os.path.dirname(HERE)
sys.path.insert(0, PT)
import wording  # noqa: E402
import playtest  # noqa: E402


class Wording(unittest.TestCase):
    def test_label(self):
        self.assertEqual(wording.label_of("Talk to the priest"), "the priest")
        self.assertEqual(wording.label_of("Speak to a man"), "a man")
        self.assertIsNone(wording.label_of("Go into the caff"))

    def test_sex_mismatch(self):
        self.assertEqual(wording.wording_faults("a woman", sex="m"), ["calls a man 'a woman'"])
        self.assertEqual(wording.wording_faults("the big man on the rank", sex="f"), ["calls a woman 'the big man on the rank'"])
        self.assertEqual(wording.wording_faults("the landlady at Regent House", sex="f"), [])
        self.assertEqual(wording.wording_faults("the scrap dealer", sex="m"), [])

    def test_age(self):
        self.assertTrue(wording.wording_faults("an old man mending nets", sex="m", age=40))
        self.assertFalse(wording.wording_faults("an old man mending nets", sex="m", age=71))
        self.assertTrue(wording.wording_faults("the lad on the pavement", sex="m", age=50))
        self.assertFalse(wording.wording_faults("the lad on the pavement", sex="m", age=24))

    def test_name_before_learned(self):
        self.assertTrue(wording.wording_faults("Ron Kirby", sex="m", age=58, name="Ron Kirby", name_known=False))
        self.assertFalse(wording.wording_faults("Ron Kirby", sex="m", age=58, name="Ron Kirby", name_known=True))
        self.assertFalse(wording.wording_faults("the priest", sex="m", age=61, name="Father Walsh", name_known=False))

    def test_classify_reply(self):
        stock = {"generic": ["Aye?", "Same as ever. Less of it."], "own": {"ron": ["Boss."]}, "keeperBarks": {}}
        self.assertEqual(wording.classify_reply("Boss.", "ron", stock), "own")
        self.assertEqual(wording.classify_reply("Same as ever. Less of it.", "ron", stock), "stock")
        self.assertEqual(wording.classify_reply("Something he knows.", "ron", stock), "other")


class Judging(unittest.TestCase):
    def test_novelty_stats(self):
        ev = [{"t": 0}, {"t": 100}, {"t": 700}, {"t": 2000}]
        s = playtest.novelty_stats(ev, 3600)
        self.assertEqual([w["new_things"] for w in s["windows"]], [3, 1])
        self.assertAlmostEqual(s["longest_gap_min"], 1600 / 60)
        self.assertAlmostEqual(s["longest_gap_from_min"], 2000 / 60)

    def test_layout_faults(self):
        snap = {"vw": 100, "vh": 100, "boxes": [
            {"id": "a", "x": 0, "y": 0, "w": 50, "h": 20, "text": "a", "overflow": False},
            {"id": "b", "x": 40, "y": 10, "w": 30, "h": 20, "text": "b", "overflow": False},
            {"id": "c", "x": 90, "y": 80, "w": 30, "h": 10, "text": "c", "overflow": True}]}
        kinds = sorted(f["kind"] for f in playtest.layout_faults(snap, "x"))
        self.assertEqual(kinds, ["off screen", "text spills out of its box", "words overlap"])

    def test_book_merges_runs(self):
        b = playtest.Book()
        b.add("walking", 5, "x")
        b.add("walking", 5, "x")
        b.add("talking", 3)
        self.assertEqual(b.by, {"walking": 10, "talking": 3})
        self.assertEqual(len(b.timeline), 2)
        self.assertEqual(b.t, 13)


class StockLines(unittest.TestCase):
    def test_reads_the_source(self):
        out = json.loads(subprocess.check_output(["node", os.path.join(PT, "stock_lines.mjs"),
                                                  os.path.join(PT, "..", "project", "src")]))
        self.assertIn("Aye?", out["generic"])
        self.assertIn("ron", out["own"])
        self.assertEqual(len(out["cast"]), 28)


if __name__ == "__main__":
    unittest.main()
