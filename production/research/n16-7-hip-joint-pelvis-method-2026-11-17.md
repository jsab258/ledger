Method researched: Epic's Retargeting Operation Stack 5.8 and Retargeting Bipeds pages, Autodesk HumanIK Retarget Specific attributes, Unity Mecanim's body transform, Unreal 5.8.4 (installed) PelvisMotionOp.cpp and RunIKRigOp.cpp

# n16-7 "CMU feet": the hip-joint pelvis method (research note, 17 Nov 2026)

Item n16-7, fault "CMU feet". Two tries are used and the fault is set aside (RULINGS 7 Nov). This note picks the one genuinely different method that comes next. It is research only: nothing was built or run in Unreal, and no project file other than this note was written. All web sources were read on 17 Nov 2026. Engine files are Unreal 5.8.4 as installed (Build.version PatchVersion 4; the project's notes call it 5.8.2), C:/Program Files/Epic Games/UE_5.8/Engine/Plugins/Animation/IKRig/Source/IKRig, read the same day. The review checked every cited line against 5.8.4 and they hold (review fix 1).

## Questions

1. How do professional pipelines retarget motion capture when the hips-to-pelvis offsets differ, so that pelvis height and knee bend match? (Placing the target pelvis from the source's hip-joint midpoint, pelvis height from the leg-length ratio, MotionBuilder/HumanIK hips handling, the options of Unreal's own Pelvis Motion op.)
2. Which one method fits this pipeline (a Python-scripted IK Retargeter asset in 5.8, six clip pairs on Rocco and RoccoP2) and is genuinely different from tries 1 and 2?
3. What exact settings, or what small offline pre-pass, implement it, and what numbers must it reach on the existing measure (height and knees, with slide still 6/6 and flips still 0)?
4. How do Mafia: The Old Country and Kingdom Come II handle this, if any public source says?

## Where things stand (project evidence)

- Diagnosis: F:/LedgerTools/tool-dev/reports/CMU-RETARGET-FEET-DIAGNOSIS-2026-11-17.md. Point 2: CMU's Hips bone sits 8.0 to 9.3 cm above the hip joints, while MetaHuman's pelvis sits 1.1 to 1.3 cm below the thighs (analysis.txt section 4, F:/LedgerTools/tool-dev/runs/cmu-diag-2026-11-17).
- Try 1 (kept): leg chains One to One, the ankle-goal rig copy, Scale Source with factor s = target pelvis / source Hips height (0.974 to 1.140), Blend to Source on the legs (horizontal only), the source feet turned back to their T-pose. Result: slide 6/6, flips 0, height 3/6, knees 1/6 (DECISIONS.md 17 Nov 05:43; F:/LedgerTools/game-inputs/cmu-2026-11-17-try1/measure).
- Try 2: Scale Source with a hip-HEIGHT ratio (1.091 to 1.272); Pelvis Motion Scale Horizontal and Vertical 1.11 to 1.13; a fixed global Z offset of -10.6 to -12.5 cm; Affect IK 1/1 (F:/LedgerTools/game-inputs/cmu-2026-11-17-try2/ue/ue_result.json, "hips" and "pelvis" blocks). Result: still only 143_18 on RoccoP2 passes. Slide fails 2 pairs (2.73 and 2.29 cm). Height fails 5 pairs: 113_15 sinks 5.4 to 5.6 cm and 131_01 floats 4.1 to 4.3 cm. A fixed Z offset is wrong whenever the pelvis tilts (DECISIONS.md 05:49).
- **Measured in this note from the try-2 files: the slide excess is the scale factor.** Over-source slide is about (Scale Source factor - 1) × the source's worst slide:

  | Pair | Predicted | Measured |
  |---|---|---|
  | 113_15 RoccoP2 | 0.2347 × 11.71 = 2.75 | 2.73 |
  | 131_01 RoccoP2 | 0.176 × 13.01 = 2.29 | 2.29 |
  | 113_15 Rocco | 1.71 | 1.69 |
  | 131_01 Rocco | 1.19 | 1.19 |
  | 143_18 RoccoP2 | 0.66 | 0.66 |

  Try 1 fits the same way (131_01 RoccoP2: 0.048 × 13.01 = 0.62, measured 0.63). Any uniform scale therefore costs slide on the existing bar, in direct proportion to the factor (see Acceptance).

## 1. What professional pipelines do

**Unreal 5.8 IK Retargeter (engine source and Epic's pages)**
- Pelvis Motion places the target pelvis at the source pelvis position × (target pelvis height / source pelvis height). Both heights come from the retarget poses (PelvisMotionOp.cpp 182-196, 217-226, 323-326). The op reads only the source bone's global transform (294-296). It does not need that bone to be the parent of the legs.
- After scaling, the op applies, in this order: Scale Vertical on the absolute Z, Scale Horizontal about the target's initial position, a static global offset, and a static local offset turned by the pelvis rotation (366-379). PelvisTranslationDelta records what these changes added (385).
- Run IK Rig places each goal at the CURRENT target chain start + the source chain vector × (target rest length / source rest length). Both lengths are straight lines from start to end (RunIKRigOp.cpp 64-80, 113-133). The vertical Affect IK weight decides whether the pelvis changes carry into the goals. With Affect IK Vertical at 0 (its default, PelvisMotionOp.h 111-117) the vertical change is subtracted again (RunIKRigOp.cpp 127-132).
- Blend to Source's Apply Pelvis Offset defaults to 0 (BlendToSourceOp.h 53-56; used at BlendToSourceOp.cpp 71-75).
- Scale Source scales about the component origin unless a pivot bone is chosen (IKRetargetProcessor.cpp 2269-2297; ScaleSourceOp.cpp 9-21). It scales the retarget pose as well (IKRetargetProcessor.cpp 84-89).
- Epic, "Retargeting Operation Stack in Unreal Engine 5.8", https://dev.epicgames.com/documentation/unreal-engine/retargeting-operation-stack-in-unreal-engine-5-8 (read 17 Nov 2026):
  - Pelvis Motion: "translation data is scaled properly between characters of different proportions".
  - Affect IK: "At 0 the IK goals remain at their retargeted position, and at 1 they move relative to the modified pelvis transform".
  - Scale Source works best "placed at the top of the operations stack".
- Epic, "Retargeting Bipeds with IK Rig", https://dev.epicgames.com/documentation/unreal-engine/retargeting-bipeds-with-ik-rig-in-unreal-engine (read 17 Nov 2026):
  - The documented way to change the pelvis's vertical scaling without lifting the body off the floor is to use the scale "together" with "Translation Offset Z", which "lowers the retarget root ... without changing its overall scale".
  - The page names the setting inconsistently (Scale Horizontal in the text, Scale Vertical in the example). The engine code above settles which one acts on Z.
- Epic, "IK Rig Animation Retargeting in Unreal Engine", https://dev.epicgames.com/documentation/en-us/unreal-engine/ik-rig-animation-retargeting-in-unreal-engine (read 17 Nov 2026): the pelvis is defined so that "root motion can be defined and transferred in a proportional way". The page says nothing about hip-joint offsets.

**Autodesk HumanIK** (the MotionBuilder/Maya solver). Maya 2025 help, "HumanIK Retarget Specific attributes", https://help.autodesk.com/cloudhelp/2025/ENU/Maya-CharacterAnimation/files/GUID-EB2A8BB0-801E-4251-8C4C-09986049CCBB.htm (read 17 Nov 2026):
- Hips Level Mode: "When set to Auto, hip height compensation is calculated automatically (default)". Hips Level is "the level of the hips relative to its center of gravity".
- Ankle Height Comp Mode: "Auto mode ensures the feet relate correctly to the floor". It is for when "the scale of your source and target characters differ".
- Action Space Comp Mode, Auto by default: scale compensation, "the higher the value, the longer the character's stride". Match Source on keeps the source's footprints, so a larger character appears "to take tiny steps".
- The page does not say how the hip compensation is computed. **Unverified:** whether HumanIK places the hips from the hip joints or from a centre of gravity.

**Unity Mecanim.** Unity 6.6 manual, "How Root Motion works", https://docs.unity.com/en-us/engine/current/manual/animation-section/animation-mecanim/avatar-creationand-setup/root-motion (read 17 Nov 2026):
- "The Body Transform is the mass center of the character. It is used in Mecanim's retargeting engine and provides the most stable displacement model."
- The body transform and orientation "are the only world-space curves"; feet and hands IK goals "are stored relative to the body transform".
- HumanPose.bodyPosition, https://docs.unity.com/en-us/engine/current/script-reference/unityengine/humanpose/bodyposition (read 17 Nov 2026): "Center of mass of the humanoid", approximated from average body-part masses.
- Animator.humanScale, https://docs.unity.com/en-us/engine/current/script-reference/unityengine/animator/humanscale (read 17 Nov 2026): the scale is "relative to Unity's Default Avatar". **Unverified:** that it is a hips-height ratio. The page does not say so.

**Research practice.** Aberman et al. 2020, "Skeleton-Aware Networks for Deep Motion Retargeting", ACM TOG 39, read at https://ar5iv.labs.arxiv.org/html/2005.05732 (17 Nov 2026):
- End-effector velocities are normalised by "the lengths of the kinematic chains from the root to the end-effector".
- Foot contacts are kept: "frames with zero foot velocity in the input motion should result in zero foot velocity in the retargeted motion".

**Common thread.** Professional pipelines carry the body's translation from a reference point that means the same thing on both bodies: Unity takes the mass centre, never the rig's own hips bone. They scale that translation by a leg-chain measure (Unreal's Run IK Rig, the Aberman paper, HumanIK's Auto action-space compensation). They add a separate floor/ankle term (HumanIK's Ankle Height Compensation, Epic's documented Scale-plus-Translation-Offset-Z). Tries 1 and 2 used the CMU Hips bone as the reference point. That bone means something different on CMU (8 to 9 cm above the hip joints) than on MetaHuman (1 cm below them).

## 2. The chosen method, and why it is different

**Method: a hip-joint-centre pelvis.**
- An offline pre-pass gives each CMU skeleton a bone, HipCentre, keyed every frame at the midpoint of the two hip joints (LeftUpLeg and RightUpLeg heads) and turning with Hips.
- Pelvis Motion reads HipCentre instead of Hips.
- Translation is scaled by the hip-to-ankle chain ratio r: the same ratio Run IK Rig already uses for the leg goals.
- The ankle-height difference is added as one constant floor term, in world Z.

With this setup the pelvis, the world-anchored feet (Blend to Source) and the chain-relative goals all use one scale and one reference point. They no longer pull against each other.

**Why the three parts agree (from the cited code):**
- Run IK Rig puts the ankle goal at thigh + r × (source ankle - source hip) (RunIKRigOp.cpp 133).
- With the target thigh centre at r × (source hip centre) + (0, 0, b), the ankle lands at r × (source ankle) + (0, 0, b).
- So b = a_t - r × a_s puts a planted source ankle (at height a_s) exactly at the target's own ankle height a_t. Here a_t is the target's rest ankle height and a_s is the source ankle height on its own floor.
- Horizontally, Blend to Source puts the foot at Scale Source factor × source ankle. With that factor also set to r, the blended foot and the chain-relative foot are the same point. In try 1 they differed: factor s, pelvis read 8 to 9 cm off the hip joints. That difference is the mechanism the diagnosis gives for the knees.

**How it differs from tries 1 and 2:**

| | Try 1 | Try 2 | This method |
|---|---|---|---|
| Source point read for the pelvis | Hips bone | Hips bone | HipCentre (hip-joint midpoint, keyed per frame) |
| Hip-to-pelvis gap | ignored | fixed WORLD Z offset (wrong under tilt) | carried by the bone itself, so it turns with the pelvis; the target's own 1.1-1.3 cm gap as a LOCAL offset |
| Scale | pelvis/Hips height s | hip-joint HEIGHT ratio (includes the ankle heights) | hip-to-ankle CHAIN LENGTH ratio r (Run IK Rig's own) |
| Floor term | none | folded into the Z offset | separate world Z: a_t - r × a_s (HumanIK's ankle compensation; Epic's Scale + Translation Offset Z) |
| Feet | chain-relative Z, blended XY with factor s | blended XY with factor r_height | blended XY with factor r, consistent with the pelvis |

The change is in the reference point and the scale, not in a tuned number. Try 2's own failure ("a fixed Z offset errs whenever the pelvis tilts") is what the per-frame HipCentre removes.

**Rejected alternatives:**
- Pelvis Motion's floor constraint with crotch offsets (PelvisMotionOp.cpp 336-359). It changes only downward motion, piecewise, so the sit and the rise would scale differently. It is still keyed to the Hips bone.
- Translation Offset Local alone on the Hips bone, no pre-pass. This works mathematically (see the derivation above with o = R_t0^-1 R_s0 × the hip-centre offset). It leaves out LHipJoint/RHipJoint rotation if the BVH keys any (unverified either way). It is also too close to try 2 to count as different.
- Stride Warping and Speed Planting. They act on goals, not on the pelvis, so they do not touch the cause.

## 3. Implementation

**A. Offline pre-pass in tools/meshgen/blender/cmu_clips.py.** Write the output to a new set folder, for example F:/LedgerTools/game-inputs/cmu-2026-11-18-hipcentre, never over cmu-2026-11-17-cm.
1. After the T-pose becomes the rest pose (after pose.armature_apply, line 116), add the edit bone HipCentre:
   - parent Hips, not connected;
   - head at the midpoint of the LeftUpLeg and RightUpLeg heads;
   - tail = head + (Hips tail - Hips head), roll equal to Hips's roll, so its rest orientation is Hips's.
2. Give the stand-in cube a second vertex group, HipCentre (half the vertices). The bone is then skinned and survives the FBX import. **Unverified:** whether Unreal keeps an unskinned leaf bone; this avoids the question.
3. In the re-key loop (lines 177-186), for each stored frame set HipCentre's pose matrix to translation = the midpoint of stored LeftUpLeg and RightUpLeg translations, rotation = stored Hips rotation. Key its location and rotation_quaternion.
4. Record the worst distance between HipCentre's head and the UpLeg midpoint over all frames. Bar: 0.05 cm or less, else stop.
5. Write floor_<subject>.json beside the clips with:
   - a_s = the mean LeftFoot/RightFoot head height (cm) at the source's standing frame, chosen by the measure's own rule (both balls planted, Hips at 97% of standing height or more, straightest knees; reuse cmu_measure's planted() and knee_flex()). This is fix M3: never the T-pose frame.
   - the frame number and the toe heights.

**B. tools/ue/cmu_ue_retarget.py.** Keep everything from try 1 (ankle rig copy, legs One to One, Blend to Source horizontal, feet restored). Then:
1. After the T-pose import, stop if the skeleton lacks HipCentre or the clip set has no floor_<subject>.json. Keep the IK rig's retarget root as Hips: the auto rig, chains and guards stay unchanged. Read this back (review fix 7): with HipCentre present, the auto result, the chains and the retarget root must equal try 1's (its ue_result.json), and no chain may start or end on HipCentre. The matched template's name cannot be read from Python (IKRigController.h 378-388, C++ only), so it is checked through the chains it produces.
2. Compute per pair, in Python:
   - Source retarget-pose positions by forward kinematics with the auto-align deltas, the way restore_source_feet() builds E (local = ref local × delta, IKRetargetProcessor.cpp 77).
   - H_p = HipCentre height in the source retarget pose.
   - L_s = mean over sides of |UpLeg - Foot| in the source retarget pose.
   - From the target RETARGET pose, the pose the op itself reads (PelvisMotionOp.cpp 217-220, GetGlobalRetargetPose; review fix 2), by the same forward kinematics over the body's reference pose with the target's deltas and root offset: L_t = mean |thigh - foot|, H_tp = pelvis height, a_t = mean foot_l/foot_r height, the pelvis position P0 and rotation R0, and the thigh midpoint T0. With no target deltas this equals the body's reference pose; the script records the largest target delta.
   - Both retarget poses' root translation deltas must read zero, else the pair stops (review fix 3): with HipCentre as the op's bone, GetPelvisBone (IKRetargetProcessor.cpp 2230-2241, 1255) hands HipCentre to the pose resolve, which adds that delta to HipCentre alone (56-62).
   - r = L_t / L_s. G = H_tp / H_p. S = r / G.
3. Scale Source: source_scale_factor = r, first in the stack, pivot component origin (read back).
4. Pelvis Motion, through its op controller's get_settings/set_settings:
   - scale_vertical = S, scale_horizontal = S;
   - translation_offset_global = (-P0.x × (1 - S), -P0.y × (1 - S), a_t - r × a_s);
   - translation_offset_local = R0^-1 × (P0 - T0);
   - affect_ik_horizontal = 1, affect_ik_vertical = 1;
   - blend_to_absolute_offset (0,0,0), floor_constraint_weight 0, blend_to_source_translation 0, rotation_alpha 1, translation_alpha 1.
   - Snake-case property names follow the C++ names in PelvisMotionOp.h 30-117. **Unverified** until read back.
5. Blend to Source leg chains: apply_pelvis_offset stays 0 (read back). With S not 1, PelvisTranslationDelta is large, and a non-zero value would drag the foot marks with it.
6. **LAST, after every assign_ik_rig_to_all_ops call:** set_source_pelvis_bone("HipCentre") on the Pelvis Motion controller (PelvisMotionOp.h 280-281), then read get_source_pelvis_bone back.
   - Each IK-rig assign resets the bone to the rig's pelvis (PelvisMotionOp.cpp 151-163).
   - set_settings never copies the bone fields (PelvisMotionOp.cpp 25-36).
7. Write r, G, S, H_p, H_tp, a_t, a_s, b and the local offset per pair into ue_result.json. Any read-back mismatch stops the pair before the batch, as the script's other guards do.

**Expected values** (from analysis.txt section 4 and the reference poses; the script computes the exact ones):

| Pair | r | G | S |
|---|---|---|---|
| 143_18 Rocco | 1.141 | 1.167 | 0.978 |
| 143_18 RoccoP2 | 1.245 | 1.255 | 0.992 |
| 113_15 Rocco | 1.062 | 1.133 | 0.937 |
| 113_15 RoccoP2 | 1.159 | 1.219 | 0.951 |
| 131_01 Rocco | 1.052 | 1.079 | 0.975 |
| 131_01 RoccoP2 | 1.148 | 1.161 | 0.989 |

- b on 113_15 (a_s about 5.06), with a_t the mean of foot_l and foot_r (review fix 6; the diagnosis gives foot_r only: Rocco 9.79, RoccoP2 9.51): about 9.8 - 1.062 × 5.06 = 4.4 cm on Rocco and 9.5 - 1.159 × 5.06 = 3.6 cm on RoccoP2. The script computes the real values from the target retarget pose.
- A pair whose computed r differs from the table by more than 0.01 is a sign of a wrong length read. Check it before the batch.

## Acceptance (on the existing measure, tools/meshgen/blender/cmu_measure.py, unchanged)

**Full pass:** every one of the six pairs PASSES frames, feet_slide_cm (2.0 or less over source), feet_height_cm (2.0 or less worse than source), knees_deg and stand_knee_deg (max(10, source + 3) or less), and limb_flips 0. Method checks besides: HipCentre error 0.05 cm or less; every setting read back.

**Predicted:**
- Slide:
  - Predicted excess = (r - 1) × the source's worst slide: 143_18 0.34 and 0.60, 113_15 0.73 and 1.86, 131_01 0.68 and 1.93 (Rocco and RoccoP2). All six pass, but RoccoP2 on 113_15 and 131_01 pass by only 0.14 and 0.07 cm.
  - This term is the uniform scale itself, not a fault of the method: the try-2 table above confirms it to within 0.03 cm.
  - HumanIK's documented default (Auto action-space compensation: a larger character takes a longer stride) treats this growth as correct. A bar that compares against the unscaled source fails any uniform scale above about 1.15 on these clips.
  - Decided by the session before the run (17 Nov): the slide bar stays as it is; there is no comparison against r × the source's slide. The predicted margins of 0.14 and 0.07 cm on 113_15 and 131_01 RoccoP2 are a known risk: a slide fail there is a new fault and sets the method aside (review fix 4).
- Height: for the ANKLE, by construction 2.0 or less on 6/6. The planted target ankle sits at a_t + r × the source's own error, so the excess is at most (r - 1) × 4.31 = 1.1 cm. The measure also takes the ball's low point (cmu_measure.py 139-151, the foot_ and ball_ bones), which follows the foot's rotation and is not set by the construction: the ball part is unverified (review fix 5). Unverified until the run: the FBIK solver's free root with pre-pull can still move the pelvis.
- Knees: the hip-to-ankle vector becomes r × the source's in all three axes, so per-frame knee flexion should follow the source within the 3-degree bar. Any residual would come from the thigh-to-shin length ratios. Unverified until the run. 131_01's walking frames (target about 30 degrees where the source is at 0 to 6.5 in try 1) are the case to look at first.

**Least result that counts under RULINGS 7 Nov** (each method must close the gap to the bar by a third, with no new fault):
- Try 1 fails 10 of 36 measures (height 3, knees_deg 5, stand_knee_deg 2).
- This method therefore needs 6 or fewer failing measures, with slide still 6/6 and flips still 0.
- If it does worse, it is set aside like the others, and its numbers are listed.

## 4. Mafia: The Old Country and Kingdom Come II

None found. No public source read here says how either game retargets captured motion onto bodies of different proportions.
- Warhorse's "Kingdom Come: Deliverance II Making of: Motion Capture Routine" (https://www.youtube.com/watch?v=OSWSgYfnc64) is listed unread in production/research/aaa-reference/TALKS.md L27: behind the sign-in wall.
- 2K's Mafia developer diaries were opened for combat research (production/research/aaa-reference/COMBAT.md, line 685) and are not about retargeting.
- The earlier claim that both studios retarget their own capture in their own tools is unsourced (CMU-RETARGET-METHOD-REVIEW-2026-11-17.md, line 24).
- Trial against the project's own measure stands in for a reference-game method here.

## Not reached, and not used as evidence

- Gleicher 1998, "Retargetting Motion to New Characters" (https://graphics.cs.wisc.edu/Papers/1998/Gle98/retarget-preprint.pdf): fetched, but the PDF text could not be read with the tools at hand. The old research.cs.wisc.edu address redirects to an error page.
- Hecker et al. 2008, Spore animation paper (http://chrishecker.com/images/c/cb/Sporeanim-siggraph08.pdf): the site answered "temporarily down".
- Autodesk MotionBuilder "Character Retargeting properties" (guid GUID-877F937B-21C2-472F-AA43-0099DBF08B75): "Page Not Found" under 2025 and 2026. The pyfbsdk FBCharacterHipsTranslationMode page was reached but has no value descriptions (only WorldRigid/BodyRigid names).
- DuckDuckGo (bot check) and Google (consent wall) refused automated search; neither was worked round. Bing returned unrelated results.
- Epic's "Retargeting Operation Stack" page for 5.7 returned only a table of contents. The 5.8 page was used.

## Unverified points, collected

- How HumanIK computes its automatic hip compensation (from hip joints, or from a centre of gravity).
- That Unity's humanScale is a hips-height ratio.
- Whether the CMU BVH keys any rotation on LHipJoint/RHipJoint. The per-frame HipCentre makes the method right either way.
- Whether Unreal keeps an unskinned leaf bone on FBX import. The pre-pass skins HipCentre to avoid it.
- The Python property names of the Pelvis Motion settings. They are read back before the batch.
- The knee and height predictions, until one run and the measure.
