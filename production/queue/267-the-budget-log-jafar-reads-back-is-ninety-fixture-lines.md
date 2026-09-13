# 267: the budget log Jafar reads back is ninety fixture lines and no readings

STATUS: POINTS 3 AND 4 LANDED 2026-09-13 under
decision-2026-09-13-ruling-the-triggers-and-the-ceilings-home-batch.md;
CLOSES on the PC run: `python3 tools/budget-log-mark.py --mark --log <PC
copy>`, counts printed before and after. `unmarked>0` on the PC means READ
THOSE ROWS before touching the 5-second bound, and a new bound needs the PC's
printed series.
POINTS 1 AND 2 LANDED 2026-09-13 at 0e522c1f under
game-design/decision-2026-09-13-ruling-the-ceiling-is-read-not-carried-batch.md;
POINTS 3 AND 4 OPEN, and they ride with 268's builder.
OPENED: 2026-09-13

## The fault, measured

`production/logs/telegram-budget.log` on his PC and in this container is the
file `log_budget` at `tools/runner/telegram-bot.py:553` describes as "written
where Jafar can read it back without the bot running". Measured on
2026-09-13:

    lines in the log                                  90
    distinct value pairs                               2
      budgetTotalPct=40 budgetFablePct=62             30
      budgetTotalPct=40 budgetFablePct=77             60
    readings Jafar actually typed                      0  of 90
    selftest runs that wrote it                       30
    lines written per selftest run                     3
    lines carrying ceilingPct=80                      90  of 90

Three writers, all of them selftest fixtures driving the real handler at line
1082 through `Captured()`:

    1994  b4.pending, b4.total = "fable", 40   then handle("62")
    2006  b4b ... 40                           then handle("77")
    2130  b8  ... 40                           then handle("77.")

Every group of three lands inside three seconds, thirty times, at 19:11,
19:14, 19:26 and on through 2026-09-12T12:07, which are verify runs.

## Why this is the silent-instrument failure and not a tidy-up

`.claude/rules/instruments.md` names the shape exactly: "an unrun formatter
printing a plausible string is the silent-instrument failure". These strings
are worse than plausible. `40` and `77` are ordinary budget percentages, and
sixty of the ninety lines close on `headroomPct=3`, which reads as a studio
sitting three points off its ceiling. Nothing in the line says fixture. A
reader opening this file to answer "what has my spend been doing" gets thirty
timestamps, a flat 40 on the total meter and a Fable meter that steps 62 to
77 and stops, and every part of that is false.

The daily wake prompt already carries the principle in another place:
SELFTESTS DO NOT COUNT and no selftest may move that number. The same rule is
owed to a log Jafar was told he could read.

CLAUDE.md rule 3b is the second half. A file that cannot say how many of its
rows are real cannot tell nothing from fine, and this one currently cannot.

## Done looks like

1. The selftest does not write the live log. Either `log_budget` takes its
   directory from the caller and the fixtures pass a scratch path, or the
   selftest points `REPO` at its own temporary home for the handler cases.
   Whichever it is, `production/logs/telegram-budget.log` gains no line from a
   verify run.
2. Proven on both outcomes, accepting case first per CLAUDE.md rule 5b: a run
   of the suite leaves the live log's line count unchanged, and a genuine
   reading through the same handler still appends exactly one line. A guard
   that stops all writing is not a fix.
3. The ninety existing lines are marked, not deleted. They are evidence of
   thirty verify runs and of this fault. A header line, or a `source=selftest`
   rewrite of those rows, so a reader can tell the two apart. The file is
   gitignored at `.gitignore:96`, so this is done on the PC and the method
   ships as a small tool, not as a commit of the log.
   THE ACCEPTING CASE IS THIS CONTAINER, ruled 2026-09-13, because the same
   thirty verify runs wrote the same ninety rows here: run the marking tool
   once against this copy and print its before and after counts. The PC copy
   is marked by the SAME tool when the runner returns, and that run is the
   second accepting case rather than the first. A MISSING `ceilingFrom=` IS NECESSARY AND NOT
   SUFFICIENT, which is the correction the builder made to this item's own
   text and to the resident's brief: a reading Jafar typed on the PC BEFORE
   0e522c1f lacks that key too, and marking one of his readings as a fixture
   would be this fault committed a second time in the other direction. The
   tool recognises a fixture GROUP by shape and span (40/62, 40/77, 40/77,
   within 5 seconds, the bound set from the printed series) and counts
   everything else as `unmarked` rather than guessing at it.
4. The log prints its own denominator when read back: how many rows are
   readings and how many are not.

## What this does not cover

The ceiling those ninety lines carry. All of them say `ceilingPct=80` against
Jafar's standing 85, which is queue 266 and is fixed there, not here. Rows
rewritten under point 3 keep the number they were written with; a fixture row
that quietly acquired the right ceiling would be a second falsification on top
of the first.
