Method researched: review of n16-7-knees-method-2026-11-17.md against its engine source, measure files and web pages (read 17 Nov 2026)

# n16-7 knees note: fresh review (17 Nov 2026)

**Verdict: same fault as the pelvis method.** The engine reading is sound, but the bent knees are the fault the stopped method was aimed at, and K1 fits only some frames.

## 1. Evidence for each cause

- **Engine claims check out** (UE 5.8 source, read 17 Nov): RunIKRigOp.cpp 127-133 subtracts only `PelvisTranslationDelta * (1 - AffectIK)`; FKChainsOp.cpp 300-301 and 346-351 give `RotationDelta * TargetInitialRotation`; BlendToSourceOp.cpp 80-82 lerps goal X/Y to the raw source end bone; OffsetGoalsOp.cpp 70 turns the local offset by the goal's rotation.
- **K1, partly supported.** The measure files confirm "rest_knees_deg ... [0.0, 0.0], [4.9, 4.9]" and "143_18 Rocco: target 17.5 where the source is 12.6" (frame 169). But the note says the bend is "carried into every frame", and the same files disagree: 143_18 stand l is +1.9, not +4.9. 113_15 stand, other side: source 11.9, target 12.0 (+0.1). 131_01 Rocco stand: -1.1 and -0.9. The note's fit table leaves out the last two. So the reference knee adds a variable 0 to 4.9 degrees, not a constant. The cheap read-only check (note section 6, item 1) has to run before K1 counts as shown.
- **K2, plausible but unverified.** "checked at frame 246 only (the worst frame is 202)". The note says so itself. The measure file confirms frame 202, left side, source 0.0, target 22.9.

## 2. Is the fix the professional method?

- **Part A.** Epic, "Retargeting Bipeds with IK Rig" (https://dev.epicgames.com/documentation/unreal-engine/retargeting-bipeds-with-ik-rig-in-unreal-engine, read 17 Nov): "Make sure both characters have matching reference poses." Confirmed. That page says nothing about knees.
- **Part B.** Autodesk HumanIK Retarget Specific attributes (Maya 2025 help, read 17 Nov, excerpts only): Feet Spacing Mode, Auto "adjusts the distance between your target character's left and right ankles". How Auto computes the spacing is still unverified. Using Offset Goals for it is the note's own construction from the code, not a documented recipe. Epic's op-stack page (read 17 Nov) has no text on foot spacing. It does name Filter Bones for limb proportions, which the note leaves out.
- **Unreached:** Kulpa 2005 (403), the MotionBuilder retargeting page, Gleicher 1998, Warhorse's video. Mafia/KCD2: none found.

## 3. Separate cause or the same fault?

The hip-joint note set out to make "pelvis height and knee bend match" (its lines 9, 11) and predicted that knees "should follow the source within the 3-degree bar" (line 161). knees_deg and stand_knee_deg were among its counted failures. RULINGS 7 Nov counts tries per fault, not per cause or method. That chain ended when the third method closed under a third of the gap. A newly found cause is a new method on the same fault, not the first try on a new one. Under the ruling the fault stays set aside and listed. Whether anything more may run is the session's decision. The read-only Blender check is a measurement, not a try.

## 4. New faults the fix could cause

- 131_01 RoccoP2 slide is 1.98 against a 2.0 bar. In Part B, Δw 2.52 × foot yaw change can fail it (the note names this).
- The local offset turns with the goal's rotation, which follows the source foot (RunIKRigOp.cpp 147-150). On pitched or raised feet (sit clips, 113_15's ball pitch) part of Δw turns vertical: a risk to feet_height.
- Part A changes L_s and so r and Scale Source on every frame, which shifts height checks that pass today.
- Squash pre-bend near straight (0.1% gives about 4 degrees): standing knees may land close to the 10-degree bar.
