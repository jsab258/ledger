#!/usr/bin/env python3
"""The stop hook's one job: while the sitting's time remains and its list has an
item left, keep going; stop only when the time is up or the whole list is done.

    python tools/sitting-clock.py --hook < payload.json   # the Stop hook's call
    python tools/sitting-clock.py --selftest

Jafar, 24 September, after the effort audit (production/audits/): every other
check this hook did - the "For you:" line, the match against FOR-JAFAR.md - is
removed. CORRECTED BY HIM THE SAME EVENING: the sitting before finished its one
goal in an hour and stopped with four hours left, because it was told to stop
when the goal was done. A sitting now has a LIST IN ORDER; when an item is
done the next is taken without asking. It reads NOW.md:

    SITTING: started <ISO time with offset>, limit <N>h
    - [ ] an open item        - [x] a done one

A SECOND STOP IN A ROW IS HELD TOO: letting it through made the hook a
formality. What ends a loop is the work (an item ticked), the time limit, the
platform's own cap on consecutive holds, and SITTING_GUARD=off.

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
OPEN_RE = re.compile(r"^\s*- \[ \]", re.M)
PERMIT, BLOCK = 0, 2


def decide(now_text, now, in_scope=True, already_blocked=False):
    """(code, reason) for a stop at time `now` given NOW.md's text."""
    if not in_scope:
        return PERMIT, "not the builder's session, so this hook does not hold it"
    m = SITTING_RE.search(now_text or "")
    if not m:
        return PERMIT, "no SITTING line in NOW.md, so nothing to hold to"
    try:
        start = datetime.datetime.fromisoformat(m.group(1))
    except ValueError:
        return PERMIT, "the SITTING line's time could not be read"
    end = start + datetime.timedelta(hours=float(m.group(2)))
    if now >= end:
        return PERMIT, "the sitting's time is up"
    left_items = len(OPEN_RE.findall(now_text))
    if left_items == 0:
        return PERMIT, "the whole list is done"
    left = (end - now).total_seconds() / 3600.0
    return BLOCK, ("%d item(s) left on the list and %.1f h of the sitting remain: take the next one "
                   "(tick it - [x] in NOW.md when it is done)" % (left_items, left))


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
    listed = ("SITTING: started 2026-09-24T13:00:00+02:00, limit 5h\n"
              "- [x] 1. the first\n- [ ] 2. the second\n")
    all_done = listed.replace("- [ ] 2.", "- [x] 2.")
    one_hour = t0 + datetime.timedelta(hours=1)
    check("an item left with time left holds", decide(listed, one_hour)[0] == BLOCK)
    check("the whole list done lets it stop", decide(all_done, one_hour)[0] == PERMIT)
    check("time up lets it stop", decide(listed, t0 + datetime.timedelta(hours=5, minutes=1))[0] == PERMIT)
    check("no SITTING line, no hold", decide("- [ ] something", t0)[0] == PERMIT)
    check("another session is never held", decide(listed, one_hour, in_scope=False)[0] == PERMIT)
    check("a second stop in a row is held too", decide(listed, one_hour, already_blocked=True)[0] == BLOCK)
    print("sitting-clock selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--hook" in sys.argv:
        sys.exit(hook())
    print(__doc__)
