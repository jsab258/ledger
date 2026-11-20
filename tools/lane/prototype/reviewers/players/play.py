"""Let an AI player type actually play a build of the LEDGER prototype (lane task 4t, piece 2).

The player sees only what a person sees (a screenshot and the words on screen) and acts only with keys. The game is
stepped by hand: it stands still while the player thinks, and moves on only by the time each action takes, so a slow
model plays at a person's pace in game time. Reading is charged too: every new word on screen costs the time a
person takes to read it (250 words a minute), so long talk moves the minute as it would for a person. The session
stops itself at --minutes. Every action is logged with the game's own state beside it in the --hidden folder, kept
apart from the screenshots (the player is never given that folder; the consequence checker and the panel read it).
The game's own saved week goes there too: at the start, every 10 actions and at the stop (consequences.py reads them).

    python play.py serve --dist DIR --out DIR --hidden DIR [--minutes 60] [--port 8765] [--seed 7]   (leave it running)
    python play.py look                                                   (the screen now)
    python play.py hold KeyW 3          hold keys for game seconds; several keys joined by +, e.g. KeyW+ShiftLeft
    python play.py tap KeyE             one press, then a third of a second
    python play.py type "Hello there"   type words (into a talk box when one is open), then Enter
    python play.py turn 90              turn the view by degrees (stands in for the mouse; minus is left)
    python play.py wait 20              let game seconds pass with no keys (at most 60 at a time)
    python play.py stop                 end the session; writes session.json

Each answer is one JSON line: minute played, the words on screen, the screenshot's file. Keys are the browser's key
codes (KeyW, KeyA, KeyS, KeyD, KeyE, KeyF, KeyQ, KeyZ, Space, ShiftLeft, Tab, Escape, Enter, Digit1 to Digit9).
Test tools only: the game's code is never changed.
"""
import argparse
import json
import math
import os
import sys
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "gate"))
sys.path.insert(0, GATE)
DT = 1 / 60
MAX_HOLD_S = 10
MAX_WAIT_S = 60
READ_WORDS_PER_S = 250 / 60

STATE_JS = "() => LEDGER.read()"
# what other people say on screen now, in full (for the consequence checker; never shown to the player): their lines
# in a talk (not Tom's own, not the hints), the written scene's line, subtitles and speech bubbles within earshot
SPOKEN_JS = """() => { const out = [], vis = (e) => e && e.offsetParent !== null;
  if (vis(document.getElementById('talk'))) for (const p of document.querySelectorAll('#tlog p.npc')) out.push(p.textContent.trim());
  const d = document.getElementById('dtxt'); if (vis(d)) out.push(d.textContent.trim());
  if (window.__gate) { const m = window.__gate.msgs(); out.push(...m.subs, ...m.bubbles); }
  return out.filter(Boolean); }"""


class Session:
    def __init__(self, dist, out, seed, hidden, minutes):
        from clumsy import Proto
        self.g = Proto(dist, seed=seed)
        self.out = out
        os.makedirs(os.path.join(out, "shots"), exist_ok=True)
        self.played_s = 0.0   # game time the actions took plus reading time
        self.keys_s = 0.0     # game time the actions took
        self.read_s = 0.0
        self.cap_s = minutes * 60
        self.seen = set()
        self.n = 0
        os.makedirs(hidden, exist_ok=True)
        if os.path.exists(os.path.join(hidden, "actions.jsonl")):
            raise SystemExit("--hidden already holds a session: give each session its own folder (replays need one log each)")
        self.log = open(os.path.join(hidden, "actions.jsonl"), "w")
        self.log.write(json.dumps({"n": 0, "seed": seed}) + "\n")
        self.hidden = hidden
        self.started = time.time()

    def save_to(self, name):
        """The game's own saved week, for the consequence checker (kept in the hidden folder only)."""
        try:
            with open(os.path.join(self.hidden, name), "w") as f:
                f.write(self.g.js("() => LEDGER.saveText()"))
        except Exception as e:  # noqa: BLE001 - a save that cannot be taken is named, never fatal to the session
            self.g.errors.append("save for the consequence checker failed: %s" % str(e)[:200])
            with open(os.path.join(self.hidden, "save_errors.txt"), "a") as f:
                f.write("%s: %s\n" % (name, str(e)[:300]))

    def step(self, secs, keys=()):
        g = self.g
        for k in keys:
            g.down(k)
        g.run(secs, every=max(secs, 0.1))
        for k in keys:
            g.up(k)
        self.played_s += secs
        self.keys_s += secs

    def screen(self, action):
        self.n += 1
        shot = os.path.join(self.out, "shots", "%04d.png" % self.n)
        shot = self.g.shot(shot)
        words = {k: v for k, v in self.g.words().items() if v}
        new = 0
        for line in "\n".join(words.values()).split("\n"):
            line = line.strip()
            if line and line not in self.seen:
                self.seen.add(line)
                new += len(line.split())
        self.read_s += new / READ_WORDS_PER_S
        self.played_s += new / READ_WORDS_PER_S
        rec = {"n": self.n, "minute": round(self.played_s / 60, 2), "action": action, "words": words, "shot": shot}
        if self.played_s >= self.cap_s:
            rec["stopped"] = "the session's time is up: run play.py stop"
        hidden = {"state": self.g.state(), "errors": self.g.errors[-5:], "spoken": self.g.js(SPOKEN_JS)}
        if self.n % 10 == 0:
            self.save_to("save_%04d.json" % self.n)
        self.log.write(json.dumps(dict(rec, hidden=hidden)) + "\n")
        self.log.flush()
        return rec

    def act(self, cmd, args):
        if self.played_s >= self.cap_s and cmd != "look":
            return {"minute": round(self.played_s / 60, 2), "stopped": "the session's time is up: run play.py stop"}
        if cmd == "look":
            pass
        elif cmd == "hold":
            keys = [k for k in args[0].split("+") if k]
            self.step(min(float(args[1]) if len(args) > 1 else 1.0, MAX_HOLD_S), keys)
        elif cmd == "tap":
            self.g.tap(args[0])
            self.step(1 / 3)
        elif cmd == "type":
            self.g.pg.keyboard.type(" ".join(args), delay=20)  # unquoted words are all typed, as the log keeps them
            self.g.tap("Enter")
            self.step(0.5)
        elif cmd == "turn":
            deg = max(-180.0, min(180.0, float(args[0])))
            self.g.js("(d) => { LEDGER.cam.yaw += d; }", math.radians(deg))
            self.step(0.2)
        elif cmd == "wait":
            self.step(min(float(args[0]), MAX_WAIT_S))
        else:
            return {"error": "unknown command %s (look, hold, tap, type, turn, wait, stop)" % cmd}
        return self.screen(" ".join([cmd] + list(args)))

    def stop(self):
        s = {"minutes_played": round(self.played_s / 60, 2), "minutes_of_keys": round(self.keys_s / 60, 2),
             "minutes_reading": round(self.read_s / 60, 2), "actions": self.n, "wall_minutes": round((time.time() - self.started) / 60, 1),
             "errors": self.g.errors[:20]}
        self.save_to("final_save.json")
        json.dump(s, open(os.path.join(os.path.dirname(self.log.name), "session.json"), "w"), indent=1)
        self.log.close()
        self.g.close()
        return s


def serve(a):
    if os.path.abspath(a.hidden).startswith(os.path.abspath(a.out) + os.sep):
        raise SystemExit("--hidden must not be inside --out (the player may open files under --out)")
    sess = Session(a.dist, a.out, a.seed, a.hidden, a.minutes)
    sess.g.clear(tries=0)  # leave the opening as a newcomer meets it
    sess.save_to("start_save.json")

    class H(BaseHTTPRequestHandler):
        def log_message(self, *x):
            pass

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
            cmd, args = body.get("cmd", "look"), body.get("args", [])
            try:
                if cmd == "stop":  # the page errors stay in the hidden session.json: the player never saw them
                    res = {k: v for k, v in sess.stop().items() if k != "errors"}
                else:
                    res = sess.act(cmd, args)
            except Exception as e:
                res = {"error": str(e)[:300]}
            data = json.dumps(res).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            if cmd == "stop":
                os._exit(0)

    srv = HTTPServer(("127.0.0.1", a.port), H)  # one request at a time, in this thread: the browser is not shared
    print("playing on port %d; screenshots in %s" % (a.port, os.path.join(a.out, "shots")), flush=True)
    srv.serve_forever()


def client(cmd, args, port):
    req = urllib.request.Request("http://127.0.0.1:%d/" % port, data=json.dumps({"cmd": cmd, "args": args}).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            print(r.read().decode())
    except OSError as e:  # the server is not running or went away: one plain line, not a traceback
        print(json.dumps({"error": "no game is running on port %d (%s)" % (port, getattr(e, "reason", e))}))
        return 1
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "serve":
        ap = argparse.ArgumentParser()
        ap.add_argument("--dist", required=True)
        ap.add_argument("--out", required=True)
        ap.add_argument("--port", type=int, default=8765)
        ap.add_argument("--seed", type=int, default=7)
        ap.add_argument("--hidden", required=True, help="the game-state log, kept apart from the screenshots")
        ap.add_argument("--minutes", type=float, default=60)
        serve(ap.parse_args(argv[1:]))
        return 0
    port = int(os.environ.get("LEDGER_PLAY_PORT", "8765"))
    if not argv:
        print(__doc__)
        return 2
    return client(argv[0], argv[1:], port)


if __name__ == "__main__":
    sys.exit(main())
