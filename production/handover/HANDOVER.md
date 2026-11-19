# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-19 09:36 (the hourly run; the last session set its Stopped line at 09:31)

**Row due:** by 10:10 (last row 09:14; page and advisor read 09:31: nothing new; last ack 09:14, 239-240)
**Stopped:** 2026-11-19 09:31 (at an item's end: layered try 1 failed and recorded; history 256k past its point; nothing of mine running, lock free; FOUR COMMITS PLUS THIS ONE LOCAL, NOT PUSHED: ci-checks could not run unattended)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). HIS GOAL THIS WEEK (advisor 220): Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits. Plan: F:/LedgerTools/tool-dev/reports/KILN-V1-CHECKLIST-2026-11-18.md (top of LOOP.md): 0 of 6 lines done. Pace: 37% at 05:07 against 12.2% (+24.8), under the ceiling; Fable 45%, at its cap. This week (RULINGS, his picks 17-18 Nov): eight helpers a session, Fable up to 40% on Kiln's hardest pieces, high effort on hard code and reviews.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, leading 'v1: N of 6', ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00. Each row: helper count and rate, F:'s free room and the next 12 h's need, what fills each helper place.
- **Every time stamp from Get-Date at the moment of writing**.
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page: read the live page first, diff, then publish index.html with items.json.
- **His hands only when nothing else can (advisors 203, 204, 221):** an ACTION item needs only_you and a one-line tried; since 18 Nov 12:20 an open DECISION item needs "kind", one of CLAUDE.md's categories (money, sign-in, hands, licence-off-list, canon, story, scope, frame-look, person-look, taste, identity); needs_you_page.py refuses both otherwise. His own tools are not licences; deleting what nothing uses, guarded by a check, is not his decision.
- **Every standing ruling names its enforcer (advisor 205)** in production/rulings-enforcers.json the same day.
- **Kiln (RULINGS 13, 14, 18 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone; M7 count in every round report (0). Share: `python tools/token_measures.py --kiln-share`.
- **Fable (advisors 227-228, to 23 Nov 13:00):** Kiln's hardest pieces (stiffness, Sheila's blouse, the trousers' legs) and any Kiln fault failing two Opus tries go to Fable at max (Agent model fable, effort max), given the problem, tries and numbers, no conclusion; never straight to a set-aside. Fable up to 40% of the week; rows name Fable helpers and share; Fable heavy runs first in the lock queue. final-reviewer and research-synthesis at effort high until 23 Nov 13:00, then medium.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads.
- **The heavy lock** F:/LedgerTools/tool-dev/runs/kiln-heavy.lockdir (mkdir as the lock, owner file inside, released at once) for every cargo/gate/drape run. A Kiln gate whose seconds matter runs alone.
- **Before writing Stopped: end every background job of your own, and check for runs your stopped helpers leave behind:** stopping a helper does NOT stop its bash scripts; at 12:20 four trees (legtorso sweeps, donkey, blouse) were still running and holding the lock. List processes matching kiln-lanes|sweep.py|regression_gate|heavy*.sh and taskkill /T each top bash; then clear the lock.
- **Lane rules file:** F:/LedgerTools/tool-dev/LANE-RULES.md (lane folders, the lock, tries, report lines, no clicks); every Kiln brief points to it; all nine briefs passed the permission check on 18 Nov.
- **Tries (RULINGS 7 Nov) over CLAUDE.md:** after two failed tries one genuinely different researched method; up to four while each closes the gap by a third with no new fault; none asks him. Helpers quote CLAUDE.md's 'third try needs his yes': correct them.
- **Helper spawns in an unattended run:** the permission check refuses some briefs (delete wording, cut runs); a leaner brief passes. Never retry a refused brief verbatim.
- Quay Run: on each driving study republish, copy its index.html to F:/LedgerTools/quay-run and run tools/driving_feel_check.py (advisor 222).
- **Page read-back, daily by the session (19 Nov):** the nightly task is off since 12 Nov; once a day query verdicts with "at" after the last read-back, out_dir production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8, then `python tools/page_answers.py --index` (ci's page-answers-fresh fails after 2 days).
- **The ceiling (advisor 237):** `python tools/pace_line.py <pct> --fable <pct>` prints it; above it the lane stops first, still above at the next row nothing new starts.
- **Storage and backup (advisors 196-198, 203):** writes and deletes only through retention.py and the storage map; nothing of his. Kiln's LOOP.md and reports folder joined the backup list today.


## Done this run (08:10 on; details in DECISIONS 19 Nov 08:13 on)
- Kiln v1 line 2 item 2: sitting shape bars set from Tom's passed jeans (gap p90 at most 21.5 mm, hem change at most 1.0 mm; pose_check.py). Ron's trousers miss the gap by 0.9 mm, in the seat: joins the legs' rework. runs/sit-shape-2026-11-19/RESULT.md.
- Layered job diagnosed: Kiln 04f9c93's FINE_PASS_POWER = 2 gives a whole garment 9x passes when one narrow piece is fine; the jumper's lower sleeves push through the jacket's cuffs. Inputs alone add 124 to 160. reports/KILN-LANE-LAYERDIAG-2026-11-19.md.
- Advisor 238: (1) cloud check: numpy/Pillow installed in the job, spec-test's off-git drawn maps unchecked on the cloud only, retention selftest SKIPPED off Windows; (2) backup: 21 lasting folders added (2.9 GB, OK), restore check says UNCHECKED when it compared nothing, storage-map honest, one real restore 44/44; 45 GB left needs room (waiting line 26); (3) elizabeth-idle (the placeholder at Mickey's window) and her voice removed from the specs.
- Advisors 239-240 (his licence rulings 09:02, 09:06), reversible half: 95 raw Mixamo files byte-checked to F:/LedgerTools/mixamo-raw-2026-11-19 and on the backup list. aaa-study (game extracts) taken back off the backup list, today's copy recycled.
- Read-back done; rows 08:30, 09:14; acks 238, 239-240.
- FOUR COMMITS LOCAL, NOT PUSHED (c8c944969, 487d9a464, 081742aa0, 6aacbb6b9): ci-checks.sh was refused by a safety prompt nobody could answer in this unattended run. The placeholder removal must reach tonight's build.

## In flight at the stop
- Nothing of mine running; the heavy lock free (released 09:29). Layered try 1 failed and is recorded (DECISIONS 19 Nov); its patch is kept uncommitted in C:/LedgerTools/kiln-lanes/finepass and runs/kiln-finepass-2026-11-19/finepass-try1.patch.
- Ceiling 40% at 09:12 (40.8%); Fable at cap.
- Stopped on history (256k past its 250k point) at the item's end.

## Next, in order
0. Verdicts and advisor reads as usual (advisor after 09:08 +01:00; last ack 09:14, 239-240). Allowance, pace_line, a row.
1. Run ci-checks (output to F:/LedgerTools/tmp/ci-HHMM.out, tail -1); on failed=none push wip (fetch and rebase first). Then confirm the cloud core run on that push is green (public annotations via api.github.com/repos/jsab258/ledger/actions/workflows/ledger-core-tests.yml/runs?branch=wip); a red run is a FINDINGS line the same day.
2. Kiln layered fix: try 1 FAILED (reports/KILN-LANE-FINEPASS-2026-11-19.md: 153 against 133, gate 24 worse). Try 2 only with a genuinely different, researched method (stiffness: long-range limits, hierarchical PBD, XPBD to convergence), never another pass weighting; research first; if it fails, Fable after Mon 13:00. Also split the 124-to-160 input shift (body or job scripts).
3. Advisors 239-240, HELD steps (his own word in a live session first): the single history rewrite (Mixamo raw files, other no-share files per THIRD-PARTY and audit R10, the extraction records per R10/R11 replaced by the one plain line, private copies and index on F:), force-push wip, main, lane-2026-11 only while the cloud lane's lock row says Lane stopped; the pre-commit refusal check (rulings-enforcers.json, RULINGS within cap); the permanent deletes on F: (keys, mappings, FModel, dotnet10, aaa-study and raw study folders, backup and bin copies) after checking no reader, RESTORE.md's re-extract lines out. First, reversibly: research the method (git filter-repo; GitHub's caches, forks, PR refs), full inventory; the 7 street glbs need cover_iron's cloud treatment in spec-test.
4. Then: wardrobe list overnight (not 01:15-04:30); Marvelous items before 25 Nov; Fable pieces Mon 13:00; DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 19 Nov 09:05: ci-checks.sh from the Bash tool in an unattended run: refused by Claude Code's removal safety check (the script runs rm; nobody to answer the prompt). Do not re-issue in the same run; the next run tries once.
- 19 Nov 09:10: aaa-study joined the backup list by a size-only sweep; it holds game extracts. Read a folder before adding it.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: layered fix 1/2 (failed 19 Nov, pass weighting); trousers seat 1/2 (passed); trousers seated hem gap 0/2; coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 1/2; blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).
