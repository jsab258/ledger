# Handover: where the production session stands

The one file a fresh session starts from (his rulings of 3 November: a fresh session every day, never two at once). Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's; the phase's items are NOW.md's; this file holds only what is in flight.

**Started:** 2026-11-04 08:43 (a run of ledger-fresh-session-handoff; held from 08:05 until both Builder sessions had been quiet 15 minutes)
**Stopped:** 2026-11-04 09:38 (history past 180,000 tokens after the at-risk list and the memory diagnosis; the next session started with the app's run of ledger-fresh-session-handoff)
(His rulings of 3 November: a fresh session by the history's size, never two at once. Each session runs `python tools/history_check.py` at the end of each item; past 200,000 tokens it rewrites this file, sets Stopped from Get-Date, starts the next session with the app's run of the task ledger-fresh-session-handoff (or ledger-daily-fresh-session when the first is its own run), and stops; the next begins only when Stopped is later than Started and no session in the checkout has been active for 15 minutes, then sets Started. The 05:15 daily run is the backstop; nothing works from 00:45 to 05:10.)

**As of:** Wednesday 4 November 2026, 09:38 (Swiss time). A fresh session starts with a history of about 145,000 tokens, so expect each session to hold only an item or two.

**The goal:** his order of 2 November (production/orders/2026-11-02.md), item by item, until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it in full.

## Done this session (08:43 on)

- His page read 08:50 (nothing new since 3 Nov 10:10). **Speech's third try asked:** item speech-third-try-2026-11-04 on Needs you (published, version 24; written to "items"), the NEEDS YOU sent 08:58. Open items now 2: that and handoff-task-mode-2026-11-03 (this run of the handoff task wrote files without stopping, so the mode looks set; leave it for his tap).
- **Card memory and the Stutter, packaged** (p1-packaged, 6c808a1, labels *-6c808a1-scans in runs.jsonl): the game's card median 5.66 to 5.76 GB, peaks 6.0 to 8.1; 1 frame over 33 ms in 5,400 (33.6 ms).
- **The peak diagnosed** (Opus diagnoser, read-only; F:/LedgerTools/scratch/card-peak-2026-11-04/DIAGNOSIS.md): a once-a-launch spike of about 2 GB for 1 to 4 s outside the measured frames, in 22 of 118 captures since October; inside the frames about 5.4 GB. Not the brick scans (about 134 MB, uncompressed, no mips): the 1024 px cut set aside (DECISIONS 09:05).
- **The AT-RISK list** (production/audits/phase1-exit/AT-RISK-2026-11-02.md) updated with run F, the walk, memory and the diagnosis; fresh small review PASS WITH FIXES (F:/LedgerTools/scratch/at-risk-review-2026-11-04.json), fixes made; **told to him in the chat ~09:12** (Wednesday's deadline met). All pushed to wip, ci 93 of 93.
- **The sampler mended** (tools/p1-packaged.ps1: one counter call, series kept each second, the game's children counted and ended). Its first series (label packaged-day-stand-6c808a1-series) places the peak: 8.06 GB about 10 s after launch, steady 5.72 to 5.80 GB through play, 6.8 to 7.8 GB in the last 8 s once the game's voice child appears (DECISIONS). Committed.

## First, in this order (the next session)

1. Read his page's answers (https://claude.ai/artifact/1VZHkCBAHdw8HBdNHrByL8, collection verdicts). Speech yes: the third try, once, at the refused first sentences (six of the seven slow lines in run F), the speech-bench skill, under US$1, old against new; no: speech reaches the exit as a missed bar. Close the item either way (the his-page skill, step 6).
2. One memory trace (-trace=memory) of the launch and of the close to name the two peaks (loading; the voice child). CLOSE-D's 6 GB: steady use reads under it, the peak not; the exit lists both.
3. The corner's midweek page (as drafted below), then the faster-builds measurement.
4. Fresh reviewers still owed (AT-RISK): the night walk's pictures for Tom's jeans, boots and sitting; Mickey's office pictures again packaged on the 6c808a1 build; Tom as played (which body and walk, from the night walk's log).

## In flight (carried)

- Corner step 6's second part (the wall's tone over metres): first packaged in last night's walk; look at its pictures (step-NNN.jpg under the walk's folders) for it and the faint copper sheen on lifted chimney bricks.
- **The corner's midweek page:** the played copy with the street's switches and `-PageShots=day` (then `night`), `-RenderOffScreen -ResX=2560 -ResY=1440`, cam_hook, cam_A, cam_B, cam_mickeys, cam_reverse to Saved/PageShots/<camera>-<day|night>.png; one fresh final reviewer per frame beside F:/LedgerTools/gate/last-good/corner; item id corner-midweek-2026-11-04, pictures under production/approvals/needs-you/pictures/; text, shortfalls first: "The corner at midweek: brick no longer repeats and varies over each wall; litter, crates, kiosk, A-board and a reaction at Rita's window are in. Still short of the Hook sheet: plain stretcher brick without its burnt headers, walls even from top to bottom, the white base layer on the people, red-clipped brick under the lamps at night." Decisions: (1) direction (keep going, recommended / not like this); (2) Mickey's gilt letters as real metal (recommended; BASELINE-2026-11-02.md row 42) / gold paint. Look at the published page at phone width before the NEEDS YOU.
- Corner step 9 planned (STEP9-PLAN-2026-11-03.md): after the office passes packaged and the midweek page.
- Phase 3's port U8: in last night's build; the walk's session lines should show no "loadRefused".
- The two "Builder" sessions (local_5c6c1f0b, local_c43d83c9) show activity while not running (remote control): this morning's start waited 38 minutes on them.

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs. Stash@{0} (06:10 editor-rebuilt material files) kept.
- Waiting list: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own.
- Tries used: the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 2 of 2 (third asked); the office's damp stain outline would be a third try (his yes first).
- API spend today: US$0.40 (run F).

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage; work while another LEDGER session works.
