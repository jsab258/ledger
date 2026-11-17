# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-17 20:07 (the hourly run; the last session set its Stopped line at 19:52)

**Row due:** 2026-11-17 20:38 (last 19:38; page and advisor read 19:45; last ack 18:11, the pace guard)
**Stopped:** 2026-11-17 19:52 (history past its point at an item's end; no helper or background job running)
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

## Done this run (18:52 to the stop)
- Lane merged (82b9db3e5), ci fixed after it (catalogue, attribution row). His yes to PresentMon (19:36): allowlist item 12, item closed; page: nothing open. n16-11 Q2 decided under the 11 Oct ruling.
- Targets written, reviewed, fixed: TARGET-MICKEYS-NIGHT (front room lit at night, decided from canon) and TARGET-IMAGE-TO-3D-PROPS (DINOv3 licence pick goes with the next order); waiting items 5 and 11 link them; Mickey's night fault in FINDINGS.
- Kiln: double precision try 2 MERGED (Kiln main f901e1f, KILN_DOUBLE=1 off by default; gate 189/189 identical; closed). Cantilever matrix with it on: 12 of 12 settle (4 before).
- Retention step 2: nine open items fixed (try 4); third review PASS WITH FIXES; N-R1 and N-R3 fixed after it. Still off.
- Rows 18:58 and 19:38. Removing C:/Users/Jafar/ledger-lane (clean, merged) refused by the app's safety check: not retried, 0.1 GB left.

## Next, in order
0. FIRST: verdicts after 2026-11-17T18:40:00Z; advisor after the last ack (18:11). Row due 20:38. THE LANE: at each item end `git fetch origin lane-2026-11`, review `git log wip..origin/lane-2026-11`, merge what passes ci (check catalogue and attribution: new research folders and drawings need their lines), a DECISIONS line per merge; steer via production/lane/LANE-QUEUE.md.
1. Kiln, one machine job at a time: (a) bending try 2 = option (a) still unused: first port lane-bending's hinge (6311c22) onto the generic step (geom.rs Pt narrowing, hinge angle and moves for both precisions, about 15 lines, sketched in KILN-BENDING-SCALE's last section) as its own lane, cargo test, gate with switches off identical to 9ca019e; then option (a)'s spacing list with silk and nylon at 6 and 4 mm, KILN_DOUBLE=1. A helper's guard refused that engine edit once: brief engine work explicitly. (b) the speed lane re-checked on f901e1f (advisor 201/193 point 4, Fable allowed), drape time per garment before and after; (c) hang and Cusick re-run with double places.
2. Retention step 2: N-R2 (record link and junction targets; keep any folder they reach, e.g. voice-portable) with a self-test, plus M2, M4 (3 days vs 14 in RULINGS) and N9's part; one fresh check of those fixes only; then mapRulesLive on and owners into storage-map.json (LEDGER or Claude only where certain).
3. Up to eight helpers on machine-free work: the next order's waiting items without targets (1, 8, 12 need his ear); Kiln analysis as results land.
4. n16-8 Tom's crown (full editor; never beside a Kiln gate or bench); n16-7 look and packaged film; n16-6 Sonnet 5.5 packaged run. DAILY by 19:00 tomorrow.
5. Waiting by his pick: n16-5 S2 and n16-3's people ladder (git show 47cfaec10:production/handover/HANDOVER.md, item 1). M5 chain for Ron's trousers: refused twice by the app's permission check, not again without a new way.

## Tonight's machine-free queue (start before 01:15)
1. Kiln code (bending try 2, speed lane) and reviews, no drape runs during the night build. 2. The retention fixes and their review. 3. The next order's waiting list (advisor 192).

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 17 Nov evening: git worktree remove of the PC lane copy refused by the app's safety check (not retried). A helper's cherry-pick of the hinge onto the generic step refused by its guard (engine edit not in its brief). The catalogue reads commas inside a research line as folder names: no parentheses there. FINDINGS and CATALOGUE sit at their caps: trim a word elsewhere to add one.
- 17 Nov: zips gate-r3 stopped before judging (its space check called retention.py mid-edit): not a try. A wait loop matched its own command line (searching process command lines for 'regression_gate' finds the bash running the search): match on python.exe or the exe by name. Two heredoc edits lost backslashes (memory bash-heredoc-backslashes): write such edits with chr(92) or the Edit tool. Registering a Windows scheduled task refused by the app's safety check; superseded by the gate route.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2, 3 and 4 have targets now).
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2 (try 2 not yet run); cantilever bench 1 (passed as a bench); double precision 2 of 2 (try 2 passed, merged); retention step 2: 3 tries (the third under RULINGS 7 Nov, closing the gap; a fourth only if it closes a third of what is left with no new fault); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help (or with no arguments when its docstring shows required ones); let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
