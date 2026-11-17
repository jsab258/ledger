# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-17 20:07 (the hourly run; the last session set its Stopped line at 19:52)

**Row due:** 2026-11-17 21:57 (last 20:57; page and advisor read 20:55; last ack 20:56)
**Stopped:** 2026-11-17 21:03 (history past its point at an item's end; no helper or background job running)
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

## Done this run (20:07 to the stop)
- Lane merged (f56fead36, street furniture plan); ci 103/103; pushed to wip at about 20:25.
- Advisor 1940-eff and 2010-207 acknowledged. Step-growth table: token_measures.py --top-helpers; 17 Nov no helper run over 300 steps, so hand-backs unchanged (advisor's own condition).
- Output cap (n16-10): tools/output_cap.py built, reviewed (PASS WITH FIXES, all needed fixes in), self-test 126/126, committed. Switching the hook on in .claude/settings.json was REFUSED by the app's safety check: ACTION item output-cap-switch-on-2026-11-17 on his page (his-setting), NEEDS YOU sent. When he says it in chat: add the PreToolUse entry from production/research/tool-tests-2026-11/HOOK-OUTPUT-CAP-SETTINGS.json, check one real run (capped text, cd carries, no "hook changed input" denial), add its RULINGS enforcer entry (rulings-enforcers.json), close the item.
- Retention step 2: N-R2, M2, M4 (14 days), N-R9 fixed; fourth review PASS WITH FIXES; its fault 1 fixed (151 checks). mapRulesLive stays OFF until the first real plan with pending rows gets one fresh look (fault 2). Night task's Python is 3.12.8.
- Kiln: bench judging range merged on Kiln main (f78b98f): judged 7 of 12 (4 before). Hinge ported onto the generic step: lane-hinge-generic eb65d0d (cargo test 50/50), exe C:/LedgerTools/kiln-runs/bending2-2026-11-17/drape-studio-hinge-eb65d0d.exe (sha 6834da1d). Speed lane ported: lane-speed2 a588941 (worktree C:/LedgerTools/kiln-lanes/speed2; off = bit-identical; exe C:/LedgerTools/cargo-target/kiln-speed/release/drape-studio.exe; licence accepted, DECISIONS). Parity list: F:/LedgerTools/tool-dev/reports/KILN-PARITY-LIST-2026-11-17.md (4 garments drape today, M7 0; gap order decided: drape-to-game first).
- n16-2: Ron's routine and talk already exist (RON-ROUTINE-TALK-2026-11-17.md); talk gap for later hours is waiting item 14.
- Hang and Cusick benches started then stopped (108 strips, about 3 min each at 10 mm: hours); run a reduced set later.

## Next, in order
0. FIRST: verdicts after 2026-11-17T19:55:00Z; advisor after the last ack (2055-209). Then finish his cars rulings of 20:44/20:48 (advisors 208, 209; RULINGS and canon done): PLAN.md, the roadmap, the asset plan SUMMARY order (traffic into the friends' build), the progress page (station 8 traffic into the friends' build, station 11 "driving, once the map is bigger", AAA end state); put the traffic item with the lane's hours (production/research/lane/TRAFFIC-COST-2026-11-17.md when it lands) into the running list for the order of 23 Nov. Lane: fetch and review as before.
1. DONE: hinge gate PASS (inside every band), merged on Kiln main fdd3a6d. Any later gate must set KILN_EXE (else it takes C:/LedgerTools/cargo-target/kiln/release, an older build).
2. THEN, quiet machine: the speed timing (advisor 2010-207, next machine job): plan and ready script in F:/LedgerTools/tool-dev/reports/KILN-SPEED2-PORT-2026-11-17.md (six runs per garment, Tom j3 and Ron's trousers; check KILN_GPU_LOG); drape time per garment before and after in the row; then merge lane-speed2 after the hinge (same step: care with conflicts), gate again with switches off.
3. Bending try 2 option (a) on the merged hinge: spacing list, silk and nylon at 6 and 4 mm, KILN_DOUBLE=1, KILN_XPBD=1.
4. Kiln gap 1 (plan and adapter committed: production/research/phase2-plan/KILN-TO-GAME-PLAN-2026-11-17.md, tools/kiln_to_game.py): re-export the armline trousers OBJ from its .drape on a quiet machine (the final OBJ is gone), then steps A to J; open: the weights-body match, the hem over his boots, the Kiln front-end adoption tap before step I (check whether it is his). Never beside a Kiln gate.
5. Retention: the first real plan with pending rows gets one fresh look, then mapRulesLive on.
6. n16-8 Tom's crown, n16-7, n16-6 Sonnet 5.5 packaged run; nightly: nothing in Unreal 01:15-04:30.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 17 Nov night: switching on the output-cap hook in .claude/settings.json refused by the app's safety check (not retried; his page). The first hinge gate ran the wrong engine (no KILN_EXE): stopped, not a try. Hang and Cusick full matrix too long beside the machine queue: stopped, not a try. Two time stamps written without Get-Date, corrected (acks, DECISIONS).
- 17 Nov evening: git worktree remove of the PC lane copy refused by the app's safety check (not retried). A helper's cherry-pick of the hinge onto the generic step refused by its guard (engine edit not in its brief). The catalogue reads commas inside a research line as folder names: no parentheses there. FINDINGS and CATALOGUE sit at their caps: trim a word elsewhere to add one.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2, 3 and 4 have targets now).
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2 (try 2 not yet run); cantilever bench 1 (passed as a bench); double precision 2 of 2 (try 2 passed, merged); retention step 2: 3 tries (the third under RULINGS 7 Nov, closing the gap; a fourth only if it closes a third of what is left with no new fault); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help (or with no arguments when its docstring shows required ones); let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
