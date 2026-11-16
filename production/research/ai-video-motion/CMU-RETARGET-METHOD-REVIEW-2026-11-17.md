# Review: CMU moves onto the cast through Unreal's retargeter (method note of 12 Nov)

Reviewed 16 Nov 2026 by a fresh reviewer for n16-7 (people alive; first moves: sit down, rise, a lean, the office exit). File named for 17 Nov as briefed. Note reviewed: production/research/ai-video-motion/CMU-RETARGET-METHOD-2026-11-12.md, read in full. **D** = read at source on 16 Nov 2026; **H** = the project's own record or tool; **I** = inference, untested.

## Verdict: pass with fixes (11 fixes)

The route is sound and its claims about Epic's pages and cgspeed's conversion hold. But, as written, it would hit the same pelvis fault the HumanMotionCraft test hit on 13 Nov: CMU's BVH rest pose has the hips at the origin. It also says nothing about root motion, which the office exit needs. It offers no lean that fits and no exit clip at all, and its acceptance check is not yet measurable as written. Two of the fixes must be made before the first try: fix 1 (pelvis rest height) and fix 3 (root motion).

## 1. Claims checked against the sources marked D

| Note's claim | Source, read 16 Nov 2026 | Result |
|---|---|---|
| Two IK Rigs (pelvis set, chains), an IK Retargeter, retarget poses matched with Auto Align, export of selected animations | Epic, IK Rig animation retargeting (5.9 page), https://dev.epicgames.com/documentation/en-us/unreal-engine/ik-rig-animation-retargeting-in-unreal-engine (D, through a summarising fetch, as the note's was) | Matches. The page also says a retarget pose can be imported from an animation sequence ("Sequence Frame" default 0), which is useful for fix 1 |
| "Auto Retarget Chains" matches names to biped templates; "exact name matches are not required"; "Auto Create FBIK" | Epic, Auto retargeting (5.9), https://dev.epicgames.com/documentation/en-us/unreal-engine/auto-retargeting-in-unreal-engine (D, summarising fetch) | Matches, quote exact |
| The page names only mannequins, MetaHumans and Stack O Bot; MotionBuilder naming not named | same | Matches |
| The Auto page's link to the main page returns 404 | same | Matches (it points to /documentation/404) |
| "IK goals on the feet only where the clip plants them; Speed Planting is for walks (D on the ops)" | IK Rig retargeting page | Partly. The page says IK goals are "usually unnecessary" and are added only for adjustments such as Speed Planting, Stride Warping or Blend to Source. It does not cover what Speed Planting is for (that is on the Retargeting Operation Stack page, unreached). "For walks" should be marked I |
| cgspeed BVH: no added restriction; frame 0 a T-pose facing +Z; MotionBuilder naming; 120 fps; finger placeholders | cgspeed READMEFIRST (mirror), https://raw.githubusercontent.com/sfd158/cmu-mocap/master/READMEFIRST.txt (D); announcement, https://groups.google.com/g/bvhacker/c/r906SGjjcTA (D) | Matches. Small point: the README calls the T-pose the "new first frame" (frame 1 in a one-based player). Frame Time .0083333 (120 fps) also measured in 143_18.bvh (below) |
| cgspeed suggests 30 fps for playback | announcement (D) | Matches: "set your animation software to 30fps (for NTSC), 25fps (for PAL), or 24fps (for film)" |
| Joint flips in early directories | announcement (D) | Matches: "particularly earlier in the numeric series of directories, have a lot of joint-flip problems" |
| Clip wording 143_18, 113_15, 15_06, 140_06; "no wall or counter lean exists" | CMU index (mirror), https://raw.githubusercontent.com/sfd158/cmu-mocap/master/cmu-mocap-index-text.txt (D) | Matches. No line contains wall-lean or counter; "wall" appears only in "smash against wall" |
| Rest pose from a clip's first frame: the 7 Oct fault | production/research/sit-and-turn/RETARGET-FAULT-2026-10-07.md (H) | Matches |
| "Not reached: Epic's 5.8 pages" | RETARGET-FAULT source 13 records the 5.8 Auto retargeting page as read on 7 Oct (S/D) | Inconsistent between the two notes, but small |
| "Mafia and KCD2 retarget their own studio capture in their own tools; neither uses a public library" | no source cited | Unsourced: mark I |
| CMU home page: higher-numbered subjects first, toe and hand noise | http://mocap.cs.cmu.edu/ | **Unreached today**: the fetch tool forces https and the certificate fails. The 12 Nov terms note records a plain-http read at 02:23. The advice to prefer higher-numbered subjects is confirmed by cgspeed (above) |

**Measured today** (D, https://raw.githubusercontent.com/sfd158/cmu-mocap/master/data/143/143_18.bvh, first 100,000 characters of 571,199 read):
- `ROOT Hips`, OFFSET 0 0 0. There is no separate root bone; `LHipJoint` has a zero offset.
- LeftUpLeg offset (1.65, -1.42, 0.94), LeftLeg (2.12, -5.81, 0), LeftFoot (2.37, -6.50, 0). The two leg offsets point the same way (ratio 0.364 in both), so the rest legs are straight, splayed about 20 degrees.
- 753 frames at .0083333 s (6.3 s).
- Frame 1 (the T-pose): root at (4.66, 15.53, -0.24), rotation 0 0 0. Frame 2: rotation (-160.1, -83.6, 157.9). So the added T-pose differs from the capture's first frame by a large turn.
- Units: a hip height of 15.53 units fits a standing adult only at about 5.6 to 5.8 cm per unit. In inches it would be 39 cm. **The BVH is not in inches.** The usual CMU factor of 0.0564 m per unit (ASF length 0.45, inch based) fits the measurement but was not read at a source (I).

## 2. The 13 Nov test's three retarget faults, and whether the CMU steps guard against them
Source: production/research/tool-tests-2026-11/HUMANMOTIONCRAFT-ROUND1-2026-11-13.md (H). Engine source re-read 16 Nov in the installed 5.8 (D): PelvisMotionOp.cpp lines 183 to 224; RootMotionGeneratorOp.h; IKChainsOp.cpp lines 40 to 168.

**a. Pelvis scaled from a rest far from the clip (16x, pelvis 15 m up).** PelvisMotionOp divides the target's pelvis height by the source's retarget-pose pelvis height. If the source pelvis is near the ground, it logs "BadPelvisHeight" and uses 1.0 (5.8 source, lines 187 to 192). That would scale the pelvis about 95 times.
- *CMU guard:* only partly. Section 2's "the frame-0 pose as the bind pose" is the right intent. But the BVH's rest has Hips at 0, and Blender's BVH importer builds its rest from these offsets (I). Unless the T-pose frame is applied as the rest pose, the CMU route reproduces this fault exactly, and worse than HumanMotionCraft's 5 cm.
- *Add:* fix 1.

**b. Root motion copied from a hip bone named root.** The root op's default is CopyFromSourceRoot, which copies the source root bone's motion, scaled by height. The other mode is GenerateFromTargetPelvis, with height either CopyHeightFromSource or SnapToGround (5.8 RootMotionGeneratorOp.h, D).
- *CMU guard:* none written. CMU's root is Hips, the same shape as HumanMotionCraft's. Through Blender's FBX export, the armature object may come in as a static root above Hips (the 7 Oct "SitRig", H). That would make the copy a no-op, but that is luck, not a step.
- The office exit needs real root motion; sitting and rising in place do not.
- *Add:* fix 3.

**c. Standing knees bent 22 to 33 degrees and feet 0.3 to 4.8 cm short after the leg-IK step.** IKChainsOp places each foot goal by the source limb's current length over its retarget-pose length, times the target limb's length (5.8, lines 41 to 49 and 120 to 135).
- *CMU guard:* better than HumanMotionCraft's, untested. The CMU rest legs are straight (measured above), so a standing frame normalises near 1.
- Two risks remain:
  - a leg chain started at the zero-offset `LHipJoint`;
  - CMU subjects standing with soft knees, which the target would copy, so "under 10 degrees" could fail on the source itself.
- *Add:* fix 4.

## 3. Licence line
The note says the terms allow the moves inside a sold game, not the files as a library, and that CMU has been on the list since 12 Nov.
- This agrees with CMU-TERMS-AND-CLIPS-2026-11-12.md (CMU home and FAQ, read at source 12 Nov 02:23).
- It agrees with RULINGS.md (24 Sep line: "CMU motion capture inside the game, never resold (12 Nov)") and DECISIONS.md 2026-11-12 07:33.
- cgspeed's "no additional restrictions" is confirmed today.
- **Mismatch:** ledger-v2/research/license-allowlist.md, which CLAUDE.md calls law, has **no CMU line** (read in full 16 Nov). The ruling lives only in RULINGS.md, so the derived home disagrees with the ruling. See fix 9.
- Also: the note never names the download source. cgspeed.com is unread in both notes, and the files would come from the GitHub mirror sfd158/cmu-mocap, whose README says only "AFAIK, yes" and points to READMEFIRST.

## 4. Clips against the needs, and the acceptance check
**Sit down and rise.**
- 143_18 "Sit Down And Get Up" fits: subject 143 is a recent subject ("General Subject Capture"), 6.3 s at 120 fps.
- 113_15 "Sit in chair and get up" fits. Subject 113 is "Post pregnant woman"; 111 and 114 are pregnant subjects, so their weight and balance may read wrong on the cast (I).
- 86_09 "walking, sitting, looking, stand up" is a spare.
- Seat height is unknown for every trial. The source's seated hip height must be read before matching the game's chair.

**A lean.**
- 15_06 "lean forward, reach for" is a reach, not a lean, and comes from an early subject (cgspeed's flip warning).
- 22_18 and 23_18 (hands on a high stool) are two-person and early.
- 134_03 "Lean Turn Right" is a walking lean.
- Study 07's need is "Lean on a wall or shop front" (production/research/aaa-reference/studies/07-animation.md, H).
- **No CMU clip fits; write "none found in CMU".** Next routes: Mixamo (on the list, his account) or Motionsmith's counter lean (feet drift 0.0 to 0.16 cm, H).

**The office exit.** The note has none, because it predates the 16 Nov order.
- CMU has no door, exit, handle or doorway line (index searched today).
- Usable pieces: rise (the second half of 143_18), then 131_01 "Start Walk Stop", 131_09 and 131_12 "Start Walk Left/Right", 83_36 to 83_39 "walk forward turn 90 degrees", 69_20 to 69_27 (subject 69, mid-numbered).
- The door itself: KCD2 does doors as 2 sets of 6 stages from both sides; Mafia has about 190 door animations (study 07, H). That method should be copied; the door hands come from Mixamo as study 07 planned.
- 137_16 "Drunk Walk" must never be chosen (canon's content rule).

**Acceptance check as written.**
- "Feet hold under 2 cm on the floor" is ambiguous: slide or height? No bone is named and no planted frames are defined.
- "Knees under 10 degrees at a stand's top" has no defined frame or angle, and no source baseline.
- "No limb flip" has no threshold on the retargeted output; the 90-degree rule is only on the BVH.
- "Hands not through body or chair" can only be judged by eye. The 13 Nov test's films had no chair drawn, so this would have been impossible.
- Fixes in fix 8.

## Fixes to make to the method note
1. **Pelvis rest height, before the first try.**
   - In Blender, apply the T-pose frame as the rest pose; then drop that frame from every exported clip, because 143_18 turns about 160 degrees between frames 1 and 2.
   - Check the rest Hips height lands at 80 to 100 cm after scaling.
   - In Unreal, treat any "BadPelvisHeight" line in the log as a stop.
   - Alternative: import the source retarget pose from frame 0 of the T-pose sequence (Epic page, D), or raise it by the measured gap, as hmc_ue_retarget.py does (H).
2. **Units.** State that the BVH is not in inches. Scale at BVH import by about 0.0564 m per unit (I, consistent with the measured 15.53-unit hip height). Keep the armature object's scale at 1 (7 Oct risk: the retarget pose drops scale, H).
3. **Root motion, before the first try.**
   - Set the root op's SourceRoot explicitly and check the imported skeleton's root, either the armature-object bone or Hips.
   - Sit and rise: in place, root op off or copying a static root.
   - Office exit: RootMotionSource = GenerateFromTargetPelvis, RootHeightSource = SnapToGround, bRotateWithPelvis off (the 5.8 header warns about pelvis yaw) (D).
4. **Legs.**
   - Leg chains run LeftUpLeg to LeftFoot, never from LHipJoint.
   - Test one standing frame first: compare source and target knee angles before any sit.
   - If the feet are short, compare the result with the leg IK goals off (FK legs). Epic calls goals "usually unnecessary" (D).
5. **Source and variant.** Name the cgspeed MotionBuilder-friendly release from the sfd158/cmu-mocap mirror, at a recorded commit. Do not use the Daz hip-corrected set: its correction "occasionally... introduces foot-slip / floor-contact problems" (announcement, D).
6. **Source IK rig fallback.** The 13 Nov test found the auto rig picked up only head, clavicles and feet in an unfamiliar naming (H). Keep a hand-built rig of 19 chains named as IK_MH_IKRig names them as the fallback, reusing tools/tool-tests/hmc_ue_retarget.py and measure_fbx_legs.py (both present, H).
7. **Clips.**
   - Lean: "none found in CMU", route to Mixamo or Motionsmith.
   - Add the exit pieces above.
   - Copy KCD2's In, Loop and Out per activity, tied to a seat or door anchor, with ground alignment off at furniture (study 07, H).
   - Exclude 137_16.
   - View each trial before choosing it.
8. **Acceptance check, measurable.**
   - **Feet.** A foot is planted while the source ball bone moves under 1 cm per frame. Over each planted span, two numbers, foot and ball bones on the exported FBX:
     - slide: the horizontal drift, at most 2 cm;
     - height: the lowest point above the floor, within plus or minus 2 cm.
   - **Knees.** Knee flexion is 180 degrees minus the angle at the knee between the thigh and shin vectors. It is read on every frame from the last time the pelvis reaches 97% of its standing height to the clip's end. Pass: at most 10 degrees, or within 3 degrees of the source's own knee where the source stands softer.
   - **Flips.** Fail if any limb bone turns more than 90 degrees between two 30 fps frames, checked on the BVH and again on the retargeted clip.
   - **Hands.** The film must contain the chair. Either measure the hand and finger bones against the chair's box and simple body capsules (fail if any goes more than 1 cm inside), or judge by eye from the front and the side every 10 frames, and say which was used.
   - **Bodies.** Run on Ron and on Rocco, not on the Build Average, Heavy or Slim bodies, which are identical (H).
9. **Licence home.** Add CMU's line to ledger-v2/research/license-allowlist.md (moves inside the game, never resold, ruled 12 Nov), or record in DECISIONS.md why RULINGS.md is its home. Record the mirror and commit in THIRD-PARTY.md.
10. **Source tags.**
    - Mark "Speed Planting is for walks" and the claim about Mafia and KCD2 capture as I.
    - Make the 5.8-page "not reached" line agree with RETARGET-FAULT's source 13.
    - Cite study 07 as the reference for structure (In/Loop/Out, doors in stages), not "none found".
    - Mark the Epic pages as read through a summarising fetch.
11. **Cost.**
    - The 13 Nov route measured each retarget at 0.1 s, an Unreal run at about 20 s and a film at 1 to 2 min (H).
    - The 4 to 6 h first-clip guess should drop the Blender rework the scripts already cover, but add the exit's door stages, which have no CMU source.

## Not reached
- CMU's own pages (http://mocap.cs.cmu.edu/, faqs.php): the fetch tool forces https, which fails "unable to verify the first certificate". Their terms rest on the 12 Nov 02:23 read.
- Epic's Retargeting Operation Stack page (https://dev.epicgames.com/documentation/en-us/unreal-engine/retargeting-operation-stack-in-unreal-engine): it returned only a table of contents.
- Epic's 5.8 pages were not tried; the 5.8.2 engine source was read instead.
- The source for CMU's 0.0564 m-per-unit factor was not read; the factor is consistent with the measurement only.
- cgspeed.com was not read.
- The rest of 143_18.bvh (characters 100,000 onwards) was not read; no trial was viewed.
