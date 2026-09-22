# Ruling, 2026-09-15 (00:52Z): the grade lands as the legacy build's number and not as a bar, concrete is a named contamination and not tonight's split, no retirement is spent for a key, and the outbox brief was never a net

STATUS: LOG, 2026-09-15. NOT CURRENT once the dispatch carrying queue 299
has landed and its frame has been read per section 10; from then the verdict
file, the g++ suite, queue 299, 291, 293, 302 and 303 are the reading copies
and this is the record of what was ruled and why.

Director ruling on the batch behind queue 299 (the albedo grade) and queue
291 (the brief that missed its day), escalated because `director_cadence`
is red at about 1427 insertions over 15 files against the inherited 100,
reference commit `397ed0cd@2026-09-14T23:24:12Z`. Five calls were put to
this director and each is ruled below with the evidence beside it, including
the four places where the brief that dispatched this review was itself wrong.
No code was written by this director and this director has no shell. Every
number below was read off the file and line it names in this session, or is
arithmetic shown in full.

Author: tier-1 director, stamp at the foot naming row 621 of
`.claude/agent-log.tsv` (`2026-09-15T00:52:56Z` TAB `studio-director`,
agentId `abe78b730e4f289f3`). Rows 616 to 620 (`engine-specialist` and
`instrument-builder`, 00:22Z to 00:47Z) are the builders' rows and are not
claimed. The resident reconciles the stamp against what the gate prints.

## 0. What was opened

`production/queue/299`, `291`, `181`, `300`, `301` whole; `production/queue/
186` by name only. `ue-probe/Source/LedgerProbe/Public/SurfaceBind.h` 240 to
570 and 990 to 1290; `ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp`
3740 to 3840; `ue-probe/tests/vignette-spec-test.cpp` 2470 to 2720;
`ue-probe/Source/LedgerProbe/Public/VignetteSpec.h` 580 to 620;
`tools/ue/make_base_material.py` 140 to 180, 1300 to 1360, 3125 to 3165;
`ledger/Assets/Scripts/Game/AssetLibrary.cs` 349 to 360, 429 to 560, 819 to
840 and the grep hits at 456, 911; `ledger/Assets/Scripts/Core/LightModel.cs`
600 to 604; `ledger/Assets/Scripts/Game/StreetVignetteHost.cs` 330 to 415 and
the `AssetLibrary.` hits at 108, 238, 299, 449, 715; `production/specs/
vignette-pieces.json` 1 to 90 and every line carrying
`"surface":"concrete"` (150, itemised in section 4); `production/d1-probe/
ue-vignette-verdict.txt` line 1, 193, 232 to 248; `tools/runner/brief.py`
228 to 380, 722 to 790, 1037 to 1062; `tools/runner/telegram-bot.py` 1791
to 1929 and 3609 to 3625; `tools/runner/outbox.py` 925 to 980 and 2085 to
2128 by grep; `tools/producer-day.py` 388 to 477 and 530 to 533;
`tools/inbox-read.py` 55, 77, 92, 177 by grep; `.github/workflows/
ledger-install-supervisor-task.yml` 560 to 729 and 989 to 992;
`production/pc-ops/brief-send.txt` whole; every file under
`production/outbound/` matching `brief` (12), the listing of
`production/briefs/` (15) and `production/outbox/` (42); the six receipts
named in section 7; `ledger/verify.py` 1003 to 1028, 3431 to 3439, 4339 to
4345, 5095 to 5134, 6471 to 6570; `tools/docs-check.py` 69, 108 to 127;
`ledger-v2/respec/decision-register/D1-engine-probe.md`, `D16-engine-
unreal.md`, `D23-the-phase-a-bar-is-the-hook-sheet.md`, `D32-a-ruling-names-
its-queue-item.md` whole; `production/stages.md` 284 to 297;
`production/quality-ladder.md` 1 to 60; `production/NOW.md` 1 to 105; the
20:01Z ruling of 2026-09-14 whole as the model; `.claude/agent-log.tsv` 600
to 621. Greps, with their counts: `tintTexel|roughnessTexel|tintFrom|
tintPattern` over `tools/`, `ledger/CoreTests/` and `.github/`: 0 hits in
each, so no reader parses the four fields this batch re-fills;
`GetVectorParameterValue` over `ue-probe/`: 0 hits; `WetSurfaces|
IsGroundSurface|GroundGrade|TextureGrade|0\.55|0\.74` over
`tools/surface-tint-check.py`: 0 hits; `[Ww]etness` over
`ue-probe/Source/LedgerProbe`: 7 hits, all in `VignetteSpec.h`, none a read
site in the shot code; `Graded|bGradeSet|surfacesGraded` over
`SurfaceBind.h`: the struct at 1012 to 1013 and the printer at 1227 to 1246,
no tally anywhere; `new instrument` over `game-design/`: 4 hits, the two
precedents quoted in section 5.

## 1. The answer in one paragraph

THE BATCH LANDS, with one line of the test fixed by hand before the commit,
the corrections in section 9 applied, and the residual reported to Jafar in
the words of section 3 and not in the words of the brief that reached me.
Parity lands as parity because it is the best available STARTING number, not
because it is a bar: D16 made Unity the legacy reference build on 2026-09-10,
so the constants being copied were judged on a retired engine against
references D8 retired, and the frame beside the Hook sheet is what D23 says
decides. Concrete is a contamination the legacy source's own author named,
with the fix named beside it, and it is not split tonight because the split's
trigger is a landed still and none exists; it is queue 302. No retirement is
spent for a verdict key, because the grade is on twelve landed lines by value
and the thing actually missing is a whole-run tally and a readback, both of
which land with the retirement queue 293 already rules. The outbox brief
register retires: its record over the six days the file path has existed is
zero catches and two duplicates, and the runner-independent property it had
survives under the `.unprompted.md` register. What the recovery does not
cover, a brief older than one day, was never covered by the net either, and
is queue 303.

## 2. What I verified, claim by claim, and where the brief to me was wrong

THE COUNTS. The g++ block at `vignette-spec-test.cpp` 2485 to 2706 contains
38 `Check` calls, counted one by one: 3 on the default, 4 on the wall, 5 on
the road, 4 ground members, 5 non-members, 4 on the procedural pair, 2 decal
blends, 2 on the untextured kerb, 1 on the spelling, 5 on the graded line, 1
on the never-reached line, 1 on the procedural line, 1 on key=value. 409 plus
38 is 447, which is what the resident printed. The count is consistent with
the diff and I did not recompile it.

THE ARITHMETIC IN THE TEST REPRODUCES. ((0.74 + 0.055) / 1.055) ^ 2.4:
0.795 / 1.055 = 0.7535545, ln = -0.282954, times 2.4 = -0.679090, exp =
0.507078, matching the test's 0.50707851 at 2506 to 2508. ((0.407 + 0.055) /
1.055) ^ 2.4: 0.462 / 1.055 = 0.4379147, ln = -0.825731, times 2.4 =
-1.981754, exp = 0.137827, matching 0.13782717 at 2531 to 2533. The bytes
189, 194, 204 and 104, 107, 112 are 0.74, 0.76, 0.80 and 0.407, 0.418,
0.440 times 255 rounded. Queue 299's prediction "kerb 184.3 to about 74.8"
also reproduces on luma from the same transfer: 184.3/255 in linear is
0.48098; times the three linear grades 0.13783, 0.14583, 0.16265 gives
0.06629, 0.07014, 0.07823; back to sRGB bytes 72.8, 74.9, 79.0; luma
0.2126 R + 0.7152 G + 0.0722 B = 74.75. The item's own note that the red
channel lands at 73 is right too.

THE SET SITE AND THE ORDER. `VignetteShot.cpp` 3802 to 3810 asks
`AlbedoGradeFor(surface, bAlbedoBound)` and hands the LINEAR triple to
`SetVectorParameterValue` as an `FLinearColor`; `SurfaceBind.h` 519 to 529
forms the gamma product first and converts once, which is the order
`ProceduralAlbedoTexel` uses at 380 to 396. The generator puts the multiply
AFTER the `BaseColorMap` sample (`make_base_material.py` 3129 to 3131) and
defaults it white (166, 3157 to 3164); `--selftest` refuses a non-white
default as a number (1310 to 1314) and asks the `.cpp` files for
`SetVectorParameterValue` and `AlbedoGradeParam` separately (1330 to 1339),
so a declared-but-never-set parameter cannot print green. The procedural
pair takes white by the first branch of `AlbedoGradeFor` (504 to 508) and
the suite pins the interior texel at 31.22.14 (2605 to 2609), so nothing is
graded twice. The tint route reaches the same instance (3813), which is why
the surface name and not a bool is passed; that is the trap the comment at
3798 to 3801 names, and it is handled.

WHAT "PARITY" IS PARITY WITH, and this is the first place the brief to me
was incomplete rather than wrong. `AssetLibrary.BaseColour` (550 to 556) is
Unity's DRY base colour: `TextureGrade` times `GroundGrade` for the four in
`WetSurfaces`. `SetWetness` (819 to 840) then multiplies those same four by
`LightModel.AlbedoScale(wetness)`, which is `Clamp(1 - 0.45 * rain, 0.55,
1.0)` (`LightModel.cs` 600 to 604), and the comment at 835 to 837 says in
its own words "a wet road runs 0.55 x AlbedoScale and a dry one runs 0.55".
`StreetVignetteHost.cs` 715 calls `AssetLibrary.SetWetness((float)
c.Wetness)`, and the judged row `overcast_day` carries wetness 0.60
(`vignette-pieces.json` line 25), so the legacy host at the judged condition
runs its ground family at 0.74 x 0.55 x 0.73 = 0.297 in gamma on red. The
Unreal side has NO wetness read site at all: seven `[Ww]etness` hits in the
probe source, all in `VignetteSpec.h` (the field, its parse, and the comment
at 2562 to 2563 saying so), and the verdict prints
`nullSeriesExcludes=wetness/because-VignetteShot.cpp-has-no-read-site-for-it`
(2746). That is queue 186's half. So what lands tonight is parity with the
legacy build's DRY grade, and full parity at the judged wetness would be
darker still on the ground family by 0.73 in gamma. THE RESIDUAL REPORTED TO
JAFAR MUST SAY SO, or he will judge a number as final that has one more term
owed to it.

WHAT UNITY IS NOW. D16 (2026-09-10, Jafar): "Unreal. D1's probe is closed on
the evidence. Unity becomes THE LEGACY REFERENCE BUILD." The 2026-09-14
leak ruling, section 4: "the engine is Unreal, so no newer Unity run will
ever land". `AssetLibrary.cs` is under `Assets/Scripts/Game/`, which D16
archives with the game scripts. So the constants `SurfaceBind.h` copies are a
legacy table, the D1 blind pair that would have compared the two renders is
closed, and "the other engine does it" is a statement about provenance and
not an obligation. That changes what call 1 is: not "parity or the sheet",
but "is the legacy number the right STARTING number", which it is (section
3), and "where does the number live once Jafar judges it", which is not a
legacy C# file (section 4, queue 302).

THE PROVENANCE OF 0.55, off `AssetLibrary.cs` 468 to 510: it is
`AlbedoScale`'s floor, "the multiplier under which this game's ground has
ALREADY been judged to read as a British street, twice", and the band it
was to be read against is "recomputed per run from the five GTA V
references" (499 to 500). CLAUDE.md section 0: GTA V on PS3 is retired by D8
and may not be cited as a target. The number was judged on frames by a
person, which is why it is the best available start; the bar it was measured
against is retired, which is why it is not a bar.

THE CONCRETE PIECES, counted off the pieces file rather than off the item.
150 lines carry `"surface":"concrete"`: `C13_sills_lintels` 72 (six bays on
`east_parade` and six each on `west_south` and `west_north`, a sill and a
lintel per window, two windows per bay), `C5_shopfront_assembly` 6 (the
stall fronts `east_parade_stall0` to `5`), `D7_parapet_coping` 4,
`C1_terrace_carcass` 2 (the two roofdecks), `E3_telephone_kiosk` 1 (the
plinth), `D3_chimney_pots` 5 (meshes), `G9_chewing_gum` 60 (cylinders on
the pavement). 72 + 6 + 4 + 2 + 1 + 5 + 60 = 150. NOT ONE IS A WALL FACE.
The wall faces of this street wear `brick_red` (41), `brick_grey` (12),
`plaster` (34) and `wood` (49), with `window` (36) and `glass` (22) set into
them. "Most of them WALLS" in queue 299 and in the brief that reached me is
therefore corrected to: 84 pieces of wall TRIM (sills, lintels, stall
fronts, parapets, copings), 7 at roof level, 61 sitting on the pavement (60
gum discs and a plinth) that are ground by position and not by name. A sill
is 0.95 by 0.075 metres; the pixel share of the 150 is unmeasured and no
instrument prints it. Piece count is a count of pieces.

THE NINE OF NINE. `outbox.py` 950 to 955 claims every `.brief.md` in the live
outbox already carries a receipt, "four from 8 September, one from the 9th,
four from the 14th". Listed: `production/outbox/` holds exactly nine
`.brief.md` files with those dates, and `production/outbound/` holds a
`.brief.receipt.txt` for each of the nine by name. The claim holds, and the
selftest's live check (2105 to 2113) reads the same tree.

THE FOUR FIELDS BREAK NO READER. Zero hits for any of `tintTexel`,
`tintFrom`, `tintPattern`, `roughnessTexel` under `tools/`, `ledger/
CoreTests/` and `.github/`. The value shapes on twelve lines change from
`not-built` to words and numbers, and the only parser of the surface line
is the suite that was changed with it.

THE ONE-DAY RECOVERY. `brief.recovery_target` (261 to 300) looks at the day
before and only that day, refuses a sent or held day through
`BriefReceipts.state` (763 to 781), and its docstring says why the window is
one day: the lag series on the live tree is [0, 0, 0] over 3 receipts, so
there is no distribution to set a window from, and a wider one would be a
bound with no series (rule 2). `brief_pass` (1836 to 1852) fires it only
when the caller asked for today and today has nothing; an explicit day is
never second-guessed. The exit-6 case now prints the done line and the
BRIEFS WRITTEN AND NEVER SENT line (1864 to 1884), the workflow annotates it
(712 to 714), and `producer-day.py` prints the same line in the dossier
(533). `brief_receipts` (390 to 447) unions the checkout and the `pc-inbox`
branch through `tools/inbox-read.py`'s own `fetch_branch`, `ref_exists` and
`outbound_from_branch` (77, 92, 177, all present) and returns None, printed
as nothing measured, when the branch cannot be read.

THE FILE PATH DID SEND ON 9 SEPTEMBER, and this is the place the brief to me
was wrong. `production/outbound/brief-2026-09-09.receipt.txt` reads
`receipt: sent`, `file: production/briefs/2026-09-09.md`, `messageId: 56`,
`sent: 2026-09-09T10:55:44+00:00`. The outbox copy
`2026-09-09-morning-brief.brief.receipt.txt` reads `messageId: 39` at
04:28:38Z the same morning. Two messages, one day. On the 8th the file path
did not exist: `brief.DAILY_PATH_OPENED` is 2026-09-09 and the docstring at
246 to 253 says the earlier briefs "either went out of production/outbox/
with no buttons on them or never went at all, and neither is a miss of a
sender that did not exist". On the 14th the outbox carried FOUR messages in
the brief register (ids 93 at 19:08:52Z, 94 at 19:08:52Z, 96 at 19:44:26Z,
97 at 21:41:23Z, off their receipts) beside the file path's id 95 with
`buttons: 2/2` at 19:09:03Z. `brief.py` 355 to 357 names id 93 as the copy;
that is the one carrying the fog frame eleven seconds before id 95, and the
docstring is right. So the sentence "the outbox route is the one that
ACTUALLY DELIVERED on 8 and 9 September when the file path sent nothing" is
true of the 8th only because nothing else existed, and false of the 9th.

## 3. Call 1: parity lands as the legacy number, the residual goes to Jafar labelled, and no constant is chosen here

THE QUESTION AS IT ACTUALLY STANDS. Whether to land the copied constants and
render, or hold until Jafar has ruled on the arithmetic. It is not "parity
against the sheet": with Unity legacy (D16) and no Unity run ever landing
again, there is no live pair for parity to serve; what the constants offer is
a number judged right on frames twice (`AssetLibrary.cs` 473 to 481), tested
in both readers, and reachable by one parameter. That is the best available
start under CLAUDE.md's standing order and it is not a target under D8.

THE ROUTES.
- A. Land the copied constants, render, put the frame beside the sheet and
  report the residual with no bound. One dispatch. If the frame is too dark
  the second dispatch carries whatever he says, and the first frame is the
  evidence he says it from.
- B. Hold until he rules. He would be ruling on a texel arithmetic and a
  band median that are not the same quantity (queue 299 says so at 121 to
  124), with no frame; D23's test is a frame beside the sheet; nothing
  renders while held. Circular. REFUSED.
- C. A smaller constant chosen so `band.ground.p50` lands near 0.373. A
  bound set from arithmetic over a quantity that is not the one measured
  (rule 2), and a taste call that D23 names as his. REFUSED.

RULED: A. Parity lands exactly as the builder applied it, no number invented,
and the prediction at 299 lines 107 to 128 stands as the falsifiable claim
the run answers.

WITH THREE CONDITIONS ON THE REPORT, because the residual is the one thing
here that reaches him and it was about to reach him under a wrong label.
1. It is labelled PARTIAL: "the legacy build's dry ground grade; the wetness
   darkening the legacy build stacked on top at wetness 0.6 (a further 0.73
   in gamma) is not yet carried on this side, queue 186". A number he judges
   as final with one term owed to it is a number he will have to judge
   twice.
2. He is asked the D23 question and only that: the frame beside the Hook
   sheet, which way does the gap run. He is NOT asked for a constant. If he
   names one anyway it is recorded as his, with the date, and it goes where
   queue 302 puts the numbers, not into a legacy C# file.
3. The frame is opened by the resident BEFORE any number is quoted (299's
   acceptance THREE, rule 4), and the ground numbers of section 10 go beside
   `ce99814`'s, residuals stated, no bound.

WHAT THIS IS NOT. It is not a ruling that the legacy grade is right for the
Hook sheet. The item's own prediction is that it overshoots, and the frame
may show that. When it does, the finding is about the number, and the number
is his.

## 4. Call 2: concrete is a wetness list doing brightness duty, named by its own author, and it is not split tonight

THE FACTS. `AssetLibrary.cs` 908 to 911: "Ground the rain lands on. Walls
and roofs are deliberately absent", then `WetSurfaces = { Asphalt, Sidewalk,
Kerb, Concrete }`. `BaseColour` at 553 applies `GroundGrade` to exactly that
list. 516 to 526, headed "AND ONE HONEST CONTAMINATION OF THAT CONTROL":
`mat_concrete` is one shared material for the pavement and the walls built
from it, it is 4 per cent of the noon facade sample in the town, "and if a
landed still shows concrete WALLS reading too dark, the fix is to split the
ground family out of `WetSurfaces` rather than to move this number".
`StreetVignetteHost.cs` 238 paints every non-decal piece with
`AssetLibrary.Material(p.Surface ?? Concrete)`, which is `BuildMaterial`
(352 to 359) and therefore `BaseColour`, so the legacy host graded the same
150 pieces the Unreal reader now grades. `SurfaceBind.h` 349 to 353 copies
the four names character for character and the suite asserts each (2564 to
2573).

SO: as PARITY it is correct, the four names are the source's four names. As
a MODEL it is a contamination: a list written for rain is being read for
brightness because the rain list happened to be the ground list, and the
person who wrote it said so and said what to do. In this street the borrowed
list touches 150 pieces that are trim, roof-level and gum, not walls
(section 2), so the frame consequence is smaller than "150 of 610, mostly
walls" made it sound and is still unmeasured.

RULED: NAMED, NOT SPLIT TONIGHT, and queue 302 is the split. Three reasons.
1. The source names the trigger and it has not fired: "if a landed still
   shows concrete WALLS reading too dark". No still exists. Splitting before
   the frame is a threshold set without a series (rule 2) on a picture
   nobody has opened (rule 4).
2. Splitting on the Unreal side alone tonight puts a third list in play
   (the legacy wet list, an Unreal grade list, an Unreal wet list for 186)
   with no guard between any two: `tools/surface-tint-check.py` compares
   tints only, by its own docstring quoted at `SurfaceBind.h` 248 to 250 and
   by grep (0 hits for the list or either constant). The g++ suite asserts
   four hand-typed names against four hand-typed names, which catches a
   typo and not a drift.
3. With Unity legacy, the right home for the list and the two constants is
   the shared spec both readers read, beside `surface_tiling` (pieces file
   line 18), under A4's "every field written out"; and concrete is ONE
   logical surface covering gum on the pavement and lintels on a wall, so a
   grade keyed on the surface name cannot be right for both. The split is
   by role or edge, which the pieces file already carries per piece
   (`"edge"`, `"bom"`). That is a Core question and a director's item, and
   it is written as 302 in section 9 with the trigger, the sub-question and
   the guard, which extends the existing tool and adds no instrument.

WHAT THE LANDING READ OWES THIS CALL. The frame looked at with the sills, the
lintels, the stall fronts and the gum in mind, and one sentence written
down: do the trim pieces read too dark. That sentence is 302's opening
reading and spends its block.

## 5. Call 3: no retirement is spent for a key; the grade is on the line by value; the tally and the readback are the next rung and 293 pays for them

WHAT LANDED. Twelve pack lines go from `tintTexel=not-built tintFrom=not-
built tintPattern=not-built roughnessTexel=not-built` (verdict 232 to 247
on `ce99814`, every RESOLVED line) to, on a ground surface,
`tintTexel=grade-on-white.104.107.112 tintFrom=textureGrade-times-
groundGrade/grade.0.41.0.42.0.44/groundGrade.0.55/linear.0.1378.0.1458.0.1626
tintPattern=pack-jpeg-times-AlbedoGradeParam/the-albedo-is-the-file-and-the-
grade-is-a-parameter-on-it roughnessTexel=from-the-pack-roughness-file/not-
computed-here` (`SurfaceBind.h` 1236 to 1251, the shape asserted at 2660 to
2678). The value carries the word, `grade-on-white`, so the same key on a
procedural line (an albedo byte) and on a pack line (a grade on a white
reference texel) cannot be read as one thing, which is the instruments.md
rule satisfied in the value the way `JPEG-BGRA8/srgb=no` already satisfies
it. A surface the pass never reached still prints `not-built` on all four
(1255 to 1258, asserted 2686 to 2691), so "no grade was set" and "the grade
is white" stay different readings. No reader parses these keys (section 2),
so nothing downstream moved.

THE CLAIM I COULD NOT FIND. The brief to me says the runtime readback rides
on a `#` comment line. There is no readback of the vector parameter:
`GetVectorParameterValue` has zero hits under `ue-probe/`. What exists is
`Bound.Graded` recorded at the set site (`VignetteShot.cpp` 3818 to 3819)
with the comment at `SurfaceBind.h` 1005 to 1011 saying the line prints what
was HANDED, not what was read back. So the grade line is a claim about the
set, verified by the suite's arithmetic, and it has no twin of
`midTexReadback` or `midTilingReadback`, which exist for the textures and the
scalars and answered `same-pointer` and `same-value` on every reached line
of `ce99814`. The vector set is three statements from those two reads, on
the same instance, so the risk tonight is small; the class of fault is the
one the 2026-09-14 leak ruling records ("the value was on the line all
along" is only true of a value something read).

WHAT IS ACTUALLY MISSING is not a key for the grade. It is the WHOLE-RUN
number: the done line at 248 carries `midParamReadback=14/14
midScalarReadback=14/14` and nothing for the grade, so "how many surfaces
were graded, of how many" is twelve lines read by eye and a zero would have
no denominator (rule 3b). Under the instruments.md rule, whole-run numbers
go on the done line.

THE PRECEDENT ON THE MONTHLY RULE, so this is ruled and not felt. Jafar's
words, `production/stages.md` 296: "no new instrument this month unless one
is retired in the batch". Two directors have already read it: the 20:01Z
ruling of 2026-09-14 ("a Check inside a suite that already walks these rows
... not a tool, a reader or a gate; nothing is retired because nothing is
added"), and the leak ruling of the same day ("a correct word on a key that
already existed and a count on a line that already existed ... the rule is
about instruments that can be misread"). D32 itself sits inside an existing
tool for the same reason. Under those readings a tally on the existing done
line and a readback in the existing readback block are widenings, not
instruments. The resident chose the stricter reading and routed the grade
through four dead fields. That was a defensible reading of an owner's rule
by someone who could not ask him tonight, and it produced a line that says
what it needs to say.

RULED: acceptable as landed. No retirement is spent in this batch and no key
is added tonight. The tally (`surfacesGraded=N/of`, `groundGraded=N/of` on
the materials done line) and the readback (`midGradeReadback` on the first
instance per surface, the vector twin of the two reads beside it) land WITH
queue 293, whose retirement of the read series (eleven grid cells, six fog
rungs, two cross rungs and their shot lines) is a retirement already ruled
on 2026-09-14 at 20:01Z. So the question never has to reach him as an
exception: the batch that adds the numbers retires seventeen rendered rows.
If he reads the rule so that a key is an instrument, the retirement that
pays is the same one. I name 293 and I refuse to name a second thing to
retire tonight: retiring a measurement to buy a key nobody has shown a reader
needs is the ratchet the rule exists to stop, in the other direction.

## 6. Call 4: the outbox brief register retires; the net was never a net; what the recovery does not cover was never covered, and it is queue 303

THE RECORD OF THE NET, counted off the receipts rather than remembered.
Days on which the file path has existed: 2026-09-09 onward. Days a brief
was written down it: 09, 10, 12, 14 (four). Days the file path sent it:
09, 10, 14 (three receipts named `brief-<day>`). Days it failed: one, the
12th, sixty-one hours with no run of the step (queue 291, `01c3fd57` to
`3df34890`). Days an outbox brief covered that failure: ZERO, no outbox
copy of the 12th exists. Days an outbox brief duplicated a brief the file
path delivered: TWO, the 9th (id 39 then id 56) and the 14th (id 93 then id
95, eleven seconds apart, and three more in the same register that evening).
Zero catches, two duplicates, and on the 14th five messages in a register
whose rule is one a day.

WHAT THE NET WAS. Not a mechanism: a resident writing a `.brief.md` into the
outbox by hand. Its one real property is that the bot's poll loop sweeps the
outbox on the PC and needs no runner, where `--send-brief` is a workflow
step on the self-hosted runner (yml 602 to 683). That property is real and
it was the reason the resident reached for it on the 14th. IT SURVIVES THE
RETIREMENT: `.unprompted.md` and `.answer.md` still go by the bot's sweep.
What retires is calling such a message the brief, and the refusal says so in
its clause (`brief.py` 364 to 372: write it to `production/briefs/` for the
buttons, or send it as `.unprompted.md`), with a refusal record written
rather than silence (`outbox.py` 961 to 965).

WHY IT RETIRES, under Jafar's "retire whatever does not work".
1. His acceptance is "seven consecutive readable briefs, tapped by me"
   (`brief.py` 13 to 16). The outbox sweep hands its sender `sender(text)`
   with no keyboard, so a brief that goes that way cannot be tapped and
   cannot count. A route that cannot contribute to the only measure is a
   route that does not work FOR THE THING IT IS NAMED AFTER.
2. Its measured effect was the duplicate, twice, and the design's own
   sentence is that "a duplicate of the one message a day is itself a
   channel failure" (yml 594 to 595).
3. The rejecting case is in the suite and was watched: an unsent `.brief.md`
   in the outbox is refused with the clause (outbox selftest 2114 to 2128),
   and the accepting case first: a brief already sent out of the outbox is
   not re-refused (2085 to 2101), with the live nine of nine checked (2105 to
   2113, and by me in section 2).

WHAT THE RECOVERY COVERS AND WHAT IT DOES NOT, said in one place. It covers a
brief written on day D whose run did not happen on D and did happen on D+1,
and only that, for the reason its docstring gives and rule 2 backs. It does
NOT cover the shape that actually happened: the 12th had no run on the 12th
or the 13th, no brief exists for the 13th, so the 14th's run had nothing to
recover from and the 12th stays in BRIEFS WRITTEN AND NEVER SENT. The remedy
that line prints, `--send-brief 2026-09-12` from his PC, has no caller: the
day argument is parsed at `telegram-bot.py` 3616 to 3618 and nothing in the
tree passes one. Built, not running (rule 6). The net did not cover this
either, so nothing is lost tonight, and the brief's single point of failure,
the runner, is now the only route and is named.

RULED: the retirement lands as built. Two things follow.
1. On a runner-dark day the day's message goes ONCE, as `.unprompted.md`,
   and NO brief file is written for that day, so the file path cannot
   duplicate it when the runner returns; the streak then has a hole for a
   day the runner was dark, which is the truth, and the dossier line counts
   nothing false because nothing was written. This is dictated into 291's
   status in section 9.
2. Queue 303: a `workflow_dispatch` input on the EXISTING brief step,
   passed as the day argument the sender already takes, so "send the 12th"
   is one click of Jafar's rather than a command nobody runs. No second
   sender, no new step, no new instrument. Whether the 12th's brief itself
   goes is the Producer's call in the next brief: its ask was done on the
   14th (`brief.py` 273 to 280) and a three-day-old ask on his phone is not
   a delivery.

## 7. Call 5: what is wrong in the diff, ranked, and which of it blocks

1. A GUARD THAT CANNOT FIRE, `vignette-spec-test.cpp` 2555:

       Check(!std::fabs(Road.R - (0.50707851 * 0.55)) < 1e-4, ...)

   `!` binds before `<`, so this is `(!fabs(...)) < 1e-4`: `!` of a nonzero
   double is `false`, `false < 1e-4` is `0 < 0.0001`, true. The check passes
   whenever the difference is ANY nonzero amount and fails only on exact
   equality. A wrong-order implementation would compute
   `SrgbToLinear(0.74) * 0.55`, which differs from the eight-digit hand
   constant times 0.55 at the ninth decimal, is nonzero, and PASSES. So the
   rejecting case for the order is decorative; what actually pins the order
   is check 10's `fabs(Road.R - 0.13782717) < 1e-7` at 2542 to 2547, which
   excludes 0.2789 by a wide margin. Rule 5b: a guard must be able to see
   the case it asserts. `verify.py` 1028 compiles this suite with `-Wall`,
   under which GCC prints `logical-not-parentheses` for exactly this shape;
   the resident's separate compile may not have carried it. ONE-LINE FIX,
   dictated in section 9, hand-applied by the resident under CLAUDE.md's
   one-line-fix clause, recompiled, count still 447, zero failures. A
   CONDITION OF LANDING.

2. THE RESIDUAL'S LABEL. Section 3, condition 1: partial parity, wetness
   owed. A CONDITION OF LANDING, on the report and not on the code.

3. NO WHOLE-RUN TALLY AND NO READBACK OF THE VECTOR PARAMETER. Section 5.
   Next rung, lands with 293. Not blocking.

4. A WRONG WORD ON AN UNREACHED PATH. `SurfaceBind.h` 1245 prints
   `/groundGrade.not-a-ground-surface` whenever `bGround` is false, and
   `AlbedoGradeFor` returns before setting `bGround` for an untextured
   surface (514 to 518), so a kerb whose albedo failed to bind would print
   "not a ground surface" about a ground surface. Unreachable on `ce99814`
   (12 of 12 albedos bound) and today; the honest word when it is reached is
   `not-applied-because-white`. Fix when the line is next touched (293's
   batch). Not blocking.

5. A TESTED BRANCH NO RUN CALLS. `AlbedoGradeFor`'s decal branch (509 to
   513) is asserted at 2614 to 2622 and never reached by the runtime: the
   decal path (3748 to 3775) builds its own instance and sets no grade,
   which the comment at 462 to 468 says. Honest, and rule 6 applies to the
   string: no line will ever print
   `white/EmitDecal-sets-no-material-colour...`. Noted so nobody greps for
   it in a verdict. Not blocking.

6. THE TWO CORRECTIONS TO THE ITEMS. "Most of them WALLS" (299, and the
   brief to me) and "the outbox delivered when the file path sent nothing"
   (the brief to me; 291 does not say it but its status is where the next
   reader will look). Both dictated in section 9. Conditions of landing as
   text.

7. THE COMMENT AT `SurfaceBind.h` 1201 TO 1206 measures the longest line at
   398 characters, names 420 as too tight and sizes the buffer at 560; read
   twice, it is consistent. Not a finding.

8. `materialConnections` 14 to 16: read at `make_base_material.py` 111, 1056
   and 3138 to 3144; the three comments say why and nothing compares against
   the literal. Not a finding.

Nothing in the diff loosens a bound, moves a threshold, or weakens an
instrument. The four fields go from dead to live and the `not-built` case
keeps its words.

## 8. Rule 5b: accepting and rejecting cases, and which run proves each

- The default: accepting, `Fresh` white in both spaces and as a texel (2490
  to 2501); rejecting, the generator's selftest refuses a non-white default
  as a number (1310 to 1314). Both in the container tonight.
- The order: accepting, 2542 to 2550; rejecting, 2555 AFTER the fix in
  section 9 (`> 1e-4` against the wrong-order value 0.2789, which check 10
  already excludes). Recompile printed.
- The ground list: four members asserted one at a time and five
  non-members beside them (2564 to 2584). Rejecting case is the file's.
- The double grade: `interior` white by the parameter and 31.22.14 by the
  texel (2590 to 2609).
- The line: a graded pack surface has no `not-built` left (2660 to 2662);
  a surface never reached still prints it on all four (2686 to 2691).
- The outbox retirement: accepting first, an already-sent brief is not
  re-refused and the live nine of nine carry receipts (2085 to 2113);
  rejecting, an unsent `.brief.md` is refused with the clause (2114 to
  2128). 115 to 119 cases, 0 failures, printed by the resident.
- The recovery: `brief.py --selftest` 45 to 57, `notMeasured=1`, and the
  resident names which one is not measured in the commit message (I could
  not run it; a not-measured case is a case, and rule 3b says it is
  counted and named).
- The union: `producer-day.py --selftest` 14 to 19 with the planted
  half-tree (740 to 762) printing `briefsSentEver=nothing-measured` and the
  live tree reading both places, `notMeasured=0`.
- The frame: NOT PROVEN BY ANY OF THE ABOVE. The suite's own comment at
  2475 to 2479 says so, and section 10 is the only proof of the change.

## 9. Dictated text

Every replacement verbatim; where a sentence is replaced, grep the sentence
and replace every copy (rule 1), counts into the commit message.

1. `ue-probe/tests/vignette-spec-test.cpp` 2555, the one line, becomes:

       Check(std::fabs(Road.R - (0.50707851 * 0.55)) > 1e-4,

   The two message lines below it stay. Recompile; 447 checks, 0 failures,
   pasted into the commit message with the before line quoted.

2. Queue 299, appended to its status:

       RULED 2026-09-15 00:52Z (decision-2026-09-15-ruling-the-grade-lands-
       as-the-legacy-number-and-the-outbox-brief-was-never-a-net.md): lands
       as parity, no constant chosen, the residual to Jafar labelled PARTIAL
       because the legacy build stacks LightModel.AlbedoScale(0.6) = 0.73 on
       the ground family at the judged wetness and this side has no wetness
       read site (queue 186). He is asked which way the gap runs, not for a
       number. AND A CORRECTION TO THE RISK PARAGRAPH ABOVE, counted off the
       pieces file: the 150 concrete pieces are 72 sills and lintels, 6
       stall fronts, 4 parapet and coping, 2 roofdecks, 1 kiosk plinth, 5
       chimney pots and 60 chewing-gum discs. NOT ONE IS A WALL FACE; the
       wall faces wear brick_red, brick_grey, plaster and wood. "Most of
       those pieces are WALLS" is replaced by: 84 are wall trim, 7 are at
       roof level, 61 sit on the pavement. Pixel share unmeasured. The split
       of the ground family from the wetness list is queue 302 and waits on
       this item's frame.

3. Queue 291, appended to its status:

       RULED 2026-09-15 00:52Z (decision-2026-09-15-ruling-the-grade-lands-
       as-the-legacy-number-and-the-outbox-brief-was-never-a-net.md): the
       outbox brief register retires as built. Its record since the daily
       path opened on 2026-09-09: zero catches (no copy of the 12th was
       written) and two duplicates (the 9th, id 39 then id 56; the 14th, id
       93 then id 95). THE FILE PATH DID SEND ON THE 9TH: brief-2026-09-09.
       receipt.txt, messageId 56, 10:55:44Z. On a runner-dark day the day's
       message goes ONCE as .unprompted.md and no brief file is written for
       that day, so the file path cannot duplicate it when the runner
       returns; the streak then carries a true hole. The one-day recovery
       does not reach the 12th (no brief on the 13th to recover from) and
       --send-brief <day> has no caller: queue 303. The 12th's brief is not
       sent by this item; the Producer decides in the next brief whether to
       say one was missed.

4. Queue 293, appended to its spec:

       AND, RULED 2026-09-15 00:52Z: the materials done line gains
       surfacesGraded=N/of and groundGraded=N/of, whole-run tallies of the
       per-surface grade lines queue 299 made live, and the surface line
       gains midGradeReadback of the AlbedoGrade parameter on the first
       instance per surface, the vector twin of midTexReadback and
       midTilingReadback, IN THE SAME BATCH as this item's retirement of the
       read series, so the tally and the readback are paid for by a
       retirement already ruled and the monthly rule is met in the batch it
       is measured in. The word at SurfaceBind.h 1245 for an untextured
       ground surface becomes not-applied-because-white in the same touch.

5. The two new queue items, front matter per `production/queue/README.md`:

       302-the-ground-family-is-a-grade-list-wearing-a-wetness-lists-name.md
       line: engine (SurfaceBind.h, the shared spec, tools/surface-tint-check.py)
       spec: IsGroundSurface copies AssetLibrary.WetSurfaces character for
         character, and that list was written for rain ("Ground the rain
         lands on. Walls and roofs are deliberately absent", AssetLibrary.cs
         908 to 911) and borrowed for brightness by BaseColour; its author
         named the borrowing a contamination and named the fix (516 to 526:
         split the ground family out of WetSurfaces, do not move the
         number). In the vignette the 150 concrete pieces are 72 sills and
         lintels, 6 stall fronts, 4 parapet and coping, 2 roofdecks, 1 kiosk
         plinth, 5 chimney pots and 60 chewing-gum discs; none is a wall
         face and 61 sit on the pavement. Concrete is ONE logical surface
         covering gum on the ground and lintels on a wall, so a grade keyed
         on the surface name cannot be right for both; the split is by role
         or edge, which the pieces file carries per piece. Unity is the
         legacy reference build (D16) and no run of it will land, so the
         grade's list and its two constants move out of the legacy C# table
         into the shared spec both readers read (a per-surface block beside
         surface_tiling, A4 every field written out), the Unreal reader
         reads them from there, and tools/surface-tint-check.py is extended
         INSIDE THE EXISTING TOOL to refuse a disagreement between the
         spec's list and constants and any reader's literal, accepting case
         first on the live tree. Splitting the family does not move 0.55 or
         0.74/0.76/0.80: the values are judged numbers and the judge is
         Jafar under D23.
       acceptance: first, the landed frame from 299 looked at with the
         sills, lintels, stall fronts and gum in mind, and one sentence
         written here: do the trim pieces read too dark. If not, the split
         waits and the spec move is still owed. If so, both suites green on
         the split, surface-tint-check.py shown refusing a planted
         disagreement and accepting the live tree, and a run in which the
         concrete line prints the grade the split gave it. A director's
         item, Core question, because it touches the spec contract both
         engines read.
       max_sessions: 2
       status: READY 2026-09-15, filed by the ruling of 00:52Z
         (decision-2026-09-15-ruling-the-grade-lands-as-the-legacy-number-
         and-the-outbox-brief-was-never-a-net.md). BLOCKED on 299's frame
         being looked at; the block is spent by the landing read of that
         run and by nothing else.

       303-the-briefs-only-sender-rides-the-runner-and-a-missed-day-has-no-click.md
       line: tools and channel
       spec: --send-brief runs as a step of
         .github/workflows/ledger-install-supervisor-task.yml (line 683) on
         the self-hosted runner, keyed on today in UTC, with a one-day
         recovery since queue 291. A brief that misses its day by more than
         one run of that step is unsendable from anywhere in the tree: the
         remedy the dossier prints, --send-brief <day> from his PC, has no
         caller (the day argument is parsed at telegram-bot.py 3616 to 3618
         and nothing passes one). The 12th is that case: sixty-one hours
         with no run, no brief on the 13th to recover from, and it stays in
         BRIEFS WRITTEN AND NEVER SENT until somebody types the command on
         his machine. Add a workflow_dispatch input to the EXISTING step, a
         day, empty by default, passed as the day argument the sender
         already takes. No second sender, no new step, no new instrument.
         The outbox brief register is retired (291) and is not the answer:
         it carries no buttons and its record is zero catches and two
         duplicates.
       acceptance: a dispatch with the input set to a day whose brief is
         unsent produces exactly one receipt for that day with buttons=2/2;
         a second dispatch for the same day prints ALREADY SENT and sends
         nothing; both watched on the live path, accepting first. Whether
         the 12th's brief itself goes is the Producer's call, not this
         item's.
       max_sessions: 1
       status: READY 2026-09-15, filed by the ruling of 00:52Z. Not blocking.

6. `ledger-v2/respec/decision-register/rulings-log.md`, one line after the
   2026-09-14 20:01Z entry, in the file's form (the applying session of the
   20:01Z ruling could not write its line either, section CORRECTION of that
   record, so both may be owed; the resident writes both if the file is
   free and says so if it is not):

       - **2026-09-15** the grade lands as the legacy build's number and not
         as a bar: queue 299 applied as parity, residual to Jafar labelled
         partial (wetness owed, 186); concrete named a wetness list doing
         brightness duty and filed as 302, split waits on the frame; no
         retirement spent for a key, tally and readback land with 293; the
         outbox brief register retires (291) on a record of zero catches
         and two duplicates, the missed-day click is 303
         `game-design/decision-2026-09-15-ruling-the-grade-lands-as-the-legacy-number-and-the-outbox-brief-was-never-a-net.md`

7. `production/quality-ladder.md`, one row appended to the table, and the
   paragraph under "What is deliberately NOT on the ladder yet" gains the
   sentence "The engine was decided on 2026-09-10 (D16); rows for the
   visual aspects begin below with the first one that shipped a frame."

       | Pack surfaces, albedo (queue 299) | Twelve pack surfaces carry the legacy build's dry grade through one vector parameter, tested in the container, printed per surface on the landed line. | The grade's list and constants in the shared spec both readers read, split by role and not by rain (302); the wetness term this side does not carry (186); a whole-run tally and a readback of the parameter on the done line (with 293); then the number itself, judged by Jafar against the Hook sheet under D23, recorded as his. |

## 10. The landing read, so the next director reads the run and not the colour

The sha captured before dispatch, the run watched by ancestry. On landing,
IN THIS ORDER:

(a) THE FRAME FIRST. `ue-vign_hook_day.png` opened and looked at beside
    `ce99814`'s copy before any number below is quoted (299 acceptance
    THREE, rule 4). One sentence each on the kerb, the road, the trim
    (sills, lintels, stall fronts), the railings and bins (metal), and the
    plaster faces. The sentence on the trim is 302's opening reading.
(b) THE TWELVE LINES. Every RESOLVED surface line free of `not-built`; the
    four ground lines carry `tintTexel=grade-on-white.104.107.112` and
    `/groundGrade.0.55`; the eight others carry `189.194.204` and
    `textureGrade-only`; `interior` still `tintTexel=31.22.14` and
    `paint_yellow` still `147.127.35` with
    `AlbedoGradeParam.white-because-the-product-is-already-in-this-texel`
    on both; `card` and `multiply` still `not-built` on all four. Twelve of
    twelve, and the count printed, not the adjective.
(c) THE MATERIAL. `materialStatus=MADE` with connections 16/16 where
    `ce99814` read 14/14.
(d) THE GROUND MOVED, AND HOW MUCH, on `vign_hook_day` beside line 193 of
    `ce99814`: `band.ground.p50` beside 0.5117 and the sheet's 0.373,
    direction down, residual to each stated, NO BOUND; `band.ground.p05`
    beside 0.2006; `band.ground.meanLuma` beside 0.4501;
    `band.ground.meanRGB` beside 114.8/114.7/115.5, where the blue channel
    should fall least because the grade is 0.74/0.76/0.80.
(e) "TOO DARK" AS A NUMBER: `shotMinLuma` beside 0.0777, `shotClipLoAll`
    beside 0/921600, and the first of `shotLumaBands` beside 2440 of
    921600. Reported, not bounded.
(f) THE CONTROL THAT MUST NOT MOVE: `band.skyCentre.p50` beside 0.8035 and
    `band.skyCentre.meanLuma` beside 0.7975. Nothing in the sky wears a
    grade; if the sky moved, suspect the exposure or the instrument before
    the grade (rule 3). `shotExposurePinRead` still 0.3000/0.3000.
(g) The control quads on whichever camera shows them, unchanged: they set
    no grade and the default is white.
(h) NO-READ escalated per C4 rather than quoted around.

Then the frame pair to Jafar, Producer's channel, per the 16:25Z ruling's
item 7, with the label of section 3 condition 1 and the question of
condition 2, and nothing else asked.

## 11. The quality ladder at close

First working, and named as such. The best available result for this aspect
is not a constant copied from a legacy table; it is a number Jafar has
judged against the sheet, living in the shared spec, with the ground family
split from the rain family, the wetness term carried on this side, a tally
and a readback proving the parameter took, and a texture under it that has
something in it (300). Tonight takes the first rung of that ladder, which is
the only one that can be taken without a frame: it makes the parameter exist,
proves it in the container, and renders the frame the rest is judged from.
The rung after it is the frame itself (section 10), then 302 and 293, then
186, then 300, then his number. None of those is blank.

## 12. For the commit message

Queue 299 gives M_LedgerSurface the vector parameter the legacy build's
albedo grade had nowhere to land in, sets it per surface from the tested
header (TextureGrade 0.74/0.76/0.80 in gamma, times GroundGrade 0.55 for the
four ground names, converted once to linear), turns four dead fields live on
twelve verdict lines without a new key, and predicts before the run that the
legacy grade overshoots the Hook sheet on band.ground.p50 (0.512 against
0.373). Ruled 2026-09-15 00:52Z (decision-2026-09-15-ruling-the-grade-lands-
as-the-legacy-number-and-the-outbox-brief-was-never-a-net.md): it lands as
parity with the legacy build's DRY grade, no constant chosen, and the
residual goes to Jafar labelled partial because this side carries no wetness
term (186); the 150 concrete pieces it darkens are trim, roof-level and gum
and not walls, the rain list doing brightness duty is queue 302 and waits on
the frame; no retirement is spent for a key, the tally and the readback land
with 293. Queue 291 retires the outbox brief register on a record of zero
catches and two duplicates since the daily path opened, adds a one-day
recovery to the sender that already takes a day, makes exit 6 say so on the
run and in the dossier, and reads receipts from both places they land; the
missed-day click is 303. One test line fixed by hand (2555, a logical-not
that could not fire); suites 447/447, 149, 57 (1 not measured, named), 19,
119, 28.

## 13. Refused

- Any constant chosen here to land on 0.373, or any bound on the residual.
- Holding the render until Jafar has ruled on arithmetic; D23 names a frame.
- Splitting the ground family tonight, on either side, before a still shows
  the trim.
- A new verdict key tonight, or a retirement named tonight to buy one.
- Reading the grade line as a readback; it is the value handed.
- Keeping the outbox brief register as a hedge, or a second sender of the
  brief file in the bot's loop.
- Sending the 12th's brief by this ruling.
- Any sentence in the report to Jafar that calls tonight's frame full
  parity.

<!--RULING spawn=2026-09-15T00:52:56Z-->
