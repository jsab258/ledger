<!--RULING spawn=2026-09-16T16:06:18Z paths=ue-probe/Source/LedgerProbe/Public/VignetteSpec.h,ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp,ue-probe/Config/DefaultGame.ini,ue-probe/tests/vignette-spec-test.cpp,tools/ue/make_base_material.py,tools/ue/make_sky_material.py,tools/hdr-to-longlat.py,.github/workflows/ledger-probe-unreal.yml,ledger/Assets/Resources/Sky/polyhaven/belfast_open_field_2k.png,ledger/Assets/Resources/Sky/polyhaven/kloppenheim_04_2k.png,ledger/verify.py,game-design/decision-2026-09-16-ruling-the-photograph-is-the-sky-and-it-lights-the-street.md-->
STATUS: LOG, 2026-09-16. NOT CURRENT once amendment A1 lands and the sky
words are derived from the four read-backs rather than asserted; from then
`VignetteSpec.h` and the run verdict are the reading copies and this file is
their history.

Director ruling, 2026-09-16, on the sky-dome batch: queue 186, D40, D41.

Spawn row, quoted verbatim from `.claude/agent-log.tsv` line 699, the last
studio-director row at the time of writing:
2026-09-16T16:06:18Z	studio-director	fable	default	a635faf48a7ff2f45

HEAD reviewed: 85e3eb09. This spawn had no shell, so NOTHING BELOW WAS RUN:
every line cited was read this session, and every number quoted was printed
by the file it is cited from. Nothing here rests on a memory of a check.

## 0. The verdict in one paragraph

IT LANDS, once two instrument amendments and one dictated one-line fix are in
the same batch; none of the three touches the mechanism. The mechanism, an
8-bit sRGB long-lat PNG on an unlit two-sided engine sphere with the
atmosphere, the sky light and the fog untouched, is approved under D41. THE
AMBIENT DOES CHANGE: the batch's own material script says so, and the change
is accepted as part of this landing. What is refused is the verdict word that
says it did not. The next run's reading protocol is section 3. The mirrored
lower half is not the risk, the horizon band is, and that is a rung and not a
blocker. The parameter-name contract moves next, with one precondition now.

## 1. Structural or visual: I agree it keeps full review, for other reasons

Jafar's boundary (queue 186, 2026-09-16T14:1xZ): "If a wrong answer is undone
by another render, it is visual. If undoing it means a migration, a golden
file, a canon edit or a schema change, it is structural and keeps its full
review."

The field the brief names is not the structural part. `bPhotoDomeBound` at
VignetteSpec.h:2067 is a member of SkyIn, the verdict's INPUT struct,
defaulted false at :2080. The shared schema, `production/specs/vignette-pieces.json`,
is untouched: the C++ reads `C.Hdri` at VignetteShot.cpp:2104, a field every
one of the 33 condition rows (lines 25 to 57) carried before this batch, and
no reader parses the new bool from any file. Undoing it is deleting a line.
On its own it would be visual.

Three things in the batch are structural by his boundary, and they are why
this record exists:
(a) A cook-time asset. `/Game/Ledger/M_LedgerSky` is made by the editor
    script (make_sky_material.py:157) and cooked through
    `DirectoriesToAlwaysCook=/Game/Ledger` (DefaultGame.ini:43). A wrong
    material is undone by another BUILD, not another render.
(b) A workflow change inside the evidence channel: the staging step at
    ledger-probe-unreal.yml:1020-1045 and its count key at :1200. Every
    stale-evidence incident in the casebook lives in this file.
(c) Verdict vocabulary: SkyModelWord gains two words (VignetteSpec.h:2101-2110).
    Words are what every later reader keys on; a word that is wrong about the
    world is a golden-file-class fault, and section 3 finds one.

BOUNDARY FOR WHAT FOLLOWS, so no session re-gates the converter: once this
lands, a different PNG, a horizon treatment in `hdr-to-longlat.py`, a
different kSkyLuminance value or a different scale percentile are VISUAL
under D41 (undone by another render) and commit on the resident's read. A
change to the material's flags, the cook list, the staging step or the verdict
words stays structural.

## 2. Question 1: does it land. Claim by claim, evidence beside each

(a) DEFAULT AND EXISTING READERS. HOLDS. `bPhotoDomeBound(false)` at
    VignetteSpec.h:2080; both new branches are guarded on it (:2101, :2106),
    so false falls through to the three pre-existing branches (:2111-2120)
    unchanged; AmbientModelWord (:2123-2134) never reads it; SkySegment's
    keys (:2529-2539) are the keys it had, `skyHdriBoundAs` already existed.
    Call-site grep (rule 6): `skyModel=|ambientModel=|skyHdriBoundAs` over
    the whole `tools/` tree, 0 files read these keys. The one test that reads
    one, vignette-spec-test.cpp:4648, asserts the `skyHdriBoundAs=NOTHING/`
    prefix, which a default SkyIn still yields.

(b) SKYMODELWORD. HOLDS AS WRITTEN, AND ONE BRANCH IS WRONG ABOUT THE WORLD.
    :2101-2105 returns "photograph-longlat-png-on-an-unlit-dome/
    skyatmosphere-behind-it-lights-and-is-captured" from two booleans, bound
    and Whole, neither of which knows whether the sky light captured the dome
    or the atmosphere. Section 3. The other branch, :2106-2110, says in words
    that the ambient is not the photograph when the sky is incomplete; that
    is correct and stays.

(c) FAIL SOFT. HOLDS for the three named failures, which are all checked
    BEFORE the actor is spawned: material at VignetteShot.cpp:4405-4413, mesh
    at :4414-4421, photograph at :4422-4427, each naming itself in
    skyHdriBoundAs. ONE PATH IS NOT SOFT: at :4455-4460 the dynamic instance
    is created AFTER the actor is spawned, given the mesh and scaled to
    2000 m (:4431-4454). If Create returns null the function returns with a
    2 km sphere standing in the engine's default material, occluding the
    atmosphere for the camera, while `bPhotoDomeBound` reads false
    (:2327-2328, binds=0) and skyModel names the atmosphere. Rare, and rule
    5b says the branch has to be right, not likely. ONE-LINE FIX, DICTATED,
    the resident applies it: inside the `if (GSkyDomeMid == nullptr)` block
    at :4456, before the return, one line:
    `GSkyDome->Destroy(); GSkyDome = nullptr;`
    With that the claim is exact.

(d) DAY OVER NIGHT. HOLDS BY DATA, NOT BY CODE. BindSkyPhoto sits first in
    ApplyCondition (:2104) and returns early on an EMPTY name (:4371), so the
    guarantee is only as good as every row naming a photograph. Every row
    does: 33 of 33 in `vignette-pieces.json` lines 25 to 57, belfast on the
    31 day rows, kloppenheim on wet_night (:26) and pin_setter_night (:57). A
    future row without one would inherit the last photograph, last-wins, and
    the whole-run string at :4389 would not show it. The per-sample key goes
    to the queue (section 7), not into this batch.

(e) THE CHAIN FROM PNG TO PIXEL, EVERY LINK PRINTED (rule 6). The workflow
    never runs `make_sky_material.py` itself (grep `[Ss]ky` over the yml: 4
    hits, all the staging step) and does not need to: make_base_material.py
    :3970-3984 puts its own directory on sys.path, imports and runs it in
    the same editor session, and a raise prints `skyMaterialStatus=RAISED`
    with the message into ue-material.txt, which the build step folds in
    (yml:314). The sphere is cooked (DefaultGame.ini:27, /Engine/BasicShapes)
    and the material is cooked (:43). The staging step copies every *.png
    under `ledger/Assets/Resources/Sky` to `<dest>\SkyHdri\Sky\<dir>\<name>`
    for each texture destination (yml:1045) and prints `stagedSkyFiles=n/m`
    (:1200); the C++ looks first at `SkyHdri/Sky/polyhaven/<name>.png`
    beside the project (VignetteShot.cpp:4245), then beside the exe. Keys at
    every link: stagedSkyFiles; skyMaterialStatus, Wired, Flags, Saved;
    skyHdriFoundAt, DetectedAs; skyHdriBoundAs. LANDS.

(f) THE ARTIFACTS, OPENED (rule 4). Both PNGs were read this session.
    `belfast_open_field_2k.png`, 2048x1024: an overcast sky with cloud
    structure and a brighter patch right of centre, a horizon band of trees
    and a dry field, and below it the sky half mirrored.
    `kloppenheim_04_2k.png`, 2048x1024: a near-uniform grey gradient, a
    conifer horizon, a bright glow right of centre, mirrored below. They are
    what the converter says it writes (hdr-to-longlat.py:259). No level is
    read off the pictures (the eye reads contrast); the converter's printed
    band lines are the numbers and they go in the sentinel (section 9).

(g) THE ASSET TYPE. Within D41 and accepted. PNG is the one encoding this
    binary's ImportTexture has decoded 563 times a run; Radiance is
    unmeasured here and stays unmeasured this run, because the staging filter
    is *.png (yml:1021), so skyHdriDetectedAs answers for the PNG and not
    the .hdr. The cost becomes real the moment the dome feeds the capture:
    the p99.5 scale (hdr-to-longlat.py:83) clips the bright patch to 1.0, so
    the ambient loses the range the photograph had there. A rung (section
    8), not a reason to hold.

(h) UNTESTED BRANCHES. The two new SkyModelWord branches have no test: grep
    `photo|dome|SkyModelWord` over `ue-probe/tests` finds no assertion on
    either. Rule 5b. Folded into amendment A1.

(i) LICENCE. The PNGs are derivatives of the two Poly Haven files already in
    the same directory; nothing new enters the allowlist.
    `tools/attribution-check.py` runs under verify.py on the commit and its
    output is the evidence, not this sentence.

(j) SELFTESTS. Neither `tools/hdr-to-longlat.py --selftest` nor
    `tools/ue/make_sky_material.py --selftest` was run in this spawn. The
    resident runs both before the commit and both PASS lines, with checks=
    and failed=, go in the commit message. A PASS with checks=0 is a failure.

## 3. Question 2: the sky light captures the dome. Ruling and protocol

THE FACT. The sky light is SLS_CapturedScene with real-time capture on
(VignetteShot.cpp:1600-1601, read back at :2254-2255). A real-time capture
renders the atmosphere and every mesh whose material carries the sky flag.
The dome's material carries it ON PURPOSE: make_sky_material.py:81 sets
`is_sky` with the reason "the-skylight-realtime-capture-reads-sky-materials",
and its docstring (:42-48) says a refused flag "only stops feeding the sky
light's real-time capture". hdr-to-longlat.py:45-47 names the extra bounce
the mirrored half adds to that capture. So the batch's own tools say the
capture sees the dome, and a closed 2000 m sphere in front of the atmosphere
means the capture sees ONLY the dome. Against that, VignetteShot.cpp:273-276
and :4315-4321 say the atmosphere "still feeds the sky light's real-time
capture", and the model word at VignetteSpec.h:2103-2104 says
"skyatmosphere-behind-it-lights-and-is-captured". THE BATCH CONTRADICTS
ITSELF, and the half with the flag in it is the half that decides. The
hand-back's belief that the lighting was not touched is refuted by the
batch's own material script. The parent is right.

THE RULING. The ambient change is ACCEPTED as part of this landing. The dome
is NOT to be excluded from the capture. Three reasons:
1. It is the point. The original position at :185-195 named one virtue, that
   the seen sky and the reflected sky are one object; Jafar overturned the
   aesthetic reason (:202-210) and did not overturn that one. A photograph
   seen over a street lit by a clear-sky atmosphere would be the two-object
   failure that position warned about, with the sky band's B/R and the
   road's B/R disagreeing inside one frame.
2. It is a change in the right direction: an overcast photograph lighting a
   street the way an overcast sky does, which three directional fills never
   did and a physical atmosphere with no cloud in it did not either.
3. Excluding it is a plan that begins by weakening the instrument: it would
   keep the old ambient so the old numbers stay comparable, at the price of
   the thing the photograph is for.

Options weighed. (A) Accept, as above. (B) Drop the sky flag: the seen and
the lit sky become two objects; refused. (C) Cube the photograph into the
sky light as SLS_SpecifiedCubemap: a second cook-time asset and a second
unmeasured link for the same light, when the capture already does the job
with no asset. (A) stands.

WHAT IS REFUSED: THE WORD. A run whose skyModel says the atmosphere lights
and is captured while ue-build.txt's `skyMaterialFlags` says `is_sky=taken`
is a verdict contradicting its own build log, and a reader of the ground band
will believe whichever half he read first. That is the confusion the brief
names, and it is concrete.

WHAT THE NEXT RUN MUST PRINT. Amendment A1, in this batch, before dispatch:
(1) Four read-backs on the whole-run sky line, off the live objects after the
    last condition, the way every other key on that line is taken
    (:2244-2329): the dome material's sky flag, its two-sided flag and its
    shading model, read off the parent material of GSkyDomeMid
    (nothing-measured when there is no dome); and the sky light's
    lower-hemisphere-is-solid-colour flag, which this file has never written
    (grep LowerHemisphere over VignetteShot.cpp: 0 hits), so it sits at the
    engine default and nobody has ever printed it. The two-sided read closes
    a second hole: a refused two-sided flag is a dome culled from inside,
    invisible, with `bPhotoDomeBound` true.
(2) skyModel and ambientModel DERIVED from those reads in VignetteSpec.h,
    where g++ runs them, never asserted. Bound and sky flag yes: skyModel
    says the photograph is CAPTURED and the atmosphere is OCCLUDED from the
    capture; ambientModel says the captured sky IS THE PHOTOGRAPH. Bound and
    sky flag no: skyModel says the photograph is NOT CAPTURED and the
    atmosphere lights behind it; ambientModel says the seen sky and the lit
    sky are TWO OBJECTS. Flag unread: the words say nothing-measured. The
    spellings are the builder's; those are the facts each word must carry.
    If the flag proves unreadable off the material at runtime, the editor's
    printed flag is carried into the verdict by name and the word says it
    came from the build log, not from the running object.
(3) The test plants all three cases and asserts each word, accepting case
    first (rule 5b), beside the existing NOTHING/ assertion at
    vignette-spec-test.cpp:4648.
No new per-shot key: band.skyCentre.meanRGB, the ground band,
shotSkyIntensityRead and shotSunIntensityRead (ShotLightLine, :2192-2246)
are already on every shot line and are what the protocol reads.

THE READING PROTOCOL for the run that comes back, so a moved ground band
cannot be misattributed. Baseline: the last landed vignette verdict's shot
lines at the same condition id and camera. Read in this order:
(i)  Is the photograph in the frame at all: the sky band's lumSD and
     p05-p95 spread against the atmosphere's 2.21 and 6.7
     (VignetteShot.cpp:215-216) and against the converter's printed output
     band for the same photograph. A spread still at the atmosphere's is a
     dome no pixel shows, whatever `bPhotoDomeBound` says; stop there and
     read skyMaterialFlags.
(ii) Attribution: if the sky-flag read is yes, every change in the ground
     band's meanRGB and B/R on a shot line whose other read-backs (sun, sky
     intensity, fog, wetness, lamp, grade) equal the baseline's IS THE
     AMBIENT, attributed to the photograph and never to the road, the grade
     or the lamp. If the read is no, the ambient did not move and a moved
     ground band is a real fault somewhere else.
(iii) Level: the exposure-pinned rows (pin_003, pin_030, pin_300, pin_1000,
     `vignette-pieces.json`:53-56) show the ambient's absolute change,
     because auto-exposure cannot hide it there. The sun's units did not
     move (C.SunIntensity, :2119-2120) and the sky's did, so the sun-to-sky
     ratio on every day row is new: shadow depth on lit rows is expected to
     move and is attributed the same way. The SkyLuminance series' second
     value (make_sky_material.py:35-40 calls 1.0 the first value of a series
     never printed) comes off these rows and off nothing else.
(iv) The lower hemisphere: if the sky light reads solid colour below the
     horizon, the mirrored half lights nothing and the converter's named
     cost is nil this run; if it reads otherwise, the ground band carries
     bounce from a mirrored sky and the horizon rung in section 8 moves up.

## 4. Question 3: the mirrored lower half

The mirrored half is below the horizon. The camera sees it only where nothing
occludes a below-horizon direction out to 1000 m; the capture sees it only
if the sky light's lower hemisphere is not solid colour, which is now a
printed read. Neither is asserted here: the frames and the key answer both.

The real content risk is in the SKY half: the horizon band, trees and a dry
field, roughly the lowest tenth of the sky half of `belfast_open_field_2k.png`,
which is the horizon up to about ten degrees of elevation (row 450 of 1024 is
10.9 degrees by band_rows' own mapping, hdr-to-longlat.py:197-203). Any
frame that looks down the street to an open end has that band at its
vanishing point, and if the sky flag took, the band arrives without the
height fog's veil, since keeping sky materials out of fog and aerial
perspective is that flag's documented effect. Meridian is a port; a field is
not a port.

RULING: not a blocker for this run. D40 approved this photograph with its
horizon in it; whether the band shows in these frames is a fact the frames
will print and this container cannot; and the treatment is visual under D41,
a converter change undone by another render. What this run owes: the reader
opens every day still (rule 4) and records, per camera, whether the band is
visible at the vanishing point and whether it is fogged, and Jafar's feel
check reads it beside the Hook sheet. If it shows, the rung is section 8's
Q-C and it commits on the resident's read.

## 5. Question 4: the contract that ships unrun

The names are a contract, not measurement arithmetic, so the instruments.md
sentence the brief cites is not the one that binds. The one that binds is
SurfaceBind.h's own rule, "THE PARAMETER'S ONE SPELLING" (:840-849;
AlbedoGradeParam at :628, WetnessParam at :849). The batch has one spelling
per name in C++ (kSkyMapParam and kSkyLuminanceParam at VignetteShot.cpp
:374-375, used at :4384 and :4461) and one in python (make_sky_material.py
:60-61), cross-checked by a selftest that asserts the exact TEXT("...")
literals and the object path against the .cpp (:262-265) with a synthetic
rejecting fixture (:267). That is a real guard with both arms. What it lacks
is a CALLER: the docstring at :31-33 says the check "is run before every
dispatch", and a grep for make_sky_material over the whole tree finds eight
hits, none in `ledger/verify.py` or any dispatch script. The contract ships
unrun in exactly the brief's sense.

RULING: the move to SurfaceBind.h is NEXT, not now. NOW, as a precondition of
this landing (amendment A3): both selftests, `tools/ue/make_sky_material.py
--selftest` and `tools/hdr-to-longlat.py --selftest`, are wired into
`ledger/verify.py` beside whatever tool selftests it already runs, so they
run on every commit rather than on a docstring's word; if verify.py has no
such place, that is printed as a finding and both lines run by hand before
every dispatch with their PASS lines in the sentinel. THE MOVE ITSELF, one
inline function per name in SurfaceBind.h, the .cpp taking its spelling from
there, the selftest repointed at the header, MUST LAND BEFORE ANYTHING ELSE
READS THOSE NAMES: before the SkyLuminance series driver, before any
per-condition dome parameter, and before any python tool other than
`make_sky_material.py` spells "SkyMap" or "SkyLuminance". Queue item Q-B.
Why not now: it is three files and a builder round, it changes nothing the
next run measures, and the run is what this item has waited on since
2026-09-09.

## 6. What lands in this batch before dispatch, and who does it

A1  Builder. VignetteSpec.h, VignetteShot.cpp, vignette-spec-test.cpp: the
    four read-backs, the derived words, the three planted cases. Section 3.
A2  Resident, dictated, one line at VignetteShot.cpp:4456 block. Section 2(c).
A3  Resident, one or two lines in `ledger/verify.py`. Section 5.

Routing (waste lessons 7 and 9): A1 is builder work at the builder role's
declared model and maxTurns, taken from its role file at dispatch and named
in the brief, with a countable two-armed exit: (a) the g++ test prints the
three planted cases passing and both selftests print PASS with checks>0, all
pasted into the hand-back; or (b) the budget is reached and a named partial
comes back. Not a top model: nothing in A1 is a design decision, every
decision is written here. This ruling covers A1, A2 and A3 for
director_cadence; no second director is owed for them. A second director IS
owed if A1 finds the sky flag cannot be read off the running material and the
fallback in section 3(2) is taken, because that changes what the word is
evidence of.

## 7. Queue items opened by this ruling (named, not done: rule 11)

Q-A  Per-shot photograph key: the name the dome held when the frame was
     taken on every shot line, plus a whole-run count of rows naming no
     photograph. instruments.md's per-sample rule. Not this batch.
Q-B  The one-spelling move to SurfaceBind.h, section 5, with its precondition.
Q-C  The horizon treatment in `hdr-to-longlat.py`: fade the lowest N degrees
     of the sky half into the band's own mean, printing N, the rows and the
     band numbers before and after, selftest accepting case first; or a
     harbour-horizon photograph, which is Jafar's choice and not ours. Opened
     only if this run's stills show the band.
Q-D  The HDR rung: the Radiance file staged and skyHdriDetectedAs answered
     (the .cpp already anticipates enum=8 at :4275), imported linear, the
     p99.5 clip retired from the ambient. Opened when Q-E has a second value.
Q-E  The SkyLuminance series off the pinned rows, and the photograph's
     bright-patch azimuth printed by the converter so the sun's yaw can be
     aligned with it: from inside a sphere the image is seen mirrored in u,
     so the alignment is a measured number and not an assumption.
The resident assigns the next free queue numbers.

## 8. The quality ladder at close

FIRST WORKING, NOT BEST AVAILABLE, and the batch says so itself in three
places: kSkyLuminance 1.0 (VignetteShot.cpp:383, make_sky_material.py:35-40),
the four atmosphere constants (:278-284, now behind the dome), and the 8-bit
scale. The next rungs are Q-C, Q-D and Q-E. No rung is blank; nothing here is
a research task.

## 9. What the DISPATCH sentinel for this run must carry

The converter's printed lines for both PNGs (scaleFrom, p, scale,
clippedPixels with its denominator; the skyLinear percentiles; bandMeanRGB,
bOverR, lumSD, spread; wrote and bytes). Both selftest PASS lines with
checks=. The expected shape of the four new keys with their nothing-measured
forms. The sha of the last landed vignette verdict that section 3's protocol
reads the shot lines against. Every zero with its denominator.

## 10. Not decided here

Not which photograph: the conditions name them and Jafar approved them. Not
the Mie series: he settled that fork today and it is not to be run. Not the
workflow's 17-character margin: queue 360.
