"""The clumsy newcomer for the LEDGER loop prototype (task 4o, part 2).

Plays a build of the prototype in headless Chromium like a newcomer, keyboard first, then a simulated pad:
walks into walls and corners, drives the cab into things at a range of speeds, reverses, gets out and back in,
spams keys, pauses and resumes, saves and loads, goes indoors. Checks the experience rules in invariants.py
and records every failure with the steps that caused it.

    python clumsy.py --assets DIR [--out DIR] [--dist DIR]

--dist uses an already built folder (index.html, ledger.js and the pictures); otherwise the prototype is
built from ../prototype/project, byte for byte against the published page. The game is stepped by hand
through its own hook (window.LEDGER_MANUAL, LEDGER.tick at 1/60 s); keys are real key events.
The game's code is never changed; the only test setups are named in each scenario's steps.
"""
import argparse
import datetime
import functools
import http.server
import json
import math
import os
import random
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
PROTO = os.path.join(os.path.dirname(HERE), "prototype")
sys.path.insert(0, HERE)
sys.path.insert(0, PROTO)
import invariants as inv  # noqa: E402

GL = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
VIEW = {"width": 960, "height": 540}
DT = 1 / 60

# a pretend standard-mapping controller; the gate moves its sticks and buttons through window.__pad
PAD_INIT = """
(() => {
  const pad = { id: 'Gate pad (standard)', index: 0, connected: true, mapping: 'standard', timestamp: 0,
    axes: [0, 0, 0, 0], buttons: Array.from({length: 17}, () => ({pressed: false, touched: false, value: 0})) };
  window.__pad = pad;
  navigator.getGamepads = () => [pad, null, null, null];
})();
Math.random = (() => { let s = %d >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s;
  t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; })();
"""

WORDS_JS = """() => { const o = {}; for (const id of ['subs','prompt','obj','news','noted','called','bubbles','fare','dialog','panel','talk']) {
  const e = document.getElementById(id); o[id] = e && e.offsetParent !== null ? (e.innerText || '').trim().slice(0, 200) : ''; } return o; }"""

# the line from the look point to the camera, tested against the scene's own solid meshes (people left out)
CAMERA_JS = """() => { const L = LEDGER, T = L.THREE, cam = L.camera, c = L.cam;
  const from = new T.Vector3(c.tx, c.ty, c.tz), to = cam.position.clone();
  const d = from.distanceTo(to); if (d < 0.05) return { dist: d, hit: null };
  const ray = new T.Raycaster(from, to.clone().sub(from).normalize(), 0, d);
  const objs = []; L.scene.traverse((o) => { if ((o.isMesh || o.isInstancedMesh) && !o.isSkinnedMesh && o.visible) objs.push(o); });
  let hits = []; try { hits = ray.intersectObjects(objs, false); } catch (e) { return { dist: d, hit: null, err: String(e) }; }
  const h = hits.find((x) => x.object.material && !(x.object.material.transparent && x.object.material.opacity < 0.5));
  return { dist: d, hit: h ? h.distance : null, what: h ? (h.object.name || h.object.type) : null,
           camera: [to.x, to.y, to.z], look: [from.x, from.y, from.z] }; }"""


class Proto:
    def __init__(self, dist, seed=7):
        from playwright.sync_api import sync_playwright

        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a):
                pass
        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=dist))
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.pw = sync_playwright().start()
        self.b = self.pw.chromium.launch(args=GL)
        self.ctx = self.b.new_context(viewport=VIEW)
        self.ctx.add_init_script(PAD_INIT % seed)
        self.ctx.route("**/fonts.googleapis.com/**", lambda r: r.abort())
        self.ctx.route("**/fonts.gstatic.com/**", lambda r: r.abort())
        self.pg = self.ctx.new_page()
        self.errors = []
        self.pg.on("pageerror", lambda e: self.errors.append("pageerror: " + str(e)[:300]))
        self.pg.on("console", lambda m: m.type == "error" and "ERR_FAILED" not in m.text and self.errors.append("console: " + m.text[:300]))  # ERR_FAILED: the fonts the gate itself blocks
        self.pg.goto("http://127.0.0.1:%d/index.html" % self.srv.server_address[1])
        self.pg.wait_for_function("window.LEDGER && window.LEDGER.G", timeout=180000)
        self.pg.evaluate("LEDGER.startNew()")
        self.pg.wait_for_function("LEDGER.G.story.phase === 'play'", timeout=90000)
        self.manual()
        self.held = set()

    def manual(self):
        self.pg.evaluate("window.LEDGER_MANUAL = true; window.LEDGER_NORENDER = true")

    def js(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def down(self, key):
        self.pg.keyboard.down(key)
        self.held.add(key)

    def up(self, key=None):
        for k in ([key] if key else list(self.held)):
            self.pg.keyboard.up(k)
            self.held.discard(k)

    def tap(self, key):
        self.pg.keyboard.press(key)

    def run(self, secs, every=0.1):
        """Step the game secs seconds at 1/60 s; return samples (t, x, z, speed, inCab, box, paused) every `every` s."""
        return self.js("""([secs, every, dt]) => { const L = LEDGER, out = []; let t = 0, next = 0;
          while (t < secs - 1e-9) { L.tick(dt); t += dt;
            if (t >= next - 1e-9) { next += every; const g = L.G, tm = g.tom, inCab = !!tm.inCar;
              out.push([+t.toFixed(3), inCab ? g.car.x : tm.x, inCab ? g.car.z : tm.z, inCab ? g.car.v : (tm.v || 0), inCab,
                        L.ui.modal || null, !!g.paused, g.car.ang, g.car.dmg]); } }
          return out; }""", [secs, every, DT])

    def words(self):
        return self.js(WORDS_JS)

    def state(self):
        return self.js("() => LEDGER.read()")

    def camera(self, settle_ms=1600):
        """Draw a few frames so the game's own camera settles, then test the line from Tom to the camera."""
        self.js("window.LEDGER_NORENDER = false")
        self.pg.wait_for_timeout(settle_ms)
        r = self.js(CAMERA_JS)
        self.manual()
        return r

    def shot(self, path):
        self.js("window.LEDGER_NORENDER = false")
        self.pg.wait_for_timeout(600)
        try:
            self.pg.screenshot(path=path, timeout=120000)
        except Exception:
            path = None
        self.manual()
        return path

    def clear(self, tries=60):
        """Finish any written scene (first choice each time) and close any box, so a scenario starts in free play.
        Returns how many presses it took."""
        n = 0
        for n in range(tries):
            s = self.js("""async () => { const L = LEDGER, w = L.written.read();
              if (w.open) { if (w.choices && w.choices.length) await L.written.choose(0); else await L.written.next(); return 'scene'; }
              if (L.ui.modal) { L.press('Escape'); return 'box:' + L.ui.modal; }
              return null; }""")
            if s is None:
                break
            self.run(0.2)
        return n

    def close(self):
        try:
            self.b.close()
            self.pw.stop()
        finally:
            self.srv.shutdown()


# ---------------------------------------------------------------- scenarios

class Gate:
    def __init__(self, g, out):
        self.g, self.out, self.results, self.notes = g, out, [], []
        self.cleared = 0  # presses spent finishing scenes that started by themselves (people starting talks)
        self.shots = os.path.join(out, "shots")
        os.makedirs(self.shots, exist_ok=True)

    def record(self, rule, _ok, steps, **kw):
        kw.pop("ok", None)
        r = {"rule": rule, "ok": bool(_ok), "steps": steps}
        r.update(kw)
        self.results.append(r)
        return r

    def check_camera(self, steps, where):
        c = self.g.camera()
        near = 2.7 if self.g.js("() => LEDGER.G.tom.inCar") else 0.7
        v = inv.camera_clear(c.get("hit"), c.get("dist", 0), near)
        r = self.record("camera clear", v["ok"], steps, where=where, **{k: c.get(k) for k in ("hit", "dist", "what", "camera")})
        if not v["ok"]:
            r["shot"] = self.g.shot(os.path.join(self.shots, "camera-%02d.png" % len(self.results)))
        return r

    def escape_track(self, keys_to_try, secs_each=2.0, yaw=None):
        """Try each way out in turn; return the joined track of positions (t, x, z)."""
        g, track, t0 = self.g, [], 0.0
        for k in keys_to_try:
            self.cleared += g.clear()
            if yaw is not None:
                g.js("(y) => { LEDGER.cam.yaw = y; }", yaw)
            g.down(k)
            for s in g.run(secs_each):
                track.append((t0 + s[0], s[1], s[2]))
            g.up(k)
            t0 += secs_each
            if inv.moved_again(track)["free_after_s"] is not None:
                break
        return track

    # 1. on foot into walls, from several places, in eight directions; then get away
    def foot_walls(self, places):
        g = self.g
        for place in places:
            for h in range(8):
                yaw = h * math.pi / 4
                g.js("(p) => { LEDGER.goOutside(); LEDGER.goTo(p); }", place)
                self.cleared += g.clear()
                g.js("(y) => { LEDGER.cam.yaw = y; }", yaw)
                g.down("KeyW")
                rows = g.run(4.0)
                g.up("KeyW")
                stuck_at_wall = abs(rows[-1][3]) < 0.05 or math.hypot(rows[-1][1] - rows[-10][1], rows[-1][2] - rows[-10][2]) < 0.05
                steps = "goTo %s; camera yaw %.2f; hold W 4 s" % (place, yaw)
                if not stuck_at_wall:
                    continue
                track = self.escape_track(["KeyS", "KeyA", "KeyD"])
                v = inv.moved_again(track)
                self.record("never stuck (on foot)", v["ok"], steps + "; then S, A, D", **v)
                if h % 4 == 0:
                    self.check_camera(steps, "against a wall on foot at " + place)

    # 2. corners: find spots walled on two sides, push in, get out
    def corners(self, n=10):
        g = self.g
        spots = g.js("""(n) => { const L = LEDGER, out = []; const b = (x, z) => L.isBlocked(x, z);
          for (let x = -40; x <= 40 && out.length < n; x += 0.5) for (let z = -60; z <= 90 && out.length < n; z += 0.5) {
            if (b(x, z)) continue;
            const e = b(x + 0.7, z), w = b(x - 0.7, z), s = b(x, z + 0.7), nn = b(x, z - 0.7);
            if ((e || w) && (s || nn) && !(e && w) && !(s && nn)) {
              if (out.every((p) => Math.hypot(p[0] - x, p[1] - z) > 8)) out.push([x, z, e ? 1 : -1, s ? 1 : -1]); } }
          return out; }""", n)
        for x, z, ex, sz in spots:
            g.js("([x, z]) => { LEDGER.goOutside(); const t = LEDGER.G.tom; t.x = x; t.z = z; t.v = 0; }", [x, z])
            into = math.atan2(ex, sz)  # yaw pointing into the corner
            g.js("(y) => { LEDGER.cam.yaw = y; }", into)
            g.down("KeyW")
            g.run(2.0)
            g.up("KeyW")
            track = self.escape_track(["KeyS", "KeyA", "KeyD", "KeyW"], yaw=into)
            v = inv.moved_again(track)
            self.record("never stuck (corner)", v["ok"], "Tom put at (%.1f, %.1f); hold W into the corner 2 s; then S, A, D, W" % (x, z), **v)
        if spots:
            x, z = spots[0][:2]
            self.check_camera("Tom in the corner at (%.1f, %.1f)" % (x, z), "corner")
        return len(spots)

    # 3. the cab into things at a range of speeds; then drive away; damage told
    def cab_crashes(self, runs=12, rnd=None):
        g = self.g
        rnd = rnd or random.Random(3)
        g.js("() => { LEDGER.goOutside(); LEDGER.G.car.keys = true; LEDGER.cab.getIn(); }")
        if not g.js("() => LEDGER.G.tom.inCar"):
            self.record("cab: can get in", False, "car keys given (test setup); LEDGER.cab.getIn()")
            return
        # straight lines on the street that end in something solid 8 to 45 m ahead
        lines = g.js("""(n) => { const L = LEDGER, out = []; const b = (x, z) => L.isBlocked(x, z);
          for (let tries = 0; tries < 4000 && out.length < n; tries++) {
            const x = -30 + Math.random() * 60, z = -50 + Math.random() * 130, a = Math.random() * Math.PI * 2;
            let ok = true; for (const [dx, dz] of [[0,0],[1.6,0],[-1.6,0],[0,1.6],[0,-1.6]]) if (b(x+dx, z+dz)) ok = false;
            if (!ok) continue; let d = 0;
            for (; d < 50; d += 0.5) { const px = x + Math.sin(a) * (d + 2.2), pz = z + Math.cos(a) * (d + 2.2);
              if (b(px, pz) || b(px + Math.cos(a) * 0.9, pz - Math.sin(a) * 0.9) || b(px - Math.cos(a) * 0.9, pz + Math.sin(a) * 0.9)) break; }
            if (d >= 8 && d <= 45) out.push([x, z, a, d]); }
          return out; }""", runs)
        for i, (x, z, a, d) in enumerate(lines):
            g.js("([x, z, a]) => { const c = LEDGER.G.car; c.x = x; c.z = z; c.ang = a; c.v = 0; LEDGER.G.tom.inCar = true; }", [x, z, a])
            before = g.words()
            dmg0 = g.js("() => LEDGER.G.car.dmg")
            g.down("KeyW")
            rows = g.run(12.0, every=1 / 60)
            g.up("KeyW")
            peak, hit_t = 0.0, None
            for j in range(1, len(rows)):
                peak = max(peak, rows[j - 1][3])
                if rows[j][3] < rows[j - 1][3] - 2.0:  # a sudden loss of speed: the hit
                    hit_t = rows[j][0]
                    break
            steps = "cab put at (%.1f, %.1f) heading %.2f, %.0f m from a solid; hold W" % (x, z, a, d)
            if hit_t is None:
                self.notes.append(steps + ": no hit found within 12 s")
                continue
            mph = round(peak * 2.237, 1)
            # damage told: words within 1.5 s of the hit (the frames after the hit are re-run from here)
            frames, t = [], 0.0
            for _ in range(6):
                g.run(0.25)
                t += 0.25
                frames.append((t, g.words()))
            dmg1 = g.js("() => LEDGER.G.car.dmg")
            if dmg1 > dmg0:
                v = inv.said(before, frames, about=inv.DAMAGE_WORDS, where=inv.MESSAGE_PLACES)
                self.record("damage told", v["ok"], steps, impact_mph=mph, damage=dmg1, **v)
            track = self.escape_track(["KeyS", "KeyW"], secs_each=2.5)
            v = inv.moved_again(track, moved_m=1.0)
            self.record("never stuck (cab after a hit)", v["ok"], steps + "; then S 2.5 s, W 2.5 s", impact_mph=mph, damage=dmg1, **v)
            if i in (0, len(lines) - 1):
                self.check_camera(steps + " (after the hit)", "cab after a hit at %.0f mph" % mph)
        top = g.js("() => LEDGER.rules.DRIVING ? LEDGER.rules.DRIVING.topMetresPerSecond : null")
        dmg = g.js("() => LEDGER.G.car.dmg")
        self.notes.append("cab damage after the crash runs: %s (top speed %s m/s, each point of damage takes 5%% off)" % (dmg, top))

    # 4. keyboard steering: snaps or eases?
    def cab_steering(self):
        g = self.g
        x, z, a = g.js("""() => { const L = LEDGER; const b = (x, z) => L.isBlocked(x, z);
          for (let t = 0; t < 5000; t++) { const x = -30 + Math.random() * 60, z = -50 + Math.random() * 130, a = Math.random() * 6.28;
            let ok = true; for (let d = 0; d < 60; d += 1) if (b(x + Math.sin(a) * d, z + Math.cos(a) * d)) { ok = false; break; }
            if (ok) return [x, z, a]; } return [4.1, 37.4, 0]; }""")
        g.js("() => { LEDGER.goOutside(); LEDGER.G.car.keys = true; LEDGER.cab.getIn(); }")
        g.js("([x, z, a]) => { const c = LEDGER.G.car; c.x = x; c.z = z; c.ang = a; c.v = 9; LEDGER.G.tom.inCar = true; }", [x, z, a])
        rows0 = g.run(0.1, every=1 / 60)
        g.down("KeyD")
        rows = g.run(0.5, every=1 / 60)
        g.up("KeyD")
        rel = g.run(0.2, every=1 / 60)
        rows = rows0[-1:] + rows
        rates = [(rows[j][7] - rows[j - 1][7]) / DT for j in range(1, len(rows))]
        full = max(abs(r) for r in rates) if rates else 0
        first = abs(rates[0]) if rates else 0
        relrates = [(rel[j][7] - (rel[j - 1][7] if j else rows[-1][7])) / DT for j in range(len(rel))]
        after_release = abs(relrates[0]) if relrates else 0
        # eased: the first frame after the key goes down, and the first after it comes up, each move under half the way
        eased = full > 0 and first < 0.5 * full and after_release > 0.5 * full
        self.record("keyboard steering eased", eased, "cab at 9 m/s on a clear line; hold D 0.5 s, let go",
                    first_frame_turn_rate=round(first, 3), full_turn_rate=round(full, 3), first_frame_after_release=round(after_release, 3),
                    note="the turn rate in the first frame after the key goes down, against the full rate")

    # 5. out and back in, many times, fast
    def out_and_in(self, n=12):
        g = self.g
        g.js("() => { LEDGER.G.car.keys = true; LEDGER.cab.getIn(); LEDGER.G.car.v = 0; }")
        bad = []
        for i in range(n):
            g.tap("KeyF")
            g.run(0.15)
            s = g.js("() => ({ inCab: LEDGER.G.tom.inCar, x: LEDGER.G.tom.x, z: LEDGER.G.tom.z, blocked: LEDGER.isBlocked(LEDGER.G.tom.x, LEDGER.G.tom.z) })")
            if not s["inCab"] and s["blocked"]:
                bad.append(i)
        self.record("out of the cab onto open ground", not bad, "tap F %d times, 0.15 s apart" % n, bad_presses=bad)
        if g.js("() => LEDGER.G.tom.inCar"):
            g.tap("KeyF")
            g.run(0.3)
        track = self.escape_track(["KeyW", "KeyS", "KeyA", "KeyD"])
        self.record("never stuck (after getting out)", inv.moved_again(track)["ok"], "after the F presses, walk W, S, A, D", **inv.moved_again(track))

    # 6. key spam, then back to free play
    def key_spam(self, n=300, rnd=None):
        g = self.g
        rnd = rnd or random.Random(11)
        pool = ["KeyE", "KeyT", "KeyF", "KeyC", "KeyY", "KeyG", "KeyL", "KeyQ", "KeyR", "KeyX", "KeyZ", "Space", "Enter",
                "Escape", "Tab", "Digit1", "Digit2", "Digit3", "KeyW", "KeyA", "KeyS", "KeyD", "Backspace", "KeyK", "F2"]
        g.js("() => { LEDGER.goOutside(); LEDGER.goTo('the rank'); }")
        seq = []
        for i in range(n):
            k = rnd.choice(pool)
            seq.append(k)
            try:
                g.tap(k)
            except Exception as e:
                self.notes.append("key %s refused: %s" % (k, e))
            g.run(0.1)
        g.up()
        # back to free play: Escape up to five times, then walk
        tries = 0
        while tries < 5:
            s = g.state()
            if not s["boxOpen"] and not s["paused"] and not s["inAWrittenScene"]:
                break
            g.tap("Escape")
            g.run(0.3)
            tries += 1
        s = g.state()
        free = not s["boxOpen"] and not s["paused"]
        self.record("back to play after button spam", free, "%d random keys 0.1 s apart (seed 11), then Escape up to 5 times" % n,
                    escapes=tries, box=s["boxOpen"], paused=s["paused"], scene=s["inAWrittenScene"], last_keys=seq[-12:])
        if free:
            if g.js("() => LEDGER.G.tom.inCar"):
                g.tap("KeyF")
                g.run(0.3)
            track = self.escape_track(["KeyW", "KeyS", "KeyA", "KeyD"])
            self.record("never stuck (after button spam)", inv.moved_again(track)["ok"], "after the spam, walk", **inv.moved_again(track))
        faults = g.js("() => LEDGER.pauseFaults()")
        self.record("no pause nothing holds", faults == 0, "count of pauses nothing was holding over the whole run", pause_faults=faults)

    # 7. pause and resume, save and load
    def pause_save(self):
        g = self.g
        g.js("() => { LEDGER.goOutside(); LEDGER.goTo('the rank'); }")
        g.tap("Escape")
        g.run(0.3)
        p1 = g.state()
        g.tap("Escape")
        g.run(0.3)
        p2 = g.state()
        # resumed: the pause box is gone (a talk that starts by itself right after, at the rank, is not the pause)
        self.record("pause and resume by Escape", p1["paused"] and p1["boxOpen"] == "pause" and p2["boxOpen"] != "pause" and (not p2["paused"] or p2["inAWrittenScene"]),
                    "Escape, 0.3 s, Escape", first=[p1["paused"], p1["boxOpen"]], second=[p2["paused"], p2["boxOpen"]])
        if p2["paused"] or p2["boxOpen"]:
            g.tap("Escape")
            g.run(0.3)
        text = g.js("() => LEDGER.saveText()")
        a = g.state()
        g.js("() => LEDGER.goTo(\"Mickey's door\")")
        g.run(5)
        g.js("(t) => LEDGER.restore(t)", text)
        g.pg.wait_for_timeout(1500)
        g.manual()
        b = g.state()
        same = (abs(a["tom"]["xMetres"] - b["tom"]["xMetres"]) < 0.3 and abs(a["tom"]["zMetres"] - b["tom"]["zMetres"]) < 0.3
                and a["money"] == b["money"] and abs(a["gameMinute"] - b["gameMinute"]) < 1.0)
        self.record("save then load gives the same game", same, "saveText at the rank; walk off 5 s; restore",
                    before=[a["tom"]["xMetres"], a["tom"]["zMetres"], a["gameMinute"]], after=[b["tom"]["xMetres"], b["tom"]["zMetres"], b["gameMinute"]],
                    paused_after=b["paused"])
        if b["paused"]:
            g.tap("Escape")
            g.run(0.3)

    # 8. the pad: can a controller move Tom or the cab?
    def pad(self):
        g = self.g
        def real(ms):
            g.js("window.LEDGER_NORENDER = true; window.LEDGER_MANUAL = false")
            g.pg.wait_for_timeout(ms)
            g.manual()
        g.js("() => { const G = LEDGER.G; if (G.tom.inCar) LEDGER.cab.getOut(); G.car.v = 0; LEDGER.goOutside(); LEDGER.goTo('the rank'); }")
        c0 = g.state()["tom"]
        real(2500)  # the control: the same time with no input
        c1 = g.state()["tom"]
        control = math.hypot(c1["xMetres"] - c0["xMetres"], c1["zMetres"] - c0["zMetres"])
        g.js("() => LEDGER.goTo('the rank')")
        s0 = g.state()["tom"]
        g.js("() => { window.__pad.axes[1] = -1; window.__pad.timestamp++; }")
        # the pad is read in the drawing loop, so let a few real frames run while stepping
        g.js("window.LEDGER_NORENDER = true; window.LEDGER_MANUAL = false")
        g.pg.wait_for_timeout(2500)
        g.manual()
        g.js("() => { window.__pad.axes[1] = 0; }")
        s1 = g.state()["tom"]
        moved = math.hypot(s1["xMetres"] - s0["xMetres"], s1["zMetres"] - s0["zMetres"])
        self.record("a pad moves Tom", moved > control + 0.5, "left stick full forward for 2.5 s of real time (game running), against 2.5 s with no input",
                    moved_m=round(moved, 2), control_m=round(control, 2))
        g.js("() => { LEDGER.G.car.keys = true; LEDGER.cab.getIn(); LEDGER.G.car.v = 0; window.__pad.buttons[7].pressed = true; window.__pad.buttons[7].value = 1; }")
        c0 = g.state()["cab"]
        g.js("window.LEDGER_MANUAL = false")
        g.pg.wait_for_timeout(2500)
        g.manual()
        g.js("() => { window.__pad.buttons[7].pressed = false; window.__pad.buttons[7].value = 0; }")
        c1 = g.state()["cab"]
        moved = math.hypot(c1["xMetres"] - c0["xMetres"], c1["zMetres"] - c0["zMetres"])
        self.record("a pad drives the cab", moved > 0.5, "in the cab, right trigger held 2.5 s of real time", moved_m=round(moved, 2))
        g.js("() => { if (LEDGER.G.tom.inCar) LEDGER.cab.getOut(); }")

    # 9. indoors: walk into each room's walls; the camera
    def indoors(self):
        """Go in by each street door with E, as a player does, then walk into the room's walls."""
        g = self.g
        doors = g.js("() => Object.entries(LEDGER.places).filter(([n, p]) => p.kind === 'door').map(([n]) => n)")
        for door in doors:
            g.js("() => LEDGER.goOutside()")
            g.js("(d) => LEDGER.goTo(d)", door)
            self.cleared += g.clear()
            g.tap("KeyE")
            g.run(1.5)
            self.cleared += g.clear()
            room = g.js("() => LEDGER.read().tom.indoorsRoomId")
            if not room:
                self.notes.append("indoors: E at %s did not take Tom in (closed, or not a door at this hour)" % door)
                continue
            for h in range(4):
                g.js("(y) => { LEDGER.cam.yaw = y; }", math.pi + (h - 1.5) * 0.4)
                key = ["KeyW", "KeyA", "KeyS", "KeyD"][h]
                g.down(key)
                g.run(3.0)
                g.up(key)
                track = self.escape_track(["KeyS", "KeyW", "KeyA", "KeyD"])
                v = inv.moved_again(track)
                self.record("never stuck (indoors)", v["ok"], "in by %s with E; hold %s 3 s; then S, W, A, D" % (door, key), room=room, **v)
                if h in (0, 2):
                    self.check_camera("in by %s with E; held %s 3 s against the wall" % (door, key), "indoors: " + room)
        g.js("() => LEDGER.goOutside()")

    # 10. a person hit by the cab (his ruling of 18 Nov: hurt badly, never killed; stop or drive off)
    def person_hit(self):
        g = self.g
        tried = []
        for k in range(6):
            r = g.js("""(k) => { const L = LEDGER, G = L.G; G.car.keys = true; L.cab.getIn();
              const all = G.named.filter((p) => !p.gone && !p.dead && !p.down && p.space === 'street' && !p.inCar);
              for (const P of all.slice(k)) { for (let a = 0; a < 6.28; a += 0.785) {
                  let ok = true; for (let d = 2; d < 16; d += 0.5) if (L.isBlocked(P.x - Math.sin(a) * d, P.z - Math.cos(a) * d)) { ok = false; break; }
                  if (!ok) continue; P.route = null; P.moving = false;
                  G.car.ang = a; G.car.x = P.x - Math.sin(a) * 14; G.car.z = P.z - Math.cos(a) * 14; G.car.v = 4.5;
                  return { id: P.id, name: P.def.name }; } }
              return null; }""", k)
            if not r:
                break
            before = g.words()
            closest, frames, t = 99.0, [], 0.0
            g.down("KeyW")
            for _ in range(16):
                g.js("(id) => { const P = LEDGER.G.named.find((q) => q.id === id); P.route = null; P.moving = false; }", r["id"])
                g.run(0.25)
                t += 0.25
                d = g.js("(id) => { const P = LEDGER.G.named.find((q) => q.id === id), c = LEDGER.G.car; return Math.hypot(P.x - c.x, P.z - c.z); }", r["id"])
                closest = min(closest, d)
                frames.append((t, g.words()))
                if g.js("(id) => !!LEDGER.G.named.find((q) => q.id === id).down", r["id"]):
                    hit_t = t
                    break
            g.up("KeyW")
            p = g.js("(id) => { const P = LEDGER.G.named.find((q) => q.id === id); return { down: !!P.down, dead: !!P.dead, hurt: P.hurt || 0 }; }", r["id"])
            tried.append(r["name"])
            if not p["down"]:
                continue
            after = [(round(f[0] - hit_t, 2), f[1]) for f in frames if f[0] >= hit_t]
            for i in range(6):
                g.run(0.25)
                after.append((0.25 * (i + 1), g.words()))
            told = inv.said(before, after, about=inv.HIT_WORDS + [r["name"].split()[0].lower()], where=inv.MESSAGE_PLACES)
            self.record("a person hit is hurt, never killed", not p["dead"], "test setup: %s held still on the street, cab 14 m back at 4.5 m/s on a clear line, hold W" % r["name"],
                        person=r["name"], hurt=round(p["hurt"], 2), dead=p["dead"])
            self.record("a person hit: told on screen", told["ok"], "the same hit", person=r["name"], **told)
            choice = g.js("() => LEDGER.prompts()")
            self.record("a person hit: a choice is offered (stop and help, or drive off)", any("help" in (c.get("text") or "").lower() for c in choice),
                        "the key prompts 1.5 s after the hit", prompts=choice)
            break
        else:
            self.notes.append("person hit: no one was knocked down after trying %s" % tried)
        g.js("() => { LEDGER.G.car.v = 0; if (LEDGER.G.tom.inCar) LEDGER.cab.getOut(); }")


def build_dist(assets):
    import build
    tmp = tempfile.mkdtemp(prefix="ledger-gate-")
    problems = build.build(assets_dir=assets, dist=tmp, log=lambda *a: None)
    if problems:
        raise SystemExit("build does not match the published page: %s" % problems)
    return tmp


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets")
    ap.add_argument("--dist")
    ap.add_argument("--out", default=os.path.join(os.path.expanduser("~"), ".cache", "ledger-gate",
                                                   datetime.datetime.now().strftime("%Y%m%d-%H%M")))
    ap.add_argument("--only", default="")
    a = ap.parse_args(argv)
    dist = a.dist or build_dist(a.assets)
    os.makedirs(a.out, exist_ok=True)
    gate = Gate(None, a.out)
    errors = []
    order = ["foot_walls", "corners", "cab_crashes", "cab_steering", "out_and_in", "person_hit", "pad", "indoors", "pause_save", "key_spam"]
    only = [x for x in a.only.split(",") if x] or order
    for name in order:
        if name not in only:
            continue
        g = Proto(dist)  # a fresh new game for every scenario, so nothing carries over (damage, people down, the hour)
        gate.g = g
        gate.notes.append("%s: %d presses to clear scenes and boxes first" % (name, g.clear()))
        try:
            if name == "foot_walls":
                gate.foot_walls(["the rank", "Mickey's door"])
            else:
                getattr(gate, name)()
        except Exception as e:  # a scenario that breaks is itself a finding; the rest still run
            gate.record("scenario ran", False, name, error=str(e)[:400])
        errors += g.errors
        g.close()
        print("done", name, flush=True)
    gate.notes.append("presses spent finishing scenes that started by themselves during the run: %d" % gate.cleared)
    gate.record("no page errors", not errors, "whole run", errors=errors[:20])
    # a rule that tested nothing fails: an empty pass is not a pass
    for rule in ["never stuck (cab after a hit)", "damage told", "a person hit is hurt, never killed", "never stuck (indoors)", "camera clear"]:
        if not a.only and not any(r["rule"] == rule for r in gate.results):
            gate.record("tested something: " + rule, False, "no case of this rule was reached in the run")
    summary = inv.summarise(gate.results)
    gate.notes.append("the 'told on screen' checks read the words the page shows between steps; the page refreshes them only when it draws, so these checks are provisional until they read the game's own message list")
    report = {"when": datetime.datetime.now().isoformat(timespec="seconds"), "summary": {k: {"checked": v["checked"], "failed": v["failed"]} for k, v in summary.items()},
              "results": gate.results, "notes": gate.notes}
    with open(os.path.join(a.out, "report.json"), "w") as f:
        json.dump(report, f, indent=1)
    failed = sum(v["failed"] for v in summary.values())
    for k, v in summary.items():
        print("%-40s %3d checked %3d failed" % (k, v["checked"], v["failed"]))
    print("report:", os.path.join(a.out, "report.json"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
