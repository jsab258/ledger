# The Sunday page

STATUS: LIVE. Verified 2026-09-15, the day it was ruled.

ONE FILE THAT ACCUMULATES, newest entry at the top, never rewritten. Ruled by
Jafar 2026-09-15: "The Sunday page has never been written. It is the record of
decisions waiting on me, rulings made and not applied, numbers the plan still
lacks, what moved on the ladder, the game-versus-studio split, and what the
research lane changed. Write it this Sunday and every Sunday, kept as a file
that accumulates."

## What it is for, so that it does not drift into a status dump

The brief is the daily message and is capped at 150 words, so it carries what
he must act on TODAY. This page is the weekly one and carries what accumulates:
the things that are true for weeks and that a daily message cannot hold without
crowding out the day. IT IS NOT A SUMMARY OF THE BRIEFS. A week of briefs he
has already read is the one thing this page must never repeat.

## The six sections, in his order, and what each must not become

1. **DECISIONS WAITING ON ME.** Read from `production/decision-queue.md`. Each
   with how long it has waited and what is blocked behind it. A decision with
   nothing blocked behind it says so, because that is the argument for closing
   it rather than carrying it another week.
2. **RULINGS MADE AND NOT APPLIED.** Read from
   `ledger-v2/respec/decision-register/rulings-log.md` against the tree. This is
   the section most likely to be quietly empty when it should not be: a ruling
   is applied when something in the code or the record changed, not when a
   record was written about it. Name the ruling, its date, and what has not
   moved.
3. **NUMBERS THE PLAN STILL LACKS.** The gates and rows that read
   nothing-measured, and the thresholds no series has been printed for. A row
   that has never measured is not the same as one measuring zero, and this
   section keeps them apart.
4. **WHAT MOVED ON THE LADDER.** Read from `production/quality-ladder.md`. Which
   rungs moved, which did not, and which gained a blank next rung, since a blank
   next rung is a research task and not a finished aspect.
5. **THE GAME VERSUS STUDIO SPLIT.** His standing rule is two thirds of the
   week's spend to game work. `ledger/verify.py`'s footer prints gameShareDay
   and fableShareAll as COUNTS OF SPAWNS, which is not spend, and the difference
   is stated every week rather than assumed away. The budget table is the only
   record of actual points, and its windows are rarely clean.
6. **WHAT THE RESEARCH LANE CHANGED.** What research landed, and what it
   changed in a plan, a queue item or a ruling. Research that changed nothing
   says so; that is a finding about the lane, not an empty section.

## The rule about emptiness

An empty section is written as empty WITH ITS DENOMINATOR, never omitted. "No
decisions waiting, of 4 open in the queue" and "nothing applied this week, of 3
rulings made" are readings. A missing heading is not.

## What arms it

`trig_017Wzurh3D3fV2JiMQj7NS34`, cron `0 8 * * 0`, a FRESH SESSION each firing
so it starts from the standalone instruction rather than from whatever a
previous conversation happened to hold. First firing 2026-09-20T08:01Z. It was
armed the same day the page was ruled, because a weekly promise with nothing
watching it is CLAUDE.md rule 8 broken on the day it was made.

ONE LIMITATION, RECORDED RATHER THAN DISCOVERED: the trigger stores no
connectors, so its sessions run without the GitHub MCP tools. That is fine for
this page, which reads local files and pushes with git, and it would NOT be
fine for a page that had to query runs or the Actions API. If a future section
needs that, the trigger has to be recreated from a session holding those grants.

## Entries

### 2026-09-20, the first one

NOT YET WRITTEN. It is due on Sunday 2026-09-20, which is the first Sunday
after the ruling. This page was created on the 15th with its structure and its
rules so that the Sunday turn writes content rather than inventing a shape.
