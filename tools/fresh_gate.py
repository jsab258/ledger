#!/usr/bin/env python3
"""MAY THIS HOURLY RUN START LEDGER'S WORK? The first thing each run of the hourly fresh-session task does.

    python tools/fresh_gate.py            # one line: GO, or WAIT and why
    python tools/fresh_gate.py --selftest

WHY, 4 November 2026 (his ruling A2): "Replace the chaining with a recurring scheduled task, hourly from 05:15 to
00:45, permission mode Auto. Each run first checks the handover file and session activity, and starts work only when
the last session has stopped and no LEDGER session has been active for 15 minutes; otherwise it ends at once, having
read nothing else." The chaining of 3 November failed at 09:38 that morning: a scheduled run may not start another.

WHAT IT CHECKS, cheaply, before the run reads anything: the Swiss time (no work from 00:45 to 05:10, the night's jobs);
the handover's "**Started:**" and "**Stopped:**" lines (the last session has stopped when Stopped is later); the
project's session logs (no main log but this run's own written in the last 15 minutes). The app's session list is
the run's second check (mcp__ccd_session_mgmt__list_sessions), since only the app knows a session that is open but
not writing. A session that died without its Stopped line: when Started is later but no log has been written for
120 minutes, the last session is taken as stopped, and GO says so, for the handover.
"""
import datetime
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDOVER = os.path.join(ROOT, "production", "handover", "HANDOVER.md")
LOGS = os.path.join(os.path.expanduser("~"), ".claude", "projects", "C--Users-Jafar-ledger-local")
QUIET_MIN = 15
DEAD_MIN = 120
OWN_RUN_MIN = 10
STAMP = re.compile(r"(\d{4}-\d\d-\d\d) (\d\d:\d\d)")


def line_time(text, key):
    for line in text.splitlines():
        if line.startswith("**%s:**" % key):
            m = STAMP.search(line)
            return datetime.datetime.strptime(m.group(1) + " " + m.group(2), "%Y-%m-%d %H:%M") if m else None
    return None


def last_write_minutes(now_ts, logs=LOGS):
    """Minutes since any main session log was written, this run's own (created in the last minutes) left out."""
    ages = []
    for p in glob.glob(os.path.join(logs, "*.jsonl")):
        if now_ts - os.path.getctime(p) < OWN_RUN_MIN * 60:
            continue
        ages.append((now_ts - os.path.getmtime(p)) / 60)
    return min(ages) if ages else None


def decide(now, text, idle_min):
    hm = now.hour * 60 + now.minute
    if 45 <= hm < 5 * 60 + 10:
        return "WAIT the night (00:45 to 05:10): no work"
    started, stopped = line_time(text, "Started"), line_time(text, "Stopped")
    if started is None or stopped is None:
        return "WAIT the handover has no Started or Stopped line: a session must set them"
    if idle_min is not None and idle_min < QUIET_MIN:
        return "WAIT a session log was written %.0f minutes ago (under %d)" % (idle_min, QUIET_MIN)
    if stopped >= started:
        return "GO the last session stopped at %s; no log written for %s minutes" % (
            stopped.strftime("%H:%M"), "?" if idle_min is None else "%.0f" % idle_min)
    if idle_min is not None and idle_min >= DEAD_MIN:
        return "GO the last session (started %s) set no Stopped line but no log has been written for %.0f minutes: " \
               "taken as stopped; say so in the handover" % (started.strftime("%d %b %H:%M"), idle_min)
    return "WAIT the last session (started %s) has not stopped" % started.strftime("%d %b %H:%M")


def selftest():
    h = "**Started:** 2026-11-04 08:43 (x)\n**Stopped:** 2026-11-04 09:38 (y)\n"
    r = "**Started:** 2026-11-04 11:00 (x)\n**Stopped:** 2026-11-04 09:38 (y)\n"
    d = datetime.datetime(2026, 11, 4, 12, 15)
    cases = [
        ("stopped and quiet: GO", decide(d, h, 40), "GO"),
        ("stopped, a log 5 min ago: WAIT", decide(d, h, 5), "WAIT"),
        ("running: WAIT", decide(d, r, 40), "WAIT"),
        ("died without Stopped, quiet 3 h: GO", decide(d, r, 180), "GO"),
        ("the night: WAIT", decide(datetime.datetime(2026, 11, 5, 2, 15), h, 400), "WAIT"),
        ("00:15 still works: GO", decide(datetime.datetime(2026, 11, 5, 0, 15), h, 40), "GO"),
        ("no lines: WAIT", decide(d, "nothing", 40), "WAIT"),
    ]
    bad = [n for n, got, want in cases if not got.startswith(want)]
    print("fresh_gate selftest:", "passed" if not bad else "FAILED " + ", ".join(bad))
    return 1 if bad else 0


def main(a):
    if "--selftest" in a:
        return selftest()
    now = datetime.datetime.now()
    text = open(HANDOVER, encoding="utf-8").read() if os.path.isfile(HANDOVER) else ""
    print(decide(now, text, last_write_minutes(now.timestamp())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
