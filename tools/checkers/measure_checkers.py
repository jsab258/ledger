#!/usr/bin/env python3
"""The open fact checkers on the labelled details, the way Haiku was measured: how many invented details each lets
through, how many true ones it clears, and how long it takes.

    C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe tools/checkers/measure_checkers.py OUT.json [--only NAME]

WHY, 26 October 2026. His answer, speech 1: "a small checker on this PC clears only the sentences it is sure are
supported; everything else waits for Haiku ... compare open checkers ... on the same 127 labelled details Haiku was
measured on". Haiku lets 1 of the 42 invented details through (production/research/invented-claims/
SUCCESSORS-2026-10-07.md). The checker's job is narrower than Haiku's: only to clear what it is sure of; whatever it
does not clear goes to Haiku, so a strict threshold costs speed, never safety.

THE DATA: F:/LedgerTools/town-scratch/detail-bench/detail-gold.jsonl (255 details, each with the speaker's known
facts, the player's question, the detail and two labellers' label). True = stated or implied; invented = added or
contradicted; noclaim is left out. The "held" half is the test (127: 85 true, 42 invented) and is never used to
choose anything; the "tune" half (121) sets each checker's threshold: the most lenient one at which no invented
tuning detail is cleared.

THE CHECKERS (downloaded 26 October with his yes; F:/LedgerTools/hf): KR Labs' TinyLettuce (17M, 32M, 68M) and
LettuceDetect base (MIT), token classifiers that mark unsupported answer tokens (a detail's score: the highest
token's probability of being unsupported); Vectara's HHEM-2.1-Open (Apache 2.0), a pair classifier giving a
consistency score (a detail's score: 1 minus it). The package that runs the KR Labs models is installed apart, in
F:/LedgerTools/checkers/pkgs, so the voice environment it borrows is not changed.

THE TIMES here are the checker alone on this PC's processor; his bar (0.15 s beside the running game, no frame
stalls) is measured separately, with the game open.
"""
import json
import os
import statistics
import sys
import time

sys.path.insert(0, r"F:\LedgerTools\checkers\pkgs")
os.environ.setdefault("HF_HOME", r"F:\LedgerTools\hf")
GOLD = r"F:\LedgerTools\town-scratch\detail-bench\detail-gold.jsonl"
TRUE, INVENTED = {"stated", "implied"}, {"added", "contradicted"}
LETTUCE = {"tinylettuce-17m": "KRLabsOrg/tinylettuce-ettin-17m-en", "tinylettuce-32m": "KRLabsOrg/tinylettuce-ettin-32m-en",
           "tinylettuce-68m": "KRLabsOrg/tinylettuce-ettin-68m-en", "lettucedetect-base": "KRLabsOrg/lettucedect-base-modernbert-en-v1"}


def rows():
    out = []
    for line in open(GOLD, encoding="utf-8"):
        r = json.loads(line)
        if r["label"] in TRUE or r["label"] in INVENTED:
            r["invented"] = r["label"] in INVENTED
            out.append(r)
    return [r for r in out if r["half"] == "tune"], [r for r in out if r["half"] == "held"]


def lettuce_scorer(path):
    from lettucedetect.models.inference import HallucinationDetector
    det = HallucinationDetector(method="transformer", model_path=path)

    def score(r):
        toks = det.predict(context=r["known"], question=r["probe"], answer=r["detail"], output_format="tokens")
        return max((t["prob"] for t in toks), default=1.0)
    return score


def hhem_scorer():
    from transformers import AutoModelForSequenceClassification
    m = AutoModelForSequenceClassification.from_pretrained("vectara/hallucination_evaluation_model", trust_remote_code=True)
    m.eval()

    def score(r):
        return 1.0 - float(m.predict([("\n".join(r["known"]), r["detail"])])[0])
    return score


def threshold(tune_scores):
    """The highest score below which no invented tuning detail falls: everything under it is cleared."""
    inv = [s for s, r in tune_scores if r["invented"]]
    return min(inv) if inv else 1.0


def run(name, scorer, tune, held):
    t0 = time.time()
    ts = [(scorer(r), r) for r in tune]
    th = threshold(ts)
    times, hs = [], []
    for r in held:
        a = time.perf_counter()
        s = scorer(r)
        times.append(time.perf_counter() - a)
        hs.append((s, r))
    cleared = [r for s, r in hs if s < th]
    out = {"checker": name, "threshold": round(th, 4),
           "heldInventedCleared": sum(r["invented"] for r in cleared), "heldInvented": sum(r["invented"] for _, r in hs),
           "heldTrueCleared": sum(not r["invented"] for r in cleared), "heldTrue": sum(not r["invented"] for _, r in hs),
           "tuneTrueCleared": sum(1 for s, r in ts if s < th and not r["invented"]),
           "secondsMedian": round(statistics.median(times), 3), "secondsSlowestTenth": round(sorted(times)[int(len(times) * 0.9)], 3),
           "inventedClearedIds": [r["id"] for r in cleared if r["invented"]], "minutes": round((time.time() - t0) / 60, 1)}
    print(json.dumps(out), flush=True)
    return out


def main(argv):
    tune, held = rows()
    only = argv[argv.index("--only") + 1] if "--only" in argv else None
    results = []
    for name, path in LETTUCE.items():
        if only and only != name:
            continue
        results.append(run(name, lettuce_scorer(path), tune, held))
    if not only or only == "hhem":
        results.append(run("hhem-2.1-open", hhem_scorer(), tune, held))
    json.dump({"tune": len(tune), "held": len(held), "results": results}, open(argv[0], "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
