#!/usr/bin/env python3
"""How long the player waits to hear each reply, from the bench's turns, sorted by cause.

    python tools/voice-live/slow_turns.py RUN_DIR [RUN_DIR ...] [--voice 0.2] [--out OUT.json]

WHY, 26 October 2026. His answer, speech 2: "how often a reply waits 5 s or more, measured before and after". The
live "before" (production/research/voice-latency/SENTENCE-REPAIR-2026-10-26.md) had 30 turns, too few to show a
change; the bench (ledger/ClaimBench firsts --early, the game's own settings: rules, plain fallback, the ladder and
its judge, models by moment, the check on Haiku 5.5) gives 60 turns a run through the real engine and the real API,
each with its steps. The voice is not in the bench: all three cast now speak through Pocket, whose first sound
comes about 0.2 s after the sentence is handed over (POCKET-SWITCH-2026-10-26.md, "Darren too"), so --voice adds it.

A TURN IS HEARD at its first sentence's hand-over (firstMs) plus the voice; a turn whose first sentence never passed
(held back: firstMs -1) is heard when the whole turn ends (its fallback or ladder line). CAUSES, from its steps:
"passed" (the first sentence passed its first check), "redraft passed" (refused, the second draft's first sentence
passed), "refused twice" (both refused: the fallback or the ladder), "plain" (the second draft fell back to the plain
line at once).
"""
import json
import os
import statistics
import sys


def cause(steps):
    names = [s["step"] for s in steps]
    if "first-passed" in names:
        return "passed"
    if "re-first-passed" in names:
        return "redraft passed"
    if "re-first-plain" in names:
        return "plain"
    if "re-first-flagged" in names or "first-flagged" in names:
        return "refused twice"
    return "no early sentence"


def score(run_dir, voice):
    rows = [json.loads(l) for l in open(os.path.join(run_dir, "firsts.jsonl"), encoding="utf-8") if l.strip()]
    out = {"run": run_dir, "turns": len(rows), "byCause": {}, "byCard": {}}
    heard = []
    for r in rows:
        at = (r["firstMs"] if r["firstMs"] >= 0 else r["turnMs"]) / 1000.0 + voice
        c = cause(r["steps"])
        heard.append(at)
        b = out["byCause"].setdefault(c, {"turns": 0, "slow": 0})
        b["turns"] += 1
        b["slow"] += at >= 5.0
        k = out["byCard"].setdefault(r["card"], {"turns": 0, "slow": 0, "fallback": 0, "heard": []})
        k["turns"] += 1
        k["slow"] += at >= 5.0
        k["fallback"] += bool(r["fell"])
        k["heard"].append(at)
    for k in out["byCard"].values():
        k["medianHeard"] = round(statistics.median(k.pop("heard")), 2)
    out["slow"] = sum(h >= 5.0 for h in heard)
    out["medianHeard"] = round(statistics.median(heard), 2)
    out["p90Heard"] = round(sorted(heard)[int(len(heard) * 0.9)], 2)
    out["fallback"] = sum(bool(r["fell"]) for r in rows)
    out["firstRefused"] = sum(1 for r in rows if any(s["step"] == "first-flagged" for s in r["steps"]))
    return out


def main(a):
    voice = float(a[a.index("--voice") + 1]) if "--voice" in a else 0.2
    outp = a[a.index("--out") + 1] if "--out" in a else None
    dirs = [d for i, d in enumerate(a) if not d.startswith("--") and (i == 0 or a[i - 1] not in ("--voice", "--out"))]
    res = [score(d, voice) for d in dirs]
    for r in res:
        print("%s: %d turns, heard median %.2f s (p90 %.2f), 5 s or more %d, first sentence refused %d, fallback %d; by cause %s"
              % (os.path.basename(r["run"].rstrip("/\\")), r["turns"], r["medianHeard"], r["p90Heard"], r["slow"],
                 r["firstRefused"], r["fallback"], json.dumps(r["byCause"])))
    if outp:
        json.dump(res, open(outp, "w", encoding="utf-8"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
