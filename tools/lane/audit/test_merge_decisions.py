import json, tempfile, pathlib, unittest, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import merge_decisions as m


class T(unittest.TestCase):
    def test_merge_and_batches(self):
        with tempfile.TemporaryDirectory() as d:
            w = pathlib.Path(d) / "work"; w.mkdir()
            (w / "dec-A-x.jsonl").write_text('{"src":"a","date":"2026-11-01","topic":"t1","area":"canon","decision":"x"}\n\n{"src":"b","area":"weird","topic":"t2","decision":"y"}\n')
            (w / "dec-C-y.jsonl").write_text('{"src":"c","area":"canon","topic":"t0","decision":"z","in_force_text":true,"enforcers":["e"]}\n')
            rows = m.load(w)
            self.assertEqual([r["id"] for r in rows], ["D-A-001", "D-A-002", "D-C-001"])
            self.assertEqual(rows[1]["area"], "other")
            self.assertEqual(rows[2]["enforcers"], ["e"])
            self.assertEqual(rows[1]["words"], "")
            b = m.batches(rows, size=2)
            self.assertEqual(sum(len(x) for x in b), 3)
            self.assertEqual(b[0][0]["topic"], "t0")  # sorted by topic within area
            m.main(d)
            self.assertTrue((w / "decisions-merged.json").exists())
            self.assertTrue((w / "batch-01.json").exists())


if __name__ == "__main__":
    unittest.main()
