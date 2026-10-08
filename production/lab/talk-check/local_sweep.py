"""The local checker's threshold, chosen on the TUNING half only, then scored once on the held half.

    python -S local_sweep.py   -> F:/LedgerTools/lab/talk/sweep.json

For each labelled detail (both halves) the checker's highest token probability of "unsupported" is
kept. On the tuning half the threshold is the one that passes no more invented details than Haiku 5.5's
best on that half (2 of 50, the split) while refusing the fewest true ones; that threshold is then
applied, unchanged, to the held half. The reply first sentences are scored at the same threshold.
"""
import json
import os
import re
import statistics
import sys
import time

sys.path.insert(0, "F:/LedgerTools/pylib/lettuce")
os.environ.setdefault("HF_HOME", "F:/LedgerTools/hf")
from lettucedetect.models.inference import HallucinationDetector  # noqa: E402
import local_check as L  # noqa: E402


def main():
    det = HallucinationDetector(method="transformer", model_path=L.MODEL)

    def score(context, question, answer):
        t = time.perf_counter()
        toks = det.predict(context=context, question=question, answer=answer, output_format="tokens")
        dt = time.perf_counter() - t
        p = max([x.get("prob", 0.0) for x in toks] or [0.0])
        return p, dt
    rows = [json.loads(l) for l in open(L.BENCH, encoding="utf-8")]
    rows = sorted([r for r in rows if L.supported(r["label"]) is not None], key=lambda r: r["id"])
    res = []
    score("warm up", "warm up?", "warm up")
    for r in rows:
        p, dt = score(r["known"], r["probe"], r["detail"])
        res.append({"id": r["id"], "half": r["half"], "true": L.supported(r["label"]), "p": p, "s": dt})
    tune = [x for x in res if x["half"] == "tune"]
    held = [x for x in res if x["half"] == "held"]
    best = None
    for thr in sorted({round(x["p"], 4) for x in tune} | {0.5}):
        passed = sum(1 for x in tune if not x["true"] and x["p"] < thr)
        refused = sum(1 for x in tune if x["true"] and x["p"] >= thr)
        if passed <= 2 and (best is None or refused < best[2]):
            best = (thr, passed, refused)
    thr = best[0] if best else 0.5

    def tally(xs):
        tr = sum(1 for x in xs if x["true"]); fa = len(xs) - tr
        return {"true_refused": [sum(1 for x in xs if x["true"] and x["p"] >= thr), tr],
                "invented_passed": [sum(1 for x in xs if not x["true"] and x["p"] < thr), fa],
                "median_s": round(statistics.median([x["s"] for x in xs]), 3),
                "slowest_tenth_s": round(sorted(x["s"] for x in xs)[int(0.9 * (len(xs) - 1))], 3),
                "slowest_s": round(max(x["s"] for x in xs), 3)}
    out = {"threshold_chosen_on_tune": thr, "tune": tally(tune), "held": tally(held)}
    # the reply first sentences at that threshold
    drafts = {json.loads(l)["id"]: json.loads(l) for l in L.wip_file("production/research/invented-claims/bench/drafts.jsonl").splitlines() if l.strip()}
    gold = [json.loads(l) for l in L.wip_file("production/research/invented-claims/bench/gold.jsonl").splitlines() if l.strip()]
    gold = sorted([g for g in gold if g["id"] in drafts and drafts[g["id"]]["set"] not in L.TUNE_SETS], key=lambda g: g["id"])
    pick = [g for g in gold if g["invented"]][:15] + [g for g in gold if not g["invented"]][:15]
    tp = fp = 0
    rs = []
    for g in pick:
        d = drafts[g["id"]]
        p, dt = score([d["known"]], " ".join(d.get("said") or []), L.first_sentence(d["reply"]))
        rs.append(dt)
        if g["invented"]:
            tp += p >= thr
        else:
            fp += p >= thr
    out["replies_first_sentence"] = {"invented_caught": [tp, 15], "honest_flagged": [fp, 15],
                                     "median_s": round(statistics.median(rs), 3), "slowest_s": round(max(rs), 3)}
    json.dump({"summary": out, "rows": res}, open(os.path.join(L.OUT, "sweep.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
