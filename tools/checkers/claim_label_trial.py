#!/usr/bin/env python3
"""THE CLAIM CHECK'S LABELS BY A SCRIPTED LABELLER, ON THE API CREDIT: STAGE 1, MEASURED AGAINST THE GOLD.

    python tools/checkers/claim_label_trial.py --make OUT/requests.jsonl      # the 238 requests (no key, no call)
    python tools/checkers/claim_label_trial.py --score OUT/answers.jsonl      # agreement against the gold, the bar
    python tools/checkers/claim_label_trial.py --selftest

WHY, 3 November 2026 (n02-6-4-bulk-api; production/research/bulk-api/PLAN-2026-11-02.md, its first use; the trial's
spec, written before any call: production/research/bulk-api/CLAIM-LABELS-SPEC-2026-11-03.md). Every labelled detail of
the claim-check bench (F:/LedgerTools/town-scratch/detail-bench/detail-gold.jsonl, 255 rows of DetailBench.cs; the 17
"noclaim" left out, so 238: 111 tune, 127 held) is put to Haiku 5.5 through tools/api_batch.py in the bench's own form:
DetailBench.cs's DetailRule word for word as the system text, the speaker's numbered facts and the detail as the one
message (no question, no check verdict). --score reads the answers back and measures, held and tune apart: the exact
label; the line that matters, supported (stated, implied) against not (added, contradicted); invented details called
supported; d062 (the one invented detail Haiku's check passes); the disputed rows (the first two labellers split)
against the rest. The bar, inferred (no source sets one): on the 127 held, at least 115 on the supported line and at
most 2 of the held invented called supported. Labels made this way measure a checker and never train one
(LOCAL-CHECKERS-2026-10-26.md, section 4).
"""
import json
import os
import sys

GOLD = "F:/LedgerTools/town-scratch/detail-bench/detail-gold.jsonl"
MODEL = "claude-haiku-5-5"
MAX_TOKENS = 1500
# DetailBench.cs DetailRule, word for word (ledger/ClaimBench/DetailBench.cs 195-201), and the spec's one added line
DETAIL_RULE = (
    "You judge one detail a character in a small British port town in 1990 said, against everything they know, given as numbered items. "
    "Label it: \"stated\" (an item says it, in any words); \"implied\" (a plain listener would take an item to mean the same thing, or it "
    "follows directly from one); \"added\" (it gives something no item gives: a name, time, day, place, number, colour, size, manner, "
    "habit, deed or happening); \"contradicted\" (an item says otherwise); \"noclaim\" (it states nothing that could be true or false: a "
    "feeling, an opinion, a greeting). Also give its kind: name, number, time, day, place, vehicle, person, event, manner, habit, object "
    "or other. Answer with JSON only: {\"label\": \"stated\", \"kind\": \"event\", \"item\": \"H3\"}.")
FIRST = "Give the JSON first, on one line, and write nothing after it."
BAR_SUPPORTED_LINE = 115     # of the 127 held (9 in 10)
BAR_INVENTED_PASSED = 2      # of the held invented called supported
SUPPORTED = {"stated": True, "implied": True, "added": False, "contradicted": False}


def gold(path=GOLD):
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    return [r for r in rows if r.get("label") != "noclaim"]


def request(r):
    # the bench's own form: DetailBench.cs Numbered() joins the facts by newlines and ends with one
    msg = "WHAT THEY KNOW:\n" + "\n".join(r["known"]) + "\n" + "\nTHE DETAIL:\n" + r["detail"]
    return {"id": r["id"], "model": MODEL, "system": DETAIL_RULE + " " + FIRST,
            "messages": [{"role": "user", "content": msg}], "max_tokens": MAX_TOKENS}


def parse(text):
    """The label of an answer whose JSON comes first; None when it cannot be read."""
    if not text:
        return None
    a = text.find("{")
    b = text.find("}", a)
    if a < 0 or b < 0:
        return None
    try:
        lab = str(json.loads(text[a:b + 1]).get("label", "")).strip().lower()
    except ValueError:
        return None
    return lab if lab in SUPPORTED or lab == "noclaim" else None


def score(answers, rows):
    by = {a["id"]: parse(a.get("text")) for a in answers}
    out = {}
    for half in ("held", "tune"):
        hs = [r for r in rows if r["half"] == half]
        got = [(r, by.get(r["id"])) for r in hs]
        unread = sum(1 for _, g in got if g is None)
        exact = sum(1 for r, g in got if g == r["label"])
        line = sum(1 for r, g in got if g in SUPPORTED and SUPPORTED[g] == SUPPORTED[r["label"]])
        invented = [(r, g) for r, g in got if not SUPPORTED[r["label"]]]
        passed = sum(1 for r, g in invented if g in SUPPORTED and SUPPORTED[g])
        disputed = [(r, g) for r, g in got if len([x for x in (r.get("labels") or []) if x]) > 2]
        undisputed = [(r, g) for r, g in got if (r, g) not in disputed]
        out[half] = {"rows": len(hs), "unread": unread, "exact": exact, "supportedLine": line,
                     "invented": len(invented), "inventedCalledSupported": passed,
                     "disputedRows": len(disputed),
                     "disputedLine": sum(1 for r, g in disputed if g in SUPPORTED and SUPPORTED[g] == SUPPORTED[r["label"]]),
                     "undisputedLine": sum(1 for r, g in undisputed if g in SUPPORTED and SUPPORTED[g] == SUPPORTED[r["label"]])}
    out["d062"] = by.get("d062")
    h = out["held"]
    out["barMet"] = h["supportedLine"] >= BAR_SUPPORTED_LINE and h["inventedCalledSupported"] <= BAR_INVENTED_PASSED and h["unread"] <= 0.05 * h["rows"]
    return out


def selftest():
    ok = []
    rows = [{"id": "a", "half": "held", "label": "stated", "detail": "x", "known": ["C1: y"], "labels": ["stated", "stated", None]},
            {"id": "b", "half": "held", "label": "added", "detail": "z", "known": ["C1: y"], "labels": ["added", "implied", "added"]},
            {"id": "c", "half": "tune", "label": "contradicted", "detail": "w", "known": ["C1: y"], "labels": []}]
    req = request(rows[0])
    ok.append(("the request is the bench's own form", req["messages"][0]["content"] == "WHAT THEY KNOW:\nC1: y\n\nTHE DETAIL:\nx"
               and req["system"].startswith("You judge one detail") and req["model"] == MODEL))
    ok.append(("an answer's JSON is read first", parse('{"label": "Implied", "kind": "event"} because') == "implied"))
    ok.append(("an unreadable answer is None", parse("I think it is added") is None and parse('{"label": "maybe"}') is None))
    ans = [{"id": "a", "text": '{"label":"implied"}'}, {"id": "b", "text": '{"label":"stated"}'}, {"id": "c", "text": "no"}]
    s = score(ans, rows)
    ok.append(("held: one on the line, one invented passed, one disputed", s["held"]["supportedLine"] == 1
               and s["held"]["inventedCalledSupported"] == 1 and s["held"]["disputedRows"] == 1 and s["held"]["exact"] == 0))
    ok.append(("tune: unread counted", s["tune"]["unread"] == 1))
    ok.append(("the gold leaves the noclaim rows out", os.path.exists(GOLD) is False or all(r["label"] != "noclaim" for r in gold())))
    for name, good in ok:
        print("  %s %s" % ("ok  " if good else "FAIL", name))
    n = sum(1 for _, g in ok if g)
    print("claim_label_trial selftest: passed=%d/%d failed=%d" % (n, len(ok), len(ok) - n))
    return 0 if n == len(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if "--make" in a:
        out = a[a.index("--make") + 1]
        os.makedirs(os.path.dirname(out), exist_ok=True)
        rows = gold()
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            for r in rows:
                fh.write(json.dumps(request(r), ensure_ascii=False) + "\n")
        print("claimLabels requests=%d held=%d tune=%d -> %s" % (len(rows), sum(1 for r in rows if r["half"] == "held"),
                                                               sum(1 for r in rows if r["half"] == "tune"), out))
        sys.exit(0)
    if "--score" in a:
        path = a[a.index("--score") + 1]
        answers = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
        s = score(answers, gold())
        print(json.dumps(s, indent=1))
        json.dump(s, open(os.path.join(os.path.dirname(path), "agreement.json"), "w", encoding="utf-8"), indent=1)
        sys.exit(0)
    print(__doc__)
