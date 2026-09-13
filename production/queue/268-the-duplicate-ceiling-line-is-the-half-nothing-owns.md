# 268: the duplicate ceiling line is the half nothing owns

RENAMED 2026-09-13, and the old name is the finding. It was "nothing stops the
next header rewrite deleting the ceiling line again", which was true when it
was filed and false two hours later, because queue 266's work landed three
cases that read the live document inside the commit gate. A title asserting
something false while the body corrects it is the header-nearer-the-top fault
that produced this whole batch, so the title moved rather than the correction
being left in a footnote.

STATUS: READY
OPENED: 2026-09-13

## What happened, and it is a resident fault

Jafar asked on 2026-09-11 for the standing ceiling to be "one line nobody can
misread". The rewrite that answered him, `1aedef87`, replaced this:

    -Ceiling for LEDGER: 80% of the weekly limit. The other 20% is his.

with four prose paragraphs saying 85. The paragraphs are correct and he has
not complained about them. What went with the deleted line was the only string
in the file that `tools/glance.py:653` can read:

    CEILING = re.compile(r"Ceiling for LEDGER:\s*(\d+)\s*%")

So a rewrite asked for in the words "one line nobody can misread" produced a
line no TOOL can read. Measured on 2026-09-13, before the line was restored:

    ceilingPct=nothing-measured ceilingFrom=nothing-measured
    ceilingStandingPct=nothing-measured
    budget    NOTHING MEASURED | production/budget.md
    2 of 5 readings could not be taken (next, budget)

and after:

    ceilingPct=85 ceilingFrom=the-standing-line..2026-09-11
    ceilingStandingPct=85
    1 of 5 readings could not be taken (next)

THE INSTRUMENT DID EVERYTHING RIGHT. It printed `nothing-measured` rather than
a number, named which readings it could not take and how many of five, went
GREY, and drew no bar. That is the design working exactly as its own comment
says it should: "a console that reports green while blind is the fault this
page exists to end". Nobody read it for two days, which is a separate problem
and not this item's.

## What this item was filed on, and how much of it is already true

FILED ON A PREMISE THAT LASTED TWO HOURS, and the correction belongs at the
top rather than in a footnote. The premise was that the only thing standing
between here and a repeat of `1aedef87` is the paragraph beside the restored
line telling the next editor not to tidy it away, which is a comment, and
CLAUDE.md rule 1 is explicit that comments are not evidence and decay.

That is no longer the whole story. Queue 266's work put three cases into
`tools/runner/telegram-bot.py`'s suite that read the LIVE
`production/budget.md` rather than a fixture, and `ledger/verify.py` runs that
suite at every commit:

    accept/ceiling-is-read-from-the-live-document
    accept/ceiling-is-the-standing-85
    accept/the-prose-and-the-machine-line-agree

`read_ceiling()` with no repository argument opens the live file, and
`ceiling_from_text` returns `(None, "nothing-measured", why)` when no line
matches, so deleting the machine-readable line now turns the commit gate red
with a message naming the remedy. A repeat of `1aedef87` would be caught in
the same session rather than sitting unnoticed for two days on a GREY console
nobody opened.

## What is genuinely left, which is less than this item was filed for

1. DUPLICATES ARE NOT COVERED AND THAT IS DELIBERATE ONE LEVEL DOWN. The
   bot accepts two `Ceiling for LEDGER` lines that AGREE, naming both line
   numbers, and refuses only when they disagree, on the builder's reasoning
   that refusing Jafar a verdict over a harmless duplicate is the wrong trade
   for a channel. That reasoning is right for the bot and leaves "exactly
   one" owned by nobody. Two agreeing lines today are two lines that disagree
   after the next edit touches one of them.
2. THE GUARANTEE LIVES IN THE WRONG BUILDING. A rule about the shape of a
   document is currently enforced by the selftest of the Telegram bot, which
   is the channel that runs on Jafar's PC. It holds only while that suite
   exists and only while it keeps reading the live file rather than a fixture,
   and nothing says so where a future editor of either would see it.

## Done looks like, REWRITTEN by the 2026-09-13 ruling into one builder pass

The ruling kept this item open rather than closing it on the ground that a
guard living in another tool's tests is one nobody knows to distrust. Four
deliverables, one pass:

1. THE PATTERN'S HOME. One small standard-library-only module under `tools/`,
   name the builder's, carrying `BUDGET`, `CEILING`, `ROW_CEILING` and the
   standing-line reader: the bot's `ceiling_from_text`, MOVED, with its
   `(pct, from, why)` contract and its refusal on disagreement intact. Glance,
   the bot and the new guard all import it. `load_glance` in the bot becomes
   the import of that module by the same by-path mechanism, so the channel on
   Jafar's PC depends on a few dozen lines rather than on a page generator.
   `glance.read_budget` keeps its row preference and calls the shared reader
   for the standing half.
2. THE DOCUMENT GUARD, where the other document checks run and not in the
   bot's suite: EXACTLY ONE machine line, with zero and two both failing and
   each named, and the prose agreeing with it. Tested both ways per CLAUDE.md
   rule 5b with the live file as the accepting case and three synthetic
   fixtures as the rejecting ones (deleted, duplicated at the same number,
   disagreeing), each failure naming the remedy. The bot's
   `accept/the-prose-and-the-machine-line-agree` is RETIRED in the same
   change, so the cross-check has one implementation rather than two.
3. THE PIN MOVES. `STANDING_CEILING_PCT` leaves the module namespace and
   becomes the literal inside the selftest case that reads it, case name and
   message unchanged, so the bot's top comment saying no number lives in that
   file is true at module level.
4. ONE THING THE BUILDER MUST NOT ALIGN. The bot ANSWERS when two matching
   lines agree and refuses only on disagreement; the guard fails on ANY
   duplicate. The bot's leniency is right for a channel that would otherwise
   deny Jafar a verdict over a harmless duplicate, and the guard's strictness
   is right for the document. Ruled 2026-09-13. A case in the bot's suite
   keeps proving the lenient half, and making the two agree is the wrong fix.

## What this does not cover

Whether anybody reads the console. `glance.py` said `NOTHING MEASURED` on
every run for two days and the fault was found by a grep for a stale ceiling,
not by reading the page it was already printed on. That is a separate item and
should be filed as one rather than folded in here.
