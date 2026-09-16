line: content (production/specs/vignette-scene.json lighting.lantern and the
  four lantern pieces, the surface binder that would have to carry a lit
  surface kind)
spec: D28 step 2 and the Hook sheet both want dusk with the sodium lamps lit.
  The four lanterns in the spec are pieces of shape box and surface metal
  carrying emissive=true, and THE EMISSIVE FLAG DOES NOT MAKE THE FIXTURE
  GLOW. It spawns a point light 0.05 m below the piece centre and nothing
  else. The box itself renders through the ordinary metal surface, so the lamp
  head is a dark object with an invisible light under it. No globe, no lens,
  no lit element of any kind exists in the scene.
acceptance: the lamp head carries a surface that reads as the emitting part at
  night, and a night frame in which the fixture is measurably the brightest
  warm thing in its own neighbourhood rather than a silhouette against the sky.
  THE TARGET IS MEASURED OFF THE APPROVED REFERENCE rather than chosen: see
  THE REFERENCE HAS THE ANATOMY below
max_sessions: 2
status: READY 2026-09-16, filed from run 48's committed frames and the source.

  READ IN THE CODE, NOT INFERRED FROM THE PICTURE.
  VignetteShot.cpp:1310 to 1326 is the whole of what emissive does: "A POINT
  LIGHT UNDER EVERY EMISSIVE PIECE", then `if (!P.Emissive) { continue; }` and
  a SpawnPointLight. Grepping SurfaceBind.h and tools/ue/make_base_material.py
  for emissive, EmissiveColor and selfillum returns ZERO hits in either, so
  the surface binder never learns the piece is meant to emit. The four pieces
  are the only emissive ones in the file, 4 of 610, and each reads
  shape=box surface=metal asset=None bom=E2_sodium_lantern_head.

  SEEN IN THE FRAME. Magnified from ue-pinset_night_3.png, both lamp heads are
  dark rectangles on dark poles against a pale sky. Over the whole frame, 26
  pixels of 921600 have R minus B at or above 20, the brightest of them at
  luma 68, and the brightest pixel in the frame is the neutral sky at 181.
  There is no warm bright thing anywhere. The one warm source that DOES render
  in this street is a window practical in vign_camA_night: 23 pixels at
  (1045,170) to (1051,173), peak R minus B of 130 at rgb 131/108/1, with soft
  falloff around it. So the glow mechanism works in this scene and the lamp
  simply has nothing to glow with.

  THE ORDER THIS IMPLIES, and it is the opposite of the one the studio was
  about to take. Exposure was the standing suspect. It is not the cause: a
  tonemap is monotone, so no exposure makes a fixture darker than the sky
  behind it come out brighter than it. Exposure is still owed for a different
  reason (queue 332 and 334), but a lit lamp does not arrive with it.

  WHAT MUST NOT BE GUESSED ON THE WAY. lighting.lantern's own note says range
  18.0 and intensity 3.2 "are NOT derived and are the first values of a series
  that has never been printed: they are the numbers the night frame will be
  tuned from once one exists, and rule 2 forbids calling them anything better
  than that". That still stands. The colour IS derived and is not in question:
  589 nm low pressure sodium through the CIE 1931 functions, gamma 1.000 /
  0.857 / 0.000.

  THIS IS SPEC AND ENGINE WORK, NOT A TOOL. It touches production/specs and
  probably the surface vocabulary, so it is GATED and wants a director before
  it lands, unlike 329 and 332 beside it.

THE PICTURE IS COMMITTED, at game-design/sim-shots/lamp_reference_vs_probe.jpg:
the two fixtures side by side out of the SAME size source rectangle at the SAME
magnification, with their provenance and both numbers printed under them, so
the comparison is one picture at one scale rather than two memories.

THE REFERENCE HAS THE ANATOMY AND THE PROBE HAS HALF OF IT, read 2026-09-16 off
production/art/atlas-01/concepts/hook.png on origin/art/atlas-01, which is the
approved reference under D41. Its harbour panel carries a wall lamp, magnified
and looked at rather than described: A DARK METAL SHADE WITH A GLOWING GLASS
GLOBE UNDER IT, a wire cage over the globe, and visible warm spill on the wall
beside it. The probe's lantern is the SHADE ONLY. The glowing part does not
exist as geometry or as a surface.

  MEASURED, so the acceptance is a number and not an adjective. The reference
  lamp's lit element, the blob at (146,189) to (170,203) in a 1024x1536 sheet:

      maxLuma   242 of 255
      maxWarm   140  (R minus B, sRGB bytes)
      meanLuma  188  over its own 141 pixels

  Its lit window below it, (41,290) to (58,334), reads maxLuma 237 maxWarm 115
  meanLuma 138 over 460 pixels. Over the whole harbour panel, 5981 pixels of
  563200 (1.06 per cent) are both warm and bright at R minus B at or above 40
  AND luma at or above 100.

  THE PROBE'S NIGHT FRAME READS ZERO AT A LOOSER BOUND. ue-pinset_night_3.png
  has no pixel at all that is both luma 120 or more and R minus B 20 or more.
  The reference's 5981 are counted at the STRICTER threshold. That is the gap,
  stated as two counts over two stated denominators rather than as an
  impression.

  AND IT SETTLES THE SKY QUESTION BEFORE ANYONE SPENDS A RUN ON IT. The
  reference lamp is lit against a STILL BRIGHT overcast sky and reads as lit
  anyway, because the globe at 242 is brighter than the sky behind it. So the
  fix is not to darken the sky and it is not the exposure. It is the globe.

  RULED 2026-09-16 (06:35Z ruling, section 3): the NARROWER change, in the
  engine and the material where the flag is already half-read. Core's own
  field comment calls the emissive pieces "the lantern bowls"
  (StreetVignette.cs 89), so the spec already says they emit; no new surface
  kind, no golden, no CoreTests change. EmissiveColor vector parameter,
  default black, asserted in --selftest; a per-piece material instance on
  the decal-card precedent (VignetteShot.cpp 4089); driven by
  ApplyCondition's LanternsOn through a write-on-change guard; read back on
  the shot line; the strength an engine constant named as the first value of
  a series and printed on the scene line; the acceptance instrument is the
  projected lantern rectangle against its ring, in the tested header, three
  fixtures. Structural by the wetness precedent (a parameter, a node, a
  readback key): full review at landing. Next rung: housing and bowl as two
  pieces, for the day look, named on the ladder. Builds AFTER 329, 332 and
  337 because it shares their files.

  AND ONE CORRECTION TO THIS ITEM'S OWN TEXT, applied under D43. The
  reference measurement above is read off the Hook sheet's HARBOUR panel,
  which is a DAY frame with a lamp lit in it. THE PROJECT HAS NO DUSK
  REFERENCE SHEET AT ALL: the ruling grepped the spec for dusk and found
  zero. So the numbers above are a fair target for what a lit lamp looks
  like, and they are NOT a dusk reference. The dusk frame's judge is D41's
  second path until a dusk sheet exists, and that blank rung is now a row on
  the quality ladder.

THE IMPLEMENTATION MAP, 2026-09-16, BOUGHT WITH A WHOLE AGENT'S BUDGET AND
WRITTEN DOWN SO IT IS NEVER BOUGHT TWICE. An engine-specialist spent 49 tool
calls and wrote no code. What it produced instead is below, every site traced
against the tree rather than against the ruling. The next agent starts at turn
one with this.

  THE RULING'S LINE NUMBERS ARE UNIFORMLY ABOUT 19 LINES STALE. Every block it
  names is the right block and every number is wrong, consistent with one
  insertion upstream since it was written. Corrected:

      emissive block, "1310 to 1326"      is 1329-1347, with Lamp at 1332
      ApplyCondition visibility, ":1798"  is 1817-1818
      generator docstring, ":1083"        is 1077-1091
      decal precedent, ":4089"            is the ONE INSTANCE PER PIECE
                                          comment at 4097; the decal card's
                                          Create is 4227 and the generic
                                          per-piece Create is 4260

  (a) THE PARAMETER, tools/ue/make_base_material.py. EMISSIVE_PARAM and
  EMISSIVE_PARAM_DEFAULT beside VECTOR_PARAMS at :167, and KEPT OUT of
  VECTOR_PARAMS for the reason the file already gives for keeping WETNESS_PARAM
  out of SCALAR_PARAMS at :170-186: the summary at :2526-2532 prints
  vectors=<joined>/default.<one default>, so a second name there prints one
  default over two parameters. Name-readback loop at :3550 takes
  VECTOR_PARAMS + [EMISSIVE_PARAM]. The node goes beside grade at :3345-3366,
  a MaterialExpressionVectorParameter with the default set the two ways the
  grade block already tries. One wire, with the other connect_prop calls at
  :3488-3502.

  (b) THE DENOMINATOR IS 19 TODAY AND 20 AFTER, counted at the call sites and
  not assumed: 2 connect_uv_head + 6 connect in the UV chain (:3311-3318),
  3 samplers making 2 each (:3425-3459, called at :3480), then
  albedograde-to-grade, grade-to-basecolor, wetfloor-to-wetlerp,
  wetness-to-wetlerp, wetlerp-to-roughness. 8 + 6 + 5 = 19. This is the one
  number in the ruling the tree bears out exactly.

  (c) THE PER-PIECE INSTANCE ALREADY EXISTS AND THE RULING READS AS IF IT DOES
  NOT. VignetteShot.cpp:4260 already does
  UMaterialInstanceDynamic::Create(GBaseMaterial, *Found) for every non-decal
  piece, under the ONE INSTANCE PER PIECE comment at :4097, and the lanterns
  are shape=box surface=metal so they take that path. The work is to RECORD
  the existing MID for pieces where Pc.Emissive, not to create a second.
  AND IT OWES A DENOMINATOR the ruling does not name: a lantern falling down
  any unpainted exit (NoBind :4128, NoActor :4137, NoComponent :4139,
  NoInstance :4261) has no MID and cannot glow, so the drive prints emissive
  pieces holding an instance over emissive pieces in the file.

  (d) THE DRIVE, VignetteShot.cpp:1817-1818, the two-line lantern visibility
  loop. Copy ReDriveWetness at :1625-1759 in shape: a guard struct in the
  tested header (WetRedrive at SurfaceBind.h:1761, its counters at
  :1790-1836), counters on a done line, readback taken in the same few
  statements as the set. ApplyCondition is RE-ENTERED EVERY TICK while a
  condition settles, which is the measured reason that guard exists
  (:1631-1636). Value: the Lamp linear triple times the strength when
  C.LanternsOn, exactly (0,0,0,1) when not.

  (e) THE READBACK, MeasureShot at VignetteShot.cpp:3113-3120, where
  WetShotFields appends its asked-beside-carried segment, after
  ShotControlQuadsNow and ExposurePinNow. Bgra, W and H are in scope there,
  which is what lets a pixel instrument read the frame just decoded.

  (f) THE PROJECTION ALREADY EXISTS AND DOES NOT NEED WRITING.
  SurfaceBind.h:2631 has ProjectFilePoint(Camera, XM, YM, ZM, W, H) returning
  ScreenAt{Px,Py,ForwardM,bAhead}, and :2679 has ControlQuadBox returning
  ScreenBox with CornersAhead and CornersInFrame from four projected corners.
  A PieceScreenBox over the piece's eight corners is a near copy, in the same
  header, exercised by the same binary.

  (g) THE CONSTANT was not chosen because the edit was never reached. Shape
  settled: kLampEmissiveUnitless beside kLampGainUnitless at
  VignetteShot.cpp:141, printed on the scene line beside lampGain in the
  snprintf at :1536-1541, with the colour space named as lampColourSpace
  already does at VignetteSpec.h:760. FLAGGED FOR THE DIRECTOR: 1.0 unitless
  times the linear triple gives emissive (1.0, 0.70, 0.0) linear, while the
  reference globe reads 242 of 255 against a sky at 181, so 1.0 may be under.
  That is the argument for shipping it as a series' first value WITH the
  instrument in the same run, rather than guessing upward.

TWO THINGS THAT NEED A RULING AND NOT A BUILDER'S GUESS:

  1. "THE TESTED HEADER" IS TWO HEADERS AND THE WORK DOES NOT FIT IN ONE.
  LedgerVignette::Camera and Piece live in VignetteSpec.h and SurfaceBind.h and
  cannot be reached from FrameStats.h, which deliberately carries no spec type.
  The split that keeps both halves inside binaries verify.py already runs:
  projection in SurfaceBind.h, pixel maths and the formatter in FrameStats.h,
  whose test already builds synthetic BGRA frames (Flat(W,H,B,G,R) at :41).

  2. SECTION 3 CONDITION 3 AND PREDICTION P4 CONTRADICT EACH OTHER. Condition 3
  says the segment prints per lantern per PROBED shot. P4 predicts it prints
  "no" at day rows of the same cameras. A day row is NOT a probed shot:
  ShouldProbeShot at :2789-2794 returns true only when the condition has
  lanterns or practicals on. So P4's refutable prediction is unreachable under
  condition 3. The yes-at-night-no-at-day pair in ONE run is this item's
  acceptance sentence, which argues for P4 and for printing on every shot line
  with a decoded frame.

AND THE DISPATCH WAS SIZED WRONG, which is the resident's finding about its own
brief. The brief named four call sites across five files totalling 13,734
lines in a codebase that is 60 to 70 per cent comment by line, where the
comments are load-bearing and a 20-line window round a call site tells you
nothing. It was a READING task sized as a writing task. SPLIT IT THREE WAYS,
which have almost no overlap: the material generator plus its selftest (self
contained, runs locally, about 80 lines); the instrument plus its three
fixtures (self contained, runs locally); the .cpp wiring (cannot be verified
locally at all). Only the third is unverifiable until CI. And hand each one its
precedent function BY NAME WITH ITS LINE RANGE, because roughly a third of the
spent budget went to finding ReDriveWetness, ControlQuadBox and the paint
loop's Create.

THE RECORD'S CONTENT CLAIMS HOLD, re-checked by the resident because the agent
declined to take three of them on trust and was right to: 0 hits for emissive
or selfillum in SurfaceBind.h and make_base_material.py, 4 emissive pieces of
610, and StreetVignette.cs:89 reads `public bool Emissive;    // the lantern
bowls, and nothing else`.

