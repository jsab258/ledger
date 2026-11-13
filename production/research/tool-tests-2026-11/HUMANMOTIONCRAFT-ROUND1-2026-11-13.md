Method researched: production/research/tool-tests-2026-11/MOTIONSMITH-ROUND1-2026-11-12.md (the same moves and measures, 12 and 13 Nov) and HumanMotionCraft's README.md (v0.3.0, read 13 Nov 2026)

# HumanMotionCraft 0.3.0, round 1 (13 November 2026): the headless half

His pick (advisor 132, his tap and typed approval 14:12, advisor 141): test HumanMotionCraft, not his tool, test only, nothing enters the game. Its code is GPL-3.0 (used as a tool), rig and mannequin Apache-2.0/CC0, clips from CMU (allowed) and 100STYLE (CC BY 4.0, outside the allowlist for motion). Official Windows release v0.3.0 (31 Oct), SHA-256 matching its SHA256SUMS, unpacked in F:/LedgerTools/humanmotioncraft/app-0.3.0; driven only through its command line `ac.exe` by one helper (no clicks, no network, no installs; the motion-from-text install skipped). Work folder F:/LedgerTools/humanmotioncraft/test-r1 (commands.log, scripts, out/*.glb, pics/ strips). Still to do: the Unreal retarget onto a MetaHuman, the leg and foot measures there, and a packaged film for a fresh reviewer, beside Motionsmith and the CMU route.

## Verdict so far
**Drivable: very good.** 167 typed commands; a whole move (keys, learned in-between fill, checks, two exports, contact strips) runs as one script in 2 to 3 s; same result every run. **Good at the job: partly.** The sit and stand reads right and ends where it started; the counter lean holds hand and feet; the smoking draw is wrong by eye (the hand covers the face). Its own checks are strong and caught real faults, but its foot-slide figure contradicts the planted bones.

## Numbers (30 fps; keys from its library poses, AI fill between, feet planted after)
| Move | Result |
|---|---|
| (a) sit down and stand up, 120 frames, 45 cm box | pelvis 0.852 m at start and end (0.849 with physics), lowest 0.527; knee 93.7 deg at the deepest sit; planted foot bones move 0.0 cm (our measure); toes move up to 1.5 cm and dip 3.1 cm under the floor; its own slide figure 12 to 15 cm (disagrees) |
| (b) forearm on a 95 cm counter, weight shift, 120 frames | hips sway -5.1 to +5.9 cm; feet 0.0 cm; wrist on the counter 0.0 cm, elbow 1.2 cm; on frames 14 to 23 the left hand passes 25 cm into the counter (its own critique: 26.7 cm); wrist 28 deg past range |
| (c) smoking at a bus stop, two draws, 180 frames | hips +-4 cm, feet 0.0 cm; elbow points down and the hand covers the face (by eye); shoulder 20 deg past range |
| Time | 1.9 to 2.9 s a whole move; the in-betweener 50 to 100 ms |
| Export | valid glTF 2, one skin, one animation; game profile 68 joints, full 104 |

## What works
Every operation a typed command with JSON results; strong self-checks (pose.query, clip.metrics, clip.critique, clip.possible); feet planting holds exactly; box support works (a too-close chair put the feet on it); fast fill with no visible side effects; clean export; an MCP server (16 tools).

## What fails, and why (as far as seen)
1. Its fixtures are missing from the release (`ac fixtures` exits 2), so its self-tests could not be run.
2. Boxes are not drawn in its command-line pictures, so a sit or lean cannot be judged against its chair or counter by eye.
3. Hands near the face need many small rotations; dragging the elbow drags the whole body (the head fell to 0.67 m); a full-body reach twists the spine and turns pinned feet (one key swung the toes 25 cm). Two tries on the smoking key, then left.
4. Its foot-slide number disagrees with the planted bones (12 to 15 cm against 0.0).
5. One body size; the rig cannot be scaled; retargeting onto another character exists but is untested.
6. The physics pass is on by default and changes what queries report.

## Improvements, most useful first (for its maker, not ours)
Ship the fixtures; draw boxes in pictures; an elbow pole target that leaves the trunk alone; pinned feet that keep their direction in a full-body reach; a slide figure from the planted bones; a scale or proportions input.

Cost: about 0.25 h of session time and one helper (about 13 min); no API spend. Time log against "tool test: HumanMotionCraft round 1".

## Round 1, the Unreal half (13 November 2026, 14:59 to 15:25, his typed approval in a separate session; one reviewer)
Method researched: production/research/ai-video-motion/CMU-RETARGET-METHOD-2026-11-12.md (Unreal's IK Rig retargeting, read 12 Nov) and the engine's own source, read 13 Nov 15:10 to 15:20: PelvisMotionOp.cpp (the hips scaled by target over source pelvis height, from the retarget poses), RootMotionGeneratorOp.cpp (default CopyFromSourceRoot), IKChainsOp.cpp (each foot goal placed by how far the source leg is stretched against its retarget pose). Scripts: tools/tool-tests/hmc_ue_retarget.py (scratch project F:/LedgerTools/humanmotioncraft/ue_check, nothing in the game), hmc_body_film.py, hmc_sheet.py, measure_fbx_legs.py. Preview production/previews/humanmotioncraft-metahuman-2026-11-13.jpg.

**Setup.** The three moves (game profile, learned fill on) imported by Unreal 5.8's glTF importer; a source IK rig per move, made by hand because the engine's auto rig finds only head, clavicles and feet in this naming (19 chains, named as the MetaHuman plugin's IK_MH_IKRig names them, legs thigh to toe with the goal on the foot, arms with the goal on the wrist); one retargeter per move and body, default ops, chains auto-mapped, source aligned to target; batch retarget onto two bodies (our average build and Rocco, the heaviest cast body); exported to FBX and measured in Blender; grey-body stills from the side and front, six moments a move, and a film per move.

**Two faults of the route found and fixed (two tries on "the pelvis is wrong").** (1) The tool writes its hip bone's rest at 5 cm above the origin while its clips stand him at 85 cm, so Unreal took the source as 6 cm tall and scaled the hips about 16 times (pelvis 15 m up). Fixed by raising the source's retarget pose by the gap measured between the clip's first frame and the rest (80.1 cm). (2) The root-motion step copied the source rig's root bone, which here is the hip bone (named "root"), onto the MetaHuman's floor bone: the pelvis came out at the source's unscaled height, detached from its own thighs and spine. Fixed by switching that step off (the moves stay in place). After both, the pelvis starts at 94.5 cm on a body whose rest is 94.6.

**Numbers (our measure; Motionsmith round 3 beside, the same script).**
| Move | Standing knees after retarget (least, deg) | Tool's own standing knees (deg) | Feet above the floor (cm) | Planted-foot drift (cm) | Motionsmith, same move |
|---|---|---|---|---|---|
| Sit and stand, average / Rocco | 22.4 / 22.5 | 2.6 to 5.7 | 0.45 / 0.32 | 1.1 / 1.2 | sit-down 2.4 to 3.5 standing, floor 0.8, drift 0.0 |
| Counter lean | 22.2 to 23.5 | 3.1 to 4.8 at the start | 3.5 | 0.2 to 0.4 | 2.4 to 4.0 (relaxed leg 26 by design), drift 0.0 to 0.16 |
| Bus-stop smoke | 30 to 31 | 17.5 to 18.3 (soft stance) | 4.7 to 4.8 | 0.2 to 0.6 | 1.3 to 2.9, drift 0.0 |
Time: each retarget 0.1 s; the Unreal run about 20 s; a film 1 to 2 min. The deepest sit's knee 98 to 100 deg; the right hand comes to 13 cm of the head on the draws.

**By eye (one fresh reviewer, F:/LedgerTools/humanmotioncraft/ue_check/out/review-2026-11-13.md).** Sit and stand: partly (reads, sits on air with no chair drawn, head thrust forward while rising). Counter lean: no (a stooped reach with a fist out and a trailing arm, the head hanging sideways at its second moment). Smoke: partly (hand to mouth reads; the hand covers the face). Beside Motionsmith's previews, Motionsmith reads more natural on all three (unfair: different renderers, no props). The reviewer also caught by eye that our "heavy" body was not heavy (below).

**What works.** The whole route runs by script with no clicks: glb in, IK rig, retarget, FBX out, measures, films. The tool's foot planting survives the retarget (drift at most 1.2 cm); the body deforms cleanly on both builds; the two route faults are understood from the engine's own code and fixed in the script.

**What fails, and why.**
1. Standing knees bent 22 to 33 deg and feet 0.3 to 4.8 cm above the floor after retarget, where the tool's own legs stand nearly straight: a route fault, cause not settled. Most likely the source's retarget pose (its rest has the legs through the floor) makes the leg-IK step place the feet short. No try spent on it; next method: a standing retarget pose for the source built from the clip's first frame, or the tool's own retarget-to-character export (clip.export with a target, which reports foot holds itself).
2. The tool's own faults carry through: the lean is a hunched reach, not a forearm on a counter; the smoking hand covers the face (as in the headless half).
3. The tool's rest pose sits below the floor (hips 5 cm, ankles at -75 cm): any engine that reads the rest as the body's height gets it wrong. For its maker.
4. Ours: F:/LedgerTools/bodies' Build Average, Heavy and Slim are the same body (identical measurements, chest 923 mm, waist 941 mm); the heavy row was redone on Rocco.

**Not run.** The packaged film: nothing enters the game in a tool test (as with Motionsmith); the retargeted films are Blender renders of the MetaHuman body. The CMU library route: never built (its method note only), so nothing to set beside. The 100STYLE licence tap: not asked, the test does not pass.

**Verdict.** Not ready for our motion. Driving it is excellent and its feet hold, but two of the three moves fail by eye in its own output, and its rest pose needs two workarounds before Unreal reads it. Motionsmith stays the motion tool; HumanMotionCraft is set aside unless a later version fixes the hands near the face, the lean and the rest pose.

**How well we can drive it.** Fully, headless, as the first half found; the Unreal half adds nothing for its hands either.

Cost: about 0.45 h of session time, one small reviewer (about 1 min); no API spend. Time log "tool test: HumanMotionCraft round 1 (Unreal half)".
