#!/usr/bin/env python3
"""The fast checker and the game's Haiku check, side by side, on whole first sentences: the third try's test.

    C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe tools/checkers/sentence_test.py cutoff MODEL_DIR VAL.json OUT.json [--top 10]
    C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe tools/checkers/sentence_test.py test MODEL_DIR TEST.json HAIKU.jsonl CUTOFF.json OUT.json

WHY, 26 October 2026 (night). His page answer on the second try (2 of 42 invented details through with the checker in
front of Haiku, against Haiku's 1): a third try with more facts read, training aimed at near misses, "Then set the
confidence cut-off so it clears only what it is sure of. Enlarge the held-out test with a few hundred more invented
and true first sentences, labelled by Gemini and spot-checked, so the bar is not decided by one sentence. The bar
stays: no more invented details through than Haiku, on that larger test."

THE CUT-OFF, FIXED BEFORE THE TEST IS RUN (cutoff): on tuning data only (the bench's 111 tuning details and VAL.json,
tuning-context sentences kept out of training), the lowest score any invented item gets is the most convincing
invention seen; the cut-off is HALF of it, so the checker clears only sentences it scores well below anything invented
it has met. Written to CUTOFF.json with what it was set on.

THE TEST (test): TEST.json's sentences come from the held contexts only (never trained on, never used to set
anything), labelled by Gemini 3.8 Flash; HAIKU.jsonl is the game's own check on each (ledger/ClaimBench sentcheck).
  Haiku alone:   an invented sentence gets through when Haiku passes it.
  With checker:  it gets through when the checker clears it OR Haiku passes it (the checker answers first; what it
                 clears is spoken without Haiku).
The bar holds when "with checker" lets through no more invented sentences than "Haiku alone": that is, the checker
clears no invented sentence that Haiku refuses. Also counted: the true sentences the checker clears (the turns heard
sooner), and the true sentences Haiku refuses (its false alarms, his parallel question).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import measure_checkers as m  # noqa: E402

HAIKU127 = "F:/LedgerTools/town-scratch/talk-ladder/successors/successors-run3.jsonl"
HAIKU127_SPEC = "claude-haiku-5-5:disabled::adaptive:low"


def scorer(model, top):
    return m.lettuce_scorer(model, top)


def cutoff(a):
    model, val, out = a[1], a[2], a[3]
    top = int(a[a.index("--top") + 1]) if "--top" in a else 10
    score = scorer(model, top)
    tune, _held = m.rows()
    inv = [score(r) for r in tune if r["invented"]]
    vrows = json.load(open(val, encoding="utf-8"))
    assert all(v.get("half", "tune") == "tune" for v in vrows)
    vinv = [score({"known": v["context"], "probe": v["question"], "detail": v["answer"]}) for v in vrows if not v["supported"]]
    vtrue = [score({"known": v["context"], "probe": v["question"], "detail": v["answer"]}) for v in vrows if v["supported"]]
    lowest = min(inv + vinv)
    cut = lowest / 2
    res = {"model": model, "top": top, "rule": "half the lowest score of any invented tuning item",
           "lowestInvented": round(lowest, 6), "cutoff": round(cut, 6),
           "tuneDetailsInvented": len(inv), "valInvented": len(vinv), "valTrue": len(vtrue),
           "valTrueCleared": sum(s < cut for s in vtrue),
           "tuneTrueDetailsCleared": sum(1 for r in tune if not r["invented"] and score(r) < cut)}
    json.dump(res, open(out, "w", encoding="utf-8"), indent=1)
    print(json.dumps(res))


def test(a):
    model, test_json, haiku, cut_json, out = a[1], a[2], a[3], a[4], a[5]
    cut = json.load(open(cut_json, encoding="utf-8"))
    score = scorer(model, cut["top"])
    rows = json.load(open(test_json, encoding="utf-8"))
    assert all(r.get("half") == "held" for r in rows), "a sentence that is not from the held half"
    hv = {}
    for line in open(haiku, encoding="utf-8"):
        if line.strip():
            h = json.loads(line)
            hv[(h["key"], h["sentence"])] = h
    res = {"model": model, "cutoff": cut["cutoff"], "top": cut["top"], "sentences": 0, "invented": 0, "true": 0,
           "haikuAloneThrough": 0, "withCheckerThrough": 0, "checkerClearedInvented": 0, "checkerClearedInventedHaikuRefused": [],
           "checkerClearedTrue": 0, "haikuRefusedTrue": 0, "noHaikuVerdict": 0}
    detail = []
    for r in rows:
        h = hv.get((r.get("key", ""), r["answer"]))
        if h is None:
            res["noHaikuVerdict"] += 1
            continue
        s = score({"known": r["context"], "probe": r["question"], "detail": r["answer"]})
        cleared = s < cut["cutoff"]
        invented = not r["supported"]
        res["sentences"] += 1
        res["invented" if invented else "true"] += 1
        if invented:
            res["haikuAloneThrough"] += h["passed"]
            res["withCheckerThrough"] += cleared or h["passed"]
            res["checkerClearedInvented"] += cleared
            if cleared and not h["passed"]:
                res["checkerClearedInventedHaikuRefused"].append(r["answer"])
        else:
            res["checkerClearedTrue"] += cleared
            res["haikuRefusedTrue"] += not h["passed"]
        detail.append({"sentence": r["answer"], "card": r.get("card"), "question": r["question"], "invented": invented,
                       "geminiUnsupported": [r["answer"][l["start"]:l["end"]] for l in r["labels"]],
                       "haikuPassed": h["passed"], "haikuFound": h.get("found"), "checkerScore": round(s, 6), "checkerCleared": cleared})
    # THE 127 HELD DETAILS TOO, under the same cut-off, against Haiku as the game runs it (Haiku 5.5, thinking off:
    # successors-run3, which lets d062 through), so the enlarged test is the old one plus the new sentences.
    haiku127 = {}
    for line in open(HAIKU127, encoding="utf-8"):
        if line.strip():
            h = json.loads(line)
            if h.get("part") == "detail" and h.get("Half") == "held" and h.get("spec") == HAIKU127_SPEC:
                haiku127[h["Id"]] = h["passed"]
    _tune, held = m.rows()
    d = {"invented": 0, "haikuAloneThrough": 0, "withCheckerThrough": 0, "checkerClearedInventedHaikuRefused": [], "checkerClearedTrue": 0, "true": 0}
    for r in held:
        cleared = score(r) < cut["cutoff"]
        hp = haiku127.get(r["id"], False)
        if r["invented"]:
            d["invented"] += 1
            d["haikuAloneThrough"] += hp
            d["withCheckerThrough"] += cleared or hp
            if cleared and not hp:
                d["checkerClearedInventedHaikuRefused"].append(r["id"])
        else:
            d["true"] += 1
            d["checkerClearedTrue"] += cleared
    res["held127"] = d
    res["barHolds"] = (res["withCheckerThrough"] + d["withCheckerThrough"]) <= (res["haikuAloneThrough"] + d["haikuAloneThrough"])
    json.dump({"summary": res, "rows": detail}, open(out, "w", encoding="utf-8"), indent=1)
    print(json.dumps(res))


if __name__ == "__main__":
    a = sys.argv[1:]
    {"cutoff": cutoff, "test": test}[a[0]](a)
