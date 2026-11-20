"""Feel in numbers (lane task 4t, piece 4). Code only, no model.

    python feel_numbers.py --dist DIR [--out DIR] [--refs FILE]

Plays short drills on a build of the LEDGER loop prototype with real key events, steps the page's own frame loop
at exactly 1/60 s (so the game's camera code runs as in play), records every frame from outside (positions,
camera, field of view, the fight's state, the man struck on screen or not) and measures from those frames:

  on foot   W1 start (to 90% of walking and running speed), W2 stop, W3 a 180-degree turn while running,
            W4 walking and running speed, W5 and W6 camera distance and height, W7 camera lag, W8 field of view
  cab       M5 steering response (turn rate at 63% after the key) and self-centring (turn rate under 5%),
            M10 camera distance behind, height, lag and field of view at rest and at 9 m/s
  fists     C1 key to the blow starting, C2 start to contact and recovery after contact, C3 hit-stop,
            C4 the man struck's reaction, C10 fight camera distance and the other man (and his feet) in frame;
            each also read from the game's own drill record and compared: a disagreement of more than a frame
            and a half is a fault of the record

Speeds come from positions frame to frame, never from the game's speed variable. Each number is compared with
its reference band: the driving feel sheet (FEEL-TARGETS-DRIVING-2026-11-17.md, M5 and M10) and the melee sheet
(FEEL-TARGETS-MELEE-2026-11-18.md, C1 to C10). Both sheets' bands are mostly estimates, said so in the report.
On foot has no band until the builder's measurements of the reference games exist (from 23 Nov, the measuring
method FEEL-MEASUREMENT-METHOD-2026-11-20.md): --refs FILE (JSON, {"W1_walk_s": [lo, hi], ...}) adds or replaces
bands, and a number with no band is reported as "no reference yet", never passed.

The recordings (one JSON line a frame per drill) are kept in the out folder, so any number can be checked by
hand. The game's code is never changed; every test setup (where Tom or the cab is put, a speed held, a still
man to hit) is named in the drill's steps. Exit code 1 if any number is outside its band or a drill was not
reached.
"""
import argparse
import datetime
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

DT = 1 / 60
FRAME = DT

# ---------------------------------------------------------------- reference bands
# id: (low, high, unit, source, how sure). Only bands the sheets give; on foot waits for our own measurements.
REFS = {
    "M5_yaw63_s": (0.20, 0.35, "s", "driving sheet M5, ordinary hatch", "estimate [I]"),
    "M5_centre_s": (0.6, 1.2, "s", "driving sheet M5, self-centre to under 5%", "estimate [I]"),
    "M10_behind_m": (5.0, 7.0, "m", "driving sheet M10, camera behind the car's centre", "estimate [I]"),
    "M10_height_m": (1.6, 2.2, "m", "driving sheet M10, camera height", "estimate [I]"),
    "M10_lag_s": (0.1, 0.3, "s", "driving sheet M10, position lag", "estimate [I]"),
    "M10_hfov0_deg": (60.0, 65.0, "deg", "driving sheet M10, field of view at rest", "estimate [I]"),
    "C1_jab_s": (0.0, 0.10, "s", "melee sheet C1, key to the blow starting", "estimate"),
    "C1_heavy_s": (0.0, 0.10, "s", "melee sheet C1", "estimate"),
    "C2_jab_contact_s": (0.25, 0.40, "s", "melee sheet C2, jab start to contact", "real jab 0.36 s [READ]"),
    "C2_jab_recover_s": (0.20, 0.40, "s", "melee sheet C2, jab recovery after contact, freeze not counted", "estimate"),
    "C2_heavy_contact_s": (0.63, 0.85, "s", "melee sheet C2, heavy start to contact", "KCD2 study 14"),
    "C2_heavy_recover_s": (0.35, 0.50, "s", "melee sheet C2, heavy recovery after contact", "KCD2 study 14"),
    "C3_jab_stop_s": (0.025, 0.05, "s", "melee sheet C3, jab hit-stop", "estimate"),
    "C3_heavy_stop_s": (0.06, 0.12, "s", "melee sheet C3, heavy hit-stop", "estimate"),
    "C4_jab_react_s": (0.50, 0.70, "s", "melee sheet C4, light reaction", "KCD2 study 14"),
    "C4_heavy_react_s": (0.90, 1.30, "s", "melee sheet C4, heavy reaction", "KCD2 study 14"),
    "C10_cam_m": (3.5, 5.0, "m", "melee sheet C10, fight camera distance", "his 28 Oct pick; numbers estimate"),
    "C10_foe_in_frame": (0.95, 1.0, "share", "melee sheet C10, both men in frame", "his 28 Oct pick"),
    "C10_feet_in_frame": (0.90, 1.0, "share", "melee sheet C10, the other man's feet in frame", "his 28 Oct pick"),
}
TOL = FRAME / 2  # a number within half a frame of its band's edge counts as inside (frames are 1/60 s)

# ---------------------------------------------------------------- pure measures (tested in test_feel_numbers.py)


def speeds(xs, zs, dt=DT):
    """Speed each frame from positions (m/s); the first frame repeats the second."""
    v = [math.hypot(xs[i] - xs[i - 1], zs[i] - zs[i - 1]) / dt for i in range(1, len(xs))]
    return [v[0] if v else 0.0] + v


def steady(vals, frac=0.25):
    """Middle value of the last `frac` of a series (the settled value)."""
    tail = sorted(vals[-max(1, int(len(vals) * frac)):])
    return tail[len(tail) // 2] if tail else None


def time_to_reach(vals, start, target, frac=0.9, dt=DT):
    """Seconds from frame `start` until vals first reaches frac of target (target > 0). None if never."""
    for i in range(start, len(vals)):
        if vals[i] >= frac * target:
            return (i - start + 1) * dt
    return None


def time_to_fall(vals, start, below, dt=DT):
    """Seconds from frame `start` until |vals| is first at or under `below`. None if never."""
    for i in range(start, len(vals)):
        if abs(vals[i]) <= below:
            return (i - start + 1) * dt
    return None


def first_change(vals, start, eps=1e-6):
    """Frames from `start` until vals first differs from vals[start-1] by more than eps (key to visible change)."""
    base = vals[start - 1] if start > 0 else vals[0]
    for i in range(start, len(vals)):
        if abs(vals[i] - base) > eps:
            return i - start + 1
    return None


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def heading(xs, zs, i):
    return math.atan2(xs[i] - xs[i - 1], zs[i] - zs[i - 1])


def turn_time(xs, zs, start, top, dir0, within_deg=20.0, frac=0.9, dt=DT):
    """180-degree turn: seconds from frame `start` until he moves the opposite way of dir0 (within within_deg) at
    frac of top speed."""
    v = speeds(xs, zs, dt)
    want = wrap(dir0 + math.pi)
    for i in range(max(1, start), len(xs)):
        if v[i] >= frac * top and abs(wrap(heading(xs, zs, i) - want)) <= math.radians(within_deg):
            return (i - start + 1) * dt
    return None


def lag_seconds(dist_moving, dist_rest, speed):
    """Camera position lag as a time: the extra distance the camera trails at a steady speed, over that speed
    (the time constant of a follow camera; zero for a camera fixed to the body)."""
    if not speed or speed < 0.2 or dist_moving is None or dist_rest is None:
        return None
    return max(0.0, (dist_moving - dist_rest) / speed)


def hfov(vfov_deg, aspect):
    return math.degrees(2 * math.atan(math.tan(math.radians(vfov_deg) / 2) * aspect))


def runs_of(flags, start=0):
    """Length in frames of the first run of True at or after `start`; (index, length) or (None, 0)."""
    i = next((k for k in range(start, len(flags)) if flags[k]), None)
    if i is None:
        return None, 0
    n = 0
    while i + n < len(flags) and flags[i + n]:
        n += 1
    return i, n


def strike_from_frames(fr, press):
    """A blow from the per-frame fight record. fr: list of dicts with st (Tom's fight state), stop (hit-stop left),
    foeHurt, foeSt. press: the frame index the key went down before. Returns seconds for C1 to C4."""
    st = [f["st"] for f in fr]
    hurt = [f["foeHurt"] or 0 for f in fr]
    start = next((i for i in range(press, len(fr)) if st[i] not in ("idle", "block")), None)
    contact = next((i for i in range(press + 1, len(fr)) if hurt[i] > hurt[i - 1] + 1e-9), None)
    out = {"press_to_start_s": None if start is None else (start - press + 1) * DT,
           "start_to_contact_s": None, "hitstop_s": None, "recover_s": None, "react_s": None}
    if start is None or contact is None:
        return out
    out["start_to_contact_s"] = (contact - start) * DT
    _, nstop = runs_of([f["stop"] > 1e-9 for f in fr], contact)
    out["hitstop_s"] = nstop * DT
    back = next((i for i in range(contact + 1, len(fr)) if st[i] in ("idle", "block")), None)
    if back is not None:
        out["recover_s"] = (back - contact) * DT - nstop * DT
    i0, nre = runs_of([f["foeSt"] == "stagger" for f in fr], contact)
    if i0 is not None and i0 - contact <= 2:
        out["react_s"] = nre * DT
    return out


def strike_from_record(tele):
    """The same numbers from the game's own drill record (melee_drills.py's events)."""
    def first(ev, after=-1.0, actor=None):
        return next((e for e in tele if e["ev"] == ev and e["t"] > after and (actor is None or e.get("actor") == actor)), None)
    hs = first("hit_start", actor="player")
    hc = first("hit_contact", actor="player")
    s0 = first("hitstop_start")
    s1 = first("hitstop_end")
    rc = first("recovery_end", actor="player")
    g0 = next((e for e in tele if e["ev"] == "stagger_start" and e.get("actor") != "player"), None)
    g1 = next((e for e in tele if e["ev"] == "stagger_end" and e.get("actor") != "player"), None)
    stop = (s1["t"] - s0["t"]) if s0 and s1 else 0.0
    return {"start_to_contact_s": (hc["t"] - hs["t"]) if hs and hc else None,
            "hitstop_s": stop if s0 and s1 else None,
            "recover_s": (rc["t"] - hc["t"] - stop) if rc and hc else None,
            "react_s": (g1["t"] - g0["t"]) if g0 and g1 else None}


def judge(key, value, refs=REFS):
    """One number against its band: inside, outside, not measured, or no reference yet."""
    band = refs.get(key)
    row = {"id": key, "value": None if value is None else round(value, 3)}
    if value is None:
        row["verdict"] = "not measured"
        return row
    if not band:
        row["verdict"] = "no reference yet"
        return row
    lo, hi = band[0], band[1]
    tol = TOL if band[2] == "s" else 1e-9
    row.update(band=[lo, hi], unit=band[2], source=band[3], sure=band[4] if len(band) > 4 else "")
    row["verdict"] = "inside" if lo - tol <= value <= hi + tol else "outside"
    return row


def compare_record(frames, record, kind):
    """Frames against the game's own record: a disagreement over a frame and a half is a fault of the record."""
    out = []
    for k in ("start_to_contact_s", "hitstop_s", "recover_s", "react_s"):
        a, b = frames.get(k), record.get(k)
        if a is None or b is None:
            if (a is None) != (b is None):
                out.append("%s %s: frames say %s, the game's record says %s" % (kind, k, a, b))
            continue
        if abs(a - b) > 1.5 * FRAME:
            out.append("%s %s: frames %.3f s, the game's record %.3f s" % (kind, k, a, b))
    return out


# ---------------------------------------------------------------- the page

# The page's frame loop caught before it loads: free running until __feel.hold, then each call of step() runs
# every waiting frame callback once with a clock 1/60 s on, so the game's logic AND its camera run as in play.
HOLD_INIT = """
(() => { const real = window.requestAnimationFrame.bind(window);
  const F = window.__feel = { hold: false, now: 0, cbs: [] };
  window.requestAnimationFrame = (cb) => { if (F.hold) { F.cbs.push(cb); return 1; }
    return real((ts) => { F.now = ts; cb(ts); }); };
})();
"""

SAMPLE_JS = """() => { const L = LEDGER, G = L.G, t = G.tom, c = G.car, k = L.cam, cam = L.camera, F = L.F, T = L.THREE;
  const P = F.on && F.T ? F.T : null, foe = P && F.foes ? F.foes.find((f) => f.P === P) : null;
  let inF = null, feetF = null;
  if (P) { cam.updateMatrixWorld(); const v = new T.Vector3(P.x, 1.2, P.z).project(cam), w = new T.Vector3(P.x, 0.05, P.z).project(cam);
    inF = Math.abs(v.x) <= 1 && Math.abs(v.y) <= 1 && v.z < 1; feetF = Math.abs(w.x) <= 1 && Math.abs(w.y) <= 1 && w.z < 1; }
  const steer = L.cabFeel ? L.cabFeel().steerMinusOneToOne : null;
  return { tx: t.x, tz: t.z, tang: t.ang, inCar: !!t.inCar, cx: c.x, cz: c.z, cang: c.ang, steer,
    camx: cam.position.x, camy: cam.position.y, camz: cam.position.z, lookx: k.tx, looky: k.ty, lookz: k.tz,
    vfov: cam.fov, aspect: cam.aspect, carry: t.carry || null, run: !!t.run, fight: F.on, st: F.st, stop: F.stop || 0, foeHurt: P ? P.hurt : null,
    foeSt: foe ? foe.st : null, foeX: P ? P.x : null, foeZ: P ? P.z : null, inFrame: inF, feetInFrame: feetF,
    modal: L.ui.modal || null }; }"""

STEP_JS = """([n, dt, pre]) => { const F = window.__feel, out = [], S = eval(window.__feelSample), f = pre ? eval(pre) : null;
  for (let i = 0; i < n; i++) { if (f) f(); const cbs = F.cbs; F.cbs = []; F.now += dt * 1000; for (const cb of cbs) cb(F.now); out.push(S()); }
  return out; }"""

OPEN_LINE_JS = """([props, len, half]) => { const L = LEDGER, G = L.G;
  const bad = (x, z) => L.isBlocked(x, z) || (L.isClearOnFoot ? !L.isClearOnFoot(x, z) : false) ||
    props.some((p) => Math.hypot(p[0] - x, p[1] - z) < p[2] + 0.6);
  const folk = G.named.concat(G.crowd).filter((p) => !p.gone && p.space === 'street');
  for (let z = -120; z <= 160; z += 2) for (let x = -140; x <= 160; x += 2) for (const a of [0, Math.PI / 2, Math.PI, -Math.PI / 2]) {
    const fx = Math.sin(a), fz = Math.cos(a); let ok = true;
    for (let s = -8; s <= len && ok; s += 1) for (let w = -half; w <= half && ok; w += 0.75) {
      const px = x + fx * s + fz * w, pz = z + fz * s - fx * w; if (bad(px, pz)) ok = false; }
    if (ok && folk.every((p) => { const s = (p.x - x) * fx + (p.z - z) * fz, w = Math.abs((p.x - x) * fz - (p.z - z) * fx);
      return s < -10 || s > len + 4 || w > half + 3; })) return [x, z, a]; }
  return null; }"""


class Feel:
    def __init__(self, dist, out, refs=None):
        from clumsy import Proto

        class HeldProto(Proto):
            EXTRA_INIT = HOLD_INIT
        self.g = HeldProto(dist)
        self.g.clear()
        self.out = out
        self.refs = dict(REFS)
        for k, v in (refs or {}).items():  # [low, high] or [low, high, unit]: our own measured bands replace the sheets'
            self.refs[k] = (v[0], v[1], v[2] if len(v) > 2 else ("s" if k.endswith("_s") else ""), "--refs file", "our measurement")
        self.rows, self.faults, self.notes, self.drills = [], [], [], []
        pg = self.g.pg
        pg.set_viewport_size({"width": 480, "height": 270})  # same 16:9 shape; the picture is not looked at
        self.g.js("(s) => { window.__feelSample = s; }", SAMPLE_JS)
        self.g.js("() => { window.LEDGER_MANUAL = false; window.LEDGER_NORENDER = false; LEDGER.scene.visible = false; LEDGER.G.paused = false; }")
        pg.wait_for_timeout(300)
        self.g.js("() => { window.__feel.hold = true; }")
        pg.wait_for_timeout(300)  # the last free frame hands its callback to the hold
        self.g.js("() => { window.__feel.now = performance.now(); }")
        self.step(30)  # first held frames: the loop's own clock settles onto 1/60 s

    def step(self, n, pre=None):
        return self.g.js(STEP_JS, [n, DT, pre])

    def keep(self, name, steps, frames):
        path = os.path.join(self.out, "feel-%s.jsonl" % name)
        with open(path, "w", encoding="utf-8") as f:
            for i, r in enumerate(frames):
                f.write(json.dumps(dict(r, frame=i)) + "\n")
        self.drills.append({"drill": name, "steps": steps, "frames": len(frames), "recording": os.path.basename(path)})

    def add(self, key, value, drill):
        r = judge(key, value, self.refs)
        r["drill"] = drill
        self.rows.append(r)
        return r

    def line(self):
        import invariants as inv
        props = [[p["x"], p["z"], p["r"]] for p in inv.drawn_props()]
        return self.g.js(OPEN_LINE_JS, [props, 45, 2.5])

    def place_tom(self, x, z, a, empty_handed=False):
        self.g.js("""([x, z, a, e]) => { const L = LEDGER, t = L.G.tom; if (L.F.on) L.fight.end(); L.goOutside(); t.inCar = false;
          t.x = x; t.z = z; t.ang = a; t.hurt = 0; L.cam.yaw = a; L.cam.snap = true;
          if (e) { window.__feelCarry = window.__feelCarry || t.carry; t.carry = null; } }""", [x, z, a, empty_handed])
        self.g.clear()
        self.step(90)

    # on foot: walk, run, stop, turn, camera
    def on_foot(self, spot):
        x, z, a = spot
        steps = "test setup: Tom put on open ground at (%.0f, %.0f) facing along 45 m of clear street, camera behind him" % (x, z)
        self.place_tom(x, z, a)
        rest = self.step(30)
        g = self.g
        g.down("KeyW")
        walk = self.step(180)
        g.up("KeyW")
        wstop = self.step(90)
        fr = rest + walk + wstop
        self.keep("walk", steps + "; still 0.5 s, hold W 3 s, let go 1.5 s", fr)
        xs, zs = [f["tx"] for f in fr], [f["tz"] for f in fr]
        v = speeds(xs, zs)
        p0, r0 = len(rest), len(rest) + len(walk)
        vw = steady(v[p0:r0])
        self.add("W4_walk_mps", vw, "walk")
        self.add("W1_walk_s", time_to_reach(v, p0, vw) if vw else None, "walk")
        self.add("W2_walk_stop_s", time_to_fall(v, r0, 0.05) if vw else None, "walk")
        d_rest = steady([math.hypot(f["camx"] - f["tx"], f["camz"] - f["tz"]) for f in rest])
        d_walk = steady([math.hypot(f["camx"] - f["tx"], f["camz"] - f["tz"]) for f in walk])
        self.add("W5_cam_behind_m", d_rest, "walk")
        self.add("W6_cam_height_m", steady([f["camy"] for f in rest]), "walk")
        self.add("W7_cam_lag_walk_s", lag_seconds(d_walk, d_rest, vw), "walk")
        self.add("W8_hfov_walk_deg", hfov(fr[-1]["vfov"], fr[-1]["aspect"]), "walk")
        self.notes.append("walk: Tom as the new week starts him (carrying: %s)" % (fr[0].get("carry") or "nothing"))
        # running: he cannot run with the suitcase, so it is taken from his hands for the run and the turn
        self.place_tom(x, z, a, empty_handed=True)
        rest = self.step(30)
        g.down("Shift")
        g.down("KeyW")
        run = self.step(240)
        g.up("KeyW")
        rstop = self.step(90)
        g.up("Shift")
        fr = rest + run + rstop
        steps += "; test setup: whatever he carries taken from his hands (he cannot run carrying)"
        self.keep("run", steps + "; still 0.5 s, hold Shift and W 4 s, let go of W 1.5 s", fr)
        xs, zs = [f["tx"] for f in fr], [f["tz"] for f in fr]
        v = speeds(xs, zs)
        p0, r0 = len(rest), len(rest) + len(run)
        vr = steady(v[p0:r0])
        if not any(f["run"] for f in run):
            self.faults.append("run: Shift and W held 4 s, empty-handed, and he never ran")
            vr = None
        self.add("W4_run_mps", vr, "run")
        self.add("W1_run_s", time_to_reach(v, p0, vr) if vr else None, "run")
        self.add("W2_run_stop_s", time_to_fall(v, r0, 0.05) if vr else None, "run")
        d_run = steady([math.hypot(f["camx"] - f["tx"], f["camz"] - f["tz"]) for f in run])
        self.add("W7_cam_lag_run_s", lag_seconds(d_run, d_rest, vr), "run")
        self.add("W8_hfov_run_deg", hfov(run[-1]["vfov"], run[-1]["aspect"]), "run")
        # 180-degree turn while running: W held, then S instead (the camera's back)
        self.place_tom(x, z, a, empty_handed=True)
        g.down("Shift")
        g.down("KeyW")
        go = self.step(90)
        g.up("KeyW")
        g.down("KeyS")
        back = self.step(150)
        g.up()
        self.step(30)
        fr = go + back
        self.keep("turn", steps + "; hold Shift and W 1.5 s, then S instead of W (W let go and S pressed between the same two frames) 2.5 s", fr)
        xs, zs = [f["tx"] for f in fr], [f["tz"] for f in fr]
        top = vr or steady(speeds(xs, zs)[:len(go)])
        dir0 = heading(xs, zs, len(go) - 1)
        self.add("W3_turn180_s", turn_time(xs, zs, len(go), top, dir0) if top else None, "turn")
        # his body: the frames until he faces the new way (within 20 degrees); moving and facing can differ
        want = wrap(dir0 + math.pi)
        face = next((i for i in range(len(go), len(fr)) if abs(wrap(fr[i]["tang"] - want)) <= math.radians(20)), None)
        self.add("W3_face180_s", None if face is None else (face - len(go) + 1) * DT, "turn")
        self.g.js("() => { const t = LEDGER.G.tom; if (window.__feelCarry) { t.carry = window.__feelCarry; window.__feelCarry = null; } }")

    # the cab: steering response and the camera
    def cab(self, spot):
        x, z, a = spot
        g = self.g
        g.js("() => { const L = LEDGER; L.goOutside(); L.G.car.keys = true; L.cab.getIn(); }")
        g.js("([x, z, a]) => { const L = LEDGER, c = L.G.car; c.x = x; c.z = z; c.ang = a; c.v = 0; L.G.tom.inCar = true; L.cam.yaw = a; L.cam.snap = true; }", [x, z, a])
        g.clear()
        if not g.js("() => !!LEDGER.G.tom.inCar"):
            self.faults.append("cab: Tom could not be put in the cab: not reached")
            return
        hold = "(() => { const c = LEDGER.G.car; return () => { c.x = %f; c.z = %f; c.v = 9; }; })()" % (x, z)
        steps = "test setup: cab on open ground at (%.0f, %.0f), kept on its spot and its speed held at 9 m/s each frame" % (x, z)
        self.step(60, hold)
        base = self.step(30, hold)
        g.down("KeyD")
        press = self.step(60, hold)
        g.up("KeyD")
        rel = self.step(90, hold)
        fr = base + press + rel
        self.keep("cab-steer", steps + "; 0.5 s straight, hold D 1 s, let go 1.5 s", fr)
        ang = [f["cang"] for f in fr]
        yaw = [0.0] + [wrap(ang[i] - ang[i - 1]) / DT for i in range(1, len(ang))]
        p0, r0 = len(base), len(base) + len(press)
        peak = steady(yaw[p0:r0], 0.2)
        if peak and abs(peak) > 0.05:
            s = 1 if peak > 0 else -1
            self.add("M5_yaw63_s", time_to_reach([s * y for y in yaw], p0, abs(peak), 0.63), "cab-steer")
            self.add("M5_centre_s", time_to_fall(yaw, r0, 0.05 * abs(peak)), "cab-steer")
        else:
            self.add("M5_yaw63_s", None, "cab-steer")
            self.faults.append("cab: holding D at 9 m/s did not turn the cab")
        # camera at rest and at a held 9 m/s, moving freely along the clear line
        g.js("([x, z, a]) => { const L = LEDGER, c = L.G.car; c.x = x; c.z = z; c.ang = a; c.v = 0; L.cam.yaw = a; L.cam.snap = true; }", [x, z, a])
        still = "(() => { const c = LEDGER.G.car; return () => { c.v = 0; }; })()"
        go = "(() => { const c = LEDGER.G.car; return () => { c.v = 9; c.ang = %f; }; })()" % a
        rest = self.step(120, still)
        moving = self.step(150, go)
        fr = rest + moving
        self.keep("cab-camera", "test setup: cab on a clear straight at (%.0f, %.0f), still 2 s, then its speed held at 9 m/s and its heading held 2.5 s" % (x, z), fr)
        dist = [math.hypot(f["camx"] - f["cx"], f["camz"] - f["cz"]) for f in fr]
        d0, d9 = steady(dist[:len(rest)]), steady(dist[len(rest):])
        v9 = steady(speeds([f["cx"] for f in moving], [f["cz"] for f in moving]))
        self.add("M10_behind_m", d0, "cab-camera")
        self.add("M10_height_m", steady([f["camy"] for f in rest]), "cab-camera")
        self.add("M10_lag_s", lag_seconds(d9, d0, v9), "cab-camera")
        self.add("M10_hfov0_deg", hfov(rest[-1]["vfov"], rest[-1]["aspect"]), "cab-camera")
        self.add("M10_hfov9_deg", hfov(moving[-1]["vfov"], moving[-1]["aspect"]), "cab-camera")
        g.js("() => { const L = LEDGER; L.G.car.v = 0; if (L.G.tom.inCar && L.cab.getOut) L.cab.getOut(); }")
        g.clear()

    # fists: one still man 1.0 m in front; J for a jab, U for a heavy blow
    def fists(self, spot):
        x, z, a = spot
        for kind, key in (("jab", "KeyJ"), ("heavy", "KeyU")):
            self.place_tom(x, z, a)
            s = self.g.js("""([x, z, a]) => { const L = LEDGER, G = L.G, t = G.tom, F = L.F;
              const men = G.crowd.filter((p) => !p.gone && !p.dead && !p.inCar && p.def.sex !== 'f' && (p.def.age || 30) < 60);
              if (!men.length) return { error: 'no man in the crowd' };
              const P = men[0]; P.space = 'street'; P.x = x + Math.sin(a); P.z = z + Math.cos(a); P.hurt = 0; P.down = false; P.def.nerve = 0.95;
              L.fight.setOn([P]); F.tele = []; F.stam = 1; for (const f of F.foes) f.st = 'still'; L.cam.snap = true;
              return { man: P.def.name }; }""", [x, z, a])
            steps = "test setup: Tom on open ground at (%.0f, %.0f); one man 1.0 m in front, made to stand still; the fight set on" % (x, z)
            if s.get("error"):
                self.faults.append("fists %s: %s: not reached" % (kind, s["error"]))
                continue
            keep_still = "(() => { const F = LEDGER.F; return () => { for (const f of F.foes) if (f.st !== 'stagger' && f.st !== 'still') f.st = 'still'; }; })()"
            pre = self.step(60, keep_still)
            self.g.down(key)
            self.g.up(key)
            after = self.step(150, keep_still)
            fr = pre + after
            tele = self.g.js("() => (LEDGER.F.tele || []).slice()")
            self.g.js("() => { const L = LEDGER; L.F.tele = null; if (L.F.on) L.fight.end(); }")
            self.keep("fists-" + kind, steps + "; 1 s still, press and let go %s, 2.5 s" % key[-1], fr)
            m = strike_from_frames(fr, len(pre))
            self.add("C1_%s_s" % kind, m["press_to_start_s"], "fists-" + kind)
            self.add("C2_%s_contact_s" % kind, m["start_to_contact_s"], "fists-" + kind)
            self.add("C2_%s_recover_s" % kind, m["recover_s"], "fists-" + kind)
            self.add("C3_%s_stop_s" % kind, m["hitstop_s"], "fists-" + kind)
            self.add("C4_%s_react_s" % kind, m["react_s"], "fists-" + kind)
            if kind == "heavy":
                inside = [f for f in fr if f["fight"]]
                self.add("C10_cam_m", steady([math.hypot(f["camx"] - f["tx"], f["camz"] - f["tz"]) for f in inside]) if inside else None, "fists-heavy")
                self.add("C10_foe_in_frame", sum(1 for f in inside if f["inFrame"]) / len(inside) if inside else None, "fists-heavy")
                self.add("C10_feet_in_frame", sum(1 for f in inside if f["feetInFrame"]) / len(inside) if inside else None, "fists-heavy")
            self.faults += compare_record(m, strike_from_record(tele), kind)

    def run(self):
        spot = self.line()
        if not spot:
            self.faults.append("no clear straight of 45 m found: every drill not reached")
            return
        self.spot = spot
        for name, fn in (("on foot", self.on_foot), ("cab", self.cab), ("fists", self.fists)):
            try:
                fn(spot)
            except Exception as e:  # a drill that breaks is not reached, never passed
                self.faults.append("%s: the drill broke (%s): not reached" % (name, str(e)[:200]))
        errs = [e for e in self.g.errors if "404" not in e]
        if errs:
            self.faults.append("page errors during the drills: %s" % "; ".join(errs[:5]))

    def close(self):
        self.g.close()


def report_md(res):
    lines = ["# Feel in numbers: %s" % res["when"], "",
             "Measured from frames at 1/60 s with real keys (tools/lane/gate/feel_numbers.py). Bands are the driving and melee "
             "sheets'; most are estimates. No band means no reference yet (on foot waits for the builder's measurements).", "",
             "| Number | Value | Band | Verdict | Drill |", "|---|---|---|---|---|"]
    for r in res["numbers"]:
        band = "%s to %s %s" % (r["band"][0], r["band"][1], r.get("unit", "")) if r.get("band") else ""
        lines.append("| %s | %s | %s | %s | %s |" % (r["id"], r["value"], band, r["verdict"], r["drill"]))
    lines += ["", "Notes:"] + ["- " + n for n in res.get("notes", [])]
    lines += ["", "Faults: %d" % len(res["faults"])] + ["- " + f for f in res["faults"]]
    lines += ["", "Drills (recordings in the out folder):"] + ["- %s: %s (%d frames, %s)" % (d["drill"], d["steps"], d["frames"], d["recording"]) for d in res["drills"]]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dist", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--refs", default=None)
    a = ap.parse_args(argv)
    out = a.out or os.path.join(os.getcwd(), "feel-out")
    os.makedirs(out, exist_ok=True)
    refs = json.load(open(a.refs, encoding="utf-8")) if a.refs else None
    f = Feel(a.dist, out, refs)
    try:
        f.run()
    finally:
        f.close()
    res = {"when": datetime.datetime.now().isoformat(timespec="minutes"), "spot": getattr(f, "spot", None),
           "numbers": f.rows, "faults": f.faults, "notes": f.notes, "drills": f.drills,
           "outside": [r["id"] for r in f.rows if r["verdict"] == "outside"],
           "not_measured": [r["id"] for r in f.rows if r["verdict"] == "not measured"]}
    json.dump(res, open(os.path.join(out, "feel.json"), "w", encoding="utf-8"), indent=1)
    open(os.path.join(out, "FEEL.md"), "w", encoding="utf-8").write(report_md(res))
    print(report_md(res))
    return 1 if (res["outside"] or res["not_measured"] or f.faults) else 0


if __name__ == "__main__":
    sys.exit(main())
