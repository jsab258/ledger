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
