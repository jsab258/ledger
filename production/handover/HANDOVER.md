# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-22 03:52 (the hourly run)

**Row due:** by 05:02 (last row 04:02; page read about 04:20: nothing new; filter verdicts after 2026-11-21T20:28 UTC, advisor after 22:45:00 +01:00; last ack 302 at 22:45)
**Uncommitted:** nothing (committed with G5 SOLID and the tester fix). Not mine, left alone: four Mickey's office prints modified in production/assets/office-print/mickeys.
**Stopped:** 2026-11-22 04:22 (the 03:52 run: G5 heat length SOLID at peak two stars, five reviewed samples from two players, a sixth unreviewed; one and three stars leads; the night walk did not start, tester start fixed, try 1 of 2; row 04:02; allowance 92%; stopped near the history point, 234k of 250k, as the next piece would cross it)
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
- 22 Nov 03:52-04:22: G5 heat length SOLID at peak two stars (m_2RP_EIHM8 one hour: seven spells, four clean two-star escapes, D three-star, two deaths, F split; JVXbhH7NRGw: J1 one star, J2 and J3 two stars); two fresh reviews (LEAD with corrections, then SOLID narrowly). 2EaoIgWAW5g rejected on date (stream started 18 Nov 19:49 UTC); fCofR6iJ3ZA rejected (18 Nov, re-processed). Tester start fix. Row 04:02.
- Lane feel sheets wait in F:/LedgerTools/tmp/lane-feel-mafia-out (no retry).


## In flight
- Nothing runs; no helpers; heavy lock clear.
- Page tools (lost on reload; rewrite): seekTo(v,t); starscan(t0,t1,step,cols,cw) and starscanT(times,cols,cw) crop x 0.854W-W, y 0-0.083H into a fixed canvas, labels UNDER cells; fsheetT(times,cols,cw) full frames. Canvas at most 6 x 130 px wide; poll window._r (45 s limit).
- Finding clips: WebSearch (allowed_domains youtube.com), then in a youtube tab fetch('/watch?v=ID') and read publishDate, lengthSeconds, startTimestamp (release 19 Nov).
- Night by a brightness scan every 2 min; stars read by eye (pixel measures read the sky).

## Next, in order
000. Read the advisor channel first.
00. Allowance first: `python tools/pace_line.py <week> --fable <fable>`; the stop is 95% (week-shape.json hard_stop; the 75% lapsed at his 19 Nov Fable reset, advisor 284), ceiling line+25 capped at 95. Spare allowance before a reset funds planned or waiting work unasked (his rule 21 Nov, advisor 285).
0d. NOW (advisors 285, 286, 289): the PC measuring block: GTA VI's footage pass (lane branch's production/research/lane/gtavi/FOOTAGE-MEASURING.md; no spoiler to him), the footage studies (item 35), item 37, the feel block, then MEASUREMENTS-NEEDED's rows.
0g. FIRST test one seek on mzGG (readyState 2 or more after seeking); if stuck, this run has no window on screen: only text work (clip dating, archive players), and stop early as 22 Nov 00:35 did. DEPTH FIRST (advisor 302): only numbers solid by STATUS.md's rule count; each piece aims at five uncut, dated samples, cheapest route first. NEXT, smallest first: G3 carjack set aside to Monday's reprice (two samples; a car taken at m_2RP 12:40 is a lead); G5 heat length: peak two stars SOLID 22 Nov (review 3; J3 about 91 s unreviewed, a fourth reviewer may add it); one star (two: 55, 75 s) and three stars (one: 322 s) stay leads; JVXbhH7NRGw (live, after release, 3 h 37 min) has a 6-star spell 13:30-27:30 and its 1-3.6 h unscanned: the next source for one and three stars; m_2RP 44:56-60:40 unread; r38SUFPeuew (read for cars 22 Nov; still for S3, S7, G5 deaths; no spoiler passed on); G7 a continuous post-release night walk downtown (mzGG's night is country); G8 repeated lines (captions only; m_2RP_EIHM8 has no captions); Q6 next archive record; item 35 study 2 (our prototype filmed) after the Monday reset; Monday's frame-reading trial.
- Allowance: 92% at 04:02, ceiling 95%. Log every step (timelog.py).
0. Verdicts and advisor as on the Row due line; row hourly.
0a. Advisor 277: Kiln, hair and the crowd paused.
0b. Night walk 22 Nov did NOT run: ALREADY-RUNNING on the 21 Nov 02:04 run left unfinished, its old process number reused by another program. Fixed 04:12 (play.py start and finish need the process to be the tester's own game; try 1 of 2; selftest 14/14; checked on the real record). Tonight's walk proves it, and the talk stages fix (try 1 of 2, 21 Nov 08:40) is still unproven: read talk-open's detail.
1. Paused with Kiln: Ron's seated hem cover try 2 of 2 (Fable legs lane; the 20 Nov FAIL film its acceptance view); fins try 3 brief READY (tool-dev/reports/BRIEF-KILN-LANE-FINS3-FABLE.md).
4. Marvelous export done 21 Nov (results F:/LedgerTools/md-jobs/export-2026-11-21.json; LOG.md Exports). Marvelous stays open (his word). No Unreal work until the browser prototype is done, then Kiln (advisor 288).
5. History rewrite: HELD for his word at the PC. Progress page daily from the live page (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 21-22 Nov: 'uncut' descriptions can be false; seeks hang in some runs (test one); run ci-checks alone (./tools/ci-checks.sh after unset MSYS_NO_PATHCONV; env -u bash is refused); stamps ran about 10 minutes ahead of the clock five times: Get-Date in its own call before every stamp.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: Marvelous bridge start 1/2 (19 Nov, four copies, his item); layered stage trace (no try); layered fix 2/2 (both failed 19 Nov: pass weighting, interleave; Fable next); trousers seat 2 tries (accepted 17:15); seated hem gap 1/2 (F5-a); coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 passed at try 1 (refit2); layered3 Fable 2/2 (set aside 19 Nov); jumper import 2 (the first failed on a missing budget line); blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

