#!/usr/bin/env python3
"""THE TIME EACH TASK TAKES, RECORDED AS IT HAPPENS.

Jafar, 5 October 2026 (the plan's edit 5): "Budget per week: 70 percent production, 10 percent
independent review, 20 percent kept for me. I read the meter and stop you when the week's share
is spent; you record the time each task takes." The outside audit of 4 October could not say
what the street had cost: git holds changes and timestamps, not time per task. So every task is
started and stopped here, and phase 1 measures an accepted family's cost from this file before
the town's production is extrapolated (PLAN.md).

One line per event in production/time-log.jsonl:
  {"event": "start", "at": ISO, "task": "...", "phase": "0", "kind": "production"|"review"}
  {"event": "stop",  "at": ISO, "note": "..."}
A start while a task is open stops that task first, so a forgotten stop costs one task's
accuracy, never the week's.

  python tools/timelog.py start "0.3 the sweep" --phase 0 [--kind review]
  python tools/timelog.py stop [--note "done; evidence in ..."]
  python tools/timelog.py add "0.1 plan adopted" --start 2026-10-05T07:53 --end 2026-10-05T09:25 --phase 0
  python tools/timelog.py week [--date 2026-10-05]     # the week's minutes by kind, phase and task
  python tools/timelog.py --selftest
"""
import argparse
import datetime as dt
import io
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "production", "time-log.jsonl")
KINDS = ("production", "review")


def now():
    return dt.datetime.now().replace(microsecond=0)


def parse(s):
    return dt.datetime.fromisoformat(s)


def read(path):
    if not os.path.exists(path):
        return []
    out = []
    with io.open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except ValueError:
                    raise SystemExit("time-log: line %d is not JSON: %s" % (n, line[:80]))
    return out


def append(path, ev):
    with io.open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def tasks(events, until=None):
    """Pairs the events into finished tasks; an open task runs to `until` (or now) and is marked."""
    out, cur = [], None
    for ev in events:
        if ev["event"] == "start":
            if cur:
                out.append(dict(cur, end=ev["at"], note="(stopped by the next start)"))
            cur = {k: ev[k] for k in ("task", "phase", "kind")}
            cur["start"] = ev["at"]
        elif ev["event"] == "stop" and cur:
            out.append(dict(cur, end=ev["at"], note=ev.get("note", "")))
            cur = None
    if cur:
        out.append(dict(cur, end=(until or now()).isoformat(), note="(open)"))
    for t in out:
        t["minutes"] = round((parse(t["end"]) - parse(t["start"])).total_seconds() / 60.0, 1)
    return out


def week_of(day):
    monday = day - dt.timedelta(days=day.weekday())
    start = dt.datetime.combine(monday, dt.time(0))
    return start, start + dt.timedelta(days=7)


def week_report(events, day, until=None):
    ws, we = week_of(day)
    rows = [t for t in tasks(events, until) if ws <= parse(t["start"]) < we]
    by_kind = {k: 0.0 for k in KINDS}
    by_phase = {}
    for t in rows:
        by_kind[t["kind"]] = by_kind.get(t["kind"], 0.0) + t["minutes"]
        by_phase[t["phase"]] = by_phase.get(t["phase"], 0.0) + t["minutes"]
    total = sum(by_kind.values())
    lines = ["Week of %s: %.0f minutes recorded (%d tasks)." % (ws.date(), total, len(rows))]
    for k in KINDS:
        share = (100.0 * by_kind[k] / total) if total else 0.0
        lines.append("  %-10s %6.0f min  %3.0f%% of recorded time" % (k, by_kind[k], share))
    for p in sorted(by_phase):
        lines.append("  phase %-4s %6.0f min" % (p, by_phase[p]))
    for t in rows:
        lines.append("  %s  %5.0f min  [%s, phase %s] %s %s" % (t["start"][:16], t["minutes"], t["kind"], t["phase"], t["task"], t["note"]))
    lines.append("Minutes, not the allowance: Jafar reads the meter; these say where it went.")
    return "\n".join(lines), by_kind


def cmd_start(path, task, phase, kind, at=None):
    if kind not in KINDS:
        raise SystemExit("time-log: kind must be one of %s" % (KINDS,))
    append(path, {"event": "start", "at": (at or now()).isoformat(), "task": task, "phase": str(phase), "kind": kind})


def cmd_stop(path, note="", at=None):
    evs = read(path)
    open_ = None
    for ev in evs:
        open_ = ev if ev["event"] == "start" else None
    if not open_:
        raise SystemExit("time-log: no task is open")
    append(path, {"event": "stop", "at": (at or now()).isoformat(), "note": note})
    return open_["task"]


def selftest():
    ok = True

    def check(cond, what):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + what)
        ok = ok and cond

    d = tempfile.mkdtemp()
    p = os.path.join(d, "t.jsonl")
    t0 = dt.datetime(2026, 10, 5, 8, 0)
    cmd_start(p, "a", "0", "production", at=t0)
    cmd_stop(p, "done", at=t0 + dt.timedelta(minutes=30))
    cmd_start(p, "b", "0", "review", at=t0 + dt.timedelta(minutes=40))
    cmd_start(p, "c", "1", "production", at=t0 + dt.timedelta(minutes=50))   # stops b
    cmd_stop(p, at=t0 + dt.timedelta(minutes=80))
    ts = tasks(read(p))
    check([t["minutes"] for t in ts] == [30.0, 10.0, 30.0], "three tasks of 30, 10 and 30 minutes, the forgotten stop closed by the next start")
    rep, by_kind = week_report(read(p), dt.date(2026, 10, 7))
    check(by_kind["production"] == 60.0 and by_kind["review"] == 10.0, "the week adds production and review apart")
    rep2, by2 = week_report(read(p), dt.date(2026, 10, 12))
    check(sum(by2.values()) == 0.0, "the next week starts empty")
    cmd_start(p, "d", "1", "production", at=t0 + dt.timedelta(minutes=90))
    ts = tasks(read(p), until=t0 + dt.timedelta(minutes=100))
    check(ts[-1]["note"] == "(open)" and ts[-1]["minutes"] == 10.0, "an open task counts to now and says it is open")
    try:
        cmd_start(p, "e", "1", "lunch")
        check(False, "an unknown kind is refused")
    except SystemExit:
        check(True, "an unknown kind is refused")
    print("timelog selftest: " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=("start", "stop", "add", "week"))
    ap.add_argument("task", nargs="?")
    ap.add_argument("--phase", default="0")
    ap.add_argument("--kind", default="production")
    ap.add_argument("--note", default="")
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--date")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd == "start":
        if not a.task:
            ap.error("start needs the task's name")
        cmd_start(LOG, a.task, a.phase, a.kind)
        print("started: %s (phase %s, %s)" % (a.task, a.phase, a.kind))
    elif a.cmd == "stop":
        print("stopped: %s" % cmd_stop(LOG, a.note))
    elif a.cmd == "add":
        if not (a.task and a.start and a.end):
            ap.error("add needs the task, --start and --end")
        cmd_start(LOG, a.task, a.phase, a.kind, at=parse(a.start))
        cmd_stop(LOG, a.note, at=parse(a.end))
        print("added: %s" % a.task)
    elif a.cmd == "week":
        day = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
        print(week_report(read(LOG), day)[0])
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
