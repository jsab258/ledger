line: production (asset pipeline)
spec: game-design/decision-2026-09-02-vignette-batch-canon-crews-d1-timebox.md, Ruling 10
acceptance: a figures block placed in Unity; plates regenerated from canon's street-districts line; twenty G7 tags off the five canon names; every image under decals2d/ OPENED and the manifest's review line dated and specific
max_sessions: 2
status: REOPENED 2026-09-14 by Jafar. Was: CLOSED 2026-09-10, not on the ladder (closed by cd55a79c, an archiving commit, with no ruling naming what went with it; see production/queue/275). and untouched for 8 days 2026-09-02. content-wrangler first, then engine-specialist.

1. THE FIGURE. A `figures` block in `vignette-scene.json`: which held body,
   which idle clip, x, z, facing. Sizes come from the fbx manifest and are
   NEVER invented. Then the Unity placement through the existing character
   path. Without it the scene is not an admissible (b) scene, because D1b's
   mandatory contents name at least one clothed character body.

2. THE PLATES. `make_vignette_2d.py` line 289 takes `districts[0]`, so all
   three plates stamp `the Hook`. Canon now carries the map. Make the
   generator READ it and regenerate. The resident measured that a bare re-run
   does not fix this: the generator never reads the map, so the output is
   byte-different and district-identical.

3. THE TAGS. G7 is unblocked; canon carries TANNER, SNIDE, GULL, QUAY FIRM
   and PARADE RATS. Twenty tags off five names, marker and chrome variants,
   deterministic, because a tag must spell its crew.

4. OPEN THE IMAGES. Every file under `production/assets/vignette/decals2d/`
   gets looked at, and the manifest's `review` line changes from `pending` to
   a DATED SENTENCE NAMING WHAT WAS LOOKED AT. Three of eight were opened at
   generation; the rest are unread and the manifest currently says so
   honestly. Rule 4: open the artifact you are shipping.

  RE-SCOPED 2026-09-16 (06:35Z ruling, section 6) for the UE probe, which
  has no skeletal path (0 hits for SkeletalMesh, FBX, AnimSequence, Bone
  under ue-probe/Source) and an importer that reads GLB by magic bytes.
  Item 1 in two halves. Half one, a tool, STARTS NOW: a Blender step in CI
  takes one held body and one clip at one named frame from the 91 files
  under ledger/Assets/Characters, applies the pose, exports a static GLB
  to the props path; body, clip and frame named in the item, sizes from
  the manifest, never invented. Half two, Core: the figures block emitted
  as a prop piece with a dark tint surface, golden regenerated; waits only
  for 333 and 334's Core changes to land, one builder in Core at a time.
  The decal route stays refused: a decal card is opaque and rectangular
  by SurfaceBind.h's own words. No token is needed.

  THE ALLOWLIST LINE IS NOT CORRECTED AND THE RULING'S INSTRUCTION TO
  CORRECT IT IS NOT APPLIED. See queue 335, which carries the reason and
  the evidence. It is withheld, not forgotten.
