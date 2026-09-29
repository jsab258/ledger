# A donkey jacket from an open sewing pattern (29 September 2026)

The problem, as given: a 1990 donkey jacket (production/reference/donkey-jacket-1990.md) for a heavy-set man, about 6 ft 1 in with a big belly, on a MetaHuman body. It should be made the way the flat cap was: a FreeSewing pattern, flat panels in Blender, sewn and draped by Blender's cloth, then an Unreal 5.8 Chaos Cloth asset. The cap came out lumpy. The jacket made from a shell of the body's skin failed three blind reviews.

Research was capped at about 30 minutes. Web sources were read on 29 September 2026. Local checks were run the same day in a scratch folder; no project file was changed. **D** means documented, with the source given. **I** means my inference.

## In short

- **Pattern.** No FreeSewing design is a workman's jacket. The closest start is the **Brian** block, for the body and sleeve: its side seams hang dead straight. Add **Simon**'s pointed collar and collar stand. FreeSewing's own options set the length, the ease and the straight sides. The front overlap, the yoke, the pockets and the joined collar have to be cut after drafting, in our own Python step. **Jaeger** (a sport coat with lapels) is the worst fit, not the best.
- **Why the cap was lumpy (probable cause, found today).** Blender takes the cloth's first frame as its rest shape. `sew_cap.py` starts each piece already bent round the head, and that bending stretched or squeezed the crown's edges to between 0.56 and 1.59 times the pattern's lengths. The crown then "wanted" to keep that uneven shape. The fix is to keep the flat pattern as the rest shape through a **Rest Shape Key**. That setting is broken in Blender 4.5 unless a pass-through geometry-nodes modifier sits before the cloth. I tested this on this PC: it works with the workaround.
- **Unreal.** 5.8 can take the flat pattern from the simulation mesh's UVs and use the pattern's lengths as the cloth's rest lengths. It can also keep the drape's folds, such as the collar's roll, as the rest angles.

## 1. Which FreeSewing design

**Version.** FreeSewing 4.10 is current. The 1 July 2026 newsletter covers 4.8 to 4.10, and its five new designs include no jacket [F3] (D). npm 4.10.2, the version the project already uses, was installed in a scratch folder. Every candidate was drafted there at FreeSewing's male size 48 (chest 1263 mm) and at a bellied variant (waist 108% of chest, hips 105%). All drafted with no errors [F5] (D).

**The catalogue has no workwear or chore coat.** Its jackets and coats are Carlita, Carlton, Devon, Jaeger and Jett [F1] (D).

| Design | What it is | Parts | How it fits a donkey jacket |
|---|---|---|---|
| **Brian** | Basic menswear block | 3: back, front, sleeve | **Best body.** Checked in the draft: with chestEase 20% and lengthBonus 30%, the side seam sits at the same width (379 mm, a quarter of the girth) at the armhole, waist, hips and hem. That is a straight box, and the waist is ignored. Back length from the back of the neck is 889 mm, inside the reference's 81 to 90 cm [F5] (D). Options include chestEase (up to 35%), lengthBonus (up to 60%), shoulderEase, bicepsEase and cuffEase [F5] (D). The one-piece sleeve is fitted to the armhole (libraryFitSleeve), and the shared sleeve's cap ease defaults to 0 [F5] (D). |
| **Bent** | Brian with a two-part sleeve | 4: back, front, top and under sleeve | The same box with a sleeve bent at the elbow. Use it if a straight sleeve kinks at the elbow in the sim (I). |
| **Simon** | Button-down shirt, built on Brian | 12 | **Best collar.** It has a collar and a collar stand with collarAngle (60 to 130°), collarWidth (90 to 200%), collarRoll and collarStandCurve. It also has a back yoke (yokeHeight 40 to 90%, splitYoke), 4 to 12 buttons, a straight hem style and lengthBonus up to 60% [F5] (D). **But** its side seam follows the waist and hips. On the bellied draft it widens from 379 mm at the armhole to 398 mm at the hip [F5] (D), which is the bell hem the third reviewer failed (I). |
| **Devon** | Denim trucker jacket, built on Bent | 16 | It has a back yoke and a front yoke (yokeDrop 17 to 50%), a pointed upper and under collar, a waistband, split front panels, flap pockets, and lengthBonus up to 40% [F5] (D). The details are near, but the waistband and panel seams would all have to be merged away (I). |
| **Jaeger** | Sport coat | 17 | Lapels and a notch, chest darts or shaping, a side panel, and a cut-away rounded front (frontCutawayAngle at least 1°, hemRadius at least 35%). lengthBonus goes only up to 25% [F2] (D). No option removes the lapels. The neckline would have to be redrawn (I). |
| **Carlton** | Long double-breasted coat, built on Bent | 20 | It has a belt, tails and flaps. Far more to remove than to keep (I). |
| **Sven / Hugo / Jett** | Sweater / raglan hoodie / bomber | 5 / 10 / 12 | Sven is Brian plus ribbing. Hugo has raglan sleeves, which is the wrong sleeve. Jett has ribbing and a lining [F1][F5] (D). None is closer than Brian (I). |

**What FreeSewing's own options can do (D, [F5]):** the length, the chest ease (enough that the box clears his belly), a straight hanging body (Brian ignores the waist), sleeve ease, and the collar's angle, width and roll (Simon).

**What must be cut after drafting, in a small Python step on the drafted JSON (I):**

1. **Front opening.** Brian's front is half a piece, cut on the fold at centre front. Split it there and add a 4 cm overlap, so the jacket buttons left over right.
2. **Yoke.** Cut the front about 12 cm below the neck and shoulder, and the back about 30 cm below the collar seam (the reference). Then join the front and back yoke pieces along the shoulder seam into one panel, as on the real jacket, so the stiff PVC has no seam over the shoulder.
3. **Collar.** Take Simon's collar and collar stand and scale their length to Brian's neckline. Simon sizes its stand to its own neckline: the stand's length comes from `measurements.neck × (1 + collarEase)`, checked against Simon's own neck seam [F5] (D). Then either join the stand and collar into one piece or keep the two, and lengthen the points.
4. **Patch pockets.** Two rectangles, 18 to 20 cm tall, about 8 cm above the hem. They are for the render mesh only, not the simulation.
5. **Drop** Simon's cuffs and plackets.

`freesewing_draft.mjs` passes measurements only. It needs an options argument, which is a small change (I). Brian needs these measurements: biceps, chest, hpsToBust, hpsToWaistBack, neck, shoulderToShoulder, shoulderSlope, waistToArmpit and waistToHips [F5] (D). They should be measured on Ron's exported body (I).

## 2. Sewing multi-panel garments smoothly in Blender

**What Blender uses as the rest shape.** "Normally cloth uses the state of the object in the first frame to compute the natural rest shape of the cloth." The **Rest Shape Key** option exists "to start the simulation with the cloth in a pre-draped state without applying that shape as a plastic deformation" [B1] (D).

**Our cap.** The cap's pieces started already wrapped round the head. I measured each starting edge against the same edge on the flat pattern [L2] (D):

| Piece | Smallest | 5% | Median | 95% | Largest |
|---|---|---|---|---|---|
| Crown | 0.56 | 0.81 | 1.01 | 1.13 | 1.59 |
| Band | 0.39 | 0.98 | 1.00 | 1.07 | 1.18 |
| Brim | 0.78 | 0.94 | 0.99 | 1.03 | 1.17 |

So the crown's rest shape was not the pattern. This probably explains both the lumps and the crown standing up instead of lying forward (flat-cap-2026-09-25/README.md) (I).

**The Rest Shape Key bug and its workaround.** Bug #115321 was opened on 24 November 2023: the rest shape key is ignored from Blender 3.6 on. It is still open and marked confirmed. A comment of 24 March 2026 says a pass-through geometry-nodes modifier placed before the cloth makes it work again [B5] (D). **Tested on this PC in Blender 4.5.13 LTS** [L1] (D). A sheet starts stretched to 1.5 times its pattern width and runs 40 frames with no gravity:

| Rest shape key | Pass-through modifier | Width after 40 frames |
|---|---|---|
| Off | Off or on | 1.500 |
| On | Off | 1.500 |
| On | On | **1.000** |

So only the key plus the modifier brings the sheet back to its pattern size (D).

**Placing the pieces round the body before sewing.**
- Garment Tool bends sleeve patterns so they "wrap around the character arms" [B6] (D).
- Marvelous Designer places pieces on "arrangement points" on a bounding volume round the body [M2] (D, from a search summary; the page itself is behind a bot check).
- With the flat pattern held as the rest shape key, the placement may distort freely (I). Put the body pieces on an elliptical cylinder a few centimetres out from the torso, each sleeve on a cylinder along its arm in the body's rest pose, and the collar standing round the neck.

**Ramping, sewing force and gravity.**
- Do not leave Max Sewing Force at zero, because that causes "extreme forces in the initial frames" [B1] (D).
- Of shrinking: "it is advisable to keyframe these fields and ease in from 0 during draping" [B4] (D).
- Garment Tool's "Initialize Simulation" raises gravity from 0 to 9.8 over the start-up time and warms up the sewing force and shrinking with it [B6][B7] (D). The cap already sews weightless first (sew_cap.py).

**Settings.**
- Garment Tool: quality steps above 15, and a collision distance of about 2 mm, on the cloth and on the body [B6] (D).
- Blender's manual says a larger collision distance "tends to make it look like the cloth is resting on air, and gives it a very rounded look" [B3] (D). That is the reviewers' "padded" and "pillowy" look (I).
- Turn self-collision on for close-ups [B3] (D). Keep its distance small: Garment Tool's FAQ blames self-collision distance for gaps along seams [B8] (D).
- Pressure is for balloon-like shells, and internal springs make cloth behave like a soft body [B2] (D). Both stay off for a jacket (I).
- Stiff areas: the cap already uses per-area stiffness groups (vertex_group_bending with bending_stiffness_max) for the brim. All of these properties exist in 4.5.13: rest_shape_key, shrink_min/max, vertex_group_shrink, sewing_force_max, vertex_group_bending, vertex_group_structural_stiffness, use_pressure, use_internal_springs [L1] (D).

**Mesh density.**
- Marvelous Designer: 20 mm particle distance while draping, under 5 mm for final quality [M1] (D, from a search summary; the page is behind a bot check).
- KatsBits: "The denser a mesh, the more accurate cloth simulation will be" [B9] (D).
- For us: drape at about 10 mm, as the cap did. Build the coarser game mesh afterwards (section 3) (I).

**Seams.**
- Keep equal point counts on both sides of each seam, as sew_cap.py does.
- Keep the sleeve cap at zero ease. FreeSewing's shared sleeve defaults to 0 [F5] (D). Any extra cap length is gathered into puckers when sewn point to point (I).

**Usual causes of lumps and puckers, in order of likelihood here (I, except where marked):**

1. The rest shape taken from a distorted starting layout (measured above).
2. Too large a collision distance: a rounded, air-cushioned look [B3] (D).
3. Sudden forces from the sewing, shrinking or gravity at the start [B1][B4] (D).
4. Seam lengths that do not match, or cap ease.
5. Too coarse a mesh for the folds wanted, or uneven triangles.
6. Too few quality steps, so the cloth passes through the body [B3][B6] (D).
7. Pressure or internal springs left on.
8. Heavy smoothing or subdivision after the drape, which rounds what the simulation made sharp.

## 3. Making the sewn result game-ready (Unreal 5.8 Chaos Cloth)

**Epic's definitions.** Epic defines a sim mesh as "a simplified, single-sided mesh … It may also be a lower resolution than your render mesh". The render mesh "can have thickness" (page updated 2 September 2026) [U1] (D).

**What the engine's own 5.8 source shows** (read 29 September 2026) [U2] (D):
- **StaticMeshImport** has `UVChannel`: "UV channel of the static mesh to import the 2D simulation mesh patterns from". The value -1 unwraps the 3D mesh instead. It also has `UVScale`.
- **SimulationStretchConfig** has `bStretchUse3dRestLengths`, on by default: "Whether to use the 3D draped space as rest lengths, or use the 2D pattern space instead."
- **SimulationBendingConfig** has `RestAngleType`:
  - `Use3DRestAngles` bakes "any creases and folds" into the simulation.
  - `FlatnessRatio` can be varied by a weight map.
  - `RestAngle` sets the angle directly.
- **ProxyDeformer** drives render vertices from sim triangles. It can be limited by selection sets and can take several influences.
- The earlier note records that the static-mesh import builds sim vertices per UV island and welds the seams (character-pipeline/cloth-weight-maps-2026-09-29.md) (D).

**So (I):**
- Write the sim mesh's UV0 as the flat pattern at true size, with a UV seam along every sewn seam. Unreal then gets both the pattern and the welded garment.
- Try the pattern's rest lengths (`bStretchUse3dRestLengths` off), so no strain left over from the drape is baked in.
- Keep 3D rest angles, so the collar's roll and the drape's shape hold.
- Build the sim mesh as a coarse re-mesh of the flat pieces, triangles about 2 to 3 cm (the size drape_jacket.py chose). Find each coarse vertex's pattern position inside the fine draped mesh's pattern and take its draped position from there. Both meshes come from one pattern, so this needs no projection guesswork.
- Build the render mesh from the fine drape: subdivided once, a 3 mm Solidify, and the yoke as its own material. Pockets, buttons and the collar's thickness are separate render-only pieces.
- Export both as static FBX in the body's reference pose, which make_cloth_jacket.py already does.
- Keep the maximum-distance gradient from cloth-weight-maps-2026-09-29.md.

## 4. Estimate and risks (I)

**Steps and working time.** This is my estimate, set against the cap's measured 70 minutes for one simple piece.

| Step | Hours |
|---|---|
| Draft Brian and Simon with options | 1 |
| The alteration step (front split, yoke, collar, pockets) | 3 to 4 |
| Placement round Ron's body | 2 to 3 |
| Sewing and drape runs, tuned | 3 to 5 |
| Sim and render meshes | 2 |
| Unreal asset and films | 1 to 2 |
| **Total** | **About 12 to 17 hours, over two or three days** |

This sits inside the earlier planning figure of 20 to 40 hours for a first jacket (character-pipeline/RESEARCH-2026-09-25.md).

**Main risks:**
1. The sleeves in the A-pose: the underarm fold and the sleeve seam are the classic places for puckers.
2. The belly: a straight box must clear the belly without the front flaring into a bell. Check the hem's width against the chest's in the drape, before Unreal.
3. The rest-key workaround depends on a Blender bug staying the same. Pin Blender 4.5.13 and re-run the 40-frame test after any upgrade.
4. The collar's fold.
5. Unreal's pattern rest lengths are untried here.
6. Welding the overlapping fronts.

**What a stiff wool collar needs that the cap did not:**
- A fold that holds. In Blender:
  - Make the collar its own piece with high bending stiffness (a vertex group, as the brim had).
  - Give it a *folded* rest shape. The rest shape key is per vertex, so the collar's vertices can hold the folded shape while the body pieces hold the flat one.
  - Or keep the stand and the fall as two pieces sewn along the roll line, with the fall laid folded down at the start.
- Marvelous Designer does the same with a fold angle and fold strength on an internal line [M3] (D, from a search summary).
- In Unreal: Use3DRestAngles keeps the fold [U2] (D). A maximum distance near 0 on the collar and stand keeps it from flapping.
- Fixing the collar to the upper-back bone as a solid piece (done on 29 September) stays as the fallback.

**What a leather or PVC yoke needs:**
- Make it part of the same single cloth layer, with higher stretch and bending stiffness in its area. A second simulated layer over the wool tore and blotched in the 29 September rounds (donkey-jacket-2026-09-29/README.md) (D).
- The yoke differs only in the render mesh: its own glossy material, and a small raised step at its lower edge.
- Cut flat and seamless over the shoulders, it should lie flat without crumpling, because its rest shape is now flat and its rest lengths are the pattern's (I).

**Fronts:** sew the two fronts together along the button line into one layer in the simulation. The render mesh shows the overlap edge and the buttons.

## The most promising route, step by step

1. **Draft.** Draft Brian (Bent if the elbow kinks) at Ron's measurements, taken from his exported body:
   - chestEase so the box's girth is at least his belly plus about 10 cm (the jacket goes over a jumper);
   - lengthBonus for a back length of 85 to 88 cm;
   - bicepsEase about 25% and cuffEase about 60%, for a fairly slim straight sleeve.

   Draft Simon for the collar only, with a wider collarAngle and collarWidth for long points. Add an options argument to freesewing_draft.mjs.
2. **Alter.** A Python step on the JSON:
   - split the front and add a 4 cm overlap;
   - cut the yoke lines (12 cm front, 30 cm back) and join the front and back yokes into one panel across the shoulder;
   - scale the collar to Brian's neckline;
   - make the pocket rectangles, render only;
   - check that every seam's two sides match in length.
3. **Panels.** Mesh each flat piece at about 10 mm, as sew_cap.py does. Store the flat layout twice: as UVs at true size, and as a shape key called "flat".
4. **Place.** Place the pieces round Ron's exported body in its reference pose: the body pieces on an elliptical cylinder 3 to 4 cm out, the sleeves on cylinders along each arm, the collar round the neck. The basis is the placed shape.
5. **Cloth setup.**
   - Set the rest shape key to "flat", with a pass-through geometry-nodes modifier before the cloth.
   - Quality 15 to 20, a collision distance of 2 mm on the cloth and the body, self-collision on at 2 to 3 mm.
   - Pressure and internal springs off.
   - Stiffness groups: melton, a stiffer yoke, a very stiff collar with its own folded rest.
6. **Sew, then drape.** Sew weightless for about 40 frames with the sewing force ramped in, then ramp gravity up. Measure:
   - the seam gaps;
   - the strain against the pattern (each edge within 3% of the pattern's length);
   - the clearance from the body;
   - the hem's width against the chest's, so there is no bell;
   - the front and side outlines, against the reference.
7. **Game pair.**
   - The sim mesh is the pieces re-meshed at 2 to 3 cm and placed on the drape through the shared pattern layout.
   - The render mesh is the fine drape, subdivided, with a 3 mm Solidify, plus the yoke material, pockets, buttons and collar thickness.
   - Export both as static FBX in the reference pose.
8. **Unreal.** Run make_cloth_jacket.py with StaticMeshImport UVChannel 0 and a UVScale to centimetres. Try the stretch at 2D rest lengths, keep the bending at 3D rest angles, and add the maximum-distance gradient. Film walking, reaching and sitting.
9. **Gate.** My own comparison against the references, then a fresh blind reviewer, before anything reaches Jafar.

## Sources (all read 29 September 2026)

**FreeSewing**
- [F1] FreeSewing designs catalogue: https://freesewing.eu/designs/
- [F2] Jaeger design options: https://freesewing.eu/docs/designs/jaeger/options/
- [F3] FreeSewing newsletter, 2026 Summer edition (dated 1 July 2026): https://freesewing.eu/newsletter/2026q3/
- [F4] FreeSewing v4 announcement: https://freesewing.eu/blog/announcing-v4 (search result only)
- [F5] The FreeSewing packages themselves, 4.10.2 from npm (MIT): @freesewing/brian, bent, simon, jaeger, carlton, devon, sven, hugo, jett, library and models. Their source files were read, and each was drafted at size 48 and a bellied variant, in a scratch folder (not the project): https://www.npmjs.com/package/@freesewing/brian

**Blender**
- [B1] Blender 5.2 LTS Manual, Cloth, Shape (Sewing, Max Sewing Force, Shrinking, Dynamic Mesh, Rest Shape Key): https://docs.blender.org/manual/en/latest/physics/cloth/settings/shape.html
- [B2] Blender 5.2 LTS Manual, Cloth, Physical Properties (bending models, internal springs, pressure): https://docs.blender.org/manual/en/latest/physics/cloth/settings/physical_properties.html
- [B3] Blender 5.2 LTS Manual, Cloth, Collisions (quality, distance, troubleshooting): https://docs.blender.org/manual/en/latest/physics/cloth/settings/collisions.html
- [B4] Blender 2.79 Manual, Cloth Settings (shrink: ease in from 0): https://docs.blender.org/manual/en/2.79/physics/cloth/settings/cloth_settings.html
- [B5] Blender issue #115321, "Rest Shape Key does not function / Dynamic Mesh always on" (opened 24 November 2023, open and confirmed; workaround comment 24 March 2026): https://projects.blender.org/blender/blender/issues/115321, read through the API at https://projects.blender.org/api/v1/repos/blender/blender/issues/115321
- [B6] Garment Tool docs, Quick Start (undated; version 2.x, for Blender 3.6 and 4.x): https://joseconseco.github.io/GarmentToolDocs/quick_guide/
- [B7] Garment Tool docs, Main Panel (warm-up of the sewing force and shrinking): https://joseconseco.github.io/GarmentToolDocs/garment_panel/
- [B8] Garment Tool docs, FAQ (seam gaps and self-collision distance): https://joseconseco.github.io/GarmentToolDocs/faq/
- [B9] KatsBits, "Toolkit: Clothing using Cloth Simulation" (undated): https://www.katsbits.com/codex/toolkit-cloth-simulation/

**Marvelous Designer** (behind a bot check, so the pages were not opened; these are search-result summaries)
- [M1] Particle Distance Setting: https://support.marvelousdesigner.com/hc/en-us/articles/47358268602777-Particle-Distance-Setting
- [M2] Arrange Pattern with Arrangement Points: https://support.marvelousdesigner.com/hc/en-us/articles/47358262924185-Arrange-Pattern-with-Arrangement-Points-Flip-Wrap-Direction
- [M3] Fold Arrangement: https://support.marvelousdesigner.com/hc/en-us/articles/47358260153881-Fold-Arrangement

**Unreal**
- [U1] Epic, "Getting Started for creating Parametric Clothing in MetaHuman" (updated 2 September 2026): https://dev.epicgames.com/documentation/en-us/metahuman/getting-started-for-creating-parametric-clothing-in-metahuman
- [U2] The installed UE 5.8 source, `Engine/Plugins/ChaosClothAssetDataflowNodes/Source/ChaosClothAssetDataflowNodes/Public/ChaosClothAsset/`: StaticMeshImportNode.h, SimulationStretchConfigNode.h, SimulationBendingConfigNode.h and ProxyDeformerNode.h.

**Local tests** (29 September 2026, in the scratch folder, not kept)
- [L1] Rest-shape-key test and a list of the cloth properties, Blender 4.5.13 LTS (C:\LedgerTools\blender\4.5.13).
- [L2] The cap's starting edge lengths against the pattern: sew_cap.py's own panel and placement code, up to the point where the pieces are built, run on F:\LedgerTools\freesewing\florent-570.json.

**Not used:** GarmentCode (MIT, last updated 3 June 2025, https://github.com/maria-korosteleva/GarmentCode) makes parametric patterns and simulates them with NVIDIA Warp. Whether that runs on this AMD card was not checked. It is noted only as a possible later source of patterns.
