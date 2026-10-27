#!/usr/bin/env python3
"""The invented sentences at the source: Gemini's labels and the counts per 300 (his order of 27 October 2026, evening).

    python tools/checkers/source_test.py label [DIR]                 # Gemini labels every kept first sentence (sync calls)
    python tools/checkers/source_test.py report [DIR] OUT.json       # the counts per variant, and the harm-sort packet
                                                                     # (DIR/through-packet.json, read blind by a fresh reader)

DIR (default F:/LedgerTools/checkers/source) holds source-today.jsonl, source-facts.jsonl and source-cite.jsonl, written
by ledger/ClaimBench's source mode: each row a question of the 617 asked again of the game's reply model, the raw first
sentence it wrote, Haiku's whole check on it, and the list of facts the check read.

THE LABELS are Gemini 3.8 Flash's, with the same prompt that labelled the 617 (gemini_training_data.LABEL), against
the same facts the check read for that row, ten sentences a call, sent one call at a time rather than as a batch so the
answer comes the same evening. The key is read and sent as gemini_training_data does (its http(): the
x-goog-api-key header only). The spend is logged to the source test's task, whose cap is his $20 (Claude and Gemini).

THE COUNTS, per variant, per 300 first sentences written: invented written (Gemini: not supported); invented through
(written and passed by Haiku's check); the same with the hard rule on names, and with its wider form; harmful and
harmless apart once the blind reader has sorted the ones through; and false refusals (supported by Gemini, refused by
the check) per 300 and as a share of the supported.
"""
import json
import os
import sys
import time
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gemini_training_data as g  # noqa: E402
import name_rule as nr  # noqa: E402

VARIANTS = ("today", "facts", "cite")
TASK = "invented-source-2026-10-27"
CAP = 20.0
PRICE_IN, PRICE_OUT = 0.75, 3.75          # Gemini 3.8 Flash, dollars a million tokens, not batched


def rows(d, v):
    return [json.loads(l) for l in open(os.path.join(d, "source-%s.jsonl" % v), encoding="utf-8") if l.strip()]


def task_spent():
    total = 0.0
    for line in open(g.RUNS, encoding="utf-8"):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get("task") == TASK:
            total += float(r.get("usd") or 0)
    return total


def label(d):
    url = "%s/v1beta/models/%s:generateContent" % (g.API, g.MODEL)
    tin = tout = calls = 0
    for v in VARIANTS:
        out = os.path.join(d, "labels-%s.jsonl" % v)
        done = {}
        if os.path.exists(out):
            for l in open(out, encoding="utf-8"):
                r = json.loads(l)
                done[r["row"]] = r
        groups = {}
        for r in rows(d, v):
            if r["row"] in done:
                continue
            groups.setdefault((r["card"], tuple(r["known"])), []).append(r)
        with open(out, "a", encoding="utf-8") as fh:
            for (card, known), rs in groups.items():
                for s in range(0, len(rs), 10):
                    chunk = rs[s:s + 10]
                    body = "\n".join("%d. %s" % (m + 1, r["sentence"]) for m, r in enumerate(chunk))
                    if task_spent() + (tin * PRICE_IN + tout * PRICE_OUT) / 1e6 >= CAP:
                        sys.exit("refused: the source test's $%.0f cap" % CAP)
                    req = g.request(g.LABEL.format(facts=g.facts_text(list(known)), sentences=body), 0.0)
                    for attempt in range(3):
                        try:
                            resp = g.http("POST", url, req, {"Content-Type": "application/json"})
                            break
                        except urllib.error.HTTPError as e:
                            if attempt == 2:
                                raise
                            time.sleep(5 * (attempt + 1))
                    calls += 1
                    u = resp.get("usageMetadata") or {}
                    tin += u.get("promptTokenCount", 0)
                    tout += u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)
                    text = "".join(p.get("text", "") for p in resp["candidates"][0]["content"]["parts"])
                    text = text.strip().strip("`")
                    if text.startswith("json"):
                        text = text[4:]
                    verdicts = {int(x["n"]): x for x in json.loads(text)}
                    for m, r in enumerate(chunk):
                        x = verdicts.get(m + 1)
                        fh.write(json.dumps({"row": r["row"], "variant": v, "sentence": r["sentence"],
                                             "supported": None if x is None else bool(x["supported"]),
                                             "unsupported": [] if x is None else x.get("unsupported", [])}, ensure_ascii=False) + "\n")
                    fh.flush()
        print("labelled %s" % v)
    usd = (tin * PRICE_IN + tout * PRICE_OUT) / 1e6
    rec = {"date": time.strftime("%Y-%m-%d"), "task": TASK, "what": "Gemini 3.8 Flash labels of the source test's first sentences",
           "calls": calls, "tokens": {g.MODEL: {"in": tin, "out": tout}}, "usd": round(usd, 4),
           "usd_is": "the calls' own token counts at the standard price ($0.75 / $3.75 a million)"}
    open(g.RUNS, "a", encoding="utf-8").write(json.dumps(rec) + "\n")
    print(json.dumps({"calls": calls, "usd": round(usd, 4), "taskSpent": round(task_spent(), 4)}))


def per300(n, total):
    return round(300.0 * n / total, 1) if total else None


def report(d, out):
    res, packet = {}, []
    for v in VARIANTS:
        rs = {r["row"]: r for r in rows(d, v)}
        lab = {}
        for l in open(os.path.join(d, "labels-%s.jsonl" % v), encoding="utf-8"):
            x = json.loads(l)
            lab[x["row"]] = x
        both = [r for k, r in rs.items() if k in lab and lab[k]["supported"] is not None]
        inv = [r for r in both if not lab[r["row"]]["supported"]]
        sup = [r for r in both if lab[r["row"]]["supported"]]
        through = [r for r in inv if r["passed"]]
        through_rule = [r for r in through if not nr.missing(r["sentence"], r["known"])]
        through_wider = [r for r in through if not nr.missing_wider(r["sentence"], r["known"])]
        refused_true = [r for r in sup if not r["passed"]]
        rule_true = [r for r in sup if r["passed"] and nr.missing(r["sentence"], r["known"])]
        wider_true = [r for r in sup if r["passed"] and nr.missing_wider(r["sentence"], r["known"])]
        n = len(both)
        res[v] = {"sentences": n, "unlabelled": len(rs) - n, "inventedWritten": len(inv), "inventedWrittenPer300": per300(len(inv), n),
                  "inventedThrough": len(through), "inventedThroughPer300": per300(len(through), n),
                  "throughWithNameRule": len(through_rule), "throughWithNameRulePer300": per300(len(through_rule), n),
                  "throughWithWiderRule": len(through_wider), "throughWithWiderRulePer300": per300(len(through_wider), n),
                  "supported": len(sup), "falseRefusals": len(refused_true), "falseRefusalsPer300": per300(len(refused_true), n),
                  "falseRefusalShareOfSupported": round(len(refused_true) / len(sup), 3) if sup else None,
                  "nameRuleNewFalseRefusals": len(rule_true), "widerRuleNewFalseRefusals": len(wider_true),
                  "citeWithoutBraces": sum(1 for r in rs.values() if r.get("formatted") is False)}
        for r in through:
            packet.append({"variant": v, "row": r["row"], "card": r["card"], "question": r["question"], "sentence": r["sentence"],
                           "known": r["known"], "stoppedByNameRule": bool(nr.missing(r["sentence"], r["known"])),
                           "stoppedByWiderRule": bool(nr.missing_wider(r["sentence"], r["known"]))})
    json.dump({"byVariant": res}, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(packet, open(os.path.join(d, "through-packet.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for v, x in res.items():
        print(v, json.dumps(x))
    print("through, for the blind harm sort: %d -> %s" % (len(packet), os.path.join(d, "through-packet.json")))


if __name__ == "__main__":
    a = sys.argv[1:]
    d = a[1] if len(a) > 1 and os.path.isdir(a[1]) else "F:/LedgerTools/checkers/source"
    if a[0] == "label":
        label(d)
    elif a[0] == "report":
        report(d, a[-1])
