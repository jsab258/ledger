#!/usr/bin/env python3
"""THE VOICE'S OWN TIME, WITHOUT THE GAME (item 2, the delay; the research's
first measurement, production/research/voice-latency/NOTE-2026-09-30.md).

    python tools/voice-live/voice_bench.py [--cpu] [--who rocco] [--out F:/LedgerTools/tmp/voice-bench]

Starts the game's own voice server (voice-server.py, --prewarm) exactly as the
game does, sends it the first sentences of the 30 September real-talk run one
at a time, and prints, for each, the server's own work time ("ms") and the
length of the speech it made; then the median fixed cost and the work per
second of speech (a least-squares line through the points). Nothing else is
running beside it, so this is the voice alone; the game's timing line gives
the same figures inside the game. Writes its sound files under --out (F:).
"""
import json
import os
import statistics
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = os.environ.get("LEDGER_VOICE_PY", r"C:\LedgerTools\chatterbox-nano\env-dml\Scripts\python.exe")
SERVER = os.path.join(REPO, "tools", "voice-live", "voice-server.py")
# First sentences the real talk wrote on 30 September (production/playtest/real-talk-2026-09-30.md's run).
LINES = ["Morning.", "Quiet one today.", "Twelve years, give or take.", "Depends who's asking.",
         "Not that I've seen, no.", "The rank fills up about six.", "Couldn't tell you, pal.",
         "Aye, she's alright is Sheila.", "The drivers use the cafe.", "Ask Sheila, she keeps the book.",
         "Rita's had that shop years.", "Mind how you go."]


def fit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 0.0
    return my - b * mx, b


def main():
    who = sys.argv[sys.argv.index("--who") + 1] if "--who" in sys.argv else "rocco"
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "F:/LedgerTools/tmp/voice-bench"
    cmd = [PY, SERVER, "--prewarm", "--out", out] + (["--cpu"] if "--cpu" in sys.argv else [])
    t0 = time.time()
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
    for line in p.stdout:
        if '"ready"' in line:
            print("ready after %.1f s: %s" % (time.time() - t0, line.strip()[:160]))
            break
    work, length = [], []
    for k, text in enumerate(LINES):
        t = time.time()
        p.stdin.write(json.dumps({"id": 1000 + k, "who": who, "text": text}) + "\n")
        p.stdin.flush()
        for line in p.stdout:
            try:
                d = json.loads(line)
            except ValueError:
                continue   # the model's own chatter on its output
            if not isinstance(d, dict) or d.get("id") != 1000 + k:
                continue
            if d.get("part") == 0:
                wall = time.time() - t
                work.append(d["ms"] / 1000.0)
                length.append(d["seconds"])
                print("%-34s made in %.2f s (wall %.2f s), %.2f s of speech" % (text, d["ms"] / 1000.0, wall, d["seconds"]))
            if d.get("last") or d.get("error"):
                break
    p.stdin.close()
    p.wait(timeout=60)
    a, b = fit(length, work)
    print("median work %.2f s for median speech %.2f s; fixed cost %.2f s + %.2f s of work per second of speech"
          % (statistics.median(work), statistics.median(length), a, b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
