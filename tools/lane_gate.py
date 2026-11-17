#!/usr/bin/env python3
"""MAY THIS HOURLY RUN START THE LANE? The first thing each run of the scheduled task "LEDGER: the lane session" does.

    python tools/lane_gate.py              # one line: LANE GO, LANE WAIT or LANE STOPPED, and why
    python tools/lane_gate.py --history    # at an item's end: OVER or UNDER for the lane's own history (and the clock)
    python tools/lane_gate.py --spend HH:MM  # the lane's own list-price dollars since then, for its "Lane row"
    python tools/lane_gate.py --selftest

WHY, 17 November 2026 (his picks of about 16:05, advisor 202; RULINGS "7, 10 Nov", the "16 to 23 Nov" part, and "one
session at a time (this week's lane aside)"): for this week only a second Claude session, the lane, does work that never
touches the machine (the next order's research, plans and code needing no build; reviews of plans and specs; Kiln
research and code review, never Kiln runs). It works in its own sparse worktree (C:/Users/Jafar/ledger-lane, branch
lane), is merged by the main session at item ends, and stops by itself at Monday 23 November 07:00.

WHAT IT READS, AND ONLY THIS: the lane's own handover (production/lane/LANE-HANDOVER.md in the lane's worktree, its
"**Started:**" and "**Stopped:**" lines) and the lane's own session logs (the Claude project folder of the lane's worktree,
~/.claude/projects/C--Users-Jafar-ledger-lane, with its helpers' logs). It never reads the main session's handover or
logs, and the main gate (tools/fresh_gate.py) never reads the lane's: the two decide apart. The one outside reading is
the night walk's report (production/playtest/nightly/<day>.md in the main checkout): from 01:40 until that report, or
03:30, the lane waits too, because a working Claude window takes the front and the tester's walk then sends no keys
(3 November, 07:20); that is the tester, not the main session.

HOW IT DECIDES (fresh_gate.py's way of reading logs, on the lane's own folder): only timed user or assistant turns count;
this run's own log (CLAUDE_CODE_SESSION_ID) is left out, as are short logs of lane runs that ended at LANE WAIT or
LANE STOPPED and logs a script's `claude -p` wrote. Past 2026-11-23 07:00: LANE STOPPED. A turn in the last 15 minutes
(18 s when the last lane session wrote its Stopped line): WAIT. No Stopped line after the Started line, and Started
within the last 30 minutes, or a turn within 30 minutes, or a background command of the lane's still pending: WAIT.
Otherwise GO (a lane session that died without its Stopped line is taken as stopped after 30 quiet minutes; GO says
so, for the lane's handover). It also refuses to GO from any folder but the lane's worktree on branch lane.

--history: the main tools/history_check.py reads the main project's logs, so in the lane it would measure the wrong
session. This reads the lane's own log with history_check's own threshold and verdict, its run minute taken from the
lane handover's Started line (an hourly task fires at about the same minute), and says OVER regardless once the lane's
end (23 Nov 07:00) or the night walk's hold (from 01:25, ahead of 01:40) is reached.

--spend: token_measures.py --spend reads the main project's logs; this sums the lane's own logs and helpers' logs at the
same published prices.
"""
import datetime
import glob
import json
import os
import re
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import fresh_gate  # noqa: E402  (its pure log readers: last_turn, pending_jobs, script_run, line_time)

LANE_DIR = os.environ.get("LEDGER_LANE_DIR", "C:/Users/Jafar/ledger-lane")
MAIN_DIR = os.environ.get("LEDGER_MAIN_DIR", "C:/Users/Jafar/ledger-local")
BRANCH = "lane"
LANE_HANDOVER = os.path.join(LANE_DIR, "production", "lane", "LANE-HANDOVER.md")
LANE_LOGS = os.path.join(os.path.expanduser("~"), ".claude", "projects",
                         re.sub(r"[^A-Za-z0-9]", "-", os.path.normpath(LANE_DIR)))
NIGHTLY = os.path.join(MAIN_DIR, "production", "playtest", "nightly")
END = datetime.datetime(2026, 11, 23, 7, 0)
QUIET_MIN = 15
QUIET_STOPPED_MIN = 0.3
DEAD_MIN = 30
STARTED_HOLD_MIN = 30
DEAD_JOB_MIN = 120
OWN_RUN_MIN = 10
WALK_HOLD_FROM, WALK_HOLD_UNTIL = 1 * 60 + 40, 3 * 60 + 30
WALK_STAND_ASIDE = 1 * 60 + 25     # --history says OVER from here, so the lane has handed over before 01:40
TURNS = fresh_gate.TURNS
WAIT_RUN_TURNS = 12
WAIT_RUN_BYTES = 4 << 20
WAIT_LINES = ("LANE WAIT", "LANE STOPPED")


def same_dir(a, b):
    return os.path.normcase(os.path.normpath(os.path.abspath(a))) == os.path.normcase(os.path.normpath(os.path.abspath(b)))


def ended_at_wait(path):
    """True for a lane run that stood aside: a short log whose gate line says LANE WAIT or LANE STOPPED."""
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
                    if text.strip().startswith(WAIT_LINES):
                        waited = True
    return waited


def lane_activity(now_ts, logs=LANE_LOGS, own=None):
    """(minutes since the lane's newest real turn or None, True when a lane log with a turn in DEAD_JOB_MIN minutes
    still holds a background command not reported finished)."""
    paths = glob.glob(os.path.join(logs, "*.jsonl")) + glob.glob(os.path.join(logs, "*", "subagents", "*.jsonl"))
    newest, job = None, False
    for p in paths:
        top = os.path.dirname(p) == logs
        sid = os.path.basename(p)[:-6] if top else os.path.basename(os.path.dirname(os.path.dirname(p)))
        if own and sid == own:
            continue
        if not own and top and now_ts - os.path.getctime(p) < OWN_RUN_MIN * 60:
            continue
        if top and (ended_at_wait(p) or fresh_gate.script_run(p)):
            continue
        if now_ts - os.path.getmtime(p) > DEAD_JOB_MIN * 60 * 2:
            t = os.path.getmtime(p)
        else:
            t = fresh_gate.last_turn(p)
        if t is not None and (newest is None or t > newest):
            newest = t
        if t is not None and now_ts - t < DEAD_JOB_MIN * 60 and fresh_gate.pending_jobs(p):
            job = True
    return (None if newest is None else (now_ts - newest) / 60), job


def decide(now, text, idle_min, job_running=False, walk_reported=False, place_ok=True, place_why=""):
    if now >= END:
        return "LANE STOPPED: after 2026-11-23 07:00 (the lane was for 16 to 23 Nov only; end at once, write nothing)"
    if not place_ok:
        return "LANE WAIT not the lane's worktree: %s (the lane runs only in %s on branch %s)" % (place_why, LANE_DIR, BRANCH)
    hm = now.hour * 60 + now.minute
    if WALK_HOLD_FROM <= hm < WALK_HOLD_UNTIL and not walk_reported:
        return "LANE WAIT the night's walk has not reported: no Claude window works beside it (3 Nov)"
    started, stopped = fresh_gate.line_time(text, "Started"), fresh_gate.line_time(text, "Stopped")
    if started is None:
        if idle_min is not None and idle_min < QUIET_MIN:
            return "LANE WAIT a lane session wrote a turn %.1f minutes ago, though the handover has no Started time" % idle_min
        return "LANE GO no lane session has started yet (the lane handover has no Started time)"
    if stopped is not None and stopped >= started:
        if idle_min is not None and idle_min < QUIET_STOPPED_MIN:
            return "LANE WAIT a lane session wrote a turn %.1f minutes ago" % idle_min
        return "LANE GO the last lane session stopped at %s; no lane turn for %s minutes%s" % (
            stopped.strftime("%d %b %H:%M"), "?" if idle_min is None else "%d" % int(idle_min),
            "; a background command of the last lane session still runs: leave it, take its result" if job_running else "")
    if idle_min is not None and idle_min < QUIET_MIN:
        return "LANE WAIT a lane session wrote a turn %.1f minutes ago (under %d)" % (idle_min, QUIET_MIN)
    if job_running:
        return "LANE WAIT the lane session started %s has not stopped: a background command it started still runs" % (
            started.strftime("%d %b %H:%M"))
    since_start = (now - started).total_seconds() / 60
    if since_start < STARTED_HOLD_MIN:
        return "LANE WAIT the lane session started %s (%d min ago) has no Stopped line yet" % (
            started.strftime("%d %b %H:%M"), max(0, int(since_start)))
    if idle_min is None or idle_min >= DEAD_MIN:
        return "LANE GO the lane session started %s set no Stopped line but no lane turn for %s minutes: taken as " \
               "stopped; say so in the lane handover" % (started.strftime("%d %b %H:%M"),
                                                       "?" if idle_min is None else "%d" % int(idle_min))
    return "LANE WAIT the lane session started %s has not stopped (last turn %d min ago)" % (
        started.strftime("%d %b %H:%M"), int(idle_min))


def place_check(root=ROOT):
    if not same_dir(root, LANE_DIR):
        return False, "this copy is %s" % root
    try:
        b = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root, capture_output=True, text=True,
                           timeout=20).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return False, "git could not be read"
    if b != BRANCH:
        return False, "the branch is %s" % (b or "unknown")
    return True, ""


# ---- --history and --spend --------------------------------------------------------------------------------------

def history_line(now, text, logs=LANE_LOGS, own=None, ctx=None):
    import history_check
    started = fresh_gate.line_time(text, "Started")
    if now >= END:
        return "laneHistory verdict=OVER (the lane's end, 23 Nov 07:00: hand over and stop)"
    hm = now.hour * 60 + now.minute
    if WALK_STAND_ASIDE <= hm < WALK_HOLD_UNTIL:
        return "laneHistory verdict=OVER (the night walk's hold starts 01:40: hand over and stop)"
    path = None
    if ctx is None:
        path = history_check.newest_log(logs, own)
        ctx = history_check.last_context(path) if path else None
    if ctx is None:
        return "laneHistory verdict=UNREAD log=%s" % path
    keep = history_check.RUN_MINUTE
    try:
        if started is not None:
            history_check.RUN_MINUTE = started.minute
        word, why = history_check.verdict(ctx, now.minute)
    finally:
        history_check.RUN_MINUTE = keep
    return "laneHistory context=%dk threshold=%dk verdict=%s (%s; run minute %s) log=%s" % (
        ctx // 1000, history_check.THRESHOLD // 1000, word, why, "?" if started is None else "%02d" % started.minute,
        os.path.basename(path) if path else "-")


def spend_line(hhmm, logs=LANE_LOGS, now=None):
    import token_measures as tm
    now = now or datetime.datetime.now()
    since = tm.since_time(hhmm, now)
    stamp = since.timestamp()
    paths = [p for p in glob.glob(os.path.join(logs, "*.jsonl")) + glob.glob(os.path.join(logs, "*", "subagents", "*.jsonl"))
             if os.path.getmtime(p) >= stamp]
    steps = [s for p in paths for s in tm.read_events(p)["steps"] if s["t"] >= since]
    dollars = sum(tm.step_cost(s["u"], s["model"]) for s in steps)
    hours = max((now - since).total_seconds() / 3600, 1e-6)
    models = sorted({s["model"] for s in steps if s.get("model")})
    return "lane spend since %s: US$%.2f, US$%.2f an hour, %d steps; models %s" % (
        hhmm, dollars, dollars / hours, len(steps), ", ".join(models) or "none")


# ---- self-test ----------------------------------------------------------------------------------------------------

def selftest():
    import tempfile
    cases = []
    d = datetime.datetime(2026, 11, 18, 12, 15)
    stopped = "**Started:** 2026-11-18 10:00 (x)\n**Stopped:** 2026-11-18 11:40 (y)\n"
    running = "**Started:** 2026-11-18 11:00 (x)\n**Stopped:** 2026-11-18 09:30 (y)\n"
    fresh = "**Started:** 2026-11-18 12:00 (x)\n**Stopped:** 2026-11-18 09:30 (y)\n"
    none = "**Started:** (none yet)\n**Stopped:** (none yet)\n"
    cases += [
        ("no lane session yet: GO", decide(d, none, None), "LANE GO no lane session"),
        ("no Started time but a turn 3 min ago: WAIT", decide(d, none, 3), "LANE WAIT"),
        ("stopped and quiet: GO", decide(d, stopped, 40), "LANE GO the last lane session stopped"),
        ("stopped, a turn 10 s ago: WAIT", decide(d, stopped, 0.17), "LANE WAIT"),
        ("stopped, a turn 30 s ago: GO", decide(d, stopped, 0.5), "LANE GO"),
        ("not stopped, a turn 5 min ago: WAIT", decide(d, running, 5), "LANE WAIT a lane session wrote"),
        ("not stopped, quiet 20 min: WAIT", decide(d, running, 20), "LANE WAIT the lane session started"),
        ("not stopped, quiet 30 min, started 75 min ago: GO taken as stopped", decide(d, running, 30), "LANE GO the lane session started"),
        ("not stopped, Started 15 min ago, no turns found at all: WAIT (Started is recent)", decide(d, fresh, None), "LANE WAIT the lane session started"),
        ("not stopped, Started 15 min ago, quiet 40 min by the logs: WAIT (Started is recent)", decide(d, fresh, 40), "LANE WAIT the lane session started"),
        ("not stopped, Started 75 min ago, no turns found: GO taken as stopped", decide(d, running, None), "LANE GO the lane session started"),
        ("not stopped, quiet 3 h, its background command pending: WAIT", decide(d, running, 180, job_running=True), "LANE WAIT the lane session started"),
        ("stopped, a command pending: GO naming it", str("background command" in decide(d, stopped, 40, job_running=True)), "True"),
        ("23 Nov 06:59: still decides", decide(datetime.datetime(2026, 11, 23, 6, 59), stopped, 40), "LANE GO"),
        ("23 Nov 07:00: STOPPED", decide(datetime.datetime(2026, 11, 23, 7, 0), stopped, 40), "LANE STOPPED: after 2026-11-23 07:00"),
        ("24 Nov: STOPPED even with nothing running", decide(datetime.datetime(2026, 11, 24, 12, 0), none, None), "LANE STOPPED"),
        ("the wrong folder or branch: WAIT", decide(d, stopped, 40, place_ok=False, place_why="this copy is x"), "LANE WAIT not the lane's worktree"),
        ("the wrong folder past the end: still STOPPED", decide(END, stopped, 40, place_ok=False), "LANE STOPPED"),
        ("02:15, walk not reported: WAIT", decide(datetime.datetime(2026, 11, 19, 2, 15), stopped, 400), "LANE WAIT the night's walk"),
        ("02:45, walk reported: GO", decide(datetime.datetime(2026, 11, 19, 2, 45), stopped, 400, walk_reported=True), "LANE GO"),
        ("03:30, no report: GO", decide(datetime.datetime(2026, 11, 19, 3, 30), stopped, 400), "LANE GO"),
        ("01:39: GO", decide(datetime.datetime(2026, 11, 19, 1, 39), stopped, 400), "LANE GO"),
        ("no line at all in the handover: GO as a first run", decide(d, "nothing", None), "LANE GO no lane session"),
    ]
    # THE LOGS: fixture folders standing for the lane's project folder and, beside it, the main one.
    base = tempfile.mkdtemp(prefix="lane_gate_")
    lane, main = os.path.join(base, "C--Users-Jafar-ledger-lane"), os.path.join(base, "C--Users-Jafar-ledger-local")
    now_ts = datetime.datetime(2026, 11, 18, 11, 15, tzinfo=datetime.timezone.utc).timestamp()   # 12:15 Swiss

    def log(folder, name, rows, entry="claude-desktop", sub=False):
        p = os.path.join(folder, name, "subagents", "agent-x.jsonl") if sub else os.path.join(folder, name + ".jsonl")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            for kind, ts, extra in rows:
                row = {"type": kind, "timestamp": ts + ".000Z", "entrypoint": entry, "message": {"content": "x"}}
                row.update(extra)
                fh.write(json.dumps(row, separators=(",", ":")) + "\n")
        os.utime(p, (now_ts - 60, now_ts - 60))
        os.makedirs(main, exist_ok=True)
        return p

    def gate_rows(ts, line, extra=0):
        rows = [("user", ts, {}), ("user", ts, {"message": {"content": [
            {"type": "tool_result", "content": [{"type": "text", "text": line}]}]}})]
        return rows + [("assistant", ts, {})] * extra

    # the main session working a minute ago never counts: the lane reads only its own folder
    log(main, "main-busy", [("user", "2026-11-18T11:13:00", {}), ("assistant", "2026-11-18T11:14:00", {})])
    log(lane, "lane-old", [("user", "2026-11-18T09:00:00", {}), ("assistant", "2026-11-18T09:40:00", {})])
    m1, j1 = lane_activity(now_ts, lane, own="own")
    log(lane, "own", [("user", "2026-11-18T11:14:30", {})])
    m2, _ = lane_activity(now_ts, lane, own="own")
    log(lane, "wait-run", gate_rows("2026-11-18T11:00:00", "LANE WAIT a lane session wrote a turn 3.0 minutes ago", 2))
    log(lane, "stopped-run", gate_rows("2026-11-18T11:05:00", "LANE STOPPED: after 2026-11-23 07:00", 2))
    m3, _ = lane_activity(now_ts, lane, own="own")
    log(lane, "eyes", [("user", "2026-11-18T11:10:00", {}), ("assistant", "2026-11-18T11:10:30", {})], entry="sdk-cli")
    m4, _ = lane_activity(now_ts, lane, own="own")
    log(lane, "lane-old", [("user", "2026-11-18T09:00:00", {}), ("assistant", "2026-11-18T09:40:00", {})])
    log(lane, "lane-old", [("assistant", "2026-11-18T11:12:00", {})], sub=True)
    m5, _ = lane_activity(now_ts, lane, own="own")
    log(lane, "worked-after-wait", gate_rows("2026-11-18T11:08:00", "LANE WAIT a lane session wrote", 30))
    m6, _ = lane_activity(now_ts, lane, own="own")
    lane2 = os.path.join(base, "lane-jobs")
    log(lane2, "quiet-with-job", [("user", "2026-11-18T10:30:00", {"toolUseResult": {"backgroundTaskId": "bjob1"}}),
                                  ("assistant", "2026-11-18T10:31:00", {})])
    m7, j7 = lane_activity(now_ts, lane2, own="own")
    log(lane2, "quiet-with-job", [("user", "2026-11-18T10:30:00", {"toolUseResult": {"backgroundTaskId": "bjob1"}}),
                                  ("user", "2026-11-18T10:50:00", {"message": {"content": "<task-notification><task-id>bjob1</task-id>"}}),
                                  ("assistant", "2026-11-18T10:51:00", {})])
    m8, j8 = lane_activity(now_ts, lane2, own="own")
    m9, j9 = lane_activity(now_ts, os.path.join(base, "no-such-folder"), own="own")
    cases += [
        ("the main session's turn a minute ago is not read: idle 95 min", "%s" % (m1 is not None and 94 < m1 < 96), "True"),
        ("this run's own log left out", "%s" % (m2 is not None and m2 > 94), "True"),
        ("runs that ended at LANE WAIT or LANE STOPPED are not activity", "%s" % (m3 is not None and m3 > 94), "True"),
        ("a script's claude -p log is not activity", "%s" % (m4 is not None and m4 > 94), "True"),
        ("a lane helper's turn counts", "%s" % (m5 is not None and m5 < 4), "True"),
        ("a run that said WAIT and then worked counts", "%s" % (m6 is not None and m6 < 8), "True"),
        ("a lane command started and not finished is pending", "%s/%s" % (j7, m7 is not None and 43 < m7 < 45), "True/True"),
        ("the same command once finished is not", "%s/%s" % (j8, m8 is not None and 23 < m8 < 25), "False/True"),
        ("no lane folder yet: no turn, no job", "%s/%s" % (m9, j9), "None/False"),
        ("no lane folder, no handover times: GO", decide(d, none, m9, j9), "LANE GO"),
        ("lane quiet 44 min with its command pending, not stopped: WAIT", decide(d, running, m7, j7), "LANE WAIT"),
        ("the lane's project folder is named from its worktree", os.path.basename(LANE_LOGS) if same_dir(LANE_DIR, "C:/Users/Jafar/ledger-lane") else "C--Users-Jafar-ledger-lane", "C--Users-Jafar-ledger-lane"),
    ]
    # --history: history_check's own threshold and window, the lane's run minute from its Started line.
    h22 = "**Started:** 2026-11-18 10:52 (x)\n"
    cases += [
        ("history: below the point is UNDER", history_line(d, h22, ctx=100000), "laneHistory context=100k"),
        ("history: below the point says UNDER", str("verdict=UNDER" in history_line(d, h22, ctx=100000)), "True"),
        ("history: past the point, 15 min before the lane's own run minute (:52, at :37): OVER",
         str("verdict=OVER" in history_line(datetime.datetime(2026, 11, 18, 12, 37), h22, ctx=300000)), "True"),
        ("history: past the point at :01, 51 min before the lane run: UNDER",
         str("verdict=UNDER" in history_line(datetime.datetime(2026, 11, 18, 12, 1), h22, ctx=300000)), "True"),
        ("history: 01:30, small history: OVER for the walk", history_line(datetime.datetime(2026, 11, 19, 1, 30), h22, ctx=1000), "laneHistory verdict=OVER (the night walk"),
        ("history: 23 Nov 07:00: OVER", history_line(END, h22, ctx=1000), "laneHistory verdict=OVER (the lane's end"),
        ("history: no lane log: UNREAD", history_line(d, h22, logs=os.path.join(base, "none")), "laneHistory verdict=UNREAD"),
    ]
    # the real lane handover, when present, parses
    if os.path.isfile(LANE_HANDOVER):
        t = open(LANE_HANDOVER, encoding="utf-8").read()
        cases.append(("the real lane handover has Started and Stopped lines", str(all(re.search(r"^\*\*%s:\*\*" % k, t, re.M)
                                                                                        for k in ("Started", "Stopped"))), "True"))
    bad = [(n, got) for n, got, want in cases if not got.startswith(want)]
    for n, got in bad:
        print("  FAIL %s -> %s" % (n, got))
    print("lane_gate selftest:", "passed (%d cases)" % len(cases) if not bad else "FAILED %d of %d" % (len(bad), len(cases)))
    try:
        import shutil
        shutil.rmtree(base)
    except OSError:
        pass
    return 1 if bad else 0


def main(a):
    if "--selftest" in a:
        return selftest()
    now = datetime.datetime.now()
    own = os.environ.get("CLAUDE_CODE_SESSION_ID")
    text = open(LANE_HANDOVER, encoding="utf-8").read() if os.path.isfile(LANE_HANDOVER) else ""
    if "--history" in a:
        print(history_line(now, text, own=own))
        return 0
    if "--spend" in a:
        i = a.index("--spend")
        if i + 1 >= len(a):
            print("usage: lane_gate.py --spend HH:MM")
            return 2
        print(spend_line(a[i + 1], now=now))
        return 0
    if now >= END:
        print(decide(now, text, None))
        return 0
    ok, why = place_check()
    reported = os.path.isfile(os.path.join(NIGHTLY, now.strftime("%Y-%m-%d") + ".md"))
    idle, job = lane_activity(now.timestamp(), own=own)
    print(decide(now, text, idle, job, reported, ok, why))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
