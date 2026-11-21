# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-21 14:22 (the hourly run)

**Row due:** by 15:26 (last row 14:26; page read 14:24: no verdicts after 2026-11-21T12:57 UTC, no advisor after 14:00 +01:00; filter verdicts after 2026-11-21T13:24 UTC, advisor after 14:00:00 +01:00)
**Stopped:** 2026-11-21 14:03 (history past its point, 322k of 250k, stopped at the end of study 4's first look; allowance 85% at the ceiling 85.6%; next: item 35 study 3, port-town archive)
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
- 21 Nov 13:10-14:03: item 35 study 1 done (players' first hours, nine sessions, 8119ac4e7); study 4 first look (conversation filming, four conversations); advisor 292 (measuring block in every row) and 293 (friends play the browser evening before Unreal: into RULINGS, enforcer note) acknowledged; both pushed (the second commit at 14:00).

## In flight
- Nothing runs; no helpers; heavy lock untouched. Browser pane: a YouTube tab with a drawing canvas over it (reload clears it).
- Page tricks: YouTube's transcript panel ("Show transcript") appears only after a real scroll input in the hidden pane (computer scroll, then find); direct caption fetches return empty. Frames: define the sheet function after each navigate; keep the canvas under 790 px wide; launch the sheet without await and wait about 30-40 s, then zoom the screenshot; skip adverts first (.ad-showing). Five across at 158 px shows shot size; 131 px does not. Never write a "read at" time before reading the clock.

## Next, in order
000. Read the advisor channel first.
00. Allowance first: `python tools/pace_line.py <week> --fable <fable>`; the stop is 95% (week-shape.json hard_stop; the 75% lapsed at his 19 Nov Fable reset, advisor 284), ceiling line+25 capped at 95. Spare allowance before a reset funds planned or waiting work unasked (his rule 21 Nov, advisor 285).
0d. NOW (advisors 285, 286, 289): the PC measuring block: GTA VI's footage pass (lane branch's production/research/lane/gtavi/FOOTAGE-MEASURING.md; no spoiler to him), the footage studies (item 35), item 37, the feel block, then MEASUREMENTS-NEEDED's rows.
0e. Being seen (measurements/gtavi-being-seen-builder-2026-11-21.md, all counts there): S1 done; S3, S7, G4 sampled; G6 closed as footage allows; G5 one uncut escape and one map frame; open: re-identification on return, a second heat sample.
0f. Car chases DONE (d734c9aa0, 19 of 20; GTA IV row 5 open).
0g. Item 35: study 1 DONE (measurements/players-first-hours-sheet-2026-11-21.md); study 4 first look DONE (conversation-filming-sheet; more samples wanted: KCD2 free-talk entry, RDR2 one-to-one, 0.5 s steps). NEXT study 3: archive footage of British port towns 1989-90 (crowds, traffic, clothes, shopfronts, stance, smoking), about 3 PC h, questions first, browser only. Then study 2 (our prototype filmed by the same method; needs a tester run and Sonnet frame reading with Opus spot checks, so wait for room under the ceiling), then item 37 (district about 4 PC h, street life about 3 PC h), then the feel block. G3 car-entry seconds still need a free-roam clip; G5's second heat sample and re-identification still open (one lead in the players' sheet, Valkyrae 15:10, scripted).
- Allowance: at the ceiling (85% at 13:46 against 85.6%); work lean, no helpers. Cost so far about 1-2 weekly points per measured hour. Measuring block at 13:46: about 5.1 of 146 PC h (GTA VI 3.6 of 24.5, car chases done, players done); study 4 about 0.2 h since.
0. Verdicts and advisor as on the Row due line; row hourly.
0a. Advisor 277: Kiln, hair and the crowd paused until the browser evening holds; Kiln v1's Monday goal withdrawn.
0b. Night walk 21 Nov: 14 of 17; menu fix holds; his command-line sign-in done. Talk stages fix made 21 Nov 08:40 (try 1 of 2: route_walk presses T alone, waits for talk-open, comes round once, then play.py say --open); tonight's walk proves it: read talk-open's detail; the bench and picture check should pass now.
1. Paused with Kiln: Ron's seated hem cover try 2 of 2 (Fable legs lane; the 20 Nov FAIL film its acceptance view); fins try 3 brief READY (tool-dev/reports/BRIEF-KILN-LANE-FINS3-FABLE.md).
4. Marvelous export done 21 Nov (results F:/LedgerTools/md-jobs/export-2026-11-21.json; LOG.md Exports). Marvelous stays open (his word). No Unreal work until the browser prototype is done, then Kiln (advisor 288).
5. History rewrite: HELD for his word at the PC. Progress page daily from the live page (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: Marvelous bridge start 1/2 (19 Nov, four copies, his item); layered stage trace (no try); layered fix 2/2 (both failed 19 Nov: pass weighting, interleave; Fable next); trousers seat 2 tries (accepted 17:15); seated hem gap 1/2 (F5-a); coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 passed at try 1 (refit2); layered3 Fable 2/2 (set aside 19 Nov); jumper import 2 (the first failed on a missing budget line); blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

