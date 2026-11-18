# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-18 01:07 (the hourly run; the last session set its Stopped line at 01:02)

**Row due:** 2026-11-18 02:00 (last 01:00; page and advisor read 01:00; last ack 215 at 23:24)
**Stopped:** 2026-11-18 01:02 (history 232k of its 250k point at an item's end, verdict UNDER; stopped early on judgement: every next step needs the machine after the night build and walk (from about 04:30), and the remaining room would only be spent waiting through the stop hook. No helper or background job running.)
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

## Done this run (01:07 to the stop)
- Page and advisor read 01:08 and 01:25: nothing new (no verdicts after 00:00Z; no advisor after ack 215).
- Provot 1995 read from its scan by eye (pages extracted locally; secs. 5-7): one pass (two better), structural and shear springs only, never bending, held ends fixed, 10% (5% flag), no collisions in his tests. Lane strainorder's code read against Provot and Bridson: order, weights, edges all agree; its tests' expectations look right for the new order (no edit). Note appended to STRAIN-LIMIT-SOURCES-2026-11-18.md; DECISIONS 01:10.
- n16-2 gap 1 built: CastDay.OwnWeekWords + TalkHelper's scene gets "Your usual week: ..." for every live talker (Ron can say where he will be tonight). CoreTests 5,255 and TalkTests 132 pass; full ci-checks run before the night build. Still owed: one live talk sample in the packaged game asking "where will you be tonight?" (API, daytime). NOTEBOOK and DECISIONS 01:20.
- Diagnoser helper (Opus, read-only) on the nylon jacket's sleeveR stretch (gap 2): report to F:/LedgerTools/tool-dev/reports/KILN-NYLON-SLEEVE-DIAGNOSIS-2026-11-18.md.

## Done the run before (00:22 to 01:02)
- Page and advisor read 00:24 and 00:50: nothing new (no verdicts after 22:45Z; no advisor after ack 215). The licence item kiln-front-end-licence-2026-11-17 has NO verdict yet (the last handover's "answered yes" was wrong): trousers step I waits.
- Strain-limit lane reviewed, rebased onto a8368f3, cargo test 56/56 (off still bit for bit), gate alone PASS (F:/LedgerTools/tool-dev/runs/kiln-gate-2026-11-18-strainlimit/gate.out; donkey_jacket NOT MADE as in the baseline run). Merged: Kiln main (F:/LedgerTools/tool-dev/kiln) at 1231324. Review finding kept in the merge message: the repair runs after body contact, so keep it off until a garment run with it on shows body-through 0. Worktree and its cargo target (1.3 GB) removed, recorded.
- Hourly rows 00:30 and 01:00 (Fable's own weekly meter 40% then 43%, not used by this session). Study leftovers DECISION on his page 00:57. Reading helper: papers unreadable to it; the builder read Bridson 2002 in full (pdftotext), finding the order fault; DECISIONS 01:0x.
- Earlier run (23:22-00:10): Ron's Kiln work trousers steps A-H (c009b0d87; F:/LedgerTools/garments/ron/kiln-trousers-chain/REPORT.md); Kiln main to a8368f3 (speed path, gate bands work not seconds).

## Next, in order
0. FIRST: verdicts after 2026-11-18T00:00:00Z; advisor after 2026-11-17T23:24:00+01:00 (last ack 215).
1. After the night (from 04:30, quiet machine, after the walk and runner are done): bash C:/LedgerTools/kiln-runs/baseline-2026-11-18/make_baseline.sh (build main 1231324, base and two nudged runs, about 1 h), then commit regression_baseline.json on Kiln main; the old one is copied beside the runs.
2. His licence tap (kiln-front-end-licence-2026-11-17), when answered yes: trousers step I (held row in production/specs/garments.json, import_garments in mh-assemble, garments_shipped_check), then step J (nightly package, -WearHeld film). Never in Unreal 01:15-04:30.
3. Strain limit, per the primary source (Bridson, Fedkiw and Anderson 2002 sec. 4, read 01:05; notes F:/LedgerTools/tool-dev/reports/STRAIN-LIMIT-SOURCES-2026-11-18.md): collisions must come last. Lane strainorder (C:/LedgerTools/kiln-lanes/strainorder, bfe9e1e, written in the night, NOT built or tested): the sweep moved to each substep after the caps, before contact; the frame-end and layer-finish sweeps removed; author list fixed. After the night: CARGO_TARGET_DIR=C:/LedgerTools/cargo-target/lane-strainorder cargo test --release in engines/drapestudio (the on-strip test may need its expectation updated: contact now follows the sweep), gate alone, merge; then one Kiln run with KILN_STRAIN_LAST=1 on Ron's trousers job, body-through and leftover read. Provot 1995 and Wang 2010 still unread.
4. Darren's head remake when the editor is free (advisor 215), outside the night.
5. Bending try 2 option (a) (script C:/LedgerTools/kiln-runs/bending2-2026-11-17/try2-a/bending2.sh), not beside a gate.
6. DONE 00:57: study leftovers DECISION on his page (study-leftovers-delete-2026-11-18); on yes, delete via retention and record each line.
7. n16-6: next is the packaged run with Sonnet 5.5 for core moments (BAKEOFF-SONNET55-2026-11-16.md line 52), daytime. Retention plan (not beside a gate); n16-8 Tom's crown, n16-7.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 17 Nov 23:25: reopening the 16 Nov trousers project refused by Kiln's body standard; the old job refused by the dressing rule (no fly opening). Setup, not tries; route B worked first time.
- 17 Nov 23:55: merged tests failed once on a golden taken before main's hinge; retaken on main, equal. Not a try.
- 17 Nov late: the speed timing's first series refused by the body standard (old body paths). Output-cap hook refused by the app's safety check (his page). Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2, 3 and 4 have targets now).
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2 (try 2 not yet run); cantilever bench 1 (passed as a bench); double precision 2 of 2 (try 2 passed, merged); retention step 2: 3 tries (the third under RULINGS 7 Nov, closing the gap; a fourth only if it closes a third of what is left with no new fault); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help (or with no arguments when its docstring shows required ones); let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
