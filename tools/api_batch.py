#!/usr/bin/env python3
"""BULK TEXT WORK ON LEDGER'S API CREDIT, WITHIN THE DAY'S CEILING.

    python tools/api_batch.py --dry REQUESTS.jsonl                 # its worst cost and today's ceiling; no key, no call
    python tools/api_batch.py --run REQUESTS.jsonl ANSWERS.jsonl --what "the claim check's labels" [--batch]
    python tools/api_batch.py --fetch BATCH_ID ANSWERS.jsonl --what "..."   # a batch left waiting, collected later
    python tools/api_batch.py --selftest

WHY, 2 November 2026 (his order, n02-6-4-bulk-api; rule 12 of 1 November, RULINGS.md): his plan's monthly API credit
($200, gone at the end of each billing month) pays for bulk text work as scripted calls on the cheapest model that
passes, in batches where that works; the day's ceiling is what remains of the month's credit divided by the days left
(about $20 a day to about 11 November); each day's spend logged; the key never printed, copied or committed. The
plan: production/research/bulk-api/PLAN-2026-11-02.md.

A REQUESTS file has one JSON object a line: {"id", "model", "system" (optional), "messages", "max_tokens"}.
ANSWERS gets one a line: {"id", "model", "text", "input_tokens", "output_tokens", "stop_reason", "error"}.
--batch uses the Message Batches endpoint (half price; answers within 24 hours); it waits up to --wait minutes
(default 60), then leaves the batch's id in production/api-batches.jsonl for --fetch.

THE KEY, as tools/talk_cost_sample.py: read from LEDGER's own file and never printed or written; refused under CI or
GitHub Actions. THE CEILING, checked before anything is sent: the run's worst case (each request's input at 2.5
characters a token plus its whole max_tokens, at the model's price, halved for a batch) must fit what is left of
today's ceiling, worked out from production/api-spend.jsonl. Each run, sent or refused, is one line there.
"""
import datetime
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
SPEND = os.path.join(ROOT, "production", "api-spend.jsonl")
BATCHES = os.path.join(ROOT, "production", "api-batches.jsonl")
API = "https://api.anthropic.com/v1/messages"
VERSION = "2023-06-01"
# RULE 12 (RULINGS.md, 1 November): $200 a month; this month's credit expires about 11 November, so its billing month
# is taken to run from the 12th to the 11th (an assumption from his "about 11 November"; corrected when the bill shows).
CREDIT_USD = 200.0
BILLING_DAY = 12
# US$ per million tokens, in and out: the game's own price card (ledger/Assets/Scripts/Core/LlmClient.cs Models.Cost),
# with Opus 5.5 from Anthropic's model list (read 2 November 2026).
PRICE = {"claude-haiku-5-5": (0.10, 0.50), "claude-haiku-4-5": (1.0, 5.0), "claude-sonnet-5": (2.0, 10.0),
         "claude-sonnet-5-5": (2.0, 10.0), "claude-opus-5-5": (4.0, 20.0)}
#: 2.5, not the first 3.5 (3 November: the harm reader's 64 requests measured 2.84 characters a token, 495,828
#: characters for 174,565 tokens, so the "worst case" read US$0.39 for a run that cost US$0.44; 2.5 keeps it a worst case)
CHARS_PER_TOKEN = 2.5


def month_start(day):
    """The first day of the billing month that holds this day."""
    if day.day >= BILLING_DAY:
        return day.replace(day=BILLING_DAY)
    prev = (day.replace(day=1) - datetime.timedelta(days=1))
    return prev.replace(day=BILLING_DAY)


def days_left(day):
    """Days left in the billing month, today included."""
    start = month_start(day)
    nxt = (start.replace(day=28) + datetime.timedelta(days=10)).replace(day=BILLING_DAY)
    return (nxt - day).days


def spent(lines, since, upto=None):
    total = 0.0
    for r in lines:
        d = str(r.get("day") or "")
        if d >= since.isoformat() and (upto is None or d <= upto.isoformat()):
            total += float(r.get("usd") or 0.0)
    return total


def ceiling_today(lines, day):
    """(ceiling, spent today, left today): what remains of the month's credit before today, over the days left."""
    before = spent(lines, month_start(day), day - datetime.timedelta(days=1))
    ceiling = max(0.0, CREDIT_USD - before) / max(1, days_left(day))
    today = spent(lines, day, day)
    return ceiling, today, max(0.0, ceiling - today)


def worst_cost(req, batch=False):
    if req.get("model") not in PRICE:
        raise ValueError("unknown model %r (prices: %s)" % (req.get("model"), ", ".join(sorted(PRICE))))
    text = (req.get("system") or "") + "".join(
        m["content"] if isinstance(m.get("content"), str) else json.dumps(m.get("content")) for m in req["messages"])
    tin = len(text) / CHARS_PER_TOKEN
    pin, pout = PRICE[req["model"]]
    usd = tin / 1e6 * pin + int(req["max_tokens"]) / 1e6 * pout
    return usd * (0.5 if batch else 1.0)


def real_cost(model, tin, tout, batch=False):
    pin, pout = PRICE.get(model, (0.0, 0.0))
    return (tin / 1e6 * pin + tout / 1e6 * pout) * (0.5 if batch else 1.0)


def load_requests(path):
    reqs = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    ids = [r.get("id") for r in reqs]
    if len(set(ids)) != len(ids) or any(not i for i in ids):
        raise ValueError("every request needs its own id")
    for r in reqs:
        if not r.get("messages") or not r.get("max_tokens"):
            raise ValueError("request %s needs messages and max_tokens" % r["id"])
    return reqs


def read_spend():
    if not os.path.exists(SPEND):
        return []
    out = []
    for l in open(SPEND, encoding="utf-8"):
        try:
            out.append(json.loads(l))
        except ValueError:
            pass
    return out


def log_spend(what, usd, calls, source):
    now = datetime.datetime.now()
    with open(SPEND, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"day": now.date().isoformat(), "at": now.strftime("%H:%M"), "what": what, "usd": round(usd, 4),
                             "calls": calls, "source": source}) + "\n")


def http(method, url, key, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"x-api-key": key, "anthropic-version": VERSION, "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        raw = r.read().decode("utf-8")
    return raw


def params(r):
    p = {"model": r["model"], "max_tokens": int(r["max_tokens"]), "messages": r["messages"]}
    if r.get("system"):
        p["system"] = r["system"]
    return p


def answer_of(rid, model, msg, error=None):
    if error is not None:
        return {"id": rid, "model": model, "text": None, "input_tokens": 0, "output_tokens": 0, "stop_reason": None, "error": error}
    text = "".join(b.get("text", "") for b in msg.get("content", []) if b.get("type") == "text")
    u = msg.get("usage", {})
    return {"id": rid, "model": model, "text": text, "input_tokens": u.get("input_tokens", 0),
            "output_tokens": u.get("output_tokens", 0), "stop_reason": msg.get("stop_reason"), "error": None}


def write_answers(path, answers):
    with open(path, "w", encoding="utf-8") as fh:
        for a in answers:
            fh.write(json.dumps(a, ensure_ascii=False) + "\n")


def collect(key, batch_id, model_of):
    """The ended batch's answers, or None while it is still running."""
    b = json.loads(http("GET", API + "/batches/" + batch_id, key))
    if b.get("processing_status") != "ended":
        return None
    answers = []
    for line in http("GET", b["results_url"], key).splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        res = r.get("result", {})
        rid = r.get("custom_id")
        if res.get("type") == "succeeded":
            answers.append(answer_of(rid, model_of.get(rid), res["message"]))
        else:
            answers.append(answer_of(rid, model_of.get(rid), None, error=res.get("type")))
    return answers


def main(argv):
    if "--selftest" in argv:
        return selftest()
    today = datetime.date.today()
    lines = read_spend()
    ceiling, so_far, left = ceiling_today(lines, today)
    if "--dry" in argv:
        reqs = load_requests(argv[argv.index("--dry") + 1])
        batch = "--batch" in argv
        worst = sum(worst_cost(r, batch) for r in reqs)
        print("api_batch dry: %d requests, worst case US$%.4f%s; today's ceiling US$%.2f, spent US$%.2f, left US$%.2f"
              % (len(reqs), worst, " (batch, half price)" if batch else "", ceiling, so_far, left))
        return 0
    if os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"):
        print("api_batch refused: an automated run may never use LEDGER's key")
        return 1
    what = argv[argv.index("--what") + 1] if "--what" in argv else "bulk text work"
    import talk_cost_sample as tcs  # its key reader, so the key has one home
    key = tcs.live_key()
    if key is None:
        print("api_batch refused: LEDGER's key file is not there")
        return 1
    if "--fetch" in argv:
        batch_id, out = argv[argv.index("--fetch") + 1], argv[argv.index("--fetch") + 2]
        model_of = {}
        if os.path.exists(BATCHES):
            for l in open(BATCHES, encoding="utf-8"):
                r = json.loads(l)
                if r.get("batch") == batch_id:
                    model_of = r.get("models", {})
        answers = collect(key, batch_id, model_of)
        if answers is None:
            print("api_batch: batch %s still running" % batch_id)
            return 2
        usd = sum(real_cost(a["model"], a["input_tokens"], a["output_tokens"], True) for a in answers)
        write_answers(out, answers)
        log_spend(what, usd, len(answers), "api_batch.py --fetch %s (real tokens, batch price)" % batch_id)
        print("api_batch: %d answers, US$%.4f" % (len(answers), usd))
        return 0
    src, out = argv[argv.index("--run") + 1], argv[argv.index("--run") + 2]
    reqs = load_requests(src)
    batch = "--batch" in argv
    worst = sum(worst_cost(r, batch) for r in reqs)
    if worst > left:
        log_spend(what + " (refused)", 0.0, 0, "api_batch.py: worst case US$%.4f past today's US$%.2f left" % (worst, left))
        print("api_batch refused: worst case US$%.4f, today's ceiling US$%.2f with US$%.2f left" % (worst, ceiling, left))
        return 1
    answers = []
    if batch:
        body = {"requests": [{"custom_id": r["id"], "params": params(r)} for r in reqs]}
        b = json.loads(http("POST", API + "/batches", key, body))
        model_of = {r["id"]: r["model"] for r in reqs}
        with open(BATCHES, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"batch": b["id"], "at": datetime.datetime.now().isoformat(timespec="minutes"), "what": what,
                                 "out": out, "models": model_of}) + "\n")
        wait = float(argv[argv.index("--wait") + 1]) if "--wait" in argv else 60.0
        t0 = time.time()
        while answers == [] and time.time() - t0 < wait * 60:
            got = collect(key, b["id"], model_of)
            if got is not None:
                answers = got
                break
            time.sleep(30)
        if not answers:
            print("api_batch: batch %s still running after %.0f minutes; collect it with --fetch" % (b["id"], wait))
            return 2
    else:
        for r in reqs:
            try:
                answers.append(answer_of(r["id"], r["model"], json.loads(http("POST", API, key, params(r)))))
            except Exception as e:  # one failed call is written as such; the rest go on
                answers.append(answer_of(r["id"], r["model"], None, error=type(e).__name__))
    usd = sum(real_cost(a["model"], a["input_tokens"], a["output_tokens"], batch) for a in answers)
    write_answers(out, answers)
    log_spend(what, usd, len(answers), "api_batch.py (real tokens%s)" % (", batch price" if batch else ""))
    print("api_batch: %d answers, US$%.4f; today's ceiling US$%.2f" % (len(answers), usd, ceiling))
    return 0


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("api_batch selftest FAIL " + name)

    d = datetime.date
    check("the billing month starts on the 12th", month_start(d(2026, 11, 2)) == d(2026, 10, 12) and month_start(d(2026, 11, 12)) == d(2026, 11, 12))
    check("days left count today", days_left(d(2026, 11, 2)) == 10 and days_left(d(2026, 11, 11)) == 1)
    lines = [{"day": "2026-11-01", "usd": 0.99}, {"day": "2026-11-02", "usd": 1.51}, {"day": "2026-10-01", "usd": 50.0}]
    ceiling, today, left = ceiling_today(lines, d(2026, 11, 2))
    check("the ceiling is what remains over the days left", abs(ceiling - (200.0 - 0.99) / 10) < 1e-9)
    check("today's spend and what is left", abs(today - 1.51) < 1e-9 and abs(left - (ceiling - 1.51)) < 1e-9)
    r = {"id": "a", "model": "claude-haiku-5-5", "messages": [{"role": "user", "content": "x" * 2500}], "max_tokens": 1000}
    check("worst case: input and the whole output", abs(worst_cost(r) - (1000 / 1e6 * 0.10 + 1000 / 1e6 * 0.50)) < 1e-12)
    check("a batch is half price", abs(worst_cost(r, True) - worst_cost(r) / 2) < 1e-12)
    try:
        worst_cost(dict(r, model="gpt"))
        check("an unknown model is refused", False)
    except ValueError:
        check("an unknown model is refused", True)
    msg = {"content": [{"type": "text", "text": "yes"}], "usage": {"input_tokens": 10, "output_tokens": 2}, "stop_reason": "end_turn"}
    a = answer_of("a", "claude-haiku-5-5", msg)
    check("an answer keeps its text and tokens", a["text"] == "yes" and a["input_tokens"] == 10 and a["error"] is None)
    check("a params body has no system when none is given", "system" not in params(r) and params(dict(r, system="s"))["system"] == "s")
    print("api_batch selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
