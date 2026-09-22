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

## HE RULED IT, 2026-09-14, and these are his words

    "Queue 138 is reopened. Of the other 181 closed on 10 September, reopen only
     what the stages name a route for, and correct the closure phrase to name its
     commit."

THOSE WORDS ARE THE AUTHORITY FOR ALL FOURTEEN REOPENINGS, not only 138. He gave
the criterion (what the stages name a route for) as well as the one item, so the
thirteen the audit selected stand on his ruling and not on the studio's discretion.
What remains his is whether the audit applied that criterion correctly.

## WHAT THE AUDIT FOUND, with its coverage stated

    reopened      13   of 181   plus 138, which he named himself
    kept closed  139   of 181
    UNDECIDED     29   of 181
    13 + 139 + 29 = 181, and 14 + 168 = 182 including 138

COVERAGE, SAID PLAINLY RATHER THAN IMPLIED: full prose was read for about twenty
items. The rest were classified on their status and spec lines, which are real
content and not filenames, but are not the whole item. That is why the undecided
bucket is 29 and not smaller: it is what an honest reader could not call.

THE TWENTY-NINE UNDECIDED, by number:

    027 035 051 059 102 114 116 117 118 121 122 136 144 149 154 155 156 157 159 160 162 165 167 168 185 188 190 194 228

Each carries, in its own file, the one sentence that would settle it. None was
swept into reopen to be safe, because a queue nobody can read is the condition the
2026-09-10 sweep was correctly trying to fix.

## ONE OF THE 182 WAS NOT A CLOSURE QUESTION AT ALL

`production/queue/115-canon-says-nothing-is-wiped-and-the-code-prunes.md` is a
LIVE CANON VIOLATION and was P1, MANDATORY DIRECTOR RULING. The closure audit
wrote "not reopened" on it. A director reversed that on 2026-09-14 and it is now
REOPENED: canon.md line 99 says nothing is ever wiped, MemoryStore.cs prunes to 500
at 601 events, and CoreTests Program.cs:1712 asserts the prune fires, so the
violation sits inside a green suite. The prune itself is Jafar's ruling and nothing
moves before it.

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
