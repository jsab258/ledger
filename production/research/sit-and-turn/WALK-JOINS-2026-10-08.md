# Walk joins without foot slide: method and steps

8 October 2026, item 1.2. **D** read at source today; **S** search summary only; **I** inference, untested. Nothing run in Unreal.

## 1. The professional method

- **Join where poses match.** A set's starts and stops begin and end in its own idle; motion matching makes that choice from data (I; GASP picks starts by future velocity, D [3]). Our 27 cm was measured against mh001's idle, never against the set's own `AS_MH_Neutral_Stand_Idle_Loop`, which sits beside the starts and stops (D [6]).
- **Inertialize, don't cross-fade.** Only the destination is evaluated; the old offset decays (Bollo, S [9]; Holden, D [8]). A 5.8 montage blending by Inertialization takes full weight at once and the old one stops, so one clip's root motion counts; it needs an inertialization node after the slot (D [11]). Lyra's montages use it (D [2]).
- **Lock planted feet, release in the air.** Holden locks the toe at contact, unlocks when contact ends or the toe drifts 20 cm, decays the offset with a 0.1 s half-life, then two-bone IK (D [7]). ALS: a lock curve per foot that may only fall while moving; foot = lerp(animated, locked) (D [10]). Epic's Foot Placement locks by foot speed, pivots round the ball, unlocks past 35 cm or 45°, springs back (D [12]).
- **A lock hides centimetres, not a stance.** Past the unlock radius the foot slides. Big differences go by clip choice, a step (the stop's shuffle) or warping the travel (I).
- **Distance matching and stride/orientation warping** fit clips to capsule movement (D [1], [2], [4]); with root motion they do nothing for our joins; warping needs IK foot bones.
- **Foot Placement** (5.8 AnimationWarping) is marked Experimental; it needs IK foot bones (ours have none), pelvis, ball, Leg IK after; without a Character it assumes grounded (D [12]).

## 2. What our joins do wrong (code D; effects I)

1. **Ankle held, ball measured.** Our IK pins foot_l's position but keeps the clip's foot rotation (D [13]); as the heel lifts, the ball swings round the ankle.
2. **Held foot out of reach.** The left (stance) foot is held at the idle's place, 27 cm from the start's own, and nothing moves the body to close it; stretching is off, so the foot drags: the 13–20 cm first step.
3. **The stop blends into the wrong idle on planted feet.** Blend-out starts when time left equals the blend-out (D [11]): for 0.3 s mh001's stance pulls both planted feet before the hold begins: likely the 18–27 cm.
4. **The body moves a frame late.** WalkProofTick runs on the core ticker, after the world tick and the draw (D [14]): each frame shows the new pose at the old place, about 2.5 cm at 60 fps at walking pace. CharacterMovement moves before the mesh evaluates (D [14]).
5. **The stop's bake slips 3.9 cm**: its root goes back 4 cm after frame 8 with both feet down (D [15]).

## 3. Steps, smallest first (hours I)

| # | Step | Test | h |
|---|---|---|---|
| 1 | Editor measure: Stand_Idle_Loop's feet against the start's first frame and the stop's last; at joins, the stance foot only (a swinging foot's mismatch is a shorter step) | match ≤ 3 cm | 0.5 |
| 2 | If so: walkers stand on Stand_Idle_Loop (body only; face keeps its idle), staged for the package | proof: first step, stop ≤ 3 cm | 1–2 |
| 3 | Move her before the pose evaluates (pre-actor-tick, this frame's clip time) | -WalkProofNoHold steady steps ≤ 3 cm | 1–1.5 |
| 4 | Lock the ball: ankle target = locked ball + clip's ball-to-ankle; every contact; release at lift or 10 cm drift, 0.1 s half-life | every footfall ≤ 3 cm | 2–3 |
| 5 | Stop bake: root still after last contact; stop entry by stance foot | walk_slip stop ≤ 1 cm | 1 |
| 6 | Only if 1 fails: spread −(lock − clip's stance ball) into travel before that foot lifts, capped 30%; beyond, a shuffle | leg reach < 0.98; slip ≤ 3 cm | 2–3 |
| 7 | Inertialized montage switches, dead-blending node after the slot | pelvis jump ≤ 2 cm | 1–2 |

**First: step 1.** Half an hour, no build, and it decides the rest: if the set's idle matches, the 27 cm goes the professional way and steps 3–5 clean centimetres; if not, step 6 is needed, since IK cannot absorb 27 cm on a stance foot. Then step 3, which biases every measurement. Total 5–8 h; 6.5–10 h with step 6 (I).

## Sources (8 October 2026)

1–4. Epic docs, dev.epicgames.com/documentation/en-us/unreal-engine/: distance-matching-; animation-in-lyra-sample-game-; game-animation-sample-project- (sample unopened); pose-warping-in-unreal-engine. Read.
5. Epic Python API, AnimNode_FootPlacement. Search only; no user guide found.
6. MetaHuman plugin, UEFNAnimPreset/Locomotion folder. Disk.
7. D. Holden, github.com/orangeduck/Motion-Matching, controller.cpp. Read via fetch.
8. D. Holden, theorangeduck.com, "Dead Blending" (25 Feb 2023), "Spring-It-On" (2021). Read.
9. D. Bollo, "Inertialization", GDC 2018, gdcvault.com/play/1025165. Abstract via search.
10. github.com/Sixze/ALS-Refactored, AlsAnimationInstance.cpp. Read via fetch.
11. UE 5.8 AnimMontage.h/.cpp. Disk.
12. UE 5.8 AnimationWarping (FootPlacement, OffsetRootBone, StrideWarping) and AnimationLocomotionLibrary (Beta). Disk.
13. UE 5.8 AnimNode_TwoBoneIK.cpp. Disk.
14. UE 5.8 CharacterMovementComponent.cpp, LaunchEngineLoop.cpp, GameEngine.cpp. Disk.
15. Project: PersonAnim, WalkProofTick, F:\LedgerTools\scratch walk_*, METHOD, LOCOMOTION. Disk.

Unreached: none.
