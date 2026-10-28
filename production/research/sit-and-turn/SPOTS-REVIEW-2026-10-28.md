# Review of SPOTS-2026-10-28.md (fresh reviewer, 28 October 2026)

Read only. Every source below was opened today. The document's scripts (mafia_slots.py, kcd_helpers.py, kcd_adb.py) were re-run read-only, and short read-only measurements were made on the same files. Nothing was extracted, nothing was downloaded, and Unreal was not run.

## What holds (checked and right)

- **Mafia:** 478 slots; docking counts 352/98/15/11/2; fly mode 52; leg IK off on 1; 126 starts, 96 at zero; chair start 47.1 cm with root-motion end −47.1; hat-fanning 40, whittling 60, backwards 88 cm at −85°; the slot's fields; the empty state tree; the "UnlessInactive" precondition; loop weights 3/3/2/2/2 with Entry, Exit and FastExit; 16 of 386 NoEntry; door link ±70 cm; 53 hero door sequences.
- **Kingdom Come II:** 279 classes; the Place0 links; users and options (OmmitNav/OmmitPhys, MNMToleranceStrict, ProjectedTargetEndPosition, RequiresAllFragmentsValid, Alternatives); 694 helper sets; front sit-down at 1.257 m, moving 1.284 m and turning 178.6°; 8 side tags; 0.23 to 2.54 m; the 0.247 m variant; 19,758 objects; base layer 32,898 / 5,926 / 729; SitDown 98 options, 96 aligned, median 4.35 s; StandUp 205, none aligned, 2.9 s; blends 0.2 (0.2 to 1.0); align layer starts at 0 with median 1.0 (0.215 to 2.6); ground alignment off in 65 of 71; PushesPlayersOnly 62 of 68; door helpers at ±0.7 m with three stages; Study 1's 2,254 / 1,694 / 829.
- **Unreal 5.8:** the uproject plugins and Build.cs modules; flags (Motion Warping Beta; Gameplay Interactions and Contextual Animation Experimental; Smart Objects no flag); the subsystem's flow; the entrance annotation's fields and its 10 cm capsule from 80 to 40 cm; the 35/180/50 capsule; extents 5×5×40; AddOrUpdateWarpTargetFromTransform; AddRootMotionModifierSkewWarp; Precomputed Warp's tooltip; the subtract-remaining comment; the Character adapter; the cone at 200 cm and 45°; TryCreateBindings and StartContextualAnimScene; PrecomputeData on save; MotionMatch's return and its Experimental marks; the montage default of 0.25 s; the Gameplay Interactions tasks. The web pages (Smart Objects overview, vorixo, updated 1 March 2024) were read.
- **The sample:** two slots with entrances and NPC/Player users; the ten montages; the angle column with pose search; the feet's position and velocity plus the attach-bone distance; the threshold and "try again next frame" strings; the precomputed ease-in-out warp from a bone; sit9.log's 10.87 s, 0–3.10 s and 23.4 cm.
- **Our attempts:** 8 Oct (DECISIONS: the stand-up backwards, bent double, 38 cm, leg IK, 0.5 cm); 25–26 Oct (WALK-2026-10-25.md); the 55/120 sectors and the static/dynamic ignore in TryStartSit (SliceCharacter.cpp). Note: SitProof for Tom is in SliceCharacter.cpp (SitProofTick); CrimeProbe.cpp holds Ron's 8 October -SitProof.
- **First use:** seats 0.535 m apart, 0.451 m high, facing into the room; Ron in the middle.

## Faults

### A. Faults that change the method

**1. The 23.4 cm "drift", and subtracting it (sections 3, 4 and steps 3 and 7).**
- Doc: "The 23.4 cm drift was not subtracted | Subtract remaining root motion"; "Target = slot, drift subtracted".
- Source: the sample's montage stores `WarpPointAnimProvider::Bone`, `WarpPointAnimBoneName` "attach". RootMotionModifier.cpp gives `TargetTransform = CachedOffsetFromWarpPoint.GetValue() * WarpPointTransformGame`. Only RootMotionModifier_SkewWarp.cpp:194 reads `RootMotionRemainingAfterNotify`; PrecomputedWarp.cpp never does.
- Correction: Motion Warping lands the clip's attach bone (the bench marker) on the target, not the root. So the root's 23.4 cm after the window is the clip's own travel relative to the bench, not an error. The sample's Precomputed Warp also ignores "subtract remaining". Mark the diagnosis U. Add to the clip sheet the attach bone's world path after the window and the pelvis's offset from it. Subtract the remainder only for clips warped by Skew Warp from the root. The 8–9 cm hip offset may simply be the clip's authored pelvis-to-attach offset.

**2. Smart Objects editable only in the editor (section 2).**
- Doc: "Slots can be edited only in editor builds… The definition is therefore an editor asset".
- Source (SmartObjectDefinition.h): `GetMutableSlot(const int32 Index)` is BlueprintCallable outside `#if WITH_EDITOR`; `DebugAddSlot()` is unguarded; only `GetMutableSlots()` is editor-only.
- Correction: "A definition can be built at runtime (DebugAddSlot, GetMutableSlot, Validate), but Epic marks that path for testing; an editor asset is the supported way."

**3. Kingdom Come II's offline test is overclaimed (sections 1 and 3).**
- Doc: "Kingdom Come II alone tests every approach against the built place"; "KCD2: the clip's own path"; "**A bench by a wall never offers the approaches that would cross the wall.**"
- Source (SmartObjects.xml): `OmmitPhys` 157 times, `OmmitNav` 95 and `OmitNav` 22. Every door stage reads `'OmmitPhys,MNMToleranceStrict…'`. The table stores only `DropReasons="Physics"`.
- Correction: say it tests each approach unless the entry opts out (doors skip the physics test). What "Physics" sweeps (the clip's path, or only the start and end) is not in the data, so mark it I. The wall sentence is I unless one placed bench is shown.

**4. The door leaf's own clip (section 1, doors; "Later uses").**
- Doc: "the leaf plays its own matching clip (kcd_slaveDoorLeft_male.adb)".
- Source: that file holds one fragment id, `Door_Locked`, with two clips: `door_01_relaxed_walk_locked_door_shake_left_back_male` and `…_front_male`.
- Correction: "the leaf has its own clip only for the locked-door shake. How the leaf moves when it opens was not found (U)." This weakens "Contextual Animation's case" for doors.

**5. Steps lacking a numeric check, the tested path against the played path, and the approach path (section 5).**
- Doc, step 1 check: "a spec test fails any slot without an In and an Out". Step 5: "the run line names it". Step 3: "within 1 cm and 1 degree of the clip's own start". Step 6: play "once the cost is under the sample's threshold".
- Source: task item 4 asks for a numeric check per step. The order names "approach path" first.
- Corrections:
  - Steps 1 and 5 have pass/fail checks, not numbers. Say so, or add numbers.
  - Step 3's check only repeats its own arithmetic. Instead, play from the derived entry with the warp off and measure the hips against the seat.
  - Step 4 tests the derived entries, but step 6 starts wherever the cost passes, up to step 7's 25 cm and 30° away. Test the starts at that envelope's edges too, or refuse any warp beyond what was tested.
  - Define how Tom walks from where E is pressed to the entry. The sample follows a navigation path and reads its length; the method names no approach.

**6. The motion-match call from C++ cannot feed the distance term (step 6 and work item E).**
- Doc: "motion-match that side's clips with the sample's schema"; "UPoseSearchLibrary::MotionMatch returns clip, start time and cost".
- Source: the DistanceToSmartObject channel holds `GetChooserContextParameters`, `SmartObjectSelectionInputs`, `TargetDistance`. That is a Blueprint struct fed by the chooser CHT_SmartObject_BenchAnim.
- Correction: name it. Item E must evaluate the chooser with that context struct from C++, or the distance term is empty. Either raise E's hours or name the trigger for the stand-still fallback.

### B. Faults of fact or tagging

**7. Mafia's door clips.**
- Doc: "53 door clips… all left-handed".
- Source (index_packages.tsv): `AS_hero_nw_alert_lock_pick_door_pull_r`, `…push_r`, and their combat twins.
- Correction: the 28 door-open clips (push or pull × near or far handle) are all left-hand. The lock-pick clips come in both hands.

**8. Door approach distances.**
- Doc: "from 0.7 to 2.3 m".
- Source (re-measured on Kuttenberg's helper sets, DoorLeft and DoorRight "Door" starts): 0.657 to 2.44 m.
- Correction: write 0.66 to 2.44 m, or name the frame used. Add "and all skip the physics test".

**9. "Both games agree… a warp corrects small errors early".**
- Source: the doc's own to-fetch list has "the chair set's… warp windows". The Mafia slots read `IgnoreRootBoneTransform` True on 476 of 478.
- Correction: Mafia's warp is not read, so mark it U. Mafia's 0.2 s is its locomotion state-machine fades (study-7 FINDINGS), not sit blends.

**10. The leg IK row.**
- Doc: "Ground alignment, leg IK | off while fitted (65 of 71; Mafia IK off on 1)".
- Source: `disableLegIK=False 477`, `True 1`.
- Correction: Mafia keeps leg IK on in 477 of 478 slots. Only KCD2 supports "ground alignment off". Ground alignment is not a foot lock, so step 7's "foot lock off" has no source; mark it I.

**11. The alignment window and the hips.**
- Doc: "**the alignment window starts at 0 s and lasts median 1.0 s… so the correction is spent… before the hips drop**".
- Source: the 1.0 s is the `Blend Duration` field on the PositionAdjustAlignBone layer. The doc's own list says "where the hips drop… against the 1.0 s window (clip binaries)"; KCD2's study-7 findings mark procedural meanings "unverified".
- Correction: the numbers are M. That the field is the window's length is I. "Before the hips drop" is U.

**12. Contextual Animation as a new plugin.**
- Doc: "it adds an editor asset and an Experimental plugin (I)".
- Source: GameplayInteractions.uplugin lists ContextualAnimation; the doc's own line 78 says it is already enabled.
- Correction: it adds a module dependency and editor assets, not a plugin.

**13. The account of try 3 omits a fault.**
- Source (WALK-2026-10-25.md): "a pointed foot still snaps flat at 8.25 to 8.37 s, 3 to 4 cm, on Tom only (the copy)". Tries 1–2's known shortfall: "perched on the front of the cushion with a pointed foot".
- Correction: add both to section 4. Step 7's 3 cm slide check would catch the snap, but the method does not answer it; say so.

**14. Stand-up travel incomplete.**
- Doc: "step 0.33 to 0.99 m forward, or 0.67 to 1.25 m back over the bench".
- Source (re-run kcd_helpers.py): the side and back-diagonal stand-ups move 1.04, 1.92 and 2.39 m. Basket-weaving starts 0.17 m off the seat, milk-pan 0.04 m.
- Correction: add these. They matter for step 9's exit test beside the window.

**15. Sector widths.**
- Doc: "8 of 45 degrees (KCD2)".
- Source: 8 side tags; start yaws are uneven (front-right 52–68°, right 73°, back-right 106°).
- Correction: "8 approach directions; widths not in the data (I)".

**16. "Most scenes stream in already seated".**
- Source: Study 1 says "374 scenes carry their own person, who appears when the scene streams in".
- Correction: tag it I and cite Study 1. A zero start alone does not show it.

**17. The door-end seat's distance.**
- Doc: "about 0.65 m from the shop front".
- Source: seats.json door-end seat z 5.92; mickeys-office.json inside z0 5.12; bench box z0 5.65.
- Correction: 0.80 m from the room's front face (the bench end 0.53 m), or cite the sill's position.

**18. A question already settled.**
- Doc: "whether this new direction counts as a try is his to say".
- Source: DECISIONS 28 Oct 15:40 has "sitting reopened by the interaction-spot method"; the order "decides `o25-2b-sit`".
- Correction: drop the question. It is settled.

**19. The estimate.**
- Doc: "About 10 hours (9 to 13)".
- Source: METHOD-2026-10-06.md put the sit at 10 to 14 h, and the sit has now taken three tries. Item D is a new contact probe over 30 entries; item E carries faults 1 and 6.
- Correction: call 10 h a lower bound (about 12 to 16 h), or state when the stand-still fallback is taken.

## Smart Objects and Contextual Animation: the decision

The order requires researching both ("how… and Unreal's own Smart Objects, Motion Warping and Contextual Animation"), not using them. "Tom sits… that way" means as an interaction spot. The document does research both, so leaving them out is allowed.

The choice is sound for one player on one bench:
- Reservation already has a home in the simulation (CLAUDE.md, one home per fact).
- The sample's Smart Object entry needs a player controller that the puppet mover lacks (WALK-2026-10-25.md).

Two reasons need fixing. One is wrong (fault 2). The other is overstated (fault 12). The decision should also say plainly:
- Mafia, the Unreal reference, runs all 478 slots on Smart Objects.
- Unreal's FindEntranceLocationForSlot already does the navmesh projection, ground trace and straight test that step 4 partly rebuilds.

So for the townspeople, Smart Objects are the likely route back.

**Verdict: pass with fixes. 92 claims checked, 19 faults. Faults 1 to 6 change the method and must be fixed before it is adopted. Faults 7 to 19 are corrections of fact, tag or wording.**
