"""Build checks for the prototype source project (no browser, no pictures needed)."""
import hashlib, json, os, sys, tempfile, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import build  # noqa: E402

M = build.load_manifest()


class BuildTests(unittest.TestCase):
    def test_rebuild_is_byte_identical_to_published(self):
        with tempfile.TemporaryDirectory() as d:
            r = build.build(dist=d)
            self.assertEqual(r["changed"], [])
            with open(os.path.join(d, "ledger.js"), "rb") as f:
                data = f.read()
            self.assertEqual(hashlib.sha256(data).hexdigest(), M["code"]["ledger.js"]["sha256"])
            self.assertEqual(len(data), M["code"]["ledger.js"]["bytes"])

    def test_every_source_file_under_git_limit(self):
        for base, _, files in os.walk(os.path.join(ROOT, "src")):
            for f in files:
                self.assertLess(os.path.getsize(os.path.join(base, f)), 1_000_000, f)

    def test_publish_map_names_only_code_and_pins_version(self):
        with tempfile.TemporaryDirectory() as d:
            build.build(dist=d)
            with open(os.path.join(d, "publish-files.json")) as f:
                pub = json.load(f)
            self.assertEqual(pub["page"], M["page"])
            for a in M["assets"]:
                self.assertNotIn(a["path"], pub["files"])  # an update keeps them
                self.assertEqual(pub["files_for_a_new_page"][a["path"]], {"artifact": M["page"], "path": a["path"]})
            self.assertTrue(pub["files"]["ledger.js"].endswith("/ledger.js"))
            self.assertEqual(pub["built_on_version"], M["version"])

    def test_page_names_its_script_and_rig(self):
        with open(os.path.join(ROOT, "src", "index.html"), encoding="utf-8") as f:
            page = f.read()
        self.assertIn('src="ledger.js"', page)
        script = build.join_parts(M).decode("utf-8", "replace")
        for name in ("people.txt", "people.jpg", "people_lo.jpg"):
            self.assertIn(name, script)
            self.assertIn(name, [a["path"] for a in M["assets"]])

    def test_edited_source_is_refused_unless_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            orig = build.join_parts
            build.join_parts = lambda m: orig(m) + b"\n//edit"
            try:
                with self.assertRaises(SystemExit):
                    build.build(dist=d)
                r = build.build(dist=d, allow_changed=True)
                self.assertTrue(r["changed"])
            finally:
                build.join_parts = orig

    def test_test_hook_present(self):
        script = build.join_parts(M).decode("utf-8", "replace")
        for key in ("window.LEDGER=", "startNew:", "step:", "saveNow:", "reportText:", "simStep:"):
            self.assertIn(key, script)


if __name__ == "__main__":
    unittest.main()
