#!/usr/bin/env python3
"""A scripted sample of turns through the game's own talk program, run against its stand-in.

NO REAL CALLS (Jafar, 29 September: nothing in development calls the
Anthropic API). The talk program runs here as its stand-in (--fake), with no
key in its environment, so this checks the sample's plumbing and timing only
and every cost it reports is nothing. What live talk costs now comes from the
live talk's own record while Jafar plays, on LEDGER's own capped key, which
no tool reads. What follows is how it measured cost before, on 29 September.

    python tools/talk_cost_sample.py [--turns-per-hour 120] [--early] [--out production/playtest/talk-cost-<date>.md]
    python tools/talk_cost_sample.py --early --sizes <file.jsonl>   # what each request sends, by kind (town list T1)
    python tools/talk_cost_sample.py --early --live                 # the real model, on LEDGER's own key (town list T1)

--live (Jafar, 29 September evening: the LEDGER key "for these measurements
only, at most about a dollar a day, each run logged with its tokens and
cost"): the key is read from LEDGER's own file (%LOCALAPPDATA%/LEDGER/
live-talk-key.txt), put in the talk program's environment and never printed
or written anywhere; the run is refused under CI or GitHub Actions, and
refused when today's logged spend and the last run's cost together would pass
LIVE_DAILY_USD; every run is appended to production/playtest/talk-runs.jsonl
with its date, turns, calls, tokens by model and dollars.

With --sizes the stand-in streams, the check runs as it would with the real
model, and every request's size is logged to the file (the talk program's
LEDGER_TALK_SIZES); the summary printed is characters by kind of call, and
tokens at about four characters to a token, an estimate until the key exists.

With --early (town list 6bx) the talk program is started as the game starts it,
with --early: each reply's first sentence is sent as soon as it passes its
check, and the sample records when it was heard, how each turn went (own,
fallback, cut, brush...) and where the time went (the reply's steps).

WHY, 29 September (Jafar's list, item 9: "what one hour of conversation costs,
from real calls"). The talk program (ledger/TalkHelper) is started as the game
starts it, with no options and the key in its environment, read from the
game's own secrets file and never printed. Three short conversations are put
to it, one each with Sheila, Ron and Darren, a player's lines as a player
might type them. When its input closes it prints what the session cost (calls,
tokens by model and the dollar estimate at the game's own rate card,
Core/Models.cs); this divides that by the turns and multiplies it by how many
turns an hour of talk holds. Nothing here is simulated: every reply is a
real call.
"""
import datetime
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DLL = os.path.join(ROOT, "ledger", "TalkHelper", "bin", "Release", "net8.0", "TalkHelper.dll")
RUNS = os.path.join(ROOT, "production", "playtest", "talk-runs.jsonl")
LIVE_DAILY_USD = 1.00
# The last real run's cost (29 September, 24 turns), until a logged run replaces it.
LIVE_RUN_ESTIMATE_USD = 0.36


def live_key():
    """LEDGER's own key, from its file; None when it is not there."""
    path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "LEDGER", "live-talk-key.txt")
    try:
        key = open(path, encoding="utf-8").read().strip()
    except OSError:
        return None
    return key or None


def live_allowed():
    """(allowed, why): never under CI; within the day's allowance."""
    if os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"):
        return False, "refused: an automated run may never use LEDGER's key"
    today = datetime.date.today().isoformat()
    spent, last = 0.0, LIVE_RUN_ESTIMATE_USD
    if os.path.exists(RUNS):
        for line in open(RUNS, encoding="utf-8"):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            last = r.get("usd", last)
            if r.get("date") == today:
                spent += r.get("usd", 0.0)
    if spent + last > LIVE_DAILY_USD:
        return False, "refused: today's runs cost US$%.2f, and another (about US$%.2f) would pass US$%.2f" % (spent, last, LIVE_DAILY_USD)
    return True, "today's runs so far US$%.2f" % spent

CONVERSATIONS = [
    ("lena", ["Morning. You keep the books for Mickey's?",
              "How long have you worked here?",
              "What was Mickey like to work for?",
              "Did you hear anything about the break-in on Quay Street?",
              "Who do you think did it?",
              "Would you tell the police if you knew?",
              "Is there anything you need doing round the office?",
              "Right. I'll leave you to it. Thanks, Sheila."]),
    ("rocco", ["Alright, Ron. Quiet tonight?",
               "How long were you on the docks?",
               "What happened when the scheme ended?",
               "Anybody been hanging about the rank who shouldn't be?",
               "I heard something happened on Quay Street. Did you see it?",
               "What would you do if you found out who it was?",
               "Do you trust Darren?",
               "Fair enough. See you later, Ron."]),
    ("sam", ["Darren. What are you selling today?",
             "How much for a radio?",
             "Where do you get your stuff from?",
             "Have you heard about the break-in?",
             "Somebody said they saw you near there.",
             "Can you find out who did it for me?",
             "What's it going to cost me?",
             "All right. Don't do anything stupid."]),
]


def median(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2] if xs else None


def timing_lines(replies):
    """With --early: when the first sentence was heard, how each turn went, and
    the median time at which each step of a turn ended (town list 6bx)."""
    firsts = [r["first_s"] for r in replies if r.get("first_s") is not None]
    went = {}
    for r in replies:
        went[r.get("went") or "?"] = went.get(r.get("went") or "?", 0) + 1
    steps = {}
    for r in replies:
        for name, ms in r["steps"]:
            steps.setdefault(name, []).append(ms / 1000.0)
    out = ["- with --early, as the game runs it: a first sentence heard in %d of %d turns, median %s s, slowest %s s"
           % (len(firsts), len(replies), "%.1f" % median(firsts) if firsts else "-", "%.1f" % max(firsts) if firsts else "-"),
           "- how the turns went: " + ", ".join("%s %d" % kv for kv in sorted(went.items()))]
    if steps:
        out.append("- each step's end, median from the turn's start: " + ", ".join(
            "%s %.1f s (%d turns)" % (name, median(v), len(v)) for name, v in steps.items()))
    return out


def size_summary(path, turns):
    """What each kind of request sends, in characters, and tokens estimated."""
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    by = {}
    for r in rows:
        by.setdefault((r["kind"], r["model"]), []).append(r)
    out = ["what the talk program sends, %d turns, %d requests (the stand-in; tokens at about four characters each)" % (turns, len(rows))]
    total = 0
    for (kind, model), rs in sorted(by.items()):
        sysc = sum(r["system"] for r in rs) / len(rs)
        msgc = sum(r["messages"] for r in rs) / len(rs)
        total += sum(r["system"] + r["messages"] for r in rs)
        out.append("  %-13s %-18s %3d calls  system %6.0f chars  messages %5.0f chars  ~%5.0f tokens a call" % (kind, model, len(rs), sysc, msgc, (sysc + msgc) / 4))
    out.append("  all: %.0f characters a turn, ~%.0f tokens a turn" % (total / max(1, turns), total / max(1, turns) / 4))
    return "\n".join(out)


def main(argv):
    per_hour = int(argv[argv.index("--turns-per-hour") + 1]) if "--turns-per-hour" in argv else 120
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(
        ROOT, "production", "playtest", "talk-cost-%s.md" % datetime.date.today().isoformat())
    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)   # never a key but LEDGER's own, below
    live = "--live" in argv
    if live:
        ok, why = live_allowed()
        print(why)
        if not ok:
            return 1
        key = live_key()
        if key is None:
            print("no LEDGER key yet: nothing run")
            return 1
        env["ANTHROPIC_API_KEY"] = key
    early = "--early" in argv
    sizes = argv[argv.index("--sizes") + 1] if "--sizes" in argv else None
    if sizes:
        if os.path.exists(sizes):
            os.remove(sizes)
        env["LEDGER_TALK_SIZES"] = os.path.abspath(sizes)
    p = subprocess.Popen(["dotnet", DLL] + ([] if live else ["--fake"]) + (["--early"] if early else []), cwd=ROOT, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, text=True, encoding="utf-8", bufsize=1)
    ready = json.loads(p.stdout.readline())
    if not ready.get("online"):
        print("talk program not online: no calls made")
        p.kill()
        return 1
    turns, replies, n = 0, [], 0
    hour = 11
    for who, lines in CONVERSATIONS:
        for say in lines:
            n += 1
            p.stdin.write(json.dumps({"id": n, "to": who, "say": say, "day": 1, "hour": hour, "minute": 10,
                                      "scene": "overcast, a dry October morning"}) + "\n")
            p.stdin.flush()
            t0 = time.time()
            first_s = None
            while True:
                line = p.stdout.readline()
                if not line:
                    break
                msg = json.loads(line)
                if msg.get("id") == n and "first" in msg and first_s is None:
                    first_s = round(time.time() - t0, 2)
                if msg.get("id") == n and "reply" in msg:
                    replies.append({"to": who, "say": say, "reply": msg.get("reply"), "ms": msg.get("ms"),
                                    "offline": msg.get("offline"), "wall_s": round(time.time() - t0, 2),
                                    "first_s": first_s, "went": msg.get("went"), "steps": msg.get("steps") or []})
                    break
            turns += 1
        hour += 1
    p.stdin.close()
    tail = p.stdout.read()
    p.wait(timeout=60)
    cost = None
    for line in tail.splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if "usd" in d:
            cost = d
    if sizes:
        print(size_summary(sizes, turns))
        return 0
    if cost is None:
        print("no cost report from the talk program")
        return 1
    offline = sum(1 for r in replies if r["offline"])
    per_turn = cost["usd"] / max(1, turns)
    lines = [
        "# What an hour of conversation costs, from real calls (%s)" % datetime.date.today().isoformat(),
        "",
        "Made by tools/talk_cost_sample.py: the game's own talk program, started as the game starts it, with the real key; "
        "three conversations of eight turns (Sheila, Ron, Darren). Its own cost report at the game's rate card (US dollars):",
        "",
        "- turns: %d (answered offline: %d); calls: %d" % (turns, offline, cost["calls"]),
        "- the session: US$%.4f; per turn: US$%.5f" % (cost["usd"], per_turn),
        "- an hour of steady talk at %d turns (one every %d seconds): **US$%.2f**; at 60 turns: US$%.2f; at 180: US$%.2f"
        % (per_hour, 3600 // per_hour, per_turn * per_hour, per_turn * 60, per_turn * 180),
        "- median time to the reply: %.1f s" % sorted(r["wall_s"] for r in replies)[len(replies) // 2],
    ] + (timing_lines(replies) if early else []) + [
        "",
        "Tokens by model:",
        "",
        "```",
        cost["cost"].strip(),
        "```",
        "",
        "The turns, what was said and what came back:",
        "",
    ] + ["- %s: \"%s\" -> \"%s\" (%.1f s%s%s)" % (r["to"], r["say"], (r["reply"] or "").replace("\n", " "), r["wall_s"],
                                                   ", first sentence %.1f s" % r["first_s"] if r.get("first_s") is not None else "",
                                                   ", " + r["went"] if r.get("went") else "") for r in replies]
    if live:
        tokens = {}
        for l in cost["cost"].splitlines():
            m = __import__("re").match(r"\s*([\w.-]+): (\d+) calls, (\d+) in / (\d+) out tokens", l)
            if m:
                tokens[m.group(1)] = {"calls": int(m.group(2)), "in": int(m.group(3)), "out": int(m.group(4))}
        with open(RUNS, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps({"date": datetime.date.today().isoformat(), "what": "talk_cost_sample --live" + (" --early" if early else ""),
                                 "turns": turns, "calls": cost["calls"], "tokens": tokens, "usd": round(cost["usd"], 4)}) + "\n")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("talkCost turns=%d calls=%d usd=%.4f perTurn=%.5f perHour@%d=%.2f -> %s" % (
        turns, cost["calls"], cost["usd"], per_turn, per_hour, per_turn * per_hour, out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
