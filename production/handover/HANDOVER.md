# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-21 11:33 (the hourly run)

**Row due:** by 12:52 (last row 11:52; page read 12:03: verdicts none after 2026-11-21T10:22 UTC, advisor none after the last ack 10:58 +01:00; filter verdicts after 2026-11-21T11:03 UTC, advisor after 12:03:00 +01:00)
**Stopped:** 2026-11-21 12:04 (history near its point, 225k of 250k, stopped at a clean break; allowance 83% at the ceiling; next: car chases, 0f)
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
- **Progress page (advisor 275):** each refresh reads the live page and publishes only progress.json and changed files; never an old index.html, never plan.json. Helpers only as project types: settings_check flags catch-all helpers (target under 2%).


## Done today
- 21 Nov 11:33-12:05: GTA VI driving M1-M3 set aside after two tries (no HUD speed; the chase view hides dashes behind a pickup; the first-person dial is covered); GTA V's sheet stands in. M10 first reading (camera about 2.2 m up, looking slightly down). G3: only edited shorts (rules as claims; one game message seen); its seconds wait for the launch streams. Car-chase sheet begun (rows K1-K9) with GTA VI chase 1 from LGU3b6jXhjI's notes. Pushed (cc28ad0b7). Notes: measurements/gtavi-driving-builder-2026-11-21.md, car-chases-sheet-2026-11-21.md.
- 21 Nov 10:50-11:31: advisors 289 and 290 acted on and pushed; G6 settled from the game's Help (Jx9flonxAqw); G5 begun.

## In flight
- Nothing runs; heavy lock free; no helpers. Browser pane: LGU3b6jXhjI open, paused, harmless.

## Next, in order
000. Read the advisor channel first.
00. Allowance first: `python tools/pace_line.py <week> --fable <fable>`; the stop is 95% (week-shape.json hard_stop; the 75% lapsed at his 19 Nov Fable reset, advisor 284), ceiling line+25 capped at 95. Spare allowance before a reset funds planned or waiting work unasked (his rule 21 Nov, advisor 285).
0d. NOW (advisors 285, 286, 289): the PC measuring block: GTA VI's footage pass (lane branch's production/research/lane/gtavi/FOOTAGE-MEASURING.md, lean order: being seen and G4-G6, then driving and G1-G3, fists, on foot; no spoiler to him), car chases (five each for GTA VI, GTA V, GTA IV, Sleeping Dogs, own sheet, about 3 h), the four footage studies (waiting item 35, players first), the feel block, then MEASUREMENTS-NEEDED's rows. Rows: game and verb, weekly points per measuring hour.
0e. Being seen (measurements/gtavi-being-seen-builder-2026-11-21.md, all counts there): S1 done; S3, S7, G4 sampled; G6 closed as far as footage allows; G5 has one uncut escape (Visual Lost to heat about 20 s, heat at least about 6 min) and one map frame. Still open: re-identification on return and a second heat sample, both from the launch streams in the players' study (item 35). Stars and icons: top-right 280x140 px of a 1080p frame; minimap bottom-left 360x440 from y 640.
0f. NEXT (car chases, advisor 286; sheet measurements/car-chases-sheet-2026-11-21.md): re-step LGU3b6jXhjI 6:30-8:10 at 6 s for K3-K5 (police cars in view, tactics, road, crashes). Frames came out black at 12:04 even with the frame-callback wait: after navigating, play the video for a second first so the stream loads, then pause and seek. Then GTA VI chases 2-5 (candidates on the sheet: 8-DRGbQ1IXc check its date; KZsskohjvlw skipping story parts), then GTA V, GTA IV, Sleeping Dogs, five each (older footage, no release-date issue). M10 on a daylight saloon frame (xgCY2UE55gM 2:04) when convenient. G3 seconds and G5's second heat sample come from the launch streams in the players' study.
- Page tricks (this session): pixels of the YouTube video are readable in a canvas, so frame differences can be counted in the page (a standstill scan: difference over a third of a second every 3 s); hidden-pane seeks slow to about 1 a second after a few hundred; screenshots often need a second try (the first times out); a canvas wider than the pane is clipped, so keep sheets to 4 columns.
- Allowance: at the ceiling (83% at 11:52 against 83.8%); work lean, no helpers, until the line climbs (about 0.8 point an hour).
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

