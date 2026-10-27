#!/usr/bin/env python3
"""The fast checker's fourth try: the trade-off at three cut-offs, judged as the whole game against Haiku alone.

    PY=C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe
    $PY tools/checkers/tradeoff.py cutoffs MODEL_DIR VAL.json CUTOFFS.json [--top 10] [--int8]
    $PY tools/checkers/tradeoff.py test MODEL_DIR TEST.json HAIKU.jsonl CUTOFFS.json OUT.json [--int8]
    $PY tools/checkers/tradeoff.py firsts MODEL_DIR CUTOFFS.json OUT.json RUN_DIR [RUN_DIR ...] [--int8]

WHY, 27 October 2026. His words that afternoon (production/orders/2026-10-25.md): "judge the whole game (checker first,
then Haiku) on the 617 held sentences against Haiku alone, not on the 42 short details ... Then show me on my page the
trade-off at three cut-offs: share of real first sentences cleared, seconds saved, and invented sentences let through
per 300 against Haiku alone. I decide the cut-off." The design was written down before anything was measured
(production/research/invented-claims/LOCAL-CHECKERS-2026-10-26.md, "Fourth try").

CUTOFFS, on tuning data only (the bench's tuning details and VAL.json, the near-miss sentences kept out of training):
  strict  half the lowest score any invented tuning item gets (the third try's rule);
  middle  the lowest invented tuning score itself;
  open    the score under which 2% of the invented tuning items fall; as coded, the int(2%)-th lowest, so fewer fall
          under it (3 of 227, 1.3%, on 27 October), kept so the recorded results reproduce.
A sentence scoring below the cut-off is cleared and spoken without Haiku.

TEST: each held sentence scored once; at each cut-off the game lets an invented sentence through when the checker clears
it or Haiku (the game's own whole check, HAIKU.jsonl, already run) passes it. Reported per 300 invented sentences, with
the checker and for Haiku alone, the invented ones the checker clears that Haiku refused (for the blind hand reading),
and the true ones it clears with the Haiku check time each would skip.

FIRSTS: the bench's newcomer turns (ledger/ClaimBench firsts runs), a real question's first sentence that passed Haiku,
scored as the game would score it; at each cut-off the share cleared and the seconds saved, each cleared turn's own wait
from its first sentence written to its check passed, less the checker's own time on it.
"""
import json
import os
import re
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import measure_checkers as m  # noqa: E402

NAMES = ("strict", "middle", "open")


def opt(a, n, d):
    return a[a.index(n) + 1] if n in a else d


def scorer(a, model, top):
    return m.lettuce_scorer(model, top, int8="--int8" in a)


def cutoffs(a):
    model, val, out = a[1], a[2], a[3]
    top = int(opt(a, "--top", "10"))
    score = scorer(a, model, top)
    tune, _held = m.rows()
    inv = [score(r) for r in tune if r["invented"]]
    vrows = json.load(open(val, encoding="utf-8"))
    assert all(v.get("half", "tune") == "tune" for v in vrows)
    item = lambda v: {"known": v["context"], "probe": v["question"], "detail": v["answer"]}  # noqa: E731
    vinv = [score(item(v)) for v in vrows if not v["supported"]]
    vtrue = [score(item(v)) for v in vrows if v["supported"]]
    ttrue = [score(r) for r in tune if not r["invented"]]
    allinv = sorted(inv + vinv)
    lowest = allinv[0]
    p2 = allinv[max(0, int(len(allinv) * 0.02) - 1)]
    cuts = {"strict": lowest / 2, "middle": lowest, "open": p2}
    res = {"model": model, "top": top, "int8": "--int8" in a, "invented": len(allinv), "lowestInvented": round(lowest, 6),
           "cutoffs": {k: round(v, 6) for k, v in cuts.items()},
           "rules": {"strict": "half the lowest invented tuning score", "middle": "the lowest invented tuning score",
                     "open": "the score under which 2% of the invented tuning items fall"},
           "tuningInventedCleared": {k: sum(s < v for s in allinv) for k, v in cuts.items()},
           "tuningTrueCleared": {k: sum(s < v for s in vtrue + ttrue) for k, v in cuts.items()},
           "tuningTrue": len(vtrue + ttrue)}
    json.dump(res, open(out, "w", encoding="utf-8"), indent=1)
    print(json.dumps(res))


def test(a):
    model, test_json, haiku, cut_json, out = a[1], a[2], a[3], a[4], a[5]
    cut = json.load(open(cut_json, encoding="utf-8"))
    score = scorer(a, model, cut["top"])
    rows = json.load(open(test_json, encoding="utf-8"))
    assert all(r.get("half") == "held" for r in rows), "a sentence that is not from the held half"
    hv = {}
    for line in open(haiku, encoding="utf-8"):
        if line.strip():
            h = json.loads(line)
            hv[(h["key"], h["sentence"])] = h
    scored, missing, times = [], 0, []
    for r in rows:
        h = hv.get((r.get("key", ""), r["answer"]))
        if h is None:
            missing += 1
            continue
        t0 = time.perf_counter()
        s = score({"known": r["context"], "probe": r["question"], "detail": r["answer"]})
        times.append(time.perf_counter() - t0)
        scored.append((r, h, s))
    inv = [x for x in scored if not x[0]["supported"]]
    tru = [x for x in scored if x[0]["supported"]]
    haiku_alone = sum(h["passed"] for _r, h, _s in inv)
    res = {"model": model, "top": cut["top"], "int8": cut.get("int8", False), "sentences": len(scored), "invented": len(inv),
           "true": len(tru), "noHaikuVerdict": missing, "haikuAloneThrough": haiku_alone,
           "haikuAlonePer300": round(300.0 * haiku_alone / len(inv), 1), "checkerSecondsMedian": round(statistics.median(times), 4),
           "byCutoff": {}}
    for name in NAMES:
        c = cut["cutoffs"][name]
        through = sum((s < c) or h["passed"] for _r, h, s in inv)
        extra = [r["answer"] for r, h, s in inv if s < c and not h["passed"]]
        cleared_true = [(r, h) for r, h, s in tru if s < c]
        res["byCutoff"][name] = {
            "cutoff": c, "withCheckerThrough": through, "withCheckerPer300": round(300.0 * through / len(inv), 1),
            "checkerClearedInvented": sum(s < c for _r, _h, s in inv), "checkerClearedInventedHaikuRefused": extra,
            "trueCleared": len(cleared_true), "trueClearedShare": round(len(cleared_true) / len(tru), 3),
            "trueClearedHaikuSecondsMedian": round(statistics.median([h["ms"] for _r, h in cleared_true]) / 1000.0, 2) if cleared_true else None,
            "trueClearedSentences": [r["answer"] for r, _h in cleared_true]}
    rowsout = [{"key": r.get("key"), "card": r.get("card"), "question": r["question"], "sentence": r["answer"],
                "invented": not r["supported"], "haikuPassed": h["passed"], "haikuMs": h.get("ms"), "checkerScore": round(s, 6)}
               for r, h, s in scored]
    json.dump({"summary": res, "rows": rowsout}, open(out, "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "byCutoff"}))
    for name in NAMES:
        b = res["byCutoff"][name]
        print(name, json.dumps({k: v for k, v in b.items() if k not in ("trueClearedSentences", "checkerClearedInventedHaikuRefused")}),
              "extra invented:", len(b["checkerClearedInventedHaikuRefused"]))


def firsts(a):
    model, cut_json, out = a[1], a[2], a[3]
    dirs = [d for d in a[4:] if not d.startswith("--")]
    cut = json.load(open(cut_json, encoding="utf-8"))
    score = scorer(a, model, cut["top"])
    turns = []
    for d in dirs:
        for line in open(os.path.join(d, "firsts.jsonl"), encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if "haiku" in (r.get("model") or ""):
                continue  # small talk: reported apart, by his ruling of 26 October (the bar is real questions)
            steps = {s["step"]: s["ms"] for s in r["steps"]}
            t = {"run": os.path.basename(d), "passed": "first-passed" in steps}
            if t["passed"]:
                first = re.split(r"(?<=[.!?])\s+", r["reply"].strip())[0]
                t0 = time.perf_counter()
                t["score"] = score({"known": r["known"], "probe": r["probe"], "detail": first})
                t["checkerS"] = time.perf_counter() - t0
                t["waitS"] = (steps["first-passed"] - steps.get("first-written", steps["first-passed"])) / 1000.0
            turns.append(t)
    passed = [t for t in turns if t["passed"]]
    res = {"model": model, "runs": dirs, "realQuestionTurns": len(turns), "firstPassed": len(passed), "byCutoff": {}}
    for name in NAMES:
        c = cut["cutoffs"][name]
        cl = [t for t in passed if t["score"] < c]
        saved = [max(0.0, t["waitS"] - t["checkerS"]) for t in cl]
        res["byCutoff"][name] = {"cutoff": c, "cleared": len(cl), "clearedShareOfPassed": round(len(cl) / len(passed), 3) if passed else 0,
                                 "secondsSavedMedianPerCleared": round(statistics.median(saved), 2) if saved else 0,
                                 "secondsSavedPerRealQuestion": round(sum(saved) / len(turns), 3) if turns else 0}
    json.dump(res, open(out, "w", encoding="utf-8"), indent=1)
    print(json.dumps(res["byCutoff"]))


if __name__ == "__main__":
    a = sys.argv[1:]
    {"cutoffs": cutoffs, "test": test, "firsts": firsts}[a[0]](a)
