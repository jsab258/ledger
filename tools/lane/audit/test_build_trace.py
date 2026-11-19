import json, tempfile, pathlib, unittest, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_trace as b


class T(unittest.TestCase):
    def test_join_render(self):
        with tempfile.TemporaryDirectory() as d:
            w = pathlib.Path(d) / "work"; w.mkdir()
            rows = [{"id": "D-A-001", "group": "A", "area": "canon", "date": "2026-11-01", "topic": "t|x", "decision": "a", "src": "s", "words": "w"},
                    {"id": "D-C-001", "group": "C", "area": "process", "date": "", "topic": "u", "decision": "b", "src": "s2", "words": ""},
                    {"id": "D-C-002", "group": "C", "area": "process", "date": "", "topic": "v", "decision": "c", "src": "s3", "words": ""}]
            (w / "decisions-merged.json").write_text(json.dumps(rows))
            (w / "status-01.json").write_text(json.dumps([{"id": "D-A-001", "status": "lost", "evidence": "e"},
                                                          {"id": "D-C-001", "status": "weird"}]))
            b.main(d)
            md = (pathlib.Path(d) / "DECISIONS-TRACE.md").read_text()
            self.assertLess(md.index("Lost"), md.index("Unclear"))
            self.assertIn("t/x", md)
            data = json.loads((pathlib.Path(d) / "decisions-trace.json").read_text())["rows"]
            st = {r["id"]: r["status"] for r in data}
            self.assertEqual(st, {"D-A-001": "lost", "D-C-001": "unclear", "D-C-002": "unclassified"})


if __name__ == "__main__":
    unittest.main()
