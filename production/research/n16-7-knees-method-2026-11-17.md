Method researched: Unreal 5.8.4 engine source (FKChainsOp.cpp, RunIKRigOp.cpp, BlendToSourceOp.cpp, OffsetGoalsOp.cpp, IKRetargetProcessor.cpp, IKRetargeterPoseGenerator.cpp, PBIKSolver.cpp/.h, PBIKBody.cpp, PBIKConstraint.cpp), Autodesk HumanIK Retarget Specific attributes, Epic's Retargeting Operation Stack 5.8 and Retargeting Bipeds pages, the hip-joint try's own tracks and measure files

# n16-7 "CMU knees": what keeps the target knee bent, and one fix (research note, 17 Nov 2026)

Item n16-7 (people alive), known shortfall after the hip-joint-centre method: target knees stay bent where the CMU source stands near straight. 131_01 on both bodies (Rocco 22.9, RoccoP2 18.2 degrees against a source at 0 to 6.5) and 113_15 Rocco's later stand; 143_18 Rocco fails the same way by smaller margins. This is research only. Nothing was run in Unreal and no project file was changed apart from this note and its catalogue line. Everything below was read on 17 Nov 2026. Engine paths are relative to C:/Program Files/Epic Games/UE_5.8/Engine/Plugins (IKRig = Animation/IKRig/Source/IKRig, PBIK = Experimental/FullBodyIK/Source/PBIK). Project numbers come from:
- F:/LedgerTools/game-inputs/cmu-2026-11-18-hipcentre: ue/ue_result.json and ue/fbx/*.track.json;
- F:/LedgerTools/game-inputs/cmu-measure-gate-2026-11-17/new-hipcentre/*.json (the fixed-gate measure);
- F:/LedgerTools/tool-dev/runs/cmu-diag-2026-11-17/probe_result.json (the IK rig settings and the reference poses).

Hand arithmetic on those numbers is marked as computed here.

## Questions

1. What in the leg chain keeps a target knee bent when the source knee is near straight? Candidates: One to One FK, the ankle goals, the IK rig's solver settings (root, reach, preferred knee angle, pole), thigh-to-shin proportions, Blend to Source.
2. Why did three different pelvis setups move these knees by under 0.4 degrees?
3. Does the thigh-to-shin ratio matter? How do professional retargeters handle leg proportions (HumanIK/MotionBuilder, Unreal's own docs, papers)?
4. What one candidate fix, genuinely different from the pelvis work, follows? With what exact settings?
5. What numbers must it reach on the unchanged measure (tools/meshgen/blender/cmu_measure.py)?
6. How do Mafia: The Old Country and Kingdom Come II do it, if any public source says?

## Short answer

- **The pelvis cannot reach these knees.** Run IK Rig places each foot goal relative to the target thigh's current position, after the pelvis has moved. With Affect IK at 1 (both later tries) nothing is subtracted (IKRig/Private/Retargeter/RetargetOps/RunIKRigOp.cpp 127-133). Moving the pelvis moves the goal by the same amount, so the hip-to-goal distance, and with it the knee, does not change.
- **Cause K1: Rocco's own reference knee is carried into every frame** (143_18 Rocco, 113_15 Rocco). One to One FK applies the source bone's rotation change, measured from the source's retarget pose, to the target bone's own retarget rotation (IKRig/.../FKChainsOp.cpp 295-307 and 343-351).
  - So the target's FK knee equals the source knee plus the target's reference-pose knee bend, minus the source's retarget-pose bend.
  - The measure reads the rest knees as Rocco 4.9, RoccoP2 1.0 and the CMU sources 0.0 degrees (rest_knees_deg in every new-hipcentre measure file).
  - The PBIK solve then barely straightens a knee (section 2), so the 4.9 degrees survive. 143_18 Rocco: target 17.5 where the source is 12.6, and 12.6 + 4.9 = 17.5.
- **Cause K2: the hip-width mismatch under Blend to Source, in wide stances** (131_01, both bodies).
  - Blend to Source sets each foot goal's X and Y to the scaled source ankle in world space (IKRig/.../BlendToSourceOp.cpp 64-83).
  - The target's hip joints sit further out than r times the source's: Rocco 3.90 cm and RoccoP2 2.52 cm per side on 131_01.
  - 131_01 ends in a wide stance, with Rocco's feet 31 and 24 cm outside the hip joints. In that stance the world-placed goal falls about 1.5 cm closer to the hip than the leg's normalised length asks for (computed here). The knee has to bend.
- **Thigh-to-shin ratio: not a cause.** Under Unreal's normalised hip-to-goal distance, the knee angle depends on the ratio only through ab/(a+b)^2. Between the bodies here (0.89 to 1.05) that term changes by under 0.2% (section 3).
- **Candidate fix: "leg correspondence"** (section 5).
  - (A) Bend the source's retarget-pose knee to match each target's reference knee (Rocco 4.9, RoccoP2 1.0 degrees), in the target's bend plane. This is Epic's own checklist item, "Make sure both characters have matching reference poses".
  - (B) Space the feet to the target's hips, as HumanIK's default Feet Spacing Mode does. An Offset Goals op under Run IK Rig, after Blend to Source, pushes each foot goal out by Δw = target half hip width - r × source half hip width, in the foot goal's own frame.
  - Nothing in the fix touches the pelvis.

## 1. Why three pelvis setups left the knees alone (engine, proved by the code)

- The goal position is CurrentTargetStartLocation + source chain direction × (current source chord / source retarget chord) × target retarget chord (RunIKRigOp.cpp 118-133).
- CurrentTargetStartLocation is the target thigh in the pose after Pelvis Motion and FK. Only the part of the pelvis change NOT passed on by Affect IK is subtracted (InvRootModification, lines 127-132). Try 2 and the hip-joint try set Affect IK to 1 and 1, so nothing is subtracted.
- Try 1 kept Scale and offsets neutral, so its pelvis translation offset was zero anyway (PelvisMotionOp.cpp 366-385, cited in n16-7-hip-joint-pelvis-method-2026-11-17.md).
- So in all three tries the hip-to-goal distance is set by the source chain and the two retarget chords alone. The diagnosis's observation (knees within 0.1 to 0.4 degrees across three pelvis placements) is what the code predicts.
- Any knee fix has to act on one of four things: the chords, the goal's X and Y (Blend to Source), the FK input pose, or the solve.

## 2. What sets the knee

### K1: the target's reference knee rides on One to One FK

- **Engine.** In One to One mode, the "current" and "initial" source transforms are the source chain's current and retarget-pose globals for the same chain index (FKChainsOp.cpp 295-307). The output is RotationDelta × TargetInitialRotation, where TargetInitialRotation is the target's retarget-pose global (343-351).
  - When the source's thigh and shin turn together (no change of the source knee), the target keeps its own retarget-pose knee.
  - The target retarget pose is the body's reference pose: the run read back target_pose_largest_delta_deg 0.0 on all six pairs (ue_result.json).
- **Bodies** (positions from probe_result.json B_ref, lines 5610-5793; angles computed here, and they agree with the measure's rest_knees_deg):

  | Body | thigh cm | shin cm | thigh/shin | reference knee |
  |---|---|---|---|---|
  | Rocco | 41.40 | 42.98 | 0.963 | 4.9 deg (shin slopes 4.7 deg back from the thigh) |
  | RoccoP2 | 47.19 | 44.81 | 1.053 | 1.0 deg |
  | CMU 143_18 / 113_15 / 131_01 T-pose | 34.88 / 37.77 / 41.11 | 39.01 / 41.60 / 39.04 | 0.89 / 0.91 / 1.05 | 0.0 deg |

- **Fit to the failures** (target = source knee + reference knee where the goal does not force a bend; the fixed-gate measure files):

  | Pair, check | source | target | source + reference knee |
  |---|---|---|---|
  | 143_18 Rocco, knees_deg (frame 169 r) | 12.6 | 17.5 | 17.5 |
  | 143_18 Rocco, stand r (frame 8) | 17.3 | 21.3 | 22.2 |
  | 143_18 Rocco, stand l (frame 8) | 22.8 | 24.7 | 27.7 |
  | 113_15 Rocco, stand l | 33.4 | 37.7 | 38.3 |
  | 143_18 RoccoP2, knees_deg | (passes, 14.3) | | +1.0 only |

- **Hip-to-ankle check** at 143_18's last frame (186, left leg, computed here from the two track files):
  - Rocco's thigh-to-foot distance is 82.99 cm, 0.984 of its retarget chord (84.308). RoccoP2's is 90.90 cm, 0.989 of 91.912.
  - The same source asks for the same fraction on both bodies, and the Blend to Source sideways term differs between them by under 0.1%.
  - The 0.46% gap (about 0.4 cm) is what a knee about 4 degrees more bent gives at 19 degrees (chord change about 21 cm × sin 19° × 0.07 rad).
  - So Rocco's foot reaches its goal with the knee left near its FK value, and the leg is shorter than the goal distance asks.
- **Why the solve does not straighten it** (reading of the code; unverified by a run):
  - (a) PBIK body masses are the bone lengths in cm × MassMultiplier (0.31 in IK_MH_IKRig) × 100 (PBIKBody.cpp 77, 84-90). Rotational pushes are scaled by that inverse mass (PBIKBody.cpp 123-135). For example, Rocco's calf body is about 1,330 units, inverse mass about 0.00075.
  - (b) A pin moves its body straight onto the goal, times OverRelaxation 1.3, with no mass factor (PBIKConstraint.cpp 309-328). Joint corrections are shared by inverse mass (PBIKConstraint.cpp 28-68).
  - (c) The rig's root is Free and the pelvis has PositionStiffness 0 and no goal (probe_result.json lines 5591 and 5599; PBIKSolver.h 168-173). So after the sub-iterations, which lock everything outside the leg chains (PBIKSolver.cpp 565-589), the main iterations can meet a farther goal by moving bodies, the pelvis included, instead of turning the knee straight.
  - (d) Preferred angles act only when a limb is squashed, never when it is stretched (PBIKSolver.cpp 155-161).
  - The 113_15 Rocco gate miss fits this. In the source's late stand the target pelvis reaches only 96.9% of its height (89.9 of 92.8 cm).

### K2: Blend to Source places the feet for narrower hips (131_01)

- **Engine.** Blend to Source lerps the goal's X and Y to the raw source end-bone location, already scaled by Scale Source. Apply Pelvis Offset is 0 here (BlendToSourceOp.cpp 64-83). The goal Z stays chain-relative (axes 1, 1, 0 in cmu_ue_retarget.py BLEND_AXES).
  - The hip-joint pelvis puts the target's thigh MIDPOINT at r × the source hip-joint midpoint. Each thigh then sits w_t from that point, against r × w_s for the source.
  - So every world-placed foot goal is offset by Δw = w_t - r × w_s toward the body's middle, relative to what the source's leg vector asks.
- **Sizes** (half hip widths: target from B_ref thigh_l x, Rocco 11.12 and RoccoP2 10.42 cm; source from the probe's T-pose UpLeg x, 8.69 / 8.58 / 6.86 cm; r from ue_result.json):

  | Pair | r | Δw (cm) | knee checks |
  |---|---|---|---|
  | 143_18 Rocco | 1.144 | +1.17 | fail |
  | 143_18 RoccoP2 | 1.248 | -0.43 | pass |
  | 113_15 Rocco | 1.066 | +1.97 | fail |
  | 113_15 RoccoP2 | 1.162 | +0.45 | pass |
  | 131_01 Rocco | 1.053 | +3.90 | fail (22.9) |
  | 131_01 RoccoP2 | 1.152 | +2.52 | fail (18.2) |

- **The stance decides the sign.** On 143_18 the feet stand 1.8 to 5.4 cm INSIDE the hip joints (computed here at frame 186). There a positive Δw lengthens the hip-to-goal line slightly (about 0.07 cm), so K2 is not what bends those knees; K1 is.
- **131_01's end is a wide stance.** At frame 246 Rocco's left foot is 31.0 cm and the right 24.3 cm outside the hip joints. The left knee is 17.2 degrees and the hip-to-ankle 83.43 cm, against 84.38 cm thigh plus shin (computed here from the track).
  - With the goal at the leg-relative place (lateral 31.0 + 3.9 cm), the same leg vector would measure about 84.96 cm, beyond full reach, so the knee would be straight like the source's.
  - Blend to Source therefore costs about 1.5 cm of reach.
  - A goal closer than the FK foot is a squash. PBIK then pre-bends the knee by its preferred angle (calf Z 90 degrees) × CircularEaseOut(squash fraction) before solving (PBIKSolver.cpp 135-218; PBIKSolver.h 25). CircularEaseOut is sqrt(2x - x²), so the pre-bend climbs steeply: 0.1% squash gives 4.0 degrees, 0.5% gives 9.0, 1% gives 12.7 and 2% gives 17.9 (computed here).
  - The squash fraction is measured from the thigh BODY's centre, the mid-thigh (PBIKBody.cpp 84-93; PBIKSolver.cpp 110-121).
- **Unverified:**
  - The frame-by-frame size at frame 202, the measured worst frame (only frame 246 was read by hand).
  - That RoccoP2's 18.2 follows the same arithmetic. A rough check with a 15-degree leg slope gives a RoccoP2-to-Rocco knee ratio of 0.77, against 0.79 measured.

### The other named candidates

- **Ankle goals.** They are already on foot_l/r with matching source chain ends. Goal rotation is pinned only at output (PBIKSolver.cpp 351-362). The pin itself acts on position only (PBIKConstraint.cpp 309-328), so the foot's rotation goal does not bend the knee. Not a cause.
- **Pole / knee direction.** The bend direction is right (forward). The fault is the size of the bend. Epic's Align Pole Vector op is for direction ("Ensures the joints in a target character's limb bend the same direction as the source animation", Epic op-stack page below). Not a cause.
- **Reach.** bAllowStretch is False. The effector clamp applies only when the root is pinned (PBIKSolver.cpp 75-81). With a Free root, a goal beyond reach drags the pelvis rather than bending the knee. Not a cause of bent knees.
- **Interpolated FK.** It was set aside for the foot flips (diagnosis section 1). It would share K1, because Interpolated also applies deltas to the target's own retarget rotations (FKChainsOp.cpp 284-293, 343-351).

## 3. Thigh-to-shin ratio, and how professionals handle proportions

- **Derivation** (computed here):
  - For a two-bone leg with thigh a, shin b and knee flexion θ: d² = a² + b² + 2ab cos θ, so (d/(a+b))² = 1 - 4q(1 - cos θ), with q = ab/(a+b)² = ρ/(1+ρ)² for ρ = a/b.
  - Run IK Rig keeps d / retarget chord equal on both bodies (RunIKRigOp.cpp 64-80, 118-133). So q_t(1 - cos θ_t) ≈ q_s(1 - cos θ_s), apart from the retarget-pose bends.
  - For ρ from 0.89 to 1.05, q runs from 0.2495 to 0.2499: under 0.2% difference, a few hundredths of a degree.
  - FK copies rotations and ignores lengths. **The ratio is not a cause here.**
  - What the normalisation does carry is the retarget-pose bend: θ_t² ≈ θ_s² - θ_s0² + θ_t0² near straight. With the source at 0 and Rocco at 4.9 that adds at most about 1 degree at a 12.6-degree source knee (computed here). K1's FK term is the larger one.
- **Autodesk HumanIK** (Maya 2025 help, "HumanIK Retarget Specific attributes", https://help.autodesk.com/cloudhelp/2025/ENU/Maya-CharacterAnimation/files/GUID-EB2A8BB0-801E-4251-8C4C-09986049CCBB.htm, read 17 Nov 2026 through a reader that returns short verbatim excerpts):
  - Feet Spacing Mode: "By default, Auto mode adjusts the distance between your target character's left and right ankles."
  - Ankle Height Comp Mode: "By default, Auto mode ensures the feet relate correctly to the floor."
  - Knee Max Extension: "damp the leg as it fully extends, to prevent knee and limb snapping".
  - Knee Compression: at full effect "the leg doesn't bend and instead pushes the character's hips" (paraphrase by the reader).
  - Reach: "At 100%, the body part of a character reaches fully toward the body part of the source."
  - Match Source on makes a larger character "take tiny steps".
  - So HumanIK's defaults space the target's ankles to its own body (K2's remedy) and treat knee-versus-hips as a setting. **Unverified:** how Auto computes the spacing (the page does not say).
- **Epic** ("Retargeting Bipeds with IK Rig", https://dev.epicgames.com/documentation/unreal-engine/retargeting-bipeds-with-ik-rig-in-unreal-engine, read 17 Nov 2026): "Make sure both characters have matching reference poses." If they differ, "you will need to adjust one of their retarget poses so they match". That is K1's remedy. The same page's biped example puts Limb IK solvers rooted at the thigh on the feet goals.
- **Epic** ("Retargeting Operation Stack in Unreal Engine 5.8", https://dev.epicgames.com/documentation/unreal-engine/retargeting-operation-stack-in-unreal-engine-5-8, read 17 Nov 2026):
  - One to One: "Each bone in the source chain is copied to the equivalent bone in the target chain".
  - Offset Goals, Local Translation Offset: "Applies a local-space translation offset to the IK goal."
  - Chain Position Alpha: "Retargets the goal position based on the source length and direction."
  - The page has no text on knees or leg proportions beyond Pelvis Motion and pole alignment.
- **Auto-align.** The script's auto-align (ChainToChain) turns each source bone so that its chain tangent matches the target's at the same chain parameter (IKRigEditor/Private/RetargetEditor/IKRetargeterPoseGenerator.cpp 141-146, 253-257). **Unverified:** whether that reproduces the target's 4.9-degree knee on the CMU source. The fit in section 2 (target = source + 4.9 on Rocco, + 1.0 on RoccoP2) says it does not.
- **Papers:** none read in full; see Unreached.

## 4. Mafia: The Old Country and Kingdom Come II

None found. No public source read says how either game retargets captured motion onto other proportions. This note did not search again; n16-7-hip-joint-pelvis-method-2026-11-17.md section 4 records the search, and Warhorse's motion-capture video sits behind a sign-in. HumanIK's documented defaults and Epic's checklist stand in as the professional method.

## 5. Candidate fix: leg correspondence (no pelvis change)

Both parts go in tools/ue/cmu_ue_retarget.py and act per pair from the retarget poses, as the hip-joint values already do. Everything from the hip-joint method stays: ankle rig copy, legs One to One, Scale Source r, Blend to Source on X and Y, feet restored, HipCentre pelvis.

**A. Match the knee bend in the retarget poses (fixes K1).** New step right after auto_align_all_bones(SOURCE) (line 649) and before the first hip_centre_values call (line 659), so both hip-joint reads and their equality guard see it. For each side:
1. Target (the retarget pose, by fk_retarget over MH_LEG_CHAIN): u_t = unit(calf - thigh), v_t = unit(foot - calf), α_t = angle(u_t, v_t) (expected Rocco 4.9, RoccoP2 1.0 degrees), bend axis n_t = unit(u_t × v_t).
2. Source (the retarget pose after auto-align, fk_retarget over CMU_FOOT_PARENTS + Foot): u_s = unit(Leg - UpLeg), v_s = unit(Foot - Leg).
3. Wanted shin direction: v* = u_s turned by α_t about n = unit(n_t - (n_t·u_s)u_s). World turn W = FindBetween(v_s, v*).
4. New local delta for LeftLeg/RightLeg: D' = Qg⁻¹ · E(parent)⁻¹ · W · E(Leg) · Qg. This uses the script's own convention: E(c) = E(p) Qg D Qg⁻¹, local = ref local × delta (IKRetargetProcessor.cpp 77-79, as restore_source_feet). Write D' with set_rotation_offset_for_retarget_pose_bone(..., SOURCE).
5. Read back: the source retarget knee equals α_t within 0.1 degree and its axis lies within 5 degrees of n_t, else the pair stops.

restore_source_feet then runs unchanged. It reads the Leg's new turn, so the feet still end at their T-pose orientation.

- **Effect:** the source knee's One to One delta is now measured from a pose bent like the target's, so the target's FK knee equals the source knee (FKChainsOp.cpp 343-351). The two chords now describe the same bend, so Run IK Rig's goal asks for the same knee (θ_s0 = θ_t0 in section 3).
- **Side effect:** L_s shortens by about 0.18% on Rocco and 0.01% on RoccoP2, so r and the Scale Source factor grow by the same amount. EXPECTED_R checks r_ref from the reference pose, which is unchanged. Record α_t, the source knee before and after, L_s and r per pair in ue_result.json.

**B. Space the feet to the target's hips (fixes K2).**
1. From the retarget poses: w_t = half the horizontal distance thigh_l to thigh_r (target); w_s = half the horizontal distance LeftUpLeg to RightUpLeg (source, before scaling); Δw = w_t - r × w_s. Expected: 143_18 +1.17 / -0.43, 113_15 +1.97 / +0.45, 131_01 +3.90 / +2.52 (Rocco / RoccoP2).
2. Lateral unit L = unit(horizontal(thigh_l - thigh_r)) in the target retarget pose. World offsets: left +Δw·L, right -Δw·L.
3. Local offsets: v_s = Q_foot_s⁻¹ · offset_s, where Q_foot_s is the target foot_s retarget-pose global rotation. At rest the goal's rotation is exactly that (RunIKRigOp.cpp 139-154, source delta identity), and Offset Goals turns the local offset by the goal's current rotation (OffsetGoalsOp.cpp 64-75).
4. Add "/Script/IKRig.IKRetargetOffsetGoalsOp" (FIKRetargetOffsetGoalsOp, OffsetGoalsOp.h 96-131):
   - parent Run IK Rig (set_parent_op_by_name);
   - moved to a stack index AFTER Blend to Source. Children run in stack order (IKRetargetProcessor.cpp 1528-1535, 1652-1659); before Blend, its X and Y would be overwritten.
5. Op settings: alpha 1, translation_alpha 1, rotation_alpha 1. Chains LeftLeg and RightLeg: alpha 1, local_translation_offset v_s, global_translation_offset (0, 0, 0), rotation offsets zero. All other chains keep zero offsets.
   - Snake-case names follow OffsetGoalsOp.h 30-69. **Unverified** until read back; any mismatch stops the pair.
6. Re-run assign_ik_rig_to_all_ops before setting the chains, as the script does for Blend to Source. The HipCentre pelvis bone stays the LAST setting.

- **Why in the foot's frame and not the pelvis's:** a planted foot keeps its rotation, so the offset stands still while the pelvis turns over it. Added slide is Δw × the foot's own yaw change within a planted span, not the pelvis's.
- **Residual:** Δw × the foot's toe-out change relative to the pelvis, which falls fore-and-aft. Unverified size; at 15 degrees of extra toe-out on 131_01 Rocco it is about 1 cm fore-aft and under 0.2 cm of reach (computed here).

**Rejected alternatives:**
- Blend to Source off (fully leg-relative goals): this removes K2, but the HipCentre pelvis then drags each foot by Δw × the pelvis's turn. 131_01 RoccoP2's slide margin is 0.02 cm.
- Pre-widening the source hips in cmu_clips.py: per-body clip sets, and the same pelvis-turn slide.
- RootBehavior PinToInput: it stops the pelvis sinking, but it clamps goals at full reach (PBIKSolver.cpp 75-81) and leaves K1's FK bend in place.
- Calf preferred angle lowered from 90: tuning without a reference; kept as the named risk below.

## 6. Acceptance, on the existing measure (cmu_measure.py with the fixed 97% gate, otherwise unchanged)

**Full pass:** all six pairs pass:
- frames;
- feet_slide_cm (2.0 or less over source);
- feet_height_cm (2.0 or less worse than source);
- knees_deg and stand_knee_deg (max(10, source + 3) or less);
- limb_flips 0.

Method checks besides: every setting above read back; the source retarget knee within 0.1 degree of α_t; Offset Goals after Blend to Source in the stack.

**Predicted for today's seven failures** (computed here; unverified until the run):

| Check | now | predicted | basis |
|---|---|---|---|
| 143_18 Rocco knees_deg (bar 15.6) | 17.5 | about 12.6 to 13.5 | K1 removed |
| 143_18 Rocco stand_knee_deg (bar 20.3, r) | 21.3 | about 17.3 to 18 | K1 removed |
| 113_15 Rocco knees_deg (gate 96.9%) | n/a FAIL | gate opens, value about 32 to 33 (bar 35) | about 1 cm less sink at a 33-degree knee: about 98% of standing height |
| 113_15 Rocco stand_knee_deg (bar 36.4) | 37.7 | about 33.4 to 34 | K1 removed |
| 131_01 Rocco knees_deg (bar 10) | 22.9 | under 10 | about 1.5 cm reach restored; FK equals the source (0 to 6.5) |
| 131_01 RoccoP2 knees_deg (bar 10) | 18.2 | under 10 | same, Δw 2.52 |
| 113_15 Rocco feet_height_cm | 2.84 | still FAIL | the ball's pitch, untouched by this fix |

**Least result that counts** (RULINGS 7 Nov, a third of the gap closed with no new fault):
- The current default fails 7 of 36, so the fix needs **4 or fewer** failing (unless the session rules otherwise).
- Slide must stay 6/6, flips 0, height no worse than 5/6, and no check that passes today may fail.
- Predicted: 1 failing.

**Named risks:**
- **131_01 RoccoP2 slide** is 1.98 against 2.0. Part B adds Δw (2.52) × that foot's yaw change in its worst span: 0.5 degree of yaw is enough to fail. Part A adds about 0.001 cm. 113_15 RoccoP2 (1.88, Δw 0.45) is safer.
- **Squash pre-bend.** With FK and goals now agreeing, small leftover squashes still pre-bend the knee steeply (0.1% gives about 4 degrees). Standing knees at a source of 0 may land at 4 to 8 degrees, under the 10 bar but close.
- **113_15 Rocco's gate** depends on the pelvis rising about 1 cm; unverified.

**What would confirm the causes cheaply, before or with the run (no Unreal needed for the first):**
1. Read-only, on the existing tracks and source clips in Blender: target knee minus source knee over all frames where the source stands. Expected: about +4.9 on Rocco and +1.0 on RoccoP2 on 143_18/113_15, and a larger value only in 131_01's wide stance.
2. In the run itself, write per pair: α_t, the source knee before and after step A, Δw, and the Offset Goals settings read back.

## Unreached, not used as evidence

- Kulpa, Multon, Arnaldi 2005, "Morphology-independent representation of motions" (Computer Graphics Forum), https://onlinelibrary.wiley.com/doi/10.1111/j.1467-8659.2005.00859.x: HTTP 403, not worked round.
- Not retried here, unreached on 17 Nov per the hip-joint note: Gleicher 1998 (PDF unreadable); Autodesk MotionBuilder "Character Retargeting properties" (Page Not Found); Warhorse's KCD2 motion-capture video (sign-in).

## Unverified points, collected

- That the PBIK solve, rather than the goals, leaves Rocco's knee at its FK value. This is a reading of PBIKBody.cpp 77/123-135, PBIKConstraint.cpp 28-68/309-328 and PBIKSolver.cpp 155-161/565-604, backed by the fit in section 2, not by a run.
- That auto-align leaves the CMU knee straight. The fit says so. One open number does not fit: the hip-joint run's L_s for 143_18 (73.665 cm) is 0.22 cm shorter than the diagnosis's T-pose bone lengths (73.889). Step A's read-back records the source retarget knee directly.
- The 131_01 reach arithmetic, checked at frame 246 only (the worst frame is 202).
- How HumanIK computes Auto feet spacing.
- The Python names of the Offset Goals op class and settings, read back before the batch.
- All predicted acceptance values.
