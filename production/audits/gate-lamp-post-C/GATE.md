# Lamp post C's gate (his order of 21 October, item 5, first piece)

The game's own vignette camera, 2560 x 1440, three views, one fresh reviewer (Opus) a view, each beside its last good picture (this morning's, F:/LedgerTools/gate/last-good/lamp-post-C) and against the Hook sheet and the KCD2 frames. Pictures: F:/LedgerTools/gate/new/lamp-post-C; previews production/previews/lamp-post-c-*-2026-10-21.jpg.

## Round 1, 13:24 (the editor's street not yet re-imported)

- Hook by day: FAIL. The old lamp's box lantern and swan-neck top still stood inside each new lamp.
- Reverse by day: FAIL, the same fault.
- Night: PASS (its "dark block under the lantern" was the same leftover).
- Cause: the street had been re-exported without the old lamps, but this PC's editor still held the old import. Fix: tools/ue/import_street.py run locally (165 of 165 meshes). Not a fault of the piece; the build machine re-imports every run.

## Round 2, 13:34

- Hook by day: FAIL. The concrete reads as smooth, near-white painted or plastic posts (191, 188, 182, flat), not weathered precast concrete.
- Reverse by day: PASS. Shortfall listed: the concrete too clean.
- Night: PASS. Watch points: the near column's lit face is bright, consistent with a pale column 1 m from its lamp; the bowl's core pale rather than deep sodium orange.
- Known shortfalls, all three: no wear, rain streaks or grime at the foot (the kit's wear is a later step of the order); the bowl reads white by day, not yellowed acrylic; the number plate blank; the arm level (the target's own choice).

## The fix for round 3

The kit's master material, the order's next step: world-aligned detail from the street's own concrete photograph, a dirt band at the foot, and the concrete's starting colour moved to the dark end of aged concrete (production/research/aaa-street/KIT-MATERIALS-2026-10-21.md; production/specs/kit-materials.json). All three views are reviewed again after it, since the material shows in each.

## Round 3, 13:48: PASSED, all three views

- Hook by day: PASS. The concrete shows a mottled photographic texture and reads as concrete; the bowl does not glow by day (about 200 against the window frames' 200 to 222); no clipping (pillar box 1 m nearer at x 27, the column at x 28; the bins clear).
- Reverse by day: PASS. Matt, mottled concrete, not plastic.
- Night: PASS. Watch point: the near east column's road face burns to flat pale yellow 3 to 4 m up, under its own lamp.
- Known shortfalls, listed: the dirt at the foot barely shows (about 10 per cent darker); no rain streaks or rust runs from the spigot; the bowl reads opal white, not yellowed; the number plate blank; the arm a crisp right angle; the Hook sheet shows no lamp column, and the near one is now a pale vertical between Fresh Fish and Mickey's. The scene's older gaps (no parked cars, white puddles, a flat hill) are unchanged.
- These views are now the lamp's last good pictures (F:/LedgerTools/gate/last-good/lamp-post-C). Packaged and walked: owed to the next build machine run.

## The close views, 14:02 (new views, no earlier picture; -PageShots=at)

- Across, by day: PASS on the lamp (upright, grounded, about 4.9 m, the arm over the road, grained concrete, no glow by day). The picture is not for his page: the two passers-by wear the white base layer (the open clothes fault) and a doormat lies mid-pavement (open).
- Across, at night: PASS on the lamp (the head glows about as bright as the fish shop's window; the pool under the head; the column's face fades by about 4 stops to the foot). The same people fault.
- Under, by day: FAIL. From below the bowl vanished (no yellowing, no surface: an open white dish) and the jacket read as a solid white rod; also the satellite dish's bracket shows through its face (an older fault of the street, not the lamp's). Fix, try 1: the jacket made see-through glass (a translucent kind of its own), the bowl a cream-amber yellowed acrylic at 0.55 opacity (production/specs/kit-materials.json). Re-shot with a second view from the road.

## The close views again, 14:11 (the new glass; under and from the road)

- From the road, by day: PASS. The bowl reads cream-amber acrylic, darker than the sky (no glow by day); the arc tube shows through.
- From the road, at night: FAIL. The column's road face clips to a flat saturated yellow from the arm to the frame's foot, brighter than the lit window: the pool's cone, straight down 0.78 m from the column, lights it from 1 m. Fix, try 1: the pool leans 20 degrees out over the road (unreal-look.json lantern_pool_tilt_deg), as a cut-off lantern throws its light.
- From under, by day (14:11): FAIL again on the jacket, which still read as one solid pale rod with no arc tube inside (try 1 did not cure it in this view). Try 2 (14:26): the cold arc tube a darker amber-brown, the jacket at 0.15 opacity. Still one pale rod by eye: the yellowed bowl (0.55 opacity, the bowl's own fix) washes everything inside it. **Set aside after two tries** (CLAUDE.md): the lamp's inner tube reads as one pale rod from directly below; listed as a known fault of the piece. The direction for research: the bowl's real transmission (the target's 0.85) against the visibility the first review asked for, a refractive bowl, or the bowl's surface sheen carrying its yellowing instead of its opacity.
- Round 4 of the close views (14:26): from the road by day PASS (the bowl cream and see-through, no glow by day); from the road at night PASS (the column now reads as lit concrete fading downward, 242/161/0 near the joint to 101/38/0 low down: the tilt cured the clipped bar); from under at night PASS. From under by day: the inner tube, set aside above.

## Round 4 of the three views, 14:30 (the pools leaned, the new glass): PASSED

- Hook by day: PASS (the bowls cream-amber, no glow by day). Reverse by day: PASS. Night: PASS: the light moved off the footways and fronts onto the road; each pool under its head and spilling over the road; the near columns' hot stripes gone. Watch point: the pavement in front of Mickey's is now among the darkest walkable areas, the woman there a silhouette; Mickey's night view (item 1.1, passed 8 October) is checked against its 8 October picture.
- These are now the lamp's last good pictures.
- Mickey's night view (item 1.1, against its 8 October pass): FAIL. Its window went near-black (the sill, plant, directory and MINICABS lettering at 5 to 9 per cent of 8 October) and two hard orange strips appeared at sill height. Cause: at 20 degrees the pool's back edge (26 degrees from straight down) misses the house fronts 2.3 m behind the lantern. Try 2 of the tilt: 11 degrees (back edge 35: the fronts from sill height down, not the column's top metre).
- Try 2 of the tilt (11 degrees): Mickey's night still near-black (mean 2.8 against 15.5 on 8 October). Measured: the sill lies about 37 degrees off a straight-down axis, 47 at 11 degrees, past the 46-degree outer edge; no lean keeps both. **Set aside after two tries**: the tilt back to 0 (Mickey's lit as when it passed), the glare on the column's road face under its own lamp listed as a known fault (FINDINGS.md), its research direction lighting channels or a cut-off lantern's light profile.

## Round 5, straight-down pools again (14:53)

- Night: the pools sit under their heads, Mickey's front and the footways lit again, nothing else broken; the reviewer's one fault is the near column's clipped road-face stripe, the fault set aside above and listed in FINDINGS.md, so it does not block (CLAUDE.md: known shortfalls are listed, failing nothing alone). The day views are unchanged by the pools (rounds 3 and 4 passed).
- Mickey's night (item 1.1, against 8 October): PASS. About 37 per cent darker overall (the blind about half), every key thing still legible: the phone number, MINICABS 24 HOURS, the clock, map, board, cards, plant and directories. Noted beside it: two lit windows across the road now reflect in its glass; the back door and the directories changed with the merged sets, not the lamps.
- Lamp post C: through its gate, with two faults listed (FINDINGS.md). Its page: production/approvals/2026-10-21-lamp.

## His ruling, 21 October: weathered and a shade darker (two tries)

- Try 1 (15:31, rain streaks of 70 even runs, growth on top faces, a stronger foot band, the concrete 0.85 darker): hook day PASS and reverse day PASS (a shade darker, a soft grimy foot; the streaks too faint to read as rain staining); the column close up FAIL: "a uniform full-height grain that reads like a grey timber pole, with no rain runs from the arm, joint, spigot or plate".
- Try 2 (16:20, 22 wider, varied runs hanging from the piece's top and fading down 2.6 m): by eye at the close view the runs are thin and faint; it does not read as run-off staining either. **Set aside after two tries.** Kept: the darker concrete and the grimy foot. Research direction: run-offs placed from their sources (the cloud's wear masks as decals under the arm and spigot, the rust bleed under the spigot), or staining baked onto the column in Blender. Not done by his ruling; shown on his next page with this shortfall first.

## 22 October: the staining, a third direction (his message: "then the lamp's staining")

**The research** (production/research/street-wear/LAMP-STAINING-BAKE-2026-10-22.md).
- The two tries were one even, world-aligned pattern on every face, so they read as grain.
- The column's own design names its stains and their sources: lime under the arm and from the top, rust under the door plate's screws and the spigot, algae on the shaded face and the arm's top.
- So they are baked where it puts them, the method that passed on Rita's front today.

**The build.**
- **The recipe:** tools/art-recipes/kit_stain.py, with the spec production/specs/kit-wear/lamp_post_C.json.
- **The bake:** the column's faces get their own unwrap. Cycles bakes each texel's position and facing, and the stains are drawn on those.
- **The kit material:** the shared material gains an optional StainMap with StainStrength, default 0, so every other slot is as it was (tools/ue/make_kit_materials.py; 91/91 wired). The column's slot takes strength 1, and its world-aligned runs are off.
- **Added within canon:** broad dark run-off below the arm and from the top, 1 to 2.5 m. It is what real columns show, and what the 21 October close reviewer asked for. The design's lime, rust and algae alone are too small to read from the pavement.
- **What git carries:** the kit's materials and the lamp's mesh are tracked in git. Only the four assets meant to change are committed: the opaque master, the column's material, its stain and the mesh. The rest were restored to 21 October's, and the column measured identical.

**Round 1** (F:/LedgerTools/gate/new/lamp-post-C/s4):
- **The column close up: PASS**, only partly answering the weathering. The run-off was too weak to read, and with the even pattern gone the shaft was 4 to 5% lighter than his approved shade.
- **From the road: FAIL** on the lantern: its bowl and tube read about 12 levels lighter than on 21 October.
- **The lantern, measured three ways.** In each, the bowl stays at 170 against 21 October's 157:
  - today's build with the column's stain switched off;
  - 21 October's committed glass materials restored;
  - 21 October's committed lamp mesh restored.
  
  Two pictures of 21 October agree with each other, as do two of today. So it is not this change, nor the lamp's own files: a drift elsewhere in the scene since 21 October, cause not found, listed in FINDINGS.md.
- **Fixes:**
  - the shaft's colour to 0.91 of 21 October's, so its shade is his again (134 against 136 mid-shaft in the close view);
  - the run-off darker, broader, longer and held longer, spread across the face under the arm;
  - two faults of the recipe's own found on the way: the run-offs fell on one spot, and each new stain was drawn under the earlier ones, not over.

**Round 2** (F:/LedgerTools/gate/new/lamp-post-C/s5; one fresh reviewer a view): **all six views PASS.**
- **The column close up.** It reads as weathered concrete, with run-off and lime drips from the arm and a grimy foot; the grey-timber grain is gone. The middle 2.4 m are plain.
- **From the road.** Run-off from the joint fades down, with pale runs under it; nothing else changed against the stain-off picture.
- **From across.** It reads as weathered; the bowl's drift is warmer as well as lighter, noted for its investigation.
- **Hook by day.** All four columns read as darkened, weathered concrete with grime from the arm.
- **Reverse by day.** The near column has soft run-off below the arm; the far ones are faint, acceptable at their size.
- **From the road at night.** Nothing glows or bands. The known yellow bar under its own light is now more two-tone, because the run-off darkens the shaft above it.
- **Points to watch:** the lime streaks look crisp, close to painted drips, when enlarged 3 to 5 times; at each view's distance they read as lime.
- **The last good pictures** are now these (F:/LedgerTools/gate/last-good/lamp-post-C). Preview: production/previews/lamp-staining-2026-10-22.jpg (before left, after right).
- **Not done:** the chipped arris (one column's only).
