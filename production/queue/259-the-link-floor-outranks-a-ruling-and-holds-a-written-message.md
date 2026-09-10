# 259: the link floor outranks a ruling, and it is holding a finished message

STATUS: READY
OPENED: 2026-09-10

## What is wrong

`tools/producer-check.py` sets `LINK_MIN, LINK_MAX = 1, 2` and enforces
`linkfloor` in the answer register. The director's ruling of 2026-09-10
(`game-design/decision-2026-09-10-ruling-the-move-batch-and-the-fleet-left-
behind.md`, section 5 finding 6, with queue 256) says no site link goes out
until one dispatched publish-glance run prints a served commit on the new
repository, and that the register allows zero until then. THE CODE HAS NOT
CAUGHT UP WITH THE RULING and the code is what runs.

It is not theoretical. One finished message is already held:
`production/outbox-blocked/2026-09-10-the-move-and-the-one-thing-left.answer.md`,
Jafar's answer about the move, sound on every other rule.

## Why it bites twice

The register is walked by `ledger/verify.py`, so a refused message sitting in
`production/outbox/` holds THE WHOLE PRE-COMMIT GATE RED and nothing else in
the project can land while it waits. That is why the message was moved out
rather than left in place, and moving it is a workaround rather than a fix.

## Done looks like

1. The permitted-destination list and the floor both read the ruling: zero
   links is legal while no page is served on the new repository, and the floor
   returns to one once one is.
2. `tools/runner/outbox.py:run_check` agrees with `tools/producer-check.py`.
   THEY MOVE TOGETHER OR THE MESSAGE STILL NEVER SENDS: the send step runs the
   same single-file check, so reconciling only the register leaves the message
   refused at the door instead of at the gate.
3. Tested on BOTH outcomes, accepting case first: a message with no link PASSES
   while no page is served, and a message with a bad link is still REFUSED. A
   floor that cannot tell those apart is not a floor.
4. The held message moves back to `production/outbox/` and the ordinary sweep
   sends it. `production/outbox-blocked/` is empty, and if it stays empty it
   goes away.

## What this must not become

Do not delete the floor. It exists because a message without evidence behind it
teaches vagueness, and that reasoning is untouched by the move. The floor is
wrong only about a window in which no page is served at all.

## Depends on

Queue 256 decides when a page IS served on the new repository, which is the
condition the reconciled floor reads. This item can land before 256 and should,
because the message is waiting now.
