# Tom's walk by motion matching: the trial, 22 October 2026

His order of 21 October, item 7: "Tom's walk rebuilt on Epic's Game Animation Sample with motion matching; foot slide measured at the joins, at or under 3 cm." **Result: not passed.** The motion-matched walk is built and runs, but it stays off by default (`-LedgerMotionMatch` turns it on). Its starts, stops and turns slide far over the bar. Tom's own clips remain his walk.

## Questions

1. How does the Game Animation Sample (GASP) drive its character, node by node and setting by setting?
2. Can that run in this project, which has no Blueprint assets, inside a packaged game?
3. With it, do Tom's planted feet slide 3 cm or less at starts, stops and turns?

## Sources (all read on 22 October 2026, on disk; nothing reached over the network)

- **The sample itself**, `F:/LedgerTools/GameAnimationSample` (Epic, Fab; allowed by his 13 October ruling). Its animation blueprint `SandboxCharacter_CMC_ABP` and character `SandboxCharacter_CMC` were exported to text by the editor (`F:/LedgerTools/game-inputs/gasp/exports/gasp_abp.t3d`, 31 MB; `gasp_cbp.t3d`) and read node by node. Its chooser `CHT_PoseSearchDatabases_Sparse` is kept here as `tom-walk-2026-10-22/gasp-chooser-sparse.txt`. The character's speed defaults were read from its class defaults.
- **Engine 5.8 source** under `C:/Program Files/Epic Games/UE_5.8/Engine/Plugins/Animation`:
  - `PoseSearch`: `AnimNode_MotionMatching.cpp`, `AnimNode_PoseSearchHistoryCollector.cpp`, `PoseSearchTrajectoryLibrary.cpp`, `PoseSearchLibrary.h`.
  - `AnimationWarping`: `AnimNode_OffsetRootBone`, `AnimNode_Steering.cpp`, `AnimNode_FootPlacement.cpp`, `AnimationWarpingTypes.h`.
  - `Engine/Classes/Animation/AnimNodeBase.h` (`GetData`, `check(NodeData)`).

## What the sample does (measured from its own files)

- **The main chain.** Motion Matching (its blend stack graph holds Orientation Warping, Reset Root and two Steering nodes) → lean additives → Slot → Offset Root Bone → Remap Curves → Foot Placement → Leg IK → Pose History → output.
- **Motion Matching.**
  - Blend 0.5 s with the `FastFeet+Root_Weight` profile, Hermite.
  - Play rate 0.85 to 1.15.
  - Notifies filtered.
- **Offset Root Bone.**
  - Translation interpolates while moving and is released when idle. Half-life 0.3 s moving and 0.1 s idle.
  - Never more than 30 cm.
  - Rotation is held (Accumulate), so the clips and the Steering nodes do the turning.
- **The chooser.** Standing searches:
  - the idles below 20 cm/s;
  - walk stops from 20 cm/s;
  - run stops from 100 cm/s;
  - turn-in-place, only on the frame he stops with the body 50° off.

  Moving searches the loops, plus the starts (speed ahead ≥ speed + 100, not pivoting) and the pivots. Searched together, turn-in-place wins every search, because its base cost bias is −0.2.
- **The interrupt.** Interrupt on a database change happens only on the frame the movement state (or the gait, while moving) changes. Otherwise the current clip continues.
- **Its movement.**
  - The capsule turns instantly (rotation rate −1).
  - Acceleration 800, ground friction 5, braking-friction factor 0.
  - Braking 2,000 when the stick is released and 500 while pushed.
  - Walk 200 cm/s, run 500 cm/s. Tom's are 160 and 420.

## What was built

- **The walk graph.** An animation blueprint, `ABP_TomMotion`, made by script and never by hand (`tools/ue/make_tom_retarget.py` calling `ULedgerMotionMatchTools::WireMotionMatchBlueprint`). It holds the sample's main chain and settings, with three changes: play rate 0.75 to 1.25; no Steering inside the blend; no curve remap. The parent class `ULedgerMotionMatchAnim` makes the sample's choice of sets and interrupt each update, and hears its footstep notifies.
- **The hidden mannequin.** It runs that graph beside Tom. Tom's body copies its pose through `RTG_UEFN_to_TomPlayer` (Retarget Pose From Mesh, native).
- **The measure.** `-TomWalkProof` walks a set route along the clearest line in the street:
  - 3 s standing;
  - a 4 s walk;
  - a stop;
  - an about-turn from standing;
  - an about-turn while walking;
  - a 45° turn and back;
  - a stop;
  - a 2.5 s run back;
  - a stop.

  Each foot counts as planted when its ball is within 2.5 cm of its standing height and no higher than the other foot. Its drift along the ground is measured once the frame's pose is final. Both bodies are measured: Tom and the mannequin.

## Results (Tom's feet, per contact; median / share over 7 cm / worst, cm)

Corrected the same day after the fresh review of phase 1's Exit B. The first table gave only medians and the printed contacts' worst; it hid that in his own clips his right foot slides 27 to 36 cm on every steady stride. Each worst is now the run's own header line, which counts contacts still planted when a stretch ends.

| | starts | stops | turns | walk loop | run | all steps over 7 cm |
|---|---|---|---|---|---|---|
| Motion matching (final) | 23.4 / 2 of 4 / 53.4 | 66.7 / 4 of 5 / 101.8 | 13.2 / 5 of 8 / 43.3 | 4.8 / 5 of 15 / 88.4 | 4.7 / 1 of 7 / 12.4 | 17 of 39 |
| His own clips (the walk he has) | 26.9 / 3 of 5 / 35.6 | 20.4 / 2 of 2 / 30.8 | 3.5 / 8 of 18 / 43.4 | 3.4 / 15 of 40 / 80.2 (his right foot 27 to 36 on each stride) | not read* | 35 of 72 |

\* The clip run lowers his body 21 cm (RunDropCm), so the measure, calibrated standing, reads both feet as always planted.

The mannequin's own feet slide as much as Tom's, so copying the pose onto Tom adds nothing: the slide comes from the motion matching.

**Both walks fail the bar, each on about half its steps.** The motion-matched walk is worse at stops and steadier in the run and the loop; his own clips' right foot slides on every stride. Neither is better overall. The default stays his own clips, so the player sees no change until one passes. That is the reason; it is not that his clips are better.

## What failed and why (in order)

1. **Built in code alone (no blueprint).** The engine's Motion Matching and Offset Root Bone nodes read some settings through `GET_ANIM_NODE_DATA`, which in a game without editor data calls `check(NodeData)`. A packaged game would stop. Hence the script-made blueprint.
2. **All sets searched at once.** He turned on the spot while walking (turn-in-place's −0.2 bias). Fixed with the sample's chooser.
3. **The route.** The first-day tour holds the player's feet, and he walked into people and walls. Fixed by measuring through it and taking the clearest line.
4. **Movement unlike the sample's** (instant stop): stops slid 40 to 56 cm. With the sample's movement and interrupt rule, the first stop measured 7 to 11 cm.
5. **Root rotation eased instead of held.** The instantly turning capsule swung his planted feet 40 to 100 cm at turns. Held (as the sample does), the turns while walking improved but the turns from standing did not.
6. **Dense sets** (the sample's own player's). The steady walk slid more: 15 to 24 cm against 3 to 6.

What remains: the first one or two contacts of each start and turn slide 20 to 100 cm. The per-frame trace (`tom-walk-matched.txt` from an earlier run with `-TomWalkProofTrace`) shows the back foot moving 34 cm in 0.15 s at ground height as the first clip blends in. That is too fast for Foot Placement to treat it as planted. In the sample, the Steering and Orientation Warping inside the blend stack keep each clip's turning aimed at the desired facing; that is the piece not built here.

## Next directions (set aside after more than two tries: his rule)

- **A. Build the blend stack graph by script.** Build the sample's blend-stack graph inside the Motion Matching node the same way: Orientation Warping, Reset Root and two Steering nodes, fed by `GetCurrentBlendStackAnimAsset`/`Time` and a desired facing (the sample's `Get_DesiredFacing`). The export gives every setting.
- **B. Drive the sample's own character.** Use `SandboxCharacter_CMC` unchanged, hidden, as a puppet. Feed it Tom's input and speeds by reflection, and have Tom follow its capsule. Every Epic node and function stays as Epic made it.
- **Either way, onto MetaHuman Tom.** The walk then goes onto Tom's MetaHuman body (approved face L1) through Epic's own `RTG_UEFN_to_Metahuman` retargeters, which are already in the project. Epic's garments (item 7's second half) need that body anyway.

## Direction B already exists in the sample (read on disk, 22 October 2026, 17:40)

The sample's own content (F:/LedgerTools/GameAnimationSample/Content, listed on 22 October) ships Epic's path for a different visible body:
- `Blueprints/AC_VisualOverrideManager` and `Blueprints/RetargetedCharacters/ABP_GenericRetarget`: its own character keeps running its own graph, and a second mesh copies the pose through a retargeter.
- A MetaHuman, `MetaHumans/Kellan`, with `MetaHumans/Common/Common/Rigs/RTG_UEFN_to_Metahuman_nrw` and `_ovw`.
- The same for Echo, TwinBlast and both mannequins.

So direction B is Epic's built and shipped method, and the right next go for Tom's MetaHuman body: the sample's character as the mover, Tom's body worn over it. How `AC_VisualOverrideManager` picks and drives the mesh is not yet read (its blueprint is not exported); that is the first step of the next go. **Not started:** the walk is set aside under his two-tries rule, so the next go waits for his yes (FOR-JAFAR.md, Needs you).

## Cost

About 3.5 hours on 22 October (09:00 to 10:15 build and measure loops after the morning's set-up; GASP migration and retargeter earlier).

## Evidence

- `tom-walk-2026-10-22/tom-walk-matched.txt` and `tom-walk-clips.txt`: the route's lines, every contact.
- `tom-walk-2026-10-22/gasp-chooser-sparse.txt`: the sample's chooser as exported.
- The sample's full exports are on F: (`F:/LedgerTools/game-inputs/gasp/exports/`: `gasp_abp.t3d`, `gasp_cbp.t3d`, the three choosers). They are 31 MB and 9 MB, too large for git and kept there.
