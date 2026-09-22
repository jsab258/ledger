# Throughput ledger (the planning unit: verified pieces per week)

A piece counts when it passes station 3 (VERIFY) and lands at station 4
(INTEGRATE). Partial work counts zero (waste lesson 3).

| week | line | pieces verified | notes |
|---|---|---|---|
| 2026-W36 | dialogue bank | 1 (pub-regular-v1, 48 lines) | pilot of the five stations; mechanical gates clean (canon, rung, repetition worst 0.18, license tagged); tone PENDING the D7 judge, whose calibration sample this bank is |
| 2026-W36 | signage/brand | 0 (brand-bible-v1, 8 entries) | VERIFY passed and INTEGRATE did not, so by this ledger's own rule it counts ZERO. The only thing that reads content/brands/brand-bible-v1.json is its own verifier: rule 6, built is not running, applied to content. Grepped rather than assumed. Queued as 009 |
| 2026-W36/W37 | prop/asset | 22 (pilot package one, A7_gully_grate) | THE FIRST PROP-LINE PILOT. It counted ZERO for three days by this ledger's own rule, station 4 INTEGRATE not having happened, and it crossed on 2026-09-09. Stations 1 SPEC and 2 AUTHOR are done (production/specs/asset-interface.md, and the GLB is on disk at 0.3999 x 0.015 x 0.3999 m as the spec box, exact to 0.0000 mm). Station 3 VERIFY passes in the container: the importer selftest reads 48 of 48, and it is wired into ledger/verify.py so it runs before every commit rather than by hand. Station 4 DID NOT HAPPEN, and the reason RECORDED HERE FIRST WAS WRONG: this row said "the engine has a glTF EXPORTER and no importer, so nothing loaded back". That was an instrument fault twice over and it is corrected by measurement, not by argument. Run 2 on f3f395c printed propGltfCanTranslate=3/3 with eleven Interchange plugins present, so the engine CAN translate glTF headlessly; the failure was the importer script treating a None return from its own load-back as the engine refusing. Run 3 on 7f12005 then imported 15 of 16: propImported=15/16 propSaved=15/16 propUassetsOnDisk=16 propUassetBytesOnDisk=1736681, the grate resolved at 0.0474 mm worst against its spec box, and sixteen real .uasset files are committed under ue-probe/Content/Ledger/Props/. IT COUNTS TWENTY-TWO, AND IT COUNTED ZERO FOUR HOURS EARLIER. Run 33 on 76e4238 placed the imported meshes in the walk build: propsAsMesh=22/23 where every earlier run read 0/23, propStandIns=1/23, propPlacedWithCollision=22/22 propPlacedCollisionUnread=0/22, and the one fallback is pavement_sign, whose source GLB holds three mesh nodes and whose resolver correctly refuses to choose among them. STATION 4 INTEGRATE HAS HAPPENED. The grate itself reads propBurialSubject=prop_drainage_grate_01_0/via=loaded-asset/collision=YES, and via=loaded-asset rather than via=box-stand-in is the word that says this is a placed reading and not spec arithmetic.
| 2026-W37 | prop/asset | 0 (package two, C15_fascia_cornice_console, 2 assets in 17 placements) | IT COUNTS ZERO AND THE REASON IS ONE SENTENCE: station 4 INTEGRATE has not been measured on the PC, because the engine run is the game lane's today and the art lane does not take the runner. Everything short of that is done and measured on 2026-09-10, listed with its command in production/art/fascia-01/03-VERIFY-fascia-package.md. Station 1 SPEC: 01-SPEC, with the geometry-versus-decal split decided by arithmetic (a 25 mm applied letter buys a sub-pixel gradient under an overcast sky; a 0.215 m cornice throws a hard line across 36 m). Station 2 AUTHOR: two GLBs at 300 and 296 verts, authored in house, regenerating byte for byte, boxWorstMm=0.0000000. Station 3 VERIFY: placementChecks=11/of=11-passing off the committed piece list with a selftest whose 8 rejecting fixtures all fire; worstMm=0.0000/over=18/tolMm=0.001 from import_prop_meshes --measure; 0 of 293 in vignette-spec-test; All 4315 checks in CoreTests; attribution ok. Station 4 PREPARED AND NOT CROSSED: the 17 rows are in vignette-scene.json and the 610-piece list, so the two GLBs that sat NAMED BY NOTHING for a day are now named by a bill-of-materials line, which is the rule 6 half that was open. THE KEY THAT WILL CROSS IT IS propsAsMesh=39/40 propStandIns=1/40 with propFallbackWhy naming ONLY pavement_sign, whose source GLB holds three mesh nodes; 39 rather than 40 is stated in advance so a shortfall cannot be explained afterwards, and 37/40 with the fascia assets in the fallback list means the mesh did not reach the street. QUEUE 228 IS ANSWERED BY MEASUREMENT AND THE GEOMETRY DID NOT MOVE: consoleRestingOnCornice=11/of=11 consolePenetrationWorstMm=0.000000 consoleOverlapVolWorstM3=0.00000000 consoleInsideCornice=NO. The 100.0pct@150.00mm reading is the cornice's own height standing above a bracket whose top IS its soffit, at zero penetration and zero overlap volume; the same measurement found the two awnings 370 mm and 810 mm genuinely inside a toplight and a door spandrel while the gate printed 0.00 mm for both, so the missing half hides a real fault as well as inventing a false one. NO PICTURE EXISTS OF ANY OF IT, which is the other open half: tools/art-recipes/fascia-cornice-elevation.py plans six frames off this piece list, passes 30 of 30 of its own checks, and has never rendered because Blender is not in this container. |

JAFAR'S ACCEPTING CASE IS MET AS OF RUN 36, 2026-09-09: ue-walk_05_grate_a.png has the drainage grate dead centre, diagonal slots and a frame, nothing across it, taken from the third standpoint after two were refused with rail_post1 named. The piece is a real imported mesh with collision at the road surface and it is now in a picture. WHAT IS NOT SETTLED is how it LOOKS: the grate and the band around it render near-white with almost no material read, which is queue 176 and the visual bar rather than the prop route. THE PARAGRAPH BELOW IS KEPT AS WRITTEN because a superseded reason is evidence of how the row got here.

WHAT WAS STILL NOT MET WHEN THIS ROW WAS LAST EDITED, and the distinction is the whole value of keeping this row honest. He asked for the grate as a real mesh WITH COLLISION IN A WALK CLIP. It is a real mesh with collision, measured. It is not in a clip, because propFullyBuried=1/23 and the one is the grate: it sits under the carriageway and the channel both, 20.00 mm of cover at the west footprint edge and 10.25 mm at the last sampled cell, so no camera can see it. THAT IS A STREET-SPEC FAULT AND NOT A PIPELINE FAULT, and the pipeline is what this ledger measures. Twenty-two pieces are verified; the pilot's own showpiece is verified and invisible.

THE REASON THIS ROW MOVED TWICE BEFORE IT MOVED HERE, kept because a deleted number cannot be audited. Run 3 printed propCollisionPrims=0/15 and it was read as fifteen meshes with no collision. That was not a measurement: EditorStaticMeshLibrary.get_simple_collision_count refuses by RETURNING -1 rather than raising, the importer believed any non-None return, and a refusal became a measured absence. Run 4, on a rebuilt reader, printed propCollisionPrims=15/15 with propCollisionVia=not-needed/already-had-1=15. THE MESHES HAD COLLISION ALL ALONG; the glTF import put a primitive on every one and nothing needed adding. The grate itself reads RESOLVED, saved=yes, simplePrims=1, bodySetup=present, 0.0474 mm worst against its spec box. So the ASSET half of Jafar's accepting case is finished and measured. THE ROW STILL COUNTS ZERO because station 4 INTEGRATE has not happened: the walk build has never placed one prop mesh (propsAsMesh=0/23, propStandIns=23/23), and the grate is specified 13.4 mm below the top of the continuous channel slab that spans it, so no frame can show it. A piece nothing places has not been manufactured. A mesh with no body setup photographs clean and a walking character falls through it. Station 5 RECORD is this row. |

## Cost per verified piece, and the calibration it rests on

ASKED FOR BY JAFAR 2026-09-08 for pilot package one. The honest answer this
week is that it is UNDEFINED, not zero: the denominator is zero verified
pieces, and a cost divided by no pieces is not a number. Recording it as zero
would be the false claim with a number on it that rule 3b exists to stop.

THE CALIBRATION, stated so the first real figure can be read against
something. The only cost unit this project can OBSERVE is the session. Nothing
inside the container can read Jafar's usage page, which is a standing
instruction of his and not a limitation to be worked around, so a token figure
here would be invented. What can be measured is:

- SESSIONS, counted from `.claude/agent-log.tsv` spawn rows, which is the same
  denominator `directorSpawns` and `gameShareDay` already use in the verify
  footer, so the number is comparable to figures this project already prints.
- JAFAR'S OWN READINGS in `production/budget.md`, bracketing the work. Those
  are percentages of an allowance, not of this project: the 2026-09-08 rows
  say in his words that the window was not clean and that the change must not
  be attributed wholly to this work.

SO THE FIGURE, WHEN THERE IS ONE, IS SESSIONS PER VERIFIED PIECE, and any
percentage beside it is an UPPER BOUND on studio cost rather than a
measurement of it. That distinction is the calibration. It is the same one the
budget file has carried since 2026-09-06 and it is the reason no per-session
point rate has ever been computed from a dirty window.

WHAT PILOT ONE HAS COST SO FAR, with its denominator, read off the log and the
verdict files on 2026-09-08 rather than recalled:

- RUNNER TIME, the only clock this project measures directly. THREE runs of the
  mesh workflow have published a verdict. Run 2 on f3f395c:
  meshEditorBuildMinutes=1.42 propImportMinutes=0.18. Run 3 on 7f12005: 1.33
  and 0.27. Run 4 on a870a10: 1.37 and 0.35. So 1.60, 1.60 and 1.72 minutes,
  and that figure is the SUM OF
  THE TWO STEPS THE VERDICT TIMES, not the job: checkout, editor start and the
  commit-and-push step are outside it and unmeasured. ONE EARLIER RUN published
  NOTHING, so it contributes no minutes and is not averaged in;
  the cost of a run that measures nothing is real and is recorded as a count,
  one, rather than folded into a mean.
- STUDIO SESSIONS. 17 engine-specialist spawns on 2026-09-08, and WHAT THAT
  DENOMINATOR COUNTED MATTERS: it is every engine spawn that day across the
  crime probe, the walk clip and the mesh import together. The log records an
  agent type and a timestamp and nothing else, so the prop line's share of the
  17 cannot be read out of it. Attributing all 17 to the props would be a
  numerator borrowed from three lines, and that is exactly the shape rule 3b
  calls a false claim with a number on it. Plus 2 director reviews, both of
  which were about the prop line and are attributable.

OVER 22 VERIFIED PIECES, AND THIS IS THE FIRST TIME THIS FILE HAS HAD A
DENOMINATOR AT ALL.

THE ROUND TRIP, measured push to landed evidence rather than estimated, which is
the only wall clock this project owns:

- mesh run 4, dispatched 2026-09-08T23:23:49Z, evidence committed 23:25:56Z:
  2 min 07 s.
- run 33, dispatched 2026-09-09T01:01:57Z, evidence committed 01:07:39Z:
  5 min 42 s. That one is a cold build, a cook, a packaged launch, two crimes,
  a gossip round, 30 frames and a clip.

So the machine half of a piece is minutes, and it was always going to be. THE
COST IS THE STUDIO HALF AND IT IS SESSIONS.

WHAT A PIECE COST, AND THE SHAPE OF THE ANSWER MATTERS MORE THAN THE NUMBER.
Twenty-two pieces crossed station 4 in one run, on a pipeline that took the whole
of 8 September to build. Dividing the build cost by 22 would be arithmetic and
not a measurement: THE FIRST PIECE COST THE PIPELINE AND THE TWENTY-SECOND COST
NOTHING. The two figures that can be stated honestly are:

- SETUP, once: 22 engine-specialist and 7 instrument-builder spawns on 8 and 9
  September, plus 11 director spawns. WHAT THAT DENOMINATOR COUNTS: every engine
  and instrument spawn on those two days across the crime probe, the walk clip,
  the mesh import, the caption tool and the burial instrument together. The log
  holds an agent type and a timestamp and nothing that would let the prop line's
  share be read out of it, so this is an UPPER BOUND on the prop line's setup and
  not a measurement of it.
- MARGINAL, per piece after the pipeline exists: ZERO SESSIONS AND ABOUT
  0.35 MINUTES OF RUNNER TIME, that being propImportMinutes over the sixteen
  assets in one run. A twenty-third piece needs a GLB and nothing else, which is
  the number the twelve-package batch should be planned against.

AND THE HONEST CAVEAT ON THE MARGINAL FIGURE: it is measured over sixteen assets
that were already authored. It prices the IMPORT of a piece and not the MAKING of
one. What it takes to author a GLB worth importing is unmeasured, and the
twelve-package batch is what will measure it.

RECORDING A ZERO IS THE POINT OF THE LEDGER. The brand bible is real work,
cleanly verified, and it would be easy to enter as one piece: the entry
above is what stops a shelf of finished-looking content reading as
throughput. A piece nothing consumes has not been manufactured, it has
been written down.

The station-5 step was also SKIPPED for this batch and added afterwards,
which is worth admitting here rather than only in a lesson: the line has
five stations and the one that keeps everyone honest is the one easiest
to forget, because by then the work feels done.

## The BATCH unit, and the attempts nobody kept

ADDED 2026-09-21 for queue 403, from Jafar's order: "the throughput ledger
takes a batch as its unit and counts rejected attempts, since the industry
research found nobody measures rework and ours would be the instrument that
does." Everything above this heading is the PIECE unit and is unchanged by it.
The piece unit answers "what landed"; it cannot answer "what did it cost",
because a cost divided by survivors alone prices the wrong thing.

**A batch counts when every deliverable on the list it fixed at station 1
(SPEC) has passed station 3 (VERIFY) and landed at station 4 (INTEGRATE). A
batch one deliverable short counts zero, the same way a piece does.**

**An attempt counts as REJECTED when a station's gate or a named judge refuses
it and the work is not carried into station 4. A rejected attempt counts zero
pieces and one rejection.** Silence is not a refusal: a batch that nothing has
refused and nothing has landed is OPEN, and an OPEN batch is not a rejection
and not a zero.

WHY THE BATCH AND NOT THE PIECE, IN ONE SENTENCE THAT THIS FILE ALREADY
WROTE: "THE FIRST PIECE COST THE PIPELINE AND THE TWENTY-SECOND COST NOTHING."
A piece is what a batch produces, so it is a fine unit for counting output and
a hopeless one for pricing input. The batch is the smallest thing that has a
start, an end and a bill.

### The three states of a rejection count, which must never collapse into one

    attemptsRejected=0/of=4-attempts          four attempts, none refused
    attemptsRejected=0/of=0-attempts-so-far   nothing attempted yet
    attemptsRejected=nothing-measured         NOBODY COUNTED, and it ran

The third is what every batch before today reads, because there was no field
to write it in while the work happened. Entering a retrospective zero there
would be an invented measurement with a number on it, which is the exact fault
rule 3b exists to stop. `tools/throughput-check.py` refuses a bare zero
anywhere in a batch block for the same reason.

### The block shape, and why it is not a table

Each batch is a block of labelled key=value lines, values carrying no spaces so
that any reader splitting on whitespace gets the whole value. It is NOT a pipe
table, and that is measured rather than stylistic:
`tools/dashboard/build-dashboard.py:425` collects EVERY pipe row of four or
more cells and `read_throughput` at :1216 sums cell 3 of every row whose first
cell matches the current ISO week, so a batch written as a table row would be
added to the dashboard's verified-piece count in silence. The checker refuses a
pipe row inside this section.

    ### BATCH <id>
    batch:    batchId line status(OPEN|VERIFIED|REJECTED) opened closed
    unit:     deliverables(N/fixed-at-open/list=<path>) deliverableUnit
    attempts: attemptsMade(N-cumulative) attemptsRejected(N/of=M-attempts)
              rejectedAtStation
    before:   meterTakenAt meterTotalPct meterFablePct meterSource
              sessionsTakenAt sessionsCumulative sha
    after:    the same keys plus cleanWindow(yes|no|not-stated)
    machine:  runnerMinutes(N.NN/sum-of-timed-steps/over=<coverage>)
              runnerSteps
    wear:     wearCoverageN wearCoverageMin(<fraction>/<surface>)

WHAT EACH NUMBER IS A STATISTIC OF, named here once so no row has to guess.
`attemptsMade` and `attemptsRejected` are CUMULATIVE over the batch's life.
`sessionsCumulative` is a LAST-WINS reading of the whole `.claude/agent-log.tsv`
at the instant beside it, and the batch's own session cost is the DIFFERENCE
between the before and after readings, never either one alone. `meterTotalPct`
and `meterFablePct` are Jafar's own LAST-WINS readings of his usage page, which
nothing in this container can read; the ledger quotes the newest row of
`production/budget.md` and the instant he took it, and that instant is NOT the
instant the batch opened. `wearCoverageMin` is the MINIMUM over the batch's
surfaces with the surface named, per D53 point 2, because a median cannot see
the one clean wall. `runnerMinutes` is a SUM over the steps a verdict times
and never the job: checkout, editor start and the commit-and-push step are
outside it and unmeasured, which is the same caveat the cost section above
already carries, and the value states over how many runs the sum was taken
because a sum with an unstated coverage is a number waiting to be quoted as a
total.

TWO INSTANTS, NEVER ONE. The meter reading and the session count are taken at
different moments by different hands, so they carry `meterTakenAt` and
`sessionsTakenAt` separately. One `takenAt` standing for both would print two
moments as one, which is the fault this file records against itself in the
prop row above.

PRICED IS QUEUE 369'S FOUR CONDITIONS AND NOT THIS FILE'S OPINION: end to end,
the rejected work counted in, BOTH meters read before AND after, nothing else
running in the window. `tools/throughput-check.py --series` prints
`pricedConditionsMet=k/of=4` per batch and names the ones unmet. A batch
missing any of them is UNPRICED, which is a true state of the world and not a
failure; the failure would be letting it read as priced.

NO BOUND IS SET HERE. Not on rejections per batch, not on sessions per batch,
not on minutes. The series has the points printed below and no more, and a
bound needs a printed series first (rule 2). The printer ships now, the number
comes when there are runs to read it from.

### What the rows above read as under this unit, which is the test of it

Every existing row of this ledger is keyed to a named package, so each one IS a
batch and the unit describes them without rewriting a single figure. Four
batches, and NOT ONE OF THEM IS PRICED: three of the four conditions fail on
all four, which is the answer to "what does a unit of content cost" as of
tonight. The number does not exist yet, and now the shape of its absence is
visible instead of inferred.

### BATCH b001-dialogue-pub-regular-v1

batch: batchId=b001-dialogue-pub-regular-v1 line=dialogue-bank status=VERIFIED
  opened=2026-W36 closed=2026-W36
unit: deliverables=1/fixed-after-the-fact/list=production/throughput.md#row-2026-W36-dialogue
  deliverableUnit=dialogue-bank-of-48-lines
attempts: attemptsMade=nothing-measured attemptsRejected=nothing-measured
  rejectedAtStation=nothing-measured
before: meterTakenAt=nothing-measured meterTotalPct=nothing-measured
  meterFablePct=nothing-measured meterSource=nothing-measured
  sessionsTakenAt=nothing-measured sessionsCumulative=nothing-measured
  sha=nothing-measured
after: meterTakenAt=nothing-measured meterTotalPct=nothing-measured
  meterFablePct=nothing-measured meterSource=nothing-measured
  sessionsTakenAt=nothing-measured sessionsCumulative=nothing-measured
  sha=nothing-measured cleanWindow=not-stated
machine: runnerMinutes=nothing-measured runnerSteps=nothing-measured
wear: wearCoverageN=nothing-measured wearCoverageMin=nothing-measured

THE ONE THING STILL OPEN ON IT IS A JUDGE, and the batch unit now has somewhere
to put the answer: the row above says tone is PENDING the D7 judge. If that
judge refuses the bank, this becomes the ledger's first recorded REJECTION at
station 3 with a named judge, and the field to record it in exists as of
tonight. Under the old file it would have left no mark at all.

### BATCH b002-brand-bible-v1

batch: batchId=b002-brand-bible-v1 line=signage-brand status=OPEN
  opened=2026-W36 closed=not-yet
unit: deliverables=8/fixed-at-open/list=content/brands/brand-bible-v1.json
  deliverableUnit=brand-entry
attempts: attemptsMade=nothing-measured attemptsRejected=nothing-measured
  rejectedAtStation=nothing-measured
before: meterTakenAt=nothing-measured meterTotalPct=nothing-measured
  meterFablePct=nothing-measured meterSource=nothing-measured
  sessionsTakenAt=nothing-measured sessionsCumulative=nothing-measured
  sha=nothing-measured
after: meterTakenAt=nothing-measured meterTotalPct=nothing-measured
  meterFablePct=nothing-measured meterSource=nothing-measured
  sessionsTakenAt=nothing-measured sessionsCumulative=nothing-measured
  sha=nothing-measured cleanWindow=not-stated
machine: runnerMinutes=nothing-measured runnerSteps=nothing-measured
wear: wearCoverageN=nothing-measured wearCoverageMin=nothing-measured

OPEN AND NOT REJECTED, AND THE DISTINCTION IS THE POINT OF THE STATUS. VERIFY
passed and INTEGRATE did not, so it counts zero pieces by the piece rule and
zero landed deliverables by the batch rule. Nothing refused it: it has been
waiting since 2026-W36 as queue 009. A ledger with only two states would have
had to call this a rejection, and it is not one.

### BATCH b003-prop-pilot-one

batch: batchId=b003-prop-pilot-one line=prop-asset status=VERIFIED
  opened=2026-W36 closed=2026-09-09
unit: deliverables=16/fixed-after-the-fact/list=production/throughput.md#row-2026-W36-W37
  deliverableUnit=glb-mesh-asset
attempts: attemptsMade=nothing-measured attemptsRejected=nothing-measured
  rejectedAtStation=nothing-measured
before: meterTakenAt=nothing-measured meterTotalPct=nothing-measured
  meterFablePct=nothing-measured meterSource=nothing-measured
  sessionsTakenAt=nothing-measured sessionsCumulative=nothing-measured
  sha=nothing-measured
after: meterTakenAt=nothing-measured meterTotalPct=nothing-measured
  meterFablePct=nothing-measured meterSource=nothing-measured
  sessionsTakenAt=nothing-measured sessionsCumulative=nothing-measured
  sha=nothing-measured cleanWindow=not-stated
machine: runnerMinutes=nothing-measured runnerSteps=nothing-measured
wear: wearCoverageN=nothing-measured wearCoverageMin=nothing-measured

ITS DELIVERABLE LIST WAS RECONSTRUCTED AFTERWARDS AND THAT IS WHY IT IS MARKED
SO. The pilot grew while it ran, so there is no list fixed at station 1 to
divide anything by: 16 is `propUassetsOnDisk=16` from run 3, quoted in the row
above. Counted tonight rather than recalled,
`ls ue-probe/Content/Ledger/Props/*.uasset` returns 18, because two more landed
later under other work. A denominator fixed after the fact drifts; that is the
whole argument for fixing it at station 1, and this is the evidence for it.

ITS RUNNER MINUTES READ nothing-measured AND THE FILE ABOVE HAS THREE
READINGS, which is not a contradiction. The cost section carries 1.60, 1.60 and
1.72 minutes for three mesh runs, one earlier run that published nothing, and a
5 min 42 s wall clock for run 33. Those are PER RUN and on two different
clocks, over an unknown fraction of the batch's runs. Adding them would produce
a batch total whose denominator nobody can state, so this field says the words
rather than a sum, and the terrace front is the first batch that can fill it
honestly because its runs will be counted from the start.

WHAT THE 22 IS, AND THIS UNIT DOES NOT SETTLE IT. The row above counts 22 and
queue 355 is open on whether that is 22 pieces or 22 placements from 15 meshes.
The batch unit counts BATCHES, one here, so it neither inherits nor repairs
that ambiguity, and nothing in this section may be read as having closed
queue 355.

### BATCH b004-fascia-package-two

batch: batchId=b004-fascia-package-two line=prop-asset status=OPEN
  opened=2026-09-09 closed=not-yet
unit: deliverables=2/fixed-at-open/list=production/art/fascia-01/01-SPEC-fascia-package.md
  deliverableUnit=glb-mesh-asset
attempts: attemptsMade=nothing-measured attemptsRejected=nothing-measured
  rejectedAtStation=nothing-measured
before: meterTakenAt=nothing-measured meterTotalPct=nothing-measured
  meterFablePct=nothing-measured meterSource=nothing-measured
  sessionsTakenAt=nothing-measured sessionsCumulative=nothing-measured
  sha=nothing-measured
after: meterTakenAt=nothing-measured meterTotalPct=nothing-measured
  meterFablePct=nothing-measured meterSource=nothing-measured
  sessionsTakenAt=nothing-measured sessionsCumulative=nothing-measured
  sha=nothing-measured cleanWindow=not-stated
machine: runnerMinutes=nothing-measured runnerSteps=nothing-measured
wear: wearCoverageN=nothing-measured wearCoverageMin=nothing-measured

THE ONE BATCH ABOVE WHOSE LIST WAS FIXED AT STATION 1, read rather than
assumed: `production/art/fascia-01/01-SPEC-fascia-package.md` is dated
2026-09-09 and names its two assets, `fascia_cornice_01` and
`fascia_console_01`, before either was authored. It is OPEN because station 4
has not been measured on the PC, which the row above states in one sentence.

### BATCH b005-terrace-front-01

batch: batchId=b005-terrace-front-01 line=art-terrace-fronts status=OPEN
  opened=2026-09-21T18:42:08Z closed=not-yet
unit: deliverables=not-yet-fixed/at=station-1-SPEC
  deliverableUnit=glb-mesh-asset
attempts: attemptsMade=0-cumulative attemptsRejected=0/of=0-attempts-so-far
  rejectedAtStation=none/of=0-attempts-so-far
before: meterTakenAt=2026-09-21T16:2xZ meterTotalPct=13 meterFablePct=17
  meterSource=production/budget.md#row-2026-09-21b
  sessionsTakenAt=2026-09-21T18:42:08Z
  sessionsCumulative=745/src=.claude/agent-log.tsv sha=0f1b8fa4
after: meterTakenAt=nothing-measured meterTotalPct=nothing-measured
  meterFablePct=nothing-measured meterSource=nothing-measured
  sessionsTakenAt=nothing-measured sessionsCumulative=nothing-measured
  sha=nothing-measured cleanWindow=not-stated
machine: runnerMinutes=nothing-measured runnerSteps=nothing-measured
wear: wearCoverageN=nothing-measured wearCoverageMin=nothing-measured

THIS IS THE BEFORE READING, TAKEN TONIGHT SO THERE IS A BASELINE TO SUBTRACT
FROM. It is queue 403's last deliverable and the authoring session's first
input. Its three numbers were read at the two instants beside them and not
recalled: 745 spawn rows in `.claude/agent-log.tsv` and sha 0f1b8fa4 at
2026-09-21T18:42:08Z, and 13 and 17 percent from the newest row of
`production/budget.md`, which Jafar took at about 16:2xZ. THE METER IS TWO AND A
HALF HOURS OLDER THAN THE SESSION COUNT and the two keys say so rather than
averaging into a false instant. Nothing in this container can read the usage
page, which is his standing instruction, so a fresher meter is a thing to ask
for and never to compute.

WHAT THE NEXT SESSION OWES THIS BLOCK, in order. Fix the deliverable list at
station 1 SPEC and replace `not-yet-fixed`, because a denominator chosen after
the work is the fault b003 above is the evidence for. Increment `attemptsMade`
per attempt and `attemptsRejected` per refusal WITH the station that refused
and the judge who called it, whichever way the batch resolves. Print
`wearCoverage` with the batch per D53 point 5, the facade being the first point
in that series and not a surface judged against a floor that does not exist.
Ask Jafar for both meters at the close, and ask him whether the window was
clean, because `cleanWindow` is the one condition of the four that only he can
answer.

THE SUBJECT CHANGED THIS EVENING AND THE BATCH DID NOT. Queue 389 was one
facade authored from scratch and is SUPERSEDED by his kit-first ruling and then
by `game-design/decision-2026-09-21-ruling-the-terrace-fronts-are-authored-and-everything-else-comes-from-what-we-hold.md`:
the terrace fronts are authored in Blender from the atlas plans, under the
grime rule, dressed in free scanned materials. He kept all three things this
block exists for, in his own words, "both meters read before and after, the
BATCH as the throughput ledger's unit, and REJECTED ATTEMPTS COUNTED". So this
block is opened for the terrace front rather than for the superseded item.

### BATCH b006-lighting-column-01

TWO ATTEMPTS, BOTH REJECTED AT VERIFY, and they are recorded rather than
absorbed because that is what this unit exists for. A ledger counting only
successes would price this asset at one clean attempt and understate the
method's real cost by two thirds.

ATTEMPT 1, rejected by the lane's own gate, run 35649856734. The recipe
refused its own lane's arguments: status=BAD-ARGS
reason=unknown-flag/--commission, blenderExit=2, nothing rendered. Its 48 of
48 selftest could not see it, because the test asserted the flags the AUTHOR
chose rather than the flags the LANE SENDS. Fixed by deriving the contract
from the workflow and the wrapper at test time; selftest 48 to 66.

ATTEMPT 2, rejected by a named judge, the director, against the Hook sheet.
Committed at fbba39e1 on art/atlas-01. THE RENDER SUCCEEDED: status=RAN
objectsBuilt=10/10-planned previewsWrote=4/4 engineUsed=BLENDER_EEVEE_NEXT
crossCheckAgree=10/10 manifoldParts=10/10. THE SILHOUETTE IS WRONG, and the
director's account of WHY was wrong in the opposite direction, corrected here
under D43 with the false text named. What was written: "the arc is tighter and
starts higher than the reference, reading as a shepherd's crook rather than a
swan neck", with the reference described as "a long lazy sweep beginning about
two thirds up". MEASURED AFTERWARDS ON THE SHEET'S OWN PIXELS, first by the
builder and then independently by the director: the pole is 3px wide and dead
straight from y760 downward, and the entire curve, head and ridge bump resolve
between y752 and y758. SEVEN ROWS. The reference is COMPACT AND
TOP-CONCENTRATED, not a long sweep, so the description was read off a blurred
crop instead of measured, which is rule 4 exactly: the picture was strong
evidence something was wrong and weak evidence of what.
THE SYMPTOM WAS REAL AND THE CAUSE WAS THE DROPPER, NOT THE ARC. At 26.3 px
per metre, derived from the 3px pole against the spec's 0.114 m shaft, the
sheet's transition is about 0.27 m vertically, which implies an arc radius near
0.30 m and REFUTES the authored 0.75 m. So the render's arc was TOO GRADUAL,
not too tight; the crook read came from a 0.707 m external dropper hanging the
head below the curve like a rod. The director's prescription, a gentler arc,
would have made it WORSE: the builder proved in closed form that with the mount
pinned below the shaft top, a LARGER radius always LENGTHENS the dropper.
The other four hold: the head is too bulky; there is a stray tab; the base
collar is too prominent; and no wear reads at all despite a coverage figure of
0.450 on the base.

ATTEMPT 3, rejected by the same judge, and the first refusal that is a NUMBER
rather than a description. Committed at 6f738008 on art/atlas-01, status=RAN
objectsBuilt=10/10-planned previewsWrote=4/4 crossCheckAgree=10/10
manifoldParts=10/10. IT FIXED FOUR OF THE FIVE FAULTS and none of them are in
dispute: the base taper removed the sleeve step, the stray tab is gone, the
head is slimmer, and the external dropper went 0.707 m to 0.224 m.

WHAT STILL REFUSES IT, traced on both with one threshold method. The SHEET's
head assembly is 25px wide by 11px tall, aspect 2.27:1, which at the 26.3 px
per metre scale is 0.95 m by 0.42 m. ATTEMPT 3's is 129px by 139px, aspect
0.93:1, NEARLY SQUARE. The sheet's assembly is flat and wide and the authored
one is not.

AND THE SHAPE THREE ATTEMPTS HAVE MISREAD IS NOW LEGIBLE. Blown up, the
reference is NOT A SWAN NECK: it is a straight pole, a TIGHT SHORT CORNER, a
SHORT HORIZONTAL ARM, and a FLAT WIDE LANTERN HANGING LEVEL beneath the arm's
end. An L with a rounded corner. Every attempt so far built a continuous arc
that rises, turns through a large angle and descends, which spends the
assembly's height on vertical travel and leaves the lantern TILTED. Attempt 3
reports sweep_deg=131.81 jointAngle_deg=48.19; a horizontal arm arrives at
zero.

THE TARGET CARRIES ITS CAVEAT RATHER THAN BURYING IT: the sheet's lamp is 25px
across and its pole 2 to 3px wide, near the image's own resolution floor, which
is why lcSheetRef already emits confidence=low-to-moderate. 2.27:1 is a target
with a stated tolerance, not a precision figure.

THE NUMBER THAT PASSED IS THE FINDING. authoredCurvature_perM=1.3333 beat a
naive quarter circle at 2.0000 and was recorded as shallower, while the picture
shows it TIGHTER than the sheet. THE QUARTER CIRCLE WAS NEVER THE REFERENCE, so
passing it proved nothing about the only comparison that matters. Measuring
shallower and reading right are different claims, which this asset's own
authoring builder warned of in its method verdict before any frame existed.

ATTEMPT 4 IS OPEN, NOT REJECTED, AND THE DISTINCTION IS THE WHOLE ENTRY. Run
35669115224 on studio sha 595484b6, committed at 6f77ff59 on art/atlas-01. The
render RAN: status=RAN objectsBuilt=10/10-planned previewsWrote=4/4
crossCheckAgree=10/10 manifoldParts=10/10 elapsedSeconds=3.3. No gate refused
it and no named judge has refused it, so it is not counted in
attemptsRejected; silence is not a refusal and OPEN is the third state.

THE RUN WENT RED AND THE RENDER WAS FINE, which is a lane fault and is fixed in
the same commit as this entry. The render step passed only while the COUNT of
this recipe's PNGs ROSE (`$mineAfter -le $mineBefore` exits 1), and a recipe
overwrites its own four frames, so the count can rise exactly once, on a
recipe's first ever run. Proven from the art branch and not from the step:
0 lighting-column PNGs at 11d6cf51, the parent of the first such run, WHICH
PASSED; 4 at each of fbba39e1, 6f738008 and 6f77ff59, the three later runs,
EVERY ONE OF WHICH WENT RED while publishing a complete verdict. The gate now
counts frames whose write time is at or after the instant Blender started, and
that test was run on both halves before it shipped: 5 cases, accepting first,
the re-render case passing where the old condition fails.

WHAT THE FRAMES SHOW, MEASURED BEFORE IT WAS DESCRIBED. Attempt 4 is materially
closer: its silhouette's top row is y=121 against attempt 3's y=100, so the
arch is 21px lower in the same camera, and the corner plus level arm replaced
the round sweep. It is still not the sheet, and the mismatch is structural
rather than a tuning error. Traced at 4 sigma below a measured sky baseline,
THE SHEET'S LAMP ENCLOSES NO SKY: 0 of 39 dark rows split into more than one
segment, over 48 rows examined, window x230..276 which nothing touches. Both
renders enclose sky, attempt 4 in 105 of 139 dark rows and attempt 3 in 126 of
160. The sheet is a KINK with the lantern hanging off it; both renders are
ARCHES with a bare arm and a dropper under them.

AND THE TARGET ASPECT MOVES WITH THE THRESHOLD, WHICH IS WHY THIS ATTEMPT IS
NOT BEING TUNED AGAIN BLIND. Same sheet, same crop, three traces: 25x11px
(2.27:1) from the authoring builder, 23x7px (3.3:1) recorded on the recipe's own
lcSheetRef line, and 24x8px (3.0:1) from the director's 4 sigma trace tonight.
The head is 8 rows tall at 4 sigma and 11 at a looser cut, a 37 percent swing in
the denominator from where the cut falls. Attempt 4 achieves 2.279 against a
target that is anywhere between 2.27 and 3.3 depending on the ruler. NORMALISED
BY THE ONE LENGTH BOTH IMAGES PIN, the 0.114 m shaft, the sheet's head and neck
are 6.0 pole-diameters wide and 2.0 tall; attempt 4 is 6.80 and 2.98. The width
is 13 percent over and the height 49 percent over, and neither figure is worth
tuning against until the reference can resolve it.

batch: batchId=b006-lighting-column-01 line=art-lighting-column status=OPEN
  opened=2026-09-21T20:02:52Z closed=not-yet
unit: deliverables=1/fixed-at-open/list=production/queue/419-the-lighting-column-is-authored-and-unrun-blender-is-the-next-station.md
  deliverableUnit=lighting-column-blender-asset
attempts: attemptsMade=4-cumulative attemptsRejected=3/of=4-attempts
  rejectedAtStation=3-VERIFY/of=4-attempts
before: meterTakenAt=2026-09-21T19:2xZ meterTotalPct=17 meterFablePct=19
  meterSource=production/budget.md#row-2026-09-21c
  sessionsTakenAt=2026-09-21T19:41:50Z
  sessionsCumulative=750/src=.claude/agent-log.tsv sha=87bcd46d
after: meterTakenAt=nothing-measured meterTotalPct=nothing-measured
  meterFablePct=nothing-measured meterSource=nothing-measured
  sessionsTakenAt=nothing-measured sessionsCumulative=nothing-measured
  sha=nothing-measured cleanWindow=not-stated
machine: runnerMinutes=nothing-measured runnerSteps=nothing-measured
wear: wearCoverageN=4/of=4-authored-surfaces wearCoverageMin=0.000000/lantern

QUEUE 403'S SMALLER, FASTER BATCH AHEAD OF THE FACADE, exactly as his ruling
named it: the pilot whose purpose is to price the authoring method, priced
before the terrace fronts spend a week on the same question. THE BEFORE
READING IS TAKEN FROM TWO DIFFERENT INSTANTS, THE SAME SHAPE b005 ABOVE USES
AND FOR THE SAME REASON: the meter (17 total, 19 Fable) is row 2026-09-21c of
production/budget.md, read at about 19:2xZ alongside his ruling on the lamp
column card, because that is the freshest reading this container can quote
and nothing here can read a fresher one. The session count (750 spawn rows
in .claude/agent-log.tsv, one header line making 751 total, counted rather
than assumed) and sha (87bcd46d) were read at 19:41:50Z, after the spec and
research had been read but before the recipe file existed on disk. THE TWO
ARE ABOUT TWENTY MINUTES APART AND THE KEYS SAY SO RATHER THAN AVERAGING INTO
A FALSE INSTANT.

ONE ATTEMPT, ZERO REJECTED, AND THAT IS A MEASURED CLAIM AND NOT A CLEAN
STORY TOLD AFTERWARDS. The first drafted neck geometry (a cubic Bezier
between the same two spec-pinned endpoints) printed
`shallowerThanNaive=no` the first time `--plan` ran: its peak curvature
measured HIGHER than the naive quarter circle despite reading as gentler,
because a Bezier's curvature is not constant and spikes where two unaligned
tangents are reconciled. That is not counted as a REJECTED attempt under this
ledger's own definition, because nothing external (a station gate, a named
judge) refused it: it was caught by this same file's own printed numbers
before anything was shipped, and rebuilt as a true circular arc (constant
curvature, so the comparison is closed-form) inside the same attempt. Filed
in full at production/queue/419-the-lighting-column-is-authored-and-unrun-blender-is-the-next-station.md
because it is the argument for the method as much as the asset is.

WHAT THIS ROW CANNOT PRICE YET, named rather than guessed. `machine` reads
nothing-measured because there is no runner: Blender is not installed in this
container, so no minute of render time has been spent on this pilot at all,
only the pure-Python arithmetic and the selftest (48 of 48, against the live
spec files as the accepting fixture). `after` reads nothing-measured across
the board because station 3 VERIFY needs a real Blender run this session
cannot supply; the batch stays OPEN, not VERIFIED, and by this ledger's own
rule an OPEN batch counts zero pieces until it crosses station 4, the same as
b002 and b004 above.

THE WEAR READING IS REAL, NOT A PLACEHOLDER, AND ITS DENOMINATOR IS FOUR
SURFACES: base, shaft, neck and lantern, each carrying a printed
`wearCoverage` fraction (`tools/art-recipes/lighting-column.py -- --plan`).
Three carry nonzero wear (rain running down the shaft, road spray at the
base, staining below the lantern), matching the three zones D53's point 5
and this task's brief both name and no more. The lantern housing carries none
in this pilot, by an authored choice this run can separate from a clean
surface (D53 point 2's distinction), which is why `wearCoverageMin` names it
at 0.000000 rather than printing `nothing-measured`.

### The instrument, and what it refuses

`tools/throughput-check.py` reads this section and refuses: a bare zero with no
denominator, a value with a space in it, a missing reading line, a rejection
count larger than its attempts, a resolved batch with no close instant or no
fixed deliverable list, a wear pair half measured, a wear minimum that names no
surface, a pipe-table row in this section, and any of the three definition
sentences above being edited away. It prints `--series` with one line per batch
and a done line carrying every zero's denominator. Its selftest runs the live
ledger as the accepting case FIRST and every rejecting fixture is synthetic
(`b9xx`, which exists in no ledger), so doing the work this file asks for can
never break the tool. That is queue 416's fault class, named so it is not
repeated here.
