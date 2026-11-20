"""Machine checks on every build of the LEDGER loop prototype (lane task 4t, piece 1). Code only, no model.

    python machine_checks.py --dist DIR [--out DIR] [--hours 24] [--baseline FILE] [--write-baseline]
    python machine_checks.py --assets DIR ...     (build first from ../prototype/project)

Plays a new game in headless Chromium through the game's own test hook (window.LEDGER, the same contract the
clumsy newcomer uses), stepped by hand at 1/60 s, and checks:

  1. rules: every game hour of a long run (default a whole day), the clock only moves forward, money is whole
     pence and the pocket never below nothing, Tom and every person stand at real positions, and no person stays
     inside a solid outdoors (Tom is judged by never stuck instead), Tom is never killed (the game never ends by itself), no written scene or box
     that cannot be closed;
  2. save and reload: the saved week, loaded into a fresh page, gives back the same day, clock, money, debts and
     Tom's place, and plays on for two minutes without an error;
  3. never stuck: Tom sent to every named place in turn walks off again in at least one direction;
  4. camera never inside a wall: the line from Tom to the camera is clear at every named place;
  5. frame rate: the game's own benchmark (frame time, draw calls) and the cost of one logic step, against the
     last accepted build's numbers (baseline file), failing at half as slow again;
  6. the content rule in the build's own words: no drink, gambling or children words in any line of prose the
     game can show (a fixed word list; ambiguous words are warnings, never failures).

The game's code is never changed. Without the art folder the pictures are missing (404s are noted, not failed);
the rules, save, stuck, camera and content checks do not need them, and frame numbers are then marked "no art".
Exit code 1 if any check failed. A check that could not be made fails as "not reached", never passes.
"""
import argparse
import datetime
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import invariants as inv  # noqa: E402

BASELINE = os.path.join(HERE, "machine_baseline.json")
SLOWER_FAILS = 1.5          # half as slow again as the accepted build fails
TICK_BUDGET_MS = 8.0        # one logic step must cost under this in the cloud browser, whatever the baseline
DT = 1 / 60

# words that break the content rule if a line of prose shows them (canon.md: no alcohol or gambling shown or spoken
# of; no children anywhere). Matched as whole words, case-blind.
FAIL_WORDS = [
    "beer", "beers", "lager", "ale", "ales", "pint", "pints", "whisky", "whiskey", "wine", "vodka", "brandy", "rum",
    "gin", "cider", "drunk", "drunken", "booze", "boozer", "hangover", "pissed", "tipsy", "barman", "barmaid",
    "bookie", "bookies", "bookmaker", "betting", "casino", "poker", "lottery", "gamble", "gambling", "gambler",
    "fruit machine", "bingo", "roulette", "blackjack", "jackpot", "wager",
    "child", "children", "kid", "kids", "toddler", "baby", "babies", "schoolboy", "schoolgirl", "schoolkids",
    "pupil", "pupils", "teenager", "teenagers", "grandson", "granddaughter",
]
# words that are often fine ("I bet", "the pub" with no drink, "a lad" of thirty): reported, never failed
WARN_WORDS = ["bet", "bets", "odds", "pub", "pubs", "bar", "drink", "drinks", "drinking", "lad", "lads", "lass",
              "young'un", "school", "boy", "girl", "boys", "girls", "youngster", "mum", "dad",
              "son", "sons", "daughter", "daughters", "nephew", "niece"]  # grown sons and daughters are allowed
# prose strings that state the content rule itself, sent to the talk service, are not lines the game shows
RULE_TEXT = re.compile(r"CONTENT RULES|content rule|No alcohol|no children|BANNED|never mention", re.I)


def prose_strings(js_text):
    """Every string literal in the built script that reads like a line of prose: has a space and a letter word of
    three letters or more, at least 12 characters. Code identifiers and CSS are mostly left out by this."""
    out = []
    for m in re.finditer(r"'((?:[^'\\\n]|\\.){12,})'|\"((?:[^\"\\\n]|\\.){12,})\"|`((?:[^`\\]|\\.){12,})`", js_text):
        s = m.group(1) or m.group(2) or m.group(3) or ""
        if " " not in s or not re.search(r"[A-Za-z]{3,} [A-Za-z]{2,}", s):
            continue
        if re.search(r"[{};]\s*$|function\s*\(|=>|\bconst\b|\breturn\b|<\w+[ >]|\bvar\(|px\b", s) and not re.search(r"[.!?]['\"]?$", s):
            continue
        out.append(s)
    return out


def content_scan(js_text):
    strings = prose_strings(js_text)
    fails, warns = [], {}
    frx = re.compile(r"\b(" + "|".join(re.escape(w) for w in FAIL_WORDS) + r")\b", re.I)
    wrx = re.compile(r"\b(" + "|".join(re.escape(w) for w in WARN_WORDS) + r")\b", re.I)
    for s in strings:
        if RULE_TEXT.search(s):
            continue
        for m in frx.finditer(s):
            fails.append({"word": m.group(1).lower(), "line": s[:160]})
        for m in wrx.finditer(s):
            warns.setdefault(m.group(1).lower(), []).append(s[:120])
    return {"strings": len(strings), "fails": fails, "warns": {k: {"count": len(v), "first": v[:3]} for k, v in warns.items()}}


def rule_faults(r, last, people):
    """The rules at one moment. r: LEDGER.read(); last: the read an hour before (or None); people: positions."""
    f = []
    if last is not None:
        if (r["dayIndex"], r["gameMinute"]) < (last["dayIndex"], last["gameMinute"]):
            f.append("the clock went back: %s %s after %s %s" % (r["day"], r["clock"], last["day"], last["clock"]))
    for k, v in r["money"].items():
        if not isinstance(v, (int, float)) or not math.isfinite(v):
            f.append("money %s is not a number: %r" % (k, v))
        elif k.endswith("Pence") and abs(v - round(v)) > 1e-6:
            f.append("money %s is not whole pence: %r" % (k, v))
    if r["money"].get("pocketPence", 0) < 0:
        f.append("pocket below nothing: %s" % r["money"]["pocketPence"])
    t = r["tom"]
    if not all(isinstance(t[k], (int, float)) and math.isfinite(t[k]) for k in ("xMetres", "zMetres")):
        f.append("Tom has no real position: %r" % ({k: t[k] for k in ("xMetres", "zMetres")},))
    if r["phase"] not in ("play",) and not r.get("weekEnded"):
        f.append("the game left play by itself: phase %s" % r["phase"])
    for p in people:
        if p.get("bad"):
            f.append("%s: %s" % (p["id"], p["bad"]))
    return f


PEOPLE_JS = """() => { const L = LEDGER, G = L.G, out = [];
  for (const P of G.named.concat(G.crowd || [])) {
    const ok = Number.isFinite(P.x) && Number.isFinite(P.z);
    let bad = null;
    if (!ok) bad = 'no real position';
    else if (!P.space || P.space === 'street') { if (L.isBlocked(P.x, P.z) && !P.inCar && !P.hidden && !P.down) bad = 'inside a solid at ' + P.x.toFixed(1) + ', ' + P.z.toFixed(1); }
    out.push({ id: P.id || (P.def && P.def.name) || '?', bad }); }
  // Tom is left out: the checks put him at named places by hand (a door's point can sit in its wall); "never stuck"
  // judges Tom by walking him off again
  return out; }"""

RUN_HOUR_JS = """async ([secs, dt]) => { const L = LEDGER; let t = 0, scenes = 0, boxes = 0, stuck = 0, chunk = 0;
  while (t < secs - 1e-9) { L.tick(dt); t += dt; chunk += dt;
    if (chunk >= 1) { chunk = 0; let n = 0;
      while (n < 40) { const w = L.written.read();
        if (w.open) { scenes++; if (w.choices && w.choices.length) await L.written.choose(0); else await L.written.next(); }
        else if (L.ui.modal) { boxes++; L.press('Escape'); }
        else break; n++; L.tick(dt); }
      if (n >= 40) stuck++; } }
  return { scenes, boxes, stuck }; }"""

TICK_COST_JS = """() => { const L = LEDGER, n = 600, t0 = performance.now(); for (let i = 0; i < n; i++) L.tick(1 / 60);
  return (performance.now() - t0) / n; }"""


class Checks:
    def __init__(self, dist, out, hours, art, src=None):
        self.dist, self.out, self.hours, self.art, self.src = dist, out, hours, art, src
        self.results, self.notes = [], []

    def record(self, rule, _ok, steps, **kw):
        kw.pop("ok", None)
        r = {"rule": rule, "ok": bool(_ok), "steps": steps}
        r.update(kw)
        self.results.append(r)
        return r

    def proto(self):
        from clumsy import Proto
        g = Proto(self.dist)
        g.clear()
        return g

    def errors_of(self, g):
        e = g.errors
        if not self.art:
            e = [x for x in e if "404" not in x]
        return e

    # 1 and 3 and 4: the long run with the rules every hour, then never stuck and the camera at every place
    def long_run(self):
        g = self.proto()
        try:
            self._long_run(g)
        finally:
            g.close()

    def _long_run(self, g):
        last, faults, totals = None, [], {"scenes": 0, "boxes": 0, "stuck": 0}
        secs = g.js("() => LEDGER.rules.time.realSecondsPerGameHour")
        places = list(g.js("() => LEDGER.places").keys())
        for h in range(self.hours):
            r = g.state()
            f = rule_faults(r, last, self.people_held(g))
            for x in f:
                faults.append("hour %d (%s %s): %s" % (h, r["day"], r["clock"], x))
            last = r
            if places and h % 3 == 0:  # Tom moves about, so the rules are read in different places
                g.js("(p) => { LEDGER.goOutside(); LEDGER.goTo(p); }", places[(h // 3) % len(places)])
            res = g.js(RUN_HOUR_JS, [secs, DT])
            for k in totals:
                totals[k] += res[k]
            if r.get("weekEnded"):
                break
        r = g.state()
        for x in rule_faults(r, last, self.people_held(g)):
            faults.append("end (%s %s): %s" % (r["day"], r["clock"], x))
        self.record("rules hold every game hour", not faults, "new game; %d game hours at 1/60 s, Tom sent to a named place every third hour" % self.hours,
                    faults=faults[:30], fault_count=len(faults), hours_run=self.hours, scenes_closed=totals["scenes"], boxes_closed=totals["boxes"])
        self.record("no scene or box that cannot be closed", totals["stuck"] == 0, "during the long run, forty presses allowed each time", stuck_times=totals["stuck"])
        self.save_text = g.js("() => LEDGER.saveText()")
        self.saved_read = g.state()
        self.stuck_and_camera(g, places)
        errs = self.errors_of(g)
        self.record("no page errors (long run)", not errs, "whole long run", errors=errs[:20])

    @staticmethod
    def people_held(g, gap_s=1.5):
        """People inside a solid now and still inside gap_s later (a walker grazing a corner for a frame is not a
        fault; one walking through a wall is)."""
        first = {p["id"]: p for p in g.js(PEOPLE_JS) if p["bad"]}
        if not first:
            return []
        g.run(gap_s, every=gap_s)
        return [p for p in g.js(PEOPLE_JS) if p["bad"] and p["id"] in first]

    def stuck_and_camera(self, g, places):
        from clumsy import Gate
        gate = Gate(g, self.out)
        n_stuck = n_cam = 0
        for p in places:
            g.js("(p) => { LEDGER.goOutside(); LEDGER.goTo(p); }", p)
            g.clear()
            track = gate.escape_track(["KeyW", "KeyS", "KeyA", "KeyD"], secs_each=1.5)
            v = inv.moved_again(track)
            self.record("never stuck (every named place)", v["ok"], "goTo %s; W, S, A, D in turn" % p, place=p, **v)
            n_stuck += 1
            g.js("(p) => { LEDGER.goOutside(); LEDGER.goTo(p); }", p)
            c = gate.check_camera("goTo %s" % p, p)
            self.results.append(dict(c, rule="camera never inside a wall (every named place)"))
            n_cam += 1
        if not n_stuck:
            self.record("never stuck (every named place)", False, "not reached: the game gave no named places")
        if not n_cam:
            self.record("camera never inside a wall (every named place)", False, "not reached")

    # 2: save and reload
    def save_reload(self):
        if not getattr(self, "save_text", None):
            self.record("save and reload give back the same week", False, "not reached: no saved week from the long run")
            return
        g = self.proto()
        try:
            self._save_reload(g)
        finally:
            g.close()

    def _save_reload(self, g):
        g.js("(t) => LEDGER.restore(t)", self.save_text)
        g.run(0.5)
        g.clear()
        a, b = self.saved_read, g.state()
        diffs = []
        for k in ("dayIndex", "day"):
            if a[k] != b[k]:
                diffs.append("%s %r became %r" % (k, a[k], b[k]))
        if abs(a["gameMinute"] - b["gameMinute"]) > 2:
            diffs.append("clock %s became %s" % (a["clock"], b["clock"]))
        for k in ("pocketPence", "tinPence", "faresTakenPence", "earnedCleanPence", "earnedDirtyPence", "spentPence"):
            if a["money"].get(k) != b["money"].get(k):
                diffs.append("money %s %r became %r" % (k, a["money"].get(k), b["money"].get(k)))
        if json.dumps(a["debts"], sort_keys=True) != json.dumps(b["debts"], sort_keys=True):
            diffs.append("the debts changed")
        for k in ("carrying", "hasTheCoat", "weapon", "indoorsRoomId"):
            if a["tom"].get(k) != b["tom"].get(k):
                diffs.append("Tom's %s %r became %r" % (k, a["tom"].get(k), b["tom"].get(k)))
        if math.hypot(a["tom"]["xMetres"] - b["tom"]["xMetres"], a["tom"]["zMetres"] - b["tom"]["zMetres"]) > 3:
            diffs.append("Tom moved %.1f m on loading" % math.hypot(a["tom"]["xMetres"] - b["tom"]["xMetres"], a["tom"]["zMetres"] - b["tom"]["zMetres"]))
        self.record("save and reload give back the same week", not diffs, "saveText after the long run; restore in a fresh page", diffs=diffs)
        g.js(RUN_HOUR_JS, [120, DT])
        errs = self.errors_of(g)
        self.record("plays on after reload", not errs and g.state()["phase"] == "play", "two minutes after the reload", errors=errs[:10])

    # 5: frame rate
    def frame_rate(self, baseline):
        g = self.proto()
        tick_ms = g.js(TICK_COST_JS)
        try:
            g.js("window.LEDGER_NORENDER = false; window.LEDGER_MANUAL = false")
            g.pg.wait_for_timeout(2000)
            bm = g.js("() => LEDGER.benchmark()")
        except Exception as e:
            bm = {"error": str(e)[:200]}
        finally:
            g.close()
        rec = {"tick_ms": round(tick_ms, 3), "frame_ms": bm.get("ms"), "draw_calls": bm.get("calls"), "triangles": bm.get("tris"),
               "size": "%sx%s" % (bm.get("w"), bm.get("h")), "art": self.art}
        self.numbers = rec
        base = baseline or {}
        f = []
        if tick_ms > TICK_BUDGET_MS:
            f.append("one logic step costs %.2f ms, over %.1f" % (tick_ms, TICK_BUDGET_MS))
        if base.get("tick_ms") and tick_ms > base["tick_ms"] * SLOWER_FAILS:
            f.append("logic step %.2f ms against %.2f accepted" % (tick_ms, base["tick_ms"]))
        same_kind = base.get("art") == self.art
        if same_kind and base.get("frame_ms") and rec["frame_ms"] and rec["frame_ms"] > base["frame_ms"] * SLOWER_FAILS:
            f.append("frame %.1f ms against %.1f accepted (cloud software drawing; his PC's number is the real one)" % (rec["frame_ms"], base["frame_ms"]))
        if same_kind and base.get("draw_calls") and rec["draw_calls"] and rec["draw_calls"] > base["draw_calls"] * SLOWER_FAILS:
            f.append("draw calls %d against %d accepted" % (rec["draw_calls"], base["draw_calls"]))
        if rec["frame_ms"] is None:
            f.append("not reached: the game's benchmark gave no frame time (%s)" % bm.get("error", "no ms"))
        self.record("frame rate holds against the accepted build", not f, "600 logic steps timed; the game's own benchmark with drawing on",
                    faults=f, numbers=rec, baseline=base or "none yet (this run's numbers can be written as the baseline)")

    # 6: the content rule in the game's words: its own source files (the built ledger.js also holds three.js,
    # whose code words, such as children, are not lines anyone sees)
    def content(self):
        files = []
        if self.src and os.path.isdir(self.src):
            for root, _, names in os.walk(self.src):
                files += [os.path.join(root, n) for n in sorted(names) if n.endswith((".js", ".mjs", ".html", ".json", ".txt"))]
        where = "the game's source (%d files in %s)" % (len(files), self.src)
        if not files:
            js = os.path.join(self.dist, "ledger.js")
            files = [js] if os.path.exists(js) else []
            where = "the built ledger.js (no source folder given: three.js code words may show as faults)"
        if not files:
            self.record("content rule in the game's words", False, "not reached: no source and no ledger.js")
            return
        s = content_scan("\n".join(open(p, encoding="utf-8", errors="replace").read() for p in files))
        self.record("content rule in the game's words", not s["fails"] and s["strings"] > 100,
                    "every prose string in %s against the word list (%d strings)" % (where, s["strings"]),
                    fails=s["fails"][:40], fail_count=len(s["fails"]), warnings=s["warns"])


def summarise(results):
    out = {}
    for r in results:
        o = out.setdefault(r["rule"], {"checked": 0, "failed": 0})
        o["checked"] += 1
        o["failed"] += 0 if r["ok"] else 1
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets")
    ap.add_argument("--dist")
    ap.add_argument("--out", default=os.path.join(os.path.expanduser("~"), ".cache", "ledger-machine",
                                                   datetime.datetime.now().strftime("%Y%m%d-%H%M")))
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--baseline", default=BASELINE)
    ap.add_argument("--write-baseline", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--src", default=os.path.join(os.path.dirname(HERE), "prototype", "project", "src"),
                    help="the game's own source folder, for the content scan")
    a = ap.parse_args(argv)
    if not a.dist:
        from clumsy import build_dist
        a.dist = build_dist(a.assets)
    art = os.path.exists(os.path.join(a.dist, "people.jpg"))
    os.makedirs(a.out, exist_ok=True)
    baseline = json.load(open(a.baseline)) if os.path.exists(a.baseline) else None
    c = Checks(a.dist, a.out, a.hours, art, a.src)
    if not art:
        c.notes.append("run without the art folder: missing pictures (404) are not counted as page errors; frame numbers marked no art")
    order = ["content", "frame_rate", "long_run", "save_reload"]
    only = [x for x in a.only.split(",") if x] or order
    for name in order:
        if name not in only:
            continue
        try:
            getattr(c, name)(baseline) if name == "frame_rate" else getattr(c, name)()
        except Exception as e:  # a check that breaks is itself a finding
            c.record("check ran: " + name, False, name, error=str(e)[:400])
        print("done", name, flush=True)
    if a.write_baseline and getattr(c, "numbers", None):
        json.dump(dict(c.numbers, written=datetime.datetime.now().isoformat(timespec="minutes")), open(a.baseline, "w"), indent=1)
        c.notes.append("baseline written: " + a.baseline)
    summary = summarise(c.results)
    report = {"when": datetime.datetime.now().isoformat(timespec="seconds"), "dist": a.dist, "art": art,
              "summary": summary, "results": c.results, "notes": c.notes, "numbers": getattr(c, "numbers", None)}
    with open(os.path.join(a.out, "machine.json"), "w") as f:
        json.dump(report, f, indent=1)
    failed = sum(v["failed"] for v in summary.values())
    for k, v in summary.items():
        print("%-52s %3d checked %3d failed" % (k, v["checked"], v["failed"]))
    print("report:", os.path.join(a.out, "machine.json"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
