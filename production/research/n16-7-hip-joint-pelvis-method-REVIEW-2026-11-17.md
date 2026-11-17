# Review: n16-7 hip-joint pelvis method note (17 Nov 2026)

Reviewed: production/research/n16-7-hip-joint-pelvis-method-2026-11-17.md, against F:/LedgerTools/tool-dev/reports/CMU-RETARGET-FEET-DIAGNOSIS-2026-11-17.md, F:/LedgerTools/tool-dev/runs/cmu-diag-2026-11-17/analysis.txt section 4, the try-1 and try-2 measure files (F:/LedgerTools/game-inputs/cmu-2026-11-17-try1|try2/measure), tools/meshgen/blender/cmu_measure.py, tools/ue/cmu_ue_retarget.py, tools/meshgen/blender/cmu_clips.py, and the installed engine source (C:/Program Files/Epic Games/UE_5.8/Engine/Plugins/Animation/IKRig/Source). Nothing was run in Unreal; no web page was opened; no file but this one was written.

**Verdict: PASS WITH FIXES.**

## 1. Engine claims (installed source; Build.version says 5.8.4, not 5.8.2)

Every cited line was opened and matches what the note says:
- Pelvis Motion: source height and position from the global retarget pose (PelvisMotionOp.cpp 182-196), target height, rotation, position and the global scale factor (217-226); scaled position = source current × target height / source height (323-326); reads only the source bone's global transform (294-296), so the bone need not parent the legs. Order after scaling: Blend to Source translation (365-367), Scale Vertical on absolute Z (371), Scale Horizontal about Target.InitialPosition (372-373), global offset (376), local offset turned by the final rotation (379), Translation Alpha (382); PelvisTranslationDelta (385). Floor constraint only when the source is below its initial height (336-359).
- Reset of the source bone on rig assign: OnAssignIKRig (151-163). SetSettings goes through CopySettingsAtRuntime, which skips both bone fields (25-36, controller 462-465); SetSourcePelvisBone writes the field directly (467-470; header 278-281).
- Affect IK: defaults Horizontal 1, Vertical 0 (PelvisMotionOp.h 107-117). Run IK Rig subtracts PelvisTranslationDelta × (1 - weight) from the current target chain start, goal = start + source vector × (target rest length / source rest length), both straight start-to-end lengths (RunIKRigOp.cpp 64-80, 113-133).
- Blend to Source: Apply Pelvis Offset default 0 (BlendToSourceOp.h 53-56), used at BlendToSourceOp.cpp 71-75; the blended location is the scaled source end bone (70).
- Scale Source: pivot zero for ComponentOrigin (IKRetargetProcessor.cpp 2269-2297; ScaleSourceOp.cpp 9-21); the resolved retarget pose is scaled too (84-89), and it is reloaded with the current factor and the ops re-initialised when the factor changes (2140-2164, 2168-2228). The batch export scales the input pose before each frame (IKRigEditor IKRetargetBatchOperation.cpp 522).

## 2. Offset algebra (cm, Z up, component space)

Correct and consistent with the code. Because the source retarget pose is scaled by the same factor r as the live pose, the op's normalisation is scale-free: PositionScaled = G·p (p = raw HipCentre, G = H_tp/H_p). Then Z: G·p.z·S = r·p.z; XY: P0(1-S) + r·p.xy, so the global offset -P0.xy(1-S) leaves r·p.xy; plus (0,0,b) and Rotation·R0⁻¹(P0-T0) = RotDelta·(P0-T0). The target hip midpoint therefore lands at r·p + (0,0,b). Run IK Rig: source vector r·v × L_t/(r·L_s) = r·v, so a planted ankle at a_s lands at r·a_s + b = a_t. This needs Affect IK 1/1, which the note sets, and Apply Pelvis Offset 0, which it keeps. Expected r, G and S reproduce from analysis.txt section 4 (for example 143_18 Rocco: 1.141, 92.8/79.6 = 1.166, 0.978).

Known limits, narrow: the derivation is exact for the hip midpoint only; each leg differs by RotDelta·((thigh0 - T0) - r·(UpLeg0 - HC0)), whose vertical part appears only under pelvis roll (millimetres). The FBIK free root with pre-pull may still move the pelvis, as the note says.

## 3. Different from tries 1 and 2

Yes, within RULINGS 7 Nov's "genuinely different": the reference point changes (a per-frame hip-joint midpoint, not the Hips bone), the scale changes (the leg-chain ratio Run IK Rig itself uses, shared by Scale Source, Pelvis Motion and Blend to Source), and the floor term comes from the source's planted standing frame, not a fixed world Z. The engine knobs overlap with try 2 (Scale Source, Pelvis Motion scales, global Z offset, Affect IK 1/1); the note says so and rejects the local-offset-only variant as too close.

## 4. Acceptance numbers

From the unchanged measure: try 1 fails 10 of 36 (height 3, knees_deg 5, stand_knee_deg 2) and try 2 fails 13, both recounted here from the measure files; "6 or fewer, slide 6/6, flips 0" is the one-third rule. The slide model checks out: try 2's 113_15 RoccoP2 excess is 14.44 - 11.71 = 2.73, and the predicted (r - 1) × source excesses are arithmetically right. The note still says the slide bar is "for the session to settle BEFORE the run". The session has settled it (bar unchanged), so the note must say so (fix 4).

## 5. Sources

Engine files and project files cited are real and say what the note claims. TALKS.md "L27" is an item label (line 135), unread behind sign-in, as stated; COMBAT.md 685 and the method review's line 24 match. The Epic, Autodesk, Unity and ar5iv pages were not re-opened by this reviewer (no web reader used), so their quotes rest on the note's dated reads. The unreached list (Gleicher, Hecker, MotionBuilder page, refused search engines, Epic 5.7 page) is properly kept out of the evidence.

## Fixes (each one line)

1. Say the engine is 5.8.4 (Build.version PatchVersion 4); the cited lines were checked against it and hold.
2. Take P0, R0, T0, H_tp and a_t from the target retarget pose the op uses (PelvisMotionOp.cpp 217-220 read GetGlobalRetargetPose), or assert that pose equals the reference pose for pelvis and thighs, since the -P0(1-S) cancel and the local offset depend on it.
3. Read back that the source retarget pose's root translation delta is zero: with HipCentre as the op's bone, GetPelvisBone (IKRetargetProcessor.cpp 2230-2241, 1255) hands HipCentre to the pose resolve, which adds that delta to HipCentre alone (56-62).
4. Replace "for the session to settle" with the decision: the slide bar stays, so the predicted margins of 0.14 and 0.07 cm on 113_15 and 131_01 RoccoP2 are a known risk, and a slide fail there is a new fault that sets the method aside.
5. Narrow "height by construction" to the ankle: the measure also takes the ball's low point (cmu_measure.py 139-151, foot_ and ball_), which follows the foot's rotation; mark the ball part unverified.
6. Expected-values line: a_t is 9.79 for Rocco (foot_r in the diagnosis) but 9.33 for RoccoP2 (diagnosis foot_r 9.51); state both as means of foot_l and foot_r, or correct them (the script computes the real values).
7. Add a read-back that the auto-characterised source rig (template, chains, retarget root Hips) is unchanged with the extra HipCentre bone present; "the auto rig stays unchanged" is otherwise unverified.

Observation, not a fault of the note: the working copy already holds an uncommitted cmu_clips.py change behind LEDGER_CMU_HIPCENTRE=1 that follows section 3A (bone, skinning, per-frame keys, its own error check).
