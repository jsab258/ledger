# Starting the bench approach: the sample's own search, or his steps brought into step (29 October 2026)

This is the research the two-tries rule asks for after sitting's matched-foot start failed twice (DECISIONS, 28 October 22:47 and 23:52; SPOTS-2026-10-28.md, steps 5 and 6). Everything was read on 29 October 2026.

Marks: **R** read in a file, header or page; **M** measured here; **I** inference; **U** unverified.

**How the assets were read.** The sample's .uasset files cannot be opened in an editor here, so a small reader extracted their name tables, export tables and tagged property values. It ran from the session's scratch folder and was not kept. No asset was changed. Only node names and pins can be read from the Blueprint graphs; the wiring between nodes is not visible.

## Questions

1. How does Epic's Game Animation Sample start a bench approach montage? What does its search compare, at what moment does the clip start, how is the start time chosen, what blend is used, and what context does the chooser need?
2. Can that chooser or search be run from C++ for our mover? Which functions and inputs pick (a) the montage and (b) its start time?
3. What do Epic's documents, shipped games or other primary sources say about bringing the walker's last steps into step with the clip?
4. One design for a third try, with its numeric check, its cost and what is unverified.

## 1. How the sample starts a bench approach

**The chain** (R; node names in AC_SmartObjectAnimation and STT_PlayAnimFromBestCost).
- The task STT_PlayAnimFromBestCost runs every tick while the character is moved to the slot. Its own comment calls it "the heart of smart objects working with motion matching", and says it runs "until a good animation has been found or until your reach your end destination of a move".
- It evaluates only within **300 cm of path distance** (MaximumDistanceThreshold, the task's default) and past a "Minimum Velocity Check" of **100**. Which way that check compares is I.
- It plays only when **Cost ≤ 1.0** (CostThreshold, set in ST_Player_SandboxCharacter_SmartObject). Otherwise, in its own words, "the task will try again next frame". Another comment says "Using the pathed distance is really important".
- The function "Evaluate Distance and Motion Match" builds a chooser context with the anim instance and two Blueprint structs, then evaluates the proxy CHPA_SmartObject through the proxy table CHPT_SmartObject_Bench. That table's one entry is CHT_SmartObject_BenchAnim. StartTime and Cost are read back from the context.

**The chooser CHT_SmartObject_BenchAnim** (R, its property values).
- **Context, in this order:** 0 is the AnimInstance; 1 is SmartObjectSelectionInputs (TargetDistance, TargetAngle, PoseHistoryNode); 2 is SmartObjectSelectionOutputs (StartTime, Cost), marked "write".
- **Column 1, TargetAngle.** Each range has two rows, one per lead foot:

  | Clips | Range |
  |---|---|
  | F | −55 to 55 |
  | L_090 | 55 to 120 |
  | R_090 | −120 to −55 |
  | BL | 120 to 180 |
  | BR | −180 to −120 |

- **Column 2, Pose Match.**
  - Its pose history comes from PoseHistoryNode.
  - Search mode brute force, unmirrored only, continuing-pose bias 0.
  - Each row samples the whole clip (sampling range 0 to 0; the end exclusion set to 0).
  - Its outputs are StartTime and Cost.
  - It searches the chooser's internal database PSD_CHT_SmartObject_BenchAnim with the schema PSS_SmartObject.

**What the search compares** (R, PSS_SmartObject's values; unset values are the engine defaults in the headers).

| Channel | Compares | Weight |
|---|---|---|
| DistanceToSmartObject (a Blueprint Distance channel) | the clip's root-to-"attach"-bone distance against the query's TargetDistance | 0.1 |
| Position | foot_l relative to foot_r | 1 |
| Velocity | foot_l relative to foot_r | 1 |
| Velocity | foot_l, vertical only | 0.3 |
| Velocity | foot_r, vertical only | 0.3 |

- The distance channel's **MaxDistance of 50** is a hard filter. The engine discards any pose whose distance differs from the query by more than 50 cm (PoseSearchFeatureChannel_Distance.h:36–41; .cpp:51–60).
- There is no trajectory, root-velocity or phase channel. Samples are taken 30 a second and the data is normalised (PoseSearchSchema.h:73, 91).
- **So the feet choose the moment.** Distance only rules out moments more than 50 cm off, and adds a small cost.

**Which moments can be chosen** (R notifies; M against F:/LedgerTools/scratch/sit/clip_sheet.json).
- Every In clip carries a "Block Transition" or "Exclude From Database" notify from 2.26–3.67 s to its end. Epic's header says a search "will not return results that overlap this notify" (PoseSearchAnimNotifies.h:38–41).
- The searchable part therefore runs from 0 s, with 4.2 to 5.2 m of travel left, down to 32–68 cm left.
- In that part, plants of the same foot fall 150 to 170 cm apart (M).

**Blend and warp** (R).
- The montage is played by CreateProxyObjectForPlayMontage with StartingPosition set to StartTime (PlayMontageCallbackProxy.h:38–44).
- Blend-in is the montage's own: 0.25 s (AnimMontage.cpp:76, not overridden), linear. Blend-out is 0.35 s, sinusoidal (the F_Lfoot montage).
- The warp is Precomputed Warp to the target "SmartObject", taken from the bone "attach", ease-in-out, with steering on. Its window runs from 0 to 3.10–5.17 s. On F_Lfoot the warp along the direction of travel ends at 0.57 of the window, the sideways warp at 0.37, and the rotation starts at 0.73.

**Why the sample always finds a start, and ours did not** (I).
- The sample searches both lead-foot clips over the whole walk-in, inside a ±50 cm band. That covers more than a gait cycle, so a moment with his feet's arrangement nearly always exists, and the warp absorbs up to 50 cm.
- Our try asked for three things at once: the same planted foot, stance within 10 points, and position within 15 cm along. Whether such a moment exists depends on where his stride happens to fall, and nothing moves it. Our measure also needs a planted foot; Epic's feet channels also cover swing and double support.

**Unconfirmed:** the wiring of the Blueprint graphs; which way the velocity check compares; what the sample plays if the move ends without a match (I: the best found); Epic's 5.8 sample blog (403).

## 2. Running it from C++

It can be done. Untried, so U. One call answers both (a) and (b): the chooser returns the montage and writes StartTime and Cost into the outputs struct.

1. **Context.** Use `FChooserEvaluationContext` (Plugins/Chooser/Source/Chooser/Public/IObjectChooser.h:68), filled in the table's own order:
   - `AddObjectParam(AnimInstance)` (:77);
   - `AddStructViewParam(FStructView(InputsStruct, InputsMemory))` (:97);
   - the same for the outputs struct.
2. **The two structs** are Blueprint user-defined structs (/Game/Blueprints/SmartObjects/SmartObjectSelectionInputs and …Outputs).
   - Load each as a `UUserDefinedStruct`, allocate it and call `InitializeStruct`.
   - Find each field by its authored name. The stored names carry suffixes, such as `TargetDistance_4_5AACC03F…`.
   - TargetDistance and TargetAngle are doubles. PoseHistoryNode is an `FPoseHistoryReference` (PoseSearchHistory.h:412).
3. **Pose history.** `UPoseSearchLibrary::FindPoseHistoryNode(TEXT("PoseHistory"), AnimInstance)` (PoseSearchLibrary.h:282), then `GetPoseHistoryReference()` (AnimNode_PoseSearchHistoryCollector.h:127). The mover's graph, SandboxCharacter_CMC_ABP, tags its collector "PoseHistory" (R).
4. **Evaluate.** Either of:
   - `UChooserTable::EvaluateChooser(Context, Table, Callback)` (Chooser.h:214);
   - `UChooserFunctionLibrary::EvaluateObjectChooserBase(Context, UChooserFunctionLibrary::MakeEvaluateChooser(Table), UAnimMontage::StaticClass())` (ChooserFunctionLibrary.h:52, 150).

   The table is /Game/Blueprints/SmartObjects/Bench/CHT_SmartObject_BenchAnim; the proxy table only points to it (R).
5. **Read** StartTime and Cost from the outputs memory. With no match the cost stays 100 (PoseSearchChooserColumn.cpp:899–900).
6. **Why not MotionMatch alone.** The Blueprint distance channel writes its query only when the search carries a chooser context (PoseSearchFeatureChannel_Distance.cpp:66–73), and the Pose Match column passes it (PoseSearchChooserColumn.cpp:780). MotionMatch has a chooser-context overload (PoseSearchLibrary.h:243, experimental), but the bench clips have no branch-in notify, so the internal database's clip subset would have to be set by hand. The chooser already does that.
7. **Inputs to feed.**
   - TargetAngle: the kept entry's side. Forcing it keeps the room-tested side.
   - TargetDistance: the mover root's floor distance to the slot. The database stores the straight root-to-attach distance (.cpp:182–191). The sample uses path length, which on our straight last metre is the same (I).
8. **Build.** Add "Chooser" to Build.cs. The plugin is already enabled, and PoseSearch is already linked. These APIs are experimental.

## 3. Bringing his last steps into step

- **Epic, stride warping** (pose-warping page). It fits the stride to the capsule's speed, with StrideScale = LocomotionSpeed / RootMotionSpeed and clamps. It is written for locomotion; nothing is said about montage entries.
- **Epic, distance matching** (page, and AnimDistanceMatchingLibrary.h:17–18, 37). Play rate follows distance, clamped by default to 0.75–1.25. It is "common to … use techniques such as Stride Warping to make up the difference."
- **Epic, Motion Warping** (page). Skew and scale warps, windows and bone targets. No limit is given on how far an animation may be bent.
- **Mafia.** Stride warping clamped to 0.5–1.5 (studies/07-animation.md, read from its files).
- **Kingdom Come II.**
  - Stops are chosen by a distance window (0.6–2.1 m) and the quarter of the stride (study 7). That is choosing, not adjusting.
  - Sits start at frame 0 from the clip's own entry, 0.23–2.54 m out, aligned from 0 s (SPOTS).
- **Autodesk patent US8373706B2** (Michael Girard; filed 2008, granted 2013; read in full on patents.google.com). Walking to a chair:
  - Footstep plans are precomputed.
  - Stride length is set by blending a short-stride walk with a long-stride walk.
  - Steps are registered so that a step on the same foot joins the performed motion's first step, with a mirrored set for the other foot.
  - At runtime the plan is looked up. No product is named (U).
- **Epic's own sample** (section 1) takes the opposite way: it chooses the moment by the feet and lets the warp absorb up to 50 cm.

**Verdict.** Planning the steps is the exact method in the literature, but it needs control of stride length. Tom's walk is the sample's motion matching, driven by stick input. No reference was found for adjusting a walk-in to bring a foot into step. This direction comes second.

## 4. Recommendation: the sample's own search, called from C++, inside a widened tested band

Reference: Epic's Game Animation Sample (section 1).

**Design.**
1. Keep step 5, the approach line and the fallback as they are.
2. On the line, each frame while his distance to the slot lies inside the room-tested band, evaluate CHT_SmartObject_BenchAnim from C++ as in section 2, with TargetAngle forced to the kept entry's side.
3. Start when all three hold; otherwise try the next frame:
   - Cost ≤ 1.0;
   - the returned clip is a kept entry. Where only one foot was kept, about half the matches are lost (I);
   - the clip's place at StartTime lies inside the tested envelope.
4. Play from StartTime with the montage's own 0.25 s blend (the sample's), not our 0.2 s. The warp stays as now.
5. Rerun the room test (step 4) for the kept entries with the along corners widened from ±15 to **±50 cm**, the sample's MaxDistance. Then every start the search may return has been tried against the walls.
6. Log per walk-in: cost, start time, the clip's planted foot against his, and the along, across and angle errors.

**The check.**
- Run -TomSitApproachTest's 9 walk-ins, then 9 more at a slower walk. Each set needs at least 8 of 9 started by the search, with the fallback taking at most 1.
- At every start, the clip's planted foot matches his and the cost is at most 1.0.
- Step 7's numbers:
  - planted-foot slide no more than 3 cm during the warp;
  - attach bone within 2 cm and 3 degrees at the window's end;
  - hips within 5 cm, and within ±3 cm in height;
  - no room contact deeper than 1 cm.
- Then films and a fresh reviewer per view, as the gate requires.
- If the slide fails because the warp absorbs too much, narrow the along acceptance to ±25 cm. Only after that, take section 3's direction as a later design.

**Cost.**

| Work | Hours |
|---|---|
| C++: module, two structs by reflection, pose history, the call, the log | 3.0 |
| Room test widened and rerun | 1.0 |
| Walk-in runs and numbers | 1.5 |
| Packaged run (the chooser's internal database must cook) | 1.0 |

**About 6.5 hours, likely 5 to 9.** The films, the page and the packaged gate stay as SPOTS items G and H.

**Unverified.**
- That the C++ call works and that the Blueprint distance channel reads TargetDistance from our context. The context is built in the table's own order to make it the same as the sample's.
- That a match under 1.0 exists on most walk-ins inside the band. The sample's numbers suggest it; nothing has measured it here.
- Foot slide when the warp absorbs up to 50 cm.
- Cooking of the internal database for the packaged game.
- The meaning of the velocity check.

## Not reached

- Epic's 5.8 sample blog (403).
- No Epic page documents the bench, the Pose Match column's outputs, or evaluating a chooser from C++. The Choosers page covers Blueprint only.
- No shipped game's account of foot alignment for sitting was found. GDC talks are video only and were not searched.

## Sources (read 29 October 2026)

- **Sample assets (ue-probe/Content):**
  - Blueprints/SmartObjects: AC_SmartObjectAnimation, PSS_SmartObject, DistanceToSmartObject, SmartObjectSelectionInputs and SmartObjectSelectionOutputs, CHPA_SmartObject, Bench/CHT_SmartObject_BenchAnim, Bench/CHPT_SmartObject_Bench, TasksAndConditions/STT_PlayAnimFromBestCost;
  - Blueprints/AI/StateTree/ST_Player_SandboxCharacter_SmartObject;
  - Blueprints/SandboxCharacter_CMC_ABP;
  - all ten Interactions/Bench/M_interaction_bench_into_*_Montage.
- **Engine 5.8 (C:/Program Files/Epic Games/UE_5.8/Engine):**
  - Plugins/Chooser: ChooserFunctionLibrary.h, IObjectChooser.h, Chooser.h;
  - Plugins/Animation/PoseSearch: PoseSearchLibrary.h, PoseSearchFeatureChannel_Distance.h and .cpp, PoseSearchChooserColumn.h and .cpp, PoseSearchAnimNotifies.h, PoseSearchSchema.h, PoseSearchDatabase.h, PoseSearchHistory.h, AnimNode_PoseSearchHistoryCollector.h, and the Position and Velocity channel headers;
  - AnimDistanceMatchingLibrary.h, AnimNode_StrideWarping.h, AnimMontage.cpp, PlayMontageCallbackProxy.h.
- **Repository:** SPOTS-2026-10-28.md, SPOTS-REVIEW-2026-10-28.md, SliceCharacter.cpp, DECISIONS.md, orders/2026-10-25.md, seat-clips.json, studies/07-animation.md; F:/LedgerTools/scratch/sit/clip_sheet.json.
- **Web** (fetched whole; the fetch tool summarises): dev.epicgames.com/documentation/en-us/unreal-engine/ pages for the game animation sample project, motion matching, pose warping, motion warping, distance matching and dynamic asset selection (all 5.8); patents.google.com/patent/US8373706B2/en.

## Revised after review (29 October 2026)

A fresh review (START-CHOOSER-REVIEW-2026-10-29.md) passed this with fixes. Taken as follows; where this section and the text above differ, this section holds.

- The player's state tree sets the velocity check to 0 (100 is only the task's default); dropped from Unverified.
- Blend and warp curves are the kept clips' own: the behind-right montages blend HermiteCubic, R_090_Rfoot Linear, all over 0.25 s; F_Lfoot's warp curve is the engine default.
- Same-foot plants fall mostly 150 to 170 cm apart, 118 to 137 cm in the behind clips.
- Stride warping's sentence and its 0.75 to 1.25 clamp are cited from AnimDistanceMatchingLibrary.h alone, not Epic's page.
- The band is root travel left; the search measures root to attach bone, 3 to 20 cm different by clip: the band is converted per clip, or the search is gated on travel left.
- THE TARGET (major): with the approach as built only 5 of the 9 walk-ins reach the search (two start out of reach of any seat; two are the door end's behind-right entries with no room to join their path). The third try's check is therefore on the walk-ins that reach the line: 5 of 5 started by the search, at most 1 fallback among them. Reaching the door end from behind-right, and the test's out-of-reach starts, are separate items.
- THE MAIN RISK (major): the middle and counter-end seats keep one foot only (R_090_Rfoot), and one clip's band shifts his step phase by only about 0.3 of a cycle, so a walk-in matches or never does; the chooser's pose column returns one best row, so an unkept clip that scores better hides a kept match. Before the third try, room-test R_090_Lfoot again at 100 and 150 cm for those seats; if it stays dropped, the target for one-foot seats is lowered and said so.
- The check needs measures the approach test lacks: foot slide at the start, the attach bone and hips at the end, room contact during the clip, and a walk-speed switch for a slower walk; about 1 to 1.5 hours to add.
- Cost: about 8 to 11 hours for the check as written.
- Unverified, added: whether a band widened to 50 cm keeps any entry (every entry touched the room from 200 cm); the single-best masking above; the walk-ins that never reach the line.
