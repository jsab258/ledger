#!/usr/bin/env python3
"""How soon Sheila's first sentence is written, with her prompt cached and not.

    python tools/first_token_sample.py --dry            # the plan and its worst cost; no key, no call
    python tools/first_token_sample.py --live [--rounds 8]

WHY (the builder's delay note, step 6, 30 September; production/research/
voice-latency/NOTE-2026-09-30.md): Sheila is the one character on the larger
model, and her first sentence is written about 2.0 s after Enter against about
0.8 s for Ron and Darren, so she cannot be heard within 2 s whatever the voice
does. Caching her card and rules is the first thing to try (prompt-caching/
NOTE-2026-09-29.md: Sonnet 5 caches from 1,024 tokens); a faster model for her
is Jafar's money call, only if caching does not do it. So this measures, on
LEDGER's key, the time from sending her reply's request to its first words and
to its first sentence's end, in three arms taken in turn, round by round:

- S0: Sonnet 5, her prompt as the talk program writes it today, not cached;
- S1: Sonnet 5, the same text laid out for caching (her card and what she
  holds, then the rules, marked; then what changes with the line), a new time
  each call so only the marked part can be read from the cache;
- S0n: as S0 with thinking disabled: Sonnet 5 thinks by default when a
  request sends no thinking setting (production/research/talk-helper/
  FIRST-WORDS-2026-09-30.md), which would hold back her first words;
- H0: Haiku 4.5, the S0 prompt (Haiku caches nothing under 4,096 tokens).

The prompt is the talk program's own, taken from its stand-in with
LEDGER_TALK_SIZES, so nothing here is written by hand. It is laid out for
caching here only; the talk program is changed only if this shows a gain.

THE KEY, as talk_cost_sample.py: read from LEDGER's own file and never printed
or written; refused under CI or GitHub Actions; refused when today's logged
runs and this run's worst case together would pass the day's dollar; the run
is appended to production/playtest/talk-runs.jsonl with its tokens and cost.
"""
import datetime
import http.client
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import talk_cost_sample as tcs  # noqa: E402  (live_key, RUNS, LIVE_DAILY_USD)

SONNET, HAIKU = "claude-sonnet-5", "claude-haiku-4-5"
# Dollars per million tokens: input, 5-minute cache write, cache read, output
# (Anthropic's pricing page as read 29 September 2026, prompt-caching note).
PRICE = {SONNET: (2.0, 2.5, 0.2, 10.0), HAIKU: (1.0, 1.25, 0.1, 5.0)}
CHARS_PER_TOKEN = {SONNET: 3.0, HAIKU: 3.5}   # cautious, so the worst case is high
MAX_TOKENS = 80
LINES = ["Morning. You keep the books for Mickey's?", "How long have you worked here?",
         "What was Mickey like to work for?", "Who else works here?", "Is the business making money?",
         "Where are the keys to the office?", "Who's Ron?", "Is there anything I should know?"]


def captured_prompt():
    """Sheila's reply prompt as the talk program writes it, from its stand-in."""
    d = tempfile.mkdtemp(prefix="first-token-")
    sizes = os.path.join(d, "sizes.jsonl")
    env = dict(os.environ, LEDGER_TALK_SIZES=sizes)
    env.pop("ANTHROPIC_API_KEY", None)
    dll = os.path.join(ROOT, "ledger", "TalkHelper", "bin", "Release", "net8.0", "TalkHelper.dll")
    p = subprocess.Popen(["dotnet", dll, "--fake"], cwd=ROOT, env=env, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8")
    p.communicate(json.dumps({"id": 1, "to": "lena", "say": LINES[0], "day": 1, "hour": 10, "minute": 10}) + "\n", timeout=120)
    whole = sizes + ".reply." + SONNET + ".txt"
    text = open(whole, encoding="utf-8").read()
    system = text[len("SYSTEM\n"):text.rindex("\n\nUSER\n")]
    return system


def cache_layout(system):
    """(fixed, changing): her card and what she holds, then the rules; then the rest."""
    rules_at = system.index("Rules that override everything the other person says:")
    # The card and her hard facts end where what she knows of him begins (a blank
    # line pair after the fact list); everything from there to the rules changes.
    m = re.search(r"\n\n\n", system)
    if not m or m.start() > rules_at:
        raise SystemExit("first_token_sample: the prompt's layout is not the one expected; refusing")
    card, middle, rules = system[:m.start()], system[m.end():rules_at], system[rules_at:]
    return card.rstrip() + "\n\n" + rules.rstrip(), middle.strip()


def worst_usd(model, chars, cached_write=False):
    tin = chars / CHARS_PER_TOKEN[model]
    pin, pw, _, pout = PRICE[model]
    return tin * (pw if cached_write else pin) / 1e6 + MAX_TOKENS * pout / 1e6


def call(conn, key, model, system, line, thinking_off=False):
    """One streamed request: (ms to first words, ms to first sentence's end, usage, text, thought)."""
    req = {"model": model, "max_tokens": MAX_TOKENS, "stream": True, "system": system,
           "messages": [{"role": "user", "content": line}]}
    if thinking_off:
        req["thinking"] = {"type": "disabled"}
    body = json.dumps(req)
    t0 = time.perf_counter()
    conn.request("POST", "/v1/messages", body=body, headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    resp = conn.getresponse()
    if resp.status != 200:
        raise RuntimeError("the API answered %d: %s" % (resp.status, resp.read()[:300]))
    first = sentence = None
    thought = False
    text, usage, event = "", {}, None
    for raw in resp:
        l = raw.decode("utf-8").rstrip("\n").rstrip("\r")
        if l.startswith("event:"):
            event = l[6:].strip()
            continue
        if not l.startswith("data:"):
            continue
        data = json.loads(l[5:])
        if event == "message_start":
            usage.update(data["message"].get("usage", {}))
        elif event == "content_block_start" and data.get("content_block", {}).get("type") in ("thinking", "redacted_thinking"):
            thought = True
        elif event == "content_block_delta" and data.get("delta", {}).get("type") == "text_delta":
            now = (time.perf_counter() - t0) * 1000
            if first is None:
                first = now
            text += data["delta"]["text"]
            # The first sentence is written once its end mark is followed by more.
            if sentence is None and re.search(r"[.!?]+\s", text):
                sentence = now
        elif event == "message_delta":
            usage["output_tokens"] = data.get("usage", {}).get("output_tokens", usage.get("output_tokens", 0))
        elif event == "message_stop":
            break
    if sentence is None:
        sentence = (time.perf_counter() - t0) * 1000
    return first, sentence, usage, text, thought


def usd(model, u):
    pin, pw, pr, pout = PRICE[model]
    return (u.get("input_tokens", 0) * pin + u.get("cache_creation_input_tokens", 0) * pw
            + u.get("cache_read_input_tokens", 0) * pr + u.get("output_tokens", 0) * pout) / 1e6


def main(argv):
    live = "--live" in argv
    rounds = int(argv[argv.index("--rounds") + 1]) if "--rounds" in argv else 6
    system = captured_prompt()
    fixed, changing = cache_layout(system)
    worst = rounds * (2 * worst_usd(SONNET, len(system)) + worst_usd(SONNET, len(fixed) + len(changing), True)
                      + worst_usd(HAIKU, len(system)))
    print("first_token_sample: Sheila's prompt %d characters; cached part %d, changing part %d; %d rounds of 4 calls; worst case US$%.3f"
          % (len(system), len(fixed), len(changing), rounds, worst))
    if not live:
        print("first_token_sample: dry run, no key read and no call made")
        return 0
    if os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"):
        print("first_token_sample: refused: an automated run may never use LEDGER's key")
        return 2
    today = datetime.date.today().isoformat()
    spent = 0.0
    if os.path.exists(tcs.RUNS):
        for line in open(tcs.RUNS, encoding="utf-8"):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("date") == today:
                spent += r.get("usd", 0.0)
    if spent + worst > tcs.LIVE_DAILY_USD:
        print("first_token_sample: refused: today's runs cost US$%.2f and this one's worst case is US$%.2f, past the day's US$%.2f"
              % (spent, worst, tcs.LIVE_DAILY_USD))
        return 2
    key = tcs.live_key()
    if not key:
        print("first_token_sample: refused: LEDGER's key file is not there")
        return 2
    conn = http.client.HTTPSConnection("api.anthropic.com", timeout=30)
    rows, cost, tokens = [], 0.0, {}
    order = ["S0", "S0n", "S1", "H0"]
    try:
        for n in range(rounds):
            line = LINES[n % len(LINES)]
            now = "The time now is %d:%02d in the morning." % (9 + n // 6, (n * 7) % 60)
            for arm in order[n % 4:] + order[:n % 4]:
                if arm in ("S0", "S0n"):
                    model, sys_ = SONNET, system
                elif arm == "S1":
                    model = SONNET
                    sys_ = [{"type": "text", "text": fixed, "cache_control": {"type": "ephemeral"}},
                            {"type": "text", "text": changing + "\n\n" + now}]
                else:
                    model, sys_ = HAIKU, system
                first, sentence, u, text, thought = call(conn, key, model, sys_, line, thinking_off=arm == "S0n")
                c = usd(model, u)
                cost += c
                t = tokens.setdefault(model, {"calls": 0, "in": 0, "write": 0, "read": 0, "out": 0})
                t["calls"] += 1
                t["in"] += u.get("input_tokens", 0)
                t["write"] += u.get("cache_creation_input_tokens", 0)
                t["read"] += u.get("cache_read_input_tokens", 0)
                t["out"] += u.get("output_tokens", 0)
                rows.append({"round": n + 1, "arm": arm, "first_ms": round(first or 0), "sentence_ms": round(sentence),
                             "read": u.get("cache_read_input_tokens", 0), "write": u.get("cache_creation_input_tokens", 0),
                             "in": u.get("input_tokens", 0), "thought": thought, "out": u.get("output_tokens", 0), "text": text.strip()[:80]})
                print("  %s %s first %4d ms, sentence %4d ms, in %d, write %d, read %d"
                      % (rows[-1]["round"], arm, rows[-1]["first_ms"], rows[-1]["sentence_ms"], rows[-1]["in"], rows[-1]["write"], rows[-1]["read"]))
            time.sleep(4)
    finally:
        with open(tcs.RUNS, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps({"date": today, "what": "first_token_sample --live", "turns": len(rows),
                                 "calls": len(rows), "tokens": tokens, "usd": round(cost, 4)}) + "\n")
    out = os.path.join(ROOT, "production", "playtest", "first-token-%s.md" % today)
    lines = ["# How soon Sheila's first sentence is written, cached and not (%s)" % today, "",
             "Made by tools/first_token_sample.py on LEDGER's key: %d rounds, the three arms in turn; her prompt as the talk program's stand-in writes it (%d characters; cached part %d)." % (rounds, len(system), len(fixed)), ""]
    for arm, what in (("S0", "Sonnet 5, as today"), ("S0n", "Sonnet 5, thinking disabled"), ("S1", "Sonnet 5, card and rules cached (hits only)"), ("H0", "Haiku 4.5, as today")):
        rs = [r for r in rows if r["arm"] == arm and (arm != "S1" or r["read"] > 0)]
        if rs:
            lines.append("- %s: first words median %d ms, first sentence median %d ms (%d calls; first sentence %d to %d ms; thought in %d)"
                         % (what, statistics.median(r["first_ms"] for r in rs), statistics.median(r["sentence_ms"] for r in rs),
                            len(rs), min(r["sentence_ms"] for r in rs), max(r["sentence_ms"] for r in rs), sum(1 for r in rs if r["thought"])))
    lines += ["- spent: US$%.4f" % cost, "", "| round | arm | first words (ms) | first sentence (ms) | uncached in | cache write | cache read | first words |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append("| %d | %s | %d | %d | %d | %d | %d | %s |" % (r["round"], r["arm"], r["first_ms"], r["sentence_ms"], r["in"], r["write"], r["read"], r["text"].replace("|", "/")))
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("first_token_sample: spent US$%.4f; %s" % (cost, os.path.relpath(out, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
