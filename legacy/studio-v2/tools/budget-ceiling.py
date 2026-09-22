#!/usr/bin/env python3
"""THE PATTERNS THAT READ production/budget.md, ONE OF EACH, AND NO NUMBER.

Standard library only (`re`), nothing executes at import beyond definitions,
and there is no ceiling written here for a reader to fall back to. Three
readers import this file and none of them writes a pattern of its own:

    tools/glance.py                 the budget bar on Jafar's phone page
    tools/runner/telegram-bot.py    the verdict on a reading he just typed
    tools/budget-ceiling-check.py   the guard on the document's own shape

WHY THIS FILE EXISTS, and it is two incidents rather than tidiness. On
2026-09-11 a header rewrite (`1aedef87`) asked for in the words "one line
nobody can misread" deleted the only line a TOOL could read, and for two days
the console printed `ceilingPct=nothing-measured` and nobody opened it. In the
same week `CEILING_PCT = 80` sat in the Telegram bot for three days after
Jafar ruled the ceiling to 85, so on his own reading of 78 total and 82 Fable
the bot said "2 point(s) OVER the 80 percent ceiling" where the truth was "3
point(s) under". The repair for the second made the bot import tools/glance.py
for the pattern, which left the channel on his PC depending on a 2,200-line
page generator for one regex. This file is that regex's home: the channel
depends on a few dozen lines, and one idea has one implementation rather than
three copies that agree until the day the document is reworded.

WHAT IS NOT HERE. No ceiling number, no default, no fallback. A reader that
cannot find the line gets a refusal naming the reason, because the number it
would fall back to is the one that reversed a verdict.

THE TWO READERS DIFFER ON PURPOSE AND THE DIFFERENCE IS RULED (2026-09-13,
game-design/decision-2026-09-13-ruling-the-ceiling-is-read-not-carried-batch.md
section 2b): `ceiling_from_text` ANSWERS when two matching lines agree and
refuses only when they disagree, because refusing Jafar a verdict over a
harmless duplicate is the wrong trade for a channel; the document guard fails
on ANY duplicate, because "exactly one" is the document's rule. Do not align
them. tools/budget-ceiling-check.py prints both verdicts side by side on the
same fixture so the asymmetry is a measured fact and not a comment.

WHERE THE CASES ARE, because this module ships no CLI and an untested pattern
is the silent-instrument failure instruments.md names:
  - `ceiling_from_text`, both outcomes: `tools/runner/telegram-bot.py
    --selftest`, the live document as the accepting case
    (accept/ceiling-is-read-from-the-live-document) and four synthetic
    rejecting ones. Run by ledger/verify.py at every commit.
  - `CEILING` and `PROSE_CEILING` over the live document plus three synthetic
    rejecting fixtures: `tools/budget-ceiling-check.py`, whose fixtures run on
    every plain invocation. Run by ledger/verify.py at every commit.
  - `ROW_CEILING`, accepting and rejecting: `tools/glance.py --selftest`,
    section 7.
"""
import re

# THE DOCUMENT OF RECORD, named once. Every reader quotes this rather than
# typing the path again, so a move is one edit and not a hunt.
BUDGET = "production/budget.md"

# THE STANDING LINE, AND ITS WORDING IS A CONTRACT production/budget.md
# states in its own words beside the line, under a DO NOT TIDY THIS AWAY
# paragraph. Renaming or loosening this turns every reading on Jafar's phone
# into a refusal and takes the bar off the page.
CEILING = re.compile(r"Ceiling for LEDGER:\s*(\d+)\s*%")

# THE CEILING JAFAR RULED IN THE SAME MESSAGE AS A READING, read off the
# SELECTED ROW'S OWN WORDS, and read by tools/glance.py alone. Until
# 2026-09-09 the page took the ceiling from the standing line over the whole
# file and drew his bar against 80 while the row it was reading said, in its
# own words, "THE CEILING FOR THIS SESSION IS 75 ON THE GOVERNING METER, set
# by him in the same message, not the standing 80". A bar drawn against a
# ceiling he retired is a false reading with a number on it.
#
# TIGHT ON PURPOSE, and glance's rejecting fixtures are what the tightness is
# for. The phrase has to carry the number AND the words "on the governing
# meter" after it, because the same column also says "4x over pace against
# the 80% ceiling", "3 POINTS TO THE CEILING", "47 points to the 80 ceiling"
# and "the 80 ceiling is CROSSED on the governing meter", and any pattern
# loose enough to read an integer near the word ceiling out of those would
# invent a ruling out of prose. Rows are one line each in the table, so this
# never spans two readings.
#
# NOT READ BY THE BOT, deliberately: a per-session ceiling "expired with the
# reading it came with" (the 2026-09-10 ruling, quoted in budget.md), and a
# number Jafar is typing now is ruled by no old row.
ROW_CEILING = re.compile(
    r"\bthe ceiling\b(?:\s+\w+){0,3}?\s+is\s+(\d{1,3})\s*%?\s+"
    r"on the governing meter\b", re.I)

# THE SENTENCE JAFAR READS, which is the other half of the same number.
# production/budget.md carries the ceiling twice on purpose, once in prose and
# once in the line tools read, and its own instruction is that both change in
# the same edit. On 2026-09-11 they did not: the header said 80 while the
# ruling sixty lines below said 85, the wrong one was nearer the top, and work
# was narrowed for a breach that had not happened. Read by
# tools/budget-ceiling-check.py as a CROSS-CHECK and never as a second source:
# it answers with no number of its own, it only refuses to let the two halves
# drift apart in silence.
PROSE_CEILING = re.compile(
    r"\bthe\s+(?:standing\s+)?ceiling\s+is\s+(\d{1,3})\s*%?"
    r"\s+on\s+the\s+higher\s+meter\b", re.I)


def line_hits(text, pattern):
    """[(lineNo, match)] for one pattern over one document, in file order.

    ONE IMPLEMENTATION OF "WHERE DID IT MATCH", used by `ceiling_from_text`
    for its refusal and by the guard for its census, so the line numbers on
    Jafar's phone and the line numbers in a red commit gate can never be two
    different readings of one file.

    THE `+ 1` IS CORRECT HERE and is not the denominator bug: no newline
    precedes line 1, so a count of the newlines before a match is one less
    than its line number. The count of lines EXAMINED is a different quantity
    and is taken with `splitlines` below, for the reason stated there.
    """
    return [(text.count("\n", 0, m.start()) + 1, m)
            for m in pattern.finditer(text)]


def ceiling_from_text(text, rel=BUDGET, pattern=CEILING):
    """(pct, from, why) out of a document's own words. The parsing, the
    counting and the two strings all live here, where the selftest can reach
    them without a network, a PC or a real budget document.

    THE COUNT IS THE DENOMINATOR AND IT IS PART OF THE READING. One matching
    line is the document doing its job; none is the state this repository was
    actually in from 1aedef87 until 2026-09-13, when a rewrite asked for in
    the words "one line nobody can misread" deleted the only line a tool
    could read; two that disagree is the 2026-09-11 fault one level down,
    where the file carried 80 near the top and 85 sixty lines below and the
    wrong one was nearer the top. The first is answered, the other two are
    REFUSED OUT LOUD. Nothing here falls back to a number, because the number
    it would fall back to is the one that reversed a verdict.

    TWO LINES THAT AGREE ARE ANSWERED, NOT REFUSED, AND THAT IS RULED
    (2026-09-13, section 2b point 2): this reader is what speaks to Jafar's
    phone, and denying him a verdict over a duplicate that agrees with itself
    is a refusal in the wrong direction. The duplicate stays VISIBLE, because
    `from` carries every hit (`49/120..the-standing-line`). "Exactly one" is
    the DOCUMENT's rule and belongs to tools/budget-ceiling-check.py, which
    fails on any duplicate and turns the commit gate red without taking a
    verdict away from him.

    WHERE THIS IS DELIBERATELY STRICTER THAN tools/glance.py's row reading:
    a row's own ruling is read by ROW_CEILING above and drawn as a bar beside
    the file a human can open; this number is spoken to Jafar's phone as the
    word OVER or the word under.
    """
    # THE DENOMINATOR IS `splitlines`, NOT `count("\n") + 1`. The second
    # counts one more line than the file has whenever it ends in a newline,
    # which every file here does, and CLAUDE.md rule 3b names that exact
    # move: a denominator one larger than the set examined turns a clean
    # result into a false claim with a number on it. Measured against the
    # live document while this was written: wc -l 587, splitlines 587,
    # count-plus-one 588. The line NUMBERS beside it are the other case and
    # do want the plus one, since no newline precedes line 1.
    examined = len(text.splitlines())
    hits = [(m, ln) for ln, m in line_hits(text, pattern)]
    if not hits:
        return None, "nothing-measured", (
            # ONE CLAUSE CHANGED WHEN THIS MOVED, 2026-09-13, and it is named
            # here because the rest is byte-for-byte the bot's: "Nothing in
            # this bot" became "No reader of that line", because the sentence
            # now reaches Jafar's phone AND his glance page AND a red commit
            # gate, and a refusal that calls the page a bot is a false clause
            # printed in the one place a reader checks a refusal. Every
            # substring the bot's cases assert is untouched.
            "%s carries no 'Ceiling for LEDGER: N%%' line, which is the one "
            "wording any tool can read it from, and %d line(s) were examined "
            "looking for it. No reader of that line carries a ceiling of its "
            "own, so there is no number to answer with." % (rel, examined))
    values = sorted({int(m.group(1)) for m, _ln in hits})
    where = "/".join(str(ln) for _m, ln in hits)
    if len(values) > 1:
        return None, "nothing-measured", (
            "%s states %d different ceilings at once (%s), on line(s) %s of "
            "%d examined, and the file's own rule is that a disagreement is a "
            "bug to fix on sight rather than one to reason around. Picking "
            "one of them is the guess this refuses to make."
            % (rel, len(values), ", ".join("%d percent" % v for v in values),
               where, examined))
    return values[0], "%s:%s..the-standing-line" % (rel, where), ""
