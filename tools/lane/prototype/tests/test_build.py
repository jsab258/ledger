"""Build checks for the prototype, built from Fable's readable source (project/) since 18 Nov 2026.

No browser and no pictures needed. The builds need node and npm (skipped without them, never
passed); the first build installs the pinned packages once into the work folder outside the
repository (build.py), later builds take under a second.
"""
import json, os, shutil, subprocess, sys, tempfile, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import build  # noqa: E402

PUB = build.load_published()
HAVE_NODE = bool(shutil.which("node") and shutil.which("npm"))
ASSET_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".ktx2", ".glb", ".gltf", ".bin", ".hdr", ".exr",
             ".mp3", ".ogg", ".wav", ".zip")


def quiet(*a):
    pass


class BuildTests(unittest.TestCase):
    # (i) building reproduces the published ledger.js and index.html, byte for byte
    @unittest.skipUnless(HAVE_NODE, "node or npm not found: the build cannot run here")
    def test_build_reproduces_published_checksums(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(build.build(dist=d, log=quiet), [])
            for name, want in PUB["built"].items():
                p = os.path.join(d, name)
                self.assertEqual(build.sha_file(p), want["sha256"], name)
                self.assertEqual(os.path.getsize(p), want["bytes"], name)

    # (ii) every file of the readable source is under the size guard's 1,000,000 bytes
    def test_every_project_file_under_git_limit(self):
        n = 0
        for base, dirs, files in os.walk(os.path.join(ROOT, "project")):
            dirs[:] = [x for x in dirs if x not in ("node_modules", "dist")]
            for f in files:
                n += 1
                self.assertLess(os.path.getsize(os.path.join(base, f)), 1_000_000, os.path.join(base, f))
        self.assertGreater(n, 40, "project/ looks empty")

    # (iii) no picture or rig file in git (tracked, or untracked and not ignored, so ready to be added)
    def test_no_asset_files_in_git(self):
        if not shutil.which("git"):
            self.skipTest("git not found")
        try:
            out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "."],
                                 cwd=ROOT, check=True, capture_output=True, text=True).stdout.split("\n")
        except subprocess.CalledProcessError:
            self.skipTest("not a git checkout")
        names = {a["path"] for a in PUB["assets"]}
        bad = [p for p in out if p and (os.path.basename(p) in names or p.lower().endswith(ASSET_EXT))]
        self.assertEqual(bad, [], "asset files in git under tools/lane/prototype")

    # (iv) check_assets names a missing file and a changed one
    def test_check_assets_reports_missing_and_changed(self):
        with tempfile.TemporaryDirectory() as d:
            first, second = PUB["assets"][0]["path"], PUB["assets"][1]["path"]
            with open(os.path.join(d, first), "wb") as f:
                f.write(b"not the published picture")
            probs = build.check_assets(d, PUB)
            self.assertIn("asset differs from the page: " + first, probs)
            self.assertIn("missing asset: " + second, probs)
            self.assertEqual(len(probs), len(PUB["assets"]))

    # (v) dist/publish-files.json names ledger.js and the page, built on PUBLISHED.json's version
    @unittest.skipUnless(HAVE_NODE, "node or npm not found: the build cannot run here")
    def test_publish_map_names_script_and_page_and_pins_version(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(build.build(dist=d, log=quiet), [])
            with open(os.path.join(d, "publish-files.json"), encoding="utf-8") as f:
                pub = json.load(f)
        self.assertEqual(pub["page"], PUB["page"])
        self.assertEqual(pub["built_on_version"], PUB["version"])
        self.assertEqual(list(pub["files"]), ["ledger.js"], "only the script beside the page")
        self.assertTrue(pub["files"]["ledger.js"].endswith("/ledger.js"))
        self.assertTrue(pub["file_path"].endswith("/index.html"))
        for a in PUB["assets"]:
            self.assertNotIn(a["path"], pub["files"])  # an update keeps them on the page

    # (vi) the readable source still defines the test hook
    def test_hook_js_defines_the_test_hook(self):
        with open(os.path.join(ROOT, "project", "src", "hook.js"), encoding="utf-8") as f:
            hook = f.read()
        self.assertIn("window.LEDGER = hook;", hook)
        for key in ("startNew:", "step: stepBy,", "saveNow:", "reportText:", "simStep:", "restore:",
                    "rules: RULES,", "talk,", "fare,", "ledger,"):
            self.assertIn(key, hook)

    # An edited source no longer matches the page: refused unless allowed.
    @unittest.skipUnless(HAVE_NODE, "node or npm not found: the build cannot run here")
    def test_edited_source_is_refused_unless_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            proj = os.path.join(tmp, "project")
            shutil.copytree(os.path.join(ROOT, "project"), proj,
                            ignore=shutil.ignore_patterns("node_modules", "dist"))
            with open(os.path.join(proj, "src", "main.js"), "a", encoding="utf-8") as f:
                f.write("\nconsole.log('edited');\n")
            orig = build.PROJECT
            build.PROJECT = proj
            try:
                d = os.path.join(tmp, "dist")
                probs = build.build(dist=d, log=quiet)
                self.assertTrue(any(p.startswith("ledger.js differs") for p in probs), probs)
                self.assertFalse(os.path.exists(os.path.join(d, "ledger.js")), "a refused build writes nothing")
                self.assertTrue(build.build(dist=d, allow_changed=True, log=quiet))
                self.assertTrue(os.path.exists(os.path.join(d, "ledger.js")))
            finally:
                build.PROJECT = orig


if __name__ == "__main__":
    unittest.main()
