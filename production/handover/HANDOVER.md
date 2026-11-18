# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-18 02:37 (the hourly run; the last session set its Stopped line at 02:23)

**Row due:** 2026-11-18 03:43 (last 02:43; page and advisor read 03:11, nothing new; last ack 216 at 02:55)
**Stopped:** 2026-11-18 03:14 (history over its point at an item's end. Strainorder merged (Kiln main a48e139); licence item corrected (v153). Helpers left running, reports land in files named under 'Helpers running': trousers wear pass, R1, J1, gap 2 fix lane (Fable). No gate or drape running. Row due 03:43.)
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

## Done this run (02:37 to 03:14; details in DECISIONS 02:47-03:14)
- Page and advisor read 02:38, 02:53, 03:11; advisor 216 acknowledged 02:55. Row 02:43.
- Night walk of wip 4438999c: 17 of 17; known faults only; its "label on the wrong man" is Tom himself (tester misreading).
- Kiln: strainorder gated alone (PASS) and merged (main a48e139). Gap 2 traced to the mesh rebuild (reports KILN-NYLON-SLEEVE- and KILN-NYLON-REBUILD-DIAGNOSIS-2026-11-18.md). Machine-free list (16 tasks), product targets in LOOP.md, names check, B1 and public-names lanes done.
- Ron's trousers step I on local branch ron-kiln-trousers-import (ad2dc6cb6, unpushed); maps to get a wear pass.
- His licence item corrected (v153): Kiln's engine holds decompile-derived values; recommendation now Not yet.

## Helpers running at the stop (their reports land in files; read them, merge nothing unreviewed)
- Wear pass on Ron's trousers maps: F:/LedgerTools/garments/ron/kiln-trousers-chain/wear/WEAR-2026-11-18.md (gives the garments.json maps lines for the branch).
- R1 (Seamshift reads Kiln's OBJ groups): lane C:/LedgerTools/kiln-lanes/r1-objgroups, report KILN-LANE-R1-2026-11-18.md.
- Public names DONE: b2a8d92 on lane-publicnames (50/50 Python tests; replace rules keep gate results identical; 11 names found public on developer.clo3d.com and kept). Writer edits listed in KILN-LANE-PUBLICNAMES-2026-11-18.md (zip_jacket.py SEW lines 70-71, pleated_skirt.py 439, job_reexport.py line 10), not made; merge with them, gate alone.
- J1 crossing check: lane C:/LedgerTools/kiln-lanes/j1-crossing, report KILN-LANE-J1-2026-11-18.md.
- Gap 2 fix lane (Fable): debug carry dump + KILN_CARRY_OUTSIDE switch, lane C:/LedgerTools/kiln-lanes/carryinside, report KILN-LANE-CARRYINSIDE-2026-11-18.md with the two runs' commands (run them alone; the second is try 1 of 2).
- B1 wardrobe runner DONE: b0e1f44 on lane-b1-wardrobe (16/16 fake tests; report KILN-LANE-B1-2026-11-18.md with the B2 command, run from main after merge; timelog 1.3 h against B1 not yet entered). Its note: the outpath check falls open in lane folders (small fix worth its own task).
(All reports in F:/LedgerTools/tool-dev/reports unless named. If a helper is still running when the next session starts, it belongs to a finished session: read its report file when present; else re-brief from the list.)

## Next, in order
0a. Licence item corrected 03:14 (v153). Next: list every decompile-derived value in engines/drapestudio/MECHANICS.md and plan its public-source or measured replacement, costed, as Kiln's first machine-free task; trousers step I waits on his answer.
0. FIRST: verdicts after 2026-11-18T02:11:00Z; advisor after 2026-11-18T01:50:00+01:00 (last ack 216 at 02:55). Next row by 03:43, with Kiln's share (`python tools/token_measures.py --kiln-share`) until Thursday.
1. DONE 03:14: strainorder gate alone PASS (against 9ca019e); merged: Kiln main now a48e139; worktree removed; its cargo target (979 MB, C:/LedgerTools/cargo-target/lane-strainorder) still to delete through retention and record. Next: one Kiln run of Ron's trousers job with KILN_STRAIN_LAST=1 (body-through and leftover read), alone.
2. After 04:15's morning pictures finish: update make_baseline.sh to main a48e139 (or later merges) and run it (about 1 h, alone), then commit regression_baseline.json on Kiln main.
3. Kiln gap 2: rebuild diagnosis DONE (KILN-NYLON-REBUILD-DIAGNOSIS-2026-11-18.md, high confidence): at the 20-to-10 mm rebuild, new points carried over on old 20 mm triangles start up to 17 mm inside the forearm (8 right, 10 left); the first frame pushes each to its nearest skin, so long edges straddle the arm and lock. Seam pairing ruled out. Next: the cheap debug dump of carried positions after the last rebuild (confirms), then fix try 1 of 2 at sim.rs:1088-1092: a carried point landing inside the body takes its old triangle's heaviest corner (outside at the frame before); predicted sleeveR about 3.5 at frame 42, wrists under 3. General (jeans also jump 1.32 to 1.94). Armpits' cause still open. Gate alone.
4. Wear pass result into the trousers branch (maps lines), shipped check's flat-map line clear. On his licence yes: merge the branch, import (never 01:15-04:30), shipped check, nightly_package.py, -WearHeld film. Row: time from his tap to Ron in the game.
5. Helper lanes R1, publicnames, B1: review each, cargo test, merge one at a time (publicnames needs the job writers changed in the same step; results must stay identical, gate alone). Then the list's next tasks (J1, J2, R2...) into free places; C4 waits on a GarmentCode licence tap.
6. 0c: a daytime packaged talk run asking Ron "where will you be tonight?" (API within the day's ceiling); watch Darren's first-sound time.
7. Darren's head remake (advisor 215), outside the night. Bending try 2 (a), not beside a gate. n16-6 Sonnet 5.5 packaged run; n16-8, n16-7.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 18 Nov 02:45: the strainorder gate stopped at once: `cargo test --release` builds no program; built it and reran. Setup, not a try.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2, 3 and 4 have targets now).
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2 (try 2 not yet run); cantilever bench 1 (passed as a bench); double precision 2 of 2 (try 2 passed, merged); retention step 2: 3 tries (the third under RULINGS 7 Nov, closing the gap; a fourth only if it closes a third of what is left with no new fault); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help (or with no arguments when its docstring shows required ones); let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
