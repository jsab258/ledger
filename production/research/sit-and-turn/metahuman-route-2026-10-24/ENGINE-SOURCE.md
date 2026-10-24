# Planted feet through the IK Retargeter: what the installed engine says (24 October 2026)

Question 3 of QUESTIONS.md, read in the installed Unreal Engine 5.8 source on 24 October 2026. Nothing was run; no editor, game or build. No web page was used. Every claim below cites a file and line in the installed engine. Facts about the sample's own assets come from reading the bytes of the `.uasset` files in `ue-probe/Content` (their name tables and tagged property values, decoded by an inline script, read only). Those facts are marked **(asset bytes)**. They have not been seen in the editor.

Path short forms:
- `E` = `C:/Program Files/Epic Games/UE_5.8/Engine`
- `IKR` = `E/Plugins/Animation/IKRig/Source/IKRig`
- `RT` = `IKR/.../Retargeter/RetargetOps` (Public `.h`, Private `.cpp`)

---

## Short answers

**1. How the retargeter places a target foot.**
- In 5.8 the old "Retarget IK Goals" op is deprecated (`IKChainsOp.h:199`). Its jobs are split across child ops of **Run IK Rig**: Blend to Source, Offset Goals, Scale Goals, Speed Plant, Stride Warp and Floor Constraint.
- **Base goal.** Run IK Rig sets each foot goal to the *target's* current thigh position plus the source's thigh-to-foot vector. That vector is scaled by **leg-chain length ratio** L = (target thigh-to-foot length) / (source thigh-to-foot length), both measured in the retarget poses.
- **Pelvis.** The target thigh rides on the target pelvis. Pelvis Motion places the pelvis at the source pelvis position (component space) times **pelvis-height ratio** k = target pelvis height / source pelvis height. The horizontal axes are scaled by k too.
- **Root.** Root motion and "Globally Scaled" FK translation also use k.
- **No world space.** The retargeter never sees world space. Only component-space poses go in.
- **The sample's own retargeters** (`RTG_UEFN_to_Metahuman_nrw` and `_ovw`, asset bytes) **override the leg goals with Blend to Source = 1 on all three axes.** The MetaHuman's foot goal is therefore placed exactly on the mannequin's foot bone in component space.
- **Planting ops in the sample:** Speed Planting is present but inert (no speed curve named). Scale Goals, Stride Warping and Floor Constraint are absent. Pole Vector Alignment is on for both legs.

**2. Can a still source foot give a moving target foot?**
- **Default goal (no Blend to Source):** yes. On a capsule-driven character, the target foot's world velocity is about (1 − L)·v_capsule + (k − L)·v_pelvis(component), where v_pelvis(component) is the source pelvis velocity in component space. It is zero only when L = 1 and k = L.
- **With the sample's Blend to Source = 1:** the target foot goal is fixed whenever the source foot is fixed. It can still move if:
  - the IK cannot reach the goal;
  - the source pose arrives stale or a frame late;
  - the two meshes do not share one component frame;
  - Apply Pelvis Offset passes on a horizontal pelvis change;
  - a later op or node moves the foot.
- **Root motion versus pelvis motion:** the retargeter only knows component-space positions. With capsule movement, a world-planted foot slides backwards through component space at capsule speed. Any op that *scales* component-space foot positions turns that into world slide. Copying the source position 1:1 (Blend to Source) does not.
- **Pelvis translation scale:** it moves the feet only through Affect IK Horizontal (default 1) or Apply Pelvis Offset.

**3. Speed Planting.**
- **What it does:** it freezes a foot goal while a named per-foot speed curve is below 15 cm/s, then springs it back.
- **What it needs:** that curve on the source anim instance, or in the target graph. With no curve it does nothing.
- **Where the lock lives:** in **component space**, so on a moving capsule a "planted" goal travels with the capsule. It suits root-motion-in-pose playback, not the game's capsule-driven walk.
- **Sample data:** the sample's animations carry no per-foot speed curves (asset bytes). They carry `movedata_speed` (character speed), `enable_warping`, `phase`, `DisableLeftFootIK` and `DisableRightFootIK`.

**4. Retarget Pose From Mesh.**
- **Ticking and visibility:** the source must be registered and must evaluate its bones every frame. It need not be visible.
- **Hidden source needs AlwaysTickPoseAndRefreshBones.** ACharacter's mesh defaults to **AlwaysTickPose**. With that setting a hidden mesh stops refreshing bones about one second after it was last rendered, and the copy goes stale.
- **Tick order:** it matters. A target attached below the source always ticks after it. The source's tick does not complete until its pose is evaluated and flipped.
- **Lag:** none when attached (the sample's ABP_GenericRetarget uses "Parent Skeletal Mesh Component" mode, asset bytes), unless the source blends physics. If not attached, a one-frame lag is possible. That is worth up to v·Δt of slide at a start or stop, about 2.5 cm at 150 cm/s and 60 fps.

**5. Foot locking that could run on the target after the retarget.**
- **MetaHuman post-process ABP:** the MetaHuman body's post-process ABP (`ABP_Body_PostProcess`) runs after the main graph. It holds RigLogic, a head-movement Control Rig and a bool blend, and no foot nodes (asset bytes).
- **Foot Placement (experimental):** it locks in world space. It needs `ik_foot_root` and per-leg IK foot bones, and a plant speed from either the root-motion attribute (Graph mode) or speed curves (Manual mode).
  - The MetaHuman body has no `ik_foot_*` bones (asset bytes).
  - Retarget Pose From Mesh passes on no root-motion attribute.
  - So Foot Placement cannot run on the worn body as it stands.
- **Leg IK:** it has the same need for IK foot bones.
- **IK Rig node:** it accepts world-space goals, so a home-made world-space lock after the retarget is possible.
- **The source's own nodes:** the mover's own ABP already runs Leg IK, Stride Warping, Orientation Warping, Offset Root Bone and Steering. Any slide they leave on the mannequin is copied 1:1 to the MetaHuman.

---

## 1. Placing the target foot: details

### 1.1 The op stack and its order

- **Default stack** for a new retargeter: Pelvis Motion, FK Chains, Run IK Rig, Root Motion, Curve Remap (`IKR/../IKRigEditor/Private/RetargetEditor/IKRetargeterController.cpp:383-396`).
- **Parent and child order** (`IKRetargetProcessor.cpp:1482-1549`):
  1. Run IK Rig `RunBeforeChildren`
  2. children `Run`
  3. Run IK Rig `Run` (the IK solve)
  4. children `RunAfterParent`
- **Base pose:** each frame the target starts from its retarget pose (`IKRetargetProcessor.cpp:1377-1382`).
- **Inputs:** the source pose is component space, with scale stripped (`IKRetargetProcessor.cpp:1302-1309`). The run parameters carry no world or component transform (`IKRetargetProcessor.h:372-388`).
- **Deprecated op:** "Retarget IK Goals" is marked `Deprecated` (`RT/IKChainsOp.h:199`). On editor load, older assets are split into Run IK Rig chain settings plus new Blend to Source, Offset Goals and Scale Goals ops (`IKRetargeter.cpp:153-157`, `512-755`; mappings at `533-658`). Old "IK Goal" tutorials therefore describe settings that now live in those ops.

### 1.2 The base goal (Run IK Rig, per chain)

- **Lengths:** the straight thigh-to-foot length is cached from each retarget pose (`RT/RunIKRigOp.cpp:64-87`; chain transforms come from the global retarget pose, `IKRetargetProcessor.cpp:612-618`).
- **Goal formula** (`RunIKRigOp.cpp:110-136`):
  `Goal = TargetThigh_now − PelvisDelta·(1 − AffectIK) + SourceDir · (SourceLen_now / SourceLen_ref) · TargetLen_ref`
  That is, goal = target hip + L × (source foot − source hip), with L = TargetLen_ref / SourceLen_ref.
- **Rotation:** the source foot's delta rotation from its retarget pose is applied to the target foot's retarget rotation (`RunIKRigOp.cpp:139-154`).
- **Space:** goals are reset each frame to the FK pose, in component space (`RunIKRigOp.cpp:340-356`, `651-683`).
- **Solve:** `Solve()` is called with no component transform (`RunIKRigOp.cpp:315-320`).
- **Defaults** (`RT/RunIKRigOp.h:36-70`): bEnableIK true, ChainPositionAlpha 1, ChainRotationAlpha 1, bOverrideGoalAlpha false, Final Position/Rotation Alpha 1.

### 1.3 Pelvis Motion (pelvis height scale, Affect IK)

- **k:** k = target pelvis Z / source pelvis Z in the retarget poses (`RT/PelvisMotionOp.cpp:182-196`, `217-224`).
- **Position** (`PelvisMotionOp.cpp:325-333`): the source pelvis position *vector* (all three axes) is multiplied by k, then optionally blended to the absolute delta. Horizontal sway and the Offset Root Bone lag of the source are therefore scaled by k about the component origin.
- **Then applied in order** (`PelvisMotionOp.cpp:335-382`): floor constraint, blend to source, vertical scale, horizontal scale (about the retarget-pose position), static offsets, alpha.
- **What reaches the feet:** `PelvisTranslationDelta` = everything changed after the k-scaled position (`PelvisMotionOp.cpp:384-385`). Only that delta, weighted by Affect IK, reaches the feet (`RunIKRigOp.cpp:127-133`; `PelvisMotionOp.cpp:268-276`).
- **Defaults** (`RT/PelvisMotionOp.h:28-117`):

| Setting | Default |
|---|---|
| BlendToAbsoluteOffset | 0,0,0 |
| FloorConstraintWeight | 0 |
| RotationAlpha | 1 |
| TranslationAlpha | 1 |
| BlendToSourceTranslation | 0 (weights 1,1,1) |
| ScaleHorizontal | 1 |
| ScaleVertical | 1 |
| Affect IK Horizontal | **1** |
| Affect IK Vertical | **0** |

- **Sample values** (both retargeters, asset bytes; RTG_nrw offsets 11088–12296): all defaults except TranslationOffsetGlobal = (0, 0, 1). That is 1 cm up, so its horizontal part and its Affect IK effect are zero.

### 1.4 The goal-modifying child ops

**Blend to Source** (`RT/BlendToSourceOp.cpp:42-83`)
- Lerps goal X, Y, Z toward the source end-bone position (component space). The weight is BlendToSource × TranslationAlpha × op Alpha × per-axis weight.
- Optionally first adds the pelvis delta × Affect IK × ApplyPelvisOffset (`:71-75`).
- Rotation blends only if RotationAlpha > 0 (`:86-106`).
- Defaults (`RT/BlendToSourceOp.h:31-56`, `70-71`): BlendToSource **0**, TranslationAlpha 1, RotationAlpha 0, TranslationPerAxisAlpha 1,1,1, ApplyPelvisOffset 0, op Alpha 1.
- **Sample (asset bytes, RTG_nrw 23127–24217, RTG_ovw 23239–24329):**
  - LeftLeg and RightLeg: BlendToSource **1.0**, TranslationAlpha 1, RotationAlpha 0, per-axis **(1, 1, 1)**, ApplyPelvisOffset 1.0.
  - Arms: BlendToSource 0.
  - Op Alpha and bEnabled are not stored, so they are at their defaults (1, true). This is an inference: the struct has no custom serialiser, so only non-default values are written.

**Offset Goals** (`RT/OffsetGoalsOp.cpp:66-74`)
- Adds a global offset, plus a local offset rotated by the goal's rotation. A local offset on a foot therefore moves as the foot rolls.
- Defaults 0 (`RT/OffsetGoalsOp.h:30-69`).
- Sample: legs 0. In `_ovw` only the arms have local offsets, (−3, 8, 0) and (3, −8, 0) (asset bytes, offsets 24997 and 25729).

**Scale Goals** (`RT/ScaleGoalsOp.cpp:47-73`)
- `Goal *= (ScaleHorizontal, ScaleHorizontal, ScaleVertical)` about the **component origin**. Then optional "Scale Along Chain" (the old Extension) about the thigh.
- Defaults 1, 1, 1, op Alpha 1 (`RT/ScaleGoalsOp.h:29-56`).
- Not in the sample.

**Stride Warping** (`RT/StrideWarpingOp.cpp:318-360`)
- Scales each foot's forward offset from a body frame by WarpForwards, then adds sideways offset and splay.
- Defaults: WarpForwards 1, Sideways 0, Splay 1, Direction from Goals (`RT/StrideWarpingOp.h:36-94`).
- Not in the sample.

**Floor Constraint**
- Changes goal **height only** (`RT/FloorConstraintOp.cpp:445`, `510`).
- Defaults: off per chain, falloff 8 and 20 cm (`RT/FloorConstraintOp.h:117-172`).
- Not in the sample.

**Speed Plant IK Goals** — see section 3.

**Scale Source** (`IKRetargetProcessor.cpp:2259-2300`; `RT/ScaleSourceOp.h:26-36`)
- Scales the whole *source* pose about the component origin or a bone, before anything else. That changes a planted foot's component-space speed by the same factor.
- Not in the sample.

**Pin Bone**
- Copies bone transforms between bones (`RT/PinBoneOp.h:95-131`).
- Not in the sample.

### 1.5 Ops after the solve that touch the feet

**Pole Vector Alignment** (`RT/AlignPoleVectorOp.cpp:60-98`)
- Rotates the chain's base about the hip-to-foot axis to match the source knee direction, and carries the children with it.
- The foot *position* is kept, because it lies on the axis. The foot's *orientation* turns about that axis, so the ball and toes swing by the match angle times their distance from the axis.
- **Sample:** LeftLeg and RightLeg enabled, AlignAlpha 1, MaintainOffset false. Toes off. (Asset bytes, RTG_nrw 30153–34804.)

### 1.6 The target IK rig

- `IK_Metahuman_Retarget` uses the FBIK solver with RootBehavior **PinToInput** (asset bytes).
- FBIK defaults: Iterations 20, bAllowStretch **false**, RootBehavior PrePull (`IKR/Public/Rig/Solvers/IKRigFullBodyIK.h:159-178`). `bAllowStretch` is not stored in the asset, so it is probably false.
- So the pelvis does not move to help, and an out-of-reach goal leaves the foot short.

### 1.7 The deprecated op's defaults, for reading old notes

`RT/IKChainsOp.h:80-134`:

| Setting | Default |
|---|---|
| EnableIK | true |
| BlendToSource | 0 |
| BlendToSourceTranslation | 1 |
| BlendToSourceRotation | 0 |
| BlendToSourceWeights | 1,1,1 |
| ApplyPelvisOffsetToSourceGoals | false (true for very old assets, `IKChainsOp.cpp:183-197`, `219-230`) |
| StaticOffset | 0 |
| ScaleVertical | 1 |
| Extension | 1 |

The formula is the same as Run IK Rig's (`IKChainsOp.cpp:108-168`).

---

## 2. When a still source foot gives a moving target foot

### 2.1 Derivation for the default goal (from the code in 1.2 and 1.3; not measured)

Setup:
- The source foot is planted in world.
- The capsule moves the component at velocity v.
- The animation is in place in component space.
- So the source foot's component-space velocity is −v.

Goal: G ≈ k·P_s + hipoffset + L·(F_s − T_s), where P_s is the source pelvis position, F_s the source foot and T_s the source thigh, all in component space. The target foot's world velocity is then about:

> **V_foot ≈ (1 − L)·v + (k_eff − L)·dP_s/dt** (plus small terms from pelvis rotation times any hip-width mismatch)

- k_eff ≈ k·[1 + AffectIKHorizontal·(ScaleHorizontal − 1)] on the horizontal axes.
- **Term 1, leg length versus capsule speed.** A target leg 5 % longer than the source (L = 1.05) at 150 cm/s and 0.6 s of stance slides about 0.05 × 150 × 0.6 ≈ **4.5 cm per step**. That figure is illustrative, not measured.
- **Term 2, the source pelvis's own component-space motion.** This includes the sample's Offset Root Bone lag at starts, stops and turns, times the mismatch between pelvis ratio and leg ratio.
- **Scale Goals horizontal = s:** multiplies the goal's component-space velocity, giving (1 − sL)·v + s(k_eff − L)·dP_s/dt (`ScaleGoalsOp.cpp:58-61`).
- **Scale Source factor:** acts the same way (`IKRetargetProcessor.cpp:2259-2300`).
- **Stride Warping:** rescales only the forward part (`StrideWarpingOp.cpp:340-345`).

### 2.2 With the sample's Blend to Source = 1 on X, Y and Z

The goal equals the source foot position in component space (`BlendToSourceOp.cpp:64-83`). The leg-length and pelvis-scale terms vanish from the foot *position*; they only change knee bend and reach. Remaining ways a still source foot gives a moving target foot:

1. **Apply Pelvis Offset.**
   - The sample has 1.0, which adds the horizontal pelvis delta × Affect IK Horizontal.
   - It is zero in the sample, because the only pelvis change is +1 cm in Z and Affect IK Vertical = 0.
   - Any later change to Pelvis ScaleHorizontal, a horizontal static offset or the pelvis blend-to-source would leak straight into the feet (`BlendToSourceOp.cpp:71-75`; `PelvisMotionOp.cpp:362-385`).
2. **IK reach.**
   - With PinToInput and no stretch, a goal farther from the target thigh than the target leg can reach is not met. The foot then trails the goal as the hip moves.
   - Risk is highest at heel strike and push-off, when the source leg is near straight.
   - The target thigh sits at about k × source pelvis height. A MetaHuman whose legs are short relative to its pelvis height (k > L) is the risky case.
3. **Different component frames.** The pose is applied in the target's own component space (`AnimNode_RetargetPoseFromMesh.cpp:176-193`). Any fixed offset between the two meshes' component transforms becomes a world-space arc during turns: slide ≈ turn angle × offset.
4. **Stale or late source pose** (section 4).
5. **Ball or toe as the measured point.** Foot rotation is the source's delta rotation (Run IK Rig ChainRotationAlpha 1; Blend to Source RotationAlpha 0).
   - A MetaHuman foot-to-ball distance that differs from the mannequin's makes the target ball move by about |Δfoot length| × roll angle during heel-off.
   - Pole Vector Alignment adds a swing about the leg axis (1.5).
   - Both are small, about 1 cm, unverified.
6. **Height.** The Z weight of 1 puts the MetaHuman ankle at the mannequin's ankle height. A different ankle height makes the sole sink or float. That is a vertical fault, not a slide.

### 2.3 Root motion versus pelvis motion

- **What the ops see:** they see only component space (`IKRetargetProcessor.h:372-388`). The Root Motion op only places the target *root bone*, from the source root scaled by k × ScaleHorizontal/ScaleVertical (`RT/RootMotionGeneratorOp.cpp:298-329`). It does not move the IK goals.
- **The sample:** it has no Root Motion op. Its FK "Root" chain uses Globally Scaled translation, i.e. the source root × k (`RT/FKChainsOp.cpp:389-393`; asset bytes, RTG_nrw 12488–12648).
- **Capsule-driven characters:** whether the source's root motion is extracted to the capsule decides what "planted" looks like in component space. With capsule movement, as in the sample, a world-planted foot slides backwards through component space at capsule speed.

### 2.4 Settings that make a still source foot give a still target foot

- **Blend to Source on both leg chains:** BlendToSource 1, TranslationAlpha 1, per-axis X = Y = 1, op Alpha 1.
  - Z = 1 copies the source's foot height. Z = 0 keeps the default goal height instead.
  - This is what the sample ships.
- **No horizontal pelvis change, or no route for it to the feet:**
  - Pelvis ScaleHorizontal 1, BlendToSourceTranslation 0, horizontal static offsets 0;
  - or ApplyPelvisOffset 0;
  - or Affect IK Horizontal 0.
- **No horizontal scaling of the feet:**
  - no Scale Goals horizontal or along-chain scaling on the legs;
  - no Stride Warping;
  - no Scale Source ≠ 1;
  - no local Offset Goals on the feet;
  - Speed Planting off or inert (section 3).
- **One frame of reference:** the target attached to the source with an identity relative transform and the same scale.
- **Reach margin** for the MetaHuman legs at the mannequin's foot positions, or a different root behaviour or stretch in the target IK rig. Not checked; see open points.
- **A fresh source pose every frame** (section 4).

---

## 3. Speed Planting: details

- **Per chain** (`RT/SpeedPlantingOp.h:28-34`): Alpha 1 and SpeedCurveName (no default name).
- **Op settings** (`RT/SpeedPlantingOp.h:56-98`): Alpha 1, SpeedThreshold **15** cm/s, BlendMethod Spring, SpringStrength 3 Hz, MoveTowards settings (MaxBlendSpeed 900, TimeToMaxSpeed 0.2, ArrivalSpeedGain 10).
- **Behaviour** (`RT/SpeedPlantingOp.cpp:51-160`):
  - If the curve value is negative (never found), return with no effect (`:56-59`; the initial value is −1, `SpeedPlantingOp.h:133`).
  - Below the threshold the goal is held at the position it had on the planting frame (`:69-86`).
  - Leaving the plant blends back by spring or move-towards (`:89-156`).
  - Alpha lerp at `:158-159`.
- **The lock is in component space.** The goal positions are component space (`RunIKRigOp.cpp:671-674`). No component or world transform is used anywhere in the op (whole file read, 452 lines; the only `InComponentTransform` is in debug draw, `:382`).
  - On a capsule-driven character a "planted" goal therefore moves with the capsule in world: full-speed slide.
  - It suits poses whose root motion stays in the pose (batch export, editor preview).
  - This is an inference from the code, not seen running.
- **Where the curves come from:**
  - the source *main* anim instance's attribute curves, on the game thread (`:306-329`);
  - else the target graph's curves at evaluate (`:332-347`).
  - The batch exporter samples the same curve names from the source sequences (`IKR/../IKRigEditor/Private/RetargetEditor/IKRetargetBatchOperation.cpp:387-514`).
  - A bone translation-speed curve can be baked with the Motion Extractor modifier (`E/Plugins/Animation/AnimationModifierLibrary/.../MotionExtractorTypes.h:17`; `MotionExtractorModifier.h:22-49`).
- **Load bug:** PostLoad sets SpringStrength from the deprecated Stiffness on *every* load, with no version check (`SpeedPlantingOp.cpp:46-49`; called each load via `IKRetargeter.cpp:1048-1055` and `IKRetargetOps.cpp:36-39`).
  - 250 gives 2.516 Hz.
  - A value set by hand is lost on reload.
  - Both sample retargeters store 2.5165 (asset bytes).
- **The sample's op:**
  - All four SpeedCurveName entries are `None` (asset bytes, RTG_nrw 25983–26419), so the op does nothing.
  - SpeedThreshold and BlendMethod are not stored, so they are at their defaults.
- **The sample's animations** (asset bytes; name tables of 1,536 AnimSequence files under `Characters/UEFN_Mannequin`):
  - curves `movedata_speed` (1,063 files), `enable_warping` (955), `phase`/`Phase`, `DisableLeftFootIK`/`DisableRightFootIK` (80);
  - **no per-foot speed curve**;
  - `contact_l` and `contact_r` appear only as `..._CURVE_CONTROL` names, not as curve names (unverified what those are);
  - `movedata_speed` is the character's speed, so it is useless as a plant signal.

---

## 4. Retarget Pose From Mesh: details

- **Copy step:** in PreUpdate, on the game thread, the node copies the source's component-space transforms (`IKR/Private/AnimNodes/AnimNode_RetargetPoseFromMesh.cpp:261-342`).
  - It uses the leader if the source follows a leader pose (`:280-285`).
  - It skips if the source is unregistered (`:287-291`).
  - It reads the source's *cached* transforms if update-rate optimisation is in step or external interpolation is used (`:293-312`; URO is off by default, `E/Source/Runtime/Engine/Private/Components/SkeletalMeshComponent.cpp:493`).
  - It strips scale (`:314-318`).
- **Evaluate step** (`:73-259`): it gives the reference pose if anything is missing (`:213-217`). Delta time accumulates across updates (`:59-61`, `248`).
- **The header's own assumption** (`AnimNode_RetargetPoseFromMesh.h:40-42`): the source is "Assumed to be animated and tick BEFORE this anim instance".
- **When PreUpdate runs:** at the start of the target's anim update, on the game thread (`E/.../Animation/AnimInstance.cpp:832-851`; `AnimInstanceProxy.cpp:549-557`).
- **"Parent Skeletal Mesh Component" mode** walks up the attach parents to find the source (`AnimNode_RetargetPoseFromMesh.cpp:362-377`). ABP_GenericRetarget stores that mode (asset bytes). It also holds a Copy Pose From Mesh node.
- **Hidden mesh rules** (`E/.../Classes/Components/SkinnedMeshComponent.h:96-116`; `Private/Components/SkinnedMeshComponent.cpp`):
  - "Rendered" means rendered within the last second (`:1864`).
  - Tick pose unless the option is OnlyTickPoseWhenRendered and the mesh is not rendered (`:1795-1803`).
  - Refresh bones only if rendered or the option is **AlwaysTickPoseAndRefreshBones** (`:1805-1808`; `SkeletalMeshComponent.cpp:1847-1881`).
  - With AlwaysTickPose and not rendered, only a parallel pose *update* is dispatched, and the bones are not evaluated (`SkinnedMeshComponent.cpp:1874-1897`).
- **Defaults:**
  - a plain Skeletal Mesh Component: AlwaysTickPoseAndRefreshBones (`SkeletalMeshComponent.cpp:446`; `SkinnedMeshComponent.cpp:474`);
  - **ACharacter's Mesh: AlwaysTickPose** (`E/.../Private/Character.cpp:125`).
  - So a hidden ACharacter mesh feeds a stale pose. The fault would show only about one second after hiding, because of the one-second "recently rendered" window.
- **Order and lag:**
  - Attaching adds a tick prerequisite on the parent, at registration too (`SceneComponent.cpp:829-871`, `2491`).
  - The source's tick does not complete until its parallel evaluation's completion task has run (`SkeletalMeshComponent.cpp:3086-3096`, `4980-4990`). That task flips the read buffer (`:3320-3360` → `SkinnedMeshComponent.cpp:4883-4910`; read buffer at `SkinnedMeshComponent.h:1734-1737`).
  - So a target below the source reads the same frame's pose, with **no lag**.
  - Exception: when the source blends physics bodies, the flip moves to the end-physics step (`SkeletalMeshComponent.cpp:3349-3360`). Then a one-frame lag follows. That is unverified for the sample.
  - The node's "frame of latency" comment (`AnimNode_RetargetPoseFromMesh.cpp:55-57`) concerns a *pin-driven choice of source component*, not the pose.
  - ACharacter's mesh ticks after its movement component (`Character.cpp:155`). The Mover pawn's order was not checked.
- **LOD of a hidden source:**
  - A mesh's LOD comes from its render-side desired LOD (`SkinnedMeshComponent.cpp:4767-4769`). That is updated only when the mesh is seen (`E/.../Private/SkeletalRender.cpp:76`, `133-209`), so it can go stale while hidden. Unverified.
  - A child skinned mesh copies its skinned parent's LOD by default (`bSyncAttachParentLOD` true, `SkinnedMeshComponent.cpp:507`, `4762-4765`). The visible MetaHuman would therefore follow the hidden mover's LOD.
  - Forcing LOD 0 on the hidden mover (ForcedLOD 1, `:4750-4753`) avoids both risks, including LOD-thresholded nodes in the mover's ABP switching off.
- **Leader Pose:** a follower ticks after its leader (`SkinnedMeshComponent.cpp:3252-3253`) and uses the leader's bones directly. It is suitable for the MetaHuman's face and clothes on the body.
- **Copy Pose From Mesh:** copies local transforms *including translation*, by bone name (`E/Source/Runtime/AnimGraphRuntime/Private/AnimNodes/AnimNode_CopyPoseFromMesh.cpp:225-272`). That would give the MetaHuman the mannequin's bone lengths, so it is unfit across proportions.

---

## 5. Foot locking on the target after the retarget: details

- **Post-process ABP:** the post-process instance takes the main graph's output as its input pose and produces the final pose (`SkeletalMeshComponent.cpp:2590-2610`). It can be switched off per component (`bDisablePostProcessBlueprint`, `SkeletalMeshComponent.h:708-712`; `.cpp:5257-5267`).
  - The project's MetaHuman body (`SKM_MH_Lena_BodyMesh`) names `/MetaHumanCharacter/Body/ABP_Body_PostProcess`.
  - That ABP (`E/Plugins/MetaHuman/MetaHumanCharacter/Content/Body/ABP_Body_PostProcess.uasset`) contains: Linked Input Pose, RigLogic, Control Rig `CR_MetaHuman_HeadMovement_IK_Proc`, Blend List By Bool, cached poses. No foot node (asset bytes).
- **Foot Placement** (`E/Plugins/Animation/AnimationWarping/Source/Runtime/Public/BoneControllers/AnimNode_FootPlacement.h`; marked Experimental, `:522-523`):
  - Needs `IKFootRootBone`, `PelvisBone`, and per leg the FK foot, IK foot and ball bones, plus optional speed, lock and disable curves (`:415-446`, `:535-545`).
  - Defaults: SpeedThreshold 60, UnplantRadius 35, LockType PivotAroundBall, and others (`:460-516`). PlantSpeedMode Manual (`:532-533`).
  - It works in world space (`AnimNode_FootPlacement.cpp:97-110`, `421-426`).
  - Graph mode: speed = ball delta + root-motion attribute (`:1535-1546`).
  - Manual mode: a missing curve is read as "unplanted" (`:1549-1553`).
  - On the worn body:
    - no `ik_foot_*` bones exist (asset bytes: `thigh_l`, `foot_l`, `ball_l`, `root`, `pelvis` present; `ik_foot_l`, `ik_foot_root` absent);
    - Retarget Pose From Mesh writes no root-motion attribute (its evaluate fills only the pose; curves come from the Remap Curves op, `RT/CurveRemapOp.cpp:29-86`, which copies all source curves by default, `RT/CurveRemapOp.h:38-50`);
    - there are no foot speed curves.
- **Leg IK** (`E/Source/Runtime/AnimGraphRuntime/Public/BoneControllers/AnimNode_LegIK.h:104-150`): pulls the FK foot to an IK foot bone. It has the same missing-bone problem.
- **IK Rig node:** solves with the component transform, so world-space goals are converted (`IKR/Private/AnimNodes/AnimNode_IKRig.cpp:66-75`; `IKR/Private/Rig/IKRigProcessor.cpp:530-545`; `IKRigDataTypes.h:15-20`). A world-space lock built in game code could be fed to it after the retarget. Inside the retargeter this is not possible (`RunIKRigOp.cpp:318`).
- **The source side:**
  - The mover's ABP (`SandboxCharacter_Mover_ABP`) holds Motion Matching, Blend Stack, Offset Root Bone, Orientation Warping, Stride Warping (Graph mode), Steering, Leg IK and Control Rig nodes (asset bytes).
  - The mannequin's post-process ABP (`ABP_UEFN_Mannequin_PostProcess`) modifies `foot_l` and `foot_r` with Modify Bone and a mesh-space additive (asset bytes; values unknown).
  - The retargeter copies the source's final pose, so whatever these leave on the mannequin's feet is copied 1:1.

---

## Open points

1. **Measure the mannequin's own feet first.** With Blend to Source = 1, the MetaHuman foot equals the mannequin foot in component space. The 3 cm bar must first be passed by the hidden mover's feet. The last go's 13–67 cm may sit on the source side. Not measured here.
2. **IK reach.** The MetaHuman leg length against k × mannequin pelvis height, and whether FBIK (PinToInput, 20 iterations, no stretch) meets the goal at heel strike and push-off. The values were not read from the IK rig; only names were.
3. **How AC_VisualOverrideManager hides and attaches the mover's mesh:**
   - the tick option;
   - the relative transform;
   - whether the MetaHuman is a child of that mesh;
   - whether physics blending is on.
   That is question 2's helper; it decides the stale-pose and lag risks in section 4.
4. **The stale LOD of a hidden mesh**, and the MetaHuman inheriting it through `bSyncAttachParentLOD`. Read from code, not observed.
5. **The values in the mannequin post-process ABP's foot Modify Bone** and whether that ABP is assigned to `SKM_UEFN_Mannequin`.
6. **Ball and toe swing** from Pole Vector Alignment and the foot-length difference. Size estimated, not measured.
7. **The asset-byte readings:**
   - property values decoded from tagged data;
   - absent properties taken as defaults on the rule that delta-serialised structs omit defaults;
   - the BlendToSource op Alpha and bEnabled, and the SpeedThreshold, rest on that rule.
   Confirm in the editor if any of these decide a design.
8. **The Mover pawn's tick order** (mesh after movement) was not checked. Only ACharacter's was (`Character.cpp:155`).
9. **Not reached:** Epic's online pages (none used); the sample's ABP_GenericRetarget pin wiring; the IK rig goal-to-bone assignments beyond names.
