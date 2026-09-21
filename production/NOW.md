# NOW: what is in flight (read this FIRST, before the queue)

STATUS: LIVE. Verified 2026-09-21 16:2xZ, after run 56 landed: the card is out of the hero frame and the figure stands alone in it.

A session that resets loses everything not written down. The queue says what
to do NEXT; this file says what is ALREADY MOVING, which is the thing a fresh
session would otherwise duplicate, abandon, or wait for forever.

Keep it current or delete it. A stale NOW is worse than none, because it
looks like a live state.

## 2026-09-21 12:2xZ THE RESET, HIS ORDER FOR THE WEEK, AND WHAT IS MOVING

THE METER IS READ AND THE STUDIO IS UNLOCKED. His message, arriving between
11:19Z and 12:10Z: total 0, Fable 0, ceiling 85 on the higher meter, standing.
Row 2026-09-21 in `production/budget.md`. The four-day hold ends with it. The
session model was switched to Fable with the same message, so the resident's
own turns now spend the Fable meter.

HIS ORDER IS ON DISK VERBATIM, 3,529 words, at
`game-design/decision-2026-09-21-the-week-after-the-reset-five-measurements-and-eleven-rulings.md`.
Read that before anything here. Its shape, so a cold session has it in one
screen: research is finished; six unknowns remain and all are measurements;
this week takes five. The order of the week, which nothing below reconciles
because he ordered it so nothing would have to be:

1. THE VISUAL SLICE, the spine, runner first: (1) D18 in the animation
   library, fifteen minutes; (2) the exposure fault, queue 384, with the
   determinism check extended to the night shots in the same batch; then the
   figure; (3) the first authored building facade as the week's measured
   batch, behind queue 370's column and the throughput ledger's new unit.
2. THE MEASUREMENTS, in parallel, behind the slice on the runner: the
   small-model test; the MESH station's first run; the scale soak at 50 then
   200 (queue 351 with 116 folded in, runs in the container); the frame
   instrument, riding the slice's own dispatches.
3. THE ART LANE behind both: six character concept sheets.
4. Eleven rulings, D47 to D57, recorded as they go; cheap; not the week's work.
5. Cleanups, two cards, one check: the studio's third, at checkpoints.
6. If budget remains, queue 250. Then the filed audit and red-team items.
Cut from the bottom, never from the slice.

WHAT IS MOVING AT THIS WRITING: nothing yet. The first commit is the reading,
his text, and this section, so that a session that dies in the next hour
opens on his order and not on a cold read. The builders are spawned in the
turn after it and their spawn rows are in `.claude/agent-log.tsv`; a later
edit of this section names them.

RUN 56 LANDED AT d3529180 AND THE HERO FRAME IS CLEAR. Ancestry confirmed:
the commit contains the dispatch 39aa6432. THE RESIDENT OPENED BOTH FRAMES.

WHAT THE HERO FRAME SHOWS, `ue-vign_camA_night.png`: a wet street, brick left,
dark tiled wall right, a lit lamp, fog, and A WOMAN STANDING ON THE FOOTWAY,
fully visible, nothing in front of her. The four-quadrant card is GONE.
`quadOn=cam_B/1280x720`, `quadCornersInFrame=4/4`, and `controlQuadHiddenOn`
begins `vign_camA_day;vign_camA_night`, so the two hero shots hide them.

THE VERDICT HEADER NO LONGER LIES. It reads "in front of the control camera
(cam_B, ruled 2026-09-21)". Until run 55 it printed "in front of the first
shot's camera" into EVERY verdict, months after that stopped being true.

THE GUARD HELD AND IT WAS MEASURED, NOT EYEBALLED, which was a condition of
the cam_B ruling. Three named boxes 51 px square on the three printed centres
of `ue-vign_hook_day.png` (537/391, 532/392, 528/393): mean RGB about
(186, 188, 191), CHROMATIC PIXELS 0 OF 2601 in each, max channel spread 7
against the roughly 255 a quad texel would give. No square, on the camera the
sheet is judged from.

THE DONE LINE CAME BACK EXACTLY AS PREDICTED and nothing was repaired to do it:
`materialsStatus=ALL surfacesAsked=14 surfacesResolved=12/14 surfacesAbsent=none
surfacesAbsentCount=0/14 surfacesProcedural=2/14 mapsFound=36/36`, with
`piecesPainted=600/610` and `piecesUnpainted=10/610` UNCHANGED, which is the
key that proves it was a recount. `surfacePopulationCut` did not bite.

ONE FALSIFIER FIRED AND IT IS A REAL FINDING, NOT A FLUKE.
`rigRepeatsWithinBound=1/of=2`, worst 0.22977 on `vign_camA_night`, against run
55's 0.00061. The DAY repeat is fine at -0.0002. The night one went 0.3238 to
0.0940. THE CAUSE IS IN THE SHOT'S OWN SETTLE SERIES:
`0.14473..0.11980..0.11392..0.32375`, CAP-BIT at 4 of 4. Takes 1 to 3 converge
to within 0.0009 of the bound, then take four jumps to 0.32375, and the rule
commits THE LAST TAKE. So the committed hero frame is the outlier, at nearly
three times the brightness the shot was converging on, which is why it reads as
dusk rather than night. Filed as queue 413.

WHY THAT SHOT CAP-BIT WHEN IT SETTLED IN RUN 55 IS A QUESTION, NOT AN ANSWER.
The only change to that frame is that its three control quads, bright patches
the auto-exposure was metering, moved to cam_B. NOTHING HAS MEASURED THAT and
two hypotheses about this exact frame have already been refuted this month.

THE LEGS ARE STILL YELLOW AND NO PICTURE CAN SETTLE WHY. The resident measured
the leg region: hue spread 33.8 degrees, against the road's 32.1 and the brick
wall's 15.9, and the wall is certainly textured. So the frame is consistent
with BOTH a bound texture and a flat material under varied light, and settles
neither. That is exactly why queue 411 asks for `figureTexturesBound=n/N`
rather than for another look.

RUN 55 LANDED 13:55Z AT 2490b864 AND THE NIGHT EXPOSURE FAULT IS CLOSED.
Ancestry confirmed, not assumed: the landed commit's subject names the dispatch
sha 4421af2b and `git merge-base --is-ancestor` agrees. Queue 384 is LANDED.

WHAT PROVES IT IS THE RIG REPEAT, NOT THE CONTROL.
`rigRepeatsShots=vign_camA_day/day..vign_camA_night/night`, so a NIGHT shot is
repeated and the week-old blind spot is closed. `rigRepeatsWithinBound=2/of=2`
at a worst of 0.00061 on `vign_camA_night`: the same night camera photographed
at opposite ends of the run now agrees to six ten-thousandths, against a 0.20
to 0.46 band before. `settleSettled=45/of=49`, `settleNoFile=0/of=49`.

THE ACCEPTANCE THE RESIDENT WROTE INTO THE DISPATCH WAS THE WRONG TEST and is
corrected rather than dropped. It asked for the twelve control deltas to
collapse under 0.005; they read 0 OF 12. That is not the fix failing. The
control's two halves no longer get the same treatment: `AfterFrame`'s
`if (GRepeating)` branch settles, the `if (GProbing)` branch does not, so a
control now differences a SETTLED frame against an UNSETTLED one. The probe
half is itself unstable, moving more than 0.005 on 4 of 12 shots between runs
and flipping between the recurring values 0.00639 and 0.46178, which is a clamp
signature. Filed as queue 410.

FOUR NIGHT SHOTS HIT THE CAP, and two of them are BISTABLE rather than slow
(0.00637..0.18295..0.00637..0.19985). No cap size fixes those. The instrument
marks all four CAP-BIT and says they may not be compared to another frame.

THE FRAME EXISTS AND IT IS SPOILED BY AN OLDER FAULT. The resident OPENED
`ue-vign_camA_night.png` rather than reading a key: wet road, brick left, dark
tiled wall right, lamps lit, fog, and A FIGURE STANDING ON THE FOOTWAY. But a
FOUR-QUADRANT COLOUR CARD sits across the figure's torso and its legs render
flat yellow. `surfacesAbsent=card/interior/multiply/paint_yellow`,
`surfacesResolved=12/16`, IDENTICAL to runs 53 and 54. The card IS the
unresolved `card` surface; the yellow IS `paint_yellow`.

CORRECTED 2026-09-21 14:4xZ UNDER D43, AND THE CORRECTION IS THE RESIDENT'S OWN
ERROR. The two sentences above are FALSE and are left visible because a
deleted claim cannot be audited.

THE COLOUR CARD IS NOT THE `card` SURFACE. It is queue 123's COLOUR CONTROL
QUAD, an instrument deliberately placed, and run 55's own verdict says so:
`controlQuad=colour`,
`controlQuadColours=texel0.red.255.0.0/texel1.green.0.255.0/texel2.blue.0.0.255/texel3.yellow.255.255.0`,
`controlQuadHidden=47/49`,
`controlQuadVisibility=hidden-for-every-shot-whose-camera-is-not-the-one-they-were-placed-from`,
`controlQuadsRule=the-colour-quad-answers-the-texture-path/the-two-tile-quads-answer-the-scalar-path`.
It sits 3.51 m from cam_A and is visible on exactly the two shots whose camera
IS cam_A, one of which is the hero night frame. It is proof that a texture
override reaches the sampler, standing in front of the figure.

AND `card` IS PAINTED, not absent: `paintRoutes=pack.580/tint.10/decal-card.10/
decal-multiply.0` with `piecesPainted=600/610`. The 10 unpainted are
`decal-needs-a-stain-material.10` and they are FAIL-CLOSED rather than pasted,
`decalQuadsHidden=10/20`, on the recorded reasoning that pasting the grime
opaque would make the count green and the picture worse.

THE YELLOW LEGS ARE NOT `paint_yellow` EITHER. paint_yellow is ROAD PAINT and
it IS rendering: the yellow kerb line along the footway. THE PROJECT ALREADY
KNEW THIS AND THE RESIDENT CONTRADICTED ITS OWN RECORD WITHOUT READING IT:
`production/queue/226-*.md:38` and `production/NOW.md:3018` both say
paint_yellow is ProceduralOnly by design. The figure's legs are the FIGURE'S
OWN material, which nothing measures: the run prints `figureImportStatus=
IMPORTED` and no figure TEXTURE key at all. So the legs are UNANSWERABLE today
rather than answered, and that is a new item.

AND THAT PARAGRAPH WAS ITSELF WRONG WHEN FIRST WRITTEN, corrected by the
director within the hour and re-measured by the resident before this edit. It
said "ZERO figure material or texture keys, while Michelle.fbx carries four
embedded textures in a .fbm folder". THREE FALSEHOODS IN ONE CLAUSE:
`production/d1-probe/ue-build.txt` prints `figureMaterials=1` and
`figureImportVia=AssetImportTask/made=7`, so there is a material key and it is
not zero; NO `.fbm` DIRECTORY EXISTS ANYWHERE IN THE TREE (`find` returns
nothing, and `ledger/Assets/Characters/` holds one file, Michelle.fbx at
20,974,352 bytes); and the number four is printed nowhere, with no
`figureTexture*` key existing at all.

THE RESIDENT REPEATED A BUILDER'S DETAIL WITHOUT CHECKING IT, INSIDE A
CORRECTION ABOUT NOT DOING THAT. That is the finding worth more than the fact.
What IS true and is the whole of it: the figure imports with one material, and
NOTHING MEASURES WHETHER ANY TEXTURE BOUND TO IT. The item wants
`figureTexturesEmbedded=N` measured off the FBX rather than typed, beside
`figureTexturesBound=n/N`, both arms watched.

THE REAL SURFACE FIGURE IS ZERO MISSING, NOT FOUR. `surfacesAsked=16` counts
distinct NAMES, and the done line called every non-resolved row absent. Run
55's own per-surface lines classify all sixteen: 12 RESOLVED, 2 PROCEDURAL by
design (interior, paint_yellow), 2 DECAL BLEND MODES that are not surfaces
(card, multiply). Fourteen library surfaces asked, twelve resolve, zero
genuinely unresolved.

HOW THE ERROR WAS MADE, because it is the useful half: the resident OPENED the
frame, which was right, saw a colour card and yellow, and reached for the
nearest key that carried those two words. `surfacesAbsent=card/.../paint_yellow`
matched the picture and the resident stopped there. CLAUDE.md rule 4 says
looking is strong evidence that something is wrong and WEAK EVIDENCE OF WHAT OR
WHY, and that the quantity is printed before acting. The quantity here was
`controlQuad=` and `paintRoutes=`, both on the same page, and neither was read.
 THAT IS QUEUE 223,
READY since 2026-09-09 and never started, and it is now the ONLY thing between
Jafar and a judgeable figure frame. An engine-specialist is on it as of 14:1xZ,
briefed to check queue 227's denominator question BEFORE fixing anything and
to leave the exposure path alone.

THE HOURLY TRIGGER IS HEALTHY AND WAS NOT AT FAULT, checked against the
scheduler rather than guessed: `trig_017Ho772fH6Uuysbith7b3CU`, cron `3 * * * *`,
enabled, bound to this session, last run SUCCEEDED. It fires LATE because it
delivers into a persistent session that was mid-turn: the 13:03 slot arrived at
13:18, and at 14:12 the 14:03 slot had not yet been delivered. Nothing in the
configuration is wrong and there is nothing here to fix.

FIRST WAVE, 12:35Z TO 13:0xZ: SIX BUILDERS OUT, TWO BACK, NOTHING COMMITTED.
The tree holds live builder work and `ledger/.verify-footer` is DELETED, so no
commit is possible until it is quiet and green. Back and verified against the
tree by the resident:

- D18 IN THE ANIMATION LIBRARY (slice item 1) IS DONE IN THE TREE. 71 clip
  files examined, 5 touched alcohol or tobacco, GAMBLING 0 OF 71. Removed: the
  drinking clip, the bartending clip, the rejected sitting-drinking clip.
  Renamed `sit_drink` to `sit_wait`. `drink` is DELETED not renamed, because of
  1,547 distinct catalogue names zero contain tea, cup, mug, sip or coffee, so
  a renamed slot would have no candidate but the clip the rule forbids. The
  smoking clip STAYS REJECTED and the reason is measured, not assumed: it was
  never a content screen, it was `motion_ok`, hips travelling 0.68 m against a
  0.50 m bound for a standing slot. The `smoke` slot is kept live and
  `NpcWalker` now asks for it at the doorway that used to ask for `drink`, so a
  re-pick from the harvest lights it up with no further wiring.
  `tools/content-gate.py` gains SITE 6, walking the library by clip name AND
  slot name, both, because a title-only check passes `sit_drink__Sitting` and a
  slot-only check passes `work_counter__Bartending` and BOTH OF THOSE SHIPPED.
  Selftest 102 ok from 88, accepting case first. It runs in verify and the line
  that proves it is `ledger/verify.py:1829`, which fails the run if the done
  line carries no `clipsExamined=`, read and confirmed by the resident.
- THE WEEK'S QUEUE IS FILED, 389 to 403, fifteen items. `queue-check` PASSES
  at 391 items, 197 ready, 10 blocked, 11 done. The facade (389) is BLOCKED on
  370, on 403 and on the grime rule's D-record, none of which has landed.

APPLIED BY THE RESIDENT UNDER D43, NOT RULED: canon.md and D18 both said the
content rule is "enforced at five sites" and the animation library is a sixth.
Both now say six and both name why the sixth exists: the five earlier sites all
read TEXT, and a clip is a file name. This changes a COUNT and no rule, which
is what D43 covers; it is reported to him in the next brief rather than ruled.

THREE OPEN THREADS THE RESIDENT OWNS, none of them a builder's to take:
1. `director_cadence` is RED and it is not a fault: "DIRECTOR RAN BUT DID NOT
   RULE", `rulingRowsUnruled=1/1 rulingUnruledNewest=2026-09-21T12:38:32Z`.
   That is the studio-director spawned at 12:38:32Z, still writing D47 onward.
   ITS STAMPED RULING IS WHAT CLEARS THE COMMIT, so the batch waits on it.
2. `game-design/sim-shots/clips.tsv` still carries `drink`, `sit_drink` and
   `work_counter`, and the committed `clips.jpg` beside it RENDERS THE TWO
   REMOVED CLIPS AS TILES. Both are CI evidence written by the sim run, not
   inputs: `ClipSheet.cs` writes the tsv from the file names and
   `tools/sim-shots-commit.sh` commits the pair together, so hand-editing one
   would relabel tiles in the other. THE FIX IS TO FOLD `clips=1` INTO THE NEXT
   UE-PROBE DISPATCH, which is coming anyway for the exposure fix, per ci.md's
   rule that changes batch per dispatch.
3. Two C# edits (`CharacterPrefab.cs`, `NpcWalker.cs`) cannot be proved here:
   the Game layer compiles locally but a Unity API error is invisible until CI.
   The keys that answer it on the next run are `CharacterAudit importerRan/clips`
   (expect 41, was 44) and the ClipSheet slot count (expect 62, was 64).

HIS SECOND MESSAGE OF THE SAME DAY, about 12:3xZ, RULES THE CRIME AND COMBAT
AUDIT and is on disk verbatim at
`game-design/decision-2026-09-21-the-crime-and-combat-audit-ruled-eight-verbs-and-the-endings-hold.md`.
NONE OF IT IS BUILT THIS WEEK, in his words: it is stage 3 and waits behind
the slice and the measurements. Eight verbs are ruled in, the press in but
only through a person, grassing in, three combat gaps in, and the five endings
HOLD with no redemption path added. TWO THINGS ARE CHECKPOINT WORK NOW and
only two: confirm the two hunted-player endings are reachable from a hunted
state (a card to him if either is not), and correct the endings' pub wording
to the minicab office under D19 and D43. The delivery is on
`research/crime-and-combat-coverage`, which EXISTS: confirmed by
`git ls-remote --heads origin`, one of 48 research branches among
52 heads on the remote, 0 of them merged to main, which is what the consolidation cleanup is for.

A CORRECTION TO HOW THIS CHECKOUT WAS READ ON FRIDAY, applied here under D43.
Queue 387 recorded that the meridian-test-administration delivery was not in
this checkout, measured over main's tracked files, and that reading stands.
What was NOT known then is that the branch exists: a single-branch
`git fetch origin main` had left `git branch -r` showing 9 branches, and a
full fetch at 12:3xZ shows 52, among them
`origin/research/meridian-test-administration`. The delivery is not missing,
it is unmerged, which is a different fault with a different fix.

STANDING SINCE 2026-09-17 AND UNCHANGED: one brief a day with the frame in
it, the reading asked as its first line; cards only when the studio cannot
decide, beyond the two he asked for. Work until the ceiling or a limit; arm
the resume on either.

## 2026-09-19 TO 2026-09-20: A HELD STUDIO, ONE DICTATED DOCUMENT, AND A METER THREE DAYS OLD

NOTHING WAS STARTED AND THAT IS THE ORDER BEING KEPT, not a stall. His
standing instruction since 2026-09-17, given five times, is that nothing filed
starts before the reset. No builder ran, no run was dispatched, nothing
rendered. Queue 384, the night exposure race, stays first in his order and
unstarted; the figure stays behind it.

THE ONE THING THAT LANDED IS HIS OWN TEXT. On 2026-09-19 he dictated the
friends playtest runbook and authorised the write over the ceiling himself, as
documentation that spends almost nothing, wanting it on disk before Monday. It
is at `production/playtest/RUNBOOK.md`, verbatim: 19 lines, 342 words, his
punctuation, no em-dash, no italic. "It is mine, not yours to rewrite." No
agent and no director touched it. Queue 387 sits beside it, LANDED for the
runbook and NOT started for the rest. Commit 42babfd1.

THE EVIDENCE HE NAMED FOR IT IS NOT HERE. He called the research lane's
meridian-test-administration delivery its evidence. `git grep -il` found 0 hits
over 5994 tracked files before 387 was staged, and a whole-tree pass over 6545
files found exactly 1, queue 387 itself. So a later reader who greps and finds
one hit has found the note; two means the delivery landed. The runbook stands
on his authorship alone until then.

THE CHANNEL ASKED HIM FOR THE METER AND HE HAS NOT ANSWERED. At 2026-09-20
01:13:40Z the bot on his PC restarted and sent its two chrome messages,
receipts 120 and 121, identified by length rather than guessed: 236 chars is
OPENING exactly, and 224 is BUDGET_Q formatted with NUMERIC_PLACEHOLDER
(198 - 2 + 28). Zero inbound messages came with them; the pc-inbox commit says
so in its own subject. Commit bd426c23.

THE METER IS THE WHOLE BLOCKER. Newest row 2026-09-17c, takenAt
2026-09-17T07:24:56Z, 78 total and 77 Fable against the ceiling of 85. That is
about sixty nine hours old at this writing, far past the ten hour rule, so the
day is unmeasured and the studio is inbox only: no builders, no dispatches, no
renders. Three morning briefs have now asked for the reading. The tap streak
is 1 of 7 consecutive readable, last tapped 2026-09-16.

## 2026-09-17 13:1xZ HIS RULING ON THE PAIR: THE DEFERRAL IS OVER, FACADES ARE THE BLOCKER, EXPOSURE COMES FIRST

HE LOOKED AT THE COMPARISON AND RULED. Recorded in full as D28 Amendment A1;
the parts that change what happens next:

1. D28's deferral of geometry and unique buildings is LIFTED, by him. "Presentation
   is now good enough that geometry and facades are the blocker." What landed he
   names as real: wet road, grade, overcast light, materials at close range.
   What is missing he names as buildings with faces, shopfronts, windows, doors,
   signage, roofs, chimneys, and two hundred metres of depth. "Ours is a corridor
   of blank walls with fog at thirty metres doing double duty as sky and as a
   cover for there being nothing beyond."
2. THE NIGHT EXPOSURE FAULT COMES BEFORE THE FIGURE. His reason: "a figure
   cannot be judged in a frame whose exposure is random." Queue 384 is therefore
   ahead of the figure fix, and D44's studio discretion does not apply to it.
3. "Nothing starts before the reset." Unchanged, fourth and fifth time.
4. A QUESTION ANSWERED IN THE SAME RUN, per rule 13: what a single authored
   building facade costs, end to end. THE ANSWER IS THAT IT CANNOT BE MEASURED,
   and the three facts are these, each checked rather than recalled. No facade
   has ever been authored here: 39 GLBs exist in the tree and the nearest four
   to a building are a fascia cornice, a console bracket and two chimney pots,
   with no wall, window, door, shopfront or roof among them. production/throughput.md
   prices the IMPORT of a piece, zero sessions and about 0.35 minutes of runner
   time marginal, and says in its own words that it does not price the MAKING.
   And the spawn log cannot attribute a window of spend to one item, which is
   queue 370. What would produce it is his own batch rule of 2026-09-16 pointed
   at facades instead of props, with a clean window and the spawn-log column in
   place BEFORE it opens.

ITEM 1 OF D28's OWN LIST WAS NEVER CLOSED and nobody had noticed until his
ordering made it matter: "Fix the exposure fault so the same camera and
conditions give the same picture" is step one of the visual slice, still open,
now measured. That is the same thing as his ordering, arrived at from the other
end.

## 2026-09-17 12:2xZ CLOSE: THE COMPARISON IS DELIVERED. THE NIGHT CAPTURE IS THE BLOCKER, AND IT IS THE RIG, NOT THE STREET

HIS LAST INSTRUCTION, and it is the one that governs Monday: "Spend them on
one thing: the street rendered from the Hook sheet's viewpoint, put beside the
sheet, with your plain judgement of how far apart they are and what accounts
for it. Without the figure if the figure is not ready. That comparison is what
the whole week was for and it has never been made. Then stop. The figure fix
waits for the reset." Before that, four times: "Nothing filed starts before the
reset."

DO NOT RESUME BY DISPATCHING A RUN. Read the two paragraphs below first.

THE COMPARISON IS MADE AND IS NOW IN HIS HAND.
game-design/sim-shots/hook_sheet_vs_street_2026-09-17.jpg puts the lower panel
of OUR OWN sheet (production/art/compare/hook-2026-09-09-pass2/hook_pass2.png)
beside the built street at the same viewpoint, one scale, neither cropped to
flatter the other. THE JUDGEMENT: the gap is DRESSING, not people. Our sheet
has one walker and a parked car, so the first judgement, which said the gap was
inhabitation at nine or ten people, was wrong and was made against the OUTSIDE
sheet that ladder rung 1 had already retired. He caught that himself. The hard
half is good: brickwork, kerb, channel and gully, pavement, fog depth, camera
feel. What is missing is shopfronts, windows, colour and weather, which is
queue 195 showing up visually.

IT TOOK TWO SENDS AND THE SECOND ONE IS THE MECHANISM TO REMEMBER.
tools/runner/outbox.py sweep SKIPS ANY FILE WHOSE RECEIPT ALREADY EXISTS
(executor.py:421). Rewriting a message in place after it has sent makes it
unsendable for ever. The corrected body went out under a NEW STEM,
production/outbox/2026-09-17-the-right-sheet.answer.md, at 66101ede. Also: his
PC sent the first one from a stale checkout, so the correction that was already
on the remote did not go. That is queue 382 and 383, both filed.

THE BLOCKER, AND IT MOVED TODAY. Queue 384. The night frame is black, and as of
12:2xZ the cause is NOT the figure, NOT the materials, NOT a leaked exposure
pin and NOT the lights. Run 54's twelve control lines say the NIGHT CAPTURE
LANDS AT AN ARBITRARY EXPOSURE: a control photographs its own shot twice with
nothing toggled, and ten of twelve disagree with themselves by 0.20 to 0.46 of
whole-frame mean luma, three of them in the BRIGHT direction. The same camera
photographs the same street with the same figure at 0.46449 on one shot and
0.00637 on another. The figure reads exactly as bright as whatever the frame
landed at, monotonically, across all eleven shots that carry a figure record.
The rig's own determinism check never saw this because it photographs a DAY
frame (rigRepeatOf=vign_camA_day, rigMeanLumaDelta=-0.0017). The full reading,
with denominators, is at the foot of queue 384; the figure-at-6.00m hypothesis
that item named as the first thing to test is WITHDRAWN there.

WHAT THAT MEANS FOR EVERY NIGHT STILL ALREADY COMMITTED: on these numbers they
are not comparable to each other, and no night-to-night brightness claim made
this week should be trusted until the capture converges. Nothing has been
changed on that account; it is written here so it is not re-derived.

WHAT IS DONE AND NEEDS NO REDOING: the figure imports, spawns, and poses (87.0230 cm
of bone movement against a 0.0010 bound, latched on the first tick); it stands
in Quay Street at the measured place and size (projH 175.65 against 173
predicted); the day frames are stable. Runs 52, 53 and 54 are spent: 52 died on
one include, 53 gave a T-pose behind a kiosk, 54 posed correctly into a black
frame.

FILED TODAY, NONE STARTED, per his order: 372 to 384. The cost items (369, 370,
371), the red team (364 to 367) and the rest wait for the reset.

## 2026-09-16 CLOSE: JAFAR STOPPED THIS THREAD. TOMORROW IS THE VISUAL SLICE ONLY

HIS WORDS: "Land the policy batch when the director rules on what leaves
CLAUDE.md, and nothing else from this thread afterwards. Today produced no
game work at all and the two-thirds rule is judged weekly. Tomorrow is the
visual slice and nothing else: wetness, materials, then dusk with lamps lit
and a figure in silhouette, ungated under D41. If another enforcement finding
turns up, file it and keep going."

  THE JUDGEMENT IS ACCURATE AND IS NOT ARGUED WITH HERE. 25 spawns today: 11
  instrument-builder, 5 studio-director, 3 engine-specialist, 2
  systems-builder, 2 artifact-reader, 1 producer, 1 claim-auditor. The nearest
  thing to game work was the caught-claim fix in Core, which repaired a bug in
  pillar 1 rather than building anything. NO FRAME MOVED. The visual slice
  gained a material parameter defaulting to black and a written map, and the
  lamp is still dark.

  WHAT THE DAY ACTUALLY BOUGHT, so the ledger is honest in both directions:
  five false or narrowed enforcement claims found and a policy ruled over
  them, the caught-claim fix, the null floor back on the day frames, canon
  reconciled with three rulings, and fourteen queue items filed. All of it is
  the project working on itself, which is the thing the two-thirds rule
  exists to bound, and he is judging it weekly rather than daily.

  THE DIRECTOR HAS RULED, 2026-09-16 12:0xZ, addendum 1.3b of
  game-design/decision-2026-09-16-ruling-wire-or-delete-the-last-instrument-and-seven-settlements.md.
  THE BOUND DOES NOT MOVE: it is one of the six cleanly true enforcement
  claims, so raising it inside the batch that exists to make enforcement
  claims true would be the batch refuting itself. Eleven dictated edits A to
  K moved the enforcement DETAIL to the constitution, operations.md,
  organization.md, .claude/rules/ci.md and the legacy index, and struck the
  runner recital from every sentence because proving a runner is the check's
  job, not a sentence's.

  APPLIED BY THE RESIDENT, A TO J PLUS THE RESERVE: CLAUDE.md prints
  1920/2000 after A to J and about 1951 after the reserve was taken for
  Jafar's new standing rule. K lands WITH the enforcement-claims check,
  because it names a tool that has no runner until then. One miss was caught
  and fixed in the same pass: edit G deleted its passage from CLAUDE.md
  without adding it to organization.md, so for one edit the text existed
  nowhere.

## 2026-09-16 20:0xZ CLOSE: RUN 53 PUT A FIGURE IN QUAY STREET AND IT IS A T-POSE BEHIND A CRATE

READ THIS FIRST ON MONDAY. The figure LANDED, and three of the four things
that had to work did. What did not work is legible and filed, so this opens on
the figure and not on a cold read.

**WHAT WORKED, all read off the landed verdict at `4696d113` (probe from
`61e46c4e`), not predicted.** The build succeeded. `figure=STANDING`,
`figureBones=65`, `figureMeshHeightCm=166.50` against the 166.442 measured off
Michelle's own FBX in this container, so the UNIT CONFUSION IS RULED OUT and
the import is right. `figureScale=1/never-scaled`. `figureAtM=x.17.50/y.0.125/
z.4.00` and `figureFootGapCm=0.000`, so it stands on the kerb where the search
put it. `figureScopedTo=lanterns-on-only` held and `figureShownShots=12/
hidden=37`.

**THE BUFFER FIX HELD.** All seven keys that `char B[900]` was eating are
present, and `figureSegTruncated` is absent, so 2048 carries the line. Without
the audit that found it, this run would have returned green with the entire
placement readback missing and nobody would have known the keys existed.

**WHAT DID NOT WORK, AND IT IS TWO SEPARATE FAULTS.**

- **Queue 379, the pose.** `figurePoseMaxBoneDeltaCm=0.000/overBones=65` beside
  `figureWhy=pose-evaluated`. Those cannot both be true: the test needs no
  threshold precisely because a figure that never evaluated reads delta exactly
  0 on every bone. It read 0.000 on all 65 AND THAT WAS A ROUNDED POSITIVE,
  not a zero: `figurePoseTicks=1/8` and `figurePoseLatched=yes` sit on the same
  line, and the old rule latched only on a strictly positive delta. The figure
  IS in its bind pose, for a different reason (the check ran before the world
  ticked the component, so it read the seed), and the premise that equality with
  the bind pose is exact is retired. Corrected 2026-09-17. So the figure is a
  T-POSE, and
  the destroy decision that exists for that case did not fire. The
  engine-specialist predicted this exact failure at 0.8 confidence before the
  run; what happened is that fault with the opposite ending.
- **Queue 380, the silhouette reads yes on an empty box.** Six `settle_night`
  shots reported `figureSil1=figure_michelle/yes`. THE BOX WAS OPENED AND THERE
  IS NO FIGURE IN IT: a shopfront doorway, railings, crates. The projection was
  checked independently and is CORRECT (14.8 m, 13.3 degrees right of the
  cam_hook axis, x about 905, about 114 px against the reported box=x827..936
  and projH=120.80). Darkness is not evidence of a person and a core-versus-
  ring test has no way to ask whether one is there.

**THE ONE PLACE IT IS VISIBLE, measured rather than glanced at.** On
`ue-vign_camA_night`, the figure's own box differs from run 51's same rectangle
in 461 of 5460 pixels by more than 2/255, largest channel difference 168. The
before/after/difference picture is
`game-design/sim-shots/figure_run53_camA_before_after.png` and it shows a
NARROW VERTICAL SLIVER where run 51 had bright sky. The figure is almost
entirely occluded (41 of 45 sample rays blocked on the series; the
blocker's name is a list-order label until Q-E) and only the part blocking a
sky gap is visible.
`projH=77.63` against the 76.7 px predicted before the run, which is the
placement arithmetic confirmed.

**A CORRECTION TO MY OWN READING, recorded because it is the rule this project
keeps re-learning.** I first opened the camA crop and said it showed a dark
form with a readable head and shoulders. THAT WAS A GLANCE, NOT A MEASUREMENT,
and rule 4 says exactly why it is worthless: a picture is strong evidence that
something is wrong and weak evidence of what. The before/after/difference is
what settled it, and what it settles is smaller than what I claimed.

**WHERE MONDAY STARTS:** queue 379 first and its two bugs IN ORDER, the
contradiction before the pose, because a word and a number that disagree make
every future green line unreadable. Then 380. The occlusion is a placement
question and belongs with them, not before them.

## 2026-09-16 18:35Z: THE COST ASSESSMENT, AND A RATIO IS WITHDRAWN THE SAME HOUR

A SECOND EXTERNAL ASSESSMENT LANDED, on cost, and its finding is that PHASE A
CANNOT BE COSTED FROM WHAT EXISTS. Four things came with it. Three are filed
and NOT started, per his instruction and per CLAUDE.md rule 11. One could not
wait and did not.

- **Queue 369, price a batch end to end and not a piece.** His four conditions
  are all four: end to end, rejected work counted INSIDE the number, both
  meters read before and after, nothing else running in the window. A window
  missing one is refused and re-run, never recorded with a caveat.
- **Queue 370, the spawn log records who ran and not what they touched.** He
  notes this is the THIRD audit to say it.
- **Queue 371, author places from reusable kits and accept complete playable
  batches.** His words: the one to act on WHEN THE SLICE LANDS, so it is first
  after the slice and not during it. His caveat is part of the item: assume no
  saving until a batch is measured.
- **Queue 362 is reshaped, not duplicated.** "The resident measurement I asked
  for earlier becomes the first such batch rather than a per-item cost." The
  second resident stands, because one batch cannot say whether the marginal
  cost falls.

**TWO FORECASTS ARE WITHDRAWN AND BOTH ARE RECORDED AS WITHDRAWN RATHER THAN
DELETED**, which is his instruction and also the only way a retired number
stops circulating: queue 120's 14 to 34 weeks, and D22's six to ten weeks for
the visual slice, which he calls his own and untested. Both paragraphs now
carry the withdrawal above the number, so a reader who remembers the figure
meets the withdrawal first. Nothing may quote either, as a date or a range.

**THE ONE THAT COULD NOT WAIT.** His instruction on the split was an OR: "Add
the column before claiming the ratio again, or stop printing the number." The
column is queue 370 and waits for the slice by his own order, so the other
branch applied IMMEDIATELY, because the footer prints that ratio on every
verify run and it is pasted into every commit message. The next commit would
have claimed it again.

  AND GREPPING THE SENTENCE RATHER THAN THE SITE FOUND THREE PLACES, NOT ONE,
  which is CLAUDE.md rule 1 working exactly as written. `gameShareDay` in
  `ledger/verify.py`'s footer was the one I knew about.
  `tools/morning-brief.py` also writes it as PROSE TO JAFAR ("Of N sessions
  since the previous brief, X went to the studio and Y to the game"), which is
  the site that actually reaches him, and emits `splitStudio` and `splitGame`
  as verdict keys beside it. A third builder is withdrawing all three.

  THE COUNTING IS NOT DELETED, only the claim. `GAME_AGENTS` and the tally
  stay, so the day queue 370 lands the ratio does not have to be rebuilt from
  nothing. `GAME_SHARE_BASIS` does go, because a caption describes a reading
  and there is no reading left for it to describe.

  A WITHDRAWAL IS NOT A ZERO AND NOT A NOTHING-MEASURED, and the builder was
  told to keep all three distinguishable in the printed line. Withdrawn means
  the instrument still counts and the answer is refused; nothing-measured
  means no window existed. Two of them looking alike is how a fixture starts
  passing for the wrong reason.

## IN FLIGHT 2026-09-16 18:15Z: TWO BUILDERS ON THE FIGURE, THE LAST ELEMENT OF THE SLICE

HEAD is `7a620fd2`, pushed, tree clean, wake queue 0 due. Nothing is on the
machine: run 51 landed, was read in the ruled order and is committed. What is
moving is two tier-3 builders in this container.

- **instrument-builder** on `ue-probe/Source/LedgerProbe/Public/FrameStats.h`
  only: `FigurePatch`, `MeasureFigurePatch`, `FigureReadsAsSilhouette`,
  `FigureSilhouetteSegment`, written beside the lamp path at :2088 and :2270
  in that idiom. It was told to set NO constant: the silhouette decision is
  core mean luma below ring mean luma and nothing else, exactly as
  `LampPatchLit` compares two measured quantities. There are no frames with a
  figure in them yet, so there is no series to set a margin from.
- **engine-specialist** on `tools/ue/import_figure.py`, the spawn in
  `VignetteShot.cpp` and the import step in `ledger-probe-unreal.yml`. It
  compiles against a header the other builder is still writing, which is the
  lamp batch's shape and worked there.

**THE TREE CANNOT BE COMMITTED AND THE REASON IS THE CADENCE GATE, not a
fault.** `python3 ledger/verify.py` exits 1 at 18:2xZ with, verbatim:

    DIRECTOR NOT SPAWNED: 647 GATED line(s) of 647 changed work line(s)
    (647 tracked + 0 untracked in 0 new file(s)) vs 100 threshold
    workByScope=...ueprobe:647...  0 director row(s) newer than the reference
    reference = code commit 73c902b5@2026-09-16T17:42:43Z

  THAT IS QUEUE 363's EXACT PREDICTED SYMPTOM and it is filed, not fixed here:
  Jafar ruled the visual slice ungated under D41, the gate cannot see D41, so
  his own ungated work trips it every time. The gate is RIGHT on its own
  terms and is not worked around. Nothing commits until a director rules on
  the batch, and the ruling is ONE spawn covering all of it, not three,
  because questions fold into one spawn.

  DO NOT COMMIT THE DOCUMENTS SEPARATELY TO GET THE TREE CLEAN. The gate
  reads the TREE and not the staged set, so it stays red either way, and a
  commit on a red verify is the thing CLAUDE.md forbids in as many words: red
  deletes `ledger/.verify-footer`, so there is no footer to paste that is not
  scrollback.

  UNCOMMITTED AND AT RISK IF THE CONTAINER IS RECLAIMED: the three cost items
  369, 370, 371 and the ring item 372, the two withdrawals in queue 120 and
  D22, the 362 reshape and the 355 annotation, queue 368, two NOW.md sections,
  and both builders' code. All of it lands in the one commit after the ruling.

**WHY THIS IS UNGATED UNDER D41, and the reasoning has to survive a reset.**
The figure is a CODE-SPAWNED ACTOR, like the sky dome, the fog, the
atmosphere, the sky light, the camera and the player start, none of which are
pieces in `vignette-pieces.json`. It adds no shape kind, no condition field
and no shot row. Each of those three would be a schema change and therefore
structural under Jafar's own boundary, and BOTH BRIEFS SAY TO STOP AND SAY SO
rather than add one. A hand-back saying a schema change is unavoidable is a
correct outcome: spawn the director, do not add the field.

**THE FIGURE STANDS ONLY WHERE THE LAMPS ARE LIT**, which is 2 conditions of
33. That is probe scoping and NOT a world rule, and it is written into the
code comment as such, because a later reader finding it would otherwise have
canon saying nobody walks the street by day. The reason is arithmetic: it
leaves the 31 day rows byte-identical, so the sky brightness bracket and its
null control, which hold to +0.1, keep their meaning. A figure in every
condition would move frame `meanLuma` by roughly 0.2 at the size it will
render, which is ABOVE that tolerance.

**THE TWO THINGS MOST LIKELY TO COME BACK WRONG**, and the verdict was
designed to print both whether they are wrong or not. First, the mesh HEIGHT
IN CENTIMETRES: Mixamo and Unreal disagree about units, the failure modes are
a figure a hundred times too large and a hundred times too small, and neither
is a rendering opinion that a frame diagnoses on its own. Second, whether the
pose EVALUATED or silently fell back to the bind pose, because a T-pose
renders perfectly well and reports success. The sky dome's rule at
`VignetteShot.cpp:4665` was made law in both briefs: if the mesh is absent or
the skin did not come through, DESTROY THE ACTOR. A grey mannequin standing in
Quay Street while the verdict reads no figure is the same failure as a
2 km sphere carrying the default material, and worse here because it looks
plausible.

**WHAT UNBLOCKED IT, all checked at 18:1xZ rather than remembered.** Sixteen
real Mixamo bodies are TRACKED IN GIT under `ledger/Assets/Characters`, not
merely present on this disk, so the PC's checkout has them; 42 clips sit
beside them including Standing Idle 01, Old Man Walk, Walking With Shopping
Bag and Leaning On A Wall; D46 puts bodies on the allowlist the way animations
already were; and `grep -rn SkeletalMesh ue-probe/Source/LedgerProbe/` returns
nothing at all, so the probe has never placed anything skeletal.
`tools/mixamo-pick/fetch_bodies.py` already names the project's own picks
(michelle, remy, sophie) and already carries the sentence that matters: a
silhouette has to read as a person in a coat.

## SUPERSEDED 2026-09-16 13:20Z: RUN 49 ON THE MACHINE, NOTHING IN THIS CONTAINER

NO BUILDERS, NO DIRECTORS, NOTHING TO RESTART. All four agents of the day
landed and were reviewed. What is moving is a CI run on Jafar's PC.

- **Run 49**, GitHub run 35100795215, head_sha
  355e8d87d0654418253272d718648437088a0d02, started 13:15:50Z. Dispatched by
  appending to `production/d1-probe/DISPATCH`, which is also its own 48-run
  log, so the reason it ran is recorded in the act of running it. WATCH BY
  ANCESTRY against that sha, never by branch movement, and compare run files
  BY PREFIX because they are 7 chars and git abbreviates to 8.
- **The 13:50Z wake record carries the reading order** and it is not to be
  reordered: the build verdict's material line FIRST, then the probe's
  lampGlow lines, then the frames themselves before any gate. On the probe
  alone, "the base material predates EmissiveColor so the write is a silent
  no-op" and "1.00 is simply too low" produce the SAME two readings, a healthy
  drive and a dark lamp. Only the pair separates them.
- **Two card parts are waiting on the PC's next sweep.** The single card they
  replaced was refused by Telegram as too long and would have retried for
  ever. Confirm `sent=2` from the sweep log rather than assuming; part one
  carries the licence question that blocks tonight's figure.

## What landed today, so a fresh session does not re-derive it

The policy batch (d9af9a3d): canon-gate and goal-block wired into both
runners, template_sync retired for them, CLAUDE.md back under its bound at
1951/2000. THE CANON GATE'S FIRST RUN FOUND NOTHING: 0 findings in 209 files,
114,156 lines. The sentence two documents had asserted for months was false
only in the sense that nothing ran it.

The lamp (355e8d87): queue 333's three parts are all in. The acceptance is one
pair in one run, stated before the run: lampGlowLit=4/of=4 on a night row and
0/of=4 on a day row of the same camera.

THREE CLAIMS OF THE RESIDENT'S FAILED A CHECK TODAY and each was caught by
running a command rather than re-reading a sentence: a push read as successful
when it had been rejected (the pipeline returned tail's exit code); 212 read as
the same denominator as 209 (offered against examined); and queue 335's claim
that the Unity path renders a Mixamo body, repeated into a message to Jafar
before it was caught. It does not and never has.

  THE FOUR ITEMS ARE FILED AND NOT STARTED, per his standing rule of today:
  350 marked DONE at d2687bf9, 355 filed for the throughput ledger's piece
  definition, 344 and 345 already filed for the role-proxy split. His rule
  now sits in CLAUDE.md rule 11, which is the rule it generalises.

  TOMORROW, IN HIS ORDER: wetness, materials, then dusk with lamps lit and a
  figure in silhouette. Ungated under D41, so no director, no predictions, no
  ruling records. Queue 333 carries the lamp's full implementation map,
  already bought with an agent's whole budget; queue 028 half one is the
  figure. AND IF ANOTHER ENFORCEMENT FINDING TURNS UP: FILE IT AND KEEP GOING.
  Do not open a third front on it, which is what happened today.

## 2026-09-16 09:05Z: THE AUDIT LANDED IN FULL. d2687bf9 IS PUSHED, TREE CLEAN

His external audit at 07:30Z named four things and ALL FOUR CHECKED OUT AT THE
SOURCE, arithmetic included. All four are landed in d2687bf9, 36 paths. His
budget row is 2026-09-16b: 59 total, 60 Fable, ceiling 85, 25 points headroom,
takenAt 07:30:09Z.

WHAT IS MOVING RIGHT NOW: one engine-specialist on queue 333, the sodium lamp's
emissive element, briefed from section 3 of the 06:35Z ruling. Nothing else.
The tree was clean and committed when it started, so anything dirty is its
work.

THREE CORRECTIONS I OWE AND HAVE SENT, kept here because a later reader meets
this file and not the conversation:

  1. I TOLD HIM THE CLAIM BUG PROBABLY EXPLAINED THE 2026-09-06 SWEEP. It does
     not, and the director established it rather than arguing it:
     study-sweep.txt reads claim=/Unknown on 72 of 72 paths, zero
     Contradiction. Sightings file at 0.9 and knowledge promotes at 0.95, so
     nobody in that grid could be lied to about something they knew. What
     survives is narrower and still real: the sweep never put a lie in front
     of an eyewitness in 648 sessions, so the instrument is blind exactly
     where the bug lives. Queue 348 is owed for that arm.

  2. I REPORTED QUEUE 334 AS LANDED AND IT IS OPEN ON RULE 6. light_probe is
     written into the golden 49 times and read ZERO times: struct Shot at
     VignetteSpec.h:288 is {Id, CameraId, ConditionId}, S.LightProbe appears
     nowhere under ue-probe/Source, and ShouldProbeShot reads the CONDITION's
     lantern flags, which are on for wet_night. All six settling rows would be
     probed, which is the one thing a settling series forbids. No carrying run
     until the reader lands.

  3. I DAMAGED vignette-scene.json AND REPAIRED IT. Applying the dictated
     settle_note text through json.dumps reformatted the whole hand-authored
     file, 1448/536. Reconstructed from HEAD's text with the three semantic
     deltas re-applied in HEAD's own one-line aligned style; 51/44 now and the
     data asserts equal to the verified version. Rule 5, and I broke it on a
     file I had just fenced two builders out of.

THE SEVEN TURN-LIMIT DEATHS ARE THE DAY'S REAL COST. Roughly 1.2M subagent
tokens across seven agents that hit their limit without reporting, several
having FINISHED the work and simply never said so. Queue 336 is rewritten
around the actual diagnosis: the instruction is present in the definitions AND
in the briefs and does not fire, and a stop condition tied to success cannot
fire when the work does not succeed. Two-sided conditions are the only thing
that has worked.

STILL OWED, none of it dispatched: the canon gate tools/canon-register-check.py
(so his standing rule is currently a sentence nothing enforces); queue 028 half
one, the Blender GLB bake; queues 348 and 349 to file; and the D29 and D30
judgement calls the canon sweep left for him rather than applying.

## 2026-09-16 06:50Z: THE TWO THINGS HE ASKED FOR IN TOMORROW'S BRIEF

He named them himself and said to put them in the brief rather than as
messages, so they are recorded here for the Producer to pick up rather than
sent. Both are read off the 06:37Z verify footer, not recalled.

ONE, DID THE NIGHT FRAMES SURVIVE STAGING. YES, ALL OF THEM.
shotFilesNamed=43 shotFilesPresent=43 shotFilesTracked=43 shotFilesMissing=0.
The four ue-pinset_night frames had been rendered and discarded on every run
since they entered the spec, zero commits ever, because four workflow sites
filtered on ue-vign_*.png and the copy step was the decisive one. They are in
the repository now and the waiver that forgave their absence expired by itself
on the run that landed them. He gets a clean yes.

TWO, THE SPAWNS BY TIER, AND HIS PREMISE NEEDS HALVING RATHER THAN AGREEING
WITH. He said "now that routing is enforced". Half of that is true and the half
that is not is the interesting half.

  ENFORCED: the model LADDER. ledger/verify.py's agent-model-overrides check
  fails the build on any spawn that ran ABOVE its definition's declared model
  without a resolving written reason. It examined 135 rows this run and found
  justifiedUp=0 downOrSame=135, so nothing needed a reason because nothing
  exceeded its definition.

  NOT ENFORCED: the MIX. The tier keys carry their own disclaimer in the
  footer, "READING ONLY (no bound, nothing here is gated)". Nothing anywhere
  says spawn fewer of the expensive ones.

  AND THE NUMBER WORTH HIS ATTENTION IS THE BOTTOM RUNG, WHICH HAS NEVER BEEN
  USED AT ALL. Today: haiku 0, sonnet 2, opus 8, fable 2 over 12 spawns, with
  the top two at 10 of 12. LIFETIME: haiku 0, sonnet 79, opus 392, fable 173
  over 644 classified rows of 663 (the other 19 have no rankable definition).
  ZERO HAIKU SPAWNS EVER. And tierRosterIdle=3/15 names the three definitions
  never selected in the whole log, guard-tester, integrator and reach-auditor,
  which are exactly the three that sit on haiku. The cheapest rung is unused
  because the only roles defined at it are roles the studio never reaches for.
  That is a fact about the roster, not about routing, and it is the one a
  ceiling at 85 on the governing meter makes worth saying.

## 2026-09-16 06:10Z: RUN 48 READ. THE FRAMES ARRIVED AND THE LAMPS DO NOT LIGHT

His reading came in unprompted in answer to the brief's first line: 54 and 57,
Fable governing, 28 points of headroom, and HE TAPPED THE BRIEF READABLE, which
is the first tap ever recorded. He also said to keep going on the visual slice
without coming back, and to put two things in tomorrow's brief rather than as
messages: whether the night frames survived staging, and the spawns by tier.

THE STAGING FIX WORKED, WHICH IS THE FIRST ANSWER HE ASKED FOR. 43 named, 43
present, 43 tracked, 0 missing, stagedPngLeavesAbsent=0, and the waiver expired
by ITSELF because run 48's verdict carries a different sha. Four frames that
had been rendered and discarded on every run since they entered the spec are in
the repository.

AND THE BLANK MOVED: run 47 blanked pinset_night_2 and _3; run 48 blanked
pinset_night_1 and only that one. Same condition, same camera. Not
deterministic, so it is a timing or streaming race and not the 2K textures
causing it outright. Queue 325 updated.

QUEUE 329 IS QUANTIFIED AND LIVE, AND A SECOND FAULT SITS BESIDE IT.
lightsAboveFloor reads 17/28 on its first real run. EIGHT of the seventeen are
blank-frame artifacts (queue 329); SIX MORE are void because their shot's own
no-toggle control disagrees with itself by 0.16498 while certifying smaller
surpluses, which is queue 332, filed this morning. THREE SURVIVE BOTH. They
are pinset_night_4's three window practicals and not one lantern. So the
honest reading of run 48 is 3 of 28, and 17/28 must not be quoted.

  The five-to-eight correction is worth keeping: the first count filtered on
  the literal 0.00152, and camA_night writes its blanks at 0.00075. Matching a
  VALUE where the test is a THRESHOLD lost three reads. The threshold now has
  a printed gap under it (no value in the 48-line series lies between 0.00152
  and 0.02392).

  The floor DID catch pinset_night_2's blank CONTROL and made that shot
  NO-READ, so the design is right and only incomplete.

THE LAMPS DO NOT LIGHT, AND THIS IS THE DUSK FRAME'S REAL BLOCKER. I opened
ue-pinset_night_3.png and measured it: ZERO pixels in the whole frame are both
bright (luma over 120) and warm (R minus B over 20), which is what a lit lamp
is. The brightest pixel is the SKY at luma 181, neutral. The warmest thing is
dark brick. Sky band 78.1 against ground 12.8.

EXPOSURE IS NOT THE CAUSE, AND THAT WAS MY DIAGNOSIS UNTIL A BUILDER REFUSED
IT AND I CHECKED. A tonemap is monotone: it cannot make a fixture darker than
the sky behind it come out brighter than it. The cause is in the source, read
in the code rather than guessed. VignetteShot.cpp:1310 to 1326 is the whole of
what a piece's emissive flag does: it spawns a point light 0.05 m under the
piece and nothing more. SurfaceBind.h and tools/ue/make_base_material.py
contain ZERO hits for emissive, EmissiveColor or selfillum, so the lamp head
renders through the ordinary metal surface. The four lanterns are the file's
only emissive pieces, 4 of 610, each shape=box surface=metal asset=None. The
lamps are dark boxes with invisible lights under them. Queue 333.

  THE GLOW MECHANISM ITSELF WORKS, which is what makes this a content fault
  rather than a renderer one: vign_camA_night carries a lit window practical
  at (1045,170) to (1051,173), 23 pixels, peak R minus B of 130 at rgb
  131/108/1, with soft falloff around it. A warm source in this street renders
  as a warm source. The lantern just has nothing to glow with.

  EXPOSURE IS STILL OWED, for the OTHER half. All six lantern-lit rows read
  shotExposurePin=AUTO, and four of their six no-toggle controls disagree with
  themselves. That is what makes the night frames unreadable and it is queue
  332 and 334, not a lamp fix.

  AND THE FOUR pinset_night ROWS ARE NOT QUEUE 276's SETTLING SERIES, which I
  nearly adopted them as. They sit at shot indices 30, 33, 36, 39 with a
  PINNED day frame immediately before each one. Four renders each preceded by
  a different pinned exposure measure their predecessors. Queue 334.

AND THERE IS NO FIGURE, AND THE PROBE CANNOT RENDER ONE TODAY. Of the spec's
610 pieces, a search for figure, person, man, woman, ped, human, char and
silhouette returns 7 hits and ALL SEVEN ARE FALSE POSITIVES (dropped kerbs
matching "ped", a manhole matching "man"). The read-only investigation came
back with the shape of the gap:

  NO SKELETAL MESH PATH EXISTS. Grepping every .h and .cpp under
  ue-probe/Source for SkeletalMesh, USkeletalMesh, FBX, AnimSequence and Bone
  returns zero hits anywhere. VignetteShot.cpp's LoadShape, LoadPropMesh and
  SpawnPiece are all typed to UStaticMesh and AStaticMeshActor.
  tools/ue/import_prop_meshes.py imports GLB by checking the glTF magic bytes;
  it cannot read an FBX. LedgerCharacter.h says in its own words that the
  probe ships no body.

  NO TOKEN IS NEEDED, WHICH IS THE ONE ANSWER THAT MATTERED. The 91 files
  under ledger/Assets/Characters already include 18 full Mixamo bodies and
  about 65 clips on the same rig, and tools/mixamo-pick/README.md says Jafar's
  bearer token is needed only to fetch NEW ones. The blocker is pipeline, not
  acquisition, and nothing here asks him for anything.

  THE CHEAP ROUTE IS DISHONEST AND IS NOT BEING TAKEN. 20 of the 610 pieces
  are decals, and one more pointing at a photograph would need no new C++ and
  no importer. But SurfaceBind.h calls a decal card "the piece's own picture,
  opaque", and a grep of it and make_base_material.py for Masked, Opacity,
  Translucent and AlphaChannel returns zero hits in either. A decal is always
  a hard-edged opaque RECTANGLE, never a silhouette. On the frame Jafar judges
  the whole project by, that is a sandwich board, and it casts a rectangular
  shadow.

## 2026-09-16 01:15Z: RUN 47 READ. WETNESS REACHES THE FRAME; TWO NIGHT SHOTS DO NOT

bf6fc61a rendered c7387972. Section 10 of the 22:25Z ruling was written before
the run existed and it hit almost exactly: walks=17 as derived from the shot
order, wetnessRedriveWrote=10030/of=10370, refused=notOurRoute.340 with every
other bucket zero, readback=same-value, TallyMismatch ABSENT,
shotWetnessAgrees=yes on all 43, nullSeriesTiedGroups=0/of=30. Controls held:
band.skyCentre.p50=0.8035 and shotExposurePinRead=0.3000/0.3000 on hook_day,
unmoved across four runs.

WETNESS NOW REACHES THE FRAME, and the statistic that shows it is NOT the one
section 10 named. Against the certified null pair:

    pair                    px differing   maxChannelDelta   MEAN over differing
    null (same inputs)         79.86%          38/255             1.944
    wet_000 vs wet_060         82.07%          63/255             8.653
    wet_000 vs wet_100         76.82%         124/255            12.825

  The magnitude is 6.6x the null floor and the ladder is now MONOTONIC. In run
  46 the wetness pair sat BELOW the null (1.463 against 1.487) and the order
  was inverted. But the PERCENTAGE statistic is SATURATED: render noise already
  moves four fifths of the pixels, so wet_000 vs wet_100 differs in FEWER
  pixels than the null while differing far more in each. Section 10 predicted
  separation "on the same two statistics" and on percentage it does not. The
  prediction was half measuring the wrong thing, and it was mine.

TWO SHOTS CAME BACK BLANK AND RUN 46 HAD NONE: pinset_night_2 and
pinset_night_3, both pin_setter_night, 2 of the 4 shots at that condition.
shotMeanLuma=0.0015 and shotNonBlackPct=17.73 against a working sibling's
0.2439 and 100.00. NOT a wetness fault: those rows read shotWetness=0.9000,
shotWetnessOnPieces=0.9000, shotWetnessAgrees=yes. QUEUE 325, and it is ahead
of the dusk frame with 319 and 324, because pin_setter_night is one of only
two conditions that light the lanterns and the dusk frame is that family.

THE PACK IS VISIBLE AND THE ROAD IS NOT WET. Measured on rectangles, run 46
against run 47, hook_day, same camera and wetness 0.6 in both:
sky control +0.00 (sd 1.68 to 1.69), PURE ASPHALT centre -0.01 (its texture is
byte-identical between the runs), kerb region -4.78, railings -4.15 with sd
46.28 to 40.91. I FIRST WROTE THAT THE ROAD READ WET IN RUN 47 AND THE
MEASUREMENT REFUTED IT: what I saw was the kerb sitting 48 points darker in a
crop I had not measured. The eye reads contrast and invents differences, and
the cell map I ran before cropping did not excuse the sentence I wrote after.

band.ground.p50 moved 0.2702 to 0.2658 and IS NOT A WETNESS READING, exactly
as the dispatch entry said in advance: the kerb is 48 points darker and the
concrete 23 points paler this run, both inside that band.

## 2026-09-15 22:55Z: THE 22:25Z BATCH IS RULED AND COMMITTED, AND UNRENDERED

Both halves of the batch land under
`game-design/decision-2026-09-15-ruling-per-condition-wetness-lands-and-the-licence-record-owes-the-pack-its-row.md`,
whose eight dictated corrections were hand-applied before the commit and whose
hold condition was met and printed: the g++ suite went 3382 to 3383 and the
done segment measured 636 of its 700 bytes, under the 680 bound.

THE WETNESS HALF IS UNRENDERED. Every line of VignetteShot.cpp is unverifiable
in this container. THE READING ORDER FOR THE RUN THAT CARRIES IT IS SECTION 10
of that record, which was written BEFORE the run existed so the run can refute
it, and the DISPATCH note for that run quotes section 10 verbatim and dated. A
prediction written after a run is not a prediction.

322, 323 and 324 are filed by the ruling. 323 is the one that matters outside
the studio: the SHIPPED CityPack has no row in THIRD-PARTY.md at all, and that
file's ATTRIBUTION.json claims a tool enforces agreement with a file the tool
never opens. Nothing unlicensed ships, ambientCG is allowlist line 5; the
RECORD is what is wrong, and this project's own words say the record is the
part that has to be right.

313 IS EFFECTIVELY DIAGNOSED AND IT IS NOT A FAULT. The four-quadrant card and
the two swatches are the probe's own measurement controls: MakeControlTexture
builds a 2x2 nearest-filtered texture its own comment calls "four flat
quadrants", controlQuads reads 3/3, and shotWholeFrameIncludesControlQuads
reads yes on exactly 2 of 43 shots, both of them cam_A, one of them
vign_camA_night. The decisive measurement still owed is the colour quad's
projected box against 313's rectangle. THE CONSEQUENCE FOR JAFAR'S DUSK FRAME:
it must not be taken from cam_A with the controls shown.

DO NOT DISPATCH citypack-shortlist.yml until item 7 of section 11 is in the
tree (it is, as of this commit): the first live run must commit
ATTRIBUTION.json beside the sheets or the new THIRD-PARTY.md row is false.

## 2026-09-15 22:10Z: TWO BUILDERS LIVE IN THE TREE, NOTHING COMMITTABLE

DO NOT COMMIT, DO NOT STASH, DO NOT SPAWN A THIRD BUILDER INTO THESE FILES.
Both agents hit the 45-turn limit without reporting and were RESUMED, not
restarted. The tree holds two half-finished batches at once.

    content-wrangler   THIRD-PARTY.md, tools/attribution-check.py,
                       tools/citypack/fetch_textures.py
    engine-specialist  ue-probe/Source/LedgerProbe/Public/SurfaceBind.h,
                       .../Private/VignetteShot.cpp, .../Public/VignetteSpec.h

THREE THINGS INDEPENDENTLY BLOCK A COMMIT and a stop hook asking for one is
not a fourth opinion, it is the case CLAUDE.md names: the resident never
commits a builder's work-in-progress because a stop hook asks.
  1. ledger/.verify-footer does not exist. verify is red, and red DELETES it.
  2. director cadence: 445 GATED ue-probe line(s) of 1599 changed, vs the 100
     bound. The newest studio-director row is 2026-09-15T19:43:24Z, OLDER than
     the reference commit 24b54723@20:40Z, so a FRESH spawn and a fresh
     <!--RULING spawn=...--> stamp are required. The citypack half is entirely
     ungated under D45 (tools 991, workflows 163) and would commit alone, but
     the gate reads the whole tree, so it cannot.
  3. Both builders are mid-edit. The engine one moved 406 to 445 gated lines
     while this was being written.

WHAT IS ALREADY SETTLED, so nobody re-does it:
  D38 batch and its PUBLISH are DONE. publish-glance run 37 (id 35021034653)
  published 24b54723, which contains D38, and its step 13 requested the page
  back and matched. production/site-served.txt still names run 27 and is a
  DECAYED HAND-MAINTAINED MARKER, not the state of the page: queue 318.
  RUN 46 IS READ. Wetness binds but does not reach the frame per condition.
  Measured against a null control rather than from the median: two frames the
  run certifies as sharing every applied input differ by 75.59 per cent of
  pixels at maxChannelDelta 29/255, and wet_000 vs wet_060 differ by 76.03 per
  cent at 41/255. The wetness difference is INSIDE the noise floor. Queue 309
  is the fix and is what the engine builder is on.

FILED THIS TURN, not to be re-found: 318 (the served marker has no writer),
319 (the lantern state is asked per condition and read back nowhere, which is
ahead of the dusk frame because "lamps lit" is the ask), and a measured
appendix on 313 (the colour card predates the wetness batch by three runs).

THE ORDER WHEN BOTH HAND BACK: review both diffs, spawn studio-director for
the batch, verify green, footer FROM THE FILE, commit, push, THEN dispatch
citypack-shortlist.yml. Wake record 0f32ea3a carries the same instruction.

## 2026-09-15 20:05Z: THE HOLD LIFTED AT 19:42:59Z, AND D38 IS LANDED

THE HOLD IS OVER AND THE RECORD SAYS SO EXPLICITLY, because the director
reviewing D38 refused to leave it unwritten and was right to. The 19:20Z block
below says NO BUILDERS and "do not spawn a director for it". Two agents were
then spawned. Here is the sequence with its instants, so nobody has to
reconstruct it:
    19:20Z  the hold is recorded, his newest reading fifteen hours old
    19:42:59Z  HIS READING ARRIVES: total 43, Fable 44, "taken now"
    19:43:24Z  the studio-director is spawned, 25 seconds later
    19:44:56Z  the queue 314 builder is spawned
THE READING LIFTED THE HOLD BEFORE EITHER SPAWN. This is not a breach and it
is not a waiver: it is the rule working exactly as he designed it, one number
turning the studio back on. What was missing was this paragraph, not the
permission. The 19:20Z block stays below UNEDITED because it was true when it
was written, and a hold rewritten after the fact is a hold nobody can audit.

D38 IS LANDED UNDER THE 19:43Z RULING, which read the diff, RE-VERIFIED ALL
FIVE CITATIONS AGAINST THE CODE rather than against D38's table, and OPENED
THE PAGE rather than ruling from the selftest.

THE PIXEL IS ANSWERED AND THE SECOND QUESTION TO HIM IS SPENT. The ruling
prepared a question in advance in case his judgement line and RULING 3's
ladder could not share the first screen. Printed from the live run:
judgementLineTopPx=798/844-fold, judgementLineHeightPx=43,
judgementTopIsAboveTheFold=yes, and the stronger
judgementWholeLineAboveTheFold=yes, with ladderBottomPx=749. They co-exist
with 46 px to spare, so the question is not asked.

THE PAGE HALVED AND NOTHING WAS DELETED: pageScrollPx 4255 against 8556 had
the audit stayed inline, auditOnTheScroll=no-it-is-one-tap-down,
nothingDeletedToShorten=true. That last token is the 2026-09-07 rebuild's own
rule holding, which was that the evidence moves and does not go away.

WHAT THE BOARD NOW SAYS FIRST, which is the thing he asked for: "20 of 111
tiles here carry your judgement. The other 91 are the studio's reading." It is
DERIVED at render time from roleCounts, read back by check_typed_attribution
against the run's own count, and the guard bites if it claims every tile,
drops its denominator, or is deleted.

THE CITATION READING OVERTURNED ONE OF D38'S OWN SENTENCES. D38 said each of
the five should be "marked built-not-measured where no verdict key emits it".
The director read the verdict file and ALL FIVE HAVE A KEY: blood, provenance,
carry, the disguise gate, windowsLit=3/6. So the clause had no case to apply
to. The lit window is typed PARTIAL rather than exists on the builder's own
reading, and that is the one colour the code changed.

THREE ITEMS FILED BY THE RULING, 315, 316 and 317, and one of them is the
honest limit of tonight: the board's tally sentence is DERIVED AND NOTHING
READS IT BACK, and map.py's selftest plants no ruled-out tile, so the only
accepting case for the fourth mark is today's live data. Not blocking while
the data carries four, and filed because it stops being an accepting case the
moment the last ruled-out tile is retyped.

STILL OPEN AND GOING TO HIM: the sleep pair. "sleep and the day boundary"
(player-facing, 2026-09-10) and "sleep as a way to cross a day" (moat, D39
item 5) are one verb on two absent tiles. The director's recommendation is one
tile in the moat row under D39 with the older tile retyped into it under D21,
which would read 110 with 20 his. It landed as two because his record said
twenty tiles, and collapsing them is his call rather than the studio's.

## 2026-09-15 19:20Z: THE STUDIO IS AT INBOX ONLY. HIS TEN HOUR RULE BIT THE HOUR HE MADE IT.

RULED TONIGHT BY JAFAR, replacing forty eight hours: a budget reading older
than TEN HOURS means the day is UNMEASURED, and unmeasured means INBOX HALF
ONLY, NO BUILDERS, NO DISPATCHES, NO RENDERS. And the brief asks him for the
reading as its first line every morning, with the studio holding at inbox only
until he answers. Recorded in production/budget.md stop condition 2,
production/repo-move-triggers.md step 3, production/watchdog-prompt.md,
.claude/agents/producer.md as item 0, and
game-design/decision-2026-09-15-ruling-ten-hours-and-the-brief-asks-for-the-
reading.md.

THE STUDIO IS HELD AS OF NOW. His newest reading is 34/36 at about 04:1xZ.
It is 19:20Z. FIFTEEN HOURS. Under the rule he has just made, tonight is
unmeasured and nothing may be spawned, dispatched or rendered until he gives a
number. READING LANDED RESULTS AND COMMITTING FINISHED WORK STILL COST NO MODEL
TIME AND ARE STILL ALLOWED, which is what this block is.

WHAT IS HELD, NAMED SO NOBODY RESTARTS IT BY ACCIDENT:
  THE D38 BUILDER IS NOT RESUMED. It hit its turn limit a third time at 19:14Z
    with Parts 1 and 2 DONE and Part 3 unverified. Its work is ON DISK AND
    UNCOMMITTED. Do not spawn it again, do not spawn a director for it, and do
    not finish it by hand: the resident does not implement.
  QUEUE 314, the two tool changes that would make his ten hour rule
    mechanical, is filed and BLOCKED on the same rule. The first thing his
    next reading buys is the checker that enforces the rule about readings.
  NOTHING IS DISPATCHED. Run 46 landed and was read; no run 47 goes out under
    an unmeasured day.

WHAT THE D38 BUILDER ACTUALLY GOT DONE, measured off the tree rather than
taken from a report it never delivered:
  PART 1, THE SCHEMA, DONE AND GREEN. STATUSES is now the four value tuple
    with ruled-out; NOWHERE_STATUSES groups absent with ruled-out without
    collapsing them; and systems-inventory-check.py 511 to 517 REQUIRES a
    ruled-out tile to name a decision record, which is better than the
    convention I briefed and makes D38's "rather than leaving it to look like
    an oversight" impossible to forget. Selftests 44/44 on the inventory
    checker with 12 accepting first, 152/152 over 38 checks on the map.
  PART 2, THE TWENTY TILES, WRITTEN AND THE COUNTS ARE EXACTLY D38'S. The
    inventory went 91 to 111 systems, which is plus twenty. absent went 25 to
    36, plus eleven, D39's now-or-next. ruled-out is 4, D39's struck items.
    exists plus four and partial plus one is D38's five built systems, typed
    on their own evidence rather than blanket typed, which is the difference
    between reading the code and copying the ruling.
    AND THE NUMBER HE ASKED FOR: 20 of 111 tiles now name him in typedBy,
    against 0 of 91 this morning.
  PART 3, THE PAGE, UNVERIFIED. map.html is modified so something was done,
    but whether the first screen carries the judgement count derived at render
    time, and whether the diagnostics moved behind the tap, HAS NOT BEEN
    CHECKED BY ANYONE. Do not claim it landed. The page was rejected once
    before for how it READ rather than for what it computed, so the check is
    to open it, not to run the selftest.

NOTHING OF D33 TO D39 HAD LANDED BEFORE TONIGHT, which was his first question
and the answer was zero of seven, not some of seven. Their only citation
outside their own files was rulings-log.md, the register's own index. The
inventory's newest cited ruling was D16; Traces.cs and Arsenal.cs were cited
zero times in it, exactly as D38 predicted on the day it was written; and
DayCircleHeat, which D34 says to record as ruled, appeared zero times.

## 2026-09-15 18:30Z: RUN 46 RENDERED WET, BOTH NAMED FAULTS WERE AVOIDED, AND THE ALBEDO HALF WON

WHICH RUN, BY GIT AND BY THE ARTIFACT, because the sanctioned watcher is broken
(queue 312) and was not used. Commit c7f2cc01 rendered 64103f7b, which CONTAINS
0942cf1e; the verdict's own line 1 reads "UE vignette shot 64103f7", which is
the ci.md rule and outranks any tool. Dispatched 18:08Z, landed by 18:26Z:
SEVENTEEN MINUTES, so the runner is healthy again after nine hours of not
claiming.

THE PRECONDITION HOLDS AND IT WAS READ FIRST: materialConnections=19/19 in the
live ue-build.txt. The graph grew its three wetness wires and every one is
connected, so Alpha is not short and B is not short. This is a wetness result
and not a node-graph fault wearing one. (The 12/14 and 14/14 elsewhere in
d1-probe are DISPATCH prose from runs 19 to 24, not readings.)

BOTH FAULTS NAMED BEFORE THE RUN EXISTED WERE AVOIDED, neither narrowly:
  NO DEAD WRITE. midWetReadbackAll=14/14, every surface's wetness came back as
    it went in. midWetSetGot=0.6000..0.6000 on four surfaces and
    0.0000..0.0000 on ten. Queue 186 named this as the rung's likeliest
    failure and it did not happen: the parameter exists on the material and it
    is set.
  NOT POLISHED PLASTIC. wetnessSurfacesWet=4/14 and
    wetnessSurfacesDarkened=4/14, the SAME four. Every surface that got
    shinier also got darker, which is the original author's whole thesis
    holding in an engine for the first time.
  wetnessSurfacesSet=14/16, wetnessValue=0.6000 from
    overcast_day/first-shot-condition, wetnessShotsAtValue=35/43,
    wetnessCondsAtValue=29/33.

AND THE NUMBER NOBODY PREDICTED, on the row named shot vign_hook_day
camera=cam_hook condition=overcast_day, run 45 read off the same named row:

    band.ground.p50        0.2987  ->  0.2702
    ground meanRGB    68.5/69.6/73.2  ->  67.6/69.8/75.3
    band.skyCentre.p50     0.8035  ->  0.8035     control, unmoved
    shotExposurePinRead 0.3000/0.3000 -> 0.3000/0.3000  control, unmoved

THE ALBEDO HALF WON. The entry refused to predict the direction because the
albedo term darkens by about 0.73 in gamma and the roughness term brightens by
reflecting a brighter sky, and a one-point model cannot say which wins. It
came down. THE PER-CHANNEL DETAIL IS THE BETTER HALF: red FELL, 68.5 to 67.6,
while blue ROSE, 73.2 to 75.3. The road got darker AND bluer, which is what a
wet surface reflecting an overcast sky should do and is not something either
term produces alone.

THE WET LADDER CONFIRMS THE STATIC BIND AS A MEASUREMENT RATHER THAN AN
ARGUMENT. vign_wet_000, vign_wet_060 and vign_wet_100 all read
band.ground.p50=0.2702, identical. A shot asking for wetness 0.000 renders at
0.6 exactly like one asking for 1.000, because the bind takes the first shot's
condition and never re-drives. THE LADDER THAT EXISTS TO VARY WETNESS DOES NOT
VARY. That is not a bug in this batch, it is the documented cost of the static
half, and it is queue 309's justification visible rather than argued.

A FINDING FROM THE NIGHT FRAME, NOT ASKED FOR, AND DELIBERATELY UNDER-DIAGNOSED.
ue-vign_camA_night.png carries, in the middle of the shot, a piece reading as a
four-quadrant primary-colour card (green, yellow, red, blue) on the lamp post,
and two texture swatches apparently floating against the left-hand brick. The
spec DOES have card-shaped piece kinds (flat_cards, shop_cards,
_lit_interior_card), so these are plausibly spec pieces rendering wrong rather
than stray debug geometry, BUT WHICH IT IS HAS NOT BEEN MEASURED and is not
claimed here: a picture is strong evidence that something is wrong and weak
evidence of what. Filed as queue 313. It matters because his third item is a
dusk frame he judges by, and neither of these belongs in it.

## 2026-09-15 17:15Z: RUN 45 LANDED, IT RENDERED DRY, AND HIS 0.85 IS 0.2987

WHICH RUN, SETTLED BY ANCESTRY AND NOT BY EXPECTATION. Commit 22c922ee, "UE
machine probe from cb0c55a2", landed 15:09Z with 72 files. Every verdict's line
1 reads cb0c55a. cb0c55a2 CONTAINS e1d19817, the walk-back batch, and DOES NOT
CONTAIN 0942cf1e, the wetness batch. So run 45 rendered DRY and the dry re-read
he asked for in his own words WAS TAKEN. That is the cleaner of the two
branches written down this morning and it is the one he can read without
interpreting a wet road.

HIS NUMBER, ON THE HOOK DAY ROW, LIKE FOR LIKE, run 44 read out of git rather
than from memory. The file carries ONE ROW PER SHOT AND CONDITION, so the row
is named: shot vign_hook_day camera=cam_hook condition=overcast_day.

    band.ground.p50        0.2711  ->  0.2987
    ground meanRGB    62.2/63.4/67.4  ->  68.5/69.6/73.2
    band.skyCentre.p50     0.8035  ->  0.8035     (control, must not move)
    shotExposurePinRead 0.3000/0.3000 -> 0.3000/0.3000  (control)

THE DIRECTION HELD AND THE CONTROLS DID NOT MOVE, which is what makes the
ground movement attributable to the grade rather than to exposure. Blue is
still highest, 73.2 over 69.6 over 68.5, so the parameter is read as a COLOUR
and not collapsed to a scalar.

AN ERROR OF MINE, CAUGHT IN THE SAME TURN AND WORTH THE LINE. I first quoted
0.3048. That came from a grep across the WHOLE FILE, which picked an arbitrary
row out of the many this file carries. The hook day figure is 0.2987. Two
numbers off different rows compared as one is precisely what this project's own
rules name, and I did it before catching it. Third error of the day; the first
two were the -fsyntax-only reading and the stash under a reviewer.

ALL EIGHT ASSERTIONS IN THE DISPATCH ENTRY HELD, and that entry deliberately
carried NO predicted p50:
  12 of 12 resolved pack lines carry jafarWalkBack.0.85..ruled.2026-09-15,
    four at grade-on-white.126.129.134 and eight at grade-on-white.199.203.212,
    counted exactly 4 and exactly 8.
  the two procedural parity lines are UNMOVED at 31.22.14 and 147.127.35, one
    each, which is the whole point of the walk-back sitting at one call site.
  the two controls above.

THE FRAME, READ BEFORE ANY OF THOSE NUMBERS, per the ruling's section 9. Brick
reads as brick and the rubble wall on the right carries real material
variation. THE CONSPICUOUS FAULT IS THE BINS: they are the brightest things in
the picture, near-white cylinders against a mid-grey street, reading as
untextured primitives. That is queue 300's finding VISIBLE rather than
inferred, and it agrees with this morning's bins test, which refuted the fog
hypothesis by measurement. NO EYE COMPARISON AGAINST RUN 44 WAS MADE and none
will be: the standing rule ruled this morning is that the eye reads contrast,
not value, and invents differences across time. The table above is the
comparison.

WHAT IS STILL OPEN AGAINST HIS SHEET. 0.2987 sits 0.074 under the sheet's
0.373 and 0.213 under the full legacy 0.5117. His own instruction covers it:
"Do not tune by eye toward the sheet, because the sheet is wet and the street
is dry; this value is provisional and gets re-read when wetness lands rather
than kept." Wetness is now BUILT and UNRENDERED, so the re-read he named has a
date rather than a wish.

THE PRODUCER OWES HIM THIS TOMORROW, not today: he has had the blocking
exception and one message a day is his ruling. The brief carries the 0.2987
with its two neighbours in one sentence, that the dry re-read was taken and
wetness is next, and the three errors of this seat under the line he asked for.

## 2026-09-15 09:48Z: THE DEDICATED WATCHER IS STOOD DOWN AND THE HOURLY NET TAKES IT

THE ONE CHECK, AND IT BELONGS HERE RATHER THAN IN A WAKE RECORD NOBODY OPENS:

    python3 tools/landed.py --contains 0942cf1e

READ THE PRINTED LINE, never an exit code through a pipe. At 09:47Z it read
"not yet: no run contains 0942cf1. 362 run(s) known, newest cb4767e", with run
45 queued 211 minutes since 06:16:37Z. Watch by ancestry and never by branch
movement.

IF IT HAS LANDED the runner returned and the visual lane is open. Read the
FRAME FIRST in section 9 of
game-design/decision-2026-09-15-ruling-wetness-lands-static-and-the-widening-
is-not-an-instrument.md, measure before writing any sentence, and take
materialConnections=19/19 as the PRECONDITION before any wetness key, because a
short Alpha means every surface sat at the node's constant 0.5 and is not a
wetness result at all. Then settle WHICH run rendered it by ancestry and not by
expectation: run 45 checks out cb0c55a2 by its own push event, so if the landed
commit CONTAINS 0942cf1e it rendered WET and his 0.85 dry re-read was never
taken, and the Producer owes him that in one sentence.

IF IT HAS NOT LANDED: do not re-dispatch, do not touch production/d1-probe/
DISPATCH, and do not start a queue item to look busy. The 08:26Z block above
shows why every item in his order is behind this one frame.

WHY NO DEDICATED WATCHER IS ARMED, decided at 09:48Z and written down so the
next session does not read it as a dropped thread. The hourly INBOX AND RESUME
trigger reads this file before the queue and can make the check above, so a
second one-shot at fifty minutes does the same work twice for about twenty five
minutes of extra cover. THE THING BEING WAITED FOR IS A PERSON, not a job: he
was told at 07:41:27Z, pc-inbox has not moved since, and it is late morning on a
working Tuesday. Against a precedent measured in DAYS, being fifty minutes late
to notice costs nothing, and polling a machine that is waiting on a person is
not diligence. The hourly trigger is the armed resume; this block is its
instruction.

HE HAS NOT REPLIED OR TAPPED. pc-inbox head is 634da649, unchanged since
07:41:28Z. A tap or a reply is an ANSWER, a different register from a second
unprompted message, and is answered in the same run it arrives. Nothing else
goes to him today: one message a day is his ruling, he has had the blocking
exception, and a correction is not a second message in his own words.

## 2026-09-15 08:26Z: EVERY ITEM IN HIS ORDER IS NOW BEHIND ONE FRAME FROM ONE MACHINE

CHECKED RATHER THAN ASSUMED, because "there is nothing to do" is the claim a
session is most likely to make lazily:
  THE BINS, his first, are DONE and the fog hypothesis is refuted. Removing fog
    moves a bin by 2 to 8 percent, so a better texture is still the item.
  WETNESS, his second and "the term owed", is LANDED at 0942cf1e under the
    07:55Z ruling and is UNRENDERED. It needs a frame, not more code.
  THE DUSK FRAME, his third and the picture he judges by, IS a frame.
  QUEUE 300, the only visual item that looked startable, is explicitly BEHIND
    QUEUE 299 in its own status, and the order is deliberate in its own words:
    "299 lands, the frame is looked at, and THEN this item is re-scoped against
    what is left". 299 landed last night. THE FRAME HAS NOT BEEN LOOKED AT,
    because the frame is run 45.
  QUEUE 309 is ordered AFTER the first wet frame by the ruling that filed it.
  QUEUES 310 and 311 are instrument work, which is studio and not game, and his
    standing rule puts two thirds of the week's spend on the game.

SO THE VISUAL LANE IS NOT SLOW, IT IS STOPPED, and it is stopped at exactly one
point: a queued job on a runner that is not claiming. Run 45 has been queued
129 minutes at 08:25Z and tools/landed.py --contains reads "not yet" for both
e1d1981 and 0942cf1, over 362 runs known.

THIS IS RULE 13's GENUINE BLOCKER AND NOT AN IDLE ENDING. A watcher is armed
rather than a queue item started, because starting one would mean working on
the studio while the game waits, which is the thing his two thirds rule exists
to stop, and because the budget reading behind this session is four hours old
and has been spent against hard.

WHAT A RETURNING RUNNER CHANGES, so nobody has to work it out under time
pressure: run 45 checks out cb0c55a2 by its own push event, so if the landed
run's commit CONTAINS 0942cf1e it rendered WET and his 0.85 dry re-read was
never taken. That is the sentence the Producer owes him, and it is not
something he should have to infer from looking at a wet road.

## 2026-09-15 08:15Z: WETNESS IS LANDED AND UNRENDERED, AND A SECOND ERROR OF MINE IS IN IT

THE BATCH IS COMMITTED UNDER THE 07:55Z RULING and NOTHING IN IT HAS BEEN SEEN
BY A RENDERER. The builder said so itself and it is repeated here because a
landed batch reads like a finished one: the arithmetic is proven under g++, the
generator's set-site guard was watched red before the call site existed and
green after, and NEITHER OF THOSE IS A PIXEL. The frame claim, a darker and
shinier road, is not made by anyone yet.

RUN 45 STAYS QUEUED AND IS NOT RE-DISPATCHED. WHICH RUN RENDERS THIS BATCH IS
SETTLED BY ANCESTRY AND NOT BY ANYBODY'S EXPECTATION, which is section 9 of the
ruling and is the half most likely to be got wrong in a hurry: the workflow
checks out with no explicit ref, which takes the run's own sha, but ci.md
records a runner here checking out the branch tip at start. So if the landed
run's commit CONTAINS this batch, RUN 45 RENDERED WET and the dry walk-back
re-read Jafar asked for was never taken, and the Producer says that in one
sentence rather than letting him read a wet road as an answer about his 0.85.

THE FIRST WET FRAME IS READ IN SECTION 9's ORDER, FRAME FIRST, and the
precondition comes before the wetness keys: materialConnections must read 19/19,
because a short Alpha means every surface sat at the node's constant alpha of
0.5 and is not a wetness result at all, and a short B means wetter is rougher.
Then the wetness keys, then the four ground lines, and only then band.ground.p50
beside 0.2711, 0.5117 and the sheet's 0.373. NO PREDICTION OF p50 IS CARRIED and
that is deliberate for a second time: the albedo term darkens and the roughness
term reflects a brighter overcast sky and brightens, and a one-point model
cannot say which wins.

THE SECOND ERROR OF MINE TODAY, AND IT IS A PROCESS FAULT RATHER THAN A NUMBER.
I ran `git stash` to compile HEAD while the director was reading the tree. Six
of its reads landed on HEAD instead of the batch, which it noticed, discarded
and re-read, and it proved the batch was back by its own grep counts before
ruling. IT COULD HAVE RULED ON THE WRONG TREE AND STAMPED THE BATCH ANYWAY. The
rule it wrote for this seat is right and is recorded here so the next session
has it: A COMPARISON COMPILE OF HEAD GOES IN `git worktree add`, NEVER IN A
STASH OF THE TREE A REVIEWER IS READING. Both of today's errors are the same
root, a HEAD comparison taken carelessly, and the first was the -fsyntax-only
reading above.

WHAT THE RULING SETTLED, in one line each. The widening of the tint tool is a
widening and NOT a new instrument, so no retirement is spent or owed. Per
condition wetness needs NO NEW GLOBAL AND NO LIST, because the components
already hold the instances and GByName already holds the actors, with
ApplyCondition the owner and a write-on-change guard; that is queue 309 and it
is taken AFTER the first wet frame, not before. The exposure pin line is queue
310 and it is WORSE than I measured: the NOT-READ shape comes to about 794
against Buf[760], so the cap is reachable rather than latent and loses the tail
of the last key, cut mid-word. The footer's missing denominator is queue 311.
His 0.85 stays on the line with its date, and the re-read is HIS, on the first
wet frame.

## 2026-09-15 08:05Z: THE BATCH DID NOT INTRODUCE THAT WARNING. MY RULER DID.

WHAT I TOLD THE DIRECTOR AS MEASURED FACT: that the wetness batch introduces a
-Wformat-truncation warning absent at HEAD, and that something the builder
changed must have widened the compiler's estimate.

WHAT WAS ACTUALLY WRONG: I measured HEAD with `g++ -fsyntax-only`.
-Wformat-truncation is a CODE GENERATION warning and cannot fire under a flag
that skips code generation. My "zero occurrences at HEAD" was an artifact of my
own flag and not a fact about HEAD. Rule 3 names this exact move, suspect the
instrument before the reading, and I did not make it.

RE-MEASURED PROPERLY, stashed tree at -O1 with code generation on: ONE
occurrence at HEAD, same directive, the same 511-byte figure, at
VignetteSpec.h:3081. The batch adds fourteen comment lines above that snprintf,
so the identical warning now reports at 3095. A line-number-sensitive reading
calls that new. It is not new.

THE BUILDER CAUGHT IT FIRST AND INDEPENDENTLY, having built four variants in a
scratchpad without touching the tree, and it was right. It also corrected three
other things in the brief I gave it, and EVERY ONE I COULD CHECK WAS RIGHT:
  the Wetness field sits at VignetteSpec.h 257/284/497, not the 246/248/434 my
    brief asserted;
  "read by nothing" was already stale when the queue wrote it, since
    vignette-spec-test.cpp reads C.Wetness in eight places; the true and
    narrower claim is that no read site existed in VignetteShot.cpp;
  two comments in make_base_material.py state the connection denominator as 16
    where the figure after this change is 19, confirmed at lines 3261 and 3340,
    both left over from last night's AlbedoGrade batch.

WHAT SURVIVES OF THE FINDING, because the measurement was right even though the
conclusion was wrong: the emitted verdict lines are 733 and 738 bytes into a
char Buf[760]. Twenty two bytes of headroom at worst, on a line that loses its
trailing keys silently past it. That is a real latent cap in ExposurePinFields,
it PREDATES this work, and it is its own item rather than a condition of this
batch landing or something quietly folded into it.

AND TOMORROW'S BRIEF OWES THIS, under the line he asked for on 2026-09-15:
what we got wrong and corrected, in one sentence.

## 2026-09-15 07:57Z: HE HAS BEEN TOLD, AND THE SEND ITSELF NARROWED THE DIAGNOSIS TO THE SERVICE

THE RECEIPT, which is the EFFECT and not the commit going green:
  production/outbound/2026-09-15-your-desktop-stopped-taking-work.unprompted
  .receipt.txt, on pc-inbox head 634da649, reads receipt=sent
  fileCommit=2c28f18e01b852f1cd689c1cb50f1f3249e9fddd
  sent=2026-09-15T07:41:27+00:00 messageId=102 chars=772
  outboundLatencySec=187 from fileCommitInstant to sendInstant. The
  fileCommit matches what was pushed, so the text he has is the text that
  was reviewed.

AND THE SEND IS THE MEASUREMENT NOTHING ELSE COULD TAKE. Within one hundred
and eighty seven seconds of a push to main, HIS MACHINE pulled it, resynced
its checkout, swept the outbox, reached Telegram, and pushed a receipt back.
That is four things working on the machine whose runner has left a job queued
for eighty five minutes.

SO THREE OF THE FOUR CANDIDATES ARE ELIMINATED BY MEASUREMENT RATHER THAN BY
ARGUMENT. Asleep is out, signed out is out, taken back for his own use is out.
What is left is the self-hosted service itself: stopped, crashed,
deregistered, or connected to nothing. WHICH of those is still not
established and still must not be guessed at, but the class is now one
instead of four, and it was the message going out that settled it.

NO SECOND MESSAGE TODAY, AND THAT IS HIS OWN RULE APPLIED TO ITS OWN EXAMPLE.
He ruled one message a day on 2026-09-15 after a night of seven, with two
exceptions, a card he must answer and something genuinely blocking, and the
words he used were "A render landing, a correction, and a frame are not three
messages; they are one brief tomorrow morning". This is a correction to a
diagnosis. The ask, the recommendation and the deadline are all unchanged: he
goes and looks at the desktop either way. It goes in tomorrow's brief, or into
an answer if he taps, because an answer to his tap is a different register and
not a second unprompted message.

THE RISK THIS CARRIES, NAMED RATHER THAN LEFT IMPLIED, and it belongs in
tomorrow's brief: the message told him his desktop stopped taking work, and
when he looks he will find a machine that appears perfectly healthy. If he
replies, the answer says the helper that takes work is the part that stopped
and that everything else on that machine is fine.

RUN 45 IS STILL QUEUED at 07:57Z. tools/landed.py --contains e1d19817 reads
"not yet: no run contains e1d1981. 362 run(s) known, newest cb4767e". Watch by
ancestry, never by branch movement. DO NOT RE-DISPATCH.

## 2026-09-15 07:15Z: RUN 45 IS QUEUED AND HAS NEVER STARTED. THE RUNNER IS NOT TAKING JOBS.

MEASURED, NOT INFERRED, off the Actions API and two branches, all read at
07:15Z:
  run 45 (LEDGER Unreal probe, id 34936220494) status=QUEUED, created
    2026-09-15T06:16:37Z, updated 06:16:37Z, run_started_at equal to created.
    Fifty nine minutes with no update and no start.
  THE CONTROL, AND IT IS THE READING THAT MATTERS. The SAME push produced two
    runs at the SAME instant 06:16:37Z on the SAME commit cb0c55a2:
    publish-glance, which runs on a GitHub-hosted runner, COMPLETED SUCCESS;
    the probe, which runs on [self-hosted, ledger-pc], never started. Actions
    is not degraded and the queue is not stuck. It is that label.
  the workflow holds NO concurrency group, and the probe-unreal job carries no
    needs and no if. Nothing but a runner can be holding it. (Checked because
    a held group looks exactly like an absent runner from here.)
  run 44, the SAME workflow on the SAME runner, went created 02:12:27Z to
    completed 02:18:53Z. Six and a half minutes.
  the runner LAST CLAIMED A JOB at 03:33:09Z: ledger-install-supervisor-task
    on e7564eb5, completed success. Run 45 is the first self-hosted job
    dispatched since, so the window in which it stopped claiming is 03:33Z to
    06:16Z and cannot be narrowed from here.
  THE MACHINE WAS ALIVE AT 04:47Z, inside that window. pc-inbox head f858854e
    is the bot on his PC pushing two reply receipts at 2026-09-15T04:47:20Z,
    one hour and fourteen minutes after the runner's last successful claim. So
    "the machine went off at 03:34" is refuted. Anything after 04:47Z is open.
  the last thing I ran on that machine CHANGED NOTHING, which is worth saying
    before he goes looking: the 03:33Z install printed installAction=
    already-correct, startedNow=refused reason=3_supervisor_process(es)_
    already_running, resyncAction=skipped-supervisor-running, exit 0.

A ZERO WITH ITS DENOMINATOR, because the other channel proves nothing here:
pc-results last moved 2026-09-11T06:18Z and the pc-watcher channel has been
silent four days. That silence is NOT evidence about the machine. Nothing has
been ASKED of it in those four days, so the denominator is zero requests and
zero answers is the expected reading. game-design/pc-jobs/request.json still
names fetch-the-vignette-surfaces / vignette-fetch-01, which pc-results shows
was RUN on 2026-09-11T06:01Z: the file is stale, not pending.

WHICH CHANNEL STILL REACHES HIM, BECAUSE THEY ARE NOT THE SAME CHANNEL AND
THIS IS THE DIFFERENCE BETWEEN TELLING HIM AND NOT. NOT A NEW FINDING, and
saying so is the point: the grade ruling of 05:43Z this morning already states
it in its own words, "outbox on the PC and needs no runner, where --send-brief
is a workflow" step. This is that ruling being USED rather than rediscovered.
  THE DAILY BRIEF CANNOT BE SENT. --send-brief has exactly one caller, a step
    of ledger-install-supervisor-task.yml, and that step runs on the runner
    that is not claiming. Queue 303 already names this; today is its second
    occurrence.
  THE OUTBOX CAN. tools/runner/telegram-bot.py sweeps production/outbox/ IN
    ITS OWN LOOP every 120 seconds (sweep_outbox, every=120), inside the bot
    process running on his machine. --send-outbox is a one-shot entry point
    for the same work, not the only route. So a message placed in the outbox
    does NOT ride the runner.
  AND THE BOT'S LOOP WAS ALIVE AT 04:47Z, which is what the two reply receipts
    on pc-inbox are. It has not been proven alive since, and nothing has been
    placed in the outbox since, so the denominator is zero and silence there
    means nothing. COMMITTING THE MESSAGE IS THE TEST, and the receipt landing
    on pc-inbox is its EFFECT, which is the thing to verify rather than the
    commit going green.
  THE ONE FILE THAT WOULD SETTLE IT IS UNREADABLE FROM HERE, and that is worth
    filing rather than rediscovering: the bot writes botSweepPasses,
    botUptimeSec and botSweepWrittenAt to game-design/pc-jobs/bot-sweep.txt,
    in an UNTRACKED directory, pushed by nothing. It reaches this side only
    when a step on the self-hosted runner copies it out. The one instrument
    that says "the machine is up, the service is not" is invisible in exactly
    the situation it exists for. Filed as queue 308.

SO THE ledger-pc RUNNER IS NOT CLAIMING JOBS. WHY is NOT diagnosed and must
not be guessed at: asleep, the runner service stopped, signed out, and a
machine taken back for his own use are all consistent with what is measured,
and only his machine can say which. What IS established is that a queued job
with no runner is not a slow job, and that it is the self-hosted half and not
Actions.

THIS IS A GENUINE BLOCKER AND IT STOPS THE VISUAL SLICE. Run 45 is the re-read
he ordered in his own words. Nothing in the container can start it, nothing
can be learned by waiting, and DO NOT RE-DISPATCH: a second queued job behind
a runner that is not claiming would prove nothing and would confuse the
ancestry check when the runner returns.

THE PRECEDENT IS WHY THIS GOES TO HIM NOW RATHER THAN WAITING. Queue 291
records a SIXTY ONE HOUR gap, 2026-09-11 09:04 to 2026-09-14 17:47, in which
this same runner took no job and nobody noticed; the briefs of the 12th and
13th were lost to it. His standing rule since 2026-09-15 is one message a day
with two exceptions, a card he must answer and something genuinely blocking,
and both must say so in their first line. This is the second.

WHEN THE RUNNER RETURNS: run 45 should claim and complete on its own, because
the job is queued and not cancelled. Check by ancestry that the landed verdict
CONTAINS e1d19817, then read it in the ruling's section 11 order, FRAME FIRST,
quoting no prediction.

## 2026-09-15 06:10Z: THE BATCH IS REVIEWED AND LANDS, ONE STATEMENT BACK WITH THE DIRECTOR

LANDED UNDER THE RULING OF 05:43Z (game-design/decision-2026-09-15-ruling-the-
forty-are-waived-by-name-and-the-walk-back-stands-as-his-number.md): queue 299
(his 0.85 walk-back, a strength from white in gamma, one call site), D40 (the
sky is a photograph; the batch binds none and says so), and queues 256 and 259
(the site links moved, the served marker written from a watched run, the link
floor live again with the forty waived by name).

ONE CONDITION OF THAT RULING IS NOT APPLIED AND IS BACK WITH THE DIRECTOR. Its
dictated item 1 replaced the research ladder's raw-difference count with a
by-rule-name count; measured, it took researchVerbatimWaiverBit from 5/10 to
0/10 AND the register selftest from 163/0 to 10 failed. The ruling's own
condition was "equal, or the line is reverted and the inequality is reported as
a finding", so it is reverted and reported. DO NOT INVENT A THIRD VERSION. The
open question is whether the statement reads the wrong side of the ladder, or
whether 0/10 is the true by-rule-name reading and 5/10 has been the artefact
all along, which would make the fault larger than the ruling states.

RUN 45 IS THE NEXT DISPATCH and it is the re-read Jafar asked for. Read it in
the ruling's section 11 order, FRAME FIRST.

THE BRIEF CARRIES NO PREDICTED p50, AND THIS OVERRIDES THE EARLIER PLAN. The
0.368 that an earlier wake told the Producer to carry is WITHDRAWN: the
resident's exponent was fitted on two gamma-byte ratios and applied to a linear
ratio, and applied consistently the three candidate readings give 0.313, 0.305
and 0.299, inside what a one-point model can resolve. The brief names the
reading taken and the two alternatives in one sentence and quotes no
prediction; run 45 prints the measured number.

QUEUES FILED BY THE RULING: 306 (the provenance guard's rejecting fixtures have
never run) and 307 (three frozen name lists grade an archive, and the fourth is
the line). Filed by the resident: 305 (cards.py --selftest has been red and
outside the gate since 2026-09-10, and nobody has counted how many other tool
selftests verify does not run).

## 2026-09-15 04:05Z: NOTHING IS IN FLIGHT AND TWO QUESTIONS ARE WITH JAFAR

IN FLIGHT: nothing. Run 44 landed on 17710df and was read in the ruling's
section 10 order. Both builders and the director are finished and their work
is committed and pushed.

THE BRIEF REACHED HIM AT 03:34:08Z as messageId 99, with BOTH BUTTONS and the
PICTURE carried (game-design/sim-shots/grade_three_way.jpg, three panels: his
Hook sheet, the street before, the street after). briefsSentEver moved 2 to 4
across the night. That is queue 291's acceptance met on the live path and the
item CLOSES.

WHAT HE WAS ASKED, and until he answers the visual slice does not move:
  ONE, the D23 question: the bottom frame beside his sheet, which way does the
  gap run. Measured it is darker (ground median 0.271 against his 0.373) but
  his eye rules and no number was asked for. Default: nothing moves.
  TWO, the sky: does the overcast photograph become the sky, or does the built
  sky stay. Staging the photograph moves no pixel on its own and using it
  overturns the reasoned position at VignetteShot.cpp 163 to 173, so it is his
  and not a director's. Default: keep the built sky.
Both deadlines 2026-09-18.

WHAT LANDED TONIGHT: the albedo grade (299) with run 44 proving it reached the
frame; the brief path's three fixes and the outbox retirement (291), both
halves proven live; the ruling of 00:52Z; queues 300 to 303 filed.

WHAT IS UNBLOCKED IF WORK RESUMES BEFORE HE ANSWERS: queue 293 (retire the read
series, and with it the whole-run grade tally and the AlbedoGrade readback the
ruling deferred there so the monthly instrument rule is paid in the batch it is
measured in) and queue 303 (a day input on the existing send step, so a brief
that misses its day by more than one run can be sent at all). Queue 302 is
BLOCKED and its block was NOT spent: the trim reading was written, measured and
withdrawn, because the sills and lintels project at a median of 5.1 pixels
through cam_hook and that camera cannot answer the question. Queue 300 changed
shape: the bins are now the brightest thing in the street at 177.6 to 200.0
against a ground median of 69.1, the grade barely moved them (0.884), and a
distance-and-fog explanation is recorded there as a HYPOTHESIS WITH ITS TEST
NAMED AND NOT RUN. Do not start a sourcing round on that item until the
distance term is measured.

BUDGET IS UNMEASURED FROM HERE. The last reading is 25/25 at about 20:0xZ on
2026-09-14, inside 48 hours so it is not a stop, but a night of two builders, a
director and a Producer has run since and none of it is counted. The ceiling is
85 on the governing meter and where the meter actually sits is not known.

## 2026-09-15 02:05Z: THE GRADE IS COMMITTED AND RUN 44 IS WHETHER IT REACHED A FRAME

IN FLIGHT: run 44, dispatched on af6700cb, the sha captured BEFORE the
dispatch and watched by ancestry. Do not re-dispatch. Predictions are written
into production/d1-probe/DISPATCH before the run, eight of them, one written
to fail on purpose: that full parity lands band.ground.p50 BELOW the Hook
sheet's 0.373. The reading order is the ruling's section 10 and it opens with
THE FRAME, not a gate.

LANDED: af6700cb, the batch of queue 299 and 291 under the ruling of 00:52Z
(game-design/decision-2026-09-15-ruling-the-grade-lands-as-the-legacy-number-
and-the-outbox-brief-was-never-a-net.md). 33 paths, 15 of them code.
M_LedgerSurface has the AlbedoGrade vector parameter the legacy build's grade
had nowhere to land in; the brief sender recovers a day it missed, says so
when it finds nothing, and reads receipts from both branches they land on;
the outbox brief register is retired on a record of zero catches and two
duplicates. Suites: 447/447, 149, 57 (1 not measured and named), 19, 119, 28.

WHAT IS NEXT, in Jafar's order: materials LANDED as far as the grade goes and
run 44 is its frame; then the sky itself; then the dusk frame. Queue 302 (the
ground family is a wetness list doing brightness duty) is BLOCKED on run 44's
frame and the block is spent by looking at the trim, nothing else. Queue 303
(the missed-day click) is ready and not blocking. Queue 300 (four near-flat
pack albedos on 411 of 610 pieces) waits on the same frame, because a darker
flat card may be quiet enough.

THREE THINGS ARE JAFAR'S AND NO DIRECTOR MAY TAKE THEM. The sky: staging the
HDRI moves no pixel and binding it overturns a reasoned position written at
VignetteShot.cpp:163-171, so it is a ruling and not a task. The residual after
run 44, because tonight's parity is PARTIAL (this side carries no wetness
term, queue 186) and the ruling refuses any sentence to him calling it full.
And whether to spend a retirement on the verdict key his no-new-instrument
rule cost queue 299; the tally and readback currently ride queue 293.

STILL OPEN FROM BEFORE: what "deterministic" means for D31 step 1, pixel
identical or within the measured floor. The card went with the frame, id 94.
D39's twenty recommendations still have 0 of 20 queue items filed, and D39
itself says which of the sixteen to file is HIS to decide, not a resident's.

## 2026-09-14 21:05Z: THE SKY IS APPLIED AND UNPROVEN, AND RUN 43 IS THE PROOF

IN FLIGHT: run 43, dispatched on the commit carrying Jafar's sky 0.70. THE
CHANGE IS COMMITTED AND NOTHING YET SHOWS IT REACHED A FRAME. The keys that
answer it are shotSkyIntensityAsked beside shotSkyIntensityRead on all nine
rows of the null group, which is checkable PER ROW because the sky has a
per-shot read and the fog does not. Predictions are written into
production/d1-probe/DISPATCH before the run so no reading can be explained
afterwards. Do not re-dispatch; watch by ancestry.

LANDED TONIGHT, newest first: d6e21c1e sky 0.70 with the reference-cell role
moved to grid_sky070_sun003; b5fddb10 the four structural defences and three
research claims checked; 97b460f7 the judged frame to Jafar; 689d6938 the fog
series across the bracket; 622bc390 the fog cap at 0.100.

THE OPEN DECISION IS HIS AND NOT A DIRECTOR'S: what "deterministic" means for
D31 step 1, pixel-identical or within the measured floor. The card went with
the frame, id 94. Until he rules, nothing is pinned and nothing is judged.

WHAT IS NEXT, in his order: materials (queue 181, blocked behind 180 and he
must unblock it, not a resident), then the sky itself (286), then the dusk
frame. D39's twenty recommendations have 0 of 20 queue items; 16 need filing.

TWO CORRECTIONS THIS SESSION OWES ITS OWN RECORD. Queue 291's cause was wrong:
the brief path was never broken, it has a caller at
.github/workflows/ledger-install-supervisor-task.yml:683 and sent id 95 with
buttons 2/2. A grep's own exclusion filter deleted the caller because the
caller names the callee. The real defect is narrower: --send-brief keys on
TODAY in UTC, so a brief that misses its day is unreachable afterwards, and
exit 6 is continue-on-error so the miss is silent. And queue 295: cards.py
--selftest is red on main and is not among verify.py's ten TOOL_SELFTESTS rows,
so no commit has ever run it.

## 2026-09-14 14:15Z: THE LEAK LANDS, THE WEEK OPENS, AND THREE OF MY CONCLUSIONS WERE WRONG

LANDED AS 04e3cea4 ON MAIN, 46 paths, verified by ancestry rather than by the
push message. Two CI commits (the bot restart and the windowless proof) landed
while the batch was being built, so it was rebased onto them rather than forced.

THE EXPOSURE FAULT WAS A LEAKED OVERRIDE, not the snapped rate and not the
missing pin. The camera actor is spawned once and moved; the two AutoExposure
override flags were written only when a condition ASKED for a pin, so they
persisted. Run 41: four rows of 37 ask 0.0000 and read 0.0300, 0.3000, 3.0000,
10.0000 with overrides=1/1, printed AUTO. One condition at three mean lumas.
THE VALUE WAS ON THE LINE ALL ALONG. Probe suites 393/393 and 113/113.

WHAT THE COMMIT DOES NOT DO: it does not make the rig deterministic.
rigDeterminism is EXPECTED to still read DIFFERS because vign_camA_day is
unpinned. The reading that proves the fix is expPinRowsLeaked=0 over the rows
that could have leaked. Do not report that line as this fix failing.

THREE WRONG CONCLUSIONS, MINE, EACH CAUGHT BY SOMETHING ELSE, and the pattern
is the finding: every time I measured ONE instrument and generalised I was
wrong; every time I opened the artifact I was right.

  1  cmd-window loop blamed on RestartCount=999/PT1M   refuted by a verifier
  2  273's guard pair called mutually unsatisfiable    refuted by a director:
     --ahead-of-run exists and THE FAILING CHECK PRINTED IT three lines on
  3  pin batch reported as landing on 4355/4355        refuted by the gate:
     that is the C# suite; the UE probe suite read 391/393

WHAT IS OPEN AND WHO OWNS IT

  274  WHICH CONDITIONS MAY ASK FOR A PIN. An invariant says ladder rungs only
       ("a row pinned by accident would be photographed at an exposure nobody
       chose"); the builder's scene pins 25 of 27. Both defensible, code cannot
       hold both. DIRECTOR'S CALL, Core and spec. Blocks step 1's render.
  275  182 of 267 queue items closed under an archiving commit with no ruling.
       Queue 138, the crime loop, is among them and is the milestone Jafar
       named today as the one to protect. HIS CALL.
  273  the ahead_of_unity_run key can never be spent: its anchor is the newest
       LANDED UNITY RUN and D16 made the engine Unreal, so none will ever land.

THE FIVE RESEARCH DELIVERIES ARE STAGED AND NOT SENT, in
production/outbox-blocked/. All five exceed the 4096 wire cap (5300 to 6221
bytes) and nothing in the sweep splits, so sending them would have been a
refusal retrying every two minutes for ever. Jafar asked for them "in full, as
its own message"; those cannot both hold and the choice is his. NOTHING IN THEM
HAS BEEN ACTED ON, per his rule.

THE CHANNEL IS BACK. Runner picked up a job at 13:23:05Z, bot pushed a receipt
at 13:23:30Z. Last brief he actually received: 2026-09-10, messageId 63. Three
mornings missing, not two. The sending task was disabled 2026-09-11T07:59:54
and the installer deliberately never re-enables what a person turned off. It
now reads taskEnabled=True taskState=Running with five daemons; by what act is
NOT measured.

RULED 14:12Z: every sun-on condition carries the pin (B); the batch lands as one
commit; the step 1 render is dispatched after it and reads expPinRowsLeaked=0/of=6,
rigDiffPixels on a pinned vign_camA_day, and the nine-id null series. Night stays
at auto; the pin is held at 0.300 through step 2. Step 2 (light and weather) does
not wait on either.

## 2026-09-14 04:09Z: THE FOURTH REFUSAL IS THE FIRST INFORMATIVE ONE, AND THE WINDOW IS LONGER THAN A DAY

THE 2026-09-14 BRIEF DOES NOT EXIST. Second consecutive day, said out loud
because the daily wake prompt names this exact hole and because two missing
days in a row is the shape the streak cannot distinguish from a quiet week.

THE FOURTH ATTEMPT WAS THE DAILY WAKE'S TO MAKE and it made it. Yesterday's
record ended "THE NEXT MOVE BELONGS TO THE DAILY WAKE AT 04:00Z OR TO JAFAR",
so this is the armed move rather than a session deciding in the moment to try
once more. The wake fired at 04:06:59Z, the Producer was dispatched on its
ruled model with the gathered dossier, and it refused at 04:08:58Z with the
same HTTP 429 and the same wording as the other three.

    04:16Z 13 Sep   first attempt, on the daily wake
    07:19Z 13 Sep   +3h03m
    13:21Z 13 Sep   +6h02m
    04:08Z 14 Sep   +14h47m,  23h52m across the series

WHAT THIS POINT BOUGHT, AND IT IS THE FIRST ONE THAT BOUGHT ANYTHING. The
three points yesterday established only "longer than nine hours", which was
compatible with a rolling window that would clear overnight. It did not clear
overnight. The window is now known to be longer than 23h52m, which RULES OUT
the short rolling window and leaves a cap measured in days. That is a change
of conclusion, not another tally mark, and it is the reason the fourth attempt
was worth making when a fourth point at three hours would not have been.

STILL NOT KNOWN AND STILL NOT TO BE GUESSED: no notice in the series has ever
carried a reset instant, so nothing here says WHICH cap. Rule 13 says parse
the reset from the notice and arm for it; the notice carries none for the
fourth time, and that absence is recorded rather than a number being invented
to fill it.

NOTHING EXTRA IS ARMED, AND THAT IS THE TEST. The last weekly reset this file
records was 2026-09-08, so the daily wake at 04:00Z tomorrow lands near where
a weekly cap would clear and tests that hypothesis for free. A retry sooner
would spend a spawn to learn less. The hourly tick keeps watching the inbox
and the runner, which costs nothing.

WHAT I DID NOT DO, FOR THE FOURTH TIME. I did not re-spawn the Producer on
another model. The routing table was ruled 2026-09-10 and is enforced rather
than advisory; the studio-director who could rule otherwise is the other Fable
role and is unavailable with it. The cost of holding that line is now two of
his mornings rather than one, and that is the trade queue 272 asks him to rule
on. It is worth saying plainly that the line held four times is starting to
look less like discipline and more like the deadlock reporting itself.

THE BUDGET READING WENT STALE DURING THIS, AND THAT IS RETRACTED AS OF
2026-09-14T18:45Z. The paragraph above said "the newest row is 2026-09-11",
that the reading was past the 48 hour bound, and that the studio was therefore
held to work costing no model time. All three were true when written and all
three are now false. production/budget.md row 43 is dated 2026-09-14 and reads
2 per cent total and 0 per cent Fable, reported by Jafar at about 13:0xZ
opening the visual-slice week, and that row records the weekly limit resetting,
which voids every rate computed before it. The hold is lifted and the ceiling
is 85 on the governing meter, standing.

THE RUNNER IS BACK, WHICH THE NEXT PARAGRAPH ALSO PREDATES. It was dark from
2026-09-11 until today; the Unreal probe then ran to success on Jafar's PC at
2026-09-14T14:53Z on commit 32bae70, which is the run every fog reading in
today's work is taken from. Anything below written on the assumption that the
channel is down describes 11 to 13 September and not now.

WHAT WOULD HAVE HAPPENED IF THE BRIEF HAD BEEN WRITTEN, because it changes who
is waiting on whom. The sender is the bot on his PC, not the self hosted
runner: tools/runner/telegram-bot.py imports tools/runner/brief.py, and the
runner has been dark since 2026-09-11T08:18. So a written brief did not need
the runner. Whether it would have reached him is UNDETERMINED: pc-inbox last
moved 2026-09-13T03:14 with the two receipts for message 79, and a bot with
nothing to say pushes exactly as little as a bot that has stopped. That is a
missing denominator, not a diagnosis, and it is not worth a spawn to settle
while nothing can be written to send.

THE THREE SMALL THINGS WAITING ON HIM are unchanged and are now a day older:
restart the bot so it stops quoting the ceiling he repealed, start ledger-pc,
and read two figures off his usage page. The first has had a question open on
his phone since 01:14Z on 2026-09-13, which is now over a day.

## 2026-09-13 13:25Z: THREE REFUSALS ACROSS NINE HOURS, AND THE BRIEF IS THE FINDING

NO FOURTH ATTEMPT, BY THE RULE ARMED WITH THE THIRD. Fable refused the Producer
three times today, the same HTTP 429 and the same wording each time:

    04:16Z   first attempt, on the daily wake
    07:19Z   +3h03m
    13:21Z   +6h02m,  9h05m across the series

NOT ONE NOTICE CARRIED A RESET INSTANT. Three points, widening spacing, and
still no information about the window beyond "longer than nine hours". Whether
this is a rolling window that clears tonight or a weekly cap that does not is
STILL the thing not to guess at, and a fourth attempt on the same shape would
buy a fourth point and no more. The rule to stop was written at 07:22Z, before
this refusal, precisely so that stopping would not be a judgment made in the
moment by a session that wanted to keep trying.

THE 2026-09-13 BRIEF DOES NOT EXIST AND WILL NOT BE WRITTEN TODAY BY THIS
SESSION. That is the finding, stated as one rather than left to look like a
quiet day, which is the hole the daily wake prompt names in its own words.
Every other day this file records what the studio did; today it records that
the one message a day did not get written and why.

WHAT IT WAS GOING TO SAY IS NOT LOST, and that matters more than the brief
file. It is written three times over: in the wake record of 04:00Z, in the
07:18Z resume, and in the 13:21Z one, each carrying the same three items in
the same order. The first of those is the one that costs him something: his
bot has had a budget question open on his phone since 01:14Z and the bot
answering it carries the ceiling he repealed, so it will tell him he is OVER
when he is UNDER, wrong in the direction that stops work, until it is
restarted. That is now sixteen hours old and nobody has told him.

QUEUE 272 IS NO LONGER THEORETICAL. budget.md rule 1 says that at the ceiling
the studio writes the brief and stops. Today the ceiling was reached ON THE
METER THE BRIEF NEEDS, so the rule's required action was unavailable at exactly
the moment the rule fired, three times. The studio-director is the other Fable
definition, so the review gate was gone with it: tier 3 could still build and
nothing could land. That is the deadlock 272 describes, now with a date and
three timestamps against it.

WHAT I DID NOT DO, THREE TIMES. I did not re-spawn the Producer on another
model. The four-tier routing table was ruled 2026-09-10 and is enforced rather
than advisory, and a resident swapping a model for a ruled role at the moment
the rule bites is how a ruled table quietly becomes a suggestion. That call is
Jafar's or a director's. It is worth saying plainly that the cost of holding
that line today was his morning message, and that this is the trade 272 asks
him to rule on rather than one a session should keep making by default.

THE NEXT MOVE BELONGS TO THE DAILY WAKE AT 04:00Z OR TO JAFAR. Nothing further
is armed for the brief. The hourly tick keeps watching the inbox and the
runner, which is free.

## 2026-09-13 04:20Z: THE FABLE METER IS SPENT, AND THE STOP RULE NEEDS IT

THE 2026-09-13 BRIEF DOES NOT EXIST AND THAT IS A FINDING, SAID OUT LOUD
because the daily wake prompt names this exact hole: "on a day this wake fires,
a brief file for that day must EXIST. Its absence currently looks identical to
a quiet day." It is not a quiet day. The Producer turn died mid-read at 04:16Z
on an API refusal, quoted whole because its wording is the evidence:

    You've reached your Fable limit. Switch to another model, or manage usage
    credits ... (error type rate_limit, HTTP 429, model sent to the API:
    claude-fable-5-1)

NO RESET INSTANT WAS GIVEN. Rule 13 says to parse the reset from the notice
and arm for it; this notice carries none, so the resume is armed on an
interval and that fact is recorded rather than a reset being invented.

WHAT THIS MEANS UNDER THE BUDGET RULE, AND IT IS A DEADLOCK. budget.md rule 1:
"EITHER METER at or above 85 percent: STOP. Write the brief, push, and do
nothing further until Jafar gives a new number." Fable is at its hard limit,
so rule 1 fires, and rule 1's required action is to write the brief. The brief
is the Producer's alone, ruled 2026-09-03, and the Producer is one of exactly
two Fable definitions; the other is the studio-director. So the stop rule
requires the spent meter to perform the stop, and the review gate is spent
alongside it. Filed as queue 272 with the options laid out rather than one
improvised here.

WHAT IS STILL POSSIBLE AND WHAT IS NOT. Tier 3 builders are Opus and could
still run, so the studio can BUILD and cannot REVIEW, which means it could
produce work it is forbidden to land. That is a reason to stop rather than a
reason to keep going, and the last reading, 78 total and 82 Fable, was already
three points under a ceiling the Fable side has now reached.

WHAT I DID NOT DO, DELIBERATELY. I did not re-spawn the Producer on another
model. The four-tier routing table was ruled 2026-09-10 and is enforced rather
than advisory, and a resident swapping a model for a ruled role at the moment
the rule bites is how a ruled table quietly becomes a suggestion. That call is
Jafar's or a director's, and the director is the other unavailable thing.

THE SERIES, SO FAR TWO POINTS, because one refusal is an event and two are the
start of a shape. Fable was refused at 04:16Z and refused again at 07:19Z on
the retry, the same HTTP 429 and the same wording both times, three hours and
three minutes apart. NEITHER NOTICE CARRIED A RESET INSTANT. So what is known
is that the window is longer than three hours and nothing more; it is NOT known
whether this is a rolling window that will clear today or a weekly cap that
will not, and a session that assumes either has invented the number. The next
check is armed six hours out rather than three, which is a wider spacing chosen
because a three-hour point has already been spent and a second one would tell
us the same thing. If that is refused too, the honest reading becomes that the
2026-09-13 brief may not be writable today at all, and THAT is the finding to
record rather than a fourth attempt.

THE DAY'S WORK THAT DID LAND is two commits above: 0e522c1f and dc04da73. His
console is live and current for the first time since the move, measured by the
build requesting all four pages back and reading them at 200 with this
commit's own stamp. The brief that would have told him so is the one thing
that did not get written.

## 2026-09-13 03:55Z: SIX TRIGGERS COME HOME, THE CEILING HAS ONE HOME, THE NINETY ROWS SAY WHAT THEY ARE

The second half of the day's batch lands under
game-design/decision-2026-09-13-ruling-the-triggers-and-the-ceilings-home-batch.md.
269: publish-glance, citypack-inventory and citypack-fetch push on main
with their filters; ledger-build-mac, props-fetch and voice-candidates
are dispatch-only, each with its reason in its own YAML (voice-candidates
could trigger itself, and its ten dead-branch sites moved in one edit so
no push can create the old branch here). tools/workflow-branch-refs.py
reads the repository's own branch list and fails verify on a name it
does not have. 269 duplicated 254; both close on the served page reading
85 after this push's publish-glance run, which is also 256's step 1;
256's links are still 256. THIS PUSH ALSO FIRES citypack-inventory, and
a drifted catalogue lands as one CI commit on main: pull with rebase
before the next push. citypack-fetch is proven at mechanism level only
and its target tree is legacy under D16. 268 is CLOSED: the ceiling
pattern lives in tools/budget-ceiling.py, three importers, and
tools/budget-ceiling-check.py fails verify on zero lines, two lines, or
prose that disagrees (proseAt=44/46/117 today, the quotation at 46
counted on purpose). 267 points 3 and 4 landed: the ninety container
rows carry source=selftest-fixture, recognised by shape and span and
never by a missing key, because a reading he typed before 0e522c1f
lacks ceilingFrom= too; the PC copy is marked by the same tool when the
runner returns and closes 267. The marker's selftest runs in verify
(checks 83 to 84). New: 270 (tools_tracked cannot see a tool only
verify.py runs) and 271 (the branch check skips git continuation lines).
266 unchanged: open on the first PC row carrying ceilingFrom=.

AND ONE THING THE RESIDENT OWES THIS RECORD. 269 DUPLICATED 254, which had
been READY since 2026-09-10 and whose own filename says
`six-push-filters-name-a-dead-branch-and-one-would-resurrect-it`. The
resurrect hazard the 269 builder found was already written down. I filed 269
off a fresh measurement without grepping the queue for an item that already
covered it, which is the same fault as writing a threshold without reading
the series: the evidence was on disk and I went and re-derived it. The two
close together and nothing was lost but the filing, and the rule to take from
it is that a new queue item checks the queue first.

## 2026-09-13 03:00Z: THE BOT READS ITS CEILING, 266 IS LANDED NOT CLOSED, AND THE ORDER IS 269 THEN 268

The 266/267 batch lands under
game-design/decision-2026-09-13-ruling-the-ceiling-is-read-not-carried-batch.md.
The bot reads `Ceiling for LEDGER:` out of production/budget.md at each
verdict through glance.py's own pattern, refuses out loud with his two
numbers still in the chat when it cannot, names /budget in that refusal
because the question is already closed by then, and the selftest writes
nothing to the live log (90..90). 266 is LANDED and NOT CLOSED: it closes
on the first row in production/logs/telegram-budget.log on his PC carrying
ceilingFrom=production/budget.md, which needs the bot restarted on this
commit or later; until then the bot on his phone judges against 80, and
the daily brief says so. 267 landed points 1 and 2; 3 and 4 (mark the
ninety rows, print the denominator on read-back) ride with 268's builder.
268 is rewritten, not closed: the bot's suite now fails verify if the
machine line goes, and what remains is the pattern's shared home, the
document's exactly-one guard, and the pin out of the namespace. Two
readers of budget.md differ on purpose and both files now say so: glance
prefers a row's own sentence for the bar over that row, the bot reads the
standing line for a number typed now. Next dispatch cycle, one review:
269 (publish-glance re-pointed at main and proven by a run; the other
five decided per workflow under rule 9) and 268 plus 267's remainder.

## 2026-09-13 02:30Z: HIS BOT IS BACK UP, AND IT IS ASKING HIM A QUESTION IT WILL ANSWER WRONG

THE TWO DIRTY PATHS AT THE 02:03Z TICK WERE RECEIPTS, AND THEY IDENTIFY.
Every prior tick read `dirty: 0`. This one carried
`2026-09-13T011415Z-reply-78` and `...011416Z-reply-79`, both `kind:
bot-message`, 236 and 224 characters, sent one second apart at 01:14:15Z and
01:14:16Z. No inbound message on `pc-inbox` dated 09-12 or 09-13
(`52e5d509`: 0 message(s), 2 outbound record(s)), `briefTaps: onBranch=0`,
`rulings: onBranch=0`. Two acks with nothing recorded behind them.

I FIRST RECORDED THEM AS UNIDENTIFIABLE AND THAT WAS A MEASUREMENT FAULT,
not a hole in the record. I length-matched against the SOURCE LITERALS and
got `BUDGET_Q` 199 and `HELP` 647, neither of which matched, and I did not
measure `OPENING` at all. The constants interpolate `NUMERIC_PLACEHOLDER`, so
the literal in the file is not the string that is sent. Importing the module
and measuring the objects gives it exactly:

    OPENING   236   message 78
    BUDGET_Q  224   message 79

`run()` sends those two, in that order, at lines 1462 and 1464. So the
finding is not a gap. IT IS THAT THE BOT STARTED ON HIS PC AT
2026-09-13T01:14:15Z. Note also that `skip_backlog` FILES rather than drops
since the 2026-09-05 ruling, and it filed nothing, which agrees with the 0
messages on the branch: he sent nothing to a closed window. Nothing of his
was lost.

WHAT THAT DOES NOT ESTABLISH IS THAT IT IS STILL UP. The evidence is two
sends at 01:14Z and nothing since, and a bot with an empty inbox and an
unchanged outbox sends nothing, so a live bot polling quietly and a bot that
started and died look identical from here. The claim that holds is that it
started; anything stronger needs a fresh send or the PC.

THE RUNNER IS STILL OFF, and those are different machines' worth of news.
`pc-results` has not moved since 2026-09-11 08:18 and `pc-ops` still names
`70e9ac5`.

AND THE BOT BEING UP WOULD NOT RELEASE THE BRIEF ANYWAY, which is the
assumption a fresh session will otherwise make. `poll_forever` does sweep:
`flush_inbox` and `sweep_outbox` run every pass. But the 2026-09-12 brief is
in `production/briefs/` and NOT in `production/outbox/`, and the loop's own
comment says why the brief is not swept from there: "sent by `--send-brief`,
which is a one-shot and deliberately NOT swept from here: two senders on one
receipt race, and a duplicate of the one message a day is itself a channel
failure." That one-shot is a workflow step on the runner. The brief stays
queued until `ledger-pc` comes back, bot or no bot.

### What the bot is doing right now, and why it ranks

`run()` calls `ask_budget()`, which sets `pending = "total"` and sends
`BUDGET_Q`. The bot is sitting on his phone with the budget question open,
waiting for a number. The next thing he types goes through `budget_reading`.

`CEILING_PCT = 80` at `telegram-bot.py:130`. Jafar ruled 85 on 2026-09-10
(`budget.md:44`, `:90`). The comment at 125 says the constant moves with the
document and not before it; the document moved and the constant did not. Run
against his own last reading, 78 and 82:

    now:          fable at 82 percent, 2 point(s) OVER the 80 percent ceiling
    under the 85: fable at 82 percent, 3 point(s) under the 85 percent ceiling

Over by two against under by three. It does not print a stale number, it
REVERSES THE VERDICT, and the verdict decides whether the studio stops. This
is the identical wrong read Jafar corrected in me on 2026-09-11, when I
checked a stale header instead of the ruling sixty lines below it. My budget
sweep that day fixed six lines of `budget.md` and never reached the Python.
Filed as queue 266.

WHAT CANNOT BE FIXED FROM HERE: the running process. The default is bound when
the function is defined, so the bot now live on his PC keeps 80 until it is
restarted. If he answers before then, his reading is computed against 80 and
has to be re-read by hand.

### And the log he was told he could read back is ninety fixtures

`production/logs/telegram-budget.log`, the file `log_budget` describes as
"written where Jafar can read it back without the bot running":

    lines                                   90
    distinct value pairs                     2   (40/62 x30, 40/77 x60)
    readings he actually typed                0  of 90
    selftest runs that wrote it              30
    lines per selftest run                    3
    lines carrying ceilingPct=80             90  of 90

Three fixtures drive the real handler at line 1082 and so write the real log:
b4 (1994), b4b (2006/2031), b8 (2130). The clusters sit at 04:24, 04:31,
04:52, 08:06 and 12:07 on 09-12, which are my verify runs. The values are not
merely plausible, they are ordinary budget percentages, and sixty of the
ninety close on `headroomPct=3`, which reads as a studio three points off its
ceiling. Filed as queue 267. The daily wake prompt already says SELFTESTS DO
NOT COUNT; the same is owed to a log he opens.

### Pulling the thread found two more, and one is his console

RULE 1 SAYS GREP FOR THE SENTENCE, NOT THE SITE, so I swept every live copy of
the repealed 80 rather than fixing the one I had found. Two more were live.

`production/watchdog-prompt.md` lines 164 and 195 both told every scheduled
session "The ceiling is 80 percent on BOTH meters". That is the prompt that
fires on every wake, so every session since 2026-09-10 has been told the
repealed number. Both lines do also say `production/budget.md` is the
authority and this prompt is not, which is the mitigation and not an excuse:
stating a specific wrong number next to "the file wins" is precisely the trap
I fell into on 2026-09-11. Corrected in place, with the correction naming its
own staleness. The changelog entry at 288 keeps its 80 because it is history.

AND THEN THE INSTRUMENT ITSELF. `tools/glance.py:653` reads the ceiling with
`Ceiling for LEDGER:\s*(\d+)\s*%` over `production/budget.md`. That line was
not in the file. I deleted it at `1aedef87` on 2026-09-11, in the header
rewrite Jafar asked for in the words "one line nobody can misread": the
paragraphs that replaced it say 85 and are correct, and no tool can read one
of them. Measured before and after restoring it:

    before   ceilingPct=nothing-measured ceilingFrom=nothing-measured
             budget    NOTHING MEASURED | production/budget.md
             2 of 5 readings could not be taken (next, budget)
    after    ceilingPct=85 ceilingFrom=the-standing-line..2026-09-11
             1 of 5 readings could not be taken (next)

THE INSTRUMENT DID EVERYTHING RIGHT and that is the part worth keeping. It
printed `nothing-measured` rather than a number, named which of five readings
it could not take, went GREY and drew no bar, exactly as its own comment says
it must. It was right and unread for two days. The restored line carries a DO
NOT TIDY THIS AWAY paragraph naming glance.py:653 as the contract, which is a
comment and therefore the weak half; queue 268 was filed as the guard.

QUEUE 268'S PREMISE THEN LASTED TWO HOURS, which is worth recording because it
is the good direction for once. The builder's work on 266 put three cases into
the bot's suite that read the LIVE production/budget.md rather than a fixture,
and ledger/verify.py runs that suite at every commit, so deleting the
machine-readable line again now turns the commit gate red in the same session:
`accept/ceiling-is-read-from-the-live-document`,
`accept/ceiling-is-the-standing-85` and
`accept/the-prose-and-the-machine-line-agree`. 268 is rewritten and RENAMED to
what is actually left, which is smaller: a DUPLICATE is still owned by nobody,
because the bot deliberately accepts two lines that agree and refuses only two
that disagree, and the guarantee currently lives inside the Telegram bot's
selftest rather than beside the other document checks. A queue title asserting
something false while its body corrects it is the header-nearer-the-top fault
that produced this whole batch, so the title moved with the finding.

### And the console could not have republished anyway

Chasing who reads the glance produced the bigger finding. All 18 workflows
examined; SIX still carry a live push trigger on
`claude/game-dev-ai-automation-2h67ix`, the branch of the repository we left,
which does not exist here. This repository has four branches: `main`,
`art/atlas-01`, `pc-inbox`, `pc-results`.

    citypack-fetch  citypack-inventory  ledger-build-mac
    props-fetch     publish-glance      voice-candidates

Effect rather than inference, per `.claude/rules/ci.md`: `publish-glance.yml`
on `jsab258/ledger` returns `total_count 0, workflow_runs []`. It has never
run here. Of the repository's 40 runs, the 30 most recent are all workflows
WITHOUT the stale filter. A workflow that never triggers leaves no run, no log
and no red tick, which is why three days passed. All six keep
`workflow_dispatch`, so they look available rather than dead. Filed as 269.

So his console has not rebuilt since the move, and 268 and 269 are the same
fault twice: the instrument was not lying, it was not reached. Rule 4.

ALSO NOTED, NOT CHASED: `ledger-restart-telegram-bot.yml` exists and has run
on `main`. That is the mechanism for getting a fixed CEILING_PCT into the
running bot, and it dispatches to `ledger-pc`, which is off. It is the right
answer waiting on the same blocker as everything else.

### In flight

A tier 3 instrument-builder holds `tools/runner/telegram-bot.py` for 266 and
267 together, briefed not to commit. DO NOT EDIT THAT FILE until the diff is
reviewed. The ceiling is to be READ from `budget.md` rather than copied, with
a loud refusal and no silent fallback if it cannot be read, because a bot
that guesses a ceiling is the fault twice.

## 2026-09-12 04:30Z: THE BRIEF CARRIES A PICTURE, AND D18 HELD ONLY BECAUSE SOMEBODY LOOKED

THE WAKE RECORD'S TWO BLOCKS ARE CLEARED, measured rather than assumed, which is
what it asked for before anything was written:

    linkless brief at the real gate   linkFloorActive=false, linkfloor NOT enforced
    fleet on a stale checkout         messageId 77 sent 2026-09-11T14:22:27Z from
                                      ledger-migrate, receipt behind it

So the brief was writable for the first time since the 10th. It is 146 words,
passes the register at 0 findings over 8 rules, and it went out at 2ae59607 with
its sidecar and one composite picture.

I TWICE NEARLY SHIPPED THE WRONG PICTURE AND ONLY OPENING IT CAUGHT EITHER. The
third panel was captioned as our sheet beside theirs and showed only ours. I read
that as a misnamed file, fetched the outside sheet back off origin/art/atlas-01,
rebuilt the pair, OPENED IT, confirmed two proper halves, and stacked it into a
message bound for his phone. That picture carried children in school uniform and
a school nameplate. D18 forbids children rendered anywhere and queue 242 had
cropped exactly that half out two days before, measuring the gutter rather than
guessing the midline.

THE NAME MADE A DELIBERATE REMOVAL LOOK LIKE A BUG, AND I REVERTED IT. What
caught it was reading WHY the half was missing, one grep away before I built
anything and run after. A removal that does not say it was a removal is an
invitation. Queue 264.

THE PRODUCER CAUGHT THE SECOND ONE AND IT IS OWED THE CREDIT. I told it our
sheet reads as a worksheet, from heights, a gradient, colour codes and a
bookkeeping line I had seen on fairview_sheet_finished.png. The panel in today's
picture is fairview_sheet_short_s2.png, the raw output, which carries none of
them. It refused to write a caption contradicting the image it rides on, and
said so rather than dropping it quietly. It also refused to report a gate line
it could not see, having no shell by design, and hand-checked the text against
every rule instead.

D18 HAS NOW HELD THREE TIMES ON SOMEBODY HAPPENING TO LOOK, and the third is
still ahead rather than behind. The spec the studio is told to run next asks for
children in the POSITIVE half of its prompts:

    copper_row_weighhouse_lane      HITS: lads, pram
    copper_row_weighhouse_lane_s2   HITS: lads, pram
    copper_row_weighhouse_end       clean
    copper_row_weighhouse_end_s2    clean
    itemsWithChildTerms=2/4         negative names any child term: False

Its own note says why a negative cannot save it: a veto cannot summon, and "no
people" asks the model to push away the phrase and not the people. Queue 265,
which asks for a check that reads the prompts before the run and ships with the
two clean items as its accepting fixture.

THE FOUR CARDS ARE NOT WHERE THE RECORD SAYS AND I DID NOT INVENT THEM. It
points at the copper-row directory's DELIVERY for their recorded defaults; there
is no DELIVERY in that directory, and the `defaults` key in its JSON is prompt
settings. One of the four mints the Weighhouse into CANON, which is Jafar's to
approve and a director's to route. Left for a director with budget.

ONE CARD IN THE DECISION QUEUE LOOKS OVERTAKEN, named by the Producer rather
than passed on: the repository-shape question deadlined 2026-09-14 still parses
as WAITING and the round trip its default waits on has been proven since.

NO PICTURE HAS EVER GONE DOWN THIS CHANNEL: photos=0 over every receipt walked.
So this send is the accepting case for a path never once exercised, and the
acceptance test is the receipt and not the code.

AND IT HAS NOT SENT, BECAUSE HIS RUNNER IS OFFLINE. Diagnosed rather than
guessed, after 35 minutes of polling turned up nothing:

    workflow run 34673027827   event=push  head_sha=2ae59607
    created_at 04:27:00Z       updated_at 04:27:01Z      status pending
    pc-ops/supervisor-status.txt still names 70e9ac5 @ 2026-09-11
    pc-results unmoved since 2026-09-11 08:18

The trigger fired and nothing picked the job up. THE BRIEF SEND IS A ONE-SHOT
`--send-brief` RUN BY A WORKFLOW STEP ON THAT RUNNER, deliberately not in the
bot's poll loop (`telegram-bot.py` 625 and 1365), so waiting on the fleet cannot
send it. It goes by itself when his machine returns; nothing is lost and the
brief is not to be rewritten or resent.

I CONSIDERED A SECOND MESSAGE TELLING HIM AND DECIDED AGAINST IT. The regime is
one message a day and the brief is it. A message saying his machine is off is
also largely self-defeating: the path that would carry it is mostly the path
that needs him to fix the thing. So the record carries it instead and
`29f52423` is armed for 08:00Z to check the receipt.

e80f2b15 IS DISCHARGED ON THE WORK, NOT ON THE DELIVERY, and the distinction is
the whole point of that record: everything it specified is done, gated and
pushed, and the one thing left is a confirmation that only his machine can
produce. Recording it as delivered would be the 2026-09-09T04:09 fault it exists
to prevent.

STILL OFF AT 08:04Z, three hours thirty seven minutes after the push, checked
rather than assumed: no receipt on pc-inbox, pc-ops/supervisor-status.txt still
naming 70e9ac5 from 2026-09-11, pc-results unmoved since 2026-09-11 08:18. The
29f52423 check came due, found the receipt absent, and did what its own
instruction says to do with that: report it and re-arm rather than treat a
queued run as a sent message. 168f8b4d carried it to 12:00Z with one line added
that the first re-arm lacked: do not write a second brief for the same day,
because production/briefs/2026-09-12.md already exists and a wake day with a
brief file present is not a missing brief.

STILL OFF AT 12:04Z, SEVEN HOURS AFTER THE PUSH, measured a third time and
identical every time: no receipt, pc-ops naming 70e9ac5, pc-results unmoved.

THE THIRD RE-ARM IS DELIBERATELY LONG AND THAT IS THE ONLY NEW DECISION HERE.
86b37ffe is due 2026-09-13T04:00Z, riding the daily wake, instead of firing
again in four hours. Eight hourly ticks produced no new information, and each of
them ALREADY checks this receipt for free, so the send is caught within the hour
whenever his machine returns. The wake record is the durable backstop for a dead
session, not the primary watcher, and re-arming it every few hours was
generating commits that all said the same thing. It also carries what to do if
the runner is still off tomorrow: say it in the brief as a plain fact about his
machine, not as a studio failure, because nothing here can fix it.

## 2026-09-11 14:30Z: THE HOURLY TICK, BOTH JOBS DISCHARGED, NOTHING RESUMED

The trigger fired at 14:12:05Z while the batch was mid-flight and was read after
it landed. Both of its jobs are done and neither produced work:

    inbox-read   seen=2 delivered=0/2 alreadyHere=2/2, nothing new
    wake-queue   wakesDue=0/5, notYetDue=1/5 (e80f2b15, due 2026-09-12T04:00Z)

NO QUESTION FROM JAFAR IS OUTSTANDING. The tool also confirms both of today's
sends independently of the receipts: messageId=76 at 13:18:43Z (the executor's
no-cli note) and messageId=77 at 14:22:27Z with outboundLatencySec=125 (the
studio's answer).

NOTHING WAS RESUMED AND THAT IS DELIBERATE. Jafar's instruction was to report
what works and what does not and then stop, and the report is sent. The budget
stands at 78 total and 82 Fable against the standing 85, which is three points
on the governing meter. Next dispatch remains 261, then 262, 260, 256.

ONE FINDING FROM THE TICK, and it is a correction of my own first reading. The
inbox output was 90.6 percent one file's refusal records (494 of 545), which I
took for a live retry loop of the kind queue 260 describes. It is not: the file
left production/outbox/ at 7741eecd on 2026-09-09, so nothing is retrying and
these are historical records re-listed in full every run. Rule 3 again, and the
cheap check was `[ -f "$f" ]`. What IS live is that the listing has no cap while
the tool already carries a cap and a selftest for the message text, so the half
that floods is the half nobody bounded. Filed as production/queue/263.

## 2026-09-11 14:25Z: THE ANSWER REACHED HIS PHONE, AND THE RECEIPT NAMES THE COMMIT

The loop is now proven in the direction that matters, with this session's own
commit inside the evidence rather than beside it:

    commit    ce564254                                    14:20:22Z
    sent      messageId=77 chars=1660                     14:22:27Z
    receipt   production/outbound/2026-09-11-yes-it-works.answer.receipt.txt
              on pc-inbox, fileCommit=ce5642541a598977a5435022f3b603fb6b9cf650
    latency   125 s commit to send, ONE SAMPLE, not a rate

A RECEIPT AND NOT A REFUSAL is the whole point. The ruling's condition 8 said a
`refused-` record naming `linkfloor` would mean the PC's checkout or its copy of
the tool was behind this commit. It did not appear. So the sender on his machine
read `production/site-served.txt` in its own checkout, found `servedCommit=none`,
suspended the floor and sent a message carrying no link. Queue 259's item 2 is
proven end to end, by the only evidence that could prove it.

WHAT HE NOW HAS ON HIS PHONE, in order: the machine's automatic note at 13:18:43Z
saying the tool could not start, and the studio's considered answer at 14:22:27Z
explaining what that note meant. The second exists because the director refused
to let the first stand alone as "two contradictory answers on one phone".

NEXT DISPATCH IS 261 AND IT IS NOT DISPATCHED. Jafar asked to be told what works
and what does not and then for the session to stop, and the budget stands at 78
total and 82 Fable against the standing 85. The hourly inbox and resume trigger
is armed and NOW.md names the order: 261, 262, 260, 256.

## 2026-09-11 14:10Z: THE FLOOR IS CONDITIONAL, THE ORDER AGAINST 260 IS NARROWED, AND HE ALREADY HAD AN ANSWER

Queue 259's code lands: the link floor reads production/site-served.txt
and is off while it says none, and every run prints which branch it
took. The two held messages stay in outbox-blocked until 260 lands;
that is the part of the 08:40Z ordering that still binds. Jafar's "Is
this working?" was answered at 13:18:43Z by the executor's no-cli
fallback, with the archive link, so the Producer's reply is revised to
say what that note meant before it sends. Next builder dispatches, in
order: 261 (the executor's cli keys and its journal tail reach
production/pc-ops/), 262 (the executor stops adding the archive link
while the register allows zero), 260, 256. Ruling:
game-design/decision-2026-09-11-ruling-the-link-floor-marker-batch-and-the-answer-already-sent.md.

## 2026-09-11 13:40Z: THE ROUND TRIP WORKS, AND WHAT CAME BACK WAS A FAILURE NOTICE

THE LOOP IS PROVEN END TO END, by files the PC committed rather than by
anything this session ran:

    in       production/inbox/2026-09-11T1316Z-79313220.md      13:16:56Z
    out      messageId=76 chars=271                              13:18:43Z
    receipt  production/outbound/2026-09-11T1316Z-79313220.answer.receipt.txt
             committed to pc-inbox at 8633feda                   13:18:43Z
    latency  107 s, ONE SAMPLE of one message, not a rate

That is the message from his phone, the answer back and the receipt, which is
the whole of what Jafar asked to have proven. The inbound half and the return
half both work.

WHAT CAME BACK WAS NOT THE PRODUCER'S ANSWER. `chars: 271` in the receipt is
what identifies it, and it identifies it uniquely: `fallback_no_cli()` called
with no state words measures 271, the worktree variant 262 and the prepare
variant 267, so 3 of 3 variants were measured and only one matches. That call
is `tools/runner/executor.py:1533` and nowhere else. He was told "the tool it
needs is not available on this machine right now".

READ WHAT THAT LINE SITS UNDER, because it narrows the fault a long way. Line
1533 is inside `if not res["started"]`, which is reached only after
`worktree_ready` AND `prepare_worktree` have both returned ok. So the checkout
was fine, the worktree was fine, and the Claude CLI itself would not start.

AND THERE THE DIAGNOSIS STOPS, which is the finding that outranks the fault.
The branch records its reason (`why=oneword(res["why"])`, and `run_session`
separates "not on PATH" from "would not start", both with selftest fixtures).
That reason is not published anywhere.

I FIRST WROTE THAT NO CHANNEL EXISTED, WHICH WAS FALSE, and the correction is
the more useful finding. Rule 3: my analysis said something was missing, so I
opened the directory and looked. `production/pc-ops/supervisor-status.txt` is
the supervisor's own status copied off the PC by CI every run, line 1 naming
its commit, `statusFresh=yes`, and it already carries `executorState=idle
executorHandled=1 executorPending=0`. The channel is built, it works, and it
omits exactly one field. Measured:

    grep "cli=|no-cli|notOnPath|wouldNotStart" over production/pc-ops/   0 hits
    pc-jobs paths the tools name                                         8
    of those, published by CI                                            1

So the fix is a key on a status file that already ships, not a new channel.
That is `production/queue/261`, and it is small. CLAUDE.md rule 12 still names
it: the studio can read THAT the executor failed, from a character count in a
receipt, and can read WHY from nothing.

THE LINK IT CARRIED WAS THE ARCHIVE'S. The fallback wordings append `SITE_LINK`,
which is `https://jsab258.github.io/wc26-picks/`, and the answer register
enforces `linkdest`, which passes it because the archive is still ON the
permitted list. So on the same morning the link floor was suspended precisely
so that no stale link would reach him, one reached him anyway, down a path the
floor does not govern. Queue 256 moves the site list; whether it also covers
the hardcoded fallbacks is with the director.

THE CEILING FIX WAS HALF DONE AND I FINISHED IT. Jafar asked for the standing
ceiling to be "one line nobody can misread". The first pass put an unmissable
block at the top and left the BODY contradicting it, which is the same fault
one level down. Swept and measured:

    lines containing 80                                     18
    of those, near a ceiling or STOP word                   12
    dated table rows, correctly historical                   8
    the incident narrative, already says "retired"           1
    LIVE rules still naming 80 before this sweep             3
    historical arithmetic now marked as of its date          2
    live rules naming 80 after it                            0

The dangerous one was the mechanical stop condition: "1. Total reported use at
or above 80 percent: STOP." A session reading only that list would have stopped
five points early AND read one meter where the 2026-09-03 ruling says the
HIGHER of two governs. It now reads "EITHER METER at or above 85 percent". The
two arithmetic passages that price a particular day keep their 80 because
recomputing them would falsify what they measured; both now say so in place.

A6 PROVED ITSELF ON THE REAL CASE, not on a fixture. The 07:02Z install ran
after Jafar disabled the task, and its committed evidence
(`production/pc-ops/scheduled-task-verify.txt`, landed at `01c3fd57`) reads:

    taskEnabledBefore=False
    taskEnabledCarried=False reason=a-person-disabled-this-task-and-an-install-
                                    does-not-re-enable-it
    installAction=already-correct
    startedNow=refused reason=task-is-disabled-a-person-turned-it-off
    taskEnabled=False

That is the guard doing the thing it was built for, against a human's off
switch, in the live system rather than in its selftest. The same file reads
`supervisorProcessesAfter=2`, which is the pre-fix pair still up from the old
checkout, and `botSweepLastResult=sent0/refused0/of17`.

TWO INSTRUMENT FAULTS OF MY OWN, both self-matches of a kind this file already
records:

1. `pkill -f "ledger/verify.py"` matched THE SHELL RUNNING IT and killed my own
   command. Same shape as the `pgrep -f verify.py` incident that waited forty
   minutes on itself. A pattern naming a process must not appear in the command
   line of the process that greps for it.
2. `producer-check.py <file>` with no `--kind` reported `register=unprompted`
   and DO NOT SEND. The register is not derived from the filename in single
   file mode; `--kind` defaults to unprompted. The real sender passes the
   suffix-derived kind (`outbox.run_check` -> `--kind answer`), under which the
   same file reads SEND. I nearly read a wrong invocation as a regression in
   the tool. RUN THE CHECK THE WAY THE SENDER RUNS IT.

A THIRD, WORTH THE LINE: a verify run was measuring a tree two agents were
still writing to, and on green it would have written a footer that looked
pasteable. Killed it and deleted the stale footer BEFORE relaunching, so the
footer on disk can only ever come from the run that is current.

## 2026-09-11 08:40Z: THE WINDOWS WERE NEVER A CRASH LOOP, AND A CEILING I MISREAD

THE CEILING FAULT IS MINE AND IT NARROWED REAL WORK. `production/budget.md`
carried TWO ceilings at once: a stale "80% of the weekly limit" header near the
top and the live "85 ON THE HIGHER METER, STANDING, ruled by Jafar 2026-09-10"
sixty lines below it. I read the header, called his 78/82 reading a breach, and
husbanded a budget that was not short. WHAT I NARROWED, named so it is
un-narrowed rather than quietly forgotten: no agent was spawned at all, and
`tools/container-setup.sh` was written by the resident instead of a builder,
both decisions taken for a breach that had not happened. Jafar corrected it in
the same session. The header now names 85, points at the ruling and carries this
incident; a machine-readable single ceiling line is queued.

THE HEADER IS THE FIRST THING READ AND THE LAST THING UPDATED. That is the whole
mechanism and it is worth more than the apology.

THE CMD WINDOWS ARE DIAGNOSED AND IT IS NOT A CRASH LOOP. Measured:

    subprocess call sites   supervise 3, pc-watcher 2, executor 5,
                            launch-supervisor 1, telegram-bot 0   = 11
    carrying CREATE_NO_WINDOW                                     =  0

The task registers `pythonw.exe` with `windowless=True`, so the TOP process has
no console and that half was always right. On Windows a child launched from a
console-subsystem executable by a parent with NO console ALLOCATES ITS OWN
CONSOLE WINDOW. These daemons had only ever been started from `START
EVERYTHING.bat`, which has a console the children inherit silently, so the
scheduled task is the first windowless parent they have had and a latent fault
in all eleven sites surfaced at once. pc-watcher resets the checkout about once
a minute and the executor polls every fifteen seconds, each one a git
subprocess, which is the loop he watched. THE WINDOWLESS REQUIREMENT WAS HALF
MET: the parent, never its descendants.

`taskLastTaskResult=267009` is 0x00041301, "currently running". It is a status
and not a failure code, and the ruling forbids citing it as one again.

THE RE-ENABLE IS GATED ON SIX PRINTED LINES, not on anybody's judgement, and the
sharpest of them is not mine: THE INSTRUMENT MUST BE SEEN TO FAIL FIRST. The
same proof step is run against the pre-fix checkout and must print
`verdict=WINDOWS-SEEN`; without that, `verdict=WINDOWLESS` only means the
sampler cannot see windows. The conhost count is CUMULATIVE because a git child
lives a fraction of a second. And `survivedSec=300/300` per process, because a
fleet that died inside the window is the trivially windowless one. Full
condition in `game-design/decision-2026-09-11-ruling-the-windowless-fleet-and-
four-smaller-calls.md`.

ONE CONFLICT RAISED RATHER THAN RESOLVED ALONE. The ruling says re-enabling is
Jafar's click and the resident never does it on his behalf. Jafar instructed the
resident to re-enable it through the installer once proven. He outranks the
director, so the resident will, after the proof passes, and he has been told the
director wanted the click to be his.

THE SWEEP'S PERMANENT RED IS MOVED OUT OF THE WAY. The 5346-character message is
in `production/outbox-blocked/` and the next sweep should print exit 0; IF IT
STILL READS 1 THE INSTRUMENT IS THE NEXT SUSPECT rather than another message.
Queue 260 before queue 259, ruled, because the other held message is 4739
characters and the link-floor fix would walk it into the same 400.

## 2026-09-11 08:00Z: THE FLEET MOVED, THE INSTALL SUCCEEDED, AND A1 WAS PROVEN BOTH WAYS

HE DISABLED THE TASK AND SIGNED BACK IN, AND EVERYTHING DOWNSTREAM FOLLOWED.
Run 424cc7eb, measured on c843afcb:

    resyncAction=updated branch=main sha=c843afc
    repo=C:\Users\Jafar\ledger-migrate      configLocalPresent=True
    checkoutBroughtCurrentThisRun=True  taskAlreadyNamesRepo=False
      taskPathHeld=C:\Users\Jafar\wc26-picks
    installAction=update                installerExitCode=0
    supervisorPath=C:\Users\Jafar\ledger-migrate   on both processes

A1 IS NOW TESTED ON BOTH OUTCOMES BY REAL RUNS RATHER THAN BY A FIXTURE, which
is the accepting case rule satisfied in production. Last night it REFUSED, with
the checkout stale and the task holding the old path. This morning it ALLOWED,
because the resync ran first and brought the checkout current, so the first of
its two conditions was met while the second was still false. A guard that only
ever refuses is a ratchet; this one discriminates.

THE RETURN HALF REACHED THIS REPOSITORY FOR THE FIRST TIME. `pc-inbox` here
moved 2a7a234c to 7e22f2d9, carrying receipts 66 and 67 for two messages sent at
06:00Z. The archive's pc-inbox stopped at 2ca5cc39 and is now the frozen one,
which is the correct way round for the first time since the move.

SO OUTBOUND AND THE RECEIPT ARE PROVEN ON LEDGER. INBOUND IS NOT: the only file
under production/inbox/ on the branch is still 2026-09-07T0550Z-79313218.md, so
no message has come from his phone since the move. That half is untested rather
than broken, and it needs him to send one.

THE SWEEP IS RED FOR A REASON THAT WILL NEVER CLEAR ITSELF, and it is not the
move. `sweepCheckoutDecision=send` now, the staleness gate passes, and 17 of 18
files are already sent. The eighteenth is 5346 characters against Telegram's
4096 cap:

    NOT SENT ... (HTTP 400: Bad Request: message is too long).
    It stays unsent and the next pass tries again.
    outboxFiles=18 sent=0 unsent=1 alreadySent=17 sendFailed=1

A 400 naming a property of the message is not a retryable condition, so this has
been failing every pass since 0db066b2, before the move, and a permanent red
hides the next real failure behind it. Queue 260.

AND IT CATCHES THE HELD MESSAGE TOO, which is worth knowing before anybody
celebrates queue 259. `production/outbox-blocked/2026-09-10-the-move-and-the-
one-thing-left.answer.md` is 4739 characters. Reconciling the link floor would
have moved it into the outbox and straight into the same 400. TWO BLOCKS, NOT
ONE, and the second was invisible until the first stopped hiding it.

THE CONTAINER IS NOW REPRODUCIBLE. `tools/container-setup.sh` carries the five
things installed by hand on 2026-09-10 to take verify from crashing on its first
check to 81 of 81 green: dotnet 8 from apt, PowerShell from the official tarball
because `dotnet tool install --global PowerShell` FAILS on this image, the three
pip modules, the unshallow, and the tools path. Run on the accepting case and it
reads stepsOk=5/5. Its first draft read pymods=FAILED on a container where all
three modules were present, because the check called importlib.util.find_spec
without importing importlib.util; the accepting-case run is what caught it.

## 2026-09-11 04:00Z: THE WAKE FIRED, NO BRIEF WAS WRITTEN, AND THAT IS THE FINDING

SAID OUT LOUD BECAUSE THE PROMPT REQUIRES IT: on a day this wake fires a brief
file for that day must exist, and its absence otherwise looks identical to a
quiet day. There is no `production/briefs/2026-09-11.md`. This is the reason,
and it is not that nobody looked.

THE BRIEF PIPELINE IS STRUCTURALLY BLOCKED UNTIL QUEUE 259 LANDS. Measured this
wake rather than assumed, on a throwaway file so nothing was left in the tree:

    producer-check --kind brief  ->  DO NOT SEND  rulesEnforced=9/10
      linkfloor   no link to any of the 5 published page(s)

The brief register enforces the SAME link floor that held last night's answer,
and all five permitted destinations still sit under the ARCHIVE's published
pages, which after the move show the world as it was before it. So today's
brief could only pass by carrying a link that misleads him. Writing it anyway
would also turn verify red, because the register is walked by the gate, and
that would block every other commit behind it. That is the wedge already
documented in `production/outbox-blocked/README.md`.

AND EVEN A PASSING BRIEF COULD NOT BE SENT. The fleet is still in the archive
checkout, so the sender refuses on a stale checkout, exactly as it did at
20:01Z. Two independent blocks, one message.

THE STREAK IS 0/7 AND CANNOT MOVE. `briefStreakReadable=0/7 briefDaysTapped=0
briefTapRecords=0 briefsSentEver=2 briefAccepted=no`. Nothing here is a tap he
withheld; nothing has been deliverable since the move.

THE DUE WAKE RECORD IS CARRIED FORWARD, NOT DROPPED AND NOT LEFT DUE. `1ed3463a`
came due at 04:00Z asking for the Hook pair, the first authored district sheet
with its provenance table, and the sun before and after, carried as one picture
with the two buttons. None of that can ride a message that cannot be sent.

Leaving it due would have fired the turn-boundary hook for ever; discharging it
alone would have lost the instruction. So it is re-armed as `e80f2b15` for
2026-09-12T04:00Z, carrying the same order in short form plus the two blocks to
check BEFORE writing anything, and `1ed3463a` is discharged against that. The
original record is not edited: it stays readable in full at
`production/wakes/2026-09-11T0400Z-1ed3463a.wake.txt`, which is where the four
cards still waiting on a ruling also live, each with a recommendation and a
default.

WHAT UNBLOCKS IT, in order and neither is the studio's to do alone: queue 259
reconciles the link floor with the ruling that already permits zero links while
no page is served here, moving `tools/runner/outbox.py:run_check` with the
register or the message is refused at the door instead of at the gate; and the
fleet moves when the LEDGER supervisor task is disabled and he signs back in.

NOTHING ELSE WAS RUN THIS WAKE. The budget's newest reading is 2026-09-09 and a
full session of heavy work has happened since, which the budget file's own rule
says makes the day unmeasured and argues for stopping; Jafar also ruled the next
reading follows his report. An unknown budget is not permission.

## 2026-09-10 20:15Z: THE INSTALL RE-RAN AND REFUSED, WHICH IS THE ANSWER

RUN ff885ed9, measured on 9e49c53c, and it settles four things at once. Read it
rather than the exit code:

    workflowRef=main daemonsBranch=main
    repo=C:\Users\Jafar\ledger-migrate
    configLocalPresent=True
    supervisorPath=C:\Users\Jafar\wc26-picks   on all four processes
    resyncAction=skipped-supervisor-running
    checkoutBroughtCurrentThisRun=False taskAlreadyNamesRepo=False
    installAction=refused-checkout-not-current
      wanted=C:\Users\Jafar\ledger-migrate taskHolds=C:\Users\Jafar\wc26-picks
    installerExitCode=0

1. THE BRANCH REPOINT WORKS. `daemonsBranch=main` where it read the old branch
   this morning.
2. THE NEW CHECKOUT EXISTS AND IS FOUND. Find-Repo resolves `ledger-migrate`
   rather than throwing.
3. TWO PREDICTIONS OF MINE WERE WRONG AND THE MEASUREMENT CORRECTED BOTH.
   `configLocalPresent=True`: the Telegram key IS in the new checkout. I had
   reasoned that because the file is gitignored and untracked the migration's
   clone could not contain it, and I was about to report it as a blocker. Git
   could not have put it there; something else did, and the question was
   settled by running the entry point rather than by the inference. The other
   was voice-live, below.
4. A1 FIRED ON ITS FIRST REAL RUN. The refusal the director demanded is the
   thing that stopped this push from arming a fleet pinned to the archive, and
   it exits 0 because a refusal is a correct outcome.

AND THE SEND HALF REFUSED TOO, FOR A DIFFERENT AND ALSO CORRECT REASON:

    sweepCheckoutRunSha=9e49c53c... sweepCheckoutPcHeadSha=f6508b3b...
    sweepCheckoutContains=no sweepCheckoutDecision=refuse
    sweepCheckoutBehindSecByCommitTime=18073
    sweepStatus=REFUSED-STALE-CHECKOUT sweepSent=0 sweepGateExit=3

`ledger-migrate` is frozen at the migration commit, about five hours behind,
because the thing that would refresh it lives in the fleet that is still in
`wc26-picks`. So the sender declined to send a message written against files
that checkout has never seen. TWO GATES REFUSED TONIGHT AND BOTH WERE RIGHT;
neither is a fault and neither should be loosened.

SO THE ROUND TRIP STANDS AT ONE OF FOUR ON THIS REPOSITORY. The probe landed
here with a real payload. The receipt happened, on the archive. The message
from his phone and the answer back are both blocked, by the one cause, behind
his one action: stop the fleet once, or sign out and in.

THE HOURLY TRIGGER IS PROVEN RATHER THAN MERELY ARMED. It fired at 20:03:44Z
into this session, and its own rule (do the inbox half and stop when work is in
flight) was the correct behaviour and what happened. The inbox read clean:
newestMessageId=61 here against 64 and 65 on the archive, which is the split
stated as a number.

## 2026-09-10 19:20Z: FIRST SESSION ON `ledger`, AND THE FLEET IS STILL ON THE ARCHIVE

THE MOVE ITSELF IS GOOD, AND CHECKING IT CORRECTED WHAT I WAS ABOUT TO WRITE.
All four branches arrived and the migration copied them identically, so all 170
decision records keep resolving here. But "the identifiers are identical" is
TRUE OF THE MIGRATION INSTANT AND FALSE NOW, because both repositories are live
and have each moved since:

    branch          ledger        archive(wc26-picks)
    art/atlas-01    8c7a1b0a      46d7d759        ledger moved ahead, under CI
    pc-inbox        2a7a234c      2ca5cc39        THE ARCHIVE MOVED AHEAD
    pc-results      3efd67eb      3efd67eb        equal
    main            8caa61d6      (e7c92cd)       both moved, see below

The pc-inbox row is not a curiosity, it is the diagnosis. THE ARCHIVE'S RETURN
BRANCH IS AHEAD BECAUSE HIS PC IS STILL WRITING TO IT: at 18:55:55Z the bot
pushed two delivery receipts there, minutes after this session started. A
sentence saying the identifiers match would have hidden exactly the fault this
entry is about.

THE ONE COMMIT THE MIGRATION MISSED came across this session: e7c92cd, model
routing, made on wc26-picks after the copy. Its parent is the migration point,
so it merged clean into main.

THE RUNNER IS ALIVE ON THE NEW REPOSITORY AND A PROBE HAS ALREADY LANDED ON
IT. `8caa61d6 UE machine probe from f6508b3b` is a real payload and not a green
exit code: line 1 names the commit, and the verdict carries
perceptionRows=2494 perceptionMismatches=0 probeTest=PASS verdictReached=end,
with the frames and the gif regenerated beside it. That is the evidence channel
working end to end on `ledger`, which was the thing most at risk in the move.

WHAT IS NOT WORKING, AND IT IS ONE FAULT WITH THREE FACES: EVERY DAEMON ON HIS
PC IS STILL RUNNING OUT OF `C:\Users\Jafar\wc26-picks` AND READING THE ARCHIVE.
Measured off the bot restart this evening, which succeeded:
botRootCommandLine names the wc26-picks path, and stableHead reads
e7c92cdfdca0f5d558f01720e6ad9f6abb0fcaae, the archive branch tip. The
supervisor's own status file agrees: statusSource is the wc26-picks path,
supervisor=running daemons=3 running=3 gaveUp=0, botUptimeSec=68566,
botSweepPasses=531 with botSweepLastResult=sent0/refused0/of17.

So the channel is HEALTHY AND POINTED AT THE WRONG REPOSITORY. Three
consequences, and the third is the one that blocks:

1. A message from his phone lands in the ARCHIVE's `pc-inbox`, not this one.
2. An outbox file pushed here is never swept, because the sweep reads his
   checkout and his checkout is the old one.
3. THE TRANSITION CANNOT BE DONE FROM HERE. The installer refuses to touch a
   checkout while a supervisor or a bare pc-watcher is running, by design,
   because two writers on one git index cost this project four days. The old
   fleet is running, so the resync of the NEW checkout is skipped, so the new
   checkout stays frozen at whatever the migration left. It is the same
   deadlock shape the installer's own header already documents, one level
   across: the watcher that would keep `ledger-migrate` current is running
   inside the fleet that lives in `wc26-picks`.

The registered scheduled task can be repointed from CI and that is done. The
RUNNING processes move at his next logon, or when he stops them once. Nothing
here forces that, deliberately.

AND ONE THING GIT CANNOT CARRY. `tools/runner/config.local` is gitignored and
untracked (`.gitignore:98`, 0 files tracked), so the clone the migration made
CANNOT contain the Telegram token. Until it is copied across by hand, the new
checkout can receive nothing and send nothing. The installer prints
`configLocalPresent` for whichever path it is pointed at, so the re-run
measures this rather than guessing it. The file is never printed and never
committed.

THE PRE-COMMIT GATE WAS UNREACHABLE HERE AND IS ALSO BYPASSABLE. Two separate
faults, both found this session, both now repaired, and BOTH WERE WORSE THAN
FIRST DESCRIBED.

verify.py raised FileNotFoundError out of shape(), the FIRST entry in main(),
because this container has no dotnet and that step had no missing-tool guard.
checksRun=0. The repair is one chokepoint rather than 85 call sites: run()
raises MissingTool for a bare argv[0] PATH cannot find, and main() turns that
into the file's own idiom. A sweep of the call sites, with its denominators:

    BEFORE  callSites=86 binaries=5 resolveHere=4/5 guarded=0/86
            unguardedMissing=10 (all dotnet)
    AFTER   guarded=75/86 unguardedMissing=0
    footer  checks=70ran/11skipped/81total skippedFor=PowerShell:1/dotnet:10

THE GATE HOOK'S HOLE WAS NOT THE HEREDOC. I reported it as a heredoc bypass;
the builder found the real shape, which is larger. The boundary class was
`[;&|]`, WHICH CONTAINS NO NEWLINE, so a commit on ANY LINE BUT THE FIRST was
never a commit to this gate. A heredoc is only the usual way a newline gets in,
and it is the way CLAUDE.md itself prescribes. Five of fourteen shapes wrong
before, zero after.

AND IT DATES TO THE HOOK'S FIRST COMMIT. The builder could not measure this
because the clone was shallow at 60 commits; unshallowing to 2790 answered it.
`cd30c19a`, 24 August, the commit that introduced the hook, already carries
`(^|[;&|]\s*)`. So the gate has been open on the recommended command shape for
its whole life, seventeen days, and 2b67763 this session is one instance.

NINE REAL FAILURES CAME OUT FROM BEHIND THE CRASH and they are the argument for
the repair. Most are this container lacking tools rather than code faults:
game_compiles and reach both raise on dotnet ONE PROCESS BOUNDARY DOWN, where
the chokepoint cannot see them; blender_hash_parse needs PowerShell; ref_bench
wanted PIL and decal_ink numpy, both now installed; runs_map_to_commits read
362 run files against 60 commits, which was the shallow clone and is now 2790;
director_cadence wants the ruling this batch carries. sheet_read and voice_live
are the two nobody has explained yet.

THE HOOK SELFTEST FAILS ONE CASE AND IT IS PRE-EXISTING, proven by running the
same selftest against the hook as HEAD holds it: 60 passed 1 failed there, 74
passed 1 failed here, the same case. It greps for a key with a literal space
that the emitter correctly encodes. The assertion is stale, not the code. NOT
FIXED, deliberately, because fixing a test to make red go green is the one
thing that erodes a gate.

THE FIRST PUSH TO main STARTED TEN WORKFLOWS AT ONCE and they raced to push
their evidence. The supervisor install lost: its verification commit ec844444
exists only on the runner's disk, rejected non-fast-forward after its rebase
hit a conflict in `production/pc-ops/supervisor-status.txt`. The install itself
ran; only the push failed. Dispatch it ALONE, with the runner clear.

TWO TRIGGERS ARE ARMED, both bound to this session, and one of them is not the
cadence he asked for. Full record and both prompts in
`production/repo-move-triggers.md`. The scheduler refuses any interval under
an hour, so the thirty-minute trigger is hourly; two offset hourly triggers
would produce his cadence and were deliberately NOT created, because each
would pass the check alone while together they are exactly what the floor
forbids. Neither trigger carries a connector, so a fired session may be unable
to dispatch a workflow; the prompts themselves need none.

## 2026-09-10 09:00Z: THE FAIRVIEW SHEET LANDED AND THE TWO-ARM DESIGN PAID OFF

BANKED, four of four, none blank, 171.1 to 188.8 seconds each. The estimator
said 132.8 and the builder scaled it to about 158 from measured neighbours;
the truth is 179.5 mean, so the estimator UNDER-READS BY 35 PER CENT at this
size and the builder's own scaling still under-read by 14. Do not quote the
estimator as a cost without the measured neighbour beside it.

THE TWO-ARM DESIGN ANSWERED THE QUESTION IT WAS BUILT FOR, and the answer is
worth keeping. The builder spent two of four seeds on the authored prompt at 542
words and two on the same concept cut to 387, on the one adherence fact this
lane had measured. BOTH SHORT DRAWS GOT THE SHEET TITLE RIGHT AND BOTH LONG
DRAWS DID NOT. That is a measured result about prompt length and lettering from
a design that could have been four seeds of one arm and told us nothing.

OURS AGAINST THEIRS, honestly, and their sheet is the better DOCUMENT. The
photographs are competitive: red brick, slate, chimney pots, aerials, a wet road,
a washing line, the harbour and its cranes below. THEIR SHEET IS A DESIGNED
ARTEFACT AND OURS IS TWO PICTURES AND A SWATCH ROW. Theirs carries a header
block, a tagline, EIGHT LABELLED swatches, annotations ON the panels naming the
height band, the slope, the eye height and the view direction, a street sign and
a school sign, and a footer. Its two panels are the SAME LOCATION LOOKING
OPPOSITE WAYS and say so. Ours has four unlabelled swatches, no annotations and
some garbled lettering on the panels.

AND THEIRS HAS THE CHAPEL AND SCHOOL, WHICH IS OUR OWN ATLAS LANDMARK F1. We
asked for it in the positive half, a slate-roofed chapel and a railed school yard
mid-slope, and the model did not put it where the eye lands. That is not a
sourcing gap, it is an adherence gap, and it is the kind the negative half cannot
help with because the negative is never evaluated at all.

TOMORROW'S PICTURE IS BUILT AND ITS SIDECAR IS WRITTEN:
game-design/sim-shots/brief_2026-09-11.jpg stacks the sun before and after, the
Hook pair and the Fairview pair in caption order, and
production/briefs/2026-09-11.photo.txt names it.

## 2026-09-10 08:10Z: THE FOUR-LANE BATCH IS LANDED AND TWO RUNS ARE OUT

FIVE COMMITS, IN THE ORDER THE REVIEW'S C12 REQUIRES, and the working tree went
clean for the first time in two days. Game lane with the record, then the art
lane, then the annotations, then production/d1-probe/DISPATCH ALONE, then the
Fairview sentinel behind it. The two trigger files are separated from everything
else on purpose so a reader of the history can see which commit started which
run, and so nothing fires until what it fires on has been reviewed.

THE SHA TO WATCH BY IS 83dec336, captured BEFORE the dispatch per ci.md, and the
watch tests ANCESTRY AND PAYLOAD BOTH. Ancestry alone says a run started and not
that it produced anything, which cost a false landing on 9 September when a
scheduled housekeeping commit containing the watched sha was read as the render
arriving. Queue 229.

WHAT THE RENDER MUST ANSWER, written before it started: lightAimStatus=AGREES
with asked beside read on both axes, and the sun asked at pitch -36.0 and yaw
25.0. IF IT READS -82.0 AGAIN THE REPAIR DID NOT REACH THE RENDERER AND NOTHING
ELSE IN THE RUN MEANS ANYTHING. Then nullSeriesSamples=7/of=25 with
nullSeriesTiedGroups=0, cellAgree=25/of=25, rigDeterminism=IDENTICAL at
rigDiffPixels=0/921600, and fogMaxOpacityRead across four rows with every
pre-existing condition still at 0.450.

THE BEFORE FRAME FOR THE SUN COMPARISON IS AT 83dec336 AND IS PROVEN READABLE
THERE, because the render commits its new frames over the old paths and the
before picture would otherwise be gone the moment the run lands. Recover it with
`git show 83dec336:production/d1-probe/ue-vign_hook_day.png`. The pair goes
through `python3 tools/brief-sheet.py district --ref <before> --ours <after>
--left "BEFORE, the sun 82 degrees up" --right "AFTER, the sun where the plan
puts it"`.

AND THE FRAMES GET OPENED BEFORE ANY GATE IS READ. Queue 180's acceptance says
his eye is the gate and no number passes this rung.

NOW BUILDING, and it is the largest visual gap left on rung 1: queue 223. Thirty
pieces render the engine default because one line skips any piece whose surface
did not resolve, and 593 minus 563 is exactly 30. No shop interiors, no posters,
no notices, no yellow road markings. NOTHING NEEDS FETCHING; the UE probe is
missing four rules the Unity host already has written down. The number that
proves it is piecesUnpainted going 30 to 0.

TWO THINGS DELIBERATELY NOT BUILT, each with its reason on the record. The
CONTACT bucket for the burial gate, because the ruling attaches five conditions
to it and a key rename meets none of them; the series its tolerance must be read
off is already measured and waiting, 11 pairs at exactly 0.000000 mm and 16 from
3.74 to 1043.45 mm, so any tolerance between them separates the two cases on
today's street. And queue 227's gate denominator, because surfacesAsked=16
counts two decal blends as library surfaces so its green state would require
shipping wrong content, and changing what a gate counts is a conclusion change
that needs a ruling rather than a diff.

## 2026-09-10 07:30Z: A STANDING PROMPT RULE, AND A BUDGET FAULT OF THE RESIDENT'S

THE PROMPT RULE, Jafar 2026-09-10, and it applies to every image spec this lane
ever writes: A NEGATIVE VETOES BUT CANNOT SUMMON. ANYTHING THAT MUST APPEAR IS
NAMED IN THE POSITIVE HALF.

It has a measurement behind it, AND THE RESIDENT'S FIRST READING OF THAT
MEASUREMENT WAS WRONG, corrected 07:40Z the same morning it was written. The
Hook spec's negative names pleasure marina, yacht, leisure moorings and pontoon,
and the sheet still came back a pleasant basin rather than a working port. The
resident wrote "THE NEGATIVE DID ITS JOB, there is no yacht in the picture".
IT DID NOT. The negative was never evaluated at all.

tools/imagegen/imagegen.py's own negative_state says so in its docstring, read
from stable-diffusion.cpp's resolve_guidance on 25 August: a negative prompt at
cfg 1.0 DOES NOTHING, because use_uncond is set only when img_cfg differs from
txt_cfg and a model with no image conditioning has img_cfg forced to 1.0. Every
item in this lane runs at cfg 1.0 and every one reports negativeActive=False.
THE NEGATIVE HALF OF EVERY SPEC THIS LANE HAS EVER SHIPPED IS DOCUMENTATION AND
NOT A CONTROL. The absence of a yacht is the positive prompt's doing or it is
chance; it is not the veto working.

THAT MAKES JAFAR'S RULE STRONGER RATHER THAN WEAKER. He ruled a negative vetoes
but cannot summon. At this lane's settings a negative cannot even veto, so
anything that must appear and anything that must not appear are BOTH the
positive half's problem, and the negative is a note to the next reader. Queue
233 and queue 234.

The Fairview spec already satisfies both halves, measured rather than assumed:
positiveExclusions=0/542wordsScanned across its items, and nine working objects
named positively. It goes as authored.

THE BUDGET FAULT, AND IT IS THE RESIDENT'S. Two turns ended on a ceiling that
does not exist. The ceiling is SEVENTY-FIVE PER CENT ON THE HIGHER OF TWO
METERS, read by Jafar off a screen nothing in this container can see, and his
opening "Readings: total 45, Fable 41" are those two meter values. The resident
read 75 as a COUNT and counted its own tool calls toward it, stopping twice with
27 points of real budget left and the queue full. A UNIT ERROR, not an
arithmetic one, which is why it survived a day: both readings sat in the
thirties and forties, so the wrong measure never contradicted itself out loud.
NO SESSION MAY EVER STOP ON A SELF-COUNTED NUMBER. Full record in
production/budget.md and production/findings.txt.

## 2026-09-10 05:10Z: FOUR RULINGS FROM JAFAR, AND THE LANE CHANGES OWNER

1. THE LOCAL IMAGE LANE IS THE CONCEPT ROUTE. Codex's sheets stay as REFERENCE
   only. Ours are produced by the three-pass method and the remaining six
   district sheets follow, ONE PER DAY IN THE BRIEF. The next sheet is the test
   of ORIGINAL concept art: its prompt is authored from the form bible, the
   atlas and the research, with NO USE OF CODEX'S PROMPT FILES, and it goes in
   the brief beside Codex's sheet for the same district WITH A PROVENANCE TABLE
   saying which words came from which source. The Hook proved the lane can
   DRAW; this proves whether it can AUTHOR, and reaching for their prompt files
   is the exact failure it exists to detect.
2. ONE CHANNEL FIX IS ALLOWED AND NO MORE: the brief must carry its pictures
   AND its two buttons in ONE message, queue 232. "Nothing else on the channel."
3. EVERY BUILDER BRIEF OPENS WITH: produce at a clean boundary first, refine
   second. Three agents burned their whole budgets reading on the night of the
   9th and shipped nothing. AND VERIFY RUNS ALONE, NEVER BESIDE AGENTS, per
   queue 225, because contention makes it report failures it did not measure.
4. THE OUTSIDE ACCOUNT IS RETIRED FROM PRODUCTION, kept for an audit every few
   weeks. Nothing is handed to it again for images, recipes or research.

THE ORDER OF WORK HE SET: the three blocking amendments, then the sun-fixed
render dispatched with the seven-frame null accounted for, and the before and
after of the street; the Hook pass-2 result into the brief with an honest
caption; the fascia package to a real mesh in the street; the next Blender
recipe written IN-HOUSE rather than adapted from Codex's, so the 3D route is
tested the same way as the image route; and rung 1 continuing with SKY DOWN
BEFORE WETNESS, each step verified by opening the frame against the panel.

PASS 2 OF THE HOOK LANDED AND THE CORRECTION WORKED ON WHAT IT TARGETED.
imagegenVerdict=BANKED wroteThisRun=4 blankThisRun=0. The three objects the
model DROPPED in pass 1, the rope, the dustbin and the crate, are present on all
four draws, and the lettering discipline held: two named fascias rather than a
terrace of invented ones. Honest against pass 1: the panels sit smaller in more
cream margin and the street reads emptier than pass 1's best seed, and the beer
firkin came back as a plain wooden crate on all four. Best of four is the lead
seed, and choosing one of four is what Codex did too, so the comparison stays
symmetric and the caption says so.

## 2026-09-09 22:40Z: A CONTAINER RESTART KILLED TWO BUILDERS MID-EDIT

WHAT WAS LOST AND WHAT WAS NOT. The container restarted, both builders died
mid-edit, and the checkout rolled back behind origin. Everything pushed was
safe. Thirty-five uncommitted paths were not, and they were separated by hand
rather than committed together, because a resident never commits a builder's
work-in-progress.

THE ENGINE BUILDER'S 1625 INSERTIONS WERE REVERTED, NOT LANDED, and the reason
is that the tests caught real defects rather than pinned numbers. Three of 275
checks failed alone: the burial half ships the count it examined over the count
the file asked for; a fixture pinned to "pieces":593 could not be planted after
the count moved to 610; and a nothing-measured cell row CONTAINS A SPACE, which
is the instruments.md rule that every reader splits on whitespace. Two of those
three are faults in the new code. FIXING TESTS TO MAKE RED GO GREEN IS THE ONE
THING THAT ERODES A GATE, so nothing was edited to pass. The work is preserved
as a 2215-line patch in the session scratchpad, which does NOT survive another
container reclaim, and it is cheaper to rebuild from the ruling than to nurse.

WHAT LANDED INSTEAD: the record, the ruling, eight queue items, the pass-2 art
sentinel and spec, the rebuilt comparison sheet and its compositor, and the art
lane's two fascia meshes with their attribution. All of it reviewed, all of it
mine or the director's.

THE ART LANE GOT FURTHER THAN THE GAME LANE and its meshes are on disk:
ledger/Assets/Props/base-mesh/fascia_console_01.glb and fascia_cornice_01.glb,
with production/art/fascia-01/ carrying the station work. Its spec rows were
reverted with the engine batch because they moved a bill-of-materials count
that CoreTests pins, so the meshes are present and named by nothing yet, which
is rule 6 and is stated here rather than hidden. Queue 228 carries the burial
reading its placement produced.

## 2026-09-09 21:15Z: THE FRAME WAS OPENED AND IT MOVED THE RUNG

FOUR THINGS ARE IN FLIGHT RIGHT NOW, three of them builders and one a ruling.
A session that resumes this file should read this section before starting
anything, because all four touch rung 1 and two of them touch the same files.

  in flight  engine builder: the sky-by-sun grid on cam_hook, the in-frame
             ratio in FrameStats, wetness reaching the material, the fog's max
             opacity, and the DISPATCH entry. Resumed once after a turn limit.
  in flight  world designer: the fascia package through all five stations.
  in flight  content wrangler: the four surfaces with no maps (queue 223).
  in flight  studio director: the ruling on the grid, at
             game-design/decision-2026-09-09-ruling-the-grid-not-the-ladder.md.
  ready, held: the art lane's Hook pass 2 is written and validated and is NOT
             pushed, because two builders hold uncommitted work in this
             checkout and merging under them would destroy it. Push it with
             their work, not before.

THE ART LANE COMPLETED ITS FIRST FULL PASS. imagegen run 5 banked four Hook
draws at commit e4924cb7: wroteThisRun=4 blankThisRun=0 checkedThisRun=4, 154
to 157 seconds each. THEY WERE THEN OPENED AND INSPECTED BY VISION, which is
the middle step of the method and the step that had been missing. Seed
20260910 carries a crisp MICKEY'S; the other three garble it; every secondary
fascia is a smear on all four; and the three objects the prompt asked for were
dropped by the model while the four swatches arrived. Pass 2 corrects exactly
those and concedes swatch labels rather than risk the two fascias.

THE REFERENCE NUMBER THAT DROVE THIS RUNG ALL DAY WAS MEASURING A CAPTION
STRIP. The crop at (0,768,1024,1536) is 32 per cent swatch strip and near-white
caption band and omits 106 rows off the top of the photograph. The claim it
supported, that the two pictures' bright ends nearly agree, IS FALSE: reference
street p95 is 0.8239 against our 0.9532. Corrected in production/findings.txt
with nothing deleted, and both copies in this file corrected in place.

AND THE CORRECT BOUNDS WERE ALREADY IN THE REPO. vignette-scene.json's cam_hook
note records the panel content area as x 11 to 1012, y 662 to 1278, written
when cam_hook was placed from that panel, agreeing with tonight's independent
measurement to one pixel. THAT IS THE SECOND TIME IN ONE DAY that this studio
re-derived, wrongly, something already written down; the first cost a CI round
trip on a Blender question answered in blender-setup.txt on 1 September. Queue
220 is now "read the bounds that exist", not "find them".

WHAT THE CORRECTED BANDS SAY, and it is not what the instruction assumed:

    region      ref street photo              ours, ue-vign_hook_day
    ground      mean 0.4159  p95/p05 3.68     mean 0.7735  p95/p05 1.61
    sky         mean 0.6102  p95/p05 4.27     mean 0.6535  p95/p05 4.02

The sky band nearly agrees on level and on ratio; THE WHOLE GAP IS THE GROUND.
Limit stamped on it, because this is the shape that already misled twice: these
are proportional bands over pictures with different content, so the ground rows
are strong and the SKY ROWS ARE WEAK and may be a content coincidence. Queue
222 is that item.

THE BIGGEST FINDING IS NOT A LIGHTING NUMBER. Opening the frame beside the
reference shows no windows, no shop interiors, no signage and no road markings.
The obvious reading, that the blockout is untextured, IS WRONG and the verdict
refutes it: piecesTextured=563/593, texturesImported=36, texResourceValid=12/12.
The real fault is surfacesAbsent=card/interior/multiply/paint_yellow with
mapsFound=36/48, and the arithmetic closes exactly at 4 surfaces times 3 maps.

AND THE READING OF THAT WAS ALSO WRONG, corrected 22:05Z after the wrangler
answered it. NOTHING NEEDS SOURCING. card and multiply ARE NOT SURFACES AT ALL,
they are decal BLEND MODES declared at StreetVignette.cs:57 and enforced at
1651, and all twenty decal images are already on disk, ten generated plus five
CC0 ambientCG sets. paint_yellow is ProceduralOnly at AssetLibrary.cs:1613 and
a pack file for it is deliberately ignored. interior is generated from a tint
and BORROWS its normal and roughness from the window surface at
AssetLibrary.cs:611.

THE ACTUAL CAUSE OF THE BLANK FRAME IS ONE LINE, VignetteShot.cpp:2749: a piece
whose surface did not resolve gets NO MATERIAL INSTANCE AT ALL and renders the
engine default. 10 card + 10 multiply + 6 interior + 4 paint_yellow = 30, and
593 minus 563 is 30. The UE probe is missing four rules the Unity host already
has and that are already written down: the tint fallback, the
interior-borrows-window rule, any decal texture path at all, and the _b variant
rule, whose absence is why 15 of the 51 staged pack files are named by nothing.
THAT is the highest-leverage visual fix on the board and it is queue 223,
rewritten. Queue 227 is the gate whose green state would require shipping wrong
content; queue 226 is a false sentence in three files saying no yellow line art
is held, refuted by measuring it at yellowness 150.5 against 4.8.

THE RESOLVER WAS SIMULATED, NOT ASSUMED: re-implemented in Python against the
51 files on disk it printed surfacesResolved=12/16 mapsFound=36/48 and the same
four absent names, character for character with the PC. The ruler is understood.

THE SUN IS AT 82 DEGREES AND THE SPEC ASKS FOR 36. Proven by arithmetic on
committed files, not inferred. vignette-pieces.json:16 asks elevation_deg 36
and azimuth_deg 205; VignetteSpec.h's own two conversions turn those into an
asked pitch of -36.0 and an asked yaw of 25.0; the committed verdict reads
sunPitchYawRead=-82.0/25.0. YAW AGREES TO THE DECIMAL AND PITCH IS OFF BY
EXACTLY 46.0, which rules out coincidence and rules out the readback reading a
different actor. A 4 m post casts 5.5 m at the asked elevation and 0.56 m at
the rendered one, a factor of ten, and that is queue 197 explained. The
readback has printed the truth on every run since it was written and NOBODY
EVER DIFFERENCED ASKED AGAINST READ. Queue 224.

IT IS NOT THE WHOLE STORY, and the record says so rather than letting the
newest finding eat the older one. The grid ruling's own series has the
shadow-edge step at +0.0270 with three fills and no skylight and -0.0003 on
the same pixels with the captured sky. The sun was at 82 on both sides of that
change, so THE SKY IS WHAT KILLED THE STEP, which is exactly Jafar's diagnosis
with a measurement under it, and the elevation is a standing defect that caps
how much shadow is available at all. Both are real. The run separates them.

THREE OF THE RESIDENT'S OWN READINGS WERE REFUSED BY THE DIRECTOR TONIGHT and
all three deserved it. The inference that a sun would put a lit road far above
0.38 is an absolute-luma claim under unsnapped auto exposure, and there is no
level at which "far above" could have been checked. The frame it called night
is a dusk street with legible setts and a white kerb, which the director
established by OPENING it, as the resident should have. And shotMaxLuma=0.6240
is very likely a control-quad pixel rather than scene content, because
controlQuadHidden names only three frames and the quads are in all eight cam_A
frames. The whole-picture conclusion survives on the two band readings, which
are clean because the quad boxes end at y422 and the ground band starts at
y576.

SO THE ORDER HE GAVE IS BEING RUN IN PARALLEL RATHER THAN RESEQUENCED. His
words were sky, then wetness, then worn materials. The measurement says the
surfaces are the bigger lever and the sky may already be right. Decision TAKEN
and logged per his standing order: both run at once, the picture goes in the
brief with the numbers, and his verdict adjusts it.

## 2026-09-09 17:40Z: TWO LANES, AND NEITHER ENDS A TURN WITH WORK IN THE QUEUE

Jafar, reading total 39, Fable 38, ceiling 75. His standing correction first,
because it is about how a turn ends: "Do not stop when work lands. Continue until
the ceiling or a limit; on a limit arm the resume and continue when it fires. The
06:00 brief is a report on the way, not an end. If you find yourself about to end a
turn with work in the queue and budget left, that is yesterday's fault again; arm
the resume instead."

THE GAME LANE, RUNG 1, IN HIS ORDER. Two faults are fixed FIRST because they block
trusting any comparison at all:
  1. Frames with identical inputs must be the same picture. Run 38 proved they are
     not: camA_day and ladder_sun003 carry identical conditions and differ in every
     one of 921600 pixels, the later shot darker by a luma ratio of 0.82. Find and
     fix the shot-order exposure dependence.
  2. The verdict must carry ONE CAMERA LINE PER SHOT (queue 208) so the shadow probe
     can bind. It refuses on every ladder frame today and is right to.
THEN, and only then: bring the SKY DOWN toward the reference rather than pushing the
sun up, then wetness, then worn materials. EACH VERIFIED BY OPENING THE FRAME
against the lower panel of the Hook sheet, which is rule 4 and is the resident's job.

WHEN RUNG 1 HAS A FRAME WORTH HIS EYE it goes beside the panel in the brief and the
studio MOVES TO RUNG 2 WITHOUT WAITING. His words: "my verdict adjusts, it does not
gate." Nothing waits on him.

THE ART LANE IS PROTECTED at a third of the week's points and now QUEUES BEHIND THE
GAME LANE FOR THE RUNNER RATHER THAN YIELDING. That reverses the standing behaviour:
losing a render to a game job that happened to be running is a third of a lane's
output thrown away. A shared concurrency group is still refused, because that makes a
game job wait behind an art job.

HIS CORRECTION TO THE RECORD, AND IT REMOVES AN EXCUSE THIS STUDIO WAS LEANING ON:
Codex's concept sheets were inspected and corrected BY CODEX ITSELF, not by a person.
We had written "with a human eye between each pass" and built a fairness caveat on it;
their PROVENANCE.md says only "selectively edited after visual inspection" and names no
inspector. THE COMPARISON IS MODEL AGAINST MODEL. So it is not a fairness problem, it
is a METHOD problem, and a method problem has a fix: our lane draws the Hook from the
creation prompt, INSPECTS ITS OWN DRAW BY VISION, corrects once, and the result goes
beside theirs captioned THREE PASSES AGAINST TWO. It is sent whatever it looks like.

THEN the twelve-package batch, THE FASCIA FIRST, through all five stations to a real
mesh in the street. Every day after, in the brief, as images: one district sheet
regenerated in-house by the same three-pass method until all seven exist, one batch
package landed as a real mesh, and the Mickey's blockout iterated from its plans
toward a walkable interior shell. The two partial research gaps continue in the
background.

RULES FOR THE ART LANE, both of which cut against this studio's instincts: NOTHING IT
PRODUCES IS WITHHELD FOR QUALITY OR FAIRNESS, it is sent with an honest caption and he
decides; and NO NEW INSTRUMENT IS BUILT FOR IT THIS WEEK, because what exists is
enough to judge by eye.

THE CHANNEL: nothing reaches him except the daily brief and a genuinely Blocking card.
Every decision with a recommendation is TAKEN and logged.

## 2026-09-09 15:55Z: EVERYTHING HE ASKED FOR ON 9 SEPTEMBER IS LANDED

His three owed items and the map ruling are done and pushed. In his order:

1. THE BOT RUNS TODAY'S CODE. Restart job, botPidChanged=True, and the hash his
   machine reported is the CRLF form of the file here, which is why it can never
   equal ours (queue 193).
2. THE SKY LANDED AND WAS JUDGED, and two of the resident's own readings of it were
   FALSE and are corrected in the record: the control quads were hidden correctly,
   and band.skyCentre is a fixed rectangle full of rooftops on the wide cameras
   (queue 194). The before and after are committed as sky_before_after.jpg.
3. MICKEY'S RENDERED, fourth attempt, twelve point eight seconds, five frames on
   art/atlas-01 at 46d7d759 and the sheet at game-design/sim-shots/mickeys_blockout.jpg.
   Three distinct faults had to be cleared first and each was invisible until the one
   before it was fixed: no pwsh, then Blender searched in the wrong place while this
   repo held its real address since 1 September, then a commit step whose every git
   call was malformed by nullglob.
4. THE MAP IS THE BOARD HE APPROVED. 69 tiles, five areas, typed, and it no longer
   claims he ruled any of it. First screen committed as map_first_screen.jpg.

RUNG 1 CONTINUED AND PRODUCED THE MEASUREMENT IT WAS MISSING. Against Codex's sheet
our street has NO DARK IN IT: median 0.6992 against 0.3568, darkest twentieth 0.3249
against 0.1093 (CORRECTED 19:55Z, the first pair measured the sheet's caption
band; see findings.txt at the 2026-09-09 EVENING block). The cause is named by a control rather than inferred: THE SKY THIS
MORNING DROWNED THE SUN, which is still a bare literal 3.0f. Queue 205 is the ladder
that answers it and it is UNBLOCKED as of 15:36Z, because the probe is a game workflow
and starting one would have destroyed the art render in flight.

QUEUE ITEMS FILED TODAY FROM MEASUREMENT RATHER THAN FROM OPINION: 193 to 207.

THE 06:00 WAKE IS ARMED ON TWO RAILS and needs nothing further: the server Routine
fires 2026-09-10T04:07Z into this session, and production/wakes carries the disk
record, amended three times today with what the message must carry, what it must
admit, and what it must not oversell. THE SPLIT IS RETIRED FROM THE DAILY BRIEF.

WHAT THE MORNING MESSAGE HAS TO WORK WITH, all committed under game-design/sim-shots/:
rung1_vs_reference.jpg, mickeys_blockout.jpg, sky_before_after.jpg,
map_first_screen.jpg.

## 2026-09-09 13:45Z: THE MAP IS THE BOARD, THE SKY IS IN, THE RENDER WAS BLOCKED

SUPERSEDED IN PART BY THE 15:55Z SECTION BELOW IT IN TIME AND ABOVE IT ON THE PAGE:
the render is no longer blocked, it ran, and the previews are committed. Everything
else in this section still holds.

Jafar, reading total 31, Fable 33, ceiling 75. Three owed items and a ruling on
the map. Two owed items are done, the third is blocked and the blocker is named.

LANDED, 60405a13. The map page is the heatmap he approved: 69 tiles in five areas,
three colours, none hidden, the prose areas moved below the fold as the audit view.
The inventory went 27 entries to 69 and its status from evidenced to TYPED, which
is a change of contract, so it went to a director:
game-design/decision-2026-09-09-ruling-typed-systems-inventory.md answers five
questions and dictates six edits, all applied.

WHAT THE BOARD CANNOT DO, and it is his instruction that does not hold at this
size: every system a tile AND one phone screen stop being compatible at about 21
systems. 506 px of overhead plus 16.1 px a tile, so 844 px holds 20, and he named
25 player-facing systems himself. The page keeps every tile and says on its face
that it scrolls. Taken as a decision with a default, not sent as a card.

STILL OWED ON THAT PAGE and it is why the first screen is not yet his to judge:
the board says "ruled by Jafar and updated by his rulings" while 62 of 69 tiles
are a builder's reading and 7 a director's. Nobody has ruled one. A builder is on
it now, adding the computed attribution line plus the `short` and `where` fields
the ruling ordered.

THE SKY LANDED AND TWO OF THE RESIDENT'S OWN READINGS OF IT WERE FALSE. Both were
whole-run keys read as if they described one frame. The control quads were hidden
correctly (controlQuadHidden=3/5 names the rung-1 camera; controlQuads=3/3 is a
PLACEMENT count). And band.skyCentre is a fixed pixel rectangle read across
cameras whose field of view differs by half, so on the wide ones it is full of
rooftops: cam_A's 0.8459 is not the rung-1 camera's, which reads 0.9323 at spread
0.0078. Queue 194.

THE MEASUREMENT RUNG 1 WAS MISSING. The reference panel beside our frame: median
0.3568 against 0.6992, darkest twentieth 0.1093 against 0.3249 (CORRECTED
19:55Z, see findings.txt). OUR STREET HAS NO
DARK IN IT. The sky lit the street UP when the reference has not more light but
more shadow. Four items filed from opening the frame rather than from a gate: 194
the sky band, 195 no windows anywhere, 196 the street furniture is flat grey and
the phone box is not red, 197 nothing casts a contact shadow.

THE RENDER HE ASKED FOR IS BLOCKED AND THE BLOCKER IS NAMED. The Mickey's blockout
was dispatched on its own push after core-tests cleared, exactly as instructed, and
died in twelve seconds: `pwsh: command not found`. Nine workflows run on his PC,
eight call the PATH bootstrap, and the art lane is the one that does not. It is
also the one the bootstrap lint's hand list never names, so the lint read 0
problems honestly. A builder is deriving that list from the workflows instead. WHEN
IT LANDS, THE REQUEST FILE MUST BE TOUCHED AGAIN: the art workflow triggers on a
push to production/pc-ops/art-preview.request and an unchanged file starts nothing.

IN FLIGHT RIGHT NOW, three builders, none of them committing:
  the board's `short` and `where` fields plus the attribution line
  the art lane's PATH bootstrap and the lint that should have caught it
  queue 197's measurement half, naming why nothing casts a shadow

THE 06:00 WAKE IS ARMED TWICE OVER and needs no further action: the server Routine
fires 2026-09-10T04:07Z into this session, and production/wakes carries the disk
record, amended today with what the message must carry and what it must admit is
missing. THE SPLIT IS RETIRED FROM THE DAILY BRIEF, kept as a rule with its
fixtures, because it breaks two of his four register laws.

THREE PICTURES ARE COMMITTED AND WAITING for that message, under
game-design/sim-shots/: rung1_vs_reference.jpg, sky_before_after.jpg,
map_first_screen.jpg.

## 2026-09-09 09:15Z: THE CHANNEL REGIME CHANGE, AND IT RETIRES TODAY'S WORK

Jafar, with a reading of total 25, Fable 24, ceiling 75. His diagnosis first,
because it is the part that matters: "The channel fails because nobody with
judgment sits in it. Replace the machinery with one judgment step."

THAT IS A JUDGEMENT ON WHAT THIS SESSION BUILT. The morning answered a channel
that was not actionable by building MORE MACHINERY: a cards pass, a repaired brief
generator, a page notifier already running. The machinery worked, on its first
real run, and sent him six cards from a stale checkout, one of them withdrawn and
two of the day's missing. He is right that the fault was never the mechanism.

THE FOUR RULINGS, in his words:
1. ONE PRODUCER TURN A DAY writes the single message. It reads the queue, the
   findings, the decision queue, the receipts and the ladder, and decides what he
   sees and what he never sees. THE BRIEF GENERATOR, THE CARDS PASS AND THE PAGE
   NOTIFIER ARE RETIRED. The register stays as a FORMAT CHECK AFTER the Producer
   writes, not as a gate that shapes what is written.
2. The Producer applies the director test itself: no numbers with units, no
   coordinates, no file names, no studio vocabulary. It TAKES every decision that
   has a recommendation and a default, logs it, and reports the notable ones in
   the Sunday summary. THE SIX CARDS ON HIS PHONE ARE RULED AS THEIR
   RECOMMENDATIONS. A card reaches him only when the studio CANNOT form a
   recommendation, at most one a week, with buttons.
3. EVERY BRIEF CARRIES TWO BUTTONS, readable and unreadable. Unreadable means
   tomorrow's is written differently and the Producer says what it changed. THIS
   IS THE ONLY MEASURE OF THE CHANNEL: seven consecutive readable briefs, tapped
   by him, is the acceptance. SELFTESTS DO NOT COUNT.
4. Fix the cards race (queue 189), since one card a week still needs to be the
   right one. NO OTHER CHANNEL WORK.

THEN THE VISUAL WORK THAT DID NOT HAPPEN: the street has no sky, so add one, and
that is the correct fix for the road BEFORE ANY WETNESS; the Hook comparison from
the CREATION prompt in data/concept-prompts.json, not the edit file; the Mickey's
blockout render dispatched. Rung 1 continues. Images and clips arrive INSIDE the
brief.

DONE ALREADY: all eight decisions taken and logged under a new TAKEN BY THE STUDIO
section, WAITING is empty by construction, and the pages card is recorded as
RESOLVED BY EVENTS rather than taken, because the studio decided nothing there and
should not claim to have.

## 2026-09-09 09:15Z: THE ART DISPATCH MUST BE ITS OWN PUSH, OR THE RUN IS LOST

ledger-art-blender-preview.yml YIELDS rather than queues when a game workflow is
in progress, and its list is ledger-probe-unreal, ledger-build-windows,
ledger-build-mac, ledger-core-tests and ledger-ai-playtest. YIELDING LOSES THE
RUN; it does not defer it.

`ledger-core-tests.yml` fires on `tools/*.py` and `ledger/**`. So a push carrying
this batch and the art request TOGETHER starts core-tests, the art lane sees it in
progress, and the Mickey's render is lost rather than queued.

THE ORDER, therefore: land the batch, let core-tests finish, and fire
`production/pc-ops/art-preview.request` as its OWN push with nothing else in it.
Its two lines are exactly:

    commission=atlas-01
    recipe=mickeys-blockout

## 2026-09-09 09:10Z: SMALL, OPEN, AND EASY TO LOSE

The map's visual-ladder block carries one sentence in the third person on a page
written for Jafar in the second: "Every rung is a picture or a session Jafar
clears by eye, so these words are ruled by him". Every tile beside it says "the
street YOU see", "a character YOU control". The ladder file was mine and has been
corrected to second person throughout; this sentence is `tools/map.py` line 1960
and its wording is ASSERTED by `check_visual_ladder_is_ruled_not_measured` at line
3839 (`"ruled by him" in lad`), so it is a two-site change in a builder's file and
not a resident one-liner. Carried into the batch review rather than hand-applied.

## 2026-09-09 07:00Z: JAFAR'S STANDING ORDER, AND IT GATES THE GAME

His words, and the first sentence is the ordering rule for the whole day: "The
channel is not actionable and the art line skipped its visual half. Fix both
before any new game rung." Budget with it: total 16, Fable 17, taken at about
06:00Z, plan is Max 20x, ceiling 75 on the governing meter. Recorded as a row in
production/budget.md with its denominators.

THE ORDER OF THE DAY, his numbering kept:
1. MESSAGES. Every needs-you is its own message naming the exact question, its
   options, the recommendation, the default, the deadline, and a link to that
   one card and nothing else, with tap buttons. A message with nothing for him
   says nothing needs you and nothing more. The brief leads with outcomes, never
   counts, and queue 179 is DONE NOW by his ruling. Every image or clip sent is
   the newest of its kind, dated in its caption.
2. PAGES. The cards page reads the budget from his latest reading. The gallery
   shows the newest images first, dated, all of them, not two embedded files.
   The map page is the project overview: the ladder with the current rung
   marked, the areas as tiles coloured by status, and the next three, readable
   on a phone in five seconds, with no diagnostic text on the first screen. The
   town atlas from art/atlas-01 goes in the gallery as a world page, not on the
   map.
3. WAKES. A trigger that fires mid-turn is lost and it cost him yesterday's
   brief. Make wakes queue until the turn ends, and prove it.
4. ART, THE VISUAL HALF THAT WAS SKIPPED. (a) Regenerate the Hook district sheet
   through the local imagegen lane from concept-final-prompts.json and send it
   beside Codex's hook.png as two images in ONE message; that comparison decides
   whether concept images are made in house, and the previous run answered a
   different question. (b) Run the Mickey's five-camera blockout on his PC
   through the art lane and send the five previews. (c) One message, plain
   English, digesting the atlas-02 research: what was found, what is missing,
   with the link.
5. THE LADDER, visual-first, as a card. Written to production/ladder.md and
   filed as the card "Is this the visual ladder?".
6. THEN START RUNG 1. Art at its quarter share, game the rest. Brief at 06:00.

WHAT THIS REVERSES: the 2026-09-08 ruling "No further channel work this week."
The channel is now item 1 and it explicitly gates the game. The supervisor's
staleness stays a recorded finding.

## 2026-09-09 07:00Z: THE PAGES ARE 36 HOURS STALE, AND TODAY IT IS OUR FAULT

MEASURED on publish run 48, commit 650f0755, 06:28Z. Eight consecutive publish
runs failed this morning, numbers 41 to 48. Run 48 died on our own gate:

    tools/gallery.py --selftest: FAILED. 11 passed, 1 failed, over 10 check(s)
      FAIL the live repository renders a gallery and every check passes
             got: failed=pageBytes
    ##[error]Process completed with exit code 3.

The gallery base64-embeds every picture, the live repository outgrew its own
1000000 byte budget at 1000108, twelve of forty-nine pictures were dropped, and
the publisher runs that selftest as a gate before deploying.

CORRECTED AT 08:50Z, AND THE CORRECTION MATTERS. The resident first wrote that
the pages had NEVER been served. That is FALSE and a director refuted it. Of 48
publish runs, FOUR SUCCEEDED: 12, 13, 14 and 18, the last at 2026-09-07T20:23:12Z
on commit 45de6c21, which is exactly the pageCommit recorded in
production/map-notified.json. So the pages EXIST and were last published about 36
hours ago. THE FAULT IS STALENESS, NOT ABSENCE: every one of the 30 runs since has
failed, so a link Jafar taps opens a real page that does not show what today's
messages describe. That is a different fault with a different fix, and the card
that blamed the github-pages environment protection rule is describing 2026-09-06.

WHETHER THE ENVIRONMENT RULE STILL BITES IS UNKNOWN and is named as unknown: no
run has reached the deploy step since run 18. The order is ours first, un-embed the
gallery, let a run reach the deploy, and read what it says. That card has moved
out of WAITING into a new ON US, NOT ON HIM section of the decision queue so it
does not reach his phone as an ask he cannot act on.

CONSEQUENCE FOR ITEM 1: the per-card link resolves to a 36-hour-old page. The needs-you message
therefore carries the question, options, recommendation, default and deadline IN
FULL, and the link is a convenience rather than the payload.

## 2026-09-09: THE DAILY PROMPT DIFFERS FROM ITS RECORD, WRITTEN HERE FIRST

The daily wake's last line tells the session to compare what it is reading
against production/watchdog-prompt.md and to write any difference here before
doing anything else. THEY DIFFER, by four blocks, each one a ruling made after
the record's last reset on 2026-09-06:

1. The `tools/art-deliveries.py` paragraph and the whole art-branch convention,
   ruled by Jafar 2026-09-08. The record has no mention of it, so a session
   working from the record alone would never walk the art refs.
2. "WHEN SOMETHING IS SILENT, RUN THE EXISTING ENTRY POINT ON THE MACHINE AND
   READ ITS OUTPUT BEFORE PROPOSING A MECHANISM", ruled 2026-09-08 and carried
   in .claude/rules/ci.md.
3. "NOBODY TYPES CONTINUE AGAIN" with the THREE MINUTES OUT resume, ruled
   2026-09-06. This one is worse than an omission: the record carries an OLDER
   wording of rule 13 that the live prompt has replaced, so the record is not
   incomplete, it is wrong.
4. The reference to game-design/art-collaboration.md.

THE RECORD'S OWN WARNING IS WHAT CAUGHT IT: "THIS IS A SECOND COPY AND SECOND
COPIES DRIFT... The file cannot detect its own staleness; only the session
reading both can." It worked, three days late, because no session had compared
them since 2026-09-06. production/watchdog-prompt.md now carries the prompt as
received at 2026-09-09T04:09:00Z with the stale block kept beneath it, so the
drift is readable rather than described.

AND THE SAME WAKE NAMED THREE THINGS THIS SESSION HAD NOT DONE: read the inbox
(done, 0 inbound messages, so no blocking gap), walk the art branches, and stage
the 194 outbound records this checkout is holding untracked.

## 2026-09-09 05:25Z: THE GRATE IS IN A FRAME, AND IT LOOKS LIKE PALE PLASTIC

HEADING CORRECTED 2026-09-09 09:00Z. It read "READABLE AS IRONWORK" for four
hours and that was half true: the geometry reads, the material does not. Cropping
the subject rectangle out of the frame shows the bars and the gaps both pale grey
with almost no separation. Measured since, by tools/road-brightness.py:
roadCause=MATERIAL-ALBEDO, the kerb texture and not the light. The paragraph below
is kept as it was written.

RUN 36 ON 7a3fa3e. The camera traces before it shoots now: it tried three
standpoints, two were refused with rail_post1 named, and the third had five clear
subject rays and took the picture. grateShotStatus=AIMED, grateOccluded=no,
grateBlocker=none, grateCandChosen=02. ue-walk_05_grate_a.png has the drainage
grate dead centre, diagonal slots and a frame, nothing across it. That is the
piece Jafar named as the accepting case for the whole prop route.

EVERY PREDICTION WRITTEN INTO THE DISPATCH ENTRY BEFORE THE RUN HELD, including
the one that would have refuted the ruling behind it: rows 00 and 01 named a RAIL
piece and not prop_crowd_control_barrier_0. Row 02 taken, its control rectangle
OFF-FRAME as predicted, and the framing angles reproduced the computed series to
0.1 degree.

THE VOTE AND THE GRID AGREE ON THE CHOSEN ROW, 5/5 against 81/81, so on this
geometry the five-ray vote sampled past nothing. That is not the class being safe:
the harness proved the vote CAN miss a 42 mm bar 5.5 cm off centre, and the grid
stays for the run where it does. On row 00 the grid's first blocked cell already
named an infill BAR the vote could only call a post.

WHAT THE PICTURE ALSO SHOWS: the grate and the channel and kerb band around it
render NEAR-WHITE, almost paper, while the asphalt a metre further off in the same
frame is textured dark grey with red aggregate. It reads as a shape and not as
metal. Queue 176, and it is the visual bar rather than the prop route.

## 2026-09-09 03:30Z: EVERY KEY IS GREEN AND A RAILING STANDS IN THE LINE

RUN 35 aimed a camera at the grate and wrote two frames. grateShotStatus=AIMED,
grateRectStatus=MEASURED, grateViewRestoreStatus=RESTORED, walkFramesWrote=7/7,
and a director had checked the camera arithmetic before the run and found it
right to two decimals. THE PICTURE IS OF A CROWD CONTROL BARRIER IN FRONT OF A
WHITE VOID. Cropping the exact subject rectangle the verdict names and enlarging
it shows the guard railing's post and mid rail crossing the subject rectangle,
and the piece itself as a near-white patch with almost no texture. CORRECTED
2026-09-09 by a director who opened the frames: the resident named the wrong
occluder and called the pale patch void. The east kerb's pedestrian guard railing
E8 has posts at x=10, 12, 14 and 16 m in the plane z=3.375, one of them at the
grate's own x, and it stands between the camera and the piece; the crowd control
barrier is on the WEST side at x=22.5 m and cannot be in that frame. So there are
TWO faults and not one: a railing in the line, which this change addresses, and a
near-white render, which it does not.

THE Z-FIGHT READING FROM THAT RUN IS VOID AND MUST NOT BE QUOTED. It measured speckle inside a rectangle crossed by the guard railing's
post and mid rail, over a piece that renders as a near-white patch with almost no
texture. A flat near-white patch is not a surface a speckle statistic can read. Every denominator in it is honest,
which is what makes a correct reading of the wrong rectangle the worst kind.

SO ITEM 2 STANDS WHERE RUN 34 LEFT IT: the grate is a real imported mesh, it
reports collision, it is at the running surface, all from placed bounds. NOBODY
HAS SEEN IT. Queue 172 and 173 carry the two faults.

## 2026-09-09 02:40Z: THE GRATE IS AT THE SURFACE, MEASURED FROM PLACED BOUNDS

RUN 34 ON 31902b7: propFullyBuried=0/23 where it was 1/23 and the one was the
grate, and the reading carries via=loaded-asset, so it is the engine's own bounds
and not arithmetic on a file. propsAsMesh=22/23, propPlacedWithCollision=22/22,
propBurialSubject=.../collision=YES/topM=-0.0650/open=60.0pct,
propCentreWorstMm=0.00.

JAFAR'S ITEM 2 IS MET IN EVERY MEASURABLE PART. The grate is a real imported
mesh, it reports collision, it is at the running surface and it is placed 0.00 mm
from where the file put it. WHAT IS MISSING IS A PICTURE: the run's six key frames
are aimed along the street and nothing points at a 0.40 m square at x 12.0 on the
east channel. A builder is adding one still aimed at it and the z-fight reading a
director ruled must be a number rather than an opinion.

TWO CONDITIONS THE CLIP CARRIES WHEREVER IT GOES, and offering it without them is
the only version that is a fault. A double yellow line crosses exactly 25.0
percent of the piece, lying on it rather than through it, its underside 5.6 um
above the top face. And the top face is exactly coincident with two rendered
solids over about 0.16 square metres, which no number in this repository can yet
call a tie or not.

## 2026-09-09 01:10Z: THE STREET IS MADE OF REAL MESHES AND THE TOWN SPEAKS ITS OWN SENTENCE

RUN 33 LANDED EVERY PREDICTION. propsAsMesh=22/23 where every earlier run read
0/23; propPlacedWithCollision=22/22; the only fallback is pavement_sign, whose
GLB holds three mesh nodes and whose resolver correctly refuses to choose. The
throughput ledger's prop row went from 0 verified pieces to 22 in one run of
5 min 42 s, push to landed evidence.

THE OVERHEARD BEAT COMPOSES AND THE FRAME SHOWS IT.
overheardReplyMode=COMPOSED, overheardSummaryShape=clause where it read
sentence-not-clause, and clipCaptionsBySource=spoken..8/bank..0 where it was
0 and 8, with all eight differing from the bank row they would have burned.
Frame 17 of the clip was opened and reads: "You hear all sorts. The man that did
the window looked straight in at the shop before he ran, and his face is known if
not his name, apparently." That sentence did not exist before the run; it was
built from the rumour the mill carried.

WHAT IS NOT MET IS JAFAR'S ITEM 2, and the reason is geometry, not the pipeline.
propFullyBuried=1/23 and the one is the grate: it sits under the carriageway and
the channel both, 20.00 mm of cover at the west footprint edge and 10.25 mm at
the last sampled cell, so no camera can see it. Queue 162 carries the fix, one
row rising and taking the cross-fall, and it is a street-spec change under the
art line's review. THE GRATE IS A VERIFIED PIECE AND IT IS INVISIBLE, and those
are two different facts.

STILL OPEN AND NOT FIXED TONIGHT, by Jafar's own rule that only findings blocking
items 1 to 3 are fixed: six things the six stills say about the visual bar, led by
no human figure in any frame and a pure white sky. They are in the findings file
with the number that would settle each.

## 2026-09-08 NIGHT: THE CRIME LANDED, THE PROPS IMPORT, COLLISION DOES NOT

THE NIGHT'S ONE REQUIRED OUTCOME IS DONE. Run 32 launched the packaged build on
Jafar's PC and committed two crimes on Quay Street, one seen and one blocked by a
named wall (west_south_bay2), both decided by the ported Observe::Resolve on real
line traces rather than by a script. crimeStatus=COMMITTED twice,
witnessStatus=REAL, gossipStatus=REAL, overheardStatus=HEARD, memoryFiles=2/2,
clipStatus=WROTE at 2381728 bytes. production/next-three.json now has all three
steps in `done`, so the milestone's ladder reads 4 of 4 and the map shows the
goal as current.

THE PROP ROUTE WORKS AS OF RUN 3 ON 7f12005. propImported=15/16 propSaved=15/16
propUassetsOnDisk=16, and sixteen .uasset files are committed under
ue-probe/Content/Ledger/Props/. The grate resolves at 0.0474 mm worst against its
spec box.

RUN 4 ANSWERED THE COLLISION QUESTION AND THE ANSWER WAS YES ALL ALONG.
propCollisionPrims=15/15, propCollisionVia=not-needed/already-had-1=15,
propCollidable=15/15, and the grate itself RESOLVED with simplePrims=1,
bodySetup=present and 0.0474 mm worst against its spec box. The glTF import had
put a primitive on every mesh; nothing needed adding. What is still open is
PLACEMENT: the walk build has never placed one prop mesh (propsAsMesh=0/23) and
the grate sits 13.4 mm under the channel slab that spans it, so no frame can
show it yet. Queue 161 and 162 carry those.

WHAT RUN 3 SAID AND WHY IT WAS WORSE THAN NOTHING, kept because a deleted number
cannot be audited. The paragraph below was written before run 4 landed.
propCollisionPrims=0/15 was not a measurement: the legacy library refuses by
returning -1 rather than raising, the importer believed it, and a refusal became
a measured absence. Nothing read whether any of the fifteen has collision. A
mesh with no body setup photographs clean and a walking character falls through
it, so pilot package one still counts ZERO on the throughput ledger. The fix
landed uncommitted tonight: four add routes and three read routes, each read
back, a three-valued propCollidable, and a status word that separates measuring
a failure from failing to measure.

IN FLIGHT TONIGHT, so a fresh session does not duplicate it: queue 147, porting
StreetVoice.Exchange into the probe so the overheard reply is COMPOSED from what
the gossip mill carried rather than PICKED from a bank by seed. That is Jafar's
priority 3 and the rung above what run 32 achieved.

TWO TASTE CARDS ARE WAITING with defaults and a 2026-09-11 deadline: which bay
Mickey's takes, and how many bays it takes. Queue 155 (the pub's pavement beer
drop) is BLOCKED on both, on purpose: the drop goes in front of the pub's door
and building it first puts a hole in the pavement outside a pawnbroker.

## 2026-09-07: THE PAGES SERVE, THE MAP IS A MAP, AND THE ROUTE EXISTS

PAGES. Jafar allowed the branch to deploy. Publish run 12 attempt 2 landed on
`85b5222a` and run 13 on `284cfb76`. Eleven of eleven earlier runs had failed in
seconds with zero steps executed under an environment protection rule, which no
code change here could have fixed. Queue 139 DONE.

THE NOTIFICATION PATH IS PROVEN, and against the served page rather than a local
build. `production/map-notified.json` records `notified=true why=material-change
changedFields=q2/q3 digest=4917df34e120`, and the page it verified was served
from `284cfb76`, the commit that carried the redesign. The run before it recorded
a BASELINE and wrote nothing, which is the nothing-measured rule working: a first
reading is not a change. Queue 134 DONE. What is NOT proven is that Jafar
receives the message, which needs the bot running.

THE MAP. Rejected by Jafar as a dense diagnostic report and rebuilt as a visual
page: one sentence, the street frame inline, what runs and what to press, then an
SVG chain from player action to consequence, with every SHA and verdict key
behind a tap. Three area states are now DERIVED and each overturns a reading the
old page gave: the street is SEEN, NOT MEASURED rather than nothing measured, and
the word is granted only when the frame is shown; memory is RUNS, UNHEARD rather
than harness-only-with-12-of-12-ok; gossip is RUNS, AND HEARD from a different
fraction answering a different question.

THE STALE PRIORITIES ARE STRUCTURALLY IMPOSSIBLE NOW. `production/next-three.json`
is the one source and the NOW.md heading parser is DELETED, so THIS FILE NO
LONGER FEEDS THE MAP. Do not add a heading here expecting it to appear there.
The half that catches a superseded item is that nobody named it: queue 119's file
still says READY, so no status word would ever have caught it.

THE TELEGRAM TO CLAUDE ROUTE EXISTS AND HAS NEVER RUN. `tools/runner/executor.py`
is the third daemon under `START EVERYTHING.bat`. Hop by hop: Telegram, the bot's
inbox file, the pc-inbox branch, a 15 second poll, a journal line written BEFORE
anything starts, a fetch into an isolated worktree, `claude -p` bounded to 60
turns and 30 minutes, the register check, the outbox, the bot's sweep, a receipt
carrying the platform message id.

`git_call` RAISES on the repository root, because pc-watcher hard-resets it about
once a minute. Exactly one git call sits outside that guard, `git worktree add`,
once, touching no index or ref. The journal lives outside both checkouts.

NOTHING HAS BEEN DELIVERED. `production/outbound/` does not exist, so zero
messages have ever reached Jafar by any path, and the inbound half has never
carried one either. The first double-click of `START EVERYTHING.bat` is the
accepting case for the whole route.

## THE CODEX PATCH IS NOT INTEGRATED AND MUST NOT BE COUNTED

Ruled by Jafar 2026-09-06: "Keep any unavailable Codex patch explicitly
unintegrated. Do not count its reported fixes as completed or let locating it
block this delivery work."

A handoff described a patch from base `de158c2c` to `54c676d` on a branch
`codex/ledger-handoff-2026-09-06`. NONE OF IT IS HERE. There is no `.patch`
file anywhere on this filesystem, no `codex/` branch, and `54c676d` is not a
valid object in this repository. Its stated base matches what was HEAD at the
time, which corroborates the description and is not the patch.

So five reported fixes are UNINTEGRATED and none may be counted as done:
narrowed director review, unknown-reporting game and studio splits, evidence
uploaded before result banking, retained material and shader logs, and Core
novel actions requiring exact authorization. THE LAST ONE IS NOT TOUCHED AT
ALL, deliberately: it restricts functionality to close an authority hole, it
would reject every model-proposed novel state change with the live caller
supplying none, and it stays separate until its behaviour and its review are
resolved.

Where a fix here resembles one of those descriptions, it was written here from
this repository's own evidence and is not that patch. The retained material log
is the clear case: `production/d1-probe/ue-material-log.txt` exists because an
engine-specialist added the step after run 23, and it is what explained
`materialEditorCmdExit=1`.

## THE STREET IS TEXTURED, run 25, and queue 123 is DONE

Landed `87b20592`. The colour control quad renders its four bound colours where
it read chroma max 6 of 255 on the two previous runs; the whole frame with the
quad boxes excluded reads max chroma 133 over 873,860 pixels against a previous
whole-frame maximum of 15.

The third reading I set in advance is INVALID and not failed: it sampled a pane
of glass one metre from the camera while the brick it named sat sixteen metres
behind. Queue 137 inspects a named brick surface unobstructed. Nobody may
report that specific check as passed until it does.

## 2026-09-06, ANSWERED BY LANDED RUN 23: THE MATERIAL NEVER COMPILED

Run 23 landed as `de158c2c`, "UE machine probe from 245e368". Read
`production/queue/123` for the working. The one sentence:

    nothing in the scene was ever rendering M_LedgerSurface, so every number
    this project has recorded about BaseColorMap was about the wrong material.

The evidence, and it is a pair that only makes sense together. Every instance
readback is FULL: `midParamReadback=12/12 midScalarReadback=12/12
texResourceValid=12/12 compMaterialIsMid=12/12`. And neither the textures nor
the scalars reach the pixels: a control quad bound to a 2x2 of pure red, green,
blue and yellow renders chroma max 6 of 255 over 11,880 pixels, and two quads
of one size at one distance with tiling 1.00 against 4.00 render an IDENTICAL
9.0-cell checker. A perfect instance whose parameters change nothing means the
engine default material is on screen, and that material ignores instance
parameters entirely.

CANDIDATES A, B AND C ARE ALL REFUTED BY THE READBACK LINE. The tile pair is
what separated D from the rest; nothing else in this repository could tell
"the parameters do not arrive" from "the material does not exist as far as the
renderer is concerned", because the engine default and our own colour default
are both grey checkers.

The mechanism is a lead, not proven: the normal sampler carries a NULL texture
(`materialNormalDefault=none-of-2-candidates materialDefaultsBound=1/2`, both
engine paths failing in UE 5.8), and the generator's own line 161 says "A
texture parameter with no default can fail to compile".
`materialEditorCmdExit=1` beside `materialScriptReturn=0` is still unexplained.

NOT FIXED. A fix is in flight. `materialStatus=MADE` was printed over a
material that never rendered a pixel, so that word must get HARDER to print,
not easier: no compilation errors WITH positive evidence of a valid rendered
result, never the absence of a raised exception.

## AN UNPUSHABLE PROBE RESULT NOW FAILS THE JOB

`.github/workflows/ledger-probe-unreal.yml`, the "Commit the probe result"
step, ended on an echo and fell off the end with status 0. So runs 18 and 22
both reported SUCCESS having banked nothing, and both times the colour was read
as a landing. It now exits 1 on that path. The two accepting paths are
untouched and still exit 0: "nothing to commit", and a push that worked.

This is the other half of the CI rule this project already carries. "Verify a
job's EFFECTS, not its exit code" tells the reader what to do; it says nothing
about the job, and the job's duty is not to report an effect it did not have.

It does NOT make the evidence survive. A failed push still leaves the frames on
the PC. What it buys is that the loss is loud instead of silent, which is the
difference between losing a run and losing a run plus the hour spent reasoning
about numbers that were never written. As first written the step carried
continue-on-error: true, so the exit 1 failed the step and the job stayed
green; amendment A2 of the ruling of 2026-09-06 removed it, and the sentence
above is true from that commit on.

## SUPERSEDED, kept for the reasoning: the cause named before run 23

## 2026-09-06, THE STREET'S CAUSE IS NAMED, and it is not queue 062

Read `production/queue/123-the-sampler-reads-the-engine-default-texture.md`
before touching anything Unreal. The one sentence:

    the base material's colour sampler renders its own default texture,
    /Engine/EngineResources/DefaultTexture, and not the texture the dynamic
    material instance binds to BaseColorMap.

QUEUE 062 IS DISCHARGED AND WAS NOT SUFFICIENT. Its acceptance is met on
landed run 21 (commit 372fd95): `ue-build.txt` line 12 reads
`materialStatus=MADE materialScriptReturn=0 materialConnections=14/14`. The UV
head is wired and the four frames are still untextured. 062's stop rule (no
further Unreal dispatch) is LIFTED: the number it watched did move, 12/14 to
14/14. Wiring the head is what made this fault readable at all, because before
run 21 every sampler read one texel and a bound texture could not be told from
an unbound one.

The eliminations, each read off a committed artifact and not off a memory:

- The sampler IS connected to BaseColor, because the engine checker appears in
  `production/d1-probe/ue-vign_camA_day.png`. An unconnected sampler could not
  put it there.
- The samplers receive VARYING UVs: the checker on the hanging sign has a
  measured vertical period of 13 px over a 125 px face and the pillar strip 20
  px over 104 px, both detrended by a plane fit first. WITHDRAWN THE SAME
  HOUR, and queue 123 carries the correction: this does NOT prove the MID's
  scalar overrides arrive. The three large surfaces that would decide it carry
  no periodic signal at all after detrending (right wall sd 0.08, road sd 0.13,
  pavement sd 0.15), and flat is what a densely tiled checker mips down to AND
  what an untextured surface looks like. Whether any MID parameter of any kind
  reaches the shader is OPEN, which is why the dispatch now reads the scalars
  back as well as the textures.
- Import and assignment are not the fault:
  `production/d1-probe/ue-vignette-verdict.txt` lines 56 to 71 read
  `piecesTextured=563/593`, `texturesImported=36`, every albedo
  `2048x2048/JPEG-BGRA8/srgb=yes` under `albedoParam=BaseColorMap`. The 30
  unassigned pieces are exactly the four ABSENT surfaces, 10 plus 6 plus 10
  plus 4.
- The names are in the asset: `M_LedgerSurface.uasset` carries BaseColorMap,
  NormalMap, RoughnessMap, TilingU and TilingV in its name table.

THE PROOF, and it names a piece rather than averaging a frame.
`east_parade_bay3` is a brick_red piece, 6.00 x 6.20 x 8.00 m, occupying 308 x
226 px of camera A. brick_red reads `surfaceStatus=RESOLVED pieces=41
piecesAssigned=41/41`, so that piece HAS a material instance with
`brick_red.jpg` bound to BaseColorMap. Its wall face over 16,800 pixels renders
mean RGB (64.9, 66.7, 69.5), R/B 0.934, chroma mean 4.6 and max 7. The texture
is mean RGB (141.4, 131.3, 109.6), R/B 1.290, chroma mean 31.9. THE RENDERED
SURFACE IS COOLER THAN NEUTRAL WHERE THE TEXTURE IS WARM. Overcast light can
drain warmth out of a red brown albedo; it cannot invert the channel ordering.

The camera convention that rests on was established, not assumed: cam_A yaw 0
points along +x, found by trying all four axis conventions and counting piece
centres in frame, 474 of 593 for +x against 66, 5 and 0. A previous dispatch
projected cam_A using cam_B's position and yaw, so its region attributions are
wrong and are not to be reused.

The two weaker whole-frame measurements, kept because they were what pointed
here, both stated with what they do NOT reach:

- Maximum chroma 15 over 230,400 pixels sampled of 921,600. This refutes four
  of the twelve albedo files rendering anywhere in frame: brick_red mean chroma
  31 over 41 pieces, wood 42 over 32, roof 69 over 2, sidewalk texel(0,0) 86
  over 5. It does NOT refute the other five near-neutral ones, asphalt 2, kerb
  0, plaster 7, concrete 7, metal 22, which could render at 15 unnoticed. And
  how many of those 80 coloured pieces sit inside camera A's frustum has not
  been counted, so this is strong evidence and not proof.
- 6,714 of 14,400 eight-by-eight blocks below standard deviation 1.0. Nearly
  half the frame dead flat. This one does not depend on which pieces are in
  shot, which is why it is the load-bearing half.

LANDED AND DISPATCHED. The readback and THREE control quads are in
`e569b24d`, and `c84e8faf` appended run 22 to `production/d1-probe/DISPATCH`,
which is the push that runs the probe on Jafar's PC. Capture the sha before
watching: RUN 22 IS `c84e8faf`, and it is watched BY ANCESTRY, is there a
landed run whose commit CONTAINS it, never by branch movement or run name.

What run 22 answers. On the materials done line, read as a pair and never one
alone: `midParamReadback` and `midScalarReadback` over `midReadbackAsked`,
beside `texResourceValid` and `compMaterialIsMid`. Both short is A, no MID
override of any kind arrives. Scalar full with texture short is B. Both full
with the frames still flat is C.

Candidate D is answered by a picture and by nothing else. Quads `tile1` and
`tile4` are one size at one distance differing ONLY in their tiling scalars;
identical, beside full readbacks, means the base material never compiled and
every number about `BaseColorMap` has been about the wrong material. Quad
`colour` carries four saturated colours built in code, no file, no decode.
READ THE QUADS BEFORE THE KEYS, and read `quadBoxPx` to know where to sample.
The quads take about 5 percent of camera A in the left half, so any
whole-frame statistic from run 22 must exclude those boxes first; the right
half, where `east_parade_bay3` is, stays comparable with runs 18 to 21.

Nothing below this line has run an engine.

THE REGISTER AND GALLERY BATCH IS RULED AND AMENDED. Verdict LAND WITH
AMENDMENTS in
`game-design/decision-2026-09-06-ruling-register-link-band-and-gallery.md`. The
blocking amendment refused date-scoped rules: the gate was reading its rulebook
off the specimen, since a filename date is typed by the writer. Replaced by
`LEGACY_LINK_RULES`, three names frozen, never widening to a file dated on or
after 2026-09-06. All four amendments are applied and every selftest is green.

A RESIDENT ERROR ON THAT SAME GATE, recorded because the shape of it recurs.
The resident filed queue 124 claiming a resumed director can never satisfy
`director_cadence`. IT IS REFUTED, by the director and then by the resident
against the code. `verify.py` 3444 to 3455: the state is unruled only when
`ruling_fresh == 0`, so one stamp naming any fresh row clears it, and fixture
a14 is the accepting case for a killed-and-resumed director already. The
resident read `rulingRowsUnruled=1/2` and treated it as a failing bound; the
same footer said `director cadence ok` and the actual red was
`UNTRACKED/ABSENT TOOL(S)`. Rule 2: the same evidence is owed for WHICH number
a gate reads as for the number itself, and an unbounded reading that moves
looks exactly like a bound that is failing.

## Where this is, 2026-09-02: THE STREET RENDERS, and it is a street

Run 152198e landed all four frames and all three gate numbers came good:
`datumMissing=0/845` (521/845 before the rotation fix), the shapes line
`cylRolled=9 cylPitched=32 cylUpright=105` equal to the CoreTests print, and
`unityYaw=65.0 appliedYaw=65.0` so the sun rotation reached the light. The
Unity half of D1b is real for the first time: shared JSON in, four matched
frames out, nothing hand-placed.

ALL FOUR STILLS WERE OPENED, which is where the next finding came from.
cam_A day: parade on the left, shadows away and a little left, consistent
with bearing 25, which is the only thing that could settle the sun
conversion. cam_B day: square to the parade, roofline in frame, wet road
reflecting. cam_A night is the best frame the project has made. cam_B night
FLOODS, and that is queue 035: same rig, two angles, one of them wrong,
which makes it the rig and not the camera.

WHAT IS STILL MISSING, so nobody reads this as done: no character body, so
the scene is NOT YET an admissible (b) scene under D1b; shopfronts are flat
untextured panels; the plates carry the wrong district (queue 028); nothing
of Unreal renders at all yet (queue 027).

## Two decisions Jafar made on 2 September: RULED

Ruling: `game-design/decision-2026-09-02-tiebreak-reversed-and-the-moat-item.md`.

**THE TIE-BREAK IS REVERSED AND IT MOVES THE WHOLE PROBE.** Unity now wins
only if the visuals are decisively better FOR UNITY, or if the Unreal loop
fails by non-convergence or hand-edit dependence. Otherwise Unreal wins, on
equal as on better. Named consequence, not softened: Unity ahead in one or
two pairs with Unreal ahead in none is a TIE and goes to Unreal.

So the weight moves from (b) the visual ceiling to (a) the loop. Landing
four admissible pairs through a converging loop is now winning, which makes
queue 032's round-trip printer the decisive instrument rather than a
nice-to-have. It rides 027's first UE dispatch.

**THE PREFERENCE AND THE BLIND LOOK COEXIST BY ORDER.** Write A, B or EQUAL
for each pair on the D8 decomposition, and why, BEFORE any label is
unmasked; the tie-break is applied to that sheet afterwards. Today no blind
look is possible at all, because both engines commit files named after
themselves. Queue 038 is the fix and WAITS for a UE still.

**D11 AND D12 DID NOT REORDER 027. They exposed something worse:** the queue
held twenty-two ready items and not one of them was a moat item. Queue 037
is that item, engine-neutral C# in Core, not blocked by D1, and it takes the
SECOND builder slot of a day ahead of every governance item.

## A correction to carry, from the ruling

The 20-minute UE round trip is run 16's ESTIMATE with cook and capture in
the loop, not a measurement. The measured figure is a 10-minute median over
9 rows taken before either was in it. That gap is exactly why 032 rises.

## Budget: RUNNING, at a measured pace rule

32 percent at 14:40Z on 2 September. The period is NOT a calendar week: the
one-time Tuesday reset restarted the counter and the next reset is the
normal Monday 14:00 CEST, so about 136 hours, of which roughly 14 percent
had elapsed against 32 percent spent. That is 4x over pace.

THE ALLOWANCE IS ABOUT 10 POINTS A DAY, roughly five spawns including the
resident's own turns. The rule and its arithmetic are in
`production/budget.md`. Three parts: two or three builder spawns a day and a
director only on a mandatory trigger; brief with facts inline rather than a
reading list; batch related work into one spawn rather than several.

WORK IS RUNNING AND THE DAILY ALLOWANCE IS RETIRED. Jafar, 2026-09-02: "I
don't care if we get to 80% before monday, we just stop when our budget is
used up". So there is no daily ration; run to the ceiling and stop there.
The 80 percent ceiling still binds and the other 20 percent is his.

IMAGEGEN RUN 1 RAN AND FAILED AT ONE SETUP STEP, AND THE FIX IS LANDED. Run
33654488608 on b8b805f2: the API's per-step conclusions put the only
failure at `The commit this run is measuring`, 0 seconds, and the four work
steps skipped behind it. Cause, from a differential over .github/workflows:
that step ran git without the safe.directory env every other git step on
ledger-pc carries, and the commit step's own git rev-parse succeeded under
it in the same run. The summary that named three causes it never observed
is replaced by tools/runner/step-verdict.sh (three states plus
NO-READABLE-OUTCOME, 32 checks). Ruling:
game-design/decision-2026-09-02-imagegen-run1-stopper-and-run2.md.

A SECOND FAULT IS NAMED AND NOT YET PROVEN: run 1 printed a verdict and
then `staged=0`, so the verdict never reached the committed channel.
Reading: Windows Python ends every stdout line in \r\n and bash keeps the
\r, so `[ -e "$f" ]` looked for a name ending in a carriage return. Run 2
prints every candidate with %q and strips it, which is the measurement.
The vignette-fetch loop is the same shape and has never staged a file in
this tree either (no fetch-verdict.txt, no surfaces/); queue 044 carries it.

## THE ASSETS ARE NOT IN THE FRAME (queue 046, found 2026-09-02)

37 props and 14 generated decals sit in this repository and THE STREET SCENE
USES NEITHER. Measured: `grep -c "base-mesh|BaseMesh"` returns 0 in both
`StreetVignetteHost.cs` and `StreetVignette.cs`, and no C# file names any
generated decal by key. The four frames Jafar has seen are built entirely
from primitive shapes.

BUILT IS NOT RUNNING, and the resident missed it while reporting asset
counts as progress. Jafar found it by asking what the images are FOR.

This outranks generating more pictures. The overnight batch adds 31 files to
a directory nothing reads: worth doing because it is free, but it moves no
number the Meridian Test measures. Queue 046 is what turns the inventory
into a street, and it is also the only way to learn whether a generated
decal looks right AT SIZE, ON A SURFACE, IN THE RAIN.

## In flight

- **THE HOURLY WATCHDOG IS OFF UNTIL MONDAY, AND HERE IS HOW TO PUT IT BACK.**
  Silenced 2026-09-04 on Jafar's instruction. It is `trig_01EA7ybQTcsiFyrTryptqVUi`,
  cron `20 * * * *`, and it is NOT a free reader: `persist_session` is true and
  its payload is a `type: user` message, so every firing delivers a user turn
  into this session and costs a cache read of the whole conversation plus
  output. About 76 firings sat between that instruction and the Monday reset,
  against 3 points of headroom.

  RE-ENABLING IS ARMED, not remembered: `trig_011GMwPxL5vvqrpb8Nxyzedw` is a
  one-shot at 2026-09-08T12:00:00Z that fires into this session and re-enables
  the watchdog first, before anything else. IF THAT ONE-SHOT FAILS, the
  watchdog stays off silently and nothing will say so, which is why this note
  exists: call `update_trigger` on `trig_01EA7ybQTcsiFyrTryptqVUi` with
  `enabled` true and NO prompt field, read it back to confirm, and delete this
  bullet.

  A note on the warning that came back when the one-shot was created: it said
  fired sessions run without connector tools, which would matter because
  re-enabling IS a connector call. It does not apply to a `persist_session`
  trigger. The evidence is the watchdog itself, which carries the same empty
  `mcp_connections` and has been firing into this session since 1 August while
  the session plainly has those tools.

- **MONDAY'S ORDER, queued 2026-09-04, START NOTHING BEFORE THE RESET.**
  Jafar ruled: spend nothing until Monday 14:00 CEST. The order below is
  PROPOSED and is confirmed by a fresh reading of BOTH meters on the day, not
  by this list. If the reading is not comfortable, the order shortens from the
  bottom; it does not start anyway.

  1. **Queue 062 step 2**, the third material status word. Small, and a
     precondition to the next dispatch.
  2. **Unreal run 21.** These two are first because they are the only items
     that end in something Jafar can LOOK AT: four frames that are not flat
     grey. If 21 prints `materialConnections=12/14` again, that is the answer
     and it gets reported, not retried, and D1's hand-edit clause is invoked.
  3. **Queue 080**, the send check that leaves no trace it ran.
  4. **Queue 079**, the queue gate reading `game-design/queue.md`, retired on
     31 August.
  5. **Queue 078**, the inventory of every list that means machine-written.
  6. **Queue 081**, the two small producer-check tidies.

  QUEUE 067, THE TELEGRAM BOT, LEFT THIS LIST ON 2026-09-04: Jafar moved it
  BEFORE the reset so that Monday is a full game day rather than a setup day.
  See the bullet above.

  Items 4 to 7 are all small and all found by grep at zero cost this week,
  which is the argument for doing that kind of looking whenever the meter is
  tight.

## 2026-09-06 04:10Z: THE FIRST DAILY WAKE RAN ITSELF, AND ITS BRIEF IS HELD

The daily trigger fired for the first time and did its own order unaided: read
the inbox, checked the budget, generated the brief from repo state. Nobody
wrote a word of it.

TODAY'S BRIEF IS GENERATED AND NOT SENT. It is kept VERBATIM at
`production/briefs/2026-09-06.md` because the tool's real output is the
evidence; the reasons live here rather than on top of it, since the register
gate correctly refuses a brief with a preamble and the resident learned that
by failing it.

TWO FAULTS IN ITS BUDGET SECTION, both filed:
- IT SAID TWELVE SESSIONS WENT TO THE GAME. ONE DID. The split counts WHICH
  AGENT TYPE ran, not what it built, so nine console passes by
  engine-specialists counted as game work on the most studio-heavy day this
  project has had. That is the number Jafar's item 5 rests on and it pointed
  the wrong way. QUEUE 111.
- IT DID NOT SAY THE DAY IS UNMEASURED. Newest reading 2026-09-05 08:30Z with
  27 sessions since, so the stop condition held and the brief printed only
  "taken yesterday", which reads as reassurance. QUEUE 112.

NO BUILDER WORK STARTED. An unknown budget is not permission.

THE "PASSED THE REGISTER" CLAIM IS CORRECTED, 2026-09-06, amendment A5 of the
ruling on the register's link band. Grepped repo-wide for the SENTENCE and not
the site, per rule 1: six hits, three of them inside the ruling record itself
that names the correction. The three real sites are
`game-design/decision-2026-09-05-ruling-build-batch-and-roadmap-fold.md` lines
271 and 432 and `production/queue/095`, and all three now carry the dated
correction. NOW.md was named as a possible fourth and IS NOT ONE: it carries no
such sentence, and what it does say about that message is the paragraph below,
which was already right.

NOTHING HAS COME THROUGH THE BOT. `inbox-read` reports nothing measured, the
`pc-inbox` branch does not exist, and `outbound: records=0`, so the report
written on 2026-09-05 was never sent. That points at the bot not running with
that day's code rather than at the transport, which is untested either way.

## IN FLIGHT: THE ORDER OF WORK, ruled 2026-09-05 section 8

His list is the order; this is only about which files two builders cannot
share.

1. **088 alone, first, reviewed and committed on its own** so it lands early.
   Everything in item 1 stacks on its branch, and Jafar can test the transport
   tonight by sending the bot one message.
2. In parallel after it lands: **089 with 091** (both are the sender on the PC,
   one loop, one file), and **095 with 079's half** (a new tool,
   `producer-check.py`, `run-night.ps1`, the footer's counter). One review for
   the pair.
3. **090 with 104** (both are the bot's input handling), then **094**, then
   **093** when Jafar has two minutes and not before 088, 089 and 090 land.
4. Then **096, 097, 098, 099, 100** with its own stamped ruling, then **101**.
   After 100 lands the studio stops building studio; 101 still runs because it
   is item 5 of his order rather than a new process item.
5. Then the game: **062 step 2, run 21**, the first textured frames to him as
   images through 091. Then **102**, whose content-type choice is a director
   ruling. Then **103**, after 094 and 095.

THE VERIFY FOOTER'S `22 queue items ready` READS THE RETIRED QUEUE (079) and is
NOT TO BE QUOTED until 095 lands its counter.

## THE WEEKEND, RULED BY JAFAR 2026-09-06: GAME WORK ONLY

TWO ITEMS, IN THIS ORDER, AND NOTHING ELSE:
1. FIND THE CAUSE OF THE UNTEXTURED STREET and get Meridian's textures onto it.
   The wire moved to 14/14 and the frames changed; staging ran
   (`stagedTexFiles=102/102 piecesTextured=563/593`); the street still renders
   the ENGINE CHECKER and the cause is UNKNOWN.
2. QUEUE 119, the three unbriefed players. SUPERSEDED THE SAME DAY by Jafar's
   ruling to run the comparison in the studio: the sweep ran
   (production/stranger-test/, queue 127, lieHeard=0/90) and the redesign is
   queue 131, which waits for 129.

EVERYTHING ELSE WAITS FOR MONDAY unless it blocks those two: the remaining
audit items (114 to 118, 120 to 122), all console work, all tooling. ANY NEW
TOOLING OR PROCESS ITEM DISCOVERED THIS WEEKEND GOES TO THE QUEUE AND WAITS. It
does not get built.

SPEND DOWN TO ROUGHLY 75 OF 80 BY SUNDAY EVENING AND STOP THERE. Fable governs
and read 33 on 2026-09-06 at about 04:20Z. FRAMES COME TO HIM AS IMAGES.

THE ONE EXCEPTION, because he ordered it in the same message: the brief
register and the gallery page, since the first brief was wrong and he wants
today's rewritten in the new shape and SENT so he can judge it.

## NOBODY TYPES "CONTINUE" AGAIN, ruled 2026-09-06

A turn ends for the ceiling, a limit, or a genuine blocker. EVERY OTHER ENDING
ARMS THE RESUME: a one-shot three minutes out to take the next item, armed
BEFORE the turn ends, while queue items and budget remain. Rule 13 in
CLAUDE.md and the daily trigger both carry it.

CONVERSATION IS THE POINT OF THE CHANNEL. A message arriving in the inbox while
a run is going is ANSWERED IN THAT SAME RUN, by the Producer, in the register,
and the bot sends it. A QUESTION SITTING UNANSWERED IS A BLOCKING GAP, not a
queue item.

THE BRIEF'S SHAPE WAS WRONG AND IS RULED: images as Telegram images, never as
links; at most two links and never to a repository markdown file, only the
glance, map or gallery; everything else in plain words; and it LEADS WITH WHERE
THE PROJECT STANDS AND WHAT CHANGED FOR THE GAME, not with what was engineered.
Twenty seconds to read and feel informed. Fifteen links to markdown files is
not a director update.

## 2026-09-06: AN OUTSIDE AUDIT FOUND THREE THINGS OUR GATES CERTIFIED GREEN

A different model family audited this project. Jafar verified all three
findings himself and ruled: TREAT THIS AS EVIDENCE ABOUT OUR PROCESS, NOT AS A
SUGGESTION. Filed as queue 113 to 120. THE ORDER IS HIS, P0 FIRST, and it
outranks the 2026-09-05 order below for everything not already in flight.

P0, STOP THE LINE. Queue 113 and 114. `IntentRouter` takes `check`, `effect`
and a magnitude from model JSON; `Checks.Known("none")` is true; and
`Adjudicator.cs:62` is `case Checks.None: break;`, which falls through to Pass
and CANNOT REFUSE ANYTHING. So the model both proposes an action and picks the
check that would have constrained it, then DialogueUI applies the effect to
real state. THE MODEL IS ADJUDICATING, INSIDE THE LAYER THIS PROJECT IS NAMED
FOR. Re-verified in the code by the resident, not taken on report. Our own
CoreTests case that proves checks CAN fail SKIPS `Checks.None`, so the suite
certified the hole by trimming its denominator to the passing cases.

P1: queue 115, canon says nothing is ever wiped and MemoryStore prunes at 600
under a comment saying that is not forgetting; queue 116, the soak printed NOT
GATED and ran on SEVEN agents while being cited for hundreds.

P2: queue 117 groups the evidence that cannot disagree with us (a self-rating
of 93 cited as a premise in D12, a judge calibrated on 48 passes and ZERO
fails, the split of queue 111, the soak citation); queue 118, a verified piece
whose tone gate is pending.

AHEAD OF ANY REMAINING CONSOLE WORK: queue 119, the cheapest test of the
differentiator. Three unbriefed people, one crime, real propagation against
canned responses. Jafar: "If they cannot perceive a difference, that is the
most important finding this project can produce." It is designed so it CANNOT
come out well by construction, which is the opposite of the 117 group.

QUEUE 120 produces our own cost per verified piece against the audit's, which
puts the stated 300 to 500 resident town at 14 to 34 weeks of full budget for
content alone. THE SCOPE DECISION IS A CARD FOR JAFAR, not a change the studio
makes.

ITEM 6 IS UNFINISHED, NOT SOLVED. The wire moved to 14/14 and the frames
changed, and the street still renders the engine checker with 563 of 593 pieces
assigned. THE CAUSE IS UNKNOWN. Keep it open and find it.

BALANCE, ruled the same day: 63 of 106 queue files were infrastructure and 85
of the last 100 commits touched no game path. Mandatory director review is CUT
for documents and routine assets and KEPT for simulation changes and anything
touching Core. CLAUDE.md carries it.

## JAFAR'S STANDING ORDER, 2026-09-05. THIS REPLACES EVERY EARLIER ORDERING.

Readings taken at about 08:30Z after an EARLY RESET: total 7, Fable 8, ceiling
80 on both, higher governs. No crossing this week. The early reset is a REGIME
CHANGE and every rate computed before it is void, as on 1 September.

TWO STANDING RULES OVER THE WHOLE LIST. After item 4 lands, THE STUDIO STOPS
BUILDING STUDIO THIS WEEK and any new process item goes to the queue and waits.
Every brief reports the STUDIO VERSUS GAME split of points.

JUDGED SUNDAY: if Jafar can run the week from one Telegram thread and know what
is happening, the console is done.

1. **Close the Producer loop over Telegram.** Inbound: anything he sends the
   bot lands as a dated file in an inbox and reaches the session through the PC
   channel, never waiting more than a few minutes. Outbound: the Producer
   answers in the register, the check runs on the SENDING side, the bot sends.
   Rulings: every card arrives with option buttons and a tap writes the ruling
   into `production/decision-queue.md`. Images: every verified visual lands as
   an image with one caption line. Readings he taps reach the repo without him.
   ACCEPTING CASE: he sends a question from his phone and gets a
   register-compliant answer back, and he taps a button and the queue shows the
   ruling.

   088's CONTAINER HALF IS IN. The transport has two named holes until queue
   090's pass: a message sent while the PC bot is OFF is skipped at its next
   start and never filed, and a fresh clone of the PC checkout rewrites
   `pc-inbox` from its own disk. The daily trigger now calls the reader
   (`trig_013itgDeay6t41BHEmaYFbAj`, set 2026-09-05T11:38:02Z, recorded whole
   in `production/watchdog-prompt.md`).

   INBOUND CLAUSE AMENDED PENDING JAFAR'S RULING; the proposed sentence and the
   reason are in
   `game-design/decision-2026-09-05-ruling-standing-order-refill-and-the-wake-half.md`
   section 1.4; queue 092 prices the wake.

1b. **Limit visibility.** When a session or weekly limit is hit, the reset time
   is PARSED FROM THE NOTICE and written to a file the bot reads; the bot says
   "studio paused, back at HH:MM" and again when it resumes. A studio silent
   more than two hours with no reset time on file is flagged as a Blocking
   item. The runner SLEEPS until the parsed reset rather than spawning into a
   closed session.

1e. **Part of 1b, and it starts NOW by hand.** When a limit is hit, arm a
   one-shot trigger for the parsed reset whose instruction is to resume the
   current item and continue this order. From the first limit onward, by hand
   until 1b is built. NO RESET SHOULD EVER NEED JAFAR TO RESTART THE STUDIO.

1c. **The brief is GENERATED FROM REPO STATE BY A TOOL** and pushed by the bot
   every morning. Not written by hand in a session.

1d. **A recurring daily trigger** wakes the studio, plans the day and produces
   the brief. THE HOURLY WATCHDOG STAYS OFF in favour of it. Live as
   `trig_013itgDeay6t41BHEmaYFbAj`, 04:00 UTC daily, which is 06:00 CEST, so
   the brief is on his phone before 07:00. The Monday one-shot that would have
   re-enabled the watchdog was DELETED on 2026-09-05.

2. **Nothing reaches him outside Telegram.** The session's own pop-up questions
   become cards. If something can only be answered on the floor, THAT IS A GAP
   TO FILE, not a reason to page him there.

3. **The glance page, phone-first:** overall state as a colour and one dated
   sentence; needs-you count and top item; next visible thing and when; the
   latest image; the budget bar on both meters. Everything else one tap down.

3b. **The glance publishes to GitHub Pages** so it opens on his phone. IF PAGES
   IS REFUSED FOR ANY REASON, SAY SO rather than leaving a file he cannot read.

4. **Player-facing systems inventory, as DATA not prose.** One entry per
   system: name, area (moat, world, player-facing, content, studio), status
   (exists, partial, absent), class (cheap to author, taste-bound,
   moat-adjacent), phase, and what blocks it. At minimum: the Ledger notebook,
   HUD, menus, controls, camera, first hour and tutorial, save and load, new
   game, settings, accessibility, subtitles, gamepad, pause, map and minimap,
   inventory, economy and trading, combat, music, SFX, audio mix, loading and
   streaming, failure states and autosave policy, time and calendar display,
   graphics settings including the local-LLM toggle, credits and attributions,
   photo mode, feedback path. THEN RENDER IT AS THE MAP VIEW: every system a
   tile, grouped by area, coloured by status, one screen, phone-first, tap a
   tile for status, blocker and decisions. It sits BESIDE the glance, not
   inside it: the glance is today, the map is the whole. Then fold the
   inventory into roadmap-v2 as phases. Research on the taste-bound systems is
   coming separately from the planning session.

5. **A weekly planner role, cheapest tier,** whose only job is the larger plan:
   read the roadmap, the map and the week's landed items, and report whether
   the week MOVED THE PROJECT or MAINTAINED THE STUDIO. External evidence Jafar
   cites: practitioners running long autonomous builds report agents that keep
   working, get absorbed in small details and stop improving the project, and
   the fix is a coordinator holding the plan while others do the work. Our
   resident does both jobs. Flag it when several consecutive items are
   self-maintenance.

6. **Then the game:** 062 step 2, run 21. THE FIRST TEXTURED FRAMES COME TO HIM
   AS IMAGES.

7. **The pilot assembly line,** which Phase 0 requires and the queue does not
   contain. Run ONE content type end to end, spec to author to verify to
   integrate to record, and report THE COST PER VERIFIED PIECE IN POINTS with
   the calibration it rests on. This is the number the whole plan rests on and
   nobody has measured it. The studio chooses the content type and says why.

8. **One supervised trial night this week:** a small queue, the runner
   unattended, and a report in the morning on what it did and what broke. THE
   NIGHT RHYTHM IS UNPROVEN until a night has actually run, and
   `production/logs` is empty.

9. **Then the hygiene queue in filed order.**

10. **Meter readings: NO PRESET BUTTONS.** Ask for the exact number and take it
   as typed, numeric keypad where the platform allows, REJECT anything that is
   not an integer rather than rounding it. Presets are for rulings, never for
   measurements. This overrides the button grid the bot shipped with on
   2026-09-04.

11. **A note, not a task.** A widely-shared 2026 build of an impressive Unreal
   world by an autonomous agent used EXISTING assets including MetaHumans and
   ASSEMBLED rather than authored them. Our bias for bought and free Epic
   ecosystem parts over generated ones is confirmed; the studio's job is
   assembly and logic. Relevant to D1 and D2, NO CHANGE to either.

- **SUPERSEDED BY THE ORDER ABOVE: THE CEILING IS CROSSED, DELIBERATELY, ON ONE ITEM. Read 2026-09-04 at
  about 08:30Z: total 82, Fable 83, ceiling 80.** Jafar chose to spend past the
  line on the Telegram bot alone, so that Monday is a full game day. THIS IS
  HIM SPENDING HIS OWN 20 PERCENT AND IT IS HIS TO SPEND. No session may read
  it as the ceiling having gone soft, and the 80 line binds again the moment
  067 is done or its cap is hit.

  HIS CAP, and it is mechanical: one builder, one director review, STOP at 6
  points spent or at the first failed accepting run on the PC, whichever comes
  first. NO FIX LOOPS BEFORE THE RESET: a broken bot waits for Monday. At least
  8 points stay untouched for Monday morning. Checked rather than accepted: the
  governing meter is Fable at 83, so 17 remain to 100, 6 spent lands at 89 and
  leaves 11, clearing the floor of 8.

  SCOPE CUT BY THE RESIDENT, because 067's six acceptance clauses do not fit in
  6 points. Building: the launcher, the config read, a two-way message, an
  unprompted push, and the budget-reading ask with numeric quick-replies for
  both meters. NOT building, and these stay Monday's: gallery images, decision
  buttons that write rulings, voice memos with local transcription. 067's
  acceptance is therefore NOT fully met by this run and the item stays open.

- **SUPERSEDED, kept for the series: NEAR-STOP AT 3 POINTS, read at 00:30Z.**
  Total 77 percent, Fable 76, ceiling 80, about 84 hours to the Monday
  14:00 CEST reset. The higher meter governs and this time it is the TOTAL,
  which is the reverse of 1 September, so no session may infer one meter from
  the other. The limit Jafar hit on the evening of 3 September was the 5-hour
  SESSION limit; the weekly meter did not reset and the arithmetic in
  `production/budget.md` still stands. One builder spawn is a material
  fraction of what is left. Spend nothing without a fresh reading or a direct
  instruction, and prefer zero-cost work: two of today's findings (queue 078
  and 079) were found by grep and cost nothing.

- **THE DATED HAZARD IS DISCHARGED, 2026-09-04.** It said the tree would go
  red at 2026-09-05T09:01Z by itself, because `producer-check.py` measured the
  committed message's deadline against the wall clock. Queue 077 landed and
  the gate now pins each file's clock to the ISO date in its own name. Proven
  at the exact instant rather than inferred: `--gate --now 2026-09-05T09:01`
  reads `PASS filesChecked=1 filesExempt=5 filesWalked=6 filesDatePinned=1/1`,
  the same verdict it gives today and in 2027. Ruled in
  `game-design/decision-2026-09-04-ruling-077-deadline-clock-pin.md`. The
  residue is queue 080: a date is a day, not an instant, and nothing in the
  tree proves the pre-send check ever ran.

- **LANDED 2026-09-03, one commit, ruled in
  `game-design/decision-2026-09-03-batch-review-register-banner-spawnlog-uvsweep.md`:**
  the register gate (walks the outbox and the briefs on every verify; its
  accepting artifact is now the served message read at THREE clocks in one run,
  `--gate`, `--now 2026-09-08T12:00` and `--now 2027-06-01T12:00`, all PASS at
  `filesDatePinned=1/1`; the single reading of 3 September was accepting at one
  instant only, ruling of 4 September section 4), the banner law (135 documents
  migrated,
  the retired form refused), the spawn log's tier and turn fields (hook
  REGISTERED, first row NOT YET READ: read it before quoting it), and the UV
  head sweep (nine candidate pin names in one run, not yet dispatched). Open
  holes are queue 073, 074, 075 and the steps added to 024 and 062.

- **THE UNREAL STOP RULE IS DISCHARGED, RUN 21 LANDED 2026-09-05.**
  `materialConnections=14/14`, up from the 12/14 that held across runs 19 and
  20, taken by the FIRST of nine candidate pin names
  (`materialUvHeadTriedAtWorst=1/9`) with `materialUvHeadByPropertyWrite=0/2`,
  so `materialStatus=MADE` is honest and the third status word did not fire.
  THE FRAMES CONFIRM IT INDEPENDENTLY: the flat grey of the last two runs is
  gone and a checkerboard tiles correctly in perspective, which a count cannot
  fake.

  THE STREET IS STILL NOT MERIDIAN AND THE CAUSE IS UNKNOWN. Staging RAN
  (`stagedTexFiles=102/102 piecesTextured=563/593` in
  `ue-vignette-verdict.txt`), so the frames show the engine checker on
  surfaces the verdict says were assigned, which is an UNNAMED fault and the
  next thing to find. The resident first blamed the staging step, having
  grepped `ue-build.txt`, a file that has never carried those keys; the
  correction and both refuted claims are in queue 062. Do not re-derive the
  wrong answer from the old sentence.

- **THE DIRECTOR'S CONSOLE EXISTS AS FAR AS STEP 2.** `production/decision-queue.md`
  is the single home for anything awaiting Jafar and for lighter rulings; the
  legacy `game-design/decisions-pending.md` is RETIRED and carries a pointer.
  The Producer is the only role permitted to address him (CLAUDE.md, and
  `.claude/agents/producer.md` carries the register). Constitution law 12 sets
  evidence beside the sentence for agents and behind it for Jafar, with the
  link REQUIRED rather than optional.

- **THE REGISTER CHECK IS REAL AND IT REFUSED THE RESIDENT FOUR TIMES.** The
  first live Producer message failed on missing options, a missing deadline and
  twice on length before it passed. Pointing at the card instead of restating
  its options is exactly the vagueness a word cap alone teaches, which is why
  the link and the options are floors rather than suggestions.

- **BUDGET: TWO METERS NOW, AND THE HIGHER GOVERNS.** Total was 60 percent at
  10:25Z; Fable was not read. On the only day both were read, 1 September,
  Fable was 41 against a total of 34. Directors run on Fable, builders do not,
  so the meter that moves on reviews is the one this file used to be blind to.
  A row where Fable was not read says `not read`, never zero and never the
  total carried across.

- NOT DISPATCHED AND DELIBERATELY: `production/d1-probe/DISPATCH` is a push
  trigger. Do not touch it in a commit unless an Unreal run is wanted, and the
  stop rule says one is not wanted until 062 lands.

- **DO NOT COMMIT WHILE A BUILDER IS WRITING**, however loudly a stop hook
  asks. That is CLAUDE.md's rule and it exists because the resident once ran a
  checkout over a builder's uncommitted work and cost a whole session.

## THE DASHBOARD IS NOW A HOSTED LIVE PAGE, and it needs writing to

Published 2026-09-02 after Jafar refused to double-click anything to see
current state, in his words: "not running a bat to update a dashboard. your
job is to keep it up to date all the time, that's the whole point."

    https://claude.ai/code/artifact/2c3da7c0-8b8e-4626-8e73-2498acbe6ed8

It holds NO numbers of its own. It subscribes to the artifact document store
at `status/current` and repaints when the document is written. So:

    python3 tools/dashboard/build-dashboard.py --emit-json
    then write tools/dashboard/live-dashboard.json to status/current

WRITE IT AFTER EVERY LANDING. The page reports the age of its numbers and
turns red when the feed stops, which is honest, but a red feed is still a
reader learning nothing. The writer is the resident and nothing automates it
yet: queue 048. Republishing the PAGE is not needed and should not be done
casually; the page changes only when the generator's renderer changes.

The wake subscription on it did NOT register in this session (the artifact
service refuses them here), so nothing tells this session when it is
republished. Do not claim to be watching it.

## THE IMAGE QA, 45 of 45 OPENED, and the answer is a number

Jafar, 2 Sep: "did you view and QA the images and fix/redo if necessary? are
they built and cropped and shaped in a way that they can be used in UE? QA
should be standard procedure." The resident had opened THREE of forty-five
and published the rest. A verifier then opened all 45, plus 18 zoomed crops,
and confirmed the files are byte-identical to the blobs at HEAD, so the
judgements apply to what the engine will load.

    41 of 45 are SCENE PHOTOGRAPHS, 4 of 45 are plates
     1 of 45 usable as is, and it is probe_wall_cfg1, measurement only
    29 of 45 croppable
    15 of 45 need regenerating
     0 of 45 carry a real brand, real person or recognisable face
    12 of 45 carry people or vehicles the negative prompt already bans
     1 more, sign_telephone, is close to GPO kiosk trade dress: a WATCH ITEM
       for a decision record, not a proven breach, and not a builder's call

THE CAUSE IS ONE LINE OF PROMPT, not 45 problems. Sign, fascia, notice and
poster families carry "photograph, straight-on flat elevation, evenly lit"
plus "deserted empty street", which asks for an object standing in a street
and gets one. The four that came out as plates used a prefix ALREADY IN THAT
FILE: "flat orthographic texture sheet, square-on to the surface, the surface
filling the frame edge to edge", with a negative list naming kerb, pavement,
road, sky and roofline. Four of four. Queue 056 moves the rest onto it and
makes the generator REFUSE a prompt with no framing clause.

TWO MORE SHARED CAUSES. All three interiors came back as exterior shopfronts
when they are meant to be cards seen from inside a window. Prominent
SECONDARY text resolves as broken near-words in eight images, against the R1
big-type-only rule already written in that file: HOOK STREATS, HARBOOR
MASTER, BORHOUGH, PORIE SHUOP.

A CLAIM THE RESIDENT PUBLISHED AND HAD TO WITHDRAW: the gallery page said
headlines come out clean and correctly spelled, written after opening three
images. It is corrected on the live page. And the verifier withdrew one of
its own: it read two signs as perspective-distorted, measured the edge slopes
at 0.27 and 0.07 degrees, and refuted itself. Faces are square-on across the
batch to within half a degree; what reads as perspective is a baked 3D lip on
the surrounding frame.

## THE NIGHT'S DISPATCH ORDER, and why it is this way round

`ledger-pc` is ONE machine, so two dispatches contend and the order is a
decision rather than a detail. It is:

1. **UE probe first**, because it is the risky one. Unreal has never
   rendered the street and the last five probe runs each hit a different
   engine wall. Running it first buys hours to name a wall and re-dispatch.
   Running it last means a 04:00 failure with no time left.
2. **Unity build second.** It is the known-good path, it produces the first
   still of the street WITH the props and decals in it, and it is what
   clears the cross-engine guard by landing a run whose piece count matches
   the file.

WHAT BLOCKS BOTH RIGHT NOW: `ledger/verify.py` is red, so nothing commits and
therefore nothing pushes and therefore nothing dispatches. Two red items:
- the cross-engine guard (file against the last landed Unity run), cleared by
  the queue 041 ahead-of-run key, which is in the UE builder's brief;
- the piece list drift (committed 627, generated 628), caused by the three
  interior pictures landing mid-flight, with the queue 046 builder naming the
  cause before regenerating.
Then a director reviews the three-builder batch, one commit, push, dispatch.

DO NOT SHORTCUT THE RED. The cross-engine guard exists so a judged
Unreal-versus-Unity pair cannot compare two different streets, which is the
one way this whole comparison could produce a confident wrong answer.

## Standing hazards a fresh session will otherwise walk into

- Do not edit `content/dialogue/pub-regular-v1.json`. Those 48 lines are the
  graded judge calibration sample; changing one invalidates it silently.
- The studio split is MANDATORY and was skipped for a full day on 1 Sep.
  Builders build, verifiers verify, the director rules. If a session
  instruction says otherwise, that is a conflict to raise with Jafar in one
  line, not to resolve alone.
- The stop hook will ask for a commit the cadence gate refuses while builders
  hold the tree. That is a NAMED FALSE POSITIVE (queue 014, ruled). The
  constitution wins: never commit a builder's work-in-progress because a hook
  asks.
- `git status` at session start is not a list of YOUR edits. Read the
  In flight section above before assuming any dirty path is yours to commit.
- Every session so far has opened by reading the head of a queue file that
  declared itself superseded on 31 August. Queue 021 fixes it.
