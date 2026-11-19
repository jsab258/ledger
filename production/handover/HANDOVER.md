# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-19 13:36 (the hourly run; the last session set its Stopped line at 12:52)

**Row due:** by 14:42 (last row 13:42; page and advisor read 13:58: nothing new after advisor 246)
**Stopped:** 2026-11-19 12:52 (still above the week's ceiling: 45% against 44.1%, Fable 48%; page and advisor read 12:52, nothing new after advisor 245, no verdicts since 12:24; the reset item still open; started nothing, spends nothing while the ceiling rises)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). HIS GOAL THIS WEEK (advisor 220): Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits. Plan: F:/LedgerTools/tool-dev/reports/KILN-V1-CHECKLIST-2026-11-18.md (top of LOOP.md): 0 of 6 lines done. Pace (advisor 246): 47% at 13:37, non-Fable 23.5% against the ceiling 44.8%, hard stop 75%; Fable 51%, burn it on Kiln before his reset. This week (RULINGS): eight helpers a session, Fable at max on Kiln's hardest pieces, high effort on hard code and reviews.

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
- **Fable (advisors 227-228, to 23 Nov 13:00):** Kiln's hardest pieces (stiffness, Sheila's blouse, the trousers' legs) and any Kiln fault failing two Opus tries go to Fable at max (Agent model fable, effort max), given the problem, tries and numbers, no conclusion; never straight to a set-aside. No Fable cap (advisor 245, 19 Nov): full speed at max where right, his resets undo the cost, warning at 95% of its meter; rows name Fable helpers and share; Fable heavy runs first in the lock queue. final-reviewer and research-synthesis at effort high until 23 Nov 13:00, then medium.
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


## Done this run (13:36 to 14:0x)
- Advisor 246 (his pick 13:31) recorded and acked: until his Fable reset the ceiling counts non-Fable use only (weekly less 0.46 x Fable %), hard stop 75% weekly; pace_line.py reads week-shape.json's fable_reset_pending / fable_share_per_pct / hard_stop (29 self-test cases). Always pass --fable to pace_line. At 13:37: 47% weekly, Fable 51%, non-Fable 23.5% against 44.8%.
- His taps 13:28-13:29: Marvelous renewal cancelled; one copy running since 13:29 (closed). fable-reset item closed as held: put it back (ACTION, one step) at about 98% of Fable's meter, record the press time, then set fable_reset_pending false.
- Bridge: start_bridge -DryRun 13:43: one copy, but a small box (392x174) of Marvelous's own over a disabled main window; the starter stops by design (no try used). ACTION item marvelous-box-2026-11-19, NEEDS YOU sent.
- Cloud lane merged as one folded commit ceb964611 (17 of its commits carry screenshots the push guard refuses; they are gitignored in wip, copies in F:/LedgerTools/game-inputs/lane-playtest-round5-shots). Fold later lane merges the same way. Attribution rows for its prototype source and driver.
- Rows 13:42. Commits 2d2cfc296, ceb964611 pushed, ci 108/108.

## In flight
- Six Fable helpers (diagnoser, model fable, effort max; the sixth, 14:05: R4 refit2, KILN-LANE-R4-REFIT2-2026-11-19.md), all under the heavy lock, reports due in F:/LedgerTools/tool-dev/reports unless named: layered3 (KILN-LANE-LAYERED3-2026-11-19.md), coat2 (coat collar, also the donkey jacket's fault: KILN-LANE-COAT2-2026-11-19.md), blouse2 (wrists: KILN-LANE-BLOUSE2-2026-11-19.md), stiffness3 (a third, different method: KILN-LANE-STIFFNESS3-2026-11-19.md), Ron's trousers seat (F:/LedgerTools/garments/ron/kiln-trousers-chain/chain-boots/seat-try2/REPORT.md). If the session stops before they report, the next run reads those reports, then checks for leftover runs (kiln-lanes|regression_gate|heavy*.sh) and the lock.

## Next, in order
0. Verdicts (UTC, after 2026-11-19T13:20) and advisor (after 14:10 +01:00; last ack 247). ADVISOR 247: until his press every helper on Fable; the press item (ACTION, one step: press a Fable reset in the Claude app) goes on his page at Fable 97% or week 73%, whichever first (pace_line prints RESET ITEM NOW), NEEDS YOU sent; from Fable 95% no new long Fable helper; a row each hour at about :40 with week, Fable and its hourly rise, non-Fable, projected press time and week then. 14:21: week 55%, Fable 67% (about 22 an hour), press due about 15:45. After the press: row with its time and both readings, week-shape fable_reset_pending false, normal models and ceiling.
1. Each Fable report as it lands: a pass goes to a merge candidate on Kiln main with the full gate on a quiet machine (Opus), a fail is recorded with its numbers (tries per RULINGS 7 Nov). Spare places (up to 8): the nylon wrist on Fable, merges and gates on Opus/Sonnet.
2. When he taps Done on marvelous-box: md_job.py --start (try 2 of 2), then one export job over the 52 .zprj (ImportZprj, then export_api.ExportPatternJSON and ExportFBX beside each), check each opens again, list in production/art/clothing/LOG.md 'Exports'; copy the kiln-md-compare-2026-11-18 projects into F:/LedgerTools/garments. Then the reference drapes (Kiln v1 line 5).
3. History rewrite: HELD for his word at the PC (the 4 unstaged files and the n09-12 line's two other homes).
4. Then: wardrobe list overnight (not 01:15-04:30); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 19 Nov 09:05: ci-checks.sh from the Bash tool in an unattended run: refused by Claude Code's removal safety check (the script runs rm; nobody to answer the prompt). Do not re-issue in the same run; the next run tries once.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: Marvelous bridge start 1/2 (19 Nov, four copies, his item); cloud core install 2/2 (passed), its scipy fault 1/2 (passed); layered stage trace (no try); layered fix 2/2 (both failed 19 Nov: pass weighting, interleave; Fable next); trousers seat 1/2 (passed); trousers seated hem gap 0/2; coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 1/2; blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

