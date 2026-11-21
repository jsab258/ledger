# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-21 16:22 (the hourly run)

**Row due:** by 16:48 (last row 15:48; page read 16:09, nothing new; filter verdicts after 2026-11-21T15:09 UTC, advisor after 15:28:00 +01:00; ack 294 written 15:45)
**Stopped:** 2026-11-21 16:16 (history 241k of 250k after G5; any next footage item would cross the point mid-item, so stopped at the item boundary)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). Kiln v1's Monday goal withdrawn (advisor 277); the PC measuring block leads. Pace rules: production/week-shape.json and `python tools/pace_line.py`.

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
- **Measuring block in every row (advisor 292, 21 Nov):** PC hours done against planned per block (GTA VI 24.5, car chases 3, players 6, own build 2, port towns 3, conversations 2, district 4, street life 3, feel 82, extra rows 16.5), weekly points per measured hour, expected finish at current pace (estimate marked). Done at 13:46: GTA VI about 3.6, car chases 1.0 (done), players 0.5 (done).
- **Progress page (advisor 275):** each refresh reads the live page and publishes only progress.json and changed files; never an old index.html, never plan.json. Helpers only as project types: settings_check flags catch-all helpers (target under 2%).


## Done today
- 21 Nov 15:39-16:16: advisor 294 (reconcile footage with the old period research) acknowledged and done: RECONCILED tables on the port-town sheet and studies 1, 2, 10; waiting item 38 holds the owners' changes; memory saved. Study 10 reactions: KCD2 two clips, RDR2 one (still bystanders / a knot of 2-4 / Yakuza's ring of 10-12: a design choice). G5 second sample. Page read-back done. All pushed.

## In flight
- Nothing runs; no helpers; heavy lock clear. Browser pane: the GTA VI clip 4Sj3c8sMO-Y with a frame sheet over it (reload clears it).
- Frame sheets: seek, wait for 'seeked' or 1.5 s, draw the stars row (x 1600-1900, y 22-67 of 1080p) at twice size in a fixed div, zoom the screenshot; step 1 s or finer (2 s blink). Check each clip's datePublished (release 19 Nov).

## Next, in order
000. Read the advisor channel first.
00. Allowance first: `python tools/pace_line.py <week> --fable <fable>`; the stop is 95% (week-shape.json hard_stop; the 75% lapsed at his 19 Nov Fable reset, advisor 284), ceiling line+25 capped at 95. Spare allowance before a reset funds planned or waiting work unasked (his rule 21 Nov, advisor 285).
0d. NOW (advisors 285, 286, 289): the PC measuring block: GTA VI's footage pass (lane branch's production/research/lane/gtavi/FOOTAGE-MEASURING.md; no spoiler to him), the footage studies (item 35), item 37, the feel block, then MEASUREMENTS-NEEDED's rows.
0e. Being seen (measurements/gtavi-being-seen-builder-2026-11-21.md, all counts there): S1 done; S3, S7, G4 sampled; G6 closed as footage allows; G5 settled 21 Nov 16:26 on 4Sj3c8sMO-Y by a 1 s frame sheet (one grey 93 s, four grey flashing 50 s, four red heat 50 s, seen: four white, no star added; the earlier 'three white' was a flash misread). Open: whether return adds a star (one sample each way).
0g. Footage first passes DONE: item 35 studies 1, 3, 4; item 37 studies 2 and 10 (sheets in measurements/, each with its RECONCILED table and OPEN list). Advisor 294 rule: every study first reads production/research/ and aaa-reference/studies/ on its subject. NEXT: item 35 study 2 (our prototype filmed by the same method, held against the sheets' figures; tester run, Sonnet frame reading, Opus spot checks) once there is room under the ceiling; then the feel block. Meanwhile, lean: study 10 spread and settling (an uncut MKIceAndFire KCD2 part with a crime in town); study 3 narrowed to Q6 smoking (chest-up 1989-90 vox pops), Q1 at 10 s, Q5 stance; G3 an uncut free-roam car entry and heat's length when it clears unseen.
- Allowance: 86% all session (15:39 to 16:16) against a ceiling of 87.2%; work lean, no helpers. Measuring block: about 6.6 of 146 PC h (estimate).
0. Verdicts and advisor as on the Row due line; row hourly.
0a. Advisor 277: Kiln, hair and the crowd paused until the browser evening holds; Kiln v1's Monday goal withdrawn.
0b. Night walk 21 Nov: 14 of 17; menu fix holds; his command-line sign-in done. Talk stages fix made 21 Nov 08:40 (try 1 of 2: route_walk presses T alone, waits for talk-open, comes round once, then play.py say --open); tonight's walk proves it: read talk-open's detail; the bench and picture check should pass now.
1. Paused with Kiln: Ron's seated hem cover try 2 of 2 (Fable legs lane; the 20 Nov FAIL film its acceptance view); fins try 3 brief READY (tool-dev/reports/BRIEF-KILN-LANE-FINS3-FABLE.md).
4. Marvelous export done 21 Nov (results F:/LedgerTools/md-jobs/export-2026-11-21.json; LOG.md Exports). Marvelous stays open (his word). No Unreal work until the browser prototype is done, then Kiln (advisor 288).
5. History rewrite: HELD for his word at the PC. Progress page daily from the live page (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 21 Nov 15:42: wrote a sheet's window as "15:42-16:05" ahead of the clock again; corrected from Get-Date before commit. Write the end only after reading the clock.
- 21 Nov, the footage block's first passes (studies 1, 3, 4, 2, 10) were viewed before reading our own research (his correction 15:23, advisor 294); reconciled afterwards.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: Marvelous bridge start 1/2 (19 Nov, four copies, his item); layered stage trace (no try); layered fix 2/2 (both failed 19 Nov: pass weighting, interleave; Fable next); trousers seat 2 tries (accepted 17:15); seated hem gap 1/2 (F5-a); coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 passed at try 1 (refit2); layered3 Fable 2/2 (set aside 19 Nov); jumper import 2 (the first failed on a missing budget line); blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

