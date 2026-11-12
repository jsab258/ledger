# CMU moves onto the cast through Unreal's retargeter: the method (12 Nov 2026)

Written 18:35 Swiss by the production session, for advisor 117 (sit-down, stand-up and a lean from the CMU library, retargeted with Unreal's own retargeter, filmed packaged beside ours) and advisor 118 (methods ready before the double week). No try made yet. Fresh reviewer against the sources owed before the first try (none spawned while the week is over 6 ahead). **D** = read at source on the date; **H** = our own tool or record; **I** = inference, untested.

## Questions
1. Which CMU files: format, licence, rest pose?
2. How does a non-Unreal skeleton reach Unreal as animation?
3. What does Unreal's retargeter need, and what does it make automatically?
4. What went wrong before on this route, and how is it avoided?
5. What reference does a studio game give? What is the check?

## Sources read (12 Nov 2026)
- Epic, IK Rig animation retargeting (page is for 5.9): https://dev.epicgames.com/documentation/en-us/unreal-engine/ik-rig-animation-retargeting-in-unreal-engine (D, via a summarising fetch)
- Epic, Auto retargeting (5.9): https://dev.epicgames.com/documentation/en-us/unreal-engine/auto-retargeting-in-unreal-engine (D, via a summarising fetch)
- Our CMU terms note: CMU-TERMS-AND-CLIPS-2026-11-12.md (CMU's own pages read at source 12 Nov 02:23)
- Our retarget fault: production/research/sit-and-turn/RETARGET-FAULT-2026-10-07.md; tools/ue/retarget_sitting.py, tools/meshgen/blender/sitting_clips.py, tools/ue/make_tom_retarget.py (H)
- Not reached: Epic's 5.8 pages (the installed engine is 5.8.2; the 5.9 pages were read, so every call is checked against the 5.8.2 source before use); the Auto retargeting page's link to the main retargeting page returned 404; the supported-skeleton video not watched.

## 1. Files
- CMU's terms allow the moves inside a sold game, not the files as a library (CMU home and FAQ, read at source; licence item on his page answered, CMU on the list since 12 Nov). The 4TU FBX set is CC BY-NC: out.
- Use cgspeed's BVH conversion (Hahne, 2010): no added restriction; **frame 0 is a T-pose facing +Z**; joints in MotionBuilder naming; 120 fps; no finger data (placeholders) (CMU-TERMS note, D).
- Prefer higher-numbered subjects (CMU home page: earlier captures noisier; cgspeed: joint flips in early directories).

## 2. Into Unreal
- Unreal imports FBX, not BVH (I: no BVH importer in the editor's import list; to check in 5.8.2's source before the first try). Route: Blender's BVH importer, then FBX out, the same way sitting_clips.py already writes Mixamo clips (H).
- One FBX per source skeleton holds the T-pose and a stand-in mesh (the frame-0 pose as the bind pose); each clip goes out as the armature's motion only and imports onto that skeleton. This is the fix of 7 Oct: imported alone, a clip's first frame becomes the rest pose and a seated start retargets as standing (RETARGET-FAULT, D).
- Resample 120 to 30 fps at export (cgspeed suggests 30 for playback; our clips run at 30) (I on our rate: check the existing A_*_MH clips' rate).

## 3. Unreal's retargeter (Epic, D)
- Two IK Rigs (source, target) with a pelvis set and chains; an IK Retargeter from source to target; retarget poses matched (T-pose source onto the MetaHuman's A-pose: Auto Align in Edit Retarget Pose); export the selected animations as new sequences.
- Auto: "Auto Retarget Chains" matches bone names to biped templates, "exact name matches are not required"; "Auto Create FBIK" makes the full-body solver. The page names only Epic's mannequins, MetaHumans and Stack O Bot; MotionBuilder naming is not named (unverified: our Mixamo skeleton, of similar naming, was auto-characterised on 7 Oct, H).
- Target: the MetaHuman plugin's IK_MH_IKRig and the cast's shared body skeleton, as retarget_sitting.py already does (H).
- IK goals on the feet only where the clip plants them (sit-down, stand-up); Speed Planting is for walks, not needed here (D on the ops, I on the choice).

## 4. Known faults and their guards
- Rest pose from a clip's first frame: avoided by the shared T-pose skeleton (section 2).
- Joint flips (cgspeed): read each clip's rotations frame to frame before retargeting; a jump over 90 degrees in one frame on any limb fails the clip (I: a script check, cheap, on the BVH itself).
- Fingers: none captured; the hands take the MetaHuman's relaxed hand from our idle, blended over the retargeted arms (I).
- Toe and hand noise (CMU home page): the toes take the foot's rotation; one smoothing pass on the hands only if the film shows jitter (I).
- Pelvis height and seat: the retargeter scales the pelvis by the rest heights; the game places the body on its seat, as the sitting clips do (H).

## 5. Reference and check
- Reference first: Mafia and KCD2 retarget their own studio capture in their own tools; neither uses a public library, so their numbers do not apply. Our own route (Mixamo sitting clips, 7 Oct; Tom's motion matching through RTG_UEFN_to_TomPlayer) is the reference: "none found" for a public library beyond our own.
- Clips to try first (CMU index wording, trials not yet viewed): stand up 143_18 "Sit Down And Get Up", 113_15 "Sit in chair and get up"; lean 15_06 "lean forward, reach for" (no wall or counter lean exists in the index); idle 140_06.
- The check: the retargeted clip on Ron, filmed packaged beside our current sit and stand: feet hold under 2 cm on the floor, knees straight at the top of a stand (under 10 degrees, where the markerless solve left 77), no limb flip, hands not through the body or the chair; one small reviewer, then the packaged walk.
- Cost guess, unmeasured: 4 to 6 hours for the first clip end to end (the Blender step reuses sitting_clips.py; the Unreal step reuses retarget_sitting.py), under an hour each after.

## Steps for the first try
1. Fetch the cgspeed BVH for the three clips (CMU on the list; record source and licence in THIRD-PARTY.md).
2. Blender: T-pose skeleton FBX with a stand-in mesh; clips as motion only at 30 fps (extend sitting_clips.py with a BVH entry).
3. Flip check on each clip.
4. Unreal: import, auto IK rig, retargeter onto IK_MH_IKRig, Auto Align, export (extend retarget_sitting.py; calls checked against 5.8.2's source first).
5. Film packaged beside the current clips; the check above.
