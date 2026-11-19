#!/usr/bin/env python3
"""THE WEEK'S PACE AGAINST HIS LINE (his yes of 7 November, keep-monday-share-2026-11-06; RULINGS.md).

    python tools/pace_line.py 65            # the week's allowance now reads 65%: the line, the gap, what it allows
    python tools/pace_line.py 65 --fable 33 # also Fable's own weekly reading: the row's share, a warning at 95%
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
# presses a spare weekly reset. Shape: 0 to 99% from Monday 13:00 to Wednesday 15:00 (99 since his ruling of 17 Nov
# 21:12, advisor 210: the reset is pressed at 98 to 99%, never 100); after the reset, 0 to 90% from
# the reset's time to the next Monday 07:00. OFF until his tap adopting the order of 16 Nov sets "active": true in
# production/week-shape.json for that week's Monday; "reset_at" (Swiss "YYYY-MM-DD HH:MM") is written when he presses
# the reset. Any other week, or the file missing, keeps the single line above.
SHAPE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "production", "week-shape.json")
FIRST_LEG_HOURS = 2 * 24 + 2  # Monday 13:00 to Wednesday 15:00
FIRST_LEG_TOP = 99.0


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
    out = {"reset": reset}
    if "post_reset_top" in shape:
        out["top"] = float(shape["post_reset_top"])
    if "ceiling_margin" in shape:
        out["margin"] = float(shape["ceiling_margin"])
    return out


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
        top = float(double.get("top", 90.0))
        return min(top, top * (now - reset).total_seconds() / 3600 / span)
    return min(90.0, 90.0 * (now - monday).total_seconds() / 3600 / WEEK_HOURS)


def line_per_hour(now, shape=None):
    """How fast the line climbs at this moment, points an hour (the gate's catch-up time)."""
    return max(0.01, line_at(now + datetime.timedelta(hours=1), shape) - line_at(now, shape))


# ONE CEILING FOR BOTH SESSIONS (advisor 237, 19 Nov 00:25, replacing 236's two-row projection): after the reset the
# line runs 0 to 99 (week-shape.json "post_reset_top") and the ceiling is the line plus "ceiling_margin" (25). Above
# the ceiling the lane stops first; still above at the next row, nothing new starts until back under. The gate reads
# the stored "ahead" against its 6-point limit, so while a ceiling applies "ahead" is stored as percent - ceiling + 6.
def ceiling_at(now, shape=None):
    shape = read_shape() if shape is None else shape
    double = double_for(now, shape)
    if not double or double["reset"] is None or now < double["reset"] or "margin" not in double:
        return None
    return line_at(now, shape) + double["margin"]


# UNTIL HIS FABLE RESET (advisor 246, his pick 13:31, 19 Nov): the ceiling counts only non-Fable use: the weekly
# reading less Fable's share (week-shape.json "fable_share_per_pct", 0.46 points per Fable percent, corrected from
# readings), and new work stops outright when the weekly reading itself reaches "hard_stop" (75). Active while
# "fable_reset_pending" is true; set it false with the press time once he has pressed the reset.
def non_fable(percent, fable, shape=None):
    shape = read_shape() if shape is None else shape
    if fable is None or not shape.get("fable_reset_pending"):
        return None
    return percent - float(shape.get("fable_share_per_pct", 0.46)) * fable


def verdict(now, percent, shape=None, fable=None):
    line = line_at(now, shape)
    ahead = percent - line
    ceiling = ceiling_at(now, shape)
    nf = non_fable(percent, fable, shape)
    if ceiling is not None and nf is not None:
        stop = float((read_shape() if shape is None else shape).get("hard_stop", 75))
        if percent >= stop:
            what = "HARD STOP: the weekly reading has reached %.0f%%, start nothing new" % stop
        elif nf > ceiling:
            what = "ABOVE THE CEILING (non-Fable): the lane stops first; still above at the next row, start nothing new"
        else:
            what = "under the ceiling (non-Fable): Fable at max on Kiln before the reset"
        return ("pace: %.0f%% against the line's %.1f%%; non-Fable %.1f%% against the ceiling %.1f%%; hard stop at %.0f%%; %s"
                % (percent, line, nf, ceiling, stop, what))
    if ceiling is not None:
        what = ("ABOVE THE CEILING: the lane stops first; still above at the next row, start nothing new"
                if percent > ceiling else "under the ceiling: Kiln first, work within his rules")
        return "pace: %.0f%% against the line's %.1f%%, %+.1f points; ceiling %.1f%%; %s" % (percent, line, ahead, ceiling, what)
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


# FABLE'S CAP (his pick 18 Nov, advisors 227-228, 236: Fable up to 40% of its week; the backstop of 21:35 found nothing
# enforced it). 19 Nov 11:07 (advisor 244, his words "Fable cap to 70%"): the cap rises to 70%. The reading is the usage tool's Weekly Fable line, stored beside the pace in STATE; tools/lane/item_tags.py's
# helper hook refuses a new helper on model fable when the stored reading is at or over the cap.
FABLE_CAP = 95.0  # 19 Nov, advisor 245: no cap; a warning at 95% of Fable's own meter, the reset item at about 98%


def fable_verdict(fable):
    if fable >= 98:
        return "Fable %.0f%% of its week: RESET ITEM NOW (his page: Press a Fable reset now), full speed after" % fable
    if fable >= FABLE_CAP:
        return "Fable %.0f%% of its week: WARN (%.0f%%), the reset item at about 98%%" % (fable, FABLE_CAP)
    return "Fable %.0f%% of its week (no cap; warning at %.0f%%)" % (fable, FABLE_CAP)


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
    c237 = dict(on, reset_at="2026-11-18 15:20", post_reset_top=99, ceiling_margin=25)
    tue = datetime.datetime(2026, 11, 17, 14, 0)
    cases += [
        ("double off keeps the single line", abs(line_at(tue, off) - line_at(tue, {})) < 1e-9, True),
        ("double on, Tuesday 14:00 about 49.5", abs(line_at(tue, on) - 99.0 * 25 / 50) < 0.01, True),
        ("double on, Wednesday 15:00 is 99", abs(line_at(datetime.datetime(2026, 11, 18, 15, 0), on) - 99) < 0.01, True),
        ("no reset yet, Thursday stays 99", abs(line_at(datetime.datetime(2026, 11, 19, 12, 0), on) - 99) < 0.01, True),
        ("reset at 15:00, 0 just after", line_at(datetime.datetime(2026, 11, 18, 15, 30), pressed) < 0.5, True),
        ("reset, Monday 07:00 is 90", abs(line_at(datetime.datetime(2026, 11, 23, 7, 0), pressed) - 90) < 0.01, True),
        ("another week ignores it", abs(line_at(fri, on) - line_at(fri, {})) < 1e-9, True),
        ("237: ceiling at Thursday 00:52 about 33.4", abs(ceiling_at(datetime.datetime(2026, 11, 19, 0, 52), c237) - 33.45) < 0.1, True),
        ("237: 31% is under", "under the ceiling" in verdict(datetime.datetime(2026, 11, 19, 0, 52), 31, c237), True),
        ("237: 40% is above", "ABOVE" in verdict(datetime.datetime(2026, 11, 19, 0, 52), 40, c237), True),
        ("237: Monday 07:00 line is 99", abs(line_at(datetime.datetime(2026, 11, 23, 7, 0), c237) - 99) < 0.01, True),
        ("no ceiling without its margin", ceiling_at(datetime.datetime(2026, 11, 19, 0, 52), pressed) is None, True),
        ("double climbs about 1.98 an hour", abs(line_per_hour(tue, on) - 1.98) < 0.01, True),
        ("245: 70% gives no warning", "WARN" in fable_verdict(70), False),
        ("245: 95% warns", "WARN" in fable_verdict(95), True),
        ("245: 98% asks for the reset", "RESET ITEM NOW" in fable_verdict(98), True),
    ]
    c246 = dict(c237, fable_reset_pending=True, fable_share_per_pct=0.46, hard_stop=75)
    thu = datetime.datetime(2026, 11, 19, 13, 40)
    cases += [
        ("246: 47% with Fable 51 is under (non-Fable 23.5)", "under the ceiling (non-Fable)" in verdict(thu, 47, c246, 51), True),
        ("246: 75% is a hard stop", "HARD STOP" in verdict(thu, 75, c246, 10), True),
        ("246: without a Fable reading the plain ceiling", "ABOVE THE CEILING:" in verdict(thu, 47, c246), True),
        ("246: after the press the plain ceiling", "ABOVE THE CEILING:" in verdict(thu, 47, dict(c246, fable_reset_pending=False), 51), True),
    ]
    bad = [n for n, got, want in cases if got != want]
    print("pace_line selftest:", "passed (%d cases)" % len(cases) if not bad else "FAILED " + ", ".join(bad))
    return 1 if bad else 0


def main(a):
    if "--selftest" in a:
        return selftest()
    now = datetime.datetime.now()
    fable = float(a[a.index("--fable") + 1]) if "--fable" in a else None
    print(verdict(now, float(a[0]), fable=fable))
    state = {"at": now.strftime("%Y-%m-%d %H:%M"), "percent": float(a[0]), "ahead": round(float(a[0]) - line_at(now), 2)}
    ceiling = ceiling_at(now)
    if ceiling is not None:
        state["ceiling"] = round(ceiling, 2)
        nf = non_fable(float(a[0]), fable)
        measured = float(a[0]) if nf is None else nf
        state["ahead"] = round(measured - ceiling + 6.0, 2)
        if nf is not None:
            state["non_fable"] = round(nf, 2)
            if float(a[0]) >= float(read_shape().get("hard_stop", 75)):
                state["ahead"] = 99.0
    if "--fable" in a:
        state["fable"] = float(a[a.index("--fable") + 1])
        state["fable_at"] = state["at"]
        print(fable_verdict(state["fable"]))
    else:
        try:   # keep the last Fable reading when only the pace is given
            with open(STATE, encoding="utf-8") as fh:
                old = json.load(fh)
            if "fable" in old:
                state["fable"], state["fable_at"] = old["fable"], old.get("fable_at", old.get("at"))
        except (OSError, ValueError):
            pass
    try:
        with open(STATE, "w", encoding="utf-8") as fh:
            json.dump(state, fh)
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
