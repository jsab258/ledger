Method researched: production/research/tool-tests-2026-11/CASCADEUR-METHOD-2026-11-12.md (motion clean-up: contact pinning, then leg straightening and physics, read 2026-11-12), and the tool's own README, MECHANICS and CREDITS (read 2026-11-12 23:15).

# Motionsmith, round 1 (12 Nov 2026, 23:15 to 23:55, the session alone, no helpers)

His own replacement for Cascadeur (C:\Game Dev Tools\Motionsmith), advisor 119 and 120. Work folder F:/LedgerTools/tool-tests-2026-11/motionsmith-r1; nothing written into his folder; nothing enters the game.

## Verdict

**Level 2 (can the builder use it): passes clearly, better than Cascadeur.** Every job runs from a job file with no click, in 1 to 3 s, same bytes twice (28 of 28 FBX), with a pass/fail file, a log and a film; Unreal 5.8 imports its FBX onto Epic's MetaHuman skeleton and exports back the same motion (knees, elbows, pelvis height identical to 0.001).

**Level 1 (is it good at the job): not yet shown on our faults.** Its own stand-in captures carry mild faults (knees about 3.5 degrees bent by an independent measure), and it fixes those. Our real head-turn solve had standing knees bent 28 to 35 degrees; by its own rule (MECHANICS: "knees bent more than 18.19 degrees are left alone (crouch, sit)") it would leave them bent. Below that limit it straightens knees that are bent on purpose: fixing its own clean moves changed them by up to 15 degrees (crouch, sit-down) and 42.6 degrees (the relaxed leg of the counter lean). The sit-down from five key poses passes every physics bar on two bodies; whether it looks natural is unjudged (stick-figure film only).

**The real-clip jobs did not run:** the session deleted the head-turn solve and the chair-rise control solve at 23:02 with a folder it had listed as its own unused leftovers (DECISIONS, 12 Nov 23:12). Remaking them is round 2's first step.

## The tests

| Job (advisor 119) | Run? | Result |
|---|---|---|
| Head-turn solve, real clip (knees within 5 deg, toes, slide 1 cm or less, timing) | no, input lost | stand-in clip: all bars met (below) |
| Real-footage chair rise | no, input lost | not run |
| Sit-down from key poses | yes, medium and heavy bodies | physics bars met; look unjudged |
| Its 23-move library (sitting, leaning, hands, idles, turns, starts, stops) | yes | 23 of 23 pass its own checks |
| Unreal import | yes, 3 files (head-turn, sit-down, walk stop) | read on metahuman_base_skel, round trip identical |
| Fix of an already clean move (should change nothing) | yes, 3 moves | changes knees by 15 to 43 degrees |

## Numbers

Independent measure in Blender 5.2 (tools/tool-tests/measure_fbx_legs.py), beside the tool's own checks.json:

| File | Ball drift while planted L / R (cm) | Standing knee bend L / R (deg) | Floor (lowest point, cm) | Tool's own verdict |
|---|---|---|---|---|
| Stand-in head-turn (input) | 3.38 / 4.64 | 0.2 / 3.5 | -4.2 (a foot through the floor) | before: slide 3.5 / 4.6, knees 6.3 / 6.4 |
| Its fix | 0.06 / 0.08 | 2.5 / 2.5 every frame | +0.85 (ball joint, sole on the floor) | pass, timing correlation 1.000 |
| Fix on the tall body | 0.06 / 0.09 | 2.5 / 2.5 | +0.81 | pass |
| Sit-down, medium body | 0.0 / 0.0 | 2.5 standing, 88.9 seated | +0.8 | pass |
| Stand up from a chair | 0.0 / 0.0 | 2.5 to 90.9 | +0.8 | pass |
| Walk stop | 0.27 / 1.34 (my detector; may count the last step's roll) | 11.9 median | +0.8 | pass |

Our real head-turn solve, for the bar (CASCADEUR-TEST4): slide L 2.6 / R 0.8 cm, knees 28 / 28 median (35 worst), left ball 1.8 to 2.9 cm up. Cascadeur after Fix Foot: slide met, knees 11.5 / 29.3, balls 1 to 2 cm into the floor.

Fix of clean moves (motionsmith --compare, input against output):

| Move | Largest knee change | Its checks "before" on its own clean move |
|---|---|---|
| Crouch | 15.2 deg | slide 1.78 cm, standing knee 17.7 deg (fails its own fix bars) |
| Sit-down | 14.8 deg | standing knee 17.3 deg |
| Lean on a counter | 42.6 deg (left, the relaxed leg) | slide 1.88 cm, knee 16.5 deg; only 2 frames counted as standing |

Time: 0.9 to 2.7 s a job with film (28 jobs in 46 s), about 1 s without. Unreal check: one commandlet run, exit 0. Builder time for the round: about 0.7 h, logged ("tool test: Motionsmith round 1").

## What works

- No clicks anywhere: job files, a command line, a Python wrapper; exit code 0 or 2; checks.json with before and after for every bar; a log with file fingerprints; a film beside the input; a four-moment preview; editable key poses from any clip.
- Same input, same bytes: 28 of 28 outputs identical across two runs.
- Unreal reads it as it is: classic FBX importer, Epic's MetaHuman skeleton, every body bone keyed, 30 fps; the round trip changes nothing measurable.
- 18 MetaHuman bodies by word or code; a move made once is refitted by leg length (sit-down on the heavy body passes).
- Contact pinning is exact on the stand-in: 0.06 to 0.08 cm drift, no floor penetration, timing kept to the frame.
- A move library of 23 period-useful moves (sitting, leaning, cigarette, pockets, door, envelope, idles, turns, starts, stops) with root motion for the walking set.
- No GPU; MECHANICS.md lists every number and its source, estimates marked.

## What fails, and why

1. **The leg rule cannot fix a sunk-pelvis solve.** Standing legs are straightened only when bent under 18.19 degrees; above that they are taken as a crouch or sit. Video solves bend standing knees 28 to 35 degrees (ours). So the job the tool exists for is the one case it leaves alone. Cause: "standing" is decided from the knee angle, not from what the body is doing (feet planted, pelvis height against leg length, the clip's own still frames).
2. **Not a no-op on clean motion.** Below the limit, deliberate bends are flattened to 2.5 degrees (the relaxed leg of a lean straightened by 42.6 degrees). Cause: the same rule, plus a fixed 2.5-degree target on every standing frame (the knee reads exactly 2.5 on all 150 frames, which looks locked rather than alive).
3. **Its own moves fail its own fix bars** (slide 1.8 cm, knees 17 degrees "before") although their make checks passed: make and fix judge with different definitions of planted and standing.
4. **The stand-ins are too easy.** Knees about 3.5 degrees (its checks say 6.3), slide 3 to 5 cm, one foot through the floor; our real faults are about eight times the knee error.
5. **Perfect symmetry** in made moves: left and right knees identical to the decimal through the sit-down and stand-up; fingers at rest. Likely to read mechanical in the game; unjudged until a body is filmed.
6. **Films are stick figures**: no body mesh, so "natural" cannot be judged from the tool; it needs our packaged film.
7. Unreal's frame count reads one less than the tool's (66 against 67): Unreal counts intervals; not a fault.
8. Its README opens with a line saying the build "contains the original game's own files"; CREDITS names only Epic's MetaHuman skeleton data. Most likely boilerplate; noted, not judged.

## Improvements, most useful first

1. Decide "standing" from contact and pelvis height (feet planted, both soles near the floor, pelvis within a band of the body's standing height), not from the knee angle; then straighten every standing knee whatever its bend, and leave knees alone only where the pelvis is genuinely low (sitting on a seat, a crouch the keys ask for).
2. An identity case in its own tests: fixing any library move must change it by under 1 degree and 0.5 cm; run it on all 23 moves.
3. One definition of planted and standing shared by make, fix and the checks.
4. Stand-ins with real solve faults: standing knees 25 to 35 degrees, pelvis 5 to 8 cm sunk, a ball 2 to 3 cm up and another 1 to 2 cm under, foot slide 2 to 3 cm. Our real head-turn numbers are in CASCADEUR-TEST4 for the shape.
5. Let the standing knee breathe: a small range (1 to 4 degrees) following the input's own rhythm instead of a fixed 2.5.
6. Left-right variation in made moves (a few degrees and frames of offset), and fingers that relax and curl with the hands.
7. A body-mesh film (the MetaHuman body from the DNA, flat-shaded) so the look can be judged from the tool.
8. A --compare mode against a reference clip's joint angles, so a fix can be judged against a real person's motion, not only bars.

## Next (round 2)

1. Remake the inputs: the kept stock clip re-solved through tools/ue/mocap-solve-project (about 35 min of processor time, outside 01:15 to 04:30), and the head-turn if its source can be remade; then the head-turn and chair-rise jobs on them, numbers beside Cascadeur's.
2. The identity check and the stress clip above on any update he makes.
3. The sit-down and stand-up filmed packaged on a MetaHuman beside the current ones, for a fresh reviewer, only once the leg rule holds.

## Files

F:/LedgerTools/tool-tests-2026-11/motionsmith-r1/: jobs-a, jobs-b (job copies pointing at his folder for inputs), out-a, out-b (all outputs, films, checks), summary-a.json and summary-b.json (exit, seconds, hashes, checks), measure-a.json (the Blender measures), jobs-stress and out-stress (fix of clean moves), ue_check (the Unreal check copied, ue_result.json, round-trip FBX, ue_run.log). Scripts: tools/tool-tests/motionsmith_r1.py, tools/tool-tests/measure_fbx_legs.py.

## Round 2, 13 November 2026 (05:27 to 06:08)
- Inputs remade: the solve project rebuilt from its kept source (tools/ue/mocap-solve-project, copied to C:/LedgerTools/mocap-solve, editor build 66 s), the kept stock cut (Pexels 6615631 reversed, rise-430-230.mp4, 201 frames at 24 fps) re-solved on the processor: every stage ok, 2,234 s (37 min), /Game/MocapSolve/rise430s_Body, exported to F:/LedgerTools/tool-tests-2026-11/motionsmith-r2/rise430s_Body.fbx (342 bones). The head-turn cannot be remade: its source video was lost with the solve on 12 Nov, no copy.
- Motionsmith's fix job on it (motionsmith-r2/jobs/01_rise_fix.json, our pass bars): ALL PASSED. Foot slide 21.6 and 25.8 cm down to 0.4 and 0.5; sole tilt 28.0 to 0.5 degrees; floor 2.3 to 0.0 cm; timing untouched (correlation 1.000). But it found 0 standing frames and did not straighten the knees: the solve never brings him upright (preview: crouched, the last two moments the same pose, as in the 12 Nov control solve). Picture: production/previews/motionsmith-round2-rise-2026-11-13.jpg.
- What it says: its feet fix is real on real footage; its checks pass a move that never reaches its goal. A check that the clip ends standing (or reaches the move's named end pose) is missing; the leg fault is the solver's, beyond what a clean-up can repair.
- Cascadeur beside it: none to compare (test 4 set aside, 2 of 2). The identity check and the stress clip wait for an update from him (none since round 1).
- Cost: about 0.6 h of session time, 37 min of processor, no helpers. Time log: "tool test: Motionsmith round 2 re-solve".
