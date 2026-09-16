# Ruling, 2026-09-16 (03:27Z): queue 326 lands AMENDED, the floor is read, the key that changed meaning changes its name, five things the 3416-check suite could not see, and what the first carrying run must print

STATUS: LOG, 2026-09-16. NOT CURRENT once the first landed run whose commit
CONTAINS the amended batch has been read against section 9; from then the
verdict file, the g++ suite and the queue items filed in section 10 are the
reading copies and this is the record of what was ruled and why.

Director ruling on the queue 326 batch, three files under the GATED
`ue-probe/` prefix, 769 lines against the 100 bound:
`ue-probe/Source/LedgerProbe/Public/FrameStats.h` (+405),
`ue-probe/tests/frame-stats-test.cpp` (+288),
`ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp` (+76). Item:
`production/queue/326-the-light-probes-control-reads-the-same-as-the-lights-it-floors.md`.

Author: tier-1 director, stamp at the foot naming row 658 of
`.claude/agent-log.tsv` (`2026-09-16T03:27:21Z` TAB `studio-director` TAB
`fable` TAB `default` TAB `a6b87c1efb9aaa3a2`), the newest row in the log.
The reference commit `be57db05` is `.git/logs/HEAD` line 121, epoch
1789528102, which is 2026-09-16T03:08:22Z ("The wake records for queue 326,
and why it goes ahead of 319"); row 658 is nineteen minutes newer. Line 122,
a `reset: moving to HEAD` at 03:18:51Z, is the builder's revert of the
half-applied accounted key (section 5), and it is consistent with the account
I was given. Rows 653, 654, 656, 657 (`instrument-builder`) and 655
(`engine-specialist`) are builder lives and are not claimed. No code was
written by this director, this director has no shell and no `git diff`: the
tree was READ at the line numbers in section 0, the run 47 verdict was read
by line, and the builder's summary was not read except as the caller relayed
it and as the wake file states it. The four g++ binaries at 3416 checks are
the caller's printed number, not mine; nothing in this ruling rests on that
number except the statement that the batch compiles and its own checks pass.

VERDICT IN ONE LINE: the finding is real and the rule is right; the batch
does not land as it stands because the run-level key keeps a name whose
meaning it changed, two print branches ship unrun, the header carries an
arithmetic claim the verdict refutes, one fixture's two tallies disagree, and
two new caps truncate in silence. All five are in the g++-compiled files and
one comment line, one builder pass, and this ruling covers the amended batch.

## 0. What was opened

`FrameStats.h` 1 to 961 whole on the first read (the 326 material is 322 to
332, 347 to 355, 401 to 412, 448 to 544, 571 to 607, 610 to 772, 774 to
872). `frame-stats-test.cpp` 1 to 865 (the 326 block is 406 to 688; the
queue 059 light block it extends is 322 to 405). `VignetteShot.cpp` 1 to 962
(globals 526 to 547), 2008 to 2030 and 2140 to 2176 (`PlaceCamera`, the two
`GShotPin` write sites), 2560 to 2610 (the verdict assembly, floor lines at
2584 to 2592, the done line at 2593 to 2597), 3180 to 3420 (`EmitLightLine`
3205, `BeginNextProbe` 3232, `MeasureProbe` 3291, `StartLightProbe` 3337,
`AfterFrame` 3370), 4490 to 4622 by grep (`ApplyShot` is the only caller of
`PlaceCamera`, line 4594). `SurfaceBind.h` 1560 to 1609 (the naming law at
1571 to 1577). `VignetteSpec.h` by grep (`ExposurePinWord` at 3011, takes
`const ExposurePinIn&`, returns `const char*`). The run 47 verdict
`production/d1-probe/ue-vignette-verdict.txt` lines 270 to 325 whole (the 48
light lines and the done line at 323) and line 189 by key for the shot line's
pin family. `verify.py` 3660 to 3677 (the `ue-probe/` scope entry and its
stated reason), 5725 to 5770 (the gate's three states and the stamp rule).
D45 whole. The rulings log 1 to 40 and 338 to 355. The 2026-09-15 22:25Z
ruling 1 to 60 and 690 to 741 as the house format. `.claude/agent-log.tsv`
645 to 659. The wake `production/wakes/2026-09-16T0345Z-e0a512a3.wake.txt`
whole. Queue 326 whole.

Greps, this session, with counts. `lightsReachedFrame` over the tree
excluding the verdict: 15 hits in 8 files, of which the live ones are the
header (comment 329, comment 778 to 784, format 845 and 853), the test (486,
564, 567, 583) and one verdict comment string in the .cpp (2591); the rest
are queue 326, queue 319, the 2026-09-03 lighting-probe ruling and one wake
file, all historical. NO TOOL READS THE KEY: nothing under `tools/` or in
`verify.py` matched. The four strings of the NO-CONTROL and no-comparable
print branches (section 6(a)) over the test: 0 hits of 1 file examined.
The six new floor identifiers over the .cpp: 16 hits, all read. The stamp
pattern over `game-design/`: the recently landed rulings close with the HTML
comment carrying `RULING spawn=` and the row's timestamp, with or without a
`paths=` list, which is the form `verify.py` 5744 asks for and the form at
the foot of this record.

## 1. The finding, re-derived from the verdict and not from the brief

The caller verified the camA lines to the pixel; I verified them again and
went further, because a ruling on a rule needs the whole run, not the shot
the item was written from.

At `vign_camA_night` (verdict 275 to 282) the control prints

    deltaPixelsRoseAtLeast=921600/921315/917618/898971/802512/597624
    deltaPixelsDarkerWithLightOn=0/921600

and `lantern1`, `lantern2`, `lantern3` and `east_parade_interior5` print the
same six integers. `lantern0` prints `157235/79512/28412/5977/786/46`.
`east_parade_interior0` prints `921600/921315/917269/891812/763592/539411`
and `east_parade_interior2` prints `921600/921315/917426/892147/769620/551675`,
tied with the control at two edges and below it at four. The control's
`meanOffFull` is 0.00075 and so is each of the four identical lights': five
probe frames of one shot that came back with the same near-black mean,
against a reference at 0.25136. Confirmed as stated.

THE OLD DONE LINE IS REPRODUCED FROM THE OLD RULE, which is the check the
brief did not carry. Counting lights whose first `deltaPixelsRoseAtLeast`
entry is above zero across the six probed shots: camA 7 of 7, camB 5 of 7
(lantern0 and lantern3 are all zeros), pinset_1 7 of 7 (lantern3 at 1),
pinset_2 1 of 7 (lantern3 at 56), pinset_3 4 of 7 (62, 4, 92, 58), pinset_4
6 of 7 (lantern3 at 0). Sum 30, and line 323 says `lightsReachedFrame=30/42`.
The caller's statement of what decided the shipped number is therefore
proven from the printed series, not from the comment that says so.

`pinset_night_2` (299 and 303): the control has an all-zero rise histogram,
`deltaMeanFull=-0.37873` and `deltaPixelsDarkerWithLightOn=921600/921600`;
its lantern3 has `56/0/0/0/0/0`. Under a rise-only floor 56 beats 0 and
lantern3 reads. Confirmed as the builder said, and it is the case the third
fixture plants (test 535 to 557).

## 2. Ruling on the name: the key is renamed, and the stat token is not enough

THE DECISION. `lightsReachedFrame` does not survive this batch under that
name. The run-level count becomes `lightsAboveFloor=R/U` and its stat key
`lightsAboveFloorStat`. The old name is asserted ABSENT by the test on every
done line the test builds. No tombstone key: the old instrument is gone, and
a grep for its name in a new verdict finding nothing is the correct answer,
because `lightProbeStatus` on the same line already says whether the pass
ran.

WHY THE TOKEN IS NOT SUFFICIENT. The naming law at `SurfaceBind.h` 1571 to
1577 is about a grep, not about a reader: "a grep that found either under one
name would take whichever line it reached first". The evidence channel here
is a committed file with per-run copies keyed by short-sha and a git history
of the same path, so a grep for the old key over that channel returns
`30/42`, `36/42` and then whatever the next run prints, as one series under
one key. The stat token sits 250 characters into a 1200-character line and
is not what a key-grep returns. A key whose numerator rule AND denominator
both changed is a new instrument, and a new instrument gets a new name; the
project's own precedent from the last ruling on this file family is
`wetnessValue` to `wetnessBindValue` on 2026-09-15, "because the number
became a seed, old names asserted absent", which is this case exactly.

WHY NOT KEEP THE NAME FOR CONTINUITY. There is no continuity to keep: the
run 47 number counted one pixel rising by one code value and the new number
counts lights that beat their own shot's control, over a denominator that
excludes swamped shots. Plotting them on one axis is the fault. The
acceptance sentence in queue 326 names the old key, and the acceptance's
object is the rule, not the name; the close-out says so.

THE NAME ITSELF. `lightsAboveFloor` pairs with the per-light
`lightAboveFloor=YES` and `lightAboveFloor=NO` the batch already prints and
with the run-level plural pattern the line already uses (`lightsProbed`,
`lightsSkippedBudget`, `lightsInNoReadShots`). The per-shot
`lightsReadThisShot` keeps its name.

Cost, measured by grep in section 0: two format strings and one comment in
the header, four `Check` strings in the test plus the absence checks, one
verdict comment string in the .cpp. No Python reader. Condition C1.

## 3. Ruling on the decision rule: it holds, and here is what it cannot do

`LightReadEdge` (header 469 to 478): for E from 32 codes down to 1, the
light reads at the first E where the light's `RoseAtLeast[E]` strictly
exceeds the control's `MovedAtLeast[E]`, integer pixel counts, same
pre-existing edge. It returns the HIGHEST edge with a surplus. Checked
against the code, not the comment.

THE ASYMMETRY IS CORRECT AND IT IS THE PHYSICS. The probe frame is the one
with the light OFF, so a genuine contribution can only appear as pixels that
ROSE in the reference relative to the probe; a probe frame that came back
brighter is the exposure answering, which `deltaPixelsDarkerWithLightOn`
already counts and which must not be a contribution. The control toggled
nothing, so every pixel it moved, either way, is the run's own disturbance.
Rises on the numerator, moves on the floor: the builder's reasoning holds.

`MovedAtLeast` RATHER THAN RISES ALONE IS RIGHT, and pinset_night_2 is the
proof from the series (section 1). A control that darkened every pixel has
an empty rise histogram and a full move histogram; a rise-only floor would
read as pristine at the shot whose exposure was least stable. The cost is
that under symmetric one-code jitter the moved floor is about twice the
rise-only floor at the lowest edges, so a faint light contributing a code
or two over less than the jittered fraction of the frame will not read at
edge 1. That is the right side to err on: with one control frame, a
one-code contribution under one-code jitter is not distinguishable from the
jitter, and NO carries both counts so nobody reads it as dark.

THE FLOAT ARGUMENT HOLDS. At camA the control and four lights print
`deltaMeanFull=0.25060`, and `deltaMeanPeak` reads 0.86557 on the control
against 0.86558 on the lights, so the doubles differ in the sixth place
between frames whose histograms are byte-identical; a strict comparison on
those doubles would decide by rounding. Integer counts at a printed edge,
tie is not a read: nothing chosen.

THE ONE NUMBER IN THE COMPARISON THAT IS NOT AN INTEGER. `MeasureLightDelta`
compares the move against the edge minus 1e-9 (header 408). I cannot see
from the tree whether 326 added it. Classified: it is a representation
guard, not a bound. A luma difference times 255 is 0.299a + 0.587b + 0.114c
for integer channel steps a, b, c; the only such value within a thousandth
of an edge is the exact edge (a = b = c = 1 gives 1.000 in the reals and
0.9999999999999999 in doubles), so 1e-9 decides nothing except which side
of the literal integer that rounding lands on. It is nine orders below the
quantum it guards and cannot be crossed by any measurement. Exempt from
rule 2 on that reasoning, and the reasoning is written here so the next
reader does not have to redo it.

WHAT THE RULE CANNOT DO, so nobody over-reads the first green:

(a) It counts a light that beat its control by ONE PIXEL as a read. On run
47's numbers `vign_camB_night` lantern2 reads YES at 32 codes with
`lightVsFloorPx=1..vs..0` (verdict 286 against 283: the control's largest
move is 0.04521 luma, 11.5 codes, so its 32-code count is zero; lantern2
has one pixel at 32). `pinset_night_4` lantern1 reads YES by two pixels
(317 against 315). Those are literally lights that reached a pixel, which is
the question asked, and they are thin. The per-light line shows the pair;
the done line does not. The next rung is a printer (section 12).

(b) It cannot see a BLANK PROBE FRAME under a good control. Section 6(d).
This is the larger of the two and it is the reason the new numerator is not
yet a number to report.

## 4. Rule 2, every number in the diff, classified

No measurement threshold was invented. The decision rides integer counts
at the six pre-existing edges. `lightFloorCodeEdges=1/2/4/8/16/32` (header
754) is a label: the edges are `DeltaCodeEdge`'s table at 364 and every run
47 light line already prints `deltaCodeEdges=1/2/4/8/16/32` (verdict 275 to
322, 48 of 48 lines). Verified as the builder said.

The caps, each named with what it holds and whether it can bite:

- `LightDeltaLine` `Body[1400]`: bounded numbers plus the note; announces
  `lightLineCut=yes/at-1400-chars` (603 to 606). Sized against run 47's
  longest light line, which the header states as 704 characters.
- `LightFloorLine` `Head[320]` and `Buf[1100]`: the shot id rides the head,
  the light id rides the body as a `std::string` so that the body's cap is
  the only one; both announce (769 to 770) and BOTH announcers are planted
  and fire (test 677 to 687). This is the pattern done right.
- `LightProbeDoneLine` `Buf[1500]`: announces (867 to 870).
- `LightPinSegment` `Buf[420]`: the word is from a fixed vocabulary; the
  header says 420 was read off `-Wformat-truncation`, which is a printed
  series of a kind.
- `LightFloorSegment` `Buf[420]`: fixed strings and two integers; cannot
  bite; no announcer needed.
- `Reach[96]`, `N[48]`, `T[160]`, `Read[64]`: bounded numbers; cannot bite.
- `AtWorst[40]` (812, 831) carries a mean and a LIGHT ID, and
  `WorstBuf[300]` (838 to 841) carries a SHOT ID, both through `snprintf`
  with no `Needed` check, and both are then passed into the done line's
  buffer as a string, so the done line's announcer CANNOT fire for them.
  This is the fault the builder's own comment at 726 to 730 names and
  avoids in `LightFloorLine`, applied at one site and not the other.
  Today's ids are short (the longest light id in run 47 is
  `east_parade_interior5`, 21 characters, and the mean and slash add nine;
  40 holds it) so it cannot bite on the live spec, and a cap that cannot
  announce is a comment. Condition C5.

THE SERIES THE CAPS STAND ON was printed by the test (the line beginning
`atRealFrameWidth:` with `deltaLineChars`, `floorLineChars`,
`doneLineChars`, `floorSegChars`, `pinSegChars` and `assembledChars`, test
654 to 659) and I have not seen its values: no shell. Rule 2 is satisfied by
the mechanism, and the record needs the numbers: the resident quotes that
one printed line in the commit message (section 13).

## 5. The reverted accounted key: a queue item, and the first prediction

`lightFloorLightsAccounted=<sum>/<probed>` was half-applied, left the tree
red, and was reverted (the `reset` at 03:18:51Z). The builder traced the
paths and found no live hole; I traced them too, from the code: `GProbed`
increments at 3331 in the one branch where `LightFloorAddLight` is called at
3332, NO-FILE, UNDECODABLE and NOT-COMPARABLE return at 3299, 3308 and
3314 before either, and every light added lands in the `GFloor` that
`StartLightProbe` reset at 3345 and that `AfterFrame` pushes exactly once at
3402 (the NO-REFERENCE branch pushes at 3357 and returns before any light
is probed). So today U + N = P holds by construction, where U is the
denominator of `lightsAboveFloor`, N the numerator of `lightsInNoReadShots`
and P the numerator of `lightsProbed`. That is an argument, as the builder
said, and it becomes an instrument two ways: the first carrying run PRINTS
all three and a reader checks the identity (prediction P1), and queue item B
(section 10) makes the line check itself. Not a block.

WHAT THE TRACE ALSO FOUND. The test's own Mixed fixture violates the
identity: the `LightProbeDoneLine` call at 573 passes Probed = 6 over floors
holding 2 + 2 + 1 = 5 lights, and the checks at 583 to 586 assert
`lightsInNoReadShots=3/6` on it. With one budget skip the fixture's own
arithmetic gives Probed = 5 and Eligible = 6. The suite is green because
nothing checks the identity, which is precisely the fault the reverted key
would have caught, in the fixture that claims run 47's shape. Condition C4.
And NOT-COMPARABLE lights are counted on no done-line key at all (they are
eligible, photographed, decoded and dropped at 3314), so the gap between
`lightsProbed`'s numerator and denominator has an unnamed component; queue B.

## 6. What the brief did not carry

(a) TWO PRINT BRANCHES SHIP UNRUN. `LightFloorLine`'s NO-CONTROL branch
(717 to 725, printing `lightsReadThisShot=nothing-measured/N` and the
`lightFloorCtrl=nothing-measured` word) and `LightFloorSegment`'s two
nothing-measured words (671 to 679) have no fixture: 0 hits for any of
their strings in 1 test file examined. Both are reachable in the live rig
today: a control whose probe frame never arrives (NO-FILE at 3295) leaves
`bHaveControl` false with the lights still probed, and a light whose frame
fails to decode under a good control takes the second. The header's own
preamble (lines 3 to 10) exists because "an unrun formatter printing a
plausible string is the silent-instrument failure"; the batch added two
such formatters. Rule 5b: both outcomes watched. Condition C3.

(b) TWO WRONG WORDS ON REACHABLE LINES. First, the done line folds a
NO-CONTROL shot into `lightFloorShotsNoRead` (the `else` at 806 takes every
non-usable floor) while its stat token says NO-READ means the control
swamped the lights, which is false for a shot that had no control; the
per-shot line distinguishes the two facts and the run line erases the
distinction. Second, `EmitLightLine` for a NO-REFERENCE shot (3351) passes
Seq = -1, so `LightFloorSegment` prints `lightAboveFloor=IS-THE-FLOOR` on a
control line whose `lightDelta=NOTHING-MEASURED`: a control that never
measured is not the floor. Both in condition C3.

(c) THE HEADER'S ARITHMETIC IS REFUTED BY THE VERDICT. Header 782 to 783
says "Applied to run 47's committed numbers that is at most 9 of 21 where
the line said 30 of 42", and the brief says "5/14 certain and at most 9/21".
Applying the rule to lines 275 to 322, with the control's `deltaMaxRise`
and `deltaMaxDrop` bounding its move histogram where the old verdict does
not print it:

    shot             verdict   control floor           certain YES  uncertain  certain NO
    vign_camA_night  NO-READ   Moved = Rose, darker 0  0            0          7 (4 ties, 3 below)
    vign_camB_night  USABLE    max move 11.5 codes     1 lantern2   3          3
                               so Moved[16],[32] = 0   1..vs..0 @32
    pinset_night_1   USABLE    Moved = Rose, darker 0  2 epi0, epi2 0          5
                                                       467763..vs..204178 @32
    pinset_night_2   NO-READ   all 921600 darker,      0            0          7
                               mean -0.37873
    pinset_night_3   NO-READ   94 at edge 1, max       0            0          7
                               move 1.0 code
    pinset_night_4   USABLE    max move 26.9 codes     3 lantern1   3          1
                               so Moved[32] = 0        2..vs..0 @32;
                                                       lantern2, epi0
                                                       289587..vs..0 @32

Usable 3 of 6, NO-READ 3 of 6, `lightsAboveFloor` 6 of 21 certain and at
most 12 of 21, `lightsInNoReadShots` 21 of 42. The pinset_2 "certain" rests
on this: for lantern3's 56 to beat the control's edge-1 count, 921545 pixels
would have to have dropped by under one code, and then the frame's mean drop
could not exceed about one code (0.004 luma) against the printed 0.37873.
pinset_3's rests on the control's max move of exactly 1.0 code, so its
histogram above edge 1 is zero and every light's is too. The "uncertain"
cells are lights whose deciding edge is one where the control's darker
pixels could add to the move count by an amount the old verdict does not
print. Condition C2 corrects the comment to this table; the number gates
nothing, and a wrong number in a comment is a number the next session will
quote.

(d) FOUR OF THE SIX CERTAIN READS ON RUN 47'S NUMBERS ARE BLANK FRAMES.
`pinset_night_1` epi0 and epi2 (296, 297) print identical histograms with
`meanOffFull=0.00152`; `pinset_night_4` lantern2 and epi0 (318, 320) print
identical histograms with `meanOffFull=0.00151` and `0.00152`. Queue 325
names 0.0015 as the mean of its BLANK shots, and two of this run's
references carry it too (`meanOnFull=0.00151` at 299, `0.00152` at 307).
A probe frame that came back blank differences against the reference as
the whole reference, which is the largest surplus any light can show, and
the new rule counts it as YES at 32 codes with a six-figure margin. The
control floor catches a blank CONTROL (camA is that case, and reads NO-READ
correctly) and cannot catch a blank LIGHT frame under a good control. So on
run 47's numbers the new key would print six reads of which four are the
blank-frame fault and two are one and two pixels. This is outside 326's
acceptance, it needs a different mechanism (the shot line's own structural
`Blank` rule applied to the probe frame, which `FrameStats::Measure` already
computes), and it is the largest remaining false-green path in this
instrument. Queue item A, ordered directly behind the carrying run, ahead of
319, with the prediction that exposes it (P7). NOT a condition on 326: the
two are separable instruments with separate accepting and rejecting cases,
and bundling the second into a held batch is how a planted case gets
skipped.

## 7. The conditions, dictated, and the landing rule

One builder pass over the two g++-compiled files and one comment line.
Every dictated string sits on its own indented line, unbroken; the resident
hand-applies none of it beyond the one item marked so.

C1. RENAME. Header 845, the run key:

    lightsAboveFloor=%s

Header 853, the stat key and its whole token, one line:

    lightsAboveFloorStat=whole-run/count-of-lights-that-beat-their-OWN-shots-control-at-some-code-edge/denominator-is-lights-probed-in-shots-with-a-usable-floor-and-lightsInNoReadShots-and-lightsInNoControlShots-are-the-rest-of-lightsProbed/RENAMED-BY-QUEUE-326-from-lightsReachedFrame-which-counted-one-pixel-rising-by-one-code-value-through-run-47-and-is-not-comparable

Header 778 to 784 becomes the history note: which key it replaces, why, and
the table's numbers from C2. Test 486, 564, 567 and 583 take the new name.
New checks: the old key absent on RG, L, M and R47D, that is

    lightsReachedFrame=

found nowhere on any of those four lines. The .cpp comment string at 2591
names `lightsAboveFloor` (one line; the resident may apply this one).

C2. THE COMMENT'S ARITHMETIC. Header 782 to 783, and the same claim wherever
the header repeats it (grep `9 of 21`), becomes: on run 47's committed
numbers, three of six shots usable, six of twenty-one certain and at most
twelve of twenty-one, twenty-one of forty-two lights in NO-READ shots, and
four of the six certain reads are the blank probe frames queue item A
refuses. The sentence "at most 9 of 21" does not survive.

C3. THE UNRUN BRANCHES AND THE TWO WORDS.

(i) Plant a `LightFloor` with no control holding one comparable light and
one non-comparable light, and assert on its floor line:

    lightFloorVerdict=NO-CONTROL
    lightsReadThisShot=nothing-measured/2
    lightFloorCtrl=nothing-measured/no-comparable-control-frame-for-this-shot

and that every value after `shot=` is space-free.

(ii) `LightFloorSegment` on that floor, for its comparable light, prints

    lightAboveFloor=nothing-measured/this-shot-has-no-comparable-control

and on the accepting floor F, for a non-comparable delta, prints

    lightAboveFloor=nothing-measured/this-light-has-no-comparable-delta

both asserted.

(iii) `LightFloorSegment` with `bIsControl` true and `D.Comparable` false
prints, instead of IS-THE-FLOOR,

    lightAboveFloor=nothing-measured/the-control-did-not-measure-so-this-shot-has-no-floor lightAboveFloorEdge=nothing-measured lightVsFloorPx=nothing-measured

asserted.

(iv) The done line gets a third shot count and a third light count. The
tally loop at 802 to 811 splits non-usable floors by `bHaveControl`: with
a control, NO-READ; without, NO-CONTROL. The line prints

    lightFloorShotsUsable=a/n lightFloorShotsNoRead=b/n lightFloorShotsNoControl=c/n
    lightsInNoReadShots=N/P lightsInNoControlShots=K/P

and the `lightFloorShotStat` token's sentence about NO-READ stays as it is,
because NO-CONTROL is no longer inside it. The done line over the
NO-CONTROL floor alone, called with Probed = 2, asserts

    lightFloorShotsNoControl=1/1
    lightsInNoControlShots=2/2

(v) When `Floors` is non-empty and no shot is usable, `lightsAboveFloor`
never prints `0/0`; it prints

    lightsAboveFloor=nothing-measured/no-usable-floor-in-any-of-<n>-shots

with n the floor count, and the done line over the rejecting floor N alone
asserts it.

C4. THE MIXED FIXTURE. Test 573: the call's first two arguments become
Probed = 5 and Eligible = 6. Test 584 asserts

    lightsInNoReadShots=3/5

and the same fixture adds

    lightsProbed=5/6
    lightsAboveFloor=1/2

so the three numbers whose identity section 5 relies on are all asserted on
one fixture that satisfies it.

C5. THE SILENT PRE-CAPS. `LightProbeDoneLine` builds the worst-shot segment
as a `std::string` the way `LightFloorLine` builds `Best` (731 to 739): the
shot id and the light id concatenated, only the two means through a bounded
`snprintf`, so the done line's single 1500-character announcer is the one
that fires. Plant it: a worst floor whose `ShotId` is 900 characters asserts

    lightProbeDoneLineCut=yes/at-1500-chars

`LightDeltaLine`'s `Head[420]` is the same pattern's remaining site and goes
to queue B, since I cannot tell from the tree whether 326 wrote it.

THE LANDING RULE. This ruling covers the batch as amended by C1 to C5 and
nothing else. The resident commits when: the four g++ binaries are green
and the check count is printed; the `atRealFrameWidth:` line is quoted in
the commit message; a grep for `lightsReachedFrame` under `ue-probe/`
returns only the history note in the header. No second director is owed for
these amendments; a change that alters a conclusion here (a rule other than
strict integer surplus, a floor other than moves, a name other than the one
dictated) is a new batch and owes one. If any g++ check that was green at
3416 goes red under the amendments, the amendment is wrong and not the
check: hold and report, never loosen.

## 8. The scope question: no carve-out, and why that is a ruling

The tension is real: `FrameStats.h` and its test are pure instrument, D45
says a tool that measures the game gets a test and no review, and the gate
fired anyway because the prefix holds the Core port too. Ruled: the scope
stays as it is, for three reasons, one of them measured on this batch.

First, the gate's own text at `verify.py` 3666 to 3672 already refused the
tests carve-out with a D41 reason: `ue-probe/tests/` holds the Core's
planted rejecting cases and the perception golden's runner, and "a loosened
Core test is undone by re-deriving a golden, which is D41's structural side
exactly". A path carve-out of the tests directory would put the Core's
rejecting cases on the ungated side. The other two files do both jobs by
design: `Public/` holds formatters AND rules the rig acts on (the wetness
choice, the control-quad visibility rule), and `VignetteShot.cpp` holds the
probe walk AND `ApplyCondition`. No path under `ue-probe/` today carries the
D45 distinction, so the gate cannot read it by path, and it must not read it
by judgement, because it is mechanical by design.

Second, the measurement. D45's premise is that a fault in a checker "shows
up the next time somebody reads what it printed". Of the five findings in
sections 5 and 6, four would not have: an untested branch prints a
plausible string, a wrong number in a comment is never printed, a cap that
cannot announce never fires on today's ids, and a fixture's mismatch lives
in the test. Five findings per 769 lines, none visible from a verdict, is
the reading that says a review under this prefix is still earning its
spawn. Revisit when two consecutive reviews of pure-instrument batches under
`ue-probe/` find nothing; that is a series, and the bound moves on it, not
on one batch's inconvenience.

Third, rule 2 applies to the gate as much as to any bound: I will not move
the scope in the ruling the scope fired on. The design of a future carve-out
is named so it is not re-invented: make the PATH carry the distinction (an
instrument subtree beside a Core subtree under `ue-probe/tests/`, and the
formatters' headers likewise), so the classifier keeps reading paths and
never reads judgement. That is queue item C, research first: print the
per-directory line series over the last 200 landed commits under
`ue-probe/` before anyone proposes the split. It would not have changed
this batch: removing the test's 288 lines leaves 481, still over the bound.

## 9. Predictions for the first carrying run, written before it exists

The run is the one the wake names: it carries 326 and the pinset staging
fix, and its verdict has a different sha. Each prediction is refutable from
the committed file by grep; a refutation is a finding about the walk, not
about the rule.

P1. On the done line, reading R/U from `lightsAboveFloor` (U = 0 when it
prints the C3(v) words), N/P from `lightsInNoReadShots`, K/P from
`lightsInNoControlShots` and P/E from `lightsProbed`: U + N + K = P and R
is at most U. And with a/n, b/n, c/n from `lightFloorShotsUsable`,
`lightFloorShotsNoRead` and `lightFloorShotsNoControl`: a + b + c = n, and n
equals the number of `lightfloor` lines in the file. If any of these fails,
a floor was pushed twice or not at all and section 5's argument was wrong.

P2. Every `lightfloor` line's `lightsReadThisShot=r/n` has n equal to the
count of `light` lines for that shot id with `lightStatus=MEASURED` and a
kind other than control, because `LightFloorAddLight` is called only in
that branch (3331 to 3332).

P3. On every MEASURED light line, `deltaPixelsMovedAtLeast` is at or above
`deltaPixelsRoseAtLeast` at each of the six positions (a rise is a move,
header 403 to 412), and the control line of every probed shot prints
`lightAboveFloor=IS-THE-FLOOR` when it measured and the C3(iii) words when
it did not.

P4. Every light line's `lightExposurePin` word and `lightExposurePinRead`
pair equal its shot line's `shotExposurePin` word and `shotExposurePinRead`
pair (verdict line 189 shows the shot-side names), because `GShotPin` is
written only inside `PlaceCamera` (2024, 2165), which only `ApplyShot` calls
(4594), and a probe pass cycles Warm, Timed, Ask, WaitFile without
re-entering `ApplyShot` (3388 to 3396). A mismatch means the pin was
rewritten mid-pass, which would be a finding of its own.

P5. None of `lightLineCut`, `lightFloorLineCut` or `lightProbeDoneLineCut`
appears anywhere in the file: the buffers were sized against run 47's
longest lines and the run adds no id longer than run 47's.

P6. Shape, conditional on the run's controls resembling run 47's (which run
46 against 47 shows they need not): about half the probed shots print
`lightFloorVerdict=NO-READ` with the swamping control's own numbers on the
line, and `lightsAboveFloor` is far below `lightsProbed`. The number the
Producer may NOT report is R as "lights reaching the frame" until P7 is
read.

P7. THE ONE THAT DECIDES QUEUE ITEM A'S PRIORITY. If any two MEASURED light
lines within one shot carry identical `deltaPixelsRoseAtLeast` sextuples,
or any light line's `meanOffFull` sits within 0.0002 of 0.0015 while its
shot's reference `meanOnFull` is above 0.1, those lines are blank probe
frames and every YES among them is a false read; count them and put the
count beside R in the reading. If the staging fix has cured the blank
frames, this count is zero over the light lines examined and item A drops
in priority but not off the queue, because the fault has returned twice.

P8. The thinnest YES in the file (smallest `lightVsFloorPx` surplus among
`lightAboveFloor=YES` lines) is a small number of pixels at 32 codes, as
camB lantern2 and pinset_4 lantern1 are on run 47's numbers. That is the
reading queue item B's printer exists to put on the done line.

## 10. Queue items filed by this ruling

The resident writes the cards; the essentials are here so the cards cannot
drift from the ruling. Order relative to the wake's chain: 326 amended,
the carrying run, then A, then 325's second half (A and 325 may be one
fault; A is still owed as an instrument), then 319, then 324, then the
dusk frame.

A. A BLANK PROBE FRAME IS NOT A LIGHT-OFF FRAME. Spec: the probe walk runs
`FrameStats::Measure` on every decoded probe frame, control included, and a
frame whose structural `Blank` is true (one colour bucket or no non-black
pixel, the shot line's own rule, no signature threshold) is never handed to
`MeasureLightDelta`; its light line prints `lightStatus=BLANK-PROBE-FRAME`
with the frame's `shotMeanLuma`, `shotDistinctBuckets` and
`shotNonBlackPixels` keys as `PixelLine` prints them; a blank CONTROL makes
the shot NO-CONTROL with the word `blank-control-frame` on its floor line;
the done line prints `lightProbesBlank=k/<frames decoded>`. Evidence:
verdict 296, 297, 318, 320 (four YES reads under the new rule at
`meanOffFull` 0.00151 to 0.00152 with pairwise identical histograms) and
275 to 282 (a control at 0.00075 with four lights at the same value).
Acceptance, both outcomes: a planted single-bucket Off buffer is refused and
counted; a planted two-bucket near-black Off buffer is measured and not
refused. Under D45 a test, no review, and no ruling record; it is over 100
lines under `ue-probe/` only if the builder makes it so.

B. THE DONE LINE ACCOUNTS FOR ITSELF AND NAMES ITS THINNEST READ. Spec:
`lightsAccounted=U+N+K/P` computed on the line with the word `DISAGREE`
when the sum and P differ; `lightProbesNotComparable=k` for the branch at
3314 that no key counts today; `LightDeltaLine`'s `Head[420]` restructured
as C5 restructures the worst segment, or its ids carried as `std::string`;
`lightFloorThinnestRead=<light>/<shot>/Rpx..vs..Cpx/at<E>codes` over every
YES in the run, a printer and not a bound; and the worst-floor selection at
808 to 810, which picks by the control's MEAN while the rule decides by
MOVED counts, either picks by `MovedAtLeast[0]` or prints both with the
statistic named. Evidence: sections 4, 5 and 3(a).

C. THE PATH CARRIES THE D45 DISTINCTION, OR THE GATE KEEPS FIRING ON
INSTRUMENT WORK. Research first: print, per landed commit over the last
200, the `ue-probe/` lines split by `tests/`, `Public/`, `Private/` and by
whether the file is in the Core port's list; propose a directory split from
that series. No scope change without the series and without a director,
because it is a change to the commit gate.

## 11. Corrections to the brief

- "5/14 certain and at most 9/21": my count off the verdict is 6/21 certain
  and at most 12/21, three of six shots usable, per section 6(c). The
  difference is camB's lantern2 (certain from the control's printed
  `deltaMaxDrop`, which bounds its 32-code count at zero) and the three
  uncertain lights at pinset_4 that the brief treated as decided. The
  header comment carries the brief's number and C2 corrects it.
- "Both watched outcomes are RUN with the accepting case first": true of
  the floor rule (test 427 to 533, accepting first) and of the third
  planted case; not true of the NO-CONTROL and no-comparable print
  branches, which have no case at all (section 6(a)).
- "The diff shape obeys instruments.md": except at `AtWorst[40]` and
  `WorstBuf[300]` (section 4).
- "four of seven lights at that shot produced a histogram indistinguishable
  from a probe that changed nothing", "lightsReachedFrame=30/42 was decided
  by one pixel rising by one code value", the pinset_night_2 claim, and the
  `lightFloorCodeEdges` label: all verified from the printed lines and the
  code, sections 1 and 4.
- "all four g++ binaries green at 3416 checks": not verified here, no
  shell; taken as the caller's printed number and named as such above.

## 12. The quality ladder at close

The rule: best available for what the item asked. A per-shot control floor
on integer counts at printed edges, no epsilon, tie is not a read, NO-READ
with both numbers, the exposure pin on the light line, and the run line
split by usable floor. The rung above it is not a stricter rule; it is two
printers and one refusal: the thinnest read on the done line (B), the
blank probe frame refused by the shot line's own structural rule (A), and
the accounting identity checked on the line (B). After those three land,
the next blank rung is whether a control of ONE repeat frame is enough of a
floor, which is a research task: a second control frame would give the
floor a spread and the read a margin, at the price of one more screenshot
round trip per shot against a 240-second budget the pass already announces.

The instrument's process: a director without a diff found five things a
green 3416-check suite did not, by reading the verdict against the rule and
the test against its own fixtures. The suite tests what it was told to
plant; the review asks what was not planted. That is the measurement
behind section 8.

## 13. For the commit message, the log and the close-out

Commit message, after the amendments: "Queue 326, the light probe's control
is read: `LightReadEdge` decides a read as this light's risen pixels strictly
exceeding this shot's own control's moved pixels at the same pre-existing
code edge, integer counts, no epsilon, tie is not a read; `MovedAtLeast`
joins the light line as the floor's histogram because pinset_night_2's
control has an empty rise histogram and 921600 darker pixels; one
`lightfloor` line per probed shot with FLOOR-USABLE, NO-READ or NO-CONTROL
and both numbers; the run key is RENAMED `lightsAboveFloor=R/U` by the
ruling of 2026-09-16 03:27Z because its rule and denominator changed, old
name asserted absent, with `lightsInNoReadShots` and
`lightsInNoControlShots` holding the rest of `lightsProbed`;
`lightExposurePin` and `lightExposurePinRead` ride every light line from the
shot's own `GShotPin`. Applied to run 47's committed numbers, three of six
shots usable, six of twenty-one certain and at most twelve, where the line
said 30 of 42; four of the six are blank probe frames and queue A refuses
them next. Two unrun branches planted, one fixture's tallies made
consistent, two silent caps replaced by the one announcer, the header's
arithmetic corrected. NOTHING RENDERED. g++ <count as printed>;
`atRealFrameWidth:` <line as printed>. Queues A, B, C filed by the ruling."
Then the footer from `ledger/.verify-footer`, never from the scrollback.

Rulings-log entry, appended by the resident under the 2026-09-15 entries in
the log's own shape:

    - **2026-09-16** queue 326 lands amended (03:27Z): the control floor is
      read per shot on integer counts at the same edge, strict, no epsilon;
      moves floor rises; the run key is renamed lightsAboveFloor because its
      rule and denominator changed and the stat token is not what a grep
      returns; two unrun print branches, a NO-CONTROL fold, a wrong count in
      the header, a fixture whose tallies disagree and two silent caps are
      conditions; the reverted accounted key is queue B; four of run 47's
      six certain reads are blank probe frames, queue A; the ue-probe gate
      stays whole and the carve-out is queue C, research first; predictions
      written before the run
      `game-design/decision-2026-09-16-ruling-326-lands-amended-the-floor-is-read-and-the-key-that-changed-meaning-changes-name.md`

Queue 326 close-out line, for the resident: DONE on the landing date under
the ruling of 2026-09-16 03:27Z, amended by its C1 to C5; the acceptance's
`lightsReachedFrame` is `lightsAboveFloor` by that ruling and the rule is as
accepted; what the acceptance did not ask, a blank light frame under a good
control, is queue A; and the first carrying run is read against the ruling's
section 9 before any number from it is reported.

<!--RULING spawn=2026-09-16T03:27:21Z-->
