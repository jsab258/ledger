# Tom's jacket: skin at the chest below the collar (n09-2), diagnosis, 9 November 2026

Files read only. Blender, Unreal and the game were not run. Measures were made with a small FBX reader and rasteriser in the helper's scratch folder.

## Is the measure wrong?

Partly. The 9 Nov review calls the two patches new. They are not. The same oval left of the zip and the same fleck right of it show in every engine picture of Tom in jacket v30: editor 30 Oct (tom-outfit/2026-10-30-dress, dress5), 2 Nov (2026-11-02-sole4), the packaged walk of 4 Nov ("throat patch, known", 2026-11-04-packaged/review-jacket.md), and now. The jacket row in garments.json, unchanged since 4ee1f3d3f (30 Oct), lists it as a kept fault: "a small opening at the collar's front left of the zip seen standing". However, the FINDINGS entry covers only the chin and jaw from 10 degrees down, and the 2 Nov collar measure only tested head-down and turned poses. So this patch has been listed under the wrong name and never diagnosed. Nothing changed in the jacket, the import or the head. The 9 Nov frame is just the first close, frontal, daylit view at talk distance.

## Which mesh: the head mesh (sure: high)

- Where the patch is: the collar's top at the zip is at z 1.6545 m (the jacket's open edges). At 3.2 px/mm (from the zip band's width), the oval lies about 30 to 66 mm below that point, so z is about 1.59 to 1.625. Across, it runs from x about -20 mm to the zip (Tom's right). The fleck is at about +28 to +31 mm.
- At the front, the body mesh stops at z 1.505 (MH_TomL1_Body.fbx LOD0, |x| < 4 cm), and in the hidden-face build its chest is cut away. The head mesh reaches down to z 1.500 at the breastbone at all four levels of detail (hidden-faces/after face FBX, as dumped in dress-cast-2026-11-07/slits/npz/tom_face.npz). Only the head mesh is there.

## The jacket itself is whole

- The mesh has 220 open edges and no non-manifold edges. In the chest box, the only open edges are the collar's top edge.
- Seen from the front, every face nearest the camera in the patch area is cloth and faces the camera. The only back-facing faces are above the collar's top, where the inside of the collar's back shows. So the patch is not a hole and not a missing back-face.

## At rest the cloth clears the head by only about 3 mm

- Rasterised from the front at the bind pose, the head stays behind the cloth everywhere below the collar's top. The smallest gap is 3.09 mm at LOD0 and 3.20 mm at LOD1; LOD2 and LOD3 are similar, so the level of detail is not the cause.
- The closest places form two bands either side of the zip: left at x -34 to -16 mm, z 1.585 to 1.627, and right at x +16 to +31 mm. Within 3.5 mm there are 142 cells on the left and 2 on the right. This matches the large left oval and the tiny right fleck.

## Why the head crosses in the game

- The jacket and the head skin follow different bones at the patch. The jacket points there take spine_04 at 0.57 to 0.64 and spine_05 at 0.13 to 0.41 (skinned from the body without a neck; skin.json).
- The head points there take 60 to 90% from the face rig's neck joints (FACIAL_*_12IPV_NeckB*, NeckA*, AdamsA2). These sit under FACIAL_C_Neck1Root/Neck2Root, below neck_01 and neck_02. spine_04 carries only 0.10 to 0.34.
- RigLogic also moves these joints from driver-joint rotations measured against the DNA's neutral pose (UE 5.8, Plugins/Animation/RigLogic/Source/RigLogicModule/Private/AnimNode_RigLogic.cpp, lines 410 to 445).
- When neck_01 tips back relative to spine_05, the skin below its pivot (about z 1.624) swings forward. That happens when the head is held level on a bind neck that leans about 12 degrees forward (neck axis 0, -0.205, 0.979; head-map-record.json). By rough arithmetic, 3 mm takes about 8 to 9 degrees.
- Tipping the head down moves this skin backward, so the 2 Nov probe could not see it.
- Darren's breastbone slits (7 Nov) were the same kind of fault and looked the same: flat salmon.

**Flat and unlit:** this fits skin a few millimetres proud of the cloth, inside the collar's shadow. It does not tell a hole from a poke-through.

**The memory lead:** right about the mesh, since it is the head mesh. But on Ron and Darren the head crossed the cloth at bind. On Tom it is clear at bind and crosses only in the game's pose.

## Most likely cause

In the standing pose, the lower front of the head mesh, carried by the neck joints, comes forward through the base of the jacket's collar beside the zip. The cloth there clears it by only about 3 mm and follows the chest bones instead. Confidence: high that it is the head mesh; medium for the pose mechanism.

## Smallest fix and its check

- **Confirm first:** log in the game the standing idle's neck_01 rotation against spine_05, and the offset of the face part's FACIAL_C_Neck1Root from its bind pose. Pose the margin map by that amount; it should cross at the patch.
- **Fix:** the 7 Nov Darren method. Run clear_layers.py --head on v30, front only, x -40 to +35 mm, z 1.57 to 1.645, clearing to the logged depth plus 3 mm (about 7 to 10 mm). Keep the weights. Then skin_garment.py, import_garments.py and a package.
- **Check:** the same close camera in the packaged game. The skin mask (r > 100, r > b + 40, r - g > 25) inside x 1150 to 1350, y 950 to 1150 now counts 5,486 px; it should count none. Also check the collar's look and the posed checks against v30.
- The jacket is set aside after four collar tries. Whether this counts as the same fault, so a new try needs Jafar's yes, is for the session to decide.

## Not checked

- The game's actual neck angle and RigLogic output.
- Tom's DNA driver list.
- The cooked jacket's levels of detail.
- The head's material in that area: Blender names the slot MI_Teeth_Baked, the same naming oddity as in head-map-record.json.
- The tester films of 28 to 29 Oct: no longer on disk.
