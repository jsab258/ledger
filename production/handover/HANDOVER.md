# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-18 03:38 (the hourly run; the last session set its Stopped line at 03:14)

**Row due:** 2026-11-18 04:39 (last 03:39; page and advisor read 03:50, nothing new; last ack 216 at 02:55)
**Stopped:** 2026-11-18 03:56 (history near its point at an item's end. Kiln main 0264a9e (R1, B1, J1, P2 merged, tests pass); gap 2 try 1 FAILED; trousers strain-last run clean; licence item v154. Helpers left running, reports land in files named under Running.)
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

## Done this run (03:38 to 03:56; details in DECISIONS 03:41-03:55)
- Page and advisor read 03:39, 03:50: nothing new. Row 03:39.
- Ron's trousers branch ron-kiln-trousers-import now 536ce6307 (wear maps, twill tile 73 at 0.5); unpushed; waits on his licence answer.
- Kiln main 0264a9e: R1, B1, J1 (+ review fixes 7686368), P2 (+ classes plain) merged; drapestudio 62/62, root 5/5, python 69 OK.
- Gap 2 try 1 of 2 FAILED (carry-outside switch): run 1 matched the baseline; with it on the frame-42 wrist edge is unchanged (6.14), body through 112 to 82. Lane not merged.
- Trousers with KILN_STRAIN_LAST=1: body through 0, worst 1.242, checks pass.
- Decompile list (58) and costed replacement plan (about 28 h helper, 5 h machine; trousers first about 10 and 4); licence item corrected (v154), still Not yet.
- Deleted own leftover cargo target lane-strainorder (1.1 GB).

## Running at the stop (reports in F:/LedgerTools/tool-dev/reports; read, review, merge nothing unreviewed)
- Wrist diagnosis after try 1 (diagnoser): KILN-NYLON-WRIST-AFTER-FIX-DIAGNOSIS-2026-11-18.md (diag folder in the carryinside run folder).
- J2 rest label: lane C:/LedgerTools/kiln-lanes/j2-restlabel, KILN-LANE-J2-2026-11-18.md.
- J3 negative controls: lane C:/LedgerTools/kiln-lanes/j3-negative, KILN-LANE-J3-2026-11-18.md.
- Re-source slice on the trousers path (rows 8, 10, 11, 18, 20, 21, 26, 29, 55): lane C:/LedgerTools/kiln-lanes/resource-trousers (from 0264a9e), KILN-LANE-RESOURCE-TROUSERS-2026-11-18.md; must change no gate result (gate alone to prove it).
(A helper still running at a new start belongs to a finished session: read its report when present.)

## Next, in order
0. Verdicts after 2026-11-18T02:50:00Z; advisor after 2026-11-18T02:55:00+01:00 (last ack 216). Row by 04:39 with Kiln's share until Thursday.
1. Read the wrist diagnosis; design gap 2 try 2 from it (last try before a researched different method; armpits' cause still open). The carryinside lane's inside-skin choice (no offset) was flagged as first to question.
2. Public names lane: gate alone on the lane (every switch off, against 9ca019e), merge, then the writer edits in the lanes review (never regenerate the gate's job files).
3. After 04:15's morning pictures: make_baseline.sh at the newest Kiln main (about 1 h, alone), commit regression_baseline.json on Kiln main.
4. A gate with KILN_STRAIN_LAST=1 on every job, alone; if all pass with body through 0, decide making it the default.
5. Review then merge J2, J3, the re-source slice; then the plan's next trousers rows (9 and 13 re-derived, 27 measured) toward clearing Ron's trousers.
6. Small items: outpath fall-open in lane folders (now B1 is merged); the built-in figure's shoulder fault (J1 review); B2 run from main on a quiet machine.
7. On his licence answer: trousers merge, import (never 01:15-04:30), shipped check, nightly_package.py, -WearHeld film. Then 0c daytime talk run; Darren's head remake (advisor 215); bending try 2 (a); n16-6 Sonnet 5.5 packaged run; n16-8, n16-7.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 18 Nov 03:40: gap 2 try 1 (carried points landing inside the body moved to their old triangle's heaviest corner): the wrist edge's jump at frame 42 is unchanged, so inside points are not the whole cause; try 2 waits on the diagnosis.
- 18 Nov 02:45: the strainorder gate stopped at once: `cargo test --release` builds no program; built it and reran. Setup, not a try.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2, 3 and 4 have targets now).
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 18 Nov: Kiln gap 2 (nylon sleeve) 1 of 2; 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2 (try 2 not yet run); cantilever bench 1 (passed as a bench); double precision 2 of 2 (try 2 passed, merged); retention step 2: 3 tries (the third under RULINGS 7 Nov, closing the gap; a fourth only if it closes a third of what is left with no new fault); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help (or with no arguments when its docstring shows required ones); let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
