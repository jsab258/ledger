#!/usr/bin/env python3
"""IS THIS SESSION'S HISTORY PAST THE POINT WHERE EACH STEP STARTS COSTING MORE? Read from its own session log.

    python tools/history_check.py            # the working session's context at its last step, and OVER or UNDER
    python tools/history_check.py --selftest

WHY, 3 November 2026 (his ruling, changing point 2 of his efficiency fixes): "switch to a fresh session by the history's
size, not by the clock. At the end of each item, measure this session's history from its own session log; when it passes
a threshold you set from your token audit (where the cost per step starts climbing), write the handover, stop, and let a
fresh session start from the handover file and the order with this same goal."

THE THRESHOLD, from the token audit's own reading of this PC's session logs (tools/token_audit.py read_log; the six newest
logs, 3 November, 42,563 steps): a step's cost holds at about US$0.068 to 0.069 with 100,000 to 200,000 tokens of context,
then climbs with every 50,000 more: 0.077, 0.085, 0.095, 0.110 ... 0.150 at 550,000 to 600,000 and 0.196 beyond. So the
knee is 200,000 tokens: past it each step re-reads more than it works.

WHICH LOG: the project's newest main session log (~/.claude/projects/C--Users-Jafar-ledger-local/*.jsonl, helpers'
logs excluded), which is the working session's because two sessions never work at once (his ruling). Read from its end
only (a long session's log runs to hundreds of MB): the last assistant step's input, cache-read and cache-written tokens,
as token_audit.py counts a step's context.
"""
import datetime
import glob
import json
import os
import sys

LOGS = os.path.join(os.path.expanduser("~"), ".claude", "projects", "C--Users-Jafar-ledger-local")
THRESHOLD = 250000  # 5 Nov 20:25, from 5 Nov's twelve take-overs (tools/handover_cost.py): the start now reaches 140,000, so 200,000
# left 23 steps; best by tokens about 261,000, by dollars about 302,000, flat from 250,000 to 400,000; items end about 40,000 past it
# Before: 4 Nov, his ruling A3: about 300,000 while the start was heavy; set 4 Nov 16:25 from the cost per step
# (the first real take-over's own log: a start of about 542,000 tokens summed over its 6 steps, the handover's writing about
# as much again, so R = 1.1 M a switch; the history grew 1,488 tokens a step from 101,559. The mean cost a step over T steps,
# (R + 101,559 T + 1,488 T^2 / 2) / T, is least at T = sqrt(2R / 1,488) = 38 steps, about 158,000 a step at about 160,000 of
# history; 200,000 leaves room for an item to end and costs about 6% over that, against about 25% at 300,000)
TAIL_BYTES = 4 * 1024 * 1024
# 5 Nov, the advisor's message 10 (half the day idle between sessions; a step costs about the same from 250,000 to 400,000): past
# THRESHOLD the size says a switch is due, and the clock only picks which item's end: one 5 to 15 minutes before the next run,
# so it takes over at once. HARD_STOP ends the wait whatever the clock. RUN_MINUTE is when the hourly task really fires: :21 in all
# 20 runs of 5 Nov (tools/handover_cost.py), though set for :15. The gate needs 3 quiet minutes, so 5 before leaves room.
HARD_STOP = 400000
RUN_MINUTE = 21
WINDOW_MINUTES = (5, 15)


def verdict(ctx, minute):
    """OVER or UNDER for a context at a minute of the hour, with why."""
    if ctx >= HARD_STOP:
        return "OVER", "hard stop"
    if ctx < THRESHOLD:
        return "UNDER", "below the point"
    left = (RUN_MINUTE - minute) % 60
    if WINDOW_MINUTES[0] <= left <= WINDOW_MINUTES[1]:
        return "OVER", "%d min before the next run" % left
    return "UNDER", "past the point, %d min to the next run: take the next item or the next part of one" % left


def newest_log(logs=LOGS, own=None):
    """This session's own log when its id is known (CLAUDE_CODE_SESSION_ID), else the newest. 4 November: the app
    appends untimed bookkeeping to idle old logs, which moves their file times, so the newest file can be another's."""
    if own:
        p = os.path.join(logs, own + ".jsonl")
        if os.path.isfile(p):
            return p
    paths = [p for p in glob.glob(os.path.join(logs, "*.jsonl")) if os.path.isfile(p)]
    return max(paths, key=os.path.getmtime) if paths else None


def last_context(path, tail=TAIL_BYTES):
    """The context of the log's last assistant step that carries usage, or None."""
    size = os.path.getsize(path)
    with open(path, "rb") as fh:
        fh.seek(max(0, size - tail))
        chunk = fh.read().decode("utf-8", "replace")
    for line in reversed(chunk.splitlines()):
        if '"usage"' not in line or '"assistant"' not in line:
            continue
        try:
            d = json.loads(line)
        except ValueError:
            continue
        m = d.get("message") or {}
        u = m.get("usage") if isinstance(m, dict) else None
        if d.get("type") == "assistant" and isinstance(u, dict):
            return (u.get("input_tokens", 0) or 0) + (u.get("cache_read_input_tokens", 0) or 0) + (u.get("cache_creation_input_tokens", 0) or 0)
    return None


def selftest():
    import tempfile
    ok = []
    with tempfile.TemporaryDirectory() as d:
        a = os.path.join(d, "a.jsonl")
        b = os.path.join(d, "b.jsonl")
        with open(a, "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"type": "assistant", "message": {"usage": {"input_tokens": 5, "cache_read_input_tokens": 100}}}) + "\n")
        with open(b, "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"type": "assistant", "message": {"usage": {"input_tokens": 1, "cache_read_input_tokens": 150000,
                                                                            "cache_creation_input_tokens": 160000}}}) + "\n")
            fh.write(json.dumps({"type": "user", "message": {"content": "x"}}) + "\n")
        os.utime(a, (1, 1))
        ok.append(("the newest log is the working session's", newest_log(d) == b))
        ok.append(("its last step's context counts input, cache reads and writes", last_context(b) == 310001))
        ok.append(("past the point inside the window is over", verdict(last_context(b), 10)[0] == "OVER"))
        ok.append(("below the point is under, whatever the clock", verdict(last_context(a), 10)[0] == "UNDER"))
        ok.append(("past the point outside the window takes the next item", verdict(300000, 30)[0] == "UNDER"))
        ok.append(("the window's edges: 15 and 5 minutes before", verdict(300000, 6)[0] == "OVER" and verdict(300000, 16)[0] == "OVER"))
        ok.append(("too close to the run to go quiet in time", verdict(300000, 18)[0] == "UNDER"))
        ok.append(("the hard stop ignores the clock", verdict(400000, 30)[0] == "OVER"))
        ok.append(("no log, no answer", newest_log(os.path.join(d, "none")) is None))
        ok.append(("its own log by its id, even when another was touched since", newest_log(d, own="a") == a))
    for name, good in ok:
        print("  %s %s" % ("ok  " if good else "FAIL", name))
    n = sum(1 for _, g in ok if g)
    print("history_check selftest: passed=%d/%d failed=%d" % (n, len(ok), len(ok) - n))
    return 0 if n == len(ok) else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    path = newest_log(own=os.environ.get("CLAUDE_CODE_SESSION_ID"))
    ctx = last_context(path) if path else None
    if ctx is None:
        print("historyCheck verdict=UNREAD log=%s" % path)
        sys.exit(2)
    word, why = verdict(ctx, datetime.datetime.now().minute)
    print("historyCheck context=%dk threshold=%dk hardStop=%dk verdict=%s (%s) log=%s" % (ctx // 1000, THRESHOLD // 1000, HARD_STOP // 1000,
                                                                                         word, why, os.path.basename(path)))
    sys.exit(0)
