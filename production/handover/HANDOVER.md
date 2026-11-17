# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-17 16:37 (the hourly run; the last session set its Stopped line at 16:31)

**Row due:** ROWDUE
**Stopped:** STOPPED
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

## Done this run (16:37 to the stop)
- His messages via the advisor (203-206) acted on and acknowledged: PC tasks withdrawn (page: nothing open); backup started by the gate; ACTION items need a reason only he can meet; every ruling's enforcer listed (84 of 84) and checked on commit; seven new checks; the lane is the advisor's cloud task.
- Retention step 2: two hostile reviews failed it; three fix tries; off.
- Kiln: convergence, zips (5ee46da) and benches (911bfdc) merged; double precision rests truly but failed its gate (diagnosed: the jobs' sensitivity).
- Next order's targets: props, light and weather, hill crowns, Rita's fixes; the quay-end stop diagnosed (FINDINGS). DAILY-2026-11-17 written.

## Next, in order
0. FIRST: verdicts after 2026-11-17T16:30:00Z; advisor after the last ack (advisor 206). THE LANE (his pick about 17:15, advisor 206): runs in the cloud as the advisor's hourly task (at :15, to 23 Nov 07:00) on branch lane-2026-11, writing only production/lane/, production/research/lane/, tools/lane/. At each item end: `git fetch origin lane-2026-11`, `git log wip..origin/lane-2026-11`, review, merge what passes the checks into wip, a DECISIONS line per merge; steer it by editing production/lane/LANE-QUEUE.md on wip; its results in production/lane/LANE-LOG.md. The PC lane is dropped: C:/Users/Jafar/ledger-lane (95 MB worktree), tools/lane_gate.py and production/lane's PC setup files are unused; remove the worktree through retention.py's map with one DECISIONS line (own leftover).
1. Kiln, one machine job at a time: (a) double precision try 2: the diagnosis (report's section 'why the gate failed') says the change is not the fault: layered's jacket jitters at 25-36 mm/s against the 30 mm/s stillness limit, cuffR is one edge with two states (main's cuffL does the same under a 1 mm nudge), the seen-through point exists in both engines, four 'failures' were better. Step 1, running at the stop in a helper: layered over a fixed jumper and the jacket at +-1 mm (section 'try 2 step 1: confirm runs'); read it first. If it confirms sensitivity: merge lane-double with a re-taken baseline as a recorded decision (or rank 2: a precision switch, off by default); not contact in double precision. (b) the speed lane re-checked on the new engine (advisor 201/193 point 4, Fable allowed), drape time per garment before and after; (c) DONE 17:59: lane-benches merged (Kiln main 911bfdc; main held the same first commit under another hash, so the lane's files were taken whole; unit tests OK); (d) bending try 2 = option (a) (DECISIONS 16:30), on top of double precision; (e) the cantilever matrix re-run on the merged engine to see how many of 12 settle now.
2. Retention step 2: the second review FAILED (N1, N2: production/research/disk/RETENTION-STEP2-REVIEW2-2026-11-17.md); try 3 fixed both (DECISIONS 17 Nov); its 6 should-fix and 3 minor items are still open: fix them with self-tests (never during a Kiln gate), then a THIRD fresh hostile review (final-reviewer, high effort, read-only, both earlier reviews as its list; also measure the plan's time once a test row has an owner, since the scan opens every mapped folder); mapRulesLive on only on its PASS; then write owners into storage-map.json (LEDGER or Claude only where certain).
3. Up to eight helpers on machine-free work: the next order's research and targets (waiting items 5, 6, 7, 9 have none yet); Kiln analysis as results land.
4. n16-8 Tom's crown (full editor: only when no Kiln gate runs); n16-7 look and packaged film; n16-6 Sonnet 5.5 packaged run (never during a Kiln gate). DAILY by 19:00 tomorrow.
5. Waiting by his pick: n16-5 S2 and n16-3's people ladder (git show 47cfaec10:production/handover/HANDOVER.md, item 1). M5 chain for Ron's trousers: refused twice by the app's permission check, not again without a new way.

## Tonight's machine-free queue (start before 01:15)
1. Kiln code (bending try 2, speed lane) and reviews, no drape runs during the night build. 2. The retention fixes and their review. 3. The next order's waiting list (advisor 192).

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 17 Nov: zips gate-r3 stopped before judging (its space check called retention.py mid-edit): not a try. A wait loop matched its own command line (searching process command lines for 'regression_gate' finds the bash running the search): match on python.exe or the exe by name. Two heredoc edits lost backslashes (memory bash-heredoc-backslashes): write such edits with chr(92) or the Edit tool. Registering a Windows scheduled task refused by the app's safety check; superseded by the gate route.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2, 3 and 4 have targets now).
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2; cantilever bench 1 (passed as a bench); double precision 1 of 2 (M1 passed, gate failed); retention step 2: 3 tries (the third under RULINGS 7 Nov, closing the gap; a fourth only if it closes a third of what is left with no new fault); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none today.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help (or with no arguments when its docstring shows required ones); let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
