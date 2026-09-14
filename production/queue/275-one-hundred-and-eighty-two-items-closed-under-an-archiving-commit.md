# 275: 182 queue items were closed under an archiving commit, and the milestone to protect is one of them

STATUS: READY, and it needs Jafar rather than a builder
OPENED: 2026-09-14, found by a director reading the queue against the new stages document.

## The measurement

    queue files carrying "CLOSED 2026-09-10, not on the ladder"   182
    queue files examined                                          267
    records under game-design/, ledger-v2/ or NOW.md that
      contain that phrase                                           0

So 68 percent of the queue was closed on one day with a phrase that appears
nowhere in any ruling, decision record or live-state file.

## It is not unrecorded, it is UN-RULED, and the difference matters

The closures rode `cd55a79c`, 2026-09-10T13:20, whose subject is "D18 lands at
five sites, 510 files are archived and nothing is deleted". So there IS a
commit, and the corrected claim is narrower than "nobody wrote it down": what
is missing is a RULING that says the queue was cut by two thirds, and any
statement of what went with it. An archiving commit is where you look for
archived files, not for the disposal of the work plan.

## The casualty that makes this urgent

`production/queue/138-one-playable-visual-crime-and-consequence-loop.md` is
among the 182.

On 2026-09-14 Jafar wrote the stages, and stage 3 is "one street that knows me,
the crime loop visible in a place that looks right", with his own words beside
it: THE MILESTONE TO PROTECT IF ANYTHING SLIPS. Its queue item has been closed
for four days as "not on the ladder", and the ladder he judges by eye has no
rung under stage 3 at all, so the milestone he named cannot be seen to slip.

Also among them, per the director's read: the weekly process audit (900), the
row-law checker (107), and every item the quality ladder's next rungs cite for
stages 2 and 3.

## What is being asked

THIS IS A DECISION AND NOT A CLEANUP, which is why it is addressed to him.

The closures may have been entirely correct: "not on the ladder" was a real
criterion on 2026-09-10, when the ladder was the plan and the phases were
being retired. Four days later the stages document puts many of those items
back on the route. So the question is not whether the sweep was wrong, it is
which of the 182 the stages have reopened.

Proposed default, to be overruled rather than merely approved: reopen the items
the stages name a route for, starting with 138, and leave the rest closed with
the phrase corrected to name the commit that closed them so the next reader can
find it in one step.

## What must not happen

Do not reopen all 182 to be safe. A queue nobody can read is the condition this
sweep was trying to fix, and undoing it wholesale would recreate it while
destroying the one thing the sweep got right.
