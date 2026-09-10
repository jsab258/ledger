# Messages written, judged sound, and held back by a rule that outranks nobody

STATUS: LIVE. Created 2026-09-10.

A message in here is NOT a draft and NOT rejected on its merits. It is a
finished Producer message that `tools/producer-check.py` refuses for a reason
the studio believes is wrong TODAY and has not yet reconciled in code. It sits
outside `production/outbox/` for one mechanical reason: the register walks that
directory, `ledger/verify.py` runs the register, and a refused message there
holds the whole pre-commit gate red, so nothing else in the project can land
while it waits.

MOVING A FILE OUT OF HERE IS THE WHOLE FIX. When the rule is reconciled, move
it back to `production/outbox/` and the ordinary sweep sends it.

## What is held, and why

`2026-09-10-the-move-and-the-one-thing-left.answer.md`, the answer to Jafar's
question of 2026-09-10 about the repository move and his four-part round trip.

It fails ONE rule, `linkfloor`, which requires one to two links to the glance,
the map, the gallery or the world. Every one of those five permitted
destinations sits under the ARCHIVE's published pages. After the move they show
the world as it was before it, so a link would point him at the wrong thing,
and the message says so in plain words as its reason for carrying none.

THE RULING AND THE CODE DISAGREE, and the ruling is newer. The director's
record of 2026-09-10 (`game-design/decision-2026-09-10-ruling-the-move-batch-
and-the-fleet-left-behind.md`, section 5 finding 6, and queue 256) rules that
no site link goes out until one dispatched publish-glance run prints a served
commit on the new repository, and that the register allows zero until then.
`tools/producer-check.py` still sets `LINK_MIN, LINK_MAX = 1, 2` and enforces
`linkfloor` in the answer register.

## Why it was not simply made to pass

Three ways were available and all three are worse than holding it:

1. ADD A LINK. It would satisfy the rule and mislead him, and it would falsify
   the paragraph in the message that explains why there is no link.
2. LOOSEN `LINK_MIN`. Changing what a gate reads, to make a red thing green,
   in the same turn as the work being gated. That is the one move this project
   says erodes a gate, and a resident may not make it alone in any case.
3. ADD THE FILE TO `LEGACY_LINK_RULES`. That frozen list exists for messages
   written BEFORE the rule they breach. Using it for a message written today,
   to excuse today's message, is the loophole the list's own comment warns
   about.

So the message waits, whole, and the disagreement is visible rather than
resolved by whoever happened to be holding the pen.

## The other thing that has to change with it

`tools/runner/outbox.py:run_check` runs the same single-file check before
sending. Even reconciled in `producer-check.py`, a message with no link is
refused at the send step unless that path agrees. Both halves move together or
the message never goes automatically.
