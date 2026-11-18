# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-18 08:36 (the hourly run; the last session set its Stopped line at 08:23)

**Row due:** 2026-11-18 08:15 (last 07:15; page and advisor read 07:13, nothing new; last ack 216 at 02:55)
**Stopped:** 2026-11-18 08:23 (history past its point at an item's end. Kiln main 424695a: every re-sourcing batch, row 28 and the new baseline in; advisor 217 and 218 acked, their steps first below. No helper or job running.)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). The doubled line, full pace: 65% at 04:25 against 78%, 13 behind. His 17 Nov 22:12 direction (advisor 213): Kiln's share aims at 60% of spend from this morning (25.5% at 04:25). This week (RULINGS, his picks 17 Nov): eight helpers a session, a machine-free lane session, Fable up to 20% for the hardest code (3.3% today), high effort on hard code and reviews. week-shape.json's reset_at stays null until HE presses the spare reset.

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

## Done this run (06:22 on; details in DECISIONS 06:29 on)
- Page and advisor read 06:24 to 08:09 every 15 min; advisor 217 and 218 at 08:09 (acked). Rows 06:32, 07:15, 08:09. wip pushed 5d91f1a87 (ci 105/105).
- Kiln main now f8b8f6e (cargo 116, Python 133). Merged this run, each after its review: resource-public + resource-rewrite (rows 2-58 batches PUBLIC/DROP and "script calls"; the review's three fixes), stderrlog (the front drains the engine's stderr as it is written; KILN_ENGINE_LOG; bad bytes replaced), resource-window (rows 15, 16, 43-46; keys.rs), resource-lineinfo (rows 31-36; ExportPatternJSON returns False, kiln_api.export_pieces; both review fixes), resource-thread (row 39: one 0.5 mm drawing default). The work-jacket writer, ledger-local tools/md/make_jacket_job.py, now calls kiln_api.export_pieces on Kiln (its Kiln copy re-hashed; stream 290 calls, 35 add_seam, sha256 6c90aa10).
- Waiting item 14 (talk, usual day) was already built at 01:20 (4438999c0); a helper moved it into CastDay.TalkLines with eight tests (d2b997f18 on wip, all eight suites pass). Order ledger: mark item 14 done with that evidence.
- Row 39's research-reader brief was refused by the permission check (06:31): the thread value stays unverified (drawing only).

## Running at the stop
- Nothing running. Baseline re-taken 08:23 on c52c3ab (Kiln 424695a; runs F:/LedgerTools/tool-dev/runs/kiln-baseline-2026-11-18-c52c3ab). Row 28 (resource-position) merged 07:20 into Kiln main c52c3ab after its gate (j3, jacket, jeans, layered identical to the 02:52 gate; cargo 118, Python 136). Kiln main is now free of every REWRITE, PUBLIC and DROP row the plan listed except row 27.

## Next, in order
0. Verdicts after 2026-11-18T07:05:00Z; advisor after 2026-11-18T08:20:00+01:00 (last ack 218, both 217 and 218 acked 08:09). Row due 09:09.
0a. Advisor 218 (his 08:05 yes to all ten blind-spots points; exact wording in advisor doc 2026-11-18-0820-218): today, within RULINGS' cap (condense), each with its rulings-enforcers.json entry: the monthly cold skill re-run (replaces 13 Oct "no recipe tests"); no Kiln props/vehicles/buildings modules before its three proofs; the fight lab test's place in PLAN.md; six public-footage frames kept for one blind line-up; the Kiln share line notes the week's order may set another (70% this week).
0b. token_measures.py --kiln-share: count by order item (n16-1 and Kiln's items) against the week's share, not task names against 15%; corrected share from Monday in the next row.
0c. Advisor 217.3: the public-docs line on the licence item before his tap; tap-to-game time in a row; re-source row 27.
0d. After Kiln (218): P4 talk run in a night walk before the corner is copied; hair fallback choice only if this week's verdict fails; merge the cloud lane's paper parts.
1. Row 28 merged without a second reader (the gate was the plan's check): a small review of c52c3ab's row-28 diff when a place is free; old probe jobs that set the style first now place differently (listed in its report).
2. Step 6 left: row 27 (Z-step sweep, machine). The 58-value list then has no decompiled row left but 27 and any the plan marks PHYSICS; check the plan's group totals.
3. Baseline done (424695a). Still owed: check rest_label on real lines; then the cantilever convergence check.
4. Public names lane: gate alone (every switch off), merge, then the writer edits.
5. A gate with KILN_STRAIN_LAST=1 on every job, alone; if all pass with body through 0, decide making it the default.
6. R4, J4, B2 (drapes after a gate).
7. Gap 2 (nylon right wrist) SET ASIDE 06:05 after three routes; only a removing fix under an hour or a new researched method closing a third. Listed: rule 4 refuses uncapped rib at the solver's limit while rule 2 does not.
8. On his licence answer: trousers merge (ron-kiln-trousers-import 536ce6307), import (never 01:15-04:30), shipped check, nightly_package.py, -WearHeld film. Then 0c daytime talk run; Darren's head remake (advisor 215); bending try 2 (a); n16-6 Sonnet 5.5 packaged run; n16-8, n16-7.
- C: sits near its 40 GB floor (40.7 at 06:55): reuse C:/LedgerTools/cargo-target/lane-resource-lineinfo for builds; the merged lanes' worktrees and build folders (resource-public, resource-rewrite, lineinfo, window, thread, stderrlog, position after merge) are my own leftovers to delete through the map, one DECISIONS line.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 18 Nov: Kiln gap 2 (nylon right wrist): two tries and the S6 fit route failed; the cuff is too short for the forearm it lands on (details in TRIED-ARCHIVE.md, 18 Nov).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2, 3 and 4 have targets now).
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 18 Nov: Kiln gap 2 (nylon sleeve) 2 of 2 used, both failed; the third route (S6 fit) running; 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2 (try 2 not yet run); cantilever bench 1 (passed as a bench); double precision 2 of 2 (try 2 passed, merged); retention step 2: 3 tries (the third under RULINGS 7 Nov, closing the gap; a fourth only if it closes a third of what is left with no new fault); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help (or with no arguments when its docstring shows required ones); let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
