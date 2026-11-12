#!/usr/bin/env python3
"""THE WEEK'S PACE AGAINST HIS LINE (his yes of 7 November, keep-monday-share-2026-11-06; RULINGS.md).

    python tools/pace_line.py 65            # the week's allowance now reads 65%: the line, the gap, what it allows
    python tools/pace_line.py --selftest

A straight line from 0% at Monday's 13:00 reset to 90% at the next Monday's 07:00, the last 10% kept for Monday morning.
The reading comes from the session's usage tool (Weekly all models), which a script cannot read. Up to 3 points ahead:
carry on. 3 to 6 ahead: at most two helpers. More than 6 ahead: finish the item in hand, start no new session until
back on the line. Behind it: full pace within his rules. Monday 07:00 to 13:00: full pace.
"""
import datetime
import json
import os
import sys

# THE LAST READING, FOR THE GATE (the advisor's message 114, 12 Nov): tools/fresh_gate.py reads it without tokens and
# stands an hourly run aside while the week is more than 6 points ahead. Local state, not a record (gitignored).
STATE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "production", "handover", "pace-state.json")

WEEK_HOURS = 6 * 24 + 18  # Monday 13:00 to the next Monday 07:00

# THE DOUBLE WEEK, A DRAFT (the advisor's message 118, 12 Nov; his picks in chat 16:24): for the week of 16 Nov he
# presses a spare weekly reset. Shape: 0 to 95% from Monday 13:00 to Wednesday 15:00; after the reset, 0 to 90% from
# the reset's time to the next Monday 07:00. OFF until his tap adopting the order of 16 Nov sets "active": true in
# production/week-shape.json for that week's Monday; "reset_at" (Swiss "YYYY-MM-DD HH:MM") is written when he presses
# the reset. Any other week, or the file missing, keeps the single line above.
SHAPE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "production", "week-shape.json")
FIRST_LEG_HOURS = 2 * 24 + 2  # Monday 13:00 to Wednesday 15:00
FIRST_LEG_TOP = 95.0


def week_monday(now):
    monday = (now - datetime.timedelta(days=now.weekday())).replace(hour=13, minute=0, second=0, microsecond=0)
    if now < monday:
        monday -= datetime.timedelta(days=7)
    return monday


def read_shape(path=SHAPE):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def double_for(now, shape):
    """The double week's settings when it is active for this week, else None."""
    if not shape or not shape.get("active") or shape.get("monday") != week_monday(now).strftime("%Y-%m-%d"):
        return None
    reset = shape.get("reset_at")
    try:
        reset = datetime.datetime.strptime(reset, "%Y-%m-%d %H:%M") if reset else None
    except ValueError:
        reset = None
    return {"reset": reset}


def line_at(now, shape=None):
    """The line's percent at a Swiss local time."""
    monday = week_monday(now)
    end = monday + datetime.timedelta(hours=WEEK_HOURS)
    double = double_for(now, read_shape() if shape is None else shape)
    if double:
        reset = double["reset"]
        if reset is None or now < reset:
            return min(FIRST_LEG_TOP, FIRST_LEG_TOP * (now - monday).total_seconds() / 3600 / FIRST_LEG_HOURS)
        span = max(1.0, (end - reset).total_seconds() / 3600)
        return min(90.0, 90.0 * (now - reset).total_seconds() / 3600 / span)
    return min(90.0, 90.0 * (now - monday).total_seconds() / 3600 / WEEK_HOURS)


def line_per_hour(now, shape=None):
    """How fast the line climbs at this moment, points an hour (the gate's catch-up time)."""
    return max(0.01, line_at(now + datetime.timedelta(hours=1), shape) - line_at(now, shape))


def verdict(now, percent, shape=None):
    line = line_at(now, shape)
    ahead = percent - line
    if line >= 90.0 and not double_for(now, read_shape() if shape is None else shape):
        what = "full pace: Monday morning, the last 10% shared with him"
    elif ahead > 6:
        what = "more than 6 ahead: finish the item in hand, start no new session until back on the line"
    elif ahead > 3:
        what = "3 to 6 ahead: at most two helpers"
    elif ahead > 0:
        what = "up to 3 ahead: carry on"
    else:
        what = "behind the line: full pace within his rules"
    return "pace: %.0f%% against the line's %.1f%%, %+.1f points; %s" % (percent, line, ahead, what)


def selftest():
    fri = datetime.datetime(2026, 11, 6, 21, 0)
    cases = [
        ("Friday 21:00 is about 58", abs(line_at(fri, {}) - 57.8) < 0.5, True),
        ("just after the reset, near 0", line_at(datetime.datetime(2026, 11, 9, 13, 30)) < 0.5, True),
        ("Monday 07:00, 90", abs(line_at(datetime.datetime(2026, 11, 9, 7, 0)) - 90) < 0.01, True),
        ("Monday 12:00 stays 90", abs(line_at(datetime.datetime(2026, 11, 9, 12, 0)) - 90) < 0.01, True),
        ("behind", "behind" in verdict(fri, 50), True),
        ("2 ahead", "carry on" in verdict(fri, 60), True),
        ("5 ahead", "two helpers" in verdict(fri, 63), True),
        ("8 ahead", "no new session" in verdict(fri, 66), True),
        ("Monday morning, whatever the reading", "full pace" in verdict(datetime.datetime(2026, 11, 9, 8, 0), 99), True),
    ]
    off = {"active": False, "monday": "2026-11-16"}
    on = {"active": True, "monday": "2026-11-16"}
    pressed = dict(on, reset_at="2026-11-18 15:00")
    tue = datetime.datetime(2026, 11, 17, 14, 0)
    cases += [
        ("double off keeps the single line", abs(line_at(tue, off) - line_at(tue, {})) < 1e-9, True),
        ("double on, Tuesday 14:00 about 46", abs(line_at(tue, on) - 95.0 * 25 / 50) < 0.01, True),
        ("double on, Wednesday 15:00 is 95", abs(line_at(datetime.datetime(2026, 11, 18, 15, 0), on) - 95) < 0.01, True),
        ("no reset yet, Thursday stays 95", abs(line_at(datetime.datetime(2026, 11, 19, 12, 0), on) - 95) < 0.01, True),
        ("reset at 15:00, 0 just after", line_at(datetime.datetime(2026, 11, 18, 15, 30), pressed) < 0.5, True),
        ("reset, Monday 07:00 is 90", abs(line_at(datetime.datetime(2026, 11, 23, 7, 0), pressed) - 90) < 0.01, True),
        ("another week ignores it", abs(line_at(fri, on) - line_at(fri, {})) < 1e-9, True),
        ("double climbs about 1.9 an hour", abs(line_per_hour(tue, on) - 1.9) < 0.01, True),
    ]
    bad = [n for n, got, want in cases if got != want]
    print("pace_line selftest:", "passed (%d cases)" % len(cases) if not bad else "FAILED " + ", ".join(bad))
    return 1 if bad else 0


def main(a):
    if "--selftest" in a:
        return selftest()
    now = datetime.datetime.now()
    print(verdict(now, float(a[0])))
    try:
        with open(STATE, "w", encoding="utf-8") as fh:
            json.dump({"at": now.strftime("%Y-%m-%d %H:%M"), "percent": float(a[0]),
                       "ahead": round(float(a[0]) - line_at(now), 2)}, fh)
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
