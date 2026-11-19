"""Plays the built prototype in headless Chromium through its own test hook (window.LEDGER).

Needs the pictures: set LEDGER_PROTO_ASSETS to a folder holding them (the files in
PUBLISHED.json "assets"; read them from the page with the Artifact tool, or keep a
copy outside git). Without it the test is skipped, never passed.
"""
import functools, http.server, os, sys, tempfile, threading, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build  # noqa: E402

ASSETS = os.environ.get("LEDGER_PROTO_ASSETS")
GL = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]


@unittest.skipUnless(ASSETS and os.path.isdir(ASSETS), "LEDGER_PROTO_ASSETS not set: pictures missing, smoke test skipped")
class Smoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        build.build(assets_dir=ASSETS, dist=cls.tmp.name)
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a):
                pass
        h = functools.partial(Quiet, directory=cls.tmp.name)
        cls.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.url = "http://127.0.0.1:%d/index.html" % cls.srv.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown(); cls.tmp.cleanup()

    def test_week_starts_and_runs_without_errors(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(args=GL)
            pg = b.new_page(viewport={"width": 1280, "height": 720})
            errors, failed = [], []
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.on("requestfailed", lambda r: failed.append(r.url) if "127.0.0.1" in r.url else None)
            pg.on("response", lambda r: failed.append(r.url) if "127.0.0.1" in r.url and r.status >= 400 else None)
            pg.goto(self.url)
            pg.wait_for_function("window.LEDGER && window.LEDGER.G", timeout=90000)
            self.assertEqual(pg.evaluate("LEDGER.G.story.phase"), "title")
            pg.evaluate("LEDGER.startNew()")
            pg.wait_for_function("LEDGER.G.story.phase === 'play'", timeout=30000)
            pos = "JSON.stringify(Object.values(LEDGER.G.people).map(p => [p.x, p.z, p.pos && p.pos.x, p.pos && p.pos.z]))"
            t0, p0 = pg.evaluate("LEDGER.G.t"), pg.evaluate(pos)
            pg.evaluate("LEDGER.step(60)")
            t1, p1 = pg.evaluate("LEDGER.G.t"), pg.evaluate(pos)
            self.assertGreater(t1, t0, "the clock must move")
            self.assertNotEqual(p0, p1, "people must move")
            self.assertGreaterEqual(pg.evaluate("Object.keys(LEDGER.G.people).length"), 10)
            shot = os.environ.get("LEDGER_PROTO_SHOT")
            if shot:
                pg.screenshot(path=shot)
            pg.evaluate("LEDGER.endWeek('silent')")
            pg.wait_for_function("LEDGER.G.story.phase === 'end'", timeout=30000)
            report = pg.evaluate("LEDGER.reportText()")
            self.assertIn("Choice: silent", report)
            b.close()
            self.assertEqual(errors, [], "page errors: %s" % errors[:3])
            self.assertEqual(failed, [], "files that did not load: %s" % failed[:3])


if __name__ == "__main__":
    unittest.main()
