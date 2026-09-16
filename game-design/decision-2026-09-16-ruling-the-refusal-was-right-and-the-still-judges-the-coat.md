<!--RULING spawn=2026-09-16T18:42:46Z paths=ue-probe/Source/LedgerProbe/Public/FrameStats.h,ue-probe/tests/frame-stats-test.cpp,ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp,tools/ue/import_figure.py,tools/ue/make_base_material.py,ledger/verify.py,tools/morning-brief.py,game-design/decision-2026-09-16-ruling-the-refusal-was-right-and-the-still-judges-the-coat.md-->
STATUS: LOG, 2026-09-16. NOT CURRENT once the first run with a figure in it
has landed and its night stills have been read under section 3's protocol;
from then the run verdict and queue 372's series are the reading copies and
this file is their history.

Director ruling, 2026-09-16, on the three-builder batch: the figure's
measurement half (queue 368, FrameStats.h), the figure's engine half (queue
368, import_figure.py, VignetteShot.cpp, make_base_material.py), and the
withdrawn studio-versus-game ratio (Jafar's order of 2026-09-16, verify.py,
morning-brief.py). Queue 372 and 374 are ruled on as filed.

Spawn row, quoted verbatim from `.claude/agent-log.tsv` line 707, the last
studio-director row at the time of writing:
2026-09-16T18:42:46Z	studio-director	fable	default	a5f61169909846042

HEAD reviewed: 7a620fd2 (`.git/refs/heads/main`), with the batch uncommitted
on top of it; the cadence gate's reference is 73c902b5. This spawn had no
shell, so NOTHING BELOW WAS RUN: every line cited was read this session,
every printed number is quoted from the file that printed it, and every
number I re-derived says so and shows the constants it came from. The
selftest counts in this record (236/0, 70/0, 170/0, 82/0, 75/0, 41/0) are the
resident's runs as reported in the brief, and the commit message carries
them again from the run that precedes it, not from this file.

## 0. The verdict in one paragraph

ALL THREE PIECES LAND, with four dictated one-line corrections in the same
batch (section 8), none of which touches a mechanism or a number a run reads.
The engine builder's refusal was correct and the brief was wrong: the route
through the editor process stands. 77 px is accepted as the first value of a
series and NOT as the acceptance's answer; the still judges the coat, and if
it says no, every lever is schema and comes back here. The pose asymmetry
stands: an unreadable instrument is not a failed subject. The 14-to-1 ring
was right to file and does not block, and the line gains the words that say
what its ring is. The unconditional withdrawal marker stands, for a different
reason from the one the builder gave. Queue 374 waits behind the slice. The
hand correction to the test header is upheld. This ruling covers the 647
gated lines and the four one-liners for `director_cadence`; no second
director is owed for anything in section 8.

## 1. Question 1: the refused instruction and the route through the editor

THE REFUSAL WAS RIGHT. The brief instructed a new step in
`.github/workflows/ledger-probe-unreal.yml`. `tools/workflow-size.py` carries
the evidence in its own text: `KNOWN_GOOD = 23184` (:51), "23184 dispatched
fine, repeatedly, all morning" and "24868 422, max expression length"
(:31-32), and its done line prints the headroom against that largest
accepted block (:162). The resident reproduced 17 characters of headroom on
the build step. A 422 at dispatch is no Windows build at all (:158). A builder
that measures before obeying is the studio working; the instruction, obeyed,
would have taken down the only channel out of CI, which is queue 360's whole
content.

THE ROUTE STANDS, and every link was read (rule 6):
(a) `make_base_material.py:4018-4033`: inside `_inside_unreal()`, after the
    material and the sky lines are already on disk (:3929 is the material's
    path, :3994 the sky's append, both above :4018), `import_figure.main()`
    runs in a try; a raise appends `figureImportStatus=RAISED
    figureImportReturn=2 figureNote=...` to ue-material.txt. The material's
    own `_code` is not touched by the figure's return (:4022 discards it).
(b) `import_figure.py:1395-1400` appends its one line to ue-material.txt
    beside the uproject; :1426-1429 refuses to write anything outside the
    editor; :1436-1448 never raises SystemExit inside the editor.
(c) The yml deletes `$matOut` before the run (:302) and reads it whole
    (:314), which is what makes a stale figure line impossible under a new
    run's name. The selftest's G2 section (:1037-1066) asserts (a) and (c)
    against the live files, accepting case first.
(d) Precedent: the sky material took the same route for the same reason and
    the 16:06Z ruling, section 2(e), traced that chain link by link.

THE COST, NAMED SO IT IS NOT DISCOVERED: the figure import runs in the ONE
editor process the step starts. A native crash inside the FBX importer takes
that process down and with it the cook that follows, so that run would lose
everything, not only the figure. Accepted, because it runs LAST in that
process (everything before it is on disk), because a second step is
impossible at 17 characters, and because a second editor launch is exactly
the cost 360 exists to avoid. If a run ever ends with `figureImportStatus`
absent from the verdict AND the material line present, that is this failure
and it reads as such.

THE BRIEF'S FAULT, RECORDED (waste lesson 2): the constraint the builder had
to measure for itself is in no role file. `.claude/agents/engine-specialist.md`
has no hit for `workflow-size` or `360` (grep this session; its frontmatter
reads `model: opus`, `maxTurns: 45`). Section 8, item A4.

## 2. Question 2: seventy-seven pixels, and what judges the coat

THE NUMBER, CHECKED BY HAND from the constants in `import_figure.py`. cam_A
is at x=4, z=4, eye 1.6 m, pitch 4 degrees down, `fov_vertical_deg` 60
(`vignette-scene.json:846-849`); the engine projects with the same vertical
convention, `TanV = tan(FovVerticalDeg/2)` (SurfaceBind.h:2657), and sets the
camera from `HorizontalFovDeg(C.FovVerticalDeg, ...)` (VignetteShot.cpp:2759),
so the derivation and the projection agree on what 60 means, which was the
instrument question to ask first (rule 3). At x=17.5 the figure is 13.5 m
out; the frame is 2 x 13.5 x tan(30) = 15.59 m tall there; 1.66 m of it is
76.7 px of 720. The series: at x=17.5 the back term is 1/8.258^2 + 1/11.25^2
+ 1/22.1^2 = 0.0246 against a front term of 1/10.32^2 = 0.0094, ratio 2.62,
dominant backlight 28.7 degrees; at x=18.0 the x=18 lamp's dot product is
zero and it moves to the front term, ratio 0.45. The C++ carries 17.5 / 4.0 /
0.125 / 0.35 at :471-486 and the selftest's section G reads them back.

THE CONFLICT IS THE STREET'S, NOT THE BUILDER'S. The acceptance in 368 has
two halves: reads as a person in a coat, and dark against lit ground. On this
street they pull apart: every position nearer than the x=18 lamp has the x=8
lamp between the camera and the figure (front-lit) or overhead (63 degrees,
top-lit); the far end is where the backlight is. The search took the
backlight as the constraint and the size as a band (6 to 20 m) and the
answer came out at the far side of the band. Nothing a builder may touch
changes that: the camera row, a shot row and the lamp positions are all
schema.

RULING. 77 px is the FIRST VALUE and this ruling certifies nothing about the
coat. A figure at 13.5 m in a 60-degree vertical field is a person at
mid-distance on a street, the size every pedestrian a GTA or KCD2 player
walks past has for most of a play session, so the ask is not unreasonable;
whether THIS body's outline reads as a coat is the still's question and
Jafar's feel check is the instrument (D41; Meridian Test 1). Options weighed:
(A) run as placed and read the frames; (B) move nearer inside the band, x=14
at ratio 0.95, about 104 px, which loses the silhouette by geometry and the
instrument would rightly print no; (C) a nearer or longer-lens night camera
row, which is schema and a ruling on frames that do not exist. (A) stands.
(B) is refused. (C) is the named rung IF the stills say the figure is too
small, and it comes back to a director then, with the stills, not before.

WHAT THE READER RECORDS from the night stills, per still, in words beside
the numbers: `projH` from the figure token against 76.7 (the engine's own
projection; a projH far from it is a placement or instrument fault and is
read BEFORE any taste question); whether the outline is a person or a
mannequin, and whether it is a coat or not; `figureSil` with its
`coreMinusRingMeanLuma`. If Michelle's clothes are not a coat at all, the
pick was wrong on the acceptance's own words (the standard sentence is
`fetch_bodies.py:64-65`) and the lever is another body of the same four, a
build product and a director's one-question spawn with the stills attached.

## 3. Question 3: STANDING-POSE-UNPROVEN and the sky dome's destroy rule

THE CODE. `FigurePoseCheck` (VignetteShot.cpp:5133-5173): any positive
worst-bone delta latches STANDING/pose-evaluated; after the 8-tick budget, a
delta of exactly zero DESTROYS (bind pose, :5165-5172) and a delta that could
not be read (-1, no component-space transforms, :4967-4970) leaves the figure
standing under STANDING-POSE-UNPROVEN (:5156-5163). The check ticks on
condition settle ticks: `ApplyCondition` at :6122 is re-entered every tick
for `kSettleAfterCondition = 0.5` seconds (:142, :6128), and calls
`DriveFigure` (:2379) which calls the check (:5198).

THE ASYMMETRY STANDS, on three grounds. (1) The sky dome's fault was a
success word over a wrong object: a 2 km sphere standing while the verdict
said fine. Here the word is not a success word and `figureWhy` names the
instrument. (2) Rule 3, the instrument first: a delta that cannot be read is
the ruler failing, and destroying the subject when the ruler fails makes a
ruler fault indistinguishable from a subject fault for ever after. The still
with the word beside it is the only evidence that can tell them apart: a
T-pose in it says the animation never ran, a posed person says the readback
is what is broken. (3) The 31 day rows are untouched either way, since the
figure is hidden wherever the lanterns are off (:5180-5185).

ONE GAP, NAMED AND NOT BLOCKING. The budget is in ticks and the settle is in
seconds. At 16 frames per second and above, eight ticks fit inside the first
lit condition's settle; below it the count carries across shots
(`GFigurePoseTicks` is never reset) and the bind-pose destroy can fire AFTER
the first lit shot's frame is on disk. The done line would then read
`figure=DESTROYED` beside `figureShownShots=1`, which is visible as a
contradiction but not attributable per frame, because the shot line's figure
segment carries no pose word. instruments.md: per-sample numbers on the
sample line. Rung Q-B in section 9. The first run reads `figurePoseTicks=N/8`
and `figurePoseLatched` on the done line and the frame times on the shot
lines, and that is enough to know whether this bit anyone.

## 4. Question 4: the ring that is the lamp's ring

THE ARITHMETIC, from the test's own fixture (frame-stats-test.cpp:1481-1506)
and `LampRingPadPx` (FrameStats.h:2028-2032, pad = the longer side): an 18 x
60 box gets 60 px of pad on every edge, 138 x 120 after the frame clips it,
15480 ring pixels over 1080 core, 14.3 to 1. In the real frame, at 77 px
tall and roughly 20 px wide, the pad is 77 and the ring is about 175 x 231
px, of the order of 20 to 1; with the horizon 48 px above centre at 4
degrees of pitch, that ring takes in sky and the far street above the head
and footway below the feet. `ringMeanLuma` is the brightness of that part
of the picture, as the builder said, and at night the dark sky in it drags
the ring mean DOWN, so the reading is biased towards the expensive failure
the test names at :1464-1468: a false NO on a real silhouette. That is worth
knowing before the first line is read, and it is why 372 is a real item.

FILING WAS RIGHT AND IT DOES NOT BLOCK. Changing the pad changes the
lantern's annulus, whose night series is measured; a second helper is the
copy nobody fixes; a "shorter side" rule is a bound nobody has measured
(rule 2), and 372's own card refuses to set it from an argument. Both
rectangles print in pixels on every token (:2593, asserted at :1645-1648),
so the ring is re-derivable from the line, and the signed
`coreMinusRingMeanLuma` is the series a margin will be read from.

WHAT IS DICTATED NOW: the line says what its ring is. Section 8, A1. The
comment beside the emit (:2335-2344) already says it; the token does not,
and the token is what a reader of the verdict has.

ONE OBSERVATION, NOT A FAULT: the header says six no-reading exits (:2376)
and the test plants six (:1565-1605); the seventh Why at :2511-2515,
`covers-no-pixel-of-this-frame`, is unreachable, since after clipping the
ring rectangle contains the core rectangle (RX0 <= CX0, RX1 >= CX1, same in
Y) and :2476 already refused an empty core. Dead, harmless, noted so nobody
plants a fixture for it.

## 5. Question 5: the marker prints in every branch

STANDS, and the reason that carries it is not the builder's first one. "A
marker that read withdrawn on a day with rows and nothing-measured on a day
without would leak one bit of the number" (verify.py:5584-5587) leaks
nothing the same line does not already print: `fableShareDay` at :5581-5583
says whether the newest day had rows. The reason that carries it is the
second sentence at :5587-5589: the refusal is prior to the log's contents.
A withdrawal is a ruling about a CLAIM, not the outcome of a measurement,
so it does not branch on `measured`; rule 3b governs measurements, and on
this line the three measured values still print `nothing-measured` when
they measured nothing (:5574-5575, :5583) and the prose names the absent
log (:5608-5613). The distinction 3b insists on is on the line, one key over.
`GAME_SHARE_WITHDRAWN` (:4003-4004) has one definition, imported by
morning-brief, and the rung at :7439-7472 asserts the tally still tells a
building day from a self-measuring day while both print the same marker,
which is the right shape for queue 370 to rebuild from. The fourth consumer,
`split_in_words` (morning-brief.py:1020-1041), gained
`theWithdrawalIsStated` at :1038; correct, and it guards a retired program,
which is why 374 exists.

FORMATTING LAW, corrected on sight: the comment this batch wrote at
verify.py:5587 carries an em-dash, and so does the rung comment at
morning-brief.py:2356. Section 8, A2.

## 6. Question 6: can 374 wait

IT WAITS. The door is open and unsignposted: `producer-check.py:209` takes
`split` out of every register; `.claude/agents/producer.md` has no
instruction to state the split (its one `split` at :223 is the write/send
split, another sense); today's brief carries no split sentence (374's own
check); the only artifact a Producer could copy the number from now prints
the withdrawal; nothing generates the Sunday summary. Rule 11 in Jafar's own
words: the finding is filed and the standing order resumes. The condition
under which it stops waiting: a brief or summary stating the ratio before
374 lands is a Blocking gap in the run that finds it, answered in that run,
not a queue item.

## 7. The hand correction, upheld

frame-stats-test.cpp:14-23 now cites the gate's flags and the reason; the
gate compiles at `g++ -std=c++11 -O1 -Wall` (verify.py:1028). A header
claiming a looser standard is the one direction that lets hand-clean code
fail in CI. Upheld as written.

Also read and holding: D18 as a measurement, `h >= 120` cm on the FBX's own
vertices (import_figure.py:879-885) with the resident's 166.442 cm going on
the line as `figureSourceCm`; D46 on the allowlist
(`license-allowlist.md:6`, Mixamo characters AND animations); the height
verdict's decade bands (:365-391) which cannot judge the figure and say so;
`figureScalePolicy=1/never-scaled`; and the four placement literals read
back out of the C++ by the selftest (:1005-1035) so the derivation and the
constants cannot drift.

## 8. What lands in this batch, and who does it

Everything in the brief's file list, plus these four, each a one-line fix
the resident applies (CLAUDE.md, the studio split), and none owed a second
director:

A1  FrameStats.h:2704, the `figureSilStat` literal: insert
    `/ring=box-grown-by-its-LONGER-side-on-every-edge/queue-372` before
    `/strictly-darker`. The Head buffer is 512 and the head is about 240
    with that added, and the cut announces itself at :2711-2714 regardless.
    Re-run the g++ test at the gate's flags and paste its
    `frame-stats-test: N check(s), 0 failure(s)` line into the commit.
A2  Formatting law: the em-dash at verify.py:5587 and the one at
    morning-brief.py:2356 become commas. Comments only; the selftests are
    re-run because the commit runs them anyway.
A3  import_figure.py:186-187: the comment's "28% of frame height at 6 m and
    8% at 20 m" is not what the function beside it prints. From
    `figure_height_px`: 177 px (25%) at 6 m and 53 px (7%) at 20 m for a
    1.7 m figure. The resident replaces the two figures with those, or with
    the values `--measure` prints, never with the comment's own.
A4  `.claude/agents/engine-specialist.md`, one line under its constraints:
    before adding any step to `ledger-probe-unreal.yml`, run
    `tools/workflow-size.py` and paste its headroom line into the hand-back;
    a step that does not fit goes through the editor process
    `make_base_material.py` already starts, as the sky material and the
    figure import do. A document; commits on the resident's read.

No builder is dispatched by this ruling. If the resident finds A1 breaks a
test assertion this reading missed, that is a partial to report, not a
reason to widen the change.

## 9. Queue items opened by this ruling (named, not done: rule 11)

Q-A  Queue 372's first step, annotated onto the card: when the first figure
     frames exist, print a SECOND annulus beside the first on the same
     token, padded by the shorter side, with its own rectangle, neither
     deciding, so the pad rule is chosen from two printed series rather than
     one series and an argument. The lamp's helper is not touched by that.
Q-B  A per-shot pose word on the figure segment: the pose state AS OF THE
     SHUTTER (evaluated / unproven / not-yet / destroyed) on the shot line,
     so a still can be attributed without reading the done line's
     cumulative tick count against it. Section 3. Tested layer first, the
     .cpp supplying only the word.
Q-C  The unreachable seventh exit at FrameStats.h:2511-2515: delete it or
     make it reachable; either way the header's "six" and the code agree.
     One-line, lowest priority, listed so it is not rediscovered.
The resident assigns the next free queue numbers.

## 10. The quality ladder at close

FIRST WORKING, NOT BEST AVAILABLE, and the batch says so in its own keys:
`figurePlacementBound=NONE-YET`, `POSE_FRACTION` as the first value of a
series (import_figure.py:333-338), the inherited pad rule (section 4), the
facing sign unresolved (`GFigureShoulderAxis` prints
`facing-sign-unresolved`, VignetteShot.cpp:5087-5106, which a silhouette
does not need and a coat might). The next rungs, in order: the run and its
stills (section 2's protocol); Q-B; 372 via Q-A; then the body and clip
series, which is Jafar's feel check and not ours. No rung is blank; the
margin a silhouette needs on a wet Meridian street is a series 372 will
print, not a research task.

## 11. What the commit and the dispatch sentinel must carry

The six selftest PASS lines with their counts (frame-stats 236 or the A1
re-run's count; import_figure 70; make_base_material 170; director-cadence
82; footer-string 75; morning-brief 41), the `--measure` print of the
placement series and `figureSourceCm` (166.442 as the resident reported it,
re-printed rather than recited), `tools/workflow-size.py`'s headroom line
(the 17), and the expected shape of the new keys with their nothing-measured
forms: the figure block on the materials done line (:5227-5249), the
`figureImportStatus` line from ue-material.txt, and `figureSil` with its
four exits on every shot line. The next run's reader opens every night
still before reading any figure key (rule 4) and records section 2's three
readings per still.

## 12. Not decided here

Not whether the figure or the sky exists: Jafar ruled both. Not the pad
rule: 372, from a series. Not a camera row or a shot row: schema, and this
ruling adds none; if the stills say 77 px does not read, that is a director's
question with the stills attached. Not the 17-character margin itself:
queue 360. Not queue 370's column: it waits for the slice on Jafar's own
instruction.
