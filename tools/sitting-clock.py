#!/usr/bin/env python3
"""The stop hook's one job: while the sitting's goal is open and its time is
not up, keep going; when either ends, stop.

    python tools/sitting-clock.py --hook < payload.json   # the Stop hook's call
    python tools/sitting-clock.py --selftest

Jafar, 24 September, after the effort audit (production/audits/): every other
check this hook did - the standing list, the "For you:" line, the match against
FOR-JAFAR.md - is removed. It reads two lines of NOW.md:

    SITTING: started <ISO time with offset>, limit <N>h
    GOAL: open | <the sitting's goal>        (or GOAL: done | ...)

It acts only for the builder's own session: the untracked marker
.claude/builder-checkout must exist in the folder the session runs in and hold
that session's id. Everywhere else, and on anything it cannot read, it lets
the turn end and says why. Exit 2 keeps the turn going; exit 0 lets it end.
"""
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITTING_RE = re.compile(r"^SITTING:\s*started\s+(\S+)\s*,\s*limit\s+([0-9]+(?:\.[0-9]+)?)\s*h\s*$", re.M)
GOAL_RE = re.compile(r"^GOAL:\s*(open|done)\b", re.M | re.I)
PERMIT, BLOCK = 0, 2


def decide(now_text, now, in_scope=True, already_blocked=False):
    """(code, reason) for a stop at time `now` given NOW.md's text."""
    if not in_scope:
        return PERMIT, "not the builder's session, so this hook does not hold it"
    if already_blocked:
        return PERMIT, "the last stop was already held once; letting this one end"
    m = SITTING_RE.search(now_text or "")
    g = GOAL_RE.search(now_text or "")
    if not m or not g:
        return PERMIT, "no SITTING or GOAL line in NOW.md, so nothing to hold to"
    try:
        start = datetime.datetime.fromisoformat(m.group(1))
    except ValueError:
        return PERMIT, "the SITTING line's time could not be read"
    end = start + datetime.timedelta(hours=float(m.group(2)))
    if g.group(1).lower() == "done":
        return PERMIT, "the sitting's goal is marked done"
    if now >= end:
        return PERMIT, "the sitting's time is up"
    left = (end - now).total_seconds() / 3600.0
    return BLOCK, ("the sitting's goal is still open and %.1f h of its time remain: "
                   "keep going (mark GOAL: done in NOW.md when it is)" % left)


def hook():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        payload = {}
    cwd = payload.get("cwd") or os.getcwd()
    marker = os.path.join(cwd, ".claude", "builder-checkout")
    try:
        mine = open(marker, encoding="utf-8").read().strip()
    except OSError:
        mine = None
    in_scope = bool(mine) and mine == str(payload.get("session_id", "")).strip()
    try:
        text = open(os.path.join(cwd, "NOW.md"), encoding="utf-8").read()
    except OSError:
        text = ""
    code, why = decide(text, datetime.datetime.now().astimezone(), in_scope,
                       bool(payload.get("stop_hook_active")))
    print(("HOLD " if code == BLOCK else "PERMIT ") + why)
    return code


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("sitting-clock selftest FAIL " + name)
    t0 = datetime.datetime.fromisoformat("2026-09-24T13:00:00+02:00")
    open_goal = "SITTING: started 2026-09-24T13:00:00+02:00, limit 5h\nGOAL: open | the encounter\n"
    done_goal = open_goal.replace("GOAL: open", "GOAL: done")
    check("an open goal with time left holds", decide(open_goal, t0 + datetime.timedelta(hours=1))[0] == BLOCK)
    check("a done goal lets it stop", decide(done_goal, t0 + datetime.timedelta(hours=1))[0] == PERMIT)
    check("time up lets it stop", decide(open_goal, t0 + datetime.timedelta(hours=5, minutes=1))[0] == PERMIT)
    check("no lines, no hold", decide("nothing here", t0)[0] == PERMIT)
    check("another session is never held", decide(open_goal, t0, in_scope=False)[0] == PERMIT)
    check("a second stop in a row is let go", decide(open_goal, t0, already_blocked=True)[0] == PERMIT)
    print("sitting-clock selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--hook" in sys.argv:
        sys.exit(hook())
    print(__doc__)
