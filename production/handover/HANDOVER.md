# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-21 10:02 (the hourly run)

**Row due:** by 11:43 (last row 10:43; page read 10:33: verdicts none after 2026-11-21T09:20 UTC; advisor 288 and the 10:10 model watchdog acked; filter advisor after 10:10:00 +01:00, verdicts after 2026-11-21T09:33 UTC)
**Stopped:** 2026-11-21 10:43 (history past its point, 347k; allowance 83% at the 83.1% ceiling; next: 0e, a clip with a haircut or mask change in one shot for the face icon)
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
- 21 Nov 10:02-10:45: his sign-in checked and closed; marvelous-box Done acted on: the 52-project export (above); his page now has nothing open; progress page refreshed on the live base with 21 Nov pictures; advisor 288 into RULINGS; GTA VI being seen: kc_QthzX9So's pawn shop (resist, report 19 s with gunfire), corner shop (comply 1 s; subdued, no report), electronics shop (report about 25 s); G6 two clean samples (4x1Z8hOWn_0, 7QJWRNYq8qc).
- 21 Nov 09:22-09:53: GTA VI being seen (unseen robbery to its end; witnesses inside, kc_QthzX9So); advisor 287 into RULINGS; advisor 259 applied (licences never his: CLAUDE.md, RULINGS, page check); pushed.

## In flight
- Nothing runs; heavy lock free. Browser pane: a YouTube tab with an overlay canvas, harmless.

## Next, in order
000. Read the advisor channel first.
00. Allowance first: `python tools/pace_line.py <week> --fable <fable>`; the stop is 95% (week-shape.json hard_stop; the 75% lapsed at his 19 Nov Fable reset, advisor 284), ceiling line+25 capped at 95. Spare allowance before a reset funds planned or waiting work unasked (his rule 21 Nov, advisor 285).
0d. NOW (advisor 285, his '1' 07:44): the PC measuring block started 21 Nov: GTA VI's footage pass first (lane FOOTAGE-MEASURING.md, story missions allowed, no spoiler to him), then the feel block (FEEL-MEASUREMENT-METHOD-2026-11-20.md), then car chases (advisor 286: five each for GTA VI, GTA V, GTA IV, Sleeping Dogs, own sheet, against the Hook and docks, about 3 h; after GTA VI, before the feel block), then MEASUREMENTS-NEEDED's extra rows; the Marvelous export when he answers its box. Rows: game and verb, when each game's numbers land, weekly points per measuring hour (measured).
0e. Being seen (measurements/gtavi-being-seen-builder-2026-11-21.md): S1 done; S3 comply 2 (about 1 s hands up; at most 3 s cowering), resist 1 (return fire about 2 s); S7 4 with free witnesses (32, 42, 19, about 25 s; gunfire starts at two stars); G4 unseen side 2 (all witnesses subdued, no report in 4 and 2 min); kc_QthzX9So is spent. G6: two clean samples (a bought top clears "outfit known" at once; a respray clears "vehicle known" within 0.5 s; stars unchanged), the icons named by the game's own legend (7QJWRNYq8qc 0:45); the face icon not yet seen clearing. Grw0hsFkE-s read (masked gas-station heist, no stars to the getaway; logo hides the icons; threat cut). Next: a clip showing a haircut or mask change in one shot for the face icon (ttv_wv52nVk is a cut short, a claim only), then G5, stretches 2-3, driving, advisor 286's car chases. Sheets: ytd-app visible while drawing, hidden before the screenshot; icon strip the top-right 160x70 px scaled up.
0. Verdicts and advisor as on the Row due line; row hourly.
0a. Advisor 277: Kiln, hair and the crowd paused until the browser evening holds; Kiln v1's Monday goal withdrawn.
0b. Night walk 21 Nov: 14 of 17; menu fix holds. His command-line sign-in done 09:46, checked 10:08 and closed (advisor 288). Talk stages: fix made 21 Nov 08:40 (try 1 of 2; route_walk presses T alone, waits for talk-open, comes round once, then play.py say --open); tonight's walk proves it: read talk-open's detail, and the bench and picture check should pass now.
1. Paused with Kiln: Ron's seated hem cover try 2 of 2 (Fable legs lane; the 20 Nov FAIL film its acceptance view); fins try 3 brief READY (tool-dev/reports/BRIEF-KILN-LANE-FINS3-FABLE.md).
4. Marvelous export DONE 21 Nov 10:15 (bridge start try 2 of 2 worked): all 52 .zprj reopened, pattern JSON and garment FBX beside each (tools/md-bridge/export_all.py; results F:/LedgerTools/md-jobs/export-2026-11-21.json; LOG.md Exports); compare runs copied to F:/LedgerTools/garments. Marvelous stays open (his word). Advisor 288: no Unreal work until the browser prototype is done, then Kiln (RULINGS 20 Nov line).
5. History rewrite: HELD for his word at the PC. Progress page daily from the live page (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: Marvelous bridge start 1/2 (19 Nov, four copies, his item); layered stage trace (no try); layered fix 2/2 (both failed 19 Nov: pass weighting, interleave; Fable next); trousers seat 2 tries (accepted 17:15); seated hem gap 1/2 (F5-a); coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 passed at try 1 (refit2); layered3 Fable 2/2 (set aside 19 Nov); jumper import 2 (the first failed on a missing budget line); blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

