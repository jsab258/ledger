#!/usr/bin/env python3
"""WATCH AN INSTALLED GAME'S OPENING, SENDING NO KEYS (n23-1, 23 Nov 2026).

    python tools/drills/watch_opening.py --exe "C:\\Games\\Sleeping Dogs Definitive Edition\\sdhdship.exe" --seconds 240 [--every 2] [--keys 45:enter,52:enter]

--keys: a FIXED list of taps, each at its second after launch, written before the run from an
earlier run's frames (never chosen from frames during the run); a tap goes only when the game's
window is in front, else the run stops; each tap's time is logged on the frames' clock.

Why: INSTALLED-METHOD.md's openings rule says a game's opening is played only
by fixed key scripts where it is linear; to write such a script the session
must first know what the opening shows and asks for, without choosing keys
from frames (that would be computer use). So this starts the game, sends no
key or click at all, films its own window every few seconds with the time on
the high-resolution clock, and closes the game at the end.

Rules kept: runs only after he has been away 10 minutes (INSTALLED-METHOD
"When it runs"); stops and closes the game the moment he touches the mouse or
keyboard (last-input time moves while this sends nothing); the window's own
pixels only (play.py's screenshot); frames on F: under the retention-covered
tmp folder, never in git. The game's files are never touched.
"""
import argparse
import ctypes
import ctypes.wintypes as wt
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ai-tester"))
import play  # noqa: E402  (screenshot, seconds_since_input, window_pid)

user32 = ctypes.windll.user32
OUT_ROOT = r"F:\LedgerTools\tmp\drills"
AWAY_S = 600


def windows_of(pid):
    found = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
    def cb(hwnd, _):
        if user32.IsWindowVisible(hwnd) and play.window_pid(hwnd) == pid:
            r = wt.RECT()
            user32.GetClientRect(hwnd, ctypes.byref(r))
            if r.right * r.bottom > 200 * 200:
                found.append((r.right * r.bottom, hwnd))
        return True
    user32.EnumWindows(cb, 0)
    return max(found)[1] if found else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", required=True)
    ap.add_argument("--seconds", type=float, default=240)
    ap.add_argument("--every", type=float, default=2.0)
    ap.add_argument("--keys", default="")
    a = ap.parse_args()
    away = play.seconds_since_input()
    if away < AWAY_S:
        print("watch status=PC-IN-USE away=%.0f s (needs %d)" % (away, AWAY_S))
        return 1
    stamp = time.strftime("%Y-%m-%d-%H%M")
    out = os.path.join(OUT_ROOT, os.path.splitext(os.path.basename(a.exe))[0] + "-opening-" + stamp)
    os.makedirs(out, exist_ok=True)
    proc = subprocess.Popen([a.exe], cwd=os.path.dirname(a.exe))
    t_start = time.perf_counter()
    base_input = play.seconds_since_input()
    n, why = 0, "time"
    keys = sorted((float(k.split(":")[0]), k.split(":")[1]) for k in a.keys.split(",") if k)
    sent_at = None
    with open(os.path.join(out, "times.jsonl"), "w", encoding="utf-8") as tf:
        tf.write(json.dumps({"event": "launched", "t": round(t_start, 4), "pid": proc.pid}) + "\n")
        while time.perf_counter() - t_start < a.seconds:
            time.sleep(a.every)
            # he touched the PC: last input is newer than when we began (this sends nothing)
            since_ours = (time.perf_counter() - sent_at) if sent_at else (time.perf_counter() - t_start) + base_input
            if play.seconds_since_input() < since_ours - 1.5:
                why = "his-input"
                break
            if proc.poll() is not None:
                why = "game-exited"
                break
            hwnd = windows_of(proc.pid)
            if not hwnd:
                continue
            while keys and time.perf_counter() - t_start >= keys[0][0]:
                at, name = keys.pop(0)
                if play.window_pid(user32.GetForegroundWindow()) != proc.pid:
                    # a game started from a background process is not handed the front (23 Nov, run 2031):
                    # bring it forward once, as the tester does (play.focus; its ALT counts as our input)
                    play.focus(hwnd)
                    sent_at = time.perf_counter()
                if play.window_pid(user32.GetForegroundWindow()) != proc.pid:
                    why = "not-in-front"
                    break
                tk = time.perf_counter()
                if name.startswith("walk") or name.startswith("run"):
                    # walk4 / run4: hold W (with Shift for run) that many seconds, filmed fast with
                    # every grab's window logged (the drills' timing, FILM-RULER-2026-11-23.md)
                    secs = float(name.lstrip("walkrun") or 4)
                    kept = []

                    def grab():
                        g0 = time.perf_counter()
                        try:
                            im_ = play.screenshot(hwnd)
                        except RuntimeError:
                            return
                        kept.append((g0, time.perf_counter(), im_))
                    tf.write(json.dumps({"event": "key_down", "key": name, "t": round(time.perf_counter(), 4)}) + "\n")
                    play.hold("w", secs, run=name.startswith("run"), each=grab, gap=0.0)
                    tf.write(json.dumps({"event": "key_up", "key": name, "t": round(time.perf_counter(), 4)}) + "\n")
                    for k, (g0, g1, im_) in enumerate(kept, 1):
                        w_, h_ = im_.size
                        im_.resize((960, max(1, round(h_ * 960 / float(w_))))).save(
                            os.path.join(out, "%s-%.0f-%04d.jpg" % (name, at, k)), quality=82)
                        tf.write(json.dumps({"hold": name, "at": at, "k": k, "t0": round(g0, 4), "t1": round(g1, 4)}) + "\n")
                else:
                    play.tap(name)
                sent_at = time.perf_counter()
                tf.write(json.dumps({"event": "tap", "key": name, "t": round(tk, 4), "since_launch": round(tk - t_start, 2)}) + "\n")
            if why == "not-in-front":
                break
            try:
                t0 = time.perf_counter()
                im = play.screenshot(hwnd)
                t1 = time.perf_counter()
            except RuntimeError:
                continue
            n += 1
            w, h = im.size
            im.resize((960, max(1, round(h * 960 / float(w))))).save(os.path.join(out, "w-%04d.jpg" % n), quality=80)
            tf.write(json.dumps({"n": n, "t0": round(t0, 4), "t1": round(t1, 4), "since_launch": round(t0 - t_start, 2)}) + "\n")
    subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)
    print("watch status=DONE stop=%s frames=%d dir=%s" % (why, n, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
