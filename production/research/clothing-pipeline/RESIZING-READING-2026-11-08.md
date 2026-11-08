# Epic's resizable MetaHuman outfit: first-pass reading (item n09-6, read 8 November 2026)

First-pass reading only. No synthesis, recommendation or decision. All pages read 8 Nov 2026 (the day this file was written). "Unverified" marks anything not confirmed from a page read in full. The helper had no shell, so the Swiss clock could not be read; the 00:25 deadline was not checked.

## Already known at home (not repeated in detail)

- production/research/clothing-pipeline/DEEP-DIVE-2026-11-01.md: the Outfit Asset route (lines 17 to 23, 52, 76 to 77): two kinds of MetaHuman clothing, 1,500 interpolation points, weights re-transferred at every build, refit comparison "untried".
- production/research/wardrobe-at-scale/3-METAHUMAN-AND-FAB.md and SUMMARY.md: Fab listings (from search summaries only), Epic's known 5.8 faults, Collections Experimental.
- New below: the cook/runtime answer from the engine source, the Epic docs read in full (build pages, source bodies, testing, packaging), and the Epic Fab listing.

## 1. What the resizable outfit is

- Asset type: the Chaos Outfit Asset (class UChaosOutfitAsset), made from the "Resizable Outfit" Dataflow template. Source: Epic's page https://dev.epicgames.com/documentation/metahuman/create-a-metahuman-parametric-outfit-asset (read 8 Nov). Engine source: MetaHumanOutfitEditorPipeline.cpp line 41, C:\Program Files\Epic Games\UE_5.8\Engine\Plugins\MetaHuman\MetaHumanCharacter\Source\MetaHumanDefaultEditorPipeline\Private\Item\ (read 8 Nov).
- Epic's name for the feature: "Parametric Clothing", from 5.6 with the "Parametric Body System", "continuously adjustable MetaHumans". https://dev.epicgames.com/documentation/metahuman/creating-parametric-clothing-for-metahuman (read 8 Nov). Fab calls it "Outfit Clothing", resizable to "certain MetaHuman body shapes" (as quoted in wardrobe-at-scale/3-METAHUMAN-AND-FAB.md; the Fab page itself not re-read).
- What resizing fits: the body of any MetaHuman Character from Creator, using the body measurements. The outfit holds one or more "sized sources", each a cloth asset paired with the body it was made on. The code picks the closest body size (FindClosestBodySize, line 120) and fits the garment to the character's merged head and body (lines 63 to 72). Epic's testing page: "You will see it resize automatically"; sliders and presets in Head & Body change the fit. https://dev.epicgames.com/documentation/metahuman/testing-and-configuring-your-parametric-outfit-asset (read 8 Nov).
- Height versus body shape: the pages read do not say separately. The compatibility-body advice reads "all bodies of a single height (ideally the middle height)" (source-bodies page, below). Whether height is fitted as well as shape: unverified.
- 5.6 release posting of the Techwear Outfit: https://forums.unrealengine.com/t/metahuman-5-6-release/2539165 (read 8 Nov).

## 2. How an outside garment becomes one

Pages read in full 8 Nov: https://dev.epicgames.com/documentation/metahuman/building-an-outfit-asset-in-unreal-engine (overview only), .../building-a-metahuman-parametric-outfit-with-an-fbx-export, .../with-a-usd-export, .../with-a-render-mesh, .../create-a-metahuman-parametric-outfit-asset, .../creating-your-metahuman-characters. Two pages ("parametric-asset-setup", "getting-started-with-parametric-clothing") returned only a table-of-contents heading: not read.

Required inputs:
- A source body: a MetaHuman Character made in Creator, exported with Geometry Export, "Full Body Skeletal Mesh", named ending `_CombinedSkelMesh`. Epic: "create at least 2 source bodies (masculine, feminine)"; "the more source bodies, the higher the quality". Armpits and thigh gap need clearance; clipping "is likely to cause some issues with resizing". Skeleton copied once into the working folder, shared by all bodies; no link to a skeleton outside the folder.
- Compatibility mode: Project Settings > MetaHuman Character > "Show Compatibility Mode Bodies" gives the 18 fixed bodies of the old Creator; Epic recommends "no more than 6, all bodies of a single height (ideally the middle height)", or 4.
- The garment: FBX (Epic's example from Maya, render mesh only, imported as a static mesh), or USD from Marvelous Designer or CLO (render and sim mesh), or a render mesh plus a hand-made sim mesh. Dependencies in the working folder.
- UV and weights: the pages do not list UV or weight requirements. Weights are not authored in: TransferSkinWeights copies them from the body skeletal mesh (FBX page: Target Meshes = Render Mesh, Transfer Method = Closest Point on Surface). The engine re-transfers weights for each character at build (line 74, `TransferSkinWeights`). Whether a mesh's own skin weights are kept: the pages say nothing; the engine override is as above.
- Four body LODs: "MetaHuman expects four body LODs" (render-mesh page). Remesh targets 50, 30 and 10 percent for LOD1 to 3, or hand-made LODs 0 to 3.

Steps (FBX path): import static mesh; create Physics > Cloth Asset with the USD Cloth template; keep TransferSkinWeights, Remesh nodes and ClothAssetTerminal; StaticMeshImport (Import Sim Mesh off); set the body skeletal mesh; optional painted relax maps (SetSkinningSelection) for tearing in armpits and upper thighs; re-evaluate and save. Then create an Outfit Asset from the "Resizable Outfit" template: tick Sized Outfit Source, one index per body size, set Size Name, Source Asset (cloth asset) and Source Body Parts; Num Resizing Interpolation Points 1,000 to 2,500 (default 1,500); the outfit's name must equal its folder's name; evaluation "can take several minutes". Then the Wardrobe Item (WI_) with the MetaHuman Outfit Pipeline, runtime material parameters (vector, name identical across materials and sizes) and an optional Body Hidden Face Map.

Tools: Unreal's Dataflow Editor and Paint Weight Map; Creator; MetaHuman Manager for packaging. No Blender or Marvelous steps appear in Epic's pages; Epic's example garments come from Maya (earlier note: Epic "covers only the Unreal side").

## 3. Packaged game, run time, cost

- Engine source, MetaHumanOutfitEditorPipeline.cpp lines 145 to 152 (8 Nov): for Production-quality builds the comment reads "we bake to meshes, because Outfits can't yet be cooked", and the fitted outfit is exported with `ExportToSkeletalMesh`. In Preview quality the Chaos outfit itself is kept (lines 154 to 159). So in 5.8.2 the resize is made by the editor pipeline at build time and the result shipped is a baked skeletal mesh per character.
- The pipeline class is in an editor module (MetaHumanDefaultEditorPipeline); the runtime class is MetaHumanOutfitPipeline. Whether any packaged game can fit an outfit to a new body at run time: not confirmed; the source read does not show a run-time resize. Unverified.
- Epic's Collections page: assembly "is fast enough to run on demand at runtime"; "Build is resource-intensive and runs once in the editor"; no memory figures; packaged game "not covered"; Experimental ("use caution when shipping with it"). https://dev.epicgames.com/documentation/metahuman/metahuman-collections-in-unreal-engine (read 8 Nov).
- No frame-time or memory number for outfits was found in any page read. Packaged-package size limit: 6 GB or less, about 1.5 GB advised (packaging page, below).

## 4. Known limits stated by Epic

- Body mismatch warping (quoted in wardrobe-at-scale/3-METAHUMAN-AND-FAB.md, original page not re-read).
- Clipping of armpits/thigh gap in source bodies hurts resizing (bodies page).
- Weight transfer can tear at armpits and upper thighs; fix by painted maps (build pages).
- Relax maps on a sim mesh need a merged mesh or it "pull[s] apart at the seams".
- Cannot hide faces on the head mesh; only body (testing page). Several items per slot allowed; remove by hand.
- Importing with skeleton data as a skeletal mesh "not recommended" (FBX page).
- The pages read say nothing specific about layered garments, boots, tight knits or collars. Third-party reports of stretched cuffs and lost cloth are in wardrobe-at-scale/3 (search summaries only; unverified).

## 5. What a small test would show, and Epic's own resizable garments

- Epic's documented fit check: wear the WI_ item in Creator's Hair & Clothing tool, then move Head & Body sliders and presets and watch resizing and source-size switching; clipping is judged with the Body Hidden Face Map; "If the outfit doesn't fit accurately to a certain body type, export that body type and create a new size for it." No numeric measure is given. (testing page, read 8 Nov.)
- Verification: MetaHuman Manager "Verify" blocks packaging on errors; engine class VerifyMetaHumanOutfitClothing (VerifyMetaHumanOutfitClothing.cpp, lines 56 to 75) checks the outfit structure and the WI_ item.
- Epic's own resizable garment found: "MetaHuman Techwear Outfit", seller Epic Games, free, jacket, pants and shoes in one asset, 4 body LODs, wardrobe item included. https://www.fab.com/listings/9e04c752-1979-4723-b78f-6d24afc532bc (read 8 Nov). Others by Epic: none found (a search summary found none; unverified).
- Epic's 5.8 install has DefaultOutfitPipeline.uasset under MetaHumanCharacter\Content\BuildPipeline; a search for other bundled outfit assets was not carried out.

## 6. Licence

- The Techwear Outfit listing's "License terms" field is blank ("-"), so no terms are stated there (same listing, read 8 Nov).
- Epic's MetaHumans-on-Fab and Buying pages (https://dev.epicgames.com/documentation/metahuman/metahumans-on-fab, .../buying-metahumans-from-fab, read 8 Nov) carry no licence terms; the first says buyers "can add any products you acquire that use the MetaHuman format directly to your Unreal Engine project".
- Search summary only (unverified): assets with MetaHuman-compatible content may not be sold under CC BY 4.0; Epic launch coverage says MetaHuman clothing can be used in other engines.
- The MetaHuman licence agreement and Fab's standard licence were not read. Not confirmed from a primary page.

## Could not be reached or read

- https://dev.epicgames.com/documentation/metahuman/parametric-asset-setup and .../getting-started-with-parametric-clothing (heading only returned).
- Official 5.6 to 5.8 release notes (only the forum posting partly read).
- MetaHuman licence agreement; Fab licence page; Epic's own Fab listing beyond the Techwear page.
- A Swiss clock reading (no shell available).
