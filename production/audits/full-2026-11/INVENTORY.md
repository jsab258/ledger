# Inventory of the repository (full audit, November 2026)

Every folder in the repository (branch wip merged into lane-2026-11), 1095 folders, read on 2026-11-19; newest commit 2026-11-19; full history (shallow: False). Made by tools/lane/audit/inventory.py; the full record per folder is in inventory.json.

How to read the status: live (changed lately or referred to and in use), reference (kept to look things up: old versions, research, archives), stale (referred to but unchanged for over 30 days), dead (nothing refers to it and unchanged for over 21 days), duplicate (same files as another folder). The status is a first guess by rule, for the stage 2 reviewers to test. It is weakest for code folders: code is rarely named by its path, so code folders under ledger/ can show as dead while the build still uses them.

## Counts

| Status | Folders |
|---|---|
| stale | 350 |
| reference | 297 |
| dead | 235 |
| live | 213 |

## The areas (top-level folders)

| Folder | What it is | Owner | Last change | Size MB | Files | Folders inside by status |
|---|---|---|---|---|---|---|
| ledger | the town simulation in C# (the Town session's code and tests) | town (simulation) | 2026-11-18 | 1655.2 | 2917 | dead 43, stale 42, live 14 |
| production | the studio's records, plans, research, audits and art work | shared | 2026-11-19 | 837.9 | 5146 | stale 275, reference 199, dead 174, live 119 |
| legacy | the old versions' records (reference only) | none (archive) | 2026-09-26 | 115.0 | 2367 | reference 92 |
| tools | the checks and scripts that run the studio and the game's gates | builder | 2026-11-19 | 62.3 | 839 | live 41, stale 19 |
| game-design | the game's design documents | design | 2026-11-18 | 42.0 | 594 | stale 5, live 2, reference 1 |
| ue-probe | the Unreal project (the builder's) | builder | 2026-11-18 | 13.5 | 151 | live 11, stale 1 |
| voice-candidates | voice samples kept from voice casting | builder | 2026-07-31 | 5.8 | 67 | dead 18, stale 1 |
| content | game content in text form | builder | 2026-11-06 | 0.6 | 14 | live 6, stale 4 |
| .github | the build workflows on his PC | shared | 2026-11-12 | 0.2 | 3 | live 1 |
| .claude | the sessions' skills, agents and settings | shared | 2026-11-18 | 0.2 | 17 | live 11 |
| ledger-v2 | the second version's research (reference) | reference (old version) | 2026-11-18 | 0.1 | 8 | reference 2 |
| research | older shared research | shared research | 2026-09-03 | 0.0 | 1 |  |
| ledger-imagegen | the image generation tools | builder | 2026-09-22 | 0.0 | 1 |  |
| .githooks | the shared commit checks | shared | 2026-09-01 | 0.0 | 1 |  |

## .claude/

| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |
|---|---|---|---|---|---|---|---|
| .claude/agents |  | shared | 2026-11-18 | 0.0 | 7 | 76 | live (touched 1 days before newest commit; 76 refs) |
| .claude/skills |  | shared | 2026-11-17 | 0.2 | 9 | 111 | live (touched 2 days before newest commit; 12 refs) |

## .github/

| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |
|---|---|---|---|---|---|---|---|
| .github/workflows |  | shared | 2026-11-12 | 0.2 | 3 | 156 | live (touched 7 days before newest commit; 156 refs) |

## content/

| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |
|---|---|---|---|---|---|---|---|
| content/brands |  | builder | 2026-10-04 | 0.0 | 1 | 34 | stale (last commit 46 days before newest; still referenced by 34 files) |
| content/dialogue |  | builder | 2026-10-01 | 0.0 | 2 | 55 | stale (last commit 49 days before newest; still referenced by 55 files) |
| content/props |  | builder | 2026-09-01 | 0.2 | 2 | 15 | stale (last commit 79 days before newest; still referenced by 15 files) |
| content/rules |  | builder | 2026-09-10 | 0.0 | 1 | 8 | stale (last commit 70 days before newest; still referenced by 8 files) |
| content/voice |  | builder | 2026-11-06 | 0.4 | 8 | 24 | live (touched 13 days before newest commit; 2 refs) |

## game-design/

| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |
|---|---|---|---|---|---|---|---|
| game-design/mickeys-office |  | design | 2026-10-01 | 0.0 | 1 | 3 | stale (last commit 49 days before newest; still referenced by 3 files) |
| game-design/picked-clips |  | design | 2026-11-06 | 4.9 | 23 | 48 | live (touched 13 days before newest commit; 48 refs) |
| game-design/reference | THE FRAMES ARE NOT HERE since 3 October (Jafar: other games' screenshots never in the | design | 2026-10-03 | 0.0 | 1 | 16 | reference (archive / old version / research location) |
| game-design/research |  | design | 2026-09-22 | 0.2 | 8 | 36 | stale (last commit 58 days before newest; still referenced by 36 files) |
| game-design/sim-shots |  | design | 2026-09-21 | 24.8 | 419 | 121 | stale (last commit 59 days before newest; still referenced by 103 files) |
| game-design/voice-conds |  | design | 2026-11-06 | 6.6 | 45 | 14 | live (touched 13 days before newest commit; 14 refs) |
| game-design/voice-live |  | design | 2026-08-22 | 3.8 | 17 | 14 | stale (last commit 89 days before newest; still referenced by 14 files) |

## ledger/

| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |
|---|---|---|---|---|---|---|---|
| ledger/Adversary |  | town (simulation) | 2026-09-06 | 0.0 | 2 | 2 | stale (last commit 74 days before newest; still referenced by 2 files) |
| ledger/Assets |  | town (simulation) | 2026-11-18 | 1651.2 | 2814 | 598 | live (touched 1 days before newest commit; 32 refs) |
| ledger/BackendCheck |  | town (simulation) | 2026-08-08 | 0.0 | 1 | 2 | stale (last commit 103 days before newest; still referenced by 2 files) |
| ledger/BalanceLab |  | town (simulation) | 2026-09-28 | 0.1 | 2 | 7 | stale (last commit 52 days before newest; still referenced by 7 files) |
| ledger/BarkGen |  | town (simulation) | 2026-08-13 | 0.0 | 2 | 6 | stale (last commit 98 days before newest; still referenced by 6 files) |
| ledger/ClaimBench |  | town (simulation) | 2026-11-16 | 0.3 | 15 | 25 | live (touched 3 days before newest commit; 25 refs) |
| ledger/ConvoProbe |  | town (simulation) | 2026-09-29 | 0.0 | 2 | 8 | stale (last commit 51 days before newest; still referenced by 8 files) |
| ledger/CoreTests |  | town (simulation) | 2026-11-18 | 2.1 | 10 | 61 | live (touched 1 days before newest commit; 61 refs) |
| ledger/DevTools |  | town (simulation) | 2026-11-16 | 0.0 | 2 | 5 | live (touched 3 days before newest commit; 5 refs) |
| ledger/GameCheck |  | town (simulation) | 2026-08-05 | 0.0 | 2 | 2 | stale (last commit 106 days before newest; still referenced by 2 files) |
| ledger/LineTest |  | town (simulation) | 2026-09-29 | 0.0 | 2 | 2 | stale (last commit 51 days before newest; still referenced by 2 files) |
| ledger/Packages |  | town (simulation) | 2026-08-21 | 0.0 | 1 | 0 | dead (no references to it or below it; last commit 90 days before newest) |
| ledger/PerceptionGolden |  | town (simulation) | 2026-11-07 | 0.4 | 3 | 30 | live (touched 12 days before newest commit; 30 refs) |
| ledger/ProjectSettings |  | town (simulation) | 2026-07-24 | 0.0 | 1 | 2 | stale (last commit 118 days before newest; still referenced by 2 files) |
| ledger/ReachCheck |  | town (simulation) | 2026-10-28 | 0.1 | 3 | 10 | live (touched 22 days before newest commit; 10 refs) |
| ledger/Relay |  | town (simulation) | 2026-09-29 | 0.0 | 4 | 16 | stale (last commit 51 days before newest; still referenced by 16 files) |
| ledger/RouterFloor |  | town (simulation) | 2026-09-29 | 0.0 | 2 | 60 | stale (last commit 51 days before newest; still referenced by 60 files) |
| ledger/SaveChaos |  | town (simulation) | 2026-09-30 | 0.0 | 2 | 8 | stale (last commit 50 days before newest; still referenced by 8 files) |
| ledger/ShapeCheck |  | town (simulation) | 2026-08-08 | 0.0 | 2 | 5 | stale (last commit 103 days before newest; still referenced by 5 files) |
| ledger/SimHarness |  | town (simulation) | 2026-09-29 | 0.1 | 3 | 6 | stale (last commit 51 days before newest; still referenced by 6 files) |
| ledger/Soak |  | town (simulation) | 2026-09-23 | 0.1 | 2 | 18 | stale (last commit 57 days before newest; still referenced by 18 files) |
| ledger/SpeechBench |  | town (simulation) | 2026-08-14 | 0.0 | 2 | 5 | stale (last commit 97 days before newest; still referenced by 5 files) |
| ledger/StrangerTest |  | town (simulation) | 2026-09-23 | 0.1 | 3 | 7 | stale (last commit 57 days before newest; still referenced by 7 files) |
| ledger/TalkHelper |  | town (simulation) | 2026-11-18 | 0.2 | 2 | 47 | live (touched 1 days before newest commit; 47 refs) |
| ledger/TalkTests |  | town (simulation) | 2026-11-18 | 0.1 | 2 | 6 | live (touched 1 days before newest commit; 6 refs) |
| ledger/Tier2Gen |  | town (simulation) | 2026-09-29 | 0.1 | 2 | 1 | stale (last commit 51 days before newest; still referenced by 1 files) |
| ledger/TownReach |  | town (simulation) | 2026-10-28 | 0.1 | 2 | 12 | live (touched 22 days before newest commit; 12 refs) |
| ledger/breaks |  | town (simulation) | 2026-08-23 | 0.1 | 22 | 3 | stale (last commit 88 days before newest; still referenced by 3 files) |

## ledger-v2/

| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |
|---|---|---|---|---|---|---|---|
| ledger-v2/research |  | reference (old version) | 2026-11-18 | 0.1 | 8 | 124 | reference (archive / old version / research location) |

## legacy/

| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |
|---|---|---|---|---|---|---|---|
| legacy/outbound-refusals-2026-09-03 |  | none (archive) | 2026-09-10 | 0.6 | 494 | 1 | reference (archive / old version / research location) |
| legacy/outbox | STATUS: LOG. A message here was written, never sent, and can no longer be sent. | none (archive) | 2026-09-09 | 0.0 | 2 | 2 | reference (archive / old version / research location) |
| legacy/studio-v2 | Produced 2026-08-31 in the claude.ai planning session, from: the wc26/ledger repo, the game-studio framework repo, the d | none (archive) | 2026-09-26 | 113.9 | 1849 | 83 | reference (archive / old version / research location) |
| legacy/unity-reference-build |  | none (archive) | 2026-09-10 | 0.0 | 3 | 1 | reference (archive / old version / research location) |
| legacy/v1-era |  | none (archive) | 2026-09-10 | 0.3 | 12 | 21 | reference (archive / old version / research location) |
| legacy/week-plans |  | none (archive) | 2026-09-10 | 0.0 | 2 | 2 | reference (archive / old version / research location) |

## production/

| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |
|---|---|---|---|---|---|---|---|
| production/approvals |  | builder | 2026-11-19 | 25.3 | 497 | 144 | live (touched 0 days before newest commit; 17 refs) |
| production/archive |  | none (archive) | 2026-11-09 | 1.6 | 37 | 47 | reference (archive / old version / research location) |
| production/art |  | builder | 2026-11-16 | 349.2 | 442 | 562 | live (touched 3 days before newest commit; 39 refs) |
| production/asset-checks |  | builder | 2026-11-08 | 0.1 | 6 | 14 | live (touched 11 days before newest commit; 14 refs) |
| production/assets |  | builder | 2026-11-08 | 131.1 | 232 | 290 | live (touched 11 days before newest commit; 27 refs) |
| production/audio |  | builder | 2026-10-01 | 0.5 | 6 | 5 | live (touched 49 days before newest commit; 0 refs) |
| production/audits |  | builder | 2026-11-19 | 6.2 | 217 | 219 | live (touched 0 days before newest commit; 28 refs) |
| production/cast |  | builder | 2026-10-07 | 0.0 | 3 | 29 | stale (last commit 43 days before newest; still referenced by 1 files) |
| production/casting |  | builder | 2026-11-08 | 61.7 | 298 | 227 | live (touched 11 days before newest commit; 40 refs) |
| production/cloud-week |  | builder | 2026-10-24 | 24.8 | 609 | 412 | live (touched 26 days before newest commit; 8 refs) |
| production/d1-probe |  | builder | 2026-11-18 | 2.7 | 28 | 227 | live (touched 1 days before newest commit; 224 refs) |
| production/design |  | builder | 2026-10-01 | 19.4 | 57 | 32 | stale (last commit 49 days before newest; still referenced by 1 files) |
| production/fonts |  | builder | 2026-10-12 | 4.0 | 40 | 73 | stale (last commit 38 days before newest; still referenced by 29 files) |
| production/friends-build |  | builder | 2026-10-05 | 0.0 | 1 | 8 | stale (last commit 45 days before newest; still referenced by 8 files) |
| production/handover |  | builder | 2026-11-18 | 0.0 | 5 | 21 | live (touched 1 days before newest commit; 21 refs) |
| production/handovers | For the builder (town list T2, Jafar, 29 September evening: every handover | builder | 2026-10-07 | 0.0 | 13 | 28 | stale (last commit 43 days before newest; still referenced by 28 files) |
| production/lab | A separate session testing one method while the builder works: give the AI an exact, measurable target and check every a | builder | 2026-10-08 | 2.0 | 133 | 34 | stale (last commit 42 days before newest; still referenced by 16 files) |
| production/lane | A second Claude session that does only machine-free work, beside the main production session (his picks of 17 Nov about  | lane | 2026-11-18 | 23.9 | 186 | 79 | live (touched 1 days before newest commit; 28 refs) |
| production/licences |  | builder | 2026-10-05 | 0.1 | 9 | 7 | live (touched 45 days before newest commit; 0 refs) |
| production/orders |  | builder | 2026-11-19 | 0.5 | 7 | 83 | live (touched 0 days before newest commit; 63 refs) |
| production/playtest |  | builder | 2026-11-16 | 0.2 | 64 | 106 | live (touched 3 days before newest commit; 71 refs) |
| production/previews |  | builder | 2026-11-18 | 155.6 | 1007 | 290 | live (touched 1 days before newest commit; 137 refs) |
| production/progress-page |  | builder | 2026-11-18 | 0.1 | 2 | 19 | live (touched 1 days before newest commit; 19 refs) |
| production/proof-view | The list's item 2 (Jafar, 3 October): the hook camera by day, built to the Hook sheet through the | builder | 2026-10-03 | 0.0 | 2 | 3 | stale (last commit 47 days before newest; still referenced by 3 files) |
| production/reference | THE ONLY PLACE A REFERENCE LIVES. Every tool, recipe and check that compares | builder | 2026-10-03 | 6.1 | 10 | 99 | reference (archive / old version / research location) |
| production/research | WHAT THIS ANSWERS. Before authoring anything, two questions: which research | shared research | 2026-11-18 | 20.9 | 1155 | 1561 | reference (archive / old version / research location) |
| production/sittings |  | builder | 2026-09-24 | 0.0 | 1 | 1 | stale (last commit 56 days before newest; still referenced by 1 files) |
| production/specs |  | builder | 2026-11-18 | 1.2 | 62 | 576 | live (touched 1 days before newest commit; 550 refs) |
| production/store |  | builder | 2026-10-03 | 0.0 | 3 | 10 | stale (last commit 47 days before newest; still referenced by 10 files) |
| production/stranger-test |  | builder | 2026-09-23 | 0.0 | 3 | 20 | stale (last commit 57 days before newest; still referenced by 20 files) |

## tools/

| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |
|---|---|---|---|---|---|---|---|
| tools/ai-tester |  | builder | 2026-11-03 | 0.1 | 2 | 37 | live (touched 16 days before newest commit; 37 refs) |
| tools/art-recipes |  | builder | 2026-11-08 | 2.4 | 59 | 247 | live (touched 11 days before newest commit; 196 refs) |
| tools/blender-live |  | builder | 2026-11-11 | 0.0 | 3 | 10 | live (touched 8 days before newest commit; 10 refs) |
| tools/checkers |  | builder | 2026-11-03 | 0.1 | 12 | 17 | live (touched 16 days before newest commit; 17 refs) |
| tools/citypack |  | builder | 2026-09-21 | 46.0 | 18 | 46 | stale (last commit 59 days before newest; still referenced by 37 files) |
| tools/friends |  | builder | 2026-10-05 | 0.0 | 1 | 13 | stale (last commit 45 days before newest; still referenced by 13 files) |
| tools/hooks |  | builder | 2026-11-17 | 0.0 | 3 | 18 | live (touched 2 days before newest commit; 18 refs) |
| tools/imagegen | Double-click 1 MAKE THE PICTURES.bat. That is the whole thing. | builder | 2026-09-24 | 0.5 | 13 | 82 | stale (last commit 56 days before newest; still referenced by 82 files) |
| tools/lane |  | lane | 2026-11-19 | 2.0 | 178 | 98 | live (touched 0 days before newest commit; 42 refs) |
| tools/md |  | builder | 2026-11-18 | 0.3 | 40 | 33 | live (touched 1 days before newest commit; 28 refs) |
| tools/md-bridge |  | builder | 2026-11-18 | 0.3 | 29 | 45 | live (touched 1 days before newest commit; 40 refs) |
| tools/meshgen | LIVE. Verified 2026-09-01. The code is the source of truth; this file | builder | 2026-11-18 | 2.0 | 111 | 179 | live (touched 1 days before newest commit; 52 refs) |
| tools/mixamo-pick | UPDATE.bat — pulls the latest project. Always first. | builder | 2026-09-21 | 2.1 | 19 | 22 | stale (last commit 59 days before newest; still referenced by 18 files) |
| tools/play |  | builder | 2026-09-29 | 0.0 | 2 | 8 | stale (last commit 51 days before newest; still referenced by 8 files) |
| tools/props |  | builder | 2026-11-08 | 1.0 | 13 | 43 | live (touched 11 days before newest commit; 43 refs) |
| tools/runner |  | builder | 2026-10-05 | 0.0 | 2 | 178 | stale (last commit 45 days before newest; still referenced by 178 files) |
| tools/tool-tests |  | builder | 2026-11-13 | 0.0 | 6 | 9 | live (touched 6 days before newest commit; 9 refs) |
| tools/tts-benchmark | One file. Download it, run it. | builder | 2026-07-28 | 0.0 | 3 | 4 | stale (last commit 114 days before newest; still referenced by 4 files) |
| tools/ue |  | builder | 2026-11-17 | 1.5 | 84 | 268 | live (touched 2 days before newest commit; 262 refs) |
| tools/ui |  | builder | 2026-10-01 | 0.0 | 4 | 6 | stale (last commit 49 days before newest; still referenced by 6 files) |
| tools/voice-fetch | Your part is two commands and a listening pass. | builder | 2026-08-14 | 0.1 | 9 | 21 | stale (last commit 97 days before newest; still referenced by 21 files) |
| tools/voice-gen | Run this on your machine, not in CI. The render needs a GPU and chatterbox; | builder | 2026-08-26 | 0.1 | 4 | 7 | stale (last commit 85 days before newest; still referenced by 7 files) |
| tools/voice-live |  | builder | 2026-11-06 | 0.9 | 67 | 100 | live (touched 13 days before newest commit; 100 refs) |

## ue-probe/

| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |
|---|---|---|---|---|---|---|---|
| ue-probe/Config |  | builder | 2026-11-16 | 0.0 | 4 | 42 | live (touched 3 days before newest commit; 42 refs) |
| ue-probe/Content |  | builder | 2026-11-18 | 4.9 | 49 | 52 | live (touched 1 days before newest commit; 22 refs) |
| ue-probe/Source |  | builder | 2026-11-16 | 3.6 | 86 | 209 | live (touched 3 days before newest commit; 39 refs) |
| ue-probe/perception-golden |  | builder | 2026-11-08 | 4.5 | 5 | 9 | live (touched 11 days before newest commit; 9 refs) |
| ue-probe/tests |  | builder | 2026-11-05 | 0.6 | 6 | 83 | live (touched 14 days before newest commit; 73 refs) |

## voice-candidates/

| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |
|---|---|---|---|---|---|---|---|
| voice-candidates/ada |  | builder | 2026-07-31 | 0.3 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/crowd_f1 |  | builder | 2026-07-31 | 0.3 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/crowd_f2 |  | builder | 2026-07-31 | 0.1 | 1 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/crowd_f3 |  | builder | 2026-07-31 | 0.3 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/crowd_m1 |  | builder | 2026-07-31 | 0.3 | 3 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/crowd_m2 |  | builder | 2026-07-31 | 0.4 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/crowd_m3 |  | builder | 2026-07-31 | 0.3 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/ellis |  | builder | 2026-07-31 | 0.4 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/emil |  | builder | 2026-07-31 | 0.1 | 1 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/hal |  | builder | 2026-07-31 | 0.3 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/joey |  | builder | 2026-07-31 | 0.3 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/kest |  | builder | 2026-07-31 | 0.4 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/lena |  | builder | 2026-07-31 | 0.4 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/marla |  | builder | 2026-07-31 | 0.2 | 2 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/reese |  | builder | 2026-07-31 | 0.4 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/rita |  | builder | 2026-07-31 | 0.3 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/rocco |  | builder | 2026-07-31 | 0.4 | 4 | 1 | stale (last commit 111 days before newest; still referenced by 1 files) |
| voice-candidates/sam |  | builder | 2026-07-31 | 0.4 | 4 | 0 | dead (no references to it or below it; last commit 111 days before newest) |
| voice-candidates/vesna |  | builder | 2026-07-31 | 0.2 | 2 | 0 | dead (no references to it or below it; last commit 111 days before newest) |

## Dead at depth 3 or less (41)

Nothing in the repository names these and they have not changed in three weeks. Candidates for deletion or archiving, each to be checked by a reviewer first.

- ledger/GameCheck/Shims (last change 2026-08-05, 1 files, 0.0 MB)
- ledger/Packages (last change 2026-08-21, 1 files, 0.0 MB)
- production/approvals/2026-09-25-in-game (last change 2026-09-25, 2 files, 0.0 MB)
- production/approvals/2026-09-30-town (last change 2026-09-29, 1 files, 0.0 MB)
- production/approvals/2026-09-30-town-2 (last change 2026-09-30, 1 files, 0.0 MB)
- production/approvals/2026-09-30-town-3 (last change 2026-09-30, 1 files, 0.0 MB)
- production/approvals/2026-10-01-cleanup (last change 2026-10-01, 2 files, 0.0 MB)
- production/approvals/2026-10-01-town (last change 2026-09-29, 1 files, 0.0 MB)
- production/approvals/2026-10-05-sweep (last change 2026-10-05, 3 files, 0.0 MB)
- production/approvals/2026-10-07-voice (last change 2026-10-07, 3 files, 0.0 MB)
- production/approvals/2026-10-22-close (last change 2026-10-22, 3 files, 0.0 MB)
- production/approvals/2026-10-23 (last change 2026-10-23, 3 files, 0.0 MB)
- production/approvals/2026-10-26-b (last change 2026-10-26, 3 files, 0.0 MB)
- production/approvals/2026-10-26-c (last change 2026-10-26, 3 files, 0.0 MB)
- production/approvals/2026-10-27 (last change 2026-10-27, 3 files, 0.0 MB)
- production/approvals/2026-10-28 (last change 2026-10-28, 3 files, 0.0 MB)
- production/audits/gate-found-list-2026-10-21 (last change 2026-10-21, 1 files, 0.0 MB)
- production/casting/candidates-tom-2026-10-06 (last change 2026-10-06, 1 files, 0.0 MB)
- production/d1-probe/crime-by-input (last change 2026-09-22, 1 files, 0.0 MB)
- production/d1-probe/live-encounter (last change 2026-09-24, 1 files, 0.0 MB)
- production/lab/3-jacket (last change 2026-10-08, 27 files, 0.4 MB)
- production/lab/4-plain-clothes (last change 2026-10-08, 47 files, 0.7 MB)
- production/lab/tools (last change 2026-10-08, 8 files, 0.0 MB)
- voice-candidates/ada (last change 2026-07-31, 4 files, 0.3 MB)
- voice-candidates/crowd_f1 (last change 2026-07-31, 4 files, 0.3 MB)
- voice-candidates/crowd_f2 (last change 2026-07-31, 1 files, 0.1 MB)
- voice-candidates/crowd_f3 (last change 2026-07-31, 4 files, 0.3 MB)
- voice-candidates/crowd_m1 (last change 2026-07-31, 3 files, 0.3 MB)
- voice-candidates/crowd_m2 (last change 2026-07-31, 4 files, 0.4 MB)
- voice-candidates/crowd_m3 (last change 2026-07-31, 4 files, 0.3 MB)
- voice-candidates/ellis (last change 2026-07-31, 4 files, 0.4 MB)
- voice-candidates/emil (last change 2026-07-31, 1 files, 0.1 MB)
- voice-candidates/hal (last change 2026-07-31, 4 files, 0.3 MB)
- voice-candidates/joey (last change 2026-07-31, 4 files, 0.3 MB)
- voice-candidates/kest (last change 2026-07-31, 4 files, 0.4 MB)
- voice-candidates/lena (last change 2026-07-31, 4 files, 0.4 MB)
- voice-candidates/marla (last change 2026-07-31, 2 files, 0.2 MB)
- voice-candidates/reese (last change 2026-07-31, 4 files, 0.4 MB)
- voice-candidates/rita (last change 2026-07-31, 4 files, 0.3 MB)
- voice-candidates/sam (last change 2026-07-31, 4 files, 0.4 MB)
- voice-candidates/vesna (last change 2026-07-31, 2 files, 0.2 MB)

## Duplicates (0)

None found by content.

## Largest folders

- ledger/Assets: 1651.2 MB, 2814 files (live)
- ledger/Assets/StreamingAssets: 855.6 MB, 2199 files (stale)
- ledger/Assets/Characters: 746.8 MB, 88 files (stale)
- production/art: 349.2 MB, 442 files (live)
- ledger/Assets/StreamingAssets/Audio: 315.5 MB, 2012 files (live)
- ledger/Assets/StreamingAssets/Audio/Voice: 315.5 MB, 2012 files (stale)
- ledger/Assets/StreamingAssets/Decals: 310.1 MB, 131 files (stale)
- ledger/Assets/StreamingAssets/Decals/ambientcg: 297.7 MB, 104 files (stale)
- production/art/compare: 271.6 MB, 127 files (stale)
- ledger/Assets/StreamingAssets/CityPack: 229.8 MB, 55 files (stale)
- ledger/Assets/StreamingAssets/CityPack/textures: 229.8 MB, 54 files (stale)
- production/previews: 155.6 MB, 1007 files (live)
- production/assets: 131.1 MB, 232 files (live)
- production/art/compare/hook-street-2026-09-22: 116.5 MB, 41 files (dead)
- legacy/studio-v2: 113.9 MB, 1849 files (reference)

## The PC side (from the builder's read-only inventory)

216 folders on his PC read on 2026-11-19 00:56 (folder sizes and dates only, never contents). 61 of them are named by no repository file, tool, retention.json or CATALOGUE.md.

| Folder | GB | Files | Last change | Named by |
|---|---|---|---|---|
| C:\LedgerTools\cargo-target | 19.78 | 40446 | 2026-11-18 | 1 |
| F:\LedgerTools\mh-dress | 19.76 | 3656 | 2026-11-07 | 3 |
| F:\LedgerTools\mh-dress\Content | 19.48 | 3282 | 2026-11-07 | 3 |
| C:\Users\Jafar\ledger-local\ue-probe | 16.33 | 9097 | 2026-11-18 | 3 |
| C:\LedgerTools\zen | 12.61 | 3526 | 2026-11-18 | 1 |
| F:\LedgerTools\garments | 6.74 | 4546 | 2026-11-18 | 3 |
| F:\LedgerTools\gate | 6.06 | 5950 | 2026-11-17 | 3 |
| F:\LedgerTools\played-game | 6.03 | 649 | 2026-11-18 | 3 |
| F:\LedgerTools\played-game\Windows | 6.03 | 647 | 2026-11-18 | 3 |
| F:\LedgerTools\garments\tom | 5.37 | 3182 | 2026-11-11 | 3 |
| F:\LedgerTools\gate\new | 5.05 | 5023 | 2026-11-17 | 3 |
| C:\Users\Jafar\Dropbox\LEDGER backup\metahuman | 4.84 | 1018 | 2026-09-25 | 3 |
| C:\Users\Jafar\ledger-local\.git | 4.42 | 7158 | 2026-11-19 | 2 |
| F:\LedgerTools\tool-dev | 4.25 | 14963 | 2026-11-19 | 3 |
| C:\LedgerTools\mh-assemble | 4.14 | 1098 | 2026-11-17 | 3 |
| C:\LedgerTools\kiln-lanes | 4.09 | 17809 | 2026-11-19 | 1 |
| F:\LedgerTools\voice-portable | 4.06 | 17819 | 2026-11-07 | 3 |
| C:\LedgerTools\chatterbox-nano | 4.06 | 20325 | 2026-09-30 | 3 |
| C:\Users\Jafar\ledger-local\production | 3.54 | 28249 | 2026-11-19 | 3 |
| F:\LedgerTools\game-inputs | 3.52 | 2340 | 2026-11-18 | 3 |
| F:\LedgerTools\tool-dev\runs | 3.3 | 8925 | 2026-11-18 | 3 |
| F:\LedgerTools\uv | 2.87 | 65645 | 2026-11-13 | 1 |
| C:\LedgerTools\mocap-solve | 2.67 | 119 | 2026-11-13 | 1 |
| F:\LedgerTools\voice-env-export | 2.1 | 54706 | 2026-10-26 | 1 |
| C:\Users\Jafar\ledger-local\ledger | 1.74 | 3686 | 2026-11-18 | 3 |
| F:\LedgerTools\fab | 1.69 | 18 | 2026-11-02 | 3 |
| C:\Users\Jafar\ledger-local\ledger\Assets | 1.56 | 2829 | 2026-11-18 | 3 |
| F:\LedgerTools\game-inputs\gasp | 1.43 | 1437 | 2026-10-25 | 1 |
| F:\LedgerTools\bodies | 1.33 | 323 | 2026-11-18 | 3 |
| F:\LedgerTools\voice-graphs | 1.32 | 4 | 2026-10-06 | 3 |
| F:\LedgerTools\hf | 1.11 | 41 | 2026-11-18 | 3 |
| F:\LedgerTools\texture-tools | 1.06 | 438 | 2026-11-12 | 1 |
| F:\LedgerTools\pylib | 0.98 | 38301 | 2026-10-08 | 0 |
| F:\LedgerTools\lab | 0.92 | 694 | 2026-10-22 | 0 |
| F:\LedgerTools\tool-tests-2026-11 | 0.92 | 1170 | 2026-11-17 | 3 |
| F:\LedgerTools\approved-cast-2026-09-25 | 0.89 | 328 | 2026-09-25 | 1 |
| F:\LedgerTools\blender52 | 0.89 | 7228 | 2026-11-18 | 3 |
| C:\LedgerTools\blender | 0.87 | 6034 | 2026-10-27 | 3 |
| F:\LedgerTools\game-inputs\production | 0.82 | 344 | 2026-11-17 | 3 |
| F:\LedgerTools\bpyenv | 0.79 | 6143 | 2026-10-21 | 3 |

Named by nothing (the 40 largest):

- F:\LedgerTools\pylib (0.98 GB, last change 2026-10-08)
- F:\LedgerTools\lab (0.92 GB, last change 2026-10-22)
- F:\LedgerTools\sw-scratch (0.51 GB, last change 2026-10-24)
- C:\LedgerTools\kiln-runs (0.29 GB, last change 2026-11-18)
- F:\LedgerTools\game-inputs\fab-megascans (0.25 GB, last change 2026-11-11)
- F:\LedgerTools\garments\ron_cc0_outfit (0.25 GB, last change 2026-10-07)
- F:\LedgerTools\gate\work (0.23 GB, last change 2026-11-09)
- F:\LedgerTools\garments\ron_plain_outfit (0.17 GB, last change 2026-10-07)
- F:\LedgerTools\mh-dress\Saved (0.14 GB, last change 2026-11-07)
- F:\LedgerTools\drapestudio-test-2026-11-11 (0.12 GB, last change 2026-11-11)
- F:\LedgerTools\ast-grep (0.1 GB, last change 2026-11-16)
- F:\LedgerTools\dotnet10-download (0.07 GB, last change 2026-10-25)
- F:\LedgerTools\gate\page-check-2026-10-22 (0.06 GB, last change 2026-10-21)
- F:\LedgerTools\bound (0.05 GB, last change 2026-09-30)
- F:\LedgerTools\game-inputs\cmu-2026-11-17-cm (0.05 GB, last change 2026-11-17)
- F:\LedgerTools\game-inputs\cmu-2026-11-17-try2 (0.05 GB, last change 2026-11-17)
- F:\LedgerTools\game-inputs\cmu-2026-11-18-hipcentre (0.05 GB, last change 2026-11-17)
- F:\LedgerTools\vctk-young-men (0.04 GB, last change 2026-11-06)
- F:\LedgerTools\gate\page-frames-2026-10-22 (0.04 GB, last change 2026-10-21)
- F:\LedgerTools\casting-work (0.03 GB, last change 2026-11-06)
- F:\LedgerTools\game-inputs\brick-flemish-photo-n16-5-grey (0.03 GB, last change 2026-11-17)
- F:\LedgerTools\garments\md_suit_jacket (0.03 GB, last change 2026-10-02)
- F:\LedgerTools\proof-2.1-setaside (0.02 GB, last change 2026-10-03)
- F:\LedgerTools\shops-wip-2026-10-03 (0.02 GB, last change 2026-10-03)
- F:\LedgerTools\garments\sheila_blouse (0.02 GB, last change 2026-09-30)
- F:\LedgerTools\proof-2.2-paused (0.01 GB, last change 2026-10-03)
- F:\LedgerTools\review-faces-2026-09-26 (0.01 GB, last change 2026-09-26)
- F:\LedgerTools\ron-voice (0.01 GB, last change 2026-09-25)
- F:\LedgerTools\garments\darren_tshirt (0.01 GB, last change 2026-09-30)
- F:\LedgerTools\garments\sheila_handbag (0.01 GB, last change 2026-09-30)
- F:\LedgerTools\garments\sheila_spectacles (0.01 GB, last change 2026-09-30)
- F:\LedgerTools\gate\prev (0.01 GB, last change 2026-10-08)
- F:\LedgerTools\atlas-01-2026-10-06 (0.0 GB, last change 2026-10-06)
- F:\LedgerTools\casting-candidates (0.0 GB, last change 2026-10-06)
- F:\LedgerTools\cleanup-2026-09-26 (0.0 GB, last change 2026-09-26)
- F:\LedgerTools\game-voice (0.0 GB, last change 2026-09-25)
- F:\LedgerTools\game-voice2 (0.0 GB, last change 2026-09-25)
- F:\LedgerTools\lane-research (0.0 GB, last change None)
- F:\LedgerTools\n16-6-parked (0.0 GB, last change 2026-11-16)
- F:\LedgerTools\pso-record (0.0 GB, last change None)

