<!--RULING spawn=2026-09-17T06:46:16Z paths=ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp,tools/ue/import_figure.py,production/queue/379-the-pose-reads-zero-on-every-bone-and-the-line-says-pose-evaluated.md,production/NOW.md,game-design/decision-2026-09-16-ruling-the-refusal-was-right-and-the-still-judges-the-coat.md,game-design/decision-2026-09-17-ruling-visibility-outranks-the-silhouette-for-the-first-frame.md-->
STATUS: LOG, 2026-09-17. NOT CURRENT once the first run with kFigureXM=10.0
has landed and its camA night still has been read under section 2's
protocol; from then the run verdict and Jafar's word on the frame are the
reading copies and this file is their history.

Director ruling, 2026-09-17, on one builder's batch under queue 379: the
pose rule and the forced evaluation (VignetteShot.cpp), the occlusion term
and the moved placement (import_figure.py, kFigureXM), the done-line buffer,
and the three hand corrections the resident applied under D43.

Spawn row, quoted verbatim from `.claude/agent-log.tsv` line 715, the last
studio-director row at the time of writing:
2026-09-17T06:46:16Z	studio-director	fable	default	a65cf94a82459bdf9

HEAD reviewed: 16254d78 (`.git/refs/heads/main`), with the batch uncommitted
on top of it; `verify.py` reports `linesGated=176/556` against 100. This
spawn had no shell, so NOTHING BELOW WAS RUN: every line cited was read this
session, every printed number is quoted from the file that printed it, and
every number I re-derived says so and shows the constants it came from. The
selftest count 84/0 (was 70/0) is the resident's run as reported in the
brief, and the commit carries it again from the run that precedes it.

## 0. The verdict in one paragraph

THE BATCH LANDS, with six dictated one-line corrections (section 7), none of
which touches a mechanism, a bound or an engine call. The bound is sound and
it IS a threshold, so rule 2 applies to it and is satisfied by run 53's own
line, not by the word "resolution" (section 1). VISIBILITY OUTRANKS THE
SILHOUETTE FOR THE FRAME JAFAR GETS FIRST, and it does not need him before
the frame exists: it goes to him WITH the frame, under one sentence that
names what it is not and what the alternative costs, so the feel call stays
his (section 2). Yesterday's refusal of "move nearer" is superseded on the
measurement it lacked. RefreshBoneTransforms alone is sound, and the pair is
inside it (section 3). Both retired guards are replaced by stronger ones and
neither retirement is a ratchet (section 4). 3072 is honest headroom and the
cap still announces itself; two different counts were reported for one
literal and the commit carries the printed one (section 5). The three hand
corrections stand in substance; two of them split a sentence in half and are
moved below it, and one stated a derived number as a reading (section 6).

## 1. Question 1: the bound, and whether rule 2 is satisfied

THE PREMISE WAS REFUTED, AND THE PROOF IS ON RUN 53'S OWN LINE
(`production/d1-probe/ue-vignette-verdict.txt:256`, read this session):
`figurePoseMaxBoneDeltaCm=0.000/overBones=65` beside
`figurePoseTicks=1/8 figurePoseLatched=yes`. Under the old code the latch on
tick 1 was reachable ONLY through the strictly-positive branch (the budget
branches need ticks >= 8), so 0 < D < 0.0005 cm on a seed pose. Equality
with the bind pose is unreachable, and the check's own composition
(`PoseDeltaFromRefCm`, VignetteShot.cpp:5014-5032, `RefPoseComponentSpace`
composed here against the engine's `GetComponentSpaceTransforms()`) is why.
The resident had it wrong first and the correction is in the three
documents; the builder is right.

THE REPLACEMENT IS A THRESHOLD, AND THE BUILDER'S WORD FOR IT IS THE ONE
THING I OVERTURN. "Not a tuned threshold but the printed resolution" is a
property of the PRINT, not of the RULE: 0.0010 cm decides whether an actor
is destroyed, so it is a bound on a measurement and rule 2 is owed. It is
paid, on the evidence, in this order:
(a) Which number and which statistic: at-worst over bones (max, :5024-5030),
    last-wins over ticks (`GFigurePoseMaxDeltaCm = D` every tick, :5238,
    latched once). The line says the first (`figurePoseStat=at-worst-over-
    bones`) and `figurePoseTicks=N/8` names the tick the value is from.
(b) The bind side has ONE printed value, run 53's: under 0.0005 cm and above
    0. The bound sits at least 2x above that one reading. The 2.4e-5 cm
    floor is DERIVED (1.19e-7 relative float precision times a bone under
    200 cm from the root, :536-538), not printed; and whether the engine's
    transforms are float or double in this engine version was not opened
    here, so that figure is an upper estimate of one composition path and
    the line must not carry it as a reading. Section 7, A3 and A5.
(c) The evaluated side has NO series yet: no frame has printed a delta from
    an evaluated pose. "Tens of centimetres" (:540-541) is an expectation.
    The first run with `figurePoseEval=forced-at-build` prints the first
    value of that series at four places, and THAT reading is the evidence
    the bound waits on. If it prints under 0.0010 the finding is about the
    evaluation, not the bound: the bound does not move to make red go away.
(d) The bound is on the line beside the number with the rule stated
    (`figurePoseMovedAtCm=0.0010/...`, :5363), which is what lets a reader
    check the word against the digits.

ONE SENTENCE IN THE CODE IS FALSE AND IS CORRECTED, NOT ARGUED. :5241-5244
and :5319-5323 say the word and the digits "can never disagree". The word is
decided on the unrounded D and the digits are `%.4f`, so a D in
[0.00095, 0.00100) prints 0.0010 and the word reads bind pose. The half of
the claim that matters is true and stays: a reading that prints 0.0000 can
never carry pose-evaluated. The half-step band is 5e-5 cm wide, twice the
derived floor, and a reading landing in it IS a bind pose, so the word is
the right one and the digits round up. Section 7, A2. A one-line code fix
that decides on the rounded value exists and is refused today: it touches a
decision in a file this container cannot compile, eight points from his
ceiling, for a 5e-5 cm band. Queue item Q-D.

AND THE OLD PREMISE IS STILL IN THE FILE. VignetteShot.cpp:772-777, the
comment on `GFigurePoseMaxDeltaCm`, now reads "reads under kFigurePoseMovedCm,
which is composition noise and not exactly 0 on every bone, which is why the
test is equality and needs no measured threshold". The first clause is this
batch's and the second is the refuted premise it half-overwrote. Rule 1:
changing code changes the comments about it. Section 7, A1.

## 2. Question 2: the placement, and who decides the silhouette

THE NUMBERS, READ FROM THE FILES AND RE-DERIVED WHERE SAID. The series
(import_figure.py:473-515, `placement_series`, x from 6.0 to 32.0 by 0.5,
scored with `clear_reading` at :403-457, a 5 by 9 grid over a 0.60 by 1.70 m
box) as the C++ quotes it at :477-482: x=10.0 ratio=0.24 clear=43/45;
x=10.5 0.28 39/45; x=15.0 1.31 40/45; x=17.5 2.62 4/45. Of the 25 admissible
rows none is fully clear (:206-208; the selftest prints the count at
:1235-1238). Run 53's pixels agree with the rays: 461 of 5460 pixels in the
figure's projected box changed, 8 per cent (NOW.md:97-105, from the
before/after difference picture), against 4 of 45 rays, 9 per cent. That is
the measurement yesterday's ruling did not have. Yesterday's option (A),
"run as placed", assumed a figure at 17.5 that could be seen; it could not.
Yesterday's refusal of (B), "move nearer, which loses the silhouette by
geometry", rested on the same assumption and is SUPERSEDED on this evidence,
which is the landing-that-changes-a-conclusion this spawn exists for.

WHAT THE TWO CANDIDATES ARE, in pixels and in what is hidden. From cam_A
(x=4, z=4, eye 1.6 m, 60 degrees vertical, `vignette-scene.json:846-849` as
yesterday's section 2 read it) and the engine's own height 166.50 cm
(run 53's line):
- x=10.0: 6.00 m out; frame 2 x 6 x tan(30) = 6.93 m tall; 166.5 cm is
  173 px of 720, 24 per cent of the frame. The 2 blocked rays are the
  bottom row: the public bin at x=8 clips the near shin (:210). The x=8
  lamp head, 4.96 m up and 2 m in FRONT, is 63 degrees above the torso,
  the exact geometry constraint 1 (:178-184) refuses for a BACKlight; the
  dominant backlight is the x=18 lamp 8 m behind at 20.2 degrees (C++
  :486). Ratio 0.237: four times the lamp light from the camera's side as
  from beyond. A person under a street lamp, lit from above and in front,
  head intact, feet on the footway. NOT a silhouette, and the batch says so
  in its own key (`figurePlacementOrder=.../visibility-outranks-the-
  silhouette/queue-379`, :775-776).
- x=15.0: 11.0 m out; frame 12.70 m; 94 px, 13 per cent. Ratio 1.31,
  backlit; it is the row the C++ quotes from the eight tied at 40/45
  (:528-529), and whether it is the best of those eight is on the
  `--measure` print the commit carries, not on this page. The 5 blocked
  rays are the TOP row: the awning at x=12 hangs at 1.628 m (:208-209) and
  a ray from the eye to the crown passes x=12 at 1.6 + 0.19 x 8/11 = 1.74 m;
  the highest visible point is 1.6 + 0.028 x 11/8 = 1.64 m, so the top 15
  to 20 cm of a 166.5 cm body, crown to about the brow, is under the
  awning's edge (the spread is whether the eye's 1.6 m is above the
  carriageway or the footway, which I did not open). A dark shape against
  lit ground with its head cut by a dark edge.
So the lexicographic order is not choosing "3 rays": it is choosing a shin
behind a bin over a head under an awning, at 173 px over 94.

THE RULING. Visibility outranks the silhouette FOR THE FRAME HE GETS FIRST,
and it does not need him before that frame exists. Grounds:
(1) His operative order is the later and narrower one: "the figure still
    has not rendered", "send me the frame when a person is standing in Quay
    Street, and stop there". "A figure in silhouette" was the slice's
    description. A person 91 per cent behind a kiosk fails both sentences,
    and the first sentence is the one with a frame count on it.
(2) The candidate that honours both sentences at once, x=15, honours each
    weakly: a 1.31 ratio is a modest silhouette and a head cut at the brow
    is a weak person, at half the pixels. With eight points left, the frame
    with the highest chance of reading as a person without argument is the
    one to send, and its cost is one constant.
(3) The feel call between a lit person and a silhouette is HIS (D41,
    Meridian Test 1), and he cannot make it on a frame that does not exist.
    Ruling x=10 does not take it from him: it puts a frame in front of him
    and names the alternative in one sentence. Rule 11's card would ask him
    to choose between two placements from a description, which is the
    studio's work handed up, not his decision handed down.
(4) The order is written once, in `placement_key` (:518-536), tested both
    ways round on rows nobody measured (:1331-1347), and printed on the
    line. If he wants the silhouette the order flips to "ratio among rows
    with head and torso clear" and the answer falls out of the same series;
    that is a director's one-question spawn with HIS words and the still,
    not a builder's discretion.

WHAT GOES WITH THE FRAME, in the Producer's register (section 7, A6): that
the person is lit from the front by the lamp two metres ahead of him, not in
silhouette; that the silhouette position was measured at 4 of 45 rays and 8
per cent of its own pixels visible behind the kiosk; and that the backlit
alternative is about 94 px at x=15 with the head under the awning's edge,
one constant and one run away. Nothing else, and no question mark he has to
answer for the frame to count.

WHAT JUDGES THE FRAME, AND WHAT DOES NOT. The C++ says "figureSil on the
shot line is the instrument that judges it, on pixels" (:490-491). It is
not, yet: queue 380 (NOW.md:89-95) is figureSil printing yes on six boxes
with no figure in them, because a core-darker-than-ring test cannot ask
whether a person is there. The reader of the next run records `figureSil`
and does not decide on it. The judge is rule 4: the camA night still opened,
the before/after difference in the projected box (the method NOW.md:97-105
already used), `projH` against 173 (the engine's projection; far from it is
an instrument fault and is read first), and the pose word from section 1.

TWO OBSERVATIONS, NEITHER BLOCKING. (i) The answer sits ON MIN_CAM_DISTANCE_M
= 6.0 (:192, :548-553), a first-value bound nobody measured; at 6 m the
crown is 1.8 degrees above the axis and the feet 13.8 below, inside a field
of plus or minus 30, so the bound is not load-bearing for "in frame" and
does not move. (ii) `clear_reading` names the blocker by FIRST HIT IN LIST
ORDER (:443-446 break on the first box in `near`), not nearest along the
ray, so `worst blocker` can name the wrong box while the clear COUNT is
right; NOW.md:103 says "a crate" and the series says "kiosk:33", and neither
name is trusted until Q-E. The count is the measurement and the name is a
label.

## 3. Question 3: RefreshBoneTransforms alone

SOUND, on three grounds, two of them the builder's. (1) The asymmetry is
real: a call that is not public here produces no binary and the run measures
nothing, which reads on the verdict as NO PLAYER LOG (:5168-5170); a weak
evaluation leaves the figure standing under a word that says so and the
8-tick budget behind it, now reachable because the rule that latched on tick
1 is gone. (2) The pair is INSIDE the one call. Two secondary sources on the
engine's `RefreshBoneTransforms` (not the engine source, which this
container cannot open) describe it calling `TickAnimation(0.f, false)`
itself when the instance's update counter has never been updated, bypassing
TickPose so update-rate optimisation cannot intercept it; with a null tick
function the evaluation runs on the game thread and the transforms are
readable on the next line, which is what :5146-5150 says. Sources:
https://ikrima.dev/ue4guide/gameplay-programming/animation-subsystem/animation-subsystem/
and https://issues.unrealengine.com/issue/UE-231728 (a bug in exactly that
HasEverBeenUpdated check, which is how one knows the check exists). If that
recollection is wrong the budget is the backstop and `figurePoseTicks`
prints which tick the verdict came from. (3) Stop() stays (:5120,
:5141-5145), so the frame is one pose, not a clip playing from the top.

The one gap named yesterday stands: `GFigurePoseTicks` is never reset and
the budget is in ticks while the settle is in seconds (yesterday's section
3, Q-B). Not widened here.

## 4. Question 4: the two retired guards

(a) `place[2] > 1.0` (import_figure.py:1220-1229). What it covered: "the
chosen position is backlit". That property was deliberately WITHDRAWN by
this batch and the withdrawal is printed on the line (:775-776), so the
guard's subject no longer exists; a ratchet is loosened when the bound moves
and the claim stays. The replacements cover MORE than it did, two-armed:
accepting, "the chosen position is the most visible admissible position"
(:1302-1304) and "the best backlit of the most visible ones" (:1239-1243);
rejecting, run 53's own row (:1305-1330): admissible on the three old
constraints, best ratio of any admissible row, under a tenth of its rays
clear, STILL chosen by the ratio-only argmax, refused by the new order by
more than half the rays cast. That is 5b done properly: the old fault is
planted by the live series and the old rule is shown to still commit it.
One observation, not a fault: the check at :1230-1238 is labelled and coded
as "no admissible position is both fully clear and backlit", which is weaker
than the comment's "zero are fully clear" (:207-208); the printed detail
`fullyClear=%d of admissible=%d` carries the stronger fact, so the reader has
it. Nothing dictated.

(b) The 0.25 margin (:1265-1277). What it covered: "the top-lit fixture at
the lamp's foot scores clearly below the chosen". At chosen 0.237 and a
fixture reading of 0.15 (:1258), 0.15 < 0.237 - 0.25 is false by arithmetic,
so it WAS a property of 2.62. The replacement is two facts, both checked:
strict `<` on the ratio (passes by 0.087, the fixture's own printed pair),
and x=8 refused outright by the distance band (`not [r ... r[4]]` at :1276),
plus the standing "never chooses a position at a lamp's own foot" (:1278-
1282, more than 1.0 m from every lantern). The failure the margin guarded,
choosing under a lamp, is guarded twice. Covered.

## 5. Question 5: the buffer

HONEST. The literal at :5354-5377 renders about 1555 for an ordinary line
and a worst case near 1850 with `GFigureWhy` at its W[160] and the shoulders
string at S[160] (:5337-5340); my own tally of the value fields (two 160
strings, two asset paths, eighteen numerics) agrees to within a hundred.
3072 leaves about 1200. The cap announces itself at :5399-5407: `Need >=
sizeof(B)` appends `figureSegTruncated=yes/wantedChars=N/cap=3072` to the
std::string, outside the buffer, so the marker survives its own truncation.
The consumer at :3289-3294 concatenates std::strings into an FString with no
second fixed buffer, so there is no silent cap downstream that I can read.
Run 53 proves the 2048 fix held: all seven tail keys, `figureAtM` through
`figureScopedTo`, are on line 256 of its verdict.

ONE FAULT OF RECORD: two counts exist for one literal. The comment says
"1369 characters ... 70 ... so 1299" (:5335-5337); the brief says 1380, 70,
1310. Both claim to be measured in this container on 2026-09-17. A number
nobody printed does not enter a comment. Section 7, A4: after the literal
edit in A3 the resident prints the length once and pastes THAT into the
comment and the commit.

## 6. The three hand corrections

Queue 379 (production/queue/379-...md:14-25), NOW.md:76-88, and the
2026-09-16 ruling at :142-148 all now carry the correction with the
evidence, and the evidence is right (section 1). Upheld in substance. Three
corrections of form, dictated in section 7, A5:
- Two of the three were inserted INTO a sentence: 379's line 12 ends "DESTROY
  the actor for," and resumes at :27 "and instead it reported"; the ruling's
  :140 ends "a delta that could" and resumes at :150 "not be read". Each
  block moves to the line after the sentence it split. Not rewritten.
- 379:18 and the ruling's :145 state "order 2.4e-5 cm" as the reading. The
  reading was "under 0.0005 cm at three places, above 0"; 2.4e-5 is derived.
  One parenthesis each.
- NOW.md:103 names "a crate" as the occluder from a glance; the series
  counts 41 of 45 rays blocked and its blocker name is not yet trusted
  (section 2, observation ii). The count replaces the name.

## 7. What lands in this batch, and who does it

Everything in the brief's file list, plus these six, each a one-line fix or
dictated text the resident applies (CLAUDE.md, the studio split), none owed a
second director. No engine call, no bound, no schema, no workflow step.

A1  VignetteShot.cpp:775-777, replace the three comment lines with:
    `// kFigurePoseMovedCm, which is composition noise and not exactly`
    `// 0 on every bone (queue 379: the old equality test was unreachable`
    `// and latched on the noise). -1 means nothing was read at all.`
A2  VignetteShot.cpp:5242-5244, replace "so the word here and the digits on
    the line can never disagree: anything that prints as 0.0000 fails this
    test" with "so anything that prints as 0.0000 fails this test; the one
    band where word and digits differ is the half-step under the bound,
    0.00095..0.00099, which prints 0.0010 and IS a bind pose". Same
    sentence, once, at :5321-5323 ("so a reader can apply the rule to the
    digits and get the word beside them" gains "except in the half-step
    under the bound, where the digits round up and the word is right").
A3  VignetteShot.cpp:5364, the literal `/noise-floor-is-2.4e-5-cm/` becomes
    `/derived-floor-2.4e-5-cm/run-53-bind-pose-printed-under-0.0005/`. No
    spaces; one value.
A4  After A3: print the literal's length once (a python one-liner over the
    file, extracting :5354-5377), and write the three numbers it gives
    (literal, specifier characters, fixed characters) into :5335-5337 in
    place of 1369/70/1299, and into the commit message. Neither 1369 nor
    1380 is copied anywhere.
A5  The three documents: move 379's block :14-25 to after :27, and the
    2026-09-16 ruling's block :142-148 to after :154; in 379:18 and the
    ruling's :145, "order 2.4e-5 cm" becomes "under 0.0005 cm as printed,
    the derived floor being 2.4e-5"; NOW.md:103 "almost entirely occluded
    by a crate" becomes "almost entirely occluded (41 of 45 sample rays
    blocked on the series; the blocker's name is a list-order label until
    Q-E)". Documents; commit on the resident's read.
A6  The Producer's sentence with the frame, dictated in section 2 ("what
    goes with the frame"), carried in `.claude/agents/producer.md`'s register
    and cap, with the required link to the still. It states, it does not ask.

The selftest is re-run because the commit runs it anyway; A1 to A3 touch a
file the selftest reads constants from (`_cpp_const`, :1356-1359) and none of
them touches a constant.

## 8. Queue items opened by this ruling (named, not done: rule 11)

Q-D  Decide the pose word on the digits that print: compare the value
     rounded to four places, so the half-step band closes. One line, in the
     .cpp, after a run has proved the forced evaluation compiles. Lowest
     priority; section 1.
Q-E  `clear_reading` names the blocker by list order, not by the nearest
     hit along the ray (:443-446). Return the hit with the smallest ray
     parameter. The count is unaffected. One function; section 2.
Q-F  THE SILHOUETTE POSITION, WAITING ON JAFAR'S WORD AND NOT ON OURS: if
     the frame at x=10 is not what he wants, `placement_key` flips to the
     ratio among rows with head and torso clear, the answer falls out of the
     same series (x=15 on the C++'s own quote, about 94 px, crown under the
     awning), and the lever above that is a night camera row or a longer
     lens, which is schema. Comes back to a director with his words and the
     still attached.
The resident assigns the next free queue numbers; Q-B and Q-C from
yesterday's ruling stand.

## 9. The quality ladder at close

FIRST WORKING, NOT BEST AVAILABLE, and the batch says so on its line
(`figurePlacementBound=NONE-YET`, the order key naming queue 379, the pose
delta's evaluated side unmeasured). The next rungs, in order: the run and its
camA night still under section 2's protocol; Jafar's word on lit versus
silhouette (Q-F); 380, an instrument that can tell a figure from a doorway,
which the before/after difference already is by hand; Q-B, the per-shot pose
word; then the body and clip series, his feel check and not ours. No rung is
blank.

## 10. What the commit and the next run's reader must carry

The commit: `import_figure --selftest: 84 check(s), 0 failure(s)` re-printed
after A1 to A3; the `--measure` series whole, with the x=10.0, 15.0 and 17.5
rows quoted; A4's three printed numbers; and this file's path. The next run's
reader opens the camA night still BEFORE any figure key (rule 4), then reads:
`figure=` and `figureWhy=` (STANDING/pose-evaluated is the accepting case,
DESTROYED/bind-pose the rejecting one, and either is an honest ending);
`figurePoseMaxBoneDeltaCm` at four places as the first value of the evaluated
series against `figurePoseMovedAtCm=0.0010`; `figurePoseTicks=N/8`; `projH`
against 173; the before/after difference in the projected box;
`figureSegTruncated` absent; and `figureSil` recorded, not decided on (380).
Then the frame goes to Jafar with A6's sentence, and the studio stops there.

## 11. Not decided here

Not whether the figure exists: Jafar ruled it. Not lit versus silhouette as
a matter of taste: his, on the frame, Q-F. Not a camera row, a shot row or
a lens: schema, and this ruling adds none. Not the pad rule (372) or the
per-shot pose word (Q-B). Not queue 380's fix: it is named as the reason
figureSil does not judge this frame, and it is not started in this batch.
