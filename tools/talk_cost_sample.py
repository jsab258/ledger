#!/usr/bin/env python3
"""What an hour of conversation costs, from real calls: a scripted sample of turns through the game's own talk program.

    python tools/talk_cost_sample.py [--turns-per-hour 120] [--out production/playtest/talk-cost-<date>.md]

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
SECRETS = os.path.join(os.path.expanduser("~"), "AppData", "LocalLow", "DefaultCompany", "ledger", "secrets.json")
DLL = os.path.join(ROOT, "ledger", "TalkHelper", "bin", "Release", "net8.0", "TalkHelper.dll")

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


def main(argv):
    per_hour = int(argv[argv.index("--turns-per-hour") + 1]) if "--turns-per-hour" in argv else 120
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(
        ROOT, "production", "playtest", "talk-cost-%s.md" % datetime.date.today().isoformat())
    env = dict(os.environ)
    env["ANTHROPIC_API_KEY"] = json.load(open(SECRETS, encoding="utf-8"))["anthropic_api_key"]
    env.pop("LEDGER_TALK_FAKE", None)
    p = subprocess.Popen(["dotnet", DLL], cwd=ROOT, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
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
            while True:
                line = p.stdout.readline()
                if not line:
                    break
                msg = json.loads(line)
                if msg.get("id") == n and "reply" in msg:
                    replies.append({"to": who, "say": say, "reply": msg.get("reply"), "ms": msg.get("ms"),
                                    "offline": msg.get("offline"), "wall_s": round(time.time() - t0, 2)})
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
        "",
        "Tokens by model:",
        "",
        "```",
        cost["cost"].strip(),
        "```",
        "",
        "The turns, what was said and what came back:",
        "",
    ] + ["- %s: \"%s\" -> \"%s\" (%.1f s)" % (r["to"], r["say"], (r["reply"] or "").replace("\n", " "), r["wall_s"]) for r in replies]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("talkCost turns=%d calls=%d usd=%.4f perTurn=%.5f perHour@%d=%.2f -> %s" % (
        turns, cost["calls"], cost["usd"], per_turn, per_hour, per_turn * per_hour, out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
