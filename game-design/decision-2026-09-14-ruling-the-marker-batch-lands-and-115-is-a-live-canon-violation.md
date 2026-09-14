# Ruling, 2026-09-14: the marker batch lands, 115 is reopened as a live canon violation, the twenty-nine say they are undecided, and nothing here is acceptance of the prune

STATUS: LOG, 2026-09-14. NOT CURRENT once the batch this rules on has landed
with the conditions in section 9 applied and Jafar has ruled queue 115; from
then 115's own status line and production/queue/275 are the reading copies and
this is the record of what was decided and why.

Director ruling on a batch of 789 changed lines against a 100 threshold, put by
the resident on 2026-09-14. No code was written by this director, and this
director has no shell (its definition disallows Bash), so every number below
was read off the file and line it names, by grep or by opening the file, in
this session. Two gates the batch claims green on, `tools/producer-check.py
--gate` and `tools/docs-check.py`, were NOT run by me; `ledger/verify.py` runs
both at commit (verify.py lines 1639 and 1803), so the footer is the
measurement that stands, not the resident's scrollback and not this record.

Author: tier-1 director, stamp at the foot naming row 588 of
`.claude/agent-log.tsv` (`2026-09-14T15:16:36Z` TAB `studio-director`, agentId
`a1721fe7539805c12`), the newest director row in the log at the time of
writing. Row 581 (`14:12:50Z`) belongs to the pin ruling and is not claimed.

## 1. The ruling in one paragraph

THE BATCH LANDS, AND IT DOES NOT LAND AS IT STANDS. It lands once seven edits
in section 9 are made, six of them to documents and one to the checker the
batch itself added. The one refusal is queue 115: the batch, as it sits in the
tree, writes "Reviewed 2026-09-14 against production/stages.md and not
reopened" onto a P1 item recording a live canon violation, and a considered
re-closure with no ruling is worse than the sweep it corrects, because the
sweep never claimed to have looked. 115 is reopened before anything lands.
The prune itself is not ruled here; it is Jafar's, and the record says in as
many words that landing is not acceptance.

## 2. The canon violation, first, because it outranks the rest

VERIFIED, every line opened this session:

    canon.md:99          "Permanent per-NPC memory. Nothing is ever wiped;
                          remediation is behavioral."
    MemoryStore.cs:62    public const int MaxEvents = 600;
    MemoryStore.cs:63    const int PruneTo = 500;
    MemoryStore.cs:81    if (Events.Count > MaxEvents)
    MemoryStore.cs:96    int toDrop = Events.Count - PruneTo;
    MemoryStore.cs:98    Events.RemoveAll(doomed.Contains);

At the 601st event the lowest-importance events of the older half are removed
until 500 remain. The comment above it (lines 57 to 61) says "pruning is for
scale, not for forgetting", which is the code's own words about the code and
is not evidence. Two more lines matter for whoever rules it:

    CoreTests/Program.cs:1712   Check(mem.Events.Count <= MemoryStore.MaxEvents,
                                 "a lifetime of ordinary hours stays bounded"
    PerceptionGolden/Program.cs:480   Key(sb, "mem_prune", "maxEvents", ...)

The first is a test that PASSES BECAUSE THE PRUNE FIRES, so the green suite
locks the violation in and will flip whichever way the ruling goes. The
second means the value is already on a printed line.

HOW LONG IT HAS BEEN THERE. The comment cites an audit of 2026-07-27, so the
tree has been in violation for at least seven weeks. It was recorded as
queue 115 on 2026-09-06 at P1 with MANDATORY DIRECTOR RULING in its status,
swept closed by cd55a79c on 2026-09-10 with no ruling, and on 2026-09-14 the
closure audit wrote "not reopened" on it. No ruling exists either way. Runtime
reach is real, not hypothetical: MemoryStore is constructed at
`Game/SimDirector.cs:13821`, `Game/HouseholdHost.cs:102` and
`Game/ConversationHost.cs:75`. Whether any NPC reaches 600 events inside a
play session is NOT MEASURED and no number for it is given here (rule 7).

THE RULING ON LANDING. This batch did not introduce the violation and may
land. It may not land with 115 closed. Condition 1 in section 9 reopens it
with the text dictated there. Until Jafar rules, NOTHING in
`MemoryStore.cs` lines 57 to 99, `CoreTests/Program.cs` lines 1706 to 1715 or
`canon.md` line 99 changes, because moving either side prejudges pillar 1,
which is his. That includes disabling the prune "to be safe": canon outranks
the code, but the acceptance in 115 requires that whichever side moves, the
other is measured and tested, and a disable with no answer at scale is the
"state that satisfies neither" 115's rejecting half names.

WHAT THE RECORD MUST SAY SO NOBODY READS THE LANDING AS ACCEPTANCE, and it
says it here and in 115's status line: THE LANDING OF THE 2026-09-14 BATCH IS
NOT ACCEPTANCE OF THE PRUNE. The tree is in violation of canon by the
project's own law from the moment 115 reopens until his ruling lands, and
every message that leaves the studio claiming permanent memory rests on canon
and not on the code.

TWO THINGS THE BRIEF ASSERTED THAT THE TREE DOES NOT CARRY. (a) "Jafar put it
on his own housekeeping list this morning as a ruling." I grepped
production/stages.md, the four decision-2026-09-14 records and
production/NOW.md for prune, MemoryStore, 115 and housekeeping: the only 115
hit is NOW.md line 2486, the 2026-09-06 audit line. His words are recorded
nowhere. Condition 1 has the resident write them into 115 or write that they
were spoken and not recorded. (b) The research pack going out today carries
"Our whole premise is that nothing is ever wiped" (disco-elysium part2 line
7) and "the moat assumes being seen is permanent" (kcd2 part2 line 14). Those
sentences quote canon and are lawful; they go out. His ruling on 115 decides
whether the code makes them true.

QUEUE: 115 canon-says-nothing-is-wiped-and-the-code-prunes

## 3. Question A: is a marker check honest enough to ship

YES, SHIP IT, and the reason is the one D32 already gives: the rule as Jafar
stated it is "names the item by number, and something checks the item
exists", and that is exactly what the check does. What the rule does NOT
cover is one of the three reasons he gave for it. The three instances are
two orders that never became items (the marker covers that direction) and
182 items that stopped being work with no ruling (the inverse direction,
which no marker can see). A gate that says on every run "this reads markers,
not prose" and prints the size of what it cannot see is honest. The
denominator it prints I re-derived this session: `to the queue` occurs on 23
lines of 17 top-level `game-design/decision-*.md` files, and exactly one of
those files carries a marker (the 2026-09-10 exposure ruling, line 140,
naming 276). So 16 of 17 is the reading and it is correct.

What would make it dishonest is leaving the rule's third reason unaddressed
and unnamed, so the next rung is named here, by number, per D32 itself:

QUEUE: 280 a-closure-dated-after-2026-09-14-names-the-ruling-that-closed-it
QUEUE: 281 the-sixteen-unmarked-rulings-are-read-once-and-marked-or-cleared

280 is the inverse direction, INSIDE `tools/queue-check.py`, which already
walks every status line and already reads the first word (lines 84 to 86 and
127 to 150): a status whose first word is CLOSED and whose date is after
2026-09-14 must name a `game-design/decision-*.md`, the 182 of 2026-09-10 are
grandfathered by date and PRINTED as grandfathered, the accepting fixture is
a closure naming a real record and the rejecting one is a planted tree.
Nothing new ships, per the standing rule at production/stages.md line 296.
281 is documents: read the 23 lines once, classify each as an order or not,
and for every order either add the marker to an existing item or file the
item and the marker. That turns the printed blind spot from unjudged to
judged one time; it does not make it zero for ever, and the print stays.

BOTH MARKERS ABOVE WILL READ RED UNTIL THE ITEMS ARE FILED. That is the gate
doing what it was built for, not an error in this record: the resident files
279, 280 and 281 (documents, which commit on the resident's read) before
running verify, and only then is the tree green. If the red were to be made
to go away by deleting a marker, that would be rule 2's move and is refused.

## 4. Question B: the fourth unruled order

NOT SATISFIED BY 234, AND IT GETS ITS OWN NUMBER. The order, verbatim at
decision-2026-09-10-ruling-the-exposure-ladder-and-the-sheet.md lines 311 to
314: "Grep for other specs that put requirements in a negative prompt and
list them. That is ADJACENT, so it goes to the queue with a name and does not
enter this change: 'negative-half requirements audit'." Its deliverable is a
LIST WITH A COUNT over the specs examined. Queue 234's acceptance is
"negativeActive printed per item on every validate run, and each shipped spec
carrying a line saying what its negative is FOR given that value". A builder
doing 234 properly would open every negative and might notice a requirement
sitting in one, but 234 does not require the list, the count, or the move to
the positive half, and an order satisfied by a side effect of adjacent work
is the shape D32 exists to stop. 233 is further away still: it is about what
the positive half must name.

QUEUE: 279 negative-half-requirements-audit

Acceptance for 279, dictated so the item does not have to invent it: every
image spec under tools/imagegen/specs and production/specs walked, the count
walked printed, and for each spec whether any requirement (a thing that MUST
appear, or must not) sits in the negative field; a printed list of the hits
with `requirementsInNegative=N/of=M`; and for each hit, the sentence moved to
the positive half or the reason it stays. 234's finding that the negative is
never evaluated at cfg 1.0 is the reason this list matters: every hit is a
requirement that was never read.

The builder's refusal to write a marker for an unconfirmed mapping was
correct and is the convention working: a marker asserting a mapping nobody
confirmed would have gone green on the wrong item, which is the silent form
of the same fault.

TWO CORRECTIONS THAT RIDE WITH THIS. (a) 278 exists for instance 2, and its
own status says "THE MARKER FOLLOWS IT"; it has not. `grep '^QUEUE: '` under
game-design/ finds exactly one marker in the tree, 276. The 278 marker goes
into the 2026-09-10 ruling below line 164, where the order sits (lines 155 to
164), and the 279 marker goes below line 314. (b) D32 lines 26 to 27 say of
instance 2 "It exists in no queue item", which was true when written and is
false now; it names 278. D32 also gains the fourth instance, naming 279,
because a register of three that was four by the time it landed is the decay
D32 is about.

## 5. Question C: the index resolves against queue/ and done/

RIGHT, AND IT MISSES ONE DIRECTORY THAT THE INSTRUMENT IT IMPORTS FROM ALREADY
WALKS. `tools/docs-check.py` queue_index (lines 212 to 241) walks `queue` and
`done`. `tools/queue-check.py` count_queue (lines 151 to 156) also walks
`blocked/`, and counts an item moved there as blocked. No `production/queue/
blocked/` exists today (glob, this session), so nothing is red, but the day
one item is moved there its ruling goes red for the same reason the brief
corrected its own first design: rule 5b's ratchet, and the work breaking the
tool. Condition 5 in section 9: index `blocked/` too, print `inBlocked`, and
prove it on a planted tree, since a real fixture pinned to a directory that
does not exist is the trap the file's own comment names.

ONE MORE THING IT CANNOT SEE, NOTED AND NOT ORDERED. `QUEUE_NUM_RE` (line
173) requires a numeric prefix, so an unnumbered item cannot be named by a
marker at all. There is at least one live: `production/queue/
art-atlas-01-integration.md`, reopened today. The skip is silent; the same
condition has the checker print `unnumberedSkipped=N` beside `indexed`, because
a file it declined to index is part of the denominator (rule 3b).

## 6. Question D: the twenty-nine

THE POSTURE IS RIGHT AND THE TREE DOES NOT CARRY IT. 275 is Jafar's call
(NOW.md line 46 to 48, "HIS CALL"), and the 29 are precisely the part of it
the audit could not make for him, so they are not to be resolved before
landing by a resident deciding on his behalf. But measured this session:

    files carrying "Reviewed 2026-09-14 against production/stages.md
      and not reopened"                                             168
    audit's keep-closed 139 plus unsure 29                          168
    files anywhere in the repository carrying "unsure", "UNSURE"
      or "undecided" that are queue items                             0
    files carrying "keep-closed" or the 13/139/29 split               0

So the 29 the audit could not decide carry the same sentence as the 139 it
did, the sentence reads as a decision, and the audit's own split, including
that it read full prose for about twenty of 181, exists in no file. A
decision that lives only in a conversation decays into a preference; a
classification that lives only there decays into "reviewed". Condition 3.

## 7. The thirteen "by Jafar"

138's line says "REOPENED 2026-09-14 BY JAFAR, BY NAME. His words: 'Queue 138
is reopened.'" The other thirteen (028, 030, 032, 037, 055, 145, 146, 147,
148, 150, 151, 208, art-atlas-01-integration) say "REOPENED 2026-09-14 by
Jafar." The difference between those two phrasings is deliberate and far too
subtle: the next reader takes both as him naming the item. The brief
describes the thirteen as the closure audit's classification under 275's
proposed default ("reopen the items the stages name a route for"). Condition
4 has each line say which it was, in whichever direction his words support.

## 8. The research sends

APPROVED. What I opened: the kcd2 pair in full; part 1 ends with the cut
announcement at its last line and part 2 opens with it. What I measured: all
ten parts carry the announcement at column 0 (5 `[CUT HERE: part 1 of 2`, 5
`[PART 2 of 2`, 10 of 10 files); zero em-dashes across the ten parts and
zero in D32. `RESEARCH_DELIVERIES` (producer-check.py 362 to 393) is five rows
of three names, `RESEARCH_VERBATIM` is derived from `row[:2]` (399), and the
blocked originals are the third name and never sendable. What I did not do:
run the gate; verify runs it at commit. NOW.md line 57 records that nothing
in the five has been acted on, and the kcd2 summary itself is the accepting
case for that rule (its four questions are his, not the studio's).

## 9. Conditions of landing, in the order to do them

1. QUEUE 115 REOPENED. Its status line begins with the word REOPENED
   (queue-check reads the first word) and reads: "REOPENED 2026-09-14 by
   director ruling, game-design/decision-2026-09-14-ruling-the-marker-batch-
   lands-and-115-is-a-live-canon-violation.md. P1; MANDATORY DIRECTOR RULING
   stands and the ruling is Jafar's, pillar 1. A LIVE CANON VIOLATION:
   canon.md line 99 against MemoryStore.cs lines 62 to 97, in the tree since
   the 2026-07-27 audit the code's own comment cites; CoreTests
   Program.cs:1712 asserts the prune fires. Was: CLOSED 2026-09-10 by
   cd55a79c with no ruling (see 275); the 2026-09-14 closure audit wrote 'not
   reopened' on it, which the ruling above reverses. THE LANDING OF THE
   2026-09-14 BATCH IS NOT ACCEPTANCE OF THE PRUNE. Nothing in MemoryStore.cs,
   CoreTests 1706 to 1715 or canon.md 99 changes before he rules." Below it,
   his words putting it on his list today, quoted, or the sentence "spoken on
   2026-09-14 and not recorded; this line is the only record".
2. THE TWO MISSING MARKERS in decision-2026-09-10-ruling-the-exposure-ladder-
   and-the-sheet.md: `QUEUE: 278 the-determinism-matrix-a-ruling-ordered-and-
   nobody-filed` below line 164, and `QUEUE: 279 negative-half-requirements-
   audit` below line 314, each with the one-line note the 276 marker carries.
3. THE TWENTY-NINE SAY SO. 275 gains the audit's numbers (reopen 13, keep
   139, undecided 29, of 181; full prose read for about 20, the rest by status
   and spec line) and the 29 listed by number. Each of the 29 keeps CLOSED as
   its first word and its tail changes from "and not reopened" to "and
   UNDECIDED, the audit could not make this call for him; see 275". If the
   list of 29 no longer exists anywhere, 275 says exactly that, and all 168
   tails change to "by status and spec line, not reopened; 275 is still his
   call", so the loss is recorded and not papered.
4. THE THIRTEEN NAME THEIR AUTHORITY. If Jafar's words cover them, 275 quotes
   the words and the lines stand. If his words were "Queue 138 is reopened"
   and no more, each of the thirteen reads "REOPENED 2026-09-14 by the
   closure audit under 275's proposed default, pending his overrule", and
   275's status says the default was applied on 2026-09-14 and awaits him.
5. docs-check.py queue_index indexes `blocked/` beside `queue` and `done`,
   the run line gains `inBlocked=` and `unnumberedSkipped=`, and the fixture
   is a planted tree with one item in each of the three places and one
   unnumbered file. Instrument-builder; the same file it is already in.
6. D32: lines 26 to 27 name 278; a fourth instance names 279 with the
   sentence from section 4 above; the title stays.
7. FILE 279, 280 AND 281 under production/queue/ with the acceptance in
   sections 3 and 4, BEFORE running verify. Until they exist, this record's
   three markers read red, and that is the gate, not a fault.

Then `python3 ledger/verify.py`, the footer from the file, one commit. The
prune stays exactly as it is.

## 10. What is refused, and what is not ruled

Refused: landing with 115 reading "not reopened"; deleting any marker to
clear a red; touching MemoryStore.cs, CoreTests 1706 to 1715 or canon.md 99
before Jafar rules. Not ruled: the prune itself, which is his; and the
retirement or reversal of any of the 139 the audit kept closed, which is
275, also his. Adjacent and named only: an events-per-NPC-per-game-day series
from a real soak, which his ruling will need and which 115's own body already
orders ("that answer must be measured, not asserted; note queue 116").

<!--RULING spawn=2026-09-14T15:16:36Z-->
