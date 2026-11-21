# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-21 21:41 (the hourly run)

**Row due:** by 23:46 (last row 22:46; page read 22:50: nothing new; filter verdicts after 2026-11-21T20:28 UTC, advisor after 22:30:00 +01:00; last ack 302 at 22:45)
**Uncommitted:** none.
**Stopped:** 2026-11-21 22:56 (the 21:41 run: advisors 297-302 done, all eleven sheets reconciled, the block repriced with depth; stopped lean at 91% against ceiling 93%, next run near)
(At each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

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
- **Page read-back, daily (19 Nov):** query verdicts with "at" after the last read-back, out_dir production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8, then `python tools/page_answers.py --index` (ci fails after 2 days).
- **Storage and backup (advisors 196-198, 203):** writes and deletes only through retention.py and the storage map; nothing of his.
- **Measuring block in every row (advisors 292, 295):** read from measurements/STATUS.md (per aspect and game: planned, logged, state, open question); weekly points per measured hour, expected finish (estimate marked). Mafia is never a reference.
- **Progress page (advisor 275):** each refresh reads the live page and publishes only progress.json and changed files; never an old index.html, never plan.json. Helpers only as project types: settings_check flags catch-all helpers (target under 2%).


## Done today
- 21 Nov 21:41-22:55: advisors 297-302 done and acknowledged: research_rules_check in ci (all eleven sheets reconciled, owed list empty); the prototype-play item off his page and the order (page check refuses such asks until production/lane/one-shot/REPORT-*.md exists); live voices and six preparation items in RULINGS (at its 4,900 cap); voice items 39-40 on the waiting list; STATUS.md: solid rule, none solid today, about 141 h (134 to go, near 11 Dec), one-stream leads. Space check 22:56: GO (C 45 GB, F 30 GB).
- Corrected lane feel sheets wait in F:/LedgerTools/tmp/lane-feel-mafia-out for that branch's session (do not retry the commit).

## In flight
- Nothing runs; no helpers; heavy lock clear. Browser pane closed.
- Finding clips: WebSearch with allowed_domains youtube.com, then fetch('/watch?v=ID') from a youtube tab and read title, datePublished, duration for several ids at once.
- Frame sheets: seek, wait until not seeking and readyState 2 (up to 8 s), draw into a fixed div, zoom the screenshot (viewport 1024 shown at 800: a 480 px canvas reads at 375); step 1 s or finer for blinking HUD. Check each clip's datePublished (release 19 Nov). YouTube search pages draw nothing while the pane is hidden; watch pages work: find ids by WebSearch.

## Next, in order
000. Read the advisor channel first.
00. Allowance first: `python tools/pace_line.py <week> --fable <fable>`; the stop is 95% (week-shape.json hard_stop; the 75% lapsed at his 19 Nov Fable reset, advisor 284), ceiling line+25 capped at 95. Spare allowance before a reset funds planned or waiting work unasked (his rule 21 Nov, advisor 285).
0d. NOW (advisors 285, 286, 289): the PC measuring block: GTA VI's footage pass (lane branch's production/research/lane/gtavi/FOOTAGE-MEASURING.md; no spoiler to him), the footage studies (item 35), item 37, the feel block, then MEASUREMENTS-NEEDED's rows.
0e. Being seen: counts and open rows in its sheet; G5 return-adds-a-star unsettled (one sample each way).
0g. DEPTH FIRST (advisor 302): only numbers solid by STATUS.md's rule count for the design gate; each piece now aims at five uncut, dated samples, and the cheaper route comes first: check the one-stream leads in STATUS.md (dates, cuts, spoilers) and use one uncut stream for several rows at once; Monday's frame-reading trial before more hours. Footage first passes DONE: item 35 studies 1, 3, 4; item 37 studies 2 and 10 (sheets in measurements/, each with its RECONCILED table and OPEN list). Advisor 294 rule: every study first reads production/research/ and aaa-reference/studies/ on its subject. NEXT (advisor 296): each run takes the next footage piece that fits the room, smallest first: G7's continuous post-release night walk (partly confirmed 21:35; eiSklleD708, 909Gxmye7n8, vRRqGNTIwtI are pre-release; a brightness scan finds night stretches in long reels cheaply), G5 whether return adds a star (one sample each way), port-town Q6 from the ITV Calendar 1990 playlist (ids need the pane shown), G8 repeated lines (captions only: the session hears nothing), the split hour's second stretch; item 35 study 2 (our prototype filmed) once a run has room, after the Monday reset if need be. Also: study 10 spread and settling (an uncut KCD2 part with a crime in town); study 3 Q1 at 10 s, Q5 stance; G3 a free-roam car entry and heat's length.
- Allowance: 91% at 22:46 against a ceiling of 93%; spend since 21:41 US$9.54; one Sonnet extractor (finished). Log every step (timelog.py).
0. Verdicts and advisor as on the Row due line; row hourly.
0a. Advisor 277: Kiln, hair and the crowd paused until the browser evening holds; Kiln v1's Monday goal withdrawn.
0b. Night walk 21 Nov: 14 of 17. Talk stages fix (try 1 of 2, 21 Nov 08:40: route_walk presses T alone, waits for talk-open, comes round once, then play.py say --open); tonight's walk proves it: read talk-open's detail.
1. Paused with Kiln: Ron's seated hem cover try 2 of 2 (Fable legs lane; the 20 Nov FAIL film its acceptance view); fins try 3 brief READY (tool-dev/reports/BRIEF-KILN-LANE-FINS3-FABLE.md).
4. Marvelous export done 21 Nov (results F:/LedgerTools/md-jobs/export-2026-11-21.json; LOG.md Exports). Marvelous stays open (his word). No Unreal work until the browser prototype is done, then Kiln (advisor 288).
5. History rewrite: HELD for his word at the PC. Progress page daily from the live page (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 21 Nov 16:25: a pixel count read HUD icons as stars; 2 s steps alias the blink. 20:27: YouTube search blank in a hidden pane.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: Marvelous bridge start 1/2 (19 Nov, four copies, his item); layered stage trace (no try); layered fix 2/2 (both failed 19 Nov: pass weighting, interleave; Fable next); trousers seat 2 tries (accepted 17:15); seated hem gap 1/2 (F5-a); coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 passed at try 1 (refit2); layered3 Fable 2/2 (set aside 19 Nov); jumper import 2 (the first failed on a missing budget line); blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

