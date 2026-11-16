# CMU moves onto the cast through Unreal's retargeter: the method (12 Nov 2026)

Written 18:35 Swiss by the production session, for advisor 117 (sit-down, stand-up and a lean from the CMU library, retargeted with Unreal's own retargeter, filmed packaged beside ours) and advisor 118 (methods ready before the double week). No try made yet. Fresh review: CMU-RETARGET-METHOD-REVIEW-2026-11-17.md, pass with fixes (11), all taken 17 Nov (section 6 and the edits marked 'review'). **D** = read at source on the date; **H** = our own tool or record; **I** = inference, untested.

## Questions
1. Which CMU files: format, licence, rest pose?
2. How does a non-Unreal skeleton reach Unreal as animation?
3. What does Unreal's retargeter need, and what does it make automatically?
4. What went wrong before on this route, and how is it avoided?
5. What reference does a studio game give? What is the check?

## Sources read (12 Nov 2026)
- Epic, IK Rig animation retargeting (page is for 5.9): https://dev.epicgames.com/documentation/en-us/unreal-engine/ik-rig-animation-retargeting-in-unreal-engine (D, read through a summarising fetch)
- Epic, Auto retargeting (5.9): https://dev.epicgames.com/documentation/en-us/unreal-engine/auto-retargeting-in-unreal-engine (D, read through a summarising fetch)
- Our CMU terms note: CMU-TERMS-AND-CLIPS-2026-11-12.md (CMU's own pages read at source 12 Nov 02:23)
- Our retarget fault: production/research/sit-and-turn/RETARGET-FAULT-2026-10-07.md; tools/ue/retarget_sitting.py, tools/meshgen/blender/sitting_clips.py, tools/ue/make_tom_retarget.py (H)
- Not reached: Epic's 5.8 pages were not tried (as RETARGET-FAULT's source 13; the installed engine is 5.8.2; the 5.9 pages were read, so every call is checked against the 5.8.2 source before use); the Auto retargeting page's link to the main retargeting page returned 404; the supported-skeleton video not watched.

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
- IK goals on the feet only where the clip plants them (sit-down, stand-up); Speed Planting is for walks, not needed here (I).

## 4. Known faults and their guards
- Rest pose from a clip's first frame: avoided by the shared T-pose skeleton (section 2).
- Joint flips (cgspeed): read each clip's rotations frame to frame before retargeting; a jump over 90 degrees in one frame on any limb fails the clip (I: a script check, cheap, on the BVH itself).
- Fingers: none captured; the hands take the MetaHuman's relaxed hand from our idle, blended over the retargeted arms (I).
- Toe and hand noise (CMU home page): the toes take the foot's rotation; one smoothing pass on the hands only if the film shows jitter (I).
- Pelvis height and seat: the retargeter scales the pelvis by the rest heights; the game places the body on its seat, as the sitting clips do (H).

## 5. Reference and check
- Reference first (review): study 07 (production/research/aaa-reference/studies/07-animation.md) for structure: KCD2's In, Loop and Out per activity tied to a seat or door anchor, ground alignment off at furniture; doors in stages (KCD2 2 sets of 6 from both sides; Mafia about 190 door animations). That both retarget their own studio capture rather than a public library is I. Our own route (Mixamo sitting clips, 7 Oct; HumanMotionCraft's retarget, 13 Nov) is the reference for the retarget itself.
- Clips to try first (CMU index wording, trials not yet viewed): stand up 143_18 "Sit Down And Get Up", 113_15 "Sit in chair and get up"; lean: none found in CMU (15_06 is a reach, 134_03 a walking lean; study 07 needs a lean on a wall or shop front): Mixamo or Motionsmith's counter lean; idle 140_06. Office exit (review): no door clip in CMU; rise (second half of 143_18), then 131_01 "Start Walk Stop", 131_09/131_12 "Start Walk Left/Right", 83_36 to 83_39 "walk forward turn 90", 69_20 to 69_27; the door hands from Mixamo in stages as study 07. Never 137_16. Each trial viewed before it is chosen.
- The check (review, measurable), on Ron and on Rocco, filmed packaged beside our current sit and stand: feet: a foot is planted while the source ball bone moves under 1 cm a frame; over each planted span, foot and ball bones on the exported FBX slide at most 2 cm and sit within plus or minus 2 cm of the floor. Knees: flexion = 180 minus the thigh-shin angle, every frame from the last time the pelvis reaches 97% of standing height to the end: at most 10 degrees, or within 3 of the source's own knee. Flips: no limb bone turns over 90 degrees between two 30 fps frames, on the BVH and on the result. Hands: the chair in the film; hand bones against the chair's box and body capsules (fail over 1 cm inside), or by eye front and side every 10 frames, saying which. Then one small reviewer and the packaged walk.
- Cost guess, unmeasured: 3 to 5 hours for the first clip end to end (the scripts cover the Blender and Unreal steps; the 13 Nov route measured a retarget at 0.1 s, an Unreal run about 20 s, a film 1 to 2 min), plus the exit's door stages, which have no CMU source; under an hour each after.

## Steps for the first try
1. Fetch the cgspeed MotionBuilder-friendly BVH (from the sfd158/cmu-mocap mirror, commit recorded; never the Daz hip-corrected set, which can add foot slip) for the chosen clips; record source, commit and licence in THIRD-PARTY.md (CMU is item 11 of the licence allowlist).
2. Blender: import the BVH at about 0.0564 m per unit (it is not inches; I, checked by the rest hips landing at 80 to 100 cm), armature object scale 1; apply frame 0's T-pose as the rest pose, then drop that frame from every clip (143_18 turns about 160 degrees between frames 1 and 2); T-pose skeleton FBX with a stand-in mesh; clips as motion only at 30 fps (extend sitting_clips.py with a BVH entry).
3. Flip check on each clip.
4. Unreal: import; auto IK rig, falling back to the hand-built 19-chain rig named as IK_MH_IKRig (tools/tool-tests/hmc_ue_retarget.py); leg chains LeftUpLeg to LeftFoot, never from LHipJoint; retargeter onto IK_MH_IKRig, Auto Align; the root op's SourceRoot set by name (CMU's top bone is Hips): sit and rise in place (root op off or a static root), the exit with GenerateFromTargetPelvis, SnapToGround, bRotateWithPelvis off; any BadPelvisHeight log line is a stop; one standing frame first, source and target knees compared, and if the feet are short, compared with the leg IK goals off; export (extend retarget_sitting.py; calls checked against 5.8.2's source first).
5. Film packaged beside the current clips; the check above.
