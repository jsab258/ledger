#!/usr/bin/env python3
"""MAY THIS HOURLY RUN START LEDGER'S WORK? The first thing each run of the hourly fresh-session task does.

    python tools/fresh_gate.py            # one line: GO, WAIT or REHEARSAL GO/WAIT, and why
    python tools/fresh_gate.py --selftest

WHY, 4 November 2026 (his ruling A2): "Replace the chaining with a recurring scheduled task, hourly from 05:15 to
00:45, permission mode Auto. Each run first checks the handover file and session activity, and starts work only when
the last session has stopped and no LEDGER session has been active for 15 minutes; otherwise it ends at once, having
read nothing else." The chaining of 3 November failed at 09:38 that morning: a scheduled run may not start another.

WHAT IT CHECKS, cheaply, before the run reads anything: the Swiss time (no work from 00:45 to 05:10, the night's jobs);
the handover's "**Started:**" and "**Stopped:**" lines (the last session has stopped when Stopped is later); the
project's own activity: the newest real turn (a user or assistant line with its timestamp) in any of the project's
session logs and their helpers' logs, this run's own log left out (CLAUDE_CODE_SESSION_ID). A session that died
without its Stopped line, or ended its turn idle without one: when Started is later but no turn has been written for
30 minutes and none of its own background jobs is still running, the last session is taken as stopped, and GO says
so, for the handover; 120 minutes while such a job runs.

30 MINUTES, NOT 120 (9 November, the advisor's message 64): his pasted message at about 15:31 resumed an old session,
which worked a turn and ended it idle with no Stopped line and no goal loop; the 16:40 and 17:21 starts waited on it
and nothing ran from about 16:00 to 18:15. A job of its own is a background command whose start ("backgroundTaskId")
is in the newest session's log and whose finish ("<task-id>") is not; helpers' turns already count as activity.

THREE MINUTES AFTER A WRITTEN STOP (5 November, his yes on his page): a session that stopped just before the quarter
past made the next run stand aside for an hour, his answers waiting up to about 75 minutes. Stopped later than Started
means the old session has declared itself finished, so 3 quiet minutes are enough; 15 stay when it has not.

WHY NOT A FILE'S TIME OR THE APP'S SESSION LIST (4 November, his message at 13:38): the 12:15 run stood aside because
the app listed an idle "Ledger Builder" session under remote control as active three minutes before (its
lastActivityAt moves without any turn); the 13:15 run stood aside because the app had appended bookkeeping lines
(artifact-autoreact-ledger, untimed) to two idle old logs fourteen minutes before, which moved their file times.
Neither was work. So only timed turns count, and the app's list is not consulted.

A RUN THAT ENDED AT WAIT IS NOT ACTIVITY (7 November, the advisor's message 20): Windows restarted the PC at 00:14 and
killed the 23:22 session before it wrote Stopped. Every hourly run after that ended at WAIT, and the next run counted
its few turns as a session's, so the idle time never passed about 60 minutes, DEAD_MIN was never reached, and nothing
started until he cleared it by hand, about 10:45. So a short log whose gate line says WAIT is left out. A log that went
on working after it, or any bigger one, still counts.

THE REHEARSAL (his message of 4 November: test the take-over itself, not only standing aside): while
production/handover/takeover-rehearsal.json exists and has not expired, the gate decides from the rehearsal's
handover instead and leaves out the logs it names (the working session standing in for the stopped one); its line
then begins REHEARSAL, and the task's prompt says what a rehearsal run does. The production session writes the file
and deletes it afterwards.
"""
import datetime
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDOVER = os.path.join(ROOT, "production", "handover", "HANDOVER.md")
REHEARSAL = os.path.join(ROOT, "production", "handover", "takeover-rehearsal.json")
LOGS = os.path.join(os.path.expanduser("~"), ".claude", "projects", "C--Users-Jafar-ledger-local")
QUIET_MIN = 15
QUIET_STOPPED_MIN = 3
DEAD_MIN = 30
DEAD_JOB_MIN = 120
JOB_START = re.compile(rb'"backgroundTaskId": ?"([A-Za-z0-9]+)"')
JOB_DONE = re.compile(rb'<task-id>([A-Za-z0-9]+)</task-id>')
OWN_RUN_MIN = 10
TAIL = 1 << 20
ROUND_CLOCK_UNTIL = datetime.datetime(2026, 11, 9, 13, 0)
WALK_HOLD_FROM, WALK_HOLD_UNTIL = 1 * 60 + 40, 3 * 60 + 30
NIGHTLY = os.path.join(ROOT, "production", "playtest", "nightly")
STAMP = re.compile(r"(\d{4}-\d\d-\d\d) (\d\d:\d\d)")
TURNS = (b'"type":"user"', b'"type":"assistant"')
WAIT_RUN_TURNS = 12
WAIT_RUN_BYTES = 4 << 20


def line_time(text, key):
    for line in text.splitlines():
        if line.startswith("**%s:**" % key):
            m = STAMP.search(line)
            return datetime.datetime.strptime(m.group(1) + " " + m.group(2), "%Y-%m-%d %H:%M") if m else None
    return None


def last_turn(path, size_cap=64 << 20):
    """The newest timed user or assistant line in a log, as a UTC timestamp, read from the end; None if none."""
    size = os.path.getsize(path)
    with open(path, "rb") as fh:
        end, block = size, TAIL
        while end > 0 and size - end < size_cap:
            start = max(0, end - block)
            fh.seek(start)
            lines = fh.read(end - start).split(b"\n")
            if start > 0:
                lines = lines[1:]
            for raw in reversed(lines):
                if not any(t in raw.replace(b" ", b"") for t in TURNS):
                    continue
                try:
                    d = json.loads(raw)
                except ValueError:
                    continue
                if d.get("type") in ("user", "assistant") and d.get("timestamp"):
                    return datetime.datetime.strptime(d["timestamp"][:19], "%Y-%m-%dT%H:%M:%S").replace(
                        tzinfo=datetime.timezone.utc).timestamp()
            end = start
    return None


def ended_at_wait(path):
    """True for an hourly run that stood aside: a short log, its gate's line WAIT. Anything longer did real work."""
    if os.path.getsize(path) > WAIT_RUN_BYTES:
        return False
    turns, waited = 0, False
    with open(path, "rb") as fh:
        for raw in fh:
            if not any(t in raw.replace(b" ", b"") for t in TURNS):
                continue
            try:
                d = json.loads(raw)
            except ValueError:
                continue
            if d.get("type") not in ("user", "assistant"):
                continue
            turns += 1
            if turns > WAIT_RUN_TURNS:
                return False
            content = (d.get("message") or {}).get("content")
            for b in content if isinstance(content, list) else ():
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    c = b.get("content")
                    text = c if isinstance(c, str) else " ".join(x.get("text", "") for x in c or () if isinstance(x, dict))
                    if text.startswith(("WAIT ", "REHEARSAL WAIT")):
                        waited = True
    return waited


def pending_jobs(path, cap=16 << 20):
    """Background commands started in a log and not reported finished there (read from its last 16 MB)."""
    with open(path, "rb") as fh:
        fh.seek(max(0, os.path.getsize(path) - cap))
        data = fh.read()
    return set(JOB_START.findall(data)) - set(JOB_DONE.findall(data))


def last_turn_minutes(now_ts, logs=LOGS, leave_out=(), own=None, with_log=False):
    """Minutes since the project's newest real turn, this run's own log and those named left out; with_log also
    gives the main session log that turn belongs to (a helper's turn gives its parent's log)."""
    paths = glob.glob(os.path.join(logs, "*.jsonl")) + glob.glob(os.path.join(logs, "*", "subagents", "*.jsonl"))
    newest, newest_log = None, None
    for p in paths:
        sid = os.path.basename(p)[:-6] if os.path.dirname(p) == logs else os.path.basename(os.path.dirname(os.path.dirname(p)))
        if sid in leave_out or (own and sid == own):
            continue
        if not own and os.path.dirname(p) == logs and now_ts - os.path.getctime(p) < OWN_RUN_MIN * 60:
            continue
        if os.path.dirname(p) == logs and ended_at_wait(p):
            continue
        if now_ts - os.path.getmtime(p) > DEAD_JOB_MIN * 60 * 2:
            t = os.path.getmtime(p)  # no turn is newer than the file; reading old giants would cost seconds
        else:
            t = last_turn(p)
        if t is not None and (newest is None or t > newest):
            newest, newest_log = t, os.path.join(logs, sid + ".jsonl")
    minutes = None if newest is None else (now_ts - newest) / 60
    return (minutes, newest_log) if with_log else minutes


def decide(now, text, idle_min, walk_reported=False, job_running=False):
    hm = now.hour * 60 + now.minute
    if now < ROUND_CLOCK_UNTIL:
        # ROUND THE CLOCK until Monday's 13:00 (6 November, his yes on his page, whole-allowance-2026-11-06). Only the
        # tester's walk stands everyone aside: the app's window takes the front from a working session and the walk then
        # sends no keys (3 November, 07:20); a walk that lost its keys passes nothing. Its report, or 03:30, ends the wait.
        if WALK_HOLD_FROM <= hm < WALK_HOLD_UNTIL and not walk_reported:
            return "WAIT the night's walk has not reported: nothing runs beside it"
    elif 45 <= hm < 5 * 60 + 10:
        return "WAIT the night (00:45 to 05:10): no work"
    started, stopped = line_time(text, "Started"), line_time(text, "Stopped")
    if started is None or stopped is None:
        return "WAIT the handover has no Started or Stopped line: a session must set them"
    quiet = QUIET_STOPPED_MIN if stopped >= started else QUIET_MIN
    if idle_min is not None and idle_min < quiet:
        return "WAIT a session wrote a turn %d minutes ago (under %d)" % (int(idle_min), quiet)
    if stopped >= started:
        return "GO the last session stopped at %s; no turn written for %s minutes" % (
            stopped.strftime("%H:%M"), "?" if idle_min is None else "%d" % int(idle_min))
    dead = DEAD_JOB_MIN if job_running else DEAD_MIN
    if idle_min is not None and idle_min >= dead:
        return "GO the last session (started %s) set no Stopped line but no turn has been written for %d minutes: " \
               "taken as stopped; say so in the handover" % (started.strftime("%d %b %H:%M"), int(idle_min))
    return "WAIT the last session (started %s) has not stopped%s" % (
        started.strftime("%d %b %H:%M"), "; a background job of its own is still running" if job_running else "")


def rehearsal(now):
    """The rehearsal's settings while its file exists and has not expired, else None."""
    if not os.path.isfile(REHEARSAL):
        return None
    r = json.load(open(REHEARSAL, encoding="utf-8"))
    if now > datetime.datetime.strptime(r["expires"], "%Y-%m-%d %H:%M"):
        return None
    return r


def selftest():
    import tempfile
    h = "**Started:** 2026-11-04 08:43 (x)\n**Stopped:** 2026-11-04 09:38 (y)\n"
    r = "**Started:** 2026-11-04 11:00 (x)\n**Stopped:** 2026-11-04 09:38 (y)\n"
    d = datetime.datetime(2026, 11, 4, 12, 15)
    cases = [
        ("stopped and quiet: GO", decide(d, h, 40), "GO"),
        ("stopped, a turn 2.9 min ago: WAIT", decide(d, h, 2.9), "WAIT"),
        ("stopped, a turn 3 min ago: GO", decide(d, h, 3), "GO"),
        ("not stopped, a turn 5 min ago: WAIT, 15", decide(d, r, 5), "WAIT a session wrote"),
        ("not stopped, a turn 14.6 min ago: WAIT, 15", decide(d, r, 14.6), "WAIT a session wrote"),
        ("running: WAIT", decide(d, r, 20), "WAIT"),
        ("died without Stopped, quiet 3 h: GO", decide(d, r, 180), "GO"),
        ("ended its turn idle, no Stopped, quiet 29 min: WAIT", decide(d, r, 29), "WAIT"),
        ("ended its turn idle, no Stopped, quiet 30 min: GO", decide(d, r, 30), "GO"),
        ("no Stopped, quiet 45 min, its own job running: WAIT", decide(d, r, 45, job_running=True), "WAIT"),
        ("no Stopped, quiet 125 min, its job never reported: GO", decide(d, r, 125, job_running=True), "GO"),
        ("until Monday, 00:50: GO", decide(datetime.datetime(2026, 11, 7, 0, 50), h, 400), "GO"),
        ("until Monday, the walk not reported, 02:15: WAIT", decide(datetime.datetime(2026, 11, 7, 2, 15), h, 400), "WAIT the night's walk"),
        ("until Monday, the walk reported, 02:45: GO", decide(datetime.datetime(2026, 11, 7, 2, 45), h, 400, True), "GO"),
        ("until Monday, no report by 03:30: GO", decide(datetime.datetime(2026, 11, 7, 3, 30), h, 400), "GO"),
        ("after Monday's 13:00, the night: WAIT", decide(datetime.datetime(2026, 11, 10, 2, 15), h, 400), "WAIT the night"),
        ("after Monday's 13:00, 00:15 still works: GO", decide(datetime.datetime(2026, 11, 10, 0, 15), h, 40), "GO"),
        ("no lines: WAIT", decide(d, "nothing", 40), "WAIT"),
    ]
    # The project's own activity, from logs made here: an idle log the app keeps appending untimed bookkeeping to
    # (13:15's fault) must not count; a real turn must; this run's own log and a left-out log must not.
    tmp = tempfile.mkdtemp(prefix="fresh_gate_")
    now_ts = datetime.datetime(2026, 11, 4, 12, 21, tzinfo=datetime.timezone.utc).timestamp()

    def log(name, turn_utc, untimed=0, sub=False):
        p = os.path.join(tmp, name, "subagents", "agent-x.jsonl") if sub else os.path.join(tmp, name + ".jsonl")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"type": "user", "timestamp": turn_utc + ".000Z", "message": {"content": "x"}}) + "\n")
            fh.write(json.dumps({"type": "assistant", "timestamp": turn_utc + ".500Z", "message": {"content": []}}) + "\n")
            for _ in range(untimed):
                fh.write(json.dumps({"type": "artifact-autoreact-ledger", "v": 1, "artifacts": {}}) + "\n")
        os.utime(p, (now_ts - 60, now_ts - 60))
        return p

    log("idle-builder", "2026-11-04T09:04:12", untimed=5)
    m1 = last_turn_minutes(now_ts, tmp, own="none-such")
    log("own-run", "2026-11-04T12:20:00")
    m2 = last_turn_minutes(now_ts, tmp, own="own-run")
    log("standing-in", "2026-11-04T12:19:00")
    m3 = last_turn_minutes(now_ts, tmp, leave_out=("standing-in",), own="own-run")
    m4 = last_turn_minutes(now_ts, tmp, own="own-run")
    log("helper", "2026-11-04T12:18:00", sub=True)
    m5 = last_turn_minutes(now_ts, tmp, leave_out=("standing-in",), own="own-run")
    # A killed session, then hourly runs that each ended at WAIT (7 November): the runs must not read as activity, so
    # the idle time reaches DEAD_MIN and the next run goes; a run that said WAIT and then worked still counts.
    tmp2 = tempfile.mkdtemp(prefix="fresh_gate_wait_")

    def run_log(name, turn_utc, gate_line, extra=0):
        with open(os.path.join(tmp2, name + ".jsonl"), "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"type": "user", "timestamp": turn_utc + ".000Z", "message": {"content": "prompt"}}) + "\n")
            fh.write(json.dumps({"type": "user", "timestamp": turn_utc + ".100Z", "message": {"content": [
                {"type": "tool_result", "content": [{"type": "text", "text": gate_line}]}]}}) + "\n")
            for _ in range(extra):
                fh.write(json.dumps({"type": "assistant", "timestamp": turn_utc + ".500Z", "message": {"content": []}}) + "\n")
        os.utime(os.path.join(tmp2, name + ".jsonl"), (now_ts - 60, now_ts - 60))

    run_log("killed", "2026-11-04T08:00:00", "GO the last session stopped", extra=40)
    run_log("wait-1", "2026-11-04T10:21:00", "WAIT the last session (started 04 Nov 09:00) has not stopped", extra=2)
    run_log("wait-2", "2026-11-04T11:21:00", "WAIT the last session (started 04 Nov 09:00) has not stopped", extra=2)
    m6 = last_turn_minutes(now_ts, tmp2, own="own-run")
    run_log("rehearsal-wait", "2026-11-04T11:40:00", "REHEARSAL WAIT a session wrote a turn", extra=2)
    m7 = last_turn_minutes(now_ts, tmp2, own="own-run")
    run_log("waited-then-worked", "2026-11-04T11:50:00", "WAIT a session wrote a turn 2 minutes ago", extra=30)
    m8 = last_turn_minutes(now_ts, tmp2, own="own-run")
    # A background job of the newest session: pending until its <task-id> notification is in the same log.
    jl = os.path.join(tmp2, "job-session.jsonl")
    with open(jl, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"type": "user", "timestamp": "2026-11-04T11:55:00.000Z", "toolUseResult": {
            "backgroundTaskId": "bjob1"}, "message": {"content": "x"}}) + "\n")
    os.utime(jl, (now_ts - 60, now_ts - 60))
    m9, log9 = last_turn_minutes(now_ts, tmp2, own="own-run", with_log=True)
    pend = pending_jobs(log9) if log9 else set()
    with open(jl, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"type": "user", "timestamp": "2026-11-04T12:00:00.000Z", "message": {
            "content": "<task-notification>\n<task-id>bjob1</task-id>\n<status>completed</status>"}}) + "\n")
    os.utime(jl, (now_ts - 60, now_ts - 60))
    done = pending_jobs(jl)
    cases += [
        ("the newest session's log is named", "%s" % (log9 == jl), "True"),
        ("a started job without its finish is pending", "%s" % (pend == {b"bjob1"}), "True"),
        ("a job with its finish is not pending", "%s" % (done == set()), "True"),
        ("killed, then WAIT runs: they are not activity, 261 min", "%s" % (m6 is not None and 255 < m6 < 265), "True"),
        ("killed, then WAIT runs: the next run goes", decide(d, r, m6), "GO"),
        ("a rehearsal's WAIT is not activity either", "%s" % (m7 is not None and 255 < m7 < 265), "True"),
        ("a run that waited and then worked counts", "%s" % (m8 is not None and m8 < 32), "True"),
        ("untimed bookkeeping on an idle log does not count: 196 min", "%s" % (m1 is not None and 190 < m1 < 200), "True"),
        ("this run's own log left out", "%s" % (m2 is not None and m2 > 190), "True"),
        ("a left-out log does not count", "%s" % (m3 is not None and m3 > 190), "True"),
        ("a real turn 2 min ago counts", "%s" % (m4 is not None and m4 < 3), "True"),
        ("a helper's turn counts", "%s" % (m5 is not None and m5 < 4), "True"),
    ]
    bad = [n for n, got, want in cases if not got.startswith(want)]
    print("fresh_gate selftest:", "passed (%d cases)" % len(cases) if not bad else "FAILED " + ", ".join(bad))
    return 1 if bad else 0


def main(a):
    if "--selftest" in a:
        return selftest()
    now = datetime.datetime.now()
    own = os.environ.get("CLAUDE_CODE_SESSION_ID")
    r = rehearsal(now)
    path = os.path.join(ROOT, r["handover"]) if r else HANDOVER
    text = open(path, encoding="utf-8").read() if os.path.isfile(path) else ""
    reported = os.path.isfile(os.path.join(NIGHTLY, now.strftime("%Y-%m-%d") + ".md"))
    idle, log = last_turn_minutes(now.timestamp(), leave_out=tuple(r["leave_out"]) if r else (), own=own, with_log=True)
    job = bool(log and os.path.isfile(log) and pending_jobs(log))
    line = decide(now, text, idle, reported, job)
    print(("REHEARSAL " + line + " (rehearsal handover %s; left out %s)" % (r["handover"], ", ".join(r["leave_out"])))
          if r else line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
