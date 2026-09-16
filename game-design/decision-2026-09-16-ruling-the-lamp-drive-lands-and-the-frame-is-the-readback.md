<!--RULING spawn=2026-09-16T13:03:17Z paths=ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp queue=333 third=c-->
STATUS: LOG, 2026-09-16. NOT CURRENT once queue 333's follow-ups land (the
drive guard moves into the tested header, the 4994 shot row, the length
printer); from then VignetteShot.cpp and queue 333 are the reading copies and
this file is their history.

Decision record, written 2026-09-16 by the studio director spawned at
13:03:17Z, answering the resident's brief `brief-director-lamp.md`. No code was
written and nothing was committed by this director.

# Ruling: queue 333 third (c) lands; the drive guard ships unrun this once and moves next; the frame is the value's readback and the build verdict is the parameter's

## The spawn row this record answers

Line 697 of `.claude/agent-log.tsv`, quoted verbatim, tabs and all:

    2026-09-16T13:03:17Z	studio-director	fable	default	abdf8958536bbf273

The gate this clears: `ledger/verify.py` red with `DIRECTOR NOT SPAWNED: 340
GATED line(s) ... 0 director row(s) newer than the reference`. The batch under
review is the working-tree change to
`/home/user/ledger/ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp`
(+334 lines by the brief's count). This director has no shell, so the FILE was
read, not the diff: every new site was located by grep over the file and read
in context. Other dirty paths (outbox, queue, agent logs) are the resident's
and were not reviewed.

## 0. Premise check

The change lights a sodium lantern's own glass in a late-analog British port
town at dusk, off the file's stated lantern colour (589 nm sodium through the
CIE functions, canon and queue 333). It touches no world fact, no era, no
brand. It is in service of the visual slice Jafar ordered today (dusk with
lamps lit, judged against the Hook sheet). Premise holds; nothing in the
change re-frames it.

## 1. Question 1: does this batch land? YES, with one resident check and one named follow-up

Every claim below was traced to a line opened this session; the line numbers
are the working tree's.

1a. The denominator. `LanternsInFile` is
`LedgerVignette::EmissiveCount(GSpec.Pieces)` at BOTH emit sites:
`LampDriveSegment` at 1961 and `LampGlowNow` at 3200, the latter passed as the
second argument of `LedgerFrame::LampGlowSegment(Patches, InFile, bDecoded, 0)`
at 3229, whose signature at `FrameStats.h` 2270 to 2272 is
`(const std::vector<LampPatch>&, int LanternsInFile, bool bDecodedFrame, int
MaxShown)`. `Patches.size()` appears at neither site. `EmissiveCount` at
`VignetteSpec.h` 701 to 706 counts `Pieces[I].Emissive` and nothing else.
`Held` on the done line is `GLampPieces.size()` (1962), and the push at 4639
to 4646 happens only for `Pc.Emissive` pieces that survived the paint loop's
four unpainted exits, so held over inFile is the count that can glow over the
count the file asks for, as the map at queue 333 (c) required. CONFIRMED.

1b. Definition before use, same anonymous namespace. `LampPiece` and
`GLampPieces` 714 to 720 (used 1912, 1962, 4645); `LampDrive` and
`GLampDrive` 736 to 757 (used 1887 onward, 1964 onward);
`ReDriveLampEmissive` 1885, called once at 2055 inside `ApplyCondition`,
unconditionally, immediately beside the lantern visibility loop at 2048 to
2049; `LampDriveSegment` 1959, called at 2799 on the materials done line
beside `WetRedriveSegment`; `LampGlowNow` 3198, called at 3283, 3301 and
3427 inside `MeasureShot` (3235 onward); the push at 4645 is inside
`BindSurfaces`, declared at 796. `NoSpaces`, `SrgbToLinear` and
`EmissiveCount` are `LedgerVignette` (using-directive at 111). CONFIRMED.

1c. The segment on every exit. One grep over the whole file for
`GShotLines.push_back` returns exactly four producers of a shot line: 3276
(NO-FILE), 3294 (UNDECODABLE), 3428 (decoded) and 4994 (the shot loop's
NO-SUCH-CAMERA-OR-CONDITION row, outside `MeasureShot`). The three inside
`MeasureShot` carry `LampGlowNow`: with `(S, nullptr, 0, 0)` at 3283 and
3301, where the tested formatter prints
`lampGlow=nothing-measured/this-shot-line-carries-no-decoded-frame
lampGlowExamined=0/inFile=%d` (`FrameStats.h` 2277 to 2280), and with the
decoded `Bgra`, `W`, `H` at 3427. The only line with a decoded frame is
3428's and it carries the segment, so section 3.4 of the wire-or-delete
ruling (its line 411 to 412: every shot line that has a decoded frame, per
lantern, with its denominator, and `(+N not shown)` if capped) is met.
Carrying the key on the two frameless exits is ACCEPTED as going further
than 3.4 in the right direction: a shot whose file never landed measured
nothing, which is a different fact from a dark lantern. The fourth producer
at 4994 to 4998 carries `ShotCamAndCaptureNow()` and
`ShotControlQuadsNow(S, false)` but not the lamp key. It has no decoded
frame, so 3.4 does not bind it, and it does NOT block landing; it is the
named follow-up in section 5, because a grep counting `lampGlow` over shot
lines would otherwise read one short on any run with a mis-named camera.
The comment at 3104, "all four of MeasureShot's exits", is loose wording:
`MeasureShot` has three line-producing exits and the fourth is the loop's.

1d. No cap. `MaxShown` is passed 0 at 3229, and the reason at 3222 to 3228
is the right one under rule 2: four emissive pieces is not a number that
needs a cap and any cap would be unmeasured. `lampGlowShown=%d/notShown=%d`
prints on every decoded line (`FrameStats.h` 2309), so the cap announces
itself whether or not it bites. ONE THING THIS DIRECTOR DID NOT OPEN: the
body of `LampGlowSegment` between 2286 and 2312, where "0 or less means no
cap" is implemented. That is third (b), landed in `d9af9a3d` in the tested
header, and it is the resident's check in section 4, not a builder's.

1e. The write and the value. `Mid->SetVectorParameterValue(FName(TEXT(
"EmissiveColor")), Value)` at 1917 has two opened precedents in the same
file (1812 and 4610). The value at 1906 to 1911 is `SrgbToLinear` of the
file's `GSpec.Lantern.R/G/B` times a gain, the same conversion
`LinearFromGamma` (932 to 938) applies at the point-light spawn (1417), so
the bulb and the glass cannot disagree about sodium. Off multiplies by a
hard 0.0 and lands `(0,0,0,1)`, which is `EMISSIVE_PARAM_DEFAULT` at
`tools/ue/make_base_material.py` 190, so a day row leaves the glass at the
asset's own default. CONFIRMED.

1f. The guard. `Calls` is incremented at 1887 before the compare at 1889,
`Skipped` on the refused path, `Walks` on the taken one, so walks plus
skipped is calls, the identity the wetness precedent prints. The first call
always walks (`bHaveWant` false). The readback is `Comp->GetMaterial(0) ==
Mid`, asked once per walk (1936 to 1946), a call with precedent in this file
(the wetness NoMid path). CONFIRMED.

1g. The strings. The done-line `snprintf` at 1971 to 1990 carries 13
conversions against 13 arguments, types consistent (the `%.2f` receives a
float promoted to double). The fixed text is about 420 bytes at typical ids
against `char B[560]`; it has no truncation printer, which is the class
queue 310 already names for `WetRedriveSegment`'s `Buf[860]`, and is
inherited rather than new. The scene line's addition at 1627 to 1642
(`lampEmissive=%.2f/unitless/first-value-of-a-series/never-measured`) sits
inside a `snprintf` that DOES announce its cap at 1641. Every key value is
space-free. CONFIRMED.

VERDICT: the batch LANDS. It is a builder's diff that traced every engine
call to an opened signature or an in-file precedent and refused the one it
could not open. Commit it under this record.

## 2. Question 2: move `LampDrive` into the tested header before dispatch, or ship unrun once? SHIP UNRUN THIS ONCE, MOVE IN THE NEXT BATCH

The brief's contradiction is real and is the resident's: "put the guard in a
tested header" and "touch one file" cannot both be obeyed, and the builder
chose one-file, said so at 722 to 733, and held the blast radius.

The decisive fact, read off the code rather than argued: THE UNRUN FORMATTER
CARRIES NO NUMBER ANY DECISION READS. The constant's series, the thing rule 2
protects here, is `coreMaxLuma` against `ringMaxLuma` per lantern on the
shot lines, produced by `MeasureLampPatch` and `LampGlowSegment` in
`FrameStats.h`, which is the tested header and landed in third (b).
`LampDriveSegment` prints whole-run tallies of the guard (asked, walked,
skipped, wrote, visits, held) and one boolean. If it printed nonsense
tonight, the acceptance sentence (yes at night, no at day, in one run) and
the next value of `kLampEmissiveUnitless` would be untouched.

What moving first would buy: the compile-and-run of one `snprintf` and six
increments, against a hand count of 13 conversions to 13 arguments done in
section 1g. What it would cost: one more builder and a delay to the dusk
frame Jafar ordered today, on a 25-minute round trip.

RULED: ship unrun this once. The move is OWED, not optional, under
instruments.md's standing rule of 25 August, and it is queued in section 5
with an accepting fixture first (four emissive pieces, lanterns on, a second
tick: asked=2/walked=1/skipped=1, wrote=4/visits=4, held=4/inFile=4) and a
rejecting fixture (one lantern lost at an unpainted exit: held=3/inFile=4).
It moves BEFORE the second value of the series is written into the constant,
so no bound is ever set from a run whose done line was formatted by unrun
code. The 4994 follow-up rides the same batch because it is the same file.

## 3. Question 3: is the frame an adequate readback for the value, or is the echo owed? THE FRAME IS THE VALUE'S READBACK; THE ECHO IS NOT OWED; THE PARAMETER'S READBACK IS THE BUILD VERDICT, AND IT ALREADY EXISTS

3a. The echo. `GetVectorParameterValue` and `K2_GetVectorParameterValue`
have zero hits over `/home/user/ledger` outside prose (one grep over the
tree: the only engine getters in use are `K2_GetScalarParameterValue` at
1848, 4706, 4707, 4723 and `K2_GetTextureParameterValue` at 4685, 4883). The
2026-09-15 grade ruling (its lines 349 to 361) already recorded that the
AlbedoGrade vector ships with no readback twin and judged the class of risk
small. The builder's refusal to write a call it could not open is upheld:
an unopened signature costs a CI round trip and buys a weaker answer than
the frame, because a parameter echo answers on the game thread and the
frame answers on the render side, which is where the fault of queue 186
lives.

3b. The queue 186 shape, asked as the brief asked it. On the probe verdict
ALONE the batch CANNOT tell "the base material the cook carried has no
EmissiveColor" from "1.0 is too low": both read `lampDriveWrote=4/visits=4
lampDriveCompIsMid=is-the-instance-we-wrote` and `lampGlowLit=0/of=4`. An
echo would not separate them either, on the builder's own account of the
write, and this director records that as reasoning about the engine, not a
check made here.

3c. Where the case IS told apart, from a file this project already
commits. The cook's material is built every run by
`tools/ue/make_base_material.py` in the build step
(`.github/workflows/ledger-probe-unreal.yml` 296 to 322), and "failing here
cannot stop the cook": on a failed script the cook carries the LAST
COMMITTED `M_LedgerSurface.uasset` (2195 to 2202), which is exactly how a
base material comes to predate a parameter. The build verdict already prints
the discriminator. `production/d1-probe/ue-build.txt` line 12 reads, for its
own sha, `materialStatus=COMPILE-UNPROVEN materialScriptReturn=2
materialExistedBefore=yes materialParams=BaseColorMap/NormalMap/RoughnessMap
materialScalars=TilingU/TilingV/Wetness materialConnections=19/19`, which is
the 186 shape in the flesh: a script that returned 2 and an asset that was
already there. Third (a) makes the wire count 20 (queue 333 map (b), counted
at the call sites) and adds `EmissiveColor` to the name-readback loop
(`make_base_material.py` 3812) and to the summary's `vectors=` field (2720
to 2728).

RULED: the reading protocol for the first frame is a PAIR of committed
files at ONE sha, in this order: the build verdict's material line first
(`materialScriptReturn=0`, `materialConnections=20/20`, `vectors=` carrying
`EmissiveColor`), then the probe verdict's `lampGlow` lines. If the material
line reads 20/20 with the vector present and `lampGlowLit` reads 0, the
constant is under and the next value comes off `coreMaxLuma` against
`ringMaxLuma`. If the material line reads a nonzero script return,
`materialExistedBefore=yes` with 19/19, or a `vectors=` list without
`EmissiveColor`, it is the 186 shape, NO CONSTANT MOVES, and the material
step is the item. The one key that would put this on the probe's own done
line is `lampParamOnBase=yes/no/nothing-measured`, asked of `GBaseMaterial`
and not of an instance; it needs an engine signature nobody here can open
today and is queued as the research half of section 5, not written.

## 4. What the resident does now, in this order

1. Commit third (c) under this record. The stamp is line 1 of this file.
2. Before dispatch, ONE grep on the tested suite's own printed output from
   this session: `LampGlowSegment` with `MaxShown=0` on the (b) fixture
   prints `lampGlowShown=<n>/notShown=0` with n equal to the fixture's
   patch count. If it prints `shown=0`, "0 means no cap" is false in the
   header and the call at 3229 needs a builder before dispatch. This is the
   one thing this director did not open (section 1d).
3. Dispatch, and read the two files in the order section 3c gives.
4. `kLampEmissiveUnitless` stays 1.0 until the pair has been read. Not the
   value, not from argument: rule 2, the one place this item was built to
   honour it.

## 5. Queue, named so it is not re-derived

- 333 follow-up (one builder, one file, after the first frame): move
  `LampDrive` and `LampDriveSegment` into `SurfaceBind.h` beside
  `WetRedrive` (1761) and `WetRedriveSegment` (1838), fixtures as section 2
  states, accepting case first; give the segment the length printer queue
  310 names; carry the frameless `lampGlow` branch on the shot loop's
  NO-SUCH-CAMERA-OR-CONDITION line at 4994 to 4998 so every shot line
  carries the key. Must land before the constant's second value.
- 333 research: `lampParamOnBase` on the probe done line, asked of the base
  material. Names the candidate engine call and opens its signature in CI's
  engine headers first; zero precedent in this repository.
- Quality ladder, this aspect: first working is a lit box. Next rung is
  already on the ladder from the 06:35Z ruling: housing and bowl as two
  pieces for the day look. The dusk reference sheet is the blank rung the
  06:35Z ruling named and it stays blank until Jafar approves one.

## 6. Denominators and budget

Examined: 4 shot-line producers over the whole file (one grep, cap not hit);
3 `LampGlowNow` call sites; 2 `EmissiveCount` emit sites; 13 conversions
against 13 arguments; 0 hits for a vector getter over the tree (one grep,
`*.md` prose excluded); 1 stamp regex (`verify.py` 3962 to 3963, extra
`key=value` tokens allowed). Not examined: `LampGlowSegment`'s body 2286 to
2312, the ue-build.txt sha on its line 1, and the diff itself as a diff.
Tool calls at the time of writing: 29 of the brief's 30, declared
`maxTurns: 40`.
