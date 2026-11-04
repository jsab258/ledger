# Handover: where the production session stands

The one file a fresh session starts from (his rulings of 3 November: a fresh session every day, never two at once). Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's; the phase's items are NOW.md's; this file holds only what is in flight.

**Started:** 2026-11-04 06:09 (the 05:15 run of ledger-daily-fresh-session; held from 05:21 until both Builder sessions had been quiet 15 minutes)
**Stopped:** 2026-11-04 06:33 (history at about 175,000 tokens after speech run F, close to the switch; the next session started by the app's run of ledger-fresh-session-handoff, or ledger-daily-fresh-session if that is refused)
(His rulings of 3 November: a fresh session by the history's size, never two at once. Each session runs `python tools/history_check.py` at the end of each item; past 200,000 tokens it rewrites this file, sets Stopped from Get-Date, starts the next session with the app's run of the task ledger-fresh-session-handoff (or ledger-daily-fresh-session when the first is its own run), and stops; the next begins only when Stopped is later than Started and no session in the checkout has been active for 15 minutes, then sets Started. The 05:15 daily run is the backstop; nothing works from 00:45 to 05:10.)

**As of:** Wednesday 4 November 2026, 06:33 (Swiss time). A fresh session starts with a history of about 145,000 tokens (the system prompt and rules), so expect each session to hold only an item or two.

**The goal:** his order of 2 November (production/orders/2026-11-02.md), item by item, until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it in full.

## Done this morning (06:09 to 06:33)

- The day's summary and the overview in FOR-JAFAR.md (token shares for 3 Nov: history 53%, Opus 98%, reviewing 27%); the progress page published with today's pictures (version 29); pushed to wip, ci 93 of 93.
- The night walk (production/playtest/nightly/2026-11-04.md), build 6c808a1 = wip 3738e401: ran in full, 14 of 15 stages, lost sight of Darren; "that's all I know" 3 of 60; broke the illusion: the white base layer (Ron, the woman by Mickey's), Ron heard while out of sight, the road ending in a grey slab and blank sky. Its pictures of the new brick, A-board, crates, kiosk and Rita's reaction not yet looked at (step-NNN.jpg under the walk's folders).
- **Speech run F** (packaged, shipped talk, 30 lines from the 20 held newcomer questions, -AskNear, cap 0.80): median 2.02 s, 14 of 30 at or under 2.0 s, p90 6.04, worst 8.22, no fall-backs, 2 timed out (the check flagged the first sentence, the redraft passed 8 s); every question went to Haiku 4.5. US$0.40, logged in api-spend.jsonl. Fresh small review PASS WITH FIXES (F:/LedgerTools/latency/askreal-2026-11-04f/review.json), fixes made. Note: IN-GAME-2026-11-02.md (run F row, D's line marked superseded); DECISIONS 06:33; NOW.md line 1. Committed with this file and pushed to wip.
- The three editor-rebuilt material files were set aside in a stash (stash@{0}, "2026-11-04 06:10 ..."), since discarding them was refused; kept, not dropped.

## First, in this order (the next session)

1. Check the push above reached wip (git log origin/wip -1: speech run F); if not, push it (ci-checks to failed=none first; unset MSYS).
2. Read his page's answers (https://claude.ai/artifact/1VZHkCBAHdw8HBdNHrByL8, collection verdicts; last read 06:14, nothing new since 3 Nov 10:10). One item open: handoff-task-mode-2026-11-03.
3. **Speech's third try, his call (the speech-bench skill; RULINGS 1 Nov rule 4):** the bar is missed by 0.02 s on its own measure, two tries spent. Put one item on his page (the his-page skill, step 3) and send the NEEDS YOU first: a third try, once, with its reason: the tail is the check's redrafts (7 of 30 at 4 s or more); the cheapest lever is the one the run points to (the check flagging a first sentence that was then rewritten); options yes (recommended, about 2 hours, under US$1) / no, stop rule (report speech as a failed capability). Check the lever's standing in SPEECH-LEVERS-2026-11-01.md first; the fast checker's cut-off and prepared openers are his calls, never moved without his word.
4. **The AT-RISK list, Wednesday is its deadline:** production/audits/phase1-exit/AT-RISK-2026-11-02.md, update with run F and the walk, one fresh review, then tell him in plain words in the chat what may miss 9 November (a report, no ask in it).
5. Card memory (AT-RISK's High row, CLOSE-D): measure packaged on the 6c808a1 build (powershell -File tools/p1-packaged.ps1, its memory lines); over 6 GB: brick scans and maps at 1024 px (brick map halved by nearest), a small piece.
6. The corner's midweek page (as drafted below), then the faster-builds measurement.

## In flight (carried from 3 November)

- Corner step 6's second part (the wall's tone over metres, macro 0.08 / 0.0025): pushed, first packaged in last night's walk; look at the walk's pictures for it and for the faint copper sheen on lifted chimney bricks.
- **The corner's midweek page:** the played copy with the street's switches and `-PageShots=day` (then `night`), `-RenderOffScreen -ResX=2560 -ResY=1440`, cam_hook, cam_A, cam_B, cam_mickeys, cam_reverse to Saved/PageShots/<camera>-<day|night>.png; one fresh final reviewer per frame beside F:/LedgerTools/gate/last-good/corner; item id corner-midweek-2026-11-04, pictures under production/approvals/needs-you/pictures/; text, shortfalls first: "The corner at midweek: brick no longer repeats and varies over each wall; litter, crates, kiosk, A-board and a reaction at Rita's window are in. Still short of the Hook sheet: plain stretcher brick without its burnt headers, walls even from top to bottom, the white base layer on the people, red-clipped brick under the lamps at night." Decisions: (1) direction (keep going, recommended / not like this); (2) Mickey's gilt letters as real metal (recommended; BASELINE-2026-11-02.md row 42) / gold paint. Look at the published page at phone width before the NEEDS YOU.
- Corner step 9 planned (STEP9-PLAN-2026-11-03.md): after the office passes packaged and the midweek page.
- Phase 3's port U8 (the load check refuses an unreadable day or clock): in last night's build; the walk's session lines should show no "loadRefused".
- The fresh-session test (scheduled task ledger-fresh-session-test-2026-11-03): stopped at its first write waiting for his approval; its session still shows running; result, if any, F:/LedgerTools/scratch/fresh-start-test-2026-11-03.txt.
- The two "Builder" sessions (local_5c6c1f0b, local_c43d83c9) show activity every few minutes while not running (remote control): this morning's start waited 50 minutes on them. Their transcripts can be read with list_events rather than waiting two hours (as on 3 Nov 22:14).

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs.
- Waiting list added 3 Nov: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear. Worth adding at the next order: Flemish bond with burnt headers for the corner's brick.
- Tries used: the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 2 of 2 (run F was a measure, not a try); the office's damp stain outline would be a third try (his yes first).
- API spend today: US$0.40 (run F).

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage; work while another LEDGER session works.
