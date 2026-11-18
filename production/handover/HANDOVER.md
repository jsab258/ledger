# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-18 05:20 (the hourly run; the last session set its Stopped line at 05:11)

**Row due:** 2026-11-18 07:13 (last 06:13; page and advisor read 06:00, nothing new; last ack 216 at 02:55)
**Stopped:** 2026-11-18 06:17 (history past its point at an item's end. Kiln main 278e006, eight pieces merged this run; gap 2 set aside after three routes; resource-rewrite reviewed MERGE WITH FIXES, fixes not applied. No helper running.)
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

## Done this run (05:20 on; details in DECISIONS 05:25 on)
- Page and advisor read 05:21, 05:28, 05:41, 05:50, 06:00: nothing new. Rows 05:22, 06:13.
- Kiln main now 278e006 (cargo 90, Python 107): seampartial (compat's long partial-seam forms refused) and figuresurface (the built-in figure's face pushes) merged after small reviews; before them outpath-closed (the output-path guard refused nothing from lane folders; now fails closed), R3 re-target (review MERGE), C2 import hardening (fixes applied), r3-passfalse (R3's follow-ups), C3 garment as data, C1 spec-to-job check. cargo 88 passed, Python suite OK on main.
- Gap 2 try 2 (of 2) used and FAILED: KILN_BAND_STRETCH (lane bandstretch 300ee5d, not merged) wrapped the cuffs fully; Kiln's own pattern check refused before frame 1 (cuffR rest 172 mm, 219 at the rib's limit, needs 235 where its seams bring it). The half wrap on main hid the shortfall. Girth measured (session scratchpad girth.py): 209-263 mm across the cuff's landing, 193 mm 20 mm nearer the hand.
- Cause found in the writer's own docstring: the nylon draft is at MH_SamC5's measures but drapes on MH_SamS6 (unmeasured, moved up to 56 mm).
- Shoulder probe (KILN-SHOULDER-PROBE): the built-in figure has no surface for face pushes; sample only.

## Running at the stop
- Nothing. resource-rewrite's review came back MERGE WITH FIXES (KILN-LANE-RESOURCE-REWRITE-REVIEW-2026-11-18.md; scratch merge into 278e006: cargo 97 passed; Python 119 with fix 1): three fixes, all from main's seampartial merge: (1) test_compat_public's 11/12-argument test expects NotSupported, (2) MECHANICS.md's partial-seam row conflict, (3) the stale "More calls" CutPatternAlongInternalShapes row; exact text in that report.

## Next, in order
0. Verdicts after 2026-11-18T05:00:00Z; advisor after 2026-11-18T02:55:00+01:00 (last ack 216). Row due 07:13, with Kiln's share. Then item 0b: apply resource-rewrite's three review fixes in its lane (exact text in its review), merge lane-resource-rewrite (it carries resource-public) into main, cargo and Python on main, DECISIONS and NOTEBOOK lines (18 + 14 rows re-sourced).
1. Gap 2 (nylon right wrist) SET ASIDE 06:05 after the S6 fit route (KILN-NYLON-S6-FIT): unchanged winding 0, new 10.2 mm seam gap. Listed; only a removing or simplifying fix under an hour, or a new researched method that closes a third with no new fault. The S6 draft and measures stay on F: for the jacket when it resumes.
2. After resource-rewrite merges: step 6's remaining REWRITE batches (line info and export 31-36 with the work-jacket writer; window 15, 16, 43-46), row 39, row 28 (needs a gate).
3. Run alone, no helper compiling: make_baseline.sh at current Kiln main (about 1 h), commit regression_baseline.json; the gate with every switch off must match it; check rest_label on real lines. Then the cantilever convergence check.
4. Public names lane: gate alone (every switch off, against 9ca019e), merge, then the writer edits.
5. A gate with KILN_STRAIN_LAST=1 on every job, alone; if all pass with body through 0, decide making it the default.
6. Row 27 Z-step sweep (machine) toward clearing Ron's trousers; R4, J4, B2 (drapes after a gate).
7. Listed: rule 4 refuses uncapped rib at the solver's limit while rule 2 does not; the placement log line lost (the front reads the engine's stderr only at exit).
8. On his licence answer: trousers merge (ron-kiln-trousers-import 536ce6307), import (never 01:15-04:30), shipped check, nightly_package.py, -WearHeld film. Then 0c daytime talk run; Darren's head remake (advisor 215); bending try 2 (a); n16-6 Sonnet 5.5 packaged run; n16-8, n16-7.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 18 Nov 05:40: gap 2 try 2 (band started fully wrapped and stretched): refused by Kiln's pattern check, the cuff too short for the forearm where it lands (cut for another body).
- 18 Nov 04:40: causal check, cuffs' closing seams held to the 20 mm stage's end: frames 1-3 identical, so that seam is not the cause (not a try).
- 18 Nov 03:40: gap 2 try 1 (carried inside points to their old triangle's heaviest corner): wrist edge unchanged; inside points were a symptom.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2, 3 and 4 have targets now).
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 18 Nov: Kiln gap 2 (nylon sleeve) 2 of 2 used, both failed; the third route (S6 fit) running; 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2 (try 2 not yet run); cantilever bench 1 (passed as a bench); double precision 2 of 2 (try 2 passed, merged); retention step 2: 3 tries (the third under RULINGS 7 Nov, closing the gap; a fourth only if it closes a third of what is left with no new fault); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help (or with no arguments when its docstring shows required ones); let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
