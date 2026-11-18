"""Why Ron stops about 3 m from the rank after 23:36 (systems2_test.py, test_3b2), checked by running it.

The hand reading (production/lane/PROTOTYPE-RULES-READ-2026-11-18.md, round two, section 11) says:
from 23:30 Tom being out on the street counts as an act ("night out", severity 0.35); a moving person
who sees an act within 26 m is paused 0.9 + 1.6 x severity = 1.46 real seconds, and a watcher's
attention refills in 0.36 to 1.3 s, so the pause is topped up before it runs out while Tom is near
and in sight.

Two runs, each in its own fresh page, same set-up as systems2_test.py (headless Chromium, the hook
only, the clock stopped between steps; LEDGER_PROTO_ASSETS needed, skipped otherwise):
  near  Tom left where the new week puts him (about 16 m from the rank, in the open): Ron sets off at
        23:36, his pause (LEDGER.G.people.ron.pauseT) keeps being set back up to 1.46 s, he moves
        under a metre and is still on the street at 02:00.
  far   Tom moved 60 m down Quay Street at 23:30, before Ron sets off: Ron's pause is never set and
        he gets home.
Run with: python -m pytest tests/ronstop_test.py
"""
import functools, http.server, os, sys, tempfile, threading
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build  # noqa: E402

ASSETS = os.environ.get("LEDGER_PROTO_ASSETS")
GL = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
HOUR = 45  # LEDGER.step seconds per game hour
SEV_PAUSE = 0.9 + 1.6 * 0.35  # 1.46 s, the pause a "night out" sighting sets

pytestmark = pytest.mark.skipif(not (ASSETS and os.path.isdir(ASSETS)),
                                reason="LEDGER_PROTO_ASSETS not set: pictures missing, skipped")

RON = """(() => { const r = LEDGER.G.people.ron, t = LEDGER.G.tom;
  return {t: LEDGER.G.t, x: r.x, z: r.z, space: r.space, moving: r.moving, pause: r.pauseT || 0,
          goal: r.goalKey, d: Math.hypot(r.x - t.x, r.z - t.z)}; })()"""


@pytest.fixture(scope="module")
def page_factory():
    from playwright.sync_api import sync_playwright
    tmp = tempfile.TemporaryDirectory()
    build.build(assets_dir=ASSETS, dist=tmp.name)

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=tmp.name))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    pw = sync_playwright().start()
    b = pw.chromium.launch(args=GL)
    pages = []

    def new_week():
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto("http://127.0.0.1:%d/index.html" % srv.server_address[1])
        pg.wait_for_function("window.LEDGER && window.LEDGER.G", timeout=90000)
        pg.evaluate("LEDGER.startNew()")
        pg.wait_for_function("LEDGER.G.story.phase === 'play'", timeout=30000)
        pg.evaluate("window.LEDGER_MANUAL = true; window.LEDGER_NORENDER = true")
        pages.append(pg)
        return pg, errors
    yield new_week
    try:
        b.close(); pw.stop()
    finally:
        srv.shutdown(); srv.server_close(); tmp.cleanup()


def step_to(pg, minute):
    """Step the clock to game minute `minute` of Monday's night (a bit at a time, as systems2_test)."""
    for _ in range(400):
        pg.wait_for_function("!LEDGER.G.paused && !LEDGER.talk.state().on", timeout=60000)
        now = pg.evaluate("LEDGER.G.t")
        if now >= minute - 0.5:
            return
        pg.evaluate("LEDGER.step(%f)" % (min(60, minute - now) / 60 * HOUR))
    raise AssertionError("clock did not reach %s" % minute)


def watch(pg, until):
    """Step in small slices (0.1 real s each) to game minute `until`, recording Ron each slice."""
    rows = []
    while pg.evaluate("LEDGER.G.t") < until - 0.05:
        pg.evaluate("LEDGER.step(0.1)")
        rows.append(pg.evaluate(RON))
    return rows


def refreshes(rows):
    """How many times the pause was set back up (rose between two slices)."""
    return sum(1 for a, b in zip(rows, rows[1:]) if b["pause"] > a["pause"] + 1e-6)


def test_near_ron_is_held_by_an_endless_witness_pause(page_factory):
    pg, errors = page_factory()
    step_to(pg, 23 * 60 + 30)
    r0 = pg.evaluate(RON)
    assert r0["goal"] != "home|sleep" and r0["d"] < 26, "set-up: Ron still on the rank, Tom within 26 m"
    rows = watch(pg, 23 * 60 + 50)  # 23:30 to 23:50, about 15 real seconds in 0.1 s slices
    walking = [r for r in rows if r["goal"] == "home|sleep"]
    assert walking, "Ron sets off home after 23:36"
    moved = max(((r["x"] - r0["x"]) ** 2 + (r["z"] - r0["z"]) ** 2) ** 0.5 for r in rows)
    held = [r for r in walking if r["pause"] > 0]
    print("near: Tom %.1f m away; slices walking %d, paused %d; pause max %.2f; refreshes %d; moved %.2f m"
          % (r0["d"], len(walking), len(held), max(r["pause"] for r in walking), refreshes(walking), moved))
    assert max(r["pause"] for r in walking) == pytest.approx(SEV_PAUSE, abs=0.01), "the pause is the night-out one"
    assert len(held) >= len(walking) - 3, "after the first second Ron is paused in every slice"
    assert refreshes(walking) >= 5, "the pause keeps being topped up before it runs out"
    assert all(r["moving"] for r in walking), "still marked as walking"
    assert moved < 3.5
    step_to(pg, 24 * 60 + 120)  # Tuesday 02:00
    end = pg.evaluate(RON)
    print("near: at 02:00 Ron space %s, pause %.2f, moved %.2f m" % (
        end["space"], end["pause"], ((end["x"] - r0["x"]) ** 2 + (end["z"] - r0["z"]) ** 2) ** 0.5))
    assert end["space"] == "street" and end["moving"], "the stop reproduced: still walking on the street at 02:00"
    assert errors == []


def test_far_ron_gets_home_when_tom_is_out_of_range(page_factory):
    pg, errors = page_factory()
    step_to(pg, 23 * 60 + 30)
    pg.evaluate("LEDGER.G.tom.x = -5.4; LEDGER.G.tom.z = -32")  # down Quay Street, about 70 m from the rank
    r0 = pg.evaluate(RON)
    assert r0["d"] > 26, "set-up: Tom beyond the 26 m pause range"
    rows = watch(pg, 23 * 60 + 50)
    walking = [r for r in rows if r["goal"] == "home|sleep"]
    assert walking, "Ron sets off home after 23:36"
    moved = max(((r["x"] - r0["x"]) ** 2 + (r["z"] - r0["z"]) ** 2) ** 0.5 for r in rows)
    print("far: Tom %.1f m away; pause max %.2f; refreshes %d; moved %.2f m by 23:50"
          % (min(r["d"] for r in rows), max(r["pause"] for r in walking), refreshes(walking), moved))
    assert max(r["pause"] for r in walking) == 0, "no pause set with Tom out of range"
    step_to(pg, 24 * 60 + 120)  # Tuesday 02:00
    end = pg.evaluate(RON)
    print("far: at 02:00 Ron space %s, moving %s" % (end["space"], end["moving"]))
    assert end["space"] != "street", "Ron gets home"
    assert errors == []
