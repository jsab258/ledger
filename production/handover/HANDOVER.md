# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-20 23:07 (the hourly run; the last session set its Stopped line at 22:52)

**Row due:** by 00:09 (last row 23:09; page read 23:08: verdicts none after 2026-11-20T21:52 UTC; advisor 283 closed, ack 23:09; filter advisor after 23:09:00 +01:00, verdicts after 2026-11-20T22:08 UTC)
**Stopped:** 2026-11-20 23:11 (advisor 283 closed; allowance 73% against the 73.4% ceiling, +24.6 over the line, Fable 44%; both open items his hands. No helpers or background jobs; heavy lock free.)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). HIS GOAL THIS WEEK (advisor 220): Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits. Plan: F:/LedgerTools/tool-dev/reports/KILN-V1-CHECKLIST-2026-11-18.md (top of LOOP.md): 0 of 6 lines done. Pace (advisor 246): 47% at 13:37, non-Fable 23.5% against the ceiling 44.8%, hard stop 75%; Fable 51%, burn it on Kiln before his reset. This week (RULINGS): eight helpers a session, Fable at max on Kiln's hardest pieces, high effort on hard code and reviews.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, leading 'v1: N of 6', ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00. Each row: helper count and rate, F:'s free room and the next 12 h's need, what fills each helper place.
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page: read the live page first, diff, then publish index.html with items.json.
- **His hands only when nothing else can (advisors 203, 204, 221):** an ACTION item needs only_you and a one-line tried; since 18 Nov 12:20 an open DECISION item needs "kind", one of CLAUDE.md's categories (money, sign-in, hands, licence-off-list, canon, story, scope, frame-look, person-look, taste, identity); needs_you_page.py refuses both otherwise. His own tools are not licences; deleting what nothing uses, guarded by a check, is not his decision.
- **Every standing ruling names its enforcer (advisor 205)** in production/rulings-enforcers.json the same day.
- **Kiln (RULINGS 13, 14, 18 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone; M7 count in every round report (0). Share: `python tools/token_measures.py --kiln-share`.
- **Fable (advisors 248, 250):** reset pressed 19 Nov; Fable at max for Kiln's hardest pieces, prototype, simulation, any Kiln fault failing two Opus tries (given problem, tries, numbers, no conclusion); his last reset untouched, never called for. final-reviewer and research-synthesis at effort high until 23 Nov 13:00, then medium.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads.
- **The heavy lock** F:/LedgerTools/tool-dev/runs/kiln-heavy.lockdir (mkdir as the lock, owner file inside, released at once) for every cargo/gate/drape run. A Kiln gate whose seconds matter runs alone.
- **Before writing Stopped: end every background job of your own, and check for runs your stopped helpers leave behind:** stopping a helper does NOT stop its bash scripts; at 12:20 four trees (legtorso sweeps, donkey, blouse) were still running and holding the lock. List processes matching kiln-lanes|sweep.py|regression_gate|heavy*.sh and taskkill /T each top bash; then clear the lock.
- **Lane rules:** F:/LedgerTools/tool-dev/LANE-RULES.md; every Kiln brief points to it.
- **Tries (RULINGS 7 Nov) over CLAUDE.md:** after two failed tries one genuinely different researched method; up to four while each closes the gap by a third with no new fault; none asks him. Helpers quote CLAUDE.md's 'third try needs his yes': correct them.
- **Page read-back, daily by the session (19 Nov):** the nightly task is off since 12 Nov; once a day query verdicts with "at" after the last read-back, out_dir production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8, then `python tools/page_answers.py --index` (ci's page-answers-fresh fails after 2 days).
- **Storage and backup (advisors 196-198, 203):** writes and deletes only through retention.py and the storage map; nothing of his. Kiln's LOOP.md and reports folder joined the backup list today.
- **Progress page (advisor 275):** every refresh starts from the live page (Artifact read), takes its index.html as base, publishes only progress.json plus files changed; never republish an old index.html, never touch plan.json or the plan's sections. Helpers only as project types: settings_check flags catch-all helpers (efficiency review 20 Nov, target under 2%).


## Done today
- 23:07-23:11: advisor 283 closed (his words 23:03): GTA VI's story may be studied, no spoiler in anything he reads; RULINGS study line reworded (cap 4,899 held), enforcer note (story-working folders), DECISIONS line, ack and row on the page.
- 22:11-22:17: advisors 281-282 closed (his answers 22:08, 22:10): RULINGS' study line (GTA VI measured first, higher bar wins) and genre line (no mods at release), Monday-audit notes in rulings-enforcers.json, cap held at 4,899; waiting-list item 32 (next week's PC block: Marvelous export, GTA VI ~24.5 h, then the reference games); DECISIONS line; ci 108/108. The design proof's mods part is the lane session's to mark OUT.
- Morning: game menu fix pushed (b6e9687bc); Ron's seated film FAIL; fins tries 1-2 failed. Advisor 271 closed (GTA V, RDR2 reviews).
- 21:57-22:09: advisor 276 closed: story patterns reviewed (PASS WITH FIXES), builder story_patterns.py and head fixed once, pushed on lane-2026-11 (6a475fbda; ranking pooled over 171 coded reviews). Advisor 273 closed: walkthrough study results written, reviewed (PASS WITH FIXES), fixed once, NOTEBOOK lines for both units, pushed wip a30366f8b (ci 108/108). Mafia placeholder stays (protected path); DECISIONS line.
- 18:14-21:55: walkthrough games coded and hand-checked (F:/LedgerTools/steam-reviews/walkthrough/checks.md); story patterns rest on hand counts; advisors 277-279 done.

## In flight
- Nothing runs: all pulls finished (KCD2 3,939 reviews); no helpers; heavy lock free.

## Next, in order
000. Advisors 273, 276, 281, 282 are DONE (both reviewed and fixed once; the studies stand; no further tries owed). Read the advisor channel first: anything new from him comes before the rest.
00. Allowance first: `python tools/pace_line.py <week> --fable <fable>`; 70% at 22:09 against the 72.4% ceiling (hard stop 75%), +22 over the line: only his asks, at most two Sonnet helpers; if nothing of his is open and everything below waits, write the handover and stop rather than idle.
0. Verdicts and advisor as on the Row due line; row hourly. When he taps Done on licence-rule-2026-11-20, close it and the four licence items with decisions.
0a. His rulings tonight (advisor 277): after the Marvelous export, Kiln, hair and the crowd pause until the browser evening holds; Kiln v1's Monday goal withdrawn. Next week: the export, the walkthrough measuring, browser-game work. Steps below that serve Kiln wait unless the order says otherwise.
0b. Tonight's packaged walk proves the tester guard and the menu fix (try 1 of 2; production/audits/night-walk-2026-11-20-diagnosis.md): read its report in the morning.
0c. Fable: one builder at a time, max effort (advisor 266); none before the one-shot's end row (advisor 267).
1. Ron's seated hem cover try 2 of 2 (Fable legs lane), this morning's FAIL film its acceptance view: paused with Kiln unless the order says otherwise.
2. Fins try 3 brief READY (tool-dev/reports/BRIEF-KILN-LANE-FINS3-FABLE.md): paused with Kiln.
3. Advisors 252/259: the licence edits only in a session he starts; four licence items open (presentmon, kiln-front-end, font-pick, dinov3).
4. When he taps Done on marvelous-box (deadline Thu 26 Nov, first in next week's order): md_job.py --start (try 2 of 2), one export job over the 52 .zprj (ImportZprj, ExportPatternJSON, ExportFBX beside each), check each reopens, list in production/art/clothing/LOG.md under Exports; copy kiln-md-compare-2026-11-18 into F:/LedgerTools/garments.
5. History rewrite: HELD for his word at the PC. Progress page daily from the live page (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 20 Nov 16:53: Steam's appreviews address is retired (redirects); use IUserReviewsService/GetAppReviews (NOTEBOOK.md).
- 20 Nov 15:52: advisor 270's RULINGS models-line edit ('Fable: one builder per piece of work, max effort (his, 20 Nov).', trimmed to hold 4,900) refused unattended; do it in a session he starts, then rulingsCheck.
- 19 Nov 18:12: CLAUDE.md, RULINGS and page-check edits for advisor 252 refused by the unattended run's safety check (do not retry unattended).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: Marvelous bridge start 1/2 (19 Nov, four copies, his item); layered stage trace (no try); layered fix 2/2 (both failed 19 Nov: pass weighting, interleave; Fable next); trousers seat 2 tries (accepted 17:15); seated hem gap 1/2 (F5-a); coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 passed at try 1 (refit2); layered3 Fable 2/2 (set aside 19 Nov); jumper import 2 (the first failed on a missing budget line); blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

