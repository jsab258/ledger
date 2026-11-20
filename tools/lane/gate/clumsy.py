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

WORDS_JS = """() => { const o = {}, shown = (e) => !!e && !e.classList.contains('hidden') && getComputedStyle(e).display !== 'none'
  && getComputedStyle(e).visibility !== 'hidden' && e.getClientRects().length > 0; for (const id of ['subs','prompt','obj','news','noted','called','bubbles','fare','dialog','panel','talk']) {
  const e = document.getElementById(id); o[id] = shown(e) ? (e.innerText || '').trim().slice(0, 200) : ''; } return o; }"""
# shown(e): on screen now. offsetParent alone misses fixed boxes (the written scene's #dialog is fixed, so its offsetParent
# is always null and its words were never read, found 20 Nov by the panel's first packet)

# The gate's own helpers in the page (test instrumentation only; the game's code is not changed).
# msgs(): the game's message lists as a player could read them now: the subtitles (ui.subs), the Noted line when it
# is up (drawn by the game's hud from ui.notes), the queued Noted lines not yet shown, the newspaper when it shows,
# speech bubbles of people within earshot (ui.bubs), and the length of the game's event log.
# watch(): steps the game one tick per drawn frame, so the page's own hud runs between steps as in play.
GATE_JS = """() => { window.__gate = {
  msgs() { const L = LEDGER, ui = L.ui, G = L.G, t = G.tom, tx = t.inCar ? G.car.x : t.x, tz = t.inCar ? G.car.z : t.z;
    const n = document.getElementById('noted'), nw = document.getElementById('news');
    return { subs: ui.subs.map((s) => (s.el.textContent || '').trim()),
      noted: n && n.classList.contains('on') ? (n.textContent || '').trim() : '',
      queued: ui.notes.slice(),
      news: nw && !nw.classList.contains('hidden') && nw.style.opacity !== '0' ? (nw.textContent || '').trim() : '',
      bubbles: ui.bubs.filter((b) => b.P && b.P.space === t.space && Math.hypot(b.P.x - tx, b.P.z - tz) <= L.rules.talk.bubbleHeardWithinMetres).map((b) => String(b.text)),
      events: G.events.length }; },
  async watch(secs, dt, each) { const out = []; let t = 0;
    while (t < secs - 1e-9) { if (each) each(); LEDGER.tick(dt); t += dt;
      await new Promise((r) => requestAnimationFrame(r)); const m = this.msgs(); m.t = +t.toFixed(3); out.push(m); }
    return out; } }; }"""

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
    EXTRA_INIT = None  # a test tool's own script put in before the page loads (feel_numbers.py catches the frame loop)

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
        if self.EXTRA_INIT:
            self.ctx.add_init_script(self.EXTRA_INIT)
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
        self.pg.evaluate(GATE_JS)
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

    # 3. the cab into named things (walls, lamp posts, bollards, parked cars, traffic) at a range of speeds;
    #    the damage is reset before each crash so every crash is judged; then drive away; damage told
    CRASH_JS = """async ([x, z, a, tx, tz, maxs]) => { const L = LEDGER, G = L.G, c = G.car, dt = 1 / 60;
      G.tom.inCar = true; c.x = x; c.z = z; c.ang = a; c.v = 0; c.dmg = 0;
      const before = __gate.msgs(), e0 = G.events.length; let t = 0, peak = 0, prev = 0, hit = null, closest = 1e9, cause = null;
      while (t < maxs) { if (G.paused || L.ui.modal) return { interrupted: L.ui.modal || 'paused' }; L.tick(dt); t += dt; peak = Math.max(peak, c.v);
        if (tx !== null) closest = Math.min(closest, Math.hypot(c.x - tx, c.z - tz));
        if (c.dmg > 0) { hit = t; cause = 'damage'; break; }
        if (c.v < prev - 2) { hit = t; cause = 'speed lost'; break; } prev = c.v; }
      const at = { x: c.x, z: c.z, front: [c.x + Math.sin(c.ang) * 2.2, c.z + Math.cos(c.ang) * 2.2], dmg: c.dmg };
      if (hit === null) return { hit, peak, closest, at };
      const frames = await __gate.watch(3.0, dt);
      for (const f of frames) if (tx !== null) closest = Math.min(closest, Math.hypot(c.x - tx, c.z - tz));
      return { hit, cause, peak, closest, at, before, frames, kinds: G.events.slice(e0).map((e) => e.kind), dmg: c.dmg }; }"""

    # a clear run-up to a target point: [x, z, heading, metres] or null (the line checked with the collision map,
    # the last stretch before the target left out so the target itself is what the cab meets)
    APPROACH_JS = """([tx, tz, want, stop]) => { const L = LEDGER, b = (x, z) => L.isBlocked(x, z); let best = null;
      for (let k = 0; k < 24; k++) { const a = k * Math.PI / 12, sx = Math.sin(a), sz = Math.cos(a); let d = stop;
        for (; d <= want + 1.6; d += 0.5) { const px = tx - sx * d, pz = tz - sz * d;
          if (b(px, pz) || b(px + sz * 0.9, pz - sx * 0.9) || b(px - sz * 0.9, pz + sx * 0.9) || b(px + sz * 0.5, pz - sx * 0.5) || b(px - sz * 0.5, pz + sx * 0.5)) break; }
        d -= 1.6;
        d -= 0.5; if (d >= 8 && (!best || Math.abs(d - want) < Math.abs(best[3] - want))) best = [tx - sx * d, tz - sz * d, a, d]; }
      return best; }"""

    def crash_targets(self, rnd):
        """Named targets from what the game draws, plus walls and moving traffic. Returns a list of
        (type, label, target x, target z or None, run-up dict)."""
        g, out = self.g, []
        props = inv.drawn_props()
        speeds = [9, 18, 30, 42, 14, 24, 36]
        for typ, n in (("lamp post", 3), ("bollard", 2), ("parked car", 3)):
            cands = [p for p in props if p["type"] == typ]
            rnd.shuffle(cands)
            got = 0
            for p in cands:
                if got >= n:
                    break
                want = speeds[(len(out)) % len(speeds)]
                stop = p["r"] + 2.2 + 0.2
                ap = g.js(self.APPROACH_JS, [p["x"], p["z"], want, stop])
                if ap:
                    out.append((typ, "%s at (%.1f, %.1f)" % (typ, p["x"], p["z"]), p["x"], p["z"], p["r"], ap))
                    got += 1
            if got < n:
                self.notes.append("crash targets: only %d of %d %s targets had a clear run-up" % (got, n, typ))
        # walls: straight lines on the street that end in a wall or building 8 to 45 m ahead
        lines = g.js("""(n) => { const L = LEDGER, out = []; const b = (x, z) => L.isBlocked(x, z);
          for (let tries = 0; tries < 4000 && out.length < n; tries++) {
            const x = -30 + Math.random() * 60, z = -50 + Math.random() * 130, a = Math.random() * Math.PI * 2;
            let ok = true; for (const [dx, dz] of [[0,0],[1.6,0],[-1.6,0],[0,1.6],[0,-1.6]]) if (b(x+dx, z+dz)) ok = false;
            if (!ok) continue; let d = 0;
            for (; d < 50; d += 0.5) { const px = x + Math.sin(a) * (d + 2.2), pz = z + Math.cos(a) * (d + 2.2);
              if (b(px, pz) || b(px + Math.cos(a) * 0.9, pz - Math.sin(a) * 0.9) || b(px - Math.cos(a) * 0.9, pz + Math.sin(a) * 0.9)) break; }
            if (d >= 8 && d <= 45) out.push([x, z, a, d]); }
          return out; }""", 4)
        for x, z, a, d in lines:
            out.append(("wall", "wall %.0f m ahead of (%.1f, %.1f)" % (d, x, z), None, None, 0, [x, z, a, d]))
        return out

    def traffic_target(self):
        """A moving car or the bus, found in the drawn scene (vehicle groups that are not parked and not the cab):
        the cab is put 16 m ahead of it on a clear line, facing it."""
        g = self.g
        g.run(6.0)  # the first car comes after about 3 s
        return g.js("""() => { const L = LEDGER, G = L.G, b = (x, z) => L.isBlocked(x, z), seen = [];
          const parked = %s;
          for (const o of L.scene.children) { if (!o.isGroup || o.name || !o.visible || o.position.y > 1) continue;
            const x = o.position.x, z = o.position.z;
            if (Math.hypot(x - G.car.x, z - G.car.z) < 3) continue;
            if (parked.some((p) => Math.hypot(p[0] - x, p[1] - z) < 1)) continue;
            let n = 0; o.traverse((m) => { if (m.isMesh) n++; }); if (n < 6) continue;
            const a = o.rotation.y, sx = Math.sin(a), sz = Math.cos(a);
            for (const d of [16, 13, 10]) { const cx = x + sx * d, cz = z + sz * d; let ok = true;
              for (let k = 2; k <= d; k += 0.5) if (b(x + sx * k, z + sz * k)) { ok = false; break; }
              if (ok && !b(cx, cz)) return { x, z, cab: [cx, cz, a + Math.PI, d] }; } }
          return null; }""" % json.dumps([[p["x"], p["z"]] for p in inv.drawn_props() if p["type"] == "parked car"]))

    def cab_crashes(self, rnd=None):
        g = self.g
        rnd = rnd or random.Random(3)
        g.js("() => { LEDGER.goOutside(); LEDGER.G.car.keys = true; LEDGER.cab.getIn(); }")
        if not g.js("() => LEDGER.G.tom.inCar"):
            self.record("cab: can get in", False, "car keys given (test setup); LEDGER.cab.getIn()")
            return
        crash_rx, count_rx = inv.source_phrases("crash"), inv.count_line_rx()
        targets = self.crash_targets(rnd)
        tr = self.traffic_target()
        if tr:
            targets.append(("traffic", "a moving car at (%.1f, %.1f)" % (tr["x"], tr["z"]), None, None, 0, tr["cab"]))
        judged = {}
        for i, (typ, label, tx, tz, tr_r, (x, z, a, d)) in enumerate(targets):
            steps = "test setup: cab put %.0f m from a %s, facing it, damage set to 0; hold W" % (d, label)
            for _ in range(4):  # a talk or a scene that starts by itself stops the game: finish it, then try again
                self.cleared += g.clear()
                g.down("KeyW")
                r = g.js(self.CRASH_JS, [x, z, a, tx, tz, 12.0])
                g.up("KeyW")
                if not r.get("interrupted"):
                    break
            if r.get("interrupted"):
                self.record("crash reached", False, steps, target=typ, prop=label, note="a box kept opening (%s): not reached" % r["interrupted"])
                continue
            mph = round(r["peak"] * 2.237, 1)
            if tx is not None and r["closest"] < max(0.5, tr_r):
                # the cab's middle went over the thing: it is drawn but not solid
                self.record("drawn things are solid (cab)", False, steps, target=typ, prop=label, closest_m=round(r["closest"], 2), impact_mph=mph,
                            note="the cab drove through it")
                continue
            if r["peak"] < 1.0:
                self.notes.append(steps + ": the cab could not move off from where the gate put it (a set-up spot touching something); not judged")
                continue
            if r["hit"] is None:
                self.record("crash reached", False, steps, target=typ, prop=label, note="no hit within 12 s (not reached)", top_mph=mph)
                continue
            if tx is not None:
                fx, fz = r["at"]["front"]
                if math.hypot(fx - tx, fz - tz) > tr_r + 2.0:
                    self.notes.append(steps + ": hit something else first, %.1f m short (%s)" % (math.hypot(fx - tx, fz - tz), r["cause"]))
                    typ = "something else"
                else:
                    self.record("drawn things are solid (cab)", True, steps, target=typ, prop=label, impact_mph=mph)
            frames = [(f["t"], f) for f in r["frames"]]
            if r["dmg"] > 0:
                v = inv.told(r["before"], frames, crash_rx, count_rx=count_rx)
                self.record("damage told", v["ok"], steps, target=typ, prop=label, impact_mph=mph, damage=r["dmg"],
                            event_kinds=r["kinds"], **v)
                judged[typ] = judged.get(typ, 0) + 1
            else:
                self.notes.append(steps + ": hit at %.1f mph made no damage (the game counts a crash above %s m/s)" % (mph, g.js("() => LEDGER.rules.driving.crashAboveMetresPerSecond")))
            track = self.escape_track(["KeyS", "KeyW"], secs_each=2.5)
            v = inv.moved_again(track, moved_m=1.0)
            self.record("never stuck (cab after a hit)", v["ok"], steps + "; then S 2.5 s, W 2.5 s", target=typ, prop=label, impact_mph=mph, damage=r["dmg"], **v)
            if i in (0, len(targets) - 1):
                self.check_camera(steps + " (after the hit)", "cab after a hit at %.0f mph" % mph)
        for typ in ("wall", "lamp post", "bollard", "parked car", "traffic"):
            if not judged.get(typ):
                self.record("damage told", False, "no damaging crash into a %s was reached" % typ, target=typ, note="not reached")
        top = g.js("() => LEDGER.rules.driving.topMetresPerSecond")
        self.notes.append("crash runs: damage set to 0 before each; top speed %s m/s (%.0f mph); each point of damage takes 5%% off" % (top, top * 2.237))

    # 4. keyboard steering: press, release, and a straight switch from A to D, at a steady speed
    # The cab is kept on its spot (put back each frame) with the speed held, so the turn rate shows the steering
    # and nothing else. (Fixed 19 Nov, round 6: the cab used to run 27 m along a line checked only down its middle,
    # met a wall, and the A-to-D result ended at no turn at all; that passed only by luck.)
    STEER_JS = """([secs, v, x, z]) => { const L = LEDGER, c = L.G.car, dt = 1 / 60, out = []; let t = 0;
      while (t < secs - 1e-9) { if (L.G.paused || L.ui.modal) return null; c.v = v; c.x = x; c.z = z; const a0 = c.ang; L.tick(dt); t += dt; out.push(-(c.ang - a0) / dt); }
      return out; }"""

    def cab_steering(self):
        g = self.g
        # a spot of open ground: nothing solid, nothing drawn and nobody standing within 5 m of it
        spot = g.js("""(props) => { const L = LEDGER, G = L.G; const b = (x, z) => L.isBlocked(x, z) || (L.isClearOnFoot ? !L.isClearOnFoot(x, z) : false);
          for (let z = 40; z <= 60; z += 1) for (let x = -110; x <= 140; x += 2) { let ok = true;
            for (let dx = -5; dx <= 5 && ok; dx += 0.5) for (let dz = -5; dz <= 5 && ok; dz += 0.5) if (b(x + dx, z + dz)) ok = false;
            if (ok && props.every((p) => Math.hypot(p[0] - x, p[1] - z) > 5 + p[2]) && G.named.concat(G.crowd).every((p) => p.gone || p.space !== 'street' || Math.hypot(p.x - x, p.z - z) > 8)) return [x, z]; }
          return null; }""", [[p["x"], p["z"], p["r"]] for p in inv.drawn_props()])
        if not spot:
            self.record("keyboard steering eased", False, "no spot of open ground found for the measurement", phase="all", note="not reached")
            return
        x, z = spot
        g.js("() => { LEDGER.goOutside(); LEDGER.G.car.keys = true; LEDGER.cab.getIn(); }")
        g.js("([x, z]) => { const c = LEDGER.G.car; c.x = x; c.z = z; c.ang = 1.57; c.v = 9; LEDGER.G.tom.inCar = true; }", [x, z])
        V = 9.0
        self.cleared += g.clear()
        base = g.js(self.STEER_JS, [0.2, V, x, z])
        g.down("KeyD")
        press = g.js(self.STEER_JS, [0.6, V, x, z])
        g.up("KeyD")
        release = g.js(self.STEER_JS, [0.6, V, x, z])
        g.down("KeyA")
        held_a = g.js(self.STEER_JS, [0.6, V, x, z])
        g.up("KeyA")
        g.down("KeyD")  # A let go and D pressed between the same two frames
        switch = g.js(self.STEER_JS, [0.6, V, x, z])
        g.up("KeyD")
        setup = "test setup: cab on open ground at (%.0f, %.0f), kept on its spot and its speed held at %.0f m/s each frame" % (x, z, V)
        if any(x is None for x in (base, press, release, held_a, switch)):
            self.record("keyboard steering eased", False, setup, phase="all", note="a box opened during the measurement: not reached")
            return
        for phase, before, series, steps in (
                ("press", base, press, "hold D 0.6 s"),
                ("release", press, release, "after D held 0.6 s, let go"),
                ("A to D", held_a, switch, "hold A 0.6 s, then let go of A and press D in the same frame")):
            v = inv.steer_change([before[-1]] + series, DT, start=before[-1], end=series[-1])
            if phase == "A to D" and v["ok"] and abs(v.get("to", 0)) < 0.5 * abs(press[-1]):
                # the swing must end turning the other way at about full lock, or it measured something else
                v = dict(v, ok=False, reason="after the switch the cab was not turning the other way")
            self.record("keyboard steering eased", v["ok"], setup + "; " + steps, phase=phase,
                        first_frames=[round(r, 2) for r in series[:8]], **v)

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
        # the one-shot: with the menus worked by the keyboard, random keys can save and leave for the title screen
        # (Escape, down, Enter). That loses nothing; a player presses Continue, and so does this run, and says so.
        if g.js("() => LEDGER.G.story.phase === 'title'"):
            went = g.js("() => { const b = document.querySelector('[data-act=\"cont\"]'); if (!b) return false; b.click(); return true; }")
            g.run(1.5)
            self.cleared += g.clear()
            self.notes.append("button spam: the keys saved and left for the title screen; Continue %s" % ("pressed" if went else "was not offered"))
        s = g.state()
        free = not s["boxOpen"] and not s["paused"] and g.js("() => LEDGER.G.story.phase === 'play'")
        self.record("back to play after button spam", free, "%d random keys 0.1 s apart (seed 11), then Escape up to 5 times" % n,
                    escapes=tries, box=s["boxOpen"], paused=s["paused"], scene=s["inAWrittenScene"], last_keys=seq[-12:])
        if free:
            if g.js("() => LEDGER.G.tom.inCar"):
                g.tap("KeyF")
                g.run(0.3)
            track = self.escape_track(["KeyW", "KeyS", "KeyA", "KeyD"])
            self.record("never stuck (after button spam)", inv.moved_again(track)["ok"], "after the spam, walk",
                        state=g.js("() => { const G = LEDGER.G, t = G.tom, x = G.x || {}; return { modal: LEDGER.ui.modal, paused: G.paused, why: G.pauseWhy || null, inCar: t.inCar, space: t.space, at: [t.x, t.z], down: !!t.down, fighting: !!(G.fight || t.fight), foot: x.foot ? { sit: x.foot.sit || x.foot.blend || null, chase: x.foot.chase || null } : null, custody: (x.law && x.law.custody) || null, hour: (G.t / 60) % 24 }; }"),
                        **inv.moved_again(track))
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
    # (Fixed 19 Nov, round 6: at the rank a written scene opens by itself within half a second and holds the game, so
    # neither the control nor the pad could move anything and the check failed whatever the game did. Scenes are now
    # finished first, each window is tried again if a box opened in it, and a window that never ran clear is
    # "not reached", which fails.)
    def pad(self):
        g = self.g

        def window(setup_js, ms=2500):
            """Run the game in real time for ms with the pad as setup_js leaves it. Returns (before, after, box)."""
            for _ in range(4):
                self.cleared += g.clear()
                g.js("() => { for (let i = 0; i < 4; i++) { window.__pad.axes[i] = 0; } for (const b of window.__pad.buttons) { b.pressed = false; b.value = 0; } }")
                a = g.state()
                g.js(setup_js)
                g.js("window.LEDGER_NORENDER = true; window.LEDGER_MANUAL = false")
                g.pg.wait_for_timeout(ms)
                g.manual()
                b = g.state()
                g.js("() => { for (let i = 0; i < 4; i++) { window.__pad.axes[i] = 0; } for (const b of window.__pad.buttons) { b.pressed = false; b.value = 0; } }")
                if not (b["boxOpen"] or b["paused"]):
                    return a, b, None
            return a, b, b["boxOpen"] or "paused"

        def dist(a, b, who):
            return math.hypot(b[who]["xMetres"] - a[who]["xMetres"], b[who]["zMetres"] - a[who]["zMetres"])

        g.js("() => { const G = LEDGER.G; if (G.tom.inCar) LEDGER.cab.getOut(); G.car.v = 0; LEDGER.goOutside(); LEDGER.goTo('the rank'); }")
        g.run(1.0)
        c0, c1, box = window("() => {}")  # the control: the same time with no input
        control = dist(c0, c1, "tom")
        s0, s1, box2 = window("() => { window.__pad.axes[1] = -1; window.__pad.timestamp++; }")
        moved = dist(s0, s1, "tom")
        if box or box2:
            self.record("a pad moves Tom", False, "left stick full forward for 2.5 s of real time", note="not reached: a box kept opening (%s)" % (box or box2))
        else:
            self.record("a pad moves Tom", moved > control + 0.5, "scenes finished first; left stick full forward for 2.5 s of real time (game running), against 2.5 s with no input",
                        moved_m=round(moved, 2), control_m=round(control, 2))
        g.js("() => { LEDGER.G.car.keys = true; LEDGER.cab.getIn(); LEDGER.G.car.v = 0; }")
        k0, k1, box3 = window("() => { window.__pad.buttons[7].pressed = true; window.__pad.buttons[7].value = 1; }")
        moved = dist(k0, k1, "cab")
        if box3:
            self.record("a pad drives the cab", False, "in the cab, right trigger held 2.5 s of real time", note="not reached: a box kept opening (%s)" % box3)
        else:
            self.record("a pad drives the cab", moved > 0.5, "scenes finished first; in the cab, right trigger held 2.5 s of real time", moved_m=round(moved, 2))
        g.js("() => { if (LEDGER.G.tom.inCar) { LEDGER.G.car.v = 0; LEDGER.cab.getOut(); } }")

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
    HIT_JS = """async (id) => { const L = LEDGER, G = L.G, dt = 1 / 60, P = G.named.find((q) => q.id === id);
      const everyone = G.named.concat(G.crowd), downBefore = new Set(everyone.filter((q) => q.down));
      const shownAs = (q) => { const r = L.people().find((x) => x.personId === q.id), d = q.def.desc || ''; return r ? r.shownAs : d ? d[0].toUpperCase() + d.slice(1) : null; };
      const before = __gate.msgs(), e0 = G.events.length; let t = 0, hit = null, closest = 1e9;
      const fell = new Map(); let k = 0;
      const falls = (now) => { for (const q of everyone) if (q.down && q !== P && !downBefore.has(q) && !fell.has(q)) fell.set(q, now); };
      while (t < 4) { if (G.paused || L.ui.modal) return { hit: null, interrupted: L.ui.modal || 'paused', closest }; P.route = null; P.moving = false; L.tick(dt); t += dt;
        closest = Math.min(closest, Math.hypot(P.x - G.car.x, P.z - G.car.z)); falls(-1); if (P.down) { hit = t; break; } }
      if (hit === null) return { hit, closest };
      // others who fall while the words are watched: when each fell, counted from the hit frame (-1: before it)
      const frames = await __gate.watch(3.0, dt, () => { falls(k * dt); k++; });
      falls(k * dt);
      const others = [...fell].map(([q, at]) => ({ name: q.def.name || q.def.desc || 'someone', shown: shownAs(q), fell_at_s: at, dead: !!q.dead }));
      return { hit, closest, before, frames, kinds: G.events.slice(e0).map((e) => e.kind), down: !!P.down, dead: !!P.dead, hurt: P.hurt || 0,
               others, prompts: L.prompts().concat(((L.written.read().open && L.written.read().choices) || []).map((c, i) => ({ key: String(i + 1), text: c }))) }; }"""

    def person_hit(self):
        g = self.g
        knocked_rx, count_rx = inv.source_phrases("knocked"), inv.count_line_rx()
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
            self.cleared += g.clear()
            g.down("KeyW")
            h = g.js(self.HIT_JS, r["id"])
            g.up("KeyW")
            tried.append(r["name"])
            if h["hit"] is None:
                continue
            steps = "test setup: %s held still on the street, cab 14 m back at 4.5 m/s on a clear line, hold W" % r["name"]
            frames = [(f["t"], f) for f in h["frames"]]
            v = inv.told(h["before"], frames, knocked_rx, count_rx=count_rx)
            self.record("a person hit is hurt, never killed", not h["dead"], steps, person=r["name"], hurt=round(h["hurt"], 2), dead=h["dead"])
            self.record("a person hit: told on screen", v["ok"], steps + "; the game's message lists read each frame from the hit",
                        person=r["name"], event_kinds=h["kinds"], **v)
            # Others knocked down on the way (people standing together): each must be told in words too, by the name
            # Tom knows them by, within the limit of their own fall, and none killed. (Changed 19 Nov, round 6: this
            # used to fail whenever anybody else went down. A cab driven through three people standing together
            # knocks down three; the fault the gate found was that nothing said so.)
            for o in h["others"]:
                at = max(o["fell_at_s"], 0.0)  # someone knocked down on the way in is judged from the hit frame
                told = None
                for t, d in frames:
                    if told is not None or t < at - 1e-9:
                        continue
                    for place in inv.SCREEN_PLACES:
                        v = d.get(place) or []
                        for text in ([v] if isinstance(v, str) else v):
                            if told is None and o["shown"] and o["shown"] in (text or "") and any(p.search(text) for p in knocked_rx):
                                told = round(t - at, 2)
                ok = told is not None and told <= inv.SILENT_LIMIT_S + 1e-9 and not o["dead"]
                self.record("everyone knocked down is told on screen", ok, steps + "; others who went down in the same run",
                            person=o["name"], shown_as=o["shown"], fell_at_s=o["fell_at_s"], told_after_s=told, dead=o["dead"])
            # keyed by the rule alone (driven_at is not a signature key): the missing choice is not about who was hit
            self.record("a person hit: a choice is offered (stop and help, or drive off)",
                        any("help" in (c.get("text") or "").lower() for c in h["prompts"]), "the key prompts and the written choice 3 s after the hit",
                        driven_at=r["name"], prompts=h["prompts"])
            break
        else:
            self.record("a person hit is hurt, never killed", False, "no one was knocked down after trying %s" % tried, note="not reached")
        g.js("() => { LEDGER.G.car.v = 0; if (LEDGER.G.tom.inCar) LEDGER.cab.getOut(); }")

    # 11. drawn against solid: Tom walks at every drawn thing on the street (lamp posts, bollards, bins, stalls,
    #     parked cars...) and must not pass through it
    def drawn_solid(self):
        g = self.g
        props = inv.drawn_props()
        g.js("() => { LEDGER.goOutside(); if (LEDGER.G.tom.inCar) LEDGER.cab.getOut(); }")
        walk_js = """([px, pz, pr]) => { const L = LEDGER, G = L.G, t = G.tom, dt = 1 / 60, b = (x, z) => L.isBlocked(x, z);
              const st = pr + 2.5;
              for (let k = 0; k < 16; k++) { const a = k * Math.PI / 8, sx = Math.sin(a), sz = Math.cos(a);
                const x0 = px - sx * st, z0 = pz - sz * st; let ok = true;
                for (let d = pr + 0.6; d <= st; d += 0.25) if (b(px - sx * d, pz - sz * d)) { ok = false; break; }
                if (!ok) continue;
                t.x = x0; t.z = z0; t.v = 0; L.cam.yaw = a; let closest = 1e9, s = 0;
                while (s < 2.5) { if (G.paused || L.ui.modal) return { interrupted: L.ui.modal || 'paused' }; L.tick(dt); s += dt;
                  closest = Math.min(closest, Math.hypot(t.x - px, t.z - pz)); }
                return { from: [x0, z0], yaw: a, start: st, closest, blockedAtCentre: b(px, pz) }; }
              return null; }"""
        for p in props:
            label = "%s at (%.1f, %.1f)" % (p["type"], p["x"], p["z"])
            steps = "test setup: Tom put %.1f m from the %s, camera turned to face it; hold W 2.5 s" % (p["r"] + 2.5, label)
            for _ in range(4):  # a talk that starts by itself stops the game: finish it, then try again
                self.cleared += g.clear()
                g.down("KeyW")
                r = g.js(walk_js, [p["x"], p["z"], p["r"]])
                g.up("KeyW")
                if not (r and r.get("interrupted")):
                    break
            if not r:
                self.notes.append("drawn things: no clear walk-up to the %s" % label)
                continue
            if r.get("interrupted") or r["closest"] > r["start"] - 0.5:
                self.record("drawn things are solid (on foot)", False, steps, target=p["type"], prop=label,
                            note="not reached: " + ("a box kept opening" if r.get("interrupted") else "Tom did not walk"))
                continue
            through = r["closest"] < min(0.25, p["r"])
            self.record("drawn things are solid (on foot)", not through, steps, target=p["type"], prop=label,
                        closest_m=round(r["closest"], 2), solid_in_collision_map=r["blockedAtCentre"],
                        **({"note": "Tom walked through it"} if through else {}))


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
    order = ["foot_walls", "corners", "drawn_solid", "cab_crashes", "cab_steering", "out_and_in", "person_hit", "pad", "indoors", "pause_save", "key_spam"]
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
    for rule in ["never stuck (cab after a hit)", "damage told", "a person hit is hurt, never killed", "a person hit: told on screen",
                 "never stuck (indoors)", "camera clear", "keyboard steering eased", "drawn things are solid (on foot)",
                 "drawn things are solid (cab)"]:
        if not a.only and not any(r["rule"] == rule for r in gate.results):
            gate.record("tested something: " + rule, False, "no case of this rule was reached in the run")
    summary = inv.summarise(gate.results)
    gate.notes.append("the 'told on screen' checks read the game's own message lists each frame from the event frame, one game step per drawn frame so the page's hud runs, and match the game's own lines for the event (kinds.js, talk_lines.js)")
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
