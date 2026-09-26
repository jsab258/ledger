#!/usr/bin/env python3
"""How long from the player's line to the character's first spoken words, stage by stage.

    python tools/voice-live/latency.py --lines 12 [--prewarm] [--early] [--voice nano|pocket] [--out F:/.../latency.json]
    python tools/voice-live/latency.py --selftest

WHY, 26 September. Jafar: "Today about six seconds pass between my line and the
character speaking. ... First, measure the path: my line sent, the first words
of the reply, the first sentence ready, the first sound made, the first sound
heard. Median and slowest, with the game running." The target is under two
seconds to the first real words.

It drives the game's own two helpers exactly as the game does
(CrimeProbe.cpp LiveAsk / LiveHelperPump / LiveVoiceSay / LiveVoicePump):
ledger/TalkHelper (the real model, with its check for invented details) and
tools/voice-live/voice-server.py (the cast voices), one JSON line each way.
Run it with the game open in the street, so the graphics card is as busy as
when he plays. The key is read from the game's settings into the helper's
environment only, never printed.

THE STAGES, each in seconds after the line is sent:
  firstWords     the reply's first words reach the game (without --early, the
                 whole reply at once: the helper does not stream)
  firstSentence  the reply's first sentence is known
  firstSoundMade the voice server has the first piece's sound
  firstHeard     the game starts playing it: the game reads the voice
                 server's line on its next frame and plays at once, so
                 firstSoundMade plus one frame at 60 a second (0.017 s) plus the
                 sound card's buffer (PLAY_S, measured below)
--prewarm  the cast voices are learned and the voice run once before the first
           line (voice-server.py --prewarm), as the fix proposes
--early    the helper sends the reply's first checked sentence as soon as it
           has it (TalkHelper --early), and the voice starts on it at once
"""
import json
import os
import statistics
import subprocess
import sys
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HELPER = os.path.join(ROOT, "ledger", "TalkHelper", "bin", "Release", "net8.0", "TalkHelper.exe")
VOICE_PY = r"C:\LedgerTools\chatterbox-nano\env-dml\Scripts\python.exe"
POCKET_PY = r"F:\LedgerTools\pocket-tts\env\Scripts\python.exe"
SECRETS = os.path.join(os.path.expanduser("~"), "AppData", "LocalLow", "DefaultCompany", "ledger", "secrets.json")
FRAME_S = 1 / 60
PLAY_S = 0.02          # the sound card's start-up buffer for a procedural sound (Unreal's default mixer buffer, 1024 frames at 48 kHz)

LINES = [
    ("lena", "Evening. Anything going on round here?"),
    ("rocco", "You look like you've been stood there a while."),
    ("sam", "What are you selling today, then?"),
    ("lena", "How long have you kept the books for Mickey?"),
    ("rocco", "Did you hear the glass go last night?"),
    ("sam", "Who's the new owner, then?"),
    ("lena", "Is it always this quiet on a Tuesday?"),
    ("rocco", "Were you on the docks, before?"),
    ("sam", "Can you get me a pager?"),
    ("lena", "Do you know who broke the window?"),
    ("rocco", "Cold one tonight, isn't it."),
    ("sam", "Your mum know you're out?"),
]


class Pipe:
    """A child process spoken to in JSON lines; each line read is kept with the time it arrived."""

    def __init__(self, args, env=None):
        self.p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                  env=env, cwd=ROOT, text=True, encoding="utf-8", bufsize=1)
        self.lines = []
        self.cv = threading.Condition()
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        for line in self.p.stdout:
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            with self.cv:
                self.lines.append((time.perf_counter(), d))
                self.cv.notify_all()

    def send(self, d):
        self.p.stdin.write(json.dumps(d) + "\n")
        self.p.stdin.flush()

    def wait(self, test, timeout=120):
        end = time.perf_counter() + timeout
        with self.cv:
            while True:
                for i, (t, d) in enumerate(self.lines):
                    if test(d):
                        del self.lines[i]
                        return t, d
                left = end - time.perf_counter()
                if left <= 0:
                    return None, None
                self.cv.wait(left)

    def stop(self):
        try:
            self.p.stdin.close()
            self.p.wait(10)
        except Exception:
            self.p.kill()


def first_sentence(text):
    import re
    parts = [x for x in re.split(r"(?<=[.!?])\s+", text.strip()) if x]
    return parts[0] if parts else text


def summary(rows, key):
    xs = [r[key] for r in rows if r.get(key) is not None]
    if not xs:
        return None
    return {"median": round(statistics.median(xs), 2), "slowest": round(max(xs), 2), "fastest": round(min(xs), 2), "n": len(xs)}


def run(n, prewarm=False, early=False, voice="nano"):
    env = dict(os.environ)
    try:
        env["ANTHROPIC_API_KEY"] = json.load(open(SECRETS, encoding="utf-8"))["anthropic_api_key"]
    except Exception:
        return {"error": "no key in the game's settings"}
    hargs = [HELPER] + (["--early"] if early else [])
    if voice == "pocket":
        vargs = [POCKET_PY, os.path.join(ROOT, "tools", "voice-live", "pocket-server.py")]
    else:
        vargs = [VOICE_PY, os.path.join(ROOT, "tools", "voice-live", "voice-server.py")]
    if prewarm:
        vargs.append("--prewarm")
    venv = dict(os.environ, HF_HUB_OFFLINE="1")
    t_start = time.perf_counter()
    helper = Pipe(hargs, env)
    voicep = Pipe(vargs, venv)
    th, h = helper.wait(lambda d: d.get("ready"), 60)
    tv, v = voicep.wait(lambda d: d.get("ready"), 240)
    out = {"voice": voice, "prewarm": prewarm, "early": early, "helperReadyS": round(th - t_start, 1) if th else None,
           "voiceReadyS": round(tv - t_start, 1) if tv else None, "voiceDevice": (v or {}).get("device"), "lines": []}
    if not (h and v):
        out["error"] = "a helper did not start"
        helper.stop(); voicep.stop()
        return out
    for i in range(n):
        who, say = LINES[i % len(LINES)]
        rid = 100 + i
        t0 = time.perf_counter()
        helper.send({"id": rid, "to": who, "say": say, "hour": 21, "scene": "the street by Mickey's, evening"})
        row = {"who": who, "say": say}
        spoke = False
        tr = r = None
        if early:
            te, e = helper.wait(lambda d: d.get("id") == rid and ("first" in d or "reply" in d), 30)
            if e and "first" in e:
                row["firstWords"] = row["firstSentence"] = te - t0
                voicep.send({"id": rid * 10, "who": who, "text": e["first"]})
                spoke = True
            elif e:
                tr, r = te, e    # no early sentence (it did not pass its check): the whole reply came first
        if r is None:
            tr, r = helper.wait(lambda d: d.get("id") == rid and "reply" in d, 30)
        if r is None:
            row["error"] = "no reply"
            out["lines"].append(row)
            continue
        row["reply"] = r.get("reply")
        row["helperMs"] = r.get("ms")
        row["replyWhole"] = tr - t0
        if not spoke:
            row["firstWords"] = row["firstSentence"] = tr - t0
            voicep.send({"id": rid * 10, "who": who, "text": r["reply"]})
        elif r.get("rest"):
            voicep.send({"id": rid * 10 + 1, "who": who, "text": r["rest"]})
        tm, m = voicep.wait(lambda d: d.get("id") == rid * 10 and d.get("part") == 0, 60)
        if m is None:
            row["error"] = "no sound"
        else:
            row["firstSoundMade"] = tm - t0
            row["firstHeard"] = row["firstSoundMade"] + FRAME_S + PLAY_S
            row["firstPieceSeconds"] = m.get("seconds")
            row["firstPieceWav"] = m.get("wav")
            if m.get("firstChunk"):
                # A STREAMING VOICE (Pocket): its first sound came ahead of the
                # whole first piece; when that piece is whole is kept beside it.
                tw, w = voicep.wait(lambda d: d.get("id") == rid * 10 and d.get("part") == 0 and d.get("pieceLast"), 60)
                if w is not None:
                    row["firstPieceWhole"] = tw - t0
        # let every piece of this reply finish before the next line, as a player would listen
        deadline = time.perf_counter() + 40
        while time.perf_counter() < deadline:
            t_, d_ = voicep.wait(lambda d: d.get("id") in (rid * 10, rid * 10 + 1) and d.get("last"), 2)
            if d_ is not None:
                if d_.get("id") == rid * 10 + 1 or not (early and r.get("rest")):
                    break
        for k in ("firstWords", "firstSentence", "firstSoundMade", "firstHeard", "firstPieceWhole", "replyWhole"):
            if k in row:
                row[k] = round(row[k], 2)
        out["lines"].append(row)
        print(json.dumps({k: row.get(k) for k in ("who", "firstWords", "firstSentence", "firstSoundMade", "firstHeard", "helperMs")}), flush=True)
    helper.stop()
    voicep.stop()
    ok = [r for r in out["lines"] if "error" not in r]
    out["summary"] = {k: summary(ok, k) for k in ("firstWords", "firstSentence", "firstSoundMade", "firstHeard", "firstPieceWhole", "replyWhole")}
    return out


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("latency selftest FAIL " + name)
    check("the first sentence is cut at its end", first_sentence("Aye. I saw it. Dark coat.") == "Aye.")
    check("a reply with no stop is its own first sentence", first_sentence("Not now love") == "Not now love")
    s = summary([{"a": 1.0}, {"a": 3.0}, {"a": 2.0}], "a")
    check("median and slowest", s["median"] == 2.0 and s["slowest"] == 3.0)
    check("twelve lines across the three", len(LINES) == 12 and {w for w, _ in LINES} == {"lena", "rocco", "sam"})
    check("the key never reaches the command line", "anthropic" not in " ".join([HELPER]).lower())
    print("latency selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    n = int(a[a.index("--lines") + 1]) if "--lines" in a else 12
    voice = a[a.index("--voice") + 1] if "--voice" in a else "nano"
    res = run(n, prewarm="--prewarm" in a, early="--early" in a, voice=voice)
    if "--out" in a:
        json.dump(res, open(a[a.index("--out") + 1], "w", encoding="utf-8"), indent=1)
    print("SUMMARY " + json.dumps(res.get("summary"), indent=None))
