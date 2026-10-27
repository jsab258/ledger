#!/usr/bin/env python3
"""The fourth try's first measure: each candidate checker's time alone on this PC's processor, with the 10 closest facts,
in full precision and in 8 bits, before any is trained.

    C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe tools/checkers/speed_sizes.py OUT.json [--threads 2] [--calls 300]

WHY, 27 October 2026. His fourth try (production/research/invented-claims/LOCAL-CHECKERS-2026-10-26.md, "Fourth try:
the design"): a larger small checker with the 10 closest facts, within 0.15 s beside the game. Untrained weights answer as
fast as trained ones of the same size, so the size is chosen on speed first. The third try's trained 17M is timed the
same way as the yardstick: beside the packaged game it took 0.072 s (median).

Run only with the game, the editor and the build machine's work closed (the times are the processor's alone).
"""
import json
import os
import statistics
import sys
import time

os.environ.setdefault("HF_HUB_OFFLINE", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import measure_checkers as m  # noqa: E402

CANDIDATES = [("trained-17m-try3", r"F:\LedgerTools\checkers\trained\tinylettuce-17m-try3-2026-10-26"),
              ("tinylettuce-32m", m.LETTUCE["tinylettuce-32m"]), ("tinylettuce-68m", m.LETTUCE["tinylettuce-68m"]),
              ("lettucedetect-base", m.LETTUCE["lettucedetect-base"])]


def main(a):
    opt = lambda n, d: a[a.index(n) + 1] if n in a else d  # noqa: E731
    import torch
    torch.set_num_threads(int(opt("--threads", "2")))
    calls = int(opt("--calls", "300"))
    tune, held = m.rows()
    items = (held + tune)[:calls]
    out = []
    for name, path in CANDIDATES:
        for int8 in (False, True):
            score = m.lettuce_scorer(path, 10, int8=int8)
            score(items[0])
            times = []
            for r in items:
                s = time.perf_counter()
                score(r)
                times.append(time.perf_counter() - s)
            times.sort()
            row = {"model": name, "int8": int8, "calls": len(times), "secondsMedian": round(statistics.median(times), 4),
                   "secondsP99": round(times[int(len(times) * 0.99)], 4), "secondsMax": round(times[-1], 4)}
            print(json.dumps(row), flush=True)
            out.append(row)
    json.dump({"threads": torch.get_num_threads(), "top": 10, "rows": out}, open(a[0], "w", encoding="utf-8"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
