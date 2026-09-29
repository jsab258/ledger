# Skinning loose trousers for sitting, walking and stairs (research note, 29 September 2026)

The clothing session asked for this after two blind reviewers failed the heavy man's posed work trousers on the same four faults: the waist falling away when he sits, the body showing through the seat on the stair, the hems pinching, and the belt folding like a concertina. A separate helper did the research in about thirty minutes and read every source on 29 September 2026. D marks something documented, with its source; I marks the helper's own inference. "Search summary" means the helper saw only a search engine's summary, not the page itself.

## In short

- **Recipe (I).** Stop copying each point's weights from the nearest point of the body. Give the trousers zone weights on the main bones only:
  - **Belt, band, loops and top 3 cm:** one stiff ring on the pelvis, with spine_01 at the back.
  - **Seat and front rise:** blend from the pelvis into the thigh on the same side.
  - **Knee:** blend from thigh to calf over about 15 cm.
  - **From 10 cm below the knee to the hem:** the calf only, the same all the way round each ring.
  - **Corrective joints:** fold them into their parent bones.
  - **In the test:** hide the body under the trousers, as the game does.
- **Our weights reach the game only if the builder keeps them (D/I).** Epic's documented route copies the weights from the body again [E1]. The resizing graph has its own switch that transfers them again [E9]. To keep ours, the builder needs Epic's skeletal-mesh cloth template and that switch turned off.
- **If Unreal must transfer the weights,** use Inpaint Weights with a mask over the crotch, seat and lower legs. Epic says it beats nearest-point copying "for almost every use case" [E4] (D).
- **Body through the seat:** the outfit's Body Hidden Face Map removes the body faces the clothing always covers [E3] (D). Our test must do the same, or it judges the body, not the cloth (I).
- **Our test is not yet fair (D/I).** The MetaHuman body's corrective joints move in Unreal but stay still in Blender [M1][M2][L1].
- **The belt** is a stiff ring, with the same weights across its width. Stiff pieces sit on one bone [B1] (D).
- **Lap and knee creases** cannot come from skinning alone [K1] (D). Use wrinkle normal maps driven by the thigh or knee angle through the Pose Driver [E8] (D/I). Model only the permanent wear (I).
- **No Epic advice was found specifically for trousers or for seated characters.**

## A. How artists weight loose trousers

- **Hip and seat when sitting (D [K1]).** Kiel Figgins:
  - Spreading leg weight into the pelvis "looks better when walking, but had severe volume loss during squats or sitting".
  - Moving it towards the pelvis instead gives "harsher lines".
  - He adds a crotch joint to "any rig that's not skin tight".
  - Knees and hips eventually need "a corrective blend shape or additional helper joints" [K2].
- **Stiff accessories (D [B1]).** A pouch is weighted "100% to the upper leg bone only"; points in one group "will never deform".
- **Nearest-point copying** "has well-known issues when it comes to handling non-skin-tight clothing" [E4] (D).
- **Robust transfer (D [P1][P2][E4]).** Abdrashitov and others, at Epic, SIGGRAPH Asia 2023.
  - It copies weights only where the body point is near and faces the same way, and fills in the rest smoothly.
  - The reference code (MIT) uses a distance of 5% of the bounding-box diagonal, an angle of 30 degrees, and then 10 smoothing steps at 0.2. It needs libigl.
  - Unreal's Inpaint Weights is the same method, and Epic advises masking "armpit or crotch areas or any creases".
  - A search summary says the paper fixes the crotch and lower legs.
  - A Blender add-on exists (GPL-3.0; its libraries must be pip-installed) [P3], with a fork for Blender 5.2 [P4].
- **Proportions (I).**
  - **Waistband:** pelvis, with spine_01 at the back only.
  - **Seat:** falls from pelvis to thigh down to about 10 cm below the crotch.
  - **Knee:** a wide blend.
  - **Hem:** follows the calf, never the foot or ankle. When the mix varies round the ring, the hem pinches (fault 3).
  - **Helper joints:** we cannot add any, because MetaHuman's skeleton is fixed.

## B. What MetaHuman's clothing tools do with a garment's weights

- **Epic's documented route (D [E1]).** The garment is imported as a static mesh, not a skeletal one, because of "issues with visualization in the Dataflow Editor". TransferSkinWeights then copies from the body by Closest Point on Surface. Painted maps can Relax, Prune, Hammer, Clamp or Normalize; Epic warns of "tearing in areas like armpits and upper thigh regions".
- **The skeletal-mesh cloth template keeps the garment's own weights.** It uses SkeletalMeshImport and has no transfer node (D, our note cloth-weight-maps-2026-09-29). Weight editing inside the graph is experimental in 5.6 [E6] (D).
- **The resizing graph (D [E9], read from the installed 5.8 file).**
  - It has the variables TransferSkinWeights and StripSimMesh.
  - It has branches that transfer the render and simulation weights again (both methods, with an inpaint mask).
  - It has "corrective" sub-graphs that correct the weights.
  - The switch's default could not be read, so that is unproven. With it on, the weights come from the target body (I).
  - Epic's 5 August 2026 answer names only Strip Sim Mesh false [E11].
- **Users confirm it (D [E10]).** Wardrobe items "reset to the character's bones" (August 2025), and the complaint is still being made in 2026. One workaround in 5.8 (15 September 2026) copies the weights back from the original mesh after assembly.
- **Simulation (D [E5]).** It works for one size only, and Epic advises render meshes only for now. Resizing uses 1500 RBF points, with 1000 to 2500 advised [E2].
- **Morph targets on the garment.** Surviving the outfit route is undocumented, so do not rely on them (I).

## C. A fair Blender test, and the cheapest recipe (Blender 4.5, Python)

**Fairness first:**

- **Corrective joints.** The heavy build carries thigh_fwd, thigh_bck, thigh_in and thigh_out, their _lwr joints, calf_knee, calf_kneeBack, ankle_fwd and ankle_bck, and the twistCor and correctiveRoot joints [L1] (D). RBF solvers move them in Unreal [M1][M2] (D). After the transfer, add each one's weights to its parent and delete it (I).
- **Skinning method.** Keep the Armature modifier's Preserve Volume off: that is plain blend skinning [B3] (D), as in Unreal (I). Use no Corrective Smooth modifier, because the game has no such step (I).
- **Hide the covered body.** Mask the body faces lying about 3 cm or less inside the trousers (I).

**The recipe (I): numpy writes to vertex groups, then `vertex_group_normalize_all`.**

1. **The waistband stays closed when he sits.**
   - Band, belt, loops and top 3 cm: pelvis 1.0 at the front and sides. At centre back, pelvis 0.6 and spine_01 0.4, fading to pelvis only at the side seams. No thigh weight.
   - At the front below the band, the thigh share rises from 0 at 3 cm to about 0.7 at 12 cm. The lap then folds under the belt, not through it. The earlier stiff try lacked this graded zone.
   - Seat: pelvis about 0.7 at the top, 0.5 at the widest point, 0.2 at the fold under the buttock, 0 below.
2. **The hems stay open when the knee bends.**
   - From 10 cm below the knee joint down: calf 1.0, identical round each ring, with no foot, ball or ankle weights.
   - Across the knee: blend thigh to calf over 15 cm.
   - Drop the twelve smoothing passes over the whole mesh, which carry foot weight upwards.
3. **No body through the seat.**
   - Keep 1.5 to 3 cm of room at the seat, bridging the cleft.
   - At the centre seam, fade each side's thigh into the pelvis over 6 to 8 cm (today it is a 2.4 cm strip).
   - Hide the covered body.
4. **The belt stays a smooth band.**
   - Ring weights by angle, identical across the width, on at most two bones.
   - Smooth along the length only, and keep it 4 to 5 mm off the band.
- **Only if the zones fall short:** inpainting in numpy alone is cheap (hold the matched points and average the rest) and needs no installing (I).

## D. Heavy worn twill, not clean slacks

- **Model the big folds, bake the small ones.** Games model the large folds into the mesh and bake the medium and small ones into normal maps (search summary). ML Cloth suits "tight-fitting clothing like pants" (search summary), but each garment needs its own training [W2] (D). That is too costly for us (I).
- **Folds that come and go.** Blending wrinkle maps by bone rotation is an established method [W1] (search summary). Pose Driver can "Drive Curves" from a bone [E8] (D). One map behind the knee and one in the lap would give the reviewers' creases (I).
- **Model only the permanent wear (I):**
  - a forward knee bag of 1 to 2 cm;
  - a seat that hangs and does not follow the cleft (drape against a copy of the body with the cleft filled);
  - one break over the boot;
  - 5 to 8 gathers, 3 to 6 mm deep, under the belt.

  Creases that belong only to sitting would show when he stands.

## Sources (all read 29 September 2026)

- [E1] Epic, "Building with an FBX Export", MetaHuman docs, undated. dev.epicgames.com/documentation/metahuman/building-a-metahuman-parametric-outfit-with-an-fbx-export
- [E2] Epic, "Create an Outfit Asset", undated. …/metahuman/create-a-metahuman-parametric-outfit-asset
- [E3] Epic, "Testing and Configuring your Parametric Outfit Asset", undated. …/metahuman/testing-and-configuring-your-parametric-outfit-asset
- [E4] T. Brakensiek (Epic), "Panel Cloth Transfer Skin Weights Node", 6 Sep 2023, updated 2 Mar 2026. dev.epicgames.com/community/learning/tutorials/Dl20
- [E5] T. Brakensiek, "Chaos Cloth Outfit Asset Resizing Addendum", 19 Aug 2025. …/tutorials/9Xjd
- [E6] Epic, "Chaos Cloth – Updates 5.6", 14 Jun 2025, updated 2 Oct 2025. …/tutorials/LZZo
- [E8] Epic, "Pose Driver in Unreal Engine", UE 5.8 docs, undated. …/unreal-engine/pose-driver-in-unreal-engine
- [E9] Installed UE 5.8: Engine/Plugins/ChaosOutfitAsset/Content/ResizeOutfitTemplate.uasset (names read from the file).
- [E10] Forum, "Skin Weights In MetaHuman Wardrobe Item Is Not Same From Skeletal Mesh", 6 Aug 2025 to 15 Sep 2026. forums.unrealengine.com/t/…/2631722
- [E11] Forum, Epic answer (E. Carmichael), 5 Aug 2026. forums.unrealengine.com/t/…/2762838
- [P1] Abdrashitov, Raichstat, Monsen, Hill, "Robust Skin Weights Transfer via Weight Inpainting", SIGGRAPH Asia 2023. The project page was read; the PDF would not parse; the pants detail is from a search summary. dgp.toronto.edu/~rinat/projects/RobustSkinWeightsTransfer
- [P2] rin-23/RobustSkinWeightsTransferCode, MIT, undated; source read.
- [P3] sentfromspacevr/robust-weight-transfer, GPL-3.0, undated.
- [P4] protoco-jp/robust-weight-transfer, undated; search result only.
- [K1] K. Figgins, "Corrective Joint Rigging Setups", undated (cites a February 2020 post). 3dfiggins.com/writeups/corrective
- [K2] K. Figgins, "Painting Weights and Skinning", undated. 3dfiggins.com/writeups/paintingWeights
- [B1] Blender Artists, "Rigging belts and pouches to a character", 23 Sep 2015.
- [B3] Blender manual, Armature modifier, "Preserve Volume" (bundled copy on F:), undated.
- [M1] mGear forum, "Metahuman issue with thigh correctives", 29 to 31 Jan 2025.
- [M2] CG Channel, "MetaHuman DNA add-on for Blender gets new RBF Editor", 31 Mar 2026.
- [L1] Our file F:\LedgerTools\bodies\MH_BuildHeavy\MH_BuildHeavy_Body.fbx, its joint names.
- [W1] L. McEwen, "Dynamic Wrinkle Maps in UE4", ArtStation, undated; search summary only.
- [W2] 80.lv, "Leveraging Unreal Engine's ML Deformer to Create Realistic Clothing", 3 May 2024.
