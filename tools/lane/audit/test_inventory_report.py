import json, tempfile, pathlib, unittest, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import inventory_report as r


def folder(p, st="live", size=10):
    return {"path": p, "depth": p.count("/") + 1, "size_bytes": size, "file_count_total": 1, "purpose": "x|y", "owner": "o",
            "last_commit": "2026-11-01", "referenced_by_incl_descendants": 0, "status": st, "status_reason": "r", "duplicates": []}


class T(unittest.TestCase):
    def test_render(self):
        with tempfile.TemporaryDirectory() as d:
            inv = {"made": "2026-11-19T00:00", "newest_commit": "2026-11-19", "shallow": False,
                   "folders": [folder("a", size=100), folder("a/b", "dead"), folder("a/b/c", "dead")]}
            (pathlib.Path(d) / "inventory.json").write_text(json.dumps(inv))
            r.main(d)
            md = (pathlib.Path(d) / "INVENTORY.md").read_text()
            self.assertIn("## a/", md)
            self.assertIn("- a/b/c", md)
            self.assertIn("Not yet read", md)
            (pathlib.Path(d) / "pc-inventory.json").write_text(json.dumps({"made": "2026-11-19", "folders": [{"path": "F:\\X", "size_gb": 1, "referenced_by": []}]}))
            r.main(d)
            self.assertIn("Named by nothing", (pathlib.Path(d) / "INVENTORY.md").read_text())


if __name__ == "__main__":
    unittest.main()
