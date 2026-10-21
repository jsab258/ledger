"""The talk check's first sentence on a small local model, on this PC's CPU (lab test 6, 8 October 2026).

    python -S local_check.py [threshold]    -> F:/LedgerTools/lab/talk/local_<model>.jsonl and a summary

The same labelled sets and selection as ClaimBench's successors run of 7 October
(ledger/ClaimBench/Successors.cs on wip; production/research/invented-claims/SUCCESSORS-2026-10-07.md):
- THE DETAILS: detail-gold.jsonl's held half, labelled stated/implied (true) or added/contradicted
  (invented), noclaim left out: 127 details. Each is put to the checker with the character's known
  facts as the context and the player's probe as the question: true details refused, invented passed.
- THE REPLIES: the held sets of the 28 September bench (drafts.jsonl with gold.jsonl; the sets not in
  ClaimBench's TuneSets), the first 15 invented and first 15 honest by id. Only each reply's FIRST
  SENTENCE goes to the local checker (the part whose check sets the floor of the first sound): first
  sentences of invented replies caught, of honest replies flagged.
The checker is LettuceDetect's TinyLettuce Ettin 68M (KRLabsOrg/tinylettuce-ettin-68m-en, MIT), a token
classifier that marks answer spans the context does not support; a detail or sentence is flagged when
it marks any span. Its own default threshold unless one is given. No tuning on the held sets.
"""
import json
import os
import re
import statistics
import sys
import time

sys.path.insert(0, "F:/LedgerTools/pylib/lettuce")   # run with python -S: everything from this folder, nothing from the PC's site-packages
os.environ.setdefault("HF_HOME", "F:/LedgerTools/hf")
from lettucedetect.models.inference import HallucinationDetector  # noqa: E402

MODEL = "KRLabsOrg/tinylettuce-ettin-68m-en"
BENCH = "F:/LedgerTools/town-scratch/detail-bench/detail-gold.jsonl"
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT = "F:/LedgerTools/lab/talk"
TUNE_SETS = {"saw-window", "heard-vague", "ordinary-day", "the-rank"}


def supported(label):
    return {"stated": True, "implied": True, "added": False, "contradicted": False}.get(label)


def first_sentence(text):
    m = re.search(r"^(.+?[.!?])(\s|$)", text.strip(), re.S)
    return (m.group(1) if m else text).strip()


def wip_file(rel):
    import subprocess
    return subprocess.run(["git", "-C", REPO, "show", "origin/wip:" + rel], capture_output=True, check=True).stdout.decode("utf-8")


def main():
    thr = float(sys.argv[1]) if len(sys.argv) > 1 else None
    os.makedirs(OUT, exist_ok=True)
    t0 = time.perf_counter()
    det = HallucinationDetector(method="transformer", model_path=MODEL)
    load_s = time.perf_counter() - t0

    def check(context, question, answer):
        t = time.perf_counter()
        spans = det.predict(context=context, question=question, answer=answer, output_format="spans")
        dt = time.perf_counter() - t
        if thr is not None:
            spans = [s for s in spans if s.get("confidence", 1.0) >= thr]
        return bool(spans), dt, spans

    rows = [json.loads(l) for l in open(BENCH, encoding="utf-8")]
    rows = sorted([r for r in rows if r["half"] == "held" and supported(r["label"]) is not None], key=lambda r: r["id"])
    out, times = [], []
    tr = fa = ref = pas = 0
    check("warm up", "warm up?", "warm up")
    for r in rows:
        flagged, dt, spans = check(r["known"], r["probe"], r["detail"])
        times.append(dt)
        gold = supported(r["label"])
        if gold:
            tr += 1
            ref += flagged
        else:
            fa += 1
            pas += not flagged
        out.append({"part": "detail", "id": r["id"], "gold_true": gold, "flagged": flagged, "s": round(dt, 4),
                    "spans": [s.get("text") for s in spans][:4]})
    drafts = {json.loads(l)["id"]: json.loads(l) for l in wip_file("production/research/invented-claims/bench/drafts.jsonl").splitlines() if l.strip()}
    gold = [json.loads(l) for l in wip_file("production/research/invented-claims/bench/gold.jsonl").splitlines() if l.strip()]
    gold = sorted([g for g in gold if g["id"] in drafts and drafts[g["id"]]["set"] not in TUNE_SETS], key=lambda g: g["id"])
    pick = [g for g in gold if g["invented"]][:15] + [g for g in gold if not g["invented"]][:15]
    rtimes, tp = [], 0
    fp = inv_n = hon_n = 0
    in_first = 0
    for g in pick:
        d = drafts[g["id"]]
        s1 = first_sentence(d["reply"])
        q = " ".join(d.get("said") or [])
        flagged, dt, spans = check([d["known"]], q, s1)
        rtimes.append(dt)
        if g["invented"]:
            inv_n += 1
            tp += flagged
            # is the invented detail in the first sentence at all? (word overlap, for reading the numbers)
            words = lambda t: set(re.findall(r"[a-z']+", t.lower()))
            hit = any(len(words(x["detail"]) & words(s1)) >= max(2, len(words(x["detail"])) // 2) for x in g.get("details", []))
            in_first += hit
        else:
            hon_n += 1
            fp += flagged
        out.append({"part": "reply_first_sentence", "id": g["id"], "invented": g["invented"], "flagged": flagged,
                    "s": round(dt, 4), "sentence": s1, "spans": [s.get("text") for s in spans][:4]})
    tag = MODEL.split("/")[-1] + ("" if thr is None else "_t%.2f" % thr)
    with open(os.path.join(OUT, "local_%s.jsonl" % tag), "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")

    def tenth(xs):
        xs = sorted(xs)
        return xs[int(0.9 * (len(xs) - 1))]
    summary = {
        "model": MODEL, "threshold": thr if thr is not None else "model default", "load_s": round(load_s, 2),
        "details": {"true_refused": [ref, tr], "invented_passed": [pas, fa],
                    "median_s": round(statistics.median(times), 3), "slowest_tenth_s": round(tenth(times), 3), "slowest_s": round(max(times), 3)},
        "replies_first_sentence": {"invented_caught": [tp, inv_n], "honest_flagged": [fp, hon_n],
                                   "invented_with_the_detail_in_sentence_1": in_first,
                                   "median_s": round(statistics.median(rtimes), 3), "slowest_tenth_s": round(tenth(rtimes), 3), "slowest_s": round(max(rtimes), 3)},
        "cost_usd": 0.0, "cpu_threads": __import__("torch").get_num_threads(),
    }
    json.dump(summary, open(os.path.join(OUT, "summary_%s.json" % tag), "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
