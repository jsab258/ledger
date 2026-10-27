#!/usr/bin/env python3
"""The fast checker, served to the game's talk over a pipe (his page pick of 27 October 2026, night: the open cut-off,
in the game behind a switch, measured live before it is on by default).

    C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe -I tools/checkers/checker_server.py SPEC.json

SPEC is production/specs/fast-checker.json (the model, how many of the closest facts it reads, its cut-off). One JSON
line in a request, one out: {"id": 7, "known": ["C1: ...", ...], "probe": "the player's line", "detail": "the first
sentence"} answers {"id": 7, "score": 0.031, "ms": 48}, the score the chance the sentence holds something the facts do
not; below the cut-off the game says it without waiting for Haiku. A line it cannot score answers {"id": .., "error":
".."}. It prints {"ready": true, ...} once the model is loaded, and ends when its input closes.

WHY A PROCESS OF ITS OWN, 27 October: it is the checker exactly as it was measured (tools/checkers/measure_checkers.py,
PyTorch on 2 threads), with nothing new to download. The way to ship it inside the game's own process is ONNX Runtime,
which needs his yes for its download; this is the measurement's way, behind a switch that is off.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    import torch
    torch.set_num_threads(int(spec.get("threads", 2)))
    import measure_checkers as m
    score = m.lettuce_scorer(spec["model"], int(spec["top"]), int8=bool(spec.get("int8", False)))
    score({"known": ["C1: warm-up."], "probe": "Warm up?", "detail": "Warm up."})
    print(json.dumps({"ready": True, "model": spec["model"], "top": spec["top"], "cut": spec["cut"]}), flush=True)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        rid = None
        try:
            r = json.loads(line)
            rid = r.get("id")
            t0 = time.perf_counter()
            s = float(score({"known": r["known"], "probe": r.get("probe", ""), "detail": r["detail"]}))
            print(json.dumps({"id": rid, "score": round(s, 6), "ms": int((time.perf_counter() - t0) * 1000)}), flush=True)
        except Exception as e:  # one bad line never ends the server
            print(json.dumps({"id": rid, "error": "%s: %s" % (type(e).__name__, e)}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
