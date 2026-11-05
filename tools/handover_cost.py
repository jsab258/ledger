#!/usr/bin/env python3
"""WHAT DOES EACH HANDOVER COST? Read from the project's own session logs, one line per hourly run of a day.

    python tools/handover_cost.py 2026-11-05            # a table, the day's totals and the switch point the numbers give

WHY, 5 November 2026 (the advisor's message 09, within his handover ruling of 3 November): the tokens of a fresh start, the
idle minutes between sessions, the sessions in a day and the minutes of work each; the switch point moves only if these say so.
Dollars are token_audit.py's: the same steps at published API prices, a measure to compare work, not his bill. Main sessions
only, helpers' logs left out. The start is a run's first 8 steps and the writing of its handover its last 8, a fixed cut.
"""
import datetime
import glob
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from token_audit import step_cost  # noqa: E402

LOGS = os.path.join(os.path.expanduser("~"), ".claude", "projects", "C--Users-Jafar-ledger-local")
EDGE = 8
MAX_LOG = 100 * 1024 * 1024  # the old long sessions, resumed by hand, are no hourly runs


def read_steps(path):
    steps = {}
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if '"assistant"' not in line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message") or {}
            if d.get("type") != "assistant" or d.get("isSidechain") or not m.get("usage") or m.get("model") == "<synthetic>":
                continue
            steps[m.get("id") or d.get("uuid")] = (d["timestamp"], m["usage"], m.get("model"))
    return sorted(steps.values(), key=lambda s: s[0])


def local(ts):
    return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()


def context(u):
    return (u.get("input_tokens", 0) or 0) + (u.get("cache_read_input_tokens", 0) or 0) + (u.get("cache_creation_input_tokens", 0) or 0)


def runs_of(day):
    runs = []
    for p in glob.glob(os.path.join(LOGS, "*.jsonl")):
        if os.path.getsize(p) > MAX_LOG:
            continue
        s = read_steps(p)
        if not s or local(s[0][0]).strftime("%Y-%m-%d") != day:
            continue
        cost = [step_cost(u, mdl) for _, u, mdl in s]
        ctx = [context(u) for _, u, _ in s]
        runs.append({"log": os.path.basename(p)[:8], "from": local(s[0][0]), "to": local(s[-1][0]), "steps": len(s), "usd": sum(cost),
                     "start": sum(cost[:EDGE]), "end": sum(cost[-EDGE:]), "ctx0": ctx[0], "ctxEdge": ctx[min(EDGE, len(ctx)) - 1], "ctxN": ctx[-1],
                     "startTokens": sum(ctx[:EDGE]), "endTokens": sum(ctx[-EDGE:])})
    return sorted(runs, key=lambda r: r["from"])


def main(a):
    day = a[0] if a else datetime.date.today().isoformat()
    runs = runs_of(day)
    work = [r for r in runs if r["steps"] > 2 * EDGE]
    idle = [r for r in runs if r["steps"] <= 2 * EDGE]
    print("from  to    min steps ctx-start ctx-end  usd   start  end  log")
    for r in runs:
        print("%s %s %4.0f %5d %8d %8d %6.2f %5.2f %5.2f %s" % (r["from"].strftime("%H:%M"), r["to"].strftime("%H:%M"),
              (r["to"] - r["from"]).total_seconds() / 60, r["steps"], r["ctxEdge"], r["ctxN"], r["usd"], r["start"], r["end"], r["log"]))
    if not work:
        print("no working session that day")
        return 0
    gaps = [(b["from"] - a_["to"]).total_seconds() / 60 for a_, b in zip(work, work[1:])]
    mins = [(r["to"] - r["from"]).total_seconds() / 60 for r in work]
    usd = sum(r["usd"] for r in work)
    print("working sessions %d; minutes each: mean %.0f, least %.0f, most %.0f" % (len(work), sum(mins) / len(mins), min(mins), max(mins)))
    if gaps:
        print("idle between them: mean %.0f min, most %.0f, total %.0f; working %.0f min of the span's %.0f" % (sum(gaps) / len(gaps), max(gaps), sum(gaps), sum(mins), sum(mins) + sum(gaps)))
    print("short runs (gate or rehearsal) %d, US$%.2f in all" % (len(idle), sum(r["usd"] for r in idle)))
    start, end = sum(r["start"] for r in work) / len(work), sum(r["end"] for r in work) / len(work)
    print("US$%.2f; a start US$%.2f (%.0f tokens summed), its handover's last steps US$%.2f; together %.0f%% of the day" % (
        usd, start, sum(r["startTokens"] for r in work) / len(work), end, 100 * (start + end) * len(work) / usd))
    # his ruling's formula (history_check.py): R a switch, T steps after it, the mean a step (R + h T + g T^2 / 2) / T
    r_tokens = sum(r["startTokens"] + r["endTokens"] for r in work) / len(work)
    h = sum(r["ctxEdge"] for r in work) / len(work)
    g = sum((r["ctxN"] - r["ctxEdge"]) / max(r["steps"] - EDGE, 1) for r in work) / len(work)
    t = math.sqrt(2 * r_tokens / g)
    print("R = %.0f tokens a switch, history from %.0f, growing %.0f a step: best T = %.0f steps, history %.0f at the switch" % (r_tokens, h, g, t, h + g * t))
    for point in (150000, 200000, 250000, 300000, 400000):
        tp = max((point - h) / g, 1)
        # in dollars too: a start is mostly cache written (US$8 a million), history only re-read (US$0.20), which the token sum weighs alike
        dollars = start / tp + (h + g * tp / 2) * 0.20 / 1e6
        print("  switch at %6d: T %4.0f steps, mean context a step %.0f, the start and history US$%.3f a step" % (point, tp, (r_tokens + h * tp + g * tp * tp / 2) / tp, dollars))
    print("  in dollars the best T = %.0f steps, history %.0f at the switch" % (math.sqrt(2 * start / (g * 0.20 / 1e6)), h + g * math.sqrt(2 * start / (g * 0.20 / 1e6))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
