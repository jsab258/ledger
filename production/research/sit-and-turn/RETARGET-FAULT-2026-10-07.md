# Retarget fault: Mixamo sitting clips on the MetaHuman

7 October 2026. **D** = read at source; **S** = search summary; **I** = inference, untested. Nothing was run in Unreal.

## 1. The cause

- **The source's rest pose is each clip's first frame.** All three imports warn of "invalid bind poses", so Unreal sets every joint's rest to its pose at time zero [5, 6] (D). Blender writes the bones' default transforms from the current frame's pose, which does not match its bind pose [8, 12] (I/S). sit_talk and stand_up start seated [7] (D).
- **The retargeter measures against that rest pose.** FK copies rotations as changes from it, and the pelvis height is scaled by the ratio of the two rest heights [2] (D). Seated against a seated rest pose is no change, so the MetaHuman stays standing: head 143.1, rest 143.4 (I). IK goals are the source leg's direction times the target leg's length [2] (D), so a seated leg is thrown forward: foot y 49.7, z 28.1 (I). stand_up overshoots by about 90°, likely the body lying in mid-air (I).
- **The pelvis reading of −3.2 fits no rigid body** with the head at 143.1 (146 cm apart; the spine is 56). This picture puts it at about 86.8. Re-read it with the target mesh as `optional_skeletal_mesh` (I).
- **Why set_retarget_root changed nothing:** the Mixamo template already sets the pelvis to Hips, and the call writes that same field [1] (D). "SitRig" is only the root-motion bone, and it does not move [1, 3] (D). The clips were rebuilt at 20:56 [4, 6] (D): same input, same output. The script comment blaming the top node is wrong.
- **Ruled out:** missing tracks; every target bone is written each frame [4] (D). **Risk:** the retarget pose drops scale [3] (D), so SitRig's scale must be 1 (I).

## 2. The reliable route

- Unreal imports skinless Mixamo clips as animations onto an existing skeleton, as the project already does [9] (D). Blender is needed only for one T-pose mesh per bot.
- The harvest holds Mixamo's T-Pose clips for both bots [10] (D): X Bot for sit_down and stand_up, Y Bot for sit_talk.
- Unreal 5.8 ships no Mixamo rig assets; the Mixamo template is built in [1, 11] (D). The MetaHuman plugin ships IK_MH_IKRig (full-body IK, free pelvis) and RTG_MH_IKRig [11] (D).
- Align T-pose to A-pose with Auto Align [13] (S/D). Keep the Blender settings, so mesh and clips share one skeleton.

## 3. Steps, each with its proof

1. In Blender, export the T-Pose clip with the stand-in mesh, and the sit clips as armature only. **Proof:** rest Hips z is 100 to 105, and the hands are within 5 cm of shoulder height.
2. Import the mesh with `FbxImportUI` (`import_mesh`, `import_as_skeletal`). Import the clips with `mesh_type_to_import=FBXIT_ANIMATION` and `skeleton` set to that mesh's skeleton [9]. **Proof:** each clip uses that skeleton, and SitRig's scale is 1.
3. On the rig: `set_skeletal_mesh(sk)`, then `apply_auto_generated_retarget_definition()`. **Proof:** it returns True, and `get_retarget_root()` returns "Hips".
4. On the retargeter: `set_ik_rig` for both sides; `set_preview_mesh` for source and target; `add_default_ops()`; `assign_ik_rig_to_all_ops` for both sides; `auto_map_chains(FUZZY, True)`; `auto_align_all_bones(SOURCE)`. **Proof:** `get_source_chain` returns a chain for Spine, Head, LeftLeg and RightArm.
5. Run `run_batch_retarget`. **Proof for sit_talk at 0.5 s:** the pelvis is within 3 cm of 55.8 × 87.1 / the rest Hips height (about 47). Head minus pelvis is 50 to 57 cm. The feet are 0 to 15 cm high. **Proof for stand_up's last frame:** pelvis 85 to 90, head about 143.
6. Drop set_retarget_root.

## Sources (all read 7 Oct 2026)

1. D, IKRigAutoCharacterizer.cpp ~672–716, ~1775–1795; IKRigController.cpp ~412–494.
2. D, PelvisMotionOp.cpp ~165–391; FKChainsOp.cpp ~241–353; RunIKRigOp.cpp ~99–137.
3. D, IKRetargetProcessor.cpp ~28–92; RootMotionGeneratorOp.cpp ~197–329.
4. D, IKRetargetBatchOperation.cpp ~222–572, ~763–811.
5. D, Interchange: InterchangeSkeletonHelper.cpp ~341–352; FbxScene.cpp ~563–591.
6. D, ue-probe log, 7 Oct, 20:56.
7. D, sitting_clips.py ~26–28.
8. D, Blender 5.2 export_fbx_bin.py ~726–761.
9. D, import_figure.py ~1751–1779.
10. D, the harvest folder.
11. D, the 5.8 Plugins folder; the strings in IK_MH_IKRig.
12. S, web search on the time-zero fallback; Blender issue #113073 (page returned 403).
13. S/D, Epic, "Auto Retargeting in Unreal Engine" (5.8 page); IKRetargeterController.h ~435–452.
