#!/usr/bin/env python3
"""MAY THIS TURN END? Two questions, so a Stop hook can act on the answer.

    python3 tools/sitting-clock.py            # the verdict for this repo, now
    python3 tools/sitting-clock.py --hook     # the Stop payload on stdin
    python3 tools/sitting-clock.py --selftest # both decisions, both ways

WHY THIS EXISTS, and it is an exception Jafar made by name. CLAUDE.md says
"Do not build anything whose purpose is to measure, report on, or enforce this
session's own behaviour", and this does exactly that. His instruction, 2026-09-22:
the sitting kept ending when one item got hard, against the rule in CLAUDE.md,
"because a rule in a document cannot stop a turn from ending. Fix that
mechanically, once, and it is the only piece of automation this session gets."

IT HAS TWO JOBS AND HE ADDED THE SECOND THE SAME DAY, after the same kind of
failure: things he needed to know kept arriving in the middle of long reports
and he found them by accident. So every message now begins with a line reading
"For you:", and a rule that lives only in a document could not make that happen
either.

    1. THE STANDING LIST. If NOW.md has unfinished items and the sitting's
       time limit has not passed, the turn does not end.
    2. THE FIRST LINE. If the turn's last message does not begin "For you:",
       the turn does not end.

Nothing else: no wake queue, no records, no counters, nothing written anywhere.

WHAT IT READS. One line in NOW.md, written at the start of each sitting:

    SITTING: started 2026-09-22T14:05:00+02:00, limit 6h

the standing list's own unchecked boxes, `- [ ]`, and the last assistant
message out of the Stop hook's own payload. That is all.

FAIL OPEN, ALWAYS AND OUT LOUD. Every unexpected outcome here lets the turn
end, and says which one it was. A broken clock that BLOCKS is a session that
cannot be ended without a human; a broken clock that PERMITS costs one turn
boundary and the next one reads the same file again. Recoverable against
unrecoverable, which is the same trade the hook this is adapted from made.
"""
import datetime
import json
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

#: THE OPENER, EXACTLY. Not "for you", not "**For you:**", not a greeting with
#: it further down - the first non-blank line has to START with this, because
#: the whole point of the rule is that it cannot be missed by someone
#: skimming the top of a message.
OPENER = "For you:"

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


def first_line(message):
    """The first line with anything on it, stripped of leading space.

    BLANK LINES AND LEADING WHITESPACE ARE FORGIVEN and nothing else is. A
    message that opens with an empty line still opens with "For you:" as far
    as a reader is concerned; one that opens with a paragraph does not,
    however soon the line arrives afterwards.
    """
    for line in (message or "").splitlines():
        if line.strip():
            return line.strip()
    return ""


def opener_ok(message):
    """(ok, reason). Whether the message begins the way every message must."""
    if message is None:
        return None, "the Stop payload carried no last message"
    if not (message or "").strip():
        return None, "the last message was empty"
    head = first_line(message)
    if head.startswith(OPENER):
        return True, "it opens with %r" % OPENER
    return False, ("the last message opens %r and every message must open %r. "
                   "Write the message again with that line first - the word "
                   "'nothing' after it is a complete and correct answer."
                   % (head[:48], OPENER))


def decide(text, now, message=None):
    """(verdict, reason). The whole decision, pure, so the selftest drives the
    same code the hook runs.

    THE OPENER IS ASKED FIRST and it is asked whatever the clock says. A
    sitting whose time is up still has to hand over a message he can read;
    ending on a buried report is the failure this was added for, and "the
    hours ran out" is not a reason to commit it one last time.
    """
    ok, why = opener_ok(message)
    if ok is False:
        return BLOCK, why

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
    good = "For you: nothing\n\nThe street is rendered."

    # THE BLOCKING CASE FIRST, because it is the one this exists for.
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=1), good)
    check("accept/open-list-inside-the-limit-blocks", v == BLOCK, r)
    check("accept/and-the-reason-says-what-to-do", "next item" in r, r)
    check("accept/and-counts-them", "2 item(s)" in r, r)

    # THE TWO WAYS A SITTING LEGITIMATELY ENDS.
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=6), good)
    check("accept/at-the-limit-the-stop-is-permitted", v == PERMIT, r)
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9), good)
    check("accept/past-the-limit-too", v == PERMIT, r)
    v, r = decide(head + "- [x] done\n- [x] also done\n",
                  t0 + datetime.timedelta(hours=1), good)
    check("accept/an-empty-list-permits-early", v == PERMIT, r)
    check("accept/and-says-how-long-was-left", "still to run" in r, r)

    # ONE MINUTE INSIDE THE LIMIT STILL BLOCKS, which is the boundary the
    # whole thing turns on.
    v, _r = decide(head + two_open, t0 + datetime.timedelta(hours=5, minutes=59), good)
    check("accept/one-minute-short-of-the-limit-still-blocks", v == BLOCK)

    # ---- THE OPENER, WHICH IS THE SECOND JOB ------------------------------
    done = head + "- [x] done\n"
    v, r = decide(done, t0 + datetime.timedelta(hours=1), "The street is rendered.")
    check("reject/a-message-with-no-opener-blocks", v == BLOCK, r)
    check("reject/and-the-reason-quotes-what-it-found", "For you:" in r, r)
    v, r = decide(done, t0 + datetime.timedelta(hours=1), good)
    check("accept/an-empty-For-you-is-a-complete-answer", v == PERMIT, r)
    v, r = decide(done, t0 + datetime.timedelta(hours=1),
                  "\n\n   For you: the runner is down\nand here is the rest")
    check("accept/blank-lines-and-indent-are-forgiven", v == PERMIT, r)
    v, r = decide(done, t0 + datetime.timedelta(hours=1),
                  "Here is what happened.\nFor you: nothing")
    check("reject/an-opener-on-the-SECOND-line-is-not-an-opener", v == BLOCK, r)
    v, r = decide(done, t0 + datetime.timedelta(hours=1), "**For you:** nothing")
    check("reject/and-neither-is-one-wearing-bold", v == BLOCK, r)
    v, r = decide(done, t0 + datetime.timedelta(hours=1), "for you: nothing")
    check("reject/nor-one-in-lower-case", v == BLOCK, r)
    # AND IT IS ASKED EVEN WHEN THE TIME IS UP, which is the case a tired
    # reading of this would get wrong: ending on a buried report is exactly
    # the failure it was added for.
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9), "no opener here")
    check("accept/the-opener-is-asked-even-past-the-limit", v == BLOCK, r)

    # FAIL OPEN, EVERY WAY IT CAN GO WRONG.
    for name, text in (
            ("no-sitting-line", two_open),
            ("unparseable-time", "SITTING: started yesterday, limit 6h\n" + two_open),
            ("no-timezone", "SITTING: started 2026-09-22T10:00:00, limit 6h\n" + two_open),
            ("zero-limit", "SITTING: started 2026-09-22T10:00:00+02:00, limit 0h\n" + two_open),
            ("empty-file", ""),
    ):
        v, r = decide(text, t0 + datetime.timedelta(hours=1), good)
        check("reject/%s-permits-rather-than-traps" % name, v == UNASSESSED, "%s %s" % (v, r))
    # A MESSAGE THE PAYLOAD DID NOT CARRY is not a missing opener. The hook
    # has no business blocking on a field the tool did not send.
    v, r = decide(done, t0 + datetime.timedelta(hours=1), None)
    check("reject/no-message-in-the-payload-does-not-block", v != BLOCK, "%s %s" % (v, r))
    v, r = decide(done, t0 + datetime.timedelta(hours=1), "   \n  ")
    check("reject/an-empty-message-does-not-block", v != BLOCK, "%s %s" % (v, r))

    # A CLOCK RUNNING BACKWARDS IS NOT A LIMIT.
    v, r = decide(head + two_open, t0 - datetime.timedelta(hours=1), good)
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

    # THE PAYLOAD IS PARSED HERE, in the layer that has a selftest, rather
    # than in four lines of bash beside it - the same reasoning the hook this
    # is adapted from gave for the same choice. A hook that greps JSON is a
    # hook that is wrong about a message containing a quotation mark.
    message = None
    if "--hook" in argv[1:]:
        try:
            payload = json.loads(sys.stdin.read() or "{}")
            if isinstance(payload, dict):
                if payload.get("stop_hook_active"):
                    print("%s this boundary was already blocked once; blocking "
                          "it again is a loop" % PERMIT)
                    return 0
                got = payload.get("last_assistant_message")
                if isinstance(got, str):
                    message = got
        except ValueError:
            # A payload that will not parse is an instrument fault, not a
            # verdict about the turn.
            print("%s the Stop payload did not parse as JSON" % UNASSESSED)
            return 0

    verdict, reason = decide(text, datetime.datetime.now(datetime.timezone.utc), message)
    print("%s %s" % (verdict, reason))
    return 2 if verdict == BLOCK else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
