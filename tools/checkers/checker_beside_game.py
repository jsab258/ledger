#!/usr/bin/env python3
"""The trained checker working without pause beside the running game: its own times, for the game's frame times to be
read against a run without it.

    C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe tools/checkers/checker_beside_game.py MODEL_DIR OUT.json
        [--top 6] [--threads 2] [--seconds 90] [--calls CALLS.txt]

WHY, 26 October 2026. His bar for the fast checker (orders/2026-10-25.md, speech 1): "answers in 0.15 s or less on
this PC beside the running game without frame stalls". Its times alone are in measure_checkers.py; this runs it
beside the packaged game (the slice, as the build machine's performance step runs it), scoring the bench's labelled
details over and over, one at a time, with a fixed small thread count (LOCAL-CHECKERS-2026-10-26.md, "Three levers",
3), so that the game's CSV frame times with it can be laid beside a run without it. Working without pause is harsher
than the game, which checks one sentence a turn.

--calls writes each answer's end time (seconds since the epoch) and its length as it goes, so the answers given while
the game was actually running can be picked out (the fresh review of 26 October night: a 150-second run beside a
35-second game timed mostly answers with no game open).
"""
import json
import os
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import measure_checkers as m  # noqa: E402


def main(a):
    opt = lambda n, d: a[a.index(n) + 1] if n in a else d  # noqa: E731
    import torch
    torch.set_num_threads(int(opt("--threads", "2")))
    tune, held = m.rows()
    score = m.lettuce_scorer(a[0], int(opt("--top", "6")))
    score(held[0])
    secs, times, t0 = float(opt("--seconds", "90")), [], time.time()
    calls = open(opt("--calls", os.devnull), "w", encoding="utf-8")
    while time.time() - t0 < secs:
        for r in held + tune:
            s = time.perf_counter()
            score(r)
            times.append(time.perf_counter() - s)
            calls.write("%.3f %.4f\n" % (time.time(), times[-1]))
            calls.flush()
            if time.time() - t0 >= secs:
                break
    times.sort()
    out = {"model": a[0], "threads": torch.get_num_threads(), "calls": len(times), "secondsMedian": round(statistics.median(times), 4),
           "secondsP99": round(times[int(len(times) * 0.99)], 4), "secondsMax": round(times[-1], 4),
           "over015": sum(t > 0.15 for t in times)}
    json.dump(out, open(a[1], "w", encoding="utf-8"), indent=1)
    print(json.dumps(out), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
