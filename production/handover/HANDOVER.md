# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-18 17:37 (the hourly run; the last session set its Stopped line at 17:05)

**Row due:** at the next start (last row 19:31; page and advisor read 21:20, last acks 230 and 231 at 21:25)
**Stopped:** 2026-11-18 17:05 (history OVER at an item's end; all helpers and my background runs stopped, leftover trees ended, lock clear; last commit pushed, this handover's final edits uncommitted: no notes-only commits)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). HIS GOAL THIS WEEK (advisor 220): Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits. Plan: F:/LedgerTools/tool-dev/reports/KILN-V1-CHECKLIST-2026-11-18.md (top of LOOP.md): 0 of 6 lines done. Pace: 20% at 19:31 against a line of 3.4% (+16.6, ahead: no new helpers until within 6; Fable 29% of its week). This week (RULINGS, his picks 17-18 Nov): eight helpers a session, Fable up to 40% on Kiln's hardest pieces, high effort on hard code and reviews.

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
- **Fable (advisors 227-228, to 23 Nov 13:00):** Kiln's hardest pieces (stiffness, Sheila's blouse, the trousers' legs) and any Kiln fault failing two Opus tries go to Fable at max (Agent model fable, effort max), given the problem, tries and numbers, no conclusion; never straight to a set-aside. Fable up to 40% of the week; rows name Fable helpers and share; Fable heavy runs first in the lock queue. final-reviewer and research-synthesis at effort high until 23 Nov 13:00, then medium.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads.
- **The heavy lock** F:/LedgerTools/tool-dev/runs/kiln-heavy.lockdir (mkdir as the lock, owner file inside, released at once) for every cargo/gate/drape run. A Kiln gate whose seconds matter runs alone.
- **Before writing Stopped: end every background job of your own, and check for runs your stopped helpers leave behind:** stopping a helper does NOT stop its bash scripts; at 12:20 four trees (legtorso sweeps, donkey, blouse) were still running and holding the lock. List processes matching kiln-lanes|sweep.py|regression_gate|heavy*.sh and taskkill /T each top bash; then clear the lock.
- **Lane rules file:** F:/LedgerTools/tool-dev/LANE-RULES.md (lane folders, the lock, tries, report lines, no clicks); every Kiln brief points to it; all nine briefs passed the permission check on 18 Nov.
- **Tries (RULINGS 7 Nov) over CLAUDE.md:** after two failed tries one genuinely different researched method; up to four while each closes the gap by a third with no new fault; none asks him. Helpers quote CLAUDE.md's 'third try needs his yes': correct them.
- **Helper spawns in an unattended run:** the permission check refuses some briefs (delete wording, cut runs); a leaner brief passes. Never retry a refused brief verbatim.
- Quay Run: on each driving study republish, copy its index.html to F:/LedgerTools/quay-run and run tools/driving_feel_check.py (advisor 222).
- **Storage and backup (advisors 196-198, 203):** writes and deletes only through retention.py and the storage map; nothing of his. Kiln's LOOP.md and reports folder joined the backup list today.


## Done this run (17:37 on; details in DECISIONS 17:40 on)
- Kiln main is 9b5141d (candidates 2 and 3 passed the whole gate alone; gate2.out, gate3.out in runs/kiln-merge-cand-2026-11-18; baseline still c52c3ab). Line 5: Kiln jobs run in Marvelous as written; copies in runs/kiln-md-compare-2026-11-18/jobs, runner run_md.sh [jobs]. DAILY-2026-11-18 pushed. Advisors 229-231 acknowledged.

## In flight at the stop
- No helpers running; the heavy lock is free. The stiffness2 lane build (1 GB on C:) is left in place.
- MARVELOUS IS STUCK: since 19:31 inside the bridge job md_work_trousers (busy.json), process idle, a second Marvelous window open (most likely an import box from ImportFBX). md-jobs/inbox still holds md_work_trousers.py. A scheduled run may not click; the page tool refuses an ACTION item for it (only_you: sign-in, purchase, licence, taste, his-setting). A session he starts at the desk may close it (computer use: Marvelous only, after 10 min idle). Send no more Marvelous jobs until busy.json clears.

## Next, in order
0. Verdicts after 2026-11-18T20:00:00Z; advisor after 2026-11-18T21:15:00+01:00 (last acks 230, 231 at 21:25). A row at once.
0a. ADVISOR 231 (his question why his yes was not on his page): the check is built: python tools/needs_you_page.py --waiting (not yet in ci-checks; it fails today on waiting items 11 and 20). In tomorrow's first batch put every line it names on his page, then add it to tools/ci-checks.sh, name it in rulings-enforcers.json with a RULINGS line within the cap, one item each with a recommendation: the Special Elite font (Apache 2.0 read at source, kind licence-off-list, recommend yes for the prototype only), waiting item 11's DINOv3 licence, and any other the check finds; nothing his rulings settle. The four prototype tools are done (allowlist ship-safe 13, THIRD-PARTY.md, waiting item 20 narrowed).
0b. ADVISOR 230: add to the next order's waiting list (when the 23 Nov order is written) the real game's phase plan checked against the prototype design once he approves it; RULINGS' prototype line within the cap if it fits (rounds build the approved design; the design traces every study line and ruling), enforcer the Monday audit. Quay Run already holds round 3 (check faults=0). The frame-time reading needs Chrome clicked on his PC: not allowed to computer use; for a desk session or his hands.
1. Stiffness steps 5-7: Fable 2 of 2 failed (see Tried); a third, genuinely different method only when pace allows a helper.
2. When pace is within 6 of the line: Fable on the coat (lane coat, Opus 2 of 2 failed; layout fixes uncommitted in the lane, diff copies in its run folder; open faults: the pattern check picks the sleeve tube as the hanging ring with the fronts open; collar stand through the neck = the donkey-start switch's fault), then legs, blouse, R4 (Fable priorities).
3. Ron's trousers M5 steps 6-10 on the borrowed leg values (KILN-V1-CHECKLIST line 3).
4. Line 5 drapes once Marvelous is free: method 3 is one .avt per body made once (Tom's route) instead of an FBX per job; trousers first as the check (tries 2 of 2 used on the FBX route).
5. Then n16-6, n16-8, n16-7.
6. Morning 19 Nov: the P4 table (tonight's long session is requested: production/playtest/nightly/long-session-request.json); Thursday's checkpoint (KILN-V1-CHECKLIST section c). The DAILY token file by 19:00 each day.
- tools/timelog.py start "<item> ..." at every task.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 18 Nov: Kiln stiffness 5-7 (Fable, lane stiffness2 82c87f1): switches off identical to main; switches on 2 of 2 failed, 26 lines outside (XPBD budget doubles solves; j3 must stretch past its cap; its 20 mm stage never calms). One different researched method may follow (KILN_XPBD_EQUIV its likely start) when pace allows.
- 18 Nov: Marvelous drape try 1: ImportAvatar takes .avt, so the job's body FBX never loaded (avatar false, nothing arranged); try 2 (ImportFBX as avatar) stalled inside Marvelous at its start.
- 18 Nov: coat try 2: layout fixed (950 to 0 cloth crossings) but the pattern check chose the sleeve tube as the hanging ring.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: 18 Nov coat 2 of 2 (to Fable); Marvelous line-5 drapes 2 of 2 on the FBX route (method 3 next); legs 2 of 2 plus a screen (Fable); J4 passed; skin-verdict passed; nylon-jam passed and merged; R4 1 of 2; blouse set aside (Fable). Earlier: git show 570374d9a:production/handover/HANDOVER.md.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 or 18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).
