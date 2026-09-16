<!--RULING spawn=2026-09-16T17:21:05Z paths=ue-probe/Source/LedgerProbe/Public/VignetteSpec.h,ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp,ue-probe/tests/vignette-spec-test.cpp,production/queue/361-one-sky-luminance-serves-day-and-night-so-night-renders-like-noon.md,game-design/decision-2026-09-16-ruling-the-sky-luminance-is-visual-and-no-ruling-was-needed.md-->
STATUS: LOG, 2026-09-16. NOT CURRENT once run 51's verdict lands: from then
the verdict's materials line and shot lines are the reading copies and this
file is the prediction they were read against.

Director ruling, 2026-09-16, on the queue 361 batch: the sky dome's
luminance driven per condition.

Spawn row, quoted verbatim from `.claude/agent-log.tsv` line 702, the last
studio-director row at the time of writing:
2026-09-16T17:21:05Z	studio-director	fable	default	ac8c0b21732cd6dbc

HEAD reviewed: 13acb9a4, working tree. This spawn had no shell, so NOTHING
BELOW WAS RUN: every line cited was read this session and every number quoted
was printed by the file it is cited from. The diff's file list was established
two ways that agree, a grep for the batch's own tokens (`kSkyLuminanceGain`,
`skyLumDrive`) over `ue-probe/` and the modification order of every source
file under `ue-probe/`, both giving the same three files. The resident confirms
that against `git diff --stat -- ue-probe/` before the commit; a fourth file,
if one exists, is added to the stamp's paths, which `ledger/verify.py`'s
RULING_RE (:4011) accepts as an extra token and ignores.

## 0. The ruling in one line

NO RULING WAS NEEDED. This batch is visual under D41 and lands on the
resident's read; the gate fired because `director_cadence` reads paths and not
D41's boundary, which is queue 363, filed today and not started. The rest of
this record is the evidence for that line, one correction to the item's own
acceptance text, and the two predictions run 51 must be read against.

## 1. Question 1: visual, by the boundary and by what was looked for

Jafar's boundary (`ledger-v2/respec/decision-register/rulings-log.md`:333-335):
a wrong answer undone by another render is visual; one whose undoing means a
migration, a golden file, a canon edit or a schema change is structural. The
run-50 record (`decision-2026-09-16-ruling-the-photograph-is-the-sky-and-it-
lights-the-street.md`:57-62) had already drawn the line for this parameter: "a
different kSkyLuminance value" is visual; the material's flags, the cook list,
the staging step and the verdict words stay structural.

What this batch is, read in the files:
(a) One constant renamed and re-meant: `kSkyLuminanceGain = 1.0f`
    (VignetteShot.cpp:402), a gain the condition's `sky_intensity` is
    multiplied by, floored at zero (VignetteSpec.h:3808-3812).
(b) One drive on the two existing precedents: `ReDriveSkyLuminance`
    (VignetteShot.cpp:2077-2115); exact-compare guard in the tested header
    (VignetteSpec.h:3843-3846); readback in the same statements as the set
    (:2110-2114) compared through `CellAgrees` (VignetteSpec.h:3878); tallies
    on the materials line with every zero beside its denominator and a
    nothing-measured form (VignetteSpec.h:3862-3898).
(c) A test, accepting case first, on the live file's two values, then the
    floor, then both arms of the guard (vignette-spec-test.cpp:6597-6628).

What was looked for and NOT found, each with its denominator:
- Schema: no new field. `sky_intensity` was already required in both readers
  (VignetteSpec.h:505, `NeedNum`), and `production/specs/vignette-scene.json`
  is outside the diff; its 33 condition rows already carry the field.
- Two writers on one parameter: `kSkyLuminanceParam` appears on 3 lines of
  VignetteShot.cpp (:376 definition, :2096 the one set, :2111 the readback).
  The build-time write the item names at its old :4582 is gone; the bind
  string now says `lumPerCondition=skyLumDrive-on-the-materials-line` (:4595).
  The header's "ONLY writer" claim (:392) holds.
- Built but not running (rule 6): `ReDriveSkyLuminance` has one call site,
  :2199, as `ReDriveLampEmissive` has one, :2233. Whether the enclosing
  function is the per-tick apply was not read this session; the printed
  `skyLumDriveAsked=/walked=/skipped=` on the materials line proves it either
  way, because asked far above walked is the tick re-entering the guard.
- Golden file or parser: `skyHdriBoundAs`, `lum=`, `SkyLuminance` and `skyLum`
  over every .py, .yml, .yaml and .sh in the tree: 2 hits, both the
  parameter's spelling in `tools/ue/make_sky_material.py` (:25, :61), which
  this batch does not change (VignetteShot.cpp:376 still spells it
  `SkyLuminance`). Nothing parses the keys whose format changed. The one test
  that reads the bind string asserts its `NOTHING/` prefix, the no-dome path
  (run-50 record :73-74), untouched.
- Canon, migration, workflow: none in `ue-probe/`, and the diff is
  `ue-probe/` only.

Undoing a wrong answer here is reverting three files and rendering again. That
is the visual side of the boundary, word for word. Nothing here is a fault of
the builder or the resident: both read the boundary correctly, and the spawn
is the gate's cost, which queue 363 already prices as "a director spawn each
time" until the gate can read something the tree knows.

One sentence for the next reader, because this is a change of MEANING and not
of schema, and meanings are where the next misreading hides: `sky_intensity`
now says two things, how bright the captured sky is and how bright the seen
sky is, so the 12 grid rows and the 3 `fog010_sky` rows that step it now step
both at once. That changes what those series measure, not what they are; it is
undone by another render and it stays visual.

## 2. Question 2: the acceptance line asked for two incompatible things

The line as written: "a night row's meanLuma returns to the order of run 49's
43.6 while the day rows are unmoved". Holding every day row still while moving
night needs a dome field separate from `sky_intensity`, the schema change the
same item forbade. The resident wrote the line and now thinks it wrong; on the
evidence it is wrong in a more specific way than "the day rows move".

THE DAY ROWS ARE NOT ONE CLASS. `vignette-scene.json` carries 33 condition
rows at four values of `sky_intensity`, read this session (:883 to :1366):
  1.00 on 10 rows: grid_sky100 (3), fog_maxop0450/0250/0100/0000/0020/0050/0080
  0.70 on 13 rows: overcast_day, grid_sky070 (3), grid_null_repeat,
                   fog010_sky070, wet_000/060/100, pin_003/030/300/1000
  0.50 on  4 rows: grid_sky050 (3), fog010_sky050
  0.35 on  6 rows: wet_night, pin_setter_night, grid_sky035 (3), fog010_sky035
Two rows have the sun off (wet_night, pin_setter_night); 31 are day rows. The
dome was 1.0 on every row. After this batch it is `sky_intensity` times a gain
of 1.0, so the 10 rows at 1.00 ARE UNMOVED, by arithmetic and not by
intention: they are the change's own null control. The other 21 day rows move,
each by its own value, and 4 of the 6 rows at 0.35 are day rows with a dim
sky, not night rows.

RULING. The day movement is ACCEPTED as part of this landing. 0.70 on
overcast_day is Jafar's value off the sky cross (VignetteShot.cpp:309-311, the
2026-09-14 ruling), and a day dome at 0.70 is that value reaching the surface
the camera sees: a coherent statement and not a slip.

THE ACCEPTANCE LINE IS AMENDED, dictated here and applied by the resident
under D43, who wrote it. In `production/queue/361-one-sky-luminance-serves-day-
and-night-so-night-renders-like-noon.md`, replace "while the day rows are
unmoved" with:
"while the 10 rows whose sky_intensity is 1.00 are unmoved, the dome being
1.00 times a gain of 1.0 there exactly as before, and every other row moves in
proportion to its own sky_intensity; a moved 1.00 row is a fault elsewhere".
A document correction; no second director is owed for it.

WHAT RUN 51 MUST PRINT so a moved day band is never read as a regression:
(1) On the materials line: `skyLumValue=`, `skyLumFrom=`,
    `skyLumSkyIntensity=`, `skyLumGain=1.000/unitless/FIRST-VALUE-OF-A-SERIES`
    and `skyLumReadback=set=/got=/same=yes`, with `skyLumDriveWrote=` equal to
    its `ofWalks=` and `noInstance=0`. These are last-wins and name one
    condition; they prove the drive and not the frames.
(2) The frames prove the rows. Every shot line already carries
    `shotSkyIntensityRead` and the sky band's mean (run-50 record :227-229).
    Group run 51's shot lines by `shotSkyIntensityRead` and read each against
    run 50's same file and camera: the 1.00 group's sky band UNCHANGED within
    the spread that `grid_null_repeat` against `overcast_day` prints inside
    run 51 itself (same sun and sky values, :884-886 and :1094-1096; the same
    cell twice is the run's own noise floor where their other read-backs
    agree); the 0.70, 0.50 and 0.35 groups DOWN, and in that order. No size is
    set here (rule 2): the ordering and the null control are the prediction,
    the sizes are what the run prints.
(3) The dispatch sentinel names run 50's verdict sha as the baseline and this
    record as the reason 21 day rows moved, before the run, so the intention
    is on the tree before the diff exists.

## 3. Question 3: one field moves the ambient twice

The fact: run 50 read `skyDomeMatIsSky=yes`, so the sky light's real-time
capture sees the dome. At night the dome is now 0.35 as the captured surface
and the sky light is 0.35 as the scale on that capture. The builder named the
coupling in the tested header (VignetteSpec.h:3790-3798) and did not resolve
it, and that was the right call: nothing in this container can compute what
the capture does with it.

What CAN be said before the run, as a hypothesis and not a number: relative to
run 50, the seen sky and the captured contribution fall by the same factor on
every row, because the sky light's intensity did not change. What differs is
the street-to-sky ratio ACROSS conditions: if the capture is linear in the
dome, the ambient scales as `sky_intensity` squared while the seen sky scales
as `sky_intensity`, so a night street sits darker under its sky than a day
street does under its own. That is not obviously wrong for a port at night. It
is what run 51 prints.

Options weighed. (A) Accept and read the run. (B) A separate dome field so
the two can be tuned apart: the schema change the item forbade, and a guess
without the reading. (C) Compensate now, the gain above 1.0 or the sky light
at 1.0 on the night rows: a threshold with no series behind it, and queue 361
itself says the sky light is not the lever. (A) stands.

RULING: accepted for this run. THE NUMBER THAT SAYS IT WENT TOO FAR is the
ground band's mean on the exposure-pinned night row, `pin_setter_night`,
where auto-exposure cannot hide a level, and it has a bracket: run 49 (no
dome, the sky light capturing the atmosphere at 0.35) and run 50 (dome at
1.0, captured at 0.35) both printed that file's shot lines. Run 51 inside the
bracket is the ambient landing between two things already seen. Run 51 BELOW
run 49's ground band is the product taking the street darker than the
atmosphere lit it before the photograph came, the wrong direction for a
photograph brought in to light the street. The whole-frame meanLuma the item
printed (43.6 and 142.9 on ue-pinset_night_3.png) is the coarser bracket and
is confounded by the sky band, which is the dome itself; read it second. Below
the bracket, the next rung is (B) as a queue item with the reading beside it,
structural, and it takes a director then.

## 4. Not decided here

Not the gain: 1.0 is the first value of a series and the line says so
(VignetteShot.cpp:396-402; VignetteSpec.h:3891). Not the photograph. Not queue
363's fix (rule 11). One data point filed to it and nothing more: the item's
draft heuristic, "touches no .h in the tested headers", would have gated this
batch too, because instruments.md puts every drive's arithmetic INTO the
tested header, so a visual drive that follows the rules always touches one.
Whatever the gate learns to read, it is not that.

## 5. The quality ladder at close

FIRST WORKING, and the batch says so on its own line. The next rung is the
gain's second value off run 51's pinned rows, which the run-50 record already
carries as Q-E; the rung after that, if the coupling in section 3 proves
wrong, is the separate dome field. No rung is blank; nothing here is a
research task.

## 6. What this ruling covers for director_cadence

The three `ue-probe/` files named in the stamp, and the dictated acceptance
line in queue 361. No builder round is dispatched by this record; nothing is
routed. The commit is the resident's, after `python3 ledger/verify.py` is
green and its footer is pasted from the file.
