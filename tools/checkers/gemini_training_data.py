#!/usr/bin/env python3
"""The fast checker's training data, written and labelled by Gemini 3.8 Flash through Google's Batch API.

    python tools/checkers/gemini_training_data.py gen-requests OUT.jsonl [--per 93 --calls-per-context 2]
    python tools/checkers/gemini_training_data.py submit IN.jsonl NAME            # uploads, creates the batch; prints its name
    python tools/checkers/gemini_training_data.py status BATCH                    # its state
    python tools/checkers/gemini_training_data.py fetch BATCH OUT.jsonl           # its results, and the cost logged
    python tools/checkers/gemini_training_data.py label-requests GEN.jsonl OUT.jsonl [--per-call 10]
    python tools/checkers/gemini_training_data.py build LABELLED.jsonl GEN.jsonl TRAIN.json
    python tools/checkers/gemini_training_data.py --selftest

WHY, 26 October 2026. His answer that evening (production/orders/2026-10-25.md): "The fast checker's training: use
Gemini instead of Haiku ... Gemini 3.8 Flash writes the training sentences from the game's facts and labels them ...
The 127 held-out details stay the test, and nothing changes in the game before I have seen the numbers." Google's
current terms allow it (production/research/invented-claims/GEMINI-TERMS-2026-10-26.md: only models competing with
Gemini are barred); the free tier is far too small, and his yes the same evening: the Batch service, up to $10.
Untrained, the open checkers clear almost nothing safely (LOCAL-CHECKERS-2026-10-26.md, "Measured").

THE DATA. Only the detail bench's tuning half is used (F:/LedgerTools/town-scratch/detail-bench/detail-gold.jsonl,
half "tune": 27 speaker-and-question contexts, each with the facts the speaker is given); the held half's 31 contexts
share no question with them and stay the test. For each context Gemini writes first sentences in the speaker's voice,
some saying only what the facts support and some adding or contradicting a detail; a separate call then labels each
sentence against the same facts, naming the exact words that are not supported. The labels, not the writer's
intentions, are what the checker learns. Ten sentences are labelled a call (each judged on its own), which cuts the
input about tenfold against one a call.

THE KEY. Read from F:/LedgerTools/keys/google.txt into memory and sent only in the x-goog-api-key header to Google's
API (as the lab's run of 22 October did: production/lab/talk-check/gemini_check.py); never printed, logged or
written anywhere. Thinking is off (thinkingBudget 0), as in that run, where 3.8 Flash let no invented detail through.

THE COST. Every fetch reads the batch's token counts, prices them at the Batch rate (half of $0.75 in and $3.75 out
per million until 31 December 2026), appends the run to production/playtest/talk-runs.jsonl, and refuses to submit
another batch once the total passes the cap ($10, his yes).
"""
import json
import os
import random
import re
import sys
import time
import urllib.request

KEYFILE = "F:/LedgerTools/keys/google.txt"
API = "https://generativelanguage.googleapis.com"
MODEL = "gemini-3.8-flash"
GOLD = "F:/LedgerTools/town-scratch/detail-bench/detail-gold.jsonl"
RUNS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "production", "playtest", "talk-runs.jsonl")
PRICE_IN, PRICE_OUT, BATCH = 0.75, 3.75, 0.5          # dollars a million tokens, Batch at half (until 31 Dec 2026)
CAP = 10.0
SPEAKERS = {"lena": "Sheila Dunn, the bookkeeper of Mickey's minicab office", "rocco": "Ron Kirby, the cab driver who keeps the rank",
            "sam": "Darren Milner, a young street hustler"}


def key():
    return open(KEYFILE, encoding="utf-8").read().strip()


def contexts():
    seen, out = set(), []
    for line in open(GOLD, encoding="utf-8"):
        r = json.loads(line)
        k = (r["card"], r["probe"])
        if r["half"] != "tune" or k in seen:
            continue
        seen.add(k)
        out.append({"card": r["card"], "probe": r["probe"], "known": r["known"]})
    return out


GEN = """You write lines for a character in a video game set in 1990 in a fictional northern English seaside town.
The character is {who}. The player has just asked them: "{probe}"

Everything the character knows is in this numbered list:
{facts}

Write {n} different possible FIRST SENTENCES of the character's spoken reply, one per line, numbered 1 to {n}.
- Spoken English as this character would say it in 1990: short, plain, in their own voice.
- About half must say only what the list supports (or say nothing checkable, or say they don't know).
- The rest must each slip in ONE specific detail the list does not support: a name, a time, a place, an event,
  a number or a habit that is invented, or that contradicts the list. Make these sound just as natural.
- Vary them: different facts, different lengths (4 to 25 words), different ways of not answering.
- Never mention alcohol, pubs, betting or gambling, children, real brands, real people, or anything after 1992.
Return only the numbered lines."""

LABEL = """You check whether each sentence a game character says is supported by what the character knows.

What the character knows (numbered facts):
{facts}

For EACH sentence below, decide on its own whether every specific detail in it (names, people, places, times,
events, numbers, habits, relationships) is stated in or clearly implied by the facts. Saying nothing checkable,
or saying they don't know, is supported. Reply with JSON only: a list with one object per sentence, in order:
{{"n": <number>, "supported": true or false, "unsupported": [the exact words copied from the sentence that state
anything not supported; empty if supported]}}

Sentences:
{sentences}"""


def facts_text(known):
    return "\n".join(known)


def request(text, temperature):
    return {"contents": [{"role": "user", "parts": [{"text": text}]}],
            "generation_config": {"temperature": temperature, "maxOutputTokens": 8000, "thinkingConfig": {"thinkingBudget": 0}}}


def gen_requests(out, per, calls):
    n = 0
    with open(out, "w", encoding="utf-8") as fh:
        for i, c in enumerate(contexts()):
            for j in range(calls):
                text = GEN.format(who=SPEAKERS.get(c["card"], c["card"]), probe=c["probe"], facts=facts_text(c["known"]), n=per)
                fh.write(json.dumps({"key": "gen-%02d-%d" % (i, j), "request": request(text, 1.0)}) + "\n")
                n += 1
    print("gen requests: %d (%d contexts x %d) -> %s" % (n, len(contexts()), calls, out))


def parse_lines(text):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        body = line.split(".", 1)[1] if "." in line[:4] else line.split(")", 1)[-1]
        body = body.strip().strip('"').strip()
        if 3 <= len(body.split()) <= 40:
            out.append(body)
    return out


def results_text(res):
    """{key: text} from a fetched results file (one GenerateContentResponse or error a line, with its key)."""
    out = {}
    for line in open(res, encoding="utf-8"):
        r = json.loads(line)
        k = r.get("key")
        resp = r.get("response") or {}
        cands = resp.get("candidates") or []
        if k and cands:
            out[k] = "".join(p.get("text", "") for p in cands[0].get("content", {}).get("parts", []))
    return out


# The project's content rule (no children anywhere; no alcohol or gambling): the writer drifted into school runs and
# childhood memories in about one sentence in 150 (26 October's batch); those are dropped before labelling.
OUT_OF_CANON = re.compile(r"\b(school\w*|child\w*|kids?|boys together|man and boy|when (s?he|I) was (a )?(little|young|"
                          r"small|twelve|ten|\w+teen|\d+)|girl|pub|pint|beer|lager|whiske?y|wine|drunk|booze|bookies?|"
                          r"bookmaker\w*|betting|casino|gambl\w*|the pools)\b", re.I)


def label_requests(gen_res, out, per_call):
    ctx = contexts()
    texts = results_text(gen_res)
    n_req = n_sent = 0
    with open(out, "w", encoding="utf-8") as fh:
        for k, text in sorted(texts.items()):
            i = int(k.split("-")[1])
            sents = [t for t in parse_lines(text) if not OUT_OF_CANON.search(t)]
            for s in range(0, len(sents), per_call):
                chunk = sents[s:s + per_call]
                body = "\n".join("%d. %s" % (m + 1, t) for m, t in enumerate(chunk))
                req = request(LABEL.format(facts=facts_text(ctx[i]["known"]), sentences=body), 0.0)
                fh.write(json.dumps({"key": "lab-%s-%03d" % (k, s), "request": req, "sentences": chunk, "context": i}) + "\n")
                n_req += 1
                n_sent += len(chunk)
    print("label requests: %d covering %d sentences -> %s" % (n_req, n_sent, out))


def http(method, url, body=None, headers=None, raw=False):
    h = {"x-goog-api-key": key()}
    h.update(headers or {})
    data = body if isinstance(body, (bytes, type(None))) else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    with urllib.request.urlopen(req, timeout=300) as r:
        return (r.read(), r.headers) if raw else json.load(r)


def spent():
    total = 0.0
    if os.path.exists(RUNS):
        for line in open(RUNS, encoding="utf-8"):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("task") == "checker-training-2026-10-26":
                total += float(r.get("usd") or 0)
    return total


def submit(path, name):
    if spent() >= CAP:
        sys.exit("refused: $%.2f already spent of the $%.0f cap" % (spent(), CAP))
    # the requests file without our own extra fields (sentences, context), which Google would refuse
    lines = []
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        lines.append(json.dumps({"key": r["key"], "request": r["request"]}))
    data = ("\n".join(lines) + "\n").encode()
    _, hdr = http("POST", API + "/upload/v1beta/files", json.dumps({"file": {"display_name": name}}).encode(),
                  {"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start",
                   "X-Goog-Upload-Header-Content-Length": str(len(data)), "X-Goog-Upload-Header-Content-Type": "application/jsonl",
                   "Content-Type": "application/json"}, raw=True)
    up = hdr.get("x-goog-upload-url")
    body, _ = http("POST", up, data, {"Content-Length": str(len(data)), "X-Goog-Upload-Offset": "0",
                                      "X-Goog-Upload-Command": "upload, finalize"}, raw=True)
    f = json.loads(body)["file"]["name"]
    b = http("POST", "%s/v1beta/models/%s:batchGenerateContent" % (API, MODEL),
             {"batch": {"display_name": name, "input_config": {"file_name": f}}}, {"Content-Type": "application/json"})
    print(json.dumps({"batch": b.get("name"), "file": f, "requests": len(lines)}))


def status(name):
    b = http("GET", "%s/v1beta/%s" % (API, name))
    md = b.get("metadata") or b
    print(json.dumps({"name": name, "state": md.get("state") or b.get("state"), "done": b.get("done"),
                      "stats": md.get("batchStats") or b.get("batchStats")}))
    return b


def fetch(name, out):
    b = status(name)
    md = b.get("metadata") or b
    dest = (b.get("response") or {}).get("responsesFile") or (md.get("output") or {}).get("responsesFile") \
        or (b.get("dest") or {}).get("fileName") or (md.get("dest") or {}).get("fileName")
    if not dest:
        sys.exit("no results file yet")
    body, _ = http("GET", "%s/download/v1beta/%s:download?alt=media" % (API, dest), raw=True)
    open(out, "wb").write(body)
    tin = tout = 0
    for line in open(out, encoding="utf-8"):
        u = (json.loads(line).get("response") or {}).get("usageMetadata") or {}
        tin += u.get("promptTokenCount", 0)
        tout += u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)
    usd = (tin * PRICE_IN + tout * PRICE_OUT) / 1e6 * BATCH
    rec = {"date": time.strftime("%Y-%m-%d"), "task": "checker-training-2026-10-26", "what": "Gemini 3.8 Flash batch %s" % name,
           "calls": sum(1 for _ in open(out, encoding="utf-8")), "tokens": {MODEL: {"in": tin, "out": tout}}, "usd": round(usd, 4),
           "usd_is": "the batch's own token counts at the Batch price (half of $0.75 / $3.75 a million)"}
    open(RUNS, "a", encoding="utf-8").write(json.dumps(rec) + "\n")
    print(json.dumps({"fetched": out, "in": tin, "out": tout, "usd": round(usd, 4), "spentTotal": round(spent(), 4)}))


def build(labelled_res, label_req, out):
    """TinyLettuce's training format: each example the context (the facts), the question, the sentence, and the
    character spans of the words Gemini named unsupported."""
    reqs = {json.loads(l)["key"]: json.loads(l) for l in open(label_req, encoding="utf-8")}
    ctx = contexts()
    texts = results_text(labelled_res)
    ex, bad = [], 0
    for k, text in texts.items():
        q = reqs.get(k)
        if q is None:
            continue
        try:
            t = text.strip().strip("`")
            t = t[t.index("["):t.rindex("]") + 1]
            verdicts = json.loads(t)
        except ValueError:
            bad += 1
            continue
        for v in verdicts:
            n = int(v.get("n", 0)) - 1
            if not 0 <= n < len(q["sentences"]):
                continue
            s = q["sentences"][n]
            spans = []
            for w in v.get("unsupported") or []:
                i = s.find(w)
                if i >= 0:
                    spans.append({"start": i, "end": i + len(w)})
            if not v.get("supported") and not spans:
                bad += 1                      # unsupported but no words found: unusable as a token label
                continue
            c = ctx[q["context"]]
            ex.append({"context": c["known"], "question": c["probe"], "answer": s, "labels": spans, "supported": bool(v.get("supported"))})
    random.Random(19901026).shuffle(ex)
    json.dump(ex, open(out, "w", encoding="utf-8"), indent=0)
    print(json.dumps({"examples": len(ex), "supported": sum(e["supported"] for e in ex), "unusable": bad, "out": out}))


def selftest():
    ok = 0
    ok += parse_lines("1. Right then.\n2) Mickey kept the books himself, he did.\nnoise\n3. Ok") == ["Mickey kept the books himself, he did."] or \
        len(parse_lines("1. Right then, that is all.\n2. Mickey kept the books himself, he did.")) == 2
    ok += len(contexts()) == 27
    ok += "x-goog-api-key" not in open(__file__, encoding="utf-8").read().split("def http")[0][-200:]
    print("gemini_training_data selftest: passed=%d/3" % ok)
    return 0 if ok == 3 else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--selftest":
        sys.exit(selftest())
    cmd = a[0]
    num = lambda n, d: int(a[a.index(n) + 1]) if n in a else d  # noqa: E731
    if cmd == "gen-requests":
        gen_requests(a[1], num("--per", 93), num("--calls-per-context", 2))
    elif cmd == "submit":
        submit(a[1], a[2])
    elif cmd == "status":
        status(a[1])
    elif cmd == "fetch":
        fetch(a[1], a[2])
    elif cmd == "label-requests":
        label_requests(a[1], a[2], num("--per-call", 10))
    elif cmd == "build":
        build(a[1], a[2], a[3])
