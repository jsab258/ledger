# Ruling, 2026-09-14 (20:01Z): the reference cell is the grid's cell at the judged row's sky and sun, so the role moves to grid_sky070_sun003 and the twins follow the judged row again

STATUS: LOG, 2026-09-14. NOT CURRENT once the dispatch carrying sky 0.70 has
landed; from then the verdict file, the two test suites, the spec notes and
queue 285, 293 and 294 are the reading copies and this is the record of what
was ruled and why.

Director ruling on one question, escalated by the resident as a simulation-
adjacent instrument cascade: Jafar's ruling ("Sky 0.70 at fog 0.100 is taken.
Apply it as the value and continue") moves `overcast_day`'s `sky_intensity`
from 1.00 to 0.70, and the reference-cell guard added at 18:23Z asserts that
`grid_sky100_sun003` equals `overcast_day` in every field that lights a frame,
sky included. Jafar's value is not revisited here. No code was written by this
director and this director has no shell. Every number below was read off the
file and line it names in this session, or is arithmetic shown in full.

Author: tier-1 director, stamp at the foot naming row 605 of
`.claude/agent-log.tsv` (`2026-09-14T20:01:27Z` TAB `studio-director`,
agentId `ab80710cc50cca499`). Row 606 (`systems-builder`, 20:01:51Z) is not
claimed. The resident reconciles the stamp against what the gate prints.

## 0. What was opened

`ue-probe/tests/vignette-spec-test.cpp` 296 to 367, 440 to 679, 726 to 750,
3354 to 3439, 3450 to 3479, 3519 to 3590, 3685 to 3693;
`ue-probe/Source/LedgerProbe/Public/VignetteSpec.h` 2530 to 2629, 2760 to
2847, and the grep hits at 245, 257, 505, 2536;
`ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp` 185 to 191 and 1494 to
1502 by grep; `ledger/CoreTests/Program.cs` 19702 to 19740, 19831 to 19879,
19961 to 19982, 19994, 20029 to 20090, 20113 to 20136, 20205 to 20249;
`production/specs/vignette-scene.json` every condition's `id`,
`sky_intensity`, `fog_max_opacity` and `exposure_pin` (33 conditions), the
notes at 895, 940, 970, 1105, 1255, 1330, and the shots at 1380 to 1422;
`production/d1-probe/ue-vignette-verdict.txt` line 1 (`622bc39`), 186, the
shot lines 189 to 230 by key, and 325 by key; the 18:23Z ruling whole; queue
285, 286, 287 (head) and the README; `rulings-log.md` 236 to 265;
`.claude/agent-log.tsv` 595 to 606. The grep for `grid_sky100_sun003` across
the tree outside `production/d1-probe`, `game-design` and `ledger-v2`: 12
hits, all listed in section 3.

## 1. The answer in one sentence

ROUTE D EXISTS AND IT IS IN THE DATA, NOT THE CODE: the grid already holds a
cell at the judged row's new sky and sun, `grid_sky070_sun003` (spec 958 to
967), and the reference cell was never defined as "sky 1.00"; it was defined
as the grid cell that carries the judged row's inputs (18:23Z section 2: "The
reference cell was the reference BECAUSE it equalled the judged row"), and
sky 1.00 was that cell's coordinate only while the judged row stood there. So
the reference-cell ROLE moves to `grid_sky070_sun003`, whose fog follows the
judged row to 0.100 exactly as five rows followed it at 18:23Z;
`grid_sky100_sun003` goes back to being grid cell 2 of 12 at the grid's own
fog, 0.450, which is the fog it was read at on `32bae70`; the null repeat, the
three wetness rows and the four pin rungs take sky 0.70; the guard keeps every
field and gains a second planted rejection for the field that moved tonight;
no bound is loosened, no instrument is added, and every id in the file tells
the truth about the row it names.

## 2. What I verified, claim by claim

THE GUARD'S FIELD LIST AND ITS ORDER. `RefCellAgainstJudged`
(`vignette-spec-test.cpp` 314 to 367; `Program.cs` 19705 to 19740) compares
hdri, sun, lanterns, window_practicals, sun_intensity, sky_intensity,
wetness, fog_density, fog_max_opacity, exposure_pin, in that order, and
returns the FIRST field that differs with both values. So a reference cell at
sky 1.00 against a judged row at 0.70 refuses as
`sky_intensity ref=1.000000 judged=0.700000`; and a copy of a sky-0.70
reference cell planted back at fog 0.450 still refuses naming
`fog_max_opacity`, because sky is compared first and is equal. The existing
plant (647 to 657; 20047 to 20057) survives the move unchanged.

THE GRID DOES NOT CARE WHICH CELL IS THE REFERENCE. The twelve-cell check
(cpp 571 to 593; C# 19961 to 19982) counts rows whose id starts `grid_sky`
against the cross of skies {1.00, 0.70, 0.50, 0.35} and suns {3, 10, 30} on
sky and sun ALONE. It stayed green at 18:23Z when the reference cell's fog left
the grid's fog, and it stays green tonight when a different cell's fog does:
twelve ids, twelve (sky, sun) pairs, no fog in the count. `gridShotOrder`
(cpp 658 to 679; C# 20237 to 20249) reads sky per grid shot and no grid row's
sky moves. Route A as the resident framed it (the reference cell's SKY moves)
would have broken this check: eleven of twelve cells found over twelve rows.
That route is refused for that reason alone before the name is considered.

THE NULL SERIES IS DISCOVERED, AND WHERE THE LARGEST GROUP LANDS DEPENDS ON
WHICH ROWS MOVE. `NullSeriesLine` takes the largest identical-input group at
one camera (`SampleKey`, `VignetteSpec.h` 2615 to 2619, over
`AppliedFieldsUnreal` 2568 to 2588, sky included). Shot indices from 1380,
0-based: hook 4, `grid_sky100_sun003` 6, `grid_sky070_sun003` 8,
`fog_maxop0100` 19, wets 21/22/23, `fog010_sky070` 28, `pin_030` 34/35, null
42. If the judged row alone moves, the largest group is the EIGHT still at
sky 1.00 (6, 19, 21, 22, 23, 34, 35, 42) and the hook's group is two (4 and
28): the hook guard at 3544 to 3546 goes red, exactly as it did at 18:23Z.
After section 3 the largest group is NINE at sky 0.70 (4, 8, 21, 22, 23, 28,
34, 35, 42), hook first, null repeat last, no tie: the 0.450 family at (1.00,
3) is `grid_sky100_sun003` plus `fog_maxop0450`, two; `fog_maxop0100` stands
alone at (1.00, 0.100).

THE FIXTURE ARITHMETIC (3387: `0.30 + 0.20 * sky + 0.0005 * (I % 4)`). The
nine's residues are 4:0, 8:0, 21:1, 22:2, 23:3, 28:0, 34:2, 35:3, 42:2, all
four present, spread 0.0015, max at the first residue-3 frame in group order
(`vign_wet_100`), min at `vign_hook_day`; 3586 asserts only the prefix
`nullSpreadMeanLuma=0.0015/max=` and stays green. The eight of the
judged-row-alone state have residues {1, 2, 3}: 0.0010, red, queue 288's
coincidence, which is why the intermediate run in section 4 will show 3586
red for a reason that is not a fault.

THE RENDERED BASIS, OFF LINE 325 OF `622bc39`, so the floor is quoted from
the file and not from a summary. The null series is read on WHOLE-FRAME mean
luma, `band.ground.p05` and `band.ground.p50`, not on the sky band:
`nullSpreadMeanLuma=0.0002/max=vign_grid_sky100_sun003/0.5402/min=vign_grid_null_repeat/0.5400`,
`skyStepSmallestMeanLuma=0.0183/between=vign_fog010_sky050..vign_fog010_sky035`,
`nullFloorMeanLuma=CLEAR/spread0.0002/vs/step0.0183`; ground p05 spread
0.0004 against step 0.0334 (the same pair); ground p50 spread 0.0009 against
step 0.0032 (`vign_grid_sky035_sun030..vign_grid_sky050_sun030`, a 0.450
grid pair); `nullSeriesVerdict=CLEAR`, `nullSeriesClear=3/of=3`. The sky
band's insensitivity to sky at fog 0.100 (the resident's basis) is therefore
NOT a null-floor problem: the floor's statistics all move with the sky, and
the smallest steps come from the three cross rows, which is the first reason
they stay in the file tonight (section 6).

THE SHOT LINES AGREE WITH THE RESIDENT'S NUMBERS, read off lines 208 (sky
1.00), 216 (0.50), 217 (0.70), 218 (0.35), all at fog 0.100:
`band.skyCentre.p50` 0.8035 on all four; `band.skyCentre.meanLuma` 0.7979,
0.7975, 0.7976, 0.7973; `band.ground.p05` 0.2536, 0.1625, 0.2003, 0.1291;
`band.skyCentre.clipHiAny=0/23040` on all four; and on every one of those
lines `shotSkyIntensityAsked` equals `shotSkyIntensityRead`. THE SKY HAS THE
PER-SHOT READ THE FOG LACKS (queue 287), so the landing can verify the sky
took on every row of the nine rather than inferring it from a band.

THE ROWS ASSERTED EQUAL TO THE JUDGED ROW, and by which suite. The four pin
rungs: `Program.cs` 19852 to 19879 compares each `pin_*` row except the night
setter to `overcast_day` in every field INCLUDING `SkyIntensity` (19866) and
asserts 4 of 4 matching; the C++ suite has no twin of this check (grep
`pin_030`: only the exposure-line fixture at 4111 to 4122). The three cross
rows: cpp 726 to 750 and C# 20113 to 20136 compare each `fog010_sky*` row to
`overcast_day` in every field BUT sky and require fog 0.100 and the three
skies present; nothing requires a cross row's sky to DIFFER from the judged
row's, so `fog010_sky070` becoming the judged row's exact twin keeps both
green. The day-sky value: cpp 554 to 555 asserts `DaySky` is 1.0 under the
sentence "carries the retired sun literal and day sky constant unchanged";
grep for `retired sun literal` and `SkyIntensity - 1\.0\)` in `Program.cs`
found no C# twin, and the resident greps `1\.00\)` beside `overcast_day` in
`Program.cs` before claiming there is none. The null cell: cpp 599 to 617 and
C# 19984 onward compare `grid_null_repeat` to the row found by the literal
`grid_sky100_sun003`.

WHAT IS NOT A DERIVATION. There is no code that derives the reference cell
from the judged row; the literal id is typed in six places in the C++ suite
and two in C# (section 3). Route D in the code, as the resident hoped, does
not exist; route D in the data does.

## 3. The ruling

THE VALUE. `production/specs/vignette-scene.json`, `overcast_day` (883)
`sky_intensity` 1.00 to 0.70. Jafar's, off row `vign_fog010_sky070` on
`622bc39` (verdict line 217): `band.skyCentre.p50` 0.8035 against the sheet's
0.808, `band.ground.p05` 0.2003 against its 0.1935, `band.skyCentre.meanLuma`
0.7976. Frame `production/d1-probe/ue-vign_fog010_sky070.png`.

THE REFERENCE-CELL ROLE MOVES TO THE GRID'S CELL AT THE JUDGED SKY AND SUN.
`grid_sky070_sun003` (958) `fog_max_opacity` 0.450 to 0.100; sky 0.70, sun
3.0, wetness 0.60, fog_density 0.0120, exposure_pin 0.300, lanterns off,
practicals off, hdri unchanged: it then equals `overcast_day` field for field.
`grid_sky100_sun003` (928) `fog_max_opacity` 0.100 to 0.450: it stops being
the reference cell, returns to the fog its eleven siblings carry and the fog
it was read at on `32bae70`, and its name is true again. Its sky stays 1.00.

THE TWINS FOLLOW THE JUDGED ROW, sky 1.00 to 0.70, fog unchanged at 0.100:
`grid_null_repeat` (1093), `wet_000` (1258), `wet_060` (1273), `wet_100`
(1288), `pin_003` (1303), `pin_030` (1318), `pin_300` (1333), `pin_1000`
(1348). Eight rows, one number each. `pin_setter_night` (1363, sun off, sky
0.35, fog 0.450) is a night row and does not move. `wet_night` is not touched.

WHAT STAYS. The seven `fog_maxop*` rows stay at sky 1.00: their series was
read on `622bc39` (queue 285 status, seven values in cap order, strictly
decreasing) and the fog was chosen from it; a series re-lit after its reading
is a different series wearing the old name. `fog010_sky035`, `fog010_sky050`
stay: section 6. `fog010_sky070` stays: it is now the judged row's own point,
the office `fog_maxop0100` held for the fog series until tonight. The eleven
grid cells other than `grid_sky070_sun003` stay at 0.450 in this dispatch,
and section 6 decides their future.

THE LITERAL RE-ANCHORS, EVERY COPY, WITH THE GREP COUNT IN THE COMMIT
MESSAGE. `grid_sky100_sun003` outside the verdict, the records and
`ledger-v2` has 12 hits. Eight are code and change to `grid_sky070_sun003`
(or `vign_grid_sky070_sun003` where the shot id is meant):
`vignette-spec-test.cpp` 603 (the null-cell lookup), 633 (the nothing-measured
message), 3454 (comment), 3463 (the derived anchor), 3526 (the printf label),
3553 (`bRefIn`, shot id); `Program.cs` 19994 (the lookup), 20033 (the
message). One is a comment that becomes past tense: `Program.cs` 20219 to
20225 ("its twin grid_sky100_sun003 is shot 7 of 43, THIRTY SIX SHOTS APART")
becomes "its twin grid_sky070_sun003 is shot 9 of 43, THIRTY FOUR SHOTS
APART". One is historical and stays: `VignetteSpec.h` 2534 to 2539 names the
seven of 25 the review found and says "Seven is a reading, never a constant".
Two are `vignette-pieces.json` 28 and 66, regenerated through the emitter,
never edited by hand. Queue 235 line 86 quotes a verdict and stays.

THIS IS NOT THE RE-ANCHORING THE 18:23Z RULING REFUSED. That ruling's route A
was to anchor the derivation to `overcast_day` itself, which would have let a
stale null repeat at 0.450 sit unseen while the guard read the judged row
against the judged row. Tonight the anchor stays a GRID CELL that must equal
the judged row, the null repeat must equal that cell, the wets and pins are
compared to the judged row in their own checks, and a stale copy anywhere in
the family still goes red. The claim is unchanged; the literal that names its
subject follows the definition the 2026-09-09 grid ruling gave it.

THE GUARD KEEPS EVERY FIELD AND GAINS THE PLANT THE SKY OWES. `sky_intensity`
does not leave the field list (route C, refused: a guard that cannot see the
field that moved tonight is a guard that has stopped reading). In both suites,
after the existing fog plant (cpp 647 to 657; C# 20047 to 20057), a second
plant in the same shape: a copy of the parsed reference cell with
`SkyIntensity` set back to 1.00, run through the same comparison, expected to
refuse naming `sky_intensity` and both values, the sentence: "and the
comparison refuses a reference cell planted back at the retired sky, naming
sky_intensity and both values". Its `nothing measured` fallback is the one
beside it. Under Jafar's no-new-instrument rule this is a Check inside a suite
that already walks these rows, in the shape of the Check beside it (the D32
shape the 18:23Z ruling used), not a tool, a reader or a gate; nothing is
retired because nothing is added.

THE DAY-SKY CHECK MOVES BY RULING, IN THE SHAPE THE FOG CHECK ALREADY HAS.
cpp 554 to 555 splits: `Check(std::fabs(DaySun - 3.0) < 1e-9, "the day
condition carries the retired sun literal unchanged")` and
`Check(std::fabs(DaySky - 0.70) < 1e-9, "the judged day row's sky is 0.70,
moved by the ruling of 2026-09-14 20:01Z from the sky cross on 622bc39, row
vign_fog010_sky070")`, with the comment at 549 to 553 gaining: "The sky moved
on 2026-09-14 (ruling of 20:01Z): a RENDERED cell, vign_fog010_sky070 on
622bc39, verdict line 217, band.skyCentre.p50 0.8035 against the sheet's
0.808 and band.ground.p05 0.2003 against its 0.1935." This is a matched-set
value, not a threshold: rule 2 is satisfied because the number was printed
(line 217) and ruled before the check learned it.

## 4. Rule 5b: the accepting and the rejecting case for every guard touched, and which run proves each

TWO TEST RUNS TONIGHT, NO RENDER BETWEEN THEM. Run 1: `overcast_day` sky
0.70 applied ALONE, both suites run on that tree. Run 2: the rest of section
3 applied, both suites run again. Both outputs pasted into the commit message
in that order.

- The reference-cell guard (cpp 635 to 640; C# 20034 to 20039). Rejecting,
  on live data: run 1, FAILED with `sky_intensity ref=1.000000
  judged=0.700000`, the guard catching the exact move it was written to catch,
  two hours after it was written. Accepting: run 2, empty diff against
  `grid_sky070_sun003`. Standing rejections, watched every run: the fog plant
  (names `fog_max_opacity ref=0.450000 judged=0.100000`) and the new sky
  plant (names `sky_intensity ref=1.000000 judged=0.700000`), accepting
  printed first.
- The day-sky check (cpp 554). Rejecting: run 1, FAILED at the old 1.0
  against the moved row. Accepting: run 2 at 0.70.
- The pin rungs (C# 19876). Rejecting: run 1, "4 rungs, 0 matching the
  reference". Accepting: run 2, 4 of 4.
- The hook guard (cpp 3544). Rejecting: run 1, the hook outside the eight.
  Accepting: run 2, hook first of nine.
- `bRefIn` (cpp 3556). Accepting: run 2 with the shot id re-anchored.
  Rejecting: run 2 BEFORE the id at 3553 is changed would fail; the resident
  need not print that state, its rejecting case is unchanged from the file.
- The null-cell check (cpp 608 to 617; C# 19984 onward). Green in run 1
  (both rows unmoved), green in run 2 (both at 0.70). Its rejecting case is
  unchanged from the file.
- 3586 (the 0.0015 prefix). Run 1 red at 0.0010 for queue 288's residue
  coincidence and not for a fault; run 2 green. Named so nobody reads run 1's
  count of failures as a count of faults.
- The twelve-cell check and `gridShotOrder`, both suites: green in both runs;
  no grid row's sky moves.

Run 1's expected reds, counted: cpp 554, 635, 3544, 3586; C# 20034, 19876.
Six, all named above with their reason. A seventh red is a finding.

## 5. The routes, costed against the file

- A (the resident's): `grid_sky100_sun003` takes sky 0.70 and is renamed.
  Its name would lie until renamed, and any rename either collides with
  `grid_sky070_sun003` or leaves the twelve-cell check at eleven of twelve.
  REFUSED; what survives of it is the principle, applied to the right cell.
- B: a new twin row is added and the guards re-anchor to it. Eight literal
  re-anchors, one row added, and the sky-1.00 family left at fog 0.100 as a
  larger identical-input group than the judged row's, so the hook guard stays
  red unless those rows also move. Route A of 18:23Z in the data. REFUSED.
- C: `sky_intensity` leaves the field list. A guard blind to the field that
  moved tonight. REFUSED, as the resident asked.
- D in the code: not there; the anchor is a typed literal in eight places.
- D in the data, this ruling: one cell's fog to 0.100, one cell's fog back
  to 0.450, eight skies to 0.70, eight literals, one value check moved by
  ruling, one plant per suite, notes corrected. Zero rows added or removed,
  43 shots stay 43, the twelve-cell check untouched, every id true.

## 6. The pins, the fog series, the cross rows, and the grid

THE FOUR PIN RUNGS FOLLOW, and the check that says so already exists (C#
19852 to 19879): a rung is the judged day cell in every field but the pin,
and a rung left at sky 1.00 would report the exposure of a street the judged
frame no longer shows. Their notes gain one sentence (section 8).

THE THREE CROSS ROWS ARE SUPERSEDED AS A SERIES AND RETAINED AS SAMPLES, and
those are two different statements. As a series they are read: `622bc39`
answered what they were built to ask and Jafar chose from the answer. As
rows they do two jobs tonight that nothing else does. `fog010_sky070` is the
judged row's own point in the sky series, a ninth null sample at the shipped
condition, and the very row whose frame the value was taken from, so the
landing compares the judged frame to line 217 like for like.
`fog010_sky035` and `fog010_sky050` are the two frames the null verdict's
smallest sky steps were found between on `622bc39` (0.0183 on mean luma,
0.0334 on ground p05, line 325); remove them and the steps are found among a
sparser set. They leave the file with the grid under queue 293, not tonight.

THE GRID RETIRES RATHER THAN MOVES, and this is the decision the 18:23Z
ruling reserved for "queue 285's landing ruling, when the fog value is
settled". It is settled, and the sky with it. Moving twelve cells to fog
0.100 would re-run a sky-by-sun grid at a cap where the sky band does not
answer to sky (lines 208, 216 to 218: p50 0.8035 at all four skies) to
choose a cell that has just been chosen; nobody asked for a sun series at
0.100, and Jafar's word was "continue". Every grid note and both suites (cpp
444 to 446) say a one-run probe row "is removed by the item that reads this
run"; the grid was read on `32bae70`, the fog and sky series on `622bc39`,
and none of the reading items removed its rows. Queue 293 is that clause
enforced, once, for all three series, with the reference cell taking a name
that is not a grid cell's when its grid goes. It is not tonight's work: it
removes rows, checks and counts in both suites and wants a landing director
with the render to hand, and the rows cost this dispatch nothing but shots.

QUEUE 286 IS TOUCHED BY THE SAME MOVE. Its spec says the Mie series is
printed "at fog 0.100 and sky 1.00"; the judged sky is 0.70 from this
commit, and a series at 1.00 would be a series about the retired street.
One correction to its text (section 8), no new item.

## 7. The landing read, so the next director reads the run and not the colour

The sha captured before dispatch, the run watched by ancestry. On landing:
(a) `nullSeriesIds` equal to the nine of section 2 in shot order,
    `first=vign_hook_day`, `last=vign_grid_null_repeat`,
    `nullSeriesTiedGroups=0`; the verdict word read, and NO-READ escalated
    per C4 rather than quoted around;
(b) THE SKY TOOK, PER ROW: `shotSkyIntensityAsked=0.700` beside
    `shotSkyIntensityRead=0.700` on all nine shot lines, which the sky can
    say and the fog cannot (line 216 to 218 carry the keys today);
(c) THE FRAME ANSWERS: the nine's `band.ground.p05` beside line 217's 0.2003
    with residuals stated and NO bound, and named as NOT near line 208's
    0.2536, which is where a sky that did not take would sit;
    `band.skyCentre.p50` printed but NOT read as confirmation, because it
    reads 0.8035 at sky 1.00 and at 0.70 alike and cannot tell the two apart;
(d) the floor's three statistics beside `622bc39`'s 0.0002, 0.0004, 0.0009
    and their steps 0.0183, 0.0334, 0.0032, residuals stated, no bound;
(e) the sky line's `fogMaxOpacityRead` still 0.100, the null repeat's cap,
    one per run, last-wins.
Then the frame to Jafar per the 16:25Z ruling's item 7, Producer's channel,
labelled with the rig line and with the value he chose named as his.

## 8. Dictated text

Every replacement verbatim; where a sentence is replaced, grep the sentence
and replace every copy (rule 1), counts into the commit message.

1. `overcast_day` note (895), appended: "sky_intensity 0.70 taken by Jafar
   on 2026-09-14 ('Sky 0.70 at fog 0.100 is taken. Apply it as the value and
   continue'), recorded in decision-2026-09-14-ruling-the-reference-cell-is-
   the-grid-cell-at-the-judged-sky.md, off the sky cross on 622bc39, row
   vign_fog010_sky070 (verdict line 217): band.skyCentre.p50 0.8035 against
   the sheet's 0.808, band.ground.p05 0.2003 against the sheet's 0.1935,
   band.skyCentre.meanLuma 0.7976. At this fog cap the sky band does not
   answer to sky_intensity (p50 0.8035 at 0.35, 0.50, 0.70 and 1.00, lines 208
   and 216 to 218, clipHiAny 0/23040), so this value is a ground reading and
   is read on band.ground.p05."
2. `grid_sky070_sun003` note (970), appended: "SINCE 2026-09-14 20:01Z THIS
   IS THE GRID'S REFERENCE CELL, because the reference cell is the grid cell
   that carries the judged row's inputs and the judged row now stands at sky
   0.70, sun 3. FOG CAP MOVED 0.450 TO 0.100 the same evening for that
   reason (decision-2026-09-14-ruling-the-reference-cell-is-the-grid-cell-
   at-the-judged-sky.md); its 32bae70 and 622bc39 frames were at 0.450 and are
   not comparable to what it renders from this commit. grid_null_repeat
   duplicates this row field for field and is shot last; both suites assert
   the duplicate and assert that this row equals overcast_day in every field
   that lights a frame."
3. `grid_sky100_sun003` note (940), appended: "REFERENCE-CELL ROLE MOVED TO
   grid_sky070_sun003 ON 2026-09-14 20:01Z when the judged row's sky went to
   0.70: a reference cell is the grid cell at the judged row's sky and sun,
   and this cell is not that any more. FOG CAP RETURNED 0.100 TO 0.450 in the
   same change, the grid's own fog and the fog this cell was read at on
   32bae70. It is grid cell 2 of 12 and nothing else, and it leaves with the
   grid under queue 293."
4. `grid_null_repeat` note (1105): "Every field is a character-for-character
   duplicate of grid_sky100_sun003, the grid's reference cell" becomes
   "Every field is a character-for-character duplicate of the grid's
   reference cell, grid_sky070_sun003 since 2026-09-14 20:01Z and
   grid_sky100_sun003 before that"; "its twin grid_sky100_sun003 is shot 7
   of 43, so the two are thirty-six shots apart" becomes "its twin
   grid_sky070_sun003 is shot 9 of 43, so the two are thirty-four shots
   apart"; "the twin is shot 7 of 43 and this row 43 of 43, thirty-six shots
   apart" becomes "the twin is shot 9 of 43 and this row 43 of 43,
   thirty-four shots apart"; appended: "SKY MOVED 1.00 TO 0.70 ON 2026-09-14
   20:01Z with the judged row and the new twin."
5. `wet_000`, `wet_060`, `wet_100` notes: "(sky 1.00, sun 3, fog_max_opacity
   0.100 since 2026-09-14)" becomes "(sky 0.70 since 2026-09-14 20:01Z, sun
   3, fog_max_opacity 0.100 since 2026-09-14)"; appended: "SKY MOVED 1.00 TO
   0.70 ON 2026-09-14 20:01Z for the reason the fog moved: this row is the
   judged row at one wetness, and its sky was a copy."
6. `pin_003`, `pin_030`, `pin_300`, `pin_1000` notes, appended: "SKY MOVED
   1.00 TO 0.70 ON 2026-09-14 20:01Z under decision-2026-09-14-ruling-the-
   reference-cell-is-the-grid-cell-at-the-judged-sky.md, for the reason the
   fog moved: a rung is the judged day cell in every field but the pin, and
   ledger/CoreTests asserts it against overcast_day sky included. THE PIN
   ITSELF IS STILL UNTOUCHED."
7. `fog010_sky070` note (1255), appended: "SINCE 2026-09-14 20:01Z THIS ROW
   IS THE JUDGED ROW'S OWN POINT: Jafar took sky 0.70 at fog 0.100 off this
   row's frame on 622bc39 (verdict line 217, ue-vign_fog010_sky070.png), so
   it repeats the value in force, is a null sample of the street that ships,
   and is the like-for-like reference the judged frame is read against on
   the next landing. The series it belongs to is read; it leaves with its two
   siblings under queue 293."
8. The four fog notes carrying it (1120, 1135, 1150, 1165): "when the judged
   row moved to 0.100 and fog_maxop0100 became the row that repeats it."
   becomes "when the judged row moved to 0.100 and fog_maxop0100 became the
   row that repeats it; fog_maxop0100 repeated it until 20:01Z the same day,
   when the judged row's sky moved to 0.70 and fog010_sky070 became that row.
   This series stays at sky 1.00, the sky it was read at on 622bc39, and
   leaves the file under queue 293."
9. `VignetteShot.cpp` 187 to 191: "carried unchanged into overcast_day and
   wet_night" becomes "carried unchanged into overcast_day and wet_night on
   9 September; overcast_day's moved to 0.70 on 2026-09-14 by Jafar's ruling
   off the sky cross on 622bc39 (decision-2026-09-14-ruling-the-reference-
   cell-is-the-grid-cell-at-the-judged-sky.md)".
10. The 18:23Z record, a block inserted BEFORE its stamp line (714 today):

        ## CORRECTION 2026-09-14, 20:01Z

        Section 3 and section 8 item 1 make `grid_sky100_sun003` follow the
        judged row. It did, for the fog, and two hours later the judged
        row's sky moved to 0.70 (Jafar), where the grid already holds a
        cell, `grid_sky070_sun003`. Ruled 20:01Z in
        `decision-2026-09-14-ruling-the-reference-cell-is-the-grid-cell-at-the-judged-sky.md`:
        the reference cell is the grid cell at the judged row's sky and sun,
        so the role moved to `grid_sky070_sun003` (fog to 0.100),
        `grid_sky100_sun003` returned to 0.450, and the null repeat, the
        wets and the four pin rungs took sky 0.70. The expected group is
        nine with `vign_grid_sky070_sun003` and `vign_fog010_sky070` in and
        `vign_grid_sky100_sun003` and `vign_fog_maxop0100` out. "Whether the
        eleven 0.450 grid cells move or retire" is decided there: retire,
        queue 293.

11. `rulings-log.md`, one line after line 245, in the file's form:

        - **2026-09-14** the reference cell is the grid cell at the judged
          row's sky and sun: Jafar's sky 0.70 applied; the role moves to
          `grid_sky070_sun003`, the null repeat, wets and pin rungs follow;
          the guard keeps every field and gains the sky plant; the read
          series retire (293) and the twins' derivation is filed (294)
          `game-design/decision-2026-09-14-ruling-the-reference-cell-is-the-grid-cell-at-the-judged-sky.md`

12. Queue 285, a paragraph appended to its status: "RULED 2026-09-14 20:01Z
    (decision-2026-09-14-ruling-the-reference-cell-is-the-grid-cell-at-the-
    judged-sky.md): Jafar took sky 0.70 at fog 0.100 off this series ('Sky
    0.70 at fog 0.100 is taken. Apply it as the value and continue'). The
    last clause of this item's acceptance is met when the dispatch carrying
    sky 0.70 lands and the note on overcast_day names run, commit and rung;
    this item moves to done/ on that landing, and its rows leave under 293."
13. Queue 286, in its spec: "at fog 0.100 and sky 1.00" becomes "at fog
    0.100 and the judged sky, 0.70 since 2026-09-14 20:01Z (a series at 1.00
    would be about the retired street)".
14. The two queue items, front matter per `production/queue/README.md`:

        293-the-read-series-leave-the-file.md
        line: engine (production/specs/vignette-scene.json and both suites)
        spec: every note on the grid, the fog series and the sky cross says
          "the item that reads this run removes it in the same change", and
          vignette-spec-test.cpp 444 to 446 says the same; the grid was read
          on 32bae70, the fog series and the cross on 622bc39, and none of
          the reading items removed a row. Retire, not move: the eleven grid
          cells other than the reference cell, the six fog rungs not in
          force (0.450, 0.250, 0.080, 0.050, 0.020, 0.000) and the two cross
          rungs not in force (0.35, 0.50), with their shots. The reference
          cell keeps its row under a name that is not a grid cell's (the
          landing director names it) and both suites' literal follows it
          ONCE. fog_maxop0100 and fog010_sky070 are decided by the landing
          director: each is the judged row's own point in a retired series.
          Checks that count the retired rows (twelve cells, gridShotOrder,
          the seven-value fog check, the cross check, the 33/26/5 count)
          go with the rows or are restated to what remains. The wetness trio
          stays (queue 186) and the pin rungs stay (queue 235).
        acceptance: both suites green on the reduced file with the counts
          printed; a committed run whose nullSeriesIds is the judged group
          in shot order, hook first and null repeat last, on the shorter
          shot list; the null verdict read, and the sky step's denominator
          printed so a NO-READ or nothing-measured is named rather than
          quoted around.
        max_sessions: 1
        status: READY 2026-09-14, filed by the ruling of 20:01Z, which is
          queue 285's landing ruling and decides retire over move. Not
          blocking; lands with the next batch that touches the spec, under
          a director because it changes counts in both suites.

        294-the-judged-rows-twins-derive-and-do-not-copy.md
        line: engine (Core question: the spec's two-engine contract)
        spec: twice on 2026-09-14 (fog at 18:23Z, sky at 20:01Z) the judged
          row moved and the rows whose only job is to carry its inputs kept
          a stale literal, because A4 made every field required with no
          defaults and the twins are copies. Section 10 of the 18:23Z ruling
          named the next rung and deferred it. Decide the shape: a
          `same_as` reference resolved by both readers, or an emitter step
          that writes the copies from the judged row before either reader
          sees the file; keep A4's "every field written out" for the
          rendered file either way. The reference-cell guard and the pin,
          wet and null-cell checks stay as the proof the derivation worked.
        acceptance: a decision record naming the shape and its cost in both
          readers; then, if built, both suites green with the guards
          unchanged, and one planted stale copy in each reader refused by
          name.
        max_sessions: 1
        status: READY 2026-09-14, filed by the ruling of 20:01Z. Not
          blocking. A director's item, because it touches the spec contract
          both engines read.

## 9. Conditions of landing tonight, in order

1. `overcast_day` sky 0.70 alone; both suites run; the six expected reds of
   section 4 printed with their text (run 1, the rejecting cases on live
   data).
2. The rest of section 3: the two fog numbers, the eight skies, the eight
   literals, the C# comment, the day-sky check, the sky plant in both suites;
   `vignette-pieces.json` regenerated through the emitter; both suites run
   (run 2): everything green, `nullSeriesIds` the nine in shot order,
   `derived from grid_sky070_sun003` printed, "counted independently:
   largestGroup=9", both plants printed with the field each names. Counts
   printed with the delta against tonight's earlier run named.
3. Section 8 items 1 to 13 applied; 293 and 294 created; docs-check green.
4. `python3 ledger/verify.py` green, footer FROM THE FILE.
5. Commit with the paragraph in section 11; sha captured; dispatch; watched
   by ancestry; landing read per section 7.
6. The frame to Jafar, Producer's channel, per the 16:25Z item 7.

## 10. The quality ladder at close

First working, and named as such: the second hand-moved twin family in one
evening under a ruling, with a guard that now plants both fields that have
gone stale. The next rung is 294, the twins deriving from the judged row so
a value move cannot leave a copy behind; two incidents in three hours are the
evidence it is due, and it is a Core question because of A4. The rung after
that is 293, at which the reference cell stops wearing a grid name and the
file stops rendering seventeen frames nobody reads. The floor itself, nine
samples at the shipped condition with the judged frame first and the null
repeat last, verified per row by the sky's own asked-beside-read, is the best
available reading this rig can give.

## 11. For the commit message

Jafar took sky 0.70 at fog 0.100 off the sky cross rendered on 622bc39 (row
vign_fog010_sky070, verdict line 217: sky p50 0.8035 against the sheet's
0.808, ground p05 0.2003 against 0.1935), and applying it moved overcast_day
out of the grid's reference cell two hours after a guard was written to
notice exactly that; run 1 of the suites shows it noticing, naming
sky_intensity 1.000000 against 0.700000. Ruled 20:01Z
(decision-2026-09-14-ruling-the-reference-cell-is-the-grid-cell-at-the-judged-
sky.md): the reference cell is the grid cell at the judged row's sky and sun,
which the grid already holds, so the role moves to grid_sky070_sun003 (fog to
0.100), grid_sky100_sun003 returns to the grid's 0.450, and the null repeat,
the three wetness rows and the four pin rungs take sky 0.70; the guard keeps
every field, its literal follows the definition in eight places, and a second
plant refuses a reference cell put back at sky 1.00; the day-sky check moves
to the ruled value in the shape of the fog check; no bound is loosened and no
instrument added. The read series (grid, fog, cross) retire under 293, the
twins' derivation is 294, and 286's series is corrected to the judged sky.

## 12. Refused

- Any id whose name says a value the row does not carry.
- `sky_intensity` leaving the guard's field list, or the guard's literal
  anchoring to `overcast_day` itself.
- Adding a row to be the twin when the grid already holds one.
- Moving the eleven grid cells or the seven fog rows to the new sky, or
  removing any row tonight.
- Reading `band.skyCentre.p50` as evidence the sky took: it cannot tell 1.00
  from 0.70 at this cap.
- A third test run for `bRefIn`'s intermediate state; its rejecting case is
  the file's.
- Any sentence saying this ruling revisits the value. It applies it.

## CORRECTION 2026-09-14, applying resident, three factual corrections

Ruled by the resident on the reading that a resident corrects a record's
factual error and never changes what was decided. THE DECISION IN THIS RECORD
IS UNTOUCHED: the end state, the values, the eight re-anchors and the guard's
field list are exactly as ruled above, and all three corrections below are to
predictions about intermediate states and to the order of operations. Every
number here was printed by a run in the applying session.

CORRECTION 1, SECTION 4 IS WRONG BY ONE AND THE COUNT IS SEVEN. Section 4
ends "Run 1's expected reds, counted: cpp 554, 635, 3544, 3586; C# 20034,
19876. Six". The true count is SEVEN. The seventh is `vignette-spec-test.cpp`
654, the fog plant written at 18:23Z, and it printed:

    FAILED - and the comparison refuses a reference cell planted back at the
    retired fog cap, naming fog_max_opacity and both values :
    sky_intensity ref=1.000000 judged=0.700000

THE GUARD IS NOT BROKEN AND THIS IS THE DISTINCTION THAT MATTERS. It still
refuses the planted cell. What fails transiently is the assertion about WHICH
FIELD the refusal names. `RefCellAgainstJudged` returns the FIRST differing
field and compares `sky_intensity` before `fog_max_opacity`, so in the
intermediate state of section 9 step 1, where the reference cell is still
`grid_sky100_sun003` at sky 1.00 while the judged row stands at 0.70, the
plant's first difference is the sky and the refusal names `sky_intensity`
rather than `fog_max_opacity`. Section 2's justification, "a copy of a
sky-0.70 reference cell planted back at fog 0.450 still refuses naming
fog_max_opacity, because sky is compared first and is equal", is TRUE OF THE
END STATE and FALSE OF THE INTERMEDIATE STATE this record's own section 9
step 1 dictates. The check returns green in run 2 by the same field order,
because the reference cell becomes `grid_sky070_sun003` at sky 0.70 and the
sky then matches; it did, and its C# twin at `Program.cs` 20054 did too.
SEVEN IS THE NUMBER THAT GOES IN THE COMMIT MESSAGE as rule 5b evidence, not
six.

CORRECTION 2, THE C# HARNESS IS FAIL-FAST, SO SECTION 4 CANNOT BE SATISFIED
AS WRITTEN AND ONE SUB-STEP IS ADDED. `Program.cs` 23 throws on the first
failed `Check`, so a run shows ONE C# red and stops. Check 19876 runs before
20034, so run 1 as dictated prints the pin-rung red and aborts, and the
reference-cell guard's own rejecting case never executes in its own engine.
Leaning on the C++ twin, which printed the identical string, would be an
argument rather than a run, and rule 5b asks for two outcomes both WATCHED.
So run 1 gained one sub-step at the cost of one suite invocation and no
render: run 1a as dictated (five reds, above), then run 1b with the seven
skies of the wets and pins applied and `grid_null_repeat` held at 1.00 beside
its unmoved twin, which clears 19876 and the null-cell check and makes 20034
the first failure. It printed:

    FAILED: the grid's reference cell is the judged day row in every field
    that lights a frame, ... - sky_intensity ref=1.000000 judged=0.700000

Then run 1c applied the two fog numbers and `grid_null_repeat`'s sky, and run
2 is green. The rejecting case of the reference-cell guard is now on the
record in BOTH engines, from live data, in the state each was written to
catch.

CORRECTION 3, SECTION 9 PUTS THE EMITTER IN THE WRONG RUN. Section 9 step 2
regenerates `production/specs/vignette-pieces.json`. It belongs in step 1 and
in every state change after it. `vignette-spec-test.cpp` 410 reads the
PIECES file and not the scene file, using the scene file only for one
provenance string, and `Program.cs` 21322 compares the committed pieces file
against a fresh regeneration byte for byte. So the dictated order would have
made run 1 show ZERO of its four predicted C++ reds, because that suite would
have read the stale sky, and would have produced an unnamed red on the drift
guard. Regenerating through the emitter at every state change, with
`--ahead-of-run cb4767e`, is the only order that produces the evidence
section 4 asks for.

THE CHECKED NEGATIVE SECTION 2 ASKED FOR: THERE IS NO C# DAY-SKY TWIN.
Established rather than assumed, so nobody re-derives it. Five greps over
`ledger/CoreTests/Program.cs`: `1\.00)` gives four hits, all unrelated (14633
and 14707 are mix and alley opens, 19111 and 19112 are sign colours) and none
beside `overcast_day`; `SkyIntensity - 1` gives nothing; `daysky` and `day
sky` case-insensitive give nothing; `retired sun literal` across the whole
tree gives one hit, `vignette-spec-test.cpp` 555. And the eight `SkyIntensity`
uses in that file are accounted for one by one, none asserting a literal for
`overcast_day`: 19724 to 19726 (`RefCellAgainstJudged`), 19866 (the pin rungs,
against `dayRef`), 19974 (the grid cross), 20006 (the null cell, against
`refCell`), 20132 (the cross rows), 20245 (`gridShotOrder`), 20262 (the
conditions print). The day-sky check therefore exists in one engine only and
nothing moved on the C# side for it.

NOT DONE, AND NAMED RATHER THAN QUIETLY SKIPPED: section 8 item 11, the
`rulings-log.md` line. That file is `ledger-v2/respec/decision-register/
rulings-log.md`, a directory the applying session was told to leave alone
because another agent held it modified in the same tree, and line 245 has
drifted under that agent's edits. The line is unwritten and its text stands
in section 8 item 11 ready to paste.

<!--RULING spawn=2026-09-14T20:01:27Z-->
