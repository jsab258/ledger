# Ruling, 2026-09-14: the prune is gone from both engines, seven residents are a floor and not a town, the fog is the cloud deck, and dusk cannot be photographed yet

STATUS: LOG, 2026-09-14. NOT CURRENT once the queue 115 batch has landed with
section 1.6 applied and the fog dispatch of section 2.5 has printed its series;
from then 115's status line, the verdict file and queue 285 are the reading
copies and this is the record of what was ruled and why.

Director ruling on two things in one spawn: the queue 115 batch (Core, and it
changes a conclusion) and the fog call that stands between Jafar and the frame
he asked for. No code was written by this director, and this director has no
shell, so every number below was read off the file and line it names, or off a
frame opened with the image reader, in this session. Nothing was run. The
builder's counts (CoreTests 4355 to 4363, soak 3 to 5, golden 2517 with 0
mismatches) are CLAIMS until `ledger/verify.py` writes a footer on the landing
tree: `ledger/.verify-footer` on disk still reads `4355 CoreTests` and `3 soak
checks`, because it is the footer of the last green run at 15:47Z, before this
batch.

Author: tier-1 director, stamp at the foot naming row 594 of
`.claude/agent-log.tsv` (`2026-09-14T16:25:22Z` TAB `studio-director`, agentId
`a037536b7a7aa7078`), the newest director row in the log. Rows 581 and 588
belong to the pin ruling and the marker ruling and are not claimed.

## 0. What was opened, so the reader knows the denominator of this record

Part one: `canon.md` 95 to 103; `ledger/Assets/Scripts/Core/MemoryStore.cs`
whole (211 lines); `ue-probe/Source/LedgerProbe/Public/MemoryStore.h` whole
(325 lines); `ledger/Soak/Program.cs` whole (511 lines);
`ledger/CoreTests/Program.cs` 265 to 410 and 1835 to 1867;
`ledger/PerceptionGolden/Program.cs` 455 to 491;
`ue-probe/Source/LedgerProbe/Public/CoreGolden.h` 180 to 224;
`ue-probe/perception-golden.txt` by grep (eight `mem_permanent` rows at 2366
to 2373, zero `mem_prune`, zero `maxEvents`); `ledger/Assets/Scripts/Core/
Gossip.cs` 355 to 414; `ledger/verify.py` 2731 to 2754 (the soak IS run at
commit, and the count is taken off the soak's own done line, which `Soak`
line 122 prints); `game-design/research/performance-budget.md` whole; D25;
D32; queue 115, 116, README; the 15:16Z ruling on 115.

Part two: `production/d1-probe/ue-vignette-verdict.txt` line 1 (commit
`32bae70`), lines 193 to 196, 204 to 210, 319 to 323; the four fog frames
`ue-vign_fog_maxop0450/0250/0100/0000.png` OPENED; `VignetteShot.cpp` 158 to
237, 1248 to 1279, 1540 to 1594, 3318 to 3341; `VignetteSpec.h` 440 to 489;
`StreetVignette.cs` 1895 to 1918; `StreetVignettePieces.cs` 395 to 424;
`StreetVignetteHost.cs` 640 to 669; `tools/frame-shadow-probe.py` 650 to 679;
`CoreTests/Program.cs` 19895 to 19944; `ue-probe/tests/vignette-spec-test.cpp`
440 to 479; `production/specs/vignette-scene.json` fog rows 1108 to 1166 and
shots 1307 to 1310; `production/findings.txt` 2815 to 2854 (the sheet's
numbers on this project's ruler); queue 180, 186, 194, 205, 206, 224, 240,
276, 282; D28, D31; the 09-09 grid ruling A4 and C11; the 14:12Z pin ruling
sections 10 to 14.

# PART ONE: THE PRUNE

## 1.1 Verified before anything else

THE CONCLUSION THAT CHANGED, and it is the largest of the day. The 600-event
cap was not a theoretical violation of canon.md line 99. `CoreTests/Program.cs`
331 to 337 carries the builder's one-run measurement: at 2,800 game-days (the
horizon `BalanceLab` already drives, `Soak` 137), seed 1, the seven agents held
3,377 events with the cap and 7,417 without. 4,040 of 7,417 destroyed, which is
54.5 percent OF THE SOAK STREET'S MEMORY. Not the town's: the town has never
been run (section 1.3). And the soak's own growth series read that street as
quiet rather than as deleting, which is the instrument reading the wrong
world.

THE PRUNE IS GONE FROM BOTH IMPLEMENTATIONS. `MemoryStore.cs` 87 to 91:
`Append` is `Events.Add(e); if (!AppendToFile(e)) Save();` and nothing else.
`MemoryStore.h` 277 to 284: `Events.push_back(E)` with the comment naming what
left. Grep over every `.cs`, `.h`, `.cpp` for `MaxEvents|PruneTo|Prune(`: three
hits, all comments (`CoreGolden.h:189`, `MemoryStore.h:13`, `:243`), plus the
transcribed fixture `PrunedLikeTheOldStore` at `CoreTests` 296 to 306, which
is the fault kept alive so the guard can be shown to catch it (rule 5b). No
live prune remains anywhere.

THE GUARD IS TESTED ON BOTH OUTCOMES, ACCEPTING FIRST. `CoreTests` 346 to 352:
901 appended, 901 remembered, `FirstMissingHour` finds no hole over 900
examined. 357 to 363: the same 901 through the transcribed old prune drop to
500 with a hole in the middle, and the day that mattered SURVIVES the prune,
which is exactly why a count-and-a-highlight could never have caught it. 368
to 372: the markdown round trip carries all 901. The check at 1845 to 1867
that used to assert `Count <= MaxEvents` now asserts 901 and no hole; the
comment says in as many words that it used to pass BECAUSE the prune fired.

THE PER-EVENT COST IS MEASURED, NOT MODELLED. `CoreTests` 313 to 325 takes a
`GC.GetTotalMemory(true)` delta between 25,000 and 50,000 retained events so
the list's own cost cancels; 389 to 391 asserts the model within one 8-byte
allocation quantum, which is a derivation about x64 rounding and not a taste,
and the code says so. `MemoryStore.cs` 97 to 103 prints the series the model
was fitted to (six text lengths, 112 to 376 bytes). The soak sums the model
PER EVENT rather than modelling the mean (`Soak` 385 to 389, 224 against 229
on the first run, the 2 percent that stepping in eights costs). At-worst, and
named at-worst, because shared strings cost less. The arithmetic checks: 1,261
events over 7 residents and 499 closed days is 0.3610 per resident per day;
300 x 2800 x 0.361 x 229 bytes is 66.2 MB; 1 GiB over 300 x 2800 x 229 is
5.58 per resident per day, 15.5x the measured mean.

THE SOAK PRINTS THE BILL AND RUNS AT COMMIT. `verify.py` 2747 runs `Soak`; its
regex takes the count off the done line. So the new gate (`Soak` 155 to 170:
no resident's count may ever fall, with the block-prune shape planted through
the same `FirstFall`) is a gate that something calls, rule 6 satisfied on the
day it lands.

ONE THING I DID NOT VERIFY AND RECORD AS THE RESIDENT'S: that `ledger/
GameCheck`'s 12 CS0117 errors pre-exist this batch. The resident names the
method (stash the batch, build HEAD), which is the right method, and the
footer at commit is what stands.

## 1.2 Question A: removal, not a cap

REMOVAL IS RIGHT, AND THE CAP BRANCH IS NOT AVAILABLE ON THE EVIDENCE. Jafar's
words are the test: "replace it with a cap derived from a measured memory cost
AT THE TOWN'S TARGET POPULATION rather than an arbitrary 600." Nobody has
measured a memory cost at 300 residents; the measurement exists at seven. A
cap derived from seven residents would be the arbitrary 600 with a derivation
beside it, which is the builder's own phrase and it is correct. A cap is also
a wipe by another name: canon says nothing is EVER wiped, and a bound that is
"never reached in practice" still deletes on the day it is reached, silently,
in a green suite, which is the shape 115 was filed against.

THE THING THE BUILDER'S HEADROOM NUMBER RESTS ON IS NOT A BUDGET, and the
record must not let it become one. `Soak` 139 to 145 says it: no system-RAM
ceiling exists for this project; `performance-budget.md` sets frame and VRAM
figures and none for RAM; the 1 GiB is a REFERENCE SCALE and the printed key
says `not-a-budget`. So "15.5x headroom" is a ratio against a number nobody
ruled. It is a fine print and a poor conclusion. The conclusion that survives
is narrower: at the rate a seven-resident street produces, permanent memory
for 300 residents over 2,800 days costs tens of megabytes, which is below any
figure a PC would need a ruling for. Whether that rate holds at 300 is
section 1.3, and it does not.

WHAT JAFAR'S "UNAFFORDABLE" CLAUSE GETS. Not shown unaffordable. Not shown
affordable either, because affordability needs a budget and a rate at the
target population, and neither exists. The finding goes to him in the brief as
a finding with its bracket (1.3), and THE CARD IS ARMED ON QUEUE 284: if the
measured rate at the largest population the soak can run puts 300 residents
over a number he would have to name a machine for, the card carries that
number; if it stays inside tens of megabytes, no card, and the record says so.

## 1.3 Question B: the denominator, which is the one that matters

A SEVEN-RESIDENT RATE IS A FLOOR OF UNKNOWN LOOSENESS, NOT A PROJECTION, and
the honest output is both: the bracket to Jafar now, and the measurement that
closes it to the queue with a number. The mechanism, read off the code and not
argued from taste:

`MemoryStore.ProjectedBytes` (`MemoryStore.cs` 130 to 132) is `residents x
days x rate x bytes`, linear in the population BY CONSTRUCTION. Everything
turns on whether `rate` is itself a function of the population. The events
that fill a memory are, at the Core sites: a witness's own observation
(`Gossip.cs` 322), a conversation (334), a HEARD rumour (392), a contradiction
noticed (404), a check (446, 493) and the crime and reflection sites (727 to
941), plus the Game-layer sites in `DirectorHost`, `TrafficHost` and
`GameController`. The observation sources scale with what happens near a
resident, which is roughly constant in the population. The HEARD source scales
with how many DISTINCT rumours reach a resident: the guard at 381 to 383 stops
the same rumour value being re-heard at equal or lower confidence, so each
rumour costs a resident O(1) heard events, and the count of rumours that exist
grows with the number of witnesses, which grows with the population. So the
heard rate per resident sits somewhere between constant (a big town where each
person hears only their own street) and proportional to the population (a
town where every story reaches everyone). Both are consistent with everything
measured so far.

THE BRACKET, WITH THE ARITHMETIC SHOWN. At the floor, the rate stays at 0.361
and 300 residents over 2,800 days cost 66.2 MB. At the ceiling, the rate
scales as 300/7 = 42.9x, to 15.5 per resident per day, and the same town costs
2.84 GB, which is 2.8x the 1 GiB reference scale and would be a number to rule
a machine for. The truth is between, and the soak at seven cannot say where.
Note also that the rate is not stationary in TIME either: 0.361 over 499 days
and 0.379 over 2,799 days (7,417 / 7 / 2,799), five percent up as rumours
accumulate, so the 2,800-day projection made with the 499-day rate is already
five percent low at seven residents.

THE STIMULUS IS SYNTHETIC, which is the second reason the number cannot be
had today. `Soak` 292 to 294 and 326 to 328: one witness plants a fact on day
one and "somebody was in the yard again" on a quarter of days; `mill.Tick`
meets pairs at ten percent per hour. That is a property of the soak, not of
the game's town, whose event generator at 300 residents does not exist. The
rate the game produces will be measured when the game produces it; what can
be measured NOW is the mill's own scaling law under a fixed stimulus, which is
the half of the bracket that is the studio's to close.

THE CHEAPEST DECISIVE MEASUREMENT is the soak with a generated roster at 7,
14, 28, 56, 112 residents, and 224 and 300 if the wall clock at 112 allows,
printing events per resident per day and wall seconds per N. Rule 7: what
dominates is `mill.Tick`, which walks pairs every hour, O(N squared) per hour;
at 300 residents that is 44,850 pairs x 67,200 hours, about 3 x 10^9
predicate calls over 2,800 days, which is minutes in .NET if the predicate is
cheap and could blow up if it is not. The series prints its own cost, so the
next session reads it instead of guessing. This is a flag on an existing
instrument and not a new one, so it is inside Jafar's rule of the day.

QUEUE: 284 the-memory-rate-against-population

AND THE SOAK'S GATE HAS A GAP THE SAME ITEM CLOSES. `FirstFall` (`Soak` 222
to 227) catches a count that FALLS, which is the old prune's shape. A
steady-state cap that dropped the oldest event on every append past a bound
would hold the count flat and pass it. The CoreTests hole-detector catches
that shape (901 examined, none missing); the soak does not, because it never
counts appends. Queue 284 has the soak count appends per resident and assert
`Events.Count == appends`, which is the canon property with its denominator
on the line.

## 1.4 Question C: the fixture

THE RIGHT TREATMENT, AND THE RENAME IS HONEST. A golden that records a canon
violation as correct behaviour has to change when the behaviour changes, and
changing it openly with the old values in the diff is the only honest form.
`perception-golden.txt` 2366 to 2373 now carries `mem_permanent` with
`countAfter601=601`, `firstTextAfter601=e0`, `countAfter701=701`,
`firstTextAfter701=e0`. Three things make it honest rather than convenient:

1. THE KEYS DID NOT MOVE. `countAfter601` and `countAfter701` are the same
   keys with new values, so a reader diffing the golden sees exactly which
   claims flipped (500 to 601, 600 to 701, e101 to e0) and nothing else.
2. THE APPEND COUNTS STAYED AT 601 AND 701 ON PURPOSE. `PerceptionGolden` 463
   to 469 and `CoreGolden.h` 192 to 196 both say why: those are the appends
   that used to trigger the cap, and a scenario that stopped crossing it would
   prove nothing about the engine that removed it. It pins the ABSENCE of the
   cap at the exact points where its presence used to show.
3. IT IS CROSS-ENGINE. The C# writes the rows and the C++ is compared to
   them, so the "0 mismatches" the builder reports, once the footer confirms
   it, is the proof that the twin at `MemoryStore.h` removed the cap too and
   not merely a comment saying it did. The name `mem_permanent` says what the
   scenario now tests; keeping `mem_prune` would have been a scenario name
   asserting a behaviour the engine no longer has.

ONE LINE OWED. `CoreGolden.h` 195 to 196 records "countAfter601 was 500 and is
601; countAfter701 was 600 and is 701" and does not record that
`firstTextAfter601` was `e101` and is `e0`. That third row is the one that
says WHICH events the old prune took (the weakest 101 of the older half, e0
to e100, importances ascending by index), and the record of a deletion should
name what was deleted. Condition 1.6.3.

## 1.5 Question D: what is refused in part one

- Any cap derived from the seven-resident rate, under any derivation.
- The sentence "54 percent of the town's memory" in any message. It is 54.5
  percent of a seven-agent soak street at 2,800 days, one seed. The sentence
  to Jafar names seven.
- "66 MB" called the bill, or "15.5x" called headroom, without the words
  floor and reference scale beside them. The soak prints `not-a-budget` on
  the line; the prose does not get to drop it.
- Landing on the builder's counts. The footer FROM THE FILE on the landing
  tree, reading the new CoreTests and soak counts, is the only evidence of
  4363 and 5.
- Two of the eight new CoreTests checks (401 to 409) are printers wearing
  check clothing: `mb500 > mb300` cannot fail for any positive inputs and
  `affords / soakRate > 1` fails only if the typed constant is retyped above
  5.58. They may stay as printers. They are not counted as guards, and the
  printed line must carry the denominator (1.6.2).

## 1.6 Conditions of landing, in order

1. QUEUE 115'S STATUS LINE begins RULED: "RULED 2026-09-14 by Jafar, 'canon
   stands, the code changes'; landed under game-design/decision-2026-09-14-
   ruling-the-prune-is-gone-seven-is-a-floor-and-the-fog-is-the-cloud-deck.md.
   The prune is gone from MemoryStore.cs and MemoryStore.h; CoreTests
   1845 to 1867 asserts 901 of 901 with no hole; the soak gates that no
   resident's count ever falls. CLOSES when ledger/.verify-footer on the
   landing commit prints the soak's 5 checks and CoreTests above 4355. The
   bill at 300 residents is a FLOOR (66.2 MB at the seven-resident rate) with
   a ceiling of 2.84 GB if the rate scales with population; queue 284
   measures which." Jafar's words stay quoted below it as they are.
2. `CoreTests/Program.cs` 402 to 403, the printed check text, reads: "the
   town bill at 2800 days is {mb300:0}MB for 300 residents and {mb500:0}MB
   for 500, AT A RATE OF 0.361/npc/day TYPED FROM THE SOAK OF 2026-09-14 OVER
   7 RESIDENTS x 499 CLOSED DAYS (queue 116: seven is not a town; queue 284:
   the rate against population is unmeasured)". Same denominator on the 407
   to 408 line. Dictated text; the resident may hand-apply it.
3. `CoreGolden.h` 195 to 196 gains "; firstTextAfter601 was e101 and is e0,
   which names the 101 weakest events of the older half the cap used to
   take". One line; the resident may hand-apply it.
4. THE RULE-6 GREP, PRINTED: `MaxEvents|PruneTo|Prune\(` over the .cs, .h and
   .cpp files, with the count of hits and every hit named; expected three
   comment hits plus the CoreTests fixture, and zero live sites. A fourth
   live hit is a stop.
5. `python3 ledger/verify.py`, footer FROM `ledger/.verify-footer`, and the
   footer's CoreTests and soak counts pasted into NOW.md beside the words
   "read off the footer, not the builder".
6. THE BRIEF, Producer's channel, carries the finding in this shape: the
   store was deleting more than half of a seven-agent street's memory at
   2,800 days while its own series read quiet; it is gone from both engines;
   the cost of permanence is measured per event and is a floor at the town's
   size; the measurement at population is queue 284 and the card is armed on
   it. No percentage of "the town".
7. Queue 116 is NOT reopened by this ruling (it is inside 275, his). Its
   instrument half is discharged by `Soak` 194 to 196, which prints
   `[queue-116:7-residents-is-not-a-town]` on the rate line; its document
   half (grep every citation of the soak for hundreds) is not done and is
   not ordered here.

QUEUE: 115 canon-says-nothing-is-wiped-and-the-code-prunes

# PART TWO: THE FOG

## 2.1 Verified, and what opening the frames added

THE SERIES IS CLEAN. All four fog rows on `32bae70` (verdict lines 206 to
209) are `cam_hook`, sun 3.000, sky 1.000, pin `PINNED-HELD` asked 0.3000 read
0.3000/0.3000, overrides 1/1, so they were photographed at ONE exposure and
none is a leaked row. Line 322: `expPinRowsLeaked=0/of=6`, so this is the
post-batch run and the leak fix held. Line 319: the nine-id null group reads
`nullSpreadMeanLuma=0.0002`, `nullSpreadGroundP05=0.0012`, verdict CLEAR.

THE SPECIALIST'S CLAIM ABOUT THE LEVER HOLDS, AND THE MECHANISM IS IN THE
CODE. `sky_intensity` 1.00 to 0.35 at sun 3 moves `band.skyCentre.meanLuma`
from 0.9268 (line 195) to 0.9259 (line 204): 0.0009. `VignetteShot.cpp` 1589
shows why: the field is written to `USkyLightComponent::SetIntensity`, the
AMBIENT captured from the sky, and the visible sky is an `ASkyAtmosphere` lit
by the sun (1288 to 1309, 1571 to 1582). It is a lighting lever, and on the
GROUND it is a large one: `band.ground.p05` 0.4617 at sky 1.00 against 0.2405
at sky 0.35, the same two lines. So the grid's sky axis moves the dark end of
the street and the fog axis moves the sky band. Two levers, two statistics,
and the twelve-cell grid was run with the fog lever pinned at 0.45 (vignette-
pieces.json 27 to 39, every grid row `fog_max_opacity 0.45`), so no cell could
have reached the sheet's sky.

THE FOUR ROWS, off the verdict lines, with the sheet's numbers from
`findings.txt` 2834 to 2839 (Rec.601, indexed percentiles, the project's own
ruler) and `VignetteShot.cpp` 200 to 201 (sky p50 0.808 over 48,800 px):

    fog    shotMeanLuma  skyCentre.mean  skyCentre.meanRGB    ground.p05  ground.p95/p05
    0.450  0.6598        0.9268          235.5/236.4/238.1    0.4617      1.80
    0.250  0.6048        0.8822          223.7/225.0/228.4    0.3625      2.15
    0.100  0.5401        0.7979          200.7/203.5/210.6    0.2532      2.84
    0.000  0.4136        0.6222          152.7/158.2/176.8    0.0862      7.83
    sheet  0.4102        0.808 (p50)     pale, no blue        0.1935      3.65

The specialist's datum figures 0.8057 and 0.1926 appear in no file I could
open; the tree's own are 0.808 and 0.1935 and the residuals below use those.
Sky at 0.100: 0.010 under. Ground p05 at 0.100: 0.060 over; linear between
the two rendered neighbours it crosses the sheet near fog 0.06. Whole-frame
mean says 0.000, and it is the weakest of the three for a reason the next
paragraph shows.

WHAT LOOKING ADDED, RULE 4. I opened all four frames. At 0.450 the sky is a
white field, the far end of the street dissolves into it, and the diagonal
shadow the left building casts across the carriageway is barely there. At
0.100 the sky is a pale grey with a little blue, the shadow across the road is
unmistakable, the lit and shadowed halves of the asphalt read as two tones,
and it is the most photographic of the four. At 0.000 the sky is a blue-grey
gradient and THE END OF THE STREET IS A BLACK SLAB: a horizontal band at the
horizon where the world ends and nothing lit stands. That slab is the
`24709/921600` near-black count. It is not dark in the street; it is the edge
of the world showing through, and it reads grey at 0.100 and white at 0.450.
So two of the specialist's three statistics, whole-frame mean and near-black,
are contaminated below about 0.25 by geometry the sheet does not have, and
`band.ground` (rows 576 to 720, the near road) and `band.skyCentre` (rows 0
to 90) are the two that are not. The record reads those two and no other
against the sheet. The open end itself is a thing the frame has and the
panel lacks (the sheet's street closes at a vanishing point with buildings),
and under queue 180's own rule it is NAMED here as a later rung and not
smoothed over by fog.

QUEUE: 180 rung-1-the-street-matched-to-the-hook-sheet

THE SKY UNDERNEATH THE FOG IS A CLEAR SKY. At 0.000 the sky band's RGB is
152.7/158.2/176.8: blue by 24 counts and 0.19 under the sheet. The four
atmosphere constants at `VignetteShot.cpp` 183 to 186 say of themselves "a
starting point" with "no series", and 171 says the HDRI the conditions name
"is the next rung". The fog has been supplying both the brightness and the
neutrality of an overcast, which is why every frame this project has shot
reads as a white far field (158 to 161). Fog is the cloud deck. That is the
finding that outlives today's number, and it gets its own item (2.5).

THE RIG STILL DIFFERS FROM ITSELF. Line 323: `rigDeterminism=DIFFERS
rigRepeatOf=vign_camA_day rigDiffPixels=784509/921600 rigMaxAbsChannelDiff=43/
255 rigMeanLumaDelta=+0.0034`, on a PINNED condition (25 of 27 pinned, line
322). Step 1 of D31 is not met on this run, and that is the resident's and
queue 235's to carry, not this ruling's to fix. What it means here: the fog
series is READABLE, because its smallest adjacent step (0.055 in mean luma,
0.09 in ground p05) is sixteen times the repeat delta; and the frame Jafar
receives is LABELLED with that line, because his own rule says nothing is
judged until two photographs of one scene are one picture.

## 2.2 The ruling: 0.100 now, and the finer series in the same dispatch

BOTH, IN ONE ROUND TRIP, and the reason is that the two options answer
different questions. Jafar's sentence asks for a frame beside the sheet.
Rule 2 asks that no bound be set without a printed series. Neither forbids
the other, and the round trip costs the same carrying one change or six.

1. THE JUDGED CONDITION `overcast_day` MOVES TO `fog_max_opacity 0.100`. It
   is a rendered cell, opened and read; the only rendered cell within 0.01 of
   the sheet's sky; the nearest rendered cell on the dark end; and the one
   whose picture shows the sun landing. It is a value chosen off a printed
   four-point series, which is what rule 2 permits, and not a bound, which is
   what rule 2 forbids without one. The pin stays 0.300 (held through step 2
   by the 14:12Z ruling); at 0.100 the row clips nothing (`shotClipHiAny=0`,
   `shotClipLoAll=0`, line 208), so the pin's reason for being still holds.
2. THREE FOG RUNGS RIDE THE SAME DISPATCH: `fog_maxop0020`, `fog_maxop0050`,
   `fog_maxop0080`, at the reference cell, everything else identical to the
   four A4 rows. And THREE SKY RUNGS AT FOG 0.100: sky 0.35, 0.50, 0.70 with
   sun 3.0, because the grid's own numbers say the dark end is the sky
   lever's and the sky band is the fog lever's, and the cross has never been
   rendered. Six probe frames, about 33 seconds at the grid ruling's 5.5 s a
   row. Read on `band.skyCentre.meanLuma` and `band.ground.p05` only.
3. THE VALUE IS RE-SET ONLY BY RULING FROM THAT PRINTED SERIES AND HIS EYE,
   never by a builder reading the residuals. The 0.06 that linear
   interpolation suggests is written here as what the series must test and
   not as a number anybody sets.

QUEUE: 285 the-fog-cap-between-0-and-0-10-is-unrendered

THE TWO TESTS THAT PIN THE JUDGED ROW AT 0.450 ARE RETIRED BY THIS RULING AND
REPLACED IN THE SAME SHAPE. `CoreTests/Program.cs` 19930 to 19935 and
`vignette-spec-test.cpp` 475 to 476 were the A4 landing's guard that "the
field replaced the literal and moved no number", which was true and is now
done. They assert 0.100 with the sentence "moved by the ruling of 2026-09-14
from the fog series on 32bae70", both engines, one commit, a matched set. The
four-row assertions at 19921 to 19929 and the C++ counterpart extend to seven
values. The 09-09 grid ruling's C11 ("every pre-existing condition reading
0.450") is superseded for `overcast_day` by this section and stands for
`wet_night`, which is not judged and is not touched.

## 2.3 Sodium at dusk: it cannot be built today, it gets a number, and it does not block the frame

VERIFIED AT ALL SIX SITES. The sun's elevation is a SCENE field, read once:
`VignetteSpec.h` 460 to 463 parses `sun.elevation_deg` at the root;
`VignetteShot.cpp` 1259 to 1264 spawns `GSun` from `GSpec.SunElevationDeg`
once per run; `StreetVignette.cs` 1911 to 1913 reads `lighting.sun.day_
elevation_deg`; `StreetVignettePieces.cs` 409 to 412 emits one `sun` block at
the root; `StreetVignetteHost.cs` 653 to 655 applies it once; `tools/frame-
shadow-probe.py` 662 to 666 reads `spec["sun"]` for every frame. A condition
called dusk today would carry a 36-degree sun with dim lamps and would be
photographed, measured and captioned as dusk. That is a spec-contract change
across two engines and a tool, Core among them, so its LANDING wants a
director; its FILING does not.

QUEUE: 283 the-sun-elevation-is-a-scene-field-and-dusk-needs-it-on-the-row

DOES IT BLOCK THE FRAME HE ASKED FOR? NO. The frame beside the Hook sheet is
rung 1 (queue 180): the sheet's lower panel is flat overcast DAY, and the
frame matched to it is a day frame. Sodium at dusk is the second half of D28
step 2 and the target frame at the END of the slice ("dusk, wet, lamps lit, a
figure in silhouette", D31), which also waits on 276 (the settled night
exposure) and on wetness. 283 blocks THAT frame and nothing before it.

## 2.4 The sheet has no hard shadow: whose call

THE DIRECTOR'S, AS TO WHAT THE SHEET IS A DATUM FOR; JAFAR'S, AS TO WHICH
LOOK HE WANTS AT RUNG 1; AND THE WAY TO ASK HIM IS TWO FRAMES, NOT A
PARAGRAPH.

Ruled here: the sheet is the datum for the SKY BAND and the DARK END (two
band statistics, 0.808 and 0.1935 on this project's ruler) and not for the
shadow step, which the sheet cannot supply because it has none. His sentence
"bring the sky down so the sun lands and the street has dark in it, measured
against the in-house Hook sheet" is consistent with that reading in every
clause: the sky comes down (0.93 to 0.80), the sun lands (the shadow step the
specialist read rose from +0.19 to +0.31 across the same rows), the street
has dark in it (ground p05 0.46 to 0.25 and falling), and the sheet supplies
the two numbers the dark end and the sky are measured against. D23 says the
sheet is a floor and not a ceiling; a cast shadow the sheet lacks is above the
floor, not beside it.

His, and not decided here: whether rung 1's frame should be the sunlit street
(renderable today) or an overcast street like the panel (NOT renderable today,
because the sky underneath the fog is a clear-sky atmosphere, section 2.1).
The default until he says otherwise is the sunlit frame at 0.100, labelled.
When queue 286's series lands, he gets the overcast candidate beside it and
says which way the gap runs, which is D23's own test. His pace rule applies:
his verdict adjusts, it does not gate.

QUEUE: 286 the-sky-is-a-clear-sky-atmosphere-and-the-reference-is-overcast

## 2.5 Conditions of the fog dispatch, in order

1. `production/specs/vignette-scene.json`: `overcast_day` `fog_max_opacity`
   0.450 to 0.100. Its note field gains, verbatim: "fog_max_opacity 0.100
   chosen by the ruling of 2026-09-14 (decision-2026-09-14-ruling-the-prune-
   is-gone-seven-is-a-floor-and-the-fog-is-the-cloud-deck.md) off the
   four-row series on 32bae70, row vign_fog_maxop0100 (verdict line 208):
   band.skyCentre.meanLuma 0.7979 against the sheet's 0.808 p50/48800px,
   band.ground.p05 0.2532 against the sheet's 0.1935. Re-set only by ruling
   from queue 285's series." `wet_night` is not touched.
2. Six new probe conditions and six `cam_hook` shots, ids `fog_maxop0020`,
   `fog_maxop0050`, `fog_maxop0080` (fog 0.020, 0.050, 0.080, sky 1.00) and
   `fog010_sky035`, `fog010_sky050`, `fog010_sky070` (fog 0.100, sky 0.35,
   0.50, 0.70), sun 3.0, wetness 0.60, fog_density 0.0120, pin 0.300,
   lanterns off, practicals off. Every field required, no defaults, as A4.
3. `vignette-pieces.json` regenerated through the emitter so the two files
   cannot disagree; the piece-list checks the 14:12Z ruling's 13.4 names are
   the gate.
4. The two 0.450 assertions become 0.100 assertions (section 2.2), and the
   seven-value series is asserted in both suites. CoreTests and vignette-spec
   -test counts printed on the final tree with the delta named.
5. Verify green, footer from the file. Docs-check green: the four markers in
   this record are red until 283, 284, 285 and 286 exist under
   `production/queue/`, and THAT IS THE GATE WORKING, not a fault in this
   record. The resident files them from section 5 before running verify.
6. The sha captured before dispatch, the run watched by ancestry. On landing:
   `fogMaxOpacityRead` asked beside read on all seven fog rows and the
   `overcast_day` rows reading 0.100; `nullSeriesIds` naming
   `vign_fog_maxop0100` and NOT `vign_fog_maxop0450` (the null twin follows
   the judged row by derivation; if 0450 is still listed, the derivation is
   stale and that is the finding); the six new rows' two statistics printed
   as a series.
7. THE FRAME TO JAFAR: `ue-vign_hook_day.png` from that run beside the
   sheet's lower panel, sent by the Producer, captioned with the rig line
   (`rigDeterminism` and `rigMeanLumaDelta` as printed) and one sentence:
   "step 1 gates the judging; this is the frame, and whether you judge it
   yet is yours."

## 3. The quality ladder at close

Part one: best available for the STORE (nothing is wiped, append is O(1), the
cost is measured per event against a real heap). First working for the
NUMBER: a floor from seven residents. Next rung named: queue 284, and the
soak's append-count denominator inside it.

Part two: first working. One rendered cell chosen off a four-point series.
Next rungs named: queue 285 (the finer series and the cross), queue 286 (the
sky's own lever), queue 283 (dusk), and under 186 the HDRI the conditions
have always named. The open end of the street is named under 180.

## 4. Refused, both parts

- Any cap on memory derived from a rate measured at seven residents.
- Adopting fog 0.000: its near-black is the world's edge, not the street.
- Any change to the exposure pin in the fog dispatch.
- A dusk built by dimming `sun_intensity` on a row while the elevation stays
  at 36: a midday sun at dusk brightness, photographed as dusk.
- Any sentence saying the frame "matches the Hook sheet". It matches two band
  statistics to within 0.01 and 0.06; the sheet is a different picture (wet,
  brick terrace, lit windows, people, a closed end) and the judgement is his.
- Any marker deleted from this record to clear a red before the items exist.

## 5. The four items, dictated so the resident files them and does not invent them

Front matter per `production/queue/README.md`. Filenames exactly as the
markers above name them.

    283-the-sun-elevation-is-a-scene-field-and-dusk-needs-it-on-the-row.md
    line: engine and Core, jointly (the shared scene contract)
    spec: sun.elevation_deg and sun.azimuth_deg leave the scene root and
      become REQUIRED fields on every condition row, in the shape A4 gave
      fog_max_opacity: parsed with NeedNum in VignetteSpec.h (462 to 463
      today), read by StreetVignette.cs (1912 to 1913), emitted per condition
      by StreetVignettePieces.cs (409 to 412), applied per condition in
      VignetteShot.cpp (1259, today a once-per-run spawn) and
      StreetVignetteHost.cs (653 to 655), read per frame by
      tools/frame-shadow-probe.py (662 to 666). Every existing row carries
      36.0/205.0 so no pixel moves. The root block is DELETED, not left as a
      fallback. The verdict prints elevation asked beside read per shot, as
      it does for the pin, with the residual.
    acceptance: a committed run whose every sun-on row prints asked beside
      read with residual 0.0; the null series unchanged; and one probe row
      dusk_probe whose elevation is DERIVED from a named latitude, date and
      clock time written in its note field, lanterns on, at auto exposure,
      which is the first row that can carry "sodium lamps at dusk". Nothing
      about dusk is judged until queue 276 exists.
    max_sessions: 2
    status: READY 2026-09-14, filed by the ruling named in the marker. Does
      NOT block rung 1 (the sheet is overcast day). Blocks D28's target frame
      (dusk, lamps lit). Landing wants a director: Core and the two-engine
      contract move together.

    284-the-memory-rate-against-population.md
    line: simulation (Core), the measurement surface
    spec: ledger/Soak gains --residents N with a GENERATED roster (names,
      circles, greed, nerve, loyalty and ties drawn from the seed; average
      degree held near the seven-street's 3.1 so N is the only thing that
      moves; --degree D to move it deliberately). The done line prints per
      N: eventsPerNpcPerDay, busiestResident, wall seconds. Series: 7, 14,
      28, 56, 112; then 224 and 300 if the wall time at 112 permits (what
      dominates is mill.Tick over pairs per hour). The permanence gate gains
      the append count per resident and asserts Events.Count == appends,
      which catches a steady-state cap FirstFall cannot. No bound is set.
    acceptance: one printed series with at least five N; the slope of rate
      against N stated with its fit; the 300-resident bill at 2800 days
      restated from the rate at the largest N run, with the extrapolation
      distance named; the append-count gate shown on its accepting case and
      on a planted steady-state cap.
    max_sessions: 2
    status: READY 2026-09-14. A flag on an existing instrument, not a new
      one. THE CARD TO JAFAR IS ARMED ON THIS ITEM: if the measured rate at
      the largest N puts 300 residents over a figure he would have to name a
      machine for, the card carries that figure; inside tens of megabytes,
      no card, and the brief says so.

    285-the-fog-cap-between-0-and-0-10-is-unrendered.md
    line: engine and art, jointly
    spec: three fog rungs (0.020, 0.050, 0.080 at sky 1.00) and three sky
      rungs (0.35, 0.50, 0.70 at fog 0.100), cam_hook, sun 3.0, pin 0.300,
      everything else identical to the four A4 rows. Read on
      band.skyCentre.meanLuma and band.ground.p05 ONLY: shotMeanLuma and any
      near-black count are contaminated below about 0.25 by the world edge at
      the end of the street (the black band in ue-vign_fog_maxop0000.png).
    acceptance: one committed run with the seven fog rows and the three
      cross rows, asked beside read on all of them, the two statistics
      printed as a series over each axis, and overcast_day's value re-set
      BY RULING from that series and Jafar's eye, with the note field naming
      run, commit and rung.
    max_sessions: 1
    status: READY 2026-09-14. The judged row moves to 0.100 in the same
      dispatch under the ruling; this item is the series after it.

    286-the-sky-is-a-clear-sky-atmosphere-and-the-reference-is-overcast.md
    line: engine and art, jointly
    spec: at fog 0.000 the atmosphere alone renders the sky band at 0.6222
      with meanRGB 152.7/158.2/176.8, blue by 24 counts and 0.19 under the
      sheet's 0.808 (verdict 32bae70 line 209). The four constants at
      VignetteShot.cpp 183 to 186 are "a starting point" with no series. Print
      a series over Mie scattering scale (0.04, 0.08, 0.16, 0.32) at fog
      0.100 and sky 1.00, Rayleigh held, reading band.skyCentre.meanLuma and
      the B minus R gap per rung. No constant moves in that run.
    acceptance: a committed run printing the Mie series; the rung where the
      sky band's B minus R gap closes to within the null spread named; and
      the overcast candidate frame from that rung sent beside the sunlit one
      so Jafar can say which way the gap runs (D23).
    max_sessions: 1
    status: READY 2026-09-14. The other route to an overcast, binding the
      HDRI the conditions have always named, sits under queue 186
      (LookForNamedHdri prints whether the file is reachable). Whichever
      series lands first decides the sky's lever.

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

<!--RULING spawn=2026-09-14T16:25:22Z-->
