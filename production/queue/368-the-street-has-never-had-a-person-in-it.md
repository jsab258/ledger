line: art and engine, jointly (D41 visual; D46 licence)
spec: THE LAST ELEMENT OF JAFAR'S VISUAL SLICE, in his own words from
  2026-09-15: "Tomorrow is the visual slice and nothing else: wetness,
  materials, then dusk with lamps lit and a figure in silhouette, ungated
  under D41." Wetness landed on run 46, the materials on run 47, the lamp lit
  on run 49, the sky on run 51. The figure is the only one of the four never
  begun.

  NOTHING SKELETAL EXISTS ANYWHERE IN THE PROBE. `grep -rn SkeletalMesh
  ue-probe/Source/LedgerProbe/` returned no hits at all on 2026-09-16, and
  `production/specs/vignette-scene.json` has no person in any of its 28
  sections. The 610 pieces are box, cyl, mesh and decal. Forty-two frames of
  this street have been rendered and not one of them has had a human being in
  it.

  WHAT UNBLOCKED IT, checked rather than recalled. Sixteen real Mixamo bodies
  are TRACKED IN GIT under `ledger/Assets/Characters` (Adam through The Boss,
  with X Bot and Y Bot excluded as the grey mannequins), so the PC's checkout
  has them without a fetch. Forty-two clips sit beside them, among them
  Standing Idle 01, Old Man Walk, Walking With Shopping Bag and Leaning On A
  Wall. D46, ruled by Jafar 2026-09-16, puts Mixamo BODIES on the licence
  allowlist the same way animations already were, and nothing is purchased.

  IT IS VISUAL AND NOT STRUCTURAL, and the reasoning is the item's main
  content because it is what lets the work proceed ungated. The figure is a
  CODE-SPAWNED ACTOR, exactly as the sky dome, the fog, the atmosphere, the
  sky light, the camera and the player start already are; none of those is a
  piece. It adds no shape kind, no condition field and no shot row. Each of
  those three WOULD be a schema change and therefore structural under his
  boundary, and the moment one becomes unavoidable this item stops and a
  director rules instead.

  THE FIGURE STANDS ONLY WHERE THE LAMPS ARE LIT, 2 conditions of 33. PROBE
  SCOPING AND NOT A WORLD RULE, and it is written into the code comment as
  such so that no later reader turns it into canon saying the town is empty by
  day. The reason is arithmetic: it leaves the 31 day rows byte-identical, so
  the sky brightness bracket and its null control, which hold to +0.1, keep
  their meaning. A figure in every condition moves frame meanLuma by roughly
  0.2 at the size it will render, which is above that tolerance.

  THE TWO FAILURES TO PRINT WHETHER THEY HAPPEN OR NOT. The mesh HEIGHT IN
  CENTIMETRES, because Mixamo and Unreal disagree about units and the two
  failure modes are a figure a hundred times too large and a hundred times too
  small, neither of which a frame diagnoses on its own. And whether the pose
  EVALUATED or fell back silently to the bind pose, because a T-pose renders
  perfectly well and reports success. The sky dome's destroy-on-failure rule
  at `VignetteShot.cpp:4665` governs both: a grey mannequin left standing
  while the verdict reads no figure is the same fault as a 2 km sphere
  carrying the default material, and worse, because it looks plausible.
acceptance: a night frame from cam_A carries a human figure that reads as a
  person in a coat rather than a mannequin, standing between the camera and a
  lit lantern so that it is dark against the lit ground; the run prints the
  mesh height in centimetres, whether the skin came through, and whether the
  pose evaluated or fell back; and the figure's own core-versus-ring luma is
  printed with its denominator, so that "it is a silhouette" is a number and
  not a look. The 31 day rows are unchanged.
max_sessions: 2
status: IN FLIGHT 2026-09-16 18:15Z, two tier-3 builders, filed as the work
  began rather than after it.

  THE PICK OF BODY AND CLIP IS THE FIRST VALUE OF A SERIES and says so beside
  itself in the code, exactly as kLampEmissiveUnitless and kSkyLuminanceGain
  do. Nothing here is tuned to a frame nobody has seen. What the wear looks
  like in silhouette is judged from the render and not from the filename;
  `tools/mixamo-pick/fetch_bodies.py` already carries the standard in one
  sentence, written months before this item: a silhouette has to read as a
  person in a coat.

  D18 IS ABSOLUTE AND APPLIES HERE: no children anywhere, none rendered, none
  in the crowd. Every body on the list is an adult and the one imported is
  named in the hand-back so that this is checked rather than assumed.
