"""Score a ClaimBench `lookpairs` run: would a second copy of a slow check call (a hedged request) cut the slow tail?

    python tools/voice-live/hedge_pairs.py F:/LedgerTools/town-scratch/slow-replies/early-looks/pairs.jsonl

Each row is one call (the check's list, or one refused detail's second look) sent twice at the same moment, each
copy's first words and end timed. A hedge sent after a delay d is simulated as the second copy started d later
(Dean and Barroso's hedged request, "The Tail at Scale", 2013), and the copy that starts answering first is the one
kept, its end the call's time: chosen before any of its answer can be read, so it cannot favour one verdict over
another by the answer's length. Read beside that: whether the copies are slow together (the paper's own caveat), and
whether, when the two copies disagree, the one that starts first leans to one verdict.
"""
import json
import random
import sys


def q(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))] if xs else 0


def hedged(r, d):
    """The call's time with a second copy sent d ms after the first, if the first has not started answering by then."""
    if r["first1"] <= d:
        return r["end1"], False
    f2, e2 = d + r["first2"], d + r["end2"]
    return (r["end1"], True) if r["first1"] <= f2 else (e2, True)


def rank_corr(a, b):
    def ranks(x):
        order = sorted(range(len(x)), key=lambda i: x[i])
        rk = [0] * len(x)
        for n, i in enumerate(order):
            rk[i] = n
        return rk
    ra, rb = ranks(a), ranks(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    va = sum((x - ma) ** 2 for x in ra) ** .5
    vb = sum((y - mb) ** 2 for y in rb) ** .5
    return cov / (va * vb) if va and vb else 0


def main(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    rows = [r for r in rows if r["first1"] >= 0 and r["first2"] >= 0]
    for call in ("list", "look"):
        sub = [r for r in rows if r["call"] == call]
        if not sub:
            continue
        print("== %s: %d pairs" % (call, len(sub)))
        firsts = [r["first1"] for r in sub] + [r["first2"] for r in sub]
        ends = [r["end1"] for r in sub] + [r["end2"] for r in sub]
        print("one copy: first words median %d, slowest tenth from %d; end median %d, slowest tenth from %d"
              % (q(firsts, .5), q(firsts, .9), q(ends, .5), q(ends, .9)))
        print("the two copies' first words, rank correlation %.2f; ends %.2f"
              % (rank_corr([r["first1"] for r in sub], [r["first2"] for r in sub]),
                 rank_corr([r["end1"] for r in sub], [r["end2"] for r in sub])))
        slow = q(firsts, .9)
        p1 = sum(r["first1"] >= slow for r in sub) / len(sub)
        both = sum(r["first1"] >= slow and r["first2"] >= slow for r in sub) / len(sub)
        print("both copies in the slowest tenth: %.3f of pairs (%.3f if independent)" % (both, p1 * p1))
        for label, d in (("at once", 0), ("after the median first word", q(firsts, .5)),
                         ("after the 75th percentile", q(firsts, .75)), ("after the 90th", q(firsts, .9))):
            t = [hedged(r, d) for r in sub]
            times = [x[0] for x in t]
            sent = sum(1 for x in t if x[1]) / len(t)
            print("  hedge %-28s (%4d ms): end median %d, slowest tenth from %d; second copies sent %.0f%%"
                  % (label, d, q(times, .5), q(times, .9), 100 * sent))
        if all(r.get("begin1", -1) >= 0 and r.get("begin2", -1) >= 0 for r in sub):
            # THE RACE ON THE MODEL'S BEGINNING (ClaimCheck.TwoCopies since the fresh review of 27 October): the copy
            # the model takes up first, its thinking included, is kept, chosen before either has a word of its answer.
            begins = [r["begin1"] for r in sub] + [r["begin2"] for r in sub]
            gap = [r["first1"] - r["begin1"] for r in sub] + [r["first2"] - r["begin2"] for r in sub]
            print("one copy: the model begins at median %d, slowest tenth from %d; from beginning to first words median %d"
                  % (q(begins, .5), q(begins, .9), q(gap, .5)))
            print("the two copies' beginnings, rank correlation %.2f" % rank_corr([r["begin1"] for r in sub], [r["begin2"] for r in sub]))
            kept = [r["end1"] if r["begin1"] <= r["begin2"] else r["end2"] for r in sub]
            print("  two at once, the one begun first kept: end median %d, slowest tenth from %d" % (q(kept, .5), q(kept, .9)))
            if call == "look":
                dis = [r for r in sub if r["ok1"] is not None and r["ok2"] is not None and r["ok1"] != r["ok2"]]
                first_ok = sum(1 for r in dis if (r["ok1"] if r["begin1"] <= r["begin2"] else r["ok2"]))
                print("  where the copies disagree (%d), the copy begun first says supported %d times" % (len(dis), first_ok))
        if call == "look":
            dis = [r for r in sub if r["ok1"] is not None and r["ok2"] is not None and r["ok1"] != r["ok2"]]
            agree = sum(1 for r in sub if r["ok1"] is not None and r["ok1"] == r["ok2"])
            first_ok = sum(1 for r in dis if (r["ok1"] if r["first1"] <= r["first2"] else r["ok2"]))
            print("verdicts: the copies agree on %d, disagree on %d; where they disagree, the copy that starts first "
                  "says supported %d times, not supported %d" % (agree, len(dis), first_ok, len(dis) - first_ok))

    # The whole check of a sentence that needs looks: its list, then its looks side by side (the slowest decides).
    # The run writes each sentence's list row, then its looks' rows.
    print("== the whole check, list then its looks (sentences with at least one refused detail)")
    order = []
    for r in rows:
        if r["call"] == "list":
            order.append([r, []])
        elif order:
            order[-1][1].append(r)
    with_looks = [(l, ls) for l, ls in order if ls]
    for label, d in (("none", None), ("at once", 0), ("after 75th percentile", "p75")):
        times = []
        for l, ls in with_looks:
            def t(r, kind):
                if d is None:
                    return r["end1"]
                dd = d if d != "p75" else q([x["first1"] for x in rows if x["call"] == kind] + [x["first2"] for x in rows if x["call"] == kind], .75)
                return hedged(r, dd)[0]
            times.append(t(l, "list") + max(t(x, "look") for x in ls))
        print("  hedge %-22s: median %d, slowest tenth from %d (%d sentences)" % (label, q(times, .5), q(times, .9), len(times)))


if __name__ == "__main__":
    main(sys.argv[1])
