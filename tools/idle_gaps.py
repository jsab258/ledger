#!/usr/bin/env python3
"""EACH GAP WITH NO SESSION RUNNING, WITH ITS CAUSE, FROM THIS PC'S SESSION LOGS (advisor 11 Nov 19:45, item 1: the DAILY file's row 1 split by gap).

    python tools/idle_gaps.py --from "2026-11-11 14:30" --until "2026-11-12 19:00" [--min 5] [--list]
    python tools/idle_gaps.py --selftest

Measures only; changes nothing. Times are Swiss (logs are UTC, converted by token_audit.swiss).

HOW: every timed turn of a real session's log or any of its helpers' logs counts as five running minutes (row 1's old rule).
An hourly run whose gate said WAIT is not running: its turns only mark that the gate held. The night hold 01:15 to 04:30 is left
out. Each gap over --min minutes gets one cause, read from the logs on either side of it:
  inside a session    the same session has turns on both sides (waiting on a job, a tool or a long thinking step);
                      "a background job" when a task notification ends the gap
  handover wait       the session before it wrote its Stopped line; the gap runs to the next real start
                      (", gate held N" when hourly runs stood aside inside it)
  usage limit         the session before it ends on a usage or rate limit message
  ended, no Stopped   the session before it simply ended its turn (the gate then waits for 30 quiet minutes)
  pace hold           hourly runs inside it read the pace over the line's stop mark and stopped at once (those runs
                      count as idle, not running)
  gate holding        no session before it in the window, only runs that stood aside
  unknown             none of these
LIMITS: a session ended by a crash reads as "ended, no Stopped"; Stopped is found as text written by a tool call in the
log's last 2 MB, so a Stopped line written by hand outside a session is missed.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from token_audit import swiss  # noqa: E402
from fresh_gate import LOGS, ended_at_wait  # noqa: E402

STEP = datetime.timedelta(minutes=5)
HOLD = (datetime.time(1, 15), datetime.time(4, 30))
DAY = (7, 23)
PACE_WORDS = re.compile(r"ahead.*(stop mark|nothing new)", re.I)
LIMIT_WORDS = re.compile(r"usage limit|rate limit|limit reached|out of extra usage", re.I)
TAIL = 2 << 20


def turns_of(path):
    """Swiss times of a log's timed user and assistant lines, and the times task notifications arrived."""
    times, notes = [], []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"timestamp"' not in line or ('"user"' not in line and '"assistant"' not in line):
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") not in ("user", "assistant") or not d.get("timestamp"):
                continue
            t = swiss(d["timestamp"])
            times.append(t)
            if d.get("type") == "user" and "<task-notification>" in line:
                notes.append(t)
    return times, notes


def tail_text(path):
    with open(path, "rb") as fh:
        fh.seek(max(0, os.path.getsize(path) - TAIL))
        return fh.read().decode("utf-8", "replace")


def stopped_written(text):
    """The last Stopped line written by a tool call (Edit, Write or a shell edit) near the log's end, as its text; '' if none."""
    found = ""
    for line in text.splitlines():
        flat = line.replace("\\*", "*")
        if '"tool_use"' in line and "**Stopped:**" in flat:
            found = flat[flat.rindex("**Stopped:**"):][:400]
    return found


def pace_stop(stopped, times):
    """An hourly run that only read the pace and stopped at once: its Stopped line names the line's stop mark, under 15 minutes."""
    return bool(stopped and PACE_WORDS.search(stopped) and times and times[-1] - times[0] < datetime.timedelta(minutes=15))


def last_words(text):
    """The text of the log's last few lines, for a limit message."""
    return "\n".join(text.splitlines()[-6:])


def sessions(since, until, logs=LOGS):
    """One record per main log touched in the window: its turns (helpers' folded in), notifications, kind and ending."""
    out = []
    lo = since.timestamp() - 86400 * 2
    for p in glob.glob(os.path.join(logs, "*.jsonl")):
        if os.path.getmtime(p) < lo:
            continue
        times, notes = turns_of(p)
        sid = os.path.basename(p)[:-6]
        for h in glob.glob(os.path.join(logs, sid, "subagents", "*.jsonl")):
            ht, _ = turns_of(h)
            times += ht
        times = sorted(t for t in times if since - STEP <= t <= until + STEP)
        if not times:
            continue
        waited = ended_at_wait(p)
        text = "" if waited else tail_text(p)
        stopped = stopped_written(text)
        paced = pace_stop(stopped, times)
        out.append({"id": sid, "times": times, "notes": notes, "wait": waited or paced, "pace": paced,
                    "stopped": bool(stopped), "limit": bool(LIMIT_WORDS.search(last_words(text)))})
    return out


def in_hold(t):
    return HOLD[0] <= t.time() < HOLD[1]


def minutes_outside_hold(a, b):
    """Minutes from a to b, the night hold left out, split into (day, night)."""
    day = night = 0
    t = a
    while t < b:
        if not in_hold(t):
            if DAY[0] <= t.hour < DAY[1]:
                day += 1
            else:
                night += 1
        t += datetime.timedelta(minutes=1)
    return day, night


def gaps(recs, since, until, min_minutes=5):
    """Idle stretches over min_minutes, each with its cause."""
    run = sorted(((t, r) for r in recs if not r["wait"] for t in r["times"]), key=lambda x: x[0])
    waits = [r["times"] for r in recs if r["wait"] and not r.get("pace")]
    paces = [r["times"] for r in recs if r.get("pace")]
    out = []
    edge, edge_rec = since, None
    for t, r in run + [(until, None)]:
        if t > edge and t - edge > datetime.timedelta(minutes=min_minutes):
            a, b = edge, min(t, until)
            day, night = minutes_outside_hold(a, b)
            if day + night > min_minutes:
                held = sum(1 for ts in waits if any(a <= w < b and not in_hold(w) for w in ts))
                paced = sum(1 for ts in paces if any(a <= w < b for w in ts))
                why = cause(edge_rec, r, a, b, held)
                if paced and not why.startswith("inside"):
                    why = "pace hold (over 6 ahead), %d runs stopped at once" % paced
                out.append({"from": a, "to": b, "day": day, "night": night, "cause": why})
        if t + STEP > edge:
            edge, edge_rec = t + STEP, r
    return out


def cause(before, after, a, b, held):
    held_note = ", gate held %d" % held if held else ""
    if before is not None and after is not None and before["id"] == after["id"]:
        return "inside a session" + (", a background job" if any(a <= n <= b + STEP for n in after["notes"]) else "")
    if before is None:
        return "gate holding" if held else "unknown"
    if before["limit"]:
        return "usage limit" + held_note
    if before["stopped"]:
        return "handover wait" + held_note
    return "ended, no Stopped" + held_note


def report(found, since, until, listing):
    by = {}
    for g in found:
        key = g["cause"].split(",")[0]
        d, n, c = by.get(key, (0, 0, 0))
        by[key] = (d + g["day"], n + g["night"], c + 1)
    td = sum(g["day"] for g in found)
    tn = sum(g["night"] for g in found)
    print("Idle %s to %s (night hold 01:15-04:30 left out; day %02d-%02dh): day %d min, night %d min, %d gaps"
          % (since.strftime("%d %b %H:%M"), until.strftime("%d %b %H:%M"), DAY[0], DAY[1], td, tn, len(found)))
    print("| cause | gaps | day min | night min |\n|---|---|---|---|")
    for k, (d, n, c) in sorted(by.items(), key=lambda kv: -(kv[1][0] + kv[1][1])):
        print("| %s | %d | %d | %d |" % (k, c, d, n))
    if listing:
        print("\n| from | to | min | cause |\n|---|---|---|---|")
        for g in found:
            print("| %s | %s | %d | %s |" % (g["from"].strftime("%d %H:%M"), g["to"].strftime("%d %H:%M"), g["day"] + g["night"], g["cause"]))


def selftest():
    T = lambda h, m: datetime.datetime(2026, 11, 11, h, m)  # noqa: E731
    rec = lambda i, ts, **k: dict({"id": i, "times": ts, "notes": [], "wait": False, "stopped": False, "limit": False}, **k)  # noqa: E731
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("ok   " if cond else "FAIL ") + name)
        ok &= bool(cond)
    a = rec("a", [T(10, 0), T(10, 4)], stopped=True)
    w = rec("w", [T(10, 30), T(10, 31)], wait=True)
    b = rec("b", [T(11, 0), T(11, 2), T(11, 30)], notes=[T(11, 30)])
    found = gaps([a, w, b], T(10, 0), T(12, 0))
    check("handover gap with one held run", found[0]["cause"] == "handover wait, gate held 1" and found[0]["day"] == 51)
    check("gap inside b ended by a notification", found[1]["cause"] == "inside a session, a background job")
    check("trailing gap after b is ended, no Stopped", found[2]["cause"] == "ended, no Stopped" and found[2]["day"] == 25)
    c = rec("c", [T(0, 50)])
    d = rec("d", [T(5, 0)])
    night = gaps([c, d], T(0, 50), T(5, 5))
    check("night hold left out of a night gap", night[0]["night"] == 20 + 30)
    check("limit cause", cause(rec("x", [], limit=True), d, T(1, 0), T(2, 0), 0) == "usage limit")
    check("Stopped found in an Edit call", stopped_written('{"type":"tool_use","input":{"new_string":"**Stopped:** 2026"}}'))
    p1 = rec("p1", [T(13, 0), T(13, 4)], wait=True, pace=True)
    e = rec("e", [T(12, 0)], stopped=True)
    f = rec("f", [T(14, 0)])
    ph = gaps([e, p1, f], T(12, 0), T(14, 1))
    check("pace runs make one pace-hold gap", len(ph) == 1 and ph[0]["cause"].startswith("pace hold") and ph[0]["day"] == 115)
    check("pace stop read from a Stopped line", pace_stop("**Stopped:** 00:22 (pace +6.0 ahead, at the stop mark)", [T(0, 22), T(0, 27)]))
    print("selftest " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--from", dest="since")
    ap.add_argument("--until")
    ap.add_argument("--min", type=int, default=5)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.since:
        print(__doc__)
        return 2
    since = datetime.datetime.strptime(a.since, "%Y-%m-%d %H:%M")
    until = datetime.datetime.strptime(a.until, "%Y-%m-%d %H:%M") if a.until else datetime.datetime.now()
    report(gaps(sessions(since, until), since, until, a.min), since, until, a.list)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
