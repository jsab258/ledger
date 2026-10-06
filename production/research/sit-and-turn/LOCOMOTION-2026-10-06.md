# In-place clips: the professional method and Ledger's cheapest route

Item 1.2, after step 3's second failure, 6 October 2026. **O** = opened and read today ("O, disk" = a file on this PC); **S** = search summary only; **I** = inference, untested. Nothing was run in Unreal.

## 1. How Epic drives in-place clips

- **Lyra**: the capsule moves the body; starts, stops and pivots are distance matched (time picked from a distance curve), then stride warping into the loop; turns use Root Yaw Offset and curves baked from root motion (O).
- **The distance curve** is made by the Distance Curve Modifier from root motion (O, docs); its code refuses a clip with root motion off (O, disk), so a clip without travel gives no curve (I).
- **Warping**: Epic's page asks for root-motion clips and IK foot bones (O); in the code, Manual mode reads no root motion (O, disk). The cast skeleton has no IK foot bones (O, METHOD).
- **GASP**: motion matching on a capsule-driven body, plus offset root bone and orientation warping (O). Motion matching clips "must contain root motion" (O, Epic). Its 5.8 update sits people on benches by smart objects and motion matching (O, The Rookies, 24 Aug 2026; Epic's post 403). It wants a large mocap set (Clavet, GDC 2016, S).
- **Paragon** (Delayen, nucl.ai, 23 Nov 2016): distance matching to world points; stride-length warping up to 60%, play rate 15% more (O, Game Developer summary, 24 Jan 2017).
- **The retargeter's Root Motion op** only copies the source root or follows the pelvis (O, 5.8 op stack page). Neither can invent travel, so step 3's 0.0 cm was certain (I).

**From native code** (O, disk): sequence evaluator, Leg IK, Two Bone IK (AnimGraphRuntime); the warping nodes (AnimationWarping, stable; placed like the Look At node, I); stop prediction (AnimationLocomotionLibrary, Beta). Its distance matching calls need Blueprint node references; the private lookup is ~40 lines to copy. Motion matching (PoseSearch, pulling in Beta MotionWarping) needs editor-made databases.

## 2. What the plugin's clips carry (O, disk)

All 25 clips' registry tags: curve list empty, no notifies, no attributes, root motion off, 30 fps. Markers L and R on loops and starts only. No name table holds Distance, Speed, Disable_*, Footstep or a turn curve; the only curve-like names are ~300 `*_CONTROL` entries of an editor-only rig track. Confidence high: the editor writes these tags from the clip's curves. The preset files beside them hold only a clip, a start time and a play rate (optionally speed-scaled, 0.5 to 1.25); Fortnite's graph using them is unreached. Distance matching cannot run on them as shipped: no curve, no travel to make one.

## 3. Options, ranked

Key fact (I, measured first below): an in-place clip keeps its travel in the planted foot, which slides backward at walking speed. Writing that speed into the root bone, pelvis keys untouched, makes the clip travel. Editor scripting can: AnimPose reads bones in component space; SetBoneTrackKeys writes root keys (O, disk).

1. **Foot-baked root motion** and a Distance curve, made in the import script, played through the proven slot and driver; a walker's stop starts when the distance left equals its baked travel, foot chosen by the loop's markers. 6–9 h (hours all I). Risk: foot changeover frames; a 3.2 s start may feel slow for Tom.
2. Route 1's clips, capsule-driven with distance matching, for Tom. 8–12 h more. Risk: Beta library, tuning.
3. Runtime foot lock: move the actor against the planted foot's movement. 2–4 h. Risk: a frame's lag, jitter, no stop distances.
4. Mixamo starts and stops with travel. 3–5 h. Risk: style seam with Epic's loops; Female Stop Walking reads 2.37 m in 0.8 s (O, clip-motion.py).
5. Stride and orientation warping. 6–10 h. No IK foot bones; polish only.
6. Motion matching. 30+ h. Needs root motion, a large set, editor assets; GASP data NoAI.

**Turns**: Mixamo Turn Left 90 reads 88.8° and 2 cm (O, clip-motion.py), sound; Turn Right 90 reads 13.8° and 2.05 m, wrong: re-download or mirror. **Sit and stand**: as the method says (Mixamo with travel; following the pelvis works there).

**Recommended: route 1**, the third try, in a new direction; route 2 for Tom after.

## 4. Next experiment

**Build**: a foot bake in make_root_motion_clips.py, same five clips: sample at 30 fps; ball_l and ball_r in component space; planted foot = the lower (1 cm hysteresis; averaged when both are down); body velocity = minus its horizontal velocity; integrate into root keys; root motion on; Distance curve written. Log travel and loop speed.

**Measure first**: the loop's baked speed. 1.0 to 1.6 m/s goes on; under 0.3 m/s the clips march on the spot and the route is reported dead.

**Then**: -MoveProof on Sheila (start, loop, stop), packaged, filmed at the hook camera.

**Pass**: over 1 m per start; planted-foot drift under 2 cm per step, median under 5 cm/s; pelvis jumps under 2 cm between clips; a fresh reviewer sees no slide.

## Sources (6 October 2026)

Epic docs, UE 5.8, undated, O: dev.epicgames.com/documentation/en-us/unreal-engine/ distance-matching-in-unreal-engine, pose-warping-in-unreal-engine, animation-in-lyra-sample-game-in-unreal-engine, game-animation-sample-project-in-unreal-engine, motion-matching-in-unreal-engine, retargeting-operation-stack-in-unreal-engine-5-8; UEFN animation-presets (no detail). therookies.co, GASP 5.8 (24 Aug 2026). gamedeveloper.com, game animation talks of 2016 (24 Jan 2017). gdcvault.com/play/1023280 (S).
Disk: clip and preset assets; engine sources (four plugins, AnimPose, IAnimationDataController); PersonAnim.h; clip-motion.py.
Unreached: Epic's GASP 5.8 post (403); the Paragon talk video.
