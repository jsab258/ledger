# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-04 13:41 (started by Jafar himself with the goal; his message at 13:38: the hourly take-over failed, fix and test it, no stop at the size until a take-over has worked)
**Stopped:** 2026-11-04 11:26 (an item's end, history about 300,000 tokens; the first live test of the hourly task's start)
(His rulings of 4 November, RULINGS.md: the hourly task "LEDGER: the hourly fresh session" (ledger-daily-fresh-session) runs at :15 from 05:15 to 00:15; each run first runs `python tools/fresh_gate.py` and checks the app's session list, and works only when Stopped is later than Started and no LEDGER session has been active for 15 minutes. Each session runs `python tools/history_check.py` at the end of each item; past its threshold (300,000 tokens while the start is heavy) it rewrites this file, sets Stopped from Get-Date and stops; the next hourly run takes over. Nothing works from 00:45 to 05:10.)

**As of:** Wednesday 4 November 2026, 11:26 (Swiss time).

**The goal:** his order of 2 November (production/orders/2026-11-02.md, now short; its archive production/orders/archive/2026-11-02.md only when an item needs it), until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it.

## Done this session (11:00 on)

- **His two rulings of 4 November recorded** (RULINGS.md: the 3 Nov fresh-session line amended, a lean-start line added; DECISIONS 11:06 and 11:35). A1: the start measured by tools/start_size.py: 122,000 to 155,000 tokens before the first item (the first step 84,000: the app's own about 57,000, our listings about 27,000); the order file 24,800 to 3,600 words (archive joined by order_ledger.py); FINDINGS.md 5,498 to 1,947 words, cap 2,000; CLAUDE.md's read-first line is ruling B's list; fourteen unused account skills hidden in this project (.claude/settings.json skillOverrides; unverified whether it reaches claude.ai-synced skills). A2: the daily task now hourly, tested idle at 11:11 (two steps, WAIT, nothing read); the handover task paused. A3: threshold 300,000. B: production/audits/lean-start/QUALITY-WEEK-2026-11-04.md (the four counts, last week's not yet counted). Told to him in the chat ~11:20 (before 122,000 to 155,000; after estimated about 105,000; the 80,000 mark out of our files' reach).
- **His page:** read 11:05; speech-third-try (yes, 08:47) and handoff-task-mode (done) closed; 0 open (page version 25, "items" collection written).
- **Speech's third try, its target found** (production/research/voice-latency/IN-GAME-2026-11-02.md, the third try's section; DECISIONS 11:35): run F's median is set by the slower check's 1.1 to 3.3 s wait on first sentences it passes; the six refused lines sit behind the same wait (2.3 to 3.5 s) before their flag. So the one try aims at that wait, not only the rewrite. No change made yet, no money spent.

## First, in this order (the next session)

1. Measure your own start: at your first item's first change, `python tools/start_size.py <your log id>` (the newest .jsonl in ~/.claude/projects/C--Users-Jafar-ledger-local); write the result in DECISIONS and tell him the start's real size after, in one line; note whether the skill list shrank (it was about 9,200). Also: did this hourly run start on time after this stop (the first live test of the start path)? One line in DECISIONS either way.
2. Read his page's answers (https://claude.ai/artifact/1VZHkCBAHdw8HBdNHrByL8, collection verdicts).
3. **Speech's third try** (the speech-bench skill; his yes; one try; under US$1 in all; old against new): first, free, which model and request the slower check is (Program.cs, ClaimCheck.cs; the stand-in with LEDGER_TALK_SIZES), its request size and output length, and so what makes its 1.1 to 3.5 s; then one change to that wait; publish the new talk program to F:/LedgerTools/scratch/<try> and run inside the packaged game as run F was (F:/LedgerTools/latency/askreal-2026-11-04f/command.txt, plus -TalkHelper), cap LEDGER_TALK_BUDGET_USD 0.50; old is run F. Pass: median at or under 2.0 s with no new fall-backs; else speech reaches the exit as a missed bar, told plainly.
4. One memory trace (-trace=memory) of the launch and of the close, to name the two peaks (loading; the voice child). Steady use reads under CLOSE-D's 6 GB, the peak not; the exit lists both.
5. The corner's midweek page (as drafted below), then the faster-builds measurement.
6. Fresh reviewers still owed (AT-RISK): the night walk's pictures for Tom's jeans, boots and sitting; Mickey's office pictures again packaged on the 6c808a1 build; Tom as played.
7. The quality guard's baseline: one Sonnet extractor counts last week's four measures from the records into QUALITY-WEEK-2026-11-04.md (its brief: no clicks, records only).
8. After your first item, from your own log's cost per step (tools/token_audit.py), set the lean start's switch point, the handover's own cost counted (A3), and tell him the number. Measured 4 Nov 11:30 on the twelve newest logs (token_audit.step_cost by 50,000-token band): about US$0.07 a step from 50,000 to 300,000, then 0.089 (300,000 to 350,000), 0.105 (350,000 to 400,000), 0.160 beyond; a handover's own cost is your start (its first steps' cache writes) plus this file's writing: measure it from your log, then set the point where the extra per step past it has cost one handover (about 300,000 to 325,000 if a handover costs about 50 steps' extra).

## Tried and failed, and why (this session)

- The chaining of 3 November: the session stopped at 09:38 and nothing took over, because a scheduled run may not start another; replaced by the hourly task (his ruling A2).
- A start under 80,000 tokens: not reachable by the project's files; the app's own prompt and tools are about 57,000 before any file. What is ours (about 27,000 in the listings, plus the reads) is being cut.

## In flight (carried)

- Corner step 6's second part (the wall's tone over metres): first packaged in last night's walk; look at its pictures (step-NNN.jpg under the walk's folders) for it and the faint copper sheen on lifted chimney bricks.
- **The corner's midweek page:** the played copy with the street's switches and `-PageShots=day` (then `night`), `-RenderOffScreen -ResX=2560 -ResY=1440`, cam_hook, cam_A, cam_B, cam_mickeys, cam_reverse to Saved/PageShots/<camera>-<day|night>.png; one fresh final reviewer per frame beside F:/LedgerTools/gate/last-good/corner; item id corner-midweek-2026-11-04, pictures under production/approvals/needs-you/pictures/; text, shortfalls first: "The corner at midweek: brick no longer repeats and varies over each wall; litter, crates, kiosk, A-board and a reaction at Rita's window are in. Still short of the Hook sheet: plain stretcher brick without its burnt headers, walls even from top to bottom, the white base layer on the people, red-clipped brick under the lamps at night." Decisions: (1) direction (keep going, recommended / not like this); (2) Mickey's gilt letters as real metal (recommended; BASELINE-2026-11-02.md row 42) / gold paint. Look at the published page at phone width before the NEEDS YOU.
- Corner step 9 planned (STEP9-PLAN-2026-11-03.md): after the office passes packaged and the midweek page.
- Phase 3's port U8: in last night's build; the walk's session lines should show no "loadRefused".
- The two "Builder" sessions (local_5c6c1f0b, local_c43d83c9) show activity while not running (remote control): this morning's start waited 38 minutes on them.

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs. Stash@{0} (06:10 editor-rebuilt material files) kept.
- Waiting list: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own.
- Tries used: the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 2 of 2 plus his yes to a third (08:47), not yet spent; the office's damp stain outline would be a third try (his yes first).
- API spend today: US$0.40 (run F).

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage; work while another LEDGER session works.
