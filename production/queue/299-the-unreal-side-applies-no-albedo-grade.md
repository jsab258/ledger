line: engine (the visual bar), and it is a D1 parity bug rather than a taste
spec: The Unity host multiplies every albedo by TextureGrade 0.74/0.76/0.80 and
  every GROUND surface by a further GroundGrade 0.55. The Unreal side applies
  neither to the twelve pack surfaces, so the two engines render one street from
  one input at two different brightnesses. Give M_LedgerSurface a colour
  parameter, set it per surface from the tested layer, and make the frame that
  comes out of it the thing that is looked at.
acceptance: Three things together, and the third is the one that counts.
  ONE, a run lands in which the surface line for every pack surface prints a
  grade instead of not-built, and the kerb line prints one.
  TWO, band.ground.p50 for vign_hook_day MOVES, measured against ce99814's
  0.5117, and the direction is down. The Hook sheet panel's own ground p50 is
  0.373 over the same bottom-20-per-cent rect, so 0.5117 to 0.373 is the gap
  this item is aimed at. NO PASS BAND IS SET ON THAT NUMBER HERE, because
  choosing how close is close enough is Jafar's eye under D23 and not a
  resident's arithmetic. The item reports the residual, it does not grade it.
  THREE, the frame is opened and looked at, by the person landing it, before
  any number is quoted. A darker kerb that has taken the whole street down with
  it is a worse frame, not a better one, and only the picture can say.
max_sessions: 2
status: READY 2026-09-15. Cause TWO of the three measured in queue 181, filed
  as its own item because it is a code fix with a right answer where the other
  two are sourcing and reporting.

  WHAT WAS READ, in this order, and every line of it is quoted from the file
  rather than remembered.

  ledger/Assets/StreamingAssets/CityPack/ATTRIBUTION.json: all seventeen albedo
  files are ambientCG, CC0 1.0 Universal, 2K-JPG. ambientCG is on
  ledger-v2/research/license-allowlist.md line 5. Nothing in this item fetches
  anything, so no licence question is opened by it.

  ue-probe/Source/LedgerProbe/Public/SurfaceBind.h:289 to 313 carries
  TextureGrade (0.74, 0.76, 0.80) and GroundGrade (0.55) as literals, with the
  comment: "AssetLibrary.BuildMaterial sets mat.color = BaseColour(logical,
  textured), which is TextureGrade for any surface carrying a texture, times
  GroundGrade for the four ground surfaces. Every surface in that host
  therefore renders its albedo DARKENED, and the Unreal base material has no
  colour parameter to darken it with."

  The same block then says: "the twelve surfaces that resolve from the pack are
  still bound at full brightness on this side, because baking a grade into a
  2048x2048 jpeg is per-texel work on every import and a colour parameter on
  the base material is the right answer to it. So these two surfaces are now
  closer to the Unity pair than the twelve around them, the gap is named on the
  materials line as gradeAppliedTo, and it is one number, not a taste."

  THAT LAST CLAUSE IS FALSE AND IT IS PART OF THIS ITEM TO FIX IT. grep
  gradeAppliedTo over ue-probe returns exactly one hit and it is that comment.
  No materials line carries it and no code emits it.
  AND THE FALSE CLAIM HAS TWO HOMES, NOT ONE, WHICH THIS ITEM MISSED AND A
  BUILDER CAUGHT. "the Unreal base material has no colour parameter" is at
  SurfaceBind.h:303 AND at VignetteSpec.h:594, proven with git grep over HEAD
  rather than off disk. This item grepped the TOKEN gradeAppliedTo and found
  its one site; CLAUDE.md rule 1 says to grep the SENTENCE and not the site,
  "the copies sit wherever a later reader was writing at the time". The brief
  that dispatched the work quoted that rule and the item that wrote the brief
  had just broken it. All three passages are corrected, and the only surviving
  hits are inside the corrections quoting what they replaced. It sits twelve lines below
  a paragraph in the same file that says a comment promising a guard is worse
  than no guard, because a reader who believes it does not check. This item's
  reader did believe it, went looking for the key, and found the comment.

  ProceduralAlbedoTexel is where both grades are applied, and it returns early
  when ProceduralSurfaceIndex is below zero. ProceduralSurfaceCount is 2 and
  the two are interior and paint_yellow. Every pack surface takes the early
  return. That is the bug in one sentence: the grade exists, is correct, is
  tested, and is reachable by ten pieces out of 610.

  IsGroundSurface is asphalt, sidewalk, kerb, concrete, character for character
  against AssetLibrary.WetSurfaces. Counted out of the 610 pieces in the spec:
  asphalt 2, sidewalk 5, kerb 95, concrete 150, so 252 pieces take the 0.55 as
  well as the 0.74/0.76/0.80. (This line first read 245 because it counted only
  kerb and concrete and then called the total the ground surfaces; corrected
  here before it landed.)

  tools/ue/make_base_material.py:147 to 148 is where the parameter list lives:
  TEXTURE_PARAMS = ["BaseColorMap", "NormalMap", "RoughnessMap"] and
  SCALAR_PARAMS = ["TilingU", "TilingV"]. There is no vector parameter, which
  is the whole of why the grade has nowhere to go. The generator already knows
  MaterialExpressionVectorParameter (line 640), so the node type is not new.

  VignetteShot.cpp sets TilingU and TilingV and the three textures and nothing
  else, at 3764, 3788 and 4007. There is no colour set anywhere in it.

  WHAT THE NUMBERS SAY TODAY. Rendered kerb pixels, projected through cam_hook
  and sampled 5x5 at each kerb top face, come to lum 179.7 over the twelve
  nearest of 75 on-screen kerb pieces. kerb.jpg's own texel mean is 184.3. So
  the render is the raw card with essentially nothing taken off it, and the
  kerb is the brightest surface in the street, above brick_red at 155.9. In the
  Hook sheet the kerbs are dark wet stone at or below the road.

  THE PREDICTION, WRITTEN BEFORE THE WORK AND ABLE TO FAIL. Following
  ProceduralAlbedoTexel's own arithmetic, which multiplies the grade by
  GroundGrade in GAMMA and only then converts both sides to linear, kerb's
  texel goes from 184 to about 75, concrete's from 107 to about 40 and metal's
  from 135 to about 101, all on lumMean. The landed reading is kerb 74.9,
  concrete 40.4, metal 100.7, so the prediction held.
  THIS PARAGRAPH FIRST SAID "kerb from 184 to about 71" AND "metal from 135 to
  about 96 ON THE RED CHANNEL", and the builder was right to push back on both.
  135 IS METAL'S LUMA AND NOT ITS RED: metal's red channel mean is 124.9 and
  its graded red is 91, so 96 was a luma figure wearing a channel's name. That
  is the instruments.md rule about saying what a number is a statistic OF,
  broken in the item that quotes it. On red rather than luma the kerb lands at
  73, not 71.

  AND A SECOND PREDICTION, WHICH IS THE ONE MOST LIKELY TO FAIL AND IS WRITTEN
  DOWN FOR THAT REASON: THE FULL UNITY GRADE PROBABLY OVERSHOOTS THE SHEET.
  Running ProceduralAlbedoTexel's arithmetic over the whole pack gives, as
  file lumMean before and after:

    kerb      184.3 to  74.8      asphalt    67.9 to  22.6
    concrete  107.2 to  40.2      sidewalk  108.9 to  41.0
    metal     134.8 to 100.8      brick_red 131.8 to  98.4
    plaster   211.7 to 160.1      wood       87.3 to  64.0

  The ground surfaces come down by roughly a third and the wall surfaces by
  roughly a quarter. But the gap this item is aimed at is 0.512 to 0.373 on
  band.ground.p50, which is a factor of 0.73, not 0.33. So the arithmetic says
  parity lands the ground WELL BELOW the reference rather than on it.
  THAT IS NOT A REASON TO APPLY A SMALLER NUMBER. A texel factor and a band
  median are not the same quantity: the band carries sky reflection, shadow and
  surfaces that are not ground, and the tonemap between them is monotone rather
  than linear. This prediction can be wrong for that reason alone, which is why
  it is written before the run rather than after it. What it does establish is
  that PARITY AND THE SHEET MAY DISAGREE, and if they do, choosing between them
  is Jafar's under D23 and a director's until he rules. The builder applies
  parity, reports the residual, and invents nothing.

  THE RISK, NAMED RATHER THAN DISCOVERED. concrete is in IsGroundSurface and is
  the street's largest surface at 150 pieces: 84 are wall TRIM, 7 are at roof
  level and 61 sit on the pavement. (This sentence first read "most of those
  pieces are WALLS rather than ground" and the ruling of 00:52Z counted them
  off the pieces file: 72 sills and lintels, 6 stall fronts, 4 parapet and
  coping, 2 roofdecks, 1 kiosk plinth, 5 chimney pots and 60 chewing-gum discs.
  NOT ONE IS A WALL FACE. The wall faces wear brick_red, brick_grey, plaster
  and wood. Pixel share is unmeasured.) Parity says darken them by 0.55 because that is
  what the other engine does to them. The frame may come out too dark as a
  whole, and if it does that is a finding about Unity's rule and not a reason
  to invent a different constant here. Print the before and after per surface,
  land it, look at it, and say so.

  ONE NUMBER IN THE SURROUNDING DOCUMENTATION MOVES AND IT IS NOT A FAULT:
  materialConnections goes 14/14 to 16/16, because the grade adds a Multiply
  and its parameter. Three comments in make_base_material.py stated 14 as
  though it were a constant. Nothing compares against the literal, since MADE
  is wired == asked, so no gate moves; a reviewer reading 16 against a
  documented 14 would have been misled, and the three were corrected.

  NO NEW VERDICT KEY, and the reason is a standing rule rather than taste:
  Jafar's rule is no new instrument this month unless one is retired in the
  same batch. None is being retired here. The surface line ALREADY carries
  tintTexel, tintFrom, tintPattern and roughnessTexel, and for every pack
  surface all four currently print not-built. Filling those in for a graded
  pack surface adds no key and turns four dead fields live. The false clause in
  the SurfaceBind.h comment is DELETED rather than made true, because making it
  true costs a key this month cannot spend.

  RULED 2026-09-15 00:52Z (decision-2026-09-15-ruling-the-grade-lands-as-the-
  legacy-number-and-the-outbox-brief-was-never-a-net.md): lands as parity, no
  constant chosen, the residual to Jafar labelled PARTIAL because the legacy
  build stacks LightModel.AlbedoScale(0.6) = 0.73 on the ground family at the
  judged wetness and this side has no wetness read site (queue 186). He is
  asked which way the gap runs, not for a number. The split of the ground
  family from the wetness list is queue 302 and waits on this item's frame.
