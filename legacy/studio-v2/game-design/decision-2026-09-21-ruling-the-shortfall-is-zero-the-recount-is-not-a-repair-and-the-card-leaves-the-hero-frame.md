# Ruling, 2026-09-21 (14:30Z spawn): the shortfall is zero, the recount is not a repair, and the card leaves the hero frame

STATUS: LOG, 2026-09-21. NOT CURRENT once the batch it rules on has been
committed with the dictated edits in sections 7, 10 and 11 applied and the
first landed run whose commit CONTAINS it has been read against sections 8
and 10; from then the verdict file, the g++ suite, the queue items and NOW.md
are the reading copies and this is the record of what was ruled and why.

Director ruling on the engine-specialist's queue 223 batch standing
uncommitted in the tree: `ue-probe/Source/LedgerProbe/Public/SurfaceBind.h`
(+190) and `ue-probe/tests/vignette-spec-test.cpp` (+77), 267 lines, all in
the g++-compiled layer; and on the three questions the resident put with it.
Section 10 is the same session's addendum after the resident applied section
7's items 1 to 17 and reported two findings. Section 11 is the same session's
second addendum after commit 7a7be367 moved the reference past the first
stamp and edits 21 to 28 plus two D43 corrections were applied.

Author: tier-1 director, one session, three spawn rows in
`.claude/agent-log.tsv` all carrying agent id `ab8a9217eda535ae0`: line 733
(`2026-09-21T14:30:16Z`), line 735 (`2026-09-21T15:04:02Z`) and line 737
(`2026-09-21T15:34:14Z`); line 738 is empty. The stamp at the foot names row
737, the newest, quoted from the log; row 733 was the stamp that closed
sections 1 to 10 and cleared commit 7a7be367 (section 11.0). This director
has no shell and wrote no code: every file below was READ at the line numbers
in section 0, every number is copied from a printed line, and the counts
marked "resident's run" were not re-run here.

VERDICT IN ONE LINE: the batch LANDS AMENDED, the keys keep their names and
the line gains one dated key that says the flip from PARTIAL to ALL over the
same pack is a recount; the control quads LEAVE cam_A for cam_B by a rule
spelled once in the tested layer, not by a literal in the .cpp; the record's
correction is sufficient at the two sites that carried the false sentence and
is itself wrong in one clause, which is corrected below; the figure's material
is filed as the next item on the engine line because it is the visual slice.

## 0. What was opened

`.claude/agent-log.tsv` 726 to 734. `ue-probe/Source/LedgerProbe/Public/
SurfaceBind.h` 1 to 1018 (the header's own account of the sixteen names at 4
to 9 and 209 to 243), 2380 to 2470 (`SurfacePopulationSegment` at 2408, its
900-char cap at 2415 and 2446 to 2449), 2469 to 2583 (`MaterialsDoneLine`, the
tally at 2480 to 2533, the status word at 2548 to 2551), 2585 to 2605 (why the
control quads exist), 2740 by grep (`ControlQuadPlace`), and grep for
`first shot|Shots[0]` (968, 1009 only: the wetness seed, nothing in the quad
section). `ue-probe/tests/vignette-spec-test.cpp` 2326 to 2440 (the 227
fixture: PARTIAL with `brick_blue` planted at 2347, the clean ALL case at 2383
to 2418, NO-BASE-MATERIAL at 2421, NOTHING-ASKED at 2429), 4384 to 4413 (the
cam_hook block that looks the quad camera up as the first shot's camera at
4404), and grep for `ControlQuad|cam_A|cam_B`. `ue-probe/Source/LedgerProbe/
Private/VignetteShot.cpp` 6160 to 6199 (`ControlCamera` at 6180) and grep for
`ControlCamera()` (1125, 3727, 6195, 6418) and `"cam_A"` (6644,
`FindCamera("cam_A")`, an unrelated start camera). `tools/map.py` 1065 to
1104 (the `textured` entry, `materialsStatus` at 1083) and grep over
`tools/**`, `ledger/verify.py`, `.github/**` and the .cpp files for
`materialsStatus|surfacesAbsent|surfacesAsked|mapsFound`: map.py:1083 and
VignetteShot.cpp 1073, 3269, 5751 only; NO GATE READS THESE KEYS.
`production/d1-probe/ue-vignette-verdict.txt` 208 (the vign_camA_night shot
line), 258 to 271 (the sixteen surface lines: twelve RESOLVED, `interior` and
`paint_yellow` PROCEDURAL, `card` and `multiply` DECAL-BLEND), 272 (the done
line), 273 to 298 (decals, the three quad lines, the quad done lines).
`production/d1-probe/ue-build.txt` 14. `production/specs/vignette-scene.json`
838 to 879 (the three cameras) and grep of shot ids and cameras (49 shots: 2
on cam_A, 2 on cam_B, 45 on cam_hook). `production/NOW.md` 60 to 130 and 3000
to 3101. `production/queue/223`, `227`, `313`, `339` whole; `062` 108 to 121;
`384` 1 to 24 and 284 to 343. `production/wakes/2026-09-21T1438Z-80f2a36b.
wake.txt` whole. `production/outbox/` by glob (newest file 2026-09-17) and by
grep for `card|paint_yellow|legs` (hits only in 2026-09-08 and 2026-09-09
files, none about this). `ledger-v2/respec/decision-register/D41`, `D45`
whole; `D43` 1 to 9 by grep. `game-design/decision-2026-09-16-ruling-326-
lands-amended-...md` 1, 32 to 37, 111 to 149, 375 to 381 (the rename
precedent). `game-design/decision-2026-09-16-ruling-run-48-...md` 625 to 626
and `decision-2026-09-15-ruling-per-condition-wetness-lands-...md` 246 to 266
(the dusk frame with the card in it). `.claude/agents/instrument-builder.md`
frontmatter (model opus, maxTurns 70). `ledger-v2/studio-v2/organization.md`
66 to 117 and 196 to 206 for the stamp's shape. For section 10: test 4252 to
4273 and 4440 to 4525; SurfaceBind.h 2640 to 2655; VignetteShot.cpp 1092 to
1100, 3208 to 3219, 3727 to 3730, 6413 to 6428; grep over ue-probe for
`controlQuadIntrusion` (test 4520 only) and for `Shots[0].CameraId|first
shot's camera|FIRST shot's camera|FIRST SHOT'S camera` (the list in 10.1);
this file's own lines 330 to 570 read back before it was rewritten. For
section 11: `.claude/agent-log.tsv` 730 to 738; as applied, test 4256 to
4273 and 4521 to 4531, VignetteShot.cpp 1072 to 1080 and 6177 to 6194,
SurfaceBind.h 2714 to 2739 (site 7 as corrected), 2768 to 2796
(`ControlCameraId`, `ControlQuadPlace` and its axis-centring comment).

## 1. What kind of change this is, and how much review it needed

Under D41 the test is what undoing a wrong answer costs. Reverting this batch
is a revert of one header and one test and another render: no migration, no
golden file, no canon edit, no schema change (every status word it prints,
ALL, PARTIAL, NONE, NO-BASE-MATERIAL, NOTHING-ASKED, existed before it; the
keys it adds are additive, and no gate reads any key on the line). Under D45
`MaterialsDoneLine` and `SurfacePopulationSegment` are the measuring half of a
file that also paints; the batch touches only the tally, and the builder's own
falsifier (every frame luma-identical to run 55) is the test that it left the
painting half alone. So: A MEASUREMENT CHANGE UNDER D45, owed a test and no
review of its code.

What sends it to a director anyway is CLAUDE.md's own list: A LANDING THAT
CHANGES A CONCLUSION. The conclusion was that four surfaces have no maps
(queue 223's title, the resident's message in NOW.md:73 to 79, queue 384:11
to 13 and 289 to 294); the batch says the shortfall is zero. That is a record
question and a naming question, and this ruling is about those. The code
review it got was confined to rule 5b: the accepting case is first (test 2383
to 2418, ALL with two blend modes still in the vector), the rejecting case is
planted (`brick_blue`, a name that exists nowhere, 2347 and 2360, keeps the
line at PARTIAL), the cap announces itself (2446 to 2449) and the test asserts
it did not bite on the longest fixture (2416). Nothing else in the 267 lines
was read for correctness, and this ruling does not claim it was.

The quad move (section 3) is VISUAL under D41: a wrong answer is undone by
another render. It needed no ruling. It is ruled because it was asked, and
because the number the builder printed needed its unit and its denominator.

## 2. Ruling 1: the conclusion change lands, the names stay, and the line says it is a recount

THE FINDING IS RIGHT, READ OFF RUN 55'S OWN LINES. The sixteen per-surface
lines at 258 to 271 (and the two before them, asphalt and brick_grey, by the
count on the done line) classify every name: twelve `surfaceStatus=RESOLVED`,
`interior` and `paint_yellow` `PROCEDURAL` with `surfaceRoute=tint` and a
built tint texel (31.22.14 and 147.127.35), `card` and `multiply`
`DECAL-BLEND` with `albedoFile=NOT-A-LIBRARY-SURFACE`. The done line at 272
says `materialsStatus=PARTIAL surfacesAsked=16 surfacesResolved=12/16
surfacesAbsent=card/interior/multiply/paint_yellow mapsFound=36/48` over
those same sixteen. The done line was wrong about the population and the
lines under it were right, which is what the resident said and what the
header now says of itself at 4 to 9. `paintRoutes=pack.580/tint.10/
decal-card.10/decal-multiply.0 piecesPainted=600/610 piecesUnpainted=10/610`
on the same line say the ten unpainted are the multiply decals, hidden
fail-closed (`decalQuadsHidden=10/20`, `decalsMultiplyRule=a-stain-needs-a-
modulate-material-and-this-build-has-one-opaque-base`). Fourteen library
surfaces asked, twelve from the pack, two by design, none missing.

IS "ALL" THE RIGHT WORD? Yes, with its meaning on the line and one more key
beside it. ALL answers the question the status always claimed to answer, "is
every surface the street asked the pack for accounted for", and the answer is
yes; the vocabulary ALL, PARTIAL, NONE is the line family's (run 55 prints
`controlQuadsStatus=ALL` and `decalsStatus=PARTIAL` on the same page), and
`materialsStatusMeans=ALL-is-every-library-surface-accounted-for/resolved-
from-the-pack-or-procedural-by-design/...` (header 2433 to 2435) sits on the
same line. A reader of `tools/map.py`'s textured entry sees `materialsStatus`
beside `piecesTextured=600/610`, on a page whose own blocker line says
"textured in the frame, and no key measures it" (map.py:1078); the word does
not claim textured, and the page already refuses to. What the word CANNOT be
allowed to do is read as an improvement between run 55 and run 56, and that
is the next paragraph.

THE NAMES STAY, AND THIS IS A DISTINCTION FROM THE 2026-09-16 PRECEDENT, NOT
A DEPARTURE FROM IT. That ruling renamed `lightsReachedFrame` because "a key
whose numerator rule AND denominator both changed is a new instrument, and a
new instrument gets a new name", and it said a stat token 250 characters
along the line "is not what a key-grep returns". Here the numerator rules did
not change: resolved still means an albedo file found, decoded and bound;
absent still means no pack file and no spec entry. What changed is that the
population was WRONG under the key's own stated meaning (`card.png` is a file
that by design can never exist, header 227 to 230; `paint_yellow.jpg` would
make two engines render one surface from two inputs, 231 to 237). A corrected
population under an unchanged meaning is the same instrument with a bug
fixed, and renaming it would leave a run-56 reader with no `surfacesResolved`
at all and a Python reader (map.py:1083) and a never-ran branch
(VignetteShot.cpp:1073, `materialsStatus=NOT-REACHED`) to edit for it. The
precedent's device is what is taken instead: a dated history key, the shape
of its `.../RENAMED-BY-QUEUE-326-from-...-through-run-47-and-is-not-
comparable`, placed on this line under its own name so that a key-grep for
it returns the whole story. Dictated in section 7 as
`surfacePopulationChanged=queue-227/...is-a-recount-and-not-a-repair`, with
the segment's cap raised from 900 to 1200 so the key cannot be the thing
that trips `surfacePopulationCut` (the ALL-case segment is already near 800
characters by count of the literals at 2426 to 2437), and one test check that
the key is on the clean line. THE RESIDUAL, NAMED: a bare grep for
`surfacesResolved` over runs 55 and 56 returns `12/16` then `12/14` with no
warning on that key. Accepted, because nothing gates on it (section 0), the
history key is on the same line, and this ruling and NOW.md carry it.

ONE WORDING ON THE LINE IS FALSE AND IS CORRECTED. `mapsAskedOf=.../a-
procedural-surface-asks-the-pack-for-nothing-so-it-is-not-in-that-
denominator` (2431 to 2432) is refuted by run 55's own `paint_yellow` line
(266): `normalFile=ABSENT normalTried=paint_yellow_n.png/paint_yellow_n.jpg/
paint_yellow_n.jpeg roughnessFile=ABSENT roughnessTried=...`. A procedural
surface asks the pack for no ALBEDO; its normal and roughness are tried, or
borrowed (`interior`, 262, `normalBorrowedFrom=window`), and print on its own
line. The comment at 2508 ("It asks for no map") is the same sentence in
prose. Both dictated.

THE MAP PAGE. Dictated: `surfacesAccountedFor` and `surfacesProceduralNames`
join the textured entry's readings at map.py:1082 to 1084, so the page prints
`ALL` beside `14/14` and `interior/paint_yellow`. A tool that reads the game:
the resident applies it and opens the page (rule 4). Until run 56 lands the
two readings are absent from the committed verdict, and whatever the page
prints for an absent key is the honest state for one run.

WHAT THIS MOVEMENT IS NOT. `surfacesAsked` 16 to 14, `surfacesAbsent` four
names to `none`, `mapsFound` 36/48 to 36/36, `materialsStatus` PARTIAL to
ALL: none is a repair. Nothing about the pack, the resolver or the painting
changed. The one instrument that can prove that is the frames (section 8).

## 3. Ruling 2: the control quads leave cam_A, by a rule spelled once

THE NUMBER, WITH ITS UNIT AND ITS DENOMINATOR. The builder's 28.6213 to
28.5426 is mean luma on 0 to 255 read off the PNG; the verdict prints luma on
0 to 1 (`shotMeanLuma=0.1125` on line 208 for this frame, `meanOnFull=`,
`rigRepeatsWorstMeanLumaDelta=0.00061`, `kSettleMeanLumaBound=0.005`). So the
builder's 0.0787 is 0.000309 on the verdict's scale, as the resident said.
BUT IT IS THE COLOUR QUAD ALONE: 15,624 px is one box, and there are three.
Line 208 prints `shotControlQuadsBoxed=3/of=3 shotControlQuadsBoxPx=x130..614/
y298..422 shotControlQuadsAtMostPctOfFrame=6.51`, so the area that changes
when the quads leave is up to 6.51 per cent of the frame, not 1.70, and the
two tile quads read as PALE UNIFORM FALLBACKS in the day frame (queue 339:
channel means near 218/222/216). The direct shift on vign_camA_night is
therefore NOT bounded by 0.000309; it is unknown and could exceed 0.005. The
builder's number was honest about what it measured and the resident's unit
resolution was right; the denominator was one quad of three.

WHY THAT DOES NOT CHANGE THE ANSWER: NO INSTRUMENT COMPARES THIS FRAME ACROSS
RUNS. `kSettleMeanLumaBound` is a stopping rule between successive takes of
one shot in one run (line 208: `shotSettleSeries=0.11192..0.11249
shotSettleDelta=+0.00057`); `rigRepeatsWorstMeanLumaDelta` is between repeats
of one shot in one run. The exposure baseline run 55 bought is those two,
and neither reads run 55's file against run 56's. The one cross-run
comparison that exists is this ruling's own falsifier for the count change,
and it is taken on the 45 cam_hook frames, which the quads were already
hidden on (`controlQuadHidden=47/49`, line 298).

AND THE MOVE CLEANS AN INSTRUMENT THAT IS CONTAMINATED TODAY. On line 208
the figure's silhouette box is `x561..719/y313..489` and its ring is
`x385..895/y137..665`; the colour quad's box (line 294) is `x488..614/
y298..422`. The quad overlaps the figure's own box on x561..614, y313..422,
and all three quads sit inside the ring. `figureSil1=.../coreMeanLuma=23.8/
ringMeanLuma=38.2/...` is read with a four-colour card inside the core and
two pale fallbacks in the ring. Moving the quads is not only Jafar's frame;
it is the figure's own reading.

WHY cam_B AND NOT ANYWHERE ELSE. The committed spec has three cameras (838 to
879). cam_A is the figure's camera (`figurePlacement=.../camDistM=6.00/...`
on ue-build.txt:14 is computed from cam_A; the night frame is the one D28
names and the 06:35Z ruling of 2026-09-16 calls "the frame the whole visual
slice is judged by"). cam_hook is the sheet's camera, 45 of 49 shots, the
grid, the fog, the pins and the wetness ladder; a quad there would sit in
every band statistic the sheet comparison reads. cam_B stands at x 21, z -4,
yaw 90, looking across the street at the east parade; the figure at x 10 is
about 54 degrees off its axis against a 45.75 degree half-field
(`fovH=91.5`), so it is outside that frame, and no reading anybody judges is
taken on cam_B. Three quads 3.5 m ahead of cam_B stand in the carriageway at
z about -0.5, hidden on every other shot by the rule that already exists.
"An instrument nobody judges by eye": the quads are not read by eye at all in
any code path, which is queue 339's finding ("prints where to look, prints
what the answer would mean, and never looks", for at least four runs). Their
liveness is 339's pixel readback, whose acceptance is camera-agnostic (the
four quadrant means per quad off the frame `quadOn` names); until it lands,
a human opens the cam_B still to read them, which is exactly what a human had
to do on cam_A. Nothing is lost.

THE PLACEMENT WAS NEVER A JUDGEMENT. VignetteShot.cpp 6176 to 6179 says the
quads stand in front of "the camera the first shot uses, read out of the file
rather than named here". cam_A is the first shot's camera by accident of
shot order. Two rulings already refused the consequence: the 2026-09-15 22:25Z
ruling's 313 section and the 2026-09-16 06:35Z ruling at 625 to 626 ("A dusk
frame taken from cam_A with the control card in it ... stands" as refused).
This ruling is the remedy those two left open.

THE MECHANISM: NOT THE ONE-LINE LITERAL. The resident proposed one line at
VignetteShot.cpp:6185. Refused as the shape, accepted as the size. The g++
suite's cam_hook block looks the quad camera up by the same "first shot's
camera" rule (test 4404) and says of itself "it is the FIRST SHOT'S camera by
definition and this block must keep saying so even if the shot order changes"
(4397 to 4399). A literal in the .cpp would leave the suite measuring where
cam_A-placed quads land in cam_hook's frame while the engine places them from
cam_B: an instrument reading the wrong world, which is the fault class
`.claude/rules/instruments.md` opens with. So the rule is ONE function in the
tested layer, `LedgerSurface::ControlCameraId()`, and both the engine and the
suite read it; the id is spelled once. The suite gains two checks: the camera
exists in the committed spec (accepting), and it is neither the first shot's
camera nor cam_hook (the two this ruling excludes). All dictated in section 7
as verbatim text; the resident applies them by hand as dictation. If any of
them fails to compile in the suite or a check goes red, the resident stops
and sends the whole of section 7 to an instrument-builder (declared model
opus, maxTurns 70; mechanical work, so the routing law applies and a cheaper
model is the right spawn if the definition allows it) rather than improvising.

QUEUE 313 CLOSES ON THE NEXT LANDED RUN IF: the vign_camA_night line reads
`shotWholeFrameIncludesControlQuads=no/hidden-for-this-camera`,
`controlQuadHiddenOn` begins `vign_camA_day;vign_camA_night`, the quad lines
read `quadOn=cam_B/1280x720`, and the still, OPENED, carries no card and no
swatch. Its own acceptance said "the fix is placement and the accepting case
is the same shot without them, with a check that says which pieces were
removed and why": those keys are that check. Queue 339 is unchanged and stays
READY on the measurements lane.

## 4. Ruling 3: the batch lands, amended, with its falsifiers written

LANDS. The guards are the ones rule 5b asks for and in the order it asks
(section 1). The population comes from the engine-side bind loop, so the
predicted split 14/12/2/2/0 and every done-line number in section 8 is a
prediction until the run prints it; the resident's suite counts (3600 to 3607
instruments ok, 267 checks) are the resident's and were not re-run here.

AMENDED BY: the history key, the cap raise, the wording fix and its comment,
the one test check (section 2), the map.py readings (section 2), and the
control-camera rule with its four sites and two checks (section 3). None of
them moves a bound, tunes a constant or touches the painting half.

NOT REQUIRED, AND SAID SO: a rename pass (section 2, the distinction from the
09-16 precedent), and any change to the ten hidden multiply decals, which are
fail-closed by a recorded reason and are the remaining content of queue 223.

## 5. The record: what the correction fixed, what it got wrong, and what is not infected

THE TWO SITES THAT CARRIED THE FALSE SENTENCE ARE CORRECTED IN PLACE AND
SUFFICIENTLY. `production/NOW.md` 73 to 79 and `production/queue/384` 289 to
294 said "The card IS the unresolved card surface; the yellow IS
paint_yellow". Both now carry the D43 block (NOW.md 81 to 125, 384 296 to
340) with the false sentences left visible, the verdict keys that refute them
quoted, and how the error was made. That is D43's shape and rule 1's
("grep for the SENTENCE"): sufficient.

THE CORRECTION IS ITSELF WRONG IN ONE CLAUSE. NOW.md 107 to 108 and 384 322
to 323 say the run prints "figureImportStatus=IMPORTED and ZERO figure
material or texture keys, while Michelle.fbx carries four embedded textures
in a .fbm folder". Read: `production/d1-probe/ue-build.txt:14` prints
`figureImportStatus=IMPORTED ... figureMaterials=1 ... figureImportVia=
AssetImportTask/made=7`. One material key exists and no texture key exists.
And no `Michelle.fbm` directory is in the tree (glob: `ledger/Assets/
Characters/Michelle.fbx` only); "four embedded textures" is the builder's
reading of the binary and is printed nowhere. Dictated in section 7: the
clause becomes "the build page prints figureImportStatus=IMPORTED and
figureMaterials=1 (ue-build.txt:14) and no texture key at all, so whether
that one material's textures bound is unmeasured, and the embedded texture
count is unprinted". The legs remain unanswerable, which was the point, and
the item in section 6 prints the count rather than assuming four.

THE BUILDER'S OTHER SITES, READ ONE BY ONE:
- NOW.md:3012 and :3036 no longer point where the builder looked (the D43
  block moved the lines by about 46). The sentences are at 3058 to 3059 ("The
  real fault is surfacesAbsent=... with mapsFound=36/48") and 3082 to 3084
  ("The ruler is understood"). Both are the 2026-09-09 log, and the same
  section corrects itself at 3061 ("AND THE READING OF THAT WAS ALSO WRONG,
  corrected 22:05Z") and 3078 ("Queue 227 is the gate whose green state would
  require shipping wrong content"). A log that was true when written and
  corrected in the same section is history, not infection. Nothing to do.
- queue 062:115 to 116 quotes `mapsFound=36/48` and `surfacesResolved=12/16`
  as what the verdict printed, to prove the staging RAN. True as written.
  Nothing to do.
- queue 384:11 to 13 reasons "NOT THE MATERIALS" from the same four names in
  runs 53 and 54. The argument holds (identical inputs cannot be the cause of
  a change); the phrase "four absent surfaces" is the pre-227 population. One
  dictated parenthesis (section 7) pointing at the correction at the foot of
  the same item.
- `production/wakes/2026-09-21T1438Z-80f2a36b.wake.txt` line 9 carries "the
  four surfaces that spoil the figure frame". A wake file is the record of
  what was armed and is not edited.
- queue 123 and 339 describe the quads as standing on cam_A or in front of
  the first shot's camera; after section 3 that is stale. 339 gets one dated
  line (section 7). 123 was not opened by this ruling; the resident greps it
  for `first shot` and `cam_A` and corrects on sight under D43.

THE MESSAGE TO JAFAR. `production/outbox/` holds no file dated 2026-09-21;
its newest is 2026-09-17, and grep for `card|paint_yellow|legs` over it finds
only unrelated 2026-09-08 and 2026-09-09 lines. The false sentence did NOT go
to his phone through the channel that leaves a file. If the resident told him
through some other path, the resident names the path and the message and
sends the correction the same way; if not, there is nothing on his phone to
correct, and a stand-alone correction of a claim he never received is noise.
Either way the Producer's next brief carries one sentence (section 6b), no
more, and reporting to him stays the Producer's (2026-09-03).

## 6. What else, and in what order against his standing order

His order: the visual slice first, then the measurements, then the art lane,
cut from the bottom.

(a) THE FIGURE'S MATERIAL, FILED BY THE RESIDENT, TOP OF THE ENGINE LINE
BEHIND THIS BATCH. It IS the visual slice: the figure is next in his order,
and "the legs are flat yellow" cannot be acted on until something prints
whether the one material the import made (`figureMaterials=1`) has its
textures bound. Line: engine and instruments, jointly. Acceptance, both arms
watched: the import step prints `figureTexturesEmbedded=N` measured off the
FBX (not typed), `figureTexturesBound=n/N` per material slot with the words
for a never-ran case, and the night frame OPENED shows the legs as the
garment; a figure whose textures never bound prints `0/N` and the frame is
still opened. The binding itself is visual work under D41 when its turn
comes: no ruling, the frame is the judge. Cite queue 123, queue 379 and this
ruling.

(b) THE "30". Queue 223:42 to 44 and NOW.md:3072 say thirty pieces got no
material instance; that was true of the run they described. Queue 227:24
says "piecesUnpainted, which is 30 today and 0 when queue 223 lands"; run 55
measures `piecesUnpainted=10/610`, all ten the multiply decals, hidden
fail-closed. D43 corrections applied on landing, dictated in section 7; not
new items. Queue 223 closes at `piecesUnpainted=0`, which now depends on one
thing, a modulate or deferred decal material for the ten stains
(`decalsMultiplyNote=drawn-in-unity-and-hidden-here/the-pair-differs-by-the-
grime-until-that-material-exists`). The resident greps the queue for that
material BEFORE filing anything (rule 3: an item may already name it); if
none does, one item on the engine and art lines, behind (a), because the
grime is the art lane and his order puts it last.

(c) FOR THE PRODUCER'S BRIEF, ONE SENTENCE: the four-colour card in the night
frame was the studio's own instrument standing in front of the figure and it
moves off that camera in the next run; the texture pack is whole (twelve of
fourteen surfaces from files, two painted by design, none missing), and the
figure's own material is the next thing measured because nothing prints it
yet.

## 7. Dictated edits, verbatim, in this order, all hand-applied by the resident

The g++ suite runs after edit 6 and again after edit 10; `python3
ledger/verify.py` after all of them; the footer is pasted from the file. If
any edit fails to compile or any check goes red, STOP: the whole of this
section goes to one instrument-builder (declared maxTurns 70) with the
two-armed exit "suite green with the two new checks passing, or a named
failing check and the line it failed on".

1. `ue-probe/Source/LedgerProbe/Public/SurfaceBind.h`, line 2415:
   `char Buf[900];` becomes `char Buf[1200];`
2. Same file, line 2448: `" surfacePopulationCut=yes/at-900-chars"` becomes
   `" surfacePopulationCut=yes/at-1200-chars"`.
3. Same file, line 2432: the literal
   `"/a-procedural-surface-asks-the-pack-for-nothing-so-it-is-not-in-that-denominator"`
   becomes
   `"/a-procedural-surface-asks-the-pack-for-no-albedo-so-its-normal-and-roughness-are-outside-this-denominator-and-print-on-its-own-surface-line"`
4. Same file, insert one literal line immediately BEFORE line 2436 (the line
   beginning `" surfacePopulationRule=queue-227/`), inside the same format
   string, no format specifier and no argument:
   `" surfacePopulationChanged=queue-227/through-run-55-surfacesAsked-counted-16-names-with-2-blend-modes-in-it-and-called-the-2-procedural-surfaces-absent/from-run-56-it-counts-14-library-surfaces/PARTIAL-12-of-16-to-ALL-14-of-14-over-the-SAME-pack-is-a-recount-and-not-a-repair"`
5. Same file, line 2508, the comment `// NO PACK FILE BY DESIGN. It asks for
   no map, so folding three` becomes `// NO PACK FILE FOR THE ALBEDO BY
   DESIGN. Its normal and roughness are tried or borrowed and print on its
   own line; folding three`.
6. `ue-probe/tests/vignette-spec-test.cpp`, insert after line 2412 (the
   check ending `"its name while its test changed");`):
   ```
   		Check(CleanLine.find("surfacePopulationChanged=queue-227/") != std::string::npos
   		      && CleanLine.find("is-a-recount-and-not-a-repair") != std::string::npos,
   		      "and the line says on its own key that PARTIAL to ALL over the same "
   		      "pack is a recount, ruled 2026-09-21");
   ```
7. `ue-probe/Source/LedgerProbe/Public/SurfaceBind.h`, insert immediately
   ABOVE line 2740 (`inline QuadPlace ControlQuadPlace(const
   LedgerVignette::Camera& C, int I)`):
   ```
   	// WHICH CAMERA THE CONTROLS STAND IN FRONT OF, AND IT IS SPELLED ONCE.
   	// Ruled 2026-09-21: not the figure's camera (cam_A, the night frame he
   	// judges by) and not the sheet's camera (cam_hook, 45 of the 49 shots);
   	// cam_B is the one camera in the committed spec that is neither. Through
   	// run 55 the rule was "the first shot's camera", which stood a four-colour
   	// card across the figure's torso in ue-vign_camA_night.png (queue 313).
   	// VignetteShot.cpp and the g++ suite both read the id from here, and the
   	// engine prints which camera answered on every quad line as quadOn.
   	inline const char* ControlCameraId() { return "cam_B"; }
   ```
8. `ue-probe/tests/vignette-spec-test.cpp`, lines 4388 to 4393, the comment
   becomes:
   ```
   	// AND THE HALF NOBODY WOULD THINK TO ASK FOR: the three material control
   	// quads are placed 3.5 m in front of LedgerSurface::ControlCameraId(),
   	// cam_B since the 2026-09-21 ruling and not this camera, so nothing in
   	// their placement knows this camera exists. A frame with colour swatches
   	// standing in the road is not a frame anybody can judge a street by, so
   	// where they land in THIS camera's frame is measured here rather than
   	// discovered in the still.
   ```
   Lines 4396 to 4399, the comment becomes:
   ```
   		// AND THE CAMERA THE QUADS ARE PLACED FROM, looked up by the SAME rule
   		// the engine reads, LedgerSurface::ControlCameraId(), so this block
   		// cannot drift from the placement it claims to measure.
   ```
   Line 4404: `if (!S.Shots.empty() && S.Cameras[I].Id == S.Shots[0].CameraId)`
   becomes `if (S.Cameras[I].Id == LedgerSurface::ControlCameraId())`.
   Lines 4411 to 4412, the printed text `"camera of that id or no camera for
   its first shot\n"` becomes `"camera of that id or no camera named by
   ControlCameraId\n"`.
9. Same file, insert immediately AFTER the closing brace of the `for` loop
   that ends at line 4408 and BEFORE `if (Hook == 0 || QuadCam == 0)`:
   ```
   		Check(QuadCam != 0,
   		      "the committed spec carries the camera ControlCameraId names, "
   		      "which is the accepting case for the rule the engine reads");
   		Check(!S.Shots.empty()
   		      && std::string(LedgerSurface::ControlCameraId()) != S.Shots[0].CameraId
   		      && std::string(LedgerSurface::ControlCameraId()) != "cam_hook",
   		      "and the controls stand in front of neither the first shot's camera "
   		      "(the figure's frame) nor cam_hook (the sheet's), ruled 2026-09-21");
   ```
10. `ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp`, lines 6176 to
    6188 become:
    ```
    	// THE CONTROLS STAND IN FRONT OF LedgerSurface::ControlCameraId(), ruled
    	// 2026-09-21 and spelled once in SurfaceBind.h. A spec carrying no camera
    	// of that id falls back to its first camera, and which camera answered is
    	// printed on every quad line.
    	const Camera* ControlCamera()
    	{
    		if (GSpec.Cameras.empty()) { return nullptr; }
    		for (size_t I = 0; I < GSpec.Cameras.size(); ++I)
    		{
    			if (GSpec.Cameras[I].Id == LedgerSurface::ControlCameraId()) { return &GSpec.Cameras[I]; }
    		}
    		return &GSpec.Cameras[0];
    	}
    ```
    This file does not compile locally; the line is the same comparison
    shape as the one it replaces, and the run is its test (section 8).
11. `tools/map.py`, lines 1082 to 1084: the readings tuple
    `("shotsWrote", "piecesTextured", "materialsStatus", "shotDistinctBuckets@vign_camA_day")`
    becomes
    `("shotsWrote", "piecesTextured", "materialsStatus", "surfacesAccountedFor", "surfacesProceduralNames", "shotDistinctBuckets@vign_camA_day")`.
    Then the page is opened.
12. `production/NOW.md` 107 to 108 and `production/queue/384-*.md` 322 to
    323: the words `the run prints \`figureImportStatus=IMPORTED\` and ZERO
    figure material or texture keys, while \`Michelle.fbx\` carries four
    embedded textures` become `the build page prints
    \`figureImportStatus=IMPORTED figureMaterials=1\` (ue-build.txt:14) and no
    texture key at all, so whether that one material's textures bound is
    unmeasured, and the embedded texture count is unprinted (corrected
    2026-09-21 by the ruling of that date)`.
13. `production/queue/384-*.md` line 13, after `in run 53 AND run 54.`:
    ` (The "four absent" is the pre-227 population: two are decal blend
    modes and two are procedural by design; the correction at the foot of
    this item, 2026-09-21.)`
14. `production/queue/223-*.md`, appended to `status:`: `RUN 55, 2026-09-21:
    piecesPainted=600/610 piecesUnpainted=10/610, all ten the multiply decals
    hidden fail-closed for want of a modulate decal material. The thirty
    above was true of the run it described. Closes at 0, which now depends on
    that material alone; ruled 2026-09-21.`
15. `production/queue/227-*.md`, appended after line 27: `RULED 2026-09-21
    (game-design/decision-2026-09-21-ruling-the-shortfall-is-zero-...md):
    lands amended; the keys keep their names, the line carries
    surfacePopulationChanged, and run 55 measured piecesUnpainted=10/610, not
    30.`
16. `production/queue/313-*.md`, appended: `RULED 2026-09-21: the controls
    move to cam_B by LedgerSurface::ControlCameraId(); closes on the first
    landed run whose vign_camA_night line reads
    shotWholeFrameIncludesControlQuads=no and whose still, opened, carries no
    card and no swatch.`
17. `production/queue/339-*.md`, appended: `2026-09-21: from the next run the
    quads stand in front of cam_B; this item's acceptance is unchanged and
    reads its pixels from whichever frame quadOn names.`
18. Queue 123: grep for `first shot` and `cam_A`, correct on sight under D43,
    one line each, citing this ruling.
19. One new queue item filed by the resident per section 6(a), number written
    into this line when filed: ______.
20. If no queue item names the modulate decal material (section 6b, grep
    first), one more, number written here: ______.

## 8. What the first landed run must print, two arms

THE DONE LINE (line 272's successor): `materialsStatus=ALL surfacesAsked=14
surfacesResolved=12/14 surfacesAbsent=none mapsFound=36/36` ...
`surfacesAccountedFor=14/14 surfacesProcedural=2/14
surfacesProceduralNames=interior/paint_yellow surfacesAbsentCount=0/14
decalBlendsAsked=2 decalBlendNames=card/multiply mapsBorrowed=2`, the
`surfacePopulationChanged=queue-227/...` key present, no
`surfacePopulationCut`, and `piecesTextured=600/610 piecesPainted=600/610
piecesUnpainted=10/610 paintRoutes=pack.580/tint.10/decal-card.10/
decal-multiply.0` UNCHANGED from run 55. Any per-piece number moving is the
count change reaching the paint path, and the batch's claim fails.

THE FRAMES. The 45 cam_hook shots: day frames bit-identical to run 55's files
(the afternoon ruling recorded day frames bit-identical across runs 53 and
54), night frames within 0.005 of run 55's `shotMeanLuma` on the same shot
id. One outside that is either the count change reaching the render path or
an unrelated drift; the resident says which by opening it, and does not
explain it away. The cam_A pair: `shotWholeFrameIncludesControlQuads=no/
hidden-for-this-camera`; `vign_camA_night` `shotMeanLuma` moves from 0.1125
by an amount this ruling does NOT predict (section 3: up to 6.51 per cent of
the frame changes content), and the move is reported as a reading, not
judged against a bound. The cam_B pair: `shotWholeFrameIncludesControlQuads=
yes`, `quadOn=cam_B/1280x720` on all three quad lines, `controlQuadHidden=
47/49`, `controlQuadHiddenOn=vign_camA_day;vign_camA_night;...`. The still
`ue-vign_camA_night.png` OPENED: figure on the footway, no card, no swatch.

## 9. What this ruling did not do, and what is not mine

It did not re-run any suite (no shell). It did not read the diffs as diffs:
it read the files as they stand. It moved no bound, tuned no constant, wrote
no code, and edited no builder file. It did not rename a key, and says why.
It did not open queue 123. It did not decide the modulate decal material's
route (art and engine, his order puts it last), did not touch queue 339's
readback (already filed, measurements lane), did not do the figure's texture
binding (visual, D41, the builder's when its turn comes), and did not send
anything to Jafar (the Producer's).

## 10. Addendum, same spawn, after items 1 to 17 were applied: the fifth site and three more, the margin that was traded, and the cap series

Reported by the resident: 17 of 20 items landed, both ordered g++ runs green
(626 then 628 checks, 0 failed), verify green at 88/88, ue-probe instruments
ok 3607 to 3610. Two findings came with it. Sections 1 to 9 above stand as
written; where this section corrects them it says so and leaves the original
text visible, because a deleted claim cannot be audited.

### 10.1 Finding 1: the fifth site is real, and my own grep is why it was missed

`ue-probe/tests/vignette-spec-test.cpp` 4259 to 4266, the block headed "THE
CONTROL QUADS, PLACED AGAINST THE COMMITTED CAMERA", read this spawn:

    const LedgerVignette::Camera* CamA = 0;
    ...
    if (!S.Shots.empty() && S.Cameras[I].Id == S.Shots[0].CameraId)
    {
        CamA = &S.Cameras[I];
    }

and every placement, box and quad line in that block (4275, 4277, 4293 to
4303, 4336, 4353) is computed from `*CamA`. The resident's proof that it did
not follow item 10 is the right one: the block's printed quad lines are
IDENTICAL before and after (`quad colour at 7.50/1.43/3.50 m ... dist 3.51 m
inFrame 4/4`), which are cam_A's numbers (run 55, line 294:
`quadAskedXYZcm=750.0/350.0/142.7`). So after items 7 to 10 the suite's
accepting fixture for the quads was measuring cam_A's placement while the
engine makes cam_B's: one implementation too many of the same rule, in the
file section 3 moved the other one out of, and exactly the fault the refusal
of the .cpp literal was for.

WHY THIS RULING DID NOT SEE IT (rule 3, the ruler). Section 0's grep of the
test file was `ControlQuad|ControlCamera|cam_A|cam_B`, case-sensitive: line
4262 carries none of those tokens (`Shots[0].CameraId` was grepped in the
header, not in the test; and the variable is `CamA`, which `cam_A` does not
match). The header grep `first shot|FIRST SHOT|Shots\[0\]` missed
SurfaceBind.h:2648, which spells "FIRST shot's". Section 4's "four sites" was
a count from those greps, and it was wrong. A grep this spawn for
`Shots\[0\]\.CameraId|first shot's camera|FIRST shot's camera|FIRST SHOT'S
camera` over `ue-probe/` returns, with the rig repeat's "first shot" lines
(VignetteShot.cpp 3247 and 4159, FrameStats.h 1825) and this ruling's own
text (SurfaceBind.h 2746, test 4417 and 4419) set aside as not sites:

- test 4262: CODE, the fifth site. Dictated, edit 21.
- SurfaceBind.h 2648 to 2654: a COMMENT in the hide rule's own section, "They
  are placed 3.5 m in front of the FIRST shot's camera ... vignette-spec-test
  measures one quad's left edge landing at column 1274 of a 1280 wide frame".
  Stale on both halves after item 10. Edit 24.
- VignetteShot.cpp 3214: a verdict HEADER line, `Out.Add(TEXT("#   in front
  of the first shot's camera, off the same base material,"))`, PRINTED into
  every verdict. Edit 25.
- VignetteShot.cpp 1092 to 1096: the tally's comment, "measures one of them
  reaching column 1274 of cam_hook's 1280 wide frame". Stale by the numbers
  in 10.2. Edit 26.

The identifier `CamA` in the 4252 block holds cam_B's camera after edit 21
and is renamed (edit 23), as is `CamAYaw` at 4476 to 4477, which is the quad
camera's yaw and never was cam_A's by anything but accident.

### 10.2 Finding 2: cam_B stands, the hide rule is the single guard, and the guard gets a pixel proof

THE MEASUREMENT, THE RESIDENT'S, COPIED: from cam_A the three quads projected
off cam_hook's 1280-wide frame (centres 1349 to 1733 px) with one quad's edge
inside it (`centres=0/3 eitherEdge=1/3 ahead=3/3`); from cam_B they project
into the middle of it (`centres=3/3 eitherEdge=3/3 ahead=3/3`, centres
537/391, 532/392, 528/393 px, 17.5 to 19.4 m forward). No check went red
because the block gates on `ControlQuadsVisibleFor` and not on geometry, and
the summary word `controlQuadIntrusion` read `at-least-one-quad-reaches-the-
frame` both before and after.

WHAT SECTION 3 GOT WRONG, AND HOW MUCH. Section 3 said cam_hook "must not
carry a quad because a quad there would sit in every band statistic" and
that cam_B's quads are "hidden on every other shot by the rule that already
exists"; it did not say they stand inside cam_hook's frustum, and it did not
predict the geometry it changed. That is on this ruling. The size of the
trade is smaller than "two guards to one": the geometric guard was ALREADY
breached before item 10. The hide rule's own section in the header (2652 to
2654) and the tally's comment in the .cpp (1092 to 1094) both record one
quad's left edge at column 1274 of cam_hook's 1280-wide frame from cam_A,
and the block's word said "at-least-one-quad-reaches-the-frame" before as
after, which is precisely why the word did not move. The hide rule was
already the only thing between that quad's edge and the hook frame's pixels.
The trade is from one edge to three centres, not from nothing to three.

WHY NO OTHER DISTANCE ON cam_B RESTORES GEOMETRY, BY ARITHMETIC ON PRINTED
NUMBERS. cam_hook is at x 4.0, z -2.10, yaw 11, 39.0 degrees vertical, which
the spec's own note converts to 64.4 degrees horizontal at 1280x720. At 17 m
ahead the half-width of that field is about 11 m (17 times tan 32.2), which
is the whole street and both footways; above the top edge would need about
8.8 m of height (1.65 plus 17 times tan 22.1). Anything cam_B can stand 1 to
5 m in front of itself, at x about 18.5 to 21 in the carriageway, is inside
cam_hook's frustum. Geometry on cam_B is not recoverable by a number, so the
second option the resident named is not available as "another distance".

WHAT WOULD RESTORE IT, NAMED AS THE NEXT RUNG AND NOT TAKEN: a fourth camera
that exists for the controls, standing at x about 4 and looking along -x, so
its quads stand at x about 0.5, BEHIND cam_A and cam_hook (both at x 4
looking +x) and about 80 degrees off cam_B's axis. It needs one shot of its
own (the quads are hidden on every shot whose camera is not the control
camera, so a camera with no shot is an instrument that is never
photographed), which makes 50 shots and moves every shots-denominator on the
page (`controlQuadHidden=47/49`, `wetnessShotsAtValue=35/49`,
`figureShownShots=12/hidden=37`) and every prediction in section 8, which is
written against 49. A builder task with a spec change under it; his order
puts it behind the slice; filed by the resident (edit 30), not taken.

THE SINGLE GUARD, READ SO THAT "SINGLE" MEANS SOMETHING. VignetteShot.cpp
6413 to 6427: when a pass is prepared for a shot (`GPassPrepared =
GShotPass`), `ControlQuadsVisibleFor(S.CameraId, control camera id)` decides
`bShow` and every actor in `GQuadActors` gets `SetActorHiddenInGame(!bShow)`;
the count prints as `controlQuadHidden=47/49`. One call site, one function
in the tested layer, applied per prepared pass, so the settle re-takes and
the probe frames of a shot inherit the shot's state; 6428 says the repeat
"is not a shot and is not counted as one", and whether the repeat path
re-prepares is not read here and is named as the one thing this paragraph
does not know. What the guard is: a game-thread claim about actor state,
not a pixel. What its failure looks like after today: three quads of about
40 px (0.7 m at 17.5 to 19.4 m through a 39 degree vertical field) near
column 530, row 392 of every cam_hook frame, in the middle rows (not the
skyTop band's rows 0 to 90 nor the ground band's 576 to 720 that the sheet
comparison reads), about 0.5 per cent of the frame, visible to an eye on the
hook pair and silent to every key.

RULED: cam_B STANDS for this dispatch, on three conditions.

(a) THE GUARD GETS A PIXEL PROOF, WHICH IS STRONGER THAN THE GEOMETRY IT
REPLACES BECAUSE IT READS THE ARTIFACT. Queue 339's acceptance gains its
second half: on every shot whose camera is not the control camera and whose
projected quad boxes fall in frame, the box where a HIDDEN quad would stand
is sampled with 339's own statistic (within-box channel spread, the four
quadrant means beside it) and printed with the count of boxes graded over
boxes in frame; the accepting case (cam_B, visible, four colours on the
colour quad) prints first and the rejecting case (cam_hook, hidden, street
pixels in the box) beside it, per shot. No bound is set here: the series
313 and 339 printed (148.4 against 10.2 and 16.1) was measured on cam_A
frames and is re-read on cam_B and cam_hook frames before any number is
chosen (rule 2). Instrument-builder, measurements lane, declared maxTurns 70,
two-armed exit "the two words print on the cam_B and cam_hook lines of a
landed run with their denominators, or a named reason nothing was sampled".
Edit 29 amends 339.

(b) UNTIL IT LANDS, ONE HUMAN LOOK AT A NAMED BOX, NOT "BY EYE". On the first
landed run the resident opens `ue-vign_hook_day.png` at the three printed
centres, 537/391, 532/392 and 528/393, each about 40 px square, and writes
beside the look what is there. Rule 4: a picture is strong evidence that
something is wrong; the coordinates are what make this a look at a named
box rather than the reading instruments.md forbids. A square there is a
guard failure and stops the run being read for anything else.

(c) THE WORD CARRIES THE COUNTS. `controlQuadIntrusion` becomes a three-way
word with the two counts printed beside it (edit 27), so that a grep on that
key sees the difference the numbers saw. The block's existing checks (4511
to 4519: the control camera sees them, cam_hook does not, an unnamed camera
on either side hides them) are the guard both ways and stay.

WHAT IS NOT RULED: any change to the 3.5 m, the 0.7 m size or the lateral
offsets (queue 123's numbers, and no value of them helps, by the arithmetic
above); any change to `ControlQuadsVisibleFor`.

### 10.3 The cap series: 1200 stands, and the next person reprints

The builder's series, copied: run 56 predicted 1147 characters, worst
plausible 1173 (two more procedural names), so 1200 leaves 53 and 27, and a
third procedural surface bites. My section 2 said "already near 800
characters by count of the literals", which was an eyeball count and 347
low, which is the thing rule 2 forbids as the basis of a bound; the printed
series is the evidence and my estimate is not. Item 1 was load-bearing: at
900 every case would have cut, and items 3 and 4 alone would have turned
test 2420 red.

RULED: 1200 stands for this dispatch. It is measured, it does not bite on
run 56, and a third procedural surface in the live spec prints
`surfacePopulationCut=yes/at-1200-chars` on the done line rather than
truncating in silence, which is the project's rule for a cap. The standing
rule for this segment, written into the header beside the buffer (edit 28):
whoever adds a key or lengthens a name list reprints the two numbers
(next-run predicted, worst plausible) beside the change and raises the
buffer in the same edit when the worst-plausible margin is smaller than what
they add. The next rung, filed not taken (edit 31): build the segment as a
string join with no fixed buffer, so the class of fault leaves the file.

### 10.4 Dictated edits, continuing section 7's numbering, verbatim, in this order

The g++ suite runs after edit 27; verify after all; the fallback is section
7's: on any compile failure or red check, the whole of 21 to 28 goes to one
instrument-builder (maxTurns 70) with the exit "suite green with the counts
in the intrusion word printing, or a named failing check".

21. `ue-probe/tests/vignette-spec-test.cpp` line 4262:
    `if (!S.Shots.empty() && S.Cameras[I].Id == S.Shots[0].CameraId)`
    becomes `if (S.Cameras[I].Id == LedgerSurface::ControlCameraId())`.
22. Same file, lines 4269 to 4270 become:
    ```
    			std::printf("    control quads: nothing measured, the spec carries no camera "
    			            "named by ControlCameraId\n");
    ```
23. Same file, identifiers, in this order: first `CamAYaw` at 4476 and 4477
    becomes `QuadCamYaw` (both lines); then every whole-word `CamA` in the
    file becomes `CtrlCam`. The resident greps `\bCamA\b` BEFORE (prints the
    count) and AFTER (expects 0), and greps `CtrlCam` after (expects the same
    count). Then the resident reads lines 4288 to 4296 and, where the comment
    says cam_A's frame is the one the street is read for, corrects on sight
    with "cam_B, the control camera since 2026-09-21, which no judged reading
    is taken from"; a comment, D43.
24. `ue-probe/Source/LedgerProbe/Public/SurfaceBind.h`, lines 2648 to 2654,
    from `They are placed 3.5 m in front of the FIRST shot's camera` through
    `the picture a person is being asked to judge a street by.` become:
    ```
    	// They are placed 3.5 m in front of ControlCameraId()'s camera (cam_B
    	// since 2026-09-21; the first shot's camera, cam_A, before that) and
    	// nothing in that placement knows any other camera exists, so a second
    	// camera pointed anywhere near the same stretch of road photographs
    	// them. cam_hook, the rung 1 viewpoint, is exactly that case: from cam_A
    	// vignette-spec-test measured one quad's left edge at column 1274 of a
    	// 1280 wide frame; from cam_B it measures all three centres inside it
    	// (about column 530, row 392, 17.5 to 19.4 m ahead). So this rule is the
    	// ONLY thing keeping an instrument out of the picture a person is being
    	// asked to judge a street by, and queue 339's second half is the pixel
    	// proof that it holds.
    ```
25. `ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp` line 3214:
    `Out.Add(TEXT("#   in front of the first shot's camera, off the same base material,"));`
    becomes
    `Out.Add(TEXT("#   in front of the control camera (cam_B, ruled 2026-09-21), off the same base material,"));`
26. Same file, lines 1092 to 1094, the words `vignette-spec-test measures one
    of them reaching column 1274 of cam_hook's 1280 wide frame, which is an
    instrument standing in the picture rung 1 is judged by` become
    `vignette-spec-test measured one of them reaching column 1274 of
    cam_hook's 1280 wide frame from cam_A, and all three centres inside it
    from cam_B (2026-09-21), which is an instrument standing in the picture
    rung 1 is judged by unless this rule hides it`.
27. `ue-probe/tests/vignette-spec-test.cpp`, lines 4520 to 4524 become:
    ```
    			std::printf("    cam_hook controlQuadIntrusion=%s centres=%d/%d edges=%d/%d "
    			            "(this is WHY the rule above exists, and it is measured "
    			            "rather than assumed; since 2026-09-21 the hide rule is the "
    			            "only guard and the word says so)\n",
    			            EdgesIn == 0 ? "none-reaches-the-frame"
    			            : (CentresIn == 0 ? "edges-only-reach-the-frame"
    			                              : "centres-in-frame/hidden-by-the-rule-alone"),
    			            CentresIn, LedgerSurface::ControlQuadCount(),
    			            EdgesIn, LedgerSurface::ControlQuadCount());
    ```
28. `ue-probe/Source/LedgerProbe/Public/SurfaceBind.h`, insert immediately
    ABOVE line 2415 (`char Buf[1200];`):
    ```
    		// THE BUFFER IS A CAP WITH A PRINTED SERIES: run 56 predicted 1147
    		// chars, worst plausible 1173 (two more procedural names), so 1200
    		// leaves 53 and 27. Whoever adds a key here or lengthens a name list
    		// reprints those two numbers beside the change and raises this in the
    		// same edit when the margin is smaller than what they add. A third
    		// procedural surface in the live spec prints surfacePopulationCut on
    		// the done line rather than truncating in silence. Ruled 2026-09-21.
    ```
29. `production/queue/339-*.md`, appended under `acceptance:` as its second
    half: `SECOND HALF, ruled 2026-09-21 (section 10.2 of the ruling of that
    date): on every shot whose camera is not the control camera and whose
    projected quad boxes fall in frame, the box where a hidden quad would
    stand is sampled with the same statistic and printed with the count of
    boxes graded over boxes in frame; accepting case (cam_B, visible, four
    colours) first, rejecting case (cam_hook, hidden, street) beside it, per
    shot; no bound until the series is re-read on cam_B and cam_hook frames.
    This is the pixel proof of the hide rule, which since 2026-09-21 is the
    only thing keeping the quads out of cam_hook's frame.`
30. One new queue item, filed by the resident, BLOCKED behind the slice on
    his order: a dedicated control camera standing at x about 4 looking
    along -x with one shot of its own, so the quads stand behind cam_A and
    cam_hook and outside cam_B's field; acceptance is the cam_hook block
    printing `controlQuadIntrusion=none-reaches-the-frame centres=0/3
    edges=0/3` on the committed spec, every shots-denominator on the page
    read against 50, and section 8's predictions re-derived. Number written
    here when filed: ______.
31. One new queue item, filed by the resident, low, measurements lane: build
    `SurfacePopulationSegment` (and the other snprintf-capped segments on the
    materials line, by grep for `Cut=yes`) as string joins with no fixed
    buffer, so a cap cannot bite; acceptance is the `Cut=` keys gone from
    the header with their test checks retired by name. Number written here
    when filed: ______.

### 10.5 What the first landed run must print, added to section 8

The three quad lines: `quadOn=cam_B/1280x720`, `quadDistM=3.51`,
`quadCornersInFrame=4/4`, `quadDeltaCm=0.00`; the asked XYZ is cam_B's and is
not predicted here beyond that (the asked/read pair on the line is its own
check). The verdict header carries "in front of the control camera (cam_B,
ruled 2026-09-21)". `ue-vign_hook_day.png` opened at 537/391, 532/392 and
528/393: street, no square (10.2 b). The suite's own line reads
`cam_hook controlQuadIntrusion=centres-in-frame/hidden-by-the-rule-alone
centres=3/3 edges=3/3` on the committed spec until edit 30's camera exists,
and that reading is the honest one.

### 10.6 What this addendum did not do

It did not read where `GQuadActors` is hidden on the repeat path (named in
10.2 as unknown). It did not set a chroma bound for the hidden-box proof (no
series on cam_B or cam_hook yet). It did not move 3.5 m, 0.7 m, 1200, or any
number section 7 set. It did not re-run the suite.

## 11. Second addendum, spawn row 737: the reference moved, two D43 sites, the rename a bare sed would have corrupted, and the ladder that proves the word

### 11.0 Why this file carries a new stamp, and only one

The resident committed the ruled state of sections 1 to 10 as `7a7be367`,
which moved `director_cadence`'s reference commit past row 733; edits 21 to
28 and two D43 comment corrections were then applied (123 gated lines of
123), and the gate is red until a `studio-director` row NEWER than that
commit is named by a stamp. The harness wrote rows 735 (`2026-09-21T15:04:
02Z`) and 737 (`2026-09-21T15:34:14Z`) for this same session (same agent id
as 733), and 737 is newer than `7a7be367` because the message that produced
it reports the commit as done. So the stamp at the foot names row 737. The
14:30:16Z stamp that closed sections 1 to 10 is retired from the foot into
this paragraph, so that this file carries ONE machine-readable stamp, the
newest, and no parser can read the older one first: it named row 733 and it
cleared `7a7be367`.

Read as applied (section 0, "For section 11"): test 4259 to 4270 reads
`CtrlCam` and `S.Cameras[I].Id == LedgerSurface::ControlCameraId()` with the
`named by ControlCameraId` printf; test 4521 to 4529 prints the three-way
word with `centres=%d/%d edges=%d/%d`; VignetteShot.cpp 6181 to 6193 is edit
10 as dictated; SurfaceBind.h 2773 is `ControlCameraId()`; 2714 to 2739 is
site 7 as the resident described it. The counts are the resident's, confirmed
by the resident: suite 628 checks, 0 failed; `\bCamA\b` 14 to 0, `CamAYaw` 3
to 0, `CtrlCam` 0 to 14; `ue-probe instruments ok (3610 checks)`.

### 11.1 Site 6, VignetteShot.cpp 1075 to 1080: NOT an overstep

"One extra plane per control in front of the camera the first shot uses"
was prose spelling the rule that edit 10 replaced; CLAUDE.md rule 1 says
changing code changes the comments about it, and D43 says a correction that
only fixes a document is applied and reported. A comment in a file that does
not compile locally cannot break a build. The resident replaced the rule
with `LedgerSurface::ControlCameraId()` and recorded why it survived the
greps (it names neither `cam_A` nor `Shots[0].CameraId`). RULED: correctly
applied, and the record of why it survived is the useful half.

### 11.2 Site 7, SurfaceBind.h 2719 to 2735: the strike was right, and the decision gets its reason now, from printed numbers

THE RESIDENT'S JUDGEMENT, UPHELD. The old sentence ("At cam_A the right of
the frame is the shopfront ... so the controls stand over the carriageway
and leave the half a reader is judging the street from alone") was false on
both halves once the control camera became cam_B, and replacing it with a
cam_B sentence would have asserted what cam_B's left half carries without
measuring it, which is the fault of the day. Striking the reason and keeping
the decision was right.

THE TRADE IS NOT THE BEST AVAILABLE, BECAUSE A LIVE REASON EXISTS WITHOUT
LOOKING AT cam_B. The offset is two decisions with two different reasons now,
and both can be derived from numbers already printed:

- THE SPACING (`ControlQuadFirstM()` 0.50 m off the axis, `ControlQuadPitchM()`
  1.00 m centre to centre) is not arbitrary. Run 55's quad lines (verdict 294
  to 296) print the three boxes at `x130..261`, `x309..437` and `x488..614`
  on rows `298..422`: 126 to 131 px wide, 177 to 178 px centre to centre, 48
  and 51 px of street between them, `quadCornersInFrame=4/4` on all three at
  `quadDistM=3.51`. The row is centred on the view axis (`ControlQuadPlace`'s
  own comment, 2793 to 2796, and `quadCentrePx=551/360` on line 294), and
  cam_B's vertical field is the same 60 degrees as cam_A's (spec 849 and
  862), so those boxes are cam_B's boxes too. Three separate boxes, none
  overlapping, all inside the frame at one distance, is what the readback
  (queue 339) needs. That is the whole of the spacing's reason and it holds
  on any camera with that field.
- THE SIDE (the sign, left) was cam_A's composition reason and has no reader
  to serve on cam_B, where no reading is judged (section 3). It is kept
  because moving it moves every printed box for no measured gain. The boxes
  sit on rows 298 to 422, outside the skyTop band (rows 0 to 90) and the
  ground band (rows 576 to 720, line 208's `rectPx`), so cam_B's band
  statistics carry no quad either way; its whole-frame keys do, and the shot
  line already says so (`shotWholeFrameIncludesControlQuads=yes/...`).
- THE CONDITION FOR RE-DERIVING, NAMED: if the control camera ever becomes a
  camera a reading is judged from, the side needs a measured reason again,
  and that is the day to measure it. Nothing about what cam_B's left half
  carries is asserted.

WHO DERIVES: nobody measures cam_B. The derivation is this ruling's, from
run 55's printed lines and the header's own axis-centring rule, and it is
dictated as a comment (edit 32) appended after the resident's paragraph,
which stays as written.

### 11.3 The rename: dictated whole-word, honoured whole-word, and the key it would have eaten

Edit 23 said "every whole-word `CamA`". The builder used `\bCamA\b` and
verified that `shotCamAskedXYZcm` (test 5100), which carries `CamA` as a
substring, is intact; the resident confirmed the key. A bare
`sed s/CamA/CtrlCam/g` would have renamed a verdict KEY in the suite's
expectations silently, and the first landed run would have failed a check
whose message named a key nobody changed. Rule 5 in one line, for the
resident to add to casebook-claims under rule 5 if it judges the line worth
its length (D43-class, its call): "a rename over a file that spells verdict
keys is word-bounded and the key list is grepped for the token as a
substring FIRST; `CamA` inside `shotCamAskedXYZcm`, 2026-09-21".

### 11.4 The four-rung ladder is the evidence for edit 27, and its cap is honest

The builder's ladder, copied: same vantage, four runs, code and spec
crossed. Rungs 1 and 2: the old word `at-least-one-quad-reaches-the-frame`
for two different worlds, `centres=3/3` and `centres=0/3`. Rungs 3 and 4:
the repaired word with its counts, and rung 4 reproduced the 1274 px left
edge from cam_A, so edits 24 and 26 quote a measurement that ran today and
not an inherited number. Two of the word's three branches were exercised;
`none-reaches-the-frame` was not, and the builder did not manufacture a
rung for it, because 10.2's arithmetic says no position on cam_B produces
one. RULED: that is rule 5b honoured, not dodged. A branch that cannot be
exercised on the committed spec is named as unexercised, and it is
exercised the day edit 30's camera exists, whose acceptance is exactly that
word with `centres=0/3 edges=0/3`.

### 11.5 The third instance today of an instrument's scope hiding its target, and it was mine

The builder's note, accepted: site 7's `cam_A` and its `controls` sit on
different lines of one comment, so any line-scoped grep AND-ing the two
terms cannot see it; a bare `cam_A` over ue-probe returns 20 hits, 2 stale
about the quads and 18 legitimately about the figure, the player start, band
statistics and fixtures. With 10.1 (case-sensitive `first shot`, and
`Shots[0]` grepped in the wrong file) that is three misses by one ruling's
own greps in one day. The lesson, for the resident to add under rule 1 in
casebook-claims if it judges it worth its length (D43-class): "a count of
sites is a count of one grep's matches. Grep each spelling of the rule
separately (the code token, the prose in every case, the identifiers derived
from it) over the whole file family, then READ the section the rule lives
in, because a rule spelled across two lines is invisible to every line
grep." This ruling's own counts (section 4's four, 10.1's five) were wrong
by that mechanism, and section 11 says so rather than quietly correcting
the numbers.

### 11.6 Dictated edit, verbatim

32. `ue-probe/Source/LedgerProbe/Public/SurfaceBind.h`, insert immediately
    BEFORE line 2736 (`inline double ControlQuadOffsetM(int I)`), after the
    resident's paragraph ending `...owed by whoever next measures what
    cam_B's left half carries.`, which stays as written:
    ```
    	//
    	// DERIVED 2026-09-21 (ruling of that date, section 11.2), FROM PRINTED
    	// NUMBERS AND NOT FROM A LOOK AT cam_B. The offset is two decisions and
    	// they have different reasons now.
    	//   THE SPACING (0.50 m first centre off the axis, 1.00 m pitch) is not
    	//   arbitrary. Run 55's quad lines print the three boxes at x130..261,
    	//   x309..437 and x488..614 on rows 298..422: 126 to 131 px wide, 177 to
    	//   178 px centre to centre, 48 and 51 px of street between them,
    	//   quadCornersInFrame=4/4 on all three at quadDistM=3.51. The row is
    	//   centred on the view axis (ControlQuadPlace below) and cam_B's
    	//   vertical field is the same 60 degrees as cam_A's, so those boxes are
    	//   cam_B's boxes too. Three separate boxes, none overlapping, all
    	//   inside the frame at one distance, is what the readback (queue 339)
    	//   needs, and it is the whole of the spacing's reason.
    	//   THE SIDE (the sign, left) was cam_A's composition reason and has no
    	//   reader to serve on cam_B, where no reading is judged. It is kept
    	//   because moving it moves every printed box for no measured gain. The
    	//   boxes sit on rows 298..422, outside the skyTop band (rows 0..90) and
    	//   the ground band (rows 576..720), so cam_B's band statistics carry no
    	//   quad either way; its whole-frame keys do, and the shot line says so.
    	//   If the control camera ever becomes one a reading is judged from, the
    	//   side needs a measured reason again, and that is the day to re-derive
    	//   it. Nothing about what cam_B's left half carries is asserted here.
    ```
    A comment: no suite re-run is owed for it; verify runs before the commit
    as always.

### 11.7 What this addendum did not do

It did not run git, so "737 is newer than 7a7be367" rests on the order of
events in the resident's message and on the log, not on a commit timestamp
read by this director. It did not measure cam_B's frame. It did not add the
two casebook lines itself (D43-class, the resident's call). It did not
change any number.

<!--RULING spawn=2026-09-21T15:34:14Z-->
