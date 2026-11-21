# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-21 08:49 (the hourly run)

**Row due:** by 09:57 (last row 08:57; page read 08:52: verdicts none after 2026-11-21T05:22 UTC; advisor none after 08:10 (286 acked); filter advisor after 08:10:00 +01:00, verdicts after 2026-11-21T07:52 UTC)
**Stopped:** 2026-11-21 09:16 (history at its point, 242k of 250k; next: rmhryFPJ0AE from 2:40 for the hostage prompt and any alarm, then the rest of 0e)
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
- 21 Nov 08:49-09:11: GTA VI S1 closed (clerk reacts about 1 s); a threat alone raised no stars, violence did within seconds; the star icons read clothes, face, weapon or car; notebook and recipe map updated; pushed.
- 21 Nov 07:52-08:28: advisors 284-286 closed (field of view setting, spare allowance rule, stop 95%, car chases added); GTA VI free-roam stretch 1 timed and pushed (8fb283c70); night walk read; 20 Nov's done list is in git history.

## In flight
- Nothing runs; heavy lock free. Browser pane: a YouTube tab with an overlay canvas, harmless.

## Next, in order
000. Read the advisor channel first.
00. Allowance first: `python tools/pace_line.py <week> --fable <fable>`; the stop is 95% (week-shape.json hard_stop; the 75% lapsed at his 19 Nov Fable reset, advisor 284), ceiling line+25 capped at 95. Spare allowance before a reset funds planned or waiting work unasked (his rule 21 Nov, advisor 285).
0d. NOW (advisor 285, his '1' 07:44): the PC measuring block started 21 Nov: GTA VI's footage pass first (lane FOOTAGE-MEASURING.md, story missions allowed, no spoiler to him), then the feel block (FEEL-MEASUREMENT-METHOD-2026-11-20.md), then car chases (advisor 286: five each for GTA VI, GTA V, GTA IV, Sleeping Dogs, own sheet, against the Hook and docks, about 3 h; after GTA VI, before the feel block), then MEASUREMENTS-NEEDED's extra rows; the Marvelous export when he answers its box. Rows: game and verb, when each game's numbers land, weekly points per measuring hour (measured).
0e. Being seen (measurements/gtavi-being-seen-builder-2026-11-21.md): S1 done. Next: rmhryFPJ0AE (robbing unseen) for G4; S3 and S7 from the hold-ups' customers; do the icons clear with a mask or new clothes or car (8dTwnFFjspo); then G5-G6, stretches 2-3, driving, advisor 286's car chases. Read by the canvas overlay (the file says how); screenshot twice if a sheet is half drawn.
0. Verdicts and advisor as on the Row due line; row hourly. When he taps Done on licence-rule-2026-11-20, close it and the four licence items with decisions.
0a. Advisor 277: Kiln, hair and the crowd paused until the browser evening holds; Kiln v1's Monday goal withdrawn.
0b. Night walk 21 Nov: 14 of 17; menu fix holds. Diagnosis done (production/audits/night-walk-2026-11-21-diagnosis.md): (1) bench and eyes fail because the command-line Claude Code's sign-in (used by the 01:30 'LEDGER nightly walk' task) expired; HIS HANDS: in a Command Prompt run claude, type /login, finish in the browser, /exit. On his page 08:34 as cli-signin-2026-11-21 (ACTION) and asked in chat as NEEDS YOU; after his Done, confirm with one short claude -p, then close it. (2) Talk stages: the tester types when Sheila is within 3.5 m but out of sight; fix made 21 Nov 08:40 (try 1 of 2): route_walk presses T alone, waits 6 s for talk-open, else walks round to her once and tries again, then types with play.py say --open (no second T); selftests 24/24 and 13/13. Tonight's walk proves it: read talk-open's detail.
1. Paused with Kiln: Ron's seated hem cover try 2 of 2 (Fable legs lane; the 20 Nov FAIL film its acceptance view); fins try 3 brief READY (tool-dev/reports/BRIEF-KILN-LANE-FINS3-FABLE.md).
3. Advisors 252/259: the licence edits only in a session he starts; four licence items open (presentmon, kiln-front-end, font-pick, dinov3).
4. When he taps Done on marvelous-box (deadline Thu 26 Nov, first in next week's order): md_job.py --start (try 2 of 2), one export job over the 52 .zprj (ImportZprj, ExportPatternJSON, ExportFBX beside each), check each reopens, list in production/art/clothing/LOG.md under Exports; copy kiln-md-compare-2026-11-18 into F:/LedgerTools/garments.
5. History rewrite: HELD for his word at the PC. Progress page daily from the live page (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 20 Nov 16:53: Steam's appreviews address is retired (redirects); use IUserReviewsService/GetAppReviews (NOTEBOOK.md).
- 19 Nov 18:12: CLAUDE.md, RULINGS and page-check edits for advisor 252 refused by the unattended run's safety check (do not retry unattended).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: Marvelous bridge start 1/2 (19 Nov, four copies, his item); layered stage trace (no try); layered fix 2/2 (both failed 19 Nov: pass weighting, interleave; Fable next); trousers seat 2 tries (accepted 17:15); seated hem gap 1/2 (F5-a); coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 passed at try 1 (refit2); layered3 Fable 2/2 (set aside 19 Nov); jumper import 2 (the first failed on a missing budget line); blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

