# D32: a ruling that orders work to the queue names the item by number

STATUS: DECIDED 2026-09-14 by Jafar, dictated and recorded by the resident.
Process level: it binds how rulings are written and adds a gate, and it was
made from three failures counted on one day.

## The rule, as given

**A ruling that orders work to the queue NAMES THE ITEM BY NUMBER, and
something CHECKS the item exists.**

His reason, in his words: **"Three instructions today landed in a commit and
became nothing, and no gate caught any of them."**

## The three, because the rule is only believable with them

1. **A research rung ordered by name, never filed.** The ruling of 2026-09-10
   said the night pin "is therefore a RESEARCH RUNG and goes to the queue with
   a name: settled night exposure reference", and dictated its three steps so
   the next brief would not have to invent them. A director grepped 268 files
   under `production/queue/` on 2026-09-14 and found ZERO hits. Four days dark.
   Now filed as `production/queue/276-settled-night-exposure-reference.md`.

2. **A measurement ordered and not filed.** The same ruling required the full
   camera-by-condition determinism matrix printed with its count, because the
   reported failure was a sample of one with no denominator. FILED 2026-09-14 as
   `production/queue/278-the-determinism-matrix-a-ruling-ordered-and-nobody-filed.md`
   and marked in its ruling, four days late. It was the checker's planted
   rejecting fixture before it was an item.

4. **A fourth, found by the checker's own builder while measuring.** The same
   2026-09-10 ruling orders a "negative-half requirements audit" to the queue BY
   NAME at its lines 311 to 314. Queue 234 was ruled NOT to satisfy it: 234's
   acceptance is a per-item print, not the list with its count, and an order
   satisfied by a side effect of adjacent work is the shape this rule exists to
   stop. Filed as `production/queue/279-negative-half-requirements-audit.md`. THE
   RULE FOUND ITS FOURTH CASE BEFORE ITS GATE HAD LANDED.

3. **182 items closed with no ruling naming what went.** They rode `cd55a79c`,
   an archiving commit. Among them was the playable crime-and-consequence loop,
   which four days later Jafar named as the milestone to protect.

## What the check can and cannot do, said here so nobody over-reads it

The honest mechanism is a MARKER: a ruling that orders queue work writes the
number explicitly, and the gate verifies the item exists. THAT CANNOT DETECT AN
ORDER WRITTEN WITHOUT THE MARKER, so the rule is a convention the gate only
partly enforces, and the gate must PRINT that limit rather than imply it read
the prose. A check that says "12 markers found, 12 items exist, and an order
written without a marker is invisible to me" is honest. One that reports a
clean sweep is not.

## Where it lives, and why nothing new ships

Jafar's other standing rule of the same day: **no new instrument this month
unless an existing one is retired in the same batch.** So this check goes
INSIDE an instrument that already walks these files rather than becoming a new
tool, and nothing is retired because nothing is added.

## What this does not change

It does not require a ruling to file the item itself. A ruling may order work
and a builder may file it, as happened with 276. What is forbidden is the order
existing with no number and no item, which is the state all three instances
above were in.
