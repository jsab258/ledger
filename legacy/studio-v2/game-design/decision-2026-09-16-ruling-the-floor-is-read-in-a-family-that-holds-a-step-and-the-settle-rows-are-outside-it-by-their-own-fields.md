# Ruling, 2026-09-16 (08:04Z): the floor is read in a family that holds a step, and the six settle rows are outside it by their own fields

STATUS: LOG, 2026-09-16. NOT CURRENT once the amended emitter has landed and
the first run whose commit CONTAINS it has been read against section 10; from
then the verdict file, the g++ suite and the queue items in section 9 are the
reading copies and this is the record of what was ruled and why.

Director ruling on the six failing checks of `ue-probe/tests/vignette-spec-test.cpp`
(6 of 555, the only red `python3 ledger/verify.py` reports), raised by the six
`settle_night_*` rows queue 334 landed in `production/specs/vignette-scene.json`
and predicted by `production/queue/340-the-null-group-is-chosen-by-size-and-would-floor-the-grid-on-night-frames.md`.

Author: tier-1 director, stamp at the foot naming row 679 of
`.claude/agent-log.tsv` (`2026-09-16T08:04:42Z` TAB `studio-director` TAB
`fable` TAB `default` TAB `aed92d2cc1a3fb4db`), the newest row in the log and
the last line of the file. The reference commit is `542804a1`, `.git/logs/HEAD`
line 133, epoch 1789542888, which is 2026-09-16T07:14:48Z ("The ruled batch is
dispatched, and the wake carries the corrected number"); row 679 is fifty
minutes newer. Row 674 (`2026-09-16T07:30:50Z`, studio-director) is already
claimed by the caught-claim ruling and is not claimed here. No code was written
by this director and this director has no shell: the tree was READ at the line
numbers in section 0, and every number below is copied from a printed line
that is named beside it.

VERDICT IN ONE LINE: the test is right and is upheld unchanged; the emitter's
rule "largest group" was a proxy for "the reference cell's family" that
coincided with it for six days and stopped coinciding on the sixth row, so the
emitter changes, not the invariant. The floor is read off the largest
identical-input group WHOSE NO-SKY FAMILY HOLDS A SKY-ONLY PAIR, because a
spread with no step in its own family has nothing to be read against, which
is a rule the emitter already states for the run as a whole. The six settle
rows and the four pinset rows are outside that floor by their own fields, with
no key declaring it. The line prints what size alone would have chosen, so the
floor can never move without the move being on the line. One check, the null
cell being literally the last shot, is restated to the thing it protects,
because the 06:35Z ruling placed the six rows after it for a measured reason.

## 0. What was opened

`ue-probe/Source/LedgerProbe/Public/VignetteSpec.h` 288 (`struct Shot`), 467 to
536 (the camera and shot parsers), 2600 to 2907 whole (`AppliedFieldsUnreal`
2624, `FrameSample` 2651, `SampleKey` 2673, `NullSeriesLine` 2696 to 2907, the
group tally 2736 to 2766, the per-statistic spread and step loop 2817 to 2894,
the done segment 2895 to 2905). `ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp`
766 to 770 (which file the rig loads), 2770 to 2801 (`ShouldProbeShot` 2790),
3064 to 3065 by grep (where the samples are filled).
`ue-probe/tests/vignette-spec-test.cpp` 521 to 535 (the null-cell-is-last
check), 4709 to 5060 (the null series block: the fixture, the independent
tally, the derived anchor 4794 to 4922, the wet ladder count 4987 to 5014, the
planted loud case 5042 onward). `production/specs/vignette-scene.json` 898 to
911 (`wet_night`), 928 to 1106 (the four sun-3 grid cells and
`grid_null_repeat`), 1363 to 1376 (`pin_setter_night`), 1400 to 1437 (the shot
list tail and the notes). `production/specs/vignette-pieces.json` 60 to 63 and
99 to 108 by grep. `production/d1-probe/ue-vignette-verdict.txt` line 1 (run 48,
commit `4e257ee`), 197, 219, 222, 225, 228, 231 (shot lines), 331 whole (the
null series line). `ledger/Assets/Scripts/Core/StreetVignette.cs` 182 to 185
and 1896, `StreetVignettePieces.cs` 514 to 518 by grep. `ledger/verify.py` 7507
to 7544 (the stamp rule). Queue 334 and 340 whole. The 06:35Z record 396 to 425
and 688 to 711. The rulings log 330 to 382. `.claude/agent-log.tsv` 661 to 680.
`.git/logs/HEAD` 118 to 133.

## 1. The fault, stated precisely

The test at 4794 to 4898 derives the null group from ONE named id, the grid's
reference cell `grid_sky070_sun003`, field by field at its own camera, calling
no shared function, and asserts the discovered group equals it exactly. That
IS the invariant: the noise floor is the spread over the reference cell's own
identical-input family, and the four checks after it say why (the judged hook
frame is in it, the null cell is last in it, the reference and null cells are
both in it, the 0.6 wet row stays in it).

The emitter at 2713 to 2755 chooses the largest group by a strict count. That
was never the invariant; it was a proxy that picked the same seven frames on
every run since the grid ruling because nothing else at `cam_hook` repeated
more than four times. Queue 334 added six identical rows under `wet_night`,
which matches `pin_setter_night` in all eleven fields the fingerprint reads
(898 to 909 against 1364 to 1374: sun off, 0.0, sky 0.35, kloppenheim_04_2k,
wet 0.90, fog 0.0220, cap 0.450, pin 0.000, lanterns on, practicals on). Ten
beats seven. The test went red on exactly the assertion built to catch this,
so the instrument worked; what failed is the emitter's proxy, and the repair
belongs there.

What the move would have cost, off run 48's printed lines and not estimated:
the day group's `nullSpreadMeanLuma=0.0001` (line 331: max
`vign_grid_sky070_sun003` 0.4228, min `vign_hook_day` 0.4227) against
`skyStepSmallestMeanLuma=0.0193` (between `vign_fog010_sky050` and
`vign_fog010_sky035`, 41 of 41 sky-only pairs), a margin of 193x. The night
rows measured 0.1694, 0.1796, 0.1694 on `pinset_night_2`, `_3`, `_4` (lines
222, 225, 228) with `pinset_night_1` BLANK at 0.0015 (line 219), a spread of
0.0102 over three frames, each with a different pinned predecessor, against
the same 0.0193: 1.9x. A floor two bad frames from `NO-READ`, quoted against a
day grid it does not belong to, is the largest number in the comparison
wearing the name of the smallest, which is the fault `SampleKey`'s camera
half and queue 235's pin term already exist to stop.

## 2. The three shapes, weighed

Shape 1, a per-shot key declaring the settle rows out of the grouping.
Restores the invariant by managing the emitter's input rather than its rule.
It is not the cheapest, and the brief's reason for thinking so is not in the
tree: the `light_probe` boolean it would mirror has no reader on the side
that renders (section 8). To make the mirror real it touches the scene spec
(ten rows, since the pinset rows are night too and would otherwise be the
next silent candidate), the Core reader and writer (`StreetVignette.cs` 1896,
`StreetVignettePieces.cs` 516) and their tests, a regenerated
`vignette-pieces.json`, `struct Shot`, the UE parser, the sample fill at
`VignetteShot.cpp` 3064 and the emitter. Six files across two layers and a
regeneration, and what it buys is a list of ids kept by hand in the spec,
which is the thing the discovery design at 4713 to 4716 was built to avoid.
And it leaves the emitter's rule wrong: the next family of repeated rows
anyone adds without the key is the same fault again.

Shape 2, the group choice stops being size alone. The brief reads this as
overturning the test and rewriting its six assertions. It is the opposite:
the test's derived anchor already says which group the floor is, so the
emitter catching up to it leaves five of the six assertions untouched and
green, and the sixth (section 4) is restated for a reason that has nothing
to do with grouping. The criterion is the part that had no name, and the
emitter already carries it for the run as a whole at 2874 to 2882: a spread
with no sky step is `nothing-measured`, because there is nothing to read it
against. Applied per group: a group whose own no-sky family holds no
sky-only pair has no step of its own and cannot be the floor. Every
FrameSample already carries `AppliedNoSky` (2656), so this needs no new
field, no spec change, no Core change, no regeneration and no line in the
untested layer. Two files, both in the g++-tested layer. Checked on the live
file: the reference cell's no-sky family (958 to 969, cap 0.100) is not the
four sun-3 grid cells, three of which still carry cap 0.450 (936, 996,
1071); its sky-only pairs are the fog010 rows at 0.35, 0.50 and 0.70, which
is exactly where run 48's smallest step came from (line 331), so the day
group qualifies. The night family has one sky value, 0.35, on both its
conditions, and holds no pair, so it does not.

Shape 3, print the runner-up beside the winner. Does not green the tree on
its own and rides along regardless (section 5), because "the floor moved and
nobody could see it move" is the fault underneath both of the others, and
the line is the only channel that reaches a reader.

RULED: shape 2 in the family form, with shape 3 riding along. Shape 1 is
refused as a hand-kept list that leaves the rule wrong. Nothing in the test's
six assertions is overturned.

## 3. What the builder changes, and what it does not

In `VignetteSpec.h`, `NullSeriesLine` only:

1. Before the group tally, tally FAMILIES: for each measured frame the family
   key is `SampleKey(S, false)`; a family HOLDS A STEP when at least two
   measured frames in it differ in `SkyIntensity`, which is the pair test the
   step loop already applies at 2849 to 2850, reused and not re-invented.
2. The kept group is the largest identical-input group (`SampleKey(S, true)`)
   whose family holds a step; the strict greater-than and the first-in-shot-
   order tie rule at 2750 to 2760 stay as they are, applied over the
   qualifying groups only. The tie counter counts qualifying groups and its
   denominator says so.
3. New whole-run keys, no spaces in values, each zero with its denominator:
   `nullSeriesFamilies=<k>/of=<m>/no-sky-families-holding-a-sky-only-pair/of-distinct-families-at-any-camera`;
   `nullSeriesOutsideStepFamilies=<n>/of=<measured>/measured-frames-whose-family-holds-no-sky-only-pair`
   with ids in shot order under the same cap as `nullSeriesIds`, the cap
   announcing itself;
   `nullSeriesBySizeAlone=<key>/n=<size>/spreadMeanLuma=<x>/SAME-AS-KEPT` or
   `/DIFFERS-FROM-KEPT`, the group the rule of 2713 would have kept, with its
   MeanLuma spread stated as max minus min over that group, and only MeanLuma,
   named as such.
4. When no group qualifies, `nullSeriesStatus=NO-FAMILY-HOLDS-A-STEP`, ids
   `none`, verdict `nothing-measured`, never `CLEAR`. When the kept group has
   fewer than two frames, `TOO-FEW-SAMPLES` as today.
5. The descriptor on `nullSeriesSamples` gains
   `/within-a-family-that-holds-a-sky-only-pair`. The key keeps its name: it
   counts the same thing, frames the floor was read off, and the rule that
   picked them is now printed in full beside it rather than implied. This is
   the 03:27Z naming rule honoured by making both rules visible on every
   line, not by renaming a count whose meaning did not change.
6. The comment at 2713 to 2716 is rewritten to the new rule and cites this
   record; the sky step itself (the smallest over ALL sky-only pairs) does not
   change, so the verdict is still spread-against-the-smallest-step-anywhere.

In `vignette-spec-test.cpp`, rule 5b both ways, accepting first:

- Accepting, the live file: the six existing assertions unchanged and green;
  `nullSeriesBySizeAlone` reads `DIFFERS-FROM-KEPT` with `n` equal to the
  independent tally's `Largest` (already computed at 4761 to 4779, which will
  now be ten and is not to be typed), and the kept group's size equal to the
  derived anchor's length; `nullSeriesFamilies` and
  `nullSeriesOutsideStepFamilies` printed with their denominators and the
  outside count equal to the number of shots at the reference camera whose
  condition's sun is off, counted from the conditions.
- Planted, the case the rule must refuse: the fixture with the reference
  family's sky-only siblings marked unmeasured, so the day family holds no
  step, and the assertion that the day group is NOT kept and the words say
  why; and the fixture with the six settle rows measured and the family rule
  disabled by construction (the by-size group), showing the ten-frame night
  key and its spread on the `BySizeAlone` key, so the guard is seen telling
  the two apart rather than assumed to.
- The ratchet toward the next rung: on the live file, the count of step-
  holding families whose sun is off is `0/of=<k>`, asserted, with the
  sentence naming section 9's item, so a night sky-only pair cannot enter
  the spec without the suite saying a per-family floor must land first.

What does NOT change: the scene spec, the pieces plan, Core, `struct Shot`,
the parser, `VignetteShot.cpp`, the derived anchor, the fixture's signal and
noise model. The change is above the 100-line `ue-probe/` bound and this
record covers it; one instrument-builder pass; a test, since it is a tool that
measures the game, and this ruling because it is entangled with 334.

## 4. The null cell's position: one check restated, the 06:35Z placement stands

The first of the six failures is not a grouping failure. The check at 534
asserts the last shot in the LIST is `grid_null_repeat`; the 06:35Z ruling
(section 4, 404 to 405) placed the six rows at the end of the list "so no
existing row's predecessor changes", and the two cannot both hold. The
placement is right and stays: moving the null cell after the six would give
it a night frame at auto exposure as its predecessor instead of the pinned
day frame it has had on every run it has been read on, and the first run
carrying the six is the run whose day floor is compared with run 48's.

The check's own comment says what it protects: "identical inputs at maximum
order separation". Six frames from another family sitting after the null
cell neither shorten its separation from its twin nor could lengthen it
without the change above. RESTATED: the null cell is the last shot at the
reference camera whose condition matches the reference cell in every field
but sky, that is, the last shot of its own family, checked field by field
the way the anchor is and calling no shared function. Tested both ways on a
synthetic list: a family row after the null cell fails it; an other-family
row after it passes. The sentence changes with the check. This is a precise
restatement of the invariant, not a bound moved to make red go away: every
case the old sentence caught for its stated purpose, the new one still
catches.

## 5. Shape 3 rides along

`nullSeriesBySizeAlone` is the runner-up print in the form that answers the
actual fault: not the second-largest group, but the group the OLD rule would
have kept, with its spread, and one word saying whether it is the kept group.
On run 48 it reads `SAME-AS-KEPT`; on the first run carrying the six it reads
`DIFFERS-FROM-KEPT` with the night key and its spread beside the day floor. A
reader comparing two runs sees the rule change on the line itself, which is
the instruments rule: one picture, one scale, never two memories.

## 6. Can an unstable night group silently become the floor?

Under this ruling, no, and here is the exact boundary. A night group cannot
be the floor at all while the night family holds no sky-only pair, and that
is true of the spec as it stands (both night conditions at sky 0.35), true at
run time regardless of which day frames blank, because qualification is a
property of the family and not of a count, and true without any row
declaring anything. If every sky-only sibling of the reference family blanked
in a run, the day group would stop qualifying and the line would say
`NO-FAMILY-HOLDS-A-STEP` and `nothing-measured`, voiding the grid loudly, not
inheriting a night floor quietly.

The boundary: the moment a night sky-only pair exists, the night family
qualifies and size chooses between families again. That is why section 3's
ratchet asserts, on the live file, that no step-holding family has the sun
off, naming the per-family floor as the item that must land first. Until it
lands, a night grid is refused by the suite, not by memory.

## 7. The settle_note, corrected

The note in `production/specs/vignette-scene.json` at 1431 was right as a
prediction and is wrong as a description the moment section 3 lands, since
its last sentence says the six rows make the night group the largest
identical-input group in the file without saying what that group now is. It
also states a fact about `light_probe` that the tree does not bear out
(section 8). Two dictated edits, the resident applies them as dictated text:

Replace the sentence beginning "light_probe is off on all six because" with:

    light_probe is off on all six because the probe toggles every lantern and
    every practical and photographs each half, which is both the cost these
    rows cannot afford and the one thing a held condition must not have done
    to it between frames. WRITTEN HERE AND NOT YET READ WHERE IT MATTERS, as
    of 2026-09-16: Core reads it (StreetVignette.cs 1896) and writes it into
    vignette-pieces.json as false (lines 103 to 108), and no reader in
    ue-probe/ consumes it: the shot parser at VignetteSpec.h 526 to 533 reads
    id, camera and condition only, and ShouldProbeShot at VignetteShot.cpp
    2790 reads the condition's lantern and practical flags, which are on for
    wet_night. Until the reader the 06:35Z ruling ordered in section 4 lands,
    a run carrying these rows probes all six, and by this note's own sentence
    the series it prints is not a settling series.

Replace the passage from "WHAT THESE ROWS ALSO DO" to the end of the note
with:

    WHAT THESE ROWS ALSO DID, AND WHY THEY ARE NOT THE FLOOR: they are six
    frames of identical applied input at one camera, and under the
    field-based fingerprint they join the four pinset_night rows into a night
    group of ten, larger than the day group of seven the noise floor had been
    read off. On 2026-09-16 that turned vignette-spec-test red on 6 of 555
    checks, because the test asserts the floor is the reference cell's own
    family and the emitter chose by size. RULED in
    game-design/decision-2026-09-16-ruling-the-floor-is-read-in-a-family-that-holds-a-step-and-the-settle-rows-are-outside-it-by-their-own-fields.md:
    the floor is read off the largest identical-input group whose no-sky
    family holds a sky-only pair, because a spread with no step in its own
    family has nothing to be read against; the night family has one sky
    value and holds no pair, so these rows and the pinset rows are outside
    the floor by their own fields, and no key declares it. The line prints
    what size alone would have chosen (nullSeriesBySizeAlone), so the
    difference is on every run's line. These six sit after the null cell in
    the list, and the null cell stays the last shot of its own family, which
    is the separation its value comes from. Their own spread is the settle
    series, a reading of whether the night condition settles, printed as its
    own done-line key and never a floor.

## 8. A finding beside the question, stated and not expanded

Rule 6. The per-shot `light_probe` boolean that the 06:35Z ruling ordered
"read by ShouldProbeShot beside the condition's flag" is written, carried into
the file the rig loads (`VignetteShot.cpp` 766 to 770 loads
`vignette-pieces.json`; its lines 103 to 108 carry `"light_probe":false` on the
six rows), and read by nothing in `ue-probe/`: a grep for the literal over
`ue-probe/` returns no file; `struct Shot` at `VignetteSpec.h` 288 has three
strings and no flag; the parser at 526 to 533 reads `id`, `camera`,
`condition`; `ShouldProbeShot` at `VignetteShot.cpp` 2790 to 2795 returns true
for any condition with lanterns or practicals on, and `wet_night` has both on.
The settle series' done-line key the same ruling ordered has no hit for
`settle` in `ue-probe/` outside `WalkProbe.cpp`'s unrelated constants.

Consequence, which is the 06:35Z ruling's own and not a new one: the carrying
run for 334 is not dispatched until `ShouldProbeShot` reads the flag, or the
six frames are probed and the series is void by the note's own sentence. That
reader is the 334 builder's remaining work under the existing ruling, it is
independent of section 3 and lands in the same or a separate pass at the
resident's choice. Not ruled further here.

## 9. Queue amendments, applied by the resident as dictated text

340, append to status:

    RULED 2026-09-16 (08:04Z ruling, section 3): the group choice stops being
    size alone. The floor is the largest identical-input group whose no-sky
    family holds a sky-only pair; the six settle rows and the four pinset rows
    are outside it by their own fields, no per-shot key. nullSeriesBySizeAlone
    prints what size alone would have kept, with its spread and SAME-AS-KEPT
    or DIFFERS-FROM-KEPT. The null-cell-is-last check is restated to the last
    shot of the reference cell's family (section 4); the 06:35Z placement of
    the six after it stands. The test's six assertions are upheld unchanged.
    One instrument-builder pass in VignetteSpec.h and vignette-spec-test.cpp,
    covered by that record's stamp. Acceptance is met when the suite is green
    on the live file and the planted cases print the words in section 3.

334, append to status:

    OPEN AT 08:04Z, rule 6: the light_probe boolean is written into
    vignette-pieces.json and read by nothing in ue-probe/ (VignetteSpec.h 288
    and 526 to 533, VignetteShot.cpp 2790 to 2795), and the settle done-line
    key is not in the tree. The rows are landed; the reader and the key are
    not. No carrying run until ShouldProbeShot reads the flag. The 08:04Z
    ruling section 8 has the evidence.

New item, filed by the resident under the next free number, line
`instrument (VignetteSpec.h NullSeriesLine)`: the floor is read PER FAMILY,
each step-holding family's largest group against that family's own smallest
step, so a night grid has a night floor and a day grid a day floor and size
never chooses between families. Acceptance: the line prints one floor per
step-holding family with its own verdict, the run verdict is the worst of
them, and the ratchet assertion of section 3 is retired in the same diff
because the thing it refuses becomes readable. Blocked on nothing; needed
BEFORE any night sky-only pair enters the spec. This is the next rung on
`production/quality-ladder.md` for the null series, and it is a research
task only in the sense that no run has yet printed two families.

## 10. What the first run carrying section 3 must print

Predictions written before the run exists, so a surprise is a surprise.
`nullSeriesSamples=7/of=49`, `nullSeriesIds` the same seven ids as run 48's
line 331 in the same order, `nullSeriesBySizeAlone` naming the
`cam.cam_hook/sun.off/...` key with `n=10` if all ten night frames measure and
`n=9` if `pinset_night_1` blanks again as it did on run 48, reading
`DIFFERS-FROM-KEPT` with a spread of the order of run 48's 0.0102 or larger
(the six consecutive frames are the series 334 exists to read and their
spread is not predicted here), `nullSeriesOutsideStepFamilies=10/of=<measured>`
or `9`, `nullSeriesFamilies` a count the builder's printer establishes on the
live file before any bound is read off it, and the day floor `CLEAR` at a
margin near 193x if the six rows have changed nothing about the day frames,
which is the comparison the 06:35Z placement was chosen to keep clean. A
day-floor margin that moves by more than the run-to-run noise of the pinned
day frames is the finding that would overturn the placement, and it is
readable only because the placement kept every day predecessor fixed.

## 11. Rulings-log line, appended by the resident to `ledger-v2/respec/decision-register/rulings-log.md`

    - **2026-09-16** the floor is read in a family that holds a step (08:04Z):
      the test's invariant is upheld and the emitter's size proxy is replaced
      by "largest group whose no-sky family holds a sky-only pair"; the settle
      and pinset rows are outside the floor by their own fields and no key
      declares it; nullSeriesBySizeAlone prints what size would have kept; the
      null-cell-is-last check is restated to the last of its family and the
      06:35Z placement stands; light_probe is found written and unread on the
      UE side, 334 stays open on it; per-family floors filed as the next rung
      `game-design/decision-2026-09-16-ruling-the-floor-is-read-in-a-family-that-holds-a-step-and-the-settle-rows-are-outside-it-by-their-own-fields.md`

<!--RULING spawn=2026-09-16T08:04:42Z-->
