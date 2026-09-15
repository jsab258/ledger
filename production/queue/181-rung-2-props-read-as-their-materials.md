line: art (the visual bar)
spec: Rung 2 of production/ladder.md. Every placed prop reads as the material it is
  meant to be, and the first batch of clutter is placed per
  production/art/atlas-01/PRODUCTION-CATALOGUE.md, in a frame Jafar can see it in.
acceptance: Jafar judges the frame. HIS EYE IS THE GATE and no number passes this rung.
max_sessions: 2
status: READY 2026-09-15, unblocked by Jafar himself; it was BLOCKED 2026-09-09
  behind rung 1 (queue 180) and the paragraph headed UNBLOCKED below quotes the
  words that spent the block. The rung itself was ruled by Jafar on 2026-09-09 as
  part of the visual-first ladder: "rung 2, props read as their materials and the
  first-batch clutter placed per the catalogue".
  WHAT IS ALREADY TRUE AND MUST NOT BE RE-DONE: 22 of 23 props are placed as real
  meshes with collision, proved by run 33 and recorded on production/throughput.md.
  This rung is about how they LOOK, not whether they are there.

  JAFAR ORDERED THIS NEXT, 2026-09-14, in his own words: "The materials are
  next: bins, kerbs and railings still render as untextured white, which is
  the material library item rather than a lighting one, and it is the loudest
  thing in the frame." That is this rung. THE STATUS LINE STILL READS BLOCKED
  BEHIND QUEUE 180 and a resident does not unblock a rung Jafar blocked; the
  dependency is raised to him rather than quietly dropped. Rung 1's frame did
  reach him tonight with its numbers, so the block may be spent, but that is
  his call or a director's.

  AND THE INSTRUMENT WILL TELL WHOEVER TAKES THIS THAT NOTHING IS WRONG.
  Run 622bc39 reads piecesPainted=600/610, piecesUnpainted=10/610,
  paintRoutes=pack.580/tint.10/decal-card.10/decal-multiply.0, and all ten
  unpainted are paintUnpaintedWhy=decal-needs-a-stain-material. By that key
  the street is 98 per cent painted. THE FRAME SHOWS WHITE BINS, WHITE
  RAILINGS AND NEAR-WHITE KERBS. Both are true: the key counts whether a
  piece RECEIVED a material instance, not whether the material RESOLVES to
  the surface it names. So piecesPainted is not evidence for this rung and
  must not be quoted as though it were, which is the exact shape of failure
  CLAUDE.md rule 6 is about (built is not running) one level in: assigned is
  not rendered.
  Queue 123 is DONE and proved THE STREET has its textures on run 25; that
  was the buildings, and it does not cover the props. Queue 176 (the near
  road renders near white) is the same family and may share a cause.
  A useful first question for whoever takes it: does a prop's material
  instance resolve its pack texture at run time, or does it fall back to the
  engine default, which is white? Queue 123's own title names that failure
  mode for the street; nothing has asked it of the props.

  UNBLOCKED 2026-09-15 ON JAFAR'S OWN WORD, and the word is quoted rather than
  paraphrased because a resident does not unblock a rung Jafar blocked. He set
  the block on 2026-09-09 behind rung 1, whose gate is his eye. Message 97 put
  the dependency to him: "You ordered materials next; your ladder holds them
  behind this step. May they start first? Until you say, they wait." He
  answered by ordering the visual slice himself: materials next, then the sky
  itself, then the dusk frame, "That is the picture I judge by, and day is the
  easier half." The person who set the block has spent it. WHAT HE DID NOT GET
  and it is said here rather than smoothed over: rung 1's acceptance as written
  is the two images SIDE BY SIDE, and what reached him was the render alone
  with its numbers. He moved on anyway. The side by side is not therefore done,
  it is overtaken, and game-design/sim-shots/rung1_vs_reference.jpg exists.

  THE CAUSE IS MEASURED AND IT IS NOT WHAT THIS FILE GUESSED. The file's own
  first question was whether a prop's material instance resolves its pack
  texture at run time or falls back to the engine default white. IT RESOLVES.
  Run ce99814's verdict says so per surface and the readback is at pointer
  level, not at intent level:

    surface metal surfaceStatus=RESOLVED pieces=132 piecesAssigned=132/132
      albedoFile=metal.jpg albedoLoadedAs=2048x2048/JPEG-BGRA8/srgb=yes
      albedoParam=BaseColorMap surfaceRoute=pack
      midTexReadback=same-pointer midTexResource=valid
      midCompMaterial=is-the-instance-we-made

  TWELVE OF THE SIXTEEN surface lines read RESOLVED, and the twelve are
  exactly the pack surfaces. The other four are not failures and could not be:
  card and multiply print DECAL-BLEND because they are blend modes and not
  library surfaces, interior and paint_yellow print PROCEDURAL because they are
  built from a tint and a pack file for them is deliberately ignored. Fourteen
  of the sixteen carry the pointer-level readbacks, the two missing being the
  decal blends, which have no library instance to read back. So binding is not
  the fault, the engine default is not in the frame, and the question this file
  posed is ANSWERED AND CLOSED.
  THAT SENTENCE FIRST SAID "every one of the sixteen reads RESOLVED", written
  after checking six of them, and is corrected here rather than quietly fixed.
  Twelve is the right number and it is the better claim, because sixteen would
  have counted four surfaces that can never say RESOLVED as though they had. Bins (6),
  railings (25) and bollards (2) are surface metal; kerbs (95) are surface
  kerb. Counted out of the 610 pieces in production/specs/vignette-pieces.json.

  THREE CAUSES, MEASURED, AND THEY ARE DIFFERENT SIZES.

  ONE. FOUR OF THE SEVENTEEN ALBEDO FILES IN THE PACK ARE NEAR-FLAT CARDS, and
  between them they clothe 411 of the street's 610 pieces. Measured over every
  texel of every albedo file in ledger/Assets/StreamingAssets/CityPack/textures
  (17 examined, the 34 _n and _r maps not examined here), sRGB bytes, lumSD is
  a standard deviation and not a peak:

    kerb      lumMean 184.3  lumSD  6.6  chromaSpread 0.0   95 pieces
    plaster   lumMean 211.7  lumSD  5.8  chromaSpread 7.2   34 pieces
    metal     lumMean 134.8  lumSD  4.6  chromaSpread 22.5  132 pieces
    concrete  lumMean 107.2  lumSD  9.3  chromaSpread 6.8   150 pieces

  against the files that read as materials, AND EVERY NUMBER IN THIS SECOND
  LIST IS A lumSD, not a lumMean. It is labelled because it was not: a reader
  taking brick_grey's 44.3 for a mean would conclude the pack is far darker
  than it is, and a builder reading this item said so.

    brick_grey 44.3   window 35.3   brick_grey_b 28.1   brick_red_b 26.9
    sidewalk   26.4   glass  23.1   brick_red    22.0   wood         15.1
    asphalt    13.8

  kerb.jpg has a chroma spread of EXACTLY 0.0, so R equals G equals B on every
  texel: it is a greyscale card at 184 with almost nothing in it, and that is
  the whole of what a kerbstone wears in this street. NO BOUND IS SET HERE.
  The series above is the reading; the split between 10.1 and 13.8 is a gap in
  a printed series and not a measured threshold, and nothing gates on it.

  TWO. THE UNREAL SIDE APPLIES NO ALBEDO GRADE AND THE COMMENT THAT SAYS IT IS
  MEASURED IS FALSE. AssetLibrary.BuildMaterial multiplies every Unity albedo
  by TextureGrade 0.74/0.76/0.80, and the four ground surfaces by a further
  GroundGrade 0.55. SurfaceBind.h:289 to 313 reproduces both constants, applies
  them in ProceduralAlbedoTexel, and that function returns early for any
  surface whose ProceduralSurfaceIndex is below zero, which is every pack
  surface. So the twelve pack surfaces are bound at full brightness on this
  side. kerb is in IsGroundSurface, so Unity would render it at 0.74 times 0.55
  of its texel and Unreal renders it at 1.00: a factor of about 2.4 on the one
  surface whitest in the frame. SurfaceBind.h:313 claims "the gap is named on
  the materials line as gradeAppliedTo, and it is one number, not a taste."
  grep gradeAppliedTo over ue-probe returns ONE hit and it is that comment.
  There is no materials line and nothing emits the key. A comment promising an
  instrument, twelve lines under a paragraph in the same file warning that a
  comment promising a guard is worse than no guard.

  THREE. THE STATISTIC THAT SEES IT WAS NOT THE ONE ON THE SHEET. Measured over
  the bottom 20 per cent of each frame, every pixel, sRGB:

                        lumMean    p05    p50    p95     sd   share>170
    Hook sheet panel      105.9   48.8   95.2  180.2   43.5    10.40%
    ue-vign_hook_day      114.7   51.1  130.2  179.5   43.7     6.05%

  The mean is 8.8 apart, p05 is 2.3 apart and p95 is 0.7 apart. THE MEDIAN IS
  35 APART. The two ground numbers already on the Hook sheet are p05 (0.2006
  against 0.1935) and the sky median, and both of them matched; neither could
  see this. The shipped instrument already prints it: run ce99814 carries
  band.ground.p50=0.5117 for this shot and my own arithmetic over the same rect
  gives 130.2/255 = 0.5106, so the ruler and the reading agree. The reference
  is 95.2/255 = 0.373. Rendered kerb pixels measured by projecting the kerb
  pieces through cam_hook and sampling 5x5 at each top face: lum 179.7 over the
  12 nearest of 75 on-screen pieces, against a texel mean of 184.3, which is
  the raw card with essentially nothing taken off it. In the reference the
  kerbs are dark wet stone at or below the road; here the kerb is the brightest
  surface in the street, above brick_red, whose RENDERED lum is 155.9. That
  155.9 is a rendered pixel reading and belongs beside 179.7, never in a
  texel column: brick_red's own texel mean is 131.8.

  AND ONE COLUMN OF THE FIRST READING OF THIS SERIES WAS WRONG, found because
  a builder's table disagreed with mine on metal and the disagreement was
  chased rather than averaged. The exploratory pass printed metal's mean RGB as
  127.3/133.4/145.1; it is 124.93/136.49/147.42. THE MECHANISM, proven rather
  than guessed at, on the same data in one run: float32 STRIDED gives
  127.31/133.35/145.10, float32 CONTIGUOUS gives 124.93/136.49/147.42, and
  float64 gives 124.93/136.49/147.42. Same dtype, same texels, different
  answer. numpy's pairwise summation rescues a contiguous reduction and does
  not reach an axis=0 reduction over an Nx3 view, and at 4,194,304 texels the
  naive accumulator reaches 5.24e8 where float32 spacing is 32, so each further
  125 is rounded away.
  WHAT IT DID AND DID NOT TOUCH, because a correction with no scope is a scare.
  It touched ONLY the per-channel mean column, which appears in no queue item.
  lumMean, lumSD and chromaSpread were all computed on CONTIGUOUS 1-D arrays
  and every one reproduces to within 0.005 against float64 across all 17 files:
  kerb 184.32/6.59/0.00, metal 134.83/4.60/22.48. So the tables in this item
  and in queue 300 STAND as printed, and this paragraph is here because a
  reading was wrong somewhere and the somewhere has to be named.

  CROSS-CHECKED AT THREE CAMERAS, because a finding from one viewpoint is a
  finding about a viewpoint. Same projection, same 5x5 patch, same twelve
  nearest of the on-screen kerb pieces, against kerb.jpg's own texel mean of
  184.3:

    vign_hook_day  kerb lum 179.7   (12 of 75 on screen, of 95 in the spec)
    vign_camA_day  kerb lum 199.7   (12 of 76 on screen, of 95)
    vign_camB_day  kerb lum 182.9   (12 of 17 on screen, of 95)

  At cam_A the kerb renders BRIGHTER than its own texture, which is the light
  adding on top of a card that was already pale. Three cameras, one answer.

  WHAT IS NOT CLAIMED. The per-surface rendered figures other than kerb sample
  a piece centre and some of those patches will be catching what is behind or
  beside the piece, so they are indicative and are not evidence for anything.
  Only the kerb row is clean, because a kerb is long and its top face fills the
  patch.

  THE ORDER THAT FOLLOWS, and cause TWO goes first because it is a parity bug
  rather than a taste, it is a code fix, and it moves the loudest surface in
  the frame by a factor of about 2.4 without sourcing anything: queue 299 adds
  the colour parameter and the grade, re-renders, and the frame is looked at
  again before a single texture is replaced. Queue 300 is cause ONE and it
  needs pixels this container cannot fetch, so it goes through the existing
  ambientCG pipeline. Cause THREE is discharged by this entry: the number is
  already printed, it was simply never compared to the sheet.

  THE CATALOGUE IS ON THE ART BRANCH, origin/art/atlas-01, and is read with git show
  rather than by merging or checking out that branch.
