"""Let an AI player type actually play a build of the LEDGER prototype (lane task 4t, piece 2).

The player sees only what a person sees (a screenshot and the words on screen) and acts only with keys. The game is
stepped by hand: it stands still while the player thinks, and moves on only by the time each action takes, so a slow
model plays at a person's pace in game time. Every action is logged with the game's own state beside it (the player
never sees that part; the consequence checker and the panel read it later).

    python play.py serve --dist DIR --out DIR [--port 8765] [--seed 7]      (one session; leave it running)
    python play.py look                                                   (the screen now)
    python play.py hold KeyW 3          hold keys for game seconds; several keys joined by +, e.g. KeyW+ShiftLeft
    python play.py tap KeyE             one press, then a third of a second
    python play.py type "Where's Mickey's?"   type words (into a talk box when one is open), then Enter
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

STATE_JS = "() => LEDGER.read()"


class Session:
    def __init__(self, dist, out, seed):
        from clumsy import Proto
        self.g = Proto(dist, seed=seed)
        self.out = out
        os.makedirs(os.path.join(out, "shots"), exist_ok=True)
        self.played_s = 0.0
        self.n = 0
        self.log = open(os.path.join(out, "actions.jsonl"), "a")
        self.started = time.time()

    def step(self, secs, keys=()):
        g = self.g
        for k in keys:
            g.down(k)
        g.run(secs, every=max(secs, 0.1))
        for k in keys:
            g.up(k)
        self.played_s += secs

    def screen(self, action):
        self.n += 1
        shot = os.path.join(self.out, "shots", "%04d.png" % self.n)
        shot = self.g.shot(shot)
        words = {k: v for k, v in self.g.words().items() if v}
        rec = {"n": self.n, "minute": round(self.played_s / 60, 2), "action": action, "words": words, "shot": shot}
        hidden = {"state": self.g.state(), "errors": self.g.errors[-5:]}
        self.log.write(json.dumps(dict(rec, hidden=hidden)) + "\n")
        self.log.flush()
        return rec

    def act(self, cmd, args):
        if cmd == "look":
            pass
        elif cmd == "hold":
            keys = [k for k in args[0].split("+") if k]
            self.step(min(float(args[1]) if len(args) > 1 else 1.0, MAX_HOLD_S), keys)
        elif cmd == "tap":
            self.g.tap(args[0])
            self.step(1 / 3)
        elif cmd == "type":
            self.g.pg.keyboard.type(args[0], delay=20)
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
        s = {"minutes_played": round(self.played_s / 60, 2), "actions": self.n, "wall_minutes": round((time.time() - self.started) / 60, 1),
             "errors": self.g.errors[:20]}
        json.dump(s, open(os.path.join(self.out, "session.json"), "w"), indent=1)
        self.log.close()
        self.g.close()
        return s


def serve(a):
    sess = Session(a.dist, a.out, a.seed)
    sess.g.clear(tries=0)  # leave the opening as a newcomer meets it

    class H(BaseHTTPRequestHandler):
        def log_message(self, *x):
            pass

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
            cmd, args = body.get("cmd", "look"), body.get("args", [])
            try:
                if cmd == "stop":
                    res = sess.stop()
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
    with urllib.request.urlopen(req, timeout=300) as r:
        print(r.read().decode())


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "serve":
        ap = argparse.ArgumentParser()
        ap.add_argument("--dist", required=True)
        ap.add_argument("--out", required=True)
        ap.add_argument("--port", type=int, default=8765)
        ap.add_argument("--seed", type=int, default=7)
        serve(ap.parse_args(argv[1:]))
        return 0
    port = int(os.environ.get("LEDGER_PLAY_PORT", "8765"))
    if not argv:
        print(__doc__)
        return 2
    client(argv[0], argv[1:], port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
