# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-17 16:37 (the hourly run; the last session set its Stopped line at 16:31)

**Row due:** 2026-11-17 16:29 (last 15:29, overdue at the stop; page and advisor read 16:20; last ack 16:12, advisors 201/202)
**Stopped:** 2026-11-17 16:31 (history past its point at an item's end; ONE helper still running: the Kiln convergence gate, self-contained, see 'At the stop')
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). The doubled line, full pace: 36% at 15:28, about 14 behind. This week (RULINGS, his picks 16:05): eight helpers a session, a machine-free lane session (production/lane/), Fable up to 20% for the hardest code (name Fable helpers and the share in rows), high effort on hard code and reviews. week-shape.json's reset_at stays null until HE presses the spare reset.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00. Each row: helper count and rate (advisor 195), F:'s free room and the next 12 h's need (advisor 189), what fills each helper place (advisor 198).
- **Every time stamp from Get-Date at the moment of writing**.
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page or the progress page: read the live page and each published file first (out_dir to the scratchpad), diff, then publish.
- **Kiln (RULINGS 13 and 14 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone from M5; M7 count in every round report (0 so far). Time log "tool loop: <tool> round n". Advisor 182 trial: Kiln rounds and judging run in helpers that hand back a short verdict only.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads; they live only in F:/LedgerTools/tool-dev/judge/heldback (hash-locked).
- **Advisor 189-192:** `python tools/retention.py space` before every Kiln round, film, build, capture and in every helper brief; each round deletes its own bulky outputs once its numbers are reported; no new drives; target 1.4 points an hour; when the current order waits on the machine, free helper places take the next order's machine-free work, recorded in the order ledger.
- **Advisor 194:** any ask needing his hands, allowance or sign-in goes on the page the same hour.
- **Advisors 196-198 (storage and backup, his picks 12:43 and 12:58):** RULINGS 17 Nov line replaced 2 Oct's: every folder has a shelf in production/storage-map.json; writes and deletes only through retention.py and the map; nothing of his on it; mh-dress is lasting. Backup: the lasting shelf to Dropbox nightly about 05:00, never deletes or overwrites, never keys, Kiln to Dropbox only (bundle), 26 h staleness item, weekly restore check, FLOOR 40 GB on C:.
- **His page items (his message 14:38, advisor 199):** every item tagged ACTION, DECISION or REVIEW (needs_you_page.py refuses an untagged open item); places named as he sees them (Claude app, Scheduled tasks, "LEDGER: the hourly fresh session", History, "Today at H:MM AM/PM" = the run that started the working session: A NEW SESSION UPDATES THAT TIME IN EACH OPEN ACTION ITEM IN THE HOUR IT TAKES OVER, publishes, and updates the items doc); all PC steps in one ACTION item; ACTION items that stop work or protect the backup are not held by the two-batch limit; after Done, check it really happened and say so in the row. Layout (advisor 200): title, at most two why bullets, numbered steps; the page's check enforces it.
- **Before writing Stopped: end every background job of your own** (fresh_gate.py holds starts up to 120 min while any session's background command still runs).

## Done this run (14:22 to the stop)
- Backup: the same-minute overwrite fixed, the other low findings made rules (audit's last section). Dropbox online-only measured: Dropbox clears attrib's mark within 10 s, only his right-click works.
- His yes on the remove list acted on 14:41: 14.6 GB removed through retention.py (protection narrowed in retention.json first); storage map 132 folders plus the lane's two.
- His page: tags (advisor 199), phone layout with title, why bullets and numbered steps (advisor 200), both enforced by needs_you_page.py; two open ACTION items: backup-schedule-at-pc (schedule + Dropbox online-only, one visit) and lane-task-at-pc (the lane's scheduled task).
- RULINGS: this week's exception (advisors 201, 202, his picks 16:05). Lane session prepared: tools/lane_gate.py, production/lane/ (handover, prompt, setup steps, lane-prompt.txt), sparse worktree C:/Users/Jafar/ledger-lane (95 MB, ff to wip 16:25, its gate says LANE GO).
- retention.py step 2: map expiry rules in, OFF until retention.json "mapRulesLive": true after a fresh hostile review (production/research/disk/RETENTION-STEP2-2026-11-17.md).
- Next order's machine-free work: TARGET-STREET-FURNITURE, PLAN-PARKED-CARS (25-41 h for the first car against the order's 12 h: restate in the next order), UE4SS-METHOD-LICENCE (mostly unverified: re-read before n16-11).
- Kiln: zips baseline re-taken on main (43d4b0f); zips gate FAILED on jeans seconds alone (123 vs 78 ±19.6; my parallel bench helpers loaded the CPU; drape measures all equal). Convergence try 2 PASSED its goal (lane-convergence 173e1ac: Normal runs Fitting's solve, 13 of 13, Normal ~6x slower). Cantilever bench rebuilt (lane-benches 0ca5376: 0 fallbacks, only 4 of 12 settle). Bending try 1 (lane-bending 6311c22, hinge angles): Denim passes, Rib, twill, nylon, silk do not. Settle diagnosis (Fable): float32 positions 6 m from the origin keep strips moving (KILN-SETTLE-DIAGNOSIS-2026-11-17.md).

## At the stop
- ONE HELPER STILL RUNNING: the convergence gate (waits for a quiet machine, gates lane-convergence switch-off, merges into Kiln main ONLY on PASS, appends "Convergence gate" to KILN-BENCHES-2026-11-17.md). Read that section first; do not start drape runs until it has written its result.
- Uncommitted on purpose: nothing of this run (all committed); the office prints and untracked shop-room files as before.

## Next, in order
0. FIRST: verdicts after 2026-11-17T15:25:00Z; advisor after the last ack (16:12, advisors 201/202). Update "Today at 2:21 PM" in backup-schedule-at-pc to your own run's time (the app's History label), publish, update the items doc. If he tapped Done on either ACTION item: check (the LEDGER backup task exists; the Dropbox folder is online-only and `python tools/backup-to-dropbox.py --verify` is not needed, use `--restore-check`; the lane task's first run shows a Started time in C:/Users/Jafar/ledger-lane/production/lane/LANE-HANDOVER.md) and say so in the row. Once the lane runs: merge its branch "lane" at item ends; rows give both sessions' combined rate (target 1.8 an hour until within 6 points of the line).
1. Kiln, one machine job at a time, nothing else on the CPU during a gate (memory kiln-gate-needs-quiet-machine): (a) the convergence gate's result; (b) re-run the zips gate unchanged on a quiet machine (commands in KILN-ZIPS 'Round 2'; lane-zips c58553d, exe in zips-r2-2026-11-17/exe), merge on PASS; (c) merge lane-benches (bench code only) after the gates; (d) the speed lane re-checked on the new engine (advisor 201/193 point 4, Fable allowed, high effort), drape time per garment before and after in the report and the row; (e) the settle confirm run (1 min, report's section 6), then double-precision positions on a new lane (try 1); (f) bending try 2 = option (a) after (e) (DECISIONS 16:30).
2. Up to eight helpers on machine-free work (advisor 201): a fresh hostile review of retention.py step 2, then mapRulesLive on; next order's research; Kiln analysis as results land; leave a place empty only with a reason in the row.
3. n16-8 Tom's crown (needs the full editor: only when no Kiln gate runs); n16-7 look and packaged film; n16-6 Sonnet 5.5 packaged run (never during a Kiln gate). DAILY by 19:00 (production/research/token-audit/DAILY-2026-11-17.md).
4. Waiting by his pick: n16-5 S2 and n16-3's people ladder (git show 47cfaec10:production/handover/HANDOVER.md, item 1). M5 chain for Ron's trousers: refused twice by the app's permission check, not again without a new way.

## Tonight's machine-free queue (start before 01:15)
1. Kiln code (double-precision lane, speed lane) and reviews, no drape runs during the night build. 2. The retention review. 3. The next order's waiting list (advisor 192).

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 17 Nov: zips gate failed on time alone from parallel CPU load (a measurement, not a fix try). The lane prompt link on the artifact did not open (the address drops the file part); the step points to the file on his PC instead. Registering a Windows scheduled task refused by the app's safety check (on his page).
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2 and 4 have targets now).
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2; cantilever bench 1 (passed as a bench); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none today.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes beside a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works (the lane is separate); write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
