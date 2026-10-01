#!/usr/bin/env python3
"""THE ROUTE, WALKED WITH REAL KEY PRESSES (item 5, 1 October; production/research/
packaged-game-testing, step 2: "the audit's missing layer").

    python tools/route_walk.py [--editor] [--out DIR]
    python tools/route_walk.py --selftest

A fixed script, no model: the AI tester's own key, mouse and typing commands
(tools/ai-tester/play.py, which refuses to start while the PC was used in the
last two minutes) drive the finished game the way a player would, and the
game's own check lines (LEDGER-ROUTE, in route-checks.jsonl beside its
files) say whether each stage happened. It steers by the place the game
reports under -RouteWalk (route-where.txt: Tom, Rita's window and the three
who talk), walking short legs and correcting, never moving him by code.

The stages, each with its own time limit and the tester's picture:
  street        New game chosen on the title; play begins
  talk-open     T beside Sheila opens the talk box
  talk-typed    a line with w, a, s and d typed and sent: Tom has not moved
  reply-words   her answer's words come (the stand-in talk)
  deed          E at Rita's window breaks it
  onlookers     who was there to see is measured
  wait          Z waits and the town's hours run
  save          the game saves itself (on the hour, after talk)
  quit          Esc, then Q: the game closes
  street        relaunched, Continue chosen
  continue      Tom stands where he saved (within half a metre)

Writes verdict.json (pass or fail per stage, in order) under --out (default
production/playtest/route-walk/<stamp>) and prints one line a stage. Exits 0
when every stage passed. Talk uses the stand-in (-TalkFake), never LEDGER's
key: no automated tool may.
"""
import json
import math
import os
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAY = [sys.executable, os.path.join(REPO, "tools", "ai-tester", "play.py")]
PACKAGED_SAVED = "F:/LedgerTools/played-game/Windows/LedgerProbe/Saved"
EDITOR_SAVED = os.path.join(REPO, "ue-probe", "Saved")
LINE = "Was it always this quiet and dead round here, Sheila?"   # w, a, s and d, typed into the box
WALK_MPS = 1.6                                                  # measured 1 October: 3.2 m in 2 s
ROAD_Z = 1.2                                                    # the road's middle, clear of the cars at the kerb


def play(*args):
    r = subprocess.run(PLAY + [str(a) for a in args], capture_output=True, text=True, cwd=REPO)
    out = (r.stdout or "").strip().splitlines()
    return out[-1] if out else ""


def parse_where(text):
    """route-where.txt: "tom x z heading clock|window x z reach|lena x z talk|..."."""
    got = {}
    for part in text.strip().split("|"):
        f = part.split()
        if len(f) >= 3:
            try:
                got[f[0]] = [float(f[1]), float(f[2])] + [float(x) for x in f[3:4]] + f[4:]
            except ValueError:
                continue
    return got


def wrap(deg):
    return (deg + 180.0) % 360.0 - 180.0


def bearing(x0, z0, x1, z1):
    return math.degrees(math.atan2(z1 - z0, x1 - x0))


def stand_off(target, frm, m):
    """The point m metres from target toward frm."""
    d = math.hypot(frm[0] - target[0], frm[1] - target[1]) or 1.0
    return [target[0] + (frm[0] - target[0]) * m / d, target[1] + (frm[1] - target[1]) * m / d]


class Route:
    def __init__(self, saved, out):
        self.saved, self.out = saved, out
        self.rows, self.seen, self.pending, self.trace = [], 0, [], []

    def where(self):
        try:
            with open(os.path.join(self.saved, "route-where.txt"), encoding="utf-8") as fh:
                return parse_where(fh.read())
        except OSError:
            return {}

    def checks(self):
        try:
            with open(os.path.join(self.saved, "route-checks.jsonl"), encoding="utf-8") as fh:
                lines = [json.loads(l) for l in fh if l.strip()]
        except (OSError, ValueError):
            return []
        new, self.seen = lines[self.seen:], len(lines)
        return new

    def wait_stage(self, stage, seconds):
        """The first line of this stage not yet taken; lines of other stages
        read on the way stay for their own wait."""
        until = time.time() + seconds
        while True:
            self.pending += self.checks()
            for i, c in enumerate(self.pending):
                if c.get("stage") == stage:
                    del self.pending[i]
                    return c
            if time.time() >= until:
                return None
            time.sleep(0.5)

    def discard(self, stage):
        """Drop lines of this stage already read: the next one is the one an action brings."""
        self.pending += self.checks()
        self.pending = [c for c in self.pending if c.get("stage") != stage]

    def record(self, stage, ok, detail):
        self.rows.append({"stage": stage, "ok": bool(ok), "detail": detail})
        print("route %-12s %s  %s" % (stage, "PASS" if ok else "FAIL", detail), flush=True)
        return ok

    def expect(self, stage, seconds, need_ok=True):
        c = self.wait_stage(stage, seconds)
        if c is None:
            return self.record(stage, False, "no %s line within %d s" % (stage, seconds))
        return self.record(stage, c.get("ok") or not need_ok, c.get("detail", ""))

    def turn_to(self, heading):
        for _ in range(5):
            w = self.where().get("tom")
            if not w:
                return False
            delta = wrap(heading - w[2])
            if abs(delta) < 5.0:
                return True
            play("turn", "%.0f" % max(-170.0, min(170.0, delta * 0.9)))
            time.sleep(0.3)
        return False

    def go_to(self, x, z, tol=0.4, legs=14, follow=None):
        """Short legs toward (x, z), turning between them; a leg that gets
        nowhere is a blockage, side-stepped once each way. follow(where)
        gives a moving target instead, read again before every leg (people
        move with their day while he walks)."""
        for _ in range(legs):
            whole = self.where()
            w = whole.get("tom")
            if not w:
                return False
            if follow is not None:
                aim = follow(whole)
                if aim is None:
                    return False
                x, z = aim
            d = math.hypot(x - w[0], z - w[1])
            self.trace.append({"to": [round(x, 2), round(z, 2)], "at": [round(w[0], 2), round(w[1], 2)], "clock": " ".join(w[3:])})
            if d <= tol:
                return True
            self.turn_to(bearing(w[0], w[1], x, z))
            play("walk", "forward", "%.2f" % max(0.25, min(2.0, d / WALK_MPS)))
            time.sleep(0.3)
            w2 = self.where().get("tom")
            if w2 and math.hypot(w2[0] - w[0], w2[1] - w[1]) < 0.15:
                play("walk", "right" if _ % 2 == 0 else "left", "0.6")
        w = self.where().get("tom")
        return bool(w) and math.hypot(x - w[0], z - w[1]) <= tol

    def by_road(self, x, z, tol=0.4):
        """Out to the road's middle, along it, and in: the pavement is walled
        off in places by parked cars and the fish market's crate."""
        w = self.where().get("tom")
        if w and abs(w[1]) > 2.0 and abs(w[0] - x) > 2.5:
            self.go_to(w[0], ROAD_Z)
            self.go_to(x, ROAD_Z)
        return self.go_to(x, z, tol)

    def write(self):
        os.makedirs(self.out, exist_ok=True)
        verdict = {"passed": sum(r["ok"] for r in self.rows), "stages": len(self.rows), "rows": self.rows, "path": self.trace}
        with open(os.path.join(self.out, "verdict.json"), "w", encoding="utf-8") as fh:
            json.dump(verdict, fh, indent=1)
        return verdict


def start(editor, save_dir):
    args = ["start", "--save", save_dir, "--wait", "5", "--game-arg", "-RouteWalk"]
    if editor:
        args.insert(1, "--editor")
    for _ in range(30):
        r = play(*args)
        if "did=started" in r:
            return True
        if "BUSY" in r or "REFUSED" in r:
            print("route start: " + r)
            return False
        time.sleep(60)          # the PC was in use: the tester waits for two idle minutes
    return False


def walk(editor, out):
    saved = EDITOR_SAVED if editor else PACKAGED_SAVED
    stamp = time.strftime("%Y-%m-%d-%H%M")
    save_dir = "F:/LedgerTools/tmp/route-walk/" + stamp
    for name in ("route-checks.jsonl", "route-where.txt"):
        try:
            os.remove(os.path.join(saved, name))
        except OSError:
            pass
    r = Route(saved, out)
    play("close")
    if not start(editor, save_dir):
        r.record("street", False, "the game did not start")
        return r.write()
    play("press", "Enter")                                          # New game
    if not r.expect("street", 60):
        play("close")
        return r.write()
    for _ in range(5):                                              # Sheila's walk round, line by line
        play("press", "Enter")
        play("wait", "4")
    # TALK: to Sheila, wherever her day has her.
    w = r.where()
    if "lena" in w and "tom" in w:
        spot = stand_off(w["lena"][:2], w["tom"][:2], 1.1)
        r.by_road(spot[0], spot[1])
        # Wherever she has gone meanwhile.
        r.go_to(0, 0, tol=0.5, legs=10,
                follow=lambda ww: stand_off(ww["lena"][:2], ww["tom"][:2], 1.1) if "lena" in ww and "tom" in ww else None)
        w = r.where()
        t = w.get("tom")
        if t and "lena" in w:
            r.turn_to(bearing(t[0], t[1], w["lena"][0], w["lena"][1]))
    # ONLY IN REACH: a line typed with no box open goes to the game as keys.
    w = r.where()
    near = "lena" in w and "tom" in w and math.hypot(w["lena"][0] - w["tom"][0], w["lena"][1] - w["tom"][1]) <= w["lena"][2]
    if near:
        play("say", LINE)
        r.expect("talk-open", 10)
        r.expect("talk-typed", 10)
        r.expect("reply-words", 30)
    else:
        r.record("talk-open", False, "never in reach of Sheila (%s)" % (
            "she is not on the street" if "lena" not in w else "%.1f m away" % math.hypot(w["lena"][0] - w["tom"][0], w["lena"][1] - w["tom"][1])))
    play("wait", "8")
    # THE DEED: by the road to Rita's window, then up to it, facing it.
    w = r.where()
    if "window" in w and "tom" in w:
        wx, wz, reach = w["window"][0], w["window"][1], w["window"][2]
        r.by_road(wx, wz - min(1.0, reach * 0.6), tol=0.3)
        t = r.where().get("tom")
        if t:
            r.turn_to(bearing(t[0], t[1], wx, wz))
    w = r.where()
    if "window" in w and "tom" in w and math.hypot(w["window"][0] - w["tom"][0], w["window"][1] - w["tom"][1]) <= w["window"][2]:
        play("press", "E")
        r.expect("deed", 15)
        r.expect("onlookers", 15)
    else:
        r.record("deed", False, "never in reach of Rita's window")
    play("wait", "10")
    # THE WAIT, and the save it brings.
    r.discard("wait")
    r.discard("save")
    play("press", "Z")
    r.expect("wait", 60)
    r.expect("save", 30)
    saved_at = r.rows[-1]["detail"] if r.rows and r.rows[-1]["stage"] == "save" else ""
    # QUIT from the pause, then back in with Continue.
    play("press", "Esc")
    play("wait", "1")
    play("press", "Q")
    gone = False
    for _ in range(60):
        if "LedgerProbe.exe" not in subprocess.run(["tasklist"], capture_output=True, text=True).stdout and \
           "UnrealEditor.exe" not in subprocess.run(["tasklist"], capture_output=True, text=True).stdout:
            gone = True
            break
        time.sleep(1)
    r.record("quit", gone, "the game closed from the pause" if gone else "still running a minute after Q")
    play("close")
    time.sleep(5)
    r.seen, r.pending = 0, []
    for name in ("route-checks.jsonl",):
        try:
            os.remove(os.path.join(saved, name))
        except OSError:
            pass
    if not start(editor, save_dir):
        r.record("street", False, "the game did not start again")
        return r.write()
    play("press", "Enter")                                          # Continue
    c = r.wait_stage("street", 60)
    r.record("street", bool(c) and "continue" in c.get("detail", ""), (c or {}).get("detail", "no street line") + " (saved " + saved_at + ")")
    r.expect("continue", 30)
    play("close")
    return r.write()


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("route_walk selftest FAIL " + name)
    w = parse_where("tom 1.000 4.000 -14.3 D0 09:32|window 18.200 5.100 1.50|lena 6.000 4.600 2.50")
    check("Tom, his heading and the clock read", w["tom"][:3] == [1.0, 4.0, -14.3] and w["tom"][3:] == ["D0", "09:32"])
    check("the window and its reach read", w["window"] == [18.2, 5.1, 1.5])
    check("a bearing up the street is 0, across toward the shops 90", abs(bearing(0, 0, 5, 0)) < 1e-9 and abs(bearing(0, 0, 0, 5) - 90) < 1e-9)
    check("headings wrap", wrap(350) == -10 and wrap(-190) == 170)
    s = stand_off([6.0, 4.6], [1.0, 4.6], 1.1)
    check("a talk spot stands off toward Tom", abs(s[0] - 4.9) < 1e-9 and abs(s[1] - 4.6) < 1e-9)
    print("route_walk selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    editor = "--editor" in sys.argv
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(
        REPO, "production", "playtest", "route-walk", time.strftime("%Y-%m-%d-%H%M"))
    v = walk(editor, out)
    print("route walk: %d of %d stages passed; %s" % (v["passed"], v["stages"], out))
    sys.exit(0 if v["passed"] == v["stages"] and v["stages"] > 0 else 1)
