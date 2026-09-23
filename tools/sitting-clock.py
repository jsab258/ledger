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

    1. THE STANDING LIST. If the sitting's time limit has not passed, the
       turn does not end while NOW.md has unfinished items - NOR WHILE IT HAS
       NONE. Widened by Jafar on 23 September, after the list was finished at
       eight minutes past midnight and the sitting stopped with eight hours
       left: CLAUDE.md already said to refill the list from ROADMAP.md when it
       runs short, and a rule in a document could not make that happen. An
       empty list with time left is a list to refill, not a place to stop.
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

#: AN EMPTY BLOCK, in either wording. Jafar, 23 September: "For you:" shows
#: only what is new since the last message, or "nothing new"; the full list
#: lives in FOR-JAFAR.md and the sitting's final message.
EMPTY = (["nothing"], ["nothing", "new"])

#: THE BUILDER'S OWN CHECKOUT, marked by an untracked file only this checkout
#: carries (Jafar, 23 September: a research session in its own folder read
#: the same rules and was held to this list). A clone or a worktree elsewhere
#: has no marker and is not held; nor is a session started in another folder.
BUILDER_MARKER = os.path.join(".claude", "builder-checkout")


def in_builder_checkout(root, cwd):
    """(ok, reason). This hook acts only for a session in the builder's own
    checkout: the marker must be in the root it reads, and the session's
    folder, when the payload names it, must be that root."""
    if not os.path.isfile(os.path.join(root, BUILDER_MARKER)):
        return False, "not the builder's checkout (no .claude/builder-checkout here)"
    if cwd:
        a = os.path.normcase(os.path.realpath(cwd))
        b = os.path.normcase(os.path.realpath(root))
        if a != b:
            return False, "the session is in another folder (%s), not the builder's checkout" % cwd
    return True, "the builder's checkout"


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


#: THE FILE THAT IS THE CHANNEL, and the hook's third job. Ruled by Jafar on
#: 22 September: "Every 'For you:' item goes into that file in the same turn it
#: is written, before it goes into a message. Nothing is ever only in a
#: message." The rule existed for about four minutes before it needed a hook,
#: which is the same story as the other two jobs.
FOR_JAFAR_MD = "FOR-JAFAR.md"

#: HOW MUCH OF AN ITEM HAS TO BE IN THE FILE. Not the whole line: a message
#: wraps and a file wraps differently, and demanding a byte-for-byte match
#: would fail on a line break and teach nobody anything. WHAT IS COMPARED is
#: the normalised WORDS - lowercased, markdown and punctuation stripped,
#: whitespace collapsed - and the test is whether a run of this many
#: consecutive words from the item appears anywhere in the normalised file.
#: EIGHT, because a run of eight words that matches by accident is not a run
#: that matches by accident, and because an item shorter than eight words has
#: to match whole, which is the right answer for a short one.
FOR_JAFAR_RUN = 8


def _words(text):
    """Normalise to a list of comparable words.

    EVERYTHING THAT IS FORMATTING GOES: asterisks, backticks, underscores,
    brackets, dashes used as bullets, and every run of punctuation. What is
    left is what the sentence SAYS, which is the only thing worth comparing
    across a message and a file that wrap differently.
    """
    out = []
    word = []
    for ch in text.lower():
        if ch.isalnum():
            word.append(ch)
        else:
            if word:
                out.append("".join(word))
                word = []
    if word:
        out.append("".join(word))
    return out


def for_you_items(message):
    """The lines of the For you: block, as written.

    THE BLOCK IS THE OPENER LINE AND THE BULLETS UNDER IT, and it ends at the
    first blank line that is followed by something which is not a bullet -
    which is how the report below it starts. A one-line `For you: nothing` has
    no items at all, and that is the commonest correct case.
    """
    if not message:
        return []
    lines = message.replace(chr(13) + chr(10), chr(10)).split(chr(10))
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return []
    items = []
    head = lines[i].strip()
    rest = head[len(OPENER):].strip() if head.startswith(OPENER) else ""
    if rest and _words(rest) not in EMPTY:
        items.append(rest)
    i += 1
    for line in lines[i:]:
        t = line.strip()
        if t.startswith("- ") or t.startswith("* "):
            items.append(t[2:].strip())
        elif t and not items:
            continue
        elif t and items and (line.startswith("  ") or line.startswith("\t")):
            items[-1] = items[-1] + " " + t
        elif not t:
            continue
        else:
            break
    return [x for x in items if _words(x) and _words(x) not in EMPTY]


def in_for_jafar(message, file_text):
    """(ok, reason). Every item in the block is already in the file.

    FAILS OPEN ON A MISSING FILE, like everything else here: a repository
    without FOR-JAFAR.md is one where this rule has not landed yet, and a hook
    that refuses to let anybody work until a file exists is a hook that gets
    switched off.
    """
    if file_text is None:
        return True, "no %s to check against" % FOR_JAFAR_MD
    items = for_you_items(message)
    if not items:
        return True, "nothing in the block to check"
    haystack = _words(file_text)
    joined = " " + " ".join(haystack) + " "
    missing = []
    for item in items:
        w = _words(item)
        n = min(FOR_JAFAR_RUN, len(w))
        found = False
        for k in range(0, len(w) - n + 1):
            if " " + " ".join(w[k:k + n]) + " " in joined:
                found = True
                break
        if not found:
            missing.append(" ".join(w[:12]))
    if not missing:
        return True, "all %d item(s) are in %s" % (len(items), FOR_JAFAR_MD)
    return False, ("%d 'For you:' item(s) are not in %s: %s. Put them in the "
                   "file first - nothing is ever only in a message."
                   % (len(missing), FOR_JAFAR_MD, "; ".join(m + "..." for m in missing[:3])))


def decide(text, now, message=None, for_jafar=None):
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

    # AND THE BLOCK ONLY REPEATS THE FILE, asked second and before the clock
    # for the same reason the opener is asked first: a sitting whose hours are
    # up still has to leave the record complete, and "the time ran out" is not
    # a reason to let an item exist only in a transcript.
    ok, why = in_for_jafar(message, for_jafar)
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
        # AN EMPTY LIST IS NOT THE END OF A SITTING THAT HAS TIME LEFT, ruled
        # 23 September. The only way out before the limit is to refill the
        # list from the roadmap and work it.
        return BLOCK, ("the standing list is empty with %.2f h of the %.2f h sitting "
                       "still to run. Refill it from the next part of ROADMAP.md, as "
                       "CLAUDE.md says, and carry on." % (left, limit))
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
    # ---- THE THIRD JOB: the block only repeats the file --------------------
    FJ = ("# For Jafar\n\n## Things you should know\n\n"
          "- 2026-09-22 The arrest is reachable from a test and from nothing "
          "else, counted rather than assumed.\n"
          "- 2026-09-22 The six hour ceiling passed and I carried on because "
          "you kept directing work.\n")
    said = ("For you:\n- The arrest is reachable from a test and from nothing "
            "else, counted rather than assumed.\n\nThe street is rendered.")
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9), said, FJ)
    check("accept/an-item-that-is-in-the-file-passes", v == PERMIT, r)

    unsaid = ("For you:\n- The runner lost a whole evening to a driver "
              "nobody has ever mentioned before now.\n\nDone.")
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9), unsaid, FJ)
    check("reject/an-item-that-is-not-in-the-file-blocks", v == BLOCK, r)
    check("reject/and-it-says-which-one", "not in FOR-JAFAR.md" in r, r)

    # NOTHING IS ALWAYS FINE, and it is the commonest correct case.
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9),
                  "For you: nothing\n\nDone.", FJ)
    check("accept/for-you-nothing-needs-no-file-entry", v == PERMIT, r)

    # WRAPPING MUST NOT MATTER. The same sentence, broken differently and
    # wearing markdown, is the same sentence.
    wrapped = ("For you:\n- **The arrest** is reachable from a test\n"
               "  and from *nothing else*, counted rather than assumed.\n\nDone.")
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9), wrapped, FJ)
    check("accept/wrapping-and-markdown-do-not-matter", v == PERMIT, r)

    # AND A MISSING FILE FAILS OPEN rather than stopping all work.
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9), unsaid, None)
    check("accept/a-missing-file-fails-open", v == PERMIT, r)

    # THE OPENER IS STILL ASKED FIRST, even with a file that would fail.
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9),
                  "No opener here at all.", FJ)
    check("reject/the-opener-still-comes-first", v == BLOCK and "open" in r, r)

    # A SHORT ITEM MATCHES WHOLE, because a run of eight words of a five-word
    # item is five words, and it must not pass by being too short to compare.
    short_fj = "# For Jafar\n- The probe is red.\n"
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9),
                  "For you:\n- The probe is red.\n\nDone.", short_fj)
    check("accept/a-short-item-matches-whole", v == PERMIT, r)
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9),
                  "For you:\n- The probe is green.\n\nDone.", short_fj)
    check("reject/a-short-item-that-differs-is-caught", v == BLOCK, r)

    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=1), good)
    check("accept/open-list-inside-the-limit-blocks", v == BLOCK, r)
    check("accept/and-the-reason-says-what-to-do", "next item" in r, r)
    check("accept/and-counts-them", "2 item(s)" in r, r)

    # THE ONE WAY A SITTING LEGITIMATELY ENDS: its time is up.
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=6), good)
    check("accept/at-the-limit-the-stop-is-permitted", v == PERMIT, r)
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9), good)
    check("accept/past-the-limit-too", v == PERMIT, r)
    # AN EMPTY LIST WITH TIME LEFT BLOCKS, 23 September: the sitting that
    # stopped at eight past midnight with eight hours to run is the case.
    v, r = decide(head + "- [x] done\n- [x] also done\n",
                  t0 + datetime.timedelta(hours=1), good)
    check("reject/an-empty-list-with-time-left-blocks", v == BLOCK, r)
    check("reject/and-says-to-refill-it-from-the-roadmap", "ROADMAP.md" in r, r)
    check("reject/and-says-how-long-is-left", "still to run" in r, r)
    v, r = decide(head + "- [x] done\n", t0 + datetime.timedelta(hours=6, minutes=1), good)
    check("accept/an-empty-list-at-the-limit-permits", v == PERMIT, r)

    # ONE MINUTE INSIDE THE LIMIT STILL BLOCKS, which is the boundary the
    # whole thing turns on.
    v, _r = decide(head + two_open, t0 + datetime.timedelta(hours=5, minutes=59), good)
    check("accept/one-minute-short-of-the-limit-still-blocks", v == BLOCK)

    # ---- THE OPENER, WHICH IS THE SECOND JOB ------------------------------
    done = head + "- [x] done\n"
    # THE OPENER IS JUDGED ON ITS OWN, with the sitting's time up, so the list
    # plays no part: since 23 September an empty list with time left blocks
    # for the list's own reason, and these cases are about the first line.
    t_up = t0 + datetime.timedelta(hours=7)
    v, r = decide(done, t_up, "The street is rendered.")
    check("reject/a-message-with-no-opener-blocks", v == BLOCK, r)
    check("reject/and-the-reason-quotes-what-it-found", "For you:" in r, r)
    v, r = decide(done, t_up, good)
    check("accept/an-empty-For-you-is-a-complete-answer", v == PERMIT, r)
    v, r = decide(done, t_up,
                  "\n\n   For you: the runner is down\nand here is the rest")
    check("accept/blank-lines-and-indent-are-forgiven", v == PERMIT, r)
    v, r = decide(done, t_up,
                  "Here is what happened.\nFor you: nothing")
    check("reject/an-opener-on-the-SECOND-line-is-not-an-opener", v == BLOCK, r)
    v, r = decide(done, t_up, "**For you:** nothing")
    check("reject/and-neither-is-one-wearing-bold", v == BLOCK, r)
    v, r = decide(done, t_up, "for you: nothing")
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
    v, r = decide(done, t_up, None)
    check("reject/no-message-in-the-payload-does-not-block", v != BLOCK, "%s %s" % (v, r))
    v, r = decide(done, t_up, "   \n  ")
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

    # "NOTHING NEW" IS AN EMPTY BLOCK, as "nothing" is (Jafar, 23 September).
    v, r = decide(head + two_open, t0 + datetime.timedelta(hours=9),
                  "For you: nothing new" + chr(10) + chr(10) + "Done.", FJ)
    check("accept/for-you-nothing-new-needs-no-file-entry", v == PERMIT, r)

    # ONLY THE BUILDER'S CHECKOUT IS HELD TO THE LIST.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        ok, why = in_builder_checkout(tmp, None)
        check("accept/no-marker-is-not-the-builder", not ok, why)
        os.makedirs(os.path.join(tmp, ".claude"))
        open(os.path.join(tmp, BUILDER_MARKER), "w").close()
        ok, why = in_builder_checkout(tmp, tmp)
        check("reject/the-builder-in-its-own-root-is-held", ok, why)
        other = os.path.join(tmp, "elsewhere")
        os.makedirs(other)
        ok, why = in_builder_checkout(tmp, other)
        check("accept/a-session-in-another-folder-is-not-held", not ok, why)
        ok, why = in_builder_checkout(tmp, None)
        check("reject/no-cwd-in-the-payload-still-holds-the-marked-root", ok, why)

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

    # FOR-JAFAR.md, AND ITS ABSENCE IS NOT A REFUSAL. Read as None when it is
    # not there, which in_for_jafar treats as "this rule has not landed here
    # yet" and passes. A hook that stops all work until a file exists is a
    # hook somebody switches off.
    for_jafar = None
    try:
        with open(os.path.join(root, FOR_JAFAR_MD), "r", encoding="utf-8") as fh:
            for_jafar = fh.read()
    except OSError:
        for_jafar = None

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
                here, why = in_builder_checkout(root, payload.get("cwd"))
                if not here:
                    print("%s %s, so this list does not hold it" % (PERMIT, why))
                    return 0
        except ValueError:
            # A payload that will not parse is an instrument fault, not a
            # verdict about the turn.
            print("%s the Stop payload did not parse as JSON" % UNASSESSED)
            return 0

    verdict, reason = decide(text, datetime.datetime.now(datetime.timezone.utc),
                             message, for_jafar)
    print("%s %s" % (verdict, reason))
    return 2 if verdict == BLOCK else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
