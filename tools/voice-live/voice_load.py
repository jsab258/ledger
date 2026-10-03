#!/usr/bin/env python3
"""THE CAST VOICE, SPEAKING WITHOUT A BREAK, beside a measurement (P1, 3 October).

    python tools/voice-live/voice_load.py [--cpu] [--seconds 600]
    python tools/voice-live/voice_load.py --selftest

WHY. Jafar's order of 3 October (P1): profile the hook camera "with the voice speaking",
and say whether "the voice on the processor" would make room. This runs the game's own
voice program (voice-server.py, the cast's voices, warmed first) on the graphics card, or
on the processor with --cpu, and hands it the cast's lines one after another, each as soon
as the last is made, so the card (or the processor) carries the voice's whole load for the
length of a capture. It prints "voiceLoad ready" when the first line is under way, one line
per sentence made, and a summary when it is stopped or its time is up. Nothing is played
aloud; the sound files go to F:/LedgerTools/tmp/builder/voice-load (scratch).
"""
import json
import os
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = r"C:\LedgerTools\chatterbox-nano\env-dml\Scripts\python.exe"
SCRIPT = os.path.join(REPO, "tools", "voice-live", "voice-server.py")
OUT = r"F:\LedgerTools\tmp\builder\voice-load"
LINES = [
    ("lena", "Morning, love. You'll be the one stopping at Mickey's, then."),
    ("rocco", "Thirty years on the quay, and this rank since. Not much moves here I haven't seen."),
    ("sam", "Alright. Not seen you round here before. You staying long?"),
    ("lena", "Rita keeps the pawn shop two doors up. She'll want to know who you are."),
    ("rocco", "Office opens at seven. Two drivers on the rank, and me on the door."),
    ("sam", "It's quiet till the boats come in. Then it's all go for an hour."),
]


def request(n):
    who, text = LINES[n % len(LINES)]
    return json.dumps({"id": n + 1, "who": who, "text": text}) + "\n"


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("voice_load selftest FAIL " + name)
    a, b = json.loads(request(0)), json.loads(request(len(LINES)))
    check("each request names the speaker and the line", a["who"] == "lena" and a["text"] and a["id"] == 1)
    check("the lines go round, numbered on", b["who"] == "lena" and b["id"] == len(LINES) + 1)
    check("the three of the cast all speak", {w for w, _ in LINES} == {"lena", "rocco", "sam"})
    check("its sound goes to scratch on F:, never the repository", OUT.lower().startswith(r"f:\ledgertools\tmp"))
    print("voice_load selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    cpu = "--cpu" in argv
    seconds = float(argv[argv.index("--seconds") + 1]) if "--seconds" in argv else 600.0
    os.makedirs(OUT, exist_ok=True)
    args = [PY, SCRIPT, "--prewarm", "--out", OUT] + (["--cpu"] if cpu else [])
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                         text=True, bufsize=1, cwd=REPO)
    t0 = time.time()
    for line in p.stdout:
        if '"ready"' in line:
            break
    print("voiceLoad warmed after %.1f s on the %s" % (time.time() - t0, "processor" if cpu else "graphics card"), flush=True)
    n, made, spoken, started = 0, 0, 0.0, time.time()
    p.stdin.write(request(n))
    p.stdin.flush()
    print("voiceLoad ready", flush=True)
    try:
        for line in p.stdout:
            if '"wav"' not in line:
                continue
            d = json.loads(line)
            made += 1
            spoken += float(d.get("seconds") or 0.0)
            if d.get("last"):
                n += 1
                if time.time() - started > seconds:
                    break
                p.stdin.write(request(n))
                p.stdin.flush()
    except KeyboardInterrupt:
        pass
    took = time.time() - started
    print("voiceLoadSummary device=%s lines=%d pieces=%d spokenSeconds=%.1f madeInSeconds=%.1f realtime=%.2f"
          % ("cpu" if cpu else "card", n, made, spoken, took, took / spoken if spoken else 0.0), flush=True)
    try:
        p.stdin.close()
        p.wait(timeout=20)
    except Exception:
        p.kill()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
