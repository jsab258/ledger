# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-19 05:46 (the hourly run; the 05:06 run set its Stopped line at 05:41)

**Row due:** by 07:07 (last row 06:07; page and advisor read 06:06: nothing new; last ack 00:54, advisor 237)
**Stopped:** 2026-11-19 05:41 (history at its point after the trousers' chain re-run; nothing of mine running, lock free; work committed with this file)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). HIS GOAL THIS WEEK (advisor 220): Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits. Plan: F:/LedgerTools/tool-dev/reports/KILN-V1-CHECKLIST-2026-11-18.md (top of LOOP.md): 0 of 6 lines done. Pace: 37% at 05:07 against 12.2% (+24.8), under the ceiling; Fable 45%, at its cap. This week (RULINGS, his picks 17-18 Nov): eight helpers a session, Fable up to 40% on Kiln's hardest pieces, high effort on hard code and reviews.

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
- **Page read-back, daily by the session (19 Nov):** the nightly task is off since 12 Nov; once a day query verdicts with "at" after the last read-back, out_dir production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8, then `python tools/page_answers.py --index` (ci's page-answers-fresh fails after 2 days).
- **The ceiling (advisor 237):** `python tools/pace_line.py <pct> --fable <pct>` prints it; above it the lane stops first, still above at the next row nothing new starts.
- **Storage and backup (advisors 196-198, 203):** writes and deletes only through retention.py and the storage map; nothing of his. Kiln's LOOP.md and reports folder joined the backup list today.


## Done this run (05:46 on; details in DECISIONS 05:51 on)
- Ron's trousers' seat, try 1 of 2 PASSED: --crotch-fade 0.04 (was 0.07; the centre seam runs crotch to waistband, so the fade held the seat's middle to the pelvis). Sitting body through 304 to 244 (bar 299), cloth inside 71 to 56 (listed; Tom's passed jeans 106); other poses clean. Kiln's own skin not taken (jeans sitting 159 inside). chain-boots/seat-try1/SEAT-TRY1-2026-11-19.md.
- Held row on wip (839c5dbff, from branch ron-kiln-trousers-import f867027fc): boots drape, seat-try1 skin, chain-boots wear maps, the twill tile; hold now "-WearHeld films only; released once the legs' start values are our own" (18 Nov 12:16).
- Imported into mh-assemble (first try raised: no budget kind for the folder; kind and parts line added, re-imported clean: 4 levels, MI_RonWorkTrousers); shipped PASS, assetBudgets OK; ci 108/108; pushed 49af3f1c5. The ue-probe junction shows the files at 05:56.
- Step 9: the passed jumper measured over the new trousers (clear_layers --measure): nearest 7.7 mm, none under 3: no re-clear, jumper untouched.
- Packaged build asked about 06:05 (nightly_package ASKED b279668f). Row 06:07 posted.
- Thursday's checkpoint drafted: F:/LedgerTools/tool-dev/reports/KILN-THURSDAY-CHECKPOINT-2026-11-19.md (tests 1 and 4 missed, 2 met with a listed count, 3 and 5 open).

## In flight at the stop
- The runner's packaged build (Runner.Worker) for the held film; no local Unreal or Kiln gate until it is gone. Nothing else of mine running; the heavy lock free.
- Ceiling: 38% at 06:07 against 38.1%; Fable 45% at cap.

## Next, in order
0. Verdicts after 2026-11-19T05:05 UTC; advisor after 2026-11-19T00:54:00+01:00 (last ack 237). Allowance, pace_line, a row (last 06:07).
1. Step 10, the held films: DONE standing on build b279668 (game log: Rocco wears RonWorkTrousers, RonJeans replaced): F:/LedgerTools/game-inputs/films/ron-work-trousers-2026-11-19/deg0, deg135, deg180 (through the office window: seat not seen), deg225, and the passed jeans on the same camera (jeans-deg0, jeans-deg135) as the before. Command: packaged LedgerProbe.exe -FaceAB -MouthFilm -MouthFilmWide -PreparedAck -WearHeld=RonWorkTrousers -FilmSize=2560x1440 -LedgerSlice -LedgerCrime -Encounter=live -LiveFresh -TalkFake -NoTitle -MouthFilmDeg=N -log (closes itself in about 3 min; frames in LedgerProbe/Saved/MouthFilm/BP_MH_RoccoP2_*). One fresh final reviewer ran on them: read REVIEW-1.md in that folder (round 1 of 2). By eye: the crotch hangs a little low and baggy. Still owed: a seated film and a back view of the seat (the film camera cannot see his back on the street), then his whole-person page with the films; release only once the legs' start values are our own.
2. Held-back run 1 on Thursday's main (quiet machine, heavy lock, the session runs it, no fixer told which); B2 and the speed table; then finish the checkpoint this evening.
3. Marvelous before 25 Nov: Darren's nylon jacket needs a body with a head; a look by eye at the three drapes; the money DECISION item by Tue 24 Nov.
4. Fable pieces (coat collar try 2, legs, blouse, R4) wait for Fable's reset Mon 13:00.
5. The DAILY token file by 19:00; the P4 table.
- tools/timelog.py start "<item> ..." at every task.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 19 Nov 05:54: the trousers' first import raised TypeError (int of None): a new garment folder needs its line in asset-budgets.json (folders and a parts entry), as Sheila's on 11 Nov.
- 19 Nov 05:52: the import worktree held a stale STAGED copy reversing its own last commit; git checkout -- restored the stale index, not HEAD: run git restore --staged first.
- 19 Nov 05:21: the trousers' boots job on Kiln main stopped at once on SetSeamlineZipper (renamed kiln_api.kiln_set_seam_zipper on 18 Nov); KILN_LEGACY_NAMES=1 runs the job unchanged.
- 19 Nov 05:20: coat on the joined lane: collar assembly inside the neck.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: trousers seat 1/2 (passed); coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 1/2; blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).
