# Epic's resizable outfit: second reading (item n09-6, read 9 November 2026)

Adds to RESIZING-READING-2026-11-08.md; does not repeat it. No synthesis. All pages read 9 Nov 2026 by fetch (a small model summarised each page; wording is not verbatim). "Unverified" marks anything not confirmed.

## 1. Setup and Getting Started pages: steps, sizes, output, limits

The 8 Nov file could not read the two pages. Their working addresses (the unreal-engine and ja-jp copies still return only a heading) are read now.

Getting Started (https://dev.epicgames.com/documentation/metahuman/getting-started-for-creating-parametric-clothing-in-metahuman):
- Parametric clothing "doesn't need skinning. The model alone is sufficient." Epic says skeletal-mesh clothing "doesn't resize, but can now be made for any body shape" and suggests it for complex assets. So a garment already bound to the MetaHuman skeleton is the non-resizing kind; the resizable kind starts from a plain model (render mesh, optional sim mesh).
- Render mesh: always present, may have thickness and detail. Sim mesh: optional, simplified, single-sided, drives the render mesh, not rendered, can support resizing and skinning. USD from Marvelous or CLO carries a sim mesh.
- An Outfit Asset links the garment to a source body and warps it to a target body. Warping is worse when the target differs greatly from the source, "especially for realistic, detailed clothing". More outfits for more source bodies reduces warping; the system picks the best source automatically. Start with one, test, add more. An outfit holds one or more cloth assets.
- Prefixes: CA_ cloth asset, OA_ outfit asset, WI_ wardrobe item.

Parametric Asset Setup (https://dev.epicgames.com/documentation/metahuman/parametric-asset-setup-for-metahuman):
1. UE 5.6 or later. Enable MetaHuman Creator, Chaos Cloth Asset and Chaos Cloth Asset Editor plugins; close Unreal fully and restart.
2. Epic Games Launcher: Library > Options > tick "MetaHuman Creator Core Data", Apply.
3. Project Settings > MetaHuman SDK: note the Outfits path (default /Game/Outfits).
4. Make /Game/Outfits/<name>/<name>/ as the working folder; everything needed must be inside it "to pass verification".
- The page states no source sizes, output spec or limits on layers, sim, materials or LODs.

Source sizes (from the 8 Nov reading, same Epic pages, not re-read): at least 2 source bodies (masculine, feminine); more is better.

Fit output (https://forums.unrealengine.com/t/tutorial-chaos-cloth-outfit-asset-resizing-addendum/2647376, read 9 Nov): resizing "relies on recreating a new Cloth Asset inside the Outfit", which must be cooked and happens only in the editor. Epic staff (Kriss Gossart): run-time resizing "not currently possible"; Mutable suggested for run-time body fitting.

Sim limit (https://forums.unrealengine.com/t/intended-workflow-for-resizing-a-chaos-outfit-asset-while-preserving-cloth-simulation/2762838, Epic reply dated 5 Aug 2026, read 9 Nov): Creator's graph "strips out the sim mesh", so a resized outfit loses its simulation. Epic's workaround: a second outfit from the "Resizing Graph" template (Resizable Outfit = the base outfit, Target Body = the re-proportioned skeletal mesh, Strip Sim Mesh = false), applied through a Chaos Cloth Component. One outfit asset per differently proportioned character. Whether that fixes the poster's belt fault: unconfirmed in the thread.

Node note (search summary only, unverified): ApplyResizing is marked Experimental and needs a target skeletal mesh whose vertices match the source mesh.

Packaging page (https://dev.epicgames.com/documentation/metahuman/packaging-your-outfit-asset-with-metahuman-manager): Verify then Package; errors block, warnings do not; output .mhpkg, 6 GB or less, about 1.5 GB advised. Needed for Fab upload; not shown to be needed for use in our own project.

## 2. Techwear Outfit: source and licence

- Source: Fab listing by Epic Games, free, jacket, pants and shoes, 4 body LODs, MetaHuman format; the setup page also says the example asset "techwearOutfit" can be downloaded from Fab. https://www.fab.com/listings/9e04c752-1979-4723-b78f-6d24afc532bc (read 9 Nov). Not from Creator or a sample project, as far as the pages say.
- Listing licence field: "-" (blank). File size and UE versions: not stated.
- Fab standard licence summary (https://www.fab.com/cla, read 9 Nov): assets may be used "commercially or privately"; projects containing Fab assets may be distributed commercially; no engine restriction stated; no resale or free redistribution of the asset on its own. The page says its summary is not legally binding; the full EULA was not in the page.
- MetaHuman licence (https://www.metahuman.com/license): the fetch redirected to an Epic sign-in. Not followed (no logins). Unreached.
- Search summary only, unverified: Epic says MetaHuman falls under the standard Unreal licence (free under USD 1 million revenue). Unverified.
- So: no licence text specific to Techwear was reached; whether it may ship in a commercial Unreal game is not confirmed from a primary source. The Fab summary points to yes; the listing field is blank.

## 3. Memory or frame cost

- None stated in any page read on 9 Nov (Getting Started, Setup, Packaging, the two forum threads). The 8 Nov file found none either.
- The only size figure: package limit 6 GB, about 1.5 GB advised (a Fab upload limit, not a run-time cost).
- Baked per-character mesh: 8 Nov reading found the engine source bakes a skeletal mesh at Production quality. No memory or draw cost is stated anywhere; would have to be measured.

## 4. What a Wednesday test on Tom's garments would need from these pages (a list, in order)

Inputs:
a. Tom's garment as a plain render mesh (FBX), not skin-bound; optionally a sim mesh (USD from Marvelous). Ron-style skinned meshes are the non-resizing kind.
b. Source bodies exported from Creator as _CombinedSkelMesh: at least 2 (masculine, feminine); Tom's own body would be one, a second differing body for the resize target.
c. UE 5.8 project with the three plugins on and Creator Core Data downloaded.
d. For comparison: the Techwear Outfit from Fab (licence caution above).

Steps:
1. Enable plugins, install Core Data, restart; confirm Outfits path.
2. Make /Game/Outfits/<name>/<name>/ and import the garment and body skeletal meshes there.
3. Build the Cloth Asset (USD Cloth template; TransferSkinWeights, Remesh to 50/30/10 percent, ClothAssetTerminal); paint relax maps if armpits or thighs tear.
4. Create the Outfit Asset from the Resizable Outfit template: one sized source per body, interpolation points 1,000 to 2,500; name equals folder name; wait several minutes.
5. Create the Wardrobe Item with the MetaHuman Outfit Pipeline.
6. Test in Creator (Hair & Clothing): drag in the WI_ item, not the OA_; move Head & Body sliders; add a size if one body fits badly.
7. Run MetaHuman Manager Verify.
8. Assemble Tom as a character at Production quality; record the baked mesh (memory, triangles, sim kept or lost per the 5 Aug 2026 reply).
9. If sim is wanted: Resizing Graph outfit with Strip Sim Mesh false.

## Not reached

- https://www.metahuman.com/license (sign-in redirect).
- Full Fab EULA text; the Learning Library addendum text itself (only the forum announcement); the weight-map painting and Fab upload pages.
- The unreal-engine and ja-jp copies of Setup and Getting Started (heading only).
