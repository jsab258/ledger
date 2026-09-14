# Ruling, 2026-09-14 (18:23Z): the null series follows the judged row, because the grid's reference cell IS the judged row and its fog was a copy

STATUS: LOG, 2026-09-14. NOT CURRENT once the fog dispatch this unblocks has
landed; from then the verdict file, the two test suites, and queue 235, 285,
287, 288, 289 and 290 are the reading copies and this is the record of what
was ruled and why.

Director ruling on one question, escalated by the resident as a
verifier-builder disagreement on a simulation-adjacent instrument: once the
judged day cell leaves the grid's reference cell, which group is the run's
noise floor? No code was written by this director and this director has no
shell. Every number below was read off the file and line it names in this
session, or is arithmetic shown in full. The resident's compile of the test
suite ("2 of 404 checks failed") is quoted from the resident's message and is
a claim until `ledger/verify.py` writes a footer on the landing tree.

Author: tier-1 director, stamp at the foot naming row 599 of
`.claude/agent-log.tsv` (`2026-09-14T18:23:24Z` TAB `studio-director`,
agentId `a93e40eed22829b8c`), which the commit gate printed as
`rulingUnruledNewest`. Row 594 belongs to the fog ruling and is not claimed.

## 0. What was opened, so the reader knows the denominator of this record

`ue-probe/tests/vignette-spec-test.cpp` 100 to 130, 440 to 720, 3180 to
3620; `ue-probe/Source/LedgerProbe/Public/VignetteSpec.h` 2500 to 2920;
`ue-probe/Source/LedgerProbe/Public/FrameStats.h` 296 to 336 and 960 to
1010; `ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp` 200 to 216, 1520
to 1660, 2336 to 2365, 2815 to 2865; `ue-probe/Config/DefaultEngine.ini`
whole (30 lines); `ledger/CoreTests/Program.cs` 19780 to 19830, 19925 to
19975, 20100 to 20240; `production/specs/vignette-scene.json` every
condition's `id`, `fog_max_opacity` and `note` (33 conditions, 43 shots at
1380 to 1422); `production/d1-probe/ue-vignette-verdict.txt` line 1
(`32bae70`), 141, 186, 193 to 225 by key, 208, 319, 323; the 2026-09-09 grid
ruling (A4 at 300 to 322, C11 at 560) and grid batch review (section 4 at 247
to 287, amended C4 at 543 to 551); the 14:12Z pin ruling 40 to 84 and 190 to
219; the 16:25Z fog ruling 280 to 620; D28 line 27; D32 whole; queue 186,
235, 273, 285, README; `tools/docs-check.py` 160 to 260 and 730 to 772;
`ledger-v2/studio-v2/organization.md` 90 to 150; `ledger-v2/respec/
decision-register/rulings-log.md` 1 to 108 and 225 to 259;
`.claude/agent-log.tsv` 590 to 601.

## 1. The answer in one sentence

NEITHER GROUP IS THE FLOOR, BECAUSE THERE IS ONLY ONE QUESTION AND THE DATA
ANSWERED A DIFFERENT ONE: the grid's reference cell exists to carry the judged
row's inputs, so when the judged row moved, the five rows that share its cell
(`grid_sky100_sun003`, `grid_null_repeat`, `wet_000`, `wet_060`, `wet_100`)
were due to move with it and did not, because each carries a literal 0.450
copied on 9 September and nothing derives it. The fog cap on those five rows
moves to 0.100. No guard is re-anchored, no bound moves, no instrument
changes, and the discovered null series comes back as nine frames in shot
order with the judged frame first and the null repeat last, which is the group
the 14:12Z pin ruling predicted and the 16:25Z fog ruling's item 6 expected.

## 2. What I verified, claim by claim

THE THREE GUARDS ARE NOT IN CONFLICT; ONE FIRED, AND IT FIRED ON THE DATA. At
`vignette-spec-test.cpp` 3336 to 3414 the expected list is DERIVED from the
literal id `grid_sky100_sun003`, field by field at that row's own camera, so
when the judged row left the reference cell the expected list left with it
and 3410 stayed green (the resident's compile confirms: `ok` at 3411, `ok` at
3434, `FAILED` at 3422). A derived check moves with the data by construction
and can only catch a miscount; 3421 to 3423 is the check that carries the
claim "this group speaks for the frame Jafar looks at", and it went red the
moment that claim stopped being true. That is a guard working.

THE FINGERPRINT (`VignetteSpec.h` 2568 to 2588) is sun on/off, sun intensity,
sky intensity, HDRI, fog density, fog max opacity, lanterns, practicals and
the exposure pin, at one camera (`SampleKey`, 2615 to 2619). Wetness is not
in it and the line says why: `wetness` has three hits in `ue-probe/Source`,
all in the header (257, 284, 497), and none in `VignetteShot.cpp`. Two rows
differing only in wetness render the same street in this engine, so the three
wetness rows are legitimate null samples HERE. The coordinator's mid-task
claim that they were accidental members was withdrawn by the coordinator and
is refuted by that grep.

`NullSeriesLine` (2638 to 2847) takes the LARGEST identical-input group, ties
broken by first appearance in shot order on a strict greater-than (2692 to
2697). It has no flag, no parameter and no second group. The fourth route the
resident was told to look for is not in the code; it is in the data, section 3.

THE JUDGED ROW'S TWINS, ON THE FILE. `overcast_day` (883 to 895) and
`fog_maxop0100` (1138 to 1150) agree in every field. `pin_030` (1318 to 1330)
agrees in every field and its note says why: "A rung left at 0.450 would
photograph a street the judged frame no longer shows", asserted in CoreTests
19803 to 19811 against `overcast_day` INCLUDING the fog cap. So the builder
already applied, to the pin rows, the principle this ruling applies to the
other five, and CoreTests is green on it (4367). The five rows that did not
follow: `grid_sky100_sun003` 936, `grid_null_repeat` 1101, `wet_000` 1266,
`wet_060` 1281, `wet_100` 1296, all 0.450.

WHAT THOSE FIVE ROWS SAY THEY ARE. The reference cell's note (940): "THIS IS
THE GRID'S REFERENCE CELL and the first half of the null pair". The null
repeat's note (1105): "Every field is a character-for-character duplicate of
grid_sky100_sun003". Each wetness row's note (1270, 1285, 1300): "wetness
0.00 at the grid's reference cell (sky 1.00, sun 3, fog_max_opacity 0.450)"
and "both ends plus the value the judged conditions already carry". Section 4
of the 2026-09-09 batch review, on why the reference cell matters at all:
"`overcast_day` at `:764` agrees with `grid_sky100_sun003` at `:806` on all
of them, which is worth saying twice because it means THE JUDGED HOOK FRAME IS
ITSELF A MEMBER OF THE NULL SERIES and the run can say whether rung 1's own
frame is exposure-drifted relative to the grid." The reference cell was the
reference BECAUSE it equalled the judged row. A reference cell that no longer
does is a reference for a street nobody ships.

THE 16:25Z RULING EXPECTED THIS AND NAMED THE FINDING. Its section 2.5 item 6:
"`nullSeriesIds` naming `vign_fog_maxop0100` and NOT `vign_fog_maxop0450` (the
null twin follows the judged row by derivation; if 0450 is still listed, the
derivation is stale and that is the finding)". There is no derivation in the
spec: A4 made every field required with no defaults, so the twins carry copies.
The copies are stale. That is the finding, and it lives in the JSON.

THE RENDERED FLOOR, so nobody quotes a fixture number as a measurement. On
`32bae70` line 319 the nine-id group (hook, reference, 0450, three wet, two
pin_030, null) reads `nullSpreadMeanLuma=0.0002` (max `vign_wet_060` 0.6600,
min `vign_pin_030_afternight` 0.6597), `nullSpreadGroundP05=0.0012`,
`nullSpreadGroundP50=0.0008`,
`nullDriftMeanLuma=-0.0000/first=vign_hook_day/last=vign_grid_null_repeat`,
verdict CLEAR on 3 of 3 against steps 0.0296, 0.0620 and 0.0036. The `0.0010`
the coordinator first compared against the twin pair's 0.0000 is the TEST
FIXTURE's synthetic noise (`vignette-spec-test.cpp` 3264:
`0.30 + 0.20 * sky + 0.0005 * (I % 4)`), not a render, and the coordinator
later said so. The rendered pair `vign_hook_day` / `vign_fog_maxop0450` (lines
193, 206) differs by 0.0000 on mean luma and 0.0001 on ground p05, and it sits
INSIDE the nine's 0.0002 and 0.0012. A two-frame difference is a subset of a
nine-frame max-minus-min and cannot exceed it; that is arithmetic, not a
tighter rig. The nine is the at-worst statistic the amended C4 chose on
purpose, because "a one-pair difference cannot tell a monotone drift from a
step". The coordinator's separation hypothesis was withdrawn on the run's own
`nullDrift` key and is not weighed here.

THE SECOND RED IS FIXTURE ARITHMETIC. The check at 3463 to 3467 says "the
spread, the one-pair drift and whether the group is monotone all print" and
asserts `nullSpreadMeanLuma=0.0015/max=`, the fixture's maximum possible
spread, which holds only while the discovered group contains a shot at index
residue 0 and one at residue 3 (mod 4). Shot indices from 1380 to 1422, 0-based:
hook 4, reference 6, 0450 17, 0100 19, wet 21/22/23, pin_030 34/35, null 42.
The builder's six at 0.450 have residues {1,2,3}: 0.0010, red. The judged four
have {0,2,3}: 0.0015. The nine of section 3 have {0,1,2,3}: 0.0015, max at
`vign_fog_maxop0100` (first residue-3 frame in group order), min at
`vign_hook_day`. Green, for the right reason, and the check's shape is queue
288's problem, not tonight's.

## 3. The ruling

THE FIVE ROWS FOLLOW THE JUDGED ROW. `production/specs/vignette-scene.json`,
`fog_max_opacity` 0.450 to 0.100 on `grid_sky100_sun003` (line 936),
`grid_null_repeat` (1101), `wet_000` (1266), `wet_060` (1281), `wet_100`
(1296). Their notes gain the sentences in section 8. Nothing else in the
JSON moves.

WHAT STAYS, AND WHY. `fog_maxop0450` stays at 0.450: its fog IS the field it
varies, and it is the series' first point; its note's "repeats the value in
force" becomes past tense (section 8). The eleven other grid cells stay at
0.450 tonight: the grid's cell choice was READ at 0.450 on `32bae70` and is
done; its remaining job, the sky step the null verdict is read against, is now
supplied at 0.100 by the three cross rows plus the judged family, and
`fog_maxop0450` remains the 0.450 family's (sky 1.00, sun 3.0) point so the
0.450 series loses nothing. Moving twelve rows for a fog value that queue 285
may move again is 285's landing ruling to decide, move or retire; NOT ordered
here. `wet_night` is not touched (16:25Z section 2.2).

THE GUARDS DO NOT CHANGE. 3410 to 3414, 3421 to 3423, 3424 to 3426, 3433 to
3437 and 3463 to 3467 keep their text and their bounds. `NullSeriesLine` and
`AppliedFieldsUnreal` do not change.

THE EXPECTED GROUP, in shot order, nine at `cam_hook`:
`vign_hook_day;vign_grid_sky100_sun003;vign_fog_maxop0100;vign_wet_000;
vign_wet_060;vign_wet_100;vign_pin_030_afternight;vign_pin_030_afterday;
vign_grid_null_repeat`. Nine is under the cap of 12, so the cap does not bite.
The 0.450 family at that cell is `vign_fog_maxop0450` alone. Largest group 9,
`nullSeriesTiedGroups=0`. On the rendered run this is line 319's list with
`vign_fog_maxop0450` replaced by `vign_fog_maxop0100`, which is item 6's
expectation word for word.

WHAT THE FLOOR NOW IS, said per rule 2 so nobody reads it as something else.
`nullSpread` is max minus min over the nine, an AT-WORST over the group;
`nullDrift` is last minus first in shot order, and with `vign_hook_day` first
and `vign_grid_null_repeat` last it is exactly "rung 1's own frame against the
rig's last frame", the statement section 4 of the batch review wanted; the sky
step is the SMALLEST difference between any two frames differing in sky alone,
found across both fog families, so it is found over a superset of the judged
family's own sky pairs and the verdict is at least as strict as one confined
to them. No number is set by this ruling. The 0.0015 is fixture arithmetic
recomputed above; the fog 0.100 was set by the 16:25Z ruling off a rendered
series.

ONE GUARD IS ADDED, IN BOTH SUITES, IN THE SHAPE EACH ALREADY HAS. After the
null-cell duplicate check (`vignette-spec-test.cpp` 516 to 534; CoreTests
19931 to 19956) a Check that `grid_sky100_sun003` equals `overcast_day` in
every field that lights a frame plus the pin, wetness included, with the
sentence: "the grid's reference cell is the judged day row in every field that
lights a frame, because the reference cell exists to carry the judged row's
inputs and a judged frame that is not in its own null series has walked out of
the floor that speaks for it". On failure it names the field and both values.
This is a Check inside two suites that already walk these rows, in the shape of
a Check already there; under Jafar's no-new-instrument rule it is the D32
shape ("inside an instrument that already walks these files"), not a new tool,
and nothing is retired because nothing is added. It is the pair the data move
owes under rule 5b, and it is what would have gone red before the builder hit
the fog rows tonight, and will go red before the next fog move does.

## 4. Rule 5b: the accepting case and the rejecting case, for every guard touched

- 3422 (hook in the group). Accepting: the live spec after section 3, hook
  first of nine. Rejecting: the live spec BEFORE section 3, which is the
  resident's own red run tonight ("FAILED - the judged hook frame is one of
  the null samples"). Both watched on live data in one session.
- 3411 and 3434. Green before and after; a derived list moves with the data.
  Their rejecting cases are unchanged from the file.
- 3463 (the 0.0015 prefix). Accepting: the nine, residues {0,1,2,3}.
  Rejecting: tonight's six, residues {1,2,3}, 0.0010. That it rejects for a
  residue coincidence and not for a fault is queue 288.
- The new reference-cell guard. ORDER OF OPERATIONS TONIGHT: add the guard
  FIRST and run both suites on the unmoved JSON, so its rejecting case is the
  live tree (`fog_max_opacity` 0.100 against 0.450) and the FAILED line is
  printed; THEN apply section 3 and print it green. It also keeps a synthetic
  rejecting fixture so it is watched on every run and not only tonight: a
  copy of the parsed conditions with the reference cell's fog set back to
  0.450, run through the same comparison, expected to refuse naming
  `fog_max_opacity`. Accepting case printed first, per the instruments rule.

## 5. The routes, costed against the file

- A, follow the judged cell by re-anchoring the derivation's literal id to
  `overcast_day`. The data would still hold `grid_null_repeat` at 0.450, so
  the maximum-separation sample ("the whole of its value", CoreTests 20118)
  would measure the 0.450 street while the judged family was read over
  positions 5 to 36. Loses the null cell's job. REFUSED.
- B, drop 3422. The floor becomes a property of a condition nobody ships,
  item 6's own expectation is contradicted, and rung 1's frame has no drift
  statement. REFUSED.
- C, move the wetness trio only (the builder's measured alternative). Half
  right: the trio does move. Without the pair it is route A in the data.
  REFUSED as tried, ADOPTED as part of section 3.
- D, print two groups. A widening of the line (two new key families on an
  existing line), not a new instrument, so the monthly rule would not bar it.
  Refused on the merits: two groups are the right shape only when the grid's
  reference condition and the judged condition are legitimately different
  conditions. They are not; one is defined as the other. And the null repeat
  would still sit at 0.450. REFUSED tonight; section 13 names the trigger on
  which it becomes the right shape.
- E, do not move the judged row this run. The decision was made on a
  rendered, opened cell and is already a matched set in two suites; the red
  guards were reporting a stale copy, not a wrong decision; a retreat costs a
  round trip and a frame. REFUSED.
- F, this ruling. Five numbers in JSON, five note sentences, the pieces file
  regenerated, one guard in two suites, two comments corrected, four false
  note sentences corrected. Nothing loosened, nothing re-anchored, nothing
  new. Render cost: zero extra shots (43 stays 43); five rows change picture,
  all five having only ever served as null samples, which they remain, now of
  the street that ships.

## 6. Section 2.5 item 6 of the 16:25Z ruling, restated to what the verdict can answer

VERIFIED: `fogMaxOpacityRead` occurs ONCE in
`production/d1-probe/ue-vignette-verdict.txt`, on line 186, the run-level sky
line, value 0.450; on 0 of the 37 shot lines. It is read in `SkySegmentNow()`
(`VignetteShot.cpp` 1635 to 1643), which runs "when a verdict asks for the
line, by which time every condition the run applied has been applied" (1613 to
1614): one read per run, last-wins, off the component after the last condition
applied, with nothing asked beside it. The shot line carries
`shotSunIntensityAsked/Read` and `shotSkyIntensityAsked/Read` "read off the
components while THIS frame stood" and no fog key (line 208 read in full). So
"asked beside read on all seven fog rows" has never been answerable, on any
run, and neither was C11 of the 09-09 grid ruling ("on all four fog rows"),
nor queue 285's acceptance line as filed, nor the sentence the four A4 notes
carry ("fogMaxOpacityRead is printed beside what was asked on every shot",
four hits, all in the spec), nor `VignetteShot.cpp` 1547 to 1548. Rule 1:
grep the sentence, and the copies are named here so the resident corrects
every one (section 8). No landing was recorded as having verified it:
`production/NOW.md` 1180 to 1186 is a pre-statement, written before the run.

ITEM 6 AS IT NOW READS. The sha captured before dispatch, the run watched by
ancestry. On landing:
(a) the sky line's `fogMaxOpacityRead` reads 0.100, which is the cap of the
    LAST condition applied, `vign_grid_null_repeat`, one per run, last-wins;
    it read 0.450 on `32bae70` when that row asked 0.450. A 0.450 here means
    the field did not reach the component on the last row or the shot order
    changed, and the finding is named as one of those two;
(b) THE FRAME ANSWERS PER ROW, which C10's own logic prefers to a readback:
    the seven fog rows' `band.skyCentre.meanLuma` printed as a series in cap
    order and strictly decreasing with the cap; the four rendered rungs beside
    their `32bae70` values 0.9268 / 0.8822 / 0.7979 / 0.6222 (lines 206 to
    209) with residuals stated and NO bound; the three new rungs between
    0.7979 and 0.6222. A 0.100 row whose sky band sits at the 0.450 level is
    a cap that did not take;
(c) `nullSeriesIds` equal to the nine of section 3 in shot order,
    `vign_fog_maxop0100` in and `vign_fog_maxop0450` out; `nullDrift` with
    `first=vign_hook_day` and `last=vign_grid_null_repeat`; the nine's sky
    band near 0.7979 and not near 0.9268; the verdict word read, and NO-READ
    escalated per C4 rather than quoted around;
(d) the three cross rows' two statistics printed as a series over sky.
Per-row asked beside read arrives with queue 287 and is not owed tonight.

QUEUE 285'S ACCEPTANCE LINE is restated the same way: "asked beside read on
all of them" becomes "(a) and (b) above, and per-row asked beside read once
287 has landed".

QUEUE: 285 the-fog-cap-between-0-and-0-10-is-unrendered

## 7. What is filed, and what is not

QUEUE 287, the per-shot fog read. A widening of the existing per-sample shot
line: `shotFogMaxOpacityAsked`, `shotFogMaxOpacityRead`,
`shotFogMaxOpacityResidual`, read off the height fog component while THIS
frame stood, at the same read site and in the same shape as
`shotSkyIntensityAsked/Read`; the formatter in the tested layer
(`VignetteSpec.h`), the fixture beside it with a planted row reading 0.450
against 0.100 asked (tonight's fault shape) and an accepting row at residual
0.000000; the run-level key keeps its name and its stat gains
"one-per-run/last-wins". I read it as a widening of an existing instrument
under the no-new-instrument rule (no new file, reader or gate; two keys on a
line whose readers already split on whitespace), the same class as 284. The
landing director may read it otherwise and must then name a retirement.

QUEUE: 287 the-fog-cap-is-read-per-shot-beside-the-sun-and-the-sky

QUEUE 288, the fixture check at 3463 to 3467. Its sentence says three keys
print; its assertion is the fixture's maximum spread, true only for a residue
coincidence. Split it: one check that the keys print, one that the printed
spread equals the spread recomputed from the discovered group's own indices by
the fixture's formula, so the expected number moves with the data the way the
derived id list already does. Not blocking.

QUEUE: 288 the-fixture-spread-check-asserts-a-coincidence-of-shot-indices

WETNESS IN UNREAL IS NOT A NEW ITEM. The coordinator asked for one. Queue 186
already says "WETNESS IS PARSED AND READ BY NOTHING in this engine", names
`StreetVignetteHost.cs:715` as the Unity read site, and says in its own text
why the wetness half must not be split from the sky and reflection halves
("Wiring Wetness alone makes the road darker and smoother WITH NOTHING TO
REFLECT, which is a black road rather than a wet one"). D28 step 5 ("Wire
wetness. It is parsed and read by nothing, and the reference street is wet")
is 186. The coordinator's correction stands: it is a PORT from the retired
engine, not a build, and 186's status line may say so in one sentence. Do not
file a second item; the resident should not either.

QUEUE: 186 the-street-has-no-sky-and-wetness-reaches-nothing

Queue 289 and 290, and 235's next measurement, are in section 13.

NOT ORDERED, NAMED SO NOBODY DERIVES IT LATER: whether the eleven 0.450 grid
cells move to the shipped fog or retire is decided by queue 285's landing
ruling, when the fog value is settled. Not before.

## 8. Dictated text, so the resident applies it and does not invent it

Every replacement below is verbatim. Where a sentence is replaced, grep the
sentence and replace every copy (rule 1), then paste the before and after
counts into the commit message.

1. `grid_sky100_sun003` note, appended: "FOG CAP MOVED 0.450 TO 0.100 ON
   2026-09-14 (ruling of 18:23Z, decision-2026-09-14-ruling-the-null-series-
   follows-the-judged-row.md). This cell is the reference cell BECAUSE it
   carries the judged row's inputs, which is what made the judged hook frame a
   member of the null series (section 4 of the 2026-09-09 grid batch review).
   Its 0.450 was a copy of overcast_day's value on 9 September and not a
   choice; when overcast_day moved to 0.100 the copy went stale and the judged
   frame walked out of its own null series. The cell follows the judged row,
   both test suites assert that it does, and the eleven other grid cells stay
   at 0.450 until queue 285's landing ruling decides whether the 0.450 grid
   moves or retires."
2. `grid_null_repeat` note, appended: "FOG CAP MOVED 0.450 TO 0.100 ON
   2026-09-14 with its twin, under the ruling of 18:23Z; the twin is shot 7 of
   43 and this row 43 of 43, thirty-six shots apart, and the duplicate is
   asserted field by field in both suites." (The note's "shot 7 of 25" and
   "eighteen shots apart" are stale since the pin batch; correct them
   opportunistically to 43 and thirty-six, which CoreTests 20119 to 20120
   already says.)
3. `wet_000`, `wet_060`, `wet_100` notes: "(sky 1.00, sun 3, fog_max_opacity
   0.450)" becomes "(sky 1.00, sun 3, fog_max_opacity 0.100 since
   2026-09-14)"; appended: "FOG CAP MOVED 0.450 TO 0.100 ON 2026-09-14 under
   the ruling of 18:23Z: this row is the judged row at one wetness and its fog
   was a copy of the judged row's, not a choice. Left at 0.450 it would have
   been a wetness series about a street the judged frame no longer shows and,
   wetness having no read site in Unreal, a null sample of the wrong street."
4. In every note carrying it (four today: the A4 rows at 1120, 1135, 1150,
   1165), "The 0.450 row is the series' own first point and repeats the value
   in force." becomes "The 0.450 row is the series' own first point; it
   repeated the value in force until 2026-09-14, when the judged row moved to
   0.100 and fog_maxop0100 became the row that repeats it."
5. In every note carrying it (the same four), "fogMaxOpacityRead is printed
   beside what was asked on every shot, so this row's own frame says whether
   the field arrived." becomes "fogMaxOpacityRead is printed ONCE PER RUN on
   the verdict's sky line, last-wins off the component after the last
   condition applied, so it speaks for the null repeat and not for this row;
   this row's own band.skyCentre.meanLuma, read in cap order against the other
   fog rows, is what says whether the field arrived, and queue 287 adds the
   per-shot read beside the ask."
6. `VignetteShot.cpp` line 212, "The two judged conditions carry 0.450, so
   nothing moved." becomes "The two judged conditions carried 0.450 when this
   was retired, so nothing moved that day; overcast_day moved to 0.100 on
   2026-09-14 by ruling off the rendered series, and the rows sharing its cell
   followed it (ruling of 18:23Z)."
7. `VignetteShot.cpp` lines 1547 to 1548, "the verdict prints
   fogMaxOpacityRead beside what was asked." becomes "the verdict prints
   fogMaxOpacityRead ONCE PER RUN on the sky line, read off the component
   after the last condition applied (SkySegmentNow, last-wins), with nothing
   asked beside it; the per-shot read beside the ask is queue 287."
8. The 16:25Z record, a block inserted BEFORE its stamp line (619 today) so
   the stamp stays last:

       ## CORRECTION 2026-09-14, 18:23Z

       Section 2.5 item 1 moved `overcast_day` alone and item 6 expected
       `nullSeriesIds` to follow "by derivation". The null series is
       discovered from the condition rows, and the rows that share the
       judged cell (`grid_sky100_sun003`, `grid_null_repeat`, `wet_000`,
       `wet_060`, `wet_100`) carry a literal 0.450 with no derivation, so on
       the working tree the judged frame left its own null series and the
       hook guard went red. Ruled 18:23Z in
       `decision-2026-09-14-ruling-the-null-series-follows-the-judged-row.md`:
       those five rows follow the judged row, and item 6's "asked beside
       read on all seven fog rows" is restated there, because
       `fogMaxOpacityRead` is one run-level, last-wins read (verdict line
       186) and no shot line carries it.

9. `rulings-log.md`, one line at the end of the date-ordered section, in that
   file's own form:

       - **2026-09-14** the null series follows the judged row: the grid's
         reference cell, its null repeat and the three wetness rows take the
         judged row's fog (0.100) because their 0.450 was a copy; no guard
         re-anchored, no bound moved; item 6 of the 16:25Z fog ruling
         restated to what the verdict can answer; 287 to 290 filed and 235
         given its next measurement
         `game-design/decision-2026-09-14-ruling-the-null-series-follows-the-judged-row.md`

10. The four queue items, front matter per `production/queue/README.md`,
    filenames exactly as the markers in sections 7 and 13 name them:

        287-the-fog-cap-is-read-per-shot-beside-the-sun-and-the-sky.md
        line: engine (the Unreal probe's verdict)
        spec: the shot line gains shotFogMaxOpacityAsked,
          shotFogMaxOpacityRead and shotFogMaxOpacityResidual, read off the
          height fog component while THIS frame stood, at the read site and
          in the shape of shotSkyIntensityAsked/Read (VignetteShot.cpp, the
          per-sample read that feeds shotLightStat). The formatter lives in
          VignetteSpec.h, the tested layer; the fixture in
          vignette-spec-test.cpp plants one row reading 0.450 against 0.100
          asked (the 2026-09-14 fault shape) and one at residual 0.000000,
          accepting first. The run-level fogMaxOpacityRead keeps its name and
          its stat gains one-per-run/last-wins. VignetteShot.cpp 1547 to 1548
          and the four A4 notes say per run until this lands.
        acceptance: a committed run whose 43 shot lines each carry the three
          keys, asked equal to the row's fog_max_opacity on 43 of 43 with
          residual 0.000000, the seven fog rows' asked values reading 0.450,
          0.250, 0.100, 0.080, 0.050, 0.020 and 0.000 on their own lines, and
          both fixture outcomes printed.
        max_sessions: 1
        status: READY 2026-09-14, filed by the ruling of 18:23Z. Read by that
          ruling as a widening of the existing shot line under the
          no-new-instrument rule; the landing director may read it otherwise
          and must then name a retirement. Does not block the fog dispatch.

        288-the-fixture-spread-check-asserts-a-coincidence-of-shot-indices.md
        line: engine (test hygiene, ue-probe/tests/vignette-spec-test.cpp)
        spec: the check at 3463 to 3467 says "the spread, the one-pair drift
          and whether the group is monotone all print" and asserts
          nullSpreadMeanLuma=0.0015, the fixture's maximum possible spread
          (0.0005 times shot index mod 4), true only while the discovered
          group holds a shot at residue 0 and one at residue 3. It went red on
          2026-09-14 for that reason alone (residues 1, 2, 3 gave 0.0010) and
          will again on any row change that shifts the residues. Split it:
          one check that the three keys print; one that the printed spread
          equals the spread recomputed from the discovered group's own
          indices by the fixture's formula, so the expected number moves with
          the data the way the derived id list does.
        acceptance: both checks on the live spec with the accepting case
          printed; a planted group at residues {1, 2} (expected 0.0005)
          passing the recomputed form and failing the literal form, printed.
        max_sessions: 1
        status: READY 2026-09-14, filed by the ruling of 18:23Z. Not blocking.

        289-rigrepeataftershots-is-one-variable-printed-twice.md
        line: instruments
        spec: VignetteShot.cpp 2829 sets OfShots = GSpec.Shots.size() and
          passes it as BOTH ShotsBetween and ShotsAsked to RigDeterminismLine
          (FrameStats.h 966 to 968) at 2833, 2842, 2848, 2856 and 2863, so
          rigRepeatAfterShots has read 25/25 and 37/37 and can read nothing
          else: it cannot see a repeat that fired early. ShotsBetween becomes
          the count of shots actually photographed before the repeat was
          captured, read off the run's own shot counter at that moment;
          ShotsAsked stays the list length. The fixture in frame-stats-test.cpp
          plants a repeat taken after 3 of 5 and expects 3/5, beside the
          accepting N/N; the rig line's stat names which count is which.
        acceptance: a committed run printing rigRepeatAfterShots=<n>/<N> from
          two different variables, the planted 3/5 fixture printed red on
          the old code and green on the new.
        max_sessions: 1
        status: READY 2026-09-14, filed by the ruling of 18:23Z from a
          verifier's finding, verified at the lines named. Not blocking.

        290-the-rig-repeat-frame-is-deleted-before-anyone-can-open-it.md
        line: instruments (the evidence channel)
        spec: Finish() in VignetteShot.cpp (2345 to 2354) deletes
          kRepeatPngLeaf at 2352 under the comment "THE PROBE'S SCRATCH FRAME
          IS NOT EVIDENCE", so the frame behind rigDiffPixels and
          rigMeanLumaDelta never reaches the committed channel and nobody can
          open the difference the headline number describes (CLAUDE.md rule
          12). The repeat frame is kept, staged BY NAME in the workflow beside
          ue-vign_camA_day.png (ci.md: stage outputs by name) with a per-run
          copy keyed by short sha; the light-probe scratch frame at 2351 stays
          deleted, and the comment says which of the two is evidence and why.
        acceptance: a committed run whose tree carries the repeat frame beside
          its first frame, rigRepeatOf naming both files, and a difference
          image or histogram producible from the two committed files by a
          tool under tools/ on this machine.
        max_sessions: 1
        status: READY 2026-09-14, filed by the ruling of 18:23Z from a
          verifier's finding, verified at the lines named. Lands before or
          with the diagnostic run under 235, which is unreadable without it.

11. Queue 235, a paragraph appended to its status:

        RULED 2026-09-14 18:23Z (decision-2026-09-14-ruling-the-null-series-
        follows-the-judged-row.md, section 13). The post-pin run 32bae70 read
        DIFFERS 784509/921600, +0.0034, ratio 1.0053 (verdict line 323) on
        the pinned camA repeat, while the nine identical-input frames at
        cam_hook spread 0.0002 (line 319). A verifier's diagnosis names
        sub-pixel anti-aliasing sampling as the cause of the pixel COUNT
        (histogram shouldering at one and two codes, gradient-correlated, no
        one-pixel shift improves the match); the project's own FrameStats.h
        316 to 320 already says temporal AA moves pixels by a code value or
        two and measures a control for it; nothing under ue-probe, tools or
        .github pins the AA method or jitter (zero hits) and
        DefaultEngine.ini has no RendererSettings section. The camA delta of
        +0.0034 (ratio 1.0053) is NOT explained by that cause, whose ratio
        the verifier measured at 1.0000 on two pairs: a second cause is live,
        and the first frame after the scene build is a candidate, not a
        finding. NEXT STEP, THE CHEAPEST DECISIVE MEASUREMENT: one diagnostic
        run with the anti-aliasing method set to none for the probe, the
        method printed on the scene line so the run says what it rendered
        with, the same shot list, its frames neither judged nor captioned;
        read rigDiffPixels and rigMeanLumaDelta. Zero pixels differing proves
        the count is AA and the acceptance above becomes reachable by pinning
        the method; a surviving delta on camA has the second cause. The
        acceptance is then set from that printed series, never loosened by
        prose. Needs 290 first so the repeat frame can be opened. Whether
        "one picture" for JUDGING means pixel-identical or within the null
        floor is Jafar's, on the card the ruling dictates.

## 9. Conditions of landing tonight, in order

1. The reference-cell guard added to both suites (section 3, last paragraph);
   both suites run on the UNMOVED JSON; the FAILED line printed (rejecting
   case on live data).
2. Section 3's five numbers and section 8's note edits applied;
   `vignette-pieces.json` regenerated through the emitter; both suites run:
   the guard green; 3422 green; 3463 green with
   `nullSpreadMeanLuma=0.0015/max=vign_fog_maxop0100`; `nullSeriesIds`
   printed as the nine of section 3; "counted independently: largestGroup=9".
   CoreTests and vignette-spec-test counts printed with the delta named.
3. Section 8 items 6 to 11 applied; docs-check green, which requires 287 to
   290 to exist first, and THAT IS THE GATE WORKING.
4. `python3 ledger/verify.py` green, footer FROM THE FILE.
5. Commit, with the paragraph in section 11; sha captured; dispatch; watched
   by ancestry; landing read per section 6's restated item 6.
6. The frame to Jafar per the 16:25Z ruling's item 7, unchanged, with the
   card of section 13 riding it, Producer's channel.

## 10. The quality ladder at close

First working, and named as such: the twins follow the judged row by hand
(five copies edited under a ruling) with a guard that catches the next
divergence. The next rung is a spec whose twin rows DERIVE from the judged row
rather than copy it, so a fog move cannot leave a stale copy at all; that rung
is not taken tonight because A4's "every field required, no defaults" was a
deliberate two-engine contract and loosening it is a Core question for 285's
landing director, who will also have the settled fog value in hand. The floor
itself, nine samples at the shipped condition with the judged frame first and
the null repeat last, is the best available reading this rig can give; the
rig's own repeat is queue 235's, and section 13 says what it does and does not
license.

## 11. For the commit message

The judged day row moved to fog_max_opacity 0.100 under the 16:25Z ruling and
the null series stayed at 0.450, because the five rows that share the judged
cell (the grid's reference cell, its null repeat and the three wetness rows)
carry a literal copy of the old value and nothing derives them; the hook guard
went red exactly as designed, reporting that the frame Jafar judges had walked
out of its own noise floor, while the derived-list guard moved with the data.
Ruled 18:23Z (decision-2026-09-14-ruling-the-null-series-follows-the-judged-
row.md): the reference cell is the reference BECAUSE it carries the judged
row's inputs, so those five rows follow the judged row to 0.100; no guard is
re-anchored, no bound moves, no instrument changes; a guard that the reference
cell equals the judged row lands in both suites, red on the pre-move tree and
green after; the discovered group is nine in shot order with the null repeat
last, as the pin ruling predicted; item 6's "asked beside read on all seven
fog rows" is restated, since fogMaxOpacityRead is one run-level last-wins read
and no shot line carries it (queue 287); and two rig-instrument faults a
verifier found are filed as 289 and 290 with 235 given its next measurement.

## 12. Refused

- Re-anchoring any guard's literal id from the grid's reference cell to the
  judged row. The literal is right; the data was stale.
- Loosening the 0.0015 prefix, the exact-list comparison, or the null-last
  check to make either red go away.
- A second group on the line tonight (route D), and any new instrument.
- Moving the eleven other grid cells tonight, or retiring them: 285's landing.
- A separate wetness item: 186 is the item and says why it must not be split.
- Any sentence saying the fog rows' caps were "verified asked beside read" on
  any past run. They were not, on any run, and the record now says so.
- Any comparison of a fixture number with a rendered one under one name.
- Writing "the null series supersedes rigDeterminism" into any record as a
  ruling before Jafar has answered the card in section 13.

## 13. Material that arrived while this was being written: the rig's own repeat, and what the null series licenses

VERIFIED HERE, not taken from the verifier: verdict line 141 says of
`rigDeterminism` "There is no epsilon: identical inputs must be the same
picture"; line 323 reads `rigDeterminism=DIFFERS rigRepeatOf=vign_camA_day
rigRepeatAfterShots=37/37 rigDiffPixels=784509/921600
rigMaxAbsChannelDiff=43/255 rigMeanLumaDelta=+0.0034 rigMeanLumaRatio=1.0053`.
`FrameStats.h` 316 to 320, written for the light probe in the same header,
already says "Temporal antialiasing and dither move pixels by a code value or
two on their own, which is why the caller is expected to run a CONTROL probe
that toggles nothing: the control's histogram is this run's own noise floor
and no invented epsilon is needed." Nothing under `ue-probe/`, `tools/` or
`.github/` sets an anti-aliasing method, TSR, TAA, jitter or screen
percentage (zero hits, my grep), and `ue-probe/Config/DefaultEngine.ini` (30
lines) has three sections and no RendererSettings. So the project's own light
probe knows AA moves pixels and measures a control; the rig repeat asserts
zero on principle. That inconsistency is verified. The verifier's histogram,
gradient correlation and shift test are NOT verified here and are named as
the verifier's.

WHAT THE VERIFIER'S CAUSE EXPLAINS AND WHAT IT DOES NOT. Sub-pixel AA
sampling explains a pixel COUNT at a mean luma ratio of 1.0000, which is what
the verifier measured on two pairs. Line 323's camA repeat has ratio 1.0053
and delta +0.0034, seventeen times the nine-frame spread at cam_hook (0.0002,
line 319). The cause the verifier names does not cover that delta; a second
cause is live, and "the first frame after the scene build" is a candidate,
not a finding. Rule 3 applies to the verifier's instrument too.

THE RULING ON "SUPERSEDES". Two instruments, two questions, and the word is
refused as a ruling. The null series is the instrument that licenses this
run's NUMBERS: a measured floor against a measured step, three statistics,
CLEAR 3 of 3 on `32bae70` with margins of 148 (0.0296 over 0.0002), 52
(0.0620 over 0.0012) and 4.5 (0.0036 over 0.0008), the last being the one
that fails first if anything moves, written here so nobody celebrates the
first two. `rigDeterminism` is the instrument behind D31 step 1, "nothing is
judged until two photographs of one scene are one picture", which is Jafar's
rule; whether "one picture" means pixel-identical or within a measured spread
is his to define and not this director's to reword. The 16:25Z arrangement
stands: the frame goes to him labelled with the rig line, and judging is his.
What this ruling ADDS is the finding and the cheapest decisive measurement,
dictated into queue 235 (section 8 item 11), which the 16:25Z ruling made the
owner of the rig's self-difference. Nobody writes "the null series supersedes
the rig repeat" into a record until he has answered.

THE CARD, Producer's channel, riding the frame of item 7, one paragraph: "one
picture" is defined today as pixel-identical; the rig cannot reach it while
the anti-aliasing jitter is unpinned, and the project's own light probe
already measures a control instead of asking for zero; a diagnostic run under
235 will say whether pinning the method reaches zero; the question for him is
whether "one picture" for judging means pixel-identical (then the method is
pinned for the probe) or within the null floor on the three statistics (then
the floor is the gate). No default is chosen for him.

WHICH COMPARISON THE FLOOR LICENSES, the coordinator's stronger argument for
two groups, answered. A floor licenses the comparisons made at its condition
and camera. After section 3 the nine sit at the shipped condition, so the
floor licenses the judged frame against the sheet, the fog series and the
cross rows, and the null pair is inside it. The eleven 0.450 grid cells carry
NO identical-input pair from this dispatch on, so no cell of that grid may be
quoted from a future run; its `32bae70` reading stands on its own CLEAR floor.
If 285's landing keeps the 0.450 grid alive for reading, route D (a second
group on the line, a widening) is the shape to take then, and this is the
trigger.

TWO INSTRUMENT FAULTS, VERIFIED AND FILED. `VignetteShot.cpp` 2829 sets
`OfShots = GSpec.Shots.size()` and passes it as BOTH `ShotsBetween` and
`ShotsAsked` to `RigDeterminismLine` (`FrameStats.h` 966 to 968) at all five
call sites (2833, 2842, 2848, 2856, 2863), so `rigRepeatAfterShots` can only
ever print N/N and cannot see a repeat that fired early: one variable printed
twice, the instruments rule's own example. And `Finish()` (2345 to 2354)
deletes `kRepeatPngLeaf` at 2352 before CI can stage anything, under a
comment calling it scratch, so the frame behind `rigDiffPixels=784509/921600`
cannot be opened by anyone: rule 12. Front matter for both is in section 8
item 10.

QUEUE: 289 rigrepeataftershots-is-one-variable-printed-twice
QUEUE: 290 the-rig-repeat-frame-is-deleted-before-anyone-can-open-it
QUEUE: 235 the-exposure-snap-did-not-settle-the-rig

## CORRECTION 2026-09-14, by the resident, to a quotation and not to a ruling

This record attributes to Jafar the sentence "nothing is judged until two
photographs of one scene are one picture" and calls it his own rule. HE DID NOT
WRITE THOSE WORDS. Grepped across the tree: the phrase appears in no decision
record of his and nowhere in `ledger-v2/respec/decision-register/D31-the-visual-path.md`.
What D31 says, in its Pace section, is "Step 1 is the one exception and it gates
only the judging: the work continues while the rig is made deterministic, and
nothing is judged until it is." The "one picture" phrasing is THE INSTRUMENT'S,
from the verdict key `rigRule=identical-inputs-must-be-the-same-picture`.

THE SUBSTANCE IS UNHARMED and neither ruling changes: D31 does hold the judging
until the rig is deterministic, which is what both rulings rest on. The reason
this is worth a correction is the card. The card sent to Jafar on 2026-09-14
asks him to define this very wording, and handing him a phrase he never used,
labelled as his, pre-loads the question he is being asked. The card was
rewritten before it sent to quote D31's recorded words and to ask what
DETERMINISTIC means, which is the real question: he said deterministic, the code
chose pixel-identical, and whether those are the same thing is his to say.

CLAUDE.md rule 1: when a claim turns out false, grep for the SENTENCE and not
the site. Done. The phrase sits in exactly two records, this one and the other
ruling of the same day, and both now carry this note.

<!--RULING spawn=2026-09-14T18:23:24Z-->
