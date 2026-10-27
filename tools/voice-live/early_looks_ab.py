"""Score a `sentcheck --ab-early` run: the check's time with its second looks started as the list is written
(ClaimCheck.EarlyLooks) and without, on the same sentences, and whether the verdicts agree.

    python tools/voice-live/early_looks_ab.py F:/LedgerTools/town-scratch/slow-replies/early-looks/ab.jsonl

The check is not deterministic (the model answers afresh each time), so verdicts are compared as two runs of the same
check would be: how often the two disagree, in each direction, against how often two runs with the switch off
disagree on the same sentences (haiku-verdicts.jsonl, 26 October night, when given with --before).
"""
import json
import sys


def q(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))] if xs else None


def main(path, before=None):
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    print("sentences: %d" % len(rows))
    for label, pick in (("all", lambda r: True),
                        ("needed a look (off made 2+ calls)", lambda r: r["callsOff"] >= 2),
                        ("cleared by the list alone (off made 1 call)", lambda r: r["callsOff"] == 1)):
        sub = [r for r in rows if pick(r)]
        if not sub:
            continue
        off = [r["msOff"] for r in sub]
        on = [r["msOn"] for r in sub]
        saved = [r["msOff"] - r["msOn"] for r in sub]
        print("%s (%d): off median %d, slowest tenth from %d | on median %d, slowest tenth from %d | saved per sentence, median %d"
              % (label, len(sub), q(off, .5), q(off, .9), q(on, .5), q(on, .9), q(saved, .5)))
    for who in (True, False):
        sub = [r for r in rows if r["earlyFirst"] == who]
        print("  checked %s first (%d): off median %d, on median %d"
              % ("on" if who else "off", len(sub), q([r["msOff"] for r in sub], .5), q([r["msOn"] for r in sub], .5)))
    both = sum(1 for r in rows if r["passedOff"] == r["passedOn"])
    off_only = sum(1 for r in rows if r["passedOff"] and not r["passedOn"])
    on_only = sum(1 for r in rows if r["passedOn"] and not r["passedOff"])
    print("verdicts: same %d, passed off only %d, passed on only %d" % (both, off_only, on_only))
    print("passed: off %d, on %d" % (sum(r["passedOff"] for r in rows), sum(r["passedOn"] for r in rows)))
    print("calls: off %d, on %d" % (sum(r["callsOff"] for r in rows), sum(r["callsOn"] for r in rows)))
    if before:
        prev = {}
        for l in open(before, encoding="utf-8"):
            if l.strip():
                x = json.loads(l)
                prev[(x["key"], x["sentence"])] = x["passed"]
        # a key covers the ten or so sentences of one request: a sentence is its key and its words
        shared = [r for r in rows if (r["key"], r["sentence"]) in prev]
        flips = sum(1 for r in shared if prev[(r["key"], r["sentence"])] != r["passedOff"])
        print("two runs with the switch off (26 October night and tonight) disagree on %d of %d" % (flips, len(shared)))


if __name__ == "__main__":
    args = sys.argv[1:]
    before = None
    if "--before" in args:
        before = args[args.index("--before") + 1]
        args = [a for a in args if a not in ("--before", before)]
    main(args[0], before)
