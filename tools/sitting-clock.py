#!/usr/bin/env python3
"""IS THIS SITTING OVER? Read NOW.md and say, so a Stop hook can act on it.

    python3 tools/sitting-clock.py            # the verdict for this repo, now
    python3 tools/sitting-clock.py --selftest # the decision, both ways

WHY THIS EXISTS, and it is an exception Jafar made by name. CLAUDE.md says
"Do not build anything whose purpose is to measure, report on, or enforce this
session's own behaviour", and this does exactly that. His instruction, 2026-09-22:
the sitting kept ending when one item got hard, against the rule in CLAUDE.md,
"because a rule in a document cannot stop a turn from ending. Fix that
mechanically, once, and it is the only piece of automation this session gets."
Stripped to one job and nothing else: no wake queue, no records, no counters.

WHAT IT READS. One line in NOW.md, written at the start of each sitting:

    SITTING: started 2026-09-22T14:05:00+02:00, limit 6h

and the standing list's own unchecked boxes, `- [ ]`. That is all. The list is
already the work and the line is two facts; nothing new is kept anywhere.

FAIL OPEN, ALWAYS AND OUT LOUD. Every unexpected outcome here lets the turn
end, and says which one it was. A broken clock that BLOCKS is a session that
cannot be ended without a human; a broken clock that PERMITS costs one turn
boundary and the next one reads the same file again. Recoverable against
unrecoverable, which is the same trade the hook this is adapted from made.
"""
import datetime
import os
import re
import sys

NOW_MD = "NOW.md"

#: The line the sitting writes about itself. Deliberately one line and
#: deliberately in NOW.md rather than a file of its own: a second file is a
#: second thing to keep in step, and this one is already read every sitting.
SITTING_RE = re.compile(
    r"^SITTING:\s*started\s+(\S+)\s*,\s*limit\s+([0-9]+(?:\.[0-9]+)?)\s*h\s*$",
    re.MULTILINE)

#: An unfinished item. Matches the standing list's own checkbox and nothing
#: else - a heading, a note or a struck-through `- [x]` is not an item of work.
OPEN_RE = re.compile(r"^\s*-\s*\[ \]", re.MULTILINE)

PERMIT = "PERMIT"
BLOCK = "BLOCK"
UNASSESSED = "PERMIT-UNASSESSED"


def open_items(text):
    """How many unfinished items the standing list has."""
    return len(OPEN_RE.findall(text))


def sitting(text):
    """(started, limit_hours) or (None, None) if the line is not there or not
    readable. Not an error: a sitting nobody stamped is a sitting this cannot
    judge, and it says so rather than guessing at one."""
    m = SITTING_RE.search(text)
    if not m:
        return None, None
    try:
        started = datetime.datetime.fromisoformat(m.group(1))
    except ValueError:
        return None, None
    if started.tzinfo is None:
        return None, None
    try:
        limit = float(m.group(2))
    except ValueError:
        return None, None
    if limit <= 0:
        return None, None
    return started, limit


def decide(text, now):
    """(verdict, reason). The whole decision, pure, so the selftest drives the
    same code the hook runs.

    THE ORDER OF THE TESTS IS THE POINT. Time is asked FIRST, because a sitting
    past its limit ends whatever is left on the list - that is what a limit is.
    Only then does an unfinished list block, and only then because the rule it
    is enforcing says a sitting ends at the time limit or when the list is
    empty, never because one piece of work finished.
    """
    started, limit = sitting(text)
    if started is None:
        return UNASSESSED, "no readable SITTING line in %s" % NOW_MD
    elapsed = (now - started).total_seconds() / 3600.0
    left = limit - elapsed
    if elapsed < 0:
        return UNASSESSED, ("the SITTING line starts %.2f h in the future; a clock "
                            "nobody can read is not a limit" % (-elapsed))
    if left <= 0:
        return PERMIT, ("the time is up: %.2f h of a %.2f h sitting"
                        % (elapsed, limit))
    n = open_items(text)
    if n == 0:
        return PERMIT, "the standing list is empty, with %.2f h still to run" % left
    return BLOCK, ("%d item(s) still open on the standing list and %.2f h of the "
                   "%.2f h sitting left. Continue with the next item."
                   % (n, left, limit))


# ---------------------------------------------------------------------------


def selftest():
    passed = failed = 0

    def check(name, ok, detail=""):
        nonlocal passed, failed
        if ok:
            passed += 1
        else:
            failed += 1
            print("sitting-clock selftest FAIL %s: %s" % (name, detail))

    t0 = datetime.datetime.fromisoformat("2026-09-22T10:00:00+02:00")
    head = "SITTING: started 2026-09-22T10:00:00+02:00, limit 6h\n"
    two_open = "- [ ] one\n- [x] done\n- [ ] two\n"

    # THE BLOCKING CASE FIRST, because it is the one this exists for.
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=1))
    check("accept/open-list-inside-the-limit-blocks", v == BLOCK, r)
    check("accept/and-the-reason-says-what-to-do", "next item" in r, r)
    check("accept/and-counts-them", "2 item(s)" in r, r)

    # THE TWO WAYS A SITTING LEGITIMATELY ENDS.
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=6))
    check("accept/at-the-limit-the-stop-is-permitted", v == PERMIT, r)
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9))
    check("accept/past-the-limit-too", v == PERMIT, r)
    v, r = decide(head + "- [x] done\n- [x] also done\n", t0 + datetime.timedelta(hours=1))
    check("accept/an-empty-list-permits-early", v == PERMIT, r)
    check("accept/and-says-how-long-was-left", "still to run" in r, r)

    # ONE MINUTE INSIDE THE LIMIT STILL BLOCKS, which is the boundary the
    # whole thing turns on.
    v, _r = decide(head + two_open, t0 + datetime.timedelta(hours=5, minutes=59))
    check("accept/one-minute-short-of-the-limit-still-blocks", v == BLOCK)

    # FAIL OPEN, EVERY WAY IT CAN GO WRONG.
    for name, text in (
            ("no-sitting-line", two_open),
            ("unparseable-time", "SITTING: started yesterday, limit 6h\n" + two_open),
            ("no-timezone", "SITTING: started 2026-09-22T10:00:00, limit 6h\n" + two_open),
            ("zero-limit", "SITTING: started 2026-09-22T10:00:00+02:00, limit 0h\n" + two_open),
            ("empty-file", ""),
    ):
        v, r = decide(text, t0 + datetime.timedelta(hours=1))
        check("reject/%s-permits-rather-than-traps" % name, v == UNASSESSED, "%s %s" % (v, r))

    # A CLOCK RUNNING BACKWARDS IS NOT A LIMIT.
    v, r = decide(head + two_open, t0 - datetime.timedelta(hours=1))
    check("reject/a-sitting-starting-in-the-future-permits", v == UNASSESSED, r)

    # THE COUNTER COUNTS ITEMS AND NOT PROSE.
    check("accept/a-struck-item-is-not-open", open_items("- [x] a\n- [X] b\n") == 0)
    check("accept/indented-items-count", open_items("  - [ ] a\n") == 1)
    check("accept/a-heading-is-not-an-item", open_items("## - [ ] not a box\n") == 0)
    check("accept/prose-about-boxes-is-not-an-item",
          open_items("the list uses - [ ] for an open item\n") == 0)

    print("sitting-clock selftest: passed=%d/%d failed=%d"
          % (passed, passed + failed, failed))
    return 0 if failed == 0 else 4


def main(argv):
    if "--selftest" in argv[1:]:
        return selftest()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, NOW_MD)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print("%s %s is unreadable (%s)" % (UNASSESSED, NOW_MD, type(exc).__name__))
        return 0
    verdict, reason = decide(text, datetime.datetime.now(datetime.timezone.utc))
    print("%s %s" % (verdict, reason))
    return 2 if verdict == BLOCK else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
