# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-17 21:22 (the hourly run; the last session set its Stopped line at 21:03)

**Row due:** 2026-11-18 00:06 (last 23:06; page and advisor read 22:50; last ack 22:39)
**Stopped:** 2026-11-17 23:06 (history past its point at an item's end; no helper or background job running)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). The doubled line, full pace: 37% at 16:47 against 52.5%, about 15 behind. This week (RULINGS, his picks 17 Nov): eight helpers a session, a machine-free lane session, Fable up to 20% for the hardest code (3.3% today), high effort on hard code and reviews. week-shape.json's reset_at stays null until HE presses the spare reset.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00. Each row: helper count and rate (advisor 195), F:'s free room and the next 12 h's need (advisor 189), what fills each helper place (advisor 198).
- **Every time stamp from Get-Date at the moment of writing**.
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page: read the live page and items.json first (out_dir to the scratchpad), diff, then publish.
- **His hands only when nothing else can (advisors 203, 204, RULINGS 17 Nov):** an ACTION item needs only_you (sign-in, purchase, licence, taste, his-setting) and a one-line tried; needs_you_page.py refuses it otherwise. Look for a route through what already runs first.
- **Every standing ruling names its enforcer (advisor 205):** a new or changed RULINGS line gets its entry in production/rulings-enforcers.json the same day (file::message, an advisor check, or monday-audit); the pre-commit hook runs tools/rulings_check.py when RULINGS or the list changes; the start gate prints its line.
- **Kiln (RULINGS 13 and 14 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone from M5; M7 count in every round report (0 so far). Kiln's share now measurable: `python tools/token_measures.py --kiln-share`.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads; they live only in F:/LedgerTools/tool-dev/judge/heldback (hash-locked).
- **A Kiln gate runs alone (memory kiln-gate-needs-quiet-machine):** no builds, drapes or bench runs beside it, and do not edit tools/retention.py while one runs (its space check calls the script: an edit mid-gate stopped gate-r3).
- **Advisor 189-192:** `python tools/retention.py space` before every Kiln round, film, build, capture and in every helper brief; each round deletes its own bulky outputs once its numbers are reported; target 1.4 points an hour; free helper places take the next order's machine-free work, recorded in the order ledger.
- **Storage and backup (advisors 196-198, 203):** every folder has a shelf in production/storage-map.json; writes and deletes only through retention.py and the map; nothing of his. The backup now starts from tools/fresh_gate.py when the last good one is over 20 h old (outside 01:15-04:30, never beside Unreal or a Kiln gate, 3 h lock file production/handover/backup-start.lock); the post-commit hook is the second chance; `backup-to-dropbox.py --stale` the 26 h alert. No Windows task, no Dropbox online-only (C: 50 GB, floor 40; if tight, free our own C: space first through the map).
- **His page items (advisors 199, 200):** tagged ACTION, DECISION or REVIEW; title, at most two why bullets, numbered steps; places named as he sees them; after Done, check it happened and say so in the row.
- **Before writing Stopped: end every background job of your own.**

## Done this run (21:22 to the stop)
- His reset ruling of 21:12 (advisor 210): pace_line.py's first leg tops at 99 (selftest 17/17); RULINGS pacing line and its enforcer (advisor backstop 21:35); both acked. Rows project when 98% comes; near 98% while he sleeps (23:00-07:00) slow to stay under 99%, never 100%.
- His car rulings carried: PLAN (phase 2 parked cars after P9; phase 4 traffic), asset plan SUMMARY order item 8, progress page stations 4, 8, 11. Traffic costed by a helper (about 29 h after the sample car), fresh review PASS WITH FIXES applied: production/research/traffic/TRAFFIC-COST-2026-11-17.md; waiting item 15 in the order of 16 Nov.
- Lane merged and pushed (ee12c86e8); later commits not pushed.
- His page: DECISION item kiln-front-end-licence-2026-11-17 (the Kiln front end's licence tap the design note requires before step I of gap 1; never asked before); NEEDS YOU sent.
- Kiln speed timing (advisor 2010-207): the plan's script named the pre-16 Nov bodies and was refused at once (setup, not a try); fixed to the standard bodies as the regression gate does (fixed script beside the runs: time1.sh). Results in F:/LedgerTools/tool-dev/runs/kiln-speed2-2026-11-17/*/time.txt; the refused first series in ...-refused (own leftover: delete, one line). Seen so far, Tom j3: cpu 103 s, card-exact 229 s, card-colour 66 s, xpbd-cpu 1016 s.
- Merge snag found (recorded in the speed report's last section and DECISIONS 21:37): main's hinge (on by default under XPBD) is a Link the card would solve as a plain distance link; the merge must refuse KILN_GPU with hinge bending on, with a test.

## Next, in order
0. FIRST: verdicts after 2026-11-17T21:50:00Z; advisor after the last ack (2235-214, 22:39). wip pushed at 23:06.
0b. His study ruling (advisor 214): check built, tools/outside_only_check.py, in ci (repo and tools/ clean). Its F: hits (FModel, the SH2 reader, an empty inZOI folder in F:/LedgerTools/aaa-study) are protected by the map: retention refused; they wait as AWAITING in the check. Put a DECISION on his page in tomorrow's first batch (delete them, recommended yes; his_files); today's two batches are used. Old memories on FModel and Mafia extracts are void: update them; check FModel's AppData settings hold no key.
0c. Kiln first (advisor 213): DONE, targets written (b515c5a0b). Fill free helper places from the design note's ready Kiln list. Targets now in the design note's last section (proposed card limits; GarmentCode is MIT but not on the allowlist, which lists items: his licence tap before use). Each row: Kiln's share of the main session since the morning (28.8% this week at 22:38; 60% from Wednesday morning).
1. Timing DONE (report's table and verdict): converged solve, card colour 1.8x (j3) and 2.35x (trousers, drop passes); exact order always slower; old solve colour fails the trousers' drop. Judge j3's card objs (judge counts; hang.py vs M2's 25 mm); objs kept in the runs folder.
2. Merge lane-speed2 onto Kiln main fdd3a6d in a new worktree with the hinge refusal and its test; cargo test; build; gate alone with every switch off, KILN_EXE set to the new build. Nothing beside it.
3. Bending try 2 option (a): script ready (C:/LedgerTools/kiln-runs/bending2-2026-11-17/try2-a/bending2.sh: darren_nylon and Silk Charmeuse Cusick at 6 and 4 mm, Fitting, KILN_XPBD=1 KILN_DOUBLE=1, engine drape-studio-hinge-eb65d0d.exe; 6 mm took about 14 min a run, 4 mm longer).
4. Kiln gap 1 (KILN-TO-GAME-PLAN-2026-11-17.md): re-export the trousers OBJ, steps A to J; step I waits on his licence tap.
5. Retention: `retention.py plan` (not beside a timing or gate); the first real plan with pending rows gets one fresh look, then mapRulesLive on.
6. n16-8 Tom's crown, n16-7, n16-6; nightly: nothing in Unreal or heavy local jobs 01:15-04:30.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 17 Nov late: the speed timing's first series refused by the body standard (old body paths in the plan's script; not a try). Two time stamps guessed (22:00, 22:10), corrected from the clock.
- 17 Nov night: switching on the output-cap hook in .claude/settings.json refused by the app's safety check (not retried; his page). The first hinge gate ran the wrong engine (no KILN_EXE): stopped, not a try. Hang and Cusick full matrix too long beside the machine queue: stopped, not a try. Two time stamps written without Get-Date, corrected (acks, DECISIONS).
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2, 3 and 4 have targets now).
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2 (try 2 not yet run); cantilever bench 1 (passed as a bench); double precision 2 of 2 (try 2 passed, merged); retention step 2: 3 tries (the third under RULINGS 7 Nov, closing the gap; a fourth only if it closes a third of what is left with no new fault); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help (or with no arguments when its docstring shows required ones); let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
