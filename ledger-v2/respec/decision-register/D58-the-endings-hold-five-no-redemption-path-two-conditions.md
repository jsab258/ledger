# D58. The endings hold: five, written and wired, no redemption path, on two conditions

CANON: none

Nothing in canon changed. D19 (Mickey's is a minicab office) is applied to the
endings' wording as checkpoint work under D43, named below.

Ruled by Jafar, 2026-09-21, in his SECOND message of that day, ruling on the
crime and combat coverage audit. Kept verbatim in
`game-design/decision-2026-09-21-the-crime-and-combat-audit-ruled-eight-verbs-and-the-endings-hold.md`.
Written by the director the same day; the resident reviews and commits.

## The rule, as given

**"The ending. There are five, written and wired, and the red team's finding
is narrower than it sounded: a route back exists, and none costs less than
half of what you have. That is the game, not a fault. It is what permanent
memory means in a noir town, and no redemption path is added. It holds on two
conditions.**

**First, checkpoint work now: confirm that the two endings left to a hunted
player, keeping everything with nobody who knew you before and giving up the
business to keep the people, are actually reachable from a hunted state. The
audit read only the first gate of the eligibility rule and says it is one
method away from certain. If either is unreachable, that is the fault, and it
comes to me as a card.**

**Second, the player must be able to see the cost coming as it approaches,
through the surface D33 already ruled, where Tom's own reading is shown with
its reasons. A cost the player could not have seen is a trap; a cost he
watched arrive is the game."**

## "Five, written and wired", checked in the code 2026-09-21

`ledger/Assets/Scripts/Core/ActThree.cs`: `public enum Ending` at line 28;
`Eligible(LedgerState s)` at line 267 is the eligibility rule. Its members, as
added in that method: Quiet at line 287 (`s.HandedOver && s.HasReadySuccessor
&& !s.Hunted`), Both at 330, StraightLife at 345 (`!empireSurvives &&
lifeSurvives`), Kingdom at 358 (`empireSurvives && booksHold`), BurnBoth at
361 when none of the other four is live; `Resolve` at 367 returns BurnBoth
when nothing is live, else the first. Five endings: Quiet, Both, StraightLife,
Kingdom, BurnBoth (`Ending.None` at line 123 is the unset value). FIVE HOLDS.
`EndingText` at line 542 is where their prose lives.

His "the two endings left to a hunted player, keeping everything with nobody
who knew you before and giving up the business to keep the people", read
against those names, is Kingdom and StraightLife. That mapping is the
director's reading; the audit's own names are on the branch. The reachability
check reads the whole of `Eligible()`, not its first gate at line 287, and says
which names it traced.

## Condition 1: checkpoint work now, QUEUE 399

`production/queue/399-the-audit-read-only-the-first-gate-of-the-eligibility-rule.md`,
line `sim`, READY 2026-09-21 as checkpoint work per his marking. Confirm
Kingdom and StraightLife (or whichever two the check names) are reachable FROM
A HUNTED STATE, by tracing `Eligible()` and the state that feeds it, with a
planted hunted state as the fixture. If either is unreachable: a card to him,
not a fix. (When this record was first written, no file numbered 388 to 398
existed and it said "the resident files it"; 399 was filed the same afternoon
and this paragraph now names it, per the afternoon ruling of 2026-09-21.)

## Condition 2: a design condition, recorded here and binding stage 3 and stage 4

The cost is visible as it approaches, through D33's surface: the player sees
their own position, never other minds, and Tom's own reading is shown with its
reasons. What it binds: every ending-relevant cost (a man's nerve near its
ceiling, the books' strain, being hunted, the successor's readiness) is
readable by the player BEFORE it lands, as Tom's reading with its reasons,
never as a number from another mind and never as a meter (D34). That is stage
3's crime layer (D56) and stage 4's Ledger (D12, D37). Nothing is built this
week. His line is the test: "A cost the player could not have seen is a trap;
a cost he watched arrive is the game."

## No redemption path is added

His first message listed among the owed "how the game ends, including a route
to going straight, since the red team found no route back once the town
turns". This ruling narrows that: a route back exists (StraightLife and Quiet
in the enum above), none costs less than half of what you have, and NONE IS
ADDED. The first message's line is superseded on this point by this record,
and marked so in that file.

## The pub wording: checkpoint work under D43, QUEUE 400, sites found 2026-09-21

His words: **"One correction, checkpoint work now under D43: the endings
still speak of signing over a pub. D19 made Mickey's a minicab office. The
logic survives, since a private-hire licence settles who owns a cab firm the
way a pub licence did, but the wording is wrong and gets updated in the same
pass."**

`production/queue/400-the-endings-still-speak-of-signing-over-a-pub.md`,
line `sim`, READY 2026-09-21 as checkpoint work per his marking, wording only
under D43.

Sites carrying "pub" in `Core/ActThree.cs` (grep, whole word, 2026-09-21):
lines 10, 15, 167, 175, 184, 197, 283, 389, 394, 534, 539, 544, 573 ("the
pub's books", "Hook Street pub", "a pub's books", "The pub is a pub", "You have
a pub"). Sites carrying "sign it over": `Core/ActThree.cs:553`,
`Game/ActThreeHost.cs:585` and `:597`, `Game/DialogueUI.cs:523`; the verb
survives, the object changes. `game-design/roadmap-history.md:719` ("signed
over") is history and is left. Canon's line: `canon.md:61`, "Mickey's, a
minicab office in the Hook (D19)".

These strings are in Core. Whether a golden file or a CoreTests fixture pins
`EndingText` was not checked; because it may, and because Core keeps its full
review (D45), the change is a builder's with review and not a hand-apply. 399
and 400 run in the same pass, as he said.

## What this does not decide

The endings' prose beyond the pub wording. The result of the reachability
check. Turning yourself in, which D56 holds until the endings are traced.
