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
import glob
import json
import os
import sys

LOGS = os.path.join(os.path.expanduser("~"), ".claude", "projects", "C--Users-Jafar-ledger-local")
THRESHOLD = 200000  # 4 Nov, his ruling A3: about 300,000 while the start was heavy; set 4 Nov 16:25 from the cost per step
# (the first real take-over's own log: a start of about 542,000 tokens summed over its 6 steps, the handover's writing about
# as much again, so R = 1.1 M a switch; the history grew 1,488 tokens a step from 101,559. The mean cost a step over T steps,
# (R + 101,559 T + 1,488 T^2 / 2) / T, is least at T = sqrt(2R / 1,488) = 38 steps, about 158,000 a step at about 160,000 of
# history; 200,000 leaves room for an item to end and costs about 6% over that, against about 25% at 300,000)
TAIL_BYTES = 4 * 1024 * 1024


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
        ok.append(("a step past the threshold is over", last_context(b) >= THRESHOLD and last_context(a) < THRESHOLD))
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
    print("historyCheck context=%dk threshold=%dk verdict=%s log=%s" % (ctx // 1000, THRESHOLD // 1000,
                                                                       "OVER" if ctx >= THRESHOLD else "UNDER", os.path.basename(path)))
    sys.exit(0)
