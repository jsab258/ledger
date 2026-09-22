# Ruling, 2026-09-14: every sun-on condition carries the pin, the rung-only invariant is restated rather than deleted, and the step 1 render waits for it

STATUS: LOG, 2026-09-14. NOT CURRENT once the pin batch (queue 274) has landed
under this ruling and the first Unreal run on or after that commit has printed
the keys in section 9; from then the verdict file is the reading copy and this
is the record of what was decided and why.

Director ruling on one question, put by the resident on 2026-09-14 and blocking
step 1 of Jafar's visual-slice week: which conditions in
`production/specs/vignette-scene.json` may ask for an exposure pin. No code was
written by this director. Every number below was read this session off the file
it names, never off another record's restatement of it.

Author: tier-1 director, stamp at the foot naming row 581 of
`.claude/agent-log.tsv` (`2026-09-14T14:12:50Z` TAB `studio-director`, agentId
`a0d8dbdca848795e6`), the newest director row in the log at the time of writing;
line 582 is empty. The 13:39:10Z row on line 580 belongs to the leak ruling and
is not claimed here.

## 1. The ruling, in one sentence

Every sun-on condition carries the exposure pin and every sun-off condition
carries none, and the guard is restated from "only the ladder rungs may ask
for a pin" to "every pin value in the file is either a ladder rung's or the
one live value whose provenance the file names", because this rig exists to
compare one condition with another and a frame photographed under automatic
exposure cannot be compared with anything.

Position B, with the invariant dictated in section 6 and the tests named in
section 7. The night conditions stay at `0.000` by section 3 of
`game-design/decision-2026-09-10-ruling-the-exposure-ladder-and-the-sheet.md`,
which this ruling does not touch.

## 2. Premise check

Section 0 of CLAUDE.md: photoreal, wet, overcast, grimy Britain, judged by the
Meridian Test. Neither position touches the premise. What decides between
them is the owner's own sentence for step 1 of the week, D28 as dictated on
2026-09-14: "Fix the exposure fault so the same camera and conditions give the
same picture." Under position A the same camera and condition give the same
picture on four rungs of twenty seven conditions and on nothing Jafar looks at.
Under position B they give the same picture on every day condition, which is
every judged day frame and every cell of the grid. Only B is what he asked for.

## 3. What was measured, read off run 41 this session

`production/d1-probe/ue-vignette-verdict.txt`, line 1 naming `f6508b3`. Every
figure is whole-frame mean luma of a tonemapped 8-bit frame unless it says
otherwise, and each one names its line.

THE AUTO-EXPOSED RIG, WITH NO LEAK POSSIBLE. Lines 189 to 213 are the twenty
five shots photographed before any pin was asked for; every one reads
`shotExposurePin=AUTO shotExposurePinRead=0.0300/8.0000`, the engine's own
clamp pair, so the leak the 13:39 ruling found cannot have touched them. Six of
them are one identical-input group at `cam_hook` (line 319, `nullSeriesIds`,
all but the leaked null repeat):

    line 193  vign_hook_day            0.5800
    line 195  vign_grid_sky100_sun003  0.6057
    line 206  vign_fog_maxop0450       0.0765
    line 210  vign_wet_000             0.5741
    line 211  vign_wet_060             0.9591
    line 212  vign_wet_100             0.6057

Spread, max minus min over those six: 0.8826. The grid's smallest sky step on
the same run, line 319: `skyStepSmallestMeanLuma=0.0023`. Line 319's own
verdict: `nullSeriesVerdict=NO-READ/no-cell-may-be-quoted`. That is automatic
exposure at adaptation rate 10000 photographing one unchanged street six times
and returning pictures from 0.08 to 0.96, on rows the leak never reached. It is
the whole of the case against position A and it was on disk before the
question was asked.

THE PINNED RIG. Line 321, four rungs, each photographed once after a night
frame and once after a day frame, `ladderPinsPaired=4/of=4`:

    pin  0.0300   afterDay 0.9579  afterNight 0.9579  clipHi 206137 and 206406 of 921600
    pin  0.3000   afterDay 0.6590  afterNight 0.6591  clipHi 0/921600  clipLo 0/921600
    pin  3.0000   afterDay 0.1892  afterNight 0.1892
    pin 10.0000   afterDay 0.0610  afterNight 0.0610  clipLo 10524 and 10511 of 921600

Four of four pairs agree within 0.0001 across an intervening night frame, with
`pinHeld=2/of=2` on each. Rung 0.300 is the only one of the four with zero
clipped pixels at both ends of both halves. The pin is the only thing on this
rig that has ever produced two matching photographs of one condition.

THE LEAK, for completeness: line 323, `rigRepeatOf=vign_camA_day`, 0.6099
against 0.0518, the repeat carrying pin 10 from the last shot before it. Fixed
on `main` at 04e3cea4 under the 13:39 ruling (`.git/logs/HEAD` line 39; HEAD
is 6029fc0b, line 41, a record-only commit after it). That fix makes the leaked
rows honest; it does not make the six rows above agree with each other, and
nothing at HEAD does.

## 4. The options, with what each sacrifices

A. RUNGS ONLY, the invariant at `ue-probe/tests/vignette-spec-test.cpp` 3236,
reason at 3239: "a row pinned by accident would be photographed at an exposure
nobody chose." Keeps every judged frame and every grid cell under automatic
exposure. Sacrifice: no cross-condition number can be read from this rig, by
the run's own null verdict. Step 2 of the week (bring the sky down, measured
against the Hook sheet) is a comparison between conditions and could not be
measured. Queue 235's acceptance, `rigDiffPixels=0/921600` on a repeat of
`vign_camA_day`, cannot be met because that condition is unpinned. What would
happen to photometry under A: nothing, because there is no instrument.

B. EVERY SUN-ON CONDITION, the builder's scene, preserved at
`/tmp/claude-0/-home-user-ledger/61d1e27a-c59f-59dd-a264-d0decb90a8e9/scratchpad/vignette-scene.builder.json`:
21 non-rung day conditions at 0.300, the four rungs at 0.030, 0.300, 3.000
and 10.000, the two sun-off conditions at 0.000; 25 of 27 pinned. Sacrifice:
the adaptation moment (walking out of a dark alley) can no longer be
photographed on any day condition, a cost already accepted in writing when
the ladder was built; the three judged day frames move from the auto level to
the pinned one, a move the next run prints beside run 41's auto values
(section 9) rather than one this ruling asserts is small.

C. PROBE ROWS ONLY, pin the grid, fog, wetness and ladder rows and leave the
judged `overcast_day` at auto. Rejected: the judged hook frame is a deliberate
member of the null group (test 3033, "with the judged hook frame among them"),
so this splits one condition into two exposures and breaks the very
comparison the grid exists for; the determinism repeat stays unpinned and
235 stays unmeetable; and the Hook sheet comparison in step 2 is made on the
judged frame, which would still be under auto.

D. EVERYTHING, night included. Refused by section 3 of the 2026-09-10 ruling:
both night frames of run 41 were photographed mid-adaptation, no settled
night reference exists, and a day value written on a night row is a number
nobody measured for night.

## 5. Why A's reason has expired and what its guard still refuses

The guard's reason was true when it was written on 2026-09-10: no value had
been chosen, the four rungs were a bracket, and any other row carrying a pin
would have carried a guess. The ladder then printed its series (line 321), a
value was read off it, and the scene names where: `exposure_pin_provenance`
carries the run, the commit, the condition and the camera. A day row at 0.300
is now a row photographed at an exposure somebody chose, on a printed series,
with the provenance beside it.

What the guard was for survives in a stronger form. The thing to refuse is
still "an exposure nobody chose", and a pin value that is neither a rung's nor
the provenance-named live value is exactly that. So the invariant is restated
rather than deleted, and it gains a clause the old one could not state: the
live value must equal the value the provenance names. Bumping the C# literal
from 4 and 23 to 25 and 2 would have been the forbidden move under rule 2; the
builder did not make it and neither does this ruling.

## 6. The invariant, dictated, one statement for both suites

Four clauses over the conditions of the live file, accepting case first.

    (a) every condition answers the pin question: pinned plus unpinned equals
        the condition count (kept from the old check)
    (b) sun on implies a pin asked; sun off implies no pin asked
    (c) every sun-on condition that is not a ladder rung (id prefix `pin_`,
        `pin_setter_night` excluded) carries one and the same value, the
        LIVE value
    (d) the LIVE value equals the value the file's exposure_pin_provenance
        names, to the four decimals the shot line prints, so a live value
        edited on the rows without re-reading the series is refused

For (d) the provenance string gains one token carrying the value itself,
`pin0.3000`, placed after `cond.pin_030`, so the clause stays checkable on the
day the one-run ladder rows leave the file. While the named rung is present
its `exposure_pin` must also equal that token; when it is absent the token
stands alone and the check still bites. The rungs' own values are read off the
file, never retyped.

Four planted rejections, each breaking one clause, all watched: a day row left
at auto; a night row given a pin; two day rows disagreeing; a live value that
does not match the provenance token. The builder's C# already plants the first
three (`Program.builder.cs` 19666-19703).

The series is printed before it is asserted, on one line:
`pins: dayPinned=N dayUnpinned=N nightPinned=N nightUnpinned=N live=V
liveRows=N rungs=N span=Lo..Hi provenancePin=V of N conditions`. No spaces in
values.

A deliberately unpinned sun-on row (an adaptation study, for instance) enters
by a ruling amending clause (b), never by a `0.000` sitting quietly on a row.
That is the guard doing its job, not an obstacle to route around.

## 7. Exactly which tests move, and what must not

Three sites. Nothing else in either suite moves; a fourth check going red on
the batch is a finding to report, not a check to adjust. The resident measured
391 of 393 under the builder's scene and both failures are named here.

1. `ue-probe/tests/vignette-spec-test.cpp` 3236-3239, "the only rows asking
   for a pin are the ladder rungs": replaced by clauses (a) to (d) with their
   four plants and the printed series line. The span check at 3240 stays and
   computes its `Lo..Hi` over the rungs.

2. `ue-probe/tests/vignette-spec-test.cpp` 3030-3034, the seven typed ids.
   THE LIST IS RE-DERIVED, NOT RE-TYPED. The check's own comment (2994-2996)
   says the typed ids exist to anchor the discovery to the review's group, and
   the "independent tally" at 2997-3015 is not independent: it calls the same
   `SampleKey` the discovery calls. So the new anchor is built the way the
   null-cell check at 292-310 already compares two conditions: walk the shots
   in shot order, keep those at `cam_hook` whose condition matches
   `grid_sky100_sun003` field by field in every field that lights a frame
   plus `exposure_pin`, excluding the field the line itself says it excludes
   (`nullSeriesExcludes=wetness` while `VignetteShot.cpp` has no read site),
   and assert the line's `nullSeriesIds` equals that list exactly. Keep three
   assertions the typed list carried implicitly: `vign_hook_day` is in the
   list, `vign_grid_null_repeat` is last, and the list holds at least the
   reference cell and the null cell. This anchors to ONE named id, the cell
   the grid ruling defined as the reference, instead of seven.

   Why derived: the list has two scheduled reasons to change this week. The
   pin batch grows it from seven to nine, `vign_pin_030_afternight` and
   `vign_pin_030_afterday` joining because a rung at the live value is,
   correctly, a null sample of the live rows (the fingerprint at
   `VignetteSpec.h` 2574 includes `expPin`, which is why the resident read
   `nullSeriesSamples=9/of=37`). D28 step 5 wires wetness, after which
   `vign_wet_000` and `vign_wet_100` leave it. A typed list fails for the
   wrong reason twice in one week. The growth to nine is a gain, not a fault:
   the after-night half of rung 0.300 is the hardest null sample the run has.

3. `ledger/CoreTests/Program.cs` 19631, `pinned == 4 && unpinned == 23`:
   replaced by the builder's invariant as written in `Program.builder.cs`
   19625-19703, clauses (a) to (c) with three plants. Clause (d) is checked in
   the C++ suite only, because `StreetVignette.cs` (line 1862) reads
   `exposure_pin` and nothing in `ledger/Assets/Scripts` reads
   `exposure_pin_provenance`; the C# check's comment says so in one sentence.
   Teaching the C# reader the string is a named rung (section 11), not this
   batch.

The suite counts move and the delta is NAMED: which checks left, which
arrived, from 393 and from 4355 (the resident's reading of CoreTests with the
builder's Program.cs). A baseline that moves without a named delta can absorb
a deletion.

## 8. The batch, one commit, under this ruling

The matched set queue 274 established by reverting one file at a time, plus
the two test edits above:

- `production/specs/vignette-scene.json`: the builder's file, plus the
  `pin0.3000` token in `exposure_pin_provenance`, plus the one-clause edit to
  `exposure_pin_note` dictated in section 12.
- `ledger/CoreTests/Program.cs`: the builder's file.
- `production/specs/vignette-pieces.json`: regenerated with
  `dotnet run -c Release --project ledger/CoreTests -- --write-vignette-pieces --ahead-of-run cb4767e`,
  the invocation the 13:39 ruling section 4 identified and 274 row 5 measured
  green; the printed `piecesGap`/`keyWrittenInto` line goes in the commit
  message.
- `ue-probe/tests/vignette-spec-test.cpp`: the two sites in section 7.

No reordering of the shot list. No change to `VignetteShot.cpp`,
`VignetteSpec.h` or `FrameStats.h`; if the derived-list check needs a helper,
it lives in the test.

## 9. Queue 235's render: AFTER the batch, and what it must print

Dispatched after this batch lands, not on HEAD. The resident's view is upheld
and the reason is sharper than "more informative": a render on HEAD alone
answers one question, whether the leak is gone, and the render after the batch
answers that same question on the same key plus the two the week needs. One
round trip on Jafar's machine instead of two, and the leak proof is not
weakened by waiting because it is read on its own key. If the batch cannot
land before the runner is next reachable, that is a blocker to report, not a
reason to render HEAD.

Keys, with their denominators, and how each reading is read. No threshold is
set here.

- `expPinRowsLeaked=0/of=6/shots-asking-for-NO-pin`. The denominator falls
  from 29 at HEAD to 6 (`vign_camA_night`, `vign_camB_night`,
  `pinset_night_1..4`), and every one of the six is shot immediately after a
  pinned row, three of them being the rows that leaked on run 41 (lines 216,
  219, 222). Six rows that each exercise the mechanism outrank twenty nine of
  which four could. Do not read `0/of=6` against the test fixture's `0/of=29`
  as a regression.
- `expPinRowsHeld=31/of=31/shots-asking-for-a-pin`, and no shot line asking
  `0.0000` carrying `shotExposurePinOverrides=1/1`.
- `rigRepeatOf=vign_camA_day`, now pinned at 0.300 on both photographs.
  `rigDiffPixels=N/921600` is read as the number; `IDENTICAL` at zero is queue
  235's acceptance and D28 step 1 met on a pinned day condition. A non-zero is
  a finding that names a second cause on the pinned rig and is NOT a reason to
  move the pin.
- `nullSeriesSamples=9/of=37` with the nine derived ids, then
  `nullSpreadMeanLuma`, then `nullFloorMeanLuma`, then the verdict, in that
  order: read the rows before the verdict. `CLEAR` is what makes the grid
  readable for step 2; `NO-READ` on a pinned group is the finding of the run.
- `shotMeanLuma` on `vign_hook_day`, `vign_camA_day` and `vign_camB_day`,
  printed in the dispatch record beside run 41's auto readings 0.5800, 0.6099
  and 0.5340 (lines 193, 189, 191), so the move of the judged frames is a
  number and not a claim.
- The three `pinset_night` rows in one exposure family, reading `AUTO` at the
  captured pair, per section 10 of the 13:39 ruling.

## 10. What this ruling does not do

- It sets no night pin and no bound. Night frames remain non-comparable across
  shots, and `IDENTICAL` on the repeat line is a statement about one pinned
  day condition, never about the run. Say that in the dispatch record and in
  NOW.md so the line cannot be quoted as "the rig is deterministic".
- It does not re-open the value. 0.300 is held through D28 step 2 so that the
  sky and sun series are read at one exposure; a value moving under a series
  confounds the light with the camera. Re-opening it is a ruling with step 2's
  printed series in hand, not a builder's option. This supersedes the "finer
  ladder is the next rung" clause in the scene's `exposure_pin_note`; the
  replacement text is in section 12.
- It does not touch the leak fix, the determinism instrument, or the
  cross-engine anchor of queue 273.

## 11. The quality ladder at close, and two rungs that were never filed

Best available, or first working? First working: one live value, chosen for
determinism at the rung that clipped nothing, not for matching the reference
sheet's 0.4102. The next rungs, named:

1. THE SETTLED NIGHT EXPOSURE REFERENCE, shape dictated in section 3 of the
   2026-09-10 ruling (render the night condition repeatedly, print the
   settling series, name the statistic, only then a night rung set). That
   ruling ordered it "to the queue with a name". Grepped this session over the
   268 files in `production/queue/` for "settled night", "night exposure
   reference" and "finer ladder": 0 hits; the phrases exist only in
   `production/findings.txt` and two `brief-input` dossiers. It was never
   filed. The resident files it now, by name, as a research rung.
2. The C# reader carrying `exposure_pin_provenance`, so CoreTests can check
   clause (d) and the two suites state all four clauses. One parse, filed by
   name.
3. Wetness wired (D28 step 5), after which the null group shrinks and the
   derived list follows it without an edit.
4. The finer ladder inside 0.300..3.000: NOT filed now, held behind step 2 by
   section 10, and re-raised only with step 2's series printed.

## 12. Dictated text the resident hand-applies, and nothing beyond it

A. `production/specs/vignette-scene.json`, `exposure_pin_provenance`: insert
the token `pin0.3000` immediately after `cond.pin_030`, so the string begins
`run41/verdict-f6508b3/cond.pin_030/pin0.3000/cam_hook/...`.

B. Same file, `exposure_pin_note`: the sentence beginning "A finer ladder
inside that bracket is the next rung" is replaced by: "The value is HELD at
0.300 through D28 step 2 by the ruling of 2026-09-14
(game-design/decision-2026-09-14-ruling-the-pin-belongs-to-the-rig-and-the-render-waits-for-it.md),
so that the sky and sun series are read at one exposure; a finer ladder inside
the 0.300 to 3.000 bracket is re-raised only with that series printed, and no
number here was interpolated toward the reference's 0.4102."

C. `production/queue/274-...md`, STATUS line: "RULED 2026-09-14, position B,
under game-design/decision-2026-09-14-ruling-the-pin-belongs-to-the-rig-and-the-render-waits-for-it.md.
Lands as one commit per its section 8; closes when the first Unreal run on or
after it prints section 9's keys."

D. `production/queue/235-...md`, appended to status: "RULED 2026-09-14: the
acceptance render is dispatched AFTER the pin batch, with rigRepeatOf on a
pinned day condition. IDENTICAL there is step 1 met on that condition and says
nothing about night, which stays at auto."

E. `production/NOW.md`, replacing "NEXT: the pin ruling, then the render for
step 1": "RULED 14:xxZ: every sun-on condition carries the pin (B); the batch
lands as one commit; the step 1 render is dispatched after it and reads
expPinRowsLeaked=0/of=6, rigDiffPixels on a pinned vign_camA_day, and the
nine-id null series. Night stays at auto; the pin is held at 0.300 through
step 2." The resident fills the time from the commit.

## 13. Conditions the resident must PRINT before committing

Each a printed artefact in this session's scrollback, not a recollection.

13.1 `python3 ledger/verify.py` green, footer pasted FROM `ledger/.verify-footer`.

13.2 `vignette-spec-test`, `frame-stats-test` and CoreTests counts printed on
the final tree, with the delta from 393, 113 and 4355 named check by check.

13.3 The new invariant's accepting run on the live file and its four planted
rejections, printed, accepting first. The C# three plants likewise.

13.4 The flagged regeneration line (`ahead-of-run cb4767e piecesGap=...
keyWrittenInto=...`) and both piece-list checks green on the final tree.

13.5 Rule 6 call-site grep: `exposure_pin` in the scene, printed as counts:
27 conditions carrying the key, 25 non-zero, 2 at `0.000`; and the
`pin0.3000` token present once.

13.6 `python3 tools/docs-check.py` and `python3 tools/goal-block-check.py`.

13.7 This record opened and read back: banner within the first eight lines,
stamp bare at the foot.

## 14. What this director refuses

- A render dispatched on HEAD before the batch.
- Any pin on a sun-off condition, and any night value derived by arithmetic
  from a day one (forbidden by name on 2026-09-10).
- Any change to the pin value before step 2's series is printed.
- The nine ids typed into the test, or the literal 4 and 23 bumped to 25 and 2.
- Any sentence calling the rig deterministic on the strength of the repeat
  line alone.

<!--RULING spawn=2026-09-14T14:12:50Z-->
