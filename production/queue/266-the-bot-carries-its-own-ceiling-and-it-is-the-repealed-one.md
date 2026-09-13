# 266: the bot carries its own ceiling and it is the repealed one

STATUS: LANDED 2026-09-13 under
game-design/decision-2026-09-13-ruling-the-ceiling-is-read-not-carried-batch.md;
CLOSES on the first row in production/logs/telegram-budget.log on the PC
carrying ceilingFrom=production/budget.md, which needs the bot restarted on
this commit or later (ledger-restart-telegram-bot.yml, waiting on ledger-pc).
OPENED: 2026-09-13

## The fault, measured

`tools/runner/telegram-bot.py:130` reads `CEILING_PCT = 80`. Jafar ruled the
ceiling to 85 on 2026-09-10, recorded at `production/budget.md:44` and again
at `:90`. The comment above the constant, at lines 125 to 129, says what
should have happened and did not:

    THE CEILING IS NOT INVENTED HERE. 80 percent is the number
    production/NOW.md carries as the spend ceiling ... If Jafar moves the
    ceiling, this constant moves with the document and not before it.

The document moved. The constant did not. Run against his own last reading,
78 total and 82 Fable, reported 2026-09-11:

    what the bot says now:
      The higher meter governs, so that is fable at 82 percent,
      2 point(s) OVER the 80 percent ceiling.
    what the standing 85 makes it:
      The higher meter governs, so that is fable at 82 percent,
      3 point(s) under the 85 percent ceiling.

Over by two against under by three. The bot does not merely print a stale
number, it reverses the verdict, and the verdict is the one that decides
whether the studio stops.

## Why this ranks now and not at leisure

The bot started on his PC at 2026-09-13T01:14:15Z. Messages 78 and 79, the
two receipts that arrived this morning, are `OPENING` at 236 characters and
`BUDGET_Q` at 224, sent one second apart by `run()` at lines 1462 and 1464.
`ask_budget` sets `pending = "total"`. So the bot is sitting on his phone
right now with the budget question open, and the next thing he types goes
through `budget_reading` with the repealed ceiling.

This is the same wrong read Jafar corrected in the resident on 2026-09-11,
where checking a stale header instead of the ruling sixty lines below it cost
a spawn and a builder. It is now in the code, aimed at him rather than at us.

## What a fix must not do

Change 80 to 85 and stop. Four selftest cases hardcode the standing number
into their expected strings, so the constant cannot move without them, and
that coupling is the actual defect:

    1820  budget_reading(40, 62)    expects headroomPct=18
    1824  budget_reading(77, 76)    expects headroomPct=3
    1827  budget_reading(80, 12)    expects "exactly on the 80 percent"
    1830  budget_reading(91.5, 12)  expects "11.5 point(s) OVER"

What those four cases are for is the ARITHMETIC: which meter governs, that
headroom goes negative rather than clamping, that a fraction prints as 91.5
and not 91. None of that is a question about policy. They should each pass
`ceiling=` explicitly and test the maths at a fixed number of their own, so
the standing ceiling can move again without touching a test.

## Done looks like

1. The bot's ceiling is READ FROM `production/budget.md`, not copied into
   Python. A ruling recorded in the document of record reaches the channel
   without an edit here, which is what the comment at 125 already promises.
2. The reader is tested on both outcomes, accepting case first per CLAUDE.md
   rule 5b: the live `production/budget.md` is the accepting fixture and must
   yield 85; a synthetic document naming no ceiling is the rejecting one, and
   the failure is LOUD, never a silent fallback to a number in the code. A bot
   that cannot read the ceiling must say so and refuse the reading rather than
   answer with a guess.
3. The four arithmetic cases pass `ceiling=` explicitly and no longer move
   when the standing number moves.
4. One case asserts the standing number itself, reading the document, so a
   future repeal that does not reach the bot fails the suite here rather than
   on his phone.

## What this does not cover

The running process. `budget_reading`'s default is bound when the function is
defined, so the bot now live on his PC keeps 80 until it is restarted. The
fix lands for the next start, and nothing in this repo can reach the one
running. If he answers the open budget question before then, his reading is
computed against 80 and must be re-read by hand against 85.
