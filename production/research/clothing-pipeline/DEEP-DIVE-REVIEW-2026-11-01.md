# Review of DEEP-DIVE-2026-11-01.md (fresh reviewer, 1 November 2026)

Verdict: **PASS WITH FIXES.** The research holds: every engine-source line checked says what the deep-dive says, and no web source checked is wrong in substance. The faults are in the trials. Trial 1 would shrink the throat by only half the intended distance, and trial 2 names the wrong project. Both trials leave out steps the existing tools need, and trial 1 has an unstated risk to Tom's working build. Fixes are below.

Method: the installed UE 5.8.2 MetaHuman plugin source was read file by file. The web sources were read in full on 1 November 2026 (Marvelous and CLO help pages through Zendesk's public article API). Also read: tools/ue/hidden_faces.py, tools/ue/blender_hidden_face_map.py, tools/ue/blender_skin_through_probe.py, HIDDEN-FACES-2026-10-30.md, RULINGS.md, DECISIONS.md (30 October and 1 November entries), and the folders of both projects.

## 1. Engine-source claims (11 checked, 0 wrong, 2 qualified, 1 material omission)

| Claim | Result |
|---|---|
| `bTransferSkinWeights = true`, MetaHumanDefaultEditorPipelineBase.cpp 498 | CONFIRMED. This is the production branch. In preview the flag follows `HasFaceDNA()` (454). |
| Passed to the outfit, 1604-1609 | CONFIRMED (1603-1611). |
| MetaHumanOutfitEditorPipeline.cpp 71-74 | CONFIRMED. 71 sets the target body to the merged head and body; 74 sets the TransferSkinWeights variable. |
| "Re-transferred at every build" | QUALIFIED. This happens only when the pipeline's `OutfitResizeDataflowAsset` is set (`CanResizeOutfits`, 1592-1595 and 1995-2003). The source shows only that the flag reaches the resize dataflow. That hand-fixed weights are lost depends on the dataflow asset, which is content and was not read, so it stays (inference). |
| A skeletal-mesh item passes untouched | CONFIRMED. MetaHumanSkeletalMeshEditorPipeline.cpp 31-43 passes the mesh through as-is. |
| Both item pipelines carry `HeadHiddenFaceMapTexture`; the quote at MetaHumanSkeletalMeshEditorPipeline.h 25-41 | CONFIRMED (the comment is at 26-41; the outfit's header is at 68-83). |
| Applied to the face mesh's skin slots on every LOD, line 762 | CONFIRMED (755-762, with the LOD loop at 738-750). Applied only at Production quality for pinned items (1632-1634, 1718-1720), which the Optimized build meets (HIDDEN-FACES section 1). |
| Cull at 0.1 or below, keep at 0.9 or above, shrink along minus the normal, MaxShrinkDistance default 0 (MetaHumanGeometryRemovalTypes.h 22-50) | CONFIRMED. |
| **Omitted, and it matters:** how far a grey pixel moves | The shrink weight is linear: `1 - clamp((p - 0.1) / 0.8)` (MetaHumanGeometryRemoval.cpp 404-410, header 42-47). **Grey 0.5 moves a vertex only 0.5 x MaxShrinkDistance.** |
| **Omitted:** morph targets | Shrunk points are dropped from every morph target (MetaHumanGeometryRemoval.cpp 762-786: "assumed to be hidden"). On the face, the grey band stops following expressions and neck motion. |
| Num Resizing Interpolation Points 1,500 | CONFIRMED in the source (ChaosOutfitAsset OutfitCollection.h 65) and on [E9]. |
| "By script if 5.8's Python allows (UNVERIFIED)" | Can now be settled. `MetaHumanCharacterExportBlueprintLibrary::ExportDNA` is BlueprintCallable, with ExternalPath, bDNAHead and bDNABody (MetaHumanCharacterExportBlueprintLibrary.h 35-72, 206-207). |

Unit: the shrink is applied to the mesh's import points (cm), so 3 mm is entered as 0.3 (inference, strong). Step 4's measurement still settles it.

## 2. Web sources (12 read in full, 0 wrong in substance)

- E10: CONFIRMED, but misquoted. The page reads "We are unable to hide faces on the head mesh at this time." The black-and-white rule, the WI_ item and the drag warning are confirmed. The page says nothing about grey values.
- E7: CONFIRMED. The rigged-FBX advice comes "due to issues with visualization in the Dataflow Editor". Remesh 50/30/10, four LODs 0-3, the Relax/Prune/Hammer/Clamp/Normalize maps and SetSkinningSelection are all there.
- E9: CONFIRMED (Resizable Outfit, a Sized Outfit Source index per body, 1,500 points, 1,000-2,500).
- E2: CONFIRMED ("does not resize", "can cause warping", "multiple outfits for multiple source bodies").
- E5: CONFIRMED (DCC, Geometry, DNA and Materials export; the Full Body Skeletal Mesh). The page gives no version.
- E13: CONFIRMED (the collar a rectangle from the neckline, M:N, Trim_Fusible_Rigid, 3D seamline 0 "to remove the seamline in render"; Offset as Internal Line, then Cut and Sew; USD Thick, Unified UV, 2,048, 5 px; avatar scale cm (DAZ Studio) 100%, Y up, points and suit on). The page does not say "FBX".
- M1: CONFIRMED (menu path, Body and Head .dna, unit and scale, both automatic options "for humanoid avatars only", axis, joints, no .mtn). "2025.2" is not in M1; it is unsupported there.
- M5: CONFIRMED (close-fitting parts skinned, a maximum of 8 joints, collision thickness 2.5 to 5 mm).
- M6: CONFIRMED, but misquoted. The page reads "smaller and more consistent than shoe meshes", not "tighter and more even".
- C1: CONFIRMED, but misquoted. The page reads "Ensure the collar doesn't eat into the neck on 'Heavy' settings". The DCC Export in 5.6 is confirmed.
- X4 (Shaafi Ahmad, 5 August 2020): CONFIRMED for thickness off ("spirals") and density at the break line. "Back after" is not stated; the article only says thickness can be added later (Solidify, Panel Loops).
- X2 (Karimfazli, 14 August 2019): CONFIRMED.

Not checked: X1, X3, X5, E1, E3, E4, E6, E8, E11, E12, M2-M4, M7, M8, C2.

## 3. The trials

### Trial 1 (head map). Fixes:

1. **Grey 0.5 gives half the shrink.** Paint about 0.15 (weight about 0.94) in the band, or set MaxShrinkDistance to twice the intended depth. Never paint 0.1 or below, which cuts. Grade the band's top edge from white so it leaves no hard step.
2. **The depth it names was never measured.** No probe ever measured the throat at "25° down, 45° turned". blender_skin_through_probe.py has no head poses and has never been run on the head mesh (HIDDEN-FACES, line 185: "Not measured: the head mesh"). Add a step: extend the probe to the face mesh (from hidden_faces' after/ FBX) with head poses, then measure.
3. **Painting is new work.** The map is painted by blender_hidden_face_map.py, not hidden_faces.py, and that script works on the body only (UDIM 1002 UVs). A head painter on the face mesh's UV0 is new.
4. **hidden_faces.py needs a code change.** It sets only `BodyHiddenFaceMapTexture` and hard-codes max_shrink_distance 0 (lines 71, 323-329). It needs to import the head texture and set the head map with its own settings, through the C++ name `HeadHiddenFaceMapTexture`.
5. **Risk to Tom's working build.** A side build (the default) is invisible to the editor's sit walk, because ue-probe's junction reaches only /Game/Ledger/MetaHumans/MH_TomL1. A build over the game's copy replaces his current, cut build of 30 October. Its only backup, hidden-faces/before/files, is the 6 October uncut build: restoring it would bring skin back through the jeans and boots he now wears by default. Before any build over the game's copy, back up the current copy and the character file to a new folder with hashes, and use a new LEDGER_HF_OUT so the probe does not overwrite before/. Otherwise judge the side build in Blender.
6. **Watch the face while it moves.** Because of the morph-target drop, add talk and expression frames to the judge, and judge "the face unchanged" while animated, not only at rest.
7. **Check the face LODs first.** A face LOD built by reduction fails the whole build (MetaHumanGeometryRemoval.cpp 442-448, then EditorPipelineBase 746-749 and 762-766).

### Trial 2 (DNA importer). Fixes:

1. **Wrong project.** Tom's character asset is F:\LedgerTools\mh-dress\Content\Cast\MH_TomL1.uasset (172 MB). C:\LedgerTools\mh-assemble holds only a built copy. Export the DNA from mh-dress with `ExportDNA` (ExternalPath set, ProjectPath empty), then put the character file back and check its hash.
2. **Window step rules.** The window step falls under the 29 October ruling and RULINGS line 25. The session does it, never a helper, after 10 minutes with no keyboard or mouse input, and logs it in the day's summary. "The builder" is ambiguous.
3. **Empty scene first.** Save the open work and start a new, empty Marvelous scene, so that Import (Add) does not add the avatar to that work.
4. **Blender cannot read .avt.** Export the old avatar as OBJ too, or compare against MH_TomL1_FullBody.fbx at scale 10.

Trial 2 does not touch the game.

## 4. Proposed skill lines

| Line | Result |
|---|---|
| Footwear dummy mesh [M6] | Supported, for a shoe registered as a .zacs accessory. Use the page's words. |
| Head map, grey under the edge [Source] | Supported as a mechanism, and only if trial 1 passes. Add: "the grey value sets the fraction moved (0.1 full, 0.5 half); shrunk points lose the face's morph targets". |
| Outfit weights re-transferred [Source] | Partly supported: the flag is passed when the resize dataflow is set. Mark "hand fixes lost" as inference. |
| Outfit Asset for a refit [E9] | Supported. |
| DNA importer as an alternative [M1] | Supported (conditional on trial 2). |
| Collar fabric and seamline [E13] | Supported. The seamline 0 is a render choice. |
| Thickness and topology [X4][X2] | Supported. "Back after" is X4's option, not its stated step. |
| Refit check [C1] | Supported. Use "doesn't eat into the neck on Heavy". |
