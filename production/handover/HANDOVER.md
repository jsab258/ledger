# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-18 04:22 (the hourly run; the last session set its Stopped line at 03:56)

**Row due:** 2026-11-18 05:25 (last 04:25; page and advisor read 05:11, nothing new; last ack 216 at 02:55)
**Stopped:** 2026-11-18 05:11 (history past its point at an item's end. Kiln main 8aca68f (resource-trousers, J3, J2, R2, resource-solver merged, tests pass); gap 2: where the tangle is born found, try 2 not yet run (redesign in Next 1); R3 and C2 back, to review/fix. No helper running.)
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

## Done this run (04:22 to 05:00; details in DECISIONS 04:28-04:59)
- Page and advisor read 04:24, 04:44: nothing new. Row 04:25.
- Kiln main now 8aca68f: resource-trousers (rows 8, 10, 11, 18, 20, 21, 26, 29, 55; the public quotes checked word for word in the raw page), J3 (+ the review's two gate fixes, 962cc04), J2 rest label, R2 seamshift carry, resource-solver (rows 9, 13, bit for bit).
- Gap 2 found where the wrist tangle is born: frame 0 every sleeve ring winds once round the forearm; frame 1 the lowest 30 mm lies beside it (first frame's sewing). Holding the cuffs' own closing seams late changed nothing (refuted). My "41 mm off-centre" was a reader's error (mean of a half ring); circle fit: cuff 7 mm off, radius 59, wrapped about 190 degrees. Real fault: band and tube end wrapped only half round; the cuff (191.6 mm) looks narrower than the limb where it lands (about 219 mm, unverified).
- Lane limbcentre (9c4b1a1 on b095276, KILN_LIMB_CENTRE, off bit for bit; exe C:/LedgerTools/cargo-target/lane-limbcentre/release/drape-studio.exe) built but NOT draped and NOT counted as a try: its premise failed on the circle fit; expected shift about 7 mm only.
- Untangling research note (production/research): thin, sources unreached.

## Running at the stop (reports in F:/LedgerTools/tool-dev/reports; read, review, merge nothing unreviewed)
- R3 (lane r3-retarget 3129b0d): built, four cases pass, KILN-LANE-R3-2026-11-18.md; needs a fresh reviewer.
- C2 pattern import (lane c2-patimport 6cb883d): review MERGE WITH FIXES (KILN-LANE-C2-REVIEW-2026-11-18.md): DXF pieces in separate blocks at the origin must not be compared (key by block name, plus its test); cargo on the merged tree owed (C: was under its floor). Seam allowance decided: FreeSewing SVGs exported without it.
(A helper still running at a new start belongs to a finished session: read its report when present.)

## Next, in order
0. Verdicts after 2026-11-18T04:11:00Z; advisor after 2026-11-18T02:55:00+01:00 (last ack 216). Row due 05:25, with Kiln's share.
1. Gap 2 try 2 (of 2), redesigned: first measure the limb's girth where the right cuff lands (body section at the cuff's placement rows, as KILN-LANE-LIMBCENTRE measures) against the cuff's cut width 191.6 mm. If the band is narrower than its limb plus gap: try 2 = a band narrower than its limb starts stretched fully round it (as a rib cuff is worn), the tube end following it, general, behind a switch, no special cases; drape alone, read winding and the frame-42 wrist. If not narrower: find why the wrap stops at about 190 degrees (rewrap_end's arc-length rule, ARM_WRAP) and make that try 2. A third try needs his yes (research note thin: reach Baraff 2003, Volino 2006 first).
2. Run alone, no helper compiling: make_baseline.sh at Kiln main 8aca68f (about 1 h), commit regression_baseline.json on Kiln main; the gate with every switch off must match it (resource-solver step 2; also check rest_label on real lines, J2's shortfall: most may read jammed). Then the cantilever convergence check (resource-solver plan step 2).
3. Public names lane: gate alone (every switch off, against 9ca019e), merge, then the writer edits.
4. A gate with KILN_STRAIN_LAST=1 on every job, alone; if all pass with body through 0, decide making it the default.
5. Review then merge R3 and C2; then the re-source plan's step 3-4 (rows 26, 29 wording done in resource-trousers; row 27 Z-step sweep, machine) toward clearing Ron's trousers; remaining machine-free tasks C3 (FreeSewing as data), R4, J4, B2, P1.
6. Small items: outpath fall-open in lane folders; the built-in figure's shoulder face 2 mm inside (J1 and R3 found it); R2's narrow notes.
7. On his licence answer: trousers merge (ron-kiln-trousers-import 536ce6307), import (never 01:15-04:30), shipped check, nightly_package.py, -WearHeld film. Then 0c daytime talk run; Darren's head remake (advisor 215); bending try 2 (a); n16-6 Sonnet 5.5 packaged run; n16-8, n16-7.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 18 Nov 04:40: causal check, cuffs' closing seams held to the 20 mm stage's end: frames 1-3 identical, so that seam is not the cause (not a try).
- 18 Nov 03:40: gap 2 try 1 (carried inside points to their old triangle's heaviest corner): wrist edge unchanged; inside points were a symptom.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2, 3 and 4 have targets now).
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 18 Nov: Kiln gap 2 (nylon sleeve) 1 of 2 (try 2 not yet run; limbcentre not counted); 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2 (try 2 not yet run); cantilever bench 1 (passed as a bench); double precision 2 of 2 (try 2 passed, merged); retention step 2: 3 tries (the third under RULINGS 7 Nov, closing the gap; a fourth only if it closes a third of what is left with no new fault); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help (or with no arguments when its docstring shows required ones); let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
