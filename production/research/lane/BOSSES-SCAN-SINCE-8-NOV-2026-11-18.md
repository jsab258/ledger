# Bosses: what changed since the 8 November scans (18 November 2026)

People in motion: one real change in the window, Unreal 5.9 Preview (9 Nov) adds retargeter steps for pelvis and body contact, the exact faults the CMU route hit; worth a test on a copy once 5.9 is final, not on the Preview.
Crowd and card memory: no change that affects the plan; 5.9 Preview adds a "Mass Characters" plugin with no memory change; an older Epic answer (July, missed before) confirms crowd people get card hair, not strands.
Hair: no new tool or Epic change in the window; the July Epic answer (missed before) narrows "strands" to people outside the MetaHuman crowd pipeline; one July paper (missed before) has no code.
Testing: nothing in the window; two pre-window AI test tools (Sept and Oct, missed before) both sit inside the game or the editor, against the project's outside-the-game rule, so no change.
Verdict: keep all four approaches; one test to plan (5.9 retargeter, after 5.9 final) and one wording change to the hair line (strands for hand-made people only, cards for crowd people).

Scope: items dated 8 to 18 November 2026, plus older items the four field scans (HAIR, PEOPLE-IN-MOTION, CROWD of 8 Nov; CROWD-DISTANCE of 9 Nov) and the testing notes (packaged-game-testing, 30 Sept; ai-tester, 23 Sept) did not have, marked "missed before". Found by web search, read by fetch on 18 Nov 2026 unless marked "not read". Licences checked against ledger-v2/research/license-allowlist.md.

## Window check: Unreal 5.8 hotfixes

- No 5.8 hotfix in the window. The latest, 5.8.4, is dated 20 Oct 2026 (https://forums.unrealengine.com/t/5-8-4-hotfix-released/2842775, and https://patchbot.io/games/unreal-engine/articles/1855-584-hotfix-released). Its only character lines are two MetaHuman RigLogic fixes (finger twist, a DNA index crash) and two automation-tool log fixes. No groom, Mass, skin cache, motion matching or retargeting fix. A search for 5.8.5 found nothing.
- Unreal 5.9 Preview ("MegaJam Preview"), posted 9 Nov 2026 (https://patchbot.io/games/unreal-engine/articles/2151-59-megajam-preview): about a week of work, "a shorter QA pass than usual", "should be considered as unstable until the final release", test only on a copy. Built mostly by agents for the Epic AI MegaJam of 12 to 15 Nov (https://80.lv/articles/unreal-engine-5-9-preview-is-out-it-was-built-with-ai/, https://www.creativebloq.com/news/unreal-engine-5-9-divides-game-devs-with-an-ai-heavy-update). No final release date found. Release notes, last updated 17 Nov (https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes): no MetaHuman or groom line at all. The forum announcement thread (https://forums.unrealengine.com/t/unreal-engine-5-9-megajam-preview/2852840) returned a server error: not read.

## 1. People in motion

Current approach: CMU real motion capture first for sitting, rising and the office exit; whole-body AI video closed except head turns and hand timing.

| Date | Source | What it is | Licence | Change? |
|---|---|---|---|---|
| 9 Nov 2026 (notes updated 17 Nov) | https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes | 5.9 IK Retargeter adds three operations: Proximity IK (limbs and contacts kept right against the torso), Pelvis Volume (pelvis placed for different body proportions), Limb Twist. The Animation Framework also updates its Pose Search, Warping and Mirroring links. | Unreal EULA, as now | Worth a test, later. The 17 Nov CMU retarget review names a pelvis-height fault and hands-through-body or chair as open risks; these two steps aim at exactly that. Only on a copy, only after 5.9 is final; the Preview is unstable and LEDGER stays on 5.8. |
| 10 Jul 2026, article updated 5 Nov (missed before by the field scan, but already in frontier-ai-uses/notes/HD-motion.md) | https://studio.aifilms.ai/blog/ardy-nvidia-real-time-motion-generation | NVIDIA ARDY, real-time text-to-motion, trained on Bones Rigplay studio capture. | Code Apache-2.0; weights NVIDIA Open Model License: not on the allowlist | No. Not new to the project; real-time on the game's own card is not practical (HD-motion note). |
| 10 Apr 2026 (missed before by the field scan, already in HD-motion.md) | https://huggingface.co/nvidia/Kimodo-SOMA-SEED-v1.1 | NVIDIA Kimodo v1.1, text plus keyframes to motion, 30-joint SOMA skeleton, 10 s at 30 fps, tested on NVIDIA cards only. | NVIDIA Open Model License: not on the allowlist | No change now. One new fact: the licence text, unreached in HD-motion.md, was read today (version of 24 Oct 2025, https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license): "Models are commercially usable", worldwide, royalty-free; NVIDIA "claims no ownership rights in outputs"; giving out the model itself needs a notice file; rights end if its guardrails are bypassed. It stays a fallback that would need his licence ruling and an NVIDIA machine, only if CMU lacks a needed clip. |
| 17 Mar 2026 announcement (missed before by the field scan) | https://huggingface.co/datasets/bones-studio/seed and https://www.roboticstomorrow.com/news/2026/03/17/bones-studio-to-release-bones-seed-the-first-multimodal-motion-dataset-purpose-built-for-humanoid-robotics/26276/ | BONES-SEED: 142,220 BVH motions, 288 h at 120 fps, 522 performers; an "Everyday" package of 5,816 motions (sitting, reading, household). Gated download. | "bones-seed-license": terms not read (the licence page did not answer in time); commercial terms unknown | No, for now. Could be a second real-capture source beside CMU, but nothing may be used until the licence is read from the PC and ruled on. |
| 2025 to 2026 (already in HD-motion.md) | https://github.com/NVlabs/gem-x | GEM-X, video to 77-joint SOMA motion. | Code Apache-2.0; weights NVIDIA Open Model License | No. AI video route is closed for whole-body motion; needs CUDA. |

Searched, nothing in the window: new text-to-motion or video-to-motion open models; MetaHuman single-camera body capture updates; Game Animation Sample or motion matching news (the Nov learning-content page found is dated 19 Nov 2025). HY-Motion: nothing new found.

## 2. Crowd and card memory

Current approach: a texture and level-of-detail packing plan before the street multiplies people.

| Date | Source | What it is | Licence | Change? |
|---|---|---|---|---|
| 9 Nov 2026 | https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes | 5.9 Preview "Mass Characters" plugin: Mass traits for character interpolation and visualisation, selective pawn replication, a game-feature setup action. No skeletal mesh, skin cache, LOD or texture memory change on the page. | Unreal EULA | No. Nothing for memory per person; Preview only. |
| 10 to 21 Jul 2026 (missed before) | https://forums.unrealengine.com/t/groom-hair-on-metahuman-crowd-high-res-actors-matching-iskm-hair-color-materials/2744949 | Epic staff (Henry Falconer, 20 Jul): MetaHuman Crowds' near "high-res" actors deliberately use skeletal-mesh card hair, not grooms, to avoid groom cost and keep shading close to the far instanced meshes. Strands on crowd actors are not supported; possible by copying and changing two pipeline classes, with shading hard to match. A user's card hair also looked darker far than near. | Read only | No change to the plan; it supports it. The packing plan can count crowd people as card hair only. Watch for the far-darker hair colour jump. |

Searched, nothing in the window: new MetaHuman Crowds fixes or memory figures; any packaged-build memory-per-person report (the measurement in CROWD-DISTANCE stays LEDGER's to make). A 5.8.4 forum report of MetaHuman Creator memory growing per scripted build (https://forums.unrealengine.com/t/5-8-4-metahuman-creator-editor-memory-grows-by-5-18-gb-per-scripted-build-and-is-never-released/2848954) was seen only as a search title: not read; it concerns the editor, not the game.

## 3. Hair

Current approach: strands.

| Date | Source | What it is | Licence | Change? |
|---|---|---|---|---|
| 20 Jul 2026 (missed before) | the Epic crowd-groom thread above | Crowd people get card hair by design; strands are only out of the box on ordinary MetaHuman actors. | Read only | Yes, narrow. "Strands" should read: strands for hand-made people near the camera; cards for anyone built through the crowd pipeline. This matches the 8 Nov scan's own reading (cards at gameplay distance, strands at talk close-ups). |
| May to Jul 2026 (missed before) | https://www.cg.tuwien.ac.at/research/publications/2026/LIPP-2026-HAIR/ and https://gamedev.net/news/4319-high-performance-real-time-implicit-strand-based-hair-rendering-via-software/ | Lipp, Jarabo, Wimmer, Bode, I3D 2026 (ACM CGIT 9(4) art. 58): software-rasterised strand hair from hair meshes, cheap far hair at one sample per pixel, distance-based level of detail, "minimal hardware support". | No code or licence found | No. A paper with no code or Unreal route; nothing to use. |

Searched, nothing in the window: groom or hair card generator changes (none on the 5.9 page); new strand-to-card tools. The two hair-related forum fixes listed in the 8 Nov scan were not re-checked against 5.8.4 beyond its notes, which name none.

## 4. Testing

Current approach: same-day packaged verdicts by an AI tester driving the game from outside with real key presses.

| Date | Source | What it is | Licence | Change? |
|---|---|---|---|---|
| 30 Oct 2026 (missed before; before the window) | https://www.gamespress.com/Ramen-Launches-Aura-Autopilot-its-Open-Source-Autonomous-Game-Tester-f and https://github.com/ramenvr/autopilot/wiki | Ramen's Aura Autopilot: an AI agent that plays a game to test it. Installed as an engine plugin; launches Play-In-Editor, reads the project source, an LLM builds the harness. Unreal 5.4 to 5.8, Windows. Packaged builds not mentioned. | Apache-2.0 (wiki) | No. It plays in the editor through a plugin; LEDGER's verdict needs the packaged game driven from outside, which the 30 Sept research chose because in-game driving skips the keyboard-to-game layer where a real bug sat. |
| 9 Sep 2026 (missed before) | https://forums.unrealengine.com/t/harshbakshi-ai-gauntlet-agent-control-surface-for-packaged-builds/2763931 | "AI Gauntlet": a runtime module compiled into the game; 34 commands over a local socket so Claude Code or a script can read state and drive a packaged build, Shipping included. | Not stated (Fab listing not read) | No. It is code inside the game, which the project ruled out; licence unknown. |

Searched, nothing in the window: new Gauntlet or automation features for packaged builds (5.9's "Modular Test Framework" is for plugin tests in the editor); new outside-the-game AI testers. Square Enix's Gemini tester (shown Aug 2026, internal only) and Roblox's Playtest Agent are not available to LEDGER.

## Not read

bones.studio SEED licence page (approval not answered in time); the 5.9 Preview forum thread (server error); the AI Gauntlet Fab listing; the 5.8.4 MetaHuman Creator memory thread (title only).
