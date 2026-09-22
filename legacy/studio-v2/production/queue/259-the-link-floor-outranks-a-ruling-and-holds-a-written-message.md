# 259: the link floor outranks a ruling, and it is holding a finished message

STATUS: ITEMS 1 TO 3 LANDED; THE CONDITION FLIPPED 2026-09-15. ITEM 4 STILL WAITS ON 260.
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

## Amended 2026-09-11 by the director, sections 4 and 5

ITEMS 1 TO 3 LAND NOW; DONE ITEM 4 WAITS ON 260. The 08:40Z ordering ("259 must
not land before 260's length gate") named ONE hazard: releasing the held
4739-character message into the same permanent 400. This batch releases nothing
from `production/outbox-blocked/`; both held messages stay there. So the code
half lands, and item 4 (move the held message back, empty the directory) waits
on 260 AND on the Producer rewriting both held messages under the cap or
dropping them. The ordering ruling is not overturned, it is attached to the
item it was written for.

ITEM 2 IS SATISFIED BY CONSTRUCTION AND PROVEN ONLY BY A RECEIPT. `run_check`
shells out to the single-file path with no `--root`, so it reads the marker in
its own checkout. That is construction, not evidence. The evidence is
`production/outbound/2026-09-11-yes-it-works.answer.receipt.txt` appearing on
`pc-inbox` after the push. If a `refused-` record naming `linkfloor` appears
instead, the PC's checkout or its copy of the tool is behind this commit, and
the instrument is the first suspect.

Ruling: game-design/decision-2026-09-11-ruling-the-link-floor-marker-batch-and-the-answer-already-sent.md

## The window closed, 2026-09-15

The conditional floor items 1 to 3 built has been sitting in the OFF branch
since it landed, because `production/site-served.txt` read `servedCommit=none`.
Queue 256 landed the other half in one commit and that file now names a served
commit, so the floor is LIVE again at the ruled 1..2 and the register requires
a link once more. Read off the gate's own done line rather than from the code:

    linkFloorActive=true reason=page-served..production/site-served.txt..
    servedCommit/5a8ef789dc1f5044052abd496667352c752b1b9c
    filesLinkFloorOff=40/42 markerOriginConsistent=true

`filesLinkFloorOff=40/42` is NOT the floor failing to bite. Those 40 are the
messages already sent when the site moved, named on `PRE_MOVE_MESSAGES` and
counted on their own report line; the 2 files not on it faced the full floor
and passed. A message the Producer writes tomorrow is on no list and is refused
without a link, which is the behaviour this item exists to restore.

ITEM 2 IS UNCHANGED AND STILL PROVEN ONLY BY A RECEIPT. `run_check` shells out
to the single-file path with no `--root`, so it reads the marker in its own
checkout. Nothing about today's change alters that; what changes is which
branch that read takes. The evidence remains a receipt appearing on `pc-inbox`
rather than a `refused-` record naming `linkfloor`.

ITEM 4 STILL WAITS ON 260 and on the Producer rewriting or dropping the held
messages. `production/outbox-blocked/` holds seven files and this batch
releases none of them.

  RULED 2026-09-15 05:43Z: the floor is back at the ruled 1..2 and the forty
  are waived by name at the gate only; at the door every name faces the live
  floor. Item 4 unchanged, still waiting on 260.
