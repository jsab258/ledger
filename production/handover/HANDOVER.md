# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-23 07:07 (the hourly run)

**Row due:** at 13:00 resume (page read 07:07: no verdicts; filter verdicts after 2026-11-23T06:07 UTC, advisor after 2026-11-23T07:10:00+01:00; last ack 319).
**Uncommitted:** nothing, but NOT PUSHED: the 07:10 commit (the order of 23 Nov, its page item). ci failed order-ledger (the new order has no item ledger; n16 and carried n09 items must be carried or closed in it, see tools/order_ledger.py) and progress-page; fix both at 13:00, then push. His page shows the order's gist, no file link.
**Stopped:** 2026-11-23 07:10 (the 07:07 run: advisor 317 moved the hold to 13:00; only the order of 23 Nov saved and its adoption item raised; advisors 309-319 acked; allowance 99%)

**Hold until:** 2026-11-23 13:00 (advisor 317: week at 99%; delete this line at 13:00 once resumed)
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
- 23 Nov 07:07-07:10: the order of 23 Nov saved, its adoption item on his page, advisors 309-319 acked.

## In flight
- Nothing runs; no helpers; heavy lock clear.
- Page tools (lost on reload; rewrite): seekTo(v,t); starscan(t0,t1,step,cols,cw) and starscanT(times,cols,cw) crop x 0.854W-W, y 0-0.083H into a fixed canvas, labels UNDER cells; fsheetT(times,cols,cw) full frames. Canvas at most 6 x 130 px wide; poll window._r (45 s limit).
- Finding clips: WebSearch (allowed_domains youtube.com), then in a youtube tab fetch('/watch?v=ID') and read publishDate, lengthSeconds, startTimestamp (release 19 Nov).
- Night by a brightness scan every 2 min; stars read by eye (pixel measures read the sky).

## Next, in order
0000. At 13:00 (advisor 317): read verdicts for 'adopt-order-2026-11-23'; on his yes do the order's section 1 point 6 (week-shape.json inactive, goal line to production/orders/2026-11-23.md). Then (1) 317's budget table from inZOI's and Silent Hill 2's files, about 3 h, then one page line that both can go; (2) 307's code measurers, the cheap-reader trial, the reprice by 20:00; (3) advisor 313: the C: folder list with sizes (safe/keep) in the first row, and the nightly package and walk paused to Sunday nights only; (4) the 13:30 audit in its new form (318, 319, judgement first, a fresh reviewer). The 00:41 and 05:41 night checks are answered in ack 319. 311 is withdrawn (312).
000a. FIRST AFTER THE MONDAY RESET (advisor 303; his words 22 Nov 08:22, "Dec 11 is way too late", efficiency ruling 11 Nov): redesign the measuring block to finish by Fri 27 Nov at the strict rule's quality: code reads the HUD (stars, timers, speed by template matching), cuts by frame difference, people by a local detector; models only label and spot-check; Monday's Sonnet/Haiku trial with Opus checks; one uncut long stream serves every study in it; coarse pass, fine steps only round events; parallel helpers; every row names its blueprint part and decision, others cut and listed; no-video rows to a cloud session. Advisor 304: frame labelling as scripted calls on his API credit (Haiku or Sonnet, whichever agrees with Opus spot checks), not the weekly allowance; key never printed, copied or committed; a spending stop at the month's remaining credit; the token file and reprice give credit used and left, cost per frame by model, hours it carries before 27 Nov. Advisor 305 (his words 22 Nov 09:07, "just need to use them up before they expire"): find this month's credit expiry and what is left; plan the frame labelling to use it all by then; if measuring alone will not, put other planned scripted work on it (talk reply labelling, Kiln render checks, review panel calibration, the checkers' AI players), cheapest agreeing model first; each daily token file shows expiry, used and left until spent. Reprice by Mon 23 Nov 20:00 (hours, points, finish date, cuts and why).
00. Allowance first: `python tools/pace_line.py <week> --fable <fable>`; the stop is 95% (week-shape.json hard_stop; the 75% lapsed at his 19 Nov Fable reset, advisor 284), ceiling line+25 capped at 95. Spare allowance before a reset funds planned or waiting work unasked (his rule 21 Nov, advisor 285).
0d. NOW (advisors 285, 286, 289): the PC measuring block: GTA VI's footage pass (lane branch's production/research/lane/gtavi/FOOTAGE-MEASURING.md; no spoiler to him), the footage studies (item 35), item 37, the feel block, then MEASUREMENTS-NEEDED's rows.
0g. GTA VI footage queue (depth first, advisor 302): the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover"; read it before the next footage piece.
0a. Advisor 277: Kiln, hair and the crowd paused.
0b. Night walk fixes unproven: play.py needs the tester's own game (try 1 of 2, 22 Nov 04:12) and the talk stages fix (try 1 of 2, 21 Nov); tonight's walk proves both (detail in TRIED-ARCHIVE.md).
1. Paused with Kiln: Ron's seated hem cover try 2 of 2 (Fable legs lane; the 20 Nov FAIL film its acceptance view); fins try 3 brief READY (tool-dev/reports/BRIEF-KILN-LANE-FINS3-FABLE.md).
4. Marvelous export done 21 Nov (results F:/LedgerTools/md-jobs/export-2026-11-21.json; LOG.md Exports). Marvelous stays open (his word). No Unreal work until the browser prototype is done, then Kiln (advisor 288).
5. History rewrite: HELD for his word at the PC. Progress page daily from the live page (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 21-22 Nov: 'uncut' descriptions can be false; seeks hang in some runs (test one); run ci-checks alone (./tools/ci-checks.sh after unset MSYS_NO_PATHCONV; env -u bash is refused); stamps ran about 10 minutes ahead of the clock five times: Get-Date in its own call before every stamp.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

