#!/usr/bin/env python3
"""How many of the bench's real first sentences the trained checker would clear before Haiku answers.

    C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe tools/checkers/firsts_cleared.py MODEL_DIR THRESHOLD OUT.json
        RUN_DIR [RUN_DIR ...] [--top 6]

WHY, 26 October 2026. The 127 labelled details measure the checker detail by detail; the game would hand it a whole
first sentence. The bench's turns (ledger/ClaimBench firsts --early, the game's own settings) keep each first sentence
that passed Haiku's check, with the speaker's facts; this scores those sentences as the game would (the sentence as
the answer, the 6 facts sharing the most words with the question and the sentence) at the threshold set on the tune
half, and counts how many it would clear, by moment: a newcomer's real question (Models.Core) or small talk
(Models.Ambient), per his ruling of 26 October that the speech bar is judged on real questions. The bench keeps no
text for a refused first sentence, so this measures what it would speed up, not what it would let through; that is
the 127's job.
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import measure_checkers as m  # noqa: E402


def main(a):
    top = int(a[a.index("--top") + 1]) if "--top" in a else 6
    dirs = [d for i, d in enumerate(a[3:], 3) if not d.startswith("--") and a[i - 1] != "--top"]
    score, th = m.lettuce_scorer(a[0], top), float(a[1])
    out = collections.defaultdict(lambda: {"turns": 0, "firstPassed": 0, "cleared": 0})
    for d in dirs:
        for line in open(os.path.join(d, "firsts.jsonl"), encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            k = out["small talk" if "haiku" in (r.get("model") or "") else "real question"]
            k["turns"] += 1
            if "first-passed" not in [s["step"] for s in r["steps"]]:
                continue
            k["firstPassed"] += 1
            first = re.split(r"(?<=[.!?])\s+", r["reply"].strip())[0]
            k["cleared"] += score({"known": r["known"], "probe": r["probe"], "detail": first}) < th
    res = {"model": a[0], "threshold": th, "top": top, "runs": dirs, "byMoment": out}
    json.dump(res, open(a[2], "w", encoding="utf-8"), indent=1)
    print(json.dumps(res["byMoment"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
