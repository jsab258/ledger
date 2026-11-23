#!/usr/bin/env python3
"""Machine checks, mended after round 1 of the checkers' proof (23 Nov 2026). Run beside tools/lane/gate/machine_checks.py
(which is left as it is); each check here answers a miss or a false alarm of round 1. Code only, no model; the game's
code is never changed. A check that could not be made fails as "not reached", never passes.

    python machine_plus.py --dist DIR --out DIR [--ref-dist DIR] [--hours 24]

  content in the built game   the content words in the lines of prose of the built ledger.js itself, so the scan always
                              reads exactly what was built; round 1's scan
                              refused the current build ("source does not match") and never ran.
  nobody under 18             every person's age as the game keeps it (P.def.age): round 1 read a field the game
                              does not use, so a passer-by of fifteen passed.
  the street is peopled       every game hour of a day, the crowd on the street against the game's own table for that
                              hour (at least half of it, and at least one after dark): round 1 never counted people.
  every fare pays             six fares in a row through the game's own fare calls: each pays and the fare book grows.
  every talk can be left      each named person on the street: talk opened with E, then Escape; the box must close.
  the pause menu by keys      Escape opens it, the arrow keys move between its buttons, Escape closes it.
  frame rate against a twin   one logic step's cost against a reference build measured in the same run on the same
                              machine (--ref-dist), not a number written on another day.
"""
import argparse, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(os.path.dirname(HERE), "gate")
sys.path.insert(0, GATE)
from machine_checks import content_scan, prose_strings, TICK_COST_JS  # noqa: E402

DT = 1 / 60


def built_prose(js):
    """Lines of prose in the built ledger.js (minified, three.js inside): prose_strings, then only strings that read as
    words (no code marks, four fifths letters and spaces). Round 1's scan read the source and refused the build."""
    out = []
    for s in prose_strings(js):
        if re.search(r"[={}<>;\\]|\bthis\.|\(\)|=>|\bvoid\b|\bnew [A-Z]", s):
            continue
        if sum(c.isalpha() or c == " " for c in s) < 0.8 * len(s):
            continue
        out.append(s)
    return out


AGES_JS = """() => { const G = LEDGER.G, out = [];
  for (const P of G.named.concat(G.crowd || [])) {
    const a = [P.age, P.def && P.def.age, P.def && P.def.ageYears].find((x) => typeof x === 'number');
    if (typeof a === 'number' && a < 18) out.push((P.id || '?') + ' is ' + a);
    if (typeof a !== 'number') out.push((P.id || '?') + ' has no age');
  }
  return { people: G.named.length + (G.crowd || []).length, bad: out }; }"""

CROWD_JS = """() => { const L = LEDGER, G = L.G, C = L.rules.crowd, h = (G.t / 60) % 24;
  const want = h < C.smallHoursUntilHour ? 1 : h < C.dawnUntilHour ? C.walkersAtDawn : h < C.earlyUntilHour ? C.walkersEarly
    : h < C.dayUntilHour ? C.walkersByDay : h < C.eveningUntilHour ? C.walkersInTheEvening : h < C.lateUntilHour ? C.walkersLate : 2;
  const out = (G.crowd || []).filter((P) => !P.keeper && !P.gone && (!P.space || P.space === 'street')).length;
  return { hour: Math.floor(h), want, out }; }"""


class Run:
    def __init__(self, dist, out):
        self.dist, self.out, self.results = dist, out, []

    def record(self, rule, ok, steps, **kw):
        self.results.append(dict(rule=rule, ok=ok, steps=steps, **kw))
        print("%-5s %s %s" % ({True: "ok", False: "FAIL", None: "???"}[ok], rule, json.dumps(kw)[:300] if not ok else ""), flush=True)

    def proto(self, dist=None):
        from clumsy import Proto
        g = Proto(dist or self.dist)
        g.clear()
        return g

    def content(self):
        js = os.path.join(self.dist, "ledger.js")
        if not os.path.exists(js):
            return self.record("content in the built game", False, "not reached: no ledger.js")
        lines = built_prose(open(js, encoding="utf-8", errors="replace").read())
        s = content_scan("\n".join(repr(x) for x in lines))
        ok = s["strings"] > 300 and not s["fails"]
        self.record("content in the built game", ok if s["strings"] > 300 else False,
                    "lines of prose in the built ledger.js: %d" % s["strings"],
                    fails=[(x["word"], x["line"][:100]) for x in s["fails"]][:12])

    def ages_and_crowd(self, hours):
        g = self.proto()
        try:
            a = g.js(AGES_JS)
            self.record("nobody under 18", a["people"] > 10 and not a["bad"], "every person the game holds, by the age it keeps",
                        people=a["people"], bad=a["bad"][:10])
            secs = g.js("() => LEDGER.rules.time.realSecondsPerGameHour")
            thin = []
            seen = 0
            for _ in range(hours):
                c = g.js(CROWD_JS)
                seen += 1
                if c["out"] < max(1, c["want"] // 2):
                    thin.append("%02d:00 %d out, the table says %d" % (c["hour"], c["out"], c["want"]))
                g.clear(10)
                g.run(secs, every=secs)
            self.record("the street is peopled", seen >= min(hours, 20) and not thin,
                        "%d game hours of a new game, the crowd counted each hour" % seen, thin=thin[:12])
        finally:
            g.close()

    def fares(self, n=6):
        g = self.proto()
        bad, paid = [], []
        try:
            g.js("() => { LEDGER.G.car.keys = true; return LEDGER.cab.getIn(); }")  # test setup: the keys given, Tom put in the cab
            for i in range(n):
                f = g.js("() => LEDGER.fare.call()")
                if not f:
                    bad.append("fare %d: no fare was offered" % (i + 1)); break
                g.js("() => LEDGER.fare.accept()")
                g.js("() => LEDGER.fare.pickUp()")
                g.run(3)
                r = g.js("async () => await LEDGER.fare.dropOff()")
                g.clear(20)
                p = (r or {}).get("paidPence", 0)
                paid.append(p)
                if not (r or {}).get("settled"):
                    bad.append("fare %d not settled" % (i + 1))
                elif p <= 0:
                    bad.append("fare %d paid nothing" % (i + 1))
                g.run(2)
            st = g.state()
            ok = not bad and len(paid) == n
            self.record("every fare pays", ok, "test setup: the cab keys given and Tom put in the cab; %d fares in a row through the game's own fare calls" % n, paid=paid, bad=bad,
                        fare_count=st.get("money", {}).get("faresCount"))
        except Exception as e:
            self.record("every fare pays", False, "not reached: " + str(e)[:200])
        finally:
            g.close()

    def talks(self):
        g = self.proto()
        try:
            ids = g.js("() => LEDGER.G.named.filter((P) => !P.gone && !P.dead && (!P.space || P.space === 'street' || (P.atWindow && P.win))).map((P) => P.id)")
            stuck, opened = [], []
            for pid in ids:
                g.clear(10)
                got = g.js("""(id) => { const L = LEDGER, G = L.G, P = G.people[id], t = G.tom;
                  if (t.space !== 'street') L.goOutside();
                  const at = P.atWindow && P.win ? [P.win.x + Math.sin(P.win.ang) * 1.2, P.win.z + Math.cos(P.win.ang) * 1.2, P.win.x, P.win.z] : [P.x + 0.9, P.z, P.x, P.z];
                  t.x = at[0]; t.z = at[1]; t.ang = Math.atan2(at[2] - t.x, at[3] - t.z); return at; }""", pid)
                g.run(0.3)
                g.tap("KeyE")
                g.run(1.2)
                m = g.js("() => LEDGER.ui.modal")
                if m not in ("talk", "dialog"):
                    continue
                opened.append(pid)
                for _ in range(3):
                    if g.js("() => LEDGER.ui.modal") not in ("talk",):
                        break
                    g.tap("Escape")
                    g.run(0.8)
                if g.js("() => LEDGER.ui.modal") == "talk":
                    stuck.append(pid)
            self.record("every talk can be left", bool(opened) and not stuck,
                        "each named person on the street or at a window (Tom put beside them): E, then Escape up to three times", opened=opened, stuck=stuck)
        finally:
            g.close()

    def pause(self):
        g = self.proto()
        try:
            g.tap("Escape"); g.run(0.4)
            m1 = g.js("() => LEDGER.ui.modal")
            f0 = g.js("() => document.activeElement && document.activeElement.textContent")
            g.tap("ArrowDown"); g.run(0.2)
            f1 = g.js("() => document.activeElement && document.activeElement.textContent")
            g.tap("Escape"); g.run(0.4)
            m2 = g.js("() => LEDGER.ui.modal")
            ok = m1 == "pause" and not m2 and f0 != f1
            self.record("the pause menu by keys", ok, "Escape, ArrowDown, Escape", opened=m1, focus=[f0, f1], after=m2)
        finally:
            g.close()

    def frame_twin(self, ref):
        if not ref:
            return self.record("frame rate against a twin", None, "no reference build given (--ref-dist)")
        nums = {}
        for name, d in (("ref", ref), ("this", self.dist), ("ref2", ref)):
            g = self.proto(d)
            try:
                nums[name] = g.js(TICK_COST_JS)
            finally:
                g.close()
        base = min(nums["ref"], nums["ref2"])
        ok = nums["this"] <= base * 1.5 + 0.05
        self.record("frame rate against a twin", ok, "one logic step, this build between two runs of the reference build",
                    tick_ms={k: round(v, 3) for k, v in nums.items()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ref-dist")
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    r = Run(a.dist, a.out)
    only = [x for x in a.only.split(",") if x]
    steps = [("content", r.content), ("crowd", lambda: r.ages_and_crowd(a.hours)), ("fares", r.fares),
             ("talks", r.talks), ("pause", r.pause), ("frame", lambda: r.frame_twin(a.ref_dist))]
    for name, fn in steps:
        if only and name not in only:
            continue
        try:
            fn()
        except Exception as e:
            r.record(name, False, "not reached: the check broke: " + str(e)[:300])
    json.dump({"when": time.strftime("%Y-%m-%dT%H:%M"), "dist": a.dist, "results": r.results},
              open(os.path.join(a.out, "machine_plus.json"), "w"), indent=1)
    return 0 if all(x["ok"] for x in r.results if x["ok"] is not None) else 1


if __name__ == "__main__":
    sys.exit(main())
