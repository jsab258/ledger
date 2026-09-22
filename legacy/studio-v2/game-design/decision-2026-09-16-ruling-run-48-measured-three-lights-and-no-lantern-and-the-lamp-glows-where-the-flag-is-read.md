# Ruling, 2026-09-16 (06:35Z): run 48 measured three lights and no lantern, the control needs two statistics and no new bound, the lamp glows where its flag is already read, and the next dispatch holds its exposure

STATUS: LOG, 2026-09-16. NOT CURRENT once the first landed run whose commit
CONTAINS the batch this ruling orders has been read against section 8; from
then the verdict file, the g++ suites and the queue items in section 10 are
the reading copies and this is the record of what was ruled and why.

Director ruling on the run 48 night-lighting batch. Two mechanical triggers
fired: a landing that changes a conclusion (`lightsAboveFloor=17/28` on run
48, commit `c36857c0`, verdict `4e257ee`, is not the run's reading), and gated
spec and engine work (queues 333 and 334) wanting an approach ruled before a
builder starts. Five questions were asked and each is answered in its own
section; a sixth thing the questions did not ask is section 5, because
without it the next run measures nothing about a lantern either.

Author: tier-1 director, stamp at the foot naming row 665 of
`.claude/agent-log.tsv` (`2026-09-16T06:35:34Z` TAB `studio-director` TAB
`fable` TAB `default` TAB `a825ff542a7789807`), the newest row in the log.
The gate's reference commit is the newest commit that touched a reviewed
scope (`verify.py` 4802), which is `c5ecf3ce` at epoch 1789532392, that is
04:19:52Z, the queue 326 landing; row 665 is newer by two hours and a
quarter. HEAD itself moved to `87169863` at 06:38:07Z, three minutes after
the spawn, and that commit is the run 48 read (documents), so it does not
move the reference. This director has no shell: every number below was read
off the committed verdict by line, every source claim off the file at the
line cited, and the four frames were opened. Nothing here rests on the
caller's table; where a number is the caller's and was not re-derived it
says so.

VERDICT IN ONE LINE: the caller's 17-to-3 correction is right in its
numerator and wrong in its denominator, and its sentence about lanterns is
wrong in kind: run 48 measured THREE lights of 42 probed, all three window
practicals at one shot, and measured NO lantern at all, 0 of 24 probed, which
is "nothing measured" and not "zero"; queue 332 needs both statistics, each
for its own question, and no absolute bound; queue 333 is the narrower
change, in the engine where the flag is already half-read, and it is
structural by the wetness precedent and not by a spec change; the next
dispatch carries 329, 332, a one-line exposure hold in the probe pass, 333
and 334 in that build order, batched, and the figure enters now as queue 028
item 1 re-scoped, its bake in parallel and its spec half behind the Core
changes already in flight.

## 0. What was opened

`production/d1-probe/ue-vignette-verdict.txt`: line 1 (names `4e257ee`),
lines 275 to 322 (the 48 light lines, by key), 323 to 328 (the six
`lightfloor` lines), 329 (the done line). `ue-pinset_night_3.png`,
`ue-pinset_night_4.png`, `ue-vign_camA_night.png`, `ue-vign_camB_night.png`
opened and looked at before any number was read.

`FrameStats.h` 300 to 440 (`LightDelta`, `MeasureLightDelta`), 448 to 545
(`LightReadEdge`, `LightFloor`, `LightFloorUsable`, `LightFloorAddLight`),
by grep 560 to 925 (the three formatters). `VignetteShot.cpp` 355 to 400
(the exposure rate and the reasoned absence of a value), 1280 to 1349 (the
spawn loop's tail, the H4 lantern block at 1310 to 1327, H5 at 1329), 1788
to 1800 (`ApplyCondition`'s light visibility), 2088 to 2200 (the per-shot
exposure writes and readback), 2764 to 2769 (`ShouldProbeShot`), 3232 to
3420 (the probe pass whole). `SurfaceBind.h` 1226 to 1249 (the four paint
routes). `make_base_material.py` 148 to 187 (the parameter contract and the
two precedents), 1078 to 1091 (the connection denominator's history).
`StreetVignette.cs` 80 to 90 (the `Emissive` field, whose comment reads "the
lantern bowls, and nothing else") and 1196 to 1222 (the lantern piece,
`Surface = "metal"`, `Emissive = true`). `StreetVignettePieces.cs` by grep.
`CoreTests/Program.cs` 19904 to 19916 and 20194 to 20206 (the two assertions
the caller named) and by grep for lantern and emissive (20338 to 20341:
`lanterns == 4`). `vignette-scene.json` 250 to 282 (the lighting block), 884
to 923 (`overcast_day`, `wet_night`), the id list 841 to 1422 (the shot
order: `pinset_night_1..4` at indices 30, 33, 36, 39, confirmed).

D41, D45 whole; D28 40 to 47; D29 22 to 40; D40 64 to 72; the 2026-09-10
exposure ladder ruling 112 to 141; the 2026-09-16 03:27Z ruling 1 to 90 and
its section list; `verify.py` 4802 to 4821 and 5722 to 5770 (the gate's
reference and stamp rules); `docs-check.py` by grep (the banner form).
Queues 028, 276, 319 (head), 325, 326, 329, 332, 333, 334 whole.
`license-allowlist.md` whole (line 6 reads "Mixamo animations").
`production/quality-ladder.md` 1 to 60 and 110 to 135. `production/NOW.md`
1 to 110. `.claude/agent-log.tsv` 655 to 666. `.git/logs/HEAD` 118 to 131.
`ledger/Assets/Characters/` by glob (91 entries, 18 top-level bodies).

Greps, this session, with counts: `SkeletalMesh|USkeletalMesh|FBX|AnimSequence|\bBone\b`
over `ue-probe/Source`: 0 files. `emissive|EmissiveColor|selfillum`
case-insensitive over `ue-probe/Source`: 10 lines in 2 files, all in
`VignetteShot.cpp` 1310 to 1317 (the H4 block) and `VignetteSpec.h` 228 to
753 (parsing and counting); over `make_base_material.py`: 0. `dusk|Dusk`
over `vignette-scene.json`: 0. `Mixamo` over the decision register: one
hit, D29 line 30. `glTF` in `import_prop_meshes.py`: the magic check at 684.
`production/queue/33[5-9]*`: none, so 335 is free.

## 1. Question 1: the reading of run 48

### 1.1 The caller's classification, re-derived

The 17 YES verdicts, by line, with the number that classifies each:

    line  shot             light         meanOffFull  deltaMeanFull  win at edge (light..vs..control)   class
    278   vign_camA_night  lantern2       0.00075     +0.09563       122321..vs..15 at 32                BLANK OFF FRAME
    279   vign_camA_night  lantern3       0.00075     +0.09563       122321..vs..15 at 32                BLANK OFF FRAME
    281   vign_camA_night  interior2      0.00075     +0.09563       122321..vs..15 at 32                BLANK OFF FRAME
    284   vign_camB_night  lantern0       0.02398     +0.16495       921201..vs..921200 at 16            1 pixel over a swung control
    286   vign_camB_night  lantern2       0.02392     +0.16501       921202..vs..921200 at 16            2 pixels
    287   vign_camB_night  lantern3       0.02397     +0.16496       781307..vs..781254 at 32            53 pixels
    288   vign_camB_night  interior0      0.02400     +0.16493       921202..vs..921200 at 16            2 pixels
    289   vign_camB_night  interior2      0.02392     +0.16494       781360..vs..781254 at 32            106 pixels
    290   vign_camB_night  interior5      0.02396     +0.16496       921201..vs..921200 at 16            1 pixel
    313   pinset_night_3   interior2      0.00152     +0.17807       247746..vs..1 at 32                 BLANK OFF FRAME
    314   pinset_night_3   interior5      0.00152     +0.17807       247746..vs..1 at 32                 BLANK OFF FRAME
    316   pinset_night_4   lantern0       0.00152     +0.16786       224533..vs..1 at 32                 BLANK OFF FRAME
    317   pinset_night_4   lantern1       0.00152     +0.16786       224533..vs..1 at 32                 BLANK OFF FRAME
    318   pinset_night_4   lantern2       0.00152     +0.16786       224533..vs..1 at 32                 BLANK OFF FRAME
    320   pinset_night_4   interior0      0.15333     +0.01605       156..vs..16 at 16                   MEASURED, margin 140 px
    321   pinset_night_4   interior2      0.15278     +0.01659       121..vs..16 at 16                   MEASURED, margin 105 px
    322   pinset_night_4   interior5     0.15916     +0.01022       22..vs..16 at 16                    MEASURED, margin 6 px

Eight blank, six over a swung control, three measured: the caller's
partition of the seventeen is confirmed line by line. Two tells the caller
did not print are worth the record. The three camA blanks carry ONE
histogram (`903409/772986/611899/467359/271182/122321`) three times, and the
three pinset_4 blanks carry one (`921600/921430/906762/761807/473203/224533`)
three times: a blank is the same frame whichever light was switched off,
which is the pairwise-identical tell queue 329 already names. And the six
camB wins are surpluses of 1, 2, 53, 2, 106 and 1 pixels over a control that
moved 921200 pixels at the 16-code edge and 781254 at the 32-code edge, with
`lightFloorCtrlDarker=0/921600`: not one pixel of the reference was darker
than the control's re-render, which is a uniform shift and not noise.

### 1.2 What the caller did not classify: the eleven NO verdicts

A NO reads as "this light did not beat its floor". Ten of the eleven are not
that.

    line  shot             light      deltaMeanFull  darkerWithLightOn   what it is
    276   vign_camA_night  lantern0     -0.15484     921600/921600       OFF frame brighter everywhere: the exposure moved
    277   vign_camA_night  lantern1     -0.15481     921582/921600       same
    280   vign_camA_night  interior0    -0.15489     921600/921600       same
    282   vign_camA_night  interior5    -0.15491     921600/921600       same
    285   vign_camB_night  lantern1     +0.00011     336888/921600       noise-shaped, under a control that is void
    308   pinset_night_3   lantern0     -0.00562     831241/921600       under a control that drifted +0.02572
    309   pinset_night_3   lantern1     -0.03806     921366/921600       OFF frame brighter: the exposure moved
    310   pinset_night_3   lantern2     -0.03206     921222/921600       same
    311   pinset_night_3   lantern3     +0.01793       1598/921600       a real-looking rise, lost to the drifted floor (tie at 32, 358 vs 92430 at 16)
    312   pinset_night_3   interior0    +0.01023      10226/921600       same shape, same fate
    319   pinset_night_4   lantern3     -0.03335     921457/921600       OFF frame brighter: the exposure moved

The header's own comment at `FrameStats.h` 341 to 343 says it: pixels that
got brighter with the light OFF are "physically impossible for a light in
isolation, so a non-trivial count here is the auto-exposure compensating and
the whole difference is suspect". Seven of the eleven NOs have that count at
or above 831241 of 921600. They are not readings of a light. Line 311 is the
opposite case and the more interesting one: `pinset_night_3`'s lantern3 rose
+0.01793 in whole-frame mean with `RoseAtLeast=904882/786369/375834/172055/358/1`,
the same shape and size as the three window practicals that WON at
`pinset_night_4` (+0.01605, `891757/711832/296409/168129/156/0`), and it
lost only because its shot's control had drifted by +0.02572 and put the
16-code floor at 92430. So the drifted control did not merely void six false
YESes at camB; at pinset_3 it hid what may be the run's one lantern reading.
"May be" is the whole claim: under that control it is not a measurement.

### 1.3 The ruling on the number

The honest partition of the 42 probed lights, under the rules queues 329 and
332 will land (section 2 states them exactly):

    nothing measured, reference or control blank (pinset_night_1, _2)     14
    nothing measured, OFF frame blank (329)                                 8
    nothing measured, OFF frame brighter beyond the control's gap (332)     7
    nothing measured, control disagrees by more than the surplus (332)     10
    MEASURED                                                                3
      of which above the floor                                              3
                                                                           42

By kind: lanterns 24 probed, 0 measured (8 in blank shots, 5 blank OFF
frames, 5 swung, 6 under a void control). Practicals 18 probed, 3 measured,
3 above the floor, all at `pinset_night_4`.

RULED: the run's reading is `lightsAboveFloor=3/3` over `lightsMeasured=3/42`,
and the sentence to carry is "run 48 measured three lights, all window
practicals at one shot, and measured no lantern". "3 of 28" is refused as
the headline: 28 is the count of lights in shots the current rule calls
usable, and 25 of those 28 were not measured, so "3 of 28" reads as
twenty-five lights that failed when the truth is twenty-five lights nobody
measured. "Zero lanterns survive anywhere" is refused for the same reason in
the other direction: rule 3b, a zero needs a denominator, and the
denominator of measured lanterns is zero, so the word is "nothing measured"
and not "zero". The caller neither over-corrected nor finished correcting;
the correction stopped one denominator short.

One caveat carried and not acted on: line 322's win is 22 pixels against 16
at the 16-code edge, a margin of six. The rule as landed under the 03:27Z
ruling is strict integer exceedance with no epsilon and it was ruled right
there; a six-pixel margin is what a rule without a noise model produces at
the edge of the noise, and the instrument prints the margin
(`lightVsFloorPx`) so the reader sees it. No bound is set on it here. The
next rung is section 11.

### 1.4 The second and third conclusions, confirmed in the source

The lamp finding. `VignetteShot.cpp` 1310 to 1327 is the whole of what
`Emissive` does in the emitter: `if (!P.Emissive) { continue; }` and a
`SpawnPointLight` 0.05 m below the piece. The grep in section 0 returns no
other reader of the flag in the engine and none in the material generator.
The piece is `Surface = "metal"` (`StreetVignette.cs` 1215) and takes the
metal pack route like every other metal box. A tonemap is monotone, so a
surface darker than the sky behind it stays darker at every exposure; the
caller's self-correction stands and is recorded: exposure was not the cause,
and the builder that refused the brief was right on both grounds. The
frames agree: at cam_hook both lamp heads are dark rectangles on dark poles
against a pale sky, and the only warm thing in any of the four frames is
the window glint at the right of `vign_camA_night`. The caller's pixel
counts (26 pixels at R minus B of 20 or more in `pinset_night_3`, the
window practical at 1045..1051 by 170..173 in camA) are the caller's; they
were not re-measured here and nothing below rests on them.

The settling series. The spec's shot ids at 1410 to 1421 put
`pinset_night_1..4` at indices 30, 33, 36 and 39 with two pinned rows
between each pair, exactly as queue 334 says. Their shot lumas (0.0015,
0.1694, 0.1796, 0.1694) are three samples each preceded by a different
pinned exposure and one blank. Confirmed: they are not 276 step 1's series
and must not be adopted as it.

## 2. Question 2: what each control statistic is a statistic OF, and the screen

Three numbers already print on every `lightfloor` line, and the question
was which is the bound. None is, alone.

`lightFloorCtrlMeanFull` is `Control.MeanDeltaFull` (`FrameStats.h` 421):
the SIGNED mean over the full frame of per-pixel luma, reference minus
re-render. It is a statistic of the whole-frame brightness shift between two
renders that should be identical. Symmetric noise cancels in it, which is
exactly what makes it the exposure-state instrument: camA reads -0.00005
and pinset_4 +0.00003 (two renders at one exposure), camB +0.16498 and
pinset_3 +0.02572 (two renders at two exposures), pinset_1 -0.18334 and
pinset_2 +0.16784 (one render and a blank). It cannot see per-pixel noise
and is not asked to.

`lightFloorCtrlMovedAtLeast` is `Control.MovedAtLeast[e]` (355): the count
of pixels whose luma moved by at least e codes in EITHER direction. It is a
statistic of per-pixel disagreement at each magnitude, for any cause. It is
the floor a light's `RoseAtLeast` beats (326) and it does not cancel, which
is exactly what makes it the floor. Its shape tells noise from shift
without a bound: an agreeing control decays (155931 / 34286 / 5981 / 486 /
16 / 1 at pinset_4, 155759 / 49176 / 12293 / 2282 / 297 / 15 at camA); a
shifted one stays at the frame (921600 through the 8-code edge at camB,
918084 / 867248 / 601281 at pinset_3). The caller's worry that 16.9 per cent
of pinset_4's pixels "moved between two renders of an identical scene" is
the noise floor being what it is, not a fault: 1.7 per cent of the frame
moved by four codes and one pixel by thirty-two. That is the ruler's own
grain, and it is why the floor exists.

`lightFloorCtrlDarker` is `PixelsDarkerWithLightOn` (344, counted at 400 on
any negative float difference, sub-code included): the sign balance. Near a
third of the frame at the two agreeing controls (275893, 311696), 0 and 646
at the two shifted ones. A third statistic of the same two frames, useful
as a diagnostic, and it is printed already.

RULED, the screen for queue 332. The signed gap is the right QUANTITY for
the question 332 asks, because the question is "are the control's two
frames at one exposure", and the MOVED histogram stays the floor for the
question 326 asks. A shot needs both and the item is amended to say which
is which. The bound is RELATIVE and comes from the item's own sentence,
"disagrees with itself by more than the surplus it is certifying", so no
number is chosen:

  (a) a light whose whole-frame mean FELL with the light on by more than the
      control's absolute gap (`deltaMeanFull < -|ctlGap|`) was photographed
      at a different exposure from its reference: status
      `EXPOSURE-SWUNG`, nothing measured. This is the header's own darker
      rule turned from a suspicion into a status word; today it prints NO,
      which is a false negative of the same instrument that printed the
      false positives.
  (b) a light whose rise over the control's absolute gap does not itself
      exceed that gap (`deltaMeanFull - |ctlGap| <= |ctlGap|`) is certified
      by nothing: status `VOID-CONTROL`, nothing measured.
  (c) a light that passes (a) and (b) is MEASURED, and the 326 edge test
      then says YES or NO exactly as it does today.
  (d) a shot whose control certified no light reads `NOT-USABLE` with its
      gap on the line; `lightFloorShotsUsable` and the done line's
      denominators follow, and every bucket above prints its count beside
      42 so no zero is bare.

The absolute bound the caller proposed, 0.001 in the 640-fold gap between
0.00005 and 0.02572, is REFUSED for this batch and not because it would
misclassify this run (it would not): six samples, two of them blanks, is not
a series, and rule 2 says the printer ships first. The printer already
ships; the series accumulates a run at a time; if a shot-level absolute
word is ever wanted independent of any light, it is set then from the
printed column, and the relative rule above needs it for nothing.

THE FIXTURES ARE FREE. Run 48's six control lines and 42 light lines are
integers and floats on disk, and the g++ test for 332 carries them verbatim
as its fixtures, accepting case first: pinset_4's three practicals MEASURED
and YES, camB's seven VOID-CONTROL, camA's four EXPOSURE-SWUNG, and the
partition in section 1.3 summing to 42. A rule tested on the run that
motivated it, before the dispatch, is the standard the 03:27Z ruling set and
it holds here.

## 3. Question 3: queue 333, the approach

### 3.1 The premise check

A low-pressure sodium lantern at 589 nm on a five-metre column is the
period's street light and is in canon's window; the dusk frame D28 names
("wet, lamps lit, a figure in silhouette") is the frame the whole visual
slice is judged by. Nothing here touches the moat. The premise holds and
the work is on the slice Jafar ordered this morning.

### 3.2 The options

A. A new surface kind in Core. The generator emits the lit element as its
own piece (a bowl under the housing) with a surface whose name says it
emits; both engines learn the kind; the golden regenerates; `CoreTests`
gains the bowl's BOM and count. Sacrifices: a Core change with full review,
a golden change, a `SurfaceBind.h` route, a schema the Unity reader would
also have to learn (no Unity workflow exists in `.github/workflows/` today,
so that half is moot but not free), and two builder sessions before any
pixel. What it buys: the day look of an unlit bowl (pale, not metal), and a
spec that describes the fixture as two parts, which is what the fixture is.

B. The narrower change, in the engine and the material only. The piece
already carries `emissive=true`, and Core's own declaration of the field
reads "the lantern bowls, and nothing else" (`StreetVignette.cs` 89): the
spec ALREADY says these four pieces are the lit element. The emitter reads
half of the flag (a light under it) and not the other half (the piece
itself emits). So the fix is where the flag is read: `M_LedgerSurface`
gains a vector parameter `EmissiveColor`, default black, wired to its
Emissive pin (one node, one wire; the connection denominator moves 19 to 20,
which the generator's own docstring at 1083 says is not a constant); each
emissive piece gets its own material instance at spawn, the decal-card
precedent at `VignetteShot.cpp` 4089; `ApplyCondition` drives that
instance's emissive with `C.LanternsOn` beside the visibility write at 1798,
through a write-on-change guard as wetness does; the shot line reads it
back. Sacrifices: the whole box glows, housing and bowl alike, and by day
the unlit lamp stays a metal box. What it buys: no spec change, no golden,
no `CoreTests` change, `Shots.Count` 43 stands, `nightPinned == 0` stands,
and one builder session before the pixel.

C. As B, with the glow masked to the underside in the material by the
surface normal. Rejected: it encodes a lantern's anatomy into a parameter
every future emissive piece would inherit, and it is a node-graph choice
the builder should not be handed by a ruling.

### 3.3 The ruling

RULED: option B, the narrower change. The reason is not economy; it is that
the spec is not silent. Core calls the emissive pieces the lantern bowls,
and a spec that says a piece emits is not improved by a second field saying
it again. The engine has a half-implemented flag, and the fix for a
half-implemented flag is the other half. Option A is the NEXT RUNG and it
is named in section 11 (housing and bowl as two pieces, for the day look),
not taken now.

Three conditions, dictated:

  1. The emissive strength is a new number and rule 2 applies. It lives in
     the engine as a named constant beside `kLampGainUnitless`, is printed
     on the scene line, and is declared in its own comment as the first
     value of a series that has never been printed, the same class the
     spec gives `range_m` and `intensity`. It is tuned from the series the
     instrument in condition 3 prints, and not by eye toward anything.
     The colour is not a new number: it is the spec's derived 589 nm
     triple, already computed at 1313 as `Lamp`, and the line says which
     colour space it took.
  2. Default black is the accepting case and it ships tested. An instance
     that never sets the parameter renders exactly as today, asserted in
     `--selftest` as the AlbedoGrade white default is asserted; the day
     rows' controls (`band.skyCentre.p50` 0.8035 on `vign_hook_day`, unmoved
     across four runs) are the live proof, and section 8 predicts them
     unmoved.
  3. The acceptance is measured in two halves, the placement pattern of
     `.claude/rules/instruments.md`: the engine projects each lantern
     piece's box to a pixel rectangle (the camera and the piece are both
     known), and the tested header takes the rectangle and the frame and
     prints, per lantern per probed shot, the rectangle, whether it is in
     frame, the peak luma and peak R minus B inside it, the same two in a
     ring around it, and `brightestWarm=yes/no` with its stat named.
     Accepting fixture: a synthetic frame with a warm box in the rectangle.
     Rejecting fixtures: the warm box outside the rectangle (a lit window
     is not a lit lamp, and camA has one), and a rectangle off frame
     (nothing measured, printed as such). The caller's whole-frame
     warm-and-bright count prints as a second series at the caller's two
     working values and is not a gate. 333's acceptance sentence, "the
     fixture is measurably the brightest warm thing in its own
     neighbourhood", is met when the yes prints at a night row and the no
     prints at a day row of the same camera, in one run.

## 4. The D41 and D45 boundary: confirmed, with one reason changed

The caller's read: 333 and 334 are not visual under D41 because undoing them
means a spec change and a golden change rather than another render.

333: CONFIRMED STRUCTURAL, on a different reason. Under option B it touches
no spec and no golden, and it would still be structural, because Jafar
named the shape himself: wetness "added a material parameter, a generator
node and a readback key" and is structural by his boundary. 333 adds
exactly those three. It keeps its full review and this ruling is that
review of the approach; the diff review is at landing.

334: CONFIRMED STRUCTURAL as spec rows in Core, and that form is RULED over
the alternative. The alternative considered: a loop in the rig that
re-captures one condition k times with no spec rows, which would be a tool
that measures the game (D45: a test, no review) and would keep `Shots.Count`
at 43. Rejected because it puts the series in the untested layer, where "a
formatter written there ships unrun" is the standing instrument rule, and
because a shot row is already the thing the rig knows how to photograph,
wait for and print. Six consecutive rows at the END of the shot list so no
existing row's predecessor changes (a `settle_night_1..6` family at
`cam_hook` under `wet_night`, the judged night condition, unless the builder
finds `wet_night` and `pin_setter_night` identical in every field, in which
case it says so and either serves); a per-shot boolean that excludes them
from the light probe, read by `ShouldProbeShot` beside the condition's flag,
because six probed night rows would cost 48 more captures for a question
the frame alone answers; `Shots.Count` moves 43 to 49 and the two hook
counts move with it, the assertions' sentences updated in the same diff with
the arithmetic in the commit message; the series printed per row as
`shotMeanLuma` already is, and reduced in the tested layer to a done-line
key naming the first, the last, the largest consecutive step and the
statistic (last-wins, consecutive rows of one condition at one camera). Six
is a length chosen for cost, one probe-free capture each, and it is a cap:
a series still stepping at row six prints NOT-SETTLED-WITHIN-6, which is a
finding 276 step 2 says outranks the pin, and not a failure.

329 and 332: tools that measure the game. A test, no review, no ruling
record beyond this batch's stamp. The cadence gate counts `ue-probe/` lines
regardless (D45's own consequence paragraph says the gate does not yet know
the difference), so this record's stamp covers the batch's gated line count
and the resident cites it.

HOW MUCH OF THIS NEEDS A DIRECTOR AGAIN: one spawn, at the batch landing,
to review the Core and engine diffs against the approaches ruled here. The
run's read needs none unless it changes a conclusion, which is mechanical.
The figure's spec half (section 6) is a Core change and lands under the same
rule.

## 5. The thing the questions did not ask: the probe measures the exposure loop

The probe pass at `VignetteShot.cpp` 3388 to 3396 toggles a light and then
re-enters the Warm phase, and the exposure rate is snapped to 10000 on every
shot (2102 to 2105), so every OFF frame is photographed after the exposure
has fully re-adapted to a scene with one light fewer. Under AUTO that makes
every difference a light contribution plus the loop's answer to it, and
section 1.2 is what that looks like: seven lights whose OFF frame came back
brighter everywhere. With 329 and 332 landed the done line will be honest,
and it will honestly read that no lantern was measured, again, on every run
until the two halves of each difference are photographed at one exposure.

The value cannot be pinned: the file's own comment at 356 to 358 says the
adapted exposure is a render-thread quantity this process never reads, the
2026-09-10 ruling forbids deriving a night pin by name, and 276's settling
series has not been run. None of that is overturned here.

But a DIFFERENTIAL measurement does not need the value; it needs the two
frames at the SAME value, whatever it is. The cheapest decisive test, one
line and two readback keys, is to write `AutoExposureSpeedUp` and
`AutoExposureSpeedDown` to 0 at the start of the probe pass (after the
reference frame is on disk, before the control's re-render) and let the
per-shot write at 2102 restore the snap on the next shot. If the engine
holds at speed zero, the adapted exposure of the reference frame is the
exposure of every probe frame of that shot. The verdict is the six controls'
signed gaps, which is the instrument 332 names: they collapse to the
noise-shaped floor seen twice this run (about 0.00005 with the decaying
histogram) on every shot whose frames are not blank, or they do not. The
readback of the two speeds prints asked beside read, so an engine that
clamps the value says so on the line, and an engine that treats zero as
instant leaves the gaps where they are: both outcomes are readable and
neither is a guess. This is not a night pin, it does not touch
`exposure_pin`, it enters no determinism gate, and it is void as an absolute
reference. Filed as queue 335 (section 10), ordered into this dispatch,
because it is the difference between a run that can measure a lantern and a
run that cannot, at the cost of one line.

## 6. Question 5: the figure

The read-only investigation's four claims were re-checked: no skeletal
symbol anywhere under `ue-probe/Source` (0 files), the importer's GLB magic
check at `import_prop_meshes.py` 684, the decal route's own words at
`SurfaceBind.h` 1235, and 91 entries under `ledger/Assets/Characters` of
which 18 are top-level bodies (`Adam`, `Big Vegas`, `David` ... `Y Bot`).
The Masked/Opacity/Translucent grep is the investigation's and was not
repeated. The token claim is confirmed from `tools/mixamo-pick/README.md`:
the bearer token fetches NEW characters; nothing on disk needs it.

The figure item ALREADY EXISTS: queue 028 item 1, reopened by Jafar on
2026-09-14, asks for a `figures` block in `vignette-scene.json` naming a held
body, a clip, x, z and facing, with sizes from the fbx manifest, and then
placement "through the existing character path", which was Unity's. The
ladder row "Character: none placed (not yet admissible)" points at it.
Filing a new item beside it would be the fault queue 275 records.

RULED: the figure enters NOW as queue 028 item 1 re-scoped for the probe,
in two halves with different owners and different gates:

  Half one, the bake, a tool, starts now in parallel with everything else
  because it touches nothing the other builders hold: a Blender step (the
  `ledger-art-blender-preview.yml` workflow already runs Blender in CI)
  takes one held body and one clip at one named frame from the files on
  disk, applies the pose, and exports a static GLB under the props path the
  importer already reads. The pose is chosen for the frame D28 names, a
  figure under the far lamp with its back half-turned, and the item names
  the body, the clip and the frame so nothing is invented. A silhouette is
  a still; no skeletal path is needed for the frame Jafar judges by, and
  the decal route stays refused for the reason the investigation gave.

  Half two, the spec, is Core: the `figures` block 028 asked for, emitted by
  the generator as a prop piece (shape mesh, the GLB asset, a dark tint
  surface, since a silhouette needs no cloth), golden regenerated, the
  piece count asserted. It waits for the 333 and 334 Core changes to land
  because two builders in one Core file at once is the 2026-09-15 22:10Z
  incident, and for no other reason: it is on the same rung as the lamp,
  not the next one, because the frame is "lamps lit, a figure in
  silhouette" and not one and then the other.

THE ALLOWLIST LINE IS STALE AND IS CORRECTED, NOT RULED. Line 6 reads
"Characters: MetaHuman ... Character Creator 4 exports ... Mixamo
animations." CLAUDE.md section 0, approved and newer, reads "Characters and
animations come from Mixamo with Jafar's account". D29 line 30 already
names "the Mixamo entry in the licence allowlist" as the implied answer for
the eighty-nine bodies nobody wrote down. Two laws disagree on Mixamo
bodies and the newer, more specific one is section 0; under D43 the line is
corrected to "Mixamo characters and animations", the correcting commit
cites Adobe's Mixamo terms in one sentence, and the brief reports it as a
correction, not a question. Nothing is purchased and no account is touched.

The dusk frame has no reference sheet. The Hook sheet is a day frame with
measured numbers; D41's first path ("send the pair when you believe it
matches the reference") has no dusk pair to send. The judge for the dusk
frame is D41's own instruction, "judge it the way I would, not only by
number", against art-direction R-B3's sodium description, and the sheet gap
is a blank rung: section 11 names it.

## 7. Queue 325's second half: what rides this dispatch and what waits

The blank moved (run 47 blanked 2 and 3, run 48 blanked 1), so it is a race
and not a scene. 329 makes a blank frame never a measurement, which is the
half that protects the channel. The DIAGNOSIS needs a key that tells "not
ready" from "black", and the rig already holds the ingredients: the Warm
phase's sample count at capture, the wall seconds from the capture request
to `SizeSettled`, and the frame's structural Blank. The instrument builder
prints those three per capture if they are cheap beside the 329 work, so
the next blank arrives with its timing. NO RETRY in this batch: a retry that
succeeds before the cause is named is a guard that cannot tell a regression
from an improvement, and 325's acceptance asks for the cause with the
measurement that names it.

## 8. Question 4: the dispatch, in build order, and what each is expected to print

ONE dispatch, batched, because the round trip costs the same carrying one
change or six and the runner's history (queue 291's sixty-one hours) makes
each dispatch a bet on the runner being up. Build order is file ownership,
not priority: the probe pass files are held by one builder at a time.

  1. Queue 329 (instrument-builder): `FrameStats.h`, `frame-stats-test.cpp`,
     `VignetteShot.cpp` probe pass. Proves: a structurally blank probe frame
     prints `BLANK-PROBE-FRAME` with its own shot keys and enters no floor; a
     blank control makes the shot `NO-CONTROL` with the words on its floor
     line; the done line prints blank probes over frames decoded. Planted
     both ways as the item says.
  2. Queue 332 (same builder, same files): section 2's four rules, the
     fixtures from run 48, the buckets on the done line.
  3. Queue 335 (same builder, one line at the probe pass and two keys on the
     floor line): the exposure hold, asked beside read.
  4. Queue 325's three timing keys (same builder, if cheap; otherwise the
     item says they were not).
  5. Queue 333 (engine-specialist, AFTER 1 to 4 hand back, because it shares
     `VignetteShot.cpp` and `FrameStats.h`): section 3's three conditions,
     `make_base_material.py` with its selftest, the projected-box instrument
     in the tested header with its three fixtures.
  6. Queue 334 (a Core builder, in parallel with 1 to 5: `StreetVignette*.cs`,
     `CoreTests/Program.cs`, the golden, `VignetteSpec.h` and its g++ test for
     the new shot field): section 4's shape. The one-line `ShouldProbeShot`
     read is dictated to the engine-specialist, who holds `VignetteShot.cpp`
     last.
  7. Queue 028 half one (content-wrangler, in parallel): the bake.

Then one director spawn for the batch diff, verify green, footer from the
file, commit, push, dispatch, watch by ancestry with the sha captured first.

THE FALLBACK, so nobody holds an honest instrument behind an unfinished
lamp: if 333 has not handed back when 1 to 4 and 6 are reviewed, the
dispatch goes without it and 333 rides the next. If the budget bites, the
order of sacrifice is 028 half one (a day's wait costs nothing), then 334;
never 329 and 332, because a false number in the only channel is the worst
state the project knows, and 333 is what the slice is for.

PREDICTIONS, WRITTEN BEFORE THE RUN EXISTS, so the run can refute them:

  P1. 329: `lightProbesBlank=k/48` with k unknown, since the blank is a
      race; every blank light line reads `BLANK-PROBE-FRAME`; the two
      histograms that repeated three times each on run 48 do not appear as
      YES verdicts anywhere.
  P2. 332 on run 48's own numbers, in the g++ fixtures before the dispatch:
      measured 3/42, above floor 3/3, lanterns measured 0/24, the four
      nothing-measured buckets 14, 8, 7 and 10. The boundary case is
      `pinset_night_3` lantern0 (-0.00562 under a +0.02572 gap), which the
      rules in section 2 put in VOID-CONTROL; whichever bucket a builder's
      exact form lands it in, 3 measured and 0 lanterns are the predictions
      that matter.
  P3. 335: if the hold takes, every non-blank control's signed gap reads at
      the noise-shaped floor (of the order of 0.00005, with a decaying
      MOVED histogram and a sign balance near a third) and the
      EXPOSURE-SWUNG bucket reads 0 over the lights probed; if it does not,
      the read speeds say why and the gaps stay in kind. The prediction
      written to be refuted: with the hold in place, at least one lantern
      at `cam_hook` under `wet_night` MEASURES, in either direction.
  P4. 333: at night rows, every lantern rectangle that is in frame prints
      `brightestWarm=yes` with its peak R minus B above its ring's; at day
      rows of the same cameras it prints no; `band.skyCentre.p50` on
      `vign_hook_day` reads 0.8035 and `shotExposurePinRead` 0.3000/0.3000,
      unmoved, because a default-black parameter moves nothing it does not
      touch.
  P5. 334: six `shotMeanLuma` values in order at one camera under one
      condition; the finding is whether consecutive steps fall to the
      run's null-pair level or do not, printed with the statistic named.
      No level is predicted, on purpose.
  P6. 325: if a frame blanks, its three timing keys print beside
      `shotBlank=yes`, and the diagnosis has its first measurement.

## 9. What this director refuses

A headline of "3 of 28" (section 1.3). "Zero lanterns" without its
denominator (section 1.3). An absolute bound on the control gap set from
six samples (section 2). A new surface kind whose only job is to say what
`emissive=true` already says (section 3). A settling series in the untested
layer (section 4). A retry on blank before the blank has a timing (section
7). A night pin derived from anything (section 5, and the 2026-09-10 ruling
by name). A second queue item for the figure beside the one Jafar reopened
(section 6). A dusk frame taken from `cam_A` with the control card in it:
the 2026-09-15 22:55Z block already rules it and it stands.

## 10. Queue items: filed and amended, dictated text

NEW: `production/queue/335-the-light-probe-differences-two-frames-at-two-exposures.md`

    line: instrument (VignetteShot.cpp the probe pass at BeginNextProbe and the
      per-shot exposure write at 2102; FrameStats.h the floor line)
    spec: The probe toggles a light and re-enters the Warm phase with the
      exposure rate snapped to 10000, so every OFF frame is photographed
      after the loop has re-adapted to a scene with one light fewer. Under
      AUTO every difference is the light plus the loop's answer, and run 48
      shows it: seven lights whose OFF frame came back brighter across
      831241 to 921600 of 921600 pixels, and no lantern measured in either
      direction, 0 of 24. The value cannot be pinned (VignetteShot.cpp 356
      to 358, the 2026-09-10 ruling, queue 276); a DIFFERENTIAL measurement
      needs only the two frames at one value, whatever it is.
    acceptance: AutoExposureSpeedUp and SpeedDown written to 0 at the start of
      the probe pass, after the reference frame is on disk and before the
      control's re-render, restored by the per-shot write on the next shot;
      the floor line carries lightProbeHoldAsked and lightProbeHoldRead for
      both speeds; the verdict is the six controls' signed gaps, read
      against run 48's two agreeing controls (about 0.00005, decaying MOVED
      histogram) and its two shifted ones (+0.16498, +0.02572). Both
      outcomes are readable: the gaps collapse on every non-blank shot, or
      the read speeds show a clamp or the gaps stay. No night pin, no
      exposure_pin change, no determinism gate; void as an absolute
      reference. If the engine does not hold at zero, the next rung is
      reading the adapted value back from the view state and pinning both
      clamps to it for the pass, which is a readback and not a derivation.
    max_sessions: 1
    status: READY 2026-09-16, filed by the 06:35Z ruling section 5. Rides the
      same dispatch as 329 and 332, in the same builder's hands. Under D45 a
      tool that measures the game: a test, no review.

AMENDED: queue 332, append to status:

    RULED 2026-09-16 (06:35Z ruling, section 2): both statistics, each for
    its own question. The signed gap (lightFloorCtrlMeanFull) is the
    exposure-state screen; the MOVED histogram stays the per-edge floor.
    The screen is RELATIVE, from this item's own sentence, and no absolute
    bound is set: a light whose mean fell below minus the control's absolute
    gap reads EXPOSURE-SWUNG; a light whose rise over the gap does not
    exceed the gap reads VOID-CONTROL; the rest are MEASURED and take the
    326 edge test; a shot that certified nothing reads NOT-USABLE. Every
    bucket prints beside lightsProbed. Run 48's 48 lines are the fixtures:
    measured 3/42, lanterns 0/24, buckets 14/8/7/10. The 0.001 proposed
    above is withdrawn; the column keeps printing.

AMENDED: queue 333, append to status:

    RULED 2026-09-16 (06:35Z ruling, section 3): the NARROWER change, in the
    engine and the material where the flag is already half-read. Core's own
    field comment calls the emissive pieces "the lantern bowls" (StreetVignette.cs
    89), so the spec already says they emit; no new surface kind, no golden,
    no CoreTests change. EmissiveColor vector parameter, default black,
    asserted in --selftest; a per-piece material instance on the decal-card
    precedent (VignetteShot.cpp 4089); driven by ApplyCondition's LanternsOn
    through a write-on-change guard; read back on the shot line; the
    strength an engine constant named as the first value of a series and
    printed on the scene line; the acceptance instrument is the projected
    lantern rectangle against its ring, in the tested header, three fixtures.
    Structural by the wetness precedent (a parameter, a node, a readback
    key): full review at landing. Next rung: housing and bowl as two pieces,
    for the day look, named on the ladder. Builds AFTER 329, 332 and 335
    because it shares their files.

AMENDED: queue 334, append to status:

    RULED 2026-09-16 (06:35Z ruling, section 4): spec rows in Core, not a rig
    loop. Six consecutive settle_night rows at the END of the shot list, at
    cam_hook under wet_night (or pin_setter_night if the builder shows the
    two conditions identical in every field), excluded from the light probe
    by a per-shot boolean ShouldProbeShot reads beside the condition's flag;
    Shots.Count 43 to 49 with the assertions' sentences and arithmetic
    updated in the same diff; the series reduced in the tested layer to a
    done-line key naming first, last, largest consecutive step and the
    statistic (last-wins). Six is a cost cap and announces when it bites:
    NOT-SETTLED-WITHIN-6 is the finding 276 step 2 names, not a failure.
    Structural (a golden): full review at landing, same batch.

AMENDED: queue 028, append to status:

    RE-SCOPED 2026-09-16 (06:35Z ruling, section 6) for the UE probe, which
    has no skeletal path (0 hits for SkeletalMesh, FBX, AnimSequence, Bone
    under ue-probe/Source) and an importer that reads GLB by magic bytes.
    Item 1 in two halves. Half one, a tool, STARTS NOW: a Blender step in CI
    takes one held body and one clip at one named frame from the 91 files
    under ledger/Assets/Characters, applies the pose, exports a static GLB
    to the props path; body, clip and frame named in the item, sizes from
    the manifest, never invented. Half two, Core: the figures block emitted
    as a prop piece with a dark tint surface, golden regenerated; waits only
    for 333 and 334's Core changes to land, one builder in Core at a time.
    The decal route stays refused: a decal card is opaque and rectangular
    by SurfaceBind.h's own words. No token is needed. The allowlist line 6
    is corrected under D43 to name Mixamo characters as CLAUDE.md section 0
    already does, citing Adobe's terms in the correcting commit.

UNCHANGED: queue 329 stands as written and goes first. Queue 276 stands;
334 is its step 1 in the form ruled above. Queue 319's lantern readback
lands with 333's emissive readback on the same shot line, and 319's status
says so when 333 lands.

## 11. The quality ladder at close

Rows for `production/quality-ladder.md`, the D1b table:

    | Light probe floor | per-shot control, integer edge test, strict; run 48 read honestly as 3 measured of 42 and 0 lanterns of 24 | two controls per shot, and a light must beat the floor by more than the two controls differ from each other, so a six-pixel win at a sixteen-pixel floor has a margin statistic under it and no epsilon is invented |
    | Light probe exposure | AUTO on both halves of every difference; the loop's answer is in every reading | the hold at speed zero (335); if the engine will not hold, the adapted value read back from the view state and pinned for the pass |
    | Sodium lantern | a point light under a dark metal box | the box emits when its condition lights it (333); then housing and bowl as two pieces with a bowl surface for the day look; then the reflection of the bowl in the wet road measured on its own rectangle, which the spec's own note names as the thing the engines will differ on |
    | Night exposure reference | none; night rows carry exposure_pin 0.000 | 276 step 1 as six settle rows (334); step 2 names the count and the level as last-wins or NOT-SETTLED; only then step 3, the night rung set, and no arithmetic from any day pin |
    | Figure | none placed | a posed static bake of a held body through the GLB path, in silhouette (028 half one); then the figures block in the spec (half two); then the skeletal path for an idle, which is the row D29 owes |
    | Dusk reference | none; the Hook sheet is a day frame | a research row: a measured dusk sheet on the allowlist, or Jafar's eye under D41's second path, named before the dusk frame is sent |

## 12. Corrections to the brief

  1. "3 of 28" is the wrong denominator and the wrong sentence; section 1.3.
  2. "ZERO lanterns survive anywhere" is a zero without its denominator;
     the denominator of measured lanterns is 0 of 24 and the word is
     "nothing measured".
  3. The caller's control gap for `pinset_night_4` (0.00004, from
     0.16938 minus 0.16934) and the line's `lightFloorCtrlMeanFull=+0.00003`
     are one number rounded twice, not two readings; the line's value is
     the one to quote. Same for camA (0.00004 against -0.00005).
  4. The eleven NO verdicts were not classified and ten of them are not
     readings; section 1.2.
  5. The 0.001 bound is withdrawn, not because it misclassifies this run
     but because six samples with two blanks is not a series; section 2.
  6. The figure item exists (queue 028, reopened by Jafar 2026-09-14); the
     brief spoke of the figure "entering the queue" as if new.
  7. The allowlist names "Mixamo animations" only; CLAUDE.md section 0
     names Mixamo for characters too; D29 already flagged the gap.
     Corrected under D43, reported in the brief.
  8. Everything the caller measured off the frames (the 26 pixels, the
     window practical's rectangle) is the caller's number here and was not
     re-measured; nothing in this ruling rests on it.

## 13. For the commit message, the log and the brief

Commit message, first line: "Run 48 read honestly: three lights measured,
no lantern, and the lamp glows where its flag is already read". The rulings
log line:

    - **2026-09-16** run 48 measured three lights and no lantern (06:35Z):
      lightsAboveFloor is 3/3 over 3 measured of 42, lanterns 0 of 24 and
      the word is nothing-measured; 332 takes both control statistics with a
      relative screen from its own sentence and no absolute bound, run 48's
      lines as fixtures; 333 is the narrower change in the engine (the spec
      already calls the piece a bowl), structural by the wetness precedent;
      334 is six settle rows in Core; 335 filed, the probe pass holds its
      exposure at speed zero and the six controls decide; 028 re-scoped as a
      posed static bake now and a spec piece behind the Core changes; the
      allowlist line corrected under D43; predictions written before the run
      `game-design/decision-2026-09-16-ruling-run-48-measured-three-lights-and-no-lantern-and-the-lamp-glows-where-the-flag-is-read.md`

For tomorrow's brief, the Producer's channel and not this record's: the
two things Jafar asked for by name (the frames survived staging, 43 of 43;
the spawns by tier), then one sentence each for the corrected reading, the
lamp finding with its cause in the source, and the allowlist correction;
no question, no picture until a run has measured one.

<!--RULING spawn=2026-09-16T06:35:34Z-->
